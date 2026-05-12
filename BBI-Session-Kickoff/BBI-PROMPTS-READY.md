# BBI — Prompts Ready to Run
**Last updated:** 2026-05-11 | Each prompt is self-contained — paste directly into a fresh Claude Code session.

---

## Completed this session ✅

| Prompt | What it did |
|---|---|
| Liquid/translation bugs | `compare-products-content` gated; `theme-variables` stub created; `side-drawer` stub confirmed |
| PDP price + width + quote pre-fill | Price above variants; `.pdp-about` full width; quote modal pre-fills product name |
| Collection Shop All + All filter | "Shop All" and "All" chip now show flat product grid |
| PDP button hierarchy + quote strip | Add to Cart promoted to first; Buy Now demoted to outline; quote card compressed to one-line strip — **deployed but unverifiable: page renders black** |

---

## 🔴 Currently stuck — black product page

Every product page on the dev theme renders black. Root cause: dev theme's active colour scheme is dark (`#0B0B0C`). Load order means `style-variables.liquid` sets a dark body before any section CSS can override it.

**Already tried and failed:**
- `body { background: #FFFFFF !important }` in `ds-pdp-base.liquid` section `<style>`
- `min-height: 100vh` on `.bbi-pdp`

**Fix:** Patch `config/settings_data.json` on the dev theme via API to switch to the light colour scheme, OR inject the override directly in `theme/layout/theme.liquid` before any other stylesheet. See Prompt 0 below.

---

## Run order — remaining prompts

| # | Prompt | Priority | Can parallel? |
|---|---|---|---|
| **0** | **🔴 Fix black product page** | **First — blocking all PDP QA** | No |
| 1 | **Cart 404 fix** | 🔴 Second — blocking purchases | No |
| 2 | **Buy Now + Quantity selector** | 🟠 Third — needs cart working | No |
| 3 | **Other products like this** | 🟡 Any time after #1 | Yes |
| 4 | **Product descriptions + specs overhaul** | 🟡 Any time | Yes — no theme files |
| 5 | **Hero + sub-hero photo audit** | 🟢 Any time | Yes — read only |
| 6 | **Empty subcollections audit** | 🟢 Any time | Yes — read only |

---

## Prompt 0 — Fix black product page 🔴

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Bug: every product page renders a black background.

