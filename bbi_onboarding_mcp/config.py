"""Central configuration for the BBI Onboarding MCP.

All secrets come from environment variables ONLY — never from tool args, never
logged. The Shopify token is held server-side and never leaves this process.

API-version policy (per build directive #3):
  - Newly-authored reads/writes use DEFAULT_API (current, supported version).
  - Functions LIFTED from proven push-* scripts keep the exact version they were
    tested against — declared as per-call overrides, not frozen globally.
  - The legacy 2024-01 smart_collections endpoint is NOT used in new code; the
    smart-collection rule read is re-authored on DEFAULT_API.
"""
from __future__ import annotations

import os
from pathlib import Path

# ── Repo paths ──────────────────────────────────────────────────────────────
# config.py lives at bbi_onboarding_mcp/config.py -> repo root is one parent up.
PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parent
ENV_PATH = REPO_ROOT / ".env"

# The server holds its OWN copy of the canonical references (bundled in the
# package so a deployed host is self-contained — data/ is gitignored). Falls
# back to the repo's data/ dirs for local development if the bundle is absent.
_PKG_REF = PKG_DIR / "reference_data"
REFERENCE_DIR = _PKG_REF if _PKG_REF.exists() else (REPO_ROOT / "data" / "reference")
EXPORT_DIR = _PKG_REF if _PKG_REF.exists() else (REPO_ROOT / "data" / "exports")

# Backups + audit logs: a writable data dir (override with MCP_DATA_DIR on a host
# where the repo layout isn't present).
_DATA_DIR = Path(os.environ.get("MCP_DATA_DIR", str(REPO_ROOT / "data")))
BACKUP_DIR = _DATA_DIR / "backups"
LOG_DIR = _DATA_DIR / "logs"

# Canonical reference files (authoritative YAML sources + merged snapshot).
SKU_PREFIX_YAML = REFERENCE_DIR / "sku-prefix-lookup.yaml"
MANUFACTURER_DEFAULTS_YAML = REFERENCE_DIR / "manufacturer-defaults.yaml"
BRAND_ROUTING_YAML = REFERENCE_DIR / "brand-collection-routing.yaml"
# The merged snapshot the intake skill bundles. We load the newest matching file.
EXPORT_GLOB = "brand-onboarding-reference-*.json"


def _load_dotenv() -> None:
    """Mirror the push-* scripts: read .env into os.environ without overriding
    anything already set in the real environment (env wins over file)."""
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()


# ── Shopify ─────────────────────────────────────────────────────────────────
SHOPIFY_TOKEN = os.environ.get("SHOPIFY_TOKEN")
# Normalize store to the bare myshopify domain.
_raw_store = os.environ.get("SHOPIFY_STORE", "office-central-online.myshopify.com")
if not _raw_store.endswith(".myshopify.com"):
    _raw_store = f"{_raw_store}.myshopify.com"
SHOPIFY_STORE = _raw_store
ADMIN_STORE_SLUG = SHOPIFY_STORE.replace(".myshopify.com", "")

# Default API version for newly-authored calls. Current + supported.
DEFAULT_API = os.environ.get("SHOPIFY_API_VERSION", "2024-10")
# Versions the lifted write functions were proven against (do not bump blindly).
PRODUCT_CREATE_API = "2026-04"   # consolidate-shipping.py create_product()
IMAGE_API = "2026-04"            # push-generated-images.py push_image()
WRITE_GQL_API = "2024-10"        # push-b4s1 productUpdate / metafieldsSet / collects / readback

# Admin UI base (for human-clickable links in tool results).
ADMIN_BASE = f"https://admin.shopify.com/store/{ADMIN_STORE_SLUG}"
STOREFRONT_BASE = "https://www.brantbusinessinteriors.com"

# Online-store nav menu handle a sub-collection is placed under (verified live).
NAV_MENU_HANDLE = os.environ.get("MCP_NAV_MENU_HANDLE", "main-menu-2")


# ── MCP auth ────────────────────────────────────────────────────────────────
# "bearer"  -> validate a static shared secret (local test + programmatic MCP
#              clients that CAN send Authorization: Bearer). NOT usable from the
#              Claude consumer custom-connector dialog (it has no token field).
# "oauth"   -> OAuth 2.1 resource server: verify RS256 JWTs from an external IdP
#              via JWKS. This is the path Claude's "Add custom connector" flow
#              authenticates with. See README.
# "none"    -> no auth (local dry-run only; refuses to start if a write is live).
AUTH_MODE = os.environ.get("MCP_AUTH_MODE", "bearer").lower()
MCP_AUTH_SECRET = os.environ.get("MCP_AUTH_SECRET")  # bearer mode shared secret

# OAuth mode settings (external IdP issues the tokens; we only verify).
OAUTH_JWKS_URL = os.environ.get("OAUTH_JWKS_URL")        # e.g. https://you.auth0.com/.well-known/jwks.json
OAUTH_ISSUER = os.environ.get("OAUTH_ISSUER")            # token `iss` must match
OAUTH_AUDIENCE = os.environ.get("OAUTH_AUDIENCE")        # token `aud` must match (this server)
OAUTH_REQUIRED_SCOPE = os.environ.get("OAUTH_REQUIRED_SCOPE", "")  # optional space-delimited

# Public URL of this server (for RFC 9728 Protected Resource Metadata).
PUBLIC_URL = os.environ.get("MCP_PUBLIC_URL", "").rstrip("/")

# Server bind.
HOST = os.environ.get("MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("MCP_PORT", "8000"))

# Hard policy constants (cannot be overridden by callers).
FORBIDDEN_VENDOR = "Brant Business Interiors"   # never settable as vendor (BBI rule)
MIN_IMAGE_PX = 500                              # smallest acceptable image edge
DEFAULT_CONDITION = "new"


class ConfigError(RuntimeError):
    pass


def require_shopify_token() -> str:
    if not SHOPIFY_TOKEN:
        raise ConfigError(
            "SHOPIFY_TOKEN is not set. The server holds the Shopify token in its "
            "environment only; refusing to make Admin API calls without it."
        )
    return SHOPIFY_TOKEN
