#!/usr/bin/env python3
"""Fetch all collection handles + page handles from Shopify Admin API."""
import os
import json
import urllib.request
from pathlib import Path

TOKEN = os.environ["SHOPIFY_TOKEN"]
STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
OUT = Path("/Users/leokatz/Desktop/Office Central/data/reports/interlink-3-tmp")

def fetch_all(endpoint, key, fields="id,handle,title"):
    items = []
    page_info = None
    while True:
        url = f"https://{STORE}/admin/api/{API_VERSION}/{endpoint}.json?limit=250&fields={fields}"
        if page_info:
            url += f"&page_info={page_info}"
        req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        items.extend(data[key])
        link = resp.headers.get("Link", "")
        if 'rel="next"' in link:
            import re
            m = re.search(r'<[^>]+page_info=([^&>]+)[^>]*>;\s*rel="next"', link)
            page_info = m.group(1) if m else None
            if not page_info:
                break
        else:
            break
    return items

print("Fetching smart collections…")
smart = fetch_all("smart_collections", "smart_collections")
print(f"  {len(smart)} smart collections")
print("Fetching custom collections…")
custom = fetch_all("custom_collections", "custom_collections")
print(f"  {len(custom)} custom collections")
print("Fetching pages…")
pages = fetch_all("pages", "pages", fields="id,handle,title,published_at")
print(f"  {len(pages)} pages")

# Combine collections
all_collections = []
for c in smart:
    all_collections.append({**c, "type": "smart"})
for c in custom:
    all_collections.append({**c, "type": "custom"})

(OUT / "live-collections.json").write_text(json.dumps(all_collections, indent=2))
(OUT / "live-pages.json").write_text(json.dumps(pages, indent=2))

# Write handle-only sets for quick lookup
collection_handles = sorted({c["handle"] for c in all_collections})
page_handles = sorted({p["handle"] for p in pages})
(OUT / "live-collection-handles.txt").write_text("\n".join(collection_handles))
(OUT / "live-page-handles.txt").write_text("\n".join(page_handles))
print(f"\n{len(collection_handles)} collection handles, {len(page_handles)} page handles written")
