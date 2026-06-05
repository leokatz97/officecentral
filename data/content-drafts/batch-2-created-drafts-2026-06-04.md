# Batch 2 — Created Shopify Drafts Manifest (2026-06-04)

All articles created as **UNPUBLISHED drafts (`published:false`)** on the News blog (`108557861177`) via the bbi-publish-post engine (`create-draft --live`). Each readback confirmed `published=None` (draft) and FAQ byte-match PASS. **Nothing is published.** Featured image + alt are NOT set by the API — added manually in Admin at publish time (flip-live gate enforces alt).

This run created ONLY the 5 NEW Batch-2 pages below. The 3 prior System C drafts (POI 689253155129 / atWork 689253187897 / The Office Shop 689253220665) already existed and were NOT re-created.

## SAFE pages (Wave-1 branch `feature/batch-2-wave1-pilot-2026-06-04`, PR #106) — normal publish flow later

| Page | Article ID | Handle | Draft URL | published |
|---|---|---|---|---|
| Office Furniture in Toronto, Ontario (geo) | 689253384505 | office-furniture-toronto-ontario | /blogs/news/office-furniture-toronto-ontario | false |
| Office Furniture in Ottawa, Ontario (geo) | 689253417273 | office-furniture-ottawa-ontario | /blogs/news/office-furniture-ottawa-ontario | false |
| Top Commercial Office Furniture Suppliers in Ontario (roundup) | 689253450041 | commercial-office-furniture-suppliers-ontario | /blogs/news/commercial-office-furniture-suppliers-ontario | false |

Roundup carries a **light-legal-glance** flag before flip-live (factual/neutral competitor descriptions, no superiority claim).

## SYSTEM C pages (branch `content-batch2-systemC-alternatives-2026-06-04`, PR #108) — LEGAL-GATED, DO NOT PUBLISH

| Page | Article ID | Handle | Draft URL | published |
|---|---|---|---|---|
| Best Alternative to Staples Office Furniture (Ontario) | (recorded on the System C branch PACK) | staples-office-furniture-alternative-ontario | /blogs/news/staples-office-furniture-alternative-ontario | false |
| Best Alternative to Grand & Toy Office Furniture (Ontario) | (recorded on the System C branch PACK) | grand-and-toy-office-furniture-alternative-ontario | /blogs/news/grand-and-toy-office-furniture-alternative-ontario | false |

System C drafts (Staples, Grand & Toy, plus the 3 prior POI/atWork/Office Shop) stay `published:false` until a lawyer + Steve sign off on the named-competitor framing. Then publish ONE first (POI) and watch before the rest. Staples + Grand & Toy are marked HIGHER-ENFORCEMENT-RISK targets.

## DESIGN/SEGMENT pages (branch `content-batch2-design-segment-2026-06-04`) — normal publish flow later

6 NET-NEW drafts created as **UNPUBLISHED (`published:false`, `published_at=None`)** on the News blog (`108557861177`) via `create-draft --live` on 2026-06-04. Each readback confirmed draft + FAQ byte-match PASS + SEO title_tag/description_tag set (all meta <=155). Nothing published. Featured image + alt added in Admin at publish (flip-live enforces alt). All product/page interlinks verified storefront-200; all SKUs distinct from the Wave-1 geo/manufacturer/roundup drafts.

| Post | Type | Article ID | Handle | Draft URL | published |
|---|---|---|---|---|---|
| Office Space Planning Guide for Ontario Businesses | design/space-planning | 689254302009 | office-space-planning-guide-ontario | /blogs/news/office-space-planning-guide-ontario | false |
| How Much Office Space Do You Need Per Employee? | design/space-planning | 689254334777 | how-much-office-space-do-you-need | /blogs/news/how-much-office-space-do-you-need | false |
| Office Fit-Out and Renovation Guide for Ontario | design/space-planning | 689254367545 | office-fit-out-renovation-guide-ontario | /blogs/news/office-fit-out-renovation-guide-ontario | false |
| Designing for Hybrid and Activity-Based Work | design/space-planning | 689254400313 | hybrid-activity-based-work-office-design | /blogs/news/hybrid-activity-based-work-office-design | false |
| Office Furniture for Ontario Law Firms | segment guide | 689254433081 | office-furniture-ontario-law-firms | /blogs/news/office-furniture-ontario-law-firms | false |
| Medical and Dental Clinic Furniture in Ontario | segment guide | 689254498617 | medical-dental-clinic-furniture-ontario | /blogs/news/medical-dental-clinic-furniture-ontario | false |

These 6 are SAFE pattern (no System-C legal gate). Before flip-live each still needs: Leo voice pass, featured image + alt in Admin, Steve sign-off, then `flip-live --spec PACK.json --live`, then build-state row + Cowork reconcile. Same normal publish flow as the Wave-1 SAFE pages.
