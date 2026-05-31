#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 follow-on — KEYWORD-SEED-EXPANSION.

Competitor ranked-keyword data shows what RIVALS rank for; it cannot surface BBI's
defensible-angle keywords (OECM, Eastern-Ontario geo, design/space-planning, brand-dealer)
where competitors don't compete. This pass runs DataForSEO keyword_suggestions on
BBI-positioning seed queries, dedupes, marks net-new vs the competitor set, applies the
same KEEP filter + classification, and writes an expansion CSV + summary.

Read-only. No production writes.
"""
import csv
import json
import os

from dfs_client import post, save_raw, OUT, LOCATION_CANADA, LANG
import recon_classify as C  # reuse keep() + classification helpers

DATE = open(os.path.join(OUT, ".run_date")).read().strip()

# BBI-positioning seeds grouped by defensible angle (ICP-informed)
SEEDS = {
    "geo_eastern_ontario": [
        "office furniture peterborough", "office furniture kingston ontario",
        "office furniture belleville", "office furniture cobourg", "office furniture lindsay ontario",
        "office furniture oshawa", "office furniture whitby", "office furniture durham region",
        "commercial office furniture ontario", "office furniture eastern ontario",
    ],
    "oecm_procurement": [
        "oecm office furniture", "oecm furniture supplier", "broader public sector furniture",
        "government office furniture canada", "office furniture rfp", "office furniture tender ontario",
        "municipal office furniture", "office furniture procurement",
    ],
    "design_space_planning": [
        "office space planning", "office design services", "office layout planning",
        "office fit out", "commercial interior design office", "office reconfiguration",
        "workspace planning",
    ],
    "vertical_product": [
        "healthcare furniture canada", "medical office furniture", "dental office furniture",
        "school furniture ontario", "classroom furniture canada", "library furniture",
        "law office furniture", "reception desk office",
    ],
    "brand_dealer": [
        "global furniture group dealer", "teknion dealer ontario", "keilhauer dealer",
        "ergocentric dealer", "offices to go furniture", "heartwood furniture", "obusforme chair",
        "authorized office furniture dealer",
    ],
    "service": [
        "office furniture installation ontario", "office furniture delivery", "office relocation services",
        "used office furniture removal",
    ],
    "smallbiz_persona": [
        "small office furniture", "startup office furniture", "office manager furniture",
        "business owner office setup",
    ],
}


def fetch(seed):
    raw_name = f"sugg-{seed.replace(' ', '_')[:50]}-{DATE}.json"
    raw_path = os.path.join(OUT, "raw", raw_name)
    if os.path.exists(raw_path):
        body = json.load(open(raw_path))
    else:
        body = post("/v3/dataforseo_labs/google/keyword_suggestions/live", [{
            "keyword": seed, "location_code": LOCATION_CANADA, "language_code": LANG,
            "limit": 200, "include_seed_keyword": True,
            "filters": [["keyword_info.search_volume", ">", 0]],
            "order_by": ["keyword_info.search_volume,desc"],
        }])
        save_raw(raw_name, body)
    t = (body.get("tasks") or [{}])[0]
    if t.get("status_code") != 20000:
        return [], f"status {t.get('status_code')}"
    res = t.get("result") or []
    return (res[0].get("items") or []) if res else [], None


def main():
    # competitor keyword set for net-new comparison
    comp = set()
    agg_path = os.path.join(OUT, f"competitor-keywords-aggregated-{DATE}.csv")
    if os.path.exists(agg_path):
        comp = {r["keyword"].strip().lower() for r in csv.DictReader(open(agg_path))}
    # BBI already-ranks set
    bbi = set()
    bbi_path = os.path.join(OUT, f"ranked-keywords-bbi-{DATE}.csv")
    if os.path.exists(bbi_path):
        bbi = {r["keyword"].strip().lower() for r in csv.DictReader(open(bbi_path))}

    agg = {}  # keyword -> record
    for angle, seeds in SEEDS.items():
        for seed in seeds:
            items, err = fetch(seed)
            if err:
                with open(os.path.join(OUT, "manual_review.csv"), "a", newline="") as f:
                    csv.writer(f).writerow(["seed-expansion", seed, "suggestions failed", err])
                continue
            for it in items:
                kw = (it.get("keyword") or "").strip()
                if not kw:
                    continue
                ki = it.get("keyword_info") or {}
                kp = it.get("keyword_properties") or {}
                si = it.get("search_intent_info") or {}
                sv = int(ki.get("search_volume") or 0)
                e = agg.get(kw.lower())
                if not e:
                    agg[kw.lower()] = {
                        "keyword": kw, "search_volume": sv, "cpc": ki.get("cpc") or "",
                        "competition": ki.get("competition_level") or "",
                        "keyword_difficulty": kp.get("keyword_difficulty") if kp.get("keyword_difficulty") is not None else "",
                        "search_intent": si.get("main_intent") or "",
                        "seed_angles": {angle}, "seeds": {seed},
                    }
                else:
                    e["search_volume"] = max(e["search_volume"], sv)
                    e["seed_angles"].add(angle)
                    e["seeds"].add(seed)
                    if not e["keyword_difficulty"] and kp.get("keyword_difficulty") is not None:
                        e["keyword_difficulty"] = kp.get("keyword_difficulty")

    rows = []
    for kwl, e in agg.items():
        kw = e["keyword"]
        ok, cat = C.keep(kw)
        if not ok or e["search_volume"] < 10:
            continue
        intent = C.intent_category(kw, cat)
        industry = C.bbi_industry(kw)
        tier = C.keyword_tier(kw)
        outcome = C.bbi_outcome(kw, intent)
        surfaces = C.site_surfaces(kw, intent, industry, tier)
        dband = C.difficulty_band(e["keyword_difficulty"])
        rows.append({
            "keyword": kw,
            "search_volume": e["search_volume"],
            "cpc": e["cpc"],
            "competition": e["competition"],
            "keyword_difficulty": e["keyword_difficulty"],
            "difficulty_band": dband,
            "search_intent": e["search_intent"],
            "seed_angles": ",".join(sorted(e["seed_angles"])),
            "is_net_new_vs_competitors": "TRUE" if kwl not in comp else "FALSE",
            "bbi_already_ranks": "TRUE" if kwl in bbi else "FALSE",
            "intent_category": intent,
            "bbi_industry_match": industry,
            "bbi_outcome_path": outcome,
            "keyword_tier": tier,
            "site_surface_recommendation": surfaces,
            "question_format": "TRUE" if C.is_question(kw) else "FALSE",
        })

    rows.sort(key=lambda r: -r["search_volume"])
    out_csv = os.path.join(OUT, f"bbi-seed-expansion-{DATE}.csv")
    cols = ["keyword", "search_volume", "cpc", "competition", "keyword_difficulty", "difficulty_band",
            "search_intent", "seed_angles", "is_net_new_vs_competitors", "bbi_already_ranks",
            "intent_category", "bbi_industry_match", "bbi_outcome_path", "keyword_tier",
            "site_surface_recommendation", "question_format"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    stats = {
        "total_seeds": sum(len(v) for v in SEEDS.values()),
        "expansion_kept": len(rows),
        "net_new_vs_competitors": sum(1 for r in rows if r["is_net_new_vs_competitors"] == "TRUE"),
        "bbi_already_ranks": sum(1 for r in rows if r["bbi_already_ranks"] == "TRUE"),
    }
    json.dump(stats, open(os.path.join(OUT, "raw", f"expansion-stats-{DATE}.json"), "w"))


if __name__ == "__main__":
    main()
