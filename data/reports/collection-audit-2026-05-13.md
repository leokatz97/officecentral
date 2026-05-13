# BBI Collection Audit
_Generated 2026-05-13 by COLLECTION-AUDIT (Sub-step C1). Read-only._
_Input for Sub-step C2 (apply dispositions)._

---

## Summary

- **Total collections:** 371 (smart: 49, custom: 322)
- **By product count:** 0 = 148, 1–2 = 45, 3–9 = 100, 10+ = 78
- **Dispositions proposed:**
  - KEEP: 86
  - KEEP-WITH-NOTE: 93
  - INVESTIGATE: 39
  - REDIRECT: 3
  - ARCHIVE: 150

> **⚠️ URGENT (fix before Sub-step C2):** `/collections/other` (337 products) is currently **published** — customers can browse 337 archived/staging products at that URL. Unpublish immediately via Shopify Admin. This is a data-exposure issue, not a collection-cleanup item.

---

## Action-required collections

---

### INVESTIGATE (39 collections)

#### Priority INVESTIGATE (named, require Steve decision)

**`global-teknion`**
- Type: smart | Products: 21 | Status: published
- Rules: `tag equals brand:global-teknion`
- 🟡 **TEMPLATE-REFERENCED**
- Smart brand collection has 21 products but should approach 0 after VENDOR-NORMALIZE-2 runs (those products are tagged brand:global-teknion from pre-normalization). Once VENDOR-NORMALIZE-2 normalises vendor tags the count will drop. Steve: confirm whether to keep this collection pointing at brand:global-teknion after normalization, or retag to brand:global or new canonical slug.

**`oecm-eligible`**
- Type: smart | Products: 592 | Status: published
- Rules: `tag equals oecm-eligible`
- Smart collection with tag:oecm-eligible rule shows 592 products = essentially the entire active catalog. Known mass-tag bug (audit-tech-debt-2026-05-12 BUG-FIX-2). OECM page currently surfaces the full catalog instead of a curated list. Steve: confirm whether oecm-eligible should be a curated subset or removed as a storefront collection.

**`other`**
- Type: custom | Products: 337 | Status: published
- Custom collection with 337 products — PE Pass 2 staging collection for archived/Other products. Currently PUBLISHED, meaning customers can browse all 337 archived products at /collections/other. Should be unpublished immediately. The collection needs to stay as a Shopify collection for admin purposes, but should never be navigable by customers.

**`keilhauer`**
- Type: smart | Products: 0 | Status: published
- Rules: `tag equals brand:keilhauer`
- 🟡 **TEMPLATE-REFERENCED**
- Smart collection (tag:brand:keilhauer), 0 products. BBI brand page /pages/brands-keilhauer exists and is published. No products tagged brand:keilhauer yet — needs PE Pass 3 to surface Keilhauer products. KEEP the collection; re-evaluate callable/callout status after PE Pass 3.

**`ergocentric`**
- Type: smart | Products: 1 | Status: published
- Rules: `tag equals brand:ergocentric`
- 🟡 **TEMPLATE-REFERENCED**
- Smart collection (tag:brand:ergocentric), 1 product. BBI brand page /pages/brands-ergocentric exists. Only 1 product tagged brand:ergocentric. KEEP the collection; re-evaluate after PE Pass 3 to confirm product depth.

**`room-break-room`**
- Type: smart | Products: 0 | Status: published
- Rules: `tag equals room:break-room`
- Smart collection (tag:room:break-room), 0 products. No products are tagged room:break-room in the current catalog. No category page for break-room in the current site architecture. Recommend ARCHIVE or repurpose if a break-room/lounge category page is planned.

**`home-page`**
- Type: custom | Products: 8 | Status: published
- 8-product custom collection — appears to be a legacy Avada/theme homepage feature collection. No corresponding nav link or brand page. The 8 products may be legacy featured items. Steve: is this actively used by any Avada homepage section or can it be archived?

**`featured-homepage`**
- Type: custom | Products: 3 | Status: unpublished
- 3-product custom unpublished collection — same pattern as home-page, legacy homepage features. Unpublished so low risk, but confirm whether to archive.

