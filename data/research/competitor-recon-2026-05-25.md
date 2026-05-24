# BBI Competitor Recon Scan — 2026-05-25

Surface-level (Approach A) read-only recon of 3 Ontario commercial office-furniture competitors. Pre-launch SERP baseline frozen. Findings are POST-LAUNCH BACKLOG REFERENCE ONLY — not promoted to `bbi-build-state.md` or the launch tracker.

Generated overnight 2026-05-24 → 2026-05-25 against `main @ 0893b4a` for Day 11 LAUNCH-2.

---

## Executive Summary

- **3 competitors analyzed:** Sensyst (sensyst.com), The Office Shop (theofficeshop.ca), POI Business Interiors (poi.ca + store.poi.ca)
- **~22 pages surveyed** across the 3 sites, plus 5 SERP baselines and 5 AI-Overview-proxy queries
- **BBI vs competitor schema:** BBI's 11 distinct JSON-LD @types beats Office Shop (~12 with AggregateRating advantage), POI (6), Sensyst (2). BBI is structurally ahead on AEO.
- **AI Overview proxy:** Office Shop appears in 4/5 queries, Sensyst 1/5, POI 0/5, BBI 0/5 direct (1/5 via oecm.ca aggregator). Office Shop wins AEO despite shallow content — driven by LocalBusiness + AggregateRating + Review schema combo.
- **Biggest BBI gap:** No standalone Google Business Profile for "Brant Business Interiors." The 296 George St N location is registered as "Brant Basics" (4.4★ / 60 reviews). Competitors with weaker schema beat BBI in local pack because of GBP + review signals BBI doesn't currently emit.
- **17 backlog items generated** (5 HIGH, 7 MED, 5 LOW) — see Pattern Extraction + Backlog Items below.

**Methodology note:** DataForSEO MCP AI optimization endpoints returned HTTP 403 (the documented `DATAFORSEO-403` issue from Day 10 backlog). AI search citation analysis fell back to Google SERP snippets as an AI-Overview proxy, per the prompt's HARD RULES allowance.

---

## Pre-Launch SERP Baseline 2026-05-25

Captured first per Phase 1 priority — only recoverable pre-launch.

### Q1: "office furniture Ontario"

| # | URL | Title |
|---|---|---|
| 1 | surplusofficesale.com | Surplus Office Sales (Ontario CA — wrong geo, US noise) |
| 2 | atwork.ca | atWork Office Furniture Canada |
| 3 | **theofficeshop.ca** | **#1 Office Furniture Store in Toronto & Markham** |
| 4 | yelp.ca/Ontario CA | Yelp listings (US noise) |
| 5 | pnpofficefurniture.com | PnP Office Furniture |
| 6 | abcogroup.ca | ABCO Group |
| 7 | festivalfurniture.com | Festival Furniture (Stratford ON) |
| 8 | officestogo.com | Offices to Go |
| 9 | officestock.com | Officestock |
| 10 | barrysofficefurniture.com | Barry's Office Furniture (Toronto since 1981) |

- **Office Shop: #3** · **Sensyst: not in top 10** · **POI: not in top 10** · **BBI: not in top 10**
- SERP feature: US-noise pollution (2/10 are Ontario California results)

### Q2: "OECM office furniture supplier"

