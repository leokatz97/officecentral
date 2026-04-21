"""
Breadcrumb + BreadcrumbList schema setup — no Claude API needed.

1. Adds breadcrumb section to templates/collection.json (already present on product)
2. Injects BreadcrumbList JSON-LD into sections/breadcrumb.liquid

Usage:
  python3 scripts/add-breadcrumbs.py            # dry-run
  python3 scripts/add-breadcrumbs.py --live      # writes to Shopify
"""
import json
import os
import sys
import urllib.request
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = None
with open(os.path.join(ROOT, ".env")) as f:
    for line in f:
        if line.startswith("SHOPIFY_TOKEN="):
            TOKEN = line.strip().split("=", 1)[1]
if not TOKEN:
    sys.exit("SHOPIFY_TOKEN missing from .env")

SHOP = "office-central-online.myshopify.com"
API = f"https://{SHOP}/admin/api/2024-10"
LIVE = "--live" in sys.argv

# ── Shopify helpers ───────────────────────────────────────────────────────────

def fetch_asset(theme_id, key):
    url = f"{API}/themes/{theme_id}/assets.json?asset[key]={urllib.parse.quote(key)}"
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
    return json.loads(urllib.request.urlopen(req).read())["asset"]["value"]


def put_asset(theme_id, key, value):
    body = json.dumps({"asset": {"key": key, "value": value}}).encode()
    req = urllib.request.Request(
        f"{API}/themes/{theme_id}/assets.json",
        data=body,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
        method="PUT",
    )
    return json.loads(urllib.request.urlopen(req).read())


def get_active_theme_id():
    req = urllib.request.Request(f"{API}/themes.json", headers={"X-Shopify-Access-Token": TOKEN})
    themes = json.loads(urllib.request.urlopen(req).read())["themes"]
    return next(t["id"] for t in themes if t["role"] == "main")


# ── JSON-LD snippet to append to breadcrumb.liquid ───────────────────────────

JSONLD = """
{%- comment -%}BreadcrumbList schema for Google rich results{%- endcomment -%}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{{ shop.url }}"
    }
    {%- if template contains 'product' -%}
      {%- if collection.url -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ collection.title | strip_html | json }},
      "item": "{{ shop.url }}{{ collection.url }}"
    },{
      "@type": "ListItem",
      "position": 3,
      "name": {{ product.title | strip_html | json }}
    }
      {%- else -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ product.title | strip_html | json }}
    }
      {%- endif -%}
    {%- elsif template contains 'collection' and collection.handle -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ collection.title | strip_html | json }},
      "item": "{{ shop.url }}{{ collection.url }}"
    }
    {%- elsif template contains 'page' -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ page.title | strip_html | json }},
      "item": "{{ shop.url }}{{ page.url }}"
    }
    {%- elsif template == 'article' -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ blog.title | strip_html | json }},
      "item": "{{ shop.url }}{{ blog.url }}"
    },{
      "@type": "ListItem",
      "position": 3,
      "name": {{ article.title | strip_html | json }}
    }
    {%- elsif template == 'blog' -%}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ blog.title | strip_html | json }},
      "item": "{{ shop.url }}{{ blog.url }}"
    }
    {%- endif -%}
  ]
}
</script>"""

SENTINEL = "{%- comment -%}BreadcrumbList schema"

# ── New breadcrumb section definition for collection template ─────────────────

BREADCRUMB_SECTION = {
    "type": "breadcrumb",
    "settings": {
        "section_visibility": "always",
        "color_scheme": "primary",
        "enable_gradient": False,
        "top_space_desktop": 20,
        "bottom_space_desktop": 10,
        "top_space_mobile": 10,
        "bottom_space_mobile": 10,
    },
}

# ── Main ──────────────────────────────────────────────────────────────────────

print("Fetching active theme...")
theme_id = get_active_theme_id()
print(f"  Theme ID: {theme_id}")

# --- Step 1: collection template ---
print("\n[1/2] Collection template")
col_raw = fetch_asset(theme_id, "templates/collection.json")
col = json.loads(col_raw)

if "breadcrumb" in col["sections"]:
    print("  Already has breadcrumb — skipping")
    col_changed = False
else:
    col["sections"]["breadcrumb"] = BREADCRUMB_SECTION
    col["order"] = ["breadcrumb"] + col["order"]
    col_changed = True
    print("  Will prepend breadcrumb section")

# --- Step 2: breadcrumb.liquid ---
print("\n[2/2] breadcrumb.liquid")
bc_raw = fetch_asset(theme_id, "sections/breadcrumb.liquid")

if SENTINEL in bc_raw:
    print("  JSON-LD already present — skipping")
    bc_changed = False
else:
    # Insert before {% schema %} so it's inside the section render
    schema_pos = bc_raw.find("{% schema %}")
    if schema_pos == -1:
        bc_new = bc_raw + JSONLD
    else:
        bc_new = bc_raw[:schema_pos] + JSONLD + "\n" + bc_raw[schema_pos:]
    bc_changed = True
    print("  Will inject BreadcrumbList JSON-LD")

if not col_changed and not bc_changed:
    print("\nNothing to do — both already up to date.")
    sys.exit(0)

if not LIVE:
    print("\nDry run complete. Run with --live to apply.")
    sys.exit(0)

print("\nApplying...")
if col_changed:
    put_asset(theme_id, "templates/collection.json", json.dumps(col, indent=2))
    print("  ✓ collection.json updated")

if bc_changed:
    put_asset(theme_id, "sections/breadcrumb.liquid", bc_new)
    print("  ✓ breadcrumb.liquid updated")

print("\nDone.")
