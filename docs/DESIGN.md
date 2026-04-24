# BBI Design System

Brant Business Interiors — live theme: **BBI Live** (`178274435385`) on `office-central-online.myshopify.com`.
All values are pulled directly from `config/settings_data.json` as of 2026-04-23.

---

## 1. Brand Overview

Brant Business Interiors serves B2B institutional buyers in Canada — municipalities, schools, healthcare facilities, and corporate offices. The aesthetic is clean, professional, and trustworthy. Not consumer retail. Promotions are rare; the primary conversion goal is a quote request, not a cart checkout.

**Core Brand Values:**
- Professional and institutional credibility
- Canadian ownership and expertise
- Long-term relationships over one-off transactions
- Knowledgeable sales support (not self-serve)
- Accessibility and AODA/WCAG compliance

---

## 2. Color Palette

### Primary Brand Colors

| Name | Hex | Usage |
|------|-----|-------|
| BBI Navy | `#003865` | Header icons, arrow backgrounds, anchor color — the core brand color |
| BBI Green | `#98ca3c` | Highlight accent, active states, "in stock", deal callouts |
| Near Black | `#121212` | Headings, body text, borders, dividers, input outlines |
| Black | `#000000` | Primary buttons, badge backgrounds, strong text |
| White | `#ffffff` | Primary background, card backgrounds, button text |

### Neutral Scale

| Name | Hex | Usage |
|------|-----|-------|
| Medium Gray | `#5c5c5c` | Secondary nav bar background, cart count background |
| Light Gray | `#c4c4c4` | Footer background |
| Off White / Light | `#f3f3f3` | Secondary scheme background, alternate sections |

### Semantic / Promotional Colors

| Name | Hex | Usage |
|------|-----|-------|
| Sale Red | `#e91616` | Sale badge background |
| Alert Red | `#e52424` | Cart count, footer hover, sub-menu hover |
| Marquee Red | `#e4172a` | Marquee/announcement bar text |
| Rating Gold | `#ecac23` | Star ratings |
| BBI Blue | `#334fb4` | Tertiary color scheme (used for hero section backgrounds) |
| Bright Blue | `#0d43da` | Custom scheme (used sparingly for feature callouts) |

### Color Schemes (Shopify Theme Schemes)

These are the named color schemes available to any section in the theme. Reference them by name when building new sections.

| Scheme | Background | Text | Accent | Use For |
|--------|-----------|------|--------|---------|
| `primary` | `#ffffff` | `#000000` | `#98ca3c` | Default — most pages |
| `secondary` | `#f3f3f3` | `#121212` | `#ffca10` | Alternate sections, subtle separation |
| `inverse` | `#242833` | `#ffffff` | `#ffca10` | Dark banners, trust sections |
| `quaternary` | `#121212` | `#ffffff` | `#ffca10` | Full-black sections, CTAs on dark |
| `tertiary` | `#334fb4` | `#ffffff` | `#ffca10` | Hero/feature sections with blue brand feel |
| `scheme-e1dc3090` | `#e40007` | `#000000` | `#98ca3c` | Promotional/sale sections (use very sparingly) |
| `scheme-a3ff4e8f` | `#98ca3c` | `#000000` | `#ffffff` | Green feature highlight sections |
| `scheme-52d244d2` | `#0d43da` | `#000000` | `#98ca3c` | Bold blue feature banners |
| `scheme-b1305ced` | `#ffffff` | `#000000` | `#98ca3c` | Cart drawer, overlays (same as primary) |

### Dark Mode

Dark mode is supported. Key overrides:

| Variable | Dark Value | Hex |
|----------|-----------|-----|
| Background | Black | `#000000` |
| Text | Light gray | `#d1d1d1` |
| Button BG | Gold | `#ffca10` |
| Button Text | Black | `#000000` |
| Hover accent | Gold | `#ffca10` |
| Header BG | Black | `#000000` |
| Header text | Light gray | `#d1d1d1` |
| Submenu BG | Near black | `#161616` |

---

## 3. Typography

### Font Stack

Both heading and body use **Inter** (loaded via Shopify Fonts). System fallback: sans-serif.

```css
--bodyFont: Inter, sans-serif;
--headingFont: Inter, sans-serif;
```

### Font Weights

| Role | Weight | Shopify Token |
|------|--------|--------------|
| Body | 500 (Medium) | `inter_n5` |
| Heading | 400 (Regular) | `inter_n4` |
| Buttons | Uses heading weight (400) | via `--buttonFontWeight` |

