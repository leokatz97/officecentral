# Stage 3.1c.1 — Hero Stats Line + Sub-cat Pill Counts

**Branch:** `feature/stage-3.1c.1-hero-stats-and-counts`
**Commit:** `5082da9`
**Generated:** 2026-05-07
**Target theme:** dev `186373570873` only
**Live theme `186495992121`:** NOT touched

---

## Phase 1 — Spec Findings

**Source:** `data/reports/stage-3.1c.1-spec-extract.md`

Neither `design-system.md` nor `bbi-component-spec-v1.md` defines a discrete "hero stats strip." All styling is inferred from established analogous patterns.

### Inferred decisions

| Element | Value | Reference pattern |
|---|---|---|
| Label font | JetBrains Mono 10px / uppercase / 0.08em tracking | `.ds-cc__brand-plates-eyebrow` |
| Label color | `rgba(var(--textColor-rgb), 0.5)` | All mono eyebrows in codebase |
| Numeral font | Inter Tight 600 / 22px mobile / 26px ≥768px | Below H2 mobile (24px) so 5 items fit 560px column |
| Numeral color | `var(--headingColor)` | Full charcoal for readability |
| Layout | `flex; flex-wrap: wrap; gap: 16px 24px` | Mirrors `.ds-cc__hero-cta-row` pattern |
| Margin below | `var(--space-6)` (24px) | Consistent DS spacing before CTA row |
| No red eyebrow tick | — | Red tick signals section heading; stats strip is inline in hero block |
| Count badge font | JetBrains Mono 11px / 0.04em tracking / `rgba(textColor, 0.55)` | Subordinate to pill label |

---

## Phase 2 — Hero Stats Line

### HTML structure

```html
<dl class="ds-cc__hero-stats">
  <div class="ds-cc__hero-stats__item">
    <dt>Models</dt>
    <dd>{{ _stat_models }}</dd>
  </div>
  <div class="ds-cc__hero-stats__item">
    <dt>Brands</dt>
    <dd>{{ _stat_brands }}</dd>
  </div>
  <div class="ds-cc__hero-stats__item">
    <dt>Canadian&#8209;made</dt>
    <dd>{{ _stat_canadian }}</dd>
  </div>
  <div class="ds-cc__hero-stats__item">
    <dt>In stock</dt>
    <dd>{{ _stat_instock }}</dd>
  </div>
  <div class="ds-cc__hero-stats__item">
    <dt>Lead time</dt>
    <dd>{{ _stat_lead }}</dd>
  </div>
</dl>
```

### Liquid derivation

| Stat | Liquid | Notes |
|---|---|---|
| Models | `collection.products_count \| default: 0` | Native |
| Brands | `collection.products \| map: 'vendor' \| uniq \| size` | Distinct vendor count |
| Canadian-made | Loop counting `p.tags contains 'canadian-made'` | Tag-based count |
| In stock | `collection.products \| where: 'available', true \| size` | Native availability filter |
| Lead time | `section.settings.lead_time \| default: '2–6 weeks'` | Schema override |

### CSS excerpt

```css
.ds-cc__hero-stats{
  display:flex;flex-wrap:wrap;gap:var(--space-4) var(--space-6);
  margin-bottom:var(--space-6);list-style:none;padding:0;margin-top:0;
}
.ds-cc__hero-stats__item{flex:0 0 auto;}
.ds-cc__hero-stats__item dt{
  font-family:"JetBrains Mono",ui-monospace,monospace;
  font-size:10px;letter-spacing:0.08em;text-transform:uppercase;
  color:rgba(var(--textColor-rgb),0.5);margin:0 0 2px;
}
.ds-cc__hero-stats__item dd{
  font-family:var(--headingFont);font-size:22px;font-weight:600;
  line-height:1.1;letter-spacing:-0.01em;
  color:var(--headingColor);margin:0;
}
@media(min-width:768px){
  .ds-cc__hero-stats__item dd{font-size:26px;}
}
```

### Position in hero

Rendered inside `.ds-cc__hero-text` column — after `hero_subtitle` standfirst (if any), before `.ds-cc__hero-cta-row`. Fits within the 560px max-width column: 5 items × ~88px + 4 gaps × 24px ≈ 536px.

---

## Phase 3 — Sub-cat Pill Count Integration

### Before (Stage 3.1b)

```html
<a class="ds-cc__filter-chip" href="/collections/task-seating">
  Task Chairs
</a>
```

### After (Stage 3.1c.1)

