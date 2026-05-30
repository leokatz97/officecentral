#!/usr/bin/env python3
"""Pull full current Admin state for the B4S2 batch (ground truth before enrichment).
Reads /tmp/b4s2-batch.json (product_ids), writes /tmp/b4s2-state.json.
Read-only — no writes."""
import json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / '.env'
TOKEN = next((l.split('=',1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
SHOP = 'office-central-online.myshopify.com'
REST = f'https://{SHOP}/admin/api/2024-10'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

def rest(path):
    req = urllib.request.Request(f'{REST}{path}', headers=HDR, method='GET')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

batch = json.loads(Path('/tmp/b4s2-batch.json').read_text())
out = []
for b in batch:
    pid = b['product_id']
    p = rest(f'/products/{pid}.json')['product']
    mf = rest(f'/products/{pid}/metafields.json').get('metafields', [])
    imgs = p.get('images', [])
    out.append({
        'product_id': pid,
        'handle': p['handle'],
        'title': p['title'],
        'vendor': p['vendor'],
        'product_type': p['product_type'],
        'tags': p['tags'],
        'status': p['status'],
        'body_html': p.get('body_html') or '',
        'variants': [{'id': v['id'], 'title': v['title'], 'price': v['price'], 'sku': v.get('sku'),
                      'inventory_quantity': v.get('inventory_quantity'),
                      'inventory_policy': v.get('inventory_policy')} for v in p.get('variants', [])],
        'options': [{'name': o['name'], 'values': o['values']} for o in p.get('options', [])],
        'image_count': len(imgs),
        'first_image': (imgs[0]['src'] if imgs else None),
        'first_image_alt': (imgs[0].get('alt') if imgs else None),
        'first_image_id': (imgs[0]['id'] if imgs else None),
        'metafields_specs': {m['key']: m['value'] for m in mf if m['namespace'] == 'specs'},
        'metafields_all_ns': sorted({m['namespace'] for m in mf}),
        'seo_title': next((m['value'] for m in mf if m['namespace']=='global' and m['key']=='title_tag'), None),
        'seo_desc': next((m['value'] for m in mf if m['namespace']=='global' and m['key']=='description_tag'), None),
    })
    print(f"  pulled {p['handle']}: vendor={p['vendor']!r} status={p['status']} "
          f"variants={len(p.get('variants',[]))} imgs={len(imgs)} specs_mf={len([m for m in mf if m['namespace']=='specs'])}")

Path('/tmp/b4s2-state.json').write_text(json.dumps(out, indent=2))
print('written /tmp/b4s2-state.json')
