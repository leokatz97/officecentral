# Stage 3.2b — Sub-Collection T4 Design Parity

**Date:** 2026-05-07  
**Branch:** `feature/stage-3.2b-subcollection-t4`  
**Dev theme:** `186373570873`  
**Live theme:** `186495992121` — confirmed untouched throughout  
**File modified:** `theme/sections/ds-cs-base.liquid` (1 file, 4 targeted edits)

---

## Phase 1 — Verification Migration

**Chosen collection:** `highback-seating`  
**Collection ID:** `473194529081`  
**Title:** High Back Seating  
**Product count:** 46  
**Prior template_suffix:** `''` (empty — legacy Starlite default template `collection.json`)  
**Post-migration template_suffix:** `base`  
**Method:** Admin API PUT `/custom_collections/473194529081.json` with `{"template_suffix": "base"}`  
**HTTP status:** 200 OK  

**Why this collection:**
- Highest product count (46) among legacy seating sub-collections with no template=base
- Seating hub — defaults to the correct parent (`seating` / `Seating`) without any schema config, so verifiable immediately
- Representative: typical mix of buyable-priced and $0/unavailable products
- The "highback" naming is clear and well-separated from the 31 empty new shells

**Note for Stage 3.2a.5:** `highback-seating` (ID 473194529081) is already migrated to `template_suffix=base`. It is the one legacy collection already on the new template. Stage 3.2a.5 should treat this as a known state when surveying the population migration path.

---

## Phase 2 — Edit 1: Image Ratio Fix

**Root cause (from recon):** `aspect-ratio:4/3` (landscape) container + `object-fit:cover` on 1:1 square catalog images clips ~25% top and bottom. Chair headrests and caster bases are cut off.

**Decision applied:** 1:1 square (user-confirmed). Actual catalog images are uniformly 1:1 square — 4:5 portrait spec would clip sides on existing stock.

### CSS change

```css
/* BEFORE */
.ds-cs__card-img{
  aspect-ratio:4/3;overflow:hidden;background:var(--alternateBackground);
  border-bottom:1px solid rgba(var(--borderColor-rgb),0.5);
}

/* AFTER */
.ds-cs__card-img{
  aspect-ratio:1/1;overflow:hidden;background:var(--alternateBackground);
  border-bottom:1px solid rgba(var(--borderColor-rgb),0.5);
}
```

### Liquid change

```liquid
{{- comment -}} BEFORE
{{ product.featured_media | image_url: width: 480 | image_tag: loading: 'lazy', alt: card_img_alt }}

{{- comment -}} AFTER — CDN serves pre-cropped 480×480; no browser-side crop work
{{ product.featured_media | image_url: width: 480, height: 480, crop: 'center' | image_tag: loading: 'lazy', alt: card_img_alt }}
```

**Integrity check after edit:** PASS (8/8)

---

## Phase 3 — Edit 2: CTA Routing Fix

**Bug (from recon):** When `is_quote_only = true` (price == 0 OR available == false), the tile footer linked to `/pages/quote?product={{ product.handle }}&source=collection&lead_type=quote`, bypassing the PDP entirely.

**BBI Rule #2:** Unbuyable items stay live as B2B lead-capture pages. The tile links to the PDP; the PDP decides between add-to-cart and Quote CTA.

### Liquid change

```liquid
{{- comment -}} BEFORE — routes to /pages/quote, bypassing PDP
<a href="/pages/quote?product={{ product.handle }}&source=collection&lead_type=quote"
   class="ds-cs__card-quote-cta"
   itemprop="url">
  Request a Quote →
</a>

{{- comment -}} AFTER — routes to PDP; comment explains the rule
{%- comment -%}
  BBI rule #2: link to PDP — the PDP decides between add-to-cart
  and quote CTA based on product state. Never bypass the PDP.
{%- endcomment -%}
<a href="{{ product_url }}"
   class="ds-cs__card-quote-cta"
   itemprop="url">
  Request a Quote →
</a>
```

**Scale:** `product_url` was already assigned at the top of the card loop (`assign product_url = product.url`) and used for the image and title links — only the footer CTA was wrong. Given ~100% of catalog products are $0/unavailable, this fix affects virtually every tile across all 32 template=base collections once populated.

**Integrity check after edit:** PASS (6/6)

---

## Phase 4 — Edit 3: Hero CTA

