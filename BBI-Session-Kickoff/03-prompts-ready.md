# BBI — Prompts Ready to Run
**Last updated:** 2026-05-11 | Paste each prompt directly into a fresh Claude Code session.

---

## Run order

| # | Prompt | Priority | Can parallel? |
|---|---|---|---|
| **0** | **Fix black product page** | 🔴 First — blocking all PDP QA | No |
| 1 | Cart 404 fix | 🔴 Second — blocking purchases | No |
| 2 | Buy Now + Quantity selector | 🟠 Third — needs cart first | No |
| 3 | Other products like this | 🟡 Any time after #1 | Yes |
| 4 | Product descriptions + specs overhaul | 🟡 Any time | Yes — no theme files |
| 5 | Hero + sub-hero photo audit | 🟢 Any time | Yes — read only |
| 6 | Empty subcollections audit | 🟢 Any time | Yes — read only |

---

## Prompt 0 — Fix black product page 🔴

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Bug: every product page renders a black background.

Root cause confirmed by audit: the dev theme's active colour scheme is
dark (#0B0B0C body). Load order means style-variables.liquid sets a
dark body before any section CSS can override it.

Already tried and failed:
  - body { background: #FFFFFF !important } in ds-pdp-base.liquid <style>
  - min-height: 100vh on .bbi-pdp

Also already deployed (but unverifiable until page is white):
  - Add to Cart is now the first/dominant button
  - Buy Now is a slim outline button below it
  - Quote card is a compact one-line strip

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
print("Colour-related keys in current settings:")
for k, v in current.items():
    if any(x in k.lower() for x in ["color", "colour", "background", "scheme"]):
        print(f"  {k}: {v}")
EOF

Report the exact key names and values before continuing.

─── Fix A: Patch settings_data.json to light colour scheme ──────────
Based on Step 1 output, apply the correct patch. Common patterns:

Pattern 1 — direct hex:
  data["current"]["colors_background_1"] = "#ffffff"

Pattern 2 — scheme reference:
  data["current"]["color_scheme"] = "scheme_2"  (whichever is light)

Pattern 3 — nested object:
  data["current"]["color_schemes"]["scheme-1"]["background"] = "#ffffff"

Then push the patched file back:

python3 - <<'EOF'
import requests, os, json

shop = "office-central-online.myshopify.com"
token = os.environ["SHOPIFY_TOKEN"]
headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

with open("data/backups/settings_data-backup-pre-lightmode.json") as f:
    data = json.load(f)

# [Apply patch from Step 1 findings]

r = requests.put(
    f"https://{shop}/admin/api/2024-01/themes/186373570873/assets.json",
    headers=headers,
    json={"asset": {"key": "config/settings_data.json",
                    "value": json.dumps(data)}}
)
print(f"HTTP {r.status_code}")
print(r.json())
EOF

─── Fix B: If Fix A fails — inject override in theme.liquid ─────────
Open theme/layout/theme.liquid. Immediately before </head>, add:

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

─── Fix C: If both fail — override the CSS variable at source ───────
Open theme/snippets/style-variables.liquid (or theme-variables.liquid).
Find where --background is defined. Add before its closing tag:

  {%- if template == 'product' -%}
    :root { --background: 255,255,255; }
  {%- endif -%}

Push with --snippets flag.

─── Step 3: Verify ───────────────────────────────────────────────────
Test both URLs — both were black:
  https://office-central-online.myshopify.com/products/vertical-file-2-drawer-letter?preview_theme_id=186373570873
  https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873

Confirm white background, content visible. Also verify CTA stack:
  1. Quantity selector (−/input/+)
  2. Buy Now (slim outline)
  3. Add to Cart (dominant black button)
  4. Compact quote strip (one line)

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

2. Open theme/sections/ds-pdp-base.liquid. Find the Add to Cart button.
   Report: does it have data-bbi-quote-trigger? Does it POST to
   /cart/add.js or redirect to /cart? Is there a <form action="/cart/add">?

3. Open theme/layout/theme.liquid lines 162–177. The cart drawer render:
     if template != 'cart' and bbi_landing == false
   Product pages have bbi_landing = true (line 91) so the cart drawer
   never loads on PDPs. Confirm this is the root cause.

Report all three findings before making any edits.

─── Fix ─────────────────────────────────────────────────────────────
Option A (most likely) — cart drawer missing on product pages:
  In theme/layout/theme.liquid, change line 173 from:
    if template != 'cart' and bbi_landing == false
  to:
    if template != 'cart'

Option B — no cart template exists:
  Create theme/templates/cart.json:
    { "sections": { "main": { "type": "main-cart-items", "settings": {} } },
      "order": ["main"] }
  Confirm theme/sections/main-cart-items.liquid exists.

Option C — ATC button incorrectly has data-bbi-quote-trigger:
  In ds-pdp-base.liquid, ensure data-bbi-quote-trigger is ONLY on the
  Request a Quote button, not Add to Cart.

Apply whichever applies. Multiple may be needed.

─── Push ─────────────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py \
  186373570873 --layout

Confirm HTTP 200. Test: add a product to cart on dev theme — cart
drawer should open or /cart loads without 404.
Commit message: "Fix cart 404: restore cart drawer on product pages"
```

---

## Prompt 2 — Buy Now button + Quantity selector 🟠

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Primary file: theme/sections/ds-pdp-base.liquid

Add a quantity selector and a Buy Now button to the product page.
Read ds-pdp-base.liquid fully before making any edits.

CRITICAL — do not break:
- All data-bbi-quote-trigger attributes
- BbiPdpVariants Web Component and its JS
- bbi-pdp-gallery Web Component and its JS
- The existing Add to Cart button and its form

─── Quantity selector ────────────────────────────────────────────────
Add directly above the Add to Cart button:

  <div class="pdp-quantity">
    <button class="pdp-quantity__btn" data-quantity-minus
            aria-label="Decrease quantity" type="button">−</button>
    <input class="pdp-quantity__input" type="number" name="quantity"
           id="pdp-quantity-input" value="1" min="1" aria-label="Quantity">
    <button class="pdp-quantity__btn" data-quantity-plus
            aria-label="Increase quantity" type="button">+</button>
  </div>

CSS:
  .pdp-quantity { display:flex; align-items:center;
    border:1px solid var(--borderColor); border-radius:var(--cardRadius);
    overflow:hidden; width:fit-content; margin-bottom:12px; }
  .pdp-quantity__btn { background:none; border:none; padding:10px 16px;
    font-size:18px; cursor:pointer; color:var(--textColor);
    line-height:1; transition:background 0.15s; }
  .pdp-quantity__btn:hover { background:var(--alternateBackground); }
  .pdp-quantity__input { width:48px; text-align:center; border:none;
    border-left:1px solid var(--borderColor);
    border-right:1px solid var(--borderColor);
    font-size:15px; padding:10px 0; -moz-appearance:textfield;
    color:var(--textColor); background:none; }
  .pdp-quantity__input::-webkit-outer-spin-button,
  .pdp-quantity__input::-webkit-inner-spin-button { -webkit-appearance:none; }

JS (after existing Web Component scripts):
  document.addEventListener('DOMContentLoaded', function () {
    const minus = document.querySelector('[data-quantity-minus]');
    const plus  = document.querySelector('[data-quantity-plus]');
    const input = document.getElementById('pdp-quantity-input');
    if (!minus || !plus || !input) return;
    minus.addEventListener('click', () => {
      const v = parseInt(input.value, 10); if (v > 1) input.value = v - 1; });
    plus.addEventListener('click', () => {
      input.value = parseInt(input.value, 10) + 1; });
  });

Ensure name="quantity" is inside the product <form>.

─── Buy Now button ───────────────────────────────────────────────────
Add directly ABOVE Add to Cart (below quantity selector):

  <button type="button" class="pdp-btn pdp-btn--primary pdp-btn--buy-now"
          data-buy-now>Buy now</button>

CSS:
  .pdp-btn--buy-now { width:100%; margin-bottom:10px;
    background:var(--textColor); color:var(--background);
    border:2px solid var(--textColor); }
  .pdp-btn--buy-now:hover { opacity:0.85; }

JS (alongside quantity JS):
  document.addEventListener('DOMContentLoaded', function () {
    const buyNow = document.querySelector('[data-buy-now]');
    if (!buyNow) return;
    buyNow.addEventListener('click', async function () {
      buyNow.disabled = true; buyNow.textContent = 'Adding…';
      try {
        const v = document.querySelector('[name="id"],[data-selected-variant]');
        const variantId = v ? (v.value || v.dataset.selectedVariant) : null;
        const qty = parseInt(
          document.getElementById('pdp-quantity-input')?.value || '1', 10);
        if (!variantId) throw new Error('No variant');
        await fetch('/cart/add.js', { method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ id: variantId, quantity: qty }) });
        window.location.href = '/checkout';
      } catch(e) {
        buyNow.disabled = false; buyNow.textContent = 'Buy now';
      }
    });
  });

─── Final CTA stack (top to bottom) ─────────────────────────────────
  1. Quantity selector
  2. Buy Now (black, full width)
  3. Add to Cart (existing, full width)
  4. Quote strip (.pdp-quote-card)

─── Push ─────────────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873

Test: quantity stepper works; Buy Now → /checkout; ATC → cart drawer.
Commit message: "Add quantity selector and Buy Now button to PDP"
```

---

## Prompt 3 — Other products like this (3-tier fallback) 🟡

```
You are working on BBI Shopify dev theme (ID: 186373570873).
File: theme/sections/ds-pdp-base.liquid

Fix: the related products section must always show products. Currently
it can be empty if no products share the same type tag.

Read the .pdp-related section in ds-pdp-base.liquid first and report
how it currently queries related products before making any changes.

─── 3-tier fallback ─────────────────────────────────────────────────
TIER 1 — Same type tag:
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

TIER 3 — Same product_type (if Tiers 1+2 empty):
  {%- if tier1_products.size == 0 and tier2_products.size == 0 -%}
    {%- assign tier3_products = collections['business-furniture'].products
        | where_exp: "p", "p.type == product.type and p.id != product.id"
        | slice: 0, 4 -%}
  {%- endif -%}

  {%- assign related_products = tier1_products | default: tier2_products
      | default: tier3_products -%}

Hide section if all tiers empty:
  {%- if related_products.size > 0 -%}
    <section class="pdp-related">…</section>
  {%- endif -%}

Heading:
  {%- assign related_label = tier1_products.size > 0
    ? ('Other ' | append: type_tag | remove: 'type:' | append: ' products' | capitalize)
    : 'You might also like' -%}

─── Push ─────────────────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs) && \
  BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873

Test on 3 products: Hero with type tags (Tier 1), product with room:
tag only (Tier 2), additional-services (Tier 3 or hidden).
Commit message: "Fix PDP related products: 3-tier fallback always shows products"
```

---

## Prompt 4 — Product descriptions + specs overhaul 🟡

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Store: office-central-online.myshopify.com.

Hero 100 products have enriched descriptions + spec metafields (PE-1,
PE-2, PE-4 in docs/plan/bbi-build-state.md). The remaining ~500 do not.
Task: audit the gap, then enrich in phases. No theme files touched.

─── Step 1: Audit ───────────────────────────────────────────────────
export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import requests, os, csv

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
    mf = requests.get(
        f"https://{shop}/admin/api/2024-01/products/{p['id']}/metafields.json?namespace=specs",
        headers=headers).json().get("metafields", [])
    rows.append({
        "id": p["id"], "title": p["title"], "hero": is_hero,
        "has_description": has_desc, "spec_count": len(mf),
        "spec_keys": ", ".join(m["key"] for m in mf),
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

Report counts before continuing.

─── Step 2: Descriptions ────────────────────────────────────────────
Read docs/strategy/icp.md and docs/strategy/voice-samples.md first.

For each non-Hero product missing body_html, write 2–3 paragraphs:
- P1: what the product is + primary use case
- P2: key functional features (infer from title + type only)
- P3: who it's for (school boards, hospitals, government, pro services)
- Do NOT fabricate dimensions, weights, or model numbers

Batch in 25s. After each batch:
  1. Save drafts → data/reports/description-drafts-batch-N.json
  2. Push via Shopify API (product UPDATE, field: body_html)
  3. Log → data/logs/description-push-YYYY-MM-DD.json
  4. Confirm HTTP 200 before next batch

─── Step 3: Spec metafields ─────────────────────────────────────────
For each non-Hero with 0 spec metafields, add:
- specs.material (infer from title/type)
- specs.warranty ("1 year limited warranty" default)
- specs.assembly ("Assembly required" or "Ships assembled")
Match the API shape in scripts/push-spec-metafields.py exactly.

─── Step 4: SEO meta ────────────────────────────────────────────────
For each non-Hero missing metafields_global_title_tag:
- Title: "[Product Title] | Brant Business Interiors" (max 60 chars)
- Desc: one sentence, max 155 chars — what + who + "Canadian institutional supplier"

Commit: "PE-5/6/7: non-Hero product description + spec + SEO enrichment"
```

---

## Prompt 5 — Hero + sub-hero photo audit 🟢

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Read-only — do not change any files.

Task: find every section with a hero or sub-hero image slot, check
whether it is populated, and flag which need a photo.

─── Find image slots ─────────────────────────────────────────────────
  grep -rn '"type": "image_picker"' theme/sections/*.liquid \
    theme/snippets/*.liquid

─── Check which are populated ────────────────────────────────────────
export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import os, json, glob, re, csv

templates = {}
for path in glob.glob("theme/templates/*.json"):
    with open(path) as f:
        try: templates[os.path.basename(path)] = json.load(f)
        except: pass

slots = []
for path in glob.glob("theme/sections/*.liquid"):
    content = open(path).read()
    if '"image_picker"' not in content: continue
    name = os.path.basename(path).replace(".liquid", "")
    ids = re.findall(r'"type":\s*"image_picker"[^}]*?"id":\s*"([^"]+)"',
                     content, re.DOTALL)
    ids += re.findall(r'"id":\s*"([^"]+)"[^}]*?"type":\s*"image_picker"',
                      content, re.DOTALL)
    for sid in set(ids):
        slots.append({"section": name, "setting_id": sid,
                      "populated": False, "current_value": None})

for slot in slots:
    for tname, tdata in templates.items():
        for skey, sdata in tdata.get("sections", {}).items():
            if sdata.get("type", "") == slot["section"]:
                val = sdata.get("settings", {}).get(slot["setting_id"])
                if val: slot["populated"] = True; slot["current_value"] = val

page_images = [p for p in glob.glob("data/page-images/**/*", recursive=True)
               if p.endswith((".jpg",".jpeg",".png",".webp"))]

with open("data/reports/image-slot-audit.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["section","setting_id","populated","current_value"])
    w.writeheader(); w.writerows(slots)

empty = [s for s in slots if not s["populated"]]
print(f"Total: {len(slots)} | Populated: {len(slots)-len(empty)} | Empty: {len(empty)}")
print(f"Photos available in data/page-images/: {len(page_images)}")
for s in empty: print(f"  EMPTY: {s['section']} → {s['setting_id']}")
EOF

For each empty slot, suggest the best match from data/page-images/
by filename keyword. Flag "NEEDS NEW PHOTO" if no match.

Output table:
  | Section | Setting ID | Status | Current value / Suggestion |

Save to data/reports/image-slot-audit.csv. No push needed.
```

---

## Prompt 6 — Empty subcollections audit 🟢

```
You are working on BBI Shopify dev theme (ID: 186373570873).
Read-only — do not modify any collection data.

Task: find every collection with zero products and check if each can
be auto-populated with a Shopify smart collection rule.

export $(grep -v '^#' .env | xargs)

python3 - <<'EOF'
import requests, json, os

shop = "office-central-online.myshopify.com"
token = os.environ["SHOPIFY_TOKEN"]
headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

all_cols = []
for kind, endpoint in [("custom","custom_collections"),("smart","smart_collections")]:
    url = f"https://{shop}/admin/api/2024-01/{endpoint}.json?limit=250"
    while url:
        r = requests.get(url, headers=headers)
        all_cols += [(kind, c) for c in r.json().get(endpoint, [])]
        link = r.headers.get("Link", "")
        url = next((p.split(";")[0].strip("<>") for p in link.split(",")
                    if 'rel="next"' in p), None)

empty = []
for kind, c in all_cols:
    count = requests.get(
        f"https://{shop}/admin/api/2024-01/collections/{c['id']}/products/count.json",
        headers=headers).json().get("count", 0)
    if count == 0:
        empty.append({"id":c["id"],"type":kind,"title":c["title"],
                      "handle":c["handle"],"rules":c.get("rules",[])})

with open("data/reports/empty-collections-audit.json","w") as f:
    json.dump(empty, f, indent=2)
print(f"Total empty: {len(empty)}")

suggestions = []
for c in [x for x in empty if x["type"]=="custom"]:
    tag_count = requests.get(
        f"https://{shop}/admin/api/2024-01/products/count.json?tag={c['handle']}",
        headers=headers).json().get("count",0)
    type_count = requests.get(
        f"https://{shop}/admin/api/2024-01/products/count.json?product_type={c['title']}",
        headers=headers).json().get("count",0)
    suggestions.append({
        "collection":c["title"],"handle":c["handle"],
        "tag_matches":tag_count,"type_matches":type_count,
        "smart_viable":tag_count>0 or type_count>0,
        "suggested_rule":(
            f"tag = {c['handle']}" if tag_count>0 else
            f"product_type = {c['title']}" if type_count>0 else
            "manual curation needed")
    })

with open("data/reports/empty-collections-smart-suggestions.json","w") as f:
    json.dump(suggestions, f, indent=2)
viable = [s for s in suggestions if s["smart_viable"]]
print(f"Smart fix viable: {len(viable)} | Manual needed: {len(suggestions)-len(viable)}")
print(json.dumps(suggestions, indent=2))
EOF

Output table:
  | Collection | Handle | Type | Smart fix? | Suggested rule |

Also flag: smart collections empty despite having rules (misconfigured);
sub-collection handles (contain a dash) with no parent link;
near-duplicates where one is empty and one has products.

Save to data/reports/empty-collections-audit.json and
data/reports/empty-collections-smart-suggestions.json. No push.
```
