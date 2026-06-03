#!/usr/bin/env python3
"""CATALOG — 225 vendor=BBI re-sourcing — vendor-correction writer (2026-06-02).

Reads the re-sourcing worksheet, filters classification == CONFIDENT, and for
each product: snapshot full state -> productUpdate (vendor + brand:* tag ONLY)
-> Admin-API hardened readback. HALTS immediately on any write failure or
readback mismatch.

DOES NOT touch: title, body_html, product_type, metafields, SEO, images.
Leaves AMBIGUOUS + SKIP products entirely untouched.

Usage:
  python3 scripts/apply-bbi-resourcing-2026-06-02.py             # DRY RUN (default)
  python3 scripts/apply-bbi-resourcing-2026-06-02.py --tier1     # DRY RUN, tier-1 only
  python3 scripts/apply-bbi-resourcing-2026-06-02.py --live      # apply (all CONFIDENT)
  python3 scripts/apply-bbi-resourcing-2026-06-02.py --tier1 --live

Backups: data/backups/bbi-resrc-<handle>-pre-<ts>.json (gitignored)
Log:     data/logs/bbi-resourcing-<ts>.log (gitignored)
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
WORKSHEET = ROOT / 'data' / 'reports' / 'bbi-resourcing-2026-06-02.csv'

# Sanity guard: BBI must never be a write target (it's the error we're fixing).
BBI_NAMES = {'brant business interiors', 'bbi'}
BBI_VENDOR = 'Brant Business Interiors'

# Hardened safety guards (parity with apply-ambiguous-corrections.py, the 5-write pass):
#   - refuse any row whose LIVE vendor != 'Brant Business Interiors' (drifted / already corrected)
#   - refuse any row whose LIVE first SKU != the scanned sku_sample (product-ID drift)
#   - refuse to ever write a BBI vendor or a brand:brant-* tag
# Guard failures SKIP the row and are reported — never force-written.


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
    tier1_only = '--tier1' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')

    allrows = list(csv.DictReader(WORKSHEET.open()))
    rows = [r for r in allrows if r['classification'] == 'CONFIDENT'
            and r['recommended_vendor_correction'] not in ('', 'NONE')]
    if tier1_only:
        rows = [r for r in rows if r['confidence_tier'] == 'tier1']

    # resume guard: skip products already corrected (all_ok) in any prior log
    done_pids = set()
    for lp in (ROOT / 'data' / 'logs').glob('bbi-resourcing-*.log'):
        for line in lp.read_text().splitlines():
            try:
                rec = json.loads(line)
                if rec.get('all_ok'):
                    done_pids.add(str(rec['pid']))
            except Exception:
                pass
    skipped = [r for r in rows if r['product_id'] in done_pids]
    rows = [r for r in rows if r['product_id'] not in done_pids]

    print(f"=== BBI RE-SOURCING {'[LIVE]' if live else '[DRY RUN]'}"
          f"{' tier1-only' if tier1_only else ''} : {len(rows)} to process "
          f"(resume: {len(skipped)} already corrected) ===\n")

    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    logpath = ldir / f'bbi-resourcing-{ts}.log'
    logf = logpath.open('a') if live else None

    done = 0
    exceptions = []
    for i, r in enumerate(rows, 1):
        pid = r['product_id']
        gid = f'gid://shopify/Product/{pid}'
        handle = r['product_handle']
        new_vendor = r['recommended_vendor_correction']
        brand_tag = f'brand:{slugify(new_vendor)}'

        current = rest('GET', f'/products/{pid}.json')['product']
        cur_vendor = (current.get('vendor') or '')
        cur_tags = [t.strip() for t in (current.get('tags') or '').split(',') if t.strip()]
        cur_skus = [v.get('sku', '') for v in (current.get('variants') or []) if v.get('sku')]
        cur_sku = cur_skus[0] if cur_skus else ''
        old_vendor = cur_vendor
        exp_sku = (r.get('sku_sample') or '').strip()

        # --- hardened safety guards: skip & report, never force ---
        problems = []
        if cur_vendor.strip().lower() not in BBI_NAMES:
            problems.append(f"live vendor {cur_vendor!r} != BBI (drifted / already corrected)")
        if exp_sku and cur_sku != exp_sku:
            problems.append(f"live SKU {cur_sku!r} != scanned {exp_sku!r} (ID drift)")
        if new_vendor.strip().lower() in BBI_NAMES or slugify(new_vendor).startswith('brant'):
            problems.append("refusing to write a BBI vendor / brand:brant-* tag")
        if problems:
            exceptions.append({'handle': handle, 'pid': pid, 'tier': r['confidence_tier'],
                               'new_vendor': new_vendor, 'problems': problems})
            print(f"  SKIP [{i}/{len(rows)}] {handle}: {'; '.join(problems)}")
            continue

        new_tags = list(cur_tags)
        if brand_tag not in new_tags:
            new_tags.append(brand_tag)

        added = [t for t in [brand_tag] if t not in cur_tags]
        label = (f"[{i}/{len(rows)}] {r['confidence_tier']:5s} {handle[:40]:40s} "
                 f"{old_vendor!r} -> {new_vendor!r}  +{added}  [{r['primary_signal'][:40]}]")

        if not live:
            print(label)
            continue

        cur_mf = rest('GET', f'/products/{pid}/metafields.json').get('metafields', [])
        (bdir / f'bbi-resrc-{handle}-pre-{ts}.json').write_text(
            json.dumps({'fetched': ts, 'product': current, 'metafields': cur_mf}, indent=2))

        res = gql(PRODUCT_UPDATE, {'input': {'id': gid, 'vendor': new_vendor, 'tags': new_tags}})
        errs = res['productUpdate']['userErrors']
        if errs:
            logf.write(json.dumps({'ts': ts, 'handle': handle, 'pid': pid, 'error': errs}) + '\n')
            logf.flush()
            print(f"\nXX HALT: productUpdate userErrors on {handle}: {errs}")
            sys.exit(2)

        rb = gql('{ product(id: "%s") { vendor tags } }' % gid)['product']
        vendor_ok = rb['vendor'] == new_vendor
        rb_tags = set(rb['tags'])
        brand_ok = brand_tag in rb_tags
        kept_ok = set(cur_tags).issubset(rb_tags)
        not_bbi = rb['vendor'].strip().lower() not in BBI_NAMES
        allok = vendor_ok and brand_ok and kept_ok and not_bbi

        rec = {'ts': ts, 'handle': handle, 'pid': pid, 'old_vendor': old_vendor,
               'new_vendor': new_vendor, 'brand_tag': brand_tag, 'tier': r['confidence_tier'],
               'signal': r['primary_signal'], 'vendor_ok': vendor_ok, 'brand_ok': brand_ok,
               'kept_ok': kept_ok, 'not_bbi': not_bbi, 'all_ok': allok}
        logf.write(json.dumps(rec) + '\n'); logf.flush()

        if not allok:
            print(f"\nXX HALT: readback MISMATCH on {handle}: {rec}")
            sys.exit(3)
        done += 1
        print(f"  OK [{i}/{len(rows)}] {handle}: vendor={new_vendor} +{brand_tag}")
        time.sleep(0.4)

    if live:
        logf.close()
        print(f"\n=== DONE: {done}/{len(rows)} corrected, all readbacks MATCH. "
              f"{len(exceptions)} skipped (guard). Log: {logpath.relative_to(ROOT)} ===")
    else:
        writeable = [r for r in rows
                     if r['product_id'] not in {e['pid'] for e in exceptions}]
        by_mfr = {}
        for r in writeable:
            by_mfr[r['recommended_vendor_correction']] = by_mfr.get(r['recommended_vendor_correction'], 0) + 1
        print(f"\n--- DRY-RUN SUMMARY: {len(writeable)} planned vendor corrections "
              f"({len(exceptions)} skipped by guard) ---")
        for m, n in sorted(by_mfr.items(), key=lambda x: -x[1]):
            print(f"  {m:34s} {n:4d}  -> +brand:{slugify(m)}")
        print("\nRe-run with --tier1 --live to apply. AMBIGUOUS + SKIP rows untouched.")

    if exceptions:
        print(f"\n!! GUARD EXCEPTIONS ({len(exceptions)}) — skipped, NOT written:")
        for e in exceptions:
            print(f"   - {e['handle']} ({e['tier']}, ->{e['new_vendor']}): {'; '.join(e['problems'])}")


if __name__ == '__main__':
    main()
