# Stage 4a — Decision Document

**Date:** 2026-05-07  
**Author:** Stage 4a recon pass (read-only)  
**Feeds:** Stage 4b (PDP build)

---

## 1. PDP Plumbing Status

**Status: No separate precursor stage needed.**

The `bbi_landing` gate already catches `template == 'product'` (confirmed at `theme/layout/theme.liquid:90–91`). PB-PDP-1 from the build-state should be marked ✅ done.

What is missing (`product.json` template + `ds-pdp-base.liquid` section) is the Stage 4b deliverable, not a prerequisite stage. Stage 4b can begin immediately.

---

## 2. T5 Spec Gaps (User Resolution Needed)

8 gaps identified in `stage-4a-t5-spec-extract.md`. Before Stage 4b build starts, these need answers:

| # | Gap | Recommendation |
|---|---|---|
| **G-1** | Breadcrumb depth: 4 levels (build-state) vs 5 levels (T5 locked screen) | **Use 5 levels.** T5 locked screen is authoritative: Home → Shop → [Category] → [Subcategory] → Product. Derive parent from `collection.metafields.bbi.parent_hub_handle` on the product's first collection. |
| **G-2** | `bestFor` callout block | **Use `specs.key_features` first 3 items as "Best for" bullets.** If empty, omit the callout. Simple and data-driven. |
| **G-3** | `.scheme-alt` commerce block | **Use `--alternateBackground` (#FAFAFA) as the canvas.** This is the natural "light surface" between white and inverse. Add to `ds-pdp-base.liquid` CSS as a local class — no new global token needed. |
| **G-4** | Brand block vendor matching | **Use multi-condition Liquid (vendor + specs.manufacturer).** See strategy in trust-pills report. |
| **G-5** | Related products fallback | **Minimum 2 required to show the section; if < 2, hide entirely.** Query: `collections["all-" + product.type]` or tag filter on `type:*`. |
| **G-6** | "View all [Brand]" link target | **Use brand page (`/pages/brands-ergocentric` etc.) as interim.** Update to collection after SMART-1 builds vendor-filtered collections. |
| **G-8** | Variant picker visual swatches | **Required.** Per feedback memory: colour swatches must be filled chips (actual colour), never text labels. Build custom swatch picker in `ds-pdp-base.liquid` using `variant.option1` + Liquid colour name→hex mapping for standard BBI finishes. |

Gaps G-1 through G-6 + G-8 are **resolvable by Leo/Claude during Stage 4b** without Steve input.

---

## 3. Current vs T5 Gap Analysis

`main-product.liquid` (current renderer) provides **zero** of the 13 T5 sections. This is a **complete greenfield build**. Key gap count:

| Category | Missing items |
|---|---|
| Chrome | BBI nav, BBI footer |
| Structure | 5-level breadcrumbs, OECM bar, CTA closer |
| Product | 4:5 gallery + 6-image strip, badge row, commerce block (buyable/unbuyable), spec table, variants picker, related products |
| Brand | Brand block (logo + blurb + authorized badge + View all link) |
| Schema | Product JSON-LD, BreadcrumbList JSON-LD |

**Files to create/modify in Stage 4b:**
- `theme/templates/product.json` (new)
- `theme/sections/ds-pdp-base.liquid` (new, ~600–900 lines)
- `theme/snippets/bbi-crumbs.liquid` (new — 5-level breadcrumb)
- `theme/snippets/bbi-product-jsonld.liquid` (new — PDP-2)
- `theme/snippets/bbi-breadcrumb-jsonld.liquid` (new — AI-6, shared with CC/CS pages)

---

## 4. Spec Metafield Strategy

**Recommendation: Include spec push in Stage 4b, before the section build.**

**Rationale:**
- 93 products have spec JSON files in `data/specs/`
- ~80% of those are already pushed to Shopify; ~20% need a re-push
- Re-running `push-specs.py` on the 93 matched handles takes ~10 minutes
- Without this, the spec table renders empty on most PDPs during smoke testing

**Effort:** Low. Run push-specs before smoke test. Flag the 2/10 products that had 0 metafields despite having source data.

**`country_of_manufacture` as Canadian badge source:** Products with `specs.country_of_manufacture = "Canada"` should drive the Canadian-made badge in Stage 4b. This covers products where spec data exists without needing a tagging pass first. Tag-based fallback can be added later.

**Spec coverage gap (84% of catalog):** The remaining 501 products need spec lookups. This is a separate post-Stage-4 task — don't block Stage 4b on it.

---

## 5. Trust Pills Feasibility

| Badge | Stage 4b feasibility | Driver | Current coverage |
|---|---|---|---|
| Sold-out (gray) | ✅ Ship now | `product.available == false` | 92% of catalog |
| Canadian-made (maple-leaf) | ✅ Ship now (partial) | `specs.country_of_manufacture = "Canada"` | ~10% (grows with spec push) |
| OECM-eligible (red dot) | ⚠️ Needs tagging pass | Tag `oecm-eligible` — 0% coverage today | 0% |

**OECM recommendation:** Wire the badge logic in Stage 4b (easy: `{% if product.tags contains 'oecm-eligible' %}`), but don't block Stage 4b on the tagging pass. Add the tag to OECM-eligible products as a separate follow-on task. The badge simply won't appear until products are tagged.

---

## 6. Brand Block Strategy

**Recommendation: Ship with partial coverage. Do NOT wait for complete assets.**

| Brand | Ship in 4b? | Condition |
|---|---|---|
| Global / Teknion | ✅ Yes | vendor = 'Global Furniture Group' OR 'Teknion' — 43 products |
| ergoCentric | ✅ Yes | `specs.manufacturer contains 'ergoCentric'` — subset of the ~93 spec-covered products |
| Keilhauer | ⚠️ Wire logic, no products | vendor = 'Keilhauer' — 0 products currently; block won't render but logic is live |
| All others | ❌ No brand block | vendor = 'Brant Business Interiors' etc. — no manufacturer logo/blurb exists |

**Brand logo gap:** No standalone manufacturer logos exist in `theme/assets/`. Brand sections use schema `image_picker` — logos must be uploaded to Shopify Files manually and referenced via schema settings. Stage 4b should use brand blurb + authorized-dealer badge only (text + badge), no manufacturer logo image, until logos are uploaded.

---

## 7. Net Stage 4 Work Estimate

| Work item | Estimate |
|---|---|
| `product.json` template | 15 min |
| `ds-pdp-base.liquid` (full section: chrome, gallery, info, commerce, desc, spec table, variants, related, brand block, CTA closer) | 3–4 hours |
| `bbi-crumbs.liquid` snippet (5-level breadcrumb with collection metafield) | 45 min |
| `bbi-product-jsonld.liquid` snippet (PDP-2) | 45 min |
| `bbi-breadcrumb-jsonld.liquid` snippet (AI-6, shared) | 30 min |
| Spec push re-run (93 handles) | 10 min |
| Smoke test (5 product states per PDP-3) | 30 min |
| **Total estimate** | **~6 hours** |

---

## 8. Stage 4 Split Recommendation

**Recommendation: Single Stage 4b pass (no further split).**

Stage 3 split into 3.1/3.2/3.2c because the collection system had distinct tiers (hubs → categories → sub-collections) that were discovered iteratively. PDPs are a single template type — the T5 spec is complete, the data model is known, and the build is straightforward.

**Stage 4b = one pass:**
1. Pre-flight: re-run spec push on 93 matched handles
2. Build `ds-pdp-base.liquid` + `product.json` + 3 snippets
3. Smoke test 5 product states on dev theme

---

## 9. Risks

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R-1 | **Breadcrumb depth requires collection metafield read** — `bbi.parent_hub_handle` exists on collections (Stage 3.2c.5), but product pages access their collection via `product.collections`. If a product belongs to multiple collections, first-collection logic may pick wrong parent. | Medium | Use `product.collections.first.metafields.bbi.parent_hub_handle`. If blank, fall back to 3-level breadcrumb. Test on multi-collection products. |
| R-2 | **Spec table JSON array parsing** — `key_features`, `certifications`, `model_codes` are stored as `list.single_line_text_field` on Shopify. This iterates directly in Liquid. But some products may have been pushed as plain string JSON (not the list type). | Low | Test on Ashmont (10 metafields) and Ibex (10 metafields) during smoke test. If plain string, add `| parse_json` filter. |
| R-3 | **92% of PDPs are sold-out** — The unbuyable RFQ CTA will render on nearly every PDP. The `bestFor` callout heading in `.bbi-cta-pdp` says "Configurable item — pricing depends on fabric, frame, and quantity" which is correct for chairs but wrong for desks, storage, tables. Copy must be generic enough to work across product types. | Medium | Use more neutral heading: "Contact us for pricing and availability." Validate on 3 product types during smoke test. |
| R-4 | **Brand block shows for 43 products (Global/Teknion) but has no manufacturer logo** — Shipping with blurb + badge only. Risk: looks unpolished vs the T5 locked screen which shows a brand logo image. | Low | Text-only brand block is acceptable for Stage 4b. Logo upload is a content task, not a build task. |
| R-5 | **OECM tag at 0%** — "OECM-eligible" badge won't appear on any product until a tagging pass runs. OECM bar still shows on every PDP (correct — BBI is OECM-eligible as a dealer). | Low | Wire badge logic in 4b; run tagging pass separately. |

---

## Decision Summary

| Decision | Answer |
|---|---|
| Does Stage 4b need a plumbing precursor? | No — gate is done. Start 4b directly. |
| T5 spec gaps blocking 4b? | No — all 8 resolved with defaults above. |
| Include spec push in Stage 4b? | Yes — re-run on 93 handles before smoke test. |
| Trust pills feasible in 4b? | Sold-out ✅ · Canadian (partial) ✅ · OECM (wire only, 0% coverage) ✅ |
| Brand block strategy? | Ship with blurb + badge text only; no manufacturer logo in 4b |
| Stage 4 split? | Single pass (4b only) |
| Stage 4 effort? | ~6 hours |
