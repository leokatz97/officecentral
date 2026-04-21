# BBI Shopify — Status Snapshot
**Date:** April 20, 2026

---

## Done ✅

**Tier 1 — Backend / Foundation (100% complete)**
- Liquid `divided by 0` bug fixed and pushed live
- Checkout tested end-to-end (desktop + mobile)
- 645 products scanned: no 404s; 9 ™/® handles renamed + redirect CSV uploaded via Shopify Admin → Navigation → URL Redirects → Import
- 11 service pseudo-products unpublished
- Site-wide floating "Request a Quote" button live
- Sold-out + $0-price variants → Request a Quote CTA (not Sold Out button)
- Announcement bar: 1-800-835-9565 visible on every page
- Payment methods verified ($65.7K across 56 paid orders)
- Tax rates audited (50/50 orders match ON 13% HST, BC 12%, AB 5%, SK 11%)
- Delivery + Installation 7-tier shipping rate live and incognito-tested
- Order confirmation emails verified (35/35 recent orders)
- Admin notification verified (sales@brantbusinessinteriors.com, 50/50 orders)

**Tier 2 — Catalog & Taxonomy (infrastructure complete; enrichment in progress)**
- 613-row tag CSV built + approved by Steve (2026-04-20)
- 584/613 products tagged: `type:*`, `room:*`, `industry:*`
- 14 automated collections built (7 by type, 7 by room) + velocity sort pushed
- Industry tags pushed: 574 products (541 business, 14 educational, 14 healthcare, 5 daycare)
- Main nav rebuilt: 8 top-level items, "Other Industries" + "Outdoor (Coming Soon)" removed
- "Keep every product live" strategy locked — no archive, no clearance
- Phase 0 branding locked in `docs/icp.md` (2026-04-20)
- Phase 1.0 Hero 100 built + Steve signed off (2026-04-20)
- Phase 1.3 Layer A confirmed clean — 0 legacy tags across all 645 products
- Phase 2.2 Breadcrumbs live (collection template + BreadcrumbList JSON-LD)
- Phase 3.2 Link audit complete — all nav + footer links return 200

---

## In Progress 🔄

**Phase 1.1 Spec lookup**
- `lookup-specs.py` running in background session (Claude Sonnet 4.6 + web search)
- 14/100 done when last checked · ~$4 of $15 budget spent
- Output: `data/specs/{handle}.json` per product → aggregated to `data/specs.json`

---

## Blocked ⛔

| Item | Blocked by |
|------|-----------|
| Phase 1.2 (normalize titles) | 1.1 spec lookup complete |
| Phase 1.3 Layer B (rich filter tags) | 1.1 spec lookup complete |
| Phase 2.1 (collection filters) | Layer B tags pushed |
| Phase 3.1 (sitemap resubmit to GSC) | W0-1 GSC setup |
| All Wave 1 content | W0-1 GSC setup |
| Tier 9 design overhaul | Full stack should be live first |

---

## Leo's Manual Tasks (unblocked)

1. **W0-1: Set up Google Search Console + GA4** — zero SEO progress measurable without this. (~30 min)
2. **W0-2: Create BBI Google Business Profile** — no GBP exists. (~30 min)

---

## Open Questions for Steve

1. **"Outdoor Coming Soon"** in the main nav — removed from Healthcare dropdown; confirm nothing else to clean up.
2. **Phase 1.1 specs**: review `data/specs.json` when lookup-specs.py finishes — flag any low-confidence entries before titles are normalized.
