# Stage 4a — PDP Plumbing Verification

**Date:** 2026-05-07  
**Dev theme:** 186373570873  
**Status:** ⚠️ PARTIAL — gate wired, section + template missing

---

## Component Inventory

| Component | Status | Path | Notes |
|---|---|---|---|
| `product.json` template | ❌ MISSING | `theme/templates/product.json` | Not created. Shopify falls back to default product template which renders `main-product.liquid`. |
| `ds-pdp-base.liquid` section | ❌ MISSING | `theme/sections/ds-pdp-base.liquid` | The BBI-designed PDP section has never been built. |
| `bbi_landing` gate — `template == 'product'` | ✅ DONE | `theme/layout/theme.liquid:90–91` | Gate correctly catches `template == 'product'`, sets `bbi_landing = true`. |
| BBI nav rendered on PDPs | ❌ NOT YET | `ds-pdp-base.liquid` must call `render 'bbi-nav'` | Gate suppresses Starlite `header-group`, but BBI nav not rendered because the section doesn't exist. |
| BBI footer rendered on PDPs | ❌ NOT YET | `ds-pdp-base.liquid` must call `render 'bbi-footer'` | Same reason. |
| Starlite chrome suppressed on PDPs | ✅ EFFECTIVE | `theme/layout/theme.liquid:136` | `unless bbi_landing` block correctly skips `header-group` + `footer-group` for products. |
| `bbi-crumbs` breadcrumb snippet | ❌ MISSING | `theme/snippets/bbi-crumbs.liquid` | No BBI-specific breadcrumb snippet exists. `breadcrumb.liquid` exists but is the stock Starlite version. |
| `bbi-oecm-bar` shared snippet | ✅ EXISTS | `theme/snippets/bbi-oecm-bar.liquid` (inherited from Stage 3.x) | Shared across LP pages; reuse on PDP. |

---

## What Currently Renders on a Product URL

A product URL on dev theme 186373570873 renders:

1. **No BBI nav** — suppressed by gate, not replaced
2. **Stock `main-product.liquid` section** — the Starlite theme's product section (gallery + blocks, no BBI styling)
3. **No BBI footer** — suppressed by gate, not replaced
4. **No spec table**, **no trust pills**, **no brand block**, **no breadcrumbs**, **no Quote CTA**
5. **Starlite recently-viewed JS** still executes via the `main-product.liquid` script block

In effect, PDPs currently render as a bare product gallery + block area with no chrome. The `bbi_landing` gate suppression works but creates a chrome void.

---

## PB-PDP-1 Re-assessment

The build-state doc marks PB-PDP-1 ("Extend `bbi_landing` gate for `template == 'product'`") as ⬜ not done. 

**Actual status: ✅ DONE.** The gate already includes:
```liquid
elsif template == 'product'
  assign bbi_landing = true
```
at `theme/layout/theme.liquid:90–91`. This was likely added during Stage 1 or earlier. PB-PDP-1 can be marked complete.

---

## Blockers for Stage 4b

Stage 4b cannot ship until both missing components are built in a single pass:

1. `theme/templates/product.json` — wires the `ds-pdp-base` section to product URLs
2. `theme/sections/ds-pdp-base.liquid` — the full BBI PDP section

No separate "Stage 5 (plumbing) precursor" is needed — these are Stage 4b deliverables, not a separate stage.

---

## Verdict

**Plumbing status: NEEDS STAGE 4b** (not a separate plumbing stage — 4b *is* the build). Gate is done. Section + template are the build.
