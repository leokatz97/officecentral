# COLLECTIONS-ARCHITECTURE — Phase 3: Nav Promotion + desks.json Repoint + Quiet Spaces Nav-Hop Fix

**Date:** 2026-06-02 · **Status:** ✅ EXECUTED — first theme write since Surface B · **Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`) · **Branch:** `feature/collections-phase3-nav-promotion-desks-repoint-2026-06-02` · **PR:** OPEN, not merged

The Phase-3 payoff from the Phase-3-prep verification (`collections-arch-phase3-prep-2026-06-01.md`): surface the 16 promotable ranking collections, repoint the 2 dangling `desks.json` tiles (unblocks batch-2), and fix the broken Quiet Spaces nav-hop. **Theme write — watcher-gated.**

---

## Preflight (SCHEMA-CRIT-1) — PASS
- **No `shopify theme dev` watcher** running (none bound to role=main `186373570873` or any theme); no dev listeners on 9292/8080/3000. Nothing to kill.
- **Live theme role re-confirmed `main`** by Admin-API readback (name "BBI Landing Dev" is historical; role is authoritative). Re-checked immediately before the PUT loop.
- All 10 target files backed up to `data/backups/phase3-theme-2026-06-02/` (gitignored) before any edit.

## Phase 0 — write-mechanism determination (the key finding)
- **Nav is HARDCODED in theme files, NOT a Shopify Navigation linklist.** Live chrome = `snippets/bbi-nav.liquid` (header) + `snippets/bbi-footer.liquid`, rendered on every customer surface via the `bbi_landing` gate in `layout/theme.liquid`. The legacy Starlite `header.liquid` + `linklists['main-menu']` nav exists in the tree but is gated off — never customer-facing.
- **Consequence:** nav promotion is a **CC theme write**. No Shopify `navigation`/`write_content` token scope is involved (the redirect-scope gap is irrelevant here). NOT a Steve-Admin task.
- **"Quiet Spaces" was never in the actual header.** `bbi-nav`'s Shop dropdown is a flat 8-item list; the footer mirrors those 8. The "9 collections the nav exposes" / the broken Quiet Spaces "nav item" = the **9-card "Browse by category" grid** (card #08), present in `sections/ds-lp-industries.liquid` (Industries Hub) and the shared `snippets/ds-browse-faq.liquid` (5 spoke pages). Both linked `/collections/quiet-spaces`, which **301-hopped → /collections/accessories** (confirmed live).
- **Live re-verify (pre-byte-write, throttled 4s):** 16 promotable handles all **200**; desks repoint targets `height-adjustable-tables` + `multi-person-workstations` **200**; old `-desks` sources still **200** (batch-2 not yet imported → repoint safe to land first); `quiet-spaces` **301 → accessories**.

## Decisions (Leo)
- **Nav mechanism = sub-collection tiles** (the proven `desks.json` pattern), NOT a mega-menu rebuild and NOT a flat-append to the header dropdown. Surfaces orphans contextually on their parent collection pages + passes internal link equity + auto-adds a filter chip with each sub-collection's product count, with zero global-header risk.
- **Quiet Spaces card = repoint → Phone Booths** (`/collections/telephone-booths`, live 200), relabel + refreshed desc. Fixes the hop AND surfaces the promotable orphan.
- **Tile labels kept keyword-anchored** (not softened) — they are distinct ranking handles.

---

## Writes executed (10 files, all PUT=200, all hardened-readback MATCH)

### A — desks.json repoint (2 tile links) — unblocks batch-2
| Block | Old link | New link |
|---|---|---|
| `tile-height-adjustable` | `/collections/height-adjustable-tables-desks` | `/collections/height-adjustable-tables` |
| `tile-computer` | `/collections/multi-person-workstations-desks` | `/collections/multi-person-workstations` |

### B — sub-collection tiles (14 new `tile` blocks across 6 parent templates; no image → graceful text placeholder)
| Template | New tiles (anchor → handle) |
|---|---|
| `collection.seating.json` | Bariatric Seating → `bariatric-seating` · Folding & Stacking Chairs → `folding-stacking-chairs-carts` · Nesting Chairs → `nesting-chairs-chair` · Recliners → `recliners` |
| `collection.tables.json` | Training / Flip-Top Tables → `training-flip-top-tables` · Bar-Height Tables → `bar-height-tables` · Coffee Tables → `coffee-tables` · Cafeteria Tables → `cafeteria-kitchen-tables` |
| `collection.storage.json` | Fireproof File Cabinets → `fire-resistant-file-cabinets-storage` · Fireproof Safes → `fire-resistant-safes-storage` · Pedestals & Drawers → `pedestal-drawers-storage` |
| `collection.boardroom.json` | Lecterns & Podiums → `lecterns-podiums` |
| `collection.panels-room-dividers.json` | Desk-Top Dividers → `desk-top-dividers` |
| `collection.accessories.json` | Phone Booths → `telephone-booths` |

- **Reception Desks** (`reception-desks-desks`, the Desks-parent promotable) was already a `desks.json` tile (`tile-reception`) — no new tile needed.
- **Gaming Chairs** (`gaming`, off-ICP per IA) → **footer Shop column link**, kept out of primary nav and out of the Seating tile grid.
- That accounts for all 16 promotable handles.

### C — Quiet Spaces nav-hop fix (2 card surfaces)
Card #08 repointed `/collections/quiet-spaces` → `/collections/telephone-booths`, relabel "Quiet Spaces" → "Phone Booths", desc → "Acoustic phone booths and focus pods for private calls in open-plan offices. No construction required." — in `sections/ds-lp-industries.liquid` + `snippets/ds-browse-faq.liquid`.

### D — Gaming → footer
`snippets/bbi-footer.liquid` Shop column: +1 link `Gaming Chairs → /collections/gaming`.

---

## Verification
- **Readback gate:** 7 JSON templates `json-parsed`-match=True, 3 `.liquid` byte-match=True. Pre-write role re-confirmed `main`.
- **theme-check:** none of the 10 files appear in the offense list — **0 new offenses** (baseline errors are all in legacy Starlite files, e.g. `header.liquid` schema-translation entries).
- **Live render (cache-busted):** seating/tables/storage/boardroom/panels/accessories grids show the new tiles; desks tiles point to `height-adjustable-tables` + `multi-person-workstations` (no `-desks`); `/pages/industries` + `/pages/healthcare` show the **Phone Booths** card → `telephone-booths` with no `quiet-spaces` leftover; footer shows **Gaming Chairs**. (JSON-template pages lag the edge cache briefly — accessories appeared on re-fetch; readback is the authoritative gate.)

## Confusing label pairs (NOTED per Leo, NOT fixed — all distinct ranking handles)
1. **Seating:** existing "Stacking & Training Chairs" (`stacking-seating`) vs new "Folding & Stacking Chairs" (`folding-stacking-chairs-carts`).
2. **Tables:** existing "Training & Folding Tables" (`training-room-tables`) vs new "Training / Flip-Top Tables" (`training-flip-top-tables`).
3. **Storage:** existing "Mobile Pedestals" (`mobile-pedestals`) vs new "Pedestals & Drawers" (`pedestal-drawers-storage`).
4. **Boardroom:** existing "Podiums & AV Furniture" (`podiums-av-furniture`) vs new "Lecterns & Podiums" (`lecterns-podiums`).

## Tracked follow-ups
- **IMAGE-GEN — 14 image-less tiles:** the 14 new tiles render a text placeholder (no `image` setting). Generate per-tile images (`bbi-coll-img-<parent>-tile-<key>-v*.jpg` convention, same as existing tiles) and add the `image` key to each block. Affects seating(4)/tables(4)/storage(3)/boardroom(1)/panels(1)/accessories(1).
- **Quiet Spaces rebuild:** when the `quiet-spaces` collection is rebuilt (acoustic-pods/focus-rooms candidates), revisit whether to restore a dedicated Quiet Spaces card and re-home telephone-booths under it.

---

## ⚠️ CRITICAL SEQUENCING — batch-2 desk-families import
`data/redirects/collections-phase2-batch2-deskfamilies-301s.csv` (9 rows) is gated on THIS repoint deploying. **Order:**
1. Merge this PR → theme live (the 2 desks tiles now point to the `-desks`-less keepers).
2. **THEN** Steve imports `collections-phase2-batch2-deskfamilies-301s.csv`.
3. **THEN** a batch-2 source-unpublish follow-up (same dormant-redirect mechanic as batch-1) unpublishes the 9 sources so the redirects fire.

**Never import batch-2 before this repoint is live** — the 2 tiles linked the `-desks` sources until this change; importing first would turn live tiles into redirect hops. (Now repointed, but the CSV still must wait for deploy to avoid the window where local≠live.)
