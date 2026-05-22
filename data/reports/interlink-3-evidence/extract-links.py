#!/usr/bin/env python3
"""Extract <a href="..."> + anchor text from BBI theme files for INTERLINK-3 audit."""
import re
import json
import os
from pathlib import Path

ROOT = Path("/Users/leokatz/Desktop/Office Central")
THEME = ROOT / "theme"

# Files in scope
SCOPE_GLOBS = [
    "sections/ds-*.liquid",
    "snippets/bbi-*.liquid",
    "templates/page.*.json",
    "templates/collection.*.json",
    "templates/index.json",
    "templates/blog.json",
    "templates/article.json",
]

# Anchor-tag regex (greedy + DOTALL to capture multiline anchors)
ANCHOR_RE = re.compile(
    r'<a\b([^>]*?)href\s*=\s*(["\'])(.*?)\2([^>]*)>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
# Liquid link_to / form-action hrefs not in <a> are out of scope here.

# JSON file href values (settings)
JSON_HREF_RE = re.compile(
    r'"(href|link|cta_url|button_link|menu_url|url|product|product_card|tile_\d+_url)"\s*:\s*"([^"]+)"',
    re.IGNORECASE,
)

def strip_text(t):
    """Strip HTML/Liquid tags and collapse whitespace from anchor text."""
    # Remove HTML tags
    t = re.sub(r'<[^>]+>', ' ', t)
    # Remove liquid tags + output
    t = re.sub(r'\{\%.*?\%\}', ' ', t, flags=re.DOTALL)
    t = re.sub(r'\{\{.*?\}\}', '<LIQUID>', t, flags=re.DOTALL)
    # Collapse whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def line_for_offset(text, offset):
    return text.count('\n', 0, offset) + 1

def collect():
    rows = []
    for pattern in SCOPE_GLOBS:
        for f in sorted((THEME).glob(pattern)):
            rel = str(f.relative_to(ROOT))
            try:
                src = f.read_text(encoding='utf-8')
            except Exception as e:
                print(f"skip {rel}: {e}")
                continue
            if f.suffix == ".liquid":
                for m in ANCHOR_RE.finditer(src):
                    href = m.group(3)
                    anchor = strip_text(m.group(5))
                    rows.append({
                        "file": rel,
                        "line": line_for_offset(src, m.start()),
                        "href": href,
                        "anchor": anchor[:200],
                    })
            elif f.suffix == ".json":
                # JSON templates: capture settings.href / button_link / cta_url etc
                for m in JSON_HREF_RE.finditer(src):
                    rows.append({
                        "file": rel,
                        "line": line_for_offset(src, m.start()),
                        "href": m.group(2),
                        "anchor": f"[JSON settings: {m.group(1)}]",
                    })
    return rows

if __name__ == "__main__":
    rows = collect()
    out = ROOT / "data/reports/interlink-3-tmp/all-links.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"Extracted {len(rows)} link rows -> {out}")
    # Quick summary by file
    by_file = {}
    for r in rows:
        by_file[r["file"]] = by_file.get(r["file"], 0) + 1
    for f in sorted(by_file):
        print(f"  {by_file[f]:4d}  {f}")
