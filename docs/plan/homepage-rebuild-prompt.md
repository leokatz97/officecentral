# Homepage Rebuild Prompt
## BBI Design System v2 — Full Conformance Fix

**File to rebuild:** `previews/homepage-draft-v1.html`
**Canonical source:** `Design System Zips/5 - Landing Page (2)/uploads/` (LOCKED files — these supersede everything)
**Date:** 2026-05-05

---

## What went wrong in the previous draft

Three root causes:

1. **Wrong structural reference** — the draft was built from `data/design-photos/components-v1-2026-04-27/Components.html`, which is a component spec sheet, not a page template. The authoritative homepage template is `uploads/02-LOCKED-Homepage.jsx`.
2. **Sections wrong** — the draft kept placeholder sections that don't exist in the template (wrong categories, wrong order). The JSX component tree is the ground truth for what sections appear and in what order.
3. **Logo + nav not updated** — old logo path and old nav labels from a prior design version.

---

## Before you start — read these files

Attach / read all of these before making any changes:

| File | Purpose |
|---|---|
| `Design System Zips/5 - Landing Page (2)/uploads/02-LOCKED-Homepage.jsx` | Authoritative section order and component tree |
| `Design System Zips/5 - Landing Page (2)/uploads/05-tokens.css` | Canonical CSS custom property names |
| `Design System Zips/5 - Landing Page (2)/uploads/06-bbi-components.css` | All shared component classes |
| `Design System Zips/5 - Landing Page (2)/uploads/07-homepage.css` | All homepage layout classes |
| `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` | Visual reference — overall layout |
| `Design System Zips/5 - Landing Page (2)/uploads/16-ANTI-REF-nav.png` | Visual reference — header/nav exact |
| `Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png` | Correct logo file |

---

## Fix 1 — Logo

**Current (wrong):**
```html
<img src="../data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png" ...>
```

**Correct:**
```html
<img src="../Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png"
     alt="Brant Business Interiors" height="36" style="height:36px;width:auto;">
```

The new logo wordmark is **"Brant ✱ BI | Business Interiors"** — confirm visually against `16-ANTI-REF-nav.png`.

---

## Fix 2 — Nav labels

**Current (wrong):** Shop | Industries | Brands | Services | About

**Correct (per ANTI-REF):** Shop | Brands | Verticals | Our work | Services | About

Update every nav link label in the `<nav>` element. Keep the same href placeholders — only the visible labels change.

---

## Fix 3 — Remove the CTA band

The draft incorrectly includes a `.bbi-cta-section.scheme-inverse` block between Testimonials and Footer.

`Homepage.jsx` goes directly: **Testimonials → Footer**. There is no CTA band on the homepage.

Delete the entire `<section class="bbi-cta-section scheme-inverse">` block.

---

## Fix 4 — Rebuild all body sections

The draft has wrong placeholder sections. Replace everything between `</header>` and `<footer>` with the correct 7-section structure from `Homepage.jsx`. Build each section using **only** classes from `06-bbi-components.css` and `07-homepage.css` — no invented classes.

### Section order (authoritative — from Homepage.jsx):

```
Header → Hero → ShopEntry → FeaturedProducts → OECMBar → Industries → Services → Testimonials → Footer
```

---

### Section 1: Hero

CSS source: `07-homepage.css` — `.hp-hero`, `.hp-hero__inner`, `.hp-hero__copy`, `.hp-hero__media`

