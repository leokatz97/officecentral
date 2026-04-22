# Segment Analysis — Online Buyer Revenue Breakdown

**Source:** 235 Shopify orders, Oct 2024 – Apr 2026. 134 companies with company-name filled on shipping address ($336k). 67 orders ($79k) with no company name.
**Date:** 2026-04-18

---

## Revenue breakdown — named-company orders ($335,618 total)

| Segment | Revenue | % |
|---|---:|---:|
| **Institutional / non-profit** | **$194,522** | **58%** |
| &nbsp;&nbsp;Non-profit social services | $65,417 | 19% |
| &nbsp;&nbsp;First Nations / Indigenous orgs | $55,566 | 17% |
| &nbsp;&nbsp;Healthcare (FHTs, clinics, small hospitals) | $23,918 | 7% |
| &nbsp;&nbsp;Government / municipal | $22,223 | 7% |
| &nbsp;&nbsp;Religious | $17,872 | 5% |
| &nbsp;&nbsp;Education | $9,526 | 3% |
| **Private-sector SMB** | **$120,365** | **36%** |
| &nbsp;&nbsp;Manufacturing / industrial | $35,130 | 10% |
| &nbsp;&nbsp;Consulting / design firms | $24,863 | 7% |
| &nbsp;&nbsp;Services / logistics | $23,602 | 7% |
| &nbsp;&nbsp;Trades / construction | $18,002 | 5% |
| &nbsp;&nbsp;Accounting / insurance | $11,982 | 4% |
| &nbsp;&nbsp;Law | $5,384 | 2% |
| **Unknown / ambiguous** | $20,732 | 6% |

**Including the 67 orders with no company name ($79k):** total store revenue ≈ **$415k**, rolling up to roughly:
- ~50% institutional / non-profit
- ~35% SMB private-sector
- ~15% individual / sole-prop / uncategorized

---

## SMB private-sector examples missed on first pass

These showed up when we re-sorted by total spend instead of frequency. Many are one-and-done buyers — the reason they weren't visible in the top-20-by-order-count view.

**Manufacturing & industrial:** Martinrea International, CUDDY FARMS (Hendrix Genetics), KADEX Aero Supply, Schwartz Chemical, SGS Canada, Alpa Lumber, Maglin Site Furniture, EMEC Machine Tools, Upper Canada Fuels, Endicott Fuels, Diasorin Canada, Lantic Érable, RBW Corp.

**Professional services:** Goddard Gamage LLP, DickinsonWright LLP, Scargall Owen-King LLP, Garson Immigration Law, Darling Insurance, Switch Insurance, RJ Brown Insurance, Thomas Financial, ISL Insurance, BV Accounting, Michael Abramczuk CPA, Huronia Oral Surgery Group, Tiffany Leigh Designs, Jp2g Consultants (Greer Galloway), Wayfinder Corp, Key Design.

**Trades & construction:** J.R. Mechanical, Riva Plumbing, Minuk Construction, Entera Utility Contractors, Quality Engineered Homes, Black & McDonald, WJ Roofing, Conterra Foundation, Bacher Construction, Cementation Canada, Generation Mining.

**Services & logistics:** Reliance Toronto, Ryder Canada, GIGG Express, Waste Connections, Grant Custom Products.

---

## Revised ICP framing (replaces earlier "quote-only secondary")

- **Primary (~60% of revenue)** — Central Ontario institutional / non-profit, **online**. Small recurring orders, median $814.
- **Secondary (~40% of revenue)** — Ontario SMB private-sector, **also online**. Higher AOV, often one-and-done. Four sub-segments with slight tone tilts:
  - Manufacturing / industrial
  - Professional services
  - Trades / construction
  - Services / logistics
- **20% quote channel** — layered on top for very large fit-outs (>$15–25k). Not a separate ICP.

Both ICPs hold the same design-forward premium tone direction, with minor tilts documented in [icp.md](icp.md).

---

## Why the first pass misread this

Ranking companies by **order frequency** (top-20) surfaces repeat small buyers — mostly non-profits reordering chairs and task seating across a year — and buries single-purchase SMB fit-outs worth $3k–$11k. Ranking by **total spend** (or by max order size) is the more honest lens for revenue-weighted ICP work. Lesson for future analyses: always look at both the count distribution and the $-weighted distribution before calling an ICP.

---

## Data caveats

1. **Named-company classification is keyword-based**, not hand-verified for all 134 companies. Edge cases (e.g. Black & McDonald, St. Francis Advocates, CIC Canada) ended up in "unknown" — hand-review would shift a few thousand dollars between buckets but not the overall rollup.
2. **67 orders have no company name** on the shipping address. Consumer email domains (gmail/hotmail/icloud) appear on ~42 of these. Some are likely SMB owner-operators who didn't enter a company name at checkout, not true individuals. Worth a follow-up: pull their email domains and cross-reference.
3. **Order date range:** Oct 29, 2024 → Apr 15, 2026. Roughly 18 months of order history. A longer window (the `read_all_orders` scope is now active) would let us see seasonality, repeat-order rates, and churn — useful for a retention/reorder SEO angle.
