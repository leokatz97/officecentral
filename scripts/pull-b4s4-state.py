#!/usr/bin/env python3
"""B4S4 Phase 2.1 — pull full Admin state for the 20-product batch (read-only).
Reads /tmp/b4s4-batch.json, writes /tmp/b4s4-state.json."""
import json, urllib.request, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = next((l.split('=',1)[1].strip().strip('"').strip("'")
              for l in (ROOT/'.env').read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
SHOP = 'office-central-online.myshopify.com'
REST = f'https://{SHOP}/admin/api/2024-10'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

def rest(path):
    for attempt in range(6):
        try:
            req = urllib.request.Request(f'{REST}{path}', headers=HDR, method='GET')
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(0.6)  # ~2 calls/sec, well under REST bucket
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 * (attempt + 1)
                print(f"    429 — backing off {wait}s")
                time.sleep(wait)
                continue
            raise
    raise SystemExit(f"rate-limited repeatedly on {path}")

batch = json.loads(Path('/tmp/b4s4-batch.json').read_text())
out = []
for b in batch:
    pid = b['product_id']
    p = rest(f'/products/{pid}.json')['product']
    mf = rest(f'/products/{pid}/metafields.json').get('metafields', [])
    colls = rest(f'/products/{pid}/collects.json' if False else f'/collects.json?product_id={pid}&limit=250').get('collects', [])
    imgs = p.get('images', [])
    out.append({
        'product_id': pid, 'handle': p['handle'], 'title': p['title'],
        'vendor': p['vendor'], 'product_type': p['product_type'], 'tags': p['tags'],
        'status': p['status'], 'body_html': p.get('body_html') or '',
        'variants': [{'id': v['id'], 'title': v['title'], 'price': v['price'], 'sku': v.get('sku'),
                      'inventory_quantity': v.get('inventory_quantity'),
                      'inventory_policy': v.get('inventory_policy')} for v in p.get('variants', [])],
        'options': [{'name': o['name'], 'values': o['values']} for o in p.get('options', [])],
        'image_count': len(imgs), 'first_image': (imgs[0]['src'] if imgs else None),
        'first_image_alt': (imgs[0].get('alt') if imgs else None),
        'collection_ids': [c['collection_id'] for c in colls],
        'metafields_specs': {m['key']: m['value'] for m in mf if m['namespace'] == 'specs'},
        'metafields_all_ns': sorted({m['namespace'] for m in mf}),
        'seo_title': next((m['value'] for m in mf if m['namespace']=='global' and m['key']=='title_tag'), None),
        'seo_desc': next((m['value'] for m in mf if m['namespace']=='global' and m['key']=='description_tag'), None),
    })
    skus = ','.join(filter(None,[v.get('sku') for v in p.get('variants',[])]))
    print(f"  {b['n']:>2}. {p['handle'][:40]:42} vendor={p['vendor']!r} status={p['status']} "
          f"var={len(p.get('variants',[]))} skus=[{skus[:40]}] specs={len([m for m in mf if m['namespace']=='specs'])} "
          f"body={len(p.get('body_html') or '')}c")

Path('/tmp/b4s4-state.json').write_text(json.dumps(out, indent=2))
print('\nwritten /tmp/b4s4-state.json')
