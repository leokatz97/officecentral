# BBI Measurement Protocols

Canonical home for measurement methodology disciplines — how to read a number
before trusting it. These protocols are referenced by name from session logs
(`bbi-build-state.md`) and should be cited whenever a session reports a
performance metric or declares a metric shifted by a change.

---

## PERFORMANCE-MEASUREMENT-DISCIPLINE

When measuring page performance on already-fast pages (LCP < 3s), single-run
Lighthouse results have ±400-500ms variance. Use multi-run median (minimum 3
runs) before declaring a change has shifted the metric. Trust architectural
correctness over single-run signals. Reference: Day 13 operational lesson 5
(single-run noise on fast pages). This discipline applies to PageSpeed Insights
mobile + desktop preset, local Lighthouse CLI, and any tool emitting Core Web
Vitals lab estimates.

### Tooling note (2026-05-30, Day 17)

- **Keyless PSI mobile API is quota-blocked** — `https://www.googleapis.com/pagespeedonline/v5/runPagespeed` returns `429 RESOURCE_EXHAUSTED` with `quota_limit_value: "0"`. A Google PSI API key is required to run mobile PSI programmatically. Without it, **Leo runs PSI mobile manually** in-browser at [pagespeed.web.dev](https://pagespeed.web.dev/) (Mobile tab) and pastes results back.
- **DataForSEO `on_page_lighthouse` (the CLAUDE.md-mandated MCP tool) runs DESKTOP-only** — `formFactor: "desktop"`, `cpuSlowdownMultiplier: 1`, no mobile/throttle param exposed. On desktop, **TBT reads ≈ 0–5 ms** → it is NOT a usable proxy for the mobile TBT we optimize for. Useful desktop signals it *does* emit: `bootup-time` (JS execution), `mainthread-work-breakdown`, `max-potential-fid`, byte weights, entity list. Always check `configSettings.formFactor` before trusting a Lighthouse number as "mobile" (repeat of the Day-13 HOTFIX-MOBILE-FRIENDLY-VERIFY-1 lesson).

### Mobile baseline reference points (regression detection)

Captured by Leo via PSI mobile (Emulated **Moto G Power**, **Slow 4G**, Lighthouse 13.3.0), 2026-05-30 (Day 17 evening, HOTFIX-MOBILE-LCP-1b). **Primary tracked metric = TBT.** Both pages already in Google's "good" (<200ms) TBT band; the waste is unused **bytes** (Avis app JS), not blocking time.

| Page | TBT runs (ms) | TBT median | LCP median | Perf | Unused-JS flagged |
|---|---|---|---|---|---|
| Homepage `/` | 80, 110 | **~95 ms** | 4.2 s | 84–85 | 334 KiB (Avis) |
| PDP `/products/global-accord-mesh-back-tilter` | 170, 190, 390 | **190 ms** | 5.0–5.4 s* | 56–73 | 287 KiB (Avis) |

\*PDP had one 12.9s LCP outlier (slow-4G image load); 5.0–5.4s typical. High TBT variance on PDP (170→390ms) — median is the trustworthy figure. Use these as the before-state when measuring AVIS-APP-SCOPE-OPTIMIZATION (expect homepage unused-JS to drop ~300 KiB) or any future mobile-perf change.
