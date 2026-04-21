# Tier 2 Disposition — Steve's Review

_Generated 2026-04-20T11:58:48+00:00 from 613 active products._

## What this is

Steve — before we touch anything on the store, here's the proposed disposition for every active product.
Four buckets:

- **archive** — ghost / placeholder SKU. Hidden from storefront, preserved in admin.
- **clearance** — never sold but real product. Moves to a dedicated Clearance / Last Chance collection at **10% off**. Keeps the URL live, preserves SEO, gives buyers a reason to browse, and turns some of the dead stock into revenue.
- **keep-live-quote** — sold-out, $0-price, or showcase page. Stays live but only shows a "Request a Quote" button (no transaction).
- **keep-live** — sold in last 18 months, OR a strategic brand line we keep visible regardless of sales.

**Nothing has been changed yet.** This is the proposal. Open the CSV ([data/tier-2-disposition-review.csv](../data/tier-2-disposition-review.csv)), mark any rows you disagree with, and send back.

## Totals

| Action | Count |
|---|---:|
| archive | 1 |
| clearance | 394 |
| keep-live-quote | 42 |
| keep-live | 176 |
| **Total active** | **613** |

## Breakdown by product type

| Type | Archive | Clearance | Keep-Live-Quote | Keep-Live | Total |
|---|---:|---:|---:|---:|---:|
| Accessories | 0 | 53 | 4 | 6 | 63 |
| Chairs | 0 | 84 | 12 | 88 | 184 |
| Desks | 0 | 58 | 2 | 19 | 79 |
| Lounge | 0 | 5 | 1 | 4 | 10 |
| Other | 1 | 64 | 13 | 16 | 94 |
| Outdoor | 0 | 1 | 3 | 1 | 5 |
| Storage | 0 | 56 | 4 | 22 | 82 |
| Tables | 0 | 73 | 3 | 20 | 96 |

## Why each row was placed (rule applied)

| Rule | Count | What it means |
|---|---:|---|
| sold | 131 | Has sold ≥1 unit in the last 18 months. Untouched. |
| strategic-brand | 45 | Brand line we protect even with zero sales (OTG, Basics, Concorde, etc.). |
| sold-out | 15 | All variants out of stock. Stays live with quote button. |
| $0-showcase | 27 | No price set, real product. Stays live with quote button. |
| showcase-brand | 0 | Known manufacturer showcase page (Teknion / Ryno / Auditorium). |
| junk | 1 | Ghost SKU or placeholder — not a real product. Archive. |
| never-sold | 394 | Real product, has price + image, never sold, no strategic protection. Move to Clearance at 10% off. |

## Proposed new collection structure

Three facets, every kept product tagged on all three. Implemented as automated tag-based collections.

**By Product Type** — Chairs · Desks · Tables · Storage · Accessories · Lounge · Outdoor

**By Room** — Private Office · Boardroom · Reception · Open Plan · Training Room · Break Room · Lounge

**By Industry** — Health Centres · Schools · Government · First Nations Organizations · Engineering Firms · Non-Profits

Tag proposals are in the CSV column `proposed_tags`. Industry tags are mostly blank — those'll be a manual pass after this CSV is approved.

## Sign-off

☐ Steve has reviewed the CSV and the bucket counts above.
☐ Steve has noted any rows to flip (comment in CSV or list back).
☐ Approved → run `apply-tier2-archives.py` + `apply-tier2-tags.py` + `build-tier2-collections.py` + `build-tier2-redirects.py`.