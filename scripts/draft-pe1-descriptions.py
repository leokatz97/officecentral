"""
PE-1 — Draft long-form HTML product descriptions for the Hero 100.

For each Hero 100 product, ask Claude to write a structured product
description in BBI's locked voice: lead paragraph + Key features bullets
+ optional Best for / Services line. Output is HTML body suitable for
Shopify's `descriptionHtml` field.

Output: data/reports/pe1-hero100-descriptions.csv
Resumable: re-runs skip handles already drafted.

Usage:
  python3 scripts/draft-pe1-descriptions.py             # full Hero 100
  python3 scripts/draft-pe1-descriptions.py --limit=5   # canary
  python3 scripts/draft-pe1-descriptions.py --handle=<h>
  python3 scripts/draft-pe1-descriptions.py --refresh

Cost: ~$0.02 / row × 100 ≈ $2.00.
"""
from __future__ import annotations
import csv, json, os, re, sys, time
import urllib.error, urllib.request

import anthropic
from pydantic import BaseModel, Field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO_CSV = os.path.join(ROOT, 'data', 'hero-100.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'pe1-hero100-descriptions.csv')
ENV_PATH = os.path.join(ROOT, '.env')
if not os.path.exists(ENV_PATH):
    ENV_PATH = '/Users/leokatz/Desktop/Office Central/.env'
with open(ENV_PATH) as f:
    ENV = dict(line.strip().split('=', 1) for line in f
               if '=' in line and not line.startswith('#'))

SHOPIFY_TOKEN = ENV['SHOPIFY_TOKEN']
SHOPIFY_STORE = ENV.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
ANTHROPIC_KEY = ENV['ANTHROPIC_API_KEY']
GRAPHQL_URL = f'https://{SHOPIFY_STORE}/admin/api/2026-04/graphql.json'
SHOPIFY_HEADERS = {'X-Shopify-Access-Token': SHOPIFY_TOKEN, 'Content-Type': 'application/json'}
MODEL = 'claude-sonnet-4-6'
COST_HARD_CAP = 8.00

CSV_FIELDS = ['handle', 'current_desc_first_200c', 'draft_body_html',
              'draft_word_count', 'notes']

SYSTEM_PROMPT = """You are a product copywriter for Brant Business Interiors,
a Canadian B2B office furniture dealer operating as a division of Office Central
Inc. — a verified OECM (Ontario Education Collaborative Marketplace) Supplier
Partner serving institutional and commercial buyers across Ontario.

You write long-form HTML product descriptions for the Hero 100 catalog.

## ICP context

Buyers are B2B Canadian procurement professionals: office administrators at
non-profits, family health teams, First Nations band offices, school boards,
municipalities, and small hospitals (Primary ICP, ~60% of revenue); and office
managers at Ontario SMB private-sector firms — manufacturing, professional
services, trades, logistics (Secondary ICP, ~40%). Not consumer e-commerce.
They need: durability, real specs, procurement-friendly language, and confidence
this is a commercial-grade Canadian supplier.

## Voice (locked — do not deviate)

- **Design-forward and premium, but grounded.** Lead with the workspace feeling
  and the use case, not a spec dump. "Built for a private office that does real
  work" is in. "Elevate your workday" is out. Think "thoughtfully designed for
  the way you actually work" — not lifestyle, not SKU-sheet.
- **Bold one-line hook as the opener. Required on every product.** The very
  first line of the HTML body must be a `<p><strong>` hook: one sentence,
  use-case or promise, no spec. Examples from the locked voice guide:
    "Built for a private office that does real work."
    "The chair that keeps your back where it should be."
    "Training-room tables that get out of the way when the room needs to do
    something else."
  Not acceptable: "This L-Shape Desk & Hutch is a practical choice..." (flat
  declarative). Not acceptable: opening with a spec or dimension.
- **Canadian-English spelling.** Use: centre, colour, metre, organization,
  customize, aluminum. The ICP locks centre/colour/metre; for -ize/-ise and
  aluminum/aluminium, follow Canadian Press style (organize, customize, aluminum).
- **Procurement-first language.** Surface model codes, sizes, capacities,
  materials, certifications. Procurement teams search by SKU.
- **Lead-time language: never commit to specific windows.** Do not write
  "4–6 weeks", "5–10 business days", or any concrete number. Use "ships from
  Ontario stock", "Quick Ship item", or push to the phone: "Call
  1-800-835-9565 for current lead times." If a Quick Ship claim appears in
  the source, surface it. Otherwise omit lead-time language entirely.
- **Delivery language: safe defaults only.** "Delivery across Ontario" and
  "installation available in Ontario" are approved. Do not promise specific
  carriers, dates, or free shipping unless confirmed in the source.
- **OECM + Office Central moat — surface on institutional-leaning SKUs.**
  Office Central's OECM Supplier status is Brant Business Interiors' biggest
  competitive differentiator for institutional buyers (school boards, hospitals,
  municipalities, band offices). Where OECM is relevant, use the locked phrase:
  "a division of Office Central Inc., a verified OECM Supplier Partner." Do NOT
  force OECM on every product — reserve for institutional-leaning SKUs (waiting
  room seating, bariatric, training tables, heavy-duty task chairs, fire-resistant
  filing, reception desks for public-facing spaces).
- **Surface Canadian-made on Global, Teknion, Keilhauer, ergoCentric, ObusForme**
  products where natural. Do NOT claim Canadian-made on imports.
- **No puffery.** Banned words: elevate, transform, discover, dream, unleash,
  boldly, reimagine, revolutionize, game-changing, world-class, premium experience.
- **No emojis. No ALL-CAPS. No clickbait.**
- **Brand name rule — universal.** Never write "BBI" or bare "Brant" in any
  output a customer could read. Always write the full name "Brant Business
  Interiors" or omit the brand reference entirely. No abbreviations, ever.
- **Indigenous products: functional, not cultural.** If a product is
  described as Indigenous-designed or for Indigenous spaces, write a factual,
  spec-driven description focused on use case, materials, and durability. Do
  not write "respectful centrepiece", "cultural significance", "cultural
  meaning", or any flowery cultural framing. Describe the product; let the
  buyer determine its cultural value.

## Required HTML structure

**Hard rules**

- 150–400 words total across the whole HTML body.
- Opening: `<p><strong>Hook sentence.</strong></p>` — required, no exceptions.
- Body paragraph(s): use case, materials, key differentiators. Lead paragraph
  must end with a complete sentence terminated by a period. Never end any
  paragraph with a comma, em-dash, conjunction, or ellipsis.
- `<h3>Key features</h3>` followed by `<ul>` with 4–8 bullets. Each bullet is
  a single self-contained spec line ending with a period.
- `<h3>Who it's for</h3>` followed by a `<p>` naming the buyer archetype(s)
  where a clear archetype exists (task chairs, executive chairs, bariatric
  seating, training tables, reception desks, any SKU with an obvious buyer
  type). Skip this section only when the use case is already obvious from the
  opening hook.
- **Closing paragraph — required on every product:**
  The final `<p>` must include `<strong>Call 1-800-835-9565</strong>` plus a
  soft ask matched to the product type, and at least one trust anchor from:
  Free Design Layouts, 5 Ontario locations, delivery across Ontario,
  installation available, Canadian-owned, OECM Supplier Partner.
  Soft ask examples by product type:
    Default: "for current lead times and free design layouts."
    High-ticket / executive: "for free design layouts and contract pricing."
    Seating / chairs: "to confirm ergonomic options and finishes for your space."
    Institutional-leaning SKUs: "for OECM procurement pricing and lead times."
  Example closing: `<p>Brant Business Interiors delivers and installs across
  Ontario from 5 locations. <strong>Call 1-800-835-9565</strong> for current
  lead times and free design layouts.</p>`
  Example (institutional): `<p>Available through Brant Business Interiors — a
  division of Office Central Inc., a verified OECM Supplier Partner. Delivery
  and installation across Ontario. <strong>Call 1-800-835-9565</strong> for
  OECM procurement pricing and lead times.</p>`
- Never invent specs, materials, dimensions, or certifications not in the
  source. If the source title is the only signal, lean on use case and
  brand-typical attributes only — do not fabricate measurements.
- Preserve all alphanumeric model codes from the source verbatim
  (MVL2782, OTG10703B, GC3608, 1240-3, etc.) when they appear in the source.
- HTML only. No markdown headings (# ##). Use `<h3>` for section headers,
  `<p>` for paragraphs, `<ul><li>` for lists, `<strong>` for the opening
  hook and the phone number. No `<h1>` or `<h2>` — Shopify renders the
  product name as `<h1>` outside this body.

## Output

Return a Description JSON object. The notes field is a short reviewer flag
("OECM-leaning", "Canadian-made surfaced", "minimal source — generic copy").
Empty is fine.
"""


class Description(BaseModel):
    body_html: str = Field(description='Full HTML body. 150–400 words. Required structure.')
    notes: str = Field(default='', description='Short reviewer flag.')


def gql(query, variables=None):
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    for attempt in range(5):
        req = urllib.request.Request(GRAPHQL_URL, data=payload, headers=SHOPIFY_HEADERS, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 + attempt * 2); continue
            raise
        if data.get('errors'):
            err = json.dumps(data['errors'])[:200]
            if 'THROTTLED' in err.upper():
                time.sleep(2 + attempt * 2); continue
            raise RuntimeError(f'GraphQL errors: {err}')
        return data['data']
    raise RuntimeError('GraphQL gave up')


def fetch_descs(handles):
    out = {}
    pending = list(handles); BATCH = 30
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        aliases = '\n'.join(
            f'  p{i}: productByHandle(handle: "{h}") {{ handle title descriptionHtml }}'
            for i, h in enumerate(chunk)
        )
        data = gql('{\n' + aliases + '\n}')
        for i, h in enumerate(chunk):
            node = data.get(f'p{i}')
            out[h] = {
                'title': (node.get('title') if node else '') or '',
                'desc': (node.get('descriptionHtml') if node else '') or '',
            }
        time.sleep(0.6)
    return out


def estimate_cost(usage):
    in_t = usage.input_tokens; out_t = usage.output_tokens
    cw = getattr(usage, 'cache_creation_input_tokens', 0) or 0
    cr = getattr(usage, 'cache_read_input_tokens', 0) or 0
    return (in_t * 3 / 1_000_000 + out_t * 15 / 1_000_000
            + cw * 3 * 1.25 / 1_000_000 + cr * 3 * 0.10 / 1_000_000)


def strip_html(s):
    return re.sub(r'<[^>]+>', ' ', s or '').strip()


def word_count(s):
    return len(re.findall(r'\b\w+\b', strip_html(s)))


def draft_one(client, row, current):
    user = (
        f"Product to draft a long-form HTML description for:\n"
        f"  Handle: {row['handle']}\n"
        f"  Storefront title: {current['title'] or row['title']}\n"
        f"  Hero rank: #{row['hero_rank']} (revenue: ${row['sold_revenue']:,.0f})\n"
        f"  Type tag: {row.get('type_tag','')}\n"
        f"  Industry tag: {row.get('industry_tag','')}\n"
        f"  Current description (first 600 chars):\n"
        f"    {(current['desc'] or '(empty)')[:600]}\n\n"
        "Draft a fresh HTML description. 150–400 words. Use the required structure "
        "from the system prompt: lead <p>, <h3>Key features</h3> + <ul><li> bullets, "
        "optional <h3>Best for</h3> + <p>, optional closing <p>. Preserve every model "
        "code from the source. Never invent specs."
    )
    for attempt in range(6):
        try:
            resp = client.messages.parse(
                model=MODEL, max_tokens=2000,
                system=[{'type': 'text', 'text': SYSTEM_PROMPT, 'cache_control': {'type': 'ephemeral'}}],
                messages=[{'role': 'user', 'content': user}],
                output_format=Description,
            )
            break
        except anthropic.RateLimitError:
            wait = 30 + attempt * 15
            print(f'      · 429 rate limit — backoff {wait}s (attempt {attempt+1}/6)')
            time.sleep(wait)
    else:
        raise RuntimeError('rate-limit retries exhausted')
    return resp.parsed_output, estimate_cost(resp.usage)


def load_existing(path):
    if not os.path.exists(path): return set()
    return {r['handle'] for r in csv.DictReader(open(path)) if r.get('handle')}


def append_row(path, row):
    new = not os.path.exists(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new: w.writeheader()
        w.writerow({k: row.get(k, '') for k in CSV_FIELDS})


def load_hero_100():
    out = []
    with open(HERO_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out.append({
                'hero_rank': int(r['hero_rank']),
                'handle': r['handle'],
                'title': r['title'],
                'type_tag': r.get('type_tag', ''),
                'industry_tag': r.get('industry_tag', ''),
                'sold_revenue': float(r.get('sold_revenue', 0) or 0),
            })
    return out


def main():
    args = sys.argv[1:]
    refresh = '--refresh' in args
    limit = None; only = None
    for a in args:
        if a.startswith('--limit='): limit = int(a.split('=', 1)[1])
        if a.startswith('--handle='): only = a.split('=', 1)[1]

    rows = load_hero_100()
    if only: rows = [r for r in rows if r['handle'] == only]
    if limit: rows = rows[:limit]

    print(f'Hero rows to process: {len(rows)}')
    print(f'Output: {OUT_CSV}')

    existing = set() if refresh else load_existing(OUT_CSV)
    if existing: print(f'  Resume: skipping {len(existing)} drafted')
    todo = [r for r in rows if r['handle'] not in existing]
    print(f'  To draft now: {len(todo)}')
    if not todo: print('Nothing to do.'); return 0

    print('\nFetching current Shopify descriptions...')
    current = fetch_descs([r['handle'] for r in todo])

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY, max_retries=8)
    total = 0.0; drafted = 0; failed = 0

    for r in todo:
        if total >= COST_HARD_CAP:
            print(f'\n⛔  Cost cap reached.'); break
        cur = current.get(r['handle'], {'title': '', 'desc': ''})
        print(f"[{r['hero_rank']:>3}] {r['handle']}")
        try:
            draft, cost = draft_one(client, r, cur)
        except Exception as e:
            print(f"      → ERROR: {e}"); failed += 1; continue
        total += cost
        body = (draft.body_html or '').strip()
        wc = word_count(body)
        flags = []
        if wc < 100: flags.append(f'SHORT_{wc}w')
        if wc > 500: flags.append(f'LONG_{wc}w')
        # Sanity: must contain <ul> or it broke structure
        if '<ul' not in body.lower(): flags.append('NO_BULLETS')
        # Mid-thought check on each <p> ending
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body, flags=re.DOTALL | re.IGNORECASE)
        bad_endings = [p.strip() for p in paragraphs if p.strip() and not re.search(r'[.!?][\"\')\s]*$', p.strip())]
        if bad_endings: flags.append(f'BAD_ENDING_{len(bad_endings)}')
        notes = (draft.notes or '').strip()
        if flags: notes = (notes + '; ' if notes else '') + ' '.join(flags)
        body = re.sub(r'\bBBI\b', 'Brant Business Interiors', body)
        body = re.sub(r'\borganised\b', 'organized', body)
        body = re.sub(r'\borganisation', 'organization', body)
        append_row(OUT_CSV, {
            'handle': r['handle'],
            'current_desc_first_200c': strip_html(cur['desc'])[:200],
            'draft_body_html': body,
            'draft_word_count': wc,
            'notes': notes,
        })
        drafted += 1
        print(f"      → {wc} words  ${cost:.4f}  (total ${total:.2f})")

    print('\n' + '='*60)
    print(f'Drafted: {drafted}    Failed: {failed}    Cost: ${total:.2f}')
    print(f'CSV: {OUT_CSV}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
