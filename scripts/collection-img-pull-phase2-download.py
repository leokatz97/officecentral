#!/usr/bin/env python3
"""
COLLECTION-IMG-PULL-1 / Phase 2 — Download lead product images.

Reads mapping CSV, downloads each REPLACE row's lead_product_image_src to
data/working/collection-img-pull-2026-05-25/raw/{slot_id}.{ext}, retries once
on failure. Read-only for Shopify (no API writes).

Usage: python3 scripts/collection-img-pull-phase2-download.py
"""
import csv
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "research" / "collection-img-pull-mapping-2026-05-25.csv"
RAW_DIR = ROOT / "data" / "working" / "collection-img-pull-2026-05-25" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def ext_from_url(url):
    path = urllib.parse.urlparse(url).path
    for e in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.lower().endswith(e):
            return e
    return ".jpg"


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 BBI-img-pull"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def main():
    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))
    replace_rows = [r for r in rows if r["action"] == "REPLACE"]
    print(f"Phase 2 — downloading {len(replace_rows)} lead product images")
    print(f"  destination: {RAW_DIR.relative_to(ROOT)}/")
    print()

    results = []
    for i, row in enumerate(replace_rows, 1):
        slot_id = row["slot_id"]
        url = row["lead_product_image_src"]
        if not url:
            print(f"  [{i:2d}/{len(replace_rows)}] SKIP  {slot_id}  (empty src)")
            results.append((slot_id, "skip_empty_src", 0, ""))
            continue
        ext = ext_from_url(url)
        dest = RAW_DIR / f"{slot_id}{ext}"
        size = None
        err = None
        for attempt in (1, 2):
            try:
                size = download(url, dest)
                break
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                if attempt == 1:
                    print(f"  [{i:2d}/{len(replace_rows)}] RETRY {slot_id}  err={err}")
                    time.sleep(3)
        if size is None:
            print(f"  [{i:2d}/{len(replace_rows)}] FAIL  {slot_id}  err={err}")
            results.append((slot_id, "fail", 0, err))
        else:
            print(f"  [{i:2d}/{len(replace_rows)}] OK    {slot_id:55s} {size/1024:7.1f} KB  →  {dest.name}")
            results.append((slot_id, "ok", size, ""))

    ok = sum(1 for _, s, _, _ in results if s == "ok")
    fail = sum(1 for _, s, _, _ in results if s == "fail")
    skip = sum(1 for _, s, _, _ in results if s.startswith("skip"))
    print(f"\nPhase 2 summary: {ok} OK / {fail} FAIL / {skip} SKIP (of {len(replace_rows)} REPLACE)")
    if fail:
        print("FAILED slots:")
        for slot_id, status, _, err in results:
            if status == "fail":
                print(f"  {slot_id}  err={err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
