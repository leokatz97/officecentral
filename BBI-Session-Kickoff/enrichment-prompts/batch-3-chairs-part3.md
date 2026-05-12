# PE Pass 2 — Batch 3: Chairs — Part 3 of 3
# 25 products · paste this as your FIRST message in a new session

---

## Pre-session checklist (do this before pasting)
1. Run safety preflight from `BBI-Session-Kickoff/01-safety-preflight.md`
2. Confirm dev theme = 186373570873 (preflight does this automatically)

---

## Paste this entire block to start the session

```
You are running a BBI product enrichment session.

BATCH: Batch 3 — Chairs — Part 3 of 3 (25 products)
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
  7. docs/strategy/brand-canonical-map.md  (canonical brand vocabulary
     + sub-brand decisions — required reading for vendor_override)
  8. docs/strategy/brand-canonical-map.csv (machine-readable map for
     string variant → canonical_brand lookup)

BATCH HANDLES (25 products, work through in this order):
   1. sonic-armless-counter-stool-polypropylene-seat-back-6558cs
   2. sparrow-otg10920-guest-chair
   3. stacking-chair-duet-glb6621
   4. the-erin-armless-chair-wood-legs-gc36530
   5. trent-tilter-chair-high-back-bonded-leather-2717-4
   6. tritek-7472-3-chair
   7. ultra-armless-high-back-tilter-mvl11732
   8. ultra-medium-back-guest-chair-with-arms-mvl11742
   9. yoho-medium-back-task-chair-mvl2778
  10. zune-tilter-chair-black-fabric-seat-plastic-mesh-back-medium-back-otg11751b
  11. adapt-high-back-synchro-tilter-mvl11724-mvl11725
  12. adapt-high-back-synchro-tilter-mvl11725
  13. bar-stool-for-42-high-tables
  14. basics-comfort-time-ultra-multi-tilter-chair-with-headrest
  15. cluster-seating-2
  16. concorde-high-back-24hr-executive-synchro-tilter-deep-seat-2424-18
  17. elora-multi-tilter-high-back-chair-black-petite-seat-baomvl1894
  18. factor-mesh-seating-stool
  19. high-back-weight-sensing-synchro-tilter
  20. ibex-upholstered-seat-back-guest-chair-mvl2832
  21. low-back-stacking-chair-mvl2747
  22. marche-guest-chair-8622
  23. marche-guest-chair-copy
  24. obusforme-comfort-high-back-chair-1260-3-schukra
  25. tl-high-back-synchro-tilter

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
    "batch": "Batch 3",
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
    "vendor_override": "...",
    "steve_notes": "...",
    "timestamp": "..."
  }

VENDOR_OVERRIDE RULES:
  - Set vendor_override to the exact canonical_brand from
    docs/strategy/brand-canonical-map.csv where is_standalone_brand=True.
  - For Global Furniture Group divisions, use the STOREFRONT-FACING brand:
    "OTG / Offices to Go" not "Global Upholstery Co.";
    "Global Furniture Group" not "Global Fileworks", "Newland", or "Global Basics".
    Folded sub-brands (is_standalone_brand=False) roll up to their parent_brand.
  - Unknown manufacturer after reasonable research: set vendor_override =
    "Brant Business Interiors" AND add research_failed_reason field explaining
    why (e.g., "no model code in title", "model code matches no known brand").
  - Case-sensitive — match canonical_brand spelling exactly as in the CSV.
  - Never null, never empty string.

CHECKPOINT FORMAT (write to pe-pass2-checkpoint.json after each product):
  completed["handle"] = {
    "action": "yes|skip|edit|other",
    "batch": "Batch 3",
    "timestamp": "..."
  }

VALIDATION (run before reporting batch complete):
  - Every product in the batch output has vendor_override populated
    (never null, never empty string).
  - Every vendor_override value matches a canonical_brand from
    brand-canonical-map.csv exactly (case-sensitive). Use:

      python3 -c "
      import csv
      with open('docs/strategy/brand-canonical-map.csv') as f:
          canonical = {r['canonical_brand'] for r in csv.DictReader(f)
                       if r.get('is_standalone_brand', '').lower() == 'true'}
      # Then check each batch output row's vendor_override is in canonical
      "

Confirm you have read all files listed above, then start with the first
unprocessed handle in this batch. Show me the product card and wait for my input.
```

---

## Products in this batch (25 total)

| Handle | Code | Tier | Price |
|---|---|---|---|
| sonic-armless-counter-stool-polypropylene-sea |                | A    | $  200.50 |
| sparrow-otg10920-guest-chair                  |                | A    | $  159.99 |
| stacking-chair-duet-glb6621                   | GLB6621        | A    | $  169.99 |
| the-erin-armless-chair-wood-legs-gc36530      | GC36530        | A    | $  899.99 |
| trent-tilter-chair-high-back-bonded-leather-2 |                | A    | $  217.99 |
| tritek-7472-3-chair                           |                | A    | $  849.99 |
| ultra-armless-high-back-tilter-mvl11732       | MVL11732       | A    | $  399.99 |
| ultra-medium-back-guest-chair-with-arms-mvl11 | MVL11742       | A    | $  447.99 |
| yoho-medium-back-task-chair-mvl2778           | MVL2778        | A    | $  369.99 |
| zune-tilter-chair-black-fabric-seat-plastic-m | OTG11751B      | A    | $  239.99 |
| adapt-high-back-synchro-tilter-mvl11724-mvl11 | MVL11725       | C    | $  399.99 |
| adapt-high-back-synchro-tilter-mvl11725       | MVL11725       | C    | $  399.99 |
| bar-stool-for-42-high-tables                  |                | C    | $  286.00 |
| basics-comfort-time-ultra-multi-tilter-chair- |                | C    | $  664.99 |
| cluster-seating-2                             |                | C    | $ 1388.00 |
| concorde-high-back-24hr-executive-synchro-til |                | C    | $ 2337.00 |
| elora-multi-tilter-high-back-chair-black-peti | BAOMVL1894     | C    | $  569.99 |
| factor-mesh-seating-stool                     |                | C    | $  599.99 |
| high-back-weight-sensing-synchro-tilter       |                | C    | $  659.00 |
| ibex-upholstered-seat-back-guest-chair-mvl283 | MVL2832        | C    | $  335.99 |
| low-back-stacking-chair-mvl2747               | MVL2747        | C    | $  159.99 |
| marche-guest-chair-8622                       |                | C    | $  570.99 |
| marche-guest-chair-copy                       |                | C    | $  670.64 |
| obusforme-comfort-high-back-chair-1260-3-schu |                | C    | $  769.99 |
| tl-high-back-synchro-tilter                   |                | C    | $  679.99 |

---

## When this batch is done

Type `done` to end the session. Claude will:
1. Commit checkpoint + output to git
2. Print a summary (done / skipped / edited / other)
3. Tell you the next batch to open

**Next batch after this one: Batch 4**
