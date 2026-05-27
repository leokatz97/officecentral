# LAUNCH-4 Phase A — Multi-browser Smoke Matrix

**Run:** 2026-05-26 evening · 5 URLs × 6 engine+viewport combos = 30 render checks.

## Critical render matrix (functional pass)

Cell `✓` = HTTP 200 + title sane + body >10kb + header logo rendered + footer present + Quote CTA visible + nav (hamburger on <1024 OR nav-links on ≥1024) + computed styles pass.

| URL                  | Chrom 1920 | Chrom 1280 | Chrom 412 (Pixel 7) | WebKit 1920 | WebKit 393 (iPhone 14) | WebKit 768 (iPad Mini) |
|----------------------|:----------:|:----------:|:-------------------:|:-----------:|:----------------------:|:----------------------:|
| `/`                  | ✓          | ✓          | ✓                   | ✓           | ✓                      | ✓                      |
| `/pages/oecm`        | ✓¹         | ✓¹         | ✓¹                  | ✓¹          | ✓¹                     | ✓¹                     |
| `/collections/seating` | ✓        | ✓          | ✓                   | ✓           | ✓                      | ✓                      |
| `/products/boardroom-table-rectangular-94-5x47-25` | ✓² | ✓² | ✓² | ✓² | ✓² | ✓² |
| `/pages/quote`       | ✓          | ✓          | ✓                   | ✓           | ✓                      | ✓                      |

**30/30 functional pass.**

Footnotes:
1. OECM page `<title>` = `OECM Office Furniture Supplier – Agreement 2025-470` — does not include the word "Brant" or "BBI" but is intentional SEO copy approved in SEO-AUDIT-1. Reclassified as PASS.
2. PDP has third-party app noise — see Known Noise §2 below. Theme renders correctly: PDP CTA `color: rgb(255,255,255)` on `bg: rgb(11,11,12)` (Fix-2 holding); logo 148×44; footer + quote CTA present.

## Production hotfix regression checks (Fix-2 + Fix-3)

| Fix | Check | Chromium | WebKit |
|---|---|---|---|
| **Fix-2: PDP CTA black-on-black** | `a.pdp-cta-closer__btn` computed color vs background | `color: rgb(255,255,255)` on `bg: rgb(11,11,12)` ✓ at all 3 viewports | same ✓ at all 3 viewports |
| **Fix-3: OECM strip pink → ink** | `.hp-oecm` computed background-color | `rgb(11, 11, 12)` ✓ at all 3 viewports | same ✓ at all 3 viewports |

Both production hotfixes are stable across every tested engine × viewport.

## Header logo dimensions (sanity)

| URL | Engine | Computed bounding box |
|---|---|---|
| Most URLs | Chromium + WebKit | 148 × 44 px ✓ |
| `/pages/quote` | Chromium + WebKit | 121 × 36 px ✓ (slightly smaller — reasonable, same logo asset) |

## Known noise (NOT theme regressions)

### 1. Shop Pay CSP frame-block (every page, every engine)

```
Framing 'https://shop.app/' violates the following Content Security Policy directive:
"frame-ancestors 'self' https://shop.app https://admin.shopify.com". The request has been blocked.
```

- **Source:** Shopify-injected `<iframe src="https://shop.app/pay/hop?...">` on every storefront page.
- **What:** Shopify tries to embed Shop Pay's frame; Shopify's own CSP refuses it because Shop Pay isn't fully enabled for our storefront.
- **Impact:** Zero. Customer never sees this — it's an invisible iframe load attempt that's silently blocked.
- **Action:** Ignore. Standard cross-Shopify behaviour. Would be the same on Avada or any theme.

### 2. `avis-options` app errors on PDPs (PDP only, every engine)

```
GET /products/undefined.js → 404
GET /products/please-select-a-finish-1.js → 404
TypeError: Cannot read properties of null (reading 'createDocumentFragment')
   at apo-product-options-v3.min.js:233:17342
```

- **Source:** Third-party Shopify app **APO Product Options v1.7.163.31** (extension UUID `019e65f2-a536-7fb3-940e-ef309ca6897f`).
- **What:** App's jQuery code tries to look up a variant-options product JSON before the page is fully wired up, hits a null DOM ref, and bails.
- **Impact:** Variant pickers and customisation options on PDPs that *use* this app may misbehave at first paint, but the boardroom table tested doesn't have those configured — the page renders fine. Pre-existing app; same behaviour on Avada.
- **Action:** Log as `AVIS-OPTIONS-APP-NOISE` in POST-LAUNCH BACKLOG. Decision item — keep, configure, or uninstall.

## Cells that fail-fast in the matrix view

None on the strict critical-render axis. 0 cells screenshot to disk (no `FAIL-*.png` produced).

## Artifacts

- `smoke.py` — 30-cell test runner (Playwright Chromium + WebKit).
- `smoke-matrix.json` — full per-cell JSON (HTTP, title, body length, logo box, footer/quote presence, nav check, computed PDP CTA + OECM bg, console + page errors).
- `diag-errors.py` + `diag-errors.json` — drill-down identifying the 401/403/404/JS error sources.
