# Stage 2 — Stabilize Chrome — Summary
**Date:** 2026-05-07  
**Branch:** `chore/stabilize-chrome-2026-05-07`  
**Scope:** Structural refactor only — no design changes, no section content changes.

---

## Objective
Make every BBI page chrome-identical at the header, footer, and breadcrumb level so Stage 3+ design work has a stable substrate.

---

## Step 2.1 — Gate Refactor

**What changed:** `theme/layout/theme.liquid` — the `bbi_landing` gate was a one-liner compound condition. Replaced with a clean multi-line `elsif` chain (one suffix per line) with a comment pointing to the reference list.

**New file:** `theme/snippets/bbi-landing-gate.liquid` — documentation-only (not rendered). Explains the Shopify `render` isolation constraint and lists all BBI templates.

**Constraint discovered:** Shopify's `render` tag is fully isolated — variables assigned inside cannot be accessed by the calling layout, and `capture` + `render` does not propagate output. Gate logic must stay inline in `theme.liquid`.

---

## Step 2.2-2.3 — Header / Footer Parity

**Pre-existing gap found:** 4 sections had hand-rolled `<header class="bbi-header">` blocks (flat nav, 5 `<a>` links) instead of `render 'bbi-nav'`. Fixed in commit `a7b5a84`.

**Sections fixed:** `ds-lp-relocation`, `ds-lp-delivery`, `ds-lp-contact`, `ds-lp-our-work`

**Parity mechanism:** `bbi-nav` and `bbi-footer` are single shared snippets → parity is guaranteed by construction. Footer takes no parameters → byte-identical across all pages. Header differs only in `active` param → correct by design.

**Stage 5 gap (documented):** PDPs (`template == 'product'`) and the 404 page have no BBI chrome section yet. Noted in audit CSVs.

**Reports:**
- `data/reports/header-parity-stage-2.csv` (pre-refactor baseline)
- `data/reports/footer-parity-stage-2.csv` (pre-refactor baseline)

---

## Step 2.4 — bbi-crumbs Snippet

### New snippet: `theme/snippets/bbi-crumbs.liquid`

Unified breadcrumb band. Accepts `c2_label`, `c2_href`, `c3_label`, `c3_href`, `c4_label`. Level 1 (Home) always rendered. Depth pattern locked:

| Depth | Usage | Example |
|-------|-------|---------|
| 2-level | Top-level pages | Home › Contact |
| 3-level | Industry / brand sub-pages | Home › Industries › Healthcare |
| 4-level | Sub-collections | Home › Shop Furniture › Seating › Task Seating |

**Snippet hash:** `8a8ab7cc`

### Sections migrated (22 total):

**Landing pages (20):** All `ds-lp-*.liquid` sections — inline `<div class="lp-crumbs-band">` (or `<nav class="bbi-crumbs-band">`) replaced with `render 'bbi-crumbs'`. Orphaned section-scoped crumbs CSS removed.

**Collection hub (1):** `ds-cc-base.liquid` — replaced `<nav class="ds-cc__crumbs-band">` with conditional render (2-level if no parent label, 3-level if parent label set). Uses schema settings `breadcrumb_parent_label` and `breadcrumb_parent_url`.

**Sub-collection (1):** `ds-cs-base.liquid` — replaced `<nav class="ds-cs__crumbs-band">` with 4-level render using `parent_title`, `parent_handle`, `page_title` vars (already computed at top of section).

### Crumb render calls by section:

