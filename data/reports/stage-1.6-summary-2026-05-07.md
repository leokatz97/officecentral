# Stage 1.6 Summary — JSON Template Link Audit
**Date:** 2026-05-07  
**Branch:** `chore/json-template-link-audit-2026-05-07`

---

## Overview

Stage 1.5 crawled `<a href>` strings in `.liquid` files only. Stage 1.6 audited link values inside JSON template block configurations — the source of the category hub tile hrefs that produced the sub-collection 404s observed in the walkthrough.

---

## 1. Audit Scope

Templates crawled: all `theme/templates/*.json` (33 files)  
Templates containing URL-valued fields: 11 (10 collection hubs + `page.oecm.json`)  
**Total link values extracted: 109**

---

## 2. Pre-Fix Results

| Status | Count |
|--------|-------|
| 200 OK | 48 |
| 404 Not Found | **61** |
| Other | 0 |

---

## 3. Bucket Assignments

| Bucket | Description | Count |
|--------|-------------|-------|
| **A** | Stale link — correct collection exists under a different handle | **17** |
| **B** | Missing collection record — handle is correct per design system, record did not exist | **44 instances → 36 unique handles** |
| **C** | Ambiguous | **0** |

---

## 4. Bucket A Fixes — Template Href Redirects

All 17 edits applied in commit `69017e9`. No tile copy, titles, or images were touched.

| Template | Old href | New href (live handle) |
|----------|----------|------------------------|
| collection.accessories.json | /collections/office-lighting | /collections/lighting |
| collection.accessories.json | /collections/whiteboards | /collections/white-board |
| collection.boardroom.json | /collections/boardroom-tables | /collections/meeting-conference-room-tables |
| collection.desks.json | /collections/height-adjustable-desks | /collections/height-adjustable-tables-desks |
| collection.desks.json | /collections/reception-desks | /collections/reception-desks-desks |
| collection.desks.json | /collections/computer-desks | /collections/workstations-computer-desks |
| collection.ergonomic-products.json | /collections/sit-stand-converters | /collections/desktop-sit-stand |
| collection.quiet-spaces.json | /collections/phone-booths | /collections/telephone-booths |
| collection.quiet-spaces.json | /collections/high-back-privacy-seating | /collections/highback-seating |
| collection.quiet-spaces.json | /collections/soundproofing | /collections/sound-dampeners |
| collection.seating.json | /collections/task-seating | /collections/task-chairs |
| collection.seating.json | /collections/training-stacking-seating | /collections/stacking-seating |
| collection.seating.json | /collections/seating-accessories | /collections/chair-accessories |
| collection.storage.json | /collections/lateral-filing-cabinets | /collections/lateral-file-cabinets-storage |
| collection.storage.json | /collections/vertical-filing-cabinets | /collections/vertical-file-cabinets-storage |
| collection.tables.json | /collections/conference-tables | /collections/meeting-conference-room-tables |
| collection.tables.json | /collections/training-tables | /collections/training-room-tables |

---

## 5. Bucket B — Collections Created

**36 collections created** via Shopify Admin API (all published, `template_suffix=base`, no products).  
Full record: [`data/reports/sub-collections-created-stage-1.6.csv`](sub-collections-created-stage-1.6.csv)

### Brand collections (4)
`keilhauer`, `global-teknion`, `ergocentric`, `global-furniture`

### Seating sub-collections (6)
`executive-seating`, `conference-seating`, `bench-seating`, `healthcare-seating`, `active-seating`, `beam-seating`

### Desks sub-collections (4)
`modular-workstations`, `executive-desks`, `training-desks`, `desk-accessories`

### Storage sub-collections (6)
`mailboxes`, `media-storage`, `mobile-storage`, `wall-storage`, `personal-storage`, `high-density-storage`

### Accessories sub-collections (2)
`desktop-accessories`, `waste-recycling`

### Boardroom sub-collections (2)
`boardroom-seating`, `boardroom-storage`

### Ergonomic sub-collections (1)
`ergonomic-accessories`

### Panels sub-collections (2)
`acoustic-panels`, `privacy-screens`

### Quiet Spaces sub-collections (2)
`acoustic-pods`, `focus-rooms`

### Tables sub-collections (7)
`cafe-tables`, `multipurpose-tables`, `standing-tables`, `side-tables`, `outdoor-tables`, `nesting-tables`, `collaborative-tables`

> **Note:** All Bucket B collections ship empty. Product population is a separate Stage 4 workstream. The `global-furniture` (Global Furniture Group brand) and `global-teknion` brand collections currently exist separately — the seating hub tile uses `global-furniture` while the desks/panels/business-furniture hubs use `global-teknion`. These are intentionally distinct brand collections; handle-level consolidation is a future content decision.

---

## 6. Bucket C Halts

**None.** Every 404 had a clear Bucket A or B resolution.

---

## 7. Post-Fix Audit Results

Re-audit run after all fixes applied.  
Full report: [`data/reports/json-template-links-post-stage-1.6.csv`](json-template-links-post-stage-1.6.csv)

| Status | Count |
|--------|-------|
| 200 OK | **109** |
| 404 | **0** |

✅ **Zero 404s across all 109 JSON template link values.**

---

## 8. Click-Through Verification

5 random tile links sampled from each of the 5 primary hub templates (boardroom has only 4 tiles → 24 total). All sampled against live Shopify API.  
Full report: [`data/reports/hub-clickthrough-post-stage-1.6.csv`](hub-clickthrough-post-stage-1.6.csv)

| Hub | Links Checked | Pass |
|-----|---------------|------|
| collection.seating.json | 5 | 5 ✅ |
| collection.desks.json | 5 | 5 ✅ |
| collection.storage.json | 5 | 5 ✅ |
| collection.tables.json | 5 | 5 ✅ |
| collection.boardroom.json | 4 | 4 ✅ |
| **Total** | **24** | **24 ✅** |

---

## 9. Commits

| SHA | Message |
|-----|---------|
| `69017e9` | fix: redirect stale tile hrefs in 8 hub templates to live handles (Stage 1.6.A) |
| `44fd3c3` | feat: create missing sub-collection records to resolve hub-tile 404s (Stage 1.6.B) |

---

**Halted. Awaiting explicit approval before proceeding to Stage 2.**
