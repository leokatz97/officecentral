#!/usr/bin/env python3
"""Export the 87 AMBIGUOUS (incl. 7 SCN) vendor=BBI products as a Steve-facing
decode review sheet (READ-ONLY, 2026-06-02).

Source: data/reports/bbi-resourcing-2026-06-02-evidence.json (Phase-0 scan / #86
worksheet). Enriches each row with LIVE product_type / tags / variant barcode
(MPN candidate) via a read-only Admin-API GET — the scan did not persist tags and
left product_type/barcode mostly blank, and those are the strongest decode signals
for a human reviewer.

One row per product, columns Steve can act on:
  decode_group · title · sku · sku_prefix · mpn_barcode · product_type · tags ·
  partial_signal · why_ambiguous · storefront_link · real_manufacturer(BLANK)

Ordering: easiest decodes first (recognizable SKU prefix / brand-ish tag / clear
title) -> harder -> true unknowns (no SKU, generic title) last. The 7 SCN
locker/site-furnishing rows are bucketed on their own and flagged
"NEEDS SUPPLIER INVOICE".

NO Shopify writes. GET only.
Output: data/reports/bbi-ambiguous-review-2026-06-02.csv
"""
import json, re, csv, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
GQL = f'https://{SHOP}/admin/api/2024-10/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
STOREFRONT = 'https://www.brantbusinessinteriors.com/products/'

EVIDENCE = ROOT / 'data/reports/bbi-resourcing-2026-06-02-evidence.json'
OUT = ROOT / 'data/reports/bbi-ambiguous-review-2026-06-02.csv'


def gql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers=HDR, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    if 'errors' in d:
        raise RuntimeError(json.dumps(d['errors'], indent=2))
    return d['data']


NODE_Q = """
query($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on Product {
      legacyResourceId handle title productType tags
      variants(first: 50) { edges { node { sku barcode } } }
    }
  }
}
"""


def fetch_live(ids):
    """Read-only batched GET of product_type / tags / sku / barcode."""
    live = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        gids = [f'gid://shopify/Product/{pid}' for pid in chunk]
        for n in gql(NODE_Q, {'ids': gids})['nodes']:
            if not n:
                continue
            skus = [v['node'].get('sku') or '' for v in n['variants']['edges']]
            bcs = [v['node'].get('barcode') or '' for v in n['variants']['edges']]
            live[str(n['legacyResourceId'])] = {
                'product_type': n.get('productType') or '',
                'tags': n.get('tags') or [],
                'sku': next((s.strip() for s in skus if s.strip()), ''),
                'barcode': next((b.strip() for b in bcs if b.strip()), ''),
            }
        print(f'  fetched {min(i + 50, len(ids))}/{len(ids)}', file=sys.stderr)
    return live


# Tags that hint at a real manufacturer/brand (decode boost). Loose, human-reviewed downstream.
BRAND_TAG_RX = re.compile(r'^(brand|manufacturer|mfg|vendor)[:=]', re.I)
# The brand:brant-business-interiors / brant tag IS the data error we're fixing — never a signal.
BBI_TAG_RX = re.compile(r'(brant[\s-]*business|brant-business-interiors|^brand:bbi$|brand:brant)', re.I)


def real_brand_tags(tags_list):
    return [t for t in tags_list if BRAND_TAG_RX.match(t) and not BBI_TAG_RX.search(t)]


def derive_prefix(sku):
    """Display prefix: alpha leading token, '(numeric)' for code-led SKUs, '(none)' if no SKU."""
    if not sku:
        return '(none)'
    m = re.match(r'^([A-Za-z]{2,})', sku)
    if m:
        return m.group(1).upper()
    return '(numeric)'


def difficulty(row):
    """Lower = easier to decode, sorts to the top. SCN bucketed separately (90)."""
    pref = row['sku_prefix']
    has_sku = bool(row['sku'])
    has_barcode = bool(row['mpn_barcode'])
    brandish_tag = bool(real_brand_tags(row['_tags_list']))
    # 90: SCN — known prefix but locked-undecoded, needs invoice (own bucket, after decodables)
    if pref == 'SCN':
        return 90
    # 0: strongest paper trail — a barcode/MPN or an explicit (non-BBI) brand tag
    if has_barcode or brandish_tag:
        return 0
    # 10: a real alphabetic SKU prefix to look up (e.g. BURO, WS, RDL, TEK...)
    if has_sku and pref not in ('(none)', '(numeric)'):
        return 10
    # 20: has a SKU but prefix is weak/numeric-led
    if has_sku:
        return 20
    # 30: no SKU but a descriptive title carrying a product-line word
    title = row['title'].lower()
    if len(re.sub(r'[^a-z]', '', title)) > 12 and not re.match(r'^(workstation|desk|chair|table|locker)s?\b', title):
        return 30
    # 99: true unknown — no SKU, generic title
    return 99