**Gap from recon (GAP-T4-1):** Hero had no CTA button. Brief specifies "Shop all [parent-category]" secondary CTA routing to the parent Level-2 hub. `parent_title` and `parent_handle` schema variables were already assigned at the top of the section.

### CSS addition (one rule)

```css
.ds-cs__hero-cta{margin-top:var(--space-4);}
```

### Liquid addition (4 lines inside hero left column)

```liquid
{{- comment -}} BEFORE — subtitle paragraph, then immediately closing </div>
{%- if section.settings.hero_subtitle != blank -%}
  <p class="ds-cs__hero-meta">{{ section.settings.hero_subtitle }}</p>
{%- else -%}
  <p class="ds-cs__hero-meta">{{ collection.products_count }} ... available</p>
{%- endif -%}
</div>

{{- comment -}} AFTER — subtitle paragraph, then hero CTA
{%- if section.settings.hero_subtitle != blank -%}
  <p class="ds-cs__hero-meta">{{ section.settings.hero_subtitle }}</p>
{%- else -%}
  <p class="ds-cs__hero-meta">{{ collection.products_count }} ... available</p>
{%- endif -%}
<div class="ds-cs__hero-cta">
  <a href="/collections/{{ parent_handle }}" class="bbi-btn bbi-btn--secondary">
    Shop all {{ parent_title }}
  </a>
</div>
</div>
```

**Renders as:** "Shop all Seating" linking to `/collections/seating` for any seating sub-collection. Defaults to `seating` until per-collection schema settings are configured (see Phase 6).

**Integrity check after edit:** PASS (12/12)

---

## Phase 5 — Edit 4: OECM Trust Line in Phone CTA Band

**Gap from recon (GAP-T4-6):** Phone CTA band missing the OECM trust line present in T3's CTA section.

### CSS addition (two rules)

```css
.ds-cs__phone-cta-trust{
  display:flex;align-items:center;gap:var(--space-2);
  font-size:14px;color:rgba(255,255,255,0.75);margin:0;
}
.ds-cs__phone-cta-trust__dot{
  width:6px;height:6px;border-radius:50%;
  background:#D4252A;flex-shrink:0;
}
```

### HTML addition (inside `.ds-cs__inner`, after actions div)

```html
<p class="ds-cs__phone-cta-trust">
  <span class="ds-cs__phone-cta-trust__dot" aria-hidden="true"></span>
  <strong>OECM vendor of record</strong> &middot; Ontario institutional buyers can purchase without open tender
</p>
```

**Design alignment:** Red dot + white/75% text matches the OECM trust line pattern from `bbi-cta-section` used in T3 hubs and all landing pages. Text reads same as the component spec's trust line.

**Full 4-edit integrity check:** PASS (16/16)

---

## Phase 6 — Parent Metadata Config Script

**Script:** `scripts/set-base-collection-schemas.py`  
**Output CSV:** `data/reports/stage-3.2b-schema-mapping.csv`

### Key discovery

Per-collection section settings (`parent_category_handle` / `parent_category_title`) **cannot be pushed via the Shopify Admin API at BBI's plan level.** The Assets API manages the shared `collection.base.json` template file — it cannot carry per-collection overrides. This is a Shopify OS 2.0 architecture constraint, not a script bug.

### Dry-run output summary

| Result | Count | Action |
|---|---|---|
| OK — seating (default correct) | 8 | No Theme Editor action needed |
| OK — non-seating | 20 | Manual Theme Editor config required |
| AMBIGUOUS (brand sub-collections) | 4 | Flagged; mappings assigned, verify with Steve |
| SKIPPED | 0 | All 32 mapped |

**4 ambiguous brand sub-collections:**

| Handle | Assigned parent | Reason for ambiguity |
|---|---|---|
| `keilhauer` | seating | Keilhauer callout appears on Seating hub in ds-cc-base; also used in Boardroom |
| `ergocentric` | ergonomic-products | ergoCentric callout is under Ergonomic Products hub in ds-cc-base |
| `global-furniture` | desks | Global Furniture Group primary product in BBI catalog is desks |
| `global-teknion` | desks | ds-cc-base places Global/Teknion under both Desks and Panels — Desks used as primary |

**8 seating sub-collections defaulting correctly (no action):**
`active-seating`, `beam-seating`, `bench-seating`, `conference-seating`, `executive-seating`, `healthcare-seating`, `highback-seating`, `keilhauer`

