# BBI Image Bucket A/B Workflow — 2026-05-25

Repo state at generation: `main` @ `4047a19` (v2 + Upwork gap analysis). Read-only analysis. No theme writes, no Shopify Admin changes, no Shopify Files uploads, no image processing.

Drives the interactive manual upload session that will follow. Categorizes each of the 28 CRITICAL+HIGH image slots as **bucket A** (Shopify theme editor friendly — `image_picker` setting in section schema) or **bucket B** (theme code edit required — CSS-class placeholder or custom_liquid `<div>`). Generates per-slot Shopify Admin URLs, pre-upload ImageMagick commands, and (for bucket B) the exact theme file + line where Claude Code will need to write later.

---

## Executive Summary

| Metric | Value |
|---|---:|
| **Total slots** | **28** (CRITICAL+HIGH) |
| **Bucket A — theme editor (`image_picker`)** | **24** |
| **Bucket B — theme code edit required** | **4** (homepage hero + 3 featured cards) |
| ImageMagick install status | ✅ **installed** (`magick` at `/opt/homebrew/bin/magick` · ImageMagick 7.1.2-22 Q16-HDRI aarch64) |
| DEV theme (target for writes) | `186373570873` ("BBI Landing Dev") |
| LIVE theme (currently published — DO NOT TOUCH) | `178274435385` ("Avada") |
| Store admin base | `https://admin.shopify.com/store/office-central-online/` |

**Mechanism split:**

| Surface | Slots | Mechanism | Bucket |
|---|---:|---|---|
| Homepage (`templates/index.json` custom_liquid) | 1-4 | `<div class="bbi-hp-ph bbi-hp-ph--*">` + CSS `background` in `assets/bbi-homepage.css` | **B** |
| Category heroes (`ds-cc-base.liquid`) | 5-13 | `image_picker` `hero_image` (line 1046-1047) | **A** |
| Industry / OECM / service / brand heroes (`ds-lp-*.liquid`) | 14-28 | `image_picker` `hero_image` (per-section schema) | **A** |

---

## Pre-Upload Image Processing

Before uploading any image to Shopify, Leo runs ImageMagick to crop/resize to spec. ImageMagick is installed. Skip the install step.

### Setup (already done — verify)

```bash
which magick
# → /opt/homebrew/bin/magick

magick --version | head -1
# → Version: ImageMagick 7.1.2-22 Q16-HDRI aarch64
```

If `which magick` returns nothing on a different machine: `brew install imagemagick`.

### Command templates by spec

The 28 CRITICAL+HIGH slots use 3 spec variants:

**1. Large hero — 5:4 at 2000×1600 (retina top-of-funnel — SLOT 1 homepage hero, SLOT 19 industries hub):**

```bash
magick INPUT.jpg -resize 2000x1600^ -gravity center \
  -extent 2000x1600 -colorspace sRGB -quality 85 \
  OUTPUT.jpg
```

**2. Standard hero — 5:4 at 1600×1280 (all category heroes + industry + brand + service + OECM + Quote — 23 slots):**

```bash
magick INPUT.jpg -resize 1600x1280^ -gravity center \
  -extent 1600x1280 -colorspace sRGB -quality 85 \
  OUTPUT.jpg
```

**3. Featured card — 4:3 at 1200×900 (3 homepage featured cards — SLOTS 2, 3, 4):**

```bash
magick INPUT.jpg -resize 1200x900^ -gravity center \
  -extent 1200x900 -colorspace sRGB -quality 85 \
  OUTPUT.jpg
```

The `^` after the dimensions tells ImageMagick to **fill** the target (cropping the long axis) instead of letterboxing. `-gravity center` centers the crop. `-extent` enforces exact final pixels. `-colorspace sRGB` guarantees Shopify CDN compatibility. `-quality 85` is the Shopify-recommended JPEG quality for hero imagery.

**Upwork source dimensions (from `data/research/v2-state-and-gap-analysis-2026-05-25.md`):**

