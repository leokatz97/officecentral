#!/usr/bin/env bash
# test-preflight-checks.sh — verification-of-the-verifier for the preflight gates.
#
# A safety check that PASSES when it should FAIL is worse than no check: it gives
# false confidence on every future write. So each preflight check is exercised here
# against BOTH a known-good input (must PASS) and known-bad inputs (must FAIL /
# must report mismatch). The fail-on-bad cases are the load-bearing ones — they
# prove the check actually catches the danger, not just that it rubber-stamps.
#
# All bad inputs are SYNTHETIC local fixtures (constructed in a temp dir). Nothing
# live is ever mutated — role-check bad cases use a captured-shape themes.json
# fixture via the PREFLIGHT_ROLE_FIXTURE escape hatch; byte-compare uses local
# file pairs. A separate LIVE role-check run confirms real-world PASS.
#
# Usage: scripts/test-preflight-checks.sh
# Exit 0 if every assertion holds; exit 1 if any test behaved unexpectedly.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="${REPO_ROOT}/scripts"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass_count=0
fail_count=0

# assert_result <label> <expected-RESULT-token> <actual-stdout>
assert_result() {
    local label="$1" expected="$2" output="$3"
    local got
    got="$(printf '%s\n' "$output" | grep -oE 'RESULT: [A-Z_]+' | tail -1 | awk '{print $2}')"
    if [[ "$got" == "$expected" ]]; then
        printf '  \033[32m[OK]\033[0m   %-52s expected=%-18s got=%s\n' "$label" "$expected" "$got"
        pass_count=$((pass_count+1))
    else
        printf '  \033[31m[FAIL]\033[0m %-52s expected=%-18s got=%s\n' "$label" "$expected" "${got:-<none>}"
        fail_count=$((fail_count+1))
    fi
}

# ---------------------------------------------------------------------------
echo "=============================================================="
echo " ROLE-CHECK  (preflight-role-check.sh)"
echo "=============================================================="

# Synthetic themes.json fixtures.
cat > "$TMP/role_good.json" <<'JSON'
{"themes":[
  {"id":186373570873,"name":"BBI Landing Dev","role":"main","updated_at":"2026-05-26T20:33:23-04:00"},
  {"id":178274435385,"name":"BBI Live","role":"unpublished","updated_at":"2026-05-26T20:08:47-04:00"}
]}
JSON

cat > "$TMP/role_wrong_id.json" <<'JSON'
{"themes":[
  {"id":999999999,"name":"Some Other Theme","role":"main","updated_at":"2026-05-28T00:00:00-04:00"},
  {"id":186373570873,"name":"BBI Landing Dev","role":"unpublished","updated_at":"2026-05-26T20:33:23-04:00"}
]}
JSON

cat > "$TMP/role_no_main.json" <<'JSON'
{"themes":[
  {"id":186373570873,"name":"BBI Landing Dev","role":"unpublished"},
  {"id":178274435385,"name":"BBI Live","role":"unpublished"}
]}
JSON

cat > "$TMP/role_multi_main.json" <<'JSON'
{"themes":[
  {"id":186373570873,"name":"BBI Landing Dev","role":"main"},
  {"id":178274435385,"name":"BBI Live","role":"main"}
]}
JSON

cat > "$TMP/role_bad_shape.json" <<'JSON'
{"not_themes":{"oops":true}}
JSON

cat > "$TMP/role_name_drift.json" <<'JSON'
{"themes":[
  {"id":186373570873,"name":"Renamed Theme","role":"main","updated_at":"2026-05-26T20:33:23-04:00"},
  {"id":178274435385,"name":"BBI Live","role":"unpublished"}
]}
JSON

cat > "$TMP/role_rollback_drift.json" <<'JSON'
{"themes":[
  {"id":186373570873,"name":"BBI Landing Dev","role":"main","updated_at":"2026-05-26T20:33:23-04:00"},
  {"id":178274435385,"name":"BBI Live","role":"development"}
]}
JSON

run_role() { PREFLIGHT_ROLE_FIXTURE="$1" bash "${SCRIPTS}/preflight-role-check.sh" 2>&1; }

echo "-- pass-on-good --"
assert_result "good fixture (id+role correct)"          PASS "$(run_role "$TMP/role_good.json")"
assert_result "name drift (soft WARN, still passes)"    PASS "$(run_role "$TMP/role_name_drift.json")"
assert_result "rollback role drift (soft WARN, passes)" PASS "$(run_role "$TMP/role_rollback_drift.json")"

echo "-- fail-on-bad (the load-bearing cases) --"
assert_result "DIFFERENT theme is main (dangerous)"     FAIL "$(run_role "$TMP/role_wrong_id.json")"
assert_result "no theme has role=main"                  FAIL "$(run_role "$TMP/role_no_main.json")"
assert_result "multiple themes report role=main"        FAIL "$(run_role "$TMP/role_multi_main.json")"
assert_result "malformed response shape"                FAIL "$(run_role "$TMP/role_bad_shape.json")"

