# BRAND-CALLOUT-AUDIT (Sub-step D)

_2026-05-13. Read-only Phase 1. Input for Steve review before Phase 2 applies changes._

---

## Summary

- **Phase 2 templates audited:** 10 (collection.business-furniture + 9 category pages)
- **Templates with `brand_callout` blocks:** 6 (business-furniture, seating, desks, boardroom, ergonomic-products, panels-room-dividers)
- **Templates with brand plates only (no callouts):** 4 (storage, tables, accessories, quiet-spaces)
- **Recommended changes:** 2 NO-CHANGE · 1 REMOVE-ONLY · 2 REPLACE · 1 ADD · 4 REVIEW-WITH-STEVE
- **Cross-cutting finding:** All 8 pages with brand plate bands show ergoCentric + Keilhauer alongside Global Furniture + Teknion — see Brand Plates section.

### Storefront-callable brands (from canonical map)

| Brand | Enriched products | Callable |
|---|---|---|
| OTG / Offices to Go | ~54 | ✅ Yes |
| Global Furniture Group | ~53 | ✅ Yes |
| Heartwood Manufacturing Ltd. | ~22 (incl. Innovations desks) | ✅ Yes |
| ObusForme | ~5 | ✅ Yes (ICP-relevant) |
| Keilhauer | 0 | ❌ No |
| ergoCentric | 1 | ❌ No |

### Active brand collections (checked 2026-05-13 via API)

| Collection | Products | Status |
|---|---|---|
| `/collections/global-teknion` | 72 | ✅ Active (GFG ∪ Teknion disjunctive, post-COLLECTION-CLEANUP-APPLY) |
| `/collections/keilhauer` | 0 | ⚠️ Active but empty smart collection |
| `/collections/ergocentric` | 1 | ⚠️ Active but near-empty smart collection |
| `/collections/otg-offices-to-go` | — | ❌ Does not exist |
| `/collections/heartwood-manufacturing-ltd` | — | ❌ Does not exist |
| `/collections/obusform*` | — | ❌ Does not exist |

**Critical constraint:** OTG, Heartwood, and ObusForme have no brand smart collections yet.
Any callout pointing to these brands requires creating those collections in Phase 2 first.
The only usable callable-brand collection URL today is `/collections/global-teknion`.

---

## Per-template findings

---

### 1. `collection.business-furniture.json`

**Role:** Top-level vertical hub. Links down to all 9 category pages.

**Current brand callouts (3 `brand_callout` blocks):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-keilhauer` | Keilhauer | `/collections/keilhauer` | 0 | ❌ |
| `brand-global-teknion` | Global / Teknion | `/collections/global-teknion` | 72 | ✅ |
| `brand-ergocentric` | ergoCentric | `/collections/ergocentric` | 1 | ❌ |

**Brand plates:** None on this template.

**Recommendation: REPLACE**

Rationale: Business Furniture is the highest-traffic brand touchpoint — the entry to the full vertical. It should only promote brands with real product depth. Keilhauer (0 products) and ergoCentric (1 product) will send buyers to near-empty dead ends.

**Specific edit:**
- Remove: `brand-keilhauer` block + entry from `block_order`
- Remove: `brand-ergocentric` block + entry from `block_order`
- Keep: `brand-global-teknion` (valid, 72 products)
- Add (Phase 2 prereq): If OTG smart collection is created, add an OTG/Offices to Go callout. If Heartwood smart collection is created, add a Heartwood callout. GFG alone is acceptable if collections aren't ready.

---

### 2. `collection.seating.json`

**Role:** Phase 2 seating category page. Largest tile grid (16 sub-type tiles).

**Current brand callouts (2 `brand_callout` blocks):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-keilhauer` | Keilhauer | `/collections/keilhauer` | 0 | ❌ |
| `brand-ergocentric` | ergoCentric | `/collections/ergocentric` | 1 | ❌ |

**Also has brand tiles in the tile grid (type `tile`, not `brand_callout`):**

