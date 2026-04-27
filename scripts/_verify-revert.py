"""Helper: fetch image arrays for verification handles. Read-only.

Usage:
  python3 scripts/_verify-revert.py before
  python3 scripts/_verify-revert.py after
"""
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API   = 'https://{}/admin/api/2026-04'.format(STORE)

HANDLES = [
    'sonic-armchair-polypropylene-seat-back-6513',
    'table-desk-height-adjustable',
    'lateral-file-storage-cabinet-with-shelves',
]

label = sys.argv[1] if len(sys.argv) > 1 else 'snapshot'
out = {}
for handle in HANDLES:
    url = '{}/products.json?handle={}&fields=id,title,images&limit=1'.format(
        API, urllib.parse.quote(handle))
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    products = data.get('products', [])
    if not products:
        out[handle] = {'error': 'not found'}
        continue
    p = products[0]
    out[handle] = {
        'title':      p['title'],
        'image_count': len(p.get('images', [])),
        'images': [
            {'id': img['id'], 'position': img['position'], 'src': img['src'][:80]}
            for img in p.get('images', [])
        ],
    }

snap_path = os.path.join(ROOT, 'data', 'logs', '_verify-revert-{}.json'.format(label))
with open(snap_path, 'w') as f:
    json.dump(out, f, indent=2)

for handle, d in out.items():
    if 'error' in d:
        print('{}: {}'.format(handle, d['error']))
        continue
    print('\n{} ({} images)'.format(handle, d['image_count']))
    for img in d['images']:
        print('  pos {} id={} {}'.format(img['position'], img['id'], img['src']))
print('\nSnapshot: ' + snap_path)
