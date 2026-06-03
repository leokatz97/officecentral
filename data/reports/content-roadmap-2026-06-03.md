# BBI Content Roadmap — Pillar/Cluster Plan (AEO + SEO)

**Date:** 2026-06-03 · **Branch:** `feature/content-roadmap-2026-06-03` · **DOCS/PLANNING ONLY — no production pages, no theme writes**

Reconciles two signals:
- **HARD signal (demand + whitespace):** PR #66 `COMPETITOR-KEYWORD-RECON-1` + `KEYWORD-SEED-EXPANSION` — 2,428 competitor keywords (12 Ontario/QC/BC dealers, DataForSEO, sv≥10) + 468 BBI-positioning seed keywords (460 net-new whitespace). Sources in [data/reports/keyword-research/](keyword-research/) (`SUMMARY-2026-05-30.md`, `SEED-EXPANSION-SUMMARY-2026-05-30.md`, `PAGE-ARCHETYPE-ANALYSIS-2026-05-30.md`).
- **SOFT signal (real questions → cluster + FAQ/AEO):** Leo's two HeyTony Reddit-mined topic lists (40 "Ontario office furnisher/supplier" + 40 "Canadian B2B/institutional", + bonus topics). Real buyer questions — ideal cluster-page and FAQPage fodder, but they do NOT set priority. Priority comes from the recon.

Build-state context: content engine = **TIER 3 / Stream B**. Cornerstone Post 1 LIVE since 2026-05-23 (`/blogs/news/oecm-ontario-school-boards-office-furniture`, OECM/education). D3 internal-linking pass **HELD** until Tier 1 URLs final. Filter system **DEFERRED** (not touched here).

---

## Phase 1 — Reconciliation findings

### 1.1 Pillar priority — VALIDATED against recon numbers

The framework's proposed order **P1 → P2 → P3 → P4 holds**, but the data reframes *why* each ranks where it does. Critically: the recon's raw volume is overwhelmingly `product_generic` / `ecom-purchase` (1,676 kw / 1.19M volume → **PDP + collection pages, not blog content**). For the *content engine* specifically, the right lens is **informational/question demand + competitor whitespace**, not gross volume.

| Pillar | Recon evidence | Verdict |
|---|---|---|
| **P1 — Design & space-planning** | Competitors near-absent: only **5** `design_service` kw across all 12 competitors; blog/content = **0.2%** and service pages **0.0%** of competitor organic traffic (PAGE-ARCHETYPE). Seed expansion found **127 net-new** design seeds + **115 net-new** `design-consultation` outcome kw. Per-kw volume is low (10–50/mo) but **uncontested + owns the design-consultation conversion path**. | **#1 CONFIRMED.** Biggest genuine *content* whitespace + the production focus. Wins on differentiation + conversion, not volume. |
| **P2 — Public-sector / OECM** | Lowest measurable demand of all: `oecm_procurement` = **1 net-new kw (vol 10)**; `compliance_certification` = **0** and `procurement_process` = **0** competitor kw. But that zero IS the moat — uncontested, highest-value buyers, already anchored by live Cornerstone Post 1. | **#2 CONFIRMED — strategic, volume-independent.** Cornerstone cadence, not a volume play. |
| **P3 — Ergonomics, wellness & durability** | **Strongest raw AEO/informational demand in the entire dataset:** `ergonomics of chair` **14,800/mo informational**; the whole PAA list is ergonomics/standing-desk/Herman-Miller ("20 8 2 rule", "30/30 rule", "90-90-90", "best chair for long hours", "is Herman Miller worth it"); 2 of 2 AI-Overview triggers are ergonomics-adjacent. Commercial volume too (`best office chairs` 4,400, `standing desk` 18,100). | **#3 as a pillar, BUT data says its demand >> P1/P2/P4.** → **Nuance A:** pull P3's FAQ/AEO cluster *early* in the sequence (right after the P1 opener) to capture the PAA / AI-Overview wins. |
| **P4 — Buying office furniture in Ontario** | Net-new geo lane: **25 net-new** Eastern-Ontario geo kw (vol 500) + 7 defensible Eastern-Ontario geo from competitors; geo pages convert local intent and are **~2%** of competitor traffic but thinly held → winnable. `office relocation services` 170, `best office chairs canada` 880, `canadian office chairs` **2,900**, `used office furniture` 880. | **#4 CONFIRMED — bottom-funnel.** → **Nuance B:** geo is a genuine *net-new, winnable* lane but low absolute per-kw volume → interleave with the geo landing pages + buy-canadian, don't lead with it. |

