#!/usr/bin/env python3
"""
COLLECTION-IMG-PULL-1 / Phase 3 — Process images via ImageMagick.

Reads mapping CSV + Phase 2 raw downloads, processes each to slot spec
(hero 1920x1080, tile 1200x900), JPG sRGB Q85, <2MB. Falls back to Q80→Q75
if needed. Writes PROCESSED-VERIFICATION.md.

Usage: python3 scripts/collection-img-pull-phase3-process.py
"""
import csv
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "research" / "collection-img-pull-mapping-2026-05-25.csv"
WORK_DIR = ROOT / "data" / "working" / "collection-img-pull-2026-05-25"
RAW_DIR = WORK_DIR / "raw"
PROC_DIR = WORK_DIR / "processed"
VERIF_MD = WORK_DIR / "PROCESSED-VERIFICATION.md"
PROC_DIR.mkdir(parents=True, exist_ok=True)
MAGICK = "/opt/homebrew/bin/magick"

SPEC = {"hero": (1920, 1080), "tile": (1200, 900)}
MAX_BYTES = 2 * 1024 * 1024


def magick_identify(path):
    """Return (width, height, format) via magick identify."""
    out = subprocess.run([MAGICK, "identify", "-format", "%w %h %m", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    parts = out.split()
    return int(parts[0]), int(parts[1]), parts[2]


def process_one(raw_path, dest_path, w, h, quality):
    subprocess.run([
        MAGICK, str(raw_path),
        "-auto-orient",
        "-resize", f"{w}x{h}^",
        "-gravity", "center",
        "-extent", f"{w}x{h}",
        "-colorspace", "sRGB",
        "-strip",
        "-quality", str(quality),
        str(dest_path),
    ], check=True)


def find_raw(slot_id):
    """Match {slot_id}.* in raw dir."""
    for p in RAW_DIR.iterdir():
        if p.stem == slot_id:
            return p
    return None


def main():
    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))
    targets = [r for r in rows if r["action"] == "REPLACE"]
    print(f"Phase 3 — processing {len(targets)} images via ImageMagick")
    print()

    records = []
    for i, row in enumerate(targets, 1):
        slot_id = row["slot_id"]
        slot_type = row["slot_type"]
        w, h = SPEC[slot_type]
        raw = find_raw(slot_id)
        if not raw:
            print(f"  [{i:2d}/{len(targets)}] FAIL  {slot_id}  raw missing")
            records.append({"slot_id": slot_id, "status": "FAIL_no_raw",
                            "source_dims": "", "target_dims": f"{w}x{h}",
                            "output_dims": "", "file_size_kb": 0, "quality": 0})
            continue

        try:
            sw, sh, sfmt = magick_identify(raw)
        except subprocess.CalledProcessError as e:
            print(f"  [{i:2d}/{len(targets)}] FAIL identify {slot_id}: {e}")
            records.append({"slot_id": slot_id, "status": "FAIL_identify",
                            "source_dims": "", "target_dims": f"{w}x{h}",
                            "output_dims": "", "file_size_kb": 0, "quality": 0})
            continue

        dest = PROC_DIR / f"{slot_id}.jpg"
        quality_used = None
        for q in (85, 80, 75):
            try:
                process_one(raw, dest, w, h, q)
            except subprocess.CalledProcessError as e:
                print(f"  [{i:2d}/{len(targets)}] FAIL process @Q{q} {slot_id}: {e}")
                continue
            size = dest.stat().st_size
            quality_used = q
            if size <= MAX_BYTES:
                break
        if quality_used is None:
            records.append({"slot_id": slot_id, "status": "FAIL_process",
                            "source_dims": f"{sw}x{sh}", "target_dims": f"{w}x{h}",
                            "output_dims": "", "file_size_kb": 0, "quality": 0})
            print(f"  [{i:2d}/{len(targets)}] FAIL  {slot_id}")
            continue

        ow, oh, _ = magick_identify(dest)
        size_kb = dest.stat().st_size / 1024
        oversize = " OVERSIZE" if dest.stat().st_size > MAX_BYTES else ""
        quality_flag = f" Q{quality_used}<85" if quality_used < 85 else ""
        status = "OK"
        if dest.stat().st_size > MAX_BYTES:
            status = "WARN_oversize"
        print(f"  [{i:2d}/{len(targets)}] OK  {slot_id:55s} src={sw:4d}x{sh:<4d} → {ow}x{oh} "
              f"{size_kb:7.1f} KB Q{quality_used}{quality_flag}{oversize}")
        records.append({"slot_id": slot_id, "status": status,
                        "source_dims": f"{sw}x{sh}", "target_dims": f"{w}x{h}",
                        "output_dims": f"{ow}x{oh}", "file_size_kb": round(size_kb, 1),
                        "quality": quality_used})

    # Write PROCESSED-VERIFICATION.md
    ok = [r for r in records if r["status"] == "OK"]
    warn = [r for r in records if r["status"].startswith("WARN")]
    fail = [r for r in records if r["status"].startswith("FAIL")]
    reduced_q = [r for r in records if r["status"] == "OK" and r["quality"] < 85]

    sizes = [r["file_size_kb"] for r in ok]
    smin = min(sizes) if sizes else 0
    smax = max(sizes) if sizes else 0
    savg = sum(sizes) / len(sizes) if sizes else 0

    md_lines = [
        "# COLLECTION-IMG-PULL-1 — Phase 3 Processed Verification",
        "",
        f"Generated 2026-05-25 · ImageMagick `{MAGICK}` · process ratio 1920x1080 (hero) / 1200x900 (tile) JPG sRGB Q85 <2MB",
        "",
        "## Summary",
        "",
        f"- Target REPLACE rows: {len(targets)}",
        f"- Processed OK: {len(ok)}",
        f"- Processed WARN (oversize after Q75 retry): {len(warn)}",
        f"- Failed: {len(fail)}",
        f"- Required Q<85 to fit under 2MB: {len(reduced_q)}",
        f"- File size (KB) — min {smin:.1f} / avg {savg:.1f} / max {smax:.1f}",
        "",
        "## Per-slot",
        "",
        "| slot_id | status | source | target | output | size KB | Q |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for r in records:
        md_lines.append(
            f"| `{r['slot_id']}` | {r['status']} | {r['source_dims']} | {r['target_dims']} | "
            f"{r['output_dims']} | {r['file_size_kb']} | {r['quality']} |"
        )

    VERIF_MD.write_text("\n".join(md_lines) + "\n")

    # Pick 3 random heroes + 3 random tiles for spot-check
    rng = random.Random(20260525)
    ok_heroes = [r["slot_id"] for r in records if r["status"] == "OK" and r["slot_id"].endswith("-hero")]
    ok_tiles = [r["slot_id"] for r in records if r["status"] == "OK" and "-tile-" in r["slot_id"]]
    rng.shuffle(ok_heroes)
    rng.shuffle(ok_tiles)
    spot_heroes = ok_heroes[:3]
    spot_tiles = ok_tiles[:3]

    print()
    print("=" * 72)
    print("PHASE 3 SUMMARY")
    print("=" * 72)
    print(f"  Processed OK:       {len(ok)} of {len(targets)}")
    print(f"  WARN (oversize):    {len(warn)}")
    print(f"  FAIL:               {len(fail)}")
    print(f"  Required Q<85:      {len(reduced_q)}")
    print(f"  File size (KB):     min {smin:.1f} / avg {savg:.1f} / max {smax:.1f}")
    print(f"  Verification table: {VERIF_MD.relative_to(ROOT)}")
    print()
    print("Spot check — 3 hero + 3 tile slot_ids randomly selected:")
    for s in spot_heroes + spot_tiles:
        print(f"  open '{(PROC_DIR / (s + '.jpg')).resolve()}'")


if __name__ == "__main__":
    main()
