# Hero Spec Gap — Batch H1A
## Fully-Empty Products: Desks, Tables & Workstations (12 products)

**Session type:** Spec researcher
**Reference:** Read `BBI-Session-Kickoff/hero-spec-prompts/MASTER-INSTRUCTIONS.md` before starting.

---

## Instructions

1. Read `data/reports/hero-spec-gaps-output.json` — skip any handle already in that file.
2. Read `data/specs.json` — all 12 products below have ALL 12 spec fields blank.
3. For each product, web-search to identify the manufacturer and fill all 12 spec fields.
4. Write output to `data/reports/hero-spec-gaps-output.json` (merge — do not overwrite existing handles).
5. Checkpoint: save after every 5 products and show a progress card.

---

## Batch H1A — 12 Products

All products below are **completely empty** — all 12 spec fields missing.

```
BATCH: hero-batch-H1A
PRIORITY: high — fully empty, all fields need filling

HANDLES:

1. 4-person-workstation
   Title: "4 Person Workstation"
   Missing ALL: manufacturer, product_line, model_codes, dimensions, weight,
                weight_capacity, materials, finishes_available, key_features,
                certifications, warranty, country_of_manufacture
   Hint: brand unknown — search "4 person workstation office furniture Canada" to identify

2. 6-person-workstation-chairs-bridges
   Title: "6 Person Workstation & Chairs Bridges"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — search "6 person workstation bridges office furniture Canada"

3. d-top-table
   Title: "D-Top Table With or Without Modesty"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "D-Top" is a common desk shape descriptor;
         search "D-top desk modesty panel Canada office furniture"

4. desk-single-pedestal-bbf
   Title: "Desk Single Pedestal BBF"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "BBF" = Box/Box/File drawer configuration;
         search "single pedestal desk BBF office Canada"

5. executive-u-shape-desk-set
   Title: "Executive U-Shape Desk Set"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — search "executive U-shape desk set Canada laminate"

6. height-adjustable-l-shape-table
   Title: "Premium Height Adjustable L-Shape Table"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — search "premium height adjustable L-shape table electric Canada"

7. height-adjustable-table-5-sizes
   Title: "Electric Height Adjustable Sit to Stand Desks"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — search "electric sit stand desk 5 sizes Canada"

8. l-shape-desk-3-sizes-13-colours
   Title: '"L" Shape Desk 6 Sizes 13 colours'
   Missing ALL: (all 12 fields)
   Hint: brand unknown — the "13 colours" detail is distinctive;
         search 'L-shape desk "13 colours" OR "13 colors" Canada office'

9. l-shape-desk-8-sizes-9-colour-options-1
   Title: "L-Shape Desk (8 Sizes & 9 Colour options)"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "8 sizes 9 colours" is a distinctive SKU count;
         Note: there are 3 variants of this title (handles -1, -2, and base).
         All three may be the same product line — check if they share model codes.

10. l-shape-desk-8-sizes-9-colour-options-2
    Title: "L-Shape Desk (8 Sizes & 9 Colour options)"
    Missing ALL: (all 12 fields)
    Hint: same product family as #9 above — likely a different size or config

11. l-shape-desk-hutch
    Title: "L-Shape Desk & Hutch"
    Missing ALL: (all 12 fields)
    Hint: brand unknown — search "L-shape desk hutch combo Canada laminate"

12. l-shape-height-adjustable-desk-set
    Title: "L-Shape Height Adjustable Desk Set"
    Missing ALL: (all 12 fields)
    Hint: brand unknown — search "L-shape height adjustable desk set electric Canada"
```

---

## Output Instructions

Write results to `data/reports/hero-spec-gaps-output.json` using this format:

```json
{
  "version": "hero-spec-gaps-v1",
  "products": {
    "4-person-workstation": {
      "status": "done",
      "specs": {
        "manufacturer": "...",
        "product_line": "...",
        "model_codes": ["..."],
        "dimensions": "...",
        "weight": "...",
        "weight_capacity": "...",
        "materials": "...",
        "finishes_available": ["..."],
        "key_features": ["..."],
        "certifications": ["..."],
        "warranty": "...",
        "country_of_manufacture": "..."
      },
      "source_urls": ["https://..."],
      "notes": ""
    }
  }
}
```

If a field cannot be found after thorough search, omit it from the output (do not include an empty value).
If the product cannot be identified at all, use `"status": "skip"` and note what was searched.

---

## End of Session — Run This When All Handles Are Done

When every handle in this batch has been written to `data/reports/hero-spec-gaps-output.json` (status `done`, `skip`, or `service`), run the merge + push in one command:

```bash
python3 scripts/merge-hero-specs.py --live --push
```

This merges the new spec fields into `data/specs.json` and pushes all changes to Shopify immediately. No separate push step needed.

**Then tell Steve:**

> ✅ Hero spec session H1A complete. Merged and pushed to Shopify.
> **Next session → open `BBI-Session-Kickoff/hero-spec-prompts/hero-batch-H1B.md` in a new Claude session.**
