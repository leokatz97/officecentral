# BBI Cart Polish — Session 2 Prompt

**Store:** office-central-online.myshopify.com  
**Dev theme ID:** 186373570873 (BBI Landing Dev — never push to live)  
**Working dir:** /Users/leokatz/Desktop/Office Central  
**Push script:** `python3 scripts/bbi-push-landing.py 186373570873 [--snippets] [--layout]`  
**Direct API push:** see pattern at end of this file.

---

## What was fixed last session

Three cart bugs were resolved:

- **Fix A (Cart 404):** `ds-pdp-base.liquid` Add to Cart now uses `fetch('/cart/add.js')` (AJAX) instead of a full-page POST form submit. On success it shows "Added ✓" for 2 s and dispatches `cart:updated`.
- **Fix B (Cart count badge):** `bbi-nav.liquid` gained a shopping bag icon + red count badge (`[data-bbi-cart-count]`) in the utility bar. Server-renders `{{ cart.item_count }}`; refreshes on `cart:updated` via `/cart.js`.
- **Fix C (Cart page design):** `theme/sections/ds-cart-base.liquid` (new) replaced `cart.liquid` as the cart template section. `theme/templates/cart.json` now points at `ds-cart-base`. The section renders the BBI nav + footer and uses BBI design tokens throughout.

---

## Three remaining issues to fix this session

---

### Issue 1 — Cart page is too black / too stark

**What the user sees:** The `/cart` page feels very dark and doesn't match the visual tone of other BBI pages (healthcare, education, PDP, etc.). The checkout button and the empty-state CTA are hardcoded `#0B0B0C` (near-black), making the page feel heavy.

**Root cause:** `theme/sections/ds-cart-base.liquid` uses hardcoded `#0B0B0C` for the checkout button (`background:#0B0B0C;color:#ffffff`) and the empty-state CTA button, instead of the design system's button tokens.

**How other BBI pages handle primary buttons:** Look at `theme/sections/ds-pdp-base.liquid` — the primary Add to Cart button uses class `.pdp-btn--primary` whose CSS reads `background: var(--buttonBackground); color: var(--buttonColor)`. The `--buttonBackground` token is set via Shopify's color scheme settings (`style-variables.liquid`) and resolves to the store's configured primary button colour, which is lighter and follows the overall brand palette.

**Fix:** In `ds-cart-base.liquid`:
1. Replace hardcoded `background:#0B0B0C;color:#ffffff` on `.bbi-cart__checkout` with `background:rgb(var(--buttonBackground));color:rgb(var(--buttonColor));border-radius:var(--buttonRadius);` and hover via `rgb(var(--buttonBackgroundHover))`.
2. Same on `.bbi-cart__empty-cta`.
3. The summary card background `var(--alternateBackground,#FAFAFA)` — wrap it in `rgb()` since Starlite tokens are stored as RGB triples (e.g. `255,255,255`), not hex. All `var(--...)` colour tokens in this theme are stored as `R,G,B` and must be accessed as `rgb(var(--tokenName))`.
4. While you're in there, verify the heading and body font-sizes feel proportionate next to the PDP — the cart heading should be ~28px, line items ~15px, matching the PDP's scale.

**Check:** Compare visually against `theme/sections/ds-pdp-base.liquid` button styles and the component spec at `docs/strategy/bbi-component-spec-v1.md`.

---

### Issue 2 — Cart icon should show a mini-cart dropdown, not navigate to /cart

**What the user wants:** Clicking the shopping bag icon in the BBI nav header should open a lightweight dropdown panel (mini-cart) that shows:
- Current cart items (thumbnail, title, qty, price — same data as the full cart page)
- Subtotal
- Two CTAs: "View Cart" (link to `/cart`) and "Checkout" (submits to `/checkout`)
- Clicking outside or pressing Escape closes it

Only clicking "View Cart" should navigate to the full `/cart?preview_theme_id=...` page.

**Current behaviour:** The cart icon is `<a href="/cart">` so clicking it navigates directly.

**Implementation approach:**

**In `theme/snippets/bbi-nav.liquid`:**

1. Change the cart `<a href="/cart">` to a `<button type="button">` with `data-bbi-cart-toggle` (keep the SVG + badge inside it).
2. Add a mini-cart panel below the utility bar (still inside `.bbi-header__inner` or positioned absolutely off the button):

```html
<div class="bbi-minicart" data-bbi-minicart hidden aria-label="Cart preview" role="dialog">
  <div class="bbi-minicart__inner">
    <div class="bbi-minicart__items" id="bbi-minicart-items">
      <!-- JS-populated -->
    </div>
    <div class="bbi-minicart__footer">
      <div class="bbi-minicart__subtotal">
        <span>Subtotal</span>
        <span id="bbi-minicart-total"></span>
      </div>
      <a href="/cart" class="bbi-minicart__view-cart">View Cart</a>
      <form action="/cart" method="post">
        <button type="submit" name="checkout" class="bbi-minicart__checkout">Checkout</button>
      </form>
    </div>
  </div>
</div>
```

