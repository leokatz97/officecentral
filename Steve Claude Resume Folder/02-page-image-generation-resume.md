# RESUME SESSION — BBI Page Image Generation (generate-page-images.py)

**Project path:** `/Users/leokatz/Desktop/Office Central/`
**Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` already in `.env`

---

## Current State

### Script: REBUILT AND READY ✅
`scripts/generate-page-images.py` was fully rebuilt from scratch (837 lines).

**Verified via dry-run:**
- 60 slots across 22 pages
- 13 SKIPPED_OCI slots (real photos cover those pages)
- 47 actual generates
- Estimated cost: $1.03–$1.32 at flux/dev

### Generation: NOT STARTED YET
No images have been generated. The script is ready to run.

---

## What the Script Does

Generates hero images, hub tiles, featured cards, and section breaks for every BBI landing page using fal.ai flux/dev (28 inference steps, ~$0.025/image).

**6 slot types:**
- `hero-product.jpg` — top SKU on white studio background (landscape_16_9)
- `hero-space.jpg` — full room scene for page ICP (landscape_16_9)
- `hub-tile.jpg` — square tile for collection/industry/brand overview pages (square)
- `featured-card-*.jpg` — homepage featured product cards (landscape_4_3)
- `section-*.jpg` — mid-page service section breaks (landscape_16_9)

**Output:** `data/page-images/{page-slug}/{filename}.jpg`

**OCI coverage (skip these — real photos already exist):**
Pages: homepage/hero-space, collaboration/hero-space, acoustic-pods/hero-space, healthcare, education, government (hero-space + hub-tile), design-services/hero-space, task-seating/hub-tile, collaboration/hub-tile, acoustic-pods/hub-tile.

---

## Steps to Complete

1. **Smoke test (3 generates):**
   ```bash
   cd /Users/leokatz/Desktop/Office\ Central
   echo "YES" | python3 scripts/generate-page-images.py --limit=3 --live
   ```
   Inspect `data/page-images/`. Confirm: one image generated, OCI slots show SKIPPED_OCI, manifest and audit log written.

2. **Review quality** — check the 3 generated images before committing to full run.

3. **Full run (~20 min, ~$1.03–$1.32):**
   ```bash
   echo "YES" | python3 scripts/generate-page-images.py --live
   ```

4. **Check manifest:** `data/reports/generated-page-images-YYYY-MM-DD.csv`

5. **Update bbi-build-page skill** — already done in previous session:
   - Photo library block updated to new slot naming
   - Step 3 pre-check updated
   - Claude Design prompt template updated with [IF IMAGES ATTACHED] block

6. **Run git-sync skill** to commit and close session.

---

## Model & Budget

| Model | Endpoint | Steps | ~$/image |
|---|---|---|---|
| flux/dev | fal-ai/flux/dev | 28 | ~$0.025 ✅ |

- Endpoint: `POST https://fal.run/fal-ai/flux/dev`
- Body: `{"prompt": "...", "image_size": "...", "num_inference_steps": 28, "num_images": 1}`
- Auth: `Authorization: Key {FAL_KEY}`
- Cost guard: warns and requires YES if estimated cost > $2.00
- Cost constants: $0.022 low / $0.028 high per image

---

## Script Features

- Python stdlib only — no pip installs
- `--live` to generate, `--limit=N` to test N images, dry-run by default
- Resume-safe: skips if file already exists (SKIPPED_EXISTS)
- OCI slots: SKIPPED_OCI with OCI filename recorded in manifest
- Manifest: `data/reports/generated-page-images-YYYY-MM-DD.csv`
  - Columns: `Page, Slot, Filename, Image_Size, Source, FAL_URL, Local_Path, Prompt, Status`
- Audit log: `data/logs/page-image-generation-YYYYMMDD-HHMMSS.json`
- Max retries: 3 with exponential backoff

---

## Key Files

| File | Purpose |
|---|---|
| `scripts/generate-page-images.py` | Main script (fully rebuilt, 837 lines) |
| `data/page-images/` | Output folder (empty — not generated yet) |
| `data/reports/generated-page-images-*.csv` | Manifest (written after run) |
| `.claude/skills/bbi-build-page/SKILL.md` | Already updated with page-image library refs |
| `docs/plan/ideas-backlog.md` item #8 | Canonical slot and folder definitions |

---

## Backlog Refs

- `docs/plan/ideas-backlog.md` items #8, #9, #10
- Pattern ref: `scripts/generate-product-images.py`
