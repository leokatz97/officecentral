# PE Pass 2 — Batch 1: Chairs — Part 1 of 3
# 26 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 1 — Chairs — Part 1 of 3 (26 products)
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

BATCH HANDLES (26 products, work through in this order):
   1. adapt-high-back-synchro-tilter-mvl11724
   2. amigo-mesh-chair-otg10900blk
   3. armless-low-back-stacking-chair-mvl2748
   4. ashmont-medium-back-management-tilter-mvl2781
   5. avro-350m-heavy-duty-multi-tilter-chairs-mvl11716
   6. basics-chevron-junior-operator-chair-mvl2363-7-1
   7. basics-comfort-time-ultra-multi-tilter-big-tall-chair
   8. basics-ergo-boss-executie-back-multi-tilter-chairs-bao28703
   9. basics-obusforme-elite-heavy-duty-multi-tilter-chair-ts2770-3-1
  10. basics-preto-swivel-tilt-chair-1
  11. beta-armless-posture-task-drafting-stool-mvl2718
  12. bolt-mesh-back-tilter-otg11510b
  13. chair-black-steel-frame-3
  14. cobalt-medium-back-tilter-mvl2785
  15. drift-seating
  16. elora-multi-tilter-high-back-chair-black-baomvl1893
  17. extended-high-back-tilter-otg11359-carleton
  18. extended-high-back-wide-deep-seat-multi-tilt-bao27513
  19. finch-armless-stacking-armchair-mvl11704
  20. format-high-back-weight-sensing-synchro-tilter-mesh-seat-and-back-mvl3197-copy
  21. full-time-chair-mvl2900
  22. global-accord-back-knee-tilter-chair-1
  23. global-accord-mesh-back-tilter
  24. global-obusforme-elite-multi-tilter-chair-high-back
  25. ibex-drafting-task-stool-mvl2808
  26. ibex-mesh-back-drafting-stool-task-chair-with-arms

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
    "batch": "Batch 1",
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
    "batch": "Batch 1",
    "timestamp": "..."
  }

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (26 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| adapt-high-back-synchro-tilter-mvl11724       | MVL11724       | A    | $  399.99 |
| amigo-mesh-chair-otg10900blk                  | OTG10900BLK    | A    | $  179.99 |
| armless-low-back-stacking-chair-mvl2748       | MVL2748        | A    | $  139.99 |
| ashmont-medium-back-management-tilter-mvl2781 | MVL2781        | A    | $  479.99 |
| avro-350m-heavy-duty-multi-tilter-chairs-mvl1 | MVL11716       | A    | $  699.99 |
| basics-chevron-junior-operator-chair-mvl2363- | MVL2363-7      | A    | $  259.99 |
| basics-comfort-time-ultra-multi-tilter-big-ta |                | A    | $  599.99 |
| basics-ergo-boss-executie-back-multi-tilter-c | BAO28703       | A    | $  749.99 |
| basics-obusforme-elite-heavy-duty-multi-tilte | TS2770-3       | A    | $  899.99 |
| basics-preto-swivel-tilt-chair-1              |                | A    | $  169.99 |
| beta-armless-posture-task-drafting-stool-mvl2 | MVL2718        | A    | $  309.99 |
| bolt-mesh-back-tilter-otg11510b               | OTG11510B      | A    | $  289.99 |
| chair-black-steel-frame-3                     |                | A    | $  357.00 |
| cobalt-medium-back-tilter-mvl2785             | MVL2785        | A    | $  299.99 |
| drift-seating                                 |                | A    | $ 1499.00 |
| elora-multi-tilter-high-back-chair-black-baom | BAOMVL1893     | A    | $  599.99 |
| extended-high-back-tilter-otg11359-carleton   |                | A    | $  319.99 |
| extended-high-back-wide-deep-seat-multi-tilt- | BAO27513       | A    | $  824.98 |
| finch-armless-stacking-armchair-mvl11704      | MVL11704       | A    | $  179.99 |
| format-high-back-weight-sensing-synchro-tilte |                | A    | $  469.99 |
| full-time-chair-mvl2900                       | MVL2900        | A    | $  389.95 |
| global-accord-back-knee-tilter-chair-1        |                | A    | $  769.99 |
| global-accord-mesh-back-tilter                |                | A    | $  749.99 |
| global-obusforme-elite-multi-tilter-chair-hig |                | A    | $  689.99 |
| ibex-drafting-task-stool-mvl2808              | MVL2808        | A    | $  599.99 |
| ibex-mesh-back-drafting-stool-task-chair-with |                | A    | $  499.99 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: Batch 2**
