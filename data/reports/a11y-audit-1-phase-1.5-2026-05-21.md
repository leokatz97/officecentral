# A11Y-AUDIT-1 Phase 1.5 — PSI re-run

_2026-05-21 · Read-only · Step 50 follow-up · Google PageSpeed Insights API v5 (authenticated)._


> **AUDIT TARGET: LIVE Avada theme** (`brantbusinessinteriors.com`), not BBI Landing Dev.
> The PSI API cannot reach `?preview_theme_id=…` URLs without an active Shopify admin
> session, so Phase 1.5 retargets the LIVE domain — same scope-limitation as Phase 1.
> Authoritative *new-theme* scores come from **Phase 2 after LAUNCH-2**, when BBI Landing
> Dev is published. These Phase 1.5 numbers measure the **bar being replaced** after the
> Wave E content + schema work landed.

---

## Audit context

- URLs audited: **15** (homepage, OECM, Industries hub, 5 industry pages, 4 system pages, 3 brand pages, 2 collection pages)
- Strategies: **mobile + desktop** = 30 PSI runs
- Categories: Performance, Accessibility, Best Practices, SEO (all four enabled per run)
- API key: authenticated via `PSI_API_KEY` (added to `.env`)
- Errors: 0 / 30 (1 transient 500 retried successfully)

## Summary — averages

| Category | Mobile | Desktop |
|---|---:|---:|
| Performance     | 58.3  | 82.9 |
| Accessibility   | **97.7** | **94.7** |
| Best Practices  | 93.1    | 94.4 |
| SEO             | 94.7   | 94.7 |

**Aggregate 4-category mobile average: 85.9** (vs Phase 1 baseline 63, performance-only).

## Comparison to Phase 1 baseline (2026-05-14)

Phase 1 sampled 10 URLs (mobile, performance category only), avg Lighthouse 63, with all 10 LCP >4000ms.
Phase 1.5 sampled 15 URLs (mobile + desktop, all 4 categories).

| Metric | Phase 1 (mobile, 10 URLs) | Phase 1.5 (mobile, 15 URLs) | Δ |
|---|---:|---:|---:|
| Avg Performance | 63 | **58.3** | -4.7 |
| URLs with LCP > 4 000ms | 10 / 10 | **15 / 15** | — |
| URLs with CLS < 0.1 (good) | 10 / 10 | **15 / 15** | — |
| URLs with TBT ≥ 600ms | 2 / 10 | **2 / 15** | — |

**Verdict:** Mobile Performance is statistically unchanged from Phase 1 — the LIVE Avada
theme is still slow, and Wave E (content + schema work) did **not** regress performance.
That's expected: Wave E shipped *copy and JSON-LD* on the new theme, none of which is
served on the LIVE domain yet. **Mobile Accessibility on the LIVE Avada theme is
surprisingly strong (97.7).** Desktop Performance (82.9) is healthy
because LCP imagery loads from the Shopify CDN with desktop bandwidth.

## Per-URL results

Mobile shown by default; CWV icons: LCP ✅ <2.5s 🟡 2.5–4s 🔴 >4s · CLS ✅ <0.1 🟡 <0.25 🔴 ≥0.25 · TBT ✅ <200 🟡 <600 🔴 ≥600

