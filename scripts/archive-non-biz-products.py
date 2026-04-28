"""
PB-1 + PB-2: Sector cleanup for the Business-Furniture-only scope (2026-04-25).

Reads two CSVs and applies the dispositions via Shopify Admin API:
  - data/reports/sector-products-disposition-2026-04-28.csv (29 products)
      ARCHIVE   → status=archived (zero sold history, 27 products)
      UNPUBLISH → published=false, status stays active (sold history, 2 products)
  - data/redirects/sector-collections-redirects-2026-04-28.csv (15 collections)
      All collections in the "Redirect from" column → unpublish (published_at=null).
      Unpublish (not delete) is reversible and triggers the imported 301 redirects.

Dry-run by default. Pass --live to mutate. Logs every API response to data/logs/.
"""
import csv, json, os, sys, time
from datetime import datetime
from urllib import request as urlreq, error as urlerr

LIVE = '--live' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'

PRODUCTS_CSV = os.path.join(ROOT, 'data/reports/sector-products-disposition-2026-04-28.csv')
COLLECTIONS_CSV = os.path.join(ROOT, 'data/redirects/sector-collections-redirects-2026-04-28.csv')
LOG_DIR = os.path.join(ROOT, 'data/logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, f'archive-sector-{datetime.utcnow().strftime("%Y%m%dT%H%M%S")}.json')

log = []

def api_call(method, path, body=None):
    url = f'{API}/{path}'
    data = json.dumps(body).encode() if body else None
    req = urlreq.Request(url, data=data, method=method, headers={
        'X-Shopify-Access-Token': TOKEN,
        'Content-Type': 'application/json',
    })
    try:
        with urlreq.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode() or '{}')
    except urlerr.HTTPError as e:
        return e.code, {'error': e.read().decode()}

def fetch_all(path):
    items, url = [], f'{API}/{path}'
    while url:
        req = urlreq.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
        with urlreq.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            items.extend(data[list(data.keys())[0]])
            link = resp.headers.get('Link', '')
            import re
            m = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = m.group(1) if m else None
    return items

# ── PRODUCTS ────────────────────────────────────────────────────────────────
print('\n═══ PRODUCTS — resolving handles to IDs ═══')
target_handles = {}
with open(PRODUCTS_CSV) as f:
    for row in csv.DictReader(f):
        target_handles[row['handle']] = row['disposition']

print(f'Loaded {len(target_handles)} target handles from CSV')
all_products = fetch_all('products.json?fields=id,handle,status,published_at&limit=250')
handle_to_product = {p['handle']: p for p in all_products if p['handle'] in target_handles}
print(f'Matched {len(handle_to_product)}/{len(target_handles)} live products')

print(f'\n═══ PRODUCTS — applying dispositions ({"LIVE" if LIVE else "DRY-RUN"}) ═══')
for handle, disp in sorted(target_handles.items()):
    p = handle_to_product.get(handle)
    if not p:
        print(f'  [SKIP    ] {handle}  (not found live)')
        log.append({'kind': 'product', 'handle': handle, 'action': 'skip-not-found'})
        continue
    pid = p['id']
    if disp == 'ARCHIVE':
        body = {'product': {'id': pid, 'status': 'archived'}}
        action = f'status: {p["status"]} → archived'
    elif disp == 'UNPUBLISH':
        body = {'product': {'id': pid, 'published': False}}
        action = f'published_at: {p["published_at"]} → null (status stays {p["status"]})'
    else:
        print(f'  [SKIP    ] {handle}  unknown disposition: {disp}')
        continue

    if LIVE:
        code, resp = api_call('PUT', f'products/{pid}.json', body)
        ok = '✓' if code == 200 else '✗'
        print(f'  [{disp:9s}] {handle:55s}  {ok} HTTP {code}')
        log.append({'kind': 'product', 'handle': handle, 'id': pid, 'disposition': disp, 'http': code, 'response_error': resp.get('error') if code != 200 else None})
        time.sleep(0.5)
    else:
        print(f'  [{disp:9s}] {handle:55s}  would: {action}')
        log.append({'kind': 'product', 'handle': handle, 'id': pid, 'disposition': disp, 'planned': action, 'dry_run': True})

# ── COLLECTIONS ─────────────────────────────────────────────────────────────
print('\n═══ COLLECTIONS — resolving handles to IDs ═══')
sector_collection_handles = set()
with open(COLLECTIONS_CSV) as f:
    for row in csv.reader(f):
        if not row or row[0].startswith('#') or row[0] == 'Redirect from':
            continue
        sector_collection_handles.add(row[0].replace('/collections/', ''))

print(f'Loaded {len(sector_collection_handles)} target collection handles from CSV')
custom = fetch_all('custom_collections.json?fields=id,handle,title,published_at&limit=250')
smart = fetch_all('smart_collections.json?fields=id,handle,title,published_at&limit=250')
matched = []
for c in custom:
    if c['handle'] in sector_collection_handles:
        matched.append(('custom_collections', c))
for c in smart:
    if c['handle'] in sector_collection_handles:
        matched.append(('smart_collections', c))
print(f'Matched {len(matched)}/{len(sector_collection_handles)} live collections')

print(f'\n═══ COLLECTIONS — unpublishing ({"LIVE" if LIVE else "DRY-RUN"}) ═══')
for endpoint, c in sorted(matched, key=lambda x: x[1]['handle']):
    cid = c['id']
    body = {endpoint[:-1]: {'id': cid, 'published': False}}
    action = f'published_at: {c["published_at"]} → null'
    if LIVE:
        code, resp = api_call('PUT', f'{endpoint}/{cid}.json', body)
        ok = '✓' if code == 200 else '✗'
        print(f'  [UNPUBLISH] /collections/{c["handle"]:50s}  {ok} HTTP {code}')
        log.append({'kind': 'collection', 'handle': c['handle'], 'id': cid, 'http': code, 'response_error': resp.get('error') if code != 200 else None})
        time.sleep(0.5)
    else:
        print(f'  [UNPUBLISH] /collections/{c["handle"]:50s}  would: {action}')
        log.append({'kind': 'collection', 'handle': c['handle'], 'id': cid, 'planned': action, 'dry_run': True})

# ── LOG ─────────────────────────────────────────────────────────────────────
with open(LOG_PATH, 'w') as f:
    json.dump({'live': LIVE, 'timestamp': datetime.utcnow().isoformat() + 'Z', 'entries': log}, f, indent=2)
print(f'\nLog → {LOG_PATH}')
if not LIVE:
    print('\nDRY-RUN complete. Re-run with --live to apply.')
