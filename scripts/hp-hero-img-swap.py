#!/usr/bin/env python3
"""
HP-HERO-IMG-SWAP — Upload a new hero image to Shopify Files and swap it into
the bbi-hero custom_liquid in templates/index.json. DEV-only.

Inputs:
  PROCESSED:  data/working/hp-hero-2026-05-25/processed/hp-hero-office-breakout.jpg
  UPLOAD_AS:  hp-hero-office-breakout.jpg
  OLD_SRC:    cdn URL currently in templates/index.json (auto-detected)
  NEW_ALT:    descriptive alt for the new image
"""
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_JSON = ROOT / "theme" / "templates" / "index.json"
PROCESSED = ROOT / "data" / "working" / "hp-hero-2026-05-25" / "processed" / "hp-hero-office-breakout.jpg"

NEW_ALT = "Office breakout space with banquette seating, lounge chairs, and adjoining meeting room — Brant Business Interiors, Peterborough Ontario"

STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
DEV_THEME_ID = "186373570873"
LIVE_THEME_ID = "178274435385"
RATE_LIMIT_SEC = 0.5

TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr); sys.exit(1)

GRAPHQL_URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

STAGED_UPLOADS_CREATE = """
mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
"""

FILE_CREATE = """
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id fileStatus alt ... on MediaImage { image { url } } }
    userErrors { field message }
  }
}
"""

FILE_QUERY = """
query getFile($id: ID!) {
  node(id: $id) {
    ... on MediaImage { id fileStatus image { url } }
  }
}
"""


def graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL, data=body, method="POST",
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())["data"]
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GraphQL HTTP {e.code}: {body[:500]}")
    finally:
        time.sleep(RATE_LIMIT_SEC)


