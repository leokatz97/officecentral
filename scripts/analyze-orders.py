import urllib.request
import urllib.parse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime

import os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'

def fetch_all(path):
    items = []
    url = f'{API}/{path}'
    while url:
        req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            key = list(data.keys())[0]
            items.extend(data[key])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(items)}...')
    return items

print('Fetching all orders...')
orders = fetch_all('orders.json?status=any&limit=250')
print(f'\nTotal orders: {len(orders)}\n')

# Revenue analysis
total_rev = 0
order_aovs = []
product_revenue = defaultdict(float)
product_qty = defaultdict(int)
product_orders = defaultdict(int)
monthly_rev = defaultdict(float)
monthly_count = defaultdict(int)
customer_spend = defaultdict(float)
customer_orders = defaultdict(int)
order_sizes = []
first_order_date = None
last_order_date = None
paid_count = 0
cancelled_count = 0
financial_status = Counter()
line_items_per_order = []

for order in orders:
    try:
        rev = float(order.get('total_price', 0))
    except (ValueError, TypeError):
        rev = 0
    total_rev += rev
    order_aovs.append(rev)
    order_sizes.append(rev)

    financial_status[order.get('financial_status', 'unknown')] += 1
    if order.get('financial_status') == 'paid':
        paid_count += 1
    if order.get('cancelled_at'):
        cancelled_count += 1

    created = order.get('created_at', '')
    if created:
        dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
        month_key = dt.strftime('%Y-%m')
        monthly_rev[month_key] += rev
        monthly_count[month_key] += 1
        if first_order_date is None or dt < first_order_date:
            first_order_date = dt
        if last_order_date is None or dt > last_order_date:
            last_order_date = dt

    email = order.get('email', '') or order.get('customer', {}).get('email', '') if order.get('customer') else ''
    if email:
        customer_spend[email] += rev
        customer_orders[email] += 1

    items = order.get('line_items', [])
    line_items_per_order.append(len(items))
    for item in items:
        pid = item.get('product_id')
        title = item.get('title', 'Unknown')
        qty = item.get('quantity', 0)
        try:
            price = float(item.get('price', 0))
        except (ValueError, TypeError):
            price = 0
        key = (pid, title)
        product_revenue[key] += qty * price
        product_qty[key] += qty
        product_orders[key] += 1

print('=== REVENUE OVERVIEW ===')
print(f'Total revenue: ${total_rev:,.2f}')
print(f'Orders: {len(orders)}')
print(f'AOV: ${total_rev/len(orders):,.2f}')
print(f'Paid: {paid_count}  Cancelled: {cancelled_count}')
print(f'Date range: {first_order_date.date()} to {last_order_date.date()}')

print('\n=== FINANCIAL STATUS ===')
for status, c in financial_status.most_common():
    print(f'  {status:20} {c}')

print('\n=== ORDER SIZE DISTRIBUTION ===')
order_sizes.sort()
if order_sizes:
    print(f'  Min:     ${order_sizes[0]:,.2f}')
    print(f'  Median:  ${order_sizes[len(order_sizes)//2]:,.2f}')
    print(f'  Mean:    ${sum(order_sizes)/len(order_sizes):,.2f}')
    print(f'  Max:     ${order_sizes[-1]:,.2f}')

    # Bucket
    buckets = [('<$100', 0), ('$100-500', 0), ('$500-2k', 0), ('$2k-10k', 0), ('$10k-50k', 0), ('>$50k', 0)]
    for o in order_sizes:
        if o < 100: buckets[0] = (buckets[0][0], buckets[0][1]+1)
        elif o < 500: buckets[1] = (buckets[1][0], buckets[1][1]+1)
        elif o < 2000: buckets[2] = (buckets[2][0], buckets[2][1]+1)
        elif o < 10000: buckets[3] = (buckets[3][0], buckets[3][1]+1)
        elif o < 50000: buckets[4] = (buckets[4][0], buckets[4][1]+1)
        else: buckets[5] = (buckets[5][0], buckets[5][1]+1)
    print('\n  Distribution:')
    for label, n in buckets:
        pct = n/len(order_sizes)*100
        bar = '█' * int(pct/2)
        print(f'    {label:12} {n:4}  {pct:5.1f}%  {bar}')

print('\n=== MONTHLY TREND (last 12 months) ===')
sorted_months = sorted(monthly_rev.keys())
for m in sorted_months[-12:]:
    print(f'  {m}  {monthly_count[m]:3} orders  ${monthly_rev[m]:>12,.2f}')

print('\n=== TOP 20 PRODUCTS BY REVENUE ===')
top_products = sorted(product_revenue.items(), key=lambda x: -x[1])[:20]
for (pid, title), rev in top_products:
    qty = product_qty[(pid, title)]
    orders_count = product_orders[(pid, title)]
    title_trim = title[:60]
    print(f'  ${rev:>10,.2f}  ({qty:3}u, {orders_count:3} ord) {title_trim}')

total_top20_rev = sum(r for _, r in top_products)
print(f'\n  Top 20 = ${total_top20_rev:,.2f} ({total_top20_rev/total_rev*100:.1f}% of total)')

unique_products_sold = len(product_revenue)
print(f'\n  Unique products sold: {unique_products_sold} (out of 650 total in catalog)')

print('\n=== CUSTOMER CONCENTRATION ===')
sorted_customers = sorted(customer_spend.items(), key=lambda x: -x[1])
if sorted_customers:
    top10_rev = sum(v for _, v in sorted_customers[:10])
    repeat = sum(1 for _, c in customer_orders.items() if c > 1)
    print(f'  Unique customers: {len(sorted_customers)}')
    print(f'  Repeat buyers: {repeat} ({repeat/len(sorted_customers)*100:.1f}%)')
    print(f'  Top 10 customer spend: ${top10_rev:,.2f} ({top10_rev/total_rev*100:.1f}% of revenue)')
    print('\n  Top 10 customers:')
    for email, spend in sorted_customers[:10]:
        orders_n = customer_orders[email]
        print(f'    ${spend:>10,.2f}  ({orders_n} orders)  {email}')

# Save full report
with open('sales-report.json', 'w') as f:
    json.dump({
        'total_revenue': total_rev,
        'order_count': len(orders),
        'aov': total_rev/len(orders) if orders else 0,
        'date_range': [str(first_order_date), str(last_order_date)] if first_order_date else [],
        'unique_products_sold': unique_products_sold,
        'unique_customers': len(sorted_customers),
        'top_products': [{'id': pid, 'title': t, 'revenue': r, 'qty': product_qty[(pid,t)], 'orders': product_orders[(pid,t)]} for (pid, t), r in top_products],
        'monthly': [{'month': m, 'orders': monthly_count[m], 'revenue': monthly_rev[m]} for m in sorted_months],
        'top_customers': [{'email': e, 'spend': s, 'orders': customer_orders[e]} for e, s in sorted_customers[:20]],
    }, f, indent=2, default=str)
print('\nFull report saved to sales-report.json')
