#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 — Phase 4 aggregation + multi-dimensional classification.

Loads all competitor ranked-keyword CSVs, dedupes, applies KEEP/DROP filter rules,
drops sv<10, and adds the full classification column set. Merges Phase 2.5 SERP-feature
flags if present. Emits the top-30 highest-volume keyword list for Phase 2.5.

Run twice: first pass (no SERP json) emits top30; after serp_features.py runs, second
pass merges featured_snippet_opportunity + ai_overview_present.
"""
import csv
import glob
import json
import os
import re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(OUT, "data", "reports", "keyword-research")
DATE = open(os.path.join(OUT, ".run_date")).read().strip()
SERP_JSON = os.path.join(OUT, "raw", f"serp-features-merge-{DATE}.json")

COMPETITOR_FILES = [f for f in glob.glob(os.path.join(OUT, f"ranked-keywords-*-{DATE}.csv"))
                    if not os.path.basename(f).startswith(("ranked-keywords-bbi", "ranked-keywords-officecentral"))]

# ---------------- filter rules ----------------
GEO_CITIES = ["canada", "canadian", "ontario", "peterborough", "kingston", "belleville",
              "cobourg", "lindsay", "oshawa", "whitby", "ajax", "pickering", "markham",
              "toronto", "gta", "eastern ontario", "mississauga", "brampton", "vaughan",
              "newmarket", "scarborough", "north york", "etobicoke", "hamilton", "ottawa",
              "london", "barrie", "durham", "york region", "halton"]

KEEP_TERMS = {
    "vendor": ["dealer", "supplier", "authorized", "vendor", "distributor", "reseller"],
    "compliance": ["bifma", "greenguard", "oecm", "bps", "broader public sector", "agreement 2025",
                   "certified", "compliance"],
    "procurement": ["rfp", "rfq", "tender", "procurement", "net 30", " po ", "purchase order", "quote", "bulk"],
    "vertical": ["healthcare", "hospital", "clinic", "medical", "dental", "school", "education",
                 "classroom", "library", "municipal", "government", "council", "law office",
                 "legal", "accounting", "non-profit", "nonprofit", "university", "college"],
    "smallbiz": ["small office", "office manager", "business owner", "startup", "small business", "home office"],
    "geo": GEO_CITIES,
    "design": ["space planning", "office design", "workspace planning", "office redesign", "fit-out",
               "fit out", "office layout", "interior design", "autocad", "floor plan", "reconfiguration",
               "space plan"],
    "service": ["installation", "delivery", "relocation", "office move", "assembly", "removal", "install"],
    "warranty": ["warranty", "repair", "guarantee"],
    "brand": ["global furniture", "teknion", "keilhauer", "ergocentric", "otg", "offices to go",
              "heartwood", "obusforme", "humanscale", "hon", "steelcase", "herman miller", "haworth",
              "allseating", "groupe lacasse", "national office"],
    "informational": ["guide", "how to", "what is", "vs ", "versus", "best ", "ergonomic"],
    "product": ["office chair", "desk", "workstation", "cubicle", "panel system", "storage cabinet",
                "conference table", "ergonomic chair", "sit-stand", "sit stand", "standing desk",
                "lateral file", "lounge seating", "reception", "boardroom", "filing cabinet",
                "task chair", "executive chair", "meeting table", "bookcase", "credenza", "office furniture",
                "office table", "office desk", "office cubicle", "drafting", "stool", "office storage"],
}

DROP_TERMS = ["ikea", "wayfair", "costco", "amazon", "walmart", "canadian tire", "structube",
              "leons", "the brick", "home depot", "kijiji", "facebook marketplace", "diy ",
              "bedroom", "living room", "patio", "outdoor", "gaming chair", "recliner sofa",
              "dining", "mattress", "nursery", "garden"]

QUESTION_STARTS = ("how", "what", "why", "when", "where", "who", "can i", "do i", "should i", "are ", "is ")


def keep(kw):
    k = " " + kw.lower() + " "
    for d in DROP_TERMS:
        if d in k:
            # allow if clearly commercial vertical overrides (rare) — keep simple: drop
            return False, "drop_consumer"
    for cat, terms in KEEP_TERMS.items():
        for t in terms:
            if t in k:
                return True, cat
    return False, "no_match"


# ---------------- classification ----------------
def intent_category(kw, matched_cat):
    k = kw.lower()
    if any(t in k for t in KEEP_TERMS["vendor"]) or any(b in k for b in KEEP_TERMS["brand"]) and ("dealer" in k or "supplier" in k or "authorized" in k):
        return "vendor_relationship"
    if any(t in k for t in KEEP_TERMS["compliance"]):
        return "compliance_certification"
    if any(t in k for t in KEEP_TERMS["procurement"]):
        return "procurement_process"
    if any(t in k for t in KEEP_TERMS["design"]):
        return "design_service"
    if any(t in k for t in KEEP_TERMS["service"]) or any(t in k for t in KEEP_TERMS["warranty"]):
        return "service"
    if any(t in k for t in KEEP_TERMS["vertical"]):
        return "use_case_vertical"
    if any(c in k for c in GEO_CITIES):
        # geo + product still geo-primary
        return "geographic"
    if is_question(kw) or any(t in k for t in ["guide", "how to", "what is", "vs ", "versus", "ideas", "tips"]):
        return "informational"
    if any(t in k for t in KEEP_TERMS["product"]):
        return "product_generic"
    # Fallback: map the KEEP-rule category that admitted this keyword, so nothing kept
    # is left silently unclassified. Only genuinely unknown matches -> manual_review.
    cat_to_intent = {
        "vendor": "vendor_relationship", "brand": "vendor_relationship",
        "compliance": "compliance_certification", "procurement": "procurement_process",
        "vertical": "use_case_vertical", "design": "design_service",
        "service": "service", "warranty": "service", "geo": "geographic",
        "informational": "informational", "product": "product_generic",
        "smallbiz": "product_generic",
    }
    return cat_to_intent.get(matched_cat, "manual_review")


def bbi_industry(kw):
    k = kw.lower()
    hits = []
    if any(t in k for t in ["healthcare", "hospital", "clinic", "medical", "dental", "health team", "exam room", "patient"]):
        hits.append("healthcare")
    if any(t in k for t in ["school", "classroom", "education", "library", "student", "teacher", "principal", "k-12", "campus", "university", "college"]):
        hits.append("education")
    if any(t in k for t in ["municipal", "government", "council", "oecm", "bps", "broader public sector", "city of", "provincial"]):
        hits.append("government")
    if any(t in k for t in ["non-profit", "nonprofit", "community service", "social service", "housing", "charity"]):
        hits.append("non-profit")
    if any(t in k for t in ["law office", "legal", "accounting", "law firm", "professional service", "office manager"]):
        hits.append("professional-services")
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return "multi-industry"
    return "not-applicable"


def bbi_outcome(kw, intent):
    k = kw.lower()
    paths = set()
    # design consultation
    if intent == "design_service" or any(t in k for t in KEEP_TERMS["design"]):
        paths.add("design-consultation")
    # quote-request: bulk/commercial/vendor/procurement/vertical/service
    if intent in ("vendor_relationship", "compliance_certification", "procurement_process",
                  "use_case_vertical", "service") or any(t in k for t in
                  ["quote", "rfp", "rfq", "tender", "bulk", "commercial", "dealer", "supplier", "installation", "fit-out"]):
        paths.add("quote-request")
    # ecom: specific single-product commercial intent
    if intent in ("product_generic",) and not any(t in k for t in ["bulk", "fit-out", "project"]):
        paths.add("ecom-purchase")
    # informational
    if intent == "informational" or is_question(kw):
        paths.add("informational-only")
    if not paths:
        # geographic / generic fallback -> quote (B2B default) unless purely informational
        paths.add("quote-request")
    if len(paths) > 1:
        # collapse to multi-outcome unless one is informational-only paired
        non_info = paths - {"informational-only"}
        if len(non_info) >= 2:
            return "multi-outcome"
        if non_info:
            return list(non_info)[0]
    return list(paths)[0]


def keyword_tier(kw):
    n = len([w for w in re.split(r"\s+", kw.strip()) if w])
    if n <= 2:
        return "head"
    if n == 3:
        return "mid"
    return "long_tail"


def is_question(kw):
    k = kw.lower().strip()
    return k.startswith(QUESTION_STARTS)


def difficulty_band(kd):
    try:
        v = float(kd)
    except (TypeError, ValueError):
        return ""
    if v < 30:
        return "easy"
    if v <= 60:
        return "medium"
    return "hard"


def site_surfaces(kw, intent, industry, tier):
    k = kw.lower()
    s = []
    def add(x):
        if x not in s:
            s.append(x)
    # product-specific commercial
    if intent == "product_generic":
        add("pdp"); add("collection_page")
    # brand+dealer
    if intent == "vendor_relationship" or any(b in k for b in KEEP_TERMS["brand"]):
        add("brand_page")
    # vertical+product
    if intent == "use_case_vertical" or industry not in ("not-applicable",):
        add("industry_page"); add("collection_page")
    # OECM/BPS
    if any(t in k for t in ["oecm", "bps", "broader public sector", "agreement 2025"]):
        add("oecm_page")
    # design/install/relocation
    if intent in ("design_service", "service"):
        add("service_page")
    # questions -> faq + blog
    if is_question(kw):
        add("faq"); add("blog")
    # how to / what is / vs / comparison
    if any(t in k for t in ["how to", "what is", " vs ", "versus", "compare", "comparison", "difference"]):
        add("blog"); add("cluster_page")
    # broad topical -> pillar
    if any(t in k for t in ["workplace design", "ergonomics", "sustainability", "office trends",
                            "workspace", "hybrid work", "office wellness"]):
        add("pillar_page")
    # geo
    if any(c in k for c in GEO_CITIES):
        add("geo_page")
    # head broad commercial -> homepage
    if tier == "head" and intent in ("product_generic", "geographic"):
        add("homepage"); add("collection_page")
    if not s:
        add("collection_page")
    return ",".join(s)


def main():
    serp_map = {}
    if os.path.exists(SERP_JSON):
        serp_map = json.load(open(SERP_JSON))

    # aggregate competitor keywords -> dedupe by keyword
    agg = {}
    for fp in COMPETITOR_FILES:
        for row in csv.DictReader(open(fp)):
            kw = (row.get("keyword") or "").strip()
            if not kw:
                continue
            sv = int(float(row.get("search_volume") or 0))
            kd = row.get("keyword_difficulty")
            dom = row.get("source_domain", "")
            e = agg.get(kw)
            if not e:
                agg[kw] = {
                    "keyword": kw, "search_volume": sv, "cpc": row.get("cpc", ""),
                    "competition": row.get("competition", ""), "keyword_difficulty": kd,
                    "search_intent": row.get("search_intent", ""), "domains": {dom},
                    "best_rank": _int(row.get("rank_absolute")),
                }
            else:
                e["search_volume"] = max(e["search_volume"], sv)
                e["domains"].add(dom)
                r = _int(row.get("rank_absolute"))
                if r and (not e["best_rank"] or r < e["best_rank"]):
                    e["best_rank"] = r
                if (not e["keyword_difficulty"]) and kd:
                    e["keyword_difficulty"] = kd

    rows, manual = [], []
    for kw, e in agg.items():
        ok, cat = keep(kw)
        if not ok:
            if cat == "no_match":
                manual.append([kw, e["search_volume"], "no KEEP-rule match", ",".join(sorted(e["domains"]))])
            continue
        if e["search_volume"] < 10:
            continue
        intent = intent_category(kw, cat)
        if intent == "manual_review":
            manual.append([kw, e["search_volume"], "intent unclassified", ",".join(sorted(e["domains"]))])
        industry = bbi_industry(kw)
        tier = keyword_tier(kw)
        outcome = bbi_outcome(kw, intent)
        surfaces = site_surfaces(kw, intent, industry, tier)
        dband = difficulty_band(e["keyword_difficulty"])
        sf = serp_map.get(kw.lower(), {})
        rows.append({
            "keyword": kw,
            "search_volume": e["search_volume"],
            "cpc": e["cpc"],
            "competition": e["competition"],
            "keyword_difficulty": e["keyword_difficulty"],
            "difficulty_band": dband,
            "search_intent": e["search_intent"],
            "best_competitor_rank": e["best_rank"] or "",
            "ranking_competitors": ",".join(sorted(e["domains"])),
            "competitor_count": len(e["domains"]),
            "intent_category": intent,
            "bbi_industry_match": industry,
            "bbi_outcome_path": outcome,
            "keyword_tier": tier,
            "site_surface_recommendation": surfaces,
            "question_format": "TRUE" if is_question(kw) else "FALSE",
            "featured_snippet_opportunity": sf.get("featured_snippet_opportunity", ""),
            "ai_overview_present": sf.get("ai_overview_present", ""),
        })

    rows.sort(key=lambda r: -r["search_volume"])
    cols = list(rows[0].keys()) if rows else []
    out_csv = os.path.join(OUT, f"competitor-keywords-aggregated-{DATE}.csv")
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # write manual review — idempotent: preserve non-classify rows, replace classify rows
    mr = os.path.join(OUT, "manual_review.csv")
    header = ["stage", "target", "reason", "detail"]
    preserved = []
    if os.path.exists(mr):
        for row in csv.reader(open(mr)):
            if not row or row == header:
                continue
            if row[0] != "phase4-classify":
                preserved.append(row)
    with open(mr, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in preserved:
            w.writerow(row)
        for m in manual:
            w.writerow(["phase4-classify", m[0], m[2], f"sv={m[1]} domains={m[3]}"])

    # emit top-30 list for Phase 2.5 (commercial KEEP set, by volume)
    top30 = [r["keyword"] for r in rows[:30]]
    json.dump(top30, open(os.path.join(OUT, f"top30-keywords-{DATE}.json"), "w"), indent=1)
    # geo keyword list for local-pack pass
    geo = [r["keyword"] for r in rows if any(c in r["keyword"].lower() for c in GEO_CITIES)
           and ("office furniture" in r["keyword"].lower() or "commercial furniture" in r["keyword"].lower())]
    json.dump(geo[:60], open(os.path.join(OUT, f"geo-keywords-{DATE}.json"), "w"), indent=1)

    print(f"Aggregated kept: {len(rows)}  | manual_review added: {len(manual)}  | top30 + {len(geo[:60])} geo emitted")
    print(f"SERP merge: {'YES' if serp_map else 'not yet (run serp_features.py then re-run)'}")


def _int(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    main()
