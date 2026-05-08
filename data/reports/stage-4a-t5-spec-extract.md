# Stage 4a — T5 Layout Spec Extract

**Source:** `docs/strategy/bbi-screens-audit-v1.md` (T5 section)  
**Date:** 2026-05-07  
**Status:** Spec LOCKED — extracted from Claude Design T5 locked screen (`screens-t5-2026-05-04/pdp-unbuyable/`)

---

## T5 Section Order (top → bottom)

| # | Section | Component Class | Visual Position | Required Content | State Variation |
|---|---|---|---|---|---|
| 1 | Header | `.bbi-header` | Top, full-width | Logo, nav (`current="shop"`), phone, cart, RFQ CTA | Shared — no variation |
| 2 | Breadcrumbs | `.pd-crumb-band` | Below header | Home → Shop → [Category] → [Subcategory] → [Product] (5 levels) | Always shown |
| 3 | Hero — gallery | `.pd-gallery` | Left column, ~55% width | 6-image thumbnail strip + main 4:5 slot; zoom on click | Always shown; fewer images if product has < 6 |
| 4 | Hero — product info | `.pd-info` | Right column | Title · brand parent line · model code · standfirst · badge row (OECM · Canadian-made · Sold-out) | Badge row changes per product state |
| 5 | Commerce block | `.pd-commerce .scheme-alt` | Right column, below info | Buyable: qty stepper + price + stock dot + Add-to-Cart. Unbuyable: eyebrow + heading + sub + RFQ CTA + phone link + trust line | **Two states — buyable vs unbuyable** |
| 6 | Description | `.pd-description` | Below hero, full-width | 3 paragraphs + `bestFor` callout block | Hidden if description empty |
| 7 | Spec table | `.pd-spec-table` | Below description | Dimensions · weight · materials · key features · certifications | Hidden row-by-row when metafield empty |
| 8 | Variants section | `.pd-variants` | Below spec table | Multi-variant chip picker | Hidden on single-variant products |
| 9 | OECM bar | `.bbi-oecm-bar` | Full-width band | Shared OECM trust bar (from Stage 3.x) | Always shown |
| 10 | Related products | `.pd-related` | Below OECM bar | 4 `.bbi-card--product` cards | Hidden if fewer than 2 related found |
| 11 | Brand block | `.pd-brand-block` | Below related products | Brand logo + blurb + "authorized dealer" badge + "View all [Brand]" link | Show only when vendor is a named brand with assets |
| 12 | CTA closer | `.bbi-cta-section .scheme-inverse` | Second-to-last | Standard charcoal-canvas RFQ section | Always shown |
| 13 | Footer | `.bbi-footer` | Bottom, full-width | Standard BBI footer | Always shown |

---

## Buyable vs Unbuyable Logic (BBI Rule #2)

**Buyable condition:** `product.price > 0 AND product.available == true`  
**Unbuyable condition:** `product.price == 0 OR product.available == false`

| Element | Buyable | Unbuyable |
|---|---|---|
| Commerce block | Qty stepper + price display + green stock dot + Add-to-Cart button | RFQ CTA block (`.bbi-cta-pdp` from component-spec-v1 §07b) — "Request a Quote" primary CTA + phone fallback + "We respond within 1 business day" microcopy |
| Sold-out badge | Hidden | `.bbi-badge--sold` shown (gray, top-right of gallery) |
| Add-to-Cart | Shown | Hidden entirely — do not render a disabled ATC |

---

## Badge Row (`pd-info`) — Tag Driver Requirements

The badge row in `.pd-info` shows up to 3 inline badges:
- **OECM** badge — driven by: tag `oecm-eligible` on the product
- **Canadian-made** badge — driven by: tag `canadian-made` on the product  
  Uses `.bbi-badge--canadian` SVG maple-leaf variant from component-spec-v1 §04
- **Sold-out** badge — driven by: `product.available == false`

**Current tag coverage: 0%** — neither `oecm-eligible` nor `canadian-made` exists in the tag taxonomy. See Phase 6 report.

