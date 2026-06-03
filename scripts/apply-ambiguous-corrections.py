#!/usr/bin/env python3
"""Apply validated vendor + brand-tag corrections for the AMBIGUOUS vendor=BBI set.

Source of truth: the FILLED review sheet (~/Desktop/bbi-ambiguous-review-2026-06-02.csv).
Only CLEAN-MATCH / explicitly-approved-canonical rows are written. Blanks and unresolved
NEEDS-REVIEW rows are NOT touched (handled by Brand-filter chip suppression -> Steve).

Per BBI hard rules:
  - Admin-API product writes only (vendor + tags). No theme. No watcher.
  - Dry-run by default; --live required to write.
  - Back up current state to data/backups/ and log to data/logs/ before writing.
  - Per-item hardened readback: vendor == canonical manufacturer AND brand:* tag present.
  - Safety guard: refuse to write a row whose live vendor != 'Brant Business Interiors'
    or whose live SKU != the expected SKU (guards against product-ID drift).
  - Never write 'Brant Business Interiors' and never add a brand:brant-* tag.

Usage:
  python3 scripts/apply-ambiguous-corrections.py            # dry-run
  python3 scripts/apply-ambiguous-corrections.py --live     # execute
"""
import json, sys, urllib.request, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
GQL = f'https://{SHOP}/admin/api/2024-10/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

LIVE = '--live' in sys.argv
STAMP = sys.argv[sys.argv.index('--stamp') + 1] if '--stamp' in sys.argv else 'manual'
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None  # restrict to one handle

# --- APPROVED write set (Leo-confirmed 2026-06-02) ---------------------------
# Each row: product_id, handle, expected_sku (safety guard), canonical vendor, brand tag.
# brand tag = 'brand:' + kebab(vendor). 'new_vendor' is informational only.
APPROVED = [
    {'id': '9858891776313', 'handle': 'links-custom-reception-unit-60x72',
     'expected_sku': 'CAB1622LOBBF-CTS3636G-DSK2436LR-ECU246048CLF-LTS1224G-LTS1236G',
     'vendor': 'Links Contract Furniture', 'brand_tag': 'brand:links-contract-furniture',
     'new_vendor': False, 'source': 'dict+live-vendor exact match'},
    {'id': '9682147737913', 'handle': 'student-chair-4-sizes-1', 'expected_sku': 'C-HR-4LEG12',
     'vendor': 'Alumni Educational Solutions', 'brand_tag': 'brand:alumni-educational-solutions',
     'new_vendor': True, 'source': 'Leo-approved new vendor (on-ICP education OEM)'},
    {'id': '9682149048633', 'handle': 'student-chair-4-sizes-copy', 'expected_sku': 'C-AIR-4LEG12',
     'vendor': 'Alumni Educational Solutions', 'brand_tag': 'brand:alumni-educational-solutions',
     'new_vendor': True, 'source': 'Leo-approved new vendor (on-ICP education OEM)'},
    {'id': '9682150621497', 'handle': 'student-chair-4-sizes', 'expected_sku': 'C-SVY-4LEG12',
     'vendor': 'Alumni Educational Solutions', 'brand_tag': 'brand:alumni-educational-solutions',
     'new_vendor': True, 'source': 'Leo-approved new vendor (on-ICP education OEM)'},
    {'id': '9725776691513', 'handle': 'anda-seat-phantom-king-gaming-style-office-chair',
     'expected_sku': 'SYNN-AD18XL-58-B-PVC',
     'vendor': 'AndaSeat', 'brand_tag': 'brand:andaseat',
     'new_vendor': True, 'source': 'Leo-approved new vendor (canonicalized AndaSeat)'},
]

BBI_VENDOR = 'Brant Business Interiors'


def gql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    if 'errors' in d:
        raise RuntimeError(json.dumps(d['errors'], indent=2))
    return d['data']


READ_Q = """
query($id: ID!) {
  product(id: $id) {
    legacyResourceId handle title vendor tags
    variants(first: 50) { edges { node { sku } } }
  }
}
"""

UPDATE_M = """
mutation($input: ProductInput!) {
  productUpdate(input: $input) {
    product { legacyResourceId vendor tags }
    userErrors { field message }
  }
}
"""


