# Collections Phase 2 — Batch-2 (Desk Families) Source-Unpublish (provenance) — 2026-06-02

**Status:** ✅ LIVE — batch-2 consolidation now firing. **This completes Phase 2 end-to-end** (both batches imported + activated). **Admin-API publish toggles only** — 0 theme writes (no watcher gate), 0 redirect writes, 0 menu writes.
**The gated follow-up to the Phase-3 `desks.json` repoint deploy ([#83](https://github.com/leokatz97/officecentral/pull/83)):** Steve imported `collections-phase2-batch2-deskfamilies-301s.csv`, so the 9 batch-2 redirects now exist; per the **dormant-redirect mechanic** they were inert while their sources stayed published. This session unpublished the 9 published desk-family sources so the redirects fire.

## Result
- **9 sources unpublished** → each now serves **301 → its keeper** (9/9 storefront 301 confirmed live, **no edge-lag**), REST `published_at=null` on all 9 (authoritative MATCH).
- **0 already-firing** (no source was pre-unpublished this round).
- **0 / 9** are ranking handles (all no-rank legacy desk dupes). **0** chains, **0** 404s.
- **Empirical self-heal confirmed** for the one source with theme data-fallback refs — see below.

## Phase 0 — verification + classification (read-only, the safety crux)
Script: `scripts/phase0-batch2-classify.py` → `data/reports/phase0-batch2-classify-2026-06-02.json`

| Gate | Result |
|---|---|
| Batch-2 redirects present in **live map** (Admin API, authoritative) | **9 / 9** — import landed fully |
| Live redirect target == CSV target | **9 / 9** match — import faithful |
| Unique keeper targets resolve **200, zero chains** | **4 / 4** (`l-shape-desks`, `u-shape-desks`, `height-adjustable-tables`, `multi-person-workstations`) |
| HARD GATE (missing redirect → would 404) | **not tripped** (0 missing) |
| Sources that are do-not-touch ranking handles (of the 25) | **0** of 9 |
| Sources already unpublished | **0** |

Classification counts: `TO_UNPUBLISH=9`, `HALT=0`, `SKIP-*=0`.

### Inbound-link sanity (Phase 0)
- **Nav tiles clean:** `collection.desks.json` crosslink tile now points to keeper `/collections/l-shape-desks` (the [#83](https://github.com/leokatz97/officecentral/pull/83) repoint); `multi-person-workstations-desks` has **zero** theme references. Both formerly-dangling sibling tiles resolved.
- **One cosmetic residue (not a blocker, tracked below):** 10 landing-page sections reference `collections['height-adjustable-tables-desks'].products.first` as a *product-teaser data fallback* (not a link/href, no redirect hop, no 404). Each is immediately backstopped on the next line by a published keeper (`height-adjustable-tables` or `collections.desks`), so the teaser self-heals to the keeper post-unpublish.

## Phase 2 — execution + hardened readback
Script: `scripts/phase1-batch2-unpublish.py --live` → log `data/logs/batch2-unpublish-2026-06-02.json`
Each write: pre-state backup (`data/backups/batch2-unpub-<handle>-2026-06-02.json`) → PUT `published:false` → REST re-GET (`published_at` must be null) → cache-busted storefront curl (expect 301→keeper). **9/9 MATCH, 9/9 storefront 301 firing immediately (no edge-lag).**

### The 9 unpublished sources (by keeper family)
**L-shape (3) → `l-shape-desks`:** l-shape-desks-desks · l-shape-desks-1 · l-shape
**U-shape (2) → `u-shape-desks`:** u-shape-desks-1 · u-shape-desks-desks
**Height-adjustable (2) → `height-adjustable-tables`:** height-adjustable-tables-1 · height-adjustable-tables-desks
**Multi-person (2) → `multi-person-workstations`:** multi-person-workstations-1 · multi-person-workstations-desks

*(Overlap-verified in Phase 2 planning: siblings ≥86% subset of keeper. Straight-desks family was DROPPED — siblings 56–71% subset, +9 unique = genuinely distinct.)*

### Empirical self-heal confirmation (post-unpublish, cache-busted live render)
Per the readback addition for `height-adjustable-tables-desks` (the source with 10 data-fallback refs): rendered `/pages/relocation` cache-busted — its `tp1` fallback chain hits `height-adjustable-tables-desks` directly. The Top-products grid rendered **4 real product cards, 0 blank slots**; card 1 self-healed to a real height-adjustable product ("Electric height adjustable sit to stand desks", Heartwood, From $769.99, with image + href). STOP condition (any blank teaser) **not triggered** → safe to commit.

## Tracked follow-up (out of scope here — watcher-gated theme edit)
- **THEME-CLEANUP — repoint the 10 `height-adjustable-tables-desks` data fallbacks** directly to the keeper `height-adjustable-tables`, and drop the now-dead source line. Pure hygiene (the next-line keeper fallback already covers it). Affected files (line):
  - `theme/sections/ds-lp-relocation.liquid:275` (tp1)
  - `theme/sections/ds-lp-design-services.liquid:535` (tp1)
  - `theme/sections/ds-lp-delivery.liquid:314` (tp1)
  - `theme/sections/ds-lp-professional-services.liquid:477` (tp2)
  - `theme/sections/ds-lp-government.liquid:504` (tp2)
  - `theme/sections/ds-lp-education.liquid:514` (tp2)
  - `theme/sections/ds-lp-non-profit.liquid:508` (tp2)
  - `theme/sections/ds-lp-industries.liquid:853` (tp2)
  - `theme/sections/ds-lp-quote.liquid:692` (tp2)
  - `theme/sections/ds-lp-healthcare.liquid:547` (tp2)

## Phase 2 — now COMPLETE end-to-end
Both batches imported + activated:
- **Batch 1** (33 sources) — LIVE since the Day-20 follow-up (`collections-batch1-source-unpublish-2026-06-02.md`); keilhauer held.
- **Batch 2** (9 desk-family sources) — LIVE this session.

Carry-forward: keilhauer unpublish decision still open (Steve); the THEME-CLEANUP item above; Cowork strip to follow on merge.
