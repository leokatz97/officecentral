#!/usr/bin/env python3
"""
COLLECTIONS Phase 2 — Batch-1 Source-Unpublish · PHASE 0 (READ-ONLY).

The gated follow-up to Day-20 publish-state reconciliation. Steve imported
collections-phase2-batch1-301s.csv, so the 34 batch-1 redirects should now
exist. This script verifies that and classifies every source handle. NO writes.

For each of the 34 batch-1 "from" handles it pulls:
  - whether its /collections/<h> redirect EXISTS in the live map (Steve imported it)
  - the redirect target (from the live map)
  - current published state (REST published_at)
  - whether the handle is one of the 25 do-not-touch ranking handles

And for each unique target: live storefront HTTP status + chain check.

HARD GATE: a source whose redirect is NOT in the live map is NOT unpublishable
(unpublishing it would 404). If any batch-1 redirect is missing -> the script
flags it MISSING and the session HALTS (no proceed on those).

Classification:
  TO_UNPUBLISH = published + redirect exists + target 200 + not a ranking handle
  SKIP         = already unpublished + redirect exists (already firing -> no action)
  EXCLUDE      = keilhauer (held per Steve's pending decision)
  HALT/MISSING = redirect not in live map (import partial)

Outputs JSON + a console table.
"""
import json, os, time, urllib.request, subprocess, sys, csv

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

def rest_get(path):
    req = urllib.request.Request(f'{API}/{path}', headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode()), r.headers.get('Link', '')

def paginate(path, key):
    out = []
    while path:
        data, link = rest_get(path)
        out.extend(data.get(key, []))
        nxt = None
        for part in link.split(','):
            if 'rel="next"' in part:
                nxt = part[part.find('<')+1:part.find('>')].replace(f'{API}/', '')
        path = nxt
    return out

# ---- 1. Parse batch-1 CSV (strip comment lines) ----
csv_path = os.path.join(ROOT, 'data', 'redirects', 'collections-phase2-batch1-301s.csv')
batch1_rows = []  # (from_handle, csv_target)
with open(csv_path) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('Redirect from'):
            continue
        frm, to = [c.strip() for c in line.split(',', 1)]
        # from is /collections/<handle>
        handle = frm.replace('/collections/', '')
        batch1_rows.append((handle, frm, to))
print(f'Parsed {len(batch1_rows)} batch-1 source rows', file=sys.stderr)

# ---- 2. 25 do-not-touch ranking handles (data/reports/collections-audit.md Step 2) ----
RANKING = {
    'bariatric-seating','folding-stacking-chairs-carts','keilhauer','nesting-chairs-chair',
    'boardroom-conference-meeting','gaming','reception-desks-desks','fire-resistant-file-cabinets-storage',
    'recliners','training-flip-top-tables','bar-height-tables','coffee-tables','pedestal-drawers-storage',
    'telephone-booths','cafeteria-kitchen-tables','coat-racks-accessories','lecterns-podiums',
    'book-displays-storage','modesty-panels','desk-top-dividers','healthcare','picnic-tables',
    'fire-resistant-safes-storage','benching-desks','laboratory-furniture',
}
EXCLUDE = {'keilhauer'}  # held per Steve

# ---- 3. Index all collections by handle (REST published_at) ----
print('Pulling all collections (smart + custom)...', file=sys.stderr)
collections = {}
for kind, key in (('smart_collections', 'smart_collections'), ('custom_collections', 'custom_collections')):
    for c in paginate(f'{kind}.json?limit=250&fields=id,handle,title,published_at', key):
        collections[c['handle']] = {
            'id': c['id'], 'title': c.get('title'),
            'published_at': c.get('published_at'),
            'kind': 'smart' if kind == 'smart_collections' else 'custom',
        }
print(f'  indexed {len(collections)} collections', file=sys.stderr)

# ---- 4. Pull full live redirect map (authoritative) ----
print('Pulling live redirect map...', file=sys.stderr)
redirects = {}
for r in paginate('redirects.json?limit=250', 'redirects'):
    redirects[r['path']] = r['target']
print(f'  {len(redirects)} redirect entries', file=sys.stderr)

# ---- 5. Throttled storefront curl (status + chain) ----
def storefront(path):
    full = PUBLIC + path
    try:
        out = subprocess.run(
            ['curl', '-sI', '-o', '/dev/null', '-w', '%{http_code} %{redirect_url}', full],
            capture_output=True, text=True, timeout=30)
        return out.stdout.strip()
    except Exception as e:
        return f'ERR {e}'

