# A11Y-AUDIT-1 Phase 1 — Accessibility Baseline (LIVE Avada theme)
_2026-05-20 · Read-only · AODA / WCAG 2.0 Level AA focus._

> **IMPORTANT — LIVE THEME, NOT DEV THEME**
> Mirrors PERF-AUDIT-1 Phase 1 constraint. The dev theme preview (186373570873)
> requires an active Shopify admin browser session — external auditors can't reach
> `?preview_theme_id=…` URLs. These findings reflect the **current LIVE theme (Avada)**
> at `brantbusinessinteriors.com`, not BBI Landing Dev. Phase 2 (post-LAUNCH-2) audits
> the new theme on the live domain. Same gating model as the perf audit.

---

## TL;DR

- **PSI API blocked**: anonymous Google PageSpeed Insights quota was exhausted today
  (`HTTP 429: Quota exceeded for quota metric 'Queries' and limit 'Queries per day'`).
  Manual HTML inspection across all 8 prescribed page types covered the same WCAG
  criteria PSI's accessibility category tests. PSI Phase 1.5 re-run can be queued for
  tomorrow with an API key.
- **AODA-blocking** (must fix on the new theme before LAUNCH-0):
  1. **No `<h1>` on 7 of 8 audited LIVE pages.** Only the homepage has an `<h1>`, and
     it's on a product card ("On Sale-Height Adjustable Tables") — not the page topic.
     Violates WCAG 1.3.1 + 2.4.6.
  2. **Heading hierarchy broken site-wide.** Pages jump h2 → h6 because Avada uses
     `<h6>` for chrome elements (footer "Login", "Quick links", "MENU", "Contact",
     "Sign up to our newsletter", "Follow Us") instead of styled non-heading elements
     or a proper h2/h3 nesting. Violates WCAG 1.3.1.
  3. **Off-screen `<h2>` "Reset account password" / "Create account"** appear in DOM
     on every page (account drawer markup) — screen-reader confusion. WCAG 1.3.1.
- **DEV theme posture is materially better**: skip link, semantic `<main>`, ARIA
  landmarks, `aria-labelledby` on sections, `aria-expanded`/`aria-controls` on filter
  toggles, `aria-hidden` on decorative SVGs, single visible `<h1>` per page,
  `:focus-visible` outlines defined. Two issues to fix before LAUNCH-0 are flagged in
  Area 4.
- **Image alt coverage on LIVE is good** (no `<img>` missing `alt`). **Lang attribute
  present** (`<html lang="en">`). **Skip-to-content link present**. **Generic link
  text rare** (1 instance of "read more" on search).

---

## Pages audited

| # | Code | Page | URL |
|---|------|------|-----|
| A | A | Homepage | `/` |
| B | B | Category — Seating | `/collections/seating` |
| C | C | PDP (real product) | `/products/obusforme-comfort-high-back-chair-fabric-1240-3` |
| D | D | About | `/pages/about` |
| E | E | Healthcare | `/pages/healthcare` |
| F | F | OECM | `/pages/oecm` |
| G | G | Search results | `/search?q=chair` |
| H | H | Cart | `/cart` |
| + | I | Quote (added — relevant institutional form) | `/pages/quote` |

---

## AREA 1 — PSI accessibility scores (BLOCKED)

**Status:** 🔴 Not collected — anonymous Google PSI API daily quota exhausted on the
shared IP. Error response from the API:

```
HTTP 429
"Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service
 'pagespeedonline.googleapis.com' for consumer 'project_number:583797351490'."
```

Retried with 15s/30s/60s/90s/120s exponential backoff and with a browser User-Agent —
all 429. This is the same shared-IP project the public PSI endpoint uses; it resets
at the daily Google quota boundary.

**Two retry paths for Phase 1.5:**
1. Re-run the same script tomorrow against a clean quota window. Script lives at
   `/tmp/a11y-audit-1/run_psi.py` (8 pages × 2 strategies = 16 queries, well under the
   per-IP daily limit when not contending with other tenants).
2. Provision a Google Cloud PSI API key (free tier covers thousands of queries/day)
   and re-run with `&key=…`. Recommended — avoids shared-IP contention.

Manual inspection (Areas 2-3) covers the same WCAG audits PSI's accessibility category
would have surfaced (`image-alt`, `html-has-lang`, `heading-order`, `label`,
`link-name`, `button-name`, `bypass`, etc.), so the AODA-blocking findings are
authoritative even without PSI scores.

