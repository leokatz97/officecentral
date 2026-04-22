# BBI Enrichment To-Do

Work this list top-to-bottom. Each phase hands me clean data I can merge back into [products_export_1.csv](/Users/leokatz/Downloads/products_export_1.csv) without guessing.

---

## Phase 1 — Tier A (22 products, 60% of revenue) — START HERE

**File to fill:** [data/tier-a-enrichment-template.csv](tier-a-enrichment-template.csv)

One row per product, columns pre-sorted by category. For each row:

### Step 1.1 — Find the source
- [ ] Open [data/tier-a-focus.md](tier-a-focus.md) for the prioritized list
- [ ] For each handle, find a competitor or manufacturer page with the specs
  - **POI** (poi.ca) — best for most BBI chairs/desks, has PDF spec sheets
  - **ABCO / Source Office Furniture** — Canadian pricing + materials
  - **Manufacturer direct** (Global, Teknion, ergoCentric, Keilhauer, Offices to Go, OTG) — use the SKU from the title (e.g. `MVL2756`, `OTG10703B`) to find the exact PDF
  - **Grand & Toy** — fallback for generic items
- [ ] Paste the URL into the `SourceURL` column

### Step 1.2 — Fill each row
Fill only the cells that are empty. Cells pre-marked `N/A` are not applicable to that product's category — leave them as `N/A`.

**Values must follow the vocabulary below** (these are Shopify's enum values — anything else won't validate on import).

### Step 1.3 — Save the file
- [ ] Save as `data/tier-a-enriched.csv` (keep the template clean for audit)
- [ ] Tell me it's ready — I'll merge it into the main export and run a dry-validation

---

## Phase 2 — Tier B (33 products)

Only after Phase 1 is merged and pushed to Shopify.

- [ ] I'll generate `data/tier-b-enrichment-template.csv` when you're ready
- [ ] Same workflow, but you can **skip fields marked optional** — focus only on: Type, Color, Material, Style, Suitable Location, Category-specific top field (Upholstery for chairs, Wood Finish for desks)

---

## Phase 3 — Tier C (55 products)

- [ ] I'll generate a minimal `tier-c-template.csv` with only **Type + Category + Tags + short Body**
- [ ] No deep spec scraping — goal is just to get these filterable/searchable

---

## Phase 4 — Tier D (536 products, zero sales since 2023)

**Do not enrich.** These are candidates for:
- [ ] Unpublish (if showcase/catalog pages) — keep as "Request a Quote"
- [ ] Archive (if truly dead)
- [ ] Delete draft/broken (32 products currently in archived status)

I'll generate `data/tier-d-disposition.csv` after Phases 1–3 with a recommended action per product. You review, then I batch-apply via the Shopify API.

---

# Value Vocabulary (Shopify taxonomy — use exact strings)

Use semicolon `;` to separate multiple values in one cell. Match casing exactly.

### Type (Shopify product type — from Product Category taxonomy)
- `Chairs & Stools` · `Desks` · `Tables` · `File Cabinets` · `Storage Cabinets` · `Bookcases & Shelves` · `Workstations` · `Sofas` · `Benches`

### Color (most-used, lowercase)
`black` · `brown` · `white` · `gray` · `beige` · `blue` · `green` · `silver` · `yellow` · `orange` · `red` · `multicolor`
(Use `;` for multi-color: e.g. `black; white`)

### Material (high-level)
`metal` · `wood` · `plastic` · `aluminum` · `rubber`
(Use `;` for composite: e.g. `wood; metal`)

### Style
`modern` · `traditional` · `industrial` · `contemporary` · `transitional` · `scandinavian`

### Suitable Location
`office` · `home-office` · `living-room` · `bedroom` · `dining-room` · `kitchen` · `storage-room` · `outdoor`

### Furniture/Fixture Material (detailed — for spec tables)
`metal` · `steel` · `aluminum` · `wood` · `maple-wood` · `oak-wood` · `walnut-wood` · `plastic` · `fabric` · `mesh` · `leather` · `faux-leather` · `polyester` · `nylon` · `foam` · `glass` · `polyurethane-pu` · `vinyl` · `particle-board` · `medium-density-fiberboard-mdf` · `melamine` · `fiber-reinforced-plastic-frp`

### Upholstery Material (chairs/sofas only)
`leatherette` · `vinyl` · `polyester` · `nylon` · `faux-leather` · `leather` · `polyurethane-pu` · `velvet` · `mesh`

### Seat Type (chairs only)
`upholstered` · `hard` · `upholstered-padded` · `flat` · `nest` · `bucket-cradle`

### Back Type (chairs only)
`backless` · `full-back` · `low-back` · `mid-back` · `high-back`

### Backrest Type (chairs only)
`hard` · `upholstered` · `upholstered-padded` · `mesh`

### Wood Finish (desks/tables with wood)
`walnut` · `oak` · `maple` · `cherry` · `mahogany` · `espresso` · `white-oak` · `natural-oak`

---

# Body HTML — Format

Keep it simple. Leo's template per PDP:

```html
<p><strong>One-sentence value proposition.</strong> 2-3 sentence paragraph explaining the product, who it's for, and top feature.</p>

<h3>Key Features</h3>
<ul>
  <li>Feature one</li>
  <li>Feature two</li>
  <li>Feature three</li>
  <li>Feature four</li>
</ul>

<h3>Specifications</h3>
<ul>
  <li><strong>Dimensions:</strong> 60"W x 30"D x 29"H</li>
  <li><strong>Material:</strong> Laminate top, steel frame</li>
  <li><strong>Warranty:</strong> 10-year manufacturer warranty</li>
</ul>
```

Swap in actual copy. **Only fill Body_HTML** if the current Body in the export is empty or <100 chars.

---

# SEO Title / SEO Description — Format

- **SEO_Title:** `{Product Title} | Brant Business Interiors` — target ≤60 chars
- **SEO_Description:** One sentence with key feature + location anchor. Target ~155 chars. Example:
  > "Ergonomic high-back office chair with adjustable lumbar support. In-stock at Brant Business Interiors, Ontario's trusted office furniture dealer."

---

# Handoff — What happens after each phase

Once Phase 1 is filled in and saved as `tier-a-enriched.csv`:

1. I read your template and run `scripts/validate-enrichment.py` (I'll build it) to check:
   - Handles match existing products
   - Metafield values are in the controlled vocab
   - No empty required cells (except `N/A`)
2. I merge the fills into a copy of `products_export_1.csv` → `products_export_1_v2.csv`
3. I diff v1 vs v2 and show you exactly what changed (handle + fields)
4. You approve → I'll either:
   - Have you re-import v2 in Shopify Admin (Products → Import), **or**
   - Push the fields directly via the Shopify Admin API (faster, no CSV round-trip)
5. I commit `tier-a-enriched.csv`, the updated `enrichment-priorities.csv`, and the scripts to git

---

# Current file inventory

| File | Purpose |
|---|---|
| [data/enrichment-priorities.csv](enrichment-priorities.csv) | All 646 products ranked A/B/C/D |
| [data/tier-a-focus.md](tier-a-focus.md) | The 22 Tier A products with gap lists |
| [data/tier-a-enrichment-template.csv](tier-a-enrichment-template.csv) | **The file you fill in for Phase 1** |
| [data/enrichment-todo.md](enrichment-todo.md) | This document |
| scripts/build-enrichment-priorities.py | Regenerates the ranked CSV |
| scripts/build-tier-a-focus.py | Regenerates the focus markdown |
| scripts/build-enrichment-template.py | Regenerates the Tier A template |
| scripts/inspect-metafield-values.py | Pulls current vocab from the export |
