# COLLECTIONS-ARCHITECTURE — Publish-State Reconciliation (Admin-API publish toggles)

**Date:** 2026-06-02 (Day 20) · **Status:** ✅ EXECUTED + HARDENED-READBACK CLEAN · **Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`)

**Scope:** Admin-API **publish toggles only** — theme-independent, NO theme writes (so no watcher gate), NO redirect writes, NO Admin redirect/menu writes. Dry-run → HALT → approval → live writes with per-item hardened readback, per BBI hard rules.

**This session activates the dormant redirect folds and rescues the ranking collections that were bleeding rank to a parent** — the gap surfaced by the 2026-06-01 Phase-3-prep verification (`data/reports/collections-arch-phase3-prep-2026-06-01.md`).

---

## The locked learning — Shopify URL redirects are DORMANT while the source is published

A Shopify URL redirect for `/collections/<h>` **does not fire while collection `<h>` is published** — the live collection wins and serves 200; the redirect is inert. It only fires once the collection is **unpublished**. Consequence:

- **To fold a collection** (consolidate it away): the redirect entry must exist **AND** the source must be unpublished. A redirect imported against a still-published source is dormant — the consolidation silently never happens.
- **To rescue a self-redirecting collection** (reclaim its rank): **republish it** — the existing redirect auto-goes dormant, the collection serves its own 200 again, and rank returns. (Deleting the now-dormant redirect entry is hygiene, not functionally required.)

This explains two stalled migrations: the Day-19 `boardroom-conference-meeting → boardroom` 301 was imported but dormant (bc-m still published → both served 200, cannibalization never fixed), and 4 ranking collections sat unpublished+redirected with rank bleeding to a nav parent.

---

## Phase 0 — publish-state map (live reads, 2026-06-02)

1,660 redirect entries pulled · 391 collections indexed · throttled storefront curl (4s spacing) · GraphQL `productsCount` · REST `published_at`.

| Handle | Pub | Prod | Redirect entry | Live storefront | Class |
|---|---|---|---|---|---|
| benching-desks | N | 1 | →desks | 301 (firing) | 🟠 RESCUE |
| coat-racks-accessories | N | 2 | →storage | 301 (firing) | 🟠 RESCUE |
| modesty-panels | N | 2 | →storage | 301 (firing) | 🟠 RESCUE |
| picnic-tables | N | 1 | →tables | 301 (firing) | 🟠 RESCUE |
| reception | **Y** | 3 | →reception-desks-desks | 200 (dormant) | 🟢 FOLD |
| healthcare-seating | N | 0 | →/pages/healthcare | 301 (firing) | ✅ ALREADY DONE |
| boardroom-conference-meeting | Y | 13 | →boardroom | 200 (dormant) | 🟡 RESOLVE |
| keilhauer | Y | 0 | *(none)* | 200 (empty) | 🔵 HOLD |
| executive-desks | N | 0 | →desks | 301 (firing) | (Steve build-unblock) |

All fold/rescue targets verified live **200, no chain**: reception-desks-desks, boardroom, desks, storage, tables, /pages/healthcare, + the nav parents.

**Two corrections vs the 2026-06-01 prep report:**
1. **healthcare-seating was already unpublished + firing 301** → /pages/healthcare (completed in the Day-19 landing-refresh session). Part B reduced to **reception only**. No write needed.
2. **All 34 Phase-2 batch-1 sources are published with NO redirect entry yet** — Steve has not imported `collections-phase2-batch1-301s.csv`. (keilhauer's →/pages/brands-keilhauer is in that CSV, also not yet live — consistent with HOLD.)

---

## Phase 2 — writes executed (Admin-API publish toggles, hardened readback)

Source: `scripts/phase1-publish-toggles.py --live` · log: `data/logs/publish-toggles-20260602.json` · pre-state backups in `data/backups/collection-<h>-pre-publish-20260602.json`.

### A — RESCUE (publish=true): republish → existing 301 goes dormant → serves 200 → reclaims rank

| Collection | id | Reclaims | REST readback | Storefront (cache-busted) |
|---|---|---|---|---|
| benching-desks | 473196101945 | #72 | published ✓ | 200 (own content) ✓ |
| coat-racks-accessories | 473354797369 | #34 (coat rack industrial) | published ✓ | 200 (own content) ✓ |
| modesty-panels | 495571730745 | #36 (modesty panel, 260 vol) | published ✓ | 200 (own content) ✓ |
| picnic-tables | 476855599417 | #48 | published ✓ | 200 (own content) ✓ |

*Flag for follow-up:* all thin (1–2 products) — this reclaims the rank, it does not nav-promote them. **Repopulate + internal-link later.** Their now-dormant redirect entries can be deleted as hygiene (Steve list #4).

### B — ACTIVATE fold (publish=false): unpublish → existing 301 fires → completes the Day-19 intent

| Collection | id | Folds into | REST readback | Storefront (cache-busted) |
|---|---|---|---|---|
| reception | 476571271481 | reception-desks-desks (#23 canonical) | unpublished ✓ | **301 → reception-desks-desks** ✓ |

**Guard cleared:** reception was published ✓, redirect present ✓, **not** a protected ranker (the ranker is `reception-desks-desks` #23). Its 3 products (`circular-reception-unit-w-41-r`, `links-custom-reception-unit-60x72`, `reception-unit-72x72`) are a **clean subset** of the canonical's 9 — the fold orphans no product. (The first cache-busted curl returned a stale 200; subsequent tries returned 301 — edge-cache lag, not a write failure. REST `published_at=null` is the authoritative gate.)

### C — boardroom RESOLVE = KEEP-CANONICAL (decided this session; no CC write)

| | Rank | Products | State |
|---|---|---|---|
| boardroom-conference-meeting | **#22** ("modular boardroom tables", vol 70 — BBI ranked-keywords 2026-05-30) | 13 | published, dormant redirect→boardroom |
| nav `boardroom` | **no captured organic rank** | — | published, 200 |

**Decision (Leo, 2026-06-02): keep bc-m as the ranking canonical.** You don't fold a #22 / 13-product ranker into a rank-less collection. → **Steve drops the `bc-m → boardroom` redirect** (Steve list #3 — no CC write). The dormant redirect does nothing live today, but removing it prevents a future accidental fold.

---

## HOLD — keilhauer (no write)

Published, empty (0 products), no redirect entry yet, serves empty 200. Published = empty 200; unpublished (after its batch-1 redirect imports) = routes #15 to `/pages/brands-keilhauer`. Empty either way → **Steve's call, not urgent.** Decision pending.

---

## D — GATED follow-up (documented, NOT written)

The batch-1 source-unpublish can only run **after** Steve imports `collections-phase2-batch1-301s.csv` — unpublishing before the redirect exists would 404. Even after import, the dormant-redirect mechanic means each source must still be **unpublished** for its fold to fire. Post-import, these **33 published sources** need unpublishing (keilhauer excluded — separate HOLD):

`acoustic-panels, active-seating, beam-seating, bench-seating, boardroom-seating, boardroom-storage, conference-seating, ergonomic-accessories, executive-seating, high-density-storage, mobile-storage, personal-storage, privacy-screens, wall-storage, type-chairs, type-desks, type-tables, type-storage, type-accessories, type-lounge, type-outdoor, room-boardroom, room-reception, room-accessories, room-private-office, room-open-plan, room-lounge, room-training-room, pedestal-drawers, pedestal-drawers-1, fire-resistant-file-cabinets, fire-resistant-file-cabinets-safes, fire-resistant-safes`

Trigger: Steve imports batch-1 → pings Leo → run `scripts/phase1-publish-toggles.py` extended with these handles (unpublish), same dry-run → readback discipline.

---

## Steve action list (parallel)

1. **Import `collections-phase2-batch1-301s.csv`**, then ping Leo → triggers the gated batch-1 source-unpublish (section D).
2. **Delete the `executive-desks → desks` redirect** — unblocks the deferred exec-desks build.
3. **Delete the `boardroom-conference-meeting → boardroom` redirect** (keep-canonical decision).
4. **Hygiene (low priority):** after the 4 rescues, delete the now-dormant redirect entries for `benching-desks` / `coat-racks-accessories` / `modesty-panels` / `picnic-tables`.

---

## Provenance

- `scripts/phase0-publish-state-recon.py` → `data/reports/phase0-publish-state-2026-06-02.json` (read map)
- `scripts/phase1-publish-toggles.py` → `data/logs/publish-toggles-20260602.json` (write log) + `data/backups/collection-*-pre-publish-20260602.json` (pre-state)
- Rank source: `data/reports/keyword-research/ranked-keywords-bbi-2026-05-30.csv`
- Companion: `data/reports/collections-arch-phase3-prep-2026-06-01.md` (the verification that surfaced the gap)