**Where does P4-geo rank?** As a *net-new whitespace* lane it's strong (uncontested, BBI's Eastern-Ontario home turf), but on absolute volume it's small (10–40/mo per city). It earns its place by tying directly to the geo landing-page program + the buy-canadian collection — structural, not blog-volume, value.

### 1.2 Keep/drop — validated against keyword data

Promotions/demotions from the framework's "borderline" guidance, with the numbers that drove them:

- **PROMOTE → P3:** "How much should I spend on an office chair" — reframed commercial as **"best office chairs in Canada / are ergonomic chairs worth it."** Real demand: `best office chairs` 4,400, `best office chairs canada` 880, `best office chair for long hours` 260, `cost of office chair` 110, plus a dense PAA value-question vein. The consumer "how much should I spend" framing is dropped in favour of the commercial framing.
- **PROMOTE → P4:** "Affordable Ontario" — merged into **"furnish a small office on a budget"** (B2B framing). Supporting: `office chairs cheap` 720, `best budget office chair` 590. Kept as one cluster, not a standalone.
- **KEEP (strong, was understated):** Reception furniture (`reception desk` **2,900**), boardroom/meeting (`boardroom tables` 880, `conference table` 720), standing/height-adjustable (`standing desk` **18,100**, `sit-stand desk` 4,400) → these get dedicated clusters.
- **KEEP (Canadian-made moat):** buy-Canadian — `canadian office chairs` **2,900**, `canadian desks` 720, `canadian made office chairs` 140 → strong P4 cluster tying to the buy-canadian collection.
- **DEMOTE → DROP:** gender-neutral spaces, intergenerational workforces, "smart furniture", "match styles & colors", warranties-as-standalone — **no measurable demand** in either dataset. (Warranties folded into a P4 buying-guide FAQ rather than a standalone post.)
- **CONTEXT FLAG — used/refurbished:** Eastern-Ontario "used office furniture {city}" terms are net-new geo whitespace, but **BBI sells new.** "Used vs new / refurbish vs new" is kept only as a P3 *decision-guide* that steers to new (and, for nonprofits/school boards, to budget-tier new) — NOT as a "we sell used" claim or a used-geo target.

---

## Phase 2 — The roadmap

