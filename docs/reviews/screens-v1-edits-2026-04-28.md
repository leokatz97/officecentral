# BBI Screens v1 — Review & Edits

**Date:** 2026-04-28
**Source:** `3 - Screens.zip` (Phase 3, round 1) from Claude Design
**Reviewed against:** `docs/strategy/bbi-component-spec-v1.md` · `data/design-photos/components-v1-2026-04-27/tokens.css`
**Patched local copy:** `data/design-photos/screens-v1-2026-04-28/`

---

## Summary

Phase 3 round 1 ships only the homepage (desktop 1440 + mobile 375) plus an automated audits panel. Five remaining screens (collection.category, collection, landing, PDP unbuyable, and any post-quote pages) are referenced in the cross-link audit but not delivered — clarify scope with Claude Design before approving round 2.

The homepage itself is structurally on-spec (canonical 5 sectors, OECM copy verbatim, Phase-2 components composed correctly, AAA contrast on most pairs). Three correctness issues block approval, and one positioning edit follows from Steve's "private companies, two buyer paths" pivot.

---

## Pass / Fail by Gate

| Gate | Status | Notes |
|---|---|---|
| Tokens consumed correctly | FAIL | `--warningBackground` missing; ~25 hardcoded hexes in footer + CTA section |
| All 5 canonical sectors present | PASS | Office & Corporate · Healthcare · Education · Government · Industrial |
| OECM copy verbatim | PASS | "OECM vendor of record" appears on header CTA target, OECM bar, and audit |
| Components reused from v1 | PASS | No invented components; all surfaces compose `.bbi-btn`, `.bbi-badge`, `.bbi-card`, `.bbi-section-head`, footer |
| A11y baseline | PASS | Semantic landmarks, focus-visible token rule, `aria-label` on logo + hamburger, `alt` on logo |
| Responsive structure | PASS | 1440 + 375 share the same component tree with a `mobile` flag |
| RFQ button readable at rest | **FAIL** | Header CTA renders charcoal-on-charcoal until hover (cascade bug) |
| Audit reflects rendered cascade | **FAIL** | Contrast row claims white-on-charcoal; actual cascade gives charcoal-on-charcoal |
| Hero copy matches locked stack | **FAIL** | Round 1 still uses old "Spec it, quote it, install it" line |
| Positioning aligned with private-co pivot | **FAIL** | Industries section still leads with "Built for institutional procurement" |

---

## Edits Required

### 1. Hero copy — replace with locked stack

**File:** `Homepage.jsx`, lines 101–106 (Hero component).

**Replace with:**

```jsx
<h1 className="hp-hero__title">
  Buy by the chair, or by the office.
</h1>
<p className="hp-hero__deck">
  One Ontario team for whatever you need.
</p>
<p className="hp-hero__sub">
  Shop online for workstations, seating, and storage — or bring us your space and we'll plan, quote, and install the full fit-out.
</p>
```

The new stack signals BBI's two buyer types simultaneously — transactional (catalogue) and project (quote + install). The existing CTA pair ("Request a quote" + "Shop furniture") already maps cleanly onto those two paths and stays as-is.

**CSS:** add `.hp-hero__deck` rule to `homepage.css` between `.hp-hero__title` and `.hp-hero__sub`. Use `--headingFont`, weight 500, 22px desktop / 18px mobile, no opacity (full-strength ink). No new tokens.

**Patched locally** in `data/design-photos/screens-v1-2026-04-28/`.

---

### 2. Header "Request a quote" button — fix cascade bug

**Symptom:** Top-corner header CTA renders with charcoal text on charcoal background at rest; only becomes white-on-charcoal on hover.

**Root cause:** In `bbi-components.css` line 182, the rule

```css
.bbi-header__utility a { color: var(--headerColor); text-decoration: none; }
```

has specificity (0,1,1), which beats `.bbi-btn--primary { color: var(--buttonColor); }` at (0,1,0). The button's white text gets overridden by `--headerColor` (#0B0B0C). On hover, `.bbi-btn--primary:hover` (0,2,0) wins and restores the white.

**Fix:** scope the utility-link rule so it doesn't cross into buttons:

```css
.bbi-header__utility a:not(.bbi-btn) { color: var(--headerColor); text-decoration: none; }
```

**Patched locally.** Audits.jsx row 25 must also be updated — the contrast it currently reports (white-on-charcoal, 20.10:1 AAA) reflected the *intended* cascade, not the rendered one. Audit values must always reflect what the cascade actually produces.

---

### 3. Token discipline — add `--warningBackground`, retire hardcoded hexes

**Missing token.** `tokens.css` does not declare `--warningBackground`. The component spec records this as resolved 2026-04-27 (#E8A317 amber, ink label contrast 7.71:1 AA). Even though the homepage doesn't surface a low-stock badge, the full token set must ship with every screen so downstream templates can consume it without discovery.

Add under `:root` in the badge block:

```css
--warningBackground:     #E8A317;  /* low-stock — ink label, 7.71:1 AA */
--warningBackground-rgb: 232, 163, 23;
```

**Hardcoded hex literals** that violate "Composes ONLY tokens from tokens.css":

- `homepage.css` lines 65, 69, 70, 71, 98 — `#FFFFFF`, `#A81E22`, `rgba(11,11,12,0.92)`. Replace with token references or compose against `--saleBadgeBackground` / `--buttonColor*`.
- `bbi-components.css` footer block lines 216–312 — entire footer hardcodes inverse-scheme values. The footer should apply `.scheme-inverse` to its container and let token cascade do the work, same as the brief specifies for hero / feature blocks.
- `bbi-components.css` `.bbi-cta-section` lines 460–527 — same fix: `.scheme-inverse` on the container, not literal hexes.

Any literal that survives must carry a one-line comment justifying why no token covers it.

---

### 4. Positioning — broaden Industries section to match the dual-buyer hero

The new hero promises both transactional and project paths. The Industries section as written contradicts that promise:

- **H2** (Homepage.jsx line 274): `"Built for institutional procurement."` — too narrow.
- **Sub** (line 277): `"We've quoted and installed for school boards, hospitals, and municipal offices since 1962."` — institutional-only.

**Suggested replacements** (Steve to confirm):

- H2: `"Five sectors. One Ontario partner."` or `"Built for the way you buy."`
- Sub: `"From private offices to school boards to hospitals — we've quoted and installed across Ontario since 1962. Each sector below has its own catalogue page with sector-specific brands and warranty terms."`

Footer brand tagline (`bbi-components.css` line 238 area, content rendered from `Homepage.jsx` line 434): currently `"Commercial furniture, specced and installed. Quoting since 1962."` — consider `"Commercial furniture, sold or installed. Ontario since 1962."` to mirror the dual-path promise.

---

### 5. Optional flags

- **Hero eyebrow** (`Homepage.jsx` line 99): `"Commercial furniture · Mississauga, ON"`. If Steve wants the homepage to read as Ontario-wide rather than Mississauga-specific, swap to `"Commercial furniture · Ontario"`. Keep "Mississauga" only on Contact / About.
- **OEM badge border** uses `--borderColor` (#E5E5E7, 1.22:1) — decorative-only by token definition. If "Ships from Steelcase" needs to actually read as a labelled control, upgrade the border to `--textColor`.

---

### 6. Missing screens — confirm scope

The cross-link audit references templates 2, 3, 4, and 5 as targets but only template 1 (homepage) is in this delivery. Either:

- Phase 3 was scoped to homepage only (then approve and queue the next batch), or
- Other templates are still pending in the same Claude Design conversation (then ask for them in the same follow-up).

Recommend asking Claude Design directly which is the case before approving round 1.

---

## Files patched locally

- `data/design-photos/screens-v1-2026-04-28/Homepage.jsx` — hero copy updated
- `data/design-photos/screens-v1-2026-04-28/homepage.css` — `.hp-hero__deck` rule added
- `data/design-photos/screens-v1-2026-04-28/bbi-components.css` — RFQ button cascade fix

These local patches let Steve preview the corrected homepage while the Claude Design follow-up regenerates the canonical version.

---

## Next step

Open the follow-up prompt at `docs/reviews/claude-design-prompt-screens-v1-r2-2026-04-28.md` and paste it into the same Claude Design conversation that produced round 1.
