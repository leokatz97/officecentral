# BBI Onboarding MCP

A remote, authenticated **MCP server** that lets Steve onboard products and
collections to the Brant Business Interiors Shopify store end-to-end from his own
Claude account — while the catalog-integrity guardrails run **server-side** (not as
skill text that can be ignored) and the **Shopify token never leaves the server**.

```
Steve's Claude  ──[custom connector: HTTPS + OAuth]──▶  BBI Onboarding MCP  ──[Admin API]──▶  Shopify
                                                        (holds the Shopify token)
```

Steve can only ever invoke the four high-level tools below. He never holds a
Shopify token and never gets raw store-write access. The tool bodies **wrap the
existing `push-*` scripts** so the server exercises code already proven against
this store.

---

## The four tools (the entire surface a client can touch)

| Tool | Kind | What it does |
|---|---|---|
| `resolve_sku` | read | SKU → resolved brand, routing collections (smart/manual + required tags), default Google category. `needs-leo` for an unknown/ambiguous prefix. Call this first to confirm the brand. |
| `onboard_product` | write | Creates a fully-enriched **DRAFT** product. Never publishes. All guards below run regardless of input. Returns a structured verification report. |
| `create_collection` | write | Creates a smart or manual collection; places a sub-collection under its parent in the nav (rejects if parent missing); registers the route and re-exports the snapshot the intake skill bundles. |
| `verify_product` | read | Current product state + born-feed-ready verdict, for Steve's pre-publish review. |

### Server-enforced guards (run regardless of what the caller asked)
- **Brand re-resolved from the SKU prefix** — the prefix wins. A payload `vendor`
  that conflicts is **rejected**; an unknown/ambiguous prefix returns `needs-leo`.
- **Vendor = resolved manufacturer.** Setting vendor to `Brant Business Interiors` is refused.
- **Duplicate guard.** If a product with that SKU (or a collection with that
  handle/name) already exists, the tool returns `already_exists` + the admin link
  instead of creating a duplicate.
- **Specs need a `source_url`.** Specs without a source are dropped and reported.
  Values are never fabricated.
- **DRAFT always.** `status=draft`; the server holds no `write_publications` scope,
  so it *cannot* publish even if asked. Publish is Steve's review gate in admin.
- **Images by URL** with a **≥500px** check; anything smaller or unverifiable is flagged.
  First passing image becomes featured.
- **Collections**: smart → tags read from the **live rule** and set to satisfy it;
  manual → `Collect`-add; missing → reported, **not** created. Membership read back.
- **`made_in_canada` / `warranty`** written only if `confirmed_by_steve` is present.
- **Backup + exact-match readback** on every write. Partial writes are reported explicitly.
- **Never writes what it can't verify.**

---

## Authentication — important reality check

Claude's **"Add custom connector"** dialog (consumer app) has **no field for a pasted
bearer token or custom header**. Verified against Anthropic's connector docs + the MCP
authorization spec (June 2026): the only methods Claude's flow authenticates with are
**OAuth 2.1** (Dynamic Client Registration / CIMD) or **authless**. A static shared
secret typed into the UI is *not supported*.

So this server has two real auth modes (plus a local-only escape hatch), selected by
`MCP_AUTH_MODE`:

| `MCP_AUTH_MODE` | Use | How it authenticates |
|---|---|---|
| `oauth` | **Production / Steve's Claude connector** | OAuth 2.1 resource server. Verifies RS256 JWT access tokens from an external IdP via its JWKS; checks `iss`/`aud`/scope. Serves RFC 9728 Protected Resource Metadata and answers unauthenticated calls with `401 + WWW-Authenticate` so Claude can discover the authorization server. |
| `bearer` | Local test harness + programmatic MCP clients (Claude Code, scripts) that *can* send `Authorization: Bearer` | Validates a static shared secret (`MCP_AUTH_SECRET`), constant-time. **Not usable from Claude's consumer dialog.** |
| `none` | Local dry-run only | No auth. The server refuses live writes in this mode. Never use on a public URL. |

The server side is the same OAuth 2.1 **resource server** either way (it verifies
tokens; it does not issue them). For `oauth` mode you point it at an **authorization
server** you control — the lowest-effort path is an IdP (Auth0, Okta, WorkOS, Keycloak,
Cognito) with the app/connection **restricted to Steve's single account**, which gives
you OAuth 2.1 + PKCE + DCR for free. See "Production OAuth setup" below.

### How writes are restricted to ONLY Steve's account
Two independent layers, both required:
1. **Token validation** (`auth.py:_verify_jwt`) — every request's `Authorization: Bearer`
   JWT is checked for **signature** (RS256 against the IdP JWKS), **issuer** (`iss` ==
   `OAUTH_ISSUER`), **audience** (`aud` == `OAUTH_AUDIENCE`), and **expiry** (`exp`
   mandatory). Any failure → `401`.
