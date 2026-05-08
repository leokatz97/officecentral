# Stage 5 Launch Audit — 4.6 Variant Picker Bug
**Date:** 2026-05-08
**Source:** `theme/sections/main-product.liquid`, `theme/snippets/product-blocks.liquid`, `data/reports/stage-4a-current-pdp-audit.md`, `data/reports/stage-4a-decision.md`
**Auditor:** Claude Code (read-only pass)

---

## Current state

PDPs render via `theme/sections/main-product.liquid` (Starlite stock section). Variant rendering is delegated to `{% render 'product-blocks', ... %}` which includes a `variant_picker` block type.

The `variant_picker` block in Starlite renders all option types as **text labels only** — there is no colour-swatch logic, no visual chip rendering, no hex-mapping. All variant options (Colour, Finish, Material, Size, etc.) display as identical borderless text buttons.

---

## The bug

**Non-colour variants** (Size, Material, Finish, Grade) render as borderless run-together text labels that visually read as inline prose rather than distinct picker options. There is no visual separation between the option name and its values.

**Colour variants** suffer additionally from rendering the colour name as a text label rather than a filled colour swatch. Per project memory: `feedback_colour_swatches_visual.md` — *"Colour-option chips must render as filled swatches in the actual colour, not text chips spelling the colour name."*

---

## Scope of fix

This fix cannot be made to `main-product.liquid` (Starlite) — the variant picker is the reason `ds-pdp-base.liquid` is a greenfield build.

### What Stage 4b must build

| Feature | Implementation |
|---|---|
| Colour swatches | Custom swatch picker in `ds-pdp-base.liquid`. Map colour option names to hex values via a Liquid `assign` table for standard BBI finishes (Black, White, Grey, Walnut, etc.). Render as `<button style="background: {hex}">` chips with aria labels. |
| Non-colour option pickers | Styled pill buttons with clear border, active state (charcoal fill), and adequate tap target (44px min height). |
| Option group labels | Visible label above each option group: "Colour: Black" updating dynamically on selection. |
| Variant URL param | Selected variant reflected in URL (`?variant=`) for shareable links. |
| Sold-out states | Crossed-out or disabled pills for unavailable variant combinations. |

Per `stage-4a-decision.md` Gap G-8:
> "Required. Per feedback memory: colour swatches must be filled chips (actual colour), never text labels. Build custom swatch picker in `ds-pdp-base.liquid` using `variant.option1` + Liquid colour name→hex mapping for standard BBI finishes."

---

## Colour name → hex mapping (initial list for Stage 4b)

To be expanded during Stage 4b. Starter list based on BBI catalog:

| Colour name | Hex |
|---|---|
| Black | `#0B0B0C` |
| White | `#FFFFFF` |
| Charcoal | `#3D3D3F` |
| Grey / Gray | `#8C8C8E` |
| Silver | `#C0C0C2` |
| Walnut | `#7C4B2B` |
| Maple | `#C8956C` |
| Cherry | `#7B2929` |
| Espresso | `#3B1A0D` |
| Blue | `#1A4F8B` |
| Navy | `#1a2744` |
| Red | `#D4252A` |
| Green | `#2E6B3E` |
| Sand / Beige | `#D4B896` |
| Brown | `#6B3D2A` |

---

## Impact

- ~640+ products with variants (all fabric/finish options)
- This bug affects every PDP on the site
- Per BBI Rule #2: sold-out variants must also show correct state on the swatch

---

## Severity

**BLOCK** — affects every PDP, directly contradicts explicit design feedback (`feedback_colour_swatches_visual.md`), and is a known regression from the Starlite stock section. Cannot launch with this state.

Fix is included in Stage 4b scope (PDP-1 deliverable).
