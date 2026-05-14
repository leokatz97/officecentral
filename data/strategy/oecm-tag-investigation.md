# OECM Tag Investigation
_2026-05-14 · BUG-FIX-2 (Step 2) · Read-only investigation._

---

## TL;DR

**Recommendation: Option B — STRIP + RE-TAG via derived rule, applied in two directions.**

The original concern ("oecm-eligible on 100% of products makes the OECM page surface the full catalog") is a half-truth. The editorial `/pages/oecm` landing page is fully fine — it doesn't filter by the tag at all. The issue is narrower: the `/collections/oecm-eligible` smart collection (published, live) currently shows 532/593 active products.

More importantly, the tag state is WRONG in both directions: 9 service/fee line items have it and shouldn't; 61 real furniture products (chairs, desks, filing cabinets, bookcases from Global, OTG, Heartwood, etc.) are missing it and should have it. BBI holds OECM Agreement 2025-470 covering their entire furniture catalog — the tag is semantically correct on all furniture products, not just a curated subset.

BUG-FIX-3 should: strip from 9 service/fee items, add to 61 missing furniture products, net result ~584 products with oecm-eligible. No curated "Hero" list needed; the OECM agreement covers the full furniture catalog. Combined with the industry:* remediation scope, estimated 45 min.

---

## Current state

| Metric | Value |
|---|---|
| Total active products | 593 |
| Products with `oecm-eligible` | 532 (89.7%) |
| Products without `oecm-eligible` | 61 (10.3%) |
| `oecm-eligible` smart collection | id=526906687801 · published 2026-05-08 · best-selling sort |

**Note on the 653 figure:** The original DEBT-03 finding (653/653) was recorded before 336 archive-candidate products were moved to the "Other" collection (PE-PASS-2 + COLLECTION-CLEANUP-APPLY). Current active count is 593, not 653.

### Vendor distribution of oecm-eligible products (top 15)

| Count | Vendor |
|---|---|
| 343 | Brant Business Interiors (unenriched placeholder) |
| 62 | Global Furniture Group |
| 57 | OTG / Offices to Go |
| 20 | Heartwood Manufacturing Ltd. |
| 11 | Teknion |
| 5 | ObusForme |
| 5 | Horizon |
| 4 | Fellowes |
| 4 | Safco |
| 3 | Office Star |
| 2 | Deflecto |
| 2 | Humanscale |
| 1 | Axis / MergeWorks / FireKing |

### OECM page mechanism

The `/pages/oecm` editorial page (`ds-lp-oecm.liquid` + `page.oecm.json`) is **fully editorial** — zero Liquid references to the `oecm-eligible` tag. The template's three cross-link tiles go to `/collections/seating`, `/collections/desks`, and `/collections/storage` (not to `/collections/oecm-eligible`). The editorial page is NOT broken and requires no changes.

The `/collections/oecm-eligible` smart collection (rule: `tag equals oecm-eligible`) is the only surface affected by the tag. It exists, is published, and currently shows 532 products. It is not linked from the OECM page or from the nav, but it is crawlable.

---

## Investigation findings

### How the OECM page references the tag

It doesn't. A full grep of `theme/sections/`, `theme/snippets/`, `theme/templates/`, and `theme/layout/` for `oecm-eligible` (as a tag filter or Liquid condition) returned zero matches. All OECM mentions in theme files are copy-level text ("OECM-eligible supplier", "Agreement 2025-470") — no product filtering logic.

### Is there an existing canonical OECM-eligible list?

No. No spreadsheet, CSV, or list of verified OECM product handles exists in the repo or in BBI-Session-Kickoff/. There are no OECM-related product metafields (`oecm_status`, `specs.oecm_status`, etc.) — none of the 18 metafield namespaces on Shopify contain "oecm". The only signal is the tag itself.

### Do vendor or metafield data support a derived eligibility rule?

Yes — and crucially, BBI's OECM Agreement 2025-470 covers the **entire furniture catalog**, not specific products. The agreement is supplier-level, not SKU-level. This is confirmed by the OECM page copy: *"Every category is OECM-eligible."* (`ds-browse-faq.liquid` line) and the landing page hero: *"Brant Business Interiors is an OECM Supplier Partner (Agreement 2025-470)."*

The correct derived rule is therefore: **any active product that is a real furniture item** (excludes service/fee line items). Service/fee items are identifiable by handle pattern.

### Tag state analysis — what's wrong in BOTH directions

**9 service/fee items incorrectly carrying `oecm-eligible` (should be stripped):**

