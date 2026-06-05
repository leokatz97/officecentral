# Batch 2 — Segment/Industry Guides & Brand-Dealer Pages: Candidate Menu

**Date:** 2026-06-04
**Status:** DOCS ONLY — research + planning artifact. No drafts, no PACKs, no Shopify writes, no gates, build-state untouched. This is the **menu to choose from**, not a build order.
**Branch:** `feature/batch-2-wave1-pilot-2026-06-04` (PR, not merged) → **HALT for Leo's review.**
**Companion plan:** [batch-2-content-plan-2026-06-04.md](batch-2-content-plan-2026-06-04.md) (covers competitor-teardown / geo / "alternative" systems — this doc adds the two systems that plan did NOT cover: **segment guides** and **brand-dealer pages**.)
**Keyword source:** DataForSEO Labs (keyword_overview + bulk_keyword_difficulty) + live SERP, **location Canada, language en, pulled 2026-06-04** (per CLAUDE.md mandatory blog-creation keyword step).

---

## 0. Executive summary

Two candidate categories, grounded in what BBI **actually serves and carries** (live-nav verified):

- **Category A — Industry/segment guides.** Honest finding: in Canada, segment-qualified terms (`[segment] office furniture`) are **near-zero volume** (most 10–30/mo; many return no DataForSEO data at all). The volume that exists sits in **broad category terms** (`school furniture` 210, `library furniture` 170, `classroom furniture` 210) that are **NOT BBI's product fit** — BBI furnishes school-board *offices/admin*, not classrooms or library stacks. So Category A is a **low-volume, high-CPC, high-conversion, qualified-intent** play, and most of its value is realised by **enriching the 5 Industries landing pages that already exist** rather than spinning up parallel blog posts. Only 2 genuinely net-new sub-vertical guides clear the bar (law firms, private medical/dental clinics).

- **Category B — Brand-dealer pages.** This is where the real volume is. BBI's carried brands have **strong brand-term search** (ergoCentric 2,900 / Keilhauer 1,900 / Global 2,900 / Humanscale 2,900 / Teknion 6,600), most at **low KD (3–14)**. Brand terms skew **navigational** (searcher wants the maker's own site) — BBI's job is to capture the **dealer / "where to buy" / product-transactional modifier** intent as an authorized Canadian dealer. Nominative use of a brand BBI genuinely carries is **legitimate referential use — Tier-1 safe, not the adversarial competitor situation.** The single highest-ROI move: **enrich the two live-but-empty brand pages (Keilhauer KD3, ergoCentric KD8)** and **build the missing OTG page** (highest catalog depth, no page today).

**Cross-cutting de-confliction (critical):** both categories collide with assets that already exist.
- Category A maps 1:1 onto the **live Industries landing pages** (`/pages/healthcare`, `/education`, `/government`, `/non-profit`, `/professional-services`, `/industries`) → **enrich, don't duplicate.**
- Category A also overlaps the **BPS Track-A post (Slot 4)** (cross-vertical public-sector furnishing) and the **OECM school-boards cornerstone** → any public-sector segment must merge/drop or carve a private-sector angle; any "schools" candidate must be FURNITURE-for-school-offices, distinct from procurement mechanics.
- Category B collides with the **live brand landing pages** (`/pages/brands-*`) and the existing **BRAND-PAGES-1 handoff plan** ([bbi-brand-pages-1-handoff-2026-05-20.md](bbi-brand-pages-1-handoff-2026-05-20.md)) → this menu **feeds that plan**, prioritized by brand-term volume; it is not a parallel content track.
- Both collide (lightly) with the **Manufacturers guide** (Wave 1 Page 1) and **Supplier roundup** (Wave 1 Page 5), which already *name* the brands — but those are multi-brand *landscape* pages; a single-brand dealer page is distinct single-brand transactional intent. Cross-link, don't overlap.

---

## 1. Grounding — what BBI actually serves / carries (verified 2026-06-04)

### 1a. Industries served (live nav → Industries dropdown)
Healthcare · Education · Government · Non-Profit · Professional Services (+ Industries Hub). **Each already has a dedicated theme landing page** (P1-6…P1-10 in CLAUDE.md). No other verticals are presented publicly.

