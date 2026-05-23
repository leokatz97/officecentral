# BBI SYS-VERIFY-1 Phase 2 — 2026-05-24

Final pre-launch verification gate for Monday LAUNCH-2.
Read-only audit across 6 categories. No theme writes, no Admin changes.

---

## Executive Summary

- **Audit duration:** ~75 minutes
- **Repo HEAD at start:** `2ea7835` (linear tracker restructure)
- **DEV theme:** `186373570873` (BBI Landing Dev, unpublished, last updated 2026-05-22)
- **LIVE theme:** `178274435385` (BBI Live, main/published — still the older Avada+BBI hybrid that LAUNCH-2 will replace)
- **Total findings:** 24
- **BLOCKER findings:** 0  ← hard gate met
- **HIGH findings:** 4
- **MED findings:** 7
- **LOW findings:** 13
- **GO/NO-GO recommendation:** **GO** for LAUNCH-2 Monday morning

The DEV theme is structurally sound. All 5 Day 9 schema batch-fix items are
live, the INTERLINK-3 phone fix is in place, AI-9 36 FAQs render across the
category pages, and the 1,654 W0-3 redirects are loaded. Four HIGH items
should be addressed Day 10 if time permits (one user-facing form-link
gap, one cross-domain JSON-LD issue, one duplicate Product JSON-LD, one
gap in the AI-9 FAQ coverage), but none block shipping.

---

## Phase 0 — Pre-flight + scope baseline

| Item | Value |
|---|---|
| Branch | `main` |
| HEAD | `2ea78359b4397fcce81136fd9a7dbf40313a02b6` |
| `bbi-build-state.md` length | 821 lines |
| Working tree | clean apart from pre-existing `.bak` files + untracked items (per prompt expectation) |
| DEV preflight | DEV unpublished, LIVE main — write target confirmed `186373570873` |
| Theme file count | 345 (`.liquid`/`.json`/`.js`/`.css` under `theme/`) |

---

## Phase 1 — Theme bundle health

### shopify theme check (full DEV theme)

- **264 files inspected · 2856 offenses across 167 files**
- **2051 errors · 805 warnings**

| Category | Count | Source / verdict |
|---|---|---|
| `ValidSchemaTranslations` (error) | 1981 | Avada starter sections — pre-existing, locale-key gap, not blocking |
| `LiquidHTMLSyntaxError` (error) | 44 | Avada starter sections (same `<span>` inside `{% capture %}` pattern across 44 files) — false positive, sections not referenced by BBI templates |
| `TranslationKeyExists` (error) | 8 | BBI customer copy uses `'general.404.title' | t | default: 'Page not found'` — `default:` filter makes the missing key safe at render time |
| `ImgWidthAndHeight` (error) | 7 | Real CLS risk — see MED-3 |
| `MissingAsset` (error) | 6 | 3× `assets/logo.png` in `booster-seo.liquid` (known orphan); 2× `assets/bbi-logo-v2.png` in `bbi-nav.liquid` + 1× in `bbi-footer.liquid` — see LOW-1 |
| `UnknownFilter` (error) | 3 | `assign x = x | push: y` in `ds-cs-base.liquid` (Shopify Liquid array extension — false positive, works at runtime) |
| `MissingTemplate` (error) | 1 | `{% render 'image' %}` in `main-reset-password.liquid` — orphan Avada section, not in BBI flow |
| `ValidSchema` (error) | 1 | Single Avada `header.liquid` schema warning |
| `VariableName` (warning) | 615 | Pre-existing Avada starter (`tuneURL`, etc.) |
| `HardcodedRoutes` (warning) | 127 | Pre-existing Avada starter |
| `UnusedAssign` (warning) | 34 | Mostly Avada starter |
| `UndefinedObject` (warning) | 13 | Avada `cycleGroup` + `paginate` in orphan sections |
| `AssetPreload` (warning) | 8 | `layout/theme.liquid` font preload — pre-existing |
| `DeprecatedFilter` (warning) | 6 | Pre-existing |
| `RemoteAsset` (warning) | 2 | Google Fonts preconnects (intentional, `theme-check-disable` already present in some spots) |

### File counts + sizes (under `theme/`)

