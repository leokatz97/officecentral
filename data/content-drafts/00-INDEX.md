# Batch-1 Content Drafts — Index, Selection & Rationale

**Date:** 2026-06-03 · **Branch:** `feature/content-batch-1-2026-06-03` · **DOCS ONLY — drafts for Leo's review, nothing published**

These five first-draft blog posts were selected from the locked roadmap (`data/reports/content-roadmap-2026-06-03.md`) + the build-state NEXT ACTIONS, then validated against a fresh DataForSEO pull (`../reports/content-engine/keyword-serp-research-2026-06-03.md`). Every draft is grounded in the North-Star ICP (`../reports/content-engine/north-star-icp.md`) and modelled on the live Cornerstone Post 1 structure. **Leo edits to voice + fact-checks every stat before anything ships.**

---

## Phase 1 — The 5 selected posts (scored, data-justified)

Scoring (1–5; ★ = standout): **Whitespace** (competitor absence) · **Demand** (vol + PAA) · **Winnability** (winnable long-tail vs high-KD heads) · **Conversion** (value to a qualified Ontario buyer) · **AEO** (citation/FAQ potential).

| # | Draft | Pillar | Primary kw (Canada vol) | Whitespace | Demand | Winnability | Conversion | AEO | Why it's in |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|---|
| **1** | [How to Plan an Office Layout](01-office-space-planning-pillar.md) | P1 pillar | office space planning 40 / office floor plan 260 / office layout ideas 110 *(+workspace planning 50)* | ★5 | 3 | 5 | ★5 | 4 | The lead production focus + design-consultation hub everything links into. **0 Ontario dealers rank** — all software/UK-fitout/US-design. Owns the differentiation moat. |
| **2** | [Are Ergonomic Office Chairs Worth It?](02-ergonomic-chairs-worth-it-faq-hub.md) | P3 AEO FAQ hub | best office chair for long hours 260 / ergonomics of chair 14,800 (info) / what is an ergonomic chair 110 | 3 | ★5 | 4 | 3 | ★5 | The dataset's richest PAA/AI-Overview vein (20-8-2, 90-90-90, "is Herman Miller worth it"). Pulled early per roadmap Nuance A. AEO citation magnet; routes to seating. |
| **3** | [Quiet, Focus & Phone Spaces for Open Offices](03-quiet-spaces-acoustic-pods.md) | P1 cluster | office phone booth 210 / office pod 720 / meeting pod 170 *(≈1,270 aggregate)* | ★5 | 4 | 4 | ★5 | 4 | Acoustic pods = hot item (`project_seo_strategy_2026`). Real demand, **`/collections/acoustic-pods` + `/collections/telephone-booths` already live.** Only atWork ranks among Ontario dealers. Project/quote-led ($3k–$13k SKUs). |
| **4** | [Canadian-Made Office Furniture for Business](04-canadian-made-office-furniture.md) | P4 buy-Canadian | canadian office chairs 2,900 / canadian made office chairs 140 / canadian desks 720 | 4 | ★5 | 3 | 4 | 3 | Highest hard demand in the non-ergonomics set + live r/BuyCanadian sentiment. **No Ontario commercial dealer owns "Canadian-made for business/procurement."** Ties to the buy-canadian collection build + 🍁 moat. |
| **5** | [Hot-Desking vs Assigned Desks](05-hot-desking-desk-allocation.md) | P1 cluster | hot desking 390 (**LOW competition**) | ★5 | 4 | ★5 | 4 | 4 | **Entire SERP is software/definitions/coworking — ZERO furniture dealers.** Total whitespace for a furniture+layout angle. "Hot-desking: hell no" (140+ Reddit comments) is the hook. Routes to design-services + benching. |

