# BBI Build State — Single Source of Truth

**Last updated:** 2026-05-06
**Dev theme:** BBI Landing Dev (`186373570873`) — never publish to live until LAUNCH-2
**Live theme:** brantbusinessinteriors.com (production — untouched)
**Replaces:** the status sections in `shopify-fix-plan.md` and the localStorage-bound `SEEDS` in `website-fix-checklist.html`

---

## How to use this file

Every wave below is a phase of work. Every row is a single piece of buildable scope with a stable ID. Status reflects **git + filesystem reality**, not intent. When you ship something, update its row in this file in the same commit. When the row says ✅ but the evidence is missing or 404, the row is wrong — fix the file before continuing.

**Status legend**

| | Meaning |
|---|---|
| ✅ | Done — committed, deployed, verified |
| 🟡 | Partial — some progress, named gap remaining |
| 🔄 | In progress — actively being worked |
| 🚧 | Blocked — waiting on a named prereq |
| ⬜ | Not started |

**Evidence column** — where to look to confirm the row is true. Either a git SHA, a file path, a Shopify URL, or a script output.

---

## How to drive this with Claude Code (prompts)

**You don't paste the markdown into every prompt.** The pattern is: reference the row ID, let Claude Code read the file. CLAUDE.md points it to these docs already, so the project context loads them on session start.

### Self-driving mode — one prompt per session (RECOMMENDED)

Paste this once at the start of a Claude Code session and let it run:

```
Standing instruction — work through Wave A of docs/plan/bbi-build-state.md
in order. For each ⬜ row:

  1. Sync this worktree first: git fetch origin && git merge origin/main
  2. Read the row's Notes column in bbi-build-state.md.
  3. If Notes contains 🔔 NEEDS DECISION → halt, ask me the question, wait.
  4. Otherwise: propose a brief plan (≤5 bullets), wait for "go" or "skip",
     then build, test, commit. Mark the row ✅ with the commit SHA in the
     same commit. Push.
  5. Continue to the next ⬜ row.

Stop and report when:
  - Wave A is complete (all rows ✅)
  - A row has a 🔔 NEEDS DECISION marker
  - A row blocks on an outside dependency (Leo's manual setup, etc.)
  - A test/audit fails

When stopping, print exactly the next prompt I should send to resume.

Start now with the first ⬜ row in Wave A.
```

That's the entire prompt. Claude Code reads `bbi-build-state.md`, picks the next row, proposes, builds, marks done, loops. You only re-engage when it hits a 🔔 row or fails.

### 🔔 NEEDS DECISION markers (rows that always halt for input)

These rows have explicit decisions only you can make. Claude Code halts before starting them:

- **NAV-1** — 🔔 5-item nav (`Shop Furniture · Industries · Brands · Services · About`) or 6-item nav (current landing-page rendering)?
- **PB-13** — 🔔 `brand-dealer` — merge from separate branch or de-gate?
- **CONTENT-1** — 🔔 BBI logo — lock `bbi-logo-v2` (Brant Basics wordmark) or source a true BBI wordmark?
- **LEAD-1** — 🔔 needs your input on which inbox each CTA currently routes to before audit
- **LEAD-3** — 🔔 single inbox to consolidate on (sales@brantbusinessinteriors.com or other?)
- **LAUNCH-0** — 🔔 you must personally review the image-approval CSV before LAUNCH-1 can run
- **LAUNCH-2** — 🔔 manual publish click — never automated

### Per-row prompts (if you prefer to drive manually)

**Common prompt shapes:**

| Goal | Prompt |
|---|---|
| **Resume** (most common) | `Continue Wave A — standing instruction.` (Claude Code already has the standing instruction in session memory; this resumes the loop after a 🔔 halt.) |
| Start the next task fresh | `What's the next ⬜ row in Wave A? Read docs/plan/bbi-build-state.md, propose how to start, wait for confirm.` |
| Build a specific row | `Work on PB-12 — read its row in docs/plan/bbi-build-state.md, propose the implementation, then build. Mark ✅ with SHA in the same commit.` |
| Build a Phase 2 page | `/bbi-build-page seating — see BUILD-STATE row P2-2 and INTERLINKING row /collections/seating.` |
| Run an audit | `Run the 12-point check from docs/plan/bbi-interlinking-map.md against /pages/healthcare. Report pass/fail per point.` |
| Drift-check a page | `Compare live /pages/quote on dev theme 186373570873 to theme/sections/ds-lp-quote.liquid in this worktree. Report any drift.` |
| Status snapshot | `Read docs/plan/bbi-build-state.md and tell me: what's done, what's blocked, what's next. Bullet form, under 200 words.` |