**Conventions.** Each cluster row: **topic** · target keyword (volume/difficulty) · intent · conversion path. Volume/KD from the recon where a mapped keyword exists; design/space-planning rows cite seed-expansion volumes (low but uncontested) and are marked *(seed)*; rows with no mapped keyword are marked *(no direct kw — AEO/topical)* and justified by PAA/question demand. Difficulty is "easy" unless noted (the recon's `difficulty_band` is "easy" for the vast majority of office-furniture terms).

**AEO treatment (all pillars):** every post emits **Article (BlogPosting) JSON-LD** via `ds-article.liquid` (already proven on Post 1). Posts built around real Q&A additionally emit **FAQPage** schema — flagged **[FAQ]** below. The Reddit topics are almost all question-format, so most clusters are FAQPage candidates. Tables + `scope`/`<caption>` markup (the Post-1 AEO pattern) on any comparison content.

---

### ⭐ P1 — Office Design & Space-Planning  *(priority #1 — biggest content whitespace, design-consultation conversion path)*

**Pillar page:** **"How to Plan an Office Layout: A Space-Planning Guide for Ontario Businesses"** · `office space planning` / `office floor plan` / `office layout planning` (40–260/mo *(seed + comp)*, easy, design_service) · informational→commercial · **→ /pages/design-services (book a free consultation); → Quiet Spaces, workstations, desks collections.** This is the hub the whole pillar links into.

| Cluster topic | Target keyword (vol/KD) | Intent | Conversion path |
|---|---|---|---|
| Right-sizing: how much office space / how much furniture do we need *(merges B1, B20, B35)* | `office space planning calculator`/`standards` (10–40 *(seed)*) **[FAQ]** | informational | → design-services consult |
| Best office layout for hybrid / 3-days-in-office *(merges B2, B14, B23)* | hybrid layout *(no direct kw — AEO/topical)* **[FAQ]** | informational | → design-services; workstations |
| Desk allocation for a hybrid workforce / fixed vs hot-desking *(merges B3, B27)* | `hot desk` / `shared desk` (50) **[FAQ]** | informational | → benching/multi-person workstations |
| Downsizing to a hot-desk setup & reducing real-estate cost *(merges B4, B20)* | office space optimization *(no direct kw — AEO/topical)* | informational | → benching desks; design-services |
| Furniture for activity-based working *(B5)* | activity-based working *(no direct kw — AEO/topical)* | informational | → modular/workstations |
| Modular / scalable / future-proof layouts *(merges B11, B24, B32, B40)* | `modular office furniture for small spaces` (10 *(seed)*) | commercial | → modular collections |
| Create focus / quiet zones in an open office *(merges A?, B12)* | noise-reducing / acoustic *(no direct kw — AEO/topical)* **[FAQ]** | informational | **→ Quiet Spaces collection (acoustic pods)** |
| Private meeting spaces & breakout areas in an open office *(merges B21, B25)* | `boardroom tables` 880 / `meeting table` 170 **[FAQ]** | commercial | → meeting/boardroom + Quiet Spaces |
| Meeting-room furniture for small businesses *(A37)* | `conference table` 720 / `boardroom chairs` 210 | commercial | → boardroom collection |
| Furniture supporting collaboration & video conferencing for hybrid/remote teams *(merges A?, B7, B28, B34)* | collaboration furniture *(no direct kw — AEO/topical)* | informational | → collaborative seating/tables |
| Reception-area furniture for small offices *(A39)* | `reception desk` **2,900** / `reception desk office` 140 *(seed)* | commercial | → reception desks collection |
| Compact / small-office & multi-purpose furniture *(merges A22, B24)* | `small office furniture` 30 *(seed)* / `office furniture for small spaces` 20 | commercial | → small-space collection |
| Shared-workspace organization & storage *(merges A30, B10, B30)* | shared workspace storage *(no direct kw — AEO/topical)* | informational | → storage collection |
| Designing an office for in-person + remote (hybrid) teams *(merges B14, B28; hybrid bonus A)* | hybrid workplace design *(no direct kw — AEO/topical)* **[FAQ]** | informational | → design-services |
| Office design that boosts culture, appeal & retention *(merges B6, B17)* | employee retention furniture *(no direct kw — AEO/topical)* | informational | → design-services |
| Phased / transition-year furniture strategy *(B32)* | phased office furniture *(no direct kw — AEO/topical)* | informational | → design-services; quote |
| Free / virtual design consultation — what to expect *(bonus A: free + virtual consults)* | `workspace planning` 50 *(seed)* / `office fit out` 30 *(seed)* | commercial→consult | **→ design-services (primary conversion CTA)** |

*Cross-link note:* "Office furniture for different job types & industries" (A35) is **topical-overlap with the Industries Hub** — treat as an industry-page cross-link, not a P1 blog.

---

### 🏛 P2 — Public-Sector / Institutional / OECM  *(priority #2 — uncontested moat, cornerstone cadence; volume-independent)*

**Anchor (LIVE):** Cornerstone Post 1 — *OECM for Ontario School Boards (Agreement 2025-470)*. **Pillar role** for the whole pillar; already emits BlogPosting + FAQPage.

**Planned cornerstones (already outlined/queued in build-state):** Post 2 — Healthcare/FHT procurement; Post 3 — *Cubicle vs Open-Plan for Municipal Offices*.

| Cluster topic | Target keyword (vol/KD) | Intent | Conversion path |
|---|---|---|---|
| How to furnish a government office efficiently *(B16)* | `government of canada surplus office furniture` 10 *(seed)* / gov office setup *(AEO/topical)* **[FAQ]** | informational | **→ /pages/government; → /pages/oecm; quote** |
| What furniture provincial government offices use + procurement rules *(merges B22, bonus: provincial procurement rules)* | provincial procurement *(no direct kw — AEO/topical, BPS framing)* **[FAQ]** | informational | → /pages/oecm; /pages/government |
| Furnishing a local / municipal office *(B31)* | municipal office furniture *(no direct kw — AEO/topical)* **[FAQ]** | informational | → /pages/government; Post 3 (cubicle vs open-plan) |
| What furniture do school offices need / making a school office functional *(merges B13, B29)* | `educational furniture` 70 / `classroom furniture canada` 170 *(seed)* **[FAQ]** | informational | **→ /pages/education; Post 1 (OECM)** |
| Budget-friendly furniture for school boards & nonprofits *(merges bonus B: school-board budgets, nonprofit refurb)* | school board budget *(no direct kw — AEO/topical)* | informational | → /pages/education; budget-tier collections |
| Public-sector vs private-sector furniture requirements *(B36)* | public vs private sector *(no direct kw — AEO/topical)* **[FAQ]** | informational | → /pages/oecm; /pages/government |
| Reception/lobby furniture for government offices *(B38)* | `reception desk` 2,900 (gov-framed) | commercial | → /pages/government; reception collection |
| Accessibility / wheelchair-accessible & compliant furniture *(merges A?, B26, bonus A: wheelchair-accessible)* | accessible office furniture *(no direct kw — AEO/topical)* **[FAQ]** | informational | → /pages/oecm (compliance angle) |
| Furnishing an office quickly for a new mandate *(B37)* | urgent gov setup *(no direct kw — AEO/topical)* | commercial | → quote; relocation/delivery |

*Note:* P2 demand is ~zero by volume — these are **AEO/positioning plays** that win citations and trust with high-value buyers, anchored by Post 1's live schema. Cornerstone cadence (1 every ~2–3 weeks), NOT volume-chasing.

---

### 🪑 P3 — Ergonomics, Wellness & Durability  *(priority #3 as a pillar — but HIGHEST raw AEO/PAA demand → run its FAQ cluster early)*

**Pillar page:** **"The Ontario Buyer's Guide to Ergonomic Office Seating"** · `best office chairs` 4,400 / `ergonomics of chair` **14,800 (informational)** · informational→commercial · **→ seating collection; ergonomic-chairs collection; quote.**

| Cluster topic | Target keyword (vol/KD) | Intent | Conversion path |
|---|---|---|---|
| **PAA/AEO FAQ hub** — is an ergonomic chair worth it · 20-8-2 rule · 90-90-90 · best chair for long hours · is Herman Miller worth it *(merges A5 reframed, A31)* | `best office chair for long hours` 260 / huge PAA vein **[FAQ — primary AEO asset]** | informational | → seating; ergonomic-chairs collection |
| Height-adjustable / sit-stand desk benefits *(merges bonus A: height-adjustable, A19 reframed, bonus B: desk-height)* | `standing desk` **18,100** / `sit-stand desk` 4,400 / `adjustable desk` 3,600 **[FAQ]** | commercial | → height-adjustable-tables collection |
| Should we invest in ergonomic furniture for hybrid workers *(B8)* | ergonomic furniture roi *(no direct kw — AEO/topical)* **[FAQ]** | informational | → seating; design-services |
| Best chairs for all-day comfort / different body types *(merges A31, bonus B: body types)* | `heavy duty office chairs` 170 / `best office chairs` 4,400 | commercial | → ergonomic-chairs collection |
| Most durable furniture for high-traffic spaces *(B15)* | `heavy duty office chairs` 170 / commercial-grade *(AEO/topical)* **[FAQ]** | commercial | → commercial-grade collections |
| Home vs commercial-grade office furniture (durability differentiation) *(A6)* | commercial vs home grade *(no direct kw — AEO/topical)* **[FAQ]** | informational | → commercial collections; quote |
| How long does office furniture last *(A32)* | furniture lifespan *(no direct kw — AEO/topical)* **[FAQ]** | informational | → quote; warranty FAQ |
| Buy new vs refurbish *(merges A16, B18; nonprofit framing)* **[steers to NEW — BBI sells new]** | new vs refurbished *(no direct kw — AEO/topical)* **[FAQ]** | informational | → budget-tier new collections |
| Creating wellness / mental-health spaces *(merges B33, bonus B: mental-health designs)* | wellness office design *(no direct kw — AEO/topical)* **[FAQ]** | informational | → lounge/soft-seating; Quiet Spaces |
| Sustainable / eco-friendly (Canadian-made tie) *(merges A40, bonus B: sustainable)* | `recycled office furniture` 50 / Canadian-made *(AEO/topical)* | informational | **→ buy-canadian collection** |

---

### 📍 P4 — Buying Office Furniture in Ontario  *(priority #4 — bottom-funnel; ties to geo landing pages + buy-canadian)*

**Pillar page:** **"Where to Buy Office Furniture in Ontario: A Complete Buyer's Guide"** *(A1)* · `office furniture toronto` 480 / `used office furniture` 880 / city geo terms · commercial · **→ geo landing pages; quote.**

| Cluster topic | Target keyword (vol/KD) | Intent | Conversion path |
|---|---|---|---|
| **Eastern-Ontario geo set** — Peterborough / Oshawa / Kingston / Whitby / Belleville office furniture *(net-new geo whitespace)* | `office furniture peterborough` 30 / `oshawa office furniture` 40 / `office furniture kingston ontario` 30 *(seed, easy)* | commercial-local | **→ geo landing pages (1 per city); quote** |
| How to find quality office desks near Toronto *(A2)* | `office furniture toronto` 480 / geo | commercial-local | → Toronto geo page; desks collection |
| Local Ontario suppliers vs national chains *(differentiation moat)* *(bonus B)* | local vs national *(no direct kw — AEO/topical)* **[FAQ]** | informational | → about/why-BBI; quote |
| Buy Canadian / Canadian-made & local customization *(merges A23, bonus A+B: customization)* | `canadian office chairs` **2,900** / `canadian made office chairs` 140 | commercial | **→ buy-canadian collection** |
| How to request a quote / the consultation process *(A29)* **[high-conversion]** | quote process *(no direct kw — AEO/topical)* **[FAQ]** | commercial | **→ /pages/quote (primary CTA)** |
| Delivery, installation & turnaround / same-day *(merges A8, A15, bonus A: same-day)* | `office furniture installation` 110 / `office relocation services` 170 *(seed)* **[FAQ]** | commercial | → /pages/delivery; /pages/relocation |
| Furnish a small / professional office on a budget *(merges A12, B9, B19)* | `office chairs cheap` 720 / `best budget office chair` 590 **[FAQ]** | commercial | → budget-tier collections; quote |
| Bulk minimums, small quantities & how to negotiate bulk *(merges A4, bonus B: negotiate bulk)* | bulk order minimums *(no direct kw — AEO/topical)* **[FAQ]** | commercial | → quote |
| Educational & corporate discounts / packages / bundles *(merges A28, A34, bonus A: corporate packages)* | `educational/corporate discounts` *(no direct kw — AEO/topical)* **[FAQ]** | commercial | → quote; /pages/education |
| Financing & payment plans *(bonus A)* | office furniture financing *(no direct kw — AEO/topical)* **[FAQ]** | commercial | → quote |
| Warranties & support in Ontario *(merges A20, bonus B)* — buying-guide FAQ, NOT standalone | warranty/support *(no direct kw — AEO/topical)* **[FAQ]** | informational | → quote; warranty section |
| Furniture customization options *(A23)* | customization *(no direct kw — AEO/topical)* | commercial | → buy-canadian; quote |

---

## Production sequence

Validated against the framework + recon. **P1 is the production focus; P3's FAQ hub jumps the queue (Nuance A); P4-geo interleaves with the geo landing-page program (Nuance B).**

1. **Post 1 — DONE (P2 anchor).** OECM/school-boards, LIVE 2026-05-23, BlogPosting + FAQPage emitting.
2. **Blog #2 → open P1 (the whitespace).** Build the **P1 pillar** ("How to Plan an Office Layout") first — it's the uncontested differentiation lane and the design-consultation conversion hub everything else links into.
3. **Blog #3 → P3 PAA/AEO FAQ hub (pulled early).** The ergonomics value-question FAQ + height-adjustable cluster — the dataset's richest PAA / AI-Overview vein. Captures citations while P1 clusters fill in.
4. **Interleave P1 clusters** (focus/quiet zones → Quiet Spaces; meeting/breakout; reception; hybrid/ABW). High-conversion, feeds design-services.
5. **Interleave P4 geo + buying** alongside the **geo landing-page program** — Eastern-Ontario city set + buy-Canadian + quote-process. Ties blog → geo pages → buy-canadian collection.
6. **P3 fills in** — durability, wellness, sustainability (Canadian-made tie).
7. **Continue P2 cornerstones** on cadence — Post 2 (Healthcare/FHT), Post 3 (Cubicle vs Open-Plan for Municipal Offices), then accessibility/sector-comparison clusters.

**Per-post hard rule (CLAUDE.md):** every blog brief starts with a DataForSEO MCP keyword pull (volume/difficulty/related/SERP/PAA) and locks 1 primary + 2–3 secondary keywords before writing. The recon tables above seed that pull — they don't replace it.

---

## DROP list (do NOT build) — with reasons

**Home-office / WFH / individual-consumer** (wrong audience — one-chair home buyers who never convert to a commercial quote):
- A3 Best home-office furniture in Ontario · A7 Choose a desk for WFH · A9 Best ergonomic chairs for home offices · A11 Should my employer pay for home-office equipment · A13 Professional home office on a budget · A14 What furniture to buy first for a home office · A17 Tax deductions for home workers · A19 Best standing desks for home offices *(home framing; standing-desk demand captured commercially in P3)* · A21 How much space for a home office · A25 Storage for home office · A26 Lighting for home office.

**Thin / transactional / dated** (low SEO/AEO value):
- A10 How to assemble furniture · A24 How to return or exchange · A27 How to maintain & clean furniture · A33 Trendy styles for 2026 · A36 Can you rent furniture *(BBI sells)* · B?/bonus COVID-safe furniture *(dated)* · A18 Match styles & colors *(thin decor, no commercial volume)* · warranties-as-standalone *(folded into P4 buying-guide FAQ instead)*.

**Borderline — dropped for no measurable demand** (recon shows ~0 volume in either dataset):
- B39 Smart furniture to manage space *(speculative, no volume)* · bonus B Gender-neutral office spaces · bonus B Intergenerational workforces.

**Context flag (not a drop, but constrained):** used/refurbished geo terms are net-new whitespace but **BBI sells new** — "buy new vs refurbish" survives only as a P3 decision-guide that steers to new; no used-inventory targets.

---

## Internal-linking (D3) — HELD

The pillar ↔ cluster ↔ commercial-page (collection/PDP/landing) link graph implied by every "conversion path" column above is the **D3 internal-linking pass**, which is **HELD until Tier 1 URLs are final** (per build-state). This roadmap *specifies the target* of each link (which collection / landing page / PDP a cluster should point to) so D3 can execute mechanically once URLs lock — but **no links are wired here.**

---

## Summary for build-state

- **Pillar priority CONFIRMED P1>P2>P3>P4**, reframed by data: P1 = biggest *content* whitespace (competitors absent from design/space-planning) + conversion hub; P2 = uncontested OECM moat (≈0 volume, cornerstone cadence); P3 = highest raw AEO/PAA demand (`ergonomics of chair` 14,800 + dense PAA) → its FAQ hub runs early; P4 = net-new geo + buy-Canadian, ties to geo landing pages.
- **~50 cluster topics** mapped across the 4 pillars from 80 Reddit topics + bonuses; **~25 dropped** (home-office/WFH, thin/transactional/dated, no-demand borderline).
- **AEO:** Article schema on all; FAQPage on the ~30 question-format clusters; Post 1's table/`scope`/`<caption>` pattern reused.
- **Sequence:** Post 1 (done) → P1 pillar → P3 AEO FAQ hub (early) → P1 clusters → P4 geo/buy-Canadian (with geo landing pages) → P3 fills → P2 cornerstones (Posts 2 & 3).
