# Brand Filter — BBI Suppression + Facet-Render Discovery — 2026-06-02

**Branch:** `feature/brand-filter-bbi-suppression-2026-06-02`
**Theme write:** `sections/ds-cs-base.liquid` → role=main `186373570873`
**Status:** ✅ **RESOLVED 2026-06-02** — facet-render bug root-caused (`push` no-op) + fixed + deployed + fresh-render verified. Brand/Type/Room facets live; #88 BBI suppression now active; card-label dealer name suppressed. **See "Resolution" at bottom.**

---

## Phase 0 — Mechanism

BBI collection-page filters are **theme-native client-side JS**, not Shopify Search & Discovery.
Implementation: `theme/sections/ds-cs-base.liquid` (base for all sub-collection pages).

| Concern | Location | Detail |
|---|---|---|
| Brand facet source | lines 352–356 | `vendor_list` built from raw `product.vendor` |
| Brand checkboxes | lines 413–432 | one chip per distinct vendor |
| Filter behavior | lines 668–684 | JS toggles `.ds-cs__card--hidden` by `data-vendor` |
| Card vendor attr | line 497 | `data-vendor="{{ product.vendor | downcase | url_param_escape }}"` |

No S&D facets, no brand metafield.

## Phase 0 — Source-field comparison (live Admin-API, 657 products)

| Source | Coverage | Suppresses BBI cleanly? | Build cost | Verdict |
|---|---|---|---|---|
| **Raw `vendor` (current)** | **657/657 (100%)** | yes — one substring skip | 1 Liquid edit | ✅ chosen |
| `brand:*` tag facet | 525/657 — 132 untagged vanish; no `brand:teknion` (only `brand:global-teknion`); `brand:brant-business-interiors` exists on 7 → does NOT auto-suppress | needs explicit tag-skip anyway | full rewrite | ✗ |
| brand metafield | not populated | n/a | new pipeline | ✗ |

The original Phase-3 hypothesis ("BBI lacks a brand tag, so tags auto-suppress") is **false**: 7 products carry `brand:brant-business-interiors`, and a tag facet would drop 132 untagged real-brand products and break Teknion.

### Live vendor distribution (suppression scope confirmed)
- `Brant Business Interiors` = **119** ✅ (matches build-state residual)
- `Office Central & Brant Business Interiors` = **4** (second dealer string — also suppressed)
- 36 real manufacturer brands populate the rest (Global Furniture Group 200, Heartwood Manufacturing 80, OTG/Offices to Go 76, IOF 26, Office Star 18, Horizon 15, Richelieu 12, Safco/MityBilt/Teknion 11 ea, Fellowes 10, Deflecto 9, … single-product tail).

## Phase 2 — Suppression edit (shipped)

`vendor_list` builder now skips any vendor whose downcased name contains `brant business interiors` (substring → catches both dealer strings, 123 products). Cards keep `data-vendor` → residual stays browsable, just not brand-filterable.

**Deploy gate:**
- Watcher preflight: no `shopify theme dev` process running.
- Target verified `role=main` via `GET /themes.json` (theme `186373570873`; "Dev" in name is historical).
- Admin-API asset readback: suppression present, old unconditional push removed (count 1), **byte-for-byte MATCH** (36,643 bytes).

## ⚠️ Discovery — facets do not render

Live-page verification (cache-busted full render **and** Section Rendering API) across `l-shape-desks`, `all-desks`, `desks`, `all-seating`, `executive-desks`, `seating`:

- Filter sidebar renders **only the Price filter** on every collection (smart and manual).
- **Brand, Type, AND Room facets render zero chips** everywhere.
- Cards render correctly (24/page) with current `data-vendor` values — they're inside `{% paginate %}`.

**Root cause:** `collection.all_tags` (line 345) and the **unpaginated** `for product in collection.products` (line 352, outside the `{% paginate %}` block) **yield empty** in the rendered section context. Classic Shopify behavior — `collection.products` referenced outside a `{% paginate %}` block returns nothing. Data is valid (Admin-API confirms products carry `type:desks`/`room:private-office` + real vendors).

