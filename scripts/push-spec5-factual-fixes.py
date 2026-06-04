#!/usr/bin/env python3
"""
§5 factual-spec corrections (batch-fixable only) from
docs/reviews/spec-audit-comparison-categories-2026-06-03.md.

Scope: ONLY §5 factual mismatches that re-confirmed UNAMBIGUOUS against the
cited manufacturer datasheet (findings JSON). EXCLUDES §3 (warranty/origin/cert,
Steve-gated), §4 (config/wrong-model divergences), brand mis-tags, and every
row the audit hedged with verify/confirm/unless (the Heartwood lesson).

Usage:
  python3 scripts/push-spec5-factual-fixes.py            # DRY RUN (default)
  python3 scripts/push-spec5-factual-fixes.py --live     # apply to LIVE

Safety:
  - DRY RUN prints, per edit, MATCH / NO-MATCH against live content. Any
    NO-MATCH blocks that product from being written (no guessing).
  - --live backs up each product's full body_html + specs.* + global.* + seo
    to data/backups/spec5-<id>-<ts>.json BEFORE writing.
  - Hardened readback per product after write: every NEW value present, every
    OLD value gone, in the field it was changed. Mismatch => logged FAILED.
  - Logs every product outcome to data/logs/spec5-fixes-<ts>.json.
"""
import os, sys, json, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for line in (ROOT / '.env').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())
SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'
LIVE = '--live' in sys.argv
TS = datetime.now().strftime('%Y%m%d-%H%M%S')

DASH = '–'   # en dash
X = '×'      # multiplication sign


def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(2 * (attempt + 1)); continue
            raise


