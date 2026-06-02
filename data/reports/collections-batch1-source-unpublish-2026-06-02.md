# Collections Phase 2 — Batch-1 Source-Unpublish (provenance) — 2026-06-02

**Status:** ✅ LIVE — batch-1 consolidation now firing. **Admin-API publish toggles only** — 0 theme writes, 0 redirect writes, 0 menu writes.
**The gated follow-up to Day-20** publish-state reconciliation: Steve imported `collections-phase2-batch1-301s.csv`, so the batch-1 redirects now exist; per the **dormant-redirect mechanic** they were inert while their sources stayed published. This session unpublished the published batch-1 sources so the redirects fire.

## Result
- **33 sources unpublished** → each now serves **301 → its target** (33/33 storefront 301 confirmed live, no edge-lag), REST `published_at=null` on all 33 (authoritative MATCH).
- **0 already-firing** (no source was pre-unpublished this round).
- **keilhauer EXCLUDED** — held per Steve's pending decision (also ranking handle #22, double-protected).
- **0 / 33** are ranking handles. **0** chains, **0** 404s.

## Phase 0 — verification + classification (read-only, the safety crux)
Script: `scripts/phase0-batch1-classify.py` → `data/reports/phase0-batch1-classify-2026-06-02.json`

| Gate | Result |
|---|---|
| Batch-1 redirects present in **live map** (Admin API, authoritative) | **34 / 34** — import landed fully |
| Live redirect target == CSV target | **34 / 34** match — import faithful |
| Unique targets resolve **200, zero chains** | **15 / 15** |
| HARD GATE (missing redirect → would 404) | **not tripped** (0 missing) |
| Sources that are do-not-touch ranking handles (of the 25) | **0** of 33 (keilhauer is the only batch-1 ranking handle → excluded) |
| Sources already unpublished | **0** |

Classification counts: `TO_UNPUBLISH=33`, `EXCLUDE(keilhauer)=1`, `HALT=0`, `SKIP-firing=0`.

## Phase 2 — execution + hardened readback
Script: `scripts/phase1-batch1-unpublish.py --live` → log `data/logs/batch1-unpublish-2026-06-02.json`
Each write: pre-state backup (`data/backups/batch1-unpub-<handle>-2026-06-02.json`) → PUT `published:false` → REST re-GET (`published_at` must be null) → cache-busted storefront curl (expect 301→target). **33/33 MATCH.**

### The 33 unpublished sources (by batch)
**Batch B — scaffold empties → nav parent (14):** acoustic-panels→panels-room-dividers · active-seating→ergonomic-products · beam-seating→seating · bench-seating→seating · boardroom-seating→boardroom · boardroom-storage→boardroom · conference-seating→boardroom · ergonomic-accessories→ergonomic-products · executive-seating→seating · high-density-storage→storage · mobile-storage→storage · personal-storage→storage · privacy-screens→panels-room-dividers · wall-storage→storage

**Batch C1 — type-*/room-* smart dupes → nav twin (14):** type-chairs→seating · type-desks→desks · type-tables→tables · type-storage→storage · type-accessories→accessories · type-lounge→seating · type-outdoor→business-furniture · room-boardroom→boardroom · room-reception→reception-desks-desks · room-accessories→accessories · room-private-office→desks · room-open-plan→desks · room-lounge→seating · room-training-room→training-flip-top-tables

**Batch C2 — legacy dupe families → ranking keeper (5):** pedestal-drawers→pedestal-drawers-storage · pedestal-drawers-1→pedestal-drawers-storage · fire-resistant-file-cabinets→fire-resistant-file-cabinets-storage · fire-resistant-file-cabinets-safes→fire-resistant-file-cabinets-storage · fire-resistant-safes→fire-resistant-safes-storage
*(sources are the non-`-storage` dupes; the `-storage` targets are the ranking keepers — authority accumulates into the rankers.)*

## Excluded / held
- **keilhauer** (`/collections/keilhauer` → `/pages/brands-keilhauer`, Batch D) — redirect imported and live, but source left **published** per Steve's pending decision. Will fire only when Steve approves unpublishing it. (Ranking handle #22 — do-not-touch by default.)

## Carry-forward (unchanged from Day-20 Steve list)
- Batch 2 (desk families, 9 rows) remains **gated on a theme repoint deploy** — not part of this session.
- keilhauer unpublish decision still open.
