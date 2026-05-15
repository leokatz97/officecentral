# Path Z — Inventory Audit
_2026-05-15 · Read-only confirmation of BBI inventory in 5 gap-areas surfaced by CATALOG-NAV-INVESTIGATION (commit 8e0de9a, Step 42)._

**Scope:** 593 active products, `/collections/other` exclusion = 0 handles (none found).  
**Method:** Title + full `body_html` description search, lowercase pattern matching per concept.

---

## Summary table

| Area | Concept | Raw count | Adjusted count | Decision |
|------|---------|-----------|----------------|----------|
| Quiet Spaces | Phone Booths | 1 | 1 | **REMOVE** |
| Quiet Spaces | Acoustic Meeting Pods | 0 | 0 | **REMOVE** |
| Quiet Spaces | Soundproofing | 7 | 5 ★ | **BUILD** |
| Quiet Spaces | High-Back Privacy Seating | 0 | 0 | **REMOVE** |
| Ergonomic | Desk Converters | 5 | 5 | **BUILD** |
| Ergonomic | Monitor Arms | 20 | 20 | **BUILD** |
| Ergonomic | Keyboard Trays | 13 | 13 | **BUILD** |
| Ergonomic | Ergonomic Accessories | 95 | ~15 ☆ | **BUILD** |
| Boardroom | AV & Presentation | 7 | 6 ★★ | **BUILD** |
| Accessories | Waste & Recycling | 0 | 0 | **REMOVE** |
| Accessories | Whiteboards & Pinboards | 3 | 3 | **BUILD-thin** |

**★** 2 of 7 Soundproofing matches are Screenflex room dividers that mention "sound absorbing" as a secondary feature — they are room dividers, not dedicated soundproofing panels. Genuine dedicated soundproofing products = 5.

**☆** Raw count of 95 is inflated because most products have no `product_type` tag, so the chair-exclusion filter couldn't fire. The genuine non-chair ergonomic accessories are already captured in the three preceding rows (monitor arms 20, keyboard trays 13, desk converters 5). Additional distinct accessories beyond those three categories (footrests, lumbar mounts, wrist rests) = approximately 10–15 products. BUILD the tile but scope collection logic to exclude chairs.

**★★** Zira Conference Table matched via "lectern" and "media cart" appearing in its description copy — it is a conference table, not AV furniture. Genuine AV/presentation products = 6.

---

## Page-level recommendations

| Page / Tile | Recommendation |
|---|---|
| **Quiet Spaces page** | **REMOVE entirely** — only 1 concept (Soundproofing) has 3+ products; does not meet the 2-concept threshold. Move Soundproofing tile to Accessories. Add Quiet Spaces to `docs/plan/ideas-backlog.md` for when BBI carries phone booths / acoustic pods. |
| **Ergonomic Products page** | **KEEP** — all 4 concepts have 5+ products. Build all 4 tiles. |
| **Boardroom AV tile** | **ADD** — 6 genuine products (1 AV stand + 5 lectern/podium variants). Thin but real. |
| **Accessories: Whiteboards & Pinboards** | **ADD (BUILD-thin)** — 3 products: 1 dedicated whiteboard + 2 Screenflex dividers with tack-board surfaces. |
| **Accessories: Waste & Recycling** | **SKIP** — 0 products. BBI does not carry Rubbermaid or equivalent. Add to ideas backlog. |

---

## Cross-tag: feature:ergonomic candidates

Total products that would carry `feature:ergonomic`: **~85**

Breakdown (approximate — exact count requires `product_type` remediation from TYPE-APPLY-1):

| Segment | Count | Notes |
|---|---|---|
| `type:desks` + `feature:ergonomic` | ~17 | Sit-stand / height-adjustable desks |
| `type:chairs` + `feature:ergonomic` | ~30 | ObusForme series + Global / Teknion ergonomic chairs with lumbar support |
| `type:accessories` + `feature:ergonomic` | ~38 | Monitor arms (20) + keyboard trays (13) + desk converters (5) + stools/footrests (~5) |

> **Note:** The chair count is soft because product_type is unpopulated for most products today. After TYPE-APPLY-1 assigns `type:chairs`, a precise ergo-chair count will be possible. ObusForme is the canonical ergonomic chair brand BBI carries.

**Namespace recommendation:** Use `feature:ergonomic` (not `type:ergonomic`) — "feature" namespace signals a cross-cutting attribute, consistent with CATALOG-NAV-INVESTIGATION taxonomy design. Confirm with Steve before tagging.

---

## Detailed per-area findings

---

### Area 1 — Quiet Spaces

**Phone Booths (1 product → REMOVE)**

| Handle | Title | Notes |
|---|---|---|
| `pod-phone-booths` | Pod phone booths | "POD (Privacy On Demand)" — 1 product family, listed as-is |

Only one product exists. The description is brief and positions it as occasional short-duration privacy from open plan. No depth of inventory to warrant a collection.

**Acoustic Meeting Pods (0 products → REMOVE)**

