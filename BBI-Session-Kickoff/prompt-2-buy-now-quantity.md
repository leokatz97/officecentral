# Prompt 2 (Updated) — Buy Now + Quantity Selector

**Paste the safety preflight first (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.**

---

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.
Primary file: theme/sections/ds-pdp-base.liquid.

Smoke test 2026-05-11 confirmed the cart funnel works end-to-end (mini-cart
opens, badge updates, /cart styled, checkout doesn't 404, logo renders).
Outstanding gap: the PDP CTA stack may be missing the quantity stepper, and
Buy Now (if present at all) may be visual-only with no /checkout wiring.

Task: add a working Quantity selector and a working Buy Now button to the PDP.

CRITICAL — must NOT break any of these:
  - data-bbi-quote-trigger (Request a Quote button + global modal intercept)
  - BbiPdpVariants Web Component + its variant-price refresh JS
  - bbi-pdp-gallery Web Component
  - The existing fetch('/cart/add.js') Add to Cart flow
  - The cart:updated CustomEvent dispatch (mini-cart depends on it)
  - The Quote-only CTA branch when product.price == 0 OR product.available == false
    (BBI Rule #2 — unbuyable items stay live as lead-capture pages)

─── Step 1: Diagnose current state — read before editing ────────────

Open theme/sections/ds-pdp-base.liquid and report all three:

1. Buy Now button:
   - Does an element with [data-buy-now], class "buy-now", or class
     "pdp-btn--buy-now" exist?
   - If yes: is it wired to fetch('/cart/add.js') + redirect to /checkout?
     Or is it just a styled button with no JS handler?

2. Quantity selector:
   - Does an element with [data-quantity-minus] / [data-quantity-plus] exist?
   - Is there an <input name="quantity"> inside the product <form>?
   - Are the increment / decrement buttons wired in any IIFE?

3. Variant state machine:
   - Where is the currently-selected variant ID stored after a chip click?
     (BbiPdpVariants WC dataset? hidden <input name="id">? something else?)
   - How does the existing Add to Cart flow read the variant ID for
     /cart/add.js? Reuse the exact same selector for Buy Now.

4. CTA gate:
   - Find the `{% if %}` (or equivalent) that hides Add to Cart on $0 /
     sold-out products and renders only the Quote CTA. Quantity selector
     + Buy Now must go INSIDE the same branch, never outside it.

Report all four findings before editing.

─── Step 2: Add Quantity selector (if Step 1 says missing) ──────────

Place directly above the Add to Cart button, inside the product <form>,
inside the buyable-only branch.

  <div class="pdp-quantity">
    <button class="pdp-quantity__btn" data-quantity-minus type="button"
            aria-label="Decrease quantity">−</button>
    <input class="pdp-quantity__input" type="number" name="quantity"
           id="pdp-quantity-input" value="1" min="1" aria-label="Quantity">
    <button class="pdp-quantity__btn" data-quantity-plus type="button"
            aria-label="Increase quantity">+</button>
  </div>

CSS — Starlite colour tokens are R,G,B triples, ALWAYS wrap in rgb():

  .pdp-quantity {
    display: flex;
    align-items: center;
    border: 1px solid rgb(var(--borderColor));
    border-radius: var(--cardRadius);
    overflow: hidden;
    width: fit-content;
    margin-bottom: 12px;
  }
  .pdp-quantity__btn {
    background: none;
    border: none;
    padding: 10px 16px;
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    color: rgb(var(--textColor));
    transition: background 0.15s;
  }
  .pdp-quantity__btn:hover {
    background: rgb(var(--alternateBackground, 244, 244, 244));
  }
  .pdp-quantity__input {
    width: 48px;
    text-align: center;
    border: none;
    border-left: 1px solid rgb(var(--borderColor));
    border-right: 1px solid rgb(var(--borderColor));
    font-size: 15px;
    padding: 10px 0;
    color: rgb(var(--textColor));
    background: none;
    -moz-appearance: textfield;
  }
  .pdp-quantity__input::-webkit-outer-spin-button,
  .pdp-quantity__input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

JS — add inside the existing PDP IIFE (do not create a duplicate
DOMContentLoaded listener):

  const qMinus = document.querySelector('[data-quantity-minus]');
  const qPlus  = document.querySelector('[data-quantity-plus]');
  const qInput = document.getElementById('pdp-quantity-input');
  if (qMinus && qPlus && qInput) {
    qMinus.addEventListener('click', () => {
      const v = parseInt(qInput.value, 10);
      if (v > 1) qInput.value = v - 1;
    });
    qPlus.addEventListener('click', () => {
      qInput.value = parseInt(qInput.value, 10) + 1;
    });
  }

─── Step 3: Add Buy Now (or wire the existing button) ───────────────

Place directly above Add to Cart, below the quantity selector, inside the
same buyable-only branch.

  <button type="button"
          class="pdp-btn pdp-btn--primary pdp-btn--buy-now"
          data-buy-now>
    Buy now
  </button>

CSS:

  .pdp-btn--buy-now {
    width: 100%;
    margin-bottom: 10px;
    background: rgb(var(--textColor));
    color: rgb(var(--background));
    border: 2px solid rgb(var(--textColor));
  }
  .pdp-btn--buy-now:hover { opacity: 0.85; }
  .pdp-btn--buy-now:disabled { opacity: 0.5; cursor: not-allowed; }

JS — variant-ID resolution MUST match how the existing ATC flow reads it
(confirmed in Step 1). Pseudo-code below uses the most likely two
selectors; replace with whatever Step 1 finds:

  const buyNow = document.querySelector('[data-buy-now]');
  if (buyNow) {
    buyNow.addEventListener('click', async () => {
      const original = buyNow.textContent;
      buyNow.disabled = true;
      buyNow.textContent = 'Adding…';
      try {
        // ⚠️ REPLACE this with the exact selector used by Add to Cart
        const variantEl = document.querySelector('[name="id"]')
                       || document.querySelector('[data-selected-variant]');
        const variantId = variantEl
          ? (variantEl.value || variantEl.dataset.selectedVariant)
          : null;
        if (!variantId) throw new Error('No variant selected');

        const qty = parseInt(
          document.getElementById('pdp-quantity-input')?.value || '1', 10
        );

        const res = await fetch('/cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: variantId, quantity: qty })
        });
        if (!res.ok) throw new Error('Cart add failed: ' + res.status);

        // Optional but nice: dispatch cart:updated before redirect so the
        // mini-cart badge is correct if checkout returns the user.
        document.dispatchEvent(new CustomEvent('cart:updated'));

        window.location.href = '/checkout';
      } catch (e) {
        console.error('Buy now failed:', e);
        buyNow.disabled = false;
        buyNow.textContent = original;
      }
    });
  }

─── Step 4: Final CTA stack on buyable PDPs (top → bottom) ──────────

  1. Quantity selector
  2. Buy Now (dominant black, full width)
  3. Add to Cart (existing — DO NOT change wiring)
  4. Quote strip (.pdp-quote-card — compact one-line)

On unbuyable PDPs (price == 0 OR available == false), only:

  1. Request a Quote CTA (existing) — no quantity, no Buy Now, no ATC

─── Step 5: Push ────────────────────────────────────────────────────

ds-pdp-base.liquid is a section — push via API (mirror the Prompt 0
pattern, NOT bbi-push-landing.py which doesn't accept individual sections):

  export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
  import os, json, urllib.request
  STORE = 'office-central-online.myshopify.com'
  TOKEN = os.environ['SHOPIFY_TOKEN']
  THEME = '186373570873'
  with open('theme/sections/ds-pdp-base.liquid', 'rb') as f:
      content = f.read().decode('utf-8')
  body = json.dumps({'asset': {
      'key': 'sections/ds-pdp-base.liquid',
      'value': content
  }}).encode()
  req = urllib.request.Request(
      f'https://{STORE}/admin/api/2024-04/themes/{THEME}/assets.json',
      data=body, method='PUT',
      headers={'X-Shopify-Access-Token': TOKEN,
               'Content-Type': 'application/json'}
  )
  with urllib.request.urlopen(req) as r:
      print(f'HTTP {r.status}')
  PYEOF

Confirm HTTP 200.

─── Step 6: Verify ──────────────────────────────────────────────────

Buyable PDP — full CTA stack:
  https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873

Confirm:
  ✓ Quantity stepper renders; − decrements (floor at 1); + increments.
  ✓ Buy Now button: visible, dominant black, full width, above ATC.
  ✓ Buy Now with no variant selected → error logged, button re-enables.
  ✓ Variant selected + Buy Now → /checkout opens with that variant + qty.
  ✓ Add to Cart still works (mini-cart opens, badge ticks up).
  ✓ Quote strip still opens the quote modal.
  ✓ Quote modal still pre-fills the product name.

Unbuyable PDP regression — sold-out:
  https://office-central-online.myshopify.com/products/anda-seat?preview_theme_id=186373570873

Unbuyable PDP regression — $0 showcase:
  https://office-central-online.myshopify.com/products/additional-services-dismantle-re-assemble?preview_theme_id=186373570873

On both unbuyable URLs: ONLY the Quote CTA renders. No quantity stepper,
no Buy Now, no Add to Cart. If any of those leak through, the
quantity/Buy Now/ATC block is outside the buyable-only branch — fix the
gate, push again.

Commit: "Add quantity selector + Buy Now to PDP (wired to /cart/add.js → /checkout)"
```
