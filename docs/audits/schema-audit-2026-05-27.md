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
2. **Collection pages emit NO `ItemList` / `CollectionPage` schema.** Product carousel rich result not eligible on any of ~22 collection pages.
3. **Industry / segment landing pages emit NO surface-specific schema.** Healthcare, Education, Government, Non-Profit, Professional Services, Industries Hub all rely on chrome only — no `Service`, no `WebPage`, no `ItemList`. These are the most strategically important pages for OECM-driven B2B SEO.
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
  - `ds-lp-oecm`, `ds-lp-quote` redeclare full `LocalBusiness` inline as `provider` instead of referencing `…/#localbusiness` — produces 3rd LocalBusiness instance per page. **WARN.**
  - `ds-article.liquid` `BlogPosting.publisher` redeclares Organization fields rather than `@id`-referencing. **WARN.**

**F-5. PDP `brand.name` falls back to `product.vendor`.** `product.vendor` is set to "Brant Business Interiors" on many SKUs (vendor = dealer, not manufacturer). Confirmed on `dual-monitor-arm` PDP — actual manufacturer is Fellowes (per description text), but emitted brand is "Brant Business Interiors". **CRIT — incorrect brand attribution.**

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

**F-8. `Product` has no `aggregateRating` / `review`.** No review data in store — not a defect per se, but blocks Review rich result.

**F-9. PDP `seller` is a 4th Organization node.** `offers.seller` declares a new `Organization` inline rather than referencing `#organization` via `@id`. WARN — duplicate entity.

**F-10. Collection pages have no `ItemList` / `CollectionPage`.** Listed products are absent from structured data. Blocks product-carousel rich results.

**F-11. Blog landing (`/blogs/news`) emits no `Blog` schema.** `ds-blog-list.liquid` does not emit `Blog` or `CollectionPage`. Individual articles do emit `BlogPosting` (via `ds-article.liquid`).

**F-12. Industry segment pages emit no `Service` / `WebPage` / `ItemList`.** Healthcare, education, government, non-profit, professional-services, industries hub — all chrome-only. These are the most strategically important B2B SEO pages and should emit `Service` (institutional procurement) with `serviceType`, `areaServed`, and ideally an `OfferCatalog` of representative product categories.

**F-13. Brand manufacturer pages emit no `Brand` schema.** `/pages/brands-ergocentric`, `…-global-teknion`, `…-heartwood`, `…-keilhauer`, `…-obusforme`, `…-otg` — no Brand or Organization schema for the featured manufacturer. Should emit a `Brand` (or `Organization` if appropriate) with `manufacturer` relationship + `subjectOf` linking BBI.

**F-14. About + Contact pages emit no `AboutPage` / `ContactPage`.** These are weak signal classes but cheap to add and aid entity disambiguation.

