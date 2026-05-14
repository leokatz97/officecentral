# PROMPT-5 Extension: Populated slot classification
_2026-05-13 evening · Read-only · Sub-step of PROMPT-5._

---

## Summary

Classified all 64 populated image_picker slots from PROMPT-5 (commit `790ec26`).

| Classification | Count | Meaning |
|---|---|---|
| KEEP-CURATED | 49 | Already using BBI curated images — no action needed |
| REPLACE-STOCK | 0 | None detected — no pexels/unsplash/hash-only filenames in use |
| REPLACE-WRONG-IMAGE | 4 | Curated image used in semantically wrong slot |
| REVIEW | 11 | Steve decides — kawartha-dairy-logo defaults + unverified OCI filenames |
| **TOTAL** | **64** | |

### Overall image strategy state after PROMPT-5 + extension

| Category | Count | Action |
|---|---|---|
| Empty slots needing fill | 56 | 91% (51/56) have candidate matches in PAGE-IMG-1 inventory |
| KEEP-CURATED | 49 | No action |
| REPLACE-STOCK | 0 | — |
| REPLACE-WRONG-IMAGE | 4 | Replace with better-fit curated candidate |
| REVIEW | 11 | Steve decides before PAGE-IMG-1 apply |
| **Total slots that may change in PAGE-IMG-1** | **71** | 56 empty + 4 wrong-image + 11 REVIEW (if approved) |

---

## REPLACE-WRONG-IMAGE slots (4) — replace recommended

These slots use a curated BBI image but the image is semantically wrong for the context.

| Template | Setting | Current filename | Why wrong | Candidate 1 | Candidate 2 |
|---|---|---|---|---|---|
| page.education.json | trust_image_1 | OCI-Education-1.jpg | **Same image as hero_image on the same page** — trust strip slot 1 duplicates the hero, which reads as a layout error to visitors | Inspiration-Meeting-1.jpg [MEDIUM] | Smart-workspace-iamge.jpg [LOW] |
| page.government.json | trust_image_1 | OCI-Government-Federal-Furniture-Gallery-Image-1 | **Same image as hero_image on the same page** — hero and trust strip slot 1 are identical; fix by swapping to a second institutional OCI photo | Mattamy-1.jpg [MEDIUM] | OCI-Service-Excellence-1.jpg [MEDIUM] |
| page.healthcare.json | trust_image_1 | OCI-Healthcare-Carousel-3.jpg | **Same image as hero_image on the same page** — trust_image_2 already uses OCI-Healthcare-Furniture-Gallery-Image.jpg; need a 3rd distinct clinical/healthcare OCI photo for slot 1 | Inspiration-Reception.jpg [MEDIUM] | OCI-Inspiration-Breakroom.jpg [LOW] |
| page.non-profit.json | trust_image_1 | Mattamy-1.jpg | **Mattamy is a for-profit residential homebuilder** — using a homebuilder project photo on the non-profit sector trust strip is semantically misleading; replace with a community or social-purpose space photo | OCI-Hospitality-1.jpg [MEDIUM] | OCI-Inspiration-Breakroom.jpg [MEDIUM] |

**Root cause for the first three:** `trust_image_1` was set to the same asset as `hero_image` during initial template setup — a copy-paste default. All three pages (education, government, healthcare) have this same pattern.

---

## REVIEW slots (11) — Steve decides

### Group A: Unverified OCI filenames (4 slots on page.industries.json)

These filenames follow the OCI naming convention (`OCI-*`) and are clearly intentional BBI-branded assets, but the exact filenames do **not** appear in `data/oci-photos/` locally. They were likely uploaded directly to Shopify Files via the Admin UI without being added to the local `data/` folder.

| Template | Setting | Current filename | Why unclear | Question for Steve |
|---|---|---|---|---|
| page.industries.json | trust_image_1 | OCI-Healthcare.jpg | Not in local data/oci-photos/ — can't verify if this is a valid OCI project photo or a different asset | Is OCI-Healthcare.jpg a real OCI project photo you uploaded directly? If yes → KEEP. If unknown → replace with OCI-Healthcare-Carousel-3.jpg [MEDIUM] |
| page.industries.json | trust_image_3 | OCI-Government.jpg | Same as above | Is OCI-Government.jpg a valid OCI photo? If yes → KEEP. If unknown → replace with OCI-Government-Federal-Furniture-Gallery-Image-1.jpg [MEDIUM] |
| page.industries.json | tile_image_1 | OCI-Healthcare.jpg | Same file as trust_image_1 — healthcare industry tile | Same question — tile links to healthcare sector page so the image should represent healthcare |
| page.industries.json | tile_image_3 | OCI-Government.jpg | Same file as trust_image_3 — government industry tile | Same question |

**Quick verification:** In Shopify Admin → Content → Files, search for `OCI-Healthcare.jpg` and `OCI-Government.jpg`. If they appear with a recognizable project photo, mark KEEP. If they look wrong or generic, use the MEDIUM candidates above.

### Group B: kawartha-dairy-logo default (6 slots)

`kawartha-dairy-logo` appears in every `testimonial_logo` slot across 6 templates. This is the schema-default placeholder — Kawartha Dairy appears in the design-services schema `info` comment as an example reference client. It was never meant to ship as the universal testimonial logo across all industry pages.

