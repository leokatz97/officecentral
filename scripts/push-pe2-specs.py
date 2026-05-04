#!/usr/bin/env python3
"""
PE-2 push: write product spec metafields under namespace `specs.*`
from data/specs/*.json into Shopify via metafieldsSet.

Usage:
  python3 scripts/push-pe2-specs.py             # DRY RUN
  python3 scripts/push-pe2-specs.py --live      # apply
  python3 scripts/push-pe2-specs.py --limit=N   # process first N products

Safety:
  - Pulls current specs.* metafields once at startup, writes to data/backups/.
  - Skips fields where current value already matches the new value.
  - Logs every mutation outcome to data/logs/pe2-push-<ts>.json.
  - Dry-run prints first 3 product diffs + summary; no API writes.

Spec key map (12 fields written; 3 skipped as internal: confidence, source_urls, notes):
  manufacturer, product_line, model_codes, dimensions, weight, weight_capacity,
  materials, finishes_available, key_features, certifications, warranty,
  country_of_manufacture
"""
import csv, glob, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT / 'data/specs'
BACKUP_DIR = ROOT / 'data/backups'
LOG_DIR = ROOT / 'data/logs'
ENV_PATH = ROOT / '.env'
for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

# Map JSON key -> (metafield key, type, is_list)
FIELD_MAP = [
    ('manufacturer',           'single_line_text_field',      False),
    ('product_line',           'single_line_text_field',      False),
    ('model_codes',            'list.single_line_text_field', True),
    ('dimensions',             'single_line_text_field',      False),
    ('weight',                 'single_line_text_field',      False),
    ('weight_capacity',        'single_line_text_field',      False),
    ('materials',              'multi_line_text_field',       False),
    ('finishes_available',     'list.single_line_text_field', True),
    ('key_features',           'list.single_line_text_field', True),
    ('certifications',         'list.single_line_text_field', True),
    ('warranty',               'single_line_text_field',      False),
    ('country_of_manufacture', 'single_line_text_field',      False),
]
INTERNAL_KEYS = {'confidence', 'source_urls', 'notes'}


def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
            if 'errors' in data: raise RuntimeError(f'GraphQL errors: {data["errors"]}')
            return data['data']
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2: time.sleep(2 ** attempt); continue
            raise


def fetch_products(handles):
    """Resolve handles -> product IDs + current specs.* metafields."""
    out = {}
    pending = list(handles); BATCH = 25
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        aliases = '\n'.join(
            f'  p{i}: productByHandle(handle: "{h}") {{ id handle '
            f'metafields(namespace: "specs", first: 20) {{ edges {{ node {{ key value type }} }} }} '
            f'}}'
            for i, h in enumerate(chunk))
        d = gql('{\n' + aliases + '\n}')
        for i, h in enumerate(chunk):
            n = d.get(f'p{i}')
            if not n:
                out[h] = None; continue
            current = {e['node']['key']: e['node']['value']
                       for e in n['metafields']['edges']}
            out[h] = {'id': n['id'], 'current': current}
        time.sleep(0.4)
    return out


def normalize_value(raw, is_list):
    """Convert spec JSON value -> Shopify metafield string."""
    if raw is None: return None
    if is_list:
        # Expect a list; if it's a string for some reason, wrap.
        if isinstance(raw, list):
            cleaned = [str(x).strip() for x in raw if x is not None and str(x).strip()]
            return json.dumps(cleaned) if cleaned else None
        s = str(raw).strip()
        return json.dumps([s]) if s else None
    s = '' if raw is None else str(raw).strip()
    return s if s else None


def set_metafields(product_id, fields):
    """Write up to 25 metafields for one product via metafieldsSet."""
    m = '''mutation($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { id namespace key }
        userErrors { field message code }
      }
    }'''
    inputs = [{
        'ownerId': product_id,
        'namespace': 'specs',
        'key': k,
        'type': t,
        'value': v,
    } for k, t, v in fields]
    d = gql(m, {'metafields': inputs})
    errs = d['metafieldsSet']['userErrors']
    if errs: raise RuntimeError(f'userErrors: {errs}')
    return d['metafieldsSet']['metafields']