**The key idea:** Claude Code reads the source-of-truth markdown each time. You give it the row ID. It looks up the row, reads its notes/evidence, and acts. When work is done, it edits the row in the same commit as the code change. The Cowork artifact then auto-reflects the new status on next reload.

**For the `/bbi-build-page` skill specifically** — once SKILL-1 is done, every page build prompt becomes one line:

```
/bbi-build-page <slug>
```

The skill reads `bbi-build-state.md` for the row's brief, `bbi-interlinking-map.md` for the page's expected outbound/inbound links, runs all 12 audit points before marking done, and refuses to commit if any check fails. No need to paste guidance into the prompt — the skill is the guidance.

**Files Claude Code should always have in context** (already in CLAUDE.md):

- `docs/plan/bbi-build-state.md` — what to do
- `docs/plan/bbi-interlinking-map.md` — how to verify pages are wired
- `docs/strategy/design-system.md` — token + component spec
- `docs/strategy/icp.md` — voice + audience
- CLAUDE.md itself — project rules, BBI-specific guardrails

---

## Lessons Learned — read before building any new page

Four deploy-error patterns recurred during P1 builds. The `/bbi-build-page` skill must enforce all four (see SKILL-1).

1. **Page must be in the `bbi_landing` gate.** Add the new template suffix to `theme/layout/theme.liquid` line 81. Skip → Starlite chrome leaks (double header, double footer, wrong nav). Symptom: `quote` page leaked Starlite chrome for weeks after build because suffix wasn't added.

2. **Logo schema setting must be populated in the template JSON.** Wiring the `image_picker` schema in the section is half the work. The template JSON's `settings: { logo: "shopify://shop_images/..." }` must be set, otherwise the section falls back to the text wordmark. Symptom: OECM, design-services, quote, FAQ all rendered text instead of logo until `b4ae936` patched.

3. **`bbi-push-landing.py` only pushes assets/sections/templates — not `theme/layout/theme.liquid`, not snippets.** Layout changes need a direct Shopify API call (or `shopify theme push --only=layout/theme.liquid`). Skip → the gate edit lives in git but never reaches the dev theme.

4. **🔴 Push from the right repo root — worktree drift bug.** `bbi-push-landing.py` defaults `BBI_PUSH_ROOT` to the main repo (`/Users/leokatz/Desktop/Office Central/theme/`). When Claude Code works in a worktree (`.claude/worktrees/*/theme/`) and the script runs without `BBI_PUSH_ROOT=$(pwd)` set, it silently uploads **the main repo's stale versions** to Shopify, overwriting any fresh worktree work. Symptom: industries page lost its embedded header/footer mid-week; all 10 BBI landing sections drifted out of sync until `9c8b7db` re-pushed all 22 files from the worktree at once. **Always run `BBI_PUSH_ROOT=$(pwd) python scripts/bbi-push-landing.py …` from inside a worktree, or fix the script to auto-detect (see PB-12).**

**Pre-deploy verification (every new page):**
- `document.querySelectorAll('.bbi-header').length === 1`
- `document.querySelectorAll('.bbi-footer').length === 1`
- No `.shopify-section-group-header-group` in DOM
- Logo `<img>` has non-empty `src`
- Every cross-link href returns 200
- `/bbi-lp-audit` returns clean
- Pre-flight: `pwd` is the worktree, `BBI_PUSH_ROOT=$(pwd)` set, OR push script has been patched (PB-12)

---

## Wave A — Foundations + Phase 2 build

**Pre-req:** Track D (DS-0 → DS-4) ✅ complete. Phase 1 (P1-1 → P1-11) ✅ complete.
**Goal:** Stop the bleeding (PB-12), harden the build skill (SKILL-1), unify nav/footer (NAV-1..4), then build the Business Furniture vertical + 9 categories.