Root cause confirmed by audit: the dev theme's active colour scheme is
dark (#0B0B0C body). The load order is:
  1. style-variables.liquid sets body { background-color: rgb(11,11,12) }
  2. bbi-homepage.css reinforces it
  3. Section-level !important in ds-pdp-base.liquid does NOT win

Already tried and failed:
  - body { background: #FFFFFF !important } in ds-pdp-base.liquid
  - min-height: 100vh on .bbi-pdp

─── Step 1: Read current dev theme colour scheme ────────────────────
export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import requests, os, json

shop = "office-central-online.myshopify.com"
token = os.environ["SHOPIFY_TOKEN"]
headers = {"X-Shopify-Access-Token": token}

r = requests.get(
    f"https://{shop}/admin/api/2024-01/themes/186373570873/assets.json"
    f"?asset[key]=config/settings_data.json",
    headers=headers
)
data = json.loads(r.json()["asset"]["value"])

with open("data/backups/settings_data-backup-pre-lightmode.json", "w") as f:
    json.dump(data, f, indent=2)

current = data.get("current", {})
print("Keys in current settings:")
for k, v in current.items():
    if any(x in k.lower() for x in ["color", "background", "scheme"]):
        print(f"  {k}: {v}")
EOF

Report the exact key names and values for any color/background/scheme
settings before continuing.

─── Fix A: Patch settings_data.json to use light colour scheme ──────
Based on Step 1 output, identify the key that controls the body
background. Common patterns (check which applies):

Pattern 1 — direct hex value:
  data["current"]["colors_background_1"] = "#ffffff"

Pattern 2 — color scheme reference:
  data["current"]["color_scheme"] = "scheme_2"  (or whichever is light)

Pattern 3 — nested scheme object:
  data["current"]["color_schemes"]["scheme-1"]["background"] = "#ffffff"

Apply the correct patch, then push:

python3 - <<'EOF'
import requests, os, json

shop = "office-central-online.myshopify.com"
token = os.environ["SHOPIFY_TOKEN"]
headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

with open("data/backups/settings_data-backup-pre-lightmode.json") as f:
    data = json.load(f)

# [Apply correct patch from Step 1 findings here]

r = requests.put(
    f"https://{shop}/admin/api/2024-01/themes/186373570873/assets.json",
    headers=headers,
    json={"asset": {"key": "config/settings_data.json",
                    "value": json.dumps(data)}}
)
print(f"HTTP {r.status_code}")
print(r.json())
EOF

─── Fix B: If Fix A doesn't resolve — inject in theme.liquid ────────
Open theme/layout/theme.liquid. In the <head> block, immediately
BEFORE the closing </head> tag (so it loads last and wins), add:

  {%- if template == 'product' -%}
  <style>
    html, body {
      background-color: #ffffff !important;
      background: #ffffff !important;
    }
  </style>
  {%- endif -%}

Push:
  export $(grep -v '^#' .env | xargs) && \
    BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py \
    186373570873 --layout

─── Fix C: If both A and B fail — remove dark scheme from source ─────
Open theme/snippets/style-variables.liquid (or theme-variables.liquid).
Find where --background is set. If it's hardcoded to a dark value
(e.g. 11,11,12), override it for product templates:

  {%- if template == 'product' -%}
    :root { --background: 255,255,255; }
  {%- endif -%}

Push via --snippets flag.

─── Step 3: Verify ───────────────────────────────────────────────────
Test both URLs — they were previously black:
  https://office-central-online.myshopify.com/products/vertical-file-2-drawer-letter?preview_theme_id=186373570873
  https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873

Confirm white background, product content visible, CTA buttons readable.
Also verify the button layout is correct:
  1. Quantity selector (−/input/+)
  2. Buy Now (slim outline button)  ← already deployed
  3. Add to Cart (dominant primary, black)  ← already deployed
  4. Compact quote strip (one line: outline button + phone)  ← already deployed

Commit message: "Fix product page black background: patch dev theme colour scheme"
```

---

## Prompt 1 — Cart 404 fix 🔴

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Bug: clicking Add to Cart on a product page results in a 404.

─── Step 1: Diagnose before touching anything ───────────────────────
1. Check whether theme/templates/cart.json or theme/templates/cart.liquid
   exists. Report which one is present or if neither exists.

2. Open theme/sections/ds-pdp-base.liquid and find the Add to Cart
   button. Report:
   - Does it have data-bbi-quote-trigger? (quote modal, not ATC)
   - Does it POST to /cart/add.js or redirect to /cart?
   - Is there a <form action="/cart/add"> wrapping it?

3. Open theme/layout/theme.liquid lines 162–177. The cart drawer
   render reads:
     if template != 'cart' and bbi_landing == false
   Since product pages have bbi_landing = true (line 91), the cart
   drawer never loads on PDPs. Confirm whether this is the root cause.

Report all three findings before making any edits.

─── Step 2: Fix based on findings ───────────────────────────────────
Option A — Cart drawer missing on product pages (most likely cause):
  In theme/layout/theme.liquid, change line 173 from:
    if template != 'cart' and bbi_landing == false
  to:
    if template != 'cart'
  This lets the cart drawer render on bbi_landing pages (product,
  collection) while still suppressing it on the cart page itself.

Option B — No cart template exists:
  If theme/templates/cart.json is missing, create it:
    {
      "sections": {
        "main": {
          "type": "main-cart-items",
          "settings": {}
        }
      },
      "order": ["main"]
    }
  Then confirm theme/sections/main-cart-items.liquid exists.

Option C — ATC button has data-bbi-quote-trigger incorrectly:
  In theme/sections/ds-pdp-base.liquid, ensure data-bbi-quote-trigger
  is ONLY on the "Request a Quote" button, not the Add to Cart button.
  The ATC button should POST to /cart/add via a standard Shopify form.

Apply whichever option(s) the diagnosis points to. More than one may
be needed.

─── Push command ─────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py \
  186373570873 --layout

Confirm HTTP 200 for each file pushed. Then test by adding a product
to cart on the dev theme and confirming the cart drawer opens or
/cart loads without a 404.
Commit message: "Fix cart 404: restore cart drawer on product pages"
```

---

## Prompt 2 — Buy Now button + Quantity selector 🟠

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Primary file: theme/sections/ds-pdp-base.liquid

Add a quantity selector and a Buy Now button to the product page.
Read ds-pdp-base.liquid fully before making any edits.

CRITICAL — do not break these:
- All data-bbi-quote-trigger attributes (wires the quote modal)
- The BbiPdpVariants Web Component and its JS (chip selection,
  price update)
- The bbi-pdp-gallery Web Component and its JS
- The existing Add to Cart button and its form

─── CHANGE 1: Quantity selector ─────────────────────────────────────
Find the Add to Cart button inside ds-pdp-base.liquid. Directly above
it, add a quantity stepper:

  <div class="pdp-quantity">
    <button class="pdp-quantity__btn" data-quantity-minus
            aria-label="Decrease quantity" type="button">−</button>
    <input class="pdp-quantity__input"
           type="number"
           name="quantity"
           id="pdp-quantity-input"
           value="1"
           min="1"
           aria-label="Quantity">
    <button class="pdp-quantity__btn" data-quantity-plus
            aria-label="Increase quantity" type="button">+</button>
  </div>

CSS:
  .pdp-quantity {
    display: flex;
    align-items: center;
    border: 1px solid var(--borderColor);
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
    cursor: pointer;
    color: var(--textColor);
    line-height: 1;
    transition: background 0.15s;
  }
  .pdp-quantity__btn:hover {
    background: var(--alternateBackground);
  }
  .pdp-quantity__input {
    width: 48px;
    text-align: center;
    border: none;
    border-left: 1px solid var(--borderColor);
    border-right: 1px solid var(--borderColor);
    font-size: 15px;
    padding: 10px 0;
    -moz-appearance: textfield;
    color: var(--textColor);
    background: none;
  }
  .pdp-quantity__input::-webkit-outer-spin-button,
  .pdp-quantity__input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }

Add JS inline (after the existing Web Component scripts, not before):
  document.addEventListener('DOMContentLoaded', function () {
    const minus = document.querySelector('[data-quantity-minus]');
    const plus  = document.querySelector('[data-quantity-plus]');
    const input = document.getElementById('pdp-quantity-input');
    if (!minus || !plus || !input) return;
    minus.addEventListener('click', function () {
      const val = parseInt(input.value, 10);
      if (val > 1) input.value = val - 1;
    });
    plus.addEventListener('click', function () {
      input.value = parseInt(input.value, 10) + 1;
    });
  });

Make sure the quantity input's name="quantity" is inside the product
<form> so it is submitted with the Add to Cart POST.

─── CHANGE 2: Buy Now button ─────────────────────────────────────────
Directly ABOVE the Add to Cart button (and below the quantity
selector), add a Buy Now button:

  <button type="button"
          class="pdp-btn pdp-btn--primary pdp-btn--buy-now"
          data-buy-now>
    Buy now
  </button>

CSS:
  .pdp-btn--buy-now {
    width: 100%;
    margin-bottom: 10px;
    background: var(--textColor);
    color: var(--background);
    border: 2px solid var(--textColor);
  }
  .pdp-btn--buy-now:hover {
    opacity: 0.85;
  }

JS (alongside quantity JS):
  document.addEventListener('DOMContentLoaded', function () {
    const buyNow = document.querySelector('[data-buy-now]');
    if (!buyNow) return;
    buyNow.addEventListener('click', async function () {
      buyNow.disabled = true;
      buyNow.textContent = 'Adding…';
      try {
        const variantInput = document.querySelector(
          '[name="id"], [data-selected-variant]'
        );
        const variantId = variantInput
          ? (variantInput.value || variantInput.dataset.selectedVariant)
          : null;
        const qty = parseInt(
          document.getElementById('pdp-quantity-input')?.value || '1', 10
        );
        if (!variantId) throw new Error('No variant selected');
        await fetch('/cart/add.js', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: variantId, quantity: qty })
        });
        window.location.href = '/checkout';
      } catch (e) {
        buyNow.disabled = false;
        buyNow.textContent = 'Buy now';
        console.error('Buy Now failed:', e);
      }
    });
  });

