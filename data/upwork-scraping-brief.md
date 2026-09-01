# Upwork Scraping Brief — BBI Product Enrichment

## The Job in One Paragraph

Brant Business Interiors (**brantbasics.com**) is a Canadian office-furniture e-commerce store with 614 active products on Shopify. Most products are missing critical spec fields (material, style, suitable location, etc.) that the site needs for filtered search, product detail pages, and Google Shopping. Your job is to go through the provided CSV row-by-row, look up each product on the manufacturer's website (pre-filled for you), and fill in the missing fields using **only the approved values listed below**.

**Estimated effort:** ~614 products. A skilled scraper should be able to complete 15-25 products/hour. Budget 25-40 hours.

---

## What You'll Receive

| File | Purpose |
|---|---|
| `url-enrichment-template.csv` | **The main file — one row per product. You fill it in.** |
| `sku-prefix-manufacturers.csv` | SKU prefix → manufacturer + website lookup (already applied in main file) |
| `product-variants-reference.csv` | Per-variant detail (all SKUs + size/colour options) — reference only |
| `enriched-pilot.csv` | Example of a completed row — use as your quality target |
| `metafield-vocabulary.md` | Full list of accepted values for each field |

---

## Workflow Per Product

For each row in `url-enrichment-template.csv`:

1. **Read the row's `RepSKU`** (or pick any one from `AllSKUs`)
2. **Visit `ManufacturerWebsite`** (already filled in) and search for the SKU
3. If the manufacturer site doesn't have it, try Google:
   - Google the `RepSKU` directly
   - Fallback sites: **poi.ca**, **sourceofficefurniture.com**, **grandandtoy.com**
4. Find the product's spec sheet / product detail page
5. **Fill these columns:**
   - `URL1` — the direct URL of the product page you used
   - `URL2` *(optional)* — a second source (useful if URL1 is weak)
6. **Fill the enrichment columns** (Type, Color, Material, Style, etc.) using **only the approved values** in `metafield-vocabulary.md`
7. Leave `N/A` in any column that doesn't apply to that product's category
8. If no suitable source exists, put `NO_SOURCE` in the Notes column and leave enrichment columns blank

---

## Approved Values (CRITICAL — see `metafield-vocabulary.md` for full list)

These are Shopify's controlled vocabulary. **Anything else will be rejected at import.** Use lowercase, hyphens (no spaces), semicolons `;` for multi-value.

**Type:** `Chairs & Stools` · `Desks` · `Tables` · `File Cabinets` · `Storage Cabinets` · `Bookcases & Shelves` · `Workstations` · `Sofas` · `Benches`

**Color:** `black` · `brown` · `white` · `gray` · `beige` · `blue` · `green` · `silver` · `yellow` · `orange` · `red` · `multicolor`

**Material (high-level):** `metal` · `wood` · `plastic` · `aluminum` · `rubber`

**Style:** `modern` · `traditional` · `industrial` · `contemporary` · `transitional` · `scandinavian`

**Suitable Location:** `office` · `home-office` · `living-room` · `bedroom` · `dining-room` · `kitchen` · `storage-room` · `outdoor`

**Furniture/Fixture Material (detailed):** `metal` · `steel` · `aluminum` · `wood` · `maple-wood` · `oak-wood` · `walnut-wood` · `plastic` · `fabric` · `mesh` · `leather` · `faux-leather` · `polyester` · `nylon` · `foam` · `glass` · `polyurethane-pu` · `vinyl` · `particle-board` · `medium-density-fiberboard-mdf` · `melamine` · `fiber-reinforced-plastic-frp`

**Upholstery Material (chairs/sofas only):** `leatherette` · `vinyl` · `polyester` · `nylon` · `faux-leather` · `leather` · `polyurethane-pu` · `velvet` · `mesh`

**Seat Type (chairs only):** `upholstered` · `hard` · `upholstered-padded` · `flat` · `nest` · `bucket-cradle`

**Back Type (chairs only):** `backless` · `full-back` · `low-back` · `mid-back` · `high-back`

**Backrest Type (chairs only):** `hard` · `upholstered` · `upholstered-padded` · `mesh`

**Wood Finish (desks/tables with wood):** `walnut` · `oak` · `maple` · `cherry` · `mahogany` · `espresso` · `white-oak` · `natural-oak`

---

## Rules / Edge Cases

1. **Never invent values.** If you can't find it on a real source page, leave it blank.
2. **Skip service rows.** Anything with "Installation", "Delivery", "Dismantle" in the title is not a real product — put `SERVICE` in Notes and leave enrichment blank.
3. **SKU isn't matching?** Try the product title + manufacturer. If still nothing, note `NO_SOURCE` and move on.
4. **Multiple variants (size/colour)?** Scrape the product family page — one source URL covers all variants. Colors go in the `Color` column semicolon-separated (e.g. `black; white; gray`).
5. **Body HTML / SEO fields are OPTIONAL for this pass.** Focus on the structured metafields first.
6. **Keep a log.** At the end of each work session, note in the CSV's `Notes` column anything confusing or inconsistent.

---

## Priority Order

The CSV is pre-sorted by revenue tier. Work **top-to-bottom** — don't skip around.

- Rows 1-22 → **Tier A** (highest-revenue — be most careful here)
- Rows 23-55 → Tier B
- Rows 56-109 → Tier C
- Rows 110-614 → Tier D (zero sales since 2023 — still enrich, but quality bar is lower)

---

## Quality Check

Before final delivery:
- [ ] Every row has `URL1` filled (or Notes=NO_SOURCE/SERVICE)
- [ ] Every value matches the approved vocabulary exactly (case, hyphens, spelling)
- [ ] No free text in controlled-vocab columns
- [ ] Spot-check 10 random rows against the source URL to confirm accuracy

Return the filled CSV. Any row marked `NO_SOURCE` or `SERVICE` will be handled separately.

---

## Contact

Questions? Reply in the Upwork thread. Leo Katz — brantbasics.com
