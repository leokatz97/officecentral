# Feed Remediation — Batch 1 (Items 1–4)

**Date:** 2026-06-05 · **Store:** office-central-online · **Branch:** feed-readiness-audit-2026-06-05
**Source audit:** [feed-readiness-audit-2026-06-05.md](feed-readiness-audit-2026-06-05.md) (PR #113)
**Scope guardrail:** LIVE catalog writes limited to named fields only (tags `brand:`, `specs.manufacturer`, `specs.weight`, `specs.dimensions`). **No** vendor / price / availability / product-status / theme changes. Every write: full-state backup → write → hardened exact-match readback.

## Preflight
| Check | Result |
|---|---|
| `shopify theme dev` watcher | None (Admin-API metafield/tag writes are theme-independent regardless) |
| `write_products` scope | **Present** |
| `read_publications` / `write_publications` | **Absent** (drives Item 3 outcome) |

---

## ITEM 1 — Part-Time chairs finished ✅ (LIVE, verified)

The §4 run corrected the **vendor** on both Part-Time chairs to `OTG / Offices to Go` but left the `brand:` tag and `specs.manufacturer` metafield carrying the ergoCentric corruption. Closed here:

| Handle | SKU | `brand:` tag | `specs.manufacturer` | Readback |
|---|---|---|---|---|
| part-time-armless-task-chair-mvl2836 | GLB-MVL2836 | `brand:ergocentric` → **`brand:offices-to-go`** | `ergoCentric` → **`OTG / Offices to Go`** | ✅ exact |
| part-time-armless-posture-task-chair | GLB-MVL2837 | *(none)* → **`brand:offices-to-go`** | *(none)* → **`OTG / Offices to Go`** | ✅ exact |

Script `scripts/apply-parttime-tag-mfr-fix.py` · log `data/logs/parttime-tag-mfr-*.log` · backups `data/backups/parttime-*`. The headline brand mis-tag fix is now fully closed (vendor + tag + metafield all consistent).

---

## ITEM 2 — weight + dimensions on the 177 feed-blocked products ⚠️ (LIVE, partial — sourcing-limited)

**Outcome: 40 products fully cleared → now feed-READY. Feed-ready 84 → 124 of 596 ACTIVE (14.1% → 20.8%).**

### What the 177 actually needed
176 of 177 were missing **shipping weight** (the binding READY blocker in the audit's accounting); 102 were missing dimensions.

### Source (a) — verified-spec dataset: **0 usable fills**
The `spec-audit-verified-specs-2026-06-03.json` set matched only 26 of the 177 by handle/model, and for the fields these products actually *need* it provided **0 dimensions and 0 shipping weights** (the dataset carries `weight_capacity`, not shipping weight; the products it covers already had their specs). The 177 are precisely the *un-enriched remainder*, so the entire lever rested on source (b).

### Source (b) — fresh manufacturer-datasheet research (per Leo: full research, all 177)
Two multi-agent research passes (65 + 38 batches; ~5.1M subagent tokens) hit every product. Trust bar (Leo's call): **write only on a manufacturer-domain URL + verbatim snippet, spot-checked by CC.** Reseller/dealer figures recorded in notes but never written.

| Result | Count |
|---|---:|
| Products with ≥1 qualifying fill (written LIVE) | **61** |
| → fully resolved (all needed fields filled) → **now READY** | **40** |
| → partially filled (still missing the other field — all 21 missing weight) | 21 |
| Unsourceable (no manufacturer-domain value) | 116 |
| **Fields written** | **40 dimensions + 40 weight** |

### Why the "~44% lever" wasn't reachable
**Shipping/product weight is almost never published on manufacturer domains** for this catalog — it lives in dealer price lists. Of the 116 unsourceable, 115 are blocked by weight (54 weight-only + 61 both); all 21 partials are blocked by weight. Per the "wrong is worse than missing / never estimate" rule, those were left blank rather than guessed. Where Global/OTG *did* publish weight (officestogo.com product pages, Global spec PDFs and price lists, Safco, Fellowes, Gardex, Kensington), it was captured and written.

**Spot-checks (CC, independent):** 5/5 manufacturer-domain HTML sources re-fetched matched the written value exactly (kaysee OTG12112B, NLMP23BBF, MVLBC36-5, ranger-steel 7732A, etc.). PDF spec-sheet/price-list sources are manufacturer-domain + verbatim snippet but not WebFetch-re-parseable (compressed binary). Multi-model price-list values were cleaned to each product's **primary SKU** before writing; one composite product (`desk-top-divider-divide`, panel + 2 posts) was left unsourceable rather than write an inferred sum.

Script `scripts/apply-item2-specs.py` (only fills blank fields; re-checks live state before each write) · log `data/logs/item2-specs-*.log` · backups `data/backups/item2-*`.
Artifacts: `data/reports/item2-research-results-2026-06-05.json` (all 177, with source URL + snippet), `item2-fill-plan-2026-06-05.json`, **`item2-unsourceable-2026-06-05.csv`** (137 rows = 116 unsourceable + 21 partial, with research notes — the worklist for a dealer-price-list sourcing session).

---

## ITEM 3 — exclude non-products from the feed ✅ (list produced)

**Mechanism:** The Google & YouTube channel excludes products **by channel publication only** — there is no exclusion metafield in the catalog (the sole `mm-google-shopping` key in use is `google_product_category`, on 466 products). The token **lacks `write_publications`**, so this cannot be set via API. → Output is the exact one-click "remove from Google & YouTube" list for Admin.

[feed-exclude-list-2026-06-05.csv](../../data/reports/feed-exclude-list-2026-06-05.csv) — **27 rows**:
- **23** $0-price B2B quote pages (`reason = zero-price-quote-page`) — legitimately not feed-eligible; stay LIVE with Request-a-Quote per BBI rules.
- **5** placeholder/option pages (`reason = placeholder-option-page`, `likely_nonproduct = YES`): `please-select-a-finish`, `please-select-a-finish-1`, `colour`, `caster-options`, `installation-1`. All brand=BBI, all-null SKUs.

**Flagged for Leo (not acted on):** the 5 placeholders are likely non-products — decide whether they should be active at all (kept ACTIVE here; no status change).

---

## ITEM 4 — Steve vendor worklist ✅

[steve-vendor-worklist-2026-06-05.csv](../../data/reports/steve-vendor-worklist-2026-06-05.csv) — **91 rows**:
- **86** ACTIVE products still vendored "Brant Business Interiors" with no auto-resolving signal (AMBIGUOUS).
- **5** NON-BBI-CONFLICT (a human set a real non-BBI brand conflicting with SKU/metafield evidence), incl. the Heartwood `GLBMVLM23FF` pedestal.

Columns: handle, title, current SKU, current vendor, conflicting evidence (SKU prefix / metafield / tag), candidate manufacturer(s), blank **`steve_real_manufacturer`**. Grouped NON-BBI-CONFLICT → decodable-but-uncertain (57) → no-SKU (34). This is the sheet CC applies (backup + readback) once Steve fills it.

---

## Net catalog state after this batch
- Feed-ready ACTIVE: **84 → 124 / 596 (14.1% → 20.8%)**
- Part-Time brand mis-tag: **fully closed** (vendor + tag + metafield)
- Open levers for next batches (unchanged from audit punch-list): weight via dealer price lists (137-row worklist ready), images <500px (160), brand=BBI resolution (91-row Steve sheet), google_product_category (107).

**Nothing published. No price/availability/status/theme/vendor changes.**
