# BBI Component Spec — v1

**Phase 2 · Chat 2 of N**
**Tokens:** v1 (locked — see `docs/strategy/bbi-tokens-v1.md`)
**Schemes:** `.scheme-default` (charcoal-on-white) · `.scheme-inverse` (white-on-charcoal)
**Logo asset:** `bbi-logo-v2.png` (true-alpha PNG, 1360×400)

---

## Conventions across all components

- **BEM-style class names** prefixed `bbi-`. Modifiers `--`, elements `__`.
- **Five-state pattern** on every interactive surface: `default · hover · focus · active · disabled`. States can be forced with `data-state="…"` for spec rendering. Disabled is global: `opacity: 0.4 + grayscale(1)`, hover-locked.
- **Red discipline.** Brand red `#D4252A` (`--saleBadgeBackground` and `--buttonBackground`) is reserved for: primary CTAs, the cart count dot, primary-nav hover, the maple-leaf accent, sale badges, and the PDP "why-quote" eyebrow. Never used for body links, form borders, contact-column links, or decorative dividers.
- **Scheme-aware tertiary buttons.** `.bbi-btn--tertiary` shifts hover ink to red on default scheme but stays white on inverse (red on charcoal = 2.32:1 fail).
- **Header is never rendered on inverse.** Header tokens live under `:root`, not the scheme classes.
- **Focus-visible everywhere.** `:focus-visible` ring is 2px outline + 2px offset, color = `--textColor`.

---

## 01 — Buttons

### Variants

#### `.bbi-btn--primary` — solid red, white type. Single allowed CTA per band.
````html
<button class="bbi-btn bbi-btn--primary">Request a quote</button>
<button class="bbi-btn bbi-btn--primary bbi-btn--lg">Request a quote <span class="arrow">→</span></button>
````

#### `.bbi-btn--secondary` — outlined charcoal, transparent fill. Pairs with primary; never the conversion action alone.
````html
<button class="bbi-btn bbi-btn--secondary">Browse models</button>
````

#### `.bbi-btn--tertiary` — text-only with animated underline. Inline-text density.
````html
<button class="bbi-btn bbi-btn--tertiary"><span class="label">View details</span></button>
````

### Sizes
````html
<button class="bbi-btn bbi-btn--primary bbi-btn--sm">Add to quote</button>
<button class="bbi-btn bbi-btn--primary">Request a quote</button>
<button class="bbi-btn bbi-btn--primary bbi-btn--lg">Browse models</button>
````

### Tokens consumed
- Primary: `--buttonBackground`, `--buttonColor`, `--buttonBorder`, `--buttonBackgroundHover`, `--buttonColorHover`, `--buttonBorderHover`
- Secondary: `--alternateButton*` parallel set
- Tertiary: `--textColor`, `--headerHoverColor` (default scheme only)
- Focus: `--textColor` (outline color, scheme-aware)

### Hierarchy / Sizing
- Default 44px min-height (AA touch target); `--sm` 36px, `--lg` 52px.
- Padding 12/20px default; scales with size modifier.
- Letter-spacing 0.02em on labels; 0.08em on tertiary underline-tracking.
- The optional `.arrow` icon span sits inside the label.

### States
Five states (default · hover · focus · active · disabled) implemented for all three variants in both schemes.
Disabled: `opacity: 0.4 + grayscale(1)`, hover-locked.
Tertiary requires a `<span class="label">` wrapper for the underline pseudo-element to anchor correctly.

### Don't
- Don't pair two primaries in the same hierarchy band — the second one isn't primary, by definition.
- Don't recolor by inline style; use scheme classes.
- Don't use tertiary as a fallback for "I don't know what hierarchy this is."

### Accessibility checklist
- 44px min touch target (AA). `--lg` exceeds.
- Focus ring: 7.0:1 on default, 20.10:1 on inverse.
- Disabled communicates via opacity AND grayscale (not color alone) — passes WCAG 1.4.1.
- Label is real text, never an SVG-as-text.

### Flagged
None.

---

## 02 — Form Inputs

### Variants

#### `.bbi-input` — single-line text input.
````html
<div class="bbi-field">
  <label class="bbi-field__label" for="email">Work email</label>
  <input class="bbi-input" id="email" type="email" placeholder="you@company.com" />
  <p class="bbi-field__helper">We'll only use this for the quote.</p>