**`buy-canadian`**
- Type: custom | Products: 0 | Status: published
- 0-product custom published collection. Potentially high SEO value as "Buy Canadian" is a strong B2B procurement keyword in the current political climate (2026 Canada-US trade tension). Steve: worth populating with products tagged country_of_manufacture:Canada or archiving. Easy win to populate since Heartwood, ObusForme, ergoCentric are Canadian manufacturers.

#### Dead-tile INVESTIGATE (30 collections — 0-product collections linked as sub-collection tiles)

These 30 custom collections are referenced as navigation tiles in category page templates
(`ds-browse-faq.liquid`, `ds-cc-base.liquid`, category template JSONs). They exist in Shopify
but have 0 products — every tile currently leads to an empty collection page.

**The fix is either (A) populate the collection by tagging products, or (B) remove the tile**
**from the template JSON for that category page. Both require a code or product-data change.**

| Handle | Title | Notes |
|---|---|---|
| `acoustic-panels` | Acoustic Panels | 🔥 high-priority — acoustic panels companion to pods |
| `acoustic-pods` | Acoustic Pods | 🔥 high-priority — acoustic pods is a hot category per ICP |
| `active-seating` | Active Seating | high-priority — key seating sub-category |
| `beam-seating` | Beam Seating | high-priority — key seating sub-category |
| `bench-seating` | Bench Seating | high-priority — key seating sub-category |
| `boardroom-seating` | Boardroom Seating | high-priority — key seating sub-category |
| `boardroom-storage` | Boardroom Storage | consider removing tile — niche |
| `cafe-tables` | Café & Bistro Tables | consider removing tile — niche |
| `chair-accessories` | Chair Accessories | consider removing tile — niche |
| `conference-seating` | Conference Seating | high-priority — key seating sub-category |
| `desktop-accessories` | Desktop Accessories | consider removing tile — niche |
| `ergonomic-accessories` | Ergonomic Accessories | high-priority — ergonomic accessories for Wave B |
| `executive-seating` | Executive Seating | high-priority — key seating sub-category |
| `focus-rooms` | Focus Room Furniture | 🔥 high-priority — focus rooms / phone booths overlap |
| `healthcare-seating` | Healthcare Seating | high-priority — healthcare vertical |
| `high-density-storage` | High-Density Storage | populate or remove tile |
| `mailboxes` | Mailboxes & Sorters | populate or remove tile |
| `media-storage` | Media & AV Storage | populate or remove tile |
| `mobile-storage` | Mobile Storage Carts | populate or remove tile |
| `modular-workstations` | Modular Workstations | populate or remove tile |
| `multipurpose-tables` | Multi-Purpose Tables | consider removing tile — niche |
| `nesting-tables` | Nesting & Folding Tables | consider removing tile — niche |
| `outdoor-tables` | Outdoor Tables | populate or remove tile |
| `personal-storage` | Personal Storage | consider removing tile — niche |
| `privacy-screens` | Privacy Screens | consider removing tile — niche |
| `side-tables` | Side & Occasional Tables | consider removing tile — niche |
| `standing-tables` | Standing & High Tables | populate or remove tile |
| `training-desks` | Training Room Desks | populate or remove tile |
| `wall-storage` | Wall-Mounted Storage | consider removing tile — niche |
| `waste-recycling` | Waste & Recycling | populate or remove tile |

---

### REDIRECT (3 collections)

| Handle | Title | Type | Products | Redirect Target | Rationale |
|---|---|---|---|---|---|
| `global-furniture` | Global Furniture Group | custom | 0 | `/pages/brands` | Legacy 0-product collection, no equity, superseded by brand/hub pages |
| `manufacturers-we-support` | Manufacturers we support | custom | 0 | `/pages/brands` | Legacy 0-product collection, no equity, superseded by brand/hub pages |
| `teknion-upscale-products` | Teknion Upscale Products | custom | 0 | `/pages/brands-global-teknion` | Legacy 0-product collection, no equity, superseded by brand/hub pages |

---

### ARCHIVE (150 collections)

All 150 are custom collections with 0–2 products and no theme template references.
All have SEO redirect recommended (even archived collections may have indexed URLs).
Blanket redirect strategy: product-category URLs → closest parent nav collection;
legacy specialty/OCI-only URLs → `/collections/business-furniture`.

**Sub-groups:**

**A. Childcare / education / residential — clearly out-of-scope for BBI B2B (33 collections)**