**Order rationale:** PB-12 first because every `--slug` push today is a coin flip until root-detection is fixed. SKILL-1 next because it's the prevention layer that uses PB-12's fix in its pre-flight check. NAV-1..4 then because Phase 2 collection-category pages should be built on top of the unified nav, not embed yet another copy.

| # | ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|---|
| 1 | **PB-12** | **🔴 Fix `bbi-push-landing.py` root detection + extend to layout/snippets** | ✅ | commit `5888659` (worktree `cool-jepsen-6d89c5`, pending merge to main) | **Done.** `_resolve_root()` is worktree-aware: env var > cwd-contains-`.claude/worktrees/` > `__file__` fallback, with loud `⚠️ ROOT MISMATCH` banner on divergence. New `--layout` flag pushes only `layout/theme.liquid`. New `--snippets` flag pushes only `snippets/bbi-*.liquid` (Starlite legacy snippets structurally excluded). Startup banner prints `Root / Layout / Snippets` for audit. |
| 2 | **CLEANUP-1** | **Remove phantom gate suffixes + prune stale planning docs** | ✅ | commit `c9e5c5a` | One-off housekeeping prerequisite to SKILL-1. Remove `brand-dealer` + `smoke-test` from `bbi_landing` gate; delete replaced/draft planning files; update CLAUDE.md reference table. |
| 3 | **SKILL-1** | **Harden `/bbi-build-page` skill** | ✅ | commit `06220d0` `.claude/skills/bbi-build-page/SKILL.md` | **Done.** v2.0: Pre-Step 0b (worktree hard-stop + build-state check + interlinking context load); gate edit automated in Step 5 (writes `theme.liquid` directly, no manual step); Step 9 (image_picker discover → upload → populate template JSON → `--layout` then `--slug` in one call); Step 11 (full 12-point check: 10 DOM assertions + source-level FAQ grep + 3-signature drift check); Step 12 (mark ✅ only on all-green). version: 2.0 pinned. |
| 4 | NAV-1 | Lock canonical nav spec | ✅ | commit `d41295a` `docs/strategy/bbi-nav-spec.md` | Decision: 5-item w/ mega-menu (per site-architecture-2026-04-25.md §1) — `Shop Furniture · Industries · Brands · Services · About` + phone CTA + Quote button right-aligned. Mobile: hamburger → full-screen accordion overlay. 🔔 ~~NEEDS DECISION~~ — Spec locked 2026-05-06. |
| 5 | NAV-2 | Build `bbi-nav.liquid` + `bbi-footer.liquid` snippets | ✅ | commit `f683fb9` `theme/snippets/bbi-nav.liquid`, `theme/snippets/bbi-footer.liquid` | **Done.** Mega-menu nav (5 items, all dropdown-only, CSS hover+focus-within, `<bbi-nav-mobile>` Web Component with WCAG focus trap + Escape). Footer: 9-cat Shop col, OECM in Services col, OECM trust band above copyright. Active state via `active` render param. Healthcare + Quote smoke-tested: 14/14 assertions green (1 header, 1 footer, correct active item, 4 columns, trust band). |
| 6 | NAV-3 | Refactor 10 ds-lp-* sections to render shared snippets | ✅ | commit `5ba69b0` (all 10 ds-lp-*.liquid files) | **Done.** All 10 sections render shared snippets (healthcare+quote in NAV-2; industries/education/government/non-profit/professional-services/design-services/faq/oecm here). ~131–141 lines removed per section (header CSS + footer CSS + HTML blocks). Smoke test: 4 pages × 5 assertions = 20/20 green; style count 14→16 (+2 snippet styles, confirming dead section CSS removed); FAQ regression OK (Services col has 6 links incl. FAQ). |
| 7 | NAV-4 | Homepage onto shared nav | ✅ | commit `2850959` `theme/sections/bbi-nav-wrap.liquid`, `theme/sections/bbi-footer-wrap.liquid`, `theme/templates/index.json`, `theme/layout/theme.liquid` | **Done.** Option A wrapper sections (bbi-nav-wrap + bbi-footer-wrap); logo image_picker + pre-populated with v2 logo URL. Gate extended: `template == 'index'` added. Smoke test 6/6 green: bbi-header=1, bbi-footer=1, Starlite suppressed, no active item on /, footerColumns=4, 10 bbi- sections in order (nav-wrap first, footer-wrap last). |
| 8 | PB-13 | Reconcile brand-dealer (merge or de-gate) | ⬜ | `theme/sections/ds-lp-brand-dealer.liquid` (currently missing on main) | 🔔 **NEEDS DECISION** — Suffix is in `bbi_landing` gate but section file is on a separate branch. Decide: merge the brand-dealer branch into main, OR remove `brand-dealer` from the gate (clean up dead reference). |
| 9 | PB-9 | Extend `bbi_landing` gate to detect collection templates | ⬜ | `theme/layout/theme.liquid` | Add `template.name == 'collection' and template.suffix == 'category'` branch. Test with throwaway template. |
| 10 | PB-10 | Build `collection.category.json` template + `ds-cc-base.liquid` section pattern | ⬜ | TBD `theme/templates/collection.category.json`, `theme/sections/ds-cc-base.liquid` | Mirror ds-lp-* pattern: hero, intro, tile grid via section blocks, breadcrumb, smart-collection "View all" button, ergoCentric/Keilhauer callouts where spec'd, phone CTA. Uses bbi-nav + bbi-footer snippets from NAV-2. |
| P2-1 | Business Furniture vertical (`/collections/business-furniture`) | ⬜ | TBD via `collection.category.json` | 9 category tiles, OCI photos, "Free design layout" CTA. |
| P2-2 | Seating (`/collections/seating`) | ⬜ | | 16 sub-type tiles |
| P2-3 | Desks & Workstations (`/collections/desks`) | ⬜ | | 9 sub-type tiles, L-Shape leads |
| P2-4 | Storage & Filing (`/collections/storage`) | ⬜ | | 14 sub-type tiles |
| P2-5 | Tables (`/collections/tables`) | ⬜ | | 10 sub-type tiles |
| P2-6 | Boardroom (`/collections/boardroom`) | ⬜ | | 3 sub-type tiles, Keilhauer callout |
| P2-7 | Ergonomic Products (`/collections/ergonomic-products`) | ⬜ | | 4 sub-type tiles, ergoCentric callout |
| P2-8 | Panels & Dividers (`/collections/panels-room-dividers`) | ⬜ | | 3 sub-type tiles |
| P2-9 | Accessories (`/collections/accessories`) | ⬜ | | 4 sub-type tiles |
| P2-10 | Quiet Spaces (`/collections/quiet-spaces`) | ⬜ | | 5 sub-type tiles |
| PB-11 | Sub-collection 200/404 + product count audit | ⬜ | `data/reports/sub-collection-audit-<date>.csv` | Verify all ~68 sub-collection URLs return 200, products > 0, smart vs manual classification |
| LEAD-1 | Crawl + dump current lead routing | ⬜ | `docs/plan/bbi-lead-routing.md` | 🔔 **NEEDS INPUT** — Claude Code can crawl and dump every CTA → destination URL, but you need to confirm where each form/email currently routes (which inbox, which CRM, any auto-replies). Halt and ask before publishing. |
| INTERLINK-1 | Formalize P1-11 audit pattern as reusable script | ⬜ | `scripts/audit-interlinks.py` + `docs/plan/bbi-interlinking-map.md` | Re-runnable on every Phase 2/3/4 page set. |
| IND-PROP | Industries Hub Browse + FAQ propagation to 5 industry pages | ⬜ | 5 ds-lp-* files | Add the two sections from commit `e98f91f` to healthcare, education, government, non-profit, professional-services. |

