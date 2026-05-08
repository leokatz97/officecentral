# Stage 5 Launch Audit — 4.5 PDP Delta
**Date:** 2026-05-08
**Auditor:** Claude Code (read-only pass)

---

## Status

**BLOCKED: T5 reference not locked — see audit category 4.4**

`ds-pdp-base.liquid` does not exist. The current PDP renderer is `theme/sections/main-product.liquid` (Starlite stock section, 1003 lines). A pixel-diff between the current state and a locked T5 design target cannot be computed because:

1. There is no `ds-pdp-base.liquid` section to diff against
2. The T5 Claude Design export (`data/design-photos/screens-t5-2026-05-04/`) contains design mockups, not live-page screenshots

---

## What Stage 4b will produce (documented gap for planning)

Stage 4b will build `ds-pdp-base.liquid` from scratch. Per `stage-4a-decision.md` and `stage-4a-current-pdp-audit.md`, the gap between current (`main-product.liquid`) and target (T5 spec) is total:

| T5 Element | Current state | Gap |
|---|---|---|
| BBI nav | Starlite (gate suppresses it — but no BBI nav rendered instead) | Full build |
| BBI footer | Same | Full build |
| 5-level breadcrumb | None | New snippet |
| 4:5 gallery + 6-image strip | Starlite generic | Full rebuild |
| Trust badge row (OECM · Canadian · Sold-out) | None | New |
| Unbuyable RFQ CTA | Starlite Add-to-Cart unconditional | BBI Rule #2 compliance |
| Spec table | None | New (metafields) |
| Variant swatch picker | Text labels only | Visual swatch rebuild |
| OECM bar | None | `render 'bbi-oecm-bar'` |
| Related products (tag-based, max 4) | App-dependent, no tag fallback | New |
| Brand block | None | New |
| CTA closer (charcoal canvas) | None | New |
| Product JSON-LD | None | PDP-2 task |
| BreadcrumbList JSON-LD | None | AI-6 shared snippet |

This is a **greenfield build** — nothing from `main-product.liquid` carries over.

---

## What the diff will measure once T5 is built

After Stage 4b lands and Steve approves a rendered screenshot of a Hero-100 PDP on the dev theme:

1. Lock the screenshot as T5 reference: `python3 scripts/capture-bbi-baselines.py --url http://127.0.0.1:9292/products/ashton-high-back-tilter --lock`
2. After any subsequent change: re-capture and run `python3 scripts/diff-bbi-baselines.py`
3. PASS = ≤5% pixel delta vs locked T5 reference

---

## Pre-Stage-4b checklist (for when Stage 4b starts)

- [ ] Re-run spec push on 93 matched handles (from `data/specs/`)
- [ ] Verify `bbi_landing` gate includes `template == 'product'` (confirmed ✓ in `stage-4a-decision.md` §1)
- [ ] Build `theme/sections/ds-pdp-base.liquid`
- [ ] Build `theme/templates/product.json`
- [ ] Build `theme/snippets/bbi-crumbs.liquid`
- [ ] Build `theme/snippets/bbi-product-jsonld.liquid`
- [ ] Build `theme/snippets/bbi-breadcrumb-jsonld.liquid`
- [ ] Smoke test 5 product states (PDP-3)
- [ ] Steve visual QA sign-off on rendered PDP
- [ ] Lock T5 screenshot baseline

**This audit will be re-run after Stage 4b is complete.**
