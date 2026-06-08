"""Authentication for the remote MCP endpoint.

Reality check (verified against Anthropic connector docs + MCP auth spec, 2026-06):
Claude's "Add custom connector" dialog has NO field for a pasted bearer token or
custom header. The only methods it authenticates with are OAuth 2.1 (DCR/CIMD) or
"authless". So this server supports two real modes plus a local-only escape hatch:

  AUTH_MODE=oauth   Production / Claude consumer connector. OAuth 2.1 resource
                    server: verify RS256 JWT access tokens from an external IdP
                    via its JWKS, check iss/aud/scope. Serves RFC 9728 Protected
                    Resource Metadata and answers unauthenticated calls with a
                    401 + WWW-Authenticate challenge so Claude can discover the AS.

  AUTH_MODE=bearer  Local test harness + programmatic MCP clients (Claude Code,
                    scripts) that CAN send `Authorization: Bearer <secret>`.
                    Validates a static shared secret (MCP_AUTH_SECRET), constant
                    time. Not usable from Claude's consumer dialog.

  AUTH_MODE=none    Local dry-run only. Refuses to serve live writes (enforced at
                    server startup). Never use on a public URL.

Implemented as pure-ASGI middleware so it never buffers the streamable-HTTP body.
The Shopify token and the auth secret are read from env only and never returned.
"""
from __future__ import annotations

import hmac
import json

from . import config

PRM_PATH = "/.well-known/oauth-protected-resource"


def _resource_metadata() -> dict:
    """RFC 9728 Protected Resource Metadata document."""
    resource = config.PUBLIC_URL or f"http://{config.HOST}:{config.PORT}"
    doc = {"resource": resource}
    if config.OAUTH_ISSUER:
        doc["authorization_servers"] = [config.OAUTH_ISSUER]
    if config.OAUTH_REQUIRED_SCOPE:
        doc["scopes_supported"] = config.OAUTH_REQUIRED_SCOPE.split()
    doc["bearer_methods_supported"] = ["header"]
    return doc


def _www_authenticate() -> str:
    resource = config.PUBLIC_URL or f"http://{config.HOST}:{config.PORT}"
    return f'Bearer resource_metadata="{resource}{PRM_PATH}"'


def _verify_bearer(token: str) -> tuple[bool, str]:
    if not config.MCP_AUTH_SECRET:
        return False, "server misconfigured: MCP_AUTH_SECRET not set"
    if hmac.compare_digest(token, config.MCP_AUTH_SECRET):
        return True, "ok"
    return False, "invalid bearer secret"


def _verify_jwt(token: str) -> tuple[bool, str]:
    if not config.OAUTH_JWKS_URL:
        return False, "server misconfigured: OAUTH_JWKS_URL not set"
    try:
        import jwt
        from jwt import PyJWKClient
    except ImportError:
        return False, "server misconfigured: PyJWT[crypto] not installed"
    # Issuer + audience are mandatory in oauth mode (enforced at startup too).
    if not config.OAUTH_ISSUER or not config.OAUTH_AUDIENCE:
        return False, "server misconfigured: OAUTH_ISSUER/OAUTH_AUDIENCE required"
    try:
        signing_key = PyJWKClient(config.OAUTH_JWKS_URL).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,                 # signature: RS256 against IdP JWKS
            algorithms=["RS256"],
            audience=config.OAUTH_AUDIENCE,   # audience: must match this server
            issuer=config.OAUTH_ISSUER,       # issuer: must match the IdP
            options={"verify_aud": True, "verify_iss": True, "verify_exp": True,
                     "require": ["exp", "iss", "aud"]},  # expiry mandatory
        )
    except Exception as e:  # noqa: BLE001 - any verification failure → 401
        return False, f"jwt verification failed: {e.__class__.__name__}"

    # Optional scope gate.
    if config.OAUTH_REQUIRED_SCOPE:
        granted = set((claims.get("scope") or "").split())
        if not set(config.OAUTH_REQUIRED_SCOPE.split()).issubset(granted):
            return False, "insufficient_scope"

    # AUTHORIZATION: the principal must be on the allowlist. A valid token is not
    # enough — this is what restricts writes to Steve's account only.
    return authorize_claims(claims)


def authorize_claims(claims: dict) -> tuple[bool, str]:
    """Allowlist check over verified token claims. Pure/testable. A valid token is
    necessary but NOT sufficient — the `sub` or email claim must be allowlisted."""
    if not config.OAUTH_ALLOWED_SUBJECTS and not config.OAUTH_ALLOWED_EMAILS:
        return False, "server misconfigured: no subject allowlist (OAUTH_ALLOWED_SUBJECTS/EMAILS)"
    sub = claims.get("sub")
    email = str(claims.get(config.OAUTH_EMAIL_CLAIM) or "").lower()
    if (sub and sub in config.OAUTH_ALLOWED_SUBJECTS) or \
       (email and email in config.OAUTH_ALLOWED_EMAILS):
        return True, "ok"
    return False, "subject not authorized"


def authenticate(headers: dict) -> tuple[bool, str]:
    """Validate the Authorization header per AUTH_MODE. Returns (ok, reason)."""
    if config.AUTH_MODE == "none":
        return True, "authless"
    raw = headers.get("authorization", "")
    if not raw.lower().startswith("bearer "):
        return False, "missing bearer token"
    token = raw[7:].strip()
    if config.AUTH_MODE == "oauth":
        return _verify_jwt(token)
    return _verify_bearer(token)


class AuthMiddleware:
    """Pure-ASGI auth gate. Serves PRM unauthenticated; 401s everything else
    that fails authentication."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        # Protected Resource Metadata is public (needed for OAuth discovery).
        if path == PRM_PATH:
            await self._json(send, 200, _resource_metadata())
            return

        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
        ok, reason = authenticate(headers)
        if not ok:
            status = 403 if reason == "insufficient_scope" else 401
            await self._json(
                send, status,
                {"error": "unauthorized", "reason": reason},
                extra_headers=[(b"www-authenticate", _www_authenticate().encode())],
            )
            return
        await self.app(scope, receive, send)

    @staticmethod
    async def _json(send, status, body, extra_headers=None):
        payload = json.dumps(body).encode()
        headers = [(b"content-type", b"application/json"),
                   (b"content-length", str(len(payload)).encode())]
        if extra_headers:
            headers.extend(extra_headers)
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": payload})