─── Final CTA stack order (top to bottom) ────────────────────────────
  1. Quantity selector
  2. Buy Now (black, full width)
  3. Add to Cart (existing, full width)
  4. Request a Quote card (.pdp-quote-card)

─── Push command ─────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873

Confirm HTTP 200. Test:
- Quantity stepper increments and decrements correctly
- Buy Now adds to cart and lands on /checkout
- Add to Cart still opens the cart drawer
- Quote card and data-bbi-quote-trigger are untouched
Commit message: "Add quantity selector and Buy Now button to PDP"
```

---

## Prompt 3 — Other products like this (3-tier fallback) 🟡

```
You are working on BBI Shopify dev theme (ID: 186373570873).
File: theme/sections/ds-pdp-base.liquid

Fix: the "Other products like this" / related products section at the
bottom of every PDP must always show products. Currently it can render
empty if no products share the same type tag as the current product.

─── Read the current implementation first ───────────────────────────
Open theme/sections/ds-pdp-base.liquid and find the .pdp-related
section. Read exactly how it currently queries related products
before making any changes. Report what you find.

─── Fix: 3-tier fallback logic ──────────────────────────────────────
TIER 1 — Same product type tag:
  {%- assign type_tag = product.tags | where_exp: "t", "t contains 'type:'" | first -%}
  {%- if type_tag != blank -%}
    {%- assign related_collection_handle = 'all-' | append: type_tag | remove: 'type:' -%}
    {%- assign tier1_products = collections[related_collection_handle].products
        | where_exp: "p", "p.id != product.id" | slice: 0, 4 -%}
  {%- endif -%}

