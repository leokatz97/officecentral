# Industry tag system — decision
_2026-05-13 · TAG-INDUSTRY-CHECK (Step 6) · Read-only investigation._

## TL;DR

**PARTIALLY ALIVE — recommend retiring the system and rebuilding the one real consumer.**
The `industry:*` tag system has exactly one active storefront use: the `business-furniture` smart collection uses three `tag not_equals industry:*` exclusion rules to keep strollers and a bariatric chair out of the business furniture catalog. That logic is real and currently working (for 2 products). However, `industry:business` — the tag on 548 of 593 products — has zero storefront consumers and is pure noise. The industry landing pages (healthcare, education, government, non-profit, professional-services) are fully editorial and do not filter products by `industry:*` tags at all. Recommendation: strip all 550 `industry:*` tags AND replace the `business-furniture` exclusion rules with positive `type:*` inclusion rules (more robust, no future maintenance burden as more niche products are added).

---

## Current state

| Tag | Count | % of active |
|---|---|---|
| `industry:business` | 548 | 92.4% |
| `industry:healthcare` | 1 | 0.2% |
| `industry:daycare` | 1 | 0.2% |
| **Total products with any `industry:*` tag** | **~550** | **92.8%** |

---

## Investigation findings

### Industry pages found

| Handle | Published | Template suffix | Uses `industry:*` tags? |
|---|---|---|---|
| `/pages/industries` | ✅ | `industries` | ❌ No |
| `/pages/healthcare` | ✅ | `healthcare` | ❌ No |
| `/pages/education` | ✅ | `education` | ❌ No |
| `/pages/government` | ✅ | `government` | ❌ No |
| `/pages/non-profit` | ✅ | `non-profit` | ❌ No |
| `/pages/professional-services` | ✅ | `professional-services` | ❌ No |

All 6 industry pages use custom template suffixes. Their Liquid section files (`ds-lp-industries.liquid`, `ds-lp-healthcare.liquid`, etc.) contain zero references to `industry:` tag filtering. These pages are fully editorial — hardcoded section content, no product tag queries. They surface products by linking to collections (e.g., "View all seating →"), not by filtering on `industry:` tags.

### Theme files referencing `industry:` tags

A full grep of `theme/sections/`, `theme/snippets/`, `theme/templates/`, and `theme/layout/` for `industry:` returned **zero matches**. No Liquid file reads or filters on `industry:*` tags.

### Smart collections referencing `industry:` tags

One smart collection uses `industry:*` tags: **`business-furniture`** (conjunctive, 3 rules).

| Rule | Column | Relation | Condition | Functional? |
|---|---|---|---|---|
| 1 | tag | not_equals | `industry:educational` | ❌ Dead — 0 products carry this tag |
| 2 | tag | not_equals | `industry:daycare` | ✅ Live — excludes `foundations-sport-splash-quad-strollers` |
| 3 | tag | not_equals | `industry:healthcare` | ✅ Live — excludes `willow-bariatric-chair` |

**No other smart collection references `industry:*` tags.** (49 smart collections checked.)

### Synthesis

The `industry:*` tag system has exactly one active storefront consumer (the `business-furniture` exclusion rules), and that consumer only meaningfully acts on 2 of the 550 tagged products. The 548 products carrying `industry:business` are not consumed by any collection rule, any Liquid template, or any filter. The design of the business-furniture collection (exclusion-only, no positive inclusion rules) means it currently includes ~591 of 593 products, which was almost certainly not the original intent.

### Classification: PARTIALLY ALIVE

At least one storefront surface (the `business-furniture` smart collection) actively reads `industry:*` tags to surface products — but the data is so fragmented (2 meaningful exclusions vs. 548 mass-applied junk tags) that the system is not meaningfully functional.

---

## Recommendation

**Retire the `industry:*` tag system. Simultaneously fix the `business-furniture` smart collection.**

### Step 1 — Strip all `industry:*` tags (550 products)

Same pattern as the OECM tag remediation (BUG-FIX-2/BUG-FIX-3). Bulk-strip:
- `industry:business` from 548 products
- `industry:healthcare` from 1 product (`willow-bariatric-chair`)
- `industry:daycare` from 1 product (`foundations-sport-splash-quad-strollers`)

### Step 2 — Fix `business-furniture` smart collection rules

**Before stripping industry tags**, update the `business-furniture` smart collection to use positive `type:*` inclusion rules instead of the 3 negative exclusion rules. The current exclusion approach is fragile: every new niche product category (e.g., residential, automotive, lab) would require a new exclusion rule manually added.

Proposed replacement rules (disjunctive = true):
- `tag equals type:chairs`
- `tag equals type:desks`
- `tag equals type:tables`
- `tag equals type:storage`
- `tag equals type:accessories`
- `tag equals type:lounge`
- _(add `type:outdoor`, `type:panels`, `type:ergonomic` as those tags roll out)_

This is more explicit, future-proof, and aligns with the existing `type:*` smart collection infrastructure (`all-chairs`, `all-desks`, etc.).

**Note:** `type:*` tag coverage is currently 39.8% of the catalog (236/593 products). The `business-furniture` disjunctive collection will be smaller than expected until TYPE-APPLY-1 (the full type-tag pass for all 593 products) runs. This is acceptable — the current exclusion-based collection is also broken (returns 591 products).

### Estimated effort

- Strip `industry:*` tags: ~15 min Claude Code session (same script pattern as BUG-FIX-3)
- Update `business-furniture` smart collection rules: ~5 min (1 API PATCH call)
- Total: ~20 min

---

## Steve's next move

**Fold into BUG-FIX-3 scope** (launch tracker Step 4 — the tag remediation session already planned).

Before running BUG-FIX-3:
1. Confirm the `business-furniture` smart collection replacement rules above (or adjust the `type:*` list)
2. Add to BUG-FIX-3 scope: (a) update `business-furniture` smart collection rules, (b) strip all `industry:*` tags

No new tracker step needed — this fits cleanly inside BUG-FIX-3's planned "bulk tag strip" session. Add a note in the BUG-FIX-3 row that it covers: oecm-eligible strip + industry:* strip + business-furniture rule fix.