```html
<!-- "All" pill at head of row -->
<a class="ds-cc__filter-chip" href="/collections/seating">
  All
  <span class="ds-cc__filter-pill-count">120</span>
</a>

<!-- Sub-collection pill with count -->
<a class="ds-cc__filter-chip" href="/collections/task-seating">
  Task Chairs
  <span class="ds-cc__filter-pill-count">48</span>
</a>
```

### Handle extraction

```liquid
assign _sub_raw = block.settings.link | remove: '/collections/'
assign _sub_handle = _sub_raw | remove: '/'
assign _sub_col = collections[_sub_handle]
```

Handles both `/collections/<handle>` and `/collections/<handle>/` (trailing slash stripped).

### CSS for count badge

```css
.ds-cc__filter-pill-count{
  font-family:"JetBrains Mono",ui-monospace,monospace;
  font-size:11px;letter-spacing:0.04em;
  color:rgba(var(--textColor-rgb),0.55);
  margin-left:var(--space-1);
}
```

---

## Phase 4 — Schema Addition

Added to schema settings array under Hero group, between `hero_image` and `cta_label`:

```json
{
  "type": "text",
  "id": "lead_time",
  "label": "Lead time",
  "default": "2–6 weeks",
  "info": "Shown in hero stats line. Override per-hub if needed."
}
```

Schema JSON validated clean (python3 json.loads — no errors).

---

## Phase 5 — Push Results

| File | Theme | HTTP |
|---|---|---|
| `sections/ds-cc-base.liquid` | dev `186373570873` | **200 OK** |

Pull-back verification (all confirmed present in returned content):

| Check | Result |
|---|---|
| `ds-cc__hero-stats` CSS | PASS |
| `ds-cc__hero-stats` Liquid `<dl>` | PASS |
| `ds-cc__filter-pill-count` CSS | PASS |
| `ds-cc__filter-pill-count` Liquid `<span>` | PASS |
| `lead_time` schema setting | PASS |
| "All" pill at head of filter row | PASS |
| `sub_handle` extraction via `remove: '/collections/'` | PASS |
| `render 'bbi-nav'` | PASS |
| `render 'bbi-crumbs'` | PASS |
| `render 'bbi-oecm-bar'` | PASS |
| `render 'bbi-footer'` | PASS |
| `{% schema %}` present | PASS |
| `{% endschema %}` present | PASS |
| Closing `.ds-cc` wrapper div | PASS |
| Live theme `186495992121` not referenced | PASS |

---

## Shared Snippets — Untouched

The following shared snippets were **not modified**:

- `bbi-nav.liquid`
- `bbi-footer.liquid`
- `bbi-crumbs.liquid`
- `bbi-oecm-bar.liquid`

---

## Edge Cases Handled

| Scenario | Handling |
|---|---|
| Empty collection (0 products, grid_mode: tiles) | All stat derivations produce `0` gracefully; `collection.products_count` is 0, loops return 0 |
| `lead_time` schema blank | `\| default: '2–6 weeks'` fallback always renders a value |
| Sub-collection link with trailing slash `/collections/foo/` | `\| remove: '/'` after removing `/collections/` strips the trailing slash |
| Sub-collection handle not found in `collections[]` | `if _sub_col != nil` guard — pill renders without count rather than crashing or showing `0` |
| Non-tile blocks mixed in `section.blocks` | `if block.type == 'tile'` guard unchanged — no regression on `brand_callout` or `brand_plate` blocks |
| `available` filter on large collection (>250 products) | Shopify paginates `collection.products` at 250 in Liquid; stat reflects first 250. Known limitation — acceptable for display stats, not inventory counts |

---

## Stage 3.1c.2 Backlog

**Filter pill bar — Brand / Height / Fabric tier / Warranty** (`Brand 18▾ · Height 4▾ · Fabric tier 5▾ · Warranty 3▾`)

**Gate:** tag census shows 0% coverage for all five namespaces (`brand:`, `height:`, `fabric-tier:`, `warranty:`, `subcategory:`). No products currently carry these tags.

**Unblocked by:** the upcoming tagging pass (Stage 3.1c.2), which must:
1. Define canonical tag namespaces per spec
2. Backfill existing products with correct `brand:*`, `height:*`, `fabric-tier:*`, `warranty:*` tags
3. Set up smart collection rules that filter by these tags (or implement JS-based client-side filter on the existing product grid)

Until the tagging pass runs, a filter rail would render all dropdowns with 0 items. The filter rail markup can be added as a progressive enhancement in 3.1c.2; it won't break the page if absent.