TIER 2 — Same parent category (if Tier 1 empty):
  {%- if tier1_products.size == 0 -%}
    {%- assign category_tag = product.tags
        | where_exp: "t", "t contains 'room:'" | first -%}
    {%- if category_tag != blank -%}
      {%- assign cat_handle = category_tag | remove: 'room:' -%}
      {%- assign tier2_products = collections[cat_handle].products
          | where_exp: "p", "p.id != product.id" | slice: 0, 4 -%}
    {%- endif -%}
  {%- endif -%}

TIER 3 — Same Shopify product_type (if Tiers 1+2 empty):
  {%- if tier1_products.size == 0 and tier2_products.size == 0 -%}
    {%- assign tier3_products = collections['business-furniture'].products
        | where_exp: "p", "p.type == product.type and p.id != product.id"
        | slice: 0, 4 -%}
  {%- endif -%}

  {%- assign related_products = tier1_products
      | default: tier2_products
      | default: tier3_products -%}

Hide section entirely if all tiers empty:
  {%- if related_products.size > 0 -%}
    <section class="pdp-related"> … </section>
  {%- endif -%}

Heading reflects which tier matched:
  {%- if tier1_products.size > 0 -%}
    {%- assign related_label = 'Other ' | append: type_tag
        | remove: 'type:' | append: ' products' | capitalize -%}
  {%- else -%}
    {%- assign related_label = 'You might also like' -%}
  {%- endif -%}

