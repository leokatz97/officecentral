#!/usr/bin/env python3
"""ITEM 1 — finish the 2 Part-Time chairs (brand tag + specs.manufacturer).

Vendor was already corrected to "OTG / Offices to Go" by §4. This closes the
residual: the `brand:` tag and `specs.manufacturer` metafield still carry the
ergoCentric corruption (mvl2836) / are absent (mvl2837) and mis-route the products.

Per product:  snapshot full state (backup) -> productUpdate(tags) +
metafieldsSet(specs.manufacturer) -> hardened INDEPENDENT readback (exact match).
HALTS on any write error or readback mismatch. Paces to avoid 429s.

Scope: tags (brand: only) + specs.manufacturer metafield. Does NOT touch vendor
(already correct), title, body, images, price, availability, status, theme.

Usage:
  python3 scripts/apply-parttime-tag-mfr-fix.py            # DRY RUN (default)
  python3 scripts/apply-parttime-tag-mfr-fix.py --live     # apply
"""
import json, sys, time, urllib.request, urllib.error
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

NEW_MFR = 'OTG / Offices to Go'   # exact match to corrected vendor
NEW_BRAND_TAG = 'brand:offices-to-go'
TARGETS = ['10196146585913', '10197752348985']  # mvl2836, mvl2837 legacy ids


def _open(req):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 2 ** attempt
                print(f"   (HTTP {e.code} backoff {wait}s)", flush=True)
                time.sleep(wait); continue
            print(f"HTTPError {e.code}: {e.read().decode()[:400]}", file=sys.stderr)
            raise


def gql(query, variables=None):
    req = urllib.request.Request(GQL, data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
                                 headers=HDR, method='POST')
    out = _open(req)
    if 'errors' in out:
        raise RuntimeError(f"GraphQL errors: {out['errors']}")
    return out['data']


def rest(method, path):
    req = urllib.request.Request(f'{REST}{path}', headers=HDR, method=method)
    return _open(req)


PRODUCT_UPDATE = '''
mutation($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id tags }
    userErrors { field message }
  }
}'''

MF_SET = '''
mutation($mf: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $mf) {
    metafields { namespace key value type }
    userErrors { field message }
  }
}'''

FULL_Q = '''
{ product(id: "gid://shopify/Product/%s") {
    id legacyResourceId handle vendor tags
    metafields(first: 50) { edges { node { namespace key value type } } }
} }'''


def fetch(pid):
    return gql(FULL_Q % pid)['product']


def main():
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    print(f"=== ITEM 1 Part-Time tag+mfr fix {'[LIVE]' if live else '[DRY RUN]'} ===\n")
    # scope check
    scopes = [s['handle'] for s in gql('{currentAppInstallation{accessScopes{handle}}}')['currentAppInstallation']['accessScopes']]
    if live and 'write_products' not in scopes:
        sys.exit("FATAL: token lacks write_products — aborting before any write.")

    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    logpath = ldir / f'parttime-tag-mfr-{ts}.log'
    logf = logpath.open('a') if live else None

    for pid in TARGETS:
        p = fetch(pid)
        gid = p['id']
        handle = p['handle']
        old_tags = p['tags']
        new_tags = [t for t in old_tags if not t.lower().startswith('brand:')] + [NEW_BRAND_TAG]
        mfr_now = next((e['node']['value'] for e in p['metafields']['edges']
                        if e['node']['namespace'] == 'specs' and e['node']['key'] == 'manufacturer'), None)
        print(f"[{handle}] ({pid}) vendor={p['vendor']!r}")
        print(f"   tags  {old_tags}  ->  {new_tags}")
        print(f"   specs.manufacturer  {mfr_now!r}  ->  {NEW_MFR!r}")

        if not live:
            print("   (dry run — no write)\n"); continue

        # backup full pre-state
        (bdir / f'parttime-{handle}-pre-{ts}.json').write_text(
            json.dumps({'fetched': ts, 'product': p}, indent=2))

        # write tags
        r1 = gql(PRODUCT_UPDATE, {'input': {'id': gid, 'tags': new_tags}})
        e1 = r1['productUpdate']['userErrors']
        if e1:
            logf.write(json.dumps({'ts': ts, 'handle': handle, 'tag_error': e1}) + '\n'); logf.flush()
            sys.exit(f"\nXX HALT: productUpdate(tags) userErrors on {handle}: {e1}")
        time.sleep(0.5)
        # write metafield
        r2 = gql(MF_SET, {'mf': [{'ownerId': gid, 'namespace': 'specs', 'key': 'manufacturer',
                                  'type': 'single_line_text_field', 'value': NEW_MFR}]})
        e2 = r2['metafieldsSet']['userErrors']
        if e2:
            logf.write(json.dumps({'ts': ts, 'handle': handle, 'mf_error': e2}) + '\n'); logf.flush()
            sys.exit(f"\nXX HALT: metafieldsSet userErrors on {handle}: {e2}")
        time.sleep(0.6)

        # hardened independent readback (fresh query), exact match
        rb = fetch(pid)
        rb_tags = rb['tags']
        rb_mfr = next((e['node']['value'] for e in rb['metafields']['edges']
                       if e['node']['namespace'] == 'specs' and e['node']['key'] == 'manufacturer'), None)
        tag_ok = ('brand:offices-to-go' in [t.lower() for t in rb_tags]
                  and not any(t.lower() == 'brand:ergocentric' for t in rb_tags))
        mfr_ok = rb_mfr == NEW_MFR
        rec = {'ts': ts, 'handle': handle, 'pid': pid,
               'readback_tags': rb_tags, 'readback_mfr': rb_mfr,
               'tag_ok': tag_ok, 'mfr_ok': mfr_ok, 'all_ok': tag_ok and mfr_ok}
        logf.write(json.dumps(rec) + '\n'); logf.flush()
        if not (tag_ok and mfr_ok):
            sys.exit(f"\nXX HALT: readback MISMATCH on {handle}: tags={rb_tags} mfr={rb_mfr!r}")
        print(f"   OK [readback tags={rb_tags} | specs.manufacturer={rb_mfr!r}] ✓\n")
        time.sleep(0.6)

    if live:
        logf.close()
        print(f"=== DONE — both Part-Time chairs corrected, readbacks EXACT-MATCH. Log: {logpath.relative_to(ROOT)} ===")
    else:
        print("DRY RUN complete — re-run with --live to apply.")


if __name__ == '__main__':
    main()
