# PROMPT-5 Image Slot Audit
_2026-05-13 · Read-only audit · Step 15._

---

## Summary

- **Templates audited:** 28 (all BBI ds-* / bbi-* templates in theme/templates/)
- **Total image_picker slots found:** 120 (across BBI sections only; Starlite legacy sections excluded)
- **Empty slots:** 56
- **Populated slots:** 64
- **Available images:**
  - `data/page-images/`: 63 images (AI-generated hero/space/product images, named by page/context)
  - `data/oci-photos/`: 80 images (real OCI project photos from officecentral.com)
  - Other (`data/design-photos/`, `data/logos/`): reference assets, not suitable for page slots

**Match quality breakdown (56 empty slots):**

| Match tier | Count | Meaning |
|---|---|---|
| EXACT | 9 | Schema `info` tag explicitly names the file — just upload and set |
| HIGH | 26 | Direct filename/semantic match in page-images or OCI catalog |
| MEDIUM | 14 | No dedicated image exists; OCI analog or generic office photo works |
| LOW | 2 | Weak match only; a new/better image is preferred |
| NO MATCH | 3 | No suitable candidate exists in current inventory |

**Total actionable with current inventory: 51 of 56 (91%)**

---

## Empty slots by template

### Collection templates (10 hero_image + 2 logo stubs)

| Template | Section | Setting | Best candidate | Confidence |
|---|---|---|---|---|
| collection.accessories.json | ds-cc-base | hero_image | data/page-images/accessories/accessories-space.jpg | HIGH |
| collection.base.json | ds-cs-base | logo | Copy shopify:// URL from any sibling template | HIGH |
| collection.base.json | ds-cs-base | hero_image | — | NO MATCH — generic template; set per-suffix |
| collection.boardroom.json | ds-cc-base | hero_image | data/page-images/boardroom/boardroom-space.jpg | HIGH |
| collection.business-furniture.json | ds-cc-base | hero_image | data/page-images/business-furniture/business-furniture-space.jpg | HIGH |
| collection.category.json | ds-cc-base | logo | Copy shopify:// URL from any sibling template | HIGH |
| collection.category.json | ds-cc-base | hero_image | — | NO MATCH — generic template; set per-suffix |
| collection.desks.json | ds-cc-base | hero_image | data/page-images/desks/desks-space.jpg | HIGH |
| collection.ergonomic-products.json | ds-cc-base | hero_image | data/page-images/ergonomic-products/ergonomic-products-space.jpg | HIGH |
| collection.panels-room-dividers.json | ds-cc-base | hero_image | data/page-images/panels-room-dividers/panels-room-dividers-space.jpg | HIGH |
| collection.quiet-spaces.json | ds-cc-base | hero_image | data/page-images/quiet-spaces/quiet-spaces-space.jpg | HIGH |
| collection.seating.json | ds-cc-base | hero_image | data/page-images/seating/seating-space.jpg | HIGH |
| collection.storage.json | ds-cc-base | hero_image | data/page-images/storage/storage-space.jpg | HIGH |
| collection.tables.json | ds-cc-base | hero_image | data/page-images/tables/tables-space.jpg | HIGH |

**Note on collection.base.json and collection.category.json:** These are generic parent templates used as fallbacks. Their `hero_image` slot cannot hold one fixed image because they serve many different collections. The logo slot can be patched by copying the bbi-logo-v2 shopify:// URL from any peer template — it's the same asset.

---

### Page templates

