# BBI Image Upload Session Log — 2026-05-25

Interactive manual upload session covering 28 CRITICAL+HIGH image slots.

- **DEV theme target:** `186373570873` (BBI Landing Dev) — LIVE theme `178274435385` (Avada) NOT touched.
- **Order:** Bucket B first (slots 1-4: homepage hero + 3 featured cards), then bucket A (slots 5-28: hero images via theme editor).
- **HALT points:** slot 4 (bucket B done — visual check) and slot 17 (CRITICAL done — natural break).
- **Source root:** `~/Desktop/Leo/`
- **Processed output:** `~/Desktop/bbi-images-v2/[v2-folder]/[locked-name].jpg`

---

## Session start

- Operator: Leo Katz
- Started: 2026-05-25
- Pre-flight: ✅ repo clean (commit `34fd438`), ✅ magick installed (`/opt/homebrew/bin/magick` — ImageMagick 7.1.2-22), ⚠️ `Top product tiles ` retains trailing space (workflow report commands handle it via quoting), ✅ v2 output folders exist.

---

## Slot logs

### SLOT 1 — Homepage hero
- Bucket: B (code edit deferred)
- Source: `~/Desktop/Leo/Homepage-Hero/homepage-product.jpg`
- Processed: `~/Desktop/bbi-images-v2/14-other-pages/homepage-hero.jpg` (2000×1600, 136 KB)
- Spec: 5:4 / 2000×1600
- Status: ✅ UPLOADED via Files
- CDN URL: https://cdn.shopify.com/s/files/1/0859/0413/0361/files/homepage-product.png?v=1779734815
- ⚠️ FLAG (accepted by Leo, advance): CDN URL is the raw PNG source (2560×1440, 16:9, multi-MB), not the optimized processed JPG (2000×1600, 5:4, 136 KB). Visual identical. Tradeoffs at code-edit time: (1) hero CSS container will crop the 16:9 again — verify chair/drawer don't get clipped, (2) hero page-load weight is heavier than necessary. Processed JPG is available at `~/Desktop/bbi-images-v2/14-other-pages/homepage-hero.jpg` if a re-upload is decided later.
- Code edit pending: `theme/assets/bbi-homepage.css:597` (`.bbi-hp-ph--hero` background-image)
- Timestamp: 2026-05-25T14:35-ish

