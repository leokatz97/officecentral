# Prompt 1 (Updated) — Cart 404 + Header Cart Count + Cart Page Design

**Paste the safety preflight first (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.**

---

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Three cart-related bugs to fix together:
  A. Clicking Add to Cart on a PDP returns 404.
  B. Header cart count badge (top-right of header) does not populate
     or update when items are added.
  C. /cart page renders with no BBI design system styling — different
     fonts, no container, no token usage, looks like default Shopify.

─── Step 1: Diagnose all three BEFORE any edits ─────────────────────

A. Cart 404 root cause:
  1. Check theme/templates/cart.json or cart.liquid — does either
     exist? If cart.json: what section does it reference?
  2. Open theme/sections/ds-pdp-base.liquid. Find the Add to Cart
     button. Report: does it have data-bbi-quote-trigger (it MUST
     NOT — that attribute belongs only on Request a Quote)? Does it
     POST to /cart/add.js or redirect to /cart? Is the button inside
     a <form action="/cart/add">?
  3. Open theme/layout/theme.liquid lines 162–177. The cart drawer
     render gate likely reads:
       if template != 'cart' and bbi_landing == false
     Product pages set bbi_landing = true (line 91) so the drawer
     never loads on PDPs. Confirm this is the root cause.

B. Header cart count root cause:
  1. Find the header section file (likely theme/sections/ds-header.liquid
     or main-header.liquid). Locate the cart icon element.
  2. Report: is there a count element? What selector? Does it render
     {{ cart.item_count }} server-side?
  3. Search theme/assets/*.js for cart count update logic. Is there
     a listener for cart:refresh / cart:updated that re-fetches
     /cart.js and updates the badge after add-to-cart?

C. /cart page root cause:
  1. Read theme/templates/cart.json — what section type does it
     reference?
  2. Open that section file. Does it use BBI design system tokens
     (var(--background), var(--textColor), var(--borderColor),
     var(--cardRadius), 1320px container, BBI typography scale)?
  3. Compare its visual language to theme/sections/ds-pdp-base.liquid.

Report all findings for A, B, C before editing anything.

─── Step 2: Fix A — Cart 404 ─────────────────────────────────────────

Most likely fix: in theme/layout/theme.liquid line 173, change:
    {%- if template != 'cart' and bbi_landing == false -%}
to:
    {%- if template != 'cart' -%}

If cart template is missing, create theme/templates/cart.json:
  {
    "sections": { "main": { "type": "ds-cart-base", "settings": {} } },
    "order": ["main"]
  }

If Add to Cart button has a stray data-bbi-quote-trigger attribute,
remove it. That attribute belongs ONLY on the Request a Quote button.

─── Step 3: Fix B — Header cart count ────────────────────────────────

In the header section file, ensure the cart icon includes:

  <a href="/cart" class="header__cart" aria-label="Cart">
    <svg>...</svg>
    <span class="header__cart-count" data-cart-count
          {%- if cart.item_count == 0 %} hidden{% endif -%}>
      {{ cart.item_count }}
    </span>
  </a>

CSS (in style-variables.liquid or header section <style>):

  .header__cart { position: relative; }
  .header__cart-count {
    position: absolute; top: -6px; right: -8px;
    min-width: 18px; height: 18px; padding: 0 5px;
    border-radius: 9px;
    background: var(--accent, #C8102E);
    color: #fff;
    font-size: 11px; font-weight: 600;
    display: inline-flex; align-items: center; justify-content: center;
    line-height: 1;
  }
  .header__cart-count[hidden] { display: none; }

JS — create theme/assets/bbi-cart.js (or append to existing cart JS):

  (function () {
    const badge = document.querySelector('[data-cart-count]');
    if (!badge) return;

    async function refresh() {
      try {
        const r = await fetch('/cart.js', { headers: { Accept: 'application/json' } });
        const cart = await r.json();
        badge.textContent = cart.item_count;
        if (cart.item_count > 0) badge.removeAttribute('hidden');
        else badge.setAttribute('hidden', '');
      } catch (e) { /* leave as-is */ }
    }

    document.addEventListener('cart:updated', refresh);
    document.addEventListener('cart:refresh', refresh);
  })();

