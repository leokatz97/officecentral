#!/usr/bin/env python3
"""
Spec-AUDIT dataset pull — comparison-target categories.

READ-ONLY. Pulls every active+published product via the GraphQL Admin API with
body_html, vendor, tags, collections, and the specs.* / global.* metafields the
audit needs. Categorizes each product into the 9 comparison-target categories
(tags + title keywords) and classifies datasheet-verifiability (real
specs.manufacturer + model_codes vs house-brand generic).

No writes of any kind. Output: data/reports/spec-audit-dataset-<date>.json

Usage: python3 scripts/audit-spec-pull.py
"""
import os, json, time, urllib.request, urllib.error, re

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
GQL = f'https://{STORE}/admin/api/2026-04/graphql.json'
DATE = '2026-06-03'
OUT = f'data/reports/spec-audit-dataset-{DATE}.json'

SPEC_KEYS = [
    'manufacturer', 'product_line', 'model_codes', 'dimensions',
    'weight_capacity', 'materials', 'finishes_available', 'key_features',
    'certifications', 'warranty', 'country_of_manufacture', 'who_its_for',
]

def gql(query, variables):
    body = json.dumps({'query': query, 'variables': variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req) as r:
                d = json.loads(r.read().decode())
            if 'errors' in d and any('THROTTLED' in str(e) for e in d['errors']):
                time.sleep(2 * (attempt + 1)); continue
            if 'errors' in d:
                raise SystemExit(f'GraphQL error: {d["errors"]}')
            return d['data']
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 * (attempt + 1)); continue
            raise
    raise SystemExit('GraphQL retries exhausted')

QUERY = '''
query($cursor: String) {
  products(first: 50, after: $cursor, query: "status:active published_status:published") {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      handle
      title
      vendor
      tags
      productType
      descriptionHtml
      collections(first: 30) { nodes { handle title } }
      metafields(first: 60) { nodes { namespace key value } }
    }
  }
}
'''

# ---- categorization ---------------------------------------------------------
# Each category: (name, required tag-or-None, title-keyword regex-or-None).
# A product matches a category if the tag matches (when given) AND/OR the title
# regex matches. Title regex is the discriminator for fine-grained categories.
CATS = [
    ('standing-desks', 'type:desks',
     r'sit[- ]?to[- ]?stand|sit[- ]?stand|standing|height[- ]?adjust|adjustable[- ]?(height|desk)|electric.*(desk|base)|crank'),
    ('task-ergonomic-chairs', 'type:chairs',
     r'task|ergonomic|operator|mesh|synchro|tilt'),
    ('executive-guest-seating', 'type:chairs',
     r'executive|guest|side chair|visitor|reception chair|conference chair|lounge'),
    ('big-tall-24hr-seating', 'type:chairs',
     r'big (and|&) tall|24[- ]?hour|24/7|intensive|heavy[- ]?duty|multi[- ]?shift|bariatric|500 ?lb|400 ?lb|350 ?lb'),
    ('conference-boardroom-tables', 'type:tables',
     r'conference|boardroom|meeting table|training table|flip[- ]?top'),
    ('reception', None,
     r'reception'),
    ('benching-workstations', None,
     r'benching|bench desk|workstation|panel system|cubicle|open[- ]?plan'),
    ('acoustic-pods', None,
     r'acoustic|pod|booth|phone booth|privacy|sound[- ]?(damp|absorb)|huddle'),
    ('storage-filing', 'type:storage',
     r'file|filing|cabinet|storage|pedestal|bookcase|lateral|locker|credenza'),
]

ROOM_TAG = {
    'reception': 'room:reception',
    'conference-boardroom-tables': 'room:boardroom',
    'benching-workstations': 'room:open-plan',
}


def categorize(title, tags):
    title_l = title.lower()
    tagset = set(tags)
    hits = []
    for name, req_tag, kw in CATS:
        tag_ok = (req_tag in tagset) if req_tag else False
        room_ok = ROOM_TAG.get(name) in tagset if name in ROOM_TAG else False
        kw_ok = bool(kw and re.search(kw, title_l))
        # fine-grained chair/desk cats need the title keyword; broad cats can match on tag/room
        if name in ('standing-desks', 'task-ergonomic-chairs', 'executive-guest-seating',
                    'big-tall-24hr-seating', 'conference-boardroom-tables'):
            if tag_ok and kw_ok:
                hits.append(name)
        elif name == 'storage-filing':
            if tag_ok or kw_ok:
                hits.append(name)
        else:  # reception, benching-workstations, acoustic-pods
            if kw_ok or room_ok:
                hits.append(name)
    return hits


HOUSE = {'brant business interiors', 'office central & brant business interiors',
         'office central', '', None}


def verifiability(mf):
    """Return (status, brand, models). Datasheet-verifiable requires a real
    manufacturer AND at least one model code."""
    man = (mf.get('specs.manufacturer') or '').strip()
    models_raw = mf.get('specs.model_codes') or ''
    models = []
    if models_raw:
        try:
            models = [m for m in json.loads(models_raw) if m and str(m).strip()]
        except Exception:
            models = [models_raw]
    man_real = man and man.lower() not in HOUSE
    if man_real and models:
        return 'datasheet-verifiable', man, models
    if man_real and not models:
        return 'brand-known-no-model', man, models
    return 'unverifiable-no-datasheet', man, models


def main():
    products, cursor = [], None
    while True:
        data = gql(QUERY, {'cursor': cursor})
        conn = data['products']
        products.extend(conn['nodes'])
        if not conn['pageInfo']['hasNextPage']:
            break
        cursor = conn['pageInfo']['endCursor']
        time.sleep(0.4)

    out = []
    for p in products:
        tags = p['tags']
        cats = categorize(p['title'], tags)
        if not cats:
            continue  # only keep comparison-target products
        mf = {}
        for m in p['metafields']['nodes']:
            mf[f"{m['namespace']}.{m['key']}"] = m['value']
        status, brand, models = verifiability(mf)
        specs = {k: mf.get(f'specs.{k}') for k in SPEC_KEYS if mf.get(f'specs.{k}')}
        out.append({
            'id': p['id'].split('/')[-1],
            'handle': p['handle'],
            'title': p['title'],
            'vendor': p['vendor'],
            'tags': tags,
            'categories': cats,
            'collections': [c['handle'] for c in p['collections']['nodes']],
            'verifiability': status,
            'brand': brand,
            'models': models,
            'specs': specs,
            'global_title_tag': mf.get('global.title_tag'),
            'global_description_tag': mf.get('global.description_tag'),
            'body_html': p['descriptionHtml'],
        })

    os.makedirs('data/reports', exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # summary
    from collections import Counter
    by_cat, by_ver = Counter(), Counter()
    for r in out:
        for c in r['categories']:
            by_cat[c] += 1
        by_ver[r['verifiability']] += 1
    print(f'Pulled {len(products)} products; {len(out)} in comparison-target categories.')
    print('--- by category (overlaps possible) ---')
    for k, v in by_cat.most_common():
        print(f'{v:4}  {k}')
    print('--- by verifiability ---')
    for k, v in by_ver.most_common():
        print(f'{v:4}  {k}')
    print(f'\nWrote {OUT}')


if __name__ == '__main__':
    main()
