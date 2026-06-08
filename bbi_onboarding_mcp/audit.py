"""Append-only write audit log.

Every write the server performs (or would perform, in dry-run) is appended as a
JSON line to data/logs/mcp-onboarding-<date>.jsonl. Secrets are NEVER logged —
only the action name and a sanitized detail dict.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from . import config

# Keys that must never be written to the audit log even if they appear in detail.
_REDACT = {"token", "shopify_token", "secret", "authorization", "auth_secret",
           "access_token", "password", "client_secret"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize(detail: dict) -> dict:
    clean = {}
    for k, v in (detail or {}).items():
        if k.lower() in _REDACT:
            clean[k] = "<redacted>"
        else:
            clean[k] = v
    return clean


class AuditLog:
    def __init__(self) -> None:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        day = datetime.now().strftime("%Y-%m-%d")
        self.path = config.LOG_DIR / f"mcp-onboarding-{day}.jsonl"

    def write(self, action: str, detail: dict, *, dry_run: bool = False,
              actor: str | None = None) -> None:
        entry = {
            "ts": _utc_now(),
            "action": action,
            "dry_run": bool(dry_run),
            "actor": actor or os.environ.get("MCP_ACTOR", "mcp"),
            "detail": _sanitize(detail),
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")
