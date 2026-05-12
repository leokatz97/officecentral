# Hero Spec Gap — Batch H1B
## Fully-Empty Products: Remaining (11 products)

**Session type:** Spec researcher
**Reference:** Read `BBI-Session-Kickoff/hero-spec-prompts/MASTER-INSTRUCTIONS.md` before starting.

---

## Instructions

1. Read `data/reports/hero-spec-gaps-output.json` — skip any handle already in that file.
2. Read `data/specs.json` — all products below have ALL 12 spec fields blank (except `installation1000` which is a service SKU).
3. For each product, web-search to identify the manufacturer and fill all 12 spec fields.
4. Write output to `data/reports/hero-spec-gaps-output.json` (merge — do not overwrite existing handles).
5. Checkpoint: save after every 5 products and show a progress card.

---

## Special Notes

- **`installation1000`**: This is a service line item (installation service), NOT a physical product. Mark it `"status": "service"` with no specs. Do not research it.
- **`medicine-wheel-table-indigenous`**: This is a specialized cultural/ceremonial table for Indigenous communities. Research carefully and respectfully. It may be a custom/artisan piece with limited online documentation — that is OK. Use `"status": "skip"` if no reliable sourcing is available, with a clear note.
- **`outdoor-park-benches`** and **`outdoor-steel-bench`**: These are commercial outdoor furnishings — check municipal/commercial furniture suppliers.

---

## Batch H1B — 11 Products

All products below are **completely empty** (all 12 spec fields missing) unless otherwise noted.

```
BATCH: hero-batch-H1B
PRIORITY: high — fully empty, all fields need filling

HANDLES:

1. l-shape-loop-leg-desk
   Title: "L-Shape Loop Leg Desk"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "Loop Leg" is a leg style; check Global Furniture Group
         (they have loop/sled leg desking lines)

2. mobile-pedestal-drawer-box-file
   Title: "Mobile Pedestal Drawer Box/File"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "Box/File" = top box drawer + lower file drawer;
         very common OTG / Global / Newland accessory pedestal

3. premium-height-adjustable-table-1
   Title: "Premium Height Adjustable Table"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — search "premium height adjustable table electric Canada"

4. square-table-x-base-3-sizes
   Title: "Square Table - X-Base 3 Sizes"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — X-Base is a leg/base style;
         search "square table X-base 3 sizes office Canada"

5. storage-cabinet-medium-duty-72x18x36w
   Title: 'Storage Cabinet Medium Duty 72"x18"x36"W'
   Missing ALL: (all 12 fields)
   Hint: brand unknown — "medium duty" + exact dimensions are distinctive;
         check Global, OTG, Tennsco, Hallowell steel storage

6. table-desk-1
   Title: "Table Desk"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — generic name; check Shopify admin for product images
         or vendor field to narrow down the brand

7. chair-black-steel-frame-2
   Title: "Chair Black Steel Frame"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — could be stacking chair or multi-use chair;
         search "chair black steel frame commercial Canada stacking"

8. outdoor-park-benches
   Title: "Outdoor Park Benches"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — commercial/municipal outdoor furniture;
         check Landscape Forms, Victor Stanley, Wabash Valley, SiteScapes

9. outdoor-steel-bench
   Title: "Outdoor Steel Bench"
   Missing ALL: (all 12 fields)
   Hint: brand unknown — similar to #8; check same commercial outdoor suppliers

10. medicine-wheel-table-indigenous
    Title: "Medicine Wheel Table Indigenous"
    Missing ALL: (all 12 fields)
    Hint: Specialized cultural/ceremonial table for Indigenous communities.
    ⚠️ Research respectfully — this is a sacred cultural item, not a standard office product.
    It may be artisan/custom-made. If no public spec sheet exists, use "status": "skip"
    with notes on what was found. Do NOT fabricate specs for this product.

11. installation1000
    Title: "Installation1000"
    ⚠️ SERVICE SKU — this is an installation service, NOT a product.
    Mark as "status": "service" with empty specs. Do not research.
```

---

## Output Instructions

Write results to `data/reports/hero-spec-gaps-output.json` using this format:

```json
{
  "version": "hero-spec-gaps-v1",
  "products": {
    "l-shape-loop-leg-desk": {
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
    },
    "installation1000": {
      "status": "service",
      "specs": {},
      "source_urls": [],
      "notes": "Service SKU — no product specs applicable"
    }
  }
}
```

If a field cannot be found after thorough search, omit it from the output (do not include an empty value).
If the product cannot be identified at all, use `"status": "skip"` and note what was searched.