---

## Wave B — Phase 3 + Smart Collections

**Pre-req:** Wave A complete.
**Goal:** Sub-collection product listings on the new design system. Migrate manual collections to smart so new products auto-populate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| PB-14 | Manual → Smart collection migration script + per-collection assignment + rollback | ⬜ | TBD `scripts/migrate-to-smart-collections.py` | Convert manual `/collections/*` to rule-based using `type:*` and `room:*` tags. Backup first. |
| PB-15 | Build `collection.json` template + `ds-cs-base.liquid` section | ⬜ | TBD `theme/templates/collection.json`, `theme/sections/ds-cs-base.liquid` | Filter sidebar + product grid + 4-level breadcrumb (Home > Shop Furniture > Category > Sub-collection) + phone CTA. |
| P3-rollout | Apply `collection.json` to ~68 Business Furniture sub-collections | ⬜ | Push script log | Script-driven push, hero images from `data/page-images/` |
| INTERLINK-2 | Re-run interlinking audit, fix drift introduced by Phase 3 | ⬜ | Audit output | |

---

## Wave C — Phase 4 trust pages

**Pre-req:** Wave B complete (so brand pages can link to live shop verticals).
**Goal:** Brands hub + brand pages + About + Contact + Our Work + Delivery + Relocation.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| P4-1 | Brands Hub (`/pages/brands`) | ⬜ | TBD `theme/sections/ds-lp-brands.liquid` | 3 brand tiles + Authorized Canadian Dealer trust |
| P4-2 | Keilhauer (`/pages/brands-keilhauer`) | ⬜ | | Premium boardroom seating, link to `/collections/boardroom` |
| P4-3 | Global / Teknion (`/pages/brands-global-teknion`) | ⬜ | | Panel systems, link to `/collections/desks`, `/collections/panels-room-dividers` |
| P4-4 | ergoCentric (`/pages/brands-ergocentric`) | ⬜ | reconcile with PB-13 | Canadian-made ergonomic specialist |
| P4-5 | About (`/pages/about`) | ⬜ | | Heritage + Office Central backing + 6 locations + OECM |
| P4-6 | Our Work / Portfolio (`/pages/our-work`) | ⬜ | uses `data/oci-photos/catalog.json` | Paginated from JSON manifest, 48 OCI photos |
| P4-7 | Contact (`/pages/contact`) | ⬜ | | 6 locations, vertical + request-type form fields, route to sales@ |
| P4-8 | Delivery & Installation (`/pages/delivery`) | ⬜ | | Mirror Design Services structure |
| P4-9 | Relocation Management (`/pages/relocation`) | ⬜ | | Mirror Design Services structure |