---

## Spec Table — Metafield Mapping

| Row label | Metafield | Behavior when blank |
|---|---|---|
| Dimensions | `product.metafields.specs.dimensions` | Hide row |
| Weight | `product.metafields.specs.weight` | Hide row |
| Materials | `product.metafields.specs.materials` | Hide row |
| Key features | `product.metafields.specs.key_features` | Hide row |
| Certifications | `product.metafields.specs.certifications` | Hide row |
| Country of manufacture | `product.metafields.specs.country_of_manufacture` | Hide row |
| Manufacturer | `product.metafields.specs.manufacturer` | Hide row |
| Product line | `product.metafields.specs.product_line` | Hide row |

**Note:** `key_features` and `certifications` are stored as JSON arrays on Shopify (`list.single_line_text_field` type). Liquid must parse with `| parse_json` or iterate directly.

---

## Component Dependencies

New shared snippets required for `ds-pdp-base.liquid`:

| Snippet | Status | Source |
|---|---|---|
| `bbi-nav.liquid` | ✅ Exists | Reuse from LP pages |
| `bbi-footer.liquid` | ✅ Exists | Reuse from LP pages |
| `bbi-oecm-bar.liquid` | ✅ Exists | Reuse from Stage 3.x |
| `bbi-product-jsonld.liquid` | ❌ Missing | PDP-2 build task |
| `bbi-breadcrumb-jsonld.liquid` | ❌ Missing | AI-6 build task |
| `bbi-crumbs.liquid` | ❌ Missing | New — 5-level product breadcrumb |

---

## Open Questions / Spec Gaps

| # | Gap | Decision Needed |
|---|---|---|
| G-1 | Breadcrumb depth discrepancy | build-state PDP-1 says "4-level" but T5 locked screen shows 5 levels (Home → Shop → Category → Subcategory → Product). Which is correct? Likely 5 — the locked screen is authoritative. |
| G-2 | `bestFor` callout in Description | Component-spec-v1 doesn't define this block. Is it a fixed text block, a metafield, or rendered only when `product.metafields.specs.key_features` has a "Best for:" entry? |
| G-3 | `.scheme-alt` commerce block | design-system.md defines only `.scheme-default` and `.scheme-inverse`. The T5 spec uses `.scheme-alt` for the commerce block. Is this a light-gray variant (like `#FAFAFA` canvas)? Needs explicit definition. |
| G-4 | Brand block vendor matching | The vendor field on Shopify doesn't consistently match brand name (many ergoCentric-line products are filed under "Brant Business Interiors" or "Global Furniture Group"). How should brand block know to show ergoCentric vs. Global vs. None? Tag-based? Metafield-based? |
| G-5 | Related products query | "same `type:*` tag, max 4" (from build-state). But `type:*` is only on ~subset of products. Fallback strategy when < 2 related products found? |
| G-6 | "View all [Brand]" link target | Brand pages exist (`/pages/brands-ergocentric` etc.) but vendor-filtered collections (SMART-1) don't exist yet. Should "View all" link to page or collection? |
| G-7 | Hero stats line | T3 collection pages have a stats band (count, delivery promise, OECM badge). T5 does NOT — confirmed no hero stats line on PDP. The badge row in `.pd-info` covers trust signals inline. |
| G-8 | Variant picker styling | build-state PDP-1 is silent on variant rendering. Feedback memory says colour swatches must be visual (filled chip in actual colour), not text labels. Needs wiring in `ds-pdp-base`. |

---

## Confirmed Inherited Decisions

- OECM badge styling → matches design system (Stage 3.0)  
- Logo → `bbi-logo-v2.png` (Stage 3.0)  
- Maple-leaf icon → SVG inline (pattern from `bbi-footer.liquid`)  
- Parent breadcrumb → collection metafield `bbi.parent_hub_handle` exists on collections (Stage 3.2c.5) — confirm whether product breadcrumb should read this from the product's first collection or use a different approach
