#!/usr/bin/env python3
"""Fetch current HTML descriptions for 5 sample products we're rewriting."""
import json
import os
import sys
import urllib.request

TOKEN = None
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("SHOPIFY_TOKEN="):
            TOKEN = line.strip().split("=", 1)[1]
            break
if not TOKEN:
    sys.exit("SHOPIFY_TOKEN missing from .env")

SHOP = "office-central-online.myshopify.com"
API = f"https://{SHOP}/admin/api/2024-10"

SAMPLES = [
    (9666764865849, "L-Shape Desk & Hutch"),
    (9499674050873, "U-Shape Height Adjust Desk"),
    (9114485391673, "Premium Series Lateral File Cabinet"),
    (9039326609721, "ObusForme Comfort High back Chair 1240-3"),
    (9686674637113, "Training Flip Top Tables"),
]

def fetch(pid):
    req = urllib.request.Request(
        f"{API}/products/{pid}.json",
        headers={"X-Shopify-Access-Token": TOKEN, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["product"]

out = []
for pid, label in SAMPLES:
    p = fetch(pid)
    out.append({
        "id": pid,
        "label": label,
        "title": p.get("title"),
        "handle": p.get("handle"),
        "vendor": p.get("vendor"),
        "product_type": p.get("product_type"),
        "tags": p.get("tags"),
        "body_html": p.get("body_html") or "",
        "variants_count": len(p.get("variants", [])),
        "price_range": [
            min((float(v["price"]) for v in p.get("variants", [])), default=None),
            max((float(v["price"]) for v in p.get("variants", [])), default=None),
        ],
        "option_names": [o.get("name") for o in p.get("options", [])],
    })

with open(os.path.join(os.path.dirname(ENV_PATH), "sample-products-current.json"), "w") as f:
    json.dump(out, f, indent=2)

print(f"Fetched {len(out)} products.")
for item in out:
    body_len = len(item["body_html"])
    print(f" - {item['label']}: {body_len} chars HTML, {item['variants_count']} variants, ${item['price_range'][0]}–${item['price_range'][1]}")
