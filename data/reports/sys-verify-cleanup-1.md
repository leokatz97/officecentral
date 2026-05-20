# SYS-VERIFY-CLEANUP-1 — Consolidated cleanup of SYS-VERIFY-1 Phase 1 findings
_Date: 2026-05-20 · Session: SYS-VERIFY-CLEANUP-1_

## Summary

Closed 8 of the SYS-VERIFY-1 Phase 1 findings in one session. **15 pages unpublished** on LIVE, **34 redirects modified/created**, and DEV `settings_data.json` favicon cleared.

Backup: `data/backups/sys-verify-cleanup-1-pre-20260520-100715/` (local, gitignored)

## Closed findings

### ✅ C2 — Quote pages consolidation
- Canonical kept: `/pages/quote` (id 170512023865, updated 2026-05-05)
- 4 stale duplicates unpublished + 301-redirected → `/pages/quote`:
  - `/pages/request-for-quote` (id 149494104377)
  - `/pages/quote-history` (id 149494137145)
  - `/pages/sb-request-quote` (id 162925019449)
  - `/pages/history-quotes` (id 166903841081)

### ✅ C3 — Legacy HTML sitemap pages
6 pages unpublished (no redirects — Shopify auto-generates `/sitemap.xml`):
- `/pages/html-sitemap`, `-articles`, `-blogs`, `-collections`, `-pages`, `-products`

### ✅ C4 — `/pages/please-click-below` resolution
- Destination chosen: **`/pages/our-work`** (project portfolio — semantic match for "look books" and "space division" inbound)
- 3 inbound redirects updated:
  - `/pages/space-division` → `/pages/our-work`
  - `/pages/look-books` → `/pages/our-work`
  - `/pages/https-books-indeal-org-...` → `/pages/our-work`
- `/pages/please-click-below` unpublished + final fallback redirect created → `/pages/our-work`

### ✅ S1 — Root-dump redirects repointed
12 of 21 root-target redirects repointed to category collections. Remaining 9 kept as `/` (admin probes, account paths, junk paths, non-BBI inventory).
- 4 → `/collections/desks`
- 4 → `/collections/storage`
- 4 → `/collections/seating`
- 1 → `/collections/boardroom`

### ✅ S2 — Redirect chains flattened
18 chains flattened to single-hop. Intermediate redirects left intact (safer — may be referenced elsewhere).
- 12 Obusforme chains → `obusforme-comfort-high-back-chair-fabric-1240-3`
- 4 collection consolidations (benching→desks, castors→seating, dorm-furniture→business-furniture, kids-couches→business-furniture, quiet-rooms→accessories, end-tab→storage)
- 2 dead-ends to `/collections/all#seogid...` (best available)

### ✅ S3 — Duplicate FAQ + shipping pages
- `/pages/frequently-asked-questions` unpublished + 301 → `/pages/faq`
- `/pages/shipping-delivery` unpublished + 301 → `/pages/delivery`

### ✅ S6 — Placeholder pages
- `/pages/llms-txt` unpublished (no redirect — meant to be `/llms.txt` static file)
- `/pages/search-results-page` unpublished (no redirect — real search uses `/search?q=`)

### ✅ S7 — DEV `settings_data.json` product image leakage
Audit found **1** suspect chrome-surface reference: `current.favicon` pointed at `shopify://shop_images/DFE_MVL11860_JN07_Side_generated.jpg` (Stradic chair render).
- Fix: favicon cleared to empty string. Shopify default until Steve uploads a real square BBI mark.
- No other chrome surfaces (share image, OG, logo) had product image leakage.

## Spot-check verification (live)
| URL | Status | Redirects to |
|---|---|---|
| `/pages/request-for-quote` | 301 | `/pages/quote` ✅ |
| `/pages/html-sitemap` | 404 | (unpublished) ✅ |
| `/roma-1900-nesting-chair` | 301 | `/collections/seating` ✅ |
| `/collections/benching` | 301 | `/collections/desks` ✅ |
| `/pages/please-click-below` | 301 | `/pages/our-work` ✅ |

## Operation totals
- Pages unpublished: **15** (4 quote + 6 sitemap + 1 please-click-below + 2 FAQ/shipping + 2 placeholder)
- Redirects updated: **33** (3 please-click-below inbound + 12 root-dump + 18 chain flattens)
- Redirects created: **7** (4 quote 301s + 1 please-click-below final + 2 FAQ/shipping 301s)
- DEV `settings_data.json`: favicon cleared

## Remaining from SYS-VERIFY-1 Phase 1
- **C1 favicon** — Steve homework (upload square BBI mark to Files, set on DEV Customize)
- **S4 `/pages/contact` refresh** — Steve homework or BRAND-PAGES-1
- **S5 cart Request-a-Quote CTA** — folds into BRAND-PAGES-1

## Next session candidates
- BRAND-PAGES-1 (Step 25)
- A11Y critical fixes
