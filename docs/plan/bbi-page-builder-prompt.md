# BBI Page Builder — Context Brief

Paste this entire document into a new Claude Code session to bring it fully up to speed on the BBI page building system. Attach the files listed at the bottom alongside this prompt.

---

## What you are building

You are Claude Code, working on the **Brant Business Interiors (BBI)** Shopify store. Your job is to build web pages that exactly match a locked design system. Pages are built as self-contained HTML files in `previews/`, previewed in-browser, then converted to Shopify Liquid.

**You build pages entirely in Claude Code.** No Claude Design. No external tools. You read the design system source files, write HTML, preview it with the preview tools, iterate until it matches, then convert to Shopify.

---

## Business context

- **Store:** office-central-online.myshopify.com ("BBI Landing Dev" theme, ID 186373570873 — draft only, never publish)
- **Business:** Brant Business Interiors — B2B institutional Canadian furniture dealer
- **Buyers:** Ontario school boards, hospitals, municipalities, non-profits. Everything is quote-based — no cart, no checkout.
- **Key differentiator:** OECM Supplier Partner (Agreement 2025-470) — Ontario institutions can purchase without open tender
- **Phone:** 1-800-835-9565 | **Address:** 295 George St N, Peterborough ON | **Email:** info@brantbusinessinteriors.com
- **Brand name rule:** Always "Brant Business Interiors" in customer copy — NEVER abbreviate to "BBI"

---

## Design system — the only sources you trust

All canonical design system files live in **`Design System Zips/5 - PDP/src/`**. Read them before writing any HTML. Never invent class names or token names — if it's not in these files, it doesn't go on the page.

### Shared (every page):
| File | What it contains |
|---|---|
| `src/tokens.css` | All CSS custom properties (`--background`, `--saleBadgeBackground`, `--headingFont`, etc.) |
| `src/bbi-components.css` | All shared classes: `.bbi-btn`, `.bbi-mono`, `.bbi-section`, `.bbi-container`, `.bbi-section-head`, `.bbi-card--collection`, `.bbi-card--product`, `.bbi-badge--oecm`, `.bbi-ph`, `.bbi-cta-section`, header, footer |

### Per page type:
| Page type | JSX template | CSS file | Class prefix |
|---|---|---|---|
| Homepage | `src/Homepage.jsx` | `src/homepage.css` | `.hp-*` |
| Landing pages (OECM, industries, brands, services, about) | `src/Landing.jsx` | `src/landing.css` | `.lp-*` |
| PDP — product detail (unbuyable + buyable) | `src/ProductDetail.jsx` | `src/pdp.css` | `.pd-*` |
| Collection category | `src/CollectionCategory.jsx` | `src/collection-category.css` | (check file) |
| Collection / sub-collection | `src/Collection.jsx` | `src/collection.css` | (check file) |

**Visual reference:** `Design System Zips/5 - PDP/BBI Templates Bundle.html` — all templates rendered, attached as a file. Use it to verify your output looks right.

---

## Token rules (locked — do not relitigate)

- **Red surface:** `#D4252A` → `var(--saleBadgeBackground)` — buttons, badges, accents ONLY
- **Red hover:** `#A81E22` → `var(--headerHoverColor)`
- **Charcoal:** `#0B0B0C` → `var(--textColor)` / `var(--headingColor)` — all headings and body
- **Canvas:** `#FFFFFF` → `var(--background)` — primary page background
- **Surface:** `#FAFAFA` → `var(--cardBackground)` — card backgrounds
- **No beige, tan, cream, sand, warm tones. No dark mode. No gradients on red. No red headings. No red body links.**
- **Red density:** 5–8% per screen. Eyeball it per section.

**Two schemes:**
- `scheme-default` — white canvas (90% of pages)
- `scheme-inverse` — charcoal canvas (CTA closer band only: `.bbi-cta-section.scheme-inverse`)

---

## Header — locked constants (every page)

```html
<!-- Logo -->
<img src="../Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png"
     alt="Brant Business Interiors" height="36" style="height:36px;width:auto;">

<!-- Nav labels (exact — do not change) -->
Shop | Brands | Verticals | Our work | Services | About

<!-- Header right -->
<a href="tel:18008359565">Call 1-800-835-9565</a>
<a class="bbi-btn bbi-btn--primary">Request a Quote</a>  <!-- CHARCOAL, never red -->
```

