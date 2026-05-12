# Brand Page Inventory

_Generated 2026-05-12 by BRAND-INVENTORY-1 audit. Read-only._

---

## Summary

| | Count |
|---|---|
| Brand-related Shopify pages | 4 (+ 1 hub) |
| Brand-related collections found | 6 |
| **Healthy** (page + ≥10 products) | **1** (Global/Teknion — 56 products) |
| **Thin** (page + 1–9 products) | **0** |
| **Empty** (page + 0 products — DEBT-01/02 pattern) | **2** (Keilhauer, ergoCentric) |
| **Orphaned-page** (page exists, no collection) | **0** |
| **Missing-page** (collection but no landing page) | **0** |
| Callable brands with no page at all | **3** (OTG / Offices to Go, Heartwood, ObusForme) |
| Stale legacy collections (empty, no active page) | **3** (`global-furniture`, `manufacturers-we-support`, `teknion-upscale-products`) |

---

## Brand-by-brand status table

| Brand | Page handle | Page exists | Collection handle | Product count | Status | Notes |
|---|---|---|---|---|---|---|
| Global Furniture Group + Teknion | `brands-global-teknion` | ✅ published | `global-teknion` (smart) | **56** | **Healthy** | Page bundles Global + Teknion together. GFG is standalone callable; Teknion is separate canonical brand with 0 enriched products. See cross-reference section. |
| Keilhauer | `brands-keilhauer` | ✅ published | `keilhauer` (smart) | **0** | **Empty** | DEBT-01. Smart collection rule `TAG EQUALS 'brand:keilhauer'` — no products tagged yet. |
| ergoCentric | `brands-ergocentric` | ✅ published | `ergocentric` (smart) | **0** | **Empty** | DEBT-02. Smart collection rule `TAG EQUALS 'brand:ergocentric'` — no products tagged yet. |
| Brands Hub | `brands` | ✅ published | _(hub page, no collection)_ | n/a | **Hub** | Aggregator page listing Keilhauer, ergoCentric, Global, Teknion. Will need updating after BRAND-PAGES-1 ships. |
| OTG / Offices to Go | _(none)_ | ❌ | _(none)_ | — | **Missing-page** | 54 enriched products. Callable. Highest-volume brand in catalog. No page, no collection. |
| Heartwood Manufacturing Ltd. | _(none)_ | ❌ | _(none)_ | — | **Missing-page** | 17 enriched products. Callable. No page, no collection. |
| ObusForme | _(none)_ | ❌ | _(none)_ | — | **Missing-page** | 5 enriched products. Callable per ICP recognition. No page, no collection. |
| — | `global-furniture` (custom) | ❌ | `global-furniture` (custom) | **0** | **Stale collection** | Legacy custom collection — no matching brand page. Likely pre-dates the brand page system. |
| — | `manufacturers-we-support` (custom) | ❌ | `manufacturers-we-support` (custom) | **0** | **Stale collection** | Legacy editorial collection — no matching page, 0 products. |
| — | `teknion-upscale-products` (custom) | ❌ | `teknion-upscale-products` (custom) | **0** | **Stale collection** | Legacy Teknion-specific collection — 0 products. Redundant with `global-teknion` smart collection. |

---

## Cross-reference with canonical brand map (VENDOR-NORMALIZE-1)

### Callable brands (from VENDOR-NORMALIZE-1)

| Canonical brand | Enriched products | Page | Collection products | Assessment |
|---|---|---|---|---|
| **OTG / Offices to Go** | 54 | ❌ None | ❌ None | **NEEDS BRAND-PAGES-1** — highest-volume callable brand with zero storefront presence |
| **Global Furniture Group** | 53 | ⚠️ Partial (`brands-global-teknion` bundles GFG + Teknion) | ✅ `global-teknion` (56 products) | **NEEDS DECISION** — see note below |
| **Heartwood Manufacturing Ltd.** | 17 | ❌ None | ❌ None | **NEEDS BRAND-PAGES-1** |
| **ObusForme** | 5 | ❌ None | ❌ None | **NEEDS BRAND-PAGES-1** |

**Global Furniture Group note:** The existing `brands-global-teknion` page bundles Global and Teknion together under one landing experience. VENDOR-NORMALIZE-1 resolved these as two separate canonical brands (Global Furniture Group callable, Teknion not callable / 0 enriched). Two options for BRAND-PAGES-1:

- **Option A — Keep bundled:** Rename the page and collection to `brands-global` and expand scope to cover GFG (Global + OTG + ObusForme family) as one brand experience. Faster, one page to maintain.
- **Option B — Split:** Separate GFG page (`brands-global`) from the Teknion mention. Teknion's page becomes optional/deferred (0 enriched products; callable=False). Cleaner canonical alignment but more work.

Steve decides. Both options are compatible with BRAND-PAGES-1.

### Non-callable brands with existing infrastructure

| Canonical brand | Callable | Reason | Page | Collection | Recommendation |
|---|---|---|---|---|---|
| **Keilhauer** | False | 0 enriched products | ✅ Exists | `keilhauer` (0) | Keep live — B2B lead-capture page has value; restore callouts in COLLECTION-CLEANUP-1 post-PE Pass 3 |
| **ergoCentric** | False | 1 enriched product, below threshold | ✅ Exists | `ergocentric` (0) | Keep live — same logic as Keilhauer; re-evaluate post-PE Pass 3 |

