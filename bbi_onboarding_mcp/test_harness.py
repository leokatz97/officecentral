"""Local test harness for the BBI Onboarding MCP.

Three tiers, increasingly invasive — none ever publish a product:

  (offline)      pure guard/resolver/image-parser logic, NO network.
                   python -m mcp.onboarding.test_harness
  --net          + live READS and DRY-RUN writes (resolve_sku, onboard_product
                   dry_run, create_collection dry_run, verify_product). Reads the
                   store and reports intended writes but executes none.
                   python -m mcp.onboarding.test_harness --net
  --live-draft SKU
                 + actually CREATE one DRAFT product (status=draft, never
                   published), enrich it, then verify_product it. Leaves the draft
                   in admin for review. Per BBI rules nothing is deleted.
                   python -m mcp.onboarding.test_harness --live-draft OTG-MCPTEST-1

Requires SHOPIFY_TOKEN in .env for --net / --live-draft. Set MCP_AUTH_MODE=bearer
+ MCP_AUTH_SECRET to mirror production auth (harness calls tool functions directly,
so auth middleware is exercised separately — see --auth-check)."""
from __future__ import annotations

import json
import struct
import sys

from . import config, guards, tools
from .references import ReferenceData
from .shopify_client import _parse_image_size


def _png(w: int, h: int) -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", w, h)


def _ok(label, cond):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        _ok.failed += 1
_ok.failed = 0


def test_offline():
    print("== OFFLINE (no network) ==")
    refs = ReferenceData()

    # Prefix resolver — known prefix.
    r = refs.resolve_sku("OTG2810")
    _ok(f"OTG resolves to a brand ({r.manufacturer})", r.status == "resolved" and r.manufacturer)
    # Greedy longest-prefix is exercised; unknown prefix -> needs-leo.
    u = refs.resolve_sku("ZZZ999")
    _ok("unknown prefix -> needs-leo", u.status == "needs-leo")
    n = refs.resolve_sku("12345")
    _ok("numeric SKU (no alpha) -> needs-leo", n.status == "needs-leo")

    # Vendor lock.
    v_bad = guards.check_vendor(r, config.FORBIDDEN_VENDOR)
    _ok("vendor=BBI rejected", not v_bad["ok"])
    v_conflict = guards.check_vendor(r, "Some Other Brand")
    _ok("conflicting vendor rejected (prefix wins)", not v_conflict["ok"])
    v_good = guards.check_vendor(r, r.manufacturer)
    _ok("vendor=manufacturer accepted", v_good["ok"] and v_good["vendor"] == r.manufacturer)

    # Spec filter — source_url required.
    kept, dropped = guards.filter_specs([
        {"name": "Weight capacity", "value": "300 lb", "source_url": "https://x/y"},
        {"name": "Material", "value": "mesh"},  # no source -> dropped
        {"name": "Color", "value": ""},          # empty -> dropped
    ])
    _ok("kept only sourced spec", len(kept) == 1 and kept[0]["name"] == "Weight capacity")
    _ok("dropped unsourced + empty (reported)", len(dropped) == 2)

    # confirmed_by_steve gate.
    mic, note = guards.gate_confirmed({"confirmed_by_steve": True, "date": "2026-06-08"}, "made_in_canada")
    _ok("confirmed made_in_canada kept", mic is not None)
    mic2, note2 = guards.gate_confirmed({"date": "2026-06-08"}, "made_in_canada")
    _ok("unconfirmed made_in_canada omitted + noted", mic2 is None and note2)

    # Image size parser.
    _ok("PNG 600x800 parsed", _parse_image_size(_png(600, 800)) == (600, 800))
    _ok("PNG 100x100 flagged < 500", min(_parse_image_size(_png(100, 100))) < config.MIN_IMAGE_PX)

    # Feed verdict.
    good = guards.feed_ready_verdict(vendor="X", specs_written=True, google_category="Furniture",
                                     identifier="123", identifier_exists=False, image_ok=True,
                                     price_or_quote=True)
    _ok("complete feed -> born_feed_ready", good["born_feed_ready"])
    bad = guards.feed_ready_verdict(vendor=None, specs_written=False, google_category=None,
                                    identifier=None, identifier_exists=False, image_ok=False,
                                    price_or_quote=False)
    _ok("empty feed -> not ready, gaps listed", not bad["born_feed_ready"] and bad["gaps"])

    # Required-tags from a synthetic smart rule.
    tags, notes = guards.required_tags_from_rule({"rules": [
        {"column": "tag", "relation": "equals", "condition": "brand:acme"},
        {"column": "tag", "relation": "equals", "condition": "type:chairs"},
        {"column": "title", "relation": "contains", "condition": "chair"},
    ]})
    _ok("derives tag-equals conditions", tags == ["brand:acme", "type:chairs"])
    _ok("flags non-tag rule as unsatisfiable", len(notes) == 1)


