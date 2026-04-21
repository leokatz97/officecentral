"""
Phase X3 — delete the "Other Industries" top-level item from main-menu-2.

Fetches main-menu-2, backs it up, filters out any top-level item whose title
(case-insensitive) matches the target, and pushes the rest back.

Usage:
  python3 scripts/delete-menu-item.py                         # dry run, default target
  python3 scripts/delete-menu-item.py --live
  python3 scripts/delete-menu-item.py --title="Some Item"     # custom target
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
TARGET_MENU_HANDLE = 'main-menu-2'


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


def fetch_menu() -> dict:
    query = '''
    {
      menus(first: 20) {
        edges {
          node {
            id handle title
            items {
              id title type url resourceId tags
              items {
                id title type url resourceId tags
                items { id title type url resourceId tags }
              }
            }
          }
        }
      }
    }
    '''
    data = gql(query)
    for edge in data['menus']['edges']:
        if edge['node']['handle'] == TARGET_MENU_HANDLE:
            return edge['node']
    raise RuntimeError(f'{TARGET_MENU_HANDLE} not found')


def item_to_input(item: dict) -> dict:
    out = {'title': item['title'], 'type': item['type']}
    if item.get('url'):
        out['url'] = item['url']
    if item.get('resourceId'):
        out['resourceId'] = item['resourceId']
    if item.get('tags'):
        out['tags'] = item['tags']
    if item.get('items'):
        out['items'] = [item_to_input(c) for c in item['items']]
    return out


def main() -> None:
    live = '--live' in sys.argv
    target = 'Other Industries'
    for arg in sys.argv[1:]:
        if arg.startswith('--title='):
            target = arg.split('=', 1)[1]

    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print(f'Target to delete: "{target}"')
    print()

    menu = fetch_menu()
    print(f'Menu: {menu["title"]} (id={menu["id"]})')
    print(f'Current top-level: {len(menu["items"])} items')
    for it in menu['items']:
        print(f'  · {it["title"]}')
    print()

    target_lower = target.strip().lower()
    new_items = [it for it in menu['items']
                 if it['title'].strip().lower() != target_lower]

    removed = len(menu['items']) - len(new_items)
    if removed == 0:
        print(f'No item titled "{target}" found — nothing to do.')
        return

    print(f'Will remove {removed} item(s). New top-level structure:')
    for it in new_items:
        print(f'  · {it["title"]}')
    print()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'main-menu-{ts}.json')
    with open(backup_path, 'w') as f:
        json.dump(menu, f, indent=2)
    print(f'Backup: {backup_path}')
    print()

    if not live:
        print('[DRY RUN] No writes. Re-run with --live to apply.')
        return

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
        'items': [item_to_input(it) for it in new_items],
    })
    errs = result.get('menuUpdate', {}).get('userErrors', [])
    if errs:
        print('User errors:')
        for e in errs:
            print(f'  {e}')
        sys.exit(1)

    updated = result['menuUpdate']['menu']
    print(f'Updated: {updated["title"]} · {len(updated["items"])} items')
    for it in updated['items']:
        print(f'  · {it["title"]}')


if __name__ == '__main__':
    main()
