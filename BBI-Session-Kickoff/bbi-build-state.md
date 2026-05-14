# BBI Build State — Single Source of Truth

**Last updated:** 2026-05-14 (BUG-FIX-3 COMPLETE — combined OECM + industry:* remediation · business-furniture smart collection rebuilt (exclude:business-furniture tag convention, 11 products tagged) · 489 industry:* tags stripped · oecm-eligible stripped from 9 service/fee items · oecm-eligible added to 61 missing furniture products · final state: 584 oecm-eligible products · Phase 1: 15 of 15 done · PHASE 1 COMPLETE)
**Dev theme:** BBI Landing Dev (`186373570873`) — never publish to live until LAUNCH-2
**Live theme:** brantbusinessinteriors.com (production — untouched)
**Replaces:** the status sections in `shopify-fix-plan.md` and the localStorage-bound `SEEDS` in `website-fix-checklist.html`

---

## ⛔ HARD RULES — APPLY EVERY SESSION, NO EXCEPTIONS

> **Incident 2026-05-10:** A session accidentally pushed `layout/theme.liquid`, `snippets/theme-variables.liquid`, and `assets/information-drawer.css` to the live theme (`178274435385`), breaking brantbusinessinteriors.com for ~30 min. These rules prevent recurrence.

| Rule | Enforcement |
|---|---|
| All theme file writes go to `186373570873` (BBI Landing Dev) **only** | `push-file.py` now hard-aborts if `THEME_ID == LIVE_THEME_ID` |
| Never run `shopify theme push` without `--theme 186373570873` | Bare push may default to live |
| Never type `yes` at the bbi-push-landing.py live-theme prompt | That prompt means you've targeted the wrong theme |
| `fetch-file.py` and `find-liquid-bug.py` may **read** live — never write | Both are labelled read-only in their headers |
| Before writing any theme asset, print `THEME_ID` and confirm it is `186373570873` | Do this as a preflight check in every session |
| If a script has `THEME_ID = '178274435385'` hardcoded — stop, fix it, then run | Never override or skip this check |

---

## How to use this file

Every wave below is a phase of work. Every row is a single piece of buildable scope with a stable ID. Status reflects **git + filesystem reality**, not intent. When you ship something, update its row in this file in the same commit. When the row says ✅ but the evidence is missing or 404, the row is wrong — fix the file before continuing.

**Status legend**

| | Meaning |
|---|---|
| ✅ | Done — committed, deployed, verified |
| 🟡 | Partial — some progress, named gap remaining |
| 🔄 | In progress — actively being worked |
| 🚧 | Blocked — waiting on a named prereq |
| ⬜ | Not started |

**Evidence column** — where to look to confirm the row is true. Either a git SHA, a file path, a Shopify URL, or a script output.

---

## How to drive this with Claude Code (prompts)

**You don't paste the markdown into every prompt.** The pattern is: reference the row ID, let Claude Code read the file. CLAUDE.md points it to these docs already, so the project context loads them on session start.

### Self-driving mode — one prompt per session (RECOMMENDED)

Paste this once at the start of a Claude Code session and let it run:

```
Standing instruction — work through Wave A of docs/plan/bbi-build-state.md
in order. For each ⬜ row:

  1. Sync this worktree first: git fetch origin && git merge origin/main
  2. Read the row's Notes column in bbi-build-state.md.
  3. If Notes contains 🔔 NEEDS DECISION → halt, ask me the question, wait.
  4. Otherwise: propose a brief plan (≤5 bullets), wait for "go" or "skip",
     then build, test, commit. Mark the row ✅ with the commit SHA in the
     same commit. Push.
  5. Continue to the next ⬜ row.

Stop and report when:
  - Wave A is complete (all rows ✅)
  - A row has a 🔔 NEEDS DECISION marker
  - A row blocks on an outside dependency (Leo's manual setup, etc.)
  - A test/audit fails

When stopping, print exactly the next prompt I should send to resume.

Start now with the first ⬜ row in Wave A.
```

That's the entire prompt. Claude Code reads `bbi-build-state.md`, picks the next row, proposes, builds, marks done, loops. You only re-engage when it hits a 🔔 row or fails.

### 🔔 NEEDS DECISION markers (rows that always halt for input)

These rows have explicit decisions only you can make. Claude Code halts before starting them:

- **NAV-1** — 🔔 5-item nav (`Shop Furniture · Industries · Brands · Services · About`) or 6-item nav (current landing-page rendering)?
- **PB-13** — 🔔 `brand-dealer` — merge from separate branch or de-gate?
- **CONTENT-1** — 🔔 BBI logo — lock `bbi-logo-v2` (Brant Basics wordmark) or source a true BBI wordmark?
- ~~**LEAD-1**~~ — ✅ resolved 2026-05-07 (audit done, doc at `docs/plan/bbi-lead-routing.md`)
- ~~**LEAD-3**~~ — ✅ decisions locked 2026-05-07 (three inboxes + modal pattern; see `docs/plan/bbi-lead-routing.md`)
- **LAUNCH-0** — 🔔 you must personally review the image-approval CSV before LAUNCH-1 can run
- **LAUNCH-2** — 🔔 manual publish click — never automated

### Per-row prompts (if you prefer to drive manually)

**Common prompt shapes:**

| Goal | Prompt |
|---|---|
| **Resume** (most common) | `Continue Wave A — standing instruction.` (Claude Code already has the standing instruction in session memory; this resumes the loop after a 🔔 halt.) |
| Start the next task fresh | `What's the next ⬜ row in Wave A? Read docs/plan/bbi-build-state.md, propose how to start, wait for confirm.` |
| Build a specific row | `Work on PB-12 — read its row in docs/plan/bbi-build-state.md, propose the implementation, then build. Mark ✅ with SHA in the same commit.` |
| Build a Phase 2 page | `/bbi-build-page seating — see BUILD-STATE row P2-2 and INTERLINKING row /collections/seating.` |
| Run an audit | `Run the 12-point check from docs/plan/bbi-interlinking-map.md against /pages/healthcare. Report pass/fail per point.` |
| Drift-check a page | `Compare live /pages/quote on dev theme 186373570873 to theme/sections/ds-lp-quote.liquid in this worktree. Report any drift.` |
| Status snapshot | `Read docs/plan/bbi-build-state.md and tell me: what's done, what's blocked, what's next. Bullet form, under 200 words.` |

**The key idea:** Claude Code reads the source-of-truth markdown each time. You give it the row ID. It looks up the row, reads its notes/evidence, and acts. When work is done, it edits the row in the same commit as the code change. The Cowork artifact then auto-reflects the new status on next reload.

**For the `/bbi-build-page` skill specifically** — once SKILL-1 is done, every page build prompt becomes one line:

```
/bbi-build-page <slug>
```

The skill reads `bbi-build-state.md` for the row's brief, `bbi-interlinking-map.md` for the page's expected outbound/inbound links, runs all 12 audit points before marking done, and refuses to commit if any check fails. No need to paste guidance into the prompt — the skill is the guidance.

**Files Claude Code should always have in context** (already in CLAUDE.md):

- `docs/plan/bbi-build-state.md` — what to do
- `docs/plan/bbi-interlinking-map.md` — how to verify pages are wired
- `docs/strategy/design-system.md` — token + component spec
- `docs/strategy/icp.md` — voice + audience
- CLAUDE.md itself — project rules, BBI-specific guardrails

---

## Lessons Learned — read before building any new page

Four deploy-error patterns recurred during P1 builds. The `/bbi-build-page` skill must enforce all four (see SKILL-1).

1. **Page must be in the `bbi_landing` gate.** Add the new template suffix to `theme/layout/theme.liquid` line 81. Skip → Starlite chrome leaks (double header, double footer, wrong nav). Symptom: `quote` page leaked Starlite chrome for weeks after build because suffix wasn't added.

2. **Logo schema setting must be populated in the template JSON.** Wiring the `image_picker` schema in the section is half the work. The template JSON's `settings: { logo: "shopify://shop_images/..." }` must be set, otherwise the section falls back to the text wordmark. Symptom: OECM, design-services, quote, FAQ all rendered text instead of logo until `b4ae936` patched.

3. **`bbi-push-landing.py` only pushes assets/sections/templates — not `theme/layout/theme.liquid`, not snippets.** Layout changes need a direct Shopify API call (or `shopify theme push --only=layout/theme.liquid`). Skip → the gate edit lives in git but never reaches the dev theme.

4. **🔴 Push from the right repo root — worktree drift bug.** `bbi-push-landing.py` defaults `BBI_PUSH_ROOT` to the main repo (`/Users/leokatz/Desktop/Office Central/theme/`). When Claude Code works in a worktree (`.claude/worktrees/*/theme/`) and the script runs without `BBI_PUSH_ROOT=$(pwd)` set, it silently uploads **the main repo's stale versions** to Shopify, overwriting any fresh worktree work. Symptom: industries page lost its embedded header/footer mid-week; all 10 BBI landing sections drifted out of sync until `9c8b7db` re-pushed all 22 files from the worktree at once. **Always run `BBI_PUSH_ROOT=$(pwd) python scripts/bbi-push-landing.py …` from inside a worktree, or fix the script to auto-detect (see PB-12).**

**Pre-deploy verification (every new page):**
- `document.querySelectorAll('.bbi-header').length === 1`
- `document.querySelectorAll('.bbi-footer').length === 1`
- No `.shopify-section-group-header-group` in DOM
- Logo `<img>` has non-empty `src`
- Every cross-link href returns 200
- `/bbi-lp-audit` returns clean
- Pre-flight: `pwd` is the worktree, `BBI_PUSH_ROOT=$(pwd)` set, OR push script has been patched (PB-12)

---

## Known Data Hygiene Issues (surfaced 2026-05-12)

These issues are catalogued here because they affect multiple upcoming sessions and must be referenced when running PE Pass 3, COLLECTION-CLEANUP-1, AI-8, and SEO-AUDIT-1.

