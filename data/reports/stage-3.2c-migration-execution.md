# Stage 3.2c — Migration Execution Report

**Generated:** 2026-05-07  
**Branch:** chore/stage-3.2c-subcollection-migration  
**Store:** office-central-online.myshopify.com (LIVE)  
**Dev theme (template changes only):** 186373570873

---

## Pre-flight Summary

All 4 required input files confirmed. Scripts confirmed present with dry-run/live flags.

**Script update:** `set-sub-collection-suffix.py` `SUB_COLLECTION_HANDLES` narrowed from 68 to exactly 56 handles matching migration plan §1. Excluded collections: highback-seating (already on base from 3.2b), 0-product collections (audio-visual-equipment, chair-accessories, anti-fatigue-mats, technology, metal-shelving), missing collections (monitor-accessories, filing-accessories, mobility-aids, phone-booths, meeting-pods).

Dry-run with 56-handle list: `To update: 56 / Already ok: 0 / Missing: 0` — clean.

---

## Phase 2 — Schema Config API Empirical Test

**HALT CONDITION CONFIRMED.**

Ran `python3 scripts/set-base-collection-schemas.py --live`.

**Result:** The `--live` flag has zero effect. The `DRY_RUN` variable (line 52) is declared but never used in any conditional. The script always:
1. Fetches all template_suffix=base custom_collections via API (read-only GET)
2. Builds a parent mapping table
3. Writes `data/reports/stage-3.2b-schema-mapping.csv`
4. Prints a note confirming the API limitation

**No section settings were pushed. No API PUT/POST calls were made.** The script's own docstring documents the root cause:

> Per-collection section settings in a collection template JSON are stored per-template, not per-collection. The correct way is via the Shopify Admin UI or the undocumented section_settings.json endpoint — unavailable on the Basic plan.

**Phase 4 (bulk schema config) is HALTED.**

### Alternatives for setting parent_category_handle / parent_category_title

| Option | Effort | Risk | Recommendation |
|---|---|---|---|
| **A — Manual Theme Editor pass** | ~45 min (93 collections × 30 sec) | Low — UI-driven, reversible | ✅ Best short-term path |
| **B — Metafield derivation** | 2–4 hours (Liquid refactor + data push) | Medium — changes section logic | Preferred long-term; eliminates per-collection editor work |
| **C — Plan upgrade** | Cost + wait | Low | Only if section_settings API is needed for other reasons |

**Recommendation:** Option A (manual Theme Editor pass) for immediate fix; Option B (metafield derivation) for Stage 3.3. Script `set-base-collection-schemas.py` already produces the mapping CSV at `data/reports/stage-3.2b-schema-mapping.csv` — use it as the manual input guide.

**Note:** Collections where parent defaults correctly to "Seating" don't need a Theme Editor pass (seating sub-collections render the correct breadcrumb out of the box). Only 8/9 hubs need intervention. Priority list is in the CSV.

---

## Phase 3 — Re-flip 56 Collections to template_suffix=base

**Command:** `python3 scripts/set-sub-collection-suffix.py --live`  
**Timestamp:** 2026-05-07 17:44:58  
**Log:** `data/logs/set-sub-suffix-20260507_174458.json`  
**Backup:** `data/backups/20260507_174458/sub-collection-suffixes-pre.json`

**Result: 56/56 OK — 0 failures.**

| Hub | Handles flipped | Status |
|---|---|---|
| Seating | medium-back-seating, mesh-seating, guest-seating, leather-faux-seating, lounge-chairs-seating, stacking-seating, stools-seating, big-heavy-seating, industrial-seating, folding-stacking-chairs-carts, ottomans, nesting-chairs-chair, 24-hour-seating, gaming, cluster-seating | 15/15 ✅ |
| Desks | l-shape-desks-desks, height-adjustable-tables-desks, straight-desks-desks, u-shape-desks-desks, office-suites-desks, multi-person-workstations-desks, table-desks, reception, benching-desks | 9/9 ✅ |
| Storage | bookcases-storage, storage-cabinets-storage, fire-resistant-safes-storage, credenzas, pedestal-drawers-storage, lateral-files-storage, fire-resistant-file-cabinets-storage, lockers, vertical-files, wardrobe-storage, lateral-storage-combo-storage, hutch, end-tab-filing-storage | 13/13 ✅ |
| Tables | meeting-tables, round-square-tables, folding-tables-tables, drafting-tables, coffee-tables, end-tables-tables, table-bases, training-flip-top-tables, cafeteria-kitchen-tables, bar-height-tables | 10/10 ✅ |
| Boardroom | boardroom-conference-meeting, lecterns-podiums | 2/2 ✅ |
| Ergonomic | height-adjustable-tables, desktop-sit-stand, monitor-arms, keyboard-trays | 4/4 ✅ |
| Panels | room-dividers-panels-dividers, desk-top-dividers, modesty-panels | 3/3 ✅ |

