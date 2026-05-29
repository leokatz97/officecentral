# BBI Schema.org / JSON-LD Audit — 2026-05-27

**Branch:** `feature/schema-audit-2026-05-27`
**Task ID:** HOTFIX-SCHEMA-AUDIT-1 (POST-STEVE-CLEANUP afternoon)
**Mode:** Read-only audit. No theme writes in this session.
**LIVE theme:** 186373570873 ("BBI Landing Dev", role=main), updated_at=2026-05-27T13:15:38-04:00
**Auditor:** Claude (Opus 4.7), under Leo Katz's direction
**Audit captures:** [data/audits/schema-audit-2026-05-27/](../../data/audits/schema-audit-2026-05-27/)

---

## TL;DR — top critical findings

1. **PDP `BreadcrumbList` position-2 URL is broken.** Position 2 ("Shop Furniture") emits the homepage URL instead of `/collections/business-furniture`. Every product page on the site has a malformed breadcrumb. **CRIT, blocks Breadcrumb rich result.**
2. **Collection pages emit NO `ItemList` / `CollectionPage` schema.** Product carousel rich result not eligible on any of ~22 collection pages. **[RESOLVED 2026-05-28 — SCHEMA-CRIT-3 shipped summary `ItemList` wrapped in `CollectionPage` on all 3 collection templates (`ds-cc-base`, `ds-cs-base`, `ds-collection-base` = ~209 published collections) via shared `bbi-itemlist-jsonld.liquid` snippet. Branch `feature/schema-crit-3-2026-05-28`, PR #34. **Eligibility correction:** the "product carousel" framing in this finding was WRONG — Google's ItemList carousel is restricted to Course/Movie/Recipe/Restaurant; products are NOT supported, so there is no SERP carousel to earn. Value is entity-graph/AEO only (CollectionPage typing + machine-readable product enumeration). Summary structure (ListItem position+url+name, NO inline Product) sidesteps the F-15 trap by design. Page-scoped, capped 30, position_offset verified across pagination. CRIT-3 output clean: 0 Product nodes, 0 errors, no regression, theme check 2850/166. See build-state SCHEMA-CRIT-3 entry + closing addendum.]**
3. **Industry / segment landing pages emit NO surface-specific schema.** Healthcare, Education, Government, Non-Profit, Professional Services, Industries Hub all rely on chrome only — no `Service`, no `WebPage`, no `ItemList`. These are the most strategically important pages for OECM-driven B2B SEO. **[RESOLVED 2026-05-28 — SCHEMA-CRIT-2 shipped `Service` + `FAQPage` on all 6 pages via shared `bbi-service-jsonld.liquid` snippet + inline FAQPage (42 verbatim Q&As). Branch `feature/schema-crit-2-2026-05-28`. Honest framing: entity-graph/AEO value only — `FAQPage` does NOT earn a SERP rich result (2023 Google policy restricts FAQ rich results to authoritative gov/health sites; BBI does not qualify, incl. the government page), `Service` is not a rich-result type. `OfferCatalog` (M-6) deliberately omitted to avoid recreating the SCHEMA-CRIT-NEW-1 invalid-Product-snippet problem. RRT 2-of-6 spot-check: 5 valid items, 0 errors each; no chrome regression. See build-state SCHEMA-CRIT-2 entry.]**
4. **PDPs missing Merchant Listing requirements.** No `priceValidUntil`, `hasMerchantReturnPolicy`, `shippingDetails`, or `itemCondition` on `offers`. Blocks eligibility for Merchant Listings rich results.
5. **Product `brand.name` is hardcoded to `product.vendor` which is set to "Brant Business Interiors" on many SKUs.** Should be the manufacturer (Fellowes, Global, Teknion, etc.). Causes brand misattribution in SERP — confirmed on `dual-monitor-arm` (actual brand: Fellowes).
6. **`booster-seo.liquid` is dead code** containing 5 duplicate JSON-LD emitters (Organization, WebSite, Product, Blog, Article). Currently un-rendered but a footgun if ever re-introduced. **Polish — delete the snippet.**

---

## Phase 0 — schema emitter inventory

### Sitewide emitters (rendered via chrome on every `bbi_landing` page)

| File | Line | Schema | Trigger | Notes |
|---|---|---|---|---|
| [`theme/snippets/bbi-org-schema.liquid`](../../theme/snippets/bbi-org-schema.liquid) | 7 | `@graph: [Organization+LocalBusiness, WebSite+SearchAction]` | rendered from `bbi-nav.liquid:12` → every BBI-routed page | `@id` = `…/#organization`. Includes `hasOfferCatalog` with 8 lightweight `Offer→Product` items (category placeholders). `parentOrganization` = Office Central Group. |
| [`theme/snippets/bbi-localbusiness-schema.liquid`](../../theme/snippets/bbi-localbusiness-schema.liquid) | 19 | `LocalBusiness` (dedicated) | rendered from `theme/layout/theme.liquid:171` (gated on `bbi_landing`) | `@id` = `…/#localbusiness`. Dedicated entity for local-pack / GBP linking, distinct from combined Org+LocalBus. `sameAs: []` (intentionally empty — Steve confirmed 2026-05-24). |
| [`theme/snippets/booster-seo.liquid`](../../theme/snippets/booster-seo.liquid) | 232, 260, 277, 598, 615 | Organization, WebSite, Product, Blog, Article | **dead code — no `render` call anywhere** | Vestigial Booster app snippet. Would emit duplicate Organization + WebSite + Product if re-introduced. Delete. |

### Section-level emitters (template-specific)

| File | Line | Schema | Surface |
|---|---|---|---|
| [`theme/sections/ds-pdp-base.liquid`](../../theme/sections/ds-pdp-base.liquid) | 407 | renders `bbi-product-jsonld` (Product + BreadcrumbList) | every PDP |
| [`theme/snippets/bbi-product-jsonld.liquid`](../../theme/snippets/bbi-product-jsonld.liquid) | 49 | `Product` w/ optional `additionalProperty[]` from specs metafields | PDPs |
| [`theme/snippets/bbi-breadcrumb-jsonld.liquid`](../../theme/snippets/bbi-breadcrumb-jsonld.liquid) | 19 | `BreadcrumbList` (1-4 levels) | PDPs, collection pages, sub-collection pages |
| [`theme/sections/ds-cc-base.liquid`](../../theme/sections/ds-cc-base.liquid) | 532, 562, 570 | `FAQPage` (if blocks present) + `BreadcrumbList` (2 or 3 level) | collection pages |
| [`theme/sections/ds-cs-base.liquid`](../../theme/sections/ds-cs-base.liquid) | 296 | `BreadcrumbList` (sub-collection) | sub-collection pages |
| [`theme/sections/ds-article.liquid`](../../theme/sections/ds-article.liquid) | 149, 192 | `BlogPosting` + optional `FAQPage` (from `article.metafields.faq.items`) | blog article pages |
| [`theme/sections/ds-lp-oecm.liquid`](../../theme/sections/ds-lp-oecm.liquid) | 297 | `@graph: [GovernmentService, FAQPage]` | `/pages/oecm` |
| [`theme/sections/ds-lp-quote.liquid`](../../theme/sections/ds-lp-quote.liquid) | 356 | `@graph: [Service, FAQPage]` | `/pages/quote` |
| [`theme/sections/ds-lp-relocation.liquid`](../../theme/sections/ds-lp-relocation.liquid) | 137 | `Service` (uses `@id` ref to `#organization`) | `/pages/relocation` |
| [`theme/sections/ds-lp-delivery.liquid`](../../theme/sections/ds-lp-delivery.liquid) | 149 | `Service` (uses `@id` ref to `#organization`) | `/pages/delivery` |
| [`theme/sections/ds-lp-design-services.liquid`](../../theme/sections/ds-lp-design-services.liquid) | 14, 31 | `HowTo` + `FAQPage` | `/pages/design-services` |
| [`theme/sections/ds-lp-faq.liquid`](../../theme/sections/ds-lp-faq.liquid) | 138 | `FAQPage` (5 hardcoded Q&A) | `/pages/faq` |

### Sections with NO surface-specific schema (chrome-only)

These pages emit only the sitewide `Organization`/`LocalBusiness`/`WebSite` chrome — no surface-specific structured data. Sorted by SEO impact:

| Section | Page | Strategic importance |
|---|---|---|
| `ds-lp-healthcare` | `/pages/healthcare` | HIGH — OECM hospital buyers |
| `ds-lp-education` | `/pages/education` | HIGH — OECM school boards |
| `ds-lp-government` | `/pages/government` | HIGH — municipalities |
| `ds-lp-non-profit` | `/pages/non-profit` | MED — broader-public-sector |
| `ds-lp-professional-services` | `/pages/professional-services` | MED — private B2B |
| `ds-lp-industries` | `/pages/industries` | HIGH — segment hub |
| `ds-lp-about` | `/pages/about` | MED — entity signal |
| `ds-lp-contact` | `/pages/contact` | MED — entity signal |
| `ds-lp-our-work` | `/pages/our-work` | MED — case study hub |
| `ds-lp-customer-stories` | `/pages/customer-stories` | LOW — content surface |
| `ds-lp-brands` | `/pages/brands` | MED — brand portfolio |
| `ds-lp-brands-*` (6 pages) | `/pages/brands-{ergocentric,global-teknion,heartwood,keilhauer,obusforme,otg}` | HIGH — per-brand SEO, no `Brand` schema |
| `ds-blog-list` | `/blogs/news` | MED — blog landing |
| `ds-system-404` | 404 page | LOW — chrome only is fine here |

---

## Phase 1 — LIVE rendering validation

**Captures:** 23 URLs fetched (`data/audits/schema-audit-2026-05-27/captures/`). All returned 200 except 404 page (intentional 404 — emits chrome correctly when fetched with error handling).

### Per-surface emission summary

| Surface | Blocks | Types (deduped) |
|---|---|---|
| Homepage | 2 | LocalBusiness + Org+LocBus + WebSite |
| Collection (seating / desks / business-furniture) | 4 | + FAQPage + BreadcrumbList |
| PDP (dual-monitor-arm) | 4 | + Product + BreadcrumbList |
| /pages/oecm | 3 | + GovernmentService + FAQPage |
| /pages/quote | 3 | + Service + FAQPage |
| /pages/relocation | 3 | + Service |
| /pages/delivery | 3 | + Service |
| /pages/design-services | 4 | + HowTo + FAQPage |
| /pages/faq | 3 | + FAQPage (hardcoded) |
| /pages/about, contact, brands, brands-*, our-work, healthcare, education, industries, customer-stories | 2 | chrome only |
| /blogs/news | 2 | chrome only (Blog schema missing) |
| /search?q=desk | 2 | chrome only |
| 404 | 2 | chrome only (correct — 404 doesn't need more) |

### Cross-cutting findings (all surfaces)

**F-1. Organization name + alternateName are correctly distinguished.** `"name": "Brant Business Interiors"`, `"alternateName": "BBI"`. The `feedback_bbi_copy_voice.md` rule ("never publish 'BBI' to customers") is respected — "BBI" only appears as `alternateName`.

**F-2. Canonical Peterborough address is consistent.** All emitters use `296 George St N, Peterborough, ON, K9J 3H2` — matches `project_bbi_canonical_address.md`. No stale Brantford references in schema.

**F-3. OECM Agreement 2025-470 is mentioned only in descriptions, not as a structured field.** Could add `Certification` or `agreementID` property to GovernmentService. (Low impact.)

**F-4. `@id` discipline is inconsistent.**
  - `bbi-org-schema` uses `…/#organization` ✓
  - `bbi-localbusiness-schema` uses `…/#localbusiness` ✓
  - `ds-lp-relocation`, `ds-lp-delivery` use `{"@id": "…/#organization"}` provider reference ✓ (good practice)
  - `ds-lp-oecm`, `ds-lp-quote` redeclare full `LocalBusiness` inline as `provider` instead of referencing `…/#localbusiness` — produces 3rd LocalBusiness instance per page. **WARN.** **[RESOLVED 2026-05-28 — SCHEMA-H-1, branch `feature/schema-polish-1-2026-05-28`.** Both inline `provider` blocks converted to `{"@id": "https://{{ shop.permanent_domain }}/#organization"}` (matching the relocation/`bbi-service-jsonld` pattern). LocalBusiness node count 3→2 per page; `provider` resolves to the canonical entity; no property loss (the `#organization` node is a strict superset). Storefront RRT confirms 2 nodes (was 3). **NB:** this fixed the *duplicate-entity* issue only — it did NOT clear the RRT "Local businesses non-critical" WARN, which is the separate missing-`image` finding (see Addendum 2026-05-28 below). The two were conflated in the original H-1 framing.]**
  - `ds-article.liquid` `BlogPosting.publisher` redeclares Organization fields rather than `@id`-referencing. **WARN.**

**F-5. PDP `brand.name` falls back to `product.vendor`.** `product.vendor` is set to "Brant Business Interiors" on many SKUs (vendor = dealer, not manufacturer). Confirmed on `dual-monitor-arm` PDP — actual manufacturer is Fellowes (per description text), but emitted brand is "Brant Business Interiors". **CRIT — incorrect brand attribution.**

  - **RESOLUTION — schema-side fix DROPPED BY DECISION 2026-05-28 (SCHEMA-CRIT-1b).** Live-data sizing invalidated the premise: enriched (Hero-100) SKUs already have `product.vendor` re-attributed to the manufacturer (21/25 sampled had `vendor == specs.manufacturer`, so preferring the metafield is a no-op); the few that would change inject messy strings ("Global Furniture Group (likely)", "…(Global Care)") worse than the clean vendor; and the broad ~410 vendor=BBI products are non-enriched (no manufacturer metafield) so the schema fix can't reach them. The real fix is the data-side vendor re-attribution project (out of scope). Working emitter left unchanged.

**F-6. PDP breadcrumb position-2 URL bug.** `bbi-product-jsonld.liquid` passes `bc2_url: bc_base | append: '/collections/business-furniture'` to the breadcrumb snippet, but the LIVE-rendered output for position 2 shows just `https://www.brantbusinessinteriors.com` (homepage). Position 1, 3, and 4 are correct.

  - Captured: `"position": 2, "name": "Shop Furniture", "item": "https://www.brantbusinessinteriors.com"`
  - Expected: `"item": "https://www.brantbusinessinteriors.com/collections/business-furniture"`
  - Hypothesis: Liquid scoping inside `render` may be dropping the `append` filter result. Needs targeted debugging — but the rendered HTML is the source of truth.
  - **CRIT — Breadcrumb rich result will not validate.**

**F-7. PDP `offers` missing Merchant-Listing-grade fields.** Captured offer block:
  ```json
  {
    "@type": "Offer",
    "url": "...",
    "priceCurrency": "CAD",
    "price": 299.99,
    "availability": "InStock",
    "seller": { "@type": "Organization", "name": "Brant Business Interiors" }
  }
  ```
  Missing: `priceValidUntil`, `hasMerchantReturnPolicy`, `shippingDetails`, `itemCondition` (recommend `https://schema.org/NewCondition`). Without these, PDPs cannot achieve Merchant Listings rich result eligibility.

  - **PARTIAL RESOLUTION ✅ 2026-05-28 (SCHEMA-CRIT-1b):** `itemCondition: https://schema.org/NewCondition` added unconditionally; `priceValidUntil` added buyable-branch-only (today+365d, leap-day-safe, renders `2027-05-28`). Quote-only branch correctly excluded from `priceValidUntil`. RRT 3/3 = 7 valid items, 0 errors.
  - **FULLY RESOLVED ✅ 2026-05-29 (SCHEMA-CRIT-1c):** `hasMerchantReturnPolicy` (`MerchantReturnPolicy`: applicableCountry CA, MerchantReturnFiniteReturnWindow, merchantReturnDays 30, ReturnByMail, ReturnShippingFees, canonical merchantReturnLink) + `shippingDetails` (`OfferShippingDetails`: CA destination, handlingTime 1–3 DAY, transitTime 1–15 DAY) added to PDP `offers`, **both unconditional**, all constants as full URIs. Policy pages verified live first (refund + shipping, HTTP 200 with real text). RRT 3/3 = 7 valid, 0 errors; both blocks recognized in RRT structured-data expansion. Regression confirmed intact on quote-only `boulevard-system-3`. **`shippingRate` + `returnShippingFeesAmount` deliberately omitted** (quote-based shipping — omission > fabrication; RRT surfaces them as recommended-only). **All four Merchant Listing fields now shipped — this finding is closed.** Honest note: the four fields are completeness — a Merchant Listing *rich result* also needs Google Merchant Center / a product feed, which is out of theme scope.

**F-8. `Product` has no `aggregateRating` / `review`.** No review data in store — not a defect per se, but blocks Review rich result.

**F-9. PDP `seller` is a 4th Organization node.** `offers.seller` declares a new `Organization` inline rather than referencing `#organization` via `@id`. WARN — duplicate entity.

**F-10. Collection pages have no `ItemList` / `CollectionPage`.** Listed products are absent from structured data. Blocks product-carousel rich results.

**F-11. Blog landing (`/blogs/news`) emits no `Blog` schema.** ~~`ds-blog-list.liquid` does not emit `Blog` or `CollectionPage`.~~ **✅ RESOLVED 2026-05-29 (SCHEMA-BLOG-1 / H-2):** `ds-blog-list.liquid` now renders `bbi-blog-jsonld.liquid` → `Blog` entity with `blogPost[]` enumeration. Individual articles emit `BlogPosting` (via `ds-article.liquid`, enhanced this session with articleSection + keywords).

**F-12. Industry segment pages emit no `Service` / `WebPage` / `ItemList`.** Healthcare, education, government, non-profit, professional-services, industries hub — all chrome-only. These are the most strategically important B2B SEO pages and should emit `Service` (institutional procurement) with `serviceType`, `areaServed`, and ideally an `OfferCatalog` of representative product categories.

**F-13. Brand manufacturer pages emit no `Brand` schema.** `/pages/brands-ergocentric`, `…-global-teknion`, `…-heartwood`, `…-keilhauer`, `…-obusforme`, `…-otg` — no Brand or Organization schema for the featured manufacturer. Should emit a `Brand` (or `Organization` if appropriate) with `manufacturer` relationship + `subjectOf` linking BBI.
  - **✅ RESOLVED 2026-05-29 (SCHEMA-BRAND-1, branch `feature/schema-brand-1-2026-05-29`).** 7 `Brand` entities shipped across the 6 pages via shared `theme/snippets/bbi-brand-jsonld.liquid` (dual Brand on `brands-global-teknion` — Global + Teknion as independent sister companies, no `parentOrganization`). `@type: Brand` chosen to match the PDP `brand.name` reference (entity-graph coherence). Each Brand: `name` + `description` + `@id` + `mainEntityOfPage` + verified `sameAs`. `logo` omitted (no assets — see MANUFACTURER-LOGO-ACQUISITION Tier 2B); `manufacturer`/`subjectOf` relationship NOT emitted (the original suggestion's `parentOrganization`/seller framing was rejected on honesty grounds — BBI is a dealer, not parent). Cache-busted curl 2→3 (single) / 2→4 (combined); RRT 0 errors (Brand not rich-result-eligible, parsed clean). Theme check 2833/165 held. See Day 16 build-state entry.

**F-14. About + Contact pages emit no `AboutPage` / `ContactPage`.** These are weak signal classes but cheap to add and aid entity disambiguation.

**F-15. `hasOfferCatalog` in `bbi-org-schema` uses lightweight `{"@type":"Product","name":"Seating"}` items.** Acceptable per Google guidelines (lightweight references, not full Product nodes). NOT a defect.  **[RECLASSIFIED 2026-05-27 ~15:06 — MISCLASSIFIED. Google's Rich Results Test flags all 8 items as invalid Product snippets ("Either 'offers', 'review' or 'aggregateRating' should be specified"). See Addendum at end of document. Tracked as SCHEMA-CRIT-NEW-1.] [RESOLVED 2026-05-27 late-night — SCHEMA-CRIT-NEW-1 shipped via Path C (block deletion). See Resolution section in Addendum.]**

**F-16. `LocalBusiness.priceRange` is set on the dedicated emitter only.** The combined Org+LocBus in `bbi-org-schema` omits `priceRange`. Both should have it for consistency. WARN.

**F-17. `bbi-localbusiness-schema.sameAs` is empty `[]`.** Intentional per code comment (Steve confirmed 2026-05-24 no social presence). Update once social profiles launch.

---

## Phase 2 — Google Rich Results eligibility (per surface)

Eligibility assessed from captured JSON-LD + Google's documented rich-result requirements. Manual review (no Rich Results Test API).

| Surface | Currently eligible for | NOT eligible (and why) |
|---|---|---|
| Homepage | Sitelinks Search Box (WebSite+SearchAction ✓), Organization knowledge panel (Org ✓) | LocalBusiness rich result (mostly populated but `sameAs: []` weakens it) |
| Collection (seating, desks, …) | Breadcrumb (✓), FAQ rich result (if blocks present ✓) | Product list / ItemList carousel (no ItemList emitted) |
| PDP (with valid breadcrumb URL) | Product snippet (price+availability ✓) | Breadcrumb (**broken position-2 URL** — F-6); Merchant Listings (no priceValidUntil, no return policy, no shipping — F-7); Reviews (no aggregateRating — F-8) |
| /pages/oecm | FAQ ✓ | GovernmentService isn't a Google rich result type but **is read by AI crawlers** — copy is good; provider should `@id`-reference (F-4) |
| /pages/quote | FAQ ✓ | Service isn't a rich result, but signals to AI crawlers — provider redeclares (F-4) |
| /pages/design-services | FAQ ✓, HowTo (✓ with optional warnings re: `image`) | — |
| /pages/faq, /pages/delivery, /pages/relocation | FAQ ✓ (faq only) | — |
| /pages/healthcare, education, government, industries, non-profit, professional-services, about, contact, brands, brands-*, our-work, customer-stories | Organization, LocalBusiness | Service / WebPage / ItemList / Brand — none emitted (F-12, F-13, F-14) |
| /blogs/news | — | Blog (F-11) |
| Blog article (sample fetch deferred — no article URL in fetch list) | BlogPosting (✓ via ds-article) | — |

---

## Phase 3 — competitive + AI-crawler context

Spot-checked POI (Steelcase Ontario dealer), Source Office Furniture (national), Grand & Toy (national B2B office). Full report in agent finding above; condensed here.

**Bar to clear (competitors' floor):**
- LocalBusiness with full address (POI ✓, Source ✓ as Organization, G&T ✗)
- WebSite + SearchAction (POI ✓, Source ✓, G&T ✗)
- BreadcrumbList sitewide (POI ✓, Source ✓, G&T ✗)
- BBI is **already at or above** this bar.

**Differentiators competitors miss (BBI's leapfrog targets):**
- Product + Offer on PDPs — BBI ✓, Source ✗, G&T ✗ ← BBI already ahead
- aggregateRating/Review on PDPs — nobody emits (review data gap industry-wide)
- ItemList on collection pages — nobody emits — **BBI gap (F-10) but adding it = competitive moat**
- FAQPage on collection pages — Source emits, BBI partially emits (only when blocks present) — **format-match Source pattern**
- Service / GovernmentService for B2B services — nobody emits — **BBI partially has it (oecm/quote/delivery/relocation), extending to industry pages = clear moat**
- Brand schema on manufacturer pages — nobody emits — **BBI gap (F-13)**
- HowTo on guides — nobody emits except BBI (design-services HowTo) — **BBI ahead**

**Standout pattern from Source:** FAQPage on every category page (strong AI Overview citation play). BBI's `ds-cc-base` only emits FAQPage when `faq_item` blocks exist — most category pages don't have them. Adding default FAQ blocks (or always-on FAQ schema with at least 3 generic Q&As about "delivery times", "OECM eligibility", "warranty") would mirror this play.

**AI crawler implications:** Perplexity / ChatGPT / Claude / Gemini all consume schema for entity grounding. The OECM `GovernmentService` framing on `/pages/oecm` is a unique-in-category signal — extending the same pattern to healthcare/education/government industry pages would compound this AI-search advantage.

---

## Phase 4 — prioritized fix matrix

Order: SEO impact × leverage (one-snippet fixes that cover many surfaces) × effort.

### CRITICAL (do first — blocks high-value rich results)

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| C-1 | Fix PDP BreadcrumbList position-2 URL (F-6). Debug why `bc_base \| append: '/collections/business-furniture'` resolves to `bc_base` only at render-call. Likely fix: assign `bc2_url` into a local variable BEFORE the render call. | `theme/snippets/bbi-product-jsonld.liquid:163-165` | S | H — every PDP loses Breadcrumb rich result eligibility today | LOW (schema-only) | — |
| C-2 | Add `ItemList` / `CollectionPage` schema to collection pages (F-10). One emitter in `ds-cc-base.liquid` — iterate `collection.products` (limit ~20) emit `ListItem` with name + URL + image. | `theme/sections/ds-cc-base.liquid` | M | H — product-carousel rich result on ~22 collections | LOW | — |
| C-3 | ~~Fix PDP `brand.name` data attribution (F-5). Schema-side fallback: prefer `product.metafields.specs.manufacturer` over `product.vendor`.~~ **DROPPED BY DECISION 2026-05-28 (SCHEMA-CRIT-1b, branch `feature/schema-crit-1b-2026-05-28`).** Live-data sizing invalidated the premise: enriched (Hero-100) SKUs already have `product.vendor` re-attributed to the manufacturer (21/25 sampled had `vendor == specs.manufacturer` → fix is a no-op); the ~2/25 that would change inject messy strings ("Global Furniture Group (likely)", "…(Global Care)") worse than the current clean vendor; and the broad ~410 vendor=BBI products are non-enriched (no metafield) so the schema fix can't touch them — that's the data-side vendor re-attribution project (out of scope). Not worth touching a working emitter. | `theme/snippets/bbi-product-jsonld.liquid:60-65` | S | ~~H~~ → near-no-op | LOW | — |
| C-4 | Add `Service` schema to industry/segment landing pages (F-12). One reusable snippet `bbi-service-jsonld.liquid` rendered from healthcare/education/government/non-profit/professional-services/industries sections. Mirror `ds-lp-delivery.liquid` pattern with `@id` ref to `#organization`. | new snippet + 6 section renders | M | H — eligibility + AI-crawler grounding for highest-value B2B pages | LOW | — |
| C-5 | Add Merchant Listing fields to PDP `offers` (F-7). **✅ COMPLETE — all 4 fields shipped.** SCHEMA-CRIT-1b (2026-05-28): `itemCondition` (unconditional) + `priceValidUntil` (buyable-branch-only). SCHEMA-CRIT-1c (2026-05-29): `hasMerchantReturnPolicy` + `shippingDetails` (both unconditional, full URIs, canonical merchantReturnLink; `shippingRate`/`returnShippingFeesAmount` deliberately omitted — quote-based). Policy pages verified live first. RRT 3/3 = 7 valid 0 errors; regression intact on quote-only. Honest framing: a Merchant Listing *rich result* also needs Merchant Center / a product feed (out of theme scope). | `theme/snippets/bbi-product-jsonld.liquid` | M | H — unlocks Merchant Listings rich result on all PDPs | LOW (schema-only) | ✅ done |

### HIGH-IMPACT

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| H-1 | ~~Convert inline `provider` redeclarations in OECM + Quote sections to `@id` references (F-4). Match the relocation/delivery pattern. Removes 1 extra LocalBusiness node per page.~~ **✅ DONE 2026-05-28** (SCHEMA-H-1, branch `feature/schema-polish-1-2026-05-28`). LocalBusiness 3→2/page; F-4 resolved on both. **Did NOT clear the missing-`image` WARN** — separate finding (see Addendum). | `ds-lp-oecm.liquid:304-317`, `ds-lp-quote.liquid:363-376` | S | M — entity-graph clarity, mild AI-crawler benefit | LOW | C-4 prep work |
| H-2 | ~~Add `Blog` schema to blog landing page (F-11). `Blog` with `mainEntityOfPage`, `publisher` `@id`-ref to `#organization`.~~ **✅ RESOLVED 2026-05-29 (SCHEMA-BLOG-1).** New `bbi-blog-jsonld.liquid` rendered from `ds-blog-list.liquid`: `Blog` with name/description/@id/url/mainEntityOfPage + publisher `@id`-ref to `#organization` + `blogPost[]` enumeration. Plus enhanced the already-live inline BlogPosting on the OECM post (articleSection + keywords + honest-omission image). RRT 5 valid / 0 errors per page; cross-page `@id` byte-identical. See Day 16 build-state. | new snippet `bbi-blog-jsonld.liquid` + `ds-blog-list.liquid` render + `ds-article.liquid` enhancement | S | M — blog hub eligibility, AI crawler grounding | LOW | — |
| H-3 | ~~Add `Brand` (or `Organization` w/ `manufacturer` relationship) schema to 6 manufacturer pages (F-13). Per-brand: name, logo, URL, parentOrganization (BBI as seller).~~ **✅ RESOLVED 2026-05-29 (SCHEMA-BRAND-1).** 7 `Brand` entities across 6 pages via `bbi-brand-jsonld.liquid` (dual on `brands-global-teknion`). `@type: Brand` (matches PDP ref). name + description + @id + mainEntityOfPage + verified sameAs. `logo` deferred (no assets → MANUFACTURER-LOGO-ACQUISITION Tier 2B); `parentOrganization` rejected on honesty grounds (BBI = dealer, not parent; Global/Teknion = sister cos). RRT 0 errors. See F-13 + Day 16 build-state. | new snippet `bbi-brand-jsonld.liquid` + 6 section renders | M | M — manufacturer-page SEO + Brand knowledge-panel eligibility | LOW | — |
| H-4 | Convert PDP `offers.seller` to `@id` reference (F-9). Remove inline Organization redeclaration. | `bbi-product-jsonld.liquid:145-148` | S | L-M — entity-graph clarity | LOW | — |
| H-5 | Format-match Source: always-on `FAQPage` on category pages, with 3 default Q&As if `faq_item` blocks empty (F-3 from Phase 3). | `ds-cc-base.liquid` | S | M — AI Overview citation play on ~22 category pages | LOW | — |

### MEDIUM-IMPACT

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| M-1 | Add `AboutPage` / `ContactPage` schema (F-14). Single page each, wraps existing entity reference. | `ds-lp-about.liquid`, `ds-lp-contact.liquid` | S | L-M — entity disambiguation signal | LOW | — |
| M-2 | Add `priceRange: "$$"` to combined Org+LocBus in `bbi-org-schema` (F-16). Match dedicated emitter. | `bbi-org-schema.liquid:40` (insert after `openingHours`) | S | L | LOW | — |
| | **DROPPED 2026-05-28 (SCHEMA-POLISH-1 triage).** `"$$"` is a dubious claim for a quote-based B2B catalog with no public pricing. **Inconsistency note for whoever revisits:** the dedicated `#localbusiness` node (`bbi-localbusiness-schema.liquid:47`) *already* asserts `priceRange:"$$"` while `#organization` does not — so the real decision is whether to assert `priceRange` at all (drop from both for consistency) vs. add it to `#organization`. **Not the missing-`image` WARN** (RRT confirmed that WARN fires on the `#localbusiness` node too, which already has priceRange). | | | | | |
| M-3 | Convert `BlogPosting.publisher` to `@id` reference (F-4). | `ds-article.liquid:168-178` | S | L | LOW | — |
| M-4 | Add `agreementID` or `Certification` for OECM 2025-470 (F-3). `GovernmentService.identifier` or sub-typed certification. | `ds-lp-oecm.liquid` | S | L — explicit OECM signal | LOW | — |
| M-5 | Add `Article` schema to customer-story pages (`/pages/customer-stories`). Each story → ItemList of Article references. | `ds-lp-customer-stories.liquid` | M | L-M — content-page SEO | LOW | content structure review |
| M-6 | Add `OfferCatalog` to industry-page Services (companion to C-4). Each Service includes representative product categories. | within C-4 service snippet | S | M | LOW | depends on C-4 |

### POLISH

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| P-1 | ~~Delete dead `booster-seo.liquid` snippet (F-6 from inventory).~~ **DONE (repo) ✅ 2026-05-28 (SCHEMA-CRIT-1b):** `git rm theme/snippets/booster-seo.liquid` (orphaned — zero refs confirmed). **LIVE asset removal deferred** as `LIVE-booster-seo-asset-removal` (Tier 3) — inert on LIVE (PDPs emit exactly 1 Product), removing it is a destructive op with zero upside, so own-session only. | `theme/snippets/booster-seo.liquid` | S | L (footgun removal) | LOW | — |
| P-2 | Update `bbi-localbusiness-schema.sameAs` once social profiles launch (F-17). | `bbi-localbusiness-schema.liquid:51` | S | L | LOW | Steve to confirm social URLs |
| P-3 | Add `image` to `HowTo` schema on design-services page (Phase 1 WARN). | `ds-lp-design-services.liquid:14-29` | S | L | LOW | — |

---

## Suggested execution order

**Session 1 — CRIT batch — split across 2 sessions (Fix 1 + CRIT-1b):**
- C-1 (breadcrumb URL fix) ✅ **SHIPPED 2026-05-27** (SCHEMA-CRIT-1 Fix 1, branch `feature/schema-crit-1-2026-05-27`, RRT-confirmed).
- C-3 (brand.name fallback) ❌ **DROPPED BY DECISION 2026-05-28** (SCHEMA-CRIT-1b) — premise stale, near-no-op, net-negative on the few it'd touch. See C-3 row / F-5 resolution.
- C-5 (Merchant Listing fields) ✅ **COMPLETE** — itemCondition + priceValidUntil SHIPPED 2026-05-28 (SCHEMA-CRIT-1b); `hasMerchantReturnPolicy` + `shippingDetails` SHIPPED 2026-05-29 (SCHEMA-CRIT-1c, branch `feature/schema-crit-1c-2026-05-29`). All 4 Merchant Listing fields now live. **This completes SCHEMA-CRIT-1 (C-1 Fix 1 + C-5 = breadcrumb + all 4 offer fields) — CRIT-1 fully closed.**
- P-1 (delete booster-seo dead code) ✅ **DONE (repo) 2026-05-28** (SCHEMA-CRIT-1b). LIVE asset removal deferred → `LIVE-booster-seo-asset-removal` (Tier 3).

PR titles: `SCHEMA-CRIT-1: fix PDP breadcrumb URL` (#28, Fix 1) + `SCHEMA-CRIT-1b: PDP Merchant Listing fields (itemCondition + priceValidUntil) + remove dead booster-seo (repo)` (branch `feature/schema-crit-1b-2026-05-28`, stacked on #35).

**Session 2 — Industry/segment schema — ✅ SHIPPED 2026-05-28 (SCHEMA-CRIT-2, branch `feature/schema-crit-2-2026-05-28`):**
- C-4 ✅ — new `bbi-service-jsonld` snippet + 6 industry pages. **Also added `FAQPage`** (not in original C-4 scope) — all 6 pages had 7 hardcoded Q&As, surfaced as inline FAQPage (42 verbatim Q&As).
- H-1 ⏸️ **deferred** — NOT done same-session. Reframed as an edit-to-live-schema (this session stayed purely additive). Tracked as SCHEMA-H-1 in build-state Tier 2B.
- M-6 ❌ **deliberately dropped** — `OfferCatalog` with lightweight `Product` items recreates the SCHEMA-CRIT-NEW-1 invalid-Product-snippet problem (Google RRT flags every `{"@type":"Product"}` stub). Zero rich-result payoff; omitted.

PR title: `SCHEMA-CRIT-2: Service + FAQPage schema for industry pages (healthcare/education/government/non-profit/professional-services/industries)`

**Session 3 — Collection schema + format-match Source (~60-90 min):**
- C-2 (ItemList / CollectionPage on collections)
- H-5 (always-on FAQPage on collections with defaults)

PR title: `SCHEMA-CRIT-3: ItemList + always-on FAQPage on collection pages`

**Session 4 — High-impact polish (~45-60 min):**
- ~~H-2 (Blog landing schema)~~ — ✅ **RESOLVED 2026-05-29 (SCHEMA-BLOG-1, own session)** — new `bbi-blog-jsonld.liquid` (`Blog` + `blogPost[]` enumeration) on `/blogs/news` + enhanced the already-live inline BlogPosting on the OECM post (articleSection + keywords + honest-omission image). RRT 5 valid / 0 errors per page; cross-page `@id` byte-identical.
- ~~H-3 (Brand pages × 6)~~ — ✅ **RESOLVED 2026-05-29 (SCHEMA-BRAND-1, own session — 7 Brand entities across 6 pages)**
- H-4 (PDP seller @id ref)
- M-1, M-2, M-3, M-4 (entity polish batch)

PR title: `SCHEMA-POLISH-1: blog/brand pages + entity-graph cleanup`

---

**SCHEMA LANE STATUS (updated 2026-05-29 after SCHEMA-BLOG-1):** **SOLO-ACTIONABLE SCHEMA WORK NOW FULLY COMPLETE.** Shipped: CRIT-1 (Fix 1 + 1b + 1c), CRIT-2 (Service + FAQPage on industry pages), CRIT-3 (ItemList/CollectionPage), CRIT-4 (bare-Product card strip), H-1 (LocalBusiness @id dedup), **BRAND-1 (Brand × 6 pages)**, **F-LOCALBUSINESS-IMAGE (`image` on both chrome LB nodes)**, **BLOG-1 (Blog schema + BlogPosting enhancement)**. **Day 16 finishes the audit. CRIT-1, CRIT-2, CRIT-3, CRIT-4, all H-* items, F-* items, and POLISH-1 items are all resolved or properly deferred to content / Steve / design.** Remaining items are NOT solo-actionable:
- ~~**SCHEMA-BLOG-1**~~ (H-2) — ✅ **RESOLVED 2026-05-29** (own session). The last solo-actionable schema item; now closed.
- ~~**F-LOCALBUSINESS-IMAGE**~~ — ✅ **RESOLVED 2026-05-29** (see Addendum). Day storefront ImageObject on both `#organization` + `#localbusiness` nodes.
- **The Local businesses row's residual non-critical is now `priceRange`-only on `#organization`** — that's **M-2** (separate POLISH-1 finding; deliberate omission — we don't assert `$$` on the Brand-encompassing #organization node for a quote-based catalog). The badge persists by design; not actionable as a "fix."
- **H-4 / M-1..M-4** — minor entity-graph polish, low priority.
- **Content-side / Steve-gated:** STEVE-SET-BLOG-FEATURED-IMAGE (unlocks Article rich-result on the OECM post, ~30 sec), BRAND-PAGE-COPY-FIX (Teknion/Global sister-co copy error), BRAND-PAGE-HERO-IMAGE-AUDIT.
- **Schema-enrichment Tier 2B:** MANUFACTURER-LOGO-ACQUISITION, BRAND-SERVICE-SCHEMA (defer), AUTHOR-URL-FIELD (~5 min, bundle into next content session), **SCHEMA-CORPORATE-HIERARCHY-FIX** (restructure chrome to the actual 3-tier BBI → Brant Basics → Office Central ownership; Steve-gated positioning call — surfaced by BLOG-1, the post body correctly describes the 3-tier structure which conflicts with the current 2-tier chrome).

**Defer / data-side:**
- F-5 root cause: vendor field re-attribution per SKU (large data project — separate workstream from schema)
- F-8 aggregateRating: requires actual reviews data first

---

## Appendix A — captured emitter inventory (raw)

All raw JSON-LD captures: [`data/audits/schema-audit-2026-05-27/captures/`](../../data/audits/schema-audit-2026-05-27/captures/)

Per-URL files: `{slug}.html` (raw HTML) + `{slug}.jsonld.json` (parsed JSON-LD blocks)
Summary index: `_summary.json`
Validator output: `validation-issues.json`

## Appendix B — validator notes

The Python validator (`validate.py`) over-reports on `hasOfferCatalog` nested Offer/Product references (Google guidelines explicitly permit lightweight `Product` stubs inside OfferCatalog). The CRIT/WARN counts in the raw output (2512 total) are inflated by this — real issue count is reflected in the Phase 4 matrix (5 CRIT + 5 HIGH + 6 MED + 3 POLISH = 19 distinct fix items).

## Appendix C — totals

- **Emitter files cataloged:** 12 (3 sitewide + 9 section-level)
- **Dead-code files:** 1 (`booster-seo.liquid`)
- **Surfaces validated on LIVE:** 23 URLs
- **Distinct fix items recommended:** 19
- **Time spent on audit:** ~40 minutes
- **No theme writes performed.**

---

## Branch + commit info

Branch: `feature/schema-audit-2026-05-27` (off `feature/post-steve-cleanup-2026-05-27` @ `119ac93`).
Commit will be created with this audit document + validation artifacts.

---

## Addendum — 2026-05-27 ~15:06 EDT — F-15 reclassification

**Author:** Claude under Leo's direction, post-SCHEMA-CRIT-1 Fix 1 Rich Results Test verification.
**Trigger:** Google Rich Results Test run on `https://www.brantbusinessinteriors.com/products/obusforme-comfort-high-back-chair-fabric-1240-3` and `https://www.brantbusinessinteriors.com/pages/oecm` via [search.google.com/test/rich-results](https://search.google.com/test/rich-results).

### Finding F-15 was misclassified

The original audit (Phase 1, line 146) stated:

> F-15. `hasOfferCatalog` in `bbi-org-schema` uses lightweight `{"@type":"Product","name":"Seating"}` items. **Acceptable per Google guidelines** (lightweight references, not full Product nodes). **NOT a defect.**

That assessment was wrong. Google's Rich Results Test, run on a real BBI page on 2026-05-27 ~15:06 EDT, returned **8 invalid Product snippets** with the error:

> "Either 'offers', 'review' or 'aggregateRating' should be specified."

The 8 items map exactly to the 8 categories in `bbi-org-schema.liquid`'s `hasOfferCatalog` block: Seating, Tables, Storage & Filing, Desks & Workstations, Boardroom Furniture, Ergonomic Products, Panels & Room Dividers, Quiet Spaces & Acoustic Pods.

### Why the audit was wrong

The audit assumed Google's documentation about "lightweight references inside `hasOfferCatalog`" meant Google's validator would treat them as references rather than Product instances. **It does not.** Google's validator parses every `{"@type": "Product"}` node — whether nested in `hasOfferCatalog` or top-level — as a Product entity that must satisfy Product validation rules. Lightweight nesting is a *schema.org pattern* but not a Google validator carve-out.

### Reclassification

| Field | Original audit | Reclassified |
|---|---|---|
| Severity | NOT a defect | **CRITICAL — invalid schema sitewide** |
| Scope | bbi-org-schema only | **Every page that includes `bbi-org-schema` chrome** (i.e. every `bbi_landing`-gated page — homepage, all PDPs, all collections, all `/pages/*` BBI landing pages). Confirmed visible on at minimum 1 PDP + 1 page; almost certainly sitewide. |
| Rich result impact | Assumed none | Blocks the affected pages from being treated as clean Product/Organization snippet sources by Google. 8 invalid Product nodes per page is a meaningful entity-graph noise signal. |
| Fix tracking | None | **SCHEMA-CRIT-NEW-1** (Tier 1, in `BBI-Session-Kickoff/bbi-build-state.md` Day 13 evening entry) |

### Follow-up

SCHEMA-CRIT-NEW-1 (full scope in build-state) will diagnose the emitter, choose between `OfferCatalog`-typed items / `ItemList` / minimal-offers Product, apply the fix under the standard approval gate, and re-verify on the same 2 RRT URLs. This work is **blocked on WATCHER-FORENSICS-AND-PROCESS-RECOVERY** landing first.

### Resolution — 2026-05-27 late-night

**F-15 RESOLVED.** SCHEMA-CRIT-NEW-1 shipped under branch `feature/schema-crit-new-1-2026-05-27` (PR #31, off PR #30 tip).

**Resolution method:** Path C deletion — removed the `hasOfferCatalog` block from [`theme/snippets/bbi-org-schema.liquid`](../../theme/snippets/bbi-org-schema.liquid) lines 50-63 (14 lines, 913 bytes). Not a refactor.

**Reasoning:** positive-evidence gap confirmed across RRT output (block produced 0 detected items, only the 8 errors), audit doc Phase 2 eligibility table (no rich result credited to the block), build-state references (no measured AI-crawler citation outcome), code provenance (stated intent only — "AI-4: required for Google AI Overview / entity clarity"), and schema.org/Google rich-result documentation (no SERP feature triggered by `Organization.hasOfferCatalog`). Per the "don't refactor what doesn't earn" criterion, deletion is the cleanest fix. Reversible — if future GSC or AI-crawler analysis demonstrates measurable benefit, the block can be reintroduced as a Path B nested OfferCatalog with verified collection URLs under its own scoped task.

**Verification:** 6 storefront surfaces cache-busted (OECM, ObusForme PDP, /collections/seating, /pages/healthcare, /pages/brands-keilhauer, homepage) — `@Product` node count dropped from 8 per surface to 0 (non-PDP) / 1 (PDP, the legitimate main product). RRT confirmed on OECM + PDP: 7 valid items, 0 invalid (was 8 invalid yesterday). Theme check held at 2850/166. CRIT-1 Fix 1 (PDP breadcrumb position-2 URL) preserved — no regression.

### Methodology note for future audits

The Phase 2 "Rich Results eligibility (per surface)" table (Phase 2, lines 158-170) was assessed by manual review of captured JSON-LD against documented Google requirements. It did NOT include running Google's actual Rich Results Test on representative URLs. That methodology gap is what allowed F-15's misclassification to land. Any future schema audit should treat manual review as a hypothesis-generator and require at least one real RRT run per surface class before publishing eligibility verdicts.

---

## Addendum — 2026-05-28 — SCHEMA-CRIT-3 resolution (F-10 / C-2) + new finding SCHEMA-CRIT-4

**Author:** Claude under Leo's direction. Branch `feature/schema-crit-3-2026-05-28` (off `feature/schema-crit-2-2026-05-28` @ `7f205da`, PR #33 tip), PR #34.

### F-10 / C-2 RESOLVED — summary ItemList + CollectionPage on 3 collection templates

Shipped summary `ItemList` wrapped in `CollectionPage` via new shared snippet `theme/snippets/bbi-itemlist-jsonld.liquid`, render-called inside the `{% paginate %}` block of all 3 collection sections: `ds-cc-base.liquid` (~9 category), `ds-cs-base.liquid` (91 sub-collections), `ds-collection-base.liquid` (109 default) = ~209 published collections.

- **Structure:** summary ListItems (`position` + `url` + `name`), **NO inline Product type** → no `offers`/`review`/`aggregateRating` required → sidesteps the F-15 trap by design. `CollectionPage` wraps `ItemList` via `mainEntity`. Page-scoped (reflects current paginated page's displayed products), capped 30, `position_offset = paginate.current_offset` for correct cross-page ranks (verified LIVE: sub-collection p2 = positions 25–48).
- **Eligibility correction (carries the audit's own methodology lesson):** finding F-10 / C-2 / TL;DR #2 all asserted "product carousel rich result" eligibility. **That was WRONG.** Google's ItemList carousel is restricted to **Course/Movie/Recipe/Restaurant**; products/e-commerce collections are **not supported** (verified against Google carousel docs 2026-05-28). There is no product-carousel SERP feature to earn — this is a **category limitation, not a markup gap.** CRIT-3's value is **entity-graph/AEO only**: CollectionPage typing + machine-readable product enumeration for Google index understanding + AI-crawler grounding (same value tier as CRIT-2). This is the second eligibility over-claim in this audit (after F-15) — reinforces the methodology note above: verify the rich-result type actually exists for the content vertical before claiming it.
- **Verified clean:** 3 structural variants cache-busted + RRT spot-checked. CRIT-3's own schema = 0 Product nodes, 0 errors, `numberOfItems` matches displayed count, chrome + BreadcrumbList + FAQPage intact (no regression). Theme check 2850/166. Commit `cee7f57`, PR #34.

### SCHEMA-CRIT-4 ✅ RESOLVED 2026-05-29 (strip)

**[RESOLVED 2026-05-29 — stripped all 7 `Product`/`Offer` microdata attributes/elements from the `ds-cs-base.liquid` product-card (itemscope+itemtype on `<article>`, itemprop=brand/name/url on the body, itemprop=offers+itemscope+itemtype on the price `<p>`, plus full-line deletion of the `priceCurrency` + `price` `<meta>` tags), matching the already-clean `ds-cc-base` + `ds-collection-base` card pattern. STRIP chosen over GUARD because CRIT-3's CollectionPage+ItemList already enumerates products at the collection level, making per-card Product microdata redundant in addition to buggy. Branch `feature/schema-crit-4-2026-05-29`. RRT on `medium-back-seating` (the discovery page): "53 items / 48 invalid" → "5 valid / 0 errors" — Product snippets AND Merchant listings rows vanished entirely (no Product schema = no Product row). Confirmed identical on `task-chairs` + `boardroom-conference-meeting` (mixed buyable+quote). Blast radius corrected to 67 published sub-collections on `template_suffix=base`. Behavioral: `data-vendor` (JS filter) + `is_quote_only` branch preserved; theme check held 2833/165. **CRIT-4 Phase 1 ACTION ITEM closed: PDP (`bbi-product-jsonld.liquid`) was always quote-aware — no parallel fix needed.** See build-state Day 15 SCHEMA-CRIT-4 entry.]**

**`ds-cs-base` product-card `Product` microdata invalid on quote-only products.** The `ds-cs-base.liquid` product-card `<article>` (line 497) carries `itemscope itemtype="https://schema.org/Product"` with `itemprop` name/brand; the `Offer` block (line 529, `itemprop="offers"` + price/priceCurrency) renders **only in the buyable branch.** For quote-only products (price=0 / unavailable) the card emits a **bare Product with no offers** → RRT error `"offers/review/aggregateRating should be specified"` (+ invalid Merchant listing).

- **PRE-EXISTING, not a CRIT-3 regression** — present in pre-session backup `data/backups/2026-05-28-schema-crit-3/ds-cs-base.liquid` line 497; CRIT-3's diff only added the ItemList render call, untouched card markup.
- **Confirmed on LIVE:** medium-back-seating page 1 = all 24 products quote-only → 24 bare Products → 24 invalid Product snippets (RRT also double-counts as 24 invalid Merchant listings).
- **Blast radius:** 91 published sub-collections render via `ds-cs-base`; severity scales with quote-only ratio (high for BBI's quote-heavy B2B catalog). `ds-cc-base` + `ds-collection-base` card markup is clean (0 microdata, plain HTML anchors).
- **Fix-vs-strip decision** (gate `itemscope` on `is_quote_only == false`, OR strip card microdata to match the two clean templates) belongs in its own session with RRT re-verify across the buyable/quote-only split. ~30-45 min.
- **CRIT-4 Phase 1 ACTION ITEM:** check whether PDP/product-detail templates have the same bare-Product-on-quote-only pattern — if the card microdata was copied from a product-page partial, the same bug likely exists on product detail pages (higher priority than collection cards if so).

### Root-pattern note — 🏁 HISTORICALLY RESOLVED 2026-05-29 (all 3 surfaces closed)

**Product schema emitted without required offers on quote-only B2B products** — a B2B-dealer-specific bug class born from a quote-heavy catalog interacting with theme markup that assumed every product has a buyable offer (false for BBI). It appeared in **three syntaxes**, now resolved in all three:
1. **F-15 / CRIT-NEW-1** — JSON-LD `hasOfferCatalog` Product stubs → **resolved 2026-05-27 by deletion.**
2. **CRIT-4** — HTML microdata `itemscope` Product cards on `ds-cs-base` → **resolved 2026-05-29 by strip.**
3. **PDP** — `bbi-product-jsonld.liquid` Product emitter → **was always quote-aware / correctly defensive from the start** (guards on `price==0`/availability; confirmed by the CRIT-4 Phase 1 diagnosis). (CRIT-3's summary ItemList also avoids this by emitting no Product type at all.)

**Architectural completion:** canonical pattern is now CollectionPage + ItemList for collection enumeration (no per-card Product) and a quote-aware Product emitter on the PDP. **Predictive value retained:** anywhere the theme emits Product schema (JSON-LD *or* microdata), verify it handles the quote-only case before declaring it valid. No known 4th surface remains.

---

## Addendum — 2026-05-28 — SCHEMA-H-1 resolution (F-4) + new finding F-LOCALBUSINESS-IMAGE

**Author:** Claude under Leo's direction. Branch `feature/schema-polish-1-2026-05-28` (off `feature/schema-crit-1b-2026-05-28` @ `d44debe`, PR #36 tip). Run as the SCHEMA-POLISH-1 + SCHEMA-H-1 session.

### F-4 RESOLVED on oecm + quote (SCHEMA-H-1)

Both inline `provider` LocalBusiness redeclarations (`ds-lp-oecm.liquid` GovernmentService node, `ds-lp-quote.liquid` Service node) converted to `{"@id": "https://{{ shop.permanent_domain }}/#organization"}`. **LocalBusiness node count 3→2 per page** (standalone inline duplicate eliminated; `provider` resolves to the canonical `#organization` entity). Clean swap, no property loss (the `#organization` node is a strict superset of the inline block). Shipped under full discipline: preflight PASS, drift IDENTICAL, post-PUT byte-compare IDENTICAL, theme check 2833/165 held, sibling schema (GovernmentService/Service, FAQPage, chrome) intact, storefront RRT confirms 2 nodes (was 3). **The other F-4 instance — `BlogPosting.publisher` in `ds-article.liquid` — was found to ALREADY carry the `@id` ref (no-op, dropped).**

### F-4 ≠ the recurring "Local businesses non-critical" WARN — they were conflated

The original H-1 framing (and the Phase 4 prediction this session) assumed fixing F-4 would clear the RRT "Local businesses — Non-critical issues detected" WARN. **It did not, and was never going to.** Post-H-1 RRT on both pages (2026-05-28) confirmed the WARN persists. F-4 (duplicate *entity*, now fixed) and the WARN (missing *recommended field* on the LocalBusiness type) are distinct findings. Methodology lesson (3rd in this audit, after F-15 and F-10 eligibility over-claims): **verify which finding a given RRT message maps to before predicting a fix will clear it.**

### F-LOCALBUSINESS-IMAGE (NEW finding) — ✅ RESOLVED 2026-05-29

> **✅ RESOLVED 2026-05-29 (branch `feature/f-localbusiness-image-2026-05-29`, off `main`).** `image` ImageObject added to BOTH chrome LocalBusiness nodes (`bbi-org-schema.liquid` `#organization` after `logo`; `bbi-localbusiness-schema.liquid` `#localbusiness` after `url`) — identical `{"@type":"ImageObject","url":".../bbi-about-grid-01-storefront-day.jpg","width":800,"height":600}` on both (entity-graph consistency). Photo: day storefront (#2 from About Us inventory; Steve categorically approved all About Us photos Day 15). **RRT (3 pages incl. `/pages/oecm`): Local businesses non-critical reduced 3 → 1** (now `priceRange`-only on `#organization` — the M-2 deliberate asymmetry, see below); **Organisation row CLEARED sitewide** (bonus — `image` was flagged at BOTH type-rows of the dual-typed `#organization` node; per-type field-checks, not per-entity). 0 errors; item counts intact (5 collection/OECM, 7 PDP). No regression (CRIT-1b/1c, CRIT-3/4, BRAND-1 all intact). Theme check held 2833/165. See Day 16 build-state. **The recurring "Missing field 'image'" non-critical is now gone from every RRT result sitewide.**

**Both sitewide chrome LocalBusiness nodes lack the recommended `image` field** → RRT `Missing field "image" (optional)` non-critical WARN, **sitewide** (every `bbi_landing` page renders the chrome).

- **Nodes:** `#organization` (combined `["Organization","LocalBusiness"]`, `bbi-org-schema.liquid`) and `#localbusiness` (dedicated, `bbi-localbusiness-schema.liquid`).
- **Confirmed 2026-05-28** via RRT on `/pages/oecm` + `/pages/quote` — WARN appears on BOTH nodes, including `#localbusiness` which already has `priceRange:"$$"` → **definitively `image`, NOT priceRange (M-2 ruled out), NOT review (F-8), NOT the F-4 duplicate.**
- `#organization` carries `logo` (an Organization-type ImageObject) but **not** the LocalBusiness `image` field — RRT counts them separately.
- **Fix:** add `image` (absolute URL to a representative business photo — storefront / install / team / product, **not the logo**) to both chrome emitters; sitewide blast radius clears the WARN everywhere at once.
- **Priority: LOW** — non-critical/optional, **zero rich-result impact** (LocalBusiness is not a Google rich-result type for BBI). **Likely Steve-gated** (needs a real image asset chosen). ~15-20 min once a URL is picked.
- **⬆️ ELEVATED RELEVANCE 2026-05-29 (post-SCHEMA-CRIT-1c):** with CRIT-1 now fully closed and CRIT-1c's Merchant-listings WARN reduced to deliberate monetary omissions, **F-LOCALBUSINESS-IMAGE is now the most likely cause of any residual "non-critical" WARN on a PDP RRT** (the PDP renders the sitewide chrome, so the `#localbusiness`/`#organization` missing-`image` WARN shows there too). Flagged for the next Steve cycle — picking one business image asset clears the last addressable non-critical WARN sitewide. (Remaining PDP non-criticals after that are F-8 review/aggregateRating, which need real review data, and the deliberate CRIT-1c monetary omissions.)
