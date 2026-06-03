#!/usr/bin/env python3
"""PHASE 1 — Venn teardown SEO reverse-engineering (DataForSEO REST-direct).

For each of the 7 Venn /resources/ comparison URLs:
  - pull ranked keywords (Canada) the PAGE ranks for (pos<=30)
  - record keyword, volume, KD, position, ETV, and SERP features present
Writes a compact CSV + a per-URL JSON summary to data/reports/comparison-content/.
Read-only. No writes to Shopify.
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfs_client import post, LOCATION_CANADA, LANG

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "reports", "comparison-content")
RAW = os.path.join(OUT, "raw")

URLS = [
 ("credit-cards", "https://www.venn.ca/resources/easiest-business-credit-cards-to-get-in-canada"),
 ("bba-small-biz", "https://www.venn.ca/resources/best-business-bank-accounts-in-canada-for-small-business"),
 ("sole-prop",    "https://www.venn.ca/resources/best-bank-account-for-sole-proprietorships-in-canada"),
 ("no-monthly-fees","https://www.venn.ca/resources/business-bank-accounts-in-canada-with-no-monthly-fees"),
 ("online-bba",   "https://www.venn.ca/resources/best-online-business-bank-account-in-canada"),
 ("startups",     "https://www.venn.ca/resources/best-business-banking-accounts-in-canada-for-startups"),
 ("reviews-2025", "https://www.venn.ca/resources/venns-2025-reviews"),
]

def ranked_keywords(url, limit=200):
    payload = [{
        "target": url,
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "limit": limit,
        "order_by": ["ranked_serp_element.serp_item.etv,desc"],
        "filters": [["ranked_serp_element.serp_item.rank_group", "<=", 30]],
        "item_types": ["organic", "featured_snippet"],
    }]
    return post("/v3/dataforseo_labs/google/ranked_keywords/live", payload)

rows = []
summaries = []
for slug, url in URLS:
    body = ranked_keywords(url)
    json.dump(body, open(os.path.join(RAW, f"venn-ranked-{slug}.json"), "w"))
    items = []
    try:
        items = body["tasks"][0]["result"][0]["items"] or []
    except Exception as e:
        print(f"  !! {slug}: no items ({e})")
    total_etv = 0.0
    top3 = top10 = 0
    feats = {}
    for it in items:
        kd = it.get("keyword_data", {})
        ki = kd.get("keyword_info", {})
        kp = kd.get("keyword_properties", {}) or {}
        se = it.get("ranked_serp_element", {}).get("serp_item", {})
        pos = se.get("rank_group")
        etv = se.get("etv", 0) or 0
        total_etv += etv
        if pos and pos <= 3: top3 += 1
        if pos and pos <= 10: top10 += 1
        # serp features present on this keyword's SERP
        sf = se.get("rank_info", {})
        for f in (it.get("ranked_serp_element", {}).get("serp_item", {}).get("serp_item_types", []) or []):
            feats[f] = feats.get(f, 0) + 1
        rows.append({
            "page": slug,
            "keyword": kd.get("keyword"),
            "volume": ki.get("search_volume"),
            "kd": (kp.get("keyword_difficulty")),
            "cpc": ki.get("cpc"),
            "intent": (kd.get("search_intent_info", {}) or {}).get("main_intent"),
            "position": pos,
            "etv": round(etv, 1),
            "url_ranked": se.get("relative_url") or se.get("url"),
            "is_featured_snippet": se.get("type") == "featured_snippet",
        })
    # sort this page's keywords by etv for primary-query detection
    page_rows = [r for r in rows if r["page"] == slug]
    page_rows.sort(key=lambda r: (r["etv"] or 0), reverse=True)
    primary = page_rows[0] if page_rows else None
    summaries.append({
        "page": slug, "url": url,
        "kw_count_pos<=30": len(items),
        "total_etv_pos<=30": round(total_etv, 1),
        "top3": top3, "top10": top10,
        "primary_query": primary["keyword"] if primary else None,
        "primary_pos": primary["position"] if primary else None,
        "primary_vol": primary["volume"] if primary else None,
        "primary_etv": primary["etv"] if primary else None,
        "serp_feature_tally": feats,
    })
    print(f"{slug:16s} kw={len(items):4d} etv={round(total_etv,1):8.1f} top10={top10:3d} primary='{primary['keyword'] if primary else None}' (pos {primary['position'] if primary else '-'}, vol {primary['volume'] if primary else '-'})")

# write outputs
with open(os.path.join(OUT, "venn-per-url-ranked-keywords.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
json.dump(summaries, open(os.path.join(OUT, "venn-per-url-summary.json"), "w"), indent=2)
print(f"\nWROTE {len(rows)} keyword rows across {len(URLS)} pages")
print("CSV: data/reports/comparison-content/venn-per-url-ranked-keywords.csv")
