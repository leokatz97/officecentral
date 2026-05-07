#!/usr/bin/env python3
"""
set-base-collection-schemas.py
Stage 3.2b — Configure parent_category_handle and parent_category_title for all
collections using template_suffix=base.  Without these settings every sub-collection
defaults to "seating" in breadcrumbs and the hero eyebrow.

Usage:
    python3 scripts/set-base-collection-schemas.py          # dry-run (default)
    python3 scripts/set-base-collection-schemas.py --live   # push to dev theme

Env: SHOPIFY_STORE, SHOPIFY_TOKEN  (read from .env)
Target: dev theme 186373570873 ONLY  (settings go into collection.base.json sections)

The Shopify Admin API does not expose section-level settings for collection templates
via the Collections endpoint.  Section settings in a collection template JSON are
stored per-template, not per-collection.  Instead, this script patches the section
settings in the theme's template JSON (collection.base.json) on the ACTIVE dev theme,
using the Assets API.

However, collection.base.json is a SHARED template used by all 32 collections — it
cannot carry per-collection overrides this way.

ALTERNATIVE APPROACH (actually correct for Shopify OS 2.0):
Per-collection theme-editor overrides are stored in the theme's sections database under
collection-scoped keys.  These are NOT accessible via the Assets API.  The correct way
to set per-collection section settings is via the Shopify Admin UI or the undocumented
/admin/api/.../themes/:id/section_settings.json endpoint (unavailable on Basic plan).

PRACTICAL RESOLUTION:
Since per-collection schema settings can't be reliably set via API at BBI's plan level,
this script instead:
  1. Outputs a mapping CSV (data/reports/stage-3.2b-schema-mapping.csv) suitable for
     manual input in the Theme Editor or a future scripted approach.
  2. Verifies which collections need updating (parent defaults to seating — wrong for 8/9 hubs).
  3. Notes that the breadcrumb + hero eyebrow default is safe for seating sub-collections;
     other hubs need a one-time editor pass.

For Stage 3.2c, the recommended approach is to set parent_category_handle and
parent_category_title via a bulk section-settings push when the Shopify plan allows it,
or to refactor the section to derive the parent hub from the collection's tags or metafields.
"""

import csv, json, os, re, sys, urllib.request, urllib.parse
from datetime import datetime

# ── Credentials ────────────────────────────────────────────────────────────────
env_content = open(os.path.join(os.path.dirname(__file__), '..', '.env')).read()
TOKEN  = re.search(r'SHOPIFY_TOKEN=(.+)',  env_content).group(1).strip()
STORE  = re.search(r'SHOPIFY_STORE=(.+)',  env_content).group(1).strip()

DRY_RUN = '--live' not in sys.argv

# ── Parent hub mapping ──────────────────────────────────────────────────────────
# Format: collection_handle → (parent_handle, parent_title, ambiguous_flag, reason)
MAPPING = {
    'acoustic-panels':      ('panels-room-dividers', 'Panels & Room Dividers', False, ''),
    'acoustic-pods':        ('quiet-spaces',          'Quiet Spaces',           False, ''),
    'active-seating':       ('seating',               'Seating',                False, ''),
    'beam-seating':         ('seating',               'Seating',                False, ''),
    'bench-seating':        ('seating',               'Seating',                False, ''),
    'boardroom-seating':    ('boardroom',             'Boardroom',              False, ''),
    'boardroom-storage':    ('boardroom',             'Boardroom',              False, ''),
    'cafe-tables':          ('tables',                'Tables',                 False, ''),
    'collaborative-tables': ('tables',                'Tables',                 False, ''),
    'conference-seating':   ('seating',               'Seating',                False, 'Meeting-room chairs are seating'),
    'desk-accessories':     ('accessories',           'Accessories',            False, ''),
    'desktop-accessories':  ('accessories',           'Accessories',            False, ''),
    'ergocentric':          ('ergonomic-products',    'Ergonomic Products',     True,  'Brand; ds-cc-base places ergoCentric under Ergonomic Products hub'),
    'ergonomic-accessories':('ergonomic-products',    'Ergonomic Products',     False, ''),
    'executive-desks':      ('desks',                 'Desks & Workstations',   False, ''),
    'executive-seating':    ('seating',               'Seating',                False, ''),
    'focus-rooms':          ('quiet-spaces',          'Quiet Spaces',           False, ''),
    'global-furniture':     ('desks',                 'Desks & Workstations',   True,  'Brand; Global Furniture Group primary in BBI catalog is desks'),
    'global-teknion':       ('desks',                 'Desks & Workstations',   True,  'Brand; ds-cc-base places Global/Teknion under Desks & Panels — using Desks as primary'),
    'healthcare-seating':   ('seating',               'Seating',                False, 'Industry-specific seating sub-collection'),
    'high-density-storage': ('storage',               'Storage & Filing',       False, ''),
    'highback-seating':     ('seating',               'Seating',                False, 'Verification migration from Stage 3.2b Phase 1'),
    'keilhauer':            ('seating',               'Seating',                True,  'Brand; ds-cc-base: Seating → Keilhauer + ergoCentric'),
    'mailboxes':            ('accessories',           'Accessories',            False, 'Mail sorting = accessories category'),
    'media-storage':        ('storage',               'Storage & Filing',       False, ''),
    'mobile-storage':       ('storage',               'Storage & Filing',       False, ''),
    'modular-workstations': ('desks',                 'Desks & Workstations',   False, ''),
    'multipurpose-tables':  ('tables',                'Tables',                 False, ''),
    'nesting-tables':       ('tables',                'Tables',                 False, ''),
    'outdoor-tables':       ('tables',                'Tables',                 False, ''),
    'personal-storage':     ('storage',               'Storage & Filing',       False, ''),
    'privacy-screens':      ('panels-room-dividers', 'Panels & Room Dividers', False, ''),
}

