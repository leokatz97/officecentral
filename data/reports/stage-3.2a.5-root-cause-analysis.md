# Stage 3.2a.5 — Root Cause Analysis

**Generated:** 2026-05-07  
**Method:** Full collection inventory (359 collections via Shopify Admin API) + cross-reference against P3-rollout logs, Stage 1.6 creation records, pre/post backup files, and revert logs.

---

## Verdict: Hypothesis B with a known-documented revert (not a silent failure)

The "31 template=base, 0 products" state that Stage 3.2a observed was caused by two independent operations:

1. **Stage 1.6 created 36 new empty shells** (all with `template_suffix=base`, all with 0 products) to fix hub-tile 404s.
2. **P3-rollout DID execute successfully** on 2026-05-06 23:34 — setting 62 legacy collections to `template_suffix=base` (all 62 returned HTTP 200). **But it was deliberately reverted** the following morning (2026-05-07 12:55-12:56) via `--rollback` mode of the same script.

Stage 3.2a observed the post-revert state: 36 Stage 1.6 shells (empty, base) + `highback-seating` (46 products, base, migrated by Stage 3.2b). The 62 legacy populated collections had their suffix restored to empty.

---

## Evidence Timeline

| Timestamp | Event | Evidence |
|---|---|---|
| 2026-05-06 21:15–23:13 | 4 sub-collection audit runs — all 68 legacy collections show `template_suffix=""` | `data/reports/sub-collection-audit-20260506_211502.csv` through `...231332.csv` |
| 2026-05-06 23:34 | P3-rollout: `set-sub-collection-suffix.py --live` applied `template_suffix=base` to 62/68 legacy collections. 6 didn't exist (no ID in backup). All 62 returned HTTP 200. | `data/logs/set-sub-suffix-20260506_233251.json`, commit `aaa105a` |
| 2026-05-06 (between commits) | Stage 1.6 created 36 new empty shells with `template_suffix=base` | `data/reports/sub-collections-created-stage-1.6.csv`, commit `44fd3c3` |
| 2026-05-07 12:55 | First revert attempt: `--rollback` mode using `custom_collections` endpoint. All 62 returned HTTP 406 (endpoint rejected). | `data/logs/revert-sub-suffix-20260507_125554.json` |
| 2026-05-07 12:56 | Second revert attempt: corrected endpoint. All 62 returned HTTP 200. P3-rollout changes fully reverted. | `data/logs/revert-sub-suffix-20260507_125644.json` |
| 2026-05-07 16:47 | Stage 3.2b: `highback-seating` migrated back to `template_suffix=base` as verification case | `data/reports/stage-3.2b-subcollection-t4.md` |

---

## Hypotheses Evaluated

### Hypothesis A: P3-rollout changes were reverted by dev theme rebuild
**Against:** The P3-rollout sets `template_suffix` via the Admin API directly on collection records — it has nothing to do with theme files. A dev theme rebuild cannot revert API-side collection settings.  
**Status: REJECTED**

### Hypothesis B: Legacy populated collections never got template_suffix=base (P3-rollout failed silently)
**Partial match:** The legacy collections currently lack `template_suffix=base`. But this is not because P3 failed — P3 succeeded (62/62 HTTP 200). The current empty-suffix state is because the changes were **subsequently reverted deliberately**.  
**Status: PARTIALLY CORRECT — correct that legacy collections don't have base, but cause is a documented revert, not a silent failure**

### Hypothesis C: Stage 1.6's new shells overlap with legacy collections by handle (Shopify duplicate behavior)
**Against:** Only one handle overlap found: `desk-accessories`. But `desk-accessories` was in P3-rollout scope with `id=None` (didn't exist at rollout time). Stage 1.6 created it fresh. There is no evidence of Shopify "duplicate handle" behavior producing the empty state.  
**Status: REJECTED** (one partial overlap, but not the cause)

### Hypothesis D: Something else
**CONFIRMED:** The correct framing is: P3-rollout ran, then was explicitly reverted. The two operations cancel each other. The current state is a clean slate: 62 legacy collections back to empty template_suffix, 36 Stage 1.6 shells with `template_suffix=base` but 0 products, and 1 migrated collection (`highback-seating`) serving as the proven template.

---

## Current State Summary (as of 2026-05-07)

| Category | Count | Description |
|---|---|---|
| Total collections in Shopify | 359 | 35 smart + 324 custom |
| Collections with `template_suffix=base` | 37 | 36 empty Stage 1.6 shells + 1 migrated (highback-seating) |
| Collections with legacy suffix (parent hubs) | 9 | seating, desks, storage, etc. — smart collections |
| Collections with other suffixes | 10 | Remaining hub templates |
| Collections with no suffix (legacy sub-colls) | 312 | Includes 62 P3-reverted legacy sub-collections |

**Where the 653 products actually live:**
- In parent hub smart collections (overlapping): seating 194, tables 104, desks 98, etc.
- In legacy sub-collections with no template_suffix: 56 populated legacy sub-collections across all 9 hubs
- In `highback-seating` (template=base, migrated): 46 products

---

## Key Finding for Stage 3.2c

The migration path is clear: **flip 56 populated legacy sub-collections to `template_suffix=base`** (re-apply the P3-rollout, but this time without reverting). The 36 Stage 1.6 empty shells do NOT need products moved to them — instead, for most of them, a corresponding populated legacy collection already exists under a different handle that should be migrated. The Stage 1.6 shells may then be candidates for deletion or consolidation.

See `data/reports/stage-3.2a.5-migration-plan.md` for the full plan.
