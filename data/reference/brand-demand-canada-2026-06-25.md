# Carried-Brand Demand — Canada (Phase 1 research)

**Date:** 2026-06-25 · **Branch:** `research/phase1-competitor-brand-demand-2026-06-25` · **READ-ONLY research. No theme, no Shopify writes, no published flags.**

**Data source:** **DataForSEO** (Labs `keyword_suggestions` for brand-term volumes/intent + SERP `organic/live/advanced` with `people_also_ask_click_depth=2` for PAA, reused via `scripts/dfs_client.py`; key never printed). **Not** the live-SERP fallback.
**Market:** location = **Canada** (location_code 2124), language = **en**. (Country-level; Ontario-level not supported on these endpoints — Canada is the correct superset for an Ontario dealer.)
**Raw pulls:** `data/research/phase1-raw/sugg__*.json` + `paa__*.json`. **BBI position** for every brand term below = **absent** (BBI ranks for no carried-brand head in the Canada top-20 — confirmed against `ranked__brantbusinessinteriors_com.json`; its only brand-ish ranking is `teknion ls` p15, a product-spec long-tail, not a brand head).

**Live BBI brand pages cross-checked** (`theme/sections/ds-lp-brands-*.liquid`): **exist** = ergoCentric, Global+Teknion (one combined page), Heartwood, Keilhauer, ObusForme, OTG. **none** = Humanscale, Safco, FireKing, Office Star.

**Carrier gate (locked):** actionable set = Global, OTG, Teknion, Humanscale, Keilhauer, ergoCentric, Heartwood, ObusForme, Safco, FireKing, Office Star. The reference set (Herman Miller, Steelcase, Haworth, Nightingale) is **NOT carried** and is quarantined in its own section below. The carried list is the carrier gate — not expanded here.

