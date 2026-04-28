# BBI Component Spec — v1

**Phase 2 · Chat 2 of N · companion to** `Components.html`
**Tokens:** v1 (locked — see `docs/strategy/bbi-tokens-v1.md`)
**Schemes:** `.scheme-default` (charcoal-on-white) · `.scheme-inverse` (white-on-charcoal)
**Status:** seven components shipped; no new tokens introduced; flagged conflicts called out per-component.

---

## Conventions used across all components

- **BEM-style class names** prefixed `bbi-`. Modifiers use `--`, elements use `__`.
- **Five-state pattern** wherever a button or interactive surface exists: `default · hover · focus · active · disabled`. States can be forced for spec rendering with `data-state="…"`. The grayscale + 0.4 opacity disabled treatment is global.
- **Red discipline.** Brand red (`#D4252A` via `--saleBadgeBackground` and `--buttonBackground`) is reserved for: primary CTAs, the cart count dot, primary-nav hover, the maple-leaf accent, sale badges, and PDP "why-quote" eyebrow + clock icon. Never used for body links, form borders, contact-column links, or decorative dividers.
- **Scheme-aware tertiary buttons.** `.bbi-btn--tertiary` shifts hover ink to red on default scheme but stays white on inverse (red on charcoal = 2.32:1, fail).
- **Header is never rendered on inverse.** Header tokens live under `:root`, not the scheme classes.

---

## 01 — Buttons

### Variants
- `.bbi-btn--primary` — solid red, white type. Single allowed CTA per band.
- `.bbi-btn--secondary` — outlined charcoal, transparent fill. Pairs with primary; never used alone as the conversion action.
- `.bbi-btn--tertiary` — text-only with animated underline. Inline-text density.
- Sizes: `.bbi-btn--sm` (36px), default (44px), `.bbi-btn--lg` (52px).

### HTML class names
- `.bbi-btn` (base, required)
- `.bbi-btn--primary` / `--secondary` / `--tertiary`
- `.bbi-btn--sm` / `--lg`
- `.bbi-btn .arrow` (optional →/↓ icon span)
- `.bbi-btn .label` (required wrapper for tertiary so the underline pseudo-element anchors correctly)

### Tokens consumed
- Primary: `--buttonBackground`, `--buttonColor`, `--buttonBorder`, `--buttonBackgroundHover`, `--buttonColorHover`, `--buttonBorderHover`
- Secondary: `--alternateButton*` parallel set
- Tertiary: `--textColor`, `--headerHoverColor` (default scheme only)
- Focus: `--textColor` (used as outline color, scheme-aware)

### Hierarchy / sizing
- Default 44px min-height satisfies AA touch targets on mobile.
- Padding 12/20px default; scales with size modifier.
- Letter-spacing 0.02em on labels; 0.08em on tertiary underline-tracking.

### States
- `default · hover · focus · active · disabled` — implemented for all three variants in both schemes.
- Disabled is `opacity: 0.4 + grayscale(1)` on every variant, including hover-locked.
- `:focus-visible` ring is 2px outline + 2px offset, color = `--textColor`.

### Don't
- Don't pair two primaries in the same hierarchy band — the second one isn't primary, by definition.
- Don't recolor by inline style. Use scheme classes; the tokens handle inversion.
- Don't use tertiary as a fallback for "I don't know what hierarchy this is." Pick.

### Accessibility
- Touch target 44px min (AA). Large size 52px exceeds.
- Focus ring contrast 7.0:1 on default, 20.10:1 on inverse.
- Disabled state communicates via opacity AND grayscale (not color alone) — passes WCAG 1.4.1.

### Flagged
- None. Buttons are clean against tokens v1.

---

## 02 — Form Inputs

### Variants
- `.bbi-input` — single-line text input.
- `.bbi-input--textarea` — multi-line.
- `.bbi-select` — native select with custom caret.
- `.bbi-checkbox` — square 18×18, custom check via SVG mask.
- `.bbi-radio` — round 18×18, custom dot.
- `.bbi-field` — wrapper with label + helper + error slots.

### HTML class names
- `.bbi-field` (wrapper)
- `.bbi-field__label` (required for accessibility)
- `.bbi-field__helper` (subtle gray)
- `.bbi-field__error` (red — `--saleBadgeBackground`)
- `.bbi-input`, `.bbi-input--textarea`, `.bbi-select`
- `.bbi-checkbox` / `.bbi-radio` (input + custom-styled label pattern)
- States via `data-state` or native `:invalid` / `:disabled` / `:focus-visible`.