### Vendor field fragmentation
- 89% of active products (526 of 593) still have vendor = "Brant Business Interiors" — a placeholder from the original Office Central migration, not the real manufacturer.
- PE Pass 3 batches 1–2 enriched 74 products with body_html + specs but did NOT populate the vendor_override field. The plumbing exists in `scripts/push-pe3-enrichment.py`; the batch prompt templates omit the field.
- Future batches (3, 4, 6) MUST populate vendor_override using the canonical brand map from VENDOR-NORMALIZE-1 (see launch tracker).

### specs.manufacturer string fragmentation
- 152 products have a specs.manufacturer metafield populated by PE Pass 2 Hero enrichment + the 74 PE Pass 3 pushes so far.
- 20+ string variants exist for Global Furniture Group alone (e.g., "Global Upholstery Co., Inc", "Global Upholstery Co. / Offices To Go", "OTG / Offices to Go (a division of Global Furniture Group)", etc.).
- Before any brand callout / tagging work, these strings must be normalized against a canonical brand map.

### Real brand distribution (data, not aspiration)
Based on 152 enriched products with specs.manufacturer:
- Global Furniture Group family (Global, OTG, Newland, Fileworks, Basics, Global Upholstery): ~113 products
- Heartwood Manufacturing: ~17 products
- Shoptech / Horizon: ~5 products
- Deflecto: ~2 products
- Fellowes: ~2–3 products
- ergoCentric: 1 product (despite having a brand collection + category page callouts)
- Keilhauer: 0 products (despite having a brand collection + category page callouts)
- Other small brands: ~11 products
- 441 products have no specs.manufacturer yet (unenriched, mostly pending PE Pass 3 batches 3 / 4 / 6).

Implication: brand callouts on category pages currently point at Keilhauer + ergoCentric (zero / one product). These should be reassigned to Global, OTG, Heartwood after VENDOR-NORMALIZE-2 lands. Tracked as part of COLLECTION-CLEANUP-1.

### Tag mass-application
- oecm-eligible: applied to 653/653 active products. Either a botched mass-tag or used historically as an "active product" marker. Currently makes the /pages/oecm page surface the full catalog instead of a curated list.
- Investigation pending in BUG-FIX-2 (launch tracker Step 2).
- Worth auditing other tag prefixes (brand:*, room:*, type:*) for similar mass-application — tracked as TAG-AUDIT-1 (launch tracker, new step).

### Three-source data inconsistency
Vendor / brand data lives in three places that don't agree:
1. Shopify vendor field (currently fragmented — 89% placeholder)
2. specs.manufacturer metafield (currently fragmented — 20+ string variants per brand family)
3. brand:* tags (sparse — only applied via `tag-products-by-collection.py` dry runs, never live)

All three must agree per product before the storefront's brand smart collections + brand callouts function correctly. The canonical brand map (VENDOR-NORMALIZE-1) is the bridge between them.

### Historical push script silent failures (resolved 2026-05-12)

Between PE Pass 2 (first Hero 100 batches) and Batch 3 of
PE Pass 3 (2026-05-12), `scripts/push-pe3-enrichment.py` had four
bugs that caused it to silently skip writes for body_html,
Shopify vendor field, and brand:* tag — while correctly writing
specs.* metafields. As a result, PE Pass 2/3 enrichment work
appeared as "live" in build state and tracker but only the
metafield specs were actually live on the storefront. Buyer-facing
descriptions, vendor attribution, and brand tags remained the
raw pre-enrichment import data.

**Bugs in push-pe3-enrichment.py (all fixed in commit 58e8a27):**
1. Script read `rec.get('description')` but batch output uses
   `draft_body_html` — descriptions never written.
2. Output JSON shape mismatch: products at top level vs under
   'products' key — script saw 0 products in some batch files.
3. Filter used `rec.get('status')` but data field is `action` —
   action='other' products would have been pushed if any matched.
4. No brand:* tag write logic — tags from batch output ignored.
5. Vendor field also wasn't being written — bundled with the
   brand-tag-write fix in 58e8a27.

**Resolution 2026-05-12:**
- Push script bugs fixed in commit 58e8a27.
- All 88 affected products (69 from Batches 1+2 + 19 from
  Batch 3) had body_html + vendor + brand:* tag pushed live.
  Evidence: `data/logs/pe3-push-20260512-224332.json` (88 products_ok, 0 failures, live: true).
  **Note for Steve:** `data/logs/` is gitignored — no standalone git commit for the Shopify push itself.
  The push occurred between commits 58e8a27 (script fix) and 33a2c35 (kody patch post-verification).
- `kody-mesh-chair-otg13110` had a draft-side copywriting gap
  (missing BBI close paragraph in the original Batch 2 draft);
  fixed in commit 33a2c35.
- Post-push verification confirmed 5/5 sample products clean on
  storefront, spec metafield average 9.4 per product.

**Lesson — required for future batch sessions:**
- Every batch's --live push must include the defensive
  prerequisite check (verify push script field names match batch
  output schema before run) AND a post-push 5-product storefront
  verification.
- The PE Pass 3 batch kickoff prompt pattern (added 2026-05-12)
  bakes both checks in by default.

### Canonical brand map gaps surfaced during PE Pass 3 + TAG-AUDIT-1
_(pending resolution in COLLECTION-CLEANUP-1 sub-steps,
 Steps 10A–10D)_

The canonical brand map (VENDOR-NORMALIZE-1, 2026-05-12) was built
from the 152 enriched products available at that point. PE Pass 3
Batches 4 + 6 + TAG-AUDIT-1 surfaced 10 additional brand variants
that need to be added to the map. None are blockers — affected
products have correct fallback handling (`vendor_override =
"Brant Business Interiors"` + `research_failed_reason` populated).
Resolution scheduled in COLLECTION-CLEANUP-1 Steps 10A–10D.

**Pending additions:**

| Brand | Source | Products | Notes |
|---|---|---|---|
| Safco | TAG-AUDIT-1 | 4 | standalone, callable=False |
| Humanscale | TAG-AUDIT-1 | 2 | standalone, callable=False |
| Victor Technology LLC | PE Pass 3 Batch 4 | 1 | standalone, callable=False |
| Rocelco | PE Pass 3 Batch 4 | 1 | standalone, callable=False |
| HDL | PE Pass 3 Batch 4 | 1 | dist by Grand & Toy; standalone, callable=False |
| Kensington | PE Pass 3 Batch 6 | 1 | tech accessories; standalone, callable=False |
| Sentry Safe | PE Pass 3 Batch 6 | 2 | Sentry Group parent; standalone, callable=False |
| FireKing | PE Pass 3 Batch 6 | 1 | standalone, callable=False |
| Tayco | PE Pass 3 Batch 6 | 1 | Toronto, ON manufacturer of the Halifax line; standalone, callable=False |
| Heartwood slug migration | TAG-AUDIT-1 | 1 | re-tag `brand:heartwood` to `brand:heartwood-manufacturing-ltd` |

**Total: 14 products** across 10 brand entries need canonical map
additions + product re-tagging.

**Re-push idempotency confirmed 2026-05-13:** The push script's
incremental catch-up behavior (rewriting all products in the
output file on each --live run, not just the newest batch) was
verified safe via Batch 4 integrity check — 3/3 sampled prior-batch
products had byte-identical body_html before and after re-push.
Future batch sessions can expect push counts higher than the
batch's product count; this is feature, not bug.

**RESOLUTION 2026-05-13:** All 15 affected products re-tagged
in commit 66a0bff (APPLY-MAP-ADDITIONS, Sub-step B).
Canonical map total: 30 brands (added Safco, Humanscale, Victor
Technology LLC, Rocelco, HDL, Kensington, Sentry Safe, FireKing,
Tayco in commit 29bcbad — Sub-step A). Heartwood slug migration
surfaced 0 stragglers — already migrated in earlier sessions.

### Global-Teknion smart collection — restored to intent (2026-05-13)
The brands-global-teknion smart collection was found to be running
on a single legacy rule `tag equals brand:global-teknion`, matching
21 unenriched products carrying the merged legacy tag. The rule
was broken — it would have collapsed to 0 products as remaining
stragglers got normalized. COLLECTION-CLEANUP-APPLY (commit 737f6f6)
updated the rule to disjunctive `brand:global-furniture-group OR
brand:teknion`, restoring the hybrid Wave C intent. Collection now
shows 72 products (all GFG + Teknion combined). 18 unenriched
stragglers had the legacy tag stripped; they will receive correct
canonical brand tags during Phase 1b post-launch enrichment.

### Collections — post-COLLECTION-CLEANUP-APPLY state (2026-05-13)
Active collections post-COLLECTION-CLEANUP-APPLY: 207
(was 371 before 2026-05-13 audit + cleanup). 164 unpublished —
either ARCHIVE (legacy / 0-product / not in nav) or REDIRECT
(legacy brand collections folded into /pages/brands).
data/url-redirects-bulk.csv contains 164 rows ready for
Shopify Admin import.

---

## Wave A — Foundations + Phase 2 build

**Pre-req:** Track D (DS-0 → DS-4) ✅ complete. Phase 1 (P1-1 → P1-11) ✅ complete.
**Goal:** Stop the bleeding (PB-12), harden the build skill (SKILL-1), unify nav/footer (NAV-1..4), then build the Business Furniture vertical + 9 categories.

**Order rationale:** PB-12 first because every `--slug` push today is a coin flip until root-detection is fixed. SKILL-1 next because it's the prevention layer that uses PB-12's fix in its pre-flight check. NAV-1..4 then because Phase 2 collection-category pages should be built on top of the unified nav, not embed yet another copy.

| # | ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|---|
| 1 | **PB-12** | **🔴 Fix `bbi-push-landing.py` root detection + extend to layout/snippets** | ✅ | commit `5888659` (worktree `cool-jepsen-6d89c5`, pending merge to main) | **Done.** `_resolve_root()` is worktree-aware: env var > cwd-contains-`.claude/worktrees/` > `__file__` fallback, with loud `⚠️ ROOT MISMATCH` banner on divergence. New `--layout` flag pushes only `layout/theme.liquid`. New `--snippets` flag pushes only `snippets/bbi-*.liquid` (Starlite legacy snippets structurally excluded). Startup banner prints `Root / Layout / Snippets` for audit. |
| 2 | **CLEANUP-1** | **Remove phantom gate suffixes + prune stale planning docs** | ✅ | commit `c9e5c5a` | One-off housekeeping prerequisite to SKILL-1. Remove `brand-dealer` + `smoke-test` from `bbi_landing` gate; delete replaced/draft planning files; update CLAUDE.md reference table. |
| 3 | **SKILL-1** | **Harden `/bbi-build-page` skill** | ✅ | commit `06220d0` `.claude/skills/bbi-build-page/SKILL.md` | **Done.** v2.0: Pre-Step 0b (worktree hard-stop + build-state check + interlinking context load); gate edit automated in Step 5 (writes `theme.liquid` directly, no manual step); Step 9 (image_picker discover → upload → populate template JSON → `--layout` then `--slug` in one call); Step 11 (full 12-point check: 10 DOM assertions + source-level FAQ grep + 3-signature drift check); Step 12 (mark ✅ only on all-green). version: 2.0 pinned. |
| 4 | NAV-1 | Lock canonical nav spec | ✅ | commit `d41295a` `docs/strategy/bbi-nav-spec.md` | Decision: 5-item w/ mega-menu (per site-architecture-2026-04-25.md §1) — `Shop Furniture · Industries · Brands · Services · About` + phone CTA + Quote button right-aligned. Mobile: hamburger → full-screen accordion overlay. 🔔 ~~NEEDS DECISION~~ — Spec locked 2026-05-06. |
| 5 | NAV-2 | Build `bbi-nav.liquid` + `bbi-footer.liquid` snippets | ✅ | commit `f683fb9` `theme/snippets/bbi-nav.liquid`, `theme/snippets/bbi-footer.liquid` | **Done.** Mega-menu nav (5 items, all dropdown-only, CSS hover+focus-within, `<bbi-nav-mobile>` Web Component with WCAG focus trap + Escape). Footer: 9-cat Shop col, OECM in Services col, OECM trust band above copyright. Active state via `active` render param. Healthcare + Quote smoke-tested: 14/14 assertions green (1 header, 1 footer, correct active item, 4 columns, trust band). |
| 6 | NAV-3 | Refactor 10 ds-lp-* sections to render shared snippets | ✅ | commit `5ba69b0` (all 10 ds-lp-*.liquid files) | **Done.** All 10 sections render shared snippets (healthcare+quote in NAV-2; industries/education/government/non-profit/professional-services/design-services/faq/oecm here). ~131–141 lines removed per section (header CSS + footer CSS + HTML blocks). Smoke test: 4 pages × 5 assertions = 20/20 green; style count 14→16 (+2 snippet styles, confirming dead section CSS removed); FAQ regression OK (Services col has 6 links incl. FAQ). |
| 7 | NAV-4 | Homepage onto shared nav | ✅ | commit `2850959` `theme/sections/bbi-nav-wrap.liquid`, `theme/sections/bbi-footer-wrap.liquid`, `theme/templates/index.json`, `theme/layout/theme.liquid` | **Done.** Option A wrapper sections (bbi-nav-wrap + bbi-footer-wrap); logo image_picker + pre-populated with v2 logo URL. Gate extended: `template == 'index'` added. Smoke test 6/6 green: bbi-header=1, bbi-footer=1, Starlite suppressed, no active item on /, footerColumns=4, 10 bbi- sections in order (nav-wrap first, footer-wrap last). |
| 7b | NAV-5 | Header search bar + BBI search results page | ✅ | 2026-05-12 `theme/snippets/bbi-nav.liquid` + `theme/sections/ds-search-results.liquid` + `theme/templates/search.json` pushed to dev theme 186373570873 | **Done.** Inline search bar (always-visible, 220px, gray pill with icon) added to `bbi-nav.liquid` utility bar between nav and phone number; hidden on mobile (mobile overlay retains its own search row). Predictive suggest via `/search/suggest` API — debounced 200ms, up to 5 product results with thumbnails + "See all" link, drops down from the bar, closes on click-outside or Escape. `ds-search-results.liquid` replaces base-theme `main-search` section in `templates/search.json` — BBI-styled 4-col product grid (same cards as ds-collection-base), breadcrumb, result count, refine-search bar, pagination, empty state. Products in `other` + `other-1` collections filtered out of results via `product.collections` loop. Only `type=product` results shown. |
| 8 | PB-13 | Reconcile brand-dealer (merge or de-gate) | ✅ | commit `71e7b5e` (CLEANUP-1) | **Done.** Resolved by CLEANUP-1 — gate already de-cluttered (brand-dealer suffix removed from theme.liquid). Branch never pushed to remote; file never existed on main. Page out of scope for v1 (Industries Hub + Brands Hub cover dealer-trust signaling). |
| 9 | PB-9 | Extend `bbi_landing` gate to detect collection templates | ✅ | commit `ceac44f` `theme/layout/theme.liquid` | **Done.** Added `template == 'collection.category'` to bbi_landing gate. Smoke test deferred to PB-10 (first collection.category page exercises it). |
| 10 | PB-10 | Build `collection.category.json` template + `ds-cc-base.liquid` section pattern | ✅ | commit `77fca26` `theme/sections/ds-cc-base.liquid`, `theme/templates/collection.category.json`, `scripts/set-collection-template-suffix.py` | **Done.** Section: hero + breadcrumb (2/3-level via settings) + intro (richtext) + tile grid (max 20 tile blocks, always rendered) + view-all CTA + brand_callout blocks (max 2) + phone CTA closer. Gate exercised: `?view=category` on dev theme. Smoke test 5/5 green: bbi-header=1, bbi-footer=1, Starlite suppressed (PB-9 confirmed), active nav="Shop Furniture", tile grid container present. Helper script: dry-run default, --live, --rollback flags; backup + log on every run. |
| P2-1 | Business Furniture vertical (`/collections/business-furniture`) | ✅ | commit `3e9ffe3` `theme/templates/collection.business-furniture.json` | 9 category tiles + 3 brand callouts (Keilhauer, Global/Teknion, ergoCentric), view-all CTA, phone CTA closer. Gate extended for `collection.business-furniture`. Smoke: 9 tiles, 3 brands, view-all, phone CTA, Starlite suppressed — all green. |
| P2-2 | Seating (`/collections/seating`) | ✅ | commit `4e04f12` `theme/templates/collection.seating.json` | 16 sub-type tiles, Keilhauer + ergoCentric callouts. Smoke: 16 tiles, 2 brands, 3-level breadcrumb, Starlite suppressed — all green. |
| P2-3 | Desks & Workstations (`/collections/desks`) | ✅ | commit `4e04f12` `theme/templates/collection.desks.json` | 9 sub-type tiles, Global/Teknion callout. Suffix set via API. |
| P2-4 | Storage & Filing (`/collections/storage`) | ✅ | commit `4e04f12` `theme/templates/collection.storage.json` | 14 sub-type tiles, no callouts. Suffix set via API. |
| P2-5 | Tables (`/collections/tables`) | ✅ | commit `4e04f12` `theme/templates/collection.tables.json` | 10 sub-type tiles, no callouts. Suffix set via API. |
| P2-6 | Boardroom (`/collections/boardroom`) | ✅ | commit `4e04f12` `theme/templates/collection.boardroom.json` | 3 sub-type tiles, Keilhauer callout. Suffix set via API. |
| P2-7 | Ergonomic Products (`/collections/ergonomic-products`) | ✅ | commit `4e04f12` `theme/templates/collection.ergonomic-products.json` | 4 sub-type tiles, ergoCentric callout. Suffix set via API. |
| P2-8 | Panels & Dividers (`/collections/panels-room-dividers`) | ✅ | commit `4e04f12` `theme/templates/collection.panels-room-dividers.json` | 3 sub-type tiles, Global/Teknion callout. Suffix set via API. |
| P2-9 | Accessories (`/collections/accessories`) | ✅ | commit `4e04f12` `theme/templates/collection.accessories.json` | 4 sub-type tiles, no callouts. Suffix set via API. |
| P2-10 | Quiet Spaces (`/collections/quiet-spaces`) | ✅ | commit `4e04f12` `theme/templates/collection.quiet-spaces.json` | 5 sub-type tiles, no callouts. Suffix set via API. |
| PB-11 | Sub-collection 200/404 + product count audit | ✅ | commit `81e83c8` `data/reports/sub-collection-audit-20260506_211829.csv` | 68/68 slugs found. 66 PASS / 2 WARN (metal-shelving + audio-visual-equipment empty — need products). 0 FAIL. `scripts/audit-sub-collections.py` report-only, exit 0. |
| LEAD-1 | Crawl + dump current lead routing | ✅ | commit `21a26df` `docs/plan/bbi-lead-routing.md` | Full CTA audit across all 10 ds-lp-* sections, bbi-nav, bbi-footer, ds-cc-base, index.json custom-liquid. Two critical gaps found: (1) design-services uses unreliable `mailto:` form; (2) `/pages/quote` "Online quote form" link goes to `/pages/contact` which has no template. LEAD-3 decisions pre-loaded. Steve to fill in Shopify notification routing + phone line + inbox verification per action items in the doc. |
| INTERLINK-1 | Formalize P1-11 audit pattern as reusable script | ✅ | commit `937cbcc` `data/reports/interlink-audit-20260506_211250.csv` | 21/21 pages checked. 0 FAIL / 52 PASS / 92 WARN / 108 SKIP. WARNs on checks 6/7/8/11 are live-theme fallback (dev theme preview requires Shopify admin auth — source files confirmed correct). `--suffix` flag added to `set-collection-template-suffix.py`. |
| IND-PROP | Industries Hub Browse + FAQ propagation to 5 industry pages | ✅ | commit `c6812bd` `theme/snippets/ds-browse-faq.liquid` | Browse (9-grid) + FAQ (5-item) added to all 5 industry sections via shared `ds-browse-faq` snippet. Smoke tested healthcare + government. |

---

## Wave B — Phase 3 + Smart Collections

