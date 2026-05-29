# Tier A Enrichment — Session Handoff (2026-05-27)

**Status:** Phase 0 + Phase 1 complete. Phase 2 (per-product enrichment loop) ready to begin.
**Scope:** `do brand:global` — 5 products from the "Other" collection (id=527013085497) where `current_vendor = "Global Furniture Group"`.
**Goal of this doc:** restart in a fresh Claude Code session and land at "begin Phase 2, product 1" with zero re-litigation of schema, routing, or scope.

---

## 1. The 6 pre-decisions (open — confirm before product 1)

The prior session's grep of `theme/sections/ds-pdp-base.liquid` + the live Boat-Shape PDP's actual metafields corrected three divergences from the prompt's worked example. The new session must confirm these before writing the first YAML:

1. **Title:** keep live casing exactly as-is (no Title Case rewrites, no model suffix added). **Y/N**
2. **Body:** lead paragraph only, no `<h3>` blocks. "Who it's for" goes to `specs.who_its_for` metafield, NOT body HTML. **Y/N**
3. **Metafield namespace:** all writes go to `specs.*` (per live theme). Nothing to `custom.*` — the prompt's worked example used `custom.*` which the theme never reads. **Y/N**
4. **`specs.tagline`:** populate with a bold one-liner per product (the Boat-Shape's is currently blank — adding this for the 5 Global chairs). **Y/N**
5. **`specs.standfirst`:** populate or leave blank? Boat-Shape leaves it blank; the lead paragraph alone reads cleanly without it. **populate / blank**
6. **MSRP:** confirmed dropped (no `custom.msrp_cad`) — list price comes from the variant, not a metafield. **Y/N**

---

## 2. Live theme schema lock (do not deviate)

### 2a. Body-HTML truncation — CRITICAL

The theme does this (`ds-pdp-base.liquid` line 663):

```liquid
{%- assign _desc_intro = product.description | split: '<h3>' | first -%}
<div class="pdp-about__body">{{ _desc_intro }}</div>
```

**Everything from the first `<h3>` onward is stripped before render.** So:

- ✅ Body = 1 lead paragraph + optionally 1 narrative paragraph. No headings, no lists.
- ❌ NO `<h3>Key features</h3><ul>…</ul>` in body — Key Features go in `specs.key_features` (list metafield) and render in the dedicated Specs table below.
- ❌ NO `<h3>Who it's for</h3>` in body — that's the `specs.who_its_for` metafield.
- ❌ NO trailing `<h3>` "Made in Canada / Request a Quote" closer — trust pills, quote CTA, and phone nudge are hardcoded in the theme.

### 2b. Metafield schema (namespace = `specs`)

| PDP section | Key | Type | Notes |
|---|---|---|---|
| H2 above "About" body | `specs.tagline` | single_line_text | Bold one-line hook |
| Lead under buybox price | `specs.standfirst` | single_line_text | Short lede in buybox area. Optional |
| "About this product" body | (`product.description`) | (body HTML) | Lead paragraph only — see §2a |
| "Who it's for" panel | `specs.who_its_for` | single_line_text | One sentence describing buyer personas |
| Specs row: Key Features | `specs.key_features` | **list**.single_line_text | Array of 6–8 plain-English bullets |
| Specs row: Manufacturer | `specs.manufacturer` | single_line_text | e.g. `"Global Furniture Group"` |
| Specs row: Product Line | `specs.product_line` | single_line_text | e.g. `"Concorde"` |
| Specs row: Model | `specs.model_codes` | **list**.single_line_text | e.g. `["2424-MT"]` |
| Specs row: Dimensions | `specs.dimensions` | single_line_text | Free text |
| Specs row: Weight | `specs.weight` | single_line_text | Optional |
| Specs row: Weight Capacity | `specs.weight_capacity` | single_line_text | e.g. `"350 lb"` |
| Specs row: Materials | `specs.materials` | **multi_line**_text | Newlines render as `<br>` |
| Specs row: Finishes Available | `specs.finishes_available` | **list**.single_line_text | Array of finish/colour options |
| Specs row: Certifications | `specs.certifications` | **list**.single_line_text | e.g. `["Exceeds ANSI/BIFMA"]` |
| Specs row: Warranty | `specs.warranty` | single_line_text | e.g. `"Limited Lifetime"` |
| Specs row: Made In | `specs.country_of_manufacture` | single_line_text | e.g. `"Canada (Global)"` |

**Drop from the prompt's worked example (theme doesn't read these — dead writes):**
- `custom.msrp_cad`, `custom.weight_lbs`, `custom.overall_*_in`, `custom.seat_*_in`, `custom.back_height_in`, `custom.weight_capacity_lbs`, `custom.brand`, `custom.series`, `custom.model_number` — all unread.
- Consolidate dimensions into `specs.dimensions` text.

### 2c. Title rule

