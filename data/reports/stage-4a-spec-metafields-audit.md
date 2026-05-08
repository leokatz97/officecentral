# Stage 4a — Spec Metafield State Audit

**Date:** 2026-05-07  
**Catalog size:** 594 active products  
**Source data:** `data/specs/` (100 JSON files from `lookup-specs.py`)

---

## 5a — Source Data State

### Namespace + key pattern

All spec data in `data/specs/` uses the namespace `specs` with the following keys:

| Key | Type | Example value |
|---|---|---|
| `specs.manufacturer` | `single_line_text_field` | `"OTG / Offices to Go (a division of Global Furniture Group)"` |
| `specs.product_line` | `single_line_text_field` | `"Ashmont"` |
| `specs.model_codes` | `list.single_line_text_field` (JSON array) | `["MVL2782","MVL2782F","MVL2780","MVL2781"]` |
| `specs.dimensions` | `single_line_text_field` | `"24.5\"W x 25.5\"D x 36.5\"H"` |
| `specs.weight` | `single_line_text_field` | `"38 lbs (17.2 kg)"` |
| `specs.weight_capacity` | `single_line_text_field` | `""` (often blank) |
| `specs.materials` | `multi_line_text_field` | Full text description |
| `specs.finishes_available` | `list.single_line_text_field` (JSON array) | `["Grade 1 seating textiles","LuxPlus bonded leather"]` |
| `specs.key_features` | `list.single_line_text_field` (JSON array) | `["Sled base guest chair","Oval steel tube frame",...]` |
| `specs.certifications` | `list.single_line_text_field` (JSON array) | `["BIFMA LEVEL","GREENGUARD","GREENGUARD Gold"]` |
| `specs.warranty` | `single_line_text_field` | `""` (often blank) |
| `specs.country_of_manufacture` | `single_line_text_field` | `"Canada"` |
| `specs.notes` | `multi_line_text_field` | Companion model notes (optional) |

### Sample JSON entry
```json
{
  "handle": "ashmont-medium-back-guest-chair-mvl2782",
  "title": "Ashmont | Medium Back Guest Chair MVL2782",
  "hero_rank": 20,
  "specs": {
    "confidence": "high",
    "manufacturer": "OTG / Offices to Go",
    "product_line": "Ashmont",
    "dimensions": "24.5\"W x 25.5\"D x 36.5\"H",
    "weight": "38 lbs (17.2 kg)",
    "materials": "...",
    "key_features": ["Sled base guest chair", ...],
    "certifications": ["BIFMA LEVEL", "GREENGUARD", "GREENGUARD Gold"],
    "country_of_manufacture": "Canada"
  }
}
```

### Coverage summary
- **Total spec JSON files:** 100
- **Catalog handles matched:** 93 (15.7% of 594 catalog)
- **Unmatched (handle changed or product deleted):** 7
  - `aktivity-environ-table`, `aktivity-puddle`, `auditorium-lecture-hall-seating`, `auditorium-lecture-hall-seating-my-space`, `gc-comet-bariatric-stacking-armchair-gc2180-1`, `global-recliner-primacare-gc3608mrc`, `nesting-training-table-8-colour-choices`

---

## 5b — Live Shopify State

### Sampling methodology
- 50 random products sampled from the full 594-product active catalog
- Per product: fetched `/admin/api/2024-01/products/{id}/metafields.json` and counted `specs.*` namespace keys

### Results

| Metric | Value |
|---|---|
| Products with **any** `specs.*` metafield | 5 / 50 (10% sample → ~10% of catalog) |
| Products with **5+** `specs.*` metafields | 4 / 50 (8%) |
| Products with **0** `specs.*` metafields | 45 / 50 (90%) |
| Spec count distribution | 0: 45 · 3: 1 · 7: 1 · 9: 1 · 10: 2 |

### Matched-products sub-sample
Of the 93 products that have a spec JSON file AND are in the catalog, a 10-product sub-sample shows:
- **8/10 already have spec metafields on Shopify** — a prior push-specs run has been executed
- **2/10 have 0 spec metafields** — either the push skipped them or they were added to the catalog after the push ran

**Confirmed fully-spec'd examples:**
- `ashmont-medium-back-guest-chair-mvl2782` — 10 spec metafields ✅
- `ibex-mesh-seat-back-multi-tilter-1` — 10 spec metafields (including `country_of_manufacture: Canada`) ✅
- `ashton-high-back-tilter` — 9 spec metafields ✅
- `overtime-350-high-back-heavy-duty-multi-` — 11 spec metafields ✅
- `pedestal-box-box-file-with-or-without-wh` — 11 spec metafields ✅

---

## Gap Analysis

| Gap | Size | Action |
|---|---|---|
| Spec JSON files that DON'T match any catalog handle | 7 files | Low priority — likely renamed/deleted products; skip |
| Catalog products that HAVE a spec JSON but 0 Shopify metafields | ~2/10 sub-sample = ~2 products | Re-run push-specs script on matched handles |
| Catalog products with NO spec JSON at all | 594 - 93 = 501 products (84.3%) | Large gap; `lookup-specs.py` would need ~5 more batches of ~100 to cover Hero tier products |

---

## Spec Push Strategy Recommendation

**Immediate action (Stage 4):** Re-run `push-specs.py` (or equivalent) on the 93 matched handles. This is the cheapest win — data exists locally, ~2 products need re-push. Estimated effort: 10 minutes.

**Phase 2 (post-Stage-4):** Run `lookup-specs.py` on the next priority tier of products (Hero-rank products without specs). The `data/specs/` source already covers ~93 products; expanding coverage to the full catalog requires web lookups for each product.

**Liquid rendering note:** `key_features`, `certifications`, `model_codes`, and `finishes_available` are stored as JSON arrays. The Liquid template must handle both array types (`list.single_line_text_field` iterates directly in Liquid) and the raw JSON string fallback.

---

## `country_of_manufacture` as Trust Signal

Multiple products with spec metafields have `specs.country_of_manufacture = Canada`. This field could drive the Canadian-made badge on the PDP without needing a product tag — a reliable fallback until the tagging pass (Phase 6) runs. Confirmed on: Ashmont, Ibex multi-tilter, and likely other ergoCentric-line chairs.
