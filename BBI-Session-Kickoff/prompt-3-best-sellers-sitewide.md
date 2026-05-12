# Prompt 3 (Expanded) — Best-Sellers Sort Site-Wide + PDP Related from Category Best Sellers

**Paste the safety preflight first (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.**

---

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

TWO related tasks, deployed together because they share one infrastructure:

  TASK A — PDP "Other products like this" must always show the
  most-purchased products in the same category. Never empty.

  TASK B — SITE-WIDE: every collection that lists products must sort by
  units sold (best-selling first → newest / never-purchased last) so the
  highest-purchased items always surface at the top.

WHY together: Task A reads from a category collection; if that collection
is sorted best-selling first, Task A's Tier 1 query is just
`collection.products`. One sort policy, two surfaces.

─── How "best-selling" works in Shopify ─────────────────────────────

Shopify exposes a built-in best-selling sort on every collection
(sort_order: "best-selling"). It's auto-computed from order data on a
rolling 90-day window. Higher unit volume ranks first, no sales ranks
last. No metafield maintenance, no nightly job needed. Set the
sort_order on each collection via the Admin API; the theme reads
collection.products in saved sort order natively.

Manual (custom) collections only support sort_order: "manual". Each
must be converted to smart (rule: tag = <handle>) before it can be
given a best-selling sort. The migration script already exists at
scripts/migrate-to-smart-collections.py (built for PB-14 in Wave B).

─── Step 1: Audit current sort orders ───────────────────────────────

export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import os, json, csv, urllib.request
from collections import Counter

STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']

rows = []
for kind, endpoint in [('smart', 'smart_collections'),
                        ('custom', 'custom_collections')]:
    url = f'https://{STORE}/admin/api/2024-04/{endpoint}.json?limit=250'
    while url:
        req = urllib.request.Request(
            url, headers={'X-Shopify-Access-Token': TOKEN})
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            link = r.headers.get('Link', '')
        for c in data.get(endpoint, []):
            rows.append({
                'kind': kind,
                'id': c['id'],
                'handle': c['handle'],
                'title': c['title'],
                'sort_order': c.get('sort_order', 'manual'),
                'published': c.get('published_at') is not None,
            })
        url = None
        for p in link.split(','):
            if 'rel="next"' in p:
                url = p.split(';')[0].strip().strip('<>')
                break

print(f'Total collections: {len(rows)}')
print('Sort order distribution:')
for so, n in Counter(r['sort_order'] for r in rows).most_common():
    print(f'  {so}: {n}')

os.makedirs('data/reports', exist_ok=True)
with open('data/reports/collection-sort-orders.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print('Saved: data/reports/collection-sort-orders.csv')

custom = [r for r in rows if r['kind'] == 'custom']
non_best = [r for r in rows if r['sort_order'] != 'best-selling']
print(f'\nCustom collections (manual sort only): {len(custom)}')
print(f'Collections NOT on best-selling today: {len(non_best)}')
EOF

Report counts before continuing.

─── Step 2: Build exclusions list ───────────────────────────────────

Some collections SHOULD keep their current sort:
  - Hand-curated "featured" collections where order is editorial
  - "New arrivals" type collections where newness > popularity
  - Brand hero lists with intentional sequencing

Create data/reports/collection-sort-exclusions.csv with one column:
  handle
(plus a notes column if you want). Default content: empty (just header).

For each collection in data/reports/collection-sort-orders.csv whose
title or handle suggests editorial curation, add a row. If unsure,
list it and ASK STEVE before bulk-updating manually-curated brand or
"featured" collections.

─── Step 3: Set sort_order = "best-selling" on smart collections ────

DRY RUN first (CONFIRM = False). Inspect the printed plan, then flip
the flag and re-run.

python3 - <<'EOF'
import os, json, csv, time, urllib.request, shutil, datetime

STORE = 'office-central-online.myshopify.com'
TOKEN = os.environ['SHOPIFY_TOKEN']
CONFIRM = False  # ← set True only after dry-run review

exclusions = set()
try:
    with open('data/reports/collection-sort-exclusions.csv') as f:
        exclusions = {r['handle'] for r in csv.DictReader(f) if r.get('handle')}
except FileNotFoundError:
    pass

with open('data/reports/collection-sort-orders.csv') as f:
    rows = list(csv.DictReader(f))

os.makedirs('data/backups', exist_ok=True)
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy('data/reports/collection-sort-orders.csv',
            f'data/backups/collection-sort-orders-pre-{ts}.csv')

targets = [r for r in rows
           if r['kind'] == 'smart'
           and r['sort_order'] != 'best-selling'
           and r['handle'] not in exclusions]

print(f'\nWill update {len(targets)} smart collections to best-selling.')
print(f'Excluded: {len(exclusions)}')
print('\nFirst 15 targets:')
for t in targets[:15]:
    print(f'  {t["handle"]:40s} {t["sort_order"]} → best-selling')

if not CONFIRM:
    print('\nDRY RUN — set CONFIRM = True to execute.')
else:
    print('\nExecuting…')
    for t in targets:
        body = json.dumps({
            'smart_collection': {
                'id': int(t['id']),
                'sort_order': 'best-selling'
            }
        }).encode()
        req = urllib.request.Request(
            f'https://{STORE}/admin/api/2024-04/smart_collections/{t["id"]}.json',
            data=body, method='PUT',
            headers={'X-Shopify-Access-Token': TOKEN,
                     'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as r:
                print(f'  OK  {t["handle"]} ({r.status})')
        except urllib.error.HTTPError as e:
            print(f'  FAIL {t["handle"]} ({e.code}): {e.read().decode()[:120]}')
        time.sleep(0.6)
EOF

For CUSTOM collections that should also be included: convert each to
smart via scripts/migrate-to-smart-collections.py (PB-14), then re-run
Step 1 + Step 3 to pick them up.

─── Step 4: PDP related products — best sellers in category ─────────

File: theme/sections/ds-pdp-base.liquid

Find the existing .pdp-related section and REPLACE its product query
with a 3-tier best-sellers fallback. Each tier reads from a collection
that is now sorted best-selling first (Step 3), so we just slice the
top 4 and exclude the current product.

TIER 1 — Same type-tag category (the smart collection like all-seating
created in SMART-1):

  {%- assign type_tag = product.tags
      | where_exp: "t", "t contains 'type:'" | first -%}
  {%- if type_tag != blank -%}
    {%- assign cat_handle = 'all-' | append: type_tag | remove: 'type:' -%}
    {%- assign tier1_products = collections[cat_handle].products
        | where_exp: "p", "p.id != product.id"
        | slice: 0, 4 -%}
  {%- endif -%}

TIER 2 — Same room-tag (parent category):

  {%- if tier1_products.size == 0 -%}
    {%- assign room_tag = product.tags
        | where_exp: "t", "t contains 'room:'" | first -%}
    {%- if room_tag != blank -%}
      {%- assign room_handle = room_tag | remove: 'room:' -%}
      {%- assign tier2_products = collections[room_handle].products
          | where_exp: "p", "p.id != product.id"
          | slice: 0, 4 -%}
    {%- endif -%}
  {%- endif -%}

TIER 3 — Cross-category best sellers (vertical-wide):

  {%- if tier1_products.size == 0 and tier2_products.size == 0 -%}
    {%- assign tier3_products = collections['all-business-furniture'].products
        | where_exp: "p", "p.id != product.id"
        | slice: 0, 4 -%}
  {%- endif -%}

  {%- assign related_products = tier1_products
      | default: tier2_products
      | default: tier3_products -%}

Heading (dynamic per tier):
  {%- if tier1_products.size > 0 -%}
    <h2 class="pdp-related__title">
      Best sellers in {{ type_tag | remove: 'type:' | replace: '-', ' ' | capitalize }}
    </h2>
  {%- else -%}
    <h2 class="pdp-related__title">Customers also bought</h2>
  {%- endif -%}

Hide the entire section if all three tiers return empty:
  {%- if related_products.size > 0 -%}
    <section class="pdp-related">
      …existing card grid…
    </section>
  {%- endif -%}

─── Step 5: Audit other product-list surfaces ───────────────────────

After Steps 3 and 4, sweep every other place products are listed to
confirm they inherit best-selling order:

  grep -rn 'collections\[' theme/sections/*.liquid theme/snippets/*.liquid

For each match, classify:
  - Iterates a collection's .products and slices → NO CHANGE needed
    (best-selling is now the saved sort)
  - Has an explicit | sort_by: or | sort: filter overriding the
    collection sort_order → FLAG; ask Steve before removing
  - Hand-coded "featured" list (no collection lookup) → intentional
    editorial curation; leave alone, log in exclusions

Output: data/reports/product-list-surfaces-audit.csv with columns:
  file, line, collection_handle, sort_applied, needs_action, notes

─── Step 6: Push + verify ───────────────────────────────────────────

Push the modified theme/sections/ds-pdp-base.liquid via direct API
(mirror the Prompt 0 pattern). Confirm HTTP 200.

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, urllib.request
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']
  THEME = '186373570873'
  with open('theme/sections/ds-pdp-base.liquid', 'rb') as f:
      content = f.read().decode('utf-8')
  body = json.dumps({'asset': {
      'key': 'sections/ds-pdp-base.liquid',
      'value': content
  }}).encode()
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/themes/{THEME}/assets.json',
      data=body, method='PUT',
      headers={'X-Shopify-Access-Token': TOKEN,
               'Content-Type': 'application/json'})
  with urllib.request.urlopen(req) as r:
      print(f'HTTP {r.status}')
  PYEOF

Verify:

A. PDP related products — 3 product states:
   - Hero in a populated category (e.g. an in-stock seating product) —
     Tier 1 fires, heading reads "Best sellers in Seating", products are
     the top 4 sellers of that category, current product is excluded.
   - Niche product with sparse category — Tier 2 (room-tag) fallback
     fires, heading reads "Customers also bought".
   - Edge case ($0 showcase like additional-services) — if no tier
     returns products, the entire .pdp-related section is hidden (no
     empty heading).

B. Collection pages — confirm product order matches units-sold ranking:
   - /collections/all-seating?preview_theme_id=186373570873
   - /collections/all-desks?preview_theme_id=186373570873
   - /collections/business-furniture?preview_theme_id=186373570873
   - /collections/all?preview_theme_id=186373570873

   The first product on each should be the one with the most units
   sold in the last 90 days. Verify against Shopify Admin → Analytics
   → Sales by product.

C. Diff check — compare data/backups/collection-sort-orders-pre-*.csv
   against the live state after Step 3. Only collections in the
   targets list should have changed. Excluded collections must still
   show their original sort.

Commit (two separate commits, one per task):
  "Site-wide: set smart collections sort_order to best-selling"
  "PDP related: 3-tier fallback now sources from category best sellers"
```

---

## Notes for Steve — read before running

**90-day rolling window.** Shopify recalculates best-selling daily based on the last 90 days of orders. So seasonal items will rotate naturally. For a B2B furniture catalog with infrequent but high-volume orders, this works well — a contract win that ships 200 chairs will rocket that chair to the top.

**Brand-new products will sink** until they have orders. If you launch a new SKU you want surfaced, options are: (1) tag it `new` and add a "New arrivals" carousel that's manually curated, or (2) add it to a hand-curated "featured" smart collection that's on the exclusions list. Worth thinking through before bulk-converting.

**Manual collections need conversion to smart** before they can be given a best-selling sort. Most BBI collections should already be smart (Wave B's PB-14 migrated the main ones). The Step 1 audit will surface anything still custom.

**Exclusions list is your editorial control.** Anything where you want manual order — brand callouts, featured "designer's pick", curated bundles — goes in `collection-sort-exclusions.csv`. Default behavior is everything else gets best-selling.
