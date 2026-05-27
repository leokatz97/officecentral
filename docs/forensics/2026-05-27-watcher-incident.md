# Watcher Auto-Push Incident — 2026-05-27

**Status:** Items 1, 2, and 3 approved; Item 4 in progress
**Branch:** `feature/watcher-forensics-2026-05-27`
**Discovery:** 2026-05-27 ~14:25 EDT during SCHEMA-CRIT-1 Fix 1 approval-gate check
**Resolution:** Watcher killed ~14:30 EDT. Forensic snapshot captured.
**Forensic snapshot:** [`data/forensics/2026-05-27-watcher-discovery/`](../../data/forensics/2026-05-27-watcher-discovery/)

---

## 1. One-paragraph summary

Between 2026-05-11 and 2026-05-27 14:30 EDT, a long-running `shopify theme dev` watcher (PID 28041) was bound to the LIVE production theme (`186373570873`, role=main). Every `Edit` against `theme/**` for 16 days was silently auto-`PUT` to LIVE within ~1 second of the local file save, bypassing the approval gates that the post-launch preflight discipline (`BBI-Session-Kickoff/01-safety-preflight.md`) is built to enforce. The breach was discovered when the SCHEMA-CRIT-1 Fix 1 pre-`PUT` re-check observed LIVE `updated_at` had already drifted forward to the post-fix state before Claude's intentional `PUT` ran. The watcher was killed within ~5 minutes of discovery; a forensic LIVE snapshot was taken; no further unintended writes are possible from that process.

**Item 2 retroactive reconciliation (§4) surfaced direct evidence that the watcher was active during today's session, not only as a 16-day hypothesis:** a previously-unrecorded LIVE event between 10:13:21 and 13:15:38 EDT — required by today's existing byte-equivalence forensic proof — is most parsimoniously a watcher-pushed `LOCAL = v4` revert that reset LIVE after the legitimate 10:13:21 re-fix PUT. This event was undetected at the time and is the strongest single-day evidence of the watcher's hands-on impact on LIVE.

## 2. Timeline (EDT)

| Time | Event |
|---|---|
| 2026-05-11 12:47 | Watcher process started. `node /opt/homebrew/bin/shopify theme dev --store=office-central-online --theme=186373570873 --port=9292`. Earliest LIVE asset `updated_at` post-watcher: `assets/accordion-box.css` at 12:47:37 (per snapshot manifest). |
| 2026-05-11 → 2026-05-26 | Pre-launch period. Theme 186373570873 was role=unpublished ("BBI Landing Dev"). Watcher writes still landed but on the not-yet-promoted theme. Risk surface was lower. |
| 2026-05-26 20:08:47 | LAUNCH-1 theme-role inversion: 186373570873 promoted to role=main. Watcher now bound to LIVE production. Approval-gate discipline (`01-safety-preflight.md`) became load-bearing. |
| 2026-05-26 → 2026-05-27 14:24 | All `theme/**` `Edit`s during this window were silently auto-PUT to LIVE without approval. Today's edits are reconciled in §4 of this report. |
| 2026-05-27 14:22-14:23 | Local `Edit` on `theme/snippets/bbi-product-jsonld.liquid` (SCHEMA-CRIT-1 Fix 1: BreadcrumbList position-2 URL). |
| 2026-05-27 14:24:13 | LIVE asset `snippets/bbi-product-jsonld.liquid` `updated_at` bumped to byte-identical post-Edit state. **This is the auto-push event that gave the watcher away.** |
| 2026-05-27 ~14:25 | Claude's pre-PUT re-check caught LIVE `updated_at` drift. Approval-gated PUT halted; Leo issued approval phrase `fire schema-crit-1 fix-1` but the operation was already moot — file content already on LIVE via watcher. |
| 2026-05-27 ~14:30 | `ps aux \| grep shopify` revealed PID 28041 = the watcher. Watcher killed. Confirmed dead. No other shopify processes running. |
| 2026-05-27 ~14:30+ | Forensic LIVE snapshot taken (`data/forensics/2026-05-27-watcher-discovery/`, 359 assets, per-asset sha256 manifest). |
| 2026-05-27 today | Forensic byte-diff and operational recovery (this PR). |

