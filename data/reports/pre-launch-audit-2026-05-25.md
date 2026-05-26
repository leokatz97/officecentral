# Pre-Launch Audit Report — 2026-05-25

**Auditor:** Claude Code (PRE-LAUNCH-AUDIT-1)
**Run at:** 2026-05-25 evening, Day 11 launch day
**Branch:** `feature/collection-img-pull-1` at `ab3b537` (3 commits pushed during this audit, Phase 1)
**LIVE theme:** 178274435385 (untouched today — verified)
**DEV theme:** 186373570873 (in sync with local)

---

## Executive summary

- **Status: ✅ READY FOR LAUNCH** — no critical findings. LIVE theme integrity confirmed. DEV renders cleanly on all 8 key URLs with zero Liquid errors. Theme-check baseline (2855 offenses) unchanged from the PR-1/PR-2 reference state. The 3 Phase 1 commits are pushed.
- **Critical findings: 0**
- **Should-fix (recommended pre-launch): 4**
- **Nuisance (post-launch backlog): 6**
- **Build-state drift: ~19 Day 11 commits unlogged + DO NEXT #1 already shipped but not moved to COMPLETED**
- **Estimated time to launch-ready: ~50 min** to clear should-fixes 1–3 and sync build-state, if Leo wants those done pre-LAUNCH-2. None of the should-fixes are launch blockers.

---

## Phase 1 — Uncommitted work

**Starting state:** 3 modified files (header polish), 27+ untracked paths, 1 stash, 1 surprise root-level `snippets/` directory.

**Commits fired during this audit (3, pushed to `origin/feature/collection-img-pull-1`):**

| SHA | Message | Files |
|---|---|---|
| `65458f6` | HEADER-POLISH: 2× logo, 140px bar, 21px nav (Day 11 launch polish) | 3 theme files, +10/-9 |
| `02668a6` | tooling: add bbi-preview-dev + bbi-wire-hero-image helper scripts | 2 new scripts, +252 |
| `ab3b537` | gitignore: stray Avada `snippets/` + build-state backups | .gitignore +7 lines |

**Group 2 (homepage border fix):** ✅ already committed as `2cbd469` + `cecabd7` before audit start — nothing to do.

**Remaining uncommitted (Group 4 — session scratch, intentionally not committed):**
- `data/working/{brand-img,collection-img-pull,customer-stories,hp-featured,industry-heroes}-2026-05-25/` — ~300 raw + processed image artifacts. Deliverables already shipped to Shopify Files via the Day 11 commits; these are scratch.
- `data/reports/smart-collections-20260520_163408.csv`, `data/research/image-uploads-log-2026-05-25.md`, `data/strategy/_path-z-products.json`, `data/strategy/_path-z-results.pkl` — session scratch / strategy data, non-launch-blocking.
- `data/working/collection-img-pull-2026-05-25/SWAP-{boardroom,tables}-2.jpg` — files matching the two HALT-2 flagged slots in the COLLECTION-IMG-PULL-1 build-state entry; likely intentional hand-swap candidates.

**Diff totals of the 3 audit commits:** +269 / -9 across 6 files.

---

## Phase 2 — Branch state

| Branch | Local commits | Ahead/behind main | Tracks remote? | Status |
|---|---|---|---|---|
| `main` | — | (base) | ✓ in sync | clean |
| `feature/collection-img-pull-1` (current) | tip = `ab3b537` | many ahead (image work) | ✓ in sync | active |
| `feature/a11y-phase-1.5` | 0 ahead | 0 ahead / 37 behind | ✓ | **merged — safe to delete** |
| `feature/stage-4b-pdp-design-parity` | 9 ahead, 4 unpushed | 9 ahead / 196 behind | ✓ | stale 17d; likely superseded |
| `feature/ds-0-screen-exports-audit` | 4 ahead | 4 ahead / 312 behind | ❌ **NO REMOTE** | **AT RISK** — verify commits ported to main, then delete or push |

**Stale agent branches:** 193 `claude/*` branches, all last touched 2026-04-21 → 2026-05-07 (18+ days idle). No commits in last 18 days. Post-launch cleanup target.

