# BBI Design System

**Status:** Skeleton — fill in after Claude Design session completes.
**Last updated:** 2026-04-27
**Owner:** Steve / Leo
**Maps to:** Shopify Admin → Theme settings → Colors

This is the canonical reference for visual design on brantbusinessinteriors.com. Every Liquid section, every Claude Code prompt, every dev handoff should reference this file. CLAUDE.md governs behaviour; this file governs appearance.

---

## Brand mark (locks the anchor colors)

**Logo file:** [`data/logos/bbi-logo-hires.png`](../../data/logos/bbi-logo-hires.png) (hi-res, cleaned 2026-04-27)
**Source options:** [`data/logos/options/`](../../data/logos/options/) (10 directions generated 2026-04-25)
**Cleaning script:** [`scripts/clean-bbi-logo.py`](../../scripts/clean-bbi-logo.py) (clarity-upscaler)

The lockup is horizontal: **"Brant"** in charcoal sans-serif + **"BASICS"** in red (with maple leaf accent and stylized paperclip replacing the "I"), a thin red vertical rule, then **"BUSINESS INTERIORS"** in charcoal uppercase stacked two lines.

**Hexes locked by the brand mark — these anchor the entire design system:**

| Role | Hex | Source |
|---|---|---|
| Brand red | `#D4252A` | Logo "BASICS" wordmark + vertical rule |
| Brand charcoal | `#0B0B0C` | Logo "Brant" + "BUSINESS INTERIORS" wordmarks |
| Brand white | `#FFFFFF` | Logo background |