</div>
````

#### `.bbi-input--textarea` — multi-line.
````html
<div class="bbi-field">
  <label class="bbi-field__label" for="notes">Project notes</label>
  <textarea class="bbi-input bbi-input--textarea" id="notes" rows="4"></textarea>
</div>
````

#### `.bbi-select` — native select with custom caret.
````html
<div class="bbi-field">
  <label class="bbi-field__label" for="industry">Industry</label>
  <select class="bbi-select" id="industry">
    <option>Office &amp; Corporate</option>
    <option>Healthcare</option>
    <option>Education</option>
    <option>Government</option>
    <option>Industrial</option>
  </select>
</div>
````

#### `.bbi-checkbox` — square 18×18.
````html
<label class="bbi-checkbox">
  <input type="checkbox" />
  <span class="bbi-checkbox__box"></span>
  <span class="bbi-checkbox__label">Subscribe to BBI updates</span>
</label>
````

#### `.bbi-radio` — round 18×18.
````html
<label class="bbi-radio">
  <input type="radio" name="freight" value="standard" />
  <span class="bbi-radio__dot"></span>
  <span class="bbi-radio__label">Standard freight</span>
</label>
````

#### Error state
````html
<div class="bbi-field" data-state="error">
  <label class="bbi-field__label" for="qty">Quantity</label>
  <input class="bbi-input" id="qty" aria-invalid="true" />
  <p class="bbi-field__error">Please enter a number ≥ 1.</p>
</div>
````

### Tokens consumed
- `--inputBg`, `--inputBorder`, `--inputBorderHover`, `--inputBorderFocus`, `--inputColor`, `--inputPlaceholder`
- `--saleBadgeBackground` (error border + error message)
- `--cardRadius` (corner)
- `--bodyFont`, `--space-2`, `--space-3`

### Hierarchy / Sizing
- Inputs: 44px min-height, 14px font, 12/14px padding.
- Labels: 13px, 600, charcoal at 100% opacity.
- Helper: 12px, charcoal at 60%.
- Error: 12px, red, with leading "!" glyph.

### States
Six states (default · hover · focus · active · error · disabled).
Focus uses `--inputBorderFocus` (charcoal) + 2px border weight (AA-large).
Error border = `--saleBadgeBackground`; never reuse red for hover/focus.

### Don't
- Don't use red borders for hover or focus — red is reserved for error.
- Don't drop the label, even if a placeholder duplicates it.
- Don't size inputs below 44px on touch surfaces.

### Accessibility checklist
- Every input has an associated `<label>` (or `aria-labelledby`).
- Error communicates via icon + text + border (three channels, not color alone).
- `aria-invalid="true"` is set on the input itself when in error state.
- Focus visible on every variant including custom checkbox/radio.

### Flagged
Placeholder contrast: `--inputPlaceholder` #6B6B6E on white = 4.55:1, just barely AA-normal at 14px. Acceptable, but flag if users enlarge text.

---

## 03 — Cards

### Variants

#### `.bbi-card--product` — image + brand + title + price-or-quote-cta.
````html
<article class="bbi-card bbi-card--product">
  <div class="bbi-card__media">
    <img src="..." alt="Steelcase Series 1 Task Chair" />
    <span class="bbi-badge bbi-badge--sale">Sale</span>
  </div>
  <div class="bbi-card__body">
    <p class="bbi-card__brand">Steelcase</p>
    <h3 class="bbi-card__title"><a href="...">Series 1 Task Chair</a></h3>
    <p class="bbi-card__price">From $649</p>
  </div>
</article>
````

#### `.bbi-card--feature` — editorial; large image, headline, kicker, body, link.
````html
<article class="bbi-card bbi-card--feature">
  <div class="bbi-card__media">
    <img src="..." alt="Open-plan office install at ABC Corp" />
  </div>
  <div class="bbi-card__body">
    <p class="bbi-card__brand">Case study</p>
    <h2 class="bbi-card__title">220 workstations in 11 weeks for ABC Corp.</h2>
    <p>From floor plan to install. Steelcase Migration desks, AMQ task chairs, and Allsteel storage — fully specced.</p>
    <a class="bbi-btn bbi-btn--tertiary" href="..."><span class="label">Read the story</span></a>
  </div>
</article>
````

