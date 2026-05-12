# BBI Launch Readiness Plan
**Created:** 2026-05-08
**Owner:** Leo + Steve
**Dev theme:** BBI Landing Dev (186373570873) — never publish to live until LAUNCH-2
**Live theme:** brantbusinessinteriors.com (production — untouched until LAUNCH-2)

---

## Premise

The May 7 remediation plan (`design-system-remediation-2026-05-07.md`) scoped Stages 0–8 to address chrome drift, routability failures, design-system parity, and process hardening. As of 2026-05-08:

- Stages 0–2 are complete (chrome stabilized, worktree reconciled, Wave C pages published)
- Stage 3 (T3 hub layout) is complete (`ds-cc-base.liquid` refactored, 9 category hubs live)
- Stage 3.2/3.2c (T4 sub-collection layout + canonical handle migration) is complete
- Stage 4a (PDP recon) is complete — greenfield build plan documented
- Stage 4b-RECOVER is merged to main (tag: `v1.5-stage-4b-recover`)
- Stage 4b (actual PDP build) has NOT started
- Stages 5–8 (PDPs, shop-all, re-verify, process lock) are NOT started

What remains is **launch hardening**: building the 4 missing templates, creating 14 smart collections, completing Wave E (SEO/hardening), and executing the launch sequence. This plan replaces Stage 5–8 of the May 7 plan with a concrete sequenced phase model tied to the Wave taxonomy in `bbi-build-state.md`.

---

## What's done (verified)

### TABLE A — May 7 Remediation Plan stages

| Stage | Name | Status | Evidence | Note |
|---|---|---|---|---|
| 0 | Freeze and measure | ✅ | `stage-0-summary-2026-05-07.md` | Route audit, visual baseline, page record audit, row truth pass |
| 1 | P0 reconcile worktree ↔ dev theme | ✅ | `chore/reconcile-dev-theme-2026-05-07` (merged) | 20 dev-only files pulled; theme.liquid reconciled |
| 1.5 | P0 sub-collection 404s | ✅ | `chore/resolve-internal-404s-2026-05-07` (merged) | 68/68 sub-collections verified |
| 1.6 | P0 JSON template link audit | ✅ | `chore/json-template-link-audit-2026-05-07` (merged) | |
| 2 | P0 chrome stabilization | ✅ | `chore/stabilize-chrome-2026-05-07` (merged) | Crumbs snippet, header/footer parity |
| 2.6 | Customer Stories footer | ✅ | commit `d22589c` | CSS alignment |
| 2.7 | White-on-white chrome fix | ✅ | commit `c86eb55` | Dark background on scheme-inverse closers |
| 3.0 | Design tokens rollout | ✅ | `feature/stage-3.0-design-tokens` (merged) | OECM badge, logo v2 |
| 3.1a | Hub gap analysis + T3 spec | ✅ | `stage-3.1a-*.md` | Hub audit + tag census |
| 3.1b | T3 hub layout refactor | ✅ | `feature/stage-3.1b-hub-t3-layout` (merged) | ds-cc-base T3 redesign |
| 3.1c.1 | Hero stats + pill counts | ✅ | `feature/stage-3.1c.1-hero-stats-and-counts` (merged) | |
| 3.1d | Empty hub smart-rule fix | ✅ | `chore/stage-3.1d-empty-hub-rules` (merged) | |
| 3.2 | T4 sub-collection refactor | ✅ | `feature/stage-3.2b-subcollection-t4` (merged) | ds-cs-base redesign |
| 3.2c | Canonical handle migration | ✅ | `chore/stage-3.2c-subcollection-migration` (merged) | 62 sub-collections flipped to template_suffix=base |
| 3.2 polish | Equal-height product cards | ✅ | `chore/stage-3.2-tile-height-polish` (merged) | |
| 4a | PDP recon | ✅ | `stage-4a-*.md` artifacts | Greenfield build plan documented |
| 4b-RECOVER | Desks hub retarget + 3 re-publishes | ✅ | commit `c64936c`, tag `v1.5-stage-4b-recover` | Merged to main |
| 4b (PDP build) | Build ds-pdp-base.liquid | ⬜ | Not started | Largest remaining build item |
| 5–8 | Re-verify, process lock, etc. | ⬜ | Not started | Replaced by Phase plan below |

