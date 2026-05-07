# Stage 3.1b — Category Hub T3 Layout: Deliverable Report

**Date:** 2026-05-07  
**Branch:** `feature/stage-3.1b-hub-t3-layout`  
**Dev theme:** `186373570873`  
**Live theme (untouched):** `186495992121`  
**Commits:** 3 (3.1b.3, 3.1b.4, 3.1b.5)

---

## 1. Spec Gaps (Phase 1)

All 8 gaps resolved from `docs/strategy/design-system.md` and `docs/strategy/bbi-component-spec-v1.md`. No halts required.

| gap_id | resolved_from_DS | resolution_value | notes |
|---|---|---|---|
| GAP-A | Yes | Schema settings `hero_stats_line1` / `hero_stats_line2`; defaults: "30+ commercial furniture brands" + "OECM-eligible · Quote in 1 business day" | DS §07 mandates 1-business-day SLA and OECM trust line |
| GAP-B | Yes (user pre-confirmed) | Navigation pills sourcing `tile` block `link` + `title` | Tag-filtering deferred to Stage 3.1c |
| GAP-C | Yes | 4-column desktop, 2-column mobile, 1-column <480px; schema `products_per_page` default 12 | Inferred from T3 locked render + DS spacing scale |
| GAP-D | Yes | `product.available == false OR product.price == 0 OR product.tags contains 'showcase'` → "Request a Quote" CTA | Component spec §03 Cards explicit |
| GAP-E | Yes (Phase 2 methodology) | Top 8 vendors by product count per hub from Shopify API; schema `brand_plate` blocks for editorial override | Data in `stage-3.1b-brands-per-hub.csv` |
| GAP-F | Yes | `.bbi-badge--canadian` (maple leaf SVG, `#D4252A`, 22px) + `.bbi-badge--oem` (outlined gray) | Component spec §04 Badges explicit |
| GAP-G | Yes | 12/page schema default; `paginate` tag with `by: products_per_page` setting | T3 render inference |
| GAP-H | Yes | `bbi-oecm-bar.liquid` created in Phase 3; Agreement 2025-470; links to `/pages/oecm` | Extracted from `ds-lp-oecm.liquid` defaults + DS tokens |

Full resolution details: [`stage-3.1b-spec-gap-resolutions.md`](stage-3.1b-spec-gap-resolutions.md)

---

## 2. Top Brands Per Hub (Phase 2)

Brand data: [`stage-3.1b-brands-per-hub.csv`](stage-3.1b-brands-per-hub.csv)

**Observation:** "Brant Business Interiors" is the dominant vendor across all populated hubs (154/91/78/98/81/89 products respectively) — these are products resold under the store's own vendor label. Real third-party vendor depth is shallow, especially for accessories (only Humanscale as a named brand) and storage (only Offices to Go + Heartwood). Brand plate slots have placeholders for editorial override.

**3 empty hubs fallback brand set:** ergoCentric · Keilhauer · Global Furniture · Teknion (Brands 5–8 omitted as placeholders would show blank names).

| hub_handle | top_brand_1 | top_brand_2 | top_brand_3 | top_brand_4 | plate_count |
|---|---|---|---|---|---|
| seating | Brant Business Interiors | Global Furniture Group | ObusForme | Offices to Go | 5 |
| desks | Brant Business Interiors | Offices to Go | Global Furniture Group | Safco | 4 |
| storage | Brant Business Interiors | Offices to Go | Heartwood Manufacturing | — | 3 |
| tables | Brant Business Interiors | Teknion | Safco | Offices to Go | 5 |
| boardroom | Brant Business Interiors | Teknion | Safco | Offices to Go | 5 |
| accessories | Brant Business Interiors | Humanscale | — | — | 2 |
| ergonomic-products | ergoCentric (fallback) | Keilhauer (fallback) | Global Furniture (fallback) | Teknion (fallback) | 4 |
| panels-room-dividers | ergoCentric (fallback) | Keilhauer (fallback) | Global Furniture (fallback) | Teknion (fallback) | 4 |
| quiet-spaces | ergoCentric (fallback) | Keilhauer (fallback) | Global Furniture (fallback) | Teknion (fallback) | 4 |

---

## 3. `bbi-oecm-bar.liquid` Snippet (Phase 3)

**File:** `theme/snippets/bbi-oecm-bar.liquid`  
**Size:** 82 lines / ~3.1 KB  
**Push status:** 200 OK

