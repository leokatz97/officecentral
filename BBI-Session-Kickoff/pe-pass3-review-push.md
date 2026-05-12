# PE Pass 3 — Review Excel + Push to Shopify

**Paste this into a fresh Claude session. It is fully self-contained.**

---

## Context

You are working on the BBI (Brant Business Interiors) Shopify project.
- **Project root:** `/Users/leokatz/Desktop/Office Central`
- **Dev theme:** `186373570873` (BBI Landing Dev) — all pushes go here only
- **Live theme:** `178274435385` — never touch this

Product enrichment Pass 2 (PE-2) is now complete. All 7 batches of enrichment descriptions have been written into `data/reports/pe-pass2-output.json` by Claude research sessions. This session does three things in sequence:

1. **Generate a review Excel** — one row per enriched product so Steve can scan and approve
2. **Dry-run the push** — confirm diff counts look right before touching Shopify
3. **Live push** — push approved products' descriptions + specs to Shopify

---

## Hard rules (apply every action, no exceptions)

- Never push to live theme `178274435385`
- Always dry-run scripts before `--live`
- Never delete products — archive or unpublish only
- Never commit `.env`

---

## Step 1 — Verify input data

First, confirm the output file is complete:

```bash
python3 -c "
import json
with open('data/reports/pe-pass2-output.json') as f:
    d = json.load(f)
prods = d.get('products', {})
batches = {}
for h,v in prods.items():
    b = v.get('batch','?')
    batches[b] = batches.get(b,0) + 1
print(f'Total: {len(prods)} products')
for b in sorted(batches):
    print(f'  {b}: {batches[b]}')
"
```

Expected: 157 products across 7 batches. If any batch is 0, stop and tell Steve which batch is missing.

---

## Step 2 — Generate the review Excel

**Script to create:** `scripts/generate-pe3-review.py`

This script reads `data/reports/pe-pass2-output.json` and writes a new Excel file:
`data/reports/pe-pass3-review-YYYYMMDD.xlsx`

### Excel structure — 3 sheets (match the v2 format exactly)

**Sheet 1: Instructions**
Simple text guide for Steve:
- Column A, rows 1-8: plain text instructions
- "Fill `steve_approve` with YES or NO (or leave blank = YES)"
- "Fill `steve_notes` if you want a correction logged"
- "Any row with steve_approve = NO is excluded from the push"
- "Save the file, then run: python3 scripts/push-pe3-enrichment.py --live"

**Sheet 2: Enrichment**
One row per product. Columns (match existing `pe-pass2-enrichment-v2-2026-05-11.xlsx` Enrichment sheet exactly):

| Column | Source | Notes |
|---|---|---|
| `handle` | `pe-pass2-output.json` key | |
| `batch` | `v['batch']` | NEW — add this to make batch visible |
| `draft_vendor` | `v['draft_vendor']` | |
| `draft_meta_title` | `v['draft_meta_title']` | |
| `draft_meta_title_chars` | `len(v['draft_meta_title'])` | Flag >60 in orange |
| `draft_meta_desc` | `v['draft_meta_desc']` | |
| `draft_meta_desc_chars` | `len(v['draft_meta_desc'])` | Flag >160 in orange |
| `draft_body_html` | `v['draft_body_html']` truncated to 500 chars + "…" | Full HTML is long — truncate for readability |
| `steve_notes` | `v.get('steve_notes','')` | Pre-fill from enrichment session notes |
| `steve_approve` | blank | Steve fills YES/NO; blank = YES |

Row height: 60px. Freeze row 1. Auto-filter on.
Flag meta_title_chars > 60 orange. Flag meta_desc_chars > 160 orange.

**Sheet 3: Specs (Draft)**
One row per product. Columns (match existing `pe-pass2-enrichment-v2-2026-05-11.xlsx` Specs sheet):