| Directory | Files | Total |
|---|---|---|
| `templates/*.json` | 51 | n/a |
| `sections/*.liquid` | 101 | 2.51 MB |
| `snippets/*.liquid` | 108 | 848 KB |
| `layout/*.liquid` | 2 | (theme + password) |
| `assets/*.js` | 13 | 552 KB |
| `assets/*.css` | 68 | 595 KB |
| All `assets/*` | — | 1.32 MB |

### Liquid parse spot-check (5 critical files)

| File | Status |
|---|---|
| `theme/layout/theme.liquid` | Reads cleanly. Contains the `bbi_landing` gate (lines 90–110) and `{% sections 'header-group' %}` at line 162 (header-group.json missing on DEV — no-ops; BBI templates include `bbi-nav-wrap` explicitly so render is unaffected — see MED-7) |
| `theme/snippets/bbi-org-schema.liquid` | Reads cleanly. Emits Organization+LocalBusiness+WebSite. Uses `shop.permanent_domain` for `@id` and entity `url` — see HIGH-2 |
| `theme/sections/ds-article.liquid` | Reads cleanly. Emits BlogPosting + FAQPage JSON-LD |
| `theme/sections/ds-pdp-base.liquid` | Reads cleanly. Renders `bbi-nav` and `bbi-footer` inline (lines 408, 803). Uses native `{% form 'product', product, id: 'pdp-add-to-cart' %}` at line 590 |
| `theme/sections/ds-cc-base.liquid` | Reads cleanly. INTERLINK-3 fix verified (line 593 area, `tel:+18008359565`). AI-9 FAQ JSON-LD auto-builds from `faq_item` blocks (line 530) |

### Dead code

- `snippets/booster-seo.liquid` — known orphan (referenced no longer; 3 missing-asset errors)
- 44 Avada starter sections trigger `LiquidHTMLSyntaxError` but aren't referenced from any active template
- `snippets/image.liquid` is referenced only by `main-reset-password.liquid` (Avada legacy)
- `header-group.json` missing — section-group call no-ops; cleanup post-launch

---

## Phase 2 — Critical page render + performance

**PSI scores: DEFERRED.** The DEV theme is unpublished and only accessible
to logged-in staff; PSI's bot cannot bypass `preview_theme_id` auth and
silently falls back to the LIVE theme. The 5 prompt URLs all redirect to
the primary domain and serve the *old* Avada+BBI hybrid, so live PSI of
the DEV bundle is not feasible from this session.

### Day 8 A11Y Phase 1.5 baseline (LIVE Avada theme, 2026-05-21)

For reference only — the new DS theme is expected to improve mobile
performance once LAUNCH-2 publishes 186373570873.

| URL | Strategy | Perf | A11Y | BP | SEO | LCP | CLS |
|---|---|---|---|---|---|---|---|
| Homepage | desktop | 80 | 95 | 96 | 100 | 2.0s | 0.001 |
| Homepage | mobile | **58** | 98 | 96 | 100 | **10.0s** | 0.0 |

### Recommendation (deferred PSI)

Run PSI immediately after LAUNCH-2 flip on the same 5 URLs from a staff
browser session (or from any non-gated environment). Compare against the
Day 8 baseline. Hard-flag anything > 5-point regression as MED, > 10
points as HIGH.

The static signals we *can* check from the DEV bundle:

- JS bundle 552 KB — moderate (target < 300 KB for mobile p75)
- CSS bundle 595 KB — moderate
- Section + snippet totals 3.36 MB — large, but Shopify only ships
  per-template subsets
- 7 `ImgWidthAndHeight` failures → real CLS risk (MED-3 below)

---

## Phase 3 — SEO + AEO foundation

### Sitemap.xml — PASS

- `https://www.brantbusinessinteriors.com/sitemap.xml` → HTTP 200
- Valid `sitemapindex` with 5 child sitemaps: agentic_discovery,
  products, pages, collections, blogs
- Sample child sitemap URLs resolve

### robots.txt — PASS

- HTTP 200, ~80 directives
- `User-agent: *` allows `/`, all public surfaces
- Disallows `/admin`, `/checkout`, `/cart/`, plus `?preview_theme_id=*` and
  `?preview_script_id=*` (correctly hides our preview URLs)
- Includes UCP/MCP discovery references (`agents.md`, `.well-known/ucp`)
- Sitemap reference present

