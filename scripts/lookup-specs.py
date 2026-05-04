"""
Look up structured spec data for the Hero 100 via Claude API + web search.

Replaces the original POI-scraping plan because POI's catalog (Steelcase-only)
has zero overlap with BBI's Hero 100 (Global / OTG / ObusForme). Instead of
building 3 brittle site scrapers, this calls Claude Opus 4.7 with web search
once per product and structured-outputs the result.

For each Hero product:
  1. Pull title, brand hint (detected from title patterns), velocity rank.
  2. Send to Claude Opus 4.7 with web_search tool + adaptive thinking.
  3. Claude searches manufacturer/dealer sites and returns a normalized
     `ProductSpecs` JSON object (dimensions, finishes, features, etc.).
  4. Save per-product to `data/specs/{handle}.json` (resumable — re-runs skip
     handles that already have a file).
  5. Aggregate all files into `data/specs.json`.

Usage:
  python3 scripts/lookup-specs.py                  # full Hero 100
  python3 scripts/lookup-specs.py --limit=5        # first 5 only (smoke test)
  python3 scripts/lookup-specs.py --handle=zira-u-shape-...   # one product
  python3 scripts/lookup-specs.py --refresh        # re-fetch even if cached
  python3 scripts/lookup-specs.py --aggregate-only # just rebuild specs.json

Cost estimate: ~$0.05–0.15 per product → ~$5–15 for the full Hero 100.
"""
import csv
import json
import math
import os
import re
import sys
import time
from typing import List, Literal

import anthropic
from pydantic import BaseModel, Field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO_CSV = os.path.join(ROOT, 'data', 'hero-100.csv')
SPECS_DIR = os.path.join(ROOT, 'data', 'specs')
AGGREGATE_JSON = os.path.join(ROOT, 'data', 'specs.json')

MODEL = 'claude-sonnet-4-6'  # ~60% cheaper than Opus 4.7; spec extraction doesn't need Opus

# Anthropic Tier 1 caps Sonnet 4.6 at ~50k input tokens/min. Each web_search
# call burns ~30k input tokens, so we must wait between calls. SDK auto-retry
# handles transient 429s with backoff.
SDK_MAX_RETRIES = 10
COST_HARD_CAP = 10_000.00  # effectively disabled — run until API funds exhausted
# Tier 1 rate limit: 30,000 input tokens / minute.
# Dynamic throttle: wait ceil(last_input_tokens / 30000) * 60 + 5s buffer.
# Minimum 30s, so short calls still get a breathing gap.
RATE_LIMIT_TOKENS_PER_MIN = 30_000

SYSTEM_PROMPT = """You are a product spec researcher for Brant Business Interiors (BBI), a Canadian B2B office furniture dealer. You look up structured product specifications for furniture in BBI's catalog so the catalog can be enriched with accurate dimensions, materials, finishes, and features.

## Your job

For each product the user gives you, search the web and return a structured `ProductSpecs` object. The data will feed into:
- standardized product titles (model code + key spec)
- filter tags (`finish:*`, `brand:*`, `feature:*`)
- rewritten product descriptions
- spec tables on each product page

## Search strategy

1. **Manufacturer site first.** BBI's catalog is mostly Global Furniture Group (globalfurnituregroup.com), OTG / Offices to Go (officestogo.com), and ObusForme Comfort. The manufacturer site is the authoritative spec source — start there. Look for the product's spec sheet PDF if the page itself omits dimensions.
2. **Authorized Canadian dealers as fallback.** If the manufacturer site is sparse: torontoofficefurniture.com (carries Global + OTG), abcogroup.ca (carries Global), officestock.com (carries ObusForme).
3. **Avoid irrelevant sources.** Do not pull spec data from Steelcase, Herman Miller, Knoll, etc. — BBI doesn't carry those brands. POI Business Interiors (poi.ca) is a Steelcase-only dealer; ignore it.
4. **Brand model codes are the key signal.** OTG codes look like `MVL2756`, `OTG10703B`. Global codes look like `GLB74475`. ObusForme codes look like `1240-3`. If the product title contains a model code, use it as your primary search query.

## Output rules

- **Never fabricate.** If a field is unknown after searching, leave it null/empty and lower the confidence score.
- **Do not copy marketing prose.** Pull factual specs only — dimensions, materials, finishes, certifications. Leave the description writing to a separate step.
- **Cite real source URLs.** `source_urls` should contain only URLs you actually loaded.
- **Confidence calibration.**
  - `high` = manufacturer site loaded with structured spec data
  - `medium` = authorized dealer with partial spec data
  - `low` = inferred from product line / brand defaults, not a specific page
  - `none` = could not find anything reliable
- **Finishes:** list distinct finish/colour names (e.g. `["Walnut", "White", "Black", "Designer White"]`). Lowercase is fine; normalization happens later.
- **Features:** short factual phrases, not marketing copy. Good: "Synchro-tilt mechanism", "BIFMA compliant", "5-year warranty". Bad: "Designed to elevate your workday".
- **Certifications:** specific cert names — BIFMA, GREENGUARD, LEVEL, FSC, LEED-contributing, AODA-compliant, etc.
- **Model codes:** all SKU/model codes you find for this product line, including variants (e.g. for a chair line: `["MVL2756", "MVL2756B", "MVL2756L"]`).

If a product is unbranded / custom (e.g. "Medicine Wheel Table", "Innovation L-Shape Set" with no manufacturer detectable), return `confidence: "none"` with a brief note explaining what you searched."""


