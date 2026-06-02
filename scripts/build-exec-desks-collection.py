#!/usr/bin/env python3
"""
Build the executive-desks MANUAL collection (Collections-architecture, exec-desks Tier-1).

Approach (approved 2026-06-02, revised after live evidence):
  Every sibling desk sub-collection (l-shape-desks, u-shape-desks, straight-desks,
  office-suites-desks, height-adjustable-tables) is a MANUAL custom collection.
  The catalog tag schema is mid-migration/fragmented (type:desks vs type:desk vs
  type:workstation; segment:executive-office on only 1 product), so a smart rule has
  no reliable tag to hang on. We therefore build executive-desks the same way as its
  siblings: hand-curated.

  1. Reuse the empty UNPUBLISHED custom collection already at the handle (id below).
  2. Add 30 curated Tier-1 executive-grade desks as collects.
  3. Set SEO meta (global.title_tag, global.description_tag) + sort_order=best-selling.
  4. Publish.
  5. Hardened readback (Admin-API gate + cache-busted storefront curl).

Dry-run by default. Pass --live to write. Backs up to data/backups/, logs to data/logs/.

The executive-desks -> desks redirect was confirmed ABSENT in the live Admin map
(verified 2026-06-02), so the handle is free to serve 200. This script does NOT touch redirects.
"""
import os, sys, json, time, urllib.request, urllib.error, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = '--live' in sys.argv
STAMP = subprocess.check_output(['date', '+%Y%m%d-%H%M%S']).decode().strip()

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
STOREFRONT = 'https://www.brantbusinessinteriors.com'

HANDLE = 'executive-desks'
COLLECTION_ID = 526867005753  # existing empty unpublished custom collection at the handle
TITLE = 'Executive Desks'
TITLE_TAG = 'Executive Desks Ontario | Brant Business Interiors'
DESC_TAG = ('Executive desks for private offices — L-shape, U-shape & double-pedestal suites '
            'in commercial-grade laminate. OECM-eligible. Free CAD layout with every quote.')

# 30 curated Tier-1 executive-grade desk handles (approved set)
TIER1_HANDLES = [
    'u-shaped-suite-with-table-desk-72w-x-96d',
    'bow-front-desk-72x42',
    'desk-double-pedestal',
    'desk-l-shape-with-drawers',
    'desk-u-shape-mlp205-1',
    'executive-suites-height-adjustable-desk',
    'executive-u-shape-desk-set',
    'executive-workstation-10x10',
    'innovation-l-shape-curved-corner',
    'innovations-double-pedestal-desk-bf-bf-5-sizes-8-colours',
    'innovations-l-shape-desk-with-hutch',
    'innovations-u-shape-suite',
    'l-shape-desk-hutch',
    'l-shape-desk-8-sizes-9-colour-options-1',
    'l-shape-desk-8-sizes-9-colour-options-2',
    'l-shape-desk-8-sizes-9-colour-options',
    'l-shape-desk-set-72x72',
    'l-shape-desk-with-hutch',
    'l-shape-height-adjustable-desk-set',
    'l-shape-loop-leg-desk',
    'l-shape-suite-layout-41c',
    'l-shape-suire',
    'l-shape-workstations',
    'desk-single-pedestal-1',
    'offices-to-go-newland-l-shaped-suite-nlp420',
    'offices-to-go-newland-u-shaped-suites-nlp406',
    'u-shape-d-top-workstation',
    'u-shape-desk-nlp205',
    'u-shape-height-adjust-desk',
    'u-shape-height-adjustable-desk-suite-zira',
]


def rest(method, path, body=None):
    url = f'{API}/{path}'
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode()
            return (json.loads(raw) if raw.strip() else {}), r.status
    except urllib.error.HTTPError as e:
        return {'_error': e.read().decode()[:300]}, e.code


