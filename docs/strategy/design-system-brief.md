# Claude Design Constraint Brief — BBI Design System Rebuild

**Paste this entire document into Claude Design at claude.ai/design as the opening message of a new chat.**
**Then attach 3–5 screenshots of the current live brantbusinessinteriors.com (homepage, PDP, collection, header, footer).**

---

## Project

I'm rebuilding the design system for **Brant Business Interiors (BBI)** — a Canadian B2B office furniture dealer. The site runs on Shopify (a heavily customized purchased theme). Audience is institutional procurement: school boards, hospitals, municipalities. We are an OECM-verified supplier (matters for trust signaling). Live site: https://www.brantbusinessinteriors.com

I want a complete design system: **tokens first, then components, then 3 reference screens.** Output everything as CSS custom properties named to match the Shopify token names listed at the bottom of this brief, so the dev handoff is a 1:1 mapping into Shopify Admin → Theme settings → Colors.

---

## Constraints (these override anything else)

### Color direction
- **No beige. No warm tones. No tan/cream/sand.** The current site has beige sections — we are eliminating them.
- **White-forward.** Page canvas is `#FFFFFF`. Surface tier is `#FAFAFA` or `#F7F7F8` for cards/sections. Avoid going warmer than that.
- **Brighter overall** — but brighter means *lighter neutrals + more whitespace + crisper borders*, NOT crank the saturation on red.
- **Brand color is RED** (BBI red, approximately `#C8102E` — propose a refined value). **Two reds required:**
  - `red-surface` — for buttons, banners, badges (large surfaces). Can sit at lower contrast against white.
  - `red-text` — about 12–18% darker, for any red text on white. Must hit AA 4.5:1.
- **Anchor neutral:** deep navy or charcoal for headings/body text. I currently use `#1a2744` — propose either keeping or shifting to a slightly cooler `#0F1A33`.
- **Red density rule:** red should appear on roughly 5–8% of any given screen. Primary CTAs, key badges, hover accents only. Body links should default to navy, not red. Reserve red for action.

### Accessibility
- All body text on background = AA 4.5:1 minimum
- Large text (18pt+ or 14pt+ bold) = 3:1 minimum
- UI components and graphic borders = 3:1 minimum
- Focus rings must be visible against white surface (don't use white-on-white focus)
- Output the contrast ratio for every text/bg and ui/border token pair

### Typography
- Already using Shopify font_picker for body and heading. Propose a sans for UI (Inter, Source Sans, or your call) and an optional display for H1/hero only.
- 6–7 size steps with line-heights. Mobile and desktop scales separately.
- Heading line-height tighter than body line-height.

### Spacing, radius, shadow
- 4px base spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96
- Radius: 4px / 8px / pill — no more
- Shadow: 2 levels max. Prefer borders over shadows on white-forward systems.

---

## Audience and tone

- B2B Canadian institutional buyers (school boards, hospitals, municipalities)
- They are reviewing this on a desktop in an office, often on Internet Explorer / Edge / mid-tier hardware
- Trust > delight. Clean > clever. Professional, calm, confident. Think Steelcase, Knoll, Herman Miller institutional pages — not D2C lifestyle brand.
- OECM partnership is a key differentiator — surface it as a quiet trust badge, never loud

---

## What to produce, in this order

### Phase 1 — Tokens
Output a single block of CSS custom properties with two named color schemes:
- **`scheme-default`** (white canvas, navy text, red accent) — used on 90% of pages
- **`scheme-inverse`** (navy canvas, white text, red accent) — used on hero/feature blocks only

For each scheme, output values for every token name listed in the **Token Map** at the bottom. Include hex AND `r,g,b` triplet (the theme uses both formats). Show contrast ratio after each color pair (e.g. `--text on --background = 12.6:1 ✓ AA`).

Also output: typography scale, spacing scale, radius scale, shadow scale.

### Phase 2 — Components
Build, in order:
1. Buttons — primary (red), secondary (navy outline), tertiary (text-only). All states: default, hover, focus, active, disabled.
2. Form inputs — text, select, textarea, checkbox, radio. All states.
3. Cards — basic, product, feature.
4. Badges — sale, new, preorder, sold, custom (5 distinct).
5. Header — desktop + mobile hamburger.
6. Footer.
7. Product card — most-exposed pattern, gets red badge treatment.
8. **Quote-request CTA block** — this is BBI's primary conversion pattern. Unbuyable items (sold-out, $0-price, showcase) keep their page with a "Request a Quote" button instead of "Add to Cart."

For each component, show all states side-by-side and the focus ring against white.

### Phase 3 — Reference screens
Build three screens at 1440px desktop:
1. **Homepage** — hero with red CTA, value prop band, featured collections (4-up), OECM trust strip, testimonial, footer.
2. **PDP (unbuyable)** — product image gallery, title, OECM badge, "Request a Quote" CTA (no price/cart), spec table, related products.
3. **Collection** — filter sidebar (left), product grid (right), pagination.

Each screen: render at 1440px and 375px (mobile).

### Phase 4 — Audits
- **Red density audit:** highlight every red pixel on each reference screen. Confirm 5–8% target.
- **Contrast audit:** table of every text/bg pair across the three screens with AA pass/fail.
- **Token coverage audit:** confirm every token in the Token Map below has a defined value.

---

## Token Map (must define values for every entry)

Output as `--token-name: #hex; /* r,g,b */`.

### Per-scheme tokens (define for both `scheme-default` and `scheme-inverse`)
```
--background
--alternateBackground
--cardBackground
--textColor
--linkColor
--headingColor
--buttonBackground
--buttonColor
--buttonBorder
--buttonBackgroundHover
--buttonColorHover
--buttonBorderHover
--alternateButtonBackground
--alternateButtonColor
--alternateButtonBorder
--alternateButtonBackgroundHover
--alternateButtonColorHover
--alternateButtonBorderHover
--inputBackground
--inputColor
--inputBorder
--productBorder
--borderColor
--ratingStarColor
--sliderArrowBackground
--sliderArrowColor
--cardBackground
--shadowColor
--productIconColor
--productIconBg
--line-color   /* highlight/accent line */
```

### Global tokens (define once)
```
--success
--error
--saleBadgeBackground
--newBadgeBackground
--preorderBadgeBackground
--soldBadgeBackground
--customBadgeBackground
--headerBg
--headerColor
--headerHoverColor
--headerIconColor
--cartCountBg
--cartCountColor
--submenuBg
--submenuColor
--submenuHoverColor
```

### Typography
```
--bodyFont, --bodyFontWeight, --bodyFontLineHeight, --bodyFontBase
--headingFont, --headingFontWeight, --headingFontLineHeight, --headingFontBase
```

### Radius
```
--cardRadius, --imageRadius, --productRadius, --inputRadius, --buttonRadius
```

---

## What to avoid

- Don't propose adding new tokens — Shopify's settings schema only accepts the names above.
- Don't suggest dark mode variants — we will disable dark mode for B2B.
- Don't introduce gradients on red surfaces (B2B procurement = solid colors only).
- Don't use red as a body link color.
- Don't use shadows heavier than 8% opacity.
- Don't put text on photo backgrounds without a tested overlay.

---

## Deliverable format

When you're done, give me:
1. A single CSS file with all tokens, named `bbi-design-system-v1.css`
2. A markdown spec sheet listing every component with usage rules
3. Three PNG exports of the reference screens (desktop + mobile each)
4. The audit tables (red density, contrast, token coverage)

Ready when you are.