| Block key | Title | Link | Products |
|---|---|---|---|
| `tile-ergocentric-chairs` | ergoCentric Task Chairs | `/collections/ergocentric` | 1 |
| `tile-keilhauer-seating` | Keilhauer Seating | `/collections/keilhauer` | 0 |

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: REPLACE**

Rationale: Both `brand_callout` blocks point to non-callable brands. Additionally, the two brand tiles in the sub-category grid create dead-end navigation (buyers click "Keilhauer Seating" and see 0 products; "ergoCentric Task Chairs" sees 1). These must be removed. Seating is OTG's strongest category (~54 OTG seating products); OTG should be the featured callout once a collection is created.

**Specific edit:**
- Remove: `brand-keilhauer` callout + `block_order` entry
- Remove: `brand-ergocentric` callout + `block_order` entry
- Remove: `tile-ergocentric-chairs` tile + `block_order` entry
- Remove: `tile-keilhauer-seating` tile + `block_order` entry
- Add (Phase 2 prereq): OTG callout once `/collections/otg-offices-to-go` or equivalent is created
- Add (Phase 2 prereq): Global Furniture Group callout (can use `/collections/global-teknion` immediately)

---

### 3. `collection.desks.json`

**Role:** Phase 2 desks category page. 8 sub-type tiles.

**Current brand callouts (1 `brand_callout` block):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-global-teknion` | Global / Teknion | `/collections/global-teknion` | 72 | ✅ (GFG callable; Teknion 0 enriched) |

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: REVIEW-WITH-STEVE**

Rationale: The GFG callout is valid — the collection link works (72 products) and GFG is callable. However, the callout names both "Global" and "Teknion" in its copy ("Two of Canada's largest commercial furniture manufacturers"), and Teknion has 0 enriched products. Additionally, Heartwood's Innovations desking line is BBI's strongest Canadian-manufactured desk story, but Heartwood has no brand collection yet.

**Questions for Steve:**
1. Keep the "Global / Teknion" callout as-is (collection is valid, brand story is established)? Or rename the copy to focus on Global Furniture Group only?
2. Create a Heartwood smart collection and add a second callout for Heartwood desks (Innovations line)? Or leave at one callout?

**Specific edit (if Steve confirms revise copy):**
- Update `brand_name` in `brand-global-teknion` from "Global / Teknion" to "Global Furniture Group"
- Update `body` copy to focus on GFG only (remove Teknion name)
- Add second Heartwood callout once collection is created (optional)

---

### 4. `collection.storage.json`

**Role:** Phase 2 storage category page. 12 sub-type tiles.

**Current brand callouts:** None.

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: ADD**

Rationale: Storage is a strong GFG category (Global Fileworks is GFG's dedicated filing/storage division, included in the global-teknion collection). A GFG callout can be added immediately using `/collections/global-teknion`. Storage is also relevant for Heartwood (credenzas, storage units in the Innovations casework line), but that requires a Heartwood collection first.

**Specific edit:**
- Add `brand-global-furniture` block:
  ```json
  {
    "type": "brand_callout",
    "settings": {
      "brand_name": "Global Furniture Group",
      "body": "Canada's largest commercial furniture manufacturer — Global's filing cabinets, storage cabinets, and high-density solutions are used in institutional environments across Ontario.",
      "link": "/collections/global-teknion",
      "link_label": "Shop Global Furniture Group"
    }
  }
  ```
- Append to `block_order` before brand plates

---

### 5. `collection.tables.json`

**Role:** Phase 2 tables category page. 5 sub-type tiles.

**Current brand callouts:** None.

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: REVIEW-WITH-STEVE**

Rationale: Tables (conference, training, collaborative) are a GFG/OTG category. The page has only 5 tile sub-categories, so adding a callout would change the page's weight. The brand plates already surface GFG. A GFG callout is defensible but not urgent.

**Question for Steve:**
1. Add a Global Furniture Group callout (using `/collections/global-teknion`)? Or leave clean with brand plates only?

---

### 6. `collection.boardroom.json`

**Role:** Phase 2 boardroom category page. 3 sub-type tiles.

**Current brand callouts (1 `brand_callout` block):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-keilhauer` | Keilhauer | `/collections/keilhauer` | 0 | ❌ |

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: REPLACE**

