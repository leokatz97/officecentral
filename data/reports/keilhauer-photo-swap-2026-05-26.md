# KEILHAUER-PHOTO-SWAP-1 — Session Report

**Date:** 2026-05-26 (Day 11+1 late evening session)
**Branch:** `feature/keilhauer-photo-swap-1` (off `feature/hp-hero-office-img`)
**Working dir:** `data/working/keilhauer-photo-swap-2026-05-26/`
**Time:** ~25 min (Phase 0 prep + 2 halts + processing/upload/push/verify)

---

## Summary

Replaced Keilhauer brand hero + brand hub tile photos with a new boardroom scene
(long marble table, tan Keilhauer chairs, floor-to-ceiling city windows). Uploaded
new `-v2.jpg` files to Shopify Files matching peer brand convention. Updated 2
template JSONs and pushed to DEV theme 186373570873 only. LIVE theme untouched
throughout (`updated_at` 2026-05-16T16:47:22-04:00 across all 5 verification points).

---

## Surfaces modified (2)

| # | File | Line | Old → New |
|---|---|---|---|
| 1 | `theme/templates/page.brands-keilhauer.json` | 7 | `bbi-brand-keilhauer-hero.jpg` → `bbi-brand-keilhauer-hero-v2.jpg` |
| 2 | `theme/templates/page.brands.json` | 8 | `bbi-brand-keilhauer-tile.jpg` → `bbi-brand-keilhauer-tile-v2.jpg` |

## New images uploaded to Shopify Files

| Slot | Shopify Files URI | CDN URL | Dims | Size | Q |
|---|---|---|---|---|---|
| Hero | `shopify://shop_images/bbi-brand-keilhauer-hero-v2.jpg` | https://cdn.shopify.com/s/files/1/0859/0413/0361/files/bbi-brand-keilhauer-hero-v2.jpg?v=1779767585 | 1920×1080 | 216 KB | 75 |
| Tile | `shopify://shop_images/bbi-brand-keilhauer-tile-v2.jpg` | https://cdn.shopify.com/s/files/1/0859/0413/0361/files/bbi-brand-keilhauer-tile-v2.jpg?v=1779767586 | 1200×900 | 141 KB | 75 |

Spec matches peer brand files (otg-hero-v2 193 KB · ergocentric-hero-v2 200 KB ·
heartwood-hero 185 KB).

## Source photo

- Path: `/Users/leokatz/Desktop/kielheur/Screenshot 2026-05-25 at 11.39.43 PM.png`
- Dims: 1374×974 PNG (1.41:1, 2.0 MB)
- Subject: Keilhauer-style boardroom — long marble table, ~14 tan camel leather
  Keilhauer chairs, floor-to-ceiling city windows, pendant ring lights,
  wall-mounted TV display, framed art, plant
- Decision (Halt 1): Option A — Lanczos upscale to peer spec (~1.4× factor),
  accept slight softening. Quality eyeballed clean post-process.

## Halts

| Halt | Phase | Decision | Notes |
|---|---|---|---|
| 1 | After Phase 1 audit | "A. Upscale via Lanczos" | Also confirmed audit scope (2 surfaces only — Keilhauer is NOT tiled on any other landing page; 0 Keilhauer-vendor products exist). |
| 2 | After Phase 4 local edits | "apply" | Pushed both template JSONs to DEV. |

## Verification (Phase 6)

### Render checks
- `/pages/brands-keilhauer` → HTTP 200, hero-v2 appears 4× in HTML, old `hero.jpg` 0×
- `/pages/brands` → HTTP 200, tile-v2 appears 3× in HTML, old `tile.jpg` 0×
- `/pages/brands-heartwood` (sanity) → HTTP 200, untouched, no `bbi-brand-keilhauer` refs
- `/pages/brands-otg` (sanity) → HTTP 200, untouched

### Image HEAD
- Hero `https://cdn.shopify.com/.../bbi-brand-keilhauer-hero-v2.jpg`: 200, 221,241 bytes
- Tile `https://cdn.shopify.com/.../bbi-brand-keilhauer-tile-v2.jpg`: 200, 145,343 bytes

### Theme check
- 166 files / 2855 offenses / 166 files with offenses — **exact PRE-LAUNCH-AUDIT-1
  baseline match** (zero new offenses)

### LIVE integrity
- Pre-Phase 1: `2026-05-16T16:47:22-04:00`
- Pre-Halt 1: `2026-05-16T16:47:22-04:00`
- Pre-Halt 2: `2026-05-16T16:47:22-04:00`
- Post-push (Phase 5): `2026-05-16T16:47:22-04:00`

## Backups

- Pre-push: `data/backups/keilhauer-photo-swap-pre-1779767691/`
  - `page.brands-keilhauer.json` (349 bytes — pre-edit)
  - `page.brands.json` (800 bytes — pre-edit)

## Preview URLs for Leo

DEV preview (cookie-based — open via `scripts/bbi-preview-dev.py --path …`):
- `/pages/brands-keilhauer` → Keilhauer brand sub-page hero
- `/pages/brands` → Brand hub (Keilhauer tile in the 3-col grid)

LIVE will reflect on LAUNCH-2 publish (not yet — still blocked on Upwork delivery
+ Step 46 IMAGE SWAP closure + SYS-VERIFY-1 Phase 2 re-run + LAUNCH-0).

## Rollback path

If needed: copy backed-up JSONs back into `theme/templates/` and re-run
`scripts/push-file.py templates/page.brands-keilhauer.json` +
`scripts/push-file.py templates/page.brands.json`. Old `bbi-brand-keilhauer-{hero,tile}.jpg`
files remain in Shopify Files (not deleted).

## Out-of-scope artifacts (informational)

- 18 `bbi-brand-*` files in Shopify Files; old `bbi-brand-keilhauer-{hero,tile}.jpg`
  (now unreferenced — orphan candidates). Did NOT delete.
- 0 `vendor=Keilhauer` products — product image exclusion clause moot.

## Working dir contents

- `raw/keilhauer-boardroom-source.png` (source copy)
- `processed/bbi-brand-keilhauer-hero-v2.jpg` (1920×1080, 216 KB)
- `processed/bbi-brand-keilhauer-tile-v2.jpg` (1200×900, 141 KB)
- `PROCESSED.md` (Phase 2 log with crop notes)
- `upload-create-response.json` (Phase 3 fileCreate API raw)
- `uploaded-final.json` (final READY status + CDN URLs)
