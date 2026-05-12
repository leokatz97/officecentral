# PDP Restructure — Claude Code prompt (paste into a fresh session)

---

## Context — read first

You are working on a Shopify Online Store 2.0 theme at `office-central-online.myshopify.com`. The repo root is the shop's working directory. All work in this task happens in **one file**:

- `theme/sections/ds-pdp-base.liquid`

You will not read or edit any other section, snippet, or template. You will not create new files.

**Dev theme:** `186373570873` (do not push to live)

**Test product URL:** https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873

**Push command** (run from repo root after each commit):
```
export $(grep -v '^#' .env | xargs) && BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873 --layout --snippets
```

**Workflow:** read the file, make the changes for one fix, commit, push, fetch the live page with `curl '<url>?preview_theme_id=186373570873' -H 'User-Agent: Mozilla/5.0' -s` and grep for the expected post-fix HTML to confirm the change is on the dev theme, then move to the next fix. **Three commits total** — one per fix — in imperative mood ("Restructure PDP right column", "Move About + Specifications below the fold", "Add variant price data to JSON").

If a Liquid syntax error 422s on push, the agent will surface the exact line — fix it before proceeding to the next fix.

---

## Fix 1 — Right column restructure

The right-column wrapper is `<bbi-pdp-variants class="pdp-info">`. Today it contains, in this order:

```
vendor → title → SKU → badge → price → variants → About section → Key Features section → Specifications section → CTA buttons → trust pills → phone nudge
```

Change it to:

```
vendor (eyebrow) → title → SKU + variant count → OECM/Canadian/availability badges → short description → quote card → trust pills
```

### Specific edits

**1.1 Remove the three `pdp-info-section` blocks** (About, Key Features, Specifications) from inside `<bbi-pdp-variants>`. They will be re-added below the fold in Fix 2 — do not delete the spec metafield assignments yet, you will reuse them.

**1.2 Remove the standalone `<p class="pdp-price">`** (and the `pdp-price--zero` variant of it). B2B context — price is not the primary signal in the right column. The price will surface inside the quote card and update via Fix 3 when the size chip changes.

**1.3 Add OECM and Canadian-Made badges** below the existing availability badge. Read `product.tags` for the strings `oecm` and `canadian-made` (case-insensitive). Render each present tag as a small pill. Use this CSS pattern as the base:

```
font-size: 11px;
font-weight: 600;
letter-spacing: 0.06em;
text-transform: uppercase;
border: 1px solid;
border-radius: 100px;
padding: 3px 10px;
display: inline-flex;
align-items: center;
gap: 5px;
```

- **OECM badge:** green border + green text. Use `#15803D` (already present elsewhere in the file as the available-badge color).
- **Canadian badge:** red border + red text. Use `var(--saleBadgeBackground)` (the brand red).

Group the OECM, Canadian, and availability badges in a flex row with `gap: 8px; flex-wrap: wrap; margin-bottom: 20px`. The existing availability badge keeps its current pill styling — do not change it.

**1.4 Replace the plain CTA button pair with a quote card.** A bordered box wrapping the CTAs:

```css
border: 1px solid var(--borderColor);
border-radius: var(--cardRadius);
padding: 20px 24px;
margin-top: 24px;
```

Contents of the quote card, in order:

1. **Eyebrow** — `<p class="pdp-section-eyebrow"><span aria-hidden="true">—</span> PROJECT QUOTE</p>`. Style the eyebrow as `font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(var(--textColor-rgb),0.5); margin: 0 0 8px;`. The `<span aria-hidden="true">—</span>` is rendered in `color: var(--saleBadgeBackground)` and has `margin-right: 6px`.
2. **Heading** — `<h3>Request a quote on this product</h3>`. Style as `font-family: var(--headingFont); font-size: 18px; font-weight: 600; line-height: 1.25; color: var(--headingColor); margin: 0 0 8px;`.
3. **Sub-text** — `<p>Volume pricing, lead time, OECM PO eligibility, freight, install — all confirmed within 1 business day.</p>`. Style as `font-size: 14px; line-height: 1.5; color: rgba(var(--textColor-rgb),0.7); margin: 0 0 16px;`.
4. **Primary button** — `Request a quote →`. Re-use the existing `pdp-btn--quote` styling (white text on red, BATCH-2 fix). **Critical:** preserve every existing trigger attribute on this button so the modal opens correctly:
   ```
   data-bbi-quote-trigger
   data-lead-type="quote"
   data-product-handle="{{ product.handle }}"
   data-product-title="{{ product.title | escape }}"
   data-variant-id="{{ product.selected_or_first_available_variant.id }}"
   ```
   Button must be `<button type="button">`, not `<a>`. Width 100%, height 48px, font 16px — match the existing `.pdp-btn` base.