| Upwork folder | Files | Source dims | Source ratio | Used for slots |
|---|---:|---|---|---|
| `~/Desktop/Leo/Homepage-Hero/` | 17 | 2560×1440 | 16:9 | SLOT 1 (crop top+bottom 22%) |
| `~/Desktop/Leo/Top product tiles ` (trailing space ⚠️) | 9 | 1205×900 | 4:3 | SLOT 2-4 (direct match — resize only) |
| `~/Desktop/Leo/Brandbanners/` | 5 | 1600×1280 | **5:4 EXACT** | SLOT 21-24 (no crop, no resize) |
| `~/Desktop/Leo/Categorybanners/` | 9 | 2400×800 | 3:1 | SLOT 5-13 (crop sides ~22%) |
| `~/Desktop/Leo/Category service tiles/` | 40 | 1200×1200 | 1:1 | SLOT 14-19, 25-28 (crop top+bottom 20%) |

---

## Per-Slot Workflow

Sorted CRITICAL (slots 1-13) → HIGH (slots 14-28). Each entry has:
- Priority, page, bucket, spec
- ImageMagick command (uses the **locked v2 output filename** so Phase B/C downstream stays consistent)
- Bucket A: Shopify Admin URL + steps
- Bucket B: Shopify Files URL + steps + exact code edit (file + line)

> **DEV preview pattern** for visual confirmation after a save (works for any path):
> `https://office-central-online.myshopify.com/<path>?preview_theme_id=186373570873`

---

### SLOT 1 — Homepage hero
- **Priority:** CRITICAL · **Bucket:** B (code edit — CSS-class placeholder)
- **Page:** `/` (Homepage)
- **Spec:** 5:4 / 2000×1600 (retina, oversized)
- **DEV preview:** `https://office-central-online.myshopify.com/?preview_theme_id=186373570873`

**Pre-upload — process the image:**

```bash
magick ~/Desktop/Leo/Homepage-Hero/homepage-hero-N.jpg \
  -resize 2000x1600^ -gravity center -extent 2000x1600 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/homepage-hero.jpg
```

