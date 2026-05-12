# Stage 3.1a — T3 Spec Extract

**Generated:** 2026-05-07  
**Source:** `docs/strategy/bbi-screens-audit-v1.md` § "T3 — Collection · sub"  
**Read alongside:** `docs/strategy/bbi-component-spec-v1.md`, `docs/strategy/design-system.md`

---

## T3 Definition

**Template name:** Collection — sub  
**Canonical route:** `/collections/seating` (generalizes to all 9 Level-2 hubs)  
**Design round:** T3  
**Source file:** `screens-t3-LOCKED-2026-04-29/src/Collection.jsx`  
**Status:** LOCKED

"Data-driven: swap `CN_CATEGORY` + `CN_PRODUCTS` data block — same component renders Desks, Storage, Tables, etc."

---

## Section Inventory (top → bottom)

| # | Section | Component class | Position | Notes |
|---|---|---|---|---|
| 1 | Header | `.bbi-header` | ATF | Shared — same as T1/T2 |
| 2 | Breadcrumbs | `.cn-crumb-band` | ATF | "Home → Shop → {Category}" |
| 3 | Intro band | `.cn-intro` | ATF | H1 · standfirst · brand count · warranty headline |
| 4 | Sub-category filter | `.cn-filter-bar` | ATF+1 | Pill-style filter strip for sub-cats |
| 5 | Product grid | `.cn-product-grid` | ATF+1 | `.bbi-card--product` data-driven; buyable vs. unbuyable CTA split |
| 6 | Brand plates | `.cn-brand-section` | Below grid | 8 brands with Canadian + authorized badges |
| 7 | Pagination | `.cn-pagination` | Below grid | 5-page strip |
| 8 | OECM bar | (shared) | Pre-footer | Reused from T1/T2 |
| 9 | CTA closer | `.bbi-cta-section .scheme-inverse` | Pre-footer | Charcoal canvas inverse scheme |
| 10 | Footer | `.bbi-footer` | Bottom | Shared |

---

## Per-Element Detail

### 1. Header (`.bbi-header`)
- Shared snippet — `bbi-nav.liquid` in current codebase
- Active nav: `shop` (Shop Furniture)
- No change expected from current

### 2. Breadcrumbs (`.cn-crumb-band`)
- Three levels: Home → Shop → {Category}
- Current: `bbi-crumbs` snippet renders this (c2 = "Business Furniture", c3 = category title)
- Functionally correct; CSS class name differs from T3 spec but renders same content

### 3. Intro Band (`.cn-intro`)
- **H1:** category title (e.g., "Seating")
- **Standfirst:** 1–2 sentence category description
- **Brand count:** e.g., "16 categories · 30+ brands" — exact copy NOT specified per collection in screens doc
- **Warranty headline:** e.g., "OECM-eligible · Quote in 1 business day" — exact copy NOT specified
- **GAP A:** Brand count and warranty headline copy is not spelled out in the spec for each of the 9 hubs. Assumed to be the existing `hero_subtitle` field extended with these two stat lines.

### 4. Sub-Category Filter (`.cn-filter-bar`)
- Pill-style horizontal strip
- Intended to filter the product grid by sub-category
- **GAP B:** The spec uses the label "sub-cats" but does not clarify:
  - Option A — pills link OUT to sub-collections (navigation, no JS filtering needed)
  - Option B — pills filter the product grid by `subcategory:*` tags (requires tag data)
- **Current tag census result:** `subcategory:` namespace has 0/653 products tagged (0% coverage). Option B is not viable without a tagging pass.
- **Recommendation:** Treat as navigation pills (Option A) in 3.1b, linking to sub-collection handles already defined in tile blocks. Defers tag-based filtering to 3.1c.

### 5. Product Grid (`.cn-product-grid`)
- Uses `.bbi-card--product` component
- Data-driven: reads `collection.products` Liquid object
- Buyable vs. unbuyable CTA split: buyable → "Add to Cart"; unbuyable → "Request a Quote"
- **GAP C:** Spec does not define grid column count (desktop/mobile), card sort order, or products-per-page count. T3 source shows 12 cards with a 4-column desktop layout (inferred from the 5-page pagination strip with assumed 12/page = ~60 products before page 2).
- **GAP D:** "Unbuyable" detection logic not specified. Current BBI rule: sold-out + $0-price + showcase products are unbuyable. Must match existing PDP logic.

