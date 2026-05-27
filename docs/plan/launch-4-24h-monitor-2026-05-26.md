# LAUNCH-4 — 24h Post-Launch Monitor Playbook

**Launch:** 2026-05-26 (Tuesday) evening · BBI theme `186373570873` → LIVE at `2026-05-26T20:08:47-04:00`.
**Owner:** Leo
**Window covered:** 2026-05-26 ~20:00 → 2026-05-27 ~20:00 (first 24 hours).
**Status when this file was written:** LAUNCH-0/1/2/3 complete + PRODUCTION-HOTFIX-1 (4 bugs) closed + multi-browser smoke 30/30 functional pass + Leo manual browser test passed.

> **Tactical doc.** For the strategic horizons (Day 2–7, Week 2–4, Day 30+) and the weekly Monday ritual, see [post-launch-monitoring.md](post-launch-monitoring.md). This file is just the first 24 hours.

---

## Section 1 — Immediate (already done as part of LAUNCH-0/1/2/3)

For reference / receipts:

- ✅ **LIVE backup confirmed on disk** — `data/backups/live-theme-pre-launch-20260526-193241/` (350 assets + MANIFEST.md, spot-check 5/5 byte-match).
- ✅ **5 critical pages smoke-tested on LIVE** — `/`, `/pages/oecm`, `/collections/seating`, a PDP, `/pages/quote` — all HTTP 200, zero Avada leakage, JSON-LD intact.
- ✅ **Lighthouse delta captured** — Avada → BBI: Perf +2/+5/+7, Best Practices +23, byte weight −82%. SEO −20 traced to Cloudflare-on-apex 403 artifact, not real regression.
- ✅ **GA4 Realtime traffic confirmed** (LAUNCH-3).
- ✅ **GSC sitemap re-submitted** (LAUNCH-3).
- ✅ **4 production hotfixes applied** — search-icon SVG geometry, defensive logo asset upload, PDP CTA black-on-black fix, OECM strip pink → ink.
- ✅ **Multi-browser smoke matrix** (LAUNCH-4 Phase A) — 5 URLs × 6 engine+viewport = 30/30 functional pass on Chromium + WebKit. Fix-2 + Fix-3 verified holding across every engine × viewport. See [data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.md](../../data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.md).
- ✅ **Leo manual browser test** (LAUNCH-4 Halt L4.1) — "browser good".

---

## Section 2 — First 24 Hours (Checks by Cadence)

### EVERY 2 HOURS (during waking hours — Wed 2026-05-27)

- [ ] **GA4 Realtime** — confirm traffic still flowing.
  https://analytics.google.com → Reports → Realtime
  Property: `G-XLCM9LCNLN`
  **Red flag:** 0 users for >1 hour during business hours (Eastern), OR a sudden cliff from typical hourly count without a corresponding marketing event.

- [ ] **Sample LIVE URL** — open https://www.brantbusinessinteriors.com, click around briefly (homepage → a collection → a PDP → /pages/quote → back).
  **Red flag:** any HTTP 500, blank page, layout break, missing image, broken CTA, or visible regression.

### MORNING (within 1 hour of waking up — Wed 2026-05-27 ~07:00–09:00)

- [ ] **GSC Coverage report** — https://search.google.com/search-console → Coverage / Pages
  **Red flag:** sudden spike in "Excluded" or "Error" pages vs Avada baseline (suggests indexing issue from theme change).
  **Tolerance:** small reshuffles (±5–10 pages in "Crawled – currently not indexed") are normal during a theme migration.

- [ ] **GA4 Acquisition report** — https://analytics.google.com → Reports → Acquisition → Traffic acquisition. Compare yesterday (full day with Avada) and this morning (BBI). Filter by hour-of-day.
  **Red flag:** <50% of typical organic traffic at the same hour vs prior week — could be either a real SERP impact or a temporary index shuffle. If still <50% at end of day, investigate.

- [ ] **Check Steve's quote-form inbox** (the email that receives form submissions).
  **Red flag:** any complaint about form not working, broken page, missing image, OR a 12+ hour silence if the form is normally getting daily traffic.

### AFTERNOON (Wed 2026-05-27 ~13:00–15:00)

- [ ] **Visit 3–5 pages on phone, hard refresh, eyeball.**
  Suggested set: `/`, `/pages/oecm`, a brand sub-page (e.g. `/pages/brands-ergocentric`), a PDP, `/pages/quote`.
  Hard-refresh on iOS Safari: pull-to-refresh from top of page; or `Cmd+R` on macOS Safari with DevTools open.
  **Red flag:** any visible regression vs last check — broken logo, layout shift, missing image, CSS not loading, color regression.