### 1b. Brands carried (live nav → Brands dropdown)
Global / Teknion · OTG / Offices to Go · Heartwood Manufacturing · ObusForme · ergoCentric · Keilhauer · ("Authorized Canadian Dealer" trust line).

### 1c. Carrier-status verification per brand (the false-claim gate)
Cross-checked against [manufacturer-defaults.yaml](../../data/reference/manufacturer-defaults.yaml), [brand-collection-routing.yaml](../../data/reference/brand-collection-routing.yaml), [brand-page-inventory-2026-05-12.md](../../data/reports/brand-page-inventory-2026-05-12.md), and products cited in the Wave-1 manufacturers/geo drafts.

| Brand | Carrier status | Evidence | Brand-page candidate? |
|---|---|---|---|
| **Global Furniture Group** | ✅ Confirmed | 53–56 products, healthy `global-teknion` collection; cited throughout Wave 1 | YES (strong) |
| **Offices to Go (OTG)** | ✅ Confirmed | 54 enriched products (highest in catalog); cited Wave 1 | YES (strong) — **no page yet** |
| **ObusForme** | ✅ Confirmed | 5 products; Global sub-brand; in nav | YES (caveat: consumer-skew) |
| **ergoCentric** | ✅ Confirmed | Live brand page (empty collection); Part-Time chair cited Wave 1; Mississauga maker | YES (strong) — enrich live page |
| **Keilhauer** | ✅ Confirmed | Live brand page (empty collection); named Canadian maker Wave 1 | YES (strong) — enrich live page |
| **Heartwood Mfg** | ✅ Confirmed | 17 products; tables specialist; in nav | YES (niche) |
| **Teknion** | ⚠️ Presented, thin | In nav (bundled "Global / Teknion") but **0 enriched products** | CAUTION — needs real product depth before a dealer page |
| **Humanscale** | ✅ Confirmed (catalog) | Products (eFloat, Nova) + manufacturer dict; **not in brand nav** | YES (secondary/premium) |
| **Safco** | ✅ Confirmed (catalog) | Products (Ranger/Vista/AlphaBetter); **not in brand nav** | Optional (secondary) |
| **FireKing** | ✅ Confirmed (catalog) | CF7236-D fire cabinet etc.; cited Ottawa geo; **not in brand nav** | Optional (niche/security) |
| **Office Star** | ✅ Confirmed (catalog) | Napa boardroom table cited Toronto geo; **not in brand nav** | Optional (secondary) |
| **Allseating** | ❌ **Unconfirmed** | Stub in routing yaml, **0 enriched products**; named only as a landscape maker | **VERIFY before any page** — false-dealer-claim risk |
| HON / Herman Miller / Steelcase / Haworth | ❌ Not carried | Dictionary stubs only / named as market landscape | **DROP** — dealer page would be a false claim |

> **Discipline:** a "[brand] dealer" page for a brand BBI does not carry is a false claim — same gate as the competitor-verification discipline. Allseating (despite a tempting 1,000/mo KD8) is **blocked pending carrier confirmation**; the not-carried US majors are dropped outright.

---

## CATEGORY A — Industry / Segment Guides

### A1. Ranked candidate table (Canada volumes, 2026-06-04)