| # | URL | Strategy | Perf | A11y | BP | SEO | LCP | CLS | TBT |
|---:|---|:--|---:|---:|---:|---:|---:|---:|---:|
| 01 | `/` (Homepage) | mobile  | 58 🟡 | 98 ✅ | 96 ✅ | 100 ✅ | 9,976 🔴 | 0.0 ✅ | 430 🟡 |
|   |   | desktop | 80 ✅ | 95 ✅ | 96 ✅ | 100 ✅ | 2,042 ✅ | 0.001 ✅ | 251 🟡 |
| 02 | `/pages/oecm` (OECM) | mobile  | 63 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 4,801 🔴 | 0 ✅ | 575 🟡 |
|   |   | desktop | 89 ✅ | 95 ✅ | 96 ✅ | 92 ✅ | 1,158 ✅ | 0.0 ✅ | 231 🟡 |
| 03 | `/pages/industries` (Industries-Hub) | mobile  | 54 🟡 | 98 ✅ | 92 ✅ | 100 ✅ | 13,782 🔴 | 0 ✅ | 345 🟡 |
|   |   | desktop | 60 🟡 | 95 ✅ | 96 ✅ | 100 ✅ | 1,467 ✅ | 0.0 ✅ | 970 🔴 |
| 04 | `/pages/healthcare` (Healthcare) | mobile  | 58 🟡 | 98 ✅ | 92 ✅ | 100 ✅ | 13,768 🔴 | 0 ✅ | 145 ✅ |
|   |   | desktop | 96 ✅ | 95 ✅ | 96 ✅ | 100 ✅ | 1,158 ✅ | 0.0 ✅ | 119 ✅ |
| 05 | `/pages/education` (Education) | mobile  | 55 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 14,130 🔴 | 0 ✅ | 316 🟡 |
|   |   | desktop | 95 ✅ | 95 ✅ | 92 ✅ | 92 ✅ | 1,127 ✅ | 0.0 ✅ | 137 ✅ |
| 06 | `/pages/government` (Government) | mobile  | 50 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 13,987 🔴 | 0 ✅ | 482 🟡 |
|   |   | desktop | 71 🟡 | 95 ✅ | 96 ✅ | 92 ✅ | 1,130 ✅ | 0.005 ✅ | 806 🔴 |
| 07 | `/pages/quote` (Quote) | mobile  | 45 🔴 | 98 ✅ | 96 ✅ | 100 ✅ | 12,877 🔴 | 0 ✅ | 681 🔴 |
|   |   | desktop | 81 ✅ | 95 ✅ | 96 ✅ | 100 ✅ | 1,119 ✅ | 0.001 ✅ | 387 🟡 |
| 08 | `/pages/delivery` (Delivery) | mobile  | 57 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 13,853 🔴 | 0 ✅ | 196 ✅ |
|   |   | desktop | 98 ✅ | 95 ✅ | 96 ✅ | 92 ✅ | 1,081 ✅ | 0.0 ✅ | 61 ✅ |
| 09 | `/pages/design-services` (Design-Services) | mobile  | 60 🟡 | 98 ✅ | 92 ✅ | 100 ✅ | 9,526 🔴 | 0.001 ✅ | 255 🟡 |
|   |   | desktop | 93 ✅ | 95 ✅ | 92 ✅ | 100 ✅ | 1,081 ✅ | 0.0 ✅ | 172 ✅ |
| 10 | `/pages/customer-stories` (Customer-Stories) | mobile  | 63 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 12,187 🔴 | 0 ✅ | 113 ✅ |
|   |   | desktop | 86 ✅ | 95 ✅ | 92 ✅ | 92 ✅ | 1,020 ✅ | 0.015 ✅ | 289 🟡 |
| 11 | `/pages/brands-otg` (Brand-OTG) | mobile  | 63 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 4,651 🔴 | 0 ✅ | 717 🔴 |
|   |   | desktop | 93 ✅ | 95 ✅ | 92 ✅ | 92 ✅ | 1,201 ✅ | 0.004 ✅ | 165 ✅ |
| 12 | `/pages/brands-heartwood` (Brand-Heartwood) | mobile  | 62 🟡 | 98 ✅ | 96 ✅ | 92 ✅ | 12,008 🔴 | 0.001 ✅ | 183 ✅ |
|   |   | desktop | 90 ✅ | 95 ✅ | 96 ✅ | 92 ✅ | 1,287 ✅ | 0.0 ✅ | 187 ✅ |
| 13 | `/pages/brands-obusforme` (Brand-Obusforme) | mobile  | 54 🟡 | 98 ✅ | 92 ✅ | 92 ✅ | 13,956 🔴 | 0 ✅ | 331 🟡 |
|   |   | desktop | 68 🟡 | 95 ✅ | 96 ✅ | 92 ✅ | 1,209 ✅ | 0.005 ✅ | 866 🔴 |
| 14 | `/collections/seating` (Collection-Seating) | mobile  | 66 🟡 | 96 ✅ | 92 ✅ | 92 ✅ | 13,734 🔴 | 0 ✅ | 219 🟡 |
|   |   | desktop | 73 🟡 | 93 ✅ | 92 ✅ | 92 ✅ | 2,409 ✅ | 0.001 ✅ | 268 🟡 |
| 15 | `/collections/desks` (Collection-Desks) | mobile  | 66 🟡 | 96 ✅ | 96 ✅ | 92 ✅ | 12,519 🔴 | 0 ✅ | 195 ✅ |
|   |   | desktop | 71 🟡 | 93 ✅ | 92 ✅ | 92 ✅ | 2,153 ✅ | 0.008 ✅ | 340 🟡 |

## Below-threshold URLs (mobile)

Thresholds per CLAUDE.md: Perf ≥ 80, A11y ≥ 90, BP ≥ 90, SEO ≥ 90.

- **Performance < 80** (15 URLs): 01 Homepage (58), 02 OECM (63), 03 Industries-Hub (54), 04 Healthcare (58), 05 Education (55), 06 Government (50), 07 Quote (45), 08 Delivery (57), 09 Design-Services (60), 10 Customer-Stories (63), 11 Brand-OTG (63), 12 Brand-Heartwood (62), 13 Brand-Obusforme (54), 14 Collection-Seating (66), 15 Collection-Desks (66)
- **Accessibility ≥ 90**: ✅ all 15 URLs pass
- **Best Practices ≥ 90**: ✅ all 15 URLs pass
- **Seo ≥ 90**: ✅ all 15 URLs pass

## Worst-performing mobile URLs (top 3)

| Rank | URL | Perf | LCP | TBT | Top opportunity |
|---:|---|---:|---:|---:|---|
| 1 | `/pages/quote` (Quote) | 45 | 12,877ms | 681ms | `network-dependency-tree-insight` |
| 2 | `/pages/government` (Government) | 50 | 13,987ms | 482ms | `network-dependency-tree-insight` |
| 3 | `/pages/industries` (Industries-Hub) | 54 | 13,782ms | 345ms | `network-dependency-tree-insight` |