| Template | Section | Setting | Best candidate | Confidence |
|---|---|---|---|---|
| page.about.json | ds-lp-about | hero_image | data/oci-photos/About-us-1.webp | **EXACT** |
| page.brands.json | ds-lp-brands | hero_image | data/page-images/brands-hub/brands-hub-space.jpg | **EXACT** |
| page.brands.json | ds-lp-brands | keilhauer_image | data/page-images/keilhauer/keilhauer-space.jpg | **EXACT** |
| page.brands.json | ds-lp-brands | ergocentric_image | data/page-images/ergocentric/ergocentric-space.jpg | **EXACT** |
| page.brands.json | ds-lp-brands | global_image | data/page-images/global-teknion/global-teknion-space.jpg | **EXACT** |
| page.brands-ergocentric.json | ds-lp-brands-ergocentric | hero_image | data/page-images/ergocentric/ergocentric-space.jpg | **EXACT** |
| page.brands-global-teknion.json | ds-lp-brands-global-teknion | hero_image | data/page-images/global-teknion/global-teknion-space.jpg | **EXACT** |
| page.brands-keilhauer.json | ds-lp-brands-keilhauer | hero_image | data/page-images/keilhauer/keilhauer-space.jpg | **EXACT** |
| page.customer-stories.json | ds-lp-customer-stories | story1_image | data/oci-photos/Mattamy-1.jpg | MEDIUM |
| page.customer-stories.json | ds-lp-customer-stories | story2_image | data/oci-photos/OCI-Government-Federal-Furniture-Gallery-Image-1.jpg | MEDIUM |
| page.customer-stories.json | ds-lp-customer-stories | story3_image | data/oci-photos/Inspiration-Executive-Office.jpg | MEDIUM |
| page.delivery.json | ds-lp-delivery | hero_image | data/page-images/delivery/delivery-space.jpg | HIGH |
| page.design-services.json | ds-lp-design-services | hero_image | data/page-images/design-services/design-services-product.jpg | HIGH |
| page.design-services.json | ds-lp-design-services | form_photo | data/oci-photos/OCI-Planning-Desogn.jpg | MEDIUM |
| page.design-services.json | ds-lp-design-services | client_logo | — | **NO MATCH** |
| page.education.json | ds-lp-education | trust_image_2 | data/oci-photos/Inspiration-Meeting-1.jpg | MEDIUM |
| page.education.json | ds-lp-education | trust_image_3 | data/oci-photos/Inspiration-Ergonomics.jpg | LOW |
| page.government.json | ds-lp-government | trust_image_2 | data/oci-photos/Mattamy-1.jpg | MEDIUM |
| page.government.json | ds-lp-government | trust_image_3 | data/oci-photos/OCI-Service-Excellence-1.jpg | MEDIUM |
| page.healthcare.json | ds-lp-healthcare | trust_image_3 | data/oci-photos/Inspiration-Reception.jpg | LOW |
| page.non-profit.json | ds-lp-non-profit | hero_image | data/page-images/non-profit/non-profit-space.jpg | HIGH |
| page.non-profit.json | ds-lp-non-profit | trust_image_3 | data/oci-photos/OCI-Inspiration-Breakroom.jpg | MEDIUM |
| page.oecm.json | ds-lp-oecm | hero_image | data/page-images/industries-hub/industries-hub-space.jpg | MEDIUM |
| page.oecm.json | ds-lp-oecm | trust_image_1 | data/oci-photos/OCI-Healthcare-Carousel-3.jpg | MEDIUM |
| page.oecm.json | ds-lp-oecm | trust_image_2 | data/oci-photos/OCI-Education-1.jpg | MEDIUM |
| page.oecm.json | ds-lp-oecm | trust_image_3 | data/oci-photos/OCI-Government-Federal-Furniture-Gallery-Image-1.jpg | MEDIUM |
| page.our-work.json | ds-lp-our-work | photo_1 | data/oci-photos/Subject-Areas-boardroom.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_2 | data/oci-photos/Inspiration-Executive-Office.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_3 | data/oci-photos/Inspiration-Conference-1-1.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_4 | data/oci-photos/OCI-Workplace-1.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_5 | data/oci-photos/Inspiration-Reception.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_6 | data/oci-photos/OCI-Healthcare-Carousel-3.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_7 | data/oci-photos/Mattamy-2.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_8 | data/oci-photos/Inspiration-Ergonomics.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_9 | data/oci-photos/OCI-Inspiration-Breakroom.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_10 | data/oci-photos/Pods-4-1.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_11 | data/oci-photos/OCI-Government-Federal-Furniture-Gallery-Image-1.jpg | HIGH |
| page.our-work.json | ds-lp-our-work | photo_12 | data/oci-photos/OCI-Education-1.jpg | HIGH |
| page.professional-services.json | ds-lp-professional-services | hero_image | data/page-images/professional-services/professional-services-space.jpg | HIGH |
| page.professional-services.json | ds-lp-professional-services | trust_image_3 | data/oci-photos/OCI-Workplace-1.jpg | MEDIUM |
| page.quote.json | ds-lp-quote | hero_image | data/oci-photos/OCI-Service-Excellence-1.jpg | MEDIUM |
| page.relocation.json | ds-lp-relocation | hero_image | data/oci-photos/OCI-Services-Relocation-management.jpg | **EXACT** |