### TABLE B — BBI Build State Wave status

| Wave | Goal | Status | Key gaps |
|---|---|---|---|
| **Track D (DS-0→DS-4)** | Design system foundation | ✅ Complete | — |
| **Phase 1b (Hero 100)** | Product enrichment | ✅ Complete | — |
| **AI Search (AI-1/2/12)** | llms.txt, robots.txt, readability script | ✅ Done | AI-4..AI-9 ⬜ (Wave E) |
| **Wave A** | Foundations + Phase 2 shop structure | ✅ Complete | — |
| **Wave B** | Sub-collection template rollout + smart collections | ✅ Complete | — |
| **Wave C** | Trust pages (Brands, About, Contact, etc.) | 🟡 Section files exist, Page records need API verification | B-8 |
| **Wave D** | SEO foundation | 🟡 W0-3 pending Admin upload | W0-1 GSC/GA4 ⬜ BLOCK |
| **Wave G** | PDP + system templates | ⬜ Not started | Largest remaining work |
| **Wave E** | Pre-launch hardening | ⬜ Not started | Hard gates: SEO-AUDIT-1, DS-VERIFY |
| **Wave F** | Launch | ⬜ Not started | LAUNCH-0 → LAUNCH-2 |

---

## What's left

### Wave C carryover (B-8)
- Verify 10 Shopify Page records + published status via Admin API
- Handles: about, brands, brands-keilhauer, brands-global-teknion, brands-ergocentric, our-work, contact, delivery, relocation, customer-stories

### Wave D carryover
- W0-1: GSC + GA4 setup (BLOCK — start async)
- W0-3: Upload redirect CSVs (ready to go)
- W0-2: Google Business Profile (FIX)

### Wave G (all ⬜)
- PB-PDP-1: Confirm gate already done ✓ (stage-4a-decision.md §1)
- PDP-1: Build `ds-pdp-base.liquid` + `product.json` (largest item, ~6h)
- PDP-2: Product JSON-LD (`bbi-product-jsonld.liquid`)
- PDP-3: Smoke test 5 product states
- CS-1: Customer Stories page (template + section exist; Shopify Page record + content)
- 404-1: Custom 404 template + section
- SMART-1: 14 smart collections (10 view-all + 4 brand-filtered)
- BLOG-TPL-1: Blog + Article templates (shells)

### Wave E (all ⬜)
- AI-4: Organization schema on homepage (confirm it fires via nav-wrap)
- AI-6: BreadcrumbList JSON-LD shared snippet
- AI-7: Entity-clarity copy on homepage
- AI-8: OECM page copy hardening
- AI-9: FAQ blocks on 9 category pages
- AI-5: FAQ schema on OECM/Design Services
- LEAD-INBOX-1: Steve provisions 3 email inboxes (hard prereq for LEAD-3)
- LEAD-3: RFQ modal (after LEAD-INBOX-1)
- INTERLINK-3: Final cross-link audit
- SEO-AUDIT-1: DataForSEO MCP crawl (HARD GATE)
- DS-VERIFY: Design system visual verification
- IMG-PHASE2: Product image regen (soft gate)
- PERF-AUDIT-1: Lighthouse + Core Web Vitals
- A11Y-AUDIT-1: WCAG 2.1 AA audit
- LINK-ROT-1: Internal + external link sweep
- SYS-VERIFY-1: System pages chrome verification
- NAV-VERIFY: Nav renders on collection + homepage
- CONTENT-1: Finalize BBI logo

---

## New items added 2026-05-08

