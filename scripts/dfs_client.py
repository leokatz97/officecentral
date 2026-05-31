#!/usr/bin/env python3
"""Shared DataForSEO REST client for COMPETITOR-KEYWORD-RECON-1.

Reads credentials from .mcp.json (DATAFORSEO_USERNAME / DATAFORSEO_PASSWORD).
Drives the REST API directly (the MCP tools return into the agent context, which
does not scale to thousands of keywords). Read-only data pulls only.
"""
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "reports", "keyword-research", "raw")
OUT = os.path.join(ROOT, "data", "reports", "keyword-research")
os.makedirs(RAW, exist_ok=True)

LOCATION_CANADA = 2124
LANG = "en"
BASE = "https://api.dataforseo.com"


def _creds():
    cfg = json.load(open(os.path.join(ROOT, ".mcp.json")))
    env = cfg["mcpServers"]["dataforseo-mcp"]["env"]
    return env["DATAFORSEO_USERNAME"], env["DATAFORSEO_PASSWORD"]


def _auth_header():
    u, p = _creds()
    tok = base64.b64encode(f"{u}:{p}".encode()).decode()
    return f"Basic {tok}"


def post(path, payload, retries=3, backoff=5):
    """POST to a DataForSEO endpoint. payload is the task array (list of dicts)."""
    url = BASE + path
    data = json.dumps(payload).encode()
    last_err = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", _auth_header())
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                body = json.loads(r.read().decode())
            sc = body.get("status_code")
            if sc == 40000 or (isinstance(sc, int) and 40100 <= sc <= 40299):
                # auth error class
                raise RuntimeError(f"AUTH/REQUEST ERROR status_code={sc} msg={body.get('status_message')}")
            if sc != 20000:
                # could be rate limit (40202) etc. -> retry
                last_err = f"status_code={sc} msg={body.get('status_message')}"
                if attempt < retries:
                    time.sleep(backoff * attempt)
                    continue
            return body
        except urllib.error.HTTPError as e:
            code = e.code
            txt = e.read().decode()[:300]
            if code in (401, 403):
                raise RuntimeError(f"AUTH FAILURE HTTP {code}: {txt}")
            last_err = f"HTTP {code}: {txt}"
            if attempt < retries:
                time.sleep(backoff * attempt)
                continue
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = f"NETERR {e}"
            if attempt < retries:
                time.sleep(backoff * attempt)
                continue
    raise RuntimeError(f"Unrecoverable after {retries} retries: {last_err}")


def save_raw(name, obj):
    p = os.path.join(RAW, name)
    json.dump(obj, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    # Preflight auth test: cheap SERP live call
    body = post("/v3/serp/google/organic/live/advanced", [{
        "keyword": "office furniture peterborough",
        "location_code": LOCATION_CANADA,
        "language_code": LANG,
        "depth": 10,
    }])
    print("AUTH OK" if body.get("status_code") == 20000 else f"AUTH PROBLEM {body.get('status_code')}")
    print("cost", body.get("cost"), "tasks", len(body.get("tasks", [])))