| Handle | Why it should be stripped |
|---|---|
| `colour` | Placeholder/dummy SKU |
| `delivery` | Delivery service line item |
| `delivery-charge-175-00` | Delivery fee |
| `delivery-charge-85-00` | Delivery fee |
| `diet` | Non-furniture placeholder |
| `dispose` | Disposal service |
| `installation-1` | Installation service |
| `installation1000` | Installation fee |
| `installation475` | Installation fee |

**61 real furniture products missing `oecm-eligible` (should be added):**

All 61 have `brand:*` tags confirming they are real, enriched furniture products — chairs, desks, bookcases, filing cabinets, folding tables, etc. from Global Furniture Group, OTG, Heartwood, Fellowes, FireKing, and others. Full list: `2-drawer-legal-width-vertical-file`, `bar-stool-for-42-high-tables`, `basics-comfort-time-ultra-multi-tilter-chair-with-headrest`, `bookcase`, `bookcase-with-closed-lower-storage`, `coffee-table`, `coffee-table-1`, `concorde-high-back-24hr-executive-synchro-tilter-deep-seat-2`, `desk-shell-5-sizes`, `desk-single-pedestal-1`, `electric-dual-monitor-height-adjustable-standing-desk-workst`, `elora-multi-tilter-high-back-chair-black-petite-seat-baomvl1`, `factor-mesh-seating-stool`, `fellowes-array-recess-ar-air-purifier-1`, `fellowes-array-wall-stand-air-purification`, `fellowes-lotus-dual-monitor-arm-kit-2-display-s-supported27-`, `fireking-storage-cabinet-44-high`, `folding-table-24-x-48-1`, `folding-table-36-bt36-resin`, `freefit-benching-height-adjustable-176w-x-62-5d-ffhab506-2`, `halifax-typical-4`, `hdl-5-resin-folding-table-granite-rectangle-dove-white-pebbl`, `heartwood-mobile-pedestal-bf`, `high-back-weight-sensing-synchro-tilter`, `innovations-l-shape-desk-with-hutch`, `innovations-u-shape-suite`, `kensington-ac12-security-charging-cabinet`, `l-shape-desk-set-72x72`, `laminate-lockers-copy`, `lateral-file-storage-cabinet-with-shelves`, `management-u-shaped-suite-72w-x-102d`, `management-u-shaped-suite-with-3-stage-height-adjustable-tab`, `marche-guest-chair-8622`, `mobile-drawer-unit-with-locks-inv-mpuf`, `newland-16w-box-box-file-mobile-pedestal-nlmp23bbf`, `newland-bookcases-assembled`, `obusforme-comfort-high-back-chair-1260-3-schukra`, `offices-to-go-ionic-table-36-x-36-x-29-material-metal-base-f`, `offices-to-go-newland-u-shaped-suites-nlp406`, `otg-panels`, `otgma2-dual-monitor-arm`, `partitions-66-high-2-offices-1`, `planter`, `rollamat-for-carpet-carpeted-floor-53-x-45-3`, `round-table-42`, `sentry-safe-security-safe-with-electronic-lock-4`, `single-pedestal-desk-nlp232`, `sit-stand-fellowes-lotus-dual-arm-not-included`, `sonic-armless-counter-stool-polypropylene-seat-back-6558cs`, `sparrow-otg10920-guest-chair`, `stacking-chair-duet-glb6621`, `the-erin-armless-chair-wood-legs-gc36530`, `tl-high-back-synchro-tilter`, `trent-tilter-chair-high-back-bonded-leather-2717-4`, `tritek-7472-3-chair`, `u-shaped-suite-with-rectangular-island`, `ultra-armless-high-back-tilter-mvl11732`, `ultra-medium-back-guest-chair-with-arms-mvl11742`, `wardrobe-storage-cabinet-htwlevsr7218`, `yoho-medium-back-task-chair-mvl2778`, `zune-tilter-chair-black-fabric-seat-plastic-mesh-back-medium`.

### Estimated count of legitimately OECM-eligible products

**~584** (532 current − 9 service/fee + 61 missing furniture = 584). This is essentially the full active furniture catalog minus nine service/fee SKUs.

---

## Remediation options analyzed

### A — STRIP + RE-TAG via curated list
Strip oecm-eligible from all 532 products, then re-apply to a manually curated "Hero OECM" subset.