def main():
    args = sys.argv[1:]
    live = '--live' in args
    limit = None
    for a in args:
        if a.startswith('--limit='): limit = int(a.split('=', 1)[1])

    spec_files = sorted(SPECS_DIR.glob('*.json'))
    if limit: spec_files = spec_files[:limit]
    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    print(f'Spec files: {len(spec_files)}')

    # Load all spec JSONs
    specs_by_handle = {}
    for p in spec_files:
        d = json.load(open(p))
        specs_by_handle[d['handle']] = d

    print('Fetching current Shopify specs metafields...')
    products = fetch_products(list(specs_by_handle.keys()))

    # Backup current state
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = BACKUP_DIR / f'pe2-specs-pre-push-{ts}.json'
    backup_path.write_text(json.dumps(
        {h: (p['current'] if p else None) for h, p in products.items()}, indent=2))
    print(f'Backup: {backup_path}')

    # Build plan
    plan = []
    for handle, spec_doc in specs_by_handle.items():
        prod = products.get(handle)
        if not prod:
            plan.append({'handle': handle, 'status': 'NOT_FOUND'}); continue
        current = prod['current']
        new_fields = []
        unchanged = []
        skipped_empty = []
        for jkey, mtype, is_list in FIELD_MAP:
            raw = spec_doc.get('specs', {}).get(jkey)
            new_val = normalize_value(raw, is_list)
            if new_val is None:
                skipped_empty.append(jkey); continue
            cur_val = current.get(jkey)
            if cur_val == new_val:
                unchanged.append(jkey); continue
            new_fields.append((jkey, mtype, new_val))
        plan.append({
            'handle': handle, 'product_id': prod['id'],
            'status': 'WILL_UPDATE' if new_fields else 'UNCHANGED',
            'new_fields': new_fields, 'unchanged': unchanged,
            'skipped_empty': skipped_empty,
        })

    will = [p for p in plan if p['status'] == 'WILL_UPDATE']
    nochange = [p for p in plan if p['status'] == 'UNCHANGED']
    missing = [p for p in plan if p['status'] == 'NOT_FOUND']
    total_field_writes = sum(len(p['new_fields']) for p in will)
    print(f'\n  Products to update: {len(will)}')
    print(f'  Products unchanged: {len(nochange)}')
    print(f'  Products not found: {len(missing)}')
    print(f'  Total metafield writes: {total_field_writes}')

    if missing:
        print('  Missing handles:')
        for p in missing: print(f'    {p["handle"]}')

    if not live:
        print(f'\n=== DRY RUN — sample of first 3 products ===')
        for p in will[:3]:
            print(f'\n  {p["handle"]}  ({len(p["new_fields"])} fields to set)')
            for k, t, v in p['new_fields']:
                vs = v if len(v) < 80 else v[:77] + '…'
                print(f'    + specs.{k:25s} [{t}] {vs}')
            if p['unchanged']:
                print(f'    (unchanged: {", ".join(p["unchanged"])})')
            if p['skipped_empty']:
                print(f'    (skipped empty: {", ".join(p["skipped_empty"])})')
        print(f'\n(Pass --live to apply {total_field_writes} metafield writes across {len(will)} products)')
        return 0

    log = []; ok_p = fail_p = ok_f = 0
    print(f'\n=== APPLYING LIVE — {total_field_writes} metafield writes / {len(will)} products ===')
    for i, p in enumerate(will, 1):
        try:
            res = set_metafields(p['product_id'], p['new_fields'])
            ok_p += 1; ok_f += len(p['new_fields'])
            log.append({'handle': p['handle'], 'status': 'OK',
                        'fields_set': [f[0] for f in p['new_fields']]})
            print(f'[{i:3d}/{len(will)}] OK  {p["handle"]}  ({len(p["new_fields"])} fields)')
        except Exception as e:
            fail_p += 1
            log.append({'handle': p['handle'], 'status': 'FAIL',
                        'error': str(e)[:300],
                        'attempted_fields': [f[0] for f in p['new_fields']]})
            print(f'[{i:3d}/{len(will)}] FAIL {p["handle"]} — {e}')

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f'pe2-push-{ts}.json'
    log_path.write_text(json.dumps({
        'timestamp': ts, 'live': True,
        'products_ok': ok_p, 'products_fail': fail_p,
        'fields_written': ok_f,
        'results': log,
    }, indent=2))
    print(f'\n{"="*60}')
    print(f'Done: {ok_p} products OK ({ok_f} fields) · {fail_p} products FAIL')
    print(f'Log: {log_path}')
    print(f'Backup: {backup_path}')
    return 0 if fail_p == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
