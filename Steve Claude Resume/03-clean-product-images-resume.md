# RESUME: BBI Clean Product Image Generation (216 products × 3 images)

**Project path:** `/Users/leokatz/Desktop/Office Central/`
**Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` already in `.env`

---

## What This Is

The product image pipeline (Session 1) already generated and pushed 3 AI images for **330 products that had only 1 image**. This session does the same thing for the **216 "Clean" products** — those with no quality flags and already having multiple images — adding 3 more AI-generated images (positions after their existing ones).

**Source of the 216 handles:** The `PRODUCTS` JSON array embedded in `previews/Product-enrichment.html`. Filter: `pub === true` AND `fl.length === 0`. Every product in this set already has `imgs > 1`.

---

## Status: NOT STARTED — Build Script First

`scripts/generate-clean-product-images.py` does **not exist yet**. Build it from scratch.

---

## Step 1: Extract the 216 Handles

Parse `previews/Product-enrichment.html` — find the `const PRODUCTS = [...]` array and extract all handles where `pub === true` AND `fl.length === 0`. Write them to `data/reports/clean-products-handles.json` as a simple list of handle strings. There should be exactly 216.

---

## Step 2: Build `scripts/generate-clean-product-images.py`

**Follow `scripts/generate-product-images.py` exactly for all patterns:**
- Python stdlib only — `urllib`, `json`, `csv`, `os`, `sys`, `time` — no pip installs
- Credentials from `.env`: `FAL_KEY` already set
- fal.ai endpoint: `POST https://fal.run/fal-ai/flux/schnell`
- Body: `{"prompt": "...", "image_size": "landscape_4_3", "num_inference_steps": 4, "num_images": 1}`
- `--live` to generate, `--limit=N` to test N products, dry run default
- Resume-safe: skip if output file already exists (SKIPPED_EXISTS)
- Cost guard: warn and require YES if estimated cost > $2.00
- Cost constants: $0.003 low / $0.004 high per image
- Manifest CSV → `data/reports/generated-clean-images-YYYY-MM-DD.csv`
  Columns: `Handle, Title, Position, Filename, FAL_URL, Local_Path, Prompt, Status`
  (Status = GENERATED | SKIPPED_EXISTS | DRY_RUN | ERROR)
- Audit log → `data/logs/clean-image-generation-YYYYMMDD-HHMMSS.json`
- Max retries: 3 with exponential backoff; non-retryable on 400/401/403

**Source products:** Read from `data/reports/clean-products-handles.json` (the 216 handles extracted in Step 1). For each handle, look up the product title from the enrichment HTML PRODUCTS array (needed for prompt generation).

### 3 Image Styles Per Product (same as Session 1):
- **gen-2** → `data/generated-clean-images/{handle}-gen-2.jpg` — white studio shot
  Prompt: `"Professional product photography of [product title] on a clean white studio background, crisp even lighting, slight drop shadow, commercial catalogue style. No people, no text overlays."`
- **gen-3** → `data/generated-clean-images/{handle}-gen-3.jpg` — office environment
  Prompt: `"[product title] in a bright modern Canadian open-plan office environment, warm natural window light, contemporary neutral decor. No people, no text overlays."`
- **gen-4** → `data/generated-clean-images/{handle}-gen-4.jpg` — close-up detail
  Prompt: `"Close-up detail shot of [product title], shallow depth of field, editorial style, studio lighting, emphasis on material texture and craftsmanship. No people, no text overlays."`

**Output folder:** `data/generated-clean-images/` (separate from `data/generated-images/` used by Session 1)

### Budget:
216 products × 3 images = 648 images × ~$0.003 = **~$1.94 est.** — just under $2 limit.
Set cost guard at $2.00.

---

## Step 3: Smoke Test (3 products)
```bash
python3 scripts/generate-clean-product-images.py --limit=3 --live
```
Check `data/generated-clean-images/`. Confirm 9 JPEGs (3 products × 3 styles), manifest written.

---

## Step 4: Full Generation Run (~20 min)
```bash
echo "YES" | python3 scripts/generate-clean-product-images.py --live
```
**Resume-safe** — if it crashes, re-run and it skips already-generated files.

---

## Step 5: Push to Shopify (within 24h of generation — fal.ai URLs expire)
```bash
echo "YES" | python3 scripts/push-generated-images.py --manifest=data/reports/generated-clean-images-YYYY-MM-DD.csv --live
```
`push-generated-images.py` already supports `--manifest` to point at a different CSV. It will push gen-2/gen-3/gen-4 images to positions **after** the product's existing images (Shopify appends new images).

**Note:** The push script has socket-timeout retry logic and resume safety — re-running skips already-pushed `(handle, position)` pairs.

---

## Step 6: Spot-Check
Open 3–5 products in [Shopify Admin](https://admin.shopify.com/store/office-central-online/products) and confirm new images appear after the existing ones with correct alt text.

**Then run `git-sync` skill to commit and close.**

---

## Key Files
- Handles list (to extract): `previews/Product-enrichment.html` → `const PRODUCTS = [...]`
- Output handles JSON: `data/reports/clean-products-handles.json` (create in Step 1)
- New script: `scripts/generate-clean-product-images.py` (create in Step 2)
- Push script (reuse): `scripts/push-generated-images.py`
- Pattern reference: `scripts/generate-product-images.py`
- Session 1 manifest (for reference): `data/reports/generated-images-2026-04-24.csv`
