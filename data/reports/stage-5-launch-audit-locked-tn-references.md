# Stage 5 Launch Audit — 4.4 Locked Tn References
**Date:** 2026-05-08
**Auditor:** Claude Code (read-only pass)
**Companion:** `docs/strategy/locked-references/README.md` (created this session)

---

## What a locked Tn reference is

A "locked Tn reference" is a static visual screenshot or HTML file of a specific BBI template (T1–T6) that was approved by Steve and serves as the pixel-diff target. Every build row is only ✅ when the rendered page passes a visual diff against its locked Tn reference (≤5% delta).

---

## Tn reference inventory

### T1 — Homepage

| Source | Location | Locked? |
|---|---|---|
| Claude Design Phase 3 screen exports | `data/design-photos/screens-v1-2026-04-28/` | ✓ Approved (DS-0, commit `c1a719c`) |
| Anti-regression baseline screenshots | `data/design-photos/ANTI-REF-baseline-2026-04-27-homepage.png`, `ANTI-REF-baseline-2026-04-27-nav.png` | ✓ Captured |
| HTML standalone | Accessible via `data/design-photos/screens-t2-locked-2026-04-28/Homepage.jsx` | Reference only |

**T1 status: LOCKED** — visual reference exists from Steve-approved DS-0 export. Can be used as baseline target for homepage diff.

---

### T2 — Shop All (Business Furniture Vertical)

| Source | Location | Locked? |
|---|---|---|
| Claude Design T2 locked screens | `data/design-photos/screens-t2-locked-2026-04-28/` | ✓ Locked |
| Standalone HTML | `data/design-photos/screens-t2-locked-2026-04-28/01-02-LOCKED-standalone.html` | ✓ Approved |
| CollectionCategory JSX | `data/design-photos/screens-t2-locked-2026-04-28/CollectionCategory.jsx` | Reference |

**T2 status: LOCKED** — Steve-approved. Use `01-02-LOCKED-standalone.html` as visual spec.

---

### T3 — Category Hub (e.g. Seating, Desks)

| Source | Location | Locked? |
|---|---|---|
| Claude Design T3 locked screens | `data/design-photos/screens-t3-LOCKED-2026-04-29/` | ✓ Locked |
| Standalone HTML | `data/design-photos/screens-t3-LOCKED-2026-04-29/01-03-LOCKED-standalone.html` | ✓ Approved |
| HTML index | `data/design-photos/screens-t3-LOCKED-2026-04-29/index.html` | ✓ |

**T3 status: LOCKED** — Steve-approved. `01-03-LOCKED-standalone.html` is the visual target for category hub diffs.

---

### T4 — Sub-collection Product Listing

| Source | Location | Locked? |
|---|---|---|
| Stage 3.2a spec extract | `data/reports/stage-3.2a-t4-spec-extract.md` | Text spec only — no screenshot |
| Stage 3.2b subcollection T4 | `data/reports/stage-3.2b-subcollection-t4.md` | Implementation report, not visual |

**T4 status: NOT LOCKED** — No Claude Design screen export exists for T4. The section was built to spec from `stage-3.2a-t4-spec-extract.md` and the locked design-system.md tokens, but there is no pixel-diff target file.

**Action needed:** Screenshot the dev theme sub-collection page (e.g. `/collections/highback-seating`) after visual QA approval by Steve, then lock it as the T4 reference. Until then, T4 visual diffs are manual inspection only.

---

### T5 — PDP (Product Detail Page)

| Source | Location | Locked? |
|---|---|---|
| Claude Design T5 screens | `data/design-photos/screens-t5-2026-05-04/` | ✓ Captured |
| T5 spec extract | `data/reports/stage-4a-t5-spec-extract.md` | Text spec |
| PDP audit | `data/reports/stage-4a-current-pdp-audit.md` | Gap analysis |

**⚠️ T5 status: BLOCKED** — `ds-pdp-base.liquid` does not exist yet (Stage 4b not started). No rendered page exists to compare against. The T5 Claude Design export (`screens-t5-2026-05-04/`) exists as a design reference, but cannot be used for pixel-diff until the section is built and Steve approves a rendered screenshot.

Directories in `screens-t5-2026-05-04/`: `landing-oecm/` and `pdp-unbuyable/` — these are design mockup exports, not live-page screenshots.

---

### T6 — Not defined

T6 is not formally defined in the site architecture. The 5-template plan covers T1 (homepage), T2 (shop-all), T3 (category hub), T4 (sub-collection), T5 (PDP). Additional templates (blog, article, 404) were added later and have no Tn designations.

---

## Status of other templates needing references

| Template | Reference status | Blocked on |
|---|---|---|
| Cart (`/cart`) | ✗ No BBI reference | Stage 5: cart rebuild required first |
| 404 | ✗ No BBI reference | 404-1 build not started |
| Blog (`/blogs/news`) | ✗ No BBI reference | BLOG-TPL-1 build not started |
| Article | ✗ No BBI reference | BLOG-TPL-1 build not started |
| RFQ modal | ✗ No BBI reference | LEAD-3 build not started |
| Search | N/A — Starlite default | Not in `bbi_landing` gate |
| Account/Login | N/A — Starlite default | Not in `bbi_landing` gate |

---

## What can be locked from dev-theme screenshots now (Steve approval needed)

These templates are built and deployed to the dev theme. Once Steve signs off on current visual state, a screenshot can be taken with `capture-bbi-baselines.py --lock` and treated as the locked reference:

- T1 Homepage
- T2 Business Furniture vertical (collection.business-furniture)
- T3 Category hubs (collection.seating, collection.desks, etc.)
- All Phase 1 landing pages (OECM, Healthcare, Quote, etc.)
- All Wave C landing pages (About, Brands, Our Work, etc.)

---

## Summary

| Template | Reference locked? | Note |
|---|---|---|
| T1 Homepage | ✓ | DS-0 export + anti-regression baseline |
| T2 Shop-All | ✓ | `01-02-LOCKED-standalone.html` |
| T3 Category Hub | ✓ | `01-03-LOCKED-standalone.html` |
| T4 Sub-collection | ✗ | No screenshot baseline — needs Steve sign-off on dev theme |
| T5 PDP | ✗ BLOCKED | `ds-pdp-base.liquid` does not exist yet |
| Cart | ✗ BLOCKED | Cart rebuild not started |
| 404 | ✗ BLOCKED | 404-1 not started |
| Blog/Article | ✗ BLOCKED | BLOG-TPL-1 not started |
| RFQ Modal | ✗ BLOCKED | LEAD-3 not started |