#### `.bbi-card--collection` — category tile; full-bleed image with overlay heading.
````html
<a class="bbi-card bbi-card--collection" href="...">
  <div class="bbi-card__media">
    <img src="..." alt="Task chairs" />
    <div class="bbi-card__overlay">
      <h3 class="bbi-card__title">Task chairs</h3>
    </div>
  </div>
</a>
````

#### `.bbi-card--testimonial` — quote-led, no image.
````html
<article class="bbi-card bbi-card--testimonial">
  <blockquote>
    "BBI quoted, delivered, and installed 220 workstations in 11 weeks. On budget."
  </blockquote>
  <p class="bbi-card__attribution">Maria L. — Facilities, ABC Corp</p>
</article>
````

### Tokens consumed
- `--cardBg`, `--cardBorder`, `--cardRadius`, `--cardShadow` (subtle, on product cards only)
- `--textColor`, `--mutedTextColor`
- `--space-3` / `--space-4` / `--space-6` (rhythm)
- `--saleBadgeBackground` (sale/new badges only)

### Hierarchy / Sizing
- Product: 4:5 image, 16px body padding, 14px title.
- Feature: 16:9 image, 24px body padding, 20–24px headline.
- Collection: 1:1 with full-bleed image, 32px overlay heading.
- Testimonial: no image; 18px quote, 14px attribution.

### States
`default · hover` only — cards aren't focusable surfaces themselves; the inner link is.
Hover lifts shadow + nudges title.
`__cta` inherits button states.

### Don't
- Don't put two CTAs on a product card. Either it has a price (and goes to PDP via the title) or it has a "Request a quote" link — never both.
- Don't mix feature-card scale into a product grid.
- Don't apply card shadow on inverse scheme; use a 1px hairline border instead.

### Accessibility checklist
- Wrap the entire card in a single `<a>` only when there's exactly one destination; otherwise use the title-link + secondary-link pattern (don't nest interactives).
- `alt` describes the product, not "image of [product]".
- Hover-only affordances are not accessibility signals — every interactive in the card has a non-hover state.

### Flagged
Card shadow on `--cardBg` works on default scheme but disappears on tinted backgrounds. Hairline-border fallback exists.

---

## 04 — Badges

### Variants

#### `.bbi-badge--sale` — solid red, white type.
````html
<span class="bbi-badge bbi-badge--sale">Sale</span>
````

#### `.bbi-badge--new` — solid charcoal, white type.
````html
<span class="bbi-badge bbi-badge--new">New</span>
````

#### `.bbi-badge--canadian` — outlined charcoal with maple-leaf glyph.
````html
<span class="bbi-badge bbi-badge--canadian">
  <svg class="leaf" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l1.2 4 3.4-1.2-1.2 3.4L19 10l-4 1.5 1 3-4-1.5-1 4-1-4-4 1.5 1-3-4-1.5 3.6-1.8L5.4 4.8 8.8 6 10 2z"/></svg>
  Canadian-owned
</span>
````

#### `.bbi-badge--low-stock` — solid amber.
````html
<span class="bbi-badge bbi-badge--low-stock">Low stock</span>
````

#### `.bbi-badge--oem` — outlined gray.
````html
<span class="bbi-badge bbi-badge--oem">Ships from Steelcase</span>
````

### Tokens consumed
- `--saleBadgeBackground` (sale fill, maple-leaf color)
- `--textColor` (new badge fill)
- `--warningBackground` (low-stock — flagged)
- `--borderColor` (oem outline)

### Hierarchy / Sizing
- 22px tall, 8/10px horizontal padding.
- Font: heading face, 11px, 600, 0.08em letter-spacing, uppercase.
- Position: top-left of card media or inline before product title.

### States
Static. No hover, no focus, no active. Badges are labels, not controls.

### Don't
- Don't stack more than 2 badges on a single card. If you need three, the taxonomy is wrong.
- Don't invent new badge colors. The five variants are the set.
- Don't use sale-red for "new" — they're different signals.

### Accessibility checklist
- Badges are descriptive text, not images. Screen readers read them in flow.
- Maple leaf SVG has `aria-hidden="true"`; the word "Canadian-owned" carries the meaning.
- Contrast: red on white = 4.93:1 (AA-large pass; AA-normal would require 14px+); charcoal on white = 18.7:1 AAA.

