import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

PRODUCTS_CSV = Path('/Users/leokatz/Downloads/products_export_1.csv')
SALES_CSV = Path('/Users/leokatz/Downloads/Total sales by product - 2023-01-01 - 2026-04-21.csv')
OUT_CSV = Path(__file__).resolve().parent.parent / 'data' / 'enrichment-priorities.csv'

SERVICE_TYPES = {'Avis-add-charge'}
SERVICE_TITLE_PATTERNS = [
    r'^installation',
    r'^delivery',
    r'^caster options',
    r'^colour$',
    r'^please select',
    r'^additional services',
]

METAFIELD_COLUMNS = {
    'Color': 'Color (product.metafields.shopify.color-pattern)',
    'Material': 'Material (product.metafields.shopify.material)',
    'Style': 'Style (product.metafields.shopify.style)',
    'Suitable location': 'Suitable location (product.metafields.shopify.suitable-location)',
    'Furniture/Fixture material': 'Furniture/Fixture material (product.metafields.shopify.furniture-fixture-material)',
    'Upholstery material': 'Upholstery material (product.metafields.shopify.upholstery-material)',
    'Seat type': 'Seat type (product.metafields.shopify.seat-type)',
    'Seat structure': 'Seat structure (product.metafields.shopify.seat-structure)',
    'Back type': 'Back type (product.metafields.shopify.back-type)',
    'Backrest type': 'Backrest type (product.metafields.shopify.backrest-type)',
    'Chair features': 'Chair features (product.metafields.shopify.chair-features)',
    'Frame design': 'Frame design (product.metafields.shopify.frame-design)',
    'Wood finish': 'Wood finish (product.metafields.shopify.wood-finish)',
    'Tabletop color': 'Tabletop color (product.metafields.shopify.tabletop-color)',
    'Leg color': 'Leg color (product.metafields.shopify.leg-color)',
    'Sound insulation': 'Sound insulation (product.metafields.shopify.sound-insulation)',
    'Furniture/Fixture features': 'Furniture/Fixture features (product.metafields.shopify.furniture-fixture-features)',
}


def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = text.replace('™', '').replace('®', '').replace('©', '')
    text = text.replace('&', ' and ')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text


def is_service_row(title, ptype):
    if ptype and ptype.strip() in SERVICE_TYPES:
        return True
    low = title.lower().strip()
    for pat in SERVICE_TITLE_PATTERNS:
        if re.match(pat, low):
            return True
    return False


def load_products():
    products = {}
    with PRODUCTS_CSV.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            handle = row.get('Handle', '').strip()
            if not handle:
                continue
            if handle not in products:
                products[handle] = {
                    'Handle': handle,
                    'Title': row.get('Title', '').strip(),
                    'Type': row.get('Type', '').strip(),
                    'ProductCategory': row.get('Product Category', '').strip(),
                    'Vendor': row.get('Vendor', '').strip(),
                    'Tags': row.get('Tags', '').strip(),
                    'Status': row.get('Status', '').strip(),
                    'Body': row.get('Body (HTML)', '').strip(),
                    'SEOTitle': row.get('SEO Title', '').strip(),
                    'SEODescription': row.get('SEO Description', '').strip(),
                    'HasImage': False,
                    'Metafields': {},
                }
                for label, col in METAFIELD_COLUMNS.items():
                    products[handle]['Metafields'][label] = row.get(col, '').strip()
            if row.get('Image Src', '').strip():
                products[handle]['HasImage'] = True
            for label, col in METAFIELD_COLUMNS.items():
                val = row.get(col, '').strip()
                if val and not products[handle]['Metafields'][label]:
                    products[handle]['Metafields'][label] = val
    return products


def load_sales():
    rows = []
    with SALES_CSV.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = (row.get('Product title') or '').strip()
            ptype = (row.get('Product type') or '').strip()
            if not title:
                continue
            if is_service_row(title, ptype):
                continue
            try:
                net_sales = float(row.get('Net sales') or 0)
                units = int(float(row.get('Net items sold') or 0))
            except ValueError:
                continue
            if net_sales <= 0:
                continue
            rows.append({'title': title, 'net_sales': net_sales, 'units': units, 'slug': slugify(title)})
    return rows


