"""
Phase C step 1 — create the 14 facet smart collections in Shopify.

Each collection is created with:
  - title:  human-readable name
  - handle: exact handle the set-collection-sort.py script looks up
  - rules:  single rule — product tag equals the facet tag
  - sort_order: manual (set-collection-sort.py pushes the velocity order next)

Idempotent: if a collection with the same handle already exists, it's skipped.

Usage:
  python3 scripts/create-collections.py           # dry run
  python3 scripts/create-collections.py --live    # POST to Shopify
"""
import json
import os
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


COLLECTIONS = [
    ('Chairs',          'type-chairs',          'type:chairs'),
    ('Desks',           'type-desks',           'type:desks'),
    ('Tables',          'type-tables',          'type:tables'),
    ('Storage',         'type-storage',         'type:storage'),
    ('Accessories',     'type-accessories',     'type:accessories'),
    ('Lounge Seating',  'type-lounge',          'type:lounge'),
    ('Outdoor',         'type-outdoor',         'type:outdoor'),
    ('Private Office',  'room-private-office',  'room:private-office'),
    ('Boardroom',       'room-boardroom',       'room:boardroom'),
    ('Reception',       'room-reception',       'room:reception'),
    ('Open Plan',       'room-open-plan',       'room:open-plan'),
    ('Training Room',   'room-training-room',   'room:training-room'),
    ('Break Room',      'room-break-room',      'room:break-room'),
    ('Lounge',          'room-lounge',          'room:lounge'),
]


def lookup(handle: str) -> dict:
    qs = urllib.parse.urlencode({'handle': handle})
    url = f'{API}/smart_collections.json?{qs}'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    colls = data.get('smart_collections', [])
    return colls[0] if colls else {}


def create(title: str, handle: str, tag: str) -> dict:
    payload = json.dumps({
        'smart_collection': {
            'title': title,
            'handle': handle,
            'sort_order': 'manual',
            'rules': [{
                'column': 'tag',
                'relation': 'equals',
                'condition': tag,
            }],
            'disjunctive': False,
        }
    }).encode()
    url = f'{API}/smart_collections.json'
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='POST')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['smart_collection']


def main() -> None:
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print()

    created = 0
    skipped = 0
    errors = []

    for title, handle, tag in COLLECTIONS:
        existing = lookup(handle)
        if existing:
            print(f'[SKIP] {handle:<22} already exists (id={existing.get("id")})')
            skipped += 1
            continue

        if not live:
            print(f'[WOULD-CREATE] {handle:<22} title="{title}" tag="{tag}"')
            continue

        try:
            c = create(title, handle, tag)
            print(f'[CREATED] {handle:<22} id={c["id"]}  title="{c["title"]}"')
            created += 1
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:300]}'
            print(f'[ERR]     {handle:<22} {msg}')
            errors.append({'handle': handle, 'error': msg})

    print()
    print(f'Summary: {mode}')
    print(f'  Created:  {created}')
    print(f'  Skipped:  {skipped}')
    print(f'  Errors:   {len(errors)}')

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