### Flagged
~~`--warningBackground` placeholder~~ **Resolved 2026-04-27.** #E8A317 (amber) approved. Token added to tokens.css with ink label contrast 7.71:1 AA.

---

## 05 — Header

### Variants

#### `.bbi-header` — desktop, ≥768px.
````html
<header class="bbi-header">
  <div class="bbi-header__inner">
    <a class="bbi-header__logo" href="/" aria-label="Brant Business Interiors home">
      <img src="bbi-logo-v2.png" alt="Brant Business Interiors" />
    </a>
    <nav class="bbi-header__nav" aria-label="Primary">
      <a class="bbi-nav-item" href="#">Shop Furniture <span class="caret"></span></a>
      <a class="bbi-nav-item" href="#">Industries</a>
      <a class="bbi-nav-item" href="#">Brands</a>
      <a class="bbi-nav-item" href="#">Services</a>
      <a class="bbi-nav-item" href="#">About</a>
    </nav>
    <div class="bbi-header__utility">
      <a href="tel:18008359565">1-800-835-9565</a>
      <a href="#">Sign in</a>
      <a class="bbi-cart" href="#" aria-label="3 items in your quote list">
        <svg>…</svg><span class="bbi-cart__count">3</span>
      </a>
      <button class="bbi-btn bbi-btn--primary">Request a quote</button>
    </div>
  </div>
</header>
````

#### `.bbi-header--mobile` — single bar with hamburger.
````html
<div class="bbi-header bbi-header--mobile">
  <div class="bbi-header__inner">
    <a class="bbi-header__logo" href="/"><img src="bbi-logo-v2.png" alt="Brant Business Interiors" /></a>
    <button class="bbi-hamburger" aria-label="Open menu" aria-expanded="false">
      <svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
</div>
````

#### `.bbi-megamenu` — single-column 9-category panel beneath nav item.
````html
<div class="bbi-megamenu" role="menu">
  <a class="bbi-megamenu__link" href="#">Seating</a>
  <a class="bbi-megamenu__link" href="#">Desks &amp; Workstations</a>
  <a class="bbi-megamenu__link" href="#">Storage &amp; Filing</a>
  <a class="bbi-megamenu__link" href="#">Tables</a>
  <a class="bbi-megamenu__link" href="#">Boardroom</a>
  <a class="bbi-megamenu__link" href="#">Ergonomic Products</a>
  <a class="bbi-megamenu__link" href="#">Panels &amp; Dividers</a>
  <a class="bbi-megamenu__link" href="#">Accessories</a>
  <a class="bbi-megamenu__link" href="#">Quiet Spaces</a>
</div>
````

### Tokens consumed
- `--headerBg`, `--headerColor`, `--headerHoverColor`, `--headerBorder`
- `--submenuBg`, `--submenuColor`, `--submenuHoverColor` (megamenu + mobile drawer share these — flagged)
- `--saleBadgeBackground` (cart count dot)
- `--buttonBackground` (request-a-quote CTA)

### Hierarchy / Sizing
- Desktop bar: 72px min-height. Mobile bar: 56px.
- Logo: 40px tall on desktop, 32px on mobile.
- Nav items: 14px, 500, 16px horizontal padding, 72px tall hit target.
- Phone number: charcoal click-to-call in utility area.
- "Request a quote" is the only red CTA in the header.

### Logo treatment
Asset is a true-alpha PNG (`bbi-logo-v2.png`). Sits directly on white. No filter, no blend-mode, no plate.

### States
Nav item: `default · hover (red ink) · focus · active · current-page (underline)`.
Cart count badge appears only when count > 0.

### Don't
- Don't render header on `.scheme-inverse` (header hover red #A81E22 on charcoal = 2.32:1 fail).
- Don't add a second red CTA. "Request a quote" is unique in this surface.
- Don't promote utility links into primary nav. Phone, sign-in, cart stay utility.

### Accessibility checklist
- Logo `<a>` has `aria-label="Brant Business Interiors home"`.
- Megamenu opens on hover AND focus AND click — keyboard equivalence enforced.
- Mobile drawer traps focus when open; Esc closes.
- Cart count has `aria-label="X items in your quote list"`.
- Tab order: logo → primary nav → utility → cart → CTA.

### Flagged
- Brief vs. baseline divergence. Baseline shows nav order Shop · Brands · Verticals · Our work · Services · About. Brief specifies Shop · Industries · Brands · Services · About. Following the brief.
- Submenu tokens reused for mobile drawer. Acceptable; chat-1 revision if a separate token set is wanted.

