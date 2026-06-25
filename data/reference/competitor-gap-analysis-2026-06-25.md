# Competitor Gap Analysis — BBI (Phase 1 research)

**Date:** 2026-06-25 · **Branch:** `research/phase1-competitor-brand-demand-2026-06-25` · **READ-ONLY research. No theme, no Shopify writes, no published flags. No competitor page copy reproduced — intelligence only (URL / keyword / volume / position / traffic estimate / page TYPE).**

**Data source:** **DataForSEO** (DataForSEO Labs `ranked_keywords` live, reused via `scripts/dfs_client.py` REST path — the same mechanism Step 3/5a + Track C used; key never printed). **Not** the live-SERP fallback.
**Market:** location = **Canada** (location_code 2124), language = **en**. (DataForSEO Labs `ranked_keywords` is country-level; Ontario-level not available on this endpoint — Canada-wide used, which is the correct superset for an Ontario/Western-Canada B2B dealer.)
**Scope filter applied** (per `priority-keywords.yaml`): dropped electronics/IT (tablets, iPads, monitors, mice), office-supplies/consumables (Staples/Grand & Toy noise), gaming chairs, foreign-geo, and pure brand-navigational terms from the *clean opportunity* set. Raw pulls retained under `data/research/phase1-raw/`; parsed CSVs under `data/research/phase1-parsed/`.

**Competitor set (live domains that returned data):** `poi.ca`, `theofficeshop.ca`, `atwork.ca`, `sourceofficefurniture.ca`, `grandandtoy.com`, `staples.ca`.
> ⚠ Domain notes: `poibusinessinteriors.com` and `sourceofficefurniture.com` returned **zero** ranked keywords — POI's live domain is **poi.ca** and Source's is **sourceofficefurniture.ca**; those are used instead. Staples & Grand & Toy are general-merchandise retailers — their furniture rows are filtered, but their org traffic is overwhelmingly non-furniture (IT/supplies), so treat them as *category-head* foils only, not strategic peers.

**BBI baseline:** brantbusinessinteriors.com ranks in the top-20 for very few commercial heads. Its best positions are mostly **brand-navigational** (`brants office` p5) or **long-tail product** (`teknion ls` p15, `wardrobe with lock` p15, `pedestal drawers` p19, `meeting table for office` p20). Nearly every category head below is **absent or >p20** for BBI — confirming the near-zero-authority position (memory: ~49 ranking kw). Full list: `data/research/phase1-parsed/comp_*.csv` + BBI rows in the parser log.

---

## 1. TOP PAGES PER COMPETITOR (highest organic traffic, page TYPE tagged)

Page TYPE legend: **BLOG** = article/blog/news/resource · **COLLECTION** = category/shop listing · **PDP** = product detail · **LANDING** = service/brand/city/project/home page. `etv` = DataForSEO estimated monthly organic traffic to that URL from the matched keywords; `vol` = monthly search volume of the page's top keyword.