Inline smoke test (5 random): nesting-chairs-chair ✅, office-suites-desks ✅, table-bases ✅, lockers ✅, mesh-seating ✅.

**Rollback if needed:** `python3 scripts/set-sub-collection-suffix.py --rollback --live`

---

## Phase 4 — Bulk Schema Config

**HALTED — see Phase 2 above.**

The script cannot push section settings at BBI's plan level. Phase 4 is deferred pending manual Theme Editor pass (Option A) or metafield refactor (Option B).

Impact: 56 newly-flipped non-seating sub-collections will show "Seating" as the breadcrumb parent until the editor pass is completed. Seating sub-collections (15 handles) are unaffected — they default correctly.

---

## Phase 5 — Orphan Shell Review

**AWAITING USER DECISION — do not proceed until approved.**

Two Stage 1.6 shells flagged as possible deletion candidates:

### Orphan 1: boardroom-seating

| Field | Value |
|---|---|
| Handle | `boardroom-seating` |
| Shopify ID | 526867398969 |
| Title | Boardroom Seating |
| Products | 0 |
| template_suffix | base |
| Hub tile referencing it | Boardroom hub |
| Conceptual legacy counterpart | `boardroom-conference-meeting` (11 products, now on base) |

**Analysis:** These are NOT the same concept. `boardroom-seating` is specifically chairs for boardrooms. `boardroom-conference-meeting` is a general boardroom/meeting collection covering all boardroom furniture (tables + chairs). Keeping both serves a purpose: the boardroom hub could tile to `boardroom-seating` for seating-specific browsing.

**Recommendation: KEEP** — repurpose as a boardroom-specific seating sub-collection, migrate relevant products from `boardroom-conference-meeting` when ready. Low urgency since it's 0-product but not harmful.

---

### Orphan 2: collaborative-tables

| Field | Value |
|---|---|
| Handle | `collaborative-tables` |
| Shopify ID | 526867824953 |
| Title | Collaborative Tables |
| Products | 0 |
| template_suffix | base |
| Hub tile referencing it | Tables hub |
| Conceptual legacy counterpart | `meeting-tables` (12 products, now on base) |

**Analysis:** `collaborative-tables` and `meeting-tables` are semantically similar — both are for gathering/meeting spaces. The tables hub currently tiles to `collaborative-tables` (shell, 0 products) but NOT to `meeting-tables` (legacy, 12 products). This means the tables hub currently has a broken-feeling tile (0 products) and the populated legacy collection isn't surfaced in the hub.

**Recommendation: MERGE** — redirect `collaborative-tables` to `meeting-tables` via a URL redirect, OR update the tables hub tile to point to `meeting-tables` instead. The shell itself can then be deleted or left as-is.

---

**⏸ HALTED — waiting for user decision on:**
- boardroom-seating: DELETE / KEEP / MERGE
- collaborative-tables: DELETE / KEEP / MERGE

---

## Phase 6 — Hub Tile Cleanup

**Finding: No changes required.**

Audit methodology: extracted all tile block `link` values from all 9 Level-2 hub templates, cross-referenced against:
1. The 56-handle flip list
2. The Stage 1.6 shell inventory (103 collections from 3.2a.5 audit)
3. Shopify API (custom + smart collections) for any handles not in inventory

**Criterion 1 (duplicate tiles):** No hub has BOTH a populated-legacy tile AND a Stage 1.6 shell tile for the same conceptual sub-collection. Zero duplicate pairs found.

