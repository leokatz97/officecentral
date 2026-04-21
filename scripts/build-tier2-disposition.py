"""
Tier 2 — produce the disposition review for Steve.

For every active product, apply the 5 decision rules from the plan and propose:
  - archive             (cut from storefront, preserved in admin)
  - keep-live-quote     (stays live with Quotify quote button — no transaction)
  - keep-live           (stays live, transactional — sold or strategic line)

READ-ONLY. Writes:
  data/tier-2-disposition-review.csv   — per-SKU
  docs/tier-2-disposition-summary.md   — 1-page summary for Steve

Re-runnable. Caches the full Orders pull at data/_orders-cache.json so we don't
re-pull every run during iteration.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = None
for line in open(os.path.join(ROOT, '.env')):
    if line.startswith('SHOPIFY_TOKEN='):
        TOKEN = line.strip().split('=', 1)[1].strip('"').strip("'")
        break

STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN}

DATA_DIR = os.path.join(ROOT, 'data')
DOCS_DIR = os.path.join(ROOT, 'docs')
ORDERS_CACHE = os.path.join(DATA_DIR, '_orders-cache.json')
CSV_OUT = os.path.join(DATA_DIR, 'tier-2-disposition-review.csv')
SUMMARY_OUT = os.path.join(DOCS_DIR, 'tier-2-disposition-summary.md')

# Strategic brand lines — protected from archive even with zero sales.
# Match against title/vendor/tags case-insensitively.
STRATEGIC_BRANDS = [
    'otg', 'offices to go', 'basics', 'concorde', 'global',
    'obusforme', 'obus forme', 'indigenous', 'medicine wheel',
    'zira', 'roma', 'ashmont', 'ibex', 'teknion', 'ryno',
    'auditorium', 'sidero', 'marche', 'overtime',
]

# Keywords that mark genuine ghost/placeholder SKUs — NOT real products.
# Kept narrow to avoid false positives on real products whose titles mention
# colour variants (e.g. "Nesting Training Table (8 Colour Choices)").
JUNK_KEYWORDS = [
    'parka', 'hydro parka',  # wrong category (apparel)
    'follower block', 'dummy variant', 'test product', 'do not use',
    'demo only', 'placeholder',
]

# Title patterns that mark known showcase/quote-only products
SHOWCASE_KEYWORDS = ['teknion', 'ryno', 'auditorium', 'medicine wheel']

# Product-type bucketing for the summary table.
TYPE_BUCKETS = [
    ('Outdoor', ['outdoor', 'patio', 'ryno']),
    ('Lounge', ['lounge', 'sofa', 'loveseat', 'ottoman', 'recliner']),
    ('Chairs', [
        'chair', 'stool', 'tilter', 'seating', 'high back', 'mid back',
        'task ', 'executive seating', 'armchair',
    ]),
    ('Desks', ['desk', 'workstation', 'sit-stand', 'sit stand']),
    ('Tables', [
        'table', 'boardroom', 'training table', 'conference', 'meeting table',
    ]),
    ('Storage', [
        'cabinet', 'pedestal', 'storage', 'bookcase', 'bookshelf',
        'lateral', 'file ', 'filing', 'credenza', 'locker', 'safe',
        'drawer', 'hutch', 'vertical file', 'wardrobe', 'shelving',
    ]),
    ('Accessories', [
        'monitor arm', 'monitor', 'mat', 'divider', 'partition', 'screen',
        'accessor', 'panel', 'coat tree', 'coat hook', 'caster', 'foot kit',
        'power', 'charging', 'usb', 'lamp', 'holder', 'rack', 'tray',
        'dampener', 'acoustic', 'sound', 'whiteboard', 'shelf only',
        'corner maker', 'modesty', 'planter', 'cushion', 'mat with lip',
    ]),
]


def fetch_all_products():
    products = []
    fields = 'id,title,handle,status,published_at,images,variants,vendor,product_type,tags,body_html'
    url = f'{API}/products.json?limit=250&fields={fields}'
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            products.extend(data['products'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(products)} products...', file=sys.stderr)
    return products


def fetch_all_orders():
    if os.path.exists(ORDERS_CACHE):
        age = time.time() - os.path.getmtime(ORDERS_CACHE)
        if age < 6 * 3600:
            print(f'  using cached orders ({int(age/60)} min old)', file=sys.stderr)
            with open(ORDERS_CACHE) as f:
                return json.load(f)
    orders = []
    url = (f'{API}/orders.json?status=any&limit=250'
           '&fields=id,name,created_at,financial_status,cancelled_at,line_items')
    while url:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            orders.extend(data['orders'])
            link = resp.headers.get('Link', '')
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
        print(f'  fetched {len(orders)} orders...', file=sys.stderr)
    with open(ORDERS_CACHE, 'w') as f:
        json.dump(orders, f)
    return orders


def build_sales_index(orders):
    """{product_id: {orders, qty, revenue, last_date}}"""
    idx = defaultdict(lambda: {'orders': 0, 'qty': 0, 'revenue': 0.0, 'last_date': None})
    for o in orders:
        created = o.get('created_at')
        for item in o.get('line_items', []):
            pid = item.get('product_id')
            if not pid:
                continue
            h = idx[pid]
            h['orders'] += 1
            qty = item.get('quantity', 0) or 0
            h['qty'] += qty
            try:
                h['revenue'] += qty * float(item.get('price') or 0)
            except (ValueError, TypeError):
                pass
            if created and (h['last_date'] is None or created > h['last_date']):
                h['last_date'] = created
    return idx


def has_keyword(text, keywords):
    t = (text or '').lower()
    return any(k in t for k in keywords)


def bucket_type(product):
    """Return one of: Chairs, Desks, Tables, Storage, Lounge, Accessories, Outdoor, Other"""
    haystack = ' '.join([
        product.get('product_type') or '',
        product.get('title') or '',
        product.get('tags') or '',
    ]).lower()
    for label, keys in TYPE_BUCKETS:
        if any(k in haystack for k in keys):
            return label
    return 'Other'


def all_variants_unavailable(product):
    """True if every variant is tracked + out of stock + deny."""
    variants = product.get('variants') or []
    tracked = [v for v in variants if v.get('inventory_management') == 'shopify']
    if not tracked:
        return False
    oos = [v for v in tracked
           if (v.get('inventory_quantity') or 0) <= 0 and v.get('inventory_policy') == 'deny']
    return len(oos) == len(tracked)


def has_zero_price(product):
    for v in product.get('variants') or []:
        try:
            if float(v.get('price') or 0) <= 0:
                return True
        except (ValueError, TypeError):
            pass
    return False


def has_image(product):
    return bool(product.get('images'))


def is_strategic(product):
    text = ' '.join([
        product.get('title') or '',
        product.get('vendor') or '',
        product.get('tags') or '',
    ])
    return has_keyword(text, STRATEGIC_BRANDS)


def is_showcase(product):
    text = ' '.join([product.get('title') or '', product.get('vendor') or ''])
    return has_keyword(text, SHOWCASE_KEYWORDS)


def is_junk(product):
    title = product.get('title') or ''
    body = product.get('body_html') or ''
    if has_keyword(title, JUNK_KEYWORDS):
        return True
    # No images, no real body, no sales — looks like a placeholder
    if not has_image(product) and len(body.strip()) < 30:
        return True
    return False


def apply_rules(product, sold_count):
    """Return (action, rule_applied, reason)."""
    sold = sold_count > 0

    # Rule 5 first: sold products are always kept live.
    if sold:
        return ('keep-live', 'sold', f'{sold_count} units sold')

    # Rule 1: genuine ghost / placeholder SKU — archive.
    if is_junk(product):
        return ('archive', 'junk', 'ghost SKU / placeholder / wrong-category')

    # Rule 2: sold-out real product
    if all_variants_unavailable(product):
        return ('keep-live-quote', 'sold-out', 'all variants out of stock — show quote button')

    # Rule 3: $0-price showcase
    if has_zero_price(product) and has_image(product):
        return ('keep-live-quote', '$0-showcase', 'no price set, real product — quote button')

    # Rule 5b: strategic brand line, even if never sold
    if is_strategic(product):
        return ('keep-live', 'strategic-brand', 'protected brand line')

    # Rule 3b: known showcase brand even with price
    if is_showcase(product):
        return ('keep-live-quote', 'showcase-brand', 'manufacturer showcase page')

    # Rule 4: never sold, real product, no strategic protection → Clearance.
    return ('clearance', 'never-sold', 'never sold — move to Clearance at 10% off')


def propose_tags(product, action):
    """Tier 2 taxonomy: type / room / industry. Heuristic — meant to be reviewed."""
    if action == 'archive':
        return ''
    type_bucket = bucket_type(product).lower()
    if type_bucket == 'other':
        type_bucket = ''

    title = (product.get('title') or '').lower()
    room = ''
    if any(k in title for k in ['boardroom', 'conference', 'meeting']):
        room = 'boardroom'
    elif any(k in title for k in ['reception', 'lobby']):
        room = 'reception'
    elif any(k in title for k in ['training']):
        room = 'training-room'
    elif any(k in title for k in ['lounge', 'sofa', 'loveseat']):
        room = 'lounge'
    elif any(k in title for k in ['break', 'lunch', 'cafeteria']):
        room = 'break-room'
    elif any(k in title for k in ['executive', 'private', 'manager']):
        room = 'private-office'
    elif type_bucket in ('chairs', 'desks'):
        room = 'open-plan'

    industry = ''
    if 'medicine wheel' in title or 'indigenous' in title:
        industry = 'first-nations'
    # Industry tagging is mostly manual — leave blank otherwise.

    parts = [type_bucket, room, industry]
    return ', '.join(p for p in parts if p)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    print('Fetching products...', file=sys.stderr)
    products = fetch_all_products()
    print('Fetching orders (cached if recent)...', file=sys.stderr)
    orders = fetch_all_orders()
    sales = build_sales_index(orders)

    # Only operate on active products. Drafts + archived already handled in Tier 1.
    active = [p for p in products if p.get('status') == 'active']

    rows = []
    for p in active:
        sold_count = sales.get(p['id'], {}).get('orders', 0)
        revenue = sales.get(p['id'], {}).get('revenue', 0.0)
        action, rule, reason = apply_rules(p, sold_count)
        bucket = bucket_type(p)
        tags = propose_tags(p, action)
        rows.append({
            'handle': p.get('handle', ''),
            'title': p.get('title', ''),
            'type_bucket': bucket,
            'product_type': p.get('product_type', ''),
            'vendor': p.get('vendor', ''),
            'sold_orders': sold_count,
            'sold_revenue': round(revenue, 2),
            'has_image': 'Y' if has_image(p) else 'N',
            'has_price': 'N' if has_zero_price(p) else 'Y',
            'all_oos': 'Y' if all_variants_unavailable(p) else 'N',
            'rule_applied': rule,
            'proposed_action': action,
            'reason': reason,
            'proposed_tags': tags,
            'admin_url': f'https://admin.shopify.com/store/office-central/products/{p["id"]}',
        })

    rows.sort(key=lambda r: (r['proposed_action'], r['type_bucket'], r['title']))

    with open(CSV_OUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    by_action = Counter(r['proposed_action'] for r in rows)
    by_rule = Counter(r['rule_applied'] for r in rows)
    by_action_type = defaultdict(Counter)
    for r in rows:
        by_action_type[r['type_bucket']][r['proposed_action']] += 1

    type_buckets = sorted(by_action_type.keys())

    lines = []
    lines.append('# Tier 2 Disposition — Steve\'s Review')
    lines.append('')
    lines.append(f'_Generated {datetime.now(timezone.utc).isoformat(timespec="seconds")} from {len(active)} active products._')
    lines.append('')
    lines.append('## What this is')
    lines.append('')
    lines.append('Steve — before we touch anything on the store, here\'s the proposed disposition for every active product.')
    lines.append('Four buckets:')
    lines.append('')
    lines.append('- **archive** — ghost / placeholder SKU. Hidden from storefront, preserved in admin.')
    lines.append('- **clearance** — never sold but real product. Moves to a dedicated Clearance / Last Chance collection at **10% off**. Keeps the URL live, preserves SEO, gives buyers a reason to browse, and turns some of the dead stock into revenue.')
    lines.append('- **keep-live-quote** — sold-out, $0-price, or showcase page. Stays live but only shows a "Request a Quote" button (no transaction).')
    lines.append('- **keep-live** — sold in last 18 months, OR a strategic brand line we keep visible regardless of sales.')
    lines.append('')
    lines.append('**Nothing has been changed yet.** This is the proposal. Open the CSV ([data/tier-2-disposition-review.csv](../data/tier-2-disposition-review.csv)), mark any rows you disagree with, and send back.')
    lines.append('')
    lines.append('## Totals')
    lines.append('')
    lines.append('| Action | Count |')
    lines.append('|---|---:|')
    for action in ['archive', 'clearance', 'keep-live-quote', 'keep-live']:
        lines.append(f'| {action} | {by_action.get(action, 0)} |')
    lines.append(f'| **Total active** | **{len(rows)}** |')
    lines.append('')
    lines.append('## Breakdown by product type')
    lines.append('')
    lines.append('| Type | Archive | Clearance | Keep-Live-Quote | Keep-Live | Total |')
    lines.append('|---|---:|---:|---:|---:|---:|')
    for t in type_buckets:
        c = by_action_type[t]
        total = sum(c.values())
        lines.append(f'| {t} | {c.get("archive", 0)} | {c.get("clearance", 0)} | {c.get("keep-live-quote", 0)} | {c.get("keep-live", 0)} | {total} |')
    lines.append('')
    lines.append('## Why each row was placed (rule applied)')
    lines.append('')
    lines.append('| Rule | Count | What it means |')
    lines.append('|---|---:|---|')
    rule_explain = {
        'sold': 'Has sold ≥1 unit in the last 18 months. Untouched.',
        'strategic-brand': 'Brand line we protect even with zero sales (OTG, Basics, Concorde, etc.).',
        'sold-out': 'All variants out of stock. Stays live with quote button.',
        '$0-showcase': 'No price set, real product. Stays live with quote button.',
        'showcase-brand': 'Known manufacturer showcase page (Teknion / Ryno / Auditorium).',
        'junk': 'Ghost SKU or placeholder — not a real product. Archive.',
        'never-sold': 'Real product, has price + image, never sold, no strategic protection. Move to Clearance at 10% off.',
    }
    for rule in ['sold', 'strategic-brand', 'sold-out', '$0-showcase', 'showcase-brand', 'junk', 'never-sold']:
        lines.append(f'| {rule} | {by_rule.get(rule, 0)} | {rule_explain.get(rule, "")} |')
    lines.append('')
    lines.append('## Proposed new collection structure')
    lines.append('')
    lines.append('Three facets, every kept product tagged on all three. Implemented as automated tag-based collections.')
    lines.append('')
    lines.append('**By Product Type** — Chairs · Desks · Tables · Storage · Accessories · Lounge · Outdoor')
    lines.append('')
    lines.append('**By Room** — Private Office · Boardroom · Reception · Open Plan · Training Room · Break Room · Lounge')
    lines.append('')
    lines.append('**By Industry** — Health Centres · Schools · Government · First Nations Organizations · Engineering Firms · Non-Profits')
    lines.append('')
    lines.append('Tag proposals are in the CSV column `proposed_tags`. Industry tags are mostly blank — those\'ll be a manual pass after this CSV is approved.')
    lines.append('')
    lines.append('## Sign-off')
    lines.append('')
    lines.append('☐ Steve has reviewed the CSV and the bucket counts above.')
    lines.append('☐ Steve has noted any rows to flip (comment in CSV or list back).')
    lines.append('☐ Approved → run `apply-tier2-archives.py` + `apply-tier2-tags.py` + `build-tier2-collections.py` + `build-tier2-redirects.py`.')

    with open(SUMMARY_OUT, 'w') as f:
        f.write('\n'.join(lines))

    print('\n=== TOTALS ===', file=sys.stderr)
    for action, n in by_action.most_common():
        print(f'  {action:18} {n}', file=sys.stderr)
    print(f'\nCSV     : {CSV_OUT}', file=sys.stderr)
    print(f'Summary : {SUMMARY_OUT}', file=sys.stderr)


if __name__ == '__main__':
    main()
