# KEILHAUER-PHOTO-SWAP-1 — Phase 2 Processing Log

**Date:** 2026-05-26 (Day 11+1 evening session)
**Branch:** `feature/keilhauer-photo-swap-1`
**Base:** `feature/hp-hero-office-img` (latest descendant of `feature/about-page-grid-1`)

---

## Source

- **File:** `raw/keilhauer-boardroom-source.png`
- **Original:** `/Users/leokatz/Desktop/kielheur/Screenshot 2026-05-25 at 11.39.43 PM.png`
- **Format:** PNG · sRGB · 8-bit
- **Dimensions:** 1374×974 (1.41:1)
- **File size:** 1,963 KB (2.0 MB)
- **Subject:** Keilhauer-style boardroom — long marble-topped table, ~14 tan/camel leather Keilhauer chairs, floor-to-ceiling city-view windows, pendant ring lights, wall-mounted TV display, framed art, plant

## Processing approach

**Option A** (per HALT 1 user decision): Lanczos upscale to peer brand spec.

ImageMagick pipeline:
```
magick {raw} \
  -auto-orient \
  -filter Lanczos \
  -resize {W}x{H}^ \
  -gravity center \
  -extent {W}x{H} \
  -colorspace sRGB \
  -strip \
  -quality {Q} \
  {processed}
```

Q-escalation: Q85 (291/193 KB — over peer range) → Q80 (244/161 KB — over) → **Q75 (216/141 KB — IN peer range)**.

## Output

| Slot | File | Dims | Aspect | Size | Q | vs. peer |
|---|---|---|---|---|---|---|
| Hero | `processed/bbi-brand-keilhauer-hero-v2.jpg` | 1920×1080 | 16:9 | 216 KB | 75 | ~peer ergocentric-hero-v2 200 KB · heartwood-hero 185 KB · otg-hero-v2 193 KB |
| Tile | `processed/bbi-brand-keilhauer-tile-v2.jpg` | 1200×900 | 4:3 | 141 KB | 75 | ~peer ergocentric-tile-v2 153 KB · heartwood-tile 151 KB · otg-tile-v2 140 KB |

## Crop notes

- **Hero (1920×1080, 16:9):** source 1.41:1 → 16:9 means crop top + bottom. Lost ~½ of ceiling-ring detail and most of carpet foreground. Preserved table, all chairs, windows, TV, art.
- **Tile (1200×900, 4:3):** source 1.41:1 → 4:3 means modest crop of left + right edges. Preserved table, chairs, windows, TV. Slight loss on right wall.

## Quality verification

Visual eyeball of both outputs at full preview size: no Lanczos artifacts on hard edges (window mullions, table edges, chair stitching). Q75 produces no visible compression banding on the marble surface or solid wall areas. Skin-tone equivalents (camel leather) hold cleanly.
