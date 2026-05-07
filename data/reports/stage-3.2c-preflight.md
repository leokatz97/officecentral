# Stage 3.2c — Pre-flight Report

**Generated:** 2026-05-07  
**Branch:** chore/stage-3.2c-subcollection-migration  
**Inputs:** stage-3.2a.5-migration-plan.md, stage-3.2a.5-collection-inventory.csv, stage-3.2a.5-legacy-vs-new.csv

---

## Verification Checks ✅

| Check | Result |
|---|---|
| Working directory | /Users/leokatz/Desktop/Office Central |
| Branch | main |
| stage-3.2a.5-collection-inventory.csv | ✅ exists |
| stage-3.2a.5-legacy-vs-new.csv | ✅ exists |
| stage-3.2a.5-migration-plan.md | ✅ exists |
| stage-3.2a.5-root-cause-analysis.md | ✅ exists |
| scripts/set-sub-collection-suffix.py | ✅ exists, has --dry-run (default) / --live flag |
| scripts/set-base-collection-schemas.py | ✅ exists, has --live flag (see Phase 2 note) |

---

## §1 — 56-handle flip list (from migration plan §1)

Confirmed: exactly 56 handles, verified via `python3 -c` count.

| Hub | Count |
|---|---|
| Seating | 15 |
| Desks | 9 |
| Storage | 13 |
| Tables | 10 |
| Boardroom | 2 |
| Ergonomic Products | 4 |
| Panels & Room Dividers | 3 |
| **Total** | **56** |

Script updated from original 68-handle list. Excluded:
- **highback-seating** — already migrated in Stage 3.2b
- **audio-visual-equipment, chair-accessories, anti-fatigue-mats, technology** — 0-product collections, migration plan §6 says no flip needed
- **metal-shelving** — not in migration plan §1 (not in populated-legacy inventory)
- **monitor-accessories, filing-accessories, mobility-aids, phone-booths, meeting-pods** — don't exist in Shopify

Dry-run result (56-handle list): `To update: 56 / Already ok: 0 / Missing: 0` — clean.

---

## §2 — 93-handle schema config list

Per migration plan §3: 56 newly-flipped + 36 Stage 1.6 shells + 1 highback-seating = 93.  
**Actual pre-flip base count from API:** 32 (31 Stage 1.6 shells + highback-seating).  
This means 5 fewer shells than the migration plan estimated — either they don't exist or are smart collections not custom collections. Does not affect Phase 3 execution.

---

## §3 — Orphan shells flagged for review

| Handle | Title | Products | Stage 1.6 shell ID | Conceptual overlap |
|---|---|---|---|---|
| boardroom-seating | Boardroom Seating | 0 | 526867398969 | boardroom-conference-meeting (11 products) |
| collaborative-tables | Collaborative Tables | 0 | 526867824953 | meeting-tables (12 products) |

Both are referenced by hub tiles (boardroom hub → boardroom-seating; tables hub → collaborative-tables). Both legacy counterparts are in the 56-handle flip list.

---

## CRITICAL — Phase 2 Schema Config API Limitation (HALT on Phase 4)

**Finding:** `scripts/set-base-collection-schemas.py` cannot push per-collection section settings, even with `--live`. The `DRY_RUN` variable is declared on line 52 but **never used** in any conditional branch. Running `--live` is identical to dry-run.

The script's own docstring (lines 24–42) documents this explicitly:
> "Per-collection section settings... are NOT accessible via the Assets API. The correct way to set per-collection section settings is via the Shopify Admin UI or the undocumented /admin/api/.../themes/:id/section_settings.json endpoint (unavailable on Basic plan)."

**Impact:** Phase 4 bulk schema config cannot proceed via script. Per-collection `parent_category_handle` and `parent_category_title` must be set manually in Theme Editor, or via metafields refactor, or after a plan upgrade.

**Alternatives (see execution report §Phase 2 for full analysis):**
1. Manual Theme Editor pass (93 collections × ~30 seconds = ~45 min)
2. Metafield-based derivation (refactor `ds-cs-base.liquid` to read hub from collection tags)
3. Shopify plan upgrade to unlock section_settings API

**Phase 4 status: HALTED. Phase 3 (flip) proceeds — it is independent.**
