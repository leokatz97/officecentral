# Stage 3.2a — Image Cropping Diagnosis

**Generated:** 2026-05-07  
**File:** `theme/sections/ds-cs-base.liquid`  
**Issue:** Chair photos cropped too tight; headrests and foot rings cut off; sizing appears inconsistent card-to-card

---

## Current State

### Liquid image rendering (line 450)
```liquid
{{ product.featured_media | image_url: width: 480 | image_tag: loading: 'lazy', alt: card_img_alt }}
```

No `height:` or `crop:` parameter. Shopify CDN serves the image at 480px wide, maintaining the **native aspect ratio** of the source image.

### CSS card container (lines 196–204)
```css
.ds-cs__card-img {
  aspect-ratio: 4/3;    /* landscape — 1.333:1 */
  overflow: hidden;
  background: var(--alternateBackground);
  border-bottom: 1px solid rgba(var(--borderColor-rgb), 0.5);
}
.ds-cs__card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;    /* crops to fill the container */
}
```

### Actual catalog image dimensions (sampled from `highback-seating` via Admin API)

| Product | Width | Height | Ratio |
|---|---|---|---|
| ObusForme Comfort high back chair | 500 | 500 | **1:1 square** |
| Format high mesh back synchro-tilter | 710 | 710 | **1:1 square** |
| Chevron ultra high back multi-tilter | 485 | 485 | **1:1 square** |

All sampled images are **1:1 square**. This is consistent with the source catalog (product photography supplied by manufacturers is predominantly square).

---

## Root Cause

**Two-layer mismatch:**

1. **Container vs. source aspect ratio:** Container is `4/3` (landscape: wider than tall). Source images are `1/1` (square). With `object-fit: cover`, the browser scales the 1:1 image to fill the container width (480px → 480×480), then the height overflows the 360px container by 120px — **clipping 60px from top and 60px from bottom, a 25% vertical crop on each side.**

2. **What gets cut:** Chair headrests (above center) and foot rings/caster bases (below center) are in the top and bottom 25% of the frame. `object-fit: cover` centers the clip, so both are simultaneously truncated.

**Why sizes "vary card-to-card":** The visual impression of inconsistent sizing comes from the crop, not from card sizing. Chairs with lower seats look truncated at the bottom; chairs with tall headrests look truncated at the top. The cards themselves are the same size.

**Component spec mismatch:** `bbi-component-spec-v1.md` (line 239) specifies product cards should use a **4:5 image** (portrait, 0.8:1). The current code uses 4:3 (landscape, 1.33:1) — the opposite direction from the spec. Using 4:5 on 1:1 source images would clip sides (20% each side) instead of top/bottom, which is arguably worse for symmetrical chair photography.

---

## Options Analysis

| Option | Aspect ratio | Effect on 1:1 source | Spec alignment |
|---|---|---|---|
| A — Fix to spec | 4:5 portrait | ~20% left+right clip | ✅ Matches bbi-component-spec-v1.md |
| B — Square container | 1:1 | **0% clip — full image shown** | Deviation from spec but best for current stock |
| C — Keep current | 4:3 landscape | ~25% top+bottom clip | Mismatches spec; causes current problem |
| D — object-fit: contain | Any ratio | No clip; adds whitespace | No spec entry; breaks card grid uniformity |
| E — CDN-level crop | 4:3 with crop:center | Same visual result as C; just faster | No improvement |

---

## Proposed Fix

**Recommended:** Option B — change container to 1:1 square.

Rationale: The actual image stock is square. Changing to 1:1 eliminates all cropping for current inventory while giving clean, consistent card thumbnails across the grid. The 4:5 spec was written for a portrait product photo convention that the BBI catalog doesn't follow.

If the image pipeline (Phase 3 AI img2img) produces portrait images in the future, the container can be revisited. For now, 1:1 is the correct default.

### Code changes (both required)

**CSS — change `.ds-cs__card-img`:**
```css
/* BEFORE */
.ds-cs__card-img {
  aspect-ratio: 4/3;
  overflow: hidden;
  background: var(--alternateBackground);
  border-bottom: 1px solid rgba(var(--borderColor-rgb),0.5);
}

/* AFTER */
.ds-cs__card-img {
  aspect-ratio: 1/1;
  overflow: hidden;
  background: var(--alternateBackground);
  border-bottom: 1px solid rgba(var(--borderColor-rgb),0.5);
}
```

**Liquid — add height param to match square ratio:**
```liquid
/* BEFORE */
{{ product.featured_media | image_url: width: 480 | image_tag: loading: 'lazy', alt: card_img_alt }}

/* AFTER */
{{ product.featured_media | image_url: width: 480, height: 480, crop: 'center' | image_tag: loading: 'lazy', alt: card_img_alt }}
```

The `height: 480, crop: 'center'` parameters instruct the Shopify CDN to serve a pre-cropped 480×480 image, offloading crop work from the browser and ensuring all cards receive identically-sized images.

**Expected behavior change:** Cards will be square instead of rectangular. Product photos will display without top/bottom clipping. Chair headrests and caster bases will be fully visible. The 4-column grid will appear taller per row — a minor visual shift balanced by better product legibility.

---

## Alternative (if portrait spec must be honored)

Use Option A (4:5) if the image pipeline is producing portrait images at scale:

```css
.ds-cs__card-img { aspect-ratio: 4/5; }
```
```liquid
{{ product.featured_media | image_url: width: 480, height: 600, crop: 'center' | image_tag: ... }}
```

This will side-clip existing 1:1 stock photos (20% each side) but is spec-correct for new portrait images.

---

## Decision required

Before writing the fix in 3.2b: confirm whether to use **1:1 square** (fits current catalog) or **4:5 portrait** (matches component spec, fits future pipeline images).
