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

## Batch 2 — BUILT (2026-06-23, PACK + gates PASS, HALT for Leo voice + Steve carrier/legal review)

Branch `feature/content-batch-trackC-b2-2026-06-23`. DOCS ONLY — no Shopify writes, no `--live`, build-state untouched.
**The five seeds were re-scoped per the build brief** (steelcase-vs-global → Haworth-vs-Teknion; knoll → Keilhauer-vs-Global; haworth-alt → solid-wood-vs-laminate; office-furniture-kitchener → delivery+installation service; office-furniture-london → Waterloo tech corridor). Full carve rules in `batch-ledger-trackC.md`.

| ID | Working title | Primary kw | Handle | Status |
|---|---|---|---|---|
| C2 | Haworth vs Teknion: Office Systems Compared in Ontario | haworth vs teknion (AEO) | `haworth-vs-teknion-office-systems-ontario` | PACK + gates · ⚠ FLAG STEVE + LEGAL |
| C3 | Keilhauer vs Global: Office Seating Compared in Ontario | keilhauer vs global (AEO) | `keilhauer-vs-global-office-seating-ontario` | PACK + gates |
| C4 | Solid Wood vs Laminate Office Furniture in Ontario | solid wood vs laminate office furniture (AEO) | `solid-wood-vs-laminate-office-furniture-ontario` | PACK + gates · ⚠ PREMISE CORRECTION (Heartwood = laminate) |
| R1 | Office Furniture Delivery and Installation in Ontario | office furniture installation (90/mo) | `office-furniture-delivery-installation-ontario` | PACK + gates |
| R2 | Office Furniture for Waterloo Region Tech Offices | region+sector tech (AEO) | `office-furniture-waterloo-region-tech-corridor` | PACK + gates · ⚠ THIN-DEMAND FLAG |

> All five: fresh DataForSEO/live SERP + PAA/AI-Overview → de-conflicted primary kw → differentiated write (distinct table, FAQ, intro, CTA, persona, #1 product) → PACK → validate-meta + check-handles 200 + create-draft DRY RUN byte-match all PASS → committed. Nothing published; build-state close-outs (5 new "Blog #N" rows) noted for the next doc PR. C2 excluded from the next create-draft run until Steve + legal clear it.

## Per-post artifacts (this session)

Each built post has three files in `data/content-drafts/`:
- `trackC-<ID>-<slug>.html` — plain body (bold hook, embedded tables, plain FAQ block, NO `<a>`; the
  engine inserts chips + interlinks at create-draft).
- `trackC-<ID>-<slug>-PACK.json` — the PUBLISH PACK (title/meta/handle/tags/excerpt/faq_items/interlinks).
- Research note + carve rule: see the matching entry in `batch-ledger-trackC.md`.
</content>
</invoke>
