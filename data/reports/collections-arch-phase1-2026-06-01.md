# COLLECTIONS-ARCHITECTURE — Phase 1: Protect + Brand (Admin-API, additive)

**Date:** 2026-06-01 · **Status:** ✅ EXECUTED (Admin-API only — 0 theme files, 0 redirects, 0 deletes) · **Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`, verified by readback)

Executes the high-value **additive** half of the locked collections-architecture decision (A nav / B kill type-room dupes / C brand build / D filters). Redirects/consolidation are **Phase 2** (separate session). No hard deletes, ever.

---

## Phase 0 — live re-verification: 3 soundness findings that overrode the plan premise

| # | Locked-plan premise | Live reality (2026-06-01) | Resolution |
|---|---|---|---|
| **S1** | 3 ranking-empties published & serving 200 → "populate, never redirect" | `book-displays-storage` & `laboratory-furniture` **already unpublished + 301 → `/collections/business-furniture`** (redirect id `521366044985` confirmed). Only `keilhauer` is live (200, published, empty). | "Populate, don't redirect" applies to keilhauer only. Other two already consolidated → no action; reversal is a Phase 2 redirect decision. |
| **S2** | keilhauer → populate via `vendor=Keilhauer` | **0 Keilhauer SKUs in catalog** — no `vendor=Keilhauer`, no `brand:keilhauer` tag across 657 products. | keilhauer **cannot be populated**. Per Steve: **do NOT unpublish** (would lose #22 rank). Queued for the Phase 2 redirect set: `keilhauer → /pages/brands-keilhauer` (preserves rank). Carrying Keilhauer inventory = separate Steve call. |
| **S3** | specs.* density ~15% (gates specs-filter decision) | **Live density = 49.8% (327/657)** — manufacturer 312, dimensions 290, country_of_manufacture 265 (40%). | Materially changes decision (D): revisit specs-based Made-in-Canada / dimensions filters in Phase 3 — far more viable than the audit assumed. |

Other live facts: catalog **657 products** (596 active, 61 archived); `global-teknion` was **NOT** an empty scaffold (live, 197 products via tag rules); `global-furniture` custom scaffold already empty + unpublished (redundant, no action needed); all 6 brand pages live with clean dealer-focused SEO titles; brand collections were **tag-driven** (`brand:X`) and tags as dirty/incomplete as vendor (the 11 Teknion SKUs were untagged).

---

## Phase 2 — executed (Admin-API, hardened readback)

### 1. Vendor dedup — 7 clusters, 43 → 35 distinct vendors (canonical = clean customer-facing names, aligned to brand pages)

| Canonical vendor | Variants merged | Products | Brand-tag synced to |
|---|---|---|---|
| OTG / Offices to Go | + "Offices to Go" | 76 | `brand:otg-offices-to-go` |
| Heartwood Manufacturing | "Heartwood Manufacturing Ltd." (28) + "Heartwood" (10) | 39 | `brand:heartwood-manufacturing` |
| Office Star Products | + "Office Star" (5) | 18 | `brand:office-star-products` |
| Deflecto | + "deflecto" (6) | 9 | `brand:deflecto` |
| Foundations Worldwide | + "Foundations" (3) | 4 | `brand:foundations-worldwide` |
| Victor Technology | "Victor" (1) + "Victor Technology LLC" (1) | 2 | `brand:victor-technology` |
| MityBilt | "MityBilt Products Inc." (1) + "MityBilt" (1) | 2 | `brand:mitybilt` |

**57 products updated** (56 vendor + 1 tag-only), vendor field + matching `brand:*` tag synced in the same pass. **57/57 hardened readback MATCH, 0 fail.** Per-product before-snapshots in `data/backups/collections-arch-p1-2026-06-01/`; log in `data/logs/dedup-2026-06-01.json`.

**Out of scope (flagged, untouched):** `Brant Business Interiors` (221) + `Office Central & Brant Business Interiors` (4) = **225 vendor=dealer data-errors** (per `VENDOR-BBI-IS-ALWAYS-A-DATA-ERROR`). Sourcing real manufacturers = enrichment-accelerator carry-forward, not a dedup.

### 2. Brand collections built — `vendor=X` smart rules (not tags; tags incomplete), published, non-competing product-browse meta

| Collection | Rule | Count | Published | SEO title (product-browse, NOT "dealer Ontario") |
|---|---|---|---|---|
| `/collections/otg` (id 528240967993) | `vendor = OTG / Offices to Go` | 76 | ✅ | Shop OTG Office Furniture \| Brant Business Interiors |
| `/collections/heartwood` (id 528241000761) | `vendor = Heartwood Manufacturing` | 39 | ✅ | Shop Heartwood Office Furniture \| Brant Business Interiors |
| `/collections/obusforme` (id 528241033529) | `vendor = ObusForme` | 6 | ✅ | Shop ObusForme Ergonomic Seating \| Brant Business Interiors |

All 3 storefront-verified **HTTP 200**. Each carries a short product-browse `body_html` that links **to** its `/pages/brands-X` story page (division of labor: PAGE owns the brand-story/"dealer Ontario" SEO surface; COLLECTION is the filterable product grid). `ergocentric` left as-is (1 SKU — page already serves the term). `global-furniture` scaffold left as-is (already empty + unpublished, redundant).

### 3. `global-teknion` widened — added `vendor = Teknion` rule (disjunctive). **197 → 208** (picks up the 11 previously-untagged Teknion SKUs).

### keilhauer — NO action this session (per S2 / Steve). Still published, rule intact, count 0. Queued for Phase 2 redirect.

---

## Phase 3 — verification summary

- **Empties protected:** keilhauer untouched (rank preserved, Phase 2 redirect queued); the 2 already-redirected handles confirmed out of scope.
- **Dedup applied:** 57/57 MATCH, 43 → 35 vendors.
- **Brand collections live:** OTG (76), Heartwood (39), ObusForme (6) — all 200, all linked to their brand pages with non-competing meta; global-teknion 197→208.
- **Live specs.* density: 49.8% (327/657)** — feeds the deferred specs-filter decision (D).

**No redirects. No theme/nav changes. No deletes. Phase 2 (redirect/consolidation) HALTED for a separate session.**
