# BBI Image Slot Inventory — 2026-05-25

Repo state at generation: `main` @ `e113239` (HIGH-3 merge). Read-only inventory. No theme writes. Drives Step 2 interactive image picker (Leo assigns one Upwork file per slot).

**URL conventions used throughout:**
- LIVE: `https://www.brantbusinessinteriors.com/...`
- DEV preview: `https://office-central-online.myshopify.com/...?preview_theme_id=186373570873`

**LIVE today still renders Avada theme** until LAUNCH-2 flip — the BBI placeholders/refs described below render on the DEV preview only. After LAUNCH-2 they render LIVE.

**Upwork delivery root:** `~/Desktop/bbi-upwork-delivery/` (8 folders).

---

## Executive Summary

| Bucket | Count |
|---|---:|
| **Total slots needing fill** | **137** |
| **CRITICAL** | 13 |
| **HIGH** | 15 |
| **MED** | 95 |
| **LOW** | 14 |

### By Upwork folder (suggested mapping)

| Upwork folder | Approx. slots |
|---|---:|
| `Homepage-Hero/` | 1 |
| `Homepage tiles/` | 9 |
| `Top product tiles/` | 3 |
| `Sub Category/` | 44 |
| `Categorybanners/` | 9 |
| `Category service tiles/` | 5 |
| `Case study cards/` | 20 |
| `Brandbanners/` | 7 |
| _Other (industry/OECM/about/quote/internal)_ | 39 |

### Estimated Phase 2 (interactive picker) time @ ~2 min/slot

- **CRITICAL only:** 13 × 2 = **~26 min**
- **CRITICAL + HIGH:** 28 × 2 = **~56 min**
- **All (CRITICAL + HIGH + MED + LOW):** 137 × 2 = **~4.5 hours**

**Recommendation:** complete CRITICAL + HIGH before LAUNCH-2 Monday (~1 hour of picker time). Defer MED + LOW to Tue/Wed post-launch — they're tiles + secondary supporting images that don't gate the launch headline.

---

## Slot Type Cheat-Sheet (placeholder mechanism per surface)

| Surface | Mechanism | Replacement path |
|---|---|---|
| Homepage (custom_liquid in `index.json`) | CSS-class placeholder `<div class="bbi-hp-ph bbi-hp-ph--{name}">` with gradient/solid fills in `assets/bbi-homepage.css:589-614` | Either swap class block for `<img>` inside the custom_liquid, or set `background-image` in CSS to a `shopify://shop_images/...` URL after upload |
| Category pages (`ds-cc-base.liquid`) | `image_picker` schema settings (`hero_image`, tile block `image`) — currently `shopify://shop_images/*.jpg` legacy Avada refs (stock-y, generic OCI/Inspiration photos) | Re-pick via theme editor or template JSON edit pointing at fresh Shopify Files URL |
| Industry/Brand/Service/OECM/About/Quote/Our-Work/Customer-Stories pages (`ds-lp-*.liquid`) | `image_picker` schema settings on the section — same mechanism as categories | Same as above |
| Cornerstone Post 1 (article body via `ds-article.liquid`) | Article featured image (currently `null` per Day 10 record) + inline `<img>` opportunities in `body_html` | Set `article.image` via Shopify Admin API + edit `body_html` inline `<img>` tags |

**Spec note:** the design-system standard for hero images on `ds-cc-base.liquid` and `ds-lp-*` sections is **5:4 ratio** (confirmed in `ds-cc-base.liquid:1049` and `ds-lp-brands-*.liquid` schema `info` strings). Tile images on `ds-cc-base.liquid` are **4:3 ratio** (`ds-cc-base.liquid:1179`). Liquid renders heroes at `width: 840` with widths `400,600,840` (~840px max served). Tiles at `width: 600` with widths `280,400,600`.

---

## CRITICAL Priority Slots (13)

