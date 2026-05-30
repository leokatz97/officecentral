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
