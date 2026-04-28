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

**Shop Furniture** → single-column dropdown (Business Furniture only — scope change 2026-04-25):

| 🪑 Business Furniture |
|---|
| Seating |
| Desks & Workstations |
| Storage & Filing |
| Tables |
| Boardroom |
| Ergonomic Products |
| Panels & Dividers |
| Accessories |
| Quiet Spaces |

Header links to `/collections/business-furniture`. Each item links to the corresponding category page.

**Industries** → simple dropdown: Healthcare · Education · Government · Non-Profit · Professional Services

**Brands** → simple dropdown: Keilhauer · Global/Teknion · ergoCentric

**Services** → simple dropdown: Design Services · Delivery & Installation · Relocation Management · OECM Procurement

**About** → simple dropdown: Our Work · About Us · Contact · Request a Quote

### Click behaviour
- **Clicking** "Shop Furniture" → navigates to `/collections/business-furniture` (the Business Furniture vertical page — Shop Hub removed, scope change 2026-04-25)
- **Hovering** "Shop Furniture" → opens the dropdown for quick deep-linking to category pages
- All other top-level items: click opens their dropdown

### Mobile nav
Hamburger → vertical accordion with identical 5-item structure.

---

## 2. Page Inventory & Shop Journey

### 2a. The Shop — 3-Level Hierarchy (Business Furniture only)

The shop is structured as a 3-level journey. (Shop Hub removed — scope change 2026-04-25. Educational, Daycare, and Healthcare verticals archived.)

```
Level 1                   → Level 2               → Level 3             → Products
Vertical page                Category page           Sub-collection
/collections/business-      (9 categories)          product listing
furniture
```

**Templates at each level:**

| Level | Page type | Template | Description |
|---|---|---|---|
| 1 | Vertical page | `collection.category.json` | 9 category tiles — no products |
| 2 | Category page | `collection.category.json` | Sub-collection tiles — no products |
| 3 | Sub-collection | `collection.json` | Product listing with filters |
| — | Product | `product.json` | Individual product detail |

---

### 2b. Shop Hub — ~~Removed~~

> **Removed — scope change 2026-04-25.** The Shop Hub page (`/pages/shop`) and its template (`page.shop-hub.json`) are no longer needed. "Shop Furniture" in the nav links directly to `/collections/business-furniture`. Any existing `/pages/shop` URL should redirect to `/collections/business-furniture`.

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

### ~~2d. Educational Furniture~~ — Removed

> **Removed — scope change 2026-04-25.** Products archived in Shopify. The `/collections/educational` vertical and its 13 sub-collections are no longer part of the active shop. The `/pages/education` industry landing page remains (see 2g) but now links to relevant Business Furniture sub-collections rather than the educational vertical.

---

### ~~2e. Daycare & Early Childhood Education~~ — Removed

> **Removed — scope change 2026-04-25.** Products archived in Shopify. The `/collections/daycare` vertical and its ~11 sub-collections are no longer part of the active shop.

---

### ~~2f. Healthcare & Seniors~~ — Removed

> **Removed — scope change 2026-04-25.** Products archived in Shopify. The `/collections/healthcare` vertical and its 18 sub-collections are no longer part of the active shop. The `/pages/healthcare` industry landing page remains (see 2g) but now cross-links to relevant Business Furniture sub-collections (waiting room seating, reception desks, etc.).

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
| Customer Stories | `/pages/customer-stories` | ⭐ |
| About Us | `/pages/about` | — |
| Contact | `/pages/contact` | — |
| Request a Quote | `/pages/quote` | ⭐ |
| FAQ | `/pages/faq` | ⭐ |

FAQ covers: ordering & payment (PO, NET 30, credit accounts) · OECM ordering process · delivery & install · returns & warranty · design services. FAQ schema markup (JSON-LD) required for AI Overview readiness.

**Our Work vs Customer Stories** — both are social proof but serve different buyer modes:
- *Our Work* (`/pages/our-work`) — visual portfolio. Photo-heavy project cards (Mattamy-1 through Mattamy-5 from `data/oci-photos/`). Quick credibility scan.
- *Customer Stories* (`/pages/customer-stories`) — narrative case studies with industry filter chips. Each story: situation → solution → products used (linked) → outcome → client quote. Required JSON-LD: Review schema per testimonial. Cross-links into industry pages and product categories.

---

### 2k. Blog / Resources

| Page | URL | Template |
|---|---|---|
| Resources Hub | `/blogs/news` | Custom blog template |
| Articles | `/blogs/news/[handle]` | Article template |

