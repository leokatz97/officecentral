# Stage 3.2a — Current `ds-cs-base.liquid` Audit

**Generated:** 2026-05-07  
**File audited:** `theme/sections/ds-cs-base.liquid` (704 lines)  
**Template:** `theme/templates/collection.base.json`  
**Template suffix:** `base`

---

## 1. Schema Settings

| ID | Type | Label | Default | Notes |
|---|---|---|---|---|
| `logo` | image_picker | Logo | — | Falls back to bbi-nav snippet default |
| `hero_title` | text | Page title | — | Falls back to `collection.title` |
| `hero_subtitle` | text | Subtitle | — | Falls back to product count string |
| `hero_image` | image_picker | Hero image | — | Optional 180px accent image right of title |
| `parent_category_handle` | text | Parent category handle | `"seating"` | Used in breadcrumb + "no products" fallback link |
| `parent_category_title` | text | Parent category title | `"Seating"` | Used in breadcrumb + hero eyebrow label |
| `show_phone_cta` | checkbox | Show phone CTA band | `true` | Toggles the entire bottom CTA band |
| `phone_cta_heading` | text | CTA Heading | "Need help choosing the right furniture?" | |
| `phone_cta_body` | textarea | CTA Body | "Our furniture consultants work..." | |

**Blocks defined:** only `@app` (no merchant-editable content blocks beyond settings)  
**Presets:** one preset — "Sub-Collection Page"