## 3. Drift findings — LIVE forensic snapshot vs git HEAD

**Methodology:** byte-compared every file in the 359-asset forensic snapshot against `git show HEAD:theme/<path>` on branch `feature/schema-crit-1-2026-05-27` (the source-of-truth branch for the incident state; PR #28 open). Raw diff data: [`data/forensics/2026-05-27-watcher-discovery/diff-output/`](../../data/forensics/2026-05-27-watcher-discovery/diff-output/).

### Headline numbers

| Result | Count |
|---|---|
| Identical (snap == git HEAD byte-for-byte) | 310 |
| Differs (snap != git HEAD bytes) | 47 |
| In snap, absent in git | 2 |
| In git (theme/), absent in snap (i.e. not on LIVE) | 5 |
| Snapshot total | 359 |

### Categorization

**(a) JSON re-escape artifact — logically identical, no action.** 46 files.

All 46 `.json` files that show byte differences parse to **deep-equal** JSON objects when compared via `json.dumps(obj, sort_keys=True)`. The byte difference is whitespace / key ordering / Unicode escape form variance introduced by Shopify's wire-format vs the locally-saved form. Documented behaviour, expected, no remediation needed.

Files: every `templates/*.json` except `page.design-services.json` and `page.quote.json` (still category-a — both deep-equal — listed here for completeness). Full list in [`json-classification.json`](../../data/forensics/2026-05-27-watcher-discovery/diff-output/json-classification.json).

**(b) Known intended LIVE-only state — no action.** 1 file diff + 7 asymmetric paths.

- `config/settings_data.json` (in snap, absent in git) — Theme Editor merchant customizations. Excluded by `.gitignore` line `theme/config/settings_data.json`. Per Shopify best practice and project CLAUDE.md.
- `config/settings_schema.json` (in snap, absent in git) — Starlite theme settings schema (`theme_name: "Starlite", theme_version: "3.6.1"`). Not in `.gitignore`. Pre-existing gap from the initial commit (19b1758) — this file was never imported. Not watcher-caused. **Out of scope for WATCHER-FORENSICS.** Belongs to STARLITE-LEGACY-SNIPPETS-AUDIT scope; do not commit (Starlite legacy artifact — committing plants confusion).
- `templates/customers/{account, activate_account, addresses, login, order}.json` (5 files, in git, absent on LIVE) — orphan scaffolding from the initial commit; LIVE uses only `register.json` and `reset_password.json` (both present and identical-modulo-(a)). Not watcher-caused. Out of scope for this incident PR.

**(c) Unexplained drift requiring investigation.** **0 files.**

The single Liquid byte-difference (`snippets/style-variables.liquid`) is **not** category (c). Resolution:
- LIVE: 397 lines, contains the original Avada dark-mode CSS variable block (6 occurrences of `[color-mode="dark"]`).
- git HEAD: 289 lines, dark-mode block stripped.
- The strip happened in commit `1277566` ("Track D complete: DS-0 → DS-4 design system", merged 2026-05-05) — **before** the watcher started (2026-05-11). Track D refactored this snippet in git but the file was never included in a deploy push, so LIVE retained the original Avada version. The watcher only triggers on local saves; since no edit landed on this file post-watcher, the watcher had no role in this divergence.
- **Category:** (b) — pre-existing git/LIVE divergence, watcher-unrelated. **Out of scope for WATCHER-FORENSICS.** Tracked as Tier 2B backlog item STYLE-VARIABLES-DEPLOY-RECONCILIATION ("why was Track D never deployed?") — do NOT sync either direction until that question is answered, since a 22-day undeployed state likely reflects an intentional pause rather than oversight.

### Drift table

| File | Bytes (snap / git) | Kind | Category | Notes |
|---|---|---|---|---|
| `snippets/style-variables.liquid` | 20682 / 17097 | liquid | **(b)** | Pre-watcher git/LIVE divergence. Track D commit (2026-05-05) stripped dark-mode CSS in git only; LIVE retains original Avada. Watcher had no role. |
| 46 × `templates/*.json` and `templates/customers/{register,reset_password}.json` | varies | json | **(a)** | JSON re-escape; logically deep-equal. |
| `config/settings_data.json` | 69300 / — | json | **(b)** | Theme Editor merchant customizations; `.gitignore`d. |
| `config/settings_schema.json` | 67458 / — | json | **(b)** | Starlite schema; never imported to git (pre-watcher gap). |
| `templates/customers/{account,activate_account,addresses,login,order}.json` | — / 5 files | json | **(b)** | Git-only orphans; LIVE uses different customer template set. |

### Headline conclusion

**Finding: no current divergent state on LIVE between the forensic snapshot and git HEAD that the watcher uniquely caused.** Every byte-difference is fully explained by:
- JSON wire-format re-escape (a), or
- Pre-existing intentional/orphan git/LIVE asymmetries (b) that pre-date the watcher and are unrelated to it.

**This is not a finding that the watcher was harmless.** The watcher was active and dangerous for 16 days against an unpublished theme and ~18 hours against LIVE-production after LAUNCH-1 (2026-05-26 20:08 EDT). It is known to have pushed at least one approval-gated edit (SCHEMA-CRIT-1 Fix 1, `bbi-product-jsonld.liquid`, 2026-05-27 14:24:13) **before** the approval phrase was issued, bypassing the post-launch preflight discipline entirely. Each of Claude's `Edit`s during the LIVE window was an un-gated production write.

The reason this audit finds zero category-(c) divergence is that the watcher's mechanism — auto-push local saves *to* LIVE — happens to leave LIVE and the subsequent committed git state in agreement on any file Claude edited and then committed. Convergence ≠ safety. It only means: by the time we took the snapshot, LIVE matched what git eventually agreed should be there. It does not mean the un-gated pushes during the 16-day window were authorised, reviewed, or correct at the moment they landed.

Implications for future readers:
- **Do not conclude that watchers are safe.** Watchers against a role=main theme are unconditionally unsafe and are now blocked at preflight (Item 3).
- **Convergence finding is operational, not absolving.** It means the current LIVE content can be treated as ground truth for *now* — not that the discipline can be relaxed in future sessions.
- The breach class was **governance / approval-gate**, with one known specific instance (Fix 1) where the approval phrase was issued *after* the write had already landed. Other un-gated writes during the 16-day window are likely but undetectable post-hoc, since the watcher and a legitimate post-edit push produce indistinguishable LIVE states.

---

## 4. Retroactive reconciliation of today's drift events

Today's build-state framed **three** substantive `templates/index.json` `bbi-shop` events as drift attributable to Theme-Editor cache flushes. With the watcher now known, that count is corrected to **two genuine drift events** (the third, 10:13:21, was Claude's intended re-fix PUT and never belonged in the drift bucket — see Event 2 below), **plus one previously-undetected event** surfaced by this reconciliation. Each event is re-examined here. The reconciliation framework:

