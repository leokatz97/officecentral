# Step 1 — Safety Preflight (Post-Launch)
**Paste this as your first message in every new Claude Code session. Do not skip.**

---

> **Why this exists:**
> - **2026-05-10** — a session pushed `theme.liquid` + two snippet stubs to the live theme, breaking brantbusinessinteriors.com for ~30 minutes.
> - **2026-05-26 (LAUNCH-1, 20:08:47-04:00)** — theme roles **inverted**. `186373570873` ("BBI Landing Dev") was promoted to `role=main` and is now production. `178274435385` ("BBI Live", Avada) was demoted to `role=unpublished` and is the rollback artifact.
>
> There is no DEV theme anymore. **Every theme write is a production write.** These rules and the preflight check enforce that reality.

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

PREFLIGHT CHECK — run this now (must pass before any work):
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