Wire it into layout/theme.liquid via:
  <script src="{{ 'bbi-cart.js' | asset_url }}" defer></script>

After every successful /cart/add.js call (in PDP / Buy Now / quote-modal
add flows), dispatch:
  document.dispatchEvent(new CustomEvent('cart:updated'));

─── Step 4: Fix C — Cart page design ─────────────────────────────────

Create theme/sections/ds-cart-base.liquid following the BBI design
system. Mirror the tokens and patterns used in ds-pdp-base.liquid:

  Container:
    - 1320px max-width
    - var(--background), var(--textColor), var(--borderColor),
      var(--cardRadius)
    - Typography: H1 matches PDP product-title size; body 17px/1.6

  Layout (desktop ≥960px): 60/40 grid — line items left, summary
  right. Mobile: stacked.

  Line item row (per item):
    - 80×80 thumbnail (link to product, 4:5 crop ok)
    - Title (link to /products/<handle>) + variant title if any
    - Quantity stepper — reuse the .pdp-quantity component pattern
      (− / input / +), bound to /cart/change.js
    - Line total ({{ line_item.final_line_price | money }})
    - Remove (×) button → POST /cart/change.js with quantity=0

  Summary card (sticky on desktop):
    - Subtotal ({{ cart.total_price | money }})
    - Note: "Taxes and shipping calculated at checkout"
    - Checkout button (full width, dominant black, name="checkout")
    - "Continue shopping" link → /collections/all (outline style)

  Empty state (cart.item_count == 0):
    - Centered "Your cart is empty" headline
    - "Continue shopping" CTA → /collections/all

Form wrapper:
  <form action="/cart" method="post" novalidate>
    ... line items + summary ...
    <button type="submit" name="checkout" class="pdp-btn pdp-btn--primary">
      Checkout
    </button>
  </form>

Update theme/templates/cart.json to reference ds-cart-base:
  {
    "sections": { "main": { "type": "ds-cart-base", "settings": {} } },
    "order": ["main"]
  }

Comment block at top of ds-cart-base.liquid documenting purpose and
any non-obvious schema settings.

─── Step 5: Push ─────────────────────────────────────────────────────

For theme/layout/theme.liquid (Fix A):
  export $(grep -v '^#' .env | xargs) && \
    BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py \
    186373570873 --layout

For header section (Fix B): push via API (mirror the ds-pdp-base.liquid
push pattern from Prompt 0).

For ds-cart-base.liquid section + cart.json template + bbi-cart.js
asset (Fixes B + C): push each via API. Confirm HTTP 200 each.

─── Step 6: Verify ───────────────────────────────────────────────────

A. Cart 404 fix — PDP add-to-cart:
   https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873
   Click Add to Cart → cart drawer opens OR /cart loads without 404.

B. Header count:
   - After adding 1 item, header cart badge shows "1" without a
     page reload.
   - Add a second item → badge updates to "2".
   - Hard refresh /cart page — header still shows correct count.
   - Remove an item from /cart — badge decrements without reload.
   - Empty cart → badge is hidden.

C. Cart page design:
   https://office-central-online.myshopify.com/cart?preview_theme_id=186373570873
   - White background, BBI typography, 1320px container.
   - 60/40 layout on desktop, stacked on mobile.
   - Working quantity steppers; line totals update on change.
   - Remove button works.
   - Dominant black Checkout button matches PDP Add to Cart style.
   - Empty state renders when cart is empty.
   - Visual language matches the PDP.

Commit (separate commits, one per fix):
  "Fix cart 404: restore cart drawer on product pages (drop bbi_landing gate)"
  "Fix header cart count: subscribe to cart:updated events, re-render badge"
  "Add ds-cart-base section: cart page now uses BBI design system"
```
