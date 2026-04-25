# RESUME SESSION — BBI Product Image Push (3 AI images per product)

**Project path:** `/Users/leokatz/Desktop/Office Central/`
**Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` already in `.env`

---

## Current State

### Generation: COMPLETE ✅
- **974 images** generated across **330 products** (flux/schnell, 3 styles each)
- Files: `data/generated-images/{handle}-gen-2.jpg`, `gen-3.jpg`, `gen-4.jpg`
- Manifest: `data/reports/generated-images-2026-04-24.csv`
- Cost: ~$2.92–$5.84

**3 image styles:**
- `gen-2` — clean white studio shot (catalogue style) → Shopify position 2
- `gen-3` — product in a bright modern Canadian office → Shopify position 3
- `gen-4` — close-up detail/texture shot (editorial, shallow DoF) → Shopify position 4

### Push: COMPLETE ✅ (but with duplicates — see below)
- **974 images pushed** to Shopify, 0 errors, 0 not found
- Push log: `data/reports/shopify-images-pushed-2026-04-25.csv`
- Audit log: `data/logs/push-images-20260425-121836.json`

### ⚠️ Duplicate Images — Action Required
The push script crashed mid-run on the first attempt (socket timeout at product 116/325) before it could write the results CSV. When it was restarted, the resume logic had nothing to skip, so it pushed all 974 images again.

**Result:** ~115 products now have 6 AI images instead of 3 (positions 2–7 instead of 2–4).

**Fix needed:** Build `scripts/dedup-product-images.py` that:
1. Reads each product's images from the Shopify API
2. For any product with more than 4 images total (1 original + 3 AI), deletes the extras
3. Keeps images at positions 1–4, deletes positions 5+
4. Dry-run by default, `--live` to actually delete
5. Log deletions to `data/logs/dedup-images-YYYYMMDD-HHMMSS.json`

Use the same stdlib-only pattern as `scripts/push-generated-images.py` (urllib, no pip installs).

Shopify delete endpoint: `DELETE /admin/api/2026-04/products/{product_id}/images/{image_id}.json`
Shopify list images: `GET /admin/api/2026-04/products/{product_id}/images.json`

The 330 product handles are in `data/reports/generated-images-2026-04-24.csv`.

---

## Steps to Complete

1. **Build** `scripts/dedup-product-images.py` (see spec above)
2. **Dry-run** to confirm what would be deleted: `python3 scripts/dedup-product-images.py`
3. **Live run** to delete duplicates: `python3 scripts/dedup-product-images.py --live`
4. **Spot-check** 3–5 products in Shopify Admin — each should have exactly 4 images:
   - Position 1: original product photo
   - Position 2: gen-2 white studio
   - Position 3: gen-3 office setting
   - Position 4: gen-4 close-up detail
5. **Run git-sync skill** to commit and close session

---

## Key Files

| File | Purpose |
|---|---|
| `scripts/generate-product-images.py` | Generates AI images via fal.ai flux/schnell |
| `scripts/push-generated-images.py` | Pushes to Shopify (has retry + resume logic) |
| `data/reports/generated-images-2026-04-24.csv` | Generation manifest (330 products, 974 rows) |
| `data/reports/shopify-images-pushed-2026-04-25.csv` | Push results (all PUSHED) |
| `data/generated-images/` | 989 local JPEGs |

---

## Script Improvements Made This Session (already in files)

`push-generated-images.py` was updated to:
- Retry socket timeouts up to 3× with 5/10/15s backoff
- Resume-safe: reads today's push CSV, skips already-PUSHED (handle, position) pairs
- Appends to today's CSV across retries (never overwrites)
