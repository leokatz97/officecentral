#!/usr/bin/env python3
"""KEYWORD-SEED-EXPANSION — summary generator.

Reads bbi-seed-expansion-{date}.csv and writes SEED-EXPANSION-SUMMARY-{date}.md.
Focus: net-new BBI-positioning keywords competitors do NOT rank for, by defensible angle.
Pure file I/O.
"""
import csv
import os
from collections import Counter

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(OUT, "data", "reports", "keyword-research")
DATE = open(os.path.join(OUT, ".run_date")).read().strip()

ANGLES = ["geo_eastern_ontario", "oecm_procurement", "design_space_planning",
          "vertical_product", "brand_dealer", "service", "smallbiz_persona"]


def iv(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


def main():
    rows = list(csv.DictReader(open(os.path.join(OUT, f"bbi-seed-expansion-{DATE}.csv"))))
    net_new = [r for r in rows if r["is_net_new_vs_competitors"] == "TRUE"]

    L = []
    w = L.append
    w("KEYWORD-SEED-EXPANSION SUMMARY")
    w(f"Date: {DATE}  |  Branch: feature/competitor-keyword-recon-1")
    w("Follow-on to COMPETITOR-KEYWORD-RECON-1. DataForSEO keyword_suggestions run on")
    w("BBI-positioning seeds across 7 defensible angles. Read-only; no production writes.")
    w("")
    w("=== COVERAGE ===")
    w(f"Expansion keywords kept (sv>=10, KEEP-filtered): {len(rows)}")
    w(f"NET-NEW vs competitor set (competitors do NOT rank for these): {len(net_new)}")
    w(f"  -> these are BBI's clearest whitespace — own them before rivals do.")
    w(f"Already in competitor set (validation overlap): {len(rows)-len(net_new)}")
    w(f"BBI already ranks for: {sum(1 for r in rows if r['bbi_already_ranks']=='TRUE')}")
    w("")

    w("=== BY DEFENSIBLE ANGLE (net-new count | total volume) ===")
    for a in ANGLES:
        rs = [r for r in net_new if a in r["seed_angles"].split(",")]
        w(f"  {a}: {len(rs)} net-new | volume {sum(iv(r['search_volume']) for r in rs):,}")
    w("")

    for a in ANGLES:
        rs = sorted([r for r in net_new if a in r["seed_angles"].split(",")],
                    key=lambda r: -iv(r["search_volume"]))
        if not rs:
            continue
        w(f"=== TOP NET-NEW: {a} ===")
        for r in rs[:20]:
            w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['difficulty_band'] or '?'}, "
              f"{r['intent_category']}, surfaces:{r['site_surface_recommendation']})")
        w("")

    w("=== QUICK WINS (net-new, easy difficulty, by volume) ===")
    qw = sorted([r for r in net_new if r["difficulty_band"] == "easy"], key=lambda r: -iv(r["search_volume"]))[:30]
    for r in qw:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']}, {r['seed_angles']})")
    w("")

    w("=== FAQ / QUESTION-FORMAT CANDIDATES (net-new) ===")
    qf = sorted([r for r in net_new if r["question_format"] == "TRUE"], key=lambda r: -iv(r["search_volume"]))[:25]
    if qf:
        for r in qf:
            w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo)")
    else:
        w("    (none — expansion seeds were commercial; pull PAA from RECON-1 for FAQ)")
    w("")

    w("=== INTENT DISTRIBUTION (net-new) ===")
    ic = Counter(r["intent_category"] for r in net_new)
    for k, v in ic.most_common():
        w(f"  {k}: {v}")
    w("")

    w("=== OUTCOME PATH (net-new) ===")
    oc = Counter(r["bbi_outcome_path"] for r in net_new)
    for k, v in oc.most_common():
        w(f"  {k}: {v}")
    w("")

    w("=== NEXT ACTION ===")
    w("  1. Review net-new keywords by angle — these don't appear in competitor rankings.")
    w("  2. In ICP-KEYWORD-WALKTHROUGH, prioritize: geo_eastern_ontario + oecm_procurement +")
    w("     design_space_planning (BBI's three strongest moats, thinnest competitor coverage).")
    w("  3. Map quick-wins to pages (geo_page / oecm_page / service_page) for the content plan.")

    open(os.path.join(OUT, f"SEED-EXPANSION-SUMMARY-{DATE}.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
