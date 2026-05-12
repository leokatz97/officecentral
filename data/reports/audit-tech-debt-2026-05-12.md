# BBI Tech-Debt Audit — 2026-05-12

**Scope:** Read-only audit of theme codebase + Shopify API state  
**Sessions context:** PE Pass 3 continuation, COLLECTION-CLEANUP-1, Wave E hardening, BLOG-SEED-1  
**Preflight:** DEV `186373570873` = unpublished ✓  LIVE `178274435385` = main (untouched) ✓  

---

## Summary

| Impact | Count |
|---|---|
| **Blocks launch** (must fix before LAUNCH-0) | 4 |
| **Nuisance** (real issues, no immediate launch blocker) | 7 |
| **Info** (observations, no action before launch) | 4 |
| **Total findings** | 15 |

Top 4 blockers in order of severity:
1. `keilhauer` brand collection — 0 products (all category callout links dead)
2. `ergocentric` brand collection — 0 products (same)
3. `oecm-eligible` collection — 653/653 products all tagged (OECM page shows full catalog)
4. Our Work page — 48 OCI photos not uploaded to Shopify CDN (broken images at launch)

---

## Findings

---

### DEBT-01
**Section:** D. Empty collections  
**Impact:** Blocks launch — `/collections/keilhauer` is empty; brand callout CTAs dead  
**What:** Smart collection `keilhauer` has rule `TAG EQUALS 'brand:keilhauer'` but **0 products** match. `scripts/tag-products-by-collection.py` was written in WAVE-G-FIXES-1 BATCH-4 with 34 boardroom + 14 global-teknion candidates identified, but was never run `--live`. No products have been assigned `brand:keilhauer`. Category pages (seating, desks, boardroom, ergonomic) render Keilhauer brand callout blocks with "View all Keilhauer" CTAs pointing to `/collections/keilhauer`. All of those links resolve to an empty collection page.  
**Why it matters:** Every category page with a Keilhauer callout surfaces a dead collection before launch.

---

### DEBT-02
**Section:** D. Empty collections  
**Impact:** Blocks launch — `/collections/ergocentric` is empty; brand callout CTAs dead  
**What:** Smart collection `ergocentric` has rule `TAG EQUALS 'brand:ergocentric'` but **0 products** match — same unrun tagging script issue as DEBT-01. Category pages with ergoCentric brand callouts (ergonomic products, seating) link to an empty collection.  
**Why it matters:** ergoCentric is one of the three marquee brands; landing on 0 results undermines trust.

---

### DEBT-03
**Section:** D. Empty collections  
**Impact:** Blocks Wave E AI-8 (OECM copy hardening)  
**What:** Smart collection `oecm-eligible` has rule `TAG EQUALS 'oecm-eligible'` and returns **653 products** — the full active catalog. Every product has this tag, which is almost certainly unintentional mass-tagging during a PE push or import. The `/collections/oecm-eligible` page would surface all 653 products as "OECM eligible", invalidating BBI's OECM differentiation claim. Confirmed via API: rule column=TAG, relation=EQUALS, condition="oecm-eligible", productsCount=653.  
**Why it matters:** AI-8 is supposed to harden OECM copy. If the collection itself is inaccurate, that hardening work publishes a false claim to institutional buyers.

---

### DEBT-04
**Section:** F. Forward-build snags  
**Impact:** Blocks launch — Our Work page has broken image references  
**What:** `theme/sections/ds-lp-our-work.liquid:85` contains an explicit TODO: "Upload OCI photos to Shopify CDN assets and replace these asset_url references." The 48 OCI project photos (`data/oci-photos/`) are on the local filesystem. At launch, the Our Work / Portfolio page (`/pages/our-work`) will render broken image slots.  
**Why it matters:** Our Work is a trust page; broken images at launch undermine the "48 real project photos" proof point.

---

### DEBT-05
**Section:** A. Anti-pattern  
**Impact:** Nuisance only — redundant override, Wave E DS-VERIFY may flag  
**What:** `theme/sections/ds-pdp-base.liquid:73` and `theme/sections/ds-cart-base.liquid:23` each contain `body { background: #FFFFFF !important; }`. The PDP-BLACK-FIX consolidated the authoritative override in `<head>` in `theme/layout/theme.liquid` with matching specificity. The section-level rules are a leftover belt-and-suspenders layer. They're harmless but any future section-level background attempt will silently lose to these `!important` rules, and DS-VERIFY will flag hardcoded color literals in section CSS.  
**Why it matters:** DS-VERIFY checks token compliance; these hardcoded literals will produce false positives.

---

### DEBT-06
**Section:** D. Empty collections  
**Impact:** Nuisance only — misleading collection definition  
**What:** Smart collection `fees-products` uses two negative exclusion rules (`TYPE NOT_CONTAINS 'mws_fee_generated'` AND `TYPE NOT_EQUALS 'mws_apo_generated'`), resulting in **653 products** — the entire active catalog minus Avada fee line items. This is an Avada/MWS app collection. It appears in the Shopify Admin collections list, making it easy to misread during COLLECTION-CLEANUP-1.  
**Why it matters:** Can cause confusion during COLLECTION-CLEANUP-1 if someone mistakes it for a real content collection.

