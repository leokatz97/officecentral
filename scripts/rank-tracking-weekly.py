#!/usr/bin/env python3
"""PHASE-C-STREAM-C — DataForSEO weekly rank tracking for priority-keywords.yaml v1.

Re-runs the LOCKED v1 priority-keyword list against DataForSEO each week and records
where brantbusinessinteriors.com currently ranks in Canadian Google organic results.

Two API calls power each snapshot:
  1. serp/google/organic/live/advanced  -> current organic rank (1-100) + ranking URL
  2. dataforseo_labs/google/keyword_overview/live -> search volume + keyword difficulty (KD)

Market : Canada (location_code 2124), language en
Target : brantbusinessinteriors.com
Output : data/reports/rank-tracking/{YYYY-MM-DD}-priority-keywords.csv
         (pass --baseline to suffix the filename ...-baseline.csv)

The keyword list is the frozen v1 lock from data/reference/priority-keywords.yaml
(4 locked clusters: design-services hub, professional-services + healthcare spokes,
4 collection funnels). Re-locking the list here keeps every weekly snapshot comparable
to the baseline regardless of later edits to the yaml. When walkthrough session 2
locks more clusters, append them to KEYWORDS below and note the version bump.

Read-only against Shopify/the site; the only network writes are paid DataForSEO SERP
pulls (~$0.001/keyword). The only filesystem write is the local CSV.

Usage:
    export $(grep -v '^#' .env | xargs) 2>/dev/null   # not required; creds come from .mcp.json
    python3 scripts/rank-tracking-weekly.py            # dated weekly snapshot
    python3 scripts/rank-tracking-weekly.py --baseline # baseline-suffixed snapshot
    python3 scripts/rank-tracking-weekly.py --date 2026-06-08   # override run date
"""
import csv
import os
import sys
import time
from datetime import datetime, timezone

# Reuse the tested REST client (auth from .mcp.json -> DATAFORSEO_USERNAME/PASSWORD).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfs_client import post  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "reports", "rank-tracking")
os.makedirs(OUT_DIR, exist_ok=True)

LOCATION_CODE = 2124      # Canada
LANGUAGE = "en"
TARGET_DOMAIN = "brantbusinessinteriors.com"
SERP_DEPTH = 100          # capture rank 1-100

SERP_PATH = "/v3/serp/google/organic/live/advanced"
OVERVIEW_PATH = "/v3/dataforseo_labs/google/keyword_overview/live"

# --- LOCKED v1 priority keywords (priority-keywords.yaml v1, 2026-05-31) ---
# (keyword, cluster, tier)  tier in {primary, secondary, opportunistic}
KEYWORDS = [
    # cluster 1 — design-services (hub)
    ("office space planning",                "design-services",       "primary"),
    ("space planning office",                "design-services",       "secondary"),
    ("space planning for office",            "design-services",       "secondary"),
    ("office layout planning",               "design-services",       "secondary"),
    ("workspace planning",                   "design-services",       "secondary"),
    ("office design services",               "design-services",       "secondary"),
    ("office interior design services",      "design-services",       "secondary"),
    ("office reconfiguration",               "design-services",       "secondary"),
    ("office floor plan",                    "design-services",       "opportunistic"),
    # cluster 2 — professional-services (spoke)
    ("law firm office furniture",            "professional-services", "primary"),
    ("law office furniture",                 "professional-services", "secondary"),
    ("accounting office furniture",          "professional-services", "secondary"),
    ("insurance office furniture",           "professional-services", "secondary"),
    ("financial services office design",     "professional-services", "secondary"),
    ("consulting office furniture",          "professional-services", "secondary"),
    # cluster 3 — healthcare (spoke)
    ("healthcare furniture canada",          "healthcare",            "primary"),
    ("healthcare furniture",                 "healthcare",            "secondary"),
    ("furniture healthcare",                 "healthcare",            "secondary"),
    ("medical furnitures",                   "healthcare",            "secondary"),
    ("medical office furniture",             "healthcare",            "secondary"),
    ("furniture for medical office",         "healthcare",            "secondary"),
    ("dental office furniture",              "healthcare",            "secondary"),
    # cluster 4a — reception (collection funnel)
    ("reception desk",                       "reception",             "primary"),
    ("l-shaped reception desk",              "reception",             "secondary"),
    ("reception desk canada",                "reception",             "secondary"),
    ("small reception desk",                 "reception",             "secondary"),
    ("modern reception desk",                "reception",             "secondary"),
    ("reception desk for sale",              "reception",             "secondary"),
    # cluster 4b — executive-desks (collection funnel)
    ("executive desk",                       "executive-desks",       "primary"),
    ("executive office desk",                "executive-desks",       "secondary"),
    ("l-shaped executive desk",              "executive-desks",       "secondary"),
    ("executive desk canada",                "executive-desks",       "secondary"),
    ("modern executive desk",                "executive-desks",       "secondary"),
    ("wood executive desk",                  "executive-desks",       "secondary"),
    # cluster 4c — boardroom (collection funnel)
    ("boardroom table",                      "boardroom",             "primary"),
    ("conference table",                     "boardroom",             "secondary"),
    ("wood boardroom table",                 "boardroom",             "secondary"),
    ("conference table canada",              "boardroom",             "secondary"),
    ("modular conference table",             "boardroom",             "secondary"),
    ("conference table with chairs",         "boardroom",             "secondary"),
    # cluster 4d — waiting-room-seating (collection funnel)
    ("office chairs for waiting room",       "waiting-room-seating",  "primary"),
    ("waiting room chairs canada",           "waiting-room-seating",  "secondary"),
]


