#!/usr/bin/env python3
"""B4S4 Phase 6 — reverse the Session-3 brand-recovery miss on cluster-seating-2.
SKU MTY-B2 2424 is MityBilt, not Global. Set vendor=MityBilt, swap brand tag, snapshot + readback.
Usage: python3 scripts/revert-cluster-seating-to-mitybilt.py [--live]"""
import json, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = next((l.split('=',1)[1].strip().strip('"').strip("'")
              for l in (ROOT/'.env').read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
SHOP = 'office-central-online.myshopify.com'
REST = f'https://{SHOP}/admin/api/2024-10'
GQL = f'{REST}/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
PID = '9924896358713'
GID = f'gid://shopify/Product/{PID}'
NEW_VENDOR = 'MityBilt'

def gql(q, v=None):
    req = urllib.request.Request(GQL, data=json.dumps({'query':q,'variables':v or {}}).encode(), headers=HDR)
    out = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if 'errors' in out: raise RuntimeError(out['errors'])
    return out['data']

def rest(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(f'{REST}{path}', headers=HDR), timeout=30).read())

live = '--live' in sys.argv
ts = datetime.now().strftime('%Y%m%d-%H%M%S')
cur = rest(f'/products/{PID}.json')['product']
cur_tags = [t.strip() for t in cur['tags'].split(',') if t.strip()]
new_tags = ['brand:mitybilt' if t == 'brand:global-furniture-group' else t for t in cur_tags]
if 'brand:mitybilt' not in new_tags:
    new_tags.append('brand:mitybilt')

print(f"=== REVERT cluster-seating-2 -> MityBilt {'[LIVE]' if live else '[DRY]'} ===")
print(f"  vendor: {cur['vendor']!r} -> {NEW_VENDOR!r}")
print(f"  tags:   {cur_tags}\n       -> {new_tags}")

if not live:
    print("  DRY RUN — no writes."); sys.exit(0)

bdir = ROOT/'data/backups'; bdir.mkdir(exist_ok=True)
bpath = bdir/f'b4s4-cluster-seating-2-pre-{ts}.json'
bpath.write_text(json.dumps({'fetched':ts,'product':cur}, indent=2))
print(f"  backup -> {bpath}")

r = gql('''mutation($input: ProductInput!){productUpdate(input:$input){product{vendor tags} userErrors{field message}}}''',
        {'input': {'id': GID, 'vendor': NEW_VENDOR, 'tags': new_tags}})
errs = r['productUpdate']['userErrors']
if errs: raise RuntimeError(errs)
print("  productUpdate OK")

rb = gql('{ product(id: "%s"){ vendor tags } }' % GID)['product']
ok_v = rb['vendor'] == NEW_VENDOR
ok_t = set(rb['tags']) == set(new_tags)
print(f"  --- READBACK --- vendor {'OK' if ok_v else 'XX'} ({rb['vendor']!r}) | tags {'OK' if ok_t else 'XX'} ({rb['tags']})")
print(f"  READBACK: {'ALL MATCH' if (ok_v and ok_t) else 'MISMATCH — INVESTIGATE'}")
sys.exit(0 if (ok_v and ok_t) else 2)
