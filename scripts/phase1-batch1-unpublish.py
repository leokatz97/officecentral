#!/usr/bin/env python3
"""
COLLECTIONS Phase 2 — Batch-1 Source-Unpublish · PHASE 1/2 (publish toggles).

DRY-RUN by default (BBI hard rule). Pass --live to execute.
Admin-API publish writes ONLY — no theme writes, no redirect writes, no menu writes.

Reads the Phase 0 classification JSON and acts on the TO_UNPUBLISH set only.
keilhauer (EXCLUDE) is never touched. Any HALT-* row aborts the run.

Each LIVE write:
  1. backs up the collection's pre-state to data/backups/
  2. PUT published=false (REST)
  3. hardened readback: REST published_at re-GET (must be null = authoritative)
     + throttled, cache-busted storefront curl (expect 301 -> target once edge clears)
Logs the full run to data/logs/.
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
args = ap.parse_args()
MODE = 'LIVE' if args.live else 'DRY-RUN'

STAMP = '2026-06-02'
p0 = json.load(open(os.path.join(ROOT, 'data', 'reports', f'phase0-batch1-classify-{STAMP}.json')))

# Abort if any HALT row survived in Phase 0
halts = [r for r in p0['rows'] if r['classification'].startswith('HALT')]
if halts:
    print('🔴 ABORT — Phase 0 has HALT rows; resolve before any toggle:', file=sys.stderr)
    for r in halts:
        print(f'    {r["handle"]}: {r["classification"]} — {r["reason"]}', file=sys.stderr)
    sys.exit(1)

PLAN = [r for r in p0['rows'] if r['classification'] == 'TO_UNPUBLISH']
print(f'MODE={MODE}  TO_UNPUBLISH={len(PLAN)}  (keilhauer excluded, 0 HALT)', file=sys.stderr)

def rest_get(path):
    req = urllib.request.Request(f'{API}/{path}', headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def rest_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f'{API}/{path}', data=data, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def storefront(path, bust=False):
    full = PUBLIC + path + ('?_cb=%d' % int(time.time()) if bust else '')
    try:
        out = subprocess.run(
            ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code} %{redirect_url}', full],
            capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception as e:
        return f'ERR {e}'

log = {'mode': MODE, 'stamp': STAMP, 'writes': []}

for r in PLAN:
    handle = r['handle']
    kind = r['kind']            # 'smart' | 'custom'
    cid = r['collection_id']
    resource = 'smart_collections' if kind == 'smart' else 'custom_collections'
    skey = 'smart_collection' if kind == 'smart' else 'custom_collection'
    target = r['live_redirect_target']

    print(f'\n--- {handle}  (id={cid}, {kind}) -> 301 {target} ---')
    if not args.live:
        print(f'  [DRY-RUN] would PUT {resource}/{cid}.json {{published:false}}')
        log['writes'].append({'handle': handle, 'id': cid, 'kind': kind,
                              'target': target, 'action': 'DRY-RUN'})
        continue

    # 1. backup pre-state
    pre = rest_get(f'{resource}/{cid}.json')[skey]
    bdir = os.path.join(ROOT, 'data', 'backups')
    os.makedirs(bdir, exist_ok=True)
    with open(os.path.join(bdir, f'batch1-unpub-{handle}-{STAMP}.json'), 'w') as f:
        json.dump(pre, f, indent=2)
    pre_pub = pre.get('published_at')

    # 2. unpublish
    rest_put(f'{resource}/{cid}.json', {skey: {'id': cid, 'published': False}})

    # 3. hardened readback — REST is authoritative
    time.sleep(2)
    post = rest_get(f'{resource}/{cid}.json')[skey]
    post_pub = post.get('published_at')
    rest_ok = post_pub is None

    time.sleep(3)
    sf = storefront(f'/collections/{handle}', bust=True)
    code = sf.split()[0] if sf else '?'
    redir = sf.split(' ', 1)[1].strip() if ' ' in sf else ''
    sf_ok = code in ('301', '302') and target in redir
    sf_note = 'OK 301->target' if sf_ok else ('edge-lag (REST authoritative)' if code == '200' else f'unexpected {sf}')

    status = 'MATCH' if rest_ok else 'FAIL'
    print(f'  pre.published_at={pre_pub}')
    print(f'  post.published_at={post_pub}  REST={"null ✓" if rest_ok else "STILL SET ✗"}')
    print(f'  storefront={sf}  -> {sf_note}')
    print(f'  ==> {status}')

    log['writes'].append({
        'handle': handle, 'id': cid, 'kind': kind, 'target': target,
        'pre_published_at': pre_pub, 'post_published_at': post_pub,
        'rest_ok': rest_ok, 'storefront': sf, 'sf_ok': sf_ok, 'sf_note': sf_note,
        'status': status,
    })
    time.sleep(3)  # throttle between collections

# summary + log
if args.live:
    matched = sum(1 for w in log['writes'] if w.get('status') == 'MATCH')
    sf_fired = sum(1 for w in log['writes'] if w.get('sf_ok'))
    print(f'\n=== LIVE SUMMARY: {matched}/{len(log["writes"])} REST-MATCH; '
          f'{sf_fired}/{len(log["writes"])} storefront 301 already firing (rest = edge-lag) ===')
    ldir = os.path.join(ROOT, 'data', 'logs')
    os.makedirs(ldir, exist_ok=True)
    lpath = os.path.join(ldir, f'batch1-unpublish-{STAMP}.json')
    with open(lpath, 'w') as f:
        json.dump(log, f, indent=2)
    print(f'Wrote {lpath}')
else:
    print(f'\n=== DRY-RUN: {len(PLAN)} collections would be unpublished. Nothing written. ===')