**Rendered HTML structure:**
```html
<aside class="bbi-oecm-bar" aria-label="OECM purchasing programme">
  <div class="bbi-oecm-bar__inner">
    <div class="bbi-oecm-bar__left">
      <span class="bbi-oecm-bar__dot"></span>        <!-- red dot accent -->
      <div class="bbi-oecm-bar__copy">
        <p class="bbi-oecm-bar__label">Ontario procurement</p>
        <p class="bbi-oecm-bar__heading">OECM vendor of record — Supplier Partner Agreement 2025-470</p>
        <p class="bbi-oecm-bar__sub">Ontario's broader public sector can purchase without re-tendering...</p>
      </div>
    </div>
    <a class="bbi-oecm-bar__link" href="/pages/oecm">OECM purchasing details →</a>
  </div>
</aside>
```

Tokens: DS default scheme (#FAFAFA surface, `#E5E5E7` borders, `#D4252A` dot accent). Self-contained `<style>` block. No scope overrides.

---

## 4. `ds-cc-base.liquid` Changes (Phase 4)

### 4a — Hero CTA
**Before:** Static label "Get a free design consultation" linking to `/pages/quote`  
**After:** Dynamic `"Shop all [collection.title]"` linking to `/collections/<collection.handle>`  
**Rationale:** T3 spec — hero CTA routes through the smart-collection, not the design-services funnel.

### 4b — Skip-by-sector bar
**Before:** Not present  
**After:** `<nav class="ds-cc__skip-bar">` with 5 industry chips (Healthcare / Education / Government / Non-Profit / Professional Services) each routing to `/pages/<industry>`. Controlled by `show_sector_bar` checkbox (default true).

### 4c — 30+ brands band
**Before:** Not present  
**After:** `<div class="ds-cc__brands-band">` — copy "30+ commercial furniture brands across 3 dealer tiers · Ontario OECM partner" + CTA link to `/pages/brands`. Controlled by `show_brands_band` checkbox (default true).

### 4d — Sub-cat filter chips
**Before:** Not present  
**After:** `<nav class="ds-cc__filter-bar">` — pill strip generated from `tile` block `title` + `link` settings. Shown only when 2+ tiles exist. Controlled by `show_filter_chips` checkbox (default true). Navigation links — no JS.

### 4e — Brand plates section
**Before:** `brand_callout` blocks (max 2, rich editorial spotlight)  
**After:** `brand_callout` blocks retained (backward compat); NEW `brand_plate` block type (max 8) added. Brand plates section renders as 4-column grid (desktop) with Canadian badge + Authorized dealer badge per plate. Schema `brand_plate_canadian` checkbox controls the maple-leaf badge.

### 4f — Grid mode toggle
**Before:** Tiles only, always rendered  
**After:** `grid_mode` schema select (`tiles` / `products` / `both`). When `products` or `both`: paginated product grid renders (`.ds-cc__product-grid`, 4-column desktop). Unbuyable detection via `product.available == false OR product.price == 0 OR product.tags contains 'showcase'` → "Request a Quote" button. `products_per_page` range setting (default 12, 4–48).

### 4g — OECM bar
**Before:** No OECM bar in the section  
**After:** `{%- render 'bbi-oecm-bar' -%}` placed between brand plates and phone CTA closer.

### 4h — Integrity checks
All checks passed after every edit:

| Check | Result |
|---|---|
| `render 'bbi-nav'` present | ✓ (1 occurrence) |
| `render 'bbi-crumbs'` present | ✓ (2 occurrences — conditional + else) |
| `render 'bbi-footer'` present | ✓ (1 occurrence) |
| `render 'bbi-oecm-bar'` present | ✓ (1 occurrence) |
| `{% schema %}` present | ✓ |
| `{% endschema %}` present | ✓ |
| Schema JSON valid (`json.loads`) | ✓ |
| Closing wrapper `</div>` (`.ds-cc` root) | ✓ |

---

## 5. Per-Hub grid_mode + Brand Plate Population (Phase 5)

| hub_handle | grid_mode | products_per_page | brand_plates | notes |
|---|---|---|---|---|
| seating | both | 12 | 5 (BBI, Global Furniture Group, ObusForme, Offices to Go, Teknion) | |
| desks | both | 12 | 4 (BBI, Offices to Go, Global Furniture Group, Safco) | |
| storage | both | 12 | 3 (BBI, Offices to Go, Heartwood Manufacturing) | |
| tables | both | 12 | 5 (BBI, Teknion, Safco, Offices to Go, Global Furniture Group) | |
| boardroom | both | 12 | 5 (BBI, Teknion, Safco, Offices to Go, Global Furniture Group) | |
| accessories | both | 12 | 2 (BBI, Humanscale) | |
| ergonomic-products | tiles | 12 | 4 (ergoCentric, Keilhauer, Global Furniture, Teknion) — fallback | empty hub |
| panels-room-dividers | tiles | 12 | 4 (ergoCentric, Keilhauer, Global Furniture, Teknion) — fallback | empty hub |
| quiet-spaces | tiles | 12 | 4 (ergoCentric, Keilhauer, Global Furniture, Teknion) — fallback | empty hub |

All templates validated with `python3 -c 'import json; json.load(open(...))'` after update.

---

## 6. Push Results (Phase 6)

| file | push status | notes |
|---|---|---|
| `snippets/bbi-oecm-bar.liquid` | 200 ✓ | First push in Phase 3 |
| `sections/ds-cc-base.liquid` | 200 ✓ | |
| `templates/collection.seating.json` | 200 ✓ | Required retry (section schema propagation) |
| `templates/collection.desks.json` | 200 ✓ | Required retry |
| `templates/collection.storage.json` | 200 ✓ | Required retry |
| `templates/collection.tables.json` | 200 ✓ | Required retry |
| `templates/collection.boardroom.json` | 200 ✓ | Required retry |
| `templates/collection.accessories.json` | 200 ✓ | |
| `templates/collection.ergonomic-products.json` | 200 ✓ | |
| `templates/collection.panels-room-dividers.json` | 200 ✓ | |
| `templates/collection.quiet-spaces.json` | 200 ✓ | |

**Total: 11/11 files — 200 OK**

Note on retries: 5 populated hub templates initially returned 422 ("Type must be defined in schema"). Shopify validated the template JSON against the section schema before the `brand_plate` block type had propagated. A 3-second delay + retry resolved all 5. The section itself pushed cleanly first-pass.

---

## 7. Spot-Check Results (Phase 7)

| file | worktree ≡ dev theme | content checks |
|---|---|---|
| `sections/ds-cc-base.liquid` | ✓ exact match | nav ✓ · crumbs ✓ · footer ✓ · oecm-bar ✓ · brand_plate ✓ · grid_mode ✓ |
| `templates/collection.seating.json` | ✓ JSON content equal (formatting differs — Shopify normalizes whitespace) | grid_mode=both ✓ · brand_plates populated ✓ |
| `templates/collection.ergonomic-products.json` | ✓ JSON content equal | grid_mode=tiles ✓ · fallback brands ✓ |
| `snippets/bbi-oecm-bar.liquid` | ✓ exact match | bbi-oecm-bar__heading ✓ · 2025-470 ✓ · bbi-oecm-bar ✓ |

---

## 8. Protected Files Confirmation

- **Theme `186495992121` (live):** NOT touched. Zero API calls against this theme ID.
- **`bbi-nav.liquid`:** NOT modified.
- **`bbi-footer.liquid`:** NOT modified.
- **`bbi-crumbs.liquid`:** NOT modified.

---

## 9. Stage 3.1d Backlog Item

**Smart-collection rule fixes for 3 empty hubs**

The three empty hubs (`ergonomic-products`, `panels-room-dividers`, `quiet-spaces`) shipped the T3 layout with `grid_mode=tiles` and fallback brand plates. Their Shopify smart-collection tag rules are not configured to pull in any products — `collection.products_count == 0` for all three. Stage 3.1d must:

1. Audit and update smart-collection rules for `ergonomic-products` (currently `type:Ergonomic Products` or similar — check live admin)
2. Same for `panels-room-dividers` (panels/dividers category tag rules)
3. Same for `quiet-spaces` (acoustic pods / phone booths)
4. After rules fire and products appear, switch `grid_mode` from `tiles` to `both` on those three templates

---

## 10. Unexpected Drift / Halts

- **No halts required.** All 8 spec gaps resolved without surfacing user questions.
- **Shopify schema propagation delay** caused 422s on first push of 5 templates. Resolved with a 3-second wait + retry. Expected behavior when section and template are pushed in rapid sequence.
- **Vendor data shallow:** "Brant Business Interiors" accounts for 80–95% of products in each hub. The remaining named brands are 2–30 products each. Brand plate slots are functional and editor-overridable — this is a data quality issue, not a build issue. Recommend a vendor-taxonomy clean-up pass before launch.
- **`cta_url` schema setting removed** (4a change): The old `cta_url` setting was removed from schema because the hero CTA now dynamically routes to `/collections/<handle>`. Any collection.*.json files that had `cta_url` in their settings were cleaned up by the update script.

---

**Do not merge.** Branch halted at `feature/stage-3.1b-hub-t3-layout`. Awaiting Steve's review.

---

## Stage 3.1b.1 Hotfix — Brand Plate Replacement

**Commit:** `44181dd`  
**Date:** 2026-05-07

### Why the data-derived approach didn't ship

The Phase 2 Shopify vendor query populated brand plates from live product data. Two problems were identified post-push:

1. **"Brant Business Interiors" as plate #1 on every hub.** The store applies its own vendor label to the majority of resold products (154/91/78/98/81/89 products per hub). Showing the store's own label as a "brand plate" is meaningless to buyers and the `/collections/brant-business-interiors` link would 404.
2. **Insufficient third-party brand depth.** After excluding BBI, remaining named brands were 1–5 per hub (e.g. accessories had only Humanscale; storage had only Offices to Go + Heartwood Manufacturing). The T3 spec calls for 4–8 recognizable manufacturer brands per plate section.

### Pre-hotfix state

Full audit in [`stage-3.1b.1-pre-hotfix-brand-plates.csv`](stage-3.1b.1-pre-hotfix-brand-plates.csv).

Summary:
| hub | plates before hotfix |
|---|---|
| accessories | Brant Business Interiors, Humanscale |
| boardroom | Brant Business Interiors, Teknion, Safco, Offices to Go, Global Furniture Group |
| desks | Brant Business Interiors, Offices to Go, Global Furniture Group, Safco |
| seating | Brant Business Interiors, Global Furniture Group, ObusForme, Offices to Go, Teknion |
| storage | Brant Business Interiors, Offices to Go, Heartwood Manufacturing |
| tables | Brant Business Interiors, Teknion, Safco, Offices to Go, Global Furniture Group |

All 24 plates used `/collections/<vendor-slug>` links — none verified to exist.

### Post-hotfix state

All 6 populated hubs now have the same 4-plate curated fallback set, matching the 3 empty hubs:

| brand_plate_name | brand_plate_link | brand_plate_canadian |
|---|---|---|
| ergoCentric | /pages/brands#ergocentric | true |
| Keilhauer | /pages/brands#keilhauer | true |
| Global Furniture | /pages/brands#global-furniture | false |
| Teknion | /pages/brands#teknion | false |

Note: the 3 empty hubs (set in Stage 3.1b Phase 5) have Global Furniture and Teknion marked `canadian=true` — an artifact of the Phase 5 script's CANADIAN_BRANDS set. The populated hubs now correctly reflect the user's spec (Canadian: omitted → false). This minor discrepancy in the empty hubs can be corrected in a separate cleanup pass if needed.

### Push results

| file | status |
|---|---|
| templates/collection.accessories.json | 200 ✓ |
| templates/collection.boardroom.json | 200 ✓ |
| templates/collection.desks.json | 200 ✓ |
| templates/collection.seating.json | 200 ✓ |
| templates/collection.storage.json | 200 ✓ |
| templates/collection.tables.json | 200 ✓ |

### Spot-check confirmation

Pulled `seating` and `ergonomic-products` from dev theme `186373570873`:

- **seating** (populated): 4 plates — ergoCentric `/pages/brands#ergocentric` canadian=true · Keilhauer `/pages/brands#keilhauer` canadian=true · Global Furniture canadian=false · Teknion canadian=false ✓
- **ergonomic-products** (empty): unchanged — same 4 plates as before hotfix ✓

### Empty hubs confirmation

`git diff` against HEAD confirmed zero changes to `collection.ergonomic-products.json`, `collection.panels-room-dividers.json`, and `collection.quiet-spaces.json` before the script ran.

---

**3.1b.3** — cleared per-hub `cta_label` so the section default (`Shop all <title>`) renders cleanly. Affected all 9 hubs (old values: "Get a free seating recommendation", "Get a free space plan", etc.). Commit `b12a558`. All 9 pushes 200 OK.

**3.1b.2 cleanup** — Canadian flag corrected on Global Furniture and Teknion plates across the 3 empty hubs. All 9 hubs now consistent: ergoCentric + Keilhauer = `canadian=true`, Global Furniture + Teknion = `canadian=false`. Commit `bf3a6ff`. Pushed 200 OK.

**Do not merge.** Halted at `feature/stage-3.1b-hub-t3-layout`.
