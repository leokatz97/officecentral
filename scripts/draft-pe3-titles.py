"""
PE-3 — Draft normalized product titles for the Hero 100.

For each Hero 100 product, ask Claude to rewrite the storefront title in the
canonical format `[Brand] [Model Code] [Product Name] — [Key Spec]`,
sentence case, ≤70 chars, with all model codes preserved verbatim.

Output: data/reports/pe3-hero100-titles.csv
Resumable: re-runs skip handles already drafted.

Usage:
  python3 scripts/draft-pe3-titles.py                  # full Hero 100
  python3 scripts/draft-pe3-titles.py --limit=5        # canary
  python3 scripts/draft-pe3-titles.py --handle=<h>     # one product
  python3 scripts/draft-pe3-titles.py --refresh        # redo all

Cost: ~$0.005 / row × 100 ≈ $0.50.
"""
from __future__ import annotations
import csv, json, os, re, sys, time
import urllib.error, urllib.request

import anthropic
from pydantic import BaseModel, Field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO_CSV = os.path.join(ROOT, 'data', 'hero-100.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'pe3-hero100-titles.csv')
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
COST_HARD_CAP = 5.00

CSV_FIELDS = ['handle', 'current_title', 'draft_title', 'title_chars',
              'preserved_codes', 'notes']

SYSTEM_PROMPT = """You are a product copywriter for Brant Business Interiors (BBI),
a Canadian B2B office furniture dealer (Richmond Hill, ON; OECM Supplier Partner).

You normalize storefront product titles for the Hero 100 catalog.

## Voice (locked)

- Confident, not lifestyle. No "elevate", "transform", "discover", puffery, emojis, ALL-CAPS.
- Canadian-English (centre, colour, metre).
- Procurement-first: model codes are searchable.

## Output format

`[Brand] [Model Code] [Product Name] — [Key Spec]`

Where:
- **Brand** is included if known and present in source (Global, OTG, ObusForme,
  Newland, Lite-Lift, Foundations, Keilhauer, Teknion, ergoCentric, etc.).
  Skip the brand if not clearly present in the source.
- **Model Code** is **preserved verbatim** if present in the source title
  (MVL2782, OTG10703B, GC3608, 1240-3, 9300, 26-451, etc.). Do not invent codes.
- **Product Name** is the product type/family in sentence case
  ("High-back synchro-tilter chair", "L-shape desk", "Bariatric chair").
- **Key Spec** is optional — only add when there is a real differentiating
  spec from the source (size, sizes count, colour count, capacity).
  The em-dash `—` separator is optional.

## Hard rules

- **≤70 chars total** including spaces.
- Sentence case for words other than brand names and model codes.
  Brand names retain their canonical capitalization (Global, OTG, ObusForme).
  Model codes retain their exact capitalization (MVL2782, OTG10703B).
- **Preserve every alphanumeric model code from the source title verbatim.**
- Never use "BBI", "Brant", or any abbreviation of "Brant Business Interiors".
  No brand suffix on product titles (this is the storefront product name,
  not an SEO meta title).
- No double-spaces, no leading/trailing whitespace.
- Never invent attributes, specs, or codes that aren't in the source.

## Output

Return a `Title` JSON object. The `notes` field is for a short reviewer flag
("code preserved", "no brand surfaced", "size dropped — over cap"). Empty is fine.
"""


class Title(BaseModel):
    title: str = Field(description='Normalized product title, target ≤70 chars.')
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
    raise RuntimeError('GraphQL gave up after retries')


def fetch_titles(handles):
    out = {}
    pending = list(handles); BATCH = 50
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        aliases = '\n'.join(
            f'  p{i}: productByHandle(handle: "{h}") {{ handle title }}'
            for i, h in enumerate(chunk)
        )
        data = gql('{\n' + aliases + '\n}')
        for i, h in enumerate(chunk):
            node = data.get(f'p{i}')
            out[h] = (node.get('title') if node else '') or ''
        time.sleep(0.6)
    return out


def estimate_cost(usage):
    in_t = usage.input_tokens; out_t = usage.output_tokens
    cw = getattr(usage, 'cache_creation_input_tokens', 0) or 0
    cr = getattr(usage, 'cache_read_input_tokens', 0) or 0
    return (in_t * 3 / 1_000_000 + out_t * 15 / 1_000_000
            + cw * 3 * 1.25 / 1_000_000 + cr * 3 * 0.10 / 1_000_000)


CODE_RE = re.compile(r'\b[A-Z]{2,}[A-Z0-9-]*\d[A-Z0-9-]*\b|\b\d{4,}-\d+\b|\b\d{2,}-\d{3,}\b')


def extract_codes(s):
    return set(CODE_RE.findall(s or ''))


def draft_one(client, row, current_title):
    user = (
        f"Source title: {current_title or row['title']}\n"
        f"Hero rank: #{row['hero_rank']}\n"
        f"Type tag: {row.get('type_tag','')}\n\n"
        "Rewrite this title in the canonical format. ≤70 chars. Preserve all "
        "model codes verbatim. No 'BBI'/'Brant'."
    )
    for attempt in range(6):
        try:
            resp = client.messages.parse(
                model=MODEL, max_tokens=300,
                system=[{'type': 'text', 'text': SYSTEM_PROMPT, 'cache_control': {'type': 'ephemeral'}}],
                messages=[{'role': 'user', 'content': user}],
                output_format=Title,
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
    if existing: print(f'  Resume: skipping {len(existing)} drafted handles')
    todo = [r for r in rows if r['handle'] not in existing]
    print(f'  To draft now: {len(todo)}')
    if not todo:
        print('Nothing to do.'); return 0

    print('\nFetching current Shopify titles...')
    current = fetch_titles([r['handle'] for r in todo])

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY, max_retries=8)
    total = 0.0; drafted = 0; failed = 0

    for r in todo:
        if total >= COST_HARD_CAP:
            print(f'\n⛔  Cost cap reached.'); break
        cur = current.get(r['handle'], '') or r['title']
        print(f"[{r['hero_rank']:>3}] {r['handle']}")
        try:
            draft, cost = draft_one(client, r, cur)
        except Exception as e:
            print(f"      → ERROR: {e}"); failed += 1; continue
        total += cost
        # Post-process
        t = (draft.title or '').strip()
        # Clip if over
        clipped = False
        if len(t) > 70:
            cut = t[:69].rsplit(' ', 1)[0].rstrip(',;:.—-')
            t = cut + '…'; clipped = True
        # Strip any abbreviated brand suffix (defense-in-depth)
        t = re.sub(r'\s*\|\s*BBI\s*$', '', t)
        t = re.sub(r'\s*\|\s*Brant(\s+Business)?\s*$', '', t)
        # Code preservation check
        src_codes = extract_codes(cur)
        out_codes = extract_codes(t)
        missing = src_codes - out_codes
        flags = []
        if clipped: flags.append('CLIPPED')
        if missing: flags.append(f'CODE_MISSING={",".join(sorted(missing))}')
        notes = (draft.notes or '').strip()
        if flags: notes = (notes + '; ' if notes else '') + ' '.join(flags)
        append_row(OUT_CSV, {
            'handle': r['handle'],
            'current_title': cur,
            'draft_title': t,
            'title_chars': len(t),
            'preserved_codes': ','.join(sorted(src_codes)),
            'notes': notes,
        })
        drafted += 1
        print(f"      → {len(t)}c  ${cost:.4f}  (total ${total:.2f})")

    print('\n' + '='*60)
    print(f'Drafted: {drafted}    Failed: {failed}    Cost: ${total:.2f}')
    print(f'CSV: {OUT_CSV}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
