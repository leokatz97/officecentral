"""BBI Onboarding MCP server — streamable-HTTP transport, host-agnostic.

Run:
  MCP_AUTH_MODE=bearer MCP_AUTH_SECRET=... python -m mcp.onboarding.server

The four tools are the entire surface a connected client can touch. Guards run
inside tools.py. Auth runs in auth.py (pure-ASGI middleware) so it works for
both Claude's OAuth connector flow and programmatic bearer clients.
"""
from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from . import config, tools
from .auth import AuthMiddleware

mcp = FastMCP(
    "BBI Onboarding",
    instructions=(
        "Onboard products and collections to the Brant Business Interiors Shopify "
        "store. All products are created as DRAFTS for human review before publish. "
        "Brand/vendor, specs, images, and collection routing are validated and "
        "enforced server-side. Always resolve_sku first to confirm the brand with "
        "Steve before onboard_product. The server never publishes and never exposes "
        "the Shopify token."
    ),
    host=config.HOST,
    port=config.PORT,
    stateless_http=True,
)


def _live_blocked(dry_run: bool) -> Optional[dict]:
    """In AUTH_MODE=none, refuse live writes (dry-run only)."""
    if config.AUTH_MODE == "none" and not dry_run:
        return {"status": "rejected",
                "reason": "AUTH_MODE=none is dry-run only; live writes are disabled. "
                          "Set MCP_AUTH_MODE=bearer or oauth to enable writes."}
    return None


@mcp.tool()
def resolve_sku(sku: str) -> dict:
    """Resolve a SKU to its brand, routing collections (smart/manual + required
    tags), and default Google product category. Returns status 'needs-leo' for an
    unknown or ambiguous prefix. READ-only; call this before onboard_product."""
    return tools.resolve_sku(sku)


@mcp.tool()
def onboard_product(
    sku: str,
    title: str,
    description: str = "",
    seo_title: str = "",
    seo_description: str = "",
    price: Optional[str] = None,
    quote_only: bool = False,
    product_type: str = "",
    vendor: Optional[str] = None,
    specs: Optional[list] = None,
    feed: Optional[dict] = None,
    images: Optional[list] = None,
    collections: Optional[list] = None,
    extra_tags: Optional[list] = None,
    made_in_canada: Optional[dict] = None,
    warranty: Optional[dict] = None,
    dry_run: bool = False,
) -> dict:
    """Create a fully-enriched DRAFT product (never publishes). Server-enforced:
    brand re-resolved from SKU prefix (prefix wins, conflicts rejected); vendor =
    manufacturer (BBI vendor rejected); duplicate SKU short-circuits to the
    existing product; specs written only with a source_url; images attached by
    URL with a >=500px check; smart collections satisfied by tags read from the
    live rule, manual via Collect, missing reported not created; made_in_canada/
    warranty only if confirmed_by_steve; backup + exact-match readback. Returns a
    structured verification report. Use dry_run=true to preview writes."""
    blocked = _live_blocked(dry_run)
    if blocked:
        return blocked
    return tools.onboard_product(
        sku=sku, title=title, description=description, seo_title=seo_title,
        seo_description=seo_description, price=price, quote_only=quote_only,
        product_type=product_type, vendor=vendor, specs=specs, feed=feed,
        images=images, collections=collections, extra_tags=extra_tags,
        made_in_canada=made_in_canada, warranty=warranty, dry_run=dry_run)


@mcp.tool()
def create_collection(
    name: str,
    type: str = "smart",
    rule: Optional[list] = None,
    disjunctive: bool = False,
    products: Optional[list] = None,
    sub_collection: bool = False,
    parent_collection: Optional[str] = None,
    seo_title: str = "",
    seo_description: str = "",
    image: Optional[dict] = None,
    auto_route_brands: Optional[list] = None,
    dry_run: bool = False,
) -> dict:
    """Create a smart or manual collection. Duplicate handle/name short-circuits.
    A sub_collection is placed under parent_collection in the online-store nav and
    is REJECTED if the parent is missing. Sets SEO + image, registers the route in
    the canonical reference and re-exports the snapshot the intake skill bundles.
    Online Store channel publish is returned as a manual step (write_publications
    not held). Use dry_run=true to preview."""
    blocked = _live_blocked(dry_run)
    if blocked:
        return blocked
    return tools.create_collection(
        name=name, type=type, rule=rule, disjunctive=disjunctive, products=products,
        sub_collection=sub_collection, parent_collection=parent_collection,
        seo_title=seo_title, seo_description=seo_description, image=image,
        auto_route_brands=auto_route_brands, dry_run=dry_run)


@mcp.tool()
def verify_product(handle: Optional[str] = None, id: Optional[str] = None) -> dict:
    """Return a product's current state + born-feed-ready verdict for pre-publish
    review. READ-only. Supply either handle or id."""
    return tools.verify_product(handle=handle, id=id)


def build_app():
    """ASGI app: FastMCP streamable-HTTP wrapped in the auth gate."""
    return AuthMiddleware(mcp.streamable_http_app())


def main():
    import uvicorn
    mode = config.AUTH_MODE
    print(f"BBI Onboarding MCP — auth={mode} store={config.SHOPIFY_STORE} "
          f"api_default={config.DEFAULT_API}")
    if mode == "bearer" and not config.MCP_AUTH_SECRET:
        raise config.ConfigError("MCP_AUTH_MODE=bearer requires MCP_AUTH_SECRET")
    if mode == "oauth":
        missing = [n for n, v in (("OAUTH_JWKS_URL", config.OAUTH_JWKS_URL),
                                  ("OAUTH_ISSUER", config.OAUTH_ISSUER),
                                  ("OAUTH_AUDIENCE", config.OAUTH_AUDIENCE)) if not v]
        if missing:
            raise config.ConfigError(f"MCP_AUTH_MODE=oauth requires: {', '.join(missing)}")
        if not config.OAUTH_ALLOWED_SUBJECTS and not config.OAUTH_ALLOWED_EMAILS:
            raise config.ConfigError(
                "MCP_AUTH_MODE=oauth requires a subject allowlist — set OAUTH_ALLOWED_SUBJECTS "
                "and/or OAUTH_ALLOWED_EMAILS. Refusing to start an authenticated-but-anyone "
                "write endpoint.")
        allow_n = len(config.OAUTH_ALLOWED_SUBJECTS) + len(config.OAUTH_ALLOWED_EMAILS)
        print(f"  authorization: {allow_n} principal(s) on the allowlist")
    uvicorn.run(build_app(), host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