5. **Phone line** — `<p class="pdp-quote-card__phone">Or call <a href="tel:18008359565">1-800-835-9565</a></p>`. Style as `font-size: 13px; color: rgba(var(--textColor-rgb),0.6); margin: 12px 0 0; text-align: center;`. The `<a>` is `color: var(--textColor); font-weight: 500; text-decoration: none;`.
6. **Trust line** — `<p class="pdp-quote-card__trust">OECM purchasers welcome · Quotes within 1 business day · Same Ontario team since 1962</p>`. Style as `font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 10px; line-height: 1.5; letter-spacing: 0.04em; color: rgba(var(--textColor-rgb),0.45); margin: 16px 0 0; text-align: center;`.

**1.5 Add-to-Cart for in-stock products.** When `product.available` is true AND `product.price > 0`, render an Add-to-Cart button **above** the quote card (not inside it) as a secondary outline action. Use the existing `pdp-btn--outline` style. Width 100%, height 44px (smaller than the primary 48px to signal secondary). Existing `<form id="pdp-add-to-cart">` wiring stays intact — keep the hidden variant_id input and the submit handler. When `product.available` is false OR `product.price == 0`, the Add-to-Cart row is omitted entirely (only the quote card shows).

**1.6 Trust pills row** — keep the existing `.pdp-trust` block (the `✓ Free delivery / ✓ Same-day quote / etc.` pills). It stays at the bottom of the right column, below the quote card. **Do not include the deleted "Please note: delivery details will appear at checkout" line if it still exists in the file** — search for "Please note" and "delivery details" and remove every match.

**1.7 Phone nudge** — keep `.pdp-phone-nudge` if it currently renders below the trust pills.

### Right-column final order, post-Fix-1

```
vendor → title → SKU + variant count → badges row (OECM + Canadian + availability) → short description (still product.description, single block, no truncation, no read-more) → variant chips → Add-to-Cart button (in-stock only, secondary outline) → quote card (eyebrow + heading + sub-text + primary button + phone line + trust line) → trust pills → phone nudge
```

After Fix 1 is committed and pushed, verify:
```
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'pdp-quote-card'   # expect ≥1
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'pdp-info-section' # expect 0
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'class="pdp-price' # expect 0
```

---

## Fix 2 — Full-width below-fold sections

After `.pdp-main` closes (the right column is inside this), add **two** full-width sections **before** the existing related products section (`.pdp-related`).

### Section A — About

```html
<section class="pdp-about">
  <div class="pdp-about__inner">
    <p class="pdp-section-eyebrow"><span aria-hidden="true">—</span> About this product</p>
    <div class="pdp-about__body">{{ product.description }}</div>
    {%- assign who_for = product.metafields.specs.who_its_for.value -%}
    {%- if who_for != blank -%}
      <div class="pdp-about__best-for">
        <p class="pdp-about__best-for-label">Best for</p>
        <p class="pdp-about__best-for-text">{{ who_for | escape }}</p>
      </div>
    {%- endif -%}
  </div>
</section>
```

CSS:
```
.pdp-about { border-top: 1px solid var(--borderColor); }
.pdp-about__inner { max-width: 760px; margin: 0 auto; padding: 64px 24px; }
.pdp-about__body { font-size: 16px; line-height: 1.7; color: rgba(var(--textColor-rgb),0.85); }
.pdp-about__body p { margin: 0 0 16px; }
.pdp-about__body p:last-child { margin-bottom: 0; }
.pdp-about__best-for { margin-top: 32px; padding-top: 24px; border-top: 1px solid var(--borderColor); }
.pdp-about__best-for-label { font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(var(--textColor-rgb),0.5); margin: 0 0 6px; }
.pdp-about__best-for-text { font-size: 15px; line-height: 1.55; color: var(--textColor); margin: 0; }
```

The eyebrow class `.pdp-section-eyebrow` is already defined in Fix 1.4. Re-use it. Make sure it has `margin: 0 0 16px;` here.

### Section B — Specifications

```html
<section class="pdp-specs-section">
  <div class="pdp-specs-section__inner">
    <p class="pdp-section-eyebrow"><span aria-hidden="true">—</span> Specifications</p>
    <h2 class="pdp-specs-section__heading">Everything we'd put on the spec sheet.</h2>
    <hr class="pdp-specs-section__rule">
    <table class="pdp-specs-table">
      <tbody>
        <!-- Move the existing has_inline_specs Liquid here, with one change: -->
        <!-- Add a Key Features row at the top of the tbody -->
      </tbody>
    </table>
  </div>
</section>
```

