#!/usr/bin/env bash
# preflight-watcher-check.sh
#
# Hard-fail preflight: blocks the session if any `shopify theme dev` watcher is
# running, and especially if any such process is bound to a role=main theme.
#
# Why this exists: 2026-05-27 — a `shopify theme dev` watcher (PID 28041) was
# discovered to have been running since 2026-05-11 bound to the LIVE-main theme
# 186373570873. Every local edit under theme/** was auto-PUT to LIVE within
# seconds of file save for 16 days, bypassing every approval gate. See
# docs/forensics/2026-05-27-watcher-incident.md.
#
# Behaviour (strict binary, 2026-05-27 evening posture):
#   exit 0 + "RESULT: PASS"  — zero `shopify theme` processes running.
#   exit 1 + "RESULT: FAIL"  — ANY `shopify theme` process running, regardless
#                              of subcommand (dev/push/pull/other), regardless
#                              of bound theme role.
#
# Rationale: this preflight runs immediately before a production write session.
# There is no legitimate reason for any `shopify theme` process to be running
# at that exact moment. Soft-warn previously existed for push/pull-on-non-main
# but was collapsed to FATAL because soft warnings get ignored under fatigue
# and partial discipline was the failure mode of the 2026-05-27 incident. If
# a future workflow legitimately needs a CLI process running mid-session, gate
# it behind an explicit --allow-cli-process flag or env var — do NOT bake the
# override into default behaviour.
#
# Output (when any process is detected): PID, full command line, bound theme
# ID (parsed from --theme=...), bound theme role (resolved via Admin API),
# subcommand classification (dev/push/pull/other), and a per-process FATAL
# annotation indicating which rule triggered.
#
# Final stdout line is always `RESULT: PASS` or `RESULT: FAIL` — for grepping
# by future wrapper scripts, CI, or agent workflows.
#
# Requires: bash, ps, grep, awk, python3, curl. SHOPIFY_TOKEN in environment
# (loaded from .env if present).
#
# Wired into BBI-Session-Kickoff/01-safety-preflight.md as a mandatory step
# before any production write session.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STORE_DOMAIN="office-central-online.myshopify.com"
API_VERSION="2026-04"

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }

# Load SHOPIFY_TOKEN from .env if not already set.
if [[ -z "${SHOPIFY_TOKEN:-}" && -f "${REPO_ROOT}/.env" ]]; then
    # shellcheck disable=SC2046
    export $(grep -v '^#' "${REPO_ROOT}/.env" | xargs)
fi

# Resolve theme role via Admin API. Echoes role on stdout, or "UNRESOLVED" if
# the lookup fails. Never exits — caller decides fail-loud behaviour.
resolve_theme_role() {
    local theme_id="$1"
    if [[ -z "${SHOPIFY_TOKEN:-}" ]]; then
        echo "UNRESOLVED"
        return
    fi
    local resp
    resp="$(curl -sS --max-time 10 \
        -H "X-Shopify-Access-Token: ${SHOPIFY_TOKEN}" \
        "https://${STORE_DOMAIN}/admin/api/${API_VERSION}/themes/${theme_id}.json" \
        2>/dev/null)" || { echo "UNRESOLVED"; return; }
    local role
    role="$(printf '%s' "$resp" | python3 -c \
        'import json,sys
try:
    print(json.load(sys.stdin)["theme"]["role"])
except Exception:
    print("UNRESOLVED")' 2>/dev/null)"
    if [[ -z "$role" ]]; then
        echo "UNRESOLVED"
    else
        echo "$role"
    fi
}

# Pull every running process whose command line contains "shopify theme".
# Use `ps -axo pid=,command=` for a stable, parse-friendly format. macOS ships
# bash 3.2 (no `mapfile`), so use a portable while-read loop into an array.
MATCHES=()
while IFS= read -r _line; do
    [[ -n "$_line" ]] && MATCHES+=("$_line")
done < <(ps -axo pid=,command= 2>/dev/null \
    | awk 'tolower($0) ~ /shopify[ ]+theme/ && tolower($0) !~ /preflight-watcher-check/ {print}')

if [[ ${#MATCHES[@]} -eq 0 ]]; then
    green "preflight-watcher-check: OK — no shopify theme processes running."
    echo "RESULT: PASS"
    exit 0
fi

# At least one match. Strict binary posture (2026-05-27 evening): any
# `shopify theme` process running at preflight time is FATAL, regardless of
# subcommand or bound theme. Diagnostic detail (subcmd, theme ID, role) is
# printed for the operator's benefit so they can kill the right PID with
# context, but it does NOT influence the pass/fail decision.
red "preflight-watcher-check: HALT — detected ${#MATCHES[@]} shopify theme process(es). Strict-binary posture: any such process is FATAL."
echo

for line in "${MATCHES[@]}"; do
    pid="$(awk '{print $1}' <<<"$line")"
    cmd="$(awk '{$1=""; sub(/^ /,""); print}' <<<"$line")"

    # Extract bound theme ID if present (--theme=<id> or --theme <id>).
    theme_id="$(grep -oE -- '--theme[= ][0-9]+' <<<"$cmd" \
        | head -1 \
        | grep -oE '[0-9]+' || true)"

    # Detect subcommand: dev vs push vs pull vs other.
    if grep -qE 'shopify[[:space:]]+theme[[:space:]]+dev' <<<"$cmd"; then
        subcmd="dev"
    elif grep -qE 'shopify[[:space:]]+theme[[:space:]]+push' <<<"$cmd"; then
        subcmd="push"
    elif grep -qE 'shopify[[:space:]]+theme[[:space:]]+pull' <<<"$cmd"; then
        subcmd="pull"
    else
        subcmd="other"
    fi

    if [[ -n "$theme_id" ]]; then
        role="$(resolve_theme_role "$theme_id")"
    else
        role="N/A (no --theme= flag)"
    fi

    echo "  PID:     $pid"
    echo "  subcmd:  shopify theme $subcmd"
    echo "  theme:   ${theme_id:-(none)}  role=${role}"
    echo "  cmd:     $cmd"

    # Neutral declarative FATAL line. Detail block above already shows
    # subcmd/theme/role/cmd; the FATAL line restates the operationally
    # relevant subset + the action to take. No policy rationale here —
    # that lives in 01-safety-preflight.md and the operational doc.
    if [[ -z "$theme_id" ]]; then
        red "  → FATAL: shopify theme ${subcmd} running (PID ${pid}, no --theme flag). Wait for it to complete, or kill it, before proceeding."
    elif [[ "$role" == "UNRESOLVED" ]]; then
        red "  → FATAL: shopify theme ${subcmd} running (PID ${pid}, theme ${theme_id} role=unresolvable). Wait for it to complete, or kill it, before proceeding."
    else
        red "  → FATAL: shopify theme ${subcmd} running (PID ${pid}, theme ${theme_id} role=${role}). Wait for it to complete, or kill it, before proceeding."
    fi
    echo
done

red "preflight-watcher-check: FAILED. Kill the listed PID(s) before any production write."
echo "Hint: kill <PID>   (verify with 'ps -p <PID>' returning no row)."
echo "RESULT: FAIL"
exit 1
