# GA4 Conversion Tracking Setup

**Priority:** Pre-LAUNCH-2 (do before Monday 2026-05-25)
**Time:** ~10 minutes
**Owner:** Leo

---

## Why this matters

GA4 distinguishes **events** (every interaction) from **conversions** (events marked as meaningful business outcomes). Without marking conversions, GA4 shows traffic but can't tell you *"organic search produced 3 quote requests this week."*

For BBI, the only conversions that matter are quote requests + (eventually) form-driven leads from segment pages. Marking them now means week-1 data is usable instead of noise.

---

## Step 1: Confirm events are firing (2 min)

1. GA4 → Reports → Realtime
2. Open the BBI site in another tab, submit a test quote request
3. Back in Realtime → Event count panel
4. Look for: `page_view`, `form_submit` (or `generate_lead`), `purchase`

If `form_submit` doesn't fire, Shopify's default Contact form may not be emitting a GA4 event. Check Shopify Admin → Settings → Customer events.

---

## Step 2: Mark events as conversions (3 min)

1. GA4 → Admin (gear icon)
2. Property settings → Events
3. For each event, toggle **"Mark as conversion"** ON:
   - `form_submit`
   - `generate_lead`
   - `purchase`
   - Optionally: `view_item`, `add_to_cart`, `begin_checkout`
4. Save

---

## Step 3: Verify conversions show up (2 min)

1. GA4 → Reports → Engagement → Conversions
2. Marked events should appear in the conversions report (note: 24h propagation for historical data)

---

## Step 4: Configure goal alerts (3 min, optional)

1. GA4 → Admin → Custom Alerts
2. Create alert: **"BBI no conversions 24h"** — `form_submit` count = 0 over a Day period → email alert
3. Acts as a first-week safety net so a broken form doesn't go quietly silent

---

## Post-launch tuning (Week 1+)

Once data is flowing, layer on:

- **Custom dimensions** — OECM vs Private buyer segments
- **Funnel reports** — Landing → `/pages/oecm` → `/pages/quote`
- **Audience segments** — OECM-eligible based on page visit pattern

---

## References

- GA4 property: `G-XLCM9LCNLN`
- GSC: `brantbusinessinteriors.com`
- Shopify Customer events docs: https://shopify.dev/docs/api/web-pixels-api
- Parent playbook: [post-launch-monitoring.md](post-launch-monitoring.md)
