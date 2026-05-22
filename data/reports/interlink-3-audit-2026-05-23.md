# BBI INTERLINK-3 Cross-Link Audit — 2026-05-23

Final cross-link audit across all `bbi_landing` pages per Step 26
INTERLINK-3 prompt. Unblocked post-CONTENT-POLISH-1 (PR #10) + AI-9 +
schema batch-fix. Hard requirement: **0 FAIL findings before LAUNCH-2**.

Branch: `feature/interlink-3` from `main` @ `9d132f3`.
DEV theme target: `186373570873` (writes confined per safety preflight).

---

## Executive Summary

| Metric | Value |
|---|---|
| Pages audited (section + JSON template) | **23 BBI pages + 10 collection pages + 9 BBI snippets** |
| Theme files scanned | 31 sections + 9 snippets + 23 page templates + 12 collection templates + index.json = **75 files** |
| Total `<a href>` + JSON-setting-URL entries extracted | **623** |
| Unique BBI-internal destinations | **42 destinations linked from 2+ source pages** |
| Live BBI collection handles confirmed | **388** (66 smart + 322 custom) |
| Live BBI page handles confirmed published | **23 of 23 canonical pages PUB** ✅ |
| **FAIL findings (broken/wrong)** | **1** → fixed in this branch (target 0 met) |
| **WARN findings (consistency)** | **89** — almost all `tel:` `+1` prefix format consistency (89/90) + 1 false positive |
| **INFO findings (missing expected cross-links)** | **18** (15 HIGH / 3 LOW) — surfaced for review, not auto-fixed |
| Broken `/pages/*` references | **0** ✅ |
| Broken `/collections/*` references | **0** ✅ |
| Wrong email domain references | **0** ✅ |
| Wrong phone-number references | **1** (FAIL) — corrected |

Validation method: extracted every `<a href="...">` and JSON URL setting
from the in-scope theme tree, classified by destination type, validated
internal handles against the live Shopify Admin API (2026-04), and
cross-referenced against the EXPECTED CROSS-LINKS map from the prompt
spec.

---

## FAIL findings (must fix pre-LAUNCH-2)

### F-1 — Hard-coded local phone number on collection-base "Phone CTA closer"

- **Source:** `theme/sections/ds-cs-base.liquid:593`
- **Anchor text:** `Call a Consultant`
- **href:** `tel:+15198371810`
- **Why FAIL:** Local Brantford (519) area-code number. Locked sitewide
  phone is `tel:+18008359565` (toll-free), per `feedback_bbi_copy_voice.md`
  + `bbi-org-schema.liquid` + Day 8 schema batch-fix (commit `c7cdb20`).
  The 519 number appears nowhere else in the theme — leftover from an
  earlier draft. Affects every collection page that renders the
  ds-cs-base phone CTA closer (gated by `section.settings.show_phone_cta`).
- **Recommended fix:** one-line `tel:+15198371810` → `tel:+18008359565`.
- **Status:** ✅ **FIXED in this branch** — Phase 6, commit ahead.

After F-1 fix: **FAIL count = 0.** ✅ INTERLINK-3 hard gate met.

---

## WARN findings (consistency)

### W-1 — `tel:` href format inconsistency (89 occurrences across 29 files)

- **Pattern:** Theme code emits `tel:18008359565` (no `+1` prefix) instead
  of the locked `tel:+18008359565` from `feedback_bbi_copy_voice.md` and
  the sitewide org schema (`bbi-org-schema.liquid` uses `+1-800-835-9565`).
- **Severity rationale:** Browsers handle `tel:` URIs without the `+`
  prefix correctly — the dial action works in every modern browser and
  iOS/Android dialer. The digits match the locked number. So this is a
  **consistency issue, not a broken link**.
- **Distribution:** 86 hard-coded `tel:18008359565` + 3 Liquid-templated
  `tel:{{ section.settings.phone_href }}` (default `18008359565`). Spread
  across:

  | File | Count |
  |---|---:|
  | theme/sections/ds-lp-faq.liquid | 15 |
  | theme/sections/ds-lp-education.liquid | 6 |
  | theme/sections/ds-lp-government.liquid | 6 |
  | theme/sections/ds-lp-healthcare.liquid | 6 |
  | theme/sections/ds-lp-non-profit.liquid | 6 |
  | theme/sections/ds-lp-industries.liquid | 5 |
  | theme/sections/ds-lp-oecm.liquid | 4 (3 Liquid-templated + 1 indirect) |
  | theme/sections/ds-lp-quote.liquid | 3 (3 Liquid-templated) |
  | theme/sections/ds-lp-professional-services.liquid | 3 |
  | theme/sections/ds-lp-about.liquid | 3 |
  | (others) | ≤ 2 each — ds-lp-brands-* × 6, ds-lp-contact, ds-lp-delivery, ds-lp-relocation, ds-cc-base, ds-pdp-base, ds-article, ds-blog-list, ds-lp-customer-stories, ds-lp-our-work, ds-system-404, bbi-nav, bbi-footer |

- **Recommended fix (deferred, NOT applied in this branch — out of scope
  for INTERLINK-3 per HARD RULES "20+ findings, halt and discuss"):**
  Normalize all `tel:` hrefs to `tel:+18008359565` site-wide via a
  Phase-2 follow-up. Two-step approach:
  1. Update Liquid default `phone_href: "18008359565"` → `"+18008359565"`
     in OECM + quote section schemas (catches the 3 Liquid-templated
     cases without touching JSON templates).
  2. Run a sed pass on the 86 hard-coded `tel:18008359565` → `tel:+18008359565`
     across the 29 files.
- **Decision:** Logged as WARN-1 in this audit. Not applied — does not
  block LAUNCH-2 (digits dial correctly). Add to post-launch backlog.

### W-2 — Cross-page anchor-text inconsistency (30 destinations)

For 30 destinations linked from 2+ source pages, the anchor text differs.
**The vast majority are by-design** — each landing page contextualizes
the link with industry-specific framing (e.g., the healthcare page links
`/collections/seating` as "Patient & Bariatric Seating" while the
education page calls it "Staff & Lounge Seating"). This is intentional
editorial work from CONTENT-POLISH-1 Sessions A + B; consolidating would
reduce SEO + UX value.

**Truly worth normalizing (review-only, no fixes applied):**

- **/pages/oecm — 9 unique anchor texts across 9 source lines.** Suggest
  consolidating to two canonical patterns: short label "OECM" (nav,
  footer chips, breadcrumbs) and descriptive "OECM purchasing details"
  or "OECM Agreement 2025-470" (body content + CTAs). Currently uses:
  - "Agreement 2025-470" (ds-lp-contact.liquid:141)
  - "How OECM works →" (ds-lp-customer-stories.liquid:156)
  - "Read the OECM details →" (ds-lp-customer-stories.liquid:315)
  - "Learn about OECM purchasing →" (ds-lp-brands-ergocentric.liquid:278)
  - "See the OECM coverage table →" (ds-lp-faq.liquid:506)
  - "See our OECM overview" (ds-lp-quote.liquid:1046)
  - "OECM Procurement" (bbi-footer.liquid:226)
  - "OECM-eligible supplier" (bbi-footer.liquid:254)
  - "OECM purchasing details →" (bbi-oecm-bar.liquid:78)

- **/pages/brands** — 5 anchor texts: "View all brands →", "Brands page",
  "Browse our brand pages", "All brands", "Brands Hub". Suggest
  canonical "Browse all brands" (or short "Brands" for nav/footer).

The other 28 inconsistencies are contextual by editorial design and not
worth normalizing. Full per-destination list:
`data/reports/interlink-3-evidence/anchor-inconsistencies.json`.

### W-3 — One regex false positive: bbi-nav.liquid:832

The static extractor flagged a JS template-literal `href="' + p.url + '"`
inside the search-autocomplete `<script>` block. This is runtime markup
generation, not a broken href — `p.url` is the Shopify-supplied product
URL from `/search/suggest.json`. Confirmed safe — noted here only to
explain the discrepancy if this report is diff'd against a future run.

---

## INFO findings (missing expected cross-links — review only, no auto-fix)

Per prompt scope: "Adding NEW cross-links requires separate review."
These are surfaced for backlog triage. **18 total — 15 HIGH, 3 LOW.**

### HIGH (15 — contextual cross-links missing from body content)

> "Body content" = the page's own `ds-lp-*.liquid` section + its `page.*.json`
> template settings. Excludes nav + footer (those satisfy *minimum*
> reachability sitewide, but contextual links in body content drive
> in-flow procurement funnels and AI-search retrieval).

| Page | Missing body-level link → | Suggested anchor + location |
|---|---|---|
| /pages/oecm | /pages/education | "Eligible buyers: Ontario school boards … <a href='/pages/education'>education sector</a>" in the existing eligible-buyers FAQ |
| /pages/oecm | /pages/healthcare | same FAQ paragraph |
| /pages/oecm | /pages/government | same FAQ paragraph |
| /pages/oecm | /pages/about | Entity-clarity section already references entity — add `<a>` wrap to "Brant Business Interiors" |
| /pages/healthcare | /collections/ergonomic-products | Healthcare currently cross-links seating/desks/tables — add ergonomic to the category quartet for compliance-driven workstation buyers |
| /pages/design-services | /pages/quote | **Notable gap** — Design Services has no body-level CTA to /pages/quote (only nav/footer). Add a "Get a quote" CTA below the 3-step how-to-purchase block |
| /pages/quote | /pages/delivery | Quote currently cross-links to design-services + oecm in body; missing the delivery service cross-sell |
| /pages/relocation | /pages/design-services | Relocation has the existing 4-phase Process section — add a "Pair with design services" link in Phase 1 |
| /pages/relocation | /pages/delivery | Add a Phase 3 cross-link to /pages/delivery for the install/post-move logistics phase |
| /pages/brands-ergocentric | /pages/brands | Add "← Back to all brands" link in hero or above-fold area |
| /pages/brands-otg | /pages/brands | same pattern (6 brand pages, same gap) |
| /pages/brands-global-teknion | /pages/brands | same pattern |
| /pages/brands-heartwood | /pages/brands | same pattern |
| /pages/brands-keilhauer | /pages/brands | same pattern |
| /pages/brands-obusforme | /pages/brands | same pattern |

**Pattern observed:** the 6 brand pages all share the same gap (no body
"back to brands hub" link). A single template-edit pass to add a
breadcrumb-style "← All brands" affordance to the brand-page hero would
close 6 of these 15 in one change.

**Notable single-page gap:** Design Services has no body-level CTA to
the quote page (relies entirely on nav + footer). Worth surfacing to
Steve — design-services is a high-intent funnel page that should hand
off to /pages/quote directly.

### LOW (3 — secondary proof / related-service cross-links)

| Page | Missing body-level link → | Recommended placement |
|---|---|---|
| /pages/delivery | /pages/customer-stories | "See how Kawartha Dairy received their install →" in the proof strip |
| /pages/delivery | /pages/our-work | "See project galleries" in the closer section |
| /pages/design-services | /pages/relocation | "Planning a move? Pair design with relocation →" cross-sell |

### INFO false positives filtered (1)

- /pages/oecm → /pages/quote — Liquid `default` resolves at runtime
  (line `ds-lp-oecm.liquid:339`: `default: '/pages/quote'` + JSON
  template `page.oecm.json:108: "cta_primary_url": "/pages/quote"`).
  Live OECM page DOES link to /pages/quote. Not actually missing.

---

## Recommended fix batch (this session)

- **F-1**: Apply 1-line `tel:+15198371810` → `tel:+18008359565` in
  `theme/sections/ds-cs-base.liquid:593`. **DONE in Phase 6.**
- **W-1** (89 `tel:` format-consistency cases): deferred to post-launch
  backlog. Scoped: a single sed pass + 1 schema-default tweak. Not
  applied in INTERLINK-3 per scope ("if 20+ findings, halt and discuss").
- **W-2** (anchor-text inconsistencies): deferred. Most are by-design.
  /pages/oecm + /pages/brands worth a focused consolidation pass —
  candidate for an INTERLINK-4 session or AI-search post-launch tuning.
- **INFO HIGH × 15**: deferred to post-launch cross-link consolidation
  session. The 6 brand-page "back to brands hub" + 1 design-services
  "get a quote" gaps are highest-value adds.
- **INFO LOW × 3**: backlog.

After F-1 fix: **0 FAIL findings. INTERLINK-3 hard gate cleared for LAUNCH-2.**

---

## Out of scope (per prompt + observed)

- Schema work — closed by today's batch-fix (`c7cdb20`).
- Adding new cross-links beyond F-1 — flagged as INFO, requires separate review.
- Modifying page copy beyond link text — would require copy refresh session.
- 89 `tel:` format normalizations — deferred.
- Touching templates outside `bbi_landing` gate — none triggered.

---

## Verification artifacts

- Raw href extraction: `data/reports/interlink-3-evidence/all-links.json` (623 rows)
- Classified + validated: `data/reports/interlink-3-evidence/links-classified-v2.json`
- Cross-page anchor map: `data/reports/interlink-3-evidence/anchor-inconsistencies.json`
- Missing-link findings: `data/reports/interlink-3-evidence/missing-links-v2.json`
- Live page handles (Shopify Admin API): `data/reports/interlink-3-evidence/live-page-handles.txt`
- Live collection handles: `data/reports/interlink-3-evidence/live-collection-handles.txt`
- Scripts (reproducible): `data/reports/interlink-3-evidence/{extract-links,classify-v2,anchor-consistency,missing-links-v2,fetch-collections}.py`

---

## Sign-off

- ✅ 0 FAIL findings after F-1 fix
- ✅ All 23 canonical BBI pages confirmed published on live store
- ✅ All referenced `/collections/*` handles confirmed to exist
- ✅ Zero broken `/pages/*` or `/collections/*` links
- ✅ Hard gate met for LAUNCH-2 (per Step 26 INTERLINK-3 prompt)

INTERLINK-3 complete. Next: SYS-VERIFY-1 Phase 2 (Step 33) per Day 9
plan, then EOD Cowork.