---

## 06 — Footer

### Variants

#### `.bbi-footer` — single variant, always inverse, always full-bleed, never on white.
````html
<footer class="bbi-footer">
  <div class="bbi-footer__inner">
    <div class="bbi-footer__top">
      <div class="bbi-footer__brand">
        <span class="bbi-footer__brand-plate">
          <img src="bbi-logo-v2.png" alt="Brant Business Interiors" />
        </span>
        <p class="bbi-footer__tagline">Commercial furniture, specced and installed. Quoting since 1962.</p>
        <span class="bbi-footer__canadian">
          <svg class="leaf" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l1.2 4 3.4-1.2-1.2 3.4L19 10l-4 1.5 1 3-4-1.5-1 4-1-4-4 1.5 1-3-4-1.5 3.6-1.8L5.4 4.8 8.8 6 10 2z"/></svg>
          Canadian-owned · Mississauga, ON
        </span>
      </div>
      <div class="bbi-footer__cols">
        <div class="bbi-footer__col bbi-footer__col--nav">
          <h4>Shop Furniture</h4>
          <ul>
            <li><a href="#">Seating</a></li>
            <li><a href="#">Desks &amp; Workstations</a></li>
            <li><a href="#">Storage &amp; Filing</a></li>
            <li><a href="#">Tables</a></li>
            <li><a href="#">Boardroom</a></li>
            <li><a href="#">Ergonomic Products</a></li>
            <li><a href="#">Panels &amp; Dividers</a></li>
            <li><a href="#">Accessories</a></li>
            <li><a href="#">Quiet Spaces</a></li>
          </ul>
        </div>
        <div class="bbi-footer__col bbi-footer__col--nav">
          <h4>Industries</h4>
          <ul>
            <li><a href="#">Office &amp; Corporate</a></li>
            <li><a href="#">Healthcare</a></li>
            <li><a href="#">Education</a></li>
            <li><a href="#">Government</a></li>
            <li><a href="#">Industrial</a></li>
          </ul>
        </div>
        <div class="bbi-footer__col bbi-footer__col--nav">
          <h4>Services &amp; About</h4>
          <ul>
            <li><a href="#">Space planning</a></li>
            <li><a href="#">Installation</a></li>
            <li><a href="#">Warranty &amp; service</a></li>
            <li><a href="#">Brands we carry</a></li>
            <li><a href="#">Our story</a></li>
            <li><a href="#">Careers</a></li>
            <li><a href="#">News</a></li>
          </ul>
        </div>
        <div class="bbi-footer__col bbi-footer__col--contact">
          <h4>Contact</h4>
          <div class="row"><span class="lbl">Phone</span><a href="tel:18008359565">1-800-835-9565</a></div>
          <div class="row"><span class="lbl">Email</span><a href="mailto:quotes@brantbusinessinteriors.com">quotes@brantbusinessinteriors.com</a></div>
          <div class="row"><span class="lbl">Showroom</span><span>2400 Matheson Blvd E<br/>Mississauga, ON L4W 5G9</span></div>
          <div class="row"><span class="lbl">Hours</span><span>Mon–Fri · 8:00–17:00 ET</span></div>
        </div>
      </div>
    </div>
    <div class="bbi-footer__bottom">
      <div>© 2026 Brant Business Interiors Inc. All rights reserved.</div>
      <div class="bbi-footer__legal">
        <a href="#">Privacy</a>
        <a href="#">Terms of sale</a>
        <a href="#">Accessibility</a>
      </div>
    </div>
  </div>
</footer>
````

### Tokens consumed
- `charcoal #0B0B0C` (canvas — matches inverse scheme)
- `white #FFFFFF` (type, contact column)
- `--saleBadgeBackground` (maple leaf, primary-nav hover, Canadian-owned accent)
- `#1F1F21` (column hairline dividers — mirrors `--borderColor` on inverse)
- `--space-8` / `--space-12` / `--space-16`, `--headingFont`

### Hierarchy / Sizing
- 4-column grid ≥900px (Shop · Industries · Services + About · Contact); collapses to 2 columns below.
- Brand stack stacks above the columns on narrow.
- Column headings: `--headingFont`, 13px, 600, uppercase, 0.08em tracking.
- Nav links: 14px, 400, 8px vertical rhythm.
- Bottom strip: copyright left, legal links right; hairline divider above.

