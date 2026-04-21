"""
Phase X2 — push the industry:* tag to each active product.

Reads data/reports/industry-tags-proposed.csv (approved by Steve) and appends
the industry_tag to each product's existing tags via Shopify Admin API.

Never strips existing tags. Idempotent — re-runs are no-ops for already-tagged
products. Dry-run default.

Usage:
  python3 scripts/push-industry-tags.py               # dry run
  python3 scripts/push-industry-tags.py --live        # write to Shopify
  python3 scripts/push-industry-tags.py --limit=10    # smoke-test first N
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

IN_CSV = os.path.join(ROOT, 'data', 'reports', 'industry-tags-proposed.csv')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
ID_FROM_URL = re.compile(r'/products/(\d+)')


def product_id_from_admin_url(url: str) -> str:
    m = ID_FROM_URL.search(url)
    if not m:
        raise ValueError(f'no product id in admin_url: {url}')
    return m.group(1)


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


def merge_tag(existing_csv: str, new_tag: str) -> tuple:
    existing = [t.strip() for t in existing_csv.split(',') if t.strip()]
    lower = {t.lower() for t in existing}
    if new_tag.lower() in lower:
        return existing_csv, False
    existing.append(new_tag)
    return ', '.join(existing), True


def main() -> None:
    live = '--live' in sys.argv
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
    mode = 'LIVE' if live else 'DRY RUN'
    print(f'Mode: {mode}')
    print(f'Source: {IN_CSV}')
    if limit:
        print(f'Limit: first {limit} rows')
    print()

    rows = []
    with open(IN_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)
    if limit:
        rows = rows[:limit]

    skipped_no_tag = 0
    would_update = 0
    updated = 0
    noop = 0
    errors = []
    results = []

    for i, row in enumerate(rows, 1):
        if not row['industry_tag']:
            skipped_no_tag += 1
            continue

        try:
            pid = product_id_from_admin_url(row['admin_url'])
        except ValueError as e:
            print(f'  [{i}] SKIP bad admin_url: {e}')
            continue

        try:
            existing = fetch_tags(pid)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:120]}'
            print(f'  [{i}/{len(rows)}] FETCH-ERR {msg} · {row["title"][:55]}')
            errors.append({'pid': pid, 'title': row['title'], 'stage': 'fetch',
                           'error': msg})
            continue

        merged, added = merge_tag(existing, row['industry_tag'])
        if not added:
            noop += 1
            print(f'  [{i}/{len(rows)}] NOOP · {row["title"][:55]}')
            time.sleep(0.25)
            continue

        would_update += 1
        if not live:
            print(f'  [{i}/{len(rows)}] WOULD-ADD {row["industry_tag"]} · {row["title"][:55]}')
            continue

        try:
            status = put_tags(pid, merged)
            updated += 1
            results.append({'pid': pid, 'title': row['title'],
                            'added': row['industry_tag'], 'status': status})
            print(f'  [{i}/{len(rows)}] {status} ADDED {row["industry_tag"]} · {row["title"][:55]}')
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:200]}'
            print(f'  [{i}/{len(rows)}] PUT-ERR {msg} · {row["title"][:55]}')
            errors.append({'pid': pid, 'title': row['title'], 'stage': 'put',
                           'error': msg})

    print()
    print(f'Summary: {mode}')
    print(f'  Skipped (no industry_tag):  {skipped_no_tag}')
    print(f'  NOOP (tag already present): {noop}')
    print(f'  Would/did update:           {would_update}')
    print(f'  Actually updated:           {updated}')
    print(f'  Errors:                     {len(errors)}')

    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_path = os.path.join(LOG_DIR, f'push-industry-tags-{ts}.json')
    with open(log_path, 'w') as f:
        json.dump({'mode': mode, 'total': len(rows),
                   'skipped_no_tag': skipped_no_tag, 'noop': noop,
                   'would_update': would_update, 'updated': updated,
                   'errors': errors, 'results': results}, f, indent=2)
    print(f'  Audit log:                  {log_path}')

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