echo "-- live (real Admin API, read-only) --"
LIVE_OUT="$(bash "${SCRIPTS}/preflight-role-check.sh" 2>&1)"
assert_result "live production state"                   PASS "$LIVE_OUT"
printf '%s\n' "$LIVE_OUT" | grep -E '^VERIFIED:' | sed 's/^/        /'

# ---------------------------------------------------------------------------
echo
echo "=============================================================="
echo " BYTE-COMPARE  (preflight-byte-compare.py)"
echo "=============================================================="

# Base JSON with forward slashes and a couple of keys/values.
cat > "$TMP/a.json" <<'JSON'
{"sections":{"hero":{"type":"bbi-hero","url":"https://cdn.shopify.com/s/files/1/x/y.png","alt":"Hero"}},"order":["hero"]}
JSON

# Identical copy.
cp "$TMP/a.json" "$TMP/b_identical.json"

# Differs ONLY by forward-slash re-escape (Shopify serializer toggle).
sed 's#https://cdn.shopify.com/s/files/1/x/y.png#https:\\/\\/cdn.shopify.com\\/s\\/files\\/1\\/x\\/y.png#' \
    "$TMP/a.json" > "$TMP/b_slash.json"

# Differs ONLY by an extra trailing newline.
cp "$TMP/a.json" "$TMP/b_newline.json"; printf '\n\n' >> "$TMP/b_newline.json"

# Differs ONLY by JSON key ordering (same values), via canonical-ish reorder.
python3 - "$TMP/a.json" "$TMP/b_keyorder.json" <<'PY'
import json, sys
o = json.load(open(sys.argv[1]))
# Re-emit with keys reversed at top level and inside hero to force a different order.
hero = o["sections"]["hero"]
reordered = {
  "order": o["order"],
  "sections": {"hero": {"alt": hero["alt"], "url": hero["url"], "type": hero["type"]}},
}
open(sys.argv[2], "w").write(json.dumps(reordered, indent=2))
PY

# Differs by a REAL value change (the critical fail-on-real-drift case).
sed 's#"alt":"Hero"#"alt":"DIFFERENT ALT TEXT"#' "$TMP/a.json" > "$TMP/b_real.json"

# Liquid pair: trailing-newline only -> match.
printf 'Hello {{ x }} world\n' > "$TMP/a.liquid"
printf 'Hello {{ x }} world\n\n' > "$TMP/b_liquid_newline.liquid"
# Liquid pair: real change -> mismatch.
printf 'Hello {{ y }} world\n' > "$TMP/b_liquid_real.liquid"
# Liquid pair: \/ difference -> MISMATCH (json normalization must NOT apply to .liquid).
printf 'see https://x/y\n'  > "$TMP/a2.liquid"
printf 'see https:\\/\\/x\\/y\n' > "$TMP/b_liquid_slash.liquid"

run_bc() { python3 "${SCRIPTS}/preflight-byte-compare.py" "$@" 2>&1; }

echo "-- noise must be classified SEMANTIC_MATCH (or IDENTICAL) --"
assert_result "json identical copy"                IDENTICAL      "$(run_bc "$TMP/a.json" "$TMP/b_identical.json")"
assert_result "json forward-slash re-escape only"  SEMANTIC_MATCH "$(run_bc "$TMP/a.json" "$TMP/b_slash.json")"
assert_result "json trailing-newline only"         SEMANTIC_MATCH "$(run_bc "$TMP/a.json" "$TMP/b_newline.json")"
assert_result "json key-order only"                SEMANTIC_MATCH "$(run_bc "$TMP/a.json" "$TMP/b_keyorder.json")"
assert_result "liquid trailing-newline only"       SEMANTIC_MATCH "$(run_bc "$TMP/a.liquid" "$TMP/b_liquid_newline.liquid")"

echo "-- real drift must be SEMANTIC_MISMATCH (the load-bearing cases) --"
assert_result "json real value change"             SEMANTIC_MISMATCH "$(run_bc "$TMP/a.json" "$TMP/b_real.json")"
assert_result "liquid real change"                 SEMANTIC_MISMATCH "$(run_bc "$TMP/a.liquid" "$TMP/b_liquid_real.liquid")"
assert_result "liquid \\/ diff (json-norm OFF)"    SEMANTIC_MISMATCH "$(run_bc "$TMP/a2.liquid" "$TMP/b_liquid_slash.liquid")"

# ---------------------------------------------------------------------------
echo
echo "=============================================================="
printf ' TOTAL: %d passed, %d failed\n' "$pass_count" "$fail_count"
echo "=============================================================="
[[ $fail_count -eq 0 ]] && { echo "RESULT: PASS"; exit 0; } || { echo "RESULT: FAIL"; exit 1; }
