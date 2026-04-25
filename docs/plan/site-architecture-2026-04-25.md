# BBI Site Architecture & Page Build Plan
**Store:** [brantbusinessinteriors.com](https://www.brantbusinessinteriors.com)
**Date:** 2026-04-25
**Status:** Approved by Steve · Ready to build

> **Scope change — April 25, 2026:** The shop is narrowed to **Business Furniture only.** The Educational, Daycare & ECE, and Healthcare & Seniors vertical pages have been removed and their products archived in Shopify. The Shop Hub page (`/pages/shop`) is also removed — "Shop Furniture" in the nav now links directly to `/collections/business-furniture`. The Industries section (Healthcare, Education, Government, Non-Profit, Professional Services) remains, with copy refocused on furnishing *workspaces within those sectors* using business furniture (e.g., reception desks for a hospital, admin chairs for a school board). Page count updated from ~148 to ~102. Active templates reduced from 4 to 3 (`page.shop-hub.json` no longer needed).

This document defines every page to build, the nav bar structure, the template strategy, and how all pages interconnect. Use this as the master reference when building or modifying any page on the site.

---

## 1. Nav Bar Structure

**5 top-level items** + phone number + Quote CTA (right-aligned).

```
[Office Central Logo]  |  Shop Furniture ▾  |  Industries ▾  |  Brands ▾  |  Services ▾  |  About ▾  |  1-800-835-9565  |  [Request Quote →]
```

### Hover behaviour (mega menus / dropdowns)

**Shop Furniture** → 4-column mega menu:

| 🪑 Business Furniture | 🎓 Educational | 👶 Daycare & ECE | 🏥 Healthcare & Seniors |
|---|---|---|---|
| Seating | Student Chairs | Kids Play Tables | Waiting Room Seating |
| Desks & Workstations | Tablet Chairs | Classroom Storage | Bariatric Seating |
| Storage & Filing | Lecture Hall Seating | Arts & Crafts | Recliners |
| Tables | Student Desks | Manipulative Play | Exam Room Seating |
| Boardroom | Library Study Tables | Dramatic Play | Bedside & Overbed Tables |
| Ergonomic Products | Library Shelving | Coat Cubbies & Lockers | Beds & Mattresses |
| Panels & Dividers | Lab Furniture | Book Display & Storage | Clinician Screens |
| Accessories | Charging Units | Kids Chairs & Couches | Diagnostic Carts/Arms |
| Quiet Spaces | Book Carts | Mirrors & Room Dividers | + 10 more → |
| | + 4 more → | | |

Column headers link to the vertical page. Each item below links directly to the sub-collection.

**Industries** → simple dropdown: Healthcare · Education · Government · Non-Profit · Professional Services

**Brands** → simple dropdown: Keilhauer · Global/Teknion · ergoCentric

**Services** → simple dropdown: Design Services · Delivery & Installation · Relocation Management · OECM Procurement

**About** → simple dropdown: Our Work · About Us · Contact · Request a Quote

### Click behaviour
- **Clicking** "Shop Furniture" → navigates to `/pages/shop` (the Shop Hub page showing 4 vertical tiles)
- **Hovering** "Shop Furniture" → opens the mega menu for quick deep-linking
- All other top-level items: click opens their dropdown

### Mobile nav
Hamburger → vertical accordion with identical 5-item structure.

---

## 2. Page Inventory & Shop Journey

### 2a. The Shop — 4-Level Hierarchy

The shop is structured as a 4-level journey for Business Furniture, and a 3-level journey for Educational, Daycare, and Healthcare.

```
Level 0 → Level 1        → Level 2               → Level 3             → Products
Shop Hub   Vertical page   Category page           Sub-collection
/pages/shop  (4 options)    (Biz Furn. only)        product listing
```

**Templates at each level:**

| Level | Page type | Template | Description |
|---|---|---|---|
| 0 | Shop Hub | `page.shop-hub.json` | 4 vertical tiles |
| 1 | Vertical page | `collection.category.json` | Sub-category tile grid |
| 2 | Category page (Biz Furn.) | `collection.category.json` | Sub-collection tile grid |
| 3 | Sub-collection | `collection.json` | Product listing with filters |
| — | Product | `product.json` | Individual product detail |

> ★ Educational, Daycare, and Healthcare skip Level 2 — their vertical page goes directly to sub-collections (3 levels total). Business Furniture needs the extra level because it has 9 categories, each with 3–16 sub-collections.

---

### 2b. Shop Hub

| Page | URL | Template | Status |
|---|---|---|---|
| Shop Hub | `/pages/shop` | `page.shop-hub.json` | Build needed |

Shows 4 large tiles: Business Furniture · Educational · Daycare & ECE · Healthcare & Seniors. Each tile has: image, vertical name, short descriptor, CTA link.

---

### 2c. Business Furniture — Vertical + 9 Categories + ~68 Sub-collections

**Vertical page:**

| Page | URL | Template |
|---|---|---|
| Business Furniture | `/collections/business-furniture` | `collection.category.json` |

Shows 9 category tiles (Seating, Desks, Storage, Tables, Boardroom, Ergonomics, Panels, Accessories, Quiet Spaces).

**Category pages (tile grid of sub-types — no products):**

| Category | URL | Sub-collections |
|---|---|---|
| Seating | `/collections/seating` | 16 |
| Desks & Workstations | `/collections/desks` | 9 |
| Storage & Filing | `/collections/storage` | 14 |
| Tables | `/collections/tables` | 10 |
| Boardroom | `/collections/boardroom` | 3 |
| Ergonomic Products | `/collections/ergonomic-products` | 4 |
| Panels & Dividers | `/collections/panels-room-dividers` | 3 |
| Accessories | `/collections/accessories` | 4 |
| Quiet Spaces | `/collections/quiet-spaces` | 5 |

All use `collection.category.json` template. No products shown — clicking a tile drops into the sub-collection.

**Seating sub-collections** (`collection.json` template):
`/collections/highback-seating` · `/collections/medium-back-seating` · `/collections/mesh-seating` · `/collections/leather-faux-seating` · `/collections/stools-seating` · `/collections/lounge-chairs-seating` · `/collections/ottomans` · `/collections/guest-seating` · `/collections/stacking-seating` · `/collections/folding-stacking-chairs-carts` · `/collections/nesting-chairs-chair` · `/collections/24-hour-seating` · `/collections/big-heavy-seating` · `/collections/cluster-seating` · `/collections/industrial-seating` · `/collections/gaming`

**Desks & Workstations sub-collections** (`collection.json` template):
`/collections/u-shape-desks-desks` · `/collections/l-shape-desks-desks` · `/collections/height-adjustable-tables-desks` · `/collections/multi-person-workstations-desks` · `/collections/benching-desks` · `/collections/table-desks` · `/collections/straight-desks-desks` · `/collections/reception` · `/collections/office-suites-desks`

**Storage & Filing sub-collections** (`collection.json` template):
`/collections/lateral-files-storage` · `/collections/vertical-files` · `/collections/storage-cabinets-storage` · `/collections/bookcases-storage` · `/collections/hutch` · `/collections/lateral-storage-combo-storage` · `/collections/end-tab-filing-storage` · `/collections/pedestal-drawers-storage` · `/collections/fire-resistant-safes-storage` · `/collections/metal-shelving` · `/collections/lockers` · `/collections/fire-resistant-file-cabinets-storage` · `/collections/wardrobe-storage` · `/collections/credenzas`

**Tables sub-collections** (`collection.json` template):
`/collections/meeting-tables` · `/collections/coffee-tables` · `/collections/training-flip-top-tables` · `/collections/end-tables-tables` · `/collections/drafting-tables` · `/collections/round-square-tables` · `/collections/cafeteria-kitchen-tables` · `/collections/bar-height-tables` · `/collections/folding-tables-tables` · `/collections/table-bases`

**Boardroom sub-collections** (`collection.json` template):
`/collections/boardroom-conference-meeting` · `/collections/lecterns-podiums` · `/collections/audio-visual-equipment`

**Ergonomic Products sub-collections** (`collection.json` template):
`/collections/height-adjustable-tables` · `/collections/monitor-arms` · `/collections/keyboard-trays` · `/collections/desktop-sit-stand`

**Panels & Dividers sub-collections** (`collection.json` template):
`/collections/room-dividers-panels-dividers` · `/collections/desk-top-dividers` · `/collections/modesty-panels`

**Accessories sub-collections** (`collection.json` template):
`/collections/chairmats-accessories` · `/collections/power-modules-accessories` · `/collections/coat-racks-accessories` · `/collections/lighting`

**Quiet Spaces sub-collections** (`collection.json` template):
`/collections/telephone-booths` · `/collections/walls` · `/collections/sound-dampeners` · `/collections/av-stand` · `/collections/planters`

---

### 2d. Educational Furniture — Vertical + 13 Sub-collections

| Page | URL | Template |
|---|---|---|
| Educational Furniture | `/collections/educational` | `collection.category.json` |

Sub-collections (direct — no category tier):
`/collections/student-chairs` · `/collections/office-teachers-chairs` · `/collections/tablet-chairs` · `/collections/lecture-hall-seating` · `/collections/cafe-lounge-seating` · `/collections/student-desks` · `/collections/reception-desks-desks` · `/collections/library-study-tables` · `/collections/library-shelving` · `/collections/laboratory-furniture` · `/collections/charging-units` · `/collections/book-carts` · `/collections/dorm-penitentiary-furniture`

---

### 2e. Daycare & Early Childhood Education — Vertical + ~11 Categories

| Page | URL | Template |
|---|---|---|
| Daycare & ECE | `/collections/daycare` | `collection.category.json` |

Sub-collections (direct — no category tier):
`/collections/kids-play-tables` · `/collections/classroom-storage` · `/collections/manipulative-play` · `/collections/dramatic-play` · `/collections/coat-cubbies-lockers` · `/collections/book-displays-storage` · `/collections/cribs` · `/collections/strollers` · `/collections/kids-chairs` · `/collections/mirrors-room-dividers`

---

### 2f. Healthcare & Seniors — Vertical + 18 Sub-collections

| Page | URL | Template |
|---|---|---|
| Healthcare & Seniors | `/collections/healthcare` | `collection.category.json` |

Sub-collections (direct — no category tier):
`/collections/waiting-room-seating` · `/collections/bariatric-seating` · `/collections/recliners` · `/collections/exam-room-seating` · `/collections/lounge-seating` · `/collections/dinning-seating` · `/collections/dinning-tables` · `/collections/occasional-tables` · `/collections/bedside-tables` · `/collections/overbed-tables` · `/collections/beds-matresses` · `/collections/dressers` · `/collections/wardrobes` · `/collections/tv-units` · `/collections/clinician-screens` · `/collections/diagnostic-carts-arms` · `/collections/outdoor-seating` · `/collections/dining-room`

---

### 2g. Industries — Landing Pages

All use the same landing page template. Format: hero image · intro copy · featured products · testimonials/project photos · cross-link to relevant shop vertical · CTA.

| Page | URL | Priority |
|---|---|---|
| Industries Hub | `/pages/industries` | — |
| Healthcare | `/pages/healthcare` | ⭐ |
| Education | `/pages/education` | ⭐ |
| Government | `/pages/government` | — |
| Non-Profit | `/pages/non-profit` | — |
| Professional Services | `/pages/professional-services` | — |

---

### 2h. Brands — Landing Pages

All use the same landing page template (same structure as industry pages).

| Page | URL |
|---|---|
| Brands Hub | `/pages/brands` |
| Keilhauer | `/pages/brands-keilhauer` |
| Global / Teknion | `/pages/brands-global-teknion` |
| ergoCentric | `/pages/brands-ergocentric` |

---

### 2i. Services — Landing Pages

All use the same landing page template.

| Page | URL | Priority |
|---|---|---|
| Design Services | `/pages/design-services` | ⭐ |
| Delivery & Installation | `/pages/delivery` | — |
| Relocation Management | `/pages/relocation` | — |
| OECM Procurement | `/pages/oecm` | ⭐ |

---

### 2j. About & Trust

| Page | URL | Priority |
|---|---|---|
| Homepage | `/` | ⭐ |
| Our Work & Portfolio | `/pages/our-work` | — |
| About Us | `/pages/about` | — |
| Contact | `/pages/contact` | — |
| Request a Quote | `/pages/quote` | ⭐ |

---

### 2k. System Pages (Shopify auto-generated — template work only)

| Page | URL |
|---|---|
| Product detail pages (645 SKUs) | `/products/[handle]` |
| Cart | `/cart` |
| Search | `/search` |
| Account / Login | `/account` |
| Policies | `/policies/*` |

---

## 3. Templates to Build

Only **4 templates** need to be built. Everything else is a content/data task.

| Template | Used by | Key sections |
|---|---|---|
| `page.shop-hub.json` | Shop Hub page | Hero · 4 vertical tiles with image, name, blurb, CTA |
| `collection.category.json` | All vertical pages + all Business Furniture category pages (13 total) | Hero · tile grid (section blocks) · breadcrumbs · no product grid |
| `collection.json` | All ~110 sub-collection pages | Hero banner · breadcrumbs · filter sidebar · product grid · phone CTA block |
| Landing page template | All industry, brand, service, and about pages (~19 pages) | Hero · intro · featured cards (3–4) · testimonial/photo block · cross-links · CTA |

> The `collection.category.json` template renders tiles using section **blocks** (not metafields), so each tile's image, label, blurb, and link are configurable from the Shopify Theme Editor without code changes.

---

## 4. Page Interconnection Rules

These rules must be applied when building or editing any page. They define how every page cross-links to related pages.

### Rule 1: Sub-collection pages always show breadcrumbs
Breadcrumb trail on every sub-collection page: `Home > Shop Furniture > [Vertical] > [Category] > [Sub-collection]`
Breadcrumbs are already live (BreadcrumbList JSON-LD included). Confirm they reflect the new 4-level hierarchy.

### Rule 2: Category pages link back up and across
Every `collection.category.json` page must include:
- Breadcrumb back to the vertical page
- A "See all [Vertical] furniture →" link at the bottom
- A "Can't find it? Call 1-800-835-9565" CTA

### Rule 3: Industry landing pages cross-link to their shop vertical
Every industry landing page must include:
- "Shop [Industry] Furniture →" button linking to the corresponding shop vertical or sub-collections
- Example: `/pages/healthcare` links to `/collections/healthcare` and highlights: Waiting Room Seating, Bariatric Seating, Recliners, Exam Room Seating

Mapping:

| Industry page | Links to shop |
|---|---|
| `/pages/healthcare` | `/collections/healthcare` + highlight waiting room, bariatric, exam room |
| `/pages/education` | `/collections/educational` + `/collections/daycare` |
| `/pages/government` | `/collections/business-furniture` + highlight desks, storage, panels |
| `/pages/non-profit` | `/collections/business-furniture` + highlight seating, tables |
| `/pages/professional-services` | `/collections/desks` + `/collections/seating` + ergonomics |

### Rule 4: Shop vertical pages cross-link to their industry landing page
Every vertical page (`collection.category.json`) should include a contextual module:

| Shop vertical | Cross-links to |
|---|---|
| `/collections/healthcare` | `/pages/healthcare` |
| `/collections/educational` | `/pages/education` |
| `/collections/daycare` | `/pages/education` |
| `/collections/business-furniture` | `/pages/industries` (hub) |

### Rule 5: Every sub-collection page has a phone CTA block
At the bottom of every sub-collection (product listing) page: `"Can't find exactly what you need? Our team can help. Call 1-800-835-9565"` with a secondary "Request a Quote →" button linking to `/pages/quote`.

### Rule 6: Homepage surfaces all 4 verticals + key conversion paths
Homepage sections (in order):
1. Hero — headline, CTA to Shop or Request Quote
2. 4 vertical tiles (Business · Educational · Daycare · Healthcare)
3. Featured products (3 Hero 100 items)
4. OECM trust bar — "Verified OECM supplier. Ontario institutions can purchase without open tender."
5. Industries we serve (5 sector thumbnails → industry landing pages)
6. Services overview (Design Services · Delivery · Relocation)
7. Testimonials / Our Work preview
8. Footer with full nav + phone + quote CTA

### Rule 7: Brand pages link to relevant products
Each brand page (`/pages/brands-keilhauer`, etc.) must include:
- A "Shop [Brand] products →" link to a filtered collection or search
- Featured 3–4 products from that brand

---

## 5. Build Priority Order

### Phase 1 — Conversion & SEO pages (build first)
These pages are what institutional buyers search for and what drives leads.

1. ✅ Homepage (`/`) — hero, verticals, OECM trust bar, testimonials
2. OECM page (`/pages/oecm`) — key differentiator for Ontario institutional buyers
3. Design Services (`/pages/design-services`) — free layout offer, high conversion
4. Request a Quote (`/pages/quote`) — cross-linked from everywhere
5. Industries Hub (`/pages/industries`) + 5 industry landing pages

### Phase 2 — Shop structure (unlocks the full product UX)
6. Shop Hub page (`/pages/shop`) — 4 vertical tiles
7. 4 vertical pages (Business Furniture, Educational, Daycare, Healthcare) — `collection.category.json`
8. 9 Business Furniture category pages (Seating, Desks, Storage…) — same template, different tile data

### Phase 3 — Collection template rollout (bulk apply)
9. Build the shared `collection.json` sub-collection template
10. Apply to all ~110 sub-collection pages
11. Assign hero images from `data/page-images/` per collection (AI-generated images already in backlog)

### Phase 4 — Remaining landing pages
12. Brands Hub + 3 brand pages
13. About Us, Our Work, Contact
14. Delivery & Installation, Relocation Management

---

## 6. Pre-Build Checklist

Before building any collection page, confirm the collection is populated in Shopify:

- [ ] Audit all sub-collections from the nav: verify product count > 0 for each
- [ ] Convert any empty or manually-curated collections to smart collections with appropriate rules (e.g. "title contains L-Shape" for `/collections/l-shape-desks-desks`)
- [ ] The 14 smart collections from Phase C are tag-based (`type:*`, `room:*`) — the sub-type collections (L-Shape, U-Shape, etc.) from the original nav may need to be audited and repopulated
- [ ] Set up Google Search Console + GA4 (W0-1, still open) before Phase 1 pages launch — zero SEO progress measurable without this

---

## 7. Page Count Summary

| Section | Pages | Template |
|---|---|---|
| Homepage | 1 | Custom |
| Shop Hub | 1 | `page.shop-hub.json` |
| Vertical pages (4) | 4 | `collection.category.json` |
| Business Furniture category pages (9) | 9 | `collection.category.json` |
| Sub-collection pages | ~110 | `collection.json` |
| Industry pages (hub + 5) | 6 | Landing page template |
| Brand pages (hub + 3) | 4 | Landing page template |
| Service pages | 4 | Landing page template |
| About & Trust pages | 4 | Landing page template |
| System pages (auto) | ~5 | Template work only |
| **Total** | **~148** | **4 templates** |

---

*Source: BBI site architecture session, 2026-04-25. Approved by Steve. Reference menu backup: `data/backups/main-menu-20260420-234056.json`.*
