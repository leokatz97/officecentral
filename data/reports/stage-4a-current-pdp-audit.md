# Stage 4a — Current PDP State Audit

**Date:** 2026-05-07  
**Section audited:** `theme/sections/main-product.liquid` (current PDP renderer)  
**Target section:** `theme/sections/ds-pdp-base.liquid` (does not exist — Stage 4b will build it)

---

## Summary

There is no `ds-pdp-base.liquid`. The current PDP renders via the stock Starlite theme section (`main-product.liquid`, 1003 lines). This section is 100% generic — no BBI styling, no spec tables, no trust pills, no brand block, no quote CTA logic. Stage 4b is a **greenfield build**, not an incremental edit of an existing section.

---

## `main-product.liquid` — What Exists

### Schema settings (merchant-configurable)
- Layout mode: sticky or on-scroll
- Image size: auto / landscape / portrait / square
- Bundle products (up to 2)
- Color scheme (Starlite scheme picker)
- Section padding (desktop + mobile)

### Block types defined
- `sku`, `vendor`, `text`, `custom_liquid`, `countdown`, `Icon-with-text`
- `title`, `description`, `size-guide`, `inventory-status`, `product-accordion`
- `custom-content`, `price`, `rating`, `pickup`, `shareicons`
- `query_form`, `quantity_selector`, `variant_picker`, `buttons`
- `complementary_products`, `payment-icons`, `product_variations`, `information_content`
- `@app` (app embed)

### Gallery / image structure
- Delegates to `{% render 'product-featured-media' %}` (Starlite snippet)
- Image size from schema setting; no 4:5 lock, no 6-image thumbnail strip
- Supports media popup via `product-featured-media-popup`

### Spec table render logic
**None.** No metafield reads of any kind. No `product.metafields.*` access anywhere in the section.

### Trust pills logic
**None.** No tag-based badge logic. No OECM, no Canadian-made, no Sold-out badge.

### "About the Brand" block
**None.** No brand block, no vendor-based content, no brand logo, no blurb.

### Related products
**None.** Has `complementary_products` block (App Recommendations API, requires app), not a Liquid-powered related-by-tag query.

### Buyable vs unbuyable CTA logic
**Non-compliant with BBI Rule #2.** The `buttons` block renders Add-to-Cart unconditionally. There is no conditional logic to replace ATC with an RFQ CTA when `product.price == 0` or `product.available == false`. The `query_form` block exists as an optional add-on but is not auto-wired to unbuyable state.

### BBI chrome inclusion
**None.** `main-product.liquid` does not call `render 'bbi-nav'` or `render 'bbi-footer'`. The `bbi_landing` gate suppresses Starlite chrome correctly, but BBI chrome must be explicitly rendered from `ds-pdp-base.liquid`.

### Breadcrumbs
**None.** The stock `breadcrumb.liquid` section exists separately but `main-product.liquid` does not render it. No 5-level product breadcrumb.

### OECM bar
**None.**

### JSON-LD / structured data
**None.** No product schema, no breadcrumb schema.

---

## Gap Table: `main-product.liquid` vs T5 Spec

| T5 Element | In `main-product.liquid` | Gap |
|---|---|---|
| BBI nav | ❌ | Full build required |
| BBI footer | ❌ | Full build required |
| 5-level breadcrumb | ❌ | New `bbi-crumbs` snippet + logic |
| 4:5 gallery + 6-image strip | ❌ | New gallery block |
| Trust badge row (OECM · Canadian · Sold-out) | ❌ | Tag-based conditional logic |
| Unbuyable RFQ CTA block | ❌ | BBI Rule #2 conditional |
| Spec table (8 spec rows) | ❌ | `product.metafields.specs.*` reads |
| Spec table row-level hiding | ❌ | Per-row `{% if != blank %}` |
| Variants section (multi-variant support) | ⚠️ Partial | `variant_picker` block exists but is text-only, not visual swatches |
| OECM bar | ❌ | `render 'bbi-oecm-bar'` |
| Related products (tag-based, max 4) | ❌ | New collection + filter Liquid |
| Brand block | ❌ | Vendor-matched brand copy + assets |
| CTA closer (charcoal canvas) | ❌ | `.bbi-cta-section` from component-spec §07a |
| Product JSON-LD schema | ❌ | PDP-2 task |
| Breadcrumb JSON-LD | ❌ | AI-6 task (shared snippet) |
| BBI design tokens | ❌ | All styling via Starlite scheme classes |

---

## What Can Be Reused

| Asset | Reuse path |
|---|---|
| `bbi-nav.liquid` snippet | `{% render 'bbi-nav', logo: section.settings.logo, active: 'shop' %}` |
| `bbi-footer.liquid` snippet | `{% render 'bbi-footer', logo: section.settings.logo %}` |
| `bbi-oecm-bar.liquid` snippet | `{% render 'bbi-oecm-bar' %}` |
| BBI design tokens (CSS vars) | Copy token block from any `ds-lp-*.liquid` section |
| `.bbi-btn` button classes | Copy from any `ds-lp-*.liquid` section |
| `.bbi-cta-section` CTA closer | Copy from any `ds-lp-*.liquid` section |
| Brand copy + blurbs | Inline from `ds-lp-brands-ergocentric.liquid`, `ds-lp-brands-keilhauer.liquid`, `ds-lp-brands-global-teknion.liquid` |

---

## Verdict

`ds-pdp-base.liquid` is a **greenfield build**. No meaningful Liquid code from `main-product.liquid` carries over into the BBI PDP section. The build starts from the `ds-lp-*.liquid` pattern used across Stage 3 landing pages.
