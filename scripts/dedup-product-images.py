"""
Delete duplicate AI-generated images pushed twice due to a mid-run crash.

Expected state per product: 1 original (position 1) + 3 AI images (positions 2–4) = 4 total.
Products with > 4 images had their AI images pushed twice; this script deletes everything
beyond the first 4 images (sorted by position, then by ID as tie-breaker).

Usage:
  python3 scripts/dedup-product-images.py                                       # dry run
  python3 scripts/dedup-product-images.py --live                                # actually delete
  python3 scripts/dedup-product-images.py --manifest=data/reports/generated-images-2026-04-24.csv --live
  python3 scripts/dedup-product-images.py --limit=10                            # spot-check first N products
"""
import csv
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type':           'application/json',
}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
def parse_args():
    live     = '--live' in sys.argv
    limit    = None
    manifest = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
        elif arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
    return live, limit, manifest


# ---------------------------------------------------------------------------
# Manifest loader — returns list of unique handles in CSV order
# ---------------------------------------------------------------------------
def load_handles(path=None):
    if path:
        csv_path = path
    else:
        pattern = os.path.join(RPT_DIR, 'generated-images-*.csv')
        matches = sorted(glob.glob(pattern))
        if not matches:
            sys.exit('No generated-images-*.csv found in {}. Specify --manifest=path.'.format(RPT_DIR))
        csv_path = matches[-1]

    print('Loading manifest: ' + csv_path)
    seen    = []
    handles = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            h = row.get('Handle', '').strip()
            if h and h not in seen:
                seen.append(h)
                handles.append(h)
    print('Found {} unique product handles.\n'.format(len(handles)))
    return handles


# ---------------------------------------------------------------------------
# Shopify API helpers
# ---------------------------------------------------------------------------
def fetch_product_id(handle):
    encoded = urllib.parse.quote(handle)
    url = '{}/products.json?handle={}&fields=id&limit=1'.format(API, encoded)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data     = json.loads(resp.read().decode())
            products = data.get('products', [])
            return str(products[0]['id']) if products else None
    except urllib.error.HTTPError as e:
        print('  FETCH-ERR {}: {}'.format(e.code, e.read().decode()[:100]))
        return None
    except Exception as e:
        print('  FETCH-ERR: {}'.format(e))
        return None


def fetch_images(product_id):
    url = '{}/products/{}/images.json?fields=id,position,src&limit=250'.format(API, product_id)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get('images', [])
    except urllib.error.HTTPError as e:
        print('  IMG-FETCH-ERR {}: {}'.format(e.code, e.read().decode()[:100]))
        return None
    except Exception as e:
        print('  IMG-FETCH-ERR: {}'.format(e))
        return None


def delete_image(product_id, image_id):
    url = '{}/products/{}/images/{}.json'.format(API, product_id, image_id)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN}, method='DELETE')
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return True
    except urllib.error.HTTPError as e:
        print('  DEL-ERR {}: image_id={} - {}'.format(e.code, image_id, e.read().decode()[:100]))
        return False
    except Exception as e:
        print('  DEL-ERR: image_id={} - {}'.format(image_id, e))
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, limit, manifest_path = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)
    print()

    os.makedirs(LOG_DIR, exist_ok=True)

    handles = load_handles(manifest_path)

    if limit:
        handles = handles[:limit]
        print('Limiting to first {} products.\n'.format(limit))

    total_products  = len(handles)
    affected        = []   # handles with > 4 images
    deleted_count   = 0
    error_count     = 0
    not_found_count = 0
    log_entries     = []

    for i, handle in enumerate(handles, 1):
        pid = fetch_product_id(handle)
        time.sleep(0.6)  # gap between product-lookup and image-list calls to stay under 2 req/s
        if not pid:
            print('[{}/{}] {} — NOT FOUND in Shopify, skipping'.format(i, total_products, handle))
            not_found_count += 1
            continue

        images = fetch_images(pid)
        if images is None:
            print('[{}/{}] {} — ERROR fetching images, skipping'.format(i, total_products, handle))
            error_count += 1
            time.sleep(0.5)
            continue

        # Sort by position asc, then by id asc as tie-breaker (keeps the first set of 3 AI images)
        images_sorted = sorted(images, key=lambda img: (img.get('position', 999), img.get('id', 0)))
        total_images  = len(images_sorted)

        if total_images <= 4:
            print('[{}/{}] {} — {} images, OK'.format(i, total_products, handle, total_images))
            time.sleep(0.5)
            continue

        # Images beyond position 4 are the duplicates
        to_delete  = images_sorted[4:]
        to_keep    = images_sorted[:4]
        n_delete   = len(to_delete)

        affected.append(handle)
        del_ids    = [img['id'] for img in to_delete]
        keep_ids   = [img['id'] for img in to_keep]

        entry = {
            'handle':     handle,
            'product_id': pid,
            'total_before': total_images,
            'kept':       keep_ids,
            'deleted':    del_ids,
            'mode':       mode,
            'status':     None,
        }

        if not live:
            print('[{}/{}] {} — {} images found, would delete {} (DRY RUN)'.format(
                i, total_products, handle, total_images, n_delete))
            entry['status'] = 'DRY_RUN'
            log_entries.append(entry)
            time.sleep(0.5)
            continue

        # Live: delete each excess image
        del_success = 0
        del_errors  = 0
        for img in to_delete:
            ok = delete_image(pid, img['id'])
            if ok:
                del_success += 1
                deleted_count += 1
            else:
                del_errors  += 1
                error_count += 1
            time.sleep(0.25)  # tighter sleep inside the delete loop; outer 0.5 adds up

        status = 'DELETED' if del_errors == 0 else 'PARTIAL'
        entry['status']  = status
        entry['del_ok']  = del_success
        entry['del_err'] = del_errors
        log_entries.append(entry)

        print('[{}/{}] {} — {} images found, {} deleted{}'.format(
            i, total_products, handle, total_images, del_success,
            ' ({} errors)'.format(del_errors) if del_errors else ''))

        time.sleep(0.5)

    # Write audit log
    log_path = os.path.join(LOG_DIR, 'dedup-images-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':          mode,
            'timestamp':     TS,
            'total_checked': total_products,
            'affected':      len(affected),
            'deleted':       deleted_count,
            'errors':        error_count,
            'not_found':     not_found_count,
            'entries':       log_entries,
        }, f, indent=2)

    print()
    print('=== Summary: {} ==='.format(mode))
    print('  Products checked: {}'.format(total_products))
    print('  Affected (>4 imgs): {}'.format(len(affected)))
    if live:
        print('  Images deleted:   {}'.format(deleted_count))
        print('  Delete errors:    {}'.format(error_count))
    print('  Not found:        {}'.format(not_found_count))
    print('  Audit log:        {}'.format(log_path))

    if not live:
        print()
        print('[DRY RUN] No deletions performed. Re-run with --live to delete duplicate images.')


if __name__ == '__main__':
    main()
