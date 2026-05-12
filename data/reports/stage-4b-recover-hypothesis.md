# Stage 4b Recovery — Root Cause Hypothesis & Recovery Proposal
_Generated: 2026-05-08_

---

## Root Cause Rankings

### #1 — Intentional PB-1/PB-2 Sector Cleanup (Confidence: 99%)

**Commit:** `3dfc495` on **2026-04-28**  
**Script:** `scripts/archive-non-biz-products.py --live`  
**Input CSV:** `data/reports/sector-products-disposition-2026-04-28.csv`

This commit deliberately:
- Archived **27 products** (educational, healthcare, institutional SKUs with zero sales history)
- Unpublished **2 products** with sold-history (strollers, bariatric chair — kept active for order history)
- Unpublished **15 sector collections** (/educational, /healthcare, /student-*, etc.)
- Imported 301 redirects so prior buyers don't 404

**The 27 archived products are exactly the 27 listed in the disposition CSV.** This was not a bug — it was a planned scoping decision to make BBI a business-furniture-only store.

The archived products include:
- Student desks × 3 (student-desk, student-desk-1, student-desk-carol-single-double-sided)
- Training tables × 2 (nesting-training-table, uni-flip-training-tables-7-sizes)
- Auditorium seating × 4
- Bariatric patient chairs × 3
- Recliners × 3
- Cribs × 3 + strollers × 1
- Tablet/arm chairs × 3
- Educational tables (Aktivity × 3 + educational-student-tables)

### #2 — Two Products Unpublished Without Audit Trail (Confidence: 70%)

`solid-steel-shelving-starter-set` and `monitor-arms` are active but `published_at=null`. Not in the sector cleanup CSV. No script in `data/logs/` explains this.  
**Most likely cause:** Steve manually unpublished them via Shopify Admin, or an app (AvisPlus, Avada) triggered an automatic action.

### #3 — Empty "Executive-Desks" and "Workstations-Computer-Desks" Collections (Confidence: 95%)

These are newly created custom collections (not in the May 6 backup) that were added empty as navigation placeholders and never populated. This is a **missing curation step**, not a regression.

---

## Steve's Report: "All desks are gone from product pages"

**Main desk hub is healthy:**
- `/collections/desks` (smart): **98 products** ✓
- `/collections/l-shape-desks`: **31 products** ✓
- `/collections/height-adjustable-tables-desks`: **21 products** ✓
- `/collections/straight-desks-desks`: **17 products** ✓
- `/collections/u-shape-desks-desks`: **16 products** ✓
- `/collections/office-suites-desks`: **13 products** ✓
- `/collections/reception-desks-desks`: **9 products** ✓

**Likely what Steve saw:**
1. `/collections/executive-desks` or `/collections/workstations-computer-desks` → **0 products** (never populated)
2. `/collections/student-desks` → **5 products** (lost 3 student desk SKUs to sector cleanup)
3. A navigation link pointing to a now-unpublished sector collection (these show 404 or redirect to /business-furniture)

---

## Proposed Recovery Actions

### A — Do nothing (recommended for the 27 archived products)
The sector cleanup was deliberate and approved in the build plan. These are non-business-furniture products. Restoring them would undo the intentional scope narrowing. **Steve needs to confirm this was intentional before touching.**

### B — Restore specific archived products (if Steve approves)
If Steve wants specific products back:
```
PUT /admin/api/2024-01/products/{id}.json
{ "product": { "id": {id}, "status": "active", "published": true } }
```
Estimated time: ~5 min script, ~1 min API per product batch.  
Risk: LOW (status flip is reversible).

### C — Re-publish 2 unpublished products (if Steve approves)
`solid-steel-shelving-starter-set` and `monitor-arms` — both active, just need `published_at` restored.
```
PUT /admin/api/2024-01/products/{id}.json
{ "product": { "id": {id}, "published": true } }
```
Risk: LOW.

### D — Populate `executive-desks` and `workstations-computer-desks` (if wanted)
These empty collections need products manually added or a smart-collection rule.  
Suggested: convert to smart collections with rules:
- `executive-desks`: `tag equals type:desks AND tag equals type:executive` (or title contains "executive")
- `workstations-computer-desks`: `tag equals type:workstations`
Risk: LOW — no data loss, just curation.

---

## Products Needing Manual Review

| Handle | Category | Sales History | Recommended Action |
|---|---|---|---|
| willow-bariatric-chair | Bariatric (healthcare) | 1 order, $2,100 | Keep unpublished; has redirect |
| foundations-sport-splash-quad-strollers | Strollers (daycare) | 1 order, $798 | Keep unpublished; has redirect |
| solid-steel-shelving-starter-set | Storage (business) | Unknown | Re-publish? Needs Steve input |
| monitor-arms | Accessories (business) | Unknown | Re-publish? Needs Steve input |
| student-desk × 3 | Educational | 0 | Keep archived per PB-1 scope |
| auditorium seating × 4 | Institutional | 0 | Keep archived per PB-1 scope |

---

## Recovery Estimate

| Action | Products Affected | Time | Risk |
|---|---|---|---|
| Restore all 27 archived | 27 | 20 min (script) | Low |
| Restore specific subset | TBD | 10 min (script) | Low |
| Re-publish 2 unpublished | 2 | 5 min (script) | Low |
| Populate executive-desks | ~10–15 products | 30 min (curation) | Low |
| Populate workstations-computer-desks | ~5–10 products | 20 min (curation) | Low |

---

**HALT — awaiting Steve's approval before executing any recovery action.**
