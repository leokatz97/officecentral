"""
Update the BBI homepage: hero slideshow + trust strip.

Changes (dry-run by default):
  1. Enable the slideshow section (currently disabled)
  2. Slide 1 (Teknion video): add headline, subheading, description, CTA
  3. Slide 2 (blank template): disable it
  4. Trust strip: fix trailing comma, update to "Since 1964", "Ships Across Canada",
     "PO & NET 30 Accepted", "Free Design Layouts"

Usage:
  python3 scripts/update-homepage.py          # dry-run — prints changes only
  python3 scripts/update-homepage.py --live   # pushes to Shopify
"""
import json, os, sys, urllib.request, urllib.parse, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, ".env")) as f:
    env = dict(l.strip().split("=", 1) for l in f if "=" in l)

TOKEN = env["SHOPIFY_TOKEN"]
SHOP  = "office-central-online.myshopify.com"
THEME = "178274435385"
API   = f"https://{SHOP}/admin/api/2024-10"
LIVE  = "--live" in sys.argv

HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# ── fetch current index.json ─────────────────────────────────────────────────

def get_asset(key):
    url = f"{API}/themes/{THEME}/assets.json?asset[key]={urllib.parse.quote(key)}"
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
    return json.loads(urllib.request.urlopen(req).read())["asset"]["value"]

def put_asset(key, value):
    payload = json.dumps({"asset": {"key": key, "value": value}}).encode()
    req = urllib.request.Request(
        f"{API}/themes/{THEME}/assets.json",
        data=payload, headers=HEADERS, method="PUT"
    )
    return json.loads(urllib.request.urlopen(req).read())

raw = get_asset("templates/index.json")
page = json.loads(raw)
updated = copy.deepcopy(page)

changes = []

# ── 1. Slideshow: enable + update slides ────────────────────────────────────

SLIDESHOW_ID = "slideshow_Cb4b43"
SLIDE1_ID    = "slide_rAdxNG"   # has Teknion video — keep, add copy
SLIDE2_ID    = "slide_kqLf6Y"   # template garbage "Heading" — disable
ss = updated["sections"][SLIDESHOW_ID]

# Enable the section
if ss.get("disabled"):
    ss.pop("disabled", None)
    changes.append("✅ Slideshow section: enabled")

# Slide 1 — add copy overlay on the Teknion video
s1 = ss["blocks"][SLIDE1_ID]["settings"]
new_s1 = {
    "subheading": "Brant Business Interiors — a division of Office Central Inc.",
    "heading": "Canadian Business Furniture.\nFree Design Layouts.",
    "description": "Ontario's institutional office furniture specialist — schools, health centres, municipalities, and growing businesses.",
    "btn_text": "Get a Free Design Layout",
    "btn_link": "/pages/contact?subject=Design+engagement+request",
    "button_as_link": False,
    # text colours — white over the video
    "text_color": "#ffffff",
    "subtext_color": "#e5e7eb",
    "description_color": "#e5e7eb",
    "content_overlay_color": "#0a1628",
    "content_overlay_opacity": 45,
    "desktop_content_position": "d-center",
    "desktop_alignment": "d-text-center",
    "mobile_content_position": "m-center",
    "mobile_alignment": "m-text-center",
}
for k, v in new_s1.items():
    if s1.get(k) != v:
        changes.append(f"  Slide 1 [{k}]: {repr(s1.get(k))} → {repr(v)}")
        s1[k] = v

# Slide 2 — disable the blank template slide
s2 = ss["blocks"][SLIDE2_ID]
if not s2.get("disabled"):
    s2["disabled"] = True
    changes.append("✅ Slide 2 (blank template): disabled")

# ── 2. Trust strip: update copy ─────────────────────────────────────────────

TRUST_ID = "0c8c8fc0-f04e-4034-8eb8-f8c883b811bb"
trust = updated["sections"][TRUST_ID]

TRUST_UPDATES = {
    # block_id: (heading, description)
    "template--21380666753303__0c8c8fc0-f04e-4034-8eb8-f8c883b811bb-icon-with-text-1": (
        "<strong>Knowledgeable & Dedicated</strong>",
        "Sales Professionals."
    ),
    "template--21380666753303__0c8c8fc0-f04e-4034-8eb8-f8c883b811bb-icon-with-text-2": (
        "<strong>Proudly Canadian</strong>",
        "Owned & Operated Since 1964."
    ),
    "template--21380666753303__0c8c8fc0-f04e-4034-8eb8-f8c883b811bb-icon-with-text-3": (
        "<strong>Ships Across Canada</strong>",
        "From Ontario stock."
    ),
    "template--21380666753303__0c8c8fc0-f04e-4034-8eb8-f8c883b811bb-icon-with-text-4": (
        "<strong>PO & NET 30 Accepted</strong>",
        "For qualifying accounts."
    ),
}

for block_id, (heading, description) in TRUST_UPDATES.items():
    block_settings = trust["blocks"][block_id]["settings"]
    for field, val in [("heading", heading), ("description", description)]:
        if block_settings.get(field) != val:
            changes.append(f"  Trust strip [{block_id[-8:]}] [{field}]: {repr(block_settings.get(field))} → {repr(val)}")
            block_settings[field] = val

# ── report + push ────────────────────────────────────────────────────────────

if not changes:
    print("No changes detected.")
    sys.exit(0)

print(f"\n{'DRY RUN — ' if not LIVE else ''}Changes ({len(changes)}):\n")
for c in changes:
    print(f"  {c}")

if not LIVE:
    print("\n⚠  Dry run — nothing pushed. Re-run with --live to apply.")
    sys.exit(0)

print("\nPushing to Shopify…")
put_asset("templates/index.json", json.dumps(updated, indent=2))
print("✅ Done — homepage updated.")
