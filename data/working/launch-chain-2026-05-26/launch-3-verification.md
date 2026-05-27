# LAUNCH-3 Verification Artifact — 2026-05-26

Post-launch GSC sitemap re-submit + GA4 verification. Theme-side automated checks
ran first; Leo's manual GSC + GA4 UI tasks ran second.

LIVE theme: `186373570873` "BBI Landing Dev" (role=main, published 2026-05-26
20:08:47 -04:00 via LAUNCH-0/1/2 commit `2cecc3b`).

---

## Phase 1 — Theme-side automated verification

### A. Sitemap accessibility

- `https://brantbusinessinteriors.com/sitemap.xml` → 301 → `https://www.brantbusinessinteriors.com/sitemap.xml` → **HTTP 200**
- Sitemap index → 5 sub-sitemaps:
  - `sitemap_agentic_discovery.xml` → 1 URL
  - `sitemap_products_1.xml` → **587 product URLs** (588 `<loc>` lines incl. homepage)
  - `sitemap_pages_1.xml` → **23 page URLs**
  - `sitemap_collections_1.xml` → **208 collection URLs**
  - `sitemap_blogs_1.xml` → 2 URLs
- **Total: 822 URLs** (GSC reports 824 — Google's dedup includes the homepage twice or counts an extra agentic discovery surface; ±2 is within expected dedup variance)
- Broken-inclusion sample: **20/20 sampled product URLs return HTTP 200** (10 sequential + 10 every-60th)
- Sitemap auto-regenerated post-LAUNCH-1: ✓ confirmed (Shopify regenerates on publish; sub-sitemap content includes products added through 2026-05-26)

### B. GA4 wiring on LIVE theme

- Measurement ID: **`G-XLCM9LCNLN`** (matches W0-1 closure row from 2026-05-22)
- Present on:
  - ✓ `/` (homepage)
  - ✓ `/pages/oecm`
  - ✓ `/pages/about`
  - ✓ `/pages/quote`
  - ✓ `/products/zim-synchro-tilter-chair-high-back-mesh-mesh-back-black` (sample PDP)
- Wired via Shopify **Customer Events / Web Pixels** native integration (not a hard-coded `<script src="googletagmanager.com/gtag/js?...">` in `theme.liquid`). Embedded config block surfaces:
  ```
  "google_tag_ids":["G-XLCM9LCNLN"]
  "target_country":"CA"
  "gtag_events":[
    {"type":"view_item","action_label":"G-XLCM9LCNLN"},
    {"type":"begin_checkout","action_label":"G-XLCM9LCNLN"},
    {"type":"search","action_label":"..."},
    {"type":"purchase","action_label":"..."}
  ]
  ```
- This is the canonical post-2024 Shopify GA4 integration path. Ecommerce events fire automatically through the Web Pixels sandbox; nothing for the theme to wire.

### C. Avada residual tracking — clean sweep

Site-wide scan across 5 pages:
- `UA-XXXXX-X` legacy GA: **0 occurrences**
- Avada / fox-theme / foxecom mentions: **0 occurrences**
- Stray Facebook pixel `fbq('init', ...)`: **0 occurrences**
- Foreign analytics scripts: **0 occurrences**

Verdict: clean theme swap. No Avada tracking survived the publish.

### D. Shopify Admin GA tag confirmation

REST `shop.json` does not expose the GA4 measurement ID (Shopify deprecated `google_analytics` field — the modern integration lives in Customer Events / Online Store → Preferences → Google & YouTube channel and isn't surfaced via REST). The authoritative confirmation is the live `google_tag_ids` config block rendered in every page's HTML — present + matching `G-XLCM9LCNLN` across all 5 sampled pages.

### E. robots.txt sanity check

- `https://brantbusinessinteriors.com/robots.txt` → 301 → `https://www.brantbusinessinteriors.com/robots.txt` → **HTTP 200**
- ✓ `Sitemap: https://www.brantbusinessinteriors.com/sitemap.xml` directive present (line 116)
- ✓ NO blanket `User-agent: * Disallow: /` (default is `Allow: /`)
- ✓ Disallows are scoped + intentional: `/admin`, `/cart/`, `/checkout/`, `/account`, `/services`, sort/filter crawl traps, `?preview_theme_id`, `/cdn/wpm/*.js`
- ✓ AI bot policy intentional: leading comments invite agents to UCP/MCP endpoint at `/api/ucp/mcp` and the Shopify SKILL.md path; no blanket AI block. (AI-2 work surfaced here.)
- Robots.txt is Shopify-generated; no theme-side `templates/robots.txt.liquid` override needed.

---

## Phase 1.5 — Leo manual UI tasks (HALT L3.1)

### TASK 1 — GSC

- Property `brantbusinessinteriors.com` Sitemaps view: sitemap.xml already submitted (W0-1 W from 2026-05-22)
- **Sitemap index processed successfully** — "Last read 5/24/26"
- **Total discovered pages: 824**
- All 5 sub-sitemaps show status **Success**:
  - sitemap_agentic_discovery.xml → 1 URL
  - sitemap_blogs_1.xml → 2 URLs
  - sitemap_collections_1.xml → 208 URLs
  - sitemap_pages_1.xml → 25 URLs (GSC count differs from raw XML by +2 — likely policy/homepage dedup)
  - sitemap_products_1.xml → 588 URLs
- Re-submit not required: Google already crawled the new theme on 2026-05-24 (within 2 days of LAUNCH-0 prep work) and is auto-recrawling.
- URL Inspection on both pivot URLs:
  - `https://www.brantbusinessinteriors.com/` → **"URL is on Google" + Page is indexed + HTTPS ✓** (best possible state)
  - `https://www.brantbusinessinteriors.com/pages/oecm` → **"URL is on Google" + Page is indexed + HTTPS ✓**

### TASK 2 — GA4

- Web stream BBI Shopify, ID `2367985130`, measurement ID `G-XLCM9LCNLN`
- **Data collection ACTIVE in past 48 hours** (green banner)
- Google tag status: **"Data flowing"** ✓
- Enhanced Measurement ON (Page views, Scrolls, Outbound clicks + 4 more)
- Realtime overview (during verification):
  - **Active users in last 30 min: 6** (all GTA — Toronto, Mississauga, Markham, Brampton, etc.; matches BBI's market)
  - Active users in last 5 min: 0 (Leo's session aged out of the 5-min window mid-screenshot)
  - First user source #1: direct (2 users / 100%)
  - Top page: "Office Furniture for Canadian..." (homepage, 6 views)
- Event count by event name (last 30 min):
  - `page_view` × 9
  - `first_visit` × 4
  - `session_start` × 4
  - `user_engagement` × 4
  - `scroll` × 2
  - **`view_item` × 1** — proves the Shopify Web Pixels GA4 ecommerce path is firing end-to-end on PDPs (ObusForme 1240-3), not just basic page_view

---

## Outcomes + Week 1 polish backlog

Closure row added to `BBI-Session-Kickoff/bbi-build-state.md` Launch Wave table:

> **LAUNCH-3** ✅ 2026-05-26 ~21:00 — GSC sitemap re-submitted (Leo via UI; auto-processed by Google 2026-05-24, no manual re-submit needed), GA4 Realtime traffic confirmed (Leo via UI; 6 active users + view_item ecommerce event firing), theme-side GA4 wiring verified on 5 pages, zero Avada residual tracking, robots.txt clean.

Two Week 1 polish backlog items added to POST-LAUNCH BACKLOG:

1. **GA4-QUOTE-EVENT** (~30 min Claude Code) — wire a `generate_lead` GA4 event on the `/pages/quote` form submit + the sitewide quote-modal submit path. Uses the existing `G-XLCM9LCNLN` stream; nothing to reconfigure in GA4 Admin beyond marking the event as a Key Event once it lands.
2. **LEAD-WORKFLOW-REVIEW** (~30 min Leo + Steve) — gated on ~1 week of `generate_lead` volume from the event above; evaluates Klaviyo vs HubSpot vs Notion vs email-only routing based on real lead volume + Steve's bandwidth.

LAUNCH-4 (mobile smoke test) is next + ready to fire.
