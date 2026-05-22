#!/usr/bin/env python3
"""V2 classifier using live page + collection handles from Shopify Admin."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/leokatz/Desktop/Office Central")
TMP = ROOT / "data/reports/interlink-3-tmp"

# Load live data
live_pages = json.loads((TMP / "live-pages.json").read_text())
live_collections = json.loads((TMP / "live-collections.json").read_text())

# Maps: handle -> {published, title}
PAGE_INFO = {p["handle"]: {"published": bool(p.get("published_at")), "title": p["title"]} for p in live_pages}
COLL_INFO = {c["handle"]: {"title": c["title"], "type": c.get("type", "?")} for c in live_collections}

LOCKED_TEL = "+18008359565"
LOCKED_TEL_DIGITS = "18008359565"
LOCKED_EMAIL_DOMAIN = "brantbusinessinteriors.com"
LOCKED_EMAIL_LOCAL = {"info", "quotes", "design"}

# Liquid patterns
HAS_LIQUID = re.compile(r'\{\{|\{\%')
LIQUID_HREF = re.compile(r'^\s*\{\{.*?\}\}\s*$')
CSS_ASSET_RE = re.compile(r'\.(css|js|png|jpg|jpeg|gif|svg|webp|woff2?|ttf|otf)(\?.*)?$', re.IGNORECASE)

# Liquid defaults known to evaluate to safe values (from prior schema inspection)
KNOWN_LIQUID_PHONE_TOKENS = {
    "{{ section.settings.phone_href }}",  # default "18008359565" — same digits, missing +1 prefix → WARN
}
KNOWN_LIQUID_EMAIL_TOKENS = {
    "{{ _email }}",  # ds-lp-quote: assigned to info@brantbusinessinteriors.com default — OK
}

def classify(href):
    h = href.strip()
    if h == "" or h == "#":
        return "EMPTY", None
    if h.startswith("mailto:"):
        return "MAILTO", h[len("mailto:"):]
    if h.startswith("tel:"):
        return "TEL", h[len("tel:"):]
    if h.startswith("#"):
        return "ANCHOR", h[1:]
    if h.startswith("javascript:"):
        return "JS", h
    if h.startswith("http://") or h.startswith("https://") or h.startswith("//"):
        return "EXTERNAL", h
    if h.startswith("/cdn/") or h.startswith("/assets/") or CSS_ASSET_RE.search(h):
        return "ASSET", h
    if LIQUID_HREF.match(h):
        return "LIQUID", h
    if h.startswith("/pages/"):
        slug = h[len("/pages/"):].rstrip("/").split("?")[0].split("#")[0]
        return ("INTERNAL_PAGE_LIQUID" if HAS_LIQUID.search(slug) else "INTERNAL_PAGE"), slug
    if h.startswith("/collections/"):
        rest = h[len("/collections/"):].rstrip("/").split("?")[0].split("#")[0]
        return ("INTERNAL_COLL_LIQUID" if HAS_LIQUID.search(rest) else "INTERNAL_COLL"), rest
    if h.startswith("/products/"):
        slug = h[len("/products/"):].rstrip("/").split("?")[0].split("#")[0]
        return ("INTERNAL_PROD_LIQUID" if HAS_LIQUID.search(slug) else "INTERNAL_PROD"), slug
    if h.startswith("/blogs/"):
        return "INTERNAL_BLOG", h[len("/blogs/"):].rstrip("/")
    if h.startswith("/policies/"):
        return "INTERNAL_POLICY", h[len("/policies/"):].rstrip("/")
    if h.startswith("/account") or h.startswith("/cart") or h.startswith("/search"):
        return "INTERNAL_SYS", h
    if h == "/":
        return "INTERNAL_HOME", h
    if h.startswith("/"):
        return "INTERNAL_OTHER", h
    if HAS_LIQUID.search(h):
        return "LIQUID_MIXED", h
    return "OTHER", h

def validate(href, cat, val):
    """Return (sev, reason, finding_type, fix_hint)."""
    if cat == "EMPTY":
        return "WARN", "empty href / placeholder", "anchor", None
    if cat == "JS":
        return "OK", "js handler", None, None
    if cat == "ANCHOR":
        return "OK", "in-page anchor", None, None
    if cat == "ASSET":
        return "OK", "asset link", None, None
    if cat == "EXTERNAL":
        # External: review only
        if val.startswith("//"):
            return "WARN", "protocol-relative URL", "external", None
        return "OK", "external link", None, None
    if cat == "MAILTO":
        email = val.split("?")[0].lower().strip()
        # Handle liquid-templated mailtos
        if HAS_LIQUID.search(href):
            if "{{ _email }}" in href:
                return "OK", "ds-lp-quote _email default = info@brantbusinessinteriors.com (verified)", None, None
            return "INFO", f"liquid-templated mailto — runtime resolved: {href}", None, None
        if "@" not in email:
            return "FAIL", "malformed mailto", "wrong-contact", None
        local, _, domain = email.partition("@")
        if domain != LOCKED_EMAIL_DOMAIN:
            return "FAIL", f"wrong email domain (got {domain}, expected {LOCKED_EMAIL_DOMAIN})", "wrong-contact", None
        if local not in LOCKED_EMAIL_LOCAL:
            return "WARN", f"unrecognized email local-part: {email}", "wrong-contact", None
        return "OK", f"locked email: {email}", None, None
    if cat == "TEL":
        # Check liquid
        if HAS_LIQUID.search(val):
            if href.strip() in {"tel:" + t for t in [LIQUID_HREF.pattern]}:
                pass
            if "{{ section.settings.phone_href }}" in href:
                return "WARN", "liquid phone_href: default \"18008359565\" — missing +1 prefix vs locked tel:+18008359565 (digits match)", "tel-format", "set phone_href default to '+18008359565' OR keep as-is (browser-tolerant)"
            return "INFO", f"liquid-templated tel — runtime resolved: {href}", None, None
        tel_norm = re.sub(r'[^\d+]', '', val)
        if tel_norm == LOCKED_TEL:
            return "OK", f"locked phone: {val}", None, None
        if tel_norm == LOCKED_TEL_DIGITS:
            return "WARN", f"phone missing +1 prefix: {val} (digits OK, format inconsistent)", "tel-format", None
        return "FAIL", f"phone mismatch: {val} (expected {LOCKED_TEL})", "wrong-contact", f"replace with tel:{LOCKED_TEL}"
    if cat == "INTERNAL_PAGE":
        if val not in PAGE_INFO:
            return "FAIL", f"/pages/{val} does NOT exist on live store", "broken", None
        if not PAGE_INFO[val]["published"]:
            return "FAIL", f"/pages/{val} exists but is UNPUBLISHED ({PAGE_INFO[val]['title']})", "broken", None
        return "OK", f"/pages/{val} → {PAGE_INFO[val]['title']}", None, None
    if cat == "INTERNAL_PAGE_LIQUID":
        return "SKIP", f"liquid-templated page slug: /pages/{val}", None, None
    if cat == "INTERNAL_COLL":
        if val not in COLL_INFO:
            return "FAIL", f"/collections/{val} does NOT exist on live store", "broken", None
        return "OK", f"/collections/{val} → {COLL_INFO[val]['title']}", None, None
    if cat == "INTERNAL_COLL_LIQUID":
        return "SKIP", f"liquid-templated collection: /collections/{val}", None, None
    if cat == "INTERNAL_PROD":
        return "INFO", f"product link: /products/{val} (not checked vs live)", None, None
    if cat == "INTERNAL_PROD_LIQUID":
        return "SKIP", f"liquid-templated product: /products/{val}", None, None
    if cat == "INTERNAL_BLOG":
        parts = val.split("/")
        if parts[0] != "news":
            return "FAIL", f"unknown blog handle: /blogs/{val}", "broken", None
        return "OK", f"/blogs/{val}", None, None
    if cat == "INTERNAL_POLICY":
        return "OK", f"/policies/{val} (Shopify-managed)", None, None
    if cat == "INTERNAL_SYS":
        return "OK", "Shopify system path", None, None
    if cat == "INTERNAL_HOME":
        return "OK", "homepage", None, None
    if cat == "INTERNAL_OTHER":
        return "WARN", f"unrecognized internal path: {val}", "anchor", None
    if cat == "LIQUID" or cat == "LIQUID_MIXED":
        return "SKIP", f"pure-liquid href: {val}", None, None
    if cat == "OTHER":
        return "WARN", f"unrecognized href: {val}", "anchor", None
    return "WARN", f"unhandled category: {cat}", "anchor", None

def main():
    rows = json.loads((TMP / "all-links.json").read_text())
    out = []
    counts = {}
    for r in rows:
        cat, val = classify(r["href"])
        sev, reason, ftype, fix = validate(r["href"], cat, val)
        r2 = dict(r)
        r2["category"] = cat
        r2["resolved"] = val
        r2["severity"] = sev
        r2["reason"] = reason
        r2["finding_type"] = ftype
        r2["fix_hint"] = fix
        out.append(r2)
        counts[sev] = counts.get(sev, 0) + 1
    (TMP / "links-classified-v2.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("Severity counts:")
    for k in sorted(counts):
        print(f"  {k:6s} {counts[k]}")
    print(f"  Total: {len(out)}")
    # Surface FAILs
    print("\n=== FAIL findings ===")
    for r in out:
        if r["severity"] == "FAIL":
            print(f"  {r['file']}:{r['line']}")
            print(f"    href={r['href']!r}")
            print(f"    anchor={r['anchor']!r}")
            print(f"    reason={r['reason']}")
    # Surface WARNs by file
    print("\n=== WARN findings (grouped) ===")
    by_file = {}
    for r in out:
        if r["severity"] == "WARN":
            by_file.setdefault(r["file"], []).append(r)
    for f in sorted(by_file):
        print(f"\n  {f}:")
        for r in by_file[f]:
            print(f"    line {r['line']}: href={r['href']!r} ({r['reason']})")

if __name__ == "__main__":
    main()
