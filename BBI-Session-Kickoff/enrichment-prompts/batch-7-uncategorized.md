# PE Pass 2 — Batch 7: Uncategorized
# 13 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 7 — Uncategorized (13 products)
CHECKPOINT FILE: data/reports/pe-pass2-checkpoint.json
OUTPUT FILE:     data/reports/pe-pass2-output.json
PRODUCTS FILE:   data/reports/pe-pass2-products.json
BATCH FILE:      data/reports/pe-pass2-batches.json

READ THESE FIRST (in order):
  1. BBI-Session-Kickoff/01-safety-preflight.md
  2. BBI-Session-Kickoff/enrichment-prompts/MASTER-INSTRUCTIONS.md
  3. data/reports/pe-pass2-checkpoint.json  (skip already-completed handles)
  4. data/reports/pe-pass2-products.json    (pre-filled data for each product)
  5. docs/strategy/icp.md                  (voice + audience rules)
  6. docs/strategy/voice-samples.md        (approved copy reference)

BATCH HANDLES (13 products, work through in this order):
   1. installation475
   2. part-time-armless-task-chair-mvl2836
   3. shoptech-097-pc1000
   4. shoptech-2302-pc775
   5. shoptech-2500-pc550
   6. carpeted-floor-48-x-36-6
   7. carpeted-floor-48-x-60
   8. carpeted-floor-48-x-60-1
   9. delivery-charge-175-00
  10. delivery-charge-85-00
  11. newland-16w-box-box-file-mobile-pedestal
  12. shoptech-081
  13. shoptech-2300-pc775

SESSION RULES:
  - Work through handles IN ORDER. Skip any already in checkpoint["completed"].
  - For each product:
      1. Load its data from pe-pass2-products.json
      2. Web-search the product code + vendor name to find real specs
         (e.g. search "MVL2748 Global Furniture chair specs")
      3. Show the product card (see MASTER-INSTRUCTIONS.md for format)
      4. Wait for Steve's input: yes / skip / edit / other
      5. Write decision to checkpoint immediately after input
      6. If "edit": take Steve's raw notes, write full 3-section description
         (About This Product → Key Features → Who It's For) in Hero 100 style,
         fill spec fields from notes + web research, show to Steve for confirm
      7. Write finalised output to pe-pass2-output.json
      8. Move to next product
  - After every 10 products: git add + git commit the checkpoint + output files
  - At end of batch (or if Steve types "done"): final commit + summary report

DESCRIPTION FORMAT (always follow this — matches Hero 100 PE-1):
  <p><strong>[Bold hook — one sentence, use-case or promise, no "Elevate".]</strong></p>
  <p>[2–3 sentences: what it does, who it's built for, Ontario institutional context.]</p>
  <h3>Key features</h3>
  <ul><li>...</li><li>...</li><li>...</li></ul>
  <h3>Who it's for</h3>
  <p>[Specific Ontario buyer type — schools, hospitals, municipalities, corporate.]</p>
  <p>Available from Brant Business Interiors — Canada's OECM-eligible commercial
  furniture supplier since 1964. Delivery across Canada; installation available in Ontario and Western Canada.
  Call <strong>1-800-835-9565</strong> for current pricing, lead times, or volume quotes.</p>

VOICE RULES (from icp.md):
  - Bold hook as opener — confident, not lifestyle ("keeps your back where it should be" ✓,
    "elevate your workday" ✗)
  - Never commit to specific lead times — use "ships from Ontario stock" or push to phone
  - Phone CTA on every product: 1-800-835-9565
  - OECM is a trust signal — surface it on institutional-leaning products (procurement vehicle for Ontario buyers only; quality benchmark mention acceptable for all buyers)
  - Never write "BBI" — always "Brant Business Interiors"

OUTPUT JSON FORMAT (write to pe-pass2-output.json after each product):
  products["handle"] = {
    "action": "yes|skip|edit|other",
    "batch": "Batch 7",
    "draft_vendor": "...",
    "draft_meta_title": "...",
    "draft_meta_desc": "...",
    "draft_body_html": "...",
    "specs": {
      "manufacturer": "...",
      "product_line": "...",
      "model_codes": "...",
      "dimensions": "...",
      "weight": "...",
      "weight_capacity": "...",
      "materials": "...",
      "finishes_available": "...",
      "key_features": ["...", "..."],
      "certifications": "...",
      "warranty": "...",
      "country_of_manufacture": "..."
    },
    "steve_notes": "...",
    "timestamp": "..."
  }

CHECKPOINT FORMAT (write to pe-pass2-checkpoint.json after each product):
  completed["handle"] = {
    "action": "yes|skip|edit|other",
    "batch": "Batch 7",
    "timestamp": "..."
  }

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (13 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| installation475                               |                | A    | $  475.00 |
| part-time-armless-task-chair-mvl2836          |                | B    | $  249.99 |
| shoptech-097-pc1000                           | PC1000         | B    | $  394.00 |
| shoptech-2302-pc775                           | PC775          | B    | $  363.00 |
| shoptech-2500-pc550                           | PC550          | B    | $  299.99 |
| carpeted-floor-48-x-36-6                      |                | C    | $   89.99 |
| carpeted-floor-48-x-60                        |                | C    | $  139.99 |
| carpeted-floor-48-x-60-1                      |                | C    | $  139.99 |
| delivery-charge-175-00                        |                | C    | $  175.00 |
| delivery-charge-85-00                         |                | C    | $   85.00 |
| newland-16w-box-box-file-mobile-pedestal      |                | C    | $  589.99 |
| shoptech-081                                  |                | C    | $  335.00 |
| shoptech-2300-pc775                           | PC775          | C    | $  369.00 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: ALL DONE — run PE-PASS-3**
