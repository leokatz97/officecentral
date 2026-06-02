# COLLECTIONS-ARCHITECTURE — Phase 2: Consolidation & Crawl Hygiene (PLAN + CSVs)

**Date:** 2026-06-01 · **Status:** ✅ PLANNED — redirect CSVs + repoint spec staged for Steve. **NO live redirect writes, NO theme writes, NO deletes this session.** · **Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`)

The redirect/consolidation half of the locked collections-architecture decision. Token lacks `write_content` → redirects ship as CSVs Steve imports via Shopify Admin. The additive half (vendor dedup + brand collections) shipped in Phase 1 (`collections-arch-phase1-2026-06-01.md`).

---

## Phase 0 — Safety gate (reads only)

### Do-not-touch (ranks) list — 25 handles, LIVE-confirmed (DataForSEO `ranked_keywords`, Canada, 2026-06-01)
Built from the live rank pull, **not** the snapshot. Every handle EXCLUDED from both redirect CSVs (these are the Phase-3 promote-to-nav assets). `keilhauer` is the one deliberate exception (Batch D).

| Handle | Rank | Handle | Rank | Handle | Rank |
|---|---|---|---|---|---|
| bariatric-seating | 13 | bar-height-tables | 28 | book-displays-storage | 38 |
| folding-stacking-chairs-carts | 15 | cafeteria-kitchen-tables | 29 | desk-top-dividers | 38 |
| keilhauer | 15 | pedestal-drawers-storage | 31 | healthcare | 43 |
| nesting-chairs-chair | 18 | telephone-booths | 32 | fire-resistant-safes-storage | 48 |
| gaming | 21 | coat-racks-accessories | 34 | picnic-tables | 48 |
| fire-resistant-file-cabinets-storage | 22 | lecterns-podiums | 35 | benching-desks | 72 |
| boardroom-conference-meeting | 22 | modesty-panels | 36 | laboratory-furniture | 83 |
| reception-desks-desks | 23 | coffee-tables | 26 | | |
| recliners | 25 | training-flip-top-tables | 26 | | |

### Live re-verification — the snapshot was wildly stale (confirmed a 3rd time)
Pulled all **1,660 live URL redirects** (Admin API) + live GraphQL product counts (391 collections). Cross-checked all 139 candidates:
- **104 of 139 candidates were ALREADY redirected** (zero chains among them). Nearly the entire legacy-empty set (Batch A — `epson`, `hp`, `doll-furniture`, `heaters`, the printer/consumer remnants) was already 301'd in prior cleanup.
- `book-displays-storage` & `laboratory-furniture` still appear in rank data but are **already 301'd → `/collections/business-furniture`** (Phase 1 finding) — left as-is.
- Brand collections `otg`/`heartwood`/`obusforme` are BUILT (Phase 1) — not candidates. `global-teknion` live at 208 — a target, not a candidate. `executive-desks`/`healthcare-seating` already redirected (landing-refresh CSV).

### Out-of-scope live findings flagged (NOT redirects created here — Phase 3 carry-forwards)
- **`/collections/quiet-spaces` — a LIVE NAV item — itself 301s → `/collections/accessories`** (confirmed live curl). The nav "Quiet Spaces" link hops; its template (`collection.quiet-spaces.json`) never renders. Unusable as a redirect target → Batch B routes acoustic items to `panels-room-dividers`.
- **`/collections/benching-desks` (ranks #72) itself 301s → `/collections/desks`.** This pre-existing redirect forfeits the #72 rank AND made Steve's approved retarget `room-open-plan → benching-desks` non-viable (would chain). Resolution: `room-open-plan → /collections/desks` directly (the chain endpoint, zero-chain). Flagged for Phase 3 review.
- `/collections/all` has a stale redirect entry → `/collections/products`, but Shopify reserves `/collections/all` so it serves 200 live. Avoided as a target regardless.

---

## Batch decisions (as approved, with verified refinements)

### Batch A — ZERO redirects
`buy-canadian` is **HELD** — it becomes the Made-in-Canada collection in Phase 3 (ties to the 2D specs filter + 265 products carrying `country_of_manufacture`). The legacy printer/consumer empties were already redirected in prior cleanup. Batch A ships nothing.

### Batch 1 CSV — 34 rows — `collections-phase2-batch1-301s.csv` (no theme dependency, import anytime)
- **Batch B (14):** scaffold empties → nav parent. **HELD (not redirected):** `acoustic-pods`, `focus-rooms` (Phase-3 Quiet Spaces/Pods build candidates — keeps the quiet-spaces.json tiles valid, dropping those 2 repoints), `standing-tables` (handle intent unconfirmed).
- **Batch C1 (14):** type-*/room-* smart dupes → nav twin, accumulator-routed into a ranking twin where one exists:
  - `room-reception → reception-desks-desks` (#23), `room-training-room → training-flip-top-tables` (#26) ✓ both clean 200.
  - `room-open-plan → desks` (benching-desks retarget rejected — it self-redirects; see flag above).
  - `type-outdoor → business-furniture` (live product read = outdoor benches + recliners, **not** tables → not picnic-tables).
  - `room-private-office → desks` (confirmed).
- **Batch C2 ranking-keeper families (5 rows):** siblings folded INTO the ranking keeper — `pedestal-drawers`/`-1 → pedestal-drawers-storage` (#31); `fire-resistant-file-cabinets` + mixed `fire-resistant-file-cabinets-safes` → `fire-resistant-file-cabinets-storage` (#22); `fire-resistant-safes → fire-resistant-safes-storage` (#48). `mobile-pedestals`/`pedestals`/bookcases family HELD (distinct).
- **Batch D (1):** `keilhauer → /pages/brands-keilhauer` — the one deliberate ranking-URL redirect (200 confirmed), routes #15 authority onto the live dealer page.

### Batch 2 CSV — 9 rows — `collections-phase2-batch2-deskfamilies-301s.csv` (⚠ GATED on the repoint deploy)

**C2 product-ID overlap check** (siblings vs cleanest-handle keeper, % of sibling contained in keeper):

| Family | Keeper | Sibling overlap | Verdict |
|---|---|---|---|
| L-shape | `l-shape-desks` (31) | `-desks` 100%, `-1` 100%, `l-shape` 100% | **CONSOLIDATE** |
| U-shape | `u-shape-desks` (15) | `-1` 100%, `-desks` 94% | **CONSOLIDATE** |
| Height-adjustable | `height-adjustable-tables` (19) | `-1` 100%, `-desks` 86% | **CONSOLIDATE** |
| Multi-person workstations | `multi-person-workstations` (8) | `-1` 100%, `-desks` 89% | **CONSOLIDATE** |
| Straight desks | `straight-desks` (12) | `straight-desks-desks` 71%, `desks-straight` 56% (+9 unique) | **DROPPED — genuinely distinct** |

4 families consolidated (9 redirect rows); Straight family dropped (all 3 collections stay live). Two siblings (`height-adjustable-tables-desks`, `multi-person-workstations-desks`) are linked from live `collection.desks.json` tiles → **this CSV must not import until the repoint PR deploys.**

---

## Link-repoint spec (separate watcher-gated theme PR — NOT this session)

Nav/footer and the cornerstone blog post are **clean** (cornerstone links only `/collections/desks` + `/collections/seating`, both canonical). Only remaining repoints, both `collection.desks.json` crosslink tiles, must land + deploy BEFORE the Batch 2 CSV import:

| Live link | File | Repoint to |
|---|---|---|
| `/collections/height-adjustable-tables-desks` | `theme/templates/collection.desks.json` | `/collections/height-adjustable-tables` |
| `/collections/multi-person-workstations-desks` | `theme/templates/collection.desks.json` | `/collections/multi-person-workstations` |

(The `acoustic-pods` / `focus-rooms` repoints in `collection.quiet-spaces.json` dropped out — those two collections are now HELD, so the tiles stay valid.)

---

## Sequencing
1. **Batch 1 CSV** → Steve imports anytime (no theme dependency). Verify live + watch the rank snapshot, THEN proceed.
2. **desks.json repoint PR** (2 links, watcher-gated, separate session) → merge + deploy → **THEN** Batch 2 CSV import. Never Batch 2 before the deploy.
3. Between-batch rank monitoring — these redirects ADD to the boardroom-301 watch already on the next snapshot.

## Verification summary
- **Batch 1: 34 rows.** All targets resolve **200, zero chains**; no duplicate From rows. Only ranking handle in the From column = `keilhauer` (the sanctioned Batch D exception).
- **Batch 2: 9 rows.** All targets resolve 200, zero chains; **zero ranking handles** in the From column; no duplicates.
- C2 overlap: 4 families consolidated, Straight dropped (distinct).
- Non-nav ranking targets live-curled 200: `training-flip-top-tables`, `reception-desks-desks`, `pedestal-drawers-storage`, `fire-resistant-file-cabinets-storage`, `fire-resistant-safes-storage`.

## Phase 3 carry-forwards (logged, not acted on)
- quiet-spaces nav hop (live nav item 301s → accessories) + build a real Quiet Spaces/Pods collection (`acoustic-pods`/`focus-rooms` intent, both held here).
- `benching-desks` ranks #72 but self-redirects → desks (pre-existing authority forfeit) — review.
- `buy-canadian` → Made-in-Canada collection (with the 2D specs filter, 265 country_of_manufacture products).
- `standing-tables` target decision (pending catalog read).
- Promote the 25 ranking nav-orphans into nav / internal links (the additive upside play).

**HALT — CSVs + repoint spec staged. No live redirect writes, no theme writes, no deletes.**