| Item | Severity | Notes |
|---|---|---|
| **Variant picker bug** | BLOCK | Non-colour variants render as borderless text; colour swatches are text labels. Fix inside Stage 4b. |
| **RFQ modal DS treatment** | FIX | No `<dialog>` modal exists. `/pages/quote` works as fallback. Blocked on LEAD-INBOX-1 Steve action. |
| **Cart page rebuild** | FIX | `/cart` uses Starlite. Per architecture intent; flag for Steve awareness. Can defer post-launch. |
| **Image integrity (3 re-published products)** | FIX | Visual QA needed on willow-bariatric-chair, solid-steel-shelving-starter-set, monitor-arms during Stage 4b smoke test. |
| **Blog + Article templates** | FIX | Shell templates needed before launch for chrome consistency and SEO foundation. Zero posts required at launch. |
| **Measurable DS verification tooling** | Process | `scripts/capture-bbi-baselines.py` + `scripts/diff-bbi-baselines.py` created this session. Add to Definition of Done. |
| **Locked Tn reference library** | Process | `docs/strategy/locked-references/` created. T4/T5/Cart/404/Blog/Article refs not yet locked. |
| **Process: every phase ends with merge to main** | Process | Each phase produces a merge commit + semver tag before Phase N+1 starts. |

---

## Sequenced phases (Phase 0 → Phase 8)

### Phase 0 — Cleanup + baseline (DONE this session)
**Scope:** Branch hygiene, products export, CLI verification, guard file, baseline scripts.
**Exit criteria:** `main` is clean, no stale merged branches, baseline scripts exist.
**Duration:** Completed 2026-05-08.
**Merge:** Already on main.

---

### Phase 1 — Wave C verification (next session)
**Scope:** Admin API pass to verify 10 Wave C Shopify Page records + published status. Zero theme changes.
**Exit criteria:** All 10 handles confirmed published=true with correct template_suffix. Any 404s resolved.
**Duration:** 0.5 dev day.
**Dependencies:** None.
**Prompt sketch:** "Read docs/plan/bbi-build-state.md Wave C rows. Use Shopify Admin API to GET /pages.json. For each of the 10 Wave C handles, confirm published + template_suffix. Report pass/fail. Fix any that are wrong. Mark ✅ in bbi-build-state.md."
**Merge:** `chore/phase-1-wave-c-verify` → main + tag `v1.6-phase-1`.

---

### Phase 2 — Wave G: Templates + smart collections (largest phase)
**Scope:** Stage 4b PDP build, 404 template, blog templates, SMART-1 smart collection creation.
**Exit criteria:**
- `ds-pdp-base.liquid` + `product.json` passes 5-state smoke test (PDP-3)
- Product JSON-LD validates on 3 PDPs (Rich Results Test)
- Visual swatch variant picker renders correct colours on a test product
- `404.json` + `ds-system-404.liquid` renders BBI chrome
- `blog.json` + `article.json` render BBI chrome (empty blog OK)
- 14 smart collections created + non-zero product counts confirmed
- T5 locked reference captured (`capture-bbi-baselines.py --lock`)
**Duration:** 4–5 dev days.
**Dependencies:** Phase 1 complete (Wave C pages confirmed live).
**Prompt sketch:** "Work through Wave G rows in bbi-build-state.md in order. Start with SMART-1 (fastest win, unblocks hub CTAs). Then 404-1 + BLOG-TPL-1 (parallel). Then Stage 4b (PDP-1 + PDP-2 + PDP-3). Smoke test after each. Lock T5 screenshot after Steve QA."
**Merge:** `feature/phase-2-wave-g` → main + tag `v2.0-phase-2`.

---

