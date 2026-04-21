"""
Phase B: Rename the 9 products whose handles contain non-ASCII characters
(™, ®). Create a 301 redirect from old handle -> new handle so no SEO
or customer links break.

Reads : data/sold-history-flagged.json (for bad_handle_products)
Writes: data/handle-rename-log.json
"""
import urllib.request
import urllib.error
import json
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = None
for line in open(os.path.join(ROOT, '.env')):
    if line.startswith('SHOPIFY_TOKEN='):
        TOKEN = line.strip().split('=', 1)[1].strip('"').strip("'")
        break

STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json',
}


def clean_handle(handle):
    """Strip non-ASCII, collapse runs of dashes, trim edges."""
    out = re.sub(r'[^a-z0-9\-]+', '', handle.lower())
    out = re.sub(r'-+', '-', out)
    out = out.strip('-')
    return out


def update_handle(product_id, new_handle):
    url = f'{API}/products/{product_id}.json'
    body = json.dumps({'product': {'id': product_id, 'handle': new_handle}}).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']['handle']


def create_redirect(old_path, new_path):
    """Create a 301 redirect /products/{old} -> /products/{new}."""
    url = f'{API}/redirects.json'
    body = json.dumps({
        'redirect': {
            'path': old_path,
            'target': new_path,
        }
    }).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())['redirect']
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        if 'already been taken' in msg.lower():
            return {'status': 'already_exists', 'path': old_path}
        raise


def main():
    src = os.path.join(ROOT, 'data', 'sold-history-flagged.json')
    with open(src) as f:
        data = json.load(f)

    items = data['bad_handle_products']
    print(f'Renaming {len(items)} products with bad handles...\n')

    log = []
    for p in items:
        pid = p['id']
        old_handle = p['handle']
        new_handle = clean_handle(old_handle)
        if new_handle == old_handle:
            print(f'  SKIP (already clean): {p["title"][:50]}')
            continue
        print(f'  {p["title"][:50]}')
        print(f'    old: {old_handle}')
        print(f'    new: {new_handle}')
        try:
            confirmed = update_handle(pid, new_handle)
            print(f'    ✓ renamed (shopify returned: {confirmed})')
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f'    ✗ rename failed: {e.code} {err}')
            log.append({'id': pid, 'old_handle': old_handle, 'new_handle': new_handle, 'rename_error': err})
            continue

        # Small gap to let Shopify propagate before creating the redirect
        time.sleep(0.3)

        # Create 301 redirect old -> new
        old_path = f'/products/{old_handle}'
        new_path = f'/products/{confirmed}'
        try:
            redirect = create_redirect(old_path, new_path)
            print(f'    ✓ redirect created: {old_path} -> {new_path}')
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f'    ✗ redirect failed: {e.code} {err}')
            redirect = {'error': err}

        log.append({
            'id': pid,
            'title': p['title'],
            'old_handle': old_handle,
            'new_handle': confirmed,
            'had_sold_history': p.get('orders', 0) > 0,
            'revenue': p.get('revenue', 0),
            'redirect': redirect,
        })
        time.sleep(0.3)

    out = os.path.join(ROOT, 'data', 'handle-rename-log.json')
    with open(out, 'w') as f:
        json.dump(log, f, indent=2, default=str)
    print(f'\nLog saved to {out}')
    print(f'Renamed {len([l for l in log if "rename_error" not in l])}/{len(items)}.')


if __name__ == '__main__':
    main()
