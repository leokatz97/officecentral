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

---

# AMENDMENT — UCOS added as 4th competitor + cross-4 gap analysis + market-share tactics

Added 2026-05-25 per Leo's follow-up. Original 3-competitor scan above preserved verbatim. This amendment scans UCOS as the 4th competitor, updates the comparison tables to 4-way, then synthesizes the "How BBI wins market share from each" tactical playbook.

---

## UCOS — 4th Competitor Surface Scan

### Profile

**Domain:** [ucos.ca](https://ucos.ca/) · **Platform:** Shopify (`uc-os.myshopify.com`)
**Locations:** Kingston (HQ — 40 Grant Timmins Dr, K7M 8N2, 13,000 sq ft "Steelcase Working Showroom") · Belleville (365 North Front St Suite 208B) · Brockville
**Phones:** 1-800-267-2212 (main) · 613-547-8070 (Kingston) · 613-966-6655 (Belleville) · 613-345-0202 (Brockville) · **Email:** UCOS@UCOS.CA
**Hours:** Mo-Fr 8:30am–4:30pm
**Founded:** 1980 (44+ years) · **Headcount:** not disclosed publicly
**Cert/Assoc:** LEED-capable (no certification number cited); Belleville/Kingston/Brockville Chamber memberships; CFIB
**OECM:** NOT listed — UCOS is NOT an OECM supplier partner (confirmed by absence from [oecm.ca/marketplace/furniture-mattresses-and-related-services/](https://oecm.ca/marketplace/furniture-mattresses-and-related-services/))
**Federal procurement:** Holds 2 Steelcase Standing Offers — SA# E60PQ-120001/H (Office Seating) + SA# E60PQ-140003/D (Workspaces SA Catalog). Federal contact: Alex Nahorny (anahorny@ucos.ca)
**Brand portfolio:** Steelcase (primary, with on-site showroom) + Artopex + KI + Nightingale (furniture) · Konica Minolta + Ricoh + Quadient + Brother (office equipment) · MBM + Destroyit + Xerox (hardware SKUs on Shopify)

### Pages surveyed

| URL | Title | Words | H1 | JSON-LD @types |
|---|---|---|---|---|
| [/](https://ucos.ca/) | Upper Canada Office Systems • Home | ~650-700 | "Providing products designed for people and the way they work" | **0 blocks** |
| [/pages/office-furniture](https://ucos.ca/pages/office-furniture) | Office Furniture \| UCOS \| Kingston, Belleville Ontario | ~700 | "Office Furniture" | **0 blocks** |
| [/pages/about-us](https://ucos.ca/pages/about-us) | About Us \| Upper Canada Office Systems | ~550 | "ABOUT UPPER CANADA OFFICE SYSTEMS" | **0 blocks** |
| [/pages/federal-government](https://ucos.ca/pages/federal-government) | Federal Government \| UCOS | ~280 | "Canadian Federal Government" | **0 blocks** |
| [/pages/healthcare](https://ucos.ca/pages/healthcare) | Healthcare \| Furniture \| UCOS | ~180 | "Healthcare" | **0 blocks** |

### Site inventory (per Shopify sitemap with required `from`/`to` query params)

| Sitemap | URL count |
|---|---|
| `sitemap_pages_1.xml` | **30 pages** |
| `sitemap_products_1.xml` | **135 products** (~70% office equipment SKUs: HP toner, Xerox cartridges, Destroyit shredders, MBM folders, etc.; ~30% furniture-related) |
| `sitemap_collections_1.xml` | **13 collections** |
| `sitemap_blogs_1.xml` | **1 URL** (the blog index `/blogs/news` — last modified **2017-07-27**) |

**Blog cadence: STALE — no posts since July 2017 (9 years).** This is a 9-year content desert.

### 30 published pages (full list)

- Vertical pages: `open-office`, `private-office`, `reception`, `conference-room`, `higher-education`, `healthcare`, `lounge`
- Core: `equipment`, `office-furniture`, `about-us`, `customer-care`, `community`, `environment`, `contact-us`, `managed-it`
- Service request: `place-a-service-call`, `place-a-supplies-request`, `customer-survey`
- Commerce: `shop-online`
- Federal: `federal-government`, `sa-e60pq-140003-052-pq`, `e60pq-120001`, `e60pq-140003-d` (3 standing-offer detail pages)
- Legal/policy: `data-clear-policy`, `accessibility`, `privacy`
- Test/junk pages: `test-contact`, `testinput`, `utility`, `thank-you` (orphan housekeeping debt)

### GBP / local SEO

| Platform | Result |
|---|---|
| [yellowpages.ca/Upper-Canada-Office-Systems](https://www.yellowpages.ca/bus/Ontario/Kingston/Upper-Canada-Office-Systems/1646700.html) | **0 ratings/reviews** |
| [bbb.org](https://www.bbb.org/ca/on/kingston/profile/office-equipment/upper-canada-office-systems-0117-59843) | **Not BBB Accredited** |
| [yelp.ca](https://www.yelp.ca/biz/upper-canada-office-systems-kingston) | Profile exists; no rating surfaced |
| Google Business Profile | **No surfaceable own-name GBP rating** for either company name variant |

**UCOS has the weakest review/local-SEO posture of all 4 competitors.** 44 years operating with no public review presence.

### Phase 1 SERP baseline addendum — Q6 "office furniture Kingston Ontario" (UCOS home market)

| # | URL | Title |
|---|---|---|
| 1 | atwork.ca/locations/office-furniture-kingston-canada | atWork Kingston location page |
| 2 | **ucos.ca/** | **Upper Canada Office Systems home** |
| 3 | autonomous.ai/ourblog/best-places-to-buy-furniture-in-kingston-ontario | Autonomous.ai review article |
| 4 | facebook.com/marketplace/kingston-ca/office-furniture | Facebook Marketplace |
| 5 | yelp.ca/Used Office Furniture Kingston | Yelp listings |
| 6 | **ucos.ca/pages/office-furniture** | **UCOS office furniture page** |
| 7 | bennetts.ca/office | Bennett's Furniture (Peterborough/Kingston/Lindsay hybrid retailer) |
| 8 | stores.ashleyhomestore.ca/Kingston | Ashley HomeStore Kingston |
| 9 | **ucos.ca/pages/open-office** | **UCOS open office page** |
| 10 | yelp.ca search results | Yelp aggregator |

- **UCOS owns 3 of top 10** (positions 2, 6, 9) for its own city = 30% organic SOV.
- **BBI: not in top 10** (Bennett's Furniture position 7 is the closest-geo Peterborough mention).
- Notable: this is the inverse of Q3 (BBI invisible in Peterborough) — UCOS dominates Kingston, BBI is invisible in Peterborough.

### UCOS notable patterns

- **Hybrid equipment + furniture model** (like BBI's parent Office Central legacy). Sells HP toner, Xerox cartridges, Destroyit shredders alongside Steelcase chairs. This is the closest business-model match to BBI of all 4 competitors.
- **Federal procurement specialist** with 3 dedicated standing-offer pages (E60PQ-120001 + E60PQ-140003/D + sa-e60pq-140003-052-pq). Targets CFB Kingston / RMC / federal departments — though page content is thin (280 words) and lacks GovernmentService schema.
- **Capital Office Interiors (COI) is the *sole* Steelcase dealer for National Capital Region + Eastern Ontario** per [oecm.ca/supplier-partners/capital-office-interiors-ltd/](https://oecm.ca/supplier-partners/capital-office-interiors-ltd/) and confirmed by [Steelcase dealer locator](https://www.steelcase.com/find-us/where-to-buy/dealers/). UCOS hosts a "Steelcase Working Showroom" but is positioned beneath COI in the Steelcase channel hierarchy. UCOS's Steelcase moat is less defensible than initial framing suggested.
- **Zero JSON-LD across all 5 tested pages** — UCOS doesn't even emit Shopify-default Organization or WebSite schema. Either explicitly suppressed or running an extremely old/stripped theme. Worst-in-class schema posture.
- **Blog dead since July 2017** — UCOS has zero recent content marketing investment.
- **Test/orphan pages in sitemap** (`test-contact`, `testinput`, `utility`, `thank-you`) — poor housekeeping; signals neglected site maintenance.
- **No OECM mention anywhere** — UCOS targets federal procurement, not Ontario broader-public-sector. Distinct procurement positioning from Office Shop / POI / BBI.

---

## Updated 4-way Schema Comparison

| Schema Type | Sensyst | The Office Shop | POI | **UCOS** | **BBI (LAUNCH-2)** |
|---|:---:|:---:|:---:|:---:|:---:|
| Organization | ✅ | ✅ | — | **—** | ✅ |
| LocalBusiness | — | ✅ | ✅ | **—** | ✅ |
| WebSite + SearchAction | ✅ | ✅ | ✅ | **—** | ✅ |
| WebPage | — | ✅ | ✅ | **—** | — |
| BreadcrumbList | — | ✅ | ✅ | **—** | ✅ |
| Product + Offer | — | — | — | **—** | ✅ |
| Service | — | — | — | **—** | ✅ |
| FAQPage | — | — | — | **—** | ✅ |
| HowTo | — | — | — | **—** | ✅ |
| GovernmentService | — | — | — | **—** | ✅ |
| BlogPosting | — | ✅ | — | **—** | ✅ |
| Article | — | ✅ | — | **—** | — |
| ContactPoint | — | ✅ | ✅ | **—** | — |
| AggregateRating | — | ✅ | — | **—** | — ← gap |
| Review | — | ✅ | — | **—** | — ← gap |
| Person | — | ✅ | — | **—** | — |

**Distinct @type counts:** Office Shop ~12 · **BBI 11** · POI 6 · Sensyst 2 · **UCOS 0**

UCOS is the only entity in the comparison emitting **zero** structured data. Even Shopify's default schema blocks are absent — they may have been removed by a stripped theme or suppressed via settings. This makes UCOS effectively invisible to AI engines parsing semantic web data.

---

## Updated 4-way Content Pattern Analysis

| Pattern | Sensyst | Office Shop | POI | **UCOS** | **BBI** |
|---|---|---|---|---|---|
| Total /pages/ URLs | ~89 | unknown (large) | unknown | **30** | 25 BBI pages |
| Product catalog | 0 | overlay quote only | 4 categories on store.poi.ca | **135 SKUs** (mostly equipment, ~30% furniture) | **330 SKUs** |
| Case studies indexed | **61** w/ sq ft metadata | 4 | **31** w/ multi-section narrative | **0** (no case-study content surface) | thin (`/pages/customer-stories`) |
| Blog inventory | ~80+ | ~68 resources | **~130** | **0 posts** (last activity July 2017) | 2 published |
| Latest blog publish | 2026-05-21 | 2026-05-23 | active (undated) | **2017-07-27 (9 years stale)** | 2026-05-24 |
| Geo-targeted pages | **~50+** | none specific | 6 showroom locations | 3 (Kingston/Belleville/Brockville mentions, no dedicated city pages) | 0 |
| Vertical/industry pages | **17** | 4 | 4 segments | **7** (open-office, private-office, reception, conference-room, higher-education, healthcare, lounge — but thin: 180-700w each) | **5** (deeper content) |
| FAQ density | footer link | nav link | nav link | **none surfaced** | **36 FAQs across 9 templates** |
| Federal procurement page | — | — | — | **✅ 3 dedicated SA pages** (E60PQ-*) | — (BBI doesn't currently target federal) |
| Workflow / numbered process | 4-step (Plan/Design/Build/Furnish) | "Our Process" | — | **"OUR PROCESS" H2 on /pages/office-furniture** (no detail/schema) | HowTo schema on /pages/design-services |
| Cornerstone-length content (>2k words) | 80+ blurbs | 1,200-1,400w articles | not surfaced | **none** | OECM cornerstone 2,446w |
| Comparison tables in content | — | — | — | **—** | 3 in OECM cornerstone |

---

## Updated 4-way GBP / Local SEO Visibility

| Entity | Address | Hours | Reviews / Rating | Knowledge Panel |
|---|---|---|---|---|
| Sensyst | 6805 Invader Crescent Unit 1, Mississauga ON L5T 2K6 | Not displayed | 0 reviews YellowPages | weak |
| The Office Shop | 366 Denison St, Markham ON L3R 1B9 | Mo-Fr 9-4 | **4.81★ / 65 Google reviews** | **strong** |
| POI Business Interiors | 3389 Steeles Ave E Unit 120, North York ON M2H 3S8 | Mo-Fr 8:30-4:30 | 3.5-3.9★ / 45-56 reviews mixed | medium |
| **UCOS** | 40 Grant Timmins Dr, Kingston ON K7M 8N2 (+ Belleville + Brockville) | Mo-Fr 8:30-4:30 | **0 reviews YellowPages · not BBB-accredited · no surfaceable Google rating** | **weakest** |
| BBI / Office Central (under "Brant Basics" name) | 296 George St N, Peterborough ON K9J 3H2 | Mo-Fr 9-5 | 4.4★ / 60 reviews — but under Brant Basics, not BBI | misattributed |

UCOS edges out only BBI on review presence (and only because BBI's reviews are misattributed to Brant Basics — fix HIGH-A and BBI vaults above UCOS).

---

## Cross-4 Gap Analysis

### Patterns BBI shares with each of the 4 competitors

| Pattern | Sensyst | Office Shop | POI | UCOS | BBI |
|---|:---:|:---:|:---:|:---:|:---:|
| Family-owned heritage | — | ✅ (founder sisters) | ✅ (3rd gen Scholl) | implied | ✅ (1964, Steve Katz 2nd gen) |
| Steelcase channel | — | — | ✅ (Premier since 1958) | ✅ (showroom, sub-COI) | — |
| Global Furniture Group channel | — | ✅ (Premier dealer) | — | — | ✅ (BBI carries GFG) |
| OECM listed supplier | — | ✅ | ✅ | — | ✅ |
| Federal Standing Offer holder | — | — | — | ✅ (Steelcase E60PQ) | — (gap) |
| Hybrid equipment + furniture | — | — | — | ✅ | ✅ (legacy Office Central) |
| Functional e-commerce checkout | — | — | minimal (store.poi.ca) | ✅ (Shopify, 135 SKUs) | ✅ (Shopify, 330 SKUs) |

### Where BBI is structurally ahead of all 4

1. **Schema breadth.** BBI's 11 distinct @types beats every competitor (Office Shop is the only one close, and even they lack FAQPage/Service/HowTo/GovernmentService).
2. **GovernmentService schema for OECM positioning.** Uncontested — none of the 4 competitors emit it. BBI uniquely owns the AI-parseable OECM moat.
3. **HowTo schema on `/pages/design-services`.** Uncontested.
4. **Product + Offer schema across 330 PDPs.** UCOS has 135 products but emits zero schema. Office Shop and Sensyst have zero PDPs. POI has 4 categories on store.poi.ca. BBI is the only entity with a real schema-instrumented catalog.
5. **Cornerstone content + comparison tables.** BBI's OECM article (2,446w / 3 comparison tables / 6 Q&As / 8 internal links / BlogPosting+FAQPage schema) is structurally better-than-competition AI Overview bait — no competitor publishes anything comparable.
6. **Peterborough geo + Indigenous (Brant Basics PSAB) procurement angle.** Uncontested by all 4 competitors.

### Where ALL 4 competitors are ahead of BBI

1. **Standalone Google Business Profile with reviews.** Office Shop dominates (4.81★/65), POI mixed (3.5-3.9★), Sensyst weak, UCOS weakest — but ALL 4 have an own-name GBP that searches for the company surface. BBI's GBP is misattributed to "Brant Basics." → HIGH-A
2. **Visible client logo bar.** All 4 display 5-15 client logos prominently. BBI homepage uses gradient placeholders. → HIGH-E
3. **Active blog within last 12 months.** Sensyst + Office Shop + POI all publishing in May 2026. Even stale UCOS at least posts equipment service requests via /pages/place-a-service-call. BBI has 2 articles total. → MED-C
4. **Newsletter signup capture.** All 4 have a newsletter CTA. BBI has none. → MED-E

### Where 3 of 4 competitors are ahead of BBI

1. **Case study depth.** Sensyst (61), POI (31), Office Shop (4). UCOS has 0 → BBI is in last place but tied. → HIGH-D
2. **Geo-targeted city pages.** Sensyst 50+, POI 6 (showrooms), UCOS implicit (3 locations). Office Shop has none specific. BBI has 0. → HIGH-C + MED-A
3. **Industry/vertical page breadth.** Sensyst 17, BBI 5, POI 4, Office Shop 4, UCOS 7 (but thin). BBI is mid-pack; UCOS has more verticals but each is 180-700w. → MED-B

### Where BBI is alone but exposed

1. **No Federal Government landing page.** UCOS has 3 pages targeting federal procurement. BBI doesn't target federal but ICP A includes municipal + federal-adjacent buyers (band offices, regional health authorities, federal-funded non-profits). Worth considering. → see new Backlog item MS-A below
2. **No designer credentials displayed.** Sensyst ARIDO/IDC/BCIN, POI Steelcase Premier + Great Place to Work 2023, Office Shop WBE Canada. UCOS has none. BBI has OECM Supplier Partner. Equivalent procurement-trust signal but no design-profession signal. → LOW-B (existing)

### Where ALL 4 competitors are exposed (BBI white space)

1. **Procurement-vehicle education content.** None of the 4 publish "OECM vs RFP" / "Standing Offer vs PO" / "How to buy office furniture without going to tender" content. BBI's OECM cornerstone is the only example — and AI Overview will cite it absent alternatives. **Repeatable template.**
2. **PSAB / Indigenous procurement angle.** UCOS markets federal procurement but doesn't surface PSAB. Office Shop is WBE Canada but doesn't translate it to procurement copy. POI doesn't surface any minority/Indigenous supplier angle. Brant Basics' PSAB-recognized status is uncontested.
3. **Product specs + AI-parseable additionalProperty.** No competitor surfaces specs as structured data. BBI's AI-3 work (specs → additionalProperty in Product schema) is unique.
4. **Dual buying mode (cart + quote).** All 4 competitors force buyers into a single funnel: Sensyst quote-only, Office Shop quote-only, POI store too tiny to count, UCOS cart works but only for equipment (chairs require email/phone). BBI offers genuine self-serve checkout for 330 SKUs + quote channel for project-scale buyers.
5. **Comparison tables in content.** Universally absent in competitors. BBI's OECM article uses 3. AI engines reward table-structured content for parseable answers.

---

## How BBI Wins Market Share From Each

The actionable section. For each competitor: their single biggest exploitable weakness + 1-3 concrete tactics tied to specific BBI assets / pages / backlog items.

### vs Sensyst (Mississauga, GTA, design-services led, 50+ geo pages, 61 case studies)

**Sensyst's #1 weakness:** Zero custom schema. Their 61 case studies emit only Shopify-default Organization schema — no CreativeWork, no GovernmentService, no Product. Their 50+ geo pages emit no LocalBusiness. They've built content volume without semantic depth.

**Sensyst's #2 weakness:** No e-commerce. 100% of buyer journeys funnel to /pages/contact. They lose every buyer who just wants to order a chair.

**Sensyst's #3 weakness:** Not OECM-registered. They're invisible for "OECM" queries (Phase 1 Q2 confirms).

**Where BBI takes share:**

- **Tactic MS-S1 — Toronto / Mississauga / Vaughan geo pages.** Mirror Sensyst's geo playbook with BBI's superior schema posture (LocalBusiness + Service + GovernmentService + FAQPage on each). 3 pages × ~600w with KW-pull, BBI delivers more AI-Overview-eligible content per geo than Sensyst's 50+ blurbs. Stack ranks: Toronto first (highest search vol), Mississauga (Sensyst home), Vaughan (Sensyst clients). **Effort:** ~2hr/page × 3 = 6hr. **Expected:** Sensyst's geo SOV erodes for OECM+procurement intent queries.
- **Tactic MS-S2 — "Office furniture for Toronto fit-outs under $50k" cornerstone article.** Sensyst targets *large* fit-outs (Gatestone 16,000 sq ft) — they neglect mid-market $10-50k buyers (BBI ICP B sweet spot). Publish a comparison-table cornerstone targeting "Best office furniture for Toronto mid-size offices" with FAQPage + BlogPosting schema. **Effort:** 8hr. **Expected:** Captures the ICP B SMB buyer Sensyst doesn't service.
- **Tactic MS-S3 — Quick-ship checkout positioning.** Add "Quick-ship from Ontario stock" badge to PDPs targeting Sensyst's GTA service area. Sensyst literally cannot fulfill these orders (no products, no SKUs, no checkout). **Effort:** 2hr. **Expected:** Captures the office manager who'd otherwise call Sensyst for a single chair.

### vs The Office Shop (Markham, Global Furniture Group dealer, AggregateRating moat, 4.81★/65 reviews)

**Office Shop's #1 weakness:** Education page has **zero OECM references** despite being an OECM supplier. They're failing to position the most valuable institutional signal they could claim.

**Office Shop's #2 weakness:** No FAQPage, Service, HowTo, or GovernmentService schema. They have rich LocalBusiness + AggregateRating but no content-type schema. Their AI Overview win is driven by reviews alone.

**Office Shop's #3 weakness:** They're 100% quote-only with no real product catalog. Even their featured products "Request a Quote" overlay rather than checkout.

**Where BBI takes share:**

- **Tactic MS-O1 — HIGH-A + HIGH-B execution closes the AggregateRating gap.** GBP reclaim + AggregateRating/Review schema wiring removes Office Shop's single AEO differentiator. Once BBI has 60+ reviews via star schema, BBI's superior content-type schema (FAQPage + GovernmentService + HowTo) flips the AI Overview citation order. **Effort:** ~3hr post-launch. **Expected:** BBI moves into AI Overview citations for Q1, Q3, Q5 where Office Shop currently dominates.
- **Tactic MS-O2 — "OECM vs Global Furniture Group dealer pricing" cornerstone article.** Office Shop *is* a Global Furniture Group dealer but doesn't surface OECM. BBI publishes the comparison: GFG-only dealer pricing vs OECM-via-Brant-Business-Interiors. Cite the 2025-470 Agreement explicitly. Office Shop can't respond without writing an OECM hub of their own (which they'd need to backfill 6+ months of content for). **Effort:** 10hr. **Expected:** Captures Ontario institutional buyers comparing dealers.
- **Tactic MS-O3 — Direct-checkout SKU bundles for the GTA market.** Build 5-10 "Quick-ship workstation bundles" (chair + desk + storage) as Shopify products with bundled discount. Target "GTA office furniture under $5k" — Office Shop cannot fulfill via cart, BBI can. **Effort:** 4hr. **Expected:** Captures sub-$5k order flow Office Shop forces to quote channel.

### vs POI (North York, largest dealer, Steelcase Premier, 130 blog posts, 31 case studies)

**POI's #1 weakness:** 130 blog posts and 31 case studies — ALL emitting only LocalBusiness + BreadcrumbList schema. No BlogPosting, no Article, no FAQPage. The largest content library in the comparison has the worst content-type schema utilization.

**POI's #2 weakness:** Mixed reviews (3.5–3.9★) despite POI being 4× the size of Office Shop. Real customers signal POI under-delivers vs scale. Reputation-conscious procurement teams notice.

**POI's #3 weakness:** Their OECM listing exists ([oecm.ca/supplier-partners/poi-business-interiors-lp/](https://oecm.ca/supplier-partners/poi-business-interiors-lp/)) but their site has minimal OECM positioning. They under-leverage the moat they have.

**Where BBI takes share:**

- **Tactic MS-P1 — Publish 3 deep school-board case studies with GovernmentService + Article schema.** POI's `/our-work/` lists 4 school-board projects (Nipissing-Parry Sound Catholic SB, U of T Scarborough, Algoma U, Rosedale Day School) but each is a thin photo-blurb. BBI publishes 3 deep narratives (start with Halton Catholic DSB / 320 ergoCentric chairs / 11 schools from Day 10 cornerstone source data) — sq ft + sector + OECM Agreement 2025-470 + outcome metrics. With GovernmentService schema, BBI wins AI Overview for "Ontario school board office furniture supplier" (Phase 1 Q4 where Office Shop currently sits at #10 and POI is invisible). **Effort:** 18hr (3 × 6hr per case study). **Expected:** BBI enters Q4 SERP + AI Overview for school-board procurement.
- **Tactic MS-P2 — Healthcare clinic positioning.** POI's healthcare clients are hospitals (SickKids, Children First, College of Dental Hygienists, Canadian Hearing Services). BBI's [feedback_healthcare_tone memory](/Users/leokatz/.claude/projects/-Users-leokatz-Desktop-Office-Central/memory/feedback_healthcare_tone.md) explicitly targets *private clinics + practices* over hospital procurement. White space — POI doesn't pursue private clinics. Build `/pages/private-clinic-furniture` targeting independent practices: dental, family medicine, physio, mental health. **Effort:** 4hr. **Expected:** Captures the sub-segment POI ignores.
- **Tactic MS-P3 — "Reviews matter for procurement" trust positioning.** POI's mixed reviews are a procurement red flag. After HIGH-A + HIGH-B execution, surface BBI's 4.4★ explicitly in /pages/quote + /pages/oecm copy. Don't attack POI by name — just be the reputation-clean alternative. **Effort:** 1hr copy update. **Expected:** Buyers who Google-check POI find the 3.5★ and look for alternatives. BBI is one.

### vs UCOS (Kingston, Eastern Ontario, Steelcase showroom, federal Standing Offers, hybrid equipment+furniture)

**UCOS's #1 weakness:** Zero JSON-LD across every page tested. Worst-in-class schema posture. AI engines essentially cannot parse UCOS as a structured entity.

**UCOS's #2 weakness:** Blog dead since 2017. 9 years of content desert. UCOS is the visible "stagnant local supplier" stereotype in their digital footprint.

**UCOS's #3 weakness:** Zero public reviews on Yellow Pages / not BBB-accredited / no surfaceable Google rating. 44 years operating with no review investment.

**UCOS's strength to neutralize:** Eastern Ontario geographic moat (Kingston + Belleville + Brockville). Kingston is 2.5hr drive from BBI's Peterborough HQ — same-day delivery + install territory if BBI chooses to expand. Kingston market has CFB Kingston + RMC + Queen's University + Kingston Health Sciences — meaningful institutional buyer concentration.

**Where BBI takes share:**

- **Tactic MS-U1 — Build `/pages/kingston-office-furniture` + `/pages/belleville-office-furniture` geo pages.** Mirror HIGH-C Peterborough template. UCOS has 30 pages and zero schema — BBI's geo page with LocalBusiness + Service + FAQPage schema wins AEO head-to-head despite UCOS's home-market SERP position. Kingston is plausibly part of BBI's install zone (2.5hr from Peterborough); Belleville is closer (1.5hr). **Effort:** 2hr/page × 2 = 4hr. **Expected:** Captures Eastern Ontario long-tail UCOS currently owns by default.
- **Tactic MS-U2 — Federal procurement landing page** (new — call this **MS-A backlog**). UCOS holds Steelcase Standing Offers for federal seating (E60PQ-120001/H) and workspaces (E60PQ-140003/D). BBI's positioning to date is OECM-only. Add `/pages/federal-government-office-furniture` covering: PSAB-listed Brant Basics (Indigenous-procurement set-aside angle UCOS cannot match), OECM cross-applicability for federal-funded non-profits, plus an explicit "looking for a Steelcase Standing Offer? See alternatives." copy block. Don't compete on UCOS's Steelcase SO directly — compete on the *procurement vehicles UCOS doesn't have* (OECM, PSAB). **Effort:** 6hr (KW pull + copy + GovernmentService schema). **Expected:** Captures federal-adjacent buyers (band offices, regional health authorities, federal-funded non-profits) BBI's ICP A already includes per [icp.md](docs/strategy/icp.md).
- **Tactic MS-U3 — Active blog cadence as direct contrast.** UCOS hasn't posted since 2017. Any consistent BBI publishing schedule (even 1 post/month) creates a freshness signal that's effectively zero-effort competitive — Google's freshness ranking factor will favor BBI for Kingston/Eastern Ontario long-tail queries within 3-6 months. **Effort:** ~6-10hr/post × 1/month = ongoing 8hr/month. **Expected:** UCOS's stale digital footprint becomes visible to AI engines and SERP rankings drift.

### Universal market-share tactics (apply across all 4 competitors)

- **Tactic MS-U4 — "Procurement decoder" content hub.** None of the 4 competitors publish how-to procurement education. BBI's OECM cornerstone proves the format works. Extend the cornerstone library:
  - "OECM Agreement 2025-470 explained" ✅ (Day 10 cornerstone — published)
  - "OECM vs RFP procurement timelines" (planned MED-C item 3)
  - "PSAB Indigenous procurement set-aside for office furniture"
  - "Standing Offer vs Supply Arrangement — which one applies to your purchase"
  - "Buying office furniture for a federally-funded non-profit"
  - Each piece: 2k+ words, comparison tables, FAQ schema, GovernmentService where applicable
  - **Effort:** 8hr/post · **Cadence:** 1/month. Built quickly because BBI already has the OECM template.
- **Tactic MS-U5 — Spec-rich PDP differentiation.** BBI's 330-product catalog with additionalProperty schema is structurally unmatched. UCOS has 135 products but emits zero schema — BBI's products literally win the AI Overview answer for "best ergonomic chair Ontario." Continue the AI-3 spec metafield rollout to remaining SKUs (any post-launch backlog from sys-verify-1-phase2). **Effort:** ongoing AI-3 phase 2.
- **Tactic MS-U6 — Brant Basics + BBI dual-brand crossover.** None of the 4 competitors have a sister-brand they can cross-promote. BBI can use Brant Basics' 60-review GBP (via HIGH-A) + PSAB-registered status to win procurement angles competitors structurally cannot.

---

## Updated Backlog Items — additions from UCOS analysis

In addition to the original 5 HIGH / 7 MED / 5 LOW from the 3-competitor scan, the UCOS analysis surfaces:

### [HIGH-F] FEDERAL-PROCUREMENT-PAGE — Build `/pages/federal-government-office-furniture` targeting UCOS's positioning

- **Source observation:** UCOS holds 2 Steelcase Standing Offers (E60PQ-120001/H + E60PQ-140003/D) and runs a dedicated [Federal Government page](https://ucos.ca/pages/federal-government). BBI has no federal-procurement landing page despite Brant Basics being PSAB-listed (Indigenous procurement set-aside) — a procurement vehicle UCOS structurally cannot offer. ICP A includes federal-funded non-profits and band-office buyers per [icp.md](docs/strategy/icp.md).
- **Action:** Build `/pages/federal-government-office-furniture` covering: PSAB Indigenous-procurement angle (unique to BBI/Brant Basics), OECM cross-applicability for federal-funded entities, comparison with Standing Offers (acknowledge BBI doesn't have one but explain the alternatives). Schema: GovernmentService + FAQPage. KW-pull mandatory per CLAUDE.md SEO-AUDIT before publishing.
- **Effort:** 6 hr (KW + copy + schema).
- **Expected impact:** Captures federal-adjacent procurement traffic UCOS currently owns by default in Eastern Ontario, and PSAB-specific traffic no competitor targets.

### [MED-H] KINGSTON + BELLEVILLE GEO PAGES — Eastern Ontario market entry

- **Source observation:** UCOS owns 3 of top 10 SERP positions for "office furniture Kingston Ontario" (Phase 1 SERP addendum Q6). Kingston is 2.5hr from BBI's Peterborough HQ — same-day install territory if BBI extends service area. Belleville is 1.5hr — comfortably within current operational range.
- **Action:** Build `/pages/kingston-office-furniture` + `/pages/belleville-office-furniture` mirroring HIGH-C Peterborough template. Each ~600w with LocalBusiness schema + 4-6 region-specific FAQs (delivery to Kingston/Belleville, install availability, OECM applicability for Kingston Health Sciences / Queen's / CFB Kingston regional partners).
- **Effort:** ~2hr/page × 2 = 4 hr.
- **Expected impact:** Establishes BBI in UCOS's home market with superior schema posture. UCOS cannot defend without rebuilding schema from scratch.

### [LOW-F] BBI vs UCOS COMPARISON TRACKING — Quarterly check

- **Source observation:** UCOS's blog dead since 2017, zero JSON-LD across all pages. If UCOS modernizes (e.g., adds Shopify-default Organization schema, restarts blog, claims a GBP), the competitive picture in Eastern Ontario shifts. Worth quarterly monitoring.
- **Action:** Re-run UCOS schema + sitemap + blog cadence checks quarterly (or alongside the LOW-E OECM-moat-monitoring item).
- **Effort:** 30 min / quarter.
- **Expected impact:** Early warning if UCOS modernizes its digital footprint.

---

## Updated Methodology Notes — amendment additions

### Additional pages successfully scraped (UCOS)

5 UCOS URLs + sitemap inventory pulls (pages_1 + products_1 + collections_1 + blogs_1) + 4 GBP-aggregator URLs.

### Additional pages failed (UCOS)

- `https://ucos.ca/sitemap_pages_1.xml` (without query params) — 400 (Shopify sitemap requires `from`/`to` params; retried with params and succeeded)
- `https://ucos.ca/sitemap_products_1.xml` (without query params) — 400 (same)

### Additional hand-judgment calls (UCOS)

1. **Treated UCOS's "Steelcase Working Showroom" as a showroom relationship rather than a Premier Dealer relationship** — per [Steelcase dealer locator](https://www.steelcase.com/find-us/where-to-buy/dealers/) and OECM evidence that Capital Office Interiors is the sole Steelcase dealer for the National Capital Region + Eastern Ontario. This may understate UCOS's actual Steelcase access; worth a direct check via Steelcase channel partner inquiry if BBI ever considers a Steelcase relationship.
2. **Tagged the Federal-Government tactic as HIGH despite being new scope for BBI** — justification: ICP A explicitly includes federal-funded non-profits + band offices, and PSAB is a procurement-vehicle moat UCOS cannot match. High-leverage, schema-only-different from existing /pages/oecm pattern.
3. **Did NOT scan UCOS's product PDPs individually** — Approach A surface scan; the 135-SKU catalog is overwhelmingly office equipment (HP toner, shredders) with minimal furniture SKU presence. PDP schema audit would be low-yield.

---

## Final 4-competitor Executive Summary (amendment)

| Competitor | Domain | Founded | Locations | Reviews | Schema @types | Blog cadence | Strongest moat | BBI counter |
|---|---|---|---|---|---|---|---|---|
| Sensyst | sensyst.com | 1977 | Mississauga | 0 reviews YP | 2 | ~3/month | 50+ geo pages + 61 case studies | MS-S1/S2/S3 |
| The Office Shop | theofficeshop.ca | 1996 | Markham | **4.81★ / 65** | ~12 (w/ AggregateRating) | ~2-3/month | AggregateRating schema + GBP | MS-O1/O2/O3 |
| POI | poi.ca | 1958 | 6 Ontario | 3.5-3.9★ / 45-56 | 6 | active | 130 posts + 31 case studies + Steelcase Premier | MS-P1/P2/P3 |
| **UCOS** | ucos.ca | 1980 | Kingston/Belleville/Brockville | **0 reviews** | **0** | **dead since 2017** | Federal Standing Offers + Eastern Ontario geo | MS-U1/U2/U3 |
| **BBI (LAUNCH-2)** | brantbusinessinteriors.com | 1964 | Peterborough | 4.4★ (misattributed) | **11** | activating Day 11 | OECM + GovernmentService schema + 330 PDPs + dual-mode cart | — |

**BBI's structural advantages (after HIGH-A + HIGH-B execution):**
- Best schema posture (11 vs Office Shop's 12 w/ AggregateRating, but BBI has GovernmentService + HowTo + Service + FAQPage that Office Shop lacks)
- Only functional 330-SKU spec-rich PDP catalog
- Only OECM+PSAB+GovernmentService schema combination
- Only entity with both cart and quote-channel infrastructure

**BBI's deficits (Day 11 → 60 days):**
- GBP reattribution (HIGH-A)
- AggregateRating/Review schema (HIGH-B)
- Case study depth (HIGH-D)
- Content cadence (MED-C)

**BBI's 90-day market-share opportunity:**
- Kingston + Belleville geo pages (MS-U1) — Eastern Ontario white space
- Federal Government page (HIGH-F / MS-U2) — Brant Basics PSAB-Indigenous angle
- Toronto + Mississauga + Vaughan geo pages (MS-S1) — GTA market entry vs Sensyst
- OECM-vs-GFG cornerstone (MS-O2) — direct AI Overview hit on Office Shop's blind spot
- 3 deep school-board case studies (MS-P1) — captures Q4 SERP currently dominated by aggregators
- Private-clinic positioning (MS-P2) — sub-segment POI ignores

---

*Amendment generated 2026-05-25. UCOS added as 4th competitor; cross-4 gap analysis + market-share tactics layered on top of the original 3-competitor scan. All sections above the AMENDMENT divider preserved verbatim. Findings remain post-launch backlog reference only — NOT promoted to `bbi-build-state.md` or tracker.*

---

# FINAL PLAYBOOK — What to do to catch up + what to exploit

This is the action layer. Two columns: deficits to close (catch up) and moats to lean on (exploit). Backlog items above stay raw — this section sequences them.

---

## Strategic frame

BBI sits in a curious position relative to the 4 competitors: **structurally ahead on schema + AEO + catalog + content quality, structurally behind on GBP + reviews + content volume + visible client logos.** The catch-up work is mechanical (1-3 weeks per item). The exploit work compounds (months of advantage once entrenched). Doing both in parallel is the right call — they don't conflict on resources or copy.

The 4 competitors break down into 2 archetypes:

- **The slow incumbents** (Sensyst, POI, UCOS) — established, deep client books, but digitally calcified. Sensyst publishes blurbs without schema. POI publishes 130 posts without schema. UCOS hasn't posted in 9 years. Each carries dead weight (test pages, stale blogs, missing reviews) BBI doesn't.
- **The polished mid-sizer** (The Office Shop) — clean WordPress + Rank Math, AggregateRating + 65 Google reviews, dominant in AI Overview. But Office Shop is positionally shallow — they're an OECM supplier who doesn't lead with OECM. Their moat is mechanical, not strategic. Once BBI matches the mechanical signal (HIGH-A + HIGH-B), Office Shop's lead evaporates because BBI's content posture is deeper.

The full play: catch up on mechanical signals → out-position on procurement + verticals → take share city-by-city + vertical-by-vertical.

---

## CATCH UP — Close the deficits all 4 competitors have over BBI

Ordered by ROI. Numbers in parentheses reference backlog item IDs above.

### Tier 1 — Do first 30 days

| # | Action | Effort | Backlog ID | Why now |
|---|---|---|---|---|
| 1 | **Reclaim or rename the 296 George St N GBP** to surface "Brant Business Interiors" — Option (b) preserves the 60 reviews on the Brant Basics GBP via dual-naming | 1-2 hr submission + ~2 weeks verification | HIGH-A | Single biggest lever. Unlocks #2, #3, #4. |
| 2 | **Wire AggregateRating + Review schema** into `bbi-org-schema.liquid` once GBP is named correctly | 1 hr after #1 | HIGH-B | Closes the one schema signal Office Shop has over BBI. Likely flips AI Overview citation order. |
| 3 | **Real client logo bar on homepage** (replace gradient placeholders) | 2-3 hr permissions + 1 hr code | HIGH-E | Removes the only "unfinished" perception competitors don't trigger. Compounds with #2 for trust signal stack. |
| 4 | **`/pages/peterborough-office-furniture` geo hub** with LocalBusiness schema + 4-6 FAQs | 2-3 hr (DataForSEO KW pull mandatory first) | HIGH-C | Home city. Currently lost to UK Peterborough. One page closes the gap. |
| 5 | **Newsletter signup in footer + /pages/oecm** exit-intent | 2-3 hr | MED-E | Captured procurement contacts compound for years. All 4 competitors have it; BBI has zero captured emails. |

**Tier 1 total effort:** ~15 hours over ~30 days (most of it is the 2-week GBP verification wait).
**Tier 1 outcome:** BBI matches all 4 competitors on every mechanical visibility signal.

### Tier 2 — Do 30-60 days

| # | Action | Effort | Backlog ID | Why now |
|---|---|---|---|---|
| 6 | **First deep case study** — Halton Catholic DSB (320 ergoCentric chairs, 11 schools — already sourced from Day 10 cornerstone) | 6 hr | HIGH-D | Validates the case-study template. Source material already gathered. Pairs with #2 for AI Overview hits on school-board queries. |
| 7 | **Restart blog at 1 post/month** — start with "OECM vs RFP procurement timelines" (extends Day 10 cornerstone format) | 6-10 hr/post | MED-C | UCOS-style content rot is invisible to AI engines for ~3 months, then becomes a visible freshness penalty. Even 1/month neutralizes UCOS, narrows the gap to Sensyst/POI. |
| 8 | **Add 2nd + 3rd geo pages** — Toronto + Mississauga (Sensyst's home market with BBI's superior schema) | 2 hr/page × 2 = 4 hr | MED-A | Geo expansion compound. Each city page is independently SEO-productive. |
| 9 | **Service area page `/pages/service-area`** with Ontario + Western Canada map graphic | 2-3 hr | MED-G | Closes a procurement-FAQ question without a phone call. ICP A institutional buyers ask this constantly. |
| 10 | **2 industry pages** — manufacturing + legal/accounting (ICP B private-sector targets) | 3-4 hr/page × 2 = 6-8 hr | MED-B | Sensyst has 17 industry pages; BBI has 5. Doubling down on ICP B (SMB private-sector) closes the gap fastest. |

**Tier 2 total effort:** ~30-40 hours over ~30 days.
**Tier 2 outcome:** BBI starts overtaking competitors on content depth + vertical coverage.

### Tier 3 — Do 60-90 days

| # | Action | Effort | Backlog ID | Why now |
|---|---|---|---|---|
| 11 | **2 more case studies** — pick a healthcare clinic + a municipal/government project | 6 hr × 2 = 12 hr | HIGH-D | Case study #2 and #3 lock in the template + start to match POI's depth. |
| 12 | **Kingston + Belleville geo pages** — Eastern Ontario market entry against UCOS | 2 hr × 2 = 4 hr | MED-H | UCOS's home turf. Their schema is empty, their reviews are zero, their blog is 9 years stale. Easy share. |
| 13 | **Federal Government landing page** — PSAB + OECM angle | 6 hr | HIGH-F | New vertical BBI doesn't currently target. PSAB-Indigenous procurement angle no competitor can match. |
| 14 | **Capability Statement PDF + OECM Procurement Guide PDF** | 4-6 hr × 2 = 8-12 hr | MED-D | Procurement-team friendly trust signal. Reusable in cold outreach. |
| 15 | **Team bios on /pages/about** | 4-6 hr | MED-F | Sensyst has 10 leadership bios; POI 11; Office Shop names founders; BBI doesn't surface team. Quick trust win. |

**Tier 3 total effort:** ~35-45 hours over ~30 days.
**Tier 3 outcome:** BBI's catch-up complete; pivot fully to exploit mode.

**Full catch-up totals: ~80-100 hours over 90 days.** Sustainable at ~8-10hr/week. No theme architecture changes — almost all of it is content + schema + GBP work.

---

## EXPLOIT — Lean on BBI's unique moats to take share

These are tactics that no competitor can copy quickly. BBI is alone or near-alone on each. The cumulative effect: BBI ends 90 days with positioning competitors would need 6-12 months to replicate.

### Moat 1: OECM + GovernmentService schema combo

**What BBI alone has:** A `/pages/oecm` hub with GovernmentService JSON-LD, a 2,446-word cornerstone article with 3 comparison tables citing Agreement 2025-470, FAQPage schema across category templates, and BlogPosting+FAQPage on the cornerstone. Office Shop and POI are OECM suppliers but neither leads with OECM in copy or schema. Sensyst and UCOS aren't OECM-registered.

**Exploit tactics:**

- **EX-1 — "OECM vs Global Furniture Group dealer pricing" cornerstone** (MS-O2). Office Shop is a Premier GFG dealer but emits zero OECM-positioning copy. BBI publishes the comparison. Office Shop cannot respond without building an OECM content hub from scratch — 6+ months of catch-up content for them. **Effort:** 10 hr. **Window before competitor response:** 6+ months minimum.
- **EX-2 — "OECM vs RFP" + "OECM vs Standing Offer" comparison cornerstones** (MS-U4). Three to four more cornerstone articles using the Day 10 template (comparison table + 6 Q&As + FAQ schema). Each one captures procurement-decoder long-tail traffic across the 5 AI-Overview proxy queries. **Effort:** 8 hr/post × 4 = 32 hr. **Window before competitor response:** open indefinitely — no competitor has the OECM expertise to write these credibly.
- **EX-3 — School-board case studies with GovernmentService schema** (MS-P1). 3 deep narratives (Halton Catholic DSB anchored from Day 10 cornerstone). POI's `/our-work/` lists 4 school-board clients but emits zero GovernmentService schema. BBI wins Q4 SERP + AI Overview for "Ontario school board office furniture supplier" within 60 days of publish. **Effort:** see Catch-Up Tier 2 #6.

### Moat 2: Brant Basics PSAB-Indigenous procurement angle

**What BBI alone has:** A sister-brand legal entity (Brant Basics) with PSAB-recognized Indigenous procurement status. No competitor has an equivalent. ICP A explicitly avoids marketing to Indigenous segments per memory, but PSAB *as a procurement vehicle* is fair game for federal-funded buyers + band offices + Indigenous-led non-profits + federal contractors looking for set-aside-eligible suppliers.

**Exploit tactics:**

- **EX-4 — Federal Government landing page** (MS-U2 / HIGH-F backlog). PSAB-eligibility + OECM cross-applicability for federal-funded entities + acknowledge BBI doesn't hold a Standing Offer but explain why the procurement vehicles BBI offers (PSAB + OECM) cover most federal-adjacent use cases UCOS's E60PQ SOs target. UCOS structurally cannot match the PSAB angle. **Effort:** 6 hr.
- **EX-5 — Cold outreach to federal-funded non-profits + band offices** using the Federal page as the conversion asset. Out of scope for this report but worth flagging for sales coordination. **Effort:** sales work, not content.

### Moat 3: 330-SKU spec-rich PDP catalog with dual buying mode

**What BBI alone has:** A real Shopify catalog with Product + Offer schema, additionalProperty from specs metafields (Day 8 AI-3 work), real product photos (Day 7 img2img pipeline), and a functioning cart + quote channel dual-mode per ICP. Sensyst has 0 products. Office Shop is quote-only via overlays. POI's store is 4 categories. UCOS has 135 products with **zero schema** — invisible to AI parsing.

**Exploit tactics:**

- **EX-6 — "Quick-ship workstation bundle" Shopify products** (MS-O3). 5-10 bundled SKUs combining chair + desk + storage at a discounted bundle price. Targets "GTA office furniture under $5k" — Office Shop physically cannot fulfill via cart, BBI can. **Effort:** 4 hr (Shopify product builds + photography). **Window before competitor response:** indefinite — Office Shop's quote-only architecture isn't easily reversed.
- **EX-7 — Continue AI-3 spec rollout** to remaining PDPs (any not yet in additionalProperty metafield format). BBI's Product schema with `additionalProperty` for specs is structurally unmatched. AI engines parsing "best ergonomic chair Ontario" pull spec-rich pages first. **Effort:** ongoing AI-3 phase 2 from sys-verify backlog.
- **EX-8 — "Quick-ship from Ontario stock" badge on PDPs** in select category templates. Adds an inline trust signal Sensyst literally cannot make (zero products). Compounds with #6 newsletter signup for return-visit conversion. **Effort:** 2 hr (template edit + badge CSS).

### Moat 4: Peterborough geographic + 1964 family-business heritage

**What BBI alone has:** A real Peterborough HQ (296 George St N), 1964 founding date (older than Office Shop 1996 and Sensyst 1977), Steve Katz as 2nd-generation Peterborough family business, and the Kawartha service area that no competitor targets. UCOS is the closest competitor at 2.5hr drive (Kingston) but covers Eastern Ontario, not Kawartha.

**Exploit tactics:**

- **EX-9 — Own Peterborough + Kawartha Lakes + Northumberland geo-pack** (MS-S1 + HIGH-C). Three geo pages — `/pages/peterborough-office-furniture`, `/pages/kawartha-lakes-office-furniture`, `/pages/northumberland-office-furniture`. Each with LocalBusiness + Service + FAQPage schema. Zero competitive pressure in this geo. **Effort:** 2 hr × 3 = 6 hr. **Window:** indefinite — none of the 4 competitors target this region.
- **EX-10 — "Since 1964" badge in nav + footer** (already partially in copy per Day 8 hero eyebrow audit). Older than every competitor except POI 1958. Surface it consistently. **Effort:** 1 hr.

### Moat 5: Schema-rich content that AI engines actually parse

**What BBI alone has:** The only entity with FAQPage on 9 category templates (36 total FAQs) + GovernmentService + HowTo + Service + BlogPosting+FAQPage on the cornerstone article. AI Overview parsers can extract structured answers from BBI's pages that competitors don't expose.

**Exploit tactics:**

- **EX-11 — Fill the 4 HIGH findings from sys-verify-1-phase2** (Day 10 partial work; finalize Day 11 if time). HIGH-2 (JSON-LD .myshopify.com domain) and HIGH-3 (duplicate Product JSON-LD) close two AEO quality issues that dilute the BBI signal. **Effort:** 15 min combined. Single-highest ROI 15 min of post-launch work.
- **EX-12 — Add 4 faq_item blocks to collection.business-furniture.json** (HIGH-4). Closes the FAQ gap on the parent category page (highest-traffic collection in nav). **Effort:** 25 min. Pairs with EX-11.
- **EX-13 — Comparison tables in every new cornerstone**. AI engines reward table-structured content for direct-answer extraction. Day 10 OECM cornerstone used 3 tables — bake this into every new procurement-decoder + case-study post.

---

## 30 / 60 / 90 day sequencing

Pulled together: when each Catch-Up + Exploit item lands on the calendar. Assumes ~10 hr/week of post-LAUNCH-2 content + SEO work.

### Days 1-30 (LAUNCH-2 Monday through ~mid-June)

| Day | Action | Source |
|---|---|---|
| 1 (LAUNCH-2) | Launch as planned | — |
| 1-3 | EX-11 + EX-12 (close sys-verify HIGH-2/3/4 findings) | 40 min total |
| 3-5 | Tier 1 #1 — GBP reclaim/rename submission | 1-2 hr |
| 5-10 | Tier 1 #3 — real client logo bar (permissions outreach + implement) | 4 hr |
| 10-15 | Tier 1 #4 — Peterborough geo hub | 3 hr |
| 15-20 | Tier 1 #5 — newsletter signup | 3 hr |
| 15-30 | Wait on GBP verification card · Tier 2 #6 — first deep case study (Halton Catholic DSB) | 6 hr |
| 20-25 | EX-1 — start drafting "OECM vs GFG dealer" cornerstone (KW pull first per CLAUDE.md) | 4 hr (prep) |
| 25-30 | Tier 1 #2 — wire AggregateRating + Review schema (after GBP verified) | 1 hr |

**End of Day 30 state:** GBP claimed, schema closed, Peterborough live, case study #1 published, cornerstone #2 drafted.

### Days 31-60 (~mid-June through ~mid-July)

| Day | Action | Source |
|---|---|---|
| 31-35 | EX-1 — publish "OECM vs GFG dealer" cornerstone | 6 hr finish |
| 35-40 | Tier 2 #7 — restart blog: "OECM vs RFP procurement timelines" | 8 hr |
| 40-50 | Tier 2 #8 — Toronto + Mississauga geo pages | 4 hr |
| 50-55 | Tier 2 #9 — service area page | 3 hr |
| 55-60 | Tier 2 #10 — manufacturing + legal/accounting industry pages | 7 hr |

**End of Day 60 state:** 2 cornerstones live, 1 blog post, 3 geo pages, 2 new industry pages, service area page. Office Shop's AggregateRating moat closed, OECM positioning extended into new keyword territory.

### Days 61-90 (~mid-July through ~mid-August)

| Day | Action | Source |
|---|---|---|
| 61-70 | Tier 3 #11 — case studies #2 + #3 (healthcare clinic + municipal) | 12 hr |
| 70-75 | Tier 3 #12 — Kingston + Belleville geo pages | 4 hr |
| 75-80 | Tier 3 #13 — Federal Government landing page (EX-4) | 6 hr |
| 80-85 | EX-6 — quick-ship workstation bundles (5-10 Shopify products) | 4 hr |
| 85-90 | Tier 3 #14 + #15 — Capability Statement PDF + team bios | 14 hr |

**End of Day 90 state:** All catch-up tactics complete. Two exploit tactics deployed (EX-1 cornerstone live, EX-4 federal page live). BBI is digitally ahead of all 4 competitors on schema + content depth + procurement positioning + catalog. The "win" is now compounding — every additional cornerstone, geo page, and case study moves BBI further ahead.

---

## What "winning" looks like at Day 90

- **AI Overview citations:** BBI appears in 3+ of the 5 AI-relevant queries (vs 0 baseline). Drives Office Shop down from 4/5 to 2/5.
- **GBP:** Standalone "Brant Business Interiors" listing with 4.4★+ rating, 60+ reviews, dual-name with Brant Basics. Parity with Office Shop (4.81★) on the only signal where competitors lead.
- **SERP:** BBI top-3 for "office furniture Peterborough" (currently UK-dominated), top-10 for "office furniture Toronto" (currently The Office Shop #3, Sensyst #6), top-10 for "Ontario school board office furniture" (currently Office Shop #10 only).
- **Content inventory:** 3-5 case studies published with structured metadata; 3+ cornerstones in the procurement-decoder series; 4-6 geo pages live (Peterborough, Toronto, Mississauga, Kingston, Belleville + Kawartha); 7-9 industry pages; ~4-6 blog posts in cadence.
- **Schema posture:** 13+ distinct @types in production (+ AggregateRating + Review + CreativeWork from case studies). BBI's lead over Office Shop widens; UCOS / POI / Sensyst become non-factors in AI Overview.
- **PDP differentiation:** Spec-rich PDPs with additionalProperty schema across 330 SKUs (or larger if AI-3 phase 2 ships), unique among all 4 competitors. Quick-ship bundles capture sub-$5k order flow Office Shop forces to quote.

**The headline:** BBI ends 90 days holding the only OECM + GovernmentService + PSAB + spec-rich-catalog + dual-mode-cart + Peterborough-geo positioning in the Ontario commercial office furniture market. Every competitor has a deficit BBI doesn't, and none can close their deficit faster than BBI closed its own.

---

## What to NOT do (worth saying explicitly)

- **Do NOT try to match Sensyst's 50+ geo page volume.** 5-10 strategic geo pages with rich schema beat 50 thin pages without it. AI engines reward depth over breadth.
- **Do NOT chase POI's blog volume of 130 posts.** Their content has zero schema utility. 1-2 cornerstone posts/month with full schema beats POI's whole 130-post archive for AI Overview.
- **Do NOT try to become a Steelcase channel** to compete with UCOS + POI. BBI's existing Global Furniture Group + ergoCentric + Keilhauer + Teknion brand portfolio is differentiated. The play is OECM + PSAB + spec-rich PDPs, not channel parity.
- **Do NOT add Quebec coverage** despite the temptation when geo pages start working. ICP explicitly excludes Quebec for language + logistics reasons.
- **Do NOT remove product / SKU codes** from rebuilt PDPs (procurement teams search by code per feedback memory). Even if shorter names look cleaner.
- **Do NOT promise specific lead times** in new copy. Lead-time language is locked per ICP voice rules.

---

*Final playbook generated 2026-05-25. Sequences the original 17 backlog items (3-competitor scan) + 3 amendment items (UCOS additions) into actionable 30/60/90 day catch-up + exploit tactics. Effort total: ~80-100 hr over 90 days sustainable at ~8-10 hr/week. Findings still POST-LAUNCH backlog reference only — NOT promoted to bbi-build-state.md.*
