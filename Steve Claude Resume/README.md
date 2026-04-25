# Steve Claude Resume Prompts

Paste the contents of one of these files into a new Claude session when you run out of tokens.
Each file is self-contained — no prior context needed.

| File | What It Covers | Status |
|---|---|---|
| `01-product-image-pipeline-resume.md` | 330 products × 3 AI images — generate + push to Shopify | ✅ COMPLETE — spot-check only |
| `02-page-image-generation-resume.md` | Page-level hero/tile/section images (47 generates, all 6 slot types) | 🔜 Smoke test + full run pending |
| `03-clean-product-images-resume.md` | 216 "Clean" products × 3 AI images — build script + generate + push | 🔜 Not started — build script first |

## Order of Operations
1. `02` — Run page image smoke test + full run (quick, ~$1.30, ~20 min)
2. `03` — Build clean product script, generate 648 images (~$1.94, ~20 min), push to Shopify

## Project Details
- **Store:** brantbusinessinteriors.com
- **Admin:** https://admin.shopify.com/store/office-central-online
- **Project path:** `/Users/leokatz/Desktop/Office Central/`
- **Credentials:** `FAL_KEY` and `SHOPIFY_TOKEN` in `.env` at project root
