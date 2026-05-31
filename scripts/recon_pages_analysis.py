#!/usr/bin/env python3
"""COMPETITOR-KEYWORD-RECON-1 follow-on — competitor page-archetype analysis.

Descriptive only (no new API calls, no decisions): classifies each competitor top-page
by URL archetype and reports where competitor organic traffic (ETV) concentrates. Informs
which page types BBI should prioritise. Reads top-pages-*.csv already on disk.
"""
import csv
import glob
import os
import re
from collections import defaultdict

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(OUT, "data", "reports", "keyword-research")
DATE = open(os.path.join(OUT, ".run_date")).read().strip()

CITIES = ["toronto", "mississauga", "brampton", "vaughan", "markham", "ottawa", "hamilton",
          "london", "barrie", "kingston", "peterborough", "oshawa", "whitby", "scarborough",
          "newmarket", "burlington", "durham", "ajax", "pickering", "north-york", "gta"]
BRANDS = ["global", "teknion", "keilhauer", "ergocentric", "offices-to-go", "otg", "heartwood",
          "obusforme", "humanscale", "hon", "steelcase", "herman-miller", "haworth", "allseating"]


def archetype(url):
    u = url.lower()
    path = re.sub(r"^https?://[^/]+", "", u)
    if path in ("", "/"):
        return "homepage"
    if any(c in u for c in CITIES):
        return "geo_page"
    if any(b in u for b in BRANDS) or "/brands/" in u or "/brand/" in u:
        return "brand_page"
    if any(s in u for s in ["/collections/", "/collection/", "/category/", "/categories/",
                            "/shop/", "/c/", "/department"]):
        return "collection_page"
    if any(s in u for s in ["/products/", "/product/", "/p/", "/item/"]):
        return "product_page"
    if any(s in u for s in ["/blog", "/news", "/article", "/resources", "/guide", "/learn"]):
        return "blog_content"
    if any(s in u for s in ["/services", "/space-planning", "/design", "/installation", "/delivery"]):
        return "service_page"
    if any(s in u for s in ["/about", "/contact", "/locations", "/store", "/pages/"]):
        return "info_page"
    return "other"


def iv(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def main():
    files = [f for f in glob.glob(os.path.join(OUT, f"top-pages-*-{DATE}.csv"))]
    overall_etv = defaultdict(float)
    overall_cnt = defaultdict(int)
    per_domain = {}

    for fp in sorted(files):
        dom = os.path.basename(fp)[len("top-pages-"):-(len(DATE) + 5)]
        etv = defaultdict(float)
        cnt = defaultdict(int)
        for r in csv.DictReader(open(fp)):
            a = archetype(r.get("page_url", ""))
            e = iv(r.get("etv"))
            etv[a] += e
            cnt[a] += 1
            overall_etv[a] += e
            overall_cnt[a] += 1
        per_domain[dom] = (etv, cnt)

    order = ["homepage", "collection_page", "product_page", "geo_page", "brand_page",
             "blog_content", "service_page", "info_page", "other"]

    L = []
    w = L.append
    w("COMPETITOR PAGE-ARCHETYPE ANALYSIS")
    w(f"Date: {DATE}  |  Branch: feature/competitor-keyword-recon-1")
    w("Descriptive read-only analysis of competitor top-pages (by estimated organic traffic).")
    w("Shows which page TYPES drive competitor organic traffic -> where BBI should invest.")
    w("")

    tot = sum(overall_etv.values()) or 1
    w("=== OVERALL: share of competitor organic traffic (ETV) by page archetype ===")
    for a in order:
        share = 100 * overall_etv[a] / tot
        w(f"  {a:<16} {overall_cnt[a]:>4} pages | ETV {overall_etv[a]:>10,.0f} | {share:5.1f}% of traffic")
    w("")

    w("=== PER-COMPETITOR (top archetype by ETV) ===")
    for dom in sorted(per_domain):
        etv, cnt = per_domain[dom]
        dtot = sum(etv.values()) or 1
        top = sorted(etv.items(), key=lambda kv: -kv[1])[:3]
        desc = ", ".join(f"{a} {100*v/dtot:.0f}%" for a, v in top)
        w(f"  {dom:<32} -> {desc}")
    w("")

    w("=== READ-OUT FOR BBI ===")
    coll = 100 * overall_etv["collection_page"] / tot
    prod = 100 * overall_etv["product_page"] / tot
    geo = 100 * overall_etv["geo_page"] / tot
    blog = 100 * overall_etv["blog_content"] / tot
    svc = 100 * overall_etv["service_page"] / tot
    w(f"  - Collection pages drive ~{coll:.0f}% and product pages ~{prod:.0f}% of competitor organic "
      "traffic — category architecture + PDP SEO is table stakes.")
    w(f"  - Geo pages: ~{geo:.0f}%. Where present they convert local intent — BBI's Eastern-Ontario "
      "geo pages are a direct, winnable lever.")
    w(f"  - Blog/content: ~{blog:.0f}%; service pages: ~{svc:.0f}%. Both are THIN across competitors — "
      "design/space-planning service pages + institutional content are open lanes for BBI.")
    w("  - Cross-reference with SEED-EXPANSION net-new keywords: build geo_page + service_page + "
      "oecm_page first; they pair high BBI-fit with low competitor coverage.")

    open(os.path.join(OUT, f"PAGE-ARCHETYPE-ANALYSIS-{DATE}.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
