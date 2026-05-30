#!/usr/bin/env python3
"""B4S1 enrichment writer — payload-driven, immediate-write (Option A).

Built for PHASE-A-BLOCK-4-SESSION-1 (brand:global validation batch, 2026-05-30).
Reusable for later Tier-B batches: hand it a payload JSON in the shape under
data/reports/b4s1-payloads/ and it backs up, writes (product fields + specs.*
metafields + image alt + manual collects), and verifies via Admin-API readback.

Usage:
  python3 scripts/push-b4s1-enrichment.py data/reports/b4s1-payloads/p1.json          # DRY RUN
  python3 scripts/push-b4s1-enrichment.py data/reports/b4s1-payloads/p1.json --live    # apply

Steps (live): backup -> productUpdate -> metafieldsSet -> image alt -> collects -> readback verify.
Backups: data/backups/  Logs: data/logs/  (both gitignored)
"""
import json, sys, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=',1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
SHOP = 'office-central-online.myshopify.com'
API = '2024-10'
REST = f'https://{SHOP}/admin/api/{API}'
GQL = f'{REST}/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

def gql(query, variables=None):
    req = urllib.request.Request(GQL, data=json.dumps({'query': query, 'variables': variables or {}}).encode(), headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read())
    if 'errors' in out:
        raise RuntimeError(f"GraphQL errors: {out['errors']}")
    return out['data']

def rest(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f'{REST}{path}', data=data, headers=HDR, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

PRODUCT_UPDATE = '''
mutation($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id title vendor productType tags descriptionHtml seo { title description } }
    userErrors { field message }
  }
}'''

METAFIELDS_SET = '''
mutation($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { namespace key value type }
    userErrors { field message }
  }
}'''

def main():
    if len(sys.argv) < 2:
        print('usage: _b4s1_write.py <payload.json> [--live]'); sys.exit(1)
    payload = json.loads(Path(sys.argv[1]).read_text())
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    pid = str(payload['product_id'])
    gid = f'gid://shopify/Product/{pid}'
    handle = payload['handle']

    print(f"=== B4S1 WRITE {'[LIVE]' if live else '[DRY RUN]'} : {handle} ({pid}) ===")

    # Step a — backup current state
    current = rest('GET', f'/products/{pid}.json')['product']
    cur_mf = rest('GET', f'/products/{pid}/metafields.json').get('metafields', [])
    backup = {'fetched': ts, 'product': current, 'metafields': cur_mf}
    bdir = ROOT / 'data/backups'; bdir.mkdir(exist_ok=True)
    bpath = bdir / f'b4s1-{handle}-pre-{ts}.json'
    if live:
        bpath.write_text(json.dumps(backup, indent=2))
        print(f"  backup -> {bpath}")
    else:
        print(f"  [dry] would back up to {bpath}")
    img_id = (current.get('image') or {}).get('id') or (current.get('images') or [{}])[0].get('id')

    # Build product input
    pinput = {
        'id': gid,
        'title': payload['title'],
        'descriptionHtml': payload['body_html'],
        'vendor': payload['vendor'],
        'productType': payload['product_type'],
        'tags': payload['tags'],
        'seo': {'title': payload['seo_title'], 'description': payload['seo_description']},
    }
    mf_input = [{'ownerId': gid, 'namespace': 'specs', 'key': m['key'],
                 'type': m['type'], 'value': m['value']} for m in payload['metafields']]

    if not live:
        print('  [dry] productUpdate input:')
        print('     title       :', pinput['title'])
        print('     vendor/type :', pinput['vendor'], '/', pinput['productType'])
        print('     tags        :', ', '.join(pinput['tags']))
        print('     seo.title   :', f"{pinput['seo']['title']} ({len(pinput['seo']['title'])} chars)")
        print('     seo.desc    :', f"{pinput['seo']['description']} ({len(pinput['seo']['description'])} chars)")
        print('     body_html   :', f"{len(pinput['descriptionHtml'])} chars")
        print(f'     image_alt   : {payload.get("image_alt")!r} (img_id={img_id})')
        print(f'  [dry] {len(mf_input)} metafields:')
        for m in mf_input:
            print(f"     specs.{m['key']:24s} [{m['type']:28s}] {m['value'][:70]}")
        print('  [dry] collects:', payload.get('collects', []))
        print('  DRY RUN complete — no writes.')
        return

    # Step b — productUpdate
    r = gql(PRODUCT_UPDATE, {'input': pinput})
    errs = r['productUpdate']['userErrors']
    if errs: raise RuntimeError(f'productUpdate userErrors: {errs}')
    print('  productUpdate OK')

    # Step b2 — metafieldsSet (chunks of 25)
    for i in range(0, len(mf_input), 25):
        r = gql(METAFIELDS_SET, {'metafields': mf_input[i:i+25]})
        errs = r['metafieldsSet']['userErrors']
        if errs: raise RuntimeError(f'metafieldsSet userErrors: {errs}')
    print(f'  metafieldsSet OK ({len(mf_input)} fields)')

    # Step b3 — image alt
    if img_id and payload.get('image_alt'):
        rest('PUT', f'/products/{pid}/images/{img_id}.json', {'image': {'id': img_id, 'alt': payload['image_alt']}})
        print('  image alt OK')

    # Step c — collects (manual collection assignment)
    for cid in payload.get('collects', []):
        try:
            rest('POST', '/collects.json', {'collect': {'product_id': int(pid), 'collection_id': int(cid)}})
            print(f'  collect -> collection {cid} OK')
        except urllib.error.HTTPError as e:
            print(f'  collect -> collection {cid} FAILED: {e.read().decode()[:200]}')

    # Step e — readback verify
    rb = gql('''{ product(id: "%s") { title vendor productType tags descriptionHtml
        seo { title description }
        metafields(first: 40, namespace: "specs") { edges { node { key value } } } } }''' % gid)['product']
    checks = []
    checks.append(('title', rb['title'] == payload['title']))
    checks.append(('vendor', rb['vendor'] == payload['vendor']))
    checks.append(('product_type', rb['productType'] == payload['product_type']))
    checks.append(('seo_title', rb['seo']['title'] == payload['seo_title']))
    checks.append(('seo_desc', rb['seo']['description'] == payload['seo_description']))
    checks.append(('body_html', rb['descriptionHtml'].strip() == payload['body_html'].strip()))
    checks.append(('tags', set(rb['tags']) == set(payload['tags'])))
    rb_mf = {e['node']['key']: e['node']['value'] for e in rb['metafields']['edges']}
    for m in payload['metafields']:
        checks.append((f"mf.{m['key']}", rb_mf.get(m['key']) == m['value']))
    allok = all(ok for _, ok in checks)
    print('  --- READBACK VERIFY ---')
    for name, ok in checks:
        print(f"    {'OK ' if ok else 'XX '} {name}")
    print(f"  READBACK: {'ALL MATCH' if allok else 'MISMATCH — INVESTIGATE'}")

    log = {'ts': ts, 'handle': handle, 'product_id': pid, 'checks': dict(checks), 'all_ok': allok,
           'backup': str(bpath)}
    ldir = ROOT / 'data/logs'; ldir.mkdir(exist_ok=True)
    lpath = ldir / f'b4s1-{handle}-{ts}.json'
    lpath.write_text(json.dumps(log, indent=2))
    print(f'  log -> {lpath}')
    if not allok: sys.exit(2)

if __name__ == '__main__':
    main()