**Upload location (bucket B — Shopify Files):**
🔗 [https://admin.shopify.com/store/office-central-online/content/files](https://admin.shopify.com/store/office-central-online/content/files)

Steps:
1. Click Files link above.
2. Click **Upload files** → drop `~/Desktop/bbi-images-v2/14-other-pages/homepage-hero.jpg`.
3. After upload, click the file in the list → click the chain-link icon to copy the CDN URL (looks like `https://cdn.shopify.com/s/files/1/0xxx/yyyy/files/homepage-hero.jpg?v=...`).
4. Paste URL back to Claude Code so it's logged for the batch theme-code-edit session.

**Code edit (Claude Code will do later — for reference):**
- **File:** [theme/assets/bbi-homepage.css:597](theme/assets/bbi-homepage.css)
- **Current:** `.bbi-hp-ph--hero { background: linear-gradient(140deg, #0B0B0C 0%, #363A42 55%, #A81C20 100%); }`
- **Change to:** add `background-image: url('<CDN_URL>'); background-size: cover; background-position: center; background-color: #0B0B0C;` rule. Existing gradient stays as fallback for CSP/CDN-fail cases.
- Alt approach: edit [theme/templates/index.json:12](theme/templates/index.json) custom_liquid to swap `<div class="bbi-hp-ph bbi-hp-ph--hero">` for `<img src="<CDN_URL>" alt="...">` — *less preferred*, breaks the CSS placeholder fallback pattern.

---

### SLOT 2 — Featured product card 1 (Heartwood L-Shape Height Adjustable Desk Set)
- **Priority:** CRITICAL · **Bucket:** B (code edit — CSS-class placeholder)
- **Page:** `/` (Homepage)
- **Spec:** 4:3 / 1200×900
- **DEV preview:** `https://office-central-online.myshopify.com/?preview_theme_id=186373570873`

**Pre-upload — process the image:**

```bash
magick ~/Desktop/Leo/Top\ product\ tiles\ /Top\ product\ tiles\ N.jpg \
  -resize 1200x900^ -gravity center -extent 1200x900 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/featured-1-heartwood-l-shape-desk.jpg
```

> Note: `Top product tiles ` has a trailing space — must be quoted/escaped.

**Upload location (bucket B — Shopify Files):**
🔗 [https://admin.shopify.com/store/office-central-online/content/files](https://admin.shopify.com/store/office-central-online/content/files)

Steps: same as SLOT 1 (upload → copy CDN URL → paste back).

**Code edit (Claude Code will do later):**
- **File:** [theme/assets/bbi-homepage.css:602](theme/assets/bbi-homepage.css)
- **Current:** `.bbi-hp-ph--featured-1 { background: #E9EBEF; color: #363A42; }`
- **Change to:** add `background-image: url('<CDN_URL>'); background-size: cover; background-position: center;`
- **Plus:** [theme/templates/index.json:52](theme/templates/index.json) — retarget the existing copy/CTA from "ergoCentric tCentric Hybrid Task Chair" → "Heartwood L-Shape Height Adjustable Desk Set" and link `/products/l-shape-height-adjustable-desk-set` (per Idea #15, closed 2026-05-25).

---

### SLOT 3 — Featured product card 2 (OTG Raven High-Back Heavy-Duty Synchro-Tilter)
- **Priority:** CRITICAL · **Bucket:** B (code edit — CSS-class placeholder)
- **Page:** `/` (Homepage)
- **Spec:** 4:3 / 1200×900
- **DEV preview:** `https://office-central-online.myshopify.com/?preview_theme_id=186373570873`

**Pre-upload — process the image:**

```bash
magick ~/Desktop/Leo/Top\ product\ tiles\ /Top\ product\ tiles\ N.jpg \
  -resize 1200x900^ -gravity center -extent 1200x900 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/featured-2-otg-raven-chair.jpg
```

**Upload location:** Files (same as SLOT 1).

**Code edit (Claude Code will do later):**
- **File:** [theme/assets/bbi-homepage.css:603](theme/assets/bbi-homepage.css)
- **Current:** `.bbi-hp-ph--featured-2 { background: #F3F4F6; color: #363A42; }`
- **Change to:** add `background-image: url('<CDN_URL>'); background-size: cover; background-position: center;`
- **Plus:** [theme/templates/index.json:52](theme/templates/index.json) — retarget "Keilhauer Wish Side Chair" → "OTG Raven High-Back Heavy-Duty Synchro-Tilter", link `/products/raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b`.

---

### SLOT 4 — Featured product card 3 (GFG Accord Mesh-Back Tilter)
- **Priority:** CRITICAL · **Bucket:** B (code edit — CSS-class placeholder)
- **Page:** `/` (Homepage)
- **Spec:** 4:3 / 1200×900
- **DEV preview:** `https://office-central-online.myshopify.com/?preview_theme_id=186373570873`

**Pre-upload — process the image:**

```bash
magick ~/Desktop/Leo/Top\ product\ tiles\ /Top\ product\ tiles\ N.jpg \
  -resize 1200x900^ -gravity center -extent 1200x900 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/featured-3-gfg-accord-tilter.jpg
```

**Upload location:** Files (same as SLOT 1).

**Code edit (Claude Code will do later):**
- **File:** [theme/assets/bbi-homepage.css:604](theme/assets/bbi-homepage.css)
- **Current:** `.bbi-hp-ph--featured-3 { background: #DEE1E6; color: #363A42; }`
- **Change to:** add `background-image: url('<CDN_URL>'); background-size: cover; background-position: center;`
- **Plus:** [theme/templates/index.json:52](theme/templates/index.json) — retarget "Global Furniture Group Furtif Executive Desk" → "GFG Accord Mesh-Back Tilter", link `/products/global-accord-mesh-back-tilter`.

---

### SLOT 5 — Business Furniture (parent collection) hero
- **Priority:** CRITICAL · **Bucket:** A (theme editor)
- **Page:** `/collections/business-furniture`
- **Spec:** 5:4 / 1600×1280
- **DEV preview:** `https://office-central-online.myshopify.com/collections/business-furniture?preview_theme_id=186373570873`

**Pre-upload — process the image:**

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/business-furniture-hero.jpg
```

**Upload location (bucket A — theme editor):**
🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/business-furniture&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/business-furniture&section=ds-cc-base)

Steps:
1. Click link above. Theme editor opens with the Business Furniture collection page in the preview pane.
2. In the left sidebar, click **BBI Category Page** → scroll down to the **Hero image** setting.
3. Click the image picker → **Select image** → **Upload** tab → pick `~/Desktop/bbi-images-v2/01-category-heroes/business-furniture-hero.jpg`.
4. Click **Select**.
5. Click **Save** (top-right).
6. (Optional) Verify on DEV preview link.

---

### SLOT 6 — Seating category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/seating`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/seating-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/seating&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/seating&section=ds-cc-base)

Steps: same as SLOT 5 (sidebar → BBI Category Page → Hero image → upload).

---

### SLOT 7 — Desks category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/desks`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/desks-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/desks&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/desks&section=ds-cc-base)

---

### SLOT 8 — Storage category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/storage`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/storage-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/storage&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/storage&section=ds-cc-base)

---

### SLOT 9 — Tables category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/tables`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/tables-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/tables&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/tables&section=ds-cc-base)

---

### SLOT 10 — Boardroom category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/boardroom`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/boardroom-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/boardroom&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/boardroom&section=ds-cc-base)

---

### SLOT 11 — Ergonomic Products category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/ergonomic-products`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/ergonomic-product-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/ergonomic-products&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/ergonomic-products&section=ds-cc-base)

---

### SLOT 12 — Panels & Room Dividers category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/panels-room-dividers`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/panels-room-dividers-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/panels-room-dividers&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/panels-room-dividers&section=ds-cc-base)

---

### SLOT 13 — Accessories category hero
- **Priority:** CRITICAL · **Bucket:** A
- **Page:** `/collections/accessories`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/01-category-heroes/accessories-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/accessories&section=ds-cc-base](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/accessories&section=ds-cc-base)

---

### SLOT 14 — Healthcare industry hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/healthcare`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/11-industry-pages/healthcare-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/healthcare&section=lp-healthcare](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/healthcare&section=lp-healthcare)

Steps:
1. Click link → theme editor loads `/pages/healthcare`.
2. Left sidebar → click the **Healthcare** section (schema name on `ds-lp-healthcare`) → find **Hero image**.
3. Image picker → Upload → pick the processed file.
4. Save.

---

### SLOT 15 — Education industry hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/education`
- **Spec:** 5:4 / 1600×1280
- **Note:** OECM anchor sector — primary cornerstone-post-1 audience.

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/11-industry-pages/education-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/education&section=lp-education](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/education&section=lp-education)

