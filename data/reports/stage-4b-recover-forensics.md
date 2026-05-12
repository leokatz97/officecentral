# Stage 4b Recovery — Change-Window Forensics
_Generated: 2026-05-08_

## Timeline of Recent Script Activity (last 14 days)

| Date | Script/Log | What it touched | Status/Published_at changes? |
|---|---|---|---|
| 2026-04-25 | sharpen-page-images | 29 product images | No |
| 2026-04-28 | **archive-non-biz-products --live** | **27 products archived, 2 unpublished, 15 collections unpublished** | **YES — root cause** |
| 2026-04-29–05-04 | push-img2img (batches 01–08) | Product images | No |
| 2026-05-04 | pe7-seo-push | SEO meta on 495 products | No |
| 2026-05-04 | pe3-tm-strip-push | Title cleanup on 42 products | No |
| 2026-05-04 | pe2-push | Spec metafields on 77 products | No |
| 2026-05-06 | migrate-smart | Collection template suffixes | No |
| 2026-05-06–07 | set-sub-suffix | Collection template suffixes | No |
| 2026-05-07 | set-parent-metafields | Collection metafields | No |
| 2026-05-07 | set-canonical-suffix/metafields | Collection suffixes + metafields | No |
| 2026-05-08 | pe2-push | Spec metafields on 75 products | No |

## Root Cause: commit `3dfc495` on 2026-04-28

```
Execute PB-1, PB-2, PB-4: archive sector products + collections, redirects live
```

**Script:** `scripts/archive-non-biz-products.py --live`  
**Input:** `data/reports/sector-products-disposition-2026-04-28.csv`  
**Effect:**
- 27 products → `status: archived` (zero sales history; educational, healthcare, institutional categories)
- 2 products → `published_at: null` (active status kept; had sold-history)
- 15 sector collections → `published_at: null` (unpublished from storefront)
- **No log file saved** (likely run outside repo or log was deleted; no `data/logs/archive-sector-*.json` found)

**This was deliberate**, planned as PB-1 (29 products), PB-2 (15 collections), PB-4 (redirects).  
The sector cleanup scoped BBI to business-furniture-only, retiring educational/healthcare/institutional SKUs.

## Scripts That Write Product Status

The following scripts can mutate product status or published_at:

| Script | What it can do |
|---|---|
| `scripts/archive-non-biz-products.py` | `status=archived` or `published=False` from CSV disposition |
| `scripts/archive-drafts.py` | `status=archived` on all draft products |
| `scripts/consolidate-shipping.py` | `status=archived` on specific shipping SKUs |
| `scripts/retire-services.py` | `published_at=null` to hide service/fee products |

No stage-3.2c.x scripts (template_suffix/metafields) touch product status.  
No pe2/pe7/pe3 scripts touch product status.

## Unexplained UNPUBLISHes (2 products)

Two products went from `published=true` (Apr 21) to `published_at=null` (today) outside the sector CSV:

| Handle | Tags | Notes |
|---|---|---|
| solid-steel-shelving-starter-set | type:storage, industry:business | No audit trail; likely unpublished via Shopify Admin |
| monitor-arms | type:accessories, industry:business | No audit trail; likely unpublished via Shopify Admin |

These are active products with no sales channel. Could be Steve manually hiding them, an app conflict, or a Shopify Admin bulk action.

## Git Commits Touching Scripts / Collection Templates (last 14 days)

| Commit | Date | Files |
|---|---|---|
| 9187497 | recent | data/reports/stage-4a-* (read-only reports) |
| 81693ff | recent | scripts/set-canonical-subcollection-metafields.py |
| d3eb79c | recent | scripts/set-canonical-subcollection-suffix.py |
| ae0e367 | recent | scripts/set-collection-parent-metafields.py |
| 70ba12c | recent | theme/sections/ds-cs-base.liquid |
| 4df4211 | recent | theme/templates/collection.tables.json |

None of these touched product status, published_at, or collection membership.
