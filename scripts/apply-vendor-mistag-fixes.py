#!/usr/bin/env python3
"""§4 VENDOR MIS-TAG FIX — apply HIGH-confidence vendor corrections (LIVE writes).

Reads data/reports/vendor-mistag-candidates-<date>.csv, filters classification ==
HIGH, and for each product: snapshot full state (backup) -> productUpdate (VENDOR
field ONLY) -> hardened INDEPENDENT readback (exact match). HALTS on any write
error or readback mismatch. Paces to avoid 429s.

Scope: vendor field only. Does NOT touch title, body, tags, metafields, images,
price, availability, theme.

Usage:
  python3 scripts/apply-vendor-mistag-fixes.py          # DRY RUN (default)
  python3 scripts/apply-vendor-mistag-fixes.py --live    # apply

Backups: data/backups/feed-vendor-<handle>-pre-<ts>.json (gitignored)
Log:     data/logs/feed-vendor-corrections-<ts>.log (gitignored)
"""
import json, sys, csv, time, urllib.request, urllib.error
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
DATE = datetime.now().strftime('%Y-%m-%d')
CANDIDATES = ROOT / 'data' / 'reports' / f'vendor-mistag-candidates-{DATE}.csv'


def _open(req):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 2 ** attempt
                print(f"   (HTTP {e.code} backoff {wait}s)", flush=True)
                time.sleep(wait)
                continue
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
    product { id vendor }
    userErrors { field message }
  }
}'''


def check_write_scope():
    q = '{ currentAppInstallation { accessScopes { handle } } }'
    try:
        scopes = [s['handle'] for s in gql(q)['currentAppInstallation']['accessScopes']]
        has = 'write_products' in scopes
        print(f"  access scopes: {', '.join(scopes)}")
        print(f"  write_products present: {has}")
        return has
    except Exception as e:
        print(f"  (could not enumerate scopes: {e}) — proceeding; readback will confirm")
        return None


def main():
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    rows = [r for r in csv.DictReader(CANDIDATES.open()) if r['classification'] == 'HIGH']

    print(f"=== §4 VENDOR FIX {'[LIVE]' if live else '[DRY RUN]'} : {len(rows)} HIGH-confidence corrections ===\n")
    print("Preflight — write scope:")
    has_scope = check_write_scope()
    if live and has_scope is False:
        sys.exit("FATAL: token lacks write_products scope — aborting before any write.")
    print()

    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    logpath = ldir / f'feed-vendor-corrections-{ts}.log'
    logf = logpath.open('a') if live else None

    done = 0
    for i, r in enumerate(rows, 1):
        pid = r['id']
        gid = f'gid://shopify/Product/{pid}'
        handle = r['handle']
        new_vendor = r['expected_vendor']

        current = rest('GET', f'/products/{pid}.json')['product']
        old_vendor = current.get('vendor')
        label = f"[{i}/{len(rows)}] {handle} ({pid})  {old_vendor!r} -> {new_vendor!r}  | ev: {r['evidence'][:70]}"

        if old_vendor == new_vendor:
            print(f"  SKIP (already correct) {label}")
            continue
        if not live:
            print("  " + label)
            continue

        # snapshot full state BEFORE write
        (bdir / f'feed-vendor-{handle}-pre-{ts}.json').write_text(
            json.dumps({'fetched': ts, 'product': current}, indent=2))

        res = gql(PRODUCT_UPDATE, {'input': {'id': gid, 'vendor': new_vendor}})
        errs = res['productUpdate']['userErrors']
        if errs:
            logf.write(json.dumps({'ts': ts, 'handle': handle, 'pid': pid, 'error': errs}) + '\n'); logf.flush()
            print(f"\nXX HALT: productUpdate userErrors on {handle}: {errs}")
            sys.exit(2)

        # hardened INDEPENDENT readback (fresh GraphQL query), exact match
        rb = gql('{ product(id: "%s") { vendor } }' % gid)['product']
        vendor_ok = rb['vendor'] == new_vendor   # exact, not substring
        rec = {'ts': ts, 'handle': handle, 'pid': pid, 'old_vendor': old_vendor,
               'new_vendor': new_vendor, 'evidence': r['evidence'],
               'readback_vendor': rb['vendor'], 'vendor_ok': vendor_ok, 'all_ok': vendor_ok}
        logf.write(json.dumps(rec) + '\n'); logf.flush()
        if not vendor_ok:
            print(f"\nXX HALT: readback MISMATCH on {handle}: got {rb['vendor']!r} expected {new_vendor!r}")
            sys.exit(3)
        done += 1
        print(f"  OK {label}  [readback={rb['vendor']!r} ✓]")
        time.sleep(0.6)

    if live:
        logf.close()
        print(f"\n=== DONE: {done}/{len(rows)} corrected, all readbacks EXACT-MATCH. Log: {logpath.relative_to(ROOT)} ===")
    else:
        print(f"\nDRY RUN complete — {len(rows)} HIGH fixes planned. Re-run with --live to apply.")


if __name__ == '__main__':
    main()