---

## Available image inventory by source

### data/page-images/ — 63 images (AI-generated, purpose-named)

Organized in subdirectories by page/context. Key *-space.jpg files are wide lifestyle shots suitable for hero banners:

- `about-us/` — 4 hero variants + 8 crops (team/culture/professional)
- `accessories/` — accessories-space.jpg, accessories-product.jpg
- `acoustic-pods/` — acoustic-pods-product.jpg
- `boardroom/` — boardroom-space.jpg, boardroom-product.jpg
- `brands-hub/` — brands-hub-space.jpg, brands-hub-product.jpg
- `business-furniture/` — business-furniture-space.jpg, business-furniture-product.jpg
- `delivery/` — delivery-space.jpg, delivery-product.jpg
- `design-services/` — design-services-product.jpg (**no space version**)
- `desks/` — desks-space.jpg, desks-product.jpg
- `education/` — education-product.jpg (**no space version** — use OCI-Education-1.jpg for hero)
- `ergocentric/` — ergocentric-space.jpg, ergocentric-product.jpg
- `ergonomic-products/` — ergonomic-products-space.jpg, ergonomic-products-product.jpg
- `global-teknion/` — global-teknion-space.jpg, global-teknion-product.jpg
- `government/` — government-product.jpg (**no space version** — use OCI-Government-* for hero)
- `healthcare/` — healthcare-product.jpg (**no space version** — use OCI-Healthcare-* for hero)
- `industries-hub/` — industries-hub-space.jpg, industries-hub-product.jpg
- `keilhauer/` — keilhauer-space.jpg, keilhauer-product.jpg
- `non-profit/` — non-profit-space.jpg, non-profit-product.jpg
- `panels-room-dividers/` — panels-room-dividers-space.jpg, panels-room-dividers-product.jpg
- `professional-services/` — professional-services-space.jpg, professional-services-product.jpg
- `quiet-spaces/` — quiet-spaces-space.jpg, quiet-spaces-product.jpg
- `seating/` — seating-space.jpg, seating-product.jpg
- `storage/` — storage-space.jpg, storage-product.jpg
- `tables/` — tables-space.jpg, tables-product.jpg
- `task-seating/` — task-seating-space.jpg, task-seating-product.jpg

**Missing space versions:** education, government, healthcare, design-services — these 4 sections must use OCI photos for hero slots.

### data/oci-photos/ — 80 images (real project photos from officecentral.com)

Real project/inspiration photos. Key files by context:

**Healthcare:** OCI-Healthcare-Carousel-3.jpg, OCI-Healthcare-Furniture-Gallery-Image.jpg (both already uploaded to Shopify)  
**Education:** OCI-Education-1.jpg (already uploaded)  
**Government:** OCI-Government-Federal-Furniture-Gallery-Image-1.jpg (already uploaded)  
**About/Team:** About-us-1.webp, About-us-2.webp, About-us-3.webp  
**Office/Workplace:** Inspiration-Workplace.jpg, Smart-workspace-iamge.jpg, OCI-Workplace-1.jpg  
**Executive:** Inspiration-Executive-Office.jpg  
**Conference/Boardroom:** Inspiration-Conference-1-1.jpg, Inspiration-Meeting-1.jpg, Subject-Areas-boardroom.jpg  
**Reception/Lounge:** Inspiration-Reception.jpg, Lounge-Carousel-Image6.jpg  
**Ergonomics:** Inspiration-Ergonomics.jpg  
**Acoustics/Pods:** Inspiration-Accoustics.jpg, Inspiration-Privacy-pods.jpg, Pods-4-1.jpg, Inspiration-Quiet-Zones.jpg  
**Relocation/Services:** OCI-Services-Relocation-management.jpg ← **key file for relocation page**  
**Design/Planning:** OCI-Planning-Desogn.jpg, OCI-VR-Planning.jpg, VR-Planning.jpg  
**Breakroom:** OCI-Inspiration-Breakroom.jpg  
**Service Excellence:** OCI-Service-Excellence-1.jpg, -2.jpg, -3.jpg, -4.jpg  
**Mattamy project (real client):** Mattamy-1.jpg, Mattamy-2.jpg, Mattamy-3.jpg, Mattamy-4.jpg, Mattamy-5.jpg  
**Non-profit/Community:** OCI-Hospitality-1.jpg, OCI-Industries-Hospitality.jpg  
**Storage/Shelving:** OCI-Services-Shelving.jpg  

