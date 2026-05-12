#!/usr/bin/env python3
"""
PE-PASS-3 — push enrichment output to Shopify.

Reads: data/reports/pe-pass2-output.json
Writes:
  • product.body_html (approved description from enrichment sessions)
  • specs.* metafields (all 12 fields from enrichment output)
  • product.vendor (if vendor_override is set in the output)

Usage:
  python3 scripts/push-pe3-enrichment.py             # DRY RUN
  python3 scripts/push-pe3-enrichment.py --live      # apply to Shopify
  python3 scripts/push-pe3-enrichment.py --handle=X  # single product (dry or live)
  python3 scripts/push-pe3-enrichment.py --hero      # Hero 100 mode — reads data/specs.json

Safety:
  - Backs up current product data to data/backups/ before writing.
  - Skips products where output has status 'skip'.
  - Logs every mutation to data/logs/pe3-push-<ts>.json.
  - Dry-run prints first 3 diffs + summary; no API writes.

Sources:
  • Enrichment 157:  data/reports/pe-pass2-output.json  (from PE-PASS-2 sessions)
  • Hero 100:        data/specs.json  (from lookup-specs.py, --hero flag)
"""
import json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH  = ROOT / 'data/reports/pe-pass2-output.json'
HERO_PATH    = ROOT / 'data/specs.json'
BACKUP_DIR   = ROOT / 'data/backups'
LOG_DIR      = ROOT / 'data/logs'
ENV_PATH     = ROOT / '.env'

for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

SHOP  = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL   = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'
REST  = f'https://{SHOP}.myshopify.com/admin/api/2024-10'

