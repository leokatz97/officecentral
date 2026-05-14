# PERF-AUDIT-1 Baseline
_2026-05-14 · Read-only · Step ~30. Mobile strategy. Google PageSpeed Insights API v5._

> **IMPORTANT — LIVE THEME, NOT DEV THEME**
> The dev theme preview (186373570873) requires an active Shopify admin browser session.
> External crawlers including the PSI API cannot access `?preview_theme_id=…` URLs without
> that session. These scores reflect the **current LIVE theme (Avada)**, not BBI Landing Dev.
> They are a valid pre-launch baseline: they show what we're replacing and where the bar sits.
> Re-run against the live domain post-LAUNCH-2 for authoritative "new theme" metrics.

---

## Summary

- URLs audited: 10 (mobile strategy, live theme — Avada)
- Average Lighthouse score: 63
- PASS-GOOD (≥ 90): 0
- PASS-OK (75–89): 0
- WARN (50–74 score, no red CWVs): 0
- **FAIL: 10 / 10** — every URL has LCP > 4 000 ms (red Core Web Vital)

**Pre-launch posture: the current live site is underperforming on mobile.** The new BBI
Landing Dev theme should do better — it uses lazy-loading, `image_url` with explicit widths,
and no Avada plugin bloat — but a post-launch rerun is needed to confirm.

---

## Per-URL results

| # | URL | Score | LCP (ms) | FID (ms) | CLS | TBT (ms) | Classification |
|---|-----|------:|----------:|---------:|----:|---------:|---------------|
| 1 | `/` (homepage) | 62 | 10 506 🔴 | 145 | 0.000 ✅ | 324 | FAIL |
| 2 | `/pages/about` | 61 | 11 557 🔴 | 146 | 0.001 ✅ | 243 | FAIL |
| 3 | `/pages/contact` | 74 | 5 783 🔴 | 114 | 0.000 ✅ | 149 | FAIL |
| 4 | `/pages/our-work` | 66 | 4 501 🔴 | 217 🟡 | 0.000 ✅ | 539 | FAIL |
| 5 | `/pages/oecm` | 68 | 5 610 🔴 | 154 | 0.000 ✅ | 317 | FAIL |
| 6 | `/pages/quote` | 74 | 4 801 🔴 | 185 | 0.000 ✅ | 258 | FAIL |
| 7 | `/collections/seating` | 60 | 12 512 🔴 | 138 | 0.040 ✅ | 319 | FAIL |
| 8 | `/collections/desks` | 50 | 11 872 🔴 | 240 🟡 | 0.040 ✅ | 682 | FAIL |
| 9 | `/collections/business-furniture` | 55 | 12 224 🔴 | 286 🟡 | 0.000 ✅ | 515 | FAIL |
| 10 | `/products/l-shape-desk-3-sizes-13-colours` (PDP) | 64 | 12 518 🔴 | 108 | 0.036 ✅ | 186 | FAIL |

CWV thresholds: LCP 🔴 > 4 000ms / 🟡 2 500–4 000ms / ✅ < 2 500ms · CLS 🔴 > 0.25 / ✅ < 0.1 · FID/INP 🔴 > 500ms / 🟡 200–500ms

---

## Common opportunities

Across all 10 audited URLs (Lighthouse Opportunities section):

| Opportunity | URLs affected | Priority |
|-------------|:-------------:|---------|
| **Reduce unused JavaScript** | 8 / 10 | 🔴 High — theme-wide JS audit candidate |
| **Reduce unused CSS** | 5 / 10 | 🟡 Medium — CSS purge / per-page splitting |

**"Reduce unused JavaScript"** is the single dominant finding — it appears on 8 of 10 pages and
is almost certainly Avada's plugin stack (page builder JS, sliders, WooCommerce compat, etc.)
loading on every page regardless of use. The BBI Landing Dev theme loads only the JS it needs
per template; this should eliminate most of this penalty.

**LCP is the critical failure point site-wide.** All 10 URLs exceed 4 000 ms on mobile. The
fastest is `/pages/contact` at 5 783 ms; the worst is the PDP at 12 518 ms. The root causes
on the current live site are likely: large unoptimized hero images, Avada's render-blocking JS,
no lazy-loading discipline, and no Shopify CDN `image_url` width hints.

**CLS is healthy.** All 10 pages score below 0.1 — no layout shift issues. This is a positive
signal; the new theme's explicit image dimensions should maintain this.

**FID (Max Potential FID) is acceptable on most pages.** Three pages show yellow (200–500ms):
`/pages/our-work` (217ms), `/collections/desks` (240ms), `/collections/business-furniture`
(286ms). None are in the red (> 500ms). The new theme's vanilla JS + Web Components approach
should improve this further.

---

## Pre-launch performance posture

**Current live site: not launch-ready by CLAUDE.md standard (mobile Lighthouse ≥ 80).**
Average score is 63; no page scores above 74. All 10 fail the LCP Core Web Vital.

**This is expected for the old Avada theme and is exactly why we built BBI Landing Dev.**

For the new theme (BBI Landing Dev 186373570873), the key differentiators to verify post-launch:

| Factor | Old live (Avada) | New dev theme expectation |
|--------|-----------------|--------------------------|
| JS payload | Avada page-builder + plugins | Vanilla JS + Web Components only |
| Image loading | Unoptimized, no srcset | `image_url` + `image_tag` with width + lazy |
| LCP element | Unknown hero image, no priority hints | `fetchpriority="high"` on above-fold hero |
| CSS payload | Avada full stylesheet | Per-section scoped CSS |
| CLS | ✅ Clean | Expected ✅ (explicit dimensions everywhere) |

**Worst-performing URL:** `/collections/desks` — score 50, LCP 11 872ms, TBT 682ms.
Collection pages (seating, desks, business-furniture) are the weakest cluster — likely due to
product image grids loading without lazy-load discipline on the old theme.

**Actionable pre-launch items for PERF-FIX-1 (if needed after post-launch rerun):**
1. Confirm `fetchpriority="high"` on above-fold hero images in `ds-lp-*` sections
2. Audit `ds-cs-base.liquid` product grid — ensure all below-fold card images have `loading="lazy"`
3. Consider `preload` hint for the BBI logo (renders on every page via `bbi-nav.liquid`)
4. Check `bbi-quote-modal.liquid` JS deferred (should not block LCP on first paint)

---

## Note on DEV vs LIVE

These scores reflect the **current LIVE theme (Avada)** — not BBI Landing Dev. The PSI API
runs from Google's servers without Shopify admin authentication, so the `?preview_theme_id`
parameter is ignored and the published theme is served. This is an inherent limitation of
remote Lighthouse tooling against unpublished Shopify themes.

**To audit the dev theme specifically:** Run Chrome DevTools Lighthouse while logged into
`admin.shopify.com/store/office-central-online`, then navigate to each preview URL
(`?preview_theme_id=186373570873`). Expect scores 5–15pts lower than the eventual post-launch
live audit due to `preview_bar.js` injection by Shopify's theme editor.

**Post-launch rerun:** Once BBI Landing Dev is published (LAUNCH-2), re-run this audit
against the live domain without `?preview_theme_id`. That will be the authoritative baseline
for the new theme and will close the PERF-AUDIT-1 row in Wave E.
