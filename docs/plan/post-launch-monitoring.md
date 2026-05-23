# BBI Post-Launch Monitoring Playbook

Owner: Leo
Created: 2026-05-24 (Day 10, pre-LAUNCH-2)
Related docs:
- [GA4 Conversion Setup](ga4-conversion-setup.md)
- [Weekly Launch Monitor Template](../reports/weekly-launch-monitor-template.md)
- Build state: [BBI-Session-Kickoff/bbi-build-state.md](../../BBI-Session-Kickoff/bbi-build-state.md)

---

## Time horizons + what they measure

| Horizon | Core question |
|---|---|
| Hour 0–24 | Did launch work technically? |
| Day 2–7 | Did Google understand the changes? |
| Week 2–4 | Did rankings start to move? |
| Day 30+ | Did launch produce business outcomes? |

Each section below covers: the question being answered, where to look, and the red flags to watch for.

---

### Hour 0–24 — Did launch work technically?

**Question:** Did the site break, do redirects route, can search engines crawl?

**Where to look:**
- GSC → Index → Pages — surface any crawl errors
- GSC → Index → Sitemaps — sitemap status should read "Success"
- GA4 → Realtime — confirm pageviews are firing
- Shopify Admin → Online Store → Live View — sanity check live sessions
- Manual: click 5–10 Avada URLs (top-traffic pages from the redirect map), verify each redirect resolves to the new equivalent

**Red flags:**
- Pageviews drop 80%+ vs Avada baseline
- "Page not found" surge in the GA4 Pages report
- Multiple 5xx errors in GSC

---

### Day 2–7 — Did Google understand the changes?

**Question:** Is new schema being indexed, are new pages indexed, are redirects being honored?

**Where to look:**
- GSC → URL Inspection on 5–10 key URLs. Each should show:
  - "URL is on Google" ✓
  - Recent "Crawled" timestamp
  - Sitemap referenced
  - Enhancements section detecting: Products, Breadcrumbs, FAQ, LocalBusiness, Sitelinks searchbox, Article
- GSC → Indexing → Pages — indexed pages climbing back toward 825 (Avada baseline)
- GA4 → Search Console section — branded position movements
- Manual: Google "Brant Business Interiors" → knowledge panel should show the new 9–5 hours

**Red flags:**
- Schema enhancements still not detected after 5 days
- "Crawled – currently not indexed" status on key pages
- SERP sitelinks still showing "Skip to content" 7 days post-deploy

---

### Week 2–4 — Did rankings start to move?

**Question:** Are positions improving, are AI engines citing BBI?

**Where to look:**
- GSC → Performance → Search results, filter by query type:
  - Brand queries → position 1–3 quickly
  - Local commercial → page 3 → page 1–2 over 14–30 days
  - Informational → ranks quickly thanks to AI-7/AI-8 + schema
- GA4 → Acquisition → Search Console queries — track CTR
- Manual AI checks (weekly):
  - Perplexity: "Who supplies office furniture to Ontario school boards under OECM?"
  - ChatGPT: "Best OECM-approved office furniture vendor in Ontario"
  - Gemini: "Where can a school board buy office furniture under OECM agreement 2025-470?"

**Red flags:**
- No movement on branded queries after 14 days
- Local pack still missing BBI after 30 days
- AI engines still citing "Brant Basics" instead of BBI

---

### Day 30+ — Did launch produce business outcomes?

**Question:** Quote form submissions, qualified leads, OECM-eligible buyer engagement?

**Where to look:**
- GA4 → Events — `form_submit` events
- GA4 → Conversions — if events are marked as conversions ([setup walkthrough](ga4-conversion-setup.md))
- Shopify Admin → Customers
- Steve's inbox — actual quote requests landing as email

---

## Weekly Monday Health Check Ritual

15-minute Monday morning check. Build the rhythm — the value comes from doing it every week, not from any single check.