# Verify each unique target resolves 200 with no chain
unique_targets = sorted({to for (_, _, to) in batch1_rows})
print('\n=== TARGET VERIFY (200, no chain) ===', file=sys.stderr)
target_status = {}
for t in unique_targets:
    time.sleep(4)
    sf = storefront(t)
    code = sf.split()[0] if sf else '?'
    final = storefront(t.replace('/collections/', '/collections/')) if False else None
    # follow once to detect a chain: if 200 directly, no chain
    chain = '-'
    if code in ('301', '302'):
        # the target itself redirects -> chain. capture where.
        redir = sf.split(' ', 1)[1] if ' ' in sf else ''
        chain = f'CHAIN->{redir}'
    target_status[t] = {'raw': sf, 'code': code, 'chain': chain}
    print(f'  {t}: {sf}', file=sys.stderr)

# ---- 6. Classify each source ----
rows = []
for handle, frm, to in batch1_rows:
    meta = collections.get(handle)
    in_index = meta is not None
    pub_at = meta['published_at'] if meta else None
    published = bool(pub_at)
    live_redirect = redirects.get(frm)  # target per live map, or None if missing
    redirect_exists = live_redirect is not None
    is_ranking = handle in RANKING
    tstat = target_status.get(to, {})
    target_200 = tstat.get('code') == '200' and tstat.get('chain') == '-'

    if handle in EXCLUDE:
        cls = 'EXCLUDE'
        reason = 'keilhauer held per Steve pending decision'
    elif not redirect_exists:
        cls = 'HALT-MISSING'
        reason = 'redirect NOT in live map — unpublishing would 404'
    elif not in_index:
        cls = 'SKIP-ABSENT'
        reason = 'source not in collections index (already gone)'
    elif not published:
        cls = 'SKIP-FIRING'
        reason = 'already unpublished + redirect exists -> already firing'
    elif is_ranking:
        cls = 'HALT-RANKING'
        reason = 'source is a do-not-touch ranking handle'
    elif not target_200:
        cls = 'HALT-TARGET'
        reason = f'target not clean 200 ({tstat.get("raw")})'
    else:
        cls = 'TO_UNPUBLISH'
        reason = 'published + redirect exists + target 200 + not ranking'

    rows.append({
        'handle': handle, 'from': frm, 'csv_target': to,
        'in_index': in_index, 'kind': meta['kind'] if meta else None,
        'collection_id': meta['id'] if meta else None,
        'published': published, 'published_at': pub_at,
        'redirect_exists': redirect_exists, 'live_redirect_target': live_redirect,
        'target_http': tstat.get('raw'), 'target_200_no_chain': target_200,
        'is_ranking_handle': is_ranking,
        'classification': cls, 'reason': reason,
    })

# ---- 7. Summary ----
from collections import Counter
counts = Counter(r['classification'] for r in rows)
out = {
    'generated': '2026-06-02',
    'csv_rows': len(batch1_rows),
    'redirect_map_count': len(redirects),
    'collections_indexed': len(collections),
    'classification_counts': dict(counts),
    'target_status': target_status,
    'rows': rows,
}
outpath = os.path.join(ROOT, 'data', 'reports', 'phase0-batch1-classify-2026-06-02.json')
with open(outpath, 'w') as f:
    json.dump(out, f, indent=2)

print('\n' + '=' * 96)
print('PHASE 0 — BATCH-1 CLASSIFICATION')
print('=' * 96)
hdr = f'{"HANDLE":<34} {"PUB":<4} {"REDIR":<6} {"TGT200":<7} {"RANK":<5} {"CLASS"}'
print(hdr)
print('-' * 96)
for r in rows:
    print(f'{r["handle"]:<34} '
          f'{"Y" if r["published"] else "N":<4} '
          f'{"Y" if r["redirect_exists"] else "MISS":<6} '
          f'{"Y" if r["target_200_no_chain"] else "N":<7} '
          f'{"Y" if r["is_ranking_handle"] else "-":<5} '
          f'{r["classification"]}')
print('-' * 96)
print('COUNTS:', dict(counts))
missing = [r['handle'] for r in rows if r['classification'] == 'HALT-MISSING']
halts = [r for r in rows if r['classification'].startswith('HALT')]
if missing:
    print(f'\n🔴 HARD GATE TRIPPED — {len(missing)} batch-1 redirect(s) MISSING from live map:')
    for h in missing:
        print(f'    - {h}')
    print('    Import was partial. HALT — do not unpublish these.')
if halts:
    print(f'\n⚠️  {len(halts)} HALT row(s) total (incl. ranking/target gates) — review before any write.')
print(f'\nWrote {outpath}')
