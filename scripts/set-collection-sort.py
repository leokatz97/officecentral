"""
Phase C — push velocity-ordered sort to every facet collection in Shopify.

Assumes the 20 facet collections have already been created in Shopify admin as
smart (automated) collections with handles like:
  type-chairs, type-desks, type-tables, type-storage, type-accessories,
  type-lounge, type-outdoor,
  room-private-office, room-boardroom, room-reception, room-open-plan,
  room-training-room, room-break-room, room-lounge,
  industry-health-centres, industry-schools, industry-government,
  industry-first-nations, industry-engineering, industry-non-profits.

For each recognized collection, fetches matching products from the proposed
CSV (filtered by the corresponding tag), sorts by sold_revenue descending,
and PUTs the manual order via the smart_collections/{id}/order endpoint.

Usage:
  python3 scripts/set-collection-sort.py               # dry run
  python3 scripts/set-collection-sort.py --live        # write to Shopify
  python3 scripts/set-collection-sort.py --handle=type-chairs --live
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

IN_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')
ID_FROM_URL = re.compile(r'/products/(\d+)')

# Industry facet dropped per Steve (2026-04-20) — 14 facet collections total.
FACET_HANDLES = {
    'type-chairs': 'type:chairs',
    'type-desks': 'type:desks',
    'type-tables': 'type:tables',
    'type-storage': 'type:storage',
    'type-accessories': 'type:accessories',
    'type-lounge': 'type:lounge',
    'type-outdoor': 'type:outdoor',
    'room-private-office': 'room:private-office',
    'room-boardroom': 'room:boardroom',
    'room-reception': 'room:reception',
    'room-open-plan': 'room:open-plan',
    'room-training-room': 'room:training-room',
    'room-break-room': 'room:break-room',
    'room-lounge': 'room:lounge',
}


def load_proposed() -> list:
    rows = []
    with open(IN_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            m = ID_FROM_URL.search(r['admin_url'])
            if not m:
                continue
            rows.append({
                'pid': int(m.group(1)),
                'title': r['title'],
                'type_tag': r['type_tag'],
                'room_tag': r['room_tag'],
                'industry_tag': r['industry_tag'],
                'sold_revenue': float(r['sold_revenue'] or 0),
            })
    return rows


def lookup_collection(handle: str) -> dict:
    qs = urllib.parse.urlencode({'handle': handle})
    url = f'{API}/smart_collections.json?{qs}'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return data.get('smart_collections', [{}])[0] if data.get('smart_collections') else {}


def set_manual_order(collection_id: int, product_ids: list) -> int:
    products_qs = '&'.join(f'products[]={pid}' for pid in product_ids)
    url = f'{API}/smart_collections/{collection_id}/order.json?sort_order=manual&{products_qs}'
    req = urllib.request.Request(url, headers=HEADERS, method='PUT', data=b'')
    with urllib.request.urlopen(req) as resp:
        return resp.status


def products_for_tag(rows: list, tag: str) -> list:
    matches = [r for r in rows if tag in (r['type_tag'], r['room_tag'])]
    matches.sort(key=lambda r: -r['sold_revenue'])
    return matches


def main() -> None:
    live = '--live' in sys.argv
    only_handle = None
    for arg in sys.argv[1:]:
        if arg.startswith('--handle='):
            only_handle = arg.split('=', 1)[1]

    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print()

    rows = load_proposed()
    handles = [only_handle] if only_handle else list(FACET_HANDLES.keys())

    for handle in handles:
        tag = FACET_HANDLES.get(handle)
        if not tag:
            print(f'[SKIP] unknown handle: {handle}')
            continue

        members = products_for_tag(rows, tag)
        if not members:
            print(f'[{handle}]  0 products (no products tagged {tag})')
            continue

        coll = lookup_collection(handle)
        if not coll:
            print(f'[{handle}]  COLLECTION NOT FOUND — create it in Shopify admin first')
            continue

        top = ', '.join(m['title'][:30] for m in members[:3])
        print(f'[{handle}]  {len(members)} products · top: {top}')

        if not live:
            continue

        try:
            status = set_manual_order(coll['id'], [m['pid'] for m in members])
            print(f'           → {status} manual order set')
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            print(f'           → PUT-ERR {e.code} {e.read().decode()[:200]}')

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
