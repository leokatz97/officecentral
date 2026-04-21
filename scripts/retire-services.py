"""
Phase C: Unpublish service pseudo-products from storefront.
Keeps the product records intact (so historical orders still render) but
sets published_at=null so they disappear from storefront, search, and collections.

Reads : data/sold-history-flagged.json (services_sold + services_never_sold)
Writes: data/retire-services-log.json

PROTECTED: Delivery and Installation are kept alive by the Phase D add-on
pattern (carrier service + cart toggle), so we unpublish them here too but
the Phase D SKUs continue to be added programmatically.
"""
import urllib.request
import urllib.error
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = None
for line in open(os.path.join(ROOT, '.env')):
    if line.startswith('SHOPIFY_TOKEN='):
        TOKEN = line.strip().split('=', 1)[1].strip('"').strip("'")
        break

STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def unpublish(product_id):
    """Set published_at = null to remove from all online channels."""
    url = f'{API}/products/{product_id}.json'
    body = json.dumps({'product': {'id': product_id, 'published_at': None}}).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product']


def main():
    src = os.path.join(ROOT, 'data', 'sold-history-flagged.json')
    with open(src) as f:
        data = json.load(f)

    # Combine both buckets — Leo's rule: unpublish all service pseudo-products
    items = data['services_sold'] + data['services_never_sold']
    print(f'Unpublishing {len(items)} service pseudo-products...\n')

    log = []
    for p in items:
        pid = p['id']
        title = p['title'][:55]
        orders = p.get('orders', 0)
        print(f'  [{"sold" if orders else "never sold":>10}] {title}')
        try:
            result = unpublish(pid)
            published_at = result.get('published_at')
            status_now = result.get('status')
            print(f'    ✓ unpublished (status={status_now}, published_at={published_at})')
            log.append({
                'id': pid,
                'title': p['title'],
                'had_sold_history': orders > 0,
                'orders': orders,
                'revenue': p.get('revenue', 0),
                'prior_status': p.get('status'),
                'new_published_at': published_at,
                'new_status': status_now,
                'success': True,
            })
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f'    ✗ FAILED: {e.code} {err[:200]}')
            log.append({
                'id': pid, 'title': p['title'],
                'success': False, 'error': err,
            })
        time.sleep(0.3)

    out = os.path.join(ROOT, 'data', 'retire-services-log.json')
    with open(out, 'w') as f:
        json.dump(log, f, indent=2, default=str)
    print(f'\nLog saved to {out}')
    success = len([l for l in log if l.get('success')])
    print(f'Unpublished {success}/{len(items)}.')


if __name__ == '__main__':
    main()
