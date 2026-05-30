# specs.* field framework — verified session 1 (PR #60)

13 fields render on PDP (theme wires 15 but 2 are unused in practice).

## Renders on PDP — spec table (12 fields)

| Field | Data shape | Notes |
|---|---|---|
| specs.manufacturer | single_line_text_field | Manufacturer name |
| specs.product_line | single_line_text_field | Product line/family (e.g. "Concorde") |
| specs.model_codes | list (JSON array) | Renders via join: ', '. Multi-model parenthetical: "2670-4 (High Back)" |
| specs.dimensions | single_line_text_field | Single line; seat-height range inline (e.g. 23"–33") |
| specs.weight | single_line_text_field | e.g. "46 lbs" |
| specs.weight_capacity | single_line_text_field | e.g. "300 lbs" |
| specs.materials | multi_line_text_field | newline_to_br; one material per line |
| specs.finishes_available | list (JSON array) | Comma-joined render |
| specs.key_features | list (JSON array) | Bullet-joined render |
| specs.certifications | list (JSON array) | Comma-joined render |
| specs.warranty | single_line_text_field | e.g. "Limited Lifetime Warranty" |
| specs.country_of_manufacture | single_line_text_field | Renders under label "Made In" |

## Renders on PDP — About section (1 field)

| Field | Data shape | Notes |
|---|---|---|
| specs.who_its_for | single_line_text_field | Renders in About / audience section |

## RETIRED — theme-wired but never populated/rendered on live products

- specs.tagline — DROP from drafting (decision: do not populate)
- specs.standfirst — DROP from drafting (decision: do not populate)

## body_html convention

- Theme splits at first `<h3>`: everything before first `<h3>` renders as lede; everything from first `<h3>` onward renders below the spec table
- Keep full body_html (SEO retains the full content); the split is render-only

## SEO conventions

- product.seo.title: format "{Manufacturer} {Product} | Brant Business Interiors" (≤60 chars total)
- product.seo.description: ≤160 chars; institutional-buyer hook
- Featured image alt text: descriptive, not keyword-stuffed
