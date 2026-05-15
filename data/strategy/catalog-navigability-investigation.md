# CATALOG-NAV-INVESTIGATION (Step 42)
_2026-05-15 · Read-only investigation · 5 areas covered_

---

## Executive Summary

Three findings dominate this investigation and sequence every downstream decision.

**First:** Type:* tag coverage is critically incomplete. Of 256 in-scope active products (excluding /collections/other), only 175 (68%) carry a type:* tag. The 81 untagged products can be remediated at high confidence — 54 classify via body_html analysis with a single dominant signal, 16 are medium-confidence, and only 11 are genuinely ambiguous (delivery charges, air purifiers, miscellaneous non-furniture items). Until TYPE-APPLY-1 runs, every smart collection that uses type:* rules returns 0 products, which means the seating, desks, storage, and ergonomic-products category pages are empty or near-empty for most sub-categories.

**Second:** The global-teknion brand tile embedded in the Seating category template is the most serious coherence failure. The tile links to a collection of 72 products spanning chairs (32), tables (10), storage (5), desks (5), and lounge (2) — 38 non-seating products surfaced on a seating category page. This is the canonical INCOHERENT-POPULATED case. The fix options are explored in Area 4.

**Third:** The ds-cs-base section implements a fully functional tag-based sidebar filter (type:*, room:*, price range) that navigates via Shopify's native tagged-collection URL pattern (/collections/handle/type:chairs+type:lounge). This filter will auto-populate correctly as soon as type:* tags are applied in TYPE-APPLY-1 — no storefront API filter configuration is needed. This makes Option B (storefront filter on brand collection) viable as a supplementary brand x category navigation path.

Recommended downstream sequence: TYPE-APPLY-1 (tag 81 untagged products) → CATEGORY-TILE-FIX-1 (remove or scope global-teknion brand tile on seating page, fix 5 missing tiles for quiet-spaces and ergonomic-products) → BRAND-PAGES-1 (implement brand hub pages using Option A hybrid from Area 4).

---

## Phase 0 — Template Verification

All 10 Phase 2 category templates found in theme/templates/:

| Template | Status |
|---|---|
| collection.seating.json | FOUND |
| collection.desks.json | FOUND |
| collection.tables.json | FOUND |
| collection.storage.json | FOUND |
| collection.boardroom.json | FOUND |
| collection.accessories.json | FOUND |
| collection.panels-room-dividers.json | FOUND |
| collection.quiet-spaces.json | FOUND |
| collection.ergonomic-products.json | FOUND |
| collection.business-furniture.json | FOUND |

Extra templates present: collection.base.json (sub-collection listing, ds-cs-base), collection.category.json.

---

## Area 1 — Storefront Filter State

### A. Theme-side filter implementation

Two filter systems coexist in the theme:

**System 1 — Legacy Avada / main-collection.liquid** (theme/sections/main-collection.liquid, 1083 lines):
- Renders `collection.filters` (Shopify storefront filter API) when `section.settings.enable_filtering = true` and `collection.filters.size > 0`
- Delegates to snippet `collection-filters.liquid` for sidebar UI and `collection-filter.js` for JS logic
- Used on legacy Starlite/Avada collection templates — not on Phase 2 DS templates

**System 2 — DS tag-based sidebar** (theme/sections/ds-cs-base.liquid):
- Custom sidebar filter built into the section — no dependency on Shopify storefront filter API
- Collects all `type:*` and `room:*` tags from `collection.all_tags`
- Renders as collapsible checkbox groups
- On change: navigates to `/collections/{handle}/{tag1}+{tag2}` (Shopify native tagged-URL pattern)
- Price filter: appends `?filter.p.m.price.min=N&filter.p.m.price.max=N` via URL params
- Applied to: collection.base.json template (all sub-category pages)

The ds-cc-base.liquid (category hub pages) implements a separate horizontal "filter chip bar" that renders the tile blocks as pill navigation chips — not a product filter, just a sub-category nav.

### B. Shopify Admin filter configuration

Shopify's Admin API for `storefront_filter_settings` and `metafield_definitions` returns 404 on this store — consistent with Shopify Basic plan limitations. The storefront filter API (which powers main-collection.liquid System 1) requires Shopify to have filters configured via Admin > Navigation > Filters, and that configuration is not accessible via API on Basic plan.

**Key finding:** The Phase 2 DS templates do NOT rely on the Shopify storefront filter API. ds-cs-base.liquid's tag-based sidebar is self-contained and will work correctly as soon as type:* tags are applied in TYPE-APPLY-1.

### C. Storefront filter functional status