Structure:
```html
<section class="hp-hero">
  <div class="bbi-container">
    <div class="hp-hero__inner">

      <!-- Copy column -->
      <div class="hp-hero__copy">
        <!-- Eyebrow: red dot + JetBrains Mono text at 70% opacity -->
        <p class="hp-hero__eyebrow bbi-mono">
          <span class="dot"></span>
          Ontario's institutional furniture partner
        </p>

        <h1 class="hp-hero__title">
          The workspace your team deserves. Delivered.
        </h1>

        <p class="hp-hero__deck">
          Office furniture for Ontario's schools, hospitals, and municipal teams — OECM-eligible, quote-based, no cart required.
        </p>

        <p class="hp-hero__sub">
          OECM Supplier Partner · Agreement 2025-470 · Quote in 1 business day
        </p>

        <div class="hp-hero__actions">
          <!-- Primary CTA: RED on hero only (hp-hero__cta-red class) -->
          <a href="/pages/quote" class="bbi-btn bbi-btn--lg hp-hero__cta-red">
            Request a Quote
          </a>
          <!-- Secondary CTA: charcoal outline -->
          <a href="tel:18008359565" class="bbi-btn bbi-btn--lg bbi-btn--secondary">
            Call 1-800-835-9565
          </a>
        </div>

        <p class="hp-hero__micro">
          <a href="/pages/oecm">OECM Agreement 2025-470</a> — Ontario institutional buyers purchase without open tender.
        </p>
      </div>

      <!-- Media column -->
      <div class="hp-hero__media">
        <div class="bbi-ph" style="aspect-ratio:16/11;">
          <span class="bbi-ph__label">Hero image — office space</span>
        </div>
        <div class="hp-hero__caption">
          <span class="dot"></span>
          <span class="bbi-mono">Kawartha Dairy — 2024 install</span>
        </div>
      </div>

    </div>
  </div>
</section>
```

**Key rules for hero:**
- Red CTA uses `.hp-hero__cta-red` — this is the ONLY place on the homepage where red appears on a button
- Eyebrow: red dot + 70% opacity JetBrains Mono text, NOT red text
- No other red on this section beyond the dot and button

---

### Section 2: ShopEntry (4 collection tiles)

CSS source: `07-homepage.css` — `.hp-shop__tiles`
Component: `06-bbi-components.css` — `.bbi-card--collection`

Section head uses standard `.bbi-section-head` with eyebrow red rule (see Component canon below).

4 tiles in a `grid-template-columns: repeat(4, 1fr)` grid. Each tile is a `.bbi-card--collection` — overlay style (4:3 image with title + CTA overlaid at bottom).

```html
<section class="bbi-section">
  <div class="bbi-container">
    <div class="bbi-section-head">
      <div>
        <p class="bbi-section-head__eyebrow bbi-mono">Shop furniture</p>
        <h2 class="bbi-section-head__title">Everything your space needs</h2>
      </div>
      <div class="hp-shop__head-right">
        <p>9 categories. 200+ brands. Configured for institutional use.</p>
        <a href="/collections/business-furniture" class="bbi-btn bbi-btn--secondary bbi-btn--sm">
          View all categories <span class="arrow">→</span>
        </a>
      </div>
    </div>

    <div class="hp-shop__tiles">
      <!-- 4 × .bbi-card--collection -->
      <a href="/collections/seating" class="bbi-card--collection">
        <div class="bbi-card--collection__media bbi-ph" style="aspect-ratio:4/3;">
          <span class="bbi-ph__label">Seating</span>
        </div>
        <div class="bbi-card--collection__body">
          <span class="bbi-card--collection__title">Seating</span>
          <span class="bbi-card--collection__cta bbi-btn bbi-btn--sm bbi-btn--primary">Shop →</span>
        </div>
      </a>
      <!-- Repeat for Desks, Storage, Tables -->
    </div>
  </div>
</section>
```

---

### Section 3: FeaturedProducts (3 product cards)

CSS source: `07-homepage.css` — `.hp-products__grid`
Component: `06-bbi-components.css` — `.bbi-card--product`

3 products in `grid-template-columns: repeat(3, 1fr)`. Each `.bbi-card--product` has a **16:9 image slot at top** (non-negotiable — see design system rule).

Section head: standard `.bbi-section-head` with eyebrow.