2. **Subject allowlist** (`auth.py:_verify_jwt`) — a valid token is **necessary but not
   sufficient**. The token's `sub` (or its email claim) must appear in
   `OAUTH_ALLOWED_SUBJECTS` / `OAUTH_ALLOWED_EMAILS`, or the request is rejected
   (`401 "subject not authorized"`). If the allowlist is empty the server **won't start**
   in oauth mode. This is the explicit lock to Steve — even if your IdP issued a token to
   someone else, this server refuses them.

(The IdP-side single-account restriction is belt-and-suspenders on top of layer 2.)

---

## Environment variables

| Var | Required | Notes |
|---|---|---|
| `SHOPIFY_TOKEN` | yes | Admin API token. Read from `.env` or the host env. **Server-side only — never in tool args or logs.** |
| `SHOPIFY_STORE` | no | Defaults to `office-central-online.myshopify.com`. |
| `SHOPIFY_API_VERSION` | no | Default version for newly-authored calls. Default `2024-10`. (Lifted write functions keep their own tested versions.) |
| `MCP_AUTH_MODE` | yes | `oauth` \| `bearer` \| `none`. |
| `MCP_AUTH_SECRET` | bearer mode | Shared secret for `Authorization: Bearer`. |
| `OAUTH_JWKS_URL` | oauth mode | Your IdP's JWKS endpoint (e.g. `https://you.auth0.com/.well-known/jwks.json`). |
| `OAUTH_ISSUER` | oauth mode | Expected token `iss`. **Required** in oauth mode (validated). |
| `OAUTH_AUDIENCE` | oauth mode | Expected token `aud` (this server's identifier). **Required** in oauth mode (validated). |
| `OAUTH_ALLOWED_SUBJECTS` | oauth mode* | Comma/space-separated token `sub` values allowed to invoke tools. |
| `OAUTH_ALLOWED_EMAILS` | oauth mode* | Comma/space-separated emails allowed (matched case-insensitively against the email claim). |
| `OAUTH_EMAIL_CLAIM` | no | Claim name holding the email. Default `email`. |
| `OAUTH_REQUIRED_SCOPE` | no | Space-delimited scopes the token must carry. |
| `MCP_PUBLIC_URL` | oauth (prod) | Public HTTPS URL of this server; used in the RFC 9728 metadata + 401 challenge. |
| `MCP_HOST` / `MCP_PORT` | no | Bind address. Default `127.0.0.1:8000`. |
| `MCP_NAV_MENU_HANDLE` | no | Nav menu a sub-collection is placed under. Default `main-menu-2`. |
| `MCP_DATA_DIR` | no | Writable dir for backups + audit logs. Default `<repo>/data`. |
| `MCP_STATE_DIR` | prod | **Persistent** writable dir for the canonical reference the server reads + re-exports. Default `<MCP_DATA_DIR>/onboarding-mcp-state`. **Must be on a persistent volume** (see Persistence). |

\* In oauth mode the server **refuses to start** unless at least one of `OAUTH_ALLOWED_SUBJECTS` / `OAUTH_ALLOWED_EMAILS` is set — a valid IdP token alone is never sufficient.

The Shopify token's existing scope gaps (no `write_publications` / `write_inventory` /
`write_files` / metaobjects) are a useful natural blast-radius limit.

---

## Run locally

```bash
# from the repo root
python3.12 -m venv bbi_onboarding_mcp/.venv
bbi_onboarding_mcp/.venv/bin/pip install -r bbi_onboarding_mcp/requirements.txt

# bearer mode (local / programmatic clients)
MCP_AUTH_MODE=bearer MCP_AUTH_SECRET="$(openssl rand -hex 32)" \
  bbi_onboarding_mcp/.venv/bin/python -m bbi_onboarding_mcp.server
# serves streamable-HTTP at http://127.0.0.1:8000/mcp
```

Requires Python ≥ 3.10 (MCP SDK constraint); built/tested on 3.12.

## Test harness

Three tiers, none ever publish:

```bash
# offline — pure guard/resolver/image-parser logic, no network
bbi_onboarding_mcp/.venv/bin/python -m bbi_onboarding_mcp.test_harness

# + live READS and DRY-RUN writes (reports intended writes, executes none)
bbi_onboarding_mcp/.venv/bin/python -m bbi_onboarding_mcp.test_harness --net

# + actually create ONE draft product (status=draft, never published), then verify it
bbi_onboarding_mcp/.venv/bin/python -m bbi_onboarding_mcp.test_harness --live-draft OTG-MCPTEST-1
```

`--live-draft` leaves the draft in admin for review. Per BBI rules nothing is ever
deleted — unpublish/archive the test draft when done.

Every tool also accepts `dry_run=true` to report intended writes without executing them.

