# BBI Launch Readiness — Executive Summary
**Date:** 2026-05-08

---

**9 BLOCK / 13 FIX / 8 NIT — 8–10 dev days to launch + up to 14 calendar days for GSC verification**

---

## Counts

| Severity | Count |
|---|---|
| BLOCK (must fix before launch) | 9 |
| FIX (should fix before launch) | 13 |
| NIT (post-launch OK) | 8 |

## Timeline

| Metric | Value |
|---|---|
| Dev days estimate | 8–10 working days |
| Calendar days (with GSC) | 8–10 dev days + up to 14 calendar days GSC async |
| Earliest possible launch | ~2.5–3 weeks from today |

---

## Top 5 issues by severity

1. **PDP template missing (BLOCK B-1/B-2/B-6)** — 594 active products render on the stock Starlite section. No BBI design, no spec table, no trust badges, no visual colour swatches, no RFQ CTA for sold-out products. Stage 4b (PDP build) is the largest remaining build item: ~6 hours of dev. The variant picker is a text-only Starlite bug that contradicts explicit design feedback — cannot launch.

2. **SMART-1 smart collections not created (BLOCK B-3/B-4)** — All "View all [Category]" CTAs on the 9 category hub pages are dead (404). Brand pages have no "Shop [Brand] products" destination. 14 smart collections need to be created via Admin API. ~1 dev day. Easy to do, high user impact.

3. **GSC + GA4 not set up (BLOCK B-5)** — No measurement on the live site means the launch produces zero actionable SEO data. DNS TXT verification takes 5–14 calendar days — this is the calendar critical path. Start it immediately regardless of where dev work is.

4. **Wave C Shopify Page records unconfirmed (BLOCK B-8)** — 10 Wave C pages (About, Brands, Our Work, Contact, Delivery, Relocation, etc.) have template and section files in git but were built outside the worktree workflow. Their Shopify Page records and published status need a 30-minute Admin API verification pass. High probability they're fine; non-zero risk they 404.

5. **Policy pages empty (BLOCK B-9)** — No Privacy Policy, Terms of Service, Refund Policy, or Shipping Policy. A B2B site selling to Ontario institutions (OECM, PIPEDA obligations) cannot launch without these. Steve must fill these in via Admin → Settings → Policies.

---

## Locked Tn reference status

| Template | Reference locked? |
|---|---|
| T1 Homepage | ✓ DS-0 export |
| T2 Shop-All | ✓ `01-02-LOCKED-standalone.html` |
| T3 Category Hub | ✓ `01-03-LOCKED-standalone.html` |
| T4 Sub-collection | ✗ Needs Steve sign-off + capture |
| T5 PDP | ✗ BLOCKED — ds-pdp-base.liquid not built yet |
| Cart, 404, Blog, Article, RFQ Modal | ✗ BLOCKED — templates not built |

---

## Critical path bottleneck

**GSC DNS verification** — up to 14 calendar days. Start on Phase 4 day 1 (not at the end of dev). Every other BLOCK item can be resolved in 8–10 dev days. Only GSC verification can stretch the calendar timeline. Dev work and GSC verification run in parallel.

---

## Full details

→ `data/reports/stage-5-launch-audit-recommendation.md` — all 9 BLOCK + 13 FIX items with phases, prompt sketches, and effort estimates
→ `docs/plan/launch-readiness-plan-2026-05-08.md` — sequenced 8-phase launch plan
→ `data/reports/stage-5-launch-audit-*.md` — 14 individual audit reports
