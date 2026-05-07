#!/usr/bin/env python3
"""
set-collection-parent-metafields.py
Stage 3.2c.5 — Set bbi.parent_hub_handle and bbi.parent_hub_title metafields
on all sub-collections using template_suffix=base.

These metafields power the breadcrumb and hero eyebrow in ds-cs-base.liquid.
The section reads them first, then falls back to section settings, then to
'business-furniture' / 'Business Furniture'.

Usage:
  python3 scripts/set-collection-parent-metafields.py          # dry-run (default)
  python3 scripts/set-collection-parent-metafields.py --live   # push to Shopify

Env: SHOPIFY_TOKEN, SHOPIFY_STORE (read from .env)
Target: Shopify store (metafields are store-wide, not theme-specific)
"""

import csv, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

# ── Credentials ─────────────────────────────────────────────────────────────
env_content = open(Path(__file__).parent.parent / '.env').read()
TOKEN = re.search(r'SHOPIFY_TOKEN=(.+)', env_content).group(1).strip()
STORE = re.search(r'SHOPIFY_STORE=(.+)', env_content).group(1).strip()
API_VERSION = '2024-01'
DRY_RUN = '--live' not in sys.argv

HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json',
}

# ── Parent hub mapping ───────────────────────────────────────────────────────
# Format: collection_handle → (parent_hub_handle, parent_hub_title)
# Source: stage-3.2a.5-migration-plan.md §3 + stage-3.2b-schema-mapping.csv
MAPPING = {
    # ── 32 pre-existing Stage 1.6 shells + highback-seating (from 3.2b CSV) ──
    'acoustic-panels':       ('panels-room-dividers', 'Panels & Room Dividers'),
    'acoustic-pods':         ('quiet-spaces',          'Quiet Spaces'),
    'active-seating':        ('seating',               'Seating'),
    'beam-seating':          ('seating',               'Seating'),
    'bench-seating':         ('seating',               'Seating'),
    'boardroom-seating':     ('boardroom',             'Boardroom'),
    'boardroom-storage':     ('boardroom',             'Boardroom'),
    'cafe-tables':           ('tables',                'Tables'),
    'collaborative-tables':  ('tables',                'Tables'),
    'conference-seating':    ('seating',               'Seating'),
    'desk-accessories':      ('accessories',           'Accessories'),
    'desktop-accessories':   ('accessories',           'Accessories'),
    'ergocentric':           ('ergonomic-products',    'Ergonomic Products'),
    'ergonomic-accessories': ('ergonomic-products',    'Ergonomic Products'),
    'executive-desks':       ('desks',                 'Desks & Workstations'),
    'executive-seating':     ('seating',               'Seating'),
    'focus-rooms':           ('quiet-spaces',          'Quiet Spaces'),
    'global-furniture':      ('desks',                 'Desks & Workstations'),
    'global-teknion':        ('desks',                 'Desks & Workstations'),
    'healthcare-seating':    ('seating',               'Seating'),
    'high-density-storage':  ('storage',               'Storage & Filing'),
    'highback-seating':      ('seating',               'Seating'),
    'keilhauer':             ('seating',               'Seating'),
    'mailboxes':             ('accessories',           'Accessories'),
    'media-storage':         ('storage',               'Storage & Filing'),
    'mobile-storage':        ('storage',               'Storage & Filing'),
    'modular-workstations':  ('desks',                 'Desks & Workstations'),
    'multipurpose-tables':   ('tables',                'Tables'),
    'nesting-tables':        ('tables',                'Tables'),
    'outdoor-tables':        ('tables',                'Tables'),
    'personal-storage':      ('storage',               'Storage & Filing'),
    'privacy-screens':       ('panels-room-dividers', 'Panels & Room Dividers'),
    # ── 5 additional Stage 1.6 shells with unknown hub (migration plan §3 note) ──
    'training-desks':        ('desks',                 'Desks & Workstations'),
    'wall-storage':          ('storage',               'Storage & Filing'),
    'waste-recycling':       ('accessories',           'Accessories'),
    'side-tables':           ('tables',                'Tables'),
    'standing-tables':       ('tables',                'Tables'),
    # ── 56 newly-flipped legacy collections (Stage 3.2c Phase 3) ──
    # Seating (15)
    'medium-back-seating':           ('seating', 'Seating'),
    'mesh-seating':                  ('seating', 'Seating'),
    'guest-seating':                 ('seating', 'Seating'),
    'leather-faux-seating':          ('seating', 'Seating'),
    'lounge-chairs-seating':         ('seating', 'Seating'),
    'stacking-seating':              ('seating', 'Seating'),
    'stools-seating':                ('seating', 'Seating'),
    'big-heavy-seating':             ('seating', 'Seating'),
    'industrial-seating':            ('seating', 'Seating'),
    'folding-stacking-chairs-carts': ('seating', 'Seating'),
    'ottomans':                      ('seating', 'Seating'),
    'nesting-chairs-chair':          ('seating', 'Seating'),
    '24-hour-seating':               ('seating', 'Seating'),
    'gaming':                        ('seating', 'Seating'),
    'cluster-seating':               ('seating', 'Seating'),
    # Desks (9)
    'l-shape-desks-desks':            ('desks', 'Desks & Workstations'),
    'height-adjustable-tables-desks': ('desks', 'Desks & Workstations'),
    'straight-desks-desks':           ('desks', 'Desks & Workstations'),
    'u-shape-desks-desks':            ('desks', 'Desks & Workstations'),
    'office-suites-desks':            ('desks', 'Desks & Workstations'),
    'multi-person-workstations-desks':('desks', 'Desks & Workstations'),
    'table-desks':                    ('desks', 'Desks & Workstations'),
    'reception':                      ('desks', 'Desks & Workstations'),
    'benching-desks':                 ('desks', 'Desks & Workstations'),
    # Storage (13)
    'bookcases-storage':                   ('storage', 'Storage & Filing'),
    'storage-cabinets-storage':            ('storage', 'Storage & Filing'),
    'fire-resistant-safes-storage':        ('storage', 'Storage & Filing'),
    'credenzas':                           ('storage', 'Storage & Filing'),
    'pedestal-drawers-storage':            ('storage', 'Storage & Filing'),
    'lateral-files-storage':               ('storage', 'Storage & Filing'),
    'fire-resistant-file-cabinets-storage':('storage', 'Storage & Filing'),
    'lockers':                             ('storage', 'Storage & Filing'),
    'vertical-files':                      ('storage', 'Storage & Filing'),
    'wardrobe-storage':                    ('storage', 'Storage & Filing'),
    'lateral-storage-combo-storage':       ('storage', 'Storage & Filing'),
    'hutch':                               ('storage', 'Storage & Filing'),
    'end-tab-filing-storage':              ('storage', 'Storage & Filing'),
    # Tables (10)
    'meeting-tables':          ('tables', 'Tables'),
    'round-square-tables':     ('tables', 'Tables'),
    'folding-tables-tables':   ('tables', 'Tables'),
    'drafting-tables':         ('tables', 'Tables'),
    'coffee-tables':           ('tables', 'Tables'),
    'end-tables-tables':       ('tables', 'Tables'),
    'table-bases':             ('tables', 'Tables'),
    'training-flip-top-tables':('tables', 'Tables'),
    'cafeteria-kitchen-tables':('tables', 'Tables'),
    'bar-height-tables':       ('tables', 'Tables'),
    # Boardroom (2)
    'boardroom-conference-meeting': ('boardroom', 'Boardroom'),
    'lecterns-podiums':             ('boardroom', 'Boardroom'),
    # Ergonomic Products (4)
    'height-adjustable-tables': ('ergonomic-products', 'Ergonomic Products'),
    'desktop-sit-stand':        ('ergonomic-products', 'Ergonomic Products'),
    'monitor-arms':             ('ergonomic-products', 'Ergonomic Products'),
    'keyboard-trays':           ('ergonomic-products', 'Ergonomic Products'),
    # Panels & Room Dividers (3)
    'room-dividers-panels-dividers': ('panels-room-dividers', 'Panels & Room Dividers'),
    'desk-top-dividers':             ('panels-room-dividers', 'Panels & Room Dividers'),
    'modesty-panels':                ('panels-room-dividers', 'Panels & Room Dividers'),
}