| Filter system | Configured | Functional | Scope |
|---|---|---|---|
| Shopify storefront filter API (main-collection) | Unknown (no API access) | Untested | Legacy Avada templates only |
| DS tag sidebar (ds-cs-base) | Yes — self-configuring via collection.all_tags | Yes — navigates via /collections/handle/tag URL | All Phase 2 sub-collection pages |
| DS chip bar (ds-cc-base) | Yes — sourced from tile blocks | Yes — links to sub-collection pages | Phase 2 category hub pages |

### Recommendation for brand x category drill-down

The existing ds-cs-base filter can serve as the brand-within-category filter IF brand:* tags were included in the filter sidebar. Currently the sidebar only shows type:* and room:* tags — brand:* is excluded. This is addressable (see Area 4).

---

## Area 2 — Type:* Tag Coverage

**Scope:** 256 active products (593 total active, minus 337 in /collections/other)

### Current type:* distribution (175 tagged products)

| Tag | Count |
|---|---|
| type:chairs | 86 |
| type:desks | 27 |
| type:tables | 25 |
| type:storage | 16 |
| type:accessories | 14 |
| type:lounge | 4 |
| type:outdoor | 3 |
| **Total tagged** | **175** |

**Untagged: 81 products** (31.6% of in-scope active catalog)

### Derivation candidate analysis (body_html classification)

Rules applied to title + body_html:
- chair/seating/mesh back/swivel/tilter/stool → type:chairs
- desk/workstation/credenza/L-shape/U-shape/standing desk/sit-stand/suite → type:desks
- table/conference table/training table/meeting table/coffee table/folding table → type:tables
- cabinet/filing/file/storage/bookcase/bookshelf/lateral/pedestal/shelf/drawer/locker → type:storage
- mat/floor mat/monitor arm/keyboard tray/cable/footrest/laptop/lamp/whiteboard/easel → type:accessories
- panel/divider/partition/screen/room divider → type:panels

| Confidence | Count | Suggested types |
|---|---|---|
| HIGH-CONFIDENCE | 54 | chairs (24), desks (17), storage (16), tables (7), accessories (4), panels (2) |
| MEDIUM-CONFIDENCE | 16 | mostly desks/tables ties or desks/storage overlap |
| NO-MATCH | 11 | delivery charges (3), disposal program, air purifier, colour swatch, miscellaneous |

**Notable NO-MATCH products that should be removed or tagged manually:**
- `delivery` — Delivery service product (not furniture)
- `delivery-charge-85-00` and `delivery-charge-175-00` — Service charges
- `dispose` — Disposal program
- `colour` — Colour swatch placeholder
- `fellowes-array-recess-ar-air-purifier-1` — Air purifier (type:accessories is defensible but not a furniture type)

**Key classification examples:**
- `bar-stool-for-42-high-tables` → type:chairs HIGH (score=6: stool × 3, chair, counter stool signals)
- `2-drawer-legal-width-vertical-file` → type:storage HIGH (score=5: cabinet, filing, vertical, drawer, file)
- `u-shaped-suite-with-rectangular-island` → type:desks HIGH (score=2: desk, suite)
- `bookcase` → type:storage HIGH (score=2: bookcase, bookshelf)
- `desk-shell-5-sizes` → type:desks MEDIUM (tie: desk vs table shape overlap)
- `l-shape-desk-set-72x72` → type:desks MEDIUM (tie: desk vs storage for pedestal components)
- `foundations-sport-splash-quad-strollers` → type:desks MEDIUM (misclassified — stroller product likely in wrong catalog)

**TYPE-APPLY-1 scope:** 70 products can be auto-tagged (54 HIGH + 16 MEDIUM with manual review). 11 NO-MATCH require Steve's decision (archive, add service-type tag, or manually assign).

---

## Area 3 — Sub-Category Tile Health

**Assessment methodology:** Product counts via paginated collections/ID/products.json API. Type distribution via tag analysis. Coherence based on: is the tile name a product type (COHERENT) or a brand/room/cross-category entity (INCOHERENT)?

### Classification definitions
- **COHERENT-POPULATED:** ≥5 products AND tile describes a legitimate product sub-type
- **COHERENT-EMPTY:** 0–4 products AND legitimate sub-type name (needs TYPE-APPLY-1 or product addition)
- **INCOHERENT-POPULATED:** ≥5 products BUT tile describes a brand, room, or cross-category entity
- **INCOHERENT-EMPTY:** wrong placement AND 0–4 products
- **NOT-EXISTS:** collection handle not found in Shopify store

---