| Column | Source |
|---|---|
| `handle` | key |
| `batch` | `v['batch']` |
| `draft_vendor` | `v['draft_vendor']` |
| `draft_manufacturer` | `v['specs'].get('manufacturer','')` |
| `draft_product_line` | `v['specs'].get('product_line','')` |
| `draft_model_codes` | `', '.join(v['specs'].get('model_codes',[]))` |
| `draft_dimensions` | `v['specs'].get('dimensions','')` |
| `draft_weight` | `v['specs'].get('weight','')` |
| `draft_weight_capacity` | `v['specs'].get('weight_capacity','')` |
| `draft_materials` | `v['specs'].get('materials','')` |
| `draft_finishes_available` | `', '.join(v['specs'].get('finishes_available',[]))` |
| `draft_key_features` | `' | '.join(v['specs'].get('key_features',[]))` |
| `draft_certifications` | `', '.join(v['specs'].get('certifications',[]))` |
| `draft_warranty` | `v['specs'].get('warranty','')` |
| `draft_country_of_manufacture` | `v['specs'].get('country_of_manufacture','')` |
| `steve_approve` | blank |
| `steve_notes` | blank |

Use `openpyxl`. Output file: `data/reports/pe-pass3-review-{date}.xlsx`.

After writing, print: `✅ Review Excel written: data/reports/pe-pass3-review-{date}.xlsx — open in Excel/Numbers to review.`

---

## Step 3 — Dry-run the push

After the Excel is written, run:

```bash
python3 scripts/push-pe3-enrichment.py 2>&1 | head -40
```

(No `--live` flag = dry-run mode.) Confirm:
- Products count matches what's in the output JSON
- A few sample diffs look correct (real descriptions, not empty)
- No errors

Report the summary line (Done: X OK · Y FAIL) to Steve.

---

## Step 4 — Wait for Steve's Excel review

Tell Steve:
> "Review Excel is at `data/reports/pe-pass3-review-{date}.xlsx`. Mark any rows NO in `steve_approve` to exclude from push. When done, come back and say **ready to push**."

**Do not proceed to Step 5 until Steve says "ready to push".**

---

## Step 5 — Live push

When Steve confirms, check whether `push-pe3-enrichment.py` supports a `steve_approve` filter from the Excel. If it does not yet support reading the Excel approval column, add that feature first:

**Add Excel-gated push to `scripts/push-pe3-enrichment.py`:**

Add a `--review-file` flag:
```
python3 scripts/push-pe3-enrichment.py --live --review-file data/reports/pe-pass3-review-YYYYMMDD.xlsx
```

When `--review-file` is passed:
- Load the Enrichment sheet
- Build a set of handles where `steve_approve` is empty (treat as YES) or explicitly "YES" (case-insensitive)
- Skip any handle where `steve_approve` is "NO"
- Log skipped handles at the top of the output

If Steve did not fill in any approvals (all blank), the filter is a no-op and all records push.

Then run:
```bash
python3 scripts/push-pe3-enrichment.py --live --review-file data/reports/pe-pass3-review-YYYYMMDD.xlsx
```

Confirm: `Done: X OK · 0 FAIL`. Save the log path.

---

## Step 6 — Update build state

Edit `BBI-Session-Kickoff/bbi-build-state.md`:

Find the `PE-PASS-3` row and update:
- Status: ✅
- Evidence: log file path + count
- Notes: "All 7 batches enriched + pushed. Remaining enrichment work is Phase 1b (503 non-Hero, non-enrichment-157 products — post-launch backlog)."

Commit:
```bash
git add BBI-Session-Kickoff/bbi-build-state.md data/reports/pe-pass3-review-*.xlsx scripts/push-pe3-enrichment.py scripts/generate-pe3-review.py
git commit -m "PE-PASS-3 complete: 157 enrichment products pushed to Shopify"
```

---

## Step 7 — Tell Steve what's next

After the push, report:

```
✅ PE-PASS-3 complete — [X] products pushed to Shopify (descriptions + specs + vendor).

Remaining open items before launch:
  🔴 LEAD-INBOX-1 — provision quotes@, design@, info@brantbusinessinteriors.com
                    (hard prereq for quote modal routing + auto-replies)
  🟡 Wave E — AI-7 entity copy on homepage, AI-8 OECM page hardening,
               AI-9 FAQ blocks on category pages, SEO-AUDIT-1 (hard gate)
  🟡 CONTENT-1 — logo decision: lock bbi-logo-v2 or source true BBI wordmark
  🟡 Wave D — W0-1 GSC+GA4, W0-2 Google Business Profile, W0-6 backlinks

Full status: BBI-Session-Kickoff/bbi-build-state.md
```
