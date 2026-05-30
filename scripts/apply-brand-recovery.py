#!/usr/bin/env python3
"""PHASE-A-BLOCK-4-SESSION-3 — Phase 4 vendor-correction writer.

Reads the brand-recovery worksheet, filters decision == APPROVE, and for each
product: snapshots full state -> productUpdate (vendor + brand:/sub-brand: tags
ONLY) -> Admin-API readback verify. HALTS immediately on any write failure or
readback mismatch.

DOES NOT touch: title, body_html, product_type, metafields, SEO, images.

Usage:
  python3 scripts/apply-brand-recovery.py            # DRY RUN (default, per BBI rules)
  python3 scripts/apply-brand-recovery.py --live     # apply

Backups: data/backups/b4s3-<handle>-pre-<ts>.json (gitignored)
Log:     data/logs/b4s3-vendor-corrections-<ts>.log (gitignored)
"""
import json, sys, csv, re, time, urllib.request, urllib.error
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
WORKSHEET = ROOT / 'data' / 'reports' / 'brand-recovery-2026-05-30.csv'


def _open(req):
    """urlopen with 429/5xx retry + exponential backoff."""
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
    s = re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')
    return s


def main():
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    rows = [r for r in csv.DictReader(WORKSHEET.open()) if r['decision'] == 'APPROVE']

    # resume guard: skip products already corrected (all_ok) in any prior b4s3 log
    done_pids = set()
    for lp in (ROOT / 'data' / 'logs').glob('b4s3-vendor-corrections-*.log'):
        for line in lp.read_text().splitlines():
            try:
                rec = json.loads(line)
                if rec.get('all_ok'):
                    done_pids.add(str(rec['pid']))
            except Exception:
                pass
    skipped = [r for r in rows if r['product_id'] in done_pids]
    rows = [r for r in rows if r['product_id'] not in done_pids]
    print(f"=== B4S3 VENDOR CORRECTION {'[LIVE]' if live else '[DRY RUN]'} : "
          f"{len(rows)} to process (resume: {len(skipped)} already corrected, skipped) ===\n")

    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    logpath = ldir / f'b4s3-vendor-corrections-{ts}.log'
    logf = logpath.open('a') if live else None

    done = 0
    for i, r in enumerate(rows, 1):
        pid = r['product_id']
        gid = f'gid://shopify/Product/{pid}'
        handle = r['product_handle']
        new_vendor = r['recommended_vendor_correction']
        brand_tag = f'brand:{slugify(new_vendor)}'
        sub_tag = f'sub-brand:{slugify(r["sub_brand_detected"])}' if r['sub_brand_detected'].strip() else None

        # GET current full state (REST) for snapshot + current tags
        current = rest('GET', f'/products/{pid}.json')['product']
        cur_tags = [t.strip() for t in (current.get('tags') or '').split(',') if t.strip()]
        new_tags = list(cur_tags)
        for t in ([brand_tag] + ([sub_tag] if sub_tag else [])):
            if t not in new_tags:
                new_tags.append(t)
        old_vendor = current.get('vendor')

        label = f"[{i}/{len(rows)}] {handle} ({pid})  {old_vendor!r} -> {new_vendor!r}  +{[t for t in ([brand_tag]+([sub_tag] if sub_tag else [])) if t not in cur_tags]}"

        if not live:
            print(label)
            continue

        # snapshot
        cur_mf = rest('GET', f'/products/{pid}/metafields.json').get('metafields', [])
        (bdir / f'b4s3-{handle}-pre-{ts}.json').write_text(
            json.dumps({'fetched': ts, 'product': current, 'metafields': cur_mf}, indent=2))

        # productUpdate (vendor + tags ONLY)
        res = gql(PRODUCT_UPDATE, {'input': {'id': gid, 'vendor': new_vendor, 'tags': new_tags}})
        errs = res['productUpdate']['userErrors']
        if errs:
            logf.write(json.dumps({'ts': ts, 'handle': handle, 'pid': pid, 'error': errs}) + '\n')
            logf.flush()
            print(f"\nXX HALT: productUpdate userErrors on {handle}: {errs}")
            sys.exit(2)

        # readback verify
        rb = gql('{ product(id: "%s") { vendor tags } }' % gid)['product']
        vendor_ok = rb['vendor'] == new_vendor
        rb_tags = set(rb['tags'])
        brand_ok = brand_tag in rb_tags
        sub_ok = (sub_tag in rb_tags) if sub_tag else True
        kept_ok = set(cur_tags).issubset(rb_tags)   # no existing tags dropped
        allok = vendor_ok and brand_ok and sub_ok and kept_ok

        rec = {'ts': ts, 'handle': handle, 'pid': pid, 'old_vendor': old_vendor,
               'new_vendor': new_vendor, 'brand_tag': brand_tag, 'sub_tag': sub_tag,
               'vendor_ok': vendor_ok, 'brand_ok': brand_ok, 'sub_ok': sub_ok,
               'kept_ok': kept_ok, 'all_ok': allok}
        logf.write(json.dumps(rec) + '\n'); logf.flush()

        if not allok:
            print(f"\nXX HALT: readback MISMATCH on {handle}: {rec}")
            sys.exit(3)
        done += 1
        print(f"  OK [{i}/{len(rows)}] {handle}: vendor={new_vendor} +{brand_tag}" + (f" +{sub_tag}" if sub_tag else ""))
        time.sleep(0.5)

    if live:
        logf.close()
        print(f"\n=== DONE: {done}/{len(rows)} corrected, all readbacks MATCH. Log: {logpath.relative_to(ROOT)} ===")
    else:
        print(f"\nDRY RUN complete — {len(rows)} products planned. Re-run with --live to apply.")


if __name__ == '__main__':
    main()
