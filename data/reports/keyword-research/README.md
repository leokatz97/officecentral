# Keyword Research — COMPETITOR-KEYWORD-RECON-1

Read-only DataForSEO reconnaissance for Brant Business Interiors (BBI). Competitor +
BBI-baseline keyword data with multi-dimensional classification, plus a BBI-positioning
seed expansion and competitor page-archetype analysis. **No production writes.**

Run date: **2026-05-30** · Branch: `feature/competitor-keyword-recon-1` · PR #66

> **Note:** all `*.csv` and `raw/` JSON in this folder are **gitignored** (bulk data).
> Only the `*.md` summaries + the scripts in `scripts/recon_*.py` are committed. Regenerate
> the CSVs anytime by re-running the scripts (they read credentials from `.mcp.json`).

---

## How it was built

DataForSEO was driven via its **REST API directly** (credentials read from `.mcp.json`),
not via the MCP tools — the MCP returns results into the agent context, which does not scale
to ~10k keyword rows. All location = **Canada (2124)**, language = **en**.

| Script | Phase | What it does |
|---|---|---|
| `scripts/dfs_client.py` | 0 | Shared REST client (auth, retries, raw-JSON dump) |
| `scripts/recon_pull.py` | 1–3 | Domain Pages (relevant_pages) + Ranked Keywords (pos 1-50) for competitors + BBI/OfficeCentral baselines |
| `scripts/recon_serp_features.py` | 2.5 | SERP enrichment (PAA, featured snippet, AI Overview, local pack) for top-30 + geo |
| `scripts/recon_classify.py` | 4 | Aggregate + dedupe + KEEP/DROP filter + full classification |
| `scripts/recon_summary.py` | 5 | Builds `SUMMARY-*.md` |
| `scripts/recon_seed_expansion.py` | follow-on | keyword_suggestions on 41 BBI-positioning seeds (7 defensible angles); net-new vs competitors |
| `scripts/recon_expansion_summary.py` | follow-on | Builds `SEED-EXPANSION-SUMMARY-*.md` |
| `scripts/recon_pages_analysis.py` | follow-on | Competitor page-archetype traffic analysis |

Re-run order if regenerating: `recon_pull.py` → `recon_classify.py` → `recon_serp_features.py`
→ `recon_classify.py` (again, to merge SERP flags) → `recon_summary.py` →
`recon_seed_expansion.py` → `recon_expansion_summary.py` → `recon_pages_analysis.py`.

---

## Competitor set (12 domains, 10 Ontario-priority)

The original `shaw-furniture.com` and `furniture-options.ca` returned **zero Canada rankings**
in DataForSEO and were dropped (logged in `manual_review.csv`). Replaced/expanded with Ontario
Tier-1 dealers discovered via DataForSEO competitor analysis + a Maps shortlist, each verified
to have ranking data:

`sourceofficefurniture.ca` (ON+national), `atwork.ca` (Toronto), `mapofficefurniture.com`,
`officestock.com`, `barrysofficefurniture.com`, `grandandtoy.com` (ON HQ + national),
`theofficeshop.ca`, `poi.ca` (Mississauga), `vaughanofficefurniture.com`,
`newmarketofficefurniture.com` — plus `ugoburo.ca` (QC) and `monk.ca` (BC) for breadth.

---

## Deliverables (read these in order)

1. **`SUMMARY-2026-05-30.md`** — main report: coverage, tier × intent matrix, site-surface
   distribution, outcome paths, industry match, difficulty×volume opportunity map, FAQ/AI/PAA
   targets, featured-snippet opportunities, defensible-angle lists, gaps, next actions.
2. **`SEED-EXPANSION-SUMMARY-2026-05-30.md`** — BBI-positioning keywords by defensible angle,
   flagged **net-new vs competitors** (BBI whitespace).
3. **`PAGE-ARCHETYPE-ANALYSIS-2026-05-30.md`** — where competitor organic traffic concentrates
   by page type (collection / product / geo / blog / service), informing BBI's architecture.
4. **`manual_review.csv`** — edge cases to resolve (dropped domains, no-KEEP-match keywords).

### Data files (gitignored, on disk)
- `competitor-keywords-aggregated-2026-05-30.csv` — the master classified competitor set.
- `bbi-seed-expansion-2026-05-30.csv` — classified expansion keywords + net-new flags.
- `ranked-keywords-{domain}-*.csv`, `top-pages-{domain}-*.csv` — per-domain raw pulls.
- `ranked-keywords-bbi-*.csv` — BBI baseline (70 kw).
- `serp-features-top30-*.csv`, `geo-local-pack-*.csv` — Phase 2.5 SERP features.
- `raw/` — every DataForSEO JSON response + reconciliation stat files.

---

## Column dictionary — `competitor-keywords-aggregated-*.csv`

| Column | Meaning |
|---|---|
| `keyword`, `search_volume`, `cpc`, `competition`, `keyword_difficulty` | Base DataForSEO metrics (volume = max across ranking competitors) |
| `difficulty_band` | `easy` <30 · `medium` 30–60 · `hard` >60 |
| `best_competitor_rank`, `ranking_competitors`, `competitor_count` | Strongest position + which competitor domains rank for it |
| `intent_category` | 9-way: vendor_relationship · compliance_certification · procurement_process · use_case_vertical · geographic · informational · service · design_service · product_generic (+ manual_review) |
| `bbi_industry_match` | healthcare · education · government · non-profit · professional-services · multi-industry · not-applicable |
| `bbi_outcome_path` | quote-request · ecom-purchase · design-consultation · multi-outcome · informational-only |
| `keyword_tier` | `head` (1-2 words) · `mid` (3) · `long_tail` (4+) |
| `site_surface_recommendation` | comma-list of: pdp · brand_page · collection_page · industry_page · oecm_page · service_page · faq · blog · pillar_page · cluster_page · geo_page · homepage |
| `question_format` | TRUE if keyword starts how/what/why/when/where/who/can I/should I/are/is |
| `featured_snippet_opportunity` | TRUE if SERP has a snippet held by a non-authority competitor (top-30 only) |
| `ai_overview_present` | TRUE if AI Overview fired (top-30 + geo only; blank otherwise) |

`bbi-seed-expansion-*.csv` adds `seed_angles`, `is_net_new_vs_competitors`, `bbi_already_ranks`.

---

## Next action for Leo

1. Read the three `*.md` summaries (start with `SUMMARY`).
2. Resolve `manual_review.csv` edge cases.
3. Bring `competitor-keywords-aggregated` + `bbi-seed-expansion` CSVs + summaries to the
   **ICP-KEYWORD-WALKTHROUGH** session in web chat to lock the per-page keyword map.
4. Priority lanes (highest BBI-fit × lowest competitor coverage): **Eastern-Ontario geo**,
   **OECM / procurement**, **design / space-planning** — build geo_page / oecm_page /
   service_page first.
