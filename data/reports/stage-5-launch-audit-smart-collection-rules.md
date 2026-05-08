# Stage 5 Launch Audit — 4.2 Smart Collection Rules
**Date:** 2026-05-08
**Source:** `data/reports/stage-4b-recover-smart-rules.md` + `stage-4b-recover-smart-rules-raw.json`
**Auditor:** Claude Code (read-only pass)

---

## Overview

Smart collections are the backbone of the BBI shop. Sub-collection pages use `template_suffix=base` to render `ds-cs-base.liquid` and pull products from smart collection rules.

This audit covers the 9 core category hub collections that power the BBI shop. Additional smart collections (room:*, type:* singles) are catalogued for reference.

---

## Core Category Hub Collections

| Handle | Product Count | Logic | Rule Summary | Status |
|---|---|---|---|---|
| `seating` | 194 | OR | `type:chairs`, `type:lounge`, `type:ergonomic-seating`, `type:bariatric-seating`, `type:stacking`, `type:seating` | ✓ Healthy |
| `desks` | 98 | OR | `type:desks`, `type:benching`, `type:workstations`, `type:sit-stand` | ✓ Healthy |
| `storage` | 82 | OR | `type:storage`, `type:filing`, `type:bookcases`, `type:cabinets`, `type:lateral-files` | ✓ Healthy |
| `tables` | 104 | OR | `type:tables`, `type:folding-tables`, `type:training-tables`, `type:cafeteria-tables` | ✓ Healthy |
| `boardroom` | 87 | OR | `room:boardroom`, `type:boardroom-tables`, `type:conference-tables` | ✓ Healthy |
| `ergonomic-products` | 16 | OR | title contains `monitor arm`, `keyboard tray`, `sit-stand`, `anti-fatigue` | ⚠️ Title-match fragile — see below |
| `panels-room-dividers` | 16 | OR | title contains `partition`, `room divider`, `modesty panel`, `otg panel`, `divider` | ⚠️ Title-match fragile — see below |
| `accessories` | 91 | OR | `type:accessories`, `type:desk-accessories`, `type:power-modules`, `type:chair-accessories` | ✓ Healthy |
| `quiet-spaces` | 9 | OR | title contains `acoustic`, `sound dampener`, `phone booth`, `soft pod` | ⚠️ Low count + title-match — see below |
| `business-furniture` | 624 | AND | NOT `industry:educational`, NOT `industry:daycare`, NOT `industry:healthcare` | ✓ Healthy |

---

## Issues Found

### ⚠️ ergonomic-products (16 products) — title-match rule, fragile
- Rules: `title contains 'monitor arm'`, `title contains 'keyboard tray'`, `title contains 'sit-stand'`, `title contains 'anti-fatigue'`
- **Risk:** New products added with different title phrasing will not auto-populate. A tag-based rule (`type:ergonomic`) would be more durable.
- **Severity:** FIX (not BLOCK) — collection is populated today; risk is for future additions.

### ⚠️ panels-room-dividers (16 products) — title-match rule, fragile
- Rules: title contains `partition`, `room divider`, `modesty panel`, `otg panel`, `divider`
- **Same fragility as ergonomic-products.** Tag-based rule preferred.
- **Severity:** FIX (not BLOCK)

### ⚠️ quiet-spaces (9 products) — low count + title-match
- Rules: title contains `acoustic`, `sound dampener`, `phone booth`, `soft pod`
- Only 9 products. Low coverage for an "Acoustic Pods" category that is flagged in SEO strategy as a hot item.
- **Severity:** FIX — add tag `type:quiet-spaces` to products and migrate to tag rule before launch.

### ✗ room-break-room (0 products) — EMPTY
- Rules: `tag equals 'room:break-room'`
- No products tagged with this room tag. Collection is empty.
- Not used by any BBI nav or page template — orphaned collection.
- **Severity:** NIT — does not affect any user-facing page; can be ignored until cleanup.

### ✗ bundle-builder-products (0 products) — EMPTY
- Rules: `type equals 'Custom Bundle'`
- No products. Appears to be an app artifact (Bundler app).
- Not referenced in any BBI template.
- **Severity:** NIT

---

## "View All" Smart Collections (SMART-1 — not yet built)

Per `bbi-build-state.md` row SMART-1, the following 10 "view all" smart collections are **not yet created:**

| Required handle | Rule (planned) |
|---|---|
| `all-seating` | `tag:type:chairs` or similar |
| `all-desks` | `tag:type:desks` |
| `all-storage` | `tag:type:storage` |
| `all-tables` | `tag:type:tables` |
| `all-boardroom` | `tag:room:boardroom` |
| `all-ergonomic` | TBD |
| `all-panels` | TBD |
| `all-accessories` | `tag:type:accessories` |
| `all-quiet-spaces` | TBD |
| `all-business-furniture` | NOT `industry:educational/daycare/healthcare` |

These are referenced in the `bbi-interlinking-map.md` as required outbound links from category pages. Until SMART-1 runs, all "View all [Category]" CTAs on category hub pages will 404 or route to generic fallback.

**Severity: BLOCK** — category hub pages (T3) have broken "View all" CTA targets.

---

## Brand-Filtered Smart Collections (SMART-1 — not yet built)

Also missing per SMART-1:

| Handle | Planned rule |
|---|---|
| `keilhauer` | vendor = "Keilhauer" |
| `global-teknion` | vendor = "Global" OR vendor = "Teknion" |
| `ergocentric` | vendor = "ergoCentric" |
| `oecm-eligible` | tag = "oecm-eligible" |

Without these, brand pages dead-end (no "Shop [Brand] products" destination).
**Severity: BLOCK** — brand pages (Wave C) cannot launch without brand-filtered collections.

---

## Summary

| Status | Count | Detail |
|---|---|---|
| ✓ Healthy hub collections | 7/9 | Seating, Desks, Storage, Tables, Boardroom, Accessories, Business Furniture |
| ⚠️ Fragile (title-match) | 3/9 | Ergonomic, Panels, Quiet Spaces |
| ✗ Empty (orphan) | 2 | room-break-room, bundle-builder-products |
| BLOCK: "View all" collections missing | 10 | SMART-1 not run |
| BLOCK: Brand-filtered collections missing | 4 | SMART-1 not run |
