"""
Layer A tag cleanup — strip all non-vocabulary tags from every product.

Approved vocabulary (keep):
  type:*   room:*   industry:*   bestseller   hero

Everything else is legacy noise and gets removed.

Usage:
  python3 scripts/clean-legacy-tags.py            # dry-run, shows diff
  python3 scripts/clean-legacy-tags.py --live     # writes to Shopify
"""
import json
import os
import sys
import time
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


def is_approved(tag: str) -> bool:
    t = tag.strip()
    return (
        t.startswith("type:")
        or t.startswith("room:")
        or t.startswith("industry:")
        or t == "bestseller"
        or t == "hero"
    )


def shopify_get(path):
    req = urllib.request.Request(
        f"{API}{path}",
        headers={"X-Shopify-Access-Token": TOKEN},
    )
    return json.loads(urllib.request.urlopen(req).read())


def shopify_put(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
        },
        method="PUT",
    )
    return json.loads(urllib.request.urlopen(req).read())


def fetch_all_products():
    products = []
    url = f"{API}/products.json?limit=250&fields=id,title,tags"
    while url:
        req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        products.extend(data["products"])
        link = resp.headers.get("Link", "")
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part.strip().split("<")[1].split(">")[0]
    return products


print("Fetching all products...")
products = fetch_all_products()
print(f"  {len(products)} products loaded")

to_update = []
removed_tags = {}

for p in products:
    original = [t.strip() for t in p["tags"].split(",") if t.strip()]
    cleaned = [t for t in original if is_approved(t)]
    stripped = [t for t in original if not is_approved(t)]
    if stripped:
        to_update.append((p["id"], p["title"], original, cleaned))
        for t in stripped:
            removed_tags[t] = removed_tags.get(t, 0) + 1

print(f"\n{'DRY RUN — ' if not LIVE else ''}Products with legacy tags to strip: {len(to_update)}")
print(f"\nTags being removed (tag → count):")
for tag, count in sorted(removed_tags.items(), key=lambda x: -x[1]):
    print(f"  {count:4d}  {tag}")

if not to_update:
    print("\nNothing to do — all tags are already clean.")
    sys.exit(0)

if not LIVE:
    print(f"\nSample diffs (first 5):")
    for pid, title, before, after in to_update[:5]:
        removed = set(before) - set(after)
        print(f"  {title[:50]}")
        print(f"    remove: {', '.join(sorted(removed))}")
    print(f"\nRun with --live to apply to all {len(to_update)} products.")
    sys.exit(0)

print(f"\nApplying to {len(to_update)} products...")
ok = 0
fail = 0
for i, (pid, title, before, after) in enumerate(to_update, 1):
    try:
        shopify_put(f"/products/{pid}.json", {"product": {"id": pid, "tags": ", ".join(after)}})
        ok += 1
        print(f"  [{i}/{len(to_update)}] ✓ {title[:50]}")
    except Exception as e:
        fail += 1
        print(f"  [{i}/{len(to_update)}] ✗ {title[:50]} — {e}")
    time.sleep(0.5)

print(f"\nDone. {ok} updated, {fail} failed.")