### Tab group setup (do once)

Bookmark these 6 URLs in a "BBI Launch Monitor" folder:

1. https://search.google.com/search-console
2. https://analytics.google.com  (property G-XLCM9LCNLN)
3. https://business.google.com
4. https://www.google.com/search?q=brant+business+interiors&pws=0
5. https://office-central-online.myshopify.com/admin
6. https://www.perplexity.ai

### The 6-tab routine

**1. GSC → Performance (5 min)**
Date range: Last 28 vs Previous 28. Note clicks delta, impressions delta, average position delta, CTR delta, top 10 winning + losing queries.

**2. GSC → Index → Pages (2 min)**
Is the indexed page count holding/growing? Any new errors? How many in "Crawled – currently not indexed"?

**3. GA4 → Reports → Realtime (1 min)**
Confirm pageviews are still firing.

**4. GA4 → Acquisition → Traffic acquisition (3 min)**
Organic search WoW, direct WoW, goal completion rate.

**5. GA4 → Search Console section (2 min)**
Queries trending up/down. Anything surprising?

**6. Manual brand check (2 min)**
Incognito Google "Brant Business Interiors". Check the knowledge panel, hours, photos, pin. SERP sitelinks. Local pack inclusion.

Log findings each week using the template at [docs/reports/weekly-launch-monitor-template.md](../reports/weekly-launch-monitor-template.md). Copy the template to a dated file (e.g. `weekly-launch-monitor-2026-06-01.md`) and fill in.

---

## What to do if things go wrong

### Traffic dropped on launch day
**Most likely cause:** the redirect map missed something.
**First action:** GSC → URL Inspection on the top-10 Avada URLs. Add missing redirects via Shopify Admin → Online Store → Navigation → URL Redirects.

### Rankings dropped after launch
**Most likely cause:** Google re-indexing — temporary fluctuation.
**First action:** Wait 14–21 days before deciding it's persistent. If still down at day 21, re-run the schema audit.

### AI engines aren't citing us
**Most likely cause:** GBP completion gap + citations gap.
**Fix path:** Run the deferred W0-2 work post-launch (GBP completion + W0-CITATIONS). Closes the gap in 30–60 days.

### Form submissions but no orders
**Most likely cause:** quote-to-PO sales workflow.
**Owner:** Steve's operational question, not a technical fix.

---

## Honest expectations timeline

- **Week 1:** Traffic stabilizes around the Avada baseline + a slight bump from schema. Not a rocketship.
- **Week 2–4:** Brand queries sharpen. Local commercial starts moving. AI citations begin.
- **Week 4–8:** Local 3-pack inclusion if GBP completion + reviews land. AI engines reliably cite BBI.
- **Week 8–12:** Compounding. Position improvements on harder commercial keywords.
- **Week 12+:** Steady state if maintenance happens.

---

## Post-launch action items (from backlog)

**Critical Week 1** (already tracked in post-launch backlog):
- GBP completion: 13 service areas, attributes, social profiles, 8 Q&A, first 4 Google Posts
- W0-2c-EVIDENCE pack + physical signage
- W0-2c-MONITOR weekly incognito search

**Critical Week 1–4:**
- W0-CITATIONS: Bing Places, Apple Maps, LinkedIn, Yelp, BBB
- W0-2b reviews seeding: Tier 1 calls, email blast

**Ongoing:**
- Weekly Google Post
- 48-hour response SLA on reviews
- Schema enhancements review in GSC

See `BBI-Session-Kickoff/bbi-build-state.md` for the authoritative POST-LAUNCH BACKLOG.

---

## References

- GA4 property: `G-XLCM9LCNLN`
- GSC: `brantbusinessinteriors.com` (domain property)
- Tracker artifact: `bbi-launch-tracker`
- Build state: [BBI-Session-Kickoff/bbi-build-state.md](../../BBI-Session-Kickoff/bbi-build-state.md)