> Note: BBI uses Medium weight for body text for institutional legibility, with Regular-weight headings — the inverse of typical consumer retail. This keeps the aesthetic professional and dense without being harsh.

### Type Scale

The scale is relative to a base size, calculated in CSS using `calc()`.

| Token | Desktop | Mobile | Usage |
|-------|---------|--------|-------|
| `--bodyFontBase` | `14px` | smaller | Standard body copy |
| `--headingFontBase` | `27px` | `23px` | Base for heading scale |
| `--h0` | `59px` | `33px` | Hero headlines |
| `--h1` | `52px` | `31px` | Page titles |
| `--h2` | `31px` | `25px` | Section headers |
| `--h3` | `27px` | `23px` | Card/subsection headers |
| `--h4` | `23px` | `21px` | Minor headings |
| `--h5` | `21px` | `19px` | Labels, callouts |
| `--h6` | `19px` | `17px` | Smallest heading |
| `--xsmallText` | `10px` | — | Micro labels |
| `--smallText` | `12px` | — | Captions, metadata |
| `--text` | `14px` | — | Body default |
| `--mediumText` | `16px` | — | Slightly larger body |
| `--largeText` | `18px` | — | Emphasized body |
| `--xlargeText` | `20px` | — | Large body |

### Typography Guidelines

- Headings: Inter Regular (400) — clean and institutional
- Body: Inter Medium (500) — readable at small sizes for spec-heavy product pages
- Prices and key CTAs: Bold (700) applied manually in component
- All-caps used only for badges and short labels
- Line height: `1.5` body, `1.3` headings

---

## 4. Spacing System

BBI uses an 8px base unit. Key spacing values:

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | `4px` | Tight inline gaps |
| `space-2` | `8px` | Icon-to-text gaps, compact padding |
| `space-3` | `12px` | Small component padding |
| `space-4` | `16px` | Standard padding, card gutters |
| `space-6` | `24px` | Section padding |
| `space-8` | `40px` | Major section separators |
| `space-10` | `64px` | Page-level section gaps |

### Layout

| Context | Value |
|---------|-------|
| Page margin (mobile) | `16px` |
| Page margin (tablet) | `24px` |
| Page margin (desktop) | `32–48px` |
| Max content width | `1440px` |
| Grid gutter | `16px` |
| Header height | ~`64px` |

---

## 5. Border Radius

All radius values come from theme settings and apply globally.

| Token | Desktop | Mobile | Applies To |
|-------|---------|--------|------------|
| `--buttonRadius` | `54px` | `54px` | Buttons — fully pill-shaped |
| `--cardRadius` | `10px` | `8px` | Content cards |
| `--imageRadius` | `16px` | `8px` | Images within cards |
| `--productRadius` | `10px` | `8px` | Product grid cards |
| `--inputRadius` | `30px` | `20px` | Form inputs — rounded pill |

> BBI uses heavily rounded buttons and inputs (near-pill) with moderately rounded cards. This softens the institutional aesthetic without looking consumer-retail.

---

## 6. Component Library

### Buttons

**Primary Button**
```
Background:       #000000
Text:             #ffffff
Border:           #000000
Border Radius:    54px (pill)
Hover BG:         #ffffff
Hover Text:       #000000
Hover Border:     #ffffff
Shadow:           #bbbbbb
Font:             Inter, 400 (heading weight)
Text Transform:   as set in settings (check btn_text_color settings)
```

**Secondary Button (Outlined)**
```
Background:       #ffffff
Text:             #121212
Border:           2px solid #121212
Border Radius:    54px (pill)
Hover BG:         #ffffff
Hover Text:       #ffffff
Hover Border:     #ffffff
Shadow:           #000000
```

**Quote / Contact CTA Button**
Used in place of "Add to Cart" for showcase products and $0-price items.
```
Label:   "Request a Quote"
Style:   Primary button styling (black pill)
Action:  Links to /pages/contact or opens contact form
```

> B2B rule: unbuyable products stay live with a quote CTA. Never archive a showcase page just because it has no price.

### Product Cards

```
Structure:
├── Image Container (square aspect ratio)
│   ├── Product Image (border-radius: 16px desktop / 8px mobile)
│   ├── Favorite / Wishlist Icon (top right)
│   └── Badges (top left — Sale, New, Custom)
├── Product Info
│   ├── Brand Name (12px, #5c5c5c, Regular)
│   ├── Product Name (heading font, #121212, h4-size)
│   ├── Rating Stars (#ecac23) + Review Count (#5c5c5c)
│   └── Price Section
│       ├── Current Price (bold, #121212)
│       └── Compare-at Price (strikethrough, #5c5c5c)
└── Delivery / Lead Time (12px, gray)

Card:
- Background:     #ffffff
- Border Radius:  10px (desktop) / 8px (mobile)
- Shadow on hover: 0 2px 8px rgba(0,0,0,0.1)
- Product border: #121212
```