| Template | Setting | Current filename | Question for Steve |
|---|---|---|---|
| page.education.json | testimonial_logo | kawartha-dairy-logo | Is Kawartha Dairy an education sector BBI client? If not, provide the actual client logo (school board, university, etc.) or leave blank until approved |
| page.government.json | testimonial_logo | kawartha-dairy-logo | Replace with a municipal / government client logo, or remove the testimonial block until a real client is secured |
| page.healthcare.json | testimonial_logo | kawartha-dairy-logo | Replace with a clinic / hospital client logo, or remove |
| page.industries.json | testimonial_logo | kawartha-dairy-logo | Industries Hub anchor client — who is the marquee testimonial here? Needs a decision before PAGE-IMG-1 |
| page.non-profit.json | testimonial_logo | kawartha-dairy-logo | Replace with an actual non-profit / community org client logo |
| page.professional-services.json | testimonial_logo | kawartha-dairy-logo | Replace with a law firm, consulting, or private-practice client logo |

**Fastest resolution:** If Kawartha Dairy is genuinely the anchor client for all sectors, the logo can stay — but it would read oddly on a healthcare or government page. More likely, these pages need sector-specific client logos or the testimonial block should be hidden until those logos are secured.

### Group C: Generic image on sector-specific page (1 slot)

| Template | Setting | Current filename | Why unclear | Swap candidate |
|---|---|---|---|---|
| page.non-profit.json | trust_image_2 | Inspiration-Workplace.jpg | Generic open-plan office — not non-profit sector specific. In `data/oci-photos/` so it's a curated image, but it doesn't communicate non-profit context. | OCI-Hospitality-1.jpg [MEDIUM] — community/social-purpose space closer to non-profit |

---

## KEEP-CURATED slots (49) — no action

All `logo` slots (38): every template sets `bbi-logo-v2` — the official BBI logo — confirmed correct across all 38 nav/footer logo slots.

Content image slots verified as curated (11):

| Template | Setting | Filename | Source |
|---|---|---|---|
| page.education.json | hero_image | OCI-Education-1.jpg | data/oci-photos/ ✓ |
| page.government.json | hero_image | OCI-Government-Federal-Furniture-Gallery-Image-1 | data/oci-photos/ ✓ |
| page.healthcare.json | hero_image | OCI-Healthcare-Carousel-3.jpg | data/oci-photos/ ✓ |
| page.healthcare.json | trust_image_2 | OCI-Healthcare-Furniture-Gallery-Image.jpg | data/oci-photos/ ✓ |
| page.industries.json | hero_image | industries-hub-space | data/page-images/industries-hub/ ✓ |
| page.industries.json | trust_image_2 | OCI-Education-1.jpg | data/oci-photos/ ✓ |
| page.industries.json | tile_image_2 | OCI-Education-1.jpg | data/oci-photos/ ✓ |
| page.industries.json | tile_image_4 | OCI-Workplace-1.jpg | data/oci-photos/ ✓ |
| page.industries.json | tile_image_5 | Inspiration-Executive-Office | data/oci-photos/ ✓ |
| page.professional-services.json | trust_image_1 | Inspiration-Executive-Office.jpg | data/oci-photos/ ✓ |
| page.professional-services.json | trust_image_2 | Inspiration-Meeting-1.jpg | data/oci-photos/ ✓ |

---

## Key finding: REPLACE-STOCK = 0

Zero stock photos detected in populated slots. All images in use are:
- BBI official logo (`bbi-logo-v2`)
- OCI project photos (`OCI-*`, `Inspiration-*`, `Mattamy-*`)
- BBI AI-generated page images (`industries-hub-space`)
- One client logo placeholder (`kawartha-dairy-logo`)

No Pexels, Unsplash, hash-only, or `IMG_XXXX`/`DSC_XXXX` filenames found. The store was seeded with real OCI content from the start — good foundation.

---

## Recommendations for PAGE-IMG-1 scope

### Before PAGE-IMG-1 fires — Steve's decisions needed

1. **Verify OCI-Healthcare.jpg and OCI-Government.jpg** in Shopify Admin → Files. 2 slots each = 4 REVIEW slots resolved quickly.
2. **kawartha-dairy-logo decision**: either confirm it's the intended client logo across all pages, or provide sector-appropriate logos. 6 slots. If removing logos is faster, hide the testimonial block per page in the Theme Editor temporarily.
3. **non-profit trust_image_2**: accept generic workspace photo or swap to OCI-Hospitality-1.jpg.

### PAGE-IMG-1 priority order

| Priority | Category | Slots | Est. effort |
|---|---|---|---|
| 1 | Empty slots — EXACT matches (9 slots) | 9 | ~10 min — upload + set, zero ambiguity |
| 2 | Our Work page (12 empty photo slots) | 12 | ~20 min — all HIGH-confidence OCI matches with schema labels |
| 3 | Collection hero images (10 empty slots) | 10 | ~15 min — direct page-images/ matches |
| 4 | REPLACE-WRONG-IMAGE (4 slots) | 4 | ~10 min — all have curated candidates |
| 5 | REVIEW — OCI filename verification (4 slots) | 4 | ~5 min if Steve pre-confirms |
| 6 | Remaining empty page heroes + trust strips (25 slots) | 25 | ~40 min — HIGH/MEDIUM confidence |
| 7 | REVIEW — client logos (6 slots) | 6 | Depends on Steve sourcing logos |
| 8 | NO MATCH slots (3 slots) | 3 | Deferred — client logo or generic template |

**Total slot decisions in PAGE-IMG-1:**
- Fill 56 empty + fix 4 REPLACE-WRONG + resolve up to 11 REVIEW = **up to 71 slot writes**
- Realistic minimum (skipping REVIEW) = **60 slot writes**
- Estimated effort: **2 sessions of ~60 min each** (one for uploads + high-confidence fills; one for trust strips + Steve review slots)

---

_Report generated: 2026-05-13 evening · PROMPT-5-EXTEND · Read-only · No theme writes made_
_Source CSV: data/reports/image-slot-audit-2026-05-13.csv (extended with 4 new columns)_
_Builds on: PROMPT-5 commits 790ec26 + 324df1f_
