"""
Phase D — rebuild the main nav menu via GraphQL Admin API.

Fetches the existing main-menu, backs it up to data/backups/main-menu-<ts>.json,
then replaces the menu with:

  Shop by Room  (submenu → 6 room collections)
  Shop by Type  (submenu → 7 type collections)
  <preserved non-collection top-level items, e.g. About, Contact>

Industry facet intentionally skipped — Tier 5 landing pages don't exist yet.

Requires the Shopify token to have write_online_store_navigation scope.

Usage:
  python3 scripts/update-main-menu.py              # dry run
  python3 scripts/update-main-menu.py --live       # write to Shopify
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
GRAPHQL = f'https://{STORE}/admin/api/2026-04/graphql.json'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

BACKUP_DIR = os.path.join(ROOT, 'data', 'backups')

SHOP_BY_ROOM = [
    ('Private Office', 'room-private-office'),
    ('Boardroom',      'room-boardroom'),
    ('Reception',      'room-reception'),
    ('Open Plan',      'room-open-plan'),
    ('Training Room',  'room-training-room'),
    ('Lounge',         'room-lounge'),
]

SHOP_BY_TYPE = [
    ('Chairs',          'type-chairs'),
    ('Desks',           'type-desks'),
    ('Tables',          'type-tables'),
    ('Storage',         'type-storage'),
    ('Accessories',     'type-accessories'),
    ('Lounge Seating',  'type-lounge'),
    ('Outdoor',         'type-outdoor'),
]

ALL_FACET_HANDLES = [h for _, h in SHOP_BY_ROOM] + [h for _, h in SHOP_BY_TYPE]


def gql(query: str, variables: dict = None) -> dict:
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GRAPHQL, data=payload, headers=HEADERS,
                                 method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{e.code}: {e.read().decode()[:400]}')
    if data.get('errors'):
        raise RuntimeError(f'GraphQL errors: {json.dumps(data["errors"], indent=2)}')
    return data['data']


def fetch_collection_gids() -> dict:
    """Query all 14 collections by handle in one call, return {handle: gid}."""
    aliases = '\n'.join(
        f'  c{i}: collectionByHandle(handle: "{h}") {{ id handle title }}'
        for i, h in enumerate(ALL_FACET_HANDLES)
    )
    query = '{\n' + aliases + '\n}'
    data = gql(query)
    result = {}
    for i, handle in enumerate(ALL_FACET_HANDLES):
        node = data.get(f'c{i}')
        if not node:
            raise RuntimeError(f'Collection not found: {handle}')
        result[handle] = node['id']
    return result


TARGET_MENU_HANDLE = 'main-menu-2'


def fetch_main_menu() -> dict:
    # 3-level deep so we don't drop nested sub-items (Shopify supports up to 3 levels)
    query = '''
    {
      menus(first: 20) {
        edges {
          node {
            id
            handle
            title
            items {
              id title type url resourceId tags
              items {
                id title type url resourceId tags
                items {
                  id title type url resourceId tags
                }
              }
            }
          }
        }
      }
    }
    '''
    data = gql(query)
    for edge in data['menus']['edges']:
        node = edge['node']
        if node['handle'] == TARGET_MENU_HANDLE:
            return node
    raise RuntimeError(f'{TARGET_MENU_HANDLE} not found on this store')


def item_to_input(item: dict) -> dict:
    """Convert a fetched MenuItem into a MenuItemUpdateInput (no id = create new)."""
    out = {
        'title': item['title'],
        'type': item['type'],
    }
    if item.get('url'):
        out['url'] = item['url']
    if item.get('resourceId'):
        out['resourceId'] = item['resourceId']
    if item.get('tags'):
        out['tags'] = item['tags']
    if item.get('items'):
        out['items'] = [item_to_input(child) for child in item['items']]
    return out


def build_submenu(entries: list, gids: dict) -> list:
    return [
        {
            'title': title,
            'type': 'COLLECTION',
            'resourceId': gids[handle],
        }
        for title, handle in entries
    ]


def is_facet_collection_item(item: dict) -> bool:
    """True if item links to one of our 14 facet collections — we'll replace these."""
    if item.get('type') == 'COLLECTION':
        for gid in item.get('_our_facet_gids', set()):
            if item.get('resourceId') == gid:
                return True
    url = (item.get('url') or '').lower()
    return any(f'/collections/{h}' in url for h in ALL_FACET_HANDLES)


def main() -> None:
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print()

    print('Fetching collection GIDs...')
    gids = fetch_collection_gids()
    print(f'  Found {len(gids)} collections')

    print('Fetching main menu...')
    menu = fetch_main_menu()
    print(f'  Menu id: {menu["id"]}')
    print(f'  Title:   {menu["title"]}')
    print(f'  Current top-level items: {len(menu["items"])}')
    for item in menu['items']:
        sub = f' ({len(item["items"])} sub-items)' if item.get('items') else ''
        print(f'    · {item["title"]:<30} [{item["type"]}]{sub}')
    print()

    # Back up existing menu before any change
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'main-menu-{ts}.json')
    with open(backup_path, 'w') as f:
        json.dump(menu, f, indent=2)
    print(f'Backup saved to {backup_path}')
    print()

    # Option B: additive — preserve ALL existing top-level items, just skip
    # "Shop by Room" / "Shop by Type" so re-runs don't duplicate.
    preserved = []
    skipped_titles = {'shop by room', 'shop by type'}
    for item in menu['items']:
        if item['title'].strip().lower() in skipped_titles:
            continue
        preserved.append(item)

    print(f'Preserving {len(preserved)} existing top-level items:')
    for p in preserved:
        sub_count = len(p.get('items') or [])
        sub = f' ({sub_count} subs)' if sub_count else ''
        print(f'  · {p["title"]:<38} [{p["type"]}]{sub}')
    print()

    # Prepend new facet items so they appear first in the nav.
    new_items = [
        {
            'title': 'Shop by Room',
            'type': 'COLLECTIONS',
            'items': build_submenu(SHOP_BY_ROOM, gids),
        },
        {
            'title': 'Shop by Type',
            'type': 'COLLECTIONS',
            'items': build_submenu(SHOP_BY_TYPE, gids),
        },
    ] + [item_to_input(p) for p in preserved]

    print('New menu structure:')
    for item in new_items:
        sub_count = len(item.get('items', []))
        sub = f' ({sub_count} sub-items)' if sub_count else ''
        print(f'  · {item["title"]:<30} [{item["type"]}]{sub}')
        for child in item.get('items', []):
            print(f'      - {child["title"]}')
    print()

    if not live:
        print('[DRY RUN] No writes performed. Re-run with --live to apply.')
        return

    print('Pushing menu update...')
    mutation = '''
    mutation($id: ID!, $title: String!, $handle: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, handle: $handle, items: $items) {
        menu { id handle title items { title } }
        userErrors { field message code }
      }
    }
    '''
    result = gql(mutation, {
        'id': menu['id'],
        'title': menu['title'],
        'handle': menu['handle'],
        'items': new_items,
    })
    update = result.get('menuUpdate', {})
    errors = update.get('userErrors', [])
    if errors:
        print('User errors:')
        for e in errors:
            print(f'  {e}')
        sys.exit(1)
    items = update['menu'].get('items', [])
    print(f'Updated: {update["menu"]["title"]} · {len(items)} top-level items')
    for it in items:
        print(f'  · {it["title"]}')


if __name__ == '__main__':
    main()
