# Metafield Vocabulary — Accepted Values

Every value below is from Shopify's controlled taxonomy. **Anything else will fail on import.** Use lowercase, hyphens, semicolons to separate multiple values.

---

## Type (product_type)
One value per product.

- `Chairs & Stools`
- `Desks`
- `Tables`
- `File Cabinets`
- `Storage Cabinets`
- `Bookcases & Shelves`
- `Workstations`
- `Sofas`
- `Benches`

## Color
Multiple values allowed. Separate with `; `.

`black` · `brown` · `white` · `gray` · `beige` · `blue` · `green` · `silver` · `yellow` · `orange` · `red` · `multicolor`

*Example:* `black; white` for a two-tone product.

## Material (high-level)
Multiple values allowed.

`metal` · `wood` · `plastic` · `aluminum` · `rubber`

*Example:* `wood; metal` for a laminate desk with steel frame.

## Style
One value per product.

`modern` · `traditional` · `industrial` · `contemporary` · `transitional` · `scandinavian`

## Suitable Location
Multiple values allowed.

`office` · `home-office` · `living-room` · `bedroom` · `dining-room` · `kitchen` · `storage-room` · `outdoor`

*Default for office furniture:* `office; home-office`

## Furniture/Fixture Material (detailed)
Multiple values allowed. More granular than the "Material" field — use this to describe exactly what the product is made of.

- **Metals:** `metal` · `steel` · `aluminum`
- **Woods:** `wood` · `maple-wood` · `oak-wood` · `walnut-wood`
- **Composites:** `particle-board` · `medium-density-fiberboard-mdf` · `melamine` · `fiber-reinforced-plastic-frp`
- **Soft:** `fabric` · `mesh` · `leather` · `faux-leather` · `polyester` · `nylon` · `foam` · `vinyl` · `polyurethane-pu`
- **Other:** `plastic` · `glass`

*Example:* `steel; melamine` for a laminate desk. `mesh; metal; polyester` for a task chair.

## Upholstery Material
Chairs and sofas only. Multiple allowed.

`leatherette` · `vinyl` · `polyester` · `nylon` · `faux-leather` · `leather` · `polyurethane-pu` · `velvet` · `mesh`

## Seat Type
Chairs and stools only. One value (usually).

`upholstered` · `hard` · `upholstered-padded` · `flat` · `nest` · `bucket-cradle`

## Back Type
Chairs only. One value.

`backless` · `full-back` · `low-back` · `mid-back` · `high-back`

## Backrest Type
Chairs only. One value. (This overlaps with Seat Type — fill both.)

`hard` · `upholstered` · `upholstered-padded` · `mesh`

## Wood Finish
Desks and tables with a wood/laminate surface. Multiple allowed.

`walnut` · `oak` · `maple` · `cherry` · `mahogany` · `espresso` · `white-oak` · `natural-oak`

## Tabletop Color
Desks and tables. Use values from the Color field above.

## Leg Color
Desks, tables, chairs. Use values from the Color field above.

---

# Mapping Source Page Text → Approved Values

Source pages will use non-standard words. Here's how to translate:

| You see on source | Map to |
|---|---|
| "Bonded Leather" | `leatherette` (upholstery) or `faux-leather` |
| "Eco Leather" / "Vegan Leather" | `faux-leather` |
| "Mesh back" | `mesh` |
| "Chrome" / "Stainless Steel" | `steel` |
| "Contemporary" / "Modern" | pick whichever fits; if both, default to `modern` |
| "High-Pressure Laminate" / "HPL" / "Thermofused Laminate" / "TFL" | `melamine` + `medium-density-fiberboard-mdf` |
| "Walnut finish" / "Dark Walnut" / "Winter Wood" | `walnut-wood` (material) and `walnut` (finish) |
| "Oak" / "Natural Oak" / "Lite Oak" | `oak-wood` and `oak` or `natural-oak` |
| "Espresso" / "Dark Cherry" | `walnut-wood` (material) and `espresso` or `cherry` (finish) |
| "Foam-padded cushion" | seat type = `upholstered-padded` |
| "Sled base" | `steel` in Furniture/Fixture Material |
| "Polypropylene seat" | `plastic` in Material |