**Consequences:**
- ✅ Suppression logic correct, deployed, asset-verified, forward-compatible.
- ❌ Brand filter NOT live; cannot be functionally verified; **do not mark complete.**
- 🔧 Remaining Phase 3 piece (escalated, supersedes the "50-cap" item): fix the unpaginated vendor/tag enumeration so Brand/Type/Room facets render across the full collection. Likely build the lists inside a `{% paginate %}` pass or via a working all-products source. Non-trivial Liquid task.

## Next Phase 3 piece (after facet-render fix)

Made-in-Canada filter + the `buy-canadian` Made-in-Canada collection (HELD handle).

---

## ✅ Resolution — facet-render bug fixed (2026-06-02)

### Real root cause: `| push:` is not a Shopify Liquid filter
The Discovery above mis-attributed the empty facets to "`collection.products` / `collection.all_tags` yield empty outside `{% paginate %}`." **That hypothesis was false.** The facet-build block ([ds-cs-base.liquid:340-365](../../theme/sections/ds-cs-base.liquid)) appended to `type_tags`/`room_tags`/`vendor_list` with `| push:` — **Shopify Liquid has no `push` filter**, so every append was a silent no-op and all three lists stayed empty arrays → all three `{% unless … blank %}` groups skipped → only the hardcoded Price filter rendered.

Proof the "outside-paginate" theory was wrong: `l-shape-desks` has **31 products** (< any pagination cap) with valid `type:`/`room:` tags and 6 vendors, yet rendered **zero** facets. A 50-cap/empty-outside-paginate cause would still enumerate a sub-50 collection. The only size- and source-independent failure is the no-op append. `push` appeared in exactly these 3 lines theme-wide; `concat` (the supported idiom) nowhere.

### Fix (Fix A + Fix B, one section file)
- **Fix A** — replaced the 3 `| push:` with the Shopify-supported `concat`-via-`split` idiom (`assign _one = x | split: '~~|~~'` → `concat: _one`). Restores Brand + Type + Room together.
- **Fix B** — card vendor label now suppresses the dealer name too (mirrors the facet substring test at line ~363): `{% unless _cv contains 'brant business interiors' %}`. Stops "Brant Business Interiors" leaking on product-card brand labels.

### Brand 50-cap: theoretical, deferred
Distribution across all **108 `base`-suffix collections**: max = **50** products, median 5, mean 8. **Zero exceed 50** (`51-100`: 0, `100+`: 0). So the unpaginated `collection.products` vendor loop sees every product on every collection today → Brand ships **complete**. `collection.products | map: 'vendor' | uniq` does NOT escape the cap; reliable >50 enumeration would need `{% paginate … by 250 %}`. Tracked as forward-compat only (triggers if a `base` collection ever grows past 50).

### Deploy + verification
- Watcher preflight PASS (no `shopify theme dev`); target `186373570873` confirmed `role=main`.
- PUT → Admin-API readback **byte-for-byte MATCH** (SHA256 `0fff77a4fcf98b15`, 37,409 bytes); live asset has **0** `push`, **3** `concat: _one`, card-label suppression present.
- **Fresh-render verification (cart-cookie cache bypass — Shopify full-page `page_cache` was serving stale pre-fix HTML to anonymous requests):** `l-shape-desks` renders **Type=4** (accessories/desk/desks/tables), **Room=2** (open-plan/private-office), **Brand=5** (Heartwood, OTG, Global, Intelligent Office Furniture, Tayco — **Brant Business Interiors absent**), `data-filter-group` brand+room+type present, **0** BBI card labels. Both fixes confirmed working.
- Note: anonymous full-page cache lags theme edits; the fix is live in the theme and serves to fresh/uncached sessions immediately, to cached anonymous sessions once `page_cache` flips.

### Known pre-existing (not this fix)
`l-shape-desks` tag hygiene: both `type:desk` AND `type:desks` (+ `type:tables`, `type:accessories`) — dedup pass later.