### Badges

**Sale Badge**
```
Background:   #e91616
Text:         #ffffff (auto by brightness)
Font:         11px, Bold, uppercase
Padding:      4px 8px
Border Radius: 4px
```

**New Badge**
```
Background:   #000000
Text:         #ffffff
Font:         11px, Bold, uppercase
```

**Custom Badge**
Configurable per-product. Background auto-determines text (black or white based on brightness).

### Navigation

**Primary Header**
```
Background:         #ffffff
Icon Color:         #003865 (BBI Navy)
Text:               #ffffff (on dark nav bar section)
Text Hover:         #e7e7e7
Cart Count BG:      #5c5c5c
Cart Count Color:   #e52424
```

**Secondary Header / Hamburger**
```
Background:         #5c5c5c
Text:               #ffffff
Text Hover:         #5c5c5c
```

**Mega Menu / Submenu**
```
Submenu BG:         from settings (header_sub_menu_bg)
Submenu Text Hover: #e52424
Overlay BG:         rgba(mega_menu_overlay)
Overlay Text:       from settings
```

**Footer**
```
Background:   #c4c4c4
Text:         #000000
Link Hover:   #e52424
```

### Search Bar

```
Height:       44px
Border:       1px solid #121212
Border Radius: 30px (input radius, pill)
Background:   #ffffff
Text Color:   #000000
Placeholder:  "Search products..."
Focus:        Border #003865, subtle shadow
```

### Form Inputs

```
Background:     #ffffff
Text:           #121212
Border:         1px solid #121212
Border Radius:  30px (desktop) / 20px (mobile) — pill shape
Height:         44px
Padding:        12px 20px
Focus:          Border #003865, box-shadow rgba(0,56,101,0.2)
Error:          Border #e52424
```

### Rating Stars

```
Filled:    #ecac23 (gold)
Empty:     #d6d6d6
Size:      14–16px
Count:     (#reviews) in #5c5c5c
```

### Announcement Bar / Marquee

```
Text Color:   #e4172a
Background:   from section scheme
Animation:    scrolling marquee, ~3s speed
```

---

## 7. Layout & Grid

### Breakpoints

| Name | Width | Columns | Notes |
|------|-------|---------|-------|
| Mobile | 0–767px | 2 | 16px margins |
| Tablet | 768–1023px | 3–4 | 24px margins |
| Desktop | 1024–1439px | 4–5 | 32px margins |
| Desktop Large | 1440px+ | 5–6 | 48px margins |

### Product Grid

| Viewport | Products Per Row |
|----------|-----------------|
| Mobile | 2 |
| Tablet | 3–4 |
| Desktop | 4–5 |

### Page Structure

```
Layout:
├── Header (sticky on scroll)
│   ├── Secondary nav bar (gray, #5c5c5c)
│   ├── Main header (white, logo + search + cart)
│   └── Mega menu / category bar
├── Announcement Bar (marquee, optional)
├── Hero Section (scheme: tertiary or primary)
├── Main Content
│   ├── Breadcrumbs
│   ├── Page Title
│   ├── Filters (desktop sidebar or top bar)
│   ├── Product Grid
│   └── Pagination
├── Cross-sell / Related Products
└── Footer (#c4c4c4)
    ├── Logo + tagline
    ├── Link columns
    ├── Social icons
    └── Legal / copyright
```

---

## 8. Motion & Animation

### Durations

| Duration | Time | Usage |
|----------|------|-------|
| Instant | `100ms` | Hover color changes |
| Fast | `150ms` | Button states |
| Normal | `200ms` | Card hover, transitions |
| Moderate | `300ms` | Modals, drawers |
| Slow | `400ms` | Page-level animations |

### Standard Animations

**Hover Lift (Product Card)**
```css
transition: transform 200ms ease, box-shadow 200ms ease;
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
```

**Button Press**
```css
transition: transform 100ms ease;
transform: scale(0.98);
```

**Slider / Carousel Arrows**
```
Arrow BG:     #003865 (BBI Navy)
Arrow Color:  #ffffff
Width:        52px (desktop) / 40px (tablet) / 32px (mobile)
```