- Keep `product.title` exactly as-is (live casing). Don't propose Title Case rewrites or model-number suffixes.
- Existing model suffix in `concorde-high-back-executive-multi-tilter-2424` ("— 2424") is preserved by being already in the title.

### 2d. Voice rules (unchanged from CLAUDE.md / icp.md)

- Never publish "BBI" — always "Brant Business Interiors" spelled out.
- Strip ™/® glyphs (the live `global.title_tag` has `Concorde®` — clean it).
- No invented specs — if a dimension isn't in source data, omit the metafield (its row just won't render).
- Canadian English (colour, not color).
- Phone CTA, OECM pill, "Canadian Made" pill are auto-rendered by the theme from tags. Don't duplicate in copy.
- Leave `judgeme.badge` / `judgeme.widget` metafields alone (review widget — not our concern).

---

## 3. Theme + safety baseline

- **LIVE theme:** `186373570873` (role=main, "BBI Landing Dev"). Confirmed via Admin API at 2026-05-27T11:23:29-04:00.
- **No theme writes this session.** Output is YAML files only. Ingest happens later via `~/Downloads/prompt-other-collection-tier-a-ingest.md`.
- **Branch state:** working on `feature/morning-image-swaps-2026-05-27`. The v3 artifacts live on a sibling branch (`feature/other-collection-prep-2026-05-27`, commit `331d1d2`) — restored into the working tree (see §6).

---

## 4. Scope — 5 Global products in priority order

| # | Price | Handle | Title | Recommender misfire? |
|---|---|---|---|---|
| 1 | $2099.99 | `concorde-high-back-executive-multi-tilter-2424` | Concorde high back executive multi-tilter — 2424 | ⚠ medium-back-seating, monitor-arms |
| 2 | $1920.76 | `concorde-high-back-24hr-executive-synchro-tilter-2424` | Concorde high back 24HR executive synchro-tilter (2424) — 2424 | check before use |
| 3 | $869.99 | `ergo-boss-multi-tilter-chair-2` | Ergo boss multi-tilter chair | check |
| 4 | $659.99 | `the-accord-tilter-high-back-chair-1` | The accord tilter high back chair | check |
| 5 | $549.99 | `ibex-mesh-seat-back-drafting-chair-stool-1` | Ibex \| mesh seat & back drafting chair stool | likely needs `stools-drafting-chairs` |

All 5 are >$500 → suggest `https://www.globalfurnituregroup.com/` URLs in research cards by default.

### 4a. Routing corrections per product type

The CSV recommender produces some misfires for chairs. **Replacement defaults:**

| Product | Correct sub-collections (all routable=Y) | Add method |
|---|---|---|
| High-back executive chairs (Concorde 2424, Accord) | `task-chairs` + `gfg-chairs` + `highback-seating` | tag-write `task-chair`; tag-write-multi `brand:global-furniture-group`+`type:chairs`; collects-post for highback |
| 24/7 executive (Concorde 24HR) | + add `24-hour-seating` (collects-post) — the `-24hr-` variant is rated for 24/7 duty cycle |
| Ergonomic task (Ergo Boss) | `task-chairs` + `gfg-chairs` + possibly `mesh-seating` if mesh-back |
| Drafting stool (Ibex) | `stools-drafting-chairs` (collects-post) + `gfg-chairs` + `stools-seating` (collects-post). **Don't** use `task-chairs` — drafting stools aren't task chairs |

**Never use for chairs:**
- `medium-back-seating` — only for medium-back products
- `monitor-arms` — desk accessory, not a chair
- `executive-seating` — `routable=N` in v3 picklist (empty collection)

---

## 5. Tag-write recipes (from v3 picklist)

Each recommended sub-collection has a recipe in `data/reports/_recipe-map-20260527-113938.json`. For chairs, the relevant ones:

| Sub-collection | add_method | Tag(s) to write |
|---|---|---|
| `task-chairs` | tag-write | `task-chair` |
| `gfg-chairs` | tag-write-multi | `brand:global-furniture-group`, `type:chairs` |
| `seating` | tag-write | `type:chairs` |
| `boardroom` | tag-write | `room:boardroom` |
| `ergocentric` | tag-write | `brand:ergocentric` |
| `highback-seating` | collects-post | *(no tag — custom collection)* |
| `24-hour-seating` | collects-post | *(no tag)* |
| `stools-drafting-chairs` | collects-post | *(no tag)* |
| `mesh-seating` | collects-post | *(no tag)* |

Enrichment tags (additive, per product): `line:<line>`, `model:<model>`, `made-in-canada` (if confirmed), `chair-type:<synchro-tilter|multi-tilter|drafting-stool>`, `back-height:<high|medium|low>`, plus existing `oecm-eligible` preserved.

---

## 6. Restore command (if v3 artifacts go missing again)

The v3 source artifacts live on sibling branch `feature/other-collection-prep-2026-05-27`, commit `331d1d2`. They are NOT committed on the current branch. If the working tree gets cleaned, restore via:

```bash
cd "/Users/leokatz/Desktop/Office Central"
for f in \
  "data/reports/other-collection-products-20260527-093211-with-recs.csv" \
  "data/reports/other-collection-picklists-20260527-093211.csv" \
  "data/reports/canonical-decisions-20260527-093211.csv" \
  "data/reports/other-collection-README-20260527-093211.md"; do
  git show "331d1d2:$f" > "$f"
done
```

Phase 1 outputs (triage CSV + recipe map cache) live only in the working tree — not committed:

- `data/reports/tier-a-triage-20260527-113938.csv`
- `data/reports/_recipe-map-20260527-113938.json`
- `data/reports/_triage-results-20260527-113938.json`

If these disappear, rerun Phase 1 logic from the prior session's script (paste into the new session if needed).

---

## 7. Triage results summary (already computed — don't rebuild)

```
TIER COUNTS (per ENRICHMENT_ROI formula in prompt):
  A-PRIORITY  :   8
  B-WORTH-IT  : 190
  C-MAYBE     : 119
  D-SKIP      :  21

PREMIUM-BRAND VENDOR COUNTS:
  Teknion                  : 11
  Global Furniture Group   :  5  ← this session's scope
  Humanscale               :  2

DETECTED BRAND-LINE NAMES:
  Concorde: 2 | Loover: 2 | Factor: 2 | Wave: 1 | Altona: 1 | Ibex: 1 | Supra: 1

Tier A already enriched (skipping): 0
Tier A pending in catalog:           338
```

Note: only **5 products** have `vendor = Global Furniture Group`. The other 313 catch-all "Brant Business Interiors" vendor entries may include mis-vendor-tagged Global products, but `do brand:global` per the prompt scopes to the 5 explicit rows only.

---

## 8. "tier-b only" minimal record (under corrected schema)

If Leo types `tier-b only` (or default-fallback when no competitor data found), produce this YAML:

```yaml
product_id: <id>
handle:     <handle>
storefront_url: <url>

# Identity unchanged — no title, no body, no metafields
vendor_current:  "<current>"
vendor_proposed: "Global Furniture Group"   # if confirmable

# Sub-collection adds (from routing corrections in §4a, NOT CSV recommender)
sub_collections_add:
  - task-chairs           # or stools-drafting-chairs for Ibex
  - gfg-chairs
  - highback-seating      # or 24-hour-seating, etc.

# Smart-routing recipes (from §5)
smart_tag_writes:
  task-chairs: "task-chair"
  gfg-chairs: ["brand:global-furniture-group", "type:chairs"]
  # highback-seating: (custom — no tag needed)

# Tags — additive, brand + routing only
tags_current: [...existing...]
tags_to_add:
  - "task-chair"
  - "brand:global-furniture-group"
  - "type:chairs"
  - "brand:global"
  # NO line/model tags in tier-b — those require confirmed research

status: tier_b_minimal
finalized_at: <iso>
finalized_by: leo
```

---

## 9. What the new session starts with

1. Read this handoff doc first.
2. Read the prompt file at `~/Downloads/prompt-other-collection-tier-a-enrichment.md` for full context.
3. Skip Phase 0 preflight rebuild — files are on disk (verify with `ls`).
4. Skip Phase 1 triage rebuild — already done; surface the stats from §7.
5. Ask Leo the 6 pre-decisions in §1 (or accept "all defaults Y, standfirst=blank" if he says "all defaults").
6. Begin Phase 2 with product 1 (Concorde 2424 multi-tilter).

---

## 10. Files of record

| File | Purpose |
|---|---|
| `~/Downloads/prompt-other-collection-tier-a-enrichment.md` | Master prompt (full Phase 0/1/2/3 spec) |
| `~/Downloads/prompt-other-collection-tier-a-ingest.md` | YAML → Shopify ingest (later session) |
| `~/Downloads/prompt-other-collection-tier-b-routing.md` | Steve-CSV companion routing |
| `data/reports/other-collection-products-20260527-093211-with-recs.csv` | 338 products with recommender output |
| `data/reports/other-collection-picklists-20260527-093211.csv` | 235 rows (166 routable) |
| `data/reports/canonical-decisions-20260527-093211.csv` | 16 duplicate-title cluster resolutions |
| `data/reports/other-collection-README-20260527-093211.md` | Steve's README |
| `data/reports/tier-a-triage-20260527-113938.csv` | Phase 1 output, 338 scored + bucketed |
| `data/reports/_recipe-map-20260527-113938.json` | Parsed picklist recipes (tag-write / tag-write-multi / collects-post) |
| `data/reports/_triage-results-20260527-113938.json` | Phase 1 raw results (incl. reason strings) |
| `theme/sections/ds-pdp-base.liquid` | Live PDP template — schema lock source |
| `theme/snippets/bbi-product-jsonld.liquid` | JSON-LD reads same `specs.*` metafields |
| `data/reports/enrichment/` | YAML output dir (empty — 0 / 338 enriched) |
| `data/logs/` | Audit JSONL output dir |