─── Push command ─────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873

Test on 3 products: a Hero with type tags (Tier 1), a product with
room: tag only (Tier 2), additional-services (Tier 3 or hidden).
Commit message: "Fix PDP related products: 3-tier fallback always shows products"
```

---

## Prompt 4 — Product descriptions + specs overhaul 🟡

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

The Hero 100 products already have enriched descriptions, spec
metafields, and SEO meta (PE-1, PE-2, PE-4 in docs/plan/bbi-build-state.md).
The remaining ~500 non-Hero products do not.

Task: audit the gap, then run a phased enrichment pass.

─── Step 1: Audit current state ─────────────────────────────────────
  export $(grep -v '^#' .env | xargs)

  python3 - <<'EOF'
  import requests, json, os, csv

  shop = "office-central-online.myshopify.com"
  token = os.environ["SHOPIFY_TOKEN"]
  headers = {"X-Shopify-Access-Token": token}

  products, url = [], (
      f"https://{shop}/admin/api/2024-01/products.json"
      f"?limit=250&fields=id,title,tags,body_html,"
      f"metafields_global_title_tag,metafields_global_description_tag"
  )
  while url:
      r = requests.get(url, headers=headers)
      products += r.json().get("products", [])
      link = r.headers.get("Link", "")
      url = next((p.split(";")[0].strip("<>") for p in link.split(",")
                  if 'rel="next"' in p), None)

  rows = []
  for p in products:
      is_hero = "hero" in p.get("tags", "").lower()
      has_desc = bool(p.get("body_html", "").strip())
      mf_url = (f"https://{shop}/admin/api/2024-01/products/"
                f"{p['id']}/metafields.json?namespace=specs")
      mf = requests.get(mf_url, headers=headers).json().get("metafields", [])
      spec_keys = [m["key"] for m in mf]
      rows.append({
          "id": p["id"], "title": p["title"], "hero": is_hero,
          "has_description": has_desc, "spec_count": len(spec_keys),
          "spec_keys": ", ".join(spec_keys),
          "has_seo_title": bool(p.get("metafields_global_title_tag")),
          "has_seo_desc": bool(p.get("metafields_global_description_tag")),
      })

  with open("data/reports/product-enrichment-gap.csv", "w", newline="") as f:
      w = csv.DictWriter(f, fieldnames=rows[0].keys())
      w.writeheader(); w.writerows(rows)

  no_desc  = [r for r in rows if not r["has_description"] and not r["hero"]]
  no_specs = [r for r in rows if r["spec_count"] == 0 and not r["hero"]]
  no_seo   = [r for r in rows if not r["has_seo_title"] and not r["hero"]]
  print(f"Total: {len(rows)} | Hero: {sum(1 for r in rows if r['hero'])}")
  print(f"Missing desc: {len(no_desc)} | specs: {len(no_specs)} | SEO: {len(no_seo)}")
  EOF

Report the four counts before continuing.

─── Step 2: Descriptions for non-Hero products ──────────────────────
Read docs/strategy/icp.md and docs/strategy/voice-samples.md first.

For each non-Hero product missing body_html, generate 2–3 paragraphs:
- P1: what the product is + primary use case
- P2: key functional features (infer from title + type only)
- P3: who it's for (school boards, hospitals, government, professional
  services)
- Do NOT fabricate dimensions, weights, or model numbers

Batch in groups of 25. After each batch:
  1. Write drafts to data/reports/description-drafts-batch-N.json
  2. Push via Shopify API (product UPDATE, field: body_html)
  3. Log to data/logs/description-push-YYYY-MM-DD.json
  4. Confirm HTTP 200 before next batch

─── Step 3: Core spec metafields for non-Hero products ──────────────
For each non-Hero product with 0 spec metafields, add at minimum:
- specs.material (infer from title/type)
- specs.warranty ("1 year limited warranty" default)
- specs.assembly ("Assembly required" or "Ships assembled")

Match the API shape in scripts/push-spec-metafields.py exactly.

─── Step 4: SEO meta ────────────────────────────────────────────────
For each non-Hero product missing metafields_global_title_tag:
- Title: "[Product Title] | Brant Business Interiors" (max 60 chars)
- Description: one sentence, max 155 chars — what + who + "Canadian
  institutional supplier"

No theme files touched. No bbi-push-landing.py needed.
Commit: "PE-5/6/7: non-Hero product description + spec + SEO enrichment"
```

