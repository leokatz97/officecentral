# COLLECTIONS-AUDIT + ARCHITECTURE — Phase 0 (full-store, READ-ONLY)

**Date:** 2026-06-01 · **Status:** AUDIT ONLY — no writes, no redirects, no meta edits. Decision-prep for a web-chat architecture call.
**Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`, verified prior session)
**Scope:** the *rest* of the store. The funnel set (reception, boardroom, executive-desks, healthcare, healthcare-seating) is already characterized in [`landing-refresh-plan.md`](landing-refresh-plan.md) — cross-referenced here, not re-litigated.

**Data sources**
- **Structure:** [`stage-4b-recover-current-collections.csv`](stage-4b-recover-current-collections.csv) — 358 collections (id, handle, type, published_at, live product count). 2026-05 snapshot.
- **Rank:** live DataForSEO `dataforseo_labs/ranked_keywords` pull (Canada, 2026-06-01) — 98 ranking keywords total; **60 on /collections/ URLs across 25 distinct handles**, plus 27 product-page + 11 homepage keywords. This is the authoritative "which collection ranks" asset.
- **Nav:** live `bbi-nav.liquid` + `bbi-footer.liquid` (the 2026-04-20 menu backup with 150 collection links is STALE — superseded by the Liquid-driven nav).
- **HTTP:** live `curl` spot-checks of decision-critical handles.

---

## TL;DR — the three structural facts

1. **The store has 358 collections; the live nav exposes 9.** Nav + footer link to exactly: `seating, desks, storage, tables, boardroom, ergonomic-products, panels-room-dividers, accessories, quiet-spaces` (+ `/collections/all`). **The other ~349 collections are nav-orphans** — reachable only by direct URL, search, internal links, or Google.

2. **Every collection that ranks is a nav-orphan.** All 25 ranking handles sit *outside* the 9-collection nav. BBI's hard-won organic authority lives almost entirely in **legacy 2024 custom collections the new nav doesn't link to.** Ranking authority and site architecture have drifted apart.

3. **~120 collections are empty (0 products) but still return HTTP 200.** 91 legacy empties + 31 from a 2026-05-07 taxonomy-scaffolding batch that was created but never populated. Each is a thin/empty page Google can crawl and index. Confirmed live: `acoustic-pods`, `active-seating`, `beam-seating`, `keilhauer`, `buy-canadian` all serve raw 200 with zero products.

4. **The store is sitting on a ready-to-use brand filter it isn't using.** `vendor` is populated with a real manufacturer on **435 of 656 products (66%)** — Global Furniture Group alone is **200**. Yet `/collections/global-furniture` is one of the empty 2026-05-07 scaffolds (0 products). The data to build brand collections/filters exists; it's just not wired up. (Step 5.)

---

## Step 1 — Inventory summary

| Metric | Count |
|---|---|
| Total collections | **358** |
| Smart collections | 35 |
| Custom collections | 323 |
| In **live nav** (canonical surface) | **9** |
| **Ranking** in Google top 100 (distinct handles) | **25** |
| Unpublished (no `published_at`) | 23 |
| Product count == 0 (empty) | 132 |
| ↳ of which **empty + published (serving 200)** | **~120** (91 legacy + ~29 scaffold) |
| ↳ empty + unpublished | 5 |
| Product count == -1 (smart/unresolved at snapshot) | 49 |

SEO-meta state was not pulled per-collection (358 Admin-API calls out of scope for a read-only pass); meta is inferred where it matters and flagged as "verify at write time." The prior funnel audit already established that the #70 meta pass only touched the funnel collections — **the ranking legacy collections below almost certainly carry generic/auto meta.**

---

## Step 2 — Rank per collection (the authority map)

All 25 ranking handles, by best position. **None are in nav.** `*FUNNEL*` = already covered in landing-refresh-plan.

| Handle | Pub | Products | Best rank — keyword (vol) | Breadth |
|---|---|---|---|---|
| `bariatric-seating` | Y | 5 | **#18** bariatric chairs (320) | 2 kw |
| `folding-stacking-chairs-carts` | Y | 7 | #20 folding chairs and cart (90) | 4 kw — banquet chair, stacking chairs canada |
| `keilhauer` | Y | **0 🔴** | #22 keilhauer office chairs (90) | ranks but EMPTY |
| `nesting-chairs-chair` | Y | 5 | #25 **nesting chair (1,600)** | 2 kw — highest-volume orphan term |
| `boardroom-conference-meeting` | Y | 11 | #26 modular boardroom tables (70) | *FUNNEL* |
| `gaming` | Y | 3 | #27 naz gaming chair (90) | **6 kw** — gaming-chair cluster |
| `reception-desks-desks` | Y | 9 | #27 custom reception counters (50) | *FUNNEL*, 5 kw |
| `fire-resistant-file-cabinets-storage` | Y | 6 | #28 fireproof cabinets (320) | **8 kw** — fireproof/fire-safe cabinet cluster |
| `recliners` | Y | 3 | #29 brant fine furniture (70) | brand-navigational |
| `training-flip-top-tables` | Y | 5 | #31 flip top tables (210) | 2 kw |
| `bar-height-tables` | Y | 3 | #31 tall table round (90) | 4 kw |
| `coffee-tables` | Y | 5 | #34 coffee table for office (70) | 1 kw |
| `pedestal-drawers-storage` | Y | 9 | #36 drawer pedestal (70) | 4 kw |
| `telephone-booths` | Y | 1 | #37 buy phone booth (90) | 1 kw |
| `cafeteria-kitchen-tables` | Y | 4 | #41 cafeteria kitchen (90) | **5 kw — cafeteria tables canada (4,400), cafeteria tables (880)** |
| `coat-racks-accessories` | Y | 2 | #41 coat rack industrial (50) | 1 kw |
| `lecterns-podiums` | Y | 5 | #41 podiums and lecterns (90) | 1 kw |
| `book-displays-storage` | Y | **0 🔴** | #43 literature display cabinet (90) | ranks but EMPTY |
| `modesty-panels` | Y | 2 | #45 modesty panel (260) | 1 kw |
| `desk-top-dividers` | Y | 4 | #48 office desk divider (90) | 3 kw |
| `healthcare` | **N** | 1 | #48 furniture healthcare (90) | *FUNNEL* (now unpublished) |
| `picnic-tables` | Y | 1 | #55 table picnic bmr (50) | 1 kw |
| `fire-resistant-safes-storage` | Y | 11 | #58 fire safe cabinet (140) | 1 kw |
| `benching-desks` | Y | 1 | #86 office benching (70) | 1 kw |
| `laboratory-furniture` | Y | **0 🔴** | #97 lab furnitures (110) | ranks but EMPTY |

**Highest-value orphans (volume × winnability):** `nesting-chairs-chair` (nesting chair, 1,600), `cafeteria-kitchen-tables` (cafeteria tables canada 4,400 + cafeteria tables 880, both ranking but deep at #75–79 — climbing room), the `fire-resistant-file-cabinets-storage` cluster (8 kw, ~320 vol each), and the `gaming` cluster (6 kw).

> Note for context: home page ranks #11 for **"brant's" (22,200)** and several brand-navigational terms; 27 product pages rank (strong cluster: the `wardrobe-with-lock` PDP holds 6 lock-wardrobe terms; `ceiling-baffles` PDP holds the acoustic-baffle cluster). Product-level authority is healthy and separate from this collections decision.

---

## Step 3 — Classification

### 🟢 A. Ranking orphans — the crown jewels (KEEP, protect, consider promoting)
The 22 non-funnel ranking handles above. They carry **all** of BBI's non-brand collection authority and **none** are linked from nav. **Ranking exposure: MAXIMUM.** Touching the handle/URL of any of these (rename, merge, redirect) risks the rank. These are keep-and-protect by default; the upside play is *adding* them to nav/internal links, not restructuring them.

### 🔴 B. Ranking-but-EMPTY — authority at risk (URGENT, but NOT a redirect)
`keilhauer` (#22), `book-displays-storage` (#43), `laboratory-furniture` (#97) **rank in Google but now have 0 products.** An empty page that ranks is a thin-content liability that will eventually drop. **Fix = repopulate, not redirect** — redirecting would forfeit the rank. (`keilhauer` is doubly notable: it's also a 2026-05-07 scaffold collection AND a `/pages/brands-keilhauer` nav page — the empty collection and the nav brand page coexist.)

### 🟠 C. Duplicate smart-collection taxonomies — cannibalization with the nav canon
Two parallel auto-generated smart-collection sets shadow the 9 nav collections:
- **`type-*`** (created 2026-04-20): `type-chairs`(184), `type-desks`(98), `type-tables`, `type-storage`(82), `type-accessories`(91), `type-lounge`, `type-outdoor` — near-duplicates of `seating/desks/tables/storage/accessories`.
- **`room-*`** (created 2026-04-20): `room-boardroom`(87 — **identical count to nav `boardroom`(87)**), `room-private-office`(168), `room-reception`(21), `room-open-plan`, `room-lounge`, `room-training-room`, `room-break-room`(0), `room-accessories`(0).

These are a "shop by type / shop by room" faceting scheme that was built but **not wired into the live nav.** They duplicate product sets under extra URLs → split crawl budget and potential self-cannibalization. **Ranking exposure: LOW** — none of the `type-*`/`room-*` handles appear in the rank pull. Safe to consolidate/redirect into their nav-canonical twin, *or* deliberately wire them in as faceted nav (a product decision, not just SEO).

### 🟠 D. 2026-05-07 taxonomy scaffolding — built, never filled (crawl bloat)
**31 empty custom collections** created 2026-05-07, all 0 products, mostly serving 200:
`acoustic-panels, acoustic-pods, active-seating, beam-seating, bench-seating, boardroom-seating, boardroom-storage, cafe-tables, conference-seating, desk-accessories, desktop-accessories, ergocentric, ergonomic-accessories, executive-desks*, executive-seating, focus-rooms, global-furniture, global-teknion, healthcare-seating*, high-density-storage, keilhauer†, mailboxes, media-storage, mobile-storage, nesting-tables, outdoor-tables, personal-storage, privacy-screens, standing-tables, wall-storage, waste-recycling`
(`*` = funnel, already handled; `†` = the ranking-but-empty case in B). **Ranking exposure: NONE** (except `keilhauer`). These are either (a) repopulate if the category is real, or (b) redirect to the nearest populated parent. `acoustic-pods` / `acoustic-panels` are worth flagging — the SEO strategy memo names acoustic pods a *hot* term, and the page exists but is empty.

### 🟠 E. Legacy granular duplicate families (2024 — double/triple variants)
The 2024 catalog created the same subcategory multiple times with suffix variants. Representative triples (all published, splitting authority):
- **L-shape desks:** `l-shape-desks`(31) · `l-shape-desks-1`(30) · `l-shape-desks-desks`(unresolved) · `l-shape`(27)
- **U-shape desks:** `u-shape-desks`(unresolved) · `u-shape-desks-1`(15) · `u-shape-desks-desks`(16)
- **Straight desks:** `straight-desks`(12) · `straight-desks-desks`(17) · `desks-straight`(18)
- **Height-adjustable tables:** `height-adjustable-tables`(19) · `-1`(18) · `-desks`(21)
- **Multi-person workstations:** ×3 · **Bookcases:** `bookcases`(9)/`bookcases-1`(1)/`bookcases-storage`(13) · **Pedestal drawers:** ×3 · **Fire-resistant cabinets:** several overlapping handles.

**Ranking exposure: MIXED — check per handle.** `pedestal-drawers-storage` and `fire-resistant-*-storage` and `boardroom-conference-meeting` ARE the ranking variant in their family → those are the keepers; their empty/non-ranking siblings are the redirect targets. The desks family is flagged in the prior funnel audit's "exec-desks inventory reality" — coordinate with that.

### ⚪ F. Long-tail legacy empties (redirect/cleanup candidates, no authority)
**91 empty + published legacy collections** serving 200 with zero products and zero rank — e.g. `anti-fatigue-mats, art-easel, audio-visual-equipment, beds-matresses, dining-room, dinning-furniture, doll-furniture, doors, epson, heaters, hp, ink-and-toner, kids-desks, paint-dryers, podiums, …`. Many are office-supply / printer / consumer-furniture remnants from the old Office Central catalog that don't fit BBI's B2B furniture focus. **Ranking exposure: NONE.** Redirect to nearest parent or unpublish-then-redirect. Plus **5 empty + unpublished** (`classroom-storage, educational, exam-room-seating, infant-toddler, preschool-couches-chairs`) — verify these aren't still 200 (unpublished ≠ non-200, per the executive-desks finding).

### ⚫ G. System / infrastructure collections (LEAVE)
`all, products, products-1, fees-products, mandatory-fees, smart-products-filter-index-do-not-delete, avada-best-sellers, bundle-builder-products, orderly-emails-recommended-products, business-furniture, oecm-eligible, frontpage, home-page, featured-homepage`. App-driven or system. Not customer-facing SEO targets. No action.

---

## Step 4 — Architecture options + ranking-exposure tags

> Redirects only (recoverable). **No hard deletes** — per BBI rule, archive/unpublish/redirect, never delete. Each option is decision-prep; nothing executes here.

| # | Issue | Option (recommended first) | Ranking exposure |
|---|---|---|---|
| 1 | **Ranking orphans (A)** — 22 authority collections invisible to nav | **KEEP all.** Upside play: add the top ~6 (nesting-chairs, cafeteria-kitchen-tables, fire-resistant-file-cabinets, gaming, bariatric-seating, folding-stacking-chairs) to nav or to relevant landing/PDP internal links to compound existing rank. Do **not** rename/merge. | 🔴 MAX — protect handles |
| 2 | **Ranking-but-empty (B)** — keilhauer / book-displays-storage / laboratory-furniture rank with 0 products | **Repopulate** each with relevant SKUs to convert the rank into a real page. **Never redirect** (forfeits rank). Resolve keilhauer's collection-vs-brand-page duplication separately. | 🔴 MAX — repopulate, don't touch URL |
| 3 | **Duplicate smart taxonomies (C)** — type-*/room-* shadow the 9 nav collections | (a) **Redirect** type-*/room-* into their nav-canonical twin (e.g. `type-chairs`→`seating`, `room-boardroom`→`boardroom`); **or** (b) deliberately surface them as faceted "shop by type / by room" nav. Decision is product-strategy, not just SEO. | 🟢 LOW — none rank |
| 4 | **2026-05-07 scaffolding (D)** — 31 empty pages serving 200 | Per handle: **repopulate** if the category is real & on-strategy (acoustic-pods/panels, focus-rooms, privacy-screens look worth filling for the workspitality/acoustic angle); **redirect** the rest to nearest populated parent. | 🟢 LOW (except keilhauer → see #2) |
| 5 | **Legacy granular dupes (E)** — l-shape/u-shape/straight desks, height-adjustable tables, bookcases, pedestals, etc. | **Pick the ranking variant as canonical per family; 301 the siblings into it.** Where none rank, keep the most-populated, redirect the rest. Coordinate desks family with the deferred exec-desks build session. | 🟠 MIXED — verify each handle vs rank table before merging |
| 6 | **Long-tail legacy empties (F)** — 91 empty+published serving 200, + 5 empty+unpublished | **Bulk 301** the off-strategy / printer / consumer remnants to nearest parent (or `/collections/all`); confirm the 5 unpublished ones actually stop 200-ing (redirect is the real 200-killer). Biggest single crawl-hygiene win. | ⚪ NONE |
| 7 | **System collections (G)** | **Leave.** | ⚪ NONE |

### Two cross-cutting calls for the architecture session
- **(A) Nav strategy:** does BBI *want* the 9-collection minimalist nav, with ranking orphans surfaced only via internal links — or should the high-value ranking orphans (nesting chairs, cafeteria tables, fireproof cabinets, gaming) be promoted into nav? This is the single highest-leverage decision in the audit.
- **(B) type-*/room-* faceting:** kill as dupes, or activate as a faceted browse layer? Affects whether option #3 is a redirect job or a nav build.

### Redirect mechanism note
Per the COLLECTION-CLEANUP precedent and the token's missing `write_content` scope, any approved 301s ship as a **CSV for manual Shopify-Admin import**, not POSTed via API. Nothing was created on the live store in this pass.

---

---

## Step 5 — Filter & sub-collection readiness (candidates only — DO NOT BUILD)

### 5a. Current faceted-nav state
The theme renders **Shopify's native storefront filters** generically (`results.filters` in [`collection-filters.liquid`](../../theme/snippets/collection-filters.liquid)) — boolean, list, swatch, and `price_range` types, with per-collection `enable_filtering` toggles on the `base`/hub templates. The actual *facet set* (which fields appear) is defined in the **Search & Discovery app** (Admin-level, not in theme/token reach), so this audit infers availability from the underlying data rather than reading the app config directly — **verify the live filter config before building.**

**Crawl-bloat note:** Shopify's filter system appends `?filter.*=` params and applies `rel="canonical"` back to the clean collection URL by default, so faceted URLs are largely self-canonicalising — filters are **not** the main index-bloat risk here. The real bloat is the **349 nav-orphan collections + ~120 empty-but-200 pages** (Steps 1–4). Tag-handle collection URLs (`/collections/x/tag`) are the one filter-adjacent path that *can* generate crawlable variants — confirm none are linked/indexed if tag-faceting is enabled.

### 5b. Filterable-attribute readiness (what the data actually supports today)

| Candidate facet | Data source | Density (of 656) | Verdict |
|---|---|---|---|
| **Brand / Manufacturer** | native `vendor` field | **435 real (66%)** — Global 200, OTG 75, Heartwood 38, Teknion 11, Safco 11, Fellowes 10… | ✅ **Viable now** — but vendor is **dirty**: `Heartwood Manufacturing Ltd.`+`Heartwood`, `Office Star Products`+`Office Star`, `deflecto`+`Deflecto`, `Office Central & Brant Business Interiors`. **Normalize/dedupe (43→~30 vendors) first.** No metafield needed. |
| **Price** | native variant price | 100% | ✅ Already live (price-range slider in theme). |
| **Made in Canada / Country** | `specs.country_of_manufacture` | ~**15%** (enriched only) — but derivable from vendor (Global, Heartwood, Teknion, Tayco, Borgo = Canadian) for far more | ⚠️ Thin via metafield; **better sourced from a normalized vendor→country map** until enrichment expands. |
| **Product line** | `specs.product_line` | ~15% (Global family) | ⚠️ Useful only inside the Global family; not catalog-wide. |
| **Certifications (BIFMA/GREENGUARD)** | `specs.certifications` | ~15%; BIFMA common, **GREENGUARD rare** | ❌ Not ready — a GREENGUARD filter would surface a handful of items. Revisit after enrichment. |
| **Dimensions (W/D/H)** | `specs.dimensions` | ~15%, **stored as one unparsed string** (`20"W x 21"D x 31.5"H`) | ❌ Not range-filterable without parsing into numeric fields. |
| **Product type** | native `product_type` field | **85% BLANK** (557/656) | ❌ Dead — type faceting must come from `type:`/`room:` **tags**, not this field. |

