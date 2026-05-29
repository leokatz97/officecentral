# BBI Product Enrichment Brief
**Brant Business Interiors — April 2026**

---

## Goal
Enrich all 646 Shopify products so every page can match the quality of a site like effydesk.com:
- Clean title + feature badges
- "Get to Know" intro paragraph
- Specs & Dimensions table
- "Explore Further" bullets
- Care tips + Considerations
- 4–6 lifestyle images per product
- SEO title + meta description

---

## The Tool
**File:** `Office Central/previews/hero-100-lookup.html`
Open in any browser. All 646 products pre-loaded. Notes auto-save to localStorage.

**Filters that matter most:**
- Filter by flag → start with `no-desc` (13 products with no description at all)
- Filter by flag → `no-img` (12 products with zero images)
- Filter by flag → `zero-price` (29 products at $0 — decide: quote-only or archive)
- Filter by flag → `unpublished` (41 draft products — decide what to publish)

---

## Data Quality Snapshot

| Issue | Count | Priority |
|---|---|---|
| No product type set | 632 / 646 | LOW — inferred from tags |
| No SEO title/desc | 75 | HIGH — affects search |
| No SKU on any variant | 72 | MEDIUM |
| Only 1 image | 330 | HIGH — hurts conversion |
| No images at all | 12 | CRITICAL |
| $0 price | 29 | HIGH — broken checkout |
| No description | 13 | CRITICAL |
| Unpublished | 41 | REVIEW — publish or archive |

---

## What to Fill Per Product (fields in the tool)

### Identity
- **Brand / Manufacturer** — Global, Teknion, ObusForme, ergoCentric, etc.
- **Product Line** — Zira, Overtime 350, Ibex, etc.
- **Model Code / SKU** — the manufacturer part number
- **Feature Badges** — 2–4 chips shown at top of page (e.g. "Bestseller, Height Adjustable, BIFMA Certified")

### Specs & Dimensions (for the specs table)
- Dimensions (W × D × H)
- Height range (if adjustable)
- Weight capacity
- Product weight
- Materials / Finishes
- Warranty
- Certifications (BIFMA, Greenguard, ANSI)
- Any other specs (motor type, lifting speed, noise level, etc.)

### Description Copy
- **"Get to Know" paragraph** — 2–3 sentences, benefit-driven, conversational
- **"Explore Further" bullets** — 2–4 feature callouts
- **Product Care Tips** — 3–5 one-liners (avoid X, use Y)
- **Considerations** — buying guide context (Space Requirements, Adjustability, Material & Style)

### SEO
- **SEO Title** — 50–60 chars, keyword-first
- **SEO Description** — 140–155 chars, includes key spec + CTA

---

## Where to Scrape Specs

| Brand | Source |
|---|---|
| Global Furniture Group | globalfurnituregroup.com/products |
| ObusForme | obusforme.com |
| Teknion | teknion.com |
| ergoCentric | ergocentric.com |
| Offices To Go (OTG) | officestogo.com |
| Keilhauer | keilhauer.com |
| Kimball | kimball.com |
| Mayline | mayline.com |
| Competitor reference | abcoffice.com, poifurniture.com, grandtoy.com |

For each product: find the manufacturer page → copy dims, weight cap, warranty, certifications → paste into the tool → Export CSV when done → re-upload to Shopify.

---

## Prioritization Order

1. **Published products with revenue** (top of list in tool, sorted by price)
2. **Products with no description** (filter: no-desc)
3. **Products with no/few images** (filter: no-img or 1-img)
4. **Products with $0 price** (filter: zero-price) — decide quote vs. archive
5. **Draft products** (filter: unpublished) — publish or archive

---

## Export → Re-upload Flow

1. Fill enrichment data in the tool
2. Click **Export CSV** → downloads `bbi-products-enriched.csv`
3. Hand to Claude: "Use this enrichment CSV to update the Shopify products export and re-upload"
4. Claude maps fields → updates Body HTML, SEO fields, metafields, re-formats for Shopify import

---

*Tool built April 2026. Notes persist in browser localStorage — don't clear browser data.*