**AI-Overview signal:** brand-*name* queries did **not** trigger AI Overview for any brand (consistent with Track C's finding that AIO fires on *comparison/alternative* queries — which the live comparison posts + Track C already target — not on brand-nav). The brand-page AEO play is therefore **PAA capture** (the recurring "is it Canadian / where made / is it good quality / how long does it last" questions below), not AIO.

---

## ACTIONABLE SET — carried brands (BBI is the dealer = structural advantage)

Top brand + brand-intent terms by Canada volume (top of each pull; full 15 in the parser log). Intent: nav = navigational, txn = transactional, info = informational, comm = commercial. BBI position = **absent** for all unless noted.

### Teknion — page: EXISTS (combined with Global) · **thin for Teknion** · demand: HIGH
- `teknion` 6,600 (info) · `teknion furniture systems` 720 · `teknion furniture` 480 · `contessa teknion` 260 (chair) · plus many corporate-nav variants (llc/ltd/oneplace).
- **PAA:** *Is Teknion a good brand? · Is Teknion a Canadian company? · Who owns Teknion furniture? · Where is Teknion furniture manufactured?*
- **Verdict:** highest brand volume in the carried set, but the live page is **shared with Global** (thin for Teknion specifically) and BBI ranks absent. **Deepen — or split Teknion into its own brand page.** Strong dealer advantage; PAA is "is it Canadian / who owns / where made" — ideal FAQ/AEO block.

### ergoCentric — page: EXISTS · not ranking (absent) · demand: HIGH (Ontario-made)
- `ergocentric` 2,900 (info) · `ergocentric chair(s)` 1,000 · `ergocentric seating systems` 590 · `ergocentric store/canada` 590 · `ergocentric toronto` 170 · `ergocentric office chair(s)` 170 · `ergocentric aircentric / tcentric` 90.
- **PAA:** *Are ergoCentric chairs good for long hours of sitting? · What ergoCentric chair is best for back pain? · Does an ergonomic chair really work? · Are ergo chairs worth it?*
- **Verdict:** strong, very on-brand (Ontario manufacturer, BBI dealer, OECM-adjacent). Page exists but earns no top-20 rank → **deepen + optimize.** PAA maps cleanly to `/pages/ergonomic-office-chairs` cross-link (do NOT target ergonomic-chair heads here — those are LOCKED to that page; target the **brand** terms `ergocentric chair / ergocentric office chair / ergocentric canada`).

### Keilhauer — page: EXISTS · not ranking (absent) · demand: MED-HIGH (design-led, Canadian)
- `keilhauer` / `keilhauer canada` 1,900 (info) · `keilhauer furniture` 210 · `keilhauer chair(s)` 170 · `keilhauer office chair(s)` 90 · model tails (`ponder` `cahoots` `pact` `juxta`) 20–40.
- **PAA:** *Is Keilhauer furniture good quality? · Where is Keilhauer furniture made/manufactured? · How much is the Keilhauer Ponder chair? · Who makes the best furniture in Canada?*
- **Verdict:** real branded demand, page exists but absent in rank → **deepen.** "Where is it made / is it good quality / best furniture in Canada" PAA is a natural Canadian-made + dealer-trust FAQ block.

### Humanscale — page: **NONE** · demand: HIGH · **highest structural gap**
- `humanscale` 2,900 (info) · `humanscale chair(s)` 720 (txn) · `humanscale monitor arm(s)` 590 (txn) · `humanscale freedom (chair)` 480/260 (txn) · `humanscale canada` 170 · `humanscale keyboard tray` 170.
- **PAA:** *How good are Humanscale chairs? · Is Humanscale a good chair? · Why is Humanscale so expensive? · What is the best luxury office chair?*
- **Verdict:** **strongest opportunity in the set** — real, transactional Canadian demand (chairs + monitor arms + Freedom model), BBI is the dealer, and there is **no brand page at all.** Transactional intent (`humanscale chair`, `humanscale monitor arms`, `humanscale freedom chair`) is dealer-capture gold. **Build a new Humanscale brand page.**

### Global — page: EXISTS (combined with Teknion) · demand: MED (disambiguation-limited)
- `office furniture global` / `global office furniture` 320 (nav) · `global office chair` / `office chair global` 110 (txn) · `global office furniture canada` 90 · `global upholstery office chair` 40 · geo/model tails 10–20.
- **PAA:** none returned for `global office chair` (brand too generic to trigger PAA).
- **Verdict:** demand is real but the word "global" is hard to disambiguate from non-furniture intent, depressing measured volume. BBI's catalog is Global-heavy, so the **transactional `global office chair` / `global office furniture canada`** terms are worth owning. **Deepen the Global half of the combined page** (and the split argument in Teknion above would give Global a cleaner standalone target too).

### OTG / Offices To Go — page: EXISTS · demand: LOW-MED but transactional
- `offices to go` 260 (nav) · `offices to go canada` 70 · `offices to go standing desk` 20 (txn) · `offices to go desks / reception desk / avro` 10 (txn) · `offices to go warranty / dealers / replacement parts` 10.
- **PAA:** none returned.
- **Verdict:** lower volume, but **transactional model-level tails** (`offices to go standing desk`, `offices to go desks`, `offices to go avro`, `offices to go warranty`) are exactly what a dealer page should catch. Page exists → **deepen with model + warranty + dealer content.** Note: BBI ranks for `offices to go`-adjacent product long-tail already in catalog, just not the brand head.

### ObusForme — page: EXISTS · demand: HIGH but **wellness-skewed (low office fit)**
- `obusforme` 2,400 (info) — but demand is dominated by **consumer wellness**: `obusforme pillow(s)/canada` 880, `obusforme back support` 880, `obusforme massager/massage` 390, `obusforme seat cushion(s)` 260. Office-**chair** terms: `obusforme chair(s)` 170, `obusforme back` 170.
- **PAA:** none returned.
- **Verdict:** big brand name, but ~90% of the demand is pillows/cushions/massagers, **not office furniture.** Office-chair volume is thin (170). Keep the existing page for catalog support; **low net-new SEO upside** for the B2B furniture buyer. Flag — do not over-invest.

### Heartwood — page: EXISTS · demand: NEAR-ZERO
- `heartwood furniture` 110 (nav) · `heartwood office furniture` 40 · `heartwood innovations` 20 · `heartwood furniture kelowna` 10 (a *different* BC retailer — disambiguation risk).
- **PAA:** none.
- **Verdict:** **negligible branded search demand.** Page exists; treat as catalog/casegoods support only — no keyword-driven reason to deepen. (Cross-ref Track C C4 premise correction: Heartwood casegoods are *commercial laminate*, not solid wood.)

### Safco — page: NONE · demand: NEAR-ZERO for furniture (**name collision**)
- `safco` 320 — but split: `safco dental supply / safco dental (canada)` 210/90 is a **different company** (Safco Dental). Furniture terms: `safco products (company)` 50, `safco furniture` 20, `safco canada` 30.
- **PAA:** *Where is Safco Furniture located? · How durable are Safco Office products? · What is the warranty on Safco products?* (generic).
- **Verdict:** furniture demand is near-zero and the head term collides with Safco Dental. **Do not build a brand page.** Catalog support only.

### FireKing — page: NONE · demand: LOW + **stock conflict**
- `fireking` 590 — split across **bakeware/safes** (`fireking jade` 140, `fireking bakeware/loaf pan/plates/coffee cup`). Filing terms: `fireking file cabinet(s) / filing cabinet / fireproof file cabinet` ~40 each.
- **PAA:** none.
- **Verdict:** thin filing-specific demand, **and** BBI's fire-resistant filing is stocked 100% **Gardex, not FireKing** (memory: do NOT re-push FireKing copy; OPEN decision for Steve). **Do not build a FireKing page.** The real fire-filing demand (`fire safe file cabinet` 390, `fireproof cabinet` 320 — BBI ranks p32–36) belongs to the **Gardex/fire-filing collection** (see FILE A gap), not a FireKing brand page.

### Office Star — page: NONE · demand: NOISE (no real brand demand)
- `office star` 140 — but the pulled set is **pure noise**: `star wars box office`, `star of the sea parish office`, `day star first nation band office`, `toronto star office`. Real brand terms: `office star products (canada)` 170/50 (nav).
- **PAA:** none.
- **Verdict:** **no meaningful Canadian brand demand. Drop** — no page, no deepen.

---

## REFERENCE ONLY — NON-CARRIED, cautious-bucket at most, NOT page targets

> ⚠ Everything in this section is **[CARRIER]** — BBI does **not** carry these brands. These rows exist to **size the demand BBI cannot directly capture** (only foil against, fit-based, Steve legal glance). Do **not** mix into the actionable rankings. The live comparison/alternative blog set + Track C already cover the foil play (e.g. `steelcase-vs-teknion`, `nightingale-vs-global`, `humanscale-vs-ergocentric` live; Track C **C1 Herman Miller alternative** drafted + **legal-held**).

| Brand | Top Canada demand | PAA buyers ask | Foil status |
|---|---|---|---|
| **Herman Miller** [CARRIER] | `herman miller` 22,200 · `herman miller chair(s)` 12,100 · `aeron by herman miller` 8,100 | *Is a Herman Miller chair worth it? · Does Herman Miller ship to Canada? · What is the best office chair to buy in Canada? · Why is Herman Miller so expensive?* | Largest premium-US demand pool. Already foiled by Track C **C1 (legal-held)** + live `steelcase-chairs-vs-canadian-ergonomic-seating` mirror. Cautious bucket only. |
| **Steelcase** [CARRIER] | `steelcase` 5,400 · `steelcase leap (v2)` 5,400/1,900 · `steelcase chair(s)` 2,900 · `steelcase gesture` 2,400 (note: `steelcase tires` 2,900 = unrelated tire shop — exclude) | (brand-nav; no furniture PAA) | Foiled by live `steelcase-vs-teknion-ontario-comparison` + `steelcase-chairs-vs-canadian-ergonomic-seating`. Cautious bucket only. |
| **Haworth** [CARRIER] | `haworth office chair(s)` 320 · model tails (`fern` `zody` `soji` `very`) 10–50 | *Is Haworth a good chair brand? · Is Haworth as good as Herman Miller? · Which country made Haworth chairs?* | Modest demand. Foiled by Track C **C2 Haworth vs Teknion (legal-held)**. Cautious bucket only. |
| **Nightingale** [CARRIER] | `nightingale chair` 70 · `nightingale office chair` 40 · `nightingale cxo (chair)` 20 | (thin) | Canadian brand but NOT on BBI's carried list. Foiled by live `nightingale-vs-global-canadian-seating`. Cautious bucket only. |

---

## FLAGS legend
- **[CARRIER]** — non-carried brand (entire reference section). Not a page target; cautious-bucket/fit-based foil only; Steve legal glance.
- **[CANNIBAL]** — brand pages must **not** target the LOCKED generic heads in `priority-keywords.yaml` (ergonomic-chair heads → `/pages/ergonomic-office-chairs`; use-case chair heads → Step-6 review pages). Target **brand** terms only (`<brand> chair`, `<brand> canada`, `<brand> office furniture`).
- **[USED]** — none of the carried-brand heads above are claimed in `batch-ledger.md` / `batch-ledger-trackC.md` (the ledgers claim *comparison/alternative* intent, not brand-nav heads) → all carried-brand heads are unclaimed and available to the brand pages.
- **[SURFACE]** — **Step 4 brand-page deepen** (page exists) or **Step 4 brand-page new** (no page).

---

## TOP CARRIED-BRAND OPPORTUNITIES (real Canadian demand + thin/no page + BBI is dealer), ranked

| # | Brand | Demand signal | Page status | Surface | Why it ranks here |
|---|---|---|---|---|---|
| 1 | **Humanscale** | 2,900 brand / 720 chairs / 590 monitor arms / 480 Freedom — **transactional** | **NONE** | **Step 4 — NEW brand page** | Highest structural advantage: real txn demand + dealer + zero existing page. Monitor-arms + Freedom are dealer-capture gold. |
| 2 | **Teknion** | 6,600 brand (highest in set) + systems tails | EXISTS but **shared w/ Global (thin)** | **Step 4 — deepen / split out** | Biggest brand volume; combined page dilutes it; PAA "is it Canadian / who owns / where made" = ready FAQ block. |
| 3 | **ergoCentric** | 2,900 brand / 1,000 chairs / 170 office chair | EXISTS, not ranking | **Step 4 — deepen** | Ontario-made, OECM-adjacent, perfectly on-brand; rich back-pain/long-hours PAA; cross-links 5a ergonomic hub. |
| 4 | **Keilhauer** | 1,900 brand / 210 furniture / 170 chairs | EXISTS, not ranking | **Step 4 — deepen** | Design-led Canadian brand; "where made / good quality / best Canadian furniture" PAA → Canadian-made trust FAQ. |
| 5 | **OTG / Offices To Go** | 260 brand + txn model tails (standing desk, desks, avro, warranty) | EXISTS | **Step 4 — deepen** | Lower volume but transactional model/warranty tails are dealer-perfect; catalog-heavy. |
| 6 | **Global** | 320 brand / 110 `global office chair` (txn) / 90 canada | EXISTS (combined) | **Step 4 — deepen Global half** | Catalog backbone; own `global office chair` + `global office furniture canada`; benefits from a Teknion split. |

**Do-not-build (carried but no real fit):** **ObusForme** (demand is pillows/cushions, not office), **Heartwood** (near-zero brand demand), **Safco** (collides with Safco Dental; furniture demand ~0), **FireKing** (thin + stock conflict: BBI stocks Gardex — route fire-filing demand to the Gardex/fire-filing *collection*, see FILE A, not a FireKing brand page), **Office Star** (demand is noise).

**Cross-file tie-in:** FILE A shows competitors' **brand-dealer landing pages** earn real traffic (atWork `hon dealers` ~1,874 etv; Source `hon` ~2,932 etv). BBI's carried-brand pages are the same structural play on brands BBI *actually carries* — Humanscale (new) + Teknion/ergoCentric/Keilhauer (deepen) are the highest-leverage Step-4 targets.

---

## BUILD-STATE NOTE (for the next doc PR — not edited this session)
> Phase-1 FILE B (`data/reference/brand-demand-canada-2026-06-25.md`) sizes carried-brand Canadian demand. **Top Step-4 targets:** build a **new Humanscale brand page** (real txn demand, no page, BBI is dealer = highest structural gap); **deepen Teknion (split from the combined Global+Teknion page), ergoCentric, Keilhauer, OTG, Global.** Do-not-build: ObusForme/Heartwood/Safco/FireKing/Office Star (no fit / stock conflict / name collision / noise). Non-carried reference brands (Herman Miller/Steelcase/Haworth/Nightingale) stay cautious-bucket foils — already covered by live comparison posts + Track C (C1/C2 legal-held). Advisory only; building is a separate gated step.
