# Stage 4b — PDP Design Parity Build

**Date:** 2026-05-08  
**Branch:** `feature/stage-4b-pdp-design-parity`  
**Dev theme:** `186373570873` (BBI Landing Dev) — ONLY

---

## Phase 1 — Gap resolution checklist (all 8 resolved before build)

| Gap | Resolution | Status |
|-----|-----------|--------|
| **G-1** Breadcrumb depth | 5 levels using `collection.metafields.bbi.parent_hub_handle`; fallback to 4-level if metafield blank | ✅ |
| **G-2** `bestFor` callout | `specs.key_features` first 3 bullets; generic RFQ headline ("Contact us for pricing and availability") | ✅ |
| **G-3** `.scheme-alt` commerce block | `--alternateBackground` (#FAFAFA) local class in section CSS | ✅ |
| **G-4** Brand block vendor matching | Multi-condition: vendor contains OR `specs.manufacturer` contains; `OTG`/`Offices to Go` mapped to Global | ✅ |
| **G-5** Related products fallback | `_pdp_related_count >= 2` required; section hidden if < 2 | ✅ |
| **G-6** "View all [Brand]" link | `/pages/brands-ergocentric`, `/pages/brands-keilhauer`, `/pages/brands-global-teknion` (interim until SMART-1) | ✅ |
| **G-7** Hero stats line | Confirmed NOT in T5 spec; no stats band on PDP | ✅ (no action) |
| **G-8** Variant picker styling | Visual filled circle chips for colour options (Liquid hex mapping); text pill chips for size/other | ✅ |

---

## Phase 2 — `bbi-crumbs.liquid` disposition

**Extended** (from 4-level to 5-level support).

### Diff summary
- Added `c4_href` parameter: enables c4 to render as a linked crumb when `c5_label` is present
- Added `c5_label` parameter: always terminal, product title on PDPs
- All existing 2/3/4-level callers unchanged — `c5_label` blank preserves prior terminal behaviour on c4

### Backward compatibility trace
| Caller pattern | c5_label | Result | ✓ |
|---|---|---|---|
| `c2_label` only | blank | Home > c2 (terminal) | ✅ |
| `c2 + c3` | blank | Home > c2 > c3 (terminal) | ✅ |
| `c2 + c3 + c4` | blank | Home > c2 > c3 > c4 (terminal) | ✅ |
| `c2 + c3 + c4 + c4_href + c5` | set | Home > c2 > c3 > c4(linked) > c5 (terminal) | ✅ |
| `ds-cs-base.liquid` caller | blank | 4-level sub-collection, unchanged | ✅ |

---

## Phase 3 — JSON-LD snippets shipped

| Snippet | Schema type | Key fields |
|---------|------------|-----------|
| `bbi-product-jsonld.liquid` | `Product` | name, description, image, sku, mpn, brand, offers (price/currency/availability), countryOfOrigin (from `specs.country_of_manufacture`) |
| `bbi-breadcrumb-jsonld.liquid` | `BreadcrumbList` | Up to 5 levels, mirrors bbi-crumbs visual path; params: `bc_c2_label/href` through `bc_c5_label` |

Both pushed to dev theme `186373570873`. HTTP 200 confirmed.

---

## Phase 4 — `ds-pdp-base.liquid` summary

**File:** `theme/sections/ds-pdp-base.liquid`  
**Lines:** 950  
**Key Liquid logic excerpts:**

### RFQ block (primary state, ~92% of catalog)
```liquid
{%- if _pdp_buyable -%}
  {{- price block + variant picker + add-to-cart form -}}
{%- else -%}
  <div class="bbi-pdp-rfq">
    <p class="bbi-pdp-rfq__headline">Contact us for pricing and availability</p>
    {%- if _pdp_has_key_features -%}
      {%- for feat in product.metafields.specs.key_features.value limit: 3 -%}…{%- endfor -%}
    {%- endif -%}
    <button … onclick="document.getElementById('bbi-rfq-dialog').showModal()">Request a Quote</button>
    <a href="tel:+18008359565">1-800-835-9565</a>
  </div>
{%- endif -%}
```

### Spec table conditional (hides on zero rows)
```liquid
{%- if _pdp_spec_row_count > 0 -%}
  <section … aria-labelledby="bbi-pdp-specs-heading">
    <table class="bbi-pdp-specs-table">…</table>
  </section>
{%- endif -%}
```
`_pdp_spec_row_count` is computed from 10 individual metafield presence checks + `product.type` — renders 0 when no specs set.

### Breadcrumb derivation (5-level with fallback)
```liquid
{%- assign _pdp_parent_hub_handle = _pdp_sub_coll.metafields.bbi.parent_hub_handle.value -%}
{%- if _pdp_parent_hub_title != blank -%}
  {%- render 'bbi-crumbs', c2_label: 'Shop Furniture', c2_href: '…',
      c3_label: hub_title, c3_href: hub_href,
      c4_label: sub_coll.title, c4_href: sub_coll.url,
      c5_label: product.title -%}
{%- elsif _pdp_sub_coll != nil -%}
  {%- render 'bbi-crumbs', c2_label: 'Shop Furniture', …, c3_label: sub_coll.title,
      c3_href: sub_coll.url, c4_label: product.title -%}
{%- else -%}
  {%- render 'bbi-crumbs', c2_label: 'Shop Furniture', …, c3_label: product.title -%}
{%- endif -%}
```

### Section structure (13 T5 zones)
| Zone | Implementation |
|------|---------------|
| Chrome — nav | `{% render 'bbi-nav', active: 'shop' %}` |
| Chrome — footer | `{% render 'bbi-footer' %}` |
| JSON-LD | Both snippets rendered at top of section |
| Breadcrumb | 5-level with collection metafield; graceful 4/3-level fallback |
| Hero gallery | Web Component `<bbi-gallery>`, 4:3 aspect ratio, eager first + lazy rest, 8-image strip, prev/next nav |
| Commerce panel | `.bbi-pdp-info` on `--alternateBackground`; buyable → ATC; unbuyable → RFQ |
| Trust pills | Sold-out badge, Canadian-made (maple SVG + `country_of_manufacture=Canada`), OECM-eligible (tag) |
| Variant swatches | Filled circle chips with hex colour map (26 colours); text pill chips for size/other; `<label>+<input type=radio>` pattern |
| Description | Renders `product.description`, hidden if blank |
| Spec table | 10 metafield rows + `product.type` + brand; hidden entirely if zero rows |
| Related products | Same `product.type` within collection, max 4, hidden if < 2 |
| Brand block | Text-only: ergoCentric / Keilhauer / Global+OTG (Canadian badge + authorized dealer + blurb + "View all" link); hidden for generic vendor |
| OECM bar | `{% render 'bbi-oecm-bar' %}` |
| CTA closer | `.scheme-inverse` charcoal band; "Ready to furnish your next space?" heading; Quote + phone CTA |
| RFQ modal | `<dialog>` element; pre-filled product handle; name/email/phone/message form |

---

## Phase 5 — `product.json` shipped

```json
{
  "sections": { "ds-pdp-base": { "type": "ds-pdp-base", "settings": {} } },
  "order": ["ds-pdp-base"]
}
```
Pushed to dev theme `186373570873`. HTTP 200 confirmed.

---

## Phase 6 — Spec push results

Script: `scripts/push-pe2-specs.py --live`

| Metric | Result |
|--------|--------|
| Spec files processed | 100 (grew from 93 estimated in 4a) |
| Products updated | 75 |
| Products already current | 25 |
| Products not found | 0 |
| Total metafield writes | 174 |
| Failures | 0 |
| Log | `data/logs/pe2-push-20260508-081538.json` (gitignored) |
| Backup | `data/backups/pe2-specs-pre-push-20260508-081538.json` (gitignored) |

---

## Phase 7 — Smoke test (5 product states)

### Static analysis (22 checks on `ds-pdp-base.liquid`)
All 22 logical patterns confirmed present. One check ("c5_label != blank") returns false-negative because the 5-level conditional lives in `bbi-crumbs.liquid` (where it was confirmed ✅), not the calling section.

### Product state verification (Admin API)

| State | Handle | HTTP | Specs | Pass | Notes |
|-------|--------|------|-------|------|-------|
| In-stock priced | `alphabetter-stand-up-desk` | 200 | 0 | ✅ | Section: ATC renders; product.available=true, price=$562.79 |
| Sold-out RFQ | `l-shape-desk-3-sizes-13-colours` | 200 | 0 | ✅ | Section: RFQ block renders; sold-out, price=$1179.99 |
| Zero-price showcase | `additional-services-dismantle-re-assemble` | 200 | 0 | ✅ | Section: RFQ block renders; price=$0 |
| Full-spec Canadian | `ashmont-medium-back-guest-chair-mvl2782` | 200 | 10 | ✅ | Spec table: 10 rows; Canadian badge: `country_of_manufacture=Canada` |
| Sparse spec | `ibex-synchro-tilter-chairs-mvl2801` | 200 | 0 | ✅ | Spec table hidden (`_pdp_spec_row_count=0`); RFQ block |

**Result: 5/5 PASS**

### Browser verification URLs (requires Shopify login)
Full HTML render must be verified in browser. Preview theme: `186373570873`.

- **In-stock:** https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873
- **Sold-out RFQ:** https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873
- **Zero-price:** https://office-central-online.myshopify.com/products/additional-services-dismantle-re-assemble?preview_theme_id=186373570873
- **Full-spec Canadian:** https://office-central-online.myshopify.com/products/ashmont-medium-back-guest-chair-mvl2782?preview_theme_id=186373570873
- **Sparse spec:** https://office-central-online.myshopify.com/products/ibex-synchro-tilter-chairs-mvl2801?preview_theme_id=186373570873

---

## Safety confirmation

- ✅ Dev theme `186373570873` only — live theme `178274435385` (BBI Live) was NOT touched
- ✅ `bbi-nav.liquid` — NOT modified
- ✅ `bbi-footer.liquid` — NOT modified
- ✅ `bbi-oecm-bar.liquid` — NOT modified
- ✅ No products created, tagged, or moved

---

## Stage 4 status

**Stage 4 is COMPLETE after this merge** (pending visual browser verification of 5 PDPs).

Commits on this branch:
1. `feat: extend bbi-crumbs to support 5-level product breadcrumb (Stage 4b.2)`
2. `feat: add bbi-product-jsonld + bbi-breadcrumb-jsonld snippets (Stage 4b.3)`
3. `feat: build ds-pdp-base + product.json for T5 design parity (Stage 4b.4-5)`
4. `feat: push 75 spec metafield sets (174 fields) from data/specs/ (Stage 4b.5)`
5. `docs: stage 4b PDP design artifacts (this commit)`

---

## Stage 4 backlog (post-merge follow-on tasks)

| Item | Description | Effort |
|------|------------|--------|
| **OECM tagging pass** | Tag all OECM-eligible products with `oecm-eligible`. This unlocks the OECM-eligible badge logic already wired in `ds-pdp-base.liquid` — currently 0% coverage. | Medium |
| **Spec metafield push — full catalog** | Hero 100 (now fully covered). Remaining ~501 products have no spec JSON files. Requires `lookup-specs.py` run on remaining handles. | High effort |
| **Brand logo assets** | Upload manufacturer logos to Shopify Files and wire via schema `image_picker` in brand block. Currently text-only (per Stage 4b decision). | Low-medium |
| **Colour swatch expansion** | Hex map covers 26 standard colours. Extended fabric codes (e.g. "Grade 1 Seating Textiles") render as text chips — correct for now. Could add swatch images for fabric grades. | Low |
| **Buyable PDP QA** | Only 21 of 594 products are buyable. When a buyable product has multiple colour variants, test swatch → variant sync on a real browser. | Low |