### Logo treatment
Same true-alpha PNG (`bbi-logo-v2.png`) as the header.
Sits inside a white plate (`.bbi-footer__brand-plate`) because the lockup rule is "never on dark without white plate."
Plate: `background: #FFFFFF`, `padding 16px 20px`, `border-radius: var(--cardRadius)`. Padding satisfies clear-space (≥ half the height of "B" in "Brant").
Maple-leaf accent is an inline SVG with `color: #D4252A`, `fill: currentColor` — never filtered.

### States
Mostly static. Primary-nav links shift to red on hover (matches header). Contact-column links underline on hover (utility, not navigation — never red).
Legal links: 55% white at rest, 100% on hover. Never red.

### Don't
- Don't use red on contact-column links. Red is reserved for primary-nav hover and the maple leaf.
- Don't render footer on white scheme. That's the header's job.
- Don't drop the Canadian-owned line. Mandatory across every page.
- Don't promote a CTA button into the footer columns. Quote-request lives in dedicated CTA blocks (07).
- Don't recolor the logo in CSS.

### Accessibility checklist
- Contact links use semantic schemes: `tel:`, `mailto:`.
- White on charcoal = 20.10:1 AAA. Red hover on charcoal = 4.83:1 borderline AA-large for 14px nav links → mitigated by 500-weight bump on hover.
- Address uses real `<br>` linebreaks; SR announces as a block.
- Tab order: brand → Shop → Industries → Services → Contact → bottom legal.

### Flagged
- ~~Industries sector list~~ **Resolved 2026-04-27.** Canonical 5 sectors confirmed: Office & Corporate · Healthcare · Education · Government · Industrial.
- AA-large hover ink for 14px nav links — mitigated by 500-weight bump, but flag for the audit.

---

## 07 — Quote-request CTA

### Variants

#### (a) `.bbi-cta-section` — standalone marketing band. Charcoal canvas, white heading, red CTA, OECM trust line.
````html
<section class="bbi-cta-section">
  <div class="bbi-cta-section__inner">
    <div>
      <p class="bbi-cta-section__eyebrow">Built around your space</p>
      <h2 class="bbi-cta-section__heading">Get a quote, not a cart total.</h2>
      <p class="bbi-cta-section__sub">Send us a floor plan, a screenshot, or a list — we'll come back with a fully-specced proposal including freight, install, and warranty. No accounts to create, no minimums.</p>
    </div>
    <div class="bbi-cta-section__actions">
      <button class="bbi-btn bbi-btn--primary bbi-btn--lg">Request a quote <span class="arrow">→</span></button>
      <div class="bbi-cta-section__trust">
        <span class="dot"></span>
        <span><b>OECM vendor of record</b> · serving Ontario since 1962</span>
      </div>
      <div class="bbi-cta-section__trust">
        <span class="dot"></span>
        <span>Or call <a href="tel:18008359565" class="bbi-cta-section__phone">1-800-835-9565</a> · Mon–Fri 8–5 ET</span>
      </div>
    </div>
  </div>
</section>
````

#### (b) `.bbi-cta-pdp` — inline PDP block, replaces add-to-cart on unbuyable items.
````html
<div class="bbi-cta-pdp">
  <span class="bbi-cta-pdp__why">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">
      <circle cx="12" cy="12" r="9"/><path d="M12 8v5"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor"/>
    </svg>
    Why request a quote?
  </span>
  <h3 class="bbi-cta-pdp__heading">Configurable item — pricing depends on fabric, frame, and quantity.</h3>
  <p class="bbi-cta-pdp__why-body">Tell us how many, the space, and any preferred finishes. We'll send a fully-priced proposal with freight and install included.</p>
  <button class="bbi-btn bbi-btn--primary">Request a Quote <span class="arrow">→</span></button>
  <div class="bbi-cta-pdp__micro">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">
      <circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>
    </svg>
    We respond within 1 business day
  </div>
  <div class="bbi-cta-pdp__divider"></div>
  <div class="bbi-cta-pdp__alt">
    <a href="tel:18008359565">Or call 1-800-835-9565</a>
    <a href="#">Add to project list</a>
  </div>
</div>
````

