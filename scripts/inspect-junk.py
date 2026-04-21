"""
Inspect the 26 'empty' products flagged in audit-report.json.
Pull full details (price, variants, inventory, tags, status) and
check whether they've received any orders in the last 90 days.
Output: junk-inspection.json with a suggested action for each.
"""
import urllib.request
import urllib.parse
import json
import re
import sys
from datetime import datetime, timezone, timedelta

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


def get(path):
    url = f'{API}/{path}' if not path.startswith('http') else path
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        link = resp.headers.get('Link', '')
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        return json.loads(resp.read().decode()), (m.group(1) if m else None)


def fetch_all_products():
    products = []
    url = f'{API}/products.json?limit=250'
    while url:
        data, next_url = get(url)
        products.extend(data['products'])
        print(f'  products fetched: {len(products)}')
        url = next_url
    return products


def fetch_recent_orders(days=90):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    orders = []
    url = f'{API}/orders.json?status=any&limit=250&created_at_min={urllib.parse.quote(since)}&fields=id,created_at,line_items'
    while url:
        data, next_url = get(url)
        orders.extend(data['orders'])
        print(f'  orders fetched: {len(orders)}')
        url = next_url
    return orders


def main():
    with open('audit-report.json') as f:
        audit = json.load(f)
    empty_titles = set(audit['empty_products'])
    print(f'Targeting {len(empty_titles)} empty-description products\n')

    print('Fetching all products...')
    all_products = fetch_all_products()
    matches = [p for p in all_products if p['title'] in empty_titles]
    print(f'\nMatched {len(matches)} of {len(empty_titles)} expected\n')

    missing = empty_titles - {p['title'] for p in matches}
    if missing:
        print('Missing (title mismatch?):')
        for t in sorted(missing):
            print(f'  - {t}')
        print()

    print('Fetching orders from last 90 days...')
    orders = fetch_recent_orders(90)
    print(f'  total orders: {len(orders)}\n')

    variant_sales = {}
    product_sales = {}
    for o in orders:
        for li in o.get('line_items', []):
            vid = li.get('variant_id')
            pid = li.get('product_id')
            qty = li.get('quantity', 0)
            if vid:
                variant_sales[vid] = variant_sales.get(vid, 0) + qty
            if pid:
                product_sales[pid] = product_sales.get(pid, 0) + qty

    report = []
    for p in matches:
        variants = p.get('variants', [])
        has_inventory = any((v.get('inventory_quantity') or 0) > 0 for v in variants)
        prices = [float(v.get('price') or 0) for v in variants]
        total_orders_90d = product_sales.get(p['id'], 0)
        variant_orders = sum(variant_sales.get(v['id'], 0) for v in variants)

        title = p['title']
        tl = title.lower()
        if re.search(r'delivery|installation|install\b', tl) or 'installation' in tl:
            suggested = 'service_sku_review'
        elif tl in ('colour', 'colour choices', 'caster options', 'chair frame colour options',
                    'dummy variants colors', 'radio buttons', 'please select a finish',
                    'feet', 'follower block', 'coming soon'):
            suggested = 'delete'
        elif 'coming soon' in tl:
            suggested = 'delete'
        elif total_orders_90d > 0 or variant_orders > 0:
            suggested = 'keep_had_sales'
        elif p.get('status') == 'draft':
            suggested = 'delete_was_draft'
        else:
            suggested = 'review'

        report.append({
            'id': p['id'],
            'title': title,
            'handle': p['handle'],
            'status': p['status'],
            'vendor': p.get('vendor'),
            'product_type': p.get('product_type'),
            'tags': p.get('tags'),
            'variant_count': len(variants),
            'price_range': [min(prices), max(prices)] if prices else None,
            'has_inventory': has_inventory,
            'total_inventory': sum((v.get('inventory_quantity') or 0) for v in variants),
            'orders_90d': total_orders_90d,
            'variant_orders_90d': variant_orders,
            'suggested_action': suggested,
            'admin_url': f'https://admin.shopify.com/store/office-central-online/products/{p["id"]}',
        })

    report.sort(key=lambda r: (r['suggested_action'], r['title']))

    print('=== SUMMARY ===')
    from collections import Counter
    action_counts = Counter(r['suggested_action'] for r in report)
    for a, c in action_counts.most_common():
        print(f'  {a:25} {c}')

    print('\n=== DETAIL ===')
    for r in report:
        sales = f'{r["orders_90d"]}o' if r['orders_90d'] else '—'
        price = f'${r["price_range"][0]:.0f}-${r["price_range"][1]:.0f}' if r['price_range'] and r['price_range'][1] > 0 else '—'
        print(f'  [{r["suggested_action"]:22}] {r["title"][:55]:55}  status={r["status"]:8} sales90d={sales:4} price={price}')

    with open('junk-inspection.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(f'\nWrote junk-inspection.json ({len(report)} products)')


if __name__ == '__main__':
    main()
