# Wave E Execution Plan — BRAND-PAGES-1 → SEO-AUDIT-1 → PSI re-run

_Drafted 2026-05-20. Sequences the chain Steve handed off:_

> BRAND-PAGES-1 + A11Y bundle (substantial) ↓ AI-7 homepage copy ↓ AI-8 OECM page copy ↓ CONTENT-1 content polish ↓ AI-9 + AI-5 schema work ↓ SEO-AUDIT-1 (against near-final theme) ↓ A11Y Phase 1.5 PSI re-run

**Status: APPROVED — build handed to Claude Code (2026-05-20).** Cowork made no theme/Shopify changes. See `docs/plan/bbi-brand-pages-1-handoff-2026-05-20.md` for the Claude Code build brief.

**Decisions locked (2026-05-20):** (1) BRAND-PAGES-1 = **Approach A** (copy an existing per-brand section per new brand). (2) Global/Teknion = **Option A** (keep bundled, rename/expand to GFG-family). (3) CONTENT-1 logo = **lock `bbi-logo-v2`** (no schedule impact). (4) SEO-AUDIT-1 crawl access = still open; settle before Phase 6 (does not block Phases 1–5).

This was for sign-off. Source of truth for IDs/status is `BBI-Session-Kickoff/bbi-build-state.md` (Wave E). The ordering is sound: it front-loads all content/copy/schema so the SEO audit and PSI re-run land against a near-final theme, which is exactly what the "(against near-final theme)" annotation calls for.

---

## 1. The chain at a glance

| # | Link | Tracker ID(s) | Status today | Est. focused effort | Hard dependencies |
|---|---|---|---|---|---|
| 1 | BRAND-PAGES-1 + A11Y bundle | BRAND-PAGES-1 (new — not yet a tracker row), A11Y-AUDIT-1 | Both ⬜ | **7–9 h** + 2–3 h audit | brand:* tags (✅ done), 2 scope decisions |
| 2 | AI-7 homepage copy | AI-7 | ⬜ | 0.5–1 h | none (draft copy exists) |
| 3 | AI-8 OECM copy hardening | AI-8 | ⬜ | 2–3 h | none (draft copy + table spec exist) |
| 4 | CONTENT-1 content polish | CONTENT-1 | ⬜ 🔔 needs decision | 0.5 h (lock) **or** +1–2 days (source new) | logo decision |
| 5 | AI-9 + AI-5 schema work | AI-9, AI-5 | Both ⬜ | 6–8 h (AI-9) + ~1 h (AI-5) | AI-9 builds the FAQ snippet AI-5 reuses |
| 6 | SEO-AUDIT-1 (hard gate) | SEO-AUDIT-1 | ⬜ | 3–4 h once unblocked | **DataForSEO MCP + crawl access** (see §3), all of 1–5 |
| 7 | A11Y Phase 1.5 PSI re-run | PERF-AUDIT-1 (🟡), A11Y-AUDIT-1 delta | 🟡 / ⬜ | 1–2 h once unblocked | **crawl/preview access** (see §3), near-final theme |

**Rollup: ~22–30 focused hours ≈ 4–6 working sessions**, modulo the two blockers in §3 and the logo decision in §2.

---

## 2. Decisions needed from Steve

These gate or shape the work. The first three I'd like resolved before building; #4 is mid-chain but independent.

1. **BRAND-PAGES-1 build approach — Approach A vs B.** (Recommend **B.**)
   - **A:** copy an existing per-brand section per new brand, hardcode copy. ~30–45 min/page, but one more section file per brand and perpetuates the Google-Fonts duplication (DEBT-10).
   - **B (recommended):** build one generic `theme/sections/ds-lp-brand.liquid` driven by schema (brand name, tagline, intro rich-text, collection handle, repeatable H3 body blocks, sibling-brand links, OECM callout, testimonial). ~3–4 h upfront, then every future brand page is a template-JSON edit — no code push. Amortizes immediately given 3 new pages now and more later, and fixes the font-duplication issue. Matches the ugoburo two-tier pattern in `docs/strategy/competitor-audit-ugoburo.md` §3.

2. **Global / Teknion page — Option A vs B.** (Per `data/reports/brand-page-inventory-2026-05-12.md`.)
   - **A:** keep the existing `brands-global-teknion` page bundled, rename/expand to a GFG-family experience. Faster.
   - **B:** split into a standalone GFG page and defer Teknion (0 enriched, not callable). Cleaner canonical alignment, more work.
   - The existing page is healthy (56 products), so this is a copy/scope call, not a rebuild emergency.