Foundation for the SEO strategy 2026 (outcome-based search, AI Overview citations, Workspitality trend, niche keyword clusters). Content pillars: buying guides · industry insights · trends · procurement how-tos. Every article must include FAQ schema, link to a relevant collection, and a CTA to `/pages/quote`.

---

### 2l. Brand-Filtered Smart Collections

Each brand dealer page links to a vendor-filtered smart collection that lists every product from that brand as a flat list with filters. Required so brand pages don't dead-end.

| Brand page | Brand-filtered collection | Smart-collection rule |
|---|---|---|
| `/pages/brands-keilhauer` | `/collections/keilhauer` | vendor = "Keilhauer" |
| `/pages/brands-global-teknion` | `/collections/global` + `/collections/teknion` | vendor = "Global" / "Teknion" |
| `/pages/brands-ergocentric` | `/collections/ergocentric` | vendor = "ergoCentric" |

ObusForme also gets `/collections/obusforme` if traffic warrants. All use the standard `collection.json` template.

---

### 2m. System Pages (Shopify auto-generated — template work only)

| Page | URL | Notes |
|---|---|---|
| Product detail pages (645 SKUs) | `/products/[handle]` | Custom product template (see Phase 2 build plan) |
| Cart | `/cart` | Standard Shopify cart |
| Search | `/search` | Standard, but consider custom no-results page |
| Account / Login | `/account` | Standard |
| 404 Not Found | `/404` | **Custom** — replace Shopify default. Show search box + 4 top category tiles + phone CTA. Track 404 hits in GA4 to identify URLs needing 301 redirects. |
| Policies (Privacy, Returns, Shipping, Terms) | `/policies/*` | Auto-generated URLs; content must be filled in via Admin → Settings → Policies. PIPEDA/CASL compliance required. |

---

## 3. Templates to Build

**5 templates** to build. (`page.shop-hub.json` is no longer needed — scope change 2026-04-25.)

| Template | Used by | Key sections |
|---|---|---|
| `collection.category.json` | Business Furniture vertical + 9 category pages (10 total) | Hero · "View all [Category] →" button · tile grid (section blocks) · breadcrumbs · no product grid |
| `collection.json` | ~68 BF sub-collections + 9 "View all" smart collections + 4 brand-filtered smart collections (~81 total) | Hero banner · breadcrumbs · filter sidebar · product grid · phone CTA block |
| Landing page template | Industry, brand, service, about, FAQ pages (~20 pages) | Hero · intro · featured cards (3–4) · testimonial/photo block · cross-links · CTA. FAQ variant adds JSON-LD schema + accordion. |
| Blog template (`blog.json` + `article.json`) | Resources hub + articles | Hub: featured + latest + category filter + email capture. Article: H1 + TOC + sections + FAQ schema + related collection CTA. |
| `404.json` | Custom 404 page | Brief message + search box + 4 top category tiles + phone CTA + Quote button |

Plus the existing `product.json` (custom product detail template) which is in the Phase 2 build plan.

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
- **A "View all [Category] →" button** at the top of the tile grid linking to a tag-based smart collection (e.g. `/collections/all-desks`, `/collections/all-seating`) that shows every product in the category as a flat product list with filters. Lets buyers who want to browse everything skip the sub-type drilldown.

**Smart collections to create** (one per category, tag-based on `category:*`):
| Category page | "View all" smart collection |
|---|---|
| `/collections/seating` | `/collections/all-seating` |
| `/collections/desks` | `/collections/all-desks` |
| `/collections/storage` | `/collections/all-storage` |
| `/collections/tables` | `/collections/all-tables` |
| `/collections/boardroom` | `/collections/all-boardroom` |
| `/collections/ergonomic-products` | `/collections/all-ergonomic` |
| `/collections/panels-room-dividers` | `/collections/all-panels` |
| `/collections/accessories` | `/collections/all-accessories` |
| `/collections/quiet-spaces` | `/collections/all-quiet-spaces` |

The Business Furniture vertical page (`/collections/business-furniture`) gets a "View all Business Furniture →" link to `/collections/all` (Shopify auto-generated) or a dedicated smart collection `/collections/all-business-furniture` if more curation is needed.

### Rule 3: Industry landing pages cross-link to filtered Business Furniture sub-collections
Every industry landing page must include:
- "Shop [Industry] Furniture →" button linking to a curated set of Business Furniture sub-collections relevant to that industry (the verticals `/collections/healthcare`, `/collections/educational`, `/collections/daycare` no longer exist — scope change 2026-04-25)
- "See [Industry] customer stories →" link to `/pages/customer-stories#[industry-slug]` (filtered view)
- Example: `/pages/healthcare` highlights: Waiting Room Seating, Reception Desks, Recliners, Exam Room Seating — all linking to the corresponding Business Furniture sub-collections

