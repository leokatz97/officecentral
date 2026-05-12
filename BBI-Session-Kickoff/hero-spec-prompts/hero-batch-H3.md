# Hero Spec Gap — Batch H3
## Minor Gaps: 1–5 Missing Fields (57 products)

**Session type:** Spec researcher
**Reference:** Read `BBI-Session-Kickoff/hero-spec-prompts/MASTER-INSTRUCTIONS.md` before starting.

---

## Instructions

1. Read `data/reports/hero-spec-gaps-output.json` — skip any handle already in that file.
2. Read `data/specs.json` — each product below has partial existing specs; only fill the listed blank fields.
3. Most products here have a known brand (OTG/Offices to Go, Global Furniture Group, Fellowes, etc.) — use model codes in titles to look up specific spec pages.
4. Write output to `data/reports/hero-spec-gaps-output.json` (merge — do not overwrite existing handles).
5. Checkpoint: save after every 5 products and show a progress card.

---

## Quick Reference — OTG / Offices to Go Lookups

Many products below are OTG (Offices to Go / Global Total Office). Their pages are at:
- `https://www.officestogo.com/products/...`
- Search by MVL or OTG model code directly (e.g. "MVL2782 chair" or "OTG12112B chair")

---

## Batch H3A — OTG / Offices to Go Chairs (14 products)

```
BATCH: hero-batch-H3A (sub-batch of H3)

1. arlo-lounge-swivel-task-chair-1
   Title: "Arlo | Lounge Swivel Task Chair"
   Brand: OTG / Offices to Go
   Missing: warranty
   Existing: manufacturer, product_line, model_codes, dimensions, weight,
             weight_capacity, materials, finishes_available, key_features,
             certifications, country_of_manufacture

2. ashmont-medium-back-guest-chair-mvl2782
   Title: "Ashmont | Medium Back Guest Chair MVL2782"
   Brand: OTG / Offices to Go (model: MVL2782)
   Missing: weight_capacity, warranty

3. ashton-high-back-tilter
   Title: "Ashton | High Back Tilter"
   Brand: OTG / Offices to Go
   Missing: weight_capacity, warranty, country_of_manufacture

4. brighton-high-back-tilter-mvl2787
   Title: "Brighton | High Back Tilter MVL2787"
   Brand: OTG / Offices to Go (model: MVL2787)
   Missing: weight_capacity, warranty

5. format-high-back-synchro-tilter-with-adjustable-headrest-chair-mvl3192
   Title: "Format | High Back Synchro-Tilter with Adjustable Headrest Chair MVL3192"
   Brand: OTG / Offices to Go (model: MVL3192)
   Missing: weight_capacity, warranty

6. format-high-mesh-back-synchro-tilter
   Title: "Format | High Mesh Back Synchro-Tilter"
   Brand: OTG / Offices to Go
   Missing: weight_capacity, warranty

7. ibex-mesh-seat-back-multi-tilter-1
   Title: "Ibex | Mesh Seat & Back Multi-Tilter"
   Brand: OTG / Offices to Go
   Missing: weight_capacity, warranty

8. ibex-upholstered-seat-mesh-back-multi-tilter-1
   Title: "Ibex | Upholstered Seat & Mesh Back Multi-Tilter MVL2803"
   Brand: OTG / Offices to Go (model: MVL2803)
   Missing: weight_capacity, finishes_available, certifications, warranty, country_of_manufacture

9. kaysee-high-back-tilter-otg12112b
   Title: "Kaysee | High Back Tilter OTG12112B"
   Brand: OTG / Offices to Go (model: OTG12112B)
   Missing: weight, weight_capacity, certifications, warranty, country_of_manufacture

10. mvl11886-caman-high-back-tilter-bonded-leather
    Title: "MVL11886 Caman | High Back Tilter Bonded Leather"
    Brand: OTG / Offices to Go (model: MVL11886)
    Missing: weight_capacity, warranty

11. otg13026-safari-medium-mesh-back-tilter-chair
    Title: "OTG13026 Safari | Medium Mesh Back Tilter Chair"
    Brand: OTG / Offices to Go (model: OTG13026)
    Missing: weight_capacity, warranty, country_of_manufacture

12. overtime-350-high-back-heavy-duty-multi-tilter-mvl13040
    Title: "Overtime 350 | High Back Heavy Duty Multi-Tilter MVL13040"
    Brand: OTG / Offices to Go (model: MVL13040)
    Missing: certifications, warranty

13. overtime-350-high-back-heavy-duty-multi-tilter
    Title: "Overtime 350 | High Back Heavy Duty Multi-Tilter"
    Brand: OTG / Offices to Go
    Missing: warranty

14. raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b
    Title: "Raven High Back Heavy Duty Synchro-Tilter Chair OTG10703B"
    Brand: OTG / Offices to Go (model: OTG10703B)
    Missing: warranty, country_of_manufacture
```

