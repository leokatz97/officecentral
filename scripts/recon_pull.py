#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 — Phases 1-3 data pulls (DataForSEO Labs REST).

Phase 1: relevant_pages (Domain Pages) top 100 by traffic per competitor.
Phase 2: ranked_keywords pos 1-50, Canada, top 1000 by traffic per competitor.
Phase 3: ranked_keywords baseline for BBI + Office Central.

Resumable: skips a pull whose raw JSON already exists. Edge cases -> manual_review.csv.
"""
import csv
import json
import os
import sys

from dfs_client import post, save_raw, RAW, OUT, LOCATION_CANADA, LANG

DATE = open(os.path.join(OUT, ".run_date")).read().strip()

# Final set after Ontario-priority discovery (2026-05-30):
# Original shaw-furniture.com / furniture-options.ca returned ZERO Canada rankings
# (logged to manual_review). Replaced + expanded with Ontario Tier-1 dealers — discovered
# via competitors_domain + Leo's Maps/SERP list, each verified to have ranking data.
COMPETITORS = [
    # --- Ontario Tier-1 (Leo's priority) ---
    "sourceofficefurniture.ca",      # Toronto/Mississauga/Brampton + national ~4390 kw
    "atwork.ca",                     # Toronto, ON — HON dealer ~3282 kw
    "mapofficefurniture.com",        # Toronto, ON — new/used ~1788 kw
    "officestock.com",               # Toronto/GTA, ON — modern ~1394 kw
    "barrysofficefurniture.com",     # North York / Toronto, ON ~1308 kw
    "grandandtoy.com",               # Vaughan, ON HQ — national institutional/BPS ~13196 kw
    "theofficeshop.ca",              # Toronto/Markham/Miss/Brampton/Vaughan ~909 kw
    "poi.ca",                        # Mississauga, ON — POI Business Interiors ~255 kw
    "vaughanofficefurniture.com",    # Vaughan, ON ~201 kw
    "newmarketofficefurniture.com",  # Newmarket, ON ~115 kw
    # --- Non-Ontario (original, kept for breadth) ---
    "ugoburo.ca",                    # QC ~1000 kw
    "monk.ca",                       # Victoria, BC ~1000 kw
]
# Province tags for the summary report
PROVINCE = {
    "sourceofficefurniture.ca": "ON+national", "atwork.ca": "ON", "mapofficefurniture.com": "ON",
    "officestock.com": "ON", "barrysofficefurniture.com": "ON", "grandandtoy.com": "ON(HQ)+national",
    "theofficeshop.ca": "ON", "poi.ca": "ON", "vaughanofficefurniture.com": "ON",
    "newmarketofficefurniture.com": "ON", "ugoburo.ca": "QC", "monk.ca": "BC",
}
# Dropped (no Canada ranking data): shaw-furniture.com, furniture-options.ca
BASELINES = {"bbi": "brantbusinessinteriors.com", "officecentral": "officecentral.ca"}

MR_PATH = os.path.join(OUT, "manual_review.csv")


def log_manual(stage, target, reason, detail=""):
    new = not os.path.exists(MR_PATH)
    with open(MR_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["stage", "target", "reason", "detail"])
        w.writerow([stage, target, reason, detail])


def get_result_items(body):
    tasks = body.get("tasks") or []
    if not tasks:
        return None, "no tasks in response"
    t = tasks[0]
    if t.get("status_code") != 20000:
        return None, f"task status {t.get('status_code')} {t.get('status_message')}"
    res = t.get("result") or []
    if not res:
        return [], "empty result"
    items = res[0].get("items") or []
    return items, None


# ---------- Phase 1: Domain Pages (relevant_pages) ----------
def pull_domain_pages(domain):
    raw_name = f"domain-pages-{domain}-{DATE}.json"
    raw_path = os.path.join(RAW, raw_name)
    if os.path.exists(raw_path):
        body = json.load(open(raw_path))
    else:
        payload = [{
            "target": domain,
            "location_code": LOCATION_CANADA,
            "language_code": LANG,
            "limit": 100,
            "order_by": ["metrics.organic.etv,desc"],
        }]
        body = post("/v3/dataforseo_labs/google/relevant_pages/live", payload)
        save_raw(raw_name, body)
    items, err = get_result_items(body)
    if items is None:
        log_manual("phase1", domain, "relevant_pages failed", err)
        print(f"  [P1] {domain}: FAILED ({err})")
        return 0
    rows = []
    for it in items:
        m = (it.get("metrics") or {}).get("organic") or {}
        rows.append({
            "page_url": it.get("page_address", ""),
            "etv": m.get("etv", 0),
            "organic_keywords_count": m.get("count", 0),
            "pos_1": m.get("pos_1", 0),
            "pos_2_3": m.get("pos_2_3", 0),
            "pos_4_10": m.get("pos_4_10", 0),
            "impressions_etv": m.get("impressions_etv", 0),
        })
    csv_path = os.path.join(OUT, f"top-pages-{domain}-{DATE}.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ["page_url", "etv", "organic_keywords_count", "pos_1", "pos_2_3", "pos_4_10", "impressions_etv"])
        w.writeheader()
        w.writerows(rows)
    print(f"  [P1] {domain}: {len(rows)} pages -> {os.path.basename(csv_path)}")
    return len(rows)


# ---------- Phase 2/3: Ranked Keywords ----------
def pull_ranked_keywords(target, out_basename, label):
    raw_name = f"ranked-{out_basename}-{DATE}.json"
    raw_path = os.path.join(RAW, raw_name)
    if os.path.exists(raw_path):
        body = json.load(open(raw_path))
    else:
        payload = [{
            "target": target,
            "location_code": LOCATION_CANADA,
            "language_code": LANG,
            "limit": 1000,
            "filters": [["ranked_serp_element.serp_item.rank_absolute", "<=", 50]],
            "order_by": ["ranked_serp_element.serp_item.etv,desc"],
        }]
        body = post("/v3/dataforseo_labs/google/ranked_keywords/live", payload)
        save_raw(raw_name, body)
    items, err = get_result_items(body)
    if items is None:
        log_manual("ranked", target, "ranked_keywords failed", err)
        print(f"  [{label}] {target}: FAILED ({err})")
        return 0
    rows = []
    for it in items:
        kd = it.get("keyword_data") or {}
        kw = kd.get("keyword", "")
        ki = kd.get("keyword_info") or {}
        kp = kd.get("keyword_properties") or {}
        si = (kd.get("search_intent_info") or {})
        rse = (it.get("ranked_serp_element") or {}).get("serp_item") or {}
        rows.append({
            "keyword": kw,
            "search_volume": ki.get("search_volume", 0) or 0,
            "cpc": ki.get("cpc", 0) or 0,
            "competition": ki.get("competition_level", "") or "",
            "keyword_difficulty": kp.get("keyword_difficulty", "") if kp.get("keyword_difficulty") is not None else "",
            "search_intent": si.get("main_intent", "") or "",
            "rank_absolute": rse.get("rank_absolute", ""),
            "rank_group": rse.get("rank_group", ""),
            "etv": rse.get("etv", 0) or 0,
            "url": rse.get("url", "") or "",
            "serp_type": rse.get("type", "") or "",
            "source_domain": target,
        })
    csv_path = os.path.join(OUT, f"ranked-keywords-{out_basename}-{DATE}.csv")
    with open(csv_path, "w", newline="") as f:
        cols = ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty",
                "search_intent", "rank_absolute", "rank_group", "etv", "url", "serp_type", "source_domain"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"  [{label}] {target}: {len(rows)} keywords -> {os.path.basename(csv_path)}")
    return len(rows)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "p1"):
        print("PHASE 1 — Domain Pages")
        for d in COMPETITORS:
            try:
                pull_domain_pages(d)
            except Exception as e:
                log_manual("phase1", d, "exception", str(e)[:200])
                print(f"  [P1] {d}: EXCEPTION {e}")
    if which in ("all", "p2"):
        print("PHASE 2 — Ranked Keywords (competitors)")
        for d in COMPETITORS:
            try:
                pull_ranked_keywords(d, d, "P2")
            except Exception as e:
                log_manual("phase2", d, "exception", str(e)[:200])
                print(f"  [P2] {d}: EXCEPTION {e}")
    if which in ("all", "p3"):
        print("PHASE 3 — Baselines")
        for key, dom in BASELINES.items():
            try:
                pull_ranked_keywords(dom, key, "P3")
            except Exception as e:
                log_manual("phase3", dom, "exception", str(e)[:200])
                print(f"  [P3] {dom}: EXCEPTION {e}")
    print("DONE", which)


if __name__ == "__main__":
    main()
