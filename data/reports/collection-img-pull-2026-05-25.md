# COLLECTION-IMG-PULL-1 — Session Report (2026-05-25)

**Task:** programmatic pull of 1 lead product image per collection / sub-collection → resize + crop to slot spec → upload to Shopify Files → patch hero_image / tile image settings across the 9 category-template JSONs on DEV theme `186373570873`.

**Scope:** 9 category-collection heroes + 44 sub-category tiles = **53 slots**.

**Honest-scope context (preserved from the prompt):** This is the PAGE-IMG-1 (commit be1409d) pattern re-applied to fill the launch-day collection-page image slots. Day 3 visual-quality concerns accepted by Leo. The Upwork bbi-images-v2 hand-sourced photos remain available as a Day 12-13 re-polish pass if specific slots look bad after launch.

## Summary

| Metric | Value |
|---|---:|
| Total slots | 53 (9 hero + 44 tile) |
| REPLACE rows in mapping | 53 |
| SKIP rows | 0 |
| Phase 2 downloads OK | 53/53 |
| Phase 3 processed OK | 53/53 (Q85, no Q reduction needed; max size 137.4 KB) |
| Phase 4 Shopify Files uploads READY | 53/53 |
| Phase 5 DEV template writes verified | 53/53 |
| Bucket B slots (homepage) KEEP | 0 (not in scope) |
| Lead-product selection — bestseller-driven | 37 |
| Lead-product selection — first-in-collection | 16 |

## HALT decisions

- **HALT 1 — Phase 1 mapping:** initial run produced 2 SKIPs (`accessories-hero` + `business-furniture-tile-accessories` — both pointed at `/collections/accessories` whose first bestseller `caster-options` has 0 images). Leo upgraded selection logic to *first bestseller WITH at least one image* (then fallback to first product with images). Re-run produced 53 REPLACE / 0 SKIP. Selection rule change persisted in [scripts/collection-img-pull-phase1-mapping.py](scripts/collection-img-pull-phase1-mapping.py) for future use.
- **HALT 2 — Phase 3 spot-check:** 3 hero (`desks-hero`, `storage-hero`, `panels-room-dividers-hero`) + 3 tile (`business-furniture-tile-boardroom`, `storage-tile-pedestals`, `desks-tile-straight`) reviewed via [SPOT-CHECK-2x3.jpg](data/working/collection-img-pull-2026-05-25/SPOT-CHECK-2x3.jpg) contact sheet. Leo approved "looks good". Two surface-level category-match concerns surfaced and accepted as the Day 3 visual compromise: `business-furniture-tile-boardroom` lead product reads more as a desk than a boardroom item, and `desks-tile-straight` (Single-Surface Desks) lead reads more as an executive desk. Both candidates for Day 12-13 hand-swap from bbi-images-v2 if Leo wants to upgrade them.
- **HALT 3 — Phase 5 apply:** Leo approved "apply". Backups taken pre-write.

## Backups

Pre-write template JSON snapshots: `data/backups/collection-img-pull-pre-20260525-161759/` (9 files).

To roll back any single template:

```bash
# Restore one template to its pre-apply state on DEV theme 186373570873
HANDLE=seating  # change to the template you want to roll back
cp "data/backups/collection-img-pull-pre-20260525-161759/collection.${HANDLE}.json" "theme/templates/"
python3 scripts/push-file.py "templates/collection.${HANDLE}.json"
```

## Verification

- **Admin API re-fetch (strongest signal):** all 9 templates show 1 hero `bbi-coll-img-<handle>-hero` setting + N tile `bbi-coll-img-<handle>-tile-<key>` settings, totaling 53/53.
- **`shopify theme check`:** 265 files / 2855 offenses across 166 files — identical to the PR-1 / PR-2 baseline (no new offenses introduced; the 9 changed JSONs are valid Shopify template settings).
- **DEV preview HEAD (unauthenticated):** all 9 URLs return 301 (redirect to admin login — expected for unpublished theme behind preview-auth gate; not a useful signal without an authenticated browser session). Documented as a limitation.
- **LIVE HEAD:** all 9 URLs return 200 — Avada theme still healthy; nothing was pushed LIVE.

## Spec compliance

- Hero slots (9): processed to 1920x1080 JPG sRGB Q85 (min 46.5 KB / max 137.4 KB).
- Tile slots (44): processed to 1200x900 JPG sRGB Q85 (min 18.6 KB / max 120.5 KB).
- All 53 outputs well under the 2MB budget — no Q<85 reductions required.

