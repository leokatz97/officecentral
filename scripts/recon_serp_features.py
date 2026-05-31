#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 — Phase 2.5 SERP-feature enrichment.

For the top-30 aggregated keywords: pull live Google CA SERP and capture PAA questions,
featured snippet (owner + content), AI Overview presence, local pack, knowledge panel.
For geo keywords: capture local pack presence + top-3 businesses.

Outputs:
  serp-features-top30-{date}.csv
  geo-local-pack-{date}.csv
  raw/serp-features-merge-{date}.json   (keyword.lower -> flags for Phase 4 merge)
"""
import csv
import json
import os

from dfs_client import post, save_raw, OUT, LOCATION_CANADA, LANG

DATE = open(os.path.join(OUT, ".run_date")).read().strip()

HIGH_AUTHORITY = ["wikipedia.org", ".gov", "gc.ca", "ontario.ca", "canada.ca", "britannica.com",
                  "merriam-webster.com", "dictionary.com", "youtube.com", "reddit.com",
                  "thespruce.com", "wikihow.com"]


def is_high_authority(owner):
    o = (owner or "").lower()
    return any(h in o for h in HIGH_AUTHORITY)


def pull_serp(keyword):
    raw_name = f"serp-{keyword.replace('/', '_').replace(' ', '_')[:50]}-{DATE}.json"
    raw_path = os.path.join(OUT, "raw", raw_name)
    if os.path.exists(raw_path):
        return json.load(open(raw_path))
    body = post("/v3/serp/google/organic/live/advanced", [{
        "keyword": keyword, "location_code": LOCATION_CANADA, "language_code": LANG,
        "depth": 20, "people_also_ask_click_depth": 2,
    }])
    save_raw(raw_name, body)
    return body


def parse(body):
    out = {"paa": [], "fs_present": "N", "fs_owner": "", "fs_content": "",
           "ai_present": "N", "lp_present": "N", "lp_top3": [], "kp_present": "N"}
    tasks = body.get("tasks") or [{}]
    res = (tasks[0].get("result") or [{}])
    items = res[0].get("items") or [] if res else []
    for it in items:
        t = it.get("type")
        if t == "people_also_ask":
            for el in it.get("items") or []:
                q = el.get("title")
                if q:
                    out["paa"].append(q)
        elif t == "featured_snippet":
            out["fs_present"] = "Y"
            out["fs_owner"] = it.get("domain", "")
            txt = ""
            for fld in ("description", "title"):
                if it.get(fld):
                    txt = it[fld]; break
            if not txt:
                # try table/list content
                txt = json.dumps(it.get("table") or it.get("items") or "")[:200]
            out["fs_content"] = (txt or "")[:200]
        elif t in ("ai_overview", "ai_overview_reference"):
            out["ai_present"] = "Y"
        elif t == "local_pack":
            out["lp_present"] = "Y"
            ttl = it.get("title")
            if ttl and len(out["lp_top3"]) < 3:
                out["lp_top3"].append(ttl)
        elif t in ("knowledge_graph",):
            out["kp_present"] = "Y"
    return out


def main():
    top30 = json.load(open(os.path.join(OUT, f"top30-keywords-{DATE}.json")))
    geo = json.load(open(os.path.join(OUT, f"geo-keywords-{DATE}.json")))

    merge = {}
    rows = []
    for kw in top30:
        try:
            p = parse(pull_serp(kw))
        except Exception as e:
            with open(os.path.join(OUT, "manual_review.csv"), "a", newline="") as f:
                csv.writer(f).writerow(["phase2.5", kw, "serp pull failed", str(e)[:120]])
            continue
        fs_opp = "TRUE" if (p["fs_present"] == "Y" and not is_high_authority(p["fs_owner"])) else "FALSE"
        merge[kw.lower()] = {
            "featured_snippet_opportunity": fs_opp,
            "ai_overview_present": "TRUE" if p["ai_present"] == "Y" else "FALSE",
        }
        rows.append({
            "keyword": kw,
            "paa_questions": json.dumps(p["paa"]),
            "featured_snippet_present": p["fs_present"],
            "featured_snippet_owner": p["fs_owner"],
            "featured_snippet_content": p["fs_content"],
            "ai_overview_present": p["ai_present"],
            "local_pack_present": p["lp_present"],
            "local_pack_top3": json.dumps(p["lp_top3"]),
            "knowledge_panel_present": p["kp_present"],
            "featured_snippet_opportunity": fs_opp,
        })

    with open(os.path.join(OUT, f"serp-features-top30-{DATE}.csv"), "w", newline="") as f:
        cols = ["keyword", "paa_questions", "featured_snippet_present", "featured_snippet_owner",
                "featured_snippet_content", "ai_overview_present", "local_pack_present",
                "local_pack_top3", "knowledge_panel_present", "featured_snippet_opportunity"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    # geo local pack pass
    geo_rows = []
    for kw in geo:
        try:
            p = parse(pull_serp(kw))
        except Exception as e:
            with open(os.path.join(OUT, "manual_review.csv"), "a", newline="") as f:
                csv.writer(f).writerow(["phase2.5-geo", kw, "serp pull failed", str(e)[:120]])
            continue
        geo_rows.append({
            "keyword": kw,
            "local_pack_present": p["lp_present"],
            "local_pack_top3": json.dumps(p["lp_top3"]),
            "ai_overview_present": p["ai_present"],
            "featured_snippet_owner": p["fs_owner"],
        })
        # also feed AI overview flag into merge for geo keywords
        merge.setdefault(kw.lower(), {})["ai_overview_present"] = "TRUE" if p["ai_present"] == "Y" else "FALSE"

    with open(os.path.join(OUT, f"geo-local-pack-{DATE}.csv"), "w", newline="") as f:
        cols = ["keyword", "local_pack_present", "local_pack_top3", "ai_overview_present", "featured_snippet_owner"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(geo_rows)

    save_raw(f"serp-features-merge-{DATE}.json", merge)
    print(f"Top30 SERP enriched: {len(rows)}  | geo local-pack: {len(geo_rows)}  | merge keys: {len(merge)}")


if __name__ == "__main__":
    main()
