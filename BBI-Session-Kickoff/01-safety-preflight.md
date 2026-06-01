# Step 1 — Safety Preflight (Post-Launch)
**Paste this as your first message in every new Claude Code session. Do not skip.**

---

> **Why this exists:**
> - **2026-05-10** — a session pushed `theme.liquid` + two snippet stubs to the live theme, breaking brantbusinessinteriors.com for ~30 minutes.
> - **2026-05-26 (LAUNCH-1, 20:08:47-04:00)** — theme roles **inverted**. `186373570873` ("BBI Landing Dev") was promoted to `role=main` and is now production. `178274435385` ("BBI Live", Avada) was demoted to `role=unpublished` and is the rollback artifact.
> - **2026-05-27 (~14:25-04:00)** — a `shopify theme dev` watcher (PID 28041) was discovered to have been running since 2026-05-11 bound to LIVE-main `186373570873`. Every `theme/**` edit for 16 days was silently auto-PUT to LIVE within ~1 second of file save, bypassing every approval gate. Watcher killed. See `docs/forensics/2026-05-27-watcher-incident.md`. **The watcher check below (Step 0) is now mandatory before any production write.**
>
> There is no DEV theme anymore. **Every theme write is a production write.** These rules and the preflight check enforce that reality.

---

## Watchers and auto-push

**Never run `shopify theme dev` against a `role=main` theme.** The CLI's `theme dev` subcommand is a filesystem watcher: every local save under `theme/**` is auto-`PUT` to the bound theme within ~1 second of the save event. Bound to LIVE-main, this completely bypasses the approval-gated push discipline the rest of this document is built to enforce — local edits become production writes without any of the pre-write checks, backups, byte-match verifications, or render-checks that the rest of the preflight requires.

In this repo today, there is no dev theme. The only theme roles are LIVE-main (`186373570873`) and rollback-unpublished (`178274435385`), and binding `shopify theme dev` to either is unsafe — LIVE-main is the failure mode below; rollback is the disaster-recovery artifact and must not drift. **Therefore the active rule is stronger than "use a dev theme": do not run `shopify theme dev` against any BBI theme, period, until a dedicated dev theme is provisioned.** If a dev theme is provisioned in future, the rule becomes "only ever bind `shopify theme dev` to a theme with `role ≠ main`."

The `scripts/preflight-watcher-check.sh` script enforces this. The script's posture is strict-binary: any running `shopify theme` process at preflight time fails the check, regardless of subcommand or bound theme. Final stdout line is `RESULT: PASS` or `RESULT: FAIL` for greppable wrapping by automation.

