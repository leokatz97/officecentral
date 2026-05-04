# BBI Design System

**Status:** v1 — DS-1 complete. All token values locked from Claude Design T4/T5 screens.
**Last updated:** 2026-05-04
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
  - `red-text` = darker variant `#A81E22` (confirmed 5.88:1 AA on white ✓) for any red text on white. Must hit AA 4.5:1.
- **Red density 5–8%** of any given screen. Reserved for action: primary CTAs, key badges, hover accents. Body links default to charcoal.
- **Anchor neutral is `#0B0B0C` charcoal** (from the logo) for headings and body text. NOT navy. Earlier proposals used navy `#1a2744` — superseded by the brand mark.
- **AA 4.5:1** for body text, 3:1 for large text and UI components. Non-negotiable.
- **No dark mode.** B2B procurement use case doesn't need it. Disabled in theme.
- **No gradients on red.** Solid colors only on action surfaces.
- **Borders over shadows** on white-forward systems. Shadows max 8% opacity, 2 levels.

---

## Color tokens

> Values confirmed from Claude Design T4/T5 locked screens (2026-05-04). Keep both hex and `r,g,b` triplet — `style-variables.liquid` consumes the triplet for `rgba()` math.

### Scheme: default (white canvas) — used 90% of pages

| Token | Hex | r,g,b | Contrast vs `--background` |
|---|---|---|---|
| `--background` | `#FFFFFF` | `255,255,255` | — |
| `--alternateBackground` | `#FAFAFA` | `250,250,250` | 18.87 : 1 AAA |
| `--cardBackground` | `#FFFFFF` | `255,255,255` | — |
| `--textColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--linkColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--headingColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--buttonBackground` *(charcoal solid, red on hover)* | `#0B0B0C` | `11,11,12` | — |
| `--buttonColor` | `#FFFFFF` | `255,255,255` | 20.10 : 1 AAA on charcoal |
| `--buttonBorder` | `#0B0B0C` | `11,11,12` | — |
| `--buttonBackgroundHover` | `#D4252A` | `212,37,42` | — |
| `--alternateButtonBackground` *(secondary outline)* | `#FFFFFF` | `255,255,255` | — |
| `--alternateButtonColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--alternateButtonBorder` | `#0B0B0C` | `11,11,12` | — |
| `--inputBackground` | `#FFFFFF` | `255,255,255` | — |
| `--inputColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--inputBorder` | `#0B0B0C` | `11,11,12` | 20.10 : 1 (high-trust procurement form treatment — full ink border) |
| `--borderColor` | `#E5E5E7` | `229,229,231` | 1.22 : 1 (decorative hairline — intentionally low; focus rings use `--textColor`) |
| `--productBorder` | `#E5E5E7` | `229,229,231` | 1.22 : 1 (decorative) |
| `--ratingStarColor` | `#0B0B0C` | `11,11,12` | — |
| `--shadowColor` | `#0B0B0C` | `11,11,12` | — |
| `--line-color` *(accent line / divider)* | `#E5E5E7` | `229,229,231` | — |

### Scheme: inverse (charcoal canvas) — hero/feature blocks only

| Token | Hex | r,g,b | Contrast vs `--background` |
|---|---|---|---|
| `--background` | `#0B0B0C` | `11,11,12` | — |
| `--alternateBackground` | `#161618` | `22,22,24` | — |
| `--cardBackground` | `#161618` | `22,22,24` | — |
| `--textColor` | `#FFFFFF` | `255,255,255` | 20.10 : 1 AAA |
| `--headingColor` | `#FFFFFF` | `255,255,255` | 20.10 : 1 AAA |
| `--linkColor` | `#FFFFFF` | `255,255,255` | 20.10 : 1 AAA *(NEVER `#A81E22` on inverse — only 2.32:1, fails)* |
| `--buttonBackground` *(white solid, red on hover)* | `#FFFFFF` | `255,255,255` | — |
| `--buttonColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA on white |
| `--buttonBorder` | `#FFFFFF` | `255,255,255` | — |
| `--buttonBackgroundHover` | `#D4252A` | `212,37,42` | 4.83 : 1 AA vs charcoal canvas |
| `--alternateButtonBackground` | `transparent` | `11,11,12` *(effective canvas)* | — |
| `--alternateButtonColor` | `#FFFFFF` | `255,255,255` | 20.10 : 1 AAA |
| `--alternateButtonBorder` | `#FFFFFF` | `255,255,255` | — |
| `--inputBackground` | `#161618` | `22,22,24` | — |
| `--inputColor` | `#FFFFFF` | `255,255,255` | 18.41 : 1 AAA on plate |
| `--inputBorder` | `#FFFFFF` | `255,255,255` | 20.10 : 1 vs canvas |
| `--borderColor` | `#1F1F21` | `31,31,33` | 1.17 : 1 (symmetric to default hairline) |
| `--productBorder` | `#1F1F21` | `31,31,33` | 1.17 : 1 (decorative) |
| `--ratingStarColor` | `#FFFFFF` | `255,255,255` | — |
| `--shadowColor` | `#000000` | `0,0,0` | — |
| `--line-color` | `#1F1F21` | `31,31,33` | — |

