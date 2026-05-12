# Stage 3.1a — Decision Document

**Generated:** 2026-05-07  
**Based on:** `stage-3.1a-t3-spec-extract.md`, `stage-3.1a-tag-census.csv`, `stage-3.1a-hub-gap-analysis.csv`  
**Inputs to:** Stage 3.1b (build pass)

---

## 1. T3 Spec Gaps

**8 gaps total — 2 high, 3 medium, 3 low**

| ID | Gap | Severity | Blocker for 3.1b? |
|---|---|---|---|
| GAP-A | Brand count + warranty headline copy not specified per hub | Medium | No — can default to existing `hero_subtitle` + add generic stat line |
| GAP-B | Sub-cat filter: nav pills vs. tag-filter not disambiguated | **High** | **YES — must decide before filter-bar build** |
| GAP-C | Products-per-page for grid not specified | Low | No — default to 12 |
| GAP-D | Unbuyable detection criteria not specified | Low | No — reuse existing BBI rule |
| GAP-E | Brand plates: which 8 brands per hub not listed | **High** | **YES — blocks brand-section content** |
| GAP-F | Canadian + authorized badge styling (tokens/size) | Medium | No — reference T1 maple-leaf badge |
| GAP-G | Pagination strip page-count not specified | Low | No — Shopify `paginate` handles this natively |
| GAP-H | No shared `bbi-oecm-bar.liquid` snippet exists | Medium | No — create snippet in 3.1b from ds-lp-oecm.liquid content |

**Decisions needed from you before 3.1b starts:**

1. **GAP-B:** Sub-cat filter pills — navigation links (→ sub-collection handles) or tag-based filtering?  
   *Recommendation: navigation links in 3.1b. All `subcategory:*` tags are absent (0% coverage). Pill links reuse the tile block data already in each collection.*.json.*

2. **GAP-E:** Which 8 brands appear in the brand plates section for each hub?  
   *Recommendation: provide a per-hub brand list (8 × 9 = 72 entries). Alternatively, use a fixed canonical 8 from the main brands page for all hubs — simpler but less targeted.*

---

## 2. Filter Rail Verdict: DEFER to 3.1c

**Tag census results (653 products, 2026-05-07):**

| Namespace | Products tagged | Coverage | Distinct values | Verdict |
|---|---|---|---|---|
| `subcategory:` | 0 | **0.0%** | 0 | DEFER |
| `brand:` | 0 | **0.0%** | 0 | DEFER |
| `height:` | 0 | **0.0%** | 0 | DEFER |
| `fabric:` | 0 | **0.0%** | 0 | DEFER |
| `warranty:` | 0 | **0.0%** | 0 | DEFER |

**Verdict: DEFER — all 5 namespaces at 0%. No filter rail in 3.1b.**

The catalog uses a different tag schema: `type:` (87.9% coverage), `industry:` (88.4%), `room:` (46.2%). None of these map directly to the T3 filter namespaces. A tagging pass (Stage 3.1c) must run before the filter rail can ship.

For 3.1b, the sub-category filter section will be built as navigation pills (links to sub-collection handles from tile blocks) — no JS, no tag filtering, degrade-safe. The filter rail markup can be added in 3.1c as a progressive enhancement.

---

## 3. Empty Collection Alert (Pre-existing Risk)

Three hubs have 0 products because their smart collection tag rules reference tags that don't exist:

| Hub | Smart collection rule tags | Tags actually in catalog |
|---|---|---|
| `ergonomic-products` | `type:ergonomic`, `type:monitor-arms`, `type:keyboard-trays`, `type:footrests`, `type:back-supports`, `type:sit-stand-converters`, `type:ergonomic-products` | NONE match |
| `panels-room-dividers` | `type:panels`, `type:dividers`, `type:room-dividers`, `type:panel-systems`, `type:acoustic-panels` | NONE match |
| `quiet-spaces` | `type:acoustic-pods`, `type:phone-booths`, `type:focus-pods`, `type:quiet-spaces`, `type:acoustic-booths` | NONE match |

**Actual `type:` tags in catalog:** `chairs` (184) · `tables` (104) · `desks` (98) · `accessories` (91) · `storage` (82) · `lounge` (10) · `outdoor` (5)

The T3 product grid for these 3 hubs will render empty until products are re-tagged with the correct `type:` values. This is the same tagging pass required for the filter rail. 3.1b should build the product grid component; the tagging pass (3.1c) unblocks all three.

