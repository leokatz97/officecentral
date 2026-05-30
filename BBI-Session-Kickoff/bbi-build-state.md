# BBI Build State — Single Source of Truth

> **Source of truth.** This file is canonical. The `bbi-launch-tracker` Cowork artifact is the visual dashboard view of it — both update together. **Restructured 2026-05-24:** the day-block navigation (Day 9 / Day 10 / Day 11) was replaced with a linear **DO NEXT** queue (21 items in dependency order, now 16 after the Day 10 closures) plus a **RIGHT NOW** fireable-now list and an expanded **POST-LAUNCH BACKLOG**. The full session log, ⛔ Hard Rules + Safety Rules, technical sections, Wave A–H tables, and reference material are preserved verbatim below the divider. Full ship history lives in `docs/project/launch-tracker-archive.md`.

**Current state:** 2026-05-25 (Monday evening) · **🚀 LAUNCH DAY (Day 11) — IN PROGRESS** · **43 of 54 launch steps done (80%)** · Day 11 morning HIGH-3 fix landed (commit `7fb46b7` — closes the last SYS-VERIFY HIGH from LEAD-2). Day 11 afternoon/evening shipped parallel image rounds substantively advancing Step 46 IMAGE SWAP without waiting on the Upwork delivery — COLLECTION-IMG-PULL-1 (53 slots), BRAND-IMG-1 (12 slots), customer-stories (2 slots), homepage hp-featured (3 slots), INDUSTRY-HEROES + INDUSTRIES-HUB-TILES (4 slots) — for a Day 11 total of **~74 image slots filled**, with **~63 inventory slots still pending the Upwork delivery** for Step 46 to fully close. HOMEPAGE-BORDERS introduced the `--bbi-line` token; HEADER-POLISH shipped (with caveat: bar/nav rules modify CSS not loaded on BBI surface — see should-fix #1 in audit report); preview-dev tooling + gitignore hygiene also landed Day 11. **PRE-LAUNCH-AUDIT-1 verdict: ✅ READY FOR LAUNCH — 0 critical findings; LIVE integrity confirmed (`updated_at` 2026-05-16); DEV renders cleanly on all 8 key URLs with zero Liquid errors; theme-check baseline (2855 offenses) unchanged.** Target LAUNCH-2: once Upwork delivers remaining ~63 images + Step 46 closes + SYS-VERIFY-1 Phase 2 re-run + LAUNCH-0 image approval. The queue below is dependency-ordered with ⏳ ready / 🔒 blocked status flags — no day labels. *(This snapshot is the Day 11 evening sync, written 2026-05-25 after PRE-LAUNCH-AUDIT-1 — see `data/reports/pre-launch-audit-2026-05-25.md`.)*

---

## 🟢 Day 17 — 2026-05-30 — (AM) PHASE A BLOCK 1 (QUICK WINS) → 2 TIER 2B CLOSURES · **OECM-TRUST-ALT-TEXT** + **PERFORMANCE-MEASUREMENT-DISCIPLINE** (PR #52) · (PM) PHASE-A-BLOCK-2-SESSION-1 → **HOMEPAGE-CONTENT-DENSITY** RESOLVED, Scope C all 5 opportunities — WebPage + ItemList + 3×Service + FAQPage schema · "authorized dealer"+BPS keyword weave · 5-Q&A visible FAQ block (PR #53) · (EVENING) **PHASE A BLOCK 4 NOW IN PROGRESS** — catalog enrichment Sessions 1-4: **32 products enriched** (PRs #60/#61/#63) + **183 vendor corrections** (PR #62) + 4 reference files established + manufacturer dictionary grown 3→19 · **17 PRs total on Day 17** (13 morning/afternoon #45-56 + 4 evening enrichment #60-63)

### 🟢 Day 17 morning — PHASE A BLOCK 1 (quick wins) ✅ SHIPPED 2026-05-30 · PR #52

- **PHASE-A-BLOCK-1 ✅** — two Tier 2B closures bundled into one PR (`feature/phase-a-block-1-quick-wins-2026-05-30`, off `main` @ `4d46f5f`). Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (watcher clear; role=main verified on `186373570873`). Theme check baseline `2833/165` held throughout.
  - **OECM-TRUST-ALT-TEXT ✅ shipped (production write).** Diagnosed the *residual* trust-cell alt mismatch via markup→schema→asset→photo-content trace: **cell 1 (`trust_image_1`, Education)** renders `OCI-Healthcare-Carousel-3.jpg` (a healthcare reception corridor — "ACCUEIL" wall, stacking guest chairs, A–G wayfinding) but its alt still claimed "Halton DSB admin offices OECM install." This is the mirror of the slot-1/2 image shuffle that Day 13 QW-1 corrected on cell 2. **The pending inventory entry's text described cell 2 (already fixed Day 13) — classic BUILD-STATE-INVENTORY-DRIFT; diagnosis confirmed the real residual was cell 1.** Corrected alt → "Healthcare reception corridor with a row of stacking guest chairs and lettered wayfinding signage" (provenance-neutral, content-accurate, per Day 13 alt convention; `ds-lp-oecm.liquid:492`). PUT to LIVE role=main `186373570873` (`updated_at 11:12:19`); asset SHA match (`be317cb1…`); cache-busted curl on `/pages/oecm` confirmed new alt renders + stale alt **0 occurrences**; theme check `2833/165` holds. **Scope discipline:** alt-text-only — the visible `<figcaption>` caption-vs-image mismatch remains owned by **OECM-TRUST-CAPTIONS-1** (Tier 1, scope-separate).
  - **PERFORMANCE-MEASUREMENT-DISCIPLINE ✅ shipped (docs-only, no theme write).** Formalized the discipline — referenced by name across this file (Day 13 HOTFIX-MOBILE-LCP work) but never written into a canonical home — into new **`BBI-Session-Kickoff/measurement-protocols.md`**: multi-run median (min 3 runs) before declaring a metric shifted on already-fast pages (LCP < 3s) where single-run Lighthouse has ±400-500ms variance; trust architectural correctness over single-run signals; applies to PSI mobile+desktop, local Lighthouse CLI, and any Core Web Vitals lab-estimate tool. Cross-linked from `01-safety-preflight.md` REFERENCE DOCS for discoverability. Location call (dedicated protocols file vs. folding into the write-safety preflight doc) was Leo's — delegated to Claude, chose the dedicated file as the cleaner thematic home.
  - **Logged OECM-TRUST-IMAGE-SLOT-ASSIGNMENT** as new Tier 2B item — root cause underlying the trust-row mismatches; PR #52 fix addressed alt-text symptom only.

### 🟢 Day 17 afternoon — PHASE-A-BLOCK-2-SESSION-1 — HOMEPAGE-CONTENT-DENSITY ✅ SHIPPED 2026-05-30 · PR #53

- **HOMEPAGE-CONTENT-DENSITY ✅ SHIPPED 2026-05-30** (branch `feature/homepage-content-density-2026-05-30`, off `main` @ `962d99c` = PR #52 tip). Scope **C** — all 5 audit opportunities, single PR, 3 commits. Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (watcher clear; role=main `186373570873`). Theme check baseline `2833/165` held throughout.
  - **AUDIT (no writes) overturned the "reads thin" premise.** Homepage = `templates/index.json`, 9 custom-liquid sections (hero→trust→about→shop→featured→oecm→industries→services→work). Content is already **dense**: 952 visible words, 25 headings, clean H1→H2→H3 hierarchy, strong defensible-angle coverage (OECM ×20, Ontario ×15, Agreement 2025-470 ×5, founded-1964 ×6, Peterborough ×6). **The real gap was schema:** the homepage emitted only sitewide CHROME (`bbi-org-schema` #organization/#website + `bbi-localbusiness` #localbusiness) and ZERO page-specific schema — the conspicuous hole, since every other template type already emits page schema. Content micro-gaps: "authorized dealer" + PSAB both zero-count.
  - **Commit 1 — Schema lane** (`5b1ce05`): new snippet `theme/snippets/bbi-homepage-schema.liquid` — **WebPage** (#webpage, isPartOf→#website, about→#organization, primaryImageOfPage=hero, mainEntity→ItemList) + **ItemList** (#featured-categories, 4 collection links — CollectionPage links, no Product node, grounding-only by design) + **3× Service** via the shared `bbi-service-jsonld` snippet (space planning / installation / warranty, distinct id_suffix each, provider→#organization). Wired via a `bbi-home-schema` custom-liquid section. @id convention matches `bbi-blog-jsonld` (page nodes on `canonical_url`, chrome refs on `shop.permanent_domain`).
  - **Commit 2a — Keyword weave** (`5b788e5`): `bbi-about` paragraph 2 reframed — "As an authorized dealer for [Global, OTG, Heartwood, ObusForme, 25+ more]…" (closes the zero-count "authorized dealer" gap; was "from authorized lines") + "Ontario's broader public sector (BPS)" (was "Ontario institutional procurement"). **Brief said "PSAB" but PSAB = Public Sector Accounting Board (accounting-standards body, NOT a procurement term); DataForSEO confirms ~0 search volume on PSAB furniture terms ("PSAB compliance" ≈10/mo, rest nil). Used BPS — the accurate, established Ontario term (matches ds-lp-faq.liquid). Leo-approved.**
  - **Commit 2b — FAQ block + FAQPage** (`31cd4a1`): new snippet `theme/snippets/bbi-homepage-faq.liquid` — visible 5-Q&A accordion (ordering / NET 30 / OECM-2025-470 / delivery / space planning), condensed from `/pages/faq`, scoped `.hp-faq` + `[data-hp-faq-trigger]` so JS can't collide with the `/pages/faq` accordion. Matching **FAQPage** JSON-LD (#faq, 5 Qs, answer text identical to visible copy) added to the schema snippet. Wired via a `bbi-faq` section between `bbi-services` and `bbi-work`. Three Leo micro-edits applied: Q3 OECM grammar reworded; Q5 threshold matched `/pages/faq` canonical ("5 or more workstations or a full-room fit-out"); Q4 delivery = "across Canada, install ON + Western Canada" (matches homepage about, NOT `/pages/faq`'s "across Ontario" — divergence surfaced + logged as FAQ-DELIVERY-FOOTPRINT-RECONCILE).
  - **VERIFICATION — methodology shift to Admin-API readback.** Live render confirmed 6 JSON-LD blocks, 0 parse errors, 5/5 new entities + FAQPage present, 3/3 chrome invariants intact, no @id collisions. **Authoritative gate was Admin-API asset readback** (GET `…/themes/186373570873/assets.json?asset[key]=…`, compare bytes to local) — `ALL_DEPLOYED_OK` ×2. role=main re-verified after each PUT. Theme check held `2833/165` (pre-existing `ValidSchemaTranslations` header error untouched).
  - **OPERATIONAL LESSONS (3, → memory):**
    1. **SILENT-PUT-FAILURE-CLAIMING-VERIFICATION** — `push-file.py` reads `SHOPIFY_TOKEN` from env (lives in `.env`, not exported); run without sourcing `.env` it died silently and Commit 1's first message claimed "verified on live" when nothing deployed. Caught by independent Admin-API readback before the PR; commit amended. Forward: source `.env` first (`set -a && . ./.env && set +a`); never claim verification without an independent check touching deployed bytes; tools should FAIL LOUD on missing prereqs. Sub-pattern of "outcome correctness ≠ process integrity."
    2. **CURL-VS-ADMIN-API-VERIFICATION-METHODOLOGY** — Shopify edge serves multiple cached full-page variants; `?cb=` query-string busting does NOT reliably bust the full-page cache (rendered byte size bounced between 3 values across consecutive fetches; just-deployed copy kept showing old for minutes). **Admin-API asset readback is the deploy gate; cache-busted curl is supplementary "can users see it yet" only.** Promotes the known "page_cache async from asset_cache" finding to a formal verification methodology.
    3. **BPS-OVER-PSAB-KEYWORD-CHOICE** — see Commit 2a; logged for future SEO content.
  - **Follow-up logged:** FAQ-DELIVERY-FOOTPRINT-RECONCILE (Tier 2B, below). **OG-META-WIRE-UP-SITEWIDE was the next (and final Phase A Block 2) session — shipped same day as a no-op closure, see below.**
  - _push-file.py path/flag note for future sessions: arg 1 is the asset KEY (e.g. `snippets/foo.liquid`), there is no `--live` flag — it always writes to `186373570873`; source `.env` before running._

### 🟢 Day 17 PM (late) — PHASE-A-BLOCK-2-SESSION-2 — OG-META-WIRE-UP-SITEWIDE ✅ SHIPPED 2026-05-30 · PR #54 · **NO-OP CLOSURE**

- **OG-META-WIRE-UP-SITEWIDE ✅ SHIPPED 2026-05-30 — no-op closure** (branch `feature/og-meta-wire-up-sitewide-2026-05-30`, off `main` @ `39f3be2` = PR #53 tip). **Final Phase A Block 2 item → Block 2 fully complete.** Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (watcher clear; role=main `186373570873`). PR #53 files (`bbi-homepage-schema`, `bbi-homepage-faq`) re-verified byte-identical to production. Theme check baseline `2833/165` held (no theme write this session).
  - **AUDIT (no writes) overturned the premise.** The restored item assumed og:* tags were *not reliably wired* and social shares rendered without title/description/image. **They are already 100% wired sitewide.** Cache-busted curl across 10 representative URLs (homepage, PDP, collection, brand, OECM, industries hub, healthcare, blog index, blog article, About) — **every one** emits a complete `og:title` / `og:description` / `og:image` / `og:url` / `og:type` + `twitter:card`/`title`/`description`. All 4 distinct og:image URLs return HTTP 200. A literal wire-up edit would have written **zero** new tags.
  - **WHY coverage is already complete.** All logic is one snippet — `theme/snippets/meta-tags.liquid` (rendered from `theme.liquid:11`). Homepage → `og-preview.png` (1024×1024). Every other template → `elsif page_image` branch, and Shopify's `page_image` global itself falls back to the **store Social-sharing-image preference** (`IMG_2566.jpg`) when a template has no specific image — so brand/OECM/industries/About/blog-index/image-less-collection pages all still emit a reachable og:image. No explicit `{%- else -%}` is needed because Shopify's fallback already covers it.
  - **No drift.** Admin-API readback confirmed local `meta-tags.liquid` is byte-identical to LIVE `186373570873` (SHA `a49096a3…`). This was the audit gate; cache-busted curl was supplementary live-render confirmation (per the CURL-VS-ADMIN-API methodology formalized in PR #53).
  - **SCOPE DECISION (Leo's call, in-session):** of 4 options (default-image swap / explicit-else+twitter:image / **document-only no-op closure** / hold-for-Steve-assets), Leo chose **document-only no-op closure**. No Liquid edit, no production PUT. Rationale: the wire-up is genuinely done; what's left is image *quality*, which needs assets, not Liquid.
  - **WHAT'S WEAK (quality/relevance, not presence) → 3 new Tier 2B follow-ups:** (1) **OG-IMG-DEFAULT-LANDSCAPE** — generic fallback `IMG_2566.jpg` is portrait 1039×1184, wrong ratio for social cards (want 1200×630); (2) **OG-IMG-PER-SEGMENT** (Steve/asset-gated) — per-segment topical OG images for landing/brand pages; (3) **OG-TWITTER-IMAGE-EXPLICIT** (low priority) — add explicit `twitter:image` (X already falls back to og:image). PDP product images are also small (658×352) — overlaps AI image pipeline Session 03.
  - **DELIVERABLE:** audit doc `docs/reviews/og-meta-audit-2026-05-30.md` (logic location, drift check, 10-row coverage table, reachability results, follow-ups, Leo's manual-validator URL list).
  - **Leo post-session (brief):** run the 5 priority URLs through LinkedIn Post Inspector / FB Sharing Debugger / X Card Validator (external scrapers can't run from Claude Code). Priority: `/`, `/pages/oecm`, OECM blog article, `/pages/healthcare`, `/pages/brands-global-teknion`.

### 🟢 Day 17 evening — PHASE-A-BLOCK-3 — HOTFIX-MOBILE-LCP-1b ✅ SHIPPED (theme-level JS hygiene) 2026-05-30 · PR #55

- **HOTFIX-MOBILE-LCP-1b ✅ COMPLETED 2026-05-30** (branch `feature/hotfix-mobile-lcp-1b-2026-05-30`, off `main` @ `0dbf164` = PR #54 tip). Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (watcher clear; role=main `186373570873`). Theme check baseline **`2833/165` held** (2043 err / 790 warn — verified before AND after both edits; deletion of the orphan snippet did not change the file count since it carried 0 offenses). Post-cascade readback (meta-tags / homepage-schema / homepage-faq) all byte-matched LIVE before work began.
- **AUDIT (Phase 1, no writes) reframed the premise — same pattern as the og-meta no-op.** The Day-14 backlog framed 1b as "333 KiB unused JS + transpile/polyfill drop + per-template code-split." The audit found:
  - **Avis Product Options is ~90% of all JS weight** — 300 KB gzip / 1.24 MB raw across 14 `apo-*` files, loaded on **every page incl. the homepage** (no configurable products there). This IS the 287–334 KiB "unused JS" PSI flags. **It is app-embed-injected via `content_for_header` → NOT theme-editable.** Split out as new Tier 2B **AVIS-APP-SCOPE-OPTIMIZATION** (the real lever; app-settings work).
  - **The theme's heavy asset JS is already dead** — `theme.js` (270KB), `jquery.min.js` (87KB), `flickity.js` (81KB), `player.js`, `aos.js`, `parallax.js`, `lazysizes.min.js` are referenced in **0 liquid files** and served on **0 live pages**. "Remove unused JS" in this theme = repo cleanup with zero live-perf impact (deferred to a separate cleanup task — deleting served assets risks legacy non-BBI templates).
  - **The genuine theme-editable JS surface is ~37 KB inline** (ds-pdp-base 10KB, bbi-nav 9.6KB, bbi-quote-modal 7.6KB), already reasonably placed.
- **MEASUREMENT — real mobile baseline captured (Leo ran PSI manually).** Keyless PSI mobile API quota-blocked (`quota_limit_value: 0`); DataForSEO Lighthouse is desktop-only (TBT≈0, useless for this objective). Leo ran PSI mobile (Moto G Power + Slow 4G) 3× per page:
  - **Homepage:** TBT **80 / 110 ms** (median ~95ms), LCP 4.2s, Perf 84–85, unused-JS flagged **334 KiB**.
  - **PDP** (`/products/global-accord-mesh-back-tilter`): TBT **170 / 190 / 390 ms** (median 190ms), LCP 5.0–5.4s (one 12.9s slow-4G image outlier), Perf 56–73, unused-JS flagged **287 KiB**.
  - **Key insight:** TBT is *already in Google's "good" (<200ms) band* on both pages. The waste is in **bytes** (unused Avis JS), not blocking time. Captured in `BBI-Session-Kickoff/measurement-protocols.md` as the regression-detection reference point.
- **SCOPE DECISION (Leo's call, in-session via 2-question halt):** measurement = "Leo runs PSI mobile manually"; scope = **"Theme cleanup only (low-risk)"**. Two changes, each its own commit + fire-phrase ceremony:
  - **`lcp-1b-aos-noop`** — `theme/layout/theme.liquid`: removed the dead AOS/`universalParallax` `DOMContentLoaded` init block (20 lines). Guarded by `typeof AOS !== 'undefined'`, always false sitewide (`aos.js`/`parallax.js` load nowhere) → a per-page no-op listener. Fire phrase `fire lcp-1b-aos-noop`; PUT to role=main `186373570873`; updated_at → 13:11:40; size 10,308 → 10,233 b; **post-PUT Admin-API readback byte-match** (`AOS.init` confirmed gone; "universalParallax" remains only in the explanatory Liquid comment).
  - **`lcp-1b-seoant-orphan`** — deleted `theme/snippets/SEOAnt-SpeedUp.liquid` (10,688 b orphan; `AllowJsPlugin` interaction-deferral, **never rendered** — grep confirmed 0 references repo-wide before delete). Fire phrase `fire lcp-1b-seoant-orphan`; DELETE on role=main; **readback HTTP 404 confirmed gone**.
- **FUNCTIONAL VERIFICATION:** cache-busted curl on homepage / PDP / collection → all **HTTP 200** with body + nav + ATC/quote markers intact. The freshly-rendered collection page shows `AOS.init:0` (post-change render correct); homepage/PDP briefly still showed `AOS.init:1` = **stale edge full-page cache** (pre-PUT HTML), per the CURL-VS-ADMIN-API methodology — Admin-API readback is the authoritative gate and was green. **No functional surface to break:** the removed block never executed (guards always false); the deleted snippet was never rendered.
- **HONEST OUTCOME:** shipped as **dead-JS hygiene** (cleaner codebase, removed an orphaned script-injection snippet), **NOT a measurable TBT win** — consistent with the success criterion ("ship the JS work, not a lab LCP target"). The measurable mobile-perf win lives in AVIS-APP-SCOPE-OPTIMIZATION. **Deferred-this-session:** dead asset-file deletion (theme.js/jquery/flickity/etc. — zero perf, legacy-template risk) → separate cleanup task.
### 🟢 Day 17 evening (late) — DEAD-ASSET-CLEANUP ✅ SHIPPED 2026-05-30

- **DEAD-ASSET-CLEANUP ✅ SHIPPED 2026-05-30** (branch `chore/remove-dead-theme-assets-2026-05-30`, off `main` @ `0dbf164` = PR #54 tip). **Closes the dead asset-file deletion item deferred from HOTFIX-MOBILE-LCP-1b** (PR #55, Day 17 evening — "Deferred-this-session: dead asset-file deletion → separate cleanup task"). Repo + LIVE-theme hygiene, **zero live-perf impact** (the files were served on 0 pages). Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (watcher clear; role=main verified `186373570873`). Theme check baseline `2833/165` held.
  - **Deleted 10 dead asset files** (repo `git rm` + LIVE Admin-API DELETE) — `theme.js` (270KB), `jquery.min.js` (87KB), `flickity.js` (81KB), `player.js` (38KB), `aos.js` (14KB), `parallax.js`, `lazysizes.min.js`, `customer.js`, `ds-landing.js`, `theme-editor.js`. **Kept** (still referenced): `cart.js`, `product.js`, `collection-filter.js`.
  - **Reference audit (per-file, individual grep):** each of the 10 has **0 references** in any `.liquid` file (and 0 anywhere in `theme/` outside itself). The only `aos.js`/`parallax.js` hits are inside the HOTFIX-MOBILE-LCP-1b removal comment at `theme.liquid:216`. Whole-theme JS-load scan confirms the **only** `.js` asset loaded by any liquid is `collection-filter.js` (`main-collection.liquid:484`, `main-search.liquid:265`) — none of the 10 delete targets appear.
  - **Legacy-template risk check (the deferral's stated concern):** the `bbi_landing` gate's fall-through branch renders `{% sections 'header-group' %}` / `{% sections 'footer-group' %}`, but **neither section-group JSON exists in `theme/sections/`** — fall-through templates (gift_card, password, list-collections, generic pages) render no legacy chrome at all. And since the grep covered **all** `.liquid` (including any legacy sections), no legacy surface references the deleted assets. Safe.
  - **Production-write ceremony:** preflight PASS → per-file Admin-API `DELETE …/themes/186373570873/assets.json?asset[key]=assets/<file>` (all `200`) → per-file readback `GET` returned **HTTP 404** for all 10 (removal verified) → theme check held `2833/165` post-delete.
  - **Note:** the deferral note this closes is logged in **PR #55** (merged immediately before this PR; build-state additively merged at rebase, consistent with the established multi-PR build-state convention).

**Cowork artifact sync (Day 17 EOD):** bbi-launch-tracker Cowork artifact updated to Day 17 EOD state in parallel — Phase A Blocks 1-3 marked complete in the BLOG-LAUNCH-ROADMAP active view, Block 4 reframed to new manual workflow, 5 operational lessons added as Day 17 fold, Day 17 closed-history group added with all 10 PR refs (#45-48, #51-56). Build-state and Cowork now in sync.

### 🟢 Day 17 (2026-05-30) — OPERATIONAL LESSONS CONSOLIDATION (5)

Consolidated from the day's sessions (PRs #52–#56). Builds on Day 16's **BUILD-STATE-INVENTORY-DRIFT-FROM-SHIPPED-REALITY** lesson (see Day 16 BACKLOG-TRACKER-CLEANUP block).

1. **SILENT-PUT-FAILURE-CLAIMING-VERIFICATION** — `push-file.py`'s missing-token failure mode was silent; the commit message claimed live verification anyway. Caught by Admin-API readback showing **0/5 new schema entities on live** despite a "successful" PUT. Forward pattern: never trust a deploy succeeded without independent verification touching deployed bytes. Script-level fix: tools must FAIL LOUD on missing prerequisites (token unset = exit 1, not a silent skip). Sub-pattern of Day 13's "outcome correctness ≠ process integrity" lesson. Surfaced PR #53 mid-session.

2. **CURL-VS-ADMIN-API-VERIFICATION-METHODOLOGY** — Shopify edge serves multiple cached page variants across nodes; query-string cache-busting does not reliably bust the full-page cache. Curl-based "verification" served a stale variant initially, causing two false-positive verification claims. **Admin-API asset readback is the authoritative verification gate** (bypasses page cache entirely, reads stored bytes directly). Curl is a supplementary "edge propagation status" check, not the gate. Formalizes Day 13's "page_cache async from asset cache" finding into a methodology shift. Verification ordering going forward: pre-PUT byte snapshot → PUT → Admin-API readback (gate) → cache-busted curl (supplementary). Surfaced PR #53 mid-session.

3. **BPS-OVER-PSAB-KEYWORD-CHOICE** — DataForSEO empirical finding: "PSAB compliance" searches ~10/mo, other PSAB furniture terms ~0 volume. PSAB is an accounting standards body, not a procurement framework. **"Broader public sector (BPS)" is the correct phrase for Ontario institutional buyer SEO.** Used in PR #53 Commit 2a keyword weave. Logged for future SEO content reference.

4. **TIER-2B-WORK-ASSUMPTIONS-EXPIRE** — Tier 2B items logged based on point-in-time measurements (PSI runs, Okara audits, traffic snapshots) carry assumptions that age. The work description states what was true when logged; actual current-state can differ materially by the time the item is scheduled. The audit-first discipline catches three failure modes: (a) work was already done by other changes (**OG-META PR #54** — assumed missing, found 100% complete), (b) work was wrongly characterized initially (**HOMEPAGE-CONTENT-DENSITY PR #53** — assumed thin content, found 952 words dense), (c) baseline shifted under us (**HOTFIX-MOBILE-LCP-1b PR #55** — Day 13/14 cited TBT spikes to 3267ms, actual measurement showed ~95ms in good band). Three independent cases in 24 hours substantiate the pattern. Forward discipline: any Tier 2B item with a measurement-based work description older than 5 days starts with a Phase 1 audit verifying current baseline before any execution. Items based on architectural facts age more slowly than items based on performance metrics. Builds on Day 16's BUILD-STATE-INVENTORY-DRIFT-FROM-SHIPPED-REALITY lesson.

5. **EXTERNAL-METRIC-SEMANTIC-DRIFT** — An external tool's named metric ≠ what its name suggests. Okara's "1% content rate" was treated as evidence of thin homepage content; the audit revealed 952 meaningful words with dense defensible-angle coverage (OECM 20×, Ontario 15×, etc.). The "1% content rate" likely measures text-to-HTML ratio, not absolute content quantity. Forward discipline: when an external tool surfaces a named metric used as decision evidence, verify what the metric actually measures before acting on it. Particularly relevant for SEO/perf tools where named metrics can imply different things across vendors.

---

## 🟢 Day 17 evening (enrichment) — PHASE A BLOCK 4 SESSIONS 1-4 ✅ IN PROGRESS 2026-05-30 · PRs #60 / #61 / #62 / #63

**Block 4 (OTHER-COLLECTION catalog enrichment) is no longer "NEXT" — it is IN PROGRESS with substantial work shipped.** Four sessions ran on Day 17 evening, enriching 32 products, correcting 183 vendors catalog-wide, and standing up the reference infrastructure (4 files + a manufacturer dictionary grown from 3 → 19) that makes Sessions 5+ faster and more deterministic. All four PRs were merged to `main` (post-#63 tip `02e5860`).

### Sessions completed today

- **Session 1 — PR [#60](https://github.com/leokatz97/officecentral/pull/60): 5 `brand:global` products enriched.** Workflow-validation batch. Gold-standard field-shape verification anchored on `vion-mesh-high-back-chair-1` as the reference product. **13-field `specs.*` framework locked** (down from 15 — `tagline` and `standfirst` retired). Surfaced the SUB-BRAND-HOUSE-RULE (Basics / OTG / ObusForme → manufacturer = Global Furniture Group) via the Ergo Boss / Basics case.
- **Session 2 — PR [#61](https://github.com/leokatz97/officecentral/pull/61): 8 products enriched (accelerated workflow).** Established four reference files: `data/reference/brand-collection-routing.yaml`, `data/reference/manufacturer-defaults.yaml`, `data/reference/sku-prefix-lookup.yaml` (created Session 3), `data/reference/field-framework.md`. **Readback gate hardened** in `push-b4s1-enrichment.py` to absorb Shopify cosmetic normalization (entity-decode, list whitespace, seo-title-null when equal to product-title, HTML pretty-print) — future writes inherit this protection.
- **Session 3 — PR [#62](https://github.com/leokatz97/officecentral/pull/62): 183 catalog-wide vendor corrections** via the brand-recovery audit. **15 manufacturers discovered** (12 mapped in the dictionary + 3 unmapped sub-brands). 184 rollback snapshots taken. SKU prefix lookup created with **15 deterministic prefix→manufacturer mappings**. 204 products still UNKNOWN (decoded-SKU-prefix groups pending Leo input: HDL 40, IOF 26, RIC 12, HZN 10, MTY 9 — *since decoded to MityBilt in Session 4*, SCN 7, + 48 no-SKU). **Critical reframe locked: `vendor=BBI` is ALWAYS a data error — BBI is a dealer, not a manufacturer.**
- **Session 4 — PR [#63](https://github.com/leokatz97/officecentral/pull/63): 19 Global products enriched.** Auto-source success 19/20 (95%). MityBilt misclassification caught and reversed inline (`cluster-seating-2`). Corrupted boilerplate detected and rebuilt from manufacturer source (`loover` product). **20-agent parallel fan-out completed in 3.8 min wall-clock.** 5 new product types added (Workstation, Height-Adj Desk, Panel System, Flip-Top Table, Bar Stool). `officestogo.com` discovered as the primary source for Newland / NLP-prefix products.

### Block 4 totals as of EOD

- **32 products fully enriched** (5 + 8 + 19)
- **183 vendor corrections** (Session 3) + **1 reversal** (Session 4 MityBilt fix on `cluster-seating-2`)
- **19 manufacturers now in the dictionary** (was 3 at start of day: Global, Teknion, Humanscale)
- **4 reference files established** (see Reference Files inventory below)
- **~101 Global products remaining** for Sessions 5-8
- **~9 MityBilt products pending re-routing**
- **204 products deferred** (UNKNOWN SKU prefixes + 48 boilerplate-corrupted bodies)

### Operational lessons — Day 17 evening (13, from Sessions 1-4)

Format consistent with the Day 17 OPERATIONAL LESSONS CONSOLIDATION (5) above: label + brief context + actionable rule. *(12 process/workflow lessons + 1 field-handling rule.)*

1. **CSV-ROUTING-RECS-ARE-WEAK-HINTS** — Sessions 1-2 validated that the enrichment CSV's `recommended_sub_collection_*` columns are unreliable. Every product needs either a brand→collection lookup match or a human routing check. **Rule:** demote CSV recs to fallback signal only; the brand-collection routing YAML is the source of truth.
2. **SUB-BRAND-HOUSE-RULE-LOCKED** — Basics, Offices To Go (OTG), ObusForme → manufacturer field = **Global Furniture Group**; the sub-brand is captured in `product_line` (no redundant prefix) and a `sub-brand:{slug}` tag. Source: Session 1 (Ergo Boss / Basics case).
3. **READBACK-GATE-COSMETIC-NORMALIZATION** — Shopify storage normalizes entity-decoding, list whitespace, seo-title-null (when equal to product-title), and HTML pretty-printing. The hardened comparator in `push-b4s1-enrichment.py` handles all four. **Rule:** future writes inherit this protection; do not "fix" a diff that is purely cosmetic-normalization noise.
4. **AUTO-SOURCE-OUT-OF-FUEL-WAS-A-MISDIAGNOSIS** — Session 2 concluded the remaining catalog was "94% un-enrichable house-brand generic." Session 3's `vendor=BBI is always a data error` reframe reopened the auto-source path. **Rule:** when a workflow appears blocked, question the diagnosis before pivoting strategy.
5. **VENDOR-BBI-IS-ALWAYS-A-DATA-ERROR** — Locked rule: BBI is a dealer, not a manufacturer. Any product with `vendor="Brant Business Interiors"` is mis-labeled. **No legitimate house-brand carve-out exists.**
6. **SKU-PREFIX-PATTERNS-ARE-DETERMINISTIC** — Session 3 surfaced 15 prefix→manufacturer mappings (GLB/GLO/OFGO/OTG/MVL=Global, SAF=Safco, HTW=Heartwood, OSP=Office Star, etc.). SKU-prefix matching is higher-confidence than name-matching heuristics. **Rule:** use SKU prefix as the primary signal in future brand-recovery scans. Session 4 added MTY=MityBilt.
7. **SINGLE-FIELD-VENDOR-UPDATES-SCALE-CLEANLY** — Session 3's 183 vendor corrections completed at ~2 sec/product with zero failures across all readbacks. **Rule:** single-field Admin API updates with the hardened readback gate are a safe pattern for bulk corrections at any reasonable scale (the resume-guard pattern in the apply script handles interruptions).
8. **MULTI-LAYER-VERIFICATION-CATCHES-ERRORS** — Session 3 had 1/183 misclassification (`cluster-seating-2` = MityBilt not Global → 99.5% accuracy). Session 4's auto-source agent caught it via SKU-prefix mismatch and refused to apply Global defaults. **Rule:** defense-in-depth across sessions works — each layer catches the previous layer's drift; keep the layers independent.
9. **BOILERPLATE-BODY-CORRUPTION-RECOGNIZABLE-BY-AGENT** — ~48 products carry identical wrong boilerplate text (a jacket and an ice-melt both carrying a chair description). Session 4 auto-source agents demonstrated the ability to detect mismatched body content and rebuild from manufacturer source (`loover` product). **Rule:** a separate session is warranted for the full 48-product boilerplate cleanup.
10. **PARALLEL-FAN-OUT-FOR-DRAFTING-SCALES** — Session 4's 20-agent fan-out completed 20 product drafts in ~3.8 min wall-clock (1.13M tokens, 112 tool calls). **Rule:** larger batch sizes (25-30) are recommended for Sessions 5+ — drafting is fully parallel; only human review is sequential.
11. **OFFICESTOGO.COM-AS-PRIMARY-SOURCE-FOR-NEWLAND** — Newland (NLP-prefix) products aren't on globalfurnituregroup.com; they live on officestogo.com. **Rule:** add officestogo.com as a first-class secondary source in the auto-source URL fallback chain. 4 of 6 desks in Session 4 needed this.
12. **GREENGUARD-IS-SERIES-LEVEL-NOT-PRODUCT-LEVEL** — Global's GREENGUARD certification is published at line/series level, not per individual product page. **Rule:** defaults should mark this as `certifications_typical_series_level` with a "confirm per product" note — less aggressive auto-application.

*(bonus field-handling rule surfaced Session 4)* **SINGLE-LINE-METAFIELDS-NEED-NEWLINE-SANITIZATION** — Session 4 caught a write failure on a product with multi-size dimensions written across newlines into a `single_line_text_field`. The builder now sanitizes newlines → `" / "` for single-line fields. **Rule:** add to standing field-handling rules.

### Reference Files (established Day 17 evening, Sessions 2-3)

Four files under `data/reference/` now back the enrichment workflow:

- **`data/reference/brand-collection-routing.yaml`** — 24 manufacturer routing blocks. Maps brand → primary collections per product type. **Source of truth for routing recommendations** (overrides the weak CSV `recommended_sub_collection_*` hints — see CSV-ROUTING-RECS-ARE-WEAK-HINTS).
- **`data/reference/manufacturer-defaults.yaml`** — 24 manufacturer default blocks. Country of manufacture, warranty, `certifications_typical`. Reduces per-product decision overhead during drafting.
- **`data/reference/sku-prefix-lookup.yaml`** — 21 decoded prefix→manufacturer mappings (created Session 3 with 15; grown to 21 incl. MTY=MityBilt decoded Session 4) + 5 undecoded prefixes pending Leo decode (HDL 40, IOF 26, RIC 12, HZN 10, SCN 7). **Deterministic primary signal for brand-recovery scans** (see SKU-PREFIX-PATTERNS-ARE-DETERMINISTIC).
- **`data/reference/field-framework.md`** — Verified **13-field `specs.*` framework** (was 15, with `tagline`/`standfirst` retired). Documents data shapes, theme rendering behavior, SEO conventions, and the `body_html` split contract.

### Manufacturer dictionary — 19 in scope (was 3 at start of day)

At the start of Day 17 the dictionary held 3 manufacturers (Global, Teknion, Humanscale). Sessions 3-4 grew it to **19 in scope**, backed by 24 stub/default blocks in `manufacturer-defaults.yaml` (the extra blocks are stubs for brands not yet enriched, country = null).

- **Canada-manufactured (9):** Global Furniture Group, Teknion, Humanscale, Steelcase, Keilhauer, ErgoCentric, Heartwood, MityBilt *(added Session 4)*, plus Global sub-brands Basics, Offices To Go, ObusForme.
- **USA-manufactured (5):** Safco, Kensington, FireKing, HON, Herman Miller.
- **Country pending (stubs, `country = null` in `manufacturer-defaults.yaml`; populate when first product enriched):** Office Star Products, deflecto, Gardex, Sentry Safe, Borgo, Tayco, Foundations, Fellowes, Links Contract Furniture, 3M, Victor, Allseating.

### PR ledger — Day 17 evening (enrichment)

Added to the Day 17 shipped-work log:

- **PR [#60](https://github.com/leokatz97/officecentral/pull/60)** — Block 4 Session 1 (5 `brand:global` products enriched)
- **PR [#61](https://github.com/leokatz97/officecentral/pull/61)** — Block 4 Session 2 (8 products + reference files + readback gate hardening)
- **PR [#62](https://github.com/leokatz97/officecentral/pull/62)** — Block 4 Session 3 (183 vendor corrections + SKU prefix lookup)
- **PR [#63](https://github.com/leokatz97/officecentral/pull/63)** — Block 4 Session 4 (19 Global products enriched + MityBilt reversal)

**Day 17 total: 17 PRs** = 13 morning/afternoon (#45-56) + 4 evening enrichment (#60-63).

---

## 🟢 Day 16 — 2026-05-29 — SCHEMA-BLOG-1 → BLOG SCHEMA ON `/blogs/news` + BLOGPOSTING ENHANCEMENT (H-2/F-11 RESOLVED — SOLO-ACTIONABLE SCHEMA LANE NOW COMPLETE) · SCHEMA-BRAND-1 → 7 BRAND ENTITIES ON 6 MANUFACTURER PAGES (F-13/H-3 RESOLVED) · F-LOCALBUSINESS-IMAGE → `image` FIELD ON BOTH CHROME LOCALBUSINESS NODES (RESOLVED) · **BRAND-PAGE-TEKNION-COPY-FIX → TEKNION↔GLOBAL "SISTER COMPANIES" COPY CORRECTION ON 3 PAGES (TIER 2B `BRAND-PAGE-COPY-FIX` CLOSED)** · **SCHEMA-CORPORATE-HIERARCHY-FIX → CHROME `parentOrganization` 2-TIER → 3-TIER (BBI → BRANT BASICS → OFFICE CENTRAL GROUP OF COMPANIES); TIER 2B CLOSED** · **SMALL-ITEMS-CLEANUP-A → AUTHOR-URL-FIELD + BRAND-PAGE-COPY-SINGLE-SOURCE-PHRASING (2 TIER 2B ITEMS CLOSED); OECM ARTICLE NOW FULLY ARTICLE-RICH-RESULT-ELIGIBLE** · **BRAND-SERVICE-SCHEMA → 6 `Service` ENTITIES ("AUTHORIZED [BRAND] DEALER") ACROSS 5 BRAND-PAGE TEMPLATES VIA PARAMETERIZED SHARED SNIPPET; TIER 2B CLOSED**

### 🟢 Day 16 afternoon — BRAND-PAGE-TEKNION-COPY-FIX ✅ SHIPPED 2026-05-29

- **BRAND-PAGE-TEKNION-COPY-FIX ✅ SHIPPED 2026-05-29** (branch `feature/brand-page-teknion-copy-2026-05-29`, **independent off `main` @ `b2c1b79`** — not stacked). Closes Tier 2B **`BRAND-PAGE-COPY-FIX`**. Leo took the decision in-session this afternoon rather than routing through Steve; fix landed same day.
  - **SHIPPED:** corrected the Teknion↔Global relationship copy on **3 files** — `theme/sections/ds-lp-brands-global-teknion.liquid` (dedicated page, 8 edits: H1, hero badge/caption, intro H2 + body, FAQ 01, OECM bar, schema H1/standfirst defaults), `theme/sections/ds-lp-brands.liquid` (hub, 6 edits: killed "(which includes Teknion)" + pulled Teknion out of all 4 GFG-family roster lists + tile meta + alt), `theme/sections/ds-lp-about.liquid` (2 edits: both "GFG family (Global, Teknion, OTG, ObusForme)" lists). 16 edits total; diff balanced 18/18.
  - **PRIOR INACCURACY:** copy implied **parent/subsidiary** — treated Teknion as a "premium tier within the Global Furniture Group family," called GFG the "parent." Corrected to **sister companies under Feldberg-family ownership** per Global Furniture Group's own press release (Saul Feldberg founded Global 1966 + Teknion 1983; Joel Feldberg → Global, David Feldberg → Teknion). Verified live via web search (GFG press release + Interior Design + officeinsight) — not assumed.
  - **SCOPE (Leo's calls, in-session):** surgical/minimal — fix explicit false statements + soften tiered framing, **no page restructure**; **OECM Agreement 2025-470 + authorized-dealer claims preserved verbatim** (Teknion stays OECM-eligible, just no longer mislabeled a GFG family product); about page + all hub roster lists included for full consistency. **OTG + ObusForme left as genuine GFG brands** (correct).
  - **NO SCHEMA CHANGES:** BRAND-1's schema was already correct — Global + Teknion emit as two standalone `Brand` entities with **no `parentOrganization`** between them. This fix aligns the *visible copy* with the schema's already-accurate sister-company framing. (The 2 `parentOrganization` refs on the page are the site-wide BBI org + LocalBusiness chrome schemas, unrelated to the Brand entities.)
  - **VERIFICATION OUTCOME:** cache-busted curl on all 3 pages — new "sister company" copy renders (dedicated 2× incl. Feldberg founding fact, hub 4×, about 2×); old "premium tier"/"parent"/"which includes Teknion" = **0**; BRAND-1 Brand entities intact (Global + Teknion, no parent/sub link); F-LOC-IMG image on both chrome LB nodes intact; OECM/dealer claims preserved (2025-470 ×12, dealer ×9). No-regression control (Keilhauer): Brand schema + chrome + F-LOC-IMG all intact, no Teknion bleed. Leo manual spot-check confirmed all 3 pages read right.
  - **Theme check held at `2833/165`** (run from `theme/`) — copy edits don't change the Liquid lint surface, as expected.
  - **Residual flagged (not touched, scope-honored):** dedicated-page diff card L195 still says BBI offers the range *"without mixing manufacturers"* — slightly soft now that Teknion is a separate manufacturer, but reads as BBI's single-source convenience; possible later micro-pass, not in surgical scope. Logged as Tier 2B `BRAND-PAGE-COPY-SINGLE-SOURCE-PHRASING` (below).
  - **BRAND-PAGE-COPY-SINGLE-SOURCE-PHRASING ✅ RESOLVED 2026-05-29 (PR #47)** (Tier 2B, low priority, ~5 min OR no-action, surfaced during BRAND-PAGE-TEKNION-COPY-FIX Phase 3 self-catch) — The dedicated Global/Teknion page's diff card (`theme/sections/ds-lp-brands-global-teknion.liquid` L195) claims BBI offers the range *"without mixing manufacturers."* Now that Teknion is reframed as a **separate manufacturer** (sister company to Global, not a GFG family member), the claim's interpretation matters: the **"single-source dealer convenience"** reading is still accurate (one BBI quote/delivery/install across all lines); the **"single-manufacturer product line"** reading is now soft (Teknion ≠ Global's manufacturer). **Resolution options:** (a) ~5-min copy edit to rephrase toward the dealer-convenience framing (e.g. "without juggling multiple dealers" / "one source, one quote"), OR (b) close as **no-action** if "single-source dealer" was always the intended reading. Leo's call when next in this file.

### 🟢 Day 16 afternoon — SCHEMA-CORPORATE-HIERARCHY-FIX ✅ SHIPPED 2026-05-29

- **SCHEMA-CORPORATE-HIERARCHY-FIX ✅ SHIPPED 2026-05-29** (branch `feature/schema-corporate-hierarchy-2026-05-29`, **independent off `main` @ `b2c1b79`** — not stacked; theme files are conflict-free with the open `#45` Teknion-copy PR, though both PRs append to this build-state file so a small build-state merge is expected, accepted by Leo in-session). Closes Tier 2B **`SCHEMA-CORPORATE-HIERARCHY-FIX`** (was Steve-gated; Leo took the decision in-session this afternoon — same pattern as BRAND-PAGE-TEKNION-COPY-FIX — fix landed same day).
  - **SHIPPED:** chrome `parentOrganization` restructured from **2-tier → 3-tier** on **both** sitewide chrome snippets — `theme/snippets/bbi-org-schema.liquid` (the `#organization` combined `["Organization","LocalBusiness"]` @graph node) **and** `theme/snippets/bbi-localbusiness-schema.liquid` (the dedicated `#localbusiness` emitter). Identical edit on both. **Chain now:** BBI → **Brant Basics** (immediate legal parent, `url: brantbasics.com`) → **Office Central Group of Companies** (ultimate owner, `url: officecentral.com`). Was: BBI → Office Central directly, with the Brant Basics tier missing.
  - **WHY:** aligns chrome schema with BLOG-1's article body (live since this morning, PR #43), which already publicly describes the 3-tier structure — *"registered under our parent legal entity, Brant Basics, as an authorized OECM Supplier Partner under Agreement 2025-470."* The chrome lagging that public description was a known accuracy gap; this session closes it.
  - **DESIGN DECISIONS (surfaced Phase 1/2, Leo-approved):**
    * **Nested-chain structure** (NOT sibling `@graph` entities with `@id` refs) — chosen by correctly applying the runbook's "match existing pattern" rule. The existing pattern is inline nested `parentOrganization` objects (Office Central was a nested object with no `@id`), and `bbi-localbusiness-schema` is a single top-level object (not a `@graph`). Nesting `parentOrganization` within `parentOrganization` supports 3 tiers cleanly with zero topology change; the sibling-`@id` approach would have been a larger restructure with no validator benefit.
    * **Detail level matched Office Central's existing 3 fields** (`@type` + `name` + `url`) — no fabricated `legalName`/`foundingDate`/`address`/`@id` invented for Brant Basics. Symmetric: no field present on one parent and absent on the other.
    * **`brantbasics.com` URL is honest** — already present in BBI's `#organization` `sameAs` array, so we surface a publicly-acknowledged entity, not private corporate info.
    * **Name kept "Office Central Group of Companies"** (not bare "Office Central") for consistency with existing chrome + the about/contact prose pages.
  - **VERIFICATION OUTCOME (cache-busted curl + Leo manual RRT):**
    * **PDP `boulevard-system-3` fully converged** — both chrome nodes emit the identical 3-tier chain; cross-page + cross-snippet **byte-identical** (4 `parentOrganization` blocks compared; when converged all collapse to a single serialization). Homepage also converged (sitewide chrome confirmed).
    * **RRT (Leo manual, PDP): 0 errors**, 3-tier chain (BBI → Brant Basics → Office Central Group of Companies) renders correctly in the Organization detail view. **Organisation row count stayed at 2** — RRT counts top-level `Organization`-typed entities and does NOT increment for nested `parentOrganization` objects; the nested chain is recognized in the field strings but doesn't change the headline count (matched the "more likely" Phase 4 prediction). The 3 pre-existing non-criticals (Product/Merchant/LB rows) unchanged, none caused here.
    * **`brands-keilhauer` mid-propagation at session close** — Shopify internal page-cache oscillating new/stale; schema source byte-confirmed correct (Phase 3 API byte-compare); RRT will reflect once cache flushes. Per the source-level-proof lesson below, not gating.
  - **NO REGRESSION:** PDP `boulevard-system-3` — F-LOC-IMG `image` on both LB nodes intact, CRIT-1b/1c Product node intact (offers + `brand: "Brant Business Interiors"`), BreadcrumbList 4 items. Brand `brands-keilhauer` — BRAND-1 Keilhauer Brand entity intact. Homepage chrome 3-tier confirmed.
  - **Pre-write discipline:** preflight PASS (fresh re-run, watcher clear, role=main verified on `186373570873`); both snippets backed up to `data/backups/2026-05-29-corporate-hierarchy/`; pre-write drift **NO DRIFT** on both vs LIVE pulled from `186373570873`; local JSON-parse confirmed both chains valid pre-PUT. Sequenced PUT (both independent, `updated_at 14:27:31`), 30s CDN wait, each post-PUT byte-compare **BYTE-IDENTICAL**. **Theme check held `2833/165`** (JSON-content-only edit = 0 new Liquid lint surface).
  - **OPERATIONAL LESSON (SCHEMA-CORPORATE-HIERARCHY-FIX, 2026-05-29) — source-level byte-verify + one converged rendered page = sufficient verification for sitewide chrome changes.** When (a) the API byte-compare confirms identical source on the live theme AND (b) at least one rendered page is fully converged showing the correct output, additional page convergence is **confirmation, not gating** — identical source must render identically once each page's internal page-cache TTL flushes. The "2–3 consecutive stable reads" discipline matters when there is *no* source-level proof; here there was. This complements the existing Shopify-internal-page-cache lesson (under SCHEMA-BLOG-1): that one explains *why* `?cb=` can't force convergence (`cf-cache-status: DYNAMIC`, own-TTL eventual consistency); this one says *what is sufficient to stop waiting*. Saved ~4+ min of poller wait — the brand page never hit 3 consecutive new-gen reads in ~6 min of polling, yet the fix was provably correct from byte-compare + the converged PDP/homepage.

- **SMALL-ITEMS-CLEANUP-A ✅ SHIPPED 2026-05-29** (afternoon; branch `feature/small-items-cleanup-a-2026-05-29`, off `main` @ `b2c1b79`). Bundled two tiny Tier 2B closes into one approval-gated write session. Chronologically lands **after** this afternoon's SCHEMA-CORPORATE-HIERARCHY-FIX (`f8d83f5`, separate unmerged branch) and Steve's OECM-article featured-image upload. Files touched: **2** (`theme/sections/ds-article.liquid`, `theme/sections/ds-lp-brands-global-teknion.liquid`).
  - **SHIPPED — AUTHOR-URL-FIELD:** added `url` to the BlogPosting `author` Person object in `ds-article.liquid` (value `https://www.brantbusinessinteriors.com/pages/about` — the live `/pages/about` page where the business/people are introduced; HTTP 200 verified, only honest candidate, no fabrication). Resolves the pre-existing RRT "Missing field 'url' (optional)" non-critical on the author Person.
  - **SHIPPED — BRAND-PAGE-COPY-SINGLE-SOURCE-PHRASING:** resolved via **Option 3 rephrase** of the L195 "Tiered" diff card on `ds-lp-brands-global-teknion.liquid` — `without mixing manufacturers or finish palettes` → **`without juggling separate dealers or mismatched finishes`**. Removes the manufacturer-count claim entirely; honestly captures BBI's actual value prop (single-source dealer + finish coordination across the lineup) without contradicting yesterday's TEKNION-COPY-FIX reframing of Teknion as a separate Feldberg-family manufacturer.
  - **BONUS OUTCOME:** combined with this afternoon's featured-image upload, the OECM article BlogPosting is now **fully Article rich-result eligible — first BBI content to clear the full required-field bar** (image + author + headline + datePublished + publisher all populated). RRT Articles row now **clean, 0 non-criticals**: `image` resolved content-side (Steve's featured-image upload), `author.url` resolved via this session's PUT.
  - **DESIGN DECISIONS RECORDED:**
    * **Option 3 rephrase chosen over Option 1 ("manufacturer families")** — Option 1 quietly reintroduced the TEKNION-COPY-FIX contradiction at the "family" abstraction level (you *are* mixing manufacturers within the GFG family). Option 3 sidesteps the manufacturer-count claim entirely and leans on the dealer + finish-coordination framing the page actually sells. (Leo decision, logged.)
    * **Decoupled git artifact from PUT payload** (see new operational lesson) — `ds-lp-brands-global-teknion.liquid` was PUT from the LIVE-pulled copy (which carries the unmerged TEKNION-COPY-FIX content) + the one L195 edit, so LIVE received ONLY the L195 change and kept all 7 TEKNION-COPY-FIX blocks. The git commit edits the off-main file → a clean one-line L195 diff vs `main`. `ds-article.liquid` needed no decouple (local == LIVE, IDENTICAL).
  - **VERIFICATION OUTCOME:**
    * **RRT (Leo manual, OECM article): 0 errors; Articles row CLEAN** (both pre-existing non-criticals resolved). Fully Article-eligible.
    * Article `author.url`: source byte-verify post-PUT **IDENTICAL**; converged render nodes show `/pages/about` (Shopify-internal-page-cache oscillation, same as SCHEMA-BLOG-1). BLOG-1 invariant intact (`articleSection` + `keywords` both present).
    * Brands page: L195 rephrase live (old phrase absent); **all 7 TEKNION-COPY-FIX blocks intact on live** (13 sister-brand/Feldberg markers) — decoupled PUT preserved them, no clobber.
  - **NO REGRESSION:** PDP `boulevard-system-3` (CRIT-1b/1c + F-LOC-IMG, 37 image markers, 3-tier chain converged); brand `brands-keilhauer` (BRAND-1 `Keilhauer` + F-LOC-IMG); **SCHEMA-CORPORATE-HIERARCHY-FIX 3-tier `parentOrganization` chain (BBI → Brant Basics → Office Central Group of Companies) confirmed in LIVE source on both chrome snippets + converged on PDP** (keilhauer/article rendered 2-tier = afternoon-chrome page-cache lag, not a regression — session never touched chrome).
  - **Pre-write discipline:** preflight PASS (fresh re-run, watcher clear, role=main `186373570873`); both files backed up to `data/backups/2026-05-29-small-items-cleanup-a/`; pre-write drift — `ds-article.liquid` **IDENTICAL**, `ds-lp-brands-global-teknion.liquid` **SEMANTIC_MISMATCH** (LIVE ahead of `main` from unmerged TEKNION-COPY-FIX → triggered the decouple). Sequenced PUT (both independent), each post-PUT byte-compare **IDENTICAL** vs intended state (article vs working-tree; brands vs LIVE-pulled+edit). 30s CDN wait. **Theme check held 2833/165** (small copy/schema edits = 0 new Liquid lint surface).
  - **OPERATIONAL LESSON — BRANCH-BASE-VS-LIVE-DRIFT-FROM-OPEN-PRS** — when branching a new session off `main` while open-but-unmerged PRs exist that have already PUT to production, files those PRs touched will have `main` lagging LIVE. PUT-ing the off-main file directly to LIVE would **clobber the unmerged-PR content** on production. Pre-write byte-compare against LIVE catches this drift. Two valid workflow patterns: **(A) STACK** the new branch off the latest open PR's tip (matches morning's #42-on-#41, #43-on-#42 pattern) — branch from where LIVE actually is, so local == LIVE, PUT + byte-verify work normally, patch-id rebase cleans up when the parent PR merges. **(B) DECOUPLE** git artifact from PUT payload (this session's resolution) — edit the off-main file for the git commit (keeps a clean diff vs `main`), edit the LIVE-pulled copy for the actual PUT (preserves the open-PR content), post-PUT byte-verify against the LIVE-state-plus-edit, NOT the off-main local. Pattern A is cleaner if planned upfront; Pattern B works when the mismatch is discovered mid-session with backups already taken. Discovered during SMALL-ITEMS-CLEANUP-A Phase 3 pre-write drift check — same family as the SCHEMA-CRIT-1 "assumed LIVE state without verification" incidents but a different mechanism (branch-base lag, not watcher auto-PUT).

### 🟢 Day 16 afternoon — BRAND-SERVICE-SCHEMA ✅ SHIPPED 2026-05-29

- **BRAND-SERVICE-SCHEMA ✅ SHIPPED 2026-05-29** (branch `feature/brand-service-schema-2026-05-29`, **stacked on `#46` SCHEMA-CORPORATE-HIERARCHY-FIX @ `f8d83f5`**). Closes Tier 2B **`BRAND-SERVICE-SCHEMA`** (logged during SCHEMA-BRAND-1). 6 `Service` entities across 5 brand-page templates.
  - **SHIPPED:** 6 `Service` JSON-LD nodes ("Authorized [Brand] Dealer") across the 5 in-scope brand-page sections — keilhauer (1), global-teknion (**2**: `service-global` + `service-teknion`), otg (1), heartwood (1), obusforme (1) — emitted via the **existing** `theme/snippets/bbi-service-jsonld.liquid` snippet. Files touched: **6** (1 snippet + 5 sections).
  - **DESIGN DECISIONS (surfaced Phase 1/2, Leo-approved):**
    * **"Authorized [Brand] Dealer" framing** chosen over corporate-genealogy framing — focus on brand + BBI's dealer capability + OECM; no Feldberg/ownership references in the Service descriptions.
    * **Extended the existing shared snippet — NOT a new `{% case %}` snippet.** ⚠️ **Plan-vs-built correction:** the session brief specified a *new* snippet with a centralized `{% case brand %}` block + single brand-slug param. Phase 1 found `bbi-service-jsonld.liquid` **already existed** (SCHEMA-CRIT-2, committed `97b9416`) with a **param-passing interface** in active use by 6 industry/segment callers; a `{% case %}` rewrite would have broken them. Built instead: a **one-line backward-compatible `@id` parameterization** — `@id` changed from hardcoded `#service` to `#{{ id_suffix | default: 'service' }}`. Per-brand `service_name`/`service_description`/`service_type`/`id_suffix` are passed from each render call (mirrors the sibling `bbi-brand-jsonld` pattern). The 6 existing industry callers omit `id_suffix` → default `'service'` → **byte-identical output** (zero regression). This preserves single-source-of-truth for `Service` emission across industry + brand callers.
    * **`id_suffix` per brand** (`service-keilhauer`, `service-global`, `service-teknion`, …) gives each node a distinct `@id` — required so the dual Global/Teknion page emits two non-colliding `Service` nodes.
    * **`provider` `@id`-refs chrome BBI Org** (`https://office-central-online.myshopify.com/#organization`) — entity-graph coherence with BRAND-1, SCHEMA-CORPORATE-HIERARCHY-FIX, BLOG-1 publisher refs.
    * **`areaServed` kept as the existing snippet's `AdministrativeArea / "Ontario, Canada"`** (NOT chrome Org's `State / Ontario / CA`) — chosen for consistency with the 6 industry `Service` nodes over a byte-match to chrome. Both valid + semantically equivalent; format inconsistency logged as Tier 2B `SCHEMA-AREASERVED-FORMAT-HARMONIZE`.
    * **6 `Service` descriptions Leo-approved**, full-name "Brant Business Interiors" throughout — Keilhauer + OTG had mid-sentence "BBI" in the supplied copy; swapped to full name per the locked voice rule.
  - **ergocentric brand page EXCLUDED** — discovered in Phase 1 (6th brand page; has a BRAND-1 Brand entity, but no Leo-approved `Service` description). Logged as Tier 2B `BRAND-SERVICE-SCHEMA-ERGOCENTRIC`.
  - **DECOUPLE on `ds-lp-brands-global-teknion.liquid`:** LIVE carries `#45` (TEKNION-COPY-FIX) + `#47` (SMALL-ITEMS-CLEANUP-A L195) content the off-`#46` tree lacks. Git artifact = off-`#46` file + 2 render calls (clean render-only diff); PUT payload = **LIVE-pulled + same 2 render calls** (preserves #45 + #47); post-PUT byte-verify against LIVE+edit, not the off-`#46` tree. Render-call region byte-identical in both → graft structurally clean.
  - **VERIFICATION OUTCOME (cache-busted curl + Leo manual RRT on `brands-keilhauer` + `brands-global-teknion`):**
    * 6 `Service` nodes live; all fields present (name, suffixed `@id`, serviceType "Furniture Dealer", description, provider `@id`-ref, areaServed, url); JSON valid; em-dashes + "OECM Agreement 2025-470" intact.
    * **RRT: 4 valid items / 0 errors per brand page, no new non-criticals.** No dedicated "Services" row (RRT-scope limitation — `Service`/`Brand` entities are parsed/stored in Google's knowledge graph but don't surface as dedicated RRT rows). Local businesses + Organization rows unchanged.
    * `brands-keilhauer` edge-cache lagged ~4 min at first surface, then converged (RRT crawl 16:46:27 clean, matching Global/Teknion 16:46:16) — per the source-level-proof lesson, not gating.
  - **NO REGRESSION:** BRAND-1 Brand entities intact on all brand pages (alongside new `Service`); F-LOC-IMG `image` on both chrome LB nodes; SCHEMA-CORPORATE-HIERARCHY-FIX (#46) 3-tier `parentOrganization` on chrome; #45 + #47 intact on Global/Teknion LIVE; PDP `boulevard-system-3` CRIT-1b/1c intact (Product + Offer + image, 0 empty/null fields).
  - **Pre-write discipline:** preflight PASS (fresh; watcher clear; role=main on `186373570873`); backups + LIVE pulls + Global/Teknion PUT-payload to `data/backups/2026-05-29-brand-service-schema/`; pre-write drift matched Phase 1 (5 IDENTICAL + Global/Teknion MISMATCH confirming decouple). Sequenced PUT (snippet first → 4 standard sections → Global/Teknion LIVE+edit last), 30s CDN wait, all 6 post-PUT byte-compare **MATCH**. **Theme check held `2833/165`** (pure Liquid render-call additions + 1 snippet line = 0 new lint surface).

- **SCHEMA-BLOG-1 ✅ SHIPPED 2026-05-29** (branch `feature/schema-blog-1-2026-05-29`, off `24894b9` = F-LOC-IMG tip, includes BRAND-1). Closes audit **H-2 / F-11** (Blog landing emitted no `Blog` schema) — **the last solo-actionable schema item.** ⚠️ **Numbering note:** the session brief labelled this "H-3", but the audit doc is unambiguous — **BLOG-1 = H-2** (Blog/F-11); **H-3 = Brand pages**, already resolved by SCHEMA-BRAND-1 this morning. Marked **H-2** resolved. Files touched: **3** (1 new snippet + 2 sections).
  - **SHIPPED:**
    * **NEW `theme/snippets/bbi-blog-jsonld.liquid`** — `Blog` JSON-LD on `/blogs/news` (rendered from `ds-blog-list.liquid`): `name` (section heading), `description`, `@id` (`canonical_url#blog`), `url`, `mainEntityOfPage`, `publisher` `@id`-ref to chrome `#organization`, and a **`blogPost[]` enumeration** of `blog.articles` (currently 1, future-proof to N).
    * **`ds-article.liquid` BlogPosting enhancement** (enhance-in-place, not duplicate) — added `articleSection` (first tag) + `keywords` (joined tags); rewrote the `image` block to honest native dimensions (`article.image.width`/`.height`, replacing a hardcoded `width:1200`). All additions guarded — omitted when blank.
  - **PHASE 1 KEY FINDING (brief premise corrected):** the brief assumed net-new BlogPosting emission, but a **BlogPosting was already LIVE** (inline in `ds-article.liquid`, shipped in the "H-1 batch-fix 2026-05-23" — Person author, publisher `@id`-ref, datePublished/dateModified, articleBody). A second emitter would have **duplicated** it. Re-scoped with Leo to **(a)** net-new `Blog` on the index (genuinely missing — what H-2/F-11 actually was) + **(b)** enhance the existing inline BlogPosting.
  - **DESIGN DECISIONS RECORDED:**
    * **"Enhance in place"** — existing inline BlogPosting enhanced (articleSection/keywords/honest-image), NOT refactored to a snippet nor duplicated. New snippet is for the `Blog` index entity only.
    * **`domain_base = canonical_url | remove: blog.url`** derivation (no hardcoded host) so the index `blogPost[].@id` values are **byte-identical** to the per-post `BlogPosting.@id` (`canonical_url#article`) → cross-page entity-graph coherence.
    * **Tags richer than Phase 2 modeled** — the OECM post carries **4 tags** (`education, OECM, procurement, school boards`), not the 1 ("education") the brief stated → `keywords` is rich; `articleSection` takes the first ("education").
    * **Image: honest omission** via `{% if article.image %}`. The post has **no featured image set** (`article.image` falsy) so the JSON-LD `image` is omitted, not fabricated. The hero readers see (`IMG_2566.jpg`) is Shopify's *derived first-inline-body-image* (its og:image fallback) — a distinct mechanism from `article.image`, which is why the image block never rendered live, before or after this session.
    * **`Blog.name`** = section heading "Guides, Tips & Industry Insights" with `blog.title` ("News") as fallback — more descriptive than the raw blog title.
  - **VERIFICATION OUTCOME (RRT, Leo manual + cache-busted curl):**
    * **5 valid items / 0 errors on BOTH `/blogs/news` and the article page.** Schema parsed cleanly.
    * **BONUS — index-level Articles recognition:** RRT shows an **Articles row on the INDEX page too**, not just the per-post page — Google resolves the `blogPost[].@id` references to the real BlogPosting entity and surfaces it at the referencing page. Validates the enumerate-on-index design (see new operational lesson).
    * **Cross-page `@id` BYTE-IDENTICAL confirmed**: index `blogPost[0].@id` == article `BlogPosting.@id`.
    * **2 non-criticals on the Articles row, both honest optional-field omissions, NEITHER caused by this session:** (1) `image` (content-side — no featured image → STEVE-SET-BLOG-FEATURED-IMAGE), (2) `author.url` (pre-existing — the inline BlogPosting's Person never had a url; the author field was untouched → AUTHOR-URL-FIELD). The article *schema* is valid; *rich-result display* is gated on the featured image.
    * Local businesses non-critical persists (`priceRange` M-2 asymmetry, deliberate per POLISH-1); Organisation row clean (F-LOC-IMG this morning).
  - **NO REGRESSION:** PDP `boulevard-system-3` (CRIT-1b/1c + F-LOC-IMG), sub-collection `medium-back-seating` (CRIT-3 ItemList **24 items** at `CollectionPage.mainEntity` + CRIT-4 0 microdata + F-LOC-IMG), brand `brands-keilhauer` (BRAND-1 `name:"Keilhauer"` + F-LOC-IMG), chrome (Org/LB @graph + WebSite) intact on both blog pages.
  - **Pre-write discipline:** preflight PASS (fresh re-run, role=main `186373570873`); both sections backed up to `data/backups/2026-05-29-schema-blog-1/`; pre-write drift **IDENTICAL** on both vs LIVE pulled from `186373570873`; theme check baseline 2833/165. Sequenced PUT (snippet → ds-blog-list render-caller → ds-article), each post-PUT byte-compare **IDENTICAL**. **Theme check held 2833/165** (new snippet 0 offenses).
  - **OPERATIONAL LESSONS (SCHEMA-BLOG-1, 2026-05-29):**
    * **Shopify internal page-cache vs CDN edge cache distinction.** After a theme PUT, Shopify's own internal page-cache layer (`cf-cache-status: DYNAMIC` — i.e. NOT Cloudflare-cached) oscillates between old and new generations and **IGNORES `?cb=` query params** — cache-busting won't force a clean read. It is eventually-consistent on its own TTL. This is different from the CDN-edge stale-first-hit pattern (where a refetch clears). **For verification during convergence: capture multiple new-gen reads, ignore stale fetches, and trust the API-level byte-identical confirmation.** Discovered during SCHEMA-BLOG-1 Phase 3 propagation — a poller ran 8+ min without ever hitting 3 consecutive stable reads; `cf-cache-status: DYNAMIC` ruled out Cloudflare; schema correctness was confirmed independent of full convergence (API byte-identical + repeated new-gen captures).
    * **Cross-page `@id` coherence enables index-level rich-result recognition.** When `Blog.blogPost[]` entries use `@id` values **byte-identical** to the per-post `BlogPosting.@id` (achieved via `domain_base = canonical_url | remove: blog.url`, NOT a hardcoded host), RRT surfaces the referenced entities as an **Articles row on the INDEX page**, not just the per-post page. Generalizes: any entity-graph schema using `@id` refs to dereferenceable entities can surface those entities at the *referencing* page's RRT, not only at the canonical page. Discovered during SCHEMA-BLOG-1 Phase 4 (index showed Articles: 1 valid via `blogPost[0].@id` reference — not predicted).

- **F-LOCALBUSINESS-IMAGE ✅ SHIPPED 2026-05-29** (branch `feature/f-localbusiness-image-2026-05-29`, off `main`). Closes the recurring **"Missing field 'image' (optional)"** non-critical WARN that appeared on every RRT screenshot for 5+ days across PDP / collection / brand pages. Additive ImageObject on both sitewide chrome LocalBusiness nodes. Files touched: **2**.
  - **SHIPPED:** `image` field added to both chrome LocalBusiness nodes — `theme/snippets/bbi-org-schema.liquid` (the `#organization` combined `["Organization","LocalBusiness"]` @graph node, inserted right after `logo`) **and** `theme/snippets/bbi-localbusiness-schema.liquid` (the dedicated `#localbusiness` emitter, inserted after `url`). **Identical ImageObject on both** for entity-graph consistency: `{"@type":"ImageObject","url":".../bbi-about-grid-01-storefront-day.jpg","width":800,"height":600}`. Image asset: **`bbi-about-grid-01-storefront-day.jpg`**, Shopify CDN `https://www.brantbusinessinteriors.com/cdn/shop/files/bbi-about-grid-01-storefront-day.jpg`, native 800×600.
  - **DESIGN DECISIONS RECORDED:**
    * **Photo: Day storefront** (#2 from the About Us photo inventory — Steve categorically approved all About Us photos Day 15 morning as "all real and usable"). Google's LocalBusiness convention favors a building-exterior photo; the daytime storefront is the conventional baseline for thumbnail legibility (vs night/showroom/team alternates).
    * **ImageObject pattern** (`@type`/`url`/`width`/`height`) — matches the existing `logo` ImageObject pattern in the chrome rather than a bare URL string.
    * **Same image on both nodes** — they describe the same business; divergent images would create entity-graph inconsistency. Verified scope: grep confirmed these are the ONLY two `@type: LocalBusiness` emitters in `theme/` (the other 4 matches are comments / the superseded `ds-lp-contact` node).
  - **VERIFICATION OUTCOME:**
    * HTML emission verified via cache-busted curl across **4 page types** — PDP (`boulevard-system-3`), sub-collection (`medium-back-seating`), brand (`brands-keilhauer`), dedicated-LB landing (`/pages/oecm`). Both nodes render the identical ImageObject on every page (consistent across the @graph LocalBusiness AND the dedicated emitter).
    * **RRT (Leo manual, 3 pages incl. `/pages/oecm`): Local businesses non-critical reduced 3 → 1** — was `#localbusiness` "Missing image" + `#organization` "Missing priceRange" + "Missing image" (3); now `#localbusiness` clean + `#organization` "Missing priceRange" only (1). **Organisation row CLEARED across all 3 spot-checked pages (bonus)** — `image` was being flagged at BOTH the Organization and LocalBusiness type-rows of the dual-typed `#organization` node; F-LOC-IMG cleared both. Item counts intact (5 on collection/OECM, 7 on PDP); **0 errors anywhere.**
    * **The persistent Local businesses non-critical is `priceRange` on `#organization`** — that's the **M-2 asymmetry from POLISH-1** (deliberate: we don't assert `$$` on the Brand-encompassing `#organization` node for a quote-based commercial catalog, only on the dedicated `#localbusiness` node). NOT a F-LOC-IMG failure; the badge persists by design.
  - **NO REGRESSION:** PDP `boulevard-system-3` — CRIT-1b/1c invariants intact (`itemCondition`, `hasMerchantReturnPolicy`, `shippingDetails`, `price:"0"` + `priceSpecification "Price available on request"`; `priceValidUntil` correctly ABSENT on the quote-only branch). Sub-collection `medium-back-seating` — CRIT-3 ItemList (24 enumerated products at `CollectionPage.mainEntity`) + CRIT-4 (0 card microdata) intact. Brand `brands-keilhauer` — BRAND-1 Brand entity intact (`name: "Keilhauer"`, `sameAs: ["https://www.keilhauer.com"]`). Chrome consistency (Org + LocalBusiness @graph + WebSite) valid on every page. F-LOC-IMG touched only the two chrome LB snippets — the PDP Offer / collection ItemList / brand Brand come from different snippets entirely.
  - **OPERATIONAL LESSON — RRT applies field-checks PER-TYPE, not per-entity.** For a dual-typed node like `@type ["Organization","LocalBusiness"]`, a missing field can be flagged under multiple type-rows simultaneously when the field applies to multiple types. **Universal fields (`image`, `name`, `url`, `description`) get cross-row flagging** (this is why fixing `image` once cleared BOTH the Organisation and Local businesses image-warnings on `#organization`); **type-specific fields (`priceRange` for LocalBusiness) get single-row flagging** (which is why the Local businesses badge persists on `priceRange` but the Organisation row went clean). Useful for predicting cleanup scope on dual-typed entities.
  - **Pre-write discipline:** preflight PASS (watcher clear, role=main verified on `186373570873`) — re-run fresh immediately before PUT, PASS again; both snippets backed up to `data/backups/2026-05-29-f-localbusiness-image/`; pre-write drift check both **SEMANTIC_MATCH** (EOF-newline only, zero substantive drift vs LIVE pulled from `186373570873`); theme-check baseline 2833/165. Sequenced PUT (both independent), each post-PUT byte-compare **SEMANTIC_MATCH** (content byte-identical); 30s CDN wait + transient edge-cache variance noted on the brand page (some PoP nodes held pre-edit full-page cache, expire on own TTL — asset confirmed live on the published theme). **Theme check held 2833/165** (additive JSON literals = 0 new Liquid lint surface; per-file delta 0 on both edited snippets).

- **SCHEMA-BRAND-1 ✅ SHIPPED 2026-05-29** (branch `feature/schema-brand-1-2026-05-29`, off `main` @ `2b29f0a`). Net-new Brand JSON-LD emission on the 6 manufacturer/brand landing pages — closes audit **F-13 / H-3** (audit doc tagged it both H-2 and H-3; resolved here). CRIT-2-shaped: one shared parameterized snippet + N template render-calls.
  - **SHIPPED: 7 Brand entities across 6 pages** via new `theme/snippets/bbi-brand-jsonld.liquid` (single shared snippet). Single Brand on 5 pages (ergoCentric, Heartwood, Keilhauer, ObusForme, OTG); **dual Brand on `brands-global-teknion`** (Global Furniture Group + Teknion as two standalone entities). 6 section files edited (render-call appended after the uniform `bbi-footer` render line); 1 new snippet. Files touched: 7.
  - **DESIGN DECISIONS RECORDED:**
    * **`@type` = `Brand`** (not Manufacturer/Organization) — chosen to MATCH the PDP emitter's `brand.name` reference (`bbi-product-jsonld.liquid:68-71` emits `{"@type":"Brand","name":<vendor>}`). Entity-graph coherence: the Brand declared on each page is the *same* Brand entity hundreds of PDPs reference by name. Manufacturer would have created a type mismatch.
    * **Multi-brand mechanic via `id_suffix` param** (default `'brand'`) — backward-compatible single-brand `@id` fragment `#brand`; extensible to multiple Brands on one page via distinct fragments (`#brand-global`, `#brand-teknion`). The combined page renders the shared snippet twice with different params — no snippet variant needed.
    * **Sister-company structure for Global/Teknion: NO `parentOrganization` between them.** Per Leo verification (sourced to Global Furniture Group's own press release on Saul Feldberg's passing): Saul Feldberg founded Global (1966) and established Teknion (1983); Joel Feldberg = Global CEO, David Feldberg = Teknion CEO. They are **independent SISTER companies under common Feldberg family ownership — NOT parent/subsidiary.** Two standalone Brand entities, no relationship asserted between them. BBI is a confirmed Teknion dealer (teknion.com/ca/locations/locations-dealers, Leo verified). OTG + ObusForme *are* genuine GFG brands; Teknion is not.
    * **Honesty principle preserved (per CRIT-1c):** no `logo` field (no manufacturer logo assets on file — `section.settings.logo` is BBI's logo, not the brand's → omitted, logged as MANUFACTURER-LOGO-ACQUISITION Tier 2B); no `parentOrganization` (relationship doesn't fit clean parent/sub for sister companies, and BBI is dealer not parent for the independents); descriptions carry brand nuance in plain text rather than fabricated schema cross-references. Every emitted field backed by real/verified data; absent fields omitted entirely (no empty strings/nulls).
  - **TWO HONESTY CATCHES IN PHASE 2 (sameAs verification):**
    * **Heartwood** — ruled out the dead `heartwoodmfg.com` (my first guess, 000/no-resolve), verified the correct live **`heartwood.ca`** (Kelowna BC laminate-desking & casegoods manufacturer, confirmed via WebSearch).
    * **ObusForme** — entity disambiguation catch. The office-seating ObusForme is a **GFG product line** (sameAs → `https://www.globalfurnituregroup.com/ca/products/obusforme`), **NOT** the consumer wellness brand at `obusforme.com` (different entity, different products — heating pads/cushions). Extended the omission>fabrication principle: when the *correct* entity URL is reachable with one more click, reach for it rather than dropping the field or pointing at the wrong entity.
    * Other 4 verified clean: ergocentric.com (WebFetch-confirmed), globalfurnituregroup.com (title-confirmed), keilhauer.com (title-confirmed), officestogo.com (WebSearch-confirmed official OTG site; curl hits a UA/cookie redirect-loop but it's the verified live entity site).
  - **VERIFICATION OUTCOME (honest framing):**
    * HTML emission verified via cache-busted curl: `brands-global-teknion` **2→4** ld+json blocks (dual Brand), single-brand pages **2→3**. Distinct `@id`s on the dual page confirm the `id_suffix` mechanic works as designed. All Brand fields render with **zero empty/null values** across all 3 spot-checked pages (global-teknion, keilhauer, obusforme).
    * **RRT: 4 valid items / 0 errors** across all 3 spot-checked pages. RRT does NOT display Brand entities in its UI (Brand isn't rich-result-eligible — see new operational lesson below), but the **0-errors result confirms RRT parsed the Brand JSON-LD cleanly.** Items-count did NOT increase (predicted +1/+2 was wrong — RRT counts rich-result-eligible items, not total schema blocks). Schema serves entity-graph / knowledge-graph / AEO grounding, not a rich-result trigger (always the known purpose).
  - **NO REGRESSION:** PDP `boulevard-system-3` (quote-only canary) — offers present, `price:"0"`, `itemCondition: NewCondition`, `hasMerchantReturnPolicy` + `shippingDetails` PRESENT, `priceSpecification: "Price available on request"` (CRIT-1b/1c invariants intact). Sub-collection `medium-back-seating` — 0 card microdata (CRIT-4), ItemList enumerates 24 products (CRIT-3). Snippet renders didn't touch PDP/collection paths; verified anyway.
  - **Pre-write discipline:** preflight PASS (watcher clear, role=main verified on `186373570873`); 6 sections backed up to `data/backups/2026-05-29-schema-brand-1/`; pre-write drift check all 6 IDENTICAL vs LIVE; theme-check baseline 2833/165. Sequenced PUT (snippet FIRST, then 6 sections alphabetically), each post-PUT byte-compare **IDENTICAL**; 30s CDN wait; post-CDN canary verify. **Theme check held 2833/165** (new snippet = 0 offenses).

- **BACKLOG-TRACKER-CLEANUP ✅ SHIPPED 2026-05-29** (PR #49, branch `feature/backlog-tracker-cleanup-2026-05-29`, docs-only — no production write). Reorganized this file's backlog (Tier 1 / Tier 2 / Tier 2B) into Pending-top / Completed-bottom subsections, most-recent-first, and corrected **7 stale-status items** that had shipped per git but were still marked open/blocked/pending in the inventory (WATCHER-FORENSICS, SCHEMA-CRIT-NEW-1, F-LOCALBUSINESS-IMAGE, WORKING-TREE-CLEANUP, THEME-CHECK-CONFIG, BRAND-SERVICE-SCHEMA, SCHEMA-CORPORATE-HIERARCHY-FIX). Companion all-tiers Cowork prompt emitted to sync the BBI Launch Tracker artifact.
  - **OPERATIONAL LESSONS (BACKLOG-TRACKER-CLEANUP, 2026-05-29):**
    1. **BUILD-STATE-INVENTORY-DRIFT-FROM-SHIPPED-REALITY.** Build-state has two structures that need to stay synchronized: chronological session entries ("we shipped X today") and Tier 2B inventory entries ("X is pending/in-progress/completed"). Each session reliably adds the chronological entry, but inventory entries only update if the session author reaches back to mark the closed item resolved. Over multi-session days and across days, stale-status accumulates: items that shipped continue to appear pending in the Tier 2B list. BACKLOG-TRACKER-CLEANUP (PR #49, Day 16) found 7 stale corrections in one sweep — 3 from same-day Day 16 sessions and 4 from Day 13-14 sessions. Forward discipline (split responsibility): the wrap text dictated from the chat side should include explicit instruction to "mark Tier 2B item X resolved in the inventory" whenever a session closes an item; Claude Code on the receiving side should treat that inventory update as part of the wrap commit. Safety net: periodic reconciliation passes (like PR #49) catch what the wrap-step discipline misses; recommended cadence is end-of-each-multi-session-day, or weekly during lighter periods.

## 🟢 Day 15 — 2026-05-29 — SCHEMA-CRIT-1c → CRIT-1 FULLY RESOLVED · SCHEMA-CRIT-4 → BARE-PRODUCT ROOT PATTERN CLOSED

- **SCHEMA-CRIT-4 ✅ COMPLETE — shipped 2026-05-29** (branch `feature/schema-crit-4-2026-05-29`, off `main` @ `55e5207` post-CRIT-1c). **Stripped — not guarded** — all `Product`/`Offer` microdata from the `ds-cs-base.liquid` product-card, matching the already-clean `ds-cc-base` + `ds-collection-base` card pattern. This is the **architectural close of the bare-Product-on-quote-only ROOT PATTERN across all 3 surfaces.**

  - **PREFLIGHT-FIRST:** `scripts/preflight-write-check.sh` → RESULT: PASS (no watcher, role=main 186373570873 confirmed). Re-run fresh immediately before the PUT — PASS again.
  - **DESIGN DECISION — STRIP over GUARD (locked Phase 1):** CRIT-3 (PR #34, `cee7f57`) already added CollectionPage + ItemList JSON-LD enumerating every product at the collection level, making per-card Product microdata **redundant in addition to buggy.** Gating `itemscope` on `is_quote_only==false` would have left microdata on buyable cards for marginal value (ItemList already enumerates them with url+position) while keeping conditional complexity. Stripping removes the bug class entirely — no quote-only branch to guard — and matches the canonical collection-enumeration pattern (CollectionPage + ItemList) used by the two already-clean templates. This was a **deletion, not a behavioral change** — lower risk than the additive CRIT-1c session.
  - **FULL 7-ATTRIBUTE STRIP (the value of Phase 1 — partial strip would have left RRT still flagging the card, since `itemprop` doesn't require `itemscope` on the same element):** (1) `itemscope itemtype="https://schema.org/Product"` on the `<article>` (line 497), (2) `itemprop="brand"` on the vendor `<p>` (512), (3) `itemprop="name"` on the title `<a>` (514), (4) `itemprop="url"` on the quote CTA `<a>` (525), (5) `itemprop="offers" itemscope itemtype="https://schema.org/Offer"` on the price `<p>` (529), (6)+(7) **full-line deletion** of the two microdata-only `<meta>` tags (`priceCurrency` 530 + `price` 531 — removed entirely, no empty-tag syntactic noise). `git diff`: 5 ins / 8 del, all subtractions. **`ds-cs-base.liquid` was the ONLY file in `theme/` carrying `schema.org/Product` microdata** — strip removes the bug class sitewide. Single file touched: `theme/sections/ds-cs-base.liquid`.
  - **BLAST RADIUS — 67 published sub-collections** render via template suffix `base` (`collection.base.json` → `ds-cs-base`). (Prior diagnosis said "up to 91"; the live published count on `template_suffix=base` is **67**.) All now show clean Product/Merchant rows in RRT.
  - **ZERO DEPENDENCIES (Phase 1 confirmed):** no Liquid `{% if %}`/`{% case %}` against itemprop values; no CSS `[itemprop]`/`[itemscope]` selectors anywhere in `theme/assets/`; no JS `querySelector('[itemprop]')`. The brand filter reads `.ds-cs__card` + **`data-vendor`** (both preserved); the `is_quote_only` branch is behavioral (price vs quote CTA), not microdata-coupled.
  - **DISCIPLINE:** backup → `data/backups/2026-05-29-schema-crit-4/`. Pre-write drift check (`scripts/preflight-byte-compare.py`, local-unedited vs LIVE pulled from 186373570873): **IDENTICAL** raw sha — confirms CRIT-3's `cee7f57` was the last write, zero drift. PUT to LIVE role=main; 30s CDN wait; post-PUT byte-compare: **IDENTICAL** (sha `f02548d4…`). updated_at → `2026-05-28T17:45:35-04:00`, size 37,704 → 37,334 bytes.
  - **RRT VERIFIED (Leo manual, 3 structural variants — `medium-back-seating` (24 products, the discovery page), `task-chairs` (10 products), `boardroom-conference-meeting` (mixed 13 = 10 buyable + 3 quote)):** all show **5 valid items / 0 errors**. **THE HEADLINE: `medium-back-seating` went from "53 items / 48 invalid" (24 invalid Product snippets + 24 invalid Merchant listings, captured in CRIT-3's RRT screenshots) → "5 valid / 0 errors."** The Product snippets **and** Merchant listings rows **vanished entirely** — the architecturally-correct outcome: no Product schema means no Product row to show. Valid items remaining: ItemList (CollectionPage, from CRIT-3), Breadcrumbs, Local businesses (with expected `F-LOCALBUSINESS-IMAGE` non-critical), Organisation. The strip didn't merely clear the invalid items — it eliminated the broken-by-design Product schema, leaving CollectionPage + ItemList as the canonical enumeration pattern.
  - **BEHAVIORAL VERIFICATION (the strip is invisible to users):** `data-vendor` preserved (JS brand filter still functions); `is_quote_only` Liquid branch intact (price renders for buyable cards — e.g. boardroom `$689.99 – $749.99` — quote CTA renders for quote-only cards); CSS unchanged; card visual structure (`<article class="ds-cs__card" data-vendor=...>`, image, vendor `<p>`, title `<a>`, price element / quote CTA) byte-identical minus the schema attributes. Cache-busted curl on all 3 confirmed **0 / 0 / 0** itemtype/itemprop/itemscope.
  - **OPERATIONAL CATCH — stale-edge-cache first-hit on `medium-back-seating`** returned the pre-strip copy (microdata still present) on the first cache-busted curl while `task-chairs`/`boardroom` were clean immediately; a no-store refetch cleared it to 0 on the next attempt. **Same async `page_cache` pattern as QW-4 and the CRIT-2 healthcare stale-cache — this is a recurring pattern on cached templates, NOT a one-off.** Standard discipline (no-cache refetch + brief wait) handles it cleanly every time; treat a single stale first-hit as expected, not a fix failure.
  - **THEME CHECK:** strip added **0** offenses — repo total held at **2833/165** exactly (canonical theme-root scan, pre-edit and post-edit identical), `ds-cs-base.liquid` held at **10** offenses (microdata attributes aren't theme-check lint targets — deletions can't add offenses and these weren't tracked, so per-file delta 0 as predicted).
  - **🏁 ROOT-PATTERN CLOSED — bare-Product-on-quote-only resolved across ALL 3 surfaces (see ROOT-PATTERN NOTE below, now historically resolved).**

- **SCHEMA-CRIT-1c ✅ COMPLETE — shipped 2026-05-29** (branch `feature/schema-crit-1c-2026-05-29`, off `main` @ `d744d38` post-stack-merge — no longer stacked). Session A (Steve-side) published the two policy pages; this session (B) wired the matching Merchant Listing schema into the PDP Product `offers` emitter. **CRIT-1 is now FULLY RESOLVED.**

  - **PREFLIGHT-FIRST:** `scripts/preflight-write-check.sh` → RESULT: PASS (no watcher, role=main 186373570873 confirmed). Re-run fresh immediately before the PUT — PASS again.
  - **POLICY PAGES VERIFIED LIVE (Phase 1 gate):** cache-busted curl confirmed both return HTTP 200 with real policy text — `/policies/refund-policy` (2,688 chars: 30-day window, restocking fee, return shipping, OECM clause) + `/policies/shipping-policy` (2,247 chars: handling 1–3 days, transit zones, quote-based costs, Canada-only). Wiring schema to empty pages would be worse than not wiring — gate passed, not halted.
  - **SHIPPED:** `hasMerchantReturnPolicy` (`MerchantReturnPolicy`) + `shippingDetails` (`OfferShippingDetails`) added to PDP Product `offers`, **both unconditional** (placed before the `price==0` split, same slot as CRIT-1b's `itemCondition`). All schema constants emitted as **full URIs** (`https://schema.org/MerchantReturnFiniteReturnWindow`, `…/ReturnByMail`, `…/ReturnShippingFees` — matching the existing `InStock`/`NewCondition` pattern). `merchantReturnLink` resolves canonically to `https://www.brantbusinessinteriors.com/policies/refund-policy` (`shop.url | append`). Single file touched: `theme/snippets/bbi-product-jsonld.liquid`.
  - **FIELD-TO-POLICY SOURCING (honesty check — every value cites a clause):** `merchantReturnDays:30` ← "Standard catalog items may be returned within 30 days"; `returnFees:ReturnShippingFees` ← "customer is responsible for return shipping costs unless… damage, defect, or our error"; `returnMethod:ReturnByMail` ← "return authorization and shipping instructions… trackable, insured shipping service"; `applicableCountry:"CA"` ← "ships within Canada"; `handlingTime` 1–3 DAY ← "In-stock items typically ship within 1–3 business days"; `transitTime` 1–15 DAY ← min "Peterborough… 1–2 business days" / max "Freight (Canada-wide)… 5–15 business days"; `shippingDestination` CA ← "ships and delivers throughout Ontario and across Canada".
  - **DELIBERATE OMISSIONS (omission > fabrication — Phase 1 reasoning, RRT-confirmed as recommended-only):**
    * `shippingRate` OMITTED — "Shipping is quoted at order time and depends on order size, weight, destination." No honest flat value exists; a fake $0 would falsely signal free shipping. RRT flags it as a recommended-but-missing optional field — expected.
    * `returnShippingFeesAmount` OMITTED — same logic (variable, freight pickup at customer expense). RRT flags as optional-missing — expected.
    * `restockingFee` OMITTED — the policy's 20% restocking fee is conditional (orders >$2,000 / freight / large casegoods; NOT small items), so no flat value is honest. `returnFees:ReturnShippingFees` covers the universal truth.
    * `handlingTime` kept at in-stock 1–3 days (made-to-order 2–8 wk lead times are per-product; no metafield to drive a conditional).
  - **REGRESSION CONFIRMED INTACT (the load-bearing invariant — 3 additive sessions, working emitter still working):** quote-only PDP `boulevard-system-3` rendered LIVE shows `price:"0"` + `priceSpecification "Price available on request"` **byte-identical** to pre-edit, with the two new blocks + `itemCondition` correctly added above the if-split, and `priceValidUntil` **correctly ABSENT** (CRIT-1b's else-branch guard preserved). `availability` + `seller` unchanged.
  - **DISCIPLINE:** backup → `data/backups/2026-05-29-schema-crit-1c/`. Pre-write drift check (`scripts/preflight-byte-compare.py`, local-unedited vs LIVE pulled from 186373570873): **IDENTICAL** raw sha — confirms CRIT-1b's `d44debe` was the last write, zero drift. PUT to LIVE role=main; 30s CDN wait; post-PUT byte-compare: **IDENTICAL**. updated_at → `2026-05-28T16:33:17-04:00`, size 7,483 → 8,488 bytes.
  - **THEME CHECK:** edit added **0** offenses — file held at **24/24** (0 errors) and repo total held at **2833/165** (canonical theme-root scan, pre-edit and post-edit both = 2833/165 exactly; verified by swapping the backup in and re-running). The new JSON literals contain no Liquid, so no new VariableName/UndefinedObject/MissingTemplate checks.
  - **RRT VERIFIED (Leo manual, all 3 PDP types — buyable-branded `l-shape-desk-3-sizes-13-colours`, quote-only `boulevard-system-3`, vendor=BBI `l-shaped-desk-with-double-pedestals-72w-x-78d`):** 7 valid items, 0 errors each. `hasMerchantReturnPolicy` fully populated (all 7 fields, `merchantReturnLink` resolving) + `shippingDetails` fully populated — both recognized and rendered in RRT's structured-data expansion. The Phase 1 worked-example structure rendered exactly as designed.
  - **HONEST WARN OUTCOME (the H-1 "WARN persists but field strings show why" lesson applied — see operational lessons):** the Merchant listings WARN **moved from "missing structural blocks" (the real gap CRIT-1c was scoped to close) to "missing recommended monetary fields"** (`returnShippingFeesAmount` + `shippingRate` — both deliberate omissions above). Successful close on the structural dimension. Other residual PDP non-critical WARNs are all pre-existing, tracked, NOT CRIT-1c regressions:
    * **Product snippets** = missing `review` + `aggregateRating` — **F-8** (no review data in store, unfixable without real customer reviews).
    * **Local businesses** = `#localbusiness` missing `image` (**F-LOCALBUSINESS-IMAGE**, logged in POLISH-1, needs Steve image asset) + `#organization` missing `priceRange` (**M-2** asymmetry — deliberately not asserted on the org node for a quote-based catalog) + `image` (F-LOCALBUSINESS-IMAGE again).
  - **NET:** CRIT-1c fully resolved on its scoped dimensions. Remaining PDP non-critical warnings are either deliberate monetary omissions (honest by design) or pre-existing findings already tracked. **F-LOCALBUSINESS-IMAGE is now the most likely cause of any residual non-critical PDP WARN — flagged for the next Steve cycle (business image asset).**

---

## 🔀 Day 14 — 2026-05-28 — GIT-HISTORY RECONCILIATION (stack merge #21–#37 → main)

- **STACK-MERGE-RECONCILIATION ✅ COMPLETE — git-only, NO theme writes.** Reconciled the entire open-PR backlog into `main`. **`main` HEAD: `34fd438` → `d744d38`** (clean fast-forward, no force, no merge commit). Preflight `scripts/preflight-write-check.sh`: RESULT: PASS (no watcher, role=main 186373570873 confirmed). All work was already LIVE on the production theme via Admin-API PUTs throughout Day 13–14 — this was history reconciliation, not a deployment.

  - **⚠️ SCOPE REALITY — the merge was broader than the #28–#37 we set out to merge.** The ten PRs were *not* a clean isolated stack. Ancestry analysis showed a **single linear chain of 70 commits** on top of `main` (`34fd438`), in which #28–#37 sit on top of **#21–#27** (nav-redesign-1, lead-high-2, seo-audit-1, launch-chain, morning-image-swaps, steve-priority-changes, post-steve-cleanup — all also open + already live) **plus ~36 un-PR'd direct Day-11 commits** (homepage/image/launch-polish work). #28 is not landable without its ancestors, so the fast-forward necessarily swept the **whole chain (#21–#37 + the loose commits)** onto `main`. Net effect: **`main` now reflects the full Day 11–14 production state** for the first time since #20 (2026-05-24). The GitHub PR base-branch labels were misleading (#30/#32 *said* `base: main` but were actually stacked) — the git ancestry, not the labels, is authoritative.
    - Pre-merge `main` (`34fd438`) had 2 direct commits since #20's merge (`4047a19`, `34fd438` — Day-11 image-bucket workflow, data files only). The chain was built on top of `34fd438`, so **no divergence** — `merge-base(main, #37) == main HEAD` → fast-forward, **zero conflicts** (the 40 build-state.md edits + 8 schema-audit edits replayed in sequence; nothing resolved, nothing dropped).

  - **⚠️ PR STATUS — 9 merged-badged, 8 CLOSED-as-reconciled (NOT abandoned).** After pushing `main`, GitHub auto-marked the **9** `base: main` PRs as **MERGED** (#21, #22, #23, #25, #26, #27, #28, #30, #32). The **8 stacked PRs** whose base was another feature branch (**#24, #29, #31, #33, #34, #35, #36, #37**) **could not** be merged-badged: their heads were already fully contained in `main`, so GitHub returned *"There are no new commits between base branch 'main' and head branch …"* and refused both retarget-to-main and merge. They were therefore **closed with a reconciliation comment** pointing to **`d744d38` as the canonical landing commit for all 8.** **These 8 are CLOSED, not MERGED, purely as a GitHub stacked-PR artifact — the work shipped and is live. A future audit must NOT read closed-not-merged here as abandoned/reverted work.** Canonical commit reference for all 8: **`d744d38`**.

  - **Branch cleanup ✅ 17/17 deleted (local + remote)** via safe `git branch -d` (refuses if not fully merged — never `-D` blindly). One nuance worth recording: **#31 `feature/schema-crit-new-1-2026-05-27`** local tip (`fbff56c`) was 1 commit ahead of its remote (`994349d`) — both verified in `main` — so `-d` balked on the tracking-ref technicality (not a "missing from main" case); resolved by resyncing local to origin (`994349d`) so the `-d` merge-check passed naturally, then deleted. No force-delete used on any branch.

  - **git ↔ live agreement ✅ verified on 3 schema snippets** (`bbi-product-jsonld`, `bbi-service-jsonld`, `bbi-itemlist-jsonld`): pulled LIVE from `186373570873` and byte-compared against `main` via `scripts/preflight-byte-compare.py` → all **RESULT: IDENTICAL** (raw sha256 match). git and live agree post-merge. **No PUTs, no asset changes — this entry itself is the only write, a direct doc commit to `main`.**

## 🖼️ Day 13 morning — 2026-05-27

- **MORNING-IMAGE-SWAPS-2026-05-27 ✅** — 4 hero images replaced on LIVE in a single chained session with per-image mapping halt + per-image real-device check. 9 references swapped across 8 templates. Exact-match approval discipline, pre-write backups, byte-match verification, theme-check baseline held (2852/166), Lighthouse desktop spot-check on 5 surfaces (all Perf 85-89, all LCP < 2.5s). LAUNCH-1 work fully preserved throughout. Detail entry below.

## 🎨 Day 13 midday — 2026-05-27

- **STEVE-PRIORITY-CHANGES-2026-05-27 ✅** — Three Steve-requested visual changes + a speed-optimization pass shipped on LIVE in a single sequential chain with exact-match approval halts between phases, pre-write backups, byte-match verification, and a single theme-check baseline (2852/166) held across 7 production write rounds. Detail entry below.

## 🧹 Day 13 afternoon — 2026-05-27

- **POST-STEVE-CLEANUP-2026-05-27 ✅** — Repo state-correction + post-launch backlog finalization. LOCAL `templates/index.json` synced to v5 seating tile (morning's commit `cfe918f` captured LOCAL state BEFORE the 10:13 IMG-1 re-fix, leaving v4/v5 divergence between LOCAL and LIVE). No production write needed — LIVE self-corrected via a third Theme-Editor stale-cache event at 13:15:38 during Steve/Leo Admin session between 12:38 and 13:15. Forensic byte-comparison confirmed the drift was a single surgical v4→v5 substitution (`LIVE NOW == LIVE pre-drift + v4→v5 substitution`, sha256 `37d77715b37b367a`). 3-tier post-launch backlog finalized. Detail entry below.

## 🛑 Day 13 evening — 2026-05-27

- **SCHEMA-CRIT-1 Fix 1 + WATCHER-DISCOVERY-2026-05-27 ⚠️** — SCHEMA-CRIT-1 session started clean (branch off audit `63c9596`, pre-session checks all passed: LIVE updated_at `13:15:38-04:00`, theme-check baseline `2852/166`, canonical source `theme/snippets/bbi-product-jsonld.liquid` confirmed). Local `Edit` applied Fix 1 (BreadcrumbList position-2 URL: pre-assigned `bc2_u` before render call, matching surrounding `bc3_u` pattern). Pre-PUT `updated_at` re-check detected drift to `14:24:14-04:00` — LIVE asset `bbi-product-jsonld.liquid` had bumped to byte-identical state as LOCAL (sha256 `4fe3c703…`) before any PUT was authorized. Root cause: long-running `shopify theme dev` watcher (PID 28041, started 2026-05-11) bound to `--theme=186373570873` (LIVE main) auto-PUT every local Edit under `theme/**` for 16 days. Approval phrase `fire schema-crit-1 fix-1` was issued but Claude's manual PUT never executed — the watcher had already promoted the change. Session halted, watcher killed (confirmed no other shopify processes), full LIVE theme snapshotted to `data/forensics/2026-05-27-watcher-discovery/` (359 assets, 6.2MB; 311 md5-matched LIVE server checksum, 48 JSON files showing known re-escape wire-format variance). **Fix 1 shipped under anomalous discovery conditions — outcome bytes match the intended fix and 3-PDP verification confirms correctness, but the change was not delivered under the approval gate.** Theme check post-fix `2850/166` — file count unchanged, 2 `UnusedAssign` warnings on the edited file incidentally cleared (theme-check shifts when filter chains are pulled into named assigns); zero new offences. Fix 2/3/4 explicitly deferred — process recovery comes first. Detail entry below.

---

## 🌙 Day 13 late-night — 2026-05-27

- **QUICK-WINS-STACK Day 13 late-night session log.** Branch `feature/quick-wins-stack-2026-05-27` off `feature/watcher-forensics-2026-05-27` (PR #29 base). Preflight watcher check: RESULT: PASS. First post-WATCHER-FORENSICS write session — preflight discipline validated end-to-end.
  - **QW-1 — OECM-TRUST-ALT-TEXT ✅ shipped.** Single-line alt-text fix on `theme/sections/ds-lp-oecm.liquid:515` — `trust_image_2` alt changed from "Brantford General waiting area OECM install" (image was swapped to Artcobell classroom post-IMG-3, alt didn't follow) to "Classroom with active-learning chairs and modular tables" (provenance-neutral, content-accurate). PUT to LIVE role=main 186373570873; updated_at 12:30:51 → 16:14:24; size 58907 → 58920 (+13 bytes); post-CDN sha match. Theme check 2850/166 holds. **Surfaced broader caption-vs-image-content provenance issue** for all 3 trust cells — captured as OECM-TRUST-CAPTIONS-1 Tier 1 backlog item, NOT fixed in this session (scope discipline).
  - **QW-2 — HOTFIX-LANG-ATTR-1 ✅ shipped.** `theme/layout/theme.liquid:2` — `lang="{{ request.locale.iso_code }}"` upgraded to inline conditional `lang="{% if request.locale.iso_code == 'en' %}en-CA{% else %}{{ request.locale.iso_code }}{% endif %}"` because `shop.primary_locale` is still `en`. Storefront now renders `<html lang="en-CA">` on homepage + OECM page (verified via curl post-CDN). Comment in the file points to LOCALE-CONFIG-EN-CA Tier 2B backlog item — config-layer fix at shop level is the cleaner solution and is owed; the conditional is a flag that the workaround is in place. `password.liquid` has identical bug but `/password` route is not active for BBI — bundled into LOCALE-CONFIG-EN-CA scope, not fixed tonight.
  - **QW-3 — HOTFIX-MOBILE-FRIENDLY-VERIFY-1 ✅ verification complete, no theme write.** Cross-checked Okara's "Mobile Friendly: No" claim. Initial Claude verdict was "Okara false positive" — based on a desktop Lighthouse run (DataForSEO Lighthouse defaulted to `formFactor: "desktop"`, Claude did not check the field; treated desktop SEO score 1.00 as a mobile pass). Leo ran PageSpeed Insights mobile preset directly: Performance 58 / FCP 4.4s / LCP 13.3s / SI 6.4s on the homepage under emulated Moto G Power + Slow 4G. **Revised verdict: Okara was directionally correct.** The specific binary "Mobile Friendly: Yes/No" verdict likely wraps the retired Dec 2023 Mobile-Friendly Test endpoint and is low-confidence framing, but the underlying signal (the site is slow on mobile) is real and serious. Real signal rolls into HOTFIX-MOBILE-LCP-1 (single-run mobile measurement under Moto G Power + Slow 4G emulation; baseline pending multi-run averaging per PERFORMANCE-MEASUREMENT-DISCIPLINE); 8 diagnostic signals captured there, fix-phase split into three sub-items HOTFIX-MOBILE-LCP-1a/b/c. No new sub-item created for verify-1 itself (it was a session task, not a backlog item). Methodology lesson captured below.
  - **QW-4 — HOTFIX-HOMEPAGE-META-1 ✅ shipped.** Path A (theme write to `theme/layout/theme.liquid` lines 22 + 37) — brief's original mechanism plan (Admin API metafield update) didn't match current code: title + description are hardcoded strings in the index-template branch, not metafield-driven. Surfaced as 4th Class B catch (committed mechanism assumption vs current code state). New title (56 chars): `Brant Business Interiors · OECM Furniture · Peterborough` — brand-led with Local SEO (Peterborough) + OECM moat. New meta description (148 chars): `OECM Supplier Partner (Agreement 2025-470). Commercial office furniture for Ontario schools, hospitals, and municipalities. Quote in 1 business day.` — leads with verifiable Agreement number, institutional triad verticals, 1-business-day CTA. PUT to LIVE role=main 186373570873; size 10386 → 10308 (−78 bytes); post-PUT API sha match; cache-busted storefront verify confirmed both new title + new meta-description. Theme check 2850/166 holds. Side-effect checks: `/pages/oecm` title intact (index-template-only branch correctly scoped); `content-language=en-CA` header still effective from QW-2.

- **HOTFIX-RENDER-BLOCKING-1 ✅ DIAGNOSED — NOT A VIABLE FIX TARGET (Day 14, 2026-05-28, this entry). No theme write. Branch deleted, no PR.** Opened `feature/render-blocking-1-2026-05-28` off PR #32 tip (`edff249`) as a diagnostic probe of the bimodal-LCP hypothesis. Preflight watcher check: RESULT: PASS. Phase 1 diagnosis (PSI 5-run trace inspection, no writes) **overturned the hypothesis before any fix — exactly the cheap-learning outcome the probe was designed for (~15 min to rule out render-blocking vs. discovering it 90 min into a JS session).**

  **🔴 REFRAME — the "bimodal 12s LCP" is largely a Lighthouse Lantern SIMULATION artifact, not a real bimodal paint.** Trace-observed LCP (real render timing) was **0.4–2.3s in EVERY run, including the "12s" ones** (run1 obsLCP 2313ms, run5 2284ms, run3 832ms, run2 426ms, run4 1876ms). The hero `<img>` paints fast and consistently every load; the hero image downloads in **<600ms every run** (37–100ms transfer). The headline "12.0s / 11.6s" tracks **TTI/interactive** (~12.06s / 11.69s), which the Lantern model folds into a *simulated* LCP. **This corrects the record:** last night's "5.0s / 62% reduction" and this morning's standalone "11.9s" were both readings of a simulation amplifying main-thread variance — NOT real changes in hero paint. Real users are not seeing a 12s hero.

  **Srcset fix (HOTFIX-MOBILE-LCP-1a-HERO-SRCSET) is CONFIRMED working and not in question** — observed paint fast, image bytes deterministic, hero downloads <600ms every run. That win is real and stands.

  **Render-blocking inventory (homepage):** exactly ONE render-blocking resource — `bbi-homepage.css` (35 KB raw / ~6 KB gz, the theme's main stylesheet, loaded unconditionally on all templates), est savings 164–350ms. It is legitimately critical above-the-fold CSS; deferring (media=print/onload) risks FOUC. No render-blocking scripts. Third-party JS (GTM 159ms mainthread, GA, shop.app) all already **0ms blocking** (async). The lone inline `<script>` (no-js class flip, head) is tiny/inline, not network-blocking.

  **Status:** DIAGNOSED — not a viable fix target. Critical-CSS inline extraction is the only real render-blocking win available but is a separate higher-risk task (**CRITICAL-CSS-INLINE**, new Tier 2B) with marginal payoff on a simulated metric. No production write warranted. Backlog entry closed below; `CRITICAL-CSS-INLINE` added to Tier 2B.

  **Redirect:** the genuine remaining mobile-perf lever is **HOTFIX-MOBILE-LCP-1b (JS)** — TBT swinging 134ms→3267ms across runs, ~1.3s script eval+parse (899ms eval + 415ms parse), 333 KB unused JS. The real-user harm is **interactivity (TBT/INP), not hero paint.** See reframed 1b backlog entry.

  **Measurement-honesty note (applies to ALL our LCP figures):** PSI shows "Discover what your real users are experiencing — No Data" → the site has **no CrUX field data** (insufficient traffic). Every LCP number we've reasoned about is a **lab estimate**. Reliability ranking: trace-observed LCP (~2s, lab-but-real-render) > Lantern headline LCP (simulated, least reliable). Real-user LCP is currently **unmeasurable**. **Implication:** do not over-invest chasing the simulated lab LCP toward 2.5s — it's the least trustworthy signal we have. Track real progress via **TBT** (the JS problem is real and measurable); revisit LCP when CrUX field data appears.

- **HOTFIX-MOBILE-LCP-1a-LCP-ELEMENT 🚫 NO-OP SESSION (scope-validation halt at Phase 1).** Branch `feature/lcp-1a-hero-2026-05-27` opened off `feature/schema-crit-new-1-2026-05-27` (PR #31 tip, 994349d) for the scoped LCP-element-only sub-piece of HOTFIX-MOBILE-LCP-1a — intent was to add `fetchpriority="high"` + explicit `width`/`height` to the homepage hero `<img>` (highest-leverage single fix within 1a). Preflight watcher check: RESULT: PASS. **Phase 1 grep + cache-busted curl on LIVE confirmed every attribute this session was scoped to add is already shipped.** Homepage hero img (`theme/templates/index.json` → `bbi-hero` section → `custom_liquid`) renders with `fetchpriority="high" loading="eager" decoding="async" width="2308" height="1362"` — landed earlier today in commits `28a0078` ("HP-HERO-OFFICE-IMG: real <img> in hero media slot (office.jpg, eager + LCP-safe)") + `cfe918f` (morning image swap). LIVE byte verify: single `fetchpriority` occurrence in the rendered HTML, on this exact img. **No writes executed, branch deleted, no PR opened.** Theme check unchanged at 2850/166 (no edits made). PSI multi-run verification also blocked tonight: `pagespeedonline.googleapis.com` returned `RESOURCE_EXHAUSTED — quota_limit_value: "0"` on the baseline run; daily quota resets midnight Pacific. Operational outcome: Phase 1's read-before-write discipline caught the duplicate-work scope hit before any theme touches; the structured session-prompt halt-gates (Phase 1 surface findings → HALT for Leo approval before Phase 2) absorbed the scope-invalidation cleanly. **Secondary finding (deferred, not fixed):** the actual remaining LCP byte savings on this hero `<img>` come from a missing responsive `srcset`/`sizes` — Shopify CDN serves 471 KB at `?width=1920` (current LIVE src) vs 108 KB at `?width=768` vs 32 KB at `?width=390`, so ~440 KB of the 679 KB image-delivery savings PSI flagged are sitting on this one LCP element. That fix is in-scope for HOTFIX-MOBILE-LCP-1a's "audit responsive srcset coverage on hero + LCP-candidate images" line and remains Day 14 work. Sub-scope note added to backlog entry. Detail entry below.

- **HOTFIX-MOBILE-LCP-1a-HERO-SRCSET ✅ SHIPPED (Day 13 final-night session, this entry).** Branch `feature/lcp-1a-hero-srcset-2026-05-27` opened off `feature/schema-crit-new-1-2026-05-27` (tip `fbff56c`, the LCP-ELEMENT no-op build-state update) for the (a) sub-piece of HOTFIX-MOBILE-LCP-1a — the secondary-finding from the LCP-ELEMENT no-op session. **Scope shipped:** add `srcset` (400w / 800w / 1200w / 1600w — dropped 1920w as dead weight at all viewports) + `sizes="(max-width: 767px) 100vw, (min-width: 1320px) 603px, 46vw"` (Option A precise 3-tier, matches actual layout math) + drop `src` fallback from `width=1920` to `width=1200` (worst→middle fallback for srcset-non-supporters) + future-pointer comment `<!-- Hero: raw HTML pending HERO-SECTION-REFACTOR (Tier 2B). Edit with JSON-escape discipline. -->` to the homepage hero `<img>` in `theme/templates/index.json` `bbi-hero` `custom_liquid` block. PUT to LIVE role=main 186373570873; updated_at 13:15:38 → 19:05:51; size 26,021 → 26,763 bytes (+742); post-PUT API sha match (`ab52da09…`). Theme check 2850/166 holds. Cache-busted mobile + desktop UA curl both confirmed rendered HTML on LIVE.

  **Bytes-served delta on the LCP element (CDN HEAD-verified):**

  | Viewport / DPR | Variant browser picks | Bytes | Saved vs 460 KB baseline |
  |---|---|---|---|
  | 390px / DPR 2.625 (PSI Moto G Power emulation) | 1200w | 244 KB | **216 KB / 47%** |
  | 390px / DPR 2 (typical mid-range Android — real-user majority) | 800w | 113 KB | **347 KB / 75%** |
  | 1920px / DPR 1 (standard desktop) | 800w (sizes→603px fixed) | 113 KB | 347 KB / 75% |
  | 1920px / DPR 2 (Retina/HiDPI desktop) | 1600w | 404 KB | 56 KB / 12% |
  | 768px / DPR 2 (tablet) | 800w | 113 KB | 347 KB / 75% |

  **Honesty framing:** PSI multi-run measurement DEFERRED to Day 14 morning (public API quota exhausted: `pagespeedonline.googleapis.com` returns `RESOURCE_EXHAUSTED quota_limit_value: "0"`; resets midnight Pacific). PSI emulation reports the **conservative case** (216 KB saved on LCP element) because PSI's Moto G Power DPR 2.625 forces browser to pick the 1200w variant. **Real-world delta will be larger than what PSI reports** — typical real-user mobile (mid-range Android at DPR 2) sees the browser pick the 800w variant (113 KB), for a ~347 KB saving (75% reduction on the LCP image). PSI is the success-criterion measurement, not the typical-user case.

  **Day 14 morning task:** 3-run PSI mobile preset on `https://www.brantbusinessinteriors.com/`, capture median LCP, compute delta from 13.3s baseline. Success criterion: median LCP < 2.5s. If not met, surfaces remaining 1a sub-work (sitewide width/height audit, AVIF/WebP catalog conversion, fetchpriority on non-homepage LCP candidates) as still-required to clear the LCP gate.

  **PSI single-run verification — 2026-05-27 22:01 EDT (web UI, post-fix):**

  | Metric | Baseline (PSI 16:35) | Post-fix (PSI 22:01) | Delta |
  |---|---|---|---|
  | Performance score | 58 | 79 | +21 points |
  | FCP | 4.4s | 1.7s | -2.7s (Poor → Good) |
  | **LCP** | **13.3s** | **5.0s** | **-8.3s (62% reduction)** |
  | Speed Index | 6.4s | 3.4s | -3.0s (Poor → Good) |
  | TBT | 170ms | 130ms | -40ms |
  | CLS | 0 | 0 | unchanged |
  | Accessibility | 95 | 95 | unchanged |
  | Best Practices | 96 | 96 | unchanged |
  | SEO | 100 | 100 | unchanged |

  Same emulation context: Moto G Power, Slow 4G throttling, headless Chromium, single page session. Measurement ran via PSI **web UI** (different quota pool than the API, which was `RESOURCE_EXHAUSTED` end-of-previous-session and reset midnight Pacific — Leo's manual web-UI run unblocked single-run verification ahead of Day 14 morning).

  **Single-run caveat:** PERFORMANCE-MEASUREMENT-DISCIPLINE Tier 2B notes single-run on already-fast pages has ±400ms LCP variance. The 8.3s delta is large enough that variance doesn't change the directional conclusion (fix obviously worked) but does affect the precision of the exact 5.0s figure. 3-run median measurement still owed for Day 14 morning.

  **PSI 5-run median verification — 2026-05-28 08:10–08:20 EDT (authenticated API, Day 14 morning) — CANONICAL:**

  Measurement source upgraded: anonymous PSI API quota was exhausted at value 0 (shared Google default project, does NOT reliably reset midnight Pacific — the "reset" assumption was wrong). Created a dedicated GCP PSI API key (PageSpeed Insights API, restricted; stored in `.env` as `PSI_API_KEY`, gitignored + untracked). All 5 runs authenticated, mobile strategy, 60s apart. One run 500'd (server-side Lighthouse error) and was re-run.

  | Metric | run1 | run2 | run3 | run4 | run5 | **Median** | Range (min–max) |
  |---|---|---|---|---|---|---|---|
  | Performance | 60 | 83 | 81 | 52 | 59 | **60** | 52–83 |
  | **LCP** | 12.0s | 4.4s | 4.2s | 4.2s | 11.6s | **4.4s** | **4.2–12.0s (7.8s spread)** |
  | FCP | 3.7s | 1.7s | 1.7s | 1.8s | 3.6s | **1.8s** | 1.7–3.7s |
  | Speed Index | 5.6s | 2.7s | 2.4s | 5.2s | 5.8s | **5.2s** | 2.4–5.8s |
  | TBT | 216ms | 134ms | 244ms | 3267ms | 241ms | **241ms** | 134–3267ms |
  | CLS | 0.000 | 0.001 | 0.003 | 0.000 | 0.000 | **0.000** | 0.000–0.003 |

  **🔴 KEY FINDING — LCP is BIMODAL, not normally-distributed-noisy.** Sorted LCP: [4.2, 4.2, 4.4, 11.6, 12.0]. The page lands in one of two discrete states under *identical* emulation (Moto G Power / Slow 4G): a **fast state ~4.3s** and a **slow state ~12s** — nothing in between. This is not ±400ms Gaussian jitter; it is a conditional bottleneck that either fires or doesn't on a given load. Corroborating signal: TBT carries a single 3267ms outlier (run4) against a 134–244ms baseline — main-thread blocking spikes intermittently. CLS is rock-stable (~0), so layout is not the variable.

  **What the bimodality rules in / out:**
  - **Rules OUT image weight as the variance driver.** The HERO-SRCSET fix made image bytes deterministic across runs; a fixed-byte image cannot produce a 7.8s LCP swing. The fix did its job (FCP is consistently sub-2s in the fast state).
  - **Rules IN critical-path / JS instability.** Bimodal LCP + intermittent TBT spike points at a render-blocking resource or third-party/JS execution that sometimes lands in the critical path and sometimes doesn't (CDN cold edge, GTM/analytics sync load, or a render-blocking stylesheet/script racing the LCP paint).
  - **Sequencing implication:** the next-highest-leverage target is **HOTFIX-RENDER-BLOCKING-1 and/or HOTFIX-MOBILE-LCP-1b (JS)**, NOT the remaining 1a image sub-work (width/height audit, AVIF). More image optimization cannot fix a path that is already image-deterministic but JS/critical-path-unstable. **⤷ UPDATE 2026-05-28:** RENDER-BLOCKING-1 was diagnosed and RULED OUT (only one render-blocking resource, critical CSS, not deferrable; bimodal LCP is a Lantern simulation artifact — hero paints ~2s every run). Sole remaining lever is **HOTFIX-MOBILE-LCP-1b (JS)** — real-user harm is interactivity (TBT), not paint. See the HOTFIX-RENDER-BLOCKING-1 DIAGNOSED entry near the top of this file.

  **The median itself is sample-composition-dependent — treat with caution.** With 3/5 runs landing fast, the median sits at 4.4s (fast cluster). A 2-fast/3-slow sample would put the median at ~11.6s. So even 5 runs is insufficient for a *stable* central tendency on a bimodal distribution — the honest summary is "fast state ~4.3s, slow state ~12s, ~60% fast in this sample," not a single trustworthy number. Last night's 5.0s was a favorable single run (fast-state); this morning's standalone 11.9s was an unfavorable single run (slow-state); neither is "the truth" and neither should be cited as canonical.

  **Success criterion analysis (against 5-run median):**
  - Target: median LCP < 2.5s on homepage
  - Actual median: **4.4s** (and unstable — fast state ~4.3s never reaches 2.5s either)
  - Status: **NOT MET.** Even the best-case fast state (~4.2s) is above the 2.5s Good threshold. Two distinct gaps remain: (1) close the ~4.3s fast-state floor toward 2.5s; (2) eliminate the slow-state spikes to ~12s. The variance fix and the floor fix are likely the *same* work — stabilizing the critical path. Remaining HOTFIX-MOBILE-LCP-1 work required:
    - ~~**HOTFIX-RENDER-BLOCKING-1** — now the leading candidate per the bimodality finding.~~ **DIAGNOSED & RULED OUT 2026-05-28** — not the bimodal trigger; only one render-blocking resource (critical CSS, not deferrable); bimodal LCP is a Lantern simulation artifact. No fix shipped.
    - **HOTFIX-MOBILE-LCP-1b — SOLE remaining lever.** JS optimization (333 KiB unused JS + 19 KiB legacy + forced-reflow profiling). The 3267ms TBT outlier is the 1b signal. Real-user harm is interactivity (TBT/INP), not hero paint.
    - HOTFIX-MOBILE-LCP-1a remaining (image width/height audit, AVIF, non-homepage fetchpriority) — **deprioritized** for LCP variance; still valid hygiene/byte work but won't move the unstable LCP.

  **Bytes-served projection vs PSI delta:**
  - Projected savings on LCP element at PSI DPR 2.625: 216 KB (460→244)
  - "Improve image delivery" PSI diagnostic before fix: 679 KiB est savings
  - "Improve image delivery" PSI diagnostic after fix: 384 KiB est savings
  - Delta in PSI estimate: 295 KiB cleared
  - The 295 KiB cleared by PSI matches the bytes-saved projection within reasonable measurement variance, confirming the fix is working as designed at the byte level. LCP delta (8.3s) exceeded byte-savings projection because reducing the LCP element also unblocked other resources in the network waterfall.

  **Updated diagnostic signals for remaining HOTFIX-MOBILE-LCP-1 work (from post-fix PSI):**
  1. Improve image delivery — 384 KiB est savings (was 679; -295 captured by hero srcset)
  2. Render-blocking requests — 310ms est savings (was 150; increase to investigate in HOTFIX-RENDER-BLOCKING-1)
  3. Forced reflow — still flagged (no change; HOTFIX-MOBILE-LCP-1b territory)
  4. Network dependency tree — still flagged (>4 preconnect connections; HOTFIX-MOBILE-LCP-1c)
  5. Use efficient cache lifetimes — 4 KiB est savings (small)
  6. Legacy JavaScript — 19 KiB est savings (HOTFIX-MOBILE-LCP-1b)
  7. Reduce unused JavaScript — 333 KiB est savings (HOTFIX-MOBILE-LCP-1b)
  8. Image elements missing explicit width/height — still flagged sitewide (HOTFIX-MOBILE-LCP-1a sub-piece a)
  9. Avoid enormous network payloads — total 3,012 KiB (was 2,999; ~unchanged)

  Day 14 morning task ✅ DONE (2026-05-28): ran 5-run PSI (upgraded from 3 given the variance) via authenticated API. Result: bimodal LCP (fast ~4.3s / slow ~12s), median 4.4s, criterion NOT MET. Sequencing conclusion: RENDER-BLOCKING-1 / 1b-JS lead the next-target queue over remaining 1a image work, because the variance is critical-path/JS-driven, not image-byte-driven. Awaiting Leo's direction pick.

  **Operational discipline notes from this session:**

  - **Path A drift handling (~3 min cost).** Pre-write LIVE sha check halted on byte mismatch: local `16eb9aac…` (25,574 bytes) vs LIVE `37d77715…` (25,952 chars / 26,021 bytes). Substantive-diff normalization (treating `\/` ↔ `/` as semantically identical) showed **0 substantive differences** — the entire 378-byte drift was Shopify Admin's JSON serializer re-escaping URL forward-slashes at the 13:15:38 Theme-Editor save (same event surfaced in WATCHER-FORENSICS Item 2 Event 3). Chose Path A (pull LIVE → re-edit on `\/`-escaped clean base → PUT) to preserve the byte-match-post-PUT invariant. Strict halt was correct given the load-bearing nature of the byte-match check, but this is exactly the false-positive scenario PREFLIGHT-V2-BYTE-PRIMARY (Tier 2B) was designed to eliminate — concrete justification logged in that backlog item, scope tightened to cover (i) JSON `\/` re-escape, (ii) object key re-ordering, (iii) trailing-newline diffs.

  - **6th Class B catch — build-state forecast forecast vs CDN HEAD measurement.** Build-state line 285 forecast `~440 KB on the LCP element` based on DPR 1 / 390w → 32 KB delta. Pre-write CDN HEAD measurement at PSI Moto G Power DPR 2.625 (which forces 1200w variant pick, not 400w) showed actual delta is `~216 KB`. Class B input failure caught pre-write — forecasted savings vs actual delta — same shape as QW-1 (memory-derived name vs API-derived role) and QW-3 (assumed form-factor vs config-asserted form-factor). Fix pattern: freshness verification at the input boundary (CDN HEAD measurement before claiming bytes saved). Forecast was wrong by ~2x but was a forecast — not a shipped commitment — so no remediation owed beyond logging in matrix and being honest in the commit message + this entry. **Class B catch count this day: 6** (QW-1 memory, QW-3 form-factor, PERF-AUDIT-1 reference, QW-4 mechanism, SCHEMA-CRIT-NEW-1 audit, LCP-1a forecast).

  - **Byte-vs-character measurement discrepancy (operational lesson, not Class B).** During Path A drift analysis, Python's `len(raw)` reported 25,952 (character count) while `wc -c` reported 26,021 (byte count) on the same content. Difference: the JSON string contains UTF-8 multi-byte characters — `—` (3 bytes), `·` (2 bytes), `→` (3 bytes) — which `len()` counts as 1 character each but `wc -c` counts as their UTF-8 byte width. **Not a Class B incident** (no wrong decision was made; sha matched separately to confirm byte-identical pull). Operational reminder: byte counts from different tools require careful interpretation when files contain non-ASCII characters. Tools that count bytes: `wc -c`, `stat -f %z`, `ls -la` size field, `Content-Length` HTTP header. Tools that count characters: Python `len(str)` on a `str` object, JavaScript `string.length`, etc. When checking file-on-disk vs content-length-on-wire, force byte-counting on both sides (e.g., `len(content.encode('utf-8'))` in Python).

  PR #32 opened against `main` with explicit scope-limited title and description referencing predecessor PRs #28-31 + the LCP-ELEMENT no-op finding from earlier session (commit `fbff56c`) for context.

- **QUICK-WINS-STACK — QW-1 stale-memory incident (operational lessons, in-flight session).** During the QW-1 verification table for the OECM-TRUST-ALT-TEXT fix, Claude labelled the PUT target as "dev theme 186373570873" — citing the auto-memory `feedback_push_target.md` as the rule source. The PUT itself targeted the correct resource (production write was intended), but the label was wrong: theme `186373570873` has `role=main` since LAUNCH-2 (2026-05-26 evening) and is the LIVE production storefront — the "Dev" suffix in its name is a pre-LAUNCH-2 artifact. The stale memory had not been updated when the role swap happened, and Claude reasoned forward from the stale name-based framing rather than verifying `role` via the Admin API. Caught by Leo at the QW-1 → QW-2 handoff, before any further PUTs landed under the same mislabel.

  **Remediation shipped same session:**
  - Memory `feedback_push_target.md` rewritten to require role-verification language and to explicitly call out the historical-name failure mode (pending Leo wording sign-off — Action 1).
  - New Tier 1 backlog item PREFLIGHT-ROLE-VERIFICATION added — automate `GET /themes.json` + role assertion as a pre-PUT gate (Action 2, shipped above).

- **Meta-observation — stale-context as a distinct unauthorized-write mechanism class.** WATCHER-FORENSICS surfaced one class of silent unauthorized-write mechanism (background CLI processes auto-PUT-ing local `Edit`s). The QW-1 incident surfaced a second class (stale auto-memory creating false labels Claude reasons from, propagating into verification tables and potentially into commit messages, PR descriptions, and follow-on session prompts). Both reduce to:

  > **"Discipline that depends on Claude's interpretation of context can be silently undermined by stale context."**

  **Triage matrix — Process × Context:**

  |  | **Process gate enforced** | **Process gate missing or bypassed** |
  |---|---|---|
  | **Context fresh** | Working as intended | **Class A — process failure** (2026-05-27 watcher case) |
  | **Context stale** | **Class B — input failure** (2026-05-27: QW-1 + QW-3 + PERF-AUDIT-1 + QW-4 + SCHEMA-CRIT-NEW-1 audit + LCP-1a forecast cases — 6 catches this day) | **Class C — compound failure** (most dangerous) |

  **Apply at incident triage:** ask both axes, not just "did the gate fire." Process-only review would have cleared QW-1 (gate fired, approval issued, PUT correct) and missed that the verification label propagated a stale claim that would have shipped into the commit + PR.

  **Fix patterns by class:**
  - **Class A** — kill the side channel + add preflight detection (WATCHER-FORENSICS pattern).
  - **Class B** — add freshness verification at the input boundary (PREFLIGHT-ROLE-VERIFICATION pattern: API-derived assertion, not memory-derived name).
  - **Class C** — both fixes, plus a session-start sanity check that surfaces any context older than N days for ack. **Class C is the only quadrant where the system produces no signal that anything is wrong; every other quadrant has at least one axis still functioning.** This makes Class C detection an explicit design goal of future preflight work, not an afterthought.

  Future incident reports can extend this matrix with more worked-example rows over time — each new incident gets tagged into the cell that produced it, building an empirical record of which failure modes actually fire in this project vs which remain hypothetical.

- **Methodology lesson — verify form-factor of the measurement tool.** Claude failed to verify the form-factor of the tool used (DataForSEO Lighthouse returned `formFactor: "desktop"` in `configSettings`; Claude did not check the field and treated the desktop result as a mobile cross-check). The error produced a confidently-stated "Okara false positive" verdict that was 180° wrong on a Tier 1 acquisition-impact issue. Caught by Leo running PageSpeed Insights mobile preset directly.

  **Rule:** when verifying any mobile-specific claim, the measurement must come from a tool running in mobile form factor. Reading `configSettings.formFactor` (or equivalent) in the tool's output is a hard pre-condition — if the field reads `"desktop"`, the run does not count as a mobile cross-check regardless of how good the scores look.

  **Valid mobile measurement sources:**
  - PageSpeed Insights mobile preset (web UI: https://pagespeed.web.dev/, set form factor to "Mobile")
  - PageSpeed Insights public API (no auth needed for limited rate):
    ```
    curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&strategy=mobile"
    curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&strategy=desktop"
    ```
    Both variants included so future Claude doesn't make the inverse error (passing `strategy=desktop` while verifying a mobile claim, or vice versa).
  - Local Lighthouse CLI: `lighthouse <url> --preset=mobile`
  - WebPageTest mobile device profiles

  **Known-bad sources for mobile verification:**
  - DataForSEO Lighthouse via MCP (`mcp__dataforseo-mcp__on_page_lighthouse`) — defaults to `formFactor: "desktop"` with no exposed form-factor toggle in the tool parameters. Useful for desktop measurements and SEO/a11y signals that don't change with viewport. **Not valid as a mobile cross-check.**

  **Connection to the Process × Context 2x2 above:** this is a Class B input failure (process gate present — Leo was running a cross-check against a third-party claim; input was stale/wrong — the measurement form-factor didn't match the claim's form-factor). Fix pattern: freshness verification at the input boundary, exactly the same shape as PREFLIGHT-ROLE-VERIFICATION. The matrix cell above has been updated to reflect both QW-1 and QW-3 in the Class B tag.

  **Session catch-rate note:** four Class B catches in this session alone — (1) QW-1 stale-memory framing (Leo caught at the QW-1→QW-2 handoff), (2) QW-3 form-factor methodology error (Leo caught after PageSpeed mobile run), (3) PERF-AUDIT-1 reference verification (Claude verified pre-write via grep before introducing as committed history — see "Notes worth flagging" exchange before WRITE A), (4) QW-4 mechanism assumption (Claude diagnosed that the brief's Admin-API-metafield plan didn't match current code — title + meta-description are hardcoded in `theme/layout/theme.liquid` index-template branch — and surfaced the mechanism delta before executing on the stale plan). The catch-rate suggests verify-input-freshness discipline is reaching habituation, at least for high-stakes asserted facts. Worth tracking whether subsequent sessions maintain the habituation or revert when not under active reinforcement.

- **Methodology lesson — Shopify HTML page_cache invalidation lags asset PUT.** The 30s CDN wait discipline established in QW-1/QW-2 verified asset-layer changes correctly because those edits (section-level + html-tag-level) bypassed Shopify's rendered-HTML page_cache. QW-4 changed `theme/layout/theme.liquid:22` (title) and `:37` (meta description) within the index template branch — content that lives in cached rendered HTML output, not direct asset output. After the 30s CDN wait, the asset API confirmed new bytes on LIVE but uncached storefront curl returned the OLD rendered HTML with the prior title/description. Cache-busted curl (`?nocache=<ts>` + `Cache-Control: no-cache`) returned the new HTML immediately. The page_cache key (visible in ETag: `W/page_cache:...:IndexController:...`) confirmed the layer.

  **Rule:** when verifying changes that touch cached template output (`theme.liquid` index/collection/PDP branches, section settings rendered into cached HTML, anything in a cached controller path), the verify-curl MUST use cache-buster OR wait for natural TTL expiry (5-10 min for index). Asset-layer sha-match alone does NOT confirm storefront rendering.

  **Matrix tagging:** This is not a Class A/B/C failure — the verify-discipline operated correctly at the layer it was designed for. It's a new pattern: verification methodology scope-limitation. Don't formalize a 'Class D' yet; let more examples accumulate before extending the matrix. Tracked via VERIFY-CACHE-BUSTER-DEFAULT Tier 2B.

- **SCHEMA-CRIT-NEW-1 — F-15 (category-card Product schema) RESOLVED ✅ shipped.** Branch `feature/schema-crit-new-1-2026-05-27` off `feature/quick-wins-stack-2026-05-27` (PR #30 tip @ `6aad5d8`). Preflight watcher check: RESULT: PASS. Sitewide schema fix following the F-15 reclassification (PR #28 audit + addendum) caught yesterday by Google's Rich Results Test on the OECM page + ObusForme PDP (8 invalid `Product` snippets per surface).

  - **Emitter located:** [theme/snippets/bbi-org-schema.liquid](theme/snippets/bbi-org-schema.liquid) lines 50-63. Sole emitter — grep across `theme/` confirmed no other source for the 8 category Product nodes. Audit hypothesis confirmed.
  - **Structure clarified:** the 8 items were nested `Offer → itemOffered → Product`, not bare top-level `Product` (audit's summary framed them as bare Products). Google's validator parses each `@type: Product` independently regardless of nesting depth — the inner Product nodes are what RRT flagged.
  - **Rendering scope:** sitewide. `bbi-org-schema` is rendered from `bbi-nav.liquid:12`, which is rendered from 31 distinct surfaces — every PDP, every collection, every sub-collection, all 16 landing-page sections, all 6 brand pages, blog list, article, 404, and the nav-wrap. Every `bbi_landing`-gated page was emitting the 8 invalid Product nodes.
  - **Fix choice — Path C (deletion), not refactor.** Three paths surfaced in Phase 2: Path A (convert inner Products to `Service`), Path B (nested `OfferCatalog` with collection URLs), Path C (delete the `hasOfferCatalog` block entirely). Phase 2 evidence inventory found zero positive signal that the block earned its keep — RRT showed 0 detected items from it (only the 8 errors); the audit's Phase 2 eligibility table credited Sitelinks Search Box + Organization knowledge panel to WebSite+SearchAction and Organization (independent of `hasOfferCatalog`); code provenance was a stated intent ("AI-4: required for Google AI Overview / entity clarity") with no measured outcome; schema.org/Google rich-result docs list no SERP feature triggered by Organization.hasOfferCatalog. Per the "don't refactor what doesn't earn" criterion: Path C is the cleanest fix. Reversible — if future GSC/AI-crawler analysis demonstrates measurable benefit, the block can be reintroduced as Path B (nested OfferCatalog with verified URLs) under its own scoped task.
  - **Edit applied:** removed lines 50-63 (the entire `hasOfferCatalog` block + trailing comma). Pre-edit size 3509 bytes (sha256 `f9f576a2…4564b5`), post-edit 2596 bytes (sha256 `f565a338…48c7e31`) — 913 bytes removed. Local JSON-LD parses cleanly post-edit; `@graph: [[Organization, LocalBusiness], WebSite]` preserved; `parentOrganization`, `sameAs`, `address`, `geo`, `areaServed`, `openingHours`, WebSite+SearchAction all intact.
  - **Pre-PUT discipline (all green):** preflight watcher PASS; fresh `GET /themes.json` confirmed id=186373570873 role=**main** (role-derived, not name-derived per the QW-1 stale-memory lesson — the theme is still named "BBI Landing Dev" but role=main since LAUNCH-2); pre-edit backup written to `data/backups/2026-05-27-schema-crit-new-1/bbi-org-schema.liquid.pre-edit`; pre-edit LIVE-vs-LOCAL sha match PASS (both 3509 bytes, `f9f576a2…`); theme check from `theme/` HOLDS at 2850/166 post-edit.
  - **PUT to LIVE:** approval phrase `fire schema-crit-new-1` issued; single-asset PUT `snippets/bbi-org-schema.liquid` accepted (200), LIVE asset `updated_at` 2026-05-27T18:07:01-04:00; post-PUT Admin API sha re-fetch confirmed LIVE `f565a338…48c7e31` == LOCAL — MATCH.
  - **Verification (cache-busted, per QW-4 page_cache lesson):** 6 surfaces curl'd with `?nocache=<ts>` + `Cache-Control: no-cache` headers — page_cache ETags visible per controller (`PageDetailsController`, `ProductDetailsController`, `CollectionDetailsController`, `IndexController`). Results — `@Product` node count: **0 on non-PDP, 1 on PDP (legitimate main product)** — was 8 per surface previously.
    - `/pages/oecm`: 0 ✓ (was 8)
    - `/products/obusforme-comfort-high-back-chair-fabric-1240-3`: 1 (real product) ✓ (was 9 = 1 real + 8 categories)
    - `/collections/seating`: 0 ✓
    - `/pages/healthcare`: 0 ✓
    - `/pages/brands-keilhauer`: 0 ✓
    - `/` homepage: 0 ✓
  - **Positive-detection preservation:** Organization, LocalBusiness, WebSite, SearchAction all present on all 6 surfaces — none regressed. PDP BreadcrumbList still present, position-2 `item` still resolves to `https://www.brantbusinessinteriors.com/collections/business-furniture` (CRIT-1 Fix 1 preserved, not regressed). PDP Product Offer block intact (Merchant Listing fields C-5 still deferred — out of scope this session).
  - **Brand observation (out-of-scope but worth noting):** ObusForme PDP `brand.name = "Global Furniture Group"` — already the correct manufacturer attribution, not the BBI vendor fallback the audit flagged in F-5. Suggests the F-5 brand-attribution audit finding may not apply as broadly as the audit assumed, at least on enriched SKUs. Supports the SCHEMA-CRIT-1b triage hint from QW-3 that the Hero-100-enriched SKUs may have already accreted correct vendor data. Not investigated further in this session; flag for SCHEMA-CRIT-1b scoping.
  - **RRT confirmation (Leo manual):** both URLs returned **7 valid items, 0 invalid** — yesterday's "8 invalid Product snippets" → 0. PDP: Product ✓, Merchant listings ✓ (non-critical issues only, deferred via SCHEMA-CRIT-1c), Breadcrumbs ✓, Local businesses ✓, Organisation ✓. OECM: FAQ ✓, Local businesses ✓, Organisation ✓.
  - **Theme check:** held at 2850/166 throughout (2048 errors, 802 warnings — identical pre- and post-edit).
  - **F-15 status:** RESOLVED. Audit doc addendum updated with resolution reference.

- **Methodology lesson — manual schema review without RRT is hypothesis-generation only.** The original F-15 misclassification (audit doc Phase 1, line 146) stated "lightweight Product references inside hasOfferCatalog are acceptable per Google guidelines" — a reading of schema.org documentation that Google's actual validator does not honor. RRT parses every `@type: Product` independently and applies Product validation rules regardless of nesting depth. This produced an audit that confidently graded the homepage as eligible for the Organization knowledge panel while 8 invalid Product nodes were silently emitting across 31 surfaces. The audit's own addendum (added during SCHEMA-CRIT-1 Fix 1 RRT verification) captured this lesson: **manual JSON-LD review against documented requirements is hypothesis-generation; eligibility verdicts require real RRT runs per surface class.** SCHEMA-CRIT-NEW-1 vindicated that lesson in practice — yesterday's RRT discovery surfaced F-15's misclassification; today's RRT confirmation post-fix proved the resolution. Future schema audits gated to the existing rule: manual review = hypothesis, RRT = verdict.

---

## 🧹 POST-STEVE-CLEANUP-2026-05-27 ✅ 2026-05-27 afternoon (Day 13)

Repo state-correction + post-launch backlog finalization. No production theme write needed — LIVE self-corrected externally during the prep window. Branch `feature/post-steve-cleanup-2026-05-27` off `feature/steve-priority-changes-2026-05-27 @ 21c0e2a`.

### Task A — HP-SHOP-TILES-REFIX-v5

**Premise at session start (13:13 EDT):**
- LIVE `templates/index.json` bbi-shop seating tile = `bbi-coll-img-seating-hero-v4.jpg` (incorrect — needed v5)
- LOCAL `templates/index.json` bbi-shop seating tile = v4 (matches LIVE; morning's commit `cfe918f` captured pre-re-fix state)
- `/collections/seating` page hero (separate template) = v5 (correct, untouched)

**Forensic drift discovery (mid-session, 13:16 EDT):**
- LIVE `updated_at` baseline at preflight (13:13): `2026-05-27T12:38:47-04:00` (Phase-4-extended write)
- LIVE `updated_at` at pre-write re-check (13:16): `2026-05-27T13:15:38-04:00` — drifted during prep window
- Single asset bumped: `templates/index.json` only (verified via assets-list filter `updated_at > 12:38:50`)
- LIVE NOW size 25952B (escaped JSON form, same byte count as pre-drift)
- Byte-equivalence proof: `LIVE NOW == LIVE pre-drift + v4→v5 character-level substitution` (sha256 `37d77715b37b367a` ≡ `37d77715b37b367a`)
- Interpretation: Steve/Leo were in Shopify Admin between 12:38 and 13:15 (Leo confirmed); a Theme-Editor save flushed a cached v5 state to LIVE — mirror image of this morning's IMG-1 reverse-revert at 09:57:27. Third Theme-Editor stale-cache event today on the same `bbi-shop` `custom_liquid` field.

**Decision:** Skip production PUT, commit LOCAL only. LIVE was already in the desired end state; pushing LOCAL would only rewrite JSON escape form (cosmetic, same `JSON re-escaping artifact pattern from earlier launch sessions` noted in build-state) and bump `updated_at` without semantic gain.

**Commit:** `c9ec186` — 1 file, 1 line, scope: `bbi-coll-img-seating-hero-v4.jpg` → `bbi-coll-img-seating-hero-v5.jpg` in LOCAL `theme/templates/index.json:42` only. Other tiles (desks/storage/boardroom) unchanged. Backup `data/backups/hp-shop-refix-pre-20260527-131533/{index.json.LIVE, index.json.LOCAL}` (both captured the v4 pre-state for any future forensic recovery).

### Theme-Editor stale-cache pattern — full day tally

Three byte-substantive events on `bbi-shop` section's `custom_liquid` field, plus three timestamp-only drifts on other templates:

| Time | Asset | Direction | Effect |
|---|---|---|---|
| 09:57:27 | templates/index.json | IMG-1 reverse-revert (v5→v4) | Required 10:13 re-fix |
| 10:13:21 | templates/index.json | IMG-1 re-fix PUT (v4→v5) + width=1920 opt | LIVE correct; morning commit didn't capture in LOCAL |
| 13:15:38 | templates/index.json | Steve/Leo Admin reverse-reverse-revert (v4→v5) | LIVE corrected; this commit syncs LOCAL |

Plus three morning timestamp-only drifts (08:40:10 collection.seating.json + index.json, 08:52:03 collection.ergonomic-products.json, 09:25:11 four IMG-3 templates).

### LIVE 186373570873 updated_at trail — full day

```
2026-05-26T20:33:23  (post-PRODUCTION-HOTFIX-1 baseline)
2026-05-27T08:37:23  IMG-1 (morning seating + homepage tile)
2026-05-27T08:40:10  Theme-Editor save (timestamp-only)
2026-05-27T08:51:18  IMG-2 (ergonomic)
2026-05-27T08:52:03  Theme-Editor save (timestamp-only)
2026-05-27T09:22:41  IMG-3 (5 education refs)
2026-05-27T09:25:11  Theme-Editor save (timestamp-only)
2026-05-27T09:54:03  IMG-4 (homepage hero)
2026-05-27T09:57:27  IMG-1 reverse-revert (SUBSTANTIVE)
2026-05-27T10:13:21  IMG-1 re-fix + width=1920 opt
2026-05-27T11:03:42  STEVE Phase 1 base CSS
2026-05-27T11:15:37  STEVE Phase 1 extended (33 files single PUT cycle)
2026-05-27T11:23:29  STEVE Phase 2 PDP price
2026-05-27T12:24:15  STEVE Phase 3 collection reorder
2026-05-27T12:30:51  STEVE Phase 4 (20 ds-lp-* fetchpriority)
2026-05-27T12:38:47  STEVE Phase 4 extended (ds-cc-base fetchpriority)
2026-05-27T13:15:38  Steve/Leo Theme-Editor save (SUBSTANTIVE — v4→v5 self-correction)
```

Monotonic, every bump accounted for. No unauthorized writes.

### Safety
- **Theme-check baseline:** held at `2852/166` EXACTLY across all 8 production write rounds today (1 morning width=1920 PUT + 7 STEVE-PRIORITY phase PUTs). Today's afternoon Task A had no theme write — baseline carried from STEVE-PRIORITY close-out; current LIVE state is byte-equivalent to that baseline + v4→v5 substitution.
- **ROLLBACK 178274435385:** `unpublished` throughout, untouched.
- **All commits/PRs today (4):**
  - `cfe918f` MORNING-IMAGE-SWAPS-2026-05-27 (4 image swaps + width=1920 opt)
  - `21c0e2a` STEVE-PRIORITY-CHANGES-2026-05-27 (3 visual changes + speed pass, 35 files)
  - `c9ec186` POST-STEVE-CLEANUP-2026-05-27 Task A (LOCAL state sync, no PUT)
  - this build-state commit

### POST-LAUNCH BACKLOG — 3-tier finalized

#### 🚀 BLOG-LAUNCH ROADMAP — active plan (2026-05-29)

**Goal:** ship the first cornerstone blog post live. Three phases. _(This is the active execution plan; the Tier 1 / Tier 2 / Tier 2B inventory below remains the canonical per-item detail reference.)_

**Phase A — Pre-blog gates (~10–15 hrs · 2–3 focused work days)**

- **Block 1 — Quick wins (~30 min)**
  - OECM-TRUST-ALT-TEXT (~5 min)
  - PERFORMANCE-MEASUREMENT-DISCIPLINE (~10 min)
- **Block 2 — Schema + SEO foundation (~3.5–4.5 hrs)**
  - ~~HOMEPAGE-CONTENT-DENSITY · both lanes~~ ✅ DONE Day 17 (PR #53 · Scope C all 5 opportunities)
  - ~~OG-META-WIRE-UP-SITEWIDE~~ ✅ DONE Day 17 PM (PR #54 · **no-op closure** — audit found og:* coverage already 100% complete sitewide; 0 new tags needed)
- **Block 3 — Mobile LCP reasonable bar (~2–3 hrs)**
  - HOTFIX-MOBILE-LCP-1b (~2–3 hrs · JS optimization)
  - Success criterion: ship the JS work, NOT sub-2.5s lab LCP (no field data exists; lab metric is theoretical)
  - LCP-1c (~30–45 min) deferred to Phase C unless time permits
- **Block 4 — Catalog enrichment (~6-8 hrs across multiple sessions) — ✅ IN PROGRESS (Sessions 1-4 shipped Day 17 evening)**

  **⤷ STATUS UPDATE 2026-05-30 (Day 17 evening):** Block 4 is no longer "NEXT" — it is **IN PROGRESS**. Sessions 1-4 shipped: **32 products enriched** (PRs #60/#61/#63), **183 catalog-wide vendor corrections** (PR #62), **4 reference files** established, and the **manufacturer dictionary grown 3 → 19**. The 13-field `specs.*` framework is locked (was 15; `tagline`/`standfirst` retired). Remaining: ~101 Global products (Sessions 5-8), ~9 MityBilt re-routes, 204 deferred (UNKNOWN SKU prefixes + 48 boilerplate-corrupted). **Full session detail, the 12 operational lessons, reference-files inventory, and manufacturer dictionary live in the Day 17 evening (enrichment) section at the top of this file.**

  **OTHER-COLLECTION-TIER-A-ENRICHMENT** — Enrich 338 currently-invisible products on /collections/other with structured PDP data, bringing them to parity with the live enriched catalog. Enables Shopify storefront filters (material, weight_capacity, certifications, etc.) once metafields are consistent.

  **Workflow (revised Day 17 evening):** Manual paste-and-draft workflow with Claude in conversation, batched in 10s. Replaces the automated YAML pipeline approach prepped Day 13.

  Per product: Leo pastes CSV row + manufacturer source material → Claude drafts title verbatim + body_html lead + 15 `specs.*` metafields + SEO title/description + alt text + recommended tags → Leo reviews/approves → next product.

  Per batch of 10: Leo pushes via Admin API → theme check + storefront spot-verify 1-2 PDPs → update tier_a_enriched=Y in CSV → commit CSV update.

  **Queue source:** data/reports/other-collection-products-20260527-093211-with-recs.csv (ROI-ranked, includes existing_metafields / variant_options / inventory_status / recommended sub-collection per product). Saves "what's next" decision and over-writing already-correct metafields.

  **Starting batch:** brand:global (5 premium products, $549-2099 range) as workflow validation. If first 1-2 products take 30-45 min each, recalibrate; if faster, batches of 10 stay realistic. Tier B (190 products) and Tier C (119 commodity) follow once Tier A workflow proves out.

  **Dropped from prior plan:**
  - YAML intermediate files (data/reports/enrichment/*.yaml) — manual workflow goes straight from input → Admin API push per batch
  - prompt-other-collection-tier-a-ingest.md ingest script — Leo pushes batches directly
  - prompt-other-collection-tier-b-routing.md — already skipped per Day 13 decision (no Steve CSV review)
  - prompt-other-collection-tier-a-enrichment.md interactive Claude Code workflow — superseded by conversational batched approach

  **Filter goal informs priority fields:** `specs.materials`, `specs.weight_capacity`, `specs.certifications`, `product_type` need consistency across products to power filters later.
- **Block 5 — Site verification (~30–60 min)**
  - Theme check baseline + RRT spot-check across page types
  - Cache-busted smoke test: homepage, brand pages, OECM page, 3 PDPs, collection grid
  - Confirm merge state clean

**Phase B — First blog publish (~3–4 hrs)**

- Cornerstone Post 1 editorial pass (already drafted per Day 14 backlog)
- Schema: Article + BreadcrumbList + FAQPage if applicable
- Internal linking pass
- Publish via Admin API
- RRT on published URL + social-share preview check

**Phase C — Parallel / post-blog (ongoing)**

- **Content production (primary mode after Phase B):**
  - Cornerstone Post 2 (gated on SERP analysis 2.2)
  - Cornerstone Post 3 "Cubicle vs Open-Plan for Municipal Offices" (gated on 2.3)
  - PAA mining → FAQ expansion
  - Featured snippet mining
- **Steve-gated (whenever Steve responds):**
  - OECM-TRUST-CAPTIONS-1
  - OUR-WORK-CLIENT-LOGOS (restored item)
  - STEVE-SET-BLOG-FEATURED-IMAGE
  - BRAND-PAGE-HERO-IMAGE-AUDIT
- **Catalog continuation:**
  - OTHER-COLLECTION Session 4 (NONE bucket, 71 products, ~45–60 min)
- **Performance (informed by real field data):**
  - HOTFIX-MOBILE-LCP-1c
  - Additional perf guided by CrUX
  - STORAGE-COLLECTION-COLD-CACHE
- **SEO measurement infrastructure (Tier 2 carry-forward):**
  - DataForSEO competitor recon (2.1)
  - SERP analysis defensible angles (2.2)
  - Keyword research Cornerstone 3 (2.3)
  - Rank tracking baseline (2.4)
  - Featured snippet mining (2.5)
  - PAA mining (2.6)
  - AI Overview tracking (2.7)
- **Architectural hygiene (Tier 2B carry-forward):**
  - ~~BRAND-PAGE-COPY-FIX~~ ✅ resolved 2026-05-29 (PR #45)
  - MANUFACTURER-LOGO-ACQUISITION (~1 hr + 10 min)
  - ~~AUTHOR-URL-FIELD~~ ✅ resolved 2026-05-29 (PR #47)
  - CRITICAL-CSS-INLINE (~60–120 min)
  - FETCH-FILE-STALE-ID (~10 min)
  - PREFLIGHT-AUTOMATION residual (~30–45 min)
  - HERO-SECTION-REFACTOR (~45–90 min)
  - LOCALE-CONFIG-EN-CA (~15–20 min)
  - BBI-SEO-METAFIELD-MIGRATION (~30–45 min)
  - VERIFY-CACHE-BUSTER-DEFAULT (~15 min)
  - FORENSIC-SNAPSHOT-TIME-WINDOWED (~30 min)
  - DEV-THEME-PROVISIONING (~25 min)
  - HP-SHOP-TILES-REFACTOR (~30–60 min)
  - STARLITE-LEGACY-SNIPPETS-AUDIT (~30–60 min · restored item)


**Tier 1 — Pending (Week 1, high priority):**
- _(~90–120 min · 1b JS/TBT is the live lever · highest acquisition impact)_ **HOTFIX-MOBILE-LCP-1 🆕🔥** (Tier 1, **highest-acquisition-impact open item**, added 2026-05-27 late-night from QW-3 verification) — Mobile performance is genuinely failing on LIVE. Core Web Vitals → ranking is a more direct signal than rich-result eligibility, and the gap is enormous (LCP 13.3s vs Good threshold 2.5s = 5.3x over). **⚠️ REFRAME 2026-05-28 (RENDER-BLOCKING-1 diagnosis):** the headline LCP figures (13.3s baseline, "5.0s", "11.9s") are **Lantern simulation estimates**, not real paint — trace-observed LCP is 0.4–2.3s and the hero downloads <600ms every run. The real, measurable problem is **interactivity (TBT 134→3267ms)**, owned by sub-item 1b. No CrUX field data exists (site below traffic threshold), so lab LCP is the least trustworthy signal — track TBT, revisit LCP when field data appears. 1a-HERO-SRCSET shipped (confirmed working); RENDER-BLOCKING-1 diagnosed & ruled out; **1b is the sole remaining lever.**

  **Measurement (authoritative baseline):**
  - Source: PageSpeed Insights mobile preset
  - Date: 2026-05-27 ~16:35 EDT
  - Page: homepage (`/`)
  - Emulation: Moto G Power, Slow 4G throttling, headless Chromium
  - Run count: single (variance acknowledged — multi-run averaging recommended per PERFORMANCE-MEASUREMENT-DISCIPLINE Tier 2B before declaring the fix successful)

  **Numbers:**
  | Metric | Value | Threshold (Good) | Status |
  |---|---|---|---|
  | Performance score | 58 | ≥ 90 | 🟡 yellow zone |
  | FCP | 4.4s | < 1.8s | ❌ 2.4x over |
  | LCP | 13.3s | < 2.5s | ❌ 5.3x over — "Poor" zone |
  | Speed Index | 6.4s | < 3.4s | ❌ |
  | TBT | 170ms | < 200ms | ✅ |
  | CLS | 0 | < 0.1 | ✅ perfect |
  | Accessibility | 95 | — | ✅ |
  | Best Practices | 96 | — | ✅ |
  | SEO | 100 | — | ✅ |

  **Historical context:** Okara had earlier reported homepage LCP at 4.6s. PageSpeed mobile preset now reports 13.3s. Possible explanations: (a) degradation since launch from new content/assets, (b) harsher throttling profile in PageSpeed mobile vs whatever Okara measured under, (c) Okara measurement methodology differs. The PageSpeed figure is the trusted source going forward; do not reuse the 4.6s figure as a baseline.

  **Diagnostic phase: COMPLETE.** The following 8 diagnostic signals were surfaced by PageSpeed and are the inputs for the fix phase:
  1. **Render-blocking requests** — Est savings 150ms · tracked separately as HOTFIX-RENDER-BLOCKING-1 (Tier 1, distinct row; fix-surface is CSS/JS ordering)
  2. **Legacy JavaScript** — Est savings 19 KiB (modernize transpile targets / drop polyfills)
  3. **Improve image delivery** — Est savings **679 KiB** (significant; AVIF/WebP, proper srcset, responsive sizing)
  4. **Forced reflow** — JS triggering layout thrash; profile in Performance tab
  5. **Network dependency tree warnings** — >4 preconnect connections (audit `<link rel="preconnect">` list, drop unused)
  6. **Reduce unused JavaScript** — Est savings **334 KiB** (code-splitting / defer / remove dead bundles)
  7. **Image elements missing explicit width and height** — CLS risk + layout-shift cost
  8. **Avoid enormous network payloads** — Total page weight 2,999 KiB

  **Remaining scope: fix-phase only, split into three discrete sub-items.** Diagnostic work that would have been the first ~30 min of this item is already complete (PageSpeed surfaced everything). Each sub-item below is independently shippable on Day 14+ based on time/energy:

  - **HOTFIX-MOBILE-LCP-1a — Image delivery (~90-120 min)** — addresses diagnostic signals #3 (Improve image delivery, 679 KiB est savings) and #7 (Image elements missing explicit width/height). Fix surfaces: convert remaining JPG/PNG assets to AVIF/WebP via Shopify `image_url` filter with `format` param; ensure every `<img>` has explicit `width`/`height` (or `image_tag` filter use); audit responsive `srcset` coverage on hero + LCP-candidate images; add explicit `fetchpriority="high"` on the homepage LCP candidate. **Recommended FIRST.** Largest single-bundle savings (679 KiB) and most likely to directly improve LCP since the LCP element on a Shopify storefront homepage is almost always a hero image. **Scope update 2026-05-27 late-night (HOTFIX-MOBILE-LCP-1a-LCP-ELEMENT no-op session):** the homepage hero `<img>` already has `fetchpriority="high"` + explicit `width="2308"`/`height="1362"` + `loading="eager"` + `decoding="async"` (shipped in commits `28a0078` + `cfe918f`). **Scope update 2026-05-27 final-night (HOTFIX-MOBILE-LCP-1a-HERO-SRCSET shipped, this session):** sub-piece (a) shipped — homepage hero img now carries `srcset` (400w/800w/1200w/1600w) + `sizes="(max-width: 767px) 100vw, (min-width: 1320px) 603px, 46vw"` (Option A precise 3-tier) + `src` fallback dropped 1920w → 1200w + future-pointer comment for HERO-SECTION-REFACTOR. PSI emulated Moto G Power DPR 2.625 picks 1200w variant → 460 KB → 244 KB = 216 KB saved (47% reduction); typical mid-range Android DPR 2 picks 800w → 460 KB → 113 KB = 347 KB saved (75% reduction). Remaining 1a sub-scope for Day 14+: (b) sitewide audit of `<img>` tags missing explicit `width`/`height` (homepage hero done — check PDP gallery, collection cards, industry-page heroes, OECM trust cells); (c) AVIF/WebP format conversion via Shopify `image_url` `format:` param across catalog; (d) `fetchpriority="high"` on LCP candidates of other heavy templates (PDP main product image, collection grid first row, industry pages — none currently set, only homepage). Order suggestion: (b) for sitewide hygiene, then (c) for byte savings everywhere, then (d) for non-homepage LCP coverage.

  - **HOTFIX-MOBILE-LCP-1b — JS optimization ✅ COMPLETED 2026-05-30 (Day 17 evening, PR #55).** Shipped as **theme-level JS hygiene** (AOS/parallax no-op cleanup in `theme.liquid` + `SEOAnt-SpeedUp.liquid` orphan deletion). **Honest framing:** the TBT baseline was *already in Google's "good" band* before this session — Leo's 3-run PSI mobile (Moto G Power + Slow 4G): homepage TBT **~95ms** (80/110), PDP TBT median **190ms** (170/190/390). Theme cleanup doesn't move that number (the AOS block was a guaranteed global no-op — `aos.js`/`parallax.js` load on zero pages, so `typeof AOS` was always false), but it removes dead code paths and an orphaned script-injection snippet. **Key audit finding:** the Day-14 reframe ("333 KiB unused JS is the 1b lever") was directionally right about the *bytes* but mislocated the *owner* — the 287–334 KiB unused JS is the **Avis Product Options app** (300 KB gzip / 1.24 MB raw across 14 files, loaded sitewide incl. homepage where no configurable products exist), which is **app-embed-injected via `content_for_header`, NOT theme-editable**. The genuine theme-editable JS surface is only ~37 KB inline (already well-placed). So the real perf lever was split out as new Tier 2B **AVIS-APP-SCOPE-OPTIMIZATION** (below). Original full-scope intent (transpile/polyfill drop, forced-reflow profiling, per-template code-split) was found to not apply — the theme has no transpiled bundle on its live pages; legacy asset JS (theme.js 270KB/jquery/flickity/etc.) is referenced in **0 liquid files** = dead, not served. Baseline captured in `measurement-protocols.md`. **Measurement note:** keyless PSI mobile API is quota-blocked and DataForSEO Lighthouse runs desktop-only (TBT≈0) — true mobile TBT requires Leo's manual PSI run or a PSI API key.

  - **HOTFIX-MOBILE-LCP-1c — Network / preconnect cleanup (~30-45 min) — ⏳ STILL PENDING.** Addresses diagnostic signals #5 (preconnect warnings, >4 connections) and #8 (Enormous network payloads, 2999 KiB total). Fix surfaces: audit every `<link rel="preconnect">` in `theme/layout/theme.liquid` for actual usage; remove unused preconnects (each idle connection costs browser resources); investigate single biggest payload contributors via DevTools Network tab; consider lazy-loading of below-fold third-party scripts (GA, GTM, Shop Pay). **Recommended THIRD or as cleanup.** Investigative work (audit-then-decide); easier to scope correctly once 1a and 1b have shifted the baseline. **⤷ Dependency note (2026-05-30, Day 17 evening):** 1b shipped as theme hygiene only and did NOT shift the baseline (homepage TBT ~95ms / PDP 190ms already "good"; the real byte lever is AVIS-APP-SCOPE-OPTIMIZATION, not theme JS). The Day-17 audit confirmed PSI still flags >4 preconnects and ~3 MB homepage / ~8 MB PDP payloads — but with TBT already in the good band and LCP dominated by image delivery (1a srcset shipped), 1c may turn out **smaller than the original 30-45 min estimate**. Re-audit when scheduled; scope it *after* AVIS-APP-SCOPE-OPTIMIZATION, which will materially change the network payload picture on non-PDP pages. *Recommendations are recommendations — future-Leo can override based on time/energy or new signals.*

  - **AVIS-APP-SCOPE-OPTIMIZATION 🆕 (Tier 2B, added 2026-05-30 Day 17 evening from HOTFIX-MOBILE-LCP-1b audit, ~30-60 min) — THE ACTUAL LEVER the 1b "333 KiB unused JS" estimate pointed at.** The Avis Product Options app loads **287–334 KiB unused JS sitewide** (300 KB gzip / 1.24 MB raw across 14 `apo-*` script files — biggest single is `apo-product-options-v3.min.js` at 110 KB gzip / 404 KB raw), including the homepage, collections, and all landing pages **where there are no configurable products and none of it is used**. PSI flags it directly: "Reduce unused JavaScript — 334 KiB" (homepage) / "287 KiB" (PDP). **Fix:** scope the Avis app embed to product/cart pages only (vs all pages) to reclaim the bytes on every non-PDP route. **Where the lever lives:** this is **primarily app-settings work in the Shopify admin** (Avis Product Options → settings, and/or the Theme Editor → App embeds toggle) — Avis injects via `{{ content_for_header }}`, so the theme cannot conditionally gate it; a small theme conditional may help only if Avis exposes an app-block (not embed) mechanism. **Expected impact:** meaningful reduction in transferred bytes on non-PDP pages (big mobile-data win for B2B buyers on metered/slow connections), possibly modest TBT/LCP improvement. **⚠️ Behavioral risk:** must NOT break the configurable-product add-to-cart / options flow on PDPs — verify ATC + options render on a configurable product after any scoping change. Confirm via PSI mobile re-run (homepage unused-JS should drop ~300 KB) + functional ATC smoke. Requires Avis app-settings access; surface to Leo/Steve for the admin step.

  **Success criteria:** mobile LCP < 2.5s on homepage under same PSI mobile preset emulation. Multi-run averaging (3 runs, median) per PERFORMANCE-MEASUREMENT-DISCIPLINE before declaring done. Each sub-item should re-run PSI mobile and report its delta contribution.

  **Related work:**
  - HOTFIX-RENDER-BLOCKING-1 (Tier 1, distinct row) — diagnostic signal #1 above; mechanical fix-surface is CSS/JS ordering, separate from image/payload work in this item.
  - PERFORMANCE-MEASUREMENT-DISCIPLINE (Tier 2B) — multi-run averaging discipline.
  - STORAGE-COLLECTION-COLD-CACHE (Tier 2) — separately tracked perf anomaly on `/collections/storage`.
  - PERF-AUDIT-1 Phase 2 (committed item at [bbi-build-state.md:1606](BBI-Session-Kickoff/bbi-build-state.md:1606)) — same root concern; HOTFIX-MOBILE-LCP-1 + sub-items are the actionable Tier 1 instances of PERF-AUDIT-1 Phase 2's "re-run PSI against the new theme post-LAUNCH-2" deliverable.

- _(~30–60 min · Steve-gated · photos/policy)_ **OECM-TRUST-CAPTIONS-1 🆕** (Tier 1, ~30-60 min once policy decided, **BLOCKED on content-policy decision OR Steve install assets**) — All 3 trust cells in `theme/sections/ds-lp-oecm.liquid` (lines ~501-536: `trust_image_1` Education / `trust_image_2` Healthcare / `trust_image_3` Government) have potentially stale `alt` + visible `<figcaption>` text after IMG-3 image swaps. Visible `<figcaption>` elements display incorrect provenance — confirmed example: caption reads "Brantford General · waiting" under what is now an Artcobell classroom photo (per build-state OECM-TRUST-ALT-TEXT note). Same risk pattern applies to cells 1 and 3.

  **Two-part fix:**
  (a) Audit all 3 cells — for each, pull the currently-uploaded image from LIVE settings, compare to the hardcoded alt + visible figcaption (`<span class="lp-trust-row__caption-key">`, the bold install line, and the spec line), document which cells are stale.
  (b) Decide policy — **option 1**: neutral content-accurate descriptions for both alt + caption (drops "OECM PO · 2024" specificity, weakens the trust signal but is honest); **option 2**: wait for Steve to provide real OECM install photos + verified caption data, restore the original install-specific framing (preferred long-term — these are credibility-critical cells).

  **Scope discipline:** Do NOT attempt fix in QUICK-WINS-STACK session — captured 2026-05-27 late-night when QW-1 surfaced that the alt-only fix for cell #2 leaves the visible caption misrepresenting. ~5 min alt-only correction (cell #2) is being shipped in QW-1 as a narrow a11y/SEO fix; the broader caption/provenance issue is this item.

- _(~10-30 min · depends on path · partially Steve-gated)_ **OECM-TRUST-IMAGE-SLOT-ASSIGNMENT 🆕** (Tier 2B, logged 2026-05-30) — Root-cause issue underlying the OECM trust-row alt/caption mismatches. Cell 1 ("Education · Halton DSB" caption) renders a healthcare reception photo (`OCI-Healthcare-Carousel-3.jpg`); Cell 2 ("Brantford General · waiting" caption) renders an education classroom photo. Images appear to have been shuffled between slots at some point. PR #52 fixed Cell 1's alt to describe the rendered photo (provenance-neutral); underlying slot assignment remains misaligned. **Fix options:** (a) restore correct images to correct slots; (b) rewrite captions to match rendered photos (overlap with OECM-TRUST-CAPTIONS-1); (c) replace all 3 cells with real install photos from Steve (Steve-gated path of OECM-TRUST-CAPTIONS-1). ~10-30 min depending on path. **Scope-distinct from OECM-TRUST-CAPTIONS-1** because that item addresses captions; this addresses the underlying photo assignment.

- ✅ **OECM-TRUST-ALT-TEXT — RESOLVED 2026-05-30 · PR #52.** Corrected the residual stale alt on **`trust_image_1`** (the Education cell), `theme/sections/ds-lp-oecm.liquid:492` — alt was "Halton DSB admin offices OECM install" but the assigned image is `OCI-Healthcare-Carousel-3.jpg`, a healthcare reception corridor (the slot-1/2 image shuffle that Day 13 QW-1 fixed on the mirror cell). New alt: "Healthcare reception corridor with a row of stacking guest chairs and lettered wayfinding signage" (provenance-neutral, content-accurate, Day 13 convention). PUT to LIVE role=main 186373570873; asset SHA match (`be317cb1…`); cache-busted curl on `/pages/oecm` confirmed new alt renders + stale alt 0 occurrences; theme check 2833/165 holds. **Inventory-drift note:** this entry's text described `trust_image_2` (the cell Day 13 QW-1 already fixed) — the pending item was the residual on cell 1, diagnosed via markup→schema→asset→photo trace. Caption-vs-image provenance remains open under **OECM-TRUST-CAPTIONS-1** (Tier 1, scope-separate).

- **HP-SHOP-TILES-REFACTOR → moved to Tier 2B 2026-05-27 evening.** See revised entry in Tier 2 section below. (WATCHER-FORENSICS Item 2 re-attributed 2 of the 3 recurrences to the watcher; refactor urgency drops, architectural justification survives.)

- _(resolved 2026-05-30 · PR #53 · branch `feature/homepage-content-density-2026-05-30`)_ **HOMEPAGE-CONTENT-DENSITY ✅ RESOLVED 2026-05-30** (Day 17 PHASE-A-BLOCK-2-SESSION-1 — see Day 17 afternoon entry at top of file). **Audit-first finding overturned the original "reads thin" premise:** homepage content is already dense (952 visible words, 25 headings, clean H1→H2→H3, strong defensible-angle coverage — OECM ×20, Ontario ×15, Agreement 2025-470 ×5, founded-1964 ×6). The real gap was **page-specific schema** (the homepage emitted only sitewide chrome — `#organization`/`#website`/`#localbusiness` — and zero page-level schema, unlike every other template). Shipped Scope C (all 5 opportunities, 3 commits): **(1) schema** — new `bbi-homepage-schema.liquid` with WebPage + ItemList(4 collections) + 3×Service(shared snippet) + FAQPage; **(2a) keywords** — "authorized dealer" + "broader public sector (BPS)" woven into bbi-about (brief said PSAB but PSAB = accounting body, ~0 furniture search volume per DataForSEO → used BPS, Leo-approved); **(2b) FAQ** — new `bbi-homepage-faq.liquid` visible 5-Q&A accordion (ordering / NET 30 / OECM / delivery / space planning). Verified via Admin-API asset readback (authoritative — bypasses page cache). Theme check held 2833/165. _Original diagnosis retained for reference:_ Homepage reads thin above the value-proposition fold relative to the B2B institutional buyer's need for trust + breadth signals. Two lanes: (a) copy/section density; (b) proof density. The homepage is the primary internal-link target from the first blog post, so density work compounds with Phase B. Restored to the tracked inventory 2026-05-29 (had dropped off the list). ~2–3 hrs across both lanes.
- _(~5 min · added 2026-05-30 from HOMEPAGE-CONTENT-DENSITY Commit 2b · likely Steve-gated)_ **FAQ-DELIVERY-FOOTPRINT-RECONCILE 🆕** (Tier 2B) — `/pages/faq` (`ds-lp-faq.liquid`) says BBI "delivers across Ontario," while the homepage `bbi-about` section AND the new homepage FAQ say "delivery across Canada, installation in Ontario + Western Canada." The two pages disagree on the delivery footprint. Leo chose "across Canada" for the homepage FAQ Q&A #4 in-session (matched the already-live homepage about copy) and flagged this for reconciliation. **Steve to confirm the true delivery footprint, then align both pages to one canonical statement.** Small.
- _(~30–45 min · added 2026-05-30 from OG-META-WIRE-UP-SITEWIDE audit)_ **OG-IMG-DEFAULT-LANDSCAPE 🆕** (Tier 2B) — The sitewide og:image fallback for landing/brand/static pages + image-less collections is the store Social-sharing-image preference (`IMG_2566.jpg`), which is **portrait 1039×1184** — the wrong aspect ratio for `summary_large_image` social cards (want ~1.91:1 / 1200×630), so it letterboxes/crops on LinkedIn/FB. Homepage `og-preview.png` is square 1024×1024 (renders OK, not ideal). **Fix:** create one explicit 1200×630 landscape OG default and either swap the store social-share preference asset or make the fallback explicit in `meta-tags.liquid`. Needs a 1200×630 asset (generate via fal.ai page-image pipeline, or crop an existing brand photo). Low effort once asset exists.
- _(~Steve-gated · added 2026-05-30 from OG-META-WIRE-UP-SITEWIDE audit)_ **OG-IMG-PER-SEGMENT 🆕** (Tier 2B, **Steve/asset-gated**) — Landing + brand pages currently all share the single generic OG default. Topically-relevant per-segment OG images (healthcare / education / government / non-profit / professional-services / per-brand) would lift social-share CTR. **Asset-gated** — needs per-segment 1200×630 images (Steve assets or AI image pipeline) before any Liquid wiring. Builds on OG-IMG-DEFAULT-LANDSCAPE.
- _(~10 min · added 2026-05-30 from OG-META-WIRE-UP-SITEWIDE audit · low priority)_ **OG-TWITTER-IMAGE-EXPLICIT 🆕** (Tier 2B, low priority) — No explicit `twitter:image` tag is emitted anywhere; X currently falls back to og:image so cards still render — but an explicit `twitter:image` mirroring og:image in `meta-tags.liquid` is a small hardening. Optional; bundle with OG-IMG-DEFAULT-LANDSCAPE when that's actioned.
- **OG-META-WIRE-UP-SITEWIDE ✅ RESOLVED 2026-05-30 (PR #54 · NO-OP CLOSURE)** (Tier 1, was ~1.5 hrs · restored 2026-05-29 · gates blog social shares) — **The audit overturned the premise.** Open Graph + Twitter-card meta turned out to be **already 100% wired sitewide** — every page type (homepage, PDP, collection, brand, OECM, industries hub, healthcare, blog index, blog article, About) emits a complete, reachable set of `og:title` / `og:description` / `og:image` / `og:url` / `og:type` + `twitter:card`/`title`/`description`. A literal wire-up would have written **zero** new tags. **Why coverage is complete:** [`theme/snippets/meta-tags.liquid`](../theme/snippets/meta-tags.liquid) (rendered from `theme.liquid:11`) handles homepage via `og-preview.png` and all other templates via Shopify's `page_image` global — which itself falls back to the **store Social-sharing-image preference** (`IMG_2566.jpg`) for any page without a template image, so landing/brand/static pages all still get an og:image. **No drift:** local `meta-tags.liquid` is byte-identical to LIVE `186373570873`. **No Liquid edit, no production PUT.** Full audit: [`docs/reviews/og-meta-audit-2026-05-30.md`](../docs/reviews/og-meta-audit-2026-05-30.md). What remains is **image quality/relevance**, not presence — logged as 3 new Tier 2B follow-ups below (OG-IMG-DEFAULT-LANDSCAPE / OG-IMG-PER-SEGMENT / OG-TWITTER-IMAGE-EXPLICIT). **Phase A Block 2 fully complete.**
- _(~Steve-gated · restored item 2026-05-29)_ **OUR-WORK-CLIENT-LOGOS 🆕** (Tier 1, **Steve-gated**) — Surface real client/institution logos (school boards, hospitals, municipalities) on the Our Work / homepage trust strip as social proof. **Steve-gated** — needs Steve to confirm which logos BBI has permission to display (institutional clients often restrict logo use). Restored 2026-05-29. Asset acquisition + a logo-strip render once greenlit; tracked in Phase C → Steve-gated until then.

**Tier 1 — Completed:**
- _(resolved 2026-05-29 · Fix1+1b+1c)_ **SCHEMA-CRIT-1 — ✅ FULLY RESOLVED 2026-05-29 (Fix 1 + CRIT-1b + CRIT-1c all shipped & RRT-confirmed)** (branches `feature/schema-crit-1-2026-05-27`, `feature/schema-crit-1b-2026-05-28`, `feature/schema-crit-1c-2026-05-29`). The largest schema item in the backlog, now closed end-to-end: **Fix 1** = BreadcrumbList position-2 URL (PR #28, Day 13); **CRIT-1b** = `itemCondition` + `priceValidUntil` + brand-dropped-by-decision + booster-seo removal (PR #36, Day 14); **CRIT-1c** = `hasMerchantReturnPolicy` + `shippingDetails` (Day 15 — see top-of-file Day 15 entry). RRT on all 3 PDP types: 7 valid items, 0 errors. Residual Merchant-listings non-critical WARN moved from structural-gap to deliberate monetary-omission (`shippingRate` + `returnShippingFeesAmount`, both honest-by-design omissions). Remaining PDP non-critical WARNs are pre-existing/tracked: F-8 (review/aggregateRating, no review data) + F-LOCALBUSINESS-IMAGE (needs Steve image) + M-2 (org priceRange, deliberately not asserted).
  - **Fix 1 ✅ shipped 2026-05-27 evening under anomalous discovery conditions** (not under approval gate; outcome bytes match intended fix; watcher-pushed before manual PUT could fire — see Day 13 evening detail entry). BreadcrumbList position-2 URL: pre-assigned `bc2_u` in `theme/snippets/bbi-product-jsonld.liquid:155` before render call; 3-PDP JSON-LD verification confirms position-2 = `https://www.brantbusinessinteriors.com/collections/business-furniture`; theme check 2850/166 (net improvement, no regression); **Rich Results Test verification CONFIRMED 2026-05-27 ~15:06 — Breadcrumbs 1 valid item detected on `obusforme-comfort-high-back-chair-fabric-1240-3`; eligibility moved blocked → eligible**.
  - **SCHEMA-CRIT-1b ✅ COMPLETE — shipped 2026-05-28** (branch `feature/schema-crit-1b-2026-05-28`, off `feature/preflight-automation-2026-05-28` PR #35 tip). Three sub-changes consolidated into this session (note: supersedes the older 1b/1c/1d sub-labeling — "CRIT-1c" now refers to the Steve-gated returns/shipping work below):
    - **Merchant Listing fields (C-5/F-7) — shipped under approval gate.** `itemCondition: https://schema.org/NewCondition` added **unconditionally** to PDP `offers` (BBI sells new furniture). `priceValidUntil` added **buyable-branch-only** (`{%- else -%}` branch, where `product.price != 0`) — computed leap-day-safe via epoch math (`'now' | date: '%s' | plus: 31536000 | date: '%Y-%m-%d'`), renders `2027-05-28`. The quote-only (`price == 0`) branch correctly receives `itemCondition` but **no** `priceValidUntil` (a price-expiry on a "Price available on request" offer is meaningless). This is the regression guard.
    - **brand.name (C-3/F-5) — DROPPED BY DECISION.** Live-data sizing showed the audit's premise was stale: on enriched (Hero-100) SKUs, `product.vendor` has already been re-attributed to match the manufacturer — 21/25 sampled SKUs had `vendor == specs.manufacturer` (fix = no-op); only ~2/25 would change, and those inject messy strings ("Global Furniture Group (likely)", "...(Global Care)") that are worse than the current clean vendor. The broad misattribution (~410 vendor=BBI products) is **non-enriched** (no manufacturer metafield), so the schema-side fix cannot touch them — that's the data-side vendor re-attribution project (out of scope, large data workstream). Not worth touching a working emitter for ~10 net-negative PDPs. Emitter brand handling unchanged.
    - **booster-seo.liquid (P-1/F-6) — repo-deleted only.** `git rm theme/snippets/booster-seo.liquid` (orphaned — zero `render`/`include`/`section` refs anywhere). **LIVE theme asset removal DEFERRED** (see LIVE-booster-seo-asset-removal backlog item) — it's inert on LIVE (confirmed: PDPs emit exactly 1 Product, zero standalone Organization/WebSite/Blog/Article blocks), so deleting it from LIVE is a destructive irreversible API op with zero upside; not worth it. Repo deletion is the real hygiene win.
    - **Regression confirmed:** quote-aware offers behavior intact on all 3 PDP types (buyable-branded `l-shape-desk-3-sizes-13-colours`, quote-only `boulevard-system-3`, vendor=BBI `l-shaped-desk-with-double-pedestals-72w-x-78d`). Quote-only still renders `price:"0"` + `priceSpecification` "Price available on request", now with `itemCondition`, correctly without `priceValidUntil`. **RRT 3/3: 7 valid items, 0 errors** each. BreadcrumbList (Fix 1) + Org/LocalBusiness chrome intact.
    - **Honest Merchant Listing framing:** `itemCondition` + `priceValidUntil` are **completeness — necessary-but-not-sufficient.** They clear two missing-field warnings but do NOT by themselves trigger a Merchant Listing rich result, which also requires Google Merchant Center / a product feed + the CRIT-1c fields (`hasMerchantReturnPolicy`, `shippingDetails`). The remaining RRT "Merchant listings non-critical" warnings = the known CRIT-1c scope. The "Local businesses non-critical" warning = pre-existing F-4 duplicate-entity (SCHEMA-H-1) — tracked, not a regression.
    - **Preflight:** PASS (`scripts/preflight-write-check.sh` — watcher + role gate). **Drift check:** IDENTICAL pre-write, IDENTICAL post-PUT byte-compare (`scripts/preflight-byte-compare.py`). **Theme check:** edit itself added **0** offenses (24→24 on the file, total held 2850/166); after `git rm booster-seo.liquid` repo total improved to **2833/165** (−17 offenses, −1 file = dead-code removed from repo). Backups in `data/backups/2026-05-28-schema-crit-1b/`.
  - **SCHEMA-CRIT-1c — ✅ COMPLETE 2026-05-29** (branch `feature/schema-crit-1c-2026-05-29`, off `main` @ `d744d38`). `hasMerchantReturnPolicy` (`MerchantReturnPolicy`) + `shippingDetails` (`OfferShippingDetails`) added to PDP `offers`, both unconditional, full URIs, `merchantReturnLink` resolving canonically. Single OfferShippingDetails covering CA with 1–15 day transit (honest middle — not split Ontario-direct vs Canada-wide-freight). `shippingRate` + `returnShippingFeesAmount` + `restockingFee` deliberately omitted (quote-based/conditional — omission > fabrication). Regression confirmed intact on quote-only `boulevard-system-3` (price:"0" + priceSpecification byte-identical, priceValidUntil correctly absent). RRT 3/3 = 7 valid, 0 errors. Theme check 2833/165 held; file 24/24. **Full detail in the top-of-file Day 15 entry.** This was the other half of full Merchant Listing eligibility (with CRIT-1b's two fields) — **CRIT-1 now fully closed.**

- _(resolved 2026-05-29 · commit 2b29f0a)_ **SCHEMA-CRIT-4 ✅ RESOLVED 2026-05-29 (strip; see Day 15 entry at top). Original diagnosis preserved below for record.** — **`ds-cs-base` product-card `Product` microdata invalid on quote-only products.** The `ds-cs-base.liquid` product-card `<article>` (line 497) carries `itemscope itemtype="https://schema.org/Product"` with `itemprop` name/brand; the Offer block (line 529, `itemprop="offers"` + price/priceCurrency) renders **only in the buyable branch.** For quote-only products (price=0 / unavailable → `is_quote_only`) the card emits a **bare Product with no offers** → Google RRT error `"offers/review/aggregateRating should be specified"` + invalid Merchant listing. **Confirmed PRE-EXISTING** (present in pre-session backup `data/backups/2026-05-28-schema-crit-3/ds-cs-base.liquid` line 497; CRIT-3's git diff only added the ItemList render call — untouched card markup). Confirmed on LIVE: medium-back-seating page 1 = all 24 products quote-only → 24 bare Products → 24 invalid (RRT also double-counts them as 24 invalid Merchant listings). **Blast radius: 91 published sub-collections** render via `ds-cs-base`; severity scales with quote-only ratio (high for BBI's quote-heavy B2B catalog). `ds-cc-base` and `ds-collection-base` card markup is **clean (0 microdata — plain HTML anchors)**, which is why their RRT is clean. **Fix-vs-strip decision** (gate `itemscope` on `is_quote_only == false`, OR strip card microdata entirely to match the two clean templates) belongs in its own session with **RRT re-verify across the buyable/quote-only split.** ~30-45 min. **Phase 1 ACTION ITEM:** check whether PDP/product-detail templates have the same bare-Product-on-quote-only pattern — if the card microdata was copied from a product-page partial, the same bug likely exists on product detail pages (**higher priority than collection cards if so**).
  - **🏁 ROOT-PATTERN NOTE — HISTORICALLY RESOLVED 2026-05-29 (all 3 surfaces closed).** A B2B-dealer-specific bug class: Product schema emitted without required offers on quote-only products, born from a **quote-heavy catalog interacting with theme markup that assumed every product has a buyable offer** — false for BBI. It appeared in **three syntaxes**, now resolved in all three:
    1. **F-15 / CRIT-NEW-1 — JSON-LD `hasOfferCatalog` Product stubs** → resolved 2026-05-27 by deletion (Day 13, PR #31 / `d744d38`).
    2. **CRIT-4 — HTML microdata `itemscope` Product cards on `ds-cs-base`** → resolved 2026-05-29 by strip (Day 15, this session).
    3. **PDP — `bbi-product-jsonld.liquid` Product emitter** → was **always quote-aware / correctly defensive from the start** (guards on `price==0` / availability → "Price available on request"; confirmed clean by the CRIT-4 Phase 1 diagnosis, Day 14).
    **Architectural completion:** the canonical pattern is now CollectionPage + ItemList for collection enumeration (no per-card Product), and a quote-aware Product emitter on the PDP. **Predictive value retained:** anywhere the theme emits Product schema (JSON-LD or microdata), verify it handles the quote-only case before declaring it valid. CRIT-3's summary ItemList sidesteps this by design (no Product type at all). No known 4th surface remains.

- _(resolved 2026-05-29 · commit 75651f1)_ **F-LOCALBUSINESS-IMAGE ✅ RESOLVED 2026-05-29** (commit `75651f1` — `image` field added to both chrome LocalBusiness nodes) — _Original finding preserved:_ Both sitewide chrome LocalBusiness nodes — `#organization` (combined `["Organization","LocalBusiness"]` in `bbi-org-schema.liquid`) and `#localbusiness` (dedicated, `bbi-localbusiness-schema.liquid`) — **lack the recommended LocalBusiness `image` field** → Google RRT flags **`Missing field "image" (optional)`** on every page that renders the chrome (i.e. **sitewide**, every `bbi_landing` surface). **Confirmed 2026-05-28** via RRT on `/pages/oecm` + `/pages/quote` (screenshots): the WARN appears on BOTH nodes, including `#localbusiness` which already has `priceRange:"$$"` — definitively **`image`, NOT priceRange.** **This is the "recurring Local businesses non-critical WARN" — and it is NOT:** M-2 (priceRange — ruled out, dedicated node has it), F-8 (review/aggregateRating — separate), or F-4 (duplicate entity — H-1 fixed that). Note `#organization` carries `logo` (an *Organization* property, an ImageObject) but **not** the LocalBusiness `image` field, which Google's RRT counts separately. **Fix:** add an `image` field (absolute URL to a representative business photo — storefront / install / team / product shot, **NOT the logo**) to both chrome emitters; sitewide blast radius means it clears the WARN everywhere at once. **Priority: LOW** — non-critical/optional, **zero rich-result impact** (LocalBusiness is not a Google rich-result type for BBI). **Likely Steve-gated** — needs a real business image asset chosen. ~15-20 min once a URL is picked. Track as own backlog item.

- _(shipped 2026-05-28 · PR #33)_ **SCHEMA-CRIT-2 — COMPLETE ✅ shipped 2026-05-28** (branch `feature/schema-crit-2-2026-05-28`, off `feature/lcp-1a-hero-srcset-2026-05-27` @ `36360e2` — PR #32 tip; PR #33, commit `97b9416`):
  - **Shipped:** `Service` + `FAQPage` JSON-LD on all 6 industry/segment landing pages (healthcare, education, government, non-profit, professional-services, industries hub). Service via new shared snippet `theme/snippets/bbi-service-jsonld.liquid` (parameterized name/description/serviceType/areaServed; `@id`=`{canonical}#service`; `provider` is an `@id` ref to `#organization` — the F-4-correct pattern, mirrors `ds-lp-delivery.liquid`). FAQPage emitted **inline per-section** (7 Qs each, 42 verbatim total) — kept inline rather than shared because each page's Q&A is unique hardcoded HTML; matches the `ds-lp-faq.liquid` precedent. Comment in each section flags FAQPage/visible-FAQ sync.
  - **Emitter architecture:** hybrid — one shared snippet for the Service node (consistent w/ `bbi-org-schema`/`bbi-breadcrumb-jsonld` codebase pattern), per-template inline for FAQPage. Two `<script>` blocks per page (valid; Google merges). 4 JSON-LD blocks render per page total (chrome Org+LocalBusiness + dedicated LocalBusiness + WebSite + new Service + FAQPage).
  - **Honest eligibility — NO rich-result claim:** `FAQPage` earns **entity-graph/AEO value only, NO FAQ SERP rich result** — Google's Aug-2023 policy restricts FAQ rich results to authoritative government/health sites; BBI is a commercial furniture vendor and does not qualify (**including the government page** — it *serves* but is not *operated by* government). `Service` is not a rich-result type at all. The real value is AI-crawler Q&A grounding (ChatGPT / Perplexity / AI Overviews / Gemini) + entity-graph completeness, NOT SERP features. Do not claim rich results anywhere (avoids repeating the F-15 over-claim).
  - **Scope decision:** `OfferCatalog` (originally scoped as M-6) **deliberately NOT added** — lightweight `Product` items inside `hasOfferCatalog` recreate exactly the SCHEMA-CRIT-NEW-1 invalid-Product-snippet problem deleted 2026-05-27 (Google RRT flags every `{"@type":"Product"}` stub). Zero rich-result payoff, so omitted.
  - **Honesty guardrails applied:** no OECM-eligibility claim on private-sector pages (professional-services, non-profit — their FAQs explicitly distinguish eligible vs. non-eligible buyers); `areaServed` capped at Ontario/Canada; Agreement 2025-470 stays in description text, not a fabricated `Certification`/`agreementID` node; FAQ answers are verbatim from visible on-page copy (entities decoded, anchor tags stripped, no truncation — no fabricated Q&A).
  - **RRT verification:** spot-checked 2 of 6 (healthcare = OECM-eligible-content shape; professional-services = private-sector non-eligible shape) — **both 5 valid items, 0 errors**. FAQ validates (1 valid item); Service correctly gets no RRT row (not a rich-result type). Remaining 4 pages render+parse confirmed programmatically + cache-busted storefront verified; RRT not individually run (shared pattern, 2-of-6 spot-check confirms the pattern validates).
  - **No regression:** chrome entity graph (Organization/LocalBusiness/WebSite) intact on all 6 pages — confirmed despite the recent `bbi-org-schema` change in SCHEMA-CRIT-NEW-1; no interaction. (The non-critical LocalBusiness WARN visible in RRT is the **pre-existing F-4 duplicate-entity issue** that H-1 addresses — not introduced by this session.)
  - **Preflight:** PASS (no watcher). **Theme check:** 2850/166 held (inlined `areaServed` default in the snippet to avoid a net-new `VariableName` warning). **Deploy discipline:** target asserted `id=186373570873 role=main`; no drift (6 sections matched HEAD, snippet net-new 404); backups in `data/backups/2026-05-28-schema-crit-2/`; snippet PUT + sha-verified first; 6 sections PUT sequentially w/ per-file sha verify; cache-busted storefront verified.
  - **Deferred — H-1** (see Tier 2B backlog): convert OECM + Quote inline `provider` LocalBusiness redeclarations to `@id` refs. Kept out as an edit-to-live-schema (this session was purely additive).

- _(shipped 2026-05-28 · PR #34)_ **SCHEMA-CRIT-3 — COMPLETE ✅ shipped 2026-05-28** (branch `feature/schema-crit-3-2026-05-28`, off `feature/schema-crit-2-2026-05-28` @ `7f205da` — PR #33 tip; stacked **PR #34**, commit `cee7f57`):
  - **Shipped:** summary `ItemList` wrapped in `CollectionPage` on **all 3 collection section templates** — `ds-cc-base.liquid` (~9 category pages), `ds-cs-base.liquid` (91 sub-collections), `ds-collection-base.liquid` (109 default-suffix collections) = ~209 published collections covered. Emitted via new shared snippet `theme/snippets/bbi-itemlist-jsonld.liquid` (parameterized: `products`, `list_url`, `list_name`, `position_offset`, `item_cap`; `@id`=`{canonical}#collectionpage`; `mainEntity` = the `ItemList`). Render-call placed inside each section's existing `{% paginate %}` block so the list reflects the **current page's actually-displayed products**.
  - **Structure decision:** **summary ItemList** — each item is `{"@type":"ListItem","position":N,"url":...,"name":...}` with **NO inline Product type** → no `offers`/`review`/`aggregateRating` required → sidesteps the F-15 / CRIT-NEW-1 invalid-Product trap entirely. CollectionPage wraps ItemList via `mainEntity` (schema.org-correct page typing). Page-scoped, **capped at 30** items (collections run large: seating 127, business-furniture 250+). `position_offset = paginate.current_offset` gives correct global ranks across pagination — **verified on LIVE: sub-collection page 2 = positions 25–48** with its own `?page=2#collectionpage` @id.
  - **Honest eligibility — NO rich-result claim:** ItemList earns **entity-graph/AEO value only, NO product-carousel SERP feature.** Verified against Google docs: ItemList carousel rich results are restricted to **Course/Movie/Recipe/Restaurant** — products/e-commerce collections are **not a supported type.** This is a **category limitation, not a markup gap.** The session prompt's premise (product-carousel eligibility) was incorrect; Leo chose to proceed knowing the accurate framing. Real value: CollectionPage entity typing + machine-readable product enumeration for Google index understanding + AI-crawler grounding (same value tier as CRIT-2). Do NOT claim a carousel anywhere.
  - **CRIT-3 output verified clean:** cache-busted storefront curls on 3 structural variants (seating = top-level category; medium-back-seating = sub-collection w/ pagination; business-furniture = high-count) — CollectionPage+ItemList parses, **0 parse errors, 0 `@type:Product` nodes from CRIT-3's own schema**, `numberOfItems` matches actual displayed count, chrome (Org/LocalBusiness/WebSite) + BreadcrumbList + (where present) FAQPage all intact = **no regression.**
  - **RRT spot-check:** 3 variants. seating + business-furniture (ds-cc-base) = 6 valid items, 0 Product snippets, clean. medium-back-seating (ds-cs-base) surfaced **24 invalid Product snippets — a PRE-EXISTING, unrelated card-microdata bug, NOT from CRIT-3** (see SCHEMA-CRIT-4 below). CRIT-3's own ItemList JSON-LD is valid on all 3 (RRT shows no ItemList rich-result row — expected, as products aren't a supported carousel type, exactly like Service in CRIT-2).
  - **Honesty guardrails applied:** no inline Product without valid offers ✅; ItemList reflects actually-displayed (page-scoped) products, not all-products ✅; no overclaimed rich-result eligibility ✅.
  - **Preflight:** PASS (no watcher). **Theme check:** 2850/166 held (snippet vars prefixed `il_*` to avoid a net-new `VariableName` warning — same class of fix as CRIT-2's inlined `_area`). **Deploy discipline:** target asserted `id=186373570873 role=main` (fresh); no drift (3 sections matched HEAD, snippet net-new); backups in `data/backups/2026-05-28-schema-crit-3/`; snippet PUT + sha-verified FIRST; 3 sections PUT sequentially w/ per-file sha verify; 30s CDN wait + post-CDN sha re-verify all 4 files.
  - **FAQPage scope:** the audit's H-5 (always-on FAQ w/ fabricated default Q&As) **deliberately NOT done** — violates the no-fabrication guardrail, and FAQPage earns no rich result for BBI anyway (CRIT-2 finding). Category pages already emit FAQPage from real `faq_item` blocks; the other 200 collections have no FAQ content, so none was fabricated. CRIT-3 = ItemList only.

- _(shipped 2026-05-28 · H-1 done, rest dropped/deferred · PR #37)_ **SCHEMA-POLISH-1 + SCHEMA-H-1 ✅ session run 2026-05-28 — H-1 SHIPPED; 1 item dropped-as-no-op, 5 dropped/deferred. Branch `feature/schema-polish-1-2026-05-28` (off `feature/schema-crit-1b-2026-05-28` @ `d44debe`, PR #36 tip).** Deliberately scoped as a *polish* session — deciding what NOT to do was the bulk of the value. The original POLISH-1 bundle was the audit's "Session 4" grab-bag (H-2, H-3, H-4, M-1, M-2, M-3, M-4); after Phase 1 triage only the separately-tracked **H-1** was judged worth a write.

  - **H-1 ✅ DONE (the one write this session).** Converted the inline `provider` LocalBusiness redeclaration in `theme/sections/ds-lp-oecm.liquid` (was ~lines 304-317, GovernmentService node) and `theme/sections/ds-lp-quote.liquid` (was ~lines 363-376, Service node) to a single `@id` reference: `"provider": { "@id": "https://{{ shop.permanent_domain }}/#organization" }` — matching the proven `ds-lp-relocation` / `bbi-service-jsonld` (CRIT-2) pattern. `{{ shop.permanent_domain }}` renders to `office-central-online.myshopify.com`, byte-matching the chrome's `#organization` `@id`. **Result: LocalBusiness node count 3→2 per page** (the standalone inline duplicate is gone; `provider` now resolves to the canonical entity). **F-4 duplicate-entity finding RESOLVED on these two pages.** Clean swap, **no property loss** — the `#organization` node (`["Organization","LocalBusiness"]`) is a strict superset of the inline block. Shipped clean: fresh preflight PASS; pre-write drift IDENTICAL both files; PUTs 200 (oecm 58920→58553, quote 74642→74275, −367B each); post-PUT byte-compare IDENTICAL (after 30s CDN settle — one transient stale re-fetch confirmed read-after-write asset-cache lag, not a failed write); theme check **2833/165 held**; cache-buster storefront RRT confirms 2 LocalBusiness (was 3), `provider` renders the `@id`, sibling schema (GovernmentService/Service, FAQPage, Org+LocalBusiness/WebSite/SearchAction chrome — 3 ld+json blocks/page) all intact, zero regression.

  - **⚠️ EXPLICIT CORRECTION (do not misread the record):** H-1 **did NOT clear** the "Local businesses — Non-critical issues detected" WARN that has appeared on every RRT run, and **was never going to.** The Phase 4 prediction conflated two *distinct* findings: **F-4** (duplicate LocalBusiness entity — H-1 FIXED this, 3→2) vs. the **missing-recommended-field WARN** on the LocalBusiness *type* (H-1 did NOT touch this). They are unrelated. Post-H-1 RRT (oecm + quote, 2026-05-28) confirmed the WARN persists by design — see the new finding F-LOCALBUSINESS-IMAGE below. **"H-1 done" ≠ "WARN cleared."**

  - **POLISH-1 triage — the drop/defer decisions ARE the permanent record (so a future session does not re-litigate or mechanically "finish the list"):**
    - **M-3 — DROPPED (no-op).** `BlogPosting.publisher` in `ds-article.liquid:170` **already** carries `"@id": ".../#organization"`. An object with `@id` + properties is the *same* node, not a duplicate — no F-4 violation. The only "fix" left would be deleting the redundant inline `name`/`logo` = zero-value cosmetic churn on a working emitter. No write.
    - **H-4 — DEFERRED.** PDP `offers.seller` → `@id` ref (`bbi-product-jsonld.liquid:154`, a real 4th-Org duplicate per F-9). Edit to the **every-PDP** offers emitter CRIT-1b just touched; `seller`-as-inline-Org is industry-standard and breaks nothing. Low value × highest-traffic working surface = not worth tail-of-session risk.
    - **M-2 — DROPPED.** `priceRange:"$$"` on the combined Org+LocalBusiness chrome (`bbi-org-schema`, max blast radius). `"$$"` is a dubious claim for a quote-based B2B catalog with no public pricing. **Sub-note for whoever revisits:** the two chrome LocalBusiness emitters are now *inconsistent* — the dedicated `#localbusiness` node (`bbi-localbusiness-schema.liquid:47`) **already asserts** `priceRange:"$$"`, while `#organization` does not. If M-2 is ever picked up, the real decision is whether to assert `priceRange` at all (drop from both) or make them consistent — not "add the missing one."
    - **M-1 — DEFERRED.** `AboutPage`/`ContactPage` typing (additive, F-14 weak signal). Low value.
    - **M-4 — DEFERRED.** OECM `agreementID`/Certification (additive). Explicitly **declined as a same-file rider** on H-1 — different change class (additive field vs dedup swap); if worth doing it earns its own deliberate decision, not a scope-accretion ride-along.
    - **H-2 — PROMOTED to its own session.** `Blog` schema on `/blogs/news` is a **net-new additive emitter** (like CRIT-2), not "polish." Precondition: verify the blog is populated first.
    - **H-3 — PROMOTED to its own session.** `Brand` schema × 6 manufacturer pages = new snippet + 6 template renders — substantive net-new, not polish-sized.

  - **Naming note:** the "POLISH-1" label now mostly means *decided-against*. The two genuinely-worthwhile remainders are net-new emitter work — track them as **SCHEMA-BLOG-1** (was H-2) and **SCHEMA-BRAND-1** (was H-3), each its own additive session. H-4/M-1/M-2/M-4 remain low-priority backlog under their audit IDs; do not resurrect them under a "finish POLISH-1" framing.

- _(closed 2026-05-28 · diagnosed, not a fix target)_ **HOTFIX-RENDER-BLOCKING-1 ✅ CLOSED — DIAGNOSED, not a viable fix target (2026-05-28).** Day 14 diagnostic probe (PSI 5-run trace inspection, no theme write) ruled this out as the bimodal-LCP trigger. **Findings:** the homepage has exactly ONE render-blocking resource — `bbi-homepage.css` (35 KB raw / ~6 KB gz), the theme's main stylesheet, est savings 164–350ms — and it is legitimately critical above-the-fold CSS; deferring it (media=print/onload) risks FOUC. No render-blocking scripts. Third-party JS (GTM/GA/shop.app) already async (0ms blocking). The "bimodal 12s LCP" turned out to be a **Lighthouse Lantern simulation artifact** — trace-observed LCP was 0.4–2.3s in every run; the hero paints fast and consistently, so there is no real render-blocking-induced slow mode to eliminate. **No production write warranted; branch `feature/render-blocking-1-2026-05-28` deleted, no PR** (same pattern as LCP-1a-LCP-ELEMENT no-op). Critical-CSS inline extraction is the only real render-blocking win available — split out as **CRITICAL-CSS-INLINE** (new Tier 2B, low priority). Full diagnosis entry near top of file. Remaining mobile-perf lever is **HOTFIX-MOBILE-LCP-1b (JS)**. ~~_Original entry:_~~ ~~Eliminate render-blocking resources flagged by PageSpeed mobile preset on homepage (Est savings 150ms). Fix-surface: CSS/JS ordering, defer/async, critical-path inlining.~~

  **Scope:**
  - Audit every `<link rel="stylesheet">` and `<script>` in `theme/layout/theme.liquid` for `defer` / `async` / `media` attribute correctness.
  - Identify which stylesheets/scripts are above-the-fold critical vs deferrable; inline critical CSS where appropriate.
  - Confirm Shopify CDN bundles use HTTP/2 multiplexing efficiently (no waterfalling on duplicate connections).

  **Success criteria:** PageSpeed mobile preset re-run shows 0 "Render-blocking resources" diagnostic flagged on homepage; total render-blocking savings claim drops below 50ms.

  **Related work:**
  - HOTFIX-MOBILE-LCP-1 (parent perf item) — render-blocking fix contributes to but does not solely resolve mobile LCP regression.

- _(resolved 2026-05-28 · PR #35)_ **PREFLIGHT-ROLE-VERIFICATION ✅ RESOLVED 2026-05-28 (PREFLIGHT-AUTOMATION session)** — shipped as `scripts/preflight-role-check.sh`. **How to invoke:** `./scripts/preflight-role-check.sh` (or via the unified wrapper `./scripts/preflight-write-check.sh`; re-runnable before each PUT). Does a fresh `GET /admin/api/2026-04/themes.json` (the list, to catch "main moved to a different id" and "multiple mains"), asserts the sole `role=main` theme is `id=186373570873`, FAILs LOUD on mismatch/no-main/multi-main/API-error/bad-shape, soft-WARNs on name or rollback-role drift, and emits a `VERIFIED: id=… role=main name=…` triple for pasting into verification tables (the QW-1 antidote). API version standardized on `2026-04` to match all existing tooling (the backlog's `2024-10` was superseded — both are valid; consistency won). Design Qs resolved: integration = (b) standalone script composed by wrapper; failure = abort on production id/role mismatch, warn on name/rollback drift; scope = `--expect-id` flag (defaults 186373570873) protects any future production theme; verified triple is emitted for table integration. Tested pass-on-good + fail-on-bad via `scripts/test-preflight-checks.sh`. ~~_Original entry:_~~ Automate a pre-PUT role-verification step. Before any asset PUT, fetch `GET /admin/api/2024-10/themes.json`, locate the target theme by ID, and assert `role` matches intent (production writes require `role=main` AND `id=186373570873`). Today's near-miss: stale auto-memory `feedback_push_target.md` framed `186373570873` as "the dev theme" (true pre-LAUNCH-2, false post-LAUNCH-2 since 2026-05-26 evening). Claude propagated the stale label into QW-1's verification table; the actual PUT was correct (production write was intended), but the labeling was wrong by accident, not by design — that is precisely the failure mode WATCHER-FORENSICS was supposed to harden against.

  **Design questions to resolve in the session (do not pre-decide here):**
  1. **Integration point.** Three candidates: (a) extend `scripts/preflight-watcher-check.sh` to also fetch + assert role; (b) standalone `scripts/preflight-role-check.sh` chained in `01-safety-preflight.md`; (c) wrap into `scripts/bbi-push-landing.py` as an internal pre-PUT gate. Trade-off: (a) keeps one preflight script — simpler but mixes concerns; (b) clean separation — two scripts to run; (c) closer to the actual PUT, harder to bypass, but only protects PUTs going through that script (not ad-hoc `curl` / Python).
  2. **Failure behavior.** Abort vs warn. Abort is strict (matches watcher-kill discipline) but blocks legitimate edge cases (e.g., role-swap during a planned launch). Warn requires explicit human ack each time — annoying but safer against role drift. Recommend: abort for ID/role mismatch on production target; warn-only for unexpected `name` while ID + role match.
  3. **Scope.** All themes or only LIVE-eligible PUTs? Pragmatic: apply to any PUT where the target theme has `role=main` regardless of which theme — that way the check protects ANY future production theme too, not just `186373570873`.
  4. **Verification output integration.** Should the verified `{id, role, name}` triple be auto-emitted into every verification table Claude produces? (Recommend yes — would have caught QW-1 framing error at write time, not in user review.)

  **Linked context:**
  - QW-1 incident detail: see Day 13 late-night entry below (operational lessons: stale-context failure mode).
  - Sister discipline already shipped: `feedback_preflight_watcher_check.md` (kill rogue watchers before PUT).
  - Memory now corrected: `feedback_push_target.md` rewritten 2026-05-27 late-night to require role-verification language.

- _(resolved 2026-05-27 · commit 994349d)_ **SCHEMA-CRIT-NEW-1 ✅ RESOLVED 2026-05-27** (commit `994349d` — F-15 fixed by deleting the `hasOfferCatalog` block; RRT-confirmed 0 invalid Product nodes) — _Original diagnosis + plan preserved:_ Reclassification of audit F-15 (originally "acceptable lightweight reference / not a defect" → **MISCLASSIFIED — actually critical**). `hasOfferCatalog` block (almost certainly in `theme/snippets/bbi-org-schema.liquid`) emits 8 category cards as `{"@type":"Product","name":"<category>"}` with no `offers` / `review` / `aggregateRating`. Google's Rich Results Test flags all 8 as invalid Product snippets sitewide (confirmed 2026-05-27 ~15:06 on obusforme PDP + `/pages/oecm`; visible on every `bbi_landing`-gated page that loads `bbi-org-schema` chrome).

  **Operational notes:** Single-fix session, not multi-fix like CRIT-1. Halt after each phase. Watcher preflight check FIRST (the watcher is killed but verify before any edit — this is now permanent discipline per `feedback_preflight_watcher_check.md`). Approval phrase: `fire schema-crit-new-1` (case-sensitive). Branch: `feature/schema-crit-new-1-2026-05-27` off `main` (if PR #28 merged by then) or off `feature/schema-crit-1-2026-05-27` (if not).

  **Phase 1 — Diagnosis (~15 min, no writes):**
  1. Locate the emitter. Confirm hypothesis: `bbi-org-schema.liquid` `hasOfferCatalog` block. Read the file, identify the loop that emits the 8 category items.
  2. Confirm rendering scope. Where does `bbi-org-schema.liquid` render? `theme.liquid`? Specific layouts? Document which pages emit this schema (= which pages currently fail RRT).
  3. Capture the current emitted JSON-LD for the `hasOfferCatalog` block (live API fetch + parse) — baseline state for the fix.

  **Phase 2 — Design (no writes; propose before approving):** Three candidates, pick best:
  - **Option A** — Change `@type` from `Product` to `OfferCatalog` entry items: `{"@type": "OfferCatalog", "name": "Seating", "url": "..."}`. Aligns with schema.org guidance for catalog references. Cleanest semantic match; no validation errors; no need to fabricate offers/aggregateRating.
  - **Option B** — Change `@type` to `CollectionPage` or `ItemList`. Treats the category cards as collection references. Valid, but semantically a different signal — these aren't really CollectionPages from this schema block's perspective.
  - **Option C** — Keep `@type=Product`, add minimal `offers` block referencing the category collection URL with placeholder price range or "InStock" availability. Functionally fixes the validation error but is semantically dishonest (a category isn't a single product with a single offer).

  Guidance: **Option A is almost certainly correct** — semantically honest representation: these ARE catalog entries, not products and not collection pages. Surface a recommendation with reasoning after reading the actual emitter.

  **Phase 3 — Fix:** single surgical snippet edit. Pre-write backup. Approval gate (case-sensitive `fire schema-crit-new-1`). Watcher preflight check FIRST. 30s CDN wait → byte-match verify → 60s phone hard-refresh.

  **Phase 4 — Verification:**
  - RRT on 2 pages: obusforme PDP + `/pages/oecm`. Both must show: 0 invalid Product snippets (8 category items either disappear from Product detection under Option A, or revalidate under whichever option chosen).
  - Theme check: 2850/166 must hold (or improve, not regress).
  - Pull JSON-LD via API on both pages → byte-confirm fix is on LIVE.

  **Dependency:** WATCHER-FORENSICS must complete first (including `scripts/preflight-watcher-check.sh` being wired into `01-safety-preflight.md`). Do NOT start until WATCHER-FORENSICS commits.

- _(shipped 2026-05-27 · commit fb1f661 · PR #29)_ **WATCHER-FORENSICS-AND-PROCESS-RECOVERY ✅ SHIPPED 2026-05-27** (commit `fb1f661`, on main · PR #29 — preflight script + operational doctrine + memory edit landed) — _Original scope preserved for record:_ `shopify theme dev --theme=186373570873` watcher (PID 28041) running since 2026-05-11 bound to LIVE main. Every edit in `theme/**` for 16 days was silently auto-PUT to LIVE within seconds of file save. Discovered 2026-05-27 ~14:25 during SCHEMA-CRIT-1 Fix 1 approval-gate breach. Watcher killed. Forensic LIVE snapshot at `data/forensics/2026-05-27-watcher-discovery/`. **Scope:**
  1. **LIVE-vs-git diff pass.** For every file in `theme/**` that exists in both the forensic snapshot and `git HEAD`: byte-compare. Surface every drift. Categorize: (a) JSON re-escape artifact — logically identical, ignore; (b) known intended LIVE-only state (e.g. Theme Editor section settings) — document, ignore; (c) unexplained drift — investigate.
  2. **Retroactive reconciliation of today's "drift events."** Re-examine the 3 substantive drift events on `templates/index.json` `bbi-shop` section that were attributed to Theme Editor cache flushes (09:57:27 v5→v4, 10:13:21 v4→v5, 13:15:38 v4→v5). With the watcher now known, was each event actually a watcher-pushed local file edit? Cross-reference local file mtimes against LIVE updated_at deltas from today's session logs.
  3. **Pre-session check script.** New `scripts/preflight-watcher-check.sh` that: fails loud (exit 1) if any `shopify theme dev` process exists; fails loud if any `shopify theme` process is bound to a `--theme=` matching a `role=main` theme; outputs the bound theme ID for human verification if any watcher exists; is wired into the existing `01-safety-preflight.md` workflow as a mandatory pre-write step.
  4. **Operational doc update.** Add section to `BBI-Session-Kickoff/` (or wherever discipline doc lives): "Watchers and auto-push: never run `shopify theme dev` against a `role=main` theme. Use a dev theme. The pre-session preflight check enforces this." Include the incident summary as a footnote so future sessions understand why the check exists.
  5. **Memory edit applied 2026-05-27 by Claude** — Leo's permanent memory now includes [feedback_preflight_watcher_check.md](../-/...) ("Before any approval-gated production write session on BBI/Shopify, check for running `shopify theme dev` watchers"). No further action needed on this item.

  Outputs: `docs/forensics/2026-05-27-watcher-incident.md` (incident report + drift findings + retroactive reconciliation results), `scripts/preflight-watcher-check.sh`, updated operational doc. No production writes. Branch: `feature/watcher-forensics-2026-05-27` off `main` (or off CRIT-1 branch if not yet merged).

- _(audit complete 2026-05-27 · fixes split out)_ **HOTFIX-SCHEMA-AUDIT-1 ✅ audit complete, fixes split between shipped + deferred** — comprehensive read-only schema audit completed 2026-05-27 afternoon on branch `feature/schema-audit-2026-05-27`. 12 emitter files cataloged (3 sitewide chrome + 9 section-level), 23 LIVE surfaces validated, 19 distinct fix items identified across 5 CRIT / 5 HIGH / 6 MED / 3 POLISH severity. Full report: [docs/audits/schema-audit-2026-05-27.md](../docs/audits/schema-audit-2026-05-27.md). Top critical findings: (1) PDP BreadcrumbList position-2 URL is broken — emits homepage URL instead of `/collections/business-furniture`, breaking Breadcrumb rich result on every PDP **[SHIPPED 2026-05-27 evening, anomalous]**; (2) Collection pages emit no `ItemList` / `CollectionPage` — no product-carousel rich result on ~22 collections; (3) Industry/segment landing pages (healthcare, education, government, non-profit, professional-services, industries hub) emit no surface-specific schema — chrome-only despite being highest-value B2B SEO pages; (4) PDPs missing Merchant Listings fields (`priceValidUntil`, `hasMerchantReturnPolicy`, `shippingDetails`, `itemCondition`); (5) PDP `brand.name` falls back to `product.vendor` = "Brant Business Interiors" on many SKUs causing manufacturer misattribution in SERP (e.g. dual-monitor-arm shows BBI as brand, actual brand Fellowes); (6) `booster-seo.liquid` is dead code carrying 5 unrendered duplicate-schema JSON-LD blocks (footgun, delete). Suggested execution: 4 fix sessions across 1-2 weeks (SCHEMA-CRIT-1/2/3 + SCHEMA-POLISH-1). No theme writes performed in audit session.

**Tier 2 — Pending (Week 1, medium priority):**
- ✅ **PERFORMANCE-MEASUREMENT-DISCIPLINE — RESOLVED 2026-05-30 · PR #52.** Formalized into a canonical home: new **`BBI-Session-Kickoff/measurement-protocols.md`** holds the discipline (multi-run median, min 3 runs, on already-fast pages where single-run Lighthouse has ±400-500ms variance; trust architectural correctness over single-run signals; applies to PSI mobile+desktop, local Lighthouse CLI, and any tool emitting Core Web Vitals lab estimates). Cross-linked from `01-safety-preflight.md` REFERENCE DOCS. The discipline was already referenced by name across this file (Day 13 HOTFIX-MOBILE-LCP work) but had never been written down — this closes that gap. Docs-only, no theme write.

- _(~30 min)_ **STORAGE-COLLECTION-COLD-CACHE** — `/collections/storage` measured Perf 78 / LCP 2187ms in the STEVE-PRIORITY Phase-4 Lighthouse spot-check (vs Perf 95-98 / LCP < 1500ms on every other measured collection). Root cause flagged as cold-cache origin response (`server-response-time: 558ms`, `network-server-latency: 1067ms`) — not fetchpriority-fixable. Re-measure after traffic warms the edge cache; if persists, investigate storage's section block content or backend data pattern. ~30 min.

**Tier 2 — Completed:**
- _(resolved 2026-05-29 · commit 7f08104)_ **WORKING-TREE-CLEANUP ✅ RESOLVED 2026-05-29** (commit `7f08104` — gitignore working artifacts, track audit outputs) — _Original:_ repo working tree carries pre-existing uncommitted state surfaced at Task A start: modified `.claude/launch.json` + many untracked directories and files (`data/working/*` from morning + Day 11 sessions, `BBI-Session-Kickoff copy/`, `Industry/`, `Leo/`, `Product Enrichment/`, `bbi-images-v2/`, `bbi-logo-v2.png` at repo root, several `data/reports/*` from today's tier-a-triage work, `data/strategy/_path-z-*` pickle/JSON, etc). Audit pass + commit/gitignore/delete sweep needed to leave the repo clean. ~30 min.

- _(resolved 2026-05-28)_ **PREFLIGHT-V2-BYTE-PRIMARY ✅ RESOLVED 2026-05-28 (PREFLIGHT-AUTOMATION session)** — shipped as `scripts/preflight-byte-compare.py`, a pure network-free comparison helper. **How to invoke:** `python3 scripts/preflight-byte-compare.py <local-file> <live-file>` (used in `01-safety-preflight.md` Rules 2a pre-write drift check + 4a post-write byte-match, replacing bare sha-equality HALTs). Primary signal is a 3-way `RESULT: IDENTICAL | SEMANTIC_MATCH | SEMANTIC_MISMATCH` (NOT binary — deliberately richer than the gates, which is why it is NOT folded into the session-start wrapper). Normalization classes, cumulative, earliest-match reported: (1) trailing-newline (all files); (2) JSON forward-slash unescape `\/`→`/` (.json only); (3) JSON canonical re-serialize for key-order/formatting (.json only). Secondary diagnostics emit raw + normalized shas and which class accounted for the diff. **Critical correctness boundary:** JSON normalization is scoped to `.json` files only — a `\/` diff in a `.liquid` file is treated as REAL drift, because the `\/` artifact is a JSON-string-serializer effect and `.liquid` assets are stored as raw text. Tested: ignores `\/`/newline/key-order noise as SEMANTIC_MATCH, but a genuine value change (`"Hero"→"DIFFERENT ALT TEXT"`) still HALTs as SEMANTIC_MISMATCH — proven in `scripts/test-preflight-checks.sh`. ~~_Original entry:_~~ upgrade preflight check to use byte-content / sha256 as the primary safety signal, with `updated_at` timestamp as secondary. Today's drift events bumped timestamps but were sometimes byte-only (JSON re-escape) and sometimes substantive (v4↔v5 substitutions); a byte-primary check would distinguish them automatically and avoid spurious HALTs. ~30 min. **Scope tightened 2026-05-27 final-night (HOTFIX-MOBILE-LCP-1a-HERO-SRCSET session):** primary normalization should cover (i) JSON forward-slash re-escape — `/` ↔ `\/` Shopify serializer toggle (this session's case; cost ~3 min Path A pull+re-edit on what was 0 substantive diff); (ii) JSON object key re-ordering — Shopify serializer is order-stable but worth confirming; (iii) trailing-newline differences — common false positive when local editors auto-append. Raw byte sha stays as secondary diagnostic signal. **Priority justification:** tonight's strict byte-match correctly halted on raw mismatch, but the actual drift was JSON `\/` re-escape (semantic no-op from Shopify's 13:15:38 Theme-Editor save). PREFLIGHT-V2-BYTE-PRIMARY would have classified this automatically: "drift but semantically equivalent — proceed with annotation" rather than full HALT requiring manual diff. Saves ~3 min per write session on this class of false-positive, and removes a cognitive interrupt during otherwise clean operations.

**Tier 2B — Pending (Week 1-2, medium priority — architectural / forensic hygiene):**
- **BRAND-SERVICE-SCHEMA-ERGOCENTRIC 🆕** (Tier 2B, low priority, ~20 min, added 2026-05-29 from BRAND-SERVICE-SCHEMA Phase 1) — Add a `Service` entity ("Authorized ergoCentric Dealer") to `theme/sections/ds-lp-brands-ergocentric.liquid`, the 6th brand page. Excluded from the initial 6-brand session because **no Leo-approved Service description was researched** (the brief's pre-verified per-brand data covered only keilhauer/global/teknion/otg/heartwood/obusforme). The page already carries a BRAND-1 Brand entity, so it's the only brand page without the Service layer. Mechanically trivial now that the snippet is parameterized — add one `{%- render 'bbi-service-jsonld', … id_suffix: "service-ergocentric" -%}` call after the existing Brand render. Requires ~10-min description research + Leo approval, then ~10-min schema addition.

- **BRAND-PAGE-FELDBERG-TENSE-AUDIT 🆕** (Tier 2B, low priority, ~5-10 min copy audit, added 2026-05-29 from BRAND-SERVICE-SCHEMA research) — Read the Global and Teknion brand-page copy (`theme/sections/ds-lp-brands-global-teknion.liquid`) for **present-tense references to Saul Feldberg**, who passed away in 2023. The #45 TEKNION-COPY-FIX rewrite added Feldberg-family framing ("Saul Feldberg founded Global in 1966 and Teknion in 1983, and his sons Joel and David lead them today") — the founding verbs are correctly past-tense, but confirm no copy implies Saul is still living. Update any present-tense usages. Surfaced during BRAND-SERVICE-SCHEMA; not blocking schema work.

- **SCHEMA-AREASERVED-FORMAT-HARMONIZE 🆕** (Tier 2B, low priority, ~30 min, added 2026-05-29 from BRAND-SERVICE-SCHEMA Phase 1/2) — Harmonize the `areaServed` format across all `Service` emitters + chrome to one canonical shape. Currently the brand + industry `Service` nodes (`bbi-service-jsonld.liquid`) emit `{ "@type": "AdministrativeArea", "name": "Ontario, Canada" }` while chrome (`bbi-org-schema.liquid` / `bbi-localbusiness-schema.liquid`) uses `{ "@type": "State", "name": "Ontario", "addressCountry": "CA" }`. Both are valid + semantically equivalent, but the inconsistency is avoidable. Pick one canonical form (the chrome `State`/`addressCountry` shape is the more structured/specific) and apply it everywhere. Not urgent — no validator or rich-result impact; pure schema hygiene.

- _(~1 hr + ~10 min · medium)_ **MANUFACTURER-LOGO-ACQUISITION 🆕** (Tier 2B, medium priority, ~1 hr + ~10 min, added 2026-05-29 from SCHEMA-BRAND-1 Phase 2 honesty-omission) — Acquire manufacturer logos from each of the 6 brands' public press/brand-asset pages (ergoCentric, Global, Heartwood, Keilhauer, ObusForme, OTG), upload to Shopify Files, then add an optional `logo` field to `theme/snippets/bbi-brand-jsonld.liquid` as an `ImageObject` param. BRAND-1 omitted `logo` because no manufacturer logo assets exist on file (`section.settings.logo` is BBI's logo, not the brand's — omitting was the honest call). Logo enriches the Brand entity for knowledge-graph. ~1 hr asset acquisition + ~10 min snippet edit. Single follow-up PR.

- _(medium · Steve-gated)_ **BRAND-PAGE-HERO-IMAGE-AUDIT 🆕** (Tier 2B, medium priority, **Steve-gated**, added 2026-05-29 from SCHEMA-BRAND-1 wrap) — Design audit on which of the 6 brand pages have/need hero images, and photography sourcing per page (Steve's own project photography vs manufacturer marketing imagery). Each brand section has a `hero_image` image_picker setting with a placeholder; several render the `lp-hero__ph` placeholder block on LIVE. Page-design + brand-positioning concern, Steve-gated. Not schema-related.

- _(~30 sec · content-side · Steve-gated)_ **STEVE-SET-BLOG-FEATURED-IMAGE 🆕** (Tier 2B, **content-side / Steve-gated**, ~30 sec, added 2026-05-29 from SCHEMA-BLOG-1 Phase 4) — Steve sets a **featured image** on `/blogs/news/oecm-ontario-school-boards-office-furniture` in Shopify Admin (Online Store → Blog posts → the post → Featured image). The post currently has **no featured image** (`article.image` is blank; the hero readers see is Shopify's derived first-inline-body-image, a separate mechanism), so the `BlogPosting` JSON-LD `image` field is honestly omitted → RRT flags `Missing field 'image' (optional)` and the **Article rich result won't fully display.** **No schema work needed once set** — the `ds-article.liquid` image block auto-populates with honest native dimensions via the `{% if article.image %}` guard already shipped. Unlocks Article rich-result eligibility on the only published post.

- _(~60–120 min · low priority)_ **CRITICAL-CSS-INLINE 🆕** (Tier 2B, **low priority**, added 2026-05-28 from HOTFIX-RENDER-BLOCKING-1 diagnosis, ~60-120 min) — The homepage's lone render-blocking resource is `bbi-homepage.css` (35 KB raw / ~6 KB gz), the theme's main stylesheet loaded unconditionally on all templates. It is critical above-the-fold CSS, so it cannot be safely deferred (FOUC). The only way to remove the 164–350ms render-block is to **extract the above-the-fold critical rules, inline them in `<head>`, and lazy-load the remainder** (preload + media=print/onload, or load on interaction). **Why low priority:** (1) payoff is ~164–350ms on the *simulated* Lantern LCP, which is the least trustworthy signal we have — no CrUX field data exists for this site; (2) FOUC risk is real and requires careful critical-path extraction + cross-template testing (the stylesheet loads on every template, not just the homepage); (3) the genuine mobile-perf harm is interactivity (TBT/INP), addressed by HOTFIX-MOBILE-LCP-1b, not by shaving render-block ms. Revisit only after 1b ships and if CrUX field data later shows a real LCP problem. **Do NOT attempt as a quick win** — it is a higher-risk change masquerading as a small one.

- _(~10 min)_ **FETCH-FILE-STALE-ID 🆕** (added 2026-05-28 from PREFLIGHT-AUTOMATION session, ~10 min) — `scripts/fetch-file.py` hardcodes inverted/stale theme-id labels: `LIVE_THEME_ID = '178274435385'` (post-LAUNCH-1 this is the role=**unpublished** ROLLBACK) and `DEV_THEME_ID = '186373570873'` (post-LAUNCH-1 this is role=**main** LIVE), with the default `THEME_ID = LIVE_THEME_ID`. So `fetch-file.py` with no override pulls assets from the **rollback theme, not LIVE** — the same stale-label failure class as the QW-1 memory bug, but baked into a script the pre-write backup discipline (Rule 2b) leans on. **Fix:** correct the constants to reflect post-LAUNCH-1 roles (LIVE=186373570873, ROLLBACK=178274435385) and update the default + comments; or better, resolve role via the Admin API (same call `preflight-role-check.sh` makes) instead of hardcoding. **Interim mitigation already shipped:** `01-safety-preflight.md` Rule 2b now warns against trusting the default and gives the explicit `186373570873` curl. Deliberately NOT fixed in the PREFLIGHT-AUTOMATION PR to keep that change scoped to the new preflight tooling. **Verify no other script shares the stale constants before closing.**

- _(~30–45 min residual · partially resolved)_ **PREFLIGHT-AUTOMATION ⚠️ PARTIALLY RESOLVED 2026-05-28 — composition shipped, auto-invocation still open.** The 2026-05-28 session built the unified composition wrapper `scripts/preflight-write-check.sh` (runs watcher → role, one combined `RESULT: PASS|FAIL`, exit 0/1) and wired it into `01-safety-preflight.md` Rule 0 / STEP 0, plus shipped the two component checks (PREFLIGHT-ROLE-VERIFICATION + PREFLIGHT-V2-BYTE-PRIMARY, both ✅ above). **Architecture chosen: (b) composed + wrapper** — evaluated against (a) one unified script and (c) standalone-no-wrapper. (a) was rejected because the three checks are not the same *kind* of thing: watcher + role are run-once binary session-start gates (compose cleanly into one command), but byte-compare runs per-file inside the write loop, takes two file arguments, and emits a 3-way signal — it cannot be a session-start binary gate without destroying its richer output. (c) was rejected because individual invocation is the exact 2026-05-27 failure mode (forget a step). (b) gives the single-command session-start ergonomics of (a) via the wrapper while keeping byte-compare as the separate per-file tool it structurally must be, and keeps role-check independently runnable per-PUT. The wrapper genuinely *calls* `preflight-watcher-check.sh` (not a reimplementation), so the watcher gate is preserved verbatim.
  **Residual (still Tier 2B, the original "(b) automated wrapper" intent in the harder sense — auto-invocation):** the wrapper still relies on human-paste + Claude self-enforcement to be *run*. Truly automatic invocation remains: (1) shell-rc hook (zsh/bash) that runs `preflight-write-check.sh` on `cd` into the repo; (2) wrap `bbi-push-landing.py` to refuse unless `preflight-write-check.sh` exited 0 in the same shell within the last N seconds; (3) git pre-push hook. Pick the lightest. The combined `RESULT:` line on the wrapper was designed to be greppable by exactly these. ~30-45 min.
  **Operational lessons (this session):**
  - **JSON key-order normalization is DEFENSIVE-BUT-UNOBSERVED.** No documented BBI drift event was caused by Shopify reordering JSON object keys (every real drift this codebase has logged was `\/` re-escape — see the LCP-1a Path-A entry and WATCHER-FORENSICS Event 3). The key-order class is retained anyway because the canonical `json.dumps(sort_keys=True)` pass that neutralizes `\/` *also* neutralizes key-order for free (zero marginal cost) and cannot mask a real value change (it only reorders). So: kept as cheap insurance, not because Shopify was observed to reorder. If a future session ever needs to know "did Shopify reorder keys" — we still haven't seen it do so as of 2026-05-28.
  - **`\/` normalization MUST be `.json`-scoped (subtle correctness boundary).** Applying JSON-string forward-slash unescaping to `.liquid` files would mask real edits, because the `\/`↔`/` toggle is a JSON-serializer artifact, not a Liquid one — `.liquid` assets are stored as raw text and a `\/` difference there is a genuine content change. byte-compare enforces this; the test suite proves a `.liquid` `\/` diff is reported SEMANTIC_MISMATCH.
  - **Verify the verifier with fail-on-bad fixtures; never mutate live to test a failure path.** A safety check that passes when it should fail is worse than no check (false confidence on every future write). Every check here was exercised against known-bad inputs (wrong-id-main, no-main, multi-main, malformed shape; real-value-change diff) that must FAIL/MISMATCH — using synthetic local fixtures and a `PREFLIGHT_ROLE_FIXTURE` escape hatch, so the live theme was never touched to prove a failure path. `scripts/test-preflight-checks.sh` is the committed 16-case regression suite (pass-on-good + fail-on-bad). This discipline should apply to any future safety-check work.
  - **`fetch-file.py` carries the same stale-label bug as the QW-1 memory** (out of scope here, flagged: FETCH-FILE-STALE-ID) — its default `THEME_ID = 178274435385` is the post-LAUNCH-1 *unpublished rollback*, not LIVE. Anything using its default to "snapshot LIVE" pulls the wrong theme. `01-safety-preflight.md` Rule 2b now warns and gives the explicit `186373570873` curl. byte-compare sidesteps it entirely by taking two already-materialized files (zero theme knowledge).

- _(~45–90 min)_ **HERO-SECTION-REFACTOR 🆕** (added 2026-05-27 final-night from HOTFIX-MOBILE-LCP-1a-HERO-SRCSET, ~45-90 min) — Migrate homepage hero from raw HTML in `custom_liquid` (`theme/templates/index.json` `bbi-hero` section) to proper section schema with `image_picker` + heading text settings (or a Liquid section using `image_url`/`image_tag` filters). Same architectural debt pattern as HP-SHOP-TILES-REFACTOR. Eliminates JSON-escape edit risk on every future hero change. Touched as part of HOTFIX-MOBILE-LCP-1a-HERO-SRCSET (2026-05-27 final-night) — the srcset/sizes fix landed via direct JSON edit with `<!-- Hero: raw HTML pending HERO-SECTION-REFACTOR (Tier 2B). Edit with JSON-escape discipline. -->` future-pointer comment, but future hero changes (alt text updates, image swaps, copy revisions) inherit the same JSON-escape-discipline fragility. **Sets convention:** comment-as-future-pointer in items that ship via the architecturally-fragile pattern while waiting for the proper refactor (mirrors LOCALE-CONFIG-EN-CA pointer in `theme.liquid`).

- _(~15–20 min)_ **LOCALE-CONFIG-EN-CA 🆕** (added 2026-05-27 late-night from QW-2 HOTFIX-LANG-ATTR-1) — Decide whether changing `primary_locale` en → en-CA at the shop level has acceptable side effects on email templates, currency, date format, and other locale-aware features. **If acceptable:** change shop config, remove the en→en-CA conditional from BOTH `theme/layout/theme.liquid:2` AND `theme/layout/password.liquid:2`. **If not acceptable:** document why and leave the `theme.liquid` conditional; also apply the same conditional to `password.liquid` for consistency (latent bug, `/password` route not active for BBI but identical pattern). ~15-20 min Shopify Admin investigation + theme cleanup. **Justification:** Option D shipped in QW-2 is a theme-layer workaround for a config-layer issue. Bundling `password.liquid` into this item keeps both layout files in sync — they always reflect the same decision, no fork in state across files. Linking comment is in the `theme.liquid` edit so the code itself points back here.

- _(~30–45 min)_ **BBI-SEO-METAFIELD-MIGRATION 🆕** (added 2026-05-27 late-night from QW-4 HOTFIX-HOMEPAGE-META-1, ~30-45 min) — Migrate hardcoded title + meta description in `theme/layout/theme.liquid` index template branch (lines 22 + 37) to `shop.metafields.global.{title_tag,description_tag}`-driven with hardcoded fallback. Pattern: `{{ shop.metafields.global.title_tag | default: 'Brant Business Interiors · OECM Furniture · Peterborough' }}` (or equivalent for description). Same architectural debt pattern as LOCALE-CONFIG-EN-CA — current QW-4 shipped a theme-layer fix for what should be a config-layer surface. Allows non-engineers (Steve, Leo without dev session) to update homepage SEO copy via Shopify Admin → Online Store → Preferences without touching theme code. **Scope:** (1) write metafields with current QW-4 values via Admin API; (2) update `theme.liquid:22` and `:37` to read metafields with hardcoded fallback; (3) verify Admin UI edits propagate to LIVE; (4) consider extending pattern to other `template == 'index'` and other-template hardcoded copy. **Justification:** Future Leo / future Steve should not need to open a PR to change a homepage meta description.

- _(~15 min)_ **VERIFY-CACHE-BUSTER-DEFAULT 🆕** (added 2026-05-27 late-night from QW-4 page_cache discovery, ~15 min) — Update standard post-PUT verification protocol to include both cache-busted (`?nocache=<ts>` + `Cache-Control: no-cache` header) and uncached curl, with explicit diff note when they disagree. **Justification:** QW-4 discovered that Shopify's HTML page_cache layer (visible via ETag `W/"page_cache:...:IndexController:..."`) is asynchronous from asset cache; the 30s CDN wait discipline verifies asset bytes on LIVE but NOT rendered HTML on cached template branches. Asset-layer sha-match alone gave a false "verification complete" signal in QW-4 until cache-busted re-curl confirmed actual storefront rendering. **Scope:** (1) document the cache-busted + uncached dual-check in `01-safety-preflight.md` or equivalent verification runbook; (2) when uncached returns OLD rendered HTML but cache-busted returns NEW, surface explicitly as "asset updated, page_cache TTL pending" — not as a failure; (3) add a one-line greppable signal line for tooling (e.g., `PAGECACHE_CHECK: BUSTED_OK / UNCACHED_PENDING`). Mirrors `RESULT: PASS/FAIL` pattern from `preflight-watcher-check.sh`. **Linked:** form-factor methodology lesson + page_cache methodology lesson are both Day-13-late-night artifacts of the same broader principle (verify methodology scope matches the layer being changed).

- _(~30 min)_ **FORENSIC-SNAPSHOT-TIME-WINDOWED** (added 2026-05-27 evening from WATCHER-FORENSICS Item 2 forensic gap) — upgrade future incident-response snapshot tooling to capture time-windowed asset history via Shopify Admin API polling (e.g. periodic `assets.json` snapshots stored with capture timestamp), not just a single current-state manifest. **Justification:** today's forensic snapshot manifest retains only the most-recent `server_updated_at` per asset, so the morning bumps on `templates/index.json` (09:54, 09:57:27, 10:13:21) were forensically erased by the 13:15:38 bump and limited the reconciliation certainty for Event 1 and Event 2 to "consistent with multiple causes" rather than definitive attribution. A time-windowed history would have made the watcher's morning activity directly visible. ~30 min for tool + runbook.

- _(~25 min)_ **DEV-THEME-PROVISIONING** (added 2026-05-27 evening from WATCHER-FORENSICS Item 4 doctrine gap) — provision a dedicated dev theme in Shopify Admin (`Online Store → Themes → Add theme → Create blank` or duplicate the current main). Until this is done, the doctrine "never run `shopify theme dev` against any BBI theme, period" (per `01-safety-preflight.md` Watchers and auto-push section) is in effect — no `theme dev` workflow is available at all. Once provisioned: update preflight doc + memory entries to allow `shopify theme dev --theme=<dev-theme-id>` and update `scripts/preflight-watcher-check.sh` to allow that specific theme role≠main. ~15 min Shopify Admin action + ~10 min doc/script updates.

- _(~30–60 min)_ **HP-SHOP-TILES-REFACTOR** (moved from Tier 1 2026-05-27 evening after WATCHER-FORENSICS Item 2 reconciliation) — move homepage "Shop the catalog" tile URLs out of `bbi-shop` section's `custom_liquid` raw HTML into `image_picker` schema settings (or a proper Liquid section using `image_url` filter calls). **Revised justification:** WATCHER-FORENSICS reconciled today's 3 apparent "Theme-Editor stale-cache" recurrences on this field as 2 plausibly watcher-attributable + 1 genuinely Theme-Editor (13:15:38). Watcher kill stops the dominant noise source, dropping urgency from Tier 1 to Tier 2B. However the underlying architectural fragility — untyped image URLs embedded in `custom_liquid` raw HTML are inherently vulnerable to a Theme-Editor save with stale cached state — remains real (Event 3 today). Refactor still wanted; just no longer urgent. ~30-60 min.
- _(~30–60 min · restored item 2026-05-29)_ **STARLITE-LEGACY-SNIPPETS-AUDIT 🆕** (Tier 2B, low priority) — Audit and retire legacy Starlite-theme snippets/sections still present in `theme/` from the pre-rebuild theme lineage (DS-VERIFY 2026-05-14 flagged ~64 legacy-starlite candidate section files; the root `snippets/` carries ~98 Starlite-legacy snippets per the Day-13 canonical-path note). Confirm none are referenced by live templates, then remove the dead ones to shrink the theme-check surface and reduce edit-confusion risk. Cross-ref `data/reports/ds-verify-2026-05-14.{csv,md}`. Restored 2026-05-29. ~30–60 min.
- _(~6–8 hrs · multi-session · NEW 2026-05-29 · Phase A Block 4 · **IN PROGRESS — Sessions 1-4 shipped 2026-05-30**)_ **OTHER-COLLECTION-TIER-A-ENRICHMENT 🆕** (Tier 2B) — **IN PROGRESS.** Enrich 338 currently-invisible products on /collections/other with structured PDP data (now a **13-field** `specs.*` framework, down from 15 — `tagline`/`standfirst` retired) to bring parity with the live catalog and enable Shopify storefront filters. **Sessions 1-4 (Day 17 evening) shipped 32 products enriched (PRs #60/#61/#63) + 183 vendor corrections (PR #62) + 4 reference files + manufacturer dictionary 3→19** — see the Day 17 evening (enrichment) section at the top of this file. Remaining: ~101 Global products (Sessions 5-8), ~9 MityBilt re-routes, 204 deferred (UNKNOWN SKU prefixes + 48 boilerplate-corrupted). Workflow revised Day 17 evening: manual paste-and-draft batched in 10s, replacing the prepped automated YAML pipeline; Session 4 proved a 20-agent parallel draft fan-out (~3.8 min wall-clock). See **Block 4 description** in the BLOG-LAUNCH-ROADMAP section for the full workflow. Queue source: `data/reports/other-collection-products-20260527-093211-with-recs.csv`.

**Tier 2B — Completed:**
- _(resolved 2026-05-29 · PR #47 · branch `feature/small-items-cleanup-a-2026-05-29`)_ **AUTHOR-URL-FIELD ✅ RESOLVED 2026-05-29** (shipped via SMALL-ITEMS-CLEANUP-A — see Day 16 entry at top of file). Added `author.url` = `https://www.brantbusinessinteriors.com/pages/about` to the BlogPosting Person in `ds-article.liquid` (honest live `/pages/about`, HTTP 200; no LinkedIn used). RRT "Missing field 'url' (optional)" on the author Person resolved; combined with Steve's featured-image upload, the OECM Article is now fully rich-result eligible. _Original diagnosis retained for reference:_ (Tier 2B, low priority, ~5 min, added 2026-05-29 from SCHEMA-BLOG-1 Phase 4) — Add an `author.url` to the `BlogPosting` Person entity in `theme/sections/ds-article.liquid`. The existing inline BlogPosting's `author` (`{@type: Person, name: "Steve Katz"}`) has **no `url`** — pre-existing schema choice, NOT introduced by BLOG-1 (we didn't touch the author field) — so RRT shows a second non-critical `Missing field 'url'` on the Person. Options: `/pages/about` (where Steve is introduced on-site) OR his LinkedIn. Honesty: only emit a url that genuinely profiles the author. Bundle into the next blog/content session.

- _(resolved 2026-05-29 · PR #47 · branch `feature/small-items-cleanup-a-2026-05-29`)_ **BRAND-PAGE-COPY-SINGLE-SOURCE-PHRASING ✅ RESOLVED 2026-05-29** (shipped via SMALL-ITEMS-CLEANUP-A — see Day 16 entry at top of file). Resolved via **Option 3 rephrase** of the L195 "Tiered" diff card on `ds-lp-brands-global-teknion.liquid`: `without mixing manufacturers or finish palettes` → `without juggling separate dealers or mismatched finishes` — removes the manufacturer-count claim entirely, no contradiction with the TEKNION-COPY-FIX sister-company reframing. _Original diagnosis retained for reference:_ (Tier 2B, low priority, ~5 min OR no-action, surfaced during BRAND-PAGE-TEKNION-COPY-FIX Phase 3 self-catch) — The dedicated Global/Teknion page's diff card (`theme/sections/ds-lp-brands-global-teknion.liquid` L195) claims BBI offers the range *"without mixing manufacturers."* Now that Teknion is reframed as a **separate manufacturer** (sister company to Global, not a GFG family member), the claim's interpretation matters: the **"single-source dealer convenience"** reading is still accurate (one BBI quote/delivery/install across all lines); the **"single-manufacturer product line"** reading is now soft (Teknion ≠ Global's manufacturer). **Resolution options:** (a) ~5-min copy edit to rephrase toward the dealer-convenience framing (e.g. "without juggling multiple dealers" / "one source, one quote"), OR (b) close as **no-action** if "single-source dealer" was always the intended reading. Leo's call when next in this file.

- _(resolved 2026-05-29 · PR #45 · branch `feature/brand-page-teknion-copy-2026-05-29`)_ **BRAND-PAGE-COPY-FIX ✅ RESOLVED 2026-05-29** (shipped as **BRAND-PAGE-TEKNION-COPY-FIX**, independent off `main` @ `b2c1b79` — see Day 16 afternoon entry at top of file). **Leo took the decision in-session this afternoon rather than routing through Steve; fix landed same day.** Sister-company framing (Teknion + Global = Feldberg-family sister companies, NOT parent/sub) now corrected across the dedicated page + hub + about page; OTG/ObusForme left as genuine GFG brands; OECM/dealer claims preserved; BRAND-1 schema was already correct so no schema changes. _Original diagnosis retained for reference:_ (Tier 2B, medium priority, **likely Steve-gated**, added 2026-05-29 from SCHEMA-BRAND-1 Phase 1) — The `brands-global-teknion` page copy (`theme/sections/ds-lp-brands-global-teknion.liquid`) mislabels **Teknion as a Global "tier" / member of "the Global Furniture Group family" / Global as the "parent" behind its lines** (e.g. hero badge "Global flagship + **Teknion premium tier**", intro "Global Furniture Group is the…contract furniture **parent** behind…lines", FAQ "**All four are part of the Global Furniture Group family**"). **This is a factual error:** per verification (Leo, 2026-05-29, sourced to Global's own press release on Saul Feldberg's passing), **Teknion and Global are independent SISTER companies under common Feldberg family ownership — NOT parent/subsidiary.** Saul Feldberg founded Global (1966) and established Teknion (1983); Joel Feldberg = Global CEO, David Feldberg = Teknion CEO. ObusForme + OTG *are* genuine GFG brands; Teknion is not. The page's tiered-portfolio framing needs a rewrite that positions Teknion as a co-represented independent brand BBI deals (BBI is a confirmed Teknion dealer per teknion.com/ca/locations/locations-dealers), not a GFG sub-tier. **NOT touched by SCHEMA-BRAND-1** (schema-only scope — the emitted Brand schema is already factually correct: two standalone Brand entities, no parent/sub relationship asserted). **Steve-gated likely** — dealer-page brand positioning is a copy/marketing decision he'll have opinions on. ~30-45 min copy rewrite when greenlit.

- _(shipped 2026-05-29 · commit a43c489 · merged 2026-05-30 · PR #48)_ **BRAND-SERVICE-SCHEMA ✅ MERGED 2026-05-30** (commit `a43c489`, branch `feature/brand-service-schema-2026-05-29`, merged to main 2026-05-30 via PR #48 — 6 Service entities across 5 brand-page templates) — _Original deferral note preserved:_ Emit a `Service` entity on each brand page describing BBI's *dealer relationship* per brand (custom design coordination, manufacturer-showroom visits, project delivery + install, OECM eligibility). CRIT-2-shaped pattern via a new `bbi-brand-service-jsonld.liquid` (mirrors `bbi-service-jsonld.liquid`). **Particularly relevant for Teknion** (no stock products in the BBI catalog — the relationship is pure service/specify-and-deliver) and partially for Global (mixed catalog + service). Defer until there's a clear AEO/positioning reason — BRAND-1's Brand entities already ground the manufacturer identities; this would add the service layer on top.

- _(shipped 2026-05-29 · commit f8d83f5 · merged 2026-05-30 · PR #46)_ **SCHEMA-CORPORATE-HIERARCHY-FIX ✅ MERGED 2026-05-30** (commit `f8d83f5`, branch `feature/schema-corporate-hierarchy-2026-05-29`, merged to main 2026-05-30 via PR #46 — chrome parentOrganization 2-tier → 3-tier) — _Original Steve-gated note preserved:_ Current chrome (`bbi-org-schema.liquid`) captures **BBI → Office Central** directly (2-tier), skipping the intermediate legal parent. **Actual structure (per Leo, 2026-05-29):** BBI (operating brand) → **Brant Basics** (immediate legal parent, operated/owned by Office Central, operates separately) → **Office Central** (ultimate owner). The OECM blog post body *correctly* describes the 3-tier structure ("registered under our parent legal entity, Brant Basics") — which now **conflicts with the 2-tier chrome schema.** Fix: restructure chrome to insert Brant Basics as an intermediate `Organization` tier — `parentOrganization` on BBI → Brant Basics, `parentOrganization` on Brant Basics → Office Central. **Steve-gated** (corporate-positioning call). Note: BLOG-1's BlogPosting `publisher` correctly references the BBI `#organization` entity (the operating brand publishes the blog) — that's accurate regardless of how the parent tiers are restructured.

- _(resolved 2026-05-29 · commit 69c8d12 · on main)_ **THEME-CHECK-CONFIG ✅ RESOLVED 2026-05-29** (commit `69c8d12`, on main — `.theme-check.yml` now committed at theme root) — _Original rationale preserved:_ Commit a `.theme-check.yml` at the theme root pinning the canonical scope so `shopify theme check` produces the canonical `2833/165` (or whatever the live number is) **regardless of which directory it's invoked from.** No config exists today, so a repo-root invocation scans the entire tree (data/backups, scripts, etc. → ~11,256 offenses) AND mis-resolves theme assets/snippets from the wrong root, throwing context-sensitive `MissingTemplate`/`MissingAsset` false-positives (CRIT-1c saw repo-root give an inflated `3216/219` that collapsed to the canonical `2833/165` when run from `theme/`). Pinning the root eliminates the whole "wait, why is the count different" confusion class. **Operational lesson meanwhile: the canonical theme-check invocation is `shopify theme check` run from the `theme/` directory, NOT from repo root.** Not blocking — pure hygiene.

- _(resolved 2026-05-28)_ **SCHEMA-H-1 ✅ SHIPPED 2026-05-28** (branch `feature/schema-polish-1-2026-05-28`, run alongside the SCHEMA-POLISH-1 triage — see the consolidated SCHEMA-POLISH-1 + SCHEMA-H-1 entry above for full detail). Converted the inline `provider` LocalBusiness redeclarations in `ds-lp-oecm.liquid` + `ds-lp-quote.liquid` to `@id` refs to `#organization`. **LocalBusiness node count 3→2 per page; F-4 duplicate-entity RESOLVED on both.** ✅ Clean swap (no property loss), drift IDENTICAL, post-PUT byte-compare IDENTICAL, theme check 2833/165 held, sibling schema intact, storefront RRT confirms 2 nodes (was 3). **⚠️ Important — H-1 did NOT clear the "Local businesses non-critical" WARN.** That WARN is the *separate* missing-`image`-field finding (F-LOCALBUSINESS-IMAGE, logged above), confirmed via post-H-1 RRT to persist by design. F-4 (fixed) and the missing-field WARN (untouched) are distinct — the original H-1 framing here conflated them.

**Tier 2B — Reference / Operational Lessons:**
- **OPERATIONAL LESSONS (SCHEMA-CRIT-1c, 2026-05-29):**
  - **"WARN persists but field strings show why" diagnostic discipline** (this session's catch + yesterday's H-1 catch). Do NOT read a residual non-critical RRT badge as failure without clicking into the row — the field strings disambiguate three distinct states: (a) "fix didn't work" (structural block missing), (b) "fix worked but unrelated warnings remain" (e.g. F-8 review data), and (c) "fix worked, the flagged field is a deliberate omission surfaced as a recommendation" (e.g. `shippingRate`). CRIT-1c's Merchant-listings WARN moved from (a) to (c) — a successful structural close, not a miss. Same trap H-1 fell into (conflating F-4 duplicate-entity with the missing-`image` WARN).
  - **"Deliberate omission > fabrication" honesty pattern.** When a schema field has no honest value — `shippingRate` when shipping is quoted at order time, `returnShippingFeesAmount`/`restockingFee` when fees are variable/conditional — **omitting is correct even though RRT flags it as recommended-but-missing.** Better a recommended-field nudge than a false claim (a fabricated `$0` shippingRate falsely signals free shipping). Schema must reflect real published policy; where the policy is richer than a flat value can honestly capture, omit and document why. **Extension (SCHEMA-BRAND-1):** the principle has an *upgrade* corollary — when the *correct* value is reachable with one more verification step, reach for it rather than omitting OR pointing at a plausible-but-wrong value. ObusForme's sameAs: `obusforme.com` (the consumer wellness brand) was the wrong entity; one more search surfaced the correct GFG product-line URL. Heartwood's `heartwoodmfg.com` was dead; one more search surfaced the live `heartwood.ca`. Verify-then-emit beat both omit-on-doubt and emit-the-guess.
  - **RRT scope limitation — Google's Rich Results Test only displays rich-result-ELIGIBLE entities** (Article, Book, FAQ, JobPosting, LocalBusiness, Organization, Product, Recipe, Review, etc.). Non-eligible schema like standalone `Brand`, `Service`-without-`Product`, or generic Organization sub-types renders to HTML and IS parsed by Google but does **NOT** appear in RRT's "Detected structured data" panel. Verify non-eligible schema via **validator.schema.org** (full schema visibility, not just the rich-result UI) plus **cache-busted curl** (HTML emission confirmation). RRT's "X valid items detected" headline is the *rich-result-eligible items count*, NOT the *total schema-blocks-on-page count*. Future sessions emitting `Brand`/`Service`-alone/entity-graph-grounding schema should **not** predict RRT items-count increases. **Discovered during SCHEMA-BRAND-1 Phase 4** — predicted +1 (single-brand) / +2 (global-teknion) items, actual was **+0** (Brand entities not displayed in RRT despite being parsed cleanly with 0 errors). The 0-errors result is the success signal for non-eligible schema, not the items-count delta.

**Tier 3 (Week 2-3, polish):**
- **LIVE-booster-seo-asset-removal** 🆕 (low priority, ~5 min, **own session — destructive op**) — `snippets/booster-seo.liquid` was deleted from the repo in SCHEMA-CRIT-1b (2026-05-28) but the inert asset still exists on the LIVE theme (186373570873, 28,490 bytes). It is orphaned/un-rendered on LIVE (confirmed: PDPs emit exactly 1 Product, zero standalone Organization/WebSite/Blog/Article blocks), so it harms nothing. Removing it from LIVE requires a destructive irreversible `DELETE /themes/186373570873/assets.json?asset[key]=snippets/booster-seo.liquid` — do it as its own deliberate session (destructive-op discipline), never bundled into another fix's approval phrase. Zero functional upside; pure hygiene. Skip unless doing a LIVE-theme dead-asset sweep.
- **SEATING-COLLECTION-HERO-V6** — current seating hero v5 is a canvas-expanded mesh-back chair on white (functional but catalog-shot, not lifestyle). Source proper lifestyle seating image when Steve provides a photo. ~30 min once source is in hand.
- **HOMEPAGE-HERO-WIDTH-1200** — deferred optimization from STEVE-PRIORITY Phase 4-C. Homepage hero currently delivered at `?width=1920` (471KB after Shopify CDN resize). Drop to `?width=1200` (~250KB) only if LCP regression observed post-traffic-warm; today's homepage Perf 96 / LCP 1317ms is comfortably under CWV targets so don't trade desktop quality preemptively. ~5 min when needed.

**Closed items (this session):**
- **AVADA-LOGO-CLEANUP** ✅ closed 2026-05-27 — `New_OC_BBI_Logo-raster_x320.png` Avada-era reference was already gone from `theme/`, `config/`, `settings_data.json`, and rendered HTML by the time STEVE-PRIORITY Phase 4-A ran the audit. Likely self-resolved during FAVICON-1 + SEO-AUDIT-1 work yesterday. No remaining references.
- **EDU-HERO-FETCHPRIORITY** ✅ closed 2026-05-27 — STEVE-PRIORITY Phase 4-B added `fetchpriority: 'high'` to every `ds-lp-*` hero `image_tag` using `loading: 'eager'` (20 files) + Phase 4-B-extended added it to `ds-cc-base.liquid:631` (collection hero applying to 12 BBI collection templates). All 21 hero image tags across BBI landing pages + collection pages now carry the hint. Education page LCP improvement: 1735-2124ms → 1270ms (-600ms typical).

### Branch
`feature/post-steve-cleanup-2026-05-27` (off `feature/steve-priority-changes-2026-05-27 @ 21c0e2a`).

---

## 🛑 SCHEMA-CRIT-1 Fix 1 + WATCHER-DISCOVERY-2026-05-27 ⚠️ 2026-05-27 evening (Day 13)

**Fix 1 (BreadcrumbList position-2 URL) shipped under anomalous discovery conditions** — outcome bytes match intended fix, but change was promoted to LIVE by a long-running auto-push watcher *before* the approval phrase authorized a manual PUT. The session pivoted from sequential-write execution to incident response, forensic snapshot, watcher kill, and process-recovery backlog work. Fix 2 / Fix 3 / Fix 4 explicitly deferred to next session. Branch `feature/schema-crit-1-2026-05-27` off `feature/schema-audit-2026-05-27 @ 63c9596` (audit not yet in main).

### Pre-session — all checks passed

- Branch base decision: audit commit `63c9596` not yet in main → branched off audit branch (per session prompt).
- LIVE theme verified: 186373570873 ("BBI Landing Dev", role=main), `updated_at=2026-05-27T13:15:38-04:00` ✓ matches prompt-stated baseline.
- Rollback theme verified: 178274435385 ("BBI Live", role=unpublished) ✓.
- Theme-check baseline `2852/166` (2048 errors + 804 warnings) ✓ matches prompt invariant.
- Canonical source path: file lives only at `theme/snippets/bbi-product-jsonld.liquid` — root `snippets/` is 98 Starlite-legacy snippets (no `bbi-*` files); push script `bbi-push-landing.py` operates on `theme/`. Prompt's `snippets/bbi-product-jsonld.liquid` shorthand confirmed to mean the theme/ canonical.
- Pre-write backup created: `data/backups/2026-05-27-schema-crit-1/{bbi-product-jsonld.liquid.pre-fix1, booster-seo.liquid.pre-delete}` (booster-seo backed up though Fix 4 ultimately deferred).
- Discipline gap (now closed by feedback memory `feedback_preflight_watcher_check.md`): pre-session did NOT check for running `shopify theme dev` watchers. This gap is what allowed the breach.

### Fix 1 local edit + breach detection

**Local edit applied** at ~14:23 EDT: 1 line added (`{%- assign bc2_u = bc_base | append: '/collections/business-furniture' -%}` before render), 1 render arg changed (`bc2_url: bc_base | append: '/collections/business-furniture'` → `bc2_url: bc2_u`). Matches the existing `bc3_u` pre-assign pattern used elsewhere in the file. Implements audit recommendation C-1 verbatim.

**Approval phrase proposed:** `fire schema-crit-1 fix-1` — Leo confirmed approach with two adjustments (Rich Results Test mandatory; root `snippets/booster-seo.liquid` out of scope as Starlite legacy) and authorized via embedded-phrase form.

**Pre-PUT updated_at re-check (immediately before manual PUT) caught drift:**
- Pre-session updated_at: `2026-05-27T13:15:38-04:00`
- Pre-PUT updated_at:    `2026-05-27T14:24:14-04:00`
- DRIFT — investigated immediately, no PUT issued.

**Asset-level investigation revealed the bumped asset was `snippets/bbi-product-jsonld.liquid` itself**, size 7029 bytes, server-side `updated_at=2026-05-27T14:24:13-04:00` (one second before the theme bump). The byte content was identical to Claude's LOCAL post-edit file: sha256 `4fe3c703fab0e62b4c253a82f2669c181f06a6da73e257f5a5e06c4b5591e66b` on both LIVE and LOCAL; pre-fix backup sha256 `21e0156f31312e53f0928a18b069844a28c92900fc68d9d4c40f4274e1742a9f`.

Claude's command history had no PUT — only Edit/Read/diff/ls/cp/curl-GET. Something else in the environment had pushed.

### Root cause — orphaned `shopify theme dev` watcher

`ps aux | grep shopify` revealed:

```
leokatz  28041  3.4 0.1 469873920 9392 ??  SN  11May26 518:31.35
  node /opt/homebrew/bin/shopify theme dev
       --store=office-central-online
       --theme=186373570873          ← LIVE main
       --port=9292
```

A `shopify theme dev` watcher running since 2026-05-11 (16 days), bound directly to the LIVE main theme. Every local edit under `theme/**` in this repo had been auto-PUT to LIVE within seconds for the entire 16-day window — including but not limited to today's Fix 1 attempt.

### Containment + forensic snapshot

- **14:30 EDT — watcher killed.** PID 28041 confirmed dead via `ps -p 28041` (exit 1). No other shopify processes running.
- **14:30+ EDT — full LIVE theme snapshot taken** to `data/forensics/2026-05-27-watcher-discovery/`:
  - `meta/theme.json` — theme metadata at snapshot time
  - `meta/assets-index.json` — 359-asset index with server checksums + sizes + updated_at
  - `snapshot/` — every asset downloaded (mirror of LIVE theme tree, 6.2 MB total)
  - `meta/snapshot-manifest.json` — per-asset sha256 + md5 + size + live-md5-match flag
  - `README.md` — incident timeline + directory key + immutable-evidence notice
- Snapshot integrity: 311/359 assets md5-match LIVE server checksum byte-exactly; the 48 mismatches are all `.json` files (config/settings_*, templates/*) showing the known JSON re-escape wire-format variance (semantically identical, documented pattern from earlier today's drift log).
- Snapshot byte-confirmed for the audited file: `data/forensics/.../snapshot/snippets/bbi-product-jsonld.liquid` sha256 = LIVE sha256 = LOCAL sha256 = `4fe3c703…`.

### Fix 1 verification (post-watcher-kill, Fix 1 only — verified for record, NOT to authorize further fixes)

| Check | Result |
|---|---|
| LIVE bytes vs intended Fix 1 bytes | byte-identical (sha256 `4fe3c703…`) |
| 3-PDP JSON-LD pull (seating / desking / storage) | All 3 emit `position 2: name='Shop Furniture' item='https://www.brantbusinessinteriors.com/collections/business-furniture'` |
| BreadcrumbList block parses on all 3 PDPs | ✓ 4 positions each, well-formed |
| Theme check post-fix | **2850/166** (file count unchanged; 2 `UnusedAssign` warnings on the edited file incidentally cleared by static-analysis shift when filter chain pulled into named assign; zero new offences anywhere) |
| Rich Results Test | **CONFIRMED 2026-05-27 ~15:06** — Breadcrumbs: **1 valid item detected** on the obusforme PDP. Fix 1 landed cleanly from Google's perspective. Detail block below. |

PDPs sampled: `obusforme-comfort-high-back-chair-fabric-1240-3` (seating), `height-adjustable-table-5-sizes` (desking), `pedestal-box-box-file-with-or-without-wheels` (storage).

### Rich Results Test — 2026-05-27 ~15:06 EDT

Tested URL: `https://www.brantbusinessinteriors.com/products/obusforme-comfort-high-back-chair-fabric-1240-3` via [search.google.com/test/rich-results](https://search.google.com/test/rich-results).

**Fix 1 result: ✓ CONFIRMED.** Breadcrumbs — 1 valid item detected. Position-2 URL fix landed from Google's perspective. Breadcrumb rich result eligibility moved from blocked → eligible on PDPs.

**Other detected items on the same PDP (for the record):**
- **Merchant listings: 1 valid item, 2 non-critical issues** — missing `shippingDetails` + `hasMerchantReturnPolicy` (exactly the SCHEMA-CRIT-1c-deferred scope; gated on returns + shipping policy pages going live; working as designed).
- **Local businesses: 2 valid** (combined Org+LocBus + dedicated LocalBusiness emitters).
- **Organisation: 2 valid.**
- **ObusForme Product snippet itself: valid** with the same 2 non-critical issues as Merchant Listings.
- **`brand.name` on the ObusForme product = "Global Furniture Group"** (correct manufacturer, NOT the vendor="Brant Business Interiors" fallback). Worth flagging: the audit's brand.name fix (originally CRIT-1c Fix 2) was scoped on the Fellowes `dual-monitor-arm` example, but this chair shows enriched products already emit correct brand. **Triage hint for CRIT-1c:** count how many SKUs actually have `vendor="Brant Business Interiors"` *and* lack `specs.manufacturer` before assuming the fix is high-impact across the catalog. May be lower priority than originally scoped.

### Audit F-15 reclassification — NOT a net-new finding, an audit error

The RRT test surfaced what was initially framed as a "net-new defect," but is correctly understood as **a reclassification of existing audit finding F-15**, not a discovery outside the audit's scope.

- **Audit F-15 (Phase 1, line 146)** stated: `hasOfferCatalog` in `bbi-org-schema` uses lightweight `{"@type":"Product","name":"Seating"}` items. *"Acceptable per Google guidelines (lightweight references, not full Product nodes). NOT a defect."*
- **Google's Rich Results Test (2026-05-27 ~15:06 EDT, run on the obusforme PDP + `/pages/oecm`) contradicts the audit:** 8 invalid Product snippets detected, error on all 8: "Either 'offers', 'review' or 'aggregateRating' should be specified."
- **Items affected (8/8 match the `hasOfferCatalog` category list exactly):** Seating, Tables, Storage & Filing, Desks & Workstations, Boardroom Furniture, Ergonomic Products, Panels & Room Dividers, Quiet Spaces & Acoustic Pods.
- **Reclassification:** F-15 → status changed from "acceptable lightweight reference / validator false positive" to **"MISCLASSIFIED — actually critical."** The audit assumed Google's docs about lightweight `hasOfferCatalog` references meant the validator would treat them as references rather than Product entities. **It does not.** Google's validator parses every `{"@type": "Product"}` node — nested or not — as a Product instance requiring Product-validation compliance. Lightweight nesting is a schema.org pattern, not a Google-validator carve-out.
- **Scope of impact:** every page that emits `bbi-org-schema` chrome (every `bbi_landing`-gated page). At minimum 1 PDP + 1 page confirmed; almost certainly sitewide.

Audit doc updated with an explicit Addendum dated 2026-05-27 documenting the reclassification + methodology gap (manual schema review without running RRT on real URLs allowed this misclassification to land). See [docs/audits/schema-audit-2026-05-27.md](../docs/audits/schema-audit-2026-05-27.md) — the Addendum at end of doc.

Tracked as **SCHEMA-CRIT-NEW-1** (Tier 1, full scope in backlog). Blocked on WATCHER-FORENSICS-AND-PROCESS-RECOVERY.

### Discipline implications

- **Outcome correctness:** Fix 1 bytes on LIVE are exactly what the approval gate would have produced. The intended fix is in place.
- **Process integrity:** Failed. The `fire schema-crit-1 fix-1` approval phrase was issued but Claude's PUT never executed because the watcher beat it. The gate was bypassed, even if intent and outcome aligned.
- **Scope of the historical breach:** Any local `Edit` under `theme/**` from 2026-05-11 through 2026-05-27 14:30 was auto-promoted to LIVE main without an approval gate. This is the scope WATCHER-FORENSICS-AND-PROCESS-RECOVERY must reconcile.
- **Re-attribution candidates:** The 3 "Theme-Editor stale-cache" events on `templates/index.json` `bbi-shop` section in today's drift log (09:57:27 v5→v4, 10:13:21 v4→v5, 13:15:38 v4→v5) all happened during periods of human + Claude activity in the repo. With the watcher now known, some or all may actually have been watcher-pushed local edits rather than Theme-Editor saves. Retroactive reconciliation is in scope for WATCHER-FORENSICS.

### LIVE 186373570873 updated_at trail — Day 13 evening additions

```
2026-05-27T13:15:38  Steve/Leo Theme-Editor save (substantive — v4→v5 self-correction, per afternoon Task A) — OR watcher-pushed Claude edit (re-investigate)
2026-05-27T14:24:13  WATCHER-PUSHED Fix 1 — snippets/bbi-product-jsonld.liquid (unauthorized; outcome bytes match approval-intent)
2026-05-27T14:24:14  theme updated_at rolled
```

No other writes to LIVE in this session.

### Safety

- **Theme-check baseline:** held at `2852/166` through pre-session; landed at `2850/166` post-watcher-pushed-Fix-1 — improvement-only delta, both warnings cleared on the edited file, zero new offences. File count unchanged (166).
- **ROLLBACK 178274435385:** `unpublished` throughout, untouched.
- **No Theme Editor opened by Claude.** Phone hard-refresh discipline preserved.
- **Watcher status now:** dead. Preflight memory saved so future sessions check before any approval-gated work.
- **No PUTs issued by Claude this session.** All LIVE bytes traceable to the orphaned watcher.

### POST-LAUNCH BACKLOG — Tier 1 reordered

**WATCHER-FORENSICS-AND-PROCESS-RECOVERY is now Tier 1 top-of-stack, before any SCHEMA-CRIT-1b / CRIT-2 / CRIT-3 / POLISH-1 work resumes.** SCHEMA-CRIT-1 itself is split: Fix 1 shipped (anomalous), Fix 2 / 3 / 4 deferred. Updated Tier 1 below.

### Commit + branch

Branch: `feature/schema-crit-1-2026-05-27` off `feature/schema-audit-2026-05-27 @ 63c9596`. Commit message acknowledges the discipline breach explicitly. Pushed to origin; PR opened against `main` (will require audit branch to merge first or be retargeted).

---

## 🎨 STEVE-PRIORITY-CHANGES-2026-05-27 ✅ 2026-05-27 midday (Day 13)

Three Steve-requested visual changes + post-change speed optimization, all on LIVE `186373570873` between 10:51 and 12:38 EDT. Exact-match approval discipline (`fire …`, `<phase> good`) at every gate. 7 production write rounds across 35 unique theme files (some edited in multiple rounds). Theme-check baseline `2852/166` held EXACTLY across every write. No regressions.

### Phase 1 — Primary button color invert (sitewide)
- **Round 1 base CSS** (`bbi-homepage.css`, 11:03:42): inverted `.bbi-btn--primary` rule — `#D4252A` default, `#0B0B0C` hover.
- **Scope discovery**: 22 scoped overrides in `.lp-*` / `.ds-cc` / `.ds-cs` selectors using `var(--buttonBackground)` masked the base edit on every BBI page.
- **Round 2 extended** (33 files, 11:15:37): swapped literal hex values in each section's canonical `.scheme-default` block (or equivalent) — `--buttonBackground: #0B0B0C → #D4252A`, `--buttonBorder: #0B0B0C → #D4252A`, `--buttonBackgroundHover: #D4252A → #0B0B0C`, `--buttonBorderHover: #D4252A → #0B0B0C`. Plus `bbi-nav.liquid` header rule (hardcoded hex, not var-based) swapped directly.
- **Files touched**: `theme/assets/bbi-homepage.css` + 25 STANDARD section files (ds-article, ds-blog-list, ds-cart-base, ds-collection-base, ds-cs-base, ds-lp-{about, brands, brands-ergocentric, brands-global-teknion, brands-heartwood, brands-keilhauer, brands-obusforme, brands-otg, contact, customer-stories, delivery, design-services, faq, oecm, our-work, quote, relocation}, ds-pdp-base, ds-search-results, ds-system-404) + 7 VARIANT section files (`ds-cc-base`, `ds-lp-education`, `ds-lp-government`, `ds-lp-healthcare`, `ds-lp-industries`, `ds-lp-non-profit`, `ds-lp-professional-services` — main scope swapped, `.lp-closer` / `.ds-cc__phone-cta` white-button secondary scopes LEFT UNTOUCHED per design) + `theme/snippets/bbi-nav.liquid`.
- **Untouched**: all `.scheme-inverse` blocks (light-on-dark sections), `style-variables.liquid` (Shopify-settings-driven), `media-grid.liquid` (block-setting-driven), `.bbi-mobile-nav__quote` (already different reds).
- **Side effect**: `.bbi-search__pagination span.current` (current-page pill on search pagination) reads `var(--buttonBackground)` so renders red now — semantically correct as "active page" indicator.

### Phase 2 — PDP pricing red + 12.5% size bump
- **Write** (`ds-pdp-base.liquid:179-186`, 11:23:29): `.pdp-price-row` font-size `22px → 25px`, color added `var(--saleBadgeBackground)` = `#D4252A`. font-weight, font-family, margin unchanged. No `!important`.
- **Markup**: PDP price element is a single `<div class="pdp-price-row">` — no compare-price strikethrough rendered (compare_at_price is exposed in variant JSON for JS but never displayed). Sale price + regular price get identical red treatment.
- **NOT changed**: `.pdp-prod-card__price` (related-products card on PDP, font-size 14px black). Collection-grid product card prices on `/collections/*` (separate template). All stay inherited-ink color.

### Phase 3 — Collection page layout reorder
- **Write** (`ds-cc-base.liquid`, 12:24:15): Liquid block reorder after the hero in `ds-cc-base.liquid`. Sub-cat filter chips (`<nav class="ds-cc__filter-bar">`) + their `_filter_tiles` assign moved ABOVE the 30+brands band + intro text; the Skip-by-sector bar (`<nav class="ds-cc__skip-bar">`) moved BELOW the intro. Tile grid prep assigns stay co-located with the tile grid below. No markup, class names, or schema changes — only block order.
- **Single-file impact**: all 12 BBI collection templates use this one section (`collection.{accessories, base, boardroom, business-furniture, category, desks, ergonomic-products, panels-room-dividers, quiet-spaces, seating, storage, tables}.json`) — every BBI collection page flipped on a single push.
- **New order**: hero → sub-cat pills → 30+brands band → intro text → Shop-by-sector pills → tile grid. Buyer's first decision (product subtype) above brand decision (sector) — conversion-flow improvement per Steve's spec.
- **Render verification**: cache-busted headless fetch on 3 collections (seating, desks, ergonomic-products) all confirmed new DOM order.

### Phase 4 — Speed optimization
- **A. AVADA-LOGO-CLEANUP → NO-OP** (already gone). Audit found zero `New_OC_BBI_Logo-raster_x320.png` refs in `theme/`, `config/`, `settings_data.json`, or any rendered HTML. Likely self-resolved during FAVICON-1 + SEO-AUDIT-1 work. Logged closed for the backlog.
- **B. EDU-HERO-FETCHPRIORITY (extended)** (Round 1, 20 files, 12:30:51): added `fetchpriority: 'high'` to every `ds-lp-*` hero `image_tag` that uses `loading: 'eager'`. Files: ds-lp-{about, brands, brands-ergocentric, brands-global-teknion, brands-heartwood, brands-keilhauer, brands-obusforme, brands-otg, delivery, design-services, education, government, healthcare, industries, non-profit, oecm, our-work (photo_1 only — photo_2 left as secondary), professional-services, quote, relocation}. Single attribute insertion per file, no other changes.
- **B-extended** (Round 2, `ds-cc-base.liquid:631`, 12:38:46): same `fetchpriority: 'high'` attribute added to the collection page hero `image_tag` after a Lighthouse diagnostic on `/collections/seating` (first reading showed an outlier 1883ms LCP that turned out to be measurement variance — re-run gave 997ms — but the collection hero genuinely lacked fetchpriority and warranted the surgical add for architectural consistency with ds-lp-* heroes). All 12 BBI collection page heroes now have the hint.
- **C. HOMEPAGE-HERO-WIDTH (?width=1200 step-down)** → DEFERRED per spec. Homepage LCP already passing CWV (~1317ms in post-Phase-4 measurement) with `?width=1920` from the morning width-opt fix. Don't trade desktop quality for a passing metric.

### Lighthouse — desktop, on `www.brantbusinessinteriors.com`
| Page | Morning post-IMG-4 | Post-STEVE | Δ |
|---|---|---|---|
| `/` | Perf 89 · LCP 1908ms | Perf 96 · LCP 1317ms | +7 · −591ms |
| `/collections/desks` | ~Perf 85–90 · ~1400ms | Perf 97 · LCP 1030ms | +~10 · −~370ms |
| `/collections/seating` | ~Perf 85–90 · ~1400ms | Perf 98 · LCP 1041ms | +~10 · −~360ms |
| `/collections/ergonomic-products` | n/a | Perf 95 · LCP 1330ms | — |
| `/collections/boardroom` | n/a | Perf 95 · LCP 1454ms | — |
| `/collections/storage` | n/a | Perf 78 · LCP 2187ms¹ | — |
| `/pages/education` | Perf ~85–89 · LCP 1735–2124ms | Perf 96 · LCP 1270ms | +~10 · −~600ms |
| `/products/dual-monitor-arm` | n/a | Perf 94 · LCP 1478ms | — |
¹ Storage outlier was cold-cache origin response (`server-response-time: 558ms`, `network-server-latency: 1067ms`) — not fetchpriority-fixable; will warm with traffic.

All Core Web Vitals targets met across the board (`LCP < 2.5s`, `CLS < 0.1` on every measured surface). Best Practices held at 0.73 throughout. Education page is the Phase-4 fetchpriority win (−600ms LCP). Collection page LCPs were already in the ≤1000ms range pre-Phase-4-B-extended, so additional fetchpriority gain was within measurement variance — architectural correctness, not a measurable performance jump.

### Safety
- **LIVE 186373570873 `updated_at` trail (full session)**: `2026-05-27T10:15:48` (baseline, post-morning-image-swaps) → `11:03:42` (Phase 1 base CSS) → `11:15:37` (Phase 1 extended — 33 files in single PUT cycle) → `11:23:29` (Phase 2 PDP price) → `12:24:15` (Phase 3 collection reorder) → `12:30:51` (Phase 4 — 20 ds-lp-* fetchpriority) → `12:38:46` (Phase 4 extended — ds-cc-base fetchpriority). Monotonic, no unauthorized writes.
- **Theme-check baseline**: held at `2852/166` EXACTLY across all 7 production write rounds. Zero new offenses introduced.
- **Pre-write backups**: 5 task-slug backup dirs under `data/backups/`:
  - `steve-1-buttons-pre-20260527-105048/` (base CSS pre-state)
  - `steve-1-buttons-extended-pre-20260527-111424/` (33 files pre-state)
  - `steve-2-pdp-pricing-pre-20260527-112310/` (PDP pricing pre-state)
  - `steve-3-collection-layout-pre-20260527-122341/` (collection reorder pre-state)
  - `steve-opt-b-fetchpriority-pre-20260527-123029/` (20 ds-lp-* pre-state)
  - `steve-opt-b2-cchero-fetchpriority-pre-20260527-123837/` (ds-cc-base pre-state)
- **All 35 unique theme files verified byte-match LIVE == local** at end of each phase. Cache-busted headless render + cache-busted preview-theme-id fetch confirmed customer-facing render on 8+ pages. Steve's 4 real-device sign-offs (`steve-1 good`, `steve-2 good`, `steve-3 good`, `steve-opt good`) cleared each phase before proceeding.

### Files touched (theme/)
35 unique files — `assets/bbi-homepage.css` (1) + 33 `sections/*.liquid` (ds-article, ds-blog-list, ds-cart-base, ds-cc-base, ds-collection-base, ds-cs-base, ds-lp-{about, brands, brands-ergocentric, brands-global-teknion, brands-heartwood, brands-keilhauer, brands-obusforme, brands-otg, contact, customer-stories, delivery, design-services, education, faq, government, healthcare, industries, non-profit, oecm, our-work, professional-services, quote, relocation}, ds-pdp-base, ds-search-results, ds-system-404) + 1 `snippets/bbi-nav.liquid`. ds-cc-base was edited in 3 separate rounds (Phase 1 vars, Phase 3 reorder, Phase 4 fetchpriority); ds-pdp-base in 2 rounds (Phase 1 vars, Phase 2 price). All other files edited in 1 round each.

### POST-LAUNCH BACKLOG additions
- **DEAD-LOGO-PNG (closed)** — the `New_OC_BBI_Logo-raster_x320.png` Avada-era reference flagged in the morning audit is gone from theme, config, and rendered HTML. Likely self-resolved during FAVICON-1 / SEO-AUDIT-1 work yesterday. No action.
- **HP-OECM-TINT-AUDIT (still open)** — pink `#FBECEC` accents at `bbi-homepage.css:588` (`.bbi-hp-ph--avatar`) and `:658` (`.hp-case__year`) are out of scope for STEVE-* changes; verify visually after the OECM strip hotfix landed yesterday.
- **STORAGE-COLLECTION-COLD-CACHE** — `/collections/storage` measured 1067ms `network-server-latency` on one Lighthouse run, suggesting an origin cold-cache path; monitor over next few days as edge cache warms. If it persists post-traffic warm-up, look at whether storage has unusual section block content or a heavy first-render hit.
- **DS-CS-BASE-THUMBNAIL-EAGER** — `ds-cs-base.liquid:326` hero image_tag uses `loading: 'eager'` at `width: 360` (a small thumbnail, not the LCP). Not a fetchpriority candidate; consider switching to `loading: 'lazy'` for a marginal byte saving if/when the page surface is touched again.

### Branch
`feature/steve-priority-changes-2026-05-27` (off `feature/morning-image-swaps-2026-05-27 @ cfe918f`).

---

## 🖼️ MORNING-IMAGE-SWAPS-2026-05-27 ✅ 2026-05-27 morning (Day 13)

4 hero images replaced on LIVE `186373570873` between 08:35 and 10:13 EDT. Each swap surfaced a mapping halt (sitewide refs + new-source compatibility flags) and a real-device check halt. All approvals via exact-match phrases ("fire image-N sitewide ...", "image-N good"). 9 references swapped across 8 templates. Source files canvas-expanded (image 1, 2, 4) or content-aware cropped (image 3) to match slot aspect ratios.

### Image 1 — SEATING collection hero
- **Source:** `DBE_6942-8_ML48_VU26_Side.jpg` (mesh-back chair side profile, 3600×3600 square)
- **Canvas-expanded:** 6400×3600 (16:9) with white L+R padding; uploaded as `bbi-coll-img-seating-hero-v5.jpg`
- **Refs swapped (2):** `templates/collection.seating.json:172` (collection hero) + `templates/index.json:42` (homepage "Shop the catalog" tile, inside bbi-shop custom_liquid)
- **Push receipt:** `2026-05-27T08:37:23-04:00`

### Image 2 — ERGONOMIC collection hero
- **Source picked:** OCI Platinum monitor arms image[1] (1024×1024 AI-generated studio shot) — Leo paused mid-halt to verify resolution headroom; original /products/dual-monitor-arm pdp-2 was 669×669 master (too soft for retina mobile at 0.47× DPR coverage). Surfaced 8 collection alternatives with 1024×1024 masters, OCI-1 chosen.
- **Canvas-expanded:** 1820×1024 (16:9) with white L+R padding; uploaded as `bbi-coll-img-ergonomic-products-hero-v5.jpg`
- **Refs swapped (1):** `templates/collection.ergonomic-products.json:124` (collection hero)
- **Push receipt:** `2026-05-27T08:51:18-04:00`

### Image 3 — EDUCATION pages (5 sitewide refs)
- **Source:** `165387 - Artcobell - product grouping with intrepid.jpg` (active-learning classroom with Artcobell Intrepid kidney tables + teal accent chairs, 2705×3500 portrait)
- **Strategy decision (Leo intervention mid-halt):** Canvas-expansion would create too much white margin around content-rich classroom scene. Instead, content-aware landscape crop to 16:10 (2705×1691) via centered crop. Trades off TV/BELIEVE art (acceptable per Leo) to preserve full table + chair composition.
- **4 candidates surfaced** (A=center, B=north, C=mid-upper, D=lower). Leo chose A.
- **Uploaded as:** `bbi-page-img-education-artcobell-v1.jpg`
- **Refs swapped (5):** `templates/page.education.json:9` (hero) + `templates/page.industries.json:11+14` (trust photo 2 + Education tile) + `templates/page.oecm.json:116` (trust photo 2) + `templates/page.our-work.json:18` (photo 12). Both `OCI-Education-1.jpg` and hash variant `OCI-Education-1_643da778-...jpg` redirected to the new file.
- **Push receipt:** `2026-05-27T09:22:41-04:00`
- **Pre-existing A11Y issue surfaced (not introduced):** `ds-lp-oecm.liquid:515` has hardcoded alt "Brantford General waiting area OECM install" on trust_image_2 — was misaligned before our swap, now more visible. Logged as follow-up.

### Image 4 — HOMEPAGE main hero
- **Source:** `hero.jpg` extracted from `~/Downloads/main page.zip` (professional at sit-stand desk with laptop + coffee, teal accent chairs, bamboo, modular shelving, 2308×1362 ~16:11)
- **Slot geometry:** Desktop 16:11, Mobile 4:3. Source 1.69:1 cover-crops L+R cleanly on both; subject (woman+desk) horizontally centered survives both crops.
- **Edits:** src + alt + width + height all updated. Alt = "Professional at sit-stand desk with laptop and coffee, teal accent chairs and bamboo plant — modern Canadian workspace by Brant Business Interiors". Caption "BBI PROJECT · PETERBOROUGH, ON" preserved (per Leo decision).
- **Uploaded as:** `bbi-homepage-hero-2026-05-27.jpg`
- **Push receipt:** `2026-05-27T09:54:03-04:00` (initial)
- **og:image:** unchanged — homepage still uses `og-preview.png` (1024×1024) per FAVICON-1 + SEO-AUDIT-1 wiring. Social shares unaffected.

### Lighthouse spot-check + width=1920 optimization
After image 3 Leo requested mid-flight Lighthouse on 4 swap surfaces before image 4. All 4 measured Perf 85-90, LCP 1735-2124 ms, CLS ≤ 0.028 — well within Core Web Vitals targets. LCP element on `/pages/education` confirmed as the new Artcobell hero with `loading=eager` but missing `fetchpriority=high` (logged as separate follow-up). Day-over-day variance from yesterday's anomalously-low TBW 549KB baseline explained by Lighthouse measurement window differences, not image-swap regression.

Post-IMG-4 Lighthouse triggered Leo's >5pt regression threshold (homepage Perf 99→85, LCP 781→2344 ms). Root cause: new hero delivered at 645 KB master URL vs old 271 KB. Leo authorized `?width=1920` URL parameter optimization (Shopify CDN auto-resize: 645→471 KB delivered). Re-PUT at 10:13:21 brought LCP to 1908 ms / Perf 89. CWV still passing; gap to yesterday is split between measurement variance + real ~200 KB byte delta.

### LIVE regression detected + fix
Between IMG-4 initial PUT (09:54:03) and the width-opt PUT (10:13:21), a 09:57:27 LIVE update reverted the IMG-1 homepage tile from `bbi-coll-img-seating-hero-v5.jpg` back to v4. Forensic dig: surgical single-field revert (6-line diff, only the seating tile URL inside `bbi-shop` section's custom_liquid). All 6 other IMG-1/2/3 writes byte-intact. No webhooks attribution available, no Plus audit logs. Leo confirmed Theme-Editor save of the `bbi-shop` section with stale-cached pre-IMG-1 state. v5 tile re-applied in the same PUT as the width=1920 optimization.

### Theme-Editor stale-cache pattern — 4 drifts surfaced + reconciled
Across the morning, LIVE `updated_at` drifted 4 times due to Leo's Theme-Editor verification opens (all confirmed by Leo, all timestamp-only except the IMG-1 tile revert):
- 08:40:10 — `collection.seating.json` + `index.json` bumped (timestamp-only, bytes match IMG-1 work)
- 08:52:03 — `collection.ergonomic-products.json` bumped (timestamp-only, bytes match IMG-2 work)
- 09:25:11 — all 4 IMG-3 templates bumped (timestamp-only)
- 09:57:27 — `index.json` bbi-shop seating-tile reverted v5→v4 (SUBSTANTIVE — re-fixed at 10:13:21)

### Safety
- **LIVE 186373570873 `updated_at` trail (morning):** 2026-05-26T20:33:23 (post-PRODUCTION-HOTFIX-1 baseline) → 08:37:23 (IMG-1) → 08:40:10 (Editor save) → 08:51:18 (IMG-2) → 08:52:03 (Editor save) → 09:22:41 (IMG-3) → 09:25:11 (Editor save) → 09:54:03 (IMG-4) → 09:57:27 (Editor regression) → 10:13:21 (IMG-1 tile re-fix + width=1920 opt). Monotonic, no unauthorized writes.
- **Theme-check baseline:** held at 2852/166 throughout (3 fewer offenses than 2855 baseline — same JSON re-escaping artifact pattern from earlier launch sessions).
- **Pre-write backups:** 4 task-slug backup dirs under `data/backups/image-swap-{seating,ergonomic,education,homepage}-pre-2026-05-27*/` — each contains LIVE + edited + local snapshots + the displaced source image for rollback.
- **/collections/seating page hero, /collections/ergonomic-products page hero, /pages/education, /pages/industries (trust + tile), /pages/oecm trust band, /pages/our-work photo 12, homepage hp-hero, homepage hp-shop seating tile:** all 9 references verified as new images via Admin API byte-match + headless render fetch at the close of each phase. All confirmed real-device by Leo ("image-1 good", "image-2 good", "image-3 good", "image-4 good").

### Files touched (theme/)
- `templates/collection.seating.json` — v4 → v5 hero (1 line)
- `templates/collection.ergonomic-products.json` — v4 → v5 hero (1 line)
- `templates/index.json` — hp-hero src + alt + width + height swap; hp-shop seating tile v4 → v5; hero src `?width=1920` appended (1 line, multiple changes)
- `templates/page.education.json` — hero_image swap (1 line)
- `templates/page.industries.json` — trust_image_2 + tile_image_2 swap (2 lines)
- `templates/page.oecm.json` — trust_image_2 swap (1 line)
- `templates/page.our-work.json` — photo_12 swap (1 line)

### Files added to Shopify Files (4 new assets, 4 old assets preserved for rollback)
- `bbi-coll-img-seating-hero-v5.jpg` (6400×3600, 526 KB master)
- `bbi-coll-img-ergonomic-products-hero-v5.jpg` (1820×1024, 89 KB)
- `bbi-page-img-education-artcobell-v1.jpg` (2705×1691, 595 KB)
- `bbi-homepage-hero-2026-05-27.jpg` (2308×1362, 944 KB)
- Old assets preserved in Files: `bbi-coll-img-seating-hero-v4.jpg`, `bbi-coll-img-ergonomic-products-hero-v4.jpg`, `OCI-Education-1.jpg`, `OCI-Education-1_643da778-93eb-45ab-8a69-8f274a3ceba3.jpg`, `hp-hero-office-breakout.jpg`

### POST-LAUNCH BACKLOG additions
- **HP-SHOP-TILES-REFACTOR** — homepage "Shop the catalog" tile URLs are inlined as raw HTML inside the `bbi-shop` section's `custom_liquid` setting. This makes them vulnerable to Theme-Editor stale-cache reverts (proven during this session). Refactor to a proper Liquid section that uses `image_url` filter calls or `image_picker` section settings, so the URLs are managed structurally rather than as raw text.
- **LCP-FETCHPRIORITY-EDU** — `theme/sections/ds-lp-education.liquid:378` renders hero via `image_tag` filter but doesn't include `fetchpriority: 'high'`. Single-attribute add would shave 100-300 ms off `/pages/education` LCP.
- **DS-LP-OECM-ALT-FIX** — `theme/sections/ds-lp-oecm.liquid:515` has hardcoded alt "Brantford General waiting area OECM install" on `trust_image_2`. This was misaligned before today's Education-photo swap (the prior `OCI-Education-1_643da778-...jpg` was already a classroom photo), but our swap makes the mismatch more visible. Replace with a setting-driven alt, or fix to "Active-learning classroom — Artcobell installation" to match the new content.
- **DEAD-LOGO-PNG** — `New_OC_BBI_Logo-raster_x320.png` (187 KB) was surfaced in the Lighthouse top-10 byte-heavy resources on `/pages/education`. Avada-era stale asset still loading somewhere in the page. Find + remove the reference.

### Branch
`feature/morning-image-swaps-2026-05-27` (off `feature/launch-chain-2026-05-26 @ e8212b2`).

---

## 🔓 Day 12 evening — 2026-05-26

- **DATAFORSEO-MCP-UNBLOCK ✅** — DataForSEO MCP HTTP 403 resolved; SEO-AUDIT-1 hard gate now ready to run tomorrow as Step 5 of the launch path.
- **SEO-AUDIT-1 ✅** — pre-launch SEO hard gate passed (see entry below). LAUNCH-0 cleared.
- **LAUNCH-0/1/2 ✅** — BBI theme published to LIVE (see LAUNCH-CHAIN entry below). Avada demoted to `unpublished`. brantbusinessinteriors.com now serving BBI.
- **PRODUCTION-HOTFIX-1 ✅** — 4 production bugs caught + fixed post-publish in the same chain (search-icon strikethrough, PDP CTA black-on-black, OECM strip pink→ink, defensive logo asset).
- **LAUNCH-3 ✅** — GSC sitemap re-submitted + GA4 Realtime traffic confirmed (commit `ea98842`).
- **LAUNCH-4 ✅** — multi-browser smoke 30/30 functional pass on Chromium + WebKit (5 URLs × 6 viewports) + Leo manual browser test passed + 24h monitor playbook saved to `docs/plan/launch-4-24h-monitor-2026-05-26.md`. Launch chain closed.

---

## 🚀 LAUNCH-0/1/2 + PRODUCTION-HOTFIX-1 ✅ 2026-05-26 evening (Day 12+, post-SEO-AUDIT-1)

LAUNCH chain v3 executed end-to-end: 6 LAUNCH-0 phases (pre-flight, automated mobile breakpoint tests, Lighthouse baseline, LIVE backup, DEV verification, smoke render) → Halt 0.M phone test → Halt 1 publish gate (`fire launch-1` from Leo) → LAUNCH-1 publish (irreversible PUT role:main) → Halt 2 → LAUNCH-2 smoke + Lighthouse on LIVE + DEV/LIVE delta → Halt 3 → 4 production hotfixes (1 pre-publish search-icon fix from Halt 0.M, 3 post-publish hotfixes from Halt 3 pause) → final verification.

### LAUNCH-1 publish receipt
- **PUT** `/admin/api/2026-04/themes/186373570873.json` body `{"theme": {"role": "main"}}` → HTTP 200.
- **New LIVE:** theme `186373570873` (BBI Landing Dev → main), `updated_at` `2026-05-26T20:08:47-04:00`.
- **Old LIVE:** theme `178274435385` (Avada) demoted to `role: "unpublished"` — retrievable + fully backed up to `data/backups/live-theme-pre-launch-20260526-193241/` (350 assets + MANIFEST.md restore instructions).
- **LIVE baseline broken (by design):** was `2026-05-16T16:47:22-04:00` (held 10 days through 16 build sessions).

### LAUNCH-0 verification matrix (read-only)
- **Phase 0.A pre-flight:** DEV `186373570873` unpublished + LIVE `178274435385` main both confirmed via Admin API.
- **Phase 0.B mobile breakpoint tests:** Playwright at 5 viewports × 4 pages = 20 combos. **13/20 strict pass**; 7 fails categorized as known/non-blocking: 4× iPad Mini Landscape 1024×768 docOverflow 258–312px (known MID-DESKTOP-OVERFLOW already in POST-LAUNCH BACKLOG from NAV-REDESIGN-1), 3× OECM coverage table 640px (scrolls inside wrapper — page docOverflow=0, standard B2B spec-table pattern). Tap-target outliers were 1× inline body text-link (not the primary CTA) + iPad-L desktop-context elements where 44px HIG doesn't apply.
- **Phase 0.C DEV Lighthouse baseline:** desktop Lighthouse via DataForSEO MCP on homepage / oecm / seating. **Important caveat:** the MCP follows the apex→www 301 redirect and strips the `preview_theme_id` param, so the "DEV baseline" actually measured pre-publish LIVE (Avada). This same constraint affected SEO-AUDIT-1 earlier today. Pre-publish Avada scores: homepage Perf 97 / oecm 91 / seating 92 (all A11Y 92 / BP 73 / SEO 100). Mobile Lighthouse not available via this MCP — WAIVED to manual PSI post-launch.
- **Phase 0.D LIVE backup:** 350/350 assets downloaded to `data/backups/live-theme-pre-launch-20260526-193241/` with MANIFEST.md (per-file size + restore command). Spot-check 5/5 byte-match.
- **Phase 0.E DEV verification:** 9 spot-check assets across 10 feature branches (SEO-AUDIT-1, LEAD-HIGH-2, STALE-OECM-DATE-FIX-1, FAVICON-1, NAV-REDESIGN-1, HOMEPAGE-SHOP-FURNITURE-HOVER-1, HOMEPAGE-TILE-BORDER-MATCH-1, KEILHAUER-PHOTO-SWAP-1, og-preview.png) all present with correct timestamps. `shopify theme check`: **166 / 2855 — exact PRE-LAUNCH-AUDIT-1 baseline match**.
- **Phase 0.F smoke render:** 5 DEV pages (/, /pages/about, /pages/oecm, /collections/seating, /pages/quote) all HTTP 200, BBI header rendering, no Liquid errors, content markers present (the `bbi-card` marker absent on `/collections/seating` is expected — that collection uses default Avada `templates/collection.json`, not a BBI-specific template).

### Halt 0.M (real-device phone test) — caught **1 production bug pre-publish**
Leo flagged: "search bar magnifying-glass icon has a visible strikethrough line through it on DEV preview". Empirical diagnosis (Playwright Chromium + WebKit at 4 viewports × DPR 2–3) showed CSS chain clean (zero `text-decoration: line-through`), no pseudo-element overlays, no LEAD-HIGH-2 button→anchor regression. **Actual root cause: SVG path geometry** — magnifying-glass handle `path d="M11.25 11.25L15.75 15.75"` started essentially ON the lens edge `(11.21, 11.21)` in the 45° direction; `stroke-linecap="round"` extended the cap 0.875 units backward into the lens, creating ~1.5 device-pixel overlap that read as "line cutting through the icon" at iPhone Retina 3× DPR. Latent geometry issue, not a recent regression.

**Fix:** `theme/snippets/bbi-nav.liquid:606` + `:699` — `M11.25 11.25` → `M12 12` on both desktop and mobile search SVG icons. New start point is 1.11 units outside lens edge; round cap end lands 0.24 units outside lens = clean visual gap. Push receipt: `2026-05-26T20:03:01-04:00` (pre-LAUNCH-1). Verified at 8 render contexts (Chromium + WebKit × iPhone-SE / Pixel-7 / iPad-Mini / desktop). Pre-write backup: `data/backups/search-icon-fix-pre-20260526-200249/bbi-nav.liquid`. Leo re-tested on phone after fix — confirmed "mobile good".

### LAUNCH-2 verification (post-publish on `brantbusinessinteriors.com`)
- **5 LIVE URLs smoke test:** HTTP 200, zero Avada leakage (`primary-header-blocks` / `nav-menu-link` absent), JSON-LD present on all 5, no Liquid errors.
- **LEAD-HIGH-2 anchor fallback:** 2× `<a class="bbi-btn--primary" href="/pages/quote">` on homepage; `/pages/quote` HTTP 200. ✓
- **Redirects:** `/pages/ergocentric` → 301 → `/pages/brands-ergocentric` ✓; `/pages/how-to-adjust-my-new-chair` → 301 → `/pages/brands-ergocentric` ✓.
- **Favicon CDN (6 assets):** all HEAD → HTTP 200 with correct Content-Types (favicon.svg image/svg+xml, favicon-32/16.png, apple-touch-icon.png image/png, site.webmanifest application/octet-stream, og-preview.png image/png).
- **og:image:** homepage `<meta property="og:image">` points to `og-preview.png` (FAVICON-1 + SEO-AUDIT-1 wiring intact). ✓
- **LIVE Lighthouse:** homepage Perf 99 / A11Y 88 / BP 96 / SEO 80 (raw), LCP 781ms, TBW 547KB · oecm Perf 96 / A11Y 88 / BP 96 / SEO 80, LCP 729ms, TBW 582KB · seating Perf 99 / A11Y 88 / BP 96 / SEO 80, LCP 738ms, TBW 549KB.

### Pre-publish (Avada) vs post-publish (BBI) Lighthouse delta
Important framing: the Phase 0.C "DEV baseline" was actually Avada (preview_theme_id stripped). The pre/post comparison below is therefore old-Avada → new-BBI on the same 3 URLs — more informative than the chain's intended DEV→LIVE production-parity check.

| Metric | Homepage Avada→BBI | OECM Avada→BBI | Seating Avada→BBI |
|---|---|---|---|
| Performance | 97 → 99 (+2) | 91 → 96 (+5) | 92 → 99 (+7) |
| A11Y | 92 → 88 (-4) | 92 → 88 (-4) | 92 → 88 (-4) |
| Best Practices | 73 → 96 (**+23**) | 73 → 96 (**+23**) | 73 → 96 (**+23**) |
| SEO (raw) | 100 → 80 (-20) | 100 → 80 (-20) | 100 → 80 (-20) |
| LCP | 890ms → 781ms (-109) | 1538ms → 729ms (-809) | 1396ms → 738ms (-658) |
| Total byte weight | 3.04MB → 534KB (**-83%**) | 3.04MB → 568KB (-81%) | 3.03MB → 536KB (-82%) |

**SEO -20 is a Lighthouse measurement artifact, NOT a real regression.** DataForSEO's HeadlessChrome bot hits the apex domain → Shopify 301 → www. Lighthouse's `http-status-code` audit registered `displayValue=403` mid-chain (likely Cloudflare bot protection on apex), which knocked both `http-status-code` AND `meta-description` audits to `score=None` and dropped the SEO category by 20 points. **Real SEO state is 100** — verified via curl with Safari UA: `<title>Office Furniture for Canadian Businesses | Brant Business Interiors</title>` + `<meta name="description" content="Commercial office furniture for Ontario businesses, schools, and institutions. Global Furniture Group, OTG / Offices to Go, Heartwood Manufacturing. OECM Supplier Partner (Agreement 2025-470). Quote in 1 business day.">` + og:image referencing og-preview.png all present and correct.

**A11Y -4** is already covered in POST-LAUNCH BACKLOG (PDP-A11Y-1 — variant picker form-labels / button-name attrs). Not a launch blocker.

### Halt 3 pause — 3 additional production bugs caught + fixed
After LAUNCH-2 verification passed, Leo's manual phone testing surfaced 3 more issues that automated smoke tests didn't catch. Bundled diagnosis + fix:

1. **PRODUCTION-HOTFIX BUG #1 — defensive logo upload.** Leo reported header logo rendering as broken-image icon on his phone. Empirical Chromium + WebKit testing at 4 viewports could NOT reproduce — every test combo loaded the logo correctly from `cdn/shop/files/bbi-logo-v2_aa647658-...png` (HTTP 200 PNG for old iOS Safari UAs, AVIF for modern iOS Safari UAs — Shopify format negotiation working correctly). Suspected cause: stale browser cache on Leo's phone from pre-launch Avada-era visit. **Defensive fix: uploaded `theme/assets/bbi-logo-v2.png`** (1360×400 master, 445,988B) to LIVE 186373570873 via Admin API. The Liquid template at `bbi-nav.liquid:491` + `:677` has a fallback `<img src="{{ 'bbi-logo-v2.png' | asset_url }}">` for when `section.settings.logo` is blank; the asset was previously MISSING from LIVE (verified via Admin API 404) — fallback would have 404'd if ever triggered. Now the fallback works. Push receipt: `2026-05-26T20:32:42-04:00`. Byte-match verified.

2. **PRODUCTION-HOTFIX BUG #2 — PDP CTA black-on-black.** "Request a Quote" CTA at bottom of every PDP (`.pdp-cta-closer__btn`) rendered with `color: rgb(11,11,12)` (Avada `--textColor` black) on `bg: rgb(11,11,12)` (BBI `--buttonBackground` black) — **black text on black background**, invisible. Empirical computed-style inspection on LIVE PDP confirmed. Root cause: LEAD-HIGH-2's `<button>` → `<a>` conversion meant the anchor now inherited from Avada's site-wide `a { color: var(--textColor); }` cascade rules. The `ds-pdp-base.liquid:287` inline `<style>` had `color: #ffffff` but bare class selector `.pdp-cta-closer__btn` (specificity `0,0,1,0`) lost to Avada's `body .template-product a` (`0,0,1,1`) in the cascade. The other 7 LEAD-HIGH-2 anchor conversions (`.bbi-btn--primary` on header/collection/design + `.bbi-mobile-nav__quote` + `.blog-cta__btn` + `.s404-btn--primary` + `.pdp-btn--quote-outline`) were verified non-broken — they use higher-specificity rules or shielded base classes. **Fix:** `ds-pdp-base.liquid:287` + `:288` — `.pdp-cta-closer__btn` → `a.pdp-cta-closer__btn` (specificity gains 1 type-selector → `0,0,1,1`, ties Avada cascade and wins on source-order since inline `<style>` loads after `theme/assets/*.css`). Push receipt: `2026-05-26T20:33:02-04:00`. Verified Chromium + WebKit × iPhone-SE + desktop (4/4 combos): `color: rgb(255,255,255)` on `bg: rgb(11,11,12)` — white text on black, fully legible.

3. **PRODUCTION-HOTFIX BUG #3 — OECM strip pink→ink.** Homepage `section.hp-oecm` rendered with `bg: rgb(251,236,236)` = `#FBECEC` (pale pink, off-canonical-palette). Source: `bbi-homepage.css:646` `.hp-oecm { background: #FBECEC; } /* --bbi-accent-tint */`. Affected page: homepage only (the `hp-oecm` markup is a `custom_liquid` block in `templates/index.json`; other OECM trust elements `.bbi-oecm-bar` / `.lp-oecm-callout` / `.lp-trust-row__cell` use different patterns and were already on-brand). **Fix:** `bbi-homepage.css:645-647` — 3-line block replaced with 5-line block: `.hp-oecm { background: #0B0B0C; border-top-color: #0B0B0C; border-bottom-color: #0B0B0C; }` + `.hp-oecm__copy { color: #FAF8F5; opacity: 0.85; }` + `.hp-oecm .bbi-badge--oecm { color: #FAF8F5; border-color: rgba(250,248,245,0.6); }` + `.hp-oecm .bbi-btn--tertiary { color: #FAF8F5; }`. The red dot inside `.bbi-badge--oecm .dot` already uses `var(--saleBadgeBackground)` = `#D4252A` (canonical brand red — same as footer maple leaf, favicon divider) — unchanged. Push receipt: `2026-05-26T20:33:23-04:00`. Verified Chromium (after ~20s CDN cache propagation) + WebKit: `bg rgb(11,11,12)` + copy/badge/link `rgb(250,248,245)` + dot `rgb(212,37,42)`. Two other `#FBECEC` usages elsewhere in `bbi-homepage.css` (`.bbi-hp-ph--avatar:588`, `.hp-case__year:658`) are tiny accent-pills that remain on the pink-tint by design — out of scope for this hotfix.

### Safety
- **LIVE 186373570873 updated_at trail:** `20:08:47` (LAUNCH-1 publish) → `20:32:42` (Fix-1 logo PUT) → `20:33:02` (Fix-2 PDP CTA PUT) → `20:33:23` (Fix-3 OECM strip PUT). Monotonic, no unexpected writes.
- **Avada 178274435385:** stayed `role: unpublished` throughout — no accidental re-publish.
- **`shopify theme check`:** **166 / 2855** — exact PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses introduced by any of the 4 fixes.
- **Pre-write backups:** `data/backups/search-icon-fix-pre-20260526-200249/bbi-nav.liquid` (pre-search-icon-fix) + `data/backups/launch-hotfixes-pre-20260526-203227/{ds-pdp-base.liquid, bbi-homepage.css}` (pre-PRODUCTION-HOTFIX-1).
- **Phone re-tests:** Leo confirmed "mobile good" after search-icon fix (pre-publish) AND "production good" after the 3 post-publish hotfixes (logo + PDP CTA + OECM strip).

### Working dir artifacts
- `data/working/launch-chain-2026-05-26/mobile-viewport-tests.json` — Phase 0.B raw test matrix (20 combos)
- `data/working/launch-chain-2026-05-26/lighthouse-dev-baseline.json` — Phase 0.C Lighthouse (pre-publish; LIVE-Avada due to redirect strip)
- `data/working/launch-chain-2026-05-26/lighthouse-live-post.json` — LAUNCH-2 Lighthouse on LIVE (BBI)
- `data/working/launch-chain-2026-05-26/dev-vs-live-delta.json` — Avada→BBI metric delta
- `data/working/launch-chain-2026-05-26/launch-1-receipt.json` — LAUNCH-1 PUT receipt
- `data/working/launch-chain-2026-05-26/launch-2-smoke.json` — LAUNCH-2 smoke test results
- `data/working/launch-chain-2026-05-26/live-backup-summary.json` — LIVE backup integrity check
- `data/working/launch-chain-2026-05-26/diagnose-search-icon.json` + screenshots — Halt 0.M diagnostic
- `data/working/launch-chain-2026-05-26/diagnose-pdp-cta.json` + screenshots — Halt 3 PDP CTA diagnostic
- `data/working/launch-chain-2026-05-26/diagnose-logo.json` — Halt 3 logo diagnostic (could not reproduce empirically)
- Verification screenshots: `after-fix2-pdp-cta-{chromium,webkit}-{iphone-se,desktop}.png`, `after-fix3-oecm-{chromium,webkit}.png`

### POST-LAUNCH BACKLOG additions
- **PDP-PERF-1** — already logged from SEO-AUDIT-1; now also relevant for the PDP A11Y -4 from Lighthouse on LIVE.
- **MOBILE-LIGHTHOUSE-MANUAL** — DataForSEO MCP only supports desktop Lighthouse. Run mobile Lighthouse manually via PageSpeed Insights post-launch and log scores into the build-state.
- **APEX-DOMAIN-BOT-403** — Cloudflare bot protection on `brantbusinessinteriors.com` (apex) returns 403 to HeadlessChrome UA mid-redirect to `www.`, which knocks Lighthouse SEO scores by 20 points despite the actual page serving 200 with full meta. Investigate whether to relax Cloudflare bot rules for Lighthouse bots OR document the artifact in performance reports.
- **SEARCH-ICON-WEBKIT-APPEARANCE** — `<input type="search">` has `webkit-appearance: auto` with `::-webkit-search-cancel-button { display: block }`. iOS Safari renders a native "X" clear button inside the input once user types — out of scope for this hotfix but worth tightening to fully-custom-styled input post-launch.
- **HP-OECM-TINT-AUDIT** — two remaining `#FBECEC` usages in `bbi-homepage.css` (`.bbi-hp-ph--avatar:588`, `.hp-case__year:658`) — verify they still look right on the homepage after the `.hp-oecm` swap; the case-study year pill especially since it sits in a different visual context now.
- **DEV-LIGHTHOUSE-COOKIE-SESSION** — DataForSEO MCP strips `preview_theme_id` during redirect. For future DEV-Lighthouse measurements, run Lighthouse locally via `npx lighthouse` or use a different MCP that can preserve cookies.
- **AVIS-OPTIONS-APP-NOISE** — third-party Shopify app **APO Product Options v1.7.163.31** (`avis-options` extension) throws `Cannot read properties of null (reading 'createDocumentFragment')` and 404s on `/products/undefined.js` + `/products/please-select-a-finish-1.js` on every PDP, across both Chromium and WebKit. Surfaced during LAUNCH-4 multi-browser smoke. Pre-existing app (was installed under Avada), not theme. Decision: keep / configure / uninstall.
- **24h monitor playbook** — first-24h tactical checklist saved at `docs/plan/launch-4-24h-monitor-2026-05-26.md` (cadence: every 2h / morning / afternoon / evening + red flags + rollback procedure). Complements the strategic horizon doc at `docs/plan/post-launch-monitoring.md`.

### Branch
`feature/launch-chain-2026-05-26` (off `feature/seo-audit-1 @ 72b4908`).

---

## 🌐 LAUNCH-4 ✅ 2026-05-26 evening (Day 12+, after LAUNCH-3)

Multi-browser smoke + 24h monitor playbook setup. Final step in the launch chain.

### Phase A — Multi-browser smoke (30 cells)

Playwright Chromium + WebKit running 5 URLs × 6 viewport+engine combos = **30 render checks**, all on LIVE `brantbusinessinteriors.com`. Critical render checks (HTTP 200, title sane, body >10kb, header logo with non-zero dimensions, footer present, Quote CTA visible, nav element appropriate to viewport width, computed-style spot checks for PDP CTA contrast + OECM strip background) **passed on all 30 cells**.

URLs tested: `/`, `/pages/oecm`, `/collections/seating`, `/products/boardroom-table-rectangular-94-5x47-25`, `/pages/quote`.

Engines × viewports:
- Chromium 1920×1080 / 1280×800 / 412×915 (Pixel 7 emulation, DPR 2.625, touch)
- WebKit 1920×1080 / 393×852 (iPhone 14 Pro emulation, DPR 3, touch, iOS Safari UA) / 768×1024 (iPad Mini emulation, DPR 2, touch)

**Fix-2 + Fix-3 regression verification across all PDP/homepage cells:**
- PDP CTA computed style: `color: rgb(255, 255, 255)` on `bg: rgb(11, 11, 12)` — Fix-2 holding ✓
- `.hp-oecm` computed background: `rgb(11, 11, 12)` — Fix-3 holding ✓

**Header logo:** 148×44 on most URLs, 121×36 on `/pages/quote` (reasonable for both — same asset, different surface).

### Noise identified (NOT theme regressions)

- **30/30 cells: `shop.app/pay/hop` CSP frame-block (403).** Shopify-injected iframe blocked by Shopify's own CSP. Universal across all Shopify stores; would be identical on Avada. Ignore.
- **6/30 PDP cells: third-party app errors.** APO Product Options v1.7.163.31 (`avis-options` extension) throws `Cannot read properties of null (reading 'createDocumentFragment')` + 404s on `/products/undefined.js` + `/products/please-select-a-finish-1.js`. Pre-existing app from Avada-era. Logged as **AVIS-OPTIONS-APP-NOISE** in POST-LAUNCH BACKLOG.
- **OECM page title** doesn't contain "Brant"/"BBI" but is intentional SEO copy (`OECM Office Furniture Supplier – Agreement 2025-470`, approved in SEO-AUDIT-1). Reclassified as PASS.

### Phase A artifacts

- `data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke.py` — 30-cell Playwright runner
- `data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.json` — full per-cell results
- `data/working/launch-chain-2026-05-26/launch-4-multibrowser/smoke-matrix.md` — human-readable matrix + footnotes
- `data/working/launch-chain-2026-05-26/launch-4-multibrowser/diag-errors.py` + `diag-errors.json` — drill-down identifying the 401/403/404/JS error sources

### Halt L4.1 — Leo manual browser test

Leo confirmed **"browser good"** after Phase A — Firefox/Chrome-Android spot-check passed for header logo, nav dropdown, Quote modal, PDP rendering, footer.

### Phase B — 24h monitor playbook

Created **`docs/plan/launch-4-24h-monitor-2026-05-26.md`** — tactical first-24h checklist (cadence: every 2h, morning, afternoon, evening) with red-flag thresholds, rollback procedure (Shopify Admin path + Admin API path), and a Section 5 pointer to Week 1 priorities. Complements (does not duplicate) the strategic horizon doc at `docs/plan/post-launch-monitoring.md` which already covered Hour 0–24 through Day 30+ at a higher level.

### Safety

- **Phase A is read-only** — Playwright headless against LIVE URLs only, no Admin API writes.
- **Phase B is documentation-only** — created one new markdown file under `docs/plan/`, edited only `BBI-Session-Kickoff/bbi-build-state.md` (this file). Zero theme writes; LIVE `updated_at` unchanged from Fix-3 timestamp `2026-05-26T20:33:23-04:00`.

### Branch
`feature/launch-chain-2026-05-26` — LAUNCH-4 closure commit pending.

---

## 🔍 SEO-AUDIT-1 ✅ 2026-05-26 evening (Day 12+, after STALE-OECM-DATE-FIX-1)

Pre-launch SEO hard gate. 39 bbi_landing URLs crawled via cookie-session DEV preview + DataForSEO `on_page_lighthouse` on top 5 templates. **Verdict: READY FOR LAUNCH-0.** 0 BLOCK · 15 FIX (all in-scope FIXes applied via Claude Code Admin API today — zero Steve work) · 3 WAIVE (logged for post-launch backlog). Report at `data/reports/seo-audit-1-2026-05-26.md`; copy-review log at `data/working/seo-audit-1-2026-05-26/halt-1.5-copy-review.md`; backup snapshot at `data/backups/seo-audit-1-fix-batch-pre-20260526-165131/` (35 pre-state metafield JSONs + 3 pre-state theme files).

- **Branch:** `feature/seo-audit-1` (off `feature/lead-high-2 @ f4f68ec`).
- **Scope probe outcome (Phase 7.0):** `write_content` ✓, `write_products` ✓, `metafieldsSet` on Shop owner ✓, redirect POST/DELETE ✓, page PUT ✓. `shopUpdate` GraphQL mutation removed from current Admin API; `PUT /shop.json` returns 406 → storefront-wide SEO **not directly writable**. Reframed FIX #3/#4 as theme-level override via `theme/snippets/meta-tags.liquid` (renders before `{{ content_for_header }}`, so our tags win over Shopify's stale defaults).

**Theme edits (2 files):**
1. `theme/snippets/meta-tags.liquid` — conditional og:title for homepage (`'Office Furniture for Canadian Businesses | Brant Business Interiors'`); replaces stale `shop.description` fallback with BBI-voice default (`'Commercial office furniture for Ontario businesses, schools, and institutions. ergoCentric, GFG, OTG, Heartwood, ObusForme. OECM Agreement 2025-470. Quote in 1 business day.'`); wires `og-preview.png` (uploaded by FAVICON-1 but never wired) as homepage og:image 1024×1024. Twitter tags mirror via existing `og_title`/`og_description` assigns.
2. `theme/layout/theme.liquid:30` — title-suffix logic broadened from `unless page_title contains shop.name` to `unless page_title contains 'Brant' or contains 'OECM' or contains shop.name`. Prevents the 40-char `– Office Central & Brant Business Interiors` auto-append from double-stuffing the new 50-60 char title_tags.

**Shopify Admin metafield writes (68 total — 62 first-pass + 6 retry after Shopify's 2-call/sec rate cap):**
- 33 `title_tag` writes — 17 pages + 10 collections + 1 blog hub + 1 article + 4 trims of existing oversized title_tags (contact, design-services, healthcare, industries)
- 29 `description_tag` writes — 17 pages + 10 collections + 1 blog hub + 1 article (cornerstone, replaces 324-char auto-desc)
- All retry-rate-limited writes succeeded on second attempt with 3-second backoff

**URL redirects (2) + page unpublish (2):**
- `/pages/ergocentric` → 301 → `/pages/brands-ergocentric` (verified live); source page unpublished. Resolves FIX #9 (phantom `brand-dealer` template suffix → H1=0 LEAK).
- `/pages/how-to-adjust-my-new-chair` → 301 → `/pages/brands-ergocentric` (verified live); source page unpublished. Resolves FIX #10 (generic `page` template → H1=0 LEAK). Visual-guide content migration to a future `ds-lp-howto-chair.liquid` logged as post-launch backlog.

**`data/llms-txt-draft.md` refreshed (FIX #1b):** 7 stale items addressed — Richmond Hill → 296 George St N Peterborough; added Agreement 2025-470 throughout; lead brands updated to GFG/OTG/Heartwood/ObusForme/ergoCentric (Keilhauer/Teknion now "on request"); broken `/pages/services` link split into `/pages/design-services` + `/pages/delivery` + `/pages/relocation`; added 6 brand sub-page URLs + brands hub + cornerstone article + customer-stories + our-work + contact + faq; entity framing updated to "Brant Basics is the OECM-registered entity"; date stamp 2026-04-30 → 2026-05-26. **FIX #1a (deployment path) WAIVED to post-launch backlog** — Shopify currently auto-generates `/llms.txt` with `pageType=llms_txt` (overrides AI-1's deployed `/pages/llms-txt` redirect from commit `a2118f3`); no `templates/llms.txt.liquid` override documented and no Admin toggle exists. Refreshed draft is ready as soon as Shopify ships a hook OR Leo opens a support ticket.

**Before / after metrics (39 URL DEV crawl):**

| Metric | Before | After |
|---|---:|---:|
| Pages with `<meta name=description>` | 13/39 | **39/39** |
| Pages with stale "BBI and Office Central specialize…" og:description | 29/39 | **0/39** |
| Pages with title_length 51-60 (target band) | 0/39 | **37/39** (only homepage 67 + PDP 108 outside; both intentional) |
| Pages with title_length >140 (severe SERP truncation) | 2/39 | **0/39** |
| Pages with H1=0 (LEAK pages) | 2 | **0** (both redirected, sources unpublished) |
| Meta-desc >160 chars (truncation risk) | 2 (quote 320, cornerstone 324) | **0** |
| Homepage og:image | `IMG_2566.jpg` (Avada legacy) | **`og-preview.png`** (BBI 1024×1024) |
| HTTP 200 on all audit URLs | 39/39 | 39/39 |
| JSON-LD parse errors sitewide | 0 | 0 |

**Lighthouse desktop (top 5 templates, DataForSEO MCP):** homepage Perf 94 / SEO 100; OECM 90 / 92; About 83 / 92; Seating 85 / 92; PDP (adapt-hb) 81 / 100. CWV pass on 4/5 (PDP LCP 2585ms, 85ms over target — marginal, **WAIVED** as image-weight optimization that touches every Hero PDP and would risk regressing SPEC-CANARY work). Mobile Lighthouse not available via this MCP — **WAIVED** to manual PSI run post-launch. PDP A11y 0.85 + sitewide Best Practices 0.73 also **WAIVED** post-launch.

**Schema surface confirmed:** Organization + LocalBusiness sitewide via `bbi-org-schema.liquid` + `bbi-localbusiness-schema.liquid` (SCHEMA-LOCALBIZ-1); WebSite + SearchAction sitewide; BreadcrumbList on 10 collections + PDP (AI-6); FAQPage on 14 pages (oecm 8 Q&A, faq 22, quote 5, design-services 5, delivery 7, relocation 6, all 10 collections incl. business-furniture 3-5 each); BlogPosting on cornerstone article (H-1 fix); Product + Brand + Offer on PDP (PDP-2 absorbs AI-3); GovernmentService on /pages/oecm (AI-8). Zero JSON-LD parse errors across all 39 URLs.

**robots.txt (AI-2) re-verified:** Shopify default with `User-agent: *  Allow: /` open to all major AI crawlers (GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Googlebot, Google-Extended). Sitemap pointer present. AI-2 audit from 2026-04-30 still valid.

**ds-article.liquid AEO foundation verified on live cornerstone post:** BlogPosting JSON-LD + datePublished + author + Q&A schema + 4 tables / 9 `scope="col"` / 3 `<caption>` rendered correctly.

**Safety:**
- LIVE theme `178274435385` `updated_at = 2026-05-16T16:47:22-04:00` verified 7× during audit (pre-Phase-0, pre-meta-tags push, post-meta-tags push, pre-theme.liquid push, post-theme.liquid push, post-metafield-batch, final post-write). LIVE untouched ✓.
- `shopify theme check`: 166 files / **2855 offenses** — **EXACT PRE-LAUNCH-AUDIT-1 baseline match**, zero new offenses introduced by theme edits.
- Day 12+ work integrity: FAVICON-1 5 link tags + `theme-color #FAF8F5` ✓ · NAV-REDESIGN-1 `var(--headerColor)` intact (bbi-nav.liquid not touched) ✓ · ABOUT-PAGE-GRID-1 6 `<figure>` 2×3 grid ✓ · STALE-OECM-DATE-FIX-1 11× "Agreement 2025-470" + 0× "since 2019" on /pages/about ✓ · LEAD-HIGH-2 bbi-quote-modal.liquid not touched ✓.

**POST-LAUNCH BACKLOG additions:**
- **FIX #1a — re-investigate llms.txt override path** — quarterly check on Shopify changelog for `templates/llms.txt.liquid` support OR open Shopify support ticket. Refreshed `data/llms-txt-draft.md` is ready to deploy.
- **PDP-PERF-1** — PDP byte-weight optimization (7.81 MB total transfer; avisplus.io reviews + Hero image weights). Defer because it touches every Hero PDP and risks regressing SPEC-CANARY work.
- **PDP-A11Y-1** — PDP A11y 0.85 (vs 0.92 sitewide). Likely missing form labels / button-name attrs on variant pickers. ~30 min targeted pass.
- **SITEWIDE-BEST-PRACTICES-1** — 0.73 flat sitewide; likely deprecated 3rd-party API. Investigate during post-LAUNCH-1 health check.
- **HOWTO-CHAIR-REBUILD** — migrate the visual-guide content from the now-redirected `/pages/how-to-adjust-my-new-chair` into a proper `ds-lp-howto-chair.liquid` in the BBI gate (HowTo schema would be high-value AEO content). The 301 redirect preserves SEO juice in the interim.
- **PDP-TITLE-PATTERN-SITEWIDE** — apply title_tag pattern (≤60 chars, brand suffix policy) to all 100 Hero PDPs (PE-5 follow-up). Today's audit only touched the representative Hero PDP for verification.

---

## ✏️ STALE-OECM-DATE-FIX-1 ✅ 2026-05-26 evening (Day 12+, after FAVICON-1)

PR-1 FIX 2 closure — aligned 4 stale OECM date references in `theme/sections/ds-lp-about.liquid` to the canonical **Agreement 2025-470** framing locked Day 8 STEVE-FACT-CHECK. Closes PRE-LAUNCH-AUDIT-1 should-fix (b) further down in this file (line ~151). Build-state row had anticipated 2 spots (`:113` body + `:245` schema, from the pre-restructure line numbers); the diff-card pair on the live file's L195/L197 carried the same legacy "since 2019" anchor and was bundled into the same fix per Leo "apply" at HALT 1. Text-only edit, no CSS or schema-structure changes.

- **Edits (4, single file `theme/sections/ds-lp-about.liquid`):**
  1. **L124** hero standfirst Liquid `default:` — `OECM Supplier Partner since 2019.` → `OECM Supplier Partner under Agreement 2025-470.`
  2. **L195** diff-card #02 `<span class="lp-diff-card__num">` — `2019` → `2025-470` (matches AI-8 OECM-page proof-bar precedent from build-state row 866)
  3. **L197** diff-card #02 body sentence — `OECM Supplier Partner since 2019, Agreement 2025-470.` → `OECM Supplier Partner under Agreement 2025-470.` (dropped redundant "since 2019" prefix; Agreement number was already present)
  4. **L278** schema `subheading` textarea `default` — mirrors L124 so theme-editor reset matches Liquid default
- **Sitewide scan** ("since 2019" across `theme/{snippets,sections,templates}`): **0 hits outside `ds-lp-about.liquid`** — no spread needed. All other sections (government, healthcare, education, non-profit, brands-*, oecm, footer, schema snippets, industries, design-services, customer-stories, quote, faq, index.json) already use canonical "Agreement 2025-470" framing.
- **Pushed via direct Admin API** (PUT `assets.json`, ApiVersion 2026-04, hardcoded to DEV `186373570873`). PUT `updated_at = 2026-05-26T15:02:16-04:00`. Re-fetch SHA-256 byte-match: `249046561a5377d5` ✓ (26,056 bytes local = remote).
- **Render check** (`/pages/about` via `preview_theme_id=186373570873`, redirect-followed to `www.brantbusinessinteriors.com/pages/about`): HTTP 200; `since 2019` rendered count = 0; `under Agreement 2025-470` count = 3; total "Agreement 2025-470" mentions = 8; diff-card `>2025-470<` anchor present (1); "Then & now" section + phone `1-800-835-9565` (11×) + Peterborough HQ `296 George St N` (5×) all intact.
- **`shopify theme check` (JSON output):** 166 files inspected / **2855 offenses** / 166 files-with-offenses — **EXACT PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses**.
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified pre-push + post-push. LIVE untouched ✓.
- **Adjacent Day 12+ work integrity (sanity checks):** FAVICON-1 (5 favicon link tags in `theme.liquid`) ✓ · NAV-REDESIGN-1-TEXT-COLOR-FIX (10 `var(--headerColor)` references in `bbi-nav.liquid`, commit `8e01aee` intact) ✓ · ABOUT-PAGE-GRID-1 (2×3 figure grid: 6 `<figure>` across `lp-evol__row` structure) ✓.
- **Pre-write backup:** `data/backups/stale-oecm-date-fix-1-pre-20260526-150159/ds-lp-about.liquid` (rollback path).
- **Branch:** `feature/stale-oecm-date-fix-1` (off `feature/favicon-1-retry @ f4aef78` — the canonical descendant tip after FAVICON-1).

---

## 🦁 FAVICON-1 ✅ 2026-05-26 (Day 12+, retry after morning revert)

Complete favicon set with brand red `#D4252A` divider (matches the footer maple leaf). 11 assets uploaded + `theme.liquid` head updated with 5 link tags + paper-white `#FAF8F5` theme-color meta. Manifest `name: "Brant Basics Business Interiors"` matches the header co-brand wordmark; `short_name: "Brant Basics"` (no customer-facing "BBI" per copy-voice rule). DEV theme only — LIVE untouched. **Retry context:** earlier today the first attempt was reverted when an unrelated header text-color bug surfaced; that bug was fixed by NAV-REDESIGN-1-TEXT-COLOR-FIX commit `8e01aee`, after which this retry ran cleanly with the already-prepared file set in `data/working/favicon-1-2026-05-26/favicon/`.

- **Phase 0 prep verification (pre-write):** All 11 prepared files present in working dir. SVG recolored to brand red (`#D4252A` rect at x=42); webmanifest uses relative paths (zero root-absolute); manifest `name` corrected mid-flight from "Brant Business Interiors" to **"Brant Basics Business Interiors"** + `short_name` set to "Brant Basics" (Leo caught the missing "Basics" before push; "BBI" not used per `feedback_bbi_copy_voice.md` rule that "BBI" is internal-only and the PWA home-screen label is customer-facing).
- **Files added (`theme/assets/`, 11):** `favicon.svg` (384B, brand red divider) · `favicon-maskable.svg` (376B) · `favicon-16.png` (508B) · `favicon-32.png` (681B) · `favicon-48.png` (813B) · `favicon-64.png` (960B) · `apple-touch-icon.png` (3,538B, 180×180 for iOS) · `icon-192.png` (3,713B, Android) · `icon-512.png` (2,205B, Android splash + PWA) · `og-preview.png` (5,358B, **uploaded but NOT wired** to `og:image` meta — deferred to FINAL PRE-LAUNCH REVIEW per earlier decision) · `site.webmanifest` (432B, relative paths).
- **`theme/layout/theme.liquid` head edit (single block):** `<meta name="theme-color" content="">` → `content="#FAF8F5"` (line 8); the `{%- if settings.favicon != blank -%}` conditional at lines 13-19 replaced with 5 link tags (`rel="icon"` SVG + 32 PNG + 16 PNG + `rel="apple-touch-icon"` + `rel="manifest"`), all using `{{ 'filename' | asset_url }}`.
- **Pushed via direct Admin API** (PUT `assets.json`, ApiVersion 2026-04, hardcoded to DEV `186373570873`, 0.5s rate-limit between writes). All 12 writes succeeded first try. Each verified by re-fetch + SHA-256 match against local — 12/12 byte-identical ✓.
- **Render check (cookie-jar request to `/?preview_theme_id=186373570873`):** 200, all 5 new link tags present in `<head>`, theme-color meta `#FAF8F5` confirmed, all 5 CDN asset URLs return HTTP 200 with correct Content-Types (PNG/SVG/octet-stream).
- **`shopify theme check` (JSON output):** 166 files-with-offenses / **2855 offenses** — **EXACT PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses**.
- **NAV-REDESIGN-1 integrity verified post-push:** DEV `snippets/bbi-nav.liquid` still has `.bbi-header { color: var(--headerColor, #0B0B0C); ... }` (from commit 8e01aee); zero `color: var(--textColor)` references; search-bar `flex:0 0 180px` from Option 4 logo bump preserved. No regression.
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified pre-push + post-push. LIVE untouched ✓.
- **Pre-write backup:** `data/backups/favicon-1-retry-pre-20260526-144825/theme.liquid` (9,446 B for rollback).
- **Working dir source:** `data/working/favicon-1-2026-05-26/favicon/` (11 files used as-is; webmanifest name corrected in place mid-Phase-0).
- **Branch:** `feature/favicon-1-retry` (off `feature/nav-redesign-1-text-color-fix @ 8e01aee` — the current canonical tip).
- **Caveat (informational, not blocker):** Shopify serves `.webmanifest` with `Content-Type: application/octet-stream` rather than the ideal `application/manifest+json`. Browsers still parse it correctly because the `<link rel="manifest">` declares intent; flag for FINAL PRE-LAUNCH REVIEW if PWA install behavior needs tightening.
- **Deferred (intentional):** `og-preview.png` uploaded as asset but NOT wired to `<meta property="og:image">` — bundled into FINAL PRE-LAUNCH REVIEW per Leo's earlier decision.

---

## 🧭 NAV-REDESIGN-1 ✅ 2026-05-26 afternoon (Day 12+)

**Third attempt at the BBI header succeeded via diagnostic-first approach.** Previous two attempts (HEADER-POLISH `65458f6`, HEADER-POLISH-2 reverted via REGRESSION-RECOVERY-1) failed because they targeted Avada selectors (`.primary-header-blocks`, `.nav-menu-link` in `theme/sections/header.liquid` + `theme/assets/header.css`) that aren't loaded on any BBI landing page. This commit targets the ACTUAL BBI header classes — `.bbi-header__inner`, `.bbi-nav__item`, `.bbi-header__logo`, `.bbi-header__search-bar` — emitted from `theme/snippets/bbi-nav.liquid` and verified in the rendered DOM via headless-browser empirical inspection at 1280 / 1600 / 1900px viewports.

- **Phase 1 (READ-ONLY diagnostic):** Render-path mapped — every BBI page (homepage via `bbi-nav-wrap.liquid` section wrapper + 30+ `ds-lp-*.liquid` sections) renders the header via `{%- render 'bbi-nav' -%}` from `theme/snippets/bbi-nav.liquid` (44KB / 1060 lines / inline 15.4KB `<style>` block). The Avada `header.liquid` / `header.css` / `header-logo.liquid` files confirmed NOT loaded on any of 5 audited BBI URLs. Single-file edit target.
- **Phase 1 root cause for >1384px misalignment bug:** NOT a `box-sizing` issue and NOT the outer `.bbi-header` extending full-width. Both `.bbi-header__inner` AND `.hp-hero__inner` correctly cap at 1320px (border-box). The actual bug: `.bbi-header__inner` flex children sum to ~1414px natural width (logo 123 + 24mR + 538 nav + 220 search + 333 utility + 64 padding + 32×3 gaps + 16 nav-mL) vs the 1320px cap → cart icon overflows the inner's right edge by 61-94px at viewports ≥1384, becoming visible as "cart at viewport-right while hero indents".
- **HALT 1 surfaced 6 options (A-F) with explicit tradeoffs.** Leo chose **Option D + Option 4** (skip bigger-nav today, fix overflow + logo bump only). Bigger-nav + 1440-cap (Option F) deferred to post-launch backlog with informational headless-browser preview saved.

**Edits (single file: `theme/snippets/bbi-nav.liquid`; plus `bbi-nav-wrap.liquid` section + `bbi-homepage.css` cleanup):**

1. **Change 4 — overflow fix:** `.bbi-header__inner` add `gap:16px` (was inheriting 32px from now-deleted bbi-homepage.css duplicate). `.bbi-nav__item` padding `0 14px → 0 12px` (saves 20px across 5 items). `.bbi-nav__item--active::after` left/right `14px → 12px` to track padding. `.bbi-header__search-bar` `flex:0 0 220px → 0 0 200px → 0 0 180px` (the final 180 set by Option 4 below). Net: -104px from natural child width.
2. **Change 5a — dead-code deletion in `bbi-homepage.css:200-234` (~34 lines):** removed duplicate `.bbi-header*` rules that the inline `<style>` in `bbi-nav.liquid` already governs (same specificity, source-order tie loses to inline). Also removed stale `.bbi-nav-item` ruleset (class never rendered — DOM uses `.bbi-nav__item`) and unused `.phone` rule. Replaced with a 5-line comment marker referencing this commit.
3. **Change 5b — semantic cleanup in `bbi-nav-wrap.liquid:14`:** `<header class="bbi-nav-wrap">` → `<div class="bbi-nav-wrap">`. Eliminates the nested `<header>` on homepage (the inner `<header class="bbi-header" role="banner">` from the snippet was already the page banner). Zero visual effect.
4. **Change 5c — mobile drawer bar:** `.bbi-mobile-nav__header` height `72px → 80px`. Proportional bump for the hamburger menu drawer header. Only visible when mobile nav is open.
5. **Change 5d — active state mechanism:** verified WORKING (not broken). The Liquid loop in `bbi-nav.liquid` correctly emits `.bbi-nav__item--active` when the `active` param matches. Home (`active:''` from `bbi-nav-wrap.liquid`) has no active item by design; all other pages emit correctly. No edit needed.
6. **Option 4 — logo bump:** `.bbi-header__logo` container height `40px → 48px`; `.bbi-header__logo img` height `36px → 44px` (+22% taller, ~150px wide vs 123px before). Liquid emission `image_url width: 300 → 400` (retina sharpness at new display size) and `image_tag height: 36 → 44` (matches CSS, prevents CLS during load). Fallback `<img>` (logo:blank path) `height="36" → "44"`. Search-bar `flex:0 0 200 → 180px` absorbs the ~26px logo width increase. Net: zero docOverflow at all viewports 1280-1900.

- **Empirical layout post-edit (headless Chrome at 1280 / 1600 / 1900px viewports):** `.bbi-header__inner` correctly 1320px wide (border-box), centered, no overflow; cart breathing-room inside inner = 0px at 1280, 32px at 1600, 32px at 1900; `docScrollWidth - viewport = 0` everywhere; logo rendered at 44×149.
- **Pushed via `scripts/push-file.py`** (hardcoded to DEV `186373570873`). Three files: `snippets/bbi-nav.liquid` (44,063 B), `sections/bbi-nav-wrap.liquid` (1,150 B), `assets/bbi-homepage.css` (36,007 B). All API-fetched post-push and byte-identical to local. Spot-checks confirm all 5 markers present, all 4 stale markers absent.
- **`shopify theme check`:** 265 files / **2855 offenses** / 166 files-with-offenses — **EXACT PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses**.
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified 5×: pre-Phase-1, pre-Phase-2 push, post-Phase-2 push, pre-Option-4 push, post-Option-4 push. LIVE untouched ✓.
- **Pre-write backups:** `data/backups/nav-redesign-1-pre-20260526-121419/` (3 files for Phase-2 rollback) + `data/backups/nav-redesign-1-pre-20260526-125853-option-4/` (incremental snapshot of `bbi-nav.liquid` before the logo bump).
- **Working dir:** `data/working/nav-redesign-1/` — rendered HTML cache for all 5 pages, header-block extraction, inline CSS dump, headless-browser test page, Option F informational preview (`option-f-preview-20260526-122231.png`), Option D applied state (`option-d-applied-20260526-122250.png`), Option 4 final state (`option-4-applied-20260526-130204.png`).
- **POST-LAUNCH BACKLOG additions:**
  - **OPTION-F-NAV-REDESIGN-2** — bigger nav (bar 88px, font 16px, padding 18px) + sitewide 1440 cap (`.bbi-container`, `.bbi-header__inner`, `.bbi-footer__inner`, `.hp-trust__inner`, `.hp-oecm__inner`, `.hp-hero__inner` all → 1440). Note: my Option F render at 1900vw showed ~51px residual cart overflow even with 1440 cap → would need 1500-1520 cap OR drop one inline element (search-bar → icon trigger). Reference preview at `data/working/nav-redesign-1/option-f-preview-20260526-122231.png`.
  - **MID-DESKTOP-OVERFLOW (1024-1280px viewport range)** — pre-existing horizontal scroll on small Windows laptops / iPad-landscape. NAV-REDESIGN-1 reduced it from 357px → 0px at 1280 specifically, but 1024-1279 still overflows by up to 250px. Fix options: tighten mobile breakpoint up to 1280, OR hide inline search/phone at <1280, OR shrink top-level nav items further.
- **Branch:** `feature/nav-redesign-1` (off `feature/homepage-shop-furniture-hover-1 @ cb06df9` — the canonical latest descendant of REGRESSION-RECOVERY-1 `e81978a`).

---

## 🖱 HOMEPAGE-SHOP-FURNITURE-HOVER-1 ✅ 2026-05-26 late evening (Day 11+1)

Added black-fill `:hover` + `:focus-visible` behavior to the homepage hero **Shop furniture** secondary CTA (`href="/collections/business-furniture"`). Phase 1 audit surfaced a hidden architectural issue: the existing secondary-CTA hover rule at `bbi-homepage.css:641-646` was scoped to `.hp-root .bbi-btn--secondary, .bbi-section .bbi-btn--secondary` — but `.hp-root` is **never used in any template** (grep across `theme/` returns zero matches outside the CSS file itself), and the hero is `<section class="hp-hero">` (not `.bbi-section`), so the hero button matched neither selector and had no hover today. Other homepage secondaries (e.g. "Browse all categories" inside `.bbi-section .hp-shop`) were already covered. Chose Option 1: extend the existing rule's selector list to add `.hp-hero .bbi-btn--secondary` + add `:focus-visible` parity across all three ancestry contexts.

- **Edit (1, CSS-only):** `theme/assets/bbi-homepage.css:641-646` — existing 2-selector `:hover` block expanded to 6 selectors: `(hp-root | bbi-section | hp-hero) × (:hover | :focus-visible)`. Values unchanged: `background:#0B0B0C; color:#F7F8FA; border-color:#0B0B0C;` (matches the canonical `--textColor` BBI ink).
- **No new tokens, no `!important`.** Transition already inherited from base `.bbi-btn` at line 145 (`background-color 120ms ease, color 120ms ease, border-color 120ms ease`).
- **`templates/index.json` NOT touched.** CSS-only change per prompt scope.
- **Pushed via `scripts/push-file.py`** (hardcoded to DEV `186373570873`). Push confirmed `updated_at` 2026-05-26T00:27:56. DEV sha = local sha post-push (`aa481982514bfb1e`).
- **Render-check:** `/?preview_theme_id=186373570873` 200, hero Shop furniture button present (`bbi-btn--secondary bbi-btn--lg`), primary CTA (`hp-hero__cta-red` Request a Quote) intact in DOM, CSS asset URL serving fresh hash.
- **Side-effect (intentional):** existing `.hp-root` + `.bbi-section` secondary CTAs picked up `:focus-visible` keyboard-parity behavior — minor accessibility win at zero visual cost.
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified pre- and post-push. LIVE untouched ✓.
- **Pre-push backup:** `data/backups/shop-furniture-hover-pre-20260526_002744/bbi-homepage.css`.
- **Branch:** `feature/homepage-shop-furniture-hover-1` (off `feature/homepage-tile-border-match-1` @ 164ac6b).

---

## 🎨 HOMEPAGE-TILE-BORDER-MATCH-1 ✅ 2026-05-26 late evening (Day 11+1)

Aligned tile borders + hover behavior across the 3 homepage tile sections so they share one visual language. Two-reference surgical CSS change: **Featured this quarter** (`.bbi-card--product`) + **Shop the catalog** (`.bbi-card--collection`) tiles now inherit the static border color from **Industries** (`.hp-industry`, `var(--bbi-line) = #E5E5E7`) and the hover-darken behavior + transition from **Our Work** (`.hp-case`, `border-color: var(--textColor); transition: border-color 120ms ease`). R1 and R2 turned out to already share identical static borders, hover targets, and transition timing — fully coherent reference set, no mixing required.

- **Edits (3, CSS-only spirit):**
  1. `theme/assets/bbi-homepage.css:280` — `.bbi-card--product` gains `transition: border-color 120ms ease` + adds `.bbi-card--product:hover { border-color: var(--textColor); }`.
  2. `theme/assets/bbi-homepage.css:505-510` — `.bbi-card--collection` gains `border: 1px solid var(--bbi-line); transition: border-color 120ms ease;` + adds `.bbi-card--collection:hover { border-color: var(--textColor); }`. (Previously had no border at all.)
  3. `theme/templates/index.json` `bbi-featured` inline `<style>` — removed duplicate `.hp-products .bbi-card--product { border: 1px solid #9BA1AB; }` rule that was overriding the CSS file. Phase 1 confirmed border was defined inline, so prompt allowed touching `index.json` here.
- **No new tokens, no `!important`.** Reuses `--bbi-line` + `--textColor`.
- **Pushed via direct Admin API** (assets.json PUT, ApiVersion 2026-04) — `bbi-push-landing.py` doesn't cover `bbi-homepage.css` or `index.json` (its patterns are `ds-*`/`page.*`). Target: DEV `186373570873` only. Push confirmed `updated_at` 2026-05-26T00:09:17 (CSS) + 00:09:20 (index.json).
- **Render-check:** `/?preview_theme_id=186373570873` 200, all 4 section titles present in HTML, old `#9BA1AB` literal absent. CDN-served minified CSS confirms all 4 target rules live (`.12s` is minifier-normalized `120ms`).
- **`shopify theme check`:** 265 files / **2855 offenses** / 166 files-with-offenses — **EXACT PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses** (CSS-only changes can't introduce Liquid/schema warnings).
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified pre-push + post-push. LIVE untouched ✓.
- **Pre-push backup:** `data/backups/homepage-tile-border-match-pre-20260526_000904/` (bbi-homepage.css + index.json snapshots for rollback).
- **Branch:** `feature/homepage-tile-border-match-1` (off `feature/keilhauer-photo-swap-1` @ a1b6fc2 — the canonical latest descendant).
- **Caveats (visible diff):** Featured tile borders go from `#9BA1AB` (mid-gray) to `#E5E5E7` (lighter); Shop catalog tiles gain a thin 1px frame they didn't have before. Both Featured + Shop tiles now darken to near-black on hover instead of being static.

---

## 📷 KEILHAUER-PHOTO-SWAP-1 ✅ 2026-05-26 late evening (Day 11+1)

Replaced Keilhauer brand hero + brand hub tile photos with a new boardroom scene (long marble table, ~14 tan/camel Keilhauer chairs, floor-to-ceiling city windows, pendant rings, wall TV). Audit-first scope confirmation surfaced that Keilhauer has ONLY 2 image surfaces in the entire theme — sub-page hero + brand hub tile (no Keilhauer-branded tiles on any industry/category landing pages; 0 `vendor=Keilhauer` products). New `-v2.jpg` files uploaded matching peer-brand convention (otg/ergocentric/obusforme already on v2).

- **Source:** `/Users/leokatz/Desktop/kielheur/Screenshot 2026-05-25 at 11.39.43 PM.png` (1374×974 PNG, 2.0 MB). Smaller than hero target → Halt 1 Option A: Lanczos upscale to peer spec, accept slight softening (boardroom subject hides it cleanly).
- **Processing:** ImageMagick Lanczos `1920x1080^` + `1200x900^` center-extent + sRGB strip + Q-escalation (Q85 291/193 KB over peer range → Q80 244/161 KB still over → Q75 216/141 KB in peer range).
- **Uploads (2 BBI-prefixed Shopify Files):** `bbi-brand-keilhauer-hero-v2.jpg` (1920×1080, 216 KB) · `bbi-brand-keilhauer-tile-v2.jpg` (1200×900, 141 KB). Both READY first poll.
- **Files modified (2 templates):** `templates/page.brands-keilhauer.json:7` (hero ref) · `templates/page.brands.json:8` (`keilhauer_image` tile ref). Pushed via `push-file.py` (rate-limit 0.5s) to DEV `186373570873`. DEV re-fetch confirms 1 new-ref / 0 old-ref per file.
- **Render-check (4 URLs):** `/pages/brands-keilhauer` 200 (hero-v2 ×4) · `/pages/brands` 200 (tile-v2 ×3) · `/pages/brands-heartwood` 200 (untouched sanity) · `/pages/brands-otg` 200 (untouched sanity). All HEAD checks on new CDN URLs: 200, 221/145 KB.
- **`shopify theme check`:** 166 files / 2855 offenses / 166 files-with-offenses — **EXACT PRE-LAUNCH-AUDIT-1 baseline match, zero new offenses**.
- **LIVE integrity:** `updated_at = 2026-05-16T16:47:22-04:00` verified 5×: pre-Phase-1, pre-Halt-1, pre-Halt-2, post-push, post-verify. LIVE untouched ✓.
- **Pre-push backup:** `data/backups/keilhauer-photo-swap-pre-1779767691/` (2 JSONs for rollback).
- **Report:** `data/reports/keilhauer-photo-swap-2026-05-26.md`. **Working dir:** `data/working/keilhauer-photo-swap-2026-05-26/` (raw + processed + PROCESSED.md + upload-create-response.json + uploaded-final.json).
- **Branch:** `feature/keilhauer-photo-swap-1` (off `feature/hp-hero-office-img` since HOMEPAGE-HERO-SLIDESHOW-1 hadn't landed). Old `bbi-brand-keilhauer-{hero,tile}.jpg` files remain in Shopify Files as orphan candidates (not deleted — rollback path).
- **Out-of-scope (informational):** 0 `vendor=Keilhauer` products → product-image exclusion clause moot.

---

## 🛠 REGRESSION-RECOVERY-1 (Option C, FULL COVERAGE) ✅ 2026-05-25 late evening

Followed the HEADER-POLISH-2 regression earlier in the evening; full diagnostic + recovery executed.

- **Root cause:** branch `feature/header-polish-2` was created off `main` (not off `feature/about-page-grid-1`), then `bbi-push-landing.py --snippets` was fired from there — bulk push uploaded `main`'s stale pre-Day-11 content for every in-glob file to DEV. The 10-line HEADER-POLISH-2 CSS commit was byte-clean; the bulk push that followed it caused all damage. Reflog + DEV `updated_at` clustering at `2026-05-25T21:19:55-04:00` = direct evidence. See `data/reports/regression-diagnostic-1-2026-05-26.md`.
- **Recovery path:** Option C — full revert of HEADER-POLISH-2 by re-running the bulk push from `feature/about-page-grid-1`. HEADER-POLISH-2 was dropped entirely (preserved on `origin/feature/header-polish-2` for future redesign).
- **Files restored on DEV (22 BOTH_REGRESSED + 1 LOCAL_REGRESSED + bonus drift fix):**
  - 22 templates/sections/snippets restored to `feature/about-page-grid-1` state
  - `assets/bbi-homepage.css` HOMEPAGE-BORDERS `--bbi-line × 18` tokens restored (new finding the original regression report missed)
  - `snippets/bbi-quote-modal.liquid` pre-existing 4-day drift fixed as bonus
  - `templates/index.json` was self-restored at 21:38:31 before this recovery
- **Push mechanics:** 65 files via `bbi-push-landing.py 186373570873 --snippets`, +3 rate-limit retries via `push-file.py`, +13 secondary pushes for files outside the `--snippets` glob (9 `collection.*.json` + `bbi-homepage.css` + `sections/header.liquid` + `snippets/header-logo.liquid` + `assets/header.css`). All 81 push operations succeeded.
- **Verification:**
  - Content: 30/30 marker counts match local about-grid; JSON files show normal Shopify whitespace normalization on PUT
  - `--bbi-line` × 18 present in `bbi-homepage.css` ✓; HEADER-POLISH-2 `140px`/`21px`/`64px` rules absent from `bbi-nav.liquid` ✓
  - Theme check: **265 files / 2855 offenses / 166 files-with-offenses — exact PRE-LAUNCH-AUDIT-1 baseline match** ✓
  - Render check: **38/38 pages pass** across Categories 1–7 (homepage / 9 collections / 10 sub-collections / 6 brand pages on corrected `/pages/brands-{slug}` URLs / 6 industries / about + customer-stories / quote+contact+oecm smoke)
  - LIVE theme: still `updated_at = 2026-05-16T16:47:22-04:00` throughout — UNTOUCHED ✓
- **Pre-recovery DEV snapshot:** `data/backups/regression-recovery-1-option-c-pre-1779763620/` (30 files for rollback)
- **Render results:** `data/working/regression-recovery-1/render-results.json`
- **Push logs:** `data/working/regression-recovery-1/bulk-push.log` + `secondary-push.log`
- **POST-LAUNCH BACKLOG additions:** (a) **stale-local guard** on `bbi-push-landing.py` — abort if any local blob SHA is older than DEV's last-write SHA from the image-work branch tip; (b) **HEADER-POLISH-2 redo** — preserved on `origin/feature/header-polish-2`, future redesign opportunity with full hero-image sizing plan; (c) **fix `bbi-push-landing.py` glob** to optionally include `templates/collection.*.json` + `assets/bbi-*.css` + `sections/header.liquid` + `snippets/header-logo.liquid` + `assets/header.css` behind explicit flags (today recovery needed 13 secondary `push-file.py` calls to cover them).
- **URL correction noted (non-regression):** brand-page handles are `brands-{slug}` (URLs `/pages/brands-{slug}`), not `{slug}` — the regression-diagnostic-1 Phase 6 list and the recovery prompt used `/pages/brands/{slug}` and `/pages/{slug}` which both 404. The 6 actual brand sub-pages all render clean on the corrected URLs.
- **State after recovery:** DEV matches PRE-LAUNCH-AUDIT-1 baseline. Day 11 image work intact. Build can resume on `feature/about-page-grid-1` from here.

---

## 📍 RIGHT NOW — fireable this moment

⏳ items with no prerequisites blocking them. Pick any, in any order. **Day 11 launch-day evening queue** — HIGH-3 fix already landed (`7fb46b7`); Day 11 parallel image rounds (collection / brand / customer-stories / homepage-featured / industry-heroes) already shipped; PRE-LAUNCH-AUDIT-1 returned ✅ READY FOR LAUNCH. What remains is mostly the Upwork delivery + LAUNCH-0→4 chain.

- **#1 Cornerstone Post 1 visual spot-check** — quick eyeball of the published article on the DEV preview (tables, CTA buttons, captions render clean) (~5 min)
- **#2 W0-1 + W0-3 final verify** — quick confirm GSC/GA4 + redirects (~10 min, anytime)
- **#3 PRE-LAUNCH-AUDIT-1 should-fixes (4 items, all optional)** — see `data/reports/pre-launch-audit-2026-05-25.md`: (a) HEADER-POLISH dead-code decision — accept as-is OR port bar/nav rules to `bbi-homepage.css` (~0–15 min); (b) STALE-OECM-DATE-FIX — `ds-lp-about.liquid:113` body + `:245` schema still say "OECM Supplier Partner since 2019", should be Agreement 2025-470 framing (~5 min); (c) 7 non-BBI-prefixed Shopify Files uploads today — rename or annotate (~0–5 min); (d) 2 raw RGB `229,229,231` occurrences in `bbi-homepage.css` — tokenize to `var(--bbi-line)` (~2 min). None block LAUNCH-2.

> #4 Upwork delivery review / #5 Step 46 IMAGE SWAP ✅ RESOLVED / STALE 2026-05-26 — Day 11 image work shipped all launch-critical slots. LAUNCH-0 → LAUNCH-4 chain is no longer blocked on image work; only gated by remaining launch-path steps (Step 3-6 in tomorrow's path). The Day 11 EOD tracker + build-state sync fires at end of day — not a "right now" candidate.

---

## 📋 DO NEXT (linear order) — 15 items, dependency order

No day labels. Order reflects dependencies. Each item carries a status flag (⏳ READY / 🟡 SUPERSEDED / 🔒 BLOCKED) + time estimate; 🔒 items show a **BLOCKED ON** line. The 9 Day-10 closures + the Day 11 morning HIGH-3 fix (commit `7fb46b7`) have dropped off the queue — see the COMPLETED archive. Reordered for Day 11 evening: residual ⏳ READY items → image-swap stack → LAUNCH-0→4 stack.

1. **Cornerstone Post 1 visual spot-check** — ⏳ READY — ~5 min. Eyeball the published article on the DEV preview — 3 tables, CTA buttons, `<caption>` + `scope` attrs all render clean under `ds-article.liquid`.
2. **Image swap pipeline prep** — 🟡 SUPERSEDED Day 11. Was: pre-draft the Claude Code manifest-ingestion prompt + verify the Shopify Files upload pipeline with a test image. Today's parallel image rounds (collection / brand / customer-stories / homepage-featured / industry-heroes) shipped directly via per-round Python scripts in `scripts/collection-img-pull-phase{1..5}.py` etc. without the manifest pipeline. Remaining Upwork-delivered slots (~63) can use the same per-round pattern.
3. **W0-1 + W0-3 final verify** — ⏳ READY anytime — ~10 min. Quick confirm GSC + GA4 (✅ done 2026-05-22) and redirects CSV (✅ 171/173 verified). Quick-confirm only.
4. **Upwork delivery review** — ✅ RESOLVED / STALE 2026-05-26. Day 11 image work shipped all launch-critical slots (COLLECTION-IMG-PULL-1, BRAND-IMG-1, INDUSTRY-HEROES, ABOUT-PAGE-GRID-1). The 63-slot block was stale planning. LAUNCH-0 → LAUNCH-4 no longer blocked.
5. **Step 46 IMAGE SWAP session (remaining ~63 slots)** — ✅ RESOLVED / STALE 2026-05-26. Day 11 image work shipped all launch-critical slots (COLLECTION-IMG-PULL-1, BRAND-IMG-1, INDUSTRY-HEROES, ABOUT-PAGE-GRID-1). The 63-slot block was stale planning. LAUNCH-0 → LAUNCH-4 no longer blocked.
6. **W0-2-PHOTOS — 10 photos upload to GBP** — 🔒 BLOCKED — ~15 min. Upload 10 photos to the Google Business Profile. **BLOCKED ON:** Steve photo selection (10 from `oci-photos` + `design-photos` folders).
7. **SYS-VERIFY-1 Phase 2 re-run** — ⏳ READY — ~30 min (light). Verify no regressions after Day 11 image work. (Was: BLOCKED on #5 image swap — unblocked 2026-05-26 since #4/#5 are RESOLVED/STALE.)
8. **Step 37 LAUNCH-0 — image confirmation gate** — ⏳ READY — ~30 min. Leo row-by-row image CSV approval; hard gate before LAUNCH-1. (Only gated by remaining launch-path steps — Step 3-6 in tomorrow's path; image-block dependency cleared.)
9. **Step 38 LAUNCH-1 — GO/NO-GO report** — ⏳ READY — ~30 min. Pre-publish GO/NO-GO report. (Only gated by remaining launch-path steps — Step 3-6 in tomorrow's path; image-block dependency cleared.)
10. **Step 39 LAUNCH-2 — GO-LIVE manual click** — ⏳ READY. The manual Publish click in Shopify Admin; never automated. (Only gated by remaining launch-path steps — Step 3-6 in tomorrow's path; image-block dependency cleared.)
11. **Step 40 LAUNCH-3 — sitemap resubmit + 72h 404 monitor** — 🔒 BLOCKED — ~15 min. Resubmit sitemap to GSC + start the 72h 404 monitor. **BLOCKED ON:** #10 LAUNCH-2.
12. **Step 41 LAUNCH-4 — post-launch monitoring + mobile smoke test** — 🔒 BLOCKED — ~15 min. Activate the post-launch monitoring playbook (`docs/plan/post-launch-monitoring.md`) + mobile smoke test across Chrome, Safari, Firefox, iOS, Android. **BLOCKED ON:** #10 LAUNCH-2.
13. **GSC-RECRAWL — submit affected URLs after SERP fixes go LIVE** — 🔒 BLOCKED — ~5 min. Submit affected URLs in Google Search Console once the DEV theme is published. Do Monday after LAUNCH-2. **BLOCKED ON:** PR-1 merged (✅ done) + #10 LAUNCH-2 live + 24h re-crawl latency.
14. **Step 36d Cornerstone Post 2 — Healthcare FHTs** — 🔒 BLOCKED — ~2–3h. Same flow as Post 1; links `/pages/healthcare` + `/pages/oecm`. Outline approved by Steve — drafting deferred to **Tuesday**; does not block Monday launch. **BLOCKED ON:** dedicated drafting session (Tue) + Steve draft review.
15. **EOD tracker + build-state update (Day 11)** — 🟡 IN PROGRESS — this build-state sync (2026-05-25 evening, after PRE-LAUNCH-AUDIT-1) covers Day 11 morning + afternoon work; a final EOD sync after LAUNCH-2 will close this row.

---

## ⏳ STEVE HOMEWORK

**Pending now:**
- **Idea #15 — 3-card SKU picks** ✅ CLOSED 2026-05-25 — Heartwood: L-Shape Height Adjustable Desk Set (`/products/l-shape-height-adjustable-desk-set`) · OTG: Raven High-Back Heavy-Duty Synchro-Tilter OTG10703B (`/products/raven-high-back-heavy-duty-synchro-tilter-chair-otg10703b`) · GFG: Global Accord Mesh-Back Tilter (`/products/global-accord-mesh-back-tilter`) — unblocks #6 IMAGE SWAP critical path.
- **W0-2-PHOTOS selection** — 10 photos from `oci-photos` + `design-photos` folders — needed for #7 GBP photo upload.

**Post-launch (optional / non-blocking):**
- **Cornerstone Post 1 editorial pass** — post is LIVE at `/blogs/news/oecm-ontario-school-boards-office-furniture` (article ID `689003888953`); edit in Shopify Admin anytime. Optional now that it's published — no longer blocks anything.
- **W0-2 GBP completion** — areas, attributes, social, Q&A, posts (see POST-LAUNCH BACKLOG).
- **W0-2c-EVIDENCE** pack.
- **W0-2c-SIGNAGE** — physical "Brant Business Interiors" signage at 296 George St N.
- **W0-CIT-OECM** — verify OECM vendor directory NAP.

> Resolved/closed Steve items moved to record: **HIGH-1 Notifications inbox routing** ✅ verified by Steve 2026-05-24 (closed the LEAD-2 lead-loss risk → LAUNCH-2 GO) · **Cornerstone Post 1 outline** ✅ approved 2026-05-24 (used for the published draft) · **Cornerstone Post 2 outline** ✅ approved 2026-05-24 (saved for Tuesday's draft) · **SCHEMA-LOCALBIZ-1 sameAs URLs** ✅ answered 2026-05-24 (no current LinkedIn/Facebook/Instagram presence — sameAs stays empty; documented in `bbi-localbusiness-schema.liquid` via PR-2) · **W0-1** ✅ done 2026-05-22 (GA4 `G-XLCM9LCNLN` + GSC domain property + GSC↔GA4 link; Leo added as GA4 Admin) · **W0-3** ✅ verified Day 9 (171/173 redirects live) · **INSTALL-PHOTO-QUERY (Step 53)** ✅ answered 2026-05-21 (stock fine) · **STEVE-FACT-CHECK (Step 55)** ✅ resolved 2026-05-21 · **LEAD-INBOX-1 (Step 21)** ✅ done 2026-05-14. LEAD-3 manual M365 follow-ups remain (see `docs/strategy/bbi-lead-routing.md`). Leo launch gates (LAUNCH-0 #9, LAUNCH-2 #11) live in the DO NEXT queue; the INTERLINK-3 INFO pre/post-launch call sits in the POST-LAUNCH BACKLOG.

---

## ✅ COMPLETED STEPS — condensed, by day (43 items)

Mirrors the tracker's Completed Archive. Full commits/counts/rationale in `docs/project/launch-tracker-archive.md` and the Wave A–H tables preserved below.

**Day 11 · 2026-05-25 — (no new numbered Steps closed · 1 numbered-Step sub-closure + 14 non-counted closures)**

- **HIGH-3 fix — `theme/snippets/product-form-buttons.liquid:31`** (was `:30` pre-edit) — sub-closure of the last SYS-VERIFY HIGH finding from Step 22 LEAD-2 (LEAD-2 itself was numbered-step-closed Day 10). Stale `/pages/contact` CTA → `/pages/quote` with new param schema (`lead_type=quote&product=handle&title=title`) so the sitewide `bbi-quote-modal.liquid` click handler intercepts it. Same modal-intercept pattern PR-2 used for HIGH-1. Affects sold-out / $0-price PDPs. Commit `7fb46b7` (timestamped 2026-05-24 12:01 but labeled "Day 11 #1" in the commit body — Leo did the work after Day 10 EOD sync was already written). Does NOT increment the /54 (LEAD-2 was the numbered step; this is a sub-finding closure).

> **Also shipped Day 11 but NOT counted in the /54** (the count stays at 43 because today's work was either sub-finding closures or sub-work toward Step 46 IMAGE SWAP — which still owns ~63 remaining inventory slots, gated on the Upwork delivery). Net image slots filled Day 11: **~82** (53 collection + 12 brand + 2 customer-stories + 3 homepage-featured + 4 industry + 8 about-grid; the 8 about-grid slots are an out-of-Upwork-manifest brand-evolution narrative add — they do NOT shrink the ~63-remaining count):
>
> - **COLLECTION-IMG-PULL-1 — programmatic collection image pull (53 slots)** — Claude Code session pulled 1 lead product image per collection / sub-collection (bestseller-tagged → first-product fallback, both filtered to require ≥1 image after HALT 1 selection-logic upgrade), processed to slot spec via ImageMagick (1920×1080 hero / 1200×900 tile, JPG sRGB Q85), uploaded to Shopify Files via GraphQL `stagedUploadsCreate` + `fileCreate` (53/53 READY), and patched into the 9 category-template JSONs on DEV `186373570873`. **53/53 verified** via Admin API re-fetch. **0 SKIP** after the HALT 1 selection-rule upgrade. **0 KEEP** (bucket B homepage slots not in scope). 9 templates touched: `collection.{seating,desks,tables,storage,boardroom,accessories,panels-room-dividers,ergonomic-products,business-furniture}.json`. Hero refs added: 9; tile refs added: 44. `shopify theme check`: 265 files / 2855 offenses across 166 files — IDENTICAL to PR-1/PR-2 baseline (zero new offenses). Pre-write backups: `data/backups/collection-img-pull-pre-20260525-161759/` (9 JSONs). Report: `data/reports/collection-img-pull-2026-05-25.md`. Working dir: `data/working/collection-img-pull-2026-05-25/` (raw + processed + uploaded.csv + PROCESSED-VERIFICATION.md + SPOT-CHECK-2x3.jpg). Mapping: `data/research/collection-img-pull-mapping-2026-05-25.csv`. Scripts (5 new): `scripts/collection-img-pull-phase{1-mapping,2-download,3-process,4-upload,5-apply}.py`. **Honest scope (preserved from prompt):** this is the PAGE-IMG-1 commit `be1409d` approach re-applied; visual-quality limitations from low-res source thumbnails accepted upfront; Upwork bbi-images-v2 set still on the table as a Day 12-13 re-polish pass. **Two slots flagged at HALT 2** for potential hand-swap from Upwork later: `business-furniture-tile-boardroom` (lead reads more like a desk than boardroom) and `desks-tile-straight` (lead reads more like an executive desk than single-surface). Branch `feature/collection-img-pull-1`. **Commits:** `0d3d1ba` (initial 53-slot pull) → `edf3207` (tables hero+tile + boardroom hero+tile photo swap) → `a85be7c` (9 heroes v3: cover-crop → contain) → `7da3d74` (v4: upgrade all 53 slots to higher-res recent product photos + apply contain processing across tiles).
> - **BRAND-IMG-1 — 12 brand-page hero + hub-tile slots populated (6 brands × 2 slots)** — Leo hand-sourced brand photos via brand-owner sites + Shopify Files upload, applied to hero + hub-tile slots on the 6 brand pages: Heartwood, Global/Teknion, OTG, ObusForme, ergoCentric, Keilhauer. Initial round contain processing (12 slots); follow-up #1 switched 3 brand-hub tiles contain → cover to fill entire tile block; follow-up #2 switched 3 brand-page heroes contain → cover to fill the hero block. **Commits:** `71b0d05` (initial 12 slots) → `401c4df` (3 hub-tile cover) → `1fa3cff` (3 hero cover). 18 BBI-prefixed Shopify Files uploads (`bbi-brand-{slug}-{hero,tile}{-v2}.jpg`).
> - **Customer-stories — story4 (Healthcare) + story5 (School Library) populated** — replaced "case study pending verification" placeholders with real photos + body rewrites. Commit `71c2e97`. 2 BBI-prefixed Shopify Files uploads (`bbi-cs-{healthcare,school-library}.jpg`).
> - **Homepage hp-featured — 3 product cards filled with Idea #15 SKU picks (5 commits of iteration)** — Heartwood L-Shape Height Adjustable Desk Set + OTG Raven High-Back Heavy-Duty Synchro-Tilter OTG10703B + GFG Global Accord Mesh-Back Tilter; aspect-ratio 16:9 → 1:1 with visible #0B0B0C card border; 3 product cards switched `object-fit: cover` → `contain` so full product fits; bordered + padded card frames with flex-centered images; card border #0B0B0C → #9BA1AB (design-system gray-400). **Commits:** `b60a47c` → `e884b57` → `b915800` → `3c5bf43` → `40510cb`. 3 BBI-prefixed Shopify Files uploads (`bbi-hp-featured-card{1,2,3}.jpg`).
> - **Homepage hero H1 + 4 shop tiles + 5 industry tiles** (3 of 4 requested parts shipped). Commit `8dd62b6`.
> - **INDUSTRY-HEROES — non-profit + professional-services hero swaps** — Leo hand-picked 2 industry-page heroes. Commit `a0ffa99`. 4 BBI-prefixed Shopify Files uploads (`bbi-page-img-{non-profit,professional-services}-{hero,tile}.jpg`).
> - **INDUSTRIES-HUB-TILES — non-profit + pro-services tile cards on `/pages/industries`** (positions 04 + 05). Commit `0be4c2c`.
> - **HOMEPAGE-INDUSTRY-TILES — swap non-profit + pro-services tile `<img>` srcs to match new industry-page heroes**. Commit `b07b2af`.
> - **ABOUT-PAGE-GRID-1 — 2×4 brand-evolution photo grid on `/pages/about` (8 slots)** — Claude Code session sourced 12 screenshots from `/Users/leokatz/Desktop/About us/`, surfaced filenames + proposed position assignment to Leo, processed 8 selected sources to 800×600 JPG @ Q85 via ImageMagick (gravity=center for 7; **gravity=north for POS 2 jumbotron** to preserve the upper-half subject — one-line content-aware deviation accepted at HALT 1), uploaded all 8 to Shopify Files via GraphQL `stagedUploadsCreate` + `fileCreate` (8/8 READY) with BBI-prefixed filenames `bbi-about-grid-{01..08}-{slug}.jpg` (matches audit should-fix #3 hygiene rule), then inserted a new `<section class="lp-evol">` between `.lp-intro` (history narrative) and `.lp-diff` (Why-BBI cards) inside `theme/sections/ds-lp-about.liquid`. **Top row (history):** Brant Basics daytime storefront → arena jumbotron → legacy wordmark → night storefront. **Bottom row (current):** open-plan workstations → boardroom → showroom floor → atrium lounge. Heading "Then and Now." with intro "What started as Brant Basics has evolved into Brant Business Interiors — same family, expanded mission." closes the rebrand loop the prose nearby doesn't make explicit. Single-file edit (CSS + HTML inline in the section's existing `<style>` block, matching the About-page-local pattern — no `bbi-homepage.css` edit, no template JSON edit, no `theme.liquid` edit). Liquid `'name.jpg' | file_url` filter resolves URLs dynamically at render. Per-image alt text, `width="800" height="600"`, `loading="lazy"`. Mobile breakpoint added at ≤768px (4-col → 2-col). `shopify theme check`: **2855 offenses across 166 files — IDENTICAL to PRE-LAUNCH-AUDIT-1 baseline (zero new offenses)**. DEV verification: HTTP 200 on `/pages/about`, all 9 markup checks pass on re-fetch, all 8 image CDN URLs return HTTP 200 via HEAD (combined 547 KB; largest 115 KB / smallest 20 KB). Pre-write backup: `data/backups/about-grid-pre-20260525-205448/ds-lp-about.liquid`. Report: `data/reports/about-grid-2026-05-25.md`. Working dir: `data/working/about-grid-2026-05-25/` (raw + processed + PROCESSED-VERIFICATION.md + UPLOAD-LOG.md + uploaded.csv). Branch `feature/about-page-grid-1`. The team photo (~25 staff in red shirts, 6:14.01 source) was set aside as ambiguous-era; would slot as full-width below the grid if Leo wants it later.
> - **HOMEPAGE-BORDERS — introduce `--bbi-line` token (canonical `#E5E5E7`)** in `theme/assets/bbi-homepage.css` + `bbi-about` inline style; drop dead `!important` polish block; subsequent commit aligned the token value to canonical `#E5E5E7`. Post-edit state: 17 `var(--bbi-line)` refs in `bbi-homepage.css`; 0 `var(--borderColor)` refs remain (replaced); **2 raw RGB `229,229,231` occurrences still in `bbi-homepage.css`** — flagged as should-fix #4 in `data/reports/pre-launch-audit-2026-05-25.md` (~2 min to tokenize). **Commits:** `2cbd469` (introduce token + replace `--borderColor` refs + drop dead polish block) → `cecabd7` (align value to canonical `#E5E5E7`).
> - **Image bucket A/B workflow (28 CRITICAL+HIGH slots categorized)** — manual-friendly (theme editor, 24 slots) vs code-edit-required (theme code, 4 slots); per-slot Shopify Admin URLs + ImageMagick pre-processing commands. Output drives interactive manual upload session. Commit `34fd438` (on `main`).
> - **Image slot inventory + Upwork gap analysis** — 137 slots across BBI theme (13 CRITICAL + 15 HIGH + 95 MED + 14 LOW) categorized; 28 CRITICAL+HIGH read: 0 ready, 9 needs-resize, 10 needs-sourcing, 9 needs-placeholder-creation. Output: `data/research/image-slot-inventory-2026-05-25.md`. Read-only — no theme writes. **Commits:** `d3fd023` (inventory) → `4047a19` (v2 + Upwork gap analysis).
> - **HEADER-POLISH — 2× logo, 140px bar, 21px nav** — `theme/sections/header.liquid` `--logoWidth` multiplied by 2 (logo doubles visually via the inline `<style>` in the section + `header-logo.liquid`); `theme/snippets/header-logo.liquid` `image_url width: 200→500` + widths array `'50,100,150,200,250'`→`'100,200,300,400,500'` + height/width recomputed off `logo_w_display`; `theme/assets/header.css` `.primary-header-blocks` `min-height: 75→140px`, `.nav-menu-link` `padding: 15→23px` + `font-size: 14→21px`. **PRE-LAUNCH-AUDIT-1 Phase 5 caveat:** the `header.css` and `sections/header.liquid` portions modify CSS / a section that is NOT loaded / rendered on any BBI landing page (5/5 audited pages load only `bbi-homepage.css` + `information-drawer.css`; BBI DOM has zero `.primary-header-blocks` / `.nav-menu-link` class references). The logo 2× DOES render via `header-logo.liquid` where invoked. Should-fix #1 in `data/reports/pre-launch-audit-2026-05-25.md` is the decision: (a) accept as no-op on BBI surface, or (b) port the bar/nav rules to `bbi-homepage.css` targeting the actual BBI header. Commit `65458f6` (fired during PRE-LAUNCH-AUDIT-1 Phase 1).
> - **Tooling — `scripts/bbi-preview-dev.py` + `scripts/bbi-wire-hero-image.py`** — `bbi-preview-dev.py` generates a signed DEV-theme preview URL using `_ab=0&_fd=0&_sc=1` params to keep requests on `office-central-online.myshopify.com` (the naive form 301s to the custom domain and drops the preview cookie); `--verify` curl-checks for dev markers (`hp-hero__title`, `logoWidth`); used extensively by PRE-LAUNCH-AUDIT-1 Phase 5. `bbi-wire-hero-image.py` is a helper for wiring hero image refs into template JSON. Commit `02668a6` (fired during PRE-LAUNCH-AUDIT-1 Phase 1).
> - **`.gitignore` hygiene — stray Avada `snippets/` + build-state `.bak-*` backups** — surfaced by PRE-LAUNCH-AUDIT-1 Phase 1: 98-file root-level `./snippets/` directory dated 2026-05-11 12:10 (a misdirected `shopify theme pull` from repo root that dumped LIVE Avada theme snippets); 8 `bbi-build-state.md.bak-*` auto-snapshots from 2026-05-21 → 2026-05-23. Both now `.gitignore`d (no commit of those files). Commit `ab3b537` (fired during PRE-LAUNCH-AUDIT-1 Phase 1).
> - **PRE-LAUNCH-AUDIT-1 — comprehensive state audit before LAUNCH-2** — read-only audit across uncommitted work, branch state, DEV deployment, LIVE integrity, render-breakage on 8 key URLs, build-state deltas. **Verdict: ✅ READY FOR LAUNCH — 0 critical findings · 4 should-fix · 6 nuisance.** LIVE theme `updated_at` 2026-05-16 (zero LIVE assets touched today; 350 LIVE assets all dated 2026-05-11 or earlier). DEV in sync with local (5 apparent JSON byte-drifts ruled whitespace-only after structural comparison). All 8 audited URLs (`/`, `/collections/seating`, 4 industry pages, `/pages/industries`, `/pages/contact`, `/pages/quote`) return HTTP 200 with zero Liquid errors / app errors and DEV theme markers present. `shopify theme check` baseline (2855 offenses across 166 files; 1981 `ValidSchemaTranslations` pre-existing Foxtheme inheritance) unchanged from PR-1/PR-2 reference. Report: `data/reports/pre-launch-audit-2026-05-25.md`. Phase 1 cleanup pushed 3 commits during the audit (HEADER-POLISH `65458f6`, tooling `02668a6`, gitignore `ab3b537` — all above).
> - **Operational** — session recap doc commit `d0fcef4`; this Day 11 evening build-state sync (post-PRE-LAUNCH-AUDIT-1).

**Day 10 · 2026-05-24 — 2 numbered steps (Step 33 SYS-VERIFY-1 Phase 2 + Step 22 LEAD-2) (+ 5 non-counted closures)**
- Step 33 SYS-VERIFY-1 Phase 2 — final pre-launch verification gate, read-only audit across 6 categories (theme bundle health, critical page render + perf, SEO/AEO foundation, Shopify Admin state, critical functional checks, prior-work bug surface); **0 BLOCKER + 4 HIGH + 7 MED + 13 LOW** findings; GO/NO-GO recommendation: **GO** for LAUNCH-2 Monday. PSI on DEV deferred (preview gate blocks PSI bot — re-run after LAUNCH-2 flip). Report `data/reports/sys-verify-1-phase2-2026-05-24.md`. Commit `e3a260b`. Closes DO NEXT #1.
- Step 22 LEAD-2 — read-only lead-routing gap analysis across 5 entry-point surfaces (PDP add-to-cart/quote, Quote-page CTAs, the sitewide contact modal, OECM callouts, footer); **PASS** on in-theme routing; **GO** for LAUNCH-2. 3 findings: HIGH-1 (Steve verified the Notifications inbox routing ✅ closed 2026-05-24 — this was the lead-loss risk), HIGH-2 (no-JS modal fallback — judged not lead-loss, deferred post-launch), HIGH-3 (`product-form-buttons.liquid:30` stale `/pages/contact` CTA → Day 11 morning fix, ~30 min, DO NEXT #1). Report `data/reports/lead-routing-2026-05-24.md`. Commit `2d752ab`. Closes the LEAD-2 numbered step (was DO NEXT #6).

> **Also shipped Day 10 but NOT counted in the /54** (Step 36c is sub-work toward parent Step 36 BLOG-SEED-1, which stays 🟡 IN PROGRESS until 36d drafts Tuesday + 36e post-launch — so it does NOT move the /54). The count moved 41 → 43 on the two numbered steps closed today (Step 33 SYS-VERIFY-1 Phase 2 + Step 22 LEAD-2). The non-counted closures below — Cornerstone Post 1 (36c), PR-1's 5 fixes, PR-2's 2 fixes + sameAs rewrite, the `ds-article` CSS bug-fix bundle, and the post-launch monitoring docs — shipped as a single Day 10 block:
> - **Step 36c BLOG-SEED-1 / Cornerstone Post 1 — *OECM for Ontario School Boards: How to Procure Office Furniture Under Agreement 2025-470*** — article ID `689003888953`, handle `oecm-ontario-school-boards-office-furniture`, published 2026-05-23 20:45 ET via Shopify Admin API (`POST /admin/api/2026-04/blogs/108557861177/articles.json`); body updated 20:56 ET with AEO upgrade (3× `<caption>` + 9× `scope="col"`, per Leo post-publish review). Published immediately to LIVE per Leo HALT 3A decision. Live URL: `https://www.brantbusinessinteriors.com/blogs/news/oecm-ontario-school-boards-office-furniture` — HTTP 200, 3 HTML tables + 1 `<ol>` workflow + 30 mentions of "Agreement 2025-470" rendering on Avada theme today (Avada strips `<caption>` and `scope` at render — both attrs ARE stored in Shopify Admin body_html and will surface on LAUNCH-2 Monday when BBI `ds-article.liquid` renders unfiltered `{{ article.content }}`). Will switch to BBI `ds-article.liquid` rendering on LAUNCH-2 Monday at which point `BlogPosting` JSON-LD (lines 130-168, H-1 batch-fix from Day 9) starts emitting. 2,446 words / 16,600 chars; 3 comparison tables (Direct Award vs Open RFP, Eligible Buyer Sectors, Coverage Under 2025-470); 1 numbered 7-step procurement workflow with step/responsibility/output metadata for AI parsing; 6 procurement-actionable Q&As; 8 internal cross-links (`/pages/oecm` ×3, `/pages/quote` ×2, `/pages/education`, `/pages/design-services`, `/collections/seating`, `/collections/desks`). Excerpt 296 chars locking primary keyword "OECM Ontario school boards office furniture". Author Steve Katz. Tags: education, OECM, procurement, school boards. **No featured image** — Option A v1 fallback per HALT 0 critical safeguard (data/page-images/ is AI-generated per `project_ai_image_pipeline.md` memory; prompt hard-rule forbids AI photos in cornerstone procurement content; real photo added in follow-up edit after Sun EOD Upwork delivery + Step 46 IMAGE SWAP — article URL stays stable). DataForSEO MCP returned HTTP 403 — fell back to static KW targets in prompt CONTEXT (primary: "OECM Ontario school boards office furniture"; secondary: "OECM Agreement 2025-470 office furniture", "office furniture procurement Ontario school board", "OECM supplier school board"). Voice-rule audit clean: 0 literal "BBI" in customer copy, 0 forbidden lead-time commitments (only locked carry-overs from /pages/oecm — "one business day on most line-item quotes" and "around five business days" for design-layout quotes — both already site-locked), full "Brant Business Interiors" customer-facing throughout, "Brant Basics" cited in OECM legal-entity context, family-owned since 1964 + 296 George St N Peterborough HQ in closing section, locked microcopy "Request a Quote" + "Call 1-800-835-9565" used verbatim. All claims sourced from `ds-lp-oecm.liquid` + `page.oecm.json` + bbi-build-state Day 8 verified case studies (Halton Catholic DSB 320 ergoCentric task chairs across 11 schools / Agreement 2025-470 / 340+ POs across 90+ Ontario school boards-hospitals-municipalities / 12-yr ergoCentric mechanism warranty / 10-yr most other lines) — zero invented stats, zero fabricated comparisons. Draft archived `data/drafts/cornerstone-post-1-oecm-school-boards-v2.html`; payload `data/backups/articles/cornerstone-post-1-payload-20260523-204502.json`; API response `data/backups/articles/cornerstone-post-1-response-20260523-204502.json`. Closes DO NEXT #4.
> - **PR-1 `feature/serp-fix-and-schema`** — five-fix bundle (~90 min Claude Code session, 4 with writes + 1 SKIP after audit). All writes to DEV `186373570873` only — LIVE untouched.
>   - **SERP-FIX-1 (skip-link visibility):** added inline `<style>` block in `theme.liquid <head>` carrying the `.skip-to-content-link` visually-hidden pattern (off-screen by default, reveal on `:focus`/`:focus-visible`). Belt-and-suspenders guard: the same rule already exists in `bbi-homepage.css:546` but the inline copy makes off-screen behaviour load-order-independent so the link can never appear in Google sitelinks even if asset order changes. Pre-existing legacy redundant rules in `style.css` + `base.css` left untouched (out of scope).
>   - **SERP-FIX-2 (Office Central refs in BBI copy):** **SKIPPED** after HALT 0 audit. `grep theme/ "Office Central"` returned 35 matches; all 35 categorized as parent-company attribution per locked facts (5× schema `parentOrganization`, ~22× body copy "Part of the Office Central group", 2× footer "a division of Office Central Inc.", 1× About page H3 section header, 5× About page schema defaults). **Zero standalone customer-facing brand leaks** — Session B content polish (Day 8) handled this consistently. Zero file changes.
>   - **SCHEMA-LOCALBIZ-1 (LocalBusiness moved sitewide):** new `theme/snippets/bbi-localbusiness-schema.liquid` (58 lines) with DISTINCT `@id` `https://office-central-online.myshopify.com/#localbusiness` (intentionally different from `bbi-org-schema`'s combined `#organization` graph entity → no validator collision, two related-but-separate Schema.org nodes). Rendered sitewide via `theme.liquid` `{%- if bbi_landing -%}` body gate alongside `bbi-quote-modal`. Address/geo/hours/areaServed/priceRange/parentOrganization populated. **`sameAs: []` empty array with TODO comment** referencing Steve homework (LinkedIn + Facebook + Instagram canonical URLs — append once delivered). H-4 dedicated LocalBusiness block deleted from `ds-lp-contact.liquid` (`-36 / +1` lines) — sitewide snippet covers contact page too, no duplicate emission.
>   - **HIGH-2 (JSON-LD domain consistency — SYS-VERIFY-1 finding):** surgical 3-line domain edit across 2 files. Rule: `@id` entity identifiers keep `shop.permanent_domain` (Shopify canonical, stable across domain changes); user-facing `url` + `logo.url` use HARDCODED brand domain `https://www.brantbusinessinteriors.com` (pattern matches `ds-lp-quote.liquid:366` already in codebase). Changed: `bbi-org-schema.liquid:16` Org `url`, `bbi-org-schema.liquid:19` Org `logo.url`, `ds-article.liquid:156` BlogPosting publisher `logo.url`. All other emitters (`bbi-product-jsonld`, `bbi-breadcrumb-jsonld`, `ds-lp-delivery` Service, `ds-lp-relocation` Service, `ds-lp-quote` Service) already correct — verified.
>   - **HIGH-3 (duplicate Product JSON-LD — SYS-VERIFY-1 finding):** deleted lines 33-46 of `theme/snippets/meta-tags.liquid` (the `{% unless settings.seo_microdata %}{...}{% endunless %}` wrapper + Shopify auto-Product `{{ product | structured_data }}` emission). `settings.seo_microdata` is null on DEV → `unless null` evaluated true → Shopify auto-block fired alongside BBI's custom `bbi-product-jsonld.liquid`, producing duplicate Product emissions on every PDP. After deletion, BBI custom is sole Product schema source (richer: `additionalProperty` from specs metafields + `brand` + `mpn`). Theme-wide grep confirms only one active `application/ld+json` Product emitter remains. Matches SYS-VERIFY-1 Phase 2's own recommended fix.
>   - **shopify theme check:** ran post-edit on full theme — 265 files / 2855 offenses across 166 files (down from SYS-VERIFY-1 Phase 2 baseline of 264 files / 2856 offenses across 167 files: +1 file = new snippet, -1 offense = HIGH-3 wrapper removed). Zero new offenses on any of the 6 changed files. The 2 pre-existing warnings on changed files (`layout/theme.liquid` AssetPreload, `ds-article.liquid` HardcodedRoutes) are unchanged from baseline.
>   - **JSON validation:** simulated emit on all 3 JSON-LD blocks (new LocalBusiness snippet, edited Org+WebSite combined graph, edited BlogPosting block) — all parse cleanly. `@id` values stable: Org `#organization` and LocalBusiness `#localbusiness` are distinct fragments; publisher refs unify to Org.
> - **PR-2 `feature/quote-form-and-business-furniture-faqs`** — two-fix bundle + bonus comment edit (~60 min Claude Code session). All writes to DEV `186373570873` only — LIVE untouched.
>   - **HIGH-1 (Quote→Contact form gap closed):** 2-line default-string flip in `theme/sections/ds-lp-quote.liquid:402,403` — `_cta_url` + `_form_url` defaults changed from `/pages/contact` to `/pages/quote`. **Key discovery during HALT 0 investigation:** `theme/snippets/bbi-quote-modal.liquid` (shipped sitewide via `theme.liquid:170` inside `bbi_landing` gate) has a global `document.addEventListener('click', ...)` handler at lines 455-466 that intercepts ALL `<a href*="/pages/quote">` clicks and opens the existing dialog-form contact modal with lead_type context. The Quote page's CTAs were defaulting to `/pages/contact` (which has no `<form>` per HIGH-1 finding) instead of using the sitewide modal trigger pattern. By flipping the defaults to `/pages/quote`, all 4 CTAs on the Quote page now trigger the modal: hero "Request a Quote" (line 428), Online quote form channel (line 517 — the original HIGH-1 finding), OECM callout "Request an OECM Quote" (line 563), and closer "Request a Quote" (line 764). No new JS, no new HTML, no template change — purely re-points existing wiring through the already-built modal infrastructure. Graceful no-JS fallback: href stays valid (`/pages/quote` is the page they're already on; click reloads, doesn't 404).
>   - **HIGH-4 (business-furniture parent FAQs added):** 4 `faq_item` blocks appended to `theme/templates/collection.business-furniture.json` (blocks map + block_order). Q&As are parent-collection scoped (cross-category procurement), distinct from the 5 seating-specific FAQs on `/collections/seating`: (1) "Can I order across every business furniture category under OECM Agreement 2025-470?" (full-catalog OECM coverage), (2) "How do I request a single quote that spans multiple product categories?" (multi-category quote workflow + single PO routing), (3) "What's included in delivery and installation for a multi-category office fit-out?" (fit-out-level install scope with after-hours hedging "can typically be arranged…ask during quoting" per icp.md #8 lead-time hedging rule), (4) "Do you offer space planning for a full office fit-out across categories?" (parent-level free space planning + link to `/pages/design-services`). FAQPage JSON-LD auto-emits via `ds-cc-base.liquid:530-547` (`cc_faq_blocks.size > 0` ⇒ true with 4 blocks); accordion renders via `ds-cc-base.liquid:933-973` below the OECM bar with first FAQ auto-open. No section file changes — pure template metafield addition mirroring AI-9 pattern. Simulated JSON-LD parses cleanly with 4 Question entities; JSON template validates (13 blocks total, 13 in block_order, 4 faq_item).
>   - **sameAs TODO rewrite (bonus, per Steve update 2026-05-24):** updated comment block in `theme/snippets/bbi-localbusiness-schema.liquid:15-20` from the Steve-homework TODO (LinkedIn + Facebook + Instagram URLs pending delivery) to a documented intentional-empty rationale: *"sameAs intentionally empty: BBI has no current LinkedIn/Facebook/Instagram presence (confirmed Steve 2026-05-24). When social profiles launch, append URLs here."* `sameAs: []` array unchanged (PR-1 already had it empty). Steve homework item removed from STEVE HOMEWORK section above + moved to resolved-items record.
>   - **shopify theme check:** ran post-edit on full theme — 265 files / 2855 offenses across 166 files (IDENTICAL to PR-1 baseline). **Zero new offenses on any of the 3 changed files.** `ds-lp-quote.liquid` has 2 pre-existing warnings (HardcodedRoutes, VariableName) unchanged from PR-1; `bbi-localbusiness-schema.liquid` and `collection.business-furniture.json` have zero offenses.
>   - **Push verification:** all 3 files HTTP 200 to DEV `186373570873` (`bbi-push-landing.py --slug quote` for ds-lp-quote.liquid + page.quote.json; `push-file.py` for the collection template and localbusiness snippet). Updated_at timestamps recorded.
> - **Step 36c follow-up — `ds-article.liquid` CSS bug-fix bundle** — 2 visual fixes on the new BBI article template (DEV theme `186373570873` only, LIVE untouched), surfaced when Leo eyeballed Cornerstone Post 1 on the DEV preview:
>   - **Table styling (Bug-Fix A):** `.article-prose` had zero `<table>` CSS — comparison tables rendered with browser-default no borders. Added ~17 lines of new prose CSS: border-collapse table reset, `.article-prose__table-wrap` overflow scroll for mobile, `<caption>` styling (JetBrains Mono uppercase eyebrow caption-side: top), `<thead>` `#FAFAFA` bg, `<th>` 2px solid `#0B0B0C` bottom-border + Inter Tight heading font, `<td>` 1px `#E5E5E7` row separators, last-row no-border, zebra striping on even rows (`rgba(11,11,12,0.015)`), inline-link underline on `td a`, mobile `<th>/<td>` padding compression below 640px.
>   - **CTA button visibility (Bug-Fix B):** `.article-cta__btn` `<a>` was rendering invisibly on DEV — root cause `theme/assets/base.css:122` global `a { color: rgb(var(--linkColor)) }` uses `rgb()` with a hex value (invalid CSS — rgb() expects three space-separated numbers, not a hex), causing descendant `<a>` color to drop to canvas-default on some renders + button bg failing to apply. Hardened `.article-cta__btn` + `:hover` with explicit hex fallbacks: `background: #0B0B0C !important` + `background: var(--buttonBackground, #0B0B0C) !important` (double-declaration pattern — older browsers ignore the var() line, modern browsers honour the cascading `!important`), `color: #FFFFFF !important` + `var(--buttonColor, #FFFFFF) !important`, `border-color: var(--buttonBorder, #0B0B0C)`, `border-radius: var(--buttonRadius, 4px)`, `font-family: var(--bodyFont), "Inter", system-ui, sans-serif`, font-size + letter-spacing fallbacks, `text-decoration: none !important`, and hover-state fallbacks for `#D4252A` sale-red bg.
>   - **Article body AEO upgrade (also shipped):** updated `article.body_html` via Shopify Admin API PUT (article ID `689003888953`, body length 20,209 → 20,634 chars) to add **3× `<caption>`** ("Procurement path comparison — OECM Direct Award (Agreement 2025-470) vs Open RFP", "OECM Agreement 2025-470 — eligible buyer sectors in Ontario's broader public sector", "Coverage matrix — what's included under OECM Agreement 2025-470 and what sits outside it") + **9× `scope="col"`** on every `<th>` (3 tables × 3 columns). Captions = explicit AEO context tags; scope = a11y + AI-parser disambiguation. Avada theme today strips both at render (verified via fetch — `<caption>` count 0 on LIVE URL despite Admin API confirming 3 stored). Both surface on LAUNCH-2 Monday when BBI `ds-article.liquid` renders unfiltered `{{ article.content }}`.
>   - **Push:** `sections/ds-article.liquid` HTTP 200 to DEV `186373570873`, updated_at 2026-05-23 20:55:49 ET. Admin API confirms new CSS rules present in pushed asset (table styling + caption styling + thead bg + th borders + td zebra + button hex fallbacks for bg, color, hover — all 8 grep checks ✅). `shopify theme check` clean on `ds-article.liquid` (only pre-existing `HardcodedRoutes` warning from prior baseline — unchanged).
>   - **Diff stat:** `theme/sections/ds-article.liquid` +22 / -2 lines · `data/drafts/cornerstone-post-1-oecm-school-boards-v2.html` +13 / -7 lines (mirror updates of the captions + scope attrs on the archived draft).
> - **Post-launch monitoring deliverables** — `docs/plan/post-launch-monitoring.md` (the monitoring playbook), `docs/plan/ga4-conversion-setup.md` (10-min GA4 conversion-tracking walkthrough), and `docs/reports/weekly-launch-monitor-template.md` (weekly monitor report template). Activates at LAUNCH-4 (DO NEXT #13).
> - Operational: build-state.md updated + Day 10 EOD synced to tracker.

**Day 9 · 2026-05-23 — 1 numbered step (+ 5 non-counted closures)**
- Step 26 INTERLINK-3 — final cross-link audit; 623 internal links across 75 theme files (31 sections + 9 snippets + 35 JSON templates) validated against the live Shopify Admin API (388 collection + 23 page handles all PUB); **1 FAIL fixed** (`ds-cs-base.liquid:593` Brantford local `tel:+15198371810` → toll-free `tel:+18008359565`, matches locked sitewide phone fact); 89 WARN (tel: `+1`-prefix consistency, deferred post-launch); 18 INFO (15 HIGH + 3 LOW body-level cross-links, surfaced for review); **0 broken `/pages/*` or `/collections/*` — hard gate CLEAR for LAUNCH-2**; all writes to DEV `186373570873` only; branch `feature/interlink-3` · PR #17 → 28a2450 · report `data/reports/interlink-3-audit-2026-05-23.md`

> **Also shipped Day 9 but NOT counted in the /54** (so the count moved 40 → 41, not 46):
> - **bbi-quote-modal.liquid cleanup** — pre-existing change finally committed (`4d48187`); working tree clean for the first time since Day 1.
> - **W0-3 PRODUCT-REDIRECTS verified** — 171/173 (98.8%) live in Shopify Admin; 2 minor edge cases non-blocking; effectively done (Wave D sub-step, not a numbered step).
> - **W0-1 GSC + GA4** — Steve completed 2026-05-22: GA4 property `G-XLCM9LCNLN`, GSC domain property `brantbusinessinteriors.com`, GSC↔GA4 link created (1,488 queries already tracking), Leo added as GA4 Admin; Google Merchant Center + Google Business Profile both already connected (Wave D sub-step, not a numbered step).
> - **Step 36a BlogPosting JSON-LD** on `ds-article.liquid` — ✅ via the schema batch-fix H-1 (Step 36 stays open as a numbered step until 36c+36d ship Day 10).
> - **Step 36b Sitewide schema audit** — `data/reports/schema-audit-2026-05-23.md` surfaced 4 HIGH + 3 MED + 3 LOW gaps + 3 validation issues (commit `477a50d`); scope-set the batch-fix that followed.
> - **Schema batch-fix** — PR #16 → 9d132f3 (5 commits across two branches: `e05e036` W0-1 housekeeping + `c7cdb20` 5 HIGH schema fixes): closed 4 HIGH gaps (H-1 BlogPosting · H-2 WebSite+SearchAction · H-3 Service on delivery+relocation · H-4 LocalBusiness on contact) + 1 validation (V-1 broken Article block deleted) + 2 bonus residual fixes (founding year 1982→1964 + structural `foundingDate`, and a 6-location operating-hours sweep to 9–5 ET per Steve's canonical confirmation); V-2 verified by Leo — Shopify "Add structured data automatically" toggle NOT present in store, no collision risk.
> - Operational: tracker + build-state Day 9 EOD update (this session).

**Day 8 · 2026-05-21 — 5 items**
- Step 19 AI-9 — FAQ blocks + FAQPage JSON-LD on 9 category collection pages. 36 procurement-actionable Q&As across Seating (5) + Desks/Storage/Tables/Boardroom/Accessories/Ergonomic/Quiet Spaces (4 each) + Panels & Room Dividers (3). Pattern centralized in `ds-cc-base.liquid` (FAQ render + accordion JS + auto-built FAQPage JSON-LD from `faq_item` blocks); per-collection JSON templates add `faq_item` blocks. Schema differentiator vs ugoburo (zero JSON-LD anywhere). Commit 4f2aafe · PR #11 → d5800da.
- Step 20 AI-5 — FAQPage JSON-LD on /pages/design-services **verified, no writes** — Session B already shipped both the `HowTo` and `FAQPage` JSON-LD blocks in `ds-lp-design-services.liquid` (lines 14–42) alongside 5 `faq_item` blocks in `page.design-services.json` (commit 6c33b60). Simulated emit parses cleanly (5 valid Q&As). OECM no-regression confirmed: deployed `ds-lp-oecm.liquid` FAQPage block intact at lines 322–334, `page.oecm.json` 8 `faq_item` blocks, simulated emit parses cleanly. Blog: 1 published article (_How to adjust your chair_) currently emits no `BlogPosting` JSON-LD — gap deferred to BLOG-SEED-1 (Step 36) per scope. Branch `feature/ai-5` · PR #12 → 1df3cff.
- Step 54 CONTENT-POLISH-1 — Session A + B complete (13 pages refreshed total); Session B shipped 7 service + adjacent pages (quote, delivery, design-services, relocation, customer-stories, our-work, faq); commit 6c33b60 · merged via PR #10 to main (merge commit 24ade31)
- Step 55 STEVE-FACT-CHECK — ✅ Resolved; 3 claims verified (proof-bar "340+ OECM POs / 90+ Ontario buyers" numbers · entity-name rule Brant Basics ↔ Brant Business Interiors · ownership framing Ontario-owned vs family-owned); LAUNCH-2 unblocked on this vector
- Step 34 CONTENT-1 — ✅ Done; logo locked to `bbi-logo-v2` at BRAND-PAGES-1 (commit 70c242c); no new wordmark sourcing

> **Also shipped Day 8 but NOT counted in the /54** (so the count moved 38 → 40, not 42):
> - **Step 50 A11Y-AUDIT-1 Phase 1.5** — PSI re-run on LIVE Avada (15 URLs × 2 strategies, all 4 Lighthouse categories, authenticated PSI API key). Read-only; no theme writes. **Result:** mobile P 58 / A 98 / BP 93 / SEO 95 · desktop P 83 / A 95 / BP 94 / SEO 95. **No regressions from Wave E** (content + schema shipped on dev theme only, not on LIVE). Mobile LCP still red on 15/15 URLs (Avada page-builder bloat); CLS clean 30/30. Three a11y binary audits fail across most pages — `heading-order` 26/30, `target-size` 15/30, `color-contrast` 4/30 — worth confirming on new theme. Outputs: `data/reports/a11y-audit-1-phase-1.5-2026-05-21.{csv,md}` · PR #13 → b0e29b4. *(Upgrade to already-counted Step 50 — authoritative new-theme re-baseline gated by Phase 2 post-LAUNCH-2.)*
> - **Task #12 DEV-3** — search.json + 7 customers/* templates migrated into `bbi_landing` gate (closes A11Y Fix E + a latent launch gap) · branch `feature/dev-3-task-12` · PR #14 → 5ec8f19. *(Sub-work, not a numbered launch step.)*
> - **Homepage bug fix + polish round** — PR #15 merged `766e555` · branch `feature/homepage-bug-fix` (2 commits `e6bc89a` + `6e3f983`) · 14 broken `bbi-hp-*.jpg` refs → safe design-system placeholders + hero H1 trim + "Who we are" full-width + secondary button outlines + 6 design-system color accents · homepage no longer shows broken images · closes the cosmetic aspect of **Task #13** (Day 9 swaps placeholders for real stock images, slots + aspect ratios preserved). DEV theme `186373570873` in sync with main. *(Task #13 is a post-launch backlog item — does NOT increment the /54.)*
> - Operational: build-state.md restructure committed (commit 45cad41) + mid-day audit (commit 59a7eec); PR-MERGE-3 — PR #10 merged as merge commit 24ade31.

**Day 6 · 2026-05-20 — 9 items**
- Step 17 AI-7 — homepage entity-clarity copy (Version B plainspoken); commit 17da6cc
- Step 18 AI-8 — OECM page hardening (Version A); 177-product Coverage Table + 8 procurement FAQs; commit 17da6cc
- Step 25 BRAND-PAGES-1 — 3 new brand pages + 15 smart collections + nav/footer/hub; commit 70c242c (22 files)
- Step 47 SYS-VERIFY-1 Phase 1 — read-only audit of 8 system surfaces; commit 52417c8
- Step 48 POLICY-PAGES-AUDIT — policy content gap audit (4 wrong-entity findings); commit d81c0e8
- Step 49 POLICY-WRITE-1 — rewrote all 4 policies + Shopify contact to Brant Business Interiors
- Step 50 A11Y-AUDIT-1 Phase 1 — 🟡 baseline; Fix D applied, A/B/C no-ops; commit 64a567c
- Step 51 SYS-VERIFY-CLEANUP-1 — 8 findings; 15 LIVE pages unpublished, 40 redirect changes; commit 8d66860
- Step 52 S4-CONTACT-FIX — address 295→296 across 6 files + contact map embed; commit a59a774

**Day 4 · 2026-05-15 — 5 items**
- Step 16 PAGE-IMG-1 — filled hero/sub-hero slots, 99 ops across 28 templates; commit be1409d
- Step 42 CATALOG-NAV-INVESTIGATION — 5-area navigability audit; commits 8e0de9a + f8f9b09
- Step 43 TYPE-APPLY-1 — type:* coverage 68%→94.9%; commit 52cd8d7
- Step 44 CATEGORY-TILE-FIX-1 — fixed sub-category tiles across 9 templates; commit 5c29b13
- Step 45 TILE-CLEANUP-1 — removed remaining 0-count tiles; commit 1eaafc8

**Day 3 · 2026-05-14 — 7 items**
- Step 3 BUG-FIX-3 — OECM + industry tag remediation; 584 oecm-eligible; commit 1ddbe05 (closes Phase 1)
- Step 21 LEAD-INBOX-1 — provisioned quotes@/design@/info@ aliases; SPF/DKIM/DMARC; test emails confirmed; commit b6a6855
- Step 23 LEAD-3 — per-type lead routing + auto-replies (Option D); commits df105af, 1be5ca5, e9cb497
- Step 24 COMP-SCRAPE-1 — ugoburo.ca competitor audit (unlocked AI-7/8)
- Step 27 NAV-VERIFY — homepage + collections render shared nav; 62 links; commit 3aa74c3
- Step 28 DS-VERIFY — design-system screenshot diff; 97 sections inventoried; commit f38d2d0
- Step 32 LINK-ROT-1 — 94 URLs swept, 1 dead fixed; commits 589bcff + b779f3e

**Day 2 · 2026-05-13 — 11 items**
- Step 2 BUG-FIX-2 — OECM tag mass-application investigation; commit cc7c31c
- Step 6 TAG-INDUSTRY-CHECK — industry:* tag investigation (retire)
- Step 7 BUG-FIX-4 — uploaded 48 OCI photos + fixed Our Work page
- Step 8 PE-PASS-3 — ran remaining enrichment batches (~82 products)
- Step 9 PE-PASS-3-REVIEW — review xlsx + live-pushed approvals
- Step 10 CANONICAL-MAP-ADDITIONS — +10 brand entries; commit 29bcbad
- Step 11 APPLY-MAP-ADDITIONS — re-tagged 14 products; commit 66a0bff
- Step 12 COLLECTION-AUDIT — audited 371 collections (read-only); commit a24b9e3
- Step 13 COLLECTION-CLEANUP-APPLY — 164 collections unpublished + redirects; commit 737f6f6
- Step 14 BRAND-CALLOUT-AUDIT — fixed brand callouts on category pages; commit 326241f
- Step 15 PROMPT-5 — image slot audit (read-only)

**Day 1 · 2026-05-12 — 3 items**
- Step 1 VENDOR-NORMALIZE-1 — built canonical brand vocabulary
- Step 4 VENDOR-NORMALIZE-2 — applied canonical brands to 152 products
- Step 5 TAG-AUDIT-1 — audited all tag prefixes

---

## 📦 POST-LAUNCH BACKLOG (expanded)

None of this blocks the Monday launch — it compounds after BBI is live. The pre-launch-critical slices of W0-2 (hours, pin, photos) live in the DO NEXT queue; everything else (full GBP, citations, reviews) lives here. (The historical pre-restructure backlog is preserved verbatim below the divider.)

**LAUNCH-3 Week 1 polish backlog (2026-05-26) — added at LAUNCH-3 closure:**
- **GA4-QUOTE-EVENT** — wire a `generate_lead` GA4 event on `/pages/quote` form submit (and on the sitewide quote-modal submit path). ~30 min Claude Code work in `ds-lp-quote.liquid` + the modal handler snippet; uses the existing `G-XLCM9LCNLN` web stream (Web Pixels already shows `view_item` + `page_view` + `scroll` firing as of LAUNCH-3 verification, so `gtag('event', 'generate_lead', ...)` will surface cleanly in GA4 Events without any property reconfig). Mark `generate_lead` as a Key Event in GA4 Admin → Events once first event lands so it shows up in Acquisition reports.
- **LEAD-WORKFLOW-REVIEW** — ~30 min Leo + Steve conversation, gated on ~1 week of `generate_lead` volume from the event above. Evaluate Klaviyo vs HubSpot vs Notion vs email-only based on real lead volume + Steve's bandwidth (single-inbox routing via HIGH-1 is working today; per-type / CRM-grade routing is the question). Output: a one-pager picking the tool + an integration plan if not email-only.

**Day 10 discoveries (2026-05-24) — 5 new items added this session:**
- **DATAFORSEO-403 ✅ RESOLVED 2026-05-26 evening** — the DataForSEO MCP returned HTTP 403 during Cornerstone Post 1 drafting (fell back to static keyword targets). Needs a subscription/config fix; SEO-AUDIT-1 is hard-gated on this MCP per `CLAUDE.md`, so this blocks SEO-AUDIT-1. ~30 min triage. **Unblock 2026-05-26 evening:** `.mcp.json` credentials live-verified via `mcp__dataforseo-mcp__dataforseo_labs_google_keyword_overview` test call ("office furniture toronto" → 480/mo, HIGH competition, CA). **SEO-AUDIT-1 is now READY to run as the pre-launch hard gate before LAUNCH-0.**
- **STALE-OECM-DATE-FIX** — `theme/sections/ds-lp-about.liquid:113` body copy and `:245` schema textarea default still say *"OECM Supplier Partner since 2019"*. Canonical fact is **Agreement 2025-470** (locked Day 8 STEVE-FACT-CHECK), contradicting the Agreement-number framing applied across `ds-lp-oecm` + all 5 industry pages in CONTENT-POLISH-1 Session A. Two edits, ~5 min. Surfaced during the PR-1 FIX 2 audit.
- **LEAD-HIGH-2 — no-JS modal fallback** ✅ **DONE 2026-05-26 (commit pending)** — converted all `data-bbi-quote-trigger` `<button>` elements to `<a href="/pages/quote">` across 6 files (8 buttons — audit header said "9" but body listed 8, code confirmed 8). Progressive enhancement: JS-enabled users still get the modal (modal handler calls `preventDefault()` on both trigger-class and anchor-class paths); JS-disabled users + crawlers + right-click "Open in new tab" now reach `/pages/quote` (a real form). PDP primary trigger preserves product context in URL params (`?product=<handle>&title=<title>`). DEV theme 186373570873 only — LIVE untouched. theme-check baseline 2855 unchanged.
- **CORNERSTONE-1-IMG** — Cornerstone Post 1 has NO featured image (AI-photo hard-rule + no real photo yet). Swap in a real photo Tuesday, after the Upwork delivery + Step 46 IMAGE SWAP. Article URL stays stable.
- **LEAD-INBOX-1 per-type routing** — single-inbox routing works today (verified via HIGH-1); per-type routing (quotes@ / design@ / info@ → distinct destinations) is an optimization, not a launch blocker.

**GBP completion (deferred from pre-launch W0-2):**
- W0-2-AREAS — 13 Ontario service areas
- W0-2-ATTR — attributes: family-owned, wheelchair accessible, accepts POs
- W0-2-SOCIAL — link LinkedIn / Facebook / Instagram
- W0-2-QA — 8 Q&A seeded
- W0-2-POSTS-1 — first 4 Google Posts
- W0-2-POSTS-RECUR — weekly Google Posts cadence
- W0-2-VERIFY — services + products audit

**Cross-channel citations (W0-CITATIONS):**
- W0-CIT-BING — Bing Places
- W0-CIT-APPLE — Apple Maps
- W0-CIT-LINKEDIN — company page
- W0-CIT-YELP — Yelp Canada
- W0-CIT-BBB — BBB listing

**Reviews seeding (W0-2b full workstream):**
- W0-2b-DOC, W0-2b-LIST, W0-2b-LINK, W0-2b-WEEK1, W0-2b-WEEK2, W0-2b-AUTO, W0-2b-RESPOND

**Duplicate-suspension monitoring:**
- W0-2c-MONITOR — weekly Monday incognito search

**Schema + content backlog:**
- AI-10 — spec completeness audit
- AI-11 — "best of" / comparison content
- Step 36e Cornerstone Post 3 (*Cubicle vs Open-Plan for Municipal Offices*) — every post starts with DataForSEO keyword research
- Font tokens follow-up — homepage Avada residuals (`--headingFont`, `--bodyFont`, hardcoded JetBrains Mono); load DS tokens globally OR define `--bbi-font-*` locally in `bbi-homepage.css`
- INTERLINK-3 — 15 HIGH + 3 LOW INFO findings (most notable: 6 brand pages missing a body link to the `/pages/brands` hub; `/pages/design-services` missing a CTA to `/pages/quote`) — awaits a Leo pre/post-launch call
- INTERLINK-3 — 89 WARN: tel: `+1`-prefix sweep (cosmetic, browser-tolerant)

**Phase 2 audits (post-LAUNCH-2):**
- Step 30 PERF-AUDIT-1 Phase 2 — Lighthouse + CWV re-baseline against the new theme (target mobile ≥80)
- Step 31 A11Y-AUDIT-1 Phase 2 — authoritative WCAG 2.1 AA re-baseline
- Step 35 SEO-AUDIT-1 — pre-launch SEO hard gate ✅ 2026-05-26 evening — 0 BLOCK / 15 FIX (all in-scope FIXes applied via Claude Code Admin API, zero Steve work) / 3 WAIVE → READY FOR LAUNCH-0; report `data/reports/seo-audit-1-2026-05-26.md`

**Catalog · blog · future waves (carried forward):**
- Phase 1b full catalog — PE-5/6/7 for the remaining 503 non-Hero products (descriptions, specs, meta)
- Blog B4–B10 — weekly cadence after the BLOG-SEED-1 cornerstone posts · every post starts with DataForSEO keyword research
- SEO-AUDIT-2 — site-wide keyword audit + cannibalization fix · output `docs/strategy/bbi-keyword-map.md`
- Smart collections — finish migration on remaining manual collections
- Wave 2 — Acoustic Pods sub-collection · sit-stand buyer guide · hybrid work bundle
- Wave 3 — City-level SEO · ergonomics hub · sustainability / LEED page · manufacturer dealer locator pages
- W0-6 — parent-domain backlinks (officecentral.com, brantbasics.com)
- W0-7 — surface OECM + "Since 1964" trust signals site-wide (likely folds into Step 46 image/branding work)
- Task #13 homepage image rot — cosmetic ✅ resolved 2026-05-21 (PR #15 → 766e555); real image swap folds into Step 46 / #14
- Ideas backlog — see `docs/plan/ideas-backlog.md`

---

> ═══════════════════════════════════════════════════════════════════════
> **EVERYTHING BELOW THIS LINE IS PRESERVED VERBATIM** from the prior
> `bbi-build-state.md` — the canonical session log, ⛔ Hard Rules + Safety
> Rules, Lessons Learned, Known Data Hygiene Issues, the full Wave A–H
> tables, the post-launch Backlog, and all reference sections. The
> navigation layer above is the dashboard view; the record below is the
> source detail. (One surgical annotation was added to the Wave E
> `IMG-PHASE2` row pointing to the CURRENT FOCUS / ACTIVE STEPS image-scope
> note above; nothing was removed.)
> ═══════════════════════════════════════════════════════════════════════

---

**Last updated:** 2026-05-21 (CONTENT-POLISH-1 Session B COMPLETE — 7 service + adjacent pages refreshed (quote + delivery + design-services + relocation + customer-stories + our-work + faq) with AI-7/AI-8 voice patterns + Session A layout standardization · 4× literal-`BBI`-in-customer-copy violations fixed (delivery, relocation FAQ, customer-stories case+testimonial, faq Q391) · 3× wrapper-class rename from `.bbi-lp-*` to `.lp-*` short form (quote, design-services, faq) · Quote page: NEW 6-item Quote intake checklist + NEW Browse + NEW How-to-Purchase 3-step + NEW Top Products + NEW Entity note + 6 FAQs (added lead-time Q) · 5 service pages get Session A canonical modules · Customer-stories: Mattamy unverified card replaced with Halton Catholic DSB verified case (320 chairs / 11 schools / OECM 2025-470) + 2 placeholder cards (Healthcare + Pro Services) for Steve case-study completion · Our-Work: 2× Mattamy unverified mentions anonymized to "Corporate boardroom · GTA" + Ontario-owned framing · FAQ: NEW Brand Portfolio group (2 Qs) + entity-clarity hero lede · Ownership framing applied per locked rules (quote/our-work=Ontario-owned, delivery/design-services/relocation/customer-stories=family-owned, faq=both) · branch feature/content-polish-1-session-b from main · Day 8 Step 54 closing — Session A + Session B both complete)
**Prior session 2026-05-21:** (CONTENT-POLISH-1 Session A COMPLETE — 6 industry pages refreshed (industries hub + healthcare + education + government + non-profit + professional-services) with AI-7/AI-8 voice patterns · NEW Entity-clarity section · NEW Coverage Table (5 OECM-heavy pages) · NEW How-to-Purchase 3-step (5 OECM-heavy pages) · NEW Entity note · NEW Top Products 4-card grid (all 6 pages) · 5× proof-bar factual fix (2019→2025-470) · Pro-Svc since-1982→1964 fix · Pro-Svc Keilhauer→storefront-callable rebrand · 39 procurement-actionable FAQs replacing 30 generic · Browse-categories crosslinks repositioned between Intro and Who-we-are on all 5 industry pages · Industries hub Browse-catalogue repositioned · Layout standardization (intro 880→1280px, full-width heads + body copy on entity/coverage/howto sections, glance dl spacing fixed, hero badge CSS scoped to .lp-hc/.lp-edu/.lp-gov/.lp-np/.lp-ps) · branch feature/content-polish-1-session-a from main)
**Prior session 2026-05-20:** AI-7 + AI-8 COMPLETE — homepage entity-clarity copy (new bbi-about section + bbi-hero refresh; Version B plainspoken) · OECM page hardening (new Coverage Table section · new How-to-Purchase 3-step · new Entity note · 3 factual errors fixed · 8 procurement-focused FAQs · hero settings refreshed; Version A comprehensive) · branch feature/ai-7-ai-8 stacked on feature/brand-pages-1
**Prior session 2026-05-20:** BRAND-PAGES-1 + A11Y bundle COMPLETE — 3 new brand pages (OTG, Heartwood, ObusForme) via Approach A clone · Global/Teknion rescoped to GFG-family per Option A · 15 brand×category smart collections live + populated (177 product memberships) · Brands hub updated to 6 tiles · nav menu (desktop + mobile) + footer Brands column (new 5th col) + homepage meta description + about page + Phase 5 Fix D (duplicate role="main" removed) · branch feature/brand-pages-1
**Dev theme:** BBI Landing Dev (`186373570873`) — never publish to live until LAUNCH-2
**Live theme:** brantbusinessinteriors.com (production — untouched)
**Replaces:** the status sections in `shopify-fix-plan.md` and the localStorage-bound `SEEDS` in `website-fix-checklist.html`

**2026-05-21 — CONTENT-POLISH-1 Session B COMPLETE (Claude Code session).** Followed the CONTENT-POLISH-1 Session B multi-halt prompt (`/Users/leokatz/Downloads/prompt-content-polish-1-session-b.md`). Branched `feature/content-polish-1-session-b` from main (NOT stacked on Session A — Session A merged via PR #9 first). Refreshed all 7 service + adjacent pages: **Quote (Version B buyer-friendly per HALT 2A pick):** wrapper rename `.bbi-lp-quote` → `.lp-quote`; entity-clarity opener in intro naming Brant Basics as OECM-registered legal entity; NEW 6-item Quote intake checklist (Scope / Floor plan / OECM membership / PO routing / Lead-time window / Existing furniture); NEW Browse-categories crosslinks; NEW How-to-Purchase 3-step framed for quote intake; NEW Top Products 4-card grid; NEW Entity note; 6 FAQs (added "What's your typical lead time?"); diff card 03 Canadian-owned → Ontario-owned; proof bar + closer reframed to Ontario-owned per locked rule. **Delivery (single draft):** fixed "Why BBI delivery" violation; hero rewrite leads with own crew + Ontario + Western Canada + after-hours/weekend + family-owned since 1964; intro entity-clarity opener; NEW Browse + How-to-Purchase 3-step + Top Products + Entity note; diff cards 01/02/04 rewritten for own-crew/after-hours/Western-Canada; 2 NEW FAQs (after-hours installs + Western Canada install coverage). **Design Services:** wrapper rename `.bbi-lp-design-services` → `.lp-ds`; hero standfirst swap Canadian-owned → family-owned + Brant Basics OECM mention; NEW intro para 3 entity-clarity opener; NEW Browse + How-to-Purchase 3-step + Top Products + Entity note. **Relocation (single draft):** hero rewrite leads with project-management framing + family-owned + multi-site specialty; intro entity-clarity opener; fixed FAQ violation "BBI-sourced furniture" → "furniture we originally supplied"; NEW Browse + Top Products + Entity note; 2 NEW FAQs (multi-site sequencing + after-hours/weekend moves); existing 4-phase Process section kept as how-to equivalent. **Customer-Stories (per HALT 4A decision — keep Halton + 2 placeholders for Steve):** replaced Mattamy unverified card with Halton Catholic DSB verified case (320 ergoCentric chairs · 11 schools · OECM Agreement 2025-470 — pulled from homepage `bbi-work` verified data); kept Kawartha Dairy (verified via homepage testimonial); kept generic Ontario Municipal (anonymized, no fabrication); added 2 placeholder cards (Healthcare + Pro Services) labeled "case study pending verification" with image picker slots for Steve to complete; fixed 2 BBI violations (case summary + testimonial blockquote); added Entity note; tightened OECM bar (Brant Basics-led copy). **Our-Work:** removed 2 unverified Mattamy Homes references (page-head sub copy + 2 photo captions) anonymized to "Corporate boardroom · GTA" + "Open-plan multi-office floor · GTA"; H1 + sub now lead with Ontario-owned since 1964 (institutional-projects framing per prompt); added Browse-crosslinks + Entity note (inline-styled to match existing compressed CSS convention); closer reframed to Ontario-owned; schema labels updated. **FAQ:** wrapper rename `.bbi-lp-faq` → `.lp-faq`; fixed Q391 "BBI furniture" violation → "your furniture"; hero lede now opens with entity-clarity (family-owned since 1964 + Brant Basics ↔ BBI relationship); NEW Brand Portfolio group (2 procurement-relevant Qs: "Which brands do you carry?" + "Which brands are eligible under OECM 2025-470?"); Entity note added before footer; total 21 FAQs across 6 groups. **Standardization summary across all 7 pages:** Session A canonical modules applied where appropriate (Browse-crosslinks on all 7, How-to-Purchase 3-step on 3 service pages + quote, Top Products 4-card grid on 4 pages, Entity note on all 7, OECM treatment consistent); intro container widths normalized 880→1280px; hero badge CSS scoping where missing; wrapper class names normalized to `.lp-{short}` canonical pattern. All writes to DEV `186373570873` only — LIVE untouched. Pre-existing `bbi-quote-modal.liquid` uncommitted change preserved untouched per prompt rule. Untracked `snippets/` folder at repo root and 3 untracked data-strategy files left untouched (not Session B scope). Branch `feature/content-polish-1-session-b` ready for PR + merge. shopify theme check: pre-existing underscore-variable warnings on quote page (unchanged from prior session); no new errors introduced. Closes CONTENT-POLISH-1 (Session A + B together = 13 pages refreshed across both Days 7-8).

**2026-05-21 — CONTENT-POLISH-1 Session A COMPLETE (Claude Code session).** Followed the CONTENT-POLISH-1 Session A multi-halt prompt (`/Users/leokatz/Downloads/prompt-content-polish-1-session-a.md`). Branched `feature/content-polish-1-session-a` from main. Refreshed all 6 industry pages with AI-7/AI-8 voice patterns: industries hub (Version B buyer-pattern-first hero), healthcare (Version A clinical/compliance-first per locked feedback memory `feedback_healthcare_tone.md`), education (Version B use-case-first per Steve's call at HALT 3A), government (single procurement-officer-led draft), non-profit (single budget-conscious draft), professional-services (single private-sector draft, NO OECM/Coverage/How-to-Purchase modules per private-sector framing). **Surgical edits per page:** NEW Entity-clarity section (AI-7 Version B voice; 3 paragraphs naming Brant Basics ↔ BBI entity relationship + 296 George St N HQ + GFG/OTG/Heartwood/ObusForme + 25 more lines + buyer split + ON+Western install + glance dl); NEW Coverage Table (5 OECM-heavy pages; same 177-product table from /pages/oecm with per-industry framing line); NEW How-to-Purchase 3-step (5 OECM-heavy pages; per-industry Step 03 emphasis — healthcare W5-cleared installers, education summer windows, government audit-trail billing, non-profit volunteer-staffed delivery); NEW Entity note (all 6 pages; same disclosure line below proof bar); NEW Top Products 4-card grid (all 6 pages; pulls top sit-stand from `height-adjustable-tables-desks` + Citi lounge specific product + 2 top chairs from `seating`; 4 product picker settings per page for theme-editor override). **Factual fixes:** 5× proof-bar stat 01 replaced "2019 OECM vendor since" → "2025-470 OECM Agreement number" (healthcare, education, government, non-profit + industries-hub new proof bar); 5× stat 02 detail removed "since 2019" tail; Pro-Svc proof bar `1982 Year founded` → `1964 Family-owned since` (correcting locked-fact violation); Pro-Svc intro brand swap: removed Keilhauer+Global pair → ergoCentric/GFG/OTG/Heartwood as leads with "Keilhauer, Allsteel, Teknion on request" disclosure (per BRAND-PAGES-1 storefront-callable decisions). **FAQs:** 30 generic FAQs replaced with 39 procurement-actionable Q&As across 6 pages (7 hub, 7 healthcare, 7 education, 7 government, 7 non-profit, 7 pro-svc). **Layout standardization across all 6 pages:** intro container widened from 880px to 1280px to align left with all sections below; removed body max-width on entity/coverage/howto sections so heads + copy span full container width (reduces vertical scroll); glance dl spacing fixed (symmetric 24px padding + left-borders on items 2/3 instead of right-borders with collapsing padding); hero badge CSS added scoped to `.lp-hc`/`.lp-edu`/`.lp-gov`/`.lp-np`/`.lp-ps` (was absent — caused badge to render inline beside H1); Browse-categories crosslinks section repositioned from below trust row to between Intro and Who-we-are entity-clarity on healthcare/education/government/non-profit/professional-services (visual break between text walls); industries hub Browse-the-catalogue section repositioned same. All writes to DEV `186373570873` only — LIVE untouched. Pre-existing `bbi-quote-modal.liquid` uncommitted change preserved untouched per prompt rule. Branch `feature/content-polish-1-session-a` ready for merge. Session B (4 service pages + customer-stories + our-work) pending separate session.

**2026-05-20 — AI-7 + AI-8 COMPLETE (Claude Code session, evening).** Followed the AI-7 + AI-8 multi-halt prompt (`/Users/leokatz/Downloads/prompt-ai-7-ai-8.md`). Branched `feature/ai-7-ai-8` off `feature/brand-pages-1` (not `main` per prompt; deviated because BRAND-PAGES-1 already touched `theme/templates/index.json` and branching from main would have regressed those edits on push to DEV). **AI-7:** rewrote `bbi-hero` settings in `index.json` and inserted a new `bbi-about` custom-liquid section between bbi-trust and bbi-shop — Version B plainspoken selected. Hero leads "Canadian-owned · Since 1964" + new H1/deck/sub surfacing OECM Agreement 2025-470. New body section (~150 words) names the Brant Basics ↔ BBI entity relationship, 296 George St N Peterborough HQ, GFG/OTG/Heartwood/ObusForme + 25 more authorized lines, institutional + private-sector buyer split, ON+Western install. **AI-8:** updated `theme/sections/ds-lp-oecm.liquid` + `theme/templates/page.oecm.json` — Version A comprehensive selected. NEW Coverage Table section (Category × GFG/OTG/Heartwood/ObusForme = 177 storefront-callable products under Agreement 2025-470; counts verified live against Shopify Admin API). NEW How-to-Purchase 3-step section. NEW Entity note between proof bar and crosslinks. Fixed 3 factual errors carried in the existing copy: Card 03 (1962→1964, Brantford→296 George St N Peterborough); Card 04 (brand list reordered to lead GFG/OTG/Heartwood/ObusForme); Proof-bar stat 01 (replaced unverified "2019 OECM vendor since" with "2025-470 OECM Agreement number"). Hero badge/heading/standfirst/caption refreshed. Intro paragraph 2 rewritten to drop "since 2019"; paragraph 3 replaced self-link with service-channel inventory (1-day quote, free design, install, warranty, PO billing). 6 existing FAQs replaced with 8 procurement-focused Q&As — FAQPage + GovernmentService JSON-LD already in place auto-builds from new blocks. All writes to DEV `186373570873` only — LIVE untouched. Branch `feature/ai-7-ai-8` ready for merge after `feature/brand-pages-1`. **Three branches local-only at session end:** push and merge in sequence to origin. **Outstanding for follow-up:** verify the 340+ POs / 90+ orgs proof-bar volume claim with Steve (kept as-is for this session). Pre-existing spacing/font-size/photo-rot issues observed during AI-7 spot-check are not AI-7/8 scope.

**2026-05-20 — BRAND-PAGES-1 + A11Y bundle COMPLETE (Claude Code session).** Followed the Wave E execution plan and the Cowork handoff brief. Built 3 new brand hub pages (OTG / Offices to Go, Heartwood Manufacturing, ObusForme) via Approach A clone of `ds-lp-brands-ergocentric.liquid`; rescoped `ds-lp-brands-global-teknion.liquid` to GFG-family experience (Option A — copy/scope update, not rebuild); created 15 brand×category smart collections via `scripts/create-smart-collections.py --live` (all populated, sort_order=best-selling); extended Brands hub `/pages/brands` from 3 tiles to 6; added 3 new brands to nav (desktop + mobile) and re-ordered to put currently-callable brands first; added a new 5th "Brands" column to `bbi-footer.liquid`; rewrote homepage `<meta name="description">` and 2 in-section homepage brand-mention spots (Bucket A + C); about-page brand-mention reorder (line 144 + 169 of `ds-lp-about.liquid`); A11Y critical bundle re-audited against actual BBI theme state (Fix A/B/C found no-ops; Fix D — duplicate `role="main"` on `ds-cs-base.liquid:462` — fixed; Fix E DEV-3 legacy gate completion deferred). All writes to DEV `186373570873` only — LIVE untouched. Branch `feature/brand-pages-1` ready for merge. Follow-up tasks logged for separate sessions: DEV-3 legacy gate completion (search + customers/* still inherit Avada chrome) and homepage image rot (11 `bbi-hp-*.jpg` URLs return 404, belongs to Step 46 IMAGE-SOURCING-V2). SEO-AUDIT-1 remains blocked on DataForSEO MCP + dev-preview crawl access.

---

## ⛔ HARD RULES — APPLY EVERY SESSION, NO EXCEPTIONS

> **Incident 2026-05-10:** A session accidentally pushed `layout/theme.liquid`, `snippets/theme-variables.liquid`, and `assets/information-drawer.css` to the live theme (`178274435385`), breaking brantbusinessinteriors.com for ~30 min. These rules prevent recurrence.

| Rule | Enforcement |
|---|---|
| All theme file writes go to `186373570873` (BBI Landing Dev) **only** | `push-file.py` now hard-aborts if `THEME_ID == LIVE_THEME_ID` |
| Never run `shopify theme push` without `--theme 186373570873` | Bare push may default to live |
| Never type `yes` at the bbi-push-landing.py live-theme prompt | That prompt means you've targeted the wrong theme |
| `fetch-file.py` and `find-liquid-bug.py` may **read** live — never write | Both are labelled read-only in their headers |
| Before writing any theme asset, print `THEME_ID` and confirm it is `186373570873` | Do this as a preflight check in every session |
| If a script has `THEME_ID = '178274435385'` hardcoded — stop, fix it, then run | Never override or skip this check |

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
- ~~**LEAD-1**~~ — ✅ resolved 2026-05-07 (audit done, doc at `docs/plan/bbi-lead-routing.md`)
- ~~**LEAD-3**~~ — ✅ decisions locked 2026-05-07 (three inboxes + modal pattern; see `docs/plan/bbi-lead-routing.md`)
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

## Known Data Hygiene Issues (surfaced 2026-05-12)

These issues are catalogued here because they affect multiple upcoming sessions and must be referenced when running PE Pass 3, COLLECTION-CLEANUP-1, AI-8, and SEO-AUDIT-1.

### Vendor field fragmentation
- 89% of active products (526 of 593) still have vendor = "Brant Business Interiors" — a placeholder from the original Office Central migration, not the real manufacturer.
- PE Pass 3 batches 1–2 enriched 74 products with body_html + specs but did NOT populate the vendor_override field. The plumbing exists in `scripts/push-pe3-enrichment.py`; the batch prompt templates omit the field.
- Future batches (3, 4, 6) MUST populate vendor_override using the canonical brand map from VENDOR-NORMALIZE-1 (see launch tracker).

### specs.manufacturer string fragmentation
- 152 products have a specs.manufacturer metafield populated by PE Pass 2 Hero enrichment + the 74 PE Pass 3 pushes so far.
- 20+ string variants exist for Global Furniture Group alone (e.g., "Global Upholstery Co., Inc", "Global Upholstery Co. / Offices To Go", "OTG / Offices to Go (a division of Global Furniture Group)", etc.).
- Before any brand callout / tagging work, these strings must be normalized against a canonical brand map.

### Real brand distribution (data, not aspiration)
Based on 152 enriched products with specs.manufacturer:
- Global Furniture Group family (Global, OTG, Newland, Fileworks, Basics, Global Upholstery): ~113 products
- Heartwood Manufacturing: ~17 products
- Shoptech / Horizon: ~5 products
- Deflecto: ~2 products
- Fellowes: ~2–3 products
- ergoCentric: 1 product (despite having a brand collection + category page callouts)
- Keilhauer: 0 products (despite having a brand collection + category page callouts)
- Other small brands: ~11 products
- 441 products have no specs.manufacturer yet (unenriched, mostly pending PE Pass 3 batches 3 / 4 / 6).

Implication: brand callouts on category pages currently point at Keilhauer + ergoCentric (zero / one product). These should be reassigned to Global, OTG, Heartwood after VENDOR-NORMALIZE-2 lands. Tracked as part of COLLECTION-CLEANUP-1.

### Tag mass-application
- oecm-eligible: applied to 653/653 active products. Either a botched mass-tag or used historically as an "active product" marker. Currently makes the /pages/oecm page surface the full catalog instead of a curated list.
- Investigation pending in BUG-FIX-2 (launch tracker Step 2).
- Worth auditing other tag prefixes (brand:*, room:*, type:*) for similar mass-application — tracked as TAG-AUDIT-1 (launch tracker, new step).

### Three-source data inconsistency
Vendor / brand data lives in three places that don't agree:
1. Shopify vendor field (currently fragmented — 89% placeholder)
2. specs.manufacturer metafield (currently fragmented — 20+ string variants per brand family)
3. brand:* tags (sparse — only applied via `tag-products-by-collection.py` dry runs, never live)

All three must agree per product before the storefront's brand smart collections + brand callouts function correctly. The canonical brand map (VENDOR-NORMALIZE-1) is the bridge between them.

### Historical push script silent failures (resolved 2026-05-12)

Between PE Pass 2 (first Hero 100 batches) and Batch 3 of
PE Pass 3 (2026-05-12), `scripts/push-pe3-enrichment.py` had four
bugs that caused it to silently skip writes for body_html,
Shopify vendor field, and brand:* tag — while correctly writing
specs.* metafields. As a result, PE Pass 2/3 enrichment work
appeared as "live" in build state and tracker but only the
metafield specs were actually live on the storefront. Buyer-facing
descriptions, vendor attribution, and brand tags remained the
raw pre-enrichment import data.

**Bugs in push-pe3-enrichment.py (all fixed in commit 58e8a27):**
1. Script read `rec.get('description')` but batch output uses
   `draft_body_html` — descriptions never written.
2. Output JSON shape mismatch: products at top level vs under
   'products' key — script saw 0 products in some batch files.
3. Filter used `rec.get('status')` but data field is `action` —
   action='other' products would have been pushed if any matched.
4. No brand:* tag write logic — tags from batch output ignored.
5. Vendor field also wasn't being written — bundled with the
   brand-tag-write fix in 58e8a27.

**Resolution 2026-05-12:**
- Push script bugs fixed in commit 58e8a27.
- All 88 affected products (69 from Batches 1+2 + 19 from
  Batch 3) had body_html + vendor + brand:* tag pushed live.
  Evidence: `data/logs/pe3-push-20260512-224332.json` (88 products_ok, 0 failures, live: true).
  **Note for Steve:** `data/logs/` is gitignored — no standalone git commit for the Shopify push itself.
  The push occurred between commits 58e8a27 (script fix) and 33a2c35 (kody patch post-verification).
- `kody-mesh-chair-otg13110` had a draft-side copywriting gap
  (missing BBI close paragraph in the original Batch 2 draft);
  fixed in commit 33a2c35.
- Post-push verification confirmed 5/5 sample products clean on
  storefront, spec metafield average 9.4 per product.

**Lesson — required for future batch sessions:**
- Every batch's --live push must include the defensive
  prerequisite check (verify push script field names match batch
  output schema before run) AND a post-push 5-product storefront
  verification.
- The PE Pass 3 batch kickoff prompt pattern (added 2026-05-12)
  bakes both checks in by default.

### Canonical brand map gaps surfaced during PE Pass 3 + TAG-AUDIT-1
_(pending resolution in COLLECTION-CLEANUP-1 sub-steps,
 Steps 10A–10D)_

The canonical brand map (VENDOR-NORMALIZE-1, 2026-05-12) was built
from the 152 enriched products available at that point. PE Pass 3
Batches 4 + 6 + TAG-AUDIT-1 surfaced 10 additional brand variants
that need to be added to the map. None are blockers — affected
products have correct fallback handling (`vendor_override =
"Brant Business Interiors"` + `research_failed_reason` populated).
Resolution scheduled in COLLECTION-CLEANUP-1 Steps 10A–10D.

**Pending additions:**

| Brand | Source | Products | Notes |
|---|---|---|---|
| Safco | TAG-AUDIT-1 | 4 | standalone, callable=False |
| Humanscale | TAG-AUDIT-1 | 2 | standalone, callable=False |
| Victor Technology LLC | PE Pass 3 Batch 4 | 1 | standalone, callable=False |
| Rocelco | PE Pass 3 Batch 4 | 1 | standalone, callable=False |
| HDL | PE Pass 3 Batch 4 | 1 | dist by Grand & Toy; standalone, callable=False |
| Kensington | PE Pass 3 Batch 6 | 1 | tech accessories; standalone, callable=False |
| Sentry Safe | PE Pass 3 Batch 6 | 2 | Sentry Group parent; standalone, callable=False |
| FireKing | PE Pass 3 Batch 6 | 1 | standalone, callable=False |
| Tayco | PE Pass 3 Batch 6 | 1 | Toronto, ON manufacturer of the Halifax line; standalone, callable=False |
| Heartwood slug migration | TAG-AUDIT-1 | 1 | re-tag `brand:heartwood` to `brand:heartwood-manufacturing-ltd` |

**Total: 14 products** across 10 brand entries need canonical map
additions + product re-tagging.

**Re-push idempotency confirmed 2026-05-13:** The push script's
incremental catch-up behavior (rewriting all products in the
output file on each --live run, not just the newest batch) was
verified safe via Batch 4 integrity check — 3/3 sampled prior-batch
products had byte-identical body_html before and after re-push.
Future batch sessions can expect push counts higher than the
batch's product count; this is feature, not bug.

**RESOLUTION 2026-05-13:** All 15 affected products re-tagged
in commit 66a0bff (APPLY-MAP-ADDITIONS, Sub-step B).
Canonical map total: 30 brands (added Safco, Humanscale, Victor
Technology LLC, Rocelco, HDL, Kensington, Sentry Safe, FireKing,
Tayco in commit 29bcbad — Sub-step A). Heartwood slug migration
surfaced 0 stragglers — already migrated in earlier sessions.

### Global-Teknion smart collection — restored to intent (2026-05-13)
The brands-global-teknion smart collection was found to be running
on a single legacy rule `tag equals brand:global-teknion`, matching
21 unenriched products carrying the merged legacy tag. The rule
was broken — it would have collapsed to 0 products as remaining
stragglers got normalized. COLLECTION-CLEANUP-APPLY (commit 737f6f6)
updated the rule to disjunctive `brand:global-furniture-group OR
brand:teknion`, restoring the hybrid Wave C intent. Collection now
shows 72 products (all GFG + Teknion combined). 18 unenriched
stragglers had the legacy tag stripped; they will receive correct
canonical brand tags during Phase 1b post-launch enrichment.

### Collections — post-COLLECTION-CLEANUP-APPLY state (2026-05-13)
Active collections post-COLLECTION-CLEANUP-APPLY: 207
(was 371 before 2026-05-13 audit + cleanup). 164 unpublished —
either ARCHIVE (legacy / 0-product / not in nav) or REDIRECT
(legacy brand collections folded into /pages/brands).
data/url-redirects-bulk.csv contains 164 rows ready for
Shopify Admin import.

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
| 7b | NAV-5 | Header search bar + BBI search results page | ✅ | 2026-05-12 `theme/snippets/bbi-nav.liquid` + `theme/sections/ds-search-results.liquid` + `theme/templates/search.json` pushed to dev theme 186373570873 | **Done.** Inline search bar (always-visible, 220px, gray pill with icon) added to `bbi-nav.liquid` utility bar between nav and phone number; hidden on mobile (mobile overlay retains its own search row). Predictive suggest via `/search/suggest` API — debounced 200ms, up to 5 product results with thumbnails + "See all" link, drops down from the bar, closes on click-outside or Escape. `ds-search-results.liquid` replaces base-theme `main-search` section in `templates/search.json` — BBI-styled 4-col product grid (same cards as ds-collection-base), breadcrumb, result count, refine-search bar, pagination, empty state. Products in `other` + `other-1` collections filtered out of results via `product.collections` loop. Only `type=product` results shown. |
| 8 | PB-13 | Reconcile brand-dealer (merge or de-gate) | ✅ | commit `71e7b5e` (CLEANUP-1) | **Done.** Resolved by CLEANUP-1 — gate already de-cluttered (brand-dealer suffix removed from theme.liquid). Branch never pushed to remote; file never existed on main. Page out of scope for v1 (Industries Hub + Brands Hub cover dealer-trust signaling). |
| 9 | PB-9 | Extend `bbi_landing` gate to detect collection templates | ✅ | commit `ceac44f` `theme/layout/theme.liquid` | **Done.** Added `template == 'collection.category'` to bbi_landing gate. Smoke test deferred to PB-10 (first collection.category page exercises it). |
| 10 | PB-10 | Build `collection.category.json` template + `ds-cc-base.liquid` section pattern | ✅ | commit `77fca26` `theme/sections/ds-cc-base.liquid`, `theme/templates/collection.category.json`, `scripts/set-collection-template-suffix.py` | **Done.** Section: hero + breadcrumb (2/3-level via settings) + intro (richtext) + tile grid (max 20 tile blocks, always rendered) + view-all CTA + brand_callout blocks (max 2) + phone CTA closer. Gate exercised: `?view=category` on dev theme. Smoke test 5/5 green: bbi-header=1, bbi-footer=1, Starlite suppressed (PB-9 confirmed), active nav="Shop Furniture", tile grid container present. Helper script: dry-run default, --live, --rollback flags; backup + log on every run. |
| P2-1 | Business Furniture vertical (`/collections/business-furniture`) | ✅ | commit `3e9ffe3` `theme/templates/collection.business-furniture.json` | 9 category tiles + 3 brand callouts (Keilhauer, Global/Teknion, ergoCentric), view-all CTA, phone CTA closer. Gate extended for `collection.business-furniture`. Smoke: 9 tiles, 3 brands, view-all, phone CTA, Starlite suppressed — all green. |
| P2-2 | Seating (`/collections/seating`) | ✅ | commit `4e04f12` `theme/templates/collection.seating.json` | 16 sub-type tiles, Keilhauer + ergoCentric callouts. Smoke: 16 tiles, 2 brands, 3-level breadcrumb, Starlite suppressed — all green. |
| P2-3 | Desks & Workstations (`/collections/desks`) | ✅ | commit `4e04f12` `theme/templates/collection.desks.json` | 9 sub-type tiles, Global/Teknion callout. Suffix set via API. |
| P2-4 | Storage & Filing (`/collections/storage`) | ✅ | commit `4e04f12` `theme/templates/collection.storage.json` | 14 sub-type tiles, no callouts. Suffix set via API. |
| P2-5 | Tables (`/collections/tables`) | ✅ | commit `4e04f12` `theme/templates/collection.tables.json` | 10 sub-type tiles, no callouts. Suffix set via API. |
| P2-6 | Boardroom (`/collections/boardroom`) | ✅ | commit `4e04f12` `theme/templates/collection.boardroom.json` | 3 sub-type tiles, Keilhauer callout. Suffix set via API. |
| P2-7 | Ergonomic Products (`/collections/ergonomic-products`) | ✅ | commit `4e04f12` `theme/templates/collection.ergonomic-products.json` | 4 sub-type tiles, ergoCentric callout. Suffix set via API. |
| P2-8 | Panels & Dividers (`/collections/panels-room-dividers`) | ✅ | commit `4e04f12` `theme/templates/collection.panels-room-dividers.json` | 3 sub-type tiles, Global/Teknion callout. Suffix set via API. |
| P2-9 | Accessories (`/collections/accessories`) | ✅ | commit `4e04f12` `theme/templates/collection.accessories.json` | 4 sub-type tiles, no callouts. Suffix set via API. |
| P2-10 | Quiet Spaces (`/collections/quiet-spaces`) | ✅ | commit `4e04f12` `theme/templates/collection.quiet-spaces.json` | 5 sub-type tiles, no callouts. Suffix set via API. |
| PB-11 | Sub-collection 200/404 + product count audit | ✅ | commit `81e83c8` `data/reports/sub-collection-audit-20260506_211829.csv` | 68/68 slugs found. 66 PASS / 2 WARN (metal-shelving + audio-visual-equipment empty — need products). 0 FAIL. `scripts/audit-sub-collections.py` report-only, exit 0. |
| LEAD-1 | Crawl + dump current lead routing | ✅ | commit `21a26df` `docs/plan/bbi-lead-routing.md` | Full CTA audit across all 10 ds-lp-* sections, bbi-nav, bbi-footer, ds-cc-base, index.json custom-liquid. Two critical gaps found: (1) design-services uses unreliable `mailto:` form; (2) `/pages/quote` "Online quote form" link goes to `/pages/contact` which has no template. LEAD-3 decisions pre-loaded. Steve to fill in Shopify notification routing + phone line + inbox verification per action items in the doc. |
| INTERLINK-1 | Formalize P1-11 audit pattern as reusable script | ✅ | commit `937cbcc` `data/reports/interlink-audit-20260506_211250.csv` | 21/21 pages checked. 0 FAIL / 52 PASS / 92 WARN / 108 SKIP. WARNs on checks 6/7/8/11 are live-theme fallback (dev theme preview requires Shopify admin auth — source files confirmed correct). `--suffix` flag added to `set-collection-template-suffix.py`. |
| IND-PROP | Industries Hub Browse + FAQ propagation to 5 industry pages | ✅ | commit `c6812bd` `theme/snippets/ds-browse-faq.liquid` | Browse (9-grid) + FAQ (5-item) added to all 5 industry sections via shared `ds-browse-faq` snippet. Smoke tested healthcare + government. |

---

## Wave B — Phase 3 + Smart Collections

**Pre-req:** Wave A complete.
**Goal:** Sub-collection product listings on the new design system. Migrate manual collections to smart so new products auto-populate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| PB-14 | Manual → Smart collection migration script + per-collection assignment + rollback | ✅ | `66f7623` `scripts/migrate-to-smart-collections.py` | Convert manual `/collections/*` to rule-based using `type:*` and `room:*` tags. Backup first. |
| PB-15 | Build `collection.json` template + `ds-cs-base.liquid` section | ✅ | `de3237e` `theme/sections/ds-cs-base.liquid` + `collection.base.json` + gate update | Filter sidebar + product grid + 4-level breadcrumb (Home > Shop Furniture > Category > Sub-collection) + phone CTA. |
| P3-rollout | Apply `collection.json` to ~68 Business Furniture sub-collections | ✅ | `aaa105a` `scripts/set-sub-collection-suffix.py` + rollout run | Script-driven push, hero images from `data/page-images/` |
| INTERLINK-2 | Re-run interlinking audit, fix drift introduced by Phase 3 | ✅ | `82c64c8` Post-Wave-B audit (0 failures) | |

---

## Wave C — Phase 4 trust pages

**Pre-req:** Wave B complete (so brand pages can link to live shop verticals).
**Goal:** Brands hub + brand pages + About + Contact + Our Work + Delivery + Relocation.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| P4-1 | Brands Hub (`/pages/brands`) | ✅ | `theme/sections/ds-lp-brands.liquid` + `theme/templates/page.brands.json` exist; Page ID 170824958265 published 2026-05-07 | Phase 1 API check (2026-05-08): exists, published, suffix `brands` ✅. body_html=0 expected (OS 2.0 section-rendered). |
| P4-2 | Keilhauer (`/pages/brands-keilhauer`) | ✅ | `theme/sections/ds-lp-brands-keilhauer.liquid` + `theme/templates/page.brands-keilhauer.json` exist; Page ID 170824991033 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-keilhauer` ✅. |
| P4-3 | Global / Teknion (`/pages/brands-global-teknion`) | ✅ | `theme/sections/ds-lp-brands-global-teknion.liquid` + `theme/templates/page.brands-global-teknion.json` exist; Page ID 170825056569 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-global-teknion` ✅. |
| P4-4 | ergoCentric (`/pages/brands-ergocentric`) | ✅ | `theme/sections/ds-lp-brands-ergocentric.liquid` + `theme/templates/page.brands-ergocentric.json` exist; Page ID 170825023801 published 2026-05-07 | Phase 1 API check: exists, published, suffix `brands-ergocentric` ✅. PB-13 reconciliation resolved (CLEANUP-1 commit `71e7b5e`). |
| P4-5 | About (`/pages/about`) | ✅ | `theme/sections/ds-lp-about.liquid` + `theme/templates/page.about.json` exist; Page ID 170825220409 published 2026-05-07 | Phase 1 API check: exists, published, suffix `about` ✅. |
| P4-6 | Our Work / Portfolio (`/pages/our-work`) | ✅ | `theme/sections/ds-lp-our-work.liquid` + `theme/templates/page.our-work.json` exist; Page ID 170825318713 published 2026-05-07 | Phase 1 API check: exists, published, suffix `our-work` ✅. Content (48 OCI photos) still to be wired — content work, not scaffolding. |
| P4-7 | Contact (`/pages/contact`) | ✅ | `theme/sections/ds-lp-contact.liquid` + `theme/templates/page.contact.json` exist; Page ID 134463553849 published 2024-01-17 | Phase 1 API check: exists, published, suffix `contact` ✅. body_html=2348 chars (legacy content, harmless). Form routing to sales@ unverified — separate verification item. |
| P4-8 | Delivery & Installation (`/pages/delivery`) | ✅ | `theme/sections/ds-lp-delivery.liquid` + `theme/templates/page.delivery.json` exist; Page ID 170825253177 published 2026-05-07 | Phase 1 API check: exists, published, suffix `delivery` ✅. |
| P4-9 | Relocation Management (`/pages/relocation`) | ✅ | `theme/sections/ds-lp-relocation.liquid` + `theme/templates/page.relocation.json` exist; Page ID 170825285945 published 2026-05-07 | Phase 1 API check: exists, published, suffix `relocation` ✅. |

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

> **Launch-criticality split (2026-05-21 Day 8 audit).** Table rows above preserved verbatim; this note records the priority split mirrored in the tracker. **Pre-LAUNCH-2 critical (added to the Day 10 launch sequence in CURRENT FOCUS):** **W0-1** (GSC + GA4 — no SEO data compounds without it) and **W0-3** (product redirects CSV upload). **Parallel / post-launch acceptable (don't block any launch step):** **W0-2** (Google Business Profile), **W0-2b** (Reviews seeding), **W0-6** (parent-domain backlinks), **W0-7** (OECM + "Since 1964" site-wide trust signals — likely folds into Step 46 image/branding work).

---

## Wave G-Fixes — Visual review bugfixes (2026-05-09)

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| WAVE-G-FIXES-1 | Bug-fix pass from live visual review of dev theme 186373570873 | ✅ | commits `a20b526`→`42c4227`; all files on dev theme | **BATCH-1** Smart collections chrome: `template.name == 'collection'` gate already correct; dev theme had stale layout.liquid — re-pushed via direct API. **BATCH-2** 11 PDP fixes: (2a) gallery thumb JS clears srcset; (2b) variant chips → `<button>` + `BbiPdpVariants` WC + variant JSON; (2c) description moved after variants, full HTML; (2d) has_specs checks all 11 fields, spec-row alternating via Liquid counter; (2e) both buttons 100% width 48px; (2f) delivery note absent; (2g) validation keeps chips horizontal; (2h) image 1024px square contain; (2i) quote btn `color:#fff` explicit; (2j) additional-services product unpublished → published via API; (2k) CTA closer btn `color:#fff` explicit. **BATCH-3** blog CTA `color:#fff`; footer Blog & Resources link added. **BATCH-4** `scripts/tag-products-by-collection.py` written + dry-run: 34 boardroom / 14 global-teknion candidates found; 6 collections DATA GAP (no vendor/type metadata) — awaiting Leo review. |
| WAVE-G-FIXES-2 | Second bug-fix pass — quote modal, PDP restructure, brand plates, emoji, CTA copy | ✅ | commits `71c37e0`→`586290b`; all 26 files pushed to dev theme 186373570873 | **BATCH-1** Re-verified WAVE-G-FIXES-1 regressions: chip flex hardened with `display:flex !important` (Starlite override); blog CTA + 404 button `color:#fff !important` (class+element specificity beat class-only); additional-services confirmed HTTP 200. **BATCH-2** New `bbi-quote-modal.liquid` snippet — `<dialog>`-based Web Component with Shopify contact form, focus trap, success screen; wired nav, footer, PDP, blog, 404, cc-base, delivery pages; global JS intercept for `[href*="/pages/quote"]` covers 20+ landing pages without per-file edits; rendered once in `theme.liquid` inside `bbi_landing` gate. **BATCH-3** PDP: variant price refreshes on chip select via `Intl.NumberFormat`; description restructured as three inline labeled sections (About / Key Features / Specs) inside info column — standalone `.pdp-features` and `.pdp-specs` full-width blocks removed. **BATCH-4** `brand_plate_canadian: false` → `true` for Global Furniture and Teknion in all 9 collection JSON templates — "Canadian Authorized" badge now shows for both. **BATCH-5** 4 emoji (🚚 🔧 📋 ♻️) removed from delivery page feature card icon divs. **BATCH-6** `ds-cc-base.liquid` hero CTA: only appends `hero_title` when `cta_label` is blank — fixes "Get a free design consultationBusiness Furniture" concatenation bug on business-furniture collection. **BATCH-7** Wave A smoke check: 9/10 PASS, desks WARN-transient (subsequent check clean, likely bot rate-limit on first curl); report at `data/reports/wave-a-smoke-2026-05-10.csv`. |

---

## Wave H — Stabilization & PE Pass 1 (2026-05-10 → 2026-05-11)

**Why this wave exists:** A run of architectural fixes and feature builds completed after Wave G-Fixes-2 that didn't fit cleanly into existing waves. Includes the 2026-05-10 live-site incident recovery (81 missing assets synced live → dev), full cart funnel rebuild, PDP black-background fix, design system completion for default collection templates, PDP gallery lightbox, site-wide best-sellers sort, and the first milestone of the restructured PROMPT-4 product enrichment workflow.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| STAB-1 | Asset infrastructure recovery + cart chrome architectural fix | ✅ | commits (2026-05-10) `theme/layout/theme.liquid`, `theme/templates/cart.json`, `theme/sections/ds-cart-base.liquid`, `config/settings_data.json` | **81 missing CSS/JS assets** synced from live → dev (`base.css`, `style.css`, `collection.css`, `theme.js`, +77 others). Direct loads of collection and search pages now render correctly. **Cart chrome architectural fix:** root cause was `template == 'cart'` missing from `bbi_landing` gate, so Starlite header/footer/JS were loading alongside BBI nav. Starlite JS polluted CSS vars and localStorage, breaking the next page on navigation from cart. Added cart to gate, restructured `cart.json` with `bbi-nav-wrap` + `bbi-footer-wrap` sections, stripped inline `render` calls from `ds-cart-base.liquid`. **Settings patches:** `image_border: true`, `image_background: true`, `quickview: false` aligned dev with intended product-card behaviour. |
| PDP-BLACK-FIX | Black PDP background fix (2026-05-11) | ✅ | `theme/layout/theme.liquid` head injection + JS guard | Dark-mode toggle JS (`localStorage.darkMode == 'true'`) was setting `color-mode="dark"` on `<html>` unconditionally. Attribute-selector specificity beat every `body { ... !important }` override attempted in section CSS. Two-part fix: (a) skip dark mode on product templates via `template == 'product'` check before the JS runs; (b) CSS belt-and-suspenders in `<head>` with matching specificity (`html[color-mode] body, html[color-mode="dark"] body, html body, body { background-color: #ffffff !important }`). Steve confirmed PDPs render white. Note: existing dark-mode flag in user's localStorage requires hard refresh / incognito to fully clear after fix. |
| CART-FUNNEL | Cart 404 + badge + page DS + polish + mini-cart (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/snippets/bbi-nav.liquid`, `theme/sections/ds-cart-base.liquid`, `theme/templates/cart.json`, `theme/assets/bbi-logo-v2.png` | **Cart 404 fix:** ds-pdp-base.liquid Add to Cart now uses `fetch('/cart/add.js')` AJAX instead of full-page POST. Shows "Added ✓" for 2s + dispatches `cart:updated`. **Header cart count badge:** bbi-nav.liquid gained shopping bag icon + red count `[data-bbi-cart-count]`; server-renders `cart.item_count`; refreshes on `cart:updated` via `/cart.js`. **Cart page design system:** new `ds-cart-base.liquid` section + `cart.json` template replacing default Shopify cart. BBI nav + footer, 1320px container, BBI tokens. **Cart polish (later same day):** replaced hardcoded `#0B0B0C` with `rgb(var(--buttonBackground))` tokens on checkout + empty-state CTAs. Mini-cart dropdown in nav header — cart icon → dropdown panel (line items + subtotal + View Cart + Checkout); closes on click-outside + Escape; refreshes on `cart:updated`. Uploaded `bbi-logo-v2.png` to dev theme assets (nav/footer logo fallback now resolves). |
| PROMPT-2 | Buy Now + Quantity selector on PDP (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid` | Quantity stepper + Buy Now button wired to `/cart/add.js` → `/checkout`, sitting inside the buyable-only branch (BBI Rule #2 preserved — Quote-only CTA on $0/sold-out untouched). Variant-ID resolution matches existing ATC flow (BbiPdpVariants Web Component). Regression: ATC + mini-cart + Quote modal all continued to work. |
| PROMPT-3 | Best-sellers sort site-wide + PDP related rewrite (2026-05-11) | ✅ | 19 smart collections updated via Admin API; `ds-pdp-base.liquid` related section rewrite | **Site-wide:** audited 369 collections (49 smart, 320 custom). Set `sort_order = best-selling` on 19 smart collections (19/19 HTTP 200). 9 editorial exclusions kept original sort: `bundle-builder-products` (created-desc), `fees-products` (alpha-asc), 7 `room-*` collections. Rollback CSV at `data/backups/collection-sort-orders-pre-20260511_135450.csv`. Site-wide audit confirmed no Liquid overrides via `\| sort_by`. **PDP related:** rewired to 3-tier fallback (`all-<type>` → `room-`tag → `all-business-furniture`); heading reads "Best sellers in `<category>`" on Tier 1, "Customers also bought" otherwise; section suppressed when all empty. Capture pattern used to work around Shopify Liquid's `where_exp` outer-scope limitation. **Note:** collection sort changes are store-wide (affect live theme too, not just dev). |
| PDP-LIGHTBOX-1 | PDP gallery lightbox + related-card aspect ratio (2026-05-11) | ✅ | `theme/sections/ds-pdp-base.liquid` lightbox CSS/JS + card aspect 4/3 → 4/5 | **Lightbox:** clicking main product image opens fullscreen viewer — dark overlay (`rgba(0,0,0,0.92)`), centred full-res image, left/right arrow buttons + keyboard nav, `1 / 4` counter when multiple images, ESC or click-outside closes, body scroll locks while open, arrows auto-hide on single-image products. **Related card ratio:** 4/3 → 4/5 to match collection-page cards in `ds-cc-base.liquid`; hover eased to `scale(1.03) / 160ms`. Visual parity between PDP related cards and collection grid is now exact. |
| IMG-BG-WHITE | Product image slot background — white site-wide (2026-05-12) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/sections/ds-cs-base.liquid`, `theme/sections/ds-cc-base.liquid`, `theme/sections/ds-article.liquid` | Product images have a white background in Shopify CDN but containers were set to `var(--alternateBackground)` (#FAFAFA grey), creating a visible grey mat around every product photo. Fixed all 7 product image slots to `#FFFFFF`: PDP gallery main + thumbnails (`.pdp-gallery__main`, `.pdp-gallery__thumb`); PDP "Best sellers in…" related cards (`.pdp-prod-card__img-wrap`); smart collection page cards (`.ds-cs__card-img`); category collection tile + product cards (`.ds-cc__tile-media`, `.ds-cc__product-card-media`); article related product cards (`.prod-card__img-wrap`). Editorial hero / landing-page media containers left at `--alternateBackground` (real photos fill those). |
| IMG-CENTER | Product image centering + contain fit site-wide (2026-05-12) | ✅ | `theme/sections/ds-pdp-base.liquid`, `theme/sections/ds-cs-base.liquid`, `theme/sections/ds-cc-base.liquid`, `theme/sections/ds-article.liquid` | All product card image slots switched from `object-fit: cover` (crops/fills) to `object-fit: contain` + `object-position: center`, with `display: flex; align-items: center; justify-content: center; padding: 12px` on containers (4px for thumbnails). Matches the pattern already used on the PDP main gallery. Hover scale (`scale(1.03)`) removed from all card images — scaling a contained image expands into whitespace. 6 selectors updated: `.pdp-prod-card__img-wrap/img`, `.pdp-gallery__thumb img`, `.ds-cs__card-img/img`, `.ds-cc__tile-media/img`, `.ds-cc__product-card-media/img`, `.prod-card__img-wrap/img`. |
| COLLECTION-DS-1 | ds-collection-base for default `/collections/*` pages | ✅ | Closed by Steve 2026-05-11 | Default-template collection pages (`/collections/all` + smart collections without custom template suffixes) now resolved. The BBI design system is the source of styling on these surfaces. Closes the gap where `/collections/all` rendered with Starlite's `main-collection` product grid instead of BBI design system. |
| PE-PASS-1 | Product enrichment Pass 1 — triage CSV (2026-05-11) | ✅ | commit `76f109d` · `data/reports/product-triage-pass1-2026-05-11.csv` | First milestone of restructured PROMPT-4 (was "write 500 descriptions", now triage-first 3-pass flow). Pulled 653 products (593 active + 60 archived; `status=any` not functional on this token so pulled separately and merged). 24-month sales for 126 products (203 orders processed). SEO metafields for all 653 (2 errors, defaulted to false). **Working set:** 553 products (653 minus Hero 100). **Tier breakdown:** A=98 keep, B=12 light enrichment, C=383 archive recommended, skip=60 leave-unpublished. **Archive breakdown:** 20 HR1 ($0 hard rule), 47 non-best in duplicate clusters (+1 HR1 override), 316 zero-sales + quality-gap. **Duplicate clusters:** 52 covering 117 products. CSV has `steve_override_action` column for manual override. All 7 sanity checks pass. **Top 5 borderline archives:** 5 Teknion $0 showcase products (HR1 triggered but per BBI Rule #2 likely override to keep-quote-only). **Top 5 duplicate clusters surfaced false positives:** delivery fees (4 SKUs at different prices), chair mats (different sizes), chair variants (size/arm options not true duplicates). Steve reviewing in Sheets. |
| PE-PASS-2 | Move-to-Other + enrichment CSV generation | ✅ | commit `a734c9c` · 7 batch prompts at `BBI-Session-Kickoff/enrichment-prompts/` | **All 4 phases complete.** Phase 0: `ds-pdp-base.liquid` patched (single-tier related, Other breadcrumb fallback) + `bbi-product-jsonld.liquid` breadcrumb fallback (`d6dfaf0`). Phase 1: Other collection created (id=527013085497). Phase 2: canary `teknion-boardroom` ✅. Phase 3: 336 archive products moved to Other, tags stripped (1 failure `craft-round-20-unit` recovered). Phase 4: enrichment infrastructure built — `pe-pass2-products.json` (157 products), `pe-pass2-batches.json` (7 batches), `pe-pass2-checkpoint.json` + `pe-pass2-output.json` (empty, ready). 7 self-contained batch prompt files built for one-by-one Claude enrichment sessions. Override applied: `archive-duplicate` excluded from move (all 47 kept). **Enrichment sessions (7 batches) in progress — Steve runs these independently.** |
| SPEC-JSON-LD | `additionalProperty` in Product JSON-LD | ✅ | commits `5be9b56`, `5f4a3bc` · `theme/snippets/bbi-product-jsonld.liquid` on dev `186373570873` + live `178274435385` | Added `additionalProperty` array to Product schema.org JSON-LD. Reads all 12 `specs.*` metafields; conditionally renders each as `PropertyValue`. Also: Key Features stripped from About section in `ds-pdp-base.liquid` via `split: '<h3>' \| first` — now only appears in Specifications. Both files pushed to dev + live theme. Verified on localhost:9292 (Arlo chair): About clean, Specs correct. |
| KF-STRIP | Key Features de-duplication in About section | ✅ | commit `5f4a3bc` · `theme/sections/ds-pdp-base.liquid` | `product.description \| split: '<h3>' \| first` strips Key Features / Who it's for / closing boilerplate from the About block. Legacy products with no `<h3>` unaffected (single-item array, full description returned). Verified via API on 2600 Series (789 chars, 2 h3 sections stripped) and visually on Arlo chair. |
| SPEC-HERO-PUSH | Hero 100 spec gap-fill + metafield push | ✅ | `data/specs.json` (100) + `data/logs/pe2-push-20260511-230357.json` (final push) | **All hero spec sessions complete (2026-05-11).** Steve ran H1A (12), H1B (11), H2 (19), H3 (~35), and a bonus `hero-batch-other.md` (9). Output file: 99 products (49 done + 33 auto-patched OTG/Global + 16 skip + 1 service). All pushed: `merge-hero-specs.py --live --push` confirmed. Final push log: `pe2-push-20260511-230357.json`. |
| HERO-SPEC-SESSIONS | Hero 100 spec gap enrichment sessions (H1A → H3) | ✅ | `data/reports/hero-spec-gaps-output.json` — 99 products complete | **All 4 batches run by Steve (H1A/H1B/H2/H3) + bonus `hero-batch-other.md`.** 49 done + 33 auto-patched (OTG/Global warranty + country) + 16 skip + 1 service. Merge+push confirmed via `scripts/merge-hero-specs.py --live --push`. |
| PE-PASS-3 | Push enrichment to Shopify (descriptions + specs + vendor) | ✅ | `scripts/push-pe3-enrichment.py` · `data/logs/pe3-push-20260511-235643.json` · `data/logs/pe3-push-20260512-224332.json` · commits d898b12 (Batch 4) · a4582ea (INNOVATIONS-FIX) · a44d14c (Batch 6) | **COMPLETE 2026-05-13. Final progress: 143 of 157 products enriched and live on storefront.** Batches shipped: 1 (25), 2 (26), 3 (19), 4 (25), 5 (10), 6 (30), 7 (13) = 148 total batch rows; 143 enriched + live, 14 are routed-to-Other or intentional skip rows. 10 new brand singletons surfaced across Batches 4 + 6 + TAG-AUDIT-1 — catalogued in Known Data Hygiene Issues → Canonical brand map gaps; none are blockers. Closes Step 8 of the launch tracker. **PE Pass 3 COMPLETE 2026-05-13. 143/157 products enriched and live. Remaining 14 are intentional skip / routed-to-Other.** |
| SPEC-CANARY | Live canary test — Google Rich Results Test | 🟡 | `bbi-product-jsonld.liquid` + `ds-pdp-base.liquid` pushed to live theme `178274435385` | Both files live on `178274435385`. **Note:** live site brantbusinessinteriors.com uses Avada's `main-product` section (not `ds-pdp-base`) — so additionalProperty won't render on the live public site until the dev theme is set as the main theme. Dev theme (186373570873) verified on localhost:9292: additionalProperty rendered, About section clean. **Remaining:** Google Rich Results Test on a Hero product URL once dev theme preview is accessible — defers to pre-launch SEO-AUDIT-1. |
| ICP-V2 | ICP v2 approved + cascaded to all prompt files | ✅ | commit `1d6684c` · `docs/strategy/icp.md`, `.claude/skills/bbi-build-page/SKILL.md`, 8 enrichment batch files | Steve approved 2026-05-06 draft. Changes: co-primary ICPs A+B (institutional + SMB equal weight), Ontario + Western Canada co-primary geography, dual buying mode (cart + quote), install in Ontario + Western Canada. Cascaded to: SKILL.md (buyers context, ICP gate question, card CTA dual-mode), all 8 enrichment prompts (closing ¶ delivery/install language, OECM Ontario-vs-national distinction). |
| AUDIT-1 | Pre-launch tech-debt + state audit | ✅ | `data/reports/audit-tech-debt-2026-05-12.md` · `data/reports/empty-collections-snapshot-2026-05-12.csv` | 15 findings total. 4 blockers promoted to launch path Steps 1–4. 11 deferred. Surfaced vendor data hygiene issues now catalogued in "Known Data Hygiene Issues" section above. |
| PUSH-FIX-1 | Surfaced + fixed 5 silent-failure bugs in `scripts/push-pe3-enrichment.py` · body_html / vendor field / brand:* tag writes restored · 88 products affected, all pushed live 2026-05-12 | ✅ | commits 58e8a27 (script fix), 33a2c35 (kody patch); push evidence: `data/logs/pe3-push-20260512-224332.json` (88 products_ok, 0 failures, live: true) | See Known Data Hygiene Issues → Historical push script silent failures for full bug list and root-cause analysis. Post-push verification: 5/5 sample products clean on storefront, avg 9.4 spec metafields per product. |
| PE-PASS-3-BATCH-4 | Desks & Tables Part 1 enrichment batch | ✅ | commit d898b12 | 2026-05-13 · 25 products enriched + pushed (9 OTG, 7 GFG, 2 Office Star, 1 Fellowes, 1 Heartwood, 5 BBI fallback) · 5/5 storefront verification · 5 research_failed_reasons surfaced (Victor Technology, Rocelco, HDL identified for canonical map addition) |
| INNOVATIONS-FIX | Corrected canonical brand map — Innovations re-attributed from Global Furniture Group to Heartwood Manufacturing Ltd. | ✅ | commit a4582ea | 2026-05-13 · as_standalone=False, parent=Heartwood · 5 products re-tagged (vendor + metafield + brand tag) · surfaced during Batch 4 enrichment research, confirmed via heartwooddl.com · 5/5 verification |
| PE-PASS-3-BATCH-6 | Storage & Accessories enrichment batch — LAST PE Pass 3 batch | ✅ | commit a44d14c | 2026-05-13 · 30 products enriched + pushed (9 Heartwood, 7 OTG, 4 Fellowes, 1 Deflecto, 9 BBI fallback) · 5/5 storefront verification · 4 new brand singletons surfaced (Kensington, Sentry Safe, FireKing, Tayco — all flagged for canonical map addition) · Step 8 closes |
| CANONICAL-MAP-ADDITIONS | Add 9 new canonical brands to brand map | ✅ | commit 29bcbad | 2026-05-13 (Sub-step A) · added 9 new canonical brands to docs/strategy/brand-canonical-map.md + .csv (Safco, Humanscale, Victor Technology LLC, Rocelco, HDL, Kensington, Sentry Safe, FireKing, Tayco) · canonical brand total 20 → 30 · Heartwood slug migration captured in notes |
| APPLY-MAP-ADDITIONS | Re-tag 15 products to match new canonical entries | ✅ | commit 66a0bff | 2026-05-13 (Sub-step B) · re-tagged 15 products to match new canonical entries · vendor field + specs.manufacturer metafield + brand:* tag now agree per product across the full canonical brand map · 15/15 verification clean |
| COLLECTION-AUDIT | Audit all 371 collections — read-only | ✅ | commit a24b9e3 | 2026-05-13 (Sub-step C1, read-only) · 371 collections audited (49 smart, 322 custom) · 148 zero-product · 30 dead tile links surfaced · /collections/other browsable with 337 archived products flagged urgent · 39 INVESTIGATE flagged for human review · output data/reports/collection-audit-2026-05-13.md |
| COLLECTION-CLEANUP-APPLY | Apply audit dispositions — 164 collections unpublished | ✅ | commit 737f6f6 | 2026-05-13 (Sub-step C2) · applied audit dispositions · 164 collections unpublished (161 ARCHIVE + 3 REDIRECT) · 18 unenriched stragglers stripped of brand:global-teknion tag · global-teknion smart collection rule converted to disjunctive (GFG OR Teknion), now 72 products · /collections/other unpublished · 10 dead tile blocks removed from 4 category templates · 1 dead link updated · 164 redirects added to data/url-redirects-bulk.csv · Steve must manually import redirects via Shopify Admin |
| BRAND-CALLOUT-AUDIT | Audit + fix brand callouts on Phase 2 category pages | ✅ | commit 326241f | 2026-05-13 (Sub-step D, Step 14) · audited 10 Phase 2 templates · 6 templates updated · Keilhauer callouts removed from business-furniture/seating/boardroom (0 products) · ergoCentric callouts removed from business-furniture/seating/ergonomic-products (1 product) · 2 dead brand tiles removed from seating · GFG callout added to storage/tables/boardroom (→ /collections/global-teknion, 72 products) · Global/Teknion callout kept on desks/panels (valid) · accessories/quiet-spaces unchanged · brand plates band deferred to BRAND-PAGES-1 (Step 24) · audit report: data/reports/brand-callout-audit-2026-05-13.md · backups: data/backups/brand-callout-audit-20260513-190930/ |

---

## Wave G — Phase 5: Product + system templates

**Pre-req:** Wave C complete (so brand pages link to live trust pages). Independent of Wave D.
**Goal:** Rebuild the PDP template + add the missing system pages (Customer Stories, custom 404, smart collections, blog templates) before audit + launch waves run.
**Why before Wave E:** Wave E hardening runs perf / a11y / link-rot / schema audits on every page in the `bbi_landing` gate. Running those before the PDP rebuild means re-running them after — wasted work. Build everything, then audit once. The user explicitly accepted slower launch in exchange for first-time-right.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| PB-PDP-1 | Extend `bbi_landing` gate for `template == 'product'` | ✅ | `theme/layout/theme.liquid` line 90–91 | Confirmed present by Stage 4a audit (`stage-4a-decision.md` §1). Gate already includes `template == 'product'`. No action needed. |
| PDP-1 | Build `ds-pdp-base.liquid` section + `product.json` template | ✅ | `theme/sections/ds-pdp-base.liquid` (32 KB) + `theme/templates/product.json` on dev theme 186373570873. Gallery `<bbi-pdp-gallery>` Web Component (thumbnail swap); Quote-only CTA when price==0 or available==false (BBI Rule #2); spec table from all 12 `specs.*` metafields; related products from type-tag category collection (max 4); 4-level breadcrumb; `bbi-nav active=shop` + `bbi-footer`. JSON-LD placeholder comment left for PDP-2. | Hero gallery (carousel + zoom from `product.images`); spec table from PE-2 metafields (`product.metafields.specs.*`); **Request a Quote CTA auto-rendered when `product.price == 0` OR `product.available == false`** (BBI rule #2 — unbuyable items stay live as lead-capture pages); related products (same `type:*` tag, max 4); 4-level breadcrumb (Home > Shop Furniture > Category > Product); renders `bbi-nav` (active=`shop`) + `bbi-footer`. Use `image_url` + `image_tag` for responsive srcset; lazy-load below-fold images per CLAUDE.md performance rules. |
| PDP-2 | Wire JSON-LD into `ds-pdp-base` (absorbs AI-3) | ✅ | `theme/snippets/bbi-product-jsonld.liquid` + `theme/snippets/bbi-breadcrumb-jsonld.liquid` on dev theme. 24/24 source checks green (Product schema fields, InStock/OutOfStock branches, price==0 branch, calls breadcrumb snippet, 4-level BreadcrumbList). Note: `?preview_theme_id` requires admin session auth — source verification used. Rich Results Test to run in Wave E SEO-AUDIT-1. | **Absorbs AI-3 (Product schema on every PDP) — that row removed from Wave E.** Product JSON-LD: `name`, `description`, `image`, `offers` (price + availability + `priceCurrency: CAD`), `brand`, `sku`, `mpn` if present. Renders shared `bbi-breadcrumb-jsonld.liquid` snippet from AI-6 (don't duplicate breadcrumb logic). Validate with Google Rich Results Test on 3 PDPs (Hero in-stock, Hero sold-out, $0 showcase). |
| PDP-3 | PDP smoke test — 5 product states | ✅ | `data/reports/pdp-smoke-20260508.csv` — 34/34 checks green across 5 states. Real Shopify products used: (a) l-shape-desk (in-stock, price=1179.99), (b) anda-seat (sold-out, deny policy), (c) additional-services (price=$0), (d) 2600-series-4-drawer (11 spec metafields), (e) l-shape-desk (sparse/no-specs guard). Source + API verification; browser auth required to verify via ?preview_theme_id. | Test 5 PDP states: (a) in-stock priced Hero, (b) sold-out, (c) $0 showcase, (d) Hero with full spec metafields, (e) non-Hero with sparse metafields. DOM assertions per page: `bbi-header=1`, `bbi-footer=1`, Starlite suppressed, breadcrumb 4-level, Product JSON-LD valid, Quote CTA visible on (b)+(c) only. |
| CS-1 | Customer Stories page (`/pages/customer-stories`) | ✅ | `theme/sections/ds-lp-customer-stories.liquid` + `theme/templates/page.customer-stories.json` exist; Page ID 170838884665 published 2026-05-07 | Phase 1 API check (2026-05-08): exists, published, suffix `customer-stories` ✅. Content (story cards, testimonials) not yet wired — content work, not scaffolding. | Page hero + industry filter chips (healthcare, education, government, non-profit, professional-services) + story cards (image, pull-quote, customer name, industry tag, link to full case study). Review schema (`schema.org/Review`) per testimonial. Seed from `data/oci-photos/catalog.json` (48 photos) + `docs/strategy/voice-samples.md`. **Cross-linked from:** homepage Rule 6 ("Read customer stories →"), About page, 5 industry pages, 3 brand pages. Site architecture §2j flags as ⭐ priority. |
| 404-1 | Custom 404 page (`templates/404.json`) | ✅ | `theme/sections/ds-system-404.liquid` + `theme/templates/404.json` on dev theme; gate `template == '404'` already present in theme.liquid. Note: Shopify does not honour `?preview_theme_id` for 404 responses — asset presence verified via Admin API (both files 200 OK on theme 186373570873). | Branded 404 — H1 "Page not found" + brief copy + search box (`/search` form) + 4 top category tiles (seating, desks, storage, tables) + phone CTA + Quote button. Add `template == '404'` to `bbi_landing` gate. Smoke test by hitting any garbage URL on dev theme. |
| SMART-1 | Smart collections — 10 "view all" + 4 brand-filtered | ✅ | `scripts/create-smart-collections.py`; `data/reports/smart-collections-20260508_163930.csv`; 14/14 live on Shopify (all-seating … all-business-furniture, keilhauer, global-teknion, ergocentric, oecm-eligible). keilhauer/global-teknion/ergocentric were custom collections — converted via `--convert-custom` flag. | Create 14 smart collections via Shopify Admin API. **10 "view all" per category** (`all-seating`, `all-desks`, `all-storage`, `all-tables`, `all-boardroom`, `all-ergonomic`, `all-panels`, `all-accessories`, `all-quiet-spaces`, `all-business-furniture`) — rule: tagged `type:<category>`. **4 brand-filtered** (`keilhauer`, `global-teknion`, `ergocentric`, `oecm-eligible`) — rule: tagged `brand:<brand>` or `oecm-eligible`. Reuses smart-collection helper from PB-14. Backup current collection list before running; `--dry-run` default. Wired up by category-page "View all" CTAs (already in interlinking-map). |
| BLOG-TPL-1 | Blog + Article templates (empty — content deferred) | ✅ | `theme/sections/ds-blog-list.liquid` + `theme/templates/blog.json` + `theme/sections/ds-article.liquid` + `theme/templates/article.json` on dev theme; `template.name == 'blog'` and `template.name == 'article'` added to bbi_landing gate in theme.liquid. Assets verified via Admin API (all 200 OK). | BBI-styled templates only — no posts yet. **Resources hub** (paginated list, category filter chips, optional tag filter, related products from collection metafield). **Article** (hero image, prose body, related products module, FAQPage schema if `article.metafields.faq` exists, share buttons, author/date metadata). Add `template == 'blog'` and `template == 'article'` to `bbi_landing` gate. First posts (BL-1..BL-6 + B1..B10) stay in post-launch backlog per CLAUDE.md (every post starts with DataForSEO keyword research). |

---

## Wave E — Pre-launch hardening

**Pre-req:** Waves A + C complete.
**Goal:** All schema, copy, lead routing, nav, design system verified before launch gate.

| ID | Task | Status | Evidence | Notes |
|---|---|---|---|---|
| AI-4 | Organization schema on homepage + About | ✅ | `theme/snippets/bbi-org-schema.liquid` rendered from `bbi-nav.liquid` (fires on every BBI page) | `Organization` + `LocalBusiness` JSON-LD: `name`, `url`, `logo`, `telephone`, `address`, `areaServed`, `sameAs`. Renders from nav so every BBI-gated page gets it automatically. |
| AI-6 | BreadcrumbList JSON-LD via shared snippet | ✅ | `theme/snippets/bbi-breadcrumb-jsonld.liquid` + wired to `ds-pdp-base` (via `bbi-product-jsonld`) + `ds-cc-base` + `ds-cs-base` · pushed to dev `186373570873` 2026-05-11 | Snippet built (up to 4 levels, blanks omitted). Wired: PDP = 4-level via bbi-product-jsonld; cc-base = 2-level (no parent) or 3-level (with parent label); cs-base = 4-level (Home > Shop Furniture > Category > Sub-collection). Validates against Rich Results Test in SEO-AUDIT-1. |
| AI-7 | Entity-clarity copy on homepage | ✅ | branch `feature/ai-7-ai-8` · DEV 186373570873 pushed 2026-05-20 · `theme/templates/index.json` (bbi-hero settings refresh + new `bbi-about` custom-liquid section between bbi-trust and bbi-shop) | Version B (plainspoken) selected over A/C. Hero now leads "Canadian-owned · Since 1964" + new H1/deck/sub surfacing Agreement 2025-470. New "Who we are" body section (~150 words) names Brant Basics ↔ BBI entity relationship, 296 George St N Peterborough HQ, GFG/OTG/Heartwood/ObusForme + 25 more authorized lines, Ontario institutional + private-sector buyers split, ON+Western install. 3-cell glance row (Founded · OECM · Reach). Hero + entity section = ~200 words above the fold answering who/what/who-serve/where. Per Steve direction 2026-05-20, ugoburo About-page opener pattern (`docs/strategy/competitor-audit-ugoburo.md`). |
| AI-8 | OECM page copy hardening | ✅ | branch `feature/ai-7-ai-8` · DEV 186373570873 pushed 2026-05-20 · `theme/sections/ds-lp-oecm.liquid` + `theme/templates/page.oecm.json` | Version A (comprehensive) selected. NEW Coverage Table section (between Intro and Differentiators) — 7-row matrix Category × GFG · OTG · Heartwood · ObusForme · Total = 177 storefront-callable products under Agreement 2025-470. NEW How-to-Purchase 3-step section. NEW Entity note between proof bar and crosslinks (Brant Basics OECM-registered entity sentence). Hero badge/heading/standfirst/caption refreshed to surface Agreement 2025-470. 3 factual errors fixed (Card 03: 1962→1964, Brantford→296 George St N Peterborough; Card 04: brand list reordered GFG/OTG/Heartwood-led; Proof-bar stat 01: "2019 OECM vendor since"→"2025-470 OECM Agreement number"). Intro paragraph 2 rewritten to drop "since 2019" claim; paragraph 3 replaces self-link with service-channel inventory (quote 1bday/free design/install/warranty/PO billing). 6 existing FAQs replaced with 8 procurement-focused Q&As. FAQPage + GovernmentService JSON-LD already in place — auto-builds from new FAQ blocks. Counts verified live against Shopify Admin API. Per ugoburo NMSO contract-table pattern (`docs/strategy/competitor-audit-ugoburo.md`). |
| AI-9 | FAQ blocks on category pages | ⬜ | 9 category pages | 3–5 Q&A per category, FAQPage schema |
| AI-5 | FAQ schema on OECM, Design Services, top blog posts | ✅ | branch `feature/ai-5` · DEV 186373570873 (no writes) · audit-only confirmed via Asset API + simulated emit | **Verified — no theme writes required.** Session B (commit 6c33b60) already shipped both the `HowTo` and `FAQPage` JSON-LD blocks in `theme/sections/ds-lp-design-services.liquid` (lines 14–42), plus 5 `faq_item` blocks in `theme/templates/page.design-services.json`. Pattern mirrors canonical `ds-lp-oecm.liquid` emit (`section.blocks \| where: "type", "faq_item"` → `name` + `acceptedAnswer.text \| strip_html \| json`). Simulated emit parses cleanly (5 valid Q&As). **OECM no-regression check:** deployed `ds-lp-oecm.liquid` FAQPage block intact at lines 322–334 inside `@graph` alongside GovernmentService; `page.oecm.json` has 8 `faq_item` blocks (matches AI-8); simulated emit parses cleanly. **Blog post status:** 1 published article (_How to adjust your chair_) currently emits no `BlogPosting` JSON-LD — `ds-article.liquid` has FAQPage emit (conditional on `article.metafields.faq.items`) but no Article-type schema. Gap deferred to BLOG-SEED-1 (Step 36, post-launch backlog). |
| LEAD-2 | Gap analysis on lead routing | ⬜ | `docs/plan/bbi-lead-routing.md` | Identify duplicate forms, inconsistent inboxes |
| **LEAD-INBOX-1** | **Provision + verify lead-form inboxes (HARD PREREQ for LEAD-3)** | ✅ | commit `b6a6855` · aliases confirmed · test emails received 2026-05-14 | Three aliases (`quotes@`, `design@`, `info@`) added to `steve@brantbusinessinteriors.com` in GoDaddy M365 admin. SPF updated to include `spf.protection.outlook.com`. DMARC updated to add `rua=mailto:dmarc-reports@brantbusinessinteriors.com`. DKIM already active (selector1). Test emails from external domain confirmed received at `steve@`. |
| LEAD-3 | Unify on `bbi-lead-form.liquid` snippet + modal + per-type routing + auto-replies | 🟡 | commit TBD (this session) · `theme/snippets/bbi-quote-modal.liquid` + `theme/sections/ds-lp-design-services.liquid` pushed to DEV 186373570873 · `docs/strategy/bbi-lead-routing.md` | **Routing wired (Option D — subject-line injection).** `contact[subject]` hidden field added to modal; JS populates per lead_type: quote→`[Quote Request]`, design→`[Design Consultation]`, oecm→`[OECM Inquiry]`, contact→`[General Contact]`. Design Services broken `mailto:` form replaced with `data-bbi-quote-trigger data-lead-type="design"` button. **Steve's 3 manual follow-ups required before ✅:** (1) Update Shopify `customer_email` → `info@brantbusinessinteriors.com` (Shopify Admin → Settings → General — API returned 406, cannot automate); (2) Verify subject-line behaviour + set M365 inbox rules (Path A: subject rules if SMTP subject shows tag; Path B: body rules if generic subject — see routing doc); (3) Set M365 auto-replies on quotes@/design@/info@. Full instructions + test plan: `docs/strategy/bbi-lead-routing.md`. |
| INTERLINK-3 | Final cross-link audit, all pages | ⬜ | audit output green | |
| **SEO-AUDIT-1** | **Technical SEO audit via DataForSEO MCP (HARD GATE)** | ✅ | branch `feature/seo-audit-1` · DEV 186373570873 · `data/reports/seo-audit-1-2026-05-26.md` + `data/working/seo-audit-1-2026-05-26/` (crawler + halt-1.5 copy review + apply-fixes.py + before/after JSONs) + `data/backups/seo-audit-1-fix-batch-pre-20260526-165131/` (rollback snapshot) | **Pre-launch hard gate ✅ PASSED 2026-05-26 evening. Verdict: READY FOR LAUNCH-0.** 39 bbi_landing URLs crawled via cookie-session DEV preview + DataForSEO Lighthouse on top 5 templates. **0 BLOCK / 15 FIX (all in-scope FIXes applied via Claude Code Admin API — zero Steve work) / 3 WAIVE.** Fixes applied: 2 theme edits (`meta-tags.liquid` for og:title/desc/image override + `theme.liquid` title-suffix logic broadened); 68 metafield writes (33 title_tag + 29 description_tag + 6 retries after Shopify 2-call/sec rate cap); 2 URL redirects + 2 page unpublishes (LEAK fixes for /pages/ergocentric + /pages/how-to-adjust-my-new-chair, both → /pages/brands-ergocentric); `data/llms-txt-draft.md` refreshed (7 stale items fixed; deployment path WAIVED post-launch since Shopify auto-generates `/llms.txt` with pageType=llms_txt, no override hook documented). Before/after: meta-desc coverage 13/39 → 39/39; stale "BBI and Office Central specialize" og:description 29/39 → 0/39; title length >140 chars 2 → 0; H1=0 LEAK pages 2 → 0. Lighthouse desktop perf ≥81 on all 5 templates; CWV pass on 4/5 (PDP LCP 2585ms is 85ms over, WAIVED). LIVE `updated_at = 2026-05-16T16:47:22-04:00` verified 7× during audit. Theme check baseline 166/2855 unchanged. |
| NAV-VERIFY | Homepage + collection pages render shared nav | ⬜ | DOM check | Verify NAV-3, NAV-4 stuck |
| DS-VERIFY | DS pre-launch verification (HARD GATE) | ⬜ | screenshot diff vs T5 locked | Brand-red unified, dark-mode block stays deleted, tokens intact |
| IMG-PHASE2 | Product image regen (≥80% coverage SOFT GATE) | ⬜ | `data/reports/img-phase2-coverage.csv` | Waiver CSV for the rest. · **SCOPE NOTE 2026-05-21:** folds into the Day 9 image session — see CURRENT FOCUS Day 9 + ACTIVE STEPS → IMAGE-SOURCING-V2 (tracker Step 46), scope expanded to also cover Task #13 homepage image rot + ALL tile images sitewide + customer-stories case-study images + brand-page heroes. · **CONSOLIDATED 2026-05-21 (Day 8 audit):** removed from the ACTIVE STEPS navigation layer + the tracker active-work cards — folded entirely into Step 46 IMAGE-SOURCING-V2 (the Day 9 umbrella). This canonical Wave E row is retained as the historical record per the file's preserve-the-record rule. Note: NAV-VERIFY (a separate completed step, commit 3aa74c3) was NOT a duplicate of this row and was left intact; the Day 8 audit prompt's "two IMG-PHASE2 duplicates" premise was incorrect — there is only one IMG-PHASE2. |
| PERF-AUDIT-1 | Lighthouse + Core Web Vitals on top 10 pages | 🟡 | `data/reports/perf-audit-2026-05-14.{csv,md}` · commit `036b232` | **Phase 1 complete (live Avada baseline) — Phase 2 required post-LAUNCH-2.** Phase 1 ran PSI API (mobile) against the current LIVE theme (Avada) — NOT the new BBI Landing Dev theme. Dev theme preview requires admin browser session; external crawlers cannot access it. Results: avg score 63, **10/10 FAIL** (all pages LCP > 4 000ms — Avada JS/plugin bloat). These scores reflect what we're replacing, not what we're launching. **Phase 2 (required for ✅):** re-run post-LAUNCH-2 against `brantbusinessinteriors.com` without `?preview_theme_id` to get authoritative new-theme scores. Target: mobile Lighthouse ≥ 80 per CLAUDE.md. |
| A11Y-AUDIT-1 | WCAG 2.1 AA audit on top 10 pages | ⬜ | TBD `data/reports/a11y-audit-<date>.csv` | axe-core or pa11y CLI on the same 10 pages. Hard fails: missing alt text, no form labels, contrast < 4.5:1, focus traps broken, keyboard gaps. Per-page issue list. |
| LINK-ROT-1 | Internal + external link 200/404 sweep | ⬜ | TBD `data/reports/link-rot-<date>.csv` | Crawl every `<a href>` across all bbi_landing pages. Internal: assert 200. External: flag 404/500/timeouts. |
| SYS-VERIFY-1 | System pages (cart / search / account / password) chrome verification | ⬜ | TBD `data/reports/system-pages-verify-<date>.csv` | DOM check on `/cart`, `/search`, `/account/login`, `/account/register`, `/account`, `/password`. **Note:** `/search` is intentionally BBI-styled (NAV-5) — `templates/search.json` uses `bbi-nav-wrap` + `ds-search-results` + `bbi-footer-wrap`; no gate entry needed. `/cart` already in gate (STAB-1). Verify: no double header/footer on account/password pages, search + cart flows functional, account/register/password still render Starlite chrome intact. |
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
| **LAUNCH-3** | **GSC sitemap re-submit + GA4 verification** | ✅ | GSC sitemap index — `data/working/launch-chain-2026-05-26/launch-3-verification.md` | **2026-05-26 ~21:00** — Theme-side automated verification: sitemap.xml HTTP 200 → sitemap index → **822 URLs** (587 products + 23 pages + 208 collections + 2 blogs + 1 agentic-discovery); 20/20 sampled URLs return HTTP 200 (0 broken inclusions); robots.txt HTTP 200 with Sitemap directive + no blanket disallow + intentional UCP/MCP-aware AI bot policy. **GA4 wiring `G-XLCM9LCNLN`** present on all 5 sampled pages (homepage, /pages/oecm, /pages/about, /pages/quote, sample PDP) via Shopify Customer Events / Web Pixels native integration with pre-wired ecommerce events (view_item, begin_checkout, search, purchase). **Zero Avada residual tracking** site-wide (0 UA-* legacy / 0 Avada/foxtheme refs / 0 stray FB pixel). **GSC manual:** sitemap already submitted under earlier W0-1 setup; **GSC processed 824 discovered pages on 2026-05-24** with all 5 sub-sitemaps status=Success; URL Inspection on / and /pages/oecm both returned **"URL is on Google" + Page is indexed + HTTPS** (best possible state, no re-submit needed). **GA4 manual:** Realtime shows **6 active users last 30 min / 9 page_views** on real GTA traffic; event stream confirms `page_view`, `first_visit`, `session_start`, `user_engagement`, `scroll`, **`view_item`** (ObusForme PDP — proves Shopify Web Pixels ecommerce path firing end-to-end); Web stream "Data collection active in past 48h" + Google tag "Data flowing". **Week 1 polish backlog added below.** |
| LAUNCH-4 | Mobile smoke test (Chrome, Safari, Firefox, iOS, Android) | ⬜ | screenshots saved | |

---

## Backlog (post-launch)

These compound after live, none blocks launch:

- **Phase 1b full catalog** — PE-5/6/7 for the 503 non-Hero products (descriptions, specs, meta)
- **Blog** — BL-1..BL-6 (template + schema + related products) + first 10 posts (B1..B10). **🔍 Every blog post must start with DataForSEO MCP keyword research** — pull search volume, difficulty, related keywords, SERP competitors, and "people also ask" before drafting. Target keyword + 2–3 secondary keywords go in the brief; the post is written to rank for them.
- **SEO-AUDIT-2 — Cross-page keyword optimization (DataForSEO MCP)** — once the full site is built (post-LAUNCH-2), run a site-wide keyword audit: pull current rankings, identify cannibalization (multiple pages competing for the same keyword), find gaps (high-intent keywords with no landing page), and reassign primary/secondary keywords per page. Output: `docs/strategy/bbi-keyword-map-<date>.md` with one row per page (URL, primary KW, secondary KWs, search volume, current rank). Then patch meta titles, H1s, and intro copy across pages to align.
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
| AI-4..AI-9 | Schema + copy work | ⬜ | see Wave E (AI-3 absorbed into PDP-2 in Wave G; AI-10..AI-11 in backlog) |

---

## Open questions / decisions pending

1. **Canonical nav** — landing pages render `Shop · Brands · Verticals · Our work · Services · About`, spec says `Shop Furniture · Industries · Brands · Services · About`. NAV-1 needs Steve's call.
2. **brand-dealer reconciliation** — section file is on a separate branch, suffix is in the gate. Merge or de-gate? (PB-13)
3. ~~**BBI logo** — `bbi-logo-v2` is Brant Basics wordmark. Lock it or source a true BBI wordmark? (CONTENT-1)~~ → **RESOLVED 2026-05-20: lock `bbi-logo-v2`** (no schedule impact; revisit only if a distinct BBI wordmark is later desired).

---

### Resolved 2026-05-20 (Wave E execution planning)

- **BRAND-PAGES-1 build approach → Approach A** (copy an existing per-brand section per new brand: clone `theme/sections/ds-lp-brands-ergocentric.liquid`, rescope `.lp-ergo`→`.lp-<brand>`, swap copy). Not the generic Approach B.
- **Global / Teknion page → Option A** (keep the existing `brands-global-teknion` page bundled; rename/expand to a GFG-family experience — copy/scope update, not a rebuild).
- **CONTENT-1 logo → lock `bbi-logo-v2`.**
- **Build venue → Claude Code.** BRAND-PAGES-1 + the rest of the Wave E chain are to be built in Claude Code, not Cowork. Handoff: `docs/plan/bbi-brand-pages-1-handoff-2026-05-20.md`; full plan: `docs/plan/wave-e-execution-plan-2026-05-20.md`.
- **New brand pages to build:** OTG (`brands-otg`, 54 products), Heartwood (`brands-heartwood`, 17), ObusForme (`brands-obusforme`, 5) + 24 brand×category smart collections + gate suffixes + Brands Hub tiles + A11Y-AUDIT-1.
4. **Smart Collection migration timing** — confirmed: before Phase 3 (Wave B step 1)
5. **Customer Stories source content** — CS-1 (Wave G) needs 5–8 testimonials with photos. Pull from `data/oci-photos/catalog.json` (project photos) + voice-samples.md, or does Steve have testimonial copy approved by clients we can quote on the public site? Permission matters for Review schema.

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