---

### DEBT-07
**Section:** A. Anti-pattern  
**Impact:** Nuisance only — hardcoded token drift in ds-search-results  
**What:** `theme/sections/ds-search-results.liquid:75` uses `border-color: #0B0B0C` as a hardcoded hex instead of `rgb(var(--textColor))`. All other ds-* sections that define local token overrides use the `var(--textColor)` form (safe inside locally-scoped tokens). ds-search-results defines `--textColor: #0B0B0C` in its `:root` override but missed this one rule.  
**Why it matters:** Token drift; will fail a strict DS-VERIFY token-compliance pass.

---

### DEBT-08
**Section:** A. Anti-pattern  
**Impact:** Nuisance only — wrong brand red on product colour swatches  
**What:** `theme/snippets/product-options.liquid:130` and `:156` assign `#C8102E` (old brand red) as the swatch hex for "Red" colour variants. Current brand red is `#D4252A` (set in DS-3). This is a Starlite legacy snippet for colour variant swatch chips.  
**Why it matters:** Any product with a "Red" colour variant shows the pre-rebrand red chip; brand consistency gap.

---

### DEBT-09
**Section:** E. Blog readiness  
**Impact:** Nuisance — blog posts ship without Article structured data  
**What:** `theme/sections/ds-article.liquid` has conditional FAQPage JSON-LD but **no Article or BlogPosting JSON-LD**. The `{% schema %}` `"name": "Article"` is the section display name only, not structured data. For BLOG-SEED-1 to maximize AI Overview readiness (a CLAUDE.md objective), each post needs `@type: BlogPosting` schema with `headline`, `datePublished`, `author`, and `image`.  
**Why it matters:** Missing Article schema means no Google rich results for blog posts at seed time; harder to fix retroactively.

---

### DEBT-10
**Section:** A. Anti-pattern / performance  
**Impact:** Nuisance — duplicate Google Fonts preconnect per page  
**What:** 22 ds-* section files each independently include the same three Google Fonts link tags (`preconnect` + stylesheet for Inter/JetBrains Mono). Since each BBI template currently loads exactly one ds-* section, this fires once per page — but it's fragile. If two ds-* sections appear on one template (possible in future hybrid pages), the font stylesheet downloads twice. The canonical location is `theme/layout/theme.liquid` inside the `bbi_landing` gate.  
**Why it matters:** PERF-AUDIT-1 may flag redundant `<link>` tags; creates a maintenance trap.

---

### DEBT-11
**Section:** A. Anti-pattern  
**Impact:** Nuisance — shipped TODO comment  
**What:** `theme/sections/ds-lp-our-work.liquid:85` has a TODO comment about uploading OCI photos. This is the code-smell surface of DEBT-04. Overlapping finding, noted separately because it's also an A. anti-pattern violation (TODO in shipped code).  
**Why it matters:** Tracked under DEBT-04 (broken images); the comment is secondary.

---

### DEBT-12
**Section:** E. Blog readiness  
**Impact:** Info only — article related products require per-article metafield  
**What:** `theme/sections/ds-article.liquid` pulls related products from `article.metafields.custom.related_collection` (a `single_line_text` metafield set to a collection handle). If not set, the related products module silently does not render (graceful `{%- if related_handle != blank -%}` guard at line 231). For BLOG-SEED-1, the first 3 posts will have no related products unless the metafield is set per article in Shopify Admin after publishing.  
**Why it matters:** Operational note for BLOG-SEED-1 publishing; not a structural blocker.

---

### DEBT-13
**Section:** F. Forward-build snags  
**Impact:** Info only — AI-9 requires new block type in ds-cc-base schema  
**What:** `theme/sections/ds-cc-base.liquid` schema has block types: `tile`, `brand_callout`, `brand_plate`, `@app`. There is no `faq_item` block type. AI-9 (add 3–5 FAQ blocks + FAQPage schema to 9 category pages) requires adding a new block type to the schema and a FAQPage JSON-LD output block. This is expected implementation work, not a surprise — but it means AI-9 cannot be done via Theme Editor settings alone; it needs a code push.  
**Why it matters:** AI-9 is a section file edit + re-push, not a template JSON edit.

---

### DEBT-14
**Section:** F. Forward-build snags  
**Impact:** Info only — AI-8 / AI-5 on OECM page are structurally ready  
**What:** `theme/sections/ds-lp-oecm.liquid` already has a hardcoded FAQ section (lines 491–555) with FAQPage JSON-LD (line 280). AI-5 (FAQ schema on OECM) is already in place. AI-8 (OECM copy hardening) is a direct Liquid copy edit. No structural changes needed for either row. DEBT-03 must be resolved first before AI-8 copy work makes sense.  
**Why it matters:** Confirms AI-5 done and AI-8 is copy-only — once DEBT-03 is resolved.

---

