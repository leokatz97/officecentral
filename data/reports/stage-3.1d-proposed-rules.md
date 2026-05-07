# Stage 3.1d — Proposed Smart-Collection Rules

**Date:** 2026-05-07  
**Catalog size:** 653 products  
**Finding:** The catalog uses only 5 coarse `type:` tags (chairs, tables, desks, accessories, storage). No granular ergonomic/panel/acoustic tags exist. Rules must use `title contains` matching.

---

## ergonomic-products

**Current rules:** `tag equals type:ergonomic` / `type:monitor-arms` / etc. → **0 products**  
**Root cause:** None of these tags exist on any product.

**Proposed rules (disjunctive — any match wins):**

| # | column | relation | condition | Matches |
|---|--------|----------|-----------|---------|
| 1 | title | contains | monitor arm | 9 |
| 2 | title | contains | keyboard tray | 4 |
| 3 | title | contains | sit-stand | 3 |
| 4 | title | contains | anti-fatigue | 1 |

**Total unique products: 16**

**Sample matches:**
- Dual monitor arm
- OTGMA2 dual monitor arm
- Triple monitor arm
- Fellowes lotus dual monitor arm kit
- Jax keyboard tray
- Keyboard tray multi position
- Desktop sit-stand workstation — MVL5230B0
- Sit2stand series sit-stand workstation
- Anti-fatigue wellness mat — 36" x 24"

**Note:** "Electric desk riser + dual monitor arm" is tagged type:desks but its title contains "monitor arm" — included, as it is an ergonomic desk riser accessory. "Keyboard tray multi adjustable" is tagged type:tables (data error) but is clearly a keyboard tray product — included.

**Verdict:** ✅ Above 5-product threshold. Ready to apply pending approval.

---

## panels-room-dividers

**Current rules:** `tag equals type:panels` / `type:dividers` / etc. → **0 products**  
**Root cause:** None of these tags exist on any product.

**Proposed rules (disjunctive — any match wins):**

| # | column | relation | condition | Matches |
|---|--------|----------|-----------|---------|
| 1 | title | contains | partition | 4 |
| 2 | title | contains | room divider | 3 |
| 3 | title | contains | modesty panel | 4 |
| 4 | title | contains | otg panel | 1 |

**Total unique products: 12**

**Sample matches:**
- Partitions 66" high — 66"
- Partitions 66" high 2 offices — 66"
- Partitions 66" high 3 offices — 66"
- Partitions 66" high 6 offices — 66"
- Felt acoustic room dividers
- Screenflex 5 panel mobile light-duty portable room divider
- Screenflex room dividers
- Plexiglass modesty panels
- Laminate modesty panels
- Otg panels

**Optional addition:** Adding `title contains "divider"` would bring in 4 desk-top divider products (total → 16). These are workspace privacy screens rather than freestanding room dividers — included if desired, excluded if hub should stay freestanding-only.

**Verdict:** ✅ Above 5-product threshold. Ready to apply pending approval.

---

## quiet-spaces

**Current rules:** `tag equals type:acoustic-pods` / `type:phone-booths` / etc. → **0 products**  
**Root cause:** None of these tags exist on any product.

**Proposed rules (disjunctive — any match wins):**

| # | column | relation | condition | Matches |
|---|--------|----------|-----------|---------|
| 1 | title | contains | acoustic | 6 |
| 2 | title | contains | sound dampener | 1 |
| 3 | title | contains | phone booth | 1 |
| 4 | title | contains | soft pod | 1 |

**Total unique products: 9**

**All matched products:**
- Ceiling baffles sound acoustic dampeners
- Ceiling grids sound acoustic dampeners (3 variants)
- Felt acoustic room dividers *(also matches panels-room-dividers — product can live in both)*
- Felt acoustic wall tiles
- Felt sound dampeners
- Pod phone booths
- Soft pods

**Note:** True private-space products (pods/booths) number only 2. The remaining 7 are acoustic treatment products (ceiling baffles, panels, wall tiles). These are genuine acoustic/quiet-space category adjacents. The hub is best understood as "Quiet Spaces & Acoustic" with this rule set. Flagging for user decision — see below.

**Verdict:** ✅ 9 products — above threshold. However, only 2 are true "quiet space" enclosures. Applies if user accepts the broader acoustic interpretation. If hub should be pods/booths ONLY → ❌ flag as "needs product-side tagging" (only 2 products, below threshold).

---

## Rule format for Shopify Admin API

All proposed rules use:
- `column`: `"title"`
- `relation`: `"contains"`
- `condition`: the keyword (case-insensitive match in Shopify)
- `disjunctive`: `true` (any rule matches)

---

*Sources: [stage-3.1d-tag-investigation.csv](stage-3.1d-tag-investigation.csv) · [stage-3.1d-current-rules.csv](stage-3.1d-current-rules.csv)*
