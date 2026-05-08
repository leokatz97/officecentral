#!/usr/bin/env python3
"""
diff-bbi-baselines.py
BBI Launch Readiness — Pixel-diff Baseline Comparison Tool

Usage:
    python3 scripts/diff-bbi-baselines.py
    python3 scripts/diff-bbi-baselines.py --baseline data/baselines/locked/ --candidate data/baselines/current/
    python3 scripts/diff-bbi-baselines.py --threshold 3.0

Compares matching PNG pairs between baseline and candidate directories.
For each pair:
  - Computes per-pixel RGB delta using Pillow
  - Saves an overlay diff PNG to data/baselines/_diff/
  - Writes summary CSV to data/reports/diff-baselines-{timestamp}.csv

PASS/FAIL threshold defaults to 5% changed pixels.

Requirements:
    pip install Pillow
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

BASELINE_DIR_DEFAULT = "data/baselines/locked"
CANDIDATE_DIR_DEFAULT = "data/baselines/current"
DIFF_DIR = Path("data/baselines/_diff")
REPORTS_DIR = Path("data/reports")

DEFAULT_THRESHOLD_PCT = 5.0   # % of pixels that may differ before FAIL
DIFF_SENSITIVITY = 10         # per-channel delta below this is ignored (noise floor)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def check_pillow():
    try:
        from PIL import Image, ImageChops, ImageDraw  # noqa: F401
        return True
    except ImportError:
        return False


def find_png_pairs(baseline_dir: Path, candidate_dir: Path):
    """Walk baseline_dir recursively. For each .png, find matching path in candidate_dir."""
    pairs = []
    for base_png in sorted(baseline_dir.rglob("*.png")):
        rel = base_png.relative_to(baseline_dir)
        cand_png = candidate_dir / rel
        pairs.append((base_png, cand_png, rel))
    return pairs


def compute_diff(base_path: Path, cand_path: Path, diff_out: Path, sensitivity: int):
    """
    Compute pixel delta between two images using Pillow.
    Returns (delta_pct, total_pixels, diff_pixels).
    Saves an overlay diff PNG with changed pixels highlighted in red.
    """
    from PIL import Image, ImageChops

    base_img = Image.open(base_path).convert("RGB")
    cand_img = Image.open(cand_path).convert("RGB")

    # Resize candidate to match baseline if dimensions differ
    if base_img.size != cand_img.size:
        cand_img = cand_img.resize(base_img.size, Image.LANCZOS)

    diff = ImageChops.difference(base_img, cand_img)
    total_pixels = base_img.width * base_img.height

    # Count pixels where any channel exceeds the sensitivity threshold
    diff_pixels = 0
    diff_highlight = base_img.copy()
    pixels_base = diff_highlight.load()
    pixels_diff = diff.load()

    for y in range(base_img.height):
        for x in range(base_img.width):
            r, g, b = pixels_diff[x, y]
            if max(r, g, b) > sensitivity:
                diff_pixels += 1
                pixels_base[x, y] = (212, 37, 42)  # BBI red highlight

    delta_pct = (diff_pixels / total_pixels) * 100 if total_pixels > 0 else 0.0

    # Save diff overlay
    diff_out.parent.mkdir(parents=True, exist_ok=True)
    diff_highlight.save(str(diff_out))

    return delta_pct, total_pixels, diff_pixels


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pixel-diff BBI baseline screenshots using Pillow."
    )
    parser.add_argument(
        "--baseline",
        default=BASELINE_DIR_DEFAULT,
        help=f"Baseline directory (default: {BASELINE_DIR_DEFAULT})",
    )
    parser.add_argument(
        "--candidate",
        default=CANDIDATE_DIR_DEFAULT,
        help=f"Candidate directory (default: {CANDIDATE_DIR_DEFAULT})",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD_PCT,
        help=f"FAIL threshold: %% of pixels allowed to differ (default: {DEFAULT_THRESHOLD_PCT})",
    )
    parser.add_argument(
        "--sensitivity",
        type=int,
        default=DIFF_SENSITIVITY,
        help=f"Per-channel delta noise floor, 0–255 (default: {DIFF_SENSITIVITY})",
    )
    args = parser.parse_args()

    # Check we're in the repo root
    if not Path("theme").is_dir():
        print("ERROR: Run this script from the repo root (Office Central/).")
        sys.exit(1)

    if not check_pillow():
        print("ERROR: Pillow is not installed.")
        print()
        print("To install:")
        print("  pip install Pillow")
        print()
        sys.exit(1)

    baseline_dir = Path(args.baseline)
    candidate_dir = Path(args.candidate)

    if not baseline_dir.exists():
        print(f"ERROR: Baseline directory not found: {baseline_dir}")
        print("Run capture-bbi-baselines.py --lock first to create a locked baseline.")
        sys.exit(1)

    if not candidate_dir.exists():
        print(f"ERROR: Candidate directory not found: {candidate_dir}")
        print("Run capture-bbi-baselines.py first to capture current screenshots.")
        sys.exit(1)

    pairs = find_png_pairs(baseline_dir, candidate_dir)
    if not pairs:
        print(f"No .png files found under {baseline_dir}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = REPORTS_DIR / f"diff-baselines-{timestamp}.csv"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Baseline:  {baseline_dir}")
    print(f"Candidate: {candidate_dir}")
    print(f"Threshold: {args.threshold:.1f}%  |  Sensitivity: {args.sensitivity}")
    print(f"Pairs found: {len(pairs)}")
    print()

    rows = []
    pass_count = 0
    fail_count = 0
    missing_count = 0

    for base_png, cand_png, rel in pairs:
        if not cand_png.exists():
            print(f"  MISSING  {rel}")
            rows.append({
                "file": str(rel),
                "baseline": str(base_png),
                "candidate": str(cand_png),
                "delta_pct": "",
                "result": "MISSING",
                "diff_pixels": "",
                "total_pixels": "",
            })
            missing_count += 1
            continue

        diff_out = DIFF_DIR / rel
        try:
            delta_pct, total_pixels, diff_pixels = compute_diff(
                base_png, cand_png, diff_out, args.sensitivity
            )
        except Exception as exc:
            print(f"  ERROR    {rel}  —  {exc}")
            rows.append({
                "file": str(rel),
                "baseline": str(base_png),
                "candidate": str(cand_png),
                "delta_pct": "",
                "result": "ERROR",
                "diff_pixels": "",
                "total_pixels": "",
            })
            continue

        result = "PASS" if delta_pct <= args.threshold else "FAIL"
        icon = "✓" if result == "PASS" else "✗"
        print(f"  {icon} {result:<4}  {delta_pct:6.2f}%  {rel}")

        if result == "PASS":
            pass_count += 1
        else:
            fail_count += 1

        rows.append({
            "file": str(rel),
            "baseline": str(base_png),
            "candidate": str(cand_png),
            "delta_pct": f"{delta_pct:.4f}",
            "result": result,
            "diff_pixels": diff_pixels,
            "total_pixels": total_pixels,
        })

    # Write CSV
    fieldnames = ["file", "baseline", "candidate", "delta_pct", "result", "diff_pixels", "total_pixels"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Results: {pass_count} PASS / {fail_count} FAIL / {missing_count} MISSING")
    print(f"CSV:     {csv_path}")
    if fail_count > 0 or missing_count > 0:
        print(f"Diffs:   {DIFF_DIR}")

    if fail_count > 0 or missing_count > 0:
        print()
        print("FAILURES:")
        for row in rows:
            if row["result"] in ("FAIL", "MISSING", "ERROR"):
                delta = f"  ({row['delta_pct']}%)" if row["delta_pct"] else ""
                print(f"  {row['result']:<7} {row['file']}{delta}")
        sys.exit(1)


if __name__ == "__main__":
    main()