---

## Prompt 5 — Hero + sub-hero photo audit 🟢

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Task: find every section with a hero or sub-hero image slot, check
what image is currently set or missing, and flag which slots need a
photo chosen. Read-only — do not change any files.

─── Step 1: Find all image slots ────────────────────────────────────
  grep -rn \
    "image_picker\|hero.*image\|image.*hero\|sub.hero\|background_image\|banner_image\|page-images" \
    theme/sections/ theme/snippets/ \
    --include="*.liquid" -l

  grep -n '"type": "image_picker"' \
    theme/sections/*.liquid theme/snippets/*.liquid

Report every section file + setting ID of each image slot found.

─── Step 2: Check which slots are populated ─────────────────────────
  export $(grep -v '^#' .env | xargs)

  python3 - <<'EOF'
  import os, json, glob, re, csv

  templates = {}
  for path in glob.glob("theme/templates/*.json"):
      with open(path) as f:
          try: templates[os.path.basename(path)] = json.load(f)
          except: pass

  image_slots = []
  for path in glob.glob("theme/sections/*.liquid"):
      content = open(path).read()
      if '"image_picker"' not in content:
          continue
      section_name = os.path.basename(path).replace(".liquid", "")
      ids = re.findall(
          r'"type":\s*"image_picker"[^}]*?"id":\s*"([^"]+)"',
          content, re.DOTALL)
      ids += re.findall(
          r'"id":\s*"([^"]+)"[^}]*?"type":\s*"image_picker"',
          content, re.DOTALL)
      for sid in set(ids):
          image_slots.append({
              "section": section_name, "setting_id": sid,
              "populated": False, "current_value": None
          })

  for slot in image_slots:
      for tname, tdata in templates.items():
          for skey, sdata in tdata.get("sections", {}).items():
              if sdata.get("type", "") == slot["section"]:
                  val = sdata.get("settings", {}).get(slot["setting_id"])
                  if val:
                      slot["populated"] = True
                      slot["current_value"] = val

  page_images = [p for p in glob.glob("data/page-images/**/*", recursive=True)
                 if p.endswith((".jpg",".jpeg",".png",".webp"))]

  with open("data/reports/image-slot-audit.csv", "w", newline="") as f:
      w = csv.DictWriter(f, fieldnames=["section","setting_id","populated","current_value"])
      w.writeheader(); w.writerows(image_slots)

  empty  = [s for s in image_slots if not s["populated"]]
  filled = [s for s in image_slots if s["populated"]]
  print(f"Total slots: {len(image_slots)} | Populated: {len(filled)} | Empty: {len(empty)}")
  print(f"Available in data/page-images/: {len(page_images)}")
  print("\nEMPTY SLOTS:")
  for s in empty:
      print(f"  {s['section']} → {s['setting_id']}")
  EOF

─── Step 3: Match photos to empty slots ─────────────────────────────
List data/page-images/ and for each empty slot suggest the best photo
by matching filename keywords to section name. Flag "NEEDS NEW PHOTO"
if no match exists.

─── Step 4: Output table ────────────────────────────────────────────
  | Section | Setting ID | Status | Current value / Suggestion |