**Open PRs (4, all from stale `claude/*` branches, 2026-04-22 → 2026-05-04):**
- [#5](https://github.com/leokatz97/officecentral/pull/5) Variant swatches LIVE: 42-colour case ladder + theme baseline
- [#3](https://github.com/leokatz97/officecentral/pull/3) Lock templates 4 + 5 designs (Landing OECM + PDP unbuyable)
- [#2](https://github.com/leokatz97/officecentral/pull/2) PE-1/3/7 pipeline fixes from 2026-05-01 review
- [#1](https://github.com/leokatz97/officecentral/pull/1) Product enrichment priority queue + Upwork handoff package

All look superseded by Day 6–11 work. Close / triage post-launch.

**Stash:** 1 entry from `feature/stage-4b-pdp-design-parity` (2026-05-08), single file `data/reports/stage-4b-pdp-design.md` (69 lines). Safe to discard post-launch.

---

## Phase 3 — DEV theme verification

### A. Asset list
- DEV theme `186373570873` asset count: **347** (109 snippets, 101 sections, 85 assets, 47 templates, 2 config, 2 layout, 1 locales).
- 28 key files checked for presence: **28/28 present.**
- Most-recently-updated DEV assets all map to today's commit log:
  - `assets/bbi-homepage.css` 20:04 — HOMEPAGE-BORDERS (`cecabd7`)
  - `templates/index.json` 19:58 — homepage iteration
  - `templates/page.{non-profit,professional-services,industries}.json` 19:44–19:48 — INDUSTRY-HEROES + INDUSTRIES-HUB-TILES
  - `assets/header.css` / `sections/header.liquid` / `snippets/header-logo.liquid` 18:37 — HEADER-POLISH (pushed before this audit's commit, content matches)

### B. DEV ↔ local content drift
- 14 files compared (text hash + JSON-structural).
- **Apparent byte drift on 5 templates was investigated and ruled NOT-DRIFT:** `templates/index.json`, `templates/page.non-profit.json`, `templates/page.industries.json`, `templates/collection.business-furniture.json`, `templates/collection.seating.json` all parse to **byte-identical JSON structure** (even key-order-preserved). Shopify Admin stores JSON with different whitespace/indentation than the local repo files. **Zero structural drift.**
- 9 files MATCH local exactly. **Local fully in sync with DEV; no out-of-repo pushes detected.**

### C. Shopify Files cross-reference
- **153 files uploaded today** (paginated past the 100-edge initial query).
- 146 / 153 BBI-prefixed (`bbi-coll-img-*` 119, `bbi-brand-*` 18, `bbi-page-img-*` 4, `bbi-hp-*` 3, `bbi-cs-*` 2). All map to today's commits.
- **7 non-BBI-prefixed uploads** (flagged as should-fix #3):
  - `istockphoto-1222545492-2048x2048.jpg` (03:17), `Untitled_design_54.png` (12:22), `homepage-product.png` (18:46)
  - `featured-{1,2,3}-*.jpg` (18:59–19:03) — match the homepage `bbi-featured` work but skipped the BBI prefix
  - `desks-hero.jpg` (19:18)
- 0 uploads yesterday (2026-05-24). All Files activity is today.

### D. `shopify theme check` (local theme dir)
- **Files scanned: 166 with offenses · Total offenses: 2855 (2051 error, 804 warning).**
- **Identical to the PR-1/PR-2 baseline** referenced in build-state Day 10 ("265 files / 2855 offenses across 166 files"). **Zero new offenses introduced by Phase 1 commits.**
- Top rules: `ValidSchemaTranslations` 1981 (70% of all offenses, pre-existing inherited Foxtheme schemas), `VariableName` 615, `HardcodedRoutes` 127, `LiquidHTMLSyntaxError` 44.

---

## Phase 4 — LIVE theme integrity ✅ CLEAN

- **LIVE theme `updated_at`: 2026-05-16T16:47:22-04:00** (9 days ago).
- **Zero LIVE assets** have `updated_at` starting with 2026-05-25.
- Spot-checked 5 LIVE assets: `layout/theme.liquid` 2026-05-10, `templates/index.json` 2026-02-03, `sections/header.liquid` 2025-05-27; BBI-specific snippets (`bbi-homepage.css`, `bbi-quote-modal.liquid`) intentionally not present on LIVE (DEV-only).
- Newest LIVE asset is `sections/ds-pdp-base.liquid` at 2026-05-11 — predates the audit-relevant window. The 2026-05-10 push to `layout/theme.liquid` referenced in the safety preflight is the historical incident, NOT a new event.
- **Conclusion: LIVE has not been touched during today's session. Integrity confirmed.**

---

## Phase 5 — Breakage checks (DEV preview)

All checks use the preview-cookie mechanism documented in [scripts/bbi-preview-dev.py](scripts/bbi-preview-dev.py) with `_ab=0&_fd=0&_sc=1` params on every URL (naive `myshopify.com/<path>` requests get redirected to the custom domain and drop the preview cookie — caught + corrected mid-Phase 5).

| URL | HTTP | Theme | Liquid err | App err | `<title>` | JSON-LD | DEV markers |
|---|---|---|---|---|---|---|---|
| `/` | 200 | 24 (DEV) | ✗ | ✗ | ✓ | ✓ | bbi-homepage.css, bbi-quote-modal |
| `/collections/seating` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | bbi-* assets, quote-modal |
| `/pages/non-profit` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |
| `/pages/professional-services` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |
| `/pages/healthcare` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |
| `/pages/industries` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |
| `/pages/contact` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |
| `/pages/quote` | 200 | 24 | ✗ | ✗ | ✓ | ✓ | ↑ |

**`{{ }}` / `{% %}` "leak" signal:** 20 occurrences on the homepage — all are from inline JSON config of a 3rd-party reviews widget (`badge_n_reviews_text: "{{ n }} review/reviews"` etc.) — **not actual Liquid leakage from BBI templates.**

**Image HEAD check (first 8 images on DEV homepage):** **8/8 return 200.** Logos + collection heroes + hp-featured all live on Shopify CDN.

### Today-fixed item verification

**HEADER POLISH (commit `65458f6`):**
- `--logoWidth` rendered: ✅ **300px** (was 150px → ×2 multiplier confirmed) — via inline `<style>` from `sections/header.liquid` if/when rendered.
- ⚠️ **CRITICAL OBSERVATION:** the BBI homepage and all 4 other tested landing pages load only 2 CSS files (`bbi-homepage.css` + `information-drawer.css`). **`header.css` is NOT loaded on any BBI landing page.** The DOM also has zero `.primary-header-blocks` or `.nav-menu-link` class references — BBI uses a different header (`.bbi-qm-header` from the BBI sitewide stack), not the Avada/Foxtheme `sections/header.liquid`. **The bar-height (75→140px) and nav-size (14→21px) edits in `theme/assets/header.css` have NO visible effect on BBI landing pages.** Logo-width 2× DOES render where `header-logo.liquid` is invoked. See should-fix #1.

**BORDER FIX (commits `2cbd469` + `cecabd7`):**
- ✅ `--bbi-line: #E5E5E7` token defined in :root.
- ✅ `var(--bbi-line)` referenced 17 times in `bbi-homepage.css`.
- ✅ `var(--borderColor)` reference count: 0 (replaced).
- ⚠️ Raw RGB `229,229,231` still appears 2 times — should also be tokenized. See should-fix #4.

**H1 SIZING:**
- ✅ `.hp-hero__title font-size: clamp(36px,4.6vw,64px)` — clamp() values present.

**PREVIEW SCRIPT (commit `02668a6`):**
- ✅ `scripts/bbi-preview-dev.py --verify` → exit 0, "OK: dev theme is being rendered."

---

## Phase 6 — Build-state.md deltas

Build-state was last updated EOD Day 10 (2026-05-24). Today's Day 11 work substantially exceeds what the DO NEXT queue anticipated.

### A. ⏳ READY items in DO NEXT that have actually shipped
| DO NEXT # | Item | Actual state | Evidence |
|---|---|---|---|
| #1 | HIGH-3 fix `product-form-buttons.liquid:30` | **✅ SHIPPED** | commit `7fb46b7` 2026-05-24 12:01, on `main` and current branch |
| #2 | Cornerstone Post 1 visual spot-check | not commit-trackable | post is LIVE at `/blogs/news/oecm-...` |
| #3 | Image swap pipeline prep | superseded | actual image work happened directly (no pipeline) |
| #4 | W0-1 + W0-3 final verify | not commit-trackable | Steve handled |
| #6 | Step 46 IMAGE SWAP | parenthetical says **✅ CLOSED 2026-05-25** in line 31 of queue, but row still has 🔒 BLOCKED flag (inconsistent) | 119 collection image uploads + 18 brand + 4 page-img + 3 hp-featured + 2 customer stories shipped today |

**DO NEXT queue is stale; needs sync.**

### B. Today's commits NOT logged in build-state (since Day 10 EOD)

Build-state logs ONE Day 11 entry (COLLECTION-IMG-PULL-1 in COMPLETED archive, lines 66–69, marked "commit pending"). The actual Day 11 commit count is ~20. Unlogged:

| Commit | Description | Suggested row |
|---|---|---|
| `7fb46b7` | HIGH-3 fix product-form-buttons (Day 10 12:01, labeled "Day 11 #1") | move DO NEXT #1 → COMPLETED |
| `0d3d1ba` | COLLECTION-IMG-PULL-1 53-slot | record SHA on existing entry |
| `edf3207`, `a85be7c`, `7da3d74` | COLLECTION-IMG-PULL-1 swap + v3 contain + v4 polish | record on existing entry |
| `2cbd469`, `cecabd7` | HOMEPAGE-BORDERS (--bbi-line token) | new sub-row |
| `71b0d05`, `401c4df`, `1fa3cff` | BRAND-IMG-1 (12 brand slots + contain/cover follow-ups) | new sub-row under Wave E image work |
| `71c2e97` | Customer stories story4 + story5 populated | new sub-row |
| `8dd62b6` | Homepage hero H1 + 4 shop tiles + 5 industry tiles | new sub-row |
| `b60a47c`, `e884b57`, `b915800`, `3c5bf43`, `40510cb` | Homepage bbi-featured iteration (5 commits) | consolidate into one sub-row |
| `a0ffa99` | INDUSTRY-HEROES non-profit + pro-services | new sub-row |
| `0be4c2c`, `b07b2af` | INDUSTRIES-HUB-TILES + HOMEPAGE-INDUSTRY-TILES | new sub-row |
| `d0fcef4` | Session recap doc | meta entry |
| `d3fd023`, `4047a19` | Image slot inventory + Upwork gap analysis | already cited; needs SHA |
| `34fd438` | Image bucket A/B workflow (on main) | already cited; needs SHA |
| `65458f6` | HEADER-POLISH (this audit) | new sub-row — flag as no-BBI-effect per should-fix #1 |
| `02668a6` | bbi-preview-dev + bbi-wire-hero-image tooling | new tooling row |
| `ab3b537` | gitignore Avada snippets + build-state backups | new tooling row |

### C. Day 10 discoveries still open (per build-state lines 176–181)
- `DATAFORSEO-403` — still open
- **`STALE-OECM-DATE-FIX`** — **still open** (verified: `ds-lp-about.liquid:113` body + `:245` schema still say "OECM Supplier Partner since 2019"). See should-fix #2.
- `LEAD-HIGH-2 no-JS modal fallback` — still open (deferred)
- `CORNERSTONE-1-IMG` — still open (waits on Upwork)
- `LEAD-INBOX-1 per-type routing` — still open

### D. /54 step count
- Build-state header says **43 of 54 (80%)** as of Day 10 EOD.
- Today's work didn't close additional numbered steps (Step 46 IMAGE SWAP is the natural candidate; build-state already marked it "✅ CLOSED 2026-05-25" inline at queue line 31 but didn't move it to COMPLETED). If Step 46 is genuinely closed, the count moves to **44/54 (81.5%)**. Decision belongs to Leo (Upwork delivery integration may still be pending).

---

## Critical findings (must fix before launch)

**None.**

---

## Should-fix (recommended pre-launch)

1. **HEADER-POLISH commit modifies CSS not loaded on BBI surface.** [theme/assets/header.css](theme/assets/header.css) `.primary-header-blocks min-height: 140px` and `.nav-menu-link font-size: 21px / padding: 23px` will not render on any BBI landing page — `header.css` isn't loaded and those class names aren't in the BBI DOM. Logo 2× DOES render via [theme/snippets/header-logo.liquid](theme/snippets/header-logo.liquid) where invoked. **Decision needed:**
   - Option A (do nothing) — accept that the bar/nav portion of `65458f6` is dead code on BBI; the changes only matter if some legacy Avada surface still resolves post-launch.
   - Option B (~15 min) — move the bar-height + nav-size rules to [theme/assets/bbi-homepage.css](theme/assets/bbi-homepage.css) targeting whatever class the BBI header actually uses (likely `.bbi-qm-header` family) so the visual intent manifests.
   - Recommendation: pick Option A unless Leo specifically intended a BBI-page visual change.

2. **STALE-OECM-DATE-FIX unresolved.** [theme/sections/ds-lp-about.liquid:113](theme/sections/ds-lp-about.liquid:113) body and [theme/sections/ds-lp-about.liquid:245](theme/sections/ds-lp-about.liquid:245) schema default both still say *"OECM Supplier Partner since 2019."* Canonical fact (Day 8 STEVE-FACT-CHECK) is **Agreement 2025-470** framing, applied consistently elsewhere. Two edits, ~5 min. Already flagged in build-state Day 10 discoveries — slipped through Day 11.

3. **7 non-BBI-prefixed Shopify Files uploads today** (see Phase 3C). Likely manual Admin uploads. Either rename to `bbi-*` convention for consistency or annotate origin. Not a launch blocker. ~5 min if renaming, 0 min if accepting.

4. **Border tokenization incomplete in `bbi-homepage.css`.** 2 occurrences of raw RGB `229,229,231` remain after the `--bbi-line` token introduction. Replace with `var(--bbi-line)` for consistency. ~2 min.

---

## Nuisance (post-launch backlog)

1. **193 stale `claude/*` agent branches** (no commits in 18+ days). 198 total local branches. Cleanup with `git branch -D claude/*` once Leo confirms none of those branches have unmerged work he wants to recover.
2. **4 open PRs from `claude/*` branches** (2026-04-22 → 2026-05-04) — close/triage post-launch.
3. **1 stash** from 2026-05-08 (`data/reports/stage-4b-pdp-design.md`, 69 lines). Apply, save, or `git stash drop` post-launch.
4. **`feature/stage-4b-pdp-design-parity` branch** — 9 ahead of main, 4 unpushed locally, last commit 2026-05-08. Verify intent (likely superseded) before deleting.
5. **`feature/ds-0-screen-exports-audit` branch** — 4 ahead, **no remote tracking** (AT-RISK status). Contains "DS-0 / DS-1 / DS-2 complete" commits. Build-state says DS-0 → DS-4 are COMPLETE in `docs/plan/track-d-design-system/README.md`, so the commits likely got ported. Cross-check then delete or push.
6. **2855 theme-check offenses** (1981 `ValidSchemaTranslations` + 615 `VariableName` + 127 `HardcodedRoutes`). Baseline unchanged — all are pre-existing Foxtheme inheritance. Schedule a post-launch hygiene pass.

---

## Cleanup actions taken (Phase 1 commits during this audit)

3 commits pushed to `origin/feature/collection-img-pull-1`:
1. `65458f6` HEADER-POLISH (per Leo's Group 1 spec)
2. `02668a6` tooling: bbi-preview-dev + bbi-wire-hero-image
3. `ab3b537` gitignore: stray Avada `snippets/` + build-state `.bak-*` backups

Working tree is now clean of all tracked file modifications. Remaining untracked entries are intentional session scratch (Group 4).

---

## Recommended next steps for Leo

In priority order (~50 min total to clear should-fixes 1–3 + build-state sync, OR ~5 min to skip the cosmetic ones and just sync build-state):

1. **Decide should-fix #1 (HEADER-POLISH dead code):** Option A (accept) or Option B (port to bbi-homepage.css). If Option A, no action needed.
2. **Fire should-fix #2 (STALE-OECM-DATE-FIX) — 5 min.** Two surgical edits to `ds-lp-about.liquid` lines 113 + 245, push via `bbi-push-landing.py --slug about`. Removes a known Day-10-discovery item that contradicts the locked Day-8 facts.
3. **Sync build-state.md — 30 min.** Add the ~19 unlogged Day 11 commits, move DO NEXT #1 to COMPLETED, resolve the Step 46 inconsistency (queue says CLOSED inline but row flag still 🔒). Phase 7 offers to do this as a single commit.
4. **Run SYS-VERIFY-1 Phase 2 re-run (DO NEXT #8) — ~30 min.** Light re-verify against the image rounds shipped today before LAUNCH-0. Optional but in the queue.
5. **Then proceed: LAUNCH-0 → LAUNCH-1 → LAUNCH-2 chain.** No blockers identified.

---

## Appendix

### A.1 Branch breakdown (full)
- Local human branches: 5 (`main`, `feature/collection-img-pull-1`, `feature/a11y-phase-1.5`, `feature/stage-4b-pdp-design-parity`, `feature/ds-0-screen-exports-audit`).
- Local `claude/*` agent branches: 193.
- Total local: 198.
- Remote tracked (non-claude): 4 (the four `feature/*` branches that have origin counterparts; `ds-0-screen-exports-audit` has no remote).

### A.2 DEV asset categories (347 total)
- snippets: 109 · sections: 101 · assets: 85 · templates: 47 · config: 2 · layout: 2 · locales: 1.

### A.3 Shopify Files breakdown today (153 uploads)
- `bbi-coll-img-*`: 119 (COLLECTION-IMG-PULL-1)
- `bbi-brand-*`: 18 (BRAND-IMG-1)
- `bbi-page-img-*`: 4 (INDUSTRY-HEROES + INDUSTRIES-HUB-TILES)
- `bbi-hp-*`: 3 (homepage bbi-featured)
- `bbi-cs-*`: 2 (customer stories)
- Non-BBI: 7 (see should-fix #3)

### A.4 Theme-check rule breakdown (2855 offenses)
```
1981  ValidSchemaTranslations
 615  VariableName
 127  HardcodedRoutes
  44  LiquidHTMLSyntaxError
  33  UnusedAssign
  13  UndefinedObject
   8  AssetPreload
   8  TranslationKeyExists
   7  ImgWidthAndHeight
   6  MissingAsset
   6  DeprecatedFilter
   3  UnknownFilter
   2  RemoteAsset
   1  ValidSchema
   1  MissingTemplate
```

### A.5 Phase 1 diff summaries

#### `theme/assets/header.css` (8 lines changed)
```
.primary-header-blocks min-height: 75px → 140px
.nav-menu-link padding: 15px → 23px
.nav-menu-link font-size: 14px → 21px (in 2 places)
```

#### `theme/sections/header.liquid` (2 lines)
```
--logoWidth:{{ section.settings.logo_width }}px
→ --logoWidth:{{ section.settings.logo_width | times: 2 | round }}px
```

#### `theme/snippets/header-logo.liquid` (9 lines)
- new local var `logo_w_display = logo_width × 2`
- `image_url width: 200 → 500`
- widths array `'50, 100, 150, 200, 250' → '100, 200, 300, 400, 500'`
- height/width attrs computed off `logo_w_display`

### A.6 Surprise findings during audit
- Root-level `./snippets/` directory with 98 stale Avada theme files (dated 2026-05-11 12:10) — origin: misdirected `shopify theme pull` ran from repo root instead of `theme/`. Resolved by adding `/snippets/` to `.gitignore` in commit `ab3b537`.
- Initial Phase 5 fetch was hitting LIVE (not DEV) because plain `https://office-central-online.myshopify.com/<path>` redirects to the custom domain and drops the preview cookie. The `bbi-preview-dev.py` script's docstring explains the fix (`_ab=0&_fd=0&_sc=1` on every URL). Re-ran with correct params — all 8 URLs then served from DEV theme 24.
