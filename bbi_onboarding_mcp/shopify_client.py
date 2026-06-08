"""Consolidated Shopify Admin API client for the BBI Onboarding MCP.

The write-path bodies here are LIFTED (wrapped, not rewritten) from the proven
push-* scripts so the MCP exercises code that already works against this store:

  create_product        <- scripts/consolidate-shipping.py   create_product()  [REST 2026-04]
  update_product/specs  <- scripts/push-b4s1-enrichment.py   productUpdate / metafieldsSet [GQL 2024-10]
  attach_image_by_url   <- scripts/push-generated-images.py  push_image()      [REST 2026-04]
  add_collect           <- scripts/push-b4s1-enrichment.py   /collects.json    [REST 2024-10]
  backup + readback     <- scripts/push-b4s1-enrichment.py   backup + readback-verify [GQL 2024-10]

Re-authored on the CURRENT default version (not the legacy 2024-01 endpoint):
  get_smart_collection_rule, duplicate checks, collection create, nav write.

Every write is gated by `dry_run`; in dry-run nothing is sent and the intended
payload is recorded. Exact-match readback runs after every live write.
"""
from __future__ import annotations

import html as _html
import io
import json
import re as _re
import struct
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import config


class ShopifyError(RuntimeError):
    pass


class ShopifyClient:
    def __init__(self, *, dry_run: bool = False, audit=None):
        self.token = config.require_shopify_token()
        self.store = config.SHOPIFY_STORE
        self.dry_run = dry_run
        self.audit = audit
        self.planned_writes: list[dict] = []
        self._hdr = {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json",
        }

    # ── URLs ────────────────────────────────────────────────────────────
    def _rest_base(self, version: str) -> str:
        return f"https://{self.store}/admin/api/{version}"

    def _gql_url(self, version: str) -> str:
        return f"https://{self.store}/admin/api/{version}/graphql.json"

    # ── low-level transport (429 backoff, lifted pattern) ────────────────
    def _urlopen_retry(self, req, *, timeout: int = 30):
        last = None
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    body = r.read().decode()
                    return r.status, (json.loads(body) if body else None)
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 5:
                    time.sleep(2 * (attempt + 1))
                    continue
                detail = e.read().decode()[:500]
                raise ShopifyError(f"HTTP {e.code} {req.get_method()} {req.full_url}: {detail}")
            except urllib.error.URLError as e:  # transient network
                last = e
                time.sleep((attempt + 1) * 3)
        raise ShopifyError(f"network failure after retries: {last}")

    def rest(self, method: str, path: str, body=None, version: Optional[str] = None):
        version = version or config.DEFAULT_API
        data = json.dumps(body).encode() if body is not None else None
        url = f"{self._rest_base(version)}{path}"
        req = urllib.request.Request(url, data=data, headers=self._hdr, method=method)
        _, payload = self._urlopen_retry(req)
        return payload

    def gql(self, query: str, variables: Optional[dict] = None, version: Optional[str] = None):
        version = version or config.WRITE_GQL_API
        data = json.dumps({"query": query, "variables": variables or {}}).encode()
        req = urllib.request.Request(self._gql_url(version), data=data, headers=self._hdr)
        _, out = self._urlopen_retry(req)
        if out is None:
            raise ShopifyError("empty GraphQL response")
        if "errors" in out:
            raise ShopifyError(f"GraphQL errors: {out['errors']}")
        return out["data"]

    def _log_write(self, action: str, detail: dict) -> None:
        if self.audit:
            self.audit.write(action, detail, dry_run=self.dry_run)

    # ── DUPLICATE CHECKS (build directive #1) ────────────────────────────
    def find_product_by_sku(self, sku: str) -> Optional[dict]:
        """Exact-SKU lookup. Returns {id, gid, handle, title, status, admin_url}
        for the first product carrying a variant with this SKU, else None."""
        if not sku:
            return None
        q = """
        query($q: String!) {
          products(first: 10, query: $q) {
            edges { node {
              id legacyResourceId handle title status
              variants(first: 50) { edges { node { sku } } }
            } }
          }
        }"""
        # Shopify search: sku:'ABC123' (quote to keep it exact-ish; we re-check below)
        data = self.gql(q, {"q": f"sku:{json.dumps(sku)}"}, version=config.WRITE_GQL_API)
        want = sku.strip().lower()
        for edge in data["products"]["edges"]:
            n = edge["node"]
            skus = [ (v["node"]["sku"] or "").strip().lower()
                     for v in n["variants"]["edges"] ]
            if want in skus:
                lid = n["legacyResourceId"]
                return {
                    "id": lid,
                    "gid": n["id"],
                    "handle": n["handle"],
                    "title": n["title"],
                    "status": n["status"],
                    "admin_url": f"{config.ADMIN_BASE}/products/{lid}",
                }
        return None

    def find_collection(self, handle: Optional[str], title: Optional[str]) -> Optional[dict]:
        """Look for an existing smart OR custom collection by handle or title.
        Returns {id, gid, handle, title, type, admin_url} or None."""
        for kind, key in (("smart_collections", "smart_collections"),
                          ("custom_collections", "custom_collections")):
            if handle:
                payload = self.rest("GET", f"/{kind}.json?handle={urllib.parse.quote(handle)}",
                                    version=config.DEFAULT_API)
                hits = (payload or {}).get(key, [])
                if hits:
                    return self._collection_hit(hits[0], kind)
        # Title fallback (handles differ but a same-named collection exists).
        if title:
            for kind, key in (("smart_collections", "smart_collections"),
                              ("custom_collections", "custom_collections")):
                payload = self.rest("GET", f"/{kind}.json?title={urllib.parse.quote(title)}&limit=10",
                                    version=config.DEFAULT_API)
                for c in (payload or {}).get(key, []):
                    if (c.get("title") or "").strip().lower() == title.strip().lower():
                        return self._collection_hit(c, kind)
        return None

    @staticmethod
    def _collection_hit(c: dict, kind: str) -> dict:
        cid = c["id"]
        return {
            "id": cid,
            "gid": f"gid://shopify/Collection/{cid}",
            "handle": c.get("handle"),
            "title": c.get("title"),
            "type": "smart" if kind == "smart_collections" else "manual",
            "admin_url": f"{config.ADMIN_BASE}/collections/{cid}",
        }

    # ── READS ────────────────────────────────────────────────────────────
    def get_smart_collection_rule(self, handle: str) -> Optional[dict]:
        """Re-authored on DEFAULT_API (not legacy 2024-01). Returns the live
        smart collection incl. `rules` + `disjunctive`, or None."""
        payload = self.rest("GET",
                            f"/smart_collections.json?handle={urllib.parse.quote(handle)}",
                            version=config.DEFAULT_API)
        colls = (payload or {}).get("smart_collections", [])
        return colls[0] if colls else None

    def get_product_full(self, id_or_handle: str) -> Optional[dict]:
        """Fetch a product's current state by numeric id, GID, or handle."""
        if str(id_or_handle).startswith("gid://"):
            sel = f'product(id: "{id_or_handle}")'
        elif str(id_or_handle).isdigit():
            sel = f'product(id: "gid://shopify/Product/{id_or_handle}")'
        else:
            sel = f'productByHandle(handle: {json.dumps(id_or_handle)})'
        q = """{ %s {
            id legacyResourceId handle title status vendor productType tags
            descriptionHtml onlineStoreUrl
            seo { title description }
            featuredImage { url width height }
            images(first: 50) { edges { node { url width height altText } } }
            variants(first: 50) { edges { node { sku price } } }
            collections(first: 50) { edges { node { id handle title } } }
            metafields(first: 50, namespace: "specs") { edges { node { key value type } } }
            googleProductCategory: metafield(namespace: "mm-google-shopping", key: "google_product_category") { value }
        } }""" % sel
        data = self.gql(q, version=config.WRITE_GQL_API)
        node = data.get("product") or data.get("productByHandle")
        return node

    # ── BACKUP (lifted pattern) ──────────────────────────────────────────
    def backup_product(self, pid: str) -> Optional[str]:
        """Snapshot current product + metafields to data/backups/ before update."""
        current = self.rest("GET", f"/products/{pid}.json", version=config.WRITE_GQL_API)["product"]
        mf = self.rest("GET", f"/products/{pid}/metafields.json",
                       version=config.WRITE_GQL_API).get("metafields", [])
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        path = config.BACKUP_DIR / f"mcp-onboard-{pid}-pre-{ts}.json"
        if self.dry_run:
            return f"[dry-run] would back up product {pid} -> {path}"
        path.write_text(json.dumps({"fetched": ts, "product": current, "metafields": mf}, indent=2))
        return str(path)

    # ── WRITES (lifted) ──────────────────────────────────────────────────
    def create_product(self, *, title, body_html, vendor, product_type, tags,
                        variants, status="draft", handle=None) -> dict:
        """Lifted from consolidate-shipping.py create_product() (REST 2026-04).
        status forced by caller; this client never publishes."""
        product = {
            "title": title,
            "body_html": body_html,
            "vendor": vendor,
            "product_type": product_type,
            "tags": tags,
            "status": status,
            "variants": variants,
        }
        if handle:
            product["handle"] = handle
        self._log_write("create_product", {"title": title, "vendor": vendor,
                                            "status": status, "tags": tags})
        if self.dry_run:
            self.planned_writes.append({"op": "create_product", "product": product})
            return {"dry_run": True, "intended": product}
        payload = self.rest("POST", "/products.json", {"product": product},
                            version=config.PRODUCT_CREATE_API)
        return payload["product"]

    PRODUCT_UPDATE = """
    mutation($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title vendor productType tags descriptionHtml seo { title description } }
        userErrors { field message }
      }
    }"""

    METAFIELDS_SET = """
    mutation($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { namespace key value type }
        userErrors { field message }
      }
    }"""

    def update_product_fields(self, gid: str, fields: dict) -> dict:
        """productUpdate (GQL 2024-10), lifted from push-b4s1."""
        pinput = {"id": gid, **fields}
        self._log_write("update_product_fields", {"gid": gid, "fields": list(fields.keys())})
        if self.dry_run:
            self.planned_writes.append({"op": "productUpdate", "input": pinput})
            return {"dry_run": True, "intended": pinput}
        r = self.gql(self.PRODUCT_UPDATE, {"input": pinput}, version=config.WRITE_GQL_API)
        errs = r["productUpdate"]["userErrors"]
        if errs:
            raise ShopifyError(f"productUpdate userErrors: {errs}")
        return r["productUpdate"]["product"]

    def set_metafields(self, gid: str, metafields: list[dict]) -> dict:
        """metafieldsSet in chunks of 25 (GQL 2024-10), lifted from push-b4s1.
        Each entry: {namespace, key, type, value}."""
        inputs = [{"ownerId": gid, **m} for m in metafields]
        self._log_write("set_metafields", {"gid": gid, "count": len(inputs),
                                            "keys": [m["key"] for m in metafields]})
        if self.dry_run:
            self.planned_writes.append({"op": "metafieldsSet", "metafields": inputs})
            return {"dry_run": True, "intended": inputs}
        written = []
        for i in range(0, len(inputs), 25):
            r = self.gql(self.METAFIELDS_SET, {"metafields": inputs[i:i + 25]},
                         version=config.WRITE_GQL_API)
            errs = r["metafieldsSet"]["userErrors"]
            if errs:
                raise ShopifyError(f"metafieldsSet userErrors: {errs}")
            written.extend(r["metafieldsSet"]["metafields"])
        return {"written": written}

    def attach_image_by_url(self, pid: str, src: str, position: int, alt: str) -> dict:
        """Lifted from push-generated-images.py push_image() (REST 2026-04).
        Shopify fetches and stores the remote URL on its CDN."""
        image = {"src": src, "position": int(position), "alt": alt}
        self._log_write("attach_image", {"pid": pid, "src": src, "position": position})
        if self.dry_run:
            self.planned_writes.append({"op": "attach_image", "pid": pid, "image": image})
            return {"dry_run": True, "intended": image}
        payload = self.rest("POST", f"/products/{pid}/images.json", {"image": image},
                            version=config.IMAGE_API)
        return payload["image"]

    def add_collect(self, pid: str, collection_id: int) -> dict:
        """Lifted from push-b4s1 /collects.json (REST 2024-10). Manual collections."""
        self._log_write("add_collect", {"pid": pid, "collection_id": collection_id})
        if self.dry_run:
            self.planned_writes.append({"op": "collect", "pid": pid, "collection_id": collection_id})
            return {"dry_run": True, "intended": {"product_id": pid, "collection_id": collection_id}}
        return self.rest("POST", "/collects.json",
                         {"collect": {"product_id": int(pid), "collection_id": int(collection_id)}},
                         version=config.WRITE_GQL_API)

    # ── COLLECTION CREATE + NAV (re-authored on DEFAULT_API) ─────────────
    def create_smart_collection(self, *, title, handle, rules, disjunctive,
                                image=None) -> dict:
        # SEO is applied separately via set_collection_seo() after creation.
        body = {"title": title, "handle": handle, "rules": rules, "disjunctive": disjunctive}
        if image and image.get("url"):
            body["image"] = {"src": image["url"], "alt": image.get("alt", "")}
        self._log_write("create_smart_collection", {"handle": handle, "title": title})
        if self.dry_run:
            self.planned_writes.append({"op": "create_smart_collection", "collection": body})
            return {"dry_run": True, "intended": body}
        payload = self.rest("POST", "/smart_collections.json", {"smart_collection": body},
                            version=config.DEFAULT_API)
        return payload["smart_collection"]

    def create_custom_collection(self, *, title, handle, seo=None, image=None) -> dict:
        body = {"title": title, "handle": handle}
        if image and image.get("url"):
            body["image"] = {"src": image["url"], "alt": image.get("alt", "")}
        self._log_write("create_custom_collection", {"handle": handle, "title": title})
        if self.dry_run:
            self.planned_writes.append({"op": "create_custom_collection", "collection": body})
            return {"dry_run": True, "intended": body}
        payload = self.rest("POST", "/custom_collections.json", {"custom_collection": body},
                            version=config.DEFAULT_API)
        return payload["custom_collection"]

    def set_collection_seo(self, collection_gid: str, seo_title: str, seo_desc: str) -> dict:
        q = """
        mutation($input: CollectionInput!) {
          collectionUpdate(input: $input) {
            collection { id handle }
            userErrors { field message }
          }
        }"""
        cinput = {"id": collection_gid, "seo": {"title": seo_title, "description": seo_desc}}
        if self.dry_run:
            self.planned_writes.append({"op": "collectionSEO", "input": cinput})
            return {"dry_run": True, "intended": cinput}
        r = self.gql(q, {"input": cinput}, version=config.WRITE_GQL_API)
        errs = r["collectionUpdate"]["userErrors"]
        if errs:
            raise ShopifyError(f"collectionUpdate userErrors: {errs}")
        return r["collectionUpdate"]["collection"]

    # ── NAV MENU (lifted from update-main-menu.py menuUpdate) ────────────
    _MENU_QUERY = """
    { menus(first: 20) { edges { node { id handle title
        items { id title type url resourceId tags
          items { id title type url resourceId tags
            items { id title type url resourceId tags } } } } } } }"""

    _MENU_UPDATE = """
    mutation($id: ID!, $title: String!, $handle: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, handle: $handle, items: $items) {
        menu { id handle items { title items { title } } }
        userErrors { field message code }
      }
    }"""

    def get_menu(self, handle: str) -> Optional[dict]:
        data = self.gql(self._MENU_QUERY, version=config.WRITE_GQL_API)
        for edge in data["menus"]["edges"]:
            if edge["node"]["handle"] == handle:
                return edge["node"]
        return None

    @staticmethod
    def _item_to_input(item: dict) -> dict:
        out = {"title": item["title"], "type": item["type"]}
        if item.get("url"):
            out["url"] = item["url"]
        if item.get("resourceId"):
            out["resourceId"] = item["resourceId"]
        if item.get("tags"):
            out["tags"] = item["tags"]
        if item.get("items"):
            out["items"] = [ShopifyClient._item_to_input(c) for c in item["items"]]
        return out

    def place_in_nav(self, *, menu_handle, parent_title, child_title,
                     child_collection_gid) -> dict:
        """Append a child COLLECTION item under the parent menu item. Reject if
        the parent item is missing. Reads the menu, rebuilds the items tree,
        menuUpdate, returns a placement result."""
        menu = self.get_menu(menu_handle)
        if not menu:
            return {"ok": False, "error": f"nav menu '{menu_handle}' not found"}
        items = [self._item_to_input(i) for i in menu["items"]]
        parent = None
        for it in items:
            if it["title"].strip().lower() == parent_title.strip().lower():
                parent = it
                break
        if parent is None:
            return {"ok": False, "error": f"parent nav item '{parent_title}' not found in '{menu_handle}'"}
        parent.setdefault("items", [])
        if any(c["title"].strip().lower() == child_title.strip().lower() for c in parent["items"]):
            return {"ok": True, "note": "child already present in nav", "changed": False}
        parent["items"].append({"title": child_title, "type": "COLLECTION",
                                "resourceId": child_collection_gid})
        self._log_write("place_in_nav", {"menu": menu_handle, "parent": parent_title,
                                         "child": child_title})
        if self.dry_run:
            self.planned_writes.append({"op": "place_in_nav", "menu": menu_handle,
                                        "parent": parent_title, "child": child_title})
            return {"ok": True, "dry_run": True, "changed": True}
        r = self.gql(self._MENU_UPDATE, {"id": menu["id"], "title": menu["title"],
                                         "handle": menu["handle"], "items": items},
                     version=config.WRITE_GQL_API)
        errs = r["menuUpdate"]["userErrors"]
        if errs:
            raise ShopifyError(f"menuUpdate userErrors: {errs}")
        return {"ok": True, "changed": True, "menu": r["menuUpdate"]["menu"]}

    # ── READBACK (lifted normalization) ──────────────────────────────────
    @staticmethod
    def _norm_text(s):
        return _html.unescape(s or "").strip()

    @staticmethod
    def _norm_html(s):
        s = _html.unescape(s or "")
        s = _re.sub(r">\s+<", "><", s)
        return _re.sub(r"\s+", " ", s).strip()

    @staticmethod
    def _eq_list(a, b):
        try:
            return json.loads(a) == json.loads(b)
        except Exception:
            return (a or "") == (b or "")

    # ── IMAGE DIMENSION CHECK (no Pillow dep) ────────────────────────────
    @staticmethod
    def image_dimensions(url: str) -> Optional[tuple[int, int]]:
        """Best-effort (width, height) by reading image header bytes. Supports
        PNG, JPEG, GIF, BMP, WebP. Returns None if undeterminable."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bbi-onboarding-mcp"})
            with urllib.request.urlopen(req, timeout=20) as r:
                head = r.read(65536)
        except Exception:
            return None
        return _parse_image_size(head)


def _parse_image_size(data: bytes) -> Optional[tuple[int, int]]:
    if len(data) < 24:
        return None
    # PNG
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return int(w), int(h)
    # GIF
    if data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = struct.unpack("<HH", data[6:10])
        return int(w), int(h)
    # BMP
    if data[:2] == b"BM":
        w, h = struct.unpack("<ii", data[18:26])
        return int(w), abs(int(h))
    # WebP (VP8/VP8L/VP8X)
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        fmt = data[12:16]
        try:
            if fmt == b"VP8 ":
                w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
                h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
                return int(w), int(h)
            if fmt == b"VP8L":
                b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
                w = 1 + (((b1 & 0x3F) << 8) | b0)
                h = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
                return int(w), int(h)
            if fmt == b"VP8X":
                w = 1 + (data[24] | (data[25] << 8) | (data[26] << 16))
                h = 1 + (data[27] | (data[28] << 8) | (data[29] << 16))
                return int(w), int(h)
        except Exception:
            return None
    # JPEG
    if data[:2] == b"\xff\xd8":
        try:
            stream = io.BytesIO(data)
            stream.read(2)
            while True:
                b = stream.read(1)
                while b and b != b"\xff":
                    b = stream.read(1)
                marker = stream.read(1)
                if not marker:
                    return None
                m = marker[0]
                if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                         0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    stream.read(3)  # length(2) + precision(1)
                    h, w = struct.unpack(">HH", stream.read(4))
                    return int(w), int(h)
                seg_len = struct.unpack(">H", stream.read(2))[0]
                stream.seek(seg_len - 2, io.SEEK_CUR)
        except Exception:
            return None
    return None
