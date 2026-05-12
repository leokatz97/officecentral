# Stage 3.2a — Decision Document

**Generated:** 2026-05-07  
**Based on:** `stage-3.2a-t4-spec-extract.md`, `stage-3.2a-current-section-audit.md`, `stage-3.2a-subcollection-sample.csv`, `stage-3.2a-image-cropping-diagnosis.md`, `stage-3.2a-hub-gap-analysis.csv`  
**Inputs to:** Stage 3.2b (build pass)

---

## 0. Pre-Condition: Template Coverage Reality

Before discussing the design fixes, a structural finding that changes the scope of 3.2b:

**The 31 collections with `template_suffix = base` all have 0 products.** These are newly created collection shells from Stage 3.x work. The 68 original product-bearing sub-collections (from the Stage 3 audit CSV) use the **legacy Starlite default template** (`collection.json`), NOT `ds-cs-base.liquid`.

Practical consequence:
- Fixing `ds-cs-base.liquid` today affects 31 empty pages — nothing is visible to visitors
- The hero CTA "Get a free seating recommendation" flagged in the brief is from the **Starlite `main-collection` section**, not from `ds-cs-base.liquid` (which has no hero CTA at all)
- 3.2b must be paired with a **product population pass** (migrate products to the 31 new template=base collections, OR migrate the 68 legacy collections to template=base) before any fix is visible in production

---

## 1. T4 Spec Gaps

**8 gaps total — 2 high, 2 medium, 4 low**

