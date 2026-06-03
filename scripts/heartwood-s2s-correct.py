#!/usr/bin/env python3
"""
Heartwood electric sit-to-stand PDP spec correction (Tier-1 only).
Corrects four datasheet-confirmed overstatements on the two SKUs that carry all
four exact values: the 5-size desk (9687458873657) and the Cleo CLI-E1 base
(9842444271929 — same electric base, sold base-only).

Corrections:
  warranty  "15-year mechanical/structural"  -> 2-year electrical / 5-year steel structure
  stages    "3-stage"                         -> "2-stage"
  height    22"-47.5"                          -> 27.5"-45.5"
  speed     1.2"/sec                           -> 1"/sec

Does NOT touch origin ("Canadian-made" / "Built in Kelowna") — flagged separately.
Dry run by default. Pass --live to write.
"""
import os, sys, json, urllib.request, urllib.error

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
API = f'https://{STORE}/admin/api/2026-04'
LIVE = '--live' in sys.argv

def get(url):
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def put(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method='PUT', headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

# (old, new) substring pairs applied to scalar strings or to each list element.
A = 9687458873657
A_BODY = [
 ('heavy-duty 3-stage steel frame, giving each leg consistent, stable travel from 22" to 47.5"',
  'heavy-duty 2-stage steel frame, giving each leg consistent, stable travel from 27.5" to 45.5"'),
 ('The actuator moves at 1.2" per second', 'The actuator moves at 1" per second'),
 ('backed by a limited lifetime warranty on laminates and a 15-year warranty on the mechanical components,',
  'backed by a limited lifetime warranty on laminates, a 2-year electrical warranty, and a 5-year steel-structure warranty,'),
 ('<li>Height range: 22" – 47.5" (not including 1" top).</li>',
  '<li>Height range: 27.5" – 45.5" (not including 1" top).</li>'),
 ('<li>Heavy-duty 3-stage steel frame with dual synchronized motor driving each leg.</li>',
  '<li>Heavy-duty 2-stage steel frame with dual synchronized motor driving each leg.</li>'),
 ('<li>Operating speed: 1.2" per second; noise level under 55 dB.</li>',
  '<li>Operating speed: 1" per second; noise level under 55 dB.</li>'),
 ('<li>CSA/UL Certified; limited lifetime warranty on laminates, 15-year warranty on frame components.</li>',
  '<li>CSA/UL Certified; limited lifetime warranty on laminates, 2-year electrical warranty and 5-year steel-structure warranty.</li>'),
]
A_MF = {
 44198655131961: [('22"–47.5"', '27.5"–45.5"'), ('3-stage', '2-stage')],
 52945455939897: [('height range 22" to 47.5"', 'height range 27.5" to 45.5"')],
 52945456005433: [('3-stage', '2-stage')],
 52945456070969: [('1.2 inches per second adjustment speed', '1 inch per second adjustment speed')],
 52945456136505: [('15-year mechanical components warranty', '2-year electrical and 5-year steel-structure warranty')],
}

B = 9842444271929
B_BODY = [
 ('A commercial-grade Canadian-made sit-stand base with a 15-year structural warranty —',
  'A commercial-grade Canadian-made sit-stand base with a 5-year steel-structure warranty —'),
 ('The Heartwood Cleo CLI-E1 is a 3-stage, 2-leg electric',
  'The Heartwood Cleo CLI-E1 is a 2-stage, 2-leg electric'),
 ('Height adjusts from 22" to 47.5"H (without top) at 1.2" per second',
  'Height adjusts from 27.5" to 45.5"H (without top) at 1" per second'),
 ('Built in Kelowna, British Columbia — 15-year structural warranty and 7-year mechanical warranty on all base components.',
  'Built in Kelowna, British Columbia — 5-year steel-structure warranty and 2-year electrical warranty on all base components.'),
]
B_MF = {
 44198686196025: [('Three-stage', 'Two-stage'), ('1.2 in/sec', '1 in/sec')],
 52946255806777: [('22"–47.5"H', '27.5"–45.5"H')],
 52946255872313: [('3-stage', '2-stage')],
 52946255937849: [
    ('3-stage electric height adjustment: 22"–47.5"H (excluding top)',
     '2-stage electric height adjustment: 27.5"–45.5"H (excluding top)'),
    ('Whisper quiet <55 dB; operates at 1.2" per second',
     'Whisper quiet <55 dB; operates at 1" per second'),
    ('15-year structural warranty; 7-year mechanical warranty',
     '5-year steel-structure warranty; 2-year electrical warranty'),
 ],
 52946256003385: [('15-year structural warranty; 7-year mechanical warranty',
                   '5-year steel-structure warranty; 2-year electrical warranty')],
}

FORBIDDEN = ['15-year', '15 year', '3-stage', 'Three-stage', 'three-stage', '47.5', '1.2']

def apply_pairs(s, pairs, label):
    out = s
    for old, new in pairs:
        if old not in out:
            raise SystemExit(f'  ABORT [{label}]: expected substring not found:\n    {old!r}')
        out = out.replace(old, new)
    return out

def process_product(pid, body_pairs, mf_edits):
    p = get(f'{API}/products/{pid}.json')['product']
    mfs = {m['id']: m for m in get(f'{API}/products/{pid}/metafields.json')['metafields']}
    print(f'\n{"="*90}\n{pid} | {p["title"]}')

    # body
    new_body = apply_pairs(p['body_html'], body_pairs, f'{pid} body')
    print('  BODY: applied', len(body_pairs), 'replacements')
    for tok in FORBIDDEN:
        if tok in new_body:
            raise SystemExit(f'  ABORT: forbidden token still in body after edit: {tok!r}')

    # metafields
    mf_payloads = []
    for mid, pairs in mf_edits.items():
        m = mfs[mid]; val = m['value']; typ = m['type']
        if typ.startswith('list.'):
            lst = json.loads(val)
            newlst = []
            hit = False
            for el in lst:
                ne = el
                for old, new in pairs:
                    if old in ne:
                        ne = ne.replace(old, new); hit = True
                newlst.append(ne)
            if not hit:
                raise SystemExit(f'  ABORT mf {m["namespace"]}.{m["key"]}: no element matched any pair')
            newval = json.dumps(newlst, ensure_ascii=False, separators=(',', ':'))
        else:
            newval = apply_pairs(val, pairs, f'{m["namespace"]}.{m["key"]}')
        # forbidden check on edited mf value
        for tok in FORBIDDEN:
            if tok in newval:
                raise SystemExit(f'  ABORT: forbidden token {tok!r} still in {m["namespace"]}.{m["key"]} after edit')
        print(f'  MF {m["namespace"]}.{m["key"]}:')
        print(f'      - {val[:160]}')
        print(f'      + {newval[:160]}')
        mf_payloads.append((mid, typ, newval))

    if LIVE:
        put(f'{API}/products/{pid}.json', {'product': {'id': pid, 'body_html': new_body}})
        print('  ** body_html PUT (live)')
        for mid, typ, newval in mf_payloads:
            put(f'{API}/metafields/{mid}.json', {'metafield': {'id': mid, 'value': newval, 'type': typ}})
            print(f'  ** metafield {mid} PUT (live)')
    else:
        print('  (dry run — no writes)')

print('MODE:', 'LIVE WRITE' if LIVE else 'DRY RUN')
process_product(A, A_BODY, A_MF)
process_product(B, B_BODY, B_MF)
print('\nDone.')
