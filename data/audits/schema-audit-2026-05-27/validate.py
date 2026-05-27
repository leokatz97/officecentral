#!/usr/bin/env python3
"""
HOTFIX-SCHEMA-AUDIT-1 (Phase 1b) — deep-validate captured JSON-LD against
Schema.org required/recommended properties + BBI brand-identity invariants.
"""
import json, sys
from pathlib import Path

CAPS = Path(__file__).parent / "captures"

BBI_CANONICAL = {
    "name": "Brant Business Interiors",
    "alt": "BBI",
    "tel": "+1-800-835-9565",
    "address": "296 George St N",
    "city": "Peterborough",
    "postal": "K9J 3H2",
    "agreement": "2025-470",
    "founded": "1964",
}

# Required+recommended per Google rich result + schema.org
REQS = {
    "Organization": {"required": ["name", "url"], "recommended": ["logo", "sameAs", "description"]},
    "LocalBusiness": {"required": ["name", "address"], "recommended": ["telephone", "url", "openingHours", "geo", "priceRange"]},
    "Product": {"required": ["name", "image", "offers"], "recommended": ["brand", "sku", "description", "review", "aggregateRating"]},
    "Offer": {"required": ["price", "priceCurrency"], "recommended": ["availability", "url", "priceValidUntil", "seller"]},
    "BreadcrumbList": {"required": ["itemListElement"], "recommended": []},
    "FAQPage": {"required": ["mainEntity"], "recommended": []},
    "Service": {"required": ["name", "provider"], "recommended": ["areaServed", "serviceType", "description", "offers"]},
    "GovernmentService": {"required": ["name", "provider", "serviceType"], "recommended": ["areaServed", "description"]},
    "Article": {"required": ["headline", "image", "datePublished", "author"], "recommended": ["dateModified", "publisher"]},
    "BlogPosting": {"required": ["headline", "image", "datePublished", "author"], "recommended": ["dateModified", "publisher", "mainEntityOfPage"]},
    "HowTo": {"required": ["name", "step"], "recommended": ["description", "image", "totalTime", "estimatedCost"]},
    "WebSite": {"required": ["url", "name"], "recommended": ["potentialAction", "publisher"]},
}

def get_type(node):
    t = node.get("@type") if isinstance(node, dict) else None
    if isinstance(t, list):
        return t
    return [t] if t else []

def flatten_nodes(data):
    """Yield (path, node) for every @type-bearing dict in the JSON-LD tree."""
    def walk(obj, path):
        if isinstance(obj, dict):
            if "@graph" in obj and isinstance(obj["@graph"], list):
                for i, sub in enumerate(obj["@graph"]):
                    yield from walk(sub, f"{path}@graph[{i}]/")
            if "@type" in obj:
                yield (path, obj)
            for k, v in obj.items():
                if k in ("@graph",): continue
                yield from walk(v, path + k + "/")
        elif isinstance(obj, list):
            for i, sub in enumerate(obj):
                yield from walk(sub, f"{path}[{i}]/")
    yield from walk(data, "")

def check_node(path, node, issues, surface):
    types = get_type(node)
    for t in types:
        if t not in REQS:
            continue
        for p in REQS[t]["required"]:
            if p not in node or node.get(p) in (None, "", [], {}):
                issues.append({"sev":"CRIT","surface":surface,"path":path,"type":t,"issue":f"missing required: {p}"})
        for p in REQS[t]["recommended"]:
            if p not in node or node.get(p) in (None, "", [], {}):
                issues.append({"sev":"WARN","surface":surface,"path":path,"type":t,"issue":f"missing recommended: {p}"})

def bbi_identity_check(surface, blocks, issues):
    """Sweep the whole capture for brand-identity invariants."""
    txt = json.dumps(blocks)
    if "Brant Business Interiors" not in txt and surface not in ("404",):
        issues.append({"sev":"CRIT","surface":surface,"path":"<page>","type":"identity","issue":"Brand name 'Brant Business Interiors' missing entirely"})
    if "BBI" in txt:
        if '"name": "BBI"' in txt or '"name":"BBI"' in txt:
            issues.append({"sev":"CRIT","surface":surface,"path":"<page>","type":"identity","issue":"Schema emits 'BBI' as primary name (must be alternateName only)"})

