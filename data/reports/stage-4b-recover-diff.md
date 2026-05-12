# Stage 4b Recovery — Product Diff Report
_Generated: 2026-05-08 | Baseline: data/exports/products-export-2026-04-21.csv | Live: Shopify Admin API_

## Summary
| Category | Count |
|---|---|
| DELETED | 0 |
| STATUS_REGRESSION (active → archived) | 27 |
| UNPUBLISHED (published_at lost) | 4 |
| DETAGGED (type:/vendor: tags lost) | 0 |
| COLLECTION_DROPPED (count > 5 decrease) | 0 |
| New products added since baseline | 7 |

## STATUS_REGRESSION — 27 products archived

All archived via commit `3dfc495` on 2026-04-28 (PB-1/PB-2 sector cleanup).

| Handle | Title | Vendor | Type |
|---|---|---|---|
| aktivity-environ-table | Aktivity Environ table | Business Interiors | — |
| aktivity-puddle | Aktivity Puddle | Business Interiors | — |
| aktivity-rectangle-height-adjustable-table | Aktivity Rectangle Height Adjustable Table | Business Interiors | — |
| auditorium-lecture-hall-seating | Auditorium / Lecture Hall Seating | Business Interiors | — |
| auditorium-lecture-hall-seating-my-space | Auditorium / Lecture Hall Seating My Space | Business Interiors | — |
| auditorium-lecture-hall-seating-omni | Auditorium / Lecture Hall Seating Omni | Business Interiors | — |
| auditorium-lecture-hall-seating-primo | Auditorium / Lecture Hall Seating Primo | Business Interiors | — |
| duet-tablet-chair | Duet Tablet Chair | Business Interiors | — |
| educational-student-tables-5-shapes-sizes | Educational Student Tables (5 Shapes & Sizes) | Office Central & Brant Business Interiors | — |
| foundations-next-gen-serenity-compact-crib | Foundations Next Gen Serenity Compact Crib | Business Interiors | — |
| foundations-next-gen-serenity-safereach-compact-crib | Foundations Next Gen Serenity SafeReach Compact Crib | Business Interiors | — |
| foundations-safetycraft-compact-crib-natural-steel | Foundations SafetyCraft Compact Crib - Natural - Steel | Business Interiors | — |
| foundations-sport-splash-3-seat-strollers | Foundations Sport Splash 3-Seat Strollers | Business Interiors | — |
| gc-comet-bariatric-stacking-armchair-gc2180-1 | GC Comet™ Bariatric Stacking Armchair (GC2180) | Business Interiors | — |
| global-recliner-primacare-gc3608mrc | Global Recliner Primacare GC3608MRC | Business Interiors | — |
| nesting-training-table-8-colour-choices | Nesting Training Table (8 Colour Choices) | Business Interiors | — |
| nourish-high-back-bariatric-patient-chair-gc3685-1 | Nourish™ High Back Bariatric Patient Chair (GC3685) | Business Interiors | — |
| primacare-ht-patient-mid-back-bariatric-open-arms-gc3638-1 | Primacare™ HT Patient Mid Back Bariatric, Open Arms (GC3638) | Business Interiors | — |
| recliners-by-ryno | Recliners by Ryno | Business Interiors | — |
| sidero-tablet-arm | Sidero Tablet Arm | Business Interiors | — |
| sidero-tablet-chair | Sidero Tablet Chair | Business Interiors | — |
| student-chairs-3-sizes | Student Chairs (3 sizes) | Office Central & Brant Business Interiors | — |
| student-desk | Student Desk | Business Interiors | — |
| student-desk-1 | Student Desk | Business Interiors | — |
| student-desk-carol-single-double-sided | Student Desk Carol Single & Double Sided | Business Interiors | — |
| the-foster-recliner | The Foster Recliner | Business Interiors | Recliners |
| uni-flip-training-tables-7-sizes | Flip Top Training Tables 7 Sizes | Business Interiors | — |

## UNPUBLISHED — 4 products (published_at → null)

| Handle | Current Status | In Sector CSV | Notes |
|---|---|---|---|
| foundations-sport-splash-quad-strollers | active | Yes (UNPUBLISH disposition) | Had 1 order — intentional keep-alive |
| willow-bariatric-chair | active | Yes (UNPUBLISH disposition) | Had 1 order — intentional keep-alive |
| solid-steel-shelving-starter-set | active | **No — unexplained** | Unexplained; no audit trail in logs |
| monitor-arms | active | **No — unexplained** | Unexplained; no audit trail in logs |

## COLLECTION DROPS

No collection count drops were detected in the baseline comparison. Two collections are empty:
- `executive-desks` (0 products) — newly created custom collection, never populated
- `workstations-computer-desks` (0 products) — newly created custom collection, never populated

## Named Products — Status Check

| Handle | Status | Published | Notes |
|---|---|---|---|
| alphabetter-stand-up-desk | active | ✓ | Healthy |
| ashton-high-back-tilter | active | ✓ | Healthy |
| premium-series-lateral-file-cabinet-2-3-4-5-drawer-1 | active | ✓ | Healthy |