`art-easel`, `arts-crafts`, `beds-matresses`, `bedside-tables`, `book-carts-easels`, `book-display-book-racks`, `book-displays-storage`, `boot-cubby`, `change-tables`, `classroom-storage`, `diaper-shelves`, `doll-furniture`, `dramatic-play`, `dressers`, `educational`, `garment-care`, `headboards-footboards`, `infant-toddler`, `interactive-play-funriture`, `kids-chairs`, `kids-couches-coming-soon`, `kids-desks`, `kids-display-stands`, `manipulative-play`, `mattresses`, `paint-dryers`, `preschool-couches-chairs`, `puzzle-shelf`, `resident-room-seating`, `sand-water-tables`, `strollers`, `toddler-lockers`, `wash-stands`

**B. Legacy OCI specialty brands / verticals (17 collections)**

`diagnostic-carts-arms`, `dining-room`, `dinning-furniture`, `dinning-seating`, `dinning-tables`, `dorm-penitentiary-furniture`, `epson`, `exam-room-seating`, `facility-breakroom`, `facility-supplies`, `heaters`, `hp`, `ink-and-toner`, `laboratory-furniture`, `samsung`, `snow-and-ice-melts`, `umbrellas`

**C. Duplicate / vestigial variants (12 collections)**

`bariatric-seating-1`, `benching-1`, `blinder`, `contemporary-laminate`, `contemporary-veneer`, `frontpage`, `furniture-accessories`, `furniture-collections`, `seating-1`, `tables-1`, `workstation`, `workstations-computer-desks`

**D. Thin 0–2 product BBI-adjacent collections without template reference (88 collections)**

`adjustable-2-shelf-units`, `adjustable-block-shelf-units`, `adjustable-hinged-units`, `anti-fatigue-mats`, `audio-visual-equipment`, `av-stand`, `benches`, `benching-desks`, `bin-storage-tower`, `binder-accessories`, `binder-pockets`, `block-shelf-units`, `book-carts`, `bookcases-1`, `cabinets-racks-accessories`, `carpet-chair-mats`, `carts`, `carts-stands`, `casters`, `casters-wheels`, `castors-seating`, `chair-mats`, `chairmats`, `charging-units`, `cluster-seating`, `coat-cubbies`, `coat-cubbies-lockers`, `coat-garment-hooks`, `coat-racks`, `coat-racks-accessories`, `computer-accessories`, `convertisseur-de-bureau`, `cubby-storage-units`, `desk-accessories`, `desk-tables-sit-stand-classroom`, `desk-top-stand`, `desks-benching-units`, `doors`, `end-tab-file-cabinets-storage-coming-soon`, `end-tab-filing-storage`, `executive-desks`, `filing-storage-accessories`, `fixed-shelf-units`, `floor-mats`, `folding-tables`, `healthcare`, `higback`, `hutch`, `insulated-file-cabinets`, `ipad-holder`, `kids-play-tables`, `library-shelving`, `metal-frame-adjustable-tables`, `metal-shelving`, `mirrors-room-dividers`, `mobile-coat-cubby`, `mobile-files-carts`, `modesty-panels`, `monitor-machine-stands`, `monitor-stands-risers`, `multi-storage-units`, `occasional-tables`, `office-supplies`, `office-teachers-chairs`, `overbed-tables`, `overhead-storage-cabinets`, `picnic-tables`, `podiums`, `reception-area-accent-tables`, `reception-low-tables`, `refreshment-carts-stands`, `safes`, `sectionals`, `shelving`, `small-bin-cubby-storage-units`, `stands`, `step-stools`, `storage-and-filing`, `table-tops`, `teachers-cabinets`, `technology`, `tops`, `tv-units`, `utility-service-carts`, `waiting-room-seating`, `wardrobes`, `wobble-chairs`, `wood-frame-tables`

---

### KEEP-WITH-NOTE (93 collections)

Collections with strategic or structural value despite thin product counts.
No immediate action in Sub-step C2, but each has a noted gap to track.

#### Highest-priority KEEP-WITH-NOTE

**`quiet-spaces`** (9 products, smart, published)
- 🔴 **NAV-LINKED, only 9 products** — nav prominently features this; acoustic/quiet-space products are a top ICP priority. Must reach ≥10 products to justify primary nav placement. Tagging fix in COLLECTION-CLEANUP-1 Sub-step B.