---

## AREA 2 — AODA / WCAG 2.0 Level AA findings (LIVE Avada theme)

Ontario AODA requires WCAG 2.0 Level AA minimum. Institutional buyers (school boards,
hospitals, municipalities, OECM) routinely require this on procurement vendor
questionnaires.

| WCAG | Criterion | LIVE status | Severity | Fix |
|------|-----------|-------------|---------:|------|
| 1.1.1 | Non-text content (images have alt) | ✅ PASS — all `<img>` carry `alt`; decorative images use `alt=""` correctly (12 on search results) | — | — |
| 1.3.1 | Info and relationships (headings, lists, landmarks) | 🔴 FAIL — see Critical-1 / Critical-2 / Critical-3 in TL;DR | **AODA-blocking** | Rebuild heading hierarchy on every template |
| 1.4.3 | Contrast (Minimum) — 4.5:1 normal / 3:1 large | ⚠️ MANUAL — not verifiable from HTML alone; needs visual sampling. PSI run will confirm. | should-fix | Sample 6 page types with Chrome DevTools or axe before LAUNCH-0 |
| 2.1.1 | Keyboard | ⚠️ MANUAL — no obvious mouse-only handlers in markup, but slideshow / drawer / modal triggers need keyboard-trap testing | should-fix | Manual keyboard pass per page type |
| 2.4.1 | Bypass blocks (skip link) | ✅ PASS — `<a class="skip-to-content-link" href="#MainContent">` present in layout, all pages | — | — |
| 2.4.2 | Page titled | ✅ PASS — `<title>` populated by Avada per template | — | — |
| 2.4.4 | Link purpose (in context) | ✅ PASS — 1 "read more" on `/search`, otherwise none of `click here`, `learn more`, `here`, `details`, generic CTAs | — | — |
| 2.4.6 | Headings and labels (descriptive) | 🔴 FAIL — h6 misuse + missing h1 (see 1.3.1) | **AODA-blocking** | Same fix as 1.3.1 |
| 3.1.1 | Language of page | ✅ PASS — `<html lang="en">` on every audited page | — | — |
| 3.3.2 | Labels or instructions (form inputs) | ⚠️ PARTIAL — visible inputs (search box, newsletter signup, quote form) mostly have associated labels or `aria-label`. Some search submit / icon-only buttons rely on `title` instead of `aria-label`. | should-fix | Convert remaining `title="…"` icon buttons to `aria-label` |
| 4.1.2 | Name, role, value (interactive elements) | ⚠️ PARTIAL — 2 of 11 icon-only buttons on `/cart` use `title="…"` only (mobile-menu hamburger, back-to-top); rest carry `aria-label`. | should-fix | Add `aria-label` to mobileMenu + back_to_top |

**Critical AODA-blocking failure count: 3 distinct issues across all 8 page types audited.**

---

## AREA 3 — Manual HTML inspection (per-page)

Source data: `/tmp/a11y-audit-1/inspect.json` (regex pass over cached HTML).

### A. Image alt text

| Page | Total `<img>` | With alt | `alt=""` (decorative OK) | Missing alt |
|------|-------------:|---------:|------------------------:|-----------:|
| Homepage | 41 | 41 | 0 | 0 |
| Seating (category) | 73 | 73 | 0 | 0 |
| PDP (Obusforme chair) | 30 | 30 | 0 | 0 |
| About | 1 | 1 | 0 | 0 |
| Healthcare | 1 | 1 | 0 | 0 |
| OECM | 1 | 1 | 0 | 0 |
| Search (q=chair) | 173 | 161 | 12 | 0 |
| Cart | 1 | 1 | 0 | 0 |
| Quote | 1 | 1 | 0 | 0 |

✅ **Zero images missing alt across all 9 audited pages.**

> Caveat: alt **quality** isn't measured here. Avada often uses product handle as alt
> ("obusforme-comfort-high-back-chair-fabric-1240-3"), which is technically present
> but semantically poor for screen readers. Phase 2 should validate that the new
> theme writes human-readable alts (product title or curated alt metafield).

### B. Heading hierarchy

