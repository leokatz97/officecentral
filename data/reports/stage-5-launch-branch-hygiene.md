# Stage 5 — Branch Hygiene Report
**Date:** 2026-05-08
**Performed by:** Claude Code (claude-sonnet-4-6)

---

## Summary

| Category | Count |
|---|---|
| Merged branches deleted (local + remote) | 11 |
| Unmerged branches requiring Steve decision | 2 |
| Local `claude/*` branches total | 193 |
| Local `claude/*` with 0 unique commits (safe to delete) | 173 |
| Local `claude/*` with unique commits (Steve review needed) | 20 |
| Remote `claude/*` branches | 18 |
| Stray worktrees | 0 |

---

## Phase 1.1 — Merged branches deleted

All 11 branches below had been fully merged into `main`. Deleted from both local and remote.

| Branch | Notes |
|---|---|
| `chore/json-template-link-audit-2026-05-07` | Stage 1.6 link audit work |
| `chore/reconcile-dev-theme-2026-05-07` | Stage 1 dev-theme reconciliation |
| `chore/resolve-internal-404s-2026-05-07` | Stage 1.5 sub-collection 404 fixes |
| `chore/stabilize-chrome-2026-05-07` | Stage 2 chrome stabilization |
| `chore/stage-3.1d-empty-hub-rules` | Stage 3.1d empty hub smart-rule fix |
| `chore/stage-3.2-tile-height-polish` | Stage 3.2 product-card flex-column polish |
| `chore/stage-3.2c-subcollection-migration` | Stage 3.2c canonical-handle migration |
| `feature/stage-3.0-design-tokens` | Stage 3.0 design token rollout |
| `feature/stage-3.1b-hub-t3-layout` | Stage 3.1b T3 hub layout refactor |
| `feature/stage-3.1c.1-hero-stats-and-counts` | Stage 3.1c.1 hero stats + pill counts |
| `feature/stage-3.2b-subcollection-t4` | Stage 3.2b T4 sub-collection refactor |

---

## Phase 1.2 — Unmerged branches requiring Steve decision

These branches exist locally and have commits that are not on `main`. They were NOT deleted.

| Branch | Age | Status | Recommendation |
|---|---|---|---|
| `feature/ds-0-screen-exports-audit` | 4 days | Not merged | Steve: review and either merge or close. Work is exploratory screen-export audit from before Stage 3.0. If the locked screenshots are captured elsewhere, this can be deleted. |
| `feature/stage-4b-pdp-design-parity` | ~86 min old at time of audit | Active / keep | This is the in-progress PDP build branch. Do NOT delete. Continue on this branch when Stage 4b resumes. |

---

## Phase 1.3 — Stale worktrees

No stray `.claude/worktrees/` directories found. Clean.

---

## Phase 1.4 — `claude/*` branches

### 173 safe to delete (0 unique commits each)

These 173 local `claude/*` branches have no commits beyond what is already on `main`. They are Claude Code agent workspace branches that were created automatically and never used for real work. They are safe to delete in bulk.

**Recommended bulk-delete command (requires Steve approval before running):**
```bash
git branch | grep 'claude/' | while read b; do
  count=$(git rev-list --count main..$b 2>/dev/null)
  if [ "$count" = "0" ]; then
    git branch -d "$b"
  fi
done
```

### 20 `claude/*` branches with unique commits — Steve review needed

These branches each have 1 or more commits not on `main`. They may represent in-progress or abandoned work. Review before deleting.

| Branch | Unique commits | Action needed |
|---|---|---|
| `claude/adoring-lewin-624ec2` | 1 | Review: merge, cherry-pick, or close |
| `claude/crazy-matsumoto-3d9a1a` | 7 | Review: likely multi-step work session — inspect log |
| `claude/determined-proskuriakova-55dc9f` | 1 | Review |
| `claude/gallant-knuth-f995f9` | 5 | Review |
| `claude/gracious-brahmagupta-3c01c6` | 4 | Review |
| `claude/hungry-turing-250b42` | 1 | Review |
| `claude/inspiring-williams-bf2635` | 1 | Review |
| `claude/jolly-williamson-7100c7` | 1 | Review |
| `claude/kind-fermi-42c93a` | 1 | Review |
| `claude/nervous-knuth-8eb63a` | 4 | Review |
| `claude/nice-brown-bedeb9` | 11 | Review: 11 commits — may be significant feature work |
| `claude/nice-lehmann-742ba5` | 1 | Review |
| `claude/pe3-rebrand-fix` | 1 | Review |
| `claude/pe3-strip-tm-symbols` | 1 | Review |
| `claude/recursing-kowalevski-54cfc7` | 1 | Review |
| `claude/recursing-spence-c8ae35` | 1 | Review |
| `claude/stoic-fermat-18f681` | 4 | Review |
| `claude/vigilant-proskuriakova-448c38` | 1 | Review |
| `claude/wonderful-williamson-effe0e` | 4 | Review |
| `claude/xenodochial-boyd-a7fab9` | 1 | Review |

---

## Phase 1.5 — Remote `claude/*` branches

18 remote `claude/*` branches exist on `origin`. These should be reviewed alongside the local unique-commit list above. Remote branches persist until explicitly deleted and may be taking up unnecessary space. Recommend deleting remotes that correspond to already-merged work after Steve's review.

**To list current remote claude/* branches:**
```bash
git branch -r | grep 'origin/claude/'
```

---

## Next steps

1. **Steve to review** the 20 unique-commit `claude/*` branches. For each: inspect `git log --oneline main..{branch}` and decide merge/cherry-pick/delete.
2. **After review:** bulk-delete the 173 zero-commit `claude/*` branches (command above).
3. **After bulk-delete:** prune remote branches with `git remote prune origin`.
4. **`feature/ds-0-screen-exports-audit`:** Steve decision — merge or close.
5. **`feature/stage-4b-pdp-design-parity`:** Keep; resume when Stage 4b PDP build starts.