---

## Wave D — Wave 0 SEO foundation (parallel to A/B/C)

**Pre-req:** None — runs in parallel with theme work.
**Goal:** Make SEO progress measurable before launch. Mostly Leo's manual work.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| W0-1 | Google Search Console + GA4 setup | ⬜ | GSC property + GA4 property | Critical — no SEO compounds without this |
| W0-2 | Create BBI Google Business Profile | ⬜ | google.com/business listing | |
| W0-2b | Google Reviews seeding strategy | ⬜ | `docs/plan/reviews-seeding.md` | |
| W0-6 | Parent domain backlinks (officecentral.com, brantbasics.com) | ⬜ | inbound link audit | Coordinate with parent webmasters |
| W0-7 | OECM + "Since 1964" trust signals on store header/footer | ⬜ | shared snippets + announcement bar | Already in landing pages — surface site-wide |
| W0-3 | Upload product redirects CSV | 🟡 | `data/url-redirects.csv` exists | Manual upload in Shopify Admin pending |

---

## Wave E — Pre-launch hardening

**Pre-req:** Waves A + C complete.
**Goal:** All schema, copy, lead routing, nav, design system verified before launch gate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| AI-3 | Product schema (JSON-LD) on every PDP | ⬜ | view-source check | `name`, `description`, `image`, `offers`, `brand`, `sku` |
| AI-4 | Organization schema on homepage + About | ⬜ | view-source check | `name`, `url`, `logo`, `telephone`, `address`, `areaServed`, `sameAs` |
| AI-6 | BreadcrumbList JSON-LD on collection + product pages | ⬜ | view-source check | |
| AI-7 | Entity-clarity copy on homepage | ⬜ | first 200 words on `/` | Who BBI is, what they sell, who they serve, where |
| AI-8 | OECM page copy hardening | ⬜ | `/pages/oecm` | Highest-value AI citation target |
| AI-9 | FAQ blocks on category pages | ⬜ | 9 category pages | 3–5 Q&A per category, FAQPage schema |
| AI-5 | FAQ schema on OECM, Design Services, top blog posts | ⬜ | view-source check | |
| LEAD-2 | Gap analysis on lead routing | ⬜ | `docs/plan/bbi-lead-routing.md` | Identify duplicate forms, inconsistent inboxes |
| LEAD-3 | Unify on `bbi-lead-form.liquid` snippet + ack auto-reply per type | ⬜ | TBD `theme/snippets/bbi-lead-form.liquid` | 🔔 **NEEDS DECISION** — Single inbox to consolidate on (sales@brantbusinessinteriors.com or another?), and the auto-reply copy per `lead_type` (quote / design / contact / oecm). Halt before writing the snippet. |
| INTERLINK-3 | Final cross-link audit, all pages | ⬜ | audit output green | |
| NAV-VERIFY | Homepage + collection pages render shared nav | ⬜ | DOM check | Verify NAV-3, NAV-4 stuck |
| DS-VERIFY | DS pre-launch verification (HARD GATE) | ⬜ | screenshot diff vs T5 locked | Brand-red unified, dark-mode block stays deleted, tokens intact |
| IMG-PHASE2 | Product image regen (≥80% coverage SOFT GATE) | ⬜ | `data/reports/img-phase2-coverage.csv` | Waiver CSV for the rest |
| CONTENT-1 | Finalize BBI logo asset | ⬜ | `data/logos/bbi-logo-final.png` | 🔔 **NEEDS DECISION** — `bbi-logo-v2` is the Brant Basics wordmark (not BBI-specific). Lock it as the current answer, OR source/design a true "Brant Business Interiors" wordmark. If sourcing new, that's a content task that adds 1–2 days. |

