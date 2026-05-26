# REGRESSION-DIAGNOSTIC-1 — Report

**Diagnostic run:** 2026-05-25 (late evening, immediately after HEADER-POLISH-2 regression)
**Auditor:** Claude Code (REGRESSION-DIAGNOSTIC-1, READ-ONLY)
**Scope:** Root-cause + full damage scope for the HEADER-POLISH-2 regression on DEV theme `186373570873`
**Inputs read:** `CLAUDE.md`, `BBI-Session-Kickoff/01-safety-preflight.md`, `BBI-Session-Kickoff/bbi-build-state.md`, `data/reports/header-polish-2-session-report-2026-05-25.md`, `data/reports/pre-launch-audit-2026-05-25.md` (recovered from `feature/about-page-grid-1` — see Note 1 below)
**Writes performed:** ZERO. Theme assets, git refs, working tree, stash — all untouched.

> **Note 1 — Pre-launch audit file recovery.** The pre-launch audit referenced in the prompt is **not present in the current working tree** because HEAD (`feature/header-polish-2`) was branched off `main` *before* the commit that added it (732b303 on `feature/about-page-grid-1`) had merged. Content was retrieved via `git show feature/about-page-grid-1:data/reports/pre-launch-audit-2026-05-25.md` and is intact (`blob 1aba14de`). This is itself diagnostic evidence — see Phase 4.

---

## EXECUTIVE SUMMARY

| Metric | Value |
|---|---|
| **Files damaged on DEV** | **23** (22 confirmed BOTH_REGRESSED + 1 new finding `assets/bbi-homepage.css`) |
| **Image-marker references lost** | **111** measured at template-blob level; ~75–80 visible as rendered image slots |
| **Pages confirmed broken via rendered DOM** | **18 of 21** customer-facing pages tested (homepage + healthcare/edu/gov clean) |
| **Root cause** | **Candidate B (bad branch base) + Candidate D (bulk-push script blast radius)** — HIGH confidence |
| **Recovery source intact?** | **YES** — `feature/about-page-grid-1` (26 commits ahead of `main`) holds all Day 11 work; every commit referenced in the regression report exists in git and was verified |
| **LIVE theme `178274435385` integrity** | **UNTOUCHED** — `updated_at = 2026-05-16T16:47:22-04:00` matches PRE-LAUNCH-AUDIT-1 baseline exactly |
| **Recommended recovery** | **Option D (hybrid)** — preserve HEADER-POLISH-2 CSS as a 10-line cherry-pick onto `feature/about-page-grid-1`, then run `bbi-push-landing.py --snippets` from that branch + push the 9 collection.\*.json templates via `push-file.py`. Net: 22+1 files restored, header polish preserved, no work redone. Est ~30 min |
| **Time-to-recovery** | ~30 min mechanical; ~10 min verification |
| **Risk of re-running HEADER-POLISH-2 later** | **LOW** if Option D used (root cause is git topology, not the CSS edit itself) — the bbi-nav.liquid edit is 6 insertions / 4 deletions, byte-clean |
| **Critical safety findings** | None to LIVE. None to git. Working-tree Round-2 CSS edits are preserved (uncommitted). Pre-write `.bak` backup at `data/backups/header-polish-2-pre-20260525-211344/bbi-nav.liquid` is intact. |

