"""
One-off reorder: for each pilot product where the AI white-bg image was pushed
(originally at position 4 under the old mapping), move that image to position 2.

Shopify auto-shifts other images: old pos 2 → 3, old pos 3 → 4. Net effect:
  pos 1: original hero (untouched)
  pos 2: AI white-bg     (was pos 4)
  pos 3: AI Scene A      (was pos 2)   [if pushed]
  pos 4: AI Scene B      (was pos 3)   [if pushed]

Usage:
  python3 scripts/reorder-pilot-whitebg-first.py                   # DRY RUN
  python3 scripts/reorder-pilot-whitebg-first.py --live            # write
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

PUSH_CSV = os.path.join(ROOT, 'data', 'reports', 'shopify-img2img-pushed-2026-04-28.csv')
LOG_DIR  = os.path.join(ROOT, 'data', 'logs')
TS       = datetime.now().strftime('%Y%m%d-%H%M%S')


def update_position(product_id, image_id, new_position):
    url = '{}/products/{}/images/{}.json'.format(API, product_id, image_id)
    payload = json.dumps({'image': {'id': int(image_id), 'position': new_position}}).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())['image']


def main():
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'

    if not os.path.exists(PUSH_CSV):
        sys.exit('Push CSV not found: ' + PUSH_CSV)

    targets = []
    with open(PUSH_CSV, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') != 'PUSHED':
                continue
            if str(row.get('Image_Position')) != '4':
                continue
            targets.append({
                'handle':     row['Handle'],
                'product_id': row['Product_ID'],
                'image_id':   row['Shopify_Image_ID'],
                'cdn_url':    row.get('Shopify_CDN_URL', ''),
            })

    print('Mode:    ' + mode)
    print('Targets: {} product(s) — moving AI white-bg from pos 4 to pos 2'.format(len(targets)))
    for t in targets:
        print('  - {} (product {}, image {})'.format(t['handle'], t['product_id'], t['image_id']))
    print()

    if not live:
        print('[DRY RUN] No writes performed. Re-run with --live to apply.')
        return

    results = []
    for i, t in enumerate(targets, 1):
        print('[{}/{}] {}'.format(i, len(targets), t['handle']))
        try:
            img = update_position(t['product_id'], t['image_id'], 2)
            new_pos = img.get('position')
            print('  PUT pos=2 → reported new position: {}'.format(new_pos))
            results.append({**t, 'new_position': new_pos, 'status': 'OK'})
            time.sleep(0.5)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            print('  ERROR {}: {}'.format(e.code, msg))
            results.append({**t, 'new_position': '', 'status': 'ERROR_{}'.format(e.code), 'error': msg})

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, 'reorder-whitebg-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({'mode': mode, 'results': results}, f, indent=2)
    print()
    print('Done. Log: {}'.format(log_path))


if __name__ == '__main__':
    main()