**`telephone-booths`** (1 products, custom, published)
- 🟡 1 product, template-referenced. Phone booths = quiet spaces sub-category. Add more products or merge tile into acoustic-pods once that collection is populated.

**`white-board`** (1 products, custom, published)
- 🟡 1 product, template-referenced. Whiteboard/display = common office accessory. Add products or remove tile.

**`lounge-seating`** (2 products, custom, published)
- 🟡 2 products, template-referenced. Lounge seating is a real category. Should have more depth from tagging pass.

#### Full KEEP-WITH-NOTE list (sorted by product count)

| Handle | Type | Products | Nav? | Template? | Note |
|---|---|---|---|---|---|
| `telephone-booths` | custom | 1 |  | ✓ | custom, 1 product(s) — referenced in template but very thin |
| `white-board` | custom | 1 |  | ✓ | custom, 1 product(s) — referenced in template but very thin |
| `lounge-seating` | custom | 2 |  | ✓ | custom, 2 product(s) — referenced in template but very thin |
| `bar-height-tables` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `cafeteria-breakroom-tables` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `chairmat-accessories` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `clinician-screens` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `cribs` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `furniture` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `gaming` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `outerwear` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `panel-systems` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `reception` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `recliners` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `sit-stand-workstations` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `storage-cabinets-lockers` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `tablet-chairs` | custom | 3 |  |  | custom, 3 products — thin but has some depth |
| `24-hour-seating` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `cafeteria-kitchen-tables` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `chairs` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `desk-top-dividers` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `desktop-risers` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `fire-resistant-file-cabinets-safes` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `lecture-hall-seating` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `lighting` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `lighting-1` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `office-furniture` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `other-1` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `outdoor-seating` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `planters` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `student-tables` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `training-room-tables` | custom | 4 |  | ✓ | custom, 4 products — referenced in template tile but thin |
| `winter-supplies` | custom | 4 |  |  | custom, 4 products — thin but has some depth |
| `air-quality-management` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `bariatric-seating` | custom | 5 |  | ✓ | custom, 5 products — referenced in template tile but thin |
| `chairmats-accessories` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `coffee-tables` | custom | 5 |  | ✓ | custom, 5 products — referenced in template tile but thin |
| `end-tables-tables` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `fire-resistant-safes` | custom | 5 |  | ✓ | custom, 5 products — referenced in template tile but thin |
| `kids-bookcases` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `lateral-storage-combo-storage` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `lecterns-podiums` | custom | 5 |  | ✓ | custom, 5 products — referenced in template tile but thin |
| `nesting-chairs-chair` | custom | 5 |  | ✓ | custom, 5 products — referenced in template tile but thin |
| `side-coffee-table` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `student-chairs` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `student-desks` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `table-bases` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `training-flip-top-tables` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `walls` | custom | 5 |  |  | custom, 5 products — thin but has some depth |
| `fire-resistant-file-cabinets` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `fire-resistant-file-cabinets-storage` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `keyboard-trays` | custom | 6 |  | ✓ | custom, 6 products — referenced in template tile but thin |
| `lockers` | custom | 6 |  | ✓ | custom, 6 products — referenced in template tile but thin |
| `metal-vertical-files` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `panels-partitions` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `pedestals` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `side-coffee-table-tables` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `table-desks` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `table-desks-1` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `vertical-file-cabinets-storage` | custom | 6 |  | ✓ | custom, 6 products — referenced in template tile but thin |
| `vertical-files` | custom | 6 |  |  | custom, 6 products — thin but has some depth |
| `wardrobe-storage` | custom | 6 |  | ✓ | custom, 6 products — referenced in template tile but thin |
| `desk-top-sit-stand-ergonomic-products` | custom | 7 |  |  | custom, 7 products — thin but has some depth |
| `drafting-tables` | custom | 7 |  | ✓ | custom, 7 products — referenced in template tile but thin |
| `educational-furniture` | custom | 7 |  |  | custom, 7 products — thin but has some depth |
| `folding-stacking-chairs-carts` | custom | 7 |  |  | custom, 7 products — thin but has some depth |
| `lateral-files-storage` | custom | 7 |  | ✓ | custom, 7 products — referenced in template tile but thin |
| `ottomans` | custom | 7 |  |  | custom, 7 products — thin but has some depth |
| `pedestal-drawers` | custom | 7 |  | ✓ | custom, 7 products — referenced in template tile but thin |
| `pedestal-drawers-1` | custom | 7 |  |  | custom, 7 products — thin but has some depth |
| `bases` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `cafe-lounge-seating` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `folding-chair-chair` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `folding-tables-tables` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `industrial-seating` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `lateral-file-cabinets-storage` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `meeting-conference-room-tables` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `mobile-pedestals` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `monitor-arms` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `multi-person-workstations` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `multi-person-workstations-1` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `sound-dampeners` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `stools` | custom | 8 |  |  | custom, 8 products — thin but has some depth |
| `storage-cabinets` | custom | 8 |  | ✓ | custom, 8 products — referenced in template tile but thin |
| `bookcases` | custom | 9 |  | ✓ | custom, 9 products — referenced in template tile but thin |
| `credenzas` | custom | 9 |  | ✓ | custom, 9 products — referenced in template tile but thin |
| `desk-top-sit-stand` | custom | 9 |  |  | custom, 9 products — thin but has some depth |
| `laminate-bookcases` | custom | 9 |  |  | custom, 9 products — thin but has some depth |
| `multi-person-workstations-desks` | custom | 9 |  | ✓ | custom, 9 products — referenced in template tile but thin |
| `pedestal-drawers-storage` | custom | 9 |  |  | custom, 9 products — thin but has some depth |
| `quiet-spaces` | smart | 9 | ✓ | ✓ | nav-anchored but only 9 products — populate or reconsider na |
| `reception-desks-desks` | custom | 9 |  | ✓ | custom, 9 products — referenced in template tile but thin |
| `round-square-tables` | custom | 9 |  |  | custom, 9 products — thin but has some depth |