### Phase 3 — Wave E partial: polish + redirect + tooling
**Scope:** AI-6 BreadcrumbList, INTERLINK-3 audit, redirect CSV uploads, cart "Continue shopping" fix, T4 locked reference, FAQ schema on category pages, SYS-VERIFY-1.
**Exit criteria:**
- BreadcrumbList JSON-LD renders on sub-collection + PDP pages
- INTERLINK-3 returns 0 failures
- All 3 redirect CSVs uploaded (with willow-bariatric-chair row resolved)
- Cart empty-state routes to `/collections/business-furniture`
- T4 locked reference captured
- FAQ blocks on 9 category hubs
- SYS-VERIFY-1 passes (no chrome leak in system pages)
**Duration:** 2–3 dev days.
**Dependencies:** Phase 2 complete.
**Prompt sketch:** "Work through Wave E AI-* and verification rows. Start with AI-6 BreadcrumbList (used by multiple templates). Then run INTERLINK-3. Upload redirect CSVs. Run SYS-VERIFY-1 DOM check. Capture T4 baseline screenshot with Steve sign-off."
**Merge:** `chore/phase-3-wave-e-polish` → main + tag `v2.1-phase-3`.

---

### Phase 4 — GSC/GA4 + content gates (Steve actions required)
**Scope:** GSC + GA4 setup (B-5), policy pages content (B-9), LEAD-INBOX-1 email provisioning (F-10), CONTENT-1 logo decision, optional: W0-2 Google Business Profile.
**Exit criteria:**
- GSC property created + DNS TXT verification record added (starts async clock)
- GA4 snippet deployed to theme.liquid
- Privacy Policy, Terms of Service, Refund Policy, Shipping Policy filled in via Admin
- Steve confirms LEAD-INBOX-1 email addresses provisioned + test receipt confirmed
- CONTENT-1 decision made (lock bbi-logo-v2 as current answer)
**Duration:** 1 dev day (Claude Code side) + Steve setup time.
**Dependencies:** Phase 3 complete. GSC verification starts here and runs async — does NOT block Phase 5 or Phase 6. Only blocks Phase 7 LAUNCH-3.
**NOTE:** Start GSC DNS verification at Phase 4 kickoff. Can take 5–14 calendar days. Everything else runs in parallel.
**Prompt sketch:** "Create GA4 property. Add gtag snippet to theme.liquid (inside <head> via bbi-nav-wrap or layout). Steve: add DNS TXT record for GSC, fill in policy pages via Admin, confirm email provisioning. Report back when TXT record is live."
**Merge:** `chore/phase-4-analytics-content` → main + tag `v2.2-phase-4`.

---

### Phase 5 — SEO-AUDIT-1 (DataForSEO MCP — HARD GATE)
**Scope:** Run the mandatory DataForSEO technical SEO audit per CLAUDE.md. Resolve all block-severity issues. Produce `docs/reviews/seo-audit-2026-05-*.md`.
**Exit criteria:**
- DataForSEO `on_page_instant_pages` crawl run against dev theme preview URL
- All pages in `bbi_landing` gate audited
- Per-page issue list produced with severity (block / fix / waive)
- All `block` items resolved or waived in the review doc
- `SEO-AUDIT-1` row in Wave E marked ✅
**Duration:** 1 dev day (crawl + triage + fixes).
**Dependencies:** Phase 2 complete (PDPs + blog templates deployed — otherwise partial crawl). Can start in parallel with Phase 4.
**NOTE:** Phase 5 and Phase 4 can run concurrently. Phase 5 is async to GSC verification. Only GSC verification status blocks Phase 7.
**Prompt sketch:** "Run DataForSEO MCP on_page_instant_pages against the BBI Landing Dev preview URL. Crawl all bbi_landing pages. For each: check meta title/description, H1, schema (Organization, Product, BreadcrumbList, FAQ), canonical, broken links. Output to docs/reviews/seo-audit-<date>.md. Block items must be fixed before launch."
**Merge:** `chore/phase-5-seo-audit` → main + tag `v2.3-phase-5`.

---

