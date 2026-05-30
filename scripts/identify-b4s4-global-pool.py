#!/usr/bin/env python3
"""B4S4 Phase 1 — identify the Global Furniture Group enrichment pool (live Admin API, read-only).
Pulls every vendor='Global Furniture Group' product with authoritative tags + specs.manufacturer
metafield (the live enrichment signal). Sub-classifies pure Global vs OTG sub-brand, ranks by
ROI (price x confidence, from CSV). Writes /tmp/b4s4-pool.json."""
import json, urllib.request, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=',1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
SHOP = 'office-central-online.myshopify.com'
GQL = f'https://{SHOP}/admin/api/2024-10/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    if 'errors' in d:
        raise SystemExit(f"GraphQL errors: {d['errors']}")
    return d['data']

Q = """
query($cursor: String) {
  products(first: 100, after: $cursor, query: "vendor:'Global Furniture Group'") {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id legacyResourceId handle title vendor productType status tags
      priceRangeV2 { minVariantPrice { amount } maxVariantPrice { amount } }
      mfManu: metafield(namespace: "specs", key: "manufacturer") { value }
      mfLine: metafield(namespace: "specs", key: "product_line") { value }
    } }
  }
}
"""

prods, cursor = [], None
while True:
    d = gql(Q, {'cursor': cursor})
    conn = d['products']
    for e in conn['edges']:
        prods.append(e['node'])
    if conn['pageInfo']['hasNextPage']:
        cursor = conn['pageInfo']['endCursor']
    else:
        break

# CSV for ROI (price x confidence)
csvrows = {}
cp = ROOT / 'data/reports/other-collection-products-20260527-093211-with-recs.csv'
for r in csv.DictReader(open(cp, encoding='utf-8')):
    csvrows[r['handle']] = r
def f(x):
    try: return float(x)
    except: return 0.0
CONF = {'high': 0.9, 'med': 0.6, 'medium': 0.6, 'low': 0.3, 'none': 0.15, '': 0.5}

def is_otg(node):
    blob = (node['title'] + ' ' + ' '.join(node['tags'])).lower()
    return ('offices to go' in blob) or ('offices-to-go' in blob) or bool(re.search(r'\botg\b', blob)) \
           or any('offices-to-go' in t.lower() or t.lower() in ('otg','sub-brand:otg','sub-brand:offices-to-go') for t in node['tags'])

out = []
for n in prods:
    h = n['handle']
    cr = csvrows.get(h, {})
    conf_raw = (cr.get('claude_confidence') or '').strip().lower()
    conf = CONF.get(conf_raw, 0.5)
    pr = n.get('priceRangeV2') or {}
    pmax = f((pr.get('maxVariantPrice') or {}).get('amount'))
    pmin = f((pr.get('minVariantPrice') or {}).get('amount'))
    price = max(pmax, pmin)
    enriched_live = bool((n.get('mfManu') or {}).get('value'))
    enriched_csv = (cr.get('tier_a_enriched') or '').strip().upper() == 'Y'
    out.append({
        'product_id': n['legacyResourceId'], 'handle': h, 'title': n['title'],
        'product_type': n['productType'], 'status': n['status'], 'tags': n['tags'],
        'price': price, 'conf_raw': conf_raw or '(none)', 'roi': round(price*conf,1),
        'specs_manufacturer': (n.get('mfManu') or {}).get('value'),
        'specs_product_line': (n.get('mfLine') or {}).get('value'),
        'enriched_live': enriched_live, 'enriched_csv': enriched_csv,
        'is_otg': is_otg(n),
        'in_csv': h in csvrows,
    })

Path('/tmp/b4s4-pool.json').write_text(json.dumps(out, indent=2))

tot = len(out)
enr = [p for p in out if p['enriched_live']]
pool = [p for p in out if not p['enriched_live']]
pure = [p for p in pool if not p['is_otg']]
otg = [p for p in pool if p['is_otg']]
print(f"=== LIVE Admin API: vendor='Global Furniture Group' ===")
print(f"  total products:           {tot}")
print(f"  already enriched (live specs.manufacturer set): {len(enr)}")
print(f"  enrichment POOL (no specs.manufacturer):        {len(pool)}")
print(f"     - Pure Global:  {len(pure)}")
print(f"     - OTG sub-brand:{len(otg)}")
print(f"  (rows missing from CSV: {len([p for p in pool if not p['in_csv']])})")
print(f"\n=== TOP 22 POOL BY ROI ===")
for p in sorted(pool, key=lambda x:-x['roi'])[:22]:
    tag = 'OTG' if p['is_otg'] else 'GLB'
    print(f"  [{tag}] roi={p['roi']:8.1f} ${p['price']:8.2f} conf={p['conf_raw']:>6} {p['status']:8} | {p['handle'][:46]}")
print("\nwritten /tmp/b4s4-pool.json")