**Pre-req:** Wave A complete.
**Goal:** Sub-collection product listings on the new design system. Migrate manual collections to smart so new products auto-populate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| PB-14 | Manual → Smart collection migration script + per-collection assignment + rollback | ✅ | `66f7623` `scripts/migrate-to-smart-collections.py` | Convert manual `/collections/*` to rule-based using `type:*` and `room:*` tags. Backup first. |
| PB-15 | Build `collection.json` template + `ds-cs-base.liquid` section | ✅ | `de3237e` `theme/sections/ds-cs-base.liquid` + `collection.base.json` + gate update | Filter sidebar + product grid + 4-level breadcrumb (Home > Shop Furniture > Category > Sub-collection) + phone CTA. |
| P3-rollout | Apply `collection.json` to ~68 Business Furniture sub-collections | ✅ | `aaa105a` `scripts/set-sub-collection-suffix.py` + rollout run | Script-driven push, hero images from `data/page-images/` |
| INTERLINK-2 | Re-run interlinking audit, fix drift introduced by Phase 3 | ✅ | `82c64c8` Post-Wave-B audit (0 failures) | |

---

## Wave C — Phase 4 trust pages

**Pre-req:** Wave B complete (so brand pages can link to live shop verticals).
**Goal:** Brands hub + brand pages + About + Contact + Our Work + Delivery + Relocation.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| P4-1 | Brands Hub (`/pages/brands`) | ✅ | `theme/sections/ds-lp-brands.liquid` + `theme/templates/page.brands.json` exist; Page ID 170824958265 published 2026-05-07 | Phase 1 API check (2026-05-08): exists, published, suffix `brands` ✅. body_html=0 expected (OS 2.0 section-rendered). |
| P4-2 | Keilhauer (`/pages/brands-keilhauer`) | ✅ | `theme/sections/ds-lp-brands-keilhauer.liquid` + `theme/templates/page.brands-keilhauer.json` exist; Page ID 170824991033 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-keilhauer` ✅. |
| P4-3 | Global / Teknion (`/pages/brands-global-teknion`) | ✅ | `theme/sections/ds-lp-brands-global-teknion.liquid` + `theme/templates/page.brands-global-teknion.json` exist; Page ID 170825056569 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-global-teknion` ✅. |
| P4-4 | ergoCentric (`/pages/brands-ergocentric`) | ✅ | `theme/sections/ds-lp-brands-ergocentric.liquid` + `theme/templates/page.brands-ergocentric.json` exist; Page ID 170825023801 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-ergocentric` ✅. PB-13 reconciliation resolved (CLEANUP-1 commit `71e7b5e`). |
| P4-5 | About (`/pages/about`) | ✅ | `theme/sections/ds-lp-about.liquid` + `theme/templates/page.about.json` exist; Page ID 170825220409 published 2026-05-07 | Phase 1 API check: exists, published, suffix `about` ✅. |
| P4-6 | Our Work / Portfolio (`/pages/our-work`) | ✅ | `theme/sections/ds-lp-our-work.liquid` + `theme/templates/page.our-work.json` exist; Page ID 170825318713 published 2026-05-07 | Phase 1 API check: exists, published, suffix `our-work` ✅. Content (48 OCI photos) still to be wired — content work, not scaffolding. |
| P4-7 | Contact (`/pages/contact`) | ✅ | `theme/sections/ds-lp-contact.liquid` + `theme/templates/page.contact.json` exist; Page ID 134463553849 published 2024-01-17 | Phase 1 API check: exists, published, suffix `contact` ✅. body_html=2348 chars (legacy content, harmless). Form routing to sales@ unverified — separate verification item. |
| P4-8 | Delivery & Installation (`/pages/delivery`) | ✅ | `theme/sections/ds-lp-delivery.liquid` + `theme/templates/page.delivery.json` exist; Page ID 170825253177 published 2026-05-07 | Phase 1 API check: exists, published, suffix `delivery` ✅. |
| P4-9 | Relocation Management (`/pages/relocation`) | ✅ | `theme/sections/ds-lp-relocation.liquid` + `theme/templates/page.relocation.json` exist; Page ID 170825285945 published 2026-05-07 | Phase 1 API check: exists, published, suffix `relocation` ✅. |

---

## Wave D — Wave 0 SEO foundation (parallel to A/B/C)

**Pre-req:** None — runs in parallel with theme work.
**Goal:** Make SEO progress measurable before launch. Mostly Leo's manual work.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| W0-1 | Google Search Console + GA4 setup | ⬜ | GSC property + GA4 property | Critical — no SEO compounds without this |
| W0-2 | Create BBI Google Business Profile | ⬜ | google.com/business listing | |
| W0-2b | Google Reviews seeding strategy | ⬜ | `docs/plan/reviews-seeding.md` | |
| W0-6 | Parent domain backlinks (officecentral.com, brantbasics.com) | ⬜ | inbound link audit | Coordinate with parent webmasters |
| W0-7 | OECM + "Since 1964" trust signals on store header/footer | ⬜ | shared snippets + announcement bar | Already in landing pages — surface site-wide |
| W0-3 | Upload product redirects CSV | 🟡 | `data/url-redirects.csv` exists | Manual upload in Shopify Admin pending |

---

## Wave G-Fixes — Visual review bugfixes (2026-05-09)

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| WAVE-G-FIXES-1 | Bug-fix pass from live visual review of dev theme 186373570873 | ✅ | commits `a20b526`→`42c4227`; all files on dev theme | **BATCH-1** Smart collections chrome: `template.name == 'collection'` gate already correct; dev theme had stale layout.liquid — re-pushed via direct API. **BATCH-2** 11 PDP fixes: (2a) gallery thumb JS clears srcset; (2b) variant chips → `<button>` + `BbiPdpVariants` WC + variant JSON; (2c) description moved after variants, full HTML; (2d) has_specs checks all 11 fields, spec-row alternating via Liquid counter; (2e) both buttons 100% width 48px; (2f) delivery note absent; (2g) validation keeps chips horizontal; (2h) image 1024px square contain; (2i) quote btn `color:#fff` explicit; (2j) additional-services product unpublished → published via API; (2k) CTA closer btn `color:#fff` explicit. **BATCH-3** blog CTA `color:#fff`; footer Blog & Resources link added. **BATCH-4** `scripts/tag-products-by-collection.py` written + dry-run: 34 boardroom / 14 global-teknion candidates found; 6 collections DATA GAP (no vendor/type metadata) — awaiting Leo review. |
| WAVE-G-FIXES-2 | Second bug-fix pass — quote modal, PDP restructure, brand plates, emoji, CTA copy | ✅ | commits `71c37e0`→`586290b`; all 26 files pushed to dev theme 186373570873 | **BATCH-1** Re-verified WAVE-G-FIXES-1 regressions: chip flex hardened with `display:flex !important` (Starlite override); blog CTA + 404 button `color:#fff !important` (class+element specificity beat class-only); additional-services confirmed HTTP 200. **BATCH-2** New `bbi-quote-modal.liquid` snippet — `<dialog>`-based Web Component with Shopify contact form, focus trap, success screen; wired nav, footer, PDP, blog, 404, cc-base, delivery pages; global JS intercept for `[href*="/pages/quote"]` covers 20+ landing pages without per-file edits; rendered once in `theme.liquid` inside `bbi_landing` gate. **BATCH-3** PDP: variant price refreshes on chip select via `Intl.NumberFormat`; description restructured as three inline labeled sections (About / Key Features / Specs) inside info column — standalone `.pdp-features` and `.pdp-specs` full-width blocks removed. **BATCH-4** `brand_plate_canadian: false` → `true` for Global Furniture and Teknion in all 9 collection JSON templates — "Canadian Authorized" badge now shows for both. **BATCH-5** 4 emoji (🚚 🔧 📋 ♻️) removed from delivery page feature card icon divs. **BATCH-6** `ds-cc-base.liquid` hero CTA: only appends `hero_title` when `cta_label` is blank — fixes "Get a free design consultationBusiness Furniture" concatenation bug on business-furniture collection. **BATCH-7** Wave A smoke check: 9/10 PASS, desks WARN-transient (subsequent check clean, likely bot rate-limit on first curl); report at `data/reports/wave-a-smoke-2026-05-10.csv`. |

---

## Wave H — Stabilization & PE Pass 1 (2026-05-10 → 2026-05-11)

