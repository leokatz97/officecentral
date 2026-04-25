"""
Push AI-generated product images to Shopify via the Product Images API.

Reads the latest data/reports/generated-images-*.csv (or --manifest=path),
fetches each product by handle, and POSTs the fal.ai image URL to Shopify.
Shopify fetches and permanently stores the image on their CDN.

Run WITHIN 24 HOURS of generate-product-images.py to ensure fal.ai URLs are valid.

Usage:
  python3 scripts/push-generated-images.py                                      # dry run
  python3 scripts/push-generated-images.py --live                               # push to Shopify
  python3 scripts/push-generated-images.py --manifest=data/reports/generated-images-2026-04-24.csv --live
  python3 scripts/push-generated-images.py --limit=5 --live                     # smoke test
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
TODAY   = datetime.now().strftime('%Y-%m-%d')
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
# Manifest loader
# ---------------------------------------------------------------------------
def load_manifest(path=None):
    if path:
        csv_path = path
    else:
        pattern = os.path.join(RPT_DIR, 'generated-images-*.csv')
        matches = sorted(glob.glob(pattern))
        if not matches:
            sys.exit('No generated-images-*.csv found in {}. Run generate-product-images.py first.'.format(RPT_DIR))
        csv_path = matches[-1]  # most recent by date string sort

    print('Loading manifest: ' + csv_path)
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') == 'OK':
                rows.append(row)
    print('Found {} OK rows to push.'.format(len(rows)))
    return rows


# ---------------------------------------------------------------------------
# Shopify API helpers
# ---------------------------------------------------------------------------
def fetch_product_id(handle, id_cache):
    """Return product ID string for handle, using cache to avoid duplicate fetches."""
    if handle in id_cache:
        return id_cache[handle]

    encoded = urllib.parse.quote(handle)
    url = '{}/products.json?handle={}&fields=id,title&limit=1'.format(API, encoded)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data     = json.loads(resp.read().decode())
            products = data.get('products', [])
            pid      = str(products[0]['id']) if products else None
    except urllib.error.HTTPError as e:
        print('  FETCH-ERR {}: {}'.format(e.code, e.read().decode()[:100]))
        pid = None
    except Exception as e:
        print('  FETCH-ERR: {}'.format(e))
        pid = None

    id_cache[handle] = pid
    time.sleep(0.5)
    return pid


def push_image(product_id, fal_url, position, alt_text, retries=3):
    """POST image to Shopify. Retries on socket/network errors. Returns image dict or raises."""
    url     = '{}/products/{}/images.json'.format(API, product_id)
    payload = json.dumps({
        'image': {
            'src':      fal_url,
            'position': int(position),
            'alt':      alt_text,
        }
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='POST')
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode())['image']
        except urllib.error.HTTPError:
            raise  # let caller handle HTTP errors (429, 4xx, 5xx)
        except Exception as e:
            last_err = e
            if attempt < retries:
                wait = attempt * 5
                print('  network error (attempt {}/{}): {} — retrying in {}s'.format(attempt, retries, e, wait))
                time.sleep(wait)
    raise last_err


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, limit, manifest_path = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)

    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RPT_DIR, exist_ok=True)

    rows = load_manifest(manifest_path)

    # Resume: skip (handle, position) pairs already successfully pushed today
    already_pushed = set()
    push_csv_pattern = os.path.join(RPT_DIR, 'shopify-images-pushed-{}.csv'.format(TODAY))
    existing_push_csvs = sorted(glob.glob(push_csv_pattern))
    if existing_push_csvs:
        resume_path = existing_push_csvs[-1]
        print('Resume: reading prior push log {}'.format(resume_path))
        with open(resume_path, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('Status') == 'PUSHED':
                    already_pushed.add((r['Handle'], r['Image_Position']))
        if already_pushed:
            before = len(rows)
            rows = [r for r in rows if (r['Handle'], r['Image_Position']) not in already_pushed]
            print('Skipping {} already-pushed images, {} remaining.\n'.format(before - len(rows), len(rows)))

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
        print('Limiting to first {} products.'.format(limit))

    # Group by handle so we do one ID lookup per product
    by_handle = {}
    for row in rows:
        h = row['Handle']
        by_handle.setdefault(h, []).append(row)

    total_products = len(by_handle)
    total_images   = len(rows)
    print('{} images for {} products to push.\n'.format(total_images, total_products))

    id_cache  = {}
    pushed    = []
    skipped   = []
    errors    = []
    result_rows = []

    for i, (handle, img_rows) in enumerate(by_handle.items(), 1):
        print('[{}/{}] {}'.format(i, total_products, handle))

        pid = fetch_product_id(handle, id_cache)
        if not pid:
            print('  SKIP - product not found in Shopify')
            for row in img_rows:
                skipped.append(handle)
                result_rows.append({
                    'Handle':          handle,
                    'Product_ID':      '',
                    'Image_Position':  row['Image_Position'],
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL': '',
                    'Alt_Text':        row['Alt_Text'],
                    'FAL_Source_URL':  row['FAL_URL'],
                    'Status':          'SKIP_NOT_FOUND',
                })
            continue

        for row in sorted(img_rows, key=lambda r: int(r['Image_Position'])):
            pos      = row['Image_Position']
            fal_url  = row['FAL_URL']
            alt_text = row['Alt_Text']

            if not live:
                print('  gen-{}: DRY RUN - would push to product {}'.format(pos, pid))
                result_rows.append({
                    'Handle':          handle,
                    'Product_ID':      pid,
                    'Image_Position':  pos,
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL': '',
                    'Alt_Text':        alt_text,
                    'FAL_Source_URL':  fal_url,
                    'Status':          'DRY_RUN',
                })
                continue

            try:
                img_data  = push_image(pid, fal_url, pos, alt_text)
                cdn_url   = img_data.get('src', '')
                img_id    = str(img_data.get('id', ''))
                pushed.append(handle)
                print('  gen-{}: PUSHED -> {}'.format(pos, cdn_url[:70]))
                result_rows.append({
                    'Handle':          handle,
                    'Product_ID':      pid,
                    'Image_Position':  pos,
                    'Shopify_Image_ID': img_id,
                    'Shopify_CDN_URL': cdn_url,
                    'Alt_Text':        alt_text,
                    'FAL_Source_URL':  fal_url,
                    'Status':          'PUSHED',
                })
                time.sleep(0.5)

            except urllib.error.HTTPError as e:
                code = e.code
                msg  = e.read().decode()[:300]
                if code == 429:
                    print('  gen-{}: 429 rate limit, sleeping 5s and retrying'.format(pos))
                    time.sleep(5)
                    try:
                        img_data = push_image(pid, fal_url, pos, alt_text)
                        cdn_url  = img_data.get('src', '')
                        img_id   = str(img_data.get('id', ''))
                        pushed.append(handle)
                        print('  gen-{}: PUSHED (retry) -> {}'.format(pos, cdn_url[:70]))
                        result_rows.append({
                            'Handle':          handle,
                            'Product_ID':      pid,
                            'Image_Position':  pos,
                            'Shopify_Image_ID': img_id,
                            'Shopify_CDN_URL': cdn_url,
                            'Alt_Text':        alt_text,
                            'FAL_Source_URL':  fal_url,
                            'Status':          'PUSHED',
                        })
                        time.sleep(0.5)
                        continue
                    except Exception as e2:
                        msg = str(e2)

                print('  gen-{}: ERROR {} - {}'.format(pos, code, msg[:150]))
                errors.append({'handle': handle, 'pos': pos, 'code': code, 'msg': msg[:300]})
                result_rows.append({
                    'Handle':          handle,
                    'Product_ID':      pid,
                    'Image_Position':  pos,
                    'Shopify_Image_ID': '',
                    'Shopify_CDN_URL': '',
                    'Alt_Text':        alt_text,
                    'FAL_Source_URL':  fal_url,
                    'Status':          'ERROR_{}'.format(code),
                })

    # Write results CSV — append to today's file so resume runs accumulate
    out_csv = os.path.join(RPT_DIR, 'shopify-images-pushed-{}.csv'.format(TODAY))
    fieldnames = ['Handle', 'Product_ID', 'Image_Position', 'Shopify_Image_ID',
                  'Shopify_CDN_URL', 'Alt_Text', 'FAL_Source_URL', 'Status']
    write_header = not os.path.exists(out_csv)
    with open(out_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(result_rows)

    # Write audit log
    log_path = os.path.join(LOG_DIR, 'push-images-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':             mode,
            'total_products':   total_products,
            'total_images':     total_images,
            'pushed':           len(pushed),
            'skipped':          len(skipped),
            'errors':           len(errors),
            'error_details':    errors,
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Products:    {}'.format(total_products))
    print('  Pushed:      {}'.format(len(pushed)))
    print('  Not found:   {}'.format(len(skipped)))
    print('  Errors:      {}'.format(len(errors)))
    print('  Results CSV: ' + out_csv)
    print('  Audit log:   ' + log_path)

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to push images.')


if __name__ == '__main__':
    main()
