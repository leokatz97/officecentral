# Stage 3.1c.1 — Spec Extract: Hero Stats Line + Sub-cat Pill Counts

**Generated:** 2026-05-07
**Source files:** `docs/strategy/design-system.md` (DS v1), `docs/strategy/bbi-component-spec-v1.md` (v1)
**Purpose:** Inform hero stats strip and filter pill count styling in `ds-cc-base.liquid`

---

## 1. Design System Coverage

Neither `design-system.md` nor `bbi-component-spec-v1.md` defines a discrete "hero stats strip" component. The component spec's §What's NOT in v1 list includes "Filter chips (taxonomy UI)" as Phase 3+ work but does not mention a stats strip at all — the strip was flagged as GAP-A in Stage 3.1a and stubbed in 3.1b as `hero_stats_line1` / `hero_stats_line2` text settings.

This spec extract infers the visual treatment from the closest analogous patterns already in the codebase.

---

## 2. Typography — Inferred Decisions

### Stat label (eyebrow)

**Reference:** `.ds-cc__brand-plates-eyebrow` (ds-cc-base.liquid line 296–301), `.ds-cc__phone-cta-label` (line 363–367), `.bbi-mono` utility class (line 89)

| Property | Value | Source |
|---|---|---|
| Font family | `"JetBrains Mono", ui-monospace, monospace` | Established eyebrow pattern throughout |
| Font size | `10px` | `.ds-cc__brand-plates-eyebrow` |
| Letter spacing | `0.08em` | Consistent across all mono eyebrows |
| Text transform | `uppercase` | Consistent across all mono eyebrows |
| Color | `rgba(var(--textColor-rgb), 0.5)` | Muted label pattern — same as brand-plates-eyebrow |
| Weight | `400` | Mono eyebrows don't use 500/600 |

### Stat numeral

**Reference:** No explicit "large numeral" component exists. Closest analogue: `ds-cc__phone-num` (line 368–372) uses `var(--headingFont), var(--fs-h2), 600`. The hero context requires a value prominent enough to read as data, but must not compete with H1.

**Inferred decision:** Use H2 mobile size (24px) with Inter Tight 600 for desktop; scale down to 20px on narrow. This sits between the brand-plates heading (H3 18/22px) and the phone number (H2 24/32px). Kept below H2 desktop (32px) to avoid competing with the page H1.

| Property | Value | Rationale |
|---|---|---|
| Font family | `var(--headingFont)` ("Inter Tight") | Heading font for all numerals |
| Font size | `22px` (mobile) / `26px` (desktop ≥768px) | Below H2 mobile (24px → rounded down) so 5 items fit in 560px column |
| Font weight | `600` | Matches heading weight throughout |
| Line height | `1.1` | Tight, matching heading scale |
| Letter spacing | `−0.01em` | Matches H2 LS from type scale |
| Color | `var(--headingColor)` | Full charcoal — data needs full contrast |

---

## 3. Layout — Inferred Decisions

**Structure:** `<dl>` element (semantic definition list — label/value pairs).
Each stat: `<div class="ds-cc__hero-stats__item">` containing `<dt>` (label) + `<dd>` (numeral).

**Reference:** The existing `.ds-cc__hero-cta-row` uses `display: flex; gap: var(--space-3); flex-wrap: wrap`. The stats strip mirrors this pattern at wider gap.

| Property | Value | Rationale |
|---|---|---|
| Display | `flex` | 5 inline columns |
| Flex-wrap | `wrap` | Graceful responsive fallback |
| Gap | `var(--space-6)` (24px) horizontal, `var(--space-4)` (16px) vertical | Consistent with DS spacing scale |
| Margin-bottom | `var(--space-6)` | Separates from CTA row |
| Item flex | `0 0 auto` | Don't stretch; natural content width |

**Responsive:** 5 items at ~88px each + 4 gaps of 24px = ~536px — fits comfortably in 560px hero column. On mobile (≤479px): 2–3 per row is natural via flex-wrap; no explicit breakpoint override needed.

---

## 4. Color & Accent

No red accent on the stats strip. The red eyebrow tick (used on `.ds-cc__brand-plates-eyebrow::before`) is NOT applied here — the stat strip is a utility readout, not a section heading. Colors: labels muted at 50% opacity, numerals full charcoal.

**Separator:** No explicit dividers between stat items. Visual rhythm comes from the 5-column layout and the label/numeral stacking. The T3 mock's `·` separators are rendered by the inline flex gap rather than markup characters.

---

## 5. Sub-cat Pill Count Styling

**Reference:** `.ds-cc__filter-chip` (line 178–186) — `13px / 500 / var(--textColor)`. Count badge is subordinate to the label.

**Inferred decision:** Inline `<span>` with JetBrains Mono 11px, muted at 55% opacity, left margin `var(--space-1)` (4px). No parentheses or bracket wrapper — number reads inline beside the pill label, slightly smaller.

| Property | Value |
|---|---|
| Font family | `"JetBrains Mono", ui-monospace, monospace` |
| Font size | `11px` |
| Letter spacing | `0.04em` |
| Color | `rgba(var(--textColor-rgb), 0.55)` |
| Margin-left | `var(--space-1)` (4px) |

---

## 6. Inferred Decision Log (for traceability)

| Decision | Inferred from | Alternative considered | Why rejected |
|---|---|---|---|
| Numeral size 22/26px | H2 mobile (24px) as ceiling; must fit 5 in 560px | H2 full (32px desktop) | Would dominate hero; 5 × 32px numerals crowds the column |
| No red eyebrow tick on stat strip | Tick used only on section headings in the pattern | Adding red tick | Section-heading tick signals "new section"; stats strip is inline in the hero block |
| `<dl>` element | Semantic accuracy — label/value pairs | `<ul>` with `<span>` children | `<dl>` is semantically correct for key-value stats |
| Inline count badge (no parens) | Filter pill UX — count is supplementary | `(120)` with parens, or separate badge | Parens add visual clutter; raw number inline is cleaner at small scale |