3. CSS: position the panel absolutely, anchored to the cart button (right-aligned, below the header bar). ~340px wide, white background, `border:1px solid var(--borderColor)`, `border-radius:var(--cardRadius)`, `box-shadow: 0 8px 24px rgba(11,11,12,.12)`. Items list max-height ~320px with overflow-y scroll.

4. JS (add to the existing nav IIFE or alongside it):
   - On `data-bbi-cart-toggle` click: fetch `/cart.js`, populate items HTML, toggle `hidden` on the panel.
   - Close on click-outside (`document.addEventListener('click', ...)`) and `Escape` key.
   - After `cart:updated` fires: if panel is open, refresh its content automatically.
   - Item row format: 56×56 thumbnail (use `line_item.featured_image` or product image), title, qty × price.
   - Empty state: "Your cart is empty" message with "Start shopping" link to `/collections/all`.

**Do not break the cart icon badge** — it should keep updating via `cart:updated`.

---

### Issue 3 — Logo not rendering in BBI nav/footer on cart page (and potentially other pages)

**Root cause (confirmed):** `bbi-nav.liquid` and `bbi-footer.liquid` use the logo object passed from `section.settings.logo` (an `image_picker`). When that setting is blank in the Theme Editor, they fall back to:
```liquid
<img src="{{ 'bbi-logo-v2.png' | asset_url }}" ...>
```

**The file `assets/bbi-logo-v2.png` is NOT uploaded to the dev theme** (confirmed via API: 404 on `assets/bbi-logo-v2.png` for theme 186373570873). So the fallback renders a broken image.

The logo source file exists locally at:
`data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png`

**Fix:** Upload `bbi-logo-v2.png` to the dev theme assets via the Shopify Assets API:

```python
import os, json, base64, urllib.request
STORE = os.environ['SHOPIFY_STORE']
TOKEN = os.environ['SHOPIFY_TOKEN']
THEME = '186373570873'

with open('data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png', 'rb') as f:
    data = base64.b64encode(f.read()).decode()
body = json.dumps({'asset': {'key': 'assets/bbi-logo-v2.png', 'attachment': data}}).encode()
req = urllib.request.Request(
    f'https://{STORE}/admin/api/2024-04/themes/{THEME}/assets.json',
    data=body, method='PUT',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as r:
    print(r.status, json.loads(r.read()).get('asset', {}).get('key'))
```

**After the upload, confirm the logo renders on:**
- Any PDP: `/products/alphabetter-stand-up-desk?preview_theme_id=186373570873`
- Cart page: `/cart?preview_theme_id=186373570873`
- At least one LP page (e.g. `/pages/healthcare?preview_theme_id=186373570873`)

**Why other pages might be affected too:** Every BBI section that renders `bbi-nav` or `bbi-footer` relies on the same fallback. If a section's logo image_picker setting is blank in the Theme Editor, the broken image shows. The push script does not set section settings — those are only configurable in the Shopify Theme Editor or via the `config/settings_data.json` file. Uploading the asset file is the correct fix (the `asset_url` call will resolve once the file exists).

---

## Sequence

1. Upload `bbi-logo-v2.png` to theme assets (quick win, no code change).
2. Fix cart page token colours in `ds-cart-base.liquid`, push via script.
3. Implement mini-cart dropdown in `bbi-nav.liquid`, push with `--snippets`.
4. Verify all three on dev theme preview URLs.
5. Separate commits: `"Fix cart page colours: use design system button tokens"`, `"Fix logo asset: upload bbi-logo-v2.png to dev theme"`, `"Add mini-cart dropdown to BBI nav header"`.

---

## Key files

| File | Purpose |
|------|---------|
| `theme/sections/ds-cart-base.liquid` | Cart page section — fix colours here |
| `theme/snippets/bbi-nav.liquid` | BBI header — add mini-cart, fix cart icon behaviour |
| `theme/snippets/bbi-footer.liquid` | BBI footer — uses same logo fallback |
| `theme/sections/ds-pdp-base.liquid` | Reference for button token usage |
| `theme/snippets/style-variables.liquid` | Token definitions — note all colour tokens are `R,G,B` triples, always wrap in `rgb()` |
| `docs/strategy/bbi-component-spec-v1.md` | Visual component spec |
| `data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png` | Logo source file to upload |

## Direct API push pattern (for files not covered by the push script)

```bash
cd /Users/leokatz/Desktop/Office\ Central && \
export $(grep -v '^#' .env | xargs) && python3 - <<'PYEOF'
import os, json, base64, urllib.request, time

STORE = os.environ['SHOPIFY_STORE']
TOKEN = os.environ['SHOPIFY_TOKEN']
THEME = '186373570873'

def push(key, path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    body = json.dumps({'asset': {'key': key, 'attachment': data}}).encode()
    req = urllib.request.Request(
        f'https://{STORE}/admin/api/2024-04/themes/{THEME}/assets.json',
        data=body, method='PUT',
        headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as r:
            print(f'OK  {key} ({r.status})')
    except urllib.error.HTTPError as e:
        print(f'FAIL {key} ({e.code}): {e.read().decode()[:120]}')
    time.sleep(0.6)

push('assets/bbi-logo-v2.png', 'data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png')
PYEOF
```
