#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 — Phase 5 summary report generator.

Reads the aggregated CSV + SERP-feature CSV + per-domain ranked CSVs and writes
SUMMARY-{date}.md. Pure file I/O (no reliance on stdout).
"""
import csv
import glob
import json
import os
from collections import Counter

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(OUT, "data", "reports", "keyword-research")
DATE = open(os.path.join(OUT, ".run_date")).read().strip()

PROVINCE = {
    "sourceofficefurniture.ca": "ON+national", "atwork.ca": "ON", "mapofficefurniture.com": "ON",
    "officestock.com": "ON", "barrysofficefurniture.com": "ON", "grandandtoy.com": "ON(HQ)+national",
    "theofficeshop.ca": "ON", "poi.ca": "ON", "vaughanofficefurniture.com": "ON",
    "newmarketofficefurniture.com": "ON", "ugoburo.ca": "QC", "monk.ca": "BC",
}


def load(p):
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def iv(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


def fv(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    agg = load(os.path.join(OUT, f"competitor-keywords-aggregated-{DATE}.csv"))
    bbi = load(os.path.join(OUT, f"ranked-keywords-bbi-{DATE}.csv"))
    serp = load(os.path.join(OUT, f"serp-features-top30-{DATE}.csv"))
    geo = load(os.path.join(OUT, f"geo-local-pack-{DATE}.csv"))
    mr = load(os.path.join(OUT, "manual_review.csv"))

    comp_counts = {}
    for fp in glob.glob(os.path.join(OUT, f"ranked-keywords-*-{DATE}.csv")):
        base = os.path.basename(fp)
        if base.startswith(("ranked-keywords-bbi", "ranked-keywords-officecentral")):
            continue
        dom = base[len("ranked-keywords-"):-(len(DATE) + 5)]
        comp_counts[dom] = sum(1 for _ in csv.DictReader(open(fp)))

    L = []
    w = L.append
    w("COMPETITOR-KEYWORD-RECON-1 REPORT")
    w(f"Date: {DATE}")
    w("Branch: feature/competitor-keyword-recon-1")
    w("")
    files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(OUT, "*.csv")))
    w("Files generated (CSVs gitignored; this summary committed):")
    for f in files:
        w(f"  - {f}")
    w(f"  - SUMMARY-{DATE}.md")
    w("")

    # ===== COVERAGE =====
    w("=== COVERAGE ===")
    w(f"Competitors analyzed: {len(comp_counts)} (10 Ontario-priority + QC + BC)")
    for dom in sorted(comp_counts, key=lambda d: -comp_counts[d]):
        w(f"  - {dom} [{PROVINCE.get(dom,'?')}]: {comp_counts[dom]} ranked kw (pos 1-50)")
    w(f"Competitor keywords aggregated (post-filter, deduped, sv>=10): {len(agg)}")
    w(f"BBI baseline ranked keywords: {len(bbi)}")
    w("Office Central baseline ranked keywords: 0 (no Canada rankings — parent site minimal SEO footprint)")
    w(f"Top 30 enriched with PAA + SERP features: YES ({len(serp)} keywords)")
    w(f"Geo keywords checked for local pack: {len(geo)}")
    w(f"Edge cases for manual review: {len([r for r in mr if r.get('stage')])}")
    w("")

    # ===== TIER DISTRIBUTION =====
    w("=== TIER DISTRIBUTION (head/mid/long-tail) ===")
    for tier in ("head", "mid", "long_tail"):
        rows = [r for r in agg if r["keyword_tier"] == tier]
        vol = sum(iv(r["search_volume"]) for r in rows)
        diffs = [fv(r["keyword_difficulty"]) for r in rows if fv(r["keyword_difficulty"]) is not None]
        avg = round(sum(diffs) / len(diffs), 1) if diffs else "n/a"
        w(f"  {tier}: {len(rows)} kw | total volume {vol:,} | avg difficulty {avg}")
    w("")

    # ===== INTENT x TIER MATRIX =====
    w("=== INTENT x TIER MATRIX (count | volume) ===")
    intents = ["vendor_relationship", "compliance_certification", "procurement_process",
               "use_case_vertical", "geographic", "informational", "service",
               "design_service", "product_generic", "manual_review"]
    tiers = ["head", "mid", "long_tail"]
    w(f"  {'intent_category':<26} " + " ".join(f"{t:>18}" for t in tiers))
    for it in intents:
        cells = []
        for t in tiers:
            rs = [r for r in agg if r["intent_category"] == it and r["keyword_tier"] == t]
            cells.append(f"{len(rs)}|{sum(iv(r['search_volume']) for r in rs):,}")
        w(f"  {it:<26} " + " ".join(f"{c:>18}" for c in cells))
    w("")
    lt = sorted([r for r in agg if r["keyword_tier"] == "long_tail"], key=lambda r: -iv(r["search_volume"]))[:12]
    w("  Highest-volume long-tail (blog/FAQ/cluster targets):")
    for r in lt:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']}, {r['difficulty_band'] or '?'})")
    head = sorted([r for r in agg if r["keyword_tier"] == "head"], key=lambda r: -iv(r["search_volume"]))[:10]
    w("  Highest-volume head terms (homepage/collection, hard to win):")
    for r in head:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['difficulty_band'] or '?'})")
    w("")

    # ===== SITE SURFACE DISTRIBUTION =====
    w("=== SITE SURFACE DISTRIBUTION ===")
    surf = Counter()
    for r in agg:
        for s in r["site_surface_recommendation"].split(","):
            if s:
                surf[s] += 1
    for s in ["pdp", "brand_page", "collection_page", "industry_page", "oecm_page",
              "service_page", "faq", "blog", "pillar_page", "cluster_page", "geo_page", "homepage"]:
        w(f"  {s}: {surf.get(s,0)}")
    w("")

    # ===== OUTCOME PATH =====
    w("=== BBI OUTCOME PATH DISTRIBUTION ===")
    for path in ["quote-request", "ecom-purchase", "design-consultation", "multi-outcome", "informational-only"]:
        rs = [r for r in agg if r["bbi_outcome_path"] == path]
        w(f"  {path}: {len(rs)} kw | total volume {sum(iv(r['search_volume']) for r in rs):,}")
    w("")

    # ===== INDUSTRY MATCH =====
    w("=== BBI INDUSTRY MATCH ===")
    for ind in ["healthcare", "education", "government", "non-profit", "professional-services",
                "multi-industry", "not-applicable"]:
        rs = [r for r in agg if r["bbi_industry_match"] == ind]
        w(f"  {ind}: {len(rs)} kw | volume {sum(iv(r['search_volume']) for r in rs):,}")
    w("")

    # ===== DIFFICULTY x VOLUME OPPORTUNITY =====
    w("=== DIFFICULTY x VOLUME OPPORTUNITY MAP ===")
    commercial = {"product_generic", "vendor_relationship", "procurement_process",
                  "use_case_vertical", "geographic", "design_service", "service",
                  "compliance_certification"}
    def band(r, b):
        return r["difficulty_band"] == b and r["intent_category"] in commercial
    qw = sorted([r for r in agg if band(r, "easy")], key=lambda r: -iv(r["search_volume"]))[:20]
    w("  Quick wins (easy difficulty, commercial intent, by volume):")
    for r in qw:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']}, surfaces:{r['site_surface_recommendation']})")
    mt = sorted([r for r in agg if band(r, "medium")], key=lambda r: -iv(r["search_volume"]))[:20]
    w("  Medium-term targets (medium difficulty):")
    for r in mt:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']})")
    lh = sorted([r for r in agg if band(r, "hard")], key=lambda r: -iv(r["search_volume"]))[:10]
    w("  Long-horizon plays (hard difficulty, pillar only):")
    for r in lh:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']})")
    w("")

    # ===== FAQ + AI OVERVIEW =====
    w("=== FAQ + AI OVERVIEW TARGETS ===")
    qf = sorted([r for r in agg if r["question_format"] == "TRUE"], key=lambda r: -iv(r["search_volume"]))[:30]
    w("  Question-format keywords (FAQ candidates, top 30 by volume):")
    for r in qf:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo)")
    ai = [r for r in serp if r.get("ai_overview_present") == "Y"]
    w(f"  AI Overview-triggering queries (from top 30): {len(ai)}")
    for r in ai:
        w(f"    - {r['keyword']}")
    if not ai:
        w("    (none detected among top 30 commercial queries — AI Overviews rarely fire on transactional product SERPs)")
    paa = []
    for r in serp:
        try:
            paa.extend(json.loads(r.get("paa_questions") or "[]"))
        except json.JSONDecodeError:
            pass
    seen = set()
    uniq = [q for q in paa if not (q in seen or seen.add(q))]
    w(f"  PAA questions surfaced (top {min(50,len(uniq))} unique — candidate FAQ entries):")
    for q in uniq[:50]:
        w(f"    - {q}")
    w("")

    # ===== FEATURED SNIPPET OPPORTUNITIES =====
    w("=== FEATURED SNIPPET OPPORTUNITIES ===")
    opp = [r for r in serp if r.get("featured_snippet_opportunity") == "TRUE"]
    w(f"  Capturable featured snippets (competitor weakly holding): {len(opp)}")
    for r in opp[:20]:
        w(f"    - {r['keyword']} — currently: {r['featured_snippet_owner']}")
    if not opp:
        w("    (no competitor-held snippets among top 30 — most lack a featured snippet entirely)")
    w("")

    # ===== DEFENSIBLE-ANGLE =====
    w("=== DEFENSIBLE-ANGLE OPPORTUNITIES (BBI-specific) ===")
    def find(terms, label, limit=25):
        rs = [r for r in agg if any(t in r["keyword"].lower() for t in terms)]
        rs.sort(key=lambda r: -iv(r["search_volume"]))
        w(f"  {label}: {len(rs)}")
        for r in rs[:limit]:
            w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo) [{r['ranking_competitors']}]")
    find(["oecm", "bps", "broader public sector", "tender", "rfp", "rfq", "procurement"], "OECM / BPS / procurement")
    find(["peterborough", "kingston", "belleville", "cobourg", "lindsay", "oshawa", "whitby",
          "ajax", "pickering", "durham"], "Eastern Ontario / Peterborough-region geo")
    find(["space planning", "office design", "fit-out", "fit out", "office layout", "floor plan",
          "reconfiguration", "interior design"], "Design / space planning (BBI underexposed)")
    find(["school", "classroom", "library", "principal", "education", "campus"], "School / education / principal")
    find(["small office", "office manager", "business owner", "startup", "small business"], "Small business / office manager")
    find(["global furniture", "teknion", "keilhauer", "ergocentric", "otg", "offices to go",
          "heartwood", "obusforme"], "Brand-specific dealer (7 BBI brands — home turf)")
    w("")

    # ===== GAPS =====
    w("=== GAPS (BBI opportunity) ===")
    bbi_kw = {r["keyword"].lower() for r in bbi}
    notbbi = [r for r in agg if r["keyword"].lower() not in bbi_kw and r["intent_category"] in commercial]
    notbbi.sort(key=lambda r: -iv(r["search_volume"]))
    w(f"  BBI ranks for {len(bbi)} kw; competitors collectively rank for {len(agg)} filtered kw.")
    w("  Top 25 high-volume commercial keywords BBI does NOT yet rank for:")
    for r in notbbi[:25]:
        w(f"    - {r['keyword']} ({iv(r['search_volume']):,}/mo, {r['intent_category']}, tier:{r['keyword_tier']})")
    w("  Intent categories with thin competitor coverage (BBI whitespace):")
    ic = Counter(r["intent_category"] for r in agg)
    for it in ["compliance_certification", "procurement_process", "design_service", "service",
               "vendor_relationship", "use_case_vertical"]:
        w(f"    - {it}: only {ic.get(it,0)} competitor kw — under-served, BBI can own with targeted pages")
    w("")

    # ===== NOTABLE PATTERNS =====
    w("=== NOTABLE PATTERNS ===")
    lp_yes = sum(1 for r in geo if r.get("local_pack_present") == "Y")
    w(f"  - {surf.get('pdp',0)} product/PDP-mappable keywords vs only {ic.get('use_case_vertical',0)} vertical-specific — "
      "competitors compete on generic product terms, leaving institutional/vertical angles open.")
    w(f"  - Local pack fires on {lp_yes}/{len(geo)} geo queries checked — Google Business Profile + geo pages "
      "are critical for '{city} office furniture' visibility.")
    w("  - Grand & Toy dominates head-term volume (national); BBI cannot win head terms but can win "
      "Eastern-Ontario geo + institutional/OECM long-tail where G&T is generic.")
    w("  - Design/space-planning keywords are sparse across ALL competitors — genuine differentiation lane for BBI.")
    w("")

    # ===== NEXT ACTION =====
    w("=== NEXT ACTION FOR LEO ===")
    w("  1. Review this summary")
    w("  2. Open manual_review.csv to resolve edge cases")
    w("  3. Bring aggregated CSV + summary to Claude web chat for ICP-KEYWORD-WALKTHROUGH session")
    w("  4. After walkthrough: KEYWORD-SEED-EXPANSION session (DataForSEO expansion on BBI-specific "
      "seed queries) to supplement competitor data with BBI-positioning data")

    out = os.path.join(OUT, f"SUMMARY-{DATE}.md")
    open(out, "w").write("\n".join(L) + "\n")

    # reconciliation stats -> tiny JSON for trustworthy verification
    stats = {
        "summary_lines": len(L),
        "agg_rows": len(agg),
        "intent_sum": sum(Counter(r["intent_category"] for r in agg).values()),
        "tier_sum": sum(Counter(r["keyword_tier"] for r in agg).values()),
        "manual_review_intent_rows": ic.get("manual_review", 0),
        "fs_opportunities": len(opp),
        "ai_overview_top30": len(ai),
        "paa_unique": len(uniq),
        "local_pack_geo_hits": lp_yes,
    }
    json.dump(stats, open(os.path.join(OUT, "raw", f"summary-stats-{DATE}.json"), "w"))


if __name__ == "__main__":
    main()