class ProductSpecs(BaseModel):
    """All string fields are REQUIRED — return empty string ("") when unknown.
    All list fields default to []. This avoids JSON-schema `null` unions which
    break the structured-outputs validator (500)."""
    confidence: Literal['high', 'medium', 'low', 'none'] = Field(
        description='How reliable is this spec data?'
    )
    source_urls: List[str] = Field(
        description='URLs actually loaded during search (manufacturer site, dealer page, spec sheet PDF). Empty list if none.',
    )
    manufacturer: str = Field(
        description='Brand / manufacturer name (e.g. "Global Furniture Group", "OTG / Offices to Go", "ObusForme Comfort"). Empty string if unknown.',
    )
    product_line: str = Field(
        description='Manufacturer\'s product line name (e.g. "Zira", "Overtime", "Premium Series"). Empty string if unknown.',
    )
    model_codes: List[str] = Field(
        description='All SKU / model codes for this product line variants. Empty list if unknown.',
    )
    dimensions: str = Field(
        description='Physical dimensions in W x D x H format (e.g. "72\\"W x 36\\"D x 29\\"H"). Include all sizes if multiple are offered. Empty string if unknown.',
    )
    weight: str = Field(
        description='Product weight (e.g. "45 lbs"). Empty string if unknown.',
    )
    weight_capacity: str = Field(
        description='Weight capacity for chairs / load-bearing products (e.g. "300 lbs", "500 lbs heavy-duty"). Empty string if not applicable or unknown.',
    )
    materials: str = Field(
        description='Primary materials (e.g. "Thermofused laminate top, steel frame, mesh back"). Empty string if unknown.',
    )
    finishes_available: List[str] = Field(
        description='List of finish / colour options available. Empty list if unknown.',
    )
    key_features: List[str] = Field(
        description='Factual feature bullets (mechanisms, adjustments, included options). Empty list if unknown.',
    )
    certifications: List[str] = Field(
        description='Specific certification names (BIFMA, GREENGUARD, LEVEL, FSC, AODA-compliant, etc.). Empty list if none found.',
    )
    warranty: str = Field(
        description='Warranty terms if stated (e.g. "10-year limited warranty"). Empty string if unknown.',
    )
    country_of_manufacture: str = Field(
        description='Where the product is manufactured (e.g. "Canada — Mississauga, ON"). Empty string if unknown.',
    )
    notes: str = Field(
        description='Caveats, ambiguities, or anything the reviewer should know. Empty string if none.',
    )


def detect_brand_hint(title: str) -> str:
    t = title.lower()
    if re.search(r'\bmvl\d+\b', title, re.I) or re.search(r'\botg\d+\b', title, re.I):
        return 'OTG / Offices to Go (look for MVL or OTG model code)'
    if re.search(r'\bglb\d+\b', title, re.I):
        return 'Global Furniture Group (look for GLB model code)'
    if 'obusforme' in t:
        return 'ObusForme Comfort'
    if any(k in t for k in ['zira', 'premium series', 'foundations', 'roma', 'sidero']):
        return 'Likely Global Furniture Group'
    if any(k in t for k in ['overtime', 'ibex', 'caman', 'format ', 'ashmont', 'chevron', 'vion']):
        return 'Likely OTG / Offices to Go'
    if 'medicine wheel' in t or 'indigenous' in t:
        return 'Custom / Indigenous-made — likely no manufacturer page'
    return 'Brand unknown — search title to identify manufacturer'