```html
<section class="bbi-section">
  <div class="bbi-container">
    <div class="bbi-section-head">
      <div>
        <p class="bbi-section-head__eyebrow bbi-mono">Featured products</p>
        <h2 class="bbi-section-head__title">Built for institutional use</h2>
      </div>
      <a href="/collections/business-furniture" class="bbi-btn bbi-btn--secondary bbi-btn--sm hp-products__all">
        View all products →
      </a>
    </div>

    <div class="hp-products__grid">
      <!-- 3 × .bbi-card--product (16:9 image at top) -->
      <div class="bbi-card--product">
        <div class="bbi-card--product__media bbi-ph" style="aspect-ratio:16/9;">
          <span class="bbi-ph__label">Product image</span>
        </div>
        <div class="bbi-card--product__body">
          <p class="bbi-card--product__name">Siento Task Chair</p>
          <p class="bbi-card--product__desc">ergoCentric — OECM eligible</p>
          <a href="#" class="bbi-btn bbi-btn--primary bbi-btn--sm">Request a Quote</a>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### Section 4: OECMBar

CSS source: `07-homepage.css` — `.hp-oecm`, `.hp-oecm__inner`, `.hp-oecm__lead`, `.hp-oecm__copy`
Component: `06-bbi-components.css` — `.bbi-badge--oecm`

Full-width band, no `.bbi-section` wrapper, no section head.

```html
<div class="hp-oecm">
  <div class="hp-oecm__inner">
    <div class="hp-oecm__lead">
      <span class="bbi-badge--oecm bbi-mono">OECM Supplier Partner</span>
      <p class="hp-oecm__copy">
        Agreement 2025-470 — Ontario school boards, hospitals, and municipalities can
        purchase directly through OECM without open tender.
      </p>
    </div>
    <div class="hp-oecm__meta">
      <a href="/pages/oecm" class="bbi-btn bbi-btn--secondary bbi-btn--sm">
        Learn more →
      </a>
    </div>
  </div>
</div>
```

---

### Section 5: Industries (5 industry tiles)

CSS source: `07-homepage.css` — `.hp-industries__grid`, `.hp-industry`, `.hp-industry__body`, `.hp-industry__num`, `.hp-industry__title`, `.hp-industry__note`

5 tiles in `grid-template-columns: repeat(5, 1fr)`. Each tile is 1:1 square. Mono numbers `01` through `05`.

```html
<section class="bbi-section">
  <div class="bbi-container">
    <div class="bbi-section-head">
      <div>
        <p class="bbi-section-head__eyebrow bbi-mono">Industries served</p>
        <h2 class="bbi-section-head__title">Ontario's institutional sectors</h2>
      </div>
    </div>

    <div class="hp-industries__grid">
      <!-- 5 × .hp-industry (mono numbers 01–05) -->
      <a href="/pages/healthcare" class="hp-industry">
        <div class="hp-industry__media bbi-ph" style="aspect-ratio:1/1;">
          <span class="bbi-ph__label">Healthcare</span>
        </div>
        <div class="hp-industry__body">
          <span class="hp-industry__num bbi-mono">01</span>
          <p class="hp-industry__title">Healthcare &amp; Seniors</p>
          <p class="hp-industry__note">Hospitals, LTCs, clinics</p>
        </div>
      </a>
      <!-- 02 Education, 03 Government, 04 Non-profit, 05 Professional Services -->
    </div>
  </div>
</section>
```

---

### Section 6: Services (3 service panels)

CSS source: `07-homepage.css` — `.hp-services__grid`, `.hp-service`, `.hp-service__num`, `.hp-service__title`, `.hp-service__body`, `.hp-service__list`, `.hp-service__cta`

3 panels in a borderless grid (`grid-template-columns: repeat(3, 1fr)`, outer border on the grid container, inner vertical dividers via `border-right`). Mono numbers are **red** (`color: var(--saleBadgeBackground)`).

```html
<section class="bbi-section">
  <div class="bbi-container">
    <div class="bbi-section-head">
      <div>
        <p class="bbi-section-head__eyebrow bbi-mono">What we offer</p>
        <h2 class="bbi-section-head__title">Services included with every project</h2>
      </div>
    </div>

    <div class="hp-services__grid">
      <div class="hp-service">
        <span class="hp-service__num bbi-mono">01</span>
        <h3 class="hp-service__title">Space Planning</h3>
        <p class="hp-service__body">Free space plan included with every quote — no commitment required.</p>
        <ul class="hp-service__list">
          <li>CAD drawings</li>
          <li>3D renders on request</li>
          <li>Furniture specification</li>
        </ul>
        <a href="/pages/design-services" class="bbi-btn bbi-btn--tertiary bbi-btn--sm hp-service__cta">
          <span class="label">Learn more</span>
        </a>
      </div>
      <!-- 02 Delivery & Installation, 03 OECM Procurement -->
    </div>
  </div>