---

## Deploy (any always-on HTTPS host)

The server is host-agnostic streamable-HTTP. Any platform that serves a public HTTPS
endpoint, can hold env secrets, and supports persistent HTTP works (small VPS,
Fly.io, Render, Railway, a container on Cloud Run, etc.).

Host **Python ≥ 3.10** is required (MCP SDK floor; built/tested on 3.12).

1. Ship the repo (or just the `bbi_onboarding_mcp/` package — it bundles its own
   `reference_data/` copy of the canonical references, so it is self-contained).
2. `pip install -r bbi_onboarding_mcp/requirements.txt`.
3. Set env (all required vars):
   - `SHOPIFY_TOKEN`, `SHOPIFY_STORE`
   - `MCP_AUTH_MODE=oauth`
   - `OAUTH_JWKS_URL`, `OAUTH_ISSUER`, `OAUTH_AUDIENCE`
   - `OAUTH_ALLOWED_SUBJECTS` and/or `OAUTH_ALLOWED_EMAILS` (Steve's `sub` / email)
   - `MCP_PUBLIC_URL=https://<your-host>`
   - `MCP_HOST=0.0.0.0`, `MCP_PORT=$PORT`
   - `MCP_DATA_DIR=/var/lib/bbi-mcp` (writable)
   - `MCP_STATE_DIR=/var/lib/bbi-mcp/state` (**persistent volume** — see Persistence)
4. Run behind TLS: `python -m bbi_onboarding_mcp.server` (or
   `uvicorn "bbi_onboarding_mcp.server:build_app" --factory --host 0.0.0.0 --port $PORT`).
5. Front it with HTTPS (the platform's TLS, or a reverse proxy). The MCP endpoint is
   `https://<your-host>/mcp`; the OAuth metadata is at
   `https://<your-host>/.well-known/oauth-protected-resource`.

### Persistence (important)
`create_collection` registers the new route and **re-exports the canonical snapshot**
that `resolve_sku` / `onboard_product` then read. That snapshot lives in `MCP_STATE_DIR`,
which is **seeded once** from the bundled read-only `reference_data/` and thereafter
read **and** written there. If `MCP_STATE_DIR` is not on a persistent volume, a restart
or redeploy reverts to the bundle and **loses every collection registered since deploy**.
Mount it on persistent storage. To re-baseline from a fresh repo snapshot, delete the
state dir (or copy a newer `brand-onboarding-reference-*.json` into it).

### Production OAuth setup (one-time)
1. Create an app/API in your IdP (Auth0/Okta/etc.). Audience = your `OAUTH_AUDIENCE`.
2. **Set the server allowlist** to Steve's principal: `OAUTH_ALLOWED_EMAILS=steve@…`
   (or `OAUTH_ALLOWED_SUBJECTS=<his sub>`). This is the enforced "lock to one user".
3. Optionally also restrict the IdP connection to Steve's single account (defence in depth).
4. Enable Dynamic Client Registration on the IdP (Claude prefers DCR), or pre-register
   a client and hand Steve the Client ID/Secret for the dialog's *Advanced settings*.
5. Set `OAUTH_JWKS_URL`, `OAUTH_ISSUER`, `OAUTH_AUDIENCE` on the server. The server
   refuses to start if any of these — or the allowlist — is missing.

---

## Add the connector in Steve's Claude (exact steps)

1. In Claude: **Settings → Connectors → Add custom connector**.
2. **URL:** `https://<your-host>/mcp`
3. **Authenticate:** Claude detects the OAuth challenge, opens your IdP's login, Steve
   signs in with his authorized account, and approves. (If you pre-registered a client
   instead of using DCR, expand **Advanced settings** and paste the **Client ID** /
   **Client Secret** first.)
4. Claude lists the four tools. Steve is connected — no Shopify token ever touches his device.

> If you run `MCP_AUTH_MODE=bearer`, the consumer "Add custom connector" dialog
> **cannot** attach the bearer token (no field for it). Bearer mode is for local
> testing and for programmatic MCP clients (e.g. Claude Code's `.mcp.json` with an
> `Authorization` header). For Steve's consumer-app connector, use `oauth`.

---

## What stays manual (honest)
- **Draft → live publish** (`write_publications` not held): Steve reviews in admin and
  clicks Publish. This is the review gate, by design.
- **Sales-channel exclusion** for quote-only items: flagged as a manual admin step.
- **Un-hosted local photos**: images attach by URL only (`write_files` not held). A
  photo that exists only on Steve's machine is added in admin after, or in a v2 with a
  `write_files` staged-upload helper.

## Audit log
Every write (and dry-run intent) is appended to `MCP_DATA_DIR/logs/mcp-onboarding-<date>.jsonl`.
Secrets are redacted; the Shopify token and auth secret are never logged.
