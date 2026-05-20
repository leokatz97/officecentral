# SYS-VERIFY-1 Phase 1 — System Surfaces Audit
_2026-05-20 · Read-only baseline · 8 areas covered_

**Scope:** non-template system surfaces (robots.txt, sitemap, search, cart, error pages, account flows, redirects, theme settings, Shopify-level features). All checks read-only against LIVE (`brantbusinessinteriors.com`, theme `178274435385`) and DEV theme `186373570873` via the Admin API. No writes.

**Phase 2 (separate prompt)** runs the same audit as a launch gate against near-final theme immediately before LAUNCH-0. This document is the baseline.

---

## Executive summary

The Shopify-level plumbing (robots.txt, XML sitemap, cart endpoint, search engine, 404 handling, SSL, Customer Accounts redirect) is fundamentally healthy — Shopify is doing its job. The risk surface is **content debt on the LIVE site that will carry over to the new theme unless cleaned up before LAUNCH-2**: a non-branded favicon pointing at a random product image, 21 redirects dumping users at the homepage, 5+ duplicate quote/contact pages all published, and 6 legacy HTML-sitemap pages from a removed app.

Of the 8 areas audited, **3 have launch-blocking issues** (favicon, page duplication, cart CTA), **3 have should-fix issues** (root-target redirects, redirect chains, stale pages), and **2 are clean** (robots.txt, 404 template). The cleanups are all data-layer (pages, redirects, theme settings) — none require theme code changes — so the work can run in parallel with the remaining ⬜ rows in Wave A.

The single thing most likely to surface as a launch defect is the **favicon**, because it's set in `settings_data.json` on both DEV (`shopify://shop_images/DFE_MVL11860_JN07_Side_generated.jpg`) and LIVE (`shopify://shop_images/business-interiors-default-title-mvl11860-stradic-mesh-bac`) to a generated *product image*, not a BBI logo asset. This will render as a tiny indistinct icon in browser tabs the moment LAUNCH-2 fires. Fix needs a proper square BBI mark uploaded to Files → set in Customize.

---

## Critical findings (must-fix before LAUNCH-2)

### C1. Favicon points at a random product image, not a BBI mark
- **Where:** `config/settings_data.json` → `favicon` setting (both themes)
  - LIVE: `shopify://shop_images/business-interiors-default-title-mvl11860-stradic-mesh-bac`
  - DEV : `shopify://shop_images/DFE_MVL11860_JN07_Side_generated.jpg`
- **Why it matters:** Browser tab + bookmark + search-result icon are part of the brand. Currently shows a chair render scaled to 16×16 — illegible.
- **Recommended fix:** Upload a square BBI logo (512×512 PNG, transparent background — `data/logos/bbi-logo-hires-transparent.png` is a candidate but may need a square crop) to Files. Set on DEV theme Customize → Theme settings → Favicon. Verify on `/cart`, `/products/...`, `/collections/...` before LAUNCH-2.

### C2. Five quote-related pages all published (content duplication)
- **Live + published:** `/pages/quote`, `/pages/request-for-quote`, `/pages/sb-request-quote`, `/pages/quote-history`, `/pages/history-quotes`. All return HTTP 200. Last-updated dates range 2024-10-20 → 2026-05-05, meaning the older ones haven't been touched in 1.5+ years but are still crawlable and in the sitemap.
- **Why it matters:** Search engines see five competing quote pages → keyword dilution. `/pages/quote` is the canonical (P1-4 build). The other four are old-theme remnants.
- **Recommended fix:** Unpublish `/pages/request-for-quote`, `/pages/sb-request-quote`, `/pages/quote-history`, `/pages/history-quotes`. Add 301 redirects from each old handle → `/pages/quote`.

### C3. Six legacy HTML-sitemap pages still published
- **Live + published:** `/pages/html-sitemap`, `/pages/html-sitemap-articles`, `/pages/html-sitemap-blogs`, `/pages/html-sitemap-collections`, `/pages/html-sitemap-pages`, `/pages/html-sitemap-products` — all updated 2025-06-28 (likely the date the generating app was last allowed to write).
- **Why it matters:** Shopify auto-generates `/sitemap.xml`. These HTML mirrors are app remnants, no SEO value, and add 6 indexable URLs.
- **Recommended fix:** Unpublish all six. No redirects needed (no inbound traffic).

### C4. `/pages/please-click-below` is published as a real page
- **Why it matters:** Title-text suggests it was a holding page from an old menu rebuild ("click below" was a placeholder). It's the target of multiple legacy redirects (e.g. `/pages/space-division` → `/pages/please-click-below`). Content currently shows old "Look Books" CTA — not brand-current.
- **Recommended fix:** Decide a real destination — likely `/pages/about` or `/pages/our-work` — and rewrite the existing inbound redirects to point there. Then unpublish the placeholder page.

---

## Should-fix findings (nice-to-have)