| Proposed title | Primary keyword | Vol | KD | Intent | BBI serves? (verified) | De-confliction note | Priority |
|---|---|---|---|---|---|---|---|
| Law Firm & Legal Office Furniture in Ontario | law office furniture | 10 | n/a (low) | commercial | ✅ Pro-Services buyer; net-new sub-vertical | Sub-page under live `/professional-services`; NOT public-sector (distinct from Slot 4 BPS). Net-new. | **1** |
| Medical & Dental Clinic Furniture (Private Practices), Ontario | medical office furniture | 30 | 42 | transactional (rising +100% q) | ✅ Healthcare served | **Enrich/extend** live `/healthcare`; lead **private clinics** (healthcare-tone memo); distinct from institutional Slot 4. Competitive SERP (Source/POI/Distrimar/Steelcase). | **1–2** |
| Enrich the 5 live Industries pages for AEO + long-tail | (industry hub long-tail) | — | — | commercial/info | ✅ all five served | **MERGE, not new content.** Highest-ROI: turn thin landing pages into real, cited, FAQ-schema guides. Each links to Slot 4 / OECM / relevant collections. | **2** |
| Call & Contact Centre Furniture (Ontario) | call center furniture | 10 | n/a (low) | commercial (CPC $9.42) | ✅ corporate buyer; net-new | Net-new niche; bulk task-seating conversion. Link to seating collections + Slot 5 grade. | **3** |
| Corporate / HQ Office Furniture | corporate office furniture | 20 | 45 | navigational | ✅ served | Thin + nav + KD45; overlaps geo/commercial guides. Fold as a section, not a page. | **3 (fold)** |
| Office Furniture for Startups / Tech Offices | office furniture for startups | 10 | low | navigational | ✅ served | Near-zero, nav; trend-adjacent to design-trends capstone. Defer. | **3 (defer)** |
| School / Classroom / Library furniture | school furniture / library furniture | 210 / 170 | 26 / 1 | transactional | ❌ **Not BBI's product fit** | **DROP.** These are classroom desks / library stacks — BBI furnishes school-board *offices/admin*. OECM cornerstone owns school-board procurement. Chasing this would over-claim. | **DROP** |
| Government / Municipal office furniture | government office furniture | 10 | low | navigational | ✅ but owned | **MERGE into Slot 4 + live `/government`.** No net-new page. | **DROP/merge** |
| Non-Profit office furniture | non profit office furniture | — (no data) | — | — | ✅ but owned | **MERGE into Slot 4 + live `/non-profit`.** | **DROP/merge** |
| Hospitality / Veterinary furniture | hospitality furniture / veterinary furniture | 50 / 10 | low | commercial | ❌ not served (BBI = office, not hospitality FF&E / vet) | **DROP** — outside BBI's offering; over-claim risk. | **DROP** |

**SERP/PAA confirmation (top buyer query, `medical office furniture`, Canada):** real commercial SERP — Source `/industry/healthcare`, POI `/environments/healthcare`, Distrimar, Steelcase Health, Herman Miller Clinical, healthcarefurniture.net, plus a "popular products" shelf. Related searches: *medical office furniture canada · medical office furniture brands · best medical office furniture · healthcare furniture manufacturers*. → A real buyer query, but a **competitive SERP dominated by US giants + product listings**; BBI wins on Ontario specificity + real PDPs + private-clinic angle, not on volume. Confirms industry/segment pages are a proven competitor pattern (both Source and POI run them).

### A2. Recommendation — build first (Category A)
Volume is thin across the board, so weight **commercial/CPC intent + conversion to quote/consult + genuine net-new fit** over raw volume.

1. **Enrich the 5 existing Industries landing pages first (Priority 2 above, but do it first).** This is the highest-ROI Category-A move and avoids cannibalization entirely — the pages already rank-eligible URLs, they're just thin. Add cited substance, FAQ schema, real PDPs, and links down to Slot 4 / OECM / collections.
2. **Law Firm & Legal Office Furniture in Ontario** — the strongest *net-new* candidate: high CPC ($6.14), commercial intent, high-value fit-out conversion, and it's a genuine private sub-vertical not owned by any existing asset (sits under Professional Services, distinct from public-sector Slot 4).
3. **Medical & Dental Clinic Furniture (private practices)** — rising transactional term, proven competitor pattern, high CPC; build as a deep private-clinic extension that the `/healthcare` page links to (lead private per the healthcare-tone memo).
4. *(Optional)* **Call/Contact Centre Furniture** — niche but high-CPC, bulk-seating conversion.