Mapping:

| Industry page | Links to shop |
|---|---|
| `/pages/healthcare` | `/collections/business-furniture` + highlight `/collections/bariatric-seating`, `/collections/recliners`, `/collections/lounge-reception` (waiting room), `/collections/reception-desks`, `/collections/task-chairs`, `/collections/storage` |
| `/pages/education` | `/collections/business-furniture` + highlight `/collections/training-tables`, `/collections/stack-chairs`, `/collections/storage`, `/collections/panels-room-dividers` |
| `/pages/government` | `/collections/business-furniture` + highlight `/collections/desks`, `/collections/storage`, `/collections/panels-room-dividers` |
| `/pages/non-profit` | `/collections/business-furniture` + highlight `/collections/seating`, `/collections/tables` |
| `/pages/professional-services` | `/collections/desks` + `/collections/seating` + `/collections/ergonomics` |

> **Note:** Sub-collection slugs above are illustrative — confirm against the live taxonomy in section 2c before wiring links. If a needed sub-collection doesn't exist (e.g., dedicated waiting-room seating), either map to the closest parent category or flag for taxonomy follow-up.

### Rule 4: Business Furniture vertical cross-links to the Industries hub
The single shop vertical page (`/collections/business-furniture`) should include a contextual module linking to `/pages/industries` (hub) so buyers can pivot from product browsing into industry-specific solution stories. Per-industry sub-collection cross-links live on the industry landing pages (Rule 3), not on the shop vertical.

### Rule 5: Every sub-collection page has a phone CTA block
At the bottom of every sub-collection (product listing) page: `"Can't find exactly what you need? Our team can help. Call 1-800-835-9565"` with a secondary "Request a Quote →" button linking to `/pages/quote`.

### Rule 6: Homepage surfaces the shop entry + key conversion paths
Homepage sections (in order):
1. Hero — headline, CTA to Shop Furniture or Request Quote
2. Shop entry — link/banner to `/collections/business-furniture` with 3–4 featured category tiles (Seating, Desks, Storage, Boardroom)
3. Featured products (3 Hero 100 items)
4. OECM trust bar — "Verified OECM supplier. Ontario institutions can purchase without open tender."
5. Industries we serve (5 sector thumbnails → industry landing pages)
6. Services overview (Design Services · Delivery · Relocation)
7. Testimonials / Our Work preview / "Read customer stories →" link to `/pages/customer-stories`
8. Footer with full nav + phone + quote CTA

### Rule 7: Brand pages link to vendor-filtered collections
Each brand page (`/pages/brands-keilhauer`, etc.) must include:
- A primary "Shop [Brand] products →" button linking to the brand's vendor-filtered smart collection (see section 2l): `/collections/keilhauer`, `/collections/global`, `/collections/teknion`, `/collections/ergocentric`
- Featured 3–4 products from that brand
- Secondary cross-links to relevant category pages (e.g. Keilhauer → Seating + Boardroom)

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
6. Business Furniture vertical page (`/collections/business-furniture`) — 9 category tiles
7. 9 Business Furniture category pages (Seating, Desks, Storage, Tables, Boardroom, Ergonomics, Panels, Accessories, Quiet Spaces) — `collection.category.json`

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
| Business Furniture vertical | 1 | `collection.category.json` |
| Business Furniture category pages (9) | 9 | `collection.category.json` |
| Sub-collection pages | ~68 | `collection.json` |
| Industry pages (hub + 5) | 6 | Landing page template |
| Brand pages (hub + 3) | 4 | Landing page template |
| Brand-filtered smart collections (4) | 4 | `collection.json` |
| Service pages | 4 | Landing page template |
| About & Trust pages (incl. Request a Quote, FAQ, Customer Stories) | 7 | Landing page template |
| Blog Resources (hub + articles) | 1 + N | Custom blog template + article template |
| Custom 404 | 1 | 404 template |
| System pages (auto, content only) | ~5 | Template work only |
| "View all" smart collections (1 per category + 1 vertical) | ~10 | `collection.json` |
| **Total core pages** | **~110** + blog articles | **5 templates** |

> Total grew from ~103 to ~110 after adding FAQ, brand-filtered collections, blog/resources, custom 404, and "View all" smart collections — these were missing for full site interconnection.

---

*Source: BBI site architecture session, 2026-04-25. Approved by Steve. Reference menu backup: `data/backups/main-menu-20260420-234056.json`.*