### S1. 21 active redirects dump users at the homepage (`/`)
- **Where:** Admin API → `redirects.json` (total redirects: **1647**).
- **Examples:** `/admin → /`, `/roma-1900-nesting-chair → /`, multiple `copy-of-...` product paths → `/`, `/account/unsubscribe → /`.
- **Impact:** Hurts SEO (303 ranking dilution to root), and gives users a confusing "you wanted X, here's the homepage" experience.
- **Fix:** Pull the list, decide per-row: delete the redirect (return real 404) or repoint to the relevant collection/category.

### S2. 18 potential redirect chains
- **Where:** Same dataset — targets that are also a `from` path of another redirect.
- **Impact:** Each extra hop hurts crawl budget and link equity.
- **Fix:** Resolve every chain to direct A → final-target. The Admin API redirect editor or a single bulk update via the API will do.

### S3. Duplicate FAQ / shipping pages
- `/pages/faq` (2026-05-06) vs `/pages/frequently-asked-questions` (2025-03-28)
- `/pages/delivery` (2026-05-07) vs `/pages/shipping-delivery` (2024-10-11)
- **Fix:** Unpublish the older versions; 301 to the newer.

### S4. `/pages/contact` is stale (last updated 2025-06-28)
- May still be the live nav target. Verify against current copy/lead-routing.

### S5. Cart page lacks an explicit "Request a Quote" CTA
- The LIVE cart HTML contains 1 checkout button and 0 quote CTAs. For BBI's B2B model (Net-30, PO, OECM eligibility), institutional buyers often expect a quote path. This is a theme-level decision (Phase 2 / Wave A) — flagging here for visibility.

### S6. `/pages/llms-txt` and `/pages/search-results-page` are oddities
- `llms-txt` is reachable as HTML (likely meant to be a `.txt` reference at `/llms.txt`).
- `search-results-page` is a placeholder handle (live search uses `/search?q=`).
- Either repurpose or unpublish.

### S7. Two `_shopify_essential` Stradic-mesh references inside DEV settings
- DEV `favicon` and other settings point at `MVL11860*` filenames — the chair Leo used as a placeholder during DS-0 screen audit. Audit the DEV `settings_data.json` for other product-image leakage into chrome (share image, social cards, theme.liquid OG fallback) before LAUNCH-2.

---

## Per-area details

### Area 1 — robots.txt + sitemap.xml — **PASS with notes**

**robots.txt** (LIVE): Standard modern Shopify-managed robots.txt. Includes:
- New agentic/UCP discovery headers (`agents.md`, `.well-known/ucp`, `/api/ucp/mcp`) — Shopify rolled this out platform-wide. Nothing to fix.
- Correct `Disallow` on `/admin`, `/cart/`, `/checkout`, `/orders`, `/account` (except `/account/login`), `/cdn/wpm/*.js`.
- Correct sort/filter crawl-trap blocks (`*sort_by*`, `*filter*&*filter*`, language-picker `ls=`).
- Sitemap reference: `Sitemap: https://www.brantbusinessinteriors.com/sitemap.xml` ✓.
- No accidental product/collection blocks. No nonstandard rules.

**sitemap.xml** (LIVE): Healthy sitemap-index pointing at 5 child sitemaps. Counts:
| Sitemap | URL count |
|---|---|
| products | **586** |
| collections | **193** |
| pages | **37** |
| blogs | **2** |
| (agentic_discovery) | 1 sitemap, no URLs |

Pages sitemap surfaces every stale page noted in C2/C3/C4. Cleanups above will drop the published page count from 37 → ~24.

### Area 2 — Search functionality — **PASS**

- `/search?q=chair` → 200, 24 unique products.
- `/search?q=ergonomic+chair` → 24, `q=Global+Furniture+Group` → 24, `q=OTG` → 24, `q=OECM` → 21, `q=Heartwood` → results returned. All buyer-intent terms surface relevant products.
- `/search?q=` (empty) → 200, returns search page with no results state.
- `/search?q=xyznonexistent12345` → 200 with "Sorry / No results" state ✓.
- `/search/suggest.json?q=ergonomic` → 200, returns proper JSON with `collections` (Ergonomic Accessories, Ergonomic Products, All Ergonomic), `products` array. Predictive search is wired correctly.
- `/search?q=...&view=json` → returns HTML (no alternate JSON view template). Not breaking — but if any code/app expects the JSON view, it would need a `templates/search.json.liquid` shim. Flag-level only.

### Area 3 — Cart + checkout — **PASS with C5 note**

- `GET /cart.js` → 200, valid empty-cart JSON, currency CAD ✓.
- `GET /recommendations/products.json?product_id=0&limit=4` → 404 (expected — product_id=0 is invalid; endpoint exists).
- `/cart` page → 200, renders. One checkout-route button present; **zero Request-a-Quote CTAs** (S5).
- LIVE theme cart is the legacy theme, not the new ds- system. New theme cart drawer is a separate Wave A item.

### Area 4 — Error pages — **PASS**