**Marquee Speed**
```css
--marqueeSpeed: 3s;
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 9. Accessibility

### Color Contrast (Key Pairs)

| Combination | Approx Ratio | WCAG |
|-------------|-------------|------|
| `#121212` on `#ffffff` | 18.1:1 | AAA |
| `#ffffff` on `#000000` | 21:1 | AAA |
| `#003865` on `#ffffff` | ~9.4:1 | AAA |
| `#98ca3c` on `#000000` | ~6.9:1 | AA |
| `#5c5c5c` on `#ffffff` | ~5.7:1 | AA |
| `#ecac23` on `#ffffff` | ~2.7:1 | Fails — use only decorative (stars) |

> Note: `#ecac23` gold on white fails WCAG. Stars are decorative — always include numeric rating text alongside.

### Focus States

```css
:focus-visible {
  outline: 2px solid #003865;
  outline-offset: 2px;
}

input:focus, select:focus, textarea:focus {
  border-color: #003865;
  box-shadow: 0 0 0 3px rgba(0, 56, 101, 0.2);
  outline: none;
}
```

### B2B-Specific Accessibility

- Minimum touch target: 44×44px (matches input/button height)
- Price always includes unit context (e.g. "per unit", "each") — institutional buyers need this
- Quote buttons must have descriptive `aria-label` including product name
- Out-of-stock / $0-price items stay published with quote CTA — never 404

### ARIA Patterns

```html
<!-- Product Card -->
<article aria-label="Product: Zira Height-Adjustable Desk">
  <img alt="Zira L-shape desk in grey laminate finish" />
  <h3>Zira Height-Adjustable Desk</h3>
  <div role="img" aria-label="4.5 out of 5 stars, 12 reviews">
    <!-- stars -->
  </div>
  <button aria-label="Request a quote for Zira Height-Adjustable Desk">
    Request a Quote
  </button>
</article>

<!-- Cart Count -->
<a href="/cart" aria-label="Cart, 3 items">
  <svg aria-hidden="true"><!-- cart icon --></svg>
  <span aria-hidden="true">3</span>
</a>
```

---

## 10. B2B-Specific Design Patterns

These patterns are unique to BBI's institutional context and should override consumer-retail defaults.

### Quote CTA (vs. Add to Cart)

Any product that is:
- Priced at `$0` or no price
- Marked as a showcase item
- Out of stock with no restock date

...must show a **"Request a Quote"** button instead of "Add to Cart." The product page stays live — it's a lead-capture page.

```
Button Label:  "Request a Quote"
Style:         Primary (black pill)
Destination:   /pages/contact?product=[handle] or modal form
```

### Manufacturer/Brand Labeling

BBI carries premium Canadian brands (Global, Teknion, ergoCentric, Keilhauer, etc.). Brand name is always shown above product name in cards:

```
Brand:    [12px, #5c5c5c, Regular]
Product:  [h4-size, #121212, heading font]
```

### Specification Tables

Products have detailed specs (dimensions, weight capacity, materials, fabrics). Tables should:
- Use clean borders (#121212 dividers)
- Be readable at small sizes (body 14px min)
- Group by category (dimensions, materials, certifications)
- Never truncate spec values

### Lead Time / Availability

Replace consumer "in stock / out of stock" with:

| Status | Label | Color |
|--------|-------|-------|
| In stock | "In Stock" | `#98ca3c` (BBI Green) |
| Ships in 2–4 weeks | "Ships in 2–4 wks" | `#ecac23` (gold) |
| Made to order | "Made to Order" | `#5c5c5c` (gray) |
| Contact for availability | "Contact Us" | `#003865` (navy link) |

### OECM / Institutional Badging

BBI is an OECM (Ontario Education Collaborative Marketplace) supplier. Products eligible for OECM pricing can show:

```
Badge:       "OECM Supplier"
Style:       #003865 background, #ffffff text
Font:        11px, Medium
```

---

## Summary

BBI's design system is built for institutional trust, not consumer impulse:

1. **Navy + Green** — `#003865` and `#98ca3c` are the two brand colors everything else anchors around
2. **Inter throughout** — Clean, legible, professional at all sizes
3. **Pill-shaped inputs and buttons** — Softens the B2B seriousness without looking retail
4. **Black-dominant primary** — Buttons and text in near-black signals quality and permanence
5. **Quote over cart** — Conversion goal is a sales conversation, not a checkout
6. **Spec-forward** — Product pages are documentation, not discovery
7. **Canadian B2B context** — OECM, lead times, institutional availability signals matter

The system supports BBI's goal of converting government buyers, school boards, and corporate procurement teams who research before they buy and need confidence, not urgency.
