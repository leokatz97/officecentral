# PE Pass 2 — Batch 6: Storage & Accessories
# 30 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 6 — Storage & Accessories (30 products)
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

BATCH HANDLES (30 products, work through in this order):
   1. 2-drawer-legal-width-vertical-file
   2. bookcase
   3. bookcase-1-shelf-32-wide-x-72-high
   4. bookcase-with-closed-lower-storage
   5. heartwood-mobile-pedestal-bf
   6. kensington-ac12-security-charging-cabinet
   7. large-fire-water-safe-13-x-16-x-19-black-2
   8. mobile-drawer-unit-with-locks-inv-mpuf
   9. newland-16w-box-box-file-mobile-pedestal-nlmp23bbf
  10. newland-bookcases-assembled
  11. pedestal-file-file-with-or-without-wheels
  12. sentry-safe-security-safe-with-electronic-lock-4
  13. wardrobe-storage-cabinet-htwlevsr7218
  14. 4-drawer-legal-width-vertical-file
  15. fireking-storage-cabinet-44-high
  16. laminate-lockers-copy
  17. lateral-file-storage-cabinet-with-shelves
  18. fellowes-array-ceiling-ac2-air-purifier
  19. fellowes-array-recess-ar-air-purifier-1
  20. fellowes-array-wall-stand-air-purification
  21. fellowes-lotus-dual-monitor-arm-kit-2-display-s-supported27-arm-only-fel8042901
  22. otg-mobile-foot-kit-pack-of-2
  23. otg-panels
  24. otgma2-dual-monitor-arm
  25. rollamat-for-carpet-carpeted-floor-53-x-45-3
  26. ceiling-grids-sound-acoustic-dampeners-copy
  27. halifax-typical-4
  28. partitions-66-high-2-offices-1
  29. partitions-66-high-3-offices-1
  30. planter

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
    "batch": "Batch 6",
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
    "batch": "Batch 6",
    "timestamp": "..."
  }

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (30 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| 2-drawer-legal-width-vertical-file            |                | A    | $  329.99 |
| bookcase                                      |                | A    | $  269.99 |
| bookcase-1-shelf-32-wide-x-72-high            |                | A    | $  380.54 |
| bookcase-with-closed-lower-storage            |                | A    | $  449.99 |
| heartwood-mobile-pedestal-bf                  |                | A    | $  399.99 |
| kensington-ac12-security-charging-cabinet     |                | A    | $ 1725.89 |
| large-fire-water-safe-13-x-16-x-19-black-2    |                | A    | $  369.89 |
| mobile-drawer-unit-with-locks-inv-mpuf        |                | A    | $  499.99 |
| newland-16w-box-box-file-mobile-pedestal-nlmp | NLMP23BBF      | A    | $  589.99 |
| newland-bookcases-assembled                   |                | A    | $  399.99 |
| pedestal-file-file-with-or-without-wheels     |                | A    | $  419.99 |
| sentry-safe-security-safe-with-electronic-loc |                | A    | $  359.99 |
| wardrobe-storage-cabinet-htwlevsr7218         | HTWLEVSR7218   | A    | $  629.99 |
| 4-drawer-legal-width-vertical-file            |                | C    | $  489.99 |
| fireking-storage-cabinet-44-high              |                | C    | $ 5299.79 |
| laminate-lockers-copy                         |                | C    | $ 1219.20 |
| lateral-file-storage-cabinet-with-shelves     |                | C    | $ 1009.99 |
| fellowes-array-ceiling-ac2-air-purifier       |                | B    | $ 5800.00 |
| fellowes-array-recess-ar-air-purifier-1       |                | B    | $ 3929.00 |
| fellowes-array-wall-stand-air-purification    |                | B    | $ 3150.00 |
| fellowes-lotus-dual-monitor-arm-kit-2-display | FEL8042901     | B    | $  146.89 |
| otg-mobile-foot-kit-pack-of-2                 |                | B    | $  169.99 |
| otg-panels                                    |                | B    | $  439.99 |
| otgma2-dual-monitor-arm                       |                | B    | $  159.99 |
| rollamat-for-carpet-carpeted-floor-53-x-45-3  |                | B    | $  306.00 |
| ceiling-grids-sound-acoustic-dampeners-copy   |                | C    | $  608.00 |
| halifax-typical-4                             |                | C    | $ 4450.00 |
| partitions-66-high-2-offices-1                |                | C    | $ 2099.99 |
| partitions-66-high-3-offices-1                |                | C    | $ 2999.00 |
| planter                                       |                | C    | $ 1399.99 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: Batch 7**