---

## Healthy collections (KEEP — no action needed)

**Total: 86** (smart infrastructure, nav-anchored, healthy custom sub-collections)

| Handle | Type | Products | Nav? | Notes |
|---|---|---|---|---|
| `fees-products` | smart | 653 |  | system/app |
| `smart-products-filter-index-do-not-delete` | smart | 653 |  | system/app |
| `all` | smart | 648 | ✓ | system/app |
| `products` | smart | 648 |  | system/app |
| `products-1` | smart | 648 |  | system/app |
| `avada-best-sellers` | smart | 624 |  | system/app |
| `business-furniture` | smart | 624 |  | smart infra |
| `all-business-furniture` | smart | 190 |  | smart infra |
| `seating` | smart | 102 | ✓ | smart infra |
| `orderly-emails-recommended-products` | smart | 100 |  | system/app |
| `all-seating` | smart | 96 |  | smart infra |
| `type-chairs` | smart | 96 |  | smart infra |
| `medium-back-seating` | custom | 49 |  | custom |
| `highback-seating` | custom | 46 |  | custom |
| `room-private-office` | smart | 45 |  | smart infra |
| `mesh-seating` | custom | 44 |  | custom |
| `guest-seating` | custom | 39 |  | custom |
| `all-tables` | smart | 32 |  | smart infra |
| `leather-faux-seating` | custom | 32 |  | custom |
| `tables` | smart | 32 | ✓ | smart infra |
| `type-tables` | smart | 32 |  | smart infra |
| `l-shape-desks` | custom | 31 |  | custom |
| `l-shape-desks-desks` | custom | 31 |  | custom |
| `all-desks` | smart | 30 |  | smart infra |
| `desks` | smart | 30 | ✓ | smart infra |
| `l-shape-desks-1` | custom | 30 |  | custom |
| `type-desks` | smart | 30 |  | smart infra |
| `reception-side-guest-chairs` | custom | 28 |  | custom |
| `l-shape` | custom | 27 |  | custom |
| `all-boardroom` | smart | 25 |  | smart infra |
| `boardroom` | smart | 25 | ✓ | smart infra |
| `room-boardroom` | smart | 25 |  | smart infra |
| `height-adjustable-tables-desks` | custom | 21 |  | custom |
| `height-adjustable-tables` | custom | 19 |  | custom |
| `all-storage` | smart | 18 |  | smart infra |
| `combo-units` | custom | 18 |  | custom |
| `desks-straight` | custom | 18 |  | custom |
| `height-adjustable-tables-1` | custom | 18 |  | custom |
| `stacking-chairs-chair` | custom | 18 |  | custom |
| `storage` | smart | 18 | ✓ | smart infra |
| `type-storage` | smart | 18 |  | smart infra |
| `straight-desks-desks` | custom | 17 |  | custom |
| `all-ergonomic` | smart | 16 |  | smart infra |
| `all-panels` | smart | 16 |  | smart infra |
| `ergonomic-products` | smart | 16 | ✓ | smart infra |
| `lounge-chairs-seating` | custom | 16 |  | custom |
| `lounge-reception` | smart | 16 |  | smart infra |
| `panels-room-dividers` | smart | 16 | ✓ | smart infra |
| `stacking-seating` | custom | 16 |  | custom |
| `u-shape-desks-desks` | custom | 16 |  | custom |
| `stools-seating` | custom | 15 |  | custom |
| `u-shape-desks` | custom | 15 |  | custom |
| `u-shape-desks-1` | custom | 15 |  | custom |
| `accessories` | smart | 14 | ✓ | smart infra |
| `all-accessories` | smart | 14 |  | smart infra |
| `type-accessories` | smart | 14 |  | smart infra |
| `bookcases-storage` | custom | 13 |  | custom |
| `office-suites-desks` | custom | 13 |  | custom |
| `room-dividers-panels-dividers` | custom | 13 |  | custom |
| `storage-cabinets-storage` | custom | 13 |  | custom |
| `student-tables-educational-furniture` | custom | 13 |  | custom |
| `meeting-tables` | custom | 12 |  | custom |
| `panels-dividers` | custom | 12 |  | custom |
| `straight-desks` | custom | 12 |  | custom |
| `boardroom-conference-meeting` | custom | 11 |  | custom |
| `fire-resistant-safes-storage` | custom | 11 |  | custom |
| `library-study-tables` | custom | 11 |  | custom |
| `lounge-chairs` | custom | 11 |  | custom |
| `stools-drafting-chairs` | custom | 11 |  | custom |
| `big-heavy-seating` | custom | 10 |  | custom |
| `boardroom-conference-meeting-1` | custom | 10 |  | custom |
| `desktop-sit-stand` | custom | 10 |  | custom |
| `lounge` | custom | 10 |  | custom |
| `power-modules-accessories` | custom | 10 |  | custom |
| `task-chairs` | smart | 10 |  | smart infra |
| `all-quiet-spaces` | smart | 9 |  | smart infra |
| `room-dividers` | custom | 7 |  | custom |
| `room-reception` | smart | 7 |  | smart infra |
| `room-lounge` | smart | 6 |  | smart infra |
| `type-lounge` | smart | 6 |  | smart infra |
| `room-open-plan` | smart | 4 |  | smart infra |
| `room-training-room` | smart | 4 |  | smart infra |
| `type-outdoor` | smart | 4 |  | smart infra |
| `mandatory-fees` | smart | 1 |  | system/app |
| `bundle-builder-products` | smart | 0 |  | system/app |
| `room-accessories` | custom | 0 |  | custom |