| Section | Render call |
|---------|-------------|
| ds-lp-about | `c2_label: 'About Us'` |
| ds-lp-brands | `c2_label: 'Brands'` |
| ds-lp-brands-ergocentric | `c2_label: 'Brands', c2_href: '/pages/brands', c3_label: 'ergoCentric'` |
| ds-lp-brands-global-teknion | `c2_label: 'Brands', c2_href: '/pages/brands', c3_label: 'Global / Teknion'` |
| ds-lp-brands-keilhauer | `c2_label: 'Brands', c2_href: '/pages/brands', c3_label: 'Keilhauer'` |
| ds-lp-contact | `c2_label: 'Contact'` |
| ds-lp-customer-stories | `c2_label: 'About', c2_href: '/pages/about', c3_label: 'Customer Stories'` |
| ds-lp-delivery | `c2_label: 'Delivery &amp; Installation'` |
| ds-lp-design-services | `c2_label: 'Design Services'` |
| ds-lp-education | `c2_label: 'Industries', c2_href: '/pages/industries', c3_label: 'Education'` |
| ds-lp-faq | `c2_label: 'FAQ'` |
| ds-lp-government | `c2_label: 'Industries', c2_href: '/pages/industries', c3_label: 'Government'` |
| ds-lp-healthcare | `c2_label: 'Industries', c2_href: '/pages/industries', c3_label: 'Healthcare &amp; Clinical'` |
| ds-lp-industries | `c2_label: 'Industries'` |
| ds-lp-non-profit | `c2_label: 'Industries', c2_href: '/pages/industries', c3_label: 'Non-Profit'` |
| ds-lp-oecm | `c2_label: 'OECM Purchasing'` |
| ds-lp-our-work | `c2_label: 'About', c2_href: '/pages/about', c3_label: 'Our Work'` |
| ds-lp-professional-services | `c2_label: 'Industries', c2_href: '/pages/industries', c3_label: 'Professional Services'` |
| ds-lp-quote | `c2_label: 'Request a Quote'` |
| ds-lp-relocation | `c2_label: 'Relocation Management'` |
| ds-cc-base | conditional 2-level/3-level via schema `breadcrumb_parent_label` |
| ds-cs-base | 4-level: Shop Furniture › `parent_title` › `page_title` |

---

## Step 2.5 — Post-Refactor Parity Audit

| Metric | Result |
|--------|--------|
| Sections fully compliant (nav + footer + crumbs) | **22 / 22** |
| bbi-nav snippet hash | `f134716c` — identical across all pages |
| bbi-footer snippet hash | `374e4670` — byte-identical, zero parameters |
| bbi-crumbs snippet hash | `8a8ab7cc` — single source of truth |
| Inline crumbs HTML remaining | 0 |
| Orphaned crumbs CSS remaining | 0 |

**Reports:**
- `data/reports/header-parity-post-stage-2.csv`
- `data/reports/footer-parity-post-stage-2.csv`
- `data/reports/crumbs-post-stage-2.csv`

---

## Known Gaps (Stage 5)

- **PDPs** (`template == 'product'`) — no BBI chrome section
- **404 page** (`template == '404'`) — no BBI chrome section

These are outside Stage 2 scope. Documented in parity CSVs.

---

## Files Changed (net change vs `main`)

| File | Change |
|------|--------|
| `theme/layout/theme.liquid` | Gate rewritten as clean elsif chain |
| `theme/snippets/bbi-landing-gate.liquid` | New — documentation only |
| `theme/snippets/bbi-crumbs.liquid` | New — unified breadcrumb snippet |
| `theme/sections/ds-lp-*.liquid` (20 files) | Inline crumbs replaced with render call; orphaned CSS removed |
| `theme/sections/ds-cc-base.liquid` | Crumbs replaced; ds-cc__crumbs CSS removed |
| `theme/sections/ds-cs-base.liquid` | Crumbs replaced; ds-cs__crumbs CSS removed |
| `data/reports/stage-2-url-set.csv` | New — 15-URL test set |
| `data/reports/header-parity-stage-2.csv` | New — pre-refactor header baseline |
| `data/reports/footer-parity-stage-2.csv` | New — pre-refactor footer baseline |
| `data/reports/header-parity-post-stage-2.csv` | New — post-refactor header audit |
| `data/reports/footer-parity-post-stage-2.csv` | New — post-refactor footer audit |
| `data/reports/crumbs-post-stage-2.csv` | New — post-refactor crumbs audit |