**Manual Theme Editor action needed for 24 non-seating sub-collections** — see `data/reports/stage-3.2b-schema-mapping.csv` for full per-collection values.

### Implication for verification

`highback-seating` defaults to `parent=seating / Seating` which is correct. No Theme Editor action needed to verify the section — breadcrumb Level 3 and hero eyebrow will read "Seating" correctly.

---

## Phase 7 — Push Results

| File | Theme | HTTP | Size | Timestamp |
|---|---|---|---|---|
| `sections/ds-cs-base.liquid` | `186373570873` (dev) | **200 OK** | 33,946 bytes | 2026-05-07T16:46:50-04:00 |

**Pull-back spot-check:** 14/14 checks passed  
**Live theme `186495992121` check:** asset present but does NOT contain any of the 4 edits — confirmed untouched  
**Shared snippets:** bbi-nav, bbi-crumbs, bbi-footer — all present in pulled-back content, unmodified

---

## Verification Target: highback-seating

**Dev theme URL:** `https://brantbusinessinteriors.com/collections/highback-seating?preview_theme_id=186373570873`

**Expected visual changes vs. pre-stage state (Starlite default template):**
- Template: now renders `ds-cs-base.liquid` instead of Starlite `main-collection`
- Hero: BBI-styled strip with breadcrumb (Home → Shop Furniture → Seating → High Back Seating), red dot eyebrow, H1, product count, "Shop all Seating" secondary CTA
- Product grid: 2/3/4-col responsive; square (1:1) product images with no vertical cropping; chair photos showing full headrest-to-caster frame
- All 46 products: "Request a Quote →" in card footer links to each product's PDP (`/products/handle`), not to `/pages/quote`
- Bottom: charcoal CTA band with "OECM vendor of record" trust line
- Footer: `bbi-footer` (charcoal, Canadian-owned, 4-column nav)

---

## Commits

| Hash | Message |
|---|---|
| `708aa3d` | `feat: refactor ds-cs-base for T4 design parity (Stage 3.2b)` |
| `9bbfde1` | `feat: add set-base-collection-schemas.py for parent metadata config (Stage 3.2b)` |

---

## Stage 3.2a.5 Inputs

Stage 3.2a.5 is the investigation into the product population strategy. Key inputs from 3.2b:

1. **`highback-seating` is already migrated.** It now uses `template_suffix=base` and has 46 products. It is the only legacy collection on the new template. Any population strategy must account for this pre-existing migration.

2. **The 31 new empty shells** (all other `template_suffix=base` collections) need products. The two strategies (migrate legacy → base, or populate new shells from scratch) remain open.

3. **`mesh-seating` is the next best candidate** if Stage 3.2a.5 wants a second validation point before committing to a bulk strategy: 44 products, seating hub, same `template_suffix=''` legacy state as `highback-seating` was before Phase 1.

4. **Template coverage audit as of 2026-05-07:**
   - `template_suffix=base`: 32 collections (31 empty shells + `highback-seating`)
   - `template_suffix=''` (legacy Starlite): 68+ collections including all other product-bearing sub-collections

---

## Stage 3.2c Inputs

Stage 3.2c is the bulk population/migration execution. Sub-collections that still need `template_suffix=base` applied (the 67 legacy product-bearing collections not yet migrated):

**Representative populated legacy sub-collections to prioritize for migration:**

| Handle | Hub | Approx. products | Notes |
|---|---|---|---|
| `mesh-seating` | seating | 44 | Second-largest seating sub |
| `l-shape-desks-desks` | desks | 31 | Largest desks sub |
| `lateral-files-storage` | storage | 7+ | Storage representative |
| `meeting-tables` | tables | 12 | Tables representative |
| `boardroom-conference-meeting` | boardroom | 12+ | Boardroom representative |
| `height-adjustable-tables` | ergonomic-products | 5+ | Ergo representative |

**Full list:** All 68 handles from `data/reports/sub-collection-audit-20260506_231332.csv` minus `highback-seating`.

**Schema config prerequisite:** Before promoting any non-seating collection to `template_suffix=base`, the `parent_category_handle` and `parent_category_title` settings must be set via Theme Editor (or via a plan-level API if available). See `data/reports/stage-3.2b-schema-mapping.csv` for the full per-collection mapping.

---

## Halt

Branch `feature/stage-3.2b-subcollection-t4` is ready for review. Not merged. Dev theme push complete. No live theme changes.