def main():
    summary = json.loads((CAPS / "_summary.json").read_text())
    all_issues = []

    for s in summary:
        surface = s["slug"]
        if s["status"] != 200:
            if surface == "404":
                all_issues.append({"sev":"INFO","surface":surface,"path":"<page>","type":"404","issue":"404 page emits NO JSON-LD (expected: bbi-nav→org-schema + bbi-localbusiness-schema)"})
            continue
        blocks_path = CAPS / f"{surface}.jsonld.json"
        if not blocks_path.exists():
            continue
        blocks = json.loads(blocks_path.read_text())
        bbi_identity_check(surface, blocks, all_issues)

        # Check for duplicate Organization / WebSite / LocalBusiness emitters
        org_count = 0; lb_count = 0; ws_count = 0
        for blk in blocks:
            for _, node in flatten_nodes(blk):
                types = get_type(node)
                if "Organization" in types: org_count += 1
                if "LocalBusiness" in types: lb_count += 1
                if "WebSite" in types: ws_count += 1
        if org_count > 1:
            all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"Organization","issue":f"Emitted {org_count}× — possible duplicate"})
        if lb_count > 2:  # combined org+LB + dedicated LB = 2 expected
            all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"LocalBusiness","issue":f"Emitted {lb_count}× — expected exactly 2 (combined + dedicated)"})
        if ws_count > 1:
            all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"WebSite","issue":f"Emitted {ws_count}× — duplicate"})

        # Check required/recommended on every node
        for blk in blocks:
            for path, node in flatten_nodes(blk):
                check_node(path, node, all_issues, surface)

        # PDP-specific deep checks
        if surface.startswith("pdp"):
            for blk in blocks:
                for path, node in flatten_nodes(blk):
                    if "Product" in get_type(node):
                        offers = node.get("offers")
                        if isinstance(offers, dict):
                            if "priceValidUntil" not in offers:
                                all_issues.append({"sev":"WARN","surface":surface,"path":path+"offers/","type":"Offer","issue":"missing priceValidUntil (Merchant Listing requirement)"})
                            if "itemCondition" not in node and "itemCondition" not in offers:
                                all_issues.append({"sev":"WARN","surface":surface,"path":path,"type":"Product","issue":"missing itemCondition"})
                            if "hasMerchantReturnPolicy" not in offers:
                                all_issues.append({"sev":"WARN","surface":surface,"path":path+"offers/","type":"Offer","issue":"missing hasMerchantReturnPolicy (Merchant Listings rich result)"})
                            if "shippingDetails" not in offers:
                                all_issues.append({"sev":"WARN","surface":surface,"path":path+"offers/","type":"Offer","issue":"missing shippingDetails (Merchant Listings rich result)"})
                        if "aggregateRating" not in node and "review" not in node:
                            all_issues.append({"sev":"INFO","surface":surface,"path":path,"type":"Product","issue":"no aggregateRating/review (no review data in store; not necessarily a defect)"})

        # Surface-specific gaps
        if surface.startswith("collection-"):
            has_itemlist = any(
                "ItemList" in get_type(n) or "CollectionPage" in get_type(n)
                for blk in blocks for _, n in flatten_nodes(blk)
            )
            if not has_itemlist:
                all_issues.append({"sev":"CRIT","surface":surface,"path":"<page>","type":"CollectionPage","issue":"No ItemList or CollectionPage schema (missing product carousel rich result eligibility)"})

        if surface == "blog":
            has_blog = any("Blog" in get_type(n) for blk in blocks for _, n in flatten_nodes(blk))
            if not has_blog:
                all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"Blog","issue":"Blog landing page emits no Blog schema (ds-blog-list missing schema)"})

        if surface.startswith("page-brands"):
            has_brand = any(any(t in get_type(n) for t in ("Brand","Organization")) and n.get("name","").lower() != "brant business interiors"
                           for blk in blocks for _, n in flatten_nodes(blk))
            if not has_brand:
                all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"Brand","issue":"Brand landing page emits no Brand schema for the featured manufacturer"})

        if surface in ("page-healthcare","page-education","page-government","page-non-profit","page-professional-services","page-industries"):
            has_service = any(any(t in get_type(n) for t in ("Service","GovernmentService")) for blk in blocks for _, n in flatten_nodes(blk))
            if not has_service:
                all_issues.append({"sev":"CRIT","surface":surface,"path":"<page>","type":"Service","issue":"Industry/service landing page has no Service/GovernmentService schema (high-value B2B page, no rich result eligibility)"})

        if surface in ("page-about","page-contact","page-our-work","page-customer-stories","page-faq","page-industries","page-brands"):
            has_webpage = any("WebPage" in get_type(n) or "AboutPage" in get_type(n) or "ContactPage" in get_type(n)
                             for blk in blocks for _, n in flatten_nodes(blk))
            if not has_webpage and surface in ("page-about","page-contact"):
                all_issues.append({"sev":"WARN","surface":surface,"path":"<page>","type":"WebPage","issue":"page emits no AboutPage/ContactPage schema (entity-level signal)"})

    # Group + emit
    by_sev = {"CRIT":[], "WARN":[], "INFO":[]}
    for i in all_issues:
        by_sev[i["sev"]].append(i)

    out = {"by_severity": by_sev, "all": all_issues, "count": len(all_issues)}
    (CAPS.parent / "validation-issues.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"Total issues: {len(all_issues)}  (CRIT={len(by_sev['CRIT'])}  WARN={len(by_sev['WARN'])}  INFO={len(by_sev['INFO'])})\n")
    for sev in ("CRIT","WARN","INFO"):
        print(f"---- {sev} ----")
        seen = {}
        for i in by_sev[sev]:
            k = (i["type"], i["issue"])
            seen.setdefault(k, []).append(i["surface"])
        for (t, msg), surfaces in sorted(seen.items()):
            print(f"  [{t}] {msg}")
            print(f"     → {', '.join(sorted(set(surfaces)))}")
        print()

if __name__ == "__main__":
    main()
