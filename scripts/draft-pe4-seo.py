"""
PE-4 — Draft per-product SEO meta titles and meta descriptions for the Hero 100.

For each row in data/hero-100.csv:
  1. Fetch current title + current SEO title/description from Shopify (read-only).
  2. Ask Claude (Sonnet 4.6) to draft a new meta_title (<=60 chars) and
     meta_description (<=160 chars) in the BBI design-forward premium voice
     calibrated in docs/strategy/voice-samples.md and docs/strategy/icp.md.
  3. Append one row at a time to data/reports/pe4-hero100-seo-draft.csv.
     Resumable: re-runs skip handles that already have a draft row.

CSV columns:
  handle, current_title, current_meta_title, current_meta_desc,
  draft_meta_title, draft_title_chars,
  draft_meta_desc, draft_desc_chars,
  notes

Voice rules (from voice-samples.md / icp.md):
  - Lead with use case + brand + key spec
  - Canadian-English (centre, colour, metre)
  - Confident, not lifestyle ("Built for ..." not "Elevate ...")
  - Surface OECM / Canadian-made where natural — do not force
  - Keep model codes in titles where they exist
  - Branding lockup suffix on meta titles where length permits:
      `| Brant Business Interiors`  (full lockup is too long for <=60)

CSV-only output. No Shopify writes.

Usage:
  python3 scripts/draft-pe4-seo.py                      # full Hero 100
  python3 scripts/draft-pe4-seo.py --limit=5            # smoke test
  python3 scripts/draft-pe4-seo.py --handle=<handle>    # one product
  python3 scripts/draft-pe4-seo.py --refresh            # redo even if drafted
  python3 scripts/draft-pe4-seo.py --dry-run            # plan only, no API calls

Cost estimate: ~$0.005 per product × 100 = ~$0.50. No web search.
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Literal

import anthropic
from pydantic import BaseModel, Field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO_CSV = os.path.join(ROOT, 'data', 'hero-100.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'pe4-hero100-seo-draft.csv')

ENV_PATH = os.path.join(ROOT, '.env')
if not os.path.exists(ENV_PATH):
    # Worktrees inherit env from the main repo.
    ENV_PATH = '/Users/leokatz/Desktop/Office Central/.env'

with open(ENV_PATH) as f:
    ENV = dict(line.strip().split('=', 1) for line in f
               if '=' in line and not line.startswith('#'))

SHOPIFY_TOKEN = ENV['SHOPIFY_TOKEN']
SHOPIFY_STORE = ENV.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
ANTHROPIC_KEY = ENV['ANTHROPIC_API_KEY']

GRAPHQL_URL = f'https://{SHOPIFY_STORE}/admin/api/2026-04/graphql.json'
SHOPIFY_HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_TOKEN,
    'Content-Type': 'application/json',
}

MODEL = 'claude-sonnet-4-6'
SDK_MAX_RETRIES = 8
COST_HARD_CAP = 5.00  # generous cap for SEO drafting

CSV_FIELDS = [
    'handle',
    'current_title',
    'current_meta_title',
    'current_meta_desc',
    'draft_meta_title',
    'draft_title_chars',
    'draft_meta_desc',
    'draft_desc_chars',
    'notes',
]

SYSTEM_PROMPT = """You are an SEO copywriter for Brant Business Interiors (BBI), a Canadian B2B office furniture dealer based in Richmond Hill, Ontario, operating as a division of Office Central Inc. — a verified OECM Supplier Partner.

You draft SEO meta titles and meta descriptions for products in BBI's Hero 100 catalog.

## Voice (locked — do not deviate)

- **Confident, not lifestyle.** "Built for a private office that does real work" is in. "Elevate your workday" is out.
- **Lead with use case + brand + key spec** in that order, when it fits.
- **Canadian-English spelling.** centre, colour, metre, organisation, customise.
- **Keep model codes / SKU codes** if present in the product title (e.g. `1240-3`, `MVL2756`, `9300 Series`). Procurement teams search by code.
- **Surface OECM or Canadian-made where it lands naturally.** Do NOT force them on every product. OECM matters most on institutional-leaning SKUs (waiting room seating, bariatric, training tables, big-and-heavy chairs, fire-resistant filing). Canadian-made matters most on Global Furniture Group, Teknion, Keilhauer, ergoCentric, ObusForme products. If neither fits cleanly, omit them.
- **Avoid lifestyle puffery.** No "unleash", "elevate", "transform", "discover", "dream", "boldly".
- **Avoid ALL-CAPS, emojis, and clickbait.**

## Hard rules

