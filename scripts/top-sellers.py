import urllib.request
import json
import re
import time
from collections import Counter

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'


def get(url):
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode())
        link = resp.headers.get('Link', '')
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        return body, m.group(1) if m else None


def fetch_orders():
    units = Counter()
    revenue = Counter()
    order_count = Counter()
    total_orders = 0
    url = f'{API}/orders.json?limit=250&status=any&financial_status=paid,partially_paid,partially_refunded,refunded&fields=id,line_items,created_at'
    while url:
        body, url = get(url)
        for o in body['orders']:
            total_orders += 1
            seen_products = set()
            for li in o.get('line_items', []):
                pid = li.get('product_id')
                if not pid:
                    continue
                qty = li.get('quantity', 0) or 0
                price = float(li.get('price', 0) or 0)
                units[pid] += qty
                revenue[pid] += qty * price
                seen_products.add(pid)
            for pid in seen_products:
                order_count[pid] += 1
        print(f'  orders: {total_orders}, unique products so far: {len(units)}')
        time.sleep(0.3)
    return units, revenue, order_count, total_orders


def fetch_product_titles(product_ids):
    titles = {}
    ids_list = list(product_ids)
    for i in range(0, len(ids_list), 100):
        batch = ids_list[i:i + 100]
        url = f'{API}/products.json?ids={",".join(str(x) for x in batch)}&fields=id,title,handle,body_html&limit=250'
        body, _ = get(url)
        for p in body['products']:
            titles[p['id']] = {'title': p['title'], 'handle': p['handle'], 'body_html': p.get('body_html', '')}
    return titles


def strip_text(html):
    if not html: return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def classify(html):
    if not html or not html.strip(): return 'empty'
    text = strip_text(html)
    if len(text) < 20: return 'empty'
    if 'mso-' in html or 'MsoNormal' in html: return 'word_junk'
    tag_density = len(re.findall(r'<[^>]+>', html)) / max(len(text.split()), 1)
    if tag_density > 0.5: return 'heavy_html'
    return 'clean'


print('Fetching all paid orders...')
units, revenue, order_count, total_orders = fetch_orders()
print(f'\nProcessed {total_orders} orders across {len(units)} unique products')

TOP_N = 50
top_pids = [pid for pid, _ in units.most_common(TOP_N + 10)]
print(f'\nFetching titles for top {len(top_pids)} products...')
info = fetch_product_titles(top_pids)

top_list = []
for pid, qty in units.most_common():
    if pid not in info:
        continue
    meta = info[pid]
    cat = classify(meta['body_html'])
    top_list.append({
        'product_id': pid,
        'title': meta['title'],
        'handle': meta['handle'],
        'units_sold': qty,
        'orders': order_count[pid],
        'revenue': round(revenue[pid], 2),
        'html_category': cat,
    })
    if len(top_list) >= TOP_N:
        break

print(f'\n=== TOP {TOP_N} BY UNITS SOLD ===')
print(f'{"#":<3} {"units":>6} {"orders":>7} {"revenue":>10}  {"html":<11}  title')
for i, r in enumerate(top_list, 1):
    print(f'{i:<3} {r["units_sold"]:>6} {r["orders"]:>7} ${r["revenue"]:>8.2f}  {r["html_category"]:<11}  {r["title"][:60]}')

by_cat = Counter(r['html_category'] for r in top_list)
print(f'\nHTML categories in top {TOP_N}: {dict(by_cat)}')
needs_cleanup = [r for r in top_list if r['html_category'] in ('heavy_html', 'word_junk')]
print(f'Top {TOP_N} products needing cleanup: {len(needs_cleanup)}')

with open('top-sellers.json', 'w') as f:
    json.dump({
        'total_orders_scanned': total_orders,
        'top_n': TOP_N,
        'top_list': top_list,
        'cleanup_pids': [r['product_id'] for r in needs_cleanup],
    }, f, indent=2)
print('\nSaved to top-sellers.json')