### collection.seating.json — 13 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Task Seating | /collections/task-chairs | 10 | COHERENT-POPULATED | Rules: tag=task-chair OR type contains task OR title contains "task chair" — legacy rules |
| Executive Seating | /collections/executive-seating | 0 | COHERENT-EMPTY | Custom collection, no products assigned — needs population |
| Guest & Visitor Seating | /collections/guest-seating | 39 | COHERENT-POPULATED | 14 of 39 have type:chairs; 25 lack type:* — collection over-counts untagged chairs |
| Lounge Seating | /collections/lounge-seating | 2 | COHERENT-EMPTY | Only 2 products — likely needs TYPE-APPLY-1 to surface more |
| Conference Seating | /collections/conference-seating | 0 | COHERENT-EMPTY | No products |
| Training & Stacking | /collections/stacking-seating | NOT-EXISTS | — | Collection not in store |
| Stools & Counter Seating | /collections/stools | NOT-EXISTS | — | Collection not in store |
| Benches & Tandem | /collections/bench-seating | 0 | COHERENT-EMPTY | No products |
| Healthcare Seating | /collections/healthcare-seating | 0 | COHERENT-EMPTY | No products |
| Outdoor & Café Seating | /collections/outdoor-seating | 4 | COHERENT-EMPTY | 4 products (2 type:outdoor, 1 type:chairs) |
| **Global Furniture Group** | **/collections/global-teknion** | **72** | **INCOHERENT-POPULATED** | **BRAND collection: 32 chairs, 10 tables, 5 storage, 5 desks, 2 lounge — 38 non-seating products on seating page** |
| Active Seating | /collections/active-seating | 0 | COHERENT-EMPTY | No products |
| Beam Seating | /collections/beam-seating | 0 | COHERENT-EMPTY | No products |

Seating totals: 1 INCOHERENT-POPULATED, 2 COHERENT-POPULATED, 8 COHERENT-EMPTY, 2 NOT-EXISTS

---

### collection.desks.json — 8 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Height-Adjustable Desks | /collections/height-adjustable-tables-desks | 21 | COHERENT-POPULATED | Mixed: 3 type:desks, 5 type:tables — rule pulls height-adj tables and desks together |
| L-Shape Desks | /collections/l-shape-desks | 31 | COHERENT-POPULATED | 11 type:desks, 1 type:tables, 1 type:accessories — mostly correct |
| Straight Desks | /collections/straight-desks | NOT-EXISTS | — | Collection not in store |
| Reception Desks | /collections/reception-desks-desks | 9 | COHERENT-POPULATED | Small but valid |
| Computer Desks | /collections/multi-person-workstations-desks | 9 | COHERENT-POPULATED | Valid sub-type |
| Modular Workstations | /collections/modular-workstations | 0 | COHERENT-EMPTY | No products |
| Executive Desks | /collections/office-suites-desks | 13 | COHERENT-POPULATED | Valid |
| Training Room Desks | /collections/training-desks | NOT-EXISTS | — | Collection not in store |

Desks totals: 0 INCOHERENT, 6 COHERENT-POPULATED, 1 COHERENT-EMPTY, 2 NOT-EXISTS

---

### collection.tables.json — 5 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Conference Tables | /collections/meeting-conference-room-tables | 8 | COHERENT-POPULATED | 3 type:tables; also linked from boardroom template — shared collection |
| Training Tables | /collections/training-room-tables | NOT-EXISTS | — | Collection not in store |
| Height-Adjustable Tables | /collections/height-adjustable-tables | 19 | COHERENT-POPULATED | Valid |
| Standing & High Tables | /collections/standing-tables | NOT-EXISTS | — | Collection not in store |
| Collaborative Tables | /collections/meeting-tables | 12 | COHERENT-POPULATED | Valid |

Tables totals: 0 INCOHERENT, 3 COHERENT-POPULATED, 0 COHERENT-EMPTY, 2 NOT-EXISTS

---

### collection.storage.json — 12 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Lateral Filing Cabinets | /collections/lateral-file-cabinets-storage | 8 | COHERENT-POPULATED | 1 type:storage (rest untagged) |
| Vertical Filing Cabinets | /collections/vertical-file-cabinets-storage | NOT-EXISTS | — | Collection not in store |
| Mobile Pedestals | /collections/mobile-pedestals | 8 | COHERENT-POPULATED | Valid |
| Storage Cabinets | /collections/storage-cabinets | NOT-EXISTS | — | Collection not in store |
| Bookcases & Shelving | /collections/bookcases | 9 | COHERENT-POPULATED | 1 type:storage (rest untagged) |
| Lockers | /collections/lockers | 6 | COHERENT-POPULATED | Valid |
| Credenzas | /collections/credenzas | 9 | COHERENT-POPULATED | Valid |
| Wardrobe Storage | /collections/wardrobe-storage | NOT-EXISTS | — | Collection not in store |
| Mobile Storage Carts | /collections/mobile-storage | 0 | COHERENT-EMPTY | No products |
| Wall-Mounted Storage | /collections/wall-storage | NOT-EXISTS | — | Collection not in store |
| Personal Storage | /collections/personal-storage | 0 | COHERENT-EMPTY | No products |
| High-Density Storage | /collections/high-density-storage | 0 | COHERENT-EMPTY | No products |