- **(i) Theme-Editor cache flush** — a save in Shopify Admin's Theme Editor flushed a stale-cached section state to LIVE.
- **(ii) Watcher auto-push of a local edit** — a filesystem event on `theme/templates/index.json` triggered the `shopify theme dev` watcher to PUT LOCAL content to LIVE.
- **(iii) Genuinely unexplained.**
- **(iv) Insufficient evidence to determine** — the outcome is consistent with multiple causes and no forensic signal disambiguates them.

### Key forensic constraint

The snapshot manifest's `server_updated_at` field captures only the **most-recent** bump per asset (it's the live value at snapshot time, ~14:30 EDT). `templates/index.json` was bumped at least 4 times today (~09:54, 09:57:27, 10:13:21, 13:15:38), but the manifest now only retains `13:15:38`. The earlier bumps are forensically erased — we have no per-bump byte content for them. This caps how strongly Events 1 and 2 can be reconciled. The reconciliation relies on:
- LOCAL state inferred from git commits (`cfe918f` at 10:20:15 captured LOCAL = v4; `c9ec186` at 13:19:34 captured LOCAL = v5).
- Direction analysis (LIVE → LOCAL is consistent with watcher; LIVE → not-LOCAL excludes watcher).
- The contemporaneous build-state attributions from earlier today.