---

### SLOT 16 — Government industry hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/government`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/11-industry-pages/government-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/government&section=lp-government](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/government&section=lp-government)

---

### SLOT 17 — Professional Services industry hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/professional-services`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/12-services-pages/professional-services-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/professional-services&section=lp-professional-services](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/professional-services&section=lp-professional-services)

---

### SLOT 18 — Non-Profit industry hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/non-profit`
- **Spec:** 5:4 / 1600×1280
- **Note:** v2 placeholder warns: **avoid for-profit aesthetic** (Mattamy problem flagged in spec).

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/11-industry-pages/non-profit-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/non-profit&section=lp-non-profit](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/non-profit&section=lp-non-profit)

---

### SLOT 19 — Industries hub hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/industries`
- **Spec:** 5:4 / **2000×1600** (retina top-of-funnel)

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 2000x1600^ -gravity center -extent 2000x1600 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/11-industry-pages/industries-hub-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/industries&section=lp-industries](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/industries&section=lp-industries)

---

### SLOT 20 — OECM page hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/oecm`
- **Spec:** 5:4 / 1600×1280
- **Note:** OECM is the single highest-converting page for institutional buyers. Idea #13 critical-path target. Currently re-uses the same file as Industries Hub (`industries-hub-space_a7491d71-...jpg`) — needs a distinct image.

```bash
# Best subject match likely a Categorybanners file (gov building or similar);
# fallback to Category service tiles if no banner fits.
magick ~/Desktop/Leo/Categorybanners/Category-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/oecm-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/oecm&section=main](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/oecm&section=main)

> Section key for `page.oecm.json` is `main` (not `ds-lp-oecm`).

---

### SLOT 21 — Brands hub hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/brands`
- **Spec:** 5:4 / 1600×1280
- **Bonus:** `Brandbanners/` Upwork source is **1600×1280 EXACT match** — no crop loss.

```bash
# 5:4 exact match — but run through magick anyway to normalize quality/colorspace
magick ~/Desktop/Leo/Brandbanners/Brand-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/15-brand-pages/brands-hub-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands&section=ds-lp-brands](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands&section=ds-lp-brands)

---

### SLOT 22 — Heartwood brand hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/brands-heartwood`
- **Spec:** 5:4 / 1600×1280
- **Note:** Currently **blank** in template. One of 3 hero brands per Idea #15.

```bash
magick ~/Desktop/Leo/Brandbanners/Brand-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/15-brand-pages/heartwood-brand-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-heartwood&section=ds-lp-brands-heartwood](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-heartwood&section=ds-lp-brands-heartwood)

---

### SLOT 23 — OTG brand hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/brands-otg`
- **Spec:** 5:4 / 1600×1280
- **Note:** Currently **blank** in template.