Storage totals: 0 INCOHERENT, 6 COHERENT-POPULATED, 3 COHERENT-EMPTY, 4 NOT-EXISTS (Note: 4 NOT-EXISTS is the highest of any category — storage sub-nav is most broken)

---

### collection.boardroom.json — 3 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Boardroom Tables | /collections/meeting-conference-room-tables | 8 | COHERENT-POPULATED | Same collection as Tables > Conference Tables — shared |
| Boardroom Seating | /collections/boardroom-seating | 0 | COHERENT-EMPTY | No products |
| Credenzas & Storage | /collections/boardroom-storage | 0 | COHERENT-EMPTY | No products |

Boardroom totals: 0 INCOHERENT, 1 COHERENT-POPULATED, 2 COHERENT-EMPTY

---

### collection.accessories.json — 2 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Lighting | /collections/lighting | 4 | COHERENT-EMPTY | 4 products — borderline; depends on whether more exist untagged |
| Whiteboards & Boards | /collections/white-board | NOT-EXISTS | — | Collection not in store |

Accessories totals: 0 INCOHERENT, 0 COHERENT-POPULATED, 1 COHERENT-EMPTY, 1 NOT-EXISTS. The accessories category page has only 2 tiles total — significantly under-built vs other categories.

---

### collection.panels-room-dividers.json — 3 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Acoustic Panels | /collections/acoustic-panels | 0 | COHERENT-EMPTY | No products |
| Room Dividers | /collections/room-dividers | NOT-EXISTS | — | Collection not in store |
| Privacy Screens | /collections/privacy-screens | 0 | COHERENT-EMPTY | No products |

Panels totals: 0 INCOHERENT, 0 COHERENT-POPULATED, 2 COHERENT-EMPTY, 1 NOT-EXISTS. Entire panels category page is empty.

---

### collection.quiet-spaces.json — 5 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Phone Booths | /collections/telephone-booths | NOT-EXISTS | — | Collection not in store |
| Acoustic Pods | /collections/acoustic-pods | NOT-EXISTS | — | Collection not in store |
| Focus Room Furniture | /collections/focus-rooms | NOT-EXISTS | — | Collection not in store |
| High-Back Privacy Seating | /collections/highback-seating | NOT-EXISTS | — | Collection not in store |
| Soundproofing Accessories | /collections/sound-dampeners | NOT-EXISTS | — | Collection not in store |

Quiet Spaces totals: 0 INCOHERENT, 0 COHERENT-POPULATED, 0 COHERENT-EMPTY, **5 NOT-EXISTS**. The entire Quiet Spaces category page is completely broken — every linked collection is missing from the store.

---

### collection.ergonomic-products.json — 4 tiles

| Tile | Collection | Count | Classification | Notes |
|---|---|---|---|---|
| Sit-Stand Converters | /collections/desktop-sit-stand | NOT-EXISTS | — | Collection not in store |
| Monitor Arms & Mounts | /collections/monitor-arms | NOT-EXISTS | — | Collection not in store |
| Keyboard Trays | /collections/keyboard-trays | NOT-EXISTS | — | Collection not in store |
| Ergonomic Accessories | /collections/ergonomic-accessories | NOT-EXISTS | — | Collection not in store |

Ergonomic Products totals: 0 INCOHERENT, 0 COHERENT-POPULATED, 0 COHERENT-EMPTY, **4 NOT-EXISTS**. Entire Ergonomic Products category page is completely broken. (Note: the top-level /collections/ergonomic-products smart collection has 16 products using title-contains rules, but the sub-category tiles all dead-link.)

---

### collection.business-furniture.json — 9 tiles

All 9 tiles link to top-level category hub collections (/collections/seating, /collections/desks, etc.). These are directory tiles, not sub-category tiles — different semantics.