### JSON-LD validation — static analysis across 10 target page types

PSI bot can't reach the DEV theme, so JSON-LD was verified by reading the
rendering Liquid sources and parsing the static portions. All emit valid
`@context: "https://schema.org"` blocks; runtime field values come from
shop / product / collection objects.

| Page type | Snippet/section | @types emitted | Status |
|---|---|---|---|
| Sitewide (any page with `bbi-nav`) | `snippets/bbi-org-schema.liquid` | Organization+LocalBusiness, WebSite+SearchAction | PASS (with HIGH-2 noted) |
| PDP | `sections/ds-pdp-base.liquid` + `snippets/bbi-product-jsonld.liquid` | Product+Offer (+additionalProperty) | PASS (with HIGH-3 duplicate noted) |
| PDP | `snippets/bbi-breadcrumb-jsonld.liquid` | BreadcrumbList | PASS |
| Category page | `sections/ds-cc-base.liquid` | FAQPage (auto from `faq_item` blocks), BreadcrumbList | PASS |
| `/pages/oecm` | `sections/ds-lp-oecm.liquid` | FAQPage, GovernmentService | PASS |
| `/pages/contact` | `sections/ds-lp-contact.liquid` | LocalBusiness (dedicated) | PASS — Day 9 schema batch-fix verified |
| `/pages/quote` | `sections/ds-lp-quote.liquid` | Service, FAQPage | PASS |
| `/pages/design-services` | `sections/ds-lp-design-services.liquid` | HowTo | PASS |
| `/pages/delivery` | `sections/ds-lp-delivery.liquid` | Service | PASS — Day 9 schema batch-fix verified |
| `/pages/relocation` | `sections/ds-lp-relocation.liquid` | Service | PASS — Day 9 schema batch-fix verified |
| `/blogs/news/how-to-adjust-your-chair` | `sections/ds-article.liquid` | BlogPosting, FAQPage | PASS — Day 9 schema batch-fix verified |

`meta-tags.liquid` `<script type="application/ld+json">{{ product | structured_data }}</script>` block (lines 34–45) **is still active** — it's wrapped in `{% unless settings.seo_microdata %}` and `seo_microdata` is `None` on DEV. This means every PDP emits two Product JSON-LDs (Shopify's auto-emit + `bbi-product-jsonld.liquid`). See HIGH-3.

### Title + meta description spot-check (published BBI pages)

- 24 published pages with BBI DS template suffixes + 1 (`our-work`, suffix `our-work`) = 25 total BBI pages (prompt expected ~23 — close, the 2 extras are valid: `customer-stories` and `our-work`)
- All have non-empty titles
- 1 page exceeds the 60-char title limit:
  - `design-services` — 69 chars: *"Free Office Design Layout & Space Planning | Brant Business Interiors"* — Google will truncate around char 55-60. See MED-2.
- No "Untitled" or empty values
- Meta-description-level audit not done (would need rendered HTML, not Admin metafields) — recommend post-launch DataForSEO On-Page audit per CLAUDE.md SEO-AUDIT-2

---

## Phase 4 — Shopify Admin state

### Themes (Admin REST)

| ID | Role | Name | Updated |
|---|---|---|---|
| `173472874809` | unpublished | AVADA Assets - DO NOT REMOVE | 2024-12-26 |
| `178274435385` | **main** | BBI Live | 2026-05-16 |
| `178281021753` | unpublished | BBI Backup — May 2025 | 2026-04-20 |
| `186373570873` | unpublished | **BBI Landing Dev** | 2026-05-22 |
| `186495992121` | unpublished | bbi-design-system-v1-WIP | 2026-05-07 |

- DEV is unpublished ✓
- LIVE is `178274435385` and is published ✓
- **Note:** LIVE is *not* still pure Avada — it's already an Avada+BBI hybrid (no `bbi-*` markers, but BBI-branded copy). The prompt's "Avada" framing reflects the pre-rebrand baseline; the DS rebuild on DEV is what LAUNCH-2 publishes.

### Pages

