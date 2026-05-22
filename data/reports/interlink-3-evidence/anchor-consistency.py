#!/usr/bin/env python3
"""Group links by destination, surface anchor-text inconsistencies as WARN."""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/leokatz/Desktop/Office Central")
TMP = ROOT / "data/reports/interlink-3-tmp"

data = json.loads((TMP / "links-classified-v2.json").read_text())

# Group only resolved internal BBI links (pages + collections + home)
INTERNAL_CATS = {"INTERNAL_PAGE", "INTERNAL_COLL", "INTERNAL_HOME", "INTERNAL_BLOG"}

# Recommended canonical anchor text per high-value destination
CANONICAL = {
    "/pages/oecm": ["OECM purchasing", "OECM Agreement 2025-470", "Our OECM page", "OECM"],
    "/pages/quote": ["Get a quote", "Request a quote", "Request a Quote"],
    "/pages/delivery": ["Delivery + installation", "Delivery", "Delivery & installation"],
    "/pages/design-services": ["Design services", "Free design services"],
    "/pages/relocation": ["Office relocation", "Relocation"],
    "/pages/about": ["About", "About Brant Business Interiors", "About us"],
    "/pages/contact": ["Contact", "Contact us"],
    "/pages/customer-stories": ["Customer stories", "Case studies"],
    "/pages/our-work": ["Our work", "Project gallery"],
    "/pages/faq": ["FAQ"],
    "/pages/industries": ["Industries"],
    "/pages/healthcare": ["Healthcare"],
    "/pages/education": ["Education"],
    "/pages/government": ["Government"],
    "/pages/non-profit": ["Non-profit"],
    "/pages/professional-services": ["Professional services"],
    "/pages/brands": ["Brands"],
    "/collections/seating": ["Office seating", "Browse seating", "Seating"],
    "/collections/desks": ["Browse desks", "Desks"],
    "/collections/storage": ["Browse storage", "Storage"],
    "/collections/tables": ["Browse tables", "Tables"],
    "/collections/boardroom": ["Browse boardroom", "Boardroom"],
    "/collections/accessories": ["Browse accessories", "Accessories"],
    "/collections/ergonomic-products": ["Browse ergonomic", "Ergonomic products"],
    "/collections/panels-room-dividers": ["Browse panels", "Panels & room dividers"],
    "/collections/quiet-spaces": ["Browse quiet spaces", "Quiet spaces"],
}

NOISE_RE = re.compile(r'<LIQUID>|&[a-z#0-9]+;|\s+')

def normalize(t):
    """Loose normalize for anchor-text comparison."""
    if not t:
        return ""
    t = NOISE_RE.sub(' ', t)
    t = re.sub(r'[‘’]', "'", t)
    t = re.sub(r'[“”]', '"', t)
    t = t.strip().lower()
    # Strip punctuation at edges
    t = re.sub(r'^[^\w]+|[^\w]+$', '', t)
    return t

# Build destination → list of (anchor, file, line) tuples
dest_map = defaultdict(list)
for r in data:
    if r["category"] not in INTERNAL_CATS:
        continue
    # Build canonical destination key
    if r["category"] == "INTERNAL_PAGE":
        dest = "/pages/" + r["resolved"]
    elif r["category"] == "INTERNAL_COLL":
        dest = "/collections/" + r["resolved"]
    elif r["category"] == "INTERNAL_HOME":
        dest = "/"
    elif r["category"] == "INTERNAL_BLOG":
        dest = "/blogs/" + r["resolved"]
    else:
        continue
    anchor = r["anchor"] or ""
    if not anchor:
        continue
    dest_map[dest].append({
        "file": r["file"], "line": r["line"], "anchor": anchor, "normalized": normalize(anchor),
    })

inconsistencies = []
for dest, entries in sorted(dest_map.items()):
    if len(entries) < 2:
        continue
    norms = {e["normalized"] for e in entries if e["normalized"]}
    if len(norms) <= 1:
        continue
    inconsistencies.append({
        "destination": dest,
        "anchor_count": len({e["normalized"] for e in entries}),
        "entry_count": len(entries),
        "anchors": entries,
    })

# Sort by impact: highest unique-anchor count first
inconsistencies.sort(key=lambda x: (-x["anchor_count"], -x["entry_count"], x["destination"]))

(TMP / "anchor-inconsistencies.json").write_text(json.dumps(inconsistencies, indent=2, ensure_ascii=False))

print(f"Total destinations with 2+ source links: {sum(1 for d, e in dest_map.items() if len(e) >= 2)}")
print(f"Destinations with inconsistent anchor text: {len(inconsistencies)}")
print()
for inc in inconsistencies[:25]:
    print(f"\n── {inc['destination']}  ({inc['anchor_count']} unique anchors / {inc['entry_count']} links)")
    seen = set()
    for e in inc["anchors"]:
        key = e["normalized"]
        if key in seen:
            continue
        seen.add(key)
        recs = CANONICAL.get(inc["destination"], [])
        rec_marker = "  ★ matches canonical" if any(normalize(c) == key for c in recs) else ""
        print(f"    {e['file']}:{e['line']}  \"{e['anchor'][:90]}\"{rec_marker}")
    if CANONICAL.get(inc["destination"]):
        print(f"    → recommend: \"{CANONICAL[inc['destination']][0]}\"")

if len(inconsistencies) > 25:
    print(f"\n... ({len(inconsistencies) - 25} more inconsistencies — full list in anchor-inconsistencies.json)")