### Tokens consumed
- (a) `charcoal #0B0B0C`, `white #FFFFFF`, `--buttonBackground`, `--headingFont`, `--bodyFont`, `--space-12` / `--space-16`
- (b) `--bodyBg`, `--borderColor`, `--cardRadius`, `--saleBadgeBackground`, `--buttonBackground`, `--textColor`

### Hierarchy / Sizing
- (a) Heading-led. Heading: `clamp(32px, 4.2vw, 56px)`, 700, -0.01em. Subhead: 17px, max-width 52ch. CTA: `.bbi-btn--lg` (52px). Section padding: `clamp(48px, 7vw, 96px)`.
- (b) Action-led. Heading: 20px, 700. Body: 14px, 78% opacity. CTA: 56px tall, full-width, 16px font, centered label. Card max-width: 460px.

### Copy rules
- (a) Heading: outcome-framed, ≤8 words. Model: "Get a quote, not a cart total."
- (b) Eyebrow: always "Why request a quote?" — answers the visitor's implicit question.
- (b) Heading: one sentence, ≤14 words, names the specific reason ("configurable", "freight-dependent", "quantity-priced").
- (b) Microcopy: "We respond within 1 business day" is mandatory. If you can't honor the SLA, change the copy — don't drop it.
- Button label: "Request a quote" on standalone (sentence case); "Request a Quote" on PDP (title case, action-emphasis). Asymmetry is intentional.

### States
Inherits five button states from `.bbi-btn--primary`. No new state work.
Focus ring on standalone (charcoal) = white. On PDP card (white) = charcoal. Both already covered by the button component.

### Don't
- Don't pair the standalone CTA with another red element in the same band. The button is the only red.
- Don't use the PDP variant on items that are genuinely add-to-cart-able. If a SKU has a fixed price + ships standalone, give it a real cart button.
- Don't shrink the PDP button below 56px.
- Don't replace "OECM vendor of record" with a generic "trusted by businesses" line. Trust signals are specific or they're noise.
- Don't add a secondary button alongside the primary CTA. Phone fallback is a text link.
- Don't use the standalone section as a header. It's a closer.

### Accessibility checklist
- (a) White on charcoal = 20.10:1 AAA. White-78% on charcoal = ~13.9:1 AAA.
- (b) Red eyebrow on white: #D4252A = 4.93:1 AA-large. Eyebrow is 12px/600 — borderline. Mitigation: 600 weight + 0.08em tracking lifts perceived weight above the AA-large threshold.
- Phone numbers use `tel:` schemes.
- Tab order on PDP: button → phone link → project-list link.
- Standalone heading is `<h2>`. PDP heading is `<h3>` (sits inside the PDP's `<h1>` + `<h2>` outline).

### Flagged
~~OECM trust line~~ **Resolved 2026-04-27.** BBI confirmed on the OECM roster. "OECM vendor of record" copy is accurate and ships as written.

---

## Cross-component flagged conflicts (consolidated)

| # | Component | Flag | Resolution |
|---|---|---|---|
| 1 | 02 Form Inputs | `--inputPlaceholder` contrast 4.55:1 — barely AA-normal | Acceptable; flag if users enlarge text |
| 2 | 03 Cards | Card shadow disappears on tinted backgrounds | Hairline-border fallback exists |
| 3 | 04 Badges | `--warningBackground` not specified in tokens v1; used #E8A317 placeholder | ✅ #E8A317 approved 2026-04-27; token added to tokens.css |
| 4 | 05 Header | Brief vs. baseline nav-order divergence | Following brief: Shop · Industries · Brands · Services · About |
| 5 | 05 Header | Submenu tokens reused for mobile drawer | Acceptable; chat-1 revision if separate set wanted |
| 6 | 06 Footer | Industries — 5 sectors assumed (Office & Corporate · Healthcare · Education · Government · Industrial) | ✅ Confirmed canonical 2026-04-27 |
| 7 | 06 Footer | 14px nav-link AA-large hover ink borderline | Mitigated by 500-weight on hover |
| 8 | 07 CTA | OECM trust line — used as lead signal | ✅ BBI confirmed on OECM roster 2026-04-27; copy ships as written |

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

---

**Phase 2 complete. All three flags resolved 2026-04-27.** OECM confirmed, Industries sectors confirmed, `--warningBackground` #E8A317 approved. Ready for Phase 3 screen work.
