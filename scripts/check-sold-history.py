"""
Phase A of broken-products fix: cross-reference every flagged product ID
against the full Orders API to determine which ones have ever been purchased.

Input : data/broken-products-report.json
Output: data/sold-history-flagged.json + console table
"""
import urllib.request
import json
import re
import os
from collections import defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = None
for line in open(os.path.join(ROOT, '.env')):
    if line.startswith('SHOPIFY_TOKEN='):
        TOKEN = line.strip().split('=', 1)[1].strip('"').strip("'")
        break

STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}


def fetch_all_orders():
    orders = []
    url = f'{API}/orders.json?status=any&limit=250&fields=id,name,created_at,financial_status,cancelled_at,line_items,total_price'
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            orders.extend(data['orders'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(orders)} orders...')
    return orders


def build_product_history(orders):
    """Return {product_id: {orders, qty, revenue, last_date, titles, statuses}}"""
    hist = defaultdict(lambda: {
        'orders': 0, 'qty': 0, 'revenue': 0.0,
        'last_date': None, 'titles': set(),
        'paid_orders': 0, 'cancelled_orders': 0,
    })
    for o in orders:
        is_cancelled = bool(o.get('cancelled_at'))
        is_paid = o.get('financial_status') == 'paid'
        created = o.get('created_at')
        for item in o.get('line_items', []):
            pid = item.get('product_id')
            if not pid:
                continue
            h = hist[pid]
            h['orders'] += 1
            h['qty'] += item.get('quantity', 0) or 0
            try:
                h['revenue'] += (item.get('quantity', 0) or 0) * float(item.get('price') or 0)
            except (ValueError, TypeError):
                pass
            if item.get('title'):
                h['titles'].add(item['title'])
            if created:
                if h['last_date'] is None or created > h['last_date']:
                    h['last_date'] = created
            if is_paid:
                h['paid_orders'] += 1
            if is_cancelled:
                h['cancelled_orders'] += 1
    # serialize sets
    for pid in hist:
        hist[pid]['titles'] = sorted(hist[pid]['titles'])
    return hist


def enrich(flagged_list, hist):
    out = []
    for p in flagged_list:
        pid = p['id']
        h = hist.get(pid, {})
        out.append({
            **p,
            'orders': h.get('orders', 0),
            'paid_orders': h.get('paid_orders', 0),
            'cancelled_orders': h.get('cancelled_orders', 0),
            'qty': h.get('qty', 0),
            'revenue': round(h.get('revenue', 0), 2),
            'last_date': h.get('last_date'),
        })
    return out


def print_bucket(title, items, show_status=False):
    print(f'\n=== {title} ({len(items)}) ===')
    if not items:
        print('  (empty)')
        return
    # Sort by revenue desc, then orders desc
    items = sorted(items, key=lambda x: (-x['revenue'], -x['orders']))
    for i in items:
        sold = '—' if i['orders'] == 0 else f"{i['paid_orders']}p/{i['orders']}t ord, {i['qty']}u, ${i['revenue']:,.0f}"
        last = i['last_date'][:10] if i.get('last_date') else 'never'
        status_tag = f" [{i.get('status','?')}]" if show_status else ''
        title = i['title'][:55]
        print(f"  {sold:28}  last:{last:>10}  {title}{status_tag}")


def main():
    report_path = os.path.join(ROOT, 'data', 'broken-products-report.json')
    with open(report_path) as f:
        report = json.load(f)

    print('Fetching all orders (this takes ~30s)...')
    orders = fetch_all_orders()
    print(f'\nTotal orders: {len(orders)}')

    hist = build_product_history(orders)
    print(f'Unique products with order history: {len(hist)}')

    # Build the bucketed view
    # Bucket 1: service pseudo-products (no-image + service-like titles + $0 price)
    SERVICE_KEYWORDS = re.compile(
        r'\b(installation|delivery|dismantle|assembly|caster|colour|color|finish|disposal|monitor arm)\b',
        re.I,
    )
    no_images = report['no_images']
    all_oos = report['all_oos']
    zero_price = report['zero_price']
    bad_handle = report['bad_handle']

    # Build quick index of flagged ids → their bucket(s)
    flagged_ids = {p['id'] for p in no_images + all_oos + zero_price + bad_handle}

    # Service bucket = intersection of (no-image OR zero-price) AND service title
    service_ids = set()
    other_no_image = []
    for p in no_images:
        if SERVICE_KEYWORDS.search(p['title']) or p['title'].lower().startswith('please select'):
            service_ids.add(p['id'])
    for p in zero_price:
        if SERVICE_KEYWORDS.search(p['title']) or p['title'].lower().startswith('please select'):
            service_ids.add(p['id'])
    # also catch named pseudo-services
    for p in no_images + zero_price:
        low = p['title'].lower()
        if 'caster options' in low or low == 'colour' or low == 'delivery':
            service_ids.add(p['id'])

    services = []
    for p in no_images + zero_price:
        if p['id'] in service_ids:
            if not any(s['id'] == p['id'] for s in services):
                services.append(p)

    # Build real-products buckets (no_image or zero_price, not a service)
    real_no_image = [p for p in no_images if p['id'] not in service_ids]
    real_zero_price = [p for p in zero_price if p['id'] not in service_ids]

    # Enrich all
    services_r = enrich(services, hist)
    oos_r = enrich(all_oos, hist)
    real_ni_r = enrich(real_no_image, hist)
    real_zp_r = enrich(real_zero_price, hist)
    bad_h_r = enrich(bad_handle, hist)

    # Segment services by sold/not-sold
    services_sold = [p for p in services_r if p['orders'] > 0]
    services_never = [p for p in services_r if p['orders'] == 0]

    # Console output
    print('\n' + '=' * 70)
    print(' SOLD-HISTORY AUDIT OF FLAGGED PRODUCTS')
    print('=' * 70)
    print_bucket('SERVICE PSEUDO-PRODUCTS — EVER SOLD (preserve record, unpublish)', services_sold, show_status=True)
    print_bucket('SERVICE PSEUDO-PRODUCTS — NEVER SOLD (safe to unpublish)', services_never, show_status=True)
    print_bucket('SOLD-OUT ACTIVE PRODUCTS (candidates for Request-a-Quote)', oos_r, show_status=False)
    print_bucket('REAL PRODUCTS MISSING IMAGE (need decision)', real_ni_r, show_status=True)
    print_bucket('REAL PRODUCTS MISSING PRICE (need decision)', real_zp_r, show_status=True)
    print_bucket('BAD-HANDLE PRODUCTS (informational — will be renamed + redirected)', bad_h_r, show_status=False)

    out = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'total_orders_scanned': len(orders),
        'unique_products_with_history': len(hist),
        'services_sold': services_sold,
        'services_never_sold': services_never,
        'sold_out_candidates': oos_r,
        'real_missing_image': real_ni_r,
        'real_missing_price': real_zp_r,
        'bad_handle_products': bad_h_r,
    }
    out_path = os.path.join(ROOT, 'data', 'sold-history-flagged.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f'\nFull report: {out_path}')


if __name__ == '__main__':
    main()
