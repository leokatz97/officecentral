# Design System Audit — Pre-Rebuild

**Date:** 2026-04-27
**Scope:** Brant Business Interiors Shopify theme
**Repo:** [leokatz97/officecentral](https://github.com/leokatz97/officecentral) · branch `main`
**Prompt:** "No more beige. Use white instead. Slightly brighter all around. But it's red — be careful."

---

## Executive summary

The current "beige" lives in **Shopify Admin → Theme settings → Colors**, not in code. The repo has zero hardcoded beige hex values. That means the rebuild is a **token-configuration job**, not a code refactor. Once the new color schemes are entered in Admin, the entire theme picks them up automatically through `snippets/style-variables.liquid`.

**Total touch surface:**
- 1 source-of-truth snippet: `theme/snippets/style-variables.liquid`
- ~30 per-scheme tokens × number of color schemes (likely 3–5)
- ~30 global tokens (header, badges, states, search, overlay)
- 1 dark-mode block with hardcoded values that need a one-time swap (lines 83–154)
- Section schema defaults in ~25 section files (low priority — usually overridden)

---

## Architecture: how colors actually flow

```
Shopify Admin
  └─ Theme settings
      ├─ Colors → color schemes (per-scheme tokens)
      └─ Header / Badges / States (global tokens)
          ↓
    config/settings_data.json   ← gitignored, NOT in repo
          ↓
    snippets/style-variables.liquid   ← single source of truth, IS in repo
          ↓
    CSS custom properties (--background, --buttonBackground, etc.)
          ↓
    All 67 sections + 31 snippets consume them
```

**Implication:** the design system must produce values for *every token name* listed below. Any token left unset falls back to whatever's currently in `settings_data.json` and creates inconsistency.

---

## Per-scheme token inventory (must be defined for every color scheme)

Source: `theme/snippets/style-variables.liquid` lines 16–81.

**Backgrounds**
- `background` — page/scheme canvas
- `alternate_background` — alternating section bg
- `card_bg` — product/content cards
- `background_gradient` — gradient option
- `highlight_solid_color` — highlight surface
- `highlight_gradient_color` — highlight gradient
- `highlight_text_color` — text on highlight surface

**Text**
- `text` — body
- `link_text` — links
- `heading` — headings

**Primary buttons** (5 states)
- `button_bg`, `button_text`, `button_border`
- `button_bg_hover`, `button_text_hover`, `button_border_hover`

**Secondary buttons** (5 states)
- `secondary_button_bg`, `secondary_button_text`, `secondary_button_border`
- `secondary_button_bg_hover`, `secondary_button_text_hover`, `secondary_button_border_hover`

**Inputs**
- `input_bg`, `input_text`, `input_border`

**Borders & dividers**
- `product_border`, `line_divider`

**Misc**
- `rating_color` — star ratings
- `arrow_bg`, `arrow_color` — slider arrows
- `card_shadow` — card shadow color
- `product_card_icon`, `product_card_icon_background` — product card icons
- `product_media_background` — product image bg
- `button_shadow`, `secondary_button_shadow`
- `highlight_color` (a.k.a. `--line-color`) — accent line/underline

---

## Global token inventory (set once across whole site)

Source: `theme/snippets/style-variables.liquid` lines 165–287.

**Mode switch** — `mode_color`, `mode_background`, `mode_border`, `mode_Activebackground`, `mode_Activecolor`, `mode_Activeborder`

**State** — `success_message`, `error_message`

**Badges** (each gets its own bg color; text color auto-computed by brightness)
- `saleBadgeBg`, `newBadgeBg`, `preorderBadgeBg`, `soldBadgeBg`, `customBadgeBg`

**Discount tags** — `discount_bg`, `discount_percent`

**Stock labels** — `in_stock`, `no_stock`, `low_stock`

**Header (primary)** — `background_header`, `header_text`, `header_text_hover`, `transparent_header_color`, `header_icon`, `header_cart_count_bg`, `header_cart_count`

**Header (secondary)** — `secondary_background_header`, `secondary_header_text`, `secondary_header_text_hover`, `secondary_menu_background_hover`, `secondary_menu_border`

**Submenus** — `header_sub_menu_bg`, `header_sub_menu`, `header_sub_menu_hover`, `header_sub_menu_bg2`, `header_sub_menu2`, `header_sub_menu_hover2`

**Search bar** — `search_input_color`, `search_bg_color`

**Mega menu overlay** — `mega_menu_overlay`, `mega_menu_overlay_text`

**Back to top** — `scroll_top_background`, `icon_color`

**Background overlay** — `background_overlay_color`, `background_overlay_opacity`

**Marquee** — `marquee_text_gr` (gradient), `marquee_text` (solid)

**Typography** — `type_body_font`, `type_header_font`, `body_scale_mobile`, `body_scale_desktop`, `heading_font_scale_mobile`, `heading_font_scale_desktop`, `type_base_line_height`, `type_heading_line_height`

**Radius** — `card_radius_mobile/desktop`, `images_radius_mobile/desktop`, `product_grid_radius_mobile/desktop`, `input_radius_mobile/desktop`, `button_radius`, `button_radius_mobile/desktop`

**Button text** — `button_text_transform`

---

## Code hotspots that are NOT settings-driven

These are hardcoded and need a one-time edit during the rebuild.

**Dark mode block** — `snippets/style-variables.liquid` lines 83–154
- Hardcoded yellow accent `#ffca10` — not BBI brand
- Hardcoded grays `#d1d1d1`, `#0e0e0e`, `#161616`
- Recommendation: either disable dark mode entirely (B2B procurement use case doesn't need it) or replace `#ffca10` with the new BBI red and re-test contrast

**Header dark-mode override** — same file, lines 301–334 (header tokens hardcoded for dark mode)

**Section schema defaults** — these are merchant-facing initial values when a section is first added. Examples worth changing if you ever rebuild a section from scratch:
- `sections/parallax.liquid` → `#0B0E0D`, `#ececec`, `#5C5B5B`
- `sections/header.liquid` → `#f2f2f2`, `#6d85a8`, `#eeeeee`, `#3FA043` (announcement)
- `sections/multiboxes.liquid` → `#0B0E0D`, `#EEEEEE`, `#2D2D2D`, `#838383`
- `sections/announcement-bar.liquid` → `#E7E7E7`, `#A3A3A3`
- `sections/blinking-icons.liquid` → `#f00f00` (this is a typo — should be `#ff0f00` or similar; flag for fix)
- `sections/shapes.liquid` → `#FFCA10` × 2 (yellow — should be BBI red or removed)

**Inline SVG fills** in `snippets/reviews.liquid` (`#ddd`) and `sections/main-addresses.liquid` (`#F5F5F7`) — minor, leave for now.

---

## What's NOT in the repo (and where it lives)

- `config/settings_schema.json` → in Shopify (defines what merchants can edit)
- `config/settings_data.json` → in Shopify (the *actual* current values — this is what defines today's beige)
- `assets/*.css` → in Shopify (compiled stylesheets)
- `locales/*.json` → in Shopify (translation strings)

To pull current settings before changing them: `shopify theme pull --only=config/settings_data.json` from a dev theme. **Do this before redesigning** so we have a baseline to diff against.

---

## Recommended workflow for the rebuild

1. **Pull current settings** from live theme to a dev theme dupe — capture today's beige.
2. **Generate new tokens in Claude Design** using the constraint brief at `docs/strategy/design-system-brief.md`.
3. **Validate contrast** — every text/bg pair against AA 4.5:1, every UI/border pair against 3:1.
4. **Enter new schemes in Shopify Admin** on a duplicate (non-live) theme.
5. **One-time code edits:**
   - Replace `#ffca10` in dark-mode block (or disable dark mode)
   - Fix `#f00f00` typo in `blinking-icons.liquid`
   - Replace `#FFCA10` in `shapes.liquid` if section is in use
6. **Visual diff** on real Shopify preview URLs — homepage, a PDP, collection, contact.
7. **Promote dev theme to live** when approved.

---

## Risks / things that will bite

- **Card shadow color** is per-scheme but optional — if blank, falls back to scheme default. Bright backgrounds + heavy shadows = muddy. Keep shadows light or skip shadows on white-bg schemes.
- **Sale badge text color is auto-computed** by `color_brightness` filter. If you pick a mid-tone red for sale badges, the auto-pick may flip text from white→black at the wrong threshold. Test with the actual hex before committing.
- **Header has TWO color sets** (primary + secondary). The "secondary" set is used by the hamburger/mobile menu. Forgetting to set it cleanly is a common cause of "the mobile menu looks broken" reports.
- **Color-scheme IDs are persistent.** If you rename schemes, every section that references the old ID by name breaks. Add new schemes; don't rename.