def why_ambiguous(row):
    pref = row['sku_prefix']
    if pref == 'SCN':
        return ('SKU prefix SCN = lockers / recycled-plastic site furnishings; this is a '
                'distributor/category code, not a single OEM. Maps to multiple possible '
                'manufacturers — NEEDS SUPPLIER INVOICE to confirm.')
    bits = []
    if not row['sku']:
        bits.append('no SKU on any variant')
    elif pref not in ('(none)', '(numeric)'):
        bits.append(f"SKU prefix '{pref}' not in the locked prefix->manufacturer lookup")
    else:
        bits.append(f"SKU '{row['sku']}' is code/numeric-led with no manufacturer prefix")
    if not row['product_type']:
        bits.append('no product_type set')
    if not real_brand_tags(row['_tags_list']):
        bits.append('no brand tag (only category/oecm tags)')
    bits.append('no manufacturer name in title/body')
    return '; '.join(bits) + '.'


def partial_signal(row):
    sig = []
    if row['sku_prefix'] not in ('(none)', '(numeric)'):
        sig.append(f"prefix={row['sku_prefix']}")
    elif row['sku']:
        sig.append(f"code-led SKU={row['sku']}")
    if row['mpn_barcode']:
        sig.append(f"barcode/MPN={row['mpn_barcode']}")
    if row['product_type']:
        sig.append(f"type={row['product_type']}")
    brand_tags = real_brand_tags(row['_tags_list'])
    if brand_tags:
        sig.append('tag:' + ','.join(brand_tags))
    return ' · '.join(sig) if sig else '(no usable signal)'


def main():
    data = json.loads(EVIDENCE.read_text())
    amb = [r for r in data if r['classification'] == 'AMBIGUOUS']
    assert len(amb) == 87, f'expected 87 ambiguous, got {len(amb)}'

    ids = [r['product_id'] for r in amb]
    print(f'Fetching live product_type/tags/barcode for {len(ids)} products (READ-ONLY)...',
          file=sys.stderr)
    live = fetch_live(ids)

    rows = []
    for r in amb:
        lv = live.get(r['product_id'], {})
        tags_list = lv.get('tags', [])
        sku = lv.get('sku') or r.get('sku_sample') or ''
        row = {
            'title': r['current_title'],
            'sku': sku,
            'sku_prefix': derive_prefix(sku),
            'mpn_barcode': lv.get('barcode', '') or r.get('barcode_sample', ''),
            'product_type': lv.get('product_type', '') or r.get('product_type', ''),
            '_tags_list': tags_list,
            'tags': '; '.join(tags_list),
            'handle': r['product_handle'],
            'body_excerpt': (r.get('current_body_first_200') or '').strip()[:160],
        }
        row['storefront_link'] = STOREFRONT + row['handle']
        row['partial_signal'] = partial_signal(row)
        row['why_ambiguous'] = why_ambiguous(row)
        row['_diff'] = difficulty(row)
        rows.append(row)

    GROUP_LABEL = {
        0: 'A · paper-trail (MPN/brand tag)',
        10: 'B · decodable SKU prefix',
        20: 'C · has SKU, weak prefix',
        30: 'D · descriptive title only',
        90: 'E · SCN — NEEDS SUPPLIER INVOICE',
        99: 'F · true unknown (no SKU, generic title)',
    }
    # easiest first; SCN (90) before true-unknown (99); stable secondary sort by prefix then title
    rows.sort(key=lambda x: (x['_diff'], x['sku_prefix'], x['title'].lower()))

    cols = ['decode_group', 'title', 'sku', 'sku_prefix', 'mpn_barcode',
            'product_type', 'tags', 'partial_signal', 'why_ambiguous',
            'body_excerpt', 'storefront_link', 'real_manufacturer']
    with OUT.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for x in rows:
            w.writerow({
                'decode_group': GROUP_LABEL[x['_diff']],
                'title': x['title'],
                'sku': x['sku'],
                'sku_prefix': x['sku_prefix'],
                'mpn_barcode': x['mpn_barcode'],
                'product_type': x['product_type'],
                'tags': x['tags'],
                'partial_signal': x['partial_signal'],
                'why_ambiguous': x['why_ambiguous'],
                'body_excerpt': x['body_excerpt'],
                'storefront_link': x['storefront_link'],
                'real_manufacturer': '',  # BLANK for Steve
            })

    from collections import Counter
    counts = Counter(GROUP_LABEL[x['_diff']] for x in rows)
    print(f'\nWrote {len(rows)} rows -> {OUT}', file=sys.stderr)
    for g in sorted(counts):
        print(f'  {counts[g]:>3}  {g}', file=sys.stderr)


if __name__ == '__main__':
    main()