**Weighting check (per brief):** 3 of 5 are P1 design/space-planning (the whitespace the brief said to weight to); the early ergonomics-FAQ AEO play is included (#2); every post anchors on a *winnable long-tail* (office floor plan, long-hours, phone booth, canadian-made, hot-desking) rather than a high-KD head term; all five route to a real conversion destination.

### Production order (recommended)
Mirrors the locked roadmap sequence + build-state NEXT ACTIONS: **#1 (P1 pillar) → #2 (ergonomics FAQ early for AEO) → #4 (buy-Canadian, pairs with the buy-canadian collection build) → #3 (Quiet Spaces, pairs with that collection) → #5 (hot-desking cluster).** Posts #3 and #4 are gated to publish *with* their collection builds so the internal links resolve.

### Runners-up (and why not, this batch)
- **Reception-area furniture** (`reception desk` 2,900) — strong demand, but already served by the live `/collections/reception-desks-desks` collection page; better as a P1 cluster cross-link than a standalone blog. *Hold for batch 2.*
- **Cost to furnish an office / budget guide** (`office chairs cheap` 720, `best budget office chair` 590) — good bottom-funnel conversion, but "cheap/budget" framing risks pulling consumer intent and has no clean winnable head; fold the cost question into the pillar + quote-process FAQ instead. *Hold.*
- **Meeting / boardroom furniture** (`conference table` 720 / `boardroom tables` 880) — commercial-collection play (`/collections/boardroom`), thinner *blog* angle. *Hold / cross-link from #1.*
- **P2 government-office setup** — strategic moat but ~0 measurable demand; belongs in the cornerstone cadence (Post 2 Healthcare/FHT, Post 3 Cubicle-vs-Open-Plan municipal), not this winnable-traffic batch.
- **Quote-process / "how to request a quote"** (A29) — highest *conversion* intent but no measurable standalone demand; deploy as a FAQ block + CTA across all five rather than its own thin post.

---

## Files in this folder
- `00-INDEX.md` — this file (selection, order, rationale, Questions for Leo at the bottom).
- `01-office-space-planning-pillar.md` … `05-hot-desking-desk-allocation.md` — one full research + draft package per post.

Each draft contains: keyword map · competitor gap + BBI angle · outline · full first-draft body (HTML-ready prose) · AEO assets (tables/checklists) · FAQ block as `Question||Answer` (drops into `faq.items`) · internal-link spec (D3 targets — HELD, spec only) · meta (title <60, description, handle) · image needs · sources.

---

## Questions for Leo (decisions parked — none blocked the drafting)

**Fact-checks before any post ships (the drafts mark these inline with ⚠️):**
1. **Canadian-made origins (Draft 4 — HIGHEST priority).** Every manufacturing-origin claim — Global Furniture Group, ergoCentric, Keilhauer, Teknion, and per-line — must be verified with the manufacturer before publishing. "Made in Canada" is legally defined (Competition Bureau). Default to "Canadian company / designed in Canada" where origin isn't confirmed. I did **not** assert any origin as fact — all are flagged ⚠️verify.
2. **ergoCentric "designed + built in Toronto" (Drafts 2 & 4).** Confirm before stating.
3. **Founding year + footprint (Draft 1 & all "Why BBI" blocks).** Build-state cites "founded-1964"; `icp.md` flags the "5 Ontario Locations" line as stale and the canonical address is now Peterborough (701 The Queensway, Units 2-4). Confirm the founding year and how to describe the footprint before any post cites it.
4. **CCOHS 72 sq ft / 6.7 m² workstation figure (Draft 1).** Pulled from the live SERP (ccohs.ca). Verify the exact number + cite the page before publishing as the Canadian benchmark.
5. **Planning heuristics (Drafts 1, 3, 5).** Space-per-person ranges, "1 pod per 8–12 people," and desk-sharing ratios (0.5–0.7/person) are framed as *guidance*, not standards. Confirm you're comfortable publishing them as heuristics, or swap for a "comes out of the layout" framing.

**Strategy / scope decisions:**
6. **Western Canada in blog content.** Drafts lead Ontario + generic-Canada and treat Western Canada as a natural extension (per the overnight North Star), even though `icp.md` makes it co-primary. Confirm Western Canada shouldn't get dedicated blog targeting in batch 1 (vs. the geo landing-page program). *(Also raised in north-star-icp.md.)*
7. **Persona source.** Personas were taken from `icp.md` (the canonical locked ICP); the recon supplied verticals + outcome paths verbatim. Confirm that's the intended reading of "extract personas from the recon + build-state." *(Also in north-star-icp.md.)*
8. **Publish gating for Drafts 3 & 4.** Both depend on collections that are NEXT-ACTION builds: Draft 3 → Quiet Spaces surfacing (`acoustic-pods`/`telephone-booths` already live; the consolidated collection isn't), Draft 4 → the `buy-canadian` collection (handle TBD). Recommend publishing each *with* its collection so internal links resolve. Confirm the final `buy-canadian` handle.
9. **Medical-claim guardrail (Draft 2).** Scoliosis/back-condition queries are answered with "adjustability matters + consult a clinician," never a health claim. Confirm that's the line you want.
10. **D3 internal links are HELD.** Every "internal-link spec" lists *targets only* — nothing is wired, per build-state (D3 held until Tier 1 URLs final). These run mechanically once D3 unblocks.

**Production:**
11. **Featured images.** Every post needs a featured image for the BlogPosting `image` field (per the STEVE-SET-BLOG-FEATURED-IMAGE pattern) — flag which come from the OCI/design-photos libraries vs. need Steve/AI-pipeline art (noted per draft).
12. **Per-post DataForSEO re-pull at write-time.** The fresh pull (`../reports/content-engine/keyword-serp-research-2026-06-03.md`) seeds these briefs; CLAUDE.md still wants a confirming pull when each post is finalized for production (volumes drift).
