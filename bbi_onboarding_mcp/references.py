"""Canonical brand reference loader + SKU prefix resolver.

Single source of truth = the server's copy of the repo reference files:
  - data/reference/sku-prefix-lookup.yaml
  - data/reference/manufacturer-defaults.yaml
  - data/reference/brand-collection-routing.yaml
  - data/exports/brand-onboarding-reference-<date>.json  (merged snapshot)

At runtime the MERGED SNAPSHOT is authoritative for reads (it already resolves
each brand's target collections to live SMART/MANUAL membership + smart rules +
default Google category + manufacturer defaults). The three YAMLs are loaded so
`create_collection` can register a new route and re-export an updated snapshot
that the intake skill bundles.

SKU prefix match: leading alpha run of the SKU, greedy longest-known-prefix
match — mirrors the method recorded in the snapshot meta.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from . import config


@dataclass
class BrandResolution:
    status: str  # "resolved" | "needs-leo"
    reason: str = ""
    brand_key: Optional[str] = None
    manufacturer: Optional[str] = None
    brand_tag: Optional[str] = None
    sub_brands: list = field(default_factory=list)
    matched_prefix: Optional[str] = None
    sku_prefixes: list = field(default_factory=list)
    routing_tag_template: list = field(default_factory=list)
    collections_by_type: dict = field(default_factory=dict)
    target_collections: list = field(default_factory=list)
    default_google_product_category: Optional[str] = None
    manufacturer_defaults: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


class ReferenceData:
    """Loads and indexes the canonical references. Construct once at startup."""

    def __init__(self) -> None:
        self.export_path: Optional[Path] = None
        self.brands: list[dict] = []
        self.meta: dict = {}
        self._by_key: dict[str, dict] = {}
        self._prefix_index: dict[str, list[str]] = {}  # prefix -> [brand_key,...]
        # raw YAML (for re-export on create_collection)
        self.sku_prefix_yaml: dict = {}
        self.manufacturer_defaults_yaml: dict = {}
        self.brand_routing_yaml: dict = {}
        self.load()

    # ── loading ──────────────────────────────────────────────────────────
    def _newest_export(self) -> Optional[Path]:
        candidates = sorted(config.EXPORT_DIR.glob(config.EXPORT_GLOB))
        return candidates[-1] if candidates else None

    def load(self) -> None:
        self.export_path = self._newest_export()
        if not self.export_path:
            raise config.ConfigError(
                f"No merged reference snapshot found in {config.EXPORT_DIR} "
                f"matching {config.EXPORT_GLOB!r}. Run the snapshot exporter first."
            )
        data = json.loads(self.export_path.read_text())
        self.meta = data.get("meta", {})
        self.brands = data.get("brands", [])
        self._by_key = {b["brand_key"]: b for b in self.brands}

        # Build prefix -> brand_key index (greedy longest match resolves later).
        self._prefix_index = {}
        for b in self.brands:
            for pfx in b.get("sku_prefixes", []) or []:
                self._prefix_index.setdefault(pfx.upper(), []).append(b["brand_key"])

        # Raw YAML sources (best-effort; absence is non-fatal for reads).
        self.sku_prefix_yaml = self._read_yaml(config.SKU_PREFIX_YAML)
        self.manufacturer_defaults_yaml = self._read_yaml(config.MANUFACTURER_DEFAULTS_YAML)
        self.brand_routing_yaml = self._read_yaml(config.BRAND_ROUTING_YAML)

    @staticmethod
    def _read_yaml(path: Path) -> dict:
        if not path.exists():
            return {}
        return yaml.safe_load(path.read_text()) or {}

    # ── resolution ───────────────────────────────────────────────────────
    @staticmethod
    def extract_prefix(sku: str) -> str:
        """Leading alpha run of the SKU (uppercased). '' if none."""
        if not sku:
            return ""
        m = re.match(r"^[A-Za-z]+", sku.strip())
        return m.group(0).upper() if m else ""

    def resolve_sku(self, sku: str) -> BrandResolution:
        sku = (sku or "").strip()
        alpha = self.extract_prefix(sku)
        if not alpha:
            return BrandResolution(
                status="needs-leo",
                reason=f"SKU {sku!r} has no leading alpha prefix to resolve a brand from.",
            )

        # Greedy longest-known-prefix match: try the full alpha run, then shrink.
        matched = None
        for end in range(len(alpha), 0, -1):
            cand = alpha[:end]
            if cand in self._prefix_index:
                matched = cand
                break
        if not matched:
            return BrandResolution(
                status="needs-leo",
                reason=f"Unknown SKU prefix {alpha!r} (sku={sku!r}); not in the canonical lookup.",
                matched_prefix=alpha,
            )

        brand_keys = self._prefix_index[matched]
        if len(set(brand_keys)) > 1:
            return BrandResolution(
                status="needs-leo",
                reason=(
                    f"Ambiguous prefix {matched!r} maps to multiple brands: "
                    f"{sorted(set(brand_keys))}. Confirm with Leo."
                ),
                matched_prefix=matched,
            )

        b = self._by_key[brand_keys[0]]
        return BrandResolution(
            status="resolved",
            brand_key=b["brand_key"],
            manufacturer=b.get("canonical_manufacturer"),
            brand_tag=b.get("brand_tag"),
            sub_brands=b.get("sub_brands", []) or [],
            matched_prefix=matched,
            sku_prefixes=b.get("sku_prefixes", []) or [],
            routing_tag_template=b.get("routing_tag_template", []) or [],
            collections_by_type=b.get("collections_by_type", {}) or {},
            target_collections=b.get("target_collections", []) or [],
            default_google_product_category=b.get("default_google_product_category"),
            manufacturer_defaults=b.get("manufacturer_defaults", {}) or {},
        )

    def brand_by_key(self, brand_key: str) -> Optional[dict]:
        return self._by_key.get(brand_key)

    # ── REGISTER + RE-EXPORT (create_collection) ──────────────────────────
    def register_route_and_reexport(self, *, collection_meta: dict,
                                    auto_route_brands: list[str],
                                    date_stamp: str, dry_run: bool) -> dict:
        """Register a newly-created collection in the canonical routing reference
        and re-export the merged snapshot the intake skill bundles.

        Patches the in-memory snapshot's `target_collections` for each
        auto_route_brand and writes a NEW dated export file. Does NOT re-crawl
        live Shopify membership for all brands (that's the snapshot exporter's
        job); it carries forward existing data + the new route so the skill's
        read side stays current. Returns a summary of what changed."""
        handle = collection_meta["handle"]
        target_entry = {
            "handle": handle,
            "membership": "SMART" if collection_meta["type"] == "smart" else "MANUAL",
            "collection_id": collection_meta.get("collection_id"),
            "title": collection_meta.get("title"),
        }
        if collection_meta.get("smart_rules"):
            target_entry["smart_rules"] = collection_meta["smart_rules"]

        touched = []
        for bk in auto_route_brands or []:
            b = self._by_key.get(bk)
            if not b:
                continue
            existing = [tc.get("handle") for tc in b.get("target_collections", [])]
            if handle not in existing:
                b.setdefault("target_collections", []).append(target_entry)
                touched.append(bk)

        new_export = config.EXPORT_DIR / f"brand-onboarding-reference-{date_stamp}.json"
        snapshot = {"meta": {**self.meta,
                             "generated": date_stamp,
                             "amended_by": "bbi-onboarding-mcp create_collection",
                             "amendment": f"registered collection '{handle}' "
                                          f"for brands {touched}"},
                    "brands": self.brands}
        result = {"routed_brands": touched, "export_path": str(new_export)}
        if dry_run:
            result["dry_run"] = True
            return result
        new_export.write_text(json.dumps(snapshot, indent=2))
        self.export_path = new_export
        return result