def load_hero_100() -> List[dict]:
    rows = []
    with open(HERO_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({
                'hero_rank': int(r['hero_rank']),
                'handle': r['handle'],
                'title': r['title'],
                'type_tag': r['type_tag'],
                'sold_revenue': float(r['sold_revenue']),
            })
    return rows


def lookup_one(client: anthropic.Anthropic, product: dict) -> dict:
    brand_hint = detect_brand_hint(product['title'])
    user_prompt = (
        f"Product to research:\n"
        f"  Title: {product['title']}\n"
        f"  Brand hint: {brand_hint}\n"
        f"  Hero rank: #{product['hero_rank']} (revenue: ${product['sold_revenue']:,.0f})\n"
        f"  Type: {product['type_tag']}\n\n"
        f"Search the web and return the structured spec data."
    )

    resp = client.messages.parse(
        model=MODEL,
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        tools=[{
            'type': 'web_search_20260209',
            'name': 'web_search',
            'max_uses': 2,
            'allowed_domains': [
                'globalfurnituregroup.com',
                'officestogo.com',
                'obusformecomfort.com',
                'torontoofficefurniture.com',
                'abcogroup.ca',
                'officestock.com',
            ],
        }],
        messages=[{'role': 'user', 'content': user_prompt}],
        output_format=ProductSpecs,
    )

    specs = resp.parsed_output
    return {
        'handle': product['handle'],
        'title': product['title'],
        'hero_rank': product['hero_rank'],
        'brand_hint': brand_hint,
        'specs': specs.model_dump() if specs else None,
        'usage': {
            'input_tokens': resp.usage.input_tokens,
            'output_tokens': resp.usage.output_tokens,
            'cache_creation_input_tokens': resp.usage.cache_creation_input_tokens or 0,
            'cache_read_input_tokens': resp.usage.cache_read_input_tokens or 0,
        },
        'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    }


def estimate_cost(usage: dict) -> float:
    # Sonnet 4.6: $3/$15 per 1M, cache write 1.25x, cache read 0.1x
    in_tok = usage['input_tokens']
    out_tok = usage['output_tokens']
    cache_w = usage['cache_creation_input_tokens']
    cache_r = usage['cache_read_input_tokens']
    return (
        in_tok * 3.0 / 1_000_000
        + out_tok * 15.0 / 1_000_000
        + cache_w * 3.0 * 1.25 / 1_000_000
        + cache_r * 3.0 * 0.10 / 1_000_000
    )


def aggregate() -> None:
    out = {}
    if not os.path.isdir(SPECS_DIR):
        print(f'[aggregate] no specs dir at {SPECS_DIR}')
        return
    for fn in sorted(os.listdir(SPECS_DIR)):
        if not fn.endswith('.json'):
            continue
        with open(os.path.join(SPECS_DIR, fn), encoding='utf-8') as f:
            data = json.load(f)
        out[data['handle']] = data
    with open(AGGREGATE_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f'[aggregate] wrote {len(out)} entries → {os.path.relpath(AGGREGATE_JSON, ROOT)}')


def main() -> None:
    args = sys.argv[1:]
    aggregate_only = '--aggregate-only' in args
    refresh = '--refresh' in args
    limit = None
    only_handle = None
    for arg in args:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
        if arg.startswith('--handle='):
            only_handle = arg.split('=', 1)[1]

    if aggregate_only:
        aggregate()
        return

    os.makedirs(SPECS_DIR, exist_ok=True)
    products = load_hero_100()
    if only_handle:
        products = [p for p in products if p['handle'] == only_handle]
    if limit:
        products = products[:limit]

    with open(os.path.join(ROOT, '.env')) as f:
        env = dict(line.strip().split('=', 1) for line in f if '=' in line)
    client = anthropic.Anthropic(
        api_key=env['ANTHROPIC_API_KEY'],
        max_retries=SDK_MAX_RETRIES,
    )
    total_cost = 0.0
    done = 0
    skipped = 0
    last_call_at = 0.0
    last_input_tokens = 0  # used to compute dynamic throttle

    for p in products:
        out_path = os.path.join(SPECS_DIR, f"{p['handle']}.json")
        if os.path.exists(out_path) and not refresh:
            skipped += 1
            continue

        # Dynamic throttle: wait enough for the previous call's tokens to clear the
        # per-minute rate limit window, minimum 30s.
        if last_call_at:
            minutes_needed = math.ceil(last_input_tokens / RATE_LIMIT_TOKENS_PER_MIN)
            required_gap = max(30, minutes_needed * 60 + 5)
            elapsed = time.time() - last_call_at
            if elapsed < required_gap:
                wait = required_gap - elapsed
                print(f'      (throttle {wait:.0f}s for rate limit)')
                time.sleep(wait)

        if total_cost >= COST_HARD_CAP:
            print(f'\n⛔  Hard cap ${COST_HARD_CAP:.2f} reached — stopping. Run again to continue.')
            break

        print(f"[{p['hero_rank']:>3}] {p['title'][:70]}")
        last_call_at = time.time()
        try:
            result = lookup_one(client, p)
        except anthropic.APIError as e:
            print(f"      → API ERROR: {e}")
            continue

        last_input_tokens = (
            result['usage']['input_tokens']
            + result['usage']['cache_creation_input_tokens']
            + result['usage']['cache_read_input_tokens']
        )
        cost = estimate_cost(result['usage'])
        total_cost += cost
        confidence = result['specs']['confidence'] if result['specs'] else 'parse-failed'
        print(f"      → confidence={confidence}  ${cost:.4f}  (running total: ${total_cost:.2f})")

        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        done += 1

    print(f'\nDone: {done} fetched, {skipped} skipped (cached). Total cost: ${total_cost:.2f}')
    aggregate()


if __name__ == '__main__':
    main()