---

## Wave F — Launch

**Pre-req:** Wave E complete.
**Goal:** Cutover from BBI Landing Dev to live theme.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| **LAUNCH-0** | **Image confirmation gate (HARD)** | ⬜ | `data/reports/page-images-audit-<date>.csv` reviewed | 🔔 **NEEDS YOUR REVIEW** — Claude Code generates the CSV; you must personally mark every row Approved / Reject / Replace before LAUNCH-1 can run. Hard gate, no automation. |
| LAUNCH-1 | Pre-publish GO/NO-GO report | ⬜ | `data/reports/launch-go-nogo-<date>.md` | 4 critical URLs return 200, no TBD/lorem, screenshots saved. No writes. |
| LAUNCH-2 | Manual publish of BBI Landing Dev → live | ⬜ | live theme backup + post-publish snapshot | 🔔 **MANUAL CLICK** — never automated. Claude Code runs the live-theme backup; you click Publish in Shopify Admin. |
| LAUNCH-3 | Resubmit sitemap to GSC, monitor 404s for 72h | ⬜ | GSC dashboard | |
| LAUNCH-4 | Mobile smoke test (Chrome, Safari, Firefox, iOS, Android) | ⬜ | screenshots saved | |

---

## Backlog (post-launch)

These compound after live, none blocks launch:

- **Phase 1b full catalog** — PE-5/6/7 for the 503 non-Hero products (descriptions, specs, meta)
- **Blog** — BL-1..BL-6 (template + schema + related products) + first 10 posts (B1..B10)
- **AI search** — AI-10 (spec completeness), AI-11 ("best of" / comparison content)
- **Smart Collections** — finish migration on remaining manual collections
- **Wave 2** — Acoustic Pods sub-collection, sit-stand buyer guide, hybrid work bundle
- **Wave 3** — City-level SEO, ergonomics hub, sustainability/LEED page, manufacturer dealer locator pages
- **Ideas backlog** — see `docs/plan/ideas-backlog.md`

---

## Phase 1 — Done ✅ (reference)

All 11 P1 rows complete on origin/main.