### Global tokens (set once — scheme-independent)

| Token | Hex | r,g,b | Notes |
|---|---|---|---|
| `--success` | `#1F6F3F` | `31,111,63` | 6.04 : 1 AA on white |
| `--error` | `#B33A1A` | `179,58,26` | 5.93 : 1 AA on white · 11° hue shift from brand red — distinct from branding |
| `--warningBackground` | `#E8A317` | `232,163,23` | 7.71 : 1 AA · low-stock badge — ink label |
| `--saleBadgeBackground` | `#D4252A` | `212,37,42` | White label, AA-large |
| `--newBadgeBackground` | `#0B0B0C` | `11,11,12` | White label, AAA |
| `--preorderBadgeBackground` | `#FFFFFF` | `255,255,255` | Outlined variant — ink label |
| `--soldBadgeBackground` | `#5A5A5E` | `90,90,94` | 6.74 : 1 AA · white label · deemphasized (still a lead-capture page) |
| `--customBadgeBackground` | `#FAFAFA` | `250,250,250` | Ink label on surface |
| `--headerBg` | `#FFFFFF` | `255,255,255` | — |
| `--headerColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--headerHoverColor` | `#A81E22` | `168,30,34` | 5.88 : 1 AA · hover only, never default |
| `--cartCountBg` | `#D4252A` | `212,37,42` | Numerals bold ≥ 11px → AA-large |
| `--cartCountColor` | `#FFFFFF` | `255,255,255` | — |
| `--submenuBg` | `#FFFFFF` | `255,255,255` | — |
| `--submenuColor` | `#0B0B0C` | `11,11,12` | 20.10 : 1 AAA |
| `--submenuHoverColor` | `#A81E22` | `168,30,34` | 5.88 : 1 AA |

---

## Typography

| Role | Font | Weight | Size (mobile) | Size (desktop) | Line-height |
|---|---|---|---|---|---|
| H0 (hero) | Inter Tight | 600 | 44px | 72px | 1.05 / 1.0 |
| H1 | Inter Tight | 600 | 32px | 48px | 1.1 / 1.05 |
| H2 | Inter Tight | 600 | 24px | 32px | 1.15 / 1.1 |
| H3 | Inter Tight | 600 | 18px | 22px | 1.25 / 1.2 |
| Body | Inter | 400 | 16px | 16px | 1.55 |
| Small | Inter | 400 | 13px | 14px | 1.5 |
| Button | Inter | 600 | 15px | 15px | 1 |

**Fallback stack:** `"Inter Tight", "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`  
**Letter-spacing:** H0 `−0.02em` · H1 `−0.015em` · H2 `−0.01em` · H3 `−0.005em` · body/small `0` · button `+0.01em`  
**Google Fonts load:** `Inter` (wght 400;500;600;700) + `JetBrains Mono` (wght 400;500) for mono eyebrows

---

## Spacing, radius, shadow

**Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96 (px)

**Radius:** `--inputRadius` 4px · `--buttonRadius` 4px · `--cardRadius` 8px · `--imageRadius` 4px · `--productRadius` 8px

**Shadow:**
- `shadow-sm` — `0 1px 2px rgba(11,11,12,0.04), 0 2px 8px rgba(11,11,12,0.05)` (cards on white)
- `shadow-md` — `0 2px 4px rgba(11,11,12,0.05), 0 12px 32px rgba(11,11,12,0.08)` (modal/drawer)

---

## Components

### Buttons
- **Primary** — charcoal bg (`#0B0B0C`), white text. Hover: red bg (`#D4252A`). Use for the single most important action on a screen.
- **Secondary** — charcoal outline, charcoal text, white bg. Hover: charcoal invert. Use for non-primary actions.
- **Tertiary** — text-only, charcoal color, no background. Use for inline links and table actions.
- All states: default, hover, focus (visible 2px outline in `--textColor`), active, disabled.
- Disabled state: 40% opacity AND grayscale — never just opacity (preserves contrast).

