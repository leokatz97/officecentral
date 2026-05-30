#!/usr/bin/env python3
"""B4S4 Phase 3 — render the 20-product review batch as scannable cards."""
import json, re, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
drafts = {d['_n']: d for d in json.load(open('/tmp/b4s4-drafts.json'))}
PAY = ROOT / 'data/reports/b4s4-payloads'
state = {s['handle']: s for s in json.load(open('/tmp/b4s4-state.json'))}

# routing recipe by product_type (from brand-collection-routing.yaml Global block)
RECIPE = {
    'desk': ['gfg-desks', 'desks'],
    'lateral file cabinet': ['gfg-storage', 'storage-filing'],
    'storage cabinet': ['gfg-storage', 'storage-filing'],
    'lounge seating': ['gfg-chairs', 'lounge-seating'],
    'lounge chair': ['gfg-chairs', 'lounge-seating'],
    'task chair': ['gfg-chairs', 'task-chairs'],
}
NEWTYPES = {'workstation', 'panel system', 'flip-top table', 'bar stool', 'beam seating'}

def strip(h): return re.sub(r'\s+',' ', re.sub('<[^>]+>',' ', h or '')).strip()

for n in range(1, 21):
    d = drafts[n]; h = d['handle']
    pay = json.loads((PAY / f'p{n}.json').read_text())
    st = state[h]
    pt = d['product_type'].lower()
    recipe = RECIPE.get(pt)
    routing = f"brand_lookup -> {recipe}" if recipe else f"brand_lookup -> TAG-ONLY (new type '{d['product_type']}', no collection recipe yet)"
    print("\n" + "="*92)
    flag = ''
    if d.get('source_quality')=='REQUIRES_LEO_SOURCE': flag=' 🚩 REQUIRES_LEO_SOURCE'
    if d.get('boilerplate_corrupted'): flag+=' 🚩 BOILERPLATE(old body) — redrafted from source'
    print(f"  #{n}  {h}{flag}")
    print("="*92)
    print(f"  source_quality : {d.get('source_quality')}   |   source_url: {d.get('source_url')}")
    print(f"  routing        : {routing}")
    print(f"  missing fields : {d.get('missing') or '(none)'}")
    print(f"  OLD title      : {st['title']}")
    print(f"  NEW title      : {pay['title']}")
    print(f"  product_type   : {pay['product_type']}    vendor: {pay['vendor']}")
    print(f"  tags           : {', '.join(pay['tags'])}")
    print(f"  seo_title ({len(pay['seo_title'])}) : {pay['seo_title']}")
    print(f"  seo_desc  ({len(pay['seo_description'])}): {pay['seo_description']}")
    print(f"  image_alt      : {pay['image_alt']}")
    print(f"  --- body (rendered) ---")
    print("   ", strip(pay['body_html'])[:700])
    print(f"  --- metafields ({len(pay['metafields'])}) ---")
    for m in pay['metafields']:
        v = m['value']
        if m['type'].startswith('list.'):
            try: v = ' · '.join(json.loads(v))
            except: pass
        v = v.replace('\n',' / ')
        print(f"     specs.{m['key']:24s} {v[:120]}")
    if d.get('notes'):
        print(f"  NOTES: {d['notes'][:400]}")