**F-15. `hasOfferCatalog` in `bbi-org-schema` uses lightweight `{"@type":"Product","name":"Seating"}` items.** Acceptable per Google guidelines (lightweight references, not full Product nodes). NOT a defect.  **[RECLASSIFIED 2026-05-27 ~15:06 — MISCLASSIFIED. Google's Rich Results Test flags all 8 items as invalid Product snippets ("Either 'offers', 'review' or 'aggregateRating' should be specified"). See Addendum at end of document. Tracked as SCHEMA-CRIT-NEW-1.]**

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
| C-3 | Fix PDP `brand.name` data attribution (F-5). Schema-side fallback: prefer `product.metafields.specs.manufacturer` over `product.vendor`. (Data-side fix — re-attributing `product.vendor` per SKU — is separate and large.) | `theme/snippets/bbi-product-jsonld.liquid:60-65` | S | H — corrects SERP brand display on all enriched PDPs | LOW | depends on specs metafield population (Hero 100 already covered) |
| C-4 | Add `Service` schema to industry/segment landing pages (F-12). One reusable snippet `bbi-service-jsonld.liquid` rendered from healthcare/education/government/non-profit/professional-services/industries sections. Mirror `ds-lp-delivery.liquid` pattern with `@id` ref to `#organization`. | new snippet + 6 section renders | M | H — eligibility + AI-crawler grounding for highest-value B2B pages | LOW | — |
| C-5 | Add Merchant Listing fields to PDP `offers` (F-7): `priceValidUntil` (computed: today + 90d), `itemCondition: NewCondition`, `hasMerchantReturnPolicy` (`MerchantReturnPolicy` with 30-day window or "Contact for return" per BBI policy — confirm w/ Steve), `shippingDetails` (`OfferShippingDetails` w/ Ontario region + "Contact for quote" handling time). | `theme/snippets/bbi-product-jsonld.liquid:131-149` | M | H — unlocks Merchant Listings rich result on all PDPs | LOW (schema-only) | Steve confirms return + shipping policies |

### HIGH-IMPACT

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| H-1 | Convert inline `provider` redeclarations in OECM + Quote sections to `@id` references (F-4). Match the relocation/delivery pattern. Removes 1 extra LocalBusiness node per page. | `ds-lp-oecm.liquid:304-317`, `ds-lp-quote.liquid:363-376` | S | M — entity-graph clarity, mild AI-crawler benefit | LOW | C-4 prep work |
| H-2 | Add `Blog` schema to blog landing page (F-11). `Blog` with `mainEntityOfPage`, `publisher` `@id`-ref to `#organization`. | `theme/sections/ds-blog-list.liquid` | S | M — blog hub eligibility, AI crawler grounding | LOW | — |
| H-3 | Add `Brand` (or `Organization` w/ `manufacturer` relationship) schema to 6 manufacturer pages (F-13). Per-brand: name, logo, URL, parentOrganization (BBI as seller). | new snippet `bbi-brand-jsonld.liquid` + 6 section renders | M | M — manufacturer-page SEO + Brand knowledge-panel eligibility | LOW | — |
| H-4 | Convert PDP `offers.seller` to `@id` reference (F-9). Remove inline Organization redeclaration. | `bbi-product-jsonld.liquid:145-148` | S | L-M — entity-graph clarity | LOW | — |
| H-5 | Format-match Source: always-on `FAQPage` on category pages, with 3 default Q&As if `faq_item` blocks empty (F-3 from Phase 3). | `ds-cc-base.liquid` | S | M — AI Overview citation play on ~22 category pages | LOW | — |

### MEDIUM-IMPACT

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| M-1 | Add `AboutPage` / `ContactPage` schema (F-14). Single page each, wraps existing entity reference. | `ds-lp-about.liquid`, `ds-lp-contact.liquid` | S | L-M — entity disambiguation signal | LOW | — |
| M-2 | Add `priceRange: "$$"` to combined Org+LocBus in `bbi-org-schema` (F-16). Match dedicated emitter. | `bbi-org-schema.liquid:40` (insert after `openingHours`) | S | L | LOW | — |
| M-3 | Convert `BlogPosting.publisher` to `@id` reference (F-4). | `ds-article.liquid:168-178` | S | L | LOW | — |
| M-4 | Add `agreementID` or `Certification` for OECM 2025-470 (F-3). `GovernmentService.identifier` or sub-typed certification. | `ds-lp-oecm.liquid` | S | L — explicit OECM signal | LOW | — |
| M-5 | Add `Article` schema to customer-story pages (`/pages/customer-stories`). Each story → ItemList of Article references. | `ds-lp-customer-stories.liquid` | M | L-M — content-page SEO | LOW | content structure review |
| M-6 | Add `OfferCatalog` to industry-page Services (companion to C-4). Each Service includes representative product categories. | within C-4 service snippet | S | M | LOW | depends on C-4 |

### POLISH

| # | Fix | Where | Effort | Impact | Risk | Deps |
|---|---|---|---|---|---|---|
| P-1 | Delete dead `booster-seo.liquid` snippet (F-6 from inventory). 5 unrendered JSON-LD blocks that would emit duplicate Organization + WebSite + Product if reactivated. | `theme/snippets/booster-seo.liquid` | S | L (footgun removal) | LOW | confirm no obscure `render` call exists |
| P-2 | Update `bbi-localbusiness-schema.sameAs` once social profiles launch (F-17). | `bbi-localbusiness-schema.liquid:51` | S | L | LOW | Steve to confirm social URLs |
| P-3 | Add `image` to `HowTo` schema on design-services page (Phase 1 WARN). | `ds-lp-design-services.liquid:14-29` | S | L | LOW | — |

---

## Suggested execution order

**Session 1 — CRIT batch (~60-90 min, single PR):**
- C-1 (breadcrumb URL fix) — debug + 1-line snippet patch
- C-3 (brand.name fallback) — 4-line snippet patch
- C-5 (Merchant Listing fields) — confirm policies with Steve, then snippet edit
- P-1 (delete booster-seo dead code) — bundled cleanup

PR title: `SCHEMA-CRIT-1: fix PDP breadcrumb URL + brand fallback + Merchant Listings + remove dead booster-seo`

**Session 2 — Industry/segment schema (~90-120 min, single PR):**
- C-4 (new `bbi-service-jsonld` snippet + 6 industry pages)
- H-1 (OECM/Quote provider @id refs — done at same time since pattern matches)
- M-6 (OfferCatalog within industry Services)

PR title: `SCHEMA-CRIT-2: Service schema for industry pages (healthcare/education/government/non-profit/professional-services/industries)`

**Session 3 — Collection schema + format-match Source (~60-90 min):**
- C-2 (ItemList / CollectionPage on collections)
- H-5 (always-on FAQPage on collections with defaults)

PR title: `SCHEMA-CRIT-3: ItemList + always-on FAQPage on collection pages`

**Session 4 — High-impact polish (~45-60 min):**
- H-2 (Blog landing schema)
- H-3 (Brand pages × 6)
- H-4 (PDP seller @id ref)
- M-1, M-2, M-3, M-4 (entity polish batch)

PR title: `SCHEMA-POLISH-1: blog/brand pages + entity-graph cleanup`

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

### Methodology note for future audits

The Phase 2 "Rich Results eligibility (per surface)" table (Phase 2, lines 158-170) was assessed by manual review of captured JSON-LD against documented Google requirements. It did NOT include running Google's actual Rich Results Test on representative URLs. That methodology gap is what allowed F-15's misclassification to land. Any future schema audit should treat manual review as a hypothesis-generator and require at least one real RRT run per surface class before publishing eligibility verdicts.