```bash
magick ~/Desktop/Leo/Brandbanners/Brand-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/15-brand-pages/otg-brand-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-otg&section=ds-lp-brands-otg](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-otg&section=ds-lp-brands-otg)

---

### SLOT 24 — Global / Teknion (GFG) brand hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/brands-global-teknion`
- **Spec:** 5:4 / 1600×1280

```bash
magick ~/Desktop/Leo/Brandbanners/Brand-banners-N.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/15-brand-pages/gfg-brand-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-global-teknion&section=ds-lp-brands-global-teknion](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/brands-global-teknion&section=ds-lp-brands-global-teknion)

---

### SLOT 25 — Delivery service hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/delivery`
- **Spec:** 5:4 / 1600×1280
- **Subject:** Delivery truck, warehouse loading, installation crew. Service excellence.

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/12-services-pages/delivery-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/delivery&section=ds-lp-delivery](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/delivery&section=ds-lp-delivery)

---

### SLOT 26 — Relocation service hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/relocation`
- **Spec:** 5:4 / 1600×1280
- **Subject:** Office moving in progress — boxes, furniture, organized crew.

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/12-services-pages/relocation-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/relocation&section=ds-lp-relocation](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/relocation&section=ds-lp-relocation)

---

### SLOT 27 — Design Services hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/design-services`
- **Spec:** 5:4 / 1600×1280
- **Subject:** Designer at work — space planning, blueprint, 3D rendering.

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/12-services-pages/design-services-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/design-services&section=main](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/design-services&section=main)

> Section key for `page.design-services.json` is `main` (not `ds-lp-design-services`).

---

### SLOT 28 — Quote page hero
- **Priority:** HIGH · **Bucket:** A
- **Page:** `/pages/quote`
- **Spec:** 5:4 / 1600×1280
- **Note:** Primary conversion page across the entire site — first impression matters.
- **Subject:** Sales rep with client, planner with blueprint, BBI showroom walk-through.

```bash
magick ~/Desktop/Leo/Category\ service\ tiles/Category_service\ tilesN.jpg \
  -resize 1600x1280^ -gravity center -extent 1600x1280 \
  -colorspace sRGB -quality 85 \
  ~/Desktop/bbi-images-v2/14-other-pages/quote-hero.jpg
```

🔗 [https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/quote&section=main](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/pages/quote&section=main)

> Section key for `page.quote.json` is `main` (not `ds-lp-quote`).

---

## Bucket Summary

### Bucket A — theme editor (`image_picker`) · 24 slots

All use the Shopify Theme Editor URL pattern with `?previewPath=<path>&section=<section-key>`. Upload via the section's **Hero image** image picker → Save.

| # | Slot | Section key in template | Folder |
|---|---|---|---|
| 5 | Business Furniture hero | `ds-cc-base` | `Categorybanners/` |
| 6 | Seating hero | `ds-cc-base` | `Categorybanners/` |
| 7 | Desks hero | `ds-cc-base` | `Categorybanners/` |
| 8 | Storage hero | `ds-cc-base` | `Categorybanners/` |
| 9 | Tables hero | `ds-cc-base` | `Categorybanners/` |
| 10 | Boardroom hero | `ds-cc-base` | `Categorybanners/` |
| 11 | Ergonomic Products hero | `ds-cc-base` | `Categorybanners/` |
| 12 | Panels hero | `ds-cc-base` | `Categorybanners/` |
| 13 | Accessories hero | `ds-cc-base` | `Categorybanners/` |
| 14 | Healthcare hero | `lp-healthcare` | `Category service tiles/` |
| 15 | Education hero | `lp-education` | `Category service tiles/` |
| 16 | Government hero | `lp-government` | `Category service tiles/` |
| 17 | Pro Services hero | `lp-professional-services` | `Category service tiles/` |
| 18 | Non-Profit hero | `lp-non-profit` | `Category service tiles/` |
| 19 | Industries hub hero | `lp-industries` | `Category service tiles/` |
| 20 | OECM hero | `main` | `Categorybanners/` |
| 21 | Brands hub hero | `ds-lp-brands` | `Brandbanners/` |
| 22 | Heartwood brand hero | `ds-lp-brands-heartwood` | `Brandbanners/` |
| 23 | OTG brand hero | `ds-lp-brands-otg` | `Brandbanners/` |
| 24 | GFG brand hero | `ds-lp-brands-global-teknion` | `Brandbanners/` |
| 25 | Delivery hero | `ds-lp-delivery` | `Category service tiles/` |
| 26 | Relocation hero | `ds-lp-relocation` | `Category service tiles/` |
| 27 | Design Services hero | `main` | `Category service tiles/` |
| 28 | Quote hero | `main` | `Category service tiles/` |