---

## NO MATCH slots

These 3 slots have no suitable candidate in the current image inventory and require manual decision or new asset sourcing:

| Template | Section | Setting | Why no match | Action needed |
|---|---|---|---|---|
| collection.base.json | ds-cs-base | hero_image | Generic fallback template shared by all sub-collections — one fixed image cannot represent all sub-categories | Leave empty or use a very generic office shot as temporary placeholder; true fix is ensuring every sub-collection has its own suffix with a specific hero |
| collection.category.json | ds-cc-base | hero_image | Same as above — parent template, not a real page | Same as above |
| page.design-services.json | ds-lp-design-services | client_logo | No client logo files exist in data/; schema default references Kawartha Dairy | Source client logo file from Steve (Kawartha Dairy or another approved reference client) |

---

## LOW-confidence slots (need better images)

| Template | Setting | Current best | Why low | Recommended action |
|---|---|---|---|---|
| page.education.json | trust_image_3 | data/oci-photos/Inspiration-Ergonomics.jpg | No 3rd education-specific OCI photo; Ergonomics is not education-specific | Acceptable as placeholder; source an additional education photo post-launch |
| page.healthcare.json | trust_image_3 | data/oci-photos/Inspiration-Reception.jpg | Reception/waiting area works but is not clinical | Acceptable as placeholder; source a 3rd healthcare project photo post-launch |

---

## Top 3 slots with strongest candidate matches (samples for apply phase)

1. **page.about.json → hero_image → data/oci-photos/About-us-1.webp**  
   Confidence: EXACT. Schema `info` tag explicitly calls out this file. File exists locally. Already uploaded to Shopify (used in prior pages) — same asset URL pattern as other populated slots.

2. **page.relocation.json → hero_image → data/oci-photos/OCI-Services-Relocation-management.jpg**  
   Confidence: EXACT. Filename is a semantic direct match ("relocation management"). File is in the OCI catalog, real project photo.

3. **page.our-work.json → photos 1–12 (all 12 slots)**  
   All 12 slots have HIGH-confidence OCI photo matches with label hints in the schema. The Our Work page is the single highest-value image target — 12 real project photos, all matched by label. This is the largest single template to wire in the apply phase.

---

## Recommended next action

**91% of empty slots (51 of 56) have candidate matches.** PAGE-IMG-1 (Step 12, apply phase) can fire immediately with this CSV as input.

**Priority order for apply phase:**

1. **EXACT matches first (9 slots across 8 templates)** — zero ambiguity, just upload + set. About hero, Brands hub hero, 3 brand tile images, 3 brand page heroes, relocation hero. ~15 min.

2. **Our Work page (12 photo slots)** — highest visual impact; all 12 have HIGH-confidence OCI matches with schema label guidance. ~20 min.

3. **Collection hero images (10 slots)** — direct page-images matches; each template already has the logo set. ~20 min.

4. **Remaining page heroes + trust strips (20 slots)** — mix of HIGH and MEDIUM confidence. May require Steve review for trust_image selections (which project photo best represents each sector). ~30 min + Steve review.

5. **NO MATCH / LOW (5 slots)** — defer or source new assets:
   - `client_logo` on design-services: get Kawartha Dairy logo from Steve
   - `trust_image_3` on healthcare + education: acceptable placeholders now; source better photos post-launch
   - `hero_image` on collection.base + collection.category: leave empty (these are generic fallback templates)

**If many images need uploading to Shopify first:** The apply script (PAGE-IMG-1) will need to handle file upload via the Shopify Files API before populating template JSON settings. The CSV candidate paths are local `data/` paths — they need to be uploaded to become `shopify://shop_images/...` URLs. Batch upload is possible via `scripts/push-file.py` pattern or the Admin API files endpoint.

---

_Report generated: 2026-05-13 · PROMPT-5 (Step 15) · Read-only · No theme writes made_  
_CSV: data/reports/image-slot-audit-2026-05-13.csv_