No products matching "acoustic pod", "meeting pod", "office pod", "focus pod", "soundproof room", or "quiet room". BBI does not currently carry enclosed acoustic pods (e.g., Framery, Hushoffice, etc.).

**Soundproofing (5 genuine products → BUILD)**

| Handle | Title | Match signal |
|---|---|---|
| `ceiling-baffles-sound-acoustic-dampeners` | Ceiling baffles sound acoustic dampeners | "acoustic baffle" |
| `ceiling-grids-sound-acoustic-dampeners-1` | Ceiling grids sound acoustic dampeners | "sound dampening" |
| `ceiling-grids-sound-acoustic-dampeners-copy` | Ceiling grids sound acoustic dampeners (variant) | "sound dampening" |
| `hardware-for-ceiling-tiles` | Hardware for ceiling tiles | "acoustic ceiling" |
| `privacy-desk-top-dividers` | Privacy desk top dividers | "sound absorbing" (PET felt panels) |

_Also matched but excluded from tile scope:_ Screenflex room dividers (2) — they mention "sound absorbing" as a secondary characteristic but are room dividers, not acoustic panels. These belong in a Dividers/Space Division collection, not Soundproofing.

Despite being a thin collection, soundproofing product lines (ceiling baffles, felt panels, hardware) are a coherent category BBI genuinely carries. **BUILD the collection.** Consider "Acoustic Solutions" as the tile label.

**High-Back Privacy Seating (0 products → REMOVE)**

No products with "high-back privacy", "privacy chair", "focus chair", or "privacy pod chair". (Note: BBI carries many high-back chairs, but none are specifically positioned as *privacy* seating.)

**Quiet Spaces page-level verdict: REMOVE**

Only 1 of 4 concepts (Soundproofing) has 3+ products. Per the BUILD criteria (2+ concepts with 3+ products each), the Quiet Spaces category page should not be built. Action items:
- Move Soundproofing to `Accessories` nav as "Acoustic Solutions"
- Add to `docs/plan/ideas-backlog.md`: "Quiet Spaces / Acoustic Privacy category — build when BBI carries phone booths (POD, Hushoffice, Framery) and acoustic meeting pods"

---

### Area 2 — Ergonomic Products

**Desk Converters (5 products → BUILD)**

| Handle | Title |
|---|---|
| `electric-desk-riser-dual-monitor-arm` | Electric desk riser + dual monitor arm |
| `electric-dual-monitor-height-adjustable-standing-desk-workstation-dc450` | Electric dual monitor height adjustable standing desk workstation — DC450 |
| `electric-height-adjustable-standing-desk-workstation-4` | Electric height adjustable standing desk workstation |
| `gas-lift-monitor-riser` | Gas lift monitor riser |
| `sit-stand-adjustable-desk-riser-32-wide` | Sit stand adjustable desk riser 32" wide |

All 5 are genuine sit-stand risers that sit ON a desk (not full height-adjustable desks). Clean category. BUILD.

**Monitor Arms (20 products → BUILD)**

Strong inventory. Top 5 examples:

| Handle | Title |
|---|---|
| `new-pneumatic-single-arm-monitor-stand` | Pneumatic single-arm monitor stand |
| `dual-monitor-arm` | Dual monitor arm (Fellowes Platinum) |
| `electric-desk-riser-dual-monitor-arm` | Electric desk riser + dual monitor arm |
| `monitor-arm-single-13-34-black` | Monitor arm single 13-34" black |
| `single-monitor-arm` | Single monitor arm |

Note: 3 of 20 are desk risers that bundle a monitor arm — they will also appear in Desk Converters. Overlap is intentional (same product, different navigation entry points).

**Keyboard Trays (13 products → BUILD)**

Strong inventory. Top 5 examples:

| Handle | Title |
|---|---|
| `easy-pull-in-out-keyboard-tray` | Easy pull in & out keyboard tray |
| `jax-keyboard-tray` | Jax keyboard tray |
| `keyboard-platform-with-wrist-rest` | Keyboard platform with wrist rest |
| `under-desk-keyboard-tray` | Under-desk keyboard tray |
| `adjustable-keyboard-tray` | Adjustable keyboard tray |

**Ergonomic Accessories — catch-all (BUILD, scoped carefully)**

Raw count: 95 — inflated by chairs (no `product_type` set on most products, so chair-exclusion filter did not fire). 

Genuine non-chair ergonomic accessories beyond the 3 preceding categories:
- Footrest-equipped stools and drafting chairs (Beta, Danio, Ibex mesh drafting, Sonic counter stool, Yoho drafting) — ~5–7 items
- Wrist rests bundled with keyboard platforms — ~3 items
- Anti-fatigue mats — 0 dedicated products found

**Real distinct ergo-accessory-only products ≈ 10–15.** Thin but real. BUILD the tile; exclude chairs from the collection via type filtering once TYPE-APPLY-1 is complete.

**Ergonomic Products page-level verdict: KEEP — BUILD all 4 tiles**