| ID | Page | Evidence |
|---|---|---|
| P1-1 | Homepage | `theme/templates/index.json` (8 sections) — commit `7172c85` |
| P1-2 | OECM | `theme/sections/ds-lp-oecm.liquid` + `page.oecm.json` — commit `ef234cf` (header/footer added `905db28`, logo `b4ae936`) |
| P1-3 | Design Services | `ds-lp-design-services.liquid` + `page.design-services.json` — commit `0ab1663` (header/footer added `905db28`, logo `b4ae936`) |
| P1-4 | Quote | `ds-lp-quote.liquid` + `page.quote.json` — commit `b40a1e3` (gate + header/footer + logo `0fe3de9` / `b4ae936`) |
| P1-4b | FAQ | `ds-lp-faq.liquid` + `page.faq.json` — commit `0d452eb` (logo `b4ae936`) |
| P1-5 | Industries Hub | `ds-lp-industries.liquid` + `page.industries.json` — commit `623cc43` (Browse + FAQ added `e98f91f`) |
| P1-6 | Healthcare | `ds-lp-healthcare.liquid` + `page.healthcare.json` — commit `9a8c27b` (crosslink fix + footer pro-services `905db28`) |
| P1-7 | Education | `ds-lp-education.liquid` + `page.education.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-8 | Government | `ds-lp-government.liquid` + `page.government.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-9 | Non-Profit | `ds-lp-non-profit.liquid` + `page.non-profit.json` — commit `ee44b06` (footer pro-services `905db28`) |
| P1-10 | Professional Services | `ds-lp-professional-services.liquid` + `page.professional-services.json` — commit `ee44b06` |
| P1-11 | Phase 1 interconnection audit + fix | commits `905db28`, `0fe3de9`, `0d452eb`, `b4ae936` |

---

## Track D — Design System Done ✅ (reference)

| ID | Task | Evidence |
|---|---|---|
| DS-0 | Land Claude Design Phase 3 — 5 screen exports + audit tables | commit `c1a719c` |
| DS-1 | Fill `design-system.md` TBD placeholders | commit `b34807c` (`grep -c TBD = 0`) |
| DS-2 | Push design tokens to BBI Landing Dev | commit `8ebc65c` |
| DS-3 | Three Liquid edits + PR + push | dark-mode block deleted, `#f00f00`/`#FFCA10` → `#D4252A` |
| DS-4 | `/bbi-build-page` readiness check | 9-row pass — `READY` verdict |

---

## Phase 1b — Hero 100 Done ✅ (reference)

All Hero 100 product enrichment is LIVE on Shopify.

| ID | Task | Evidence |
|---|---|---|
| PE-1 | Hero 100 descriptions (LIVE) | commit `58803c3` — 1,165 product mutations |
| PE-2 | Hero 100 spec metafields (LIVE) | commit `204d8dc` — 77 products / 606 metafield writes / 0 failures |
| PE-3 | Hero 100 normalized titles (LIVE, ™/® stripped) | commit `57d99f3` — 588 products |
| PE-4 | Hero 100 SEO meta titles + descriptions (LIVE) | commit `a2118f3` — 100 Hero SEO meta |
| PE-7 | Long-tail SEO drafts (LIVE) | commit `58803c3` |

---

## AI Search — Started 🟡 (reference)

| ID | Task | Status | Evidence |
|---|---|---|---|
| AI-1 | `llms.txt` deployed | ✅ | commit `a2118f3` |
| AI-2 | `robots.txt` audit | ✅ | commit `24ab01e` |
| AI-12 | `audit-ai-readability.py` script | ✅ | commit `a752eb3` |
| AI-3..AI-11 | Schema + copy work | ⬜ | see Wave E |

---

## Open questions / decisions pending

1. **Canonical nav** — landing pages render `Shop · Brands · Verticals · Our work · Services · About`, spec says `Shop Furniture · Industries · Brands · Services · About`. NAV-1 needs Steve's call.
2. **brand-dealer reconciliation** — section file is on a separate branch, suffix is in the gate. Merge or de-gate? (PB-13)
3. **BBI logo** — `bbi-logo-v2` is Brant Basics wordmark. Lock it or source a true BBI wordmark? (CONTENT-1)
4. **Smart Collection migration timing** — confirmed: before Phase 3 (Wave B step 1)

---

## File update protocol

When you ship a row:

1. Edit this file's row to ✅, fill the Evidence column with the git SHA or live URL.
2. Commit in the same change as the work (`feat: P2-2 Seating category page (closes BUILD-STATE row)`).
3. Update `docs/plan/bbi-interlinking-map.md` if the row affects cross-links.
4. Re-run `/bbi-lp-audit` if the row is a page; expect green.

When you find drift (row says ✅ but file/URL is missing):

1. Don't change the row — investigate first.
2. If the work was reverted, mark ⬜ and note why.
3. If the row was never true, mark ⬜ and note the original commit was wrong.