- [ ] **GA4 Events** — confirm `view_item` firing on PDPs.
  https://analytics.google.com → Reports → Engagement → Events. Look for `view_item` rows on the day's `event_count`.
  **Red flag:** `view_item` not appearing in events list 6+ hours after launch (suggests tracking code unwired).

### EVENING (Wed 2026-05-27 ~19:00–21:00)

- [ ] **GSC Search Console performance for the day** — Performance → Search results → date = today (2026-05-27). Compare impressions to the rolling 7-day average for the equivalent weekday.
  **Red flag:** impressions drop >30% vs typical Wednesday.
  **Tolerance:** 10–20% fluctuation is normal day-to-day; theme change causes a small Google re-crawl shuffle.

- [ ] **Final Realtime check before bed.** Confirm traffic still flowing into the late evening as usual.

---

## Section 3 — Red Flags That Warrant Immediate Action

### IMMEDIATE ACTION (treat as a P0 — diagnose now, rollback or hotfix if needed)

- **HTTP 500 errors on any page.** → Rollback or hotfix urgent. Diagnostic-first pattern: identify root cause before patching.
- **0 GA4 traffic for >1 hour during business hours.** → Check theme wiring (`{{ content_for_header }}` intact?), possible GA4 outage at status.google.com, possible DNS / CDN issue at status.shopify.com.
- **Customer complaint about a specific bug.** → Triage. Reproduce empirically via Playwright before patching. Same flow as the 4 PRODUCTION-HOTFIX-1 fixes earlier today.
- **GSC sends a "Mobile usability" or "Core Web Vitals" error notification.** → Fix promptly; these are surfaced to ranking signals.
- **Visible design regression** (e.g. another black-on-black, pink reappearing on `.hp-oecm`, broken logo) → Hotfix using same diagnostic-first pattern as today.

### WORTH NOTING BUT NOT IMMEDIATE

- Slight ranking fluctuations in GSC (normal for theme change — Google re-crawls + re-evaluates).
- Lighthouse score variations <5 points (normal CDN variability; the +23 Best Practices uplift is already in the bank).
- GA4 traffic at 60–90% of typical (normal post-launch SERP shuffle; revisit at Day 7).
- The `avis-options` app errors flagged in the multi-browser smoke (third-party app, not theme — backlog item `AVIS-OPTIONS-APP-NOISE`).

### IGNORE FOR NOW

- Bing / Yandex indexing speed differences (normal — they crawl slower than Google).
- Pinterest / Slack / LinkedIn link-preview rendering (deferred to Week 1 social validation pass).
- Backlink count changes (lagging indicator — meaningless in first 24h).
- The recurring `shop.app/pay/hop` CSP frame-block in DevTools console (standard Shopify-wide behaviour, identified during LAUNCH-4 Phase A — not a real error).

---

## Section 4 — Rollback Procedure (if needed)

### Path A — Shopify Admin (recommended; what Steve would do)

