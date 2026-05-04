#!/usr/bin/env python3
"""
PE-3 push: write product `title` from data/reports/pe3-title-normalize-draft.csv
into Shopify productUpdate. Source CSV columns: handle, proposed_title (588 rows).

Usage:
  python3 scripts/push-pe3-titles.py             # DRY RUN
  python3 scripts/push-pe3-titles.py --live      # apply
  python3 scripts/push-pe3-titles.py --limit=N   # process first N
"""
import csv, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / 'data/reports/pe3-title-normalize-draft.csv'
BACKUP_DIR = ROOT / 'data/backups'
LOG_DIR = ROOT / 'data/logs'
ENV_PATH = ROOT / '.env'
for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
            if 'errors' in data: raise RuntimeError(f'GraphQL errors: {data["errors"]}')
            return data['data']
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2: time.sleep(2 ** attempt); continue
            raise

def fetch_current(handles):
    out = {}
    pending = list(handles); BATCH = 50
    while pending:
        chunk, pending = pending[:BATCH], pending[BATCH:]
        aliases = '\n'.join(f'  p{i}: productByHandle(handle: "{h}") {{ id handle title }}'
                            for i, h in enumerate(chunk))
        d = gql('{\n' + aliases + '\n}')
        for i, h in enumerate(chunk):
            n = d.get(f'p{i}')
            out[h] = {'id': n['id'], 'title': n['title']} if n else None
        time.sleep(0.5)
    return out

def update_title(pid, title):
    m = '''mutation($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title }
        userErrors { field message }
      }
    }'''
    d = gql(m, {'input': {'id': pid, 'title': title}})
    errs = d['productUpdate']['userErrors']
    if errs: raise RuntimeError(f'userErrors: {errs}')
    return d['productUpdate']['product']

def main():
    args = sys.argv[1:]
    live = '--live' in args
    limit = None
    for a in args:
        if a.startswith('--limit='): limit = int(a.split('=', 1)[1])

    rows = list(csv.DictReader(open(CSV_PATH)))
    if limit: rows = rows[:limit]
    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    print(f'Rows: {len(rows)}')
    print('Fetching current Shopify titles...')
    current = fetch_current([r['handle'] for r in rows])

    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = BACKUP_DIR / f'pe3-titles-pre-push-{ts}.csv'
    with open(backup_path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['handle', 'product_id', 'title'])
        for r in rows:
            c = current.get(r['handle'])
            w.writerow([r['handle'], c['id'] if c else '', c['title'] if c else ''])
    print(f'Backup: {backup_path}')

    plan = []
    for r in rows:
        h = r['handle']; c = current.get(h)
        if not c: plan.append({'handle': h, 'status': 'NOT_FOUND'}); continue
        new_t = r['proposed_title']
        if c['title'] == new_t: plan.append({'handle': h, 'status': 'UNCHANGED'}); continue
        plan.append({'handle': h, 'status': 'WILL_UPDATE',
                     'product_id': c['id'], 'old_title': c['title'], 'new_title': new_t})
    will = [p for p in plan if p['status'] == 'WILL_UPDATE']
    unchanged = [p for p in plan if p['status'] == 'UNCHANGED']
    missing = [p for p in plan if p['status'] == 'NOT_FOUND']
    print(f'\n  Will update: {len(will)}\n  Unchanged: {len(unchanged)}\n  Not found: {len(missing)}')

    if not live:
        print('\n=== DRY RUN sample (first 10) ===')
        for p in will[:10]:
            print(f'\n  {p["handle"]}\n    OLD: {p["old_title"]}\n    NEW: {p["new_title"]}')
        print(f'\n(Pass --live to apply {len(will)} mutations)')
        return 0

    log = []; ok = fail = 0
    print('\n=== APPLYING LIVE ===')
    for i, p in enumerate(will, 1):
        try:
            update_title(p['product_id'], p['new_title'])
            ok += 1; log.append({'handle': p['handle'], 'status': 'OK'})
            print(f'[{i:3d}/{len(will)}] OK  {p["handle"]}')
        except Exception as e:
            fail += 1; log.append({'handle': p['handle'], 'status': 'FAIL', 'error': str(e)[:200]})
            print(f'[{i:3d}/{len(will)}] FAIL {p["handle"]} — {e}')

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f'pe3-push-{ts}.json'
    log_path.write_text(json.dumps({'timestamp': ts, 'live': True, 'ok': ok, 'fail': fail,
                                     'results': log}, indent=2))
    print(f'\n{"="*60}\nDone: {ok} OK, {fail} FAIL\nLog: {log_path}\nBackup: {backup_path}')
    return 0 if fail == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
