#!/usr/bin/env python3
"""Phase 4 v2: missing CONTEXTUAL (body-level) cross-links.
Body-level = links emitted from the page's own ds-lp-*.liquid section + its page.*.json
settings. Excludes nav, footer, crumbs (global chrome).
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/leokatz/Desktop/Office Central")
TMP = ROOT / "data/reports/interlink-3-tmp"

data = json.loads((TMP / "links-classified-v2.json").read_text())

SECTION_TO_PAGE = {
    "theme/sections/ds-lp-oecm.liquid": "/pages/oecm",
    "theme/sections/ds-lp-quote.liquid": "/pages/quote",
    "theme/sections/ds-lp-delivery.liquid": "/pages/delivery",
    "theme/sections/ds-lp-design-services.liquid": "/pages/design-services",
    "theme/sections/ds-lp-relocation.liquid": "/pages/relocation",
    "theme/sections/ds-lp-customer-stories.liquid": "/pages/customer-stories",
    "theme/sections/ds-lp-our-work.liquid": "/pages/our-work",
    "theme/sections/ds-lp-about.liquid": "/pages/about",
    "theme/sections/ds-lp-contact.liquid": "/pages/contact",
    "theme/sections/ds-lp-faq.liquid": "/pages/faq",
    "theme/sections/ds-lp-healthcare.liquid": "/pages/healthcare",
    "theme/sections/ds-lp-education.liquid": "/pages/education",
    "theme/sections/ds-lp-government.liquid": "/pages/government",
    "theme/sections/ds-lp-non-profit.liquid": "/pages/non-profit",
    "theme/sections/ds-lp-professional-services.liquid": "/pages/professional-services",
    "theme/sections/ds-lp-industries.liquid": "/pages/industries",
    "theme/sections/ds-lp-brands.liquid": "/pages/brands",
    "theme/sections/ds-lp-brands-ergocentric.liquid": "/pages/brands-ergocentric",
    "theme/sections/ds-lp-brands-otg.liquid": "/pages/brands-otg",
    "theme/sections/ds-lp-brands-global-teknion.liquid": "/pages/brands-global-teknion",
    "theme/sections/ds-lp-brands-heartwood.liquid": "/pages/brands-heartwood",
    "theme/sections/ds-lp-brands-keilhauer.liquid": "/pages/brands-keilhauer",
    "theme/sections/ds-lp-brands-obusforme.liquid": "/pages/brands-obusforme",
}

TEMPLATE_TO_PAGE = {
    "theme/templates/" + Path(f).name: SECTION_TO_PAGE[f].replace("/sections/ds-lp-", "").replace(".liquid", "")
    for f in SECTION_TO_PAGE
}
# Build correct template -> page mapping
TEMPLATE_TO_PAGE = {}
for f, p in SECTION_TO_PAGE.items():
    slug = p.replace("/pages/", "")
    TEMPLATE_TO_PAGE[f"theme/templates/page.{slug}.json"] = p

INTERNAL_CATS = {"INTERNAL_PAGE", "INTERNAL_COLL", "INTERNAL_HOME", "INTERNAL_BLOG"}

def dest_from(r):
    if r["category"] == "INTERNAL_PAGE":
        return "/pages/" + r["resolved"]
    if r["category"] == "INTERNAL_COLL":
        return "/collections/" + r["resolved"]
    if r["category"] == "INTERNAL_HOME":
        return "/"
    if r["category"] == "INTERNAL_BLOG":
        return "/blogs/" + r["resolved"]
    return None

# Body-level outbound = section .liquid + template .json
page_outbound = defaultdict(set)
for r in data:
    if r["category"] not in INTERNAL_CATS:
        continue
    dest = dest_from(r)
    if not dest:
        continue
    if r["file"] in SECTION_TO_PAGE:
        page_outbound[SECTION_TO_PAGE[r["file"]]].add(dest)
    elif r["file"] in TEMPLATE_TO_PAGE:
        page_outbound[TEMPLATE_TO_PAGE[r["file"]]].add(dest)

# Expected from spec
EXPECTED = {
    "/pages/oecm": {
        "HIGH": ["/pages/quote", "/pages/education", "/pages/healthcare", "/pages/government", "/pages/about"],
    },
    "/pages/healthcare": {
        "HIGH": ["/pages/oecm", "/pages/quote", "/collections/seating", "/collections/ergonomic-products"],
    },
    "/pages/education": {
        "HIGH": ["/pages/oecm", "/pages/quote"],
    },
    "/pages/government": {
        "HIGH": ["/pages/oecm", "/pages/quote"],
    },
    "/pages/non-profit": {
        "HIGH": ["/pages/oecm", "/pages/quote"],
    },
    "/pages/professional-services": {
        "HIGH": ["/pages/quote"],
    },
    "/pages/quote": {
        "HIGH": ["/pages/oecm", "/pages/delivery", "/pages/design-services"],
    },
    "/pages/delivery": {
        "HIGH": ["/pages/quote"],
        "LOW":  ["/pages/customer-stories", "/pages/our-work"],
    },
    "/pages/design-services": {
        "HIGH": ["/pages/quote"],
        "LOW":  ["/pages/relocation"],
    },
    "/pages/relocation": {
        "HIGH": ["/pages/design-services", "/pages/delivery", "/pages/quote"],
    },
    "/pages/brands-otg":          {"HIGH": ["/pages/quote", "/pages/brands"]},
    "/pages/brands-ergocentric":  {"HIGH": ["/pages/quote", "/pages/brands"]},
    "/pages/brands-global-teknion":{"HIGH": ["/pages/quote", "/pages/brands"]},
    "/pages/brands-heartwood":    {"HIGH": ["/pages/quote", "/pages/brands"]},
    "/pages/brands-keilhauer":    {"HIGH": ["/pages/quote", "/pages/brands"]},
    "/pages/brands-obusforme":    {"HIGH": ["/pages/quote", "/pages/brands"]},
}

findings = []
for page, exp_map in EXPECTED.items():
    body = page_outbound[page]
    for sev, dests in exp_map.items():
        for dest in dests:
            if dest not in body:
                findings.append({"page": page, "missing": dest, "severity": sev})

print(f"Total INFO findings (body-level missing cross-links): {len(findings)}")
high = [f for f in findings if f["severity"] == "HIGH"]
low = [f for f in findings if f["severity"] == "LOW"]
print(f"  HIGH: {len(high)}   LOW: {len(low)}")
print()
print("--- HIGH ---")
by_page = defaultdict(list)
for f in high:
    by_page[f["page"]].append(f["missing"])
for page in sorted(by_page):
    print(f"  {page}: missing → {', '.join(by_page[page])}")
print("\n--- LOW ---")
by_page = defaultdict(list)
for f in low:
    by_page[f["page"]].append(f["missing"])
for page in sorted(by_page):
    print(f"  {page}: missing → {', '.join(by_page[page])}")

(TMP / "missing-links-v2.json").write_text(json.dumps({
    "findings": findings,
    "page_outbound_body_level": {k: sorted(v) for k, v in page_outbound.items()},
}, indent=2, ensure_ascii=False))