### Form inputs
- White bg, charcoal text, full-ink charcoal border (high-trust procurement treatment — `#0B0B0C` 1px solid).
- Focus: 2px outline in `--textColor`, 2px offset. No fill change.
- Error: red border + red helper text below + ARIA live region.

### Badges
- Five distinct surfaces: sale (`#D4252A` red), new (`#0B0B0C` charcoal), preorder (white outlined), sold (`#5A5A5E` gray), custom (`#FAFAFA` surface).
- Sold is gray — deemphasized intentionally. Sold-out pages stay live as B2B lead-capture; the badge signals "quote, don't cart" not "ignore this product."

### Product card
- White bg, `#E5E5E7` border (1px), no shadow at rest, `shadow-sm` on hover.
- Photo crops square. Title in charcoal. Price in body color.
- Sale/new/preorder badge top-left. Sold badge top-right (separate corner — different meaning).
- For unbuyable items (sold-out, $0-price, showcase): card shows "Request a Quote" button instead of "Add to Cart". Per BBI rule: these stay live as B2B lead-capture pages.

### Quote-request CTA block
- Standalone section variant: charcoal canvas (`.scheme-inverse`), white heading, white primary CTA (red on hover), OECM trust line below.
- Inline PDP variant: replaces add-to-cart entirely on unbuyable items. Larger button, "Request a Quote" wording, "We respond within 1 business day" microcopy below.

### Header
- White bg, charcoal text. Red used for cart count badge and nav link hover only.
- Mobile: phone icon + number + hamburger. Nav drawer uses same charcoal tokens.

### Footer
- Charcoal canvas (`.scheme-inverse`). White text. Link hover: white (red-text `#A81E22` fails 2.32:1 on charcoal — never use). Maple leaf brand plate in lower-right.

---

## Usage rules

### Red usage
- ✓ Primary CTAs — hover surface (`--buttonBackgroundHover`)
- ✓ Sale badge surface (`--saleBadgeBackground`)
- ✓ Cart count badge surface (`--cartCountBg`)
- ✓ Eyebrow ticks, OECM dots, maple-leaf badge marks (small accent use)
- ✓ Critical state icons — use `--error` (`#B33A1A`), not `--saleBadgeBackground`
- ✗ Body links (use charcoal with underline)
- ✗ Section backgrounds larger than ~10% of viewport
- ✗ Headings (red headings read as warning, not branding)
- ✗ Hover state on inverse canvas (`#A81E22` = 2.32:1 on `#0B0B0C` — fails)

### When in doubt
- Default to charcoal. Red is a privilege, not a default.
- Default to no shadow. Borders carry more weight on white-forward systems.
- Default to the standard scheme. Inverse is for marketing surfaces, not utility.

---

## Implementation notes

**Where these values actually live:** Shopify Admin → Online Store → Themes → Customize → Theme settings → Colors. The values in this file are the *spec*; the live values are configured in Admin and serialized to `config/settings_data.json` (gitignored).

**Update flow:**
1. Update this file with new values.
2. Apply in Admin on BBI Landing Dev theme (`186373570873`) — never on live.
3. Preview, screenshot.
4. Promote duplicate to live when approved.

**One-time code edits required (DS-3):**
- `theme/snippets/style-variables.liquid` lines 83–154 + 301–334 — delete dark-mode block.
- `theme/sections/blinking-icons.liquid` line 205 — replace `#f00f00` → `#D4252A`.
- `theme/sections/shapes.liquid` lines 333, 339 — replace `#FFCA10` → `#D4252A`.

See [`docs/reviews/design-system-audit-2026-04-27.md`](../reviews/design-system-audit-2026-04-27.md) for the full code audit.

---

## Changelog

- **2026-04-27** — Skeleton scaffolded. Awaiting Claude Design output to populate token values.
- **2026-04-27** — Brand mark added. Anchor hexes locked: red `#D4252A`, charcoal `#0B0B0C`. Anchor neutral shifted from navy to charcoal to follow the logo.
- **2026-05-04** — DS-1 complete. All placeholder values filled from Claude Design T4/T5 locked screens. Inverse scheme expanded to full token set. Typography scale and radius/shadow values filled. "Navy" labels corrected to "charcoal" throughout.