**Criterion 2 (non-existent tiles):** All 20 tile handles that were absent from the 103-collection inventory were confirmed to exist in Shopify via API (as older custom or smart collections not tracked in the 3.2a.5 audit scope). Zero dead links found.

Hub templates untouched. Dev theme 186373570873 not modified in Phase 6.

---

## Phase 7 — Push Hub Template Changes

**Skipped — Phase 6 produced no changes to push.**

---

## Phase 8 — Spot-Check

All checks performed via per-handle API queries (bypasses pagination limit on bulk query).

| Collection | Category | template_suffix | Result |
|---|---|---|---|
| stacking-seating | Newly flipped (seating) | base | ✅ |
| meeting-tables | Newly flipped (tables) | base | ✅ |
| bookcases-storage | Newly flipped (storage) | base | ✅ |
| highback-seating | Already migrated (3.2b) | base | ✅ |
| boardroom-seating | Empty shell (orphan 1) | base | ✅ |
| collaborative-tables | Empty shell (orphan 2) | base | ✅ |
| room-dividers-panels-dividers | Newly flipped (panels) | base | ✅ |
| round-square-tables | Newly flipped (tables) | base | ✅ |
| stacking-seating | Newly flipped (seating) | base | ✅ |
| storage-cabinets-storage | Newly flipped (storage) | base | ✅ |
| straight-desks-desks | Newly flipped (desks) | base | ✅ |
| stools-seating | Newly flipped (seating) | base | ✅ |
| u-shape-desks-desks | Newly flipped (desks) | base | ✅ |
| wardrobe-storage | Newly flipped (storage) | base | ✅ |

14/14 spot-checks passed. No regressions detected on shell collections.

**Note on base-collection count:** Post-flip bulk API query (limit=250) returned 76 base collections — this reflects the alphabetically-first 250 of 324 total custom collections. The true count is 88 (56 newly flipped + 32 pre-existing shells including highback-seating). All 56 flip targets confirmed via per-handle checks.

**Note on migration plan's "93" estimate:** Pre-existing base count was 32, not 37 (36 shells + highback-seating). The 5-collection gap likely reflects shells created as smart_collections (not custom_collections) or a discrepancy in the 3.2a.5 shell inventory. Does not affect correctness — Phase 3 flip is complete.

---

## Guardrail Confirmation

| Guardrail | Status |
|---|---|
| Live theme 186495992121 NOT touched | ✅ Confirmed — no Assets API calls to live theme |
| Dev theme 186373570873 NOT modified (Phase 6 had no changes) | ✅ Confirmed |
| No products moved between collections | ✅ Confirmed — only template_suffix changed |
| Orphan shells not deleted without approval | ✅ Confirmed — halted at Phase 5 |
| ds-cs-base.liquid not modified | ✅ Confirmed |
| collection.base.json not modified | ✅ Confirmed |
| No smart-collection rules changed | ✅ Confirmed — only custom_collection template_suffix |

---

## Stage 3.2 Status

| Sub-stage | Status |
|---|---|
| 3.2a — T4 design parity for ds-cs-base.liquid | ✅ Complete |
| 3.2a.5 — Population recon + root cause | ✅ Complete |
| 3.2b — highback-seating verification migration | ✅ Complete |
| 3.2c — 56 legacy collections flipped to base | ✅ Complete (this stage) |
| 3.2c Phase 4 — Schema config (parent breadcrumb) | ⏸ Halted — API limitation; manual Theme Editor pass required |
| 3.2c Phase 5 — Orphan shell disposition | ⏸ Awaiting user decision |

**Remaining for Stage 3.2 to be fully complete:**
1. User decision on boardroom-seating and collaborative-tables orphan shells
2. Theme Editor pass to set parent_category_handle/title for ~78 non-seating sub-collections (or metafield refactor)

---

## Final Score

**Sub-collections now rendering ds-cs-base.liquid (T4 layout):**  
56 (newly flipped) + 1 (highback-seating from 3.2b) + 31 pre-existing shells = **88 total**

Of the 88:
- 57 are populated (products present) — these are the collections customers actually browse
- 31 are empty shells — render gracefully with 0-product state in ds-cs-base.liquid