def multipart_post(url, params, file_path, mime):
    boundary = "----BBI-Boundary-" + uuid.uuid4().hex
    body = []
    for p in params:
        body.append(f"--{boundary}\r\n".encode())
        body.append(f'Content-Disposition: form-data; name="{p["name"]}"\r\n\r\n'.encode())
        body.append(f"{p['value']}\r\n".encode())
    body.append(f"--{boundary}\r\n".encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'.encode())
    body.append(f"Content-Type: {mime}\r\n\r\n".encode())
    body.append(file_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode())
    payload = b"".join(body)
    req = urllib.request.Request(url, data=payload, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status


def api_get(path):
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{API_VERSION}/{path}",
        headers={"X-Shopify-Access-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def api_put(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{API_VERSION}/{path}",
        data=body, method="PUT",
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    finally:
        time.sleep(RATE_LIMIT_SEC)


def poll_file_ready(file_gid, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        d = graphql(FILE_QUERY, {"id": file_gid})
        node = d.get("node") or {}
        st = node.get("fileStatus")
        url = (node.get("image") or {}).get("url")
        if st == "READY":
            return st, url
        if st == "FAILED":
            return st, None
        time.sleep(1.5)
    return "TIMEOUT", None


def main():
    # ── Guards ────────────────────────────────────────────────────────
    print(f"DEV target → {DEV_THEME_ID}")
    t = api_get(f"themes/{DEV_THEME_ID}.json")["theme"]
    assert t["role"] != "main", f"REFUSE: theme {DEV_THEME_ID} role=main"
    print(f"  name={t['name']}  role={t['role']}  ✓ unpublished")
    live = api_get(f"themes/{LIVE_THEME_ID}.json")["theme"]
    expected_live = "2026-05-16T16:47:22-04:00"
    assert live["updated_at"] == expected_live, \
        f"LIVE baseline mismatch: {live['updated_at']} != {expected_live}"
    print(f"  LIVE updated_at OK")

    # ── Upload ────────────────────────────────────────────────────────
    print(f"\n[1/3] Upload {PROCESSED.name} → Shopify Files")
    size = PROCESSED.stat().st_size
    mime = mimetypes.guess_type(PROCESSED.name)[0] or "image/jpeg"
    staged = graphql(STAGED_UPLOADS_CREATE, {"input": [{
        "resource": "IMAGE",
        "filename": PROCESSED.name,
        "mimeType": mime,
        "httpMethod": "POST",
        "fileSize": str(size),
    }]})
    errs = staged["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    target = staged["stagedUploadsCreate"]["stagedTargets"][0]
    status = multipart_post(target["url"], target["parameters"], PROCESSED, mime)
    assert status < 400, f"staged upload HTTP {status}"
    fc = graphql(FILE_CREATE, {"files": [{
        "alt": NEW_ALT, "contentType": "IMAGE", "originalSource": target["resourceUrl"],
    }]})
    errs = fc["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    file_gid = fc["fileCreate"]["files"][0]["id"]
    st, cdn_url = poll_file_ready(file_gid)
    assert st == "READY" and cdn_url, f"file not READY: {st}"
    print(f"      READY  {round(size/1024,1)}KB  {file_gid}")
    print(f"      cdn:   {cdn_url}")

    # ── Update templates/index.json ──────────────────────────────────
    print(f"\n[2/3] Swapping <img> in bbi-hero → new CDN URL + alt")
    with open(INDEX_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    hero_html = data["sections"]["bbi-hero"]["settings"]["custom_liquid"]
    # Replace the entire src attribute value
    new_hero_html, n_src = re.subn(
        r'src="https://cdn\.shopify\.com/s/files/[^"]+hp-hero-slide-1-office\.jpg[^"]*"',
        f'src="{cdn_url}"',
        hero_html, count=1
    )
    assert n_src == 1, f"expected 1 src replacement, got {n_src}"
    # Replace the alt attribute value
    new_hero_html, n_alt = re.subn(
        r'alt="Executive office installation by Brant Business Interiors, Peterborough Ontario"',
        f'alt="{NEW_ALT}"',
        new_hero_html, count=1
    )
    assert n_alt == 1, f"expected 1 alt replacement, got {n_alt}"
    data["sections"]["bbi-hero"]["settings"]["custom_liquid"] = new_hero_html
    with open(INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"      src + alt updated in {INDEX_JSON.relative_to(ROOT)}")

    # ── Push to DEV ───────────────────────────────────────────────────
    print(f"\n[3/3] PUT theme {DEV_THEME_ID} ← templates/index.json")
    status, resp = api_put(
        f"themes/{DEV_THEME_ID}/assets.json",
        {"asset": {"key": "templates/index.json",
                   "value": INDEX_JSON.read_text(encoding="utf-8")}},
    )
    asset = resp["asset"]
    print(f"      HTTP {status} · size={asset.get('size')} · updated_at={asset.get('updated_at')}")

    # ── Verify ────────────────────────────────────────────────────────
    print(f"\nVerifying via re-fetch...")
    r = api_get(f"themes/{DEV_THEME_ID}/assets.json?asset[key]=templates/index.json")
    fetched_hero = json.loads(r["asset"]["value"])["sections"]["bbi-hero"]["settings"]["custom_liquid"]
    checks = {
        "new CDN url present": cdn_url.split("?")[0] in fetched_hero,
        "old slide-1-office URL gone": "hp-hero-slide-1-office.jpg" not in fetched_hero,
        "new alt present": NEW_ALT in fetched_hero,
        "old alt gone": "Executive office installation" not in fetched_hero,
        "fetchpriority=high preserved": 'fetchpriority="high"' in fetched_hero,
        "loading=eager preserved": 'loading="eager"' in fetched_hero,
        "OECM line still present": "OECM Agreement 2025-470" in fetched_hero,
        "Request a Quote still present": "Request a Quote" in fetched_hero,
        "phone tel link still present": "tel:18008359565" in fetched_hero,
    }
    print()
    print("=" * 72)
    all_ok = True
    for label, ok in checks.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {label}")
        if not ok: all_ok = False
    print("=" * 72)
    if not all_ok:
        print("ONE OR MORE CHECKS FAILED"); sys.exit(3)
    print(f"\nNEW CDN URL  →  {cdn_url}")


if __name__ == "__main__":
    main()
