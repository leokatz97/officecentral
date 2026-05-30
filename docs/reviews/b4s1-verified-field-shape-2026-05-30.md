# VERIFIED FIELD-SHAPE REFERENCE — PHASE-A-BLOCK-4-SESSION-1

**Locked:** 2026-05-30 — ACCEPTED by Leo. Field set = 13 (tagline/standfirst left blank). body_html = full body (theme auto-splits).
**Gold-standard product:** [vion-mesh-high-back-chair-1](https://www.brantbusinessinteriors.com/products/vion-mesh-high-back-chair-1) — Global Furniture Group, Seating collection
**Verification basis:** Admin API product pull + live storefront PDP render (`www.brantbusinessinteriors.com`, HTTP 200, 460 KB) + `theme/sections/ds-pdp-base.liquid` source.

---

## Field table (verified against LIVE render)

| Metafield | Shopify type | Renders on PDP? | Where | Data shape (verbatim from gold-standard) |
|---|---|---|---|---|
| `specs.standfirst` | *(no definition)* | **Only if populated** — BLANK on gold-standard | `<p class="pdp-standfirst">` directly under price, above fold | Not used. Theme outputs raw (no `escape`). |
| `specs.tagline` | *(no definition)* | **Only if populated** — BLANK on gold-standard | `<h2 class="pdp-about__tagline">` in About section | Not used. Theme applies `escape` → plain one-liner. |
| `specs.who_its_for` | `single_line_text_field` | **YES** | "Who it's for" block, About section | `Design-focused professional services firms, hospital administrative suites, and municipali…` — 1–2 sentences. Theme outputs raw (no escape). |
| `specs.key_features` | `list.single_line_text_field` | **YES** | Spec table, top row, as `<ul><li>` | JSON array of strings: `["Two back heights (medium and high)","Two seat widths",…]` |
| `specs.manufacturer` | `single_line_text_field` | **YES** | Spec table "Manufacturer" | `Global Furniture Group` |
| `specs.product_line` | `single_line_text_field` | **YES** | Spec table "Product Line" | `Vion` |
| `specs.model_codes` | `list.single_line_text_field` | **YES** | Spec table "Model" (`join: ', '`) | `["6321-0","6321-3","6321-8","6331-0","6331-0-C"]` |
| `specs.dimensions` | `single_line_text_field` | **YES** | Spec table "Dimensions" | `25.5"W x 24"D x 41.5"H (model 6321-0 high back)` |
| `specs.weight` | `single_line_text_field` | **YES** | Spec table "Weight" | `50 lbs` |
| `specs.weight_capacity` | `single_line_text_field` | **YES** | Spec table "Weight Capacity" | `300 lbs` |
| `specs.materials` | `multi_line_text_field` | **YES** | Spec table "Materials" (`newline_to_br`) | Long-form string; newlines → `<br>`. |
| `specs.finishes_available` | `list.single_line_text_field` | **YES** | Spec table "Finishes Available" `<ul><li>` | `["10 Vion Mesh colours","7 Dimension Mesh colours","Frame: Black",…]` |
| `specs.certifications` | `list.single_line_text_field` | **YES** | Spec table "Certifications" `<ul><li>` | `["Exceeds ANSI/BIFMA"]` |
| `specs.warranty` | `single_line_text_field` | **YES** | Spec table "Warranty" | `Limited Lifetime Warranty` |
| `specs.country_of_manufacture` | `single_line_text_field` | **YES** | Spec table **"Made In"** (label differs from key) | `Canada (Global)` |

### body_html (the split convention — CONFIRMED)
- Theme: `product.description | split: '<h3>' | first` → only content **before the first `<h3>`** renders in the "About this product" block.
- Gold-standard body_html is the **FULL rich description**, not a lead-only stub:
  1. `<p><strong>bold hook</strong></p>` (one-line hook — matches voice rules)
  2. `<p>lede paragraph</p>` (2–4 sentences)
  3. `<h3>Key features</h3><ul>…</ul>` *(split off — does NOT render on PDP; mirrors `specs.key_features`)*
  4. `<h3>Who it's for</h3><p>…</p>` *(split off; mirrors `specs.who_its_for`)*
  5. `<p>closing CTA w/ phone 1-800-835-9565</p>` *(split off)*
- The `<h3>` sections are retained in body_html for SEO/crawlers and any full-description surface, even though the PDP only shows the intro.

### SEO
- Native `product.seo.title` / `product.seo.description` === `global.title_tag` / `global.description_tag` (same underlying store). Setting `product.seo` via API is sufficient — renders to `<title>` and `<meta name="description">`. Product JSON-LD confirmed present on PDP.

### Tag taxonomy (routing recipe, from gold-standard)
`bestseller` · `brand:global-furniture-group` · `feature:ergonomic` · `oecm-eligible` · `type:chairs`
- `brand:<slug>` and `type:<slug>` drive smart-collection routing. `feature:<slug>` = filter facet. `oecm-eligible` = OECM flag. `bestseller` = merchandising.

---

## Corrections to the "15-field framework" (from Day 13 notes)

- **Framework is 15 fields; live practice is 13.** `specs.tagline` and `specs.standfirst` are wired in the theme but **BLANK on the gold-standard** and therefore never render. They are optional/aspirational, not part of the working enrichment set.
- **No metafield definitions exist for `tagline` / `standfirst` / `who_its_for`.** Only 12 definitions are registered in Shopify (the spec-table fields). `who_its_for` is populated anyway as an *unstructured* `single_line_text_field`. To write `tagline`/`standfirst` we'd write them unstructured too (no definition needed for the theme to read `.value`).
- **`country_of_manufacture` renders under the label "Made In"** (key name ≠ display label) — note for QA.
- **`who_its_for` is stored as `single_line_text_field`** despite holding 1–2 sentences. Keep it to ~1–2 sentences, no markdown.
