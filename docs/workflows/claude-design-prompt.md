# Claude Code prompt — generate the Claude Design session playbook

**Use this prompt when you're ready to run the design system rebuild.** Paste the block below into a fresh Claude Code session at the repo root. It will produce `docs/workflows/claude-design-session-playbook.md`, which is your move-by-move script for the actual claude.ai/design session.

**Prerequisites:**
- These files must already exist in the repo (they were created 2026-04-27):
  - `docs/strategy/design-system.md`
  - `docs/strategy/design-system-brief.md`
  - `docs/reviews/design-system-audit-2026-04-27.md`
  - `data/logos/bbi-logo-hires.png`

**Why this prompt is tight:** every line costs tokens — both in Claude Code (when generating the playbook) and downstream in Claude Design (when executing it). Front-loading constraints, forbidding agent spawns, and capping prompt count per Claude Design phase keeps both sides cheap.

---

## The prompt

```
Read these and output one markdown playbook. Don't re-explore the repo.

Inputs (one read pass each):
- docs/strategy/design-system.md — canonical spec with locked anchors and TBD slots
- docs/strategy/design-system-brief.md — paste-ready brief for Claude Design
- docs/reviews/design-system-audit-2026-04-27.md — token map and code hotspots
- data/logos/bbi-logo-hires.png — brand mark (just look at it)
- CLAUDE.md — project rules

Goal: a step-by-step Claude Design session playbook optimized for minimum
prompts in Claude Design. Save to docs/workflows/claude-design-session-playbook.md.

Required sections:
1. Pre-flight checklist — which dev theme to pull settings from, which 5
   screenshots to capture from the live site, which files to have open in tabs.
2. Three sequential Claude Design chats — Tokens, then Components, then Screens.
   Use one chat per phase to keep context clean. For each phase produce:
   a. The exact opening message to paste (composed from the brief, with
      attachment instructions for logo + screenshots)
   b. 3–5 stress-test follow-up prompts
   c. Pass/fail gates to verify before moving to the next chat
   d. Pushback phrases ready to send if quality is off — e.g. red-text below
      5.0:1 on white, missing focus rings, red density over 8%, link color
      indistinguishable from body text
3. Post-session steps — how to fill design-system.md TBDs, how to enter values
   in Shopify Admin on a duplicate theme, one-time code edits per the audit
   (#ffca10 in dark mode, #f00f00 typo in blinking-icons.liquid, #FFCA10 in
   shapes.liquid).
4. Credit-budget table — estimated prompt count per Claude Design phase.
   Target ≤6 prompts per phase. Front-load constraints; reserve follow-ups
   for stress tests and pushback only.

Constraints (this matters for credit cost):
- Don't re-grep the theme — the audit already enumerated every token.
- Don't propose new token names — consume the Shopify vocabulary as-is.
- Don't ask clarifying questions before producing the playbook. Flag genuine
  ambiguity inline as OPEN QUESTION and continue.
- No agent spawns, no Task tool sub-delegations, no exploratory subtasks.
- One read per input, one Write call for the output.
- Anchor hexes are locked: red #D4252A, charcoal #0B0B0C. Don't relitigate.

Output: one file. Tight prose. Tables where they help. No multi-file scaffold.
```

---

## After Claude Code finishes

You'll have `docs/workflows/claude-design-session-playbook.md` in the repo. Open it, follow it phase by phase. The playbook tells you exactly what to paste into claude.ai/design and when.
