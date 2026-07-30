#!/usr/bin/env python3
"""FEED-AUDIT — read-only full-catalog fetch for the Shopping-feed readiness audit.

Pulls every product with all fields that map to Google Merchant Center feed
attributes (title->title, body_html->description, vendor->brand,
variant.barcode->gtin, variant.sku->mpn/id, images->image_link, price->price,
inventory->availability, product_type/google category metafield, weight->shipping).
Also lists publications so we can name the Google/Merchant-Center channel.

No writes. Caches to data/reports/_catalog-feed-snapshot-<date>.json
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
GQL = f'https://{SHOP}/admin/api/2024-10/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def _open(req):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 2 ** attempt
                print(f"   (HTTP {e.code} backoff {wait}s)", file=sys.stderr, flush=True)
                time.sleep(wait)
                continue
            print(f"HTTPError {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
            raise


def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method='POST')
    d = _open(req)
    if 'errors' in d:
        raise RuntimeError(json.dumps(d['errors'], indent=2))
    return d['data']


def fetch_publications():
    q = '{ publications(first: 25) { edges { node { id name } } } }'
    try:
        return [e['node'] for e in gql(q)['publications']['edges']]
    except Exception as e:
        return [{'error': str(e)}]


PRODUCTS_Q = '''
query($cursor: String) {
  products(first: 60, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges { node {
      id legacyResourceId handle title vendor productType status tags
      descriptionHtml
      onlineStoreUrl
      totalInventory
      seo { title description }
      featuredImage { url width height altText }
      images(first: 6) { edges { node { url width height altText } } }
      category { id name fullName }
      variants(first: 30) { edges { node {
        sku barcode price inventoryQuantity inventoryPolicy
        inventoryItem { measurement { weight { value unit } } }
      } } }
      metafields(first: 60) { edges { node { namespace key value } } }
    }}
  }
}'''


def fetch_all():
    out, cursor, page = [], None, 0
    while True:
        page += 1
        conn = gql(PRODUCTS_Q, {'cursor': cursor})['products']
        out.extend(e['node'] for e in conn['edges'])
        print(f'  page {page}: total {len(out)}', file=sys.stderr, flush=True)
        if not conn['pageInfo']['hasNextPage']:
            break
        cursor = conn['pageInfo']['endCursor']
        time.sleep(0.2)
    return out


def main():
    date = datetime.now().strftime('%Y-%m-%d')
    pubs = fetch_publications()
    print('PUBLICATIONS / CHANNELS:', file=sys.stderr)
    for p in pubs:
        print('  ', p, file=sys.stderr)
    products = fetch_all()
    snap = {'fetched': date, 'count': len(products), 'publications': pubs, 'products': products}
    outp = ROOT / 'data' / 'reports' / f'_catalog-feed-snapshot-{date}.json'
    outp.write_text(json.dumps(snap, indent=2))
    print(f'\nWROTE {outp.relative_to(ROOT)} — {len(products)} products', file=sys.stderr)
    # print channel summary to stdout for the caller
    print(json.dumps({'count': len(products), 'publications': pubs}))


if __name__ == '__main__':
    main()
