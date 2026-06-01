# Priority Keyword Rank Tracking

Weekly Google-organic rank tracking for **brantbusinessinteriors.com** against the
locked **priority-keywords.yaml v1** keyword set (PHASE-C-STREAM-C, 2026-06-01).

- **Script:** [`scripts/rank-tracking-weekly.py`](../../../scripts/rank-tracking-weekly.py)
- **Source keyword list:** [`data/reference/priority-keywords.yaml`](../../reference/priority-keywords.yaml) v1 (4 locked clusters)
- **Human-readable map:** [`docs/strategy/bbi-keyword-map-2026-05-31.md`](../../../docs/strategy/bbi-keyword-map-2026-05-31.md)
- **Snapshots are gitignored** (`*.csv`) — only this README and the script are committed.

---

## Methodology

For each of the **42 locked v1 keywords** the script makes two DataForSEO REST calls:

| Data | Endpoint | Notes |
|---|---|---|
| **Current rank + ranking URL** | `serp/google/organic/live/advanced` | one call per keyword, `depth=100` (sees ranks 1–100) |
| **Search volume + KD** | `dataforseo_labs/google/keyword_overview/live` | one bulk call for all 42 keywords |

- **Market:** Canada (`location_code 2124`), **language** `en`, **device** desktop.
- **Rank = organic position** (the Nth organic result, ads/SERP-features excluded), 1–100.
  Blank `current_rank` = BBI not found in the top 100 for that keyword.
- **Keyword list is frozen in the script**, not read live from the YAML, so every weekly
  snapshot stays comparable to the baseline even if the YAML is later edited. When
  walkthrough session 2 locks more clusters, append them to `KEYWORDS` in the script and
  bump the version note.

Credentials come from `.mcp.json` (`DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`) via the
shared [`scripts/dfs_client.py`](../../../scripts/dfs_client.py) — same auth path as the
COMPETITOR-KEYWORD-RECON-1 pulls. No keys live in the script.

---

## Columns

| Column | Meaning |
|---|---|
| `keyword` | the tracked search term |
| `cluster` | which locked cluster it belongs to (`design-services`, `professional-services`, `healthcare`, `reception`, `executive-desks`, `boardroom`, `waiting-room-seating`) |
| `tier` | `primary` \| `secondary` \| `opportunistic` (role within its cluster) |
| `search_volume` | monthly CA search volume (DataForSEO Labs); blank = not in DFS DB |
| `difficulty` | keyword difficulty 0–100 (DataForSEO Labs KD); blank = not returned |
| `current_rank` | BBI organic position 1–100; **blank = not ranking in top 100** |
| `ranking_url` | the BBI page that ranks (blank if unranked) |
| `timestamp` | ISO 8601 run time (local TZ) |

---

## Running a snapshot

```bash
cd "/Users/leokatz/Desktop/Office Central"

# Weekly snapshot -> data/reports/rank-tracking/{YYYY-MM-DD}-priority-keywords.csv
python3 scripts/rank-tracking-weekly.py

# Override the date stamp (e.g. backdate / align to a Monday)
python3 scripts/rank-tracking-weekly.py --date 2026-06-08

# Baseline-suffixed file (...-priority-keywords-baseline.csv) — already run once for 2026-06-01
python3 scripts/rank-tracking-weekly.py --baseline --date 2026-06-01
```

A run takes ~1–2 min (42 sequential SERP calls + 1 bulk call) and prints a per-keyword
rank line plus the total API cost.

**Cadence:** manual, once a week (cron deferred — weekly is low-frequency enough that a
manual run is fine). Suggested: run every Monday morning and eyeball the diff vs the prior
week. The current latest snapshot is whichever dated file sorts last in this directory.

---

## Comparing two snapshots

CSVs share an identical row order (the frozen keyword list), so a plain diff is readable,
but `current_rank` is the column that matters. Quick week-over-week comparison:

```bash
cd data/reports/rank-tracking
# join two snapshots on keyword and show rank movement (old -> new)
python3 - "2026-06-01-priority-keywords-baseline.csv" "2026-06-08-priority-keywords.csv" <<'PY'
import csv, sys
def load(p):
    return {r["keyword"]: r for r in csv.DictReader(open(p))}
old, new = load(sys.argv[1]), load(sys.argv[2])
def rk(v): return int(v) if v else 101  # unranked sorts last
rows = []
for kw, n in new.items():
    o = old.get(kw, {})
    ro, rn = o.get("current_rank",""), n["current_rank"]
    delta = rk(ro) - rk(rn)  # positive = improved (moved up)
    rows.append((delta, kw, ro or "--", rn or "--"))
for delta, kw, ro, rn in sorted(rows, reverse=True):
    arrow = "UP" if delta>0 else ("DOWN" if delta<0 else "--")
    print(f"{arrow:>4} {ro:>4} -> {rn:<4}  {kw}")
PY
```

`UP` = BBI moved toward position 1 (good). A keyword going from `--` to a number means it
newly entered the top 100; the reverse means it dropped out.

---

## 2026-06-01 baseline summary

- **9 of 42** keywords rank in the top 100. The rest are not yet in the top 100 (expected —
  the site is freshly launched and climbing).
- **Where BBI already shows up:** the **healthcare** cluster (6 keywords, ranks 56–75, all on
  `/collections/healthcare-seating`) and the **boardroom** cluster (`boardroom table` #25,
  `conference table` #50, `wood boardroom table` #70).
- **Biggest open opportunities** (high volume, BBI absent from top 100): `reception desk`
  (2 900/mo), `executive desk` (1 300/mo) — both KD 0, so winnable with on-page work.
- **API cost, baseline run:** SERP `$0.5505` + overview `$0.0139` = **`$0.5644`**.

### Cost note (Phase 4 — actual vs. estimate)

The brief estimated ~`$0.001`/keyword (`~$0.20–0.32`/mo). **Actual measured cost is
~`$0.011–0.013`/keyword** because `depth=100` is required to see ranks 11–100 — and 7 of
BBI's 9 ranked keywords currently sit *below* position 25, so a shallow `depth=10` pull
(which would hit the `$0.001` estimate) would render them invisible. At depth 100:

- **Per weekly run:** ~`$0.56` (42 keywords).
- **Per month (~4.3 runs):** **~`$2.40/mo`** — still negligible.

Lever if cost ever matters: dropping `SERP_DEPTH` to 10 in the script cuts cost ~10× but
caps visibility at the top 10. Not recommended while the site is still climbing out of
page 5+.
