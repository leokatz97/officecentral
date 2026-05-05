# Track D — Design System

**Status:** DS-0 → DS-4 all complete (s2) · Track D DONE · `/bbi-build-page` READY
**Owner:** Steve / Leo
**Dev theme target:** BBI Landing Dev (`186373570873`) — never publish to live until LAUNCH-2
**Confirmed:** 2026-05-04

---

## Gate

```bash
grep -c TBD docs/strategy/design-system.md
# → 53
```

The gate is the live count of unresolved TBDs in the canonical design-system spec.
The gate **closes on DS-1** (fill TBDs), not DS-0. DS-0 lands the inputs DS-1 needs.

---

## SEEDS rows (full Track D chain)

| Row | Title | Status | Closes |
|---|---|---|---|
| **DS-0** | Land Claude Design Phase 3 — 5 screen exports + audit tables | **s2 (complete)** | Inputs for DS-1 |
| **DS-1** | Fill `design-system.md` TBD placeholders | not started | `grep -c TBD → 0` (gate) |
| **DS-2** | Push design tokens to BBI Landing Dev (theme `186373570873`) | **s2 (complete)** | `settings_data.json` updated on dev |
| **DS-3** | Three Liquid edits + PR + push to BBI Landing Dev | **s2 (complete)** | dark-mode block deleted; `#f00f00`/`#FFCA10` → `#D4252A` |
| **DS-4** | `/bbi-build-page` readiness check (9-row pass/fail) | **s2 (complete)** | Verdict line `READY` — blocks every P1 row |

DS-0 → DS-4 must run in order. DS-4 is the blocking gate before any P1 build runs.

---

## Screen rounds

- **T2** — locked → `data/design-photos/screens-t2-locked-2026-04-28/`
- **T3** — locked → `data/design-photos/screens-t3-LOCKED-2026-04-29/`
- **T4** — **locked** → `data/design-photos/round4-template-3-attachments/` (LOCKED files confirmed 2026-05-04)
- **T5** — **locked** → `data/design-photos/screens-t5-2026-05-04/` (OECM landing + PDP unbuyable — new 2026-05-04)

### 5 screens in scope
1. Homepage
2. Collection — category
3. Collection — sub
4. OECM landing
5. PDP — unbuyable (Request a Quote variant)

---

## Attachments under `data/design-photos/`

All design attachments (HTML deliverables, locked screens, component zips, baselines) land here.

**Foundations zip — DS-0 inputs:**
- `components-v1-2026-04-27/tokens.css` — design tokens (CSS custom properties)
- `components-v1-2026-04-27/Components.html` — component spec deliverable
- `components-v1-2026-04-27/bbi-logo-v2.png` — new BBI logo

**Round artefacts:**
- `screens-t2-locked-2026-04-28/`, `screens-t2-final-2026-04-28/` — T2
- `screens-t3-LOCKED-2026-04-29/`, `screens-t3-r1-2026-04-29/` — T3
- `round3-template-2-attachments/`, `round4-template-3-attachments/` — round inputs
- `screens-t5-2026-05-04/landing-oecm/` — T5 OECM landing (Template 4)
- `screens-t5-2026-05-04/pdp-unbuyable/` — T5 PDP unbuyable (Template 5)

**Anti-reference baselines:**
- `ANTI-REF-baseline-2026-04-27-homepage.png`
- `ANTI-REF-baseline-2026-04-27-nav.png`

These are the "moving away from" reference — attached to Claude Design briefs as anti-patterns so the model knows what not to reproduce. Not aspirational; cautionary.

---

## Reference files

| Need | File |
|---|---|
| Canonical spec (gate source) | [docs/strategy/design-system.md](../../strategy/design-system.md) |
| Tokens — DS-2 output (consumed by `style-variables.liquid`) | [docs/strategy/bbi-design-tokens-v1.css](../../strategy/bbi-design-tokens-v1.css) |
| Claude Design constraint brief | [docs/strategy/design-system-brief.md](../../strategy/design-system-brief.md) |
| Component spec v1 | [docs/strategy/bbi-component-spec-v1.md](../../strategy/bbi-component-spec-v1.md) |
| Pre-rebuild audit (CSS → Shopify field map) | [docs/reviews/design-system-audit-2026-04-27.md](../../reviews/design-system-audit-2026-04-27.md) |
| Foundations zip (HTML + tokens) | [data/design-photos/components-v1-2026-04-27/](../../../data/design-photos/components-v1-2026-04-27/) |
| T2 locked | [data/design-photos/screens-t2-locked-2026-04-28/](../../../data/design-photos/screens-t2-locked-2026-04-28/) |
| T3 locked | [data/design-photos/screens-t3-LOCKED-2026-04-29/](../../../data/design-photos/screens-t3-LOCKED-2026-04-29/) |
| T4 (locked) | [data/design-photos/round4-template-3-attachments/](../../../data/design-photos/round4-template-3-attachments/) |
| T5 (locked) | [data/design-photos/screens-t5-2026-05-04/](../../../data/design-photos/screens-t5-2026-05-04/) |
| **DS-0 audit doc** | [docs/strategy/bbi-screens-audit-v1.md](../../strategy/bbi-screens-audit-v1.md) |
| Live SEEDS checklist | [docs/plan/website-fix-checklist.html](../website-fix-checklist.html) |

---

## Exit criteria

- [x] DS-0: 5 locked screen exports (homepage, collection.category, collection sub, OECM landing, PDP unbuyable) at 1440px + 375px in `data/design-photos/screens-t*/` + audit tables in `docs/strategy/bbi-screens-audit-v1.md`
- [ ] DS-1: `grep -c TBD docs/strategy/design-system.md` returns `0` (gate)
- [x] DS-2: tokens pushed to BBI Landing Dev `settings_data.json`; baseline backup + push log written
- [x] DS-3: dark-mode block deleted from `theme/snippets/style-variables.liquid`; `#f00f00` and `#FFCA10` replaced with `#D4252A`; pushed to BBI Landing Dev
- [x] DS-4: 9-row readiness check returns `READY` — unblocks P1
- [ ] T4 round locked
- [ ] All 5 screens promoted from screen exports into `theme/` sections + snippets

When every box ticks, Track D is done and `/bbi-build-page` can run.

---

## DS-4 — `/bbi-build-page` Readiness Check (2026-05-04)

| Row | Check | Result |
|---|---|---|
| R1 | `grep -c TBD docs/strategy/design-system.md` → 0 | **PASS** (0) |
| R2 | Token spot-check: `btn_hover_color=#D4252A`, `background_footer=#0B0B0C`, `primary.button_bg_hover=#D4252A` | **PASS** |
| R3 | No `[color-mode="dark"]` in `style-variables.liquid` | **PASS** (0) |
| R4 | All 9 `ds-*` sections on dev theme `186373570873` | **PASS** |
| R5 | All 3 `ds-*` snippets on dev theme | **PASS** |
| R6 | `ds-landing.css` + `ds-landing.js` assets on dev theme | **PASS** |
| R7 | `page.oecm.json` + `page.brand-dealer.json` templates on dev theme | **PASS** |
| R8 | `bbi_landing` layout gate in `theme.liquid` (≥1 occurrence) | **PASS** (5) |
| R9 | `data/oci-photos/catalog.json` exists with ≥1 photo | **PASS** (48) |

**VERDICT: READY** — P1 build is unblocked.
