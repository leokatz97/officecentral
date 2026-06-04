# Track A — Pre-Publish Claims Clearance Checklist

**Date:** 2026-06-04 · **Branch:** `feature/content-batch-trackA-2026-06-03` (PR #102) · **Status: DOCS ONLY — clearance gate, NOT for merge.**

> **UPDATE 2026-06-04 (apply-all pass):** The flagged claims have now been worked across all 15 drafts (minimal surgical edits to the `.html` bodies + `-PACK.json` faq/meta only; no live writes; build-state untouched; PR #102 still open, not merged). Conservative-default rule applied throughout — no unverified claim left standing. Per-item dispositions (FIRMED / SOFTENED / CUT / FLAGGED-LEO / FLAGGED-STEVE) are recorded in **[Part 6 — Clearance Actions Applied](#part-6--clearance-actions-applied-2026-06-04)** at the foot of this doc. Web verification of the 3 weak stats + AODA + Made-in-Canada + OECM 2025-470 is summarized there too. Gates re-run green on all 15 (validate-meta, check-handles → 24/24 link targets 200, create-draft DRY RUN byte-match). **Items still needing a human decision are the FLAGGED-LEO and FLAGGED-STEVE rows — nothing publishes until those are cleared.**

This is a **read-only extraction** across all 15 Track-A conceptual + positioning drafts (brief `.md` + customer-facing `.html` body + `-PACK.json` faq/meta each). **No drafts were edited; no live writes; build-state untouched.** Nothing here changes a draft — it lists every external stat, BBI capability/service claim, legal/regulatory framing, the four re-scopes, every footing/founding-year instance, **and a §5 spec reconciliation of every product cited in the category posts (Slots 10–14) against the PR #103 §5 corrections + the verified-spec dataset**, so each can be cleared before any publish run.

## How to use this

Every item below is assigned to ONE clearer and carries a proposed action. Work the two clearer lists, then the four re-scope sign-offs, then the consistency fixes.

- **Clearer (A) — LEO:** factual accuracy, BBI capability/service truth, external stats sourcing, **§5 spec reconciliation of cited SKUs (§3.3)**, the four re-scopes, footing consistency. → [Part 3](#part-3--clearer-a--leo) (incl. §3.3 §5 reconciliation) + [Part 2](#part-2--the-four-re-scopes-leo-sign-off) + [Part 1](#part-1--footing--founding-year-consistency-check).
- **Clearer (B) — STEVE (STEVE-GATED):** every Made-in-Canada / origin statement, and every warranty mention. → [Part 4](#part-4--clearer-b--steve-steve-gated).

**Action vocabulary:** `KEEP` (cleared as-is) · `VERIFY` (confirm true/accurate before publish) · `CAVEAT` (needs a disclaimer or softening) · `CUT` (remove unless substantiated).

**Slot → file/handle map**

| Slot | File stem | Live handle (PACK) |
|---|---|---|
| 1 | `07-choose-office-furniture-supplier-ontario` | choose-office-furniture-supplier-ontario |
| 2 | `08-where-to-buy-office-furniture-dealer-bigbox-online` | where-to-buy… (dealer vs big-box vs online) |
| 3 | `09-lease-vs-buy-office-furniture-canada` | lease-vs-buy-office-furniture-canada |
| 4 | `10-public-sector-institutional-office-furniture-ontario` | public sector & institutions (BPS) |
| 5 | `11-commercial-vs-consumer-grade-office-furniture` | commercial vs consumer-grade |
| 6 | `12-sit-stand-vs-fixed-desks-office` | sit-stand vs fixed desks |
| 7 | `13-open-plan-vs-private-offices` | open-plan vs private offices |
| 8 | `14-cubicles-vs-open-benching-workstations` | cubicles vs benching |
| 9 | `15-office-pods-vs-building-meeting-rooms` | pods vs built meeting rooms |
| 10 | `16-mesh-vs-upholstered-office-chairs` | mesh vs upholstered chairs |
| 11 | `17-task-chair-vs-executive-chair` | task chair vs executive chair |
| 12 | `18-filing-cabinets-vs-shelving-vs-pedestals` | filing vs shelving vs pedestals |
| 13 | `19-conference-table-boardroom-buying-guide` | conference/boardroom table guide |
| 14 | `20-reception-area-furniture-guide` | reception-area furniture guide |
| 15 | `21-office-design-trends-2026-ontario` | office design trends 2026 (capstone) |

---

## TOP-PRIORITY ITEMS (read first)

These are the load-bearing claims — if any is false the post must not publish:

1. **OECM exclusivity superlative (Slot 1, Leo):** `No other Ontario furniture dealer holds OECM status` — a superlative/exclusivity claim; must be true and defensible.
2. **OECM Agreement number (Slots 1, 2, 4, Leo):** `Agreement 2025-470` — verify the exact agreement number and that it is held via Brant Basics.
3. **Financing program (Slot 3, Leo):** `Brant Business Interiors offers financing and payment plans through our quote process` — must be a real program (re-scope-critical).
4. **"Third-party-rated across every category" (Slot 5, Leo):** strongest all-catalog assertion in the batch — house-brand/generic SKUs may not carry marks.
5. **Three external stats with weak/secondhand sourcing (Slots 7, 8, 9, Leo):** 42,000-worker 2013 study + ~20-min refocus (Slot 7), Gensler 2023 ~12% (Slot 8), Framery study + $10k–$30k built-room (Slot 9).
6. **Made-in-Canada / origin (Slots 1, 2, 4, 10, 15 — STEVE):** STEVE-GATED.
7. **Warranty generalizations (Slots 2, 5, 15 — STEVE):** STEVE-GATED.
8. **Founding-year inconsistency (Part 1, Leo):** `since 1964` appears in only 2 of 15 posts.
9. **§5 spec reconciliation — CLEAN, guardrail only (§3.3, Leo):** every SKU cited in the category posts (Slots 10–14) is described generically (name + PDP route, no hard spec/shape number), so **zero stale §5 figures appear in any draft body.** The three flagged items resolve as: **Sidero 33"H** cited (Slot 14) with no height stated; **Napa oval→racetrack** not cited at all (Slot 13 cites the Zira *boat-shape*, correctly); **Newland pedestal dims** apply to an un-cited SKU. Action is forward-looking only — if Leo adds a figure at voice pass, use the §5-corrected value.

---

## Part 1 — Footing / founding-year consistency check

*Clearer: LEO. The drafts are internally inconsistent on founding year, OECM specificity, and delivery scope. Decide the canonical wording and apply it across the batch.*

### 1a. Corporate-structure line — `a division of Office Central Inc.`

Appears in **all 15 posts**, identically: `Brant Business Interiors, a division of Office Central Inc., …` (each post's 2nd paragraph / intro). **Consistent.** → `VERIFY` the exact legal entity name once; then KEEP.

### 1b. Founding year — `since 1964`

| Post | Wording | Note |
|---|---|---|
| Slot 1 | `…has been a commercial furniture supplier in Ontario since 1964` | present |
| Slot 4 | `…has furnished Ontario institutions since 1964` | present |
| Slots 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | — | **OMITTED** |

**Why flagged:** founding year stated in only 2 of 15 posts. **Proposed action:** `VERIFY` 1964 is correct, then decide — either add a consistent footing line to all posts or accept it only on the two positioning/institutional pieces. (Note: no post cites a location count; the stale "5 Ontario Locations" line was correctly NOT carried — good.)

### 1c. Corporate parent / OECM holder — `parent legal entity Brant Basics`

| Post | Wording | Note |
|---|---|---|
| Slot 1 | `through our parent legal entity Brant Basics, an authorised OECM Supplier Partner under Agreement 2025-470` | full |
| Slot 2 | `through our parent legal entity Brant Basics … under Agreement 2025-470` | full |
| Slot 4 | `through our parent legal entity Brant Basics, an authorised OECM Supplier Partner` **and lower:** `Brant Business Interiors holds OECM Supplier Partner standing under Agreement 2025-470` | **two framings — reconcile who holds OECM (Brant Basics vs BBI directly)** |
| Slot 3 | `our OECM Supplier Partner standing` only — no agreement number, no Brant Basics | softer |
| Slots 5–15 | — | no OECM claim |

**Why flagged:** OECM is described three ways (via Brant Basics + 2025-470 / BBI holds standing under 2025-470 / vague "standing"). Slot 4 contradicts itself in one post. **Proposed action:** `VERIFY` the correct OECM holder + agreement number, then standardize one sentence across Slots 1–4.

### 1d. Delivery / geographic scope

| Post | Wording |
|---|---|
| Slot 1 | `we ship across Canada, install in Ontario and Western Canada` (faq) + `services it across Ontario and beyond` (body) |
| Slot 2 | `installs it, and services it across Ontario and beyond` |
| Slots 4, 6, 13, 14 | scope stated as `Ontario` only (`across Ontario`, `Ontario offices`, `Ontario businesses and institutions`) |
| Slot 15 | `across Ontario and beyond` |

**Why flagged:** scope ranges from "ships across Canada / installs ON + Western Canada" (Slot 1) to "Ontario only." **Proposed action:** `VERIFY` actual ship/install footprint and standardize.

### 1e. Phone number — `1-800-835-9565`

Appears in the bottom-line CTA of **all 15 posts**, identically. → `VERIFY` once; then KEEP. *(Memory note: BBI canonical address is 296 George St N, Peterborough ON — no address appears in any post, so nothing to reconcile there, but confirm the toll-free number is current.)*

---

## Part 2 — The four re-scopes (Leo sign-off)

*Clearer: LEO. Each was re-scoped off the locked roadmap; needs explicit sign-off before publish.*

### RE-SCOPE #1 — Slot 4 → all-BPS (broadened beyond school boards)

- **What changed:** the live OECM cornerstone owns school-board mechanics; Slot 4 was broadened to a cross-vertical **broader-public-sector** furnishing hub (health/municipal/college/gov/non-profit) that links *down* to the cornerstone for school boards.
- **Key wording (body):** audience = `office administrators, facilities coordinators, and procurement leads at hospitals and health teams, municipalities, school boards, colleges, and community non-profits across Ontario`; scope sentence = `Eligible broader-public-sector organisations can purchase furniture through OECM without running a separate competitive tender, because Brant Business Interiors holds OECM Supplier Partner standing under Agreement 2025-470`; link-down = `our education furniture guidance and the OECM cornerstone cover how Ontario boards buy … We keep the mechanics … in a dedicated guide rather than repeating it here`.
- **Note:** the school-board → cornerstone link is currently **plain text (D3 held)**, not a live hyperlink.
- **Action:** `VERIFY` BPS breadth is accurate + sign off on the broadening.

### RE-SCOPE #2 — Slot 3 → buy + financing steer (not "we lease")

- **What changed:** roadmap dropped the consumer "can you rent" framing; re-scoped to a lease-vs-buy decision guide that concludes **buy + finance** (BBI sells new, never positions as a lessor).
- **Key wording (body):** thesis = `For most Canadian businesses furnishing a permanent office, buying commercial-grade furniture beats leasing it`; positioning = `Brant Business Interiors, a division of Office Central Inc., sells new commercial furniture rather than renting it, so our recommendation favours ownership`; finance steer = `If the only thing pushing you toward a lease is the cash, financing the purchase keeps the ownership advantage … Brant Business Interiors offers financing and payment plans through our quote process`; bottom line = `buy commercial-grade and own it; finance the purchase if the cash timing is the issue. Lease or rent when the need is genuinely short term`.
- **Action:** `VERIFY` the financing program is real (see Part 3, item L-B1 — the explicitly-flagged financing claim) + sign off on the buy+finance steer.

### RE-SCOPE #3 — Slot 11 → task-vs-executive (replaces new-vs-refurb)

- **What changed:** roadmap brief was new-vs-refurbished; BBI has **no refurb position** (sells new), so the slot was swapped to task-vs-executive **tier** selection.
- **Key wording (body):** `A task chair and an executive chair are not better or worse than each other; they are built for different jobs and different roles`; bottom line = `Task versus executive is a fit decision, not a quality ranking.`
- **Note:** there is **no "we sell new / no refurb" sentence in the customer-facing copy** — that rationale lives only in the brief/PACK. Confirm none needs to appear in body.
- **Action:** sign off on the angle swap (`KEEP`).

### RE-SCOPE #4 — Slot 15 → substantive trends capstone (not thin decor)

- **What changed:** roadmap dropped a thin "Trendy Styles 2026" decor piece; re-scoped into a substantive, evidence-backed 2026 workplace-design-trends capstone routing to a design consult.
- **Key wording (body lede):** `The office trends worth acting on in 2026 are not about colours or statement light fixtures. They are structural: how the space is zoned, how it supports focus and wellbeing, how sustainably it is built, and how long the furniture lasts` … `this guide is about trends you can act on, not a mood board.`
- **Open decision (from brief):** currently carries NO numeric stats; if Leo adds Gensler/Leesman figures at voice pass, they will need source verification.
- **Action:** `VERIFY` keep + sign off on the substantive scope; if stats added later, route them back through Part 3.

---

## Part 3 — Clearer (A) — LEO

### 3.1 External stats / cited claims

*Every cited statistic, study, figure, or external authority. Highest risk = unsourced or secondhand-sourced figures.*

| ID | Post | Exact wording (body/faq) | Source attributed | Why flagged | Action |
|---|---|---|---|---|---|
| S-1 | Slot 7 | `A widely cited 2013 analysis of more than 42,000 office workers across the United States, Finland, Canada, and Australia found that people in open-plan offices were less satisfied …` | **None in-text** ("widely cited"); brief trail = "via PAA → The Conversation / study" | Major stat, no study/author/journal/URL named; brief source is secondhand | `VERIFY` + cite primary study with link, or `CUT` |
| S-2 | Slot 7 | `it can take roughly twenty minutes or more to fully refocus after a distraction` | **None in-text**; brief = "European Parliament briefing citing interruption research" | Citation-of-a-citation; no link; stated as bare fact | `VERIFY` + cite, or soften/`CUT` |
| S-3 | Slot 7 | faq: `Research has linked fully open layouts to lower environment satisfaction and slower recovery after distractions` | "Research has linked" (generic) | Restates S-1/S-2 with no attribution | `VERIFY` (ties to S-1/S-2) |
| S-4 | Slot 8 | `A 2023 Gensler study found only about twelve percent of United States office workers said they preferred a cubicle layout, with most wanting both autonomy and access to collaboration` | Gensler 2023 (named); brief trail = "via PAA/poppin" | Named but secondhand (poppin's restatement, not the report); the "most wanting both…" clause exceeds the brief evidence; no URL | `VERIFY` against the primary Gensler report; trim unsupported clause |
| S-5 | Slot 8 | faq: `surveys show few workers prefer them` | "surveys" (generic) | Uncited paraphrase of S-4 | `VERIFY` (ties to S-4) |
| S-6 | Slot 9 | `Industry research has found modular pods to be substantially more cost-effective than constructing new meeting rooms` | **"Industry research"**; brief = Framery study | Framery is a **pod vendor** (self-interested); name dropped to anonymous "industry research"; no figure/link | `VERIFY` independence/citability, or `CUT` |
| S-7 | Slot 9 | body + faq: `a traditional enclosed room commonly runs $10,000 to $30,000 or more` (repeated as "five-figure range" and in faq) | **None in-text**; brief = officeinteriors.ca (one competitor blog) | Single competitor-blog $ figure, uncited, repeated in faq/AEO answer | `VERIFY` with a better source or `CAVEAT`/`CUT` |
| S-8 | Slot 5 | `A chair certified to BIFMA has survived hundreds of thousands of test cycles` | ANSI/BIFMA (generic) | Magnitude figure ("hundreds of thousands") attributed generically, no specific test/number cited | `VERIFY` magnitude is defensible |
| S-9 | Slot 5 | table/faq weight bands: consumer `around 100–115 kg (250 lb)`; commercial `to 180 kg (400 lb) and up`; faq `typically … 113 to 136 kg (250 to 300 lb)` | None (general markers) | Internal inconsistency: 250 lb used for both consumer top (table) and commercial bottom (faq) | `VERIFY` + reconcile bands |
| S-10 | Slot 5 | `Seven to ten years or more` service life (table/faq/body) | None | General marker, no source | `KEEP` as hedged marker (or cite) |
| S-11 | Slot 6 | `The Canadian Centre for Occupational Health and Safety describes a sit-stand desk as one that lets a worker change posture through the day …` | CCOHS (named) | One externally-attributed claim; confirm CCOHS's published wording supports the paraphrase; no URL | `VERIFY` against CCOHS source |
| S-12 | Slot 13 | `Plan roughly two feet (about 24 inches) of table edge per person … 30 inches giving a more comfortable … feel`; `about three feet of clearance on every side`; full seats-by-size table | None in-text; brief = ckofficefurniture + neat.no | Sizing heuristics + seats-by-size table stated as guidance, no in-text source (body does add `These are starting points, not rules`) | `KEEP` as hedged guidance (optionally cite) |
| S-13 | Slots 1, 2, 5 | `ANSI/BIFMA, CSA/UL, GREENGUARD` (Slot 1, 5) / `ANSI/BIFMA and CSA` (Slot 2) | Standards bodies named generically | Standards named as common knowledge (acceptable) **but inconsistent**: Slot 2 omits UL + GREENGUARD | `KEEP` content; standardize the list across posts |
| S-14 | Slot 15 | `Across the major 2026 workplace design reports, the same themes recur`; `on nearly every trend list` | "major 2026 workplace design reports" (none named in body); brief = Actiu, Office Principles, Gable, Poppin | Appeals to authority with no named/verifiable source in body | `CAVEAT` (name 1–2 reports) or keep as soft consensus |
| S-15 | Slot 12 | trend: `As more records go digital, many offices are shifting the balance toward open shelving and pedestals` | None ("practical, no study") | Trend asserted as fact, uncited (low risk) | `KEEP` as guidance |
| S-16 | Slot 8 | **Brief-only** `~$200/panel` cubicle cost | brief A.4 (cubicles.com) | **Correctly NOT carried into body** — note only if Leo re-adds it | `KEEP OUT` (verify if re-added) |
| S-17 | Slots 10, 11, 16 | Material/durability guidance: `cheap mesh sags, stretches, and tears` (S10); tier taxonomy (S11) | "Consensus from SERP" (no authority) | Stated as guidance, no testable source | `KEEP` as opinion/guidance |

### 3.2 BBI capability / service claims (must be TRUE)

*Every claim about what BBI offers or is. Each = `VERIFY` unless noted.*

| ID | Post(s) | Exact wording | Why flagged | Action |
|---|---|---|---|---|
| **L-B1** | **Slot 3** | **`Brant Business Interiors offers financing and payment plans through our quote process, and we are purchase-order friendly`** (body) + faq `offers financing and payment plans and is purchase-order friendly` + CTA `ask about financing` | **RE-SCOPE-CRITICAL financing claim — explicitly called out. Asserts a real financing/payment-plan program delivered through the quote process.** | **`VERIFY` the program is real before publish** |
| L-B2 | Slot 1 | `Brant Business Interiors is, through our parent legal entity Brant Basics, an authorised OECM Supplier Partner under Agreement 2025-470 … No other Ontario furniture dealer holds OECM status` | OECM holder + agreement number + **exclusivity superlative** | `VERIFY` all three; superlative is highest-risk |
| L-B3 | Slots 2, 4 | OECM Supplier Partner under `Agreement 2025-470` (via Brant Basics) | Agreement number + holder | `VERIFY` (ties to Part 1c) |
| L-B4 | Slot 3 | `our OECM Supplier Partner standing` (no number/entity) | Softer OECM phrasing, inconsistent with Slots 1/2/4 | `VERIFY` + standardize |
| L-B5 | Slots 1, 2, 3, 4, 5, 6, 7, 8, 9, 15 | `free design consultation` / `free design layout` (body + CTA + interlink to /pages/design-services) | "**Free**" is an affirmative offer asserted across 10 posts | `VERIFY` consultation/layout is genuinely free |
| L-B6 | Slot 1 | `they carry many manufacturers' lines` / `a deep bench of Canadian manufacturers` (multi-line dealer) | Multi-line dealer positioning | `VERIFY` (KEEP — matches known model) |
| L-B7 | Slot 1 | `we ship across Canada, install in Ontario and Western Canada, and stay the single point of contact` | Delivery/install scope + single-source service | `VERIFY` (ties to Part 1d) |
| L-B8 | Slot 5 | `Brant Business Interiors supplies commercial-grade, third-party-rated furniture across every category` | **Strongest all-catalog assertion** — some house-brand/generic SKUs may not carry BIFMA/CSA/GREENGUARD marks | `VERIFY` or soften to "across our core categories" |
| L-B9 | Slots 4, 6, 13, 14, 15 | `furnishes/plans Ontario offices/institutions/workplaces` (+ Slot 5 `sells commercial-grade office furniture`; Slots 10/11/12 `supplies all three / the full ladder / the full range`) | Product-range + space-planning capability per category | `VERIFY` (KEEP — routine, confirm catalog breadth) |
| L-B10 | Slots 2, 4, 6, 13, 14 | PO-friendly + `design layout` / `can spec` / `can plan the storage into your layout` | PO acceptance + design/spec service | `VERIFY` (KEEP) |
| L-B11 | Slot 12 | `lockable, and sometimes fire-rated, filing` for `confidential / legal originals` | Implies BBI carries lockable/fire-rated filing suitable for regulated records | `VERIFY` catalog carries fire-rated/lockable filing |
| L-B12 | Slots 13, 14 | spec figures on cited SKUs: `available in two to five drawers` (S13 lateral); SKUs `our L-shape reception unit` etc. | Concrete spec stated as fact (`two to five drawers`); "our" = carried SKU | `VERIFY` against PDP (handle implies 2/3/4/5-drawer — likely consistent) |
| L-B13 | All 15 | phone `1-800-835-9565` | CTA in every post | `VERIFY` once (ties to Part 1e) |

*(Tax content note — Slot 3 CRA CCA Class 8 — is a Leo factual item but lives under Legal/Regulatory; see Part 4 cross-reference T-1, kept with the caveat tracking.)*

### 3.3 §5 spec reconciliation — category posts (Slots 10–14)

*Clearer: LEO. Cross-checks every product cited in the five category/product posts against the **§5 factual corrections shipped in PR #103** (`fix/spec-audit-s5-factual-corrections-2026-06-03`, 13 SKUs LIVE) and the **verified-spec dataset** (`data/reports/spec-audit-verified-specs-2026-06-03.json`). Scope = Slots 10 (mesh-vs-upholstered), 11 (task-vs-exec), 12 (filing/shelving/pedestals), 13 (conference table), 14 (reception).*

**Headline finding — CLEAN: zero stale §5 figures in any draft body.** Every cited SKU is described **generically — product name + PDP route only, no hard dimension / shape / mechanism / brand number** — per the "category-post rule" stated in each brief (*"illustrative VERIFIED SKUs, conceptual, PDP routing"*). Because no draft exposes a hard spec, no §5-corrected value can be contradicted. The reconciliation is therefore a **forward guardrail**, not a fix list: if Leo adds any figure at voice pass, it must use the §5-corrected value below.

**The three task-flagged corrections, resolved:**
- **Sidero overall height (§5: 32"H → 33"H, SKU `9699268591929`)** — Sidero **is** cited (Slot 14, *"a commercial guest chair like the Global Sidero, offered in many colours"*) but the body states **no height / no dimension** → no stale figure. **Guardrail:** if a height is added, use **33"H**, not 32"H.
- **Napa shape (§5: oval → racetrack, SKU `9724981215545`)** — Napa is **not cited in any of the 15 drafts** → moot for Track A. Slot 13 instead cites the **Global Zira boat-shaped table** (`/products/boat-shaped-conference-table`) and describes it as *"boat-shaped"*, which is accurate for that SKU and **not** a §5-flagged shape. No action.
- **Newland pedestal dimensions (§5: `16"W` → `16"W x 22.7"D x 28"H`, SKU `9950669635897` = NLMP23**B**BF)** — that corrected SKU is **not cited**. Slot 12 cites a **different** Newland pedestal, `/products/newland-box-file-mobile-pedestal` (`9103190753593` = NLMP23BF), and states **no dimensions** → no stale figure.

**Cited-SKU reconciliation table:**

| SKU cited (handle) | Post | Spec/shape stated in BODY | §5 / audit PDP status | Reconciliation → action |
|---|---|---|---|---|
| Kody mesh chair (`kody-mesh-chair-otg13110`) | Slot 10 | none (generic "breathable mesh back") | not in §5 | **CLEAN** |
| Pacific high-back tilter (`pacific-high-back-tilter`) | Slot 10 | none (generic "executive feel") | not in §5 | **CLEAN** |
| Yoho task chair (`mvl2786-yoho-armless-low-back-task-chair`) | Slot 11 | none (generic) | not in §5 | **CLEAN** |
| Concorde exec multi-tilter (`concorde-high-back-executive-multi-tilter-2424`, `9666744680761`) | Slot 11 | none (generic) | §3b origin pending; **NOT** the §5-corrected 24HR Concorde (`9924907008313`/`…613945`) | **CLEAN** (no claim) — guardrail: don't import a 24HR Concorde spec onto this exec SKU |
| Global Premium Series lateral file (`premium-series-lateral-file-cabinet-2-3-4-5-drawer-1`, `9114485391673`) | Slot 12 | "available in two to five drawers" | §5 **deferred** "9300→Prime" line-ref (skipped, resolution pass); §3c cert + §3a warranty pending | **CLEAN** — drawer count matches the handle; draft says "Premium Series" (BBI title), **not** "9300" → `KEEP`. Guardrail: don't add "9300 Series"; PDP cert/warranty stay Steve-gated |
| Global bookcase (`bookcase-15-sizes-available`) | Slot 12 | none ("Global bookcase, 15 sizes") | not in §5 | **CLEAN** |
| Global Newland mobile pedestal (`newland-box-file-mobile-pedestal`, `9103190753593` = NLMP23BF) | Slot 12 | none (generic) | §3a warranty pending; **NOT** the §5-dimension SKU | **CLEAN** — §5 dim fix is on a different, un-cited SKU |
| Global Zira boat-shaped table (`boat-shaped-conference-table`, `9103187345721`) | Slot 13 | shape "boat-shaped" | §3b origin pending; shape **not** §5-flagged | **CLEAN** — "boat-shaped" accurate; Napa (oval→racetrack) is a different, un-cited SKU |
| Flip-top training tables (`training-flip-top-tables-1`, `9686674637113`) | Slot 13 | none (generic) | §3a warranty pending (folding = 1yr, lifetime over-claim on PDP) | **CLEAN** — post asserts no warranty; guardrail keeps it that way |
| L-shape reception unit (`l-shape-reception-72-x-72-x-41-1`, `9103183151417`) | Slot 14 | none — body says "our L-shape reception unit" (no brand, no dims) | §5 **deferred** BRAND mis-tag (Heartwood → Newland by Offices to Go); §3a warranty | **CLEAN now** — no brand stated. **Guardrail (VERIFY):** if a brand is added, use "Newland by Offices to Go (Global)", **never "Heartwood"** |
| Global Sidero guest chair (`sidero-guest-chair-28-colour-options`, `9699268591929`) | Slot 14 | none — "offered in many colours" (no height/dim) | §5 **CORRECTED** height 32→**33"H**; brand "Global" correct | **CLEAN now** — no height stated. **Guardrail (VERIFY):** if a height/dim is added, use **33"H** |

**Net:** `KEEP` all category posts as-is on §5 grounds; the only Leo actions are the two forward guardrails (Sidero height = 33"H; L-shape reception brand = Newland-not-Heartwood) **if** specs are added during the voice pass. Several cited PDPs still carry open §3 (origin/warranty/cert) or deferred §5 (line-ref/brand) items at the **PDP level** — none is asserted in the post bodies, so they don't gate these drafts, but they are the reason the generic-citation discipline must hold through voice pass.

---

## Part 4 — Clearer (B) — STEVE (STEVE-GATED)

*Made-in-Canada / origin, warranty. Plus the tax-content caveat (tracked here for completeness; factual accuracy is Leo's).*

### 4.1 Made-in-Canada / origin statements — STEVE-GATED

| ID | Post | Exact wording | Why flagged | Action |
|---|---|---|---|---|
| O-1 | Slot 1 | `"Made in Canada" is a regulated claim … under the Competition Bureau's guidance, a product can only carry it when the last substantial transformation happened here and a qualifying share of costs is Canadian` + `our Canadian-made office furniture range … when domestic origin is part of your policy 🍁` | Paraphrases the Competition Bureau test but cites no specific publication/threshold; Leo's brief flags the wording | **STEVE-GATED** `VERIFY` Competition Bureau wording + that BBI's "Canadian-made range" meets it |
| O-2 | Slot 2 | `a Canadian-made range for buyers with a domestic-origin policy 🍁` | Origin claim asserted **without** the regulatory caveat Slot 1 carries | **STEVE-GATED** `VERIFY` + consider adding caveat for consistency |
| O-3 | Slot 4 | table/body/faq: `Preference for Canadian-made`; `documented Canadian-content or sustainability preference`; `Canadian-made where policy calls for it` | Framed as buyer policy/preference (not a BBI product origin promise) | **STEVE-GATED** `VERIFY` BBI comfortable associating |
| O-4 | Slot 10 | `many of the commercial mesh and upholstered chairs we carry are Canadian-made office seating from Global and Offices To Go 🍁`; `Canadian-made commercial lines` | Names manufacturers + asserts Canadian-made on carried seating | **STEVE-GATED** `VERIFY` Global/OTG lines qualify as Canadian-made |
| O-5 | Slot 15 | `Choosing durable, Canadian-made office furniture cuts shipping impact, supports local manufacturing … 🍁`; `choose sustainable and Canadian-made where you can`; faq repeats | Canadian-made **+ sustainability-origin** claims (cuts shipping/supports local manufacturing) | **STEVE-GATED** `VERIFY` origin + substantiate sustainability framing |
| O-6 | Slots 11, 12 | **No origin copy in body** despite Global/OTG SKUs being Canadian per briefs | Possible house-style omission (maple-leaf accent expected where Canadian-owned/made copy appears) | **STEVE-GATED** decide whether to add origin copy or intentionally omit |

### 4.2 Warranty mentions — STEVE-GATED

| ID | Post | Exact wording | Why flagged | Action |
|---|---|---|---|---|
| W-1 | Slot 2 | table: `Multi-year terms, dealer handles claims` (dealer column) | Closest to a specific BBI warranty assertion (`Multi-year terms`) | **STEVE-GATED** `VERIFY` the warranty term offered |
| W-2 | Slot 5 | table: commercial warranty `Multiple years, up to lifetime on some components`; `A multi-year warranty signals…` | `up to lifetime on some components` could over-imply BBI lifetime warranties (framed as a market characteristic, not a BBI promise) | **STEVE-GATED** `VERIFY` / `CAVEAT` |
| W-3 | Slot 15 | body: `tends to come with the commercial warranties that keep furniture out of landfill`; faq: `delivering the commercial warranties that extend furniture life` | Generalized warranty assertions (softened by "tends to") | **STEVE-GATED** `VERIFY` defensible |
| W-4 | Slots 1, 10 | Slot 1 `a named warranty term and a person who handles claims` / `warranty backed by a person`; Slot 10 faq `check the rating and warranty` | Warranty referenced as buyer-advice / service framing, **no specific BBI term asserted** | **STEVE-GATED** `KEEP` (advice framing) — confirm |
| — | Slots 3, 6, 7, 8, 9, 11, 12, 13, 14 | — | No warranty mention | n/a |

### 4.3 Tax content caveat — Slot 3 (cross-ref; factual accuracy = Leo)

| ID | Post | Exact wording | Caveat status | Action |
|---|---|---|---|---|
| T-1 | Slot 3 | `office furniture you buy is generally a capital asset in Capital Cost Allowance Class 8, … depreciated at twenty percent on a declining-balance basis` (body + faq 1) | **"Not tax advice" caveat PRESENT** in-text 3×: `None of the below is tax advice; confirm the specifics with your accountant.` / `this is a question to put to them rather than to a furniture company` / faq closes `This is general information, not tax advice.` | **`VERIFY`** Class 8 / 20% declining-balance accuracy (Leo) — caveat requirement already satisfied; keep caveat |

### 4.4 AODA / accessibility framings (factual = Leo; flagged here as regulatory)

| ID | Post | Exact wording | Why flagged | Action |
|---|---|---|---|---|
| A-1 | Slot 4 | `In Ontario, public-facing organisations work under the Accessibility for Ontarians with Disabilities Act, and furniture is part of meeting it`; faq `In Ontario this supports compliance with the AODA` | Softened framing ("supports compliance," "part of meeting it") — **no over-claim** ("AODA-certified" not used). Brief parks wording for confirmation | `VERIFY` wording (cleared as AODA-aligned, not certified) |
| A-2 | Slot 14 | `an accessible-height section of counter … which in Ontario supports AODA compliance`; faq repeats `supports AODA compliance` | Softened ("supports," not "ensures/guarantees") | `VERIFY` wording |

---

## Coverage note

All 15 drafts read in full (brief `.md` + body `.html` + `-PACK.json`). No statistic, capability claim, origin/warranty statement, re-scope, or footing instance was knowingly omitted; where a figure appeared only in a brief and was correctly kept out of customer copy (e.g. Slot 8 `~$200/panel`, Slot 5 steel-gauge `16–18ga`, Slot 6 `20-8-2`, Slot 14 `28 colours` = the Sidero), it is noted as "KEEP OUT / verify if re-added" rather than dropped silently. **§5 spec reconciliation (§3.3):** all 11 distinct SKUs cited across Slots 10–14 were cross-checked against PR #103's §5 corrections + the verified-spec dataset — all describe their SKUs generically, so **zero stale §5 figures appear in any draft** (the Sidero/Napa/Newland flags resolve to two forward guardrails + one moot). **No drafts were edited; no live writes; build-state untouched. HALT for Leo + Steve review.**

---

## Part 6 — Clearance Actions Applied (2026-06-04)

*Apply-all pass on PR #102 branch. Edits limited to the flagged claims; each post's voice, structure, and conventions preserved (British spelling kept; no em-dashes; faq_items byte-synced; interlink anchors re-pointed where a host phrase was cut). **Gates re-run after every edited post:** validate-meta PASS (all titles <60, metas ≤155), check-handles PASS (24/24 unique link targets 200), create-draft DRY RUN PASS (byte-match + interlink count on all 15).*

### 6.1 Web verification results (Part A)

| Claim | Verdict | What was done |
|---|---|---|
| **S-1** Slot 7 — 42,000-worker 2013 open-plan study | **FIRMED + corrected** | Study is real (**Kim & de Dear 2013, *Journal of Environmental Psychology* 36:18–26**, 42,764 workers / 303 buildings). The "United States, Finland, Canada, and Australia" country list is **unsupported** (CBE database, Finland not in it) → **CUT the country list**, added the primary citation inline. Finding (open-plan less satisfied, privacy trade-off not offset) accurate, kept. |
| **S-2** Slot 7 — "~20 min to refocus" | **SOFTENED** | The "20 min / 23:15" figure is **not** a peer-reviewed result (traces to interviews, not a study). **Number CUT.** Reframed to Gloria Mark's actual published finding (interrupted work carries a measurable cost in stress and errors). |
| **S-4** Slot 8 — Gensler 2023 "~12% prefer cubicle" | **SOFTENED + re-attributed** | "12%" + "autonomy/collaboration" is a **Poppin restatement, not in Gensler**. Replaced with Gensler's actual finding (most workers prefer a mix of open + private), stated qualitatively ("most") to stay defensible. |
| **S-6** Slot 9 — Framery "industry research" | **FIRMED w/ honest attribution** | Real study = **Framery × CBRE (2023), ~55% more to build than a pod**. Anonymous "industry research" overclaim removed; now names **pod maker Framery + CBRE** and uses the 55% figure. |
| **S-7** Slot 9 — "$10k–$30k built room" | **FIRMED (kept)** | Independent fit-out data (Cushman & Wakefield / JLL) brackets and slightly exceeds the range, so the existing figure is **defensible and conservative** — kept as-is. *Optional Leo polish: add CAD + a C&W/JLL cite.* |
| **AODA** Slot 4 (A-1) | **ADJUSTED** | Blanket "furniture is part of meeting it" overstated. Reframed to tie to the **Integrated Accessibility Standards Regulation → Design of Public Spaces Standard** (service counters / waiting areas; "build or substantially redesign" trigger). "Supports" retained. |
| **AODA** Slot 14 (A-2) | **FIRMED (kept)** | Counter-specific + already uses "supports AODA compliance" → defensible per source (DOPS requires an accessible service-counter section). No text change. |
| **Made-in-Canada** regulatory wording (O-1 educational half) | **FIRMED** | Corrected the Competition Bureau test to the accurate thresholds: last substantial transformation in Canada + **≥51% direct costs** + a **qualifying statement** ("Made in Canada with imported parts"). |
| **OECM Agreement 2025-470** | **FIRMED (verified)** | Confirmed on oecm.ca: **Furniture, Mattresses and Related Services, ref. 2025-470**, expires 2031-11-12; **both Office Central Inc. and Brant Basics are awarded Category A (Office Furniture) supplier partners.** Number + holder check out. |

### 6.2 Decided overclaim fixes (Part B) + canonicalization (Part C)

| Item | Slot/file | Action | Note |
|---|---|---|---|
| L-B2 OECM exclusivity superlative | 1 / 07 | **CUT** | "No other Ontario furniture dealer holds OECM status" deleted; replaced by the locked self-statement only. |
| L-B8 "third-party-rated across every category" | 5 / 11 | **SOFTENED** | Now "supplies commercial-grade office furniture and can confirm which third-party ratings each line carries" — no all-catalog assertion. |
| OECM phrasing | 1–4 / 07,08,09,10 | **CANONICALIZED** | One wording everywhere: *"registered under our parent legal entity, Brant Basics, as an authorised OECM Supplier Partner"* (+ "under Agreement 2025-470" where it appears). British spelling kept to match house style. |
| Slot 4 OECM self-contradiction | 4 / 10 | **FIXED** | All three instances (intro + body + faq) now read "via Brant Basics"; the "BBI holds directly" framings removed. |
| Company footing | all 15 | **CANONICALIZED** | "family-owned division of Office Central Inc., in business since 1964" applied consistently (posts already carrying "since 1964" just gained "family-owned"). |
| Agreement 2025-470 | 1–4 | **KEPT + standardized** | Established/live; web-verified (above). |
| Phone 1-800-835-9565 | all 15 | KEPT | Already consistent. |
| Standards list (S-13) | 2 / 08 | **STANDARDIZED** | Slot 2 list extended to "ANSI/BIFMA, CSA/UL, and GREENGUARD" to match Slots 1/5. |

### 6.3 Financing (Part D) — CONSERVATIVE DEFAULT

| Item | Slot/file | Action | Note |
|---|---|---|---|
| L-B1 "Brant Business Interiors offers financing and payment plans" | 3 / 09 | **CUT → reframed** | BBI-offers-financing removed from body + faq + bottom-line CTA. Steered to buy-on-merits (kept TCO, durability, **CRA Class 8 / 20% declining-balance**, verified-spec value); third-party financing (bank / equipment-finance provider) mentioned generically. **PO-friendly kept** (real). **→ FLAGGED-LEO** to restore a specific line if BBI does offer financing. |
| T-1 CRA CCA Class 8 / 20% | 3 / 09 | **FIRMED** | Accurate; "not tax advice" caveat already present (3×), kept. |

### 6.4 Origin + warranty (Part E) — STEVE-GATED, conservative default

| Item | Slot/file | Action | Note → flag |
|---|---|---|---|
| O-1 "our Canadian-made office furniture range" | 1 / 07 | **STRIPPED** product-origin claim; kept "deep bench of Canadian manufacturers" (company fact) + "confirm a line's origin in writing"; 🍁 removed | **FLAGGED-STEVE** restore verified Canadian-made lines |
| O-2 "a Canadian-made range … domestic-origin policy 🍁" | 2 / 08 | **STRIPPED**; 🍁 removed | **FLAGGED-STEVE** |
| O-3 "Canadian-made where policy calls for it" (BBI bottom-line) | 4 / 10 | **STRIPPED** from the BBI-capability list; buyer-*preference* framings in table/faq kept (true market description) | **FLAGGED-STEVE** confirm |
| O-4 "Canadian-made office seating from Global and Offices To Go 🍁" | 10 / 16 | **STRIPPED** product-origin → "come from Canadian manufacturers like Global and Offices To Go" (company fact kept); bottom-line "Canadian-made commercial lines" → "contract-grade seating lines"; 🍁 removed; buy-canadian interlink re-anchored | **FLAGGED-STEVE** restore verified Canadian-made |
| O-5 Canadian-made + sustainability-origin (multi-instance) | 15 / 21 | **SOFTENED**: removed 🍁; "cuts shipping / supports local manufacturing" → hedged "can shorten shipping and support local industry"; durability (not warranty) now carries the landfill point. Buyer-advice "Canadian-made" (advice-framed, "where you can") retained with buy-canadian interlink | **FLAGGED-STEVE** confirm sustainability-origin framing |
| O-6 no origin copy despite Canadian SKUs | 11,12 / 17,18 | **LEFT OMITTED** (no change) | **FLAGGED-STEVE** decide add-vs-omit |
| W-1 "Multi-year terms" (dealer warranty col) | 2 / 08 | **SOFTENED** → "Manufacturer warranty, dealer handles claims" (no specific term) | **FLAGGED-STEVE** restore term |
| W-2 "up to lifetime on some components" | 5 / 11 | **SOFTENED** → "longer on some components" (lifetime over-claim removed) | **FLAGGED-STEVE** |
| W-3 "commercial warranties that keep furniture out of landfill / extend furniture life" | 15 / 21 | **SOFTENED/REMOVED** warranty generalizations (body + faq); durability framing substituted | **FLAGGED-STEVE** restore a defensible commercial-warranty line |
| W-4 warranty as buyer-advice (no BBI term) | 1,10 / 07,16 | **KEPT** (advice framing) | confirmed |

### 6.5 Delivery scope (Part C) — standardized to Ontario-wide, originals FLAGGED-LEO

| Slot/file | Original | Now | Flag |
|---|---|---|---|
| 1 / 07 (faq) | "ship across Canada, install in Ontario and Western Canada" | "deliver and install across Ontario" | **FLAGGED-LEO** restore national/Western if real |
| 1 / 07 (body Q + bottom) | "ship across Canada…"; "services it across Ontario and beyond" | "deliver and install in my region"; "across Ontario" | **FLAGGED-LEO** |
| 2 / 08 (bottom) | "services it across Ontario and beyond" | "across Ontario" | **FLAGGED-LEO** |
| 15 / 21 (body) | "does that across Ontario and beyond" | "across Ontario" | **FLAGGED-LEO** |

### 6.6 §5 guardrails (Part F) — confirmed clean, no edits needed

- **Sidero (Slot 14 / 20):** cited with **no height** stated → clean. Guardrail holds (if ever added, 33"H).
- **L-shape reception unit (Slot 14 / 20):** **no brand** stated, no "Heartwood" present → clean. Guardrail holds (Newland by Offices to Go if added).
- All other cited SKUs describe generically; reconciliation remains CLEAN.

### 6.7 Open FLAGGED items still needing a human (nothing publishes until cleared)

**FLAGGED-LEO**
- Restore a specific BBI **financing** line if BBI offers one (Slot 3 / 09).
- Confirm **delivery footprint** and restore national/Western Canada wording if real (Slots 1, 2, 15 — see 6.5).
- **L-B5** "free design consultation/layout" (10 posts) — verify genuinely free.
- **L-B11** lockable / fire-rated filing (Slot 12 / 18) — verify catalog carries it (kept as soft advice).
- **S-8** BIFMA "hundreds of thousands of test cycles" (Slot 5 / 11) — verify magnitude (kept).
- **S-9** weight-band internal inconsistency — 250 lb used as both consumer-top and commercial-bottom (Slot 5 / 11) — reconcile (kept).
- **S-14** "major 2026 workplace design reports" (Slot 15 / 21) — name 1–2 reports or keep as soft consensus (kept).
- **S-7** optional: add CAD + a C&W/JLL citation to the $10k–$30k figure (Slot 9 / 15).
- Routine capability verifies **L-B6 / L-B9 / L-B10 / L-B12** (catalog breadth, PO acceptance, drawer-count) — kept, low risk.

**FLAGGED-STEVE**
- Restore verified **Canadian-made / Made-in-Canada** product lines where true (O-1, O-2, O-3, O-4, O-5); re-add the 🍁 accent alongside any restored origin copy.
- Decide **add-vs-omit** origin copy on Slots 11 & 12 (O-6).
- Restore defensible **warranty** statements (W-1 dealer term; W-2 component coverage; W-3 commercial-warranty line).
