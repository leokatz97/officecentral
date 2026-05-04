#!/usr/bin/env python3
"""
Normalize the Shopify `vendor` field on every BBI product.

Two-pass strategy:
  1. Manufacturer detection — parse title for a known brand (high) or an
     unambiguous product-line/SKU pattern that maps to a single brand (medium).
  2. Fallback — when no brand is detectable, set vendor to the full
     "Brant Business Interiors" name (per voice rules: NEVER "BBI" customer-facing).

Pulls live products fresh from Shopify (id, handle, title, vendor) via GraphQL,
applies the rules, writes a diff CSV at data/reports/vendor-normalization-<date>.csv,
and on --live calls productUpdate for every row whose vendor would change.

Usage:
  python3 scripts/normalize-vendor-field.py             # DRY RUN — writes CSV only
  python3 scripts/normalize-vendor-field.py --live      # apply mutations after CSV
  python3 scripts/normalize-vendor-field.py --limit=N   # limit live mutations
"""
import csv, json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / 'data' / 'reports'
BACKUP_DIR  = ROOT / 'data' / 'backups'
LOG_DIR     = ROOT / 'data' / 'logs'
HERO_CSV    = ROOT / 'data' / 'hero-100.csv'
ENV_PATH    = ROOT / '.env'

for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

SHOP  = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL   = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

BBI_VENDOR = 'Brant Business Interiors'

# ---------------------------------------------------------------------------
# Brand match table
#
# Each entry: (canonical_vendor, [regex patterns], confidence)
#   - HIGH   = brand name itself appears as a standalone word in the title
#   - MEDIUM = a product line / sub-brand name that unambiguously maps to one
#              manufacturer (e.g., "Newland" is Offices to Go; "Concorde" / "Zira"
#              / "Accord" are Global product families).
#
# Patterns are matched case-insensitive against the title. \b boundaries are
# used to avoid false positives ("Global" matches the word, not substrings).
# ---------------------------------------------------------------------------
HIGH = 'high'
MEDIUM = 'medium'

BRAND_RULES = [
    # --- The Big Three ---
    ('Global Furniture Group',  [r'\bGlobal\b'],                         HIGH),
    ('Teknion',                 [r'\bTeknion\b'],                        HIGH),
    ('Groupe Lacasse',          [r'\bLacasse\b', r'\bGroupe Lacasse\b'], HIGH),

    # --- Design & specialty seating ---
    ('Keilhauer',               [r'\bKeilhauer\b'],                      HIGH),
    ('Nienkämper',              [r'\bNienk[aä]mper\b'],                  HIGH),
    ('Allseating',              [r'\bAllseating\b'],                     HIGH),
    ('ergoCentric',             [r'\bergo[Cc]entric\b'],                 HIGH),
    ('Borgo Seating',           [r'\bBorgo\b'],                          HIGH),

    # --- Workstations / desks / systems ---
    ('Tayco',                   [r'\bTayco\b'],                          HIGH),
    ('Three H',                 [r'\bThree\s*H\b'],                      HIGH),
    ('Krug',                    [r'\bKrug\b'],                           HIGH),
    ('Heartwood Manufacturing', [r'\bHeartwood\b'],                      HIGH),
    ('Logiflex',                [r'\bLogiflex\b'],                       HIGH),
    ('OFGO Studio',             [r'\bOFGO\b'],                           HIGH),

    # --- Specialized & niche ---
    ('Swiftspace',              [r'\bSwiftspace\b'],                     HIGH),
    ('Spec Furniture',          [r'\bSpec Furniture\b'],                 HIGH),
    ('ezoBord',                 [r'\bezo[Bb]ord\b'],                     HIGH),
    ('Artopex',                 [r'\bArtopex\b'],                        HIGH),

    # --- Other manufacturers BBI resells (non-Canadian or imported lines) ---
    ('ObusForme',               [r'\bObusForme\b'],                      HIGH),
    ('Humanscale',              [r'\bHumanscale\b'],                     HIGH),
    ('Steelcase',               [r'\bSteelcase\b'],                      HIGH),
    ('Safco',                   [r'\bAlphaBetter\b', r'\bSafco\b'],      HIGH),
    ('Offices to Go',           [r'\bOffices to Go\b'],                  HIGH),

    # --- Medium-confidence product-line mappings ---
    # "Newland" is Offices to Go's flagship laminate suite line.
    ('Offices to Go',           [r'\bNewland\b'],                        MEDIUM),
    # Global product families (chairs / desks): Concorde, Zira, Accord,
    # Ibex, Vion, Ashton, Overtime, Format, Six 31, Ergo Boss.
    ('Global Furniture Group',  [r'\bConcorde\b',  r'\bZira\b',
                                 r'\bAccord\b',
                                 r'\bIbex\b',      r'\bVion\b',
                                 r'\bAshton\b',    r'\bOvertime\b',
                                 r'\bFormat\b',    r'\bSix\s*31\b',
                                 r'\bErgo\s*Boss\b'],                    MEDIUM),
]

