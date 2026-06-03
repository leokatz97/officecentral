# Brand Filter — BBI Suppression + Facet-Render Discovery — 2026-06-02

**Branch:** `feature/brand-filter-bbi-suppression-2026-06-02`
**Theme write:** `sections/ds-cs-base.liquid` → role=main `186373570873`
**Status:** ⚠️ **DEFERRED 2026-06-02** — `push`→`concat` + card-label suppression DEPLOYED to live theme (role=main) + byte-verified, **BUT facets STILL DO NOT render for users** (confirmed in Leo's real browser incl. cart-cookie bypass; CC's "resolved/Brand=5" was a FALSE POSITIVE). Filter system DOWN, non-harmful (zero regression). **See "Resolution" at bottom.**

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

## ⚠️ Resolution — fix DEPLOYED + byte-verified, but facets STILL DO NOT render (DEFERRED) (2026-06-02)

**Honest status: NOT resolved.** The `push`→`concat` + card-label suppression are deployed to the live theme (role=main) and Admin-API byte-verified, **but the Brand/Type/Room facets still do not render for real users** — confirmed in **Leo's real browser, including the cart-cookie cache-bypass**. CC's earlier "✅ resolved / fresh-render confirmed Brand=5" claim (preserved below, struck through) was a **FALSE POSITIVE**; it is corrected here.

### `| push:` defect (real, but not the whole cause)
The facet-build block ([ds-cs-base.liquid:340-365](../../theme/sections/ds-cs-base.liquid)) appended to `type_tags`/`room_tags`/`vendor_list` with `| push:`, which **is not a Shopify Liquid filter** (it appeared in exactly these 3 lines theme-wide; `concat` is the supported idiom). That was a genuine defect worth fixing — but replacing it with `concat`-via-`split` **did not make the facets render**, so it was not the (sole) cause of the non-render. The earlier "outside-paginate" Discovery theory was also not confirmed as the cause.

**Why the facets still don't render is UNCONFIRMED.** Candidates for a future, real-browser-confirmed redo:
- Array initialization — `assign x = '' | split: ','` may not produce the empty base array assumed.
- A deeper render-context issue (the loops over `collection.all_tags` / `collection.products` genuinely returning empty in this section's render).
- The whole diagnosis needs a fresh pass that is gated on a **real-browser** check at each step, not automated reads.

### Fix that WAS deployed (necessary, insufficient)
- **Fix A** — 3 `| push:` → `concat`-via-`split` (`assign _one = x | split: '~~|~~'` → `concat: _one`).
- **Fix B** — card vendor label suppresses the dealer name (mirrors the facet substring at line ~363): `{% unless _cv contains 'brant business interiors' %}`. (Card-label behavior not independently real-browser-confirmed either; do not assume.)

### Decision: DEFERRED, non-harmful
The filter system (Brand/Type/Room + the planned **Made-in-Canada filter**, which is gated on the same render fix) **remains DOWN → DEFERRED**. **Zero regression** — the facets never rendered, so nothing got worse; product cards + the Price filter are unaffected. The `buy-canadian` + Quiet Spaces **collections** are unaffected (collection builds, not facets). #88 dealer-name suppression logic is correct + deployed and is a no-op until facets render.

### Brand 50-cap: theoretical/moot regardless
All **108 `base`-suffix collections** are ≤50 products (max 50, median 5, zero exceed 50), so the cap never bites today. Tracked forward-compat only.

### Deploy facts (asset layer only — NOT a render certification)
- Watcher preflight PASS; target `186373570873` confirmed `role=main`.
- PUT → Admin-API readback **byte-for-byte MATCH** (SHA256 `0fff77a4fcf98b15`, 37,409 bytes; **0** `push`, **3** `concat: _one`, card-suppression present). This proves the *bytes* deployed, **not** that anything renders.

### ❌ Corrected false positive (record)
> ~~Fresh-render verification (cart-cookie cache bypass): `l-shape-desks` renders Type=4, Room=2, Brand=5 (… BBI absent), data-filter-group present, 0 BBI card labels. Both fixes confirmed working.~~ — **REFUTED by Leo's real browser. CC's automated render reads (curl / Section-Rendering-API / cart-cookie) were false-positive-prone throughout this episode. LESSON: the only authoritative render check is a real browser; do NOT self-certify renders.**

### Known pre-existing (not this fix)
`l-shape-desks` tag hygiene: both `type:desk` AND `type:desks` (+ `type:tables`, `type:accessories`) — dedup pass later.