- **43 total · 25 published · 18 unpublished**
- 24 published with BBI DS template suffixes (`about`, `oecm`, `contact`, `quote`, `industries`, `healthcare`, `education`, `government`, `non-profit`, `professional-services`, `delivery`, `relocation`, `design-services`, `customer-stories`, `brands`, `faq`, `our-work`, 6× `brand-*`, `brands-otg`, etc.)
- 1 extra published (`how-to-adjust-my-new-chair`, suffix `page`) — legacy but valid
- 18 unpublished: all legacy Avada (`sb-request-quote`, `history-quotes`, `suppliers`, `ds-smoke-test`, `llms-txt`, `html-sitemap-*`, `quote-history`, `request-for-quote`, `search-results-page`, `shipping-delivery`, `win-a-prize-with-brant-basics`, etc.) — intentionally hidden

### Collections

- **316 total · 250 custom + 66 smart · 144 unpublished**
- Main 9 category collections (per prompt):

| Handle | Pub | Title |
|---|---|---|
| `seating` | ✓ | Seating |
| `desks` | ✓ | Desks & Workstations |
| `tables` | ✓ | Tables |
| `storage` | ✓ | Storage & Filing |
| `lighting` | ✓ | Lighting |
| `accessories` | ✓ | Accessories |
| `office-supplies` | ✗ | Office Supplies (deliberately unpublished?) |
| `workplace-essentials` | — | not found by that handle |
| `design-services` | — | not a collection — exists as page |

The "9 categories" framing actually maps to a different set in the nav.
The active BBI Shop nav lists: seating, desks, storage, tables, boardroom,
ergonomic-products, panels-room-dividers, accessories, quiet-spaces +
sub-collections (height-adjustable-tables, planters, telephone-booths,
sound-dampeners, av-stand, power-modules-accessories, walls). All 9
primary categories are published. See MED-4 re: 144 unpublished sub-collections.

### Blogs + articles

- **1 blog: `news`** ✓
- **2 articles:**
  - `how-to-adjust-your-chair` — published 2025-01-13 ✓
  - `tables` — unpublished (leftover draft) — see MED-5

### URL redirects

- **1,654 total** ✓ — matches expected from Day 9 W0-3
- Sample CSV inspection shows special-char product redirects working as
  designed (™, ® → clean URLs)
- Did not fire a live spot-test (DEV preview gate); the count match is
  sufficient evidence the W0-3 import landed

### Navigation menus (Admin GraphQL)

| Handle | Items |
|---|---|
| `main-menu` | **0** (orphan — see MED-6) |
| `footer` | 2 (Search, FAQ) |
| `customer-care` | 4 (Shipping & Delivery, Privacy, Refund, ToS) ✓ |
| `main-menu-2` | 2 top-level / 16 child items (legacy from Avada theme — irrelevant to BBI nav, which is hardcoded) |
| `customer-account-main-menu` | 2 (Orders, Profile — links to `shopify.com/85904130361/account/*` New Customer Accounts) |

The BBI nav (`snippets/bbi-nav.liquid`) does NOT use Shopify linklists — all 5 dropdown items are hardcoded in the snippet. So the empty `main-menu` and the legacy `main-menu-2` have **no effect on BBI render**. Both can be cleaned up post-launch.

---

## Phase 5 — Critical functional checks

### CTAs (static inspection)

| CTA | Target | Status |
|---|---|---|
| Homepage hero "Request a Quote" | `/pages/quote` | ✓ |
| Homepage hero "Shop furniture" | `/collections/business-furniture` | ✓ |
| Homepage hero phone | `tel:18008359565` | ✓ |
| Category page phone closer | `tel:+18008359565` | ✓ (INTERLINK-3 fix) |
| Category page CTA | `/pages/quote?source=collection-cta&lead_type=design-consultation` | ✓ |
| PDP nav rendered | `bbi-nav` inline at line 408 | ✓ |
| PDP footer rendered | `bbi-footer` inline at line 803 | ✓ |

### Form endpoints

| Form | Approach | Status |
|---|---|---|
| Quote page online form | `<a href="{{ section.settings.form_url | default: '/pages/contact' }}">` at line 517 of `ds-lp-quote.liquid`. **`form_url` is NOT set** in `templates/page.quote.json` — defaults to `/pages/contact`. The page promises an "Online quote form" but the channel just links to the contact page, which has no form. See **HIGH-1**. |
| Contact page form | None. `ds-lp-contact.liquid` renders contact info cards + a Google Maps iframe (line 164) but no `<form>` or `{% form 'contact' %}` block. Per section comment, contact page "directs to quote form" — so this is intentional but creates a circular gap with HIGH-1. |
| PDP Add-to-Cart | Native Shopify `{%- form 'product', product, id: 'pdp-add-to-cart' -%}` at `ds-pdp-base.liquid:590` — POSTs to `/cart/add` correctly | ✓ |