### LOCAL `templates/index.json` chronology

| Time | LOCAL state (`bbi-shop` seating tile) | Source |
|---|---|---|
| Pre-morning | v4 | Pre-IMG-1 baseline |
| Morning IMG-1 PUT (~09:54:03) | **v4** unchanged | Push script (`bbi-push-landing.py`) substitutes in memory and PUTs v5 to LIVE without rewriting LOCAL. Confirmed: `cfe918f` at 10:20:15 has LOCAL = v4. |
| Morning re-fix PUT (10:13:21) | **v4** unchanged | Same script mechanism — v4→v5 substitution + `?width=1920` added in memory; LOCAL not rewritten. |
| Afternoon manual sync | **v5** | `c9ec186` at 13:19:34 — Claude explicitly edited LOCAL templates/index.json to v5 to match LIVE-corrected state. |

This LOCAL chronology — v4 throughout the morning, v5 in the afternoon — is **load-bearing** for the reconciliation.

### Event-by-event reconciliation

| # | Time | LIVE direction | LOCAL state at the time | Original attribution | Revised attribution | Reasoning |
|---|---|---|---|---|---|---|
| 1 | 09:57:27 | v5 → v4 | **v4** | (i) Theme-Editor stale-cache (Leo confirmed contemporaneously being in Admin) | **(iv) insufficient evidence — both (i) and (ii) explain the outcome; (ii) is mechanistically more parsimonious** | LIVE moved *toward* LOCAL (LOCAL = v4, LIVE became v4). Either mechanism produces this: Theme-Editor save with stale v4 cache, OR any filesystem event on `templates/index.json` (no-op `touch`, transient script write) triggers watcher to push LOCAL = v4. Leo's contemporary attribution stands as **possible but not confirmed**; without filesystem-mtime logs or Shopify Admin audit logs (no Plus tier), cannot definitively rule out the watcher. Mechanistically, the watcher is a more parsimonious explanation given that the same v5→v4 revert pattern recurs (see "Missing event" below). |
| 2 | 10:13:21 | v4 → v5 (+ `?width=1920`) | **v4** | Claude's explicit re-fix PUT via `bbi-push-landing.py` | **Not a drift event — explicit Claude script PUT.** Re-classify out of "drift events" bucket entirely. | This bump was an intended, in-session API write. The script substituted v4→v5 and added `?width=1920` in memory and PUT to LIVE. The watcher *could not* have produced this state — LOCAL was v4 throughout, so any watcher push during this minute would have pushed v4, not v5+width. The script PUT is the sole proximate cause. (The prompt listed this event in the "3 drift events to reconcile" set, but my finding is that it never belonged there — it was a clean Claude write.) |
| 3 | 13:15:38 | v4 → v5 | **v4** | (i) Theme-Editor stale-cache (Steve/Leo confirmed in Admin 12:38–13:15) | **(i) Theme-Editor cache flush — CONFIRMED; (ii) watcher excluded by direction** | LIVE moved *away* from LOCAL (LOCAL = v4, LIVE became v5). The watcher pushes LOCAL → LIVE; with LOCAL = v4, a watcher push at any moment would have produced LIVE = v4, not v5. Therefore the only mechanism that can produce LIVE = v5 is an external (non-watcher) write: Theme-Editor save with v5-cached state, or a direct Admin API call. Steve/Leo's confirmed Admin session 12:38–13:15 is the contemporaneous attribution and stands. |

### Missing event — gap between 10:13:21 and 13:15:38