| ID | Gap | Severity | Blocker for 3.2b? |
|---|---|---|---|
| GAP-T4-1 | Hero: no CTA button (brief requires "Shop all [parent]" CTA) | Medium | No — easy add; data available via schema settings |
| GAP-T4-2 | Hero: stats line not specified for T4 | Medium | No — decision needed (see §3 below) |
| **GAP-T4-3** | **Product card image ratio: spec says 4:5, code is 4:3, catalog is 1:1** | **High** | **YES — decision needed before CSS change (see §4)** |
| **GAP-T4-4** | **CTA routing: quote-only tiles link to /pages/quote, not PDP** | **High** | **YES — must fix (BBI rule #2 violation)** |
| GAP-T4-5 | Product card badges (sale/new/sold) not implemented | Low | No — defer; catalog badge coverage unknown |
| GAP-T4-6 | Phone CTA band missing OECM trust line | Low | No — add copy, no new component |
| GAP-T4-7 | Brands strip: not specified for T4 | Low | No — see §5 |
| GAP-T4-8 | OECM bar shared snippet not present | Low | No — `bbi-oecm-bar.liquid` not yet created; defer |

**Decisions needed from you before 3.2b starts:**

1. **GAP-T4-3:** Image container ratio — **1:1 square** (fits actual 1:1 catalog stock, zero cropping) or **4:5 portrait** (matches component spec, would clip sides 20%)?
2. **GAP-T4-2 + §3:** Hero stats line on T4 — ship an analog or skip?

---

## 2. Filter Rail Verdict: DEFER UNCHANGED

Tag census from Stage 3.1a is unchanged — all advanced namespaces at 0%:

| Namespace | Coverage |
|---|---|
| `subcategory:` | 0% |
| `brand:` | 0% |
| `height:` | 0% |
| `fabric:` | 0% |
| `warranty:` | 0% |

The current sidebar filter (type: and room: namespaces) has functional coverage (87.9% / 46.2%) and is retained as-is. No new filter work in 3.2b.

---

## 3. Hero Stats Line on T4 — Recommendation: YES (light version)

T3 ships with two stats lines (added Stage 3.1c.1): a brand count and a warranty/OECM headline. The data that drives these on T3 is meaningful at the hub level (e.g., "16 sub-categories · 30+ brands" for Seating).

At the T4 (sub-collection) level, the analogous stat is simpler: `{N} products · [parent_hub_name]`. This is already rendered as the default `hero_subtitle` ("N product(s) available").

**Recommendation:** Do NOT ship a separate stats line for T4. The product count subtitle is the right density for a sub-collection. Adding a brand count or warranty headline at the sub-collection level would be noise. The hero subtitle is sufficient.

If the hero CTA button is added (GAP-T4-1), the hero strip becomes: label → H1 → subtitle (product count) → CTA button. That's the right rhythm.

---

## 4. Image Cropping Fix Scope

**Root cause confirmed:** `aspect-ratio: 4/3` (landscape) container + `object-fit: cover` on 1:1 source images → ~25% vertical clip. Chair headrests and foot rings cut off.

**Recommended fix:** Change to **1:1 square** container.

Rationale: Actual catalog images are uniformly 1:1. The 4:5 component spec was written for a portrait photo convention BBI doesn't use. A 1:1 container eliminates all cropping for current stock. If the AI image pipeline later produces portrait images, the container can be revisited.

**Code changes in `ds-cs-base.liquid`:**

CSS (change `aspect-ratio` only):
```css
/* BEFORE */
.ds-cs__card-img { aspect-ratio: 4/3; overflow: hidden; ... }

/* AFTER */
.ds-cs__card-img { aspect-ratio: 1/1; overflow: hidden; ... }
```

Liquid (add CDN-level square crop):
```liquid
/* BEFORE */
{{ product.featured_media | image_url: width: 480 | image_tag: loading: 'lazy', alt: card_img_alt }}

/* AFTER */
{{ product.featured_media | image_url: width: 480, height: 480, crop: 'center' | image_tag: loading: 'lazy', alt: card_img_alt }}
```

One section file change. Propagates instantly to all 31 template=base collections.

**Awaiting your decision** on 1:1 vs 4:5 before writing this in 3.2b.

---

## 5. Brands Carried Treatment — Recommendation: Omit for T4

T3 hubs have a "brand plates" section (8 brands per hub). T4 sub-collections are narrower in scope — a sub-collection is already filtered by product type (e.g., executive desks, active seating). Showing brand plates at this level would either:
- Repeat the same 8 brands as the parent hub (redundant)
- Require per-sub-collection brand curation (high content overhead × 31 collections)

**Recommendation:** No brands strip on T4. Exception: brand-specific sub-collections (keilhauer, ergocentric, global-furniture, global-teknion) could include a single brand spotlight block in the phone CTA area — but that's a content task, not a section change.

---

## 6. CTA Routing Fix Scope

**Bug:** When `is_quote_only = true` (price == 0 OR available == false), the tile footer shows:
```liquid
<a href="/pages/quote?product={{ product.handle }}&source=collection&lead_type=quote"
   class="ds-cs__card-quote-cta">
  Request a Quote →
</a>
```
This routes directly to the quote form, bypassing the PDP.

**BBI rule #2:** Unbuyable products keep their PDP live as a lead-capture page. The tile should link to the PDP, which renders `.bbi-cta-pdp` (the inline quote block).

**Scale:** ~100% of future tiles will have `is_quote_only = true` based on sampled catalog data (all sampled products have price=None / available=False). Every tile in every template=base collection needs this fix.

**Code change (6 lines):**
```liquid
/* BEFORE — routes to /pages/quote */
{%- if is_quote_only -%}
  <a href="/pages/quote?product={{ product.handle }}&source=collection&lead_type=quote"
     class="ds-cs__card-quote-cta" itemprop="url">
    Request a Quote →
  </a>

/* AFTER — routes to PDP */
{%- if is_quote_only -%}
  <a href="{{ product_url }}"
     class="ds-cs__card-quote-cta" itemprop="url">
    Request a Quote →
  </a>
```

`product_url` is already assigned at line 441 (`assign product_url = product.url`) and is already used for the image and title links. The change drops the `/pages/quote` href and uses `product_url` instead.

No change to `is_quote_only` detection logic — the detection is correct, only the routing destination is wrong.

---

## 7. Per-Collection Schema Config Gap (Structural Risk)

**Finding:** `collection.base.json` has no pre-populated settings. The schema defaults are:
- `parent_category_handle: "seating"`
- `parent_category_title: "Seating"`

With 31 template=base collections all using the same default settings, 30 of 31 will show "Seating" in the breadcrumb regardless of their actual parent hub.

**Fix options:**
- A: Set schema settings per-collection via Admin API (scripted, not a theme code change)
- B: Derive parent from collection tags using Liquid (auto-detect, brittle)
- C: Derive parent from collection handle prefix using Liquid (auto-detect, requires naming convention)

**Recommendation:** Option A — write a one-shot Python script (`set-base-collection-schemas.py`) that reads a mapping CSV and updates each collection's `settings` via the Shopify Admin API. This is analogous to the `set-collection-sort.py` / `set-collection-template-suffix.py` scripts already in `scripts/`. Not a 3.2b theme code change but a 3.2b-launch prerequisite.

---

## 8. Net 3.2b Work Estimate

### Files to modify

| File | Change type | Notes |
|---|---|---|
| `theme/sections/ds-cs-base.liquid` | **Targeted fixes** | 4 changes: hero CTA button, image aspect-ratio, CTA routing, optional OECM trust line in phone CTA |

Only **one section file** needs to change. It propagates to all 31 template=base collections automatically.

### New snippets needed
None for 3.2b. `bbi-oecm-bar.liquid` remains deferred.

### Scripts needed (not theme code, but 3.2b launch prerequisite)
- `scripts/set-base-collection-schemas.py` — set parent_category_handle + parent_category_title + parent_category_title per collection. Input: CSV mapping (31 rows). One-time run, safe to re-run.

### Change summary

| # | Change | Location | Lines affected |
|---|---|---|---|
| 1 | Add hero CTA button ("Shop all [parent]") | ds-cs-base.liquid hero strip (~line 303) | +4 lines |
| 2 | Fix image aspect-ratio: 4/3 → 1/1 (pending decision) | ds-cs-base.liquid CSS (~line 197) + Liquid (~line 450) | 2 lines changed |
| 3 | Fix CTA routing: /pages/quote → product_url | ds-cs-base.liquid card footer (~line 467) | 1 line changed |
| 4 | Add OECM trust line to phone CTA | ds-cs-base.liquid phone CTA band (~line 536) | +2 lines |

**Total theme changes: 4 targeted edits, 1 file.** Small scope — no structural rework needed.

---

## 9. Risks

### Risk 1 — All 31 template=base collections have 0 products (HIGH)
Fixing ds-cs-base.liquid today produces zero visible change on the live site. The hero CTA, image crop fix, and CTA routing fix are all invisible until products are populated into these collections. 3.2b must include a product migration or population plan to be meaningful.

**Mitigation:** Define the product migration strategy before writing 3.2b code. The 31 new collections need to either:
- Import products from the 68 legacy sub-collections (risky — would split inventory views)
- OR: flip the 68 legacy sub-collection handles to template=base (simpler — but requires schema config for each)

**This is the biggest risk for 3.2b and may require a separate 3.2a.5 decision session.**

### Risk 2 — Default schema settings apply to all 31 collections (HIGH)
All 31 template=base collections default to `parent_category_handle: "seating"`. Without the schema config script, every page except the actual seating sub-collections will show wrong breadcrumbs and wrong eyebrow labels.

**Mitigation:** Write and run `set-base-collection-schemas.py` before promoting any template=base collection to the live theme.

### Risk 3 — Image ratio change affects card grid visual rhythm (LOW)
Changing from 4:3 to 1:1 makes product cards taller. The 4-column grid row height increases by ~33%. This may affect page length and visual balance with the filter sidebar. Should be previewed on the dev theme.

**Mitigation:** Preview on dev theme URL before promoting to live.

### Risk 4 — Hero CTA "Shop all [parent]" is redundant with breadcrumb (LOW)
The breadcrumb already links to the parent collection. A "Shop all Seating" button in the hero strip may be redundant or dilute the CTA hierarchy. Consider whether it's needed if the hero just has a product count.

**Mitigation:** Leo to confirm this is the right UX direction (brief says yes, but worth calling out).

---

## 10. Recommended 3.2b Sequence

1. **Decide: image ratio** — 1:1 or 4:5? (Leo confirms)
2. **Decide: product migration strategy** — how do the 31 template=base collections get products?
3. Fix `ds-cs-base.liquid` (4 targeted edits — ~30 min)
4. Write `scripts/set-base-collection-schemas.py` with a mapping CSV for all 31 collections
5. Run schema config script on dev theme
6. Verify on dev theme preview URL for each of the 9 parent hubs
7. Promote to live after walkthrough

**Estimated scope:** Small. One section file + one script. No new snippets. No template changes. The structural complexity is all in the product migration decision (item 2), not the code.