---

## Batch H3B — OTG / Offices to Go Furniture (7 products)

```
BATCH: hero-batch-H3B (sub-batch of H3)

1. desktop-sit-stand-workstation-mvl5230b0
   Title: "Desktop Sit-Stand Workstation MVL5230B0"
   Brand: OTG / Offices to Go (model: MVL5230B0)
   Missing: certifications, warranty, country_of_manufacture

2. l-shape-reception-72-x-72-x-41-1
   Title: 'L-Shape Reception - 72" x 72" x 41"'
   Brand: OTG / Offices to Go (Newland L-Shaped Reception)
   Missing: weight_capacity, warranty

3. lounge-seating-3-sizes-suburb
   Title: "Lounge Seating 3 sizes Suburb"
   Brand: OTG / Offices to Go (Suburb lounge series)
   Missing: weight, weight_capacity, warranty

4. newland-box-file-mobile-pedestal
   Title: "Newland Box/File Mobile Pedestal NLMP23BF"
   Brand: OTG / Offices to Go (Newland line, model: NLMP23BF)
   Missing: weight_capacity, warranty

5. offices-to-go-newland-l-shaped-suite-nlp420
   Title: "Offices to Go® Newland™ L-Shaped Suite NLP420"
   Brand: OTG / Offices to Go (model: NLP420)
   Missing: weight_capacity, warranty

6. u-shape-desk-nlp205
   Title: "U-Shape Desk NLP205"
   Brand: OTG / Offices to Go (model: NLP205)
   Missing: weight, weight_capacity, country_of_manufacture

7. ultra-high-back-tilter-with-arms-mvl11730
   Title: "Ultra | High Back Tilter with Arms MVL11730"
   Brand: OTG / Offices to Go (model: MVL11730)
   Missing: weight_capacity, warranty
```

---

## Batch H3C — Global Furniture Group Products (14 products)

