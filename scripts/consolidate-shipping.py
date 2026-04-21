"""
Consolidate 10 scattered delivery/installation SKUs into 2 clean products:
    - "Delivery" (with price variants + combo variants for Delivery+Installation)
    - "Installation" (with variants for Standard and Chairs)

Old SKUs get archived (not deleted — preserves order history).

Dry-run by default; pass --confirm.
"""
import urllib.request
import urllib.error
import json
import re
import sys
import time

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

# Variant definitions — option name "Type" for clarity in checkout
DELIVERY_VARIANTS = [
    {'option1': 'Standard Delivery', 'price': '35.00'},
    {'option1': 'Local Delivery', 'price': '65.00'},
    {'option1': 'Regional Delivery', 'price': '75.00'},
    {'option1': 'Extended Delivery', 'price': '125.00'},
    {'option1': 'Tailgate / Liftgate Delivery', 'price': '300.00'},
    {'option1': 'Delivery + Installation (Basic)', 'price': '50.00'},
    {'option1': 'Delivery + Installation (Standard)', 'price': '175.00'},
    {'option1': 'Delivery + Installation (White-Glove)', 'price': '250.00'},
]

INSTALLATION_VARIANTS = [
    {'option1': 'Standard Installation', 'price': '0.00'},
    {'option1': 'Chair Installation', 'price': '15.00'},
]

DELIVERY_BODY = (
    '<p>Delivery service for Office Central / Brant Business Interiors orders. Select the '
    'option that matches your destination and delivery needs. Our team confirms scheduling '
    'and access requirements after your order is placed.</p>'
    '<ul>'
    '<li><strong>Standard / Local / Regional / Extended</strong> — curbside or dock delivery at the listed rate</li>'
    '<li><strong>Tailgate / Liftgate</strong> — for sites without a loading dock</li>'
    '<li><strong>Delivery + Installation bundles</strong> — combine shipping and on-site setup in one line</li>'
    '</ul>'
    '<p>Not sure which tier applies? Call <strong>1-800-835-9565</strong> and we\'ll advise.</p>'
)

INSTALLATION_BODY = (
    '<p>On-site installation service for furniture delivered by Office Central. Pick the '
    'option that matches what you ordered — a member of our team will confirm the appointment '
    'after checkout.</p>'
    '<ul>'
    '<li><strong>Standard Installation</strong> — desks, tables, storage, and systems furniture</li>'
    '<li><strong>Chair Installation</strong> — seating assembly billed per chair</li>'
    '</ul>'
    '<p>For large projects or complex spaces, call <strong>1-800-835-9565</strong> for a quote.</p>'
)


def api_call(method, path, body=None, attempt=0):
    data = json.dumps(body).encode() if body is not None else None
    url = f'{API}/{path}'
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            txt = resp.read().decode()
            return resp.status, (json.loads(txt) if txt else None)
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_call(method, path, body, attempt + 1)
        return e.code, {'error': e.read().decode()}


def create_product(title, body_html, variants, product_type, tags):
    payload = {
        'product': {
            'title': title,
            'body_html': body_html,
            'product_type': product_type,
            'vendor': 'Office Central & Brant Business Interiors',
            'tags': tags,
            'status': 'active',
            'options': [{'name': 'Type'}],
            'variants': [
                {**v, 'inventory_management': None, 'requires_shipping': False, 'taxable': True}
                for v in variants
            ],
        }
    }
    return api_call('POST', 'products.json', payload)


def archive_product(pid):
    return api_call('PUT', f'products/{pid}.json', {'product': {'id': pid, 'status': 'archived'}})


def main():
    confirm = '--confirm' in sys.argv
    with open('junk-inspection.json') as f:
        report = json.load(f)
    service_skus = [r for r in report if r['suggested_action'] == 'service_sku_review']

    print(f'Old service SKUs to archive: {len(service_skus)}')
    for r in service_skus:
        print(f'  {r["id"]:18}  {r["title"][:50]:50}  price={r["price_range"]}')

    print(f'\nNew "Delivery" product with {len(DELIVERY_VARIANTS)} variants:')
    for v in DELIVERY_VARIANTS:
        print(f'  {v["option1"]:45}  ${v["price"]}')
    print(f'\nNew "Installation" product with {len(INSTALLATION_VARIANTS)} variants:')
    for v in INSTALLATION_VARIANTS:
        print(f'  {v["option1"]:45}  ${v["price"]}')

    if not confirm:
        print(f'\nDRY RUN. Pass --confirm to create 2 new products + archive {len(service_skus)} old.')
        return

    print('\nCreating Delivery product...')
    status, resp = create_product(
        'Delivery', DELIVERY_BODY, DELIVERY_VARIANTS,
        product_type='Service', tags='service, delivery, internal',
    )
    if status not in (200, 201):
        print(f'  FAIL {status}: {resp}')
        return
    delivery_id = resp['product']['id']
    print(f'  OK  id={delivery_id}')
    time.sleep(0.55)

    print('Creating Installation product...')
    status, resp = create_product(
        'Installation', INSTALLATION_BODY, INSTALLATION_VARIANTS,
        product_type='Service', tags='service, installation, internal',
    )
    if status not in (200, 201):
        print(f'  FAIL {status}: {resp}')
        return
    install_id = resp['product']['id']
    print(f'  OK  id={install_id}')
    time.sleep(0.55)

    print(f'\nArchiving {len(service_skus)} old SKUs...')
    archived = []
    for r in service_skus:
        status, resp = archive_product(r['id'])
        ok = status in (200, 201)
        archived.append({'id': r['id'], 'title': r['title'], 'status': status, 'ok': ok})
        print(f'  [{"OK" if ok else f"FAIL {status}"}] {r["title"][:55]}')
        time.sleep(0.55)

    succeeded = sum(1 for x in archived if x['ok'])
    with open('consolidate-shipping-log.json', 'w') as f:
        json.dump({
            'new_delivery_id': delivery_id,
            'new_installation_id': install_id,
            'archived_attempted': len(archived),
            'archived_succeeded': succeeded,
            'archived': archived,
        }, f, indent=2)
    print(f'\nDone. Created 2 products, archived {succeeded}/{len(archived)}.')
    print(f'Delivery:     https://admin.shopify.com/store/office-central-online/products/{delivery_id}')
    print(f'Installation: https://admin.shopify.com/store/office-central-online/products/{install_id}')


if __name__ == '__main__':
    main()