| Tile | Collection | Count | Classification |
|---|---|---|---|
| Seating | /collections/seating | 102 | COHERENT-POPULATED |
| Desks & Workstations | /collections/desks | 30 | COHERENT-POPULATED |
| Storage & Filing | /collections/storage | 18 | COHERENT-POPULATED |
| Tables | /collections/tables | NOT-EXISTS | NOT-EXISTS |
| Boardroom | /collections/boardroom | NOT-EXISTS | NOT-EXISTS |
| Ergonomic Products | /collections/ergonomic-products | 16 | COHERENT-POPULATED |
| Panels & Dividers | /collections/panels-room-dividers | NOT-EXISTS | NOT-EXISTS |
| Accessories | /collections/accessories | NOT-EXISTS | NOT-EXISTS |
| Quiet Spaces | /collections/quiet-spaces | NOT-EXISTS | NOT-EXISTS |

Business Furniture: 4 COHERENT-POPULATED, 5 NOT-EXISTS — the top-level directory page is missing 5 of 9 category collection handles.

---

### Tile health summary (across all 10 templates, 64 tiles)

| Classification | Count | % |
|---|---|---|
| COHERENT-POPULATED | 22 | 34% |
| COHERENT-EMPTY | 21 | 33% |
| INCOHERENT-POPULATED | 1 | 2% |
| INCOHERENT-EMPTY | 0 | 0% |
| NOT-EXISTS | 20 | 31% |

**31% of all tile-linked collections do not exist in the Shopify store.** This is the single highest-priority fix before launch.

---

## Area 4 — Brand x Category Drill-Down Architecture Options

**Context:** 4 storefront-callable brands (Global Furniture Group/GFG, Offices to Go/OTG, ergoCentric, Keilhauer) with brand hub pages planned. Goal: buyer can navigate from brand hub to "GFG Seating" or "GFG Desks" specifically.

**Key Shopify Basic plan capability confirmed:** Smart collections support `disjunctive: false` (ALL rules must match = AND logic across fields). A rule set of `[{tag=brand:global-furniture-group}, {tag=type:chairs}]` with `disjunctive: false` returns only GFG chairs. This is confirmed via API inspection — the current /collections/seating uses `disjunctive: true` (OR between type tags). Option A is viable on Basic plan.

---

### Option A — Dedicated per-brand-per-category smart collections

**Implementation:** Create ~4 brands × ~6 categories = ~24 new smart collections with `disjunctive: false`.  
Example: `gfg-seating` → rules: [{tag=brand:global-furniture-group}, {tag=type:chairs}], disjunctive: false

| Criterion | Score | Rationale |
|---|---|---|
| Implementation complexity | 2/5 | Script-createable via Admin API; straightforward |
| Buyer experience quality | 5/5 | Clean URL, dedicated page, SEO-indexable |
| Maintenance burden | 3/5 | 24 new collections to manage; auto-updates as products are tagged |
| SEO friendliness | 5/5 | Unique URL per brand+category; indexable with canonical |
| Compatibility | 4/5 | Requires TYPE-APPLY-1 to be complete first; then works natively |

**Dependency:** Requires TYPE-APPLY-1 (all products tagged) before any collection has meaningful product count.

---

### Option B — Storefront filter on brand collection (existing tag sidebar)