# 12 spec fields: (json_key, metafield_type, is_list)
SPEC_FIELD_MAP = [
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
SKIP_SPEC_KEYS = {'confidence', 'source_urls', 'notes'}


# ── HTTP helpers ────────────────────────────────────────────────────────────

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req  = urllib.request.Request(GQL, data=body, headers={
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


def rest_put(path, payload):
    body = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f'{REST}{path}',
        data=body,
        headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
        method='PUT',
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** attempt); continue
            raise


# ── Shopify fetch ────────────────────────────────────────────────────────────

def fetch_products(handles):
    """Resolve handles → product IDs, current body_html, vendor, specs.* metafields."""
    out = {}
    pending = list(handles)
    BATCH = 25
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        aliases = '\n'.join(
            f'  p{i}: productByHandle(handle: "{h}") {{'
            f'    id handle vendor '
            f'    metafields(namespace: "specs", first: 20) {{'
            f'      edges {{ node {{ key value type }} }}'
            f'    }}'
            f'  }}'
            for i, h in enumerate(chunk)
        )
        q = f'{{ {aliases} }}'
        data = gql(q)
        for i, h in enumerate(chunk):
            node = data.get(f'p{i}')
            if not node:
                out[h] = None; continue
            current_specs = {}
            for edge in node['metafields']['edges']:
                n = edge['node']
                current_specs[n['key']] = n['value']
            out[h] = {
                'id': node['id'],
                'handle': node['handle'],
                'vendor': node['vendor'],
                'current_specs': current_specs,
            }
    return out


def fetch_product_body(numeric_id):
    """Fetch current body_html and tags via REST (GraphQL body is stripped HTML)."""
    url = f'{REST}/products/{numeric_id}.json?fields=id,body_html,vendor,tags'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())['product']


# ── Value normalisation (mirrors push-pe2-specs.py) ─────────────────────────

def normalize_value(raw, is_list):
    """Return None to skip, or a JSON-serialisable string/list."""
    if raw is None:
        return None
    if is_list:
        if isinstance(raw, list):
            items = [str(x).strip() for x in raw if str(x).strip()]
            return json.dumps(items) if items else None
        if isinstance(raw, str) and raw.strip():
            return json.dumps([raw.strip()])
        return None
    if isinstance(raw, str):
        return raw.strip() or None
    return str(raw).strip() or None


# ── Metafield writer ─────────────────────────────────────────────────────────

METAFIELDS_SET = """
mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { key namespace value }
    userErrors { field message }
  }
}
"""

def set_metafields(product_gid, fields):
    """fields: list of (key, type, value_string)"""
    batch = [
        {'ownerId': product_gid, 'namespace': 'specs',
         'key': k, 'type': t, 'value': v}
        for k, t, v in fields
    ]
    CHUNK = 25
    for i in range(0, len(batch), CHUNK):
        result = gql(METAFIELDS_SET, {'metafields': batch[i:i+CHUNK]})
        errs = result['metafieldsSet']['userErrors']
        if errs:
            raise RuntimeError(f'metafieldsSet errors: {errs}')


def update_product_body(numeric_id, body_html, vendor=None, tags=None):
    payload = {'product': {'id': numeric_id, 'body_html': body_html}}
    if vendor:
        payload['product']['vendor'] = vendor
    if tags is not None:
        payload['product']['tags'] = tags
    rest_put(f'/products/{numeric_id}.json', payload)


# ── Source loaders ───────────────────────────────────────────────────────────

def load_enrichment_products():
    """Load pe-pass2-output.json — enrichment session outputs.

    Reads both the nested 'products' dict (Batches 1+2) and top-level
    product entries (Batch 3+) which share the same record schema.
    """
    with open(OUTPUT_PATH) as f:
        data = json.load(f)
    # Merge nested 'products' key with top-level handle entries
    merged = {}
    merged.update(data.get('products', {}))
    for k, v in data.items():
        if k in ('created', 'last_updated', 'products'):
            continue
        if isinstance(v, dict) and 'action' in v:
            merged[k] = v
    ready = {}
    for handle, rec in merged.items():
        if rec.get('action') in ('skip', 'other'):
            continue
        ready[handle] = rec
    return ready


def load_hero_products():
    """Load data/specs.json — Hero 100 specs from lookup-specs.py."""
    with open(HERO_PATH) as f:
        data = json.load(f)
    ready = {}
    for handle, rec in data.items():
        ready[handle] = {
            'specs': rec.get('specs', {}),
            'description': None,   # Hero 100 don't get description rewrite here
            'vendor_override': None,
        }
    return ready


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    live         = '--live' in args
    hero_mode    = '--hero' in args
    single       = next((a.split('=',1)[1] for a in args if a.startswith('--handle=')), None)

    print(f'\n{"="*60}')
    print(f'PE-PASS-3 Enrichment Push  |  {"LIVE" if live else "DRY RUN"}')
    if hero_mode:
        print('Mode: Hero 100 (specs only — no description rewrite)')
    else:
        print('Mode: Enrichment 157 (description + specs + vendor)')
    print(f'{"="*60}\n')

    # Load source data
    if hero_mode:
        source = load_hero_products()
    else:
        source = load_enrichment_products()

    if not source:
        print('No products in output. Run enrichment sessions first.')
        return 1

    if single:
        if single not in source:
            print(f'Handle "{single}" not found in source data.')
            return 1
        source = {single: source[single]}

    print(f'Source products: {len(source)}')

    # Resolve handles → Shopify IDs
    print('Fetching Shopify product data...')
    shopify = fetch_products(list(source.keys()))

    found   = {h: v for h, v in shopify.items() if v}
    missing = [h for h, v in shopify.items() if not v]
    if missing:
        print(f'  Not found in Shopify ({len(missing)}): {", ".join(missing[:5])}{"..." if len(missing)>5 else ""}')

    # Backup current state
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = {}
    for h, prod in found.items():
        numeric_id = prod['id'].split('/')[-1]
        try:
            current = fetch_product_body(numeric_id)
            backup[h] = current
        except Exception as e:
            backup[h] = {'error': str(e)}

    mode_label = 'hero' if hero_mode else 'enrichment'
    backup_path = BACKUP_DIR / f'pe3-{mode_label}-pre-push-{ts}.json'
    backup_path.write_text(json.dumps(backup, indent=2))
    print(f'Backup: {backup_path}')

    # Build plan
    plan = []
    for handle, rec in source.items():
        prod = found.get(handle)
        if not prod:
            plan.append({'handle': handle, 'status': 'NOT_FOUND'}); continue

        numeric_id = prod['id'].split('/')[-1]
        current_specs = prod['current_specs']
        current_vendor = prod['vendor']

        # Specs diff
        spec_fields = []
        for jkey, mtype, is_list in SPEC_FIELD_MAP:
            raw = rec.get('specs', {}).get(jkey)
            new_val = normalize_value(raw, is_list)
            if new_val is None:
                continue
            if current_specs.get(jkey) == new_val:
                continue
            spec_fields.append((jkey, mtype, new_val))

        # Description diff — field may be 'draft_body_html' (enrichment sessions)
        # or 'description' (legacy)
        new_body = rec.get('draft_body_html') or rec.get('description')
        current_body = backup.get(handle, {}).get('body_html', '')
        body_changed = new_body and new_body.strip() != (current_body or '').strip()

        # Vendor diff
        vendor_override = rec.get('vendor_override')
        vendor_changed  = vendor_override and vendor_override != current_vendor

        # Brand tag diff — always apply when vendor_override is set
        new_tags_str = None
        tag_changed = False
        if vendor_override:
            slug = f'brand:{slugify(vendor_override)}'
            current_tags_raw = backup.get(handle, {}).get('tags', '') or ''
            current_tags = {t.strip() for t in current_tags_raw.split(',') if t.strip()}
            non_brand = {t for t in current_tags if not t.startswith('brand:')}
            new_tag_set = non_brand | {slug}
            tag_changed = new_tag_set != current_tags
            if tag_changed:
                new_tags_str = ', '.join(sorted(new_tag_set))

        if not spec_fields and not body_changed and not vendor_changed and not tag_changed:
            plan.append({'handle': handle, 'status': 'UNCHANGED',
                         'numeric_id': numeric_id}); continue

        plan.append({
            'handle':          handle,
            'status':          'WILL_UPDATE',
            'numeric_id':      numeric_id,
            'product_gid':     prod['id'],
            'spec_fields':     spec_fields,
            'body_changed':    body_changed,
            'new_body':        new_body if body_changed else None,
            'vendor_changed':  vendor_changed,
            'new_vendor':      vendor_override if vendor_changed else None,
            'tag_changed':     tag_changed,
            'new_tags':        new_tags_str,
        })

    will      = [p for p in plan if p['status'] == 'WILL_UPDATE']
    unchanged = [p for p in plan if p['status'] == 'UNCHANGED']
    not_found = [p for p in plan if p['status'] == 'NOT_FOUND']

    spec_writes   = sum(len(p['spec_fields']) for p in will)
    body_writes   = sum(1 for p in will if p.get('body_changed'))
    vendor_writes = sum(1 for p in will if p.get('vendor_changed'))
    tag_writes    = sum(1 for p in will if p.get('tag_changed'))

    print(f'\nPlan:')
    print(f'  Products to update: {len(will)}')
    print(f'    Spec field writes: {spec_writes}')
    print(f'    Description rewrites: {body_writes}')
    print(f'    Vendor overrides: {vendor_writes}')
    print(f'    Brand tag updates: {tag_writes}')
    print(f'  Products unchanged: {len(unchanged)}')
    print(f'  Products not found: {len(not_found)}')

    if not live:
        print(f'\n=== DRY RUN — first 3 products ===')
        for p in will[:3]:
            print(f'\n  {p["handle"]}')
            if p.get('body_changed'):
                preview = (p['new_body'] or '')[:120].replace('\n', ' ')
                print(f'    ↳ description: {preview}…')
            if p.get('vendor_changed'):
                print(f'    ↳ vendor → {p["new_vendor"]}')
            if p.get('tag_changed'):
                print(f'    ↳ tags → {p["new_tags"]}')
            for k, _, v in p['spec_fields']:
                vs = v if len(v) < 80 else v[:77] + '…'
                print(f'    + specs.{k:<25s} {vs}')
        print(f'\n(Pass --live to apply)')
        return 0

    # Apply live
    log = []; ok_p = fail_p = 0
    print(f'\n=== APPLYING — {len(will)} products ===')
    for i, p in enumerate(will, 1):
        try:
            # Spec metafields
            if p['spec_fields']:
                set_metafields(p['product_gid'], p['spec_fields'])
            # Description + vendor + tags via REST
            if p.get('body_changed') or p.get('vendor_changed') or p.get('tag_changed'):
                update_product_body(
                    p['numeric_id'],
                    p.get('new_body') or backup.get(p['handle'], {}).get('body_html', ''),
                    p.get('new_vendor'),
                    p.get('new_tags'),
                )
            ok_p += 1
            log.append({
                'handle': p['handle'],
                'status': 'OK',
                'spec_fields_set': [k for k, _, _ in p['spec_fields']],
                'description_updated': bool(p.get('body_changed')),
                'vendor_updated': bool(p.get('vendor_changed')),
                'tag_updated': bool(p.get('tag_changed')),
            })
            print(f'[{i:3d}/{len(will)}] OK  {p["handle"]}  '
                  f'({len(p["spec_fields"])} specs'
                  f'{", desc" if p.get("body_changed") else ""}'
                  f'{", vendor" if p.get("vendor_changed") else ""}'
                  f'{", tag" if p.get("tag_changed") else ""})')
        except Exception as e:
            fail_p += 1
            log.append({'handle': p['handle'], 'status': 'FAIL', 'error': str(e)[:300]})
            print(f'[{i:3d}/{len(will)}] FAIL {p["handle"]} — {e}')
        time.sleep(0.5)  # respect rate limits

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f'pe3-push-{ts}.json'
    log_path.write_text(json.dumps({
        'timestamp': ts, 'live': True,
        'mode': 'hero' if hero_mode else 'enrichment',
        'products_ok': ok_p, 'products_fail': fail_p,
        'results': log,
    }, indent=2))
    print(f'\n{"="*60}')
    print(f'Done: {ok_p} OK · {fail_p} FAIL')
    print(f'Log: {log_path}')
    print(f'Backup: {backup_path}')
    return 0 if fail_p == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
