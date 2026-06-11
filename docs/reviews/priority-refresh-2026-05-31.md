# PHASE-C-STREAM-B — Priority Page Content Refresh REPORT

**Branch:** `feature/priority-page-content-refresh-2026-05-31`
**Date:** 2026-05-31
**Base SHA:** `adbdc54` (post PR #69 — ICP-KEYWORD-WALKTHROUGH session 1)
**Source of truth:** [`data/reference/priority-keywords.yaml`](../../data/reference/priority-keywords.yaml) v1 · [`docs/strategy/bbi-keyword-map-2026-05-31.md`](../strategy/bbi-keyword-map-2026-05-31.md)
**Scope (re-scoped by Leo at Phase 2):** SEO-meta-only — **no theme files touched.** On-page H1/intro/FAQ/CTA/link work on the 3 landing pages deferred to a follow-up theme-edit session.

---

## ═══ APPLICATION COVERAGE ═══

- **Surfaces updated:** 7 of 7 (spec said "8 pages" — actual scope is **7**: 1 hub + 2 spokes + 4 collections)
- **SEO title rewritten:** 7 / 7
- **Meta description rewritten:** 7 / 7
- **Collection description body added (FAQ + JSON-LD + internal links):** 1 (`reception-side-guest-chairs` — only default-template collection that renders `{{ collection.description }}`)
- **FAQPage JSON-LD added:** 1 page (waiting-room collection), 4 Q&A
- **Internal links added:** 2 (→ `/pages/healthcare`, → `/collections/reception`)
- **Landing-page body content (H1/intro/FAQ/CTA/links):** **DEFERRED** (theme-section content — out of scope this session)

---

## ═══ KEYWORD LANDING ANALYSIS ═══

| # | Surface | Cluster | Primary KW | Landed in title | Landed in meta | Body |
|---|---------|---------|------------|:---:|:---:|:---:|
| 1 | `/pages/design-services` | Design (hub) | office space planning | ✅ | ✅ | deferred |
| 2 | `/pages/professional-services` | Pro Services (spoke) | law firm office furniture | ✅ | ✅ | deferred |
| 3 | `/pages/healthcare` | Healthcare (spoke) | healthcare furniture canada | ✅ | ✅ | deferred |
| 4 | `/collections/reception` | Collections | reception desk | ✅ | ✅ | n/a (template) |
| 5 | `/collections/office-suites-desks` | Collections | executive desk | ✅ | ✅ | n/a (template) |
| 6 | `/collections/boardroom` | Collections | boardroom table / conference table | ✅ | ✅ | n/a (template) |
| 7 | `/collections/reception-side-guest-chairs` | Collections | office chairs for waiting room | ✅ | ✅ | ✅ FAQ+JSON-LD+links |

**Primary keyword landed in title + meta on 7 / 7 surfaces.** Titles ≤60ch, metas ≤160ch, brand = full "Brant Business Interiors" (no "BBI"), healthcare meta kept private-clinic-first.

### Final SEO copy written

| Surface | SEO title | Meta description |
|---|---|---|
| design-services | Office Space Planning \| Brant Business Interiors | Office space planning and office layout design for Ontario offices — free CAD floor plan with furniture placement, no obligation. Quote in 1 business day. |
| professional-services | Law Firm Office Furniture \| Brant Business Interiors | Office furniture for Ontario law firms, accounting, insurance & consulting practices — reception, executive & boardroom fit-outs. Canadian-owned since 1964. |
| healthcare | Healthcare Furniture Canada \| Brant Business Interiors | Healthcare furniture for Canadian medical and dental clinics — waiting room, exam, and reception furniture built for clinical use. Quote in 1 business day. |
| reception | Reception Desks \| Brant Business Interiors | Commercial reception desks for Ontario offices and clinics — L-shaped, modern, and small-footprint designs. Canadian supplier, OECM eligible, bulk quotes. |
| office-suites-desks | Executive Desks \| Brant Business Interiors | Executive desks and office suites for Ontario boardrooms and private offices — L-shaped, modern, and wood-finish designs. Canadian supplier, OECM eligible. |
| boardroom | Boardroom & Conference Tables \| Brant Business Interiors | Boardroom tables and conference tables for Ontario offices — solid wood, modular, and AV-ready designs with matching seating. OECM eligible, free CAD layout. |
| reception-side-guest-chairs | Waiting Room & Guest Chairs \| Brant Business Interiors | Office chairs for waiting rooms, reception, and clinic guest areas across Canada — durable side and guest seating for busy spaces. Bulk quotes available. |

---

## ═══ FAQ + AI OVERVIEW READINESS ═══

- **FAQPage JSON-LD added to:** `/collections/reception-side-guest-chairs` (4 Q&A) — validated live, coexists with existing collection/breadcrumb schema (4 JSON-LD blocks, no regression).
- **FAQ questions:** What chairs are best for a waiting room? · Are these chairs suitable for medical and dental clinics? · How many waiting room chairs do I need? · Do you offer bulk pricing on waiting room seating in Canada?
- **Fact-check correction (Leo's Phase 4 verdict on #7):** the draft "2.5–3 seats per exam room" ratio could **not** be verified against a credible healthcare-planning source (FGI moved seat ratios to an appendix; the verifiable standard is square-footage based, ~20 sq ft/person, and explicitly operational). Per instruction, softened to an operational heuristic ("1.5–2× peak concurrent appointments; our space-planning team will model this with you") in both the visible answer and the JSON-LD. No unverifiable claim shipped.

---

## ═══ INTERNAL LINKING ARCHITECTURE ═══

| Link | Status this session |
|---|---|
| Hub → spokes | ❌ deferred (theme content) |
| Hub → collections | ❌ deferred (theme content) |
| Spokes → hub (back-link) | ❌ deferred (theme content) |
| Spokes → collections | ❌ deferred (theme content) |
| Collections → spokes | ⚠️ partial — `reception-side-guest-chairs` → Healthcare spoke + Reception collection (the one collection whose template renders a description body) |

**Hub-and-spoke architecture structurally complete:** **NO** — full internal linking requires the deferred theme-content session (see Slug/Next Action below). Only the one default-template collection received body links this session.

---

## ═══ WORKFLOW FRICTION POINTS ═══

1. **BBI content model is NOT uniform (the big one — see operational lesson).** The 3 landing pages have **empty CMS `body`**; all visible content (H1/intro/FAQ/CTA/links) is hardcoded in theme Liquid sections (`ds-lp-*.liquid`), driven by `section.settings`, not CMS body or metafields. Only SEO title/meta (`global.title_tag` / `global.description_tag`) are editable without theme edits.
2. **YAML slugs ≠ reality.** Locked YAML slugs did not match the live store:
   - `/collections/reception-desks` — **does not exist** as a handle.
   - `/collections/boardroom-conference-tables` — **does not exist**.
   - `/collections/executive-desks` — exists but **0 products**.
   - `/collections/waiting-room-seating` — exists but **0 products**.
   - Remapped to nav-canonical, product-bearing handles: `reception` (3p), `office-suites-desks` (13p, executive), `boardroom` (25p), `reception-side-guest-chairs` (28p, waiting).
3. **Collection description rendering is template-dependent.** Only `ds-collection-base` (default `collection.json`) renders `{{ collection.description }}`. The `base`-suffix (`ds-cs-base`) and custom (`ds-cc-base`) sections do **not** — so body writes only surface on default-template collections. 3 of 4 funnel collections are SEO-meta-only as a result.
   - **⚠️ SUPERSEDED 2026-06-11 (Step 2.1):** the `ds-cs-base` claim no longer holds — Step 2.1 added an answer-first intro that renders `{{ collection.description }}` (above the grid) + a FAQ band, so `base`-suffix sub-collections now surface their body (enabling the Step 2.2 category-copy push). `ds-cc-base` remains description-less. True when written (pre-2.1); retained for history.
4. **Spec count off by one.** Spec header said "8 pages"; the enumerated scope is 7 surfaces.
5. **Pre-existing title truncation.** Several legacy SEO titles were stored cut mid-word at "...| Brant". New titles use the full "| Brant Business Interiors" within the 60-char budget.

---

## ═══ SLUG CHANGE FLAG ═══

**Design Services slug recommendation (`/pages/design-services` → `/pages/office-space-planning`):**
- **Not executed this session** per spec (slug changes need redirects + a separate session).
- Estimated effort: ~30 min in a follow-up including 301 redirect setup (note: redirects need `write_content` scope — see memory `reference_shopify_api`, currently a gap).
- Recommended timing: after the measurement window confirms the keyword strategy is landing.

---

## ═══ SAFETY STATE ═══

- **Theme check:** 2,833 offenses (2,043 err / 790 warn / 269 files) → **identical** after. Zero theme files touched. ✅ HELD.
- **Admin API writes:** 7 / 7 successful.
- **Readback verification:** 7 / 7 MATCH (hardened comparator: normalized SEO fields + body content/JSON-LD/link presence checks).
- **Storefront render (cache-busted):** 7 / 7 confirmed — new title + meta on all; FAQ body + valid FAQPage JSON-LD + both internal links on the waiting-room collection.
- **Snapshots:** 7 pre-write snapshots at `data/backups/priority-refresh-*-pre-20260531T224044.json` (gitignored).
- **Log:** `data/logs/priority-refresh-20260531T224044.log` (gitignored).
- **Git tracked changes:** none from the writes (live Shopify only). This report + the operational lesson are the committed audit record.
- **LIVE state:** 7 surfaces updated, all rendering correctly.

---

## ═══ NEXT ACTION ═══

1. **Leo reviews this PR and merges from GitHub** (no auto-merge).
2. **Recommended follow-up session — "Landing Page Theme Content Refresh":** update `ds-lp-design-services` / `ds-lp-professional-services` / `ds-lp-healthcare` section files (+ their `page.*.json` templates) to apply the locked priority keywords to **H1, intro, FAQ sections, CTAs ("Get My Free Layout →" → `#design-form`), and internal hub↔spoke↔collection links.** This requires theme edits → higher risk → needs its own preflight (incl. watcher gate), theme-dev QA, `/bbi-lp-audit`, and a review pass. This is what completes the hub-and-spoke internal-linking architecture.
3. Wait 7–14 days for Google to re-crawl.
4. Begin rank tracking via DataForSEO on `priority-keywords.yaml` v1 keywords.
5. Measure: which keywords moved, which pages gained sessions, which FAQ entries triggered featured snippets / AI Overview citations.
6. Walkthrough session 2 (remaining 4 clusters) can run in parallel — does not need measurement data first.
