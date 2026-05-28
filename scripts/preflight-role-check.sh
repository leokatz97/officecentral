#!/usr/bin/env bash
# preflight-role-check.sh
#
# Pre-write theme-role verification gate. Asserts, via a fresh Admin API call,
# that the LIVE (role=main) theme is the expected production theme — id
# 186373570873 — and that exactly one theme holds role=main. Fails loud on the
# dangerous case where a DIFFERENT theme has become main (someone republished),
# which is precisely the stale-label failure class that motivated this check.
#
# Why this exists: 2026-05-27 late-night (QW-1 incident). Stale auto-memory
# (feedback_push_target.md) framed 186373570873 as "the dev theme" — true
# pre-LAUNCH-2, false since the 2026-05-26 launch when it became role=main /
# production. The label was propagated into a verification table by accident.
# A memory- or name-derived assertion can drift; an API-derived assertion of
# {id, role} cannot. This check is that API-derived assertion.
#
# Behaviour:
#   exit 0 + "RESULT: PASS"  — exactly one role=main theme AND its id == expect-id.
#   exit 1 + "RESULT: FAIL"  — any of: API error/timeout/bad shape; token missing;
#                              zero main themes; >1 main theme; main theme has an
#                              id other than expect-id. Fails LOUD, never silent.
#   Soft WARN (does NOT fail): rollback theme 178274435385 role != unpublished,
#                              or main theme name differs from expected. These are
#                              surfaced but do not block, per the design decision
#                              (warn on name/rollback drift; fail only on the
#                              production main id/role mismatch).
#
# On PASS, emits a machine-readable diagnostic line:
#   VERIFIED: id=<id> role=main name=<name> updated_at=<ts>
# so a session can paste the API-derived {id, role, name} triple straight into a
# verification table — eliminating the QW-1 framing error at write time.
#
# Usage:
#   scripts/preflight-role-check.sh                 # expects id 186373570873
#   scripts/preflight-role-check.sh --expect-id N   # protect a different prod theme
#
# Final stdout line is always `RESULT: PASS` or `RESULT: FAIL` — greppable by the
# preflight-write-check.sh wrapper, CI, or agent workflows.
#
# Requires: bash, python3 (urllib stdlib). SHOPIFY_TOKEN in environment (loaded
# from .env if present). The token is never echoed.
#
# Wired into BBI-Session-Kickoff/01-safety-preflight.md as a pre-write gate, run
# at session start (via preflight-write-check.sh) and re-runnable before each PUT.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STORE_DOMAIN="office-central-online.myshopify.com"
API_VERSION="2026-04"
EXPECT_ID="186373570873"
EXPECT_NAME="BBI Landing Dev"
ROLLBACK_ID="178274435385"

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }

# --expect-id override (defaults to the current production theme).
while [[ $# -gt 0 ]]; do
    case "$1" in
        --expect-id) EXPECT_ID="${2:-}"; shift 2 ;;
        *) red "preflight-role-check: unknown argument '$1'"; echo "RESULT: FAIL"; exit 1 ;;
    esac
done

# Load SHOPIFY_TOKEN from .env if not already set.
if [[ -z "${SHOPIFY_TOKEN:-}" && -f "${REPO_ROOT}/.env" ]]; then
    # shellcheck disable=SC2046
    export $(grep -v '^#' "${REPO_ROOT}/.env" | xargs)
fi

if [[ -z "${SHOPIFY_TOKEN:-}" ]]; then
    red "preflight-role-check: HALT — SHOPIFY_TOKEN not set (and not found in .env). Cannot verify theme role."
    echo "RESULT: FAIL"
    exit 1
fi

# Allow an injected fixture for testing the assertion logic without a live call.
# PREFLIGHT_ROLE_FIXTURE=/path/to/themes.json bypasses the network and feeds the
# parser a captured/edited response. Used by the Phase-2 fail-on-bad tests; never
# set in normal operation.
FIXTURE="${PREFLIGHT_ROLE_FIXTURE:-}"

STORE_DOMAIN="$STORE_DOMAIN" API_VERSION="$API_VERSION" EXPECT_ID="$EXPECT_ID" \
EXPECT_NAME="$EXPECT_NAME" ROLLBACK_ID="$ROLLBACK_ID" FIXTURE="$FIXTURE" \
python3 <<'PY'
import json, os, sys, urllib.request

store   = os.environ["STORE_DOMAIN"]
api     = os.environ["API_VERSION"]
expect  = os.environ["EXPECT_ID"]
ename   = os.environ["EXPECT_NAME"]
rbid    = os.environ["ROLLBACK_ID"]
fixture = os.environ.get("FIXTURE", "")
token   = os.environ["SHOPIFY_TOKEN"]

def fail(msg):
    sys.stderr.write("")  # keep token out of any trace
    print(f"\033[31mpreflight-role-check: HALT — {msg}\033[0m")
    print("RESULT: FAIL")
    sys.exit(1)

# Acquire themes list: fixture file (test) or live Admin API.
try:
    if fixture:
        with open(fixture, "r", encoding="utf-8") as fh:
            raw = fh.read()
    else:
        url = f"https://{store}/admin/api/{api}/themes.json"
        req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": token})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                fail(f"Admin API returned HTTP {resp.status} — cannot verify role. Treat as unsafe.")
            raw = resp.read().decode("utf-8")
except Exception as e:
    fail(f"Admin API call failed ({type(e).__name__}: {e}) — cannot verify role. Treat as unsafe.")

# Parse + validate shape.
try:
    themes = json.loads(raw)["themes"]
    if not isinstance(themes, list):
        raise ValueError("'themes' is not a list")
except Exception as e:
    fail(f"unexpected response shape ({type(e).__name__}: {e}) — cannot verify role. Treat as unsafe.")

mains = [t for t in themes if t.get("role") == "main"]

if len(mains) == 0:
    fail("no theme has role=main in the Admin API response. Site may be mid-republish. HALT.")
if len(mains) > 1:
    ids = ", ".join(str(t.get("id")) for t in mains)
    fail(f"{len(mains)} themes report role=main (ids: {ids}). Ambiguous production target. HALT.")

main = mains[0]
mid  = str(main.get("id"))
name = main.get("name", "")
upd  = main.get("updated_at", "")

if mid != expect:
    fail(f"LIVE (role=main) theme is id={mid} name={name!r}, expected id={expect}. "
         f"A DIFFERENT theme has been published as production — someone republished, "
         f"or roles drifted. Do NOT write. Reconcile first. HALT.")

# Production main id+role confirmed. Soft warnings below do not fail.
if name != ename:
    print(f"\033[33mpreflight-role-check: WARN — main theme name is {name!r}, "
          f"expected {ename!r}. id+role correct; name drift only (non-fatal).\033[0m")

rb = next((t for t in themes if str(t.get("id")) == rbid), None)
if rb is None:
    print(f"\033[33mpreflight-role-check: WARN — rollback theme {rbid} not found in theme list (non-fatal).\033[0m")
elif rb.get("role") != "unpublished":
    print(f"\033[33mpreflight-role-check: WARN — rollback theme {rbid} role={rb.get('role')!r}, "
          f"expected 'unpublished' (non-fatal).\033[0m")

print(f"\033[32mpreflight-role-check: OK — production theme verified via Admin API.\033[0m")
print(f"VERIFIED: id={mid} role=main name={name} updated_at={upd}")
print("RESULT: PASS")
sys.exit(0)
PY
exit $?