Header height: 72px. Inner max-width: 1320px, padding: 0 32px.

---

## Section rhythm (every body section except OECMBar)

```html
<section class="bbi-section">      <!-- padding: 96px 0 -->
  <div class="bbi-container">     <!-- max-width: 1320px; padding: 0 32px; margin: 0 auto -->
    ...
  </div>
</section>
```

Every section head eyebrow gets a red rule prefix via CSS:
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

## Page section structures

### Homepage
Read `src/Homepage.jsx` for exact component tree. Section order:

1. Header
2. Hero (`.hp-hero`) — 2-col grid, red primary CTA only here (`.hp-hero__cta-red`), eyebrow = red dot + 70% opacity mono text
3. ShopEntry (`.hp-shop__tiles`) — 4 × `.bbi-card--collection` (4:3 overlay tiles)
4. FeaturedProducts (`.hp-products__grid`) — 3 × `.bbi-card--product` (16:9 image at top, always)
5. OECMBar (`.hp-oecm`) — full-width band, no `.bbi-section` wrapper
6. Industries (`.hp-industries__grid`) — 5 × `.hp-industry` (1:1 square, mono numbers 01–05)
7. Services (`.hp-services__grid`) — 3 × `.hp-service` (mono red numbers, bullet list)
8. Testimonials (`.hp-work__grid`) — blockquote card + 3 × `.hp-case` (200px thumb)
9. Footer
**No CTA band on homepage** — goes straight Testimonials → Footer.

### Landing pages (OECM / industries / brands / services / about)
Read `src/Landing.jsx` for exact component tree. The Landing component is data-driven — one template renders all landing pages. Section order:

1. Header
2. Breadcrumbs (`.lp-crumbs-band`)
3. Hero (`.lp-hero`) — 2-col grid, standfirst, optional badge
4. Intro (`.lp-intro`) — body copy, inline CTA
5. Differentiators (`.lp-diff`) — 4-card grid, mono numbers, icons
6. Trust photos (`.lp-trust-row`) — 3 project photo tiles (conditional — omit if no photos)
7. Proof bar (`.lp-proof-bar`) — 3 stat numbers (conditional)
8. Crosslinks (`.lp-crosslinks`) — category links with icons (conditional)
9. OECM bar (conditional)
10. FAQ (`.lp-faq`) — accordion
11. Closer (`.bbi-cta-section.scheme-inverse`) — charcoal CTA band, shared component
12. Footer

### PDP — Product Detail Page
Read `src/ProductDetail.jsx` for exact component tree. Section order:

1. Header
2. Breadcrumbs (`.pd-crumb-band`)
3. Hero (`.pd-hero`) — gallery 60% (4:5 main + 6-col thumb strip) + commerce panel 40%
   - Unbuyable: quote CTA panel (`.pd-commerce`) — "Request a quote" primary, phone secondary
   - Buyable: add-to-cart panel (`.pd-commerce--buyable`)
4. Description (`.pd-description`)
5. Specs (`.pd-specs`) — table rows (conditional)
6. Variants (`.pd-variants`) — (conditional)
7. OECM bar
8. Related products (`.pd-related`) — (conditional)
9. Brand block (`.pd-brand-block`) — (conditional)
10. Closer (`.bbi-cta-section.scheme-inverse`)
11. Footer

---

## Image placeholders

Use `.bbi-ph` for all image slots where a real image isn't available:

```html
<div class="bbi-ph" style="aspect-ratio: 16/9;">
  <span class="bbi-ph__label">Description of what goes here</span>
</div>
```

