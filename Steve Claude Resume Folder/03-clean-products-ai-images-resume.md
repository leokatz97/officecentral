# RESUME SESSION — BBI AI Images for Clean Products (216 products)

**Project path:** `/Users/leokatz/Desktop/Office Central/`
**Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` already in `.env`

---

## What This Session Is

The product image pipeline (session 01) added 3 AI images to **330 products that had only 1 image**.

This session adds the same 3 AI images to the **216 "clean" products** — products that already have multiple real images but no AI supplemental shots.

"Clean" = no enrichment flags (complete title, description, SEO, SKU, and multiple images). These are the store's best-content products; adding AI images gives them the same 3-angle coverage.

**Target: 216 products × 3 images = 648 images. Est. cost ~$1.94–$3.89.**

---

## How to Identify the 216 Products

Run this Python snippet to extract their handles from the product export:

```python
import csv

# Load the Shopify export
export_path = 'data/exports/products-export-2026-04-21.csv'

# Load handles already processed in session 01
already_done_path = 'data/reports/generated-images-2026-04-24.csv'

with open(already_done_path) as f:
    done_handles = {row['Handle'] for row in csv.DictReader(f)}

# The 216 clean products are all published products with >1 image NOT in the done set
from collections import defaultdict
products = defaultdict(list)
with open(export_path) as f:
    for row in csv.DictReader(f):
        if row.get('Status', '').lower() == 'active':
            products[row['Handle']].append(row)

clean_handles = [h for h, rows in products.items()
                 if len(rows) > 1 and h not in done_handles]
print(f'Clean products: {len(clean_handles)}')

# Write to a handles file
with open('data/reports/clean-product-handles.txt', 'w') as f:
    f.write('\n'.join(clean_handles))
```

Alternatively, the 216 handles can be identified from `previews/Product-enrichment.html` — they are the products with `fl:[]` (no flags) which all happen to have >1 image.

---

## Script Plan

**Option A — Reuse `generate-product-images.py` with a `--handles-file` flag:**

Add a `--handles-file=PATH` argument to `scripts/generate-product-images.py` that reads a list of handles (one per line) instead of filtering by image count from the export CSV. Everything else (prompts, styles, cost guard, manifest, resume logic) stays identical.

Then run:
```bash
# Generate handles file first (see snippet above)
python3 scripts/generate-product-images.py --handles-file=data/reports/clean-product-handles.txt --live
```

**Option B — Copy and adapt the script as `generate-clean-product-images.py`:**

Simpler if you want a clean audit trail separate from session 01.

---

## 3 Image Styles (same as session 01)

| Style | Shopify Position | Description |
|---|---|---|
| gen-2 | Next available (e.g. position N+1) | Clean white studio shot (catalogue style) |
| gen-3 | N+2 | Product in a bright modern Canadian office |
| gen-4 | N+3 | Close-up detail/texture (editorial, shallow DoF) |

Prompts are auto-generated from the product title — same logic as `generate-product-images.py`. No manual prompt writing needed.

**Important:** These products already have images at positions 1–N. The new AI images should be pushed at positions after the existing ones. Confirm the push script handles this correctly (it uses explicit position numbers — may need to fetch existing image count first and offset).

---

## Steps to Complete

1. **Extract the 216 handles** using the snippet above → `data/reports/clean-product-handles.txt`

2. **Add `--handles-file` flag** to `scripts/generate-product-images.py`:
   - In `parse_args()`: add `--handles-file=` parsing
   - In `main()`: if handles-file provided, load those handles instead of filtering export CSV by 1-image count
   - Everything else stays identical

3. **Smoke test (5 products):**
   ```bash
   echo "YES" | python3 scripts/generate-product-images.py \
     --handles-file=data/reports/clean-product-handles.txt \
     --limit=5 --live
   ```

4. **Confirm position handling** — verify images land AFTER existing images, not replacing them.

5. **Full generation run:**
   ```bash
   echo "YES" | python3 scripts/generate-product-images.py \
     --handles-file=data/reports/clean-product-handles.txt --live
   ```
   (~15–20 min, est. $1.94–$3.89)

6. **Push to Shopify** (fal.ai URLs expire in ~24h):
   ```bash
   echo "YES" | python3 scripts/push-generated-images.py --live
   ```
   The push script is resume-safe and retries socket timeouts automatically.

7. **Spot-check** 3–5 products in Shopify Admin — confirm new images appended correctly.

8. **Run git-sync skill** to commit and close session.

---

## Key Files

| File | Purpose |
|---|---|
| `scripts/generate-product-images.py` | Modify to add `--handles-file` flag |
| `scripts/push-generated-images.py` | Push script (already has retry + resume) |
| `data/exports/products-export-2026-04-21.csv` | Full Shopify product export |
| `data/reports/generated-images-2026-04-24.csv` | Session 01 manifest (handles to exclude) |
| `data/reports/clean-product-handles.txt` | Generate this first (216 handles) |
| `previews/Product-enrichment.html` | Source of truth for "clean" product definition |

---

## Context

- Session 01 (product push): 330 one-image products → AI images added, push complete
- This session: 216 clean/multi-image products → same AI images appended
- After both: every published BBI product has at least 4 images (1 original + 3 AI angles)
