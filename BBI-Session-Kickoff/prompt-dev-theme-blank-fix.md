# Fix: Dev Theme Blank/White Product Pages

## Goal
The BBI Landing Dev theme (ID: 186373570873) renders a completely blank page on all product URLs. The live theme (178274435385, BBI Live) is working correctly. Fix the dev theme so product pages render.

## Store
- Store: office-central-online.myshopify.com / www.brantbusinessinteriors.com
- Token: in `.env` as `SHOPIFY_TOKEN`
- **Push only to dev theme 186373570873 — never to live 178274435385**

## What we know

### Dev theme architecture
- Product template: `theme/templates/product.json` → section `ds-pdp-base` → `theme/sections/ds-pdp-base.liquid`
- Layout: `theme/layout/theme.liquid` (locally modified, changes pushed to dev)
- The dev theme is a Starlite-based theme with BBI custom sections layered on top

### What was pushed to dev this session (some of it broke things)
1. `sections/ds-pdp-base.liquid` — BBI custom PDP section (CSS-only change, safe)
2. `layout/theme.liquid` — adds white body override for product pages + dark mode skip on PDPs (see diff below)
3. `snippets/style-variables.liquid` — **pushed a broken version** with `25,,255,255` double-comma CSS bug inside a `{% style %}` block; **then reverted to clean committed version and re-pushed** — should be fixed
4. `snippets/theme-variables.liquid` — **pushed a version that loaded the full Starlite CSS/JS stack**; **then reverted to stub and re-pushed** — should be fixed

### Current state of dev theme assets (what was last pushed)
- `style-variables.liquid` → clean committed version (289 lines, no double-comma)
- `theme-variables.liquid` → stub: `{%- comment -%}theme-variables stub{%- endcomment -%}`
- `theme.liquid` → modified version with white-body override + dark-mode JS skip on product pages
- `ds-pdp-base.liquid` → local version with minor CSS tweak

### theme.liquid changes (already pushed to dev)
```diff
+ {%- if template == 'product' -%}
+ <style>
+   html[color-mode] body, html[color-mode="dark"] body, html body, body {
+     background-color: #ffffff !important;
+     background: #ffffff !important;
+   }
+ </style>
+ {%- endif -%}

+ elsif template == 'cart'
+   assign bbi_landing = true

- if (localStorage.darkMode == 'true') {
+ if (localStorage.darkMode == 'true' && {{ template | json }} !== 'product') {
```

### Background: why pages were blank before
The Starlite dev theme's first color scheme has `background: #0B0B0C` (dark). `style-variables.liquid` applies `:root { --background: 0,0,0 }` from the first scheme. The base Starlite CSS (`style.css`) sets `body { background: rgb(var(--background)) }` which makes the body black. Then if dark mode localStorage is set, `html[color-mode="dark"]` compounds it. Our `ds-pdp-base.liquid` has `body { background: #FFFFFF !important }` which should win — but the session ended with pages still blank.

## Diagnostic steps (do these first)

1. **Fetch the dev theme's live `theme.liquid`** from Shopify API and check it for Liquid syntax errors — particularly around the `{%- if template == 'product' -%}` block we added:
   ```python
   GET themes/186373570873/assets.json?asset[key]=layout/theme.liquid
   ```

2. **Fetch `snippets/style-variables.liquid`** from the dev theme and check for double-commas or malformed CSS inside `{% style %}` blocks:
   ```python
   GET themes/186373570873/assets.json?asset[key]=snippets/style-variables.liquid
   ```

3. **Fetch `snippets/theme-variables.liquid`** — confirm it's the stub (1 line comment), not the full Starlite asset loader.

4. **Fetch `sections/ds-pdp-base.liquid`** — validate Liquid tag balance (all `if/for/unless` have matching `endif/endfor/endunless`).

5. **Check the dev theme's `config/settings_data.json`** — confirm which color scheme is active as the first/default:
   ```python
   GET themes/186373570873/assets.json?asset[key]=config/settings_data.json
   ```
   Look at `current.color_schemes` — the first key's `background` value determines `:root --background`.

## Fix strategy

**Option A (preferred):** If `theme.liquid` or `style-variables.liquid` on the dev theme has a Liquid/CSS error → fix the specific error and push just that file.

**Option B:** If `style-variables.liquid` on dev still has the broken version (with `25,,255,255`) → push the clean local version (`git checkout HEAD -- theme/snippets/style-variables.liquid` then push).

**Option C:** If the dev theme's first color scheme is dark → patch `settings_data.json` to put the `primary` scheme (background `#FFFFFF`) first, then upload it.

**Option D (nuclear):** Pull the full dev theme, diff against local, identify any asset that's out of sync, and push the corrected set.

## Test URL
```
https://www.brantbusinessinteriors.com/products/l-shape-loop-leg-desk?preview_theme_id=186373570873
https://www.brantbusinessinteriors.com/products/vion-mesh-high-back-chair-1?preview_theme_id=186373570873
```
Page should render with: header, product gallery, price, Add to Cart / Request a Quote CTA, About This Product section, WHO IT'S FOR section, Specifications table, related products, footer.

## Safety rules
- Push ONLY to theme 186373570873
- Never push to 178274435385 (live)
- Confirm each push with `--only` flag targeting specific files
- `config/settings_data.json` is in `.gitignore` — do not commit it