**Merge or drop:** government, municipal, non-profit → **merge** into Slot 4 + their live landing pages. School/classroom/library, hospitality, veterinary → **drop** (not BBI's product fit; over-claim risk). Corporate/startup/tech → **fold** as sections of geo/commercial guides, not standalone pages.

---

## CATEGORY B — Brand-Dealer Pages

> **Tier-1 safety:** nominative ("authorized dealer of X") use of a brand BBI genuinely carries is legitimate, expected referential use — **NOT** the adversarial competitor situation. The only gate is **carrier verification** (§1c). Brand terms skew **navigational** — flagged per row below; BBI captures the *dealer / "where to buy" / product-transactional* slice, not the bare brand SERP (the maker's own site owns that).

### B1. Ranked candidate table (Canada volumes, 2026-06-04)

| Proposed title | Primary keyword | Vol | KD | Intent | BBI carries? (verified) | De-confliction note | Priority |
|---|---|---|---|---|---|---|---|
| ergoCentric Chairs — Authorized Canadian Dealer | ergocentric (2,900) / **ergocentric chairs** | 2,900 / 1,000 | 8 / 9 | nav / **transactional** | ✅ Confirmed (live empty page) | **Enrich live** `/pages/brands-ergocentric`. Capture transactional "ergocentric chairs". Ontario maker → 🍁 angle (Steve-gated). | **1** |
| Keilhauer — Authorized Canadian Dealer (Ontario) | keilhauer (1,900) / **keilhauer chairs** | 1,900 / 170 | 3 / mid | nav / **transactional** | ✅ Confirmed (live empty page) | **Enrich live** `/pages/brands-keilhauer`. **KD3 = easiest brand win.** | **1** |
| Global Furniture Group — Dealer & Full Catalog | global furniture group / **global office furniture** | 2,900 / 320 | 11 / 9 | navigational | ✅ Confirmed (56-product collection) | Enrich/split the bundled `brands-global-teknion`; highest catalog depth (real product grid). | **1–2** |
| Offices to Go (OTG) — Dealer & Catalog | offices to go | 260 | 14 | nav | ✅ Confirmed (54 products, **no page**) | **Build new** per BRAND-PAGES-1. Lower brand-vol but biggest catalog/conversion gap (highest-volume carried brand with zero storefront presence). | **2** |
| ObusForme Seating — Where to Buy in Canada | obusforme / **obusforme chair** | 2,400 / 170 | low | informational / transactional | ✅ Confirmed (5 products, in nav, no page) | Build new; **caveat: ObusForme skews consumer back-support / informational** — confirm B2B fit before investing. | **2–3** |
| Humanscale — Authorized Dealer (Ontario) | humanscale / **humanscale chair** | 2,900 / 720 | mid | informational / transactional | ✅ Confirmed (catalog) — **not in brand nav** | High premium conversion, but not a featured brand today. Flag: decide whether to elevate to nav first. | **3** |
| FireKing Fire-Rated Cabinets — Canadian Dealer | fireking / fireking file cabinet | 590 / 40 | 10 / 15 | info / transactional | ✅ Confirmed (catalog) — not in nav | Niche but distinct (security/records); ties to Ottawa/government geo + secure-storage angle. | **3** |
| Safco Products — Canadian Dealer | safco / safco products | 320 / 50 | 11 / 24 | info / nav | ✅ Confirmed (catalog) — not in nav | Secondary/optional; accessory-skew (drafting, risers). | **Optional** |
| Office Star — Canadian Dealer | office star products | 170 | 4 | navigational | ✅ Confirmed (catalog) — not in nav | KD4 winnable but low vol + accessory-skew. Optional. | **Optional** |
| Heartwood Manufacturing — Tables & Casegoods | heartwood furniture | 110 | low | navigational | ✅ Confirmed (17 products, in nav, no page) | Build new (BRAND-PAGES-1); niche tables/boardroom specialist; genuine differentiator copy. | **3** |
| Teknion — Dealer | teknion (6,600) / teknion furniture | 6,600 / 480 | 41 / 16 | informational / nav | ⚠️ Presented in nav, **0 products** | **CAUTION/HOLD.** Highest brand vol but KD41 + no catalog depth → a dealer page now risks thin/false-depth. Build only with real Teknion product depth. | **HOLD** |
| Allseating — Dealer | allseating | 1,000 | 8 | navigational | ❌ **Unconfirmed carrier** | **BLOCKED pending verification.** Tempting (1,000/KD8) but stub-only, 0 products. Confirm dealer status before any page. | **VERIFY** |
| HON / Herman Miller / Steelcase / Haworth | (brand terms) | high | mixed | nav | ❌ Not carried | **DROP** — dealer page = false claim. | **DROP** |

**Navigational caveat (applies to all brand rows):** every bare-brand term resolves **navigational/informational** (the searcher wants the manufacturer). The winnable, conversion-bearing slices are the **product-transactional** modifiers — `ergocentric chairs` (1,000, transactional), `keilhauer chairs` (170, transactional), `humanscale chair` (720, transactional), `obusforme chair` (170, transactional), `global office chairs` (110) — plus **"[brand] dealer / where to buy [brand] / [brand] Ontario"** long-tails. Target those as H2/secondary, not the bare brand head.

### B2. Recommendation — build first (Category B)
Weight **carried + winnable KD + a transactional modifier that converts** over bare-brand navigational volume.

1. **Keilhauer** (KD3) and **ergoCentric** (KD8, transactional "ergocentric chairs" 1,000) — **enrich the two live-but-empty brand pages first.** Lowest KD, real transactional intent, infrastructure already exists (just thin), and ergoCentric/Keilhauer are Canadian (Ontario) makers → on-brand 🍁 + OECM trust story. Fastest wins in the entire menu.
2. **Global Furniture Group** — enrich/split the bundled page; it has the deepest real catalog (56 products) so the product grid is genuine, and `global office furniture` (320/KD9) is winnable.
3. **Offices to Go (OTG)** — **build the missing page** (BRAND-PAGES-1 already scoped it). Brand-term volume is modest (260) but it's the highest-depth carried brand with **zero** storefront presence — pure upside, strong conversion.
4. *(Then)* ObusForme + Heartwood as the remaining nav brands (build new), and Humanscale/FireKing as secondary premium/niche pages **if** BBI wants to elevate them into the brand nav.

**Hold / verify / drop:** **Teknion HOLD** (huge volume, but 0 products + KD41 → don't ship a thin dealer page; revisit when Teknion SKUs are enriched). **Allseating VERIFY** carrier status before anything. **HON/Herman Miller/Steelcase/Haworth DROP** (not carried → false claim).

**Build vehicle:** Category B should run **through the BRAND-PAGES-1 plan** ([bbi-brand-pages-1-handoff-2026-05-20.md](bbi-brand-pages-1-handoff-2026-05-20.md)) — enrich existing `ds-lp-brands-*` sections / build new ones — **not** as parallel blog posts that would cannibalize the brand landing pages. The Manufacturers guide (Wave 1 Page 1) and Supplier roundup (Wave 1 Page 5) already name these brands at the *landscape* level; single-brand dealer pages are distinct single-brand transactional intent — cross-link, don't overlap.

---

## 2. Guardrails carried forward (both categories)
- **Carrier/serve verification is the hard gate** — no segment page for a vertical BBI doesn't serve; no brand page for a brand BBI doesn't carry (§1c). Allseating blocked; not-carried majors dropped.
- **Claims discipline (Batch-1/Wave-1):** no product Made-in-Canada / maple-leaf except Steve-gated verified lines; warranty qualitative; certs (BIFMA/CSA/GREENGUARD) from the verified-spec set; OECM wording verbatim; no BBI financing claim; Ontario-wide delivery.
- **De-confliction is step 1:** enrich existing Industries + brand landing pages rather than duplicate; merge public-sector segments into Slot 4 + cornerstone; route Category B through BRAND-PAGES-1.
- **Author:** Steve Katz. **North Star:** qualified Ontario/Canadian business + institutional buyers → quote or design consult. Never publish "BBI" to customers (full "Brant Business Interiors").
- **Re-pull DataForSEO at build time** (volumes drift; this research seeds the brief, doesn't replace the per-post pull — CLAUDE.md rule).

---

*End of menu. No content written, nothing published, build-state untouched. HALT for Leo's review — this is the candidate list to choose from, not a build order.*