**Why this wave exists:** A run of architectural fixes and feature builds completed after Wave G-Fixes-2 that didn't fit cleanly into existing waves. Includes the 2026-05-10 live-site incident recovery (81 missing assets synced live → dev), full cart funnel rebuild, PDP black-background fix, design system completion for default collection templates, PDP gallery lightbox, site-wide best-sellers sort, and the first milestone of the restructured PROMPT-4 product enrichment workflow.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| STAB-1 | Asset infrastructure recovery + cart chrome architectural fix | ✅ | commits (2026-05-10) `theme/layout/theme.liquid`, `theme/templates/cart.json`, `theme/sections/ds-cart-base.liquid`, `config/settings_data.json` | **81 missing CSS/JS assets** synced from live → dev (`base.css`, `style.css`, `collection.css`, `theme.js`, +77 others). Direct loads of collection and search pages now render correctly. **Cart chrome architectural fix:** root cause was `template == 'cart'` missing from `bbi_landing` gate, so Starlite header/footer/JS were loading alongside BBI nav. Starlite JS polluted CSS vars and localStorage, breaking the next page on navigation from cart. Added cart to gate, restructured `cart.json` with `bbi-nav-wrap` + `bbi-footer-wrap` sections, stripped inline `render` calls from `ds-cart-base.liquid`. **Settings patches:** `image_border: true`, `image_background: true`, `quickview: false` aligned dev with intended product-card behaviour. |
| PDP-BLACK-FIX | Black PDP background fix (2026-05-11) | ✅ | `theme/layout/theme.liquid` head injection + JS guard | Dark-mode toggle JS (`localStorage.darkMode == 'true'`) was setting `color-mode="dark"` on `<html>` unconditionally. Attribute-selector specificity beat every `body { ... !important }` override attempted in section CSS. Two-part fix: (a) skip dark mode on product templates via `template == 'product'` check before the JS runs; (b) CSS belt-and-suspenders in `<head>` with matching specificity (`html[color-mode] body, html[color-mode="dark"] body, html body, body { background-color: #ffffff !important }`). Steve confirmed PDPs render white. Note: existing dark-mode flag in user's localStorage requires hard refresh / incognito to fully clear after fix. |
| CART-FUNNEL | Cart 404 + badge + page DS + polish + mini-cart (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/snippets/bbi-nav.liquid`, `theme/sections/ds-cart-base.liquid`, `theme/templates/cart.json`, `theme/assets/bbi-logo-v2.png` | **Cart 404 fix:** ds-pdp-base.liquid Add to Cart now uses `fetch('/cart/add.js')` AJAX instead of full-page POST. Shows "Added ✓" for 2s + dispatches `cart:updated`. **Header cart count badge:** bbi-nav.liquid gained shopping bag icon + red count `[data-bbi-cart-count]`; server-renders `cart.item_count`; refreshes on `cart:updated` via `/cart.js`. **Cart page design system:** new `ds-cart-base.liquid` section + `cart.json` template replacing default Shopify cart. BBI nav + footer, 1320px container, BBI tokens. **Cart polish (later same day):** replaced hardcoded `#0B0B0C` with `rgb(var(--buttonBackground))` tokens on checkout + empty-state CTAs. Mini-cart dropdown in nav header — cart icon → dropdown panel (line items + subtotal + View Cart + Checkout); closes on click-outside + Escape; refreshes on `cart:updated`. Uploaded `bbi-logo-v2.png` to dev theme assets (nav/footer logo fallback now resolves). |
| PROMPT-2 | Buy Now + Quantity selector on PDP (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid` | Quantity stepper + Buy Now button wired to `/cart/add.js` → `/checkout`, sitting inside the buyable-only branch (BBI Rule #2 preserved — Quote-only CTA on $0/sold-out untouched). Variant-ID resolution matches existing ATC flow (BbiPdpVariants Web Component). Regression: ATC + mini-cart + Quote modal all continued to work. |
| PROMPT-3 | Best-sellers sort site-wide + PDP related rewrite (2026-05-11) | ✅ | 19 smart collections updated via Admin API; `ds-pdp-base.liquid` related section rewrite | **Site-wide:** audited 369 collections (49 smart, 320 custom). Set `sort_order = best-selling` on 19 smart collections (19/19 HTTP 200). 9 editorial exclusions kept original sort: `bundle-builder-products` (created-desc), `fees-products` (alpha-asc), 7 `room-*` collections. Rollback CSV at `data/backups/collection-sort-orders-pre-20260511_135450.csv`. Site-wide audit confirmed no Liquid overrides via `\| sort_by`. **PDP related:** rewired to 3-tier fallback (`all-<type>` → `room-`tag → `all-business-furniture`); heading reads "Best sellers in `<category>`" on Tier 1, "Customers also bought" otherwise; section suppressed when all empty. Capture pattern used to work around Shopify Liquid's `where_exp` outer-scope limitation. **Note:** collection sort changes are store-wide (affect live theme too, not just dev). |
| PDP-LIGHTBOX-1 | PDP gallery lightbox + related-card aspect ratio (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid` lightbox CSS/JS + card aspect 4/3 → 4/5 | **Lightbox:** clicking main product image opens fullscreen viewer — dark overlay (`rgba(0,0,0,0.92)`), centred full-res image, left/right arrow buttons + keyboard nav, `1 / 4` counter when multiple images, ESC or click-outside closes, body scroll locks while open, arrows auto-hide on single-image products. **Related card ratio:** 4/3 → 4/5 to match collection-page cards in `ds-cc-base.liquid`; hover eased to `scale(1.03) / 160ms`. Visual parity between PDP related cards and collection grid is now exact. |
| IMG-BG-WHITE | Product image slot background — white site-wide (2026-05-12) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/sections/ds-cs-base.liquid`, `theme/sections/ds-cc-base.liquid`, `theme/sections/ds-article.liquid` | Product images have a white background in Shopify CDN but containers were set to `var(--alternateBackground)` (#FAFAFA grey), creating a visible grey mat around every product photo. Fixed all 7 product image slots to `#FFFFFF`: PDP gallery main + thumbnails (`.pdp-gallery__main`, `.pdp-gallery__thumb`); PDP "Best sellers in…" related cards (`.pdp-prod-card__img-wrap`); smart collection page cards (`.ds-cs__card-img`); category collection tile + product cards (`.ds-cc__tile-media`, `.ds-cc__product-card-media`); article related product cards (`.prod-card__img-wrap`). Editorial hero / landing-page media containers left at `--alternateBackground` (real photos fill those). |
| IMG-CENTER | Product image centering + contain fit site-wide (2026-05-12) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/sections/ds-cs-base.liquid`, `theme/sections/ds-cc-base.liquid`, `theme/sections/ds-article.liquid` | All product card image slots switched from `object-fit: cover` (crops/fills) to `object-fit: contain` + `object-position: center`, with `display: flex; align-items: center; justify-content: center; padding: 12px` on containers (4px for thumbnails). Matches the pattern already used on the PDP main gallery. Hover scale (`scale(1.03)`) removed from all card images — scaling a contained image expands into whitespace. 6 selectors updated: `.pdp-prod-card__img-wrap/img`, `.pdp-gallery__thumb img`, `.ds-cs__card-img/img`, `.ds-cc__tile-media/img`, `.ds-cc__product-card-media/img`, `.prod-card__img-wrap/img`. |
| COLLECTION-DS-1 | ds-collection-base for default `/collections/*` pages | ✅ | Closed by Steve 2026-05-11 | Default-template collection pages (`/collections/all` + smart collections without custom template suffixes) now resolved. The BBI design system is the source of styling on these surfaces. Closes the gap where `/collections/all` rendered with Starlite's `main-collection` product grid instead of BBI design system. |
| PE-PASS-1 | Product enrichment Pass 1 — triage CSV (2026-05-11) | ✅ | commit `76f109d` · `data/reports/product-triage-pass1-2026-05-11.csv` | First milestone of restructured PROMPT-4 (was "write 500 descriptions", now triage-first 3-pass flow). Pulled 653 products (593 active + 60 archived; `status=any` not functional on this token so pulled separately and merged). 24-month sales for 126 products (203 orders processed). SEO metafields for all 653 (2 errors, defaulted to false). **Working set:** 553 products (653 minus Hero 100). **Tier breakdown:** A=98 keep, B=12 light enrichment, C=383 archive recommended, skip=60 leave-unpublished. **Archive breakdown:** 20 HR1 ($0 hard rule), 47 non-best in duplicate clusters (+1 HR1 override), 316 zero-sales + quality-gap. **Duplicate clusters:** 52 covering 117 products. CSV has `steve_override_action` column for manual override. All 7 sanity checks pass. **Top 5 borderline archives:** 5 Teknion $0 showcase products (HR1 triggered but per BBI Rule #2 likely override to keep-quote-only). **Top 5 duplicate clusters surfaced false positives:** delivery fees (4 SKUs at different prices), chair mats (different sizes), chair variants (size/arm options not true duplicates). Steve reviewing in Sheets. |
| PE-PASS-2 | Move-to-Other + enrichment CSV generation | ✅ | commit `a734c9c` · 7 batch prompts at `BBI-Session-Kickoff/enrichment-prompts/` | **All 4 phases complete.** Phase 0: `ds-pdp-base.liquid` patched (single-tier related, Other breadcrumb fallback) + `bbi-product-jsonld.liquid` breadcrumb fallback (`d6dfaf0`). Phase 1: Other collection created (id=527013085497). Phase 2: canary `teknion-boardroom` ✅. Phase 3: 336 archive products moved to Other, tags stripped (1 failure `craft-round-20-unit` recovered). Phase 4: enrichment infrastructure built — `pe-pass2-products.json` (157 products), `pe-pass2-batches.json` (7 batches), `pe-pass2-checkpoint.json` + `pe-pass2-output.json` (empty, ready). 7 self-contained batch prompt files built for one-by-one Claude enrichment sessions. Override applied: `archive-duplicate` excluded from move (all 47 kept). **Enrichment sessions (7 batches) in progress — Steve runs these independently.** |
| SPEC-JSON-LD | `additionalProperty` in Product JSON-LD | ✅ | commits `5be9b56`, `5f4a3bc` · `theme/snippets/bbi-product-jsonld.liquid` on dev `186373570873` + live `178274435385` | Added `additionalProperty` array to Product schema.org JSON-LD. Reads all 12 `specs.*` metafields; conditionally renders each as `PropertyValue`. Also: Key Features stripped from About section in `ds-pdp-base.liquid` via `split: '<h3>' \| first` — now only appears in Specifications. Both files pushed to dev + live theme. Verified on localhost:9292 (Arlo chair): About clean, Specs correct. |
| KF-STRIP | Key Features de-duplication in About section | ✅ | commit `5f4a3bc` · `theme/sections/ds-pdp-base.liquid` | `product.description \| split: '<h3>' \| first` strips Key Features / Who it's for / closing boilerplate from the About block. Legacy products with no `<h3>` unaffected (single-item array, full description returned). Verified via API on 2600 Series (789 chars, 2 h3 sections stripped) and visually on Arlo chair. |
| SPEC-HERO-PUSH | Hero 100 spec gap-fill + metafield push | ✅ | `data/specs.json` (100) + `data/logs/pe2-push-20260511-230357.json` (final push) | **All hero spec sessions complete (2026-05-11).** Steve ran H1A (12), H1B (11), H2 (19), H3 (~35), and a bonus `hero-batch-other.md` (9). Output file: 99 products (49 done + 33 auto-patched OTG/Global + 16 skip + 1 service). All pushed: `merge-hero-specs.py --live --push` confirmed. Final push log: `pe2-push-20260511-230357.json`. |
| HERO-SPEC-SESSIONS | Hero 100 spec gap enrichment sessions (H1A → H3) | ✅ | `data/reports/hero-spec-gaps-output.json` — 99 products complete | **All 4 batches run by Steve (H1A/H1B/H2/H3) + bonus `hero-batch-other.md`.** 49 done + 33 auto-patched (OTG/Global warranty + country) + 16 skip + 1 service. Merge+push confirmed via `scripts/merge-hero-specs.py --live --push`. |
| PE-PASS-3 | Push enrichment to Shopify (descriptions + specs + vendor) | ✅ | `scripts/push-pe3-enrichment.py` · `data/logs/pe3-push-20260511-235643.json` · `data/logs/pe3-push-20260512-224332.json` · commits d898b12 (Batch 4) · a4582ea (INNOVATIONS-FIX) · a44d14c (Batch 6) | **COMPLETE 2026-05-13. Final progress: 143 of 157 products enriched and live on storefront.** Batches shipped: 1 (25), 2 (26), 3 (19), 4 (25), 5 (10), 6 (30), 7 (13) = 148 total batch rows; 143 enriched + live, 14 are routed-to-Other or intentional skip rows. 10 new brand singletons surfaced across Batches 4 + 6 + TAG-AUDIT-1 — catalogued in Known Data Hygiene Issues → Canonical brand map gaps; none are blockers. Closes Step 8 of the launch tracker. **PE Pass 3 COMPLETE 2026-05-13. 143/157 products enriched and live. Remaining 14 are intentional skip / routed-to-Other.** |
| SPEC-CANARY | Live canary test — Google Rich Results Test | 🟡 | `bbi-product-jsonld.liquid` + `ds-pdp-base.liquid` pushed to live theme `178274435385` | Both files live on `178274435385`. **Note:** live site brantbusinessinteriors.com uses Avada's `main-product` section (not `ds-pdp-base`) — so additionalProperty won't render on the live public site until the dev theme is set as the main theme. Dev theme (186373570873) verified on localhost:9292: additionalProperty rendered, About section clean. **Remaining:** Google Rich Results Test on a Hero product URL once dev theme preview is accessible — defers to pre-launch SEO-AUDIT-1. |
| ICP-V2 | ICP v2 approved + cascaded to all prompt files | ✅ | commit `1d6684c` · `docs/strategy/icp.md`, `.claude/skills/bbi-build-page/SKILL.md`, 8 enrichment batch files | Steve approved 2026-05-06 draft. Changes: co-primary ICPs A+B (institutional + SMB equal weight), Ontario + Western Canada co-primary geography, dual buying mode (cart + quote), install in Ontario + Western Canada. Cascaded to: SKILL.md (buyers context, ICP gate question, card CTA dual-mode), all 8 enrichment prompts (closing ¶ delivery/install language, OECM Ontario-vs-national distinction). |
| AUDIT-1 | Pre-launch tech-debt + state audit | ✅ | `data/reports/audit-tech-debt-2026-05-12.md` · `data/reports/empty-collections-snapshot-2026-05-12.csv` | 15 findings total. 4 blockers promoted to launch path Steps 1–4. 11 deferred. Surfaced vendor data hygiene issues now catalogued in "Known Data Hygiene Issues" section above. |
| PUSH-FIX-1 | Surfaced + fixed 5 silent-failure bugs in `scripts/push-pe3-enrichment.py` · body_html / vendor field / brand:* tag writes restored · 88 products affected, all pushed live 2026-05-12 | ✅ | commits 58e8a27 (script fix), 33a2c35 (kody patch); push evidence: `data/logs/pe3-push-20260512-224332.json` (88 products_ok, 0 failures, live: true) | See Known Data Hygiene Issues → Historical push script silent failures for full bug list and root-cause analysis. Post-push verification: 5/5 sample products clean on storefront, avg 9.4 spec metafields per product. |
| PE-PASS-3-BATCH-4 | Desks & Tables Part 1 enrichment batch | ✅ | commit d898b12 | 2026-05-13 · 25 products enriched + pushed (9 OTG, 7 GFG, 2 Office Star, 1 Fellowes, 1 Heartwood, 5 BBI fallback) · 5/5 storefront verification · 5 research_failed_reasons surfaced (Victor Technology, Rocelco, HDL identified for canonical map addition) |
| INNOVATIONS-FIX | Corrected canonical brand map — Innovations re-attributed from Global Furniture Group to Heartwood Manufacturing Ltd. | ✅ | commit a4582ea | 2026-05-13 · as_standalone=False, parent=Heartwood · 5 products re-tagged (vendor + metafield + brand tag) · surfaced during Batch 4 enrichment research, confirmed via heartwooddl.com · 5/5 verification |
| PE-PASS-3-BATCH-6 | Storage & Accessories enrichment batch — LAST PE Pass 3 batch | ✅ | commit a44d14c | 2026-05-13 · 30 products enriched + pushed (9 Heartwood, 7 OTG, 4 Fellowes, 1 Deflecto, 9 BBI fallback) · 5/5 storefront verification · 4 new brand singletons surfaced (Kensington, Sentry Safe, FireKing, Tayco — all flagged for canonical map addition) · Step 8 closes |
| CANONICAL-MAP-ADDITIONS | Add 9 new canonical brands to brand map | ✅ | commit 29bcbad | 2026-05-13 (Sub-step A) · added 9 new canonical brands to docs/strategy/brand-canonical-map.md + .csv (Safco, Humanscale, Victor Technology LLC, Rocelco, HDL, Kensington, Sentry Safe, FireKing, Tayco) · canonical brand total 20 → 30 · Heartwood slug migration captured in notes |
| APPLY-MAP-ADDITIONS | Re-tag 15 products to match new canonical entries | ✅ | commit 66a0bff | 2026-05-13 (Sub-step B) · re-tagged 15 products to match new canonical entries · vendor field + specs.manufacturer metafield + brand:* tag now agree per product across the full canonical brand map · 15/15 verification clean |
| COLLECTION-AUDIT | Audit all 371 collections — read-only | ✅ | commit a24b9e3 | 2026-05-13 (Sub-step C1, read-only) · 371 collections audited (49 smart, 322 custom) · 148 zero-product · 30 dead tile links surfaced · /collections/other browsable with 337 archived products flagged urgent · 39 INVESTIGATE flagged for human review · output data/reports/collection-audit-2026-05-13.md |
| COLLECTION-CLEANUP-APPLY | Apply audit dispositions — 164 collections unpublished | ✅ | commit 737f6f6 | 2026-05-13 (Sub-step C2) · applied audit dispositions · 164 collections unpublished (161 ARCHIVE + 3 REDIRECT) · 18 unenriched stragglers stripped of brand:global-teknion tag · global-teknion smart collection rule converted to disjunctive (GFG OR Teknion), now 72 products · /collections/other unpublished · 10 dead tile blocks removed from 4 category templates · 1 dead link updated · 164 redirects added to data/url-redirects-bulk.csv · Steve must manually import redirects via Shopify Admin |
| BRAND-CALLOUT-AUDIT | Audit + fix brand callouts on Phase 2 category pages | ✅ | commit 326241f | 2026-05-13 (Sub-step D, Step 14) · audited 10 Phase 2 templates · 6 templates updated · Keilhauer callouts removed from business-furniture/seating/boardroom (0 products) · ergoCentric callouts removed from business-furniture/seating/ergonomic-products (1 product) · 2 dead brand tiles removed from seating · GFG callout added to storage/tables/boardroom (→ /collections/global-teknion, 72 products) · Global/Teknion callout kept on desks/panels (valid) · accessories/quiet-spaces unchanged · brand plates band deferred to BRAND-PAGES-1 (Step 24) · audit report: data/reports/brand-callout-audit-2026-05-13.md · backups: data/backups/brand-callout-audit-20260513-190930/ |

---

## Wave G — Phase 5: Product + system templates

**Pre-req:** Wave C complete (so brand pages link to live trust pages). Independent of Wave D.
**Goal:** Rebuild the PDP template + add the missing system pages (Customer Stories, custom 404, smart collections, blog templates) before audit + launch waves run.
**Why before Wave E:** Wave E hardening runs perf / a11y / link-rot / schema audits on every page in the `bbi_landing` gate. Running those before the PDP rebuild means re-running them after — wasted work. Build everything, then audit once. The user explicitly accepted slower launch in exchange for first-time-right.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| PB-PDP-1 | Extend `bbi_landing` gate for `template == 'product'` | ✅ | `theme/layout/theme.liquid` line 90–91 | Confirmed present by Stage 4a audit (`stage-4a-decision.md` §1). Gate already includes `template == 'product'`. No action needed. |
| PDP-1 | Build `ds-pdp-base.liquid` section + `product.json` template | ✅ | `theme/sections/ds-pdp-base.liquid` (32 KB) + `theme/templates/product.json` on dev theme 186373570873. Gallery `<bbi-pdp-gallery>` Web Component (thumbnail swap); Quote-only CTA when price==0 or available==false (BBI Rule #2); spec table from all 12 `specs.*` metafields; related products from type-tag category collection (max 4); 4-level breadcrumb; `bbi-nav active=shop` + `bbi-footer`. JSON-LD placeholder comment left for PDP-2. | Hero gallery (carousel + zoom from `product.images`); spec table from PE-2 metafields (`product.metafields.specs.*`); **Request a Quote CTA auto-rendered when `product.price == 0` OR `product.available == false`** (BBI rule #2 — unbuyable items stay live as lead-capture pages); related products (same `type:*` tag, max 4); 4-level breadcrumb (Home > Shop Furniture > Category > Product); renders `bbi-nav` (active=`shop`) + `bbi-footer`. Use `image_url` + `image_tag` for responsive srcset; lazy-load below-fold images per CLAUDE.md performance rules. |
| PDP-2 | Wire JSON-LD into `ds-pdp-base` (absorbs AI-3) | ✅ | `theme/snippets/bbi-product-jsonld.liquid` + `theme/snippets/bbi-breadcrumb-jsonld.liquid` on dev theme. 24/24 source checks green (Product schema fields, InStock/OutOfStock branches, price==0 branch, calls breadcrumb snippet, 4-level BreadcrumbList). Note: `?preview_theme_id` requires admin session auth — source verification used. Rich Results Test to run in Wave E SEO-AUDIT-1. | **Absorbs AI-3 (Product schema on every PDP) — that row removed from Wave E.** Product JSON-LD: `name`, `description`, `image`, `offers` (price + availability + `priceCurrency: CAD`), `brand`, `sku`, `mpn` if present. Renders shared `bbi-breadcrumb-jsonld.liquid` snippet from AI-6 (don't duplicate breadcrumb logic). Validate with Google Rich Results Test on 3 PDPs (Hero in-stock, Hero sold-out, $0 showcase). |
| PDP-3 | PDP smoke test — 5 product states | ✅ | `data/reports/pdp-smoke-20260508.csv` — 34/34 checks green across 5 states. Real Shopify products used: (a) l-shape-desk (in-stock, price=1179.99), (b) anda-seat (sold-out, deny policy), (c) additional-services (price=$0), (d) 2600-series-4-drawer (11 spec metafields), (e) l-shape-desk (sparse/no-specs guard). Source + API verification; browser auth required to verify via ?preview_theme_id. | Test 5 PDP states: (a) in-stock priced Hero, (b) sold-out, (c) $0 showcase, (d) Hero with full spec metafields, (e) non-Hero with sparse metafields. DOM assertions per page: `bbi-header=1`, `bbi-footer=1`, Starlite suppressed, breadcrumb 4-level, Product JSON-LD valid, Quote CTA visible on (b)+(c) only. |
| CS-1 | Customer Stories page (`/pages/customer-stories`) | ✅ | `theme/sections/ds-lp-customer-stories.liquid` + `theme/templates/page.customer-stories.json` exist; Page ID 170838884665 published 2026-05-07 | Phase 1 API check (2026-05-08): exists, published, suffix `customer-stories` ✅. Content (story cards, testimonials) not yet wired — content work, not scaffolding. | Page hero + industry filter chips (healthcare, education, government, non-profit, professional-services) + story cards (image, pull-quote, customer name, industry tag, link to full case study). Review schema (`schema.org/Review`) per testimonial. Seed from `data/oci-photos/catalog.json` (48 photos) + `docs/strategy/voice-samples.md`. **Cross-linked from:** homepage Rule 6 ("Read customer stories →"), About page, 5 industry pages, 3 brand pages. Site architecture §2j flags as ⭐ priority. |
| 404-1 | Custom 404 page (`templates/404.json`) | ✅ | `theme/sections/ds-system-404.liquid` + `theme/templates/404.json` on dev theme; gate `template == '404'` already present in theme.liquid. Note: Shopify does not honour `?preview_theme_id` for 404 responses — asset presence verified via Admin API (both files 200 OK on theme 186373570873). | Branded 404 — H1 "Page not found" + brief copy + search box (`/search` form) + 4 top category tiles (seating, desks, storage, tables) + phone CTA + Quote button. Add `template == '404'` to `bbi_landing` gate. Smoke test by hitting any garbage URL on dev theme. |
| SMART-1 | Smart collections — 10 "view all" + 4 brand-filtered | ✅ | `scripts/create-smart-collections.py`; `data/reports/smart-collections-20260508_163930.csv`; 14/14 live on Shopify (all-seating … all-business-furniture, keilhauer, global-teknion, ergocentric, oecm-eligible). keilhauer/global-teknion/ergocentric were custom collections — converted via `--convert-custom` flag. | Create 14 smart collections via Shopify Admin API. **10 "view all" per category** (`all-seating`, `all-desks`, `all-storage`, `all-tables`, `all-boardroom`, `all-ergonomic`, `all-panels`, `all-accessories`, `all-quiet-spaces`, `all-business-furniture`) — rule: tagged `type:<category>`. **4 brand-filtered** (`keilhauer`, `global-teknion`, `ergocentric`, `oecm-eligible`) — rule: tagged `brand:<brand>` or `oecm-eligible`. Reuses smart-collection helper from PB-14. Backup current collection list before running; `--dry-run` default. Wired up by category-page "View all" CTAs (already in interlinking-map). |
| BLOG-TPL-1 | Blog + Article templates (empty — content deferred) | ✅ | `theme/sections/ds-blog-list.liquid` + `theme/templates/blog.json` + `theme/sections/ds-article.liquid` + `theme/templates/article.json` on dev theme; `template.name == 'blog'` and `template.name == 'article'` added to bbi_landing gate in theme.liquid. Assets verified via Admin API (all 200 OK). | BBI-styled templates only — no posts yet. **Resources hub** (paginated list, category filter chips, optional tag filter, related products from collection metafield). **Article** (hero image, prose body, related products module, FAQPage schema if `article.metafields.faq` exists, share buttons, author/date metadata). Add `template == 'blog'` and `template == 'article'` to `bbi_landing` gate. First posts (BL-1..BL-6 + B1..B10) stay in post-launch backlog per CLAUDE.md (every post starts with DataForSEO keyword research). |

---

## Wave E — Pre-launch hardening

**Pre-req:** Waves A + C complete.
**Goal:** All schema, copy, lead routing, nav, design system verified before launch gate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| AI-4 | Organization schema on homepage + About | ✅ | `theme/snippets/bbi-org-schema.liquid` rendered from `bbi-nav.liquid` (fires on every BBI page) | `Organization` + `LocalBusiness` JSON-LD: `name`, `url`, `logo`, `telephone`, `address`, `areaServed`, `sameAs`. Renders from nav so every BBI-gated page gets it automatically. |
| AI-6 | BreadcrumbList JSON-LD via shared snippet | ✅ | `theme/snippets/bbi-breadcrumb-jsonld.liquid` + wired to `ds-pdp-base` (via `bbi-product-jsonld`) + `ds-cc-base` + `ds-cs-base` · pushed to dev `186373570873` 2026-05-11 | Snippet built (up to 4 levels, blanks omitted). Wired: PDP = 4-level via bbi-product-jsonld; cc-base = 2-level (no parent) or 3-level (with parent label); cs-base = 4-level (Home > Shop Furniture > Category > Sub-collection). Validates against Rich Results Test in SEO-AUDIT-1. |
| AI-7 | Entity-clarity copy on homepage | ⬜ | first 200 words on `/` | Who BBI is, what they sell, who they serve, where |
| AI-8 | OECM page copy hardening | ⬜ | `/pages/oecm` | Highest-value AI citation target |
| AI-9 | FAQ blocks on category pages | ⬜ | 9 category pages | 3–5 Q&A per category, FAQPage schema |
| AI-5 | FAQ schema on OECM, Design Services, top blog posts | ⬜ | view-source check | |
| LEAD-2 | Gap analysis on lead routing | ⬜ | `docs/plan/bbi-lead-routing.md` | Identify duplicate forms, inconsistent inboxes |
| **LEAD-INBOX-1** | **Provision + verify lead-form inboxes (HARD PREREQ for LEAD-3)** | ⬜ | TBD email provider config + test-receipt screenshots | 🔔 **NEEDS STEVE.** Provision `quotes@`, `design@`, `info@brantbusinessinteriors.com` (or alias to existing). Configure forwarding so all three land in `steve@brantbusinessinteriors.com`. Verify SPF / DKIM / DMARC pass on outbound (so auto-replies don't spam-bin). Send a test message to each address from an external domain; confirm receipt at `steve@`. **Hard prereq for LEAD-3** — the modal smoke test cannot run without working inboxes. Mark ✅ before LEAD-3 build starts. |
| LEAD-3 | Unify on `bbi-lead-form.liquid` snippet + modal + per-type routing + auto-replies | 🟡 | `theme/snippets/bbi-quote-modal.liquid` built in WAVE-G-FIXES-2 BATCH-2 | **UI complete.** `bbi-quote-modal.liquid` — `<dialog>`-based Web Component with Shopify contact form (`/contact`), focus trap, success screen, product context data attrs. Wired to every quote CTA across nav, footer, PDP, blog, 404, cc-base, delivery, and all 20+ landing pages via global JS intercept. **Routing deferred to Phase 4** (LEAD-INBOX-1 still ⬜ — Steve must provision `quotes@`/`design@`/`info@` inboxes before routing can be wired). Three inboxes: `quotes@`, `design@`, `info@brantbusinessinteriors.com`. Lead-type → inbox: quote→quotes, design→design, contact→info, oecm→quotes. Auto-replies pending LEAD-INBOX-1. See `docs/plan/bbi-lead-routing.md`. |
| INTERLINK-3 | Final cross-link audit, all pages | ⬜ | audit output green | |
| **SEO-AUDIT-1** | **Technical SEO audit via DataForSEO MCP (HARD GATE)** | ⬜ | `data/reports/seo-audit-<date>.json` + `docs/reviews/seo-audit-<date>.md` | **Pre-launch hard gate — must run before LAUNCH-0.** Use the DataForSEO MCP (`on_page` + `lighthouse` + `domain_analytics` tools) against BBI Landing Dev (`186373570873` preview URL). Required checks: (a) crawl every published page in `bbi_landing` gate, (b) meta titles + descriptions present and within length limits, (c) H1 hierarchy correct (one H1 per page, no skipped levels), (d) all schema validates (Organization, Product, BreadcrumbList, FAQPage from AI-3..AI-6), (e) canonical tags resolve, (f) no broken internal links, (g) Lighthouse mobile perf ≥ 80, (h) Core Web Vitals pass on top 5 templates (home, OECM, quote, industries hub, healthcare). Output a per-page issue list with severity (block / fix / waive). All `block` items must be resolved or explicitly waived in the report before LAUNCH-0 can run. |
| NAV-VERIFY | Homepage + collection pages render shared nav | ⬜ | DOM check | Verify NAV-3, NAV-4 stuck |
| DS-VERIFY | DS pre-launch verification (HARD GATE) | ⬜ | screenshot diff vs T5 locked | Brand-red unified, dark-mode block stays deleted, tokens intact |
| IMG-PHASE2 | Product image regen (≥80% coverage SOFT GATE) | ⬜ | `data/reports/img-phase2-coverage.csv` | Waiver CSV for the rest |
| PERF-AUDIT-1 | Lighthouse + Core Web Vitals on top 10 pages | ⬜ | TBD `data/reports/perf-audit-<date>.csv` | Run Lighthouse mobile + desktop on /, /collections/business-furniture, /collections/seating, /pages/oecm, /pages/healthcare, /pages/quote, /pages/faq, /pages/about, /pages/our-work, /pages/contact. Save scores + LCP/FID/CLS/INP. Flag pages below mobile-perf 80 or any CWV failing. |
| A11Y-AUDIT-1 | WCAG 2.1 AA audit on top 10 pages | ⬜ | TBD `data/reports/a11y-audit-<date>.csv` | axe-core or pa11y CLI on the same 10 pages. Hard fails: missing alt text, no form labels, contrast < 4.5:1, focus traps broken, keyboard gaps. Per-page issue list. |
| LINK-ROT-1 | Internal + external link 200/404 sweep | ⬜ | TBD `data/reports/link-rot-<date>.csv` | Crawl every `<a href>` across all bbi_landing pages. Internal: assert 200. External: flag 404/500/timeouts. |
| SYS-VERIFY-1 | System pages (cart / search / account / password) chrome verification | ⬜ | TBD `data/reports/system-pages-verify-<date>.csv` | DOM check on `/cart`, `/search`, `/account/login`, `/account/register`, `/account`, `/password`. **Note:** `/search` is intentionally BBI-styled (NAV-5) — `templates/search.json` uses `bbi-nav-wrap` + `ds-search-results` + `bbi-footer-wrap`; no gate entry needed. `/cart` already in gate (STAB-1). Verify: no double header/footer on account/password pages, search + cart flows functional, account/register/password still render Starlite chrome intact. |
| CONTENT-1 | Finalize BBI logo asset | ⬜ | `data/logos/bbi-logo-final.png` | 🔔 **NEEDS DECISION** — `bbi-logo-v2` is the Brant Basics wordmark (not BBI-specific). Lock it as the current answer, OR source/design a true "Brant Business Interiors" wordmark. If sourcing new, that's a content task that adds 1–2 days. |

---

## Wave F — Launch

**Pre-req:** Wave E complete.
**Goal:** Cutover from BBI Landing Dev to live theme.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| **LAUNCH-0** | **Image confirmation gate (HARD)** | ⬜ | `data/reports/page-images-audit-<date>.csv` reviewed | 🔔 **NEEDS YOUR REVIEW** — Claude Code generates the CSV; you must personally mark every row Approved / Reject / Replace before LAUNCH-1 can run. Hard gate, no automation. |
| LAUNCH-1 | Pre-publish GO/NO-GO report | ⬜ | `data/reports/launch-go-nogo-<date>.md` | 4 critical URLs return 200, no TBD/lorem, screenshots saved. No writes. |
| LAUNCH-2 | Manual publish of BBI Landing Dev → live | ⬜ | live theme backup + post-publish snapshot | 🔔 **MANUAL CLICK** — never automated. Claude Code runs the live-theme backup; you click Publish in Shopify Admin. |
| LAUNCH-3 | Resubmit sitemap to GSC, monitor 404s for 72h | ⬜ | GSC dashboard | |
| LAUNCH-4 | Mobile smoke test (Chrome, Safari, Firefox, iOS, Android) | ⬜ | screenshots saved | |

---

## Backlog (post-launch)

These compound after live, none blocks launch:

- **Phase 1b full catalog** — PE-5/6/7 for the 503 non-Hero products (descriptions, specs, meta)
- **Blog** — BL-1..BL-6 (template + schema + related products) + first 10 posts (B1..B10). **🔍 Every blog post must start with DataForSEO MCP keyword research** — pull search volume, difficulty, related keywords, SERP competitors, and "people also ask" before drafting. Target keyword + 2–3 secondary keywords go in the brief; the post is written to rank for them.
- **SEO-AUDIT-2 — Cross-page keyword optimization (DataForSEO MCP)** — once the full site is built (post-LAUNCH-2), run a site-wide keyword audit: pull current rankings, identify cannibalization (multiple pages competing for the same keyword), find gaps (high-intent keywords with no landing page), and reassign primary/secondary keywords per page. Output: `docs/strategy/bbi-keyword-map-<date>.md` with one row per page (URL, primary KW, secondary KWs, search volume, current rank). Then patch meta titles, H1s, and intro copy across pages to align.
- **AI search** — AI-10 (spec completeness), AI-11 ("best of" / comparison content)
- **Smart Collections** — finish migration on remaining manual collections
- **Wave 2** — Acoustic Pods sub-collection, sit-stand buyer guide, hybrid work bundle
- **Wave 3** — City-level SEO, ergonomics hub, sustainability/LEED page, manufacturer dealer locator pages
- **Ideas backlog** — see `docs/plan/ideas-backlog.md`

---

## Phase 1 — Done ✅ (reference)

All 11 P1 rows complete on origin/main.

| ID | Page | Evidence |
|---|---|---|
| P1-1 | Homepage | `theme/templates/index.json` (8 sections) — commit `7172c85` |
| P1-2 | OECM | `theme/sections/ds-lp-oecm.liquid` + `page.oecm.json` — commit `ef234cf` (header/footer added `905db28`, logo `b4ae936`) |
| P1-3 | Design Services | `ds-lp-design-services.liquid` + `page.design-services.json` — commit `0ab1663` (header/footer added `905db28`, logo `b4ae936`) |
| P1-4 | Quote | `ds-lp-quote.liquid` + `page.quote.json` — commit `b40a1e3` (gate + header/footer + logo `0fe3de9` / `b4ae936`) |
| P1-4b | FAQ | `ds-lp-faq.liquid` + `page.faq.json` — commit `0d452eb` (logo `b4ae936`) |
| P1-5 | Industries Hub | `ds-lp-industries.liquid` + `page.industries.json` — commit `623cc43` (Browse + FAQ added `e98f91f`) |
| P1-6 | Healthcare | `ds-lp-healthcare.liquid` + `page.healthcare.json` — commit `9a8c27b` (crosslink fix + footer pro-services `905db28`) |
| P1-7 | Education | `ds-lp-education.liquid` + `page.education.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-8 | Government | `ds-lp-government.liquid` + `page.government.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-9 | Non-Profit | `ds-lp-non-profit.liquid` + `page.non-profit.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-10 | Professional Services | `ds-lp-professional-services.liquid` + `page.professional-services.json` — commit `ee44b06` |
| P1-11 | Phase 1 interconnection audit + fix | commits `905db28`, `0fe3de9`, `0d452eb`, `b4ae936` |

---

## Track D — Design System Done ✅ (reference)

| ID | Task | Evidence |
|---|---|---|
| DS-0 | Land Claude Design Phase 3 — 5 screen exports + audit tables | commit `c1a719c` |
| DS-1 | Fill `design-system.md` TBD placeholders | commit `b34807c` (`grep -c TBD = 0`) |
| DS-2 | Push design tokens to BBI Landing Dev | commit `8ebc65c` |
| DS-3 | Three Liquid edits + PR + push | dark-mode block deleted, `#f00f00`/`#FFCA10` → `#D4252A` |
| DS-4 | `/bbi-build-page` readiness check | 9-row pass — `READY` verdict |

---

## Phase 1b — Hero 100 Done ✅ (reference)

All Hero 100 product enrichment is LIVE on Shopify.

| ID | Task | Evidence |
|---|---|---|
| PE-1 | Hero 100 descriptions (LIVE) | commit `58803c3` — 1,165 product mutations |
| PE-2 | Hero 100 spec metafields (LIVE) | commit `204d8dc` — 77 products / 606 metafield writes / 0 failures |
| PE-3 | Hero 100 normalized titles (LIVE, ™/® stripped) | commit `57d99f3` — 588 products |
| PE-4 | Hero 100 SEO meta titles + descriptions (LIVE) | commit `a2118f3` — 100 Hero SEO meta |
| PE-7 | Long-tail SEO drafts (LIVE) | commit `58803c3` |

---

## AI Search — Started 🟡 (reference)

| ID | Task | Status | Evidence |
|---|---|---|---|
| AI-1 | `llms.txt` deployed | ✅ | commit `a2118f3` |
| AI-2 | `robots.txt` audit | ✅ | commit `24ab01e` |
| AI-12 | `audit-ai-readability.py` script | ✅ | commit `a752eb3` |
| AI-4..AI-9 | Schema + copy work | ⬜ | see Wave E (AI-3 absorbed into PDP-2 in Wave G; AI-10..AI-11 in backlog) |

---

## Open questions / decisions pending

1. **Canonical nav** — landing pages render `Shop · Brands · Verticals · Our work · Services · About`, spec says `Shop Furniture · Industries · Brands · Services · About`. NAV-1 needs Steve's call.
2. **brand-dealer reconciliation** — section file is on a separate branch, suffix is in the gate. Merge or de-gate? (PB-13)
3. **BBI logo** — `bbi-logo-v2` is Brant Basics wordmark. Lock it or source a true BBI wordmark? (CONTENT-1)
4. **Smart Collection migration timing** — confirmed: before Phase 3 (Wave B step 1)
5. **Customer Stories source content** — CS-1 (Wave G) needs 5–8 testimonials with photos. Pull from `data/oci-photos/catalog.json` (project photos) + voice-samples.md, or does Steve have testimonial copy approved by clients we can quote on the public site? Permission matters for Review schema.

---

## File update protocol

When you ship a row:

1. Edit this file's row to ✅, fill the Evidence column with the git SHA or live URL.
2. Commit in the same change as the work (`feat: P2-2 Seating category page (closes BUILD-STATE row)`).
3. Update `docs/plan/bbi-interlinking-map.md` if the row affects cross-links.
4. Re-run `/bbi-lp-audit` if the row is a page; expect green.

When you find drift (row says ✅ but file/URL is missing):

1. Don't change the row — investigate first.
2. If the work was reverted, mark ⬜ and note why.
3. If the row was never true, mark ⬜ and note the original commit was wrong.