The byte-equivalence proof recorded in today's afternoon build-state notes (sha256 `37d77715b37b367a` ≡ `37d77715b37b367a`) and the line "`LIVE NOW == LIVE pre-drift + v4→v5 character-level substitution`" require that **LIVE was v4 immediately before 13:15:38**. But the 10:13:21 PUT set LIVE = v5+width. Therefore **at least one unrecorded LIVE event between 10:13:21 and 13:15:38 reverted LIVE from v5 back to v4.** This event was not in the 3-event list and was not surfaced in today's build-state, but its existence is forensically required by the byte proof.

**Plausible attribution for the missing event:**
- **(ii) watcher auto-push.** Some filesystem event on `theme/templates/index.json` between ~10:13 and ~13:15 — a touch, a transient script write, even an editor open-and-save — would push LOCAL = v4 to LIVE, exactly reverting the 10:13 PUT. This is the most parsimonious mechanism given the watcher's persistent presence and the recurring v5→v4 direction.
- **(i) Theme-Editor cache flush.** A second Theme-Editor save during the late-morning/early-afternoon window. Less parsimonious — would require another stale-cache event with similar timing.

**Verdict on missing event: (ii) watcher auto-push likely, (i) possible.** Watcher is favored because the direction (LIVE → LOCAL state) is exactly the watcher's mechanical signature, and the assumption of a second Theme-Editor accident in the same day on the same field is a less economical hypothesis.

### Summary of revised attributions

| Event | Original | Revised |
|---|---|---|
| 09:57:27 v5→v4 | (i) Theme-Editor confirmed | **(iv) insufficient — favor (ii) watcher** |
| 10:13:21 v4→v5+width | (i) Theme-Editor (listed in 3-event set) | **Re-classify: explicit Claude script PUT, not a drift event** |
| 13:15:38 v4→v5 | (i) Theme-Editor confirmed | **(i) Theme-Editor — CONFIRMED, watcher excluded by direction** |
| *Missing event* (10:13:21 < t < 13:15:38) | *Not recorded* | **New: (ii) watcher auto-push likely** |

### Implications

- **One of three original "drift events" was never a drift event** — the 10:13:21 was Claude's intended script PUT.
- **One was misattributed to Theme-Editor and is more parsimoniously the watcher** — 09:57:27.
- **One was correctly attributed to Theme-Editor and the watcher is mechanically excluded** — 13:15:38.
- **At least one drift event was entirely undetected at the time** — the unrecorded v5→v4 revert between 10:13:21 and 13:15:38, which is most likely a watcher push.
- **HP-SHOP-TILES-REFACTOR — justification narrows but does not disappear.** Today's pattern of repeated drift on the `bbi-shop` `custom_liquid` field originally read as 3 Theme-Editor stale-cache recurrences and drove the HP-SHOP-TILES-REFACTOR work item into Tier 1. The reconciliation here re-attributes **2 of the 3 recurrences (Event 1 and the missing event) to the watcher as more parsimonious explanations** — both stop happening once the watcher is dead. The **third (Event 3, 13:15:38)** remains a real Theme-Editor cache-flush failure mode that the watcher cannot explain and that the refactor would mitigate. The architectural fragility is real: untyped image URLs inside `custom_liquid` raw HTML are inherently vulnerable to a Theme-Editor save with a stale cached view of the field. Net effect: refactor *urgency* drops (watcher kill stops most of today's noise), but the *architectural justification* survives. Re-scoped from Tier 1 to Tier 2B in build-state with the revised justification.


---

## 5. Recovery steps taken

1. **Watcher killed** (2026-05-27 ~14:30 EDT). `kill 28041` confirmed dead via `ps -p 28041` returning no row. No other `shopify` processes running at that time.
2. **Forensic LIVE snapshot captured** to [`data/forensics/2026-05-27-watcher-discovery/`](../../data/forensics/2026-05-27-watcher-discovery/) — 359 assets, per-asset sha256 manifest, theme metadata. README in that directory documents discovery timeline + snapshot integrity (311/359 md5-matched LIVE byte-exactly).
3. **Build-state entry** added (commit `5ab2d4f`) flagging Fix 1 as shipped under anomalous discovery conditions + WATCHER-FORENSICS-AND-PROCESS-RECOVERY queued as Tier 1 top-of-stack.
4. **Forensic byte-diff pass** (Item 1, this PR) — zero category-(c) divergence; all drift explained by JSON re-escape or pre-watcher git/LIVE asymmetries.
5. **Retroactive reconciliation** (Item 2, this PR) — 1 of 3 original "drift events" reclassified as not a drift event; 1 reclassified to insufficient-evidence (favor watcher); 1 confirmed Theme-Editor + watcher excluded by direction; 1 new previously-undetected event surfaced (likely watcher).

