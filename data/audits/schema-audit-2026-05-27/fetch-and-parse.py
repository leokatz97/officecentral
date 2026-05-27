#!/usr/bin/env python3
"""
HOTFIX-SCHEMA-AUDIT-1 (Phase 1) — fetch LIVE URLs and extract all JSON-LD.

Read-only. Writes captured HTML + parsed JSON-LD to data/audits/schema-audit-2026-05-27/captures/
"""
import json, re, sys, os, urllib.request, time
from pathlib import Path

OUT = Path(__file__).parent / "captures"
OUT.mkdir(exist_ok=True)

URLS = [
    ("homepage",            "https://www.brantbusinessinteriors.com/"),
    ("collection-seating",  "https://www.brantbusinessinteriors.com/collections/seating"),
    ("collection-desks",    "https://www.brantbusinessinteriors.com/collections/desks"),
    ("collection-bizfurn",  "https://www.brantbusinessinteriors.com/collections/business-furniture"),
    ("pdp-sample",          "https://www.brantbusinessinteriors.com/collections/seating/products/dual-monitor-arm"),  # may 404, will try alt
    ("page-oecm",           "https://www.brantbusinessinteriors.com/pages/oecm"),
    ("page-quote",          "https://www.brantbusinessinteriors.com/pages/quote"),
    ("page-about",          "https://www.brantbusinessinteriors.com/pages/about"),
    ("page-contact",        "https://www.brantbusinessinteriors.com/pages/contact"),
    ("page-brands",         "https://www.brantbusinessinteriors.com/pages/brands"),
    ("page-our-work",       "https://www.brantbusinessinteriors.com/pages/our-work"),
    ("page-healthcare",     "https://www.brantbusinessinteriors.com/pages/healthcare"),
    ("page-education",      "https://www.brantbusinessinteriors.com/pages/education"),
    ("page-industries",     "https://www.brantbusinessinteriors.com/pages/industries"),
    ("page-faq",            "https://www.brantbusinessinteriors.com/pages/faq"),
    ("page-design-services","https://www.brantbusinessinteriors.com/pages/design-services"),
    ("page-relocation",     "https://www.brantbusinessinteriors.com/pages/relocation"),
    ("page-delivery",       "https://www.brantbusinessinteriors.com/pages/delivery"),
    ("page-brands-ergocentric","https://www.brantbusinessinteriors.com/pages/brands-ergocentric"),
    ("page-customer-stories","https://www.brantbusinessinteriors.com/pages/customer-stories"),
    ("404",                 "https://www.brantbusinessinteriors.com/products/this-does-not-exist-test-404"),
    ("search",              "https://www.brantbusinessinteriors.com/search?q=desk"),
    ("blog",                "https://www.brantbusinessinteriors.com/blogs/news"),
]

JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; BBI-Schema-Audit/1.0)"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace") if e.code != 404 else ""
    except Exception as e:
        return None, f"ERROR: {e}"

def parse_blocks(html):
    blocks = []
    for raw in JSONLD_RE.findall(html or ""):
        raw_s = raw.strip()
        try:
            data = json.loads(raw_s)
            blocks.append({"ok": True, "data": data, "raw_len": len(raw_s)})
        except json.JSONDecodeError as e:
            blocks.append({"ok": False, "error": str(e), "raw": raw_s[:500], "raw_len": len(raw_s)})
    return blocks

summary = []
for slug, url in URLS:
    print(f"[fetch] {slug} -> {url}", flush=True)
    status, html = fetch(url)
    # save html for forensics
    (OUT / f"{slug}.html").write_text(html or "", encoding="utf-8")
    blocks = parse_blocks(html)
    types = []
    for b in blocks:
        if not b["ok"]:
            types.append(f"PARSE_ERR({b['error'][:60]})")
            continue
        d = b["data"]
        if isinstance(d, dict):
            if "@graph" in d:
                for node in d["@graph"]:
                    t = node.get("@type")
                    types.append(f"@graph:{t if not isinstance(t,list) else '+'.join(t)}")
            else:
                t = d.get("@type")
                types.append(t if not isinstance(t, list) else "+".join(t))
        elif isinstance(d, list):
            for n in d:
                types.append(n.get("@type", "?"))
    summary.append({
        "slug": slug, "url": url, "status": status,
        "block_count": len(blocks),
        "types": types,
        "html_size": len(html or ""),
    })
    (OUT / f"{slug}.jsonld.json").write_text(
        json.dumps([b.get("data") if b["ok"] else {"_parse_error": b["error"]} for b in blocks],
                   indent=2, default=str),
        encoding="utf-8"
    )
    time.sleep(0.6)

(OUT / "_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("\n=== SUMMARY ===")
for s in summary:
    print(f"  {s['slug']:30s} [{s['status']}]  {s['block_count']} blocks  types={s['types']}")
print(f"\nWrote captures + summary to {OUT}")