Rationale: Keilhauer is the aspirational boardroom brand story — but with 0 products, the callout is a dead end. Boardroom furniture (tables + executive seating) is available from GFG via the global-teknion collection.

**Specific edit:**
- Remove: `brand-keilhauer` block + `block_order` entry
- Add `brand-global-furniture` callout:
  ```json
  {
    "type": "brand_callout",
    "settings": {
      "brand_name": "Global Furniture Group",
      "body": "Canada's most-installed commercial furniture brand — Global's boardroom tables and executive seating are in conference rooms across Ontario's government offices and corporate campuses.",
      "link": "/collections/global-teknion",
      "link_label": "Shop Global Furniture Group"
    }
  }
  ```
- _Note:_ If Keilhauer's product depth grows post-PE Pass 3, Keilhauer can be re-added. The change is reversible.

---

### 7. `collection.ergonomic-products.json`

**Role:** Phase 2 ergonomics category page. 4 sub-type tiles (sit-stand converters, monitor arms, keyboard trays, ergonomic accessories).

**Current brand callouts (1 `brand_callout` block):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-ergocentric` | ergoCentric | `/collections/ergocentric` | 1 | ❌ |

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: REVIEW-WITH-STEVE**

Rationale: ergoCentric (1 product) is not callable. The page covers ergonomic accessories and converters — a category where ObusForme (5 products, ICP-referenced) has some fit (lumbar, back support products). However, ObusForme is primarily a seating-adjacent brand, not a sit-stand/monitor-arm brand; the fit is imperfect. GFG has minimal ergonomic accessories depth.

**Questions for Steve:**
1. Remove ergoCentric callout entirely (REMOVE-ONLY), leaving 4 tiles + brand plates only?
2. Replace with ObusForme callout (needs new collection, borderline category fit)?
3. Leave ergoCentric callout in place as an aspirational/brand-recognition play, knowing the collection is near-empty today?

**If REMOVE-ONLY:**
- Remove: `brand-ergocentric` block + `block_order` entry
- No replacement needed

---

### 8. `collection.panels-room-dividers.json`

**Role:** Phase 2 panels & dividers category page. 3 sub-type tiles.

**Current brand callouts (1 `brand_callout` block):**

| Block key | Brand | Link | Products | Callable |
|---|---|---|---|---|
| `brand-global-teknion` | Global / Teknion | `/collections/global-teknion` | 72 | ✅ (GFG callable; Teknion 0 enriched) |

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Current callout copy:** "Canada's leading panel and systems furniture manufacturers — Teknion's panel systems and Global's divider solutions are proven in government offices and institutional environments province-wide."

**Recommendation: REVIEW-WITH-STEVE**

Rationale: The collection link is valid (72 products). But the copy specifically credits "Teknion's panel systems" — Teknion has 0 enriched products and is historically associated with panel systems furniture, but BBI has not yet verified Teknion panel inventory. The copy creates an expectation the collection may not fulfill. GFG is callable and does have panels/dividers products.

**Question for Steve:**
1. Keep callout as-is (collection is valid, copy is a brand story, Teknion's role in panels is real)?
2. Revise copy to focus on GFG only (remove Teknion name), keeping the same collection link?
3. Wait until Teknion product depth is confirmed before keeping Teknion in the copy?

---

### 9. `collection.accessories.json`

**Role:** Phase 2 accessories category page. 2 sub-type tiles (lighting, whiteboards).

**Current brand callouts:** None.

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: NO-CHANGE**

Rationale: Accessories is a thin category (2 tiles). No callable brand has specific accessories depth justifying a callout. Brand plates already provide brand discoverability. Leave clean.

---

### 10. `collection.quiet-spaces.json`

**Role:** Phase 2 quiet spaces category page. 5 sub-type tiles.

**Current brand callouts:** None.

**Brand plates:** ergoCentric · Keilhauer · Global Furniture · Teknion

**Recommendation: NO-CHANGE**

Rationale: Acoustic pods and phone booths are specialty items. No callable brand (GFG, OTG, Heartwood, ObusForme) has meaningful quiet-spaces product depth. Brand plates provide brand context. Leave clean.

---

## Brand Plates — Cross-cutting finding

8 of 9 Phase 2 category pages (all except business-furniture) have a `brand_plate` band showing four brands: **ergoCentric · Keilhauer · Global Furniture · Teknion**. Brand plates link to `/pages/brands#brand-name` (brand hub pages), not to shop collections.

