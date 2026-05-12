# Hero Spec Gap — Master Session Instructions

## Purpose

Fill missing spec fields for the **Hero 100** products in `data/specs.json`.
These products are BBI's top-priority listings. Every blank spec field hurts PDP quality and SEO.
Your job as researcher: find the true, accurate value for each blank field from manufacturer websites, spec sheets, or trusted product databases.

---

## Ground Rules

1. **Never overwrite an existing value.** If a field already has a value, leave it alone. Only fill blank fields.
2. **Researcher mode only.** This is not a copywriting session. Fill spec fields accurately with real product data — no marketing language, no invented values.
3. **If you cannot find a value with high confidence, leave the field out of your output** — do not guess. A missing field is better than a wrong one.
4. **Respect cultural context.** The `medicine-wheel-table-indigenous` is a specialized cultural/ceremonial table. Research it carefully and respectfully.
5. **`installation1000` is a service SKU, not a product.** Mark it `"status": "service"` and include no spec fields. Skip all research for it.
6. **Commit checkpoint every 5 products.** After completing 5 products, write your output to `data/reports/hero-spec-gaps-output.json` (merge with existing content), then continue.

---

## Input Files

- **`data/specs.json`** — current product data. Each key is a product handle. The `specs` sub-object shows current spec values. Empty string `""`, empty array `[]`, or missing key = blank field.
- **`data/reports/hero-spec-gaps-output.json`** — already-completed products from prior sessions. **Skip any handle already present in this file** — do not re-research or re-write it.

### How to read specs.json

```json
{
  "some-handle": {
    "handle": "some-handle",
    "title": "Product Title",
    "hero_rank": 42,
    "brand_hint": "Global / OTG",
    "specs": {
      "manufacturer": "Global Total Office",
      "product_line": "",          // <-- blank, needs filling
      "model_codes": [],           // <-- blank list, needs filling
      "dimensions": "24\"W x 48\"D x 30\"H",
      "weight": "",               // <-- blank
      "weight_capacity": "250 lbs",
      "materials": "",            // <-- blank
      "finishes_available": [],
      "key_features": ["Height adjustable"],
      "certifications": [],
      "warranty": "",
      "country_of_manufacture": ""
    }
  }
}
```

---

## The 12 Spec Fields

| Field | Type | Notes |
|---|---|---|
| `manufacturer` | string | Full legal brand name |
| `product_line` | string | Product series/line name |
| `model_codes` | list | SKU / model numbers (e.g. `["SA-81-3016"]`) |
| `dimensions` | string | W × D × H, imperial preferred (e.g. `"24\"W x 48\"D x 29.5\"H"`) |
| `weight` | string | Shipping or product weight (e.g. `"43 lbs"`) |
| `weight_capacity` | string | Max load (e.g. `"250 lbs"`) |
| `materials` | string | Primary construction materials (e.g. `"Steel frame, laminate top"`) |
| `finishes_available` | list | Colour/finish options (e.g. `["Black", "Grey", "Walnut"]`) |
| `key_features` | list | 3–6 bullet-point product features |
| `certifications` | list | e.g. `["BIFMA", "GREENGUARD Gold", "CARB2"]` |
| `warranty` | string | e.g. `"Lifetime on frame, 2 years on parts"` |
| `country_of_manufacture` | string | e.g. `"Canada"`, `"USA"`, `"China"` |

---

## Research Strategy (per product)

1. Check `brand_hint` in the product record to identify the manufacturer.
2. Search manufacturer website + Google for model numbers and spec sheets.
3. Use the product `title` to narrow your search if model codes are unknown.
4. For Canadian brands (Global, Teknion, ergoCentric, Keilhauer, OTG/Offices to Go, Newland): check Canadian distributor pages and brand .ca sites first.
5. For accessories (casters, mats, air purifiers): check brand pages like Fellowes, Casters & Wheels suppliers, Fellowes AeraMax docs.
6. For outdoor furniture: check municipal/commercial furnishings suppliers.
7. Record the source URLs in `source_urls` so Leo can verify.

---

## Output Format

Write completed products to `data/reports/hero-spec-gaps-output.json`.

The file structure is:
```json
{
  "version": "hero-spec-gaps-v1",
  "products": {
    "some-handle": {
      "status": "done",
      "specs": {
        "field_name": "value",
        "list_field": ["item1", "item2"]
      },
      "source_urls": ["https://..."],
      "notes": "Optional — e.g. 'No weight capacity published by manufacturer'"
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

### Status values
- `"done"` — researched successfully, spec fields filled
- `"skip"` — product exists but no data could be found after thorough search
- `"service"` — service line item (installation1000), no specs apply

---

## Product Card Format (show Leo)

When presenting a completed product, use this format in the session chat:

```
[DONE] arlo-lounge-swivel-task-chair-1
  Title: Arlo | Lounge Swivel Task Chair
  Filled: warranty
  Source: https://www.officestogo.com/...
  Notes: —
```

---

## Merge Script

After a session, Leo runs:
```bash
python3 scripts/merge-hero-specs.py          # dry run first
python3 scripts/merge-hero-specs.py --live   # apply changes
```

The script reads `data/reports/hero-spec-gaps-output.json` and merges non-empty fields into `data/specs.json` without overwriting any existing values.

---

## Batch Files

Session batches are in this directory:
- `hero-batch-H1A.md` — 12 fully-empty products (desks/tables/workstations)
- `hero-batch-H1B.md` — 11 fully-empty products (remaining)
- `hero-batch-H2.md` — 19 products with 5+ missing findable fields
- `hero-batch-H3.md` — ~27 products with 1–4 missing findable fields

Each batch file is a self-contained session starter. Paste the block into a new Claude session to begin.
