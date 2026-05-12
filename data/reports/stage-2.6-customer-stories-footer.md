# Stage 2.6 — Customer Stories Footer Fix

**Date:** 2026-05-07  
**Branch:** chore/stabilize-chrome-2026-05-07  
**Commit:** d22589c

---

## Root-Cause Confirmation

The `/* Footer */` CSS block in `theme/sections/ds-lp-customer-stories.liquid` contained 8 rules that were stale or actively harmful relative to the current `bbi-footer` snippet.

**Primary cause (invisible footer):**  
`.lp-stories .bbi-footer { background: var(--background); ... }` — the `.lp-stories .bbi-footer` selector (specificity: 2 classes) outranks the snippet's own `.bbi-footer` rule (1 class). The page-level `--background` token resolves to `#FFFFFF` (white) under `.lp-stories.scheme-default`. The snippet's canonical dark token `--ft-fg: #FFFFFF` was already setting text and links to white — so white text on a white background, rendering the footer invisible.

**Secondary cause (stale dead rules):**  
Three classes targeted by the scoped block (`__grid`, `__col-head`, `__links`) do not exist in the current `bbi-footer.liquid` snippet, which uses `__top`, `__columns`, `__column h4`, and `__column ul` instead.

---

## Stale CSS Rules Removed

All 10 lines (9 rules + 1 comment) removed from `ds-lp-customer-stories.liquid`:

| Selector | Verdict | Reason |
|---|---|---|
| `/* Footer */` | removed | comment block header |
| `.lp-stories .bbi-footer` | **HARMFUL** | overrides snippet's dark `var(--ft-bg)` with white `var(--background)` |
| `.lp-stories .bbi-footer__inner` | removed | strips snippet's `padding:64px 32px 24px`; snippet handles correctly |
| `.lp-stories .bbi-footer__grid` | **STALE** | class does not exist in snippet (→ `__columns`) |
| `.lp-stories .bbi-footer__col-head` | **STALE** | class does not exist in snippet (→ `__column h4`) |
| `.lp-stories .bbi-footer__links` | **STALE** | class does not exist in snippet (→ `__column ul`) |
| `.lp-stories .bbi-footer__links a` | **STALE** | class does not exist in snippet |
| `.lp-stories .bbi-footer__links a:hover` | **STALE** | class does not exist in snippet |
| `.lp-stories .bbi-footer__bottom` | removed | overrides snippet's dark-theme color/opacity tokens |
| `.lp-stories .bbi-footer__grid` (responsive) | **STALE** | class does not exist in snippet |

---

## Surviving CSS Rules

**None.** The entire footer CSS block was removed.

**Justification:** `bbi-footer.liquid` is fully self-contained. It defines its own local CSS tokens on `.bbi-footer`:

```css
.bbi-footer {
  --ft-bg:    #0B0B0C;
  --ft-fg:    #FFFFFF;
  --ft-muted: rgba(255,255,255,0.65);
  --ft-dim:   rgba(255,255,255,0.45);
  --ft-border:#1F1F21;
  background: var(--ft-bg);
  color:      var(--ft-fg);
}
```

These tokens are scoped to `.bbi-footer` and are independent of the page's light/dark scheme. No page-level override is needed or appropriate. The snippet also handles its own responsive breakpoints at 1023px and 479px.

---

## Comparison Against ds-lp-about.liquid

`ds-lp-about.liquid` (lines 97–107) also scopes footer CSS — it overrides `__inner` layout and `__bottom` colours. This pattern is **not ideal** either (it also overrides snippet background), but the task spec calls out about as the reference point for "light scoping" rather than the goal state. Customer-stories now takes the cleaner path: zero overrides, let the snippet own its own styling entirely.

---

## Pre-Fix vs Post-Fix

**Pre-fix (static analysis):**  
`.lp-stories .bbi-footer { background: var(--background) }` resolves to `background: #FFFFFF`. Snippet text/links use `--ft-fg: #FFFFFF`. Result: white text on white background → footer invisible.

**Post-fix (static analysis):**  
No scoped override exists. Snippet's `.bbi-footer { background: var(--ft-bg) }` resolves to `background: #0B0B0C` (dark). Text/links use `--ft-fg: #FFFFFF`. Result: white text on dark background → footer visible.

**Push confirmation:**
```
✅ Pushed sections/ds-lp-customer-stories.liquid
   theme_id:   186373570873
   updated_at: 2026-05-07T13:12:03-04:00
   size:       21182 bytes
```

Verify visually at:  
`https://office-central-online.myshopify.com/pages/customer-stories?preview_theme_id=186373570873`

---

## Integrity Checks

- **`bbi-footer.liquid` not modified:** `git diff theme/snippets/bbi-footer.liquid` → empty (no changes)
- **Only theme 186373570873 touched:** push was made via Admin API with explicit `THEME_ID = '186373570873'`; theme 186495992121 was not touched
- **Content/layout unchanged:** only CSS removed; no HTML, Liquid logic, schema, or copy was modified
