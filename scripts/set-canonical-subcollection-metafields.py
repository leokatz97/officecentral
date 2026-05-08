#!/usr/bin/env python3
"""
set-canonical-subcollection-metafields.py
Stage 3.2c.6.5 — Set bbi.parent_hub_handle and bbi.parent_hub_title metafields
on the 19 canonical user-facing handles flipped in Phase 4.

Reads from data/reports/stage-3.2c.6-flip-targets.csv.

Usage:
  python3 scripts/set-canonical-subcollection-metafields.py          # dry-run (default)
  python3 scripts/set-canonical-subcollection-metafields.py --live   # push to Shopify
"""

import csv, json, re, sys, time, urllib.error, urllib.parse, urllib.request
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

HUB_TITLES = {
    'accessories':        'Accessories',
    'boardroom':          'Boardroom',
    'desks':              'Desks & Workstations',
    'ergonomic-products': 'Ergonomic Products',
    'panels-room-dividers': 'Panels & Room Dividers',
    'quiet-spaces':       'Quiet Spaces',
    'seating':            'Seating',
    'storage':            'Storage & Filing',
    'tables':             'Tables',
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
                print(f"    [429] waiting {wait:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                continue
            return e.code, json.loads(e.read().decode())
    return 429, {'error': 'max retries exceeded'}


def fetch_collection_id(handle):
    for endpoint, key in [
        (f'/custom_collections.json?handle={urllib.parse.quote(handle)}&fields=id,handle', 'custom_collections'),
        (f'/smart_collections.json?handle={urllib.parse.quote(handle)}&fields=id,handle', 'smart_collections'),
    ]:
        _, resp = api_call(endpoint)
        cols = resp.get(key, [])
        if cols:
            return cols[0]['id']
    return None


def get_existing_metafield(collection_id, namespace, key):
    _, resp = api_call(f'/collections/{collection_id}/metafields.json?namespace={namespace}&key={key}')
    mfs = resp.get('metafields', [])
    if mfs:
        return mfs[0]['id'], mfs[0].get('value')
    return None, None


def set_metafield(collection_id, namespace, key, value):
    existing_id, existing_val = get_existing_metafield(collection_id, namespace, key)
    if existing_id:
        if existing_val == value:
            return 'SKIP', 'already set'
        status, resp = api_call(
            f'/metafields/{existing_id}.json', method='PUT',
            body={'metafield': {'id': existing_id, 'value': value, 'type': 'single_line_text_field'}},
        )
        return status, resp
    status, resp = api_call(
        f'/collections/{collection_id}/metafields.json', method='POST',
        body={'metafield': {'namespace': namespace, 'key': key, 'value': value, 'type': 'single_line_text_field'}},
    )
    return status, resp


def main():
    targets = list(csv.DictReader(open(TARGETS_CSV)))
    print(f"{'DRY RUN' if DRY_RUN else 'LIVE RUN'} — {STORE}")
    print(f"Target: {len(targets)} handles\n")

    rows = []
    print("Resolving collection IDs...")
    for t in targets:
        handle = t['handle']
        parent_hub = t['parent_hub']
        parent_title = HUB_TITLES.get(parent_hub, parent_hub)
        col_id = fetch_collection_id(handle)
        time.sleep(0.5)
        if col_id is None:
            print(f"  NOT_FOUND  {handle}")
            rows.append({'handle': handle, 'col_id': None, 'parent_hub': parent_hub, 'parent_title': parent_title})
            continue
        print(f"  FOUND  {handle:<45} → {parent_hub}  id={col_id}")
        rows.append({'handle': handle, 'col_id': col_id, 'parent_hub': parent_hub, 'parent_title': parent_title})

    if DRY_RUN:
        print(f"\nDry-run complete — {len([r for r in rows if r['col_id']])} would have metafields set.")
        print("Pass --live to apply.")
        return

    print(f"\nPausing 10s to let API rate limit bucket refill...")
    time.sleep(10)

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    ok = skip = fail = 0
    log = []

    for r in rows:
        handle = r['handle']
        col_id = r['col_id']
        if not col_id:
            fail += 1
            log.append({**r, 'status_handle': 'NOT_FOUND', 'status_title': 'NOT_FOUND'})
            continue

        time.sleep(1.0)
        s1, _ = set_metafield(col_id, 'bbi', 'parent_hub_handle', r['parent_hub'])
        time.sleep(1.0)
        s2, _ = set_metafield(col_id, 'bbi', 'parent_hub_title', r['parent_title'])

        if s1 == 'SKIP' and s2 == 'SKIP':
            print(f"  SKIP  {handle}")
            skip += 1
        elif (s1 in (200, 201) or s1 == 'SKIP') and (s2 in (200, 201) or s2 == 'SKIP'):
            print(f"  OK    {handle}  → {r['parent_hub']} / {r['parent_title']}")
            ok += 1
        else:
            print(f"  ERR   {handle}  s_handle={s1}  s_title={s2}")
            fail += 1

        log.append({**r, 'status_handle': str(s1), 'status_title': str(s2)})

    log_path = Path(f'data/logs/set-canonical-metafields-{ts}.json')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2))
    print(f"\nDone: {ok} ok, {skip} already-set skipped, {fail} failed")
    print(f"Log: {log_path}")


if __name__ == '__main__':
    main()