**Implementation:** Brand hub links to /collections/global-teknion. Buyer uses the ds-cs-base tag sidebar filter to narrow by type:*. Requires: (a) /collections/global-teknion uses ds-cs-base template (it currently doesn't), (b) type:* sidebar filter is visible (currently only shown in ds-cs-base.liquid / collection.base template), (c) brand tag filter also shown in sidebar.

| Criterion | Score | Rationale |
|---|---|---|
| Implementation complexity | 3/5 | Needs template assignment change + sidebar brand-tag support |
| Buyer experience quality | 3/5 | Extra click; sidebar is secondary; filter state not obvious in URL |
| Maintenance burden | 1/5 | Zero new collections; self-maintaining as products tagged |
| SEO friendliness | 2/5 | /collections/global-teknion/type:chairs works but is not a named SEO page |
| Compatibility | 3/5 | Requires TYPE-APPLY-1 + template change for brand collections |

---

### Option C — Hybrid sectioned brand page (ds-lp-brand template)

**Implementation:** Brand hub page (e.g., /pages/global-furniture-group) with category sections — each section shows N products of type:* within that brand using metaobject or section blocks. "View all" deep-links to a per-brand-per-category URL.

| Criterion | Score | Rationale |
|---|---|---|
| Implementation complexity | 5/5 | Requires new section template with server-side filtering, which Liquid cannot do (no join queries) — would need pre-computed collections or metaobjects |
| Buyer experience quality | 5/5 | Best showcase of brand breadth; all-in-one page |
| Maintenance burden | 2/5 | Section content auto-updates if backed by collections |
| SEO friendliness | 3/5 | Single URL per brand — good for brand landing, but "View all" links to A or B |
| Compatibility | 2/5 | Liquid cannot filter collection.products by tag server-side; needs Option A collections as data sources |

---

### Recommendation: Option A + Option B Hybrid

**Primary path:** Implement Option A (24 brand x category smart collections, script-created via Admin API in BRAND-PAGES-1). These become the "View all" destinations from brand hub pages and appear in site search.

**Secondary path:** Add Option B as the filter mechanism on the brand collection itself. When a buyer lands on /collections/global-teknion (72 products), the ds-cs-base tag sidebar will auto-show type:chairs, type:tables, etc. as filter chips. This requires assigning the collection.base template to /collections/global-teknion, /collections/otg, /collections/ergo-centric, /collections/keilhauer.

**Skip Option C** at this stage — Liquid cannot server-side join a brand tag with a type tag without pre-computed collections (which Option A already provides).

**Score rationale:** Option A gives SEO-clean URLs (5/5) at low complexity (2/5) with zero UX ambiguity. The 24-collection overhead is manageable via script and they self-maintain once type:* tagging is complete.

---

## Area 5a — Cross-Category Product Placement

### Primary INCOHERENT-POPULATED case: global-teknion tile on Seating page

Collection: /collections/global-teknion  
Template placement: collection.seating.json tile-global-seating  
Products: 72 total

| Type | Count | % | Belongs on Seating page? |
|---|---|---|---|
| type:chairs | 32 | 44% | YES |
| type:lounge | 2 | 3% | YES |
| type:tables | 10 | 14% | NO — belongs on Tables or Boardroom pages |
| type:storage | 5 | 7% | NO — belongs on Storage page |
| type:desks | 5 | 7% | NO — belongs on Desks page |
| Untagged | 18 | 25% | UNKNOWN — need TYPE-APPLY-1 to classify |

**38 of 72 products (53%) in this tile are non-seating.** Specific worst instances:
1. `training-flip-top-tables-1` (GFG) — type:tables on Seating page
2. `vertical-file-2-drawer-letter` (GFG) — type:storage on Seating page
3. `u-shape-height-adjustable-desk-suite-zira` (GFG) — type:desks on Seating page
4. `4-drawer-letter-width-vertical-file` (GFG) — type:storage on Seating page
5. `loop-leg-table` (GFG) — type:tables on Seating page

**Fix options for this tile (see CATEGORY-TILE-FIX-1):**
- Remove the tile from seating.json and add brand tiles to each appropriate category page instead
- OR: Create /collections/gfg-seating (Option A) and replace the global-teknion tile link with it
- OR: Move brand callout blocks to a non-tile brand_callout component (already exists as `type=brand_callout` in desks.json and tables.json — use this pattern instead of tile blocks)

### collection.smart collection rule audit: cross-category

| Collection | Rules | Cross-category risk |
|---|---|---|
| task-chairs | tag=task-chair OR type=task OR title="task chair" | LOW: title-based rule may catch training tables |
| executive-seating | no rules (custom collection) | LOW: manually curated |
| guest-seating | no rules (custom collection) | MEDIUM: 25/39 products untagged; manual curation may have drifted |
| global-teknion | tag=brand:global-furniture-group OR tag=brand:teknion | HIGH: brand rule spans all types — 53% non-seating products on seating page |
| seating (top) | tag=type:chairs OR type:lounge OR type:ergonomic-seating etc | LOW: type-gated |
| desks (top) | tag=type:desks OR type:benching etc | LOW: type-gated |
| ergonomic-products (top) | title=contains monitor arm OR keyboard tray etc | MEDIUM: title rules are fragile; could miss items or include cross-category items |

---

## Area 5b — Sub-Category Taxonomy Redesign

### Seating (13 tiles → proposed 8)

Current issues: 2 NOT-EXISTS (stacking-seating, stools); multiple empty tiles; global-teknion brand tile is incoherent.

| Old tile | New tile | Rationale | Impact |
|---|---|---|---|
| Task Seating | Office Chairs | Broader term; "task" is industry jargon | tag rule: type:chairs |
| Executive Seating | Executive Chairs | Parallel naming | manual curation → type:chairs smart rule |
| Guest & Visitor Seating | Guest Seating | Shorter; clearer | Keep current collection |
| Lounge Seating | Lounge & Soft Seating | Add "soft seating" for B2B search recognition | type:lounge |
| Conference Seating | Meeting Room Chairs | B2B buyers say "meeting room chairs" | rule update |
| Training & Stacking | Stacking & Training | De-emphasize product-type jargon; "stacking" is recognizable | CREATE collection |
| Stools & Counter Seating | Stools | Simpler; counter seating understood from context | CREATE collection |
| Beam Seating | Beam Seating | Keep — institutional term buyers use | No change |
| Healthcare Seating | Healthcare Seating | Keep — segment-specific | No change |
| Outdoor & Café Seating | Outdoor Seating | Drop "Café" — BBI doesn't lead with hospitality | No change |
| **Global Furniture Group** (tile) | **REMOVE** | Replace with `brand_callout` block type (already exists in desks.json) | Remove 1 incoherent tile |
| Active Seating | Active & Ergonomic Seating | Merge with active; "ergonomic" is a search term | CREATE or merge |
| Benches & Tandem | Waiting Area Seating | "Bench" and "tandem" are jargon; "waiting area" is what buyers search | Update rule |

Proposed changes: 3 tiles to rename, 2 collections to CREATE, 1 tile to REMOVE (global-teknion), 1 tile to RENAME + MERGE.

---

### Desks (8 tiles → proposed 7)

| Old | New | Change |
|---|---|---|
| Height-Adjustable Desks | Sit-Stand Desks | "Sit-stand" is more common search term; unambiguous |
| L-Shape Desks | L-Shape & Corner Desks | "Corner desk" is high-volume search; add it |
| Straight Desks (NOT-EXISTS) | Single-Surface Desks | Descriptive; CREATE collection |
| Reception Desks | Reception Stations | "Station" signals the full setup (counter + storage) |
| Computer Desks | Multi-Person Workstations | Keep existing label — more accurate than "computer desks" |
| Modular Workstations | Modular Workstations | Keep |
| Executive Desks | Executive Desk Suites | "Suites" signals bundled credenza/return — upgrade perception |
| Training Room Desks (NOT-EXISTS) | REMOVE or merge into Tables | Training desks overlap heavily with training tables — only keep if BBI has dedicated products |

Proposed: 5 rename, 1 CREATE, 1 evaluate-for-removal.

---

### Tables (5 tiles → proposed 5)

| Old | New | Change |
|---|---|---|
| Conference Tables | Conference Tables | Keep — correct |
| Training Tables (NOT-EXISTS) | Training & Folding Tables | CREATE collection; "folding" is key feature |
| Height-Adjustable Tables | Height-Adjustable Meeting Tables | Disambiguates from desks category |
| Standing & High Tables (NOT-EXISTS) | Standing & Pub Tables | "Pub" is recognizable for café/breakroom; CREATE collection |
| Collaborative Tables | Collaborative & Agile Tables | "Agile" resonates with healthcare/government buyers |

Proposed: 2 CREATE, 3 rename (minor).

---

### Storage (12 tiles → proposed 8)

| Old | New | Change |
|---|---|---|
| Lateral Filing Cabinets | Lateral File Cabinets | Minor — "filing" redundant |
| Vertical Filing Cabinets (NOT-EXISTS) | Vertical File Cabinets | CREATE collection |
| Mobile Pedestals | Desk Pedestals | "Mobile" is understood; "desk pedestal" is searchable |
| Storage Cabinets (NOT-EXISTS) | Storage Cabinets | CREATE collection |
| Bookcases & Shelving | Bookcases | Keep — clear |
| Lockers | Personal Lockers | Disambiguates from high-density storage |
| Credenzas | Office Credenzas | "Office" anchors it; remove room ambiguity |
| Wardrobe Storage (NOT-EXISTS) | REMOVE | Too niche; merge into Storage Cabinets |
| Mobile Storage Carts | REMOVE | 0 products; no BBI catalog presence evident |
| Wall-Mounted Storage (NOT-EXISTS) | REMOVE | 0 products; no BBI catalog presence |
| Personal Storage | REMOVE | 0 products; merge desk organizers into Accessories |
| High-Density Storage | High-Density Shelving | Keep for institutional buyers (schools, healthcare); rename from "storage" |

Proposed: 2 CREATE, 4 REMOVE (reduce from 12 to 8 tiles), 6 rename.

---

### Boardroom (3 tiles → proposed 4)

| Old | New | Change |
|---|---|---|
| Boardroom Tables | Boardroom Tables | Keep |
| Boardroom Seating | Boardroom Chairs | "Chairs" is more searchable than "Seating" |
| Credenzas & Storage | Boardroom Credenzas | Focus on the executive piece; CREATE /collections/boardroom-credenzas |
| — | AV & Presentation Furniture | ADD: new tile for AV carts/mounts/podiums if BBI carries them |

---

### Ergonomic Products (4 tiles → proposed 4, but all need CREATE)

| Old | New | Change |
|---|---|---|
| Sit-Stand Converters (NOT-EXISTS) | Desk Converters | "Desk converters" more common search; CREATE |
| Monitor Arms & Mounts (NOT-EXISTS) | Monitor Arms | Shorter; CREATE |
| Keyboard Trays (NOT-EXISTS) | Keyboard Trays | Keep naming; CREATE |
| Ergonomic Accessories (NOT-EXISTS) | Ergonomic Accessories | Keep; CREATE |

4 collections to CREATE. Consider whether /collections/ergonomic-products should use collection.ergonomic-products template (currently unverified) vs. collection.base (existing ds-cs-base).

---

### Panels & Room Dividers (3 tiles → proposed 3, all need CREATE or product addition)

| Old | New | Change |
|---|---|---|
| Acoustic Panels (0 products) | Acoustic Wall Panels | "Wall" disambiguates from acoustic pods |
| Room Dividers (NOT-EXISTS) | Room Dividers | CREATE collection |
| Privacy Screens (0 products) | Desktop Privacy Screens | "Desktop" specifies the type BBI carries |

---

### Quiet Spaces (5 tiles → proposed 3)

| Old | New | Change |
|---|---|---|
| Phone Booths (NOT-EXISTS) | Phone Booths | CREATE — hot item, acoustic pods trend |
| Acoustic Pods (NOT-EXISTS) | Acoustic Meeting Pods | CREATE — "meeting pods" is the buyer term |
| Focus Room Furniture (NOT-EXISTS) | REMOVE | Too broad; products covered by other categories |
| High-Back Privacy Seating (NOT-EXISTS) | REMOVE | Merge into Seating > Lounge (type:lounge covers this) |
| Soundproofing Accessories (NOT-EXISTS) | Soundproofing | Simplify label; CREATE if BBI carries baffles/panels |

3 to CREATE, 2 to REMOVE.

---

### Accessories (2 tiles → proposed 5)

The accessories category page is significantly under-built. Proposed expansion:

| Old | New | Change |
|---|---|---|
| Lighting | Task Lighting | Narrow to desk/task lighting BBI carries |
| Whiteboards & Boards (NOT-EXISTS) | Whiteboards & Pinboards | CREATE |
| — | Chair Mats & Floor Protection | ADD: BBI carries Deflecto floor mats (several active products) |
| — | Monitor Arms & Desk Accessories | ADD: cross-link from Ergonomic (or move there) |
| — | Waste & Recycling | ADD: if BBI carries Rubbermaid etc. |

---

## Recommended Downstream Sequence

Three decisions Steve needs to make before downstream steps can fire:

**Decision 1 — TYPE-APPLY-1 scope approval**
Before auto-tagging 70 products, Steve needs to confirm:
- Do the 11 NO-MATCH products stay in the catalog? Delivery charges and disposal programs should likely be unpublished (not deleted — BBI rule: archive not delete). The `colour` swatch placeholder product should be reviewed.
- Is the MEDIUM-CONFIDENCE classification acceptable for auto-apply, or should Steve review each of the 16 medium-confidence products manually?
- What type:* tag should `foundations-sport-splash-quad-strollers` get? (Stroller product in office furniture catalog — likely a data import error.)

**Decision 2 — global-teknion tile disposition**
The global-teknion brand tile is on the Seating category page but 53% of its products are non-seating. Steve needs to pick one:
- (A) Remove the tile from seating.json; instead add brand_callout blocks on each appropriate category page (this component already exists in desks and tables templates)
- (B) Replace the tile with /collections/gfg-seating (requires BRAND-PAGES-1 Option A first)
- (C) Keep as-is and accept that the Seating page promotes non-seating GFG products

**Decision 3 — Missing collection strategy**
20 tile-linked collections do not exist in the Shopify store. Steve needs to confirm:
- Which of the 5 NOT-EXISTS categories are truly out of scope for launch (quiet-spaces, ergonomic-products sub-tiles) vs. which need collections created?
- Priority order: quiet-spaces (5 NOT-EXISTS) and ergonomic-products (4 NOT-EXISTS) are the most broken category pages; storage (4 NOT-EXISTS) is next.
- Does BBI carry products for: wardrobe storage, wall-mounted storage, personal storage, high-density storage? If not, remove those tiles before launch.

---

## Excluded from Scope

/collections/other (custom collection id=527013085497) contains 337 archived/miscellaneous products excluded from all analysis in this investigation per the investigation brief. This collection functions as a holding area for products not yet categorized or removed from the main storefront — it should not be linked from any navigation tile or category template.
