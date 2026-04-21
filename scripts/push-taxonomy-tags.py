"""
Phase B — push taxonomy tags from the approved CSV to Shopify.

Reads data/reports/taxonomy-tags-proposed.csv (approved by Steve), fetches each
product's current tags via the Shopify Admin API, APPENDS the facet tags
(type:*, room:*, industry:*, bestseller) without removing any existing tags,
and PUTs the result.

Usage:
  python3 scripts/push-taxonomy-tags.py               # dry run (default)
  python3 scripts/push-taxonomy-tags.py --live        # write to Shopify

Outputs:
  data/logs/push-taxonomy-tags-<timestamp>.json       # full audit trail
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

IN_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')
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


def merge_tags(existing_csv: str, new_tags: list) -> tuple:
    existing = [t.strip() for t in existing_csv.split(',') if t.strip()]
    lower = {t.lower() for t in existing}
    added = []
    for t in new_tags:
        if t and t.lower() not in lower:
            existing.append(t)
            lower.add(t.lower())
            added.append(t)
    return ', '.join(existing), added


def main() -> None:
    live = '--live' in sys.argv
    mode = 'LIVE' if live else 'DRY RUN'
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
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

    print(f'Products to process: {len(rows)}')
    print()

    skipped = 0
    would_update = 0
    updated = 0
    errors = []
    results = []

    for i, row in enumerate(rows, 1):
        try:
            pid = product_id_from_admin_url(row['admin_url'])
        except ValueError as e:
            print(f'  [{i}] SKIP: {e}')
            skipped += 1
            continue

        # Industry facet dropped per Steve (2026-04-20) — all industries buy
        # the same products, so the facet adds no sort/navigation value.
        new_tags = [t for t in [row['type_tag'], row['room_tag']] if t]
        if row['bestseller'] == 'true':
            new_tags.append('bestseller')

        if not new_tags:
            skipped += 1
            results.append({'pid': pid, 'title': row['title'],
                            'action': 'skip', 'reason': 'no tags to add'})
            continue

        try:
            existing = fetch_tags(pid)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:120]}'
            print(f'  [{i}/{len(rows)}] FETCH-ERR {msg} · {row["title"][:55]}')
            errors.append({'pid': pid, 'title': row['title'], 'stage': 'fetch',
                           'error': msg})
            continue

        merged, added = merge_tags(existing, new_tags)
        if not added:
            results.append({'pid': pid, 'title': row['title'],
                            'action': 'noop', 'existing': existing,
                            'proposed': new_tags})
            print(f'  [{i}/{len(rows)}] NOOP {row["title"][:55]}')
            time.sleep(0.25)
            continue

        would_update += 1
        if not live:
            results.append({'pid': pid, 'title': row['title'],
                            'action': 'would-update', 'added': added,
                            'existing': existing})
            print(f'  [{i}/{len(rows)}] WOULD-ADD {added} · {row["title"][:55]}')
            continue

        try:
            status = put_tags(pid, merged)
            updated += 1
            results.append({'pid': pid, 'title': row['title'],
                            'action': 'updated', 'added': added,
                            'status': status})
            print(f'  [{i}/{len(rows)}] {status} ADDED {added} · {row["title"][:55]}')
            time.sleep(0.6)
        except urllib.error.HTTPError as e:
            msg = f'{e.code} {e.read().decode()[:200]}'
            print(f'  [{i}/{len(rows)}] PUT-ERR {msg} · {row["title"][:55]}')
            errors.append({'pid': pid, 'title': row['title'], 'stage': 'put',
                           'error': msg})
        except Exception as e:
            print(f'  [{i}/{len(rows)}] PUT-ERR {e} · {row["title"][:55]}')
            errors.append({'pid': pid, 'title': row['title'], 'stage': 'put',
                           'error': str(e)})

    print()
    print(f'Summary: {mode}')
    print(f'  Skipped (no tags):        {skipped}')
    print(f'  Would/did update:         {would_update}')
    print(f'  Actually updated:         {updated}')
    print(f'  Errors:                   {len(errors)}')

    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_path = os.path.join(LOG_DIR, f'push-taxonomy-tags-{ts}.json')
    with open(log_path, 'w') as f:
        json.dump({'mode': mode, 'total': len(rows), 'skipped': skipped,
                   'would_update': would_update, 'updated': updated,
                   'errors': errors, 'results': results}, f, indent=2)
    print(f'  Audit log:                {log_path}')

    if not live:
        print('\n[DRY RUN] No writes performed. Re-run with --live to apply.')


if __name__ == '__main__':
    main()