### Tokens consumed
- `--inputBg`, `--inputBorder`, `--inputBorderHover`, `--inputBorderFocus`, `--inputColor`, `--inputPlaceholder`
- `--saleBadgeBackground` (error state border + error message)
- `--cardRadius` (input corner)
- `--bodyFont`, `--space-2`, `--space-3`

### Hierarchy / sizing
- Inputs: 44px min-height, 14px font, 12/14px padding.
- Labels: 13px, 600 weight, charcoal at 100% opacity.
- Helper: 12px, charcoal at 60% opacity.
- Error: 12px, red, with leading icon glyph "!".

### States
- `default · hover · focus · active · error · disabled`. Error is the sixth state, additive.
- Focus uses `--inputBorderFocus` (charcoal) + 0 offset; AA-large via 2px border weight.

### Don't
- Don't use red borders for hover or focus. Red is reserved for error.
- Don't drop the label, even if a placeholder duplicates it. Placeholders disappear on input; labels don't.
- Don't size inputs below 44px on touch surfaces.

### Accessibility
- Every input has an associated `<label>` (or `aria-labelledby`).
- Error state communicates via icon + text + border color (three channels, not color alone).
- Focus visible on every variant including checkbox/radio (custom check has its own focus ring).

### Flagged
- Placeholder contrast: `--inputPlaceholder` = `#6B6B6E` on white = 4.55:1, just barely AA-normal at 14px. Acceptable, but flag if users enlarge text.

---

## 03 — Cards

### Variants
- `.bbi-card--product` — image + brand + title + price-or-quote-cta.
- `.bbi-card--feature` — editorial; large image, headline, kicker, body, link.
- `.bbi-card--collection` — category tile; image background with overlay heading.
- `.bbi-card--testimonial` — quote-led, no image, used in trust sections.

### HTML class names
- `.bbi-card` (base)
- `.bbi-card--product` / `--feature` / `--collection` / `--testimonial`
- `.bbi-card__media`, `.bbi-card__body`, `.bbi-card__brand`, `.bbi-card__title`, `.bbi-card__price`, `.bbi-card__cta`, `.bbi-card__overlay`
- `.bbi-badge` (often nested top-left of `__media`)

### Tokens consumed
- `--cardBg`, `--cardBorder`, `--cardRadius`, `--cardShadow` (subtle, on product cards only)
- `--textColor`, `--mutedTextColor`
- `--space-3 / --space-4 / --space-6` (rhythm)
- `--saleBadgeBackground` (sale/new badges only)

### Hierarchy / sizing
- Product cards: 4:5 image aspect, 16px body padding, 14px title.
- Feature cards: 16:9 image, 24px body padding, 20–24px headline.
- Collection tiles: 1:1 with full-bleed image and 32px overlay heading.
- Testimonial: no image; 18px quote, 14px attribution.

### States
- `default · hover` only (cards aren't focusable surfaces themselves; the inner link is). Hover lifts shadow + nudges title.
- `__cta` inherits button states.

### Don't
- Don't put two CTAs on a product card. Either it has a price (and goes to PDP via the title) or it has a "Request a quote" link — never both.
- Don't use feature-card scale for grid cards. Mixing scales kills the grid.
- Don't apply card shadow on inverse scheme. Use a 1px hairline border instead.

### Accessibility
- Wrap the entire card in a single `<a>` only when there's exactly one destination; otherwise, use the title-link + secondary-link pattern (don't nest interactives).
- Image `alt` is mandatory and describes the product, not "image of [product]".
- Hover-only affordances are not accessibility signals — every interactive in the card has a non-hover state.

### Flagged
- Card shadow on `--cardBg` works on default scheme but disappears on tinted backgrounds. Documented as a known limitation; hairline-border fallback exists.

---

## 04 — Badges

### Variants
- `.bbi-badge--sale` — solid red, white type.
- `.bbi-badge--new` — solid charcoal, white type.
- `.bbi-badge--canadian` — outlined charcoal with maple-leaf glyph.
- `.bbi-badge--low-stock` — solid amber-ish (uses `--warningBackground`); flagged.
- `.bbi-badge--oem` — outlined gray for "ships from Steelcase / Herman Miller / etc."

### HTML class names
- `.bbi-badge` (base — pill, 11px caps, 0.08em tracking)
- `.bbi-badge--sale` / `--new` / `--canadian` / `--low-stock` / `--oem`
- `.bbi-badge .leaf` (inline SVG glyph for canadian variant — fill: currentColor, color: red)

