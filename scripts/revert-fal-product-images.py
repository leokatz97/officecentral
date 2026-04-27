"""
Revert AI-generated product images pushed by push-generated-images.py.

Reads data/reports/shopify-images-pushed-2026-04-25.csv (or --manifest=path),
and DELETEs each row's Shopify_Image_ID from its product. Position 1 (the
original product photo) is never touched — only the rows logged in the push
manifest are removed, so this is a clean revert to the pre-push gallery.

Idempotent: re-running is safe. Already-deleted images (404) are recorded as
'already_gone' and don't fail the run.

Usage:
  python3 scripts/revert-fal-product-images.py                                 # dry run
  python3 scripts/revert-fal-product-images.py --live                          # delete from Shopify
  python3 scripts/revert-fal-product-images.py --manifest=path/to.csv --live
  python3 scripts/revert-fal-product-images.py --limit=5 --live                # smoke test
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type':           'application/json',
}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
DEFAULT_MANIFEST = os.path.join(RPT_DIR, 'shopify-images-pushed-2026-04-25.csv')
TS = datetime.now().strftime('%Y%m%d-%H%M%S')


def parse_args():
    live     = '--live' in sys.argv
    limit    = None
    manifest = DEFAULT_MANIFEST
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
        elif arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
    return live, limit, manifest


def load_manifest(path):
    print('Loading manifest: ' + path)
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') != 'PUSHED':
                continue
            if not row.get('Shopify_Image_ID') or not row.get('Product_ID'):
                continue
            rows.append(row)
    print('Found {} PUSHED rows to revert.'.format(len(rows)))
    return rows


def delete_image(product_id, image_id, retries=3):
    """DELETE Shopify image. Returns 'deleted', 'already_gone', or raises."""
    url = '{}/products/{}/images/{}.json'.format(API, product_id, image_id)
    req = urllib.request.Request(url, headers=HEADERS, method='DELETE')
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp.read()
                return 'deleted'
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 'already_gone'
            if e.code == 429:
                wait = attempt * 5
                print('  429 rate limit — sleeping {}s'.format(wait))
                time.sleep(wait)
                last_err = e
                continue
            raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                wait = attempt * 5
                print('  network error (attempt {}/{}): {} — retrying in {}s'.format(attempt, retries, e, wait))
                time.sleep(wait)
    raise last_err


def main():
    live, limit, manifest_path = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)

    os.makedirs(LOG_DIR, exist_ok=True)

    rows = load_manifest(manifest_path)

    if limit:
        # limit by unique handles
        seen = []
        filtered = []
        for row in rows:
            h = row['Handle']
            if h not in seen:
                seen.append(h)
            if len(seen) <= limit:
                filtered.append(row)
        rows = filtered
        print('Limiting to first {} products ({} images).'.format(limit, len(rows)))

    by_handle = {}
    for row in rows:
        by_handle.setdefault(row['Handle'], []).append(row)

    total_products = len(by_handle)
    total_images   = len(rows)
    print('{} images across {} products to revert.\n'.format(total_images, total_products))

    deleted      = []
    already_gone = []
    errors       = []
    result_rows  = []

    for i, (handle, img_rows) in enumerate(by_handle.items(), 1):
        print('[{}/{}] {}'.format(i, total_products, handle))

        for row in sorted(img_rows, key=lambda r: int(r['Image_Position'])):
            pid    = row['Product_ID']
            img_id = row['Shopify_Image_ID']
            pos    = row['Image_Position']

            if not live:
                print('  pos-{}: DRY RUN — would DELETE image {} from product {}'.format(pos, img_id, pid))
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': img_id,
                    'Outcome':          'DRY_RUN',
                })
                continue

            try:
                outcome = delete_image(pid, img_id)
                if outcome == 'deleted':
                    deleted.append((handle, img_id))
                    print('  pos-{}: DELETED image {}'.format(pos, img_id))
                else:
                    already_gone.append((handle, img_id))
                    print('  pos-{}: already gone (404) image {}'.format(pos, img_id))
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': img_id,
                    'Outcome':          outcome,
                })
                time.sleep(0.5)

            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:200]
                print('  pos-{}: ERROR {} — {}'.format(pos, e.code, msg[:120]))
                errors.append({'handle': handle, 'image_id': img_id, 'code': e.code, 'msg': msg})
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': img_id,
                    'Outcome':          'ERROR_{}'.format(e.code),
                })
            except Exception as e:
                print('  pos-{}: ERROR — {}'.format(pos, e))
                errors.append({'handle': handle, 'image_id': img_id, 'code': 0, 'msg': str(e)})
                result_rows.append({
                    'Handle':           handle,
                    'Product_ID':       pid,
                    'Image_Position':   pos,
                    'Shopify_Image_ID': img_id,
                    'Outcome':          'ERROR_NET',
                })

    out_csv = os.path.join(RPT_DIR, 'fal-image-revert-{}.csv'.format(TS))
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Handle', 'Product_ID', 'Image_Position',
                                                'Shopify_Image_ID', 'Outcome'])
        writer.writeheader()
        writer.writerows(result_rows)

    log_path = os.path.join(LOG_DIR, 'revert-fal-images-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':           mode,
            'manifest':       manifest_path,
            'total_products': total_products,
            'total_images':   total_images,
            'deleted':        len(deleted),
            'already_gone':   len(already_gone),
            'errors':         len(errors),
            'error_details':  errors,
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Products:     {}'.format(total_products))
    print('  Deleted:      {}'.format(len(deleted)))
    print('  Already gone: {}'.format(len(already_gone)))
    print('  Errors:       {}'.format(len(errors)))
    print('  Results CSV:  ' + out_csv)
    print('  Audit log:    ' + log_path)

    if not live:
        print('\n[DRY RUN] No deletes performed. Re-run with --live to revert.')


if __name__ == '__main__':
    main()
