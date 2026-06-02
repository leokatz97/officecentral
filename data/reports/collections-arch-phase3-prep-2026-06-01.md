# COLLECTIONS-ARCHITECTURE — Phase 3 Prep: 25-handle verification + nav IA proposal

**Date:** 2026-06-01 · **Status:** ✅ READ-ONLY VERIFICATION + PLAN. **NO theme writes, NO redirect writes, NO Admin writes, NO commits this session.** · **Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`)

De-risking pass for the follow-on **watcher-gated theme session** (nav write + the dangling `collection.desks.json` 2-tile repoint + build-state PR). Output is a verification table, a Steve redirect-pull list, and a proposed nav IA. The actual nav write is the next session, where the SCHEMA-CRIT-1 preflight applies.

**Data sources (all live, this session):**
- **Ranks:** reused from the Phase 2 DataForSEO `ranked_keywords` pull (Canada, 2026-06-01) — not re-pulled.
- **Redirects:** live Admin API pull of all **1,660 URL redirects** (7 pages).
- **Counts + published state:** live GraphQL `productsCount` + REST `published_at` (token lacks `read_product_listings`, so `publishedOnCurrentPublication` unavailable — used REST `published_at` instead).
- **Live storefront:** throttled `curl` (4s spacing — Phase 2 hit 429s), HTTP code + redirect target.

---

## Grounding (3 lines)
- Phase 2 (build-state Day 19) locked 25 ranking handles as do-not-touch; `benching-desks → desks` was the one flagged self-redirect; `quiet-spaces` nav-hop + `buy-canadian`→Made-in-Canada + the desks.json 2-tile repoint are the Phase 3 carry-forwards.
- Collections-audit: nav exposes 9 collections; all 25 ranking handles are nav-orphans — organic authority lives outside the nav.
- This session re-pulled live redirects + counts + storefront status — the benching-desks self-redirect generalizes to **8 handles**, three newly surfaced.

---

## (1) The 25-handle verification table

| Handle | Rank | Prod | Pub | Live storefront | Class |
|---|---|---|---|---|---|
| bariatric-seating | 13 | 5 | Y | 200 | 🟢 PROMOTABLE |
| folding-stacking-chairs-carts | 15 | 7 | Y | 200 | 🟢 PROMOTABLE |
| nesting-chairs-chair | 18 | 5 | Y | 200 | 🟢 PROMOTABLE |
| gaming | 21 | 3 | Y | 200 | 🟢 PROMOTABLE (off-ICP — see note) |
| fire-resistant-file-cabinets-storage | 22 | 6 | Y | 200 | 🟢 PROMOTABLE |
| reception-desks-desks | 23 | 9 | Y | 200 | 🟢 PROMOTABLE (funnel) |
| recliners | 25 | 3 | Y | 200 | 🟢 PROMOTABLE |
| coffee-tables | 26 | 5 | Y | 200 | 🟢 PROMOTABLE |
| training-flip-top-tables | 26 | 5 | Y | 200 | 🟢 PROMOTABLE |
| bar-height-tables | 28 | 3 | Y | 200 | 🟢 PROMOTABLE |
| cafeteria-kitchen-tables | 29 | 4 | Y | 200 | 🟢 PROMOTABLE (high-vol) |
| pedestal-drawers-storage | 31 | 9 | Y | 200 | 🟢 PROMOTABLE |
| telephone-booths | 32 | 1 | Y | 200 | 🟢 PROMOTABLE |
| lecterns-podiums | 35 | 5 | Y | 200 | 🟢 PROMOTABLE |
| desk-top-dividers | 38 | 4 | Y | 200 | 🟢 PROMOTABLE |
| fire-resistant-safes-storage | 48 | 11 | Y | 200 | 🟢 PROMOTABLE |
| **boardroom-conference-meeting** | 22 | 13 | **Y** | **200** (dormant redirect→boardroom) | 🟡 SPECIAL — see below |
| **coat-racks-accessories** | 34 | 2 | N | **301→storage** | 🟠 SELF-REDIRECTING |
| **modesty-panels** | 36 | 2 | N | **301→storage** | 🟠 SELF-REDIRECTING |
| **picnic-tables** | 48 | 1 | N | **301→tables** | 🟠 SELF-REDIRECTING |
| **benching-desks** | 72 | 1 | N | **301→desks** | 🟠 SELF-REDIRECTING (known) |
| keilhauer | 15 | **0** | Y | 200 (empty smart) | 🔴 NOT-READY (queued →/pages/brands-keilhauer) |
| book-displays-storage | 38 | **0** | N | 301→business-furniture | 🔴 NOT-READY (empty, already 301'd) |
| healthcare | 43 | 1 | N | 301→business-furniture | 🔴 NOT-READY (funnel; /pages/healthcare owns it) |
| laboratory-furniture | 83 | **0** | N | 301→business-furniture | 🔴 NOT-READY (empty, already 301'd) |

### 🔑 Key generalization + correction to the Phase 2 record
The benching-desks self-redirect is **not a one-off — 8 ranking handles sit as redirect SOURCES in the live map**, three newly surfaced this session: `coat-racks-accessories`, `modesty-panels`, `picnic-tables`. Each forfeits its rank to a nav parent.

**De-risking insight for the nav write — Shopify URL redirects are DORMANT while the collection is published; they only fire once unpublished.** Proof from this pull:
- `boardroom-conference-meeting`: redirect entry → `boardroom`, **published**, serves **200 live** (redirect inert).
- All 7 other self-redirectors: **unpublished**, serve **301 live** (redirect active).

Consequence: **promoting a self-redirecting collection to nav = republish it (redirect auto-goes dormant) AND delete the stale redirect entry.** A nav link added without republishing would 301-hop.

**Second consequence — the landing-refresh `boardroom-conference-meeting → boardroom` migration is incomplete.** The redirect was imported but is dormant because the collection is still published — both `boardroom-conference-meeting` (#22, 13 products) and the optimized nav `boardroom` serve 200. The cannibalization it was meant to fix is still live.

---

## (2) Promotable vs self-redirecting vs not-ready split
- **🟢 PROMOTABLE — 16 handles** (200, published, products>0): ready for nav today, no Steve action.
- **🟠 SELF-REDIRECTING — 4 handles with products** (`coat-racks-accessories`, `modesty-panels`, `picnic-tables`, `benching-desks`): rescuable, but Steve must **republish + pull the redirect** first. All low-count (1–2) → marginal nav value; better as internal links unless repopulated.
- **🟡 SPECIAL — 1 handle** (`boardroom-conference-meeting`): published+200 with dormant redirect; nav already exposes canonical `boardroom` → **do not add to nav**; resolve as cannibalization cleanup.
- **🔴 NOT-READY — 4 handles**: `keilhauer` (empty, queued for its own redirect), `book-displays-storage` + `laboratory-furniture` (empty, correctly already redirected — *repopulate, never pull*), `healthcare` (funnel page owns the term). Excluded from nav.

---

## (3) Proposed nav IA — promotable handles under existing nav parents
Lowest-risk structure: nest orphans **under the 8 published nav-parent smart collections** as dropdown/mega-menu children (no new top-level parents). Anchor optimized to the ranking keyword — **bold = label differs from current collection title**.

| Nav parent | Promotable handle | Proposed anchor | Note |
|---|---|---|---|
| **Seating** | bariatric-seating | Bariatric Seating | title=label; healthcare-relevant |
| | folding-stacking-chairs-carts | **Folding & Stacking Chairs** | drop "Carts" |
| | nesting-chairs-chair | **Nesting Chairs** | drop "(Chair)"; KW *nesting chair 1,600* — top-vol orphan |
| | recliners | Recliners | healthcare/patient-recliner relevant |
| | gaming | **Gaming Chairs** | ranks 6-kw but **off-ICP for B2B institutional** → footer/internal-link, not primary nav |
| **Desks** | reception-desks-desks | **Reception Desks** | drop "(Desks)"; funnel — also a landing page |
| **Tables** | training-flip-top-tables | Training / Flip-Top Tables | KW flip top tables |
| | bar-height-tables | **Bar-Height Tables** | drop "(Tables)" |
| | coffee-tables | Coffee Tables | title=label |
| | cafeteria-kitchen-tables | **Cafeteria Tables** | drop "/ Kitchen"; **KW cafeteria tables canada 4,400 + cafeteria tables 880 — highest-value orphan** |
| **Storage** | fire-resistant-file-cabinets-storage | **Fireproof File Cabinets** | KW fireproof cabinets 320, 8-kw cluster |
| | fire-resistant-safes-storage | **Fireproof Safes** | KW fire safe cabinet |
| | pedestal-drawers-storage | **Pedestals & Drawers** | drop "(Storage)"; KW drawer pedestal |
| **Panels / Room Dividers** | desk-top-dividers | **Desk-Top Dividers** | KW office desk divider |
| **Boardroom** | lecterns-podiums | Lecterns & Podiums | KW podiums and lecterns |
| **Quiet Spaces** ⚠ | telephone-booths | **Phone Booths** | KW buy phone booth; **parent currently broken — park under Accessories until Quiet Spaces is rebuilt** |

**Filter tie-in (which promotable collections carry Brand / Made-in-Canada once built):**
- **Brand filter (vendor=X) — multi-vendor collections:** `pedestal-drawers-storage` (4 vendors), `nesting-chairs-chair` (3), `cafeteria-kitchen-tables` (2), seating cluster. **Not useful** on `fire-resistant-file-cabinets-storage` (single-vendor Gardex).
- **Made-in-Canada filter — broad:** storage/seating/tables skew Canadian (Gardex=Burlington ON, Global, Heartwood, Teknion, Tayco) → strong Canadian-Owned story (add maple-leaf accent per brand rules).

⚠ **Nav-parent blocker:** `/collections/quiet-spaces` is a **live nav item but unpublished + 301→accessories** (confirmed live). Its nav link currently hops. `telephone-booths` can only nest under it once Quiet Spaces is rebuilt (`acoustic-pods`/`focus-rooms` candidates). Until then, park `telephone-booths` under **Accessories**.

---

## (4) Steve redirect-pull list (Admin → Navigation → URL Redirects → delete)
Pulling the redirect is necessary but **not sufficient — the collection must also be republished** (the unpublished state is what makes the redirect fire).

| Delete redirect | Republish? | Rationale |
|---|---|---|
| `benching-desks → desks` | Yes | Reclaims #72; collection has its own product. Known carry-forward. |
| `coat-racks-accessories → storage` | Yes | **Newly surfaced.** Reclaims #34 (coat rack industrial); 2 products. |
| `modesty-panels → storage` | Yes | **Newly surfaced.** Reclaims #36 (modesty panel, 260 vol); 2 products. |
| `picnic-tables → tables` | Yes | **Newly surfaced.** Reclaims #48; 1 product (marginal). |
| `executive-desks → desks` | n/a (build) | **Leo-confirmed.** Temp redirect — pulling unblocks the deferred exec-desks build. |

**Explicitly NOT on the pull list:** `book-displays-storage`, `laboratory-furniture` (empty → repopulate, never pull); `healthcare` (funnel, `/pages/healthcare` owns the term); `keilhauer` (queued *for* a redirect, opposite direction); `boardroom-conference-meeting` (dormant redirect, published — pulling does nothing live; cannibalization decision).

---

## (5) Filter-readiness note (for the eventual filter build — not now)
- **Brand filter:** ✅ Ready. Vendor populated post-Phase-1 dedup (43→35). Caveat: 225 `vendor=BBI` data-errors remain (enrichment carry-forward) — show as "Brant Business Interiors" in the filter (e.g. 6/9 in reception-desks-desks); dedup before shipping.
- **Made-in-Canada filter:** ⚠ Viable, vendor-derived preferred. `country_of_manufacture` coverage ~40–50% (Phase 1 specs density 49.8%, country=265) — thin alone; best sourced from a vendor→country map (Gardex/Global/Heartwood/Teknion/Tayco = Canadian). `buy-canadian` is the intended Made-in-Canada handle — confirmed **HELD, no redirect entry** (serves 200 empty), ready to populate via a smart `country_of_manufacture=Canada` ∪ vendor∈Canadian rule.

---

## Carry-forward decisions (to the reconciliation/nav sessions)
1. **Gaming in primary nav?** Data says promotable (6-kw cluster) but off-ICP for institutional B2B → recommend footer/internal-link.
2. **boardroom-conference-meeting** — complete the migration (unpublish → activates the dormant redirect to optimized `boardroom`) or keep it as canonical and drop the redirect? Both pages serve 200 today (live cannibalization).

**HALT — verification + IA staged. No theme writes, no redirect writes, no Admin writes, no commits. The reconciliation session's PR will commit this file alongside its own provenance.**
