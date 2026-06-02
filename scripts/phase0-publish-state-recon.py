#!/usr/bin/env python3
"""
COLLECTIONS Publish-State Reconciliation — Phase 0 (READ-ONLY).

Pulls, for every source handle in scope:
  - REST published_at (published state)
  - GraphQL productsCount
  - live redirect-map entry (does a /collections/<h> redirect exist + target)
  - live storefront HTTP status + redirect target (throttled curl, 4s spacing)

NO writes. Emits a JSON + a console table.
"""
import json, os, time, urllib.request, urllib.error, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = {}
with open(os.path.join(ROOT, '.env')) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k] = v

TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

def rest_get(path):
    url = f'{API}/{path}'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        link = r.headers.get('Link', '')
        return json.loads(r.read().decode()), link

def gql(query):
    url = f'{API}/graphql.json'
    data = json.dumps({'query': query}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

# ---- 1. Pull ALL collections (smart + custom), index by handle ----
def pull_all(kind):
    out = {}
    path = f'{kind}.json?limit=250'
    while path:
        data, link = rest_get(path)
        key = kind  # smart_collections / custom_collections
        for c in data.get(key, []):
            out[c['handle']] = {
                'id': c['id'],
                'title': c['title'],
                'published_at': c.get('published_at'),
                'kind': 'smart' if kind == 'smart_collections' else 'custom',
            }
        # pagination via Link header
        nxt = None
        for part in link.split(','):
            if 'rel="next"' in part:
                start = part.find('<') + 1
                end = part.find('>')
                nxt = part[start:end].replace(f'{API}/', '')
        path = nxt
    return out

print('Pulling all collections (smart + custom)...', file=sys.stderr)
collections = {}
collections.update(pull_all('smart_collections'))
collections.update(pull_all('custom_collections'))
print(f'  indexed {len(collections)} collections', file=sys.stderr)

# ---- 2. Pull full redirect map (paginated) ----
print('Pulling redirect map...', file=sys.stderr)
redirects = {}
path = 'redirects.json?limit=250'
while path:
    data, link = rest_get(path)
    for r in data.get('redirects', []):
        redirects[r['path']] = r['target']
    nxt = None
    for part in link.split(','):
        if 'rel="next"' in part:
            start = part.find('<') + 1
            end = part.find('>')
            nxt = part[start:end].replace(f'{API}/', '')
    path = nxt
print(f'  {len(redirects)} redirect entries', file=sys.stderr)

# ---- 3. Scope lists ----
LANDING_SOURCES = ['reception', 'boardroom-conference-meeting', 'healthcare-seating', 'executive-desks']
RESCUE = ['benching-desks', 'coat-racks-accessories', 'modesty-panels', 'picnic-tables']
HOLD = ['keilhauer']
# Phase 2 batch-1 consolidate-away sources (published state + redirect-exists only)
BATCH1 = [
    'acoustic-panels','active-seating','beam-seating','bench-seating','boardroom-seating',
    'boardroom-storage','conference-seating','ergonomic-accessories','executive-seating',
    'high-density-storage','mobile-storage','personal-storage','privacy-screens','wall-storage',
    'type-chairs','type-desks','type-tables','type-storage','type-accessories','type-lounge',
    'type-outdoor','room-boardroom','room-reception','room-accessories','room-private-office',
    'room-open-plan','room-lounge','room-training-room',
    'pedestal-drawers','pedestal-drawers-1','fire-resistant-file-cabinets',
    'fire-resistant-file-cabinets-safes','fire-resistant-safes','keilhauer',
]
# targets to verify resolve 200
TARGETS = ['reception-desks-desks','boardroom','desks','storage','tables','panels-room-dividers',
           'seating','accessories','ergonomic-products','business-furniture','training-flip-top-tables',
           'pedestal-drawers-storage','fire-resistant-file-cabinets-storage','fire-resistant-safes-storage']

ALL_DETAIL = LANDING_SOURCES + RESCUE + HOLD  # full read (count too)

# ---- 4. GraphQL productsCount per detailed handle ----
def products_count(handle):
    q = '{ collectionByHandle(handle: "%s") { id title productsCount { count } } }' % handle
    res = gql(q)
    c = res.get('data', {}).get('collectionByHandle')
    if not c:
        return None
    return c['productsCount']['count']

# ---- 5. Throttled storefront curl ----
def storefront(handle, is_page=False):
    path = f'/pages/{handle}' if is_page else f'/collections/{handle}'
    url = f'https://{STORE.replace(".myshopify.com","")}'  # placeholder; use canonical domain
    # Use the public domain
    base = 'https://www.brantbusinessinteriors.com'
    full = base + path
    try:
        out = subprocess.run(
            ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code} %{redirect_url}', full],
            capture_output=True, text=True, timeout=30
        )
        return out.stdout.strip()
    except Exception as e:
        return f'ERR {e}'

def detail_row(handle):
    meta = collections.get(handle)
    pub = None
    if meta:
        pub = 'Y' if meta['published_at'] else 'N'
    cnt = products_count(handle)
    redir = redirects.get(f'/collections/{handle}')
    time.sleep(4)
    sf = storefront(handle)
    return {
        'handle': handle,
        'in_collections_index': meta is not None,
        'kind': meta['kind'] if meta else None,
        'published': pub,
        'products': cnt,
        'redirect_target': redir,
        'storefront': sf,
    }

print('\n=== DETAILED READ (landing sources + rescue + hold) ===', file=sys.stderr)
detailed = []
for h in ALL_DETAIL:
    row = detail_row(h)
    detailed.append(row)
    print(json.dumps(row), file=sys.stderr)

# batch1: published + redirect-exists only (no count, no curl)
batch1 = []
for h in BATCH1:
    meta = collections.get(h)
    pub = ('Y' if meta['published_at'] else 'N') if meta else 'ABSENT'
    batch1.append({
        'handle': h,
        'published': pub,
        'redirect_exists': f'/collections/{h}' in redirects,
        'redirect_target': redirects.get(f'/collections/{h}'),
    })

# targets: storefront only
print('\n=== TARGET VERIFY (storefront 200, no chain) ===', file=sys.stderr)
targets = []
for h in TARGETS:
    time.sleep(4)
    sf = storefront(h)
    targets.append({'handle': h, 'storefront': sf})
    print(f'{h}: {sf}', file=sys.stderr)

# /pages/healthcare target
time.sleep(4)
hc = storefront('healthcare', is_page=True)
targets.append({'handle': 'pages/healthcare', 'storefront': hc})

out = {
    'generated': '2026-06-02',
    'redirect_count': len(redirects),
    'collections_indexed': len(collections),
    'detailed': detailed,
    'batch1': batch1,
    'targets': targets,
}
outpath = os.path.join(ROOT, 'data', 'reports', 'phase0-publish-state-2026-06-02.json')
with open(outpath, 'w') as f:
    json.dump(out, f, indent=2)
print(f'\nWrote {outpath}', file=sys.stderr)
print(json.dumps(out, indent=2))
