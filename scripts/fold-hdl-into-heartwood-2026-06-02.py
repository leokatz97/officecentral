#!/usr/bin/env python3
"""CATALOG — fold stray HDL fragment chip into canonical Heartwood Manufacturing (2026-06-02).

Single-product cleanup. The store has exactly 1 product still at vendor `HDL`
(brand:hdl). HDL = "Heartwood Distributors Ltd." is the same brand family as
Heartwood (HTW) per data/reference/sku-prefix-lookup.yaml. The canonical chip is
`Heartwood Manufacturing` (brand:heartwood-manufacturing, 79 products). This
script folds the leftover fragment into the canonical:

  vendor  HDL                  -> Heartwood Manufacturing
  tags    +brand:heartwood-manufacturing  -brand:hdl   (all other tags kept)

Mirrors scripts/apply-bbi-resourcing-2026-06-02.py: snapshot full state ->
productUpdate (vendor + brand tags ONLY) -> hardened Admin-API readback. HALTS
on any write failure or readback mismatch.

DOES NOT touch: title, body_html, product_type, metafields, SEO, images.

Usage:
  python3 scripts/fold-hdl-into-heartwood-2026-06-02.py          # DRY RUN (default)
  python3 scripts/fold-hdl-into-heartwood-2026-06-02.py --live   # apply

Backup: data/backups/fold-hdl-<handle>-pre-<ts>.json (gitignored)
Log:    data/logs/fold-hdl-<ts>.log (gitignored)
"""
import json, sys, re, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
REST = f'https://{SHOP}/admin/api/2024-10'
GQL = f'{REST}/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

HANDLE = ('hdl-5-resin-folding-table-granite-rectangle-dove-white-pebble-top-'
          'powder-coated-base-60-table-top-length-x-30-table-top-width-29-height-1')

TARGET_VENDOR = 'Heartwood Manufacturing'
TARGET_BRAND_TAG = 'brand:heartwood-manufacturing'
STALE_BRAND_TAG = 'brand:hdl'
# Guards: the live product MUST currently be the stray HDL fragment, never the
# canonical chip already, and we must never write a BBI vendor.
EXPECTED_VENDORS = {'hdl', 'heartwood distributors ltd.'}
BBI_NAMES = {'brant business interiors', 'bbi'}


def _open(req):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 2 ** attempt
                print(f"   (HTTP {e.code} — backing off {wait}s)", flush=True)
                time.sleep(wait)
                continue
            raise


def gql(query, variables=None):
    req = urllib.request.Request(GQL, data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
                                 headers=HDR, method='POST')
    out = _open(req)
    if 'errors' in out:
        raise RuntimeError(f"GraphQL errors: {out['errors']}")
    return out['data']


def rest(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f'{REST}{path}', data=data, headers=HDR, method=method)
    return _open(req)


PRODUCT_UPDATE = '''
mutation($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id vendor tags }
    userErrors { field message }
  }
}'''


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')


