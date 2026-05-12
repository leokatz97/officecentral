# Stage 3.1b — T3 Spec Gap Resolutions

**Generated:** 2026-05-07  
**Source gaps from:** `data/reports/stage-3.1a-t3-spec-extract.md`  
**Resolved against:** `docs/strategy/design-system.md` (DS v1, 2026-05-04), `docs/strategy/bbi-component-spec-v1.md` (v1)  
**Status:** All 8 gaps resolved. No halts required.

---

## Gap Resolution Table

| gap_id | resolution_source | resolved_value | unresolved_question_for_user |
|---|---|---|---|
| GAP-A | DS §07 CTA copy rules + component spec §07b microcopy | Schema settings `hero_stats_line1` (default: "30+ commercial furniture brands") + `hero_stats_line2` (default: "OECM-eligible · Quote in 1 business day"). DS mandates the "1 business day" SLA and OECM trust line. Brand count is a schema override per hub. | — |
| GAP-B | User-confirmed decision (Stage 3.1a recon) | Navigation pills only. Each chip routes to `/collections/<sub-handle>` sourced from existing `tile` block `link` settings. No JS tag-filtering. Tag-filtering deferred to Stage 3.1c. | — |
| GAP-C | Component spec §03 Cards + T3 render inference | 4-column desktop grid (≥768px), 2-column mobile (≥480px), 1-column (<480px). Products per page: 12 (schema setting `products_per_page`, default 12). Consistent with DS spacing scale at 1280px max-width with 24px gaps. | — |
| GAP-D | Component spec §03 Cards (explicit) | Unbuyable = `product.available == false OR product.price == 0 OR product.tags contains 'showcase'`. Card renders "Request a Quote" button linking to `/pages/quote?product={{ product.handle }}`. Source: component spec §03: "For unbuyable items (sold-out, $0-price, showcase): card shows 'Request a Quote' button instead of 'Add to Cart'." | — |
| GAP-E | Stage 3.1b Phase 2 (pre-authorized methodology) | Top 8 vendors by product count per hub from Shopify Admin API. Schema override settings per hub for editorial control. Empty hubs fallback: `ergoCentric`, `Keilhauer`, `Global Furniture`, `Teknion` + 4 placeholders ("Brand 5"–"Brand 8"). | — |
| GAP-F | Component spec §04 Badges (explicit) | Canadian badge: `.bbi-badge--canadian` — outlined charcoal, maple-leaf SVG (`aria-hidden="true"`), "Canadian-owned" label. 22px tall, 8/10px padding, 11px/600 font. Authorized dealer: `.bbi-badge--oem` — outlined gray (`--borderColor`). Both positioned inline below brand plate name. Leaf color: `--saleBadgeBackground` (`#D4252A`). | — |
| GAP-G | T3 render inference + Stage 3.1b spec direction | 12 products per page. Exposed as schema setting `products_per_page` (default 12, min 4, max 48). Shopify `paginate` tag wraps the product loop. | — |
| GAP-H | Stage 3.1b Phase 3 (create snippet); content from `ds-lp-oecm.liquid` + DS | New `bbi-oecm-bar.liquid` snippet: self-contained `<style>` + `<aside class="bbi-oecm-bar">`. Agreement copy: "OECM Supplier Partner Agreement 2025-470". Trust line: "Ontario's broader public sector can purchase without re-tendering." Link to `/pages/oecm`. Pattern matches `bbi-footer.liquid` (style block + single BEM root element). | — |

---

## Detailed Resolution Notes

### GAP-A — Intro band copy
The design system §07 Quote-request CTA specifies mandatory microcopy: "We respond within 1 business day" (component spec §07b). The OECM vendor-of-record trust line is confirmed and mandatory per DS principles. The "30+ brands" stat is a schema setting — editors can override per hub once Phase 2 data is available. These go in the hero section as two `<p>` stat lines rendered below the standfirst when `hero_stats_line1` or `hero_stats_line2` are non-blank.

### GAP-B — Sub-category filter
Pre-resolved by user decision. Pills are generated from the `tile` block `link` + `title` settings already in each `collection.<handle>.json`. The filter bar renders only when `tile_count > 0`. Chips are `<a>` tags styled as pills using DS tokens: `--borderColor` border, `--cardRadius 999px`, `--alternateBackground` surface, charcoal text.

### GAP-C — Grid column count
DS spacing: 1280px max-width container, 24px (`--space-6`) gap, 4-column grid = `(1280 - 48 - 2×24) / 4 = ~296px` per card. Product card uses 4:5 ratio per component spec §03. 4-column is confirmed by the T3 locked design screen description.

### GAP-D — Unbuyable detection
Component spec §03 Cards is explicit. The three conditions map to Shopify Liquid as:
- `product.available == false` — sold-out (all variants exhausted)
- `product.price == 0` — $0-price (showcase or custom-quote only)
- `product.tags contains 'showcase'` — explicitly marked showcase

Any of the three → show "Request a Quote" CTA instead of "Add to Cart".

### GAP-E — Which 8 brands per hub
Phase 2 computes this from live Shopify data (vendor counts per collection). Schema `brand_plate` blocks (8 per hub) can be editorially overridden. The brand plates section is suppressed if all 8 `brand_plate_name` settings are blank (fallback-safe).

### GAP-F — Badge styling
Component spec §04 is fully specified. The `.bbi-badge--canadian` variant uses:
- Border: `1px solid rgba(var(--textColor-rgb), 0.5)` (outlined charcoal)  
- Background: `transparent`  
- Maple leaf: inline SVG `fill="currentColor"` with `color: #D4252A` (`--saleBadgeBackground`)  
- The `.bbi-badge--oem` variant uses `--borderColor` border (gray, `#E5E5E7`)

### GAP-G — Pagination
12/page matches the T3 render (5-page strip at ~60 products total). Schema setting allows hub-specific override. Shopify `paginate` tag wraps the product loop; standard `{% if paginate.pages > 1 %}` guard suppresses pagination on small collections.

### GAP-H — OECM bar content
Extracted from `ds-lp-oecm.liquid` schema defaults and DS. The agreement copy "OECM Supplier Partner Agreement 2025-470" appears in `collection.seating.json` intro_text. The snippet renders an `<aside>` with a red dot accent, "OECM vendor of record" badge, agreement number, trust line, and link to `/pages/oecm`. All tokens from DS default scheme.

---

**All 8 gaps resolved. Proceeding to Phase 2.**