### SLOT 2 — Featured card 1 (homepage)
- Bucket: B (code edit deferred)
- Source: 3rd image from `https://www.brantbusinessinteriors.com/products/l-shape-desk-8-sizes-9-colour-options` (BBI live product, AI office-context render — dark walnut L-shape desk in office scene with window, TV, plants). Downloaded from CDN: `pAgtVib6DgLw-hcM9GZup_..._6d737c21-cd99-4a50-8764-3f71105e6eb4.jpg` (1024×1024).
- Processed: `~/Desktop/bbi-images-v2/14-other-pages/featured-1-l-shape-desk-8sizes.jpg` (1200×900, 121 KB)
- Spec: 4:3 / 1200×900
- Status: ✅ UPLOADED via Files
- CDN URL: https://cdn.shopify.com/s/files/1/0859/0413/0361/files/featured-1-l-shape-desk-8sizes.jpg?v=1779735595
- ⚠️ SKU PIVOT (away from Idea #15): Leo retargeted from "Heartwood L-Shape Height Adjustable Desk Set" (`/products/l-shape-height-adjustable-desk-set`) to "L-shape desk (8 sizes & 9 colour options)" (`/products/l-shape-desk-8-sizes-9-colour-options`). Homepage featured-1 card copy + CTA must update accordingly at code-edit time. First Upwork pick (Top product tiles 6.jpg = boardroom scene) rejected as subject mismatch — processed JPG `featured-1-heartwood-l-shape-desk.jpg` still on disk but unused.
- Code edit pending: `theme/assets/bbi-homepage.css:602` (`.bbi-hp-ph--featured-1` background-image) + `theme/templates/index.json:52` (retarget featured-1 card title + URL from old Heartwood SKU → new 8-sizes-9-colours SKU)
- Timestamp: 2026-05-25T~14:50

### SLOT 3 — Featured card 2 (homepage)
- Bucket: B (code edit deferred)
- Source: 3rd image from `https://www.brantbusinessinteriors.com/products/mvl11886-caman-high-back-tilter-bonded-leather` (BBI live product, AI office-context render — black bonded-leather high-back tilter chair with ribbed backrest, in office scene with window, monitor, plant). Downloaded from CDN: `hCvWFK0d2eoN_wQ_vehDD_..._c428db48-3f7a-4a00-944f-71469de3d5c3.jpg` (1024×1024).
- Processed: `~/Desktop/bbi-images-v2/14-other-pages/featured-2-caman-chair.jpg` (1200×900, 116 KB)
- Spec: 4:3 / 1200×900
- Status: ✅ UPLOADED via Files
- CDN URL: https://cdn.shopify.com/s/files/1/0859/0413/0361/files/featured-2-caman-chair.jpg?v=1779735711
- ⚠️ SKU PIVOT (away from Idea #15): Leo retargeted from "OTG Raven High-Back Heavy-Duty Synchro-Tilter" (`/products/raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b`) to "MVL11886 Caman | High Back Tilter Bonded Leather" (`/products/mvl11886-caman-high-back-tilter-bonded-leather`). Homepage featured-2 card copy + CTA must update accordingly at code-edit time.
- Code edit pending: `theme/assets/bbi-homepage.css:603` (`.bbi-hp-ph--featured-2` background-image) + `theme/templates/index.json:52` (retarget featured-2 card title + URL from old OTG Raven SKU → new Caman bonded-leather SKU)
- Timestamp: 2026-05-25T~14:58

### SLOT 4 — Featured card 3 (homepage)
- Bucket: B (code edit deferred)
- Source: 6th image from `https://www.brantbusinessinteriors.com/products/global-accord-back-knee-tilter-chair-1` (BBI live product, AI office-context render — high-back black executive chair with ribbed back + chrome arm frames, open-plan office with herringbone wood floor + monitors + windows). Downloaded from CDN: `3XZDJ_vP5JEQZgFNpOVn7_2cfc7e6d5fc840689f9804de109d25f7.jpg` (1024×1024).
- Processed: `~/Desktop/bbi-images-v2/14-other-pages/featured-3-global-accord-knee-tilter.jpg` (1200×900, 147 KB)
- Spec: 4:3 / 1200×900
- Status: ✅ UPLOADED via Files
- CDN URL: https://cdn.shopify.com/s/files/1/0859/0413/0361/files/featured-3-global-accord-knee-tilter.jpg?v=1779735828
- ⚠️ SKU PIVOT (away from Idea #15): Leo retargeted from "GFG Accord Mesh-Back Tilter" (`/products/global-accord-mesh-back-tilter`) to "Global Accord back knee tilter chair" (`/products/global-accord-back-knee-tilter-chair-1`). Same brand family (Global Accord), different model. Homepage featured-3 card copy + CTA must update accordingly.
- Code edit pending: `theme/assets/bbi-homepage.css:604` (`.bbi-hp-ph--featured-3` background-image) + `theme/templates/index.json:52` (retarget featured-3 card title + URL from old GFG Accord Mesh-Back SKU → new Accord Back Knee Tilter SKU)
- Timestamp: 2026-05-25T~15:05

---

## HALT @ slot 4 — Bucket B COMPLETE

✓ 4 CDN URLs captured. Ready for theme code edit (separate session, ~30 min).

### Session note — Idea #15 SKU pivots (Leo, mid-session)

Three SKU pivots from the original Idea #15 list. To be reflected in `BBI-Session-Kickoff/bbi-build-state.md` at EOD Cowork session today.

- **SLOT 2:** Heartwood L-Shape (`/products/l-shape-height-adjustable-desk-set`) → **L-shape desk 8 sizes 9 colour options** (`/products/l-shape-desk-8-sizes-9-colour-options`)
- **SLOT 3:** OTG Raven (`/products/raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b`) → **Caman high-back tilter, mvl11886** (`/products/mvl11886-caman-high-back-tilter-bonded-leather`)
- **SLOT 4:** GFG Accord Mesh-Back (`/products/global-accord-mesh-back-tilter`) → **Global Accord back knee tilter** (`/products/global-accord-back-knee-tilter-chair-1`)

All three new SKUs are live BBI products with AI-rendered office-context photos in their galleries — bucket B code-edit session needs to retarget both the background-image URLs and the card title + CTA strings in `theme/templates/index.json:52`.

### SLOT 5 — Business Furniture (parent collection) hero
- Bucket: A (theme editor)
- Spec: 5:4 / 1600×1280
- Status: ⏭️ SKIPPED — Leo: "I like what is in there currently" (existing DEV hero on `/collections/business-furniture` deemed acceptable). No source pick, no magick run, no theme editor upload.
- Theme editor URL (for later if revisited): https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/business-furniture&section=ds-cc-base
- Timestamp: 2026-05-25T~15:10

### SLOT 6 — Seating category hero
- Bucket: A (theme editor)
- Spec: 5:4 / 1600×1280
- Status: ⏭️ SKIPPED — Leo: "skip" (existing DEV hero on `/collections/seating` deemed acceptable)
- Theme editor URL (for later): https://admin.shopify.com/store/office-central-online/themes/186373570873/editor?previewPath=/collections/seating&section=ds-cc-base
- Timestamp: 2026-05-25T~15:11


