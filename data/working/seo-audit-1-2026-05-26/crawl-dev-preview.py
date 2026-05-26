#!/usr/bin/env python3
"""
SEO-AUDIT-1 — DEV preview crawler.

Crawls every bbi_landing URL on DEV theme 186373570873 via cookie-session preview.
Per URL captures: HTTP, title, meta desc, H1 count, canonical, OG, Twitter,
hreflang, image alt coverage %, internal link count, JSON-LD blocks (raw + types),
faq schema markers, dom size proxy.

Output: per-URL JSON + a flat summary CSV.
"""
import json, re, sys, time, urllib.request, urllib.error, http.cookiejar
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.brantbusinessinteriors.com"
PREVIEW_TID = "186373570873"
PARAMS = "preview_theme_id=186373570873&_ab=0&_fd=0&_sc=1"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

URLS = [
    # Built-in
    ("homepage",          "/"),
    # Custom pages (23 from bbi_landing gate)
    ("about",             "/pages/about"),
    ("brands",            "/pages/brands"),
    ("brands-ergocentric","/pages/brands-ergocentric"),
    ("brands-global-teknion","/pages/brands-global-teknion"),
    ("brands-heartwood",  "/pages/brands-heartwood"),
    ("brands-keilhauer",  "/pages/brands-keilhauer"),
    ("brands-obusforme",  "/pages/brands-obusforme"),
    ("brands-otg",        "/pages/brands-otg"),
    ("contact",           "/pages/contact"),
    ("customer-stories",  "/pages/customer-stories"),
    ("delivery",          "/pages/delivery"),
    ("design-services",   "/pages/design-services"),
    ("education",         "/pages/education"),
    ("faq",               "/pages/faq"),
    ("government",        "/pages/government"),
    ("healthcare",        "/pages/healthcare"),
    ("industries",        "/pages/industries"),
    ("non-profit",        "/pages/non-profit"),
    ("oecm",              "/pages/oecm"),
    ("our-work",          "/pages/our-work"),
    ("professional-services","/pages/professional-services"),
    ("quote",             "/pages/quote"),
    ("relocation",        "/pages/relocation"),
    # Phantom-template page (in templates dir but suffix NOT in gate)
    ("LEAK-ergocentric",  "/pages/ergocentric"),
    ("LEAK-howto-chair",  "/pages/how-to-adjust-my-new-chair"),
    # Collections (top 10 BBI-templated)
    ("col-business-furniture","/collections/business-furniture"),
    ("col-seating",       "/collections/seating"),
    ("col-desks",         "/collections/desks"),
    ("col-storage",       "/collections/storage"),
    ("col-tables",        "/collections/tables"),
    ("col-boardroom",     "/collections/boardroom"),
    ("col-accessories",   "/collections/accessories"),
    ("col-ergonomic-products","/collections/ergonomic-products"),
    ("col-panels-room-dividers","/collections/panels-room-dividers"),
    ("col-quiet-spaces",  "/collections/quiet-spaces"),
    # Blog
    ("blog-news",         "/blogs/news"),
    ("article-cornerstone","/blogs/news/oecm-ontario-school-boards-office-furniture"),
    # Hero PDP
    ("pdp-adapt-hb",      "/products/adapt-high-back-synchro-tilter-mvl11724"),
]