```
BATCH: hero-batch-H3C (sub-batch of H3)

1. 2600-series-4-drawer-vertical-file-legal-26-451
   Title: "2600 Series 4 Drawer Vertical File, Legal (26-451)"
   Brand: Global Furniture Group (model: 26-451)
   Missing: weight_capacity

2. 4-drawer-letter-width-vertical-file
   Title: "4 Drawer Letter Width Vertical File"
   Brand: Global Furniture Group (2600 Series, model: 26-401)
   Missing: weight, weight_capacity

3. boat-shaped-conference-table
   Title: "Boat Shaped Conference Table"
   Brand: Global Furniture Group (Zira / Adaptabilities / Anywhere series)
   Missing: model_codes, weight, weight_capacity

4. chevron-ultra-high-back-multi-tilter-chair-high-back-bao11203-1
   Title: "Chevron Ultra High Back Multi-Tilter Chair - High Back BAO11203"
   Brand: Global Furniture Group (model: BAO11203)
   Missing: dimensions, weight, weight_capacity, certifications, warranty

5. citi-lounge-seating-3-sizes-available
   Title: "Lounge Seating (3 sizes available)"
   Brand: Global Furniture Group (Citi series)
   Missing: model_codes, weight, weight_capacity

6. ergo-boss-high-back-multi-tilter-chair-1
   Title: "Ergo Boss™ High Back Multi-Tilter Chair"
   Brand: Global Furniture Group
   Missing: dimensions, weight, weight_capacity, certifications, warranty

7. gc-comet-bariatric-stacking-armchair-gc2180-1
   Title: "GC Comet™ Bariatric Stacking Armchair (GC2180)"
   Brand: Global Furniture Group (Global Care, model: GC2180)
   Missing: weight

8. global-recliner-primacare-gc3608mrc
   Title: "Global Recliner Primacare GC3608MRC"
   Brand: Global Furniture Group (Global Care, model: GC3608MRC)
   Missing: dimensions, weight, weight_capacity

9. multi-storage-cabinet-93365msl
   Title: "Multi-Storage Cabinet 93365MSL"
   Brand: Global Furniture Group (model: 93365MSL)
   Missing: weight_capacity

10. premium-series-lateral-file-cabinet-2-3-4-5-drawer-1
    Title: "Premium Series Lateral File Cabinet (2,3,4 & 5 Drawer)"
    Brand: Global Furniture Group
    Missing: model_codes, weight, weight_capacity

11. robust-high-back-multi-tilter-chair-500lb-weight-capacity-glb74475
    Title: "Robust High Back Multi-Tilter Chair 500lb Weight Capacity GLB74475"
    Brand: Global Furniture Group (model: GLB74475)
    Missing: weight

12. sidero-guest-chair-28-colour-options
    Title: "Sidero Guest Chair 28 Colour Options"
    Brand: Global Furniture Group
    Missing: model_codes, dimensions, weight, weight_capacity

13. sirena-lounge-chair-3371
    Title: "Sirena Lounge Chair"
    Brand: Global Furniture Group
    Missing: dimensions, weight, weight_capacity

14. terina-training-tables-rectangular-table-8-sizes
    Title: "Terina™ Training Tables Rectangular Table 8 Sizes"
    Brand: Global Furniture Group
    Missing: model_codes, weight, weight_capacity
```

---

## Batch H3D — Mixed Brands (13 products)

```
BATCH: hero-batch-H3D (sub-batch of H3)

1. aktivity-environ-table
   Title: "Aktivity Environ table"
   Brand: likely MityBilt (Aktivity series)
   Missing: model_codes, dimensions, weight, weight_capacity

2. aktivity-puddle
   Title: "Aktivity Puddle"
   Brand: likely MityBilt (Aktivity series)
   Missing: weight, weight_capacity

3. anti-fatigue-wellness-mat-36-x-24-5
   Title: 'Anti-Fatigue Wellness Mat  36" x 24"'
   Brand: likely Fellowes (Anti-Fatigue Wellness Floor Mat 8707002)
   Missing: weight, weight_capacity, certifications, warranty, country_of_manufacture

4. array-stand-as-air-purifier-1
   Title: "Array™ Stand AS Air Purifier"
   Brand: Fellowes (Array AS series)
   Missing: weight, weight_capacity, certifications, warranty, country_of_manufacture

5. auditorium-lecture-hall-seating
   Title: "Auditorium / Lecture Hall Seating"
   Brand: Global Furniture Group (Pedestal/Beam Seating)
   Missing: model_codes, dimensions, weight, weight_capacity, finishes_available

6. basics-comfort-time-ultra-multi-tilter-chairs-mvl1873-1
   Title: "Basics® Comfort-Time™ Ultra Multi-Tilter Chairs MVL1873"
   Brand: Global / OTG (Basics® line, model: MVL1873)
   Missing: dimensions, weight, certifications, warranty

7. bookcase-15-sizes-available
   Title: "Bookcase (15 Sizes Available)"
   Brand: OTG / Offices to Go (Newland or Superior Laminate Bookcase)
   Missing: weight, weight_capacity, warranty

8. ceiling-grids-sound-acoustic-dampeners-1
   Title: "Ceiling Grids Sound Acoustic Dampeners"
   Brand: likely acoustic ceiling grid panels supplier
   Missing: model_codes, weight, weight_capacity, warranty

9. foundations-sport-splash-quad-strollers
   Title: "Foundations Sport Splash, Quad Strollers"
   Brand: Foundations Worldwide (Gaggle / Sport Splash daycare strollers)
   Missing: model_codes, weight, certifications, warranty, country_of_manufacture

10. nesting-training-table-8-colour-choices
    Title: "Nesting Training Table (8 Colour Choices)"
    Brand: OTG / Offices to Go (Newland flip-top training tables) or Global 2gether
    Missing: weight, weight_capacity

11. obusforme-comfort-high-back-chair-fabric-1240-3
    Title: "ObusForme Comfort High back Chair 1240-3"
    Brand: ObusForme Comfort (model: 1240-3)
    Missing: finishes_available, certifications, warranty, country_of_manufacture

12. round-table-42-high-bar-height
    Title: 'Round Table 42" High Bar Height'
    Brand: likely Global (Drift / Foli / Swap) or OTG bar-height tables
    Missing: product_line, model_codes, weight, weight_capacity, finishes_available

13. vion-mesh-high-back-chair-1
    Title: "VION Mesh High Back Chair"
    Brand: Global Furniture Group
    Missing: model_codes, dimensions, weight, weight_capacity
```

