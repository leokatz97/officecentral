# BBI Per-Page Keyword Map — ICP-KEYWORD-WALKTHROUGH

**Date:** 2026-05-31
**Source recon:** COMPETITOR-KEYWORD-RECON-1 + SEED-EXPANSION (PR #66, run 2026-05-30)
**Method:** Interactive ICP walkthrough — clusters routed to ICP A (institutional/non-profit), ICP B (SMB private-sector), or Both, then mapped to a page surface, CTA mode, and voice tilt. Persisted after each cluster lock.

> **Scope filter (applied to every cluster before trusting recon counts):** strip foreign-geo (London/Melbourne/Dubai/etc.), software/calculator/textbook-PDF/cost-research queries, and home-office terms. BBI serves Ontario + Western Canada (BC/AB/SK/MB), institutional + SMB, B2B only. Quebec excluded. The seed-expansion net-new counts are inflated ~2–2.5× before this filter.

> **Co-primary ICP reminder:** institutional and SMB are equal-weight (locked in `icp.md`). Clusters route by the product/intent the keyword implies; shared clusters split via dual-CTA + secondary-use line, not by keyword.

---

## Hub-and-spoke structure

- **Design Services** is the **hub** (cluster 1). It cross-links to industry pages via vertical design queries.
- **Professional Services** and **Healthcare** are **spokes** — each receives a design cross-link from the hub and links back.

---

## Cluster 1 — Design Services (HUB) · Both ICPs · LOCKED

| Field | Value |
|---|---|
| **Primary KW** | `office space planning` |
| **Secondaries** | `space planning office`, `space planning for office`, `office layout planning`, `workspace planning`, `office design services`, `office interior design services`, `office space planning services / consultants / companies`, `office reconfiguration` |
| **Opportunistic grab** | `office floor plan` (260/mo, KD 10 — bigger than the whole net-new core, weakly held by theofficeshop.ca) → add a floor-plan/layout section |
| **Vertical cross-links** | `medical office space planning` + `dental office design services` → **Healthcare** page · `financial services office design` → **Professional Services** page |
| **FAQ/blog pillar** | `what is office space planning`, `…standards`, `…guidelines`, `…checklist`, `…considerations` (AI-Overview fuel, supports the money page) |
| **Surface / CTA** | Service page; `Get My Free Layout →` → `#design-form` (locked microcopy); design-consultation → quote channel |
| **Meta suffix** | `\| Brant Business Interiors — a division of Office Central Inc. (OECM Supplier)` |
| **Slug** | `/pages/office-space-planning` (recommend) |
| **Strategic note** | Low volume (~400/mo core), near-zero competition, high-intent — this is the **hub** that the industry pages spoke off. Leverage = differentiation + quote funnel, not traffic. |

**Recon filter result (cluster 1):** raw 127 net-new / 1,480/mo → addressable 54 kw / 750/mo → conversion core ~15 kw / ~400/mo. Dropped: 24 foreign-geo (240/mo), 46 software/info/cost (460/mo), 3 home-office (30/mo).

---

## Cluster 2 — Professional Services (SPOKE) · ICP B · LOCKED

**Structural finding:** Professional Services has **no high-volume vertical head term** — `law office furniture` / `accounting office furniture` etc. all sit ~10/mo. The real volume lives in generic product terms (`reception desk` 2,900, `executive desk` 1,300, `boardroom table` 880) that belong on **collection pages, not this industry page**. So PS is a **thin-volume vertical landing page — conversion > traffic**: it owns the vertical long-tail, receives the design-hub spoke, and **funnels** to the fat product collections.

| Field | Value |
|---|---|
| **Primary KW** | `law firm office furniture` |
| **Vertical secondaries** | `law office furniture`, `accounting office furniture`, `insurance office furniture`, `financial services office design`, `consulting office furniture` |
| **Design-spoke (from hub)** | `financial services office design` → links back to Design Services hub |
| **Funnels to (fat collections — Both-ICP, volume NOT claimed by this page)** | Executive Desks (`executive desk` 1,300) · Boardroom (`boardroom table` 880, `conference table` 720, `wood boardroom table` 260) · Reception (`reception desk` 2,900) · Executive Seating (`executive office chair` 880, `boardroom chairs` 210) |
| **Surface / CTA** | Industry page; quote-led for fit-outs + cart for single items; ICP B aesthetic / client-facing voice tilt |
| **Excludes** | Dental + medical → routed to Healthcare (see decision below) |
| **Meta suffix** | `\| Brant Business Interiors — a division of Office Central Inc. (OECM Supplier)` |
| **Slug** | `/pages/professional-services` (page already exists — `ds-lp-professional-services`; this informs meta/copy) |
| **Strategic note** | Real revenue (ICP B law/accounting/insurance/consulting ≈ $42k / 13% of named revenue) but buyers search generically by product. Page value = conversion + funnel, not head-term traffic. |

### Decision — Dental categorization: **Dental → Healthcare** (not Professional Services)

1. **Environment > business-type as the routing axis.** Dental is a clinical patient-care space (waiting room, treatment/operatory, infection-control). Furniture needs mirror medical, not the executive-desk/boardroom set that defines law/accounting/financial.
2. **Search adjacency.** `dental office furniture` co-occurs with `medical office furniture` / `…waiting room furniture` — same intent, same SERP neighborhood. A dental buyer wants waiting-room seating, not a boardroom table.
3. **Consistency.** Cluster 1 already routed `dental office design services` → Healthcare; keeping dental product + design together avoids a split-brain.
4. **Keeps both pages clean.** PS stays "client-facing professional office"; Healthcare absorbs all clinical practices (medical + dental) under one private-clinic-first tone.
- **Shared touchpoint:** reception desks. Both pages cross-link to the Reception collection (`law office reception desk` → PS; `dental office reception desk` → Healthcare). No conflict.

### Flagged for a later cluster — Product collections (Both-ICP, fat volume)

`reception desk` (2,900) · `executive desk` (1,300) · `boardroom table` (880) · `conference table` (720) · `executive office chair` (880) · `l-shaped reception desk` (320) · `executive desk canada` (210) — all KD 0 easy, `product_generic`. These map to **collection pages** and serve BOTH ICPs. Map as a dedicated cluster after the industry spokes.

---

## Cluster 3 — Healthcare (SPOKE) · ICP A/B straddle · LOCKED

**Structural finding:** Unlike Professional Services, Healthcare **owns winnable vertical head terms** AND a healthcare-specific product spine — ~470/mo of real, easy volume. It's the genuine A/B straddle: serves ICP A (small hospitals, Family Health Teams) *and* ICP B (private medical/dental practices). Per the locked tone rule, **page copy leads private-clinic-first**; OECM/institutional is a trust signal underneath, not the hero frame.

| Field | Value |
|---|---|
| **Primary KW** | `healthcare furniture canada` |
| **Vertical head secondaries** | `healthcare furniture`, `furniture healthcare` (90 each, easy) · `medical furnitures` (50) · `healthcare furniture manufacturers canada` (10) |
| **Product spine (healthcare-specific, → collection within page)** | `office chairs for waiting room` (140) · `waiting room chairs canada` (70) |
| **Medical long-tail (NEW-product intent, keep)** | `medical office furniture` (30), `furniture for medical office` (30), `medical office furniture waiting room / exam room / reception` (10s) |
| **Dental sub-family (routed here, not PS)** | `dental office furniture`, `dental office waiting room furniture`, `dental office reception furniture`, `dental office reception desk` (10 each) |
| **Design-spokes (from hub)** | `medical office space planning` + `dental office design services` → link back to Design Services hub |
| **Cross-links to** | Reception collection (`medical/dental office reception desk`) · Waiting-room seating collection |
| **Surface / CTA** | Industry page; quote-led (clinical fit-outs) + cart for single items; **private-clinic-first voice**, OECM as trust signal |
| **Meta suffix** | `\| Brant Business Interiors — a division of Office Central Inc. (OECM Supplier)` |
| **Slug** | `/pages/healthcare` (page already exists — `ds-lp-healthcare`; this informs meta/copy) |

### Filters applied (cluster 3)

- **DROP — "used/liquidation/auction" intent (~8 terms):** `used medical office furniture`, `…liquidators`, `…auction`, `…for sale near me`. BBI sells new commercial product; these are bargain-hunter intent.
- **DROP — navigational/news:** `new sickkids hospital`, `sickkids new hospital` (70 each) — poi.ca ranks accidentally; not product intent.

**Recon filter result (cluster 3):** competitor-ranked 7 kw + seed net-new 37 kw (430/mo) → addressable ~470/mo (vertical head ~260 + product spine ~210 + new-product medical/dental long-tail), after dropping used-intent + sickkids news.

### Dental routing — see Cluster 2 decision (Dental → Healthcare, full rationale documented there).

---

## Session progress

| # | Cluster | ICP | Role | Primary KW | Status |
|---|---|---|---|---|---|
| 1 | Design Services | Both | **Hub** | `office space planning` | ✅ LOCKED |
| 2 | Professional Services | B | Spoke | `law firm office furniture` | ✅ LOCKED |
| 3 | Healthcare | A/B straddle | Spoke | `healthcare furniture canada` | ✅ LOCKED |

**Remaining clusters (not yet mapped):**
- Product collections (Both) — Executive Desks / Boardroom / Reception / Executive Seating + Waiting-room seating. Fat generic volume (reception desk 2,900, executive desk 1,300). The industry spokes funnel here.
- Education + library (ICP A) — quick-win vertical whitespace.
- Eastern-Ontario geo (Both) — geo whitespace + OECM overlay.
- Brand-dealer pages (Both) — 39 net-new home-turf brand terms.
- Ergonomic task seating / desks / storage (Both) — shared, split by CTA.

---

## Cluster 4 — Product Collections (FUNNEL TARGETS) · Both ICPs · LOCKED

**Closes the funnel loop:** the Professional Services and Healthcare spokes point here for generic product volume. Four collection pages, all `ecom-purchase` primary (cart-led), with `canada`-qualified + bulk variants triggering dual-CTA (quote for fleets). All serve **both** ICPs — institutional buyers buy boardroom tables and reception desks too.

> **Near-duplicate caution (extends the scope-filter discipline):** head terms appear as multiple near-identical strings at the same volume (`reception desk` / `reception desks` / `reception desk reception` all 2,900/mo = one SERP, not three). Do **not** naively sum — count the head once + distinct modifiers.

### 4a — Reception (collection)
| Field | Value |
|---|---|
| **Primary KW** | `reception desk` / `reception desks` (~2,900/mo, easy) |
| **Modifiers** | `l-shaped reception desk` (320), `reception desk canada` (260, quote), `small reception desk` (210), `modern reception desk` (170), `reception desk for sale` (170) |
| **Funnel-from** | Professional Services (`law office reception desk`) + Healthcare (`medical/dental office reception desk`) |
| **Surface / CTA** | collection_page; cart-led, quote for `canada`/bulk |
| **Slug** | `/collections/reception-desks` |

### 4b — Executive Desks (collection)
| Field | Value |
|---|---|
| **Primary KW** | `executive desk` (1,300/mo, easy) |
| **Modifiers** | `executive office desk` (320), `l-shaped executive desk` (260), `executive desk canada` (210, quote), `modern/wood executive desk` (110/70) |
| **Funnel-from** | Professional Services |
| **DROP** | `home office executive desks`, `executive desk for home office` (110 each) — excluded home-office ICP |
| **Re-route** | `executive desk chair leather` / `leather executive desk chair` (140 each) → Executive Seating, not here |
| **Surface / CTA** | collection_page; cart-led, quote for `canada`/bulk |
| **Slug** | `/collections/executive-desks` |

### 4c — Boardroom (collection)
| Field | Value |
|---|---|
| **Primary KW** | `boardroom table` / `boardroom tables` (880/mo) + `conference table` (720/mo) |
| **Modifiers** | `wood/wooden boardroom table` (260), `conference table canada` (90, quote), `modular conference/boardroom table` (70), `conference table with chairs` (90) |
| **Funnel-from** | Professional Services |
| **Re-route** | `boardroom chairs` (210), `conference table chairs` (90) → Executive/Conference Seating |
| **Surface / CTA** | collection_page; **quote-led** (boardroom = project fit-out) + cart for single tables |
| **Slug** | `/collections/boardroom-conference-tables` |

### 4d — Waiting-Room Seating (collection)
| Field | Value |
|---|---|
| **Primary KW** | `office chairs for waiting room` (140/mo, easy) |
| **Modifiers** | `waiting room chairs canada` (70, quote) |
| **Funnel-from** | Healthcare (`medical/dental office waiting room furniture` net-new long-tail lands here) |
| **Surface / CTA** | collection_page; cart-led, quote for bulk/clinical fit-out |
| **Slug** | `/collections/waiting-room-seating` |

**Recon filter result (cluster 4):** Reception ~2,900 head + modifiers (~5k distinct) · Executive Desks 1,300 head (after dropping 2 home-office + re-routing 2 chair terms) · Boardroom 880+720 heads · Waiting-room 140+70. All KD 0 easy; the fat winnable volume in the whole map.

---

## Operational lessons (for build-state propagation)

**LESSON: SCOPE-FILTER-MATTERS-MORE-THAN-RAW-RECON-COUNTS**
Raw recon / seed-expansion net-new counts are inflated **2–2.5×** before the BBI scope filter. Every cluster shed foreign-geo (London/Melbourne/Dubai), software/calculator/PDF research queries, used/liquidation/auction intent (BBI sells new), and home-office terms (excluded ICP) — plus same-SERP near-duplicate head terms that must not be summed. **Always filter to scope before trusting a volume number or prioritizing a cluster.** The headline "127 net-new / 1,480/mo" for Design became a real ~400/mo core.

**LESSON: HUB-AND-SPOKE-VALIDATES-AS-ARCHITECTURE**
The site architecture that fell out of the data: **service pages = topic hubs** (Design Services owns space-planning intent and cross-links outward), **industry pages = spokes** (Professional Services, Healthcare — thin vertical long-tail, conversion > traffic, voiced per ICP), **collection pages = funnel targets** (Reception, Executive Desks, Boardroom, Waiting-room — own the fat generic product volume the spokes can't). Spokes funnel into shared collections rather than trying to own head terms themselves. This validated across all 4 clusters and should govern future page builds.

---

## Final status — walkthrough session 1 complete

| # | Cluster | ICP | Role | Primary KW | Status |
|---|---|---|---|---|---|
| 1 | Design Services | Both | Hub | `office space planning` | ✅ LOCKED |
| 2 | Professional Services | B | Spoke | `law firm office furniture` | ✅ LOCKED |
| 3 | Healthcare | A/B | Spoke | `healthcare furniture canada` | ✅ LOCKED |
| 4 | Product Collections (×4) | Both | Funnel targets | reception / executive desk / boardroom / waiting-room | ✅ LOCKED |

**Deferred to walkthrough session 2 (this week):** Education + library (ICP A) · Eastern-Ontario geo (Both) · Brand-dealer pages (Both) · Ergonomic seating / desks / storage (Both).

Structured partial-lock for Session 5+ Phase 0: [`data/reference/priority-keywords.yaml`](../../data/reference/priority-keywords.yaml) (v1).
