#!/usr/bin/env python3
"""
merge-hero-specs.py

Merges filled spec fields from a session output file into data/specs.json.

Rules:
- NEVER overwrites an existing non-empty value in specs.json
- Only fills fields that are blank/missing in specs.json AND non-empty in the output
- Dry-run by default; pass --live to write changes
- Pass --push (with --live) to also run push-pe2-specs.py --live after merging

Usage:
    python3 scripts/merge-hero-specs.py              # dry run
    python3 scripts/merge-hero-specs.py --live       # write changes
    python3 scripts/merge-hero-specs.py --live --push  # write + push to Shopify
"""

import json
import os
import sys
import subprocess
from copy import deepcopy
from datetime import datetime

SPECS_FILE = "data/specs.json"
OUTPUT_FILE = "data/reports/hero-spec-gaps-output.json"
SPECS_DIR = "data/specs"

SPEC_FIELDS = [
    "manufacturer", "product_line", "model_codes", "dimensions",
    "weight", "weight_capacity", "materials", "finishes_available",
    "key_features", "certifications", "warranty", "country_of_manufacture",
    "who_its_for"
]

DRY_RUN = "--live" not in sys.argv
DO_PUSH = "--push" in sys.argv


def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, list):
        return len(value) == 0
    return False


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    if not os.path.exists(OUTPUT_FILE):
        print(f"[ERROR] Output file not found: {OUTPUT_FILE}")
        sys.exit(1)

    if not os.path.exists(SPECS_FILE):
        print(f"[ERROR] Specs file not found: {SPECS_FILE}")
        sys.exit(1)

    session_output = load_json(OUTPUT_FILE)
    specs_db = load_json(SPECS_FILE)
    products = session_output.get("products", {})

    if not products:
        print("[INFO] No products found in output file. Nothing to merge.")
        sys.exit(0)

    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print(f"\n=== merge-hero-specs.py [{mode}] ===")
    print(f"Session output version: {session_output.get('version', 'unknown')}")
    print(f"Products in output: {len(products)}\n")

    total_updated = 0
    total_fields_filled = 0
    skipped = []
    updated_summary = []

    updated_specs_db = deepcopy(specs_db)

    for handle, session_data in products.items():
        status = session_data.get("status", "done")

        if status in ("skip", "service"):
            skipped.append((handle, status))
            print(f"  SKIP [{status}] {handle}")
            continue

        if handle not in updated_specs_db:
            print(f"  WARN  handle not found in specs.json: {handle}")
            continue

        product = updated_specs_db[handle]
        existing_specs = product.get("specs", {})
        new_specs = session_data.get("specs", {})

        if not new_specs:
            print(f"  SKIP  no specs in output for: {handle}")
            continue

        fields_filled = []
        for field in SPEC_FIELDS:
            if field not in new_specs:
                continue
            new_val = new_specs[field]
            existing_val = existing_specs.get(field)

            if is_empty(new_val):
                continue  # nothing to fill
            if not is_empty(existing_val):
                continue  # already has a value — never overwrite

            fields_filled.append(field)
            if not DRY_RUN:
                existing_specs[field] = new_val

        if fields_filled:
            total_updated += 1
            total_fields_filled += len(fields_filled)
            updated_summary.append((handle, fields_filled))
            status_label = "WOULD FILL" if DRY_RUN else "FILLED"
            print(f"  {status_label} {handle}: {', '.join(fields_filled)}")
        else:
            print(f"  NO-OP {handle}: all target fields already populated or output empty")

    print(f"\n--- Summary ---")
    print(f"Products with fills: {total_updated}")
    print(f"Total fields filled: {total_fields_filled}")
    print(f"Skipped (service/skip status): {len(skipped)}")

    if DRY_RUN:
        print("\n[DRY RUN] No files written. Pass --live to apply changes.")
        return

    # Write updated specs.json
    save_json(SPECS_FILE, updated_specs_db)
    print(f"\n[WRITTEN] {SPECS_FILE}")

    # Update individual data/specs/<handle>.json files if they exist
    individual_updated = 0
    for handle, fields_filled in updated_summary:
        individual_path = os.path.join(SPECS_DIR, f"{handle}.json")
        if os.path.exists(individual_path):
            individual_data = load_json(individual_path)
            ind_specs = individual_data.get("specs", {})
            session_specs = products[handle].get("specs", {})
            for field in fields_filled:
                if is_empty(ind_specs.get(field)) and not is_empty(session_specs.get(field)):
                    ind_specs[field] = session_specs[field]
            save_json(individual_path, individual_data)
            individual_updated += 1

    if individual_updated:
        print(f"[WRITTEN] {individual_updated} individual data/specs/<handle>.json files updated")

    # Optionally push to Shopify
    if DO_PUSH:
        print("\n[PUSH] Running push-pe2-specs.py --live ...")
        result = subprocess.run(
            ["python3", "scripts/push-pe2-specs.py", "--live"],
            capture_output=False
        )
        if result.returncode != 0:
            print(f"[ERROR] push-pe2-specs.py exited with code {result.returncode}")
            sys.exit(result.returncode)
        print("[PUSH] Done.")


if __name__ == "__main__":
    main()