### 6. Brand Plates (`.cn-brand-section`)
- Shows 8 brand tiles with:
  - Brand logo
  - Canadian-made badge (maple leaf) where applicable
  - "Authorized dealer" badge
- **GAP E:** The spec says "8 brands" but does NOT list which 8 brands per hub. The current `brand_callout` blocks only cover 0–2 brands per hub. The full set of 8 and their per-hub relevance is unspecified.
- **GAP F:** "Canadian + authorized badges" styling is not detailed — size, position, token. Closest reference: maple-leaf badge from T1 homepage and OECM landing page.

### 7. Pagination (`.cn-pagination`)
- 5-page strip (1 · 2 · 3 · 4 · 5 with prev/next)
- Shopify native: `paginate` tag with `by: 12` (assumed, not confirmed)
- **GAP G:** Products-per-page count not specified. Must be confirmed or a schema setting.

### 8. OECM Bar (shared)
- Appears on T1, T2, and T3 templates
- No shared snippet exists yet (`theme/snippets/` has `bbi-nav`, `bbi-footer`, `bbi-crumbs` only)
- Currently implemented as inline HTML within T4 landing page section
- **GAP H:** OECM bar is referenced as "shared" in the spec but has no shared Liquid snippet. A new `bbi-oecm-bar.liquid` snippet must be created. Content/tokens are in `ds-lp-oecm.liquid` but not extracted.

### 9. CTA Closer (`.bbi-cta-section .scheme-inverse`)
- Charcoal canvas, white text, white primary button (red on hover)
- Current: `.ds-cc__phone-cta` renders phone number + "Request a Quote" button — functionally equivalent
- Class name differs; content matches intent. Minor restyle may be needed.

### 10. Footer (`.bbi-footer`)
- Shared — `bbi-footer.liquid` snippet
- No change expected

---

## T3 Spec Gaps Summary

| ID | Element | Gap description | Severity |
|---|---|---|---|
| GAP-A | Intro band | Brand count + warranty headline copy not specified per hub | Medium — needs copywriting pass before build |
| GAP-B | Sub-cat filter | Filter pills: navigation vs. tag-filtering not disambiguated | High — blocks filter implementation; resolve before 3.1b |
| GAP-C | Product grid | Grid column count + products-per-page not specified | Low — infer 4-col / 12-per-page from T3 render |
| GAP-D | Product grid | "Unbuyable" detection criteria not specified | Low — reuse existing BBI rule (sold-out / $0 / showcase) |
| GAP-E | Brand plates | Which 8 brands per hub not listed | High — blocks brand-section build |
| GAP-F | Brand plates | Canadian + authorized badge styling (tokens/size/position) | Medium — reference T1 maple-leaf badge |
| GAP-G | Pagination | Products-per-page count not specified | Low — default to 12 |
| GAP-H | OECM bar | No shared snippet exists; inline only in T4 section | Medium — create `bbi-oecm-bar.liquid` snippet in 3.1b |

**Total spec gaps: 8** (2 high, 3 medium, 3 low)

---

## Component Dependencies

| New component needed | Type | Notes |
|---|---|---|
| `.cn-filter-bar` | Inline CSS + Liquid | DEFER to 3.1c (0% tag coverage) |
| `.cn-product-grid` / `.bbi-card--product` | Inline or snippet | NEW — core 3.1b deliverable |
| `.cn-brand-section` | Inline or snippet | NEW — requires GAP-E resolution |
| `.cn-pagination` | Inline Liquid | Use Shopify `paginate` tag |
| `bbi-oecm-bar.liquid` | Shared snippet | Extract from `ds-lp-oecm.liquid` |

---

## Token Coverage for T3

Per `docs/strategy/bbi-screens-audit-v1.md` token matrix:

| Token group | T3 usage |
|---|---|
| Background | ✓ |
| Heading/text color | ✓ |
| Button (primary + secondary) | ✓ |
| Card (border + shadow) | ✓ |
| Badge (sold, sale, new) | ✓ (product grid) |
| Inverse scheme (charcoal) | ✓ (CTA closer) |
| `--saleBadgeBackground` | ✓ (filter pill accent?) |

Red density target for T3: ~4.2% default / ~5.0% with hover states.