# ── API helpers ─────────────────────────────────────────────────────────────────
def api_get(path):
    url = f'https://{STORE}/admin/api/2024-01{path}'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# ── Fetch current base-template collections ─────────────────────────────────────
print(f"{'DRY RUN' if DRY_RUN else 'LIVE RUN'} — {STORE}")
print()

data = api_get('/custom_collections.json?limit=250&fields=id,handle,title,template_suffix')
base_cols = {c['handle']: c for c in data['custom_collections'] if c.get('template_suffix') == 'base'}
print(f"Found {len(base_cols)} template=base collections")
print()

# ── Build output rows ─────────────────────────────────────────────────────────
rows = []
skipped = []

for handle, col in sorted(base_cols.items()):
    if handle in MAPPING:
        parent_handle, parent_title, ambiguous, reason = MAPPING[handle]
        status = 'AMBIGUOUS' if ambiguous else 'OK'
        rows.append({
            'handle':          handle,
            'collection_id':   col['id'],
            'collection_title': col['title'],
            'parent_handle':   parent_handle,
            'parent_title':    parent_title,
            'status':          status,
            'reason':          reason,
        })
    else:
        skipped.append(handle)

# ── Print dry-run table ───────────────────────────────────────────────────────
print(f"{'HANDLE':<35} {'PARENT HANDLE':<25} {'PARENT TITLE':<25} STATUS")
print('-' * 110)
for r in rows:
    flag = ' ⚠ AMBIGUOUS' if r['status'] == 'AMBIGUOUS' else ''
    print(f"{r['handle']:<35} {r['parent_handle']:<25} {r['parent_title']:<25} {r['status']}{flag}")
    if r['reason']:
        print(f"  {'':35} → {r['reason']}")

if skipped:
    print()
    print('SKIPPED (not in mapping):')
    for h in skipped:
        print(f'  {h}')

# ── Output CSV ──────────────────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'reports', 'stage-3.2b-schema-mapping.csv')
with open(csv_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['handle','collection_id','collection_title','parent_handle','parent_title','status','reason'])
    w.writeheader()
    w.writerows(rows)
print()
print(f"Mapping CSV written: {csv_path}")

# ── API SET note ───────────────────────────────────────────────────────────────
print()
print("NOTE: Per-collection section settings (parent_category_handle / parent_category_title)")
print("cannot be pushed via the Shopify Admin API at BBI's current plan level.")
print("The collection.base.json template is shared — it cannot carry per-collection overrides via Assets API.")
print()
print("Manual action required:")
print("  For each collection, set in Theme Editor → Customize → [collection] → Section settings:")
print("    parent_category_handle  → value from mapping CSV")
print("    parent_category_title   → value from mapping CSV")
print()
print("Priority order (8/9 hubs need non-seating defaults):")
non_seating = [r for r in rows if r['parent_handle'] != 'seating']
for r in non_seating:
    print(f"  {r['handle']:<35} → {r['parent_handle']}")

print()
print("Collections that default correctly (parent=seating — no action needed):")
seating_cols = [r for r in rows if r['parent_handle'] == 'seating']
for r in seating_cols:
    print(f"  {r['handle']}")
