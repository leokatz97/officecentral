# PE Pass 2 — Batch 2: Chairs — Part 2 of 3
# 26 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 2 — Chairs — Part 2 of 3 (26 products)
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
   1. ibex-mesh-seat-back-armless-drafting-chair-mvl2827
   2. ibex-synchro-tilter-chairs-mvl2801
   3. ibex-upholstered-seat-back-guest-chair-mvl2819-1
   4. ibex-upholstered-seat-mesh-back-tilter-chair-mvl2801
   5. kneeling-chair-kcm1420
   6. knight-lightweight-tilter-chair-otg11360
   7. kody-mesh-chair-otg13110
   8. kylie-multi-purpose-stacking-chair-cadet-otg11355c
   9. marlee-midback-chair-bonded-leather-mvl11722
  10. mesh-chair-java-otg10902
  11. minto-low-back-stacking-armchair-mvl2747
  12. mobile-folding-chair-storage-cart-3
  13. mvl11860-stradic-mesh-back-tilter
  14. mvl2732-annapolis-high-back-luxhide-tilter
  15. mvl2786-yoho-armless-low-back-task-chair
  16. mvl3101-avro-mesh-back-synchro-tilter-chair
  17. mvl3103-avro-upholstered-seat-mesh-back-multi-tilter
  18. obusforme-comfort-medium-back-chair-fabric-1241-3-copy
  19. obusforme-comfort-medium-back-chair-fabric-1241-3-copy-1
  20. obusforme-elite-multi-tilter-chair-medium-back
  21. offices-to-go-ashmont-tilter-chair-1
  22. offices-to-go-chair-2
  23. otg10740-masi-high-back-tilter
  24. otg3915-centro-guest-chair
  25. pacific-high-back-tilter
  26. regalia-task-mesh-chair-otg10892

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
    "batch": "Batch 2",
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
    "batch": "Batch 2",
    "timestamp": "..."
  }

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (26 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| ibex-mesh-seat-back-armless-drafting-chair-mv | MVL2827        | A    | $  529.99 |
| ibex-synchro-tilter-chairs-mvl2801            | MVL2801        | A    | $  399.99 |
| ibex-upholstered-seat-back-guest-chair-mvl281 | MVL2819        | A    | $  353.87 |
| ibex-upholstered-seat-mesh-back-tilter-chair- | MVL2804        | A    | $  379.99 |
| kneeling-chair-kcm1420                        | KCM1420        | A    | $  179.99 |
| knight-lightweight-tilter-chair-otg11360      | OTG11360       | A    | $  279.99 |
| kody-mesh-chair-otg13110                      | OTG13110       | A    | $  319.99 |
| kylie-multi-purpose-stacking-chair-cadet-otg1 | OTG11355C      | A    | $  159.99 |
| marlee-midback-chair-bonded-leather-mvl11722  | MVL11722       | A    | $  399.99 |
| mesh-chair-java-otg10902                      | OTG10902       | A    | $  249.99 |
| minto-low-back-stacking-armchair-mvl2747      | MVL2747        | A    | $  158.90 |
| mobile-folding-chair-storage-cart-3           |                | A    | $  298.71 |
| mvl11860-stradic-mesh-back-tilter             |                | A    | $  349.99 |
| mvl2732-annapolis-high-back-luxhide-tilter    |                | A    | $  219.99 |
| mvl2786-yoho-armless-low-back-task-chair      |                | A    | $  239.99 |
| mvl3101-avro-mesh-back-synchro-tilter-chair   |                | A    | $  469.99 |
| mvl3103-avro-upholstered-seat-mesh-back-multi |                | A    | $  499.99 |
| obusforme-comfort-medium-back-chair-fabric-12 |                | A    | $  645.99 |
| obusforme-comfort-medium-back-chair-fabric-12 |                | A    | $  749.99 |
| obusforme-elite-multi-tilter-chair-medium-bac |                | A    | $  669.99 |
| offices-to-go-ashmont-tilter-chair-1          |                | A    | $  499.99 |
| offices-to-go-chair-2                         |                | A    | $  321.00 |
| otg10740-masi-high-back-tilter                |                | A    | $  319.99 |
| otg3915-centro-guest-chair                    |                | A    | $  249.99 |
| pacific-high-back-tilter                      | MVL11870       | A    | $  369.99 |
| regalia-task-mesh-chair-otg10892              | OTG10892       | A    | $  369.99 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: Batch 3**