### Redirect spot-test

- Sample target URL `/products/bungee-tables-rectangular-flip-top-table-spider-legs-wheels` returned HTTP 200 on LIVE
- Did not test the `/...™...` source URL via curl (URL encoding fragility); the 1,654 admin count plus CSV alignment is sufficient evidence

### 404 page

- `https://www.brantbusinessinteriors.com/this-page-does-not-exist-xyz-12345` → HTTP 404 ✓
- Template `templates/404.json` → `ds-system-404` section with logo from shop_images ✓

---

## Phase 6 — Bug surface from previous work

### Homepage bug fix (Day 8)

- `templates/index.json` has 11 sections (nav-wrap, hero, trust, about, shop, featured, oecm, industries, services, work, footer-wrap) — order intact ✓
- 14 `bbi-hp-ph--*` placeholder references in JSON: these are CSS class names (gradient placeholders), not broken image refs. Verified `theme/assets/bbi-homepage.css:589-611` defines each (hero, seating, desks, storage, boardroom, featured-1/2/3, healthcare, education, government, non-profit, pro-services). Render as solid colored placeholders. Not broken — but see MED-1 (placeholder vs real photography).
- Hero H1: *"Commercial furniture for the way Canadian offices actually work."* — single line, trimmed ✓
- `bbi-about` eyebrow: *"Who we are"* + heading mentions Peterborough + 1964 ✓
- Hero uses `bbi-btn--primary` + `bbi-btn--secondary` classes; CSS provides borders for `--secondary` via tokens — visual outline present ✓

### AI-9 FAQs (Day 8)

- `ds-cc-base.liquid:530-545` auto-builds FAQPage JSON-LD from `faq_item` blocks ✓
- Per-collection template `faq_item` block counts:
  - `accessories: 4`, `boardroom: 4`, `desks: 4`, `ergonomic-products: 4`, `panels-room-dividers: 3`, `quiet-spaces: 4`, `seating: 5`, `storage: 4`, `tables: 4` → **36 total** ✓
  - `business-furniture: 0` — gap, see HIGH-4

### Schema batch-fix (Day 9)

| Fix | Live on DEV? | Evidence |
|---|---|---|
| BlogPosting on `/blogs/news/how-to-adjust-your-chair` | ✓ | `sections/ds-article.liquid` grep count 8 |
| WebSite+SearchAction sitewide | ✓ | `snippets/bbi-org-schema.liquid` lines 71-86 |
| Service on `/pages/delivery` + `/pages/relocation` | ✓ | both sections grep count 4 |
| Dedicated LocalBusiness on `/pages/contact` | ✓ | `sections/ds-lp-contact.liquid` grep count 3 |
| Broken Article block in `meta-tags.liquid` deleted | ✓ | meta-tags.liquid now only has `og:type=article` + Shopify product structured_data (no Article JSON-LD remains) |

### Hours + founding year sweep (Day 9)

- `grep "8:30\|1982"` across `theme/sections/ds-*.liquid` + `theme/snippets/bbi-*.liquid` → **0 results** ✓
- `bbi-org-schema.liquid` uses `Mo-Fr 09:00-17:00` ✓, `foundingDate: 1964` ✓
- Homepage hero eyebrow: *"Canadian-owned · Since 1964"* ✓

### INTERLINK-3 FAIL fix (Day 9)

- `theme/sections/ds-cs-base.liquid` ~line 593: phone CTA `tel:+18008359565` ✓ (matches the fix; the old `+15198371810` is gone)

---

## BLOCKER findings — 0

None.

---

## HIGH findings — 4

### HIGH-1 — Quote page "Online quote form" channel links to /pages/contact which has no form