- `meta_title`: **strictly <= 60 characters** including spaces and brand suffix.
- `meta_description`: **strictly <= 160 characters** including spaces. Should be a full thought (subject + verb + benefit), not a fragment.
- Always include the product type (chair / desk / cabinet / table / etc).
- Where length permits, end the meta_title with ` | Brant Business Interiors` (28 chars). If that doesn't fit, drop the suffix entirely — never produce a 61+ char title to keep the suffix.
- The meta description should be unique to this product — not a category boilerplate. Reference the actual product type, brand, and a real spec or use case.
- Never invent specs you weren't given. If a spec is unclear, lean on use case and brand language only.

## Output

Return a `MetaDraft` JSON object. The `notes` field is for short reviewer flags ("OECM-leaning", "code preserved", "no brand suffix — title at cap"). Empty string is fine.
"""


# ---------------------------------------------------------------------------
# Pydantic schema for structured outputs
# ---------------------------------------------------------------------------
class MetaDraft(BaseModel):
    meta_title: str = Field(
        description='SEO meta title, max 60 characters including spaces and any brand suffix.',
        max_length=60,
    )
    meta_description: str = Field(
        description='SEO meta description, max 160 characters including spaces. A full thought, not a fragment.',
        max_length=160,
    )
    notes: str = Field(
        default='',
        description='Short reviewer flag (e.g. "OECM-leaning", "code preserved"). Empty string if nothing to flag.',
    )


# ---------------------------------------------------------------------------
# Shopify GraphQL helpers
# ---------------------------------------------------------------------------
def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    for attempt in range(5):
        req = urllib.request.Request(GRAPHQL_URL, data=payload,
                                     headers=SHOPIFY_HEADERS, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 2 + attempt * 2
                print(f'      · Shopify {e.code} — backoff {wait}s', file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        if data.get('errors'):
            err = json.dumps(data['errors'])[:200]
            if 'THROTTLED' in err.upper():
                time.sleep(2 + attempt * 2)
                continue
            raise RuntimeError(f'GraphQL errors: {err}')
        return data['data']
    raise RuntimeError('GraphQL gave up after retries')


def fetch_seo_for_handles(handles: list[str]) -> dict[str, dict]:
    """Bulk-fetch current title + SEO fields for all handles in one paginated query.

    Returns: {handle: {title, seo_title, seo_description}}
    """
    out: dict[str, dict] = {}
    pending = list(handles)
    # Paginate in groups of 50 to keep query cost reasonable.
    BATCH = 50
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        # Use search "handle:foo OR handle:bar..." then iterate. Simpler:
        # productByHandle aliases keep it deterministic.
        aliases = '\n'.join(
            f'  p{i}: productByHandle(handle: "{h}") {{ handle title seo {{ title description }} }}'
            for i, h in enumerate(chunk)
        )
        data = gql('{\n' + aliases + '\n}')
        for i, h in enumerate(chunk):
            node = data.get(f'p{i}')
            if not node:
                out[h] = {'title': '', 'seo_title': '', 'seo_description': ''}
                continue
            out[h] = {
                'title': node.get('title') or '',
                'seo_title': (node.get('seo') or {}).get('title') or '',
                'seo_description': (node.get('seo') or {}).get('description') or '',
            }
        time.sleep(0.6)  # gentle on Shopify rate limit
    return out


# ---------------------------------------------------------------------------
# Claude call
# ---------------------------------------------------------------------------
def estimate_cost(usage) -> float:
    # Sonnet 4.6: $3/$15 per 1M
    in_t = usage.input_tokens
    out_t = usage.output_tokens
    cw = getattr(usage, 'cache_creation_input_tokens', 0) or 0
    cr = getattr(usage, 'cache_read_input_tokens', 0) or 0
    return (
        in_t * 3.0 / 1_000_000
        + out_t * 15.0 / 1_000_000
        + cw * 3.0 * 1.25 / 1_000_000
        + cr * 3.0 * 0.10 / 1_000_000
    )


def draft_one(client: anthropic.Anthropic, row: dict, current: dict) -> tuple[MetaDraft, float]:
    user_prompt = (
        f"Product to draft SEO meta for:\n"
        f"  Handle: {row['handle']}\n"
        f"  Storefront title: {current['title'] or row['title']}\n"
        f"  Hero rank: #{row['hero_rank']} (revenue: ${row['sold_revenue']:,.0f})\n"
        f"  Type tag: {row.get('type_tag', '')}\n"
        f"  Current meta_title: {current['seo_title'] or '(empty — Shopify falls back to product title)'}\n"
        f"  Current meta_description: {current['seo_description'] or '(empty — Shopify uses storefront default)'}\n"
        f"\n"
        f"Draft a fresh meta_title (<=60 chars) and meta_description (<=160 chars). "
        f"Voice rules in the system prompt are absolute. Do not exceed the character "
        f"caps. If the brand-suffix won't fit, drop it."
    )

    resp = client.messages.parse(
        model=MODEL,
        max_tokens=600,
        system=[
            {
                'type': 'text',
                'text': SYSTEM_PROMPT,
                'cache_control': {'type': 'ephemeral'},
            },
        ],
        messages=[{'role': 'user', 'content': user_prompt}],
        output_format=MetaDraft,
    )
    cost = estimate_cost(resp.usage)
    return resp.parsed_output, cost


# ---------------------------------------------------------------------------
# CSV resume helpers
# ---------------------------------------------------------------------------
def load_existing_handles(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    seen: set[str] = set()
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            if row.get('handle'):
                seen.add(row['handle'])
    return seen


def append_row(path: str, row: dict) -> None:
    new_file = not os.path.exists(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            w.writeheader()
        w.writerow({k: row.get(k, '') for k in CSV_FIELDS})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def load_hero_100() -> list[dict]:
    rows: list[dict] = []
    with open(HERO_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append({
                'hero_rank': int(r['hero_rank']),
                'handle': r['handle'],
                'title': r['title'],
                'type_tag': r.get('type_tag', ''),
                'sold_revenue': float(r.get('sold_revenue', 0) or 0),
            })
    return rows


def main() -> int:
    args = sys.argv[1:]
    refresh = '--refresh' in args
    dry_run = '--dry-run' in args
    limit: int | None = None
    only_handle: str | None = None
    for a in args:
        if a.startswith('--limit='):
            limit = int(a.split('=', 1)[1])
        if a.startswith('--handle='):
            only_handle = a.split('=', 1)[1]

    rows = load_hero_100()
    if only_handle:
        rows = [r for r in rows if r['handle'] == only_handle]
    if limit:
        rows = rows[:limit]

    print(f'Hero rows to process: {len(rows)}')
    print(f'Output: {OUT_CSV}')

    existing = set() if refresh else load_existing_handles(OUT_CSV)
    if existing and not refresh:
        print(f'  Resume mode: {len(existing)} handles already drafted, will skip')

    todo = [r for r in rows if r['handle'] not in existing]
    print(f'  To draft now: {len(todo)}')
    if not todo:
        print('Nothing to do.')
        return 0

    if dry_run:
        print('\n[DRY RUN] First 5 to be drafted:')
        for r in todo[:5]:
            print(f"  - {r['handle']}  ({r['title'][:60]})")
        return 0

    print('\nFetching current Shopify SEO fields...')
    current_by_handle = fetch_seo_for_handles([r['handle'] for r in todo])

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY, max_retries=SDK_MAX_RETRIES)
    total_cost = 0.0
    drafted = 0
    failed = 0

    for r in todo:
        if total_cost >= COST_HARD_CAP:
            print(f'\n⛔  Cost cap ${COST_HARD_CAP:.2f} reached — stopping. Re-run to resume.')
            break

        cur = current_by_handle.get(r['handle'], {'title': '', 'seo_title': '', 'seo_description': ''})

        print(f"[{r['hero_rank']:>3}] {r['handle']}")
        try:
            draft, cost = draft_one(client, r, cur)
        except (anthropic.APIError, anthropic.APIStatusError) as e:
            print(f"      → API ERROR: {e}")
            append_row(OUT_CSV, {
                'handle': r['handle'],
                'current_title': cur['title'],
                'current_meta_title': cur['seo_title'],
                'current_meta_desc': cur['seo_description'],
                'draft_meta_title': '',
                'draft_title_chars': 0,
                'draft_meta_desc': '',
                'draft_desc_chars': 0,
                'notes': f'API_ERROR: {str(e)[:100]}',
            })
            failed += 1
            continue
        except Exception as e:
            print(f"      → UNEXPECTED: {e}")
            failed += 1
            continue

        total_cost += cost
        title_len = len(draft.meta_title)
        desc_len = len(draft.meta_description)
        flags = []
        if title_len > 60:
            flags.append(f'TITLE_OVER_60={title_len}')
        if desc_len > 160:
            flags.append(f'DESC_OVER_160={desc_len}')
        notes = (draft.notes or '').strip()
        if flags:
            notes = (notes + '; ' if notes else '') + ' '.join(flags)

        append_row(OUT_CSV, {
            'handle': r['handle'],
            'current_title': cur['title'],
            'current_meta_title': cur['seo_title'],
            'current_meta_desc': cur['seo_description'],
            'draft_meta_title': draft.meta_title,
            'draft_title_chars': title_len,
            'draft_meta_desc': draft.meta_description,
            'draft_desc_chars': desc_len,
            'notes': notes,
        })
        drafted += 1
        print(f"      → t={title_len}c d={desc_len}c  ${cost:.4f}  (total ${total_cost:.2f})")

    print()
    print('=' * 60)
    print(f'Drafted: {drafted}    Failed: {failed}    Cost: ${total_cost:.2f}')
    print(f'CSV: {OUT_CSV}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
