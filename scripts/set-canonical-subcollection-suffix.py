#!/usr/bin/env python3
"""
set-canonical-subcollection-suffix.py
Stage 3.2c.6 — Flip user-facing sub-collection handles to template_suffix=base.

Reads from data/reports/stage-3.2c.6-flip-targets.csv (19 handles).
Does NOT use the hardcoded wrong-handle list from set-sub-collection-suffix.py.

Usage:
  python3 scripts/set-canonical-subcollection-suffix.py          # dry-run (default)
  python3 scripts/set-canonical-subcollection-suffix.py --live   # push to Shopify
"""

import csv, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

env_content = open(Path(__file__).parent.parent / '.env').read()
TOKEN = re.search(r'SHOPIFY_TOKEN=(.+)', env_content).group(1).strip()
STORE = re.search(r'SHOPIFY_STORE=(.+)', env_content).group(1).strip()
API_VERSION = '2024-01'
DRY_RUN = '--live' not in sys.argv

HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json',
}

TARGETS_CSV = Path(__file__).parent.parent / 'data/reports/stage-3.2c.6-flip-targets.csv'


def api_call(path, method='GET', body=None, max_retries=5):
    url = f'https://{STORE}/admin/api/{API_VERSION}{path}'
    for attempt in range(max_retries):
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = float(e.headers.get('Retry-After', 4)) + 1
                print(f"    [429] rate-limited — waiting {wait:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                continue
            return e.code, json.loads(e.read().decode())
    return 429, {'error': 'max retries exceeded'}


def fetch_collection_by_handle(handle):
    for endpoint, key in [
        (f'/custom_collections.json?handle={urllib.parse.quote(handle)}&fields=id,handle,title,template_suffix', 'custom_collections'),
        (f'/smart_collections.json?handle={urllib.parse.quote(handle)}&fields=id,handle,title,template_suffix', 'smart_collections'),
    ]:
        _, resp = api_call(endpoint)
        cols = resp.get(key, [])
        if cols:
            return cols[0], key.replace('_collections', '')
    return None, None


def set_template_suffix(col_id, col_type, suffix='base'):
    endpoint_key = 'custom_collection' if col_type == 'custom' else 'smart_collection'
    endpoint_path = f'/{"custom" if col_type == "custom" else "smart"}_collections/{col_id}.json'
    status, resp = api_call(endpoint_path, method='PUT', body={endpoint_key: {'id': col_id, 'template_suffix': suffix}})
    return status, resp


def main():
    targets = list(csv.DictReader(open(TARGETS_CSV)))
    print(f"{'DRY RUN' if DRY_RUN else 'LIVE RUN'} — {STORE}")
    print(f"Target: {len(targets)} handles from {TARGETS_CSV.name}\n")

    rows = []
    print("Resolving collection IDs...")
    for t in targets:
        handle = t['handle']
        col, col_type = fetch_collection_by_handle(handle)
        time.sleep(0.5)
        if col is None:
            print(f"  NOT_FOUND  {handle}")
            rows.append({**t, 'col_id': None, 'col_type': None, 'status': 'NOT_FOUND'})
            continue
        current_suffix = col.get('template_suffix') or ''
        print(f"  FOUND  {handle:<45} current_suffix={current_suffix!r}  id={col['id']}")
        rows.append({**t, 'col_id': col['id'], 'col_type': col_type, 'current_suffix': current_suffix, 'status': 'pending'})

    if DRY_RUN:
        print(f"\nDry-run complete — {len([r for r in rows if r['status']=='pending'])} would be flipped.")
        print("Pass --live to apply.")
        return

    print(f"\nPausing 5s before bulk writes...")
    time.sleep(5)

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    log = []
    ok = skip = fail = 0

    for r in rows:
        handle = r['handle']
        if r['status'] == 'NOT_FOUND':
            fail += 1
            log.append({**r, 'flip_status': 'NOT_FOUND'})
            continue
        if r.get('current_suffix') == 'base':
            print(f"  SKIP   {handle}  (already base)")
            skip += 1
            log.append({**r, 'flip_status': 'SKIP'})
            continue

        time.sleep(0.8)
        status, resp = set_template_suffix(r['col_id'], r['col_type'])
        if status in (200, 201):
            print(f"  OK     {handle}  → base")
            ok += 1
            log.append({**r, 'flip_status': 'OK'})
        else:
            print(f"  ERR    {handle}  status={status}  resp={resp}")
            fail += 1
            log.append({**r, 'flip_status': f'ERR_{status}'})

    log_path = Path(f'data/logs/set-canonical-suffix-{ts}.json')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2))
    print(f"\nDone: {ok} flipped, {skip} already-base skipped, {fail} failed")
    print(f"Log: {log_path}")


if __name__ == '__main__':
    main()
