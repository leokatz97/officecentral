# Stage 5 Launch Audit — 4.9 Image Integrity
**Date:** 2026-05-08
**Sources:** `data/reports/stage-4b-recover-diff.md`, `data/reports/stage-4b-recover-execute-summary.md`
**Auditor:** Claude Code (read-only pass)

---

## Context

This is a planning/scope document. No live API calls were made during this audit. The three products below are confirmed based on the Stage 4b-RECOVER audit trail and execution summary.

---

## Known-broken products (from Stage 4b diff)

These 4 products had `published_at` set to null (unpublished without explanation) relative to the April 21 baseline. They were flagged in `stage-4b-recover-diff.md` as the `UNPUBLISHED` category.

| Handle | Status | Resolution |
|---|---|---|
| `willow-bariatric-chair` | Re-published ✓ | Stage 4b-RECOVER-EXECUTE (commit `c64936c`, 2026-05-08) |
| `solid-steel-shelving-starter-set` | Re-published ✓ | Stage 4b-RECOVER-EXECUTE (commit `c64936c`, 2026-05-08) |
| `monitor-arms` | Re-published ✓ | Stage 4b-RECOVER-EXECUTE (commit `c64936c`, 2026-05-08) |
| `foundations-sport-splash-quad-strollers` | Left unpublished per directive | Had 1 order — intentional keep-alive; Steve confirmed untouched |

---

## What the image integrity audit must check

For the 3 re-published products, visual inspection is required to confirm:

1. **Primary image is present and correct** — `willow-bariatric-chair` and `solid-steel-shelving-starter-set` and `monitor-arms` should each have at least one product image. During the unpublish period, images are typically retained by Shopify, but this should be verified.

2. **Image position** — Per `scripts/reorder-product-images.py` (Phase 1b image pipeline), full-product hero images should be at position 1. Confirm these 3 products have the correct image order.

3. **Collection membership** — Confirm each re-published product still appears in its expected smart collection. Check:
   - `willow-bariatric-chair` → `seating` collection
   - `solid-steel-shelving-starter-set` → `storage` collection
   - `monitor-arms` → `ergonomic-products` collection

4. **Stage 4b audit note** — The execute summary flagged these as "image integrity issue carried as audit item" (commit message `c64936c`). Steve's sign-off was obtained for the re-publish. A visual QA check on the PDP of each product (once `ds-pdp-base.liquid` is built in Stage 4b) is the definitive verification.

---

## What this audit does NOT check

- The 27 archived products (Category A of Stage 4b-RECOVER) — these are intentionally archived per `data/policy/archived-products-do-not-restore.txt`
- The `foundations-sport-splash-quad-strollers` (kept unpublished per directive)
- The 7 new products added since the April 21 baseline — these are expected additions and don't represent regression

---

## AI-generated product image coverage

Per `bbi-build-state.md` row `IMG-PHASE2`:
- Image regeneration (≥80% coverage soft gate) is ⬜ not started
- `data/reports/hero-audit-2026-04-28.csv` contains the Phase 2 hero audit
- Approximately 216 "clean products" (Session 03 of the AI image pipeline) not yet processed

**IMG-PHASE2 is a soft gate** — waiver CSV approach is acceptable for launch if coverage is below 80%.

---

## Action items

| Action | Owner | Timing |
|---|---|---|
| Visual QA on 3 re-published PDPs (images present + correct position) | Leo / Claude | During Stage 4b PDP smoke test |
| Confirm collection membership of 3 re-published products | Scripted API check | Before launch |
| Run IMG-PHASE2 image coverage audit | Claude Code | Wave E |
| Generate waiver CSV for < 80% coverage | Claude Code | Wave E (if needed) |
