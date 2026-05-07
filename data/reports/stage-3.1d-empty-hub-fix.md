# Stage 3.1d — Empty Hub Smart-Collection Rule Fix

**Date:** 2026-05-07  
**Branch:** `chore/stage-3.1d-empty-hub-rules`  
**Dev theme:** `186373570873`  
**Catalog size at time of audit:** 653 products

---

## Pre-State: Empty Hubs

| Hub handle | Collection ID | Old rules (all tags) | Product count |
|---|---|---|---|
| ergonomic-products | 526847476025 | `tag = type:ergonomic`, `type:monitor-arms`, `type:keyboard-trays`, `type:footrests`, `type:back-supports`, `type:sit-stand-converters`, `type:ergonomic-products` | **0** |
| panels-room-dividers | 526847508793 | `tag = type:panels`, `type:dividers`, `type:room-dividers`, `type:panel-systems`, `type:acoustic-panels` | **0** |
| quiet-spaces | 526847574329 | `tag = type:acoustic-pods`, `type:phone-booths`, `type:focus-pods`, `type:quiet-spaces`, `type:acoustic-booths` | **0** |

**Root cause:** The catalog uses only 5 coarse `type:` tags (`chairs`, `tables`, `desks`, `accessories`, `storage`). None of the granular `type:ergonomic`, `type:panels`, or `type:acoustic-pods` tags exist on any product. The hubs were built with aspirational tagging that was never applied to the catalog.

---

## Tag Investigation Findings

Full data: [stage-3.1d-tag-investigation.csv](stage-3.1d-tag-investigation.csv)

**Key finding:** All 18 unique catalog tags are broad room/industry/type groupings. No product-level ergonomic, panel, or acoustic taxonomy exists. Rules must use `title contains` matching against product titles, which are more descriptive than tags in this catalog.

---

## Proposed Rules

Full spec: [stage-3.1d-proposed-rules.md](stage-3.1d-proposed-rules.md)

---

## User-Approved Rules Applied

### ergonomic-products — APPLIED ✅

**Rules (disjunctive, 4 conditions):**
| column | relation | condition |
|--------|----------|-----------|
| title | contains | monitor arm |
| title | contains | keyboard tray |
| title | contains | sit-stand |
| title | contains | anti-fatigue |

**Post-apply product count: 16** (predicted 16 — exact match ✅)

### panels-room-dividers — APPLIED ✅

**Rules (disjunctive, 5 conditions):**
| column | relation | condition |
|--------|----------|-----------|
| title | contains | partition |
| title | contains | room divider |
| title | contains | modesty panel |
| title | contains | otg panel |
| title | contains | divider |

Note: `title contains "divider"` adds 4 desk-top divider products beyond the base 12 (user approved optional expansion to 16).

**Post-apply product count: 16** (predicted 16 — exact match ✅)

### quiet-spaces — APPLIED (broad acoustic interpretation) ✅

**Rules (disjunctive, 4 conditions):**
| column | relation | condition |
|--------|----------|-----------|
| title | contains | acoustic |
| title | contains | sound dampener |
| title | contains | phone booth |
| title | contains | soft pod |

True enclosures: 2 (Pod phone booths, Soft pods). Acoustic treatment products: 7 (ceiling baffles, grids, wall tiles, felt dampeners). User approved broad interpretation pending Stage 3.2 split.

**Post-apply product count: 9** (predicted 9 — exact match ✅)

---

## Templates Flipped to grid_mode=both

All 3 hubs now exceed the 5-product threshold. All flipped from `"tiles"` → `"both"` in the dev theme.

| Template | Old grid_mode | New grid_mode | Pushed to dev theme |
|---|---|---|---|
| `templates/collection.ergonomic-products.json` | tiles | **both** | ✅ 2026-05-07T16:20:42 |
| `templates/collection.panels-room-dividers.json` | tiles | **both** | ✅ 2026-05-07T16:20:43 |
| `templates/collection.quiet-spaces.json` | tiles | **both** | ✅ 2026-05-07T16:20:43 |

---

## Spot-Check Results

| Check | Result |
|---|---|
| Admin API rules confirmed on store | ✅ All 3 collections show new rules |
| Product counts match predictions | ✅ 16 / 16 / 9 exact |
| Dev theme `grid_mode=both` confirmed via Assets API read-back | ✅ All 3 |
| `/collections/ergonomic-products` → HTTP 200 | ✅ (initial 503 was transient, 200 on immediate retry) |
| `/collections/panels-room-dividers` → HTTP 200 | ✅ |
| `/collections/quiet-spaces` → HTTP 200 | ✅ |

---

## 6 Populated Hubs — Confirmed Untouched

| Handle | Product count | Changed? |
|---|---|---|
| desks | 98 | No |
| tables | 104 | No |
| storage | 82 | No |
| accessories | 91 | No |
| chairs | (custom collection, not queried) | No |
| lounge | (custom collection, not queried) | No |

No rules were modified on any of the 6 already-populated hubs.

---

## Stage Backlog: Hubs Needing Product-Side Tagging

No hubs were left empty — all 3 exceeded the 5-product threshold with title-based rules. However, the `title contains` approach is brittle: it relies on consistent product naming and will drift as inventory changes. Product-side tagging remains a deferred workstream.

---

## Watch Items (logged for Stage 3.2 input)

1. **quiet-spaces should ideally split into two sub-collections:**
   - `Pods & Booths` — enclosures only (currently 2 products: Pod phone booths, Soft pods)
   - `Acoustic Treatments` — ceiling/wall products (currently 7 products: baffles, grids, wall tiles, dampeners)
   At 2 products, Pods & Booths is too thin to stand alone today. Recommend splitting when ≥5 pod/booth SKUs are onboarded.

2. **Tighten quiet-spaces rule when more SKUs onboard:**
   Current rule `title contains "acoustic"` pulls in acoustic treatment products. When enough pod/booth SKUs exist with consistent naming (e.g., containing "pod" or "booth"), replace the acoustic catch-all with enclosure-specific rules and move acoustic treatments to a dedicated collection.

---

## Halt

**Do not merge until you have visually verified the now-populated hubs on the dev theme preview URL.**

Dev theme preview: `https://brantbusinessinteriors.com/collections/ergonomic-products?preview_theme_id=186373570873`