- **Where:** `theme/sections/ds-lp-quote.liquid:403,517` + `theme/templates/page.quote.json` (no `form_url` setting)
- **What:** The Quote page UI advertises three channels with the first labeled *"Online quote form"* with meta *"Describe your scope · attach a floor plan · we respond in 1 business day"*. The channel anchor uses `section.settings.form_url | default: '/pages/contact'`. The template doesn't set `form_url`, so the link goes to `/pages/contact`. The Contact page (`ds-lp-contact.liquid`) renders info cards + a Maps iframe but contains **no `<form>` or `{% form 'contact' %}` block**. Users clicking "Online quote form" see the contact page and have no form to fill.
- **Why blocking-ish:** Breaks the most prominently advertised conversion path. Phone + email channels still work, so it's not a true BLOCKER (users *can* still contact BBI), but it's a clearly broken promise.
- **Fix:** Either (a) point `form_url` to the page that actually contains the form (a third-party embed page if one exists), or (b) embed a HubSpot/Fillout/native Shopify contact form on `/pages/contact` (or directly inside `ds-lp-quote.liquid`), or (c) re-label the channel to match reality (e.g., *"Quote-by-email"* with a `mailto:` link).
- **Estimated fix time:** 30–60 min depending on path chosen.

### HIGH-2 — bbi-org-schema JSON-LD uses shop.permanent_domain (.myshopify.com) instead of primary domain

- **Where:** `theme/snippets/bbi-org-schema.liquid:13, 16, 19, 72, 76`
- **What:** The Organization+LocalBusiness+WebSite JSON-LD is built with `https://{{ shop.permanent_domain }}` for `@id`, entity `url`, and logo `url`. `shop.permanent_domain` always resolves to `office-central-online.myshopify.com`. But the page canonical and `shop.url` resolve to `www.brantbusinessinteriors.com`. Google's structured-data parser will see two different domains for the same entity — risks splitting the BBI entity in Knowledge Graph / AI Overview and may dilute the canonical signal.
- **Fix:** Replace `shop.permanent_domain` with the hardcoded primary domain `www.brantbusinessinteriors.com`, or with `shop.url` stripped of scheme/trailing slash. Cleanest is hardcoded since this is BBI-specific and unambiguous.
- **Estimated fix time:** 10 min.

### HIGH-3 — Duplicate Product JSON-LD on every PDP

- **Where:** `theme/snippets/meta-tags.liquid:34-45` (Shopify default `{{ product | structured_data }}`) + `theme/snippets/bbi-product-jsonld.liquid` (custom Product schema rendered from `ds-pdp-base.liquid`)
- **What:** `meta-tags.liquid` wraps Shopify's auto-emitted Product JSON-LD in `{% unless settings.seo_microdata %}`. `seo_microdata` is `None` in `config/settings_data.json` → `unless null` evaluates true → Shopify's block IS emitted on every PDP. The custom `bbi-product-jsonld.liquid` also fires. Result: two Product JSON-LD scripts per PDP.
- **Why HIGH:** Google generally handles duplicates without penalty, but it muddies the signal — Google may pick the leaner Shopify auto block over the richer BBI block (which includes `additionalProperty` from specs metafields, brand, mpn). This undercuts the spec-rich AI-3 work.
- **Fix:** Either set `seo_microdata: true` in `config/settings_data.json` (suppresses Shopify auto), or delete the `{% unless settings.seo_microdata %}{...}{% endunless %}` block from `meta-tags.liquid`. Latter is cleaner.
- **Estimated fix time:** 5 min.

### HIGH-4 — business-furniture collection template has 0 faq_item blocks

