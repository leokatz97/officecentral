#!/usr/bin/env python3
"""ITEMS 3 & 4 — build the feed-exclusion list and the Steve vendor worklist.

READ-ONLY. Consumes the cached snapshot + feed-readiness JSON. Writes two CSVs.

Item 3: data/reports/feed-exclude-list-2026-06-05.csv
  - 23 ACTIVE $0-price B2B quote pages (price<=0)  -> reason: zero-price-quote-page
  - placeholder/option pages (all-null SKUs + option-word handle) -> reason: placeholder-option-page
  Google channel exclusion is publication-based; token lacks write_publications,
  so this list is for one-click "remove from Google & YouTube" in Admin.
  Placeholder rows additionally carry likely_nonproduct=YES (flag for Leo).

Item 4: data/reports/steve-vendor-worklist-2026-06-05.csv
  - ACTIVE products still vendored BBI/blank with no auto-resolving signal (AMBIGUOUS)
  - + all 5 NON-BBI-CONFLICT (a human set a real non-BBI brand that conflicts w/ SKU/mf)
  Columns include a blank "steve_real_manufacturer" for him to fill.
"""
import json, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = '2026-06-05'
snap = json.loads((ROOT / 'data' / 'reports' / f'_catalog-feed-snapshot-{DATE}.json').read_text())
fr = json.loads((ROOT / 'data' / 'reports' / f'feed-readiness-{DATE}.json').read_text())
P = snap['products']
byid = {p['legacyResourceId']: p for p in P}
byh = {p['handle']: p for p in P}


def mf(p):
    return {f"{e['node']['namespace']}.{e['node']['key']}": (e['node'].get('value') or '')
            for e in p['metafields']['edges']}


def skus(p):
    return [(e['node'].get('sku') or '').strip() for e in p['variants']['edges']]


def first_sku(p):
    for s in skus(p):
        if s:
            return s
    return ''


def brand_tag(p):
    for t in (p.get('tags') or []):
        if t.lower().startswith('brand:'):
            return t
    return ''


# ============ ITEM 3 — feed-exclusion list ============
fp = fr['feed_per_product']
zero = [byid[f['id']] for f in fp
        if f['status'] == 'ACTIVE' and any('price<=0' in e for e in f['errors'])]

# placeholder/option pages: ACTIVE, every variant SKU empty, option-word handle
OPTION_RX = re.compile(r'(please-select|caster-option|^colour$|^color$|select-a-|^finish$)', re.I)
placeholders = []
for p in P:
    if p['status'] != 'ACTIVE':
        continue
    h = p['handle']
    all_null = all(s == '' for s in skus(p))
    if all_null and OPTION_RX.search(h):
        placeholders.append(p)
# installation-1 is a service line-item placeholder — include explicitly if present & active
inst = byh.get('installation-1')
if inst and inst['status'] == 'ACTIVE' and inst not in placeholders:
    placeholders.append(inst)

ph_handles = {p['handle'] for p in placeholders}
rows3 = []
seen = set()
for p in zero + placeholders:
    if p['handle'] in seen:
        # if already added as zero, upgrade its placeholder flag
        continue
    seen.add(p['handle'])
    is_ph = p['handle'] in ph_handles
    reasons = []
    if p in zero:
        reasons.append('zero-price-quote-page')
    if is_ph:
        reasons.append('placeholder-option-page')
    rows3.append({
        'handle': p['handle'],
        'title': p.get('title', ''),
        'status': p['status'],
        'vendor': p.get('vendor', ''),
        'first_sku': first_sku(p),
        'variant_count': len(p['variants']['edges']),
        'reason': ' + '.join(reasons),
        'likely_nonproduct': 'YES' if is_ph else '',
    })
rows3.sort(key=lambda r: (r['likely_nonproduct'] != 'YES', r['handle']))
out3 = ROOT / 'data' / 'reports' / f'feed-exclude-list-{DATE}.csv'
with out3.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['handle', 'title', 'status', 'vendor', 'first_sku',
                                      'variant_count', 'reason', 'likely_nonproduct'])
    w.writeheader(); w.writerows(rows3)
print(f"Item 3 -> {out3.relative_to(ROOT)}  ({len(rows3)} rows: "
      f"{sum(1 for r in rows3 if 'zero-price' in r['reason'])} $0, "
      f"{sum(1 for r in rows3 if r['likely_nonproduct']=='YES')} placeholders)")


# ============ ITEM 4 — Steve vendor worklist ============
cand = fr['vendor_candidates']
worklist = []
for c in cand:
    cls = c['classification']
    if cls == 'NON-BBI-CONFLICT' or (cls == 'AMBIGUOUS' and c['status'] == 'ACTIVE'):
        p = byid.get(c['id'], {})
        m = mf(p) if p else {}
        sku = c.get('sku', '')
        ev_bits = []
        if c.get('prefix'):
            ev_bits.append(f"SKU prefix={c['prefix']}")
        if m.get('specs.manufacturer'):
            ev_bits.append(f"specs.manufacturer={m['specs.manufacturer']}")
        bt = brand_tag(p) if p else ''
        if bt:
            ev_bits.append(f"tag={bt}")
        ev_bits.append(c.get('evidence', ''))
        decodable = bool(sku.strip())
        worklist.append({
            'classification': cls,
            'group': 'decodable-but-uncertain' if decodable else 'no-SKU',
            'handle': c['handle'],
            'title': c.get('title', ''),
            'current_sku': sku,
            'current_vendor': c.get('current_vendor', ''),
            'conflicting_evidence': ' | '.join(b for b in ev_bits if b),
            'candidate_manufacturer': c.get('expected_vendor', ''),
            'steve_real_manufacturer': '',
        })

# sort: NON-BBI-CONFLICT first, then decodable-but-uncertain, then no-SKU; alpha within
order = {'NON-BBI-CONFLICT': 0, 'AMBIGUOUS': 1}
gorder = {'decodable-but-uncertain': 0, 'no-SKU': 1}
worklist.sort(key=lambda r: (order.get(r['classification'], 9), gorder.get(r['group'], 9), r['handle']))

out4 = ROOT / 'data' / 'reports' / f'steve-vendor-worklist-{DATE}.csv'
cols = ['classification', 'group', 'handle', 'title', 'current_sku', 'current_vendor',
        'conflicting_evidence', 'candidate_manufacturer', 'steve_real_manufacturer']
with out4.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(worklist)

from collections import Counter
cc = Counter(r['classification'] for r in worklist)
gc = Counter(r['group'] for r in worklist)
print(f"Item 4 -> {out4.relative_to(ROOT)}  ({len(worklist)} rows: {dict(cc)} | {dict(gc)})")
