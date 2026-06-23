# Track C — Competitor, Comparison & Regional Batch (x10) — INDEX

**Started:** 2026-06-23 · **Branch:** `feature/content-batch-trackC-2026-06-23`
**DOCS ONLY this run** — no Shopify writes, no `--live`, no build-state edits. PACKs + dry-run gates only.
**Author byline (all):** Steve Katz · **Blog:** News (`108557861177`).

This batch extends the live News blog (39 published + 1 draft as of 2026-06-23 recon, reconfirmed
live this session) into three competitor/comparison lanes: ALTERNATIVE-TO (A), COMPARISON (C), and
REGIONAL (R). Track A (15 conceptual/positioning posts) and the Step-6 review pages own the keyword
heads listed in `batch-ledger.md` and `data/reference/priority-keywords.yaml`; every Track-C target
below was de-conflicted against both before keyword work began.

## This session — BUILT (PACK + gates PASS, HALT for Leo voice + Steve carrier/legal review)

| ID | Working title | Primary kw | Handle | Status |
|---|---|---|---|---|
| A1 | Source Office Furniture Alternative (Ontario) | source office furniture alternative | `source-office-furniture-alternative-ontario` | PACK + gates |
| A2 | IKEA Office Furniture Alternative for Business (Ontario) | ikea office furniture alternative | `ikea-office-furniture-alternative-business-ontario` | PACK + gates |
| A3 | Wayfair Professional Office Furniture Alternative (Ontario) | wayfair professional alternative | `wayfair-professional-office-furniture-alternative-ontario` | PACK + gates |
| A4 | Buying New vs Used Office Furniture in Ontario | new vs used office furniture | `buying-new-vs-used-office-furniture-ontario` | PACK + gates · ⚠ THIN-DEMAND FLAG |
| C1 | Herman Miller vs Canadian Ergonomic Seating (Ontario) | herman miller alternative | `herman-miller-vs-canadian-ergonomic-seating` | PACK + gates · ⚠ FLAG STEVE + LEGAL |

## Seeded — PLANNED, batch 2 (NOT built this session)

| ID | Working title | Claimed primary kw | Lane |
|---|---|---|---|
| C2 | Steelcase vs Global office furniture (Ontario) | steelcase vs global | Comparison (carried-vs-noncarried, cautious) |
| C3 | Knoll vs Canadian contract furniture (Ontario) | knoll alternative | Comparison (cautious, non-carried) |
| C4 | Haworth vs Canadian workstations (Ontario) | haworth alternative | Comparison (cautious, non-carried) |
| R1 | Office furniture Kitchener-Waterloo | office furniture kitchener | Regional (geo) |
| R2 | Office furniture London Ontario | office furniture london ontario | Regional (geo) |

> Batch-2 targets are pre-de-conflicted in `batch-ledger-trackC.md` (claimed-keyword block) so research
> can start clean. Build-state untouched; close-outs noted for the next doc PR.

## Per-post artifacts (this session)

Each built post has three files in `data/content-drafts/`:
- `trackC-<ID>-<slug>.html` — plain body (bold hook, embedded tables, plain FAQ block, NO `<a>`; the
  engine inserts chips + interlinks at create-draft).
- `trackC-<ID>-<slug>-PACK.json` — the PUBLISH PACK (title/meta/handle/tags/excerpt/faq_items/interlinks).
- Research note + carve rule: see the matching entry in `batch-ledger-trackC.md`.
</content>
</invoke>