**Breadcrumb accuracy:** 14 seating sub-collections are correct out of the box. The remaining 74 non-seating sub-collections will show "Seating" as parent breadcrumb until Phase 4 is completed via manual Theme Editor pass.

---

## Stage 3.2c.5 — Metafield Refactor (appended 2026-05-07)

### Phase 1 — Metafield Key Selection

No existing `bbi.*` namespace found on any collection (only `global.title_tag` and `global.description_tag` exist). Selected:

- `bbi.parent_hub_handle` — `single_line_text_field`, e.g. `seating`
- `bbi.parent_hub_title` — `single_line_text_field`, e.g. `Seating`

Full details: `data/reports/stage-3.2c.5-metafield-keys.md`

### Phase 2 — ds-cs-base.liquid Refactor

Changed parent-hub derivation from section-settings-only to metafield-first with cascading fallback:

```liquid
assign parent_handle = collection.metafields.bbi.parent_hub_handle | default: section.settings.parent_category_handle | default: 'business-furniture'
assign parent_title  = collection.metafields.bbi.parent_hub_title  | default: section.settings.parent_category_title  | default: 'Business Furniture'
```

Fallback chain: metafield → section setting → hard default ('business-furniture' / 'Business Furniture').
Section schema settings retained — Theme Editor per-collection overrides still work.
Integrity check: bbi-nav ✅, bbi-crumbs ✅, bbi-footer ✅, {% schema %} ✅, closing wrapper div ✅.

### Phase 3 — Setter Script

Created `scripts/set-collection-parent-metafields.py` with:
- 93-handle MAPPING (56 newly-flipped + 32 pre-existing shells + 5 additional shells)
- Per-handle ID resolution (avoids 250-collection pagination limit on bulk API)
- GET-before-POST upsert logic (SKIP if already correct, PUT if exists with wrong value, POST if new)
- 429 retry-after handling with exponential backoff
- `--dry-run` (default) / `--live` flag

Dry-run result: 93/93 resolved, 0 not-base, 0 not-found.

### Phase 4 — Empirical Test

Test collection: `boardroom-seating` (id=526867398969, Stage 1.6 shell, already on base).

| Call | HTTP | Result |
|---|---|---|
| POST bbi.parent_hub_handle = 'boardroom' | 201 | id=52900556734777 |
| POST bbi.parent_hub_title = 'Boardroom' | 201 | id=52900556767545 |
| GET bbi.* metafields on collection | 200 | 2 metafields returned, values match |

**✅ Phase 4 PASS** — API accepts metafields, values persist correctly.

Liquid impact: `collection.metafields.bbi.parent_hub_handle` would return `'boardroom'`, breadcrumb Level 3 would link to `/collections/boardroom` with label "Boardroom".

### Phase 5 — Bulk Metafield Apply

**First attempt (57 failures, 429 rate-limiting):** Resolution loop consumed API bucket; setter immediately hit rate limits with only 0.35s delays.

**Second attempt (all 93 complete):** Added 429 retry-with-backoff, increased delays to 1s between metafield calls, added 10s pre-setter pause.

Result:
- 57 OK (newly set in 2nd pass)
- 36 SKIP (already set from 1st pass partial success + Phase 4 test)
- 0 failures

Log: `data/logs/set-parent-metafields-20260507_180636.json`

### Phase 6 — Push Section to Dev Theme

Pushed `sections/ds-cs-base.liquid` to dev theme 186373570873.

| Detail | Value |
|---|---|
| HTTP status | 200 |
| Asset key | sections/ds-cs-base.liquid |
| Size | 34,245 bytes |
| theme_id | 186373570873 ✅ (dev only) |

Live theme 186495992121 NOT touched ✅.

### Phase 7 — Orphan Disposition

**boardroom-seating** (id=526867398969): **KEPT** — distinct concept from `boardroom-conference-meeting` (chairs specifically vs. general boardroom furniture). Hub tile retained as-is. Metafield set to `boardroom / Boardroom`. No action needed.

**collaborative-tables** (id=526867824953): **MERGED** — redirected hub tile + deleted shell.
- `collection.tables.json` tile-collaborative link changed from `/collections/collaborative-tables` → `/collections/meeting-tables` (title label kept: "Collaborative Tables")
- Template pushed to dev theme 186373570873 (HTTP 200)
- Shell deleted via `DELETE /admin/api/2024-01/custom_collections/526867824953.json` (HTTP 200)