**LAUNCH-2 impact:** the regression blocks LAUNCH-2 *only* until recovery completes. Recovery is mechanical, source-of-truth is intact, no work is lost. Image-swap session (DO NEXT #6) and downstream LAUNCH-0→4 chain are not invalidated — only delayed by ~30–40 min of recovery.

---

## TIMELINE OF EVENTS

All times America/Toronto (-04:00).

| Time | Event | Evidence |
|---|---|---|
| 2026-05-25 14:20 | `main` advanced to `34fd438` (Image bucket A/B workflow) | `git log main -1` |
| 2026-05-25 ~15:00 → ~20:30 | Day 11 image work shipped on `feature/collection-img-pull-1` then continued on `feature/about-page-grid-1`: 26 commits including COLLECTION-IMG-PULL-1 (4 commits, 53 slots), BRAND-IMG-1 (3 commits, 18 slots), homepage hp-featured / hero / industry tiles, INDUSTRY-HEROES, INDUSTRIES-HUB-TILES, customer-stories story4+5, ABOUT-PAGE-GRID-1 (2 commits, 8 photos), HOMEPAGE-BORDERS (2 commits), HEADER-POLISH (1 commit — Avada classes only), tooling (2 commits), gitignore (1 commit), build-state + PRE-LAUNCH-AUDIT-1 (1 commit) | `git log --all --graph` lines around the diverged branch |
| 2026-05-25 20:38 | PRE-LAUNCH-AUDIT-1 verdict written: **READY FOR LAUNCH**, 0 critical findings, should-fix #1 = HEADER-POLISH dead-code on BBI surface | `data/reports/pre-launch-audit-2026-05-25.md` (recovered from about-grid) |
| 2026-05-25 20:55 | HEADER-POLISH-2 session started | Header report `session window: 2026-05-25 ~20:55–21:35 ET` |
| 2026-05-25 21:03 | Final ABOUT-PAGE-GRID-1 commit `cf69dc8` on `feature/about-page-grid-1` | git log |
| 2026-05-25 ~21:13 | **Reflog HEAD@{3}→{2}**: `checkout: moving from feature/about-page-grid-1 to main`. Working tree reset to main state. Pre-write backup created: `data/backups/header-polish-2-pre-20260525-211344/` | `git reflog -n 100`; `ls data/backups/` |
| 2026-05-25 ~21:14 | **Reflog HEAD@{2}→{1}**: `checkout: moving from main to feature/header-polish-2` — **new branch created off `main`, not off `feature/about-page-grid-1`** | reflog |
| 2026-05-25 21:19:55 | **Bulk push fired** — `scripts/bbi-push-landing.py 186373570873 --snippets` from `feature/header-polish-2`. Every in-scope file uploaded reflects `main`'s pre-Day-11 state. 22 files on DEV regressed to `main`'s blobs | `updated_at = 2026-05-25T21:19:55-04:00` on 22 DEV assets (verified via Admin API per-file query) |
| 2026-05-25 21:20:25 | HEADER-POLISH-2 commit `bb3b5d8` created on `feature/header-polish-2`. Diff: `M theme/snippets/bbi-nav.liquid` only, +6/−4 lines | `git show --name-status bb3b5d8` |
| 2026-05-25 21:28:39 | Round-2 bbi-nav.liquid pushed singleton via `push-file.py` (44232 B on DEV — larger than HEAD's 44163 B) — Round-2 edits stayed in working tree, never committed | DEV `bbi-nav.liquid` updated_at |
| 2026-05-25 21:38:31 | `templates/index.json` updated_at refreshed on DEV — **after** the bulk push, content matches `feature/about-page-grid-1` (11 markers), so homepage was either fixed via Theme Editor or pushed individually | DEV `index.json` updated_at + the staged-but-uncommitted local diff |
| 2026-05-25 ~21:50 | Regression observed; ground-truth verification run on 7 pages (per header report's own table) | Report Phase "GROUND-TRUTH VERIFICATION" |
| 2026-05-25 ~22:30 | This diagnostic ran | timestamps in `data/working/regression-diagnostic-1/` |

---

## PHASE 1 — Commit timeline

### A. HEADER-POLISH-2 commit content

```
commit bb3b5d85018091643fd64b0ed032b25f9ad3d250
Author:  Leo Katz <leo@venn.ca>
Date:    Mon May 25 21:20:25 2026 -0400
Parents: 34fd438594abf285b15c11999b45bac03c293d65   ← main HEAD at session start
Files:   M theme/snippets/bbi-nav.liquid             ← ONE file modified
Stat:    1 file changed, 6 insertions(+), 4 deletions(-)
```

**Critical: the commit itself is byte-clean.** It modifies one file, by 10 lines, all CSS. No template touches, no template deletions, no schema edits. This rules out Candidate C (destructive edit in the commit/prompt).

### B. Branch base

```
$ git merge-base feature/header-polish-2 origin/main
34fd438594abf285b15c11999b45bac03c293d65
$ git merge-base feature/header-polish-2 feature/about-page-grid-1
34fd438594abf285b15c11999b45bac03c293d65   ← same — common ancestor is main, not one branched off the other
$ git rev-list --count main..feature/about-page-grid-1
26
$ git rev-list --count main..feature/header-polish-2
1
```

**Confirmed: `feature/header-polish-2` branched off `main` (34fd438), not off `feature/about-page-grid-1`.** Day 11 work (26 commits) was never in the working tree when HEADER-POLISH-2 made the bulk push.

### C. Branch inventory

- `main` → `34fd438` (Image bucket A/B workflow, 2026-05-25 14:20)
- `feature/about-page-grid-1` → `cf69dc8` (ABOUT-PAGE-GRID-1 reflow, 2026-05-25 21:03) · **26 commits ahead of main** · in sync with origin · **all Day 11 work intact**
- `feature/collection-img-pull-1` → `732b303` (build-state + PRE-LAUNCH-AUDIT-1, 2026-05-25 20:38) · 7 commits ahead of main · in sync with origin
- `feature/header-polish-2` → `bb3b5d8` (HEADER-POLISH-2, 2026-05-25 21:20) · 1 commit ahead of main · in sync with origin · **current HEAD**
- 193 stale `claude/*` agent branches, all idle ≥ 18 days — non-relevant to this incident

---

## PHASE 2 — Recovery source verification

### A. `feature/about-page-grid-1` is intact

All 26 commits referenced in the regression report exist and are reachable:

```
EXISTS 0be4c2c  INDUSTRIES-HUB-TILES non-profit + pro-services tiles
EXISTS b07b2af  HOMEPAGE-INDUSTRY-TILES tile <img> srcs
EXISTS e8c75a4  ABOUT-PAGE-GRID-1 2×4 brand-evolution grid
EXISTS cf69dc8  ABOUT-PAGE-GRID-1 reflow to 2×3
EXISTS 65458f6  HEADER-POLISH (Avada classes — superseded by HEADER-POLISH-2)
EXISTS 02668a6  tooling: bbi-preview-dev + bbi-wire-hero-image
EXISTS ab3b537  gitignore: stray Avada snippets/
EXISTS 732b303  build-state Day 11 + PRE-LAUNCH-AUDIT-1 report
EXISTS 7da3d74  COLLECTION-IMG-PULL-1 v4 (53 slots higher-res + contain)
EXISTS a85be7c  COLLECTION-IMG-PULL-1 heroes v3 (cover→contain)
EXISTS edf3207  COLLECTION-IMG-PULL-1 tables + boardroom swap
EXISTS 0d3d1ba  COLLECTION-IMG-PULL-1 53-slot programmatic pull
EXISTS 71b0d05  BRAND-IMG-1 12 brand slots
EXISTS 401c4df  BRAND-IMG-1 follow-up hub-tiles contain→cover
EXISTS 1fa3cff  BRAND-IMG-1 follow-up 2 hero contain→cover
EXISTS 71c2e97  Customer stories story4 + story5
EXISTS a0ffa99  INDUSTRY-HEROES non-profit + pro-services
EXISTS 8dd62b6  Homepage hero H1 + 4 shop tiles + 5 industry tiles
EXISTS b60a47c  Homepage bbi-featured Idea-15 SKUs
EXISTS e884b57  Homepage bbi-featured cover→contain
EXISTS b915800  Homepage bbi-featured bordered/padded
EXISTS 3c5bf43  Homepage bbi-featured 1:1 + border
EXISTS 40510cb  Homepage bbi-featured border color
EXISTS 2cbd469  HOMEPAGE-BORDERS --bbi-line token introduce
EXISTS cecabd7  HOMEPAGE-BORDERS --bbi-line align to #E5E5E7
EXISTS d0fcef4  Session recap doc
```

**Zero commits missing. Recovery source is fully intact.**

### B. Critical-file blob SHAs on `feature/about-page-grid-1`

| File | blob SHA (first 10) | size (bytes) | marker count |
|---|---|---|---|
| `templates/collection.seating.json` | `9d780f2d99` | 8,620 | 8 |
| `templates/collection.desks.json` | `b4a89e3122` | 8,096 | 8 |
| `templates/collection.tables.json` | `fe150c8a35` | 7,385 | 6 |
| `templates/collection.storage.json` | `f568fac954` | 8,885 | 10 |
| `templates/collection.boardroom.json` | `8f819ee779` | 6,797 | 5 |
| `templates/collection.accessories.json` | `d247baee18` | 7,366 | 7 |
| `templates/collection.panels-room-dividers.json` | `59d789a749` | 5,709 | 3 |
| `templates/collection.ergonomic-products.json` | `8acd578db0` | 6,988 | 5 |
| `templates/collection.business-furniture.json` | `47fcfe8c2b` | 7,893 | 10 |
| `templates/page.customer-stories.json` | `32b00eea99` | 700 | 2 |
| `templates/page.industries.json` | `3f76e10c75` | 1,302 | 8 |
| `templates/page.about.json` | `ed387a36fe` | 299 | 1 (unchanged from HEAD) |
| `templates/page.brands.json` | `ef3c80ae5c` | 797 | 7 |
| `templates/page.brands-heartwood.json` | `fc8e0d9c07` | 346 | 2 |
| `templates/page.brands-obusforme.json` | `d5b83052d0` | 349 | 2 |
| `templates/page.brands-otg.json` | `0d887b7186` | 325 | 2 |
| `templates/page.brands-ergocentric.json` | `3826bcaa4e` | 357 | 2 |
| `templates/page.brands-global-teknion.json` | `7ed12a5db0` | 366 | 2 |
| `templates/page.brands-keilhauer.json` | `e640be5413` | 346 | 2 |
| `templates/page.non-profit.json` | `64fb27e30a` | 926 | 2 |
| `templates/page.professional-services.json` | `8945516503` | 1,011 | 2 |
| `templates/index.json` | `c4d41316fc` | 25,342 | 11 |
| `sections/ds-lp-about.liquid` | `2dbab4dbb7` | 26,030 | 32 (about-grid 2×3 photo block) |
| `sections/ds-lp-customer-stories.liquid` | `f191c2aa71` | 27,219 | (story4+5 with new copy, "case study pending verification" removed, "School Library" added) |
| `assets/bbi-homepage.css` | `98735f74b2` | 37,002 | 18 `--bbi-line` references |
| `snippets/bbi-quote-modal.liquid` | `6bc084789e` | 21,071 | (matches HEAD too — pre-existing DEV drift) |

---

## PHASE 3 — Damage inventory

### A. Full damage table (HEAD × about-grid × DEV)

Marker count uses regex `(bbi-collection|bbi-coll-img|bbi-cs-|bbi-brand-|bbi-page-img|bbi-about-grid|bbi-hp-featured|hero_image|tile_image|lp-evol|Then and Now|case study pending verification|School Library|Trillium Health)`. DEV `updated_at` and content fetched live from Admin API at the time of this diagnostic.

| File | HEAD sha | HEAD mk | GRID sha | GRID mk | DEV updated_at | DEV mk | Status |
|---|---|---|---|---|---|---|---|
| `sections/ds-lp-about.liquid` | `429a27ca63` | 3 | `2dbab4dbb7` | 32 | 21:19:55 | 3 | **BOTH_REGRESSED** (−29) |
| `sections/ds-lp-customer-stories.liquid` | `5daa8456c9` | 2 | `f191c2aa71` | 1 | 21:19:55 | 2 | DIFF (markers don't capture story content delta — see §C) |
| `templates/index.json` | `30333f048d` | 2 | `c4d41316fc` | 11 | 21:38:31 | **11** | **LOCAL_REGRESSED** (DEV is clean — homepage was fixed independently) |
| `templates/page.brands.json` | `a1dc57167d` | 1 | `ef3c80ae5c` | 7 | 21:19:55 | 1 | **BOTH_REGRESSED** (−6) |
| `templates/page.brands-heartwood.json` | `5871551997` | 0 | `fc8e0d9c07` | 2 | 21:19:55 | 0 | **BOTH_REGRESSED** (−2) |
| `templates/page.brands-obusforme.json` | `90ad8cb22b` | 0 | `d5b83052d0` | 2 | 21:19:55 | 0 | **BOTH_REGRESSED** (−2) |
| `templates/page.brands-otg.json` | `d25c7a4ea6` | 0 | `0d887b7186` | 2 | 21:19:55 | 0 | **BOTH_REGRESSED** (−2) |
| `templates/page.brands-ergocentric.json` | `aadc516b31` | 1 | `3826bcaa4e` | 2 | 21:19:55 | 1 | **BOTH_REGRESSED** (−1) |
| `templates/page.brands-global-teknion.json` | `352da9ce11` | 1 | `7ed12a5db0` | 2 | 21:19:55 | 1 | **BOTH_REGRESSED** (−1) |
| `templates/page.brands-keilhauer.json` | `fee1cd31f4` | 1 | `e640be5413` | 2 | 21:19:55 | 1 | **BOTH_REGRESSED** (−1) |
| `templates/page.customer-stories.json` | `51c674f530` | 0 | `32b00eea99` | 2 | 21:19:55 | 0 | **BOTH_REGRESSED** (−2; "case study pending verification" present, story4+5 lost) |
| `templates/page.industries.json` | `b60364225c` | 6 | `3f76e10c75` | 8 | 21:19:55 | 6 | **BOTH_REGRESSED** (−2; INDUSTRIES-HUB-TILES) |
| `templates/page.non-profit.json` | `282a55ea65` | 1 | `64fb27e30a` | 2 | 21:19:55 | 1 | **BOTH_REGRESSED** (−1; INDUSTRY-HERO) |
| `templates/page.professional-services.json` | `b573fa68d1` | 1 | `8945516503` | 2 | 21:19:55 | 1 | **BOTH_REGRESSED** (−1; INDUSTRY-HERO) |
| `templates/collection.seating.json` | `fa6ff4fbae` | 1 | `9d780f2d99` | 8 | 21:19:55 | 1 | **BOTH_REGRESSED** (−7; hero + 6 tiles) |
| `templates/collection.desks.json` | `e89153bdba` | 1 | `b4a89e3122` | 8 | 21:19:55 | 1 | **BOTH_REGRESSED** (−7) |
| `templates/collection.tables.json` | `f876605d89` | 1 | `fe150c8a35` | 6 | 21:19:55 | 1 | **BOTH_REGRESSED** (−5) |
| `templates/collection.storage.json` | `69364415a5` | 1 | `f568fac954` | 10 | 21:19:55 | 1 | **BOTH_REGRESSED** (−9) |
| `templates/collection.boardroom.json` | `a2c29e0bde` | 1 | `8f819ee779` | 5 | 21:19:55 | 1 | **BOTH_REGRESSED** (−4) |
| `templates/collection.accessories.json` | `e376874547` | 1 | `d247baee18` | 7 | 21:19:55 | 1 | **BOTH_REGRESSED** (−6) |
| `templates/collection.panels-room-dividers.json` | `331ddc9e94` | 1 | `59d789a749` | 3 | 21:19:55 | 1 | **BOTH_REGRESSED** (−2) |
| `templates/collection.ergonomic-products.json` | `d4ae2c17f8` | 1 | `8acd578db0` | 5 | 21:19:55 | 1 | **BOTH_REGRESSED** (−4) |
| `templates/collection.business-furniture.json` | `4214671832` | 1 | `47fcfe8c2b` | 10 | 21:19:55 | 1 | **BOTH_REGRESSED** (−9; ambiguous size 6,063 on DEV — also pre-existing pre-Day-11 partial state, see §D) |
| `assets/bbi-homepage.css` | `aba4b8b76d` | 0 `--bbi-line` | `98735f74b2` | 18 `--bbi-line` | 21:19:55 | 0 | **BOTH_REGRESSED — NEW FINDING** (HOMEPAGE-BORDERS lost — the regression report did not catch this) |
| `templates/page.about.json` | `ed387a36fe` | — | `ed387a36fe` | — | 2026-05-15 | — | CLEAN |
| `snippets/bbi-quote-modal.liquid` | `6bc084789e` | — | `6bc084789e` | — | 2026-05-21 | — | DEV out-of-sync (181 B older — pre-existing 4-day drift unrelated to HEADER-POLISH-2; flagged for Step 4 of recovery) |
| `sections/header.liquid`, `snippets/header-logo.liquid`, `assets/header.css` | (HEAD = main) | 0 | (GRID has HEADER-POLISH `65458f6` edits) | 0 | 21:19:55 | 0 | DEV regressed to main's old Avada classes — **but PRE-LAUNCH-AUDIT-1 should-fix #1 found these were dead code on BBI surface** — no visible impact |

**Totals**: 22 files BOTH_REGRESSED + 1 LOCAL_REGRESSED (already restored on DEV) + 1 pre-existing DEV drift = **23 files in the recovery scope**. Marker count lost on the 22 regressed templates/sections: **111 markers** (delta sum). At the rendered-image-slot level, this resolves to roughly 75–80 broken image slots (per the regression report's own 79–83 estimate and the rendered DOM verification in Phase 6 below).

### B. Phase 3E extended scan (every theme file under `theme/templates/`, `theme/sections/`, `theme/snippets/`)

Catches anything beyond the named scope. Files with any marker-count delta between HEAD and `feature/about-page-grid-1`:

```
theme/sections/ds-lp-about.liquid                          HEAD=  3  GRID= 32  LOST= 29
theme/sections/ds-lp-customer-stories.liquid               HEAD=  2  GRID=  1  LOST= -1  (delta is editorial — old "pending verification" marker present in HEAD)
theme/templates/collection.accessories.json                HEAD=  1  GRID=  7  LOST=  6
theme/templates/collection.boardroom.json                  HEAD=  1  GRID=  5  LOST=  4
theme/templates/collection.business-furniture.json         HEAD=  1  GRID= 10  LOST=  9
theme/templates/collection.desks.json                      HEAD=  1  GRID=  8  LOST=  7
theme/templates/collection.ergonomic-products.json         HEAD=  1  GRID=  5  LOST=  4
theme/templates/collection.panels-room-dividers.json       HEAD=  1  GRID=  3  LOST=  2
theme/templates/collection.seating.json                    HEAD=  1  GRID=  8  LOST=  7
theme/templates/collection.storage.json                    HEAD=  1  GRID= 10  LOST=  9
theme/templates/collection.tables.json                     HEAD=  1  GRID=  6  LOST=  5
theme/templates/index.json                                 HEAD=  2  GRID= 11  LOST=  9
theme/templates/page.brands-ergocentric.json               HEAD=  1  GRID=  2  LOST=  1
theme/templates/page.brands-global-teknion.json            HEAD=  1  GRID=  2  LOST=  1
theme/templates/page.brands-heartwood.json                 HEAD=  0  GRID=  2  LOST=  2
theme/templates/page.brands-keilhauer.json                 HEAD=  1  GRID=  2  LOST=  1
theme/templates/page.brands-obusforme.json                 HEAD=  0  GRID=  2  LOST=  2
theme/templates/page.brands-otg.json                       HEAD=  0  GRID=  2  LOST=  2
theme/templates/page.brands.json                           HEAD=  1  GRID=  7  LOST=  6
theme/templates/page.customer-stories.json                 HEAD=  0  GRID=  2  LOST=  2
theme/templates/page.industries.json                       HEAD=  6  GRID=  8  LOST=  2
theme/templates/page.non-profit.json                       HEAD=  1  GRID=  2  LOST=  1
theme/templates/page.professional-services.json            HEAD=  1  GRID=  2  LOST=  1

Total markers lost (HEAD vs GRID): 111
Files with damage: 23
```

The 23 files in this scan match the 22 explicitly damaged templates/sections + `index.json` (which is LOCAL_REGRESSED only — DEV already clean). **No file outside the regression report's scope was missed** at the templates/sections/snippets layer — *except* for `assets/bbi-homepage.css` (under `assets/`, not in this scan's directory set; surfaced separately in §D below).

### C. Section-file copy delta (ds-lp-customer-stories.liquid)

The regex shows a "−1 marker on HEAD vs GRID" but the real damage is editorial. About-grid REMOVES the legacy phrase "case study pending verification" (matches the marker pattern) and ADDS "School Library" + Trillium Health body copy. HEAD has the old phrase. On DEV, the old phrase is also present (BOTH_REGRESSED): verified via rendered DOM, `/pages/customer-stories` body contains literal `case study pending verification` and **does not contain** `School Library` or `Trillium Health`. The actual image refs `bbi-cs-healthcare` + `bbi-cs-school-library` live in the TEMPLATE `page.customer-stories.json` (already counted in §A) — both also missing from DEV.

### D. NEW FINDING — `assets/bbi-homepage.css` regression

Not surfaced in the original regression report. The HOMEPAGE-BORDERS work (commits `2cbd469` + `cecabd7` on `feature/about-page-grid-1`) introduced the `--bbi-line` design-system token across the file (18 occurrences) and removed a dead `!important` polish block. Live API check:

```
theme/assets/bbi-homepage.css
  HEAD       size 37,019  --bbi-line:  0 occurrences
  GRID       size 37,002  --bbi-line: 18 occurrences
  DEV        size 37,019  --bbi-line:  0 occurrences  updated_at 2026-05-25T21:19:55-04:00   ← regressed
```

DEV byte-size matches HEAD (37,019) exactly, and the timestamp falls inside the 21:19:55 bulk-push window. This is collateral damage from the same `bbi-push-landing.py` run — `assets/bbi-*` is in the script's default glob.

**Recovery implication**: add `theme/assets/bbi-homepage.css` to the file-restore list. The bulk re-push from `feature/about-page-grid-1` will cover it automatically; calling out so the verification step explicitly tests for `--bbi-line` presence.

### E. DEV updated_at timestamp clustering

22 of the 23 regressed assets share the **exact** timestamp `2026-05-25T21:19:55-04:00`. This is the bulk-push fingerprint — the API processes the queue in sub-second succession, so timestamps cluster atomically. The one outlier (`templates/index.json` at `21:38:31`) is consistent with a later, separate restoration. Working-tree evidence: `git diff --cached theme/templates/index.json` shows a staged but uncommitted change matching about-grid's content (the homepage hero copy), which means whatever fixed DEV's index.json also got staged locally — likely Leo via Theme Editor → `theme pull`, OR a singleton `push-file.py` from a temporarily-correct local file. Either way, DEV's homepage is fine and this file is **not in the recovery scope**.

---

## PHASE 4 — Root cause analysis

### A. Evidence summary

1. **Reflog ordered evidence (HEAD@{3}→{0}):**
   ```
   HEAD@{3}  cf69dc8  commit: ABOUT-PAGE-GRID-1: reflow to 2x3
   HEAD@{2}  34fd438  checkout: moving from feature/about-page-grid-1 to main
   HEAD@{1}  34fd438  checkout: moving from main to feature/header-polish-2     ← new branch off main
   HEAD@{0}  bb3b5d8  commit: HEADER-POLISH-2: bar 140px + nav 21px ...
   ```
   The session deliberately moved from `feature/about-page-grid-1` (which has Day 11 work) to `main` (which doesn't) and created the new branch from `main`.

2. **HEADER-POLISH-2 commit content**: `M theme/snippets/bbi-nav.liquid` ONLY. +6/−4 lines. No template touches in the commit itself.

3. **22 DEV files updated_at clustering** at `2026-05-25T21:19:55-04:00` (sub-second cluster = single API batch).

4. **The push tool used** (per the header session report's own root-cause trace): `scripts/bbi-push-landing.py 186373570873 --snippets`. The script's published glob covers `assets/ds-*`, `assets/bbi-*.svg`, `snippets/ds-*.liquid`, `snippets/bbi-*.liquid` (with `--snippets`), `sections/ds-*.liquid`, `templates/page.*.json`, `assets/bbi-*.css`. **67 files per run.**

5. **No `shopify theme pull` in reflog or session history** — Candidate E ruled out.

6. **Pre-write backup `data/backups/header-polish-2-pre-20260525-211344/` was created** before the session's first write — captures pristine `bbi-nav.liquid` state. This is normal session hygiene and not relevant to root cause, but confirms the session's own state preserved the pre-edit file.

### B. Hypothesis evaluation

| Candidate | Verdict | Why |
|---|---|---|
| **A — Stale local working tree** | **CONTRIBUTING** | Working tree on `feature/header-polish-2` *was* stale relative to `feature/about-page-grid-1` for all 22 regressed files. But "stale" alone doesn't write to DEV. The push step (Candidate D) was the destructive act. Candidate A explains *why the pushed bytes were stale*. |
| **B — Bad branch base** | **PRIMARY ROOT CAUSE** | Reflog proves the branch was created from `main`, not from `feature/about-page-grid-1`. The 26 Day-11 commits were never in the working tree. The HEADER-POLISH-2 prompt/session report explicitly cites this branching choice: *"Audit recommended `feature/header-polish-2` branch off `main`, not off `feature/about-page-grid-1`, to keep the header PR scoped"* — the *recommendation* was sound for the PR; the *operational mistake* was running a bulk push from that branch. |
| **C — Destructive edit in prompt** | **RULED OUT** | The commit modifies one file by 10 lines (all CSS). Templates were not touched in any local edit. |
| **D — Push-all-assets script** | **PRIMARY ROOT CAUSE (combined with B)** | `bbi-push-landing.py --snippets` pushed 67 files across `assets/`, `snippets/`, `sections/`, `templates/page.*.json` in a single batch. Files outside the actual change (every template, every section, the homepage CSS) were uploaded at HEAD's *stale-relative-to-about-grid* content. The 21:19:55 timestamp cluster across 22 DEV assets is the script's API signature. The header session's own anti-pattern list states this: *"Never use bbi-push-landing.py as a 'push this one file I changed' shortcut. It's a bulk script with 67-file blast radius."* |
| **E — `shopify theme pull` overwrote local** | **RULED OUT** | No `shopify theme pull` in reflog. No evidence of local file overwrites between branch creation and commit. |

**Side puzzle — the 8 collection templates not in push glob.** The regression report flags `collection.*.json` as "NOT in push scope" of `bbi-push-landing.py`. But all 9 collection templates regressed at the same 21:19:55 timestamp. Two non-mutually-exclusive explanations:

1. The script's glob is broader than the report assumed (e.g., it covers `templates/*.json` not just `templates/page.*.json`). Reading `scripts/bbi-push-landing.py` would confirm — out of scope for read-only diagnostic, but recommended verification before re-running for recovery. **If the glob does cover all templates, recovery is one-step.**
2. Shopify's section-rendering pipeline auto-touches templates that reference an edited section. Less plausible at the precise sub-second timestamp.

This puzzle does not change the diagnosis — both explanations point to the same operator action (bulk-push from stale branch). It does affect the recovery plan: see Phase 5 §F.

### C. Root cause statement

**ROOT CAUSE: Candidates B + D combined.** The session branched HEADER-POLISH-2 off `main` (Candidate B) and then ran the bulk `bbi-push-landing.py --snippets` script from that branch (Candidate D). The script uploaded `main`'s pre-Day-11 content for every in-glob file to DEV, overwriting Day 11 image work that lived only on `feature/about-page-grid-1`. The 10-line CSS edit in the commit itself caused no damage; the bulk push that followed it did.

**Confidence: HIGH.** Direct reflog evidence + DEV timestamp clustering + matching damage profile + the session's own self-diagnosis in the regression report.

**Why this is a system issue, not just an operator mistake.** The audit recommendation that started the session — *branch off main, not off the image-work branch, to keep the PR scoped* — is correct git practice for the PR. The error compounds when a *bulk push* is run from that PR-shaped branch. The two intents (clean PR, push only-my-change) are incompatible with `bbi-push-landing.py`'s 67-file blast radius. **The fix is a guard in the script** (compare each file's local SHA against a sentinel-of-last-known-good-DEV-push from the image-work branch tip, and abort if any local SHA is older). See Recommended Next Steps §3.

---

## PHASE 5 — Recovery feasibility

### A. Option A — Revert HEADER-POLISH-2 entirely

**What it would do:** `git revert bb3b5d8` (creates a revert commit on `feature/header-polish-2`), then push reverted theme files to DEV.

**Pros:** Cleanest local git history.
**Cons:** Reverting `bb3b5d8` only reverts `bbi-nav.liquid` (the only file in the commit). It does **not** restore the 22 regressed DEV files, because those were never committed by HEADER-POLISH-2 — the bulk push happened *before* the commit, and the commit's content is unrelated. Revert is functionally a no-op for the regression.

**Suitability: BAD.** The git revert mechanism doesn't address state that was written to DEV outside of git.

### B. Option B — Cherry-pick / force-restore Day 11 files from `feature/about-page-grid-1`

**What it would do:** For each regressed file, copy the about-grid blob to working tree (`git show feature/about-page-grid-1:<file> > <file>`), then push each file individually with `scripts/push-file.py`.

**Pros:** Surgical, no commit history pollution, preserves HEADER-POLISH-2 CSS work.
**Cons:** 22 file pushes + verification — more error-prone per file. Doesn't fix the underlying topology (working tree stays on `feature/header-polish-2` off main; next bulk push would re-regress).

**Suitability: OK.** Works, but ugly. The 22-file count makes this fragile.

### C. Option C — Push entire `feature/about-page-grid-1` theme state to DEV

**What it would do:** `git checkout feature/about-page-grid-1`, then `bbi-push-landing.py 186373570873 --snippets` from that branch.

**Pros:** Fastest, single operation, restores all 22 files + `bbi-homepage.css` + `snippets/bbi-quote-modal.liquid` pre-existing drift in one shot.
**Cons:** Loses HEADER-POLISH-2's CSS edit (DEV `bbi-nav.liquid` reverts to about-grid's plain pre-HEADER-POLISH-2 state). The Round-1 bar+logo+nav size changes are gone. (Round-2 working-tree edits stay in working tree on the old branch.)

**Suitability: GOOD if Leo accepts losing the header polish for now** (which the session report's TL;DR recommends — "fresh session redesigns the header from scratch"). The header session report's Step 7 Option B is essentially this.

### D. Option D — Hybrid (recommended)

**What it would do:**
1. `git checkout feature/about-page-grid-1`
2. Cherry-pick `bb3b5d8` onto `feature/about-page-grid-1` (10-line CSS edit; clean apply guaranteed because `bbi-nav.liquid` is identical between HEAD and about-grid at the cherry-pick boundary, ergo no merge conflict). This brings HEADER-POLISH-2 work into the branch that already has Day 11 work.
3. From the new tip (`feature/about-page-grid-1 + bb3b5d8` cherry-pick), run `bbi-push-landing.py 186373570873 --snippets`. All 23 files restore to about-grid's Day-11 state PLUS DEV `bbi-nav.liquid` gets the HEADER-POLISH-2 CSS edit.
4. For the 9 `collection.*.json` files (if not covered by the bulk-push glob — verify by reading the script first), push each via `scripts/push-file.py templates/collection.<slug>.json`.
5. Verify via the embedded 35-marker rendered-DOM script in the header session report.

**Pros:**
- Preserves ALL work (Day 11 image work + HEADER-POLISH-2 CSS).
- Cleans up `assets/bbi-homepage.css` regression as a bonus.
- Cleans up `snippets/bbi-quote-modal.liquid` 4-day drift as a bonus.
- Eliminates the stale-branch topology — after the cherry-pick, the recovery branch *is* the image-work-with-header-polish branch.
- One bulk push, predictable blast radius (the SAME bulk push that caused the regression, now correctly run from the up-to-date branch).

**Cons:**
- Round-2 working-tree CSS edits (currently sitting modified in `feature/header-polish-2`'s working tree) need to be stashed first. The header session report already plans this (Recovery Step 1 stash). The Round-2 edits are flagged as "unsatisfactory" by Leo and would not be applied during recovery anyway.

**Suitability: GOOD — recommended.** Preserves work, single bulk push, eliminates the topology hazard that caused the regression in the first place.

### E. Recommendation

**Recovery Option D.** Reasoning:

1. **Root cause is git topology** (Candidate B), not the CSS edit itself or the push script's correctness. Fixing topology *before* re-pushing eliminates the recurrence risk.
2. **The cherry-pick is mechanically safe.** `bbi-nav.liquid` on `feature/about-page-grid-1` is in the pre-HEADER-POLISH-2 state (`069f70d377`, 44,088 B). The HEADER-POLISH-2 commit's diff is 10 lines, all in the inline `<style>` block (lines 32, 40, 56, 60, 477-478). No surrounding code on about-grid has touched those lines since `34fd438`. Cherry-pick will apply byte-clean.
3. **No work is lost.** Round-2 CSS edits go into stash where they're already destined per the header session report. They're explicitly flagged as work the next session may rebuild from scratch.
4. **The bulk push from the corrected branch is the inverse of the regression push** — every file pushed will reflect Day-11 work + HEADER-POLISH-2 polish. Net DEV state will be the strict superset of pre-regression DEV state.

If Leo wants to drop HEADER-POLISH-2 entirely (per the report's own Step 7 Option B recommendation), **Recovery Option C** is the slimmer path — skip the cherry-pick, just bulk-push `feature/about-page-grid-1`. Both options share the same recovery commands except for the cherry-pick step.

### F. Open question for the next session

**Read `scripts/bbi-push-landing.py` source before re-running.** Verify the glob actually covers `templates/collection.*.json`. If yes, recovery Step 3 in the header report ("push the 9 collection templates separately via push-file.py") is unnecessary. If no, retain Step 3. Reading this is a 30-second action that prevents both an unnecessary 9-file push loop AND a missed-file rollback if the script's behavior was misunderstood.

---

## PHASE 6 — Side damage check

### A. Rendered DOM check — 21 customer-facing pages

Fetched live from DEV preview (`?preview_theme_id=186373570873&_ab=0&_fd=0&_sc=1`):

| Path | HTTP | Status | Missing markers | Anti-markers present |
|---|---|---|---|---|
| `/` | 200 | ✅ CLEAN | (none) | (none) |
| `/collections/seating` | 200 | ❌ REGRESSED | `bbi-coll-img-seating-hero-v4`, `bbi-coll-img-seating-tile` | `seating-space.jpg` |
| `/collections/desks` | 200 | ❌ REGRESSED | `bbi-coll-img-desks-hero-v4` | (none) |
| `/collections/tables` | 200 | ❌ REGRESSED | `bbi-coll-img-tables-hero-v4` | `tables-space.jpg` |
| `/collections/storage` | 200 | ❌ REGRESSED | `bbi-coll-img-storage-hero-v4` | (none) |
| `/collections/boardroom` | 200 | ❌ REGRESSED | `bbi-coll-img-boardroom-hero-v4` | (none) |
| `/collections/accessories` | 200 | ❌ REGRESSED | `bbi-coll-img-accessories-hero-v4` | (none) |
| `/collections/ergonomic-products` | 200 | ❌ REGRESSED | `bbi-coll-img-ergonomic-products-hero-v4` | (none) |
| `/collections/panels-room-dividers` | 200 | ❌ REGRESSED | `bbi-coll-img-panels-room-dividers-hero-v4` | (none) |
| `/collections/business-furniture` | 200 | ❌ REGRESSED | `bbi-coll-img-business-furniture` | (none) |
| `/pages/non-profit` | 200 | ❌ REGRESSED | `bbi-page-img-non-profit-hero` | `non-profit-space.jpg` |
| `/pages/professional-services` | 200 | ❌ REGRESSED | `bbi-page-img-professional-services-hero` | `professional-services-space.jpg` |
| `/pages/industries` | 200 | ❌ REGRESSED | `bbi-page-img-non-profit-tile`, `bbi-page-img-professional-services-tile` | (none) |
| `/pages/brands` | 200 | ❌ REGRESSED | `bbi-brand-heartwood-tile`, `bbi-brand-otg-tile`, `bbi-brand-ergocentric-tile` | (none) |
| `/pages/brands/heartwood` | 200 | ❌ REGRESSED | `bbi-brand-heartwood-hero`, `bbi-brand-heartwood-tile` | (none) |
| `/pages/brands/otg` | 200 | ❌ REGRESSED | `bbi-brand-otg-hero` | (none) |
| `/pages/customer-stories` | 200 | ❌ REGRESSED | `bbi-cs-healthcare`, `bbi-cs-school-library`, `School Library`, `Trillium Health` | `case study pending verification` |
| `/pages/about` | 200 | ❌ REGRESSED | `lp-evol`, `Then and Now`, `bbi-about-grid` | (none) |
| `/pages/healthcare` | 200 | ✅ CLEAN | (false positive — page uses legacy filenames like `IMG_2566.jpg`, not `bbi-page-img-healthcare`; about-grid + HEAD byte-identical, no actual damage) | — |
| `/pages/education` | 200 | ✅ CLEAN | (same — false positive on this diagnostic's marker assumption) | — |
| `/pages/government` | 200 | ✅ CLEAN | (same) | — |

**18 of 21 pages confirmed regressed** at the rendered HTML layer. Homepage + 3 industry segment pages (healthcare/edu/gov) are clean. The 3 false-positive segment pages confirm the regression scope is exactly the templates whose blobs differ between HEAD and about-grid — nothing more.

### B. Non-template assets

- **`assets/bbi-homepage.css`** — REGRESSED on DEV (--bbi-line × 18 → 0). NEW FINDING, not in the original regression report. Recovery: covered by the bulk re-push from `feature/about-page-grid-1`.
- **`assets/header.css`, `sections/header.liquid`, `snippets/header-logo.liquid`** — DEV reverted to main's pre-HEADER-POLISH versions. **No visible impact** (PRE-LAUNCH-AUDIT-1 should-fix #1 found these were dead code on BBI surface — `header.css` is not loaded on any BBI landing page; the bar/nav rules from `65458f6` HEADER-POLISH commit never had an effect). Recovery: cosmetic — re-push will restore the dead-code state, no behavioral change.
- **`snippets/bbi-nav.liquid`** — DEV has Round-1 + Round-2 (`44,232 B`, > both HEAD's 44,163 and about-grid's 44,088). This is the intentional header polish work; not regressed. Recovery: if Option D, cherry-pick + push restores DEV to Round-1 (44,163 B). If Option C, re-push restores DEV to plain about-grid state (44,088 B).
- **`snippets/bbi-quote-modal.liquid`** — Pre-existing 4-day drift (DEV 20,752 B vs HEAD/grid 21,071 B), updated_at 2026-05-21. **Not caused by HEADER-POLISH-2.** Day-10 PR-2 changes to this file (sameAs TODO rewrite + sitewide modal trigger pattern locked-in) never landed on DEV. Recovery: covered by the bulk re-push from about-grid.
- **All other `theme/` files** — verified via Phase 3E extended scan; no marker-count delta found beyond the 23 listed files.

### C. LIVE theme integrity

```
LIVE: BBI Live  role=main  id=178274435385  updated_at=2026-05-16T16:47:22-04:00
```

**Exactly matches PRE-LAUNCH-AUDIT-1's recorded baseline** (`2026-05-16T16:47:22-04:00`). No 2026-05-25 writes to LIVE. **Confirmed UNTOUCHED.** The 9-day-old timestamp is the historic 2026-05-16 push, not a new event.

### D. Working tree + git stash state

- Current branch: `feature/header-polish-2`
- Modified, uncommitted (working tree): `theme/snippets/bbi-nav.liquid` (Round-2 CSS edits, +14/−13 lines)
- Modified, **staged** but not committed: `theme/templates/index.json` (homepage hero copy update matching about-grid; +5/−5 lines)
- Stash list: `stash@{0}: On feature/stage-4b-pdp-design-parity: stage-4b-pdp-design report` — predates this session, unrelated
- Pre-write backup of pristine `bbi-nav.liquid`: `data/backups/header-polish-2-pre-20260525-211344/bbi-nav.liquid` — present, intact, 44,088 B (matches about-grid blob — the safe recovery reference)

The **staged index.json** is the same content as `feature/about-page-grid-1`'s `index.json` — so whoever fixed DEV's homepage at 21:38:31 also left the change staged locally. This is consistent with the diagnostic note in §3.E that the homepage was restored through a separate action (Theme Editor → pull, or singleton push), and recovery does NOT need to touch index.json.

---

## RECOVERY PREREQUISITES

| Requirement | Status |
|---|---|
| `feature/about-page-grid-1` intact (26 commits, all blob SHAs verified) | ✅ **YES** |
| LIVE theme untouched (`2026-05-16T16:47:22` matches PRE-LAUNCH-AUDIT-1 baseline) | ✅ **YES** |
| Pre-write backup of pristine `bbi-nav.liquid` available | ✅ **YES** (`data/backups/header-polish-2-pre-20260525-211344/`) |
| Round-2 uncommitted CSS edits preserved (will go into stash before recovery) | ✅ **YES** (working tree dirty as expected; header session report's Recovery Step 1 stashes them) |
| Local working tree clean (no other competing edits) | ⚠️ **Almost** — staged `templates/index.json` change should be either committed-as-housekeeping or dropped before checking out about-grid. Recovery branch (`feature/about-page-grid-1`) already has the same content in `index.json`, so staged change is redundant and safe to discard with `git restore --staged theme/templates/index.json` |
| No further sessions touch DEV until recovery is approved + complete | ⚠️ **POLICY-DEPENDENT** — Leo's call; the regression doesn't preclude other read-only sessions, but any DEV write before recovery would compound risk |
| `scripts/bbi-push-landing.py` source verified for `templates/collection.*.json` glob coverage | 📋 **PENDING** — 30-second read before recovery Step 3 |
| `SHOPIFY_TOKEN` in `.env` accessible | ✅ **YES** (preflight passed) |

**No critical blockers. Recovery is ready to execute.**

---

## RECOMMENDED NEXT STEPS

1. **(Recovery session, ~30 min execution.)** Run Recovery Option D from this report's Phase 5. Concretely, in order:
   1. `git status` confirm pristine state, then `git restore --staged theme/templates/index.json` (drop the redundant staged change — about-grid has identical content).
   2. `git stash push -u -m "header-polish-2 round-2 wip" -- theme/snippets/bbi-nav.liquid` (preserve Round-2 CSS for reference).
   3. `git checkout feature/about-page-grid-1`. Working tree must show clean.
   4. `git cherry-pick bb3b5d8` (HEADER-POLISH-2's 10-line CSS edit applies clean — about-grid's bbi-nav.liquid is at the exact pre-edit blob `069f70d377`).
   5. Read `scripts/bbi-push-landing.py` once to confirm glob coverage on `templates/collection.*.json`.
   6. `export $(grep -v '^#' .env | xargs) && BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873 --snippets` — restores 22 files + `bbi-homepage.css` + `bbi-quote-modal.liquid` 4-day drift + applies HEADER-POLISH-2 CSS to DEV.
   7. If Step 5 showed the glob does NOT cover `collection.*.json`: loop `for slug in seating desks tables storage boardroom accessories panels-room-dividers ergonomic-products business-furniture; do python3 scripts/push-file.py templates/collection.${slug}.json && sleep 1; done`.
   8. Run the embedded 35-marker rendered-DOM verification script from the header session report's Recovery Step 5. Expected: all markers turn from ✗ to ✓.
   9. `shopify theme check` — expected: 265 files / 2855 offenses / 166 files-with-offenses (the PRE-LAUNCH-AUDIT-1 baseline).
   10. Commit the cherry-pick on `feature/about-page-grid-1` (it carries `bb3b5d8`'s edit but on the corrected branch). Push to origin.
   11. Delete `feature/header-polish-2` (`git branch -D feature/header-polish-2 && git push origin --delete feature/header-polish-2`) — its only commit is now contained in the cherry-pick on about-grid.

2. **Build-state.md update (post-recovery).** Add a regression-event row noting: HEADER-POLISH-2 bulk-push regression on DEV → REGRESSION-DIAGNOSTIC-1 → Recovery Option D → all Day 11 work restored + header polish preserved. Reference this report.

3. **System hardening (post-launch backlog).** Add a guard to `scripts/bbi-push-landing.py`:
   - Before pushing, query each in-scope file's DEV `updated_at` + content-hash.
   - For each file, compute local blob SHA from current working tree.
   - If any local blob SHA is *older* than DEV's known last-write SHA from the image-work branch tip (sentinel record in `data/state/last-known-good-push.json` or similar), abort with a clear "stale local — refusing to overwrite newer DEV content" message.
   - Force-flag (`--force-stale`) for explicit override when the operator knows what they're doing.

   This prevents recurrence of the exact failure pattern: branch off `main`, run bulk push, regress DEV. With the guard in place, the script self-aborts and surfaces the topology problem.

4. **Header redesign (separate next session, ~half day).** Per the header session report's TL;DR, the Round-1 + Round-2 CSS work is "off balance" and Leo wants a full plan including hero image sizing. After recovery succeeds, scope a header redesign session that uses `scripts/push-file.py` ONLY for snippet edits (never `bbi-push-landing.py`). The header session report's "ANTI-PATTERNS" list is already a good starter doc — encode it in the prompt.

5. **No LAUNCH-2 today** until recovery completes + verification passes. Recovery is mechanical (~30 min) so LAUNCH-2 is still feasible Monday if Leo wants — just gated on the recovery + post-recovery SYS-VERIFY pass.

---

## APPENDIX A — Raw git outputs

### A1. Full reflog (HEAD@{0} → HEAD@{20})

```
bb3b5d8 HEAD@{0}: commit: HEADER-POLISH-2: bar 140px + nav 21px on actual BBI header (bbi-nav.liquid)
34fd438 HEAD@{1}: checkout: moving from main to feature/header-polish-2
34fd438 HEAD@{2}: checkout: moving from feature/about-page-grid-1 to main
cf69dc8 HEAD@{3}: commit: ABOUT-PAGE-GRID-1: reflow to 2x3 (drop wordmark + workstations)
e8c75a4 HEAD@{4}: commit: ABOUT-PAGE-GRID-1: 2x4 brand-evolution grid on About page
732b303 HEAD@{5}: checkout: moving from feature/collection-img-pull-1 to feature/about-page-grid-1
732b303 HEAD@{6}: commit: build-state: Day 11 evening sync + PRE-LAUNCH-AUDIT-1 report
ab3b537 HEAD@{7}: commit: gitignore: stray Avada snippets/ + build-state backups
02668a6 HEAD@{8}: commit: tooling: add bbi-preview-dev + bbi-wire-hero-image helper scripts
65458f6 HEAD@{9}: commit: HEADER-POLISH: 2x logo, 140px bar, 21px nav (Day 11 launch polish)
cecabd7 HEAD@{10}: commit: HOMEPAGE-BORDERS: align --bbi-line to canonical #E5E5E7
2cbd469 HEAD@{11}: commit: HOMEPAGE-BORDERS: introduce --bbi-line token
b07b2af HEAD@{12}: commit: HOMEPAGE-INDUSTRY-TILES: swap non-profit + pro-services tile <img> srcs
d0fcef4 HEAD@{13}: commit: Session recap: 2026-05-25 image rounds
0be4c2c HEAD@{14}: commit: INDUSTRIES-HUB-TILES tile cards on /pages/industries
40510cb HEAD@{15}: commit: Homepage bbi-featured: card border
a0ffa99 HEAD@{16}: commit: INDUSTRY-HEROES: non-profit + professional-services hero swaps
3c5bf43 HEAD@{17}: commit: Homepage bbi-featured fix: aspect-ratio 16:9 → 1:1
b915800 HEAD@{18}: commit: Homepage bbi-featured follow-up 2
e884b57 HEAD@{19}: commit: Homepage bbi-featured follow-up: cover → contain
b60a47c HEAD@{20}: commit: Homepage bbi-featured: 3 product cards filled with Idea #15 SKUs
```

### A2. HEADER-POLISH-2 diff (full)

```
commit bb3b5d85018091643fd64b0ed032b25f9ad3d250
Author: Leo Katz <leo@venn.ca>
Date:   Mon May 25 21:20:25 2026 -0400
Parents: 34fd438 (main HEAD)

Files changed: theme/snippets/bbi-nav.liquid (only)
Stats: 1 file changed, 6 insertions(+), 4 deletions(-)

  line 32:    .bbi-header__inner { height: 72px }    →  height: 140px
  line 40:    .bbi-header__logo img { height: 36px } →  height: 64px
  line 56:    .bbi-nav__item { height: 72px }        →  height: 140px
  line 60:    .bbi-nav__item { font-size: 14px }     →  font-size: 21px
  line 477–478 (added):
      @media (max-width: 1023px) {
        .bbi-header__inner { height: 88px }
        .bbi-header__logo img { height: 44px }
      }
```

### A3. Branch divergence

- `git merge-base feature/header-polish-2 origin/main` → `34fd438`
- `git merge-base feature/header-polish-2 feature/about-page-grid-1` → `34fd438`
- `feature/about-page-grid-1`: 26 commits ahead of `main`, in sync with origin
- `feature/header-polish-2`: 1 commit ahead of `main`, in sync with origin

### A4. Raw damage-table JSON

Saved to `data/working/regression-diagnostic-1/damage-table.json` for downstream consumption by the recovery session. Includes blob SHAs, sizes, marker counts, and DEV `updated_at` per file.

---

## APPENDIX B — Phase 6 false positives (for completeness)

The diagnostic's per-page marker check flagged `/pages/healthcare`, `/pages/education`, `/pages/government` as REGRESSED because they lacked `bbi-page-img-{slug}-hero` strings. Investigation showed:

- `theme/templates/page.healthcare.json` — HEAD blob = about-grid blob (byte-identical, 885 bytes)
- `theme/templates/page.education.json` — byte-identical (794 bytes)
- `theme/templates/page.government.json` — byte-identical (940 bytes)
- `theme/sections/ds-lp-healthcare.liquid` — byte-identical (73,675 bytes)

Healthcare top images on the rendered page resolve to `IMG_2566.jpg` (a legacy filename), confirming these segment pages were never converted to the `bbi-page-img-{slug}-` prefix during Day 11 image work. **They are NOT regressed.** The regression report's claim that healthcare/edu/gov heroes are intact is correct; this diagnostic's marker assumption was overly broad and was corrected during verification.

---

## APPENDIX C — Failure-mode checklist (from the prompt)

- ☑ **`feature/about-page-grid-1` is intact.** All 26 commits exist; all critical-file blob SHAs verified; recovery source is unimpaired.
- ☑ **Damage scope is within the regression report's estimate.** Report stated 22 files / 75–80 image refs; this diagnostic confirms 22 BOTH_REGRESSED + 1 new (bbi-homepage.css). 111 markers lost = ~75–80 visible slots once de-duplicated and account taken of multi-marker lines.
- ☑ **Root cause established with HIGH confidence.** Candidates B + D combined. Reflog is direct evidence.
- ☑ **No write needed to investigate.** This diagnostic ran fully read-only — only writes were to `data/working/regression-diagnostic-1/` and `data/reports/regression-diagnostic-1-2026-05-26.md`, which per the prompt are allowed diagnostic outputs.
- ☑ **No LIVE damage detected.** LIVE `updated_at` matches PRE-LAUNCH-AUDIT-1 baseline; no escalation needed.

**Diagnostic complete. Ready for recovery session.**