All 4 concepts have 5+ products. Full BUILD:
1. Desk Converters (5)
2. Monitor Arms (20)
3. Keyboard Trays (13)
4. Ergonomic Accessories (10–15 non-chair; tile launches thin, grows with TYPE-APPLY-1 cleanup)

---

### Area 3 — Boardroom AV & Presentation

**AV & Presentation Furniture (6 genuine products → BUILD)**

| Handle | Title | Type |
|---|---|---|
| `av-stand-sa-81-3016` | AV stand — SA-81-3016 | AV cart / equipment stand |
| `impromptu-lectern-1` | Impromptu lectern | Podium / lectern |
| `lectern-podium` | Lectern podium | Podium (mobile, coloured finish) |
| `lectern-storage-stand` | Lectern storage stand | Lectern with storage |
| `scoot-8945bl-lectern` | Scoot 8945BL lectern | Presentation cart / lectern |
| `scoot-multi-purpose-lectern-8922bl-1` | Scoot multi-purpose lectern — 8922BL | Multi-purpose podium |

_False positive:_ Zira conference table matched "lectern" and "media cart" appearing in its body text — it is a boardroom table, not AV furniture.

BBI's AV & Presentation offering is lectern-heavy (5 lectern/podium variants + 1 AV stand). Thin but coherent. BUILD the tile under Boardroom. Consider label "Podiums & AV Furniture" to reflect the actual mix.

---

### Area 4 — Accessories: Waste & Recycling

**Waste & Recycling (0 products → REMOVE)**

Zero products matched: "waste", "recycling", "garbage", "trash receptacle", "rubbermaid", or vendor = Rubbermaid. BBI does not currently carry any waste and recycling products.

Do not build tile. Add to ideas backlog: "Waste & Recycling — add if BBI brings on Rubbermaid, Safco, or equivalent janitorial line."

---

### Area 5 — Accessories: Whiteboards & Pinboards

**Whiteboards & Pinboards (3 products → BUILD-thin)**

| Handle | Title | Type | Match signal |
|---|---|---|---|
| `white-board-magnetic-mobile-on-wheels` | White board magnetic (mobile) on wheels | Dedicated whiteboard | "whiteboard", "white board" |
| `screenflex-room-dividers` | Screenflex room dividers | Room divider with tack-board surface | "bulletin board" |
| `screenflex-5-panel-mobile-light-duty-portable-room-divider-65h-x-95w-fabric-color-stone` | Screenflex 5-panel room divider | Room divider with tack-board surface | "bulletin board" |

Only 1 dedicated whiteboard product. The 2 Screenflex products are room dividers that have a bulletin-board-pinnable felt side — they legitimately belong in a Whiteboards & Pinboards tile but are not pure whiteboard products.

Decision: **BUILD-thin.** A 3-product tile is weak but real — BBI carries at least 1 standalone whiteboard. The Screenflex dividers add genuine value to someone configuring a meeting room. Tile can deepen as BBI adds more writing-surface products.

---

## Decisions for Steve

1. **Quiet Spaces page** — REMOVE from navigation per inventory findings. The single genuine inventory line (Soundproofing / acoustic ceiling products) should surface under Accessories as "Acoustic Solutions." Confirm.

2. **Ergonomic Products page** — KEEP, BUILD all 4 tiles. Desk Converters, Monitor Arms, Keyboard Trays, and Ergonomic Accessories all have real inventory. Ergo Accessories tile needs TYPE-APPLY-1 to run first so chairs are excluded from the collection. Confirm page stays in nav.

3. **Boardroom AV tile** — ADD under Boardroom as "Podiums & AV Furniture." 6 products (lecterns + 1 AV stand). Thin but genuine. Confirm.

4. **Accessories: Whiteboards & Pinboards** — ADD as BUILD-thin (3 products). Confirm.

5. **Accessories: Waste & Recycling** — SKIP. BBI carries zero waste/recycling products today. Confirm skip.

6. **`feature:ergonomic` namespace** — Recommend adding to ~85 products across sit-stand desks (~17), ergonomic chairs (~30), and desk accessories (monitor arms, keyboard trays, converters, footrests). Confirm namespace (`feature:ergonomic` vs `type:ergonomic`). Timing: after TYPE-APPLY-1 so chair count is clean.

---

## Surprises

1. **BBI has zero waste/recycling products** — Completely absent. Given the B2B institutional buyer base (schools, hospitals, municipalities), this is a meaningful gap. Janitorial/facility management buyers would expect at least Rubbermaid waste receptacles.

2. **Acoustic / soundproofing is stronger than expected** — 5 dedicated products (ceiling baffles, acoustic ceiling grids, hardware) is a real category. BBI is positioned for open-plan noise management even though "Quiet Spaces" as a page-level concept can't be built yet.

3. **Lecterns / podiums: BBI carries 5 variants** — More than expected for a furniture dealer. This is a genuine differentiator for BBI's education and government segments (school boards, municipal councils). Not currently surfaced anywhere in navigation — the Boardroom AV tile would be the first time these products are discoverable by category.