---

## 4. Net Work for 3.1b

### Files to modify

| File | Change type | Notes |
|---|---|---|
| `theme/sections/ds-cc-base.liquid` | Major rework | Add product grid, nav pills, brand plates (8), OECM bar, pagination; modify intro band; remove/convert tile grid |
| `theme/templates/collection.seating.json` | Update | Remove tile blocks → nav pill config; add brand plate data |
| `theme/templates/collection.desks.json` | Update | Same |
| `theme/templates/collection.storage.json` | Update | Same |
| `theme/templates/collection.tables.json` | Update | Same |
| `theme/templates/collection.boardroom.json` | Update | Same |
| `theme/templates/collection.ergonomic-products.json` | Update | Same + note empty state |
| `theme/templates/collection.panels-room-dividers.json` | Update | Same + note empty state |
| `theme/templates/collection.accessories.json` | Update | Same |
| `theme/templates/collection.quiet-spaces.json` | Update | Same + note empty state |

**Total files: 10** (1 section + 9 templates)

### New snippets to create

| Snippet | Purpose | Notes |
|---|---|---|
| `bbi-oecm-bar.liquid` | Shared OECM trust bar | Extract from ds-lp-oecm.liquid; reuse across T1/T2/T3 |

**Total new snippets: 1** (filter rail snippet deferred to 3.1c)

### New inline components (in ds-cc-base.liquid)

| Component | T3 class | Status |
|---|---|---|
| Product grid | `.cn-product-grid` / `.bbi-card--product` | NEW |
| Nav pills (sub-cat) | `.cn-filter-bar` (nav-only variant) | NEW |
| Brand plates (8) | `.cn-brand-section` | NEW — blocked on GAP-E resolution |
| Pagination | `.cn-pagination` | NEW |
| OECM bar hook | (shared snippet render) | NEW |

**Total new inline components: 5** (1 deferred if GAP-E unresolved)

---

## 5. Risks

### Risk 1 — Empty collections derail 3 of 9 hubs (HIGH)
ergonomic-products, panels-room-dividers, and quiet-spaces will render empty product grids until a re-tagging pass fixes their smart collection rules. These pages will look broken in production if 3.1b ships without the tagging fix. **Mitigation:** add a non-empty guard (`{% if collection.products_count > 0 %}`) that falls back to the tile grid for empty collections; or run a 0.5-day tagging sprint before 3.1b ships.

### Risk 2 — Brand plates content gap blocks the brand section (HIGH)
GAP-E (which 8 brands per hub) is unresolved. If not answered before 3.1b, the brand section can't be populated with real data. **Mitigation:** stub with placeholder brand blocks in the schema and populate in a content pass after 3.1b code ships.

### Risk 3 — Tile grid removal breaks non-T3 fallback (MEDIUM)
The current tile grid is the primary navigation aid for users finding sub-collections. Replacing it with a product grid + nav pills changes the UX fundamentally. If the nav pills aren't well-designed or the product grid is slow, conversion could drop. **Mitigation:** A/B test approach — keep tile grid visible until product grid is validated, then swap. For 3.1b, ship both and hide tiles via schema toggle.

### Risk 4 — Pagination + 9 templates = large theme push (LOW)
Changing the `paginate` wrapper requires modifying `ds-cc-base.liquid` in a way that adds a Shopify pagination context. This wraps the entire products output block. Must test that this doesn't break the OECM-gate logic in `theme.liquid`. **Mitigation:** test on dev theme before promoting.

---

## 6. Recommended 3.1b Build Sequence

1. **Resolve GAP-B and GAP-E** (decisions from you) before writing any code
2. Create `bbi-oecm-bar.liquid` snippet (extract from ds-lp-oecm.liquid)
3. Add product grid + pagination to `ds-cc-base.liquid` (wrap in `paginate`)
4. Add nav pills (sub-cat navigation) — reuse tile block data
5. Add brand plates section (after GAP-E resolved)
6. Add OECM bar render call
7. Update intro band (add brand count + warranty headline schema settings)
8. Update all 9 collection.*.json templates
9. Test on dev theme: seating (194 products), desks (98), tables (104)
10. Flag empty-collection guard for ergonomic / panels / quiet-spaces

**Estimated scope:** 1 major section rewrite + 1 new snippet + 9 template updates. Medium complexity. One focused session.