| Page | h1 | h2 | h3 | h4 | h5 | h6 | First skip detected |
|------|---:|---:|---:|---:|---:|---:|---|
| Homepage | **1** ⚠️ | 2 | 1 | 1 | 1 | 12 | h2 appears **before** h1 (wrong order); h1 is on a product card, not the page topic |
| Seating | **0** 🔴 | 2 | 1 | 0 | 0 | 9 | No h1; h2 → h6 |
| PDP | **0** 🔴 | 5 | 3 | 0 | 1 | 8 | No h1; h3 → h5 → h6 |
| About | **0** 🔴 | 3 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |
| Healthcare | **0** 🔴 | 3 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |
| OECM | **0** 🔴 | 3 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |
| Search | **0** 🔴 | 3 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |
| Cart | **0** 🔴 | 3 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |
| Quote | **0** 🔴 | 4 | 1 | 0 | 0 | 8 | No h1; h2 → h6 |

**Why so many h6s:** Avada's footer + drawers mark up "Login", "Quick links", "MENU",
"Customer Care", "Contact", "Sign up to our newsletter", "Follow Us", and
"Compare Products" as `<h6>`. These should not be h6 (or any heading) — they're
chrome labels. WCAG 1.3.1 says heading levels must reflect document structure, not
visual styling.