# Each product: body = [(old, new), ...] applied to descriptionHtml;
# meta = [(namespace, key, old, new), ...] substring-replace inside that metafield value.
EDITS = {
    '9699268591929': {  # Sidero — overall height 32->33"H
        'name': 'Sidero guest chair',
        'body': [],
        'meta': [('specs', 'dimensions',
                  '25.5"W x 24"D x 32"H (model 6900 standard arm chair)',
                  '25.5"W x 24"D x 33"H (model 6900 standard arm chair)')],
    },
    '9708357452089': {  # OTG10740 masi — weight 27.5 -> 33 lbs
        'name': 'OTG10740 masi high back tilter',
        'body': [("At 27.5 lbs it's light enough", "At 33 lbs it's light enough")],
        'meta': [('specs', 'weight', '27.5 lbs / 12.5 kg', '33 lbs / 15 kg')],
    },
    '9771515150649': {  # The Accord — seat height 18-22 -> 17-21; knee-tilt -> center-tilt
        'name': 'The Accord tilter high back chair',
        'body': [
            ('high-back knee-tilter', 'high-back center-tilter'),
            ('<li>Knee-tilt movement with waterfall seat edge and contoured cushions</li>',
             '<li>Center-tilt movement with waterfall seat edge and contoured cushions</li>'),
        ],
        'meta': [
            ('specs', 'dimensions',
             f'seat 20"W x 19"D x 18{DASH}22"H', f'seat 20"W x 19"D x 17{DASH}21"H'),
            ('specs', 'key_features',
             'Knee-tilt with waterfall seat edge and contoured cushions',
             'Center-tilt movement with waterfall seat edge and contoured cushions'),
            ('global', 'description_tag', 'Global Accord knee-tilter', 'Global Accord center-tilter'),
        ],
    },
    '9727967494457': {  # Vertical file 2dr — model MVL25201 -> 26-201; depth 25 -> 26.6 (body + meta tags only)
        'name': 'Vertical file 2 drawer letter',
        'body': [
            ('The MVL25201 is a 2-drawer', 'The 26-201 is a 2-drawer'),
            ('At 25" deep, it fits', 'At 26.6" deep, it fits'),
            ('<li>Model MVL25201: 2-drawer letter-width vertical file cabinet.</li>',
             '<li>Model 26-201: 2-drawer letter-width vertical file cabinet.</li>'),
            ('<li>25" depth fits standard filing positions',
             '<li>26.6" depth fits standard filing positions'),
        ],
        'meta': [
            ('global', 'title_tag',
             'MVL25201 2-Drawer Letter Vertical File', '26-201 2-Drawer Letter Vertical File'),
            ('global', 'description_tag',
             'The MVL25201 metal vertical file holds letter-width documents in 2 drawers with 25" depth',
             'The 26-201 metal vertical file holds letter-width documents in 2 drawers with 26.6" depth'),
        ],
    },
    '9727969984825': {  # 4dr vertical file — depth 25 -> 26.56; weight 112 -> 118 (body only)
        'name': '4 drawer letter width vertical file',
        'body': [
            (f'sized at 15.15"W {X} 25"D {X} 52"H and weighs 112 lbs',
             f'sized at 15.15"W {X} 26.56"D {X} 52"H and weighs 118 lbs'),
            (f'Dimensions: 15.15"W {X} 25"D {X} 52"H; weight 112 lbs / 50.8 kg.',
             f'Dimensions: 15.15"W {X} 26.56"D {X} 52"H; weight 118 lbs / 53.5 kg.'),
        ],
        'meta': [],
    },
    '9950669635897': {  # Newland 16 — populate dimensions
        'name': 'Newland 16"W BBF mobile pedestal',
        'body': [],
        'meta': [('specs', 'dimensions', '16"W', '16"W x 22.7"D x 28"H')],
    },
    '9664290455865': {  # Ibex MVL2823 — desc-tag synchro-tilt -> multi-tilter
        'name': 'Ibex mesh seat & back multi-tilter',
        'body': [],
        'meta': [('global', 'description_tag', 'synchro-tilt', 'multi-tilter')],
    },
    '9747454427449': {  # Sparrow — stacks 4 -> 5 high
        'name': 'Sparrow OTG10920 guest chair',
        'body': [('Stacks 4 high', 'Stacks 5 high')],   # 2 occurrences
        'meta': [('specs', 'key_features', 'Stacks 4 high', 'Stacks 5 high')],
    },
    '9098317070649': {  # Large fire/water safe — exterior dims axis remap
        'name': 'Large fire/water safe',
        'body': [(f'13"W {X} 16"D {X} 19"H', f'16.3"W {X} 19.3"D {X} 13.7"H')],  # 2 occurrences
        'meta': [('specs', 'dimensions',
                  f'13"W {X} 16"D {X} 19"H (exterior)', f'16.3"W {X} 19.3"D {X} 13.7"H (exterior)')],
    },
    '9103335326009': {  # Sentry safe — interior depth + weight
        'name': 'Sentry safe security safe w/ electronic lock',
        'body': [
            (f'12-5/8"D', f'11.6"D'),
            ('Model X125 | 35.1 lbs', 'Model X125 | 26.8 lbs'),
        ],
        'meta': [
            ('specs', 'dimensions',
             f'Interior: 16-3/4"W {X} 12-5/8"D {X} 10-1/2"H',
             f'Interior: 16-3/4"W {X} 11.6"D {X} 10-1/2"H'),
            ('specs', 'weight', '35.1 lbs / 15.9 kg', '26.8 lbs / 12.2 kg'),
        ],
    },
    '9724981215545': {  # Napa — oval -> racetrack
        'name': 'Napa boardroom conference table',
        'body': [
            ('built around an oval form that works', 'built around a racetrack form that works'),
            ('<li>Oval shape accommodates multiple room sizes and configurations.</li>',
             '<li>Racetrack shape accommodates multiple room sizes and configurations.</li>'),
        ],
        'meta': [
            ('global', 'title_tag',
             'Napa Oval Boardroom Conference Table', 'Napa Racetrack Boardroom Conference Table'),
            ('global', 'description_tag', 'The Napa oval conference table', 'The Napa racetrack conference table'),
        ],
    },
    '9827425812793': {  # Kensington AC12 — locking casters wording
        'name': 'Kensington AC12 security charging cabinet',
        'body': [('4 locking casters', '4 casters with locking front pedals (two front wheels lock)')],  # 2 occ
        'meta': [('specs', 'key_features',
                  '4 locking casters', '4 casters with locking front pedals (two front wheels lock)')],
    },
    '9832610988345': {  # Ceiling grids — 12mm felt -> 9/18mm EchoScape PET
        'name': 'Ceiling grids sound acoustic dampeners',
        'body': [
            ('Constructed from 12mm felt, each panel',
             'Constructed from 9mm or 18mm EchoScape PET (polyester), each panel'),
            ('<li>12mm felt construction designed specifically for sound dampening.</li>',
             '<li>9mm or 18mm EchoScape PET (polyester) construction designed specifically for sound dampening.</li>'),
        ],
        'meta': [('global', 'description_tag',
                  '12mm felt ceiling grid', '9mm or 18mm EchoScape PET ceiling grid')],
    },
}

Q = '''query($id:ID!){ product(id:$id){ id title descriptionHtml
  seo{ title description }
  specs:metafields(first:40,namespace:"specs"){ edges{ node{ key value type } } }
  glob:metafields(first:6,namespace:"global"){ edges{ node{ key value type } } }
}}'''

MUT_BODY = '''mutation($id:ID!,$html:String!){ productUpdate(input:{id:$id,descriptionHtml:$html}){
  product{ id } userErrors{ field message } } }'''
MUT_MF = '''mutation($mf:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$mf){
  metafields{ key namespace } userErrors{ field message } } }'''