**Enrichment density reality:** the rich `specs.*` metafields (manufacturer, product_line, certifications, country, dimensions, warranty) were written by the Block-4 enrichment to **~85 products (+~14 earlier specs pushes) ≈ 100 of 656 (~15%)**, concentrated in the **Global Furniture Group** family. They are excellent *within that island* but too sparse to drive a **catalog-wide** metafield filter yet. The one attribute that is *already* broad enough is **vendor** — and it predates enrichment.

> Note: `productsCount` silently ignores metafield query filters (a control query for a nonsense namespace returned the full 656), so exact per-metafield density couldn't be counted via that endpoint — the ~15% figure is derived from enrichment payload counts. A definitive count needs a per-product metafield scan; flag for the build session.

### 5c. Sub-collection structure (as built)
- **Model:** one-level **hub-and-spoke**, metafield-simulated (Shopify has no native nesting). 9 smart **hubs** (the nav set) at top; ~**88 "base" sub-collections** each carrying `bbi.parent_hub_handle` → its hub, rendered through `ds-cs-base.liquid` (`template_suffix=base`) with a breadcrumb up to the parent. Pilot migration: `highback-seating`.
- **Smart vs manual:** the 9 hubs + `type-*`/`room-*` + `business-furniture`/`all`/`oecm-eligible` are **smart** (tag/price rule-driven). The ~88 base subs and the legacy granular collections are mostly **custom/manual**.
- **Overlaps/redundancy (ties to Steps C & E):** `type-*` and `room-*` duplicate the hubs; legacy granular **triples** (l-shape/u-shape/straight desks, height-adjustable tables, bookcases, pedestals) split one category across 2–3 manual collections. Each sub has exactly one `parent_hub_handle`, so a product can sit in several subs but each sub rolls up to a single hub — clean enough that consolidation is redirect-and-retag, not a re-architecture.