**Pros:** Creates a tight, curated showcase collection.
**Cons:** Requires Steve to manually approve a list of ~50–200 products, with no clear OECM-specific inclusion criteria (since BBI's agreement covers the full catalog). Would make `/collections/oecm-eligible` under-represent BBI's actual OECM footprint. Maintenance burden every time a new product is added.
**Verdict: Not recommended.** BBI's agreement is supplier-level, not SKU-level.

### B — STRIP + RE-TAG via derived rule ✅ RECOMMENDED
Strip from 9 service/fee items; add to 61 currently-missing furniture products. Net result: ~584 products.

Derived rule: exclude handles matching `delivery`, `delivery-charge-*`, `installation-*`, `dispose`, `colour`, `diet` → all others are oecm-eligible.

**Pros:** Semantically accurate. Aligns with Agreement 2025-470 ("every category"). Self-documenting — "oecm-eligible" means "real furniture product, purchasable under OECM." Low maintenance: new furniture products just need to be tagged by convention. Fixes both the 9 incorrect inclusions AND the 61 incorrect exclusions.
**Cons:** The `/collections/oecm-eligible` smart collection will show ~584 products — still the full furniture catalog. If the intent was a curated showcase, this doesn't create one.
**Verdict: Recommended.** Aligns tag with BBI's actual OECM scope.

### C — RENAME + RE-SCOPE
Rename `oecm-eligible` to something like `catalog-active` (reflecting historical mass-apply use), create a new `oecm-verified` tag for a curated subset.

**Pros:** Clean separation of "active product" vs "OECM verified."
**Cons:** Requires two tag operations + smart collection rebuild. The `oecm-eligible` name is already correct for BBI's agreement (it IS their whole catalog). Adds complexity for no customer-visible benefit.
**Verdict: Not recommended.** Creates unnecessary vocabulary.

### D — RE-SCOPE OECM PAGE
Leave the tag entirely as-is; update the OECM editorial page to filter by something else if needed.

**Pros:** Zero remediation work.
**Cons:** Doesn't fix the 9 service/fee items that shouldn't be tagged. Doesn't add the 61 missing furniture products. The tag state stays inconsistently wrong in both directions.
**Verdict: Not recommended** as a standalone approach, but the editorial OECM page itself needs no changes (see findings above).

---

## Recommendation

**Use Option B.** BUG-FIX-3 should execute this two-directional tag fix:

### BUG-FIX-3 OECM scope (estimated ~20 min)

1. **Strip `oecm-eligible` from 9 service/fee products** — handles: `colour`, `delivery`, `delivery-charge-175-00`, `delivery-charge-85-00`, `diet`, `dispose`, `installation-1`, `installation1000`, `installation475`.

2. **Add `oecm-eligible` to 61 missing furniture products** — the full handle list is in the "61 real furniture products missing oecm-eligible" section above. All have `brand:*` tags; no further vetting needed.

3. **Net result:** ~584 products with `oecm-eligible`. The `/collections/oecm-eligible` smart collection auto-updates (rule-based). No Liquid changes needed.

4. **No OECM landing page changes needed.** `/pages/oecm` is editorial and correct as-is. The `bbi-oecm-bar` snippet is correct as-is. Consider adding "Browse products →" CTA on the OECM page pointing to `/collections/oecm-eligible` as part of AI-8 (OECM copy hardening) — this would surface the collection legitimately.

**Script pattern** (same as any tag-strip/apply script): pull active products, compare tags list, batch PUT via Shopify Admin API. Backup tags before run. Dry-run first, then `--live`.

---

## Combined OECM + industry:* scope for BUG-FIX-3

Per TAG-INDUSTRY-CHECK (Step 6, commit `e669122`), BUG-FIX-3 must also handle the industry:* mass-tag remediation. Summary of that scope (full detail in `data/strategy/industry-tag-decision.md`):

| Sub-task | Products affected | Estimated time |
|---|---|---|
| Fix `business-furniture` smart collection: replace 3 negative `industry:*` exclusion rules with positive `type:*` inclusion rules | 1 collection, 1 API PATCH call | ~5 min |
| Strip all `industry:*` tags from ~550 products (`industry:business` × 548, `industry:healthcare` × 1, `industry:daycare` × 1) | 550 products | ~15 min |
| Strip `oecm-eligible` from 9 service/fee items | 9 products | ~5 min |
| Add `oecm-eligible` to 61 missing furniture products | 61 products | ~10 min |

**Estimated total BUG-FIX-3 effort: ~35–45 min.**

Ordering matters: fix `business-furniture` smart collection BEFORE stripping `industry:*` tags (the collection depends on those exclusion rules until they're replaced).

---

## File written
`data/strategy/oecm-tag-investigation.md`
