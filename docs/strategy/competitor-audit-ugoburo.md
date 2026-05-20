# Competitor Structural Audit — ugoburo.ca

**Date:** 2026-05-14
**Author:** COMP-SCRAPE-1 (Step 24, Wave E hardening)
**Purpose:** Tactical, page-pattern-level competitor read. Findings fold back into AI-7, AI-8, AI-9, INTERLINK-3, BRAND-PAGES-1, and PDP enhancements. Complement to `docs/strategy/competitor-analysis.md` (strategic landscape) — this doc is about *how* their pages are constructed.
**Method:** Read-only fetch of 5 representative URLs (homepage, NMSO/government, brand hub, FAQ, About us, PDP) on 2026-05-14. No login walls; everything inspected is public.

---

## TL;DR — five takeaways

1. **Their NMSO/government page is the single highest-value pattern in this audit.** It uses two concrete contract-number tables (manufacturer × contract ID × category) as proof of eligibility. BBI's OECM page should mirror this with `Agreement 2025-470` + category breakdown. This is the AI-8 unlock.
2. **Their PDP carries a plain-language ergonomic-features panel** — one icon + one sentence per adjustment ("Tension Adjustment — increase or decrease to match body weight. Allows you to rock comfortably, without heavy pushing, reducing muscle fatigue."). Cheap, repeatable, and trivially indexable. Strong post-launch PDP enhancement target.
3. **Their brand hub uses a two-tier copy pattern**: tight intro paragraph above the product grid, long-form 7-section SEO block below. Each H3 owns one angle (history, sizing, sustainability, warranty, closing CTA). This is the template `theme/sections/ds-lp-brand.liquid` should match for BRAND-PAGES-1.
4. **They have NO JSON-LD schema, NO FAQPage markup, NO Product schema visible in markup.** BBI is *ahead* on technical SEO once SEO-AUDIT-1 ships. AI-5 (FAQPage on OECM/Design) and AI-9 (category FAQs with schema) are real differentiators, not parity moves.
5. **They are e-commerce-first, BBI is consultation-first** — and BBI should not chase parity. Ugoburo sells chairs direct online with `Add to Cart`. BBI's institutional buyer wants a quote on 80 workstations and a free design layout. Don't add "Add to Cart" prominence. *Do* steal their service-language ("real-time support", "AI Assistant", "2D/3D drawings free of charge") for the OECM and quote pages.

---

## Methodology

### Pages audited

| Page type | URL | Why this page |
|---|---|---|
| Homepage | `ugoburo.ca/en` | Entity-clarity framing, primary nav, trust signals |
| Government / NMSO | `/en/standing-offer-supply-arrangement-office-chair-furniture-sosa.html` | Direct analog of BBI's `/pages/oecm` |
| Brand hub | `/en/office-furniture-canada/global.html` | Same brand BBI builds for in BRAND-PAGES-1 |
| FAQ | `/en/faq/office-furniture.html` | Sole consolidated FAQ — informs AI-9 / AI-5 |
| About us | `/en/about-us/office-furniture.html` | Entity-clarity reference for AI-7 |
| PDP | `/en/global-ergonomic-chair-mesh-vion-6321-3.html` | PDP enhancement findings |

Skipped: blog index (low leverage for current step set), Find Your Chair wizard (interesting but post-launch backlog), collection pages (homepage taxonomy + brand hub covered the pattern).

### Platform tells

Magento (Adobe Commerce). Signals: `/customer/account/login`, `/checkout/`, `/catalog/product/view/id/`, "the store will not work correctly when cookies are disabled" default boilerplate, `media/catalog/product/cache/<hash>/` image path pattern, `TemplateMonster/theme007` in static asset paths. Older theme — TemplateMonster theme007 is a budget template. Lots of stale layout cues (e.g., "navigation has not been optimized for mobile devices" in their own FAQ).

### What we did NOT verify

- JSON-LD schema (web fetch strips inline JSON; I could not confirm absence — only that no visible JSON-LD appeared in any markup). High confidence on absence given the platform/theme age and the FAQ page itself has no FAQPage hooks visible.
- Lighthouse / Core Web Vitals — separate Phase 3 step (PERF-AUDIT-1) on BBI side.
- Internal search behaviour, account flow, checkout flow — out of scope for structural audit.