**Issue:** Keilhauer (0 products) and ergoCentric (1 product) appear prominently in the brand plates band on every category page. While they have published brand hub pages, a buyer clicking the plate to learn more about these brands will find they carry near-zero product depth.

**Brand plate links are to brand pages (not shop collections) — so this is less urgent than callout links.** Brand pages exist and are published. However, the band signals "these are our brands" to every category visitor, regardless of product depth.

**REVIEW-WITH-STEVE:**
- Keep Keilhauer + ergoCentric in the brand plates band across all pages as brand-identity anchors (acceptable because they link to pages, not dead collections)?
- Or swap them for OTG + Heartwood (the actual high-depth callable brands)?
- Note: OTG and Heartwood currently have no brand hub pages (only `/pages/brands-keilhauer`, `/pages/brands-global-teknion`, `/pages/brands-ergocentric` exist). Swapping brand plates would require creating OTG + Heartwood brand pages first.

---

## Recommended Phase 2 (apply) scope

The following are clear no-debate changes ready to apply on Steve's approval:

**1. collection.business-furniture — Remove 2 dead callouts**
- Remove `brand-keilhauer` block
- Remove `brand-ergocentric` block

**2. collection.seating — Remove 2 dead callouts + 2 dead brand tiles**
- Remove `brand-keilhauer` block
- Remove `brand-ergocentric` block
- Remove `tile-ergocentric-chairs` tile
- Remove `tile-keilhauer-seating` tile

**3. collection.boardroom — Remove dead callout + add GFG replacement**
- Remove `brand-keilhauer` block
- Add Global Furniture Group callout → `/collections/global-teknion`

**4. collection.storage — Add GFG callout**
- Add Global Furniture Group callout → `/collections/global-teknion`

**5. collection.business-furniture — Add GFG replacement for removed callouts**
- After removing Keilhauer + ergoCentric: add Global Furniture Group callout (distinct from the existing "Global / Teknion" callout — or consolidate into one stronger GFG callout)
- OR: consolidate `brand-global-teknion` into a cleaner "Global Furniture Group" callout

The following require Steve direction before Phase 2 can apply:

**A.** Desks (`collection.desks.json`) — Keep "Global / Teknion" naming or revise to "Global Furniture Group"?
**B.** Tables (`collection.tables.json`) — Add GFG callout or leave clean?
**C.** Ergonomic Products (`collection.ergonomic-products.json`) — Remove ergoCentric + no replacement, or add ObusForme?
**D.** Panels & Dividers (`collection.panels-room-dividers.json`) — Keep copy as-is or revise to remove Teknion name?
**E.** Brand plates (all pages) — Keep Keilhauer + ergoCentric in brand plate band, or wait for OTG/Heartwood brand pages before swapping?

**Phase 2 prerequisite if Steve wants OTG/Heartwood callouts:**
- Create `/collections/otg-offices-to-go` smart collection (rule: `brand:otg-offices-to-go`)
- Create `/collections/heartwood-manufacturing-ltd` smart collection (rule: `brand:heartwood-manufacturing-ltd`)
- (Optional) Create brand hub pages for OTG and Heartwood to support brand plate swaps

---

_End of Phase 1 audit. Awaiting Steve review before Phase 2 applies any theme changes._