## Notes / follow-up

- **Source-image resolution gap:** many lead products had master images in the 300-1000 px range. Upscaling to 1920x1080 (hero) or 1200x900 (tile) produces visible softening. The white-background product photos still read cleanly at category-page zoom levels. Slots that look weakest after LAUNCH-2 are tagged in the spot-check notes as Day 12-13 hand-swap candidates.
- **Category-match concerns (HALT 2 follow-up):** `business-furniture-tile-boardroom` and `desks-tile-straight` candidates for Day 12-13 re-polish via bbi-images-v2.
- **Bucket B (homepage hero + 3 featured product cards)** — NOT in scope of this session. Those 4 slots live in `templates/index.json` via CSS-class placeholders and are handled separately (per Idea #15: Heartwood L-Shape Adjustable Desk Set, OTG Raven OTG10703B, GFG Global Accord Tilter).
- **Cornerstone Post 1** featured image still null — deferred to Tuesday per bbi-build-state.md.

## Final mapping (53 slots)

| slot_id | type | template | collection_handle | lead_product | selection | new shopify:// URI |
|---|---|---|---|---|---|---|
| `seating-hero` | hero | collection.seating.json | `seating` | `obusforme-comfort-high-back-chair-fabric-1` | bestseller | `shopify://shop_images/bbi-coll-img-seating-hero.jpg` |
| `seating-tile-office-chairs` | tile | collection.seating.json | `task-chairs` | `mvl2786-yoho-armless-low-back-task-chair` | bestseller | `shopify://shop_images/bbi-coll-img-seating-tile-office-chairs.jpg` |
| `seating-tile-guest-seating` | tile | collection.seating.json | `guest-seating` | `sidero-guest-chair-28-colour-options` | bestseller | `shopify://shop_images/bbi-coll-img-seating-tile-guest-seating.jpg` |
| `seating-tile-training` | tile | collection.seating.json | `stacking-seating` | `sonic-armchair-polypropylene-seat-back-651` | first_in_collection | `shopify://shop_images/bbi-coll-img-seating-tile-training.jpg` |
| `seating-tile-stools` | tile | collection.seating.json | `stools` | `ibex-mesh-back-drafting-stool-task-chair-w` | bestseller | `shopify://shop_images/bbi-coll-img-seating-tile-stools.jpg` |
| `seating-tile-lounge` | tile | collection.seating.json | `lounge-seating` | `citi-lounge-seating-3-sizes-available` | bestseller | `shopify://shop_images/bbi-coll-img-seating-tile-lounge.jpg` |
| `seating-tile-outdoor` | tile | collection.seating.json | `outdoor-seating` | `outdoor-steel-bench` | bestseller | `shopify://shop_images/bbi-coll-img-seating-tile-outdoor.jpg` |
| `desks-hero` | hero | collection.desks.json | `desks` | `height-adjustable-table-5-sizes` | bestseller | `shopify://shop_images/bbi-coll-img-desks-hero.jpg` |
| `desks-tile-height-adjustable` | tile | collection.desks.json | `height-adjustable-tables-desks` | `height-adjustable-table-5-sizes` | bestseller | `shopify://shop_images/bbi-coll-img-desks-tile-height-adjustable.jpg` |
| `desks-tile-l-shape` | tile | collection.desks.json | `l-shape-desks` | `l-shape-desk-hutch` | bestseller | `shopify://shop_images/bbi-coll-img-desks-tile-l-shape.jpg` |
| `desks-tile-straight` | tile | collection.desks.json | `straight-desks` | `innovations-double-pedestal-desk-bf-bf-5-s` | bestseller | `shopify://shop_images/bbi-coll-img-desks-tile-straight.jpg` |
| `desks-tile-reception` | tile | collection.desks.json | `reception-desks-desks` | `l-shape-reception-72-x-72-x-41-1` | bestseller | `shopify://shop_images/bbi-coll-img-desks-tile-reception.jpg` |
| `desks-tile-computer` | tile | collection.desks.json | `multi-person-workstations-desks` | `evolve-workstations` | first_in_collection | `shopify://shop_images/bbi-coll-img-desks-tile-computer.jpg` |
| `desks-tile-executive-desks` | tile | collection.desks.json | `office-suites-desks` | `temptations-office-suite-copy` | first_in_collection | `shopify://shop_images/bbi-coll-img-desks-tile-executive-desks.jpg` |
| `tables-hero` | hero | collection.tables.json | `tables` | `premium-height-adjustable-table-1` | bestseller | `shopify://shop_images/bbi-coll-img-tables-hero.jpg` |
| `tables-tile-conference-tables` | tile | collection.tables.json | `meeting-conference-room-tables` | `boat-shaped-conference-table` | bestseller | `shopify://shop_images/bbi-coll-img-tables-tile-conference-tables.jpg` |
| `tables-tile-training-tables` | tile | collection.tables.json | `training-room-tables` | `training-flip-top-tables-1` | bestseller | `shopify://shop_images/bbi-coll-img-tables-tile-training-tables.jpg` |
| `tables-tile-height-adjustable-tables` | tile | collection.tables.json | `height-adjustable-tables` | `height-adjustable-table-5-sizes` | bestseller | `shopify://shop_images/bbi-coll-img-tables-tile-height-adjustable-tables.jpg` |
| `tables-tile-collaborative` | tile | collection.tables.json | `meeting-tables` | `loop-leg-table` | bestseller | `shopify://shop_images/bbi-coll-img-tables-tile-collaborative.jpg` |
| `storage-hero` | hero | collection.storage.json | `storage` | `pedestal-box-box-file-with-or-without-whee` | bestseller | `shopify://shop_images/bbi-coll-img-storage-hero.jpg` |
| `storage-tile-lateral-files` | tile | collection.storage.json | `lateral-file-cabinets-storage` | `premium-series-lateral-file-cabinet-2-3-4-` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-lateral-files.jpg` |
| `storage-tile-vertical-files` | tile | collection.storage.json | `vertical-file-cabinets-storage` | `vertical-file-2-drawer-letter` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-vertical-files.jpg` |
| `storage-tile-pedestals` | tile | collection.storage.json | `mobile-pedestals` | `mobile-pedestal-drawer-box-file` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-pedestals.jpg` |
| `storage-tile-storage-cabinets` | tile | collection.storage.json | `storage-cabinets` | `wood-laminate-storage-cabinets` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-storage-cabinets.jpg` |
| `storage-tile-bookcases` | tile | collection.storage.json | `bookcases` | `bookcase-31-5-wide-x-13-75-deep` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-bookcases.jpg` |
| `storage-tile-lockers` | tile | collection.storage.json | `lockers` | `laminate-lockers-1` | first_in_collection | `shopify://shop_images/bbi-coll-img-storage-tile-lockers.jpg` |
| `storage-tile-credenzas` | tile | collection.storage.json | `credenzas` | `credenza-scmsu` | bestseller | `shopify://shop_images/bbi-coll-img-storage-tile-credenzas.jpg` |
| `storage-tile-wardrobe` | tile | collection.storage.json | `wardrobe-storage` | `cabinet-file-file-right-wardrobe-inv-6524c` | first_in_collection | `shopify://shop_images/bbi-coll-img-storage-tile-wardrobe.jpg` |
| `boardroom-hero` | hero | collection.boardroom.json | `boardroom` | `premium-height-adjustable-table-1` | bestseller | `shopify://shop_images/bbi-coll-img-boardroom-hero.jpg` |
| `boardroom-tile-boardroom-tables` | tile | collection.boardroom.json | `meeting-conference-room-tables` | `boat-shaped-conference-table` | bestseller | `shopify://shop_images/bbi-coll-img-boardroom-tile-boardroom-tables.jpg` |
| `boardroom-tile-boardroom-storage` | tile | collection.boardroom.json | `credenzas` | `credenza-scmsu` | bestseller | `shopify://shop_images/bbi-coll-img-boardroom-tile-boardroom-storage.jpg` |
| `boardroom-tile-av-furniture` | tile | collection.boardroom.json | `podiums-av-furniture` | `av-stand-sa-81-3016` | first_in_collection | `shopify://shop_images/bbi-coll-img-boardroom-tile-av-furniture.jpg` |
| `accessories-hero` | hero | collection.accessories.json | `accessories` | `aeramax-air-purifier-true-hepa-plasmatrue-` | bestseller | `shopify://shop_images/bbi-coll-img-accessories-hero.jpg` |
| `accessories-tile-lighting` | tile | collection.accessories.json | `lighting` | `humanscale-nova-lighting` | first_in_collection | `shopify://shop_images/bbi-coll-img-accessories-tile-lighting.jpg` |
| `accessories-tile-whiteboards` | tile | collection.accessories.json | `white-board` | `white-board-magnetic-mobile-on-wheels` | first_in_collection | `shopify://shop_images/bbi-coll-img-accessories-tile-whiteboards.jpg` |
| `accessories-tile-chair-mats` | tile | collection.accessories.json | `chair-mats` | `polycarbonate-chairmat-for-hard-floors-har` | first_in_collection | `shopify://shop_images/bbi-coll-img-accessories-tile-chair-mats.jpg` |
| `accessories-tile-monitor-arms` | tile | collection.accessories.json | `monitor-arms` | `laptop-holder-for-100-ma1c-100-ma2c-monito` | first_in_collection | `shopify://shop_images/bbi-coll-img-accessories-tile-monitor-arms.jpg` |
| `accessories-tile-acoustic-solutions` | tile | collection.accessories.json | `acoustic-solutions` | `ceiling-baffles-sound-acoustic-dampeners` | first_in_collection | `shopify://shop_images/bbi-coll-img-accessories-tile-acoustic-solutions.jpg` |
| `panels-room-dividers-hero` | hero | collection.panels-room-dividers.json | `panels-room-dividers` | `desk-top-dividers-1` | first_in_collection | `shopify://shop_images/bbi-coll-img-panels-room-dividers-hero.jpg` |
| `panels-room-dividers-tile-room-dividers` | tile | collection.panels-room-dividers.json | `room-dividers` | `felt-acoustic-room-dividers` | first_in_collection | `shopify://shop_images/bbi-coll-img-panels-room-dividers-tile-room-dividers.jpg` |
| `ergonomic-products-hero` | hero | collection.ergonomic-products.json | `ergonomic-products` | `anti-fatigue-wellness-mat-36-x-24-5` | bestseller | `shopify://shop_images/bbi-coll-img-ergonomic-products-hero.jpg` |
| `ergonomic-products-tile-sit-stand-converters` | tile | collection.ergonomic-products.json | `desktop-sit-stand` | `sit-stand-adjustable-desk-riser-32-wide` | bestseller | `shopify://shop_images/bbi-coll-img-ergonomic-products-tile-sit-stand-converters.jpg` |
| `ergonomic-products-tile-monitor-arms` | tile | collection.ergonomic-products.json | `monitor-arms` | `laptop-holder-for-100-ma1c-100-ma2c-monito` | first_in_collection | `shopify://shop_images/bbi-coll-img-ergonomic-products-tile-monitor-arms.jpg` |
| `ergonomic-products-tile-keyboard-trays` | tile | collection.ergonomic-products.json | `keyboard-trays` | `jax-sit-to-stand` | first_in_collection | `shopify://shop_images/bbi-coll-img-ergonomic-products-tile-keyboard-trays.jpg` |
| `business-furniture-hero` | hero | collection.business-furniture.json | `business-furniture` | `height-adjustable-table-5-sizes` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-hero.jpg` |
| `business-furniture-tile-seating` | tile | collection.business-furniture.json | `seating` | `obusforme-comfort-high-back-chair-fabric-1` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-seating.jpg` |
| `business-furniture-tile-desks` | tile | collection.business-furniture.json | `desks` | `height-adjustable-table-5-sizes` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-desks.jpg` |
| `business-furniture-tile-storage` | tile | collection.business-furniture.json | `storage` | `pedestal-box-box-file-with-or-without-whee` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-storage.jpg` |
| `business-furniture-tile-tables` | tile | collection.business-furniture.json | `tables` | `premium-height-adjustable-table-1` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-tables.jpg` |
| `business-furniture-tile-boardroom` | tile | collection.business-furniture.json | `boardroom` | `premium-height-adjustable-table-1` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-boardroom.jpg` |
| `business-furniture-tile-ergonomic` | tile | collection.business-furniture.json | `ergonomic-products` | `anti-fatigue-wellness-mat-36-x-24-5` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-ergonomic.jpg` |
| `business-furniture-tile-panels` | tile | collection.business-furniture.json | `panels-room-dividers` | `desk-top-dividers-1` | first_in_collection | `shopify://shop_images/bbi-coll-img-business-furniture-tile-panels.jpg` |
| `business-furniture-tile-accessories` | tile | collection.business-furniture.json | `accessories` | `aeramax-air-purifier-true-hepa-plasmatrue-` | bestseller | `shopify://shop_images/bbi-coll-img-business-furniture-tile-accessories.jpg` |
