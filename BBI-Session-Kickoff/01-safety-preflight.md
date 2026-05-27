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

The `scripts/preflight-watcher-check.sh` script enforces this. It runs as **STEP 0** of the PREFLIGHT CHECK below, and as **Rule 0** under HARD RULES. The script's posture is strict-binary: any running `shopify theme` process at preflight time fails the check, regardless of subcommand or bound theme. Final stdout line is `RESULT: PASS` or `RESULT: FAIL` for greppable wrapping by future automation.

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
    (or the most recent documented post-launch write — bump this
     anchor in your session notes when a legitimate write lands)
  Theme check baseline: 2855 offenses across 166 files
    (must HOLD — no new offenses, no net increase)

HARD RULES — no exceptions:
0. WATCHER CHECK — run scripts/preflight-watcher-check.sh and
   confirm exit code 0 BEFORE doing anything else. A
   `shopify theme dev` process bound to a role=main theme will
   silently auto-PUT every local theme/** edit to LIVE within
   seconds, completely bypassing the approval gates in this doc.
   This rule was added 2026-05-27 after a 16-day undetected
   watcher incident — see docs/forensics/2026-05-27-watcher-
   incident.md. Exit 1 from the script = HALT, kill the
   offending process, re-run, do not proceed until exit 0.
1. Every theme write targets 186373570873 (production). Confirm
   the theme ID in any push script before invoking it.
2. PRE-WRITE for every single file:
   a. Re-fetch LIVE updated_at via Admin API. Confirm it matches
      the expected baseline. If it changed unexpectedly, HALT —
      someone else (or another session) wrote. Reconcile first.
   b. Snapshot the current LIVE version of the file to
      data/backups/{task-slug}-pre-{ts}/ via fetch-file.py.
   c. Snapshot the local file being pushed to the same backup
      dir so the exact diff is recoverable.
3. SCOPE — one logical change, named files only. No bulk
   `shopify theme push` without an explicit per-file scope
   review. `bbi-push-landing.py` should always be invoked with
   the narrowest possible flag set (--layout, --snippets,
   --section <name>, etc).
4. POST-WRITE for every single file:
   a. Re-fetch the just-pushed file from the Admin API and
      byte-match against the local source. Mismatch = HALT +
      restore from backup.
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

PREFLIGHT CHECK — run BOTH steps now (must pass before any work):

  STEP 0 — WATCHER CHECK (added 2026-05-27, hard gate):
    ./scripts/preflight-watcher-check.sh
  Exit code MUST be 0. If exit 1: a shopify theme dev watcher
  (or unresolved-role / role=main shopify theme process) is
  running. Kill the listed PID. Re-run until exit 0. Do NOT
  continue to STEP 1 until this passes. See
  docs/forensics/2026-05-27-watcher-incident.md for the
  incident that motivated this gate.

  STEP 1 — THEME-ROLE CHECK:
  python3 -c "
  import urllib.request, json, os, sys
  TOKEN = os.environ['SHOPIFY_TOKEN']
  STORE = 'office-central-online.myshopify.com'
  EXPECT = {
      '186373570873': ('main',         'BBI Landing Dev'),
      '178274435385': ('unpublished',  'BBI Live'),
  }
  ok = True
  for tid, (want_role, want_name) in EXPECT.items():
      req = urllib.request.Request(
          f'https://{STORE}/admin/api/2026-04/themes/{tid}.json',
          headers={'X-Shopify-Access-Token': TOKEN}
      )
      t = json.loads(urllib.request.urlopen(req).read())['theme']
      tag = 'LIVE' if want_role == 'main' else 'ROLLBACK'
      flag = 'OK' if t['role'] == want_role else 'MISMATCH'
      if t['role'] != want_role:
          ok = False
      print(f'{tag}: id={t[\"id\"]}  name={t[\"name\"]}  '
            f'role={t[\"role\"]}  updated_at={t[\"updated_at\"]}  [{flag}]')
  if not ok:
      print('PREFLIGHT FAILED — theme roles do not match expected '
            'post-launch state. HALT.')
      sys.exit(1)
  print('Preflight OK. Production write target: 186373570873.')
  print('Re-confirm LIVE updated_at against your session baseline '
        'before each write.')
  "

REFERENCE DOCS — read these to ground the session:
  - docs/plan/bbi-build-state.md             (canonical source of truth)
  - BBI-Session-Kickoff/02-current-status.md (latest session snapshot)
  - docs/plan/launch-4-24h-monitor-2026-05-26.md
                                             (24h monitor checks + red flags)
```
