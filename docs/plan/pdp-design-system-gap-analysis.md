# PDP Design System Gap Analysis
**Date:** 2026-05-10 | **Source of truth:** `Design System Zips/5 - PDP/` (ProductDetail.jsx + pdp.css + tokens.css)

---

## What the design system specifies

### Right column (`pd-product`)

The design spec defines a **sticky** right column (`position: sticky; top: 24px`) with this exact order:

1. **Brand eyebrow** — mono uppercase, 11px, 0.08em tracking. Red dash rendered via CSS `::before` pseudo-element (18px × 1px, `var(--saleBadgeBackground)`). Brand name is a clickable link to the brand page. Optionally a second line for the parent company (`pd-product__brand-parent`).
2. **H1 title** — Inter Tight 600, `clamp(28px, 3.4vw, 44px)`, -0.015em, `text-wrap: balance`.
3. **Model line** — `pd-product__model` — JetBrains Mono 12px, 0.06em tracking. Bold primary model code + "· N model variants available" separator.
4. **Badges row** — `pd-product__badges` flex row. Three badge kinds:
   - `bbi-badge--oecm` (green dot + text)
   - `bbi-badge--canadian` (MapleLeaf SVG + text)
   - `pd-badge--sold` (sold-out chip — gray #5A5A5E pill, NOT the green/red availability dot pattern)
5. **Standfirst** — `pd-product__standfirst` — 16px/1.55, `rgba(--textColor-rgb, 0.78)`, `text-wrap: pretty`. This is a **short 2–3 sentence summary written for the right column**, distinct from the full description below the fold.
6. **Commerce card** — `pd-commerce` — bordered card with `background: var(--alternateBackground)` (#FAFAFA), `border: 1px solid var(--borderColor)`, `border-radius: var(--cardRadius)`. Contains:
   - Eyebrow (red `::before` dash)
   - H2 heading ("Request a quote on this product")
   - Sub copy (14px/1.55)
   - **Primary CTA** — `bbi-btn bbi-btn--primary bbi-btn--lg` — black background (#0B0B0C), white text, 52px tall, full width. For buyable products, Add to Cart is the primary button.
   - **Secondary CTA** — `pd-commerce__secondary` — text link with underline, NOT a button. "Call 1-800-835-9565" or "Request a quote".
   - Trust line — 12px, red dot `::before`, mono.

### Description section (`pd-description`) — below fold

- `background: var(--background)` (white)
- `max-width: 640px`, centered, 32px horizontal padding
- Eyebrow — red `::before` dash, "About this chair" (product-type-specific)
- **H2 tagline** — Inter Tight 600, `var(--fs-h2)` — a punchy editorial line (e.g., "Plain-spoken ergonomics for a shift, not a showroom."). This is **not** from Shopify product data — it's a separate metafield.
- Body paragraphs — 17px/1.6 (not 16px), `rgba(--textColor-rgb, 0.82)`
- **Best for** — `pd-description__bestfor` — Inter Tight 500, 17px/1.5. Bold "BEST FOR" label in mono uppercase above the text. Separated by a `border-top: 1px solid var(--borderColor)`.

### Spec section (`pd-specs`) — below fold

- `background: var(--alternateBackground)`, bordered top + bottom
- `max-width: 1320px`
- Eyebrow + H2 in a `pd-specs__head` (max-width 640px)
- **Table structure is CSS grid divs — NOT an HTML `<table>`**. Each row is `div.pd-spec-row` with `display: grid; grid-template-columns: 28% 72%; gap: 24px`.
- `pd-specs__table` has `border-top: 1px solid var(--textColor)` — **thick dark top border**.
- Labels: JetBrains Mono 11px, uppercase, 0.08em, `rgba(--textColor-rgb, 0.6)`.
- Values: 15px/1.55, full `var(--textColor)`.
- Key Features list items render with a horizontal dash `::before` (10px × 1px, `var(--textColor)`) — not arrow `→`.
- **No `<hr>` between heading and table.** No alternating row colors. Border-bottom on each row.

### Layout / container

- Max-width: **1320px** (we're using 1200px)
- Hero grid: `grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr)` — **60/40 split**, not 50/50
- Gallery: `aspect-ratio: 4 / 5` on desktop (we're using 1:1)
- Thumb strip: `grid-template-columns: repeat(6, 1fr)` — 6 thumbs in a row, not flex-wrap

---

## What's wrong right now

| # | Issue | Design spec | Current implementation |
|---|-------|-------------|----------------------|
| **A** | Description in right column | Standfirst only (short summary, separate metafield) | Full `product.description` was rendering here — **fixed in this session** |
| **B** | Add to Cart button | `bbi-btn--primary` (black #0B0B0C, 52px) | Was `pdp-btn--outline` (transparent/white) — **fixed in this session** |
| **C** | Eyebrow red mark | CSS `::before` pseudo (18px × 1px red line) | HTML `<span aria-hidden="true">—</span>` with inline color |
| **D** | Commerce card background | `var(--alternateBackground)` = #FAFAFA | `var(--background)` = white (invisible card) |
| **E** | Description H2 tagline | Punchy editorial H2 above body paragraphs | Not present — we go straight to body copy |
| **F** | Description body size | 17px / 1.6 | 16px / 1.7 |
| **G** | Description max-width | 640px | 760px |
| **H** | Spec table structure | CSS grid divs (`pd-spec-row`) | HTML `<table>` with `<th>`/`<td>` |
| **I** | Spec table top border | `border-top: 1px solid var(--textColor)` (dark, strong) | `border-top: 1px solid var(--borderColor)` on `<hr>` |
| **J** | Key Features list marker | Horizontal dash `::before` (10px × 1px) | Standard `<ul>` `<li>` with default browser bullets |
| **K** | Container max-width | 1320px | 1200px |
| **L** | Hero grid split | 1.5fr / 1fr (60/40) | 1.1fr / 0.9fr (~55/45) |
| **M** | Gallery aspect ratio | 4:5 desktop, 1:1 mobile | 1:1 always |
| **N** | Right column sticky | `position: sticky; top: 24px` | Not sticky |
| **O** | Sold-out badge | `pd-badge--sold` (gray pill, #5A5A5E) | Green/red dot availability badge |
| **P** | Product names | Display in `pd-product__eyebrow` pattern | Same — no change from our commits. **Possible pre-existing issue; unrelated to PDP restructure.** |

---

## How to fix — priority order

### Immediate (already fixed in this session)
- **A** — Description removed from right column ✅
- **B** — ATC button restored to black primary ✅

### Fix group 1 — Right column typography + commerce card (1 commit)
1. Replace HTML `<span>—</span>` eyebrow pattern with CSS `::before` on `.pdp-section-eyebrow`
2. Apply `background: var(--alternateBackground)` to `.pdp-quote-card`
3. Add `position: sticky; top: 24px` to `.pdp-info`
4. Add `standfirst` support: read `product.metafields.specs.standfirst.value` and render as `pd-product__standfirst` if present. If absent, leave blank (description is below the fold — no fallback to full description in the right column).
5. Sold-out badge: switch to gray pill style matching `pd-badge--sold` spec (#5A5A5E, white text).

### Fix group 2 — Below-fold description section (1 commit)
1. Add H2 tagline from metafield `product.metafields.specs.tagline.value` (skip heading if blank — most products won't have it yet).
2. Body paragraphs: 17px / 1.6 (update `.pdp-about__body p`).
3. Max-width: 640px (update `.pdp-about__inner`).
4. Eyebrow: switch to `::before` CSS dash pattern (matches all other eyebrows on the page).
5. "Best for" label: switch from current two-`<p>` approach to the `pd-description__bestfor` pattern (bold block mono label + text inline).

### Fix group 3 — Spec table → CSS grid divs (1 commit)
1. Replace `<table>` / `<th>` / `<td>` structure with `div.pd-spec-row` grid layout.
2. `pd-specs__table` gets `border-top: 1px solid var(--textColor)` (strong dark top rule).
3. Remove `<hr>` separator between heading and table.
4. Key Features list items: replace bullet with dash `::before` pattern.
5. Spec section eyebrow: switch to `::before` CSS dash.

### Fix group 4 — Layout / container (1 commit)
1. Max-width: 1200px → 1320px throughout.
2. Hero grid: `1.5fr 1fr` split.
3. Gallery: `aspect-ratio: 4 / 5` on desktop.
4. Thumb strip: `repeat(6, 1fr)` grid.

### Metafield requirements
Two new optional metafields in the `specs` namespace needed before Fix groups 1 + 2 are useful:
- `specs.standfirst` — 1–3 sentence editorial summary for the right column
- `specs.tagline` — punchy H2 for the description section

These can be added to the Shopify admin metafield definitions and populated for Hero 100 products. The PDP handles absent values gracefully (both sections hide their respective elements).

---

## Product name change — investigation needed
Our three commits only modified `theme/sections/ds-pdp-base.liquid`. No product data, no scripts, no snippets were changed by us. The most likely cause is PE-3 (title normalization script, commit `57d99f3`) which ran earlier and stripped ™/® characters from 588 products. If names look different now, that was pre-existing. **Action:** compare a specific product title now vs. the `data/exports/` snapshot to confirm.