def _digint(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def fetch_serp_rank(keyword):
    """Return (organic_rank|None, ranking_url|None, cost) for TARGET_DOMAIN."""
    payload = [{
        "keyword": keyword,
        "location_code": LOCATION_CODE,
        "language_code": LANGUAGE,
        "device": "desktop",
        "depth": SERP_DEPTH,
    }]
    body = post(SERP_PATH, payload)
    cost = body.get("cost") or 0.0
    tasks = body.get("tasks") or []
    if not tasks or not tasks[0].get("result"):
        return None, None, cost
    items = (tasks[0]["result"][0] or {}).get("items") or []
    organic_pos = 0
    for it in items:
        if it.get("type") != "organic":
            continue
        organic_pos += 1
        dom = (it.get("domain") or "").lower()
        url = (it.get("url") or "").lower()
        if TARGET_DOMAIN in dom or TARGET_DOMAIN in url:
            return organic_pos, it.get("url"), cost
    return None, None, cost


def fetch_overview(keywords):
    """Bulk volume + KD. Return ({kw_lower: (volume, kd)}, cost)."""
    payload = [{
        "keywords": keywords,
        "location_code": LOCATION_CODE,
        "language_code": LANGUAGE,
    }]
    body = post(OVERVIEW_PATH, payload)
    cost = body.get("cost") or 0.0
    out = {}
    tasks = body.get("tasks") or []
    if not tasks or not tasks[0].get("result"):
        return out, cost
    items = (tasks[0]["result"][0] or {}).get("items") or []
    for it in items:
        kw = (it.get("keyword") or "").lower()
        ki = it.get("keyword_info") or {}
        kp = it.get("keyword_properties") or {}
        vol = _digint(ki.get("search_volume"))
        kd = _digint(kp.get("keyword_difficulty"))
        out[kw] = (vol, kd)
    return out, cost


def main():
    args = sys.argv[1:]
    baseline = "--baseline" in args
    run_date = None
    if "--date" in args:
        run_date = args[args.index("--date") + 1]
    if not run_date:
        run_date = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")

    suffix = "-priority-keywords-baseline.csv" if baseline else "-priority-keywords.csv"
    out_path = os.path.join(OUT_DIR, run_date + suffix)
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    print(f"Rank tracking run {run_date} ({'BASELINE' if baseline else 'weekly'})")
    print(f"  market=Canada(2124) lang=en target={TARGET_DOMAIN} keywords={len(KEYWORDS)}")

    # 1) bulk volume + KD (one call)
    print("Fetching search volume + KD (keyword_overview)...")
    overview, ov_cost = fetch_overview([k for k, _, _ in KEYWORDS])
    print(f"  overview returned {len(overview)} keywords  cost=${ov_cost:.4f}")

    # 2) per-keyword SERP rank
    rows = []
    serp_cost = 0.0
    ranked = 0
    for i, (kw, cluster, tier) in enumerate(KEYWORDS, 1):
        rank, url, cost = fetch_serp_rank(kw)
        serp_cost += cost
        vol, kd = overview.get(kw.lower(), (None, None))
        if rank is not None:
            ranked += 1
        print(f"  [{i:>2}/{len(KEYWORDS)}] {kw:<34} rank={rank if rank else '--':<4} "
              f"vol={vol if vol is not None else '?':<6} kd={kd if kd is not None else '?'}")
        rows.append({
            "keyword": kw,
            "cluster": cluster,
            "tier": tier,
            "search_volume": vol if vol is not None else "",
            "difficulty": kd if kd is not None else "",
            "current_rank": rank if rank is not None else "",
            "ranking_url": url or "",
            "timestamp": ts,
        })
        time.sleep(0.3)  # gentle pacing

    cols = ["keyword", "cluster", "tier", "search_volume", "difficulty",
            "current_rank", "ranking_url", "timestamp"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    total_cost = serp_cost + ov_cost
    print("-" * 60)
    print(f"Wrote {len(rows)} rows -> {os.path.relpath(out_path, ROOT)}")
    print(f"Ranking in top {SERP_DEPTH}: {ranked}/{len(KEYWORDS)} keywords")
    print(f"API cost this run: SERP=${serp_cost:.4f} + overview=${ov_cost:.4f} "
          f"= ${total_cost:.4f}")


if __name__ == "__main__":
    main()