1. Open Shopify Admin → **Online Store → Themes**.
2. Find the "BBI Live" theme (Avada) — currently sitting as **unpublished** in the theme library, theme ID `178274435385`. (Visually it's the older theme card with "Last published 2026-05-26" timestamp.)
3. Click `...` → **Publish**.
4. Shopify makes Avada `main`; BBI theme `186373570873` becomes `unpublished`.
5. `brantbusinessinteriors.com` reverts to Avada within ~30 seconds (CDN cache may extend to a couple of minutes for some pages).

### Path B — Claude Code via Admin API (faster; no Shopify Admin UI needed)

```bash
export $(grep -v '^#' .env | xargs) && curl -X PUT \
  "https://office-central-online.myshopify.com/admin/api/2026-04/themes/178274435385.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"theme": {"role": "main"}}'
```

Expected response: `HTTP 200` with `"role": "main"` on theme `178274435385`. Verify the swap with:

```bash
export $(grep -v '^#' .env | xargs) && python3 -c "
import urllib.request, json, os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
for name, tid in [('CHECK-1', '186373570873'), ('CHECK-2', '178274435385')]:
    req = urllib.request.Request(f'https://{STORE}/admin/api/2026-04/themes/{tid}.json',
        headers={'X-Shopify-Access-Token': TOKEN})
    t = json.loads(urllib.request.urlopen(req).read())['theme']
    print(f'{name}: {t[\"name\"]}  role={t[\"role\"]}')
"
```

After rollback the `main` role should sit on `178274435385` (Avada).

### Preserved on disk

- `data/backups/live-theme-pre-launch-20260526-193241/` — 350 asset files + MANIFEST.md with per-file size + restore instructions. This is a snapshot of LIVE *before* publish, in case the Avada theme in the library got corrupted somehow and needs a fresh re-upload.
- `data/backups/launch-hotfixes-pre-20260526-203227/` — pre-fix snapshots of `ds-pdp-base.liquid` + `bbi-homepage.css` (the 2 files mutated by Fix-2 + Fix-3) in case those specific hotfixes need to be unwound without touching the rest of the theme.
- `data/backups/search-icon-fix-pre-20260526-200249/bbi-nav.liquid` — pre-search-icon-fix snapshot.

### What rollback costs

- The 4 PRODUCTION-HOTFIX-1 fixes (search icon, defensive logo, PDP CTA contrast, OECM strip color) only live on BBI theme `186373570873`. A rollback to Avada `178274435385` does **not** lose them — they are still pinned on the BBI theme in unpublished state — but customers on Avada will not see them. The fixes were Avada-irrelevant anyway except the PDP CTA contrast, which is moot because Avada uses a different PDP template.
- A rollback to Avada drops the +23 Lighthouse Best Practices uplift, the 82% byte-weight reduction, and the new schema / JSON-LD. The site reverts to Avada's 3MB-per-page heaviness.
- GSC will re-crawl the rollback within 24–72 hours; no manual sitemap re-submit needed (Google will figure it out).

---

## Section 5 — 24h Done — What Next?

After 24h smoke-free + GA4 normal:

- [ ] Mark **LAUNCH-4 ✅** in `BBI-Session-Kickoff/bbi-build-state.md`.
- [ ] Move "LAUNCH-3/4 chain complete" to closed history in the build-state.
- [ ] Promote Week 1 polish items from POST-LAUNCH BACKLOG to active queue.
- [ ] Consider closing `feature/launch-chain-2026-05-26` branch + merging to `main`.

### First Week 1 priorities (from post-launch backlog)

- **GA4 quote-form event tracking** (~30 min via Claude Code) — wire `form_submit` event to the `/pages/quote` form so the conversion funnel is measurable in GA4.
- **Lead management workflow review with Steve** — quote-to-PO conversion, response SLA, who triages first.
- **Social preview validation** — LinkedIn Post Inspector + Facebook Sharing Debugger + Twitter Card Validator on the new `og-preview.png` wiring (homepage `og:image` already confirmed pointing correctly).
- **OECM strip variant for non-homepage usages** — if the canonical dark-ink OECM strip pattern needs to surface on subpages, build a reusable section variant.
- **`AVIS-OPTIONS-APP-NOISE`** — decide whether to keep, configure, or uninstall the APO Product Options app. PDP console errors are app-side, not theme-side.
- **`MOBILE-LIGHTHOUSE-MANUAL`** — DataForSEO MCP only supports desktop Lighthouse. Run mobile Lighthouse via PageSpeed Insights post-launch on the 3 sampled URLs and log scores into the build-state.
- **`APEX-DOMAIN-BOT-403`** — investigate whether to relax Cloudflare bot rules so Lighthouse scores SEO=100 cleanly instead of 80 (the 20-point hit is a measurement artifact, not a real ranking signal).
- Whatever else surfaces from the 24h monitoring window above.

---

## References

- **Strategic monitoring playbook (Day 2–7 → Day 30+):** [docs/plan/post-launch-monitoring.md](post-launch-monitoring.md)
- **Weekly Monday template:** [docs/reports/weekly-launch-monitor-template.md](../reports/weekly-launch-monitor-template.md)
- **Multi-browser smoke matrix (LAUNCH-4 Phase A):** [data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.md](../../data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.md)
- **Build state:** [BBI-Session-Kickoff/bbi-build-state.md](../../BBI-Session-Kickoff/bbi-build-state.md)
- **GA4 property:** `G-XLCM9LCNLN`
- **GSC:** `brantbusinessinteriors.com` (domain property)
- **Shopify Admin:** https://admin.shopify.com/store/office-central-online
- **LIVE URL:** https://www.brantbusinessinteriors.com
