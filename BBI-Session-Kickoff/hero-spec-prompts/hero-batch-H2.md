# Hero Spec Gap — Batch H2
## Significant Gaps: 5+ Missing Findable Fields (19 products)

**Session type:** Spec researcher
**Reference:** Read `BBI-Session-Kickoff/hero-spec-prompts/MASTER-INSTRUCTIONS.md` before starting.

---

## Instructions

1. Read `data/reports/hero-spec-gaps-output.json` — skip any handle already in that file.
2. Read `data/specs.json` — each product below has partial existing specs; only fill the listed blank fields.
3. For each product, web-search the manufacturer + model to fill only the missing fields listed.
4. Write output to `data/reports/hero-spec-gaps-output.json` (merge — do not overwrite existing handles).
5. Checkpoint: save after every 5 products and show a progress card.

---

## Batch H2 — 19 Products (5+ missing findable fields each)

```
BATCH: hero-batch-H2
PRIORITY: high — significant gaps but brand is identifiable

HANDLES:

1. av-stand-sa-81-3016
   Title: "AV Stand SA-81-3016"
   Brand hint: brand unknown — "SA-81-3016" is the model code; search it directly
   Missing: manufacturer, product_line, dimensions, weight, weight_capacity,
            materials, finishes_available, certifications, warranty, country_of_manufacture
   Note: model code SA-81-3016 should identify brand directly

2. caster-options
   Title: "Caster Options"
   Brand hint: accessory product — likely OTG / Global chair casters
   Missing: manufacturer, product_line, model_codes, dimensions, weight, weight_capacity,
            materials, certifications, warranty, country_of_manufacture
   Note: if this is a generic "caster upgrade" option, use skip status with explanation

3. folding-chair-plastic-4-pack
   Title: "Folding Chair-Plastic 4/Pack"
   Brand hint: likely Global Furniture Group (Flap folding chair) or generic event seating
   Missing: manufacturer, product_line, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture

4. u-shape-height-adjust-desk
   Title: "U-Shape Height Adjust Desk"
   Brand hint: brand unknown — electric height-adjustable U-shape;
               check Global Zira, OTG, or Innovations lines
   Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
            materials, finishes_available, certifications, warranty, country_of_manufacture

5. upscale-table-1
   Title: "UPSCALE Table"
   Brand hint: "UPSCALE" appears to be a product line name — search it
   Missing: manufacturer, product_line, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture

6. casters-2-5-set-1
   Title: "Casters - 2\" 5 / Set"
   Brand hint: 2" caster set (5 casters) — likely OTG / Global chair replacement casters
   Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
            materials, certifications, warranty, country_of_manufacture
   Note: "2 inch" and "5/set" are the size and quantity

7. casters-5-set-1
   Title: "Casters- 5 / Set"
   Brand hint: 5" caster set — likely OTG / Global chair replacement casters (larger caster)
   Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
            materials, certifications, warranty, country_of_manufacture
   Note: these may be the same line as #6 but different size

8. innovation-l-shape-curved-corner
   Title: "Innovation L-Shape Curved Corner"
   Brand hint: brand unknown — "Innovation" may be a product line name;
               check Global Furniture Group, OTG Innovations, or similar
   Missing: manufacturer, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: product_line, materials, key_features already filled

9. innovation-l-shape-set
   Title: "Innovation L-Shape Set"
   Brand hint: likely same Innovation laminate desking line as #8
   Missing: manufacturer, model_codes, dimensions, weight, weight_capacity,
            finishes_available, certifications, warranty, country_of_manufacture
   Existing: product_line, materials, key_features already filled

10. aeramax-air-purifier-true-hepa-plasmatrue-1
    Title: "AeraMax® Air Purifier - True HEPA, PlasmaTrue"
    Brand hint: Fellowes (AeraMax brand)
    Missing: model_codes, dimensions, weight, weight_capacity,
             finishes_available, certifications, warranty, country_of_manufacture
    Existing: manufacturer, product_line, materials, key_features already filled
    Note: AeraMax is Fellowes' air purifier line; check fellowes.com for full spec sheet

11. bar-leaner-1-span-collaborative
    Title: "Bar Leaner 1-Span Collaborative"
    Brand hint: "1-Span" = single bay of a bar-height leaner/table
    Missing: model_codes, dimensions, weight, weight_capacity,
             finishes_available, certifications, warranty, country_of_manufacture
    Existing: manufacturer, product_line, materials, key_features already filled

12. ceiling-baffles-sound-acoustic-dampeners
    Title: "Ceiling Baffles Sound Acoustic Dampeners"
    Brand hint: acoustic-felt ceiling baffles — check Acoustics First, FilzFelt,
                OBEX, Designtex, or Canadian acoustic suppliers
    Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
             certifications, warranty, country_of_manufacture
    Existing: materials, finishes_available, dimensions, key_features already filled

13. l-shape-desk-8-sizes-9-colour-options
    Title: "L-Shape Desk (8 Sizes & 9 Colour options)"
    Brand hint: brand unknown — base variant (no suffix);
                related to handles -1 and -2 in H1A (possibly same product family)
    Missing: manufacturer, product_line, model_codes, weight, weight_capacity,
             certifications, warranty, country_of_manufacture
    Existing: dimensions, materials, finishes_available, key_features already filled

14. loop-leg-table
    Title: "LOOP Leg Table"
    Brand hint: "LOOP Leg" is likely a product series name;
                check Global Furniture Group Loop series or similar
    Missing: model_codes, dimensions, weight, weight_capacity,
             finishes_available, certifications, warranty, country_of_manufacture
    Existing: manufacturer, product_line, materials, key_features already filled

15. napa-boardroom-conference-table
    Title: "Napa Boardroom Conference Table"
    Brand hint: Office Star Napa series (NOT Global) — search "Napa conference table"
    Missing: model_codes, dimensions, weight, weight_capacity,
             finishes_available, certifications, warranty, country_of_manufacture
    Existing: manufacturer, product_line, materials, key_features already filled

16. auditorium-lecture-hall-seating-my-space
    Title: "Auditorium / Lecture Hall Seating My Space"
    Brand hint: likely Global Furniture Group (Pedestal/Beam Seating, "My Space" descriptor)
    Missing: model_codes, dimensions, weight, weight_capacity,
             materials, finishes_available
    Existing: manufacturer, product_line, key_features, certifications,
              warranty, country_of_manufacture already filled

17. credenza-scmsu
    Title: "Credenza SCMSU"
    Brand hint: likely OTG / Offices to Go (Superior Laminate — "SCMSU" model code prefix)
    Missing: model_codes, dimensions, weight, weight_capacity,
             warranty, country_of_manufacture
    Existing: manufacturer, product_line, materials, finishes_available,
              key_features, certifications already filled

18. indestructible-ryno-furniture
    Title: "Indestructible Ryno Furniture"
    Brand hint: Pineapple Contracts (Ryno series) — heavy-duty institutional furniture
    Missing: model_codes, dimensions, weight, weight_capacity,
             certifications, country_of_manufacture
    Existing: manufacturer, product_line, materials, finishes_available,
              key_features, warranty already filled

19. innovations-double-pedestal-desk-bf-bf-5-sizes-8-colours
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