As of 2026-05-28 (PREFLIGHT-AUTOMATION), the watcher check is no longer invoked bare — it is **STEP 1 of the unified `scripts/preflight-write-check.sh` wrapper**, which composes the watcher gate with the theme-role gate (`scripts/preflight-role-check.sh`) and emits one combined `RESULT: PASS|FAIL`. The single wrapper is what runs as **STEP 0** of the PREFLIGHT CHECK below and as **Rule 0** under HARD RULES. Architecture chosen: **(b) composed + wrapper** — the watcher and role checks are both run-once binary session-start gates, so they compose into one command (you can't forget a step); the byte-content comparison (`scripts/preflight-byte-compare.py`) is deliberately NOT in the wrapper because it runs per-file inside the write loop with two file arguments and emits a 3-way classification, not a binary session gate. The wrapper genuinely calls `preflight-watcher-check.sh` as its first step, so the watcher gate is preserved verbatim, not reimplemented.

> **Footnote — incident motivating this section (2026-05-27).** A `shopify theme dev` watcher (PID 28041) was discovered to have been running since 2026-05-11 bound to `--theme=186373570873` (LIVE-main since the 2026-05-26 launch). Every `theme/**` edit for 16 days was silently auto-`PUT` to LIVE within seconds of file save, bypassing every approval gate in this document. Discovered during SCHEMA-CRIT-1 Fix 1: the pre-`PUT` `updated_at` re-check observed LIVE had already drifted forward to the post-fix state before Claude's intentional `PUT` ran. Watcher killed within ~5 minutes; forensic LIVE snapshot captured. Full report: [`docs/forensics/2026-05-27-watcher-incident.md`](../docs/forensics/2026-05-27-watcher-incident.md). The root cause was not the watcher itself — it was that the preflight rule list did not name a watcher check, and *self-enforcement only catches what the doc explicitly enumerates*. This section is the rule-surface fix.

---

```
You are working on the Brant Business Interiors Shopify theme.

BEFORE doing anything else, read and lock in these rules:

THEME IDs (post-LAUNCH-1 — 2026-05-26):
  LIVE (production, role=main)       → 186373570873  "BBI Landing Dev"
                                       brantbusinessinteriors.com
  ROLLBACK (role=unpublished, Avada) → 178274435385  "BBI Live"
                                       last touched 2026-05-26T20:08:47-04:00

There is NO dev theme. Every write is production.

BASELINE ANCHORS (re-confirm in preflight before any write):
  LIVE updated_at expected: 2026-05-26T20:33:23-04:00
    ILLUSTRATIVE, NOT A LIVE ASSERTION. No script reads this
    literal — it is a manual reference for the Rule 2a human
    re-confirm only (preflight-role-check.sh verifies id+role,
    NOT updated_at). It WILL go stale as legitimate writes land
    (e.g. SCHEMA-CRIT-2/3 PRs #33/#34 bumped LIVE to
    2026-05-28T11:32:39-04:00). Treat as "what was the last
    documented write," refresh it in session notes when a write
    lands, and never mistake it for an automated freshness gate.
  Theme check baseline: 2855 offenses across 166 files
    (must HOLD — no new offenses, no net increase)

HARD RULES — no exceptions:
0. WRITE GATE — run scripts/preflight-write-check.sh and confirm
   exit code 0 (final line `RESULT: PASS`) BEFORE doing anything
   else. This unified wrapper runs BOTH session-start gates:
     STEP 1 — watcher check (scripts/preflight-watcher-check.sh):
       a `shopify theme dev` process bound to a role=main theme
       silently auto-PUTs every local theme/** edit to LIVE within
       seconds, bypassing every approval gate in this doc. Added
       2026-05-27 after a 16-day undetected watcher incident — see
       docs/forensics/2026-05-27-watcher-incident.md.
     STEP 2 — role check (scripts/preflight-role-check.sh):
       fresh Admin API assertion that the sole role=main theme is
       id 186373570873. FAILS LOUD if a DIFFERENT theme has become
       main (someone republished / roles drifted). Added 2026-05-28
       after the QW-1 stale-label near-miss — an API-derived
       {id,role} assertion cannot drift the way a memory/name label
       can. The verified `id/role/name` triple it prints should be
       pasted into any verification table you produce.
   Exit 1 / `RESULT: FAIL` = HALT. Fix the offending condition
   (kill the watcher PID, or reconcile the theme-role drift),
   re-run, do not proceed until `RESULT: PASS`. The wrapper accepts
   --expect-id <id> (forwarded to the role check) to protect a
   different production theme in future.
1. Every theme write targets 186373570873 (production). Rule 0's
   role check already asserts this is the role=main theme; still
   confirm the theme ID in any push script before invoking it.
2. PRE-WRITE for every single file:
   a. Re-fetch LIVE updated_at via Admin API. Confirm it has not
      moved since you based your edit (the BASELINE ANCHOR above is
      illustrative — compare against the value you actually pulled
      at session start, re-confirmed by Rule 0's role check). If it
      moved unexpectedly, do NOT bare-HALT on a raw byte diff —
      classify it: pull current LIVE and run
        python3 scripts/preflight-byte-compare.py <your-base> <live>
      SEMANTIC_MISMATCH = someone wrote real content; reconcile.
      SEMANTIC_MATCH = serializer noise only (e.g. JSON \/ re-escape
      from a Theme-Editor save); safe to proceed with annotation —
      this is the Path-A false-positive the byte-compare check was
      built to eliminate.
   b. Snapshot the current LIVE version of the file to
      data/backups/{task-slug}-pre-{ts}/.
      ⚠️ fetch-file.py's DEFAULT theme id is STALE: it hardcodes
      THEME_ID = 178274435385, which post-LAUNCH-1 is the
      role=unpublished ROLLBACK, NOT LIVE. Pulling LIVE means
      targeting 186373570873 explicitly, e.g.:
        curl -s -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" \
          "https://office-central-online.myshopify.com/admin/api/\
2026-04/themes/186373570873/assets.json?asset%5Bkey%5D=<key>"
      Do NOT trust fetch-file.py's default for a LIVE snapshot until
      its theme-id labels are corrected (tracked: FETCH-FILE-STALE-ID).
   c. Snapshot the local file being pushed to the same backup
      dir so the exact diff is recoverable.
3. SCOPE — one logical change, named files only. No bulk
   `shopify theme push` without an explicit per-file scope
   review. `bbi-push-landing.py` should always be invoked with
   the narrowest possible flag set (--layout, --snippets,
   --section <name>, etc).
4. POST-WRITE for every single file:
   a. Re-fetch the just-pushed file from the Admin API (target
      186373570873 — see the Rule 2b fetch-file.py warning) and
      compare against the local source via
        python3 scripts/preflight-byte-compare.py <local> <refetched>
      IDENTICAL or SEMANTIC_MATCH (e.g. Shopify re-escaped \/ on
      save) = write verified, proceed. SEMANTIC_MISMATCH = real
      content differs from what you pushed = HALT + restore from
      backup. (This replaces the old bare byte-equality match, which
      false-HALTed on serializer-noise round-trips.)
   b. Re-run theme check (or scoped subset). Baseline 2855/166
      must hold. Any new offense = HALT + restore.
   c. Render-check every affected URL (homepage, collection,
      PDP, page — whatever the file touches) and visually
      spot-check on mobile + desktop.
5. NEVER skip hooks, never `--force`, never amend a commit that
   has already been pushed.
6. `fetch-file.py` and `find-liquid-bug.py` are read-only and
   safe at any time.
7. If `bbi-push-landing.py` prompts with "WARNING: This is the
   LIVE theme" — that's now expected. Confirm only after the
   pre-write checks above all passed. Never type "yes" reflexively.

ROLLBACK PROCEDURES — know these cold before touching production:

  Method 1 — single-file restore (default):
    1. Locate the pre-write snapshot in
       data/backups/{task-slug}-pre-{ts}/
    2. Re-push the snapshot to LIVE via bbi-push-landing.py with
       the same narrow scope flags.
    3. Re-fetch + byte-match to confirm rollback applied.
    4. Note the rollback in bbi-build-state.md.

  Method 2 — catastrophic full-site rollback (Avada re-publish):
    Only if Method 1 cannot stabilize the site.
    1. PUT https://office-central-online.myshopify.com/admin/api/
       2026-04/themes/178274435385.json
       Body: {"theme": {"role": "main"}}
       (this re-publishes Avada — site is live again on the
        pre-launch theme within seconds)
    2. If 178274435385 has been further altered for any reason,
       restore from the filesystem backup at:
         data/backups/live-theme-pre-launch-20260526-193241/
       MANIFEST.md in that dir documents the restore procedure
       (350 files captured at 19:32:41 on launch day).
    3. Notify Steve. Open an incident note in
       docs/plan/launch-4-24h-monitor-2026-05-26.md.

PUSH COMMAND (always use this form — production):
  export $(grep -v '^#' .env | xargs) && \
    BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873
  Add --layout when touching theme/layout/theme.liquid
  Add --snippets when touching theme/snippets/bbi-*.liquid
  Add --section <name> when touching a single section
  Read the script's confirmation prompt carefully — it now warns
  on LIVE because LIVE is the only target.

PREFLIGHT CHECK — run the unified wrapper now (must pass before any work):

  STEP 0 — WRITE GATE (watcher + role, one command):
    ./scripts/preflight-write-check.sh
  The FINAL stdout line must be `RESULT: PASS` (exit 0). The wrapper
  runs, in order:
    STEP 1/2  preflight-watcher-check.sh  (no shopify theme process)
    STEP 2/2  preflight-role-check.sh     (sole role=main is 186373570873)
  Each sub-gate prints its own `RESULT:` line; the wrapper's combined
  result is the LAST `RESULT:` line. If `RESULT: FAIL`:
    - watcher failure → a shopify theme process is running; kill the
      listed PID, re-run. See docs/forensics/2026-05-27-watcher-
      incident.md.
    - role failure → a DIFFERENT theme is main, no main, multiple
      mains, or the API could not be verified; reconcile theme roles
      before any write. Do NOT proceed until exit 0.
  The role check emits `VERIFIED: id=… role=main name=…` on PASS —
  copy that API-derived triple into any verification table you
  produce (it is the antidote to the QW-1 stale-label framing error).

  Sub-gates remain individually runnable when you need just one:
    ./scripts/preflight-watcher-check.sh   (re-run anytime)
    ./scripts/preflight-role-check.sh      (re-run before each PUT)
  And the per-file byte-content classifier (used in Rules 2a/4a,
  NOT part of the session-start wrapper):
    python3 scripts/preflight-byte-compare.py <local> <live>

  (The former inline-python role check is superseded by the tested
  preflight-role-check.sh — see scripts/test-preflight-checks.sh for
  the fail-on-bad regression suite that proves it.)

CONTENT / PAGE-EDIT GATE — architecture discovery BEFORE scoping page or copy edits:
  Any session that edits a page, collection, or its SEO/copy must START by
  discovering WHERE the content actually lives — do NOT assume classic CMS
  body_html. BBI uses a hybrid content model (lesson SHOPIFY-CONTENT-MODEL-
  NOT-UNIFORM, docs/strategy/bbi-keyword-map-2026-05-31.md → Operational lessons):
    - Landing pages (design-services, professional-services, healthcare, etc.):
      CMS body is EMPTY; H1/intro/FAQ/CTA/links are hardcoded in theme Liquid
      sections (ds-lp-*.liquid) via section.settings. Only SEO title/meta
      (metafields global.title_tag / global.description_tag) are editable
      WITHOUT a theme write — body/H1/FAQ/links need a theme-edit session.
    - Collections: description body is a real CMS field but only renders if the
      template section outputs {{ collection.description }} (true for
      ds-collection-base / default collection.json; FALSE for ds-cs-base "base"
      suffix and ds-cc-base). SEO seo{} (title/meta) always applies.
    - Slugs in strategy docs are NOT authoritative — verify the real handle +
      template against the live store and nav menu first.
  Discovery query first (CMS body vs metafields vs template-section + does the
  target field render), THEN scope what's editable, THEN decide if a theme-edit
  session is required. SEO meta is always safe (no theme files). Precedent +
  full friction log: docs/reviews/priority-refresh-2026-05-31.md (PHASE-C-STREAM-B).

REFERENCE DOCS — read these to ground the session:
  - docs/plan/bbi-build-state.md             (canonical source of truth)
  - BBI-Session-Kickoff/02-current-status.md (latest session snapshot)
  - docs/plan/launch-4-24h-monitor-2026-05-26.md
                                             (24h monitor checks + red flags)
  - BBI-Session-Kickoff/measurement-protocols.md
                                             (measurement disciplines — cite
                                              before reporting any perf metric;
                                              PERFORMANCE-MEASUREMENT-DISCIPLINE
                                              = multi-run median on fast pages)
  - data/reference/priority-keywords.yaml    (v1 — LOCKED page→keyword
                                              assignments; read in Phase 0 of any
                                              keyword/SEO/page-copy session BEFORE
                                              touching meta or copy. 4 of ~8
                                              clusters locked; rest PENDING under
                                              pending_clusters, not missing)
  - docs/strategy/bbi-keyword-map-2026-05-31.md
                                             (human-readable keyword map +
                                              Operational lessons incl.
                                              SHOPIFY-CONTENT-MODEL-NOT-UNIFORM)
```