---

## 6. Prevention measures

1. **`scripts/preflight-watcher-check.sh`** (Item 3, this PR) — executable bash script that fails loud on any running `shopify theme` process. Strict-binary posture: any such process at preflight time → FATAL, regardless of subcommand or bound theme. Emits a final `RESULT: PASS|FAIL` line for greppable downstream automation. Five test scenarios verified (baseline pass, dev-on-main, push-on-rollback, push-no-token-unresolved-role, push-no-theme-flag).
2. **`BBI-Session-Kickoff/01-safety-preflight.md`** (Item 3, this PR) — rule 0 (HARD RULES) and STEP 0 (PREFLIGHT CHECK run sequence) added; existing role-verification preflight is now STEP 1. Watcher-incident motivation surfaced in the "Why this exists" header.
3. **Operational doc — "Watchers and auto-push" section** (Item 4, this PR) — captures the principle: never run `shopify theme dev` against a role=main theme; use a dev theme; preflight script enforces.
4. **Tier 2B backlog adds** (build-state, this PR):
    - `PREFLIGHT-AUTOMATION` — automate the preflight invocation so it can't be skipped under fatigue. Three mitigation options listed; pick one.
    - `FORENSIC-SNAPSHOT-TIME-WINDOWED` — capture time-windowed asset history, not just current-state manifest. Today's snapshot erased the morning bumps on `templates/index.json` and limited Item 2 reconciliation certainty.
    - `HP-SHOP-TILES-REFACTOR` (re-scoped down from Tier 1) — architectural fragility on `custom_liquid` raw HTML survives the watcher kill (Event 3 was genuine Theme-Editor), but urgency drops.
5. **Memory entry** already applied in Leo's persistent memory: `feedback_preflight_watcher_check.md` — "Before any approval-gated production write session on BBI/Shopify, check for running shopify theme dev watchers."

---

## 7. Lessons

**Root cause, sharpest framing:** *self-enforcement only catches what the doc explicitly enumerates.* The post-launch preflight discipline (`01-safety-preflight.md`) was paste-driven into every session and Claude self-enforced the listed rules — but the doc did not name a watcher check until this incident, so Claude never ran one for 16 days. The watcher's invisibility was not a failure of attention; it was a failure of the rule surface. Self-enforcement is upper-bounded by the rule list. Anything not on the list is, by construction, unguarded.

Three corollaries:

1. **The preflight rule list is load-bearing infrastructure.** Adding to it is a substantive change, not a clerical one. Items 3 and 4 of this PR add rule 0 + a "Watchers and auto-push" section explicitly because absence-from-doc was the failure mode.
2. **Self-enforcement is necessary but not sufficient.** Automated enforcement (PREFLIGHT-AUTOMATION, Tier 2B) is the next safety layer — a shell-rc hook, a push-script gate, or a git pre-push hook that runs the check without depending on Claude or Leo to remember it. The `RESULT: PASS|FAIL` line on the watcher check (Item 3) was designed specifically to be greppable by such wrappers.
3. **Convergence is not safety.** Item 1's finding that LIVE and git ended up byte-aligned across the 16-day window does not absolve the watcher — it only means the *content* on LIVE happens to match what git eventually agreed should be there. The breach class was governance / approval-gate, with one demonstrated specific instance (Fix 1) and at least one previously-undetected instance (the missing event between 10:13:21 and 13:15:38). Other un-gated writes during the window are likely but post-hoc undetectable since the watcher and a legitimate post-edit push produce indistinguishable LIVE states.