Save to: data/reports/image-slot-audit.csv. No push needed.
```

---

## Prompt 6 — Empty subcollections audit 🟢

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Task: find every collection with zero products and check whether each
can be auto-populated with a Shopify smart collection rule.
Read-only — do not modify any collection data.

─── Step 1: Pull all collections + product counts ───────────────────
  export $(grep -v '^#' .env | xargs)

  python3 - <<'EOF'
  import requests, json, os

  shop = "office-central-online.myshopify.com"
  token = os.environ["SHOPIFY_TOKEN"]
  headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

  collections, url = [], f"https://{shop}/admin/api/2024-01/custom_collections.json?limit=250"
  while url:
      r = requests.get(url, headers=headers)
      collections += r.json().get("custom_collections", [])
      link = r.headers.get("Link", "")
      url = next((p.split(";")[0].strip("<>") for p in link.split(",")
                  if 'rel="next"' in p), None)

  smart, url2 = [], f"https://{shop}/admin/api/2024-01/smart_collections.json?limit=250"
  while url2:
      r = requests.get(url2, headers=headers)
      smart += r.json().get("smart_collections", [])
      link = r.headers.get("Link", "")
      url2 = next((p.split(";")[0].strip("<>") for p in link.split(",")
                   if 'rel="next"' in p), None)

  empty = []
  for kind, c in [("custom", c) for c in collections] + [("smart", c) for c in smart]:
      count = requests.get(
          f"https://{shop}/admin/api/2024-01/collections/{c['id']}/products/count.json",
          headers=headers).json().get("count", 0)
      if count == 0:
          empty.append({
              "id": c["id"], "type": kind, "title": c["title"],
              "handle": c["handle"], "rules": c.get("rules", [])
          })

  with open("data/reports/empty-collections-audit.json", "w") as f:
      json.dump(empty, f, indent=2)
  print(f"Total empty: {len(empty)}")
  print(json.dumps(empty, indent=2))
  EOF

─── Step 2: Smart collection viability check ────────────────────────
  python3 - <<'EOF'
  import requests, json, os

  shop = "office-central-online.myshopify.com"
  token = os.environ["SHOPIFY_TOKEN"]
  headers = {"X-Shopify-Access-Token": token}

  with open("data/reports/empty-collections-audit.json") as f:
      empty = json.load(f)

  suggestions = []
  for c in [c for c in empty if c["type"] == "custom"]:
      tag_count = requests.get(
          f"https://{shop}/admin/api/2024-01/products/count.json?tag={c['handle']}",
          headers=headers).json().get("count", 0)
      type_count = requests.get(
          f"https://{shop}/admin/api/2024-01/products/count.json?product_type={c['title']}",
          headers=headers).json().get("count", 0)
      suggestions.append({
          "collection": c["title"], "handle": c["handle"],
          "products_matching_tag": tag_count,
          "products_matching_type": type_count,
          "smart_collection_viable": tag_count > 0 or type_count > 0,
          "suggested_rule": (
              f"tag = {c['handle']}" if tag_count > 0 else
              f"product_type = {c['title']}" if type_count > 0 else
              "no automatic rule — manual curation needed"
          )
      })

  with open("data/reports/empty-collections-smart-suggestions.json", "w") as f:
      json.dump(suggestions, f, indent=2)
  viable = [s for s in suggestions if s["smart_collection_viable"]]
  manual = [s for s in suggestions if not s["smart_collection_viable"]]
  print(f"Smart fix viable: {len(viable)} | Manual needed: {len(manual)}")
  print(json.dumps(suggestions, indent=2))
  EOF

─── Step 3: Output table + flag issues ──────────────────────────────
Print:
  | Collection | Handle | Type | Smart fix? | Suggested rule |

Also flag:
- Smart collections empty despite having rules (misconfigured)
- Sub-collection handles (contain a dash) with no parent linking to them
- Near-duplicates (same name, one empty, one has products)

Save to:
  data/reports/empty-collections-audit.json
  data/reports/empty-collections-smart-suggestions.json

Do NOT modify any collection. Report only.
```
