# Brant Business Interiors — Master Build Plan
**Store:** [brantbusinessinteriors.com](https://www.brantbusinessinteriors.com)
**Shopify Admin:** [office-central-online](https://admin.shopify.com/store/office-central-online)
**Date:** April 18, 2026 · **Last updated:** April 25, 2026

---

> **Scope change — April 25, 2026:** The shop is narrowed to **Business Furniture only.** The Educational, Daycare & ECE, and Healthcare & Seniors vertical pages have been removed and their products archived in Shopify. The Industries section (Healthcare, Education, Government, etc.) remains — copy now focuses on furnishing *workspaces within those sectors* using business furniture (e.g., reception desks for a hospital, admin chairs for a school board), not sector-specific equipment like operating tables or lab benches.

---

## Site Architecture Reference

Master page map: [`docs/plan/site-architecture-2026-04-25.md`](site-architecture-2026-04-25.md) ← read this before building any page.

**3 active templates to build:**

| Template | Used by |
|---|---|
| `collection.category.json` | Business Furniture vertical + 9 category pages (10 pages) |
| `collection.json` | ~68 Business Furniture sub-collection pages |
| Landing page template | ~19 industry / brand / service / about pages |

**~102 pages total** across all templates.

---

## Corporate Context

BBI is the furniture division of Brant Basics, owned by **Office Central** (founded 1978, $111M revenue, Richmond Hill ON HQ).

- **Both Office Central and Brant Basics are verified OECM supplier partners** — Ontario school boards, hospitals, libraries, universities, and municipalities can buy from BBI through OECM without open tender. No Ontario furniture competitor has this status.
- BBI can claim: *"Backed by Office Central, proudly serving Ontario businesses since 1964."*
- Parent backlinks available: officecentral.com and brantbasics.com — highest-value links BBI can get, already owned.
- **BBI has no Google Business Profile yet** — needs to be created.
- Phone: 1-800-835-9565 · Email: furnorders@officecentral.com

---

## Completed Infrastructure (shipped April 19–20, 2026)

| What | Status |
|------|--------|
| Shopify Admin API + OAuth app | ✅ Done |
| Full order analysis (Oct 2024 → Apr 2026) | ✅ Done |
| Product HTML audit (all 650 SKUs) | ✅ Done |
| ICP + voice sheet locked (`docs/strategy/icp.md`) | ✅ Done |
| 5 approved product description samples (`docs/strategy/voice-samples.md`) | ✅ Done |
| HTML cleanup on 147 top-revenue products | ✅ Done |
| 9 ™/® product handles renamed + redirect CSV generated | ✅ Done (CSV upload pending — Leo's task) |
| 11 service pseudo-products unpublished | ✅ Done |
| 21 junk/test/draft products archived | ✅ Done |
| 41 boilerplate duplicates cleaned | ✅ Done |
| Taxonomy: 14 automated collections built (7 type × 7 room) | ✅ Done |
| 584/613 products tagged with `type:*`, `room:*`, `industry:*` | ✅ Done |
| Main nav rebuilt (8 top-level items live) | ✅ Done |
| Delivery + Installation 7-tier shipping rate live | ✅ Done |
| Site-wide floating "Request a Quote" button | ✅ Done |
| Sold-out/$0-price variants → Request a Quote CTA | ✅ Done |
| Liquid error `divided by 0` on product pages | ✅ Done |
| Announcement bar with phone number | ✅ Done |

---

## Pre-Build Checklist (run once before any Phase work)

- [ ] **Archive task:** run `scripts/archive-non-biz-products.py` — archive all products with sector-specific type tags (educational furniture, daycare, healthcare equipment). Dry-run first, confirm output, then `--live`.
- [ ] **Archive collections:** unpublish/archive `/collections/educational`, `/collections/daycare`, `/collections/healthcare` and all their sub-collections in Shopify Admin.
- [ ] **Update nav:** remove Educational, Daycare, Healthcare columns from mega menu; update "Shop Furniture" click to go directly to `/collections/business-furniture` (no Shop Hub).
- [ ] **Redirect:** set `/pages/shop` → `/collections/business-furniture` in Shopify Admin > Navigation > URL Redirects.
- [ ] **Audit Business Furniture sub-collections:** verify product count > 0 for all ~68 sub-collections. Convert empty collections to smart collections with appropriate rules.
- [ ] **Upload redirect CSV:** `data/url-redirects.csv` — upload in Shopify Admin (Leo's task, was W0-3).
- [ ] **GSC + GA4 setup** (W0-1) — must be live before Phase 1 pages launch so SEO progress is measurable.

---

## Wave 0 — Technical Foundation

*These block all Phase work. No SEO compounds until this layer is solid.*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W0-1 | **Google Search Console + GA4 setup** | 🔴 Critical | ⬜ Not started |
| W0-2 | **Create BBI Google Business Profile** | 🔴 Critical | ⬜ Not started |
| W0-2b | **Google Reviews seeding strategy** | 🔴 Critical | ⬜ Not started |
| W0-3 | **Fix product redirects** | 🔴 Critical | 🔄 CSV at `data/url-redirects.csv` — manual upload in Shopify Admin pending (Leo's task) |
| W0-4 | **Meta titles + descriptions audit** | 🔴 High | ⬜ Not started — brand identity locked, blocked on W0-1 |
| W0-5 | **Confirm Request a Quote CTAs are live** | 🔴 High | ✅ Done |
| W0-6 | **Parent domain backlinks** | 🔴 High | ⬜ Not started |
| W0-7 | **OECM + "Since 1964" trust signals on BBI store** | 🔴 High | ⬜ Not started |

---

## Phase 1 — Conversion & SEO Pages

*Build these first — they're what institutional buyers search for and what drives leads. Pre-req: W0-1 (GSC) live.*

| # | Page | URL | Status |
|---|------|-----|--------|
| P1-1 | **Homepage** | `/` | ⬜ Rebuild needed |
| P1-2 | **OECM Supplier Partner** | `/pages/oecm` | ⬜ Not started |
| P1-3 | **Design Services** | `/pages/design-services` | ⬜ Not started |
| P1-4 | **Request a Quote** | `/pages/quote` | ⬜ Not started |
| P1-5 | **Industries Hub** | `/pages/industries` | ⬜ Not started |
| P1-6 | **Healthcare industry page** | `/pages/healthcare` | ⬜ Not started |
| P1-7 | **Education industry page** | `/pages/education` | ⬜ Not started |
| P1-8 | **Government industry page** | `/pages/government` | ⬜ Not started |
| P1-9 | **Non-Profit industry page** | `/pages/non-profit` | ⬜ Not started |
| P1-10 | **Professional Services industry page** | `/pages/professional-services` | ⬜ Not started |

**Homepage sections (in order):**
1. Hero — headline, CTA to `/collections/business-furniture` or `/pages/quote`
2. Business Furniture category grid (9 tiles → each category page)
3. Featured products (3 Hero 100 items)
4. OECM trust bar — "Verified OECM supplier. Ontario institutions can purchase without open tender."
5. Industries we serve (5 sector thumbnails → industry landing pages)
6. Services overview (Design Services · Delivery · Relocation)
7. Testimonials / Our Work preview
8. Footer with full nav + phone + quote CTA

**Industry page cross-links (all point to Business Furniture):**

| Industry page | Cross-links to |
|---|---|
| `/pages/healthcare` | Reception desks, task seating, waiting room chairs, storage |
| `/pages/education` | Admin seating, staff desks, boardroom tables, storage |
| `/pages/government` | Desks, storage, panels, boardroom |
| `/pages/non-profit` | Seating, tables, accessories |
| `/pages/professional-services` | Ergonomic products, desks, seating |

---

## Phase 2 — Shop Structure

*Unlocks full product UX. Pre-req: Phase 1 complete.*

| # | Page | URL | Template | Status |
|---|------|-----|----------|--------|
| P2-1 | **Business Furniture vertical** | `/collections/business-furniture` | `collection.category.json` | ⬜ Not started |
| P2-2 | Seating | `/collections/seating` | `collection.category.json` | ⬜ Not started |
| P2-3 | Desks & Workstations | `/collections/desks` | `collection.category.json` | ⬜ Not started |
| P2-4 | Storage & Filing | `/collections/storage` | `collection.category.json` | ⬜ Not started |
| P2-5 | Tables | `/collections/tables` | `collection.category.json` | ⬜ Not started |
| P2-6 | Boardroom | `/collections/boardroom` | `collection.category.json` | ⬜ Not started |
| P2-7 | Ergonomic Products | `/collections/ergonomic-products` | `collection.category.json` | ⬜ Not started |
| P2-8 | Panels & Dividers | `/collections/panels-room-dividers` | `collection.category.json` | ⬜ Not started |
| P2-9 | Accessories | `/collections/accessories` | `collection.category.json` | ⬜ Not started |
| P2-10 | Quiet Spaces | `/collections/quiet-spaces` | `collection.category.json` | ⬜ Not started |

All use `collection.category.json`: hero banner · tile grid (section blocks) · breadcrumb back to vertical · "See all Business Furniture" link · phone CTA.

---

## Phase 3 — Collection Template Rollout (~68 sub-collections)

*Bulk apply. Pre-req: `collection.json` template built.*

1. **Build `collection.json` template** — filter sidebar + product grid + breadcrumbs (`Home > Shop Furniture > [Category] > [Sub-collection]`) + phone CTA block at bottom
2. **Apply to all ~68 Business Furniture sub-collections** — assign hero images from `data/page-images/`
3. **Assign hero images** per collection from AI-generated image library

Sub-collections by category: see `docs/plan/site-architecture-2026-04-25.md` §2c for full URL list.

**Phone CTA block (required on every sub-collection page):**
> "Can't find exactly what you need? Our team can help. Call 1-800-835-9565" + "Request a Quote →" button → `/pages/quote`

---

## Phase 4 — Remaining Landing Pages

| # | Page | URL | Status |
|---|------|-----|--------|
| P4-1 | **Brands Hub** | `/pages/brands` | ⬜ Not started |
| P4-2 | Keilhauer dealer page | `/pages/brands-keilhauer` | ⬜ Not started |
| P4-3 | Global / Teknion dealer page | `/pages/brands-global-teknion` | ⬜ Not started |
| P4-4 | ergoCentric dealer page | `/pages/brands-ergocentric` | ⬜ Not started |
| P4-5 | **About Us** | `/pages/about` | ⬜ Not started |
| P4-6 | **Our Work / Portfolio** | `/pages/our-work` | ⬜ Not started — 48 OCI photos ready at `data/oci-photos/catalog.json` |
| P4-7 | **Contact** | `/pages/contact` | ⬜ Not started |
| P4-8 | **Delivery & Installation** | `/pages/delivery` | ⬜ Not started |
| P4-9 | **Relocation Management** | `/pages/relocation` | ⬜ Not started |

---

## Page Interconnection Rules

Apply these when building or editing any page.

1. **Breadcrumbs on all sub-collection pages:** `Home > Shop Furniture > [Category] > [Sub-collection]` — BreadcrumbList JSON-LD included. Confirm 4-level hierarchy.
2. **Category pages link back and across:** breadcrumb to vertical + "See all Business Furniture →" + "Can't find it? Call 1-800-835-9565"
3. **Industry pages cross-link to Business Furniture:** each industry page has "Shop [Sector] Furniture →" button linking to relevant sub-collections (see Phase 1 cross-link mapping above)
4. **Shop vertical cross-links to industry pages:** `/collections/business-furniture` includes contextual module linking to `/pages/industries`
5. **Every sub-collection page has a phone CTA block** (see Phase 3 above)
6. **Homepage surfaces Business Furniture categories** (9 tiles) + OECM trust bar + 5 industry thumbnails
7. **Brand pages link to relevant products:** each `/pages/brands-*` page includes "Shop [Brand] products →" + 3–4 featured products

---

## Wave 2 — Requires Catalog or Product Work

*Pre-req: Phase 3 (Hero 100 product enrichment).*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W2-1 | **Acoustic Pods / Phone Booths sub-collection** | 🔴 High | ⬜ Under `/collections/quiet-spaces` — needs products in catalog |
| W2-2 | **Sit-stand buyer guide + collection** | 🟡 Medium | ⬜ Not started |
| W2-3 | **Hybrid work bundle collection** | 🟡 Medium | ⬜ Not started |
| W2-4 | **Email capture + lead magnet** | 🟡 Medium | ⬜ Not started |
| W2-5 | **Internal linking audit** | 🟡 Medium | ⬜ Not started — after Phase 1 content exists |
| W2-6 | **Co-published content on parent domains** | 🟡 Medium | ⬜ Not started |
| W2-7 | **Schema Markup** | 🟡 Medium | ⬜ Not started |
| W2-8 | **Product title optimization** | 🟢 Quick win | ⬜ Not started — covered in Tier 2 Phase 1.2 (Hero 100 titles) |

---

## Wave 3 — Authority Building (ongoing)

*Pre-req: Wave 1 + Wave 2 content live.*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W3-1 | **City-level SEO pages** | 🟡 Medium | ⬜ Not started |
| W3-2 | **Ergonomics education hub** | 🟡 Medium | ⬜ Not started |
| W3-3 | **Blog — comparison-style content** | 🟡 Medium | ⬜ Not started |
| W3-4 | **Sustainability / LEED / BIFMA page** | 🟢 Lower | ⬜ Not started |
| W3-5 | **Space planning landing page** | 🟢 Lower | ⬜ Not started |
| W3-6 | **Manufacturer dealer locator pages** | 🟢 Lower | ⬜ Not started |
| W3-7 | **OECM directory + Chamber + COPA backlinks** | 🟢 Lower | ⬜ Not started |
| W3-8 | **Brand kit + design authority** | 🟢 Lower | ⬜ Not started |

---

## Reference

- Site architecture (page map, URLs, sub-collections): [`docs/plan/site-architecture-2026-04-25.md`](site-architecture-2026-04-25.md)
- Interactive build checklist: [`previews/bbi-site-build-checklist.html`](../../previews/bbi-site-build-checklist.html)
- Brand voice + ICP: [`docs/strategy/icp.md`](../strategy/icp.md)
- Approved copy samples: [`docs/strategy/voice-samples.md`](../strategy/voice-samples.md)
- Script reference: [`scripts/README.md`](../../scripts/README.md)
- Blog model: btod.com/blog/best-office-chair-reviews/
- Portfolio model: poi.ca/our-work/