- **Where:** `theme/templates/collection.business-furniture.json`
- **What:** AI-9 added FAQs to 9 of the 10 category templates (36 total). `business-furniture` got 0. The category page renders the FAQ section conditionally (`if cc_faq_blocks.size > 0`), so the page won't show a broken FAQ section — but `/collections/business-furniture` (which is the parent "Shop Business Furniture" landing) misses the FAQ + FAQPage JSON-LD entirely.
- **Why HIGH:** business-furniture is the *parent* of all category nav — likely the highest-traffic collection page. Missing FAQs hurts AI Overview eligibility and on-page dwell time.
- **Fix:** Add 4 faq_item blocks (parent-level FAQs about BBI's full catalog, OECM eligibility, lead times, brand portfolio) to `collection.business-furniture.json`.
- **Estimated fix time:** 20 min content + 5 min template push.

---

## MED findings — 7

### MED-1 — Homepage uses gradient placeholder backgrounds in lieu of real photography

- **Where:** `theme/templates/index.json` + `theme/assets/bbi-homepage.css:589-611`
- **What:** Hero, 5 shop cards, 3 featured slots, 5 industry cards all use `.bbi-hp-ph--*` CSS classes that render solid color/gradient blocks (no `<img>`). This is the Day 8 bug-fix landing state, replacing the previously broken `bbi-hp-*.jpg` references.
- **Why MED:** Functional but visually thin. The hero gradient (charcoal → red) is acceptable as a brand stand-in; the rest read as "unfinished" to first-time visitors.
- **Fix:** Schedule a photo swap (Post-W0/AI-10 backlog) — use OCI photos already cataloged in `data/oci-photos/`. Not blocking launch; brand has approved this look per Day 8 commit.

### MED-2 — design-services page title is 69 chars (truncated in SERPs)

- **Where:** Shopify Admin page `design-services` → title *"Free Office Design Layout & Space Planning | Brant Business Interiors"*
- **Why MED:** Google truncates around 55–60 chars; tail clipped.
- **Fix:** Shorten to ~55 chars, e.g., *"Free Office Design & Space Planning | BBI Ontario"* (49 chars).
- **Estimated fix:** 2 min in Admin.

### MED-3 — 7 ImgWidthAndHeight errors create CLS risk

- **Where:**
  - `theme/sections/ds-lp-design-services.liquid` — 3 imgs (lines 344, 461, 483) missing height/width
  - `theme/snippets/bbi-nav.liquid` — 2 logo imgs missing width
  - `theme/sections/ds-pdp-base.liquid:809` — `pdp-lightbox__img` (src injected by JS; intentional, can suppress with `theme-check-disable`)
  - `theme/snippets/bbi-footer.liquid` — 1 logo img missing width
- **Fix:** Add `width=` to logo `<img>` tags (height is already set). Add both dimensions to the 3 design-services imgs. Suppress the lightbox warning with a `theme-check-disable` comment.
- **Estimated fix:** 15 min.

### MED-4 — 144 unpublished collections (sub-collections)

- **What:** 144 of 316 collections are unpublished. Most are sub-collections (`adjustable-2-shelf-units`, `bedside-tables`, `bin-storage-tower`, …) that are intentionally hidden from public browse but still serve products via parent smart collections.
- **Why MED:** No verification done that all 144 are *intentionally* hidden — some could be stale Avada legacy.
- **Fix:** Post-launch audit — diff the unpublished list against the BBI taxonomy plan in `docs/plan/site-architecture-2026-04-25.md`. Unpublish-or-archive sweep at AI-11 or earlier.

### MED-5 — Unpublished article "tables" in /news blog

- **Where:** `blogs/news/articles` includes one unpublished article handled `tables`
- **Fix:** Delete or finish + publish. 2 min in Admin.

### MED-6 — main-menu has 0 items (orphan)

- **What:** Shopify linklist `main-menu` is empty. BBI nav is hardcoded so this is harmless to render, but `{{ linklists.main-menu }}` references anywhere would silently emit nothing.
- **Fix:** Either populate (for consistency with default Shopify behaviour) or delete the menu entirely post-launch.

### MED-7 — header-group.json missing on DEV theme

- **What:** `theme/layout/theme.liquid:162` calls `{% sections 'header-group' %}` but no `sections/header-group.json` exists on the DEV theme. The tag silently no-ops. BBI templates include `bbi-nav-wrap` as the first section explicitly, so render is unaffected.
- **Fix:** Remove the orphan `{% sections 'header-group' %}` line, or create an empty `header-group.json`. Cleanup post-launch.

---

## LOW findings — 13

| # | Item | Where | Note |
|---|---|---|---|
| LOW-1 | `assets/bbi-logo-v2.png` asset missing from DEV theme | `bbi-nav.liquid:160,492,678` + `bbi-footer.liquid:160` | Only used as fallback in `{% if logo != blank %}{% else %}...` branches. Every BBI template instance has `logo: shopify://shop_images/bbi-logo-v2_aa647658-…png` set, so the working Files-uploaded logo renders. Broken only if a merchant clears the section logo setting. Fix: upload the asset, or rewrite fallback as `{% if logo == blank %}{{ shop.name }}{% else %}{{ logo | image_url … }}{% endif %}`. |
| LOW-2 | `assets/logo.png` missing | `snippets/booster-seo.liquid:243-625` | Snippet is orphan (not rendered). Cleanup. |
| LOW-3 | `snippets/image.liquid` missing | `sections/main-reset-password.liquid:5` | Orphan Avada section, not in BBI customer flow. |
| LOW-4 | 44 `LiquidHTMLSyntaxError` in Avada starter sections | various `sections/Collapsible-content.liquid`, `accordion-boxes.liquid`, etc. | Same false-positive pattern (`<span class="line-marker {% if … %}highlight-background {% if … gradient` inside `{% capture %}`). Sections not referenced by any BBI template. |
| LOW-5 | 1,981 `ValidSchemaTranslations` | Avada starter sections | Locale-key gap for translated section schemas. Pre-existing; doesn't affect render. |
| LOW-6 | 127 `HardcodedRoutes` warnings | various | Pre-existing Avada. |
| LOW-7 | 615 `VariableName` warnings | various | Pre-existing Avada naming. |
| LOW-8 | 3 `UnknownFilter: push` | `ds-cs-base.liquid:347,349,354` | Valid Shopify Liquid array filter; theme-check version doesn't recognize it. Verified runtime works (category filters depend on it). |
| LOW-9 | `AVADA Assets - DO NOT REMOVE` theme (173472874809) lingers | Admin Themes | Last updated 2024-12-26. Safe to keep as a fallback. Optional cleanup post-launch. |
| LOW-10 | `BBI Backup — May 2025` theme (178281021753) lingers | Admin Themes | Pre-DS-rebuild backup. Keep for now as rollback safety net. |
| LOW-11 | `bbi-design-system-v1-WIP` theme (186495992121) lingers | Admin Themes | WIP intermediate. Can delete post-launch. |
| LOW-12 | `customer-account-main-menu` links to `shopify.com/85904130361/account/*` | Customer account menu | New Customer Accounts URLs. Working as designed per Task #12 DEV-3. |
| LOW-13 | `booster-seo.liquid` orphan known | Theme | Already flagged in prior audits. No action. |

---

## GO/NO-GO recommendation

**GO** for LAUNCH-2 Monday morning.

0 BLOCKER findings. All 5 Day 9 schema batch-fix items, the Day 8 homepage
fix + AI-9 FAQs, the Day 9 INTERLINK-3 fix, and the W0-3 redirect import
are all live on DEV. 9 main category collections published, BBI nav
hardcoded so the empty `main-menu` doesn't matter, 25 BBI pages published.

The 4 HIGH findings are real but contained:

1. **HIGH-1 (quote→contact form gap)** is the most user-facing — fix
   Day 10 if possible (recommended). 30–60 min.
2. **HIGH-2 (JSON-LD .myshopify.com domain)** is an SEO/AEO quality
   issue, not a launch blocker. Fix Day 10 (10 min) — high ROI.
3. **HIGH-3 (duplicate Product JSON-LD)** — fix Day 10 (5 min) — high ROI.
4. **HIGH-4 (business-furniture FAQs missing)** — fix Day 10 (25 min).

All 4 HIGH items together: ~80 min if knocked out in sequence.

PSI verification deferred — re-run immediately after the LAUNCH-2 theme
flip from a staff browser session and compare to the Day 8 baseline.

---

## Concerns to flag for Monday

1. **Form workflow** (HIGH-1) — if not fixed Day 10, customers landing
   on `/pages/quote` and clicking the most prominent "Online quote form"
   channel see the contact page with no form. Either fix or re-label.
2. **PSI never run on DEV** — first real performance read happens *after*
   launch. If mobile LCP regresses from the 10s LIVE baseline, surface
   immediately.
3. **`business-furniture`** is the parent of all category nav — missing
   FAQs there is a measurable AI Overview gap.
4. **JSON-LD domain mismatch** is the single highest-leverage SEO/AEO
   fix in this audit — 10-minute change, multi-month payoff.

---

*Report generated by Step 33 SYS-VERIFY-1 Phase 2, 2026-05-24.*