def fetch(pid):
    d = gql(Q, {'id': f'gid://shopify/Product/{pid}'})['data']['product']
    specs = {e['node']['key']: e['node'] for e in d['specs']['edges']}
    glob = {e['node']['key']: e['node'] for e in d['glob']['edges']}
    return d, specs, glob


def main():
    print(f"\n{'LIVE WRITE' if LIVE else 'DRY RUN'} — §5 factual fixes — {len(EDITS)} products\n")
    log = []
    blocked = 0
    for pid, spec in EDITS.items():
        d, specs, glob = fetch(pid)
        body = d['descriptionHtml'] or ''
        print('=' * 74)
        print(f"{pid}  {spec['name']}")
        ok = True
        plan = {'body': None, 'meta': []}

        new_body = body
        for old, new in spec['body']:
            cnt = new_body.count(old)
            tag = 'MATCH' if cnt else 'NO-MATCH'
            if not cnt:
                ok = False
            print(f"  [body x{cnt}] {tag}: {old[:60]!r} -> {new[:60]!r}")
            new_body = new_body.replace(old, new)
        if spec['body'] and new_body != body:
            plan['body'] = new_body

        for ns, key, old, new in spec['meta']:
            store = specs if ns == 'specs' else glob
            node = store.get(key)
            cur = node['value'] if node else None
            cnt = cur.count(old) if cur else 0
            tag = 'MATCH' if cnt else 'NO-MATCH'
            if not cnt:
                ok = False
            print(f"  [{ns}.{key} x{cnt}] {tag}: {old[:50]!r} -> {new[:50]!r}")
            if cnt:
                plan['meta'].append({
                    'namespace': ns, 'key': key, 'type': node['type'],
                    'value': cur.replace(old, new),
                    'old': old, 'new': new,
                })

        if not ok:
            blocked += 1
            print("  ==> BLOCKED (a NO-MATCH edit) — skipping product, no write.")
            log.append({'id': pid, 'name': spec['name'], 'status': 'BLOCKED'})
            continue

        if not LIVE:
            log.append({'id': pid, 'name': spec['name'], 'status': 'DRY-OK'})
            continue

        # ---- LIVE ----
        BACKUP = ROOT / 'data/backups' / f'spec5-{pid}-{TS}.json'
        BACKUP.write_text(json.dumps({
            'id': pid, 'title': d['title'], 'descriptionHtml': body,
            'seo': d['seo'],
            'specs': {k: v['value'] for k, v in specs.items()},
            'global': {k: v['value'] for k, v in glob.items()},
        }, indent=1, ensure_ascii=False))

        gid = f'gid://shopify/Product/{pid}'
        if plan['body']:
            r = gql(MUT_BODY, {'id': gid, 'html': plan['body']})
            errs = r['data']['productUpdate']['userErrors']
            if errs:
                print("  BODY userErrors:", errs); log.append({'id': pid, 'status': 'FAILED', 'errs': errs}); continue
        if plan['meta']:
            mf = [{'ownerId': gid, 'namespace': m['namespace'], 'key': m['key'],
                   'type': m['type'], 'value': m['value']} for m in plan['meta']]
            r = gql(MUT_MF, {'mf': mf})
            errs = r['data']['metafieldsSet']['userErrors']
            if errs:
                print("  META userErrors:", errs); log.append({'id': pid, 'status': 'FAILED', 'errs': errs}); continue

        # ---- READBACK ----
        time.sleep(1)
        d2, specs2, glob2 = fetch(pid)
        body2 = d2['descriptionHtml'] or ''
        verify_ok = True
        for old, new in spec['body']:
            if new not in body2 or old in body2:
                verify_ok = False; print(f"  READBACK FAIL body: old gone={old not in body2} new present={new in body2}")
        for m in plan['meta']:
            store2 = specs2 if m['namespace'] == 'specs' else glob2
            val2 = store2.get(m['key'], {}).get('value', '')
            if m['new'] not in val2 or m['old'] in val2:
                verify_ok = False; print(f"  READBACK FAIL {m['namespace']}.{m['key']}")
        status = 'VERIFIED' if verify_ok else 'READBACK-MISMATCH'
        print(f"  ==> {status} (backup: {BACKUP.name})")
        log.append({'id': pid, 'name': spec['name'], 'status': status, 'backup': BACKUP.name})

    LOGP = ROOT / 'data/logs' / f'spec5-fixes-{TS}.json'
    LOGP.parent.mkdir(exist_ok=True)
    LOGP.write_text(json.dumps(log, indent=1))
    print('\n' + '=' * 74)
    print(f"{'LIVE' if LIVE else 'DRY'} done. products={len(EDITS)} blocked={blocked}")
    if not LIVE:
        print("Re-run with --live to apply (after confirmation).")
    print(f"Log: {LOGP.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
