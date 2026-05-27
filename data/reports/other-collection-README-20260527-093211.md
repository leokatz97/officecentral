# Other Collection — Steve's Worksheet (v3 — full fixes)

**Generated:** 20260527-093211  |  **Products:** 338  |  **Est time:** ~45 min

## v3 changes vs v2

| Improvement | v2 | v3 |
|---|---|---|
| Routable sub-collections | 208 | **139** (filtered) |
| Duplicate-title collections | 16 clusters mixed in | Canonical picked, 18 losers excluded |
| `all-*` mega-aggregators | included | 17 excluded (auto-populated from children) |
| Empty published collections | included | 23 excluded |
| Existing metafields per product | not surfaced | **shown** in `existing_metafields` col |
| Variant options per product | not surfaced | **shown** in `variant_options` col |
| Inventory + price status | not surfaced | **shown** in `inventory_status` col |
| Tier A enriched flag | n/a | **shown** in `tier_a_enriched` col |
| Smart-routing recipes | unknown | encoded in picklist `add_method` + `add_instruction` |

## Claude's confidence

- HIGH: 46 (13%)  ← scan, type Y
- MED:  146 (43%)
- LOW:  75 (22%)
- NONE: 71 (21%)

## Workflow

For each row:
- **Y** in `accept_recommendations` → done
- Override in `override_sub_collection_1/2/3` (use only handles where `routable=Y` in picklist)
- `leave_in_other=Y` or `archive_this=Y` to skip
- Rows with `tier_a_enriched=Y` → SKIP (Leo handles separately)

## Picklist (v3 has 9 columns)

- title, handle, type
- **routable** (Y/N) — only Y values are valid targets
- products_count
- add_method — collects-post / tag-write / tag-write-multi / complex
- add_instruction — exact ingest action
- non_routable_reasons — why a row is N

## Canonical-handle decisions (sample)

When multiple handles share a title, the one with more products won:
- **accessories** → `accessories` (22 products); excluded: `type-accessories`(22)
- **boardroom** → `boardroom` (25 products); excluded: `room-boardroom`(25)
- **chairs** → `type-chairs` (121 products); excluded: `chairs`(4)
- **lounge** → `lounge` (10 products); excluded: `room-lounge`(6)
- **lounge seating** → `type-lounge` (6 products); excluded: `lounge-seating`(2)

Full decision log: `data/reports/canonical-decisions-20260527-093211.csv`

## Files

- Products: `data/reports/other-collection-products-20260527-093211-with-recs.csv`
- Picklists: `data/reports/other-collection-picklists-20260527-093211.csv`
- Canonical: `data/reports/canonical-decisions-20260527-093211.csv`
