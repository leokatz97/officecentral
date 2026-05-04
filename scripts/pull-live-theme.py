#!/usr/bin/env python3
"""Pull the BBI Live Shopify theme via Admin API.

Equivalent to `shopify theme pull --theme=178274435385 --path=theme --nodelete`,
but uses the SHOPIFY_TOKEN from .env instead of CLI OAuth (which can't open a
browser in sandboxed environments).

Behaviour:
  - Lists every asset in the target theme
  - Downloads each to ./theme/{key}, creating subdirectories as needed
  - Skips assets unchanged on disk (size match)
  - Default theme = 178274435385 (BBI Live, role=main)
  - Override with: pull-live-theme.py <theme_id>
  - Honours the same nodelete behaviour as the CLI default
"""
import json, os, pathlib, sys, time, urllib.parse, urllib.request, base64

ROOT = pathlib.Path(__file__).resolve().parents[1]
THEME_DIR = ROOT / "theme"

def load_env():
    # Try .env locations in order: cwd, repo root, parent of repo root (for worktrees)
    candidates = [
        ROOT / ".env",
        ROOT.parent / ".env",
        ROOT.parent.parent / ".env",
        ROOT.parent.parent.parent / ".env",  # worktrees: .claude/worktrees/<name> → up to repo root
    ]
    for env_path in candidates:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return
    # No .env file — assume env vars already exported (e.g. via shell `set -a; source ...`)
    if not (os.environ.get("SHOPIFY_TOKEN") or os.environ.get("SHOPIFY_ADMIN_API_TOKEN")):
        sys.exit(f"no .env found in: {[str(p) for p in candidates]}, and no SHOPIFY_TOKEN in environment")

load_env()
STORE = os.environ.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
TOKEN = os.environ.get("SHOPIFY_TOKEN") or os.environ.get("SHOPIFY_ADMIN_API_TOKEN")
if not TOKEN:
    sys.exit("SHOPIFY_TOKEN not set in .env")

THEME_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 178274435385  # BBI Live

API = f"https://{STORE}/admin/api/2024-10"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Accept": "application/json"}

def api_get(path, params=None, max_retries=6):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    delay = 1.0
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS, method="GET")
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                # Honour Retry-After if present, else exponential backoff
                ra = e.headers.get("Retry-After")
                wait = float(ra) if ra else delay
                time.sleep(wait)
                delay = min(delay * 2, 30)
                continue
            raise

def list_assets():
    return api_get(f"/themes/{THEME_ID}/assets.json")["assets"]

def fetch_asset(key):
    return api_get(f"/themes/{THEME_ID}/assets.json", {"asset[key]": key})["asset"]

def write_asset(asset):
    key = asset["key"]
    out = THEME_DIR / key
    out.parent.mkdir(parents=True, exist_ok=True)
    if "value" in asset:
        out.write_text(asset["value"], encoding="utf-8")
        return len(asset["value"]), "text"
    elif "attachment" in asset:
        data = base64.b64decode(asset["attachment"])
        out.write_bytes(data)
        return len(data), "binary"
    else:
        return 0, "empty"

def main():
    print(f"Pulling theme {THEME_ID} from {STORE} into {THEME_DIR}/")
    assets = list_assets()
    print(f"  {len(assets)} assets in remote theme")
    THEME_DIR.mkdir(exist_ok=True)
    pulled = skipped = failed = 0
    started = time.time()
    for i, a in enumerate(assets, 1):
        key = a["key"]
        local = THEME_DIR / key
        if local.exists() and local.stat().st_size == a.get("size", -1):
            skipped += 1
            continue
        try:
            full = fetch_asset(key)
            n, kind = write_asset(full)
            pulled += 1
            if pulled % 25 == 0 or i == len(assets):
                print(f"  [{i:3d}/{len(assets)}] pulled {pulled}  skipped {skipped}  failed {failed}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {key}: {e}")
        time.sleep(0.6)  # Shopify Basic = 2 req/s leaky bucket; stay safely under
    print(f"\nDone in {time.time()-started:.1f}s — pulled={pulled} skipped={skipped} failed={failed}")
    print(f"Local: {THEME_DIR}")

if __name__ == "__main__":
    main()