# ── API helpers ──────────────────────────────────────────────────────────────
def api_get(path):
    status, resp, headers = api_call(path, method='GET')
    return resp, headers


def api_call(path, method='GET', body=None, max_retries=5):
    """Make an API call with automatic 429 retry-after handling."""
    url = f'https://{STORE}/admin/api/{API_VERSION}{path}'
    for attempt in range(max_retries):
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read()), dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = float(e.headers.get('Retry-After', 4))
                wait = retry_after + 1
                print(f"    [429] rate-limited — waiting {wait:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                continue
            return e.code, json.loads(e.read().decode()), {}
    return 429, {'error': 'max retries exceeded'}, {}


def api_post(path, body):
    status, resp, _ = api_call(path, method='POST', body=body)
    return status, resp


def api_put(path, body):
    status, resp, _ = api_call(path, method='PUT', body=body)
    return status, resp


def fetch_collection_by_handle(handle):
    """Fetch a single custom_collection by handle. Returns collection dict or None."""
    data, _ = api_get(f'/custom_collections.json?handle={urllib.parse.quote(handle)}&fields=id,handle,title,template_suffix')
    cols = data.get('custom_collections', [])
    return cols[0] if cols else None


def get_existing_metafield(collection_id, namespace, key):
    """Return (id, current_value) of existing metafield, or (None, None)."""
    data, _ = api_get(f'/collections/{collection_id}/metafields.json?namespace={namespace}&key={key}')
    mfs = data.get('metafields', [])
    if mfs:
        return mfs[0]['id'], mfs[0].get('value')
    return None, None


def set_metafield(collection_id, namespace, key, value, mf_type='single_line_text_field'):
    existing_id, existing_val = get_existing_metafield(collection_id, namespace, key)
    if existing_id:
        if existing_val == value:
            return 'SKIP', 'already set'
        status, resp = api_put(
            f'/metafields/{existing_id}.json',
            {'metafield': {'id': existing_id, 'value': value, 'type': mf_type}},
        )
        return status, resp
    else:
        status, resp = api_post(
            f'/collections/{collection_id}/metafields.json',
            {'metafield': {
                'namespace': namespace,
                'key': key,
                'value': value,
                'type': mf_type,
            }},
        )
        return status, resp


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"{'DRY RUN' if DRY_RUN else 'LIVE RUN'} — {STORE}")
    print(f"Mapping covers {len(MAPPING)} handles\n")

    # Resolve each mapped handle to a collection ID via per-handle API calls.
    # This avoids pagination issues with the bulk endpoint (324 total collections,
    # only 250 returned per page; base collections span both pages).
    print("Resolving collection IDs for all mapped handles...")
    rows = []
    missing = []
    not_base = []

    for handle in sorted(MAPPING.keys()):
        parent_handle, parent_title = MAPPING[handle]
        col = fetch_collection_by_handle(handle)
        time.sleep(0.6)
        if col is None:
            missing.append(handle)
            continue
        if col.get('template_suffix') != 'base':
            not_base.append((handle, col.get('template_suffix', '')))
            continue
        rows.append({
            'id': col['id'],
            'handle': handle,
            'title': col.get('title', ''),
            'parent_handle': parent_handle,
            'parent_title': parent_title,
        })

    print(f"To configure : {len(rows)}")
    print(f"Not base     : {len(not_base)}")
    print(f"Not found    : {len(missing)}")
    if not_base:
        for h, s in not_base:
            print(f"  NOT_BASE  {h}  (suffix={s!r})")
    if missing:
        for h in missing:
            print(f"  MISSING   {h}")

    print()
    print(f"{'HANDLE':<40} {'PARENT HANDLE':<25} PARENT TITLE")
    print('-' * 90)
    for r in rows:
        print(f"  {r['handle']:<38} {r['parent_handle']:<25} {r['parent_title']}")

    if DRY_RUN:
        print(f"\nDry-run complete. Pass --live to apply.")
        return

    # Execute
    # Let the rate limit bucket refill before starting bulk writes
    print("\nPausing 10s to let API rate limit bucket refill before bulk writes...")
    time.sleep(10)
    print(f"Setting metafields for {len(rows)} collections...")
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    log = []
    ok = skip = fail = 0

    for r in rows:
        col_id = r['id']
        handle = r['handle']

        # Set parent_hub_handle  (GET + POST/PUT = 2 calls, ~1s each to stay within rate limit)
        time.sleep(1.0)
        s1, _ = set_metafield(col_id, 'bbi', 'parent_hub_handle', r['parent_handle'])
        # Set parent_hub_title
        time.sleep(1.0)
        s2, _ = set_metafield(col_id, 'bbi', 'parent_hub_title', r['parent_title'])

        if s1 == 'SKIP' and s2 == 'SKIP':
            print(f"  SKIP  {handle}")
            skip += 1
        elif (s1 in (200, 201) or s1 == 'SKIP') and (s2 in (200, 201) or s2 == 'SKIP'):
            print(f"  OK    {handle}  → {r['parent_handle']}")
            ok += 1
        else:
            print(f"  ERR   {handle}  s_handle={s1}  s_title={s2}")
            fail += 1

        log.append({**r, 'status_handle': str(s1), 'status_title': str(s2)})

    log_path = Path(f'data/logs/set-parent-metafields-{ts}.json')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2))

    print(f"\nDone: {ok} ok, {skip} already-set skipped, {fail} failed")
    print(f"Log: {log_path}")


if __name__ == '__main__':
    main()
