#!/usr/bin/env python3
"""
COLLECTION-IMG-PULL-1 / Phase 4 — Upload processed JPGs to Shopify Files via GraphQL.

For each REPLACE row, runs:
  1. stagedUploadsCreate → staged target URL
  2. POST multipart binary upload
  3. fileCreate(originalSource=resourceUrl) → fileId
  4. Poll file until fileStatus=READY → capture CDN URL + derive shopify:// URI

Rate-limited 0.45s per Shopify call. One retry-after-5s on hard failures.

Output: data/working/collection-img-pull-2026-05-25/uploaded.csv
  slot_id, shopify_file_id, cdn_url, shop_images_uri, status

Usage: python3 scripts/collection-img-pull-phase4-upload.py
"""
import csv
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "research" / "collection-img-pull-mapping-2026-05-25.csv"
PROC_DIR = ROOT / "data" / "working" / "collection-img-pull-2026-05-25" / "processed"
OUT_CSV = ROOT / "data" / "working" / "collection-img-pull-2026-05-25" / "uploaded.csv"

STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr); sys.exit(1)

RATE_LIMIT_SEC = 0.45
POLL_TIMEOUT_SEC = 30
POLL_INTERVAL_SEC = 1.5

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
    files {
      id
      fileStatus
      alt
      ... on MediaImage { image { url } }
    }
    userErrors { field message }
  }
}
"""

FILE_QUERY = """
query getFile($id: ID!) {
  node(id: $id) {
    ... on MediaImage {
      id
      fileStatus
      image { url }
    }
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
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GraphQL HTTP {e.code}: {body[:500]}")
    finally:
        time.sleep(RATE_LIMIT_SEC)
    if "errors" in resp:
        raise RuntimeError(f"GraphQL errors: {resp['errors']}")
    return resp["data"]


def multipart_post(url, params, file_path, mime):
    """POST file to staged target URL with multipart form data."""
    boundary = "----BBI-Boundary-" + uuid.uuid4().hex
    body = []
    for p in params:
        body.append(f"--{boundary}\r\n".encode())
        body.append(f'Content-Disposition: form-data; name="{p["name"]}"\r\n\r\n'.encode())
        body.append(f"{p['value']}\r\n".encode())
    body.append(f"--{boundary}\r\n".encode())
    body.append(
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'.encode()
    )
    body.append(f"Content-Type: {mime}\r\n\r\n".encode())
    body.append(file_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode())
    payload = b"".join(body)

    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Staged upload HTTP {e.code}: {body[:300]}")


def derive_shop_images_uri(cdn_url, fallback_name):
    """https://cdn.shopify.com/.../files/foo.jpg?v=... → shopify://shop_images/foo.jpg"""
    if not cdn_url:
        return f"shopify://shop_images/{fallback_name}"
    parsed = urllib.parse.urlparse(cdn_url)
    name = parsed.path.rsplit("/", 1)[-1]
    if not name:
        name = fallback_name
    return f"shopify://shop_images/{name}"


def poll_file_ready(file_gid, timeout=POLL_TIMEOUT_SEC):
    """Poll until fileStatus=READY. Returns (status, image_url)."""
    start = time.time()
    while time.time() - start < timeout:
        d = graphql(FILE_QUERY, {"id": file_gid})
        node = d.get("node") or {}
        status = node.get("fileStatus")
        img_url = (node.get("image") or {}).get("url")
        if status == "READY":
            return status, img_url
        if status == "FAILED":
            return status, None
        time.sleep(POLL_INTERVAL_SEC)
    return "TIMEOUT", None


def upload_one(slot_id, file_path):
    """Returns dict with shopify_file_id, cdn_url, shop_images_uri, status."""
    upload_name = f"bbi-coll-img-{slot_id}.jpg"
    mime = mimetypes.guess_type(upload_name)[0] or "image/jpeg"
    size = file_path.stat().st_size

    # 1) stagedUploadsCreate
    staged = graphql(STAGED_UPLOADS_CREATE, {"input": [{
        "resource": "IMAGE",
        "filename": upload_name,
        "mimeType": mime,
        "httpMethod": "POST",
        "fileSize": str(size),
    }]})
    errs = staged["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    targets = staged["stagedUploadsCreate"]["stagedTargets"]
    if not targets:
        raise RuntimeError("stagedUploadsCreate returned no targets")
    t = targets[0]

    # 2) POST binary
    status_code, _ = multipart_post(t["url"], t["parameters"], file_path, mime)
    if status_code >= 400:
        raise RuntimeError(f"staged upload returned {status_code}")

    # 3) fileCreate
    fc = graphql(FILE_CREATE, {"files": [{
        "alt": f"BBI {slot_id} — programmatic collection pull 2026-05-25",
        "contentType": "IMAGE",
        "originalSource": t["resourceUrl"],
    }]})
    errs = fc["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    files = fc["fileCreate"]["files"]
    if not files:
        raise RuntimeError("fileCreate returned no files")
    f0 = files[0]
    file_gid = f0["id"]

    # 4) poll until READY
    fstatus, cdn_url = poll_file_ready(file_gid)
    shop_uri = derive_shop_images_uri(cdn_url, upload_name)

    return {
        "slot_id": slot_id,
        "shopify_file_id": file_gid,
        "cdn_url": cdn_url or "",
        "shop_images_uri": shop_uri,
        "status": fstatus,
    }


def main():
    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))
    targets = [r for r in rows if r["action"] == "REPLACE"]
    print(f"Phase 4 — uploading {len(targets)} processed JPGs to Shopify Files via GraphQL")
    print(f"  rate-limit {RATE_LIMIT_SEC}s between GraphQL calls + 5s retry on fail")
    print()

    results = []
    consecutive_fails = 0
    for i, row in enumerate(targets, 1):
        slot_id = row["slot_id"]
        f = PROC_DIR / f"{slot_id}.jpg"
        if not f.exists():
            print(f"  [{i:2d}/{len(targets)}] SKIP  {slot_id}  processed missing")
            results.append({"slot_id": slot_id, "shopify_file_id": "", "cdn_url": "",
                            "shop_images_uri": "", "status": "SKIP_no_processed"})
            continue

        attempt = 1
        last_err = None
        while attempt <= 2:
            try:
                r = upload_one(slot_id, f)
                results.append(r)
                tag = r["status"]
                print(f"  [{i:2d}/{len(targets)}] {tag:9s} {slot_id:55s} → {r['shop_images_uri']}")
                consecutive_fails = 0 if tag == "READY" else consecutive_fails
                break
            except Exception as e:
                last_err = e
                if attempt == 1:
                    print(f"  [{i:2d}/{len(targets)}] RETRY {slot_id}: {e}")
                    time.sleep(5)
                attempt += 1
        else:
            results.append({"slot_id": slot_id, "shopify_file_id": "", "cdn_url": "",
                            "shop_images_uri": "", "status": f"FAIL: {last_err}"})
            print(f"  [{i:2d}/{len(targets)}] FAIL  {slot_id}: {last_err}")
            consecutive_fails += 1
            if consecutive_fails >= 3:
                print("\n3 consecutive failures — halting per prompt rules (likely Shopify API issue).")
                break

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["slot_id", "shopify_file_id", "cdn_url",
                                          "shop_images_uri", "status"])
        w.writeheader()
        for r in results:
            w.writerow(r)

    ready = sum(1 for r in results if r["status"] == "READY")
    failed = sum(1 for r in results if r["status"].startswith("FAIL"))
    other = len(results) - ready - failed
    print()
    print("=" * 72)
    print(f"PHASE 4 SUMMARY  →  {OUT_CSV.relative_to(ROOT)}")
    print("=" * 72)
    print(f"  Ready:   {ready} / {len(targets)}")
    print(f"  Failed:  {failed}")
    print(f"  Other:   {other}")
    if failed:
        print("\nFAILURES:")
        for r in results:
            if r["status"].startswith("FAIL"):
                print(f"  {r['slot_id']}: {r['status']}")


if __name__ == "__main__":
    main()