def gql(query):
    req = urllib.request.Request(f'{API}/graphql.json',
                                 data=json.dumps({'query': query}).encode(),
                                 headers=HEADERS, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def curl_status(url):
    out = subprocess.run(
        ['curl', '-sS', '-o', '/dev/null', '-D', '-', '-A', 'Mozilla/5.0', f'{url}?_cb={STAMP}'],
        capture_output=True, text=True)
    lines = out.stdout.splitlines()
    status = lines[0].strip() if lines else ''
    loc = next((l for l in lines if l.lower().startswith('location:')), '')
    return status, loc


def log(m): print(m, flush=True)


def main():
    mode = 'LIVE' if LIVE else 'DRY-RUN'
    log(f'=== build-exec-desks-collection.py [MANUAL/{mode}]  {STAMP} ===\n')

    # ---- Resolve the 30 handles against LIVE product state ----
    log('Resolving 30 Tier-1 handles against live catalog...')
    resolved, missing = [], []
    for h in TIER1_HANDLES:
        d, _ = rest('GET', f'products.json?handle={h}&fields=id,handle,title,status')
        prods = d.get('products', [])
        if not prods:
            missing.append(h); continue
        p = prods[0]
        if p.get('status') != 'active':
            log(f'  !! {h} status={p.get("status")} (not active)')
        resolved.append(p)
        log(f'  ok {p["id"]:>14}  {p["handle"]}')
    if missing:
        log('\n!! MISSING handles: ' + ', '.join(missing) + '\n   Aborting.')
        sys.exit(1)
    log(f'\nResolved {len(resolved)}/30 active products.')

    log('\nPlan:')
    log(f'  1. Reuse custom collection id={COLLECTION_ID} (handle={HANDLE}).')
    log(f'  2. Add {len(resolved)} collects.')
    log(f'  3. Set meta title_tag ({len(TITLE_TAG)}ch) + description_tag ({len(DESC_TAG)}ch), sort=best-selling.')
    log(f'  4. Publish.  5. Readback.')
    log(f'\n     title_tag   : {TITLE_TAG!r}')
    log(f'     description : {DESC_TAG!r}')

    if not LIVE:
        log('\n[DRY-RUN] No writes performed. Re-run with --live to execute.')
        return

    # ---- BACKUP ----
    bdir = os.path.join(ROOT, 'data', 'backups'); os.makedirs(bdir, exist_ok=True)
    col_before, _ = rest('GET', f'custom_collections/{COLLECTION_ID}.json')
    collects_before, _ = rest('GET', f'collects.json?collection_id={COLLECTION_ID}&limit=250')
    backup = {'stamp': STAMP, 'collection_before': col_before,
              'collects_before': collects_before.get('collects', []),
              'resolved': [{'id': p['id'], 'handle': p['handle']} for p in resolved]}
    bpath = os.path.join(bdir, f'exec-desks-build-{STAMP}.json')
    with open(bpath, 'w') as f: json.dump(backup, f, indent=2)
    log(f'\nBackup: {bpath}')

    existing_pids = {c['product_id'] for c in collects_before.get('collects', [])}
    logrec = {'stamp': STAMP, 'collects': [], 'meta': [], 'published': None, 'readback': {}}

    # ---- 1. ADD COLLECTS ----
    log('\n[1] Adding collects...')
    for p in resolved:
        if p['id'] in existing_pids:
            log(f'  skip (already in) {p["handle"]}'); continue
        d, st = rest('POST', 'collects.json',
                     {'collect': {'collection_id': COLLECTION_ID, 'product_id': p['id']}})
        logrec['collects'].append({'handle': p['handle'], 'status': st,
                                   'err': d.get('_error')})
        log(f'  + {p["handle"]} ({st})' + (f' ERR {d.get("_error")}' if d.get('_error') else ''))
        time.sleep(0.5)

    # ---- 2. META + sort + title ----
    log('\n[2] Setting sort + meta...')
    _, st = rest('PUT', f'custom_collections/{COLLECTION_ID}.json',
                 {'custom_collection': {'id': COLLECTION_ID, 'title': TITLE,
                                        'sort_order': 'best-selling'}})
    log(f'  sort_order=best-selling, title set ({st})')
    for key, val in (('title_tag', TITLE_TAG), ('description_tag', DESC_TAG)):
        d, st = rest('POST', f'collections/{COLLECTION_ID}/metafields.json',
                     {'metafield': {'namespace': 'global', 'key': key,
                                    'type': 'single_line_text_field', 'value': val}})
        logrec['meta'].append({'key': key, 'status': st, 'err': d.get('_error')})
        log(f'  set global.{key} ({st})' + (f' ERR {d.get("_error")}' if d.get('_error') else ''))
        time.sleep(0.5)

    # ---- 3. PUBLISH ----
    log('\n[3] Publishing...')
    d, st = rest('PUT', f'custom_collections/{COLLECTION_ID}.json',
                 {'custom_collection': {'id': COLLECTION_ID, 'published': True}})
    pub_at = d.get('custom_collection', {}).get('published_at')
    logrec['published'] = {'status': st, 'published_at': pub_at}
    log(f'  published ({st}) published_at={pub_at}')
    time.sleep(2.0)

    # ---- 4. HARDENED READBACK ----
    log('\n[4] Hardened readback...')
    rb = logrec['readback']
    d, _ = rest('GET', f'custom_collections.json?handle={HANDLE}')
    cc = (d.get('custom_collections') or [{}])[0]
    rb['admin'] = {'id': cc.get('id'), 'published_at': cc.get('published_at'),
                   'sort_order': cc.get('sort_order')}
    log(f'  Admin: id={cc.get("id")} published_at={cc.get("published_at")} sort={cc.get("sort_order")}')
    g = gql('{ collectionByHandle(handle: "%s") { productsCount { count } } }' % HANDLE)
    cnt = (((g.get('data') or {}).get('collectionByHandle') or {}).get('productsCount') or {}).get('count')
    rb['products_count'] = cnt
    log(f'  GraphQL productsCount = {cnt} (expected 30)')
    d, _ = rest('GET', f'collections/{COLLECTION_ID}/metafields.json')
    seo = {m['key']: m['value'] for m in d.get('metafields', []) if m['namespace'] == 'global'}
    rb['meta'] = {'title_tag': seo.get('title_tag'), 'description_tag': seo.get('description_tag')}
    log(f'  meta.title_tag       = {seo.get("title_tag")!r}')
    log(f'  meta.description_tag = {seo.get("description_tag")!r}')
    d, _ = rest('GET', f'redirects.json?path=/collections/{HANDLE}')
    rb['redirect_present'] = bool(d.get('redirects'))
    log(f'  redirect present? {rb["redirect_present"]} (expected False)')
    status, loc = curl_status(f'{STOREFRONT}/collections/{HANDLE}')
    rb['storefront'] = {'status': status, 'location': loc}
    log(f'  storefront: {status} {loc}')

    ldir = os.path.join(ROOT, 'data', 'logs'); os.makedirs(ldir, exist_ok=True)
    lpath = os.path.join(ldir, f'exec-desks-build-{STAMP}.json')
    with open(lpath, 'w') as f: json.dump(logrec, f, indent=2)
    log(f'\nLog: {lpath}')

    ok = (cnt == 30 and cc.get('published_at') and not rb['redirect_present'])
    log(f'\n=== {"PASS" if ok else "CHECK"} — count={cnt}, published={bool(cc.get("published_at"))}, '
        f'redirect_absent={not rb["redirect_present"]} ===')


if __name__ == '__main__':
    main()
