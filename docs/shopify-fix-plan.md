# Brant Business Interiors — Shopify Fix Plan
**Store:** [brantbusinessinteriors.com](https://www.brantbusinessinteriors.com)
**Shopify Admin:** [office-central-online](https://admin.shopify.com/store/office-central-online)
**Date:** April 18, 2026 · **Last updated:** April 20, 2026

---

## Issues Found (Priority Order)

| # | Issue | Impact | Status |
|---|-------|--------|--------|
| 1 | Liquid error — `divided by 0` crashing product pages | High — breaks checkout | ✅ Done |
| 2 | "Example product" in footer — leftover template junk | Medium — looks unprofessional | ⬜ Pending (Tier 3) |
| 3 | No product descriptions — 625 products, most have none | High — SEO + conversions | 🔄 15/50 top products done |
| 4 | Weak homepage — no hero image, no testimonials | Medium — first impressions | ⬜ Pending (Tier 3) |
| 5 | Buried contact info — phone/email not prominent | Medium — losing leads | ✅ Done — announcement bar live |
| 6 | "Outdoor Coming Soon" — incomplete section showing publicly | Low — confusing visitors | ⬜ Pending (Tier 3) |

---

## Fix 1 — Liquid Error (Theme Code)

1. Go to: Admin → Online Store → Themes → **"..." → Edit code**
2. Open `snippets` → `product-blocks.liquid`
3. Press **Cmd+F** → search `divided by`
4. Find the line with `| divided by someVariable`
5. Change it to `| divided by someVariable | default: 1`
6. Click **Save**

---

## Fix 2 — Remove "Example Product" from Footer

1. Admin → Online Store → Themes → **Customize**
2. In left panel, scroll to bottom → click **Footer**
3. Find the block that says "Example product" or "Featured product"
4. Click it → click the **trash icon**
5. Click **Save**

---

## Fix 3 — Write Product Descriptions with Shopify Magic ⭐

**One product at a time:**
1. Admin → Products → All products
2. Click any product with no description
3. Click into the **Description** text box
4. Click the **✨ sparkle icon** inside the box
5. Type a short product summary (e.g. `Ergonomic mesh office chair with lumbar support`)
6. Click **Generate** → edit if needed → **Save**

**Bulk editing:**
1. Admin → Products → All products
2. Check boxes on multiple products → click **Edit products**
3. Use the ✨ sparkle icon on each description field in the bulk editor

---

## Fix 4 — Improve Homepage

**Add a Hero Banner:**
1. Admin → Online Store → Themes → **Customize**
2. Left panel → **+ Add section** → choose **Image banner** or **Slideshow**
3. Upload a photo of a real office setup
4. Click ✨ sparkle icon on the text field → type `Business furniture store, professional, Canadian` → Generate
5. Set CTA button to: `Shop Now` or `Get a Free Design Layout`
6. Click **Save**

**Add Testimonials:**
1. Still in Customize → **+ Add section** → choose **Testimonials** or **Rich text**
2. Add 2–3 real customer quotes
3. Click **Save**

---

## Fix 5 — Make Phone Number More Prominent

1. Admin → Online Store → Themes → **Customize**
2. Click **Header** section
3. Enable **Announcement bar**
4. Type: `Call us: 1-800-835-9565 | Free Design Layouts & Renderings`
5. Click **Save**

---

## Fix 6 — Hide "Outdoor Coming Soon"

1. Admin → Online Store → **Navigation**
2. Click your main menu (usually "Main menu")
3. Find **Outdoor (Coming Soon)** → click three dots → **Remove**
4. Click **Save menu**

---

## Next Steps — Getting More from Claude

### What to Share for Deeper Analysis

| What | How to get it | What it unlocks |
|------|--------------|-----------------|
| Product CSV | Admin → Products → Export → All products | Full audit of all 625 products |
| Theme code files | Admin → Online Store → Themes → Edit code | Direct bug fixes |
| Analytics screenshot | Admin → Analytics → Dashboard | Identify underperforming pages |
| Navigation screenshot | Admin → Online Store → Navigation | Menu redesign |

### Claude API Integration (Advanced)

A custom script can be built to:
- Auto-generate descriptions for all 625 products in bulk
- Auto-tag and categorize products
- Power an AI customer chat on the storefront

**Requirements:**
1. Claude API key from [console.anthropic.com](https://console.anthropic.com)
2. Shopify private app with read/write product permissions
3. Script runs locally, pulls products → sends to Claude → pushes descriptions back

### Easiest AI Chat Option (No Coding)

- Admin → **Apps → Shopify Inbox** — free, built-in, has AI-suggested replies

---

## Contact
- Phone: 1-800-835-9565
- Email: furnorders@officecentral.com

---

## Corporate Context (Critical — updated 2026-04-20)

BBI is the furniture division of Brant Basics, which is owned by **Office Central** (founded 1978, $111M revenue, Richmond Hill ON HQ).

- **Both Office Central and Brant Basics are verified OECM supplier partners** — Ontario school boards, hospitals, libraries, universities, and municipalities can buy from BBI through OECM without open tender. No Ontario furniture competitor has this status.
- BBI can claim: *"Backed by Office Central, proudly serving Ontario businesses since 1964."*
- Parent backlinks available: officecentral.com (48 yrs, $111M) and brantbasics.com (62 yrs) — highest-value links BBI can get, already owned.
- **BBI has no Google Business Profile yet** — needs to be created.

---

---

## Completed Infrastructure (shipped April 19–20, 2026)

*Not line items in the Wave plan — this is the groundwork that makes Wave 0+ possible.*

| What | Status |
|------|--------|
| Shopify Admin API + OAuth app | ✅ Done |
| Full order analysis (Oct 2024 → Apr 2026) | ✅ Done |
| Product HTML audit (all 650 SKUs) | ✅ Done |
| ICP + voice sheet locked (`docs/icp.md`) | ✅ Done |
| 5 approved product description samples (`docs/voice-samples.md`) | ✅ Done |
| HTML cleanup on 147 top-revenue products | ✅ Done |
| 9 ™/® product handles renamed + redirect CSV generated | ✅ Done (CSV upload pending — Leo's task) |
| 11 service pseudo-products unpublished | ✅ Done |
| 21 junk/test/draft products archived | ✅ Done |
| 41 boilerplate duplicates cleaned | ✅ Done |
| Taxonomy: 14 automated collections built (7 type × 7 room) | ✅ Done |
| 584/613 products tagged with `type:*`, `room:*`, `industry:*` | ✅ Done |
| Main nav rebuilt around facets (8 top-level items live) | ✅ Done |
| Delivery + Installation 7-tier shipping rate live | ✅ Done |
| Site-wide floating "Request a Quote" button | ✅ Done |
| Sold-out/\$0-price variants → Request a Quote CTA | ✅ Done |

---

## Wave 0 — Technical Foundation (do before any content work)

*These block everything else. No SEO effort compounds until this layer is solid.*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W0-1 | **Google Search Console + GA4 setup** | 🔴 Critical | ⬜ Not started |
| W0-2 | **Create BBI Google Business Profile** | 🔴 Critical | ⬜ Not started |
| W0-2b | **Google Reviews seeding strategy** | 🔴 Critical | ⬜ Not started |
| W0-3 | **Fix product redirects** | 🔴 Critical | 🔄 CSV at `data/url-redirects.csv` — manual upload in Shopify Admin pending (Leo's task) |
| W0-4 | **Meta titles + descriptions audit** | 🔴 High | ⬜ Not started — brand identity now locked (`docs/icp.md`), blocked on GSC (W0-1) |
| W0-5 | **Confirm Request a Quote CTAs are live** | 🔴 High | ✅ Done — live after April 19 `product-form-buttons.liquid` edit |
| W0-6 | **Parent domain backlinks** | 🔴 High | ⬜ Not started |
| W0-7 | **OECM + "Since 1964" trust signals on BBI store** | 🔴 High | ⬜ Not started |

---

## Wave 1 — Content (no catalog/dev work needed)

*All ⬜ not started. Pre-req: W0-1 (GSC) for measurement, brand identity locked (Tier 2 Phase 0).*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W1-1 | **OECM landing page** | 🔴 High | ⬜ Not started |
| W1-2 | **Brand dealer pages** | 🔴 High | ⬜ Not started |
| W1-3 | **Schools / School Board vertical page** | 🔴 High | ⬜ Not started |
| W1-4 | **Healthcare / Clinic vertical page** | 🟡 Medium | ⬜ Not started |
| W1-5 | **Government / Municipal vertical page** | 🟡 Medium | ⬜ Not started |
| W1-6 | **FAQ page** | 🟡 Medium | ⬜ Not started |
| W1-7 | **Canadian-made page** | 🟡 Medium | ⬜ Not started |
| W1-8 | **"Our Work" / Project Portfolio page** | 🟡 Medium | ⬜ Not started — 48 OCI photos ready at `data/oci-photos/catalog.json` |

---

## Wave 2 — Requires catalog or product work

*All ⬜ not started. Pre-req: Tier 2 Hero 100 enrichment (Phase 1).*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W2-1 | **Acoustic Pods / Phone Booths category page** | 🔴 High (once products exist) | ⬜ Not started — needs products in catalog |
| W2-2 | **Sit-stand buyer guide + collection** | 🟡 Medium | ⬜ Not started |
| W2-3 | **Hybrid work bundle collection** | 🟡 Medium | ⬜ Not started |
| W2-4 | **Email capture + lead magnet** | 🟡 Medium | ⬜ Not started |
| W2-5 | **Internal linking audit** | 🟡 Medium | ⬜ Not started — after Wave 1 content exists |
| W2-6 | **Co-published content on parent domains** | 🟡 Medium | ⬜ Not started |
| W2-7 | **Schema Markup** | 🟡 Medium | ⬜ Not started |
| W2-8 | **Product title optimization** | 🟢 Quick win | ⬜ Not started — covered in Tier 2 Phase 1.2 (Hero 100 titles) |

---

## Wave 3 — Authority building (ongoing)

*All ⬜ not started. Pre-req: Wave 1 + Wave 2 content live.*

| # | Task | Priority | Status |
|---|------|----------|--------|
| W3-1 | **City-level SEO pages** | 🟡 Medium | ⬜ Not started |
| W3-2 | **Ergonomics education hub** | 🟡 Medium | ⬜ Not started |
| W3-3 | **Blog — comparison-style content** | 🟡 Medium | ⬜ Not started |
| W3-4 | **Sustainability / LEED / BIFMA page** | 🟢 Lower | ⬜ Not started |
| W3-5 | **Space planning landing page** | 🟢 Lower | ⬜ Not started |
| W3-6 | **Manufacturer dealer locator pages** | 🟢 Lower | ⬜ Not started |
| W3-7 | **OECM directory + Chamber + COPA backlinks** | 🟢 Lower | ⬜ Not started |
| W3-8 | **Brand kit + design authority** | 🟢 Lower | ⬜ Not started — blocked by Tier 9 design overhaul |

---

### Reference Sites
- Blog model: btod.com/blog/best-office-chair-reviews/
- Portfolio model: poi.ca/our-work/
- Competitor analysis: see `docs/competitor-analysis.md`
- SEO strategy detail: see memory file `project_seo_strategy_2026.md`
