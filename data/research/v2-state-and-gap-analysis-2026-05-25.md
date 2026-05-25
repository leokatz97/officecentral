# BBI v2 State + Upwork Gap Analysis — 2026-05-25

Repo state at generation: `main` @ `d3fd023` (after #14a Image slot inventory commit). Read-only analysis. No theme writes, no file moves, no Upwork/v2 modifications.

Drives Step B picker — corrects assumptions in the morning #14a prompt about Upwork delivery location + naming.

---

## Executive Summary

| System | Status |
|---|---|
| `~/Desktop/bbi-images-v2/` | **15 folders, 121 slots total** (15 sourced .jpg files + 100 .txt placeholders + 5 informational READMEs) |
| `~/Desktop/Leo/` | **8 folders, 109 Upwork images** (numbered sequentially — `Brand-banners-1.jpg`, `Category-banners-1.jpg`, etc. — no descriptive names) |
| `bbi-process.sh` | **❌ DOES NOT EXIST** at `/Users/leokatz/Desktop/bbi-images-v2/bbi-process.sh` or anywhere on Desktop |
| **28 CRITICAL+HIGH slot categorization** | |
| ✅ READY-TO-APPLY | **0** |
| 📐 NEEDS-RESIZE | **9** (all 9 category heroes — but they're *wrong orientation*, not just wrong size; resize alone won't fix) |
| 📝 PLACEHOLDER-NEEDS-SOURCING | **10** |
| 🆕 NEEDS-PLACEHOLDER-CREATION | **9** |

**Top finding:** The Upwork delivery is well-sourced and Leo's "inventory is good" is correct — but **none of the 28 CRITICAL+HIGH slots are ready-to-apply today**. Every slot requires at minimum a re-source + new-placeholder + content decision per slot. The 9 sourced files from the May 15 attempt are unusable as-is for the theme's 5:4 spec (portrait orientation; would crop to ~40-55% on apply).

---

## v2 Folder Map

| Folder | Purpose (from README) | Tier | .txt | .jpg | Total slots |
|---|---|---|---:|---:|---:|
| `01-category-heroes/` | Hero banners on `/collections/*` pages | T1 | 0 | 9 | 9 |
| `02-seating-tiles/` | Seating sub-category tiles | T2 | 0 | 6 | 6 |
| `03-desks-tiles/` | Desks sub-category tiles | T2 | 6 | 0 | 6 |
| `04-tables-tiles/` | Tables sub-category tiles | T2 | 4 | 0 | 4 |
| `05-storage-tiles/` | Storage sub-category tiles | T2 | 8 | 0 | 8 |
| `06-boardroom-tiles/` | Boardroom sub-category tiles | T2 | 3 | 0 | 3 |
| `07-accessories-tiles/` | Accessories sub-category tiles | T3 | 5 | 0 | 5 |
| `08-panels-tiles/` | Panels sub-category tiles | T3 | 1 | 0 | 1 |
| `09-ergonomic-tiles/` | Ergonomic sub-category tiles | T3 | 3 | 0 | 3 |
| `10-business-furniture-tiles/` | Business Furniture parent tiles | T2 | 8 | 0 | 8 |
| `11-industry-pages/` | 4 industry heroes + 12 trust images | T1 | 16 | 0 | 16 |
| `12-services-pages/` | Services hero/supporting images | T2 | 6 | 0 | 6 |
| `13-customer-stories/` | Featured project cards | T2 | 3 | 0 | 3 |
| `14-other-pages/` | About + OECM + Quote heroes + OECM trust | T1 | 6 | 0 | 6 |
| `15-brand-pages/` | DEFERRED to BRAND-PAGES-1 — README only, no placeholders | _Deferred_ | 0 | 0 | 0 |

**Total:** 15 .jpg sourced + 69 .txt placeholders = **84 named slots in v2 system** (plus 0 in 15-brand-pages and informational READMEs). Several CRITICAL+HIGH slots have **no v2 placeholder** at all — see "Gaps Beyond v2" below.

### v2 spec vs. theme spec — ⚠️ MISMATCH

| Source | Hero spec | Tile spec |
|---|---|---|
| v2 README + all .txt placeholders | **16:9 / 1920x1080** | 4:3 or 16:10 / 1200x800-900 |
| Image-slot-inventory (theme code) | **5:4** rendered at width=840 | **4:3** rendered at width=600 |

The v2 system was designed against a 16:9 hero spec, but the theme actually renders heroes at 5:4. Either:
- (a) Up-source to 5:4 at min 1050x840, OR
- (b) Accept that 16:9 Upwork-sourced files will be cropped (top+bottom) when slotted into 5:4.

The Upwork delivery is also not 16:9 for every folder (see Upwork Delivery section). Step B picker needs to address this.

---

## v2 Sourced Files (15 .jpg total)

### `01-category-heroes/` — 9 files (all wrong aspect)

Per `01-category-heroes/_cleaned/DIAGNOSIS.md` (auto-generated 2026-05-15): **all 9 files are BOTH upscaled AND heavily cropped** when processed to the v2 spec of 1920x1080. Source ratios 0.79–1.47; target 1.78 (16:9). 2 files (seating-hero, ergonomic-product-hero) also came out grayscale in the _cleaned/ output.

| File | Source dims | Ratio | vs. theme 5:4 spec |
|---|---|---|---|
| `accessories-hero.jpg` | 956x1190 | 0.80 (portrait) | ❌ wrong orientation |
| `boardroom-hero.jpg` | 1908x1298 | 1.47 (landscape, too wide) | ⚠️ landscape, but ~3:2 (would crop sides) |
| `business-furniture-hero.jpg` | 1630x1208 | 1.35 (landscape, ~4:3) | ⚠️ close-ish to 5:4 (1.25), would lightly crop |
| `desks-hero.jpg` | 952x1200 | 0.79 (portrait) | ❌ wrong orientation |
| `ergonomic-product-hero.jpg` | 1620x1268 | 1.28 (landscape, ~5:4) | ✓ best match, but ⚠️ grayscale in _cleaned/ |
| `panels-room-dividers-hero.jpg` | 992x1016 | 0.98 (square) | ❌ near-square |
| `seating-hero.jpg` | 1456x1362 | 1.07 (near-square) | ❌ near-square |
| `storage-hero.jpg` | 956x1202 | 0.80 (portrait) | ❌ wrong orientation |
| `tables-hero.jpg` | 958x1178 | 0.81 (portrait) | ❌ wrong orientation |

There's also `01-category-heroes/_cleaned/` containing 9 processed versions at 1920x1080 (48-185KB each). These are upscaled + heavy-crop derivatives that the May 15 diagnostic explicitly flagged as **blurry/zoomed-in**. **Do not use.**

**Practical implication:** every one of these 9 category-hero slots is effectively 📐 NEEDS-RESIZE in the strict sense — but a true resize cannot fix wrong orientation, so the real path is re-source from Upwork `Categorybanners/`.

### `02-seating-tiles/` — 6 files (4 wrong aspect)

These are MED-priority slots (not part of the 28 CRITICAL+HIGH) but included for completeness because they're populated:

| File | Source dims | Ratio | vs. theme 4:3 spec |
|---|---|---|---|
| `tile-guest-visitor.jpg` | 1022x810 | 1.26 (~5:4) | ⚠️ slightly off (need 1.33) |
| `tile-lounge-soft-seating.jpg` | 1008x838 | 1.20 (~6:5) | ⚠️ slightly off |
| `tile-office-chairs.jpg` | 956x1200 | 0.80 (portrait) | ❌ wrong orientation |
| `tile-outdoor-seating.jpg` | 958x1198 | 0.80 (portrait) | ❌ wrong orientation |
| `tile-stacking-training.jpg` | 958x1194 | 0.80 (portrait) | ❌ wrong orientation |
| `tile-stools-counter.jpg` | 958x1194 | 0.80 (portrait) | ❌ wrong orientation |

Same pattern as 01: ratios ~0.80 (portrait) when theme renders 4:3 (1.33).

---

## v2 Placeholder Slots — .txt files (69 total)

Each .txt names a locked output filename and describes the slot (subject / style / avoid / aspect). All specs use 16:9 hero or 4:3 trust aspect ratios. Highlights covering CRITICAL+HIGH:

### 11-industry-pages/ (16 placeholders)
- `healthcare-hero.jpg.txt` (SLOT 14) → "Clinic waiting room, hospital reception, admin office. Calm, clean."
- `education-hero.jpg.txt` (SLOT 15) → "University, college, training room. Academic, light-filled. Avoid K-12."
- `government-hero.jpg.txt` (SLOT 16) → "Government office — service counter, reception. Avoid political/flags."
- `non-profit-hero.jpg.txt` (SLOT 18) → "Community-oriented non-profit workspace. Warm, mission-driven. Avoid for-profit (Mattamy problem)."
- + 12 trust placeholders (3 per industry; SLOT 85-98 MED — out of CRITICAL+HIGH scope)

### 12-services-pages/ (6 placeholders)
- `professional-services-hero.jpg.txt` (SLOT 17) → "Law/accounting/consulting firm aesthetic. Premium. Avoid tech startup."
- `delivery-hero.jpg.txt` (SLOT 25) → "Delivery truck, warehouse loading, installation crew. Service excellence."
- `relocation-hero.jpg.txt` (SLOT 26) → "Office moving in progress — boxes, furniture, organized crew."
- `design-services-hero.jpg.txt` (SLOT 27) → "Designer at work — space planning, blueprint, 3D rendering."
- `design-services-form-photo.jpg.txt` (SLOT 116 MED) and `professional-services-trust-3.jpg.txt` (SLOT 95 MED) also present.

### 14-other-pages/ (6 placeholders)
- `oecm-hero.jpg.txt` (SLOT 20) → "Public sector procurement — Ontario gov building OK, or multi-sector collage. Avoid US-federal aesthetic."
- `quote-hero.jpg.txt` (SLOT 28) → "Sales rep with client, planner with blueprint, BBI showroom walk-through."
- `about-hero.jpg.txt` (SLOT 135 LOW) + 3 oecm-trust (SLOT 113-115 MED) also present.

### MED-priority placeholders (full list omitted — covered in image-slot-inventory)
- `03-desks-tiles/`: 6 desk sub-tile placeholders (SLOT 55-60)
- `04-tables-tiles/`: 4 (SLOT 69-72)
- `05-storage-tiles/`: 8 (SLOT 61-68)
- `06-boardroom-tiles/`: 3 (SLOT 73-75)
- `07-accessories-tiles/`: 5 (SLOT 80-84)
- `08-panels-tiles/`: 1 (SLOT 79)
- `09-ergonomic-tiles/`: 3 (SLOT 76-78)
- `10-business-furniture-tiles/`: 8 (SLOT 41-48)
- `13-customer-stories/`: 3 (SLOT 118, 119, 120 — 121/122 left blank in template)

### v2 Gaps — slots with NO placeholder at all
| Slot | Page | Why missing |
|---|---|---|
| SLOT 1 (Homepage hero) | `/` | No `00-homepage-hero/` or equivalent folder |
| SLOT 2-4 (3 featured product cards) | `/` | No homepage-featured placeholders |
| SLOT 19 (Industries hub hero) | `/pages/industries` | No `industries-hub-hero.jpg.txt` — only the 4 sub-industries |
| SLOT 21-24 (Brands hub + Heartwood + OTG + GFG heroes) | brand pages | `15-brand-pages/` README-only, explicitly **DEFERRED to BRAND-PAGES-1** |

9 CRITICAL+HIGH slots have no v2 placeholder ready.

---

## Upwork Delivery at `~/Desktop/Leo/`

**Structure matches the 8 folders Leo expected** (the morning prompt's `~/Desktop/bbi-upwork-delivery/` assumption was a path error; content + folder names are correct). Filenames are **sequential numbered files** (e.g. `Brand-banners-1.jpg`, `Brand-banners-2.jpg`) — Leo will need to decide which numbered file maps to which slot during Step B picker.

| Folder | File count | Sample filename | Sample dims | Implied design ratio | Maps to slots |
|---|---:|---|---|---|---|
| `Homepage-Hero/` | 17 | `homepage-hero-1.jpg`...`-17.jpg` | 2560x1440 | **16:9** (1.78) | SLOT 1 |
| `Top product tiles/` | 9 | `Top product tiles 1.jpg`...`-9.jpg` | 1205x900 | **4:3** (1.34) | SLOT 2-4 |
| `Categorybanners/` | 9 | `Category-banners-1.jpg`...`-9.jpg` | 2400x800 | **3:1 ULTRA-WIDE banner** (3.0) ⚠️ | SLOT 5-13 (would crop heavily into 5:4) |
| `Brandbanners/` | 5 | `Brand-banners-1.jpg`...`-5.jpg` | 1600x1280 | **5:4** (1.25) ✓ matches theme hero exactly | SLOT 21-24 (4 needed) |
| `Category service tiles/` | 40 | `Category_service tiles1.jpg`...`-40.jpg` | 1200x1200 | **1:1 square** (1.0) ⚠️ | SLOT 14-19, 25-28 (10+ needed) |
| `Homepage tiles/` | 11 | `Homepage tiles1.jpg`...`-11.jpg` | 1200x1200 | **1:1 square** | SLOT 29-37 MED |
| `Sub Category/` (note trailing space) | 13 | `Sub-category tiles 1.jpg`...`-13.jpg` | 1208x960 | **~5:4** (1.26) | SLOT 41-84 MED (need 44 — short by 31) |
| `Case study cards/` | 5 | `Case-study-cards-1.jpg`...`-5.jpg` | 1800x1200 | **3:2** (1.5) | SLOT 38-40 + trust images MED |

**Total Upwork files: 109.** (Below the 137 slots inventoried — but expected, since MED tile slots could partly re-use v2 .txt or stock fallbacks.)

### Upwork dimension mismatches with theme

- `Categorybanners/` at **2400x800 (3:1)** is dramatically wider than the theme's 5:4 hero (1.25). Direct apply would crop the top + bottom dramatically — but in this case the source is wide-and-short rather than tall-and-narrow, so the top/bottom crop is *unused space*. A center-crop to 5:4 is feasible and probably what Upwork intended. ✓ Usable with awareness.
- `Brandbanners/` at 1600x1280 (5:4) **matches the theme's 5:4 hero spec exactly** — best dimensional match in the entire delivery.
- `Category service tiles/` at 1200x1200 (1:1) → if used for a 5:4 hero, top/bottom crop loses 20%; if for 4:3 tile, sides crop ~12%. ✓ Acceptable both ways.
- `Sub Category/` at 1208x960 (~5:4) is also good for hero use but is named as tiles — naming taxonomy could mislead an automated mapping.
- `Homepage-Hero/` at 2560x1440 (16:9) is more landscape than the theme's 5:4 hero — center-crop sides loses ~22%. ⚠️ Best-case match for SLOT 1.

---

## bbi-process.sh Status

**Verification result: ❌ DOES NOT EXIST.**

- Checked: `/Users/leokatz/Desktop/bbi-images-v2/bbi-process.sh` — not found.
- Searched: `find ~/Desktop -maxdepth 4 -name "*bbi-process*"` — 0 matches.
- Searched: no `.sh` file anywhere in `~/Desktop/bbi-images-v2/`.

**What does exist** (`01-category-heroes/_cleaned/`): the May 15 cleaning attempt was run using **ImageMagick 7.1.2-22 Q16-HDRI aarch64** (per `_cleaned/DIAGNOSIS.md` line 4). That run produced upscaled+cropped 1920x1080 outputs that the auto-generated diagnostic flagged as blurry/zoomed-in. No reusable script artifact survives.

**Dependencies for any future processing script:**
- ImageMagick (`magick` / `convert`) — installed (per the May 15 run history)
- `sips` (built-in macOS) — used for dimension checks in this analysis
- Optional: `cwebp` for .webp output

**Recommendation:** Step B picker should not assume a `bbi-process.sh`. Resize/crop operations should be inlined into the picker workflow (e.g. `magick input.jpg -resize 1050x840^ -gravity center -extent 1050x840 output.jpg` for 5:4 hero).

---

## 28 CRITICAL+HIGH Slot State

| # | Slot | Page | v2 state | Upwork candidate | Category |
|---|---|---|---|---|---|
| 1 | Homepage hero | `/` | ❌ no placeholder | `Homepage-Hero/` (17 files, 2560x1440) | 🆕 |
| 2 | Featured 1 (Heartwood) | `/` | ❌ no placeholder | `Top product tiles/` (9 files, 1205x900) | 🆕 |
| 3 | Featured 2 (OTG) | `/` | ❌ no placeholder | `Top product tiles/` | 🆕 |
| 4 | Featured 3 (GFG) | `/` | ❌ no placeholder | `Top product tiles/` | 🆕 |
| 5 | Business Furniture hero | `/collections/business-furniture` | sourced 1630x1208 (~4:3, wrong) | `Categorybanners/` (9 files, 2400x800) | 📐 |
| 6 | Seating hero | `/collections/seating` | sourced 1456x1362 (~1:1, wrong) | `Categorybanners/` | 📐 |
| 7 | Desks hero | `/collections/desks` | sourced 952x1200 (portrait) | `Categorybanners/` | 📐 |
| 8 | Storage hero | `/collections/storage` | sourced 956x1202 (portrait) | `Categorybanners/` | 📐 |
| 9 | Tables hero | `/collections/tables` | sourced 958x1178 (portrait) | `Categorybanners/` | 📐 |
| 10 | Boardroom hero | `/collections/boardroom` | sourced 1908x1298 (~3:2, off) | `Categorybanners/` | 📐 |
| 11 | Ergonomic Products hero | `/collections/ergonomic-products` | sourced 1620x1268 (~5:4) ⚠️ grayscale-prone | `Categorybanners/` | 📐 |
| 12 | Panels hero | `/collections/panels-room-dividers` | sourced 992x1016 (square) | `Categorybanners/` | 📐 |
| 13 | Accessories hero | `/collections/accessories` | sourced 956x1190 (portrait) | `Categorybanners/` | 📐 |
| 14 | Healthcare hero | `/pages/healthcare` | 📝 `11-industry-pages/healthcare-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 15 | Education hero | `/pages/education` | 📝 `11-industry-pages/education-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 16 | Government hero | `/pages/government` | 📝 `11-industry-pages/government-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 17 | Pro Services hero | `/pages/professional-services` | 📝 `12-services-pages/professional-services-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 18 | Non-Profit hero | `/pages/non-profit` | 📝 `11-industry-pages/non-profit-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 19 | Industries hub hero | `/pages/industries` | ❌ no placeholder | `Category service tiles/` | 🆕 |
| 20 | OECM hero | `/pages/oecm` | 📝 `14-other-pages/oecm-hero.jpg.txt` | `Categorybanners/` or `Category service tiles/` | 📝 |
| 21 | Brands hub hero | `/pages/brands` | ❌ (15-brand-pages DEFERRED) | `Brandbanners/` (5 files, 1600x1280) ✓ | 🆕 |
| 22 | Heartwood brand hero | `/pages/brands-heartwood` | ❌ | `Brandbanners/` | 🆕 |
| 23 | OTG brand hero | `/pages/brands-otg` | ❌ | `Brandbanners/` | 🆕 |
| 24 | GFG brand hero | `/pages/brands-global-teknion` | ❌ | `Brandbanners/` | 🆕 |
| 25 | Delivery hero | `/pages/delivery` | 📝 `12-services-pages/delivery-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 26 | Relocation hero | `/pages/relocation` | 📝 `12-services-pages/relocation-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 27 | Design Services hero | `/pages/design-services` | 📝 `12-services-pages/design-services-hero.jpg.txt` | `Category service tiles/` | 📝 |
| 28 | Quote hero | `/pages/quote` | 📝 `14-other-pages/quote-hero.jpg.txt` | `Category service tiles/` or `Categorybanners/` | 📝 |

---

## Gap Summary by Category

### ✅ READY-TO-APPLY (0)
None. No slot has a correctly-sized sourced v2 file matching theme spec.

### 📐 NEEDS-RESIZE (9) — all category heroes from `01-category-heroes/`
SLOT 5-13: business-furniture, seating, desks, storage, tables, boardroom, ergonomic-product, panels-room-dividers, accessories.

⚠️ **"Resize" is misleading for these.** All 9 source files are in wrong orientation (portrait or near-square) for the theme's 5:4 landscape hero. A resize-and-crop would lose 40-55% of the image content. **Real path forward = re-source from Upwork `Categorybanners/` (9 files at 2400x800)**, then center-crop to 5:4. The v2 `.jpg` filenames stay the same (locked output names); only the *source file* changes.

### 📝 PLACEHOLDER-NEEDS-SOURCING (10)
Each has a v2 .txt placeholder defining the locked output filename + slot spec. Candidates from Upwork numbered files; Leo picks one per slot in Step B.

| Slot | v2 placeholder | Upwork candidate folder | Note |
|---|---|---|---|
| 14 | `11-industry-pages/healthcare-hero.jpg.txt` | `Category service tiles/` (40 files at 1:1) | Square → 5:4 crops top+bottom 20% |
| 15 | `11-industry-pages/education-hero.jpg.txt` | `Category service tiles/` | Same |
| 16 | `11-industry-pages/government-hero.jpg.txt` | `Category service tiles/` | Same |
| 17 | `12-services-pages/professional-services-hero.jpg.txt` | `Category service tiles/` | Same |
| 18 | `11-industry-pages/non-profit-hero.jpg.txt` | `Category service tiles/` | Avoid for-profit (Mattamy problem flagged in spec) |
| 20 | `14-other-pages/oecm-hero.jpg.txt` | `Categorybanners/` or `Category service tiles/` | Best Upwork file likely from `Categorybanners/` if a government-context-1 exists |
| 25 | `12-services-pages/delivery-hero.jpg.txt` | `Category service tiles/` | Need warehouse/loading subject |
| 26 | `12-services-pages/relocation-hero.jpg.txt` | `Category service tiles/` | Need moving/boxes subject |
| 27 | `12-services-pages/design-services-hero.jpg.txt` | `Category service tiles/` | Need designer/planning subject |
| 28 | `14-other-pages/quote-hero.jpg.txt` | `Category service tiles/` or `Categorybanners/` | Sales/consult subject |

### 🆕 NEEDS-PLACEHOLDER-CREATION (9)
Either no v2 folder exists for the surface, or the folder is deferred. Step B needs to create the .txt placeholder + locked filename FIRST, then source from Upwork.

| Slot | Surface | Proposed v2 path + filename | Upwork candidate |
|---|---|---|---|
| 1 | Homepage hero | New `00-homepage/` or `14-other-pages/homepage-hero.jpg.txt` | `Homepage-Hero/` (17 files) — best-fit at 16:9 |
| 2 | Featured product 1 (Heartwood L-Shape Adj Desk) | New folder or extend 14 — `featured-1-heartwood.jpg.txt` | `Top product tiles/` (9 files) — 4:3 match |
| 3 | Featured product 2 (OTG Raven Chair) | `featured-2-otg.jpg.txt` | `Top product tiles/` |
| 4 | Featured product 3 (GFG Accord Tilter) | `featured-3-gfg.jpg.txt` | `Top product tiles/` |
| 19 | Industries hub | New `11-industry-pages/industries-hub-hero.jpg.txt` | `Category service tiles/` |
| 21 | Brands hub | New `15-brand-pages/brands-hub-hero.jpg.txt` (un-defer) | `Brandbanners/` (5 files, 5:4 ✓) |
| 22 | Heartwood brand | New `15-brand-pages/heartwood-hero.jpg.txt` | `Brandbanners/` |
| 23 | OTG brand | New `15-brand-pages/otg-hero.jpg.txt` | `Brandbanners/` |
| 24 | GFG brand | New `15-brand-pages/global-teknion-hero.jpg.txt` | `Brandbanners/` |

**Note on Brandbanners math:** 5 Upwork files for 4 needed slots (21-24). The 5th can serve as a backup or be assigned to one of the 3 out-of-scope brand pages (ergocentric / keilhauer / obusforme) flagged in the morning inventory.

---

## Recommended Workflow Path

### Should Step B use `bbi-process.sh`?
**No** — it doesn't exist. Inline ImageMagick commands (`magick input.jpg -resize WxH^ -gravity center -extent WxH output.jpg`) per slot are simpler than rebuilding a generic batch script for this one-time-cleanup operation. ImageMagick is already installed on the machine (per `_cleaned/DIAGNOSIS.md` history).

### Recommended order for Step B picker

**Path 1 — 🆕 NEEDS-PLACEHOLDER-CREATION + 📐 NEEDS-RESIZE (Upwork→v2 bulk swap) — ~25 min**

Since 9 of the 9 NEEDS-RESIZE slots are best fixed by re-sourcing from Upwork `Categorybanners/`, AND the 9 NEEDS-PLACEHOLDER-CREATION slots also need new Upwork picks, bundle these into one workflow:

1. For each of SLOT 1 + 19 + 21-24 + 2-4 (9 🆕 slots): create v2 .txt placeholder w/ filename + spec (~2 min/slot)
2. For each of SLOT 5-13 (9 📐 slots): replace existing v2 .jpg with Upwork `Categorybanners/` pick (~1 min/slot)
3. Center-crop all 18 to 5:4 (heroes) / 4:3 (featured cards) via `magick` (~1 min/slot)

**Path 2 — 📝 PLACEHOLDER-NEEDS-SOURCING (interactive picker) — ~20 min**

10 slots, ~2 min/slot. Show Leo the v2 .txt spec next to Upwork folder filenames + sample dimensions; he picks one number per slot.

**Path 3 — Apply (upload to Shopify Files + theme JSON edits) — ~30-45 min**

Per CLAUDE.md `push-*` scripts pattern + `image-slot-inventory` apply paths. This is Step C, not Step B.

### Total time for CRITICAL+HIGH

| Step | Time |
|---|---|
| Step B picker (Path 1 + 2) | ~45 min |
| Step C apply | ~30-45 min |
| **Total** | **~75-90 min** |

This is roughly the morning estimate (56 min picker + 30 min apply) plus the .txt-creation overhead the morning prompt didn't anticipate.

### Should Step B picker handle resize?

**Yes — for the 9 📐 slots minimum.** A picker that doesn't address dimensions just hands the same problem to Step C. Inline `magick` cropping at the moment of file selection is the cleanest split.

For 📝 slots from `Category service tiles/` (square 1:1), the picker should show Leo a preview of how the 5:4 crop will look (top+bottom 20% lost), so he can pick a file where the subject is centered vertically.

---

## Notable Findings

1. **The morning prompt's `bbi-upwork-delivery/` path was wrong** — actual location is `~/Desktop/Leo/`. Folder structure matches expected 8 folders.
2. **`bbi-process.sh` does not exist** — Leo's recollection was incorrect (or the file was deleted). The only related artifact is `01-category-heroes/_cleaned/` with a DIAGNOSIS.md from a one-off May 15 ImageMagick run.
3. **The v2 system is built against 16:9 hero spec, but the theme renders 5:4** — a fundamental conflict the picker needs to acknowledge. Either re-spec v2 to 5:4 or accept top+bottom crop on apply.
4. **Leo's "inventory is good but sizing is off" was generous to the May 15 attempt** — all 9 category-hero source files are in wrong orientation (portrait or square). The DIAGNOSIS.md from May 15 already flagged this in writing.
5. **0 slots are ready-to-apply** — no fast-track wins. Every CRITICAL+HIGH slot requires at least one decision from Leo before it can ship.
6. **9 brand/homepage slots have no v2 placeholder yet** — Step B needs a "create placeholder" sub-step the morning plan didn't account for. ~2 min/slot.
7. **Upwork `Brandbanners/` is perfectly sized for brand heroes** (1600x1280 = 5:4 exact). One bright spot in the delivery.
8. **Upwork `Categorybanners/` is 2400x800 (3:1)** — wider than expected but center-crops cleanly to 5:4 without losing content (unlike v2 source files where the source is portrait + the crop loses subject area).
9. **The Upwork delivery uses sequential numbered filenames** (not descriptive). The picker is genuinely needed — automated mapping by filename is impossible.
10. **`Category service tiles/` has 40 files for ~10 slot picks (14-18, 25-28, 19)** — generous surplus, but all 1:1 square; need vertical-center-cropped subjects.
