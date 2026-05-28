#!/usr/bin/env bash
# preflight-write-check.sh
#
# Session-start write gate. Runs the two binary, run-once preflight gates in
# sequence and emits ONE combined RESULT line:
#   1. preflight-watcher-check.sh — no `shopify theme` process may be running.
#   2. preflight-role-check.sh    — production theme (id 186373570873) is the
#                                   sole role=main, verified via fresh Admin API.
#
# This is the single command to run at the start of every production write
# session — one invocation, one RESULT, so no individual gate can be forgotten
# (the 2026-05-27 watcher incident root cause was a gate the doc did not name and
# the session therefore never ran).
#
# The byte-content comparison (preflight-byte-compare.py) is deliberately NOT part
# of this wrapper: it runs per-file INSIDE the write loop, takes two file
# arguments, and emits a 3-way classification — it is not a session-start binary
# gate. Run it separately for each file around its PUT.
#
# Behaviour:
#   exit 0 + "RESULT: PASS"  — BOTH sub-gates passed.
#   exit 1 + "RESULT: FAIL"  — either sub-gate failed (or could not verify).
#
# Sub-checks remain individually runnable:
#   scripts/preflight-watcher-check.sh   (process gate; re-run anytime)
#   scripts/preflight-role-check.sh      (role gate; re-run before each PUT)
#
# Final stdout line is always `RESULT: PASS` or `RESULT: FAIL`.
# Any extra args are forwarded to preflight-role-check.sh (e.g. --expect-id).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }

overall=0

echo "=== preflight-write-check: STEP 1/2 — watcher ==="
if ! bash "${SCRIPT_DIR}/preflight-watcher-check.sh"; then
    overall=1
fi
echo

echo "=== preflight-write-check: STEP 2/2 — theme role ==="
if ! bash "${SCRIPT_DIR}/preflight-role-check.sh" "$@"; then
    overall=1
fi
echo

if [[ $overall -eq 0 ]]; then
    green "preflight-write-check: OK — watcher + role gates both PASS. Safe to begin write session."
    echo "RESULT: PASS"
    exit 0
else
    red "preflight-write-check: HALT — one or more sub-gates FAILED. Do NOT write. See output above."
    echo "RESULT: FAIL"
    exit 1
fi
