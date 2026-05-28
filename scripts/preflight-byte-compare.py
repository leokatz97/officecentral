#!/usr/bin/env python3
"""preflight-byte-compare.py — semantic-vs-noise diff classifier for theme writes.

Purpose
-------
When comparing a local file to LIVE around a PUT (pre-write drift check, or
post-write byte-match verification), a bare sha-equality test HALTs on serializer
NOISE that is not a real change — most commonly Shopify's JSON serializer toggling
forward-slash escaping (`/` <-> `\\/`) on a Theme-Editor save. This was the "Path A"
false-positive on 2026-05-27 final-night: a strict byte-match correctly halted on a
raw mismatch whose entire 378-byte delta was `\\/` re-escape (zero substantive diff),
costing a manual pull+re-edit.

This tool makes BYTE CONTENT the primary signal and classifies the difference into
three buckets so a session sees "semantically identical, differs only by \\/ re-escape
— safe to proceed" instead of a bare HALT — WITHOUT ever masking a real change.

It is intentionally pure and network-free: it takes two already-materialized files
and does no Admin API calls. The caller is responsible for pulling LIVE correctly
(target the production theme 186373570873 explicitly — NOT fetch-file.py's default,
which still points at the unpublished rollback 178274435385). Keeping this tool free
of theme knowledge makes it trivially testable against local fixtures.

Normalization classes (cumulative; the EARLIEST level that matches is reported)
-------------------------------------------------------------------------------
  0. raw                         -> IDENTICAL
  1. trailing newline/CR strip   -> SEMANTIC_MATCH (class: trailing-newline)   [all files]
  2. forward-slash unescape      -> SEMANTIC_MATCH (class: json forward-slash re-escape)  [.json only]
  3. JSON canonical (sort_keys)  -> SEMANTIC_MATCH (class: json key-order / formatting)   [.json only]
  else                           -> SEMANTIC_MISMATCH

Normalization only ever reorders / re-formats / unescapes — it never alters a VALUE.
A genuine value change (e.g. a URL or a settings string "foo" -> "bar") survives every
class and is reported as SEMANTIC_MISMATCH. Proving that (fail-on-real-drift) is the
load-bearing test: an over-aggressive normalizer that masks real changes is the
dangerous failure mode, far worse than a spurious HALT.

Output contract
---------------
Diagnostics (stdout):
  LOCAL: <path> raw_sha=<sha256>
  LIVE:  <path> raw_sha=<sha256>
  norm:  <which class accounted for the difference>            (when not IDENTICAL/MISMATCH)
Final line (always, greppable):
  RESULT: IDENTICAL | SEMANTIC_MATCH | SEMANTIC_MISMATCH
Exit codes: 0 = IDENTICAL or SEMANTIC_MATCH (safe to proceed);
            2 = SEMANTIC_MISMATCH (real drift — HALT);
            1 = usage / read error.

Usage
-----
  scripts/preflight-byte-compare.py <local-file> <live-file>
  scripts/preflight-byte-compare.py --json <local> <live>   # force JSON normalization
  scripts/preflight-byte-compare.py --text <local> <live>   # force text-only (skip JSON)

Wired into BBI-Session-Kickoff/01-safety-preflight.md as the pre-write drift check
and post-write byte-match verification, replacing bare sha-equality HALTs.
"""

import hashlib
import json
import sys


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def strip_trailing_eol(text: str) -> str:
    # Class 1: only trailing CR/LF at EOF. Deliberately minimal — does not touch
    # interior whitespace or trailing spaces, so it cannot mask a meaningful edit.
    return text.rstrip("\r\n")


def json_canonical(text: str):
    # Returns canonical form (sorted keys, no forward-slash escaping, stable
    # separators) or None if the text is not valid JSON. Only reorders/reformats
    # — every value is preserved exactly.
    try:
        obj = json.loads(text)
    except Exception:
        return None
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def classify(local_path, live_path, force_mode=None):
    try:
        with open(local_path, "rb") as f:
            raw_a = f.read()
        with open(live_path, "rb") as f:
            raw_b = f.read()
    except OSError as e:
        print(f"preflight-byte-compare: ERROR — cannot read input ({e})", file=sys.stderr)
        print("RESULT: ERROR")
        return 1, None, None

    sha_a, sha_b = sha256_bytes(raw_a), sha256_bytes(raw_b)
    print(f"LOCAL: {local_path} raw_sha={sha_a}")
    print(f"LIVE:  {live_path} raw_sha={sha_b}")

    # Level 0 — raw byte identity.
    if raw_a == raw_b:
        print("RESULT: IDENTICAL")
        return 0, "IDENTICAL", None

    # Decode for normalization. Undecodable (binary) -> cannot normalize -> mismatch.
    try:
        text_a = raw_a.decode("utf-8")
        text_b = raw_b.decode("utf-8")
    except UnicodeDecodeError:
        print("norm:  (binary / non-utf8 — cannot normalize)")
        print("RESULT: SEMANTIC_MISMATCH")
        return 2, "SEMANTIC_MISMATCH", "binary"

    # Decide whether JSON normalization applies.
    if force_mode == "json":
        is_json = True
    elif force_mode == "text":
        is_json = False
    else:
        is_json = local_path.endswith(".json") or live_path.endswith(".json")

    # Level 1 — trailing EOL strip (all file types).
    a1, b1 = strip_trailing_eol(text_a), strip_trailing_eol(text_b)
    if a1 == b1:
        print("norm:  trailing-newline (EOF CR/LF only)")
        print("RESULT: SEMANTIC_MATCH")
        return 0, "SEMANTIC_MATCH", "trailing-newline"

    if is_json:
        # Level 2 — forward-slash unescape (isolates the Shopify \/ serializer toggle).
        a2, b2 = a1.replace("\\/", "/"), b1.replace("\\/", "/")
        if a2 == b2:
            print("norm:  json forward-slash re-escape (\\/ <-> /)")
            print("RESULT: SEMANTIC_MATCH")
            return 0, "SEMANTIC_MATCH", "fwd-slash"

        # Level 3 — full JSON canonicalization (key-order + formatting).
        ca, cb = json_canonical(text_a), json_canonical(text_b)
        if ca is not None and cb is not None and ca == cb:
            print("norm:  json key-order / formatting (canonical re-serialize)")
            print("RESULT: SEMANTIC_MATCH")
            return 0, "SEMANTIC_MATCH", "json-canonical"

    # Nothing neutralized the difference — a real, value-level change remains.
    print("norm:  none — content differs after all normalization classes")
    print("RESULT: SEMANTIC_MISMATCH")
    return 2, "SEMANTIC_MISMATCH", None


def main(argv):
    args = argv[1:]
    force_mode = None
    if args and args[0] in ("--json", "--text"):
        force_mode = args[0][2:]
        args = args[1:]
    if len(args) != 2:
        print("usage: preflight-byte-compare.py [--json|--text] <local-file> <live-file>",
              file=sys.stderr)
        return 1
    code, _result, _cls = classify(args[0], args[1], force_mode)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