def main():
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')

    # sanity: target tag must match target vendor's slug
    assert TARGET_BRAND_TAG == f'brand:{slugify(TARGET_VENDOR)}', 'brand tag/vendor mismatch'

    print(f"=== FOLD HDL -> HEARTWOOD {'[LIVE]' if live else '[DRY RUN]'} ===\n")

    # locate the product by handle (read-only)
    data = gql('{ productByHandle(handle: "%s") { id legacyResourceId } }' % HANDLE)
    node = data.get('productByHandle')
    if not node:
        sys.exit(f"FATAL: no product found for handle {HANDLE!r}")
    pid = node['legacyResourceId']
    gid = node['id']

    current = rest('GET', f'/products/{pid}.json')['product']
    cur_vendor = (current.get('vendor') or '')
    cur_tags = [t.strip() for t in (current.get('tags') or '').split(',') if t.strip()]
    cur_skus = [v.get('sku', '') for v in (current.get('variants') or []) if v.get('sku')]
    cur_sku = cur_skus[0] if cur_skus else ''

    print(f"  product_id : {pid}")
    print(f"  handle     : {HANDLE}")
    print(f"  title      : {current.get('title')}")
    print(f"  first SKU  : {cur_sku}")
    print(f"  vendor     : {cur_vendor!r}")
    print(f"  tags       : {cur_tags}\n")

    # --- hardened safety guards: refuse to write if the product isn't the stray HDL ---
    problems = []
    if cur_vendor.strip().lower() not in EXPECTED_VENDORS:
        problems.append(f"live vendor {cur_vendor!r} not in expected HDL set "
                        f"(already folded / wrong product?)")
    if STALE_BRAND_TAG not in cur_tags:
        problems.append(f"expected stale tag {STALE_BRAND_TAG!r} absent (already folded?)")
    # Heartwood family: vendor code HDL (distributor) but SKUs carry the HTW
    # (Heartwood) manufacturer prefix — accept either per sku-prefix-lookup.yaml.
    if not cur_sku.upper().startswith(('HDL', 'HTW')):
        problems.append(f"first SKU {cur_sku!r} not a Heartwood-family prefix "
                        f"(HDL/HTW) — ID drift?")
    if TARGET_VENDOR.strip().lower() in BBI_NAMES or slugify(TARGET_VENDOR).startswith('brant'):
        problems.append("refusing to write a BBI vendor / brand:brant-* tag")
    if problems:
        print("!! GUARD EXCEPTION — refusing to write:")
        for p in problems:
            print(f"   - {p}")
        sys.exit(1)

    # build new tag set: add canonical, drop stale, keep everything else
    new_tags = [t for t in cur_tags if t != STALE_BRAND_TAG]
    if TARGET_BRAND_TAG not in new_tags:
        new_tags.append(TARGET_BRAND_TAG)
    added = [TARGET_BRAND_TAG] if TARGET_BRAND_TAG not in cur_tags else []
    removed = [STALE_BRAND_TAG] if STALE_BRAND_TAG in cur_tags else []

    print("  PLANNED WRITE:")
    print(f"    vendor : {cur_vendor!r} -> {TARGET_VENDOR!r}")
    print(f"    +tags  : {added}")
    print(f"    -tags  : {removed}")
    print(f"    final tags : {new_tags}\n")

    if not live:
        print("DRY RUN — no write performed. Re-run with --live to apply.")
        return

    # snapshot full state + metafields before the write
    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    cur_mf = rest('GET', f'/products/{pid}/metafields.json').get('metafields', [])
    bpath = bdir / f'fold-hdl-{HANDLE}-pre-{ts}.json'
    bpath.write_text(json.dumps({'fetched': ts, 'product': current, 'metafields': cur_mf}, indent=2))
    print(f"  backup -> {bpath.relative_to(ROOT)}")

    res = gql(PRODUCT_UPDATE, {'input': {'id': gid, 'vendor': TARGET_VENDOR, 'tags': new_tags}})
    errs = res['productUpdate']['userErrors']
    logpath = ldir / f'fold-hdl-{ts}.log'
    if errs:
        logpath.write_text(json.dumps({'ts': ts, 'handle': HANDLE, 'pid': pid, 'error': errs}) + '\n')
        sys.exit(f"\nXX HALT: productUpdate userErrors: {errs}")

    # hardened readback
    rb = gql('{ product(id: "%s") { vendor tags } }' % gid)['product']
    rb_tags = set(rb['tags'])
    vendor_ok = rb['vendor'] == TARGET_VENDOR
    brand_ok = TARGET_BRAND_TAG in rb_tags
    stale_gone = STALE_BRAND_TAG not in rb_tags
    kept_ok = set(t for t in cur_tags if t != STALE_BRAND_TAG).issubset(rb_tags)
    not_bbi = rb['vendor'].strip().lower() not in BBI_NAMES
    allok = vendor_ok and brand_ok and stale_gone and kept_ok and not_bbi

    rec = {'ts': ts, 'handle': HANDLE, 'pid': pid, 'old_vendor': cur_vendor,
           'new_vendor': TARGET_VENDOR, 'brand_tag': TARGET_BRAND_TAG,
           'vendor_ok': vendor_ok, 'brand_ok': brand_ok, 'stale_gone': stale_gone,
           'kept_ok': kept_ok, 'not_bbi': not_bbi, 'all_ok': allok}
    logpath.write_text(json.dumps(rec) + '\n')

    print(f"\n  readback: vendor={rb['vendor']!r}  tags={sorted(rb_tags)}")
    print(f"  checks: vendor_ok={vendor_ok} brand_ok={brand_ok} stale_gone={stale_gone} "
          f"kept_ok={kept_ok} not_bbi={not_bbi}")
    if not allok:
        sys.exit(f"\nXX HALT: readback MISMATCH: {rec}")
    print(f"\n=== DONE: HDL fragment folded into Heartwood Manufacturing, readback MATCH. "
          f"Log: {logpath.relative_to(ROOT)} ===")


if __name__ == '__main__':
    main()