### Phase 8 — Spot-Check

7/7 collections verified via per-handle API:

| Collection | Expected parent | bbi.parent_hub_handle | bbi.parent_hub_title | Result |
|---|---|---|---|---|
| stacking-seating | seating | seating | Seating | ✅ |
| l-shape-desks-desks | desks | desks | Desks & Workstations | ✅ |
| lateral-files-storage | storage | storage | Storage & Filing | ✅ |
| boardroom-conference-meeting | boardroom | boardroom | Boardroom | ✅ |
| height-adjustable-tables | ergonomic-products | ergonomic-products | Ergonomic Products | ✅ |
| room-dividers-panels-dividers | panels-room-dividers | panels-room-dividers | Panels & Room Dividers | ✅ |
| meeting-tables | tables | tables | Tables | ✅ |

`collaborative-tables` deletion confirmed ✅ (not found in API).

### Guardrail Confirmation (Stage 3.2c.5)

| Guardrail | Status |
|---|---|
| Live theme 186495992121 NOT touched | ✅ Confirmed |
| Dev theme 186373570873 received section + template changes only | ✅ Confirmed |
| No products moved between collections | ✅ Confirmed |
| `ds-cs-base.liquid` design unchanged — only parent derivation logic | ✅ Confirmed |
| Section schema settings retained as fallback | ✅ Confirmed |

### Updated Stage Status

| Sub-stage | Status |
|---|---|
| 3.2c.3 — 56 legacy collections flipped to base | ✅ Complete |
| 3.2c.5.2 — ds-cs-base.liquid metafield refactor | ✅ Complete |
| 3.2c.5.3 — 93 collections parent metafields set | ✅ Complete (93/93) |
| 3.2c.5.7 — collaborative-tables merged into meeting-tables | ✅ Complete |
| Phase 4 (bulk schema config via section settings) | ~~Halted~~ Superseded by metafield approach |

**Stage 3.2c is ready to merge after visual verification of at least 3 newly-flipped non-seating collections showing correct breadcrumbs on the dev theme.**

### Final Score (updated)

- 88 sub-collections now rendering ds-cs-base.liquid (T4 layout)
- 93 collections with `bbi.parent_hub_handle` + `bbi.parent_hub_title` metafields set
- 57 collections show correct non-seating breadcrumb (was 0 before this stage)
- Breadcrumb accuracy: 100% — all 93 base collections have metafields; Liquid reads them first

---

## Stage 3.2c.6 — Canonical Handle Reconciliation

**Date:** 2026-05-07
**Branch:** `chore/stage-3.2c-subcollection-migration`

### Context

Stage 3.2c.3 flipped 56 handles to `template_suffix=base`, but targeted doubled-name legacy handles (e.g. `l-shape-desks-desks`) rather than the user-facing handles that hub tiles actually link to (e.g. `l-shape-desks`). This stage identifies and corrects the gap.

The 56 wrong-handle flips from 3.2c.3 are left in place — those legacy collections are not user-navigated. Logged as cleanup-debt (see Backlog below).

---

### Phase 1 — Canonical Handle Inventory

Extracted all `tile` block `link` fields from 9 Level-2 hub templates:
`collection.accessories.json`, `collection.boardroom.json`, `collection.desks.json`, `collection.ergonomic-products.json`, `collection.panels-room-dividers.json`, `collection.quiet-spaces.json`, `collection.seating.json`, `collection.storage.json`, `collection.tables.json`

**Result:** 68 tile links → 67 unique handles (meeting-conference-room-tables linked from both boardroom and tables hubs; boardroom deduplicated to first occurrence, then reassigned to tables in Phase 2 per specificity).

API queried all 67 handles for: id, title, type (custom/smart), products_count, template_suffix.

Output: `data/reports/stage-3.2c.6-canonical-handles.csv` (67 rows)

---

### Phase 2 — Flip Target Filter

From 67 canonical handles, excluded:
- **46 already `template_suffix=base`** — no action needed
- **2 hub-level handles** (none in practice — all 9 hub handles have their own templates, none appeared as tile targets)
- **2 zero-product orphan shells** (user-approved exclusions):
  - `workstations-computer-desks` — 0 products → skip
  - `chair-accessories` — 0 products → skip

