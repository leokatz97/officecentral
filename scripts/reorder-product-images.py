"""
Reorder product images so the AI-generated "Studio White" full-product shot is position 1.

Uses the existing push manifest (shopify-images-pushed-*.csv) to identify which Shopify
image ID corresponds to the clean white-background full-product shot (Image_Position == 2).
Fetches current image order from Shopify, then PUTs the reordered list if needed.

Zero AI API calls — we already know which images are full-product shots.

Usage:
  python3 scripts/reorder-product-images.py                      # dry run, all products
  python3 scripts/reorder-product-images.py --live               # apply to Shopify
  python3 scripts/reorder-product-images.py --limit=5            # inspect first 5
  python3 scripts/reorder-product-images.py --limit=5 --live     # smoke test
  python3 scripts/reorder-product-images.py --manifest=data/reports/shopify-images-pushed-2026-04-25.csv --live
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

# Search for .env walking up from ROOT (worktrees don't always have their own)
def find_env():
    search = ROOT
    for _ in range(4):
        candidate = os.path.join(search, '.env')
        if os.path.exists(candidate):
            return candidate
        search = os.path.dirname(search)
    return None

env_path = find_env()
if not env_path:
    sys.exit('ERROR: .env not found (searched up from {})'.format(ROOT))

env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

TOKEN = env.get('SHOPIFY_TOKEN') or os.environ.get('SHOPIFY_TOKEN', '')
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')

if not TOKEN:
    sys.exit('ERROR: SHOPIFY_TOKEN not found in .env')

API     = 'https://{}/admin/api/2026-04'.format(STORE)
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type':           'application/json',
}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
TODAY   = datetime.now().strftime('%Y-%m-%d')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

os.makedirs(RPT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


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
# Load push manifest — find the gen-2 (Studio White) image ID per product
# ---------------------------------------------------------------------------
def load_studio_white_images(manifest_path=None):
    """
    Returns dict: {handle: {'product_id': str, 'image_id': str}}
    Only includes products where Image_Position==2 and Status==PUSHED.
    """
    if manifest_path:
        csv_path = manifest_path
    else:
        pattern = os.path.join(RPT_DIR, 'shopify-images-pushed-*.csv')
        matches = sorted(glob.glob(pattern))
        if not matches:
            sys.exit('No shopify-images-pushed-*.csv found in {}. Run push-generated-images.py first.'.format(RPT_DIR))
        csv_path = matches[-1]

    print('Loading manifest: ' + csv_path)
    products = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') == 'PUSHED' and row.get('Image_Position') == '2':
                handle = row['Handle'].strip()
                products[handle] = {
                    'product_id': row['Product_ID'].strip(),
                    'image_id':   row['Shopify_Image_ID'].strip(),
                }
    print('Found {} products with a PUSHED Studio White image (position 2).\n'.format(len(products)))
    return products


# ---------------------------------------------------------------------------
# Shopify API helpers
# ---------------------------------------------------------------------------
def fetch_images(product_id):
    url = '{}/products/{}/images.json?fields=id,position&limit=250'.format(API, product_id)
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode()).get('images', [])
    except urllib.error.HTTPError as e:
        print('  IMG-FETCH-ERR {}: {}'.format(e.code, e.read().decode()[:100]))
        return None
    except Exception as e:
        print('  IMG-FETCH-ERR: {}'.format(e))
        return None


def reorder_images(product_id, ordered_image_ids):
    """PUT product with images in the desired order."""
    payload = json.dumps({
        'product': {
            'id':     int(product_id),
            'images': [{'id': int(iid)} for iid in ordered_image_ids],
        }
    }).encode()
    req = urllib.request.Request(
        '{}/products/{}.json'.format(API, product_id),
        data=payload, headers=HEADERS, method='PUT'
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, limit, manifest_path = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('=== Reorder Product Images — {} ===\n'.format(mode))

    studio_white = load_studio_white_images(manifest_path)
    handles      = list(studio_white.keys())

    if limit:
        handles = handles[:limit]
        print('Limiting to first {} products.\n'.format(limit))

    total      = len(handles)
    reordered  = 0
    already_ok = 0
    missing    = 0
    errors     = 0
    result_rows = []

    for i, handle in enumerate(handles, 1):
        info       = studio_white[handle]
        product_id = info['product_id']
        target_id  = info['image_id']  # the Studio White image ID we want at position 1

        print('[{}/{}] {}'.format(i, total, handle))

        images = fetch_images(product_id)
        if images is None:
            print('  ERROR fetching images')
            errors += 1
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'ERROR', 'Status': 'FETCH_ERROR',
                'Target_Image_ID': target_id, 'Orig_Position': '',
            })
            time.sleep(0.5)
            continue

        # Find our target image in the current list
        image_ids    = [str(img['id']) for img in sorted(images, key=lambda x: x['position'])]
        target_id_s  = str(target_id)

        if target_id_s not in image_ids:
            print('  IMAGE_MISSING — target image ID {} not in product'.format(target_id_s))
            missing += 1
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'IMAGE_MISSING', 'Status': 'IMAGE_MISSING',
                'Target_Image_ID': target_id, 'Orig_Position': '',
            })
            time.sleep(0.5)
            continue

        current_first = image_ids[0]
        orig_position = image_ids.index(target_id_s) + 1  # 1-indexed

        if current_first == target_id_s:
            print('  ALREADY_OK — Studio White already at position 1')
            already_ok += 1
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'ALREADY_OK', 'Status': 'ALREADY_OK',
                'Target_Image_ID': target_id, 'Orig_Position': orig_position,
            })
            time.sleep(0.5)
            continue

        # Build reordered list: target first, then rest in current relative order
        ordered = [target_id_s] + [iid for iid in image_ids if iid != target_id_s]
        print('  REORDER — moving image {} from pos {} to pos 1'.format(target_id_s, orig_position))

        if not live:
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'REORDER', 'Status': 'DRY_RUN',
                'Target_Image_ID': target_id, 'Orig_Position': orig_position,
            })
            time.sleep(0.5)
            continue

        try:
            reorder_images(product_id, ordered)
            reordered += 1
            print('  DONE')
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'REORDER', 'Status': 'REORDERED',
                'Target_Image_ID': target_id, 'Orig_Position': orig_position,
            })
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            print('  ERROR {}: {}'.format(e.code, msg))
            errors += 1
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'REORDER', 'Status': 'ERROR_{}'.format(e.code),
                'Target_Image_ID': target_id, 'Orig_Position': orig_position,
            })
        except Exception as e:
            print('  ERROR: {}'.format(e))
            errors += 1
            result_rows.append({
                'Handle': handle, 'Product_ID': product_id,
                'Action': 'REORDER', 'Status': 'ERROR',
                'Target_Image_ID': target_id, 'Orig_Position': orig_position,
            })

        time.sleep(0.5)

    # Write results CSV
    out_csv    = os.path.join(RPT_DIR, 'reorder-images-{}.csv'.format(TODAY))
    fieldnames = ['Handle', 'Product_ID', 'Action', 'Status', 'Target_Image_ID', 'Orig_Position']
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_rows)

    # Write audit log
    would_reorder = sum(1 for r in result_rows if r['Action'] == 'REORDER')
    log_path = os.path.join(LOG_DIR, 'reorder-images-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':         mode,
            'timestamp':    TS,
            'total':        total,
            'reordered':    reordered,
            'already_ok':   already_ok,
            'image_missing': missing,
            'errors':       errors,
        }, f, indent=2)

    print()
    print('=== Summary: {} ==='.format(mode))
    print('  Products processed: {}'.format(total))
    print('  Already correct:    {}'.format(already_ok))
    if live:
        print('  Reordered:          {}'.format(reordered))
    else:
        print('  Would reorder:      {}'.format(would_reorder))
    print('  Image missing:      {}'.format(missing))
    print('  Errors:             {}'.format(errors))
    print('  Results CSV:        {}'.format(out_csv))
    print('  Audit log:          {}'.format(log_path))

    if not live:
        print()
        print('[DRY RUN] No changes made. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
