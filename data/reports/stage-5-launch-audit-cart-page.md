# Stage 5 Launch Audit — 4.8 Cart Page
**Date:** 2026-05-08
**Sources:** `theme/sections/cart.liquid`, `theme/templates/` (cart template not found), `docs/plan/bbi-build-state.md` (SYS-VERIFY-1)
**Auditor:** Claude Code (read-only pass)

---

## Current state

### Template
No `cart.json` template exists in `theme/templates/`. The cart page (`/cart`) renders via the Starlite default cart mechanism — likely `theme/layout/theme.liquid` falls through to the Starlite header/footer since `/cart` is not in the `bbi_landing` gate.

### Cart section
`theme/sections/cart.liquid` exists — this is the Starlite stock cart section. It renders:
- Empty cart state with icon + "Continue shopping" CTA (routes to `routes.all_products_collection_url`)
- Cart item list (Starlite styling — charcoal/Starlite color scheme variables, not BBI tokens)
- Quantity selectors, remove buttons
- Order summary panel with subtotal + checkout button
- Cart drawer `ajax-cart-drawer.liquid` snippet for sidebar cart

None of this uses BBI design tokens (no `--accentRed`, no `--headingColor`, no BBI typography). The cart page will render with Starlite chrome (Starlite header + Starlite footer) because:
1. No `cart.json` template exists
2. `/cart` is not in the `bbi_landing` gate (not in `theme/layout/theme.liquid` condition list)

Per `bbi-build-state.md` SYS-VERIFY-1:
> "Architecture §2m flags these as 'Standard Shopify' templates — they should NOT be in `bbi_landing` gate, so the inherited Starlite header/footer renders intact."

---

## Clarification: cart is intentionally Starlite per architecture decision

The site architecture (`docs/plan/site-architecture-2026-04-25.md` §2m) explicitly classifies `/cart` as a system page using "Standard Shopify cart." The `bbi_landing` gate is designed to _suppress_ Starlite on BBI landing pages — system pages like cart, search, account, and password are intended to remain on Starlite.

**This is not a bug by original design.** However, the UX impact is:
- Customer adds product to cart on a BBI-branded sub-collection page
- Navigates to `/cart`
- Sees Starlite header + Starlite footer (different branding, different nav)
- Continuity break in the shopping experience

---

## The rebuild question

A cart page rebuild would require:
1. Adding `template == 'cart'` to the `bbi_landing` gate in `theme/layout/theme.liquid`
2. Creating `theme/templates/cart.json` referencing a new `ds-cart.liquid` section
3. Building `ds-cart.liquid` with BBI tokens, `bbi-nav`, `bbi-footer`
4. Preserving all cart functionality (quantity selectors, remove, checkout, cart drawer)

This is not in the current build plan. The May 7 remediation plan (design-system-remediation-2026-05-07.md) does not include a cart rebuild. SYS-VERIFY-1 confirms system pages should stay on Starlite.

---

## Assessment

| Dimension | State |
|---|---|
| Template | No `cart.json` — uses Starlite fallback |
| Section | `cart.liquid` — Starlite stock, no BBI tokens |
| Gate | Not in `bbi_landing` — Starlite chrome renders |
| Functional? | Yes — cart/checkout flows are functional |
| BBI-branded? | No |
| Architecture intent | "Standard Shopify" — cart left on Starlite per §2m |

---

## Severity

**FIX** (not BLOCK) — cart functions correctly. The brand continuity break is real and visible to customers but does not prevent purchase flow. A rebuild is desirable before launch but not required for the site to function.

**If rebuilding before launch:** estimate 0.5–1 dev day. Add `CART-1` row to Wave E or new Wave G row. Gate extension + template + section build.

**If deferring to post-launch:** add to post-launch backlog. Document the continuity gap for Steve's awareness.

---

## "Continue shopping" CTA destination

Current empty-cart state CTA routes to `routes.all_products_collection_url` — Shopify's auto-generated `/collections/all`. This should route to `/collections/business-furniture` (BBI's top-level shop entry). This is a FIX-level content issue regardless of whether the cart page is rebuilt.
