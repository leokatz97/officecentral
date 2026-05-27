#!/usr/bin/env python3
"""Phase 0.D — backup LIVE theme assets (178274435385) to disk.

Downloads every asset key via Admin API (rate-limited 0.5s),
writes MANIFEST.md with restore instructions.

Output: data/backups/live-theme-pre-launch-<ts>/
"""
from __future__ import annotations
import json, os, sys, time, base64, urllib.request, urllib.parse
from pathlib import Path

STORE = "office-central-online.myshopify.com"
LIVE_ID = 178274435385
API_VER = "2026-04"
TOKEN = os.environ["SHOPIFY_TOKEN"]
TS = time.strftime("%Y%m%d-%H%M%S")
ROOT = Path(f"data/backups/live-theme-pre-launch-{TS}")


def api(path: str, method: str = "GET", body=None) -> dict:
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{API_VER}{path}",
        method=method,
        headers={
            "X-Shopify-Access-Token": TOKEN,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data=json.dumps(body).encode() if body else None,
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def main():
    print(f"backup root: {ROOT}", file=sys.stderr)
    ROOT.mkdir(parents=True, exist_ok=True)

    print("listing LIVE assets...", file=sys.stderr)
    assets = api(f"/themes/{LIVE_ID}/assets.json")["assets"]
    print(f"{len(assets)} assets to download", file=sys.stderr)

    manifest_rows = []
    downloaded = 0
    failed = []
    for i, a in enumerate(assets, 1):
        key = a["key"]
        out = ROOT / key
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            qs = urllib.parse.urlencode({"asset[key]": key})
            full = api(f"/themes/{LIVE_ID}/assets.json?{qs}")["asset"]
            if "value" in full:
                out.write_text(full["value"])
            elif "attachment" in full:
                out.write_bytes(base64.b64decode(full["attachment"]))
            else:
                failed.append((key, "no value or attachment"))
                continue
            downloaded += 1
            size = out.stat().st_size
            manifest_rows.append((key, size, a.get("updated_at", "")))
            if i % 25 == 0 or i == len(assets):
                print(f"  [{i}/{len(assets)}] {key} ({size}B)", file=sys.stderr)
        except Exception as e:
            failed.append((key, str(e)))
            print(f"  FAIL {key}: {e}", file=sys.stderr)
        time.sleep(0.5)

    # Write MANIFEST
    manifest = [
        f"# LIVE theme backup — {TS}",
        "",
        f"Source: theme {LIVE_ID} ({STORE})",
        f"Assets listed: {len(assets)}",
        f"Assets downloaded: {downloaded}",
        f"Failures: {len(failed)}",
        "",
        "## Restore instructions",
        "",
        "To restore any file to LIVE (requires Steve approval — never auto-restore):",
        "```",
        "python3 -c \"",
        "import os, json, urllib.request, base64",
        "TOKEN = os.environ['SHOPIFY_TOKEN']",
        "key = 'layout/theme.liquid'  # change this",
        f"path = '{ROOT}/' + key",
        "with open(path, 'rb') as f: data = f.read()",
        "body = {'asset': {'key': key, 'attachment': base64.b64encode(data).decode()}}",
        "req = urllib.request.Request(",
        f"    'https://{STORE}/admin/api/{API_VER}/themes/{LIVE_ID}/assets.json',",
        "    method='PUT',",
        "    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},",
        "    data=json.dumps(body).encode())",
        "print(urllib.request.urlopen(req).read())",
        "\"",
        "```",
        "",
        "## File listing",
        "",
        "| key | bytes | live updated_at |",
        "|---|---:|---|",
    ]
    for k, sz, ts in sorted(manifest_rows):
        manifest.append(f"| `{k}` | {sz} | {ts} |")
    if failed:
        manifest.append("\n## Failed downloads\n")
        for k, err in failed:
            manifest.append(f"- `{k}`: {err}")
    (ROOT / "MANIFEST.md").write_text("\n".join(manifest) + "\n")

    # Spot-check integrity: random 5 files, verify byte size matches what we wrote
    import random
    sample = random.sample(manifest_rows, min(5, len(manifest_rows)))
    print("\nSpot-check:", file=sys.stderr)
    for k, sz, _ in sample:
        actual = (ROOT / k).stat().st_size
        ok = "✓" if actual == sz else f"✗ ({actual} vs {sz})"
        print(f"  {ok} {k}", file=sys.stderr)

    summary = {
        "ts": TS, "root": str(ROOT), "listed": len(assets),
        "downloaded": downloaded, "failed": len(failed),
        "spot_check": [{"key": k, "expected": sz, "actual": (ROOT/k).stat().st_size} for k, sz, _ in sample],
    }
    Path("data/working/launch-chain-2026-05-26/live-backup-summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\nbacked up {downloaded}/{len(assets)} → {ROOT}", file=sys.stderr)


if __name__ == "__main__":
    main()
