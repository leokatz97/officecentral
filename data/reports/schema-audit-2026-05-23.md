# BBI Sitewide Schema Audit — 2026-05-23

**Step 36b — Read-only audit. No theme writes. Surfaces JSON-LD gaps across the BBI theme so they can be batch-fixed in a single follow-up session.**

Per Day 9 plan 2026-05-23. Auditor: Claude Code (Opus 4.7). Source of truth: `theme/` directory in this repo, which is in sync with DEV theme `186373570873` (BBI Landing Dev).

---

## Executive Summary

- **Page types audited:** 14 (homepage, PDP, 9 category collections + base, brand pages × 6 + brands hub, 10 landing pages, article, blog list, contact, search, customers ×7, cart, 404, password layout)
- **Schemas currently present (live, BBI-routed):** 6 distinct types — Organization+LocalBusiness (combined `@graph`), Product, BreadcrumbList, FAQPage, GovernmentService, HowTo, Service
- **HIGH severity gaps:** **4** (BlogPosting on article template; WebSite+SearchAction sitewide; LocalBusiness as a dedicated emission on /pages/contact; Service schema on /pages/delivery + /pages/relocation)
- **MED severity gaps:** **3** (ItemList on category pages; BreadcrumbList JSON-LD on landing pages with visible crumbs; Service-page Service schema for design-services if HowTo isn't recognised)
- **LOW severity gaps:** **3** (ItemList of BlogPosting on blog list; Brand subtype Organization on brand pages; potential Blog schema on blog list)
- **Validation issues on present schemas:** **3** (broken Article block in `meta-tags.liquid` firing on blog index with unset variables; potential double-Product emission if `settings.seo_microdata` is falsy; Organization+LocalBusiness combined `@type` array fires on every BBI page including PDPs — unusual but valid)
- **Orphan file:** `theme/snippets/booster-seo.liquid` is never rendered — contains an Organization+WebSite+Article+Blog+Product implementation that does not emit. Worth either deleting or repurposing (cheapest source of WebSite+SearchAction sitelinks search box).

**Net read:** schema coverage is genuinely strong on the **landing pages and PDPs** that AI-3 / AI-4 / AI-5 / AI-6 / AI-8 / AI-9 explicitly touched. The biggest pre-launch gap is **BlogPosting on `ds-article.liquid`** (AI-5 known) and **WebSite+SearchAction sitewide** (never wired). LocalBusiness *is* present on every BBI page via the combined Organization+LocalBusiness `@graph` in `bbi-org-schema`, which technically satisfies LocalBusiness rich-result requirements but is non-standard placement.

---

## Coverage Map (page type × schema type)

Legend: ✅ present · ❌ missing · ⚠ present but validation issue · N/A not applicable · ➕ present via sitewide org snippet (`bbi-org-schema` rendered from `bbi-nav`)

| Page type | Org+LocalBus (`@graph`) | WebSite+SearchAction | Product | Offer | BreadcrumbList | FAQPage | Service / GovernmentService / HowTo | BlogPosting / Article | ItemList | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Homepage (`index.json`) | ➕ | ❌ | N/A | N/A | ❌ | N/A | N/A | N/A | ❌ | Org+LocalBus via `bbi-nav-wrap` → `bbi-nav` → `bbi-org-schema` |
| PDP (`product.json` → `ds-pdp-base`) | ➕ | ❌ | ✅ | ✅ (nested) | ✅ (4-level) | N/A | N/A | N/A | N/A | Custom `bbi-product-jsonld` + nested BreadcrumbList |
| Category pages (`collection.*.json` → `ds-cc-base`) × 9 | ➕ | ❌ | N/A | N/A | ✅ (2 or 3 level) | ✅ | N/A | N/A | ❌ | FAQPage from blocks; BreadcrumbList from `bbi-breadcrumb-jsonld` |
| Sub-collection / customer-stories (`ds-cs-base`) | ➕ | ❌ | N/A | N/A | ✅ | N/A | N/A | N/A | ❌ | |
| Brand pages × 6 + brands hub | ➕ | ❌ | N/A | N/A | ❌ | N/A | N/A | N/A | ❌ | No JSON-LD beyond sitewide Org |
| `/pages/oecm` (`ds-lp-oecm`) | ➕ | ❌ | N/A | N/A | ❌* | ✅ | ✅ GovernmentService (verified) | N/A | N/A | *Visible `bbi-crumbs` present, no JSON-LD twin |
| `/pages/design-services` (`ds-lp-design-services`) | ➕ | ❌ | N/A | N/A | ❌* | ✅ | ✅ HowTo | N/A | N/A | *Visible crumbs only |
| `/pages/quote` (`ds-lp-quote`) | ➕ | ❌ | N/A | N/A | ❌* | ✅ | ✅ Service | N/A | N/A | *Visible crumbs only |
| `/pages/delivery` (`ds-lp-delivery`) | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ Service (HIGH) | N/A | N/A | *Visible crumbs only |
| `/pages/relocation` (`ds-lp-relocation`) | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ Service (HIGH) | N/A | N/A | *Visible crumbs only |
| `/pages/healthcare` | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ (industry; Service optional) | N/A | N/A | *Visible 3-level crumbs |
| `/pages/education` | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ | N/A | N/A | *Visible 3-level crumbs |
| `/pages/government` | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ | N/A | N/A | *Visible 3-level crumbs |
| `/pages/non-profit` | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ | N/A | N/A | *Visible crumbs |
| `/pages/professional-services` | ➕ | ❌ | N/A | N/A | ❌* | ❌ | ❌ | N/A | N/A | |
| `/pages/industries` (hub) | ➕ | ❌ | N/A | N/A | ❌* | ❌ | N/A | N/A | ❌ ItemList of industries | |
| `/pages/about` (`ds-lp-about`) | ➕ | ❌ | N/A | N/A | ❌* | ❌ | N/A | N/A | N/A | Org already on it |
| `/pages/our-work` | ➕ | ❌ | N/A | N/A | ❌* | N/A | N/A | N/A | ❌ ItemList of projects | |
| `/pages/customer-stories` | ➕ | ❌ | N/A | N/A | ❌* | N/A | N/A | N/A | ❌ ItemList | |
| `/pages/contact` (`ds-lp-contact`) | ➕ | ❌ | N/A | N/A | ❌* | N/A | N/A | N/A | N/A | LocalBusiness present via combined graph; no dedicated emission |
| `/pages/faq` (`ds-lp-faq`) | ➕ | ❌ | N/A | N/A | ❌* | ✅ (hardcoded Q&As) | N/A | N/A | N/A | |
| Article (`article.json` → `ds-article`) | ➕ | ❌ | N/A | N/A | ❌ | ⚠ (gated on `metafields.faq.items`) | N/A | ❌ **(AI-5 HIGH)** | N/A | One published article emits no Article schema |
| Blog list (`blog.json` → `ds-blog-list`) | ➕ | ❌ | N/A | N/A | ❌ | N/A | N/A | N/A | ❌ ItemList of posts | Also: ⚠ malformed Article block in `meta-tags.liquid` fires here (see Validation Issues) |
| Search (`search.json`) | ➕ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | |
| Customers × 7 (`customers/*.json`) | ➕ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Private, no schema needed |
| Cart (`cart.json`) | ➕ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Transactional, no schema needed |
| 404 (`404.json` → `ds-system-404`) | ➕ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | |
| Password layout (`layout/password.liquid`) | ❌ | ❌ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Stays gated, never indexed |

**Coverage totals:** 6 distinct schema types present somewhere · 8 page-type × schema-type cells are HIGH-severity missing · 17 are MED · 9 are LOW · roughly two dozen are appropriately N/A.

---

## Validation Issues on Present Schemas

### V-1 ⚠ HIGH — Broken Article block in `meta-tags.liquid` fires on blog INDEX page

**File:** [theme/snippets/meta-tags.liquid:46–78](theme/snippets/meta-tags.liquid)

The block is gated `{% if request.page_type == 'blog' %}` (the blog INDEX page, not the article page) but references `article.title`, `article.content`, `article.published_at`, `article.created_at`, `article.author`, `article.image`, `article.excerpt`, and `page.url` — all of which are unset on the blog index. Result: emits malformed JSON with `null`/empty values, plus the entire block is wrapped in `{% unless settings.seo_microdata %}` so its actual emission depends on the Shopify setting `seo_microdata`.

This is residual Avada theme code, not BBI-written. Fix in batch session: delete lines 46–78 (this whole `{% if request.page_type == 'blog' %}` branch). Replace with proper Blog/ItemList schema on `ds-blog-list.liquid` (LOW gap below).

```
{% if request.page_type == 'blog' %}    ← fires on blog INDEX, but...
  ...
  "headline": {{ article.title | json }},    ← article is unset here
  "articleBody": {{ article.content | strip_html | json }},
  "datePublished": {{ article.published_at | date: '%Y-%m-%dT%H:%M:%SZ' | json }},
  ...
{% endif %}
```

### V-2 ⚠ MED — Potential double-Product emission on PDPs

**File:** [theme/snippets/meta-tags.liquid:33–45](theme/snippets/meta-tags.liquid) + [theme/snippets/bbi-product-jsonld.liquid](theme/snippets/bbi-product-jsonld.liquid)

`meta-tags.liquid` emits `{{ product | structured_data }}` (Shopify's auto-generated Product schema) when `settings.seo_microdata` is falsy. `bbi-product-jsonld.liquid` always emits the BBI-authored Product schema on PDPs. If `settings.seo_microdata = true` (likely default for Avada themes), only the BBI version emits — fine. If `settings.seo_microdata = false/blank`, both emit, which is duplicate Product data that Google will pick one of (usually OK but flagged by validators).

**Verification needed:** confirm the value of `settings.seo_microdata` on DEV theme `186373570873`. If `true` (suppressing Shopify auto), no change needed. If `false`, either flip it to `true` or remove lines 34–45 from `meta-tags.liquid`.

### V-3 ⚠ LOW — Organization+LocalBusiness combined `@type` array fires sitewide

**File:** [theme/snippets/bbi-org-schema.liquid](theme/snippets/bbi-org-schema.liquid) (rendered from `bbi-nav.liquid:12` → fires on every page that includes the BBI nav, i.e. every BBI-routed page).

The snippet declares `"@type": ["Organization", "LocalBusiness"]` and emits full address + geo + opening hours on every page (homepage, PDPs, collections, articles, etc.). This is **valid schema** (a single entity *can* be both an Organization and a LocalBusiness), but it's non-standard placement — most sites emit a slim Organization sitewide and a richer LocalBusiness only on contact/homepage. Search engines tend to be fine with it. **No change required** unless a Search Console rich-results audit flags it. Listed here for completeness.

Sample emit (truncated):

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "LocalBusiness"],
      "@id": "https://www.brantbusinessinteriors.com/#organization",
      "name": "Brant Business Interiors",
      "alternateName": "BBI",
      ...
      "telephone": "+18008359565",
      "address": { "@type": "PostalAddress", "streetAddress": "296 George St N", ... },
      "geo": { "@type": "GeoCoordinates", "latitude": 44.3073, "longitude": -78.3197 },
      "openingHours": "Mo-Fr 08:30-17:00",
      "hasOfferCatalog": { ... 8 product categories ... }
    }
  ]
}
</script>
```

---

## HIGH Severity Gaps (pre-launch recommended)

### H-1 ❌ BlogPosting JSON-LD on `ds-article.liquid` *(AI-5 known gap)*

- **Page:** every article (`article.json` → `ds-article.liquid`) — currently 1 published article (*How to adjust your chair*) emits no Article-type schema, only the conditional FAQPage block at [ds-article.liquid:131–158](theme/sections/ds-article.liquid).
- **Why HIGH:** AI search engines (ChatGPT, Perplexity, Google AI Overview) rely on `BlogPosting` / `Article` schema to identify and cite blog content. Without it, the 2 cornerstone posts going live Day 10 (OECM for Ontario School Boards + Healthcare Furniture Compliance for FHTs) will publish without machine-readable author/publisher/date metadata. Big retrieval loss.
- **Estimated fix time:** ~25 min
- **File to edit:** [theme/sections/ds-article.liquid](theme/sections/ds-article.liquid) — add a `BlogPosting` block emitting `@type`, `headline`, `image`, `datePublished`, `dateModified`, `author` (Person), `publisher` (Organization with logo), `mainEntityOfPage`, and `articleBody` (using `article.*` Liquid object which IS set on this template).

### H-2 ❌ WebSite + SearchAction (sitewide sitelinks search box)

- **Page:** sitewide — would render once in `theme.liquid` head (or via the existing `meta-tags.liquid` snippet).
- **Why HIGH:** the `WebSite` schema with a `SearchAction` `target` is what triggers Google's site-link search box on the SERP for branded queries ("brant business interiors"). Easy win, missing entirely (currently only present in the never-rendered orphan `booster-seo.liquid:260–272`).
- **Estimated fix time:** ~10 min
- **File to edit:** either (a) extend [theme/snippets/meta-tags.liquid](theme/snippets/meta-tags.liquid) to add a small WebSite+SearchAction block, OR (b) lift the block out of `booster-seo.liquid` and put it in a new `bbi-website-schema.liquid` snippet rendered from `theme.liquid` head, OR (c) include it as a second graph entry inside `bbi-org-schema.liquid` (cleanest — one snippet, one `@graph`, sitewide).
- **Sample emit (proposed):**
  ```
  {
    "@type": "WebSite",
    "@id": "https://www.brantbusinessinteriors.com/#website",
    "url": "https://www.brantbusinessinteriors.com",
    "name": "Brant Business Interiors",
    "publisher": { "@id": "https://www.brantbusinessinteriors.com/#organization" },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://www.brantbusinessinteriors.com/search?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
  ```

### H-3 ❌ Service JSON-LD on `/pages/delivery` and `/pages/relocation`

- **Pages:** [ds-lp-delivery.liquid](theme/sections/ds-lp-delivery.liquid) + [ds-lp-relocation.liquid](theme/sections/ds-lp-relocation.liquid). Both render the visible page chrome (nav, crumbs, content) but emit no JSON-LD beyond the sitewide Organization+LocalBusiness.
- **Why HIGH:** `/pages/quote` already has `Service` ([ds-lp-quote.liquid:355–397](theme/sections/ds-lp-quote.liquid)) and `/pages/design-services` has `HowTo` ([ds-lp-design-services.liquid:14–28](theme/sections/ds-lp-design-services.liquid)). Delivery + relocation are the missing pair in the BBI service set — they're explicit B2B services with quantifiable parameters (service area, provider, lead time). Without `Service` schema, AI search retrieval for "office furniture delivery ontario" / "office relocation peterborough" loses BBI's entity signal.
- **Estimated fix time:** ~20 min (10 min each — clone the quote-page `Service` pattern)
- **Files to edit:** [theme/sections/ds-lp-delivery.liquid](theme/sections/ds-lp-delivery.liquid), [theme/sections/ds-lp-relocation.liquid](theme/sections/ds-lp-relocation.liquid). Mirror the `Service` + nested `LocalBusiness` provider from [ds-lp-quote.liquid:355–397](theme/sections/ds-lp-quote.liquid).

### H-4 ❌ Dedicated LocalBusiness on `/pages/contact`

- **Page:** [ds-lp-contact.liquid](theme/sections/ds-lp-contact.liquid). LocalBusiness *is* technically present via the sitewide combined `Organization+LocalBusiness` `@graph` (from `bbi-org-schema`), so this is borderline HIGH/MED. It's marked HIGH because contact is the page Google Business Profile linking, Local Pack inclusion, and "office furniture peterborough" local-intent queries pivot off — a richer LocalBusiness with `priceRange`, `paymentAccepted`, `currenciesAccepted`, `additionalType`, and explicit `contactPoint` (for ContactPage schema.org expected fields) is worth having.
- **Why HIGH:** local SEO + GBP linking.
- **Estimated fix time:** ~15 min
- **File to edit:** [theme/sections/ds-lp-contact.liquid](theme/sections/ds-lp-contact.liquid) — add a dedicated `LocalBusiness` JSON-LD block (or a `ContactPage` wrapper) at the top of the section, separate from the sitewide Org graph.

---

## MED Severity Gaps

### M-1 ❌ BreadcrumbList JSON-LD on landing pages with visible breadcrumbs

- **Pages:** all 14 `ds-lp-*` landing pages render `bbi-crumbs` (visible breadcrumb UI) but do NOT render `bbi-breadcrumb-jsonld` (the JSON-LD twin). Confirmed missing on: oecm, quote, design-services, delivery, relocation, healthcare, education, government, non-profit, professional-services, industries, about, our-work, customer-stories, contact, faq, and all 6 brand pages.
- **Why MED:** Google can render visible breadcrumbs in the SERP if the JSON-LD twin is present. It's already wired into PDPs (`bbi-product-jsonld` → `bbi-breadcrumb-jsonld`) and category pages (`ds-cc-base` → `bbi-breadcrumb-jsonld`). Missing on the landing pages is asymmetric.
- **Estimated fix time:** ~45 min (find/replace pattern — every `{%- render 'bbi-crumbs', ...` should be followed by a `{%- render 'bbi-breadcrumb-jsonld', ...` with mirrored fields). Could also be refactored so `bbi-crumbs` internally renders `bbi-breadcrumb-jsonld` once and is then a single call site.
- **Files to edit:** the 14 `ds-lp-*` sections + `ds-lp-about.liquid` + `ds-lp-contact.liquid` + brand pages, OR the cleaner refactor inside `bbi-crumbs.liquid` itself.

### M-2 ❌ ItemList on category pages (and on industries hub / our-work)

- **Pages:** all 9 category collection pages (`collection.*.json` → `ds-cc-base.liquid`), plus `/pages/industries` (hub of industry tiles), `/pages/our-work` (gallery), `/pages/customer-stories` (story tiles).
- **Why MED:** `ItemList` (with `ItemListElement` of `Product` for collections, or `WebPage` for hub pages) gives AI search a structured handle on "what's on this page". For category pages, this would expose the product grid as a machine-readable list distinct from the FAQPage. Not required for rich results (BreadcrumbList + FAQPage are doing the heavy lifting) but enhances retrieval.
- **Estimated fix time:** ~30 min (one block in `ds-cc-base.liquid` iterating `collection.products limit: 30` with `position`, `url`, `name`). Optional.
- **File to edit:** [theme/sections/ds-cc-base.liquid](theme/sections/ds-cc-base.liquid). Industries/our-work would need to enumerate the section blocks similarly.

### M-3 ❌ Service schema on `/pages/design-services` (HowTo only — borderline)

- **Page:** [ds-lp-design-services.liquid:14–28](theme/sections/ds-lp-design-services.liquid). The page emits `HowTo` (the 4-step "how to get a free design") + `FAQPage`. It does **not** emit `Service` despite being a service page.
- **Why MED:** Google's rich-result panel treats HowTo + Service as alternatives in many cases. HowTo is arguably the better match for this page (it's procedural — "how to get a free design"), so this is debatable. A second `Service` block in a `@graph` alongside the HowTo would unambiguously cover "office design services" as a queryable entity. Optional.
- **Estimated fix time:** ~10 min
- **File to edit:** [theme/sections/ds-lp-design-services.liquid](theme/sections/ds-lp-design-services.liquid). Wrap existing two `<script>` blocks in a single `@graph` and add a `Service` node.

---

## LOW Severity Gaps

### L-1 ❌ Blog + ItemList of BlogPosting on `ds-blog-list.liquid`

- **Page:** [ds-blog-list.liquid](theme/sections/ds-blog-list.liquid). Currently emits no JSON-LD at all (the malformed Article block in `meta-tags.liquid` doesn't count — it's broken).
- **Why LOW:** with 1 post live today and 2 more publishing Day 10, this is light. After Day 10 the post count is 3; once it hits 5+ a proper Blog `@type` with an `ItemListElement` of `BlogPosting` URLs becomes worth it. Currently low payoff.
- **Estimated fix time:** ~15 min
- **File to edit:** [theme/sections/ds-blog-list.liquid](theme/sections/ds-blog-list.liquid). Same time you delete the malformed `meta-tags.liquid:46–78` Article block (V-1).

### L-2 ❌ Brand subtype Organization on 6 brand pages

- **Pages:** the 6 brand landing pages (`ds-lp-brands-otg`, `-global-teknion`, `-heartwood`, `-keilhauer`, `-ergocentric`, `-obusforme`).
- **Why LOW:** these pages already get the BBI Org+LocalBusiness graph via `bbi-nav` (which is the seller, not the brand). A `Brand` or `Organization` JSON-LD for the actual manufacturer (Global Furniture Group, Teknion, etc.) on each page would clarify the brand entity to AI search. Cheap to add, low SEO impact since these pages aren't ranking for "global furniture group" — they're ranking for "office furniture peterborough".
- **Estimated fix time:** ~30 min (6 pages, ~5 min each)
- **Files to edit:** the 6 `ds-lp-brands-*.liquid` sections.

### L-3 ❌ ItemList on `/pages/industries` (already counted in M-2)

Same item as M-2; restating here so the count adds up. Counted once.

---

## Recommended Batch-Fix Session Scope

**Goal:** address all HIGH severity gaps + V-1 in a single ~1.5–2h Claude Code session before LAUNCH-2 (Day 11). MED + LOW are post-launch backlog.

| # | Item | Severity | Est. time | File(s) |
|---|---|---|---|---|
| 1 | **BlogPosting on `ds-article.liquid`** | HIGH (H-1) | ~25 min | `theme/sections/ds-article.liquid` |
| 2 | **WebSite + SearchAction sitewide** (extend `bbi-org-schema` `@graph`) | HIGH (H-2) | ~10 min | `theme/snippets/bbi-org-schema.liquid` |
| 3 | **Service on `/pages/delivery`** | HIGH (H-3) | ~10 min | `theme/sections/ds-lp-delivery.liquid` |
| 4 | **Service on `/pages/relocation`** | HIGH (H-3) | ~10 min | `theme/sections/ds-lp-relocation.liquid` |
| 5 | **Dedicated LocalBusiness on `/pages/contact`** | HIGH (H-4) | ~15 min | `theme/sections/ds-lp-contact.liquid` |
| 6 | **Delete malformed Article block in `meta-tags.liquid`** | V-1 (validation) | ~5 min | `theme/snippets/meta-tags.liquid:46–78` |
| 7 | **Verify `settings.seo_microdata` value on DEV** | V-2 (validation) | ~5 min | Shopify Admin → Theme settings |
| 8 | **Verify GovernmentService still emitting on `/pages/oecm`** *(per AI-8)* | sanity | ~5 min | rendered HTML inspection only |

**Total estimated batch time:** ~85 min (1.5h). Single PR via `feature/schema-batch-fix`, push to DEV theme `186373570873`, verify with rich-results test on a representative URL per page type.

### MED + LOW deferred to post-launch backlog
- M-1 BreadcrumbList JSON-LD on landing pages (~45 min refactor of `bbi-crumbs.liquid` is cleaner than 14 individual edits)
- M-2 ItemList on category pages + hub pages (~30 min, optional)
- L-1 Blog list schema (~15 min, payoff scales with post count)
- L-2 Brand subtype Organization on 6 brand pages (~30 min, optional)

---

## Wildcards Resolved

| Wildcard from prompt | Status | Notes |
|---|---|---|
| Product schema on PDPs | ✅ **PRESENT** (no risk) | Custom `bbi-product-jsonld` with Offer + Brand + 4-level BreadcrumbList + additionalProperty from `specs.*` metafields. Best in show. |
| Organization schema on `theme.liquid` | ✅ **PRESENT** | Via `bbi-nav` → `bbi-org-schema` on every BBI-routed page. Combined with LocalBusiness in a single `@graph` node. |
| Service schema on service pages | ⚠ **PARTIAL** | Quote ✅, Design-services ⚠ (HowTo only), Delivery ❌, Relocation ❌. Two HIGH gaps. |
| LocalBusiness on contact | ⚠ **PRESENT VIA GRAPH** | Sitewide combined emission satisfies the schema but `/pages/contact` deserves a dedicated, richer block. |
| GovernmentService on `/pages/oecm` | ✅ **PRESENT** | Verified at [ds-lp-oecm.liquid:296–337](theme/sections/ds-lp-oecm.liquid). AI-8 still holding. |
| Article/BlogPosting schema | ❌ **MISSING** | Confirms AI-5 known gap. Single HIGH item that affects Day 10 cornerstone posts. |

---

## Sample emit per present schema

For traceability — these are the exact emissions on the live DEV theme:

**Organization+LocalBusiness combined `@graph`** ([bbi-org-schema.liquid](theme/snippets/bbi-org-schema.liquid)): see V-3 above.

**Product** ([bbi-product-jsonld.liquid:49–151](theme/snippets/bbi-product-jsonld.liquid)):
```
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "<product.title>",
  "description": "<product.description | strip_html | truncate: 500>",
  "image": [up to 5 image URLs with https: prefix],
  "brand": { "@type": "Brand", "name": "<product.vendor>" },
  "sku": "<variant.sku>",
  "mpn": "<variant.sku>",
  "additionalProperty": [up to 11 PropertyValue entries from specs.* metafields],
  "offers": {
    "@type": "Offer",
    "url": "<shop.url + product.url>",
    "priceCurrency": "CAD",
    "price": "<variant.price / 100>",
    "availability": "https://schema.org/InStock|OutOfStock",
    "seller": { "@type": "Organization", "name": "Brant Business Interiors" }
  }
}
```

**BreadcrumbList** ([bbi-breadcrumb-jsonld.liquid](theme/snippets/bbi-breadcrumb-jsonld.liquid)): up to 4 ListItem entries, conditional on each `bcN_name`. Used in PDPs (4 levels), category pages (2 or 3 levels), customer-stories sub-pages.

**FAQPage** ([ds-cc-base.liquid:530–547](theme/sections/ds-cc-base.liquid), [ds-lp-oecm.liquid:322–334](theme/sections/ds-lp-oecm.liquid), [ds-lp-quote.liquid:385–399](theme/sections/ds-lp-quote.liquid), [ds-lp-design-services.liquid:31–42](theme/sections/ds-lp-design-services.liquid), [ds-lp-faq.liquid:138+](theme/sections/ds-lp-faq.liquid), [ds-article.liquid:131–158](theme/sections/ds-article.liquid)): standard Q/A mainEntity array. `ds-cc-base` and `ds-lp-oecm` / `ds-lp-quote` / `ds-lp-design-services` build from `section.blocks where type == 'faq_item'`. `ds-lp-faq` hardcodes the Q&As inline. `ds-article` reads from `article.metafields.faq.items.value`.

**GovernmentService** ([ds-lp-oecm.liquid:301–321](theme/sections/ds-lp-oecm.liquid)): Service with nested LocalBusiness provider + address. AI-8 verified.

**HowTo** ([ds-lp-design-services.liquid:14–28](theme/sections/ds-lp-design-services.liquid)): 4-step recipe with estimatedCost + totalTime.

**Service** ([ds-lp-quote.liquid:356–397](theme/sections/ds-lp-quote.liquid)): Service with nested LocalBusiness provider + Offer + serviceType.

---

## Orphan file note

`theme/snippets/booster-seo.liquid` (665 lines) exists but is never rendered (no `{% render 'booster-seo' %}` anywhere in `theme/`). Contains a complete Booster Apps SEO implementation: Organization, WebSite+SearchAction, Product, Blog, Article schemas, all gated on `booster_config.google_snippets_enabled`. Recommend deleting in the batch-fix session — its WebSite+SearchAction block can be lifted into `bbi-org-schema.liquid` (H-2 fix), and the rest is residual Avada / app vestige.

---

## Methodology

- **Templates enumerated:** `ls theme/templates/*.json theme/templates/customers/*.json` (43 + 7 = 50 templates).
- **JSON-LD emission tracing:**
  - Searched `theme/{sections,snippets,layout}` for `application/ld+json` (10 emitter files, plus the orphan booster-seo).
  - Traced render chains from `theme.liquid` (sitewide) → `meta-tags.liquid`, and from each section → `bbi-nav` / `bbi-org-schema` / `bbi-product-jsonld` / `bbi-breadcrumb-jsonld`.
  - Mapped which sections render `bbi-nav` (Organization+LocalBusiness carrier): all 31 `ds-*` sections + `bbi-nav-wrap` section.
- **Per-template inspection:** read the JSON template + the referenced section file for each unique page type. Confirmed `bbi_landing` gate coverage in `theme.liquid:93–159`.
- **Read-only:** zero theme writes. Zero PRs. Single docs-only commit to `main` carrying this report.

---

*End of audit.*