### Pages referencing brands not in canonical map

None. All 4 existing brand pages map to brands that are in the canonical map (Global Furniture Group, Teknion, Keilhauer, ergoCentric). No stale aspirational pages found.

---

## Theme template / section reusability

### Architecture: hand-built one-offs, not a shared template

Each brand page uses a **unique dedicated section file** with its own hardcoded copy:

| Section file | Schema name | Template JSON | CSS scope class | Reusable? |
|---|---|---|---|---|
| `theme/sections/ds-lp-brands.liquid` | "Brands Hub" | `page.brands.json` | `.lp-brands` | No — hub-specific layout |
| `theme/sections/ds-lp-brands-keilhauer.liquid` | "Keilhauer Brand Page" | `page.brands-keilhauer.json` | `.lp-keilhauer` | No — Keilhauer-specific copy hardcoded |
| `theme/sections/ds-lp-brands-global-teknion.liquid` | "Global & Teknion Brands" | `page.brands-global-teknion.json` | `.lp-global` | No — Global/Teknion-specific copy hardcoded |
| `theme/sections/ds-lp-brands-ergocentric.liquid` | "ergoCentric Brand Page" | `page.brands-ergocentric.json` | `.lp-ergo` | No — ergoCentric-specific copy hardcoded |

### Pattern observed in all three brand pages

Each section shares identical structural code:
1. Same Google Fonts `<link>` block
2. Same CSS design token block (scoped to `.lp-<brand>` root class)
3. Same BBI component CSS (`.bbi-btn`, `.bbi-mono`, nav/footer styles)
4. Same Liquid: `{%- render 'bbi-nav' -%}` … content … `{%- render 'bbi-footer' -%}`
5. Minimal schema: only `logo` (image_picker), `heading` (text), `subheading` (textarea), `hero_image` (image_picker)

All substantive content — product highlights, differentiators, specs, FAQ — is **hardcoded HTML/Liquid**, not schema settings. This means:
- Adding a new brand page = copy an existing section file, swap the hardcoded copy, rename the CSS scope class.
- No Theme Editor control over body content.
- Consistent with the existing ds-lp-* pattern used across all 10+ landing pages in this codebase.

### Implication for BRAND-PAGES-1

BRAND-PAGES-1 has two approaches:

**Approach A — Continue the existing pattern (copy + specialise)**
Duplicate `ds-lp-brands-ergocentric.liquid` for each new brand, hardcode that brand's copy, ship. Estimated 30–45 min per page. Produces one more section file per brand. Consistent with how Keilhauer, Global, ergoCentric were built.

**Approach B — Build a generic `ds-lp-brand.liquid` section with schema-driven content**
One section file handles all brand pages via settings (brand name, tagline, feature bullets, FAQ items, collection handle for the product grid). More upfront work (~3–4 hrs to build the generic section) but each subsequent brand page is a template JSON edit only — no code push required. Also resolves the DEBT-10 Google Fonts duplication issue (one section = one font load).

Given BBI needs at least 3 new brand pages (OTG, Heartwood, ObusForme) and potentially a redesigned Global page, Approach B amortizes quickly. But this is a scope call for BRAND-PAGES-1, not this audit.

---

## Recommended actions for BRAND-PAGES-1 scope

_These are inputs for Steve's scoping decision, not a committed plan._

**Build — callable brands with product depth, no current page:**

- **OTG / Offices to Go brand page** (`/pages/brands-otg`)
  Create brand page + new smart collection `otg` (rule: vendor = "OTG / Offices to Go" OR tag = "brand:otg" — to be defined after VENDOR-NORMALIZE-2 normalises vendor fields). 54 enriched products available. Highest-priority new page.

- **Heartwood Manufacturing Ltd. brand page** (`/pages/brands-heartwood`)
  Create brand page + new smart collection `heartwood` (rule: vendor = "Heartwood Manufacturing Ltd." after VENDOR-NORMALIZE-2). 17 enriched products. Tables/boardroom specialist — strong differentiator copy available.

- **ObusForme brand page** (`/pages/brands-obusforme`)
  Create brand page + new smart collection `obusforme` (rule: vendor = "ObusForme" — already partially correct in Shopify vendor field for 5 products). 5 enriched products. ICP-referenced ergonomic brand; callable per VENDOR-NORMALIZE-1.

**Decide — existing partial infrastructure:**

- **Global Furniture Group + Teknion page** (`/pages/brands-global-teknion`)
  Choose Option A (keep bundled as GFG-family page) or Option B (split into standalone GFG page + defer Teknion). Current `global-teknion` smart collection is healthy at 56 products. No urgent rebuild needed — the existing page works; this is a copy/scope alignment question.

**Keep live, no rebuild needed:**

- **Keilhauer** (`/pages/brands-keilhauer`) — keep published; restore callouts post-PE Pass 3.
- **ergoCentric** (`/pages/brands-ergocentric`) — keep published; restore callouts post-PE Pass 3.
- **Brands Hub** (`/pages/brands`) — keep published; update featured brand tiles after new pages ship.

**Flag for COLLECTION-CLEANUP-1:**

- `global-furniture` (custom, 0 products) — likely superseded by `global-teknion` smart collection; candidate for deprecation.
- `manufacturers-we-support` (custom, 0 products) — no active page or purpose visible; candidate for deprecation.
- `teknion-upscale-products` (custom, 0 products) — redundant with `global-teknion`; candidate for deprecation.
