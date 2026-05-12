# Hero Spec Gap — Batch H2
## Significant Gaps: 5+ Missing Findable Fields (10 products)

**Session type:** Spec researcher
**Reference:** Read `BBI-Session-Kickoff/hero-spec-prompts/MASTER-INSTRUCTIONS.md` before starting.
**Status:** ✅ COMPLETE — merged and pushed to Shopify 2026-05-11

---

## Instructions

1. Read `data/reports/hero-spec-gaps-output.json` — skip any handle already in that file.
2. Read `data/specs.json` — each product below has partial existing specs; only fill the listed blank fields.
3. For each product, web-search the manufacturer + model to fill only the missing fields listed.
4. Write output to `data/reports/hero-spec-gaps-output.json` (merge — do not overwrite existing handles).
5. Checkpoint: save after every 5 products and show a progress card.

---

## Batch H2 — 10 Products (5+ missing findable fields each)

```
BATCH: hero-batch-H2
PRIORITY: high — significant gaps but brand is identifiable

HANDLES:

1. innovation-l-shape-curved-corner
   Title: "Innovation L-Shape Curved Corner"
   Brand hint: brand unknown — "Innovation" may be a product line name;
               check Global Furniture Group, OTG Innovations, or similar
   Missing: manufacturer, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: product_line, materials, key_features already filled

2. innovation-l-shape-set
   Title: "Innovation L-Shape Set"
   Brand hint: likely same Innovation laminate desking line as #1
   Missing: manufacturer, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: product_line, materials, key_features already filled

3. aeramax-air-purifier-true-hepa-plasmatrue-1
   Title: "AeraMax® Air Purifier - True HEPA, PlasmaTrue"
   Brand hint: Fellowes (AeraMax brand)
   Missing: model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: manufacturer, product_line, materials, key_features already filled
   Note: AeraMax is Fellowes' air purifier line; check fellowes.com for full spec sheet

4. bar-leaner-1-span-collaborative
   Title: "Bar Leaner 1-Span Collaborative"
   Brand hint: "1-Span" = single bay of a bar-height leaner/table
   Missing: model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: manufacturer, product_line, materials, key_features already filled

5. l-shape-desk-8-sizes-9-colour-options
   Title: "L-Shape Desk (8 Sizes & 9 Colour options)"
   Brand hint: brand unknown — base variant (no suffix);
               related to handles -1 and -2 in H1A (possibly same product family)
   Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
            certifications, warranty, country_of_manufacture
   Existing: dimensions, materials, finishes_available, key_features already filled

6. napa-boardroom-conference-table
   Title: "Napa Boardroom Conference Table"
   Brand hint: Office Star Napa series (NOT Global) — search "Napa conference table"
   Missing: model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: manufacturer, product_line, materials, key_features already filled

7. loop-leg-table
   Title: "LOOP Leg Table"
   Brand hint: "LOOP Leg" is likely a product series name;
               check Global Furniture Group Loop series or similar
   Missing: model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: manufacturer, product_line, materials, key_features already filled

8. credenza-scmsu
   Title: "Credenza SCMSU"
   Brand hint: likely OTG / Offices to Go (Superior Laminate — "SCMSU" model code prefix)
   Missing: model_codes, dimensions, weight, weight_capacity,
            warranty, country_of_manufacture
   Existing: manufacturer, product_line, materials, finishes_available,
             key_features, certifications already filled

9. indestructible-ryno-furniture
   Title: "Indestructible Ryno Furniture"
   Brand hint: Pineapple Contracts (Ryno series) — heavy-duty institutional furniture
   Missing: model_codes, dimensions, weight, weight_capacity,
            certifications, country_of_manufacture
   Existing: manufacturer, product_line, materials, finishes_available,
             key_features, warranty already filled

10. innovations-double-pedestal-desk-bf-bf-5-sizes-8-colours
    Title: "INNOVATIONS Double Pedestal Desk bf/bf 5 Sizes, 8 Colours"
    Brand hint: likely Global Furniture Group / Innovations laminate desking
    Missing: model_codes, weight, weight_capacity,
             certifications, warranty, country_of_manufacture
    Existing: manufacturer, product_line, dimensions, materials, finishes_available,
              key_features already filled
```

---

## Output Instructions

Write results to `data/reports/hero-spec-gaps-output.json` using this format:

```json
{
  "version": "hero-spec-gaps-v1",
  "products": {
    "av-stand-sa-81-3016": {
      "status": "done",
      "specs": {
        "manufacturer": "...",
        "dimensions": "...",
        "weight": "..."
      },
      "source_urls": ["https://..."],
      "notes": ""
    }
  }
}
```

**Important:** Only include fields in `specs` that you are actually filling (non-empty values you found).
Do not include fields that already have values in specs.json — they won't be overwritten,
but clean output is preferred.
If a field cannot be found after thorough search, omit it.
Use `"status": "skip"` if the product cannot be identified.

---

## End of Session — Run This When All Handles Are Done

When every handle in this batch has been written to `data/reports/hero-spec-gaps-output.json` (status `done`, `skip`, or `service`), run the merge + push in one command:

```bash
python3 scripts/merge-hero-specs.py --live --push
```

This merges the new spec fields into `data/specs.json` and pushes all changes to Shopify immediately. No separate push step needed.

**Then tell Steve:**

> ✅ Hero spec session H2 complete. Merged and pushed to Shopify.
> **Next session → open `BBI-Session-Kickoff/hero-spec-prompts/hero-batch-H3.md` in a new Claude session.**