## Best-performing mobile URLs (top 3)

| Rank | URL | Perf | LCP | TBT |
|---:|---|---:|---:|---:|
| 1 | `/collections/desks` (Collection-Desks) | 66 | 12,519ms | 195ms |
| 2 | `/collections/seating` (Collection-Seating) | 66 | 13,734ms | 219ms |
| 3 | `/pages/brands-otg` (Brand-OTG) | 63 | 4,651ms | 717ms |

## Common performance opportunities (mobile, Lighthouse insights)

Lighthouse v12 reports performance findings as *insights* (no `overallSavingsMs` field).
Impact below = inverted insight score scaled 0–100, higher = worse.

| Opportunity | URLs | Avg impact |
|---|---:|---:|
| `network-dependency-tree-insight` | 15 / 15 | 100 |
| `forced-reflow-insight` | 13 / 15 | 100 |
| `cache-insight` | 8 / 15 | 69 |
| `legacy-javascript-insight` | 6 / 15 | 100 |
| `lcp-discovery-insight` | 3 / 15 | 100 |

## Failed accessibility audits (frequency across all 30 runs)

| Audit ID | URLs |
|---|---:|
| `heading-order` | 26 / 30 |
| `target-size` | 15 / 30 |
| `color-contrast` | 4 / 30 |

## CWV status — mobile

| Metric | Threshold | URLs passing |
|---|---|---:|
| LCP < 2 500ms | green | 0 / 15 |
| LCP < 4 000ms | yellow+green | 0 / 15 |
| CLS < 0.1     | green | 15 / 15 |
| TBT < 200ms   | green | 5 / 15 |
| TBT < 600ms   | yellow+green | 13 / 15 |

## CWV status — desktop

| Metric | Threshold | URLs passing |
|---|---|---:|
| LCP < 2 500ms | green | 15 / 15 |
| LCP < 4 000ms | yellow+green | 15 / 15 |
| CLS < 0.1     | green | 15 / 15 |
| TBT < 200ms   | green | 6 / 15 |

## Synthesis — what this means pre-LAUNCH-2

1. **No regressions from Wave E content + schema work.** Wave E shipped only on the new
   theme; LIVE Avada PSI scores match the Phase 1 baseline as expected. Nothing in Wave E
   leaked into LIVE.
2. **Mobile Performance on LIVE is still red.** Average 58, with 14/15 URLs LCP >4s. This
   is the bar the new theme needs to clear at LAUNCH-2. The dev theme uses `image_url +
   srcset + loading='lazy'` and no page-builder JS — expect 20–35pt improvement.
3. **Mobile Accessibility category score is 98 avg on LIVE — but three individual binary
   audits fail across most pages:** `heading-order` (26/30), `target-size` (15/30),
   `color-contrast` (4/30). Lighthouse's category score is high because these audits
   are weighted lightly, but they're real fixes worth confirming on the new theme.
4. **Desktop Performance is healthy (83 avg)** — desktop bandwidth + CDN imagery already
   absorb most of the Avada penalty.
5. **CLS is universally clean** — 30/30 runs <0.1. The new theme must preserve this via
   explicit `width`/`height` on every image (already enforced by `image_tag`).

## Urgent pre-LAUNCH-2 fixes

**None blocking — but two a11y items worth verifying on the new dev theme:**

1. **`heading-order` fails on 26 / 30 runs.** Lighthouse flags non-sequential heading
   levels (e.g. h2 → h4 skipping h3). On the new theme, do a spot-check on `/`, `/pages/
   oecm`, and the industry pages — confirm `ds-cc-base.liquid` and `ds-lp-*` sections
   maintain `h1 → h2 → h3` order. The category-level a11y score still rounds to ≥ 96
   because Lighthouse weights this lightly, but the new theme should fix it.
2. **`target-size` fails on 15 / 30 runs.** Some touch targets are under 24×24 CSS pixels.
   Worth checking the new theme's footer-link cluster, navigation chips, and any small
   icon-only buttons (close, share, etc.).
3. **`color-contrast` fails on 4 / 30 runs.** Less frequent — likely the Avada hero
   overlays; the new theme uses BBI tokens with vetted contrast, so this should clear.

Phase 2 (post-LAUNCH-2) will retest these against the published new theme. No theme
write is required this session — this is a read-only audit.

## Phase 2 (post-LAUNCH-2) handoff

- Re-run this exact script against `brantbusinessinteriors.com` after LAUNCH-2.
- Compare Phase 1.5 numbers (LIVE Avada) → Phase 2 numbers (LIVE new theme).
- Target: mobile Performance ≥ 80 (CLAUDE.md), Accessibility ≥ 90, BP ≥ 90, SEO ≥ 90.
- Script lives at `/tmp/a11y-audit-1/run_psi_phase_1_5.py`; copy to `scripts/` if Phase 2
  wants the runner versioned.

---
_Raw PSI dumps: `/tmp/a11y-audit-1/phase_1_5/*.json` · CSV: `data/reports/a11y-audit-1-phase-1.5-2026-05-21.csv`_