</section>
```

---

### Section 7: Testimonials / Our Work

CSS source: `07-homepage.css` — `.hp-work__grid`, `.hp-work__quote`, `.hp-work__mark`, `.hp-work__attr`, `.hp-work__avatar`, `.hp-work__cases`, `.hp-case`

Two-column grid (`1fr 1.4fr`): left is a blockquote card, right is 3 `.hp-case` project tiles stacked.

Each `.hp-case` is `grid-template-columns: 200px 1fr` — thumbnail (200px) + year/client/scope text.

```html
<section class="bbi-section">
  <div class="bbi-container">
    <div class="bbi-section-head">
      <div>
        <p class="bbi-section-head__eyebrow bbi-mono">Our work</p>
        <h2 class="bbi-section-head__title">Trusted by Ontario institutions</h2>
      </div>
      <a href="/pages/customer-stories" class="bbi-btn bbi-btn--secondary bbi-btn--sm">
        View all projects →
      </a>
    </div>

    <div class="hp-work__grid">

      <!-- Left: featured quote -->
      <div class="hp-work__quote">
        <svg class="hp-work__mark" viewBox="0 0 32 24" fill="currentColor">
          <path d="M0 24V14.4C0 6.4 5.2 1.6 15.6 0l1.6 3.2C11.2 4.8 8 8 8 12h6V24H0zm18 0V14.4C18 6.4 23.2 1.6 33.6 0l1.6 3.2C29.2 4.8 26 8 26 12h6V24H18z"/>
        </svg>
        <blockquote>
          "Brant Business Interiors handled our entire Peterborough campus fit-out on time and on budget — OECM made procurement simple."
        </blockquote>
        <div class="hp-work__attr">
          <div class="hp-work__avatar">
            <div class="bbi-ph" style="width:44px;height:44px;border-radius:99px;"></div>
          </div>
          <div>
            <p class="hp-work__name">Sarah Mitchell</p>
            <p class="hp-work__role">Facilities Manager, Kawartha Dairy</p>
          </div>
        </div>
      </div>

      <!-- Right: 3 project tiles -->
      <div class="hp-work__cases">
        <!-- 3 × .hp-case -->
        <a href="#" class="hp-case">
          <div class="hp-case__thumb bbi-ph" style="width:200px;aspect-ratio:3/2;"></div>
          <div class="hp-case__info">
            <span class="hp-case__year bbi-mono">2024</span>
            <p class="hp-case__client">Kawartha Dairy</p>
            <p class="hp-case__scope">Office fit-out — 48 workstations</p>
          </div>
        </a>
      </div>

    </div>
  </div>
</section>
```

---

## Fix 5 — Section head eyebrow pattern

Every `.bbi-section-head__eyebrow` must have a red horizontal rule prefix rendered via CSS `::before`. Add this CSS rule to the `<style>` block if it isn't already there:

```css
.bbi-section-head__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
.bbi-section-head__eyebrow::before {
  content: "";
  display: block;
  width: 24px;
  height: 1px;
  background: var(--saleBadgeBackground);
  flex-shrink: 0;
}
```

---

## Fix 6 — Section/container rhythm

Every body section (except OECMBar) must use:
```html
<section class="bbi-section">   <!-- padding: 96px 0 -->
  <div class="bbi-container">  <!-- max-width: 1320px; padding: 0 32px; margin: 0 auto -->
```

No per-section `clamp()` padding. No different max-widths. All sections get 96px top/bottom padding from `.bbi-section`.

CSS to include:
```css
.bbi-section { padding: 96px 0; }
.bbi-container { max-width: 1320px; margin: 0 auto; padding: 0 32px; }
```

---

## Fix 7 — Placeholder component (bbi-ph)

For all image slots, use:
```html
<div class="bbi-ph" style="aspect-ratio: 16/9;">
  <span class="bbi-ph__label">Description</span>