**Schema gaps:**
- No hero CTA text or link setting (can't set "Shop all Seating" without code change)
- No brand strip content (no brand block type)
- No OECM bar toggle

---

## 2. Shared Snippet Inclusions

| Snippet | Location in file | Arguments passed | Status |
|---|---|---|---|
| `bbi-nav` | Line 276 | `logo: section.settings.logo, active: 'shop'` | ✅ Present, correct |
| `bbi-crumbs` | Line 281 | c2="Shop Furniture", c2_href="/collections/business-furniture", c3=parent_title, c3_href=/collections/{parent_handle}, c4=page_title | ✅ Present, 4-level breadcrumb |
| `bbi-footer` | Line 549 | `logo: section.settings.logo` | ✅ Present |

**Missing snippets:**
- `bbi-oecm-bar` — not rendered (snippet doesn't exist yet; deferred)

---

## 3. Hero Strip (lines 283–306)

```liquid
<section class="ds-cs__hero">
  <div class="ds-cs__hero-inner">
    <div>
      <div class="ds-cs__hero-label">
        <span class="ds-cs__hero-label__dot" />   <!-- red dot -->
        <span class="bbi-mono">{{ parent_title }}</span>
      </div>
      <h1>{{ page_title }}</h1>
      <p class="ds-cs__hero-meta">
        <!-- if hero_subtitle set: custom copy -->
        <!-- else: "N product(s) available" -->
      </p>
    </div>
    <!-- optional hero image: 180px accent, image_url width:360 -->
  </div>
</section>
```

**Issues:**
- ❌ No hero CTA button. The brief specifies "Shop all [parent-category]" CTA routing to parent L2 collection. Missing entirely — not a schema oversight, just absent from the design.
- ❌ No hero stats line (brand count / warranty). T3 has one (added Stage 3.1c.1). T4 spec is silent.
- ✅ Breadcrumb correctly placed (rendered just above hero via snippet)
- ✅ Parent category correctly shown as mono eyebrow label

---

## 4. Filter Sidebar (lines 313–407)

Built-in, always rendered. Two tag-group filters + price range.

**Tag extraction logic:**
```liquid
for tag in collection.all_tags
  if tag contains 'type:'   → type_tags array
  elsif tag contains 'room:' → room_tags array
endif
```

**Filter groups rendered:**
- "Product Type" (`type:` tags) — only shown if `type_tags` non-empty
- "Room / Setting" (`room:` tags) — only shown if `room_tags` non-empty
- "Price" (min/max inputs, collapsed by default)
- "Clear all filters" — appears when `current_tags.size > 0`

**Interaction behavior:** checkbox → URL tag filter (`/collections/handle/tag+tag`). JavaScript navigates on change (no AJAX).

**Issues:**
- ✅ Functional filter rail for collections with type: and room: tags
- ⚠️ No `subcategory:`, `brand:`, `height:`, `fabric:`, `warranty:` filters (all at 0% tag coverage — deferred)
- The sidebar renders even for empty collections (not gated on product count)

---

## 5. Product Grid — Image Rendering (lines 446–456)

```liquid
{%- if product.featured_media -%}
  {%- assign card_img_alt = product.featured_media.alt | default: product.title | escape -%}
  {{ product.featured_media | image_url: width: 480 | image_tag: loading: 'lazy', alt: card_img_alt }}
{%- else -%}
  <!-- SVG placeholder icon -->
{%- endif -%}
```

**CSS container (lines 196–204):**
```css
.ds-cs__card-img {
  aspect-ratio: 4/3;        /* landscape container */
  overflow: hidden;
  background: var(--alternateBackground);
}
.ds-cs__card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;        /* crops to fill */
}
```

**Image URL parameters:** `image_url: width: 480` only — no explicit height or crop parameter. Shopify CDN returns an image 480px wide at its native aspect ratio.

**Actual catalog image dimensions (sampled from highback-seating):**
- ObusForme Comfort chair: 500×500 (1:1 square)
- Format high mesh chair: 710×710 (1:1 square)
- Chevron ultra high back: 485×485 (1:1 square)

All three are 1:1 square. No height parameter means the CDN serves a 480×480 image. The CSS container at `4/3` (landscape) clipping a 1:1 image via `object-fit: cover` crops approximately **25% from top and bottom** — cuts chair headrests and foot rings.

---

## 6. Tile Button CTA Routing (lines 437–479)

**Unbuyable detection (lines 437–441):**
```liquid
assign is_quote_only = false
if product.price == 0 or product.available == false
  assign is_quote_only = true
endif
```

**CTA rendering (lines 465–479):**
```liquid
{%- if is_quote_only -%}
  <!-- ROUTES TO /pages/quote — BUG per BBI rule #2 -->
  <a href="/pages/quote?product={{ product.handle }}&source=collection&lead_type=quote"
     class="ds-cs__card-quote-cta">
    Request a Quote →
  </a>
{%- else -%}
  <!-- Shows price; title link routes to PDP — correct -->
  <p class="ds-cs__card-price">
    {{ product.price_min | money }}
    {%- if product.price_min != product.price_max %} – {{ product.price_max | money }}{%- endif -%}
  </p>
{%- endif -%}
```

**Bug:** When `is_quote_only = true`, the "Request a Quote" CTA goes to `/pages/quote`, bypassing the PDP entirely.  
**BBI Rule #2:** "Sold-out, $0-price, and showcase products keep their page with a Request a Quote CTA — these are B2B lead-capture pages, not dead listings."  
**Implication:** The PDP IS the lead-capture page. The tile should link to the PDP, which then shows the PDP-level quote CTA (`.bbi-cta-pdp`).

Note: The card image link (line 446, aria-hidden) and title link (line 462) BOTH already route to `product_url` (PDP). Only the quote CTA footer link goes to `/pages/quote`.

---

## 7. Phone CTA Band (lines 531–547)

```liquid
{%- if section.settings.show_phone_cta -%}
<section class="ds-cs__phone-cta">
  <h2>{{ section.settings.phone_cta_heading }}</h2>
  <p>{{ section.settings.phone_cta_body }}</p>
  <a href="tel:+15198371810" class="bbi-btn--inverted">Call a Consultant</a>
  <a href="/pages/quote?source=collection-cta&lead_type=design-consultation" class="bbi-btn--outline-white">
    Free Design Consultation
  </a>
</section>
{%- endif -%}
```

**Issues:**
- ✅ Correct charcoal inverse treatment
- ⚠️ Hard-coded phone number `+15198371810`. Should be a schema setting or from a global variable.
- ⚠️ "Free Design Consultation" link goes to `/pages/quote` with source params — fine for the CTA band (this is intentional, not a BBI rule #2 issue)
- ❌ No OECM trust line

---

## 8. JavaScript (lines 553–611)

- Mobile sidebar toggle (click to expand `ds-cs-filter-body`)
- Desktop filter group collapse/expand
- Tag filter checkboxes → URL navigation
- Price min/max apply button → URL searchParam update
- Clear filters button → strip to bare pathname

No AJAX. All filter actions are full-page navigations. Acceptable for V1.

---

## 9. Template file: collection.base.json

```json
{
  "sections": { "ds-cs-base": { "type": "ds-cs-base", "settings": {} } },
  "order": ["ds-cs-base"]
}
```

Single-section template, no pre-populated settings. Settings must be configured per-collection in the Theme Editor (or via API). This means the `parent_category_handle` and `parent_category_title` defaults ("seating" / "Seating") apply to ALL 31 template=base collections unless explicitly overridden.

**Issue:** If no one updates the schema settings for each sub-collection, all will show "Seating" in the breadcrumb regardless of their actual parent hub.

---

## 10. Template Coverage Reality

| Group | Count | Template | Products | Notes |
|---|---|---|---|---|
| New T4 sub-collections | 31 | `base` | **0 each** | Created in Stage 3.x; empty |
| Old product-bearing sub-collections | 68 (audit CSV) | `(none)` = default | Various | Use legacy Starlite `collection.json` |
| Parent hubs | 9 | `category` | 9–194 | T3 design — Stage 3.1 work |

The 31 `template=base` collections are the intended T4 pages but have no products yet. The 68 legacy collections have the products but use the old Starlite template (which has the "Get a free seating recommendation" CTA the brief mentioned — that's a Starlite theme element, not from ds-cs-base.liquid).