### Phase 6 — Wave E final: PERF + A11Y + DS-VERIFY + VISUAL-COMP + IMG + MOBILE
**Scope:** Lighthouse + Core Web Vitals on top 10 pages (PERF-AUDIT-1), WCAG 2.1 AA audit (A11Y-AUDIT-1), design-system visual verification (DS-VERIFY), visual component comp audit (VISUAL-COMP), image coverage audit + waiver CSV (IMG-PHASE2), mobile-responsive verification at 375px on the 5 priority pages from audit 4.10 (homepage, seating hub, highback-seating sub-collection, healthcare industry, quote).
**Exit criteria:**
- Mobile Lighthouse ≥ 80 on all top 10 pages, or waived with documented reason
- A11Y hard fails resolved (missing alt text, broken focus traps, contrast fails)
- DS-VERIFY: brand-red unified, tokens intact, no dark-mode blocks
- VISUAL-COMP: every page opened on dev theme URL and eyeballed against `data/design-photos/components-v1-2026-04-27/Components.html`; any section whose layout, card treatment, or CTA styling materially differs from the comp is documented and fixed in this phase
- IMG-PHASE2: ≥80% product image coverage OR waiver CSV produced
- All 5 priority pages from audit 4.10 pass manual mobile review at 375px (no horizontal scroll, single bbi-header, hamburger nav functional, footer collapses to single column)
**Duration:** 2.5–3 dev days.
**Dependencies:** Phase 5 complete.
**Prompt sketch:** "Run scripts/capture-bbi-baselines.py on all pages. Run Lighthouse CLI or DataForSEO MCP lighthouse tool on top 10 pages. Run pa11y CLI on same 10 pages. Fix hard fails. Check color tokens in style-variables.liquid against design-system.md. Open each ds-lp-*.liquid page on the dev theme URL and compare against Components.html — document any layout/card/CTA mismatches and fix. Run capture-bbi-baselines.py at 375px viewport on the 5 priority pages from audit 4.10. Manual review against the checklist in that audit doc. Document any mobile-only breaks."
**Merge:** `chore/phase-6-hardening` → main + tag `v2.4-phase-6`.

---

### Phase 7 — LAUNCH-0 → LAUNCH-2 (go/no-go gate)
**Scope:** Image confirmation gate (Steve review), pre-publish GO/NO-GO report, manual publish.
**Exit criteria:**
- `LAUNCH-0`: Steve personally reviews `data/reports/page-images-audit-<date>.csv` and approves/rejects each row
- `LAUNCH-1`: GO/NO-GO report green (4 critical URLs return 200, no TBD/lorem, screenshots saved)
- `LAUNCH-2`: Steve manually publishes BBI Landing Dev → live in Shopify Admin
- GSC verification confirmed (DNS TXT validated by Google) — ONLY this step requires GSC
**Dependencies:** Phase 6 complete. GSC verification confirmed (started Phase 4).
**NOTE:** If GSC is still pending at Phase 7 completion, launch can proceed for Phase 7 steps 1-2. LAUNCH-3 (sitemap resubmission) requires GSC to be active.
**Prompt sketch:** "Generate page-images-audit CSV for Steve's review. Then run LAUNCH-1 pre-publish check: GET 4 critical URLs, assert 200, no lorem. Save screenshots to data/reports/. Output GO/NO-GO report. Steve: click Publish in Shopify Admin."
**Merge:** No merge — this is the publish step.

---

### Phase 8 — LAUNCH-3: Post-publish monitoring
**Scope:** Resubmit sitemap to GSC (requires GSC verified), monitor 404s for 72h (GA4 + any 404 in server logs), mobile smoke test across 5 browsers.
**Exit criteria:**
- Sitemap submitted to GSC
- No new 404s in first 72 hours (or all flagged + redirects added)
- LAUNCH-4 mobile smoke test screenshots saved
**Duration:** 0.5 dev day upfront + 72h monitoring.
**Dependencies:** Phase 7 complete + GSC verified.
**Prompt sketch:** "Submit https://brantbusinessinteriors.com/sitemap.xml to GSC. Set up a 404 monitor (Shopify analytics + GSC coverage report). Run capture-bbi-baselines.py at 375px on 5 pages. Save screenshots to data/reports/launch-mobile-smoke-<date>/."

---

## What stays untouched

These items from the May 7 plan are NOT reworked — they are good scaffolding:

- `scripts/migrate-to-smart-collections.py` + SMART-1 plan — works as designed
- `scripts/set-sub-collection-suffix.py` + P3-rollout — correctly set on 62 sub-collections
- `bbi-nav.liquid` / `bbi-footer.liquid` — exist; parity hardening done in Stage 2
- Section files for all Wave C pages — Liquid parses; design fidelity is the issue, not structure
- `ds-pdp-base.liquid` build plan (Stage 4a artifacts) — spec complete, build starting Phase 2
- `data/specs/` spec JSON for 93 Hero products — data ready for push in Stage 4b

---

## Definition of Done (per phase — hard gate)

A phase is done when ALL of the following are true:
1. All rows targeted by the phase are ✅ in `bbi-build-state.md`
2. Every new page: `document.querySelectorAll('.bbi-header').length === 1`
3. Every new page: `document.querySelectorAll('.bbi-footer').length === 1`
4. No `.shopify-section-group-header-group` in DOM on any BBI page
5. Visual diff vs locked Tn reference ≤ 5% delta on the relevant template (tooling: `diff-bbi-baselines.py`)
6. Active nav state correct on rendered pages
7. Every `<a href>` on new/changed pages resolves to 200
8. Shopify Page record exists with correct `template_suffix` for each new page
9. (PDPs only) Spec metafields populated and spec table renders
10. Before/after screenshots attached to merge commit or PR body
11. Branch merged to main + semver tag applied

---

## Known launch risks

| Risk | Severity | Mitigation |
|---|---|---|
| Stage 4b PDP build scope creep (variant picker, brand block, spec table all in one section) | HIGH | Time-box at 6 hours. Ship working PDP first; iterate on brand block + spec styling in Phase 3. |
| GSC DNS verification delay (5–14 days) | HIGH | Start Phase 4 immediately. This is the calendar critical path. All dev work proceeds regardless. |
| Wave C Page records missing or wrong suffix | MEDIUM | Phase 1 API check resolves this in 0.5 day. |
| SMART-1 product counts too low for some collections (ergonomic 16, quiet-spaces 9) | MEDIUM | Tag-based rule migration for title-match collections before smart collection creation. |
| Policy page content not ready (Steve writes) | MEDIUM | Draft PIPEDA/CASL-compliant copy for Steve's review — unblock the content dependency. |
| LEAD-INBOX-1 email provisioning delayed (Steve action) | LOW | LEAD-3 RFQ modal deferred anyway. `/pages/quote` is functional fallback. |
| Sub-collection handle rename redirects missing | LOW | Stage 3.2c migration CSV exists. Generate + upload redirect CSV in Phase 3. |
| IMG-PHASE2 below 80% coverage | LOW | Soft gate — waiver CSV acceptable. |

---

## Path to launch (compact)

```
Today             Phase 0 complete (this session)
                  ↓
Session 2         Phase 1 — Wave C Page record API verification (0.5 day)
                  ↓
Sessions 3–6      Phase 2 — Wave G: PDP + 404 + Blog + SMART-1 (4–5 days)
                  ↓
Sessions 7–9      Phase 3 — Wave E polish: BreadcrumbList, INTERLINK-3, redirects (2–3 days)
                  ↓
Session 10        Phase 4 — Steve: GSC DNS + policy pages + email inboxes (1 day + async clock)
                  ← GSC verification running async (5–14 calendar days) →
Session 11        Phase 5 — SEO-AUDIT-1 DataForSEO crawl (1 day, parallel to Phase 4)
                  ↓
Sessions 12–14    Phase 6 — Lighthouse + A11Y + DS-VERIFY + VISUAL-COMP + IMG + MOBILE (2.5–3 days)
                  ↓
Session 14        Phase 7 — LAUNCH-0 → LAUNCH-1 → LAUNCH-2 (requires GSC confirmed)
                  ↓
Post-launch       Phase 8 — LAUNCH-3 + 72h monitoring
```

**8–10 working days of dev. Calendar timeline: 2.5–3 weeks from today (dominated by GSC DNS verification async window).**
