# PE Pass 2 — Batch 4: Desks & Tables — Part 1 of 2
# 27 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 4 — Desks & Tables — Part 1 of 2 (27 products)
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

BATCH HANDLES (27 products, work through in this order):
   1. desk-shell-5-sizes
   2. desk-single-pedestal
   3. desk-single-pedestal-1
   4. electric-dual-monitor-height-adjustable-standing-desk-workstation-dc450
   5. innovations-l-shape-desk-with-hutch
   6. innovations-suite
   7. innovations-u-shape-suite
   8. l-shape-desk-set-72x72
   9. offices-to-go-newland-u-shaped-suites-nlp406
  10. sit-stand-adjustable-desk-riser-32-wide
  11. sit-stand-fellowes-lotus-dual-arm-not-included
  12. u-shaped-suite-with-rectangular-island
  13. zira-workstation-3-person
  14. desk-top-dividers
  15. l-shape-desk-with-36h-privacy-panel-1
  16. management-u-shaped-suite-72w-x-102d
  17. single-pedestal-desk-nlp232
  18. coffee-table-1
  19. folding-table-24-x-48-1
  20. folding-table-36-bt36-resin
  21. freefit-benching-height-adjustable-176w-x-62-5d-ffhab506-2
  22. hdl-5-resin-folding-table-granite-rectangle-dove-white-pebble-top-powder-coated-base-60-table-top-length-x-30-table-top-width-29-height-1
  23. management-u-shaped-suite-with-3-stage-height-adjustable-table-nlp410
  24. offices-to-go-ionic-table-36-x-36-x-29-material-metal-base-finish-absolute-acajou-black-base-sandtex-1
  25. round-table-42
  26. zira-conference-table-9-sizes
  27. coffee-table

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
    "batch": "Batch 4",
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
    "batch": "Batch 4",
    "timestamp": "..."
  }

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (27 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| desk-shell-5-sizes                            |                | A    | $  429.99 |
| desk-single-pedestal                          |                | A    | $  699.99 |
| desk-single-pedestal-1                        |                | A    | $  949.99 |
| electric-dual-monitor-height-adjustable-stand | DC450          | A    | $  749.99 |
| innovations-l-shape-desk-with-hutch           |                | A    | $ 1699.99 |
| innovations-suite                             |                | A    | $ 4175.00 |
| innovations-u-shape-suite                     |                | A    | $ 3299.99 |
| l-shape-desk-set-72x72                        |                | A    | $ 1499.99 |
| offices-to-go-newland-u-shaped-suites-nlp406  | NLP406         | A    | $ 2369.99 |
| sit-stand-adjustable-desk-riser-32-wide       |                | A    | $  399.99 |
| sit-stand-fellowes-lotus-dual-arm-not-include |                | A    | $  672.99 |
| u-shaped-suite-with-rectangular-island        | NLP324         | A    | $ 1956.67 |
| zira-workstation-3-person                     |                | A    | $ 8779.99 |
| desk-top-dividers                             |                | C    | $  199.99 |
| l-shape-desk-with-36h-privacy-panel-1         |                | C    | $ 4199.99 |
| management-u-shaped-suite-72w-x-102d          |                | C    | $ 1944.00 |
| single-pedestal-desk-nlp232                   | NLP232         | C    | $  799.99 |
| coffee-table-1                                |                | A    | $  359.99 |
| folding-table-24-x-48-1                       |                | A    | $  125.29 |
| folding-table-36-bt36-resin                   |                | A    | $  149.99 |
| freefit-benching-height-adjustable-176w-x-62- | FFHAB506       | A    | $13333.00 |
| hdl-5-resin-folding-table-granite-rectangle-d |                | A    | $  143.87 |
| management-u-shaped-suite-with-3-stage-height | NLP410         | A    | $ 2769.99 |
| offices-to-go-ionic-table-36-x-36-x-29-materi |                | A    | $  379.99 |
| round-table-42                                |                | A    | $  449.00 |
| zira-conference-table-9-sizes                 |                | A    | $ 2499.00 |
| coffee-table                                  |                | C    | $  399.99 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: Batch 5**