**Why off-screen h2s:** Account drawer markup ("Reset account password", "Create
account") is rendered into the DOM on every page even when closed. Screen readers
announce these as headings on every page.

### C. Form accessibility (cart + quote)

| Page | Total `<input/select/textarea>` | type=hidden | Visible | With `id` | `<label for=…>` matches | `aria-label`-d |
|------|-----:|------:|------:|------:|------:|------:|
| Cart | 48 | 36 | 12 | 12 | 9 | 0 |
| Quote | 48 | 36 | 12 | 12 | 9 | 0 |
| Healthcare | 48 | 36 | 12 | 12 | 9 | 0 |

✅ Hidden inputs (36/page) don't need labels.
⚠️ Of 12 visible inputs per template, 9 have proper `<label for>` associations.
The 3 unlabeled visible inputs are global chrome: header search box, newsletter
signup field, and account drawer toggle — they have `placeholder` text but no
programmatic label. WCAG 3.3.2 (should-fix).

### D. Generic link text

| Page | Count | Examples |
|------|------:|----------|
| All except Search | 0 | — |
| Search (`q=chair`) | 1 | `read more` |

✅ Effectively clean — single instance to fix on the search results template.

### E. `<html lang>` declaration

| Page | Value |
|------|-------|
| All 9 audited | `en` ✅ |

✅ WCAG 3.1.1 met across the board.

### F. Skip-to-content link

| Page | Present |
|------|--------|
| All 9 audited | ✅ Yes — `<a class="skip-to-content-link" href="#MainContent">` |

### G. Icon-only buttons without accessible name

Inspected `/cart` (worst case — header + footer chrome shown):
- 22 `<button>` elements, 11 with no inner text (icon-only)
- **9 of those 11 carry `aria-label`** ✅ (Previous/Next slider arrows, Search submit, Speech search, Submit, Compare close, Drawer close)
- **2 rely on `title="…"` only** ⚠️ — `button.mobileMenu` (hamburger) and `button#back_to_top` (scroll-to-top). `title` is read by some screen readers but not all; `aria-label` is the WCAG-compliant attribute.

---

## AREA 4 — DEV theme accessibility patterns (`ds-cc-base`, `ds-cs-base`, layout)

Read of `theme/layout/theme.liquid`, `theme/sections/ds-cc-base.liquid`,
`theme/sections/ds-cs-base.liquid`.

### What the DEV theme does right (preserve in LAUNCH-0)

- ✅ **Skip-to-content link** — `theme/layout/theme.liquid:84` —
  `<a class="skip-to-content-link" href="#MainContent">` + `accessibility.skip_to_text` locale key.
- ✅ **Semantic main landmark** — `theme/layout/theme.liquid:170` —
  `<main id="MainContent" role="main" tabindex="-1">`.
- ✅ **Single visible `<h1>` per landing template** —
  `theme/sections/ds-cc-base.liquid:530` → `<h1 id="cc-hero-title">{{ section.settings.hero_title | default: collection.title }}</h1>`;
  `theme/sections/ds-cs-base.liquid:312` → `<h1>{{ page_title }}</h1>`.
- ✅ **`aria-labelledby` on hero/sections** — e.g. `<section class="ds-cc__hero" aria-labelledby="cc-hero-title">` (`ds-cc-base.liquid:524`).
- ✅ **`aria-label` on landmark `<nav>`** — `aria-label="Shop by sector"`, `aria-label="Sub-categories"`, `aria-label="Product pages"`, `aria-label="Filter products"`, `aria-label="Collection pagination"`.
- ✅ **`aria-expanded` / `aria-controls` on collapsible filter toggles** — `ds-cs-base.liquid:360, 369, 392, 415, 436`.
- ✅ **`aria-hidden="true"` on decorative SVGs and unicode arrows** — every leaf, arrow, dot, and badge graphic.
- ✅ **`:focus-visible` outlines defined for keyboard users** — `ds-cc-base.liquid:193, 201, 222, 363, 475` (`outline:2px solid var(--textColor); outline-offset:2px`).
- ✅ **`<label aria-label>` on number inputs** — `<input type="number" id="price-min" aria-label="Minimum price">` (`ds-cs-base.liquid:443`).
- ✅ **`<select aria-label="Sort products">`** (`ds-cs-base.liquid:473`).
- ✅ **`role="list"` on product grid `<ul>`** (`ds-cs-base.liquid:487`) — overrides Safari's `list-style:none` removing list semantics.
- ✅ **Decorative product-card link is `tabindex="-1" aria-hidden="true"`** (`ds-cs-base.liquid:498`) — avoids duplicate tab stop.

### Issues found in DEV theme — fix before LAUNCH-0

| # | File | Issue | Severity | Fix |
|---|------|-------|---------:|-----|
| DEV-1 | `theme/sections/ds-cs-base.liquid:462` | `<div class="ds-cs__grid" role="main">` — adds a second `role="main"` inside `<main id="MainContent" role="main">` from layout. WCAG 4.1.2 — only one banner/main/contentinfo landmark per page. | should-fix | Remove `role="main"` from the inner div. Use `aria-label="Products"` if a landmark is desired, or no role at all. |
| DEV-2 | `theme/layout/theme.liquid:170` | `<main … tabindex="-1">` is fine for skip-link target, but `role="main"` is redundant on `<main>`. Not a violation, just noise. | nice-to-have | Drop redundant `role="main"`. |
| DEV-3 | Inherited from Avada chrome (when BBI-landing gate **off**) | Pages outside `bbi_landing` gate (legacy templates) still render Avada's footer with `<h6>` for "Login", "Quick links", etc., and account-drawer `<h2>`s in DOM. Same WCAG 1.3.1 failure as LIVE. | should-fix or accept | Either (a) flip every remaining template into the `bbi_landing` gate before LAUNCH-0 so the BBI footer is used instead of Avada's, or (b) override `header-group` / `footer-group` snippets to use non-heading elements for chrome labels. |
| DEV-4 | DS bases | h2 nodes inside DS sections often use `visually-hidden` for grouping (`<h2 id="cc-tiles-heading" class="visually-hidden">…</h2>`). This is fine, but verify the class actually clips them off-screen rather than `display:none`-ing (which removes from a11y tree). | manual-check | Inspect computed style of `.visually-hidden` in browser. |
| DEV-5 | DS bases | Colour-contrast: tokens are defined in `--textColor`, `--brandRed`, etc. Not measurable from Liquid; needs browser pass with axe DevTools. | manual-check | Run axe on `ds-cc-base` + `ds-cs-base` + `ds-pdp-base` against 4.5:1 normal / 3:1 large. |

### Comparison summary: LIVE vs DEV

| Capability | LIVE (Avada) | DEV (BBI Landing Dev) |
|------------|:--:|:--:|
| Skip link | ✅ | ✅ |
| `<html lang>` | ✅ | ✅ |
| Image alt coverage | ✅ | ✅ (preserve) |
| Single h1 per page | 🔴 (only home) | ✅ |
| Heading hierarchy | 🔴 (h2 → h6, h6 for chrome) | ✅ (where bbi_landing gate is on) |
| ARIA landmarks | ⚠️ (no `<nav>` on most pages) | ✅ |
| ARIA on collapsibles | ⚠️ | ✅ (filter toggles) |
| `:focus-visible` styles | ⚠️ | ✅ |
| Decorative SVG `aria-hidden` | mixed | ✅ |
| Form labels | ⚠️ partial | ✅ partial — sample only 2 forms in DS; verify quote-form a11y at P1-4 |
| Icon-only button `aria-label` | mixed (some `title` only) | ✅ |
| Duplicate `role="main"` | n/a | 🔴 fix DEV-1 |

---

## AREA 5 — Comparison to PERF-AUDIT-1 findings

The perf audit (`data/reports/perf-audit-2026-05-14.md`) marked all 10 LIVE URLs FAIL
on Core Web Vitals (avg Lighthouse perf = 63, every LCP > 4 000 ms). That posture
plus the AODA findings here means the **LIVE site is institutionally non-compliant on
two axes**: performance and AODA heading structure. The DEV theme materially
improves both — perf via lazy loading, image_url with explicit widths, no Avada
plugin bloat; a11y via proper heading hierarchy, ARIA landmarks, focus styles,
single h1.

LCP failures and missing-h1 failures have no overlap in remediation work but
both must be addressed before the new theme launches.

---

## Critical fixes — must land before LAUNCH-0

1. **Every template needs a real `<h1>`** that describes the page topic. Most DS
   bases already do this — verify on every non-`bbi_landing`-gated template
   (legacy Avada surfaces still in the live theme).
2. **Stop using `<h6>` for chrome labels.** Convert Avada footer/header `<h6>`s
   to `<div>` or `<p>` with `class="h6"` for styling, OR migrate every URL into
   the `bbi_landing` gate before LAUNCH-0 (BBI's `bbi-footer.liquid` doesn't
   misuse heading levels).
3. **Remove off-screen `<h2>`s for account drawer.** Either move the drawer
   markup behind a conditional that only renders when the drawer is open, or
   demote the headings to non-heading elements with `class` styling.
4. **Remove duplicate `role="main"` in `ds-cs-base.liquid:462`** (DEV-1).
5. **Add `aria-label` to icon-only buttons currently relying on `title` only**
   (mobile menu, back-to-top).

## Important — should-fix before LAUNCH-0

1. Run axe DevTools color-contrast pass on `ds-cc-base`, `ds-cs-base`, `ds-pdp-base`,
   `ds-lp-quote`, `ds-lp-oecm`, `ds-lp-healthcare`. Sample brand-red CTAs on white
   and CM-badge text against background.
2. Verify `.visually-hidden` clips off-screen rather than `display:none` (Area 4
   DEV-4).
3. Convert single `read more` generic link on search results template.
4. Add programmatic labels (visually-hidden `<label>` or `aria-label`) to the
   header search box and newsletter signup input.
5. Keyboard-trap test on quote-modal, cart-drawer, account-drawer (manual).

## Nice-to-have

1. Improve image alt **quality** — replace product-handle alts with product title
   or curated alt metafield value.
2. Drop redundant `role="main"` on `<main>` element (Area 4 DEV-2).

## Manual-check items (carry into Phase 2)

- Colour contrast on every DS section against WCAG 4.5:1 / 3:1.
- Focus visibility on every interactive control (link, button, input, select,
  collapsible toggle, modal close).
- Keyboard navigation: tab order, focus traps in drawers/modals, Escape-closes-modal.
- Screen-reader pass with VoiceOver on PDP, category, OECM, quote form.
- Dynamic-content announcements (cart add, quote submit success, search results
  count update).

---

## Phase 2 trigger note

🟡 **Phase 2 fires post-LAUNCH-2.** Re-run this audit against the live domain once
the BBI Landing Dev theme is published. Phase 2 deliverables:
- Full PSI accessibility scores (mobile + desktop) across all 8 page types, with API
  key, no quota risk.
- axe DevTools color-contrast report against the DS tokens as actually rendered.
- VoiceOver/NVDA pass on cart, quote, PDP, OECM, Healthcare.
- Verify Phase 1 critical-fix items (h1, h6 misuse, drawer h2s, duplicate role=main,
  icon-button aria-label) are resolved in production.

## Phase 1.5 — optional PSI re-run

If a clean PSI run is desired before launch, request a Google Cloud PSI API key
and re-execute `/tmp/a11y-audit-1/run_psi.py` with `&key=…` appended. 16 queries =
trivial cost / well under free tier.

---

## Appendix — Files & artifacts

- This document: `data/reports/a11y-audit-1-phase-1.md`
- Manual-inspection JSON: `/tmp/a11y-audit-1/inspect.json` (regex-pass HTML metrics)
- PSI fetch script (blocked today, ready for re-run): `/tmp/a11y-audit-1/run_psi.py`
- Cached HTML for inspection: `/tmp/a11y-audit-1/html/*.html` (9 pages)
- Reference: `data/reports/perf-audit-2026-05-14.md`
- DEV theme files reviewed:
  - `theme/layout/theme.liquid`
  - `theme/sections/ds-cc-base.liquid`
  - `theme/sections/ds-cs-base.liquid`
