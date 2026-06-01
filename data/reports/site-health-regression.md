# Site-Health / Regression Audit — 2026-06-01

**Scope:** today's CHANGED surfaces only — the 53 S5+S6 enriched PDPs (PRs [#73](https://github.com/leokatz97/officecentral/pull/73), [#74](https://github.com/leokatz97/officecentral/pull/74)), the touched collections, the 3 landing pages.
**Mode:** READ-ONLY. No site/theme writes. This report is the only file written.
**Method:** live storefront fetches (`https://www.brantbusinessinteriors.com`), raw HTML parsed for status / robots / canonical / JSON-LD / meta / NAP / links; sitemap shards crawled; spec presence checked against committed payloads. Theme `186373570873` (role=main).
**Coverage caveat:** this audit covers **structural SEO/AEO integrity only**. Ranking impact — especially the pending **boardroom 301** — does NOT surface here; it shows up in the next weekly rank-tracking snapshot. **Boardroom is the one to watch there** (the currently-ranking `boardroom-conference-meeting` gets 301'd into the zero-rank `boardroom`).

---

## Findings table

| # | Check | Verdict | Note |
|---|-------|---------|------|
| 1 | Status codes | ⚠️ | All 53 PDPs = 200. But the "expected anomaly" note is **stale** — `executive-desks` already **301→/collections/desks** and `healthcare-seating` is **404**; neither serves 200. The real pending-redirect 200s are `reception` + `boardroom-conference-meeting`. |
| 2 | Indexability | ✅ | No `noindex` on any in-scope URL (all `index,follow`). 53/53 enriched PDPs present in `sitemap.xml`. |
| 3 | JSON-LD (Product + Breadcrumb) | ✅ | 53/53 PDPs have valid `Product` + `BreadcrumbList`; all required Product fields present; **0 parse errors**. `Organization` + `LocalBusiness` + `WebSite` render sitewide (60/60 surfaces). |
| 4 | Meta integrity | ⚠️ | `title_tag` 53/53 ≤60; all descriptions ≤160; 3 landing pages clean; healthcare meta-repair **verified clean**. Two non-blocking issues below (rendered-title suffix; one more dangling desc on the boardroom dupe). |
| 5 | Internal links | ✅ | Enriched PDP bodies contain **zero** anchors (link-wiring deferred per plan) → no broken links introduced. **Zero** in-scope pages (incl. nav/footer) link to any redirect-source slug → no chain risk from current content. |
| 6 | Canonicals | ⚠️ / 🔴 | Survivors (`reception-desks-desks`, `boardroom`) self-canonical correctly. Dupes also self-canonical → they self-compete until the 301s import (canonicals do **not** pre-resolve it). 🔴 separate issue: the **Row 4 redirect target chains** (see below). |
| 7 | Entity / NAP consistency | ✅ | 60/60 pages: "Brant Business Interiors" + "296 George" + "Peterborough" + single phone **1-800-835-9565**. No literal "BBI" in any title/desc. |
| 8 | FAQ schema | ✅ | `/pages/healthcare` `FAQPage` valid (7 questions, parses clean). Also valid on `boardroom`, `design-services`, `professional-services`. |
| 9 | Spec extractability | ✅ | 53/53 render a Specifications/Dimensions block + warranty + country + ≥1 certification + full body copy **server-side** (machine-readable, not JS-only). |

**Bottom line:** No structural regression was introduced by today's writes. The enriched PDPs are clean across the board. The action items are all in the cannibalization/redirect layer and one stale expectation — none block, but two should be fixed *before Steve imports the redirects*.

---

## Detail & proposed fixes (write nothing — for Steve / next session)

### 🔴 R1 — Row 4 redirect target chains (fix the CSV before import)
`data/redirects/landing-refresh-301s.csv` Row 4 = `/collections/healthcare-seating → /collections/healthcare`. But **`/collections/healthcare` itself 301s → `/collections/business-furniture`**. Importing Row 4 as written creates a chain `healthcare-seating → healthcare → business-furniture`, and the row's premise ("consolidate into the healthcare canonical that ranks #48") is undermined because `/collections/healthcare` doesn't serve its own content. The #48 healthcare rank lives on **`/pages/healthcare`** (200, clean), not the collection.
**Proposed fix:** repoint Row 4 to `/collections/business-furniture` directly (kills the chain), or to `/pages/healthcare` if seating authority should flow to the landing page. Decide before import.

### ⚠️ R2 — Status-code expectation is stale
- `executive-desks` → **301 → /collections/desks** (clean single hop to 200). The Row 3 redirect appears **already live** — not a pending 200.
- `healthcare-seating` → **404** (unpublished, no redirect yet). A 404 here is crawler-acceptable (better than a 200 empty page), but Row 4 is **not** imported and, as written, would chain (R1).
- The genuinely-pending-200 surfaces are **`reception`** and **`boardroom-conference-meeting`** (still published, awaiting Rows 1–2). Their 200 is correct/expected.
**Net:** the audit brief's "only expected 200 anomaly = exec-desks + healthcare-seating" is incorrect on today's live state — neither serves 200. No fix needed; just correcting the record.

### ⚠️ R3 — Reception pair is now an identical-meta twin (import Row 1 promptly)
The meta migration correctly placed the optimized meta on the survivor `reception-desks-desks` (`Reception Desks | Brant Business Interiors` / 154-char desc). But `/collections/reception` now carries the **identical** title + description, both 200, both `index,follow`, both self-canonical. Until Row 1 (`reception → reception-desks-desks`) imports, these are two identical pages competing head-to-head (arguably worse than the pre-migration state, when the dupe had differentiating generic meta). **No content fix — just import Row 1 soon.** (Recoverable; source collection still exists.)

### ⚠️ R4 — Second dangling meta description (boardroom dupe)
The audit asked to confirm no dangling strings beyond the repaired healthcare one. There is one more: **`/collections/boardroom-conference-meeting`** desc = `"- Office Central & Brant Business Interiors"` (just the theme suffix, leading dash, no real description) and title 66 chars. This is the **pre-existing generic** on the to-be-301'd dupe — it disappears once Row 2 imports, so low priority, but flagging per the explicit ask. Not introduced today.

### ⚠️ R5 — Rendered `<title>` >60 on 38/53 PDPs (pre-existing theme behaviour, not a regression)
The `title_tag` values written today are all ≤60 and well-formed. The over-length comes from a **sitewide theme title template** that appends `– Office Central & Brant Business Interiors` when the `title_tag` doesn't already end in the brand. Result is inconsistent: **15 PDPs render clean (~51 chars)** because their `title_tag` ends in "Brant Business Interiors"; **38 render at 94–106 chars** with the suffix appended (brand gets truncated in SERP). Theme was untouched today (PR notes confirm 0 theme files), so this is **not a regression** — but it's a real hygiene item and an authoring inconsistency.
**Proposed fix (later, theme-scoped, out of today's scope):** standardize — either drop the brand from all `title_tag`s and shorten the theme suffix, or keep the brand in all `title_tag`s and have the suffix-suppression fire consistently.

---

## What was verified clean (no action)
- 53/53 enriched PDPs: 200, indexable, in sitemap, valid Product + Breadcrumb + Org/LocalBusiness/WebSite JSON-LD, server-side spec blocks (dimensions/warranty/country/certs), `title_tag` ≤60, desc ≤160, no broken/redirect-source links, consistent NAP.
- 3 landing pages (`design-services`, `professional-services`, `healthcare`): clean keyword-aligned titles (48/52/54) + descs (154/156/155), valid FAQPage, healthcare meta-repair confirmed (no dangling).
- Survivor collections (`reception-desks-desks`, `boardroom`): optimized meta in place, self-canonical, indexable.
- NAP / entity consistency: perfect across all 60 surfaces.

## Watch-list for next rank snapshot
- **Boardroom (priority watch):** Row 2 301s the currently-ranking `boardroom-conference-meeting` (#22/#25/#50/#70) into the zero-rank `boardroom`. Expect short-term volatility; confirm recovery in the weekly DataForSEO snapshot. Recoverable by deleting the redirect.
- Reception cluster: watch `reception desk` / `black reception desk` (#36) / `reception desk custom` (#41) consolidate onto `reception-desks-desks` after Row 1.