# Pre-compile for speed
COMPILED_RULES = [
    (vendor, [re.compile(p, re.IGNORECASE) for p in patterns], conf)
    for vendor, patterns, conf in BRAND_RULES
]


def detect_vendor(title: str):
    """Return (proposed_vendor, confidence, matched_pattern) for a title."""
    if not title:
        return BBI_VENDOR, 'fallback', ''
    # Apply HIGH-confidence rules first; fall through to MEDIUM only if none match.
    for vendor, regexes, conf in COMPILED_RULES:
        if conf != HIGH:
            continue
        for rx in regexes:
            if rx.search(title):
                return vendor, HIGH, rx.pattern
    for vendor, regexes, conf in COMPILED_RULES:
        if conf != MEDIUM:
            continue
        for rx in regexes:
            if rx.search(title):
                return vendor, MEDIUM, rx.pattern
    return BBI_VENDOR, 'fallback', ''


# ---------------------------------------------------------------------------
# Shopify GraphQL helpers
# ---------------------------------------------------------------------------
def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
            if 'errors' in data:
                raise RuntimeError(f'GraphQL errors: {data["errors"]}')
            return data['data']
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** attempt); continue
            raise


def fetch_all_products():
    """Page through every product in the store, returning id/handle/title/vendor/status."""
    out = []
    cursor = None
    page = 0
    while True:
        page += 1
        q = '''
        query($cursor: String) {
          products(first: 250, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes { id handle title vendor status }
          }
        }'''
        d = gql(q, {'cursor': cursor})
        page_data = d['products']
        out.extend(page_data['nodes'])
        print(f'  page {page}: +{len(page_data["nodes"])} (total {len(out)})')
        if not page_data['pageInfo']['hasNextPage']:
            break
        cursor = page_data['pageInfo']['endCursor']
        time.sleep(0.5)
    return out


def update_vendor(pid, vendor):
    m = '''mutation($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id vendor }
        userErrors { field message }
      }
    }'''
    d = gql(m, {'input': {'id': pid, 'vendor': vendor}})
    errs = d['productUpdate']['userErrors']
    if errs:
        raise RuntimeError(f'userErrors: {errs}')
    return d['productUpdate']['product']


# ---------------------------------------------------------------------------
def load_hero_handles():
    if not HERO_CSV.exists():
        return set()
    with open(HERO_CSV) as f:
        return {row['handle'] for row in csv.DictReader(f)}


