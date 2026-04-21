import urllib.request
import urllib.parse
import json
import re
from collections import Counter

import os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'

def fetch_all_products():
    products = []
    url = f'{API}/products.json?limit=250&fields=id,title,body_html,vendor,product_type,tags,status,handle'
    while url:
        req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            products.extend(data['products'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(products)}...')
    return products

def strip_html(html):
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def classify(html):
    if not html or not html.strip():
        return 'empty'
    text = strip_html(html)
    if len(text) < 20:
        return 'empty'
    if 'mso-' in html or 'MsoNormal' in html:
        return 'word_junk'
    tag_density = len(re.findall(r'<[^>]+>', html)) / max(len(text.split()), 1)
    if tag_density > 0.5:
        return 'heavy_html'
    return 'clean'

print('Fetching all products...')
products = fetch_all_products()
print(f'\nTotal: {len(products)} products\n')

categories = Counter()
boilerplate_snippets = Counter()
empty_products = []
status_count = Counter()
vendor_count = Counter()

for p in products:
    cat = classify(p['body_html'])
    categories[cat] += 1
    status_count[p.get('status', 'unknown')] += 1
    if p.get('vendor'):
        vendor_count[p['vendor']] += 1
    if cat == 'empty':
        empty_products.append(p['title'])
    text = strip_html(p['body_html'])
    if text:
        first_60 = text[:60].lower()
        boilerplate_snippets[first_60] += 1

print('=== DESCRIPTION QUALITY ===')
for cat, count in categories.most_common():
    pct = count / len(products) * 100
    print(f'  {cat:15} {count:4}  ({pct:.1f}%)')

print('\n=== TOP BOILERPLATE OPENINGS (appears 5+ times) ===')
for snippet, count in boilerplate_snippets.most_common(20):
    if count >= 5:
        print(f'  [{count}x] "{snippet}..."')

print('\n=== STATUS ===')
for s, c in status_count.most_common():
    print(f'  {s:10} {c}')

print('\n=== TOP VENDORS ===')
for v, c in vendor_count.most_common(10):
    print(f'  {c:4}  {v}')

print(f'\n=== EMPTY DESCRIPTIONS (first 20 of {len(empty_products)}) ===')
for t in empty_products[:20]:
    print(f'  - {t}')

with open('audit-report.json', 'w') as f:
    json.dump({
        'total': len(products),
        'categories': dict(categories),
        'empty_products': empty_products,
        'status': dict(status_count),
        'vendors': dict(vendor_count.most_common(20)),
        'boilerplate': {k: v for k, v in boilerplate_snippets.most_common(50) if v >= 3},
    }, f, indent=2)
print('\nFull report saved to audit-report.json')