CSS:
```
.pdp-specs-section { background: var(--alternateBackground); border-top: 1px solid var(--borderColor); padding: 64px 0; }
.pdp-specs-section__inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.pdp-specs-section__heading { font-family: var(--headingFont); font-size: clamp(24px, 3vw, 32px); font-weight: 600; line-height: 1.15; letter-spacing: -0.015em; color: var(--headingColor); margin: 0 0 24px; }
.pdp-specs-section__rule { border: none; border-top: 1px solid var(--borderColor); margin: 0 0 32px; }

/* Restyled spec table */
.pdp-specs-table { width: 100%; border-collapse: collapse; }
.pdp-specs-table tr { border-bottom: 1px solid var(--borderColor); }
.pdp-specs-table tr:last-child { border-bottom: none; }
.pdp-specs-table th { width: 180px; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(var(--textColor-rgb),0.45); text-align: left; padding: 16px 20px 16px 0; vertical-align: top; }
.pdp-specs-table td { font-size: 15px; line-height: 1.55; color: var(--textColor); padding: 16px 0; vertical-align: top; }
.pdp-specs-table ul { margin: 0; padding: 0 0 0 18px; }
.pdp-specs-table li { margin-bottom: 4px; }
.pdp-specs-table li:last-child { margin-bottom: 0; }

@media (max-width: 640px) {
  .pdp-specs-table tr, .pdp-specs-table th, .pdp-specs-table td { display: block; width: 100%; }
  .pdp-specs-table th { padding: 16px 0 4px; }
  .pdp-specs-table td { padding: 0 0 16px; }
}
```

**Critical:** the existing spec table uses `tr:nth-child(even) { background: var(--alternateBackground); }` and `class="spec-row-even"` alternating rows. **Remove all of that.** No alternating row backgrounds. No outer table border. Just `border-bottom` on each row. Also delete the `assign spec_row_i = 0` and `assign spec_row_m = ...` counter logic and every `<tr{% if spec_row_m == 0 %} class="spec-row-even"{% endif %}>` — replace each with a plain `<tr>`.

### Key Features as a row inside the spec table

The current PDP renders Key Features as a separate bulleted list above the spec table. Move it inside the table as the **first row**:

```liquid
{%- assign s_key_features = product.metafields.specs.key_features.value -%}
{%- if s_key_features != blank and s_key_features.size > 0 -%}
  <tr>
    <th scope="row">Key Features</th>
    <td>
      <ul>
        {%- for f in s_key_features -%}<li>{{ f | escape }}</li>{%- endfor -%}
      </ul>
    </td>
  </tr>
{%- endif -%}
```

If `product.metafields.specs.key_features` is not a list metafield in your store (it might be `product.metafields.custom.key_features` or similar), check the namespace by reading the existing `has_specs` block in the file before Fix 1's deletions — match whatever namespace the existing code uses. Common Shopify pattern is `product.metafields.specs.*` for this theme.

After Key Features, render the existing 11 spec rows (Manufacturer, Product Line, Model, Dimensions, Weight, Weight Capacity, Materials, Finishes Available, Certifications, Warranty, Made In) — same conditional checks as before, just with the alternating-row class stripped.

**Remove the existing `.pdp-features` and `.pdp-specs` standalone blocks** (the ones that previously rendered Key Features as bullets and the spec table as a card). They are replaced by Section B.

### Section ordering after `.pdp-main`

```
.pdp-main (existing)
.pdp-about (Fix 2 Section A)
.pdp-specs-section (Fix 2 Section B)
.pdp-related (existing — UNCHANGED)
.pdp-cta-closer (existing — UNCHANGED)
```

After Fix 2 is committed and pushed, verify:
```
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'pdp-about'              # expect ≥1
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'pdp-specs-section'      # expect ≥1
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'spec-row-even'          # expect 0
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -c 'pdp-features'           # expect 0
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -B2 'Key Features' | head   # expect <th>Key Features</th> inside the table, not <h*>
```

Test on a product with no specs metafields too (e.g. https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873 if sparse, or any sparse-spec product) — the Specifications section should still render the heading + horizontal rule even if the table body is empty, OR be wrapped in `{%- if has_specs -%}` to hide the whole section when there's nothing to show. Choose the wrap-in-if approach.

---

## Fix 3 — Variant price data (one-line data fix)

Find the `<script id="pdp-variants-data" type="application/json">` block. It currently emits one entry per variant:

```liquid
{
  "id": {{ variant.id }},
  "available": {{ variant.available }},
  "options": {{ variant.options | json }}
}
```

Add `price` and `compare_at_price`:

```liquid
{
  "id": {{ variant.id }},
  "available": {{ variant.available }},
  "price": {{ variant.price }},
  "compare_at_price": {{ variant.compare_at_price | default: 0 }},
  "options": {{ variant.options | json }}
}
```

Shopify outputs prices in **cents** (integer) via `{{ variant.price }}`. The existing `BbiPdpVariants._updateFormId()` handler in the `<script>` block at the bottom of the file may or may not already update a price element. Check it. If it does not, add the following inside `_updateFormId()` after the `idInput.value = match.id;` line:

```js
// Update visible price (Shopify prices are in cents)
const priceEl = document.querySelector('.pdp-quote-card__price');
if (priceEl && match.price != null) {
  priceEl.textContent = new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: 'CAD'
  }).format(match.price / 100);
}
```

If you add the price line, also add a `<p class="pdp-quote-card__price">{{ product.selected_or_first_available_variant.price | money }}</p>` element inside the quote card from Fix 1.4, between the sub-text and the primary button. Style it as `font-family: var(--headingFont); font-size: 22px; font-weight: 600; color: var(--headingColor); margin: 0 0 16px;`. When `product.price == 0` (showcase product), hide the price element with `{% unless product.price == 0 %} ... {% endunless %}`.

After Fix 3 is committed and pushed, verify:
```
curl '<test-url>' -H 'User-Agent: Mozilla/5.0' -s | grep -A1 'pdp-variants-data' | head -20  # expect price + compare_at_price keys
```

Then open the test URL in a browser, click each size chip, and confirm the displayed price changes between variants.

---

## What NOT to change

- `<bbi-pdp-gallery>` web component and all gallery CSS — leave it intact
- Breadcrumb logic / `.pdp-breadcrumb` — leave it intact
- Related products section (`.pdp-related`) — leave it intact
- CTA-closer section at bottom of page (`.pdp-cta-closer`) — leave it intact
- All `data-bbi-quote-trigger` wiring — preserve every attribute on every quote button (modal integration must keep working)
- `BbiPdpVariants` web component class definition — only Fix 3 touches `_updateFormId()`, and only by adding the price-update lines
- Any other section, snippet, layout, or template file — only `theme/sections/ds-pdp-base.liquid`
- The `bbi_landing` gate in `theme/layout/theme.liquid` — already correct
- `theme/snippets/bbi-product-jsonld.liquid` — already correct
- `theme/snippets/bbi-breadcrumb-jsonld.liquid` — already correct

---

## Verification (after all three commits + pushes)

Open the test URL in an authenticated Shopify admin browser session:

```
https://office-central-online.myshopify.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873
```

Confirm:

1. Right column ends at trust pills — no About / Key Features / Specifications content sits beside the image
2. "About this product" appears as a centered, narrow (760px) full-width section below the gallery + right column
3. "Specifications" appears as a wider (1200px) full-width section with a tinted background, below About
4. Inside the Specifications table, "Key Features" is the first row (`<th>Key Features</th>`) and the bulleted list is in the `<td>`
5. The standalone Key Features bullet list block is gone
6. The standalone spec table card with alternating gray rows is gone
7. Quote card renders in the right column with eyebrow `— PROJECT QUOTE`, heading "Request a quote on this product", sub-text, "Request a quote →" button (white text on red), phone line, trust line
8. Clicking "Request a quote →" opens the modal (no navigation)
9. Selecting a size chip updates the price displayed inside the quote card
10. OECM badge and Canadian-Made badge render in the badges row when those tags are present on the product
11. For an in-stock priced product, Add-to-Cart appears as a small outline button above the quote card. For a sold-out or $0 product, Add-to-Cart is omitted and only the quote card renders.
12. No Liquid syntax errors. No `Please note` text anywhere.

Run a console check:
```js
document.querySelectorAll('.bbi-header').length === 1
document.querySelectorAll('.bbi-footer').length === 1
document.querySelectorAll('.pdp-quote-card').length === 1
document.querySelectorAll('.pdp-info-section').length === 0
document.querySelector('[data-bbi-quote-trigger]').click() // modal should open
```

If anything fails, surface the failure with the exact selector / grep that returned the unexpected count, and stop. Do not push more changes until the failure is diagnosed.

---

## Final commit + summary

After all three fixes pass verification, output to me:

1. The three commit SHAs in order (`git log --oneline -3`)
2. A one-line summary per fix of what changed
3. The verification results (12 checklist items)
4. Anything that surprised you during the work (e.g. metafield namespace differed, an existing class was reused, etc.)

Do not update `docs/plan/bbi-build-state.md` in this session — the build-state row will be added in a separate pass that bundles this with other polish items.