### Tokens consumed
- `--saleBadgeBackground` (sale, maple leaf)
- `--textColor` (new badge bg)
- `--warningBackground` (low-stock — flagged)
- `--borderColor` (oem outline)

### Hierarchy / sizing
- 22px tall, 8/10px horizontal padding.
- Font: heading face, 11px, 600, 0.08em letter-spacing, uppercase.
- Sit top-left of card media or inline before product title.

### States
- Static. No hover, no focus, no active. Badges are labels, not controls.

### Don't
- Don't stack more than 2 badges on a single card. If you need three, the product taxonomy is wrong.
- Don't invent new badge colors. The five variants are the set.
- Don't use sale-red for "new" — they're different signals.

### Accessibility
- Badges are descriptive text, not images. Screen readers read them in flow.
- Color contrast: red on white = 4.93:1 (AA-large pass since 11px/600 + 0.08em tracking lifts perceived weight; AA-normal would require 14px+). Charcoal on white = 18.7:1 AAA.

### Flagged
- `--warningBackground` is defined in tokens v1 but the spec didn't specify whether it's amber-yellow or BBI-red-tinted. Used `#E8A317` (amber) as a placeholder. **Confirm or replace before launch.**

---

## 05 — Header

### Variants
- `.bbi-header` — desktop, ≥768px.
- `.bbi-header--mobile` — single bar with hamburger.
- Megamenu = `.bbi-megamenu` (panel under nav item, single-column 9-category list).
- Mobile drawer = `.bbi-drawer` (uses submenu tokens).

### HTML class names
- `.bbi-header`, `.bbi-header__inner`, `.bbi-header__logo`, `.bbi-header__nav`, `.bbi-header__utility`
- `.bbi-nav-item`, `.bbi-nav-item .caret`
- `.bbi-megamenu`, `.bbi-megamenu__col`, `.bbi-megamenu__link`
- `.bbi-cart`, `.bbi-cart__count` (the only red dot)
- `.bbi-hamburger`, `.bbi-drawer`

### Tokens consumed
- `--headerBg`, `--headerColor`, `--headerHoverColor`, `--headerBorder`
- `--submenuBg`, `--submenuColor`, `--submenuHoverColor` (megamenu + mobile drawer share these — flagged)
- `--saleBadgeBackground` (cart count dot)
- `--buttonBackground` (request-a-quote CTA in utility area)

### Hierarchy / sizing
- Desktop bar 72px min-height; mobile bar 56px.
- Logo 40px tall on desktop (mix-blend-mode multiply trick — see Logo Treatment below); 32px on mobile.
- Nav items 14px, 500, 16px horizontal padding, 72px tall hit target.
- Phone number renders as charcoal click-to-call in the utility area.
- "Request a quote" is the only red CTA in the header.

### States
- Nav item: `default · hover (red ink) · focus · active · current-page (underline)`.
- Cart count: badge appears only when count > 0.

### Logo treatment (header-specific)
- Logo asset is a true-alpha PNG (`bbi-logo.png`). Sits directly on the white header.
- **No filter, no blend-mode, no plate.** Black "Brant" + red "BASICS" + black "BUSINESS INTERIORS" + red maple leaf, all as authored.

### Don't
- Don't render header on `.scheme-inverse`. Header hover red `#A81E22` on charcoal = 2.32:1, AA fail.
- Don't add a second red CTA. The "Request a quote" button is unique in this surface.
- Don't promote utility links into primary nav. Phone, sign-in, cart stay utility.

### Accessibility
- Logo `<a>` has `aria-label="Brant Business Interiors home"`.
- Megamenu opens on hover AND on focus AND on click — keyboard equivalence enforced.
- Mobile drawer traps focus when open; Esc closes.
- Cart count dot has `aria-label="X items in your quote list"`.
- Tab order: logo → primary nav → utility → cart → CTA.

### Flagged
- **Brief vs. baseline divergence.** Baseline shows nav order `Shop · Brands · Verticals · Our work · Services · About`. Brief specifies `Shop · Industries · Brands · Services · About`. **Following the brief.** Verticals→Industries, "Our work" folded into About.
- **Submenu tokens** — tokens v1 ships `--submenuBg/Color/HoverColor` as the only secondary-surface set. Mobile drawer reuses these. If a separate mobile-specific token set is needed, that's a chat-1 revision.

---

## 06 — Footer