---

## Page-type findings

### 1. Homepage

**H1:** `Office Furniture Canada - Ergonomic Chair & Standing Desk Canada`

**First-200-words substance:** None as prose. The above-the-fold experience is two rotating promo banners ("SAVE 20% Standing Desks", "SAVE 10% on Chairs by Global") and a 6-tile icon grid (Office chair, Desk, Collections, Table, Office storage, Ergonomic tool). The H1 only appears below the tile grid. *There is no who/what/who/where prose paragraph anywhere on the homepage above the fold.*

**Trust signals (above the fold):** Promo banners; phone number `1 855 846-2876`; "Canadian owned & operated" maple-leaf badge; "Buy Local"; "Easy return"; "Furniture experts — real-time support".

**Below-the-fold:**
- 8-product "Most popular ergonomic chairs" grid
- 4 testimonial quotes from named buyers ("Bryan Hipson Translations Ltd", "Elliott Ng", "Melanie Wilson", "Cody Zamora") with `Verified Buyer` framing — *no review platform attribution visible (e.g., not Google/Trustpilot embedded)*
- 4-tile collection cross-link band (Newland, Zira, Bridges, Boulevard 3)
- Newsletter signup
- Showroom address: `6955, Taschereau, suite 201, Brossard, QC, J4Z 1A7`
- D-U-N-S `252053046` in footer

**Lead-capture pattern:** Newsletter only; no quote modal, no consultation CTA. Phone-driven for B2B.

**AI-7 implication:** Ugoburo's homepage is a weak entity-clarity reference *as-is* — the H1 is keyword stuffing and there's no narrative paragraph. But their About page (see below) is strong and BBI's AI-7 should pull from that pattern, not the homepage.

---

### 2. Government / NMSO page — *the highest-leverage page on the site*

**URL:** `/en/standing-offer-supply-arrangement-office-chair-furniture-sosa.html`
**Title tag:** `NMSO Furniture – Federal Supply Arrangement Eligible`
**Meta description:** `Federal Government Canada office furniture & chairs - Supply Arrangement - NMSO. Canadian office furniture Global, Ergocentric, Humanscale.`
**H1:** `Supply Arrangement NMSO - Federal Government Canada`