---

## Nav + footer cross-reference

Collections in nav/footer that have cleanup-relevant dispositions:

| Collection | Products | Disposition | Risk |
|---|---|---|---|
| `quiet-spaces` | 9 | KEEP-WITH-NOTE | 🔴 Nav-linked but below 10-product threshold — users clicking "Quiet Spaces" in nav see only 9 products |
| `accessories` | 14 | KEEP | — |
| `ergonomic-products` | 16 | KEEP | — |
| `panels-room-dividers` | 16 | KEEP | — |
| `boardroom` | 25 | KEEP | — |
| `tables` | 32 | KEEP | — |
| `desks` | 30 | KEEP | — |
| `storage` | 18 | KEEP | — |
| `seating` | 102 | KEEP | — |

**No ARCHIVE or REDIRECT collections are currently referenced in the primary nav or footer.**
The 3 REDIRECT targets (`global-furniture`, `manufacturers-we-support`, `teknion-upscale-products`)
do not appear in `bbi-nav.liquid` or `bbi-footer.liquid`. No nav/footer updates required before
Sub-step C2 runs the redirects.

**`global-furniture` IS referenced in theme templates** (ds-browse-faq.liquid / category page tiles)
— update the tile link to `/pages/brands` as part of Sub-step C2 before archiving the collection.