### Variants
- One. `.bbi-footer` — always inverse, always full-bleed, never on white.

### HTML class names
- `.bbi-footer`, `.bbi-footer__inner`
- `.bbi-footer__top` (brand column + 4 nav columns)
- `.bbi-footer__brand`, `.bbi-footer__brand-plate`, `.bbi-footer__tagline`, `.bbi-footer__canadian`
- `.bbi-footer__cols`, `.bbi-footer__col`, `.bbi-footer__col--nav`, `.bbi-footer__col--contact`
- `.bbi-footer__bottom`, `.bbi-footer__legal`

### Tokens consumed
- charcoal `#0B0B0C` (canvas — matches inverse scheme)
- white `#FFFFFF` (type, contact column)
- `--saleBadgeBackground` (maple leaf, primary-nav hover, Canadian-owned accent)
- `#1F1F21` (column hairline dividers — mirrors `--borderColor` on inverse)
- `--space-8 / --space-12 / --space-16`, `--headingFont`

### Hierarchy / sizing
- 4-column grid ≥900px (Shop · Industries · Services + About · Contact); collapses to 2 columns below.
- Brand stack stacks above the columns.
- Column headings: `--headingFont`, 13px, 600, uppercase, 0.08em tracking.
- Nav links: 14px, 400, 8px vertical rhythm.
- Bottom strip: copyright left, legal links right, hairline divider above.

### Logo treatment (footer-specific)
- Same true-alpha PNG (`bbi-logo.png`) as the header.
- Sits inside a white plate (`.bbi-footer__brand-plate`) because the lockup rule says "never on dark without white plate."
- Plate: `background: #FFFFFF`, padding `16px 20px`, `border-radius: var(--cardRadius)`. Padding satisfies the clear-space rule (≥ half the height of "B" in "Brant").
- **No filter, no inversion, no recolor.** Logo ink renders as authored.
- Maple-leaf accent in the Canadian-owned line is an inline SVG with `color: #D4252A`, `fill: currentColor` — never filtered.

### States
- Footer is mostly static. Primary-nav links shift to red on hover (matches header behavior). Contact-column links underline on hover (utility, not navigation — never red).
- Legal links: 55% white at rest, 100% white on hover. Never red.

### Don't
- Don't use red on contact-column links. Red is reserved for primary-nav hover and the maple leaf.
- Don't render footer on white scheme. That's what the header is for.
- Don't drop the Canadian-owned line. It's mandatory across every page.
- Don't promote a CTA button into the footer columns. Quote-request lives in dedicated CTA blocks (07).
- Don't recolor the logo in CSS. Replace the PNG with a true-white SVG when one ships; the markup stays.

### Accessibility
- Contact links use semantic schemes: `tel:`, `mailto:`.
- White on charcoal = 20.10:1 AAA. Red hover on charcoal = 4.83:1, borderline AA-large for 14px nav links → mitigated by 500-weight bump on hover.
- Address uses real `<br>` linebreaks; SR announces as a block.
- Tab order: brand → Shop → Industries → Services → Contact → bottom legal.

### Flagged
- **Industries — 5 sectors used.** Office & Corporate · Healthcare · Education · Government · Industrial. Vertical landing pages were archived 2026-04-25, but Industries lives on as a filter taxonomy. **Confirm canonical sector list.**
- **AA-large hover ink** for 14px nav links — mitigated by 500-weight bump, but flag for the audit.

---

## 07 — Quote-request CTA

### Variants
- `(a) .bbi-cta-section` — standalone marketing band. Charcoal canvas, white heading, red CTA, OECM trust line.
- `(b) .bbi-cta-pdp` — inline PDP block. White card, red eyebrow, full-width 56px red button, "We respond within 1 business day" microcopy. Replaces add-to-cart on unbuyable items.

### HTML class names
- `.bbi-cta-section`, `.bbi-cta-section__inner`, `.bbi-cta-section__eyebrow`, `.bbi-cta-section__heading`, `.bbi-cta-section__sub`, `.bbi-cta-section__actions`, `.bbi-cta-section__trust`, `.bbi-cta-section__phone`
- `.bbi-cta-pdp`, `.bbi-cta-pdp__why`, `.bbi-cta-pdp__heading`, `.bbi-cta-pdp__why-body`, `.bbi-cta-pdp__micro`, `.bbi-cta-pdp__divider`, `.bbi-cta-pdp__alt`

