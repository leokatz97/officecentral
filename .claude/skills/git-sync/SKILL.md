---
name: git-sync
description: |
  End-of-session cleanup and sync for the Office Central / BBI repo.
  Use this skill when Leo says "sync", "commit everything", "clean and update git",
  "push what I've done", "go", or "clean and update git/local".
  Runs a full 9-step close-out: reorganizes folders, refreshes CLAUDE.md, stages the right
  files (skipping secrets/artefacts), writes a clear commit message, commits, and pushes
  to origin/main — leaving the repo in a clean state for the next session.
---

# git-sync — BBI Session Commit & Push

Full end-of-session close-out: reorganize folders, refresh CLAUDE.md, stage the right
files (skipping secrets and junk), write a clear commit message, commit, and push.
Leaves the repo in a clean, well-documented state ready for the next session.

---

## Step 1 — Assess the current state

Run these commands in the repo root (`/Users/leokatz/Desktop/Office Central/`):

```bash
git status
git diff --stat HEAD
git log --oneline origin/main..HEAD   # commits not yet pushed
```

Report:
- Modified / deleted tracked files
- Untracked new files
- Number of commits ahead of `origin/main`

---

## Step 2 — Reorganize folders for next session

Before staging anything, tidy the repo so the committed state is clean and the next
session can orient fast.

### previews/
- Keep: active checklists, trackers, and pages Leo actively references
- Delete or archive: any `.html` file whose corresponding plan/feature is complete and
  no longer being tracked (e.g. old status snapshots superseded by newer ones)
- Naming: files should match their content — rename if the filename is stale

### data/
- `data/specs/`, `data/reports/`, `data/redirects/`, `data/exports/` — keep, these are source of truth
- `data/backups/` and `data/logs/` — do NOT commit; these are runtime artefacts
- Loose files dropped directly in `data/` root — move to the right subdirectory or flag for review

### docs/
- `docs/plan/` — keep `shopify-fix-plan.md` (active), `ideas-backlog.md` (active); archive or delete stale snapshots older than 2 weeks
- `docs/strategy/` — keep brand/ICP/voice docs; flag anything outdated
- `docs/workflows/` — keep runbooks; update if a process changed this session
- `docs/reviews/` — keep the latest review artefact; delete older duplicates

### scripts/
- Loose scripts in `scripts/` root are fine — just confirm there are no duplicate or
  orphaned scripts that were replaced by a newer version this session
- If a script was made obsolete, delete it or add a `# DEPRECATED` comment at the top

### .claude/skills/
- Confirm each skill folder has exactly one `SKILL.md` and nothing else (no temp files)
- If a new skill was added this session, verify its frontmatter `name` matches the folder name

### General
```bash
# Remove all .DS_Store files
find . -name ".DS_Store" -not -path "./.git/*" -delete

# List any empty directories that can be removed
find . -type d -empty -not -path "./.git/*"
```

Flag anything ambiguous to Leo before deleting.

---

## Step 3 — Update CLAUDE.md

Refresh `CLAUDE.md` so the next session starts with accurate context. Check and update
these sections:

### Key Reference Files table
Verify every file in the table still exists at the listed path. Update paths for anything
that moved, and add new key files created this session (new checklists, new strategy docs, etc.).

```markdown
| Need | File |
|---|---|
| Live task list | docs/plan/shopify-fix-plan.md |
| ... | ... |
```

### Project Structure diagram
If new top-level directories or meaningful subdirectories were added this session, add them
to the ASCII tree in the "Project Structure" section.

### Skills inventory (if tracked)
If CLAUDE.md lists available skills anywhere, add any new skills created this session.

### Session notes (optional)
If there's a "Current focus" or "Last session" section, update it to reflect what was
completed and what's next. Keep it to 3-5 bullet points max.

After editing, confirm the file saves cleanly and `git diff CLAUDE.md` looks right.

---

## Step 4 — Categorize changes into buckets (after cleanup)

Sort every changed/untracked file into one of these buckets:

| Bucket | Paths |
|---|---|
| Theme / Liquid | `theme/**` |
| Previews / HTML | `previews/**` |
| Scripts | `scripts/**` |
| Docs / Plan | `docs/**` |
| Data (safe) | `data/specs/**`, `data/reports/**`, `data/redirects/**`, `data/exports/**`, `data/oci-photos/**`, `data/design-photos/**` |
| Skills | `.claude/skills/**` |
| Config / Root | `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `.gitignore`, `.shopifyignore`, `package.json`, `package-lock.json` |
| **SKIP — never stage** | `.env`, `config/settings_data.json`, `node_modules/`, `.DS_Store`, `*.log`, `data/backups/**`, `data/logs/**`, `data/oci-photos/*.png` (raw screenshots), `.claude/worktrees/**` |

If `.env` appears anywhere in the untracked or modified list, **stop and warn Leo** before proceeding.

---

## Step 5 — Stage selectively

Add only files in the allowed buckets:

```bash
# Stage tracked modifications and deletions
git add -u

# Stage new untracked files in allowed buckets (adjust paths as needed)
git add previews/ scripts/ docs/ theme/ .claude/skills/ CLAUDE.md README.md CHANGELOG.md .gitignore .shopifyignore

# Explicitly reset anything that snuck in from the skip list
git reset HEAD data/backups/ data/logs/ data/oci-photos/*.png config/settings_data.json .env 2>/dev/null || true
```

Then run `git status` again to confirm the staging area looks correct before committing.

---

## Step 6 — Draft the commit message

Write a concise imperative subject line (≤72 chars) that captures the dominant theme of the
session. If multiple buckets changed, add a blank line then bullet-point each bucket.

**Format:**
```
<Verb> <what changed> [and <second thing>]

- Previews: <brief description>
- Scripts: <brief description>
- Docs: <brief description>
- Skills: <brief description>
- Removed: <deleted files>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Good subject lines:**
- `Add BBI homepage hero section and update build checklist`
- `Enrich product tags and refresh previews`
- `Add git-sync skill and clean up stale preview files`

**Bad (avoid):**
- `Update files` — too vague
- `Fixed stuff` — past tense, no detail
- `WIP` — never commit WIP

---

## Step 7 — Commit

```bash
git commit -m "$(cat <<'EOF'
<subject line here>

- Bucket: detail
- Bucket: detail

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Step 8 — Push

```bash
git push origin main
```

If the push is rejected (non-fast-forward), run `git pull --rebase origin main` first, then
push again. Never force-push to `main`.

---

## Step 9 — Confirm and report

Run:
```bash
git log --oneline -3
```

Report back to Leo:
- ✅ Commit hash + subject
- 📁 Files committed (by bucket)
- 🚀 Pushed to `origin/main`

---

## BBI Safety Rules (always enforced)

- **Never commit** `.env`, `config/settings_data.json`, `node_modules/`, `.DS_Store`
- **Never force-push** to `main`
- **Never skip hooks** (`--no-verify`)
- `data/backups/` and `data/logs/` are runtime artefacts — exclude always
- If unsure whether a file is sensitive, ask before staging it
