# Other Collection — Classification Worksheet for Steve

**Generated:** 20260527-083821
**Source:** office-central-online.myshopify.com → collection "Other" (id=527013085497)
**Total products to classify:** 338
**Estimated time:** ~113 minutes (338 × ~20 sec/product)

---

## What this is

These 338 products live in a catch-all "Other" collection on the Brant
Business Interiors site. They're invisible to the main category nav and
underweighted in search until they're classified into real sub-collections
with proper brand + product type metadata.

Your job: for each row, fill in **brand**, **product type**, and **1-3
sub-collections** so we can graduate the product into the main catalog.

---

## How to open the file

1. Open `other-collection-products-20260527-083821.csv` in **Google Sheets** (easiest):
   - File → Import → Upload → select the CSV
   - "Replace spreadsheet", separator type "Comma"
2. Freeze the header row: View → Freeze → 1 row
3. Open `other-collection-picklists-20260527-083821.csv` in a second tab — that's
   your lookup sheet for valid values.

---

## Column-by-column guide

### Reference columns (DO NOT EDIT — for context only)

| Column | What it is |
|---|---|
| product_id, handle, title | Product identity |
| admin_url | Click to view in Shopify Admin |
| storefront_url | Click to view live on brantbusinessinteriors.com |
| current_vendor / product_type / tags | What's already on the product (may be blank or wrong) |
| status | active / draft / archived |
| variant_count | How many SKUs the product has |
| price_min / price_max | Variant price range in CAD |
| primary_image_url | Click to view the product photo |
| body_excerpt | First 400 chars of the product description |
| created_at | Date added to the store |

### Steve-fills columns

| Column | What to put | Notes |
|---|---|---|
| **new_brand** | Brand name | Pick from BRANDS list in picklist file. Top 5: OTG / Offices to Go (75), Global Furniture Group (74), Brant Business Interiors (35), Heartwood Manufacturing Ltd. (28), Fellowes (8). New brands OK — just type it and Leo will confirm. |
| **new_product_type** | Product category | Pick from PRODUCT_TYPES list. Top 5: Avis-add-charge (4), Service (2), Sound dampeners (1). New types OK. |
| **new_sub_collection_1** | Primary collection **handle** | Use the `handle` column from SUB_COLLECTIONS picklist (e.g. `seating`, not `Seating`). Required if you want it routed somewhere. |
| **new_sub_collection_2** | Optional second collection handle | Many products fit multiple collections. Leave blank if not. |
| **new_sub_collection_3** | Optional third collection handle | Same. |
| **additional_tags** | Comma-separated extra tags | Optional. E.g. `canadian-made, oecm-eligible, ergonomic`. Top sub-collections to consider: 24 Hour (Seating), Accessories, Accessories, Acoustic Panels, Acoustic Pods. |
| **leave_in_other** | Y or blank | Y = doesn't belong anywhere specific, keep in Other. Skip the rest of the row. |
| **archive_this** | Y or blank | Y = discontinued, remove from store. Skip the rest of the row. |
| **notes_for_leo** | Free text | Anything you want Leo to look at manually. |

**Mutual exclusion:** don't set both `leave_in_other` and `archive_this`
to Y on the same row. Don't classify (fill new_brand etc.) on a row
flagged as `leave_in_other` or `archive_this`.

---

## When you're done

1. File → Download → Comma-separated values (.csv)
2. Email back to Leo (leo@venn.ca)
3. Leo runs the ingest script to write your classifications into Shopify

---

## Quick stats on what's in here

- Active: 338  |  Draft: 0  |  Archived: 0
- No image: 2
- Blank vendor: 0
- Blank product type: 332

If you hit anything unclear, ping Leo before guessing.
