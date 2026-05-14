# PERF-AUDIT-1 Baseline
_2026-05-14 · Read-only · Step ~30. DEV theme preview URLs (186373570873)._

> **STATUS: AUDIT QUEUED — API UNAVAILABLE**
> Both measurement APIs failed during this session (see §API Failure Log below).
> All 10 URLs are staged and ready. Re-run using Chrome DevTools Lighthouse
> (instructions below) or wait for PSI API quota reset (resets daily at midnight PT).

---

## Summary

- URLs staged: 10 (mobile strategy, DEV theme preview)
- Average Lighthouse score: N/A — no data collected
- PASS-GOOD (≥ 90): —
- PASS-OK (75–89): —
- WARN (50–74): —
- FAIL (< 50): —
- **Pre-launch posture: UNKNOWN** — audit must complete before LAUNCH-0 gate

---

## URLs to audit

All URLs target DEV theme `186373570873` via `?preview_theme_id=186373570873`.
**Note:** Preview URLs require an active Shopify admin session in the browser.
For Chrome DevTools Lighthouse: log into admin.shopify.com first, then run Lighthouse
from DevTools > Lighthouse tab on each URL below.

| # | URL | Template type |
|---|-----|---------------|
| 1 | `https://www.brantbusinessinteriors.com/?preview_theme_id=186373570873` | index (homepage) |
| 2 | `https://www.brantbusinessinteriors.com/pages/about?preview_theme_id=186373570873` | page.about |
| 3 | `https://www.brantbusinessinteriors.com/pages/contact?preview_theme_id=186373570873` | page.contact |
| 4 | `https://www.brantbusinessinteriors.com/pages/our-work?preview_theme_id=186373570873` | page.our-work (12 photos) |
| 5 | `https://www.brantbusinessinteriors.com/pages/oecm?preview_theme_id=186373570873` | page.oecm (AI citation target) |
| 6 | `https://www.brantbusinessinteriors.com/pages/quote?preview_theme_id=186373570873` | page.quote |
| 7 | `https://www.brantbusinessinteriors.com/collections/seating?preview_theme_id=186373570873` | collection.category (largest active) |
| 8 | `https://www.brantbusinessinteriors.com/collections/desks?preview_theme_id=186373570873` | collection.category |
| 9 | `https://www.brantbusinessinteriors.com/collections/business-furniture?preview_theme_id=186373570873` | collection.business-furniture (582 products) |
| 10 | `https://www.brantbusinessinteriors.com/products/l-shape-desk-3-sizes-13-colours?preview_theme_id=186373570873` | product (PDP — in-stock, multi-variant) |

---

## API failure log

Two measurement methods were attempted and both failed:

### 1. DataForSEO `on_page_lighthouse` MCP tool
- **Result:** `HTTP error! status: 403` on every URL, including `www.brantbusinessinteriors.com/` (live, no preview param)
- **Root cause:** The DataForSEO account plan does not include the `on_page/lighthouse` endpoint. The 403 is from DataForSEO's API, not from Shopify.
- **Fix:** Upgrade DataForSEO plan to include OnPage Lighthouse, or use a different tool.

### 2. Google PageSpeed Insights API (free tier, no API key)
- **Result:** `HTTP Error 429 — Quota exceeded for quota metric 'Queries' and limit 'Queries per day'`
- **Root cause:** The free PSI API quota (project_number: 583797351490) is exhausted for today. `quota_limit_value: 0` indicates the free-tier daily quota is fully consumed.
- **Fix:** Wait until midnight PT for quota reset, OR provision a Google Cloud API key with a higher PSI quota.

### 3. Preview URL accessibility
- **Finding:** DEV theme preview URLs (`?preview_theme_id=186373570873`) require an active Shopify admin browser session. External crawlers (DataForSEO, PSI API) cannot access them.
- **Implication:** Even with working API credentials, automated remote Lighthouse against the dev theme preview would fail. Chrome DevTools Lighthouse (run from an authenticated browser session) is the correct tool for DEV theme auditing.
- **Post-launch alternative:** Once BBI Landing Dev is published as the live theme (LAUNCH-2), all standard automated tools will work against the live URLs without authentication.

---

## Re-run instructions (Chrome DevTools)

1. Log into `admin.shopify.com/store/office-central-online`
2. Open Chrome DevTools > Lighthouse tab
3. Settings: Mode = Navigation, Device = Mobile, Categories = Performance only
4. For each URL in the table above: paste URL → Analyze page load
5. Record: Performance score, LCP, CLS, TBT, FID (Max Potential FID)
6. Copy scores into `data/reports/perf-audit-2026-05-14.csv` replacing `NO-DATA` values
7. Classify per the PERF-AUDIT-1 rubric:
   - PASS-GOOD: score ≥ 90, all CWVs green
   - PASS-OK: score 75–89, no red metrics
   - WARN: score 50–74, or one metric yellow
   - FAIL: score < 50, or LCP > 4000ms / CLS > 0.25 / INP > 500ms
8. Update `classification` column and `top_opportunity_*` columns from Lighthouse Opportunities section
9. Re-commit: `git add data/reports/perf-audit-2026-05-14.{csv,md} && git commit -m "PERF-AUDIT-1 (rerun): populate metrics from Chrome DevTools Lighthouse"`

**Estimated time:** ~25–35 min for 10 URLs.

---

## Per-URL results

_No data collected — see re-run instructions above._

---

## Common opportunities

_No data collected._

---

## Pre-launch performance posture

**Unknown.** The audit could not run due to API unavailability and preview URL authentication requirements.

**Known performance risk factors to watch during manual rerun:**

| Risk | Affected templates | Why |
|------|-------------------|-----|
| Image weight — `/pages/our-work` | page.our-work | 12 OCI photos recently uploaded; no lazy-load verification done |
| JS payload — all BBI pages | All | `bbi-nav.liquid` loads megamenu JS + Web Component; `bbi-quote-modal.liquid` loads `<dialog>` + Shopify contact form on every gated page |
| Product grid image count — collections | collection.*, index | `/collections/business-furniture` surfaces 582 active products; even paginated, each card loads an image |
| PDP gallery — full-res images | product | `ds-pdp-base.liquid` loads all product images for the lightbox; large image arrays may inflate LCP |
| Shopify preview injection | All dev-theme URLs | Dev theme preview injects `preview_bar.js` and related scripts not present on live theme — expect 5–15 point lower scores vs post-launch live audit |

**Recommendation:** Run the manual Chrome DevTools audit before marking PERF-AUDIT-1 ✅ in the build state. The CLAUDE.md target is Lighthouse performance ≥ 80 on mobile for all new features. If homepage or `/collections/business-furniture` fall below 60 in the manual run, escalate as a pre-launch blocker.

---

## Note on DEV vs LIVE

DEV theme (186373570873) is unpublished and served behind Shopify's preview mechanism. Preview URLs inject `preview_bar.js` and additional Shopify editor scripts not present on the published theme. Expect DEV theme scores to run 5–15 points lower than a post-launch audit of the same pages on LIVE. Re-run against `brantbusinessinteriors.com` (without `?preview_theme_id`) after LAUNCH-2 for authoritative Core Web Vitals metrics.