</div>
```

CSS:
```css
.bbi-ph {
  background: repeating-linear-gradient(
    -45deg,
    var(--alternateBackground),
    var(--alternateBackground) 4px,
    var(--borderColor) 4px,
    var(--borderColor) 8px
  );
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.bbi-ph__label {
  font-family: "JetBrains Mono", monospace;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--textColor);
  opacity: 0.5;
  padding: 8px 12px;
  background: var(--background);
  border-radius: 2px;
}
```

---

## Component canon — CSS classes to inline

Paste the complete contents of these two files into the `<style>` block of the HTML (after tokens):

1. `Design System Zips/5 - Landing Page (2)/uploads/06-bbi-components.css` — all shared classes
2. `Design System Zips/5 - Landing Page (2)/uploads/07-homepage.css` — all homepage layout classes

Do not strip or abbreviate. The full CSS must be present so the preview renders correctly.

---

## Red density check (required after rebuild)

Scan the finished page section by section. Red (`#D4252A`) should appear ONLY on:
- Hero primary CTA button background (`.hp-hero__cta-red`)
- Hero eyebrow red dot
- Hero caption dot
- Section head eyebrow `::before` red rule
- Services mono numbers (`hp-service__num`)
- Testimonials quotation mark SVG (`hp-work__mark`)
- OECM badge border/accent (if applicable)

Red must NOT appear on:
- Any heading
- Any body text
- Any nav link
- Any card background
- Header CTA (charcoal, not red)
- Footer anything

Target: 5–8% red surface area per screen. Eyeball it — if it looks heavy, demote a secondary element.

---

## After the rebuild — update these reference files

### CLAUDE.md key reference table

Add these rows:

| Need | File |
|---|---|
| **Homepage template structure (authoritative)** | `Design System Zips/5 - Landing Page (2)/uploads/02-LOCKED-Homepage.jsx` |
| **Canonical component CSS** | `Design System Zips/5 - Landing Page (2)/uploads/06-bbi-components.css` |
| **Canonical homepage layout CSS** | `Design System Zips/5 - Landing Page (2)/uploads/07-homepage.css` |
| **Canonical tokens (DS Zips)** | `Design System Zips/5 - Landing Page (2)/uploads/05-tokens.css` |
| **Visual reference — homepage layout** | `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` |
| **Visual reference — nav/header** | `Design System Zips/5 - Landing Page (2)/uploads/16-ANTI-REF-nav.png` |
| **Logo v2 (new wordmark)** | `Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png` |

### /bbi-build-page skill

Update the following (skill update is handled separately — see skill patch below):
- Pre-Step 0a gate: reference `uploads/` LOCKED files, not `data/design-photos/design-system-v1-*/`
- Component canon: reference `uploads/06-bbi-components.css` and `uploads/07-homepage.css`
- Step 3 nav: update labels to "Shop | Brands | Verticals | Our work | Services | About"
- Step 3 readiness gate: add `uploads/02-LOCKED-Homepage.jsx` as homepage structural reference
- Logo: update to `uploads/14-bbi-logo-v2.png`
- Step 7 conformance: add checks for `.bbi-section`, `.bbi-container`, `.bbi-section-head`, `.hp-hero__cta-red`, section head eyebrow `::before` red rule

---

## Verification checklist

After the rebuild, confirm all of these:

- [ ] Logo shows new "Brant ✱ BI | Business Interiors" wordmark
- [ ] Nav labels: Shop | Brands | Verticals | Our work | Services | About
- [ ] Hero: red dot eyebrow + red primary CTA + charcoal secondary CTA
- [ ] No CTA band between Testimonials and Footer
- [ ] 7 body sections in correct order: Hero → ShopEntry → FeaturedProducts → OECMBar → Industries → Services → Testimonials
- [ ] Each section uses `.bbi-section` + `.bbi-container` wrapper
- [ ] Every section head eyebrow has red `::before` rule
- [ ] ShopEntry has 4 collection tiles (4:3 overlay cards)
- [ ] FeaturedProducts has 3 product cards (16:9 image at top)
- [ ] OECMBar is full-width band with OECM badge + copy + CTA
- [ ] Industries has 5 tiles (1:1 square, mono numbers 01–05)
- [ ] Services has 3 panels (mono red numbers, bullet list, tertiary CTA)
- [ ] Testimonials has blockquote card (left) + 3 case tiles (right, 200px thumb)
- [ ] No red headings anywhere
- [ ] No beige/warm tones anywhere
- [ ] Red density 5–8% — not concentrated beyond hero + section heads + service numbers
