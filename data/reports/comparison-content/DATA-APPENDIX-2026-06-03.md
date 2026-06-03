# Comparison-Content Strategy — Data Appendix (auditable provenance)

**Date:** 2026-06-03 · companion to [`comparison-content-strategy-2026-06-03.md`](comparison-content-strategy-2026-06-03.md)
All data: **DataForSEO** (Canada, location_code 2124, language `en`) pulled 2026-06-03, plus live HTML fetches of the 7 Venn pages and read-only HTTP status checks of BBI handles. Every figure in the strategy doc traces to a file here. Pulls are reproducible via the committed scripts (REST-direct through [`scripts/dfs_client.py`](../../../scripts/dfs_client.py)).

## Reproduce
```
python3 scripts/comparison_phase1_venn.py        # Venn per-URL ranked keywords (Canada)
python3 scripts/comparison_phase2_universe.py    # curated seeds + keyword_ideas expansion + KD
python3 scripts/comparison_phase2_brands_serp.py # brand-vs-brand + 20 live SERP reads + PAA
python3 scripts/comparison_phase3_score.py       # weighted candidate scoring
python3 scripts/comparison_phase4_traffic.py     # modelled traffic projection
```

## Committed data files (the auditable analysis tables)

| File | What | Source endpoint |
|---|---|---|
| `venn-per-url-ranked-keywords.csv` | 109 rows: per-Venn-URL ranked kw (kw, vol, KD, pos, ETV, intent) | `dataforseo_labs/google/ranked_keywords` |
| `venn-per-url-summary.json` | per-URL kw count, total ETV, top-10, primary query | derived |
| `phase2-curated-seeds.csv` | 60 curated comparison seeds w/ vol, KD, competition, intent | `keyword_overview` + `bulk_keyword_difficulty` |
| `phase2-keyword-ideas-raw.csv` | 2,400 raw expansion ideas (12 category seeds) | `keyword_ideas` |
| `phase2-comparison-filtered.csv` | 94 comparison-pattern ideas (deduped, KD-merged) | derived |
| `phase2-comparison-universe-clean.csv` | 40 furniture-relevant comparison terms (noise-filtered) | derived |
| `phase2-brand-comparison.csv` | 33 brand-vs-brand / material / value / worth-it terms | `keyword_overview` + KD |
| `phase2-serp-top10.csv` | top-10 organic results for 20 priority clusters (domain, pos, title) | `serp/google/organic/live/advanced` |
| `phase2-serp-paa.csv` | 46 People-Also-Ask questions across the 20 clusters | same SERP pull |
| `phase3-scored-candidates.csv` | 17 candidate posts, 6-dim scores + weighted rank | scoring script |
| `phase4-traffic-model.csv` | per-post + portfolio modelled monthly visits | traffic script |

## Domain calibration (measured, `domain_rank_overview`, Canada)
- **venn.ca:** 12,232 organic ranked kw · ETV ~116,288/mo · 46 #1 · 2,192 top-10.
- **brantbusinessinteriors.com:** 49 ranked kw · ETV ~60/mo · 0 #1 · 3 in pos 4–10.

## Known data limitations (honesty log)
- **Backlinks API not on subscription** (`backlinks_bulk_ranks` → 40204 access denied). Domain authority is proxied via Labs ranked-kw/ETV counts; time-to-rank on KD>25 terms is **modelled, not measured**.
- **KD is null in `keyword_overview`** — merged separately from `bulk_keyword_difficulty`. A few low-volume terms returned no KD (blank in CSVs).
- **`keyword_ideas` noise:** "executive chair" and "conference table" seeds pulled political/retail homonyms (governor general, coffee tables); filtered out in `phase2-comparison-universe-clean.csv` via a furniture-anchor whitelist.
- **SERP-feature tally** on Venn per-URL pull came back empty (wrong field level); SERP features for the office clusters were captured correctly from the live `serp_organic` reads (`phase2-serp-*`).
- **Raw API JSON** (`raw/`, ~6.3 MB / 41 files) is gitignored to keep the repo lean; it is fully regenerable from the committed deterministic scripts above.
- **Venn analysis** used live HTML (7 pages) for structure/schema only — no copy reproduced; structural facts (word counts, table columns, schema types, dates, authors) are extracted programmatically.