**Structure (verbatim H2 sequence):**
1. Office Furniture Solutions for the Federal Government of Canada *(pain-point framing)*
2. An Offer Composed of the Best Canadian Office Furniture Suppliers *(quality positioning)*
3. A Dedicated Team of Furniture Experts *(service depth)*
4. Real-Time Support *(channel inventory — phone/chat/email/AI assistant/2D-3D drawings)*
5. Master Supply Arrangements and Procurement Agreements *(eligibility claim — federal, provincial, municipal)*
6. **List of available Office Chairs — Procurement Agreements** *(contract-number table #1, 5 rows)*
7. **List of available Workplace Furniture — Procurement Agreements** *(contract-number table #2, 6 rows)*
8. A Reliable and High-Performance Canadian Supply Chain
9. Why Choose Ugoburo? *(4-bullet recap)*
10. Contact Ugoburo Today *(CTA)*

**The two contract tables verbatim:**

| Manufacturers | Categories | Contract No. |
| --- | --- | --- |
| Global Furniture Group | Office Seating | `E60PQ-120001/005/PQ` |
| Allseating | Office Seating | `E60PQ-120001/003/PQ` |
| Ergocentric | Office Seating | `E60PQ-120001/002/PQ` |
| Humanscale | Office Seating | `E60PQ-120001/010/PQ` |
| HÅG (Flokk) | Office Seating | `E60PQ-120001/017/PQ` |

| Manufacturers | Categories | Contract No. |
| --- | --- | --- |
| Global Furniture Group | Furniture (Categories 1A, 1B, 2, 3, 4, 5, 6) | `E60PQ-140003/032/PQ` |
| Global Furniture Group | Furniture (Categories 1B, 2, 3, 5) | `E60PQ-140003/033/PQ` |
| Lacasse | Furniture (Category 4) | `E60PQ-140003/020/PQ` |
| Fellowes (ESI) | Furniture (Category 6) | `E60PQ-140003/044/PQ` |
| Nightingale | Furniture (Category 6) | `E60PQ-140003/065/PQ` |
| Humanscale | Furniture (Category 6) | `E60PQ-140003/071/PQ` |

**Why this matters for BBI's OECM page (AI-8):**

The single move that lifts AI citation rate on `/pages/oecm` is **concrete proof of eligibility, structured as a table**. Ugoburo shows actual federal contract IDs broken out by manufacturer + category. AI systems can extract that table cleanly and cite it.

BBI's OECM page currently surfaces the agreement as editorial copy ("BBI holds OECM Agreement 2025-470 at the supplier level covering the full furniture catalog"). The AI-8 rewrite should add a table like:

| Agreement | Category | Coverage | Brands |
|---|---|---|---|
| OECM 2025-470 | Seating | All furniture-grade chairs | Global, OTG, ergoCentric, Heartwood, … |
| OECM 2025-470 | Desks & workstations | Single, L-shape, U-shape, benching | Global, OTG, Heartwood, Lacasse |
| OECM 2025-470 | Storage | Lateral, vertical, pedestals, bookcases | Global, OTG, Heartwood, Safco |
| OECM 2025-470 | Tables | Conference, training, cafeteria | Global, OTG, Heartwood |

(Replace placeholder rows with the actual category structure of Agreement 2025-470.)

**Also steal:**
- **Pain-point opener** ("tailored and strategic office furniture solutions designed to meet the specific needs of government offices") — BBI's equivalent is school boards, hospitals, municipalities, FHTs, post-secondary.
- **Service-channel inventory** ("Live customer support… AI Assistant Ugo… Tailored procurement support — 2D/3D drawings free of charge"). BBI should explicitly list: quote in 1 business day, free design layout, installation in Ontario, PO-friendly billing.
- **Multi-level eligibility claim** ("federal, provincial, and municipal agencies"). BBI's OECM page should explicitly state which Ontario institutional buyer types are covered (school boards, hospitals, municipalities, post-secondary, agencies) so a procurement officer can self-identify in 2 seconds.

**Do NOT steal:**
- "AI Assistant Ugo" gimmick — BBI's voice is human, established, since-1964.
- Generic "Why Choose Ugoburo?" 4-bullet closer feels cheap. BBI's closer should be a specific Ontario customer reference or a quote-CTA module.

---

### 3. Brand hub (Global) — template pattern for BRAND-PAGES-1

**URL:** `/en/office-furniture-canada/global.html`
**H1:** `Global` (just the name)
**Breadcrumb:** Home > Brands > Global
**Meta description:** `Global office chairs, desks and office furniture in Canada. Best office chairs for businesses. Bulk price on Global office chairs, desks and system furniture.`

**Two-tier copy pattern:**

**Tier 1 — hero intro above product grid** (~2 paragraphs):
> "Ugoburo.ca is proud to offer you the full range of office furniture and office chairs from Global Furniture Group. Since 1966, Global office chairs have been recognized worldwide for their excellence and durability. Whether you're looking for an ergonomic office chair, a complete desk set, versatile tables, or functional filing cabinets, Global provides a product range tailored to meet the needs of businesses of all sizes. Choosing Global office chairs and furniture means opting for exceptional quality at a competitive price."

**Tier 2 — long-form SEO block below product grid**, with the H2 `Global Furniture Group: Canada's largest office chairs and furniture manufacturer` and 7 H3 sub-sections:

1. Office chairs designed to meet new market standards
2. Everything for businesses, large or small
3. Wall-to-wall storage
4. From office furniture to relaxation!
5. Global: an environmentally responsible company *(ISO 14001, Greenguard, LEED — all named in prose, no badge artwork)*
6. Global warranty: enhanced quality assurance *("zero-defect warranty applies to office chairs, file cabinets, partitions, desks, furniture, modular units and worktables")*
7. Purchase your Global office furniture online *(closing CTA)*

**Other observations:**
- Faceted left-rail filter ("Shop By") with full taxonomy
- Brand-to-brand cross-link sidebar (10 other brands linked)
- 4-tile collection cross-link band at bottom
- No FAQ block, no testimonials specific to the brand, no JSON-LD
- Per-product star reviews ("1 Review", "4 Reviews") visible in grid — no brand-level aggregation

**BRAND-PAGES-1 implications:**
- `theme/sections/ds-lp-brand.liquid` should have:
  - Hero intro slot (rich-text, 2 paragraphs)
  - Product grid slot (collection reference)
  - Long-form body slot (H2 + repeatable H3+body blocks via section blocks, max ~8)
  - Brand-to-brand cross-link slot (auto-pulled from canonical-brand map; show 5 sibling brands)
  - Collection cross-link tile band (3–4 collection refs)
- BBI's edge: BBI **can** add testimonials specific to the brand (institutional references — "Halton District School Board standardized on OTG ProGrid for…") which ugoburo doesn't surface.
- BBI's edge: BBI **should** add a "Government / OECM eligibility under this brand" callout box (e.g., "OTG furniture is OECM 2025-470 eligible — request a quote with PO terms"). Ugoburo doesn't connect their NMSO page to their brand pages — a missed opportunity worth stealing.

---

### 4. FAQ page — informs AI-9 and AI-5

**URL:** `/en/faq/office-furniture.html`
**H1:** `Ugoburo - FAQ`

**Structure:** Single consolidated FAQ with 4 thematic sections:
1. General — Customer service (8 Q&As)
2. Prices and payments (6 Q&As, including "How can I place an order for a government or public sector agency?" and "How do I order for a tax-exempt institution?")
3. Delivery — Warranty — Returns (7 Q&As)
4. Privacy — Security (2 Q&As)

**Notable Q&A patterns:**
- *"How can I place an order for a government or public sector agency?"* — "We accept orders from schools, colleges, universities, hospitals, clinics, and any other government or public sector body or institution. To place an order, please use your purchase order number during the purchase process. One of our advisors will contact you to confirm your information." → **BBI's equivalent answer should be sharper given OECM coverage.**
- *"Are discounts available for major orders?"* — bulk pricing framing
- *"How do I order for a tax-exempt institution?"* — direct address of institutional tax exemption

**Critical absence:** No FAQPage JSON-LD visible. No accordion structure. Plain `<h3>` + paragraph throughout. This is below BBI's planned baseline once AI-5 + AI-9 ship.

**AI-9 implications (FAQ blocks on 9 category pages):**
- Ugoburo has **zero** category-level FAQs. Every FAQ is consolidated into one page. AI-9 puts BBI ahead by default — each category page (seating, desks, storage, tables, boardroom, ergonomic, panels, accessories, quiet-spaces) gets 3–5 Q&As + FAQPage JSON-LD.
- **Steal these question topics** for the seating category FAQ since they're proven user intent: "How do I order for a tax-exempt institution?", "Are discounts available for major orders?", "Do your products require assembly?", "Can you install my furniture for me?", "What should I do if I receive damaged goods?".
- Use BBI-specific phrasing that addresses *institutional* buyers, not consumers (i.e., "What's the lead time on a 50-chair OTG ProGrid order to Halton District School Board?" not "When will my chair arrive?").

**AI-5 implications (FAQPage schema on OECM + Design Services + blog):**
- Trivial competitive moat once shipped. Ugoburo doesn't have it anywhere.

---

### 5. About us — informs AI-7 (entity clarity)

**URL:** `/en/about-us/office-furniture.html`
**Title:** `Office Furniture and Chair Experts in Canada`
**Meta description:** `Ugoburo.ca: experts in ergonomic office furniture and chairs made in Canada. Work better to live better with our comfort, quality, and service!`

**Opening 4 sentences verbatim:**
> "Since 2011, Ugoburo Inc. has built a reputation as Canada's leading online and omnichannel retailer of ergonomic office furniture and accessories. 100% Canadian-owned and proudly partnered with top Canadian manufacturers, we've become the go-to destination for businesses, public institutions, and professionals seeking commercial-grade furniture designed for comfort, health, and performance. Our mission is simple yet powerful: help Canadians work better and live better."

**Structure (verbatim H2 sequence):**
1. Canada's True National Omnichannel Office Furniture Expert
2. A Trusted Name Since 2011
3. What Makes Ugoburo Different *(5-bullet feature list: Canadian-Made Quality, Tailored Ergonomic Solutions, Delivery & Installation, Secure & Seamless Experience, Warranty & After-Sales Excellence)*
4. A Human Team with a Shared Mission
5. Our Promise

**Why this matters for AI-7:**

The first 4 sentences answer **who / what / who / where / mission** in one tight block. AI-7 calls for "first 200 words on / must answer: who BBI is · what they sell · who they serve · where they install" — this About page is the better reference than ugoburo's homepage.

**BBI's equivalent opener should look like:**
> "Since 1964, Brant Business Interiors has supplied commercial-grade office furniture to Ontario's institutional buyers — school boards, hospitals, municipalities, post-secondary, family health teams, and non-profits. As an OECM-verified supplier under Agreement 2025-470, BBI provides procurement-compliant access to Global Furniture Group, OTG, Heartwood, and 27 other Canadian and ergonomic-specialist brands without open tender. We design, deliver, and install from our Brantford headquarters across Ontario."

(60 words. Folds in: since-1964, ICP, OECM eligibility, agreement number, anchor brands, service depth, geography.)

**Steal:**
- The "Since [year]" / "100% Canadian-owned" opener structure
- The 5-bullet `What Makes Us Different` block (BBI's version: OECM-verified, Since 1964, Ontario stock & install, free design layout, PO-friendly billing)

**Don't steal:**
- "Work Better to Live Better" tagline (wrong register for institutional B2B). BBI's voice is procurement-officer-friendly, not consumer-aspirational.

---

### 6. PDP (Vion 6321-3 chair) — informs post-launch PDP enhancements

**URL:** `/en/global-ergonomic-chair-mesh-vion-6321-3.html`
**H1:** `Vion 6321-3 - Ergonomic Office Chair with Mesh Back`

**Above-the-fold pattern:**
- Brand link prominently surfaced ("Global" → brand hub)
- 7 product images (front, side, back, 5 mesh-colour variants, video thumbnail)
- Star rating "(2 Ratings)"
- SKU + internal Ugoburo ID
- Configurator: back colour, finish/colour, armrest (with +$148 conditional), seat size, base, casters (with +$30 conditional)
- "From — Special Price $679.15 / Regular Price $799.00 (You save $119.85) — Bulk pricing"
- "In stock" badge
- Add to Cart (no Quote CTA — pure transactional)

**Mid-PDP:**
- Short description prose
- Features bullets (12 lines, mostly dimensional + adjustment summaries)
- **Ergonomic features panel** — *the key pattern to steal.* 10 icon + plain-language blocks, e.g.:
  > **Tension Adjustment** — Increase or decrease to match body weight. Allows you to rock comfortably, without heavy pushing, reducing muscle fatigue.
  > **Seat Height** — Raise or lower to allow your feet to rest flat on the floor. Avoids pressure under your thighs, easing blood flow.
  > **Waterfall Seat Edge** — Reduces pressure at the back of your knees, contributing to good blood flow.
- "More Information" specs table (weight, leadtime, volume, dimensions, certifications, adjustment matrix)

**Certifications surfaced in specs:** ANSI BIFMA, ISO 14001, Greenguard (logos but no badge artwork; just spec rows). BBI should surface these in the same way for any product whose spec metafield carries them.

**Critical absences:**
- No FAQ on PDP
- No JSON-LD Product schema visible
- No related-content links (no "Read the seating buyer's guide", "View OECM eligibility", "Request a design layout")
- No quote CTA — appropriate for ugoburo's e-comm model but a gap BBI fills natively

**Post-launch PDP enhancement targets (file as ideas backlog now, not Wave E):**
1. Ergonomic-features panel — port the icon + plain-language explainer pattern to BBI's chair PDPs. Use existing spec metafield + a small icon library. Big AI-search win.
2. Product JSON-LD — already on BBI's Wave E roadmap via SEO-AUDIT-1; this audit reinforces it as table-stakes.
3. "OECM eligibility under Agreement 2025-470" callout on every furniture-grade PDP, linking to `/pages/oecm`. Ugoburo doesn't do this; BBI's OECM angle makes it natural.
4. Lead time visible above the fold for institutional orders (BBI knows the buyer needs "8 weeks for 80 ProGrid chairs to Halton" before they engage). Don't hide it in the spec table.

---

## Gap analysis — prioritized

| # | Finding | Folds into | Priority | Effort |
|---|---|---|---|---|
| 1 | NMSO/OECM contract-table pattern (manufacturer × contract ID × category) | **AI-8** (Step 18) | **MUST-STEAL** | ~60 min content + 30 min schema |
| 2 | Pain-point opener + service-channel inventory on OECM page | **AI-8** (Step 18) | **MUST-STEAL** | ~30 min content |
| 3 | About-page opener pattern (since-year + ICP + mission in 60-100 words) | **AI-7** (Step 17) | **MUST-STEAL** | ~30 min content |
| 4 | Two-tier brand-hub copy (intro above grid + 7-section SEO block below) | **BRAND-PAGES-1** (Step 25) | **MUST-STEAL** | Already in scope for shared section design |
| 5 | Cross-link OECM/government page from every brand hub + every furniture PDP | **BRAND-PAGES-1**, **INTERLINK-3** | **MUST-STEAL** (BBI edge — ugoburo doesn't do this) | ~30 min in shared brand section + snippet |
| 6 | PDP ergonomic-features panel (icon + plain-language explainer) | Post-launch backlog | Consider | ~4-6 hrs to build snippet + apply to chair catalog |
| 7 | Category-level FAQ pattern + question topics worth borrowing | **AI-9** (Step 19) | Consider — BBI is already ahead, just needs the right questions | ~20 min question-mining per category |
| 8 | Find Your Chair wizard (guided product finder) | Backlog (Wave 2+) | Consider | Multi-week build; not launch-critical |
| 9 | Free colour samples ordering pattern | Skip | Skip | BBI is consultation-first; design layout is the equivalent |
| 10 | "AI Assistant" chatbot widget | Skip | Skip | Wrong register for BBI's voice |
| 11 | "Add to Cart" e-commerce primacy on PDP | Skip | Skip | BBI's quote-first model is the better fit for ICP |
| 12 | Promo discount banners ("Save 10% / Save 20%") | Skip | Skip | BBI's positioning is fair pricing + service depth, not coupons |

---

## Recommendations folded back into launch-tracker steps

**Step 17 — AI-7 (Entity-clarity copy on homepage)**
Pull from ugoburo's About-page opener structure (not their homepage). Target 60–100 words in the first paragraph answering who/what/who/where + mission. Draft text included in section 5 above.

**Step 18 — AI-8 (OECM page copy hardening)**
Highest-leverage AI-search win in Wave E. Three additions:
1. Insert OECM 2025-470 coverage table (manufacturer × category × brands). Mirror ugoburo's NMSO table pattern.
2. Add pain-point opener: "Ontario institutional buyers — school boards, hospitals, municipalities, post-secondary, FHTs, agencies — can purchase BBI's full furniture catalog under OECM Agreement 2025-470 without going to open tender."
3. Add service-channel inventory: quote in 1 business day, free design layout, Ontario installation, PO-friendly billing, OECM-compliant invoicing.

**Step 19 — AI-9 (FAQ blocks on 9 category pages)**
Steal these Q&A topics for the seating category (and adapt per category):
- "How do I order under OECM Agreement 2025-470?"
- "Are bulk discounts available for school boards / municipalities?"
- "What's the typical lead time on a [N]-chair Global / OTG / Heartwood order?"
- "Does BBI install in [Brantford / Hamilton / London / Toronto / Waterloo]?"
- "What's the warranty on commercial-grade office chairs?"
Each block carries FAQPage JSON-LD per AI-9 spec.

**Step 25 — BRAND-PAGES-1 (Shared brand-page section)**
Validate `theme/sections/ds-lp-brand.liquid` schema includes:
- Hero intro rich-text slot (2-paragraph max)
- Product grid (collection reference)
- Long-form body block list (H2 + repeatable H3-body section blocks, max 8)
- Brand-to-brand cross-link slot (auto from canonical-brand map, 5 sibling brands)
- OECM eligibility callout (new — BBI edge over ugoburo)
- Collection cross-link tile band (3–4 collection refs)
- Brand testimonial slot (BBI edge — institutional references)

**Step 26 — INTERLINK-3 (Final cross-link audit)**
Two new patterns to check during the audit:
- Every brand hub links to `/pages/oecm` (BBI edge over ugoburo)
- Every furniture-grade PDP carries an "OECM eligibility" callout linking to `/pages/oecm` (BBI edge over ugoburo; defer to post-launch if scope grows)

**Post-launch backlog (file in `docs/plan/ideas-backlog.md` under PDP enhancements)**
- PDP ergonomic-features panel (icon + plain-language explainer pattern)
- "OECM eligibility under Agreement 2025-470" callout snippet for all furniture-grade PDPs
- Above-the-fold lead time display for chairs/desks with `leadtime` metafield populated

---

## What BBI does better than ugoburo (already, before any of these steps)

Audit didn't only find gaps — there's a meaningful list of areas where BBI is already structurally ahead. Worth documenting so the launch positioning doesn't undersell BBI's actual edge.

1. **Catalog data hygiene.** Phase 1 closure means BBI has 593 active products with consistent vendor field + metafield + brand:* tag, 30 canonical brands, 0 orphaned industry:* tags, 164 redirects live. Ugoburo's tagging/data layer is opaque from the outside but the spec-table quality on individual PDPs is uneven (e.g., the Vion PDP mixes `no` strings and `logo ergo` placeholder strings in the same column).
2. **Service-first model fits institutional ICP.** Ugoburo is consumer-leaning even on the government page ("Add to Cart" CTAs in nav, promo discount banners). BBI's quote-first flow is the right register for an Ontario school board procurement officer.
3. **Soon-to-ship schema differentiators.** Once SEO-AUDIT-1 ships, BBI will carry Product, Article/BlogPosting, FAQPage, and Organization JSON-LD across the bbi_landing gate. Ugoburo has none visible.
4. **Geographic specificity.** BBI's 5-location Ontario footprint (Brantford HQ + delivery/install across SW Ontario, GTA, Hamilton, Waterloo, London) is more credible to an Ontario buyer than ugoburo's single Brossard showroom + "every province with care".
5. **Brand depth in the canonical map.** 30 canonical brands (4 storefront-callable) vs ugoburo's ~11 visible brand pages. BBI's brand-catalog reach is wider, especially in Canadian-manufactured (Heartwood, OTG, Global Furniture Group depth).

---

## Appendix — pages NOT audited (and why)

| URL | Why skipped | When to revisit |
|---|---|---|
| `/en/blog` | Low leverage for Wave E step set; BLOG-SEED-1 (Step 36) will define BBI's blog cadence independently | If BLOG-SEED-1 stalls on topic selection — ugoburo blog is a topic-mining source |
| `/en/find-your-office-ergonomic-chair.html` | Guided wizard is multi-week build; not in launch path | Wave 2 backlog if the buyer-guide concept moves forward |
| `/en/office-chair.html` (category page) | Homepage taxonomy + brand hub covered the pattern; category page is product-grid + repeated copy | Re-audit only if AI-9 reveals category-page copy gaps after FAQ blocks ship |
| `/en/collections.html` and individual collection pages | BBI's collection landscape is post-COLLECTION-CLEANUP-APPLY; structurally different shape | Once post-launch collection audit (SEO-AUDIT-2) runs |
| Checkout / account flows | Out of scope for structural audit | Pre-LAUNCH-0 if any cart bug suspected |

---

## Sources

- [Ugoburo homepage](https://www.ugoburo.ca/en)
- [Ugoburo NMSO/government page](https://www.ugoburo.ca/en/standing-offer-supply-arrangement-office-chair-furniture-sosa.html)
- [Ugoburo Global brand hub](https://www.ugoburo.ca/en/office-furniture-canada/global.html)
- [Ugoburo FAQ](https://www.ugoburo.ca/en/faq/office-furniture.html)
- [Ugoburo About us](https://www.ugoburo.ca/en/about-us/office-furniture.html)
- [Ugoburo Vion 6321-3 PDP](https://www.ugoburo.ca/en/global-ergonomic-chair-mesh-vion-6321-3.html)