### 5d. CANDIDATE new sub-collections the enriched/vendor data could support (do **not** build — for the architecture decision)

| Candidate | Build rule | Est. size | Why / caveat |
|---|---|---|---|
| **Shop by Brand** (Global Furniture Group, OTG, Heartwood, Teknion…) | smart, `vendor = X` | Global **200**, OTG 75, Heartwood 38 | Highest-leverage. Brand *content pages* already exist (`/pages/brands-*`) but no brand *product collections*; meanwhile empty scaffolds `global-furniture`/`global-teknion`/`keilhauer`/`ergocentric` sit unpopulated next to 200+ matching products. **Populate these via vendor rules** — fixes the ranking-but-empty `keilhauer` (Step B) at the same time. Dedupe vendor first. |
| **Made in Canada** | smart, vendor∈Canadian-makers (or `specs.country_of_manufacture=Canada`) | ~250+ via vendor map | Strong on-brand story (Canadian-Owned / OECM moat; add maple-leaf accent per brand rules). Use vendor-derived country for coverage; metafield alone is too thin. |
| **OECM-Eligible** | *(already exists)* smart `oecm-eligible` (653) | 653 | No build — already live; surface it more prominently if desired. |
| **BIFMA / GREENGUARD certified** | smart, `specs.certifications` contains X | thin (GREENGUARD ~handful) | ❌ Defer until certification enrichment broadens. |
| **By product line** (Global "Marche", "2600 Series"…) | smart, `specs.product_line = X` | small each | Too granular for nav; better as PDP cross-links within the Global family. |

**The single highest-value Step-5 move:** wire the **vendor → brand collection** mapping (after a vendor cleanup pass) — it simultaneously (a) gives a real Brand filter for 66% of the catalog, (b) populates the empty brand scaffolds, and (c) rescues the ranking-but-empty `keilhauer`. It needs no new enrichment — only vendor normalization.

---

## HALT
Read-only audit complete (Steps 1–5). No writes, no redirects, no meta edits, no collections/filters built. This is decision-prep for the web-chat architecture call.

**Decisions needed before any execution session is scoped:**
- **(A) Nav strategy** — keep the 9-collection minimalist nav (orphans surfaced via internal links) or promote high-value ranking orphans (nesting chairs, cafeteria tables, fireproof cabinets, gaming) into nav?
- **(B) type-*/room-* faceting** — kill as duplicates (301 → nav twins) or activate as a faceted browse layer?
- **(C) Brand architecture** — approve the vendor-cleanup → brand-collection build (populates the empty brand scaffolds + enables the Brand filter + fixes ranking-but-empty `keilhauer`)?
- **(D) Filter set** — confirm the live Search & Discovery facet config and decide whether to add Brand (ready) and Made-in-Canada (vendor-derived) filters now, deferring certification/dimension filters until enrichment broadens.
