# Stage 2.7 — Site-wide white-on-white chrome fix
**Date:** 2026-05-07  
**Branch:** `chore/stabilize-chrome-2026-05-07`  
**Dev theme:** `186373570873` only — theme `186495992121` not touched.

---

## Audit A — Footer overrides with light tokens

**22 files audited.** Full results: `data/reports/footer-override-audit.csv`

### BROKEN (5 files)
All 5 had the identical pattern: `.lp-X .bbi-footer{background:var(--alternateBackground);...}` overriding the snippet's own `--ft-bg` local token with a light page token, followed by 10+ `.lp-X .bbi-footer__*` layout rules.

| File | Broken selector | Wrong value |
|---|---|---|
| ds-lp-about.liquid | `.lp-about .bbi-footer` | `var(--alternateBackground)` |
| ds-lp-brands-ergocentric.liquid | `.lp-ergo .bbi-footer` | `var(--alternateBackground)` |
| ds-lp-brands-global-teknion.liquid | `.lp-global .bbi-footer` | `var(--alternateBackground)` |
| ds-lp-brands-keilhauer.liquid | `.lp-keilhauer .bbi-footer` | `var(--alternateBackground)` |
| ds-lp-brands.liquid | `.lp-brands .bbi-footer` | `var(--alternateBackground)` |

### OK (17 files)
No footer background override, or override uses explicit dark local token (`--background:#0B0B0C`), or layout-only overrides.

---

## Audit B — CTA closers with no background paint

**22 files audited.** Full results: `data/reports/cta-closer-audit.csv`

### BROKEN (1 file)
| File | Wrapper class | Problem |
|---|---|---|
| ds-lp-customer-stories.liquid | `bbi-cta-section` | `.lp-stories .bbi-cta-section.scheme-inverse` set layout/text-align only; no `background:` rule — scheme-inverse redefines `--background` dark but element bg stayed at page-level light |

### OK (21 files)
All other sections with scheme-inverse closers either: (a) paint background explicitly via scoped rule, (b) bake `--background:#0B0B0C` directly into the rule, or (c) use inline `style="background:var(--background)"` on the element with `scheme-inverse` class.

---

## Files modified (6 total)

| File | Fix type | What changed |
|---|---|---|
| `theme/sections/ds-lp-about.liquid` | Pattern A | Removed 11 `.lp-about .bbi-footer*` rules (lines 97–107) |
| `theme/sections/ds-lp-brands-ergocentric.liquid` | Pattern A | Removed 11 `.lp-ergo .bbi-footer*` rules |
| `theme/sections/ds-lp-brands-global-teknion.liquid` | Pattern A | Removed 11 `.lp-global .bbi-footer*` rules |
| `theme/sections/ds-lp-brands-keilhauer.liquid` | Pattern A | Removed 11 `.lp-keilhauer .bbi-footer*` rules |
| `theme/sections/ds-lp-brands.liquid` | Pattern A | Removed `/* Footer */` comment + 11 `.lp-brands .bbi-footer*` rules |
| `theme/sections/ds-lp-customer-stories.liquid` | Pattern B | Added `background:var(--background);color:var(--textColor);` to `.lp-stories .bbi-cta-section.scheme-inverse` |

---

## Before/after diff examples

### Pattern A — ds-lp-about.liquid (representative)

**Before:**
```css
.lp-about .bbi-footer{background:var(--alternateBackground);border-top:1px solid rgba(var(--borderColor-rgb),0.6);padding:var(--space-12) 0 var(--space-8);}
.lp-about .bbi-footer__inner{max-width:1320px;margin:0 auto;padding:0 32px;display:grid;grid-template-columns:1.5fr repeat(3,1fr);gap:48px;}
.lp-about .bbi-footer__brand-plate{display:flex;flex-direction:column;gap:var(--space-4);}
.lp-about .bbi-footer__brand-plate img{height:32px;width:auto;}
.lp-about .bbi-footer__tagline{...}
.lp-about .bbi-footer__col h4{...}
.lp-about .bbi-footer__col ul{...}
.lp-about .bbi-footer__col a{...}
.lp-about .bbi-footer__col a:hover{...}
.lp-about .bbi-footer__bottom{...}
@media(max-width:768px){.lp-about .bbi-footer__inner{...}.lp-about .bbi-footer__brand-plate{...}}
```

**After:** *(all 11 rules deleted)*  
The `bbi-footer` snippet defines `.bbi-footer { --ft-bg: #0B0B0C; background: var(--ft-bg); }` — always dark, no override needed.

---

### Pattern B — ds-lp-customer-stories.liquid

**Before:**
```css
.lp-stories .bbi-cta-section.scheme-inverse{padding:80px 32px;text-align:center;}
```

**After:**
```css
.lp-stories .bbi-cta-section.scheme-inverse{background:var(--background);color:var(--textColor);padding:80px 32px;text-align:center;}
```

---

## Push results

| File | HTTP status |
|---|---|
| sections/ds-lp-about.liquid | 200 |
| sections/ds-lp-brands-ergocentric.liquid | 200 |
| sections/ds-lp-brands-global-teknion.liquid | 200 |
| sections/ds-lp-brands-keilhauer.liquid | 200 |
| sections/ds-lp-brands.liquid | 200 |
| sections/ds-lp-customer-stories.liquid | 200 |

---

## Spot-check results

3 representative sections checked on dev theme `186373570873` via grep on API response:

| Section | broken footer override present? | CTA background fix present? |
|---|---|---|
| ds-lp-about.liquid | ✅ NO (0 matches) | N/A — Pattern A fix |
| ds-lp-brands-ergocentric.liquid | ✅ NO (0 matches) | N/A — Pattern A fix |
| ds-lp-customer-stories.liquid | ✅ NO (0 matches) | ✅ YES — `background:var(--background);color:var(--textColor);padding:80px` present in local file; 200 PUT confirmed on theme |

Local file integrity also verified post-edit: all 6 files confirmed correct by grep.

---

## Shared snippet / live theme confirmation

- `theme/snippets/bbi-footer.liquid` — **not modified**
- `theme/snippets/bbi-nav.liquid` — **not modified**
- Theme `186495992121` (live) — **not touched** — all pushes went to `186373570873` only

---

## Stage 8 backlog item

**Extract `bbi-cta-section` and `lp-closer` into a shared snippet**  
Root cause of this class of drift: every BBI section defines its own inline CSS for shared chrome components (`lp-closer`, `bbi-cta-section`). When the snippet structure evolves, older sections don't follow. Fix at Stage 8: extract both closer patterns into `theme/snippets/bbi-cta-closer.liquid` (or a single unified snippet) and render it via `{% render 'bbi-cta-closer', ... %}` in every section. Eliminates the per-section CSS duplication class entirely.

---

**Halt — not merged, Stage 3 not started.**