CSS (in `bbi-components.css` — do not rewrite):
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
```

---

## Copy voice rules

- **Tone:** B2B institutional. Outcome-focused. No fluff. No emoji on the site.
- **Hook:** Bold opening statement — what the buyer gets, not what BBI does
- **Phone CTA:** Always "Call 1-800-835-9565" — full number, never "Call us"
- **Quote CTA:** Always "Request a Quote" — never "Get a Quote", "Get Pricing", "Contact Sales"
- **Form submit:** "Send request" — never "Submit"
- **OECM:** State as fact in first 200 words — "OECM Supplier Partner, Agreement 2025-470"
- **Canadian:** Add 🍁 maple leaf icon adjacent to every "Canadian-owned" or "Canadian-made" claim
- **Forbidden words:** "innovative", "cutting-edge", "synergy", "solutions", "world-class"
- **Brand name:** "Brant Business Interiors" in full — never "BBI" in customer copy

---

## How to build a page (the workflow)

When asked to build a page, always follow this sequence:

### Step 1 — Identify page type and read sources
1. Determine which template applies (Homepage / Landing / PDP / Collection category / Collection)
2. Read `src/tokens.css` in full
3. Read `src/bbi-components.css` in full
4. Read the JSX template for this page type — this defines section order
5. Read the page-specific CSS for this page type

### Step 2 — Write the HTML file
Output to `previews/{slug}-draft-v1.html`. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[SEO title]</title>
  <meta name="description" content="[meta description]">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* 1. Full contents of tokens.css */
    /* 2. Full contents of bbi-components.css */
    /* 3. Full contents of page-specific CSS */
    /* 4. Any remaining layout rules */
  </style>
</head>
<body class="scheme-default">
  <!-- sections per JSX template order -->
</body>
</html>
```

### Step 3 — Preview and iterate
```
preview_start previews/{slug}-draft-v1.html
preview_screenshot
preview_console_logs
preview_resize 375 812   ← mobile check
preview_screenshot
```

Fix any issues. Check against `BBI Templates Bundle.html` visually. Take a 1440px final screenshot for approval.

### Step 4 — Convert to Shopify
For Type A (landing pages, OECM, services): emit JSON template + `ds-*` Liquid section blocks.
For Type B (homepage, collection, PDP): identify which Starlite sections match the design output.

---

## Trust signal placement

| Signal | Where it goes | Never |
|---|---|---|
| Phone `1-800-835-9565` | Header (always) + 1 in-body CTA | Buried in body paragraphs |
| OECM Agreement 2025-470 | Trust row or hero sub on institutional pages | Marketing-claim phrasing |
| Canadian-owned + 🍁 | Footer (always), hero sub on brand/industry pages | Product cards, mid-paragraph |
| "Request a Quote" CTA | Primary CTA on every page | "Add to cart" on any BBI page |

---

## Red density checklist (run per section)

Red (`#D4252A`) appears ONLY on:
- Hero primary CTA button (homepage only: `.hp-hero__cta-red`)
- Section head eyebrow `::before` rule
- OECM badge accent
- Service/differentiator mono numbers
- Testimonial quotation mark SVG
- Notification dots / active indicators

Red must NOT appear on: headings, body text, nav links, card backgrounds, header CTA button, footer.

---

## What files are attached to this prompt

Paste/attach all of the following in the same message as this prompt:

### Paste as text (copy file contents):
1. `Design System Zips/5 - PDP/src/tokens.css`
2. `Design System Zips/5 - PDP/src/bbi-components.css`
3. `Design System Zips/5 - PDP/src/Landing.jsx`
4. `Design System Zips/5 - PDP/src/landing.css`
5. `Design System Zips/5 - PDP/src/ProductDetail.jsx`
6. `Design System Zips/5 - PDP/src/pdp.css`
7. `Design System Zips/5 - PDP/src/Homepage.jsx`
8. `Design System Zips/5 - PDP/src/homepage.css`
9. `docs/strategy/icp.md` (voice + copy rules)

### Attach as files:
10. `Design System Zips/5 - PDP/BBI Templates Bundle.html` — rendered visual reference for all templates
11. `Design System Zips/5 - Landing Page (2)/uploads/15-ANTI-REF-homepage.png` — homepage layout reference
12. `Design System Zips/5 - Landing Page (2)/uploads/16-ANTI-REF-nav.png` — header/nav exact reference
13. `Design System Zips/5 - Landing Page (2)/uploads/14-bbi-logo-v2.png` — correct logo file

### Optional (for Shopify conversion context):
14. `docs/plan/shopify-fix-plan.md` (current task list)
15. `docs/plan/site-architecture-2026-04-25.md` (page/URL structure)

---

## After pasting this prompt

Tell Claude: **"Build me the [page name] page"** and it will:
1. Confirm it has read the design system sources
2. Identify the correct template (Landing / PDP / Homepage / etc.)
3. Write `previews/{slug}-draft-v1.html`
4. Preview it and share a screenshot
5. Wait for your approval before converting to Shopify