def match_sales_to_handles(sales, products):
    slug_to_handle = {h: h for h in products}
    title_slug_to_handle = {slugify(p['Title']): h for h, p in products.items() if p['Title']}
    matched = []
    unmatched = []
    for s in sales:
        h = None
        if s['slug'] in slug_to_handle:
            h = s['slug']
        elif s['slug'] in title_slug_to_handle:
            h = title_slug_to_handle[s['slug']]
        else:
            for handle in products:
                if s['slug'] and (s['slug'] in handle or handle in s['slug']):
                    if abs(len(s['slug']) - len(handle)) < 15:
                        h = handle
                        break
        if h:
            matched.append((s, h))
        else:
            unmatched.append(s)
    return matched, unmatched


def assign_tiers(products, matched):
    revenue_by_handle = defaultdict(float)
    units_by_handle = defaultdict(int)
    for s, h in matched:
        revenue_by_handle[h] += s['net_sales']
        units_by_handle[h] += s['units']
    ranked = sorted(revenue_by_handle.items(), key=lambda x: x[1], reverse=True)
    total_rev = sum(r for _, r in ranked)
    cum = 0
    tier_map = {}
    for i, (h, rev) in enumerate(ranked):
        cum += rev
        pct_cum = cum / total_rev if total_rev else 0
        pct_rank = (i + 1) / len(ranked)
        if pct_cum <= 0.80 and pct_rank <= 0.20:
            tier_map[h] = 'A'
        elif pct_rank <= 0.50:
            tier_map[h] = 'B'
        else:
            tier_map[h] = 'C'
    for h in products:
        if h not in tier_map:
            tier_map[h] = 'D'
    return tier_map, revenue_by_handle, units_by_handle


def count_gaps(p):
    gaps = []
    if not p['Type']:
        gaps.append('Type')
    if not p['ProductCategory']:
        gaps.append('Category')
    if not p['Tags']:
        gaps.append('Tags')
    if not p['Body'] or len(re.sub(r'<[^>]+>', '', p['Body'])) < 100:
        gaps.append('Body')
    if not p['SEOTitle']:
        gaps.append('SEOTitle')
    if not p['SEODescription']:
        gaps.append('SEODescription')
    if not p['HasImage']:
        gaps.append('Image')
    for label, val in p['Metafields'].items():
        if not val:
            gaps.append(f'mf:{label}')
    return gaps


def main():
    print('Loading products...')
    products = load_products()
    print(f'  {len(products)} unique products')

    print('Loading sales...')
    sales = load_sales()
    print(f'  {len(sales)} product sales rows (services excluded)')

    print('Matching sales to handles...')
    matched, unmatched = match_sales_to_handles(sales, products)
    print(f'  matched: {len(matched)}, unmatched: {len(unmatched)}')
    if unmatched:
        print('  Unmatched titles:')
        for s in unmatched[:20]:
            print(f'    - {s["title"]} (slug={s["slug"]}) ${s["net_sales"]:.0f}')

    print('Assigning tiers...')
    tier_map, rev_by_handle, units_by_handle = assign_tiers(products, matched)
    from collections import Counter
    tier_counts = Counter(tier_map.values())
    for t in 'ABCD':
        print(f'  Tier {t}: {tier_counts[t]}')

    print('Computing gaps + priority...')
    rows = []
    for h, p in products.items():
        gaps = count_gaps(p)
        tier = tier_map[h]
        tier_weight = {'A': 4, 'B': 3, 'C': 2, 'D': 1}[tier]
        score = tier_weight * len(gaps)
        rows.append({
            'Handle': h,
            'Title': p['Title'],
            'Type': p['Type'] or p['ProductCategory'] or '',
            'Status': p['Status'],
            'Tier': tier,
            'Revenue': round(rev_by_handle.get(h, 0), 2),
            'Units': units_by_handle.get(h, 0),
            'MissingCount': len(gaps),
            'PriorityScore': score,
            'MissingFields': '; '.join(gaps),
        })
    rows.sort(key=lambda r: (-r['PriorityScore'], -r['Revenue']))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f'\nWrote {len(rows)} rows to {OUT_CSV}')

    print('\nTop 20 enrichment priorities:')
    print(f'  {"Tier":5} {"Rev":>10} {"Gaps":>5}  Handle')
    for r in rows[:20]:
        print(f'  {r["Tier"]:5} {r["Revenue"]:>10.0f} {r["MissingCount"]:>5}  {r["Handle"]}')


if __name__ == '__main__':
    main()