### DEBT-15
**Section:** F. Forward-build snags  
**Impact:** Info only — AI-7 homepage entity copy is a settings edit  
**What:** `theme/templates/index.json` renders 10 sections including `bbi-hero` and `bbi-trust`. AI-7 (entity-clarity copy — who BBI is, what they sell, who they serve, where) maps to settings in `bbi-hero` and related sections. No structural change needed — this is a pure settings/copy edit in the section files or template JSON.  
**Why it matters:** Confirms AI-7 is a settings-only edit; no section rebuild required.

---

## Section D — Smart Collection Inventory

### Collections with 0–2 products

| Handle | Title | Count | Sort Order | Likely Action |
|---|---|---|---|---|
| `keilhauer` | Keilhauer | **0** | best-selling | Run tag script --live (DEBT-01) |
| `ergocentric` | ergoCentric | **0** | best-selling | Run tag script --live (DEBT-02) |
| `bundle-builder-products` | Bundle builder products | **0** | created-desc | Keep — Avada app, intentional |
| `room-break-room` | Room: Break Room | **0** | best-selling | Investigate — no room:break-room tags |
| `mandatory-fees` | Mandatory Fees | **1** | best-selling | Keep — intentional fee product |

**Notable outliers in 3+ list:**
- `oecm-eligible` — 653 (full catalog; see DEBT-03)
- `fees-products` — 653 (negative exclusion rule; see DEBT-06)
- `smart-products-filter-index-do-not-delete` — 653 (Starlite/Avada filter index — do not touch)
- `products`, `products-1`, `all` — 648–653 (Avada catch-all collections — do not touch)

Total smart collections with ≥3 intentional products: 37  
Total smart collections audited: 49  
Full CSV: `data/reports/empty-collections-snapshot-2026-05-12.csv`

---

## Section B — Search Bar Insertion Path

The existing inline search bar (`<div class="bbi-header__search-bar">`) sits between `</nav>` and `<div class="bbi-header__utility">` in `bbi-nav.liquid` — after the 5 mega-menu items, before the phone/Quote/cart/hamburger cluster. It is hidden on mobile (`display:none` at `<768px`). The bar already has `data-bbi-search-input`, `data-bbi-search-results`, and complete click-outside / Escape close logic with debounced `/search/suggest?type=product` fetch. A full-width search overlay hooks into this existing structure: toggle a CSS class (`bbi-header--search-open`) on `<header>` on input focus, expand `.bbi-header__search-bar` to full width with `position:absolute` overlaying the nav, reuse the existing suggest JS. No conflicting search element needs removal — the Starlite `header-search-bar.liquid` and `predictive-search-drawer.liquid` snippets exist in the theme's snippets folder but are **not rendered** in any BBI template header.

---

## Section C — PE Script Verdict

`scripts/push-pe3-enrichment.py` is ready for a `--review-file` flag addition without structural refactoring. The script uses a consistent ad-hoc `sys.argv` pattern throughout: `'--live' in args`, `'--hero' in args`, and `next((a.split('=',1)[1] for a in args if a.startswith('--handle=')), None)`. Adding `--review-file` follows the identical pattern: one `next()` line in the args block, one `load_review_file_products(path)` function mirroring `load_enrichment_products()` but reading handles from the specified review file, and one conditional branch in `main()`. The load / fetch / plan / apply stages are already cleanly separated. No entanglement to unwind.

---

## Section E — Blog Launch-Readiness

The blog list (`ds-blog-list.liquid`) has a proper empty state: `{%- if blog.articles_count > 0 -%}` gates both filter chips and the article grid; the `{%- else -%}` branch renders a styled `.blog-empty` div with "Coming soon" heading and copy. **It will not look broken at zero posts.** The article template (`ds-article.liquid`) renders author byline (`article.author` at line 183), first tag as pill (line 172), and a related-products module (conditional on `article.metafields.custom.related_collection`). One gap: no Article/BlogPosting JSON-LD (FAQPage schema is present and conditional — see DEBT-09). Both templates embed BBI nav/footer directly via `render 'bbi-nav'` / `render 'bbi-footer'`, and both suffixes are in the `bbi_landing` gate.

---

## Section F — Forward-Build Snag Summary

**Search bar build:** No blockers beyond Section B. Existing bar is the clean hook; expanded-mode is a CSS class toggle + style addition.

**PE Pass 3 review-file push:** No blockers beyond Section C. Script ready for flag addition. Content dependency: batches 3/4/6 must complete enrichment sessions first (not structural).

**Wave E AI copy hardening:**
- AI-7 (homepage entity copy): No blocker. Settings edit only.
- AI-8 (OECM copy): Conditional on DEBT-03 resolution. Structurally ready once tag issue is fixed.
- AI-9 (FAQ blocks on 9 category pages): New block type required in `ds-cc-base.liquid` schema — code push needed before template JSON edits can work.
- AI-5 (FAQ schema on OECM): Already done. Design Services FAQPage not audited in this pass — quick grep recommended.

**Blog seed posts (BLOG-SEED-1):** No structural blocker to publishing. Two pre-conditions: (1) DataForSEO keyword research per CLAUDE.md rule (content gate, not structural); (2) Article/BlogPosting JSON-LD added to `ds-article.liquid` before or with first post (DEBT-09 — 30-minute code push).