**Lockup rules:**
- Clear space: minimum half the height of the "B" in "Brant" on all four sides
- Minimum size: 120px wide on screen, 1in (25mm) wide in print
- Always on white or near-white (#FAFAFA max). Never on red, never on photo without a white plate behind it.
- Don't recolor. Don't reflow into a stacked layout — the horizontal lockup is the only approved version.

---

## Principles (locked)

- **White-forward.** Page canvas is white. Surface tier is `#FAFAFA`–`#F7F7F8`. Never warmer than that. No beige, tan, cream, sand.
- **Brighter through neutrals, not saturation.** Lighter backgrounds + crisper borders + more whitespace. Red stays where it is, or goes slightly down.
- **Brand red is `#D4252A`** (from the logo). On white it's ~4.7:1 — borderline AA. Therefore:
  - `red-surface` = `#D4252A` exact, used on buttons/banners/badges (large surfaces).
  - `red-text` = darker variant (~`#A81E22`, TBD test) for any red text on white. Must hit AA 4.5:1.
- **Red density 5–8%** of any given screen. Reserved for action: primary CTAs, key badges, hover accents. Body links default to charcoal.
- **Anchor neutral is `#0B0B0C` charcoal** (from the logo) for headings and body text. NOT navy. Earlier proposals used navy `#1a2744` — superseded by the brand mark.
- **AA 4.5:1** for body text, 3:1 for large text and UI components. Non-negotiable.
- **No dark mode.** B2B procurement use case doesn't need it. Disabled in theme.
- **No gradients on red.** Solid colors only on action surfaces.
- **Borders over shadows** on white-forward systems. Shadows max 8% opacity, 2 levels.

---

## Color tokens

> Replace each `TBD` with the value Claude Design returns. Keep both hex and `r,g,b` triplet — `style-variables.liquid` consumes the triplet for `rgba()` math.

### Scheme: default (white canvas) — used 90% of pages

| Token | Hex | r,g,b | Contrast vs `--background` |
|---|---|---|---|
| `--background` | `#FFFFFF` | `255,255,255` | — |
| `--alternateBackground` | TBD | TBD | TBD |
| `--cardBackground` | TBD | TBD | TBD |
| `--textColor` | TBD | TBD | TBD ✓ AA |
| `--linkColor` | TBD | TBD | TBD ✓ AA |
| `--headingColor` | TBD | TBD | TBD ✓ AA |
| `--buttonBackground` *(red-surface)* | TBD | TBD | — |
| `--buttonColor` | TBD | TBD | TBD ✓ AA |
| `--buttonBorder` | TBD | TBD | — |
| `--buttonBackgroundHover` | TBD | TBD | — |
| `--alternateButtonBackground` *(navy outline)* | TBD | TBD | — |
| `--alternateButtonColor` | TBD | TBD | TBD ✓ AA |
| `--alternateButtonBorder` | TBD | TBD | — |
| `--inputBackground` | TBD | TBD | — |
| `--inputColor` | TBD | TBD | TBD ✓ AA |
| `--inputBorder` | TBD | TBD | TBD ✓ 3:1 |
| `--borderColor` | TBD | TBD | TBD ✓ 3:1 |
| `--productBorder` | TBD | TBD | TBD ✓ 3:1 |
| `--ratingStarColor` | TBD | TBD | — |
| `--shadowColor` | TBD | TBD | — |
| `--line-color` *(accent line)* | TBD | TBD | — |

### Scheme: inverse (navy canvas) — hero/feature blocks only

| Token | Hex | r,g,b | Contrast vs `--background` |
|---|---|---|---|
| `--background` | TBD | TBD | — |
| `--textColor` | `#FFFFFF` | `255,255,255` | TBD ✓ AA |
| `--headingColor` | `#FFFFFF` | `255,255,255` | TBD ✓ AA |
| `--linkColor` | TBD | TBD | TBD ✓ AA |
| `--buttonBackground` *(red-surface)* | TBD | TBD | — |
| `--buttonColor` | TBD | TBD | — |
| *(...remainder)* | TBD | TBD | TBD |

### Global tokens (set once)

| Token | Hex | r,g,b | Notes |
|---|---|---|---|
| `--success` | TBD | TBD | Green, AA on white |
| `--error` | TBD | TBD | Distinct from brand red — use a slightly oranger or darker red |
| `--saleBadgeBackground` | TBD | TBD | — |
| `--newBadgeBackground` | TBD | TBD | — |
| `--preorderBadgeBackground` | TBD | TBD | — |
| `--soldBadgeBackground` | TBD | TBD | — |
| `--customBadgeBackground` | TBD | TBD | — |
| `--headerBg` | TBD | TBD | — |
| `--headerColor` | TBD | TBD | — |
| `--headerHoverColor` | TBD | TBD | — |
| `--cartCountBg` | TBD | TBD | — |
| `--submenuBg` | TBD | TBD | — |
| `--submenuColor` | TBD | TBD | — |
| `--submenuHoverColor` | TBD | TBD | — |

---

## Typography

| Role | Font | Weight | Size (mobile) | Size (desktop) | Line-height |
|---|---|---|---|---|---|
| H0 (hero) | TBD | TBD | TBD | TBD | TBD |
| H1 | TBD | TBD | TBD | TBD | TBD |
| H2 | TBD | TBD | TBD | TBD | TBD |
| H3 | TBD | TBD | TBD | TBD | TBD |
| Body | TBD | TBD | TBD | TBD | TBD |
| Small | TBD | TBD | TBD | TBD | TBD |
| Button | TBD | TBD | TBD | TBD | TBD |

---

## Spacing, radius, shadow

**Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96 (px)

**Radius:** `--inputRadius` TBD · `--buttonRadius` TBD · `--cardRadius` TBD · `--imageRadius` TBD · `--productRadius` TBD

**Shadow:**
- `shadow-sm` — TBD (cards on white)
- `shadow-md` — TBD (modal/drawer)

---

## Components

### Buttons
- **Primary** — red-surface bg, white text. Use for the single most important action on a screen.
- **Secondary** — navy outline, navy text, white bg. Use for non-primary actions.
- **Tertiary** — text-only, navy color, no background. Use for inline links and table actions.
- All states: default, hover, focus (visible ring), active, disabled.
- Disabled state: 40% opacity AND grayscale — never just opacity (preserves contrast).

### Form inputs
- White bg, navy text, mid-gray border (3:1 against bg).
- Focus: navy 2px ring, no fill change.
- Error: red border + red helper text below + ARIA live region.

### Badges
- Five distinct colors: sale, new, preorder, sold, custom. Sale is BBI red. Sold is gray (deemphasized — these are still pages, just unbuyable). Others can use complementary cool tones — never warm.

### Product card
- White bg, light gray border (1px), no shadow at rest, subtle shadow on hover.
- Photo crops square. Title in navy. Price in body color.
- Sale/new/preorder badge top-left. Sold badge top-right (separate corner — different meaning).
- For unbuyable items (sold-out, $0-price, showcase): card shows "Request a Quote" button instead of "Add to Cart". Per BBI rule: these stay live as B2B lead-capture pages.

### Quote-request CTA block
- Standalone section variant: navy bg, white heading, red CTA button, OECM trust line below.
- Inline PDP variant: replaces add-to-cart entirely on unbuyable items. Larger button, "Request a Quote" wording, "We respond within 1 business day" microcopy below.

### Header
- White bg, navy text. Red used only for cart count badge.
- Mobile hamburger drawer uses the secondary header tokens (separate set in `style-variables.liquid`).

### Footer
- Navy bg (uses inverse scheme). White text. Red on hover for primary nav links only.

---

## Usage rules

### Red usage
- ✓ Primary CTAs (one per viewport)
- ✓ Sale badge
- ✓ Cart count badge
- ✓ Critical state (error icons — but use `--error` not `--buttonBackground`)
- ✗ Body links (use navy)
- ✗ Section backgrounds larger than ~10% of viewport
- ✗ Headings (red headings read as warning, not branding)
- ✗ Hover state for non-critical elements (use navy or border darken)

### When in doubt
- Default to navy. Red is a privilege, not a default.
- Default to no shadow. Borders carry more weight on white-forward systems.
- Default to the standard scheme. Inverse is for marketing surfaces, not utility.

---

## Implementation notes

**Where these values actually live:** Shopify Admin → Online Store → Themes → Customize → Theme settings → Colors. The values in this file are the *spec*; the live values are configured in Admin and serialized to `config/settings_data.json` (gitignored).

**Update flow:**
1. Update this file with new values.
2. Apply in Admin on a duplicate (non-live) theme.
3. Preview, screenshot.
4. Promote duplicate to live when approved.

**One-time code edits required:**
- `theme/snippets/style-variables.liquid` lines 83–154 — disable dark mode block OR replace `#ffca10` with the BBI red.
- `theme/sections/blinking-icons.liquid` line 205 — fix `#f00f00` typo.
- `theme/sections/shapes.liquid` lines 333, 339 — replace `#FFCA10` with BBI red.

See [`docs/reviews/design-system-audit-2026-04-27.md`](../reviews/design-system-audit-2026-04-27.md) for the full code audit.

---

## Changelog

- **2026-04-27** — Skeleton scaffolded. Awaiting Claude Design output to populate token values.
- **2026-04-27** — Brand mark added. Anchor hexes locked: red `#D4252A`, charcoal `#0B0B0C`. Anchor neutral shifted from navy to charcoal to follow the logo.