def main():
    args = sys.argv[1:]
    live = '--live' in args
    limit = None
    for a in args:
        if a.startswith('--limit='):
            limit = int(a.split('=', 1)[1])

    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    print(f'Store: {SHOP}.myshopify.com')

    print('\nFetching all products from Shopify...')
    products = fetch_all_products()
    print(f'Fetched {len(products)} products.')

    hero_handles = load_hero_handles()
    print(f'Hero 100 handles loaded: {len(hero_handles)}')

    rows = []
    for p in products:
        title  = p.get('title') or ''
        vendor = (p.get('vendor') or '').strip()
        proposed, conf, matched = detect_vendor(title)
        rows.append({
            'handle':            p['handle'],
            'product_id':        p['id'],
            'title':             title,
            'status':            p.get('status', ''),
            'current_vendor':    vendor,
            'proposed_vendor':   proposed,
            'confidence':        conf,
            'matched_pattern':   matched,
            'will_change':       'yes' if vendor != proposed else 'no',
            'is_hero_100':       'yes' if p['handle'] in hero_handles else 'no',
        })

    REPORTS_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    csv_path = REPORTS_DIR / f'vendor-normalization-{today}.csv'
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'handle', 'product_id', 'title', 'status',
            'current_vendor', 'proposed_vendor',
            'confidence', 'matched_pattern',
            'will_change', 'is_hero_100',
        ])
        w.writeheader()
        # Sort: hero first, then will_change=yes, then by confidence, then handle
        conf_order = {HIGH: 0, MEDIUM: 1, 'fallback': 2}
        rows_sorted = sorted(rows, key=lambda r: (
            r['is_hero_100'] != 'yes',
            r['will_change'] != 'yes',
            conf_order.get(r['confidence'], 9),
            r['handle'],
        ))
        for r in rows_sorted:
            w.writerow(r)

    # Print summary
    will_change = [r for r in rows if r['will_change'] == 'yes']
    by_proposed = {}
    by_conf = {HIGH: 0, MEDIUM: 0, 'fallback': 0}
    for r in rows:
        by_proposed[r['proposed_vendor']] = by_proposed.get(r['proposed_vendor'], 0) + 1
        by_conf[r['confidence']] = by_conf.get(r['confidence'], 0) + 1
    by_current = {}
    for r in rows:
        by_current[r['current_vendor']] = by_current.get(r['current_vendor'], 0) + 1

    print('\n' + '=' * 70)
    print('VENDOR NORMALIZATION — DRY RUN SUMMARY')
    print('=' * 70)
    print(f'Total products: {len(rows)}')
    print(f'Will change:    {len(will_change)}')
    print(f'Unchanged:      {len(rows) - len(will_change)}')
    print()
    print('Current vendor distribution:')
    for v, n in sorted(by_current.items(), key=lambda x: -x[1]):
        print(f'  {n:5d}  {v!r}')
    print()
    print('Proposed vendor distribution:')
    for v, n in sorted(by_proposed.items(), key=lambda x: -x[1]):
        print(f'  {n:5d}  {v!r}')
    print()
    print('Confidence breakdown:')
    for c in (HIGH, MEDIUM, 'fallback'):
        print(f'  {c:9s}: {by_conf.get(c, 0)}')

    # Hero 100 spot-check rows
    hero_rows = [r for r in rows if r['is_hero_100'] == 'yes']
    hero_changing = [r for r in hero_rows if r['will_change'] == 'yes']
    print()
    print(f'Hero 100 in catalog: {len(hero_rows)}  (changing: {len(hero_changing)})')
    print('--- Hero 100 proposed changes (spot-check these manually) ---')
    for r in hero_changing[:50]:
        print(f'  [{r["confidence"]:8s}] {r["handle"]}')
        print(f'      title:    {r["title"][:90]}')
        print(f'      vendor:   {r["current_vendor"]!r:50s} -> {r["proposed_vendor"]!r}')
    if len(hero_changing) > 50:
        print(f'  ... +{len(hero_changing) - 50} more (see CSV)')

    print()
    print(f'Diff CSV written: {csv_path}')

    if not live:
        print('\nDRY RUN complete. Review the CSV, then re-run with --live to apply.')
        return 0

    # --- LIVE PATH ---
    will = will_change
    if limit is not None:
        will = will[:limit]
        print(f'\n--limit={limit} → applying {len(will)} of {len(will_change)} pending mutations')

    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = BACKUP_DIR / f'vendor-pre-push-{ts}.csv'
    with open(backup_path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['handle', 'product_id', 'old_vendor'])
        for r in will:
            w.writerow([r['handle'], r['product_id'], r['current_vendor']])
    print(f'Backup: {backup_path}')

    log = []; ok = fail = 0
    print(f'\n=== APPLYING LIVE — {len(will)} mutations ===')
    for i, r in enumerate(will, 1):
        try:
            update_vendor(r['product_id'], r['proposed_vendor'])
            ok += 1
            log.append({'handle': r['handle'], 'status': 'OK',
                        'old': r['current_vendor'], 'new': r['proposed_vendor']})
            if i % 25 == 0 or i == len(will):
                print(f'  [{i:4d}/{len(will)}] OK so far: {ok}, FAIL: {fail}')
        except Exception as e:
            fail += 1
            log.append({'handle': r['handle'], 'status': 'FAIL',
                        'error': str(e)[:200]})
            print(f'  [{i:4d}/{len(will)}] FAIL {r["handle"]} — {e}')

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f'vendor-normalize-{ts}.json'
    log_path.write_text(json.dumps({
        'timestamp': ts, 'live': True, 'ok': ok, 'fail': fail, 'results': log,
    }, indent=2))
    print(f'\n{"=" * 70}\nDone: {ok} OK, {fail} FAIL\nLog:    {log_path}\nBackup: {backup_path}')
    return 0 if fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
