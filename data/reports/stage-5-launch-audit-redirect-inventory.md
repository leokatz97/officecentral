# Stage 5 Launch Audit — 4.14 Redirect Inventory
**Date:** 2026-05-08
**Sources:** `data/redirects/url-redirects.csv`, `data/redirects/sector-collections-redirects-2026-04-28.csv`, `data/redirects/sector-products-redirects-2026-04-28.csv`
**Auditor:** Claude Code (read-only pass)

---

## Redirect files inventory

### `data/redirects/url-redirects.csv`
**Purpose:** Product URL normalization (™/® symbols stripped from handles in PE-3)
**Status:** Pending Shopify Admin manual upload
**Row count:** 8 redirects

| From | To | Target built? |
|---|---|---|
| `/products/bungee™-tables-rectangular-flip-top-table-spider-legs-wheels` | `/products/bungee-tables-rectangular-flip-top-table-spider-legs-wheels` | ✓ (handle normalized) |
| `/products/concorde®-high-back-24hr-executive-synchro-tilter-2424` | `/products/concorde-high-back-24hr-executive-synchro-tilter-2424` | ✓ |
| `/products/concorde®-high-back-24hr-executive-synchro-tilter-deep-seat-2424-18` | `/products/concorde-high-back-24hr-executive-synchro-tilter-deep-seat-2424-18` | ✓ |
| `/products/global-accord™-mesh-back-tilter` | `/products/global-accord-mesh-back-tilter` | ✓ |
| `/products/offices-to-go®-newland™-l-shaped-suite-nlp420` | `/products/offices-to-go-newland-l-shaped-suite-nlp420` | ✓ |
| `/products/offices-to-go®-newland™-u-shaped-suites-nlp406` | `/products/offices-to-go-newland-u-shaped-suites-nlp406` | ✓ |
| `/products/sonic™-armchair-polypropylene-seat-back-6513` | `/products/sonic-armchair-polypropylene-seat-back-6513` | ✓ |
| `/products/sonic™-armchair-upholstered-seat-polypropylene-back-casters-6574` | `/products/sonic-armchair-upholstered-seat-polypropylene-back-casters-6574` | ✓ |
| `/products/sonic™-armless-counter-stool-polypropylene-seat-back-6558cs` | `/products/sonic-armless-counter-stool-polypropylene-seat-back-6558cs` | ✓ |

**Upload status:** PENDING (manual Admin upload required). These protect users who bookmarked or linked to URLs with ™/® symbols in them — most browsers encode these as %E2%84%A2 which Shopify treats as a different handle.

---

### `data/redirects/sector-collections-redirects-2026-04-28.csv`
**Purpose:** Redirect removed vertical collections (Educational, Healthcare, Daycare) to Business Furniture vertical
**Status:** PARKED — comment in file says "do not import until Phase 2 (P2-1) builds /collections/business-furniture"
**Row count:** 14 redirects (after stripping comment lines)

| From (example) | To | Target built? |
|---|---|---|
| `/collections/educational` | `/collections/business-furniture` | ✓ P2-1 done |
| `/collections/educational-furniture` | `/collections/business-furniture` | ✓ |
| `/collections/healthcare` (vertical) | `/collections/business-furniture` | ✓ |
| `/collections/classroom-storage` | `/collections/business-furniture` | ✓ |
| `/collections/desk-tables-sit-stand-classroom` | `/collections/business-furniture` | ✓ |
| `/collections/student-chairs` | `/collections/business-furniture` | ✓ |
| `/collections/student-desks` | `/collections/business-furniture` | ✓ |
| `/collections/student-tables` | `/collections/business-furniture` | ✓ |
| `/collections/student-tables-educational-furniture` | `/collections/business-furniture` | ✓ |
| `/collections/cribs` | `/collections/business-furniture` | ✓ |
| `/collections/infant-toddler` | `/collections/business-furniture` | ✓ |
| `/collections/toddler-lockers` | `/collections/business-furniture` | ✓ |
| `/collections/preschool-couches-chairs` | `/collections/business-furniture` | ✓ |
| `/collections/exam-room-seating` | `/collections/business-furniture` | ✓ |
| `/collections/clinician-screens` | `/collections/business-furniture` | ✓ |

**Status:** `/collections/business-furniture` is now built (P2-1, commit `3e9ffe3`). The PARKED condition is met. **This file is now ready to upload** — strip the comment lines before import.

---

### `data/redirects/sector-products-redirects-2026-04-28.csv`
**Purpose:** Redirect specific archived products to relevant collections
**Status:** Ready to upload
**Row count:** 2 redirects

| From | To | Target built? |
|---|---|---|
| `/products/willow-bariatric-chair` | `/collections/bariatric-seating` | ⚠️ `willow-bariatric-chair` was RE-PUBLISHED in Stage 4b-RECOVER (commit `c64936c`). This redirect would incorrectly redirect a now-live product. **REVIEW BEFORE UPLOADING.** |
| `/products/foundations-sport-splash-quad-strollers` | `/collections/business-furniture` | ✓ (product kept unpublished per directive; redirect makes sense) |

**Warning:** The `willow-bariatric-chair` redirect conflicts with the Stage 4b re-publish decision. If the product is live, the redirect should not be applied. Remove this row before uploading if the product stays published.

---

## Summary

| File | Rows | Status | Action needed |
|---|---|---|---|
| `url-redirects.csv` | 9 | Ready | Upload to Shopify Admin → Navigation → URL Redirects |
| `sector-collections-redirects-2026-04-28.csv` | 15 (with comments) | Ready after stripping comments | Strip comment lines, then upload |
| `sector-products-redirects-2026-04-28.csv` | 2 | ⚠️ Review first | Remove `willow-bariatric-chair` row if product stays published; then upload |

---

## Additional redirect debt (not in CSV files)

These redirects are not yet in any CSV file but should be created:

| Scenario | From | To | Priority |
|---|---|---|---|
| `/pages/shop` → `/collections/business-furniture` | `/pages/shop` (removed per scope change 2026-04-25) | `/collections/business-furniture` | FIX |
| Brand-dealer page (de-gated) | `/pages/brand-dealer` (if it existed) | `/pages/brands` | NIT |
| Any sub-collection handles renamed during Stage 3.2c migration | (see `data/reports/stage-3.2c.6-canonical-handles.csv`) | New canonical handles | FIX |

The Stage 3.2c canonical handle migration (`d3eb79c`) flipped sub-collection handles from old names to new. A redirect audit against the new handle list should be done before launch to catch any bookmarked or indexed URLs pointing to old handles.

---

## Recommendation

Upload all three redirect files (with the corrections noted above) before or during Phase 5 (launch). The sector-collection redirects are particularly important — archived vertical collection URLs may still exist in search engine indexes and need to 301 to the Business Furniture vertical.