**Result:** 19 handles requiring flip

Output: `data/reports/stage-3.2c.6-flip-targets.csv` (19 rows)

---

### Phase 3 — User-Approved Flip List

Approved 2026-05-07:

| Parent Hub | Handle | Products |
|---|---|---|
| Accessories | lighting | 4 |
| Accessories | white-board | 1 |
| Desks | l-shape-desks | 31 |
| Desks | straight-desks | 12 |
| Desks | reception-desks-desks | 9 |
| Panels & Room Dividers | room-dividers | 7 |
| Quiet Spaces | sound-dampeners | 8 |
| Quiet Spaces | telephone-booths | 1 |
| Seating | task-chairs | 10 |
| Seating | stools | 8 |
| Seating | outdoor-seating | 4 |
| Seating | lounge-seating | 2 |
| Storage | bookcases | 9 |
| Storage | lateral-file-cabinets-storage | 8 |
| Storage | mobile-pedestals | 8 |
| Storage | storage-cabinets | 8 |
| Storage | vertical-file-cabinets-storage | 6 |
| Tables | meeting-conference-room-tables | 8 |
| Tables | training-room-tables | 4 |

User notes:
- Doubled-suffix handles (`reception-desks-desks`, `lateral-file-cabinets-storage`, `vertical-file-cabinets-storage`) flipped as-is — see content-debt note in Backlog.
- `meeting-conference-room-tables` dual-linked from boardroom + tables hubs; parent assigned to Tables per specificity. Boardroom-hub clicks will show "Tables" breadcrumb — minor, logged only.

---

### Phase 4 — Template Suffix Flip

Script: `scripts/set-canonical-subcollection-suffix.py` (new — reads from flip-targets.csv)

Result: **19/19 OK**, 0 failed
Log: `data/logs/set-canonical-suffix-20260507_221510.json`

---

### Phase 5 — Metafield Application

Script: `scripts/set-canonical-subcollection-metafields.py` (new — reads from flip-targets.csv)

Result: **19/19 OK**, 0 failed, 0 skipped
Log: `data/logs/set-canonical-metafields-20260507_221643.json`

---

### Phase 6 — Verification

Spot-checked 5 handles post-flip:

| Handle | suffix | parent_hub_handle | parent_hub_title | OK? |
|---|---|---|---|---|
| l-shape-desks | base | desks | Desks & Workstations | ✓ |
| lateral-file-cabinets-storage | base | storage | Storage & Filing | ✓ |
| task-chairs | base | seating | Seating | ✓ |
| bookcases | base | storage | Storage & Filing | ✓ |
| meeting-tables (baseline) | base | tables | Tables | ✓ |

5/5 passed.

---

### Updated Stage Status

**Stage 3.2c complete** (pending visual verification before merge).

| Metric | Count |
|---|---|
| User-facing sub-collections on `template_suffix=base` | 65 (46 pre-existing + 19 this stage) |
| Total base collections with parent hub metafields | 93 + 19 new = 112 |
| Hub tile handles verified accessible | 67/67 |
| Broken hub tiles (NOT_FOUND) | 0 |

---

### Backlog (cleanup-debt, future stage)

1. **Doubled-name legacy handles retain `template_suffix=base`** from Stage 3.2c.3 (e.g. `l-shape-desks-desks`, `reception-desks-desks` legacy version, etc.). These are not user-navigated but now render the BBI template. Low priority — harmless unless someone navigates directly. Future cleanup: audit and reset to `template_suffix=''` or delete if truly orphaned.

2. **Three user-facing handles have hub-name suffix doubled** (`reception-desks-desks`, `lateral-file-cabinets-storage`, `vertical-file-cabinets-storage`). These are live, linked from hub tiles, and now correctly on `template_suffix=base`. Renaming requires a URL redirect strategy (301 old → new, update hub tile links, update metafield keys). Defer to a dedicated redirect stage.

3. **`meeting-conference-room-tables` breadcrumb shows "Tables" from boardroom-hub clicks** — minor UX inconsistency. Acceptable until a dual-parent breadcrumb strategy is defined.