### poi.ca — wins on PROJECT-PORTFOLIO + thin BLOG (not commercial category pages)
| URL | Primary kw | vol | pos | etv | TYPE |
|---|---|---|---|---|---|
| /about-us/ | poi | 12100 | 6 | 797 | LANDING(home/brand-nav) |
| / | poi business interiors | 1300 | 1 | 435 | LANDING(home) |
| /our-work/kingsettcapital/ | 40 king street west | 2400 | 14 | 98 | LANDING(project) |
| /roserock-place/ | roserock place | 590 | 2 | 96 | LANDING(project) |
| /products/architecture-space-division/walls-work-walls/dirtt | dirtt | 880 | 6 | 61 | PDP(brand) |
| /products/series-1 | steelcase series 1 | 590 | 4 | 56 | PDP(brand) |
| **/blog/audio-visual-technology-trends-solutions-2020/** | audio visual technology | 480 | 8 | 47 | **BLOG** |
| /limberlost-place/ | limberlost place | 2900 | 10 | 44 | LANDING(project) |
| /connected-solutions/moves-and-relocation/ | office relocation service | 170 | 6 | 40 | LANDING(service) |
| **/blog/elevate-indoor-air-quality-with-surgically-clean-air/** | surgically clean air | 480 | 13 | 20 | **BLOG** |
| /products/leap-x | leap chair | 210 | 8 | 17 | PDP(brand) |

### theofficeshop.ca — wins on BRAND landing pages + CITY/LOCATION pages
| URL | Primary kw | vol | pos | etv | TYPE |
|---|---|---|---|---|---|
| / | office furniture shop | 590 | 1 | 642 (22 kw) | LANDING(home) |
| /product_brands/global-contract/ | globalcontract | 590 | 5 | 65 | LANDING(brand) |
| /product_brands/global-total-office/ | global total office | 480 | 3 | 62 | LANDING(brand) |
| /product_brands/used-office-furniture/ | 2nd hand office furniture | 880 | 10 | 54 | LANDING(brand/used) |
| /rentals/ | office rent furniture | 90 | 4 | 38 | LANDING(service) |
| /product_brands/keilhauer/ | keilhauer office chair | 90 | 4 | 34 | LANDING(brand) |
| /locations/vaughan/ | office furniture vaughan ontario | 90 | 5 | 29 | LANDING(city) |
| /locations/ottawa/ | office equipment stores near me | 2400 | 17 | 26 | LANDING(city) |
| /locations/london/ | office furniture london ontario | 110 | 2 | 24 | LANDING(city) |
| /product_brands/iof/ | iof furniture | 480 | 5 | 23 | LANDING(brand) |
| /product_category/reception/ | reception desk | 2400 | 17 | 18 | COLLECTION |

### atwork.ca — wins on HOME + BRAND-DEALER landing pages + COLLECTION category pages
| URL | Primary kw | vol | pos | etv | TYPE |
|---|---|---|---|---|---|
| / | office seating | 33100 | 9 | 2108 | LANDING(home) |
| /brand/hon-furniture_canada/ | hon dealers | 18100 | 3 | 1874 | LANDING(brand-dealer) |
| /product-category/desks/reception-desks/ | reception desk(s) | 2400 | 4 | 1202 (9 kw) | COLLECTION |
| /locations/...-london-ontario/ | (atwork) london | 880 | 1 | 568 | LANDING(city) |
| /product-category/office-phone-booth-pod/ | office pod | 720 | 2 | 339 | COLLECTION |
| /brand/artopex_canada/ | artopex | 4400 | 6 | 290 | LANDING(brand-dealer) |
| /product-category/office-cubicles-panels/cubicles/ | cubicle desk | 170 | 2 | 190 | COLLECTION |
| /product-category/tables/boardroom-conference-tables/ | boardroom table | 880 | 4 | 183 | COLLECTION |
| /brand/tayco_canada/ | tayco | 2400 | 6 | 158 | LANDING(brand-dealer) |
| /shop/filing-storage/.../gardex-classique | fire safe file cabinet | 390 | 4 | 139 | COLLECTION |

### sourceofficefurniture.ca — the COLLECTION-page engine (dominates category heads)
| URL | Primary kw | vol | pos | etv | TYPE |
|---|---|---|---|---|---|
| /shop/office-chairs-and-seating | office (with) chairs / office seating | 33100 | 3 | **17038 (7 kw)** | COLLECTION |
| /shop/desks-and-workstations | office desk | 9900 | 1 | 6252 (8 kw) | COLLECTION |
| /brand/hon | hon dealers | 18100 | 2 | 2932 | LANDING(brand-dealer) |
| / | source office furniture | 4400 | 1 | 2777 | LANDING(home) |
| /shop/filing-cabinets | filing cabinet | 12100 | 3 | 2264 | COLLECTION |
| /shop/desks-and-workstations/corner-and-l-shaped-desks | l shaped office desk | 880 | 1 | 816 | COLLECTION |
| /shop/bookshelves-and-storage/storage-cabinets-and-racks | cabinet and storage | 8100 | 4 | 788 | COLLECTION |
| /shop/reception-and-waiting-area-furniture/reception-desks | reception desk | 2400 | 2 | 730 | COLLECTION |
| /shop/standing-desks-and-height-adjustable-tables | electric standing desk | 1600 | 4 | 575 | COLLECTION |
| /shop/conference-and-boardroom-tables | boardroom table | 880 | 1 | 486 | COLLECTION |
| /shop/office-chairs-and-seating/ergonomic-chairs | desk chairs vancouver | 480 | 4 | 438 | COLLECTION |

### grandandtoy.com / staples.ca — general retailers (furniture is a sliver; foils only)
| URL | Primary kw | vol | pos | etv | TYPE | domain |
|---|---|---|---|---|---|---|
| / | office products supplies | 5400 | 5 | 7155 (47 kw) | LANDING(home) | grandandtoy |
| /collections/office-chairs-65 | desk chair office | 33100 | 3 | 11262 (9 kw) | COLLECTION | staples |
| /collections/gaming-chairs-6877 | gaming chair | 27100 | 4 | 4391 | COLLECTION | staples |
| /collections/filing-cabinet-68 | filing cabinet | 12100 | 5 | 1284 | COLLECTION | staples |
| /collections/chairmats-69 | office chair floor mat | 1900 | 1 | 2466 | COLLECTION | staples |

**Strategic read (Section 1):**
- **The competitor organic-traffic engine is COLLECTION + BRAND-DEALER + CITY pages — *not* blog.** Source and atWork pull virtually all their furniture traffic from category collections (`office seating`, `office desk`, `filing cabinet`, `reception desk`, `boardroom table`, `standing desk`) and brand-dealer landing pages (`hon dealers`, `artopex`, `tayco`). theofficeshop adds `/product_brands/*` and `/locations/*`.
- **Blog winners are nearly absent.** Across all six domains the only true BLOG winners are two aging poi.ca posts (`audio-visual-technology-trends`, `surgically-clean-air`). This is a double finding: (a) BBI's Track A/C **blog engine is contrarian whitespace** — no competitor is contesting informational/comparison content; (b) but the **larger untapped near-term gap is commercial COLLECTION + BRAND-PAGE optimization**, where BBI is absent and competitors bank the traffic.
- **Brand-dealer landing pages convert traffic** (atWork's `hon dealers` page = ~1,874 etv; Source's = ~2,932). This directly reinforces FILE B: BBI's carried-brand pages are the structural-advantage play.

---

## 2. CONTENT GAP — keywords competitors rank for (top ~20) where BBI is absent or >p20

Sorted by **volume × #competitors ranking** (multi-competitor = stronger signal). Full list (245 clean rows + 378 raw): `data/research/phase1-parsed/gap.csv`. Flags applied per the legend at the bottom.

| Keyword | vol | #comp | competitors | BBI | Flag → surface |
|---|---|---|---|---|---|
| office seating | 33,100 | 3 | atwork, source, staples | absent | **CLEAN** → Step 2 seating category/collection |
| office with chairs | 33,100 | 2 | source, staples | absent | CLEAN (near-dup of office seating) → Step 2 seating |
| desk chair office | 33,100 | 1 | staples | absent | CLEAN (seating head) → Step 2 seating |
| filing cabinet | 12,100 | 2 | source, staples | absent | **CLEAN** → Step 2 filing/storage (BBI only ranks fire-resistant subset) |
| l-shaped desk | 8,100 | 2 | source, staples | absent | **CLEAN** → Step 2 desks category |
| office desk | 9,900 | 1 | source | absent | **CLEAN** → Step 2 desks category |
| computer desk | 9,900 | 1 | staples | absent | CLEAN (consumer-leaning) → Step 2 desks |
| bookcases / bookshelves | 9,900 | 1 | staples | absent | **CLEAN** → Step 2 storage category |
| ergonomic office seating | 9,900 | 1 | staples | absent | [CANNIBAL] — `/pages/ergonomic-office-chairs` owns ergonomic-chair heads |
| cabinet and storage | 8,100 | 1 | source | absent | **CLEAN** → Step 2 storage category |
| hutch | 8,100 | 1 | source | absent | **CLEAN** → Step 2 desks/storage |
| folding table | 14,800 | 1 | staples | absent | CLEAN (events/consumer overlap) → Step 2 training/folding tables |
| reception desk | 2,400 | 3 | atwork, source, theofficeshop | absent | [CANNIBAL] — `reception` is a LOCKED funnel_target (`reception desk` head) |
| office chair near me | 2,400 | 3 | source, staples, theofficeshop | absent | [CANNIBAL] near-me → 14 live city pages / seating |
| office furniture near me | 1,300 | 2 | atwork, source | absent | [USED] — Track A Slot 1/2 claimed (1300) |
| office furniture stores | 590 | 2 | source, theofficeshop | absent | [USED] — Track A Slot 2 primary (590) |
| boardroom table | 880 | 2 | atwork, source | absent | [CANNIBAL] — `boardroom` LOCKED funnel_target (`boardroom table` head) |
| conference table | 720 | 2 | atwork, source | absent | [CANNIBAL] — `boardroom` secondary + Track A Slot 13 |
| drafting chair | 880 | 2 | source, staples | absent | **CLEAN** → Step 2 seating (drafting stools niche) |
| sit stand desk / electric standing desk | 1,600–4,400 | 1 | source | absent | [CANNIBAL]+[USED] — `best-standing-desks-canada` live + Track A Slot 6 + 5a-pending desk cluster |
| task chair canada | 2,900 | 1 | staples | absent | **CLEAN (borderline)** → Step 2 seating (collection head; Step-6 owns *use-case* review heads, not this) |
| stacking chairs / stackable chairs | 1,300 ×2 | 1 | source | p73 | **CLEAN** → Step 2 stacking-chairs collection (BBI ranks weak p73 → improve) |
| office table | 1,900 | 1 | source | absent | CLEAN → Step 2 tables |
| chair mat / office chair floor mat | 1,300–1,900 | 1–2 | source, staples | absent | CLEAN-LOW (accessory; verify BBI carries) |
| comfort chairs for office | 1,000 | 1 | source | absent | CLEAN → Step 2 seating |
| 2 drawer filing cabinet | 1,000 | 1 | source | absent | CLEAN → Step 2 filing (long-tail of filing cabinet) |
| gardex | 1,000 | 1 | atwork | absent | [CARRIER-soft] — Gardex IS stocked (fire-filing, 6 SKUs) but NOT on the FILE-B actionable list; brand-nav |
| krug / spec furniture / lacasse / logiflex | 1,300–1,600 | 1 | source, atwork, theofficeshop | absent | [CARRIER] — NON-carried manufacturers; foil/fit only, not page targets |
| hon / artopex / tayco | 2,400–18,100 | 1–2 | atwork, source | absent | [CARRIER] — NON-carried; competitor dealer-nav, not targets |
| 40 king street west / limberlost / roserock / sickkids patient support centre | 2,400–3,600 | 1 | poi | absent | [CANNIBAL-n/a] — POI *project-name* navigational, not a furniture category; skip |

---

## FLAGS legend (advisory only — building is a separate gated step)
- **[CARRIER]** — built around a brand BBI does **not** carry (HON, Artopex, Tayco, Krug, Spec, Lacasse, Logiflex, Herman Miller, Steelcase, Haworth, Nightingale). Not a page target; cautious-bucket / fit-based foil only; Steve legal glance.
- **[CANNIBAL]** — overlaps a LOCKED owner in `priority-keywords.yaml` (`reception desk`→reception; `boardroom table`/`conference table`→boardroom; ergonomic-chair heads→`/pages/ergonomic-office-chairs`; use-case chair heads→Step-6 review pages; `office furniture <city>`→14 live city pages; standing-desk heads→`best-standing-desks-canada` + Track A Slot 6).
- **[USED]** — already claimed in `batch-ledger.md` (Track A) or `batch-ledger-trackC.md` (Track C) — e.g. `office furniture stores` (Slot 2), `office furniture near me` (Slot 1/2).
- **[SURFACE]** — clean opportunity mapped to its BBI step: **Step 2** category/collection intro · Step 4 brand-page deepen · Step 5a ergonomic · Step 5b healthcare · Step 6 review page · Step 7 city · new blog batch (Batch 3).
- Live blog state reconfirmed via the ledgers: **News blog 108557861177 ≈ 39 published + Track C drafts (A1–A4, C1–C4 + R1/R2 staged, C2 legal-held)**. No gap term below duplicates a live/staged article intent.

---

## TOP 10 CLEAN COMPETITOR OPPORTUNITIES (no carrier/cannibal/used flag), ranked, mapped to surface

The clean set is dominated by **commercial CATEGORY-HEAD terms BBI is absent for on its own collection pages** — i.e. the same engine Source/atWork run. The surface is **Step 2 category/collection intro + meta optimization** (not new blog posts). This is the single highest-leverage near-term gap.

| # | Keyword | vol | Why clean | Surface |
|---|---|---|---|---|
| 1 | **office seating** (+ `office with chairs`, `desk chair office`, `task chair canada` 2,900) | 33,100 | Largest furniture head; 3 competitors rank, BBI absent on its own seating collection; not a locked owner (Step-6 owns *use-case* review heads only) | **Step 2** — seating/task-chairs collection intro + meta |
| 2 | **filing cabinet** (+ `2 drawer filing cabinet`) | 12,100 | BBI ranks only the fire-resistant subset; the general filing head is open; 2 competitors rank | **Step 2** — filing/storage collection |
| 3 | **office desk** (+ `l-shaped desk` 8,100, `hutch` 8,100) | 9,900 | Core desks head; Source owns it, BBI absent; no locked owner | **Step 2** — desks collection |
| 4 | **bookcases / bookshelves** | 9,900 | Storage head, Staples-only, BBI absent; clean | **Step 2** — storage/bookcase collection |
| 5 | **cabinet and storage** (storage cabinets) | 8,100 | Storage head, Source owns, BBI absent; clean | **Step 2** — storage cabinets collection |
| 6 | **folding table** (training/flip-top) | 14,800 | High volume; BBI carries flip-top/training tables; clean (note events/consumer overlap — frame commercial) | **Step 2** — training/folding tables collection |
| 7 | **stacking chairs / stackable chairs** | 1,300 ×2 | BBI already ranks p73 — improvement, not net-new; Source owns top | **Step 2** — stacking-chairs collection (optimize existing) |
| 8 | **drafting chair / drafting stool** | 880 | Niche seating BBI carries; 2 competitors rank; uncontested by locked owners | **Step 2** — seating (drafting) collection |
| 9 | **office table** (+ `comfort chairs for office` 1,000) | 1,900 | Generic tables/seating heads, Source-only, BBI absent | **Step 2** — tables / seating collections |
| 10 | **computer desk / computer chair** | 9,900 / 5,400 | High volume; consumer-leaning so lower-priority, but commercial intent exists; clean | **Step 2** — desks/seating (frame as commercial), or Batch-3 blog angle |

**Meta-recommendation for the next build step:** the biggest, cleanest, lowest-risk win is a **Step-2 commercial-collection optimization pass** (seating, desks, filing, storage, tables) — write category-intro copy + tune collection meta to contest `office seating / office desk / filing cabinet / bookcases / storage cabinets`. This is where competitors actually earn furniture traffic and where BBI is most absent. Blog (Batch 3) remains genuine whitespace but is a slower, lower-traffic lane than the collection gap.

---

## BUILD-STATE NOTE (for the next doc PR — not edited this session)
> Phase-1 research shipped two findings files (`data/reference/competitor-gap-analysis-2026-06-25.md`, `data/reference/brand-demand-canada-2026-06-25.md`). **Key strategic finding:** competitors' organic furniture traffic comes from COLLECTION + BRAND-DEALER + CITY pages, not blog — recommend opening a **Step-2 commercial-collection optimization** workstream (seating/desks/filing/storage/tables heads BBI is absent for) ahead of, or alongside, Batch-3 blog. De-confliction in these files is advisory (flags only); any build is a separate gated step.