### Tokens consumed
- (a) charcoal `#0B0B0C`, white `#FFFFFF`, `--buttonBackground`, `--headingFont`, `--bodyFont`, `--space-12 / --space-16`
- (b) `--bodyBg`, `--borderColor`, `--cardRadius`, `--saleBadgeBackground`, `--buttonBackground`, `--textColor`

### Hierarchy / sizing
- (a) Heading-led. Heading: `clamp(32px, 4.2vw, 56px)`, 700, -0.01em. Subhead: 17px, max-width 52ch. CTA: `.bbi-btn--lg` (52px). Section padding: `clamp(48px, 7vw, 96px)`.
- (b) Action-led. Heading: 20px, 700. Body: 14px, 78% opacity. CTA: 56px tall, full-width, 16px font, centered label. Card max-width: 460px.

### Copy rules
- (a) Heading: outcome-framed, ≤8 words. ("Get a quote, not a cart total.")
- (b) Eyebrow: always "Why request a quote?".
- (b) Heading: one sentence, ≤14 words, names the specific reason ("configurable", "freight-dependent", "quantity-priced").
- (b) Microcopy: "We respond within 1 business day" is mandatory. If you can't honor the SLA, change the copy — don't drop it.
- Button label: **"Request a quote"** on standalone (sentence case); **"Request a Quote"** on PDP (title case, action-emphasis). PDP convention is title case; the asymmetry is intentional.

### States
- Inherits five button states from `.bbi-btn--primary`. No new state work.
- Focus ring on standalone (charcoal) = white. On PDP card (white) = charcoal. Both already covered by the button component.

### Don't
- Don't pair the standalone CTA with another red element in the same band. The button is the only red.
- Don't use the PDP variant on items that are genuinely add-to-cart-able. If a SKU has a fixed price + ships standalone, give it a real cart button.
- Don't shrink the PDP button below 56px.
- Don't replace "OECM vendor of record" with a generic "trusted by businesses" line. Trust signals are specific or they're noise.
- Don't add a secondary button alongside the primary CTA. Phone fallback is a text link.
- Don't use the standalone section as a header. It's a closer.

### Accessibility
- (a) White on charcoal = 20.10:1 AAA. White-78% on charcoal = ~13.9:1 AAA.
- (b) Red eyebrow on white: `#D4252A` = 4.93:1 AA-large. Eyebrow is 12px/600 — borderline. Mitigation: 600 weight + 0.08em tracking lifts perceived weight above the AA-large threshold. Flagging.
- Phone numbers use `tel:` schemes.
- Tab order on PDP: button → phone link → project-list link.
- Standalone heading is `<h2>`. PDP heading is `<h3>` (sits inside the PDP's `<h1>` + `<h2>` outline).

### Flagged
- **OECM trust line.** Used "OECM vendor of record" as the lead trust signal. If BBI is **not** currently on the OECM (Ontario Education Collaborative Marketplace) roster, swap with another verifiable signal (since 1962, client count, contract reference). Don't ship unverifiable claims.

---

## Cross-component flagged conflicts (consolidated)

| # | Component | Flag | Resolution |
|---|---|---|---|
| 1 | 02 Form Inputs | `--inputPlaceholder` contrast 4.55:1 — barely AA-normal | Acceptable; flag if users enlarge text |
| 2 | 03 Cards | Card shadow disappears on tinted backgrounds | Hairline-border fallback exists |
| 3 | 04 Badges | `--warningBackground` not specified in tokens v1; used `#E8A317` placeholder | **Confirm or replace before launch** |
| 4 | 05 Header | Brief vs. baseline nav-order divergence | Following brief: `Shop · Industries · Brands · Services · About` |
| 5 | 05 Header | Submenu tokens reused for mobile drawer | Acceptable; chat-1 revision if separate set wanted |
| 6 | 06 Footer | Industries — 5 sectors assumed (Office & Corporate · Healthcare · Education · Government · Industrial) | **Confirm canonical sector list** |
| 7 | 06 Footer | 14px nav-link AA-large hover ink borderline | Mitigated by 500-weight on hover |
| 8 | 07 CTA | OECM trust line — used as lead signal | **Confirm BBI is on OECM roster, or swap signal** |

---

## What's NOT in v1

- Modals / dialogs
- Toast / notification surfaces
- Breadcrumbs
- Pagination
- Filter chips (taxonomy UI)
- Quote-list / project-list page chrome
- PDP image gallery + spec table
- Account / sign-in surfaces

These are Phase 3+ work. Tokens v1 should already cover them; if any require new tokens, that's a chat-1 revision before the component is built.