| # | URL | Title |
|---|---|---|
| 1 | oecm.ca/supplier-partners/korr-office-furniture/ | Korr Office Furniture |
| 2 | **oecm.ca/supplier-partners/office-central-inc/** | **Office Central Inc. (BBI parent legal entity)** |
| 3 | oecm.ca/marketplace/furniture-mattresses-and-related-services/ | OECM marketplace hub |
| 4 | beatties.com/office-furniture/oecm/ | Beatties OECM |
| 5 | oecm.ca/supplier-partners/cmg-office-interiors/ | CMG Office Interiors |
| 6 | **oecm.ca/supplier-partners/the-office-shop-inc/** | **The Office Shop (OECM profile)** |
| 7 | oecm.ca/supplier-partners/contemporary-office-interiors-ltd/ | Contemporary Office Interiors |
| 8 | oecm.ca/marketplace/office-space-furniture-and-related-services/ | OECM marketplace (office space) |
| 9 | oecm.ca/supplier-partners/capital-office-interiors-ltd/ | Capital Office Interiors |
| 10 | oecm.ca/supplier-partners/icon-office-environments/ | ICON Office Environments |

- **BBI: #2** — but only via the oecm.ca aggregator page (`/supplier-partners/office-central-inc/`), not via brantbusinessinteriors.com
- **Office Shop: #6** — also via oecm.ca aggregator
- **Sensyst: not in top 10** (Sensyst is NOT an OECM supplier — surface scan confirms)
- **POI: not in top 10** — surprising given POI IS an OECM supplier (per [oecm.ca/supplier-partners/poi-business-interiors-lp/](https://oecm.ca/supplier-partners/poi-business-interiors-lp/))

### Q3: "office furniture Peterborough"

| # | URL | Title |
|---|---|---|
| 1 | peterboroughofficesupplies.co.uk | Peterborough Office Supplies (UK — Cambridgeshire) |
| 2 | brothersofficefurniture.co.uk | Brothers Office Furniture (UK) |
| 3 | officestock.com/en-ca/peterborough | Officestock Peterborough (Canada) |
| 4 | ergooutlet.co.uk | Ergo Outlet (UK) |
| 5 | facebook.com/LOFOfficeFurniture | LOF Office Furniture (UK) |
| 6 | cityusedofficefurniture.co.uk | City Used Office Furniture (UK) |
| 7 | facebook.com/TCBOfficeFurniture | TCB Office Furniture Peterborough ON |
| 8 | stores.cort.com/new-hampshire/peterborough | CORT Peterborough NH (US) |
| 9 | peterboroughcraftworks.ca | Craftworks at the Barn (Peterborough ON) |
| 10 | niodonline.co.uk | NIOD Online (UK) |

- **7 of 10 results are UK/US** — Peterborough Cambridgeshire (UK) dominates Peterborough Ontario for organic search
- **BBI: not in top 10 for its own home city**
- **Sensyst / Office Shop / POI: all absent** (none specifically target Peterborough)
- SERP feature: heavy international (UK + NH) interference

### Q4: "Ontario school board office furniture"

| # | URL | Title |
|---|---|---|
| 1 | schoolfurnitureofcanada.ca | School Furniture of Canada |
| 2 | schoolfurniture.ca | School Furniture by Simplova |
| 3 | ascomanufacturing.com | ASCO Manufacturing (Toronto) |
| 4 | dsafurnishings.ca | DSA Furniture |
| 5 | alcoofcanada.net | Alco of Canada |
| 6 | oecm.ca/marketplace/furniture-mattresses-and-related-services/ | OECM marketplace |
| 7 | mitybilt.com | MityBilt Canadian Furniture |
| 8 | oecm.ca/supplier-partners/schoolhouse-products-inc/ | Schoolhouse Products (OECM profile) |
| 9 | cdispaces.ca | CDI Spaces |
| 10 | **theofficeshop.ca/services/office-furniture-for-educational-institutions/** | **The Office Shop — Education Solutions** |

- **Office Shop: #10** with a dedicated /services/ page — only one of the 3 competitors with an education-vertical landing page indexed
- **BBI: not in top 10** despite having `/pages/education` published (per CLAUDE.md row P1-7)
- **Sensyst / POI: not in top 10** despite both having education segments

### Q5: "office space planning Toronto"

| # | URL | Title |
|---|---|---|
| 1 | designbysda.com/office-space-planning-toronto-gta | Stephenson Design Associates |
| 2 | **theofficeshop.ca/office-design-services-toronto/** | **The Office Shop — Office Design Services Toronto** |
| 3 | toronto.ca/...office-space-needs-study | City of Toronto Office Space Needs Study |
| 4 | houzz.com | Houzz space-planning Toronto |
| 5 | parceleconomics.com/torontooffice | Parcel Economics |
| 6 | **sensyst.com** | **Commercial & Office Interior Design Firm in Toronto** |
| 7 | designbysda.com/office-space-design-toronto-gta | SDA — Office Space Design |
| 8 | studioforma.ca/office-interior-design-toronto | Studio Forma |
| 9 | thefurnitureguys.ca/space-planning-and-design | The Furniture Guys |
| 10 | depm-inc.com/depm-inc/space-planning | DEPM Inc. |

- **Office Shop: #2** (strong dedicated page) · **Sensyst: #6** · **POI: not in top 10** · **BBI: not in top 10**

### SERP baseline cross-summary

| Query | BBI rank | Sensyst | Office Shop | POI |
|---|---|---|---|---|
| office furniture Ontario | — | — | **#3** | — |
| OECM office furniture supplier | **#2** (via oecm.ca aggregator) | — | #6 (via aggregator) | — |
| office furniture Peterborough | — | — | — | — |
| Ontario school board office furniture | — | — | #10 | — |
| office space planning Toronto | — | #6 | **#2** | — |

**Conclusion:** BBI is invisible in 4/5 organic SERPs and only ranks via OECM.ca's aggregator on Q2. Office Shop dominates 4/5 queries with own-domain results. POI is invisible across all 5 despite being Canada's largest commercial dealer. Sensyst ranks once.

---

## Per-Competitor Scan

### Sensyst (Sensyst the Business Interiors Group)

**Domain:** [sensyst.com](https://sensyst.com/) · **Platform:** Shopify (content-only, no products sold online)
**Location:** 6805 Invader Crescent Unit 1, Mississauga ON L5T 2K6 · **Phone:** 905-565-9700 · **Email:** info@sensyst.com
**Founded:** 1977 (per About page, "Transforming Commercial Interiors Since 1977") · **Cert/Assoc:** ARIDO, IDC, BCIN

#### Pages surveyed

| URL | Title | Words | H1 | Schema @types |
|---|---|---|---|---|
| [/](https://sensyst.com/) | Commercial & Office Interior Design Firm in Toronto \| Sensyst | ~1,200–1,500 | "Workspaces Designed for People, Built for Growth" | Organization · WebSite+SearchAction |
| [/pages/about](https://sensyst.com/pages/about) | About Sensyst \| Office Interior Design Experts | ~3,500–4,000 | "About Sensyst" | Organization |
| [/blogs/projects](https://sensyst.com/blogs/projects) | Our Projects | ~1,100 | "Our Projects" | (Shopify defaults inherited) |
| [/blogs/projects/gatestone-co](https://sensyst.com/blogs/projects/gatestone-co) | Gatestone & Co Office Interior Design Project | ~250–300 | "Gatestone & Co." | Organization |
| [/pages/office-decor](https://sensyst.com/pages/office-decor) | Office Decor | ~1,200–1,400 | "Build an Office Your Team Loves" | (Shopify defaults inherited) |

#### Site inventory (per [sitemap_pages_1.xml](https://sensyst.com/sitemap_pages_1.xml?from=700029895020&to=706756477292) + [sitemap_blogs_1.xml](https://sensyst.com/sitemap_blogs_1.xml))

- **89 page URLs** including: 17 industry pages (automotive, banking, fintech, hospitality, engineering, manufacturing, logistics, real-estate, healthcare-medical, retail, non-profit-education, corporate-office, hybrid-workplaces, furniture-solutions), 5 gallery pages (acoustics, meeting, collaborative, support, work), **50+ geo-targeted pages** (Toronto + GTA municipalities + Toronto neighborhoods)
- **108 blog/project URLs** = 61 project case studies + 45 news articles + index pages
- News post cadence: 20/page × 4+ pages, range Feb 2024 → May 21 2026 ≈ 80+ posts over ~27 months ≈ **~3 posts/month**

#### Notable patterns

- **Case studies = leading content asset.** 61 projects, each with Area / Location / Industry / Services rendered as a structured spec block (e.g. "Gatestone & Co.": 16,000 sq ft · North York ON · Corporate · Plan/Design/Lease Acquisition/PM/Signage/Branding). Photo galleries embedded.
- **Heavy geo-targeting.** 50+ city/neighborhood pages — unusually deep geo strategy for a service-only Shopify site.
- **Service-led 4-step workflow.** Plan → Design → Build → Furnish.
- **Trust signals:** 4.9★ rating displayed on homepage; 7-8 client logos (Orangeville Chrysler, Aptum, Echologics, VersaPay, CANAM, Dealnet Capital, StarTech.com); ARIDO/IDC/BCIN designer credentials; leadership team of 10 with bios.
- **Schema is bare-minimum Shopify defaults** — Organization + WebSite/SearchAction sitewide and nothing custom on case-study pages.
- **No e-commerce.** Site lists no products; all CTAs route to /pages/contact for consultations.

---

### The Office Shop (The Office Shop Inc.)

**Domain:** [theofficeshop.ca](https://theofficeshop.ca/) · **Platform:** WordPress + Rank Math SEO plugin (confirmed by schema fingerprint)
**Location:** 366 Denison St, Markham ON L3R 1B9 · **Phone:** 905-305-9955 / 1-877-305-9955 · **Email:** info@theofficeshop.ca
**Hours:** Mo-Fr 9am-4pm, Sa-Su closed · **Founded:** 1996 by sisters Helen Stergiou + Joanne Triantafilou · **Cert:** WBE Canada (Women-Owned Business Enterprise)
**OECM:** YES — per [oecm.ca/supplier-partners/the-office-shop-inc/](https://oecm.ca/supplier-partners/the-office-shop-inc/)

#### Pages surveyed

| URL | Title | Words | H1 | Schema @types |
|---|---|---|---|---|
| [/](https://theofficeshop.ca/) | #1 Office Furniture Store in Toronto & Markham | ~5,500–6,000 | "Office Furniture is The Office Shop" | Person/Organization · WebSite+SearchAction · ImageObject · WebPage · Article · LocalBusiness · PostalAddress · ContactPoint · **AggregateRating** · **Review** (3 reviews embedded) |
| [/about-us/](https://theofficeshop.ca/about-us/) | About Us \| The Office Shop Ontario | ~2,800–3,000 | "About Us" | + BreadcrumbList |
| [/services/office-furniture-for-educational-institutions/](https://theofficeshop.ca/services/office-furniture-for-educational-institutions/) | Furniture Solutions for Educational Institutions | ~2,800 | "Office Furniture for Education..." | BreadcrumbList · LocalBusiness · AggregateRating · Review |
| [/contact-us/](https://theofficeshop.ca/contact-us/) | Contact Us \| Office Furniture \| The Office Shop Ontario | (not measured) | "Complete for a FREE consultation..." | + BreadcrumbList |
| [/resources/global-furniture-group-leader/](https://theofficeshop.ca/resources/global-furniture-group-leader/) | The Best Global Furniture Dealer in Canada | ~1,200–1,400 | "The Office Shop: The Best Global Furniture Dealer in Canada" | + **BlogPosting** + ListItem hierarchy |

#### Site inventory (per [/resources/](https://theofficeshop.ca/resources/) sidebar counts)

- **17 paginated resource pages** × ~4 per page ≈ ~68 articles total. Categories: Blogs (25), Brochures & Guides (7), Case Studies (4), Design Center (17), News-Media Mentions (1), Office Chairs (5), Uncategorized (8)
- Recent post: "Office Furniture Rental Toronto" 2026-05-23 — actively publishing

#### Notable patterns

- **AggregateRating + Review schema sitewide** — only competitor (and only entity in the comparison, including BBI) emitting structured review data. This is likely *why* Office Shop wins 4/5 AI Overview proxy queries despite shorter content.
- **Education page is 2,800 words but contains ZERO OECM mentions** — even though Office Shop is an OECM supplier. Big positioning miss they could fix, BBI is already exploiting (cornerstone OECM article published Day 10).
- **No FAQPage, Service, HowTo, or GovernmentService schema** despite content that would benefit from them. AEO gap.
- **Two-block schema strategy:** every page emits a page-specific block (Article/BlogPosting + Organization) + a sitewide LocalBusiness/Review block. Cleanly templated.
- **Trust signals:** 4.81★ / 65 Google reviews per [yably.ca](https://yably.ca/reviews/markham/office-shop-inc-366-denison-street); 2025+2026 Canadian Choice Award; clients include UHN, Sunnybrook, McMaster University, City of Markham, Country Day School; 60+ manufacturer partnerships; Premier Global Furniture Group dealer.
- **No e-commerce.** "Request a Quote" overlays only — no add-to-cart flow.

---

### POI Business Interiors (POI)

**Domain:** [poi.ca](https://www.poi.ca/) + [store.poi.ca](https://store.poi.ca/) · **Platform:** WordPress (main) + Shopify (store subdomain)
**Location:** 3389 Steeles Ave E Unit 120, North York ON M2H 3S8 · **Phone:** 1-888-296-9967 (main) / 905-479-1123 (store) · **Email:** av@poi.ca / info@poi.ca
**Hours:** Mo-Fr 8:30am-4:30pm · **Founded:** 1958 (3rd-gen Scholl family) · **Cert:** Great Place to Work Canada 2023; Steelcase Premier Partner
**OECM:** YES — per [oecm.ca/supplier-partners/poi-business-interiors-lp/](https://oecm.ca/supplier-partners/poi-business-interiors-lp/)
**Scale:** 160+ employees, 6 Ontario locations, 200+ manufacturer reps

#### Pages surveyed

| URL | Title | Words | H1 | Schema @types |
|---|---|---|---|---|
| [/](https://www.poi.ca/) | Toronto Business Interior Solutions \| inspired work. inspired life.™ | ~850 | (none) | LocalBusiness · PostalAddress · WebSite+SearchAction · WebPage · ContactPoint |
| [/about-us/](https://www.poi.ca/about-us/) | About Us — POI | ~1,100 | "About Us" | + BreadcrumbList |
| [/services/](https://www.poi.ca/services/) | Services — POI Business Interiors | ~3,200 | "Services" | + BreadcrumbList |
| [/case-studies-corporate/](https://www.poi.ca/case-studies-corporate/) | Corporate Case Studies \| POI Business Interiors | ~750 | "Corporate Case Studies" | + BreadcrumbList |
| [/connected-solutions/furniture/](https://www.poi.ca/connected-solutions/furniture/) | Modern Office Furniture Company in Toronto, Ontario \| POI | ~215 | "Furniture" | + BreadcrumbList |
| [/our-work/](https://www.poi.ca/our-work/) | Our Work \| POI Business Interiors | (not measured) | "Inspired Work" | (inherited) |
| [store.poi.ca/](https://store.poi.ca/) | The POI Store | (small catalog) | "The POI Store" | Organization · WebSite+SearchAction (Shopify defaults) |

#### Site inventory

- **31 case studies** indexed in /our-work/ (12 featured + 19 other) — clients include Brown Group, Nipissing-Parry Sound Catholic SB, Limberlost Place, U of T Scarborough, SickKids, Northleaf Capital, Sun Life Financial, Algoma U, Roserock, Toronto Region Board of Trade, Northland Power, Minto Group, Aviva Canada, Bentall Kennedy, Canon, RBC, Telus
- **~130 blog posts** (10 per page × 13 paginated index pages)
- **store.poi.ca** is a *separate, tiny* Shopify subdomain — 4 product categories (Task Seating, Custom Task Seating, Height Adjustable Desks, Accessories). Not a full catalog.

#### Notable patterns

- **Case studies feature multi-section narrative + embedded client testimonials + sq ft data** (Altus Group: 56,365 sq ft). Strongest case-study format of the 3 competitors.
- **5 distinct H2 service categories** on /services/ (Art Consultation, AV Integration, Facility Management, Relocation, Service Request) but **no Service schema markup** — AEO gap.
- **Strong vertical diversification.** Clients span corporate, healthcare (SickKids, Children First, College of Dental Hygienists, Canadian Hearing Services), education (5 institutions), government, financial services.
- **Steelcase is the spine.** Partnership since 1958. Steelcase Premier Partner designation prominently featured. POI is essentially Canada's Steelcase channel.
- **Trust signals:** 3.5–3.9★ across review platforms (45–56 reviews) per [yably.ca](https://yably.ca/reviews/north-york/poi-business-interiors-3389-steeles-ave-e-unit-120) and [Birdeye](https://reviews.birdeye.com/poi-business-interiors-167672524579902) — mixed/weaker than Office Shop despite POI being 4× the size.
- **No FAQPage / Service / HowTo / GovernmentService / BlogPosting / Article schema** despite a 130-post blog and 31 case studies. Significant AEO under-investment for the scale.

---

## Schema Comparison

| Schema Type | Sensyst | The Office Shop | POI | **BBI (LAUNCH-2)** |
|---|:---:|:---:|:---:|:---:|
| Organization | ✅ | ✅ (sitewide block 1) | — | ✅ |
| LocalBusiness | — | ✅ (sitewide block 2) | ✅ (sitewide) | ✅ (sitewide + dedicated `/pages/contact`) |
| WebSite + SearchAction | ✅ | ✅ | ✅ | ✅ |
| WebPage | — | ✅ | ✅ | — |
| BreadcrumbList | — | ✅ (on /about, /services, /resources) | ✅ (most pages) | ✅ (PDP) |
| Product + Offer | — | — | — | ✅ (every PDP) |
| Service | — | — | — | ✅ (`/pages/quote`, `/pages/delivery`, `/pages/relocation`) |
| FAQPage | — | — | — | ✅ (9 category pages, `/pages/oecm`, `/pages/quote`, blog post) |
| HowTo | — | — | — | ✅ (`/pages/design-services`) |
| GovernmentService | — | — | — | ✅ (`/pages/oecm` — unique to BBI) |
| BlogPosting | — | ✅ (resource articles) | — | ✅ (`/blogs/news/*`) |
| Article | — | ✅ (sitewide block on most pages) | — | — |
| ImageObject | — | ✅ | — | — |
| ContactPoint | — | ✅ (sitewide LocalBusiness block) | ✅ (sitewide) | — (covered inside LocalBusiness) |
| PostalAddress | — | ✅ | ✅ | ✅ (inside LocalBusiness) |
| **AggregateRating** | — | **✅** | — | **— ← GAP** |
| **Review** | — | **✅** (3 reviews embedded) | — | **— ← GAP** |
| Person | — | ✅ (founders/author) | — | — |

**Distinct schema-type count (approximate):**

- Sensyst: 2 (Shopify defaults only)
- The Office Shop: ~12 (richest competitor, AggregateRating + Review advantage)
- POI: 6 (sitewide LocalBusiness + breadcrumbs, no content-type schema despite blog volume)
- **BBI: 11** (strongest content-type schema; only one with FAQPage / Service / HowTo / GovernmentService / Product+Offer)

### Pattern observations

- **BBI is the only entity emitting GovernmentService schema** anywhere in this comparison. Combined with the OECM cornerstone article published Day 10, this is a real AEO moat IF Google/AI engines parse it correctly.
- **BBI is the only entity emitting HowTo schema.** Office Shop's resource library has plenty of how-to content but emits Article/BlogPosting, not HowTo.
- **BBI is the only entity with Product + Offer schema** because BBI is the only entity selling products online. Sensyst has zero products; POI has 4 categories on a subdomain.
- **AggregateRating + Review is the one Office Shop has that BBI doesn't.** Cited as the likely reason Office Shop wins AI Overview citations 4/5 times — review schema flags review-rich content to AI engines.
- **BBI's `business-furniture` collection has 0 FAQ blocks** (HIGH-4 in sys-verify-1-phase2). Universe of FAQs across the BBI catalog is otherwise 36 (per Day 8 AI-9), which exceeds anything visible on competitor sites.

---

## Content Pattern Analysis

| Pattern | Sensyst | Office Shop | POI | **BBI (current)** |
|---|---|---|---|---|
| Total page URLs | ~89 | unknown (large) | unknown | 25 published BBI pages |
| Case studies indexed | **61** (sq ft + sector + services metadata) | 4 | **31** (sq ft + multi-section narrative) | `/pages/customer-stories` + `/pages/our-work` (thin content) |
| Blog post inventory | **~80+** (45 news + 35+ across other handles) | ~25 blogs + ~68 total resources | **~130** | 2 articles (1 cornerstone + 1 how-to) |
| Latest blog publish | 2026-05-21 | 2026-05-23 | not dated on index | 2026-05-24 (OECM cornerstone) |
| Blog cadence (est.) | ~3 posts/month | ~2-3 posts/month | unknown but heavy | 1 cornerstone + ~10 batch backlog planned |
| Geo-targeted pages | **~50+** (Toronto + GTA cities + neighborhoods) | location section in nav, no dedicated city pages spotted | 6 location pages (showrooms) | 0 |
| Industry/vertical pages | **17** (automotive, fintech, hospitality, engineering, manufacturing, etc.) | 4 (commercial, education, healthcare, home office) | 4 segments (corporate, education, healthcare, government) | **5** (healthcare, education, government, non-profit, professional-services) |
| FAQ density | Footer FAQ link only | FAQ link in nav | not surfaced | **36 FAQs across 9 category templates** + page-level FAQs on OECM, quote, blog cornerstone |
| Workflow / numbered process | 4-step (Plan/Design/Build/Furnish) on homepage | "Our Process" on /about-us | (not surfaced) | HowTo schema on `/pages/design-services` |
| Cornerstone-length article (>2k words) | 80+ posts but most are blurbs | yes — "Best Global Furniture Dealer" 1,200-1,400w | not surfaced | yes — OECM article 2,446w / 16,600 chars |
| Comparison tables | not surfaced | not surfaced | not surfaced | yes — 3 in OECM cornerstone article (Direct Award vs Open RFP / Eligible Sectors / Coverage 2025-470) |
| Internal link density | moderate (case study cross-links) | high (resource library inter-links) | moderate (category cross-links) | high in OECM article (8 internal links within target 5-8) |
| Product-page depth | 0 PDPs (no e-commerce) | overlay-only "Request a Quote" | 4 categories on store.poi.ca | **330 products** with specs, images, additionalProperty schema |

### Cross-competitor content observations

1. **Sensyst is a content production machine for SEO.** ~197 URL inventory with dedicated pages per industry, per city, per neighborhood. This is the playbook for owning a geo+vertical matrix at scale.
2. **Office Shop is dense per page** (5,500w homepage, 2,800w service pages). Heavy keyword targeting, classic WordPress-Rank-Math approach.
3. **POI is bottom-heavy on case studies** — fewer pages but each one is a deep narrative (Altus 56,365 sq ft case study format with embedded testimonials and outcomes).
4. **BBI's strength is structured Q&A density** — 36 FAQs across category templates is more granular Q&A schema than any competitor surfaces. The OECM cornerstone's 6 procurement-actionable Q&As + 3 comparison tables format is a *better AI Overview hook* than what competitors publish — but it's a single article vs competitor portfolios in the dozens.
5. **No competitor leads with OECM** even though 2 of the 3 (Office Shop, POI) are OECM-listed suppliers. Office Shop's education page contains zero OECM references. BBI's `/pages/oecm` + cornerstone article uniquely owns this positioning.

---

## AI Search Citation Check

**Methodology limitation:** DataForSEO's `ai_optimization_chat_gpt_scraper` and `ai_optimization_llm_models` returned HTTP 403 across all attempts (consistent with the documented `DATAFORSEO-403` issue from Day 10 backlog — likely tier/subscription scope). Perplexity's `/search?q=…` URL returned 403 to WebFetch. Per the prompt HARD RULES, falling back to Google SERP snippets as an AI-Overview proxy (the prompt explicitly permits: *"featured snippets in Google search results often mirror AI citations"*).

### 5 AI-relevant queries × proxy citations

#### Q1: "Best office furniture supplier in Ontario for large fit-outs"

Proxy results from Google SERP for [the equivalent search](https://www.google.com/search?q=best+office+furniture+supplier+Ontario+large+fit-outs):

| Cited entity | Position | Source |
|---|---|---|
| atWork | top | atwork.ca |
| **The Office Shop** | top-3 | theofficeshop.ca |
| Toronto Office Furniture Inc. | top | torontoofficefurniture.com |
| ABCO Group | top | abcogroup.ca |
| Source Office Furniture | top | sourceofficefurniture.ca |

- **Sensyst: not cited** · **POI: not cited** · **BBI: not cited**

#### Q2: "Office furniture for Ontario school boards"

Per Phase 1 Q4 SERP (same query):

| Cited entity | Source |
|---|---|
| School Furniture of Canada | schoolfurnitureofcanada.ca |
| OECM marketplace | oecm.ca |
| ASCO Manufacturing | ascomanufacturing.com |
| Schoolhouse Products | oecm.ca/supplier-partners/schoolhouse-products-inc/ |
| **The Office Shop** | theofficeshop.ca/services/office-furniture-for-educational-institutions/ |

- **Sensyst: not cited** · **POI: not cited** · **BBI: not cited**

#### Q3: "Commercial office furniture dealer Toronto GTA"

Proxy results from [the equivalent search](https://www.google.com/search?q=commercial+office+furniture+dealer+Toronto+GTA):

| Cited entity | Source |
|---|---|
| **The Office Shop** | theofficeshop.ca/services/commercial-office-furniture-ontario-gta/ (dedicated page!) |
| Source Office Furniture | sourceofficefurniture.ca/office-furniture-gta |
| GTA Office Furniture | gtaofficefurniture.com |
| Barry's Office Furniture | barrysofficefurniture.com |
| Blair's atWork | atwork.ca |

- **Sensyst: not cited** · **POI: not cited** · **BBI: not cited**

#### Q4: "OECM office furniture supplier Ontario"

Per Phase 1 Q2 SERP:

- **BBI: cited at #2** via `oecm.ca/supplier-partners/office-central-inc/` aggregator
- **Office Shop: cited at #6** via same aggregator
- **Sensyst: not cited** (not OECM-registered)
- **POI: not cited** (despite being OECM-listed — Google does not surface POI's OECM profile for this query)

#### Q5: "Office space planning + furniture procurement Ontario"

Proxy results from [the equivalent search](https://www.google.com/search?q=office+space+planning+furniture+procurement+Ontario):

| Cited entity | Source |
|---|---|
| atWork Office Furniture Canada | atwork.ca |
| **The Office Shop** | theofficeshop.ca/services/space-planning-and-design/ |
| Ugoburo | ugoburo.ca |
| OECM | oecm.ca/marketplace/office-space-furniture-and-related-services/ |
| University of Toronto Procurement Services | procurement.utoronto.ca |

- **Sensyst: cited** for Toronto-specific design context (separate Phase 1 SERP Q5 = #6)
- **POI: not cited** · **BBI: not cited**

### AI search citation cross-summary

| Query | The Office Shop | Sensyst | POI | BBI |
|---|:---:|:---:|:---:|:---:|
| Best supplier Ontario large fit-outs | ✅ | — | — | — |
| Ontario school board office furniture | ✅ | — | — | — |
| Commercial dealer Toronto GTA | ✅ | — | — | — |
| OECM office furniture supplier Ontario | ✅ (via aggregator) | — | — | ✅ (via aggregator only) |
| Office space planning Ontario | ✅ | ✅ (Toronto context) | — | — |
| **Direct hits (own domain)** | **4** | **1** | **0** | **0** |

### Why Office Shop wins despite shallow content

Combining schema + content + GBP evidence: Office Shop is the only entity in the comparison emitting AggregateRating + Review schema (3 reviews embedded sitewide), backed by a real 4.81★ / 65 Google reviews GBP presence. AI Overview/citation engines weigh review-rich entities heavily for commercial-intent queries. Office Shop also has clean per-page Article + BreadcrumbList + LocalBusiness blocks via Rank Math — every page is a complete schema unit. BBI matches or exceeds on every type EXCEPT AggregateRating/Review and GBP visibility.

---

## GBP / Local SEO Visibility

| Entity | Address | Hours | Reviews / Rating | Knowledge Panel Signal |
|---|---|---|---|---|
| **Sensyst** | 6805 Invader Crescent Unit 1, Mississauga ON L5T 2K6 | Not displayed on yellowpages.ca | **0 reviews** on Yellow Pages | weak |
| **The Office Shop** | 366 Denison St, Markham ON L3R 1B9 | **Mo-Fr 9am-4pm** | **4.81★ / 65 Google reviews** ([yably.ca](https://yably.ca/reviews/markham/office-shop-inc-366-denison-street)) | strong |
| **POI Business Interiors** | 3389 Steeles Ave E Unit 120, North York ON M2H 3S8 | **Mo-Fr 8:30am-4:30pm** | **3.5–3.9★ / 45-56 reviews** (mixed across platforms) | medium |
| **BBI / Office Central** (296 George St N Peterborough — *registered as "Brant Basics"*) | 296 George St N, Peterborough ON K9J 3H2 | **Mo-Fr 9am-5pm** (Brant Basics) | **4.4★ / 60 reviews** ([yably.ca](https://yably.ca/reviews/peterborough/brant-basics-296-george-street-north)) — but under "Brant Basics" name | **misattributed** — BBI/Brant Business Interiors has no surfaceable own-name GBP |

### Critical finding

The 296 George St N location is registered as **"Brant Basics"** with its own 4.4★ / 60-review GBP. Searching for "Brant Business Interiors" or "Office Central Peterborough" specifically does NOT surface a dedicated GBP — BBI is piggybacking on Brant Basics' presence. For Q3 SERP ("office furniture Peterborough"), this misattribution means BBI is invisible in its own home city while UK Peterborough listings dominate.

### Hours mismatch flag

BBI's site-emitted Organization+LocalBusiness JSON-LD declares `Mo-Fr 09:00-17:00` ([sys-verify-1-phase2 Phase 6](data/reports/sys-verify-1-phase2-2026-05-24.md)). The Brant Basics GBP shows Mo-Fr 9am-5pm. These are consistent. But there's no cross-platform JSON-LD ↔ GBP verification chain because the GBP is under a different legal-entity name.

---

## Pattern Extraction

### What's working for competitors that BBI doesn't do yet

1. **AggregateRating + Review schema embedded sitewide** (Office Shop) — translates real Google reviews into structured data AI engines weight heavily.
2. **Standalone GBP with own-name** (all 3 competitors). BBI's GBP attribution is split between Brant Basics (active, 4.4★) and Brant Business Interiors (essentially absent).
3. **Heavy geo-page coverage** (Sensyst: 50+ city/neighborhood pages). Captures local-intent long-tail traffic BBI currently cedes.
4. **Case study depth + structure** (Sensyst's sq ft / location / sector / services metadata block; POI's multi-section narrative + embedded testimonials).
5. **Resource library volume + cadence** (Office Shop 68 articles, Sensyst 80+ news posts, POI ~130 posts at weekly+ cadence).
6. **Industry page breadth** (Sensyst 17 industry pages; BBI has 5).
7. **Client logo bar with real brand names** (all 3 competitors). BBI's homepage currently uses gradient placeholders (MED-1 in sys-verify-1-phase2).
8. **Newsletter signup** (Office Shop + POI have prominent newsletter CTAs). BBI has no captured-email channel.
9. **Designer credentials displayed** (Sensyst: ARIDO + IDC + BCIN). BBI has OECM Supplier Partner but no design-profession credentials surfaced.
10. **Press release / news cadence** (POI leads blog with DTS acquisition announcement; Office Shop announces 2025+2026 Canadian Choice Award). BBI has no press post stream.

### What's working for competitors that BBI already does (validates strategy)

1. **OECM positioning** — Office Shop and POI are both OECM suppliers but neither leads with it. BBI's `/pages/oecm` + cornerstone article uniquely own this. ([sys-verify-1-phase2 Phase 3](data/reports/sys-verify-1-phase2-2026-05-24.md))
2. **GovernmentService + HowTo + FAQPage schema combo** — no competitor matches BBI's content-type schema depth.
3. **Comparison tables in cornerstone content** — none of the 3 competitors use comparison tables. BBI's OECM article uses 3 (Direct Award vs Open RFP, Eligible Sectors, Coverage 2025-470). This is a *better-than-competition* AI Overview pattern.
4. **Structured Q&A density** — BBI's 36 FAQs across 9 category templates is more granular than anything visible on competitor sites.
5. **OECM Agreement 2025-470 mentions** — BBI's cornerstone article mentions Agreement 2025-470 30 times; competitors don't reference specific agreement numbers.
6. **Founding year + family-owned narrative** — BBI 1964 (older than Office Shop 1996 and Sensyst 1977; POI 1958 is older). All 4 lean on heritage; BBI's positioning is solid.

### What's NOT in their playbook that BBI could win on

1. **E-commerce checkout for quick-ship SKUs.** Sensyst has zero products. Office Shop has "Request a Quote" overlays only. POI's store.poi.ca is a tiny 4-category seating shop. BBI has a fully functioning 330-product cart with dual buying mode per ICP. This is a moat IF customers want self-serve flow (which per ICP data ~80% of order count is self-serve already).
2. **Combined OECM Agreement 2025-470 + GovernmentService schema + cornerstone article.** Office Shop and POI both have OECM agreements but neither structures the content for AI parsing. BBI's `/pages/oecm` is the only OECM education hub of the 4.
3. **Brant Basics as a partner-brand cross-reference.** Brant Basics has the GBP, the reviews, and a PSAB-recognized supplier status. None of the 3 competitors have an Indigenous-procurement angle equivalent.
4. **Spec-rich PDPs** with `additionalProperty` schema from metafields (Day 8 AI-3). Competitors lack product depth entirely.
5. **Peterborough as a home-base hub.** Competitors all target Toronto + GTA. Peterborough has minimal Ontario-side competition for organic — BBI is *one geo page away* from owning it.

---

## Backlog Items (HIGH / MED / LOW)

Each item is tagged HIGH / MED / LOW, scoped (~30 min / ~1–2 hr / multi-session), and tied to a specific phase finding with cited source URL.

### HIGH (5)

#### [HIGH-A] GBP-RECLAIM — Claim or migrate a standalone "Brant Business Interiors" Google Business Profile

- **Source observation:** Phase 6 — 296 George St N is registered as "Brant Basics" at [yably.ca/reviews/peterborough/brant-basics-296-george-street-north](https://yably.ca/reviews/peterborough/brant-basics-296-george-street-north) (4.4★ / 60 reviews). Searching "Brant Business Interiors Peterborough" surfaces no own-name GBP. Phase 1 Q3 ("office furniture Peterborough") shows BBI invisible in its own home city while UK Peterborough results dominate.
- **Action:** Decide between (a) creating a new GBP for "Brant Business Interiors / Office Central" at the same 296 George St N address, or (b) renaming the existing Brant Basics GBP to dual-name "Brant Basics + Brant Business Interiors". Option (b) preserves 60 reviews; option (a) requires postcard verification (~2 weeks) and starts review count at 0. Recommend (b) — dual-name with the 60 existing reviews ported.
- **Effort:** 1–2 hr decision + submission; verification card ~2 weeks; ongoing review-solicitation campaign.
- **Expected impact:** Local pack inclusion for "office furniture Peterborough" + Kawartha Lakes + Northumberland queries. Star-rating display in SERPs. Knowledge panel parity with competitors. Foundational for HIGH-B.

#### [HIGH-B] AGGREGATE-RATING-SCHEMA — Add AggregateRating + Review JSON-LD sitewide

- **Source observation:** Phase 3 schema comparison. Office Shop emits AggregateRating + Review on every page ([theofficeshop.ca](https://theofficeshop.ca/)). BBI's `bbi-org-schema.liquid` snippet does not include either type. ([sys-verify-1-phase2 Phase 3](data/reports/sys-verify-1-phase2-2026-05-24.md)).
- **Action:** After HIGH-A resolves, wire AggregateRating + Review (Reviews pulled from GBP API or hand-curated top 3-5 reviews) into `theme/snippets/bbi-org-schema.liquid` adjacent to the existing LocalBusiness block. Schema fields: `ratingValue`, `reviewCount`, plus 3–5 `Review` items with `author`, `reviewRating`, `reviewBody`.
- **Effort:** 1 hr after HIGH-A.
- **Expected impact:** Closes the single biggest BBI vs Office Shop AEO gap. Likely lifts BBI into AI Overview citations for the 5 proxy queries currently dominated by Office Shop.

#### [HIGH-C] PETERBOROUGH-GEO-HUB — Build dedicated `/pages/peterborough-office-furniture` landing page

- **Source observation:** Phase 1 Q3 "office furniture Peterborough" SERP — 7 of 10 results are UK Peterborough (Cambridgeshire). BBI's home city is uncovered. Sensyst has 50+ comparable geo pages ([sitemap_pages_1.xml](https://sensyst.com/sitemap_pages_1.xml?from=700029895020&to=706756477292)). BBI has 0.
- **Action:** Create `/pages/peterborough-office-furniture` (~600–800 words) with: hero anchored to Peterborough + Kawartha region, LocalBusiness schema, 4-6 FAQs (delivery to Peterborough, install service area, local clients, OECM applicability), 1-2 internal links to `/pages/oecm` + `/pages/quote`, embed real Peterborough client logos if available.
- **Effort:** 2–3 hr (DataForSEO KW pull required per CLAUDE.md SEO-AUDIT-2 rule before publishing) + ds-lp section template.
- **Expected impact:** Capture Peterborough + Kawartha Lakes + Northumberland local-intent traffic currently lost to UK Peterborough results.

#### [HIGH-D] CASE-STUDY-DEPTH-UPGRADE — Publish 3–5 case studies with structured metadata block

- **Source observation:** Sensyst has 61 case studies with sq ft + sector + services metadata block ([/blogs/projects/gatestone-co](https://sensyst.com/blogs/projects/gatestone-co)). POI has 31 with multi-section narrative + testimonials ([/case-studies-corporate/](https://www.poi.ca/case-studies-corporate/), Altus 56,365 sq ft). BBI's `/pages/customer-stories` + `/pages/our-work` are present but content depth is thin — the OECM cornerstone validates Halton Catholic DSB (320 ergoCentric chairs, 11 schools) as a single mention rather than a full case study page.
- **Action:** Choose 3-5 of BBI's strongest projects (Halton Catholic DSB is the obvious lead given Day 10 article work). Build a `case-study` content template with: hero photo, project specs block (sq ft / location / sector / services / brands), 800-1,200 word narrative (challenge → solution → outcome), 4-6 photos, client quote if available, CTA pair (Request Quote + Phone). Add to /pages/customer-stories index with grid layout. Consider GovernmentService schema where applicable (school boards).
- **Effort:** 4–6 hr per case study × 3-5 case studies = 12–30 hr total. Spread across post-launch weeks 2–4.
- **Expected impact:** Closes the case-study depth gap vs Sensyst + POI. Each case study is also reusable as social proof in /pages/oecm + industry pages.

#### [HIGH-E] CLIENT-LOGO-BAR-REAL — Replace homepage gradient placeholders with real client logos

- **Source observation:** All 3 competitors display 7–15 real client logos prominently (Sensyst: 7-8 logos including Orangeville Chrysler/Aptum/Echologics/VersaPay/CANAM/Dealnet/StarTech; Office Shop: UHN/Sunnybrook/McMaster/Markham/etc.; POI: Aviva/Canon/Bentall Kennedy/Finastra/RBC/Telus). BBI homepage currently uses `.bbi-hp-ph--*` gradient CSS placeholders ([sys-verify-1-phase2 MED-1](data/reports/sys-verify-1-phase2-2026-05-24.md)).
- **Action:** Compile permission-granted client logo set from existing customer base (cross-reference data/oci-photos catalog + Day 10 case study research). Add a "Trusted by" logo strip to homepage above the OECM section. Use grayscale + hover color for design coherence with the DS rebuild.
- **Effort:** 2–3 hr (logo permission tracking) + 1 hr implementation. Logo permission outreach can be batched with HIGH-D case study client outreach.
- **Expected impact:** Brand trust signal on first scroll. Drops the "unfinished" perception competitors don't trigger.

### MED (7)

#### [MED-A] GEO-LANDING-PAGE-EXPANSION — Build 5-10 city/region pages mirroring Sensyst's pattern

- **Source observation:** Sensyst has 50+ geo pages ([sitemap](https://sensyst.com/sitemap_pages_1.xml?from=700029895020&to=706756477292)). BBI has 0. Per ICP — Ontario (Peterborough, Toronto, Mississauga, Ottawa, London) + Western Canada (Vancouver, Calgary, Edmonton, Winnipeg) are the priority hubs.
- **Action:** Sequence after HIGH-C (Peterborough first as the template). Mirror Peterborough structure for: Toronto, Mississauga, Ottawa, Vancouver, Calgary. Each ~600 words + LocalBusiness schema + 4-6 region-specific FAQs (delivery zone, install availability, regional clients).
- **Effort:** ~2 hr per page × 5-10 pages = 10–20 hr. Spread across post-launch weeks 3–6.
- **Expected impact:** Mirrors Sensyst's geo capture playbook for ICP A+B regions per [docs/strategy/icp.md](docs/strategy/icp.md).

#### [MED-B] INDUSTRY-PAGE-EXPANSION — Add 4-5 vertical pages closing the gap to Sensyst's 17

- **Source observation:** Sensyst has 17 industry pages. BBI has 5 (`/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/non-profit`, `/pages/professional-services`). Per ICP B private-sector targets, the missing high-relevance verticals are: manufacturing, logistics-and-trades, retail / hospitality, financial-services / accounting, law-firms.
- **Action:** Build 4-5 of: `/pages/manufacturing`, `/pages/logistics`, `/pages/legal-and-accounting`, `/pages/retail-hospitality`. Mirror existing P1-6 ds-lp-* template. Add Service schema where applicable.
- **Effort:** 3–4 hr per page × 4-5 pages.
- **Expected impact:** Captures SMB private-sector vertical intent traffic (ICP B per [icp.md](docs/strategy/icp.md)).

#### [MED-C] BLOG-VOLUME-RAMP — Restart blog cadence at 1-2 posts/month

- **Source observation:** Sensyst publishes ~3/month, Office Shop ~2-3/month, POI weekly+. BBI has 2 published articles total. Even at 1 post/month, BBI takes years to match competitor inventory.
- **Action:** Activate the BL-* / B1..B10 backlog from [CLAUDE.md](CLAUDE.md). Each post must follow the DataForSEO MCP KW pull rule (mandatory per CLAUDE.md before any blog brief). Prioritize: (1) "Office furniture for Ontario schools without RFP" (extension of Day 10 cornerstone), (2) "Healthcare clinic furniture buying guide" (BBI's healthcare niche), (3) "OECM vs RFP procurement timelines" (extends comparison-table pattern).
- **Effort:** ~6–10 hr per post (KW research + draft + review + publish + JSON-LD verify).
- **Expected impact:** Compounding domain authority + AI Overview citation eligibility. Topical depth around procurement + verticals.

#### [MED-D] DOWNLOADABLE-BROCHURES — Add 1-2 PDF brochures for institutional procurement teams

- **Source observation:** Office Shop's resource library has 7 "Brochures & Guides" ([/resources/](https://theofficeshop.ca/resources/)). POI links to `BROCHURE_POI_RELOCATION_MANAGEMENT_BROCHURE_15OCT2012.pdf` + a POI overview PDF. BBI has no PDF download channel.
- **Action:** Build 2 PDFs: (1) "Brant Business Interiors — Capability Statement" (1-pager with company overview, OECM, key brands, contact), (2) "OECM Procurement Guide for Ontario School Boards" (extends Day 10 cornerstone — 4-6 pages with workflow + Q&A). Host in Shopify Files; surface from /pages/oecm + /pages/education.
- **Effort:** 4–6 hr per PDF (design + content + review).
- **Expected impact:** Procurement-team friendly trust signal. Reusable in cold outreach and sales conversations.

#### [MED-E] NEWSLETTER-CAPTURE — Add email signup CTA to footer + key pages

- **Source observation:** Office Shop has a "Sign up for The Office Shop Newsletter" form. POI has "Subscribe to our Email Newsletter!" H2. BBI has no captured-email channel.
- **Action:** Wire a Klaviyo (or Shopify Email native) signup form into `bbi-footer.liquid` + `/pages/oecm` exit-intent. Lightweight: name + email + (optional) procurement role.
- **Effort:** 2–3 hr (form + segment setup) + ongoing list management.
- **Expected impact:** Captured procurement contacts for nurture. Distribution channel for case studies + OECM updates.

#### [MED-F] TEAM-BIOS-PAGE — Surface BBI / Brant Basics team on /pages/about

- **Source observation:** Sensyst has 10 leadership bios + ARIDO/IDC/BCIN designer credentials ([/pages/about](https://sensyst.com/pages/about)). POI lists 11. Office Shop names the 2 founder sisters. BBI's `/pages/about` doesn't currently feature an extended team bio.
- **Action:** Add a "Meet the team" section with 4-8 staff photos + role + 2-sentence bio. Highlight Steve Katz as 2nd-generation Peterborough family business. Highlight any in-house designer credentials.
- **Effort:** 4–6 hr (photos + bio copy + permission).
- **Expected impact:** Family-business / human-trust signal per ICP voice rules ("Canadian-owned · Since 1964"). Useful internal-link target from case studies.

#### [MED-G] SERVICE-AREA-PAGE — Build `/pages/service-area` summarizing delivery + install zones

- **Source observation:** Sensyst lists service across GTA + 50+ Ontario cities. POI lists 6 Ontario locations. BBI's ICP says "delivery across Canada + installation Ontario + Western Canada" but no dedicated page surfaces this. ([icp.md](docs/strategy/icp.md))
- **Action:** Build `/pages/service-area` with: map graphic, install zone list (Ontario + BC/AB/SK/MB), delivery-only zone list (Atlantic + territories), Quebec exclusion note, Service schema. Cross-link from /pages/delivery + /pages/relocation.
- **Effort:** 2–3 hr.
- **Expected impact:** Clear procurement-friendly answer to "do you serve [my region]" without a phone call.

### LOW (5)

#### [LOW-A] CASE-STUDY-METADATA-STANDARDIZATION — Match Sensyst's structured spec block

- **Source observation:** Sensyst case studies expose Area / Location / Industry / Services as a structured spec block ([gatestone-co](https://sensyst.com/blogs/projects/gatestone-co)). POI lists clients but inconsistent sq ft visibility.
- **Action:** Once HIGH-D case study work begins, formalize the spec block template: `Square Footage | Location | Industry/Vertical | Services Provided | Brands Featured | Year Completed`. Apply consistently across the 3-5 first case studies.
- **Effort:** 1 hr template work + 30 min per case study during HIGH-D.
- **Expected impact:** Consistent structured-data parsing for AI engines; consistent UX across customer-stories.

#### [LOW-B] DESIGNER-CREDENTIAL-BAR — Display any in-house design credentials (ARIDO, IDC, BCIN)

- **Source observation:** Sensyst displays ARIDO + IDC + BCIN ([/pages/about](https://sensyst.com/pages/about)). POI displays Steelcase Premier Partner + Great Place to Work 2023.
- **Action:** Confirm whether any BBI staff hold ARIDO / IDC / IIDA / IDS designations. If yes, add to footer + /pages/about. If no, skip — don't claim what isn't held.
- **Effort:** 30 min discovery + 1 hr implementation if applicable.
- **Expected impact:** Designer-trust signal for design-services positioning.

#### [LOW-C] PRESS-RELEASE-CADENCE — Establish a press post stream when news happens

- **Source observation:** POI's blog leads with DTS acquisition announcement ([/blog/we-are-expanding/](https://www.poi.ca/blog/we-are-expanding/)). Office Shop announces 2025+2026 Canadian Choice Award.
- **Action:** When BBI / Brant Basics has newsworthy events (new OECM agreement, new partnership, new hire, new location, award), post to `/blogs/news/` and cross-promote. No fixed cadence — opportunistic.
- **Effort:** 1-2 hr per post when news warrants.
- **Expected impact:** Topical freshness for SEO; positions BBI as an active business not a dormant catalog.

#### [LOW-D] SHOPIFY-FACING-COMPETITOR-NOTE — Document Sensyst's Shopify usage as content-only

- **Source observation:** Sensyst is on Shopify but sells no products. URL patterns (`/pages/`, `/blogs/`) confirm. They use Shopify as a content CMS, not e-commerce.
- **Action:** Note this in `docs/strategy/competitor-research/` (or wherever competitor docs live). Reference for any future debate about whether BBI should de-emphasize products.
- **Effort:** 15 min note.
- **Expected impact:** Strategic note for future planning conversations.

#### [LOW-E] OECM-MOAT-MONITORING — Watch whether Office Shop / POI start surfacing OECM content

- **Source observation:** Phase 3 — Office Shop's education page contains zero OECM references despite being an OECM supplier. POI similarly under-positions OECM. BBI's OECM cornerstone + GovernmentService schema is currently uncontested.
- **Action:** Quarterly recon — re-check Office Shop + POI sitemaps + education / school-board service pages for OECM content additions. If they start matching BBI's positioning, re-evaluate.
- **Effort:** 30 min per quarter.
- **Expected impact:** Early warning if competitors close the OECM positioning gap.

---

## Methodology Notes

### Tools used

- WebSearch (Google SERP retrieval)
- WebFetch (page content extraction — note: markdown conversion strips `<script>` blocks, so JSON-LD verification required raw curl)
- Bash + Python (raw curl + regex/JSON parsing for accurate JSON-LD @type extraction)
- DataForSEO MCP `ai_optimization_chat_gpt_scraper` (attempted — returned HTTP 403)
- DataForSEO MCP `ai_optimization_llm_models` (attempted — returned HTTP 403)

### Pages successfully scraped

22 distinct URLs across 3 competitor domains + 4 OECM aggregator URLs + 9 GBP-context URLs.

### Pages failed (403 / JS-render / rate limit)

- `https://www.poi.ca/about/` — 404 (corrected to `/about-us/`)
- `https://www.poi.ca/sitemap.xml` — 404 (no public sitemap surfaced)
- `https://theofficeshop.ca/blog/` — 404 (resource library lives at `/resources/`)
- `https://www.perplexity.ai/search?q=…` — 403 (auth-gated)
- DataForSEO AI optimization endpoints — 403 (consistent with documented DATAFORSEO-403 backlog issue)

### AI platforms successfully queried

None directly. Substituted Google SERP snippets as AI-Overview proxy per the prompt's HARD RULES allowance.

### AI platforms unavailable

- ChatGPT (auth-gated; DataForSEO scraper 403)
- Gemini (auth-gated; not attempted given Perplexity + ChatGPT both blocked)
- Perplexity (search URL 403; DataForSEO scraper 403)

### Hand-judgment calls made

1. **Recommended Option (b) for GBP reclaim** (rename Brant Basics to dual-name) over Option (a) (new GBP) — preserves 60 existing reviews. Worth a strategy conversation before implementation.
2. **Scoped HIGH-D case studies to 3-5** rather than matching Sensyst's 61 — diminishing returns past 5 for the foreseeable LAUNCH-2 + post-launch window.
3. **Used Google SERP as AI Overview proxy** when AI endpoints all 403'd — explicitly permitted by prompt HARD RULES.
4. **Did NOT verify whether POI's `/our-work/` has internal per-vertical pages** (healthcare-specific, education-specific) — surface scan only per Approach A.
5. **Treated Office Central Inc. (oecm.ca/supplier-partners/office-central-inc/) as a BBI proxy** — the OECM-listed legal entity. Same business, different URL.

### Limitations of surface-level (Approach A)

- Backlink profiles not measured (would require Ahrefs/SEMrush — DataForSEO `backlinks_*` available but not exercised this session per "approach A" scoping).
- Paid traffic / ad spend not measured.
- Email funnel performance not measured.
- Pages behind JS rendering (SPA frameworks) not exercised — none of the 3 competitors appear to be SPAs.
- Per-page Lighthouse / Core Web Vitals not measured (post-launch SEO-AUDIT-1 follow-up).
- Per-product PDP schema audit not performed (none of 3 competitors have meaningful PDPs to compare to BBI's 330-product catalog).

---

## Sources

### Competitor sites

- [sensyst.com/](https://sensyst.com/)
- [sensyst.com/pages/about](https://sensyst.com/pages/about)
- [sensyst.com/pages/office-decor](https://sensyst.com/pages/office-decor)
- [sensyst.com/blogs/projects](https://sensyst.com/blogs/projects)
- [sensyst.com/blogs/projects/gatestone-co](https://sensyst.com/blogs/projects/gatestone-co)
- [sensyst.com/blogs/news](https://sensyst.com/blogs/news)
- [sensyst.com/sitemap_pages_1.xml](https://sensyst.com/sitemap_pages_1.xml?from=700029895020&to=706756477292)
- [sensyst.com/sitemap_blogs_1.xml](https://sensyst.com/sitemap_blogs_1.xml)
- [theofficeshop.ca/](https://theofficeshop.ca/)
- [theofficeshop.ca/about-us/](https://theofficeshop.ca/about-us/)
- [theofficeshop.ca/services/office-furniture-for-educational-institutions/](https://theofficeshop.ca/services/office-furniture-for-educational-institutions/)
- [theofficeshop.ca/contact-us/](https://theofficeshop.ca/contact-us/)
- [theofficeshop.ca/resources/](https://theofficeshop.ca/resources/)
- [theofficeshop.ca/resources/global-furniture-group-leader/](https://theofficeshop.ca/resources/global-furniture-group-leader/)
- [www.poi.ca/](https://www.poi.ca/)
- [www.poi.ca/about-us/](https://www.poi.ca/about-us/)
- [www.poi.ca/services/](https://www.poi.ca/services/)
- [www.poi.ca/case-studies-corporate/](https://www.poi.ca/case-studies-corporate/)
- [www.poi.ca/connected-solutions/furniture/](https://www.poi.ca/connected-solutions/furniture/)
- [www.poi.ca/our-work/](https://www.poi.ca/our-work/)
- [www.poi.ca/blog/](https://www.poi.ca/blog/)
- [store.poi.ca/](https://store.poi.ca/)

### OECM aggregator

- [oecm.ca/supplier-partners/office-central-inc/](https://oecm.ca/supplier-partners/office-central-inc/)
- [oecm.ca/supplier-partners/the-office-shop-inc/](https://oecm.ca/supplier-partners/the-office-shop-inc/)
- [oecm.ca/supplier-partners/poi-business-interiors-lp/](https://oecm.ca/supplier-partners/poi-business-interiors-lp/)
- [oecm.ca/marketplace/furniture-mattresses-and-related-services/](https://oecm.ca/marketplace/furniture-mattresses-and-related-services/)

### GBP / review aggregators

- [yably.ca — The Office Shop](https://yably.ca/reviews/markham/office-shop-inc-366-denison-street)
- [yably.ca — POI Business Interiors](https://yably.ca/reviews/north-york/poi-business-interiors-3389-steeles-ave-e-unit-120)
- [yably.ca — Brant Basics](https://yably.ca/reviews/peterborough/brant-basics-296-george-street-north)
- [reviews.birdeye.com — POI](https://reviews.birdeye.com/poi-business-interiors-167672524579902)
- [yelp.ca — Sensyst](https://www.yelp.ca/biz/sensyst-mississauga)
- [yellowpages.ca — Sensyst](https://www.yellowpages.ca/bus/Ontario/Mississauga/Sensyst-The-Business-Interior-Group/6916370.html)

### BBI internal reference baselines

- [data/reports/sys-verify-1-phase2-2026-05-24.md](data/reports/sys-verify-1-phase2-2026-05-24.md)
- [docs/strategy/icp.md](docs/strategy/icp.md)
- [CLAUDE.md](CLAUDE.md)

---

*Report generated by overnight autonomous competitor recon, 2026-05-24 → 2026-05-25. Findings live in `data/research/` only — NOT promoted to `bbi-build-state.md` or the launch tracker. User to review and selectively promote items to post-launch backlog after LAUNCH-2.*