---

## Redirect plan

### Named redirects (Sub-step C2 to execute)

| From URL | To URL | Reason |
|---|---|---|
| `/collections/global-furniture` | `/pages/brands` | legacy 0-product custom; superseded by brands hub |
| `/collections/manufacturers-we-support` | `/pages/brands` | legacy editorial 0-product custom; redirect to brands hub |
| `/collections/teknion-upscale-products` | `/pages/brands-global-teknion` | legacy 0-product custom; redundant with global-teknion smart collection |

### Blanket archive redirect strategy (Sub-step C2)

For the 150 ARCHIVE collections, Sub-step C2 should add bulk redirects to
`data/url-redirects-bulk.csv` using this mapping:

| Category | Redirect target |
|---|---|
| Seating sub-types (boardroom-seating, active-seating, etc.) | `/collections/seating` |
| Desk sub-types (executive-desks, etc.) | `/collections/desks` |
| Storage sub-types (media-storage, etc.) | `/collections/storage` |
| Table sub-types | `/collections/tables` |
| Childcare / residential / OCI-only | `/collections/business-furniture` |
| Specialty brands (samsung, hp, epson) | `/collections/accessories` |

---

## Recommendations for Sub-step C2 scope

### Immediate (before Sub-step C2 runs collection changes)

1. **Unpublish `/collections/other` NOW** — 337 archived products are publicly browsable.
   Admin API call: `PUT /admin/api/2024-04/collections/{other_id}.json` with `published: false`.
   This is a data-exposure issue, not a collection-cleanup item. 5-minute fix.

### Sub-step C2 actions (grouped by type)

2. **Add 3 redirects** to `data/url-redirects-bulk.csv`:
   - `/collections/global-furniture` → `/pages/brands`
   - `/collections/manufacturers-we-support` → `/pages/brands`
   - `/collections/teknion-upscale-products` → `/pages/brands-global-teknion`

3. **Archive 150 collections** (handles listed in ARCHIVE section above).
   Add blanket redirects per strategy table before archiving.
   No nav/footer updates needed (none are nav-linked).

4. **Update template tile** for `global-furniture`: before archiving, find and update
   the tile link in the relevant category template JSON to point at `/pages/brands`.

5. **Populate or de-tile 30 dead-tile INVESTIGATE collections** (see table above).
   Priority order:
   - `acoustic-pods`, `acoustic-panels`, `focus-rooms` — hot categories, tag products ASAP
   - `active-seating`, `executive-seating`, `boardroom-seating`, `conference-seating` — key seating sub-types
   - `healthcare-seating` — healthcare vertical page references this tile
   - `ergonomic-accessories` — Wave B ergonomic category
   - Remaining 21: evaluate individually — populate or remove tile from template

6. **Resolve INVESTIGATE — data issues:**
   - `oecm-eligible`: investigate mass-tag (BUG-FIX-2); decide if collection stays as storefront URL
   - `global-teknion`: confirm product count after VENDOR-NORMALIZE-2 runs; reassess slug
   - `buy-canadian`: populate with Canadian-made products (Heartwood, ObusForme, ergoCentric) OR archive
   - `room-break-room`: no break-room products; archive or add break-room product tags
   - `home-page` / `featured-homepage`: confirm if Avada still uses these; archive if not

7. **Deferred to BRAND-PAGES-1 / VENDOR-NORMALIZE-2:**
   - `keilhauer` — keep infrastructure; re-evaluate callable status post PE Pass 3
   - `ergocentric` — keep infrastructure; re-evaluate callable status post PE Pass 3
   - `global-teknion` — re-evaluate after VENDOR-NORMALIZE-2 runs and product count drops

### Quiet Spaces nav fix (deferred to product tagging pass)

8. **Populate `quiet-spaces` to ≥10 products** — currently 9, nav-linked.
   Acoustic pod, phone booth, and sound dampener products need type:quiet-spaces tag.
   Fix in COLLECTION-CLEANUP-1 Sub-step B (product re-tagging pass).

---

_End of report. Input for Sub-step C2 (apply dispositions)._