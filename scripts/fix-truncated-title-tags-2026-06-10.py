#!/usr/bin/env python3
"""Repair the 2 hard-clamped global.title_tag metafields (desks collection +
News blog) so the stored SEO title / og:title match the now-clean rendered
<title>. Admin-API, theme-independent. Backup -> write -> exact-match readback.
"""
import json, os, sys, urllib.request, datetime

TOKEN = os.environ["SHOPIFY_TOKEN"]
SHOP = "office-central-online.myshopify.com"
URL = f"https://{SHOP}/admin/api/2024-10/graphql.json"

TARGETS = [
    {"label": "desks collection", "ownerId": "gid://shopify/Collection/526847344953",
     "new": "Office Desks & Workstations Ontario"},
    {"label": "News blog",        "ownerId": "gid://shopify/Blog/108557861177",
     "new": "Office Furniture News & Buying Guides"},
]


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


READ = """query($id: ID!){ node(id:$id){
  ... on Collection { handle metafield(namespace:"global",key:"title_tag"){value type} seo{title} }
  ... on Blog       { handle metafield(namespace:"global",key:"title_tag"){value type} }
}}"""


def read_value(owner_id):
    d = gql(READ, {"id": owner_id})["data"]["node"]
    return d.get("metafield", {}).get("value") if d.get("metafield") else None


# 1. Backup
backup = {"timestamp": datetime.datetime.now().isoformat(), "before": {}}
for t in TARGETS:
    backup["before"][t["ownerId"]] = {"label": t["label"], "value": read_value(t["ownerId"])}
stamp = "20260610"
bpath = f"data/backups/title-tag-fix-{stamp}.json"
os.makedirs("data/backups", exist_ok=True)
with open(bpath, "w") as f:
    json.dump(backup, f, indent=2)
print("BACKUP ->", bpath)
for k, v in backup["before"].items():
    print(f"  before [{v['label']}] {v['value']!r}")

if "--live" not in sys.argv:
    print("\nDRY RUN (pass --live to write). Proposed:")
    for t in TARGETS:
        print(f"  [{t['label']}] -> {t['new']!r}")
    sys.exit(0)

# 2. Write
MUT = """mutation($mf:[MetafieldsSetInput!]!){
  metafieldsSet(metafields:$mf){
    metafields{ id namespace key value ownerType }
    userErrors{ field message code }
  }
}"""
mfs = [{"ownerId": t["ownerId"], "namespace": "global", "key": "title_tag",
        "type": "single_line_text_field", "value": t["new"]} for t in TARGETS]
res = gql(MUT, {"mf": mfs})
errs = res["data"]["metafieldsSet"]["userErrors"]
if errs:
    print("USER ERRORS:", errs); sys.exit(1)
print("\nWRITE ok, 0 userErrors")

# 3. Exact-match readback
print("\nREADBACK:")
allok = True
for t in TARGETS:
    got = read_value(t["ownerId"])
    ok = got == t["new"]
    allok &= ok
    print(f"  [{t['label']}] {'EXACT MATCH' if ok else 'MISMATCH'} -> {got!r}")
sys.exit(0 if allok else 2)
