"""
Correct industry tags on Shopify by diffing two versions of the CSV.

For every row whose industry_tag changed between v1 (what was pushed) and v2
(the current/correct state), reconcile Shopify to match v2:
  - If v1 applied a now-wrong industry tag, remove it.
  - Add the v2 industry tag.

Used 2026-04-20 to fix ObusForme misclassification (healthcare → business)
and pick up Foundations childcare items that were previously skipped.

Usage:
  python3 scripts/apply-industry-corrections.py              # dry run
  python3 scripts/apply-industry-corrections.py --live
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

V1 = os.path.join(ROOT, 'data', 'reports', 'industry-tags-proposed.v1.csv')
V2 = os.path.join(ROOT, 'data', 'reports', 'industry-tags-proposed.csv')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
ID_FROM_URL = re.compile(r'/products/(\d+)')


def fetch_tags(pid: str) -> str:
    url = f'{API}/products/{pid}.json?fields=id,tags'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['product'].get('tags', '') or ''


def put_tags(pid: str, tags_csv: str) -> int:
    url = f'{API}/products/{pid}.json'
    payload = json.dumps({'product': {'id': int(pid), 'tags': tags_csv}}).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as resp:
        return resp.status


def reconcile(existing_csv: str, remove_tag: str, add_tag: str) -> tuple:
    existing = [t.strip() for t in existing_csv.split(',') if t.strip()]
    lower = [t.lower() for t in existing]

    changed = False
    if remove_tag:
        target = remove_tag.lower()
        kept = [t for t in existing if t.lower() != target]
        if len(kept) != len(existing):
            existing = kept
            lower = [t.lower() for t in existing]
            changed = True

    if add_tag and add_tag.lower() not in lower:
        existing.append(add_tag)
        changed = True

    return ', '.join(existing), changed


def main() -> None:
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print()

    with open(V1, newline='', encoding='utf-8') as f:
        v1 = {r['handle']: r for r in csv.DictReader(f)}
    with open(V2, newline='', encoding='utf-8') as f:
        v2 = {r['handle']: r for r in csv.DictReader(f)}

    changes = []
    for h, v2row in v2.items():
        v1row = v1.get(h)
        old = v1row['industry_tag'] if v1row else ''
        new = v2row['industry_tag']
        if old == new:
            continue
        changes.append({
            'handle': h,
            'title': v2row['title'],
            'admin_url': v2row['admin_url'],
            'old_tag': old,
            'new_tag': new,
        })

    print(f'Rows with changed classification: {len(changes)}')
    for c in changes:
        print(f'  {c["old_tag"] or "(none)":<22} → {c["new_tag"]:<22} {c["title"][:55]}')
    print()

    if not changes:
        print('Nothing to reconcile.')
        return

    updated = 0
    noop = 0
    errors = []
    results = []

    for i, c in enumerate(changes, 1):
        m = ID_FROM_URL.search(c['admin_url'])
        if not m:
            print(f'  [{i}] BAD URL: {c["admin_url"]}')
            continue
        pid = m.group(1)

        try:
            existing = fetch_tags(pid)
        except urllib.error.HTTPError as e:
            print(f'  [{i}] FETCH-ERR {e.code}')
            errors.append({'pid': pid, 'stage': 'fetch', 'error': str(e)})
            continue

        merged, changed = reconcile(existing, c['old_tag'], c['new_tag'])
        if not changed:
            noop += 1
            print(f'  [{i}/{len(changes)}] NOOP · {c["title"][:55]}')
            time.sleep(0.25)
            continue

        if not live:
            print(f'  [{i}/{len(changes)}] WOULD: remove={c["old_tag"] or "(none)"}, add={c["new_tag"]} · {c["title"][:55]}')
            continue

        try:
            status = put_tags(pid, merged)
            updated += 1
            results.append({'pid': pid, 'title': c['title'],
                            'removed': c['old_tag'], 'added': c['new_tag'],
                            'status': status})
            print(f'  [{i}/{len(changes)}] {status} · -{c["old_tag"] or "(none)"} +{c["new_tag"]} · {c["title"][:55]}')
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:200]}'
            print(f'  [{i}/{len(changes)}] PUT-ERR {msg}')
            errors.append({'pid': pid, 'stage': 'put', 'error': msg})

    print()
    print(f'Summary: {mode}')
    print(f'  Changes:          {len(changes)}')
    print(f'  Updated:          {updated}')
    print(f'  NOOP:             {noop}')
    print(f'  Errors:           {len(errors)}')

    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_path = os.path.join(LOG_DIR, f'apply-industry-corrections-{ts}.json')
    with open(log_path, 'w') as f:
        json.dump({'mode': mode, 'changes': changes, 'results': results,
                   'errors': errors}, f, indent=2)
    print(f'  Audit log:        {log_path}')

    if not live:
        print('\n[DRY RUN] No writes. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
