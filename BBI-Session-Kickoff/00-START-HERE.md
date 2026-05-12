# BBI — New Session Kickoff
**Last updated:** 2026-05-11

This folder contains everything needed to start a fresh Claude Code session on the BBI Shopify project and be fully up to speed instantly.

---

## Do this in order

### Step 1 — Paste the safety preflight
Open `01-safety-preflight.md`. Copy the entire code block and paste it as your first message in the new Claude Code session. Do not skip this. A previous session pushed files to the live theme by accident and broke the site for 30 minutes. The preflight prevents that.

### Step 2 — Share the current status
Open `02-current-status.md`. This is the full picture of where the project stands: what's done, what's blocked, what decisions are pending, and the critical path to launch. Either paste it or tell Claude to read `BBI-Session-Kickoff/02-current-status.md`.

### Step 3 — Pick a prompt and run it
Open `03-prompts-ready.md`. Each prompt is self-contained and ready to paste. Run them in the order shown — Prompt 0 (black page fix) is the current blocker.

---

## What Claude Code auto-loads (no action needed)

`CLAUDE.md` is in the repo root and loads automatically. It gives Claude Code the project rules, BBI-specific guardrails, and pointers to `docs/plan/bbi-build-state.md` (the full task backlog) and other key strategy docs. You do not need to paste those manually.

---

## Only needed for specific tasks

| Doc | When to share it |
|---|---|
| `docs/strategy/icp.md` | Any copy or content writing (product descriptions, page copy) |
| `docs/strategy/voice-samples.md` | Same — approved copy examples |
| `docs/plan/bbi-lead-routing.md` | Working on LEAD-3 quote form routing |
| `docs/plan/bbi-interlinking-map.md` | Building or auditing page cross-links |
| `docs/strategy/bbi-nav-spec.md` | Touching nav or footer |

---

## Key IDs

| Thing | Value |
|---|---|
| Dev theme (write target) | `186373570873` — BBI Landing Dev |
| Live theme (never write) | `178274435385` — brantbusinessinteriors.com |
| Store | `office-central-online.myshopify.com` |
| Admin | `admin.shopify.com/store/office-central-online` |