### SLOT 1 — Homepage hero
- **Page:** Homepage · LIVE: `https://www.brantbusinessinteriors.com/` · DEV: `https://office-central-online.myshopify.com/?preview_theme_id=186373570873`
- **Section:** `templates/index.json` → `bbi-hero` custom_liquid → `<div class="bbi-hp-ph bbi-hp-ph--hero">`
- **Current state:** DS placeholder — black/red gradient (`assets/bbi-homepage.css:597`)
- **Spec:** ~5:4 to ~3:2 — fills hero media slot; alt text "Executive office installation by Brant Business Interiors, Peterborough Ontario"
- **Folder:** `Homepage-Hero/`
- **Notes:** The single most visible image on the entire site. Custom_liquid → either swap the `<div>` for an `<img>` or set `background-image` in CSS.

### SLOT 2 — Featured product card 1 (Heartwood)
- **Page:** Homepage · same URLs as SLOT 1
- **Section:** `templates/index.json` → `bbi-featured` → `bbi-hp-ph--featured-1` block
- **Current state:** DS placeholder — light gray (`#E9EBEF`)
- **Spec:** 4:3 product card; current copy says "ergoCentric tCentric Hybrid Task Chair" but **per Idea #15 closed 2026-05-25 this slot belongs to Heartwood L-Shape Height Adjustable Desk Set** (`/products/l-shape-height-adjustable-desk-set`) — copy + alt text + link will also be retargeted at the IMAGE SWAP session.
- **Folder:** `Top product tiles/`
- **Notes:** One of the 3 "Featured this quarter" cards (per Idea #15). High visibility.

### SLOT 3 — Featured product card 2 (OTG)
- **Page:** Homepage
- **Section:** `templates/index.json` → `bbi-featured` → `bbi-hp-ph--featured-2`
- **Current state:** DS placeholder — light gray (`#F3F4F6`)
- **Spec:** 4:3 product card; current copy "Keilhauer Wish Side Chair" but **per Idea #15 belongs to OTG Raven High-Back Heavy-Duty Synchro-Tilter** (`/products/raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b`)
- **Folder:** `Top product tiles/`
- **Notes:** Same retarget pattern as SLOT 2.

### SLOT 4 — Featured product card 3 (GFG)
- **Page:** Homepage
- **Section:** `templates/index.json` → `bbi-featured` → `bbi-hp-ph--featured-3`
- **Current state:** DS placeholder — gray (`#DEE1E6`)
- **Spec:** 4:3 product card; current copy "Global Furniture Group Furtif Executive Desk" but **per Idea #15 belongs to GFG Accord Mesh-Back Tilter** (`/products/global-accord-mesh-back-tilter`)
- **Folder:** `Top product tiles/`
- **Notes:** Same retarget pattern.

### SLOT 5 — Business Furniture (parent collection) hero
- **Page:** `/collections/business-furniture` · LIVE: `https://www.brantbusinessinteriors.com/collections/business-furniture` · DEV: append `?preview_theme_id=186373570873`
- **Section:** `templates/collection.business-furniture.json` → `ds-cc-base` → `hero_image`
- **Current state:** Stock-y generic Avada legacy — `shopify://shop_images/business-furniture-space.jpg`
- **Spec:** 5:4 hero (840px wide served)
- **Folder:** `Categorybanners/`
- **Notes:** Catalog landing — top of the funnel for every category buyer.

### SLOT 6 — Seating category hero
- **Page:** `/collections/seating` · LIVE + DEV
- **Section:** `templates/collection.seating.json` → `ds-cc-base` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/seating-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`
- **Notes:** Largest sub-collection by product count; OECM-anchor category.

### SLOT 7 — Desks category hero
- **Page:** `/collections/desks`
- **Section:** `templates/collection.desks.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/desks-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 8 — Storage category hero
- **Page:** `/collections/storage`
- **Section:** `templates/collection.storage.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/storage-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 9 — Tables category hero
- **Page:** `/collections/tables`
- **Section:** `templates/collection.tables.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/tables-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 10 — Boardroom category hero
- **Page:** `/collections/boardroom`
- **Section:** `templates/collection.boardroom.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/boardroom-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 11 — Ergonomic Products category hero
- **Page:** `/collections/ergonomic-products`
- **Section:** `templates/collection.ergonomic-products.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/ergonomic-products-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 12 — Panels & Room Dividers category hero
- **Page:** `/collections/panels-room-dividers`
- **Section:** `templates/collection.panels-room-dividers.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/panels-room-dividers-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

### SLOT 13 — Accessories category hero
- **Page:** `/collections/accessories`
- **Section:** `templates/collection.accessories.json` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/accessories-space.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Categorybanners/`

---

## HIGH Priority Slots (15)

### SLOT 14 — Healthcare industry hero
- **Page:** `/pages/healthcare` · LIVE: `https://www.brantbusinessinteriors.com/pages/healthcare` · DEV: append `?preview_theme_id=186373570873`
- **Section:** `page.healthcare.json` → `ds-lp-healthcare` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/OCI-Healthcare-Carousel-3.jpg`
- **Spec:** 5:4 hero
- **Folder:** `Category service tiles/` _(or `Categorybanners/` — Leo decide; the Upwork folder labelled "Category service tiles" likely maps best)_

### SLOT 15 — Education industry hero
- **Page:** `/pages/education`
- **Section:** `page.education.json` → `ds-lp-education` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/OCI-Education-1.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`
- **Notes:** Education is the OECM anchor sector — primary cornerstone-post-1 audience.

### SLOT 16 — Government industry hero
- **Page:** `/pages/government`
- **Section:** `page.government.json` → `ds-lp-government` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/OCI-Government-Federal-Furniture-Gallery-Image-1.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`

### SLOT 17 — Professional Services industry hero
- **Page:** `/pages/professional-services`
- **Section:** `page.professional-services.json` → `ds-lp-professional-services` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/professional-services-space.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`
- **Notes:** _Prompt referenced a "financial" page — no such page exists in repo; the closest match is professional-services._

### SLOT 18 — Non-Profit industry hero
- **Page:** `/pages/non-profit`
- **Section:** `page.non-profit.json` → `ds-lp-non-profit` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/non-profit-space.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`

### SLOT 19 — Industries hub hero
- **Page:** `/pages/industries`
- **Section:** `page.industries.json` → `ds-lp-industries` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/industries-hub-space_a7491d71-...jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`
- **Notes:** Hub page above the 5 sector landing pages.

### SLOT 20 — OECM page hero
- **Page:** `/pages/oecm`
- **Section:** `page.oecm.json` → `ds-lp-oecm` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/industries-hub-space_a7491d71-...jpg` (same as industries hub — re-use, needs distinct image)
- **Spec:** 5:4
- **Folder:** `Categorybanners/` or `Category service tiles/` — Leo decide
- **Notes:** OECM is the single highest-converting page for institutional buyers. Idea #13 lists this as a critical-path image swap target.

### SLOT 21 — Brands hub hero
- **Page:** `/pages/brands`
- **Section:** `page.brands.json` → `ds-lp-brands` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/brands-hub-space.jpg`
- **Spec:** 5:4
- **Folder:** `Brandbanners/`

### SLOT 22 — Heartwood brand page hero
- **Page:** `/pages/brands-heartwood`
- **Section:** `page.brands-heartwood.json` → `ds-lp-brands-heartwood` → `hero_image`
- **Current state:** **Blank** (no value set in template; schema info string says "Upload heartwood-space.jpg")
- **Spec:** 5:4
- **Folder:** `Brandbanners/`
- **Notes:** Heartwood is one of the 3 hero brands per Idea #15.

### SLOT 23 — OTG brand page hero
- **Page:** `/pages/brands-otg`
- **Section:** `page.brands-otg.json` → `ds-lp-brands-otg` → `hero_image`
- **Current state:** **Blank** (no value set; schema info "Upload otg-space.jpg")
- **Spec:** 5:4
- **Folder:** `Brandbanners/`

### SLOT 24 — Global / Teknion (GFG) brand page hero
- **Page:** `/pages/brands-global-teknion`
- **Section:** `page.brands-global-teknion.json` → `ds-lp-brands-global-teknion` → `hero_image`
- **Current state:** Set — `shopify://shop_images/global-teknion-space.jpg` (stock-y placeholder — needs branded image)
- **Spec:** 5:4
- **Folder:** `Brandbanners/`

### SLOT 25 — Delivery service page hero
- **Page:** `/pages/delivery`
- **Section:** `page.delivery.json` → `ds-lp-delivery` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/delivery-space.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`

### SLOT 26 — Relocation service page hero
- **Page:** `/pages/relocation`
- **Section:** `page.relocation.json` → `ds-lp-relocation` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/OCI-Services-Relocation-management.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`

### SLOT 27 — Design Services page hero
- **Page:** `/pages/design-services`
- **Section:** `page.design-services.json` → `ds-lp-design-services` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/design-services-product.png`
- **Spec:** 5:4
- **Folder:** `Category service tiles/`

### SLOT 28 — Quote page hero
- **Page:** `/pages/quote`
- **Section:** `page.quote.json` → `ds-lp-quote` → `hero_image`
- **Current state:** Stock-y — `shopify://shop_images/OCI-Service-Excellence-1.jpg`
- **Spec:** 5:4
- **Folder:** `Category service tiles/` or `Categorybanners/`
- **Notes:** Quote is the primary conversion page across the entire site — first impression matters.

---

## MED Priority Slots (95)

> Grouped by surface to keep this section scannable. Each row is a slot Leo will assign in Phase 2.

### Homepage tiles — 12 slots (29 → 40)

**Section:** `templates/index.json` → all `custom_liquid` blocks with `bbi-hp-ph--*` CSS placeholders.

| # | Slot | Block | Current state | Folder |
|---|---|---|---|---|
| 29 | Shop tile — Seating | `bbi-shop` | DS placeholder (gray gradient `--bbi-gray-700`) | `Homepage tiles/` |
| 30 | Shop tile — Desks & Workstations | `bbi-shop` | DS placeholder (`--bbi-gray-800`) | `Homepage tiles/` |
| 31 | Shop tile — Storage & Filing | `bbi-shop` | DS placeholder (`--bbi-gray-600`) | `Homepage tiles/` |
| 32 | Shop tile — Tables & Boardroom | `bbi-shop` | DS placeholder (`--bbi-gray-500`) | `Homepage tiles/` |
| 33 | Industry tile — Healthcare | `bbi-industries` | DS placeholder (`--bbi-info` blue) | `Homepage tiles/` |
| 34 | Industry tile — Education | `bbi-industries` | DS placeholder (`gray-700`) | `Homepage tiles/` |
| 35 | Industry tile — Government | `bbi-industries` | DS placeholder (`gray-800`) | `Homepage tiles/` |
| 36 | Industry tile — Non-Profit | `bbi-industries` | DS placeholder (`--bbi-success` green) | `Homepage tiles/` |
| 37 | Industry tile — Professional Services | `bbi-industries` | DS placeholder (`gray-600`) | `Homepage tiles/` |
| 38 | Case study card — Halton Catholic DSB | `bbi-work` | Text-label placeholder (`bbi-ph__label`) | `Case study cards/` |
| 39 | Case study card — Trillium Health Partners | `bbi-work` | Text-label placeholder | `Case study cards/` |
| 40 | Case study card — City of Mississauga | `bbi-work` | Text-label placeholder | `Case study cards/` |

### Business-Furniture parent — 8 sub-category tiles (41 → 48)

**Section:** `templates/collection.business-furniture.json` → `ds-cc-base` tile blocks. Each tile uses `image_picker` field (4:3 ratio). Folder: `Sub Category/`.

| # | Tile title | Current state |
|---|---|---|
| 41 | Seating | `shopify://shop_images/seating-product.jpg` (stock-y) |
| 42 | Desks & Workstations | `shopify://shop_images/desks-product.jpg` (stock-y) |
| 43 | Storage & Filing | `shopify://shop_images/storage-product.jpg` (stock-y) |
| 44 | Tables | `shopify://shop_images/tables-product.jpg` (stock-y) |
| 45 | Boardroom | `shopify://shop_images/boardroom-product.jpg` (stock-y) |
| 46 | Ergonomic Products | `shopify://shop_images/ergonomic-products-product.jpg` (stock-y) |
| 47 | Panels & Dividers | `shopify://shop_images/panels-room-dividers-product.jpg` (stock-y) |
| 48 | Accessories | `shopify://shop_images/accessories-product.jpg` (stock-y) |

### Seating sub-tiles — 6 (49 → 54)

`templates/collection.seating.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 49 | Office Chairs | stock-y (`task-seating-product.jpg`) |
| 50 | Guest & Visitor Seating | stock-y (`OCI-Education-1.jpg` — reused, wrong subject) |
| 51 | Stacking & Training Chairs | stock-y (`Inspiration-Meeting-1.jpg`) |
| 52 | Stools & Counter Seating | possibly blank — verify in picker |
| 53 | Lounge & Soft Seating | stock-y (`Lounge-Carousel-Image6.jpg`) |
| 54 | Outdoor Seating | stock-y (`OCI-Hospitality-1.jpg` — wrong subject) |

### Desks sub-tiles — 6 (55 → 60)

`templates/collection.desks.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 55 | Sit-Stand & Height-Adjustable Desks | stock-y (`ergonomic-products-product.jpg` — wrong subject) |
| 56 | L-Shape Desks | stock-y (`desks-space.png`) |
| 57 | Single-Surface Desks | stock-y (`desks-product.jpg`) |
| 58 | Reception Desks | stock-y (`Inspiration-Reception.jpg`) |
| 59 | Multi-Person Workstations | stock-y (`OCI-Workplace-1.jpg`) |
| 60 | Executive Desk Suites | stock-y (`Inspiration-Executive-Office.jpg`) |

### Storage sub-tiles — 8 (61 → 68)

`templates/collection.storage.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 61 | Lateral Filing Cabinets | stock-y (`storage-product.jpg`) |
| 62 | Vertical Filing Cabinets | stock-y (`storage-space.png`) |
| 63 | Mobile Pedestals | stock-y (`storage-product.jpg`) |
| 64 | Storage Cabinets | stock-y (`storage-space.png`) |
| 65 | Bookcases & Shelving | stock-y (`OCI-Services-Shelving.jpg`) |
| 66 | Lockers | stock-y (`storage-product.jpg`) |
| 67 | Credenzas | stock-y (`boardroom-space.jpg`) |
| 68 | Wardrobe & Coat Storage | stock-y (`storage-space.png`) |

### Tables sub-tiles — 4 (69 → 72)

`templates/collection.tables.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 69 | Conference Tables | stock-y (`Inspiration-Conference-1-1.jpg`) |
| 70 | Training & Folding Tables | stock-y (`tables-product.jpg`) |
| 71 | Height-Adjustable Meeting Tables | stock-y (`ergonomic-products-space.jpg`) |
| 72 | Collaborative & Agile Tables | stock-y (`collaboration-product.jpg`) |

### Boardroom sub-tiles — 3 (73 → 75)

`templates/collection.boardroom.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 73 | Boardroom Tables | stock-y (`boardroom-product.jpg`) |
| 74 | Boardroom Credenzas | stock-y (`boardroom-space.jpg`) |
| 75 | Podiums & AV Furniture | stock-y (`Subject-Areas-boardroom.jpg`) |

### Ergonomic Products sub-tiles — 3 (76 → 78)

`templates/collection.ergonomic-products.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 76 | Desk Converters | stock-y (`ergonomic-products-product.jpg`) |
| 77 | Monitor Arms | stock-y (`ergonomic-products-space.jpg`) |
| 78 | Keyboard Trays | stock-y (`Inspiration-Ergonomics.jpg`) |

### Panels & Room Dividers sub-tiles — 1 (79)

`templates/collection.panels-room-dividers.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 79 | Room Dividers | stock-y (`panels-room-dividers-product.jpg`) |

### Accessories sub-tiles — 5 (80 → 84)

`templates/collection.accessories.json` · Folder: `Sub Category/` · Spec: 4:3.

| # | Tile title | Current state |
|---|---|---|
| 80 | Task Lighting | stock-y (`OCI-Services-Lighting-2.jpg`) |
| 81 | Whiteboards & Pinboards | stock-y (`OCI-Workplace-1.jpg`) |
| 82 | Chair Mats & Floor Protection | stock-y (`accessories-product.jpg`) |
| 83 | Monitor Arms & Desk Accessories | stock-y (`ergonomic-products-product.jpg`) |
| 84 | Acoustic Solutions | stock-y (`Inspiration-Accoustics.jpg`) |

### Industry page trust images — 14 (85 → 98)

Each `ds-lp-<industry>` section has 3 `trust_image_*` slots below the hero (sector lifestyle photos). Folder: `Case study cards/` (these are case-study-style sector lifestyle shots). Spec: square or 4:3.

| # | Slot | Page | Current state |
|---|---|---|---|
| 85 | Healthcare · trust_image_1 | `/pages/healthcare` | `OCI-Inspiration-Breakroom.jpg` |
| 86 | Healthcare · trust_image_2 | `/pages/healthcare` | `OCI-Healthcare-Furniture-Gallery-Image.jpg` |
| 87 | Healthcare · trust_image_3 | `/pages/healthcare` | `Inspiration-Reception.jpg` |
| 88 | Education · trust_image_1 | `/pages/education` | `OCI-Inspiration-Breakroom.jpg` |
| 89 | Education · trust_image_2 | `/pages/education` | `Inspiration-Meeting-1.jpg` |
| 90 | Government · trust_image_1 | `/pages/government` | `OCI-Service-Excellence-1.jpg` |
| 91 | Government · trust_image_2 | `/pages/government` | `Mattamy-1.jpg` |
| 92 | Government · trust_image_3 | `/pages/government` | `OCI-Workplace-1_8dc819f3...jpg` |
| 93 | Professional Services · trust_image_1 | `/pages/professional-services` | `Inspiration-Executive-Office.jpg` |
| 94 | Professional Services · trust_image_2 | `/pages/professional-services` | `Inspiration-Meeting-1.jpg` |
| 95 | Professional Services · trust_image_3 | `/pages/professional-services` | `OCI-Workplace-1_8dc819f3...jpg` |
| 96 | Non-Profit · trust_image_1 | `/pages/non-profit` | `OCI-Hospitality-1.jpg` |
| 97 | Non-Profit · trust_image_2 | `/pages/non-profit` | `Inspiration-Workplace.jpg` |
| 98 | Non-Profit · trust_image_3 | `/pages/non-profit` | `OCI-Inspiration-Breakroom.jpg` |

> **Education trust_image_3** schema slot exists but template has no value set → currently rendered blank/placeholder. Education has only 2 of 3 trust images populated.

### Industries hub trust + tiles — 8 (99 → 106)

`page.industries.json` · Section: `ds-lp-industries`. Folder: `Case study cards/` (trust) + `Homepage tiles/` or `Category service tiles/` (tiles).

| # | Slot | Current state |
|---|---|---|
| 99 | trust_image_1 | `OCI-Healthcare.jpg` |
| 100 | trust_image_2 | `OCI-Education-1.jpg` |
| 101 | trust_image_3 | `OCI-Government.jpg` |
| 102 | tile_image_1 | `OCI-Healthcare.jpg` (re-use) |
| 103 | tile_image_2 | `OCI-Education-1.jpg` (re-use) |
| 104 | tile_image_3 | `OCI-Government.jpg` (re-use) |
| 105 | tile_image_4 | `OCI-Workplace-1.jpg` |
| 106 | tile_image_5 | `Inspiration-Executive-Office_b502dff2...jpg` |

### Brands hub tile images — 6 (107 → 112)

`page.brands.json` · Section: `ds-lp-brands`. Folder: `Brandbanners/` or `Sub Category/`. Spec: 4:3 tile.

| # | Slot | Current state |
|---|---|---|
| 107 | keilhauer_image | `keilhauer-space.jpg` (stock-y) |
| 108 | ergocentric_image | `ergocentric-space.jpg` (stock-y) |
| 109 | global_image | `global-teknion-space.jpg` (stock-y) |
| 110 | otg_image | **blank** |
| 111 | heartwood_image | **blank** |
| 112 | obusforme_image | **blank** |

### OECM trust images — 3 (113 → 115)

`page.oecm.json` · Section: `ds-lp-oecm`. Folder: `Case study cards/`. Spec: 4:3.

| # | Slot | Current state |
|---|---|---|
| 113 | trust_image_1 | `OCI-Healthcare-Carousel-3.jpg` |
| 114 | trust_image_2 | `OCI-Education-1_643da778...jpg` |
| 115 | trust_image_3 | `OCI-Government-Federal-Furniture-Gallery-Image-1.jpg` |

### Design Services secondary images — 2 (116 → 117)

`page.design-services.json` · Section: `ds-lp-design-services`. Folder: `Case study cards/` or `Category service tiles/`.

| # | Slot | Current state |
|---|---|---|
| 116 | form_photo (right-column photo by lead form) | `OCI-Planning-Desogn.jpg` (typo in filename — stock-y) |
| 117 | client_logo (Kawartha Dairy) | blank — text fallback used |

### Customer Stories cards — 5 (118 → 122)

`page.customer-stories.json` · Section: `ds-lp-customer-stories`. Folder: `Case study cards/`. Spec: card image.

| # | Slot | Current state |
|---|---|---|
| 118 | story1_image | `Mattamy-1.jpg` |
| 119 | story2_image | `OCI-Government-Federal-Furniture-Gallery-Image-1.jpg` |
| 120 | story3_image | `Inspiration-Executive-Office_46600701...jpg` |
| 121 | story4_image | **blank** |
| 122 | story5_image | **blank** |

### Our Work gallery photos — 12 (123 → 134)

`page.our-work.json` · Section: `ds-lp-our-work`. Folder: `Case study cards/`. Spec: photo_1, _7, _11 are "wide"; rest are standard.

| # | Slot | Photo subject (per schema label) | Current state |
|---|---|---|---|
| 123 | photo_1 (wide) | Corporate boardroom | `Subject-Areas-boardroom.jpg` |
| 124 | photo_2 | Executive office | `Inspiration-Executive-Office_46600701...jpg` |
| 125 | photo_3 | Conference room | `Inspiration-Conference-1-1.jpg` |
| 126 | photo_4 | Open-plan workstations | `OCI-Workplace-1_8dc819f3...jpg` |
| 127 | photo_5 | Reception | `Inspiration-Reception.jpg` |
| 128 | photo_6 | Healthcare waiting | `OCI-Healthcare-Carousel-3_8821b2f8...jpg` |
| 129 | photo_7 (wide) | Open-plan office | `Mattamy-2.jpg` |
| 130 | photo_8 | Ergonomic workstation | `Inspiration-Ergonomics.jpg` |
| 131 | photo_9 | Breakroom | `OCI-Inspiration-Breakroom.jpg` |
| 132 | photo_10 | Acoustic pods | `Pods-4-1.jpg` |
| 133 | photo_11 (wide) | Government office | `OCI-Government-Federal-Furniture-Gallery-Image-1.jpg` |
| 134 | photo_12 | Education | `OCI-Education-1_643da778...jpg` |

---

## LOW Priority Slots (14)

### About page hero — 1 (135)

| # | Slot | Page | Current state | Folder |
|---|---|---|---|---|
| 135 | hero_image | `/pages/about` | `About-us-1.webp` (legacy OCI) — needs branded BBI replacement | `Categorybanners/` or `Case study cards/` |

### Cornerstone Post 1 article images — ~4 (136 → 139) — DEFERRED TO TUESDAY

`articles/689003888953` (handle `oecm-ontario-school-boards-office-furniture`, blog `news`). Article body lives in Shopify Admin (`article.body_html`), not in a theme template.

| # | Slot | Type | Current state | Folder |
|---|---|---|---|---|
| 136 | Featured image | `article.image` | **null** (no featured image — Option A v1 fallback per HALT 0 critical safeguard) | `Case study cards/` (real Ontario school-board photo) |
| 137 | Inline image 1 | `<img>` in `body_html` | none | `Case study cards/` |
| 138 | Inline image 2 | `<img>` in `body_html` | none | `Case study cards/` |
| 139 | Inline image 3 (optional) | `<img>` in `body_html` | none | `Case study cards/` |

> Per `prompt-image-slot-inventory.md` line 64 and Steve homework: "Cornerstone Post 1 (published, can swap featured image + inline)" is deferred to Tuesday. Article URL stays stable; only `article.image` and `body_html` change.

### Contact page — 0 image slots

`page.contact.json` + `ds-lp-contact.liquid` has only a `logo` image_picker (sitewide logo, already locked to `bbi-logo-v2`). No content hero. Map embed is iframe/embed-based, not a Shopify image. **No slot needs filling.**

### FAQ page — 0 image slots

`ds-lp-faq.liquid` schema has only `logo` — no content images. **No slot needs filling.**

### PDP / search / 404 / cart / blog-list — 0 image slots in scope

- `ds-pdp-base` (PDP): images come from Shopify product images, **out-of-scope per prompt** (separate Shopify Admin workflow).
- `ds-blog-list` / `ds-article` / `ds-search-results` / `ds-cart-base` / `ds-system-404`: schema only has `logo`. No content image slots.

---

## Out-of-Scope Pages Inventoried (non-blocking, for completeness)

Three brand pages exist but are not in the prompt scope (prompt requested only OTG / GFG / Heartwood). Listed here for visibility — these can be Tue/Wed post-launch:

- `/pages/brands-ergocentric` → `ds-lp-brands-ergocentric` hero_image
- `/pages/brands-keilhauer` → `ds-lp-brands-keilhauer` hero_image
- `/pages/brands-obusforme` → `ds-lp-brands-obusforme` hero_image

Each is a `ds-lp-brands-*` section with the same hero pattern (1 image_picker, 5:4). If Leo wants these in the picker too, add 3 slots to the HIGH or MED tier (folder: `Brandbanners/`).

PDP product images are handled via Shopify Admin product images (`Top product tiles/` Upwork folder maps best for the Idea #15 trio). Excluded from this inventory per scope.

---

## Suggested Phase 2 (Interactive Picker) Approach

**Recommended order:** CRITICAL → HIGH → MED → LOW (descending visibility on LAUNCH-2 / Idea #13 critical-path).

**Critical-path-only launch path (recommended for Monday LAUNCH-2):**

1. **CRITICAL + HIGH (~56 min @ 2 min/slot)** — covers homepage hero + 3 featured product cards + 9 category heroes + 6 industry heroes + 3 brand heroes + 3 service heroes + Brands hub + OECM + Quote. After this, every "headline" hero/featured image on every major page is real.
2. **Defer MED + LOW (~3.5 hours combined) to Tue/Wed post-launch.** None of these are visible above the fold on the highest-traffic flows.
3. **Cornerstone Post 1 (slots 136-139)** explicitly deferred to Tuesday per Steve homework + Day 11 plan — does **not** block LAUNCH-2.

**Picker UX tip (for Step 2 author):** show Leo each slot with (a) the LIVE Avada URL, (b) the DEV preview URL with `preview_theme_id=186373570873`, (c) the suggested Upwork folder path, and (d) one-line context on what the surface is selling. Save progress after every 5 slots so Leo can stop / resume.

---

## Notes

- Folder taxonomy reflects Leo's 2026-05-25 screenshot of `~/Desktop/bbi-upwork-delivery/` (8 folders, ~137 images).
- **DEV preview URLs require Shopify Admin auth.** Leo must be logged into the `office-central-online` Shopify store in the same browser session to view them.
- **LIVE URLs show the current Avada theme** — none of the BBI placeholders/refs in this inventory render LIVE today. They become visible after **LAUNCH-2** flips DEV theme `186373570873` to live (DO NEXT #11).
- Two pages are intentionally **0-slot**: `/pages/contact` and `/pages/faq` — they have logo only, no content imagery.
- The legacy `shopify://shop_images/*` references throughout are **stock-y Avada-era photos that still resolve** (uploaded to the store's Shopify Files pre-BBI migration) but are unbranded, mismatched in subject (e.g. seating tiles using education photos), and generally not specific to BBI's Ontario commercial-furniture audience. Treat them all as "**stock-y image needing replacement**" rather than broken refs.
- Homepage placeholders are **CSS-class-driven** (`bbi-hp-ph--*`), not theme-editor image_picker slots — they will require either a custom_liquid edit (swap `<div>` for `<img>`) or a CSS edit (`background-image: url(...)`) in Step 2 / Step 46 IMAGE SWAP.
- Per `bbi-build-state.md` line 117 (Task #13 from PR #15), the homepage's 14 broken `bbi-hp-*.jpg` refs were already replaced with safe DS placeholders on 2026-05-21. The slots remain; only the fallback rendering changed.
- The Upwork delivery is sized at ~137 images — this inventory counts ~137 slots needing fill. Likely intentional sizing.