- `/this-page-does-not-exist-12345` → HTTP **404** ✓, full template rendered (480KB HTML — has header, footer, nav, **4 search form references** for user recovery).
- `/products/nonexistent-product-xyz-zzz` → 404 ✓.
- `/collections/nonexistent-collection-xyz-zzz` → 404 ✓.
- DEV theme has `templates/404.json` → uses `ds-system-404` section, configured with `bbi-logo-v2_aa647658-....png`. Section file is in repo. Confirms 404 is theme-aware in new build.
- 500 not tested (Shopify abstracts; not directly reachable).

### Area 5 — Account / customer flows — **PASS for B2B model**

- `/account/login` → 302 → `shopify.com/85904130361/account?locale=en&...` — Shopify's **new Customer Accounts (hosted)**. This is platform-managed; theme can no longer fully template the login form. BBI's institutional buyers will generally bypass accounts (they use PO/Net-30), so this is acceptable.
- `/account/register` → same hosted flow.
- `/account/recover` direct URL → 404 from Shopify hosted side (the password-reset link in emails works; only the manually-typed URL 404s). Low impact.
- Legacy theme footer/nav still references `Powered by Shopify` and a `Compare` widget — old-theme cruft, will go away with new theme.

### Area 6 — Redirects — **WARN**

- **Total active redirects: 1647** (queried via Admin API `redirects/count.json`).
- **Targeting `/` root: 21** → most are stale `copy-of-...` product handles + `/admin` + `/account/unsubscribe`.
- **Potential chains (target matches another from-path): 18** → cleanup work in S2.
- Spot-check of 10 random redirects: from-paths confirmed gone, to-paths all returned 200 (canonical Obusforme example: `/products/obusformea®-comfort-all-leather-1240-3-grade-10 → /products/obusforme-comfort-1240-3` ✓).
- Recent additions not isolated in this pass; if you want a delta report on "added in last 7 days," that's a single Admin API query off `created_at`.

### Area 7 — Theme settings + favicon + share image — **WARN**

- DEV brand colors are correctly set to the locked palette: `#0B0B0C` (ink), `#FFFFFF`, `#D4252A` (hover red), `#FAF...` (alt bg). Header font `inter_n4`, body `inter_n5`. Color scheme drawer wired.
- LIVE still has the older `#000000 / #b40c1c` palette — expected for legacy theme.
- **Favicon: CRITICAL (C1)** — both themes set favicon to a generated product image instead of a logo.
- Default share image / OG image: not located in surfaced keys. Worth a focused pass during meta-defaults review in SEO-AUDIT-1.
- Social links (Facebook, Twitter, Instagram, LinkedIn) all populated and BBI/OfficeCentral-branded ✓.

### Area 8 — Critical Shopify features — **PASS**

- SSL: Shopify-managed, no findings (HTTPS enforced; `Strict-Transport` headers present).
- Custom domain: `brantbusinessinteriors.com` correctly serving theme.
- Email notification templates: not inspected this pass — Admin API `notifications.json` requires a separate scope. Flag for Phase 2.
- Tax/shipping settings (Ontario): not inspected — Admin API surfaces these but they're outside theme write surface; treat as Steve's billing-side responsibility.

---

## Recommended actions (prioritized)

1. **[BLOCKING]** Replace the favicon on DEV theme with a real square BBI mark before LAUNCH-2. — owner: Leo
2. **[BLOCKING]** Unpublish the four stale quote pages (`/pages/request-for-quote`, `/pages/sb-request-quote`, `/pages/quote-history`, `/pages/history-quotes`) and add 301s → `/pages/quote`. — owner: Leo (Admin API or Shopify Admin)
3. **[BLOCKING]** Unpublish the six `/pages/html-sitemap*` pages. — owner: Leo
4. **[BLOCKING]** Resolve `/pages/please-click-below` (repoint inbound redirects → `/pages/about` or `/pages/our-work`, then unpublish).
5. Clean the 21 root-target redirects: per-row decision delete vs. repoint.
6. Flatten the 18 potential redirect chains.
7. Decide canonical FAQ + shipping handles; 301 the duplicates.
8. Audit DEV `settings_data.json` for stray product-image references on chrome surfaces (OG image, theme.liquid fallbacks) before LAUNCH-2.
9. (Optional, theme-side) Add a "Request a Quote" CTA to the cart page in new theme — supports B2B flow.
10. Run **Phase 2** of SYS-VERIFY-1 immediately before LAUNCH-0 to confirm all the above are resolved on near-final theme.

---

## Excluded from scope

- Theme template content (covered by Wave A / Track D audits)
- Performance metrics (PERF-AUDIT-1)
- Accessibility (A11Y-AUDIT-1)
- SEO meta tags + on-page (SEO-AUDIT-1, mandatory pre-LAUNCH-0 gate per CLAUDE.md)
- Email-notification template customization (separate Admin API scope)
- Tax/shipping/billing settings (Steve's responsibility, not theme)
