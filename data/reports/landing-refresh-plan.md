# LANDING-PAGE-THEME-CONTENT-REFRESH — Phase 0 Scope & Plan

**Date:** 2026-06-01 · **Status:** PLAN ONLY — no theme writes until approved
**Repo:** `leokatz97/officecentral` · **Live theme:** `186373570873` (role=`main`, verified via `GET /themes.json` — name "BBI Landing Dev" is historical)
**Source lock:** [`data/reference/priority-keywords.yaml`](../reference/priority-keywords.yaml) v1 (partial-lock) · [`docs/strategy/bbi-keyword-map-2026-05-31.md`](../../docs/strategy/bbi-keyword-map-2026-05-31.md)
**Rank baseline:** [`data/reports/rank-tracking/README.md`](rank-tracking/README.md) (2026-06-01 baseline summary; CSV gitignored)

---

## TL;DR — what this workstream actually is

The **SEO meta layer is already done.** Commit [#70](https://github.com/leokatz97/officecentral/pull/70) ("SEO meta on 7 live surfaces") set keyword-aligned `title_tag` + `description_tag` on the hub, both spokes, and the reception + boardroom collections. Verified live:

- design-services → `Office Space Planning | Brant Business Interiors` ✅
- healthcare → `Healthcare Furniture Canada | Brant Business Interiors` ✅
- professional-services → `Law Firm Office Furniture | Brant Business Interiors` ✅

**What is NOT done — and IS this workstream:** the *visible on-page body content* (H1, hero intro, FAQ, internal links) on those pages does **not** contain the locked primary keywords. The meta promises "office space planning" / "healthcare furniture canada" / "law firm office furniture"; the H1s say "free CAD floor plan", "Healthcare & Clinical Office Furniture", "Professional Services Office Furniture". This is a **theme write** (the copy lives in `ds-lp-*.liquid` + `page.*.json` template settings), which is why it's a separate, higher-risk session from the Admin-API catalog work.

Plus two surfaced gaps and one cannibalization problem (below) that should be folded in.

---

## Step 1 — Keyword-cluster lock state

| Cluster | Role | Primary KW | Lock |
|---|---|---|---|
| Design Services | Hub | `office space planning` | ✅ LOCKED |
| Professional Services | Spoke | `law firm office furniture` | ✅ LOCKED |
| Healthcare | Spoke | `healthcare furniture canada` | ✅ LOCKED |
| Reception | Funnel collection | `reception desk` | ✅ LOCKED |
| Executive Desks | Funnel collection | `executive desk` | ✅ LOCKED |
| Boardroom | Funnel collection | `boardroom table` | ✅ LOCKED |
| Waiting-Room Seating | Funnel collection | `office chairs for waiting room` | ✅ LOCKED |

**PENDING / UNLOCKED — do NOT plan on-page work against these** (walkthrough session 2, not yet run): `education-library`, `eastern-ontario-geo`, `brand-dealer`, `ergonomic-seating-desks-storage`. The YAML is `status: partial-lock` (4 of ~8 clusters). **All 7 pages above are fully locked** — the refresh is clear to plan. No partial-targeting risk on the in-scope pages.

---

## Step 2 — Priority landing-page inventory (current on-page state)

### Landing pages (theme Liquid — `ds-lp-*` sections + `page.*.json`)

| Page | Handle / URL | Template / section | Current H1 (on-page) | SEO title_tag (live) | Locked primary KW | On-page gap |
|---|---|---|---|---|---|---|
| **Design Services (hub)** | `design-services` (`/pages/design-services`) | `page.design-services.json` → `ds-lp-design-services` | "A free CAD floor plan for your office — no obligation." | `Office Space Planning \| BBI` ✅ | `office space planning` | H1/intro/FAQ have **zero** instances of "office space planning". Meta and H1 disagree. |
| **Professional Services (spoke)** | `professional-services` | `page.professional-services.json` → `ds-lp-professional-services` | "Professional Services Office Furniture for Ontario Firms" | `Law Firm Office Furniture \| BBI` ✅ | `law firm office furniture` | Exact phrase absent from H1/intro. "boardroom" present; "reception"/"executive desk" weak. FAQ hardcoded in `.liquid` (lines 636–711). |
| **Healthcare (spoke)** | `healthcare` | `page.healthcare.json` → `ds-lp-healthcare` | "Healthcare & Clinical Office Furniture for Ontario" | `Healthcare Furniture Canada \| BBI` ✅ | `healthcare furniture canada` | Exact phrase "healthcare furniture canada" absent from H1/intro. FAQ hardcoded in `.liquid` (lines 801–876). |

**Content-control note (verified):** H1 + hero intro on all three are `section.settings.* | default:` in the `.liquid`, **overridden by the `page.*.json` template settings**. So an H1/intro edit = a `page.*.json` template write (cheapest path). FAQ on Design Services is dynamic blocks; FAQ on Professional Services + Healthcare is **hardcoded `<details>` in the `.liquid`** → those FAQ edits require a section-file write.

### Funnel collections (the rank-baseline money targets)

| Target | YAML slug (NOT authoritative) | **Live reality** | SEO meta (live) | Rank baseline (2026-06-01) |
|---|---|---|---|---|
| **reception desk** (2,900/mo, KD0) | `/collections/reception-desks` ❌ doesn't exist | Two live: **`reception`** (id 476571271481, SEO-optimized → "Reception Desks") **and** `reception-desks-desks` (old, generic SEO) | `reception` ✅ optimized; `reception-desks-desks` ❌ generic | `reception desk` **NOT in top 100**. But `reception desk custom` #41 + `black reception desk` #36 rank on the **OLD** `reception-desks-desks`. |
| **executive desk** (1,300/mo, KD0) | `/collections/executive-desks` ✅ exists | **`executive-desks`** (id 526867005753) | ❌ **title_tag BLANK** — meta refresh missed this one | `executive desk` **NOT in top 100**. |
| **boardroom table** (880/mo) | `/collections/boardroom-conference-tables` ❌ doesn't exist | **`boardroom`** (id 526847443257, SEO-optimized) **plus** `boardroom-conference-meeting` + `meeting-conference-room-tables` (old, generic SEO) | `boardroom` ✅ optimized; others ❌ generic | `boardroom table` **#25**, `conference table` **#50**, `wood boardroom table` **#70**, `modular boardroom tables` #22 — all ranking on the **OLD** `boardroom-conference-meeting`. |
| **waiting-room / healthcare seating** | `/collections/waiting-room-seating` ❌ doesn't exist | **`healthcare-seating`** (id 526866874681) | ❌ **title_tag BLANK** | Healthcare cluster: 6 kw ranks **56–75**, all on `healthcare-seating`. |

**Baseline headline:** 9 of 42 locked keywords rank in the top 100. The two biggest-volume, easiest (KD0) terms — `reception desk` (2,900) and `executive desk` (1,300) — are absent from the top 100 entirely. That's the prize.

---

## Step 3 — Locked keyword → target page map (+ cannibalization & slug gaps)

**One primary per page (clean — no two pages chase the same term):**

```
office space planning      -> /pages/design-services        (hub)
law firm office furniture  -> /pages/professional-services   (spoke)
healthcare furniture canada-> /pages/healthcare              (spoke)
reception desk             -> /collections/reception         (funnel)   ⚠ dupe collection
executive desk             -> /collections/executive-desks   (funnel)
boardroom table            -> /collections/boardroom         (funnel)   ⚠ dupe collection
office chairs for waiting  -> /collections/healthcare-seating(funnel)
```

### 🔴 Cannibalization (the #1 issue to resolve before/with the refresh)
The #70 SEO pass optimized **newly-created** collections (`reception`, `boardroom`), but BBI's **existing organic ranks sit on the OLD collections** it didn't touch:
- `reception` (optimized, **0 ranks**) vs `reception-desks-desks` (generic meta, **ranks #36/#41**)
- `boardroom` (optimized, **0 ranks**) vs `boardroom-conference-meeting` (generic meta, **ranks #22/#25/#50/#70**)

Two collections per head term split authority and confuse Google. **Decision needed:** pick one canonical collection per term, point internal links + the better SEO meta + product membership there, and **301-redirect** the loser (or `canonical`-tag it). My recommendation: **keep the collection that already ranks** (the old `-conference-meeting` / `-desks-desks` ones) as canonical and migrate the optimized meta onto it — ranking authority is harder to win than a meta edit. (Final call is Steve's — flag in approval.)

### Slug gaps
The v1 YAML slugs `reception-desks`, `boardroom-conference-tables`, `waiting-room-seating` **do not exist live** (already warned in the keyword-map "SHOPIFY-CONTENT-MODEL-NOT-UNIFORM" lesson). Plan uses the verified live handles above. The YAML should be reconciled to live handles (small doc fix, note for write phase).

### Locked KW with no clean page home
- `office chairs for waiting room` / `waiting room chairs canada` → no dedicated collection; lands on `healthcare-seating`. Acceptable (low volume, 140/70). No new page needed now.

---

## Step 4 — Cross-link opportunity (compounds the on-page work; pre-stages blog internal-linking)

The **85 Block-4-enriched Global-family PDPs** (GFG desks / seating / tables / storage, now with real body copy) are the internal-link fuel. Today the 3 landing pages link only to **generic** collections (`/collections/seating`, `/collections/desks`, `/collections/tables`, `/collections/business-furniture`) — they do **not** link to the keyword-target funnel collections.

**Proposed link graph (bidirectional):**

| From | To (keyword-anchored) | Anchor text |
|---|---|---|
| Professional Services page | `/collections/executive-desks` · `/collections/boardroom` · `/collections/reception` | "executive desks", "boardroom tables", "reception desks" |
| Healthcare page | `/collections/healthcare-seating` · `/collections/reception` | "waiting room seating", "clinic reception desks" |
| Design Services hub | both spokes (`/pages/professional-services`, `/pages/healthcare`) + funnel collections | vertical design anchors |
| Enriched executive-desk PDPs | ↑ `/collections/executive-desks` + `/pages/professional-services` | breadcrumb + "see all executive desks" |
| Enriched boardroom/conf-table PDPs | ↑ `/collections/boardroom` + `/pages/professional-services` | "more boardroom tables" |
| Enriched reception-desk PDPs | ↑ `/collections/reception` + both spokes | "reception desks for offices & clinics" |

This is the single biggest compounding lever for `reception desk` / `executive desk` (collections with thin internal links currently rank nowhere). **Whichever collection wins the cannibalization decision is the link target** — don't wire links until that's settled.

---

## Step 5 — Per-page refresh plan (ranked by rank-baseline opportunity)

> Ranking logic: volume × winnability (KD0) × current-gap. Collections with fat absent head terms rank highest; the low-volume hub ranks lowest (still worth aligning for meta/H1 consistency).

### P0 — Executive Desks collection — `executive desk` (1,300/mo, KD0, rank: none)
- **Admin-API (not theme):** fill the **blank** `title_tag` → `Executive Desks | Brant Business Interiors`; write a keyword-led `description_tag`; write/expand `collection.description` body (renders only if on a description-rendering template — verify template before writing).
- **Theme:** add keyword-anchored links into this collection from Professional Services page + enriched executive-desk PDPs.
- **Why P0:** highest winnable volume with the cheapest fix (a blank meta field + internal links).

### P0 — Reception collection — `reception desk` (2,900/mo, KD0, rank: none on canonical)
- **First:** resolve cannibalization (`reception` vs `reception-desks-desks`). Consolidate to one canonical; redirect the other.
- **Admin-API:** ensure canonical has optimized meta + a keyword-led `collection.description`.
- **Theme:** internal links from both spokes + enriched reception PDPs → canonical reception collection.
- **Why P0:** biggest volume in the whole map; currently leaking authority across two URLs.

### P1 — Boardroom collection — `boardroom table` (880) / `conference table` (720)
- **First:** resolve cannibalization (`boardroom` vs `boardroom-conference-meeting`). Keep the ranking one canonical.
- **Theme:** Professional Services already links to `/collections/boardroom` — re-point to canonical; add enriched conf-table PDP links.
- **Why P1:** already ranks #22–#50, so on-page + link work pushes existing positions up rather than starting from zero.

### P2 — Healthcare page — `healthcare furniture canada` (ranks 56–75 on healthcare-seating)
- **Theme (`page.healthcare.json` + section):** work the exact phrase "healthcare furniture canada" into H1 / hero intro (currently "Healthcare & Clinical Office Furniture for Ontario"). Keep the locked **private-clinic-first** tone (per `feedback_healthcare_tone`) — lead clinics, OECM as trust signal, not hero.
- **Theme:** rework one hardcoded FAQ `<details>` to target the phrase; add keyword links to `healthcare-seating` + reception.
- **Admin-API:** fill blank `healthcare-seating` collection meta.

### P2 — Professional Services page — `law firm office furniture` (low vol, conversion play)
- **Theme (`page.professional-services.json` + section):** surface "law firm office furniture" in H1/intro; add the executive-desks / boardroom / reception funnel links with keyword anchors (currently links to generic `/collections/seating` etc.).
- **Why P2:** thin head-term volume — value is the funnel links it sends to the P0/P1 collections, not its own ranking.

### P3 — Design Services hub — `office space planning` (~400/mo, near-zero competition)
- **Theme (`page.design-services.json`):** the H1 "A free CAD floor plan…" is a strong conversion hook but contains zero instances of the locked primary. Propose working "office space planning" into the H1 or the immediately-following H2/intro so the visible page matches the meta. Keep the "free CAD floor plan / no obligation" hook + locked `Get My Free Layout →` microcopy.
- **Theme:** add spoke cross-links (to professional-services + healthcare) per the hub-and-spoke architecture.
- **Why P3:** low volume + already near-zero competition, so meta alone may already win it; on-page alignment is consistency insurance.

### Approval format
Reply per row: `✅ approve` · `⚠️ adjust {page/change}` · `❌ skip {page}`. Two cross-cutting decisions also need a call: **(A)** cannibalization — which collection is canonical for reception & boardroom (my rec: keep the already-ranking old ones); **(B)** whether the executive-desks/healthcare-seating blank-meta fills happen in this theme session or a separate Admin-API task.

---

## Step 6 — Write-phase preflight (NOT executed this session)

The follow-up execution session is a **THEME WRITE** to the live theme `186373570873` (role=`main`). Before any approval-gated PUT it is **mandatory** to:

1. **Verify role, not name** — re-run `GET /themes.json` and confirm `186373570873` is still `role: main` (the "Dev" in its name is historical). Ref: `feedback_push_target`.
2. **Kill any `shopify theme dev` watcher** bound to the live theme first — a running watcher auto-pushes local edits and silently bypasses the approval gate (the 2026-05-27 SCHEMA-CRIT-1 incident). Ref: `feedback_preflight_watcher_check`.
3. **Verify every PUT via Admin-API readback** — `push-file.py` dies silently on an unset `SHOPIFY_TOKEN`; edge serves stale full-page cache. A deploy is not "verified" without a byte-level Admin-API asset readback. Refs: `feedback_silent_put_failure`, `feedback_curl_vs_admin_api_verification`.
4. Note the split surface: H1/intro = `page.*.json` template writes; Pro-Services + Healthcare FAQ = `.liquid` section writes; collection meta/description = Admin-API (not theme). These are different files/tools — sequence accordingly.

**Understood: this gates the follow-up session. No theme writes occur until the plan above is approved.**

---

## Phase 0.5 — D1 Soundness-Gate Findings (2026-06-01, pre-write) 🔴 STOP

Per D1 ("confirm old collections are structurally sound, not just ranking") I queried live structure before any migration. **Three approved premises are invalidated — writes halted pending decisions.**

| Collection | Type | Published | Template | Products | Verdict |
|---|---|---|---|---|---|
| `reception` (optimized) | custom | ✅ global | base | **3** | dupe — 301 candidate |
| `reception-desks-desks` (ranks #36/#41) | custom | ✅ global | base | **9** | ✅ **sound** — more products + ranks → keep canonical |
| `boardroom` (optimized) | smart | ✅ web | **boardroom** (dedicated) | **25** | bigger + better template |
| `boardroom-conference-meeting` (ranks #22/#25/#50/#70) | custom | ✅ global | base | **13** | ⚠️ ranks but smaller + generic template |
| `executive-desks` (D2 "cheap win") | custom | ❌ **UNPUBLISHED** | base | **0** | 🔴 **empty + not live** |
| `healthcare-seating` (D2/P2 meta fill) | custom | ✅ web | base | **0** | 🔴 **empty** |

**Findings:**
1. 🔴 **executive-desks is unpublished AND empty (0 products).** D2's "cheapest win" is void — filling `title_tag` on an unpublished, empty collection does nothing for `executive desk` (1,300/mo). The term has **no viable landing page** right now. Needs products + publish first, or a different canonical (e.g. `/collections/desks`).
2. 🔴 **healthcare-seating is empty (0 products).** Filling meta on an empty page risks a thin-content signal. Also: the independent 2026-05-30 ranked CSV shows healthcare terms rank on **`/collections/healthcare`** (`furniture healthcare` #48), **not** healthcare-seating — the README baseline's "healthcare-seating" attribution looks wrong. Target URL for the healthcare funnel needs reconfirming.
3. ✅ **Reception is clean:** `reception-desks-desks` (9 products, published, ranks) is the sound canonical; `reception` (3 products) → 301 to it. Safe to execute as approved.
4. ⚠️ **Boardroom canonical is a genuine trade-off:** the *ranking* collection (`boardroom-conference-meeting`, 13 products, generic `base` template) vs the *optimized* one (`boardroom`, 25 products, dedicated `boardroom` template). "Keep the ranking one" sacrifices 12 products + a better template. Needs an explicit call — not a clean apply of the D1 heuristic.

**Redirect mechanism:** per the COLLECTION-CLEANUP-APPLY precedent (and the token's missing `write_content` scope for redirects), 301s are delivered as a **CSV for manual Shopify-Admin import**, not POSTed via API. No test redirect was created on the live store.

**No writes executed at gate time. Decisions received → Surface A execution below.**

---

## Phase 0.6 — Surface A execution log (2026-06-01)

**Decisions:** Q1 exec-desks = pending (analysis requested) · Q2 healthcare = use `/collections/healthcare` · Q3 boardroom = keep optimized `boardroom` · Q4 = execute reception now.

| Action | Surface | Status |
|---|---|---|
| Backup all 5 collection metas | Admin-API | ✅ `data/backups/landing-refresh-meta-backup-20260601.json` |
| Migrate optimized reception meta → `reception-desks-desks` (canonical) | Admin-API | ✅ **PUT + readback verified** |
| Generate 301 CSV (reception + boardroom) | CSV deliverable | ✅ `data/redirects/landing-refresh-301s.csv` — **Steve imports manually** |
| Repair `/collections/healthcare` broken meta — clean honest text, NOT keyword-targeted (page owns `healthcare furniture canada`) | Admin-API | ✅ **PUT + readback verified** → "Healthcare Furniture \| Brant Business Interiors" |
| Unpublish empty `healthcare-seating` (sitemap hygiene) | Admin-API | ✅ **verified unpublished** |
| Neutralize empty crawlable collections (executive-desks, healthcare-seating → 301) | CSV deliverable | ✅ rows 3–4 in `landing-refresh-301s.csv` — **Steve imports** (redirect is the real 200-killer; unpublish alone doesn't stop the 200) |
| Exec-desks canonical | — | ⏸ **deferred to a dedicated Option-A build session** (build the smart collection properly, ~30 executive-adjacent desks, then publish + meta + links). Temp 301 → `/collections/desks` in place until then. |
| D3 — link 85 PDPs → canonical collections | Admin-API | ⏸ **held until the exec-desks session** so each PDP is edited once with all its collection links together |

### Surface A status: COMPLETE (except D3 + exec-desks build, both intentionally deferred)
Canonical URLs locked: reception → `reception-desks-desks` · boardroom → `boardroom` · healthcare → `/collections/healthcare`. Remaining live action for Steve: **import `data/redirects/landing-refresh-301s.csv`** (4 rows). After import, re-run the weekly rank snapshot to watch the boardroom 301 (the one higher-risk row) recover.

**301 CSV note:** reception 301 = low risk (dupe→canonical). Boardroom 301 = **higher risk** (redirects the *currently-ranking* URL into the optimized one) — recoverable by deleting the redirect; monitor next weekly snapshot.

**Exec-desks inventory reality (grounded):** strict "executive desk" SKUs = **3**; "executive" anywhere = 10; L/U-shape desks = 26; office suites = 18; broad desks = 88. Live populated collections: `/collections/desks` 41 · `l-shape-desks` 31 · `office-suites-desks` 13 · `desks-straight` 18. → A dedicated executive-desks collection is viable only with a **broadened** executive-adjacent rule (~30 products); the 3-SKU literal reading is too thin.
