#!/usr/bin/env python3
"""
COLLECTIONS Publish-State Reconciliation — Phase 1/2 publish toggles.

DRY-RUN by default (BBI hard rule). Pass --live to execute.
Admin-API publish writes ONLY — no theme writes, no redirect writes.

Plan:
  A  RESCUE (publish=true): benching-desks, coat-racks-accessories, modesty-panels, picnic-tables
  B  ACTIVATE fold (publish=false): reception   (healthcare-seating already unpublished -> NO-OP)
  C  boardroom fold path is OFF by default (recommendation = keep-canonical, Steve drops redirect).
     Enable only with --fold-boardroom if Steve chooses fold.

Each write backs up the collection's pre-state to data/backups/ and logs to data/logs/.
After each LIVE write: hardened readback (REST published_at re-GET + throttled storefront curl).
"""
import json, os, time, urllib.request, subprocess, sys, argparse

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
PUBLIC = 'https://www.brantbusinessinteriors.com'

ap = argparse.ArgumentParser()
ap.add_argument('--live', action='store_true')
ap.add_argument('--fold-boardroom', action='store_true')
args = ap.parse_args()
MODE = 'LIVE' if args.live else 'DRY-RUN'

# Plan: handle -> (kind, action)  action: 'publish' | 'unpublish'
PLAN = [
    ('benching-desks',         'smart',  'publish'),   # A rescue #72
    ('coat-racks-accessories', 'smart',  'publish'),   # A rescue #34
    ('modesty-panels',         'smart',  'publish'),   # A rescue #36
    ('picnic-tables',          'smart',  'publish'),   # A rescue #48
    ('reception',              'smart',  'unpublish'), # B fold -> reception-desks-desks
]
if args.fold_boardroom:
    PLAN.append(('boardroom-conference-meeting', 'smart', 'unpublish'))  # C fold (only if Steve picks fold)

def rest_get(path):
    req = urllib.request.Request(f'{API}/{path}', headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def find_collection(handle):
    """Return (kind_endpoint, id, published_at) by probing smart then custom."""
    for kind in ('smart_collections', 'custom_collections'):
        data = rest_get(f'{kind}.json?handle={handle}')
        arr = data.get(kind, [])
        if arr:
            return kind, arr[0]['id'], arr[0].get('published_at')
    return None, None, None

def put_publish(kind, cid, published):
    key = kind[:-1]  # smart_collection / custom_collection
    body = json.dumps({key: {'id': cid, 'published': published}}).encode()
    req = urllib.request.Request(f'{API}/{kind}/{cid}.json', data=body, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def storefront(handle):
    full = f'{PUBLIC}/collections/{handle}'
    out = subprocess.run(['curl','-sI','-o','/dev/null','-w','%{http_code} %{redirect_url}', full],
                         capture_output=True, text=True, timeout=30)
    return out.stdout.strip()

print(f'=== Phase 1/2 publish toggles — MODE: {MODE} ===\n')
log = {'mode': MODE, 'generated': '2026-06-02', 'actions': []}

for handle, _kind, action in PLAN:
    kind, cid, pub_at = find_collection(handle)
    cur = 'published' if pub_at else 'unpublished'
    want_pub = (action == 'publish')
    target = 'published' if want_pub else 'unpublished'
    noop = (cur == target)
    print(f'[{action.upper():9}] {handle}')
    print(f'    found: {kind} id={cid}  current={cur}  -> target={target}' + ('  (NO-OP)' if noop else ''))
    rec = {'handle': handle, 'action': action, 'kind': kind, 'id': cid,
           'before': cur, 'target': target, 'noop': noop}
    if MODE == 'LIVE' and not noop:
        # backup pre-state
        bdir = os.path.join(ROOT, 'data', 'backups')
        with open(os.path.join(bdir, f'collection-{handle}-pre-publish-20260602.json'), 'w') as bf:
            json.dump({'handle': handle, 'kind': kind, 'id': cid, 'published_at': pub_at}, bf, indent=2)
        res = put_publish(kind, cid, want_pub)
        time.sleep(4)
        # hardened readback
        rb = rest_get(f'{kind}.json?handle={handle}')[kind][0]
        new_pub = 'published' if rb.get('published_at') else 'unpublished'
        sf = storefront(handle)
        rec['after'] = new_pub
        rec['readback_storefront'] = sf
        ok = (new_pub == target)
        print(f'    WROTE -> after={new_pub}  storefront={sf}  {"MATCH" if ok else "*** MISMATCH ***"}')
    elif MODE == 'DRY-RUN' and not noop:
        print(f'    would PUT {kind}/{cid}.json  {{"published": {str(want_pub).lower()}}}')
    log['actions'].append(rec)
    print()

if MODE == 'LIVE':
    ldir = os.path.join(ROOT, 'data', 'logs')
    lp = os.path.join(ldir, 'publish-toggles-20260602.json')
    with open(lp, 'w') as lf:
        json.dump(log, lf, indent=2)
    print(f'Logged -> {lp}')
else:
    print('DRY-RUN complete. No writes performed. Re-run with --live after approval.')