---

## Batch H3E — Miscellaneous (9 products)

```
BATCH: hero-batch-H3E (sub-batch of H3)

1. ibex-upholstered-seat-mesh-back-multi-tilter-1
   Title: "Ibex | Upholstered Seat & Mesh Back Multi-Tilter MVL2803"
   Brand: OTG / Offices to Go (model: MVL2803)
   Missing: weight_capacity, finishes_available, certifications, warranty, country_of_manufacture
   Note: listed in both H3A (chairs) and here for completeness; skip if already done

2. pedestal-box-box-file-with-or-without-wheels
   Title: "Pedestal - Box/Box/File (With or without wheels)"
   Brand: brand unknown — common pedestal style across OTG/Global
   Missing: weight_capacity

3. pneumatic-height-adjustable-table
   Title: "Pneumatic Height Adjustable Table"
   Brand: OTG / Offices to Go (Height Adjustable Tables)
   Missing: dimensions, weight, weight_capacity, finishes_available, warranty

4. roma-1900-nesting-chair
   Title: "Roma 1900 Nesting Chair"
   Brand: Global Furniture Group
   Missing: certifications

5. six-31-medium-back-multi-tilter-glbotg11631b
   Title: "Six 31 | Medium Back Multi-Tilter GLBOTG11631B"
   Brand: OTG / Offices to Go (GLB cross-coded SKU: GLBOTG11631B)
   Missing: weight_capacity, certifications, country_of_manufacture

6. training-flip-top-tables-1
   Title: "Training Flip Top Tables"
   Brand: brand unknown — flip-top training tables; check Global 2gether or OTG
   Missing: weight_capacity

7. u-shape-height-adjustable-desk-suite-zira
   Title: "U-Shape Height Adjustable Desk Suite Zira"
   Brand: Global Furniture Group (Zira series)
   Missing: weight, warranty

8. vertical-file-2-drawer-letter
   Title: "Vertical File 2 Drawer Letter"
   Brand: Global Furniture Group (2600 Series, model: 26-201)
   Missing: weight, weight_capacity

9. willow-bariatric-chair
   Title: "Willow Bariatric Chair"
   Brand: brand unknown — heavy-duty bariatric chair; search "Willow bariatric chair"
   Missing: certifications

10. wood-laminate-storage-cabinets
    Title: "Wood Laminate Storage cabinets"
    Brand: OTG / Offices to Go (Superior Laminate Storage Cabinet)
    Missing: weight, weight_capacity, warranty
```

---

## Output Instructions

Write results to `data/reports/hero-spec-gaps-output.json` using this format:

```json
{
  "version": "hero-spec-gaps-v1",
  "products": {
    "arlo-lounge-swivel-task-chair-1": {
      "status": "done",
      "specs": {
        "warranty": "Lifetime on frame, 5 years on mechanisms, 2 years on foam/upholstery"
      },
      "source_urls": ["https://www.officestogo.com/..."],
      "notes": ""
    }
  }
}
```

**Important:**
- Only include fields in `specs` that you are actually filling (non-empty found values).
- Do NOT include fields that already have values in specs.json.
- If a field cannot be found after thorough search, omit it.
- Use `"status": "skip"` if data cannot be found.
- Work through H3A → H3B → H3C → H3D → H3E in order; checkpoint save after every 5 products.
