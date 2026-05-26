#!/usr/bin/env python3
"""
HOMEPAGE-HERO-SLIDESHOW-1 — one-off uploader for 3 hero images to Shopify Files.

Reads from data/working/homepage-hero-slideshow-v2-2026-05-26/processed/
and writes uploaded.csv with cdn_url + shop_images_uri per slide.
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
WORK = ROOT / "data" / "working" / "homepage-hero-slideshow-v2-2026-05-26"
PROC_DIR = WORK / "processed"
OUT_CSV = WORK / "uploaded.csv"

STORE = "office-central-online.myshopify.com"
API_VERSION = "2026-04"
TOKEN = os.environ.get("SHOPIFY_TOKEN")
if not TOKEN:
    print("ERROR: SHOPIFY_TOKEN not set", file=sys.stderr); sys.exit(1)

RATE_LIMIT_SEC = 0.5
POLL_TIMEOUT_SEC = 30
POLL_INTERVAL_SEC = 1.5

GRAPHQL_URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

SLIDES = [
    {
        "slide": 1, "slug": "office",
        "filename": "hp-hero-slide-1-office.jpg",
        "alt": "Modern Canadian office workspace with collaborative desks and ergonomic seating",
    },
    {
        "slide": 2, "slug": "healthcare",
        "filename": "hp-hero-slide-2-healthcare.jpg",
        "alt": "Healthcare waiting area with AODA-compliant seating and clinical layout",
    },
    {
        "slide": 3, "slug": "education",
        "filename": "hp-hero-slide-3-education.jpg",
        "alt": "Educational classroom with flexible furniture for collaborative learning",
    },
]

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
    if not cdn_url:
        return f"shopify://shop_images/{fallback_name}"
    parsed = urllib.parse.urlparse(cdn_url)
    name = parsed.path.rsplit("/", 1)[-1]
    if not name:
        name = fallback_name
    return f"shopify://shop_images/{name}"


def poll_file_ready(file_gid, timeout=POLL_TIMEOUT_SEC):
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


def upload_one(slide):
    file_path = PROC_DIR / slide["filename"]
    mime = mimetypes.guess_type(file_path.name)[0] or "image/jpeg"
    size = file_path.stat().st_size

    staged = graphql(STAGED_UPLOADS_CREATE, {"input": [{
        "resource": "IMAGE",
        "filename": file_path.name,
        "mimeType": mime,
        "httpMethod": "POST",
        "fileSize": str(size),
    }]})
    errs = staged["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors: {errs}")
    t = staged["stagedUploadsCreate"]["stagedTargets"][0]

    status_code, _ = multipart_post(t["url"], t["parameters"], file_path, mime)
    if status_code >= 400:
        raise RuntimeError(f"staged upload returned {status_code}")

    fc = graphql(FILE_CREATE, {"files": [{
        "alt": slide["alt"],
        "contentType": "IMAGE",
        "originalSource": t["resourceUrl"],
    }]})
    errs = fc["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    f0 = fc["fileCreate"]["files"][0]
    file_gid = f0["id"]

    fstatus, cdn_url = poll_file_ready(file_gid)
    shop_uri = derive_shop_images_uri(cdn_url, file_path.name)
    return {
        "slide": slide["slide"],
        "slug": slide["slug"],
        "filename": file_path.name,
        "shopify_file_id": file_gid,
        "cdn_url": cdn_url or "",
        "shop_images_uri": shop_uri,
        "alt": slide["alt"],
        "status": fstatus,
        "size_kb": round(size / 1024, 1),
    }


def main():
    print(f"Uploading {len(SLIDES)} hero slide images to Shopify Files...")
    print(f"  rate-limit {RATE_LIMIT_SEC}s between calls")
    print()
    results = []
    for slide in SLIDES:
        attempt = 1
        last_err = None
        while attempt <= 2:
            try:
                r = upload_one(slide)
                results.append(r)
                print(f"  slide{r['slide']} {r['slug']:11s} {r['status']:8s} {r['size_kb']:6.1f}KB → {r['shop_images_uri']}")
                print(f"    cdn: {r['cdn_url']}")
                break
            except Exception as e:
                last_err = e
                if attempt == 1:
                    print(f"  slide{slide['slide']} RETRY: {e}")
                    time.sleep(5)
                attempt += 1
        else:
            results.append({**slide, "shopify_file_id": "", "cdn_url": "",
                            "shop_images_uri": "", "status": f"FAIL: {last_err}", "size_kb": 0})
            print(f"  slide{slide['slide']} FAIL: {last_err}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "slide", "slug", "filename", "shopify_file_id", "cdn_url",
            "shop_images_uri", "alt", "status", "size_kb"
        ])
        w.writeheader()
        for r in results:
            w.writerow(r)

    print()
    print("=" * 72)
    ready = sum(1 for r in results if r["status"] == "READY")
    print(f"  {ready}/{len(SLIDES)} READY  →  {OUT_CSV.relative_to(ROOT)}")
    print("=" * 72)
    if ready != len(SLIDES):
        sys.exit(1)


if __name__ == "__main__":
    main()