def read_live(pid):
    n = gql(READ_Q, {'id': f'gid://shopify/Product/{pid}'})['product']
    n['_skus'] = [v['node']['sku'] for v in n['variants']['edges'] if v['node'].get('sku')]
    return n


def main():
    mode = 'LIVE WRITE' if LIVE else 'DRY-RUN'
    work = [r for r in APPROVED if (ONLY is None or r['handle'] == ONLY)]
    print(f'=== apply-ambiguous-corrections  [{mode}]  {len(work)} products'
          + (f"  (--only {ONLY})" if ONLY else '') + ' ===\n')

    backups, results, halted = [], [], []

    for r in work:
        live = read_live(r['id'])
        cur_vendor = live['vendor']
        cur_tags = list(live['tags'])
        cur_sku = next((s for s in live['_skus']), '')

        # --- safety guards ---
        problems = []
        if cur_vendor != BBI_VENDOR:
            problems.append(f"live vendor is {cur_vendor!r}, expected {BBI_VENDOR!r}")
        if r.get('expected_sku') and cur_sku != r['expected_sku']:
            problems.append(f"live SKU {cur_sku!r} != expected {r['expected_sku']!r}")
        if r['vendor'].lower().startswith('brant') or 'brant' in r['brand_tag'].lower():
            problems.append("refusing to write a BBI vendor/brand tag")
        if problems:
            halted.append((r['handle'], problems))
            print(f"  HALT  {r['handle']}: {'; '.join(problems)}")
            continue

        new_tags = cur_tags[:]
        if r['brand_tag'] not in new_tags:
            new_tags.append(r['brand_tag'])

        backups.append({'id': r['id'], 'handle': live['handle'], 'title': live['title'],
                        'vendor': cur_vendor, 'tags': cur_tags})

        print(f"  {r['handle']}")
        print(f"      vendor: {cur_vendor!r}  ->  {r['vendor']!r}"
              + ("   (NEW VENDOR)" if r['new_vendor'] else ""))
        print(f"      tags  : +{r['brand_tag']}")

        if not LIVE:
            results.append({**r, 'status': 'dry-run'})
            continue

        # --- write ---
        out = gql(UPDATE_M, {'input': {'id': f"gid://shopify/Product/{r['id']}",
                                       'vendor': r['vendor'], 'tags': new_tags}})
        ue = out['productUpdate']['userErrors']
        if ue:
            print(f"      ERROR: {ue}")
            results.append({**r, 'status': 'error', 'userErrors': ue})
            continue

        # --- hardened readback ---
        rb = read_live(r['id'])
        ok_vendor = rb['vendor'] == r['vendor']
        ok_tag = r['brand_tag'] in rb['tags']
        ok_nobbi = rb['vendor'] != BBI_VENDOR
        verdict = 'PASS' if (ok_vendor and ok_tag and ok_nobbi) else 'FAIL'
        print(f"      readback: vendor={rb['vendor']!r} tag={'yes' if ok_tag else 'NO'} -> {verdict}")
        results.append({**r, 'status': verdict, 'readback_vendor': rb['vendor'],
                        'readback_tags': rb['tags']})

    # --- persist backup + log on live runs ---
    if LIVE:
        ts = STAMP
        bdir = ROOT / 'data/backups'; bdir.mkdir(parents=True, exist_ok=True)
        ldir = ROOT / 'data/logs'; ldir.mkdir(parents=True, exist_ok=True)
        (bdir / f'ambiguous-corrections-pre-{ts}.json').write_text(json.dumps(backups, indent=2))
        (ldir / f'ambiguous-corrections-{ts}.json').write_text(json.dumps(results, indent=2))
        print(f"\n  backup -> data/backups/ambiguous-corrections-pre-{ts}.json")
        print(f"  log    -> data/logs/ambiguous-corrections-{ts}.json")

    passes = sum(1 for x in results if x.get('status') == 'PASS')
    print(f"\n=== {mode} done: {len(results)} processed, "
          f"{passes} PASS, {len(halted)} halted ===")
    if halted:
        print("HALTED rows (not written):")
        for h, p in halted:
            print(f"  - {h}: {'; '.join(p)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
