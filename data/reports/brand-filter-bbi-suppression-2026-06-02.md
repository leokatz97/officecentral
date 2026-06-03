# Brand Filter — BBI Suppression + Facet-Render Discovery — 2026-06-02

**Branch:** `feature/brand-filter-bbi-suppression-2026-06-02`
**Theme write:** `sections/ds-cs-base.liquid` → role=main `186373570873`
**Status:** suppression shipped + asset-verified · **Brand filter NOT live (facet does not render — see Discovery)**

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