JSON_LD_RE = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.DOTALL|re.IGNORECASE)
META_RE = re.compile(r'<meta[^>]+>', re.IGNORECASE)
H_RE = re.compile(r'<h([1-6])[^>]*>(.*?)</h\1>', re.DOTALL|re.IGNORECASE)
IMG_RE = re.compile(r'<img\b([^>]*)>', re.IGNORECASE)
LINK_HREF_RE = re.compile(r'<a\b[^>]*\shref=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL|re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
ALT_RE = re.compile(r'\salt=["\']([^"\']*)["\']', re.IGNORECASE)

def attr(meta_tag, name):
    m = re.search(rf'\s{name}=["\']([^"\']*)["\']', meta_tag, re.IGNORECASE)
    return m.group(1) if m else None

def init_session():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [("User-Agent", UA), ("Accept-Language", "en-CA,en;q=0.9")]
    # Prime the cookie
    try:
        r = opener.open(f"{BASE}/?{PARAMS}", timeout=20)
        r.read()
    except Exception as e:
        print(f"Cookie prime FAILED: {e}", file=sys.stderr)
        raise
    return opener

def fetch(opener, path):
    sep = "&" if "?" in path else "?"
    url = f"{BASE}{path}{sep}{PARAMS}" if "preview_theme_id" not in path else f"{BASE}{path}"
    try:
        req = urllib.request.Request(url)
        r = opener.open(req, timeout=30)
        body = r.read()
        try:
            text = body.decode("utf-8", errors="replace")
        except Exception:
            text = body.decode("latin-1", errors="replace")
        return {
            "status": r.status,
            "final_url": r.geturl(),
            "content_length": len(body),
            "html": text,
        }
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final_url": url, "content_length": 0, "html": "", "error": str(e)}
    except Exception as e:
        return {"status": 0, "final_url": url, "content_length": 0, "html": "", "error": str(e)}

def analyse(name, path, fetched):
    html = fetched.get("html", "")
    out = {
        "name": name,
        "path": path,
        "status": fetched.get("status"),
        "final_url": fetched.get("final_url"),
        "size_bytes": fetched.get("content_length", 0),
    }
    if fetched.get("error"):
        out["fetch_error"] = fetched["error"]
        return out
    if out["status"] != 200:
        return out

    # Title
    tm = TITLE_RE.search(html)
    out["title"] = tm.group(1).strip() if tm else None
    out["title_length"] = len(out["title"]) if out.get("title") else 0

    # Meta tags
    metas = META_RE.findall(html)
    desc = None; og = {}; tw = {}; robots = None; hreflang = []
    for m in metas:
        name_attr = (attr(m, "name") or "").lower()
        prop_attr = (attr(m, "property") or "").lower()
        content = attr(m, "content")
        if name_attr == "description":
            desc = content
        elif name_attr == "robots":
            robots = content
        elif name_attr and name_attr.startswith("twitter:"):
            tw[name_attr] = content
        elif prop_attr and prop_attr.startswith("og:"):
            og[prop_attr] = content
        # hreflang on <link>, skip here
    # hreflang on <link>
    for m in re.findall(r'<link[^>]+hreflang=["\']([^"\']*)["\'][^>]*>', html, re.IGNORECASE):
        hreflang.append(m)

    out["meta_description"] = desc
    out["meta_description_length"] = len(desc) if desc else 0
    out["robots"] = robots
    out["og"] = og
    out["twitter"] = tw
    out["hreflang"] = hreflang

    # Canonical
    cm = CANONICAL_RE.search(html)
    out["canonical"] = cm.group(1) if cm else None

    # Headings
    h_counts = {f"h{i}": 0 for i in range(1, 7)}
    h_texts = {f"h{i}": [] for i in range(1, 7)}
    for lvl, inner in H_RE.findall(html):
        h_counts[f"h{lvl}"] += 1
        if lvl in ("1", "2"):
            text = re.sub(r"<[^>]+>", "", inner).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                h_texts[f"h{lvl}"].append(text[:140])
    out["h_counts"] = h_counts
    out["h1_texts"] = h_texts["h1"]
    out["h2_texts"] = h_texts["h2"][:20]  # cap

    # Images + alt coverage
    imgs = IMG_RE.findall(html)
    total = len(imgs)
    with_alt_nonempty = 0
    with_alt_empty = 0
    no_alt = 0
    for tagattrs in imgs:
        am = ALT_RE.search(tagattrs)
        if am is None:
            no_alt += 1
        elif am.group(1).strip() == "":
            with_alt_empty += 1
        else:
            with_alt_nonempty += 1
    out["images_total"] = total
    out["images_alt_nonempty"] = with_alt_nonempty
    out["images_alt_empty"] = with_alt_empty
    out["images_no_alt"] = no_alt
    out["alt_coverage_pct"] = round((with_alt_nonempty / total) * 100, 1) if total else None

    # Links
    hrefs = LINK_HREF_RE.findall(html)
    internal = [h for h in hrefs if h.startswith("/") or "brantbusinessinteriors.com" in h]
    external = [h for h in hrefs if h and not (h.startswith("/") or "brantbusinessinteriors.com" in h or h.startswith("#") or h.startswith("mailto:") or h.startswith("tel:") or h.startswith("javascript:"))]
    out["links_total"] = len(hrefs)
    out["links_internal"] = len(internal)
    out["links_external"] = len(external)

    # JSON-LD blocks
    jsonld_blocks = []
    jsonld_types = []
    jsonld_errors = []
    for raw in JSON_LD_RE.findall(html):
        raw_trim = raw.strip()
        try:
            data = json.loads(raw_trim)
        except json.JSONDecodeError as e:
            jsonld_errors.append({"error": str(e), "snippet": raw_trim[:200]})
            continue
        jsonld_blocks.append({"length": len(raw_trim), "data": data})
        # Walk to collect @types
        def walk(d):
            if isinstance(d, dict):
                t = d.get("@type")
                if isinstance(t, list):
                    jsonld_types.extend(t)
                elif isinstance(t, str):
                    jsonld_types.append(t)
                # Walk graphs and arrays
                for v in d.values():
                    walk(v)
            elif isinstance(d, list):
                for v in d:
                    walk(v)
        walk(data)
    out["jsonld_block_count"] = len(jsonld_blocks)
    out["jsonld_types"] = sorted(set(jsonld_types))
    out["jsonld_parse_errors"] = jsonld_errors
    out["jsonld_raw_lengths"] = [b["length"] for b in jsonld_blocks]
    # Persist full blocks separately (per-page file)
    out["_jsonld_full"] = [b["data"] for b in jsonld_blocks]

    # FAQ accordion detection (count of faq_item rendered)
    out["faq_item_dom_count"] = len(re.findall(r'class=["\'][^"\']*faq__item[^"\']*["\']', html, re.IGNORECASE))
    out["faq_question_count_dom"] = len(re.findall(r'<button[^>]*class=["\'][^"\']*faq__q[^"\']*["\']', html, re.IGNORECASE))

    # BBI marker presence
    out["bbi_marker_count"] = sum(html.count(m) for m in ["bbi-homepage", "bbi-quote-modal", "bbi-localbusiness", "bbi-nav", "bbi-hero", "bbi-org"])
    # Avada/leak detection
    out["avada_marker_count"] = sum(html.count(m) for m in ["primary-header-blocks", "main-header__inner", "Foxtheme", "starlite"])

    # Render-blocking proxy
    out["scripts_count"] = len(re.findall(r'<script\b', html, re.IGNORECASE))
    out["stylesheets_count"] = len(re.findall(r'<link[^>]+rel=["\']stylesheet["\']', html, re.IGNORECASE))

    return out

def main():
    outdir = Path(__file__).parent
    print(f"Initializing DEV preview session…", file=sys.stderr)
    opener = init_session()
    print(f"Session OK. Crawling {len(URLS)} URLs…", file=sys.stderr)

    summary = []
    for i, (name, path) in enumerate(URLS, 1):
        print(f"[{i:>2}/{len(URLS)}] {name:30s} {path}", file=sys.stderr)
        f = fetch(opener, path)
        a = analyse(name, path, f)

        # Write per-URL JSON-LD detail
        if "_jsonld_full" in a:
            jld = a.pop("_jsonld_full")
            if jld:
                (outdir / f"jsonld-{name}.json").write_text(json.dumps(jld, indent=2, default=str))

        summary.append(a)
        time.sleep(0.4)  # be polite

    (outdir / "crawl-summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(f"DONE: {len(summary)} URLs crawled. Output → {outdir}/", file=sys.stderr)

    # Compact tabular print
    print()
    print(f"{'URL':<33} {'HTTP':>4} {'Tlen':>4} {'Dlen':>4} {'H1#':>3} {'Schema-types':<55} {'OG':<8} {'TW':<8} {'Alt%':>5} {'Faq':>3}")
    for r in summary:
        types_short = ",".join(r.get("jsonld_types", [])[:5])
        og_n = len(r.get("og") or {})
        tw_n = len(r.get("twitter") or {})
        print(f"{r['name']:<33} {r.get('status') or 0:>4} {r.get('title_length') or 0:>4} {r.get('meta_description_length') or 0:>4} {(r.get('h_counts') or {}).get('h1', 0):>3} {types_short[:55]:<55} {og_n:>3}     {tw_n:>3}     {r.get('alt_coverage_pct') or 0:>5} {r.get('faq_item_dom_count') or 0:>3}")

if __name__ == "__main__":
    main()
