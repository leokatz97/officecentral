#!/usr/bin/env python3
"""
PE-4 push: write meta_title + meta_description from
data/reports/pe4-hero100-seo-draft.csv into Shopify product SEO fields.

Usage:
  python3 scripts/push-pe4-seo.py             # DRY RUN (default — prints intent, no writes)
  python3 scripts/push-pe4-seo.py --live      # actually write to Shopify
  python3 scripts/push-pe4-seo.py --limit=5   # process first N rows only

Safety:
  - Pulls current SEO via GraphQL once at startup, writes to data/backups/.
  - Skips rows where current value already matches the draft.
  - Logs every mutation outcome to data/logs/pe4-push-<ts>.json.
  - Dry-run prints first 10 mutations + summary; no API writes.
"""
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / 'data/reports/pe4-hero100-seo-draft.csv'
BACKUP_DIR = ROOT / 'data/backups'
LOG_DIR = ROOT / 'data/logs'
ENV_PATH = ROOT / '.env'

# Load env
for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip())

SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN,
        'Content-Type': 'application/json',
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
            if 'errors' in data:
                raise RuntimeError(f'GraphQL errors: {data["errors"]}')
            return data['data']
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise

def fetch_current_seo(handles):
    """Bulk fetch current id, seo.title, seo.description by handle."""
    out = {}
    for h in handles:
        q = '''query($q: String!) {
          products(first: 1, query: $q) {
            edges { node { id handle seo { title description } } }
          }
        }'''
        d = gql(q, {'q': f'handle:{h}'})
        edges = d['products']['edges']
        if not edges:
            out[h] = None
            continue
        n = edges[0]['node']
        out[h] = {
            'id': n['id'],
            'seo_title': n['seo']['title'] or '',
            'seo_description': n['seo']['description'] or '',
        }
    return out

def update_seo(product_id, title, description):
    m = '''mutation($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id seo { title description } }
        userErrors { field message }
      }
    }'''
    d = gql(m, {'input': {
        'id': product_id,
        'seo': {'title': title, 'description': description},
    }})
    errs = d['productUpdate']['userErrors']
    if errs:
        raise RuntimeError(f'userErrors: {errs}')
    return d['productUpdate']['product']

def main():
    args = sys.argv[1:]
    live = '--live' in args
    limit = None
    for a in args:
        if a.startswith('--limit='):
            limit = int(a.split('=', 1)[1])

    rows = list(csv.DictReader(open(CSV_PATH)))
    if limit:
        rows = rows[:limit]

    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    print(f'Rows to process: {len(rows)}')
    print('Fetching current Shopify SEO for all handles...')
    handles = [r['handle'] for r in rows]
    current = fetch_current_seo(handles)

    # Backup current state
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = BACKUP_DIR / f'pe4-seo-pre-push-{ts}.csv'
    with open(backup_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['handle', 'product_id', 'seo_title', 'seo_description'])
        for h in handles:
            c = current.get(h)
            if c:
                w.writerow([h, c['id'], c['seo_title'], c['seo_description']])
            else:
                w.writerow([h, '', '', ''])
    print(f'Backup: {backup_path}')

    # Plan mutations
    plan = []
    for r in rows:
        h = r['handle']
        c = current.get(h)
        if not c:
            plan.append({'handle': h, 'status': 'NOT_FOUND'}); continue
        new_t = r['draft_meta_title']
        new_d = r['draft_meta_desc']
        if c['seo_title'] == new_t and c['seo_description'] == new_d:
            plan.append({'handle': h, 'status': 'UNCHANGED'}); continue
        plan.append({
            'handle': h, 'status': 'WILL_UPDATE',
            'product_id': c['id'],
            'old_title': c['seo_title'], 'new_title': new_t,
            'old_desc': c['seo_description'], 'new_desc': new_d,
        })

    will = [p for p in plan if p['status'] == 'WILL_UPDATE']
    unchanged = [p for p in plan if p['status'] == 'UNCHANGED']
    missing = [p for p in plan if p['status'] == 'NOT_FOUND']

    print()
    print(f'  Will update: {len(will)}')
    print(f'  Unchanged:   {len(unchanged)}')
    print(f'  Not found:   {len(missing)}')
    if missing:
        for p in missing[:5]:
            print(f'    ⚠ {p["handle"]}')

    if not live:
        print()
        print('=== DRY RUN — sample of first 10 mutations ===')
        for p in will[:10]:
            print(f'\n  {p["handle"]}')
            print(f'    OLD title: {p["old_title"][:90]}')
            print(f'    NEW title: {p["new_title"]}')
            print(f'    OLD desc:  {p["old_desc"][:120]}')
            print(f'    NEW desc:  {p["new_desc"]}')
        print(f'\n(Pass --live to apply {len(will)} mutations)')
        return 0

    # LIVE
    log = []
    ok = fail = 0
    print()
    print('=== APPLYING LIVE ===')
    for i, p in enumerate(will, 1):
        try:
            res = update_seo(p['product_id'], p['new_title'], p['new_desc'])
            ok += 1
            log.append({'handle': p['handle'], 'status': 'OK'})
            print(f'[{i:3d}/{len(will)}] OK  {p["handle"]}')
        except Exception as e:
            fail += 1
            log.append({'handle': p['handle'], 'status': 'FAIL', 'error': str(e)[:200]})
            print(f'[{i:3d}/{len(will)}] FAIL {p["handle"]} — {e}')

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f'pe4-push-{ts}.json'
    log_path.write_text(json.dumps({
        'timestamp': ts, 'live': True,
        'ok': ok, 'fail': fail,
        'results': log,
    }, indent=2))
    print()
    print('=' * 60)
    print(f'Done: {ok} OK, {fail} FAIL')
    print(f'Log: {log_path}')
    print(f'Backup (rollback source): {backup_path}')
    return 0 if fail == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