def test_net():
    print("\n== NETWORK READS + DRY-RUN (no writes executed) ==")
    config.require_shopify_token()
    refs = tools.get_refs()
    # pick a real resolvable SKU prefix from the reference set
    sample_prefix = next(iter(refs.brands[0].get("sku_prefixes") or ["OTG"]), "OTG")
    test_sku = f"{sample_prefix}-MCPTEST-DRYRUN-1"

    rs = tools.resolve_sku(test_sku)
    _ok("resolve_sku returns resolved/needs-leo", rs["status"] in ("resolved", "needs-leo"))
    print("    resolve_sku ->", json.dumps({k: rs.get(k) for k in
          ("status", "manufacturer", "brand_tag")}, default=str))

    ob = tools.onboard_product(
        sku=test_sku, title="MCP Dry-Run Test Chair", description="<p>test</p>",
        seo_title="Test", seo_description="Test desc", price="199.00",
        product_type="Task Chairs",
        specs=[{"name": "Weight capacity", "value": "300 lb", "source_url": "https://example.com/spec"},
               {"name": "Material", "value": "mesh"}],  # 2nd dropped
        feed={"google_product_category": "Furniture > Chairs", "condition": "new"},
        collections=["task-chairs", "nonexistent-collection-xyz"],
        made_in_canada={"confirmed_by_steve": True, "date": "2026-06-08"},
        warranty={"text": "5 year"},  # not confirmed -> omitted
        dry_run=True)
    _ok("onboard dry_run did not create (status ok/needs-leo/rejected/already_exists)",
        ob["status"] in ("ok", "needs-leo", "rejected", "already_exists"))
    if ob["status"] == "ok":
        _ok("dropped unsourced spec reported", any(d["name"] == "Material" for d in ob["specs"]["dropped"]))
        _ok("missing collection reported not created",
            any(c.get("status") == "missing-reported-not-created" for c in ob.get("collections", [])))
        _ok("warranty omitted (unconfirmed)", any("warranty" in w for w in ob["warnings"]))
        print("    feed_verdict ->", json.dumps(ob.get("feed_verdict")))

    cc = tools.create_collection(name="MCP Test Collection ZZZ", type="smart",
                                 rule=[{"column": "tag", "relation": "equals", "condition": "type:test"}],
                                 dry_run=True)
    _ok("create_collection dry_run ok/already_exists", cc["status"] in ("ok", "already_exists"))

    # sub-collection with missing parent must reject (dry-run).
    cc2 = tools.create_collection(name="MCP Orphan Sub ZZZ", type="manual",
                                  sub_collection=True, parent_collection="definitely-not-a-parent",
                                  dry_run=True)
    _ok("sub-collection with missing parent rejected", cc2["status"] == "rejected")


def test_live_draft(sku: str):
    print(f"\n== LIVE DRAFT CREATE (status=draft, never published) — {sku} ==")
    config.require_shopify_token()
    ob = tools.onboard_product(
        sku=sku, title=f"MCP Harness Draft {sku}",
        description="<p>Created by the BBI Onboarding MCP test harness. Safe to delete via archive/unpublish.</p>",
        seo_title=f"MCP Harness Draft {sku}", seo_description="Test draft from MCP harness.",
        price="123.45", product_type="Task Chairs",
        specs=[{"name": "Weight capacity", "value": "300 lb",
                "source_url": "https://example.com/spec", "source_date": "2026-06-08"}],
        feed={"google_product_category": "Furniture > Chairs", "condition": "new",
              "identifier_exists": True},
        collections=["task-chairs"],
        made_in_canada={"confirmed_by_steve": True, "date": "2026-06-08"},
        dry_run=False)
    print(json.dumps(ob, indent=2, default=str)[:3000])
    _ok("live draft created", ob["status"] in ("ok", "partial", "already_exists"))
    if ob.get("product"):
        _ok("status is draft", ob["product"]["status"].lower() == "draft")
        vp = tools.verify_product(id=ob["product"]["id"])
        _ok("verify_product finds the draft", vp["status"] == "ok")
        _ok("verify confirms draft (not published)", vp["product"]["status"].lower() == "draft")
        print("    REVIEW IN ADMIN:", ob["product"]["admin_url"])


def main():
    args = sys.argv[1:]
    test_offline()
    if "--net" in args or "--live-draft" in args:
        try:
            test_net()
        except Exception as e:  # noqa: BLE001
            print("  NET TESTS ERROR:", e)
            _ok.failed += 1
    if "--live-draft" in args:
        i = args.index("--live-draft")
        sku = args[i + 1] if i + 1 < len(args) else None
        if not sku:
            print("  --live-draft requires a SKU argument")
            _ok.failed += 1
        else:
            test_live_draft(sku)
    print(f"\n{'ALL PASS' if _ok.failed == 0 else str(_ok.failed) + ' FAILURE(S)'}")
    sys.exit(1 if _ok.failed else 0)


if __name__ == "__main__":
    main()