### Bucket B — code edit required · 4 slots

All four homepage slots. Workflow: Files upload → CDN URL → Claude Code edits `theme/assets/bbi-homepage.css` later. SLOTS 2/3/4 also need `templates/index.json` copy/CTA retarget (Idea #15 SKU picks).

| # | Slot | Code file + line | Folder |
|---|---|---|---|
| 1 | Homepage hero | [theme/assets/bbi-homepage.css:597](theme/assets/bbi-homepage.css) (`.bbi-hp-ph--hero`) | `Homepage-Hero/` |
| 2 | Featured 1 (Heartwood) | [theme/assets/bbi-homepage.css:602](theme/assets/bbi-homepage.css) + [theme/templates/index.json:52](theme/templates/index.json) | `Top product tiles ` |
| 3 | Featured 2 (OTG) | [theme/assets/bbi-homepage.css:603](theme/assets/bbi-homepage.css) + [theme/templates/index.json:52](theme/templates/index.json) | `Top product tiles ` |
| 4 | Featured 3 (GFG) | [theme/assets/bbi-homepage.css:604](theme/assets/bbi-homepage.css) + [theme/templates/index.json:52](theme/templates/index.json) | `Top product tiles ` |

---

## Notes

- **Recommended order:** **bucket A first** (24 slots — visible immediately on DEV preview after each save; instant feedback loop), then **bucket B** (4 slots — uploads to Files give instant access but the theme code edit happens later in a batched session with Claude Code).
- Within bucket A: start with `Brandbanners/` (SLOTS 21-24) — source files are 1600×1280 5:4 **exact match** so no crop loss. Then `Categorybanners/` (SLOTS 5-13 + 20) — 9 hero slots from 9 source files. Then `Category service tiles/` (SLOTS 14-19, 25-28) — biggest pool, subject-driven picks.
- **DEV preview URL pattern** (after a save, to confirm visually): `https://office-central-online.myshopify.com/<path>?preview_theme_id=186373570873`
- **All uploads target DEV theme `186373570873`** ("BBI Landing Dev"). LIVE theme `178274435385` ("Avada") **must not be touched** — it'll be flipped to BBI at LAUNCH-2 Monday afternoon.
- **Filename watch-outs:** `~/Desktop/Leo/Top product tiles ` and `~/Desktop/Leo/Sub Category ` have trailing spaces (verified in v2-state research). Must be quoted/escaped in shell.
- **Bucket B alt path:** SLOTS 1-4 could alternatively be done by editing `templates/index.json` to swap the `<div class="bbi-hp-ph">` for `<img src="<CDN_URL>">`. The CSS-`background-image` approach is preferred because it preserves the gradient/solid color as a fallback when CDN/CSP issues happen.
- **OECM, design-services, and quote** all use section key `main` (not `ds-lp-*`). The theme-editor URL `&section=` param honours this.
- **Pre-existing untracked items** in the repo (e.g., `snippets/`, `.bak` files, smart-collections CSV, strategy pkl/json) were not touched in this session.

---

## Verification — 3 spot-check URLs

The Shopify theme-editor URL format `?previewPath=<path>&section=<key>` was verified by reading the actual section keys from each template JSON. Three spot-checks:

1. **SLOT 6 (Seating hero):** template `theme/templates/collection.seating.json` → sections key `ds-cc-base` ✓ → URL points to `/collections/seating&section=ds-cc-base` ✓
2. **SLOT 20 (OECM hero):** template `theme/templates/page.oecm.json` → sections key `main` (not `ds-lp-oecm`!) ✓ → URL points to `/pages/oecm&section=main` ✓
3. **SLOT 28 (Quote hero):** template `theme/templates/page.quote.json` → sections key `main` (not `ds-lp-quote`!) ✓ → URL points to `/pages/quote&section=main` ✓

All 28 section keys + paths derived from theme template files, none fabricated.

---

## Generated 2026-05-25 — Day 11 #14d

Read-only analysis. No theme writes, no Shopify Admin changes, no Shopify Files uploads, no image processing. Output drives the interactive manual upload session that follows.