3. **CONTENT-1 logo (also link #4).** 🔔 `bbi-logo-v2` is the *Brant Basics* wordmark, not a true BBI wordmark.
   - **Lock v2** as the answer → ~0.5 h, no schedule impact.
   - **Source/design a true "Brant Business Interiors" wordmark** → +1–2 days of content work. It does not block AI-9/AI-5/SEO-AUDIT technically, but it should be resolved before LAUNCH-0 since the logo is sitewide.

4. **SEO-AUDIT-1 crawl access** — see §3; needs a call on *how* the audit reaches the dev theme.

---

## 3. The two structural blockers (back half of the chain)

Both SEO-AUDIT-1 and the PSI re-run depend on a crawler reaching the BBI Landing **dev** theme (`186373570873`). Two problems:

**3a. DataForSEO MCP is not available in this session.** CLAUDE.md makes DataForSEO mandatory for SEO-AUDIT-1. It is not connected here and not in the connector registry to add. SEO-AUDIT-1 therefore has to run in the environment where the DataForSEO MCP is configured (Leo's Claude Code setup), or that MCP needs to be made available to this session first.

**3b. External crawlers can't see the dev theme.** Per the `PERF-AUDIT-1` note in the tracker, the dev-theme preview URL requires an authenticated admin browser session; external crawlers (DataForSEO's hosted crawler, the PageSpeed Insights API) can't reach `?preview_theme_id=…`. Candidate ways around it, for a decision:
   - **Run Lighthouse + axe/pa11y locally against `shopify theme dev` (localhost:9292).** Works for the PSI/Lighthouse re-run and the A11Y audit (rendered DOM, no external crawler). Does **not** help DataForSEO's hosted on-page crawl.
   - **Give DataForSEO a reachable URL:** temporarily lift the storefront password, or publish to an unlisted duplicate theme it can crawl with credentials, then run the on-page audit.
   - **Defer the full DataForSEO crawl to immediately post-LAUNCH-2** against `brantbusinessinteriors.com` (no preview param) — but SEO-AUDIT-1 is defined as a *pre-launch* hard gate, so this needs Steve's explicit waiver of the "before LAUNCH-0" condition.

**Implication for sequencing:** links 1–5 (all the building) are fully unblocked and can proceed now. Links 6–7 stall until 3a + 3b are resolved. I recommend we build 1–5, and in parallel get the audit access sorted so 6–7 can run the moment the theme is near-final.

---

## 4. Sequenced execution plan

Each phase ends with a verification gate (per CLAUDE.md: verify against the live dev DOM after every push, never trust 200/OK).

### Phase 1 — BRAND-PAGES-1 + A11Y bundle (the substantial one)

**1a. Generic brand section (if Approach B approved).** Build `theme/sections/ds-lp-brand.liquid` with the two-tier pattern from competitor-audit §3 / §"Step 25": hero intro rich-text (2 paras) → product grid (collection ref) → long-form H2 + repeatable H3-body blocks (max 8) → sibling-brand cross-link slot (5 brands from the canonical map) → **OECM-eligibility callout** (BBI edge — link to `/pages/oecm`) → 3–4 collection cross-link tiles → optional institutional testimonial. Add to the `bbi_landing` gate.

**1b. Three new brand pages** (templates only, if Approach B): `page.brands-otg.json` (54 products, highest priority), `page.brands-heartwood.json` (17), `page.brands-obusforme.json` (5). Copy sourced per brand; each cross-links `/pages/oecm`.

**1c. 24 brand×category smart collections** via Admin API (extend `scripts/create-smart-collections.py`, dry-run first per CLAUDE.md). Rule keys off `brand:*` tags, which now agree per product (APPLY-MAP-ADDITIONS ✅). These are the "View all" destinations from the brand hubs (catalog-navigability Option A hybrid).

**1d. Global/Teknion** rework per decision #2, and **update the Brands Hub** (`/pages/brands`) tiles to surface the new pages.

**1e. A11Y-AUDIT-1** — axe-core or pa11y CLI in the sandbox against the top 10 pages (preferably via localhost:9292 to dodge the preview-auth issue). Hard fails: missing alt text, unlabeled form inputs, contrast < 4.5:1, broken focus traps, keyboard gaps. Output per-page issue list to `data/reports/a11y-audit-2026-05-2x.csv`, fix block-level issues, re-check.

> **Note on bundling:** the WCAG audit at the front catches component-level issues in *existing* chrome (good). But AI-9 introduces a new interactive FAQ accordion — plan a small a11y delta-check on that component after Phase 5 rather than assuming Phase 1's audit covers it.

**Gate:** new brand pages return 200 on dev theme with correct breadcrumb + product grid + OECM callout; smart collections populated; a11y block issues resolved. New tracker row `BRAND-PAGES-1` + update `A11Y-AUDIT-1`.

### Phase 2 — AI-7 homepage entity copy
First ~200 words on `/` answering who/what/who-served/where + OECM. Draft already written in competitor-audit §5 (the "Since 1964…" 60-word opener). Place in the homepage hero/intro section (`templates/index.json`). **Gate:** view-source the first paragraph, confirm OECM + Agreement 2025-470 + ICP + geography present.

### Phase 3 — AI-8 OECM copy hardening
On `/pages/oecm` (`theme/sections/ds-lp-oecm.liquid`): (1) pain-point opener; (2) service-channel inventory (quote in 1 business day, free design layout, Ontario install, PO-friendly billing, OECM-compliant invoicing); (3) **OECM 2025-470 coverage table** (manufacturer × category × brands), mirroring the ugoburo NMSO pattern. All drafted in competitor-audit §"Step 18". This is the highest-leverage AI-citation page. **Gate:** table renders, copy live on dev, no TBD/lorem.

### Phase 4 — CONTENT-1 logo
Resolve decision #3. If "lock v2": finalize `data/logos/bbi-logo-final.png`, confirm sitewide. If "source new": that's a separate 1–2 day content track — flag it as forking off here so it doesn't block Phase 5.

### Phase 5 — AI-9 + AI-5 schema
**AI-9:** build a reusable `theme/snippets/bbi-faq.liquid` (accessible accordion + FAQPage JSON-LD), then 3–5 institutional-buyer Q&As per the 9 category pages (rendered via `ds-cc-base`). Question topics drafted in competitor-audit §4/§"Step 19" (OECM ordering, bulk discounts for boards/municipalities, lead times, install cities, warranty). **AI-5:** reuse the same snippet to add FAQPage schema to `/pages/oecm` and Design Services (`ds-lp-design-services`). **Note:** AI-5's "top blog posts" target doesn't exist yet (blog is post-launch backlog), so AI-5 reduces to OECM + Design Services for now. **Gate:** Rich Results Test (or local JSON-LD validation) passes FAQPage on each surface; accordion keyboard-accessible (the a11y delta-check).

### Phase 6 — SEO-AUDIT-1 (HARD GATE) — blocked until §3 resolved
Once DataForSEO access + crawl access are sorted: crawl every `bbi_landing` page; verify meta titles/descriptions in-range, one H1/page with no skipped levels, all schema validates (Organization ✅, Product, BreadcrumbList ✅, FAQPage new), canonicals resolve, no broken internal links, Lighthouse mobile ≥ 80, CWV pass on top 5 templates (home, OECM, quote, industries hub, healthcare). Output `data/reports/seo-audit-<date>.json` + `docs/reviews/seo-audit-<date>.md` with per-issue severity. **All `block` items resolved or explicitly waived before LAUNCH-0.**

### Phase 7 — A11Y Phase 1.5 PSI re-run — blocked until §3 resolved
Re-run PageSpeed Insights / Lighthouse against the near-final theme (Phase 1 ran against the live Avada theme — 10/10 fail — which is what we're replacing). Best done via localhost:9292 for an interim read; the authoritative run is still PERF-AUDIT-1 Phase 2 post-LAUNCH-2. Re-check the AI-9 FAQ accordion for a11y regressions. Update `PERF-AUDIT-1` evidence.

---

## 5. What can run in parallel

- **Phases 2 (AI-7) and 3 (AI-8) are pure copy** with drafts already written — they can run alongside Phase 1's brand-page build without contention.
- **CONTENT-1 (Phase 4)** is a fully independent decision/asset task — resolve it anytime; only the "source new wordmark" branch adds calendar time.
- **Audit-access setup (§3)** should proceed in parallel with all building so Phases 6–7 aren't waiting on it.
- **Strictly serial:** AI-9 → AI-5 (shared snippet), and everything → SEO-AUDIT-1 → PSI re-run.

---

## 6. Open risks

- **SEO-AUDIT-1 access (§3b)** is the biggest schedule risk — it's a hard launch gate that currently has no clean path to crawl the dev theme. Needs a decision early, not at Phase 6.
- **DataForSEO availability (§3a)** — if it can't be made available to this session, Phase 6 must run in Leo's Claude Code environment.
- **Meta-copy rule:** if any phase changes meta titles/descriptions site-wide, CLAUDE.md gates that behind a DataForSEO step. AI-7/8/9 add body/FAQ copy (not site-wide meta), so they're clear — but flag any meta edits.
- **Calendar-critical path** (from the launch-readiness notes): GSC DNS verification has a 5–14 day async clock and sits in Phase 4 of the master plan — worth starting regardless of this chain.

---

## 7. Recommended immediate next step

Approve **Approach B** (decision #1) and **Option A or B** for Global/Teknion (decision #2), give the **logo** call (decision #3), and pick a **SEO-AUDIT-1 access** path (decision #4). With those four answers I can start Phase 1 (BRAND-PAGES-1 + A11Y) immediately and run Phases 2–3 copy in parallel, leaving only Phases 6–7 gated on audit access.
