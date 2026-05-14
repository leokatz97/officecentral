# BBI Launch Tracker — Archive

_Comprehensive history + completion notes for the BBI launch project. The live tracker artifact (`bbi-launch-tracker` in the Claude.ai sidebar) shows current status only. This doc captures the full detail that previously lived inline._

_Last sync: 2026-05-14._

## How this doc relates to the live tracker

- **Live tracker** (Cowork artifact `bbi-launch-tracker`): status badges + step titles + brief descs + Right Now callout. Updated after every step completion. Loads fast.
- **This archive** (`docs/project/launch-tracker-archive.md`): completion notes + Wave history + decision log + ship lists. Updated less frequently. Read when planning the next step or needing context on what shipped when.

---

## Phase 1 completion details

13 of 15 steps done. Remaining: Step 2 (BUG-FIX-2) + Step 3 (BUG-FIX-3) — OECM investigation + remediation.

### Step 1 — VENDOR-NORMALIZE-1 ✅ Done 2026-05-12

Build canonical brand vocabulary.

89% of active products (526 of 593) still had vendor = "Brant Business Interiors" placeholder from the Office Central migration. 152 products had `specs.manufacturer` metafields but with 20+ string variants for Global Furniture Group alone. Real brand distribution: ~113 Global family · ~17 Heartwood · long tail. Read all specs.manufacturer strings + Shopify vendor field + any existing brand:* tags.

**Completion:** Canonical brand map built at `docs/strategy/brand-canonical-map.md` + `.csv`. 20 canonical brands resolved from 152 enriched products (later expanded to 30 via CANONICAL-MAP-ADDITIONS in Sub-step A). 4 storefront-callable: OTG / Offices to Go (54), Global Furniture Group (53), Heartwood Manufacturing Ltd. (17), ObusForme (5). Foundation for VENDOR-NORMALIZE-2 + INNOVATIONS-FIX + all canonical map work.

**POST-AUDIT GAPS noted:** TAG-AUDIT-1 surfaced 3 brands missing from the canonical map — Safco (4 products), Humanscale (2 products), and the brand:heartwood slug needs migration to brand:heartwood-manufacturing-ltd (1 product). Folded into COLLECTION-CLEANUP-1 (Step 10).

Commits: `d9c6e04`

---

### Step 4 — VENDOR-NORMALIZE-2 ✅ Done 2026-05-12

Apply canonical brands to all data sources.

For the 152 products with specs.manufacturer already populated: normalize the metafield string against VENDOR-NORMALIZE-1's canonical map · set Shopify vendor field to match · apply the correct `brand:<canonical>` tag. For the 441 unenriched products: SKIP — handled inside PE Pass 3 batches via vendor_override population.

**Completion:** 152 products written end-to-end (vendor field + specs.manufacturer metafield + brand:* tag all agree per product). 8/8 verification sample passed.

Commits: `5cdbb62`

---

### Step 5 — TAG-AUDIT-1 ✅ Done 2026-05-12

Audit all tag prefixes for mass-application issues.

Sweep all tag prefixes in use (`brand:*`, `room:*`, `type:*`, `oecm-eligible`, plus anything else surfaced) and report counts per tag value across the catalog.

**Completion:** 593 active products audited, 40 unique tags, 4 anomalies flagged. Key finding: industry:business mass-tagged on 548/593 (92%) — new bug, scoped to TAG-INDUSTRY-CHECK (Step 6). Plus 3 brand canonical map gaps: Safco (4 products), Humanscale (2 products), and brand:heartwood slug fix (1 product). Output: `data/reports/tag-audit-2026-05-12.md`.

Commits: `fc8b4ff`

---

### Step 6 — TAG-INDUSTRY-CHECK ✅ Done 2026-05-13

Investigate industry:* tag system + decide retire vs design vocabulary.

TAG-AUDIT-1 surfaced industry:business on 548/593 products (92% — same mass-tag pattern as OECM). Plus industry:healthcare on 1 and industry:daycare on 1 (singletons). Read-only investigation: grep `theme/templates/page.*.json` and `theme/sections/` for the string "industry:" to determine whether the industry landing pages actually filter products by industry:* tag.

**Completion:** Classified as PARTIALLY ALIVE. One real storefront use: business-furniture smart collection has 3 'tag not_equals industry:*' exclusion rules (keeps daycare strollers + bariatric healthcare chair out of business furniture). One non-use: 548 products carry industry:business but no Liquid reads it and no smart collection includes on it — orphaned data. All 6 industry landing pages (industries, healthcare, education, government, non-profit, professional-services) are purely editorial with zero tag filtering. Recommendation: fold remediation into BUG-FIX-3 scope. Output: `data/strategy/industry-tag-decision.md`.

Commits: `e669122`

---

### Step 7 — BUG-FIX-4 ✅ Done 2026-05-13

Upload OCI photos + fix Our Work page.

48 OCI photos in `data/oci-photos/` had not been uploaded to Shopify CDN; `/pages/our-work` was rendering with broken images. Source: DEBT-04.

**Completion:** 12 OCI photos uploaded to Shopify Files via GraphQL staged-upload pipeline (all READY on first poll). `page.our-work.json` template patched — photo_1 through photo_12 populated with `shopify://shop_images/` GIDs. 12/12 slots verified in DEV theme. 3/3 spot-check URLs return HTTP 200 image/jpeg. `/pages/our-work` no longer renders placeholder boxes. DEBT-04 resolved. Pattern established for PAGE-IMG-1 (Phase 3 Step 16) to upload the remaining 56 empty image slots.

Commits: `588ce31` (template), `71cdaf3` (build state)

---

### Step 8 — PE-PASS-3 ✅ Done 2026-05-13

Run remaining 3 enrichment batches (~82 products).

Batches: Batch 3 Chairs Pt3 (25) · Batch 4 Desks Pt1 (27) · Batch 6 Storage (30). Each batch is a self-contained prompt at `BBI-Session-Kickoff/enrichment-prompts/`. After each: re-run `scripts/push-pe3-enrichment.py --live`.

**Batch 3 (2026-05-12):** 19 products enriched (13 Global Furniture Group, 5 OTG, 1 ObusForme), 0 fallbacks, 0 push failures. All Batches 1+2 descriptions / vendor field / brand tags also went live in the same push — push script bugs surfaced + fixed (see PUSH-FIX-1 in Wave H history).

**Batch 4 (2026-05-13):** 25 products live (9 OTG, 7 GFG, 2 Office Star, 1 Fellowes, 1 Heartwood, 5 BBI fallback). 5/5 storefront verification. Surfaced Victor Technology, Rocelco, HDL as canonical map additions. Re-push idempotency confirmed safe.

**Innovations fix (2026-05-13):** Innovations re-attributed from Global Furniture Group to Heartwood Manufacturing Ltd. (is_standalone=False, parent=Heartwood). 5 products re-tagged. Surfaced during Batch 4 research, confirmed via heartwooddl.com.

**Batch 6 (2026-05-13):** 30 products live (9 Heartwood, 7 OTG, 4 Fellowes, 1 Deflecto, 9 BBI fallback). 5/5 storefront verification. Surfaced Kensington, Sentry Safe, FireKing, Tayco as canonical map additions.

**Final progress:** 143 of 157 products enriched and live on storefront. Remaining 14 are routed-to-Other or intentional skip rows.

Commits: `d898b12` (Batch 4), `a4582ea` (INNOVATIONS-FIX), `a44d14c` (Batch 6)

---

### Step 9 — PE-PASS-3-REVIEW ✅ Done 2026-05-13

Generate review Excel, approve rows, live-push all approvals.

**Completion:** Review pattern executed via per-batch dry-run + 5-product storefront verification in Batches 3, 4, 6. Review file pattern (3-sheet XLSX with `steve_approve` column) established for future enrichment passes.

---

### Step 10 — CANONICAL-MAP-ADDITIONS (Sub-step A) ✅ Done 2026-05-13

Add 10 new brand entries to canonical map.

PE Pass 3 + TAG-AUDIT-1 surfaced 10 brand entries missing from the canonical brand map: Safco (4 products) · Humanscale (2) · Victor Technology LLC (1) · Rocelco (1) · HDL (1) · Kensington (1) · Sentry Safe (2) · FireKing (1) · Tayco (1) · plus the brand:heartwood slug migration (1 product).

**Completion:** 9 new canonical brand entries added to `docs/strategy/brand-canonical-map.md` + `.csv` (Safco 4, Humanscale 2, Victor Technology LLC 1, Rocelco 1, HDL 1, Kensington 1, Sentry Safe 2, FireKing 1, Tayco 1). Heartwood slug migration documented in notes. Canonical brand total: 20 → 30.

Commits: `29bcbad`

---

### Step 11 — APPLY-MAP-ADDITIONS (Sub-step B) ✅ Done 2026-05-13

Re-tag the ~14 affected products to match new canonical entries.

For the 14 products affected by Sub-step A's canonical map additions, update vendor field + specs.manufacturer metafield + brand:* tag per product to match the new canonical names. Same pattern as VENDOR-NORMALIZE-2 and INNOVATIONS-FIX.

**Completion:** 15 products re-tagged across 9 canonical brands. Vendor field + specs.manufacturer metafield + brand:* tag now agree per product. 15/15 verification clean. Heartwood slug migration found to be already complete (0 stragglers). After this step ALL catalog data is consistent with the canonical brand map.

Commits: `66a0bff`

---

### Step 12 — COLLECTION-AUDIT (Sub-step C1) ✅ Done 2026-05-13

Audit all collections + propose dispositions (read-only).

Pull every collection (smart + custom), count products, identify those at 0, 1, or 2 products. For each, decide disposition: archive / merge / redirect / keep-with-quote.

**Completion:** 371 collections audited (49 smart, 322 custom). 148 zero-product collections found. Dispositions proposed: 150 ARCHIVE, 3 REDIRECT, 39 INVESTIGATE, 93 KEEP-WITH-NOTE, 86 KEEP. Surfaced `/collections/other` urgent fix (337 archived products browsable) + 30 dead tile links on live category pages. Output: `data/reports/collection-audit-2026-05-13.md`.

Commits: `a24b9e3`

---

### Step 13 — COLLECTION-CLEANUP-APPLY (Sub-step C2) ✅ Done 2026-05-13

Apply audit dispositions + urgent fixes + theme cleanup.

**Completion (multi-phase):**
- Phase 1 urgent hotfixes: unpublished `/collections/other` (337 archived products no longer browsable) · hotfix global-recliner-primacare (VN2-missed product) · fix OTG mis-tag (offices-to-go-ultra-high-back-tilter)
- Phase 2: 18 unenriched stragglers stripped of brand:global-teknion tag · global-teknion smart collection rule converted to disjunctive (GFG OR Teknion), now 72 products
- Phase 3: 164 collections unpublished (161 ARCHIVE + 3 REDIRECT). Active collection count: 371 → 207
- Phase 4: 10 dead tile blocks removed from 4 category templates (collection.tables/storage/accessories/seating.json) + 1 dead link updated
- Phase 6: 164 redirects added to `data/url-redirects-bulk.csv` (Steve must manually import via Shopify Admin → Navigation → URL Redirects)

5/5 verification clean.

Commits: `737f6f6`

---

### Step 14 — BRAND-CALLOUT-AUDIT (Sub-step D) ✅ Done 2026-05-13

Audit + fix brand callouts on Phase 2 category pages.

Audit each Phase 2 category page's brand callout sections. Current callouts pointed at Keilhauer (0 products) and ergoCentric (1 product).

**Completion:** 10 Phase 2 category pages audited. 6 templates updated with 14 block edits:
- Removed: Keilhauer callouts from business-furniture, seating, boardroom (0 products)
- Removed: ergoCentric callouts from business-furniture, seating, ergonomic-products (1 product)
- Removed: 2 dead brand tiles from seating
- Added: GFG callouts on storage, tables, boardroom (→ /collections/global-teknion, 72 products)
- Kept: Global/Teknion callouts on desks, panels (valid)
- Unchanged: accessories, quiet-spaces

4 templates unchanged (desks + panels-room-dividers + accessories + quiet-spaces). 6/6 DEV theme verification. Deferred to BRAND-PAGES-1 (Step 24): OTG + Heartwood callouts and brand plates band swap — both require OTG + Heartwood brand collections to exist first. COLLECTION-CLEANUP arc (Sub-steps A → D) now closed.

Audit report: `data/reports/brand-callout-audit-2026-05-13.md`. Backups: `data/backups/brand-callout-audit-20260513-190930/`.

Commits: `326241f` (templates), `af7f75f` (build-state)

---

### Step 15 — PROMPT-5 ✅ Done 2026-05-13

Image slot audit (read-only).

Grep `image_picker` schemas across sections + snippets · cross-reference template JSONs · output CSV of empty slots with match suggestions from `data/page-images/` + `data/oci-photos/`.

**Completion:** 28 templates audited, 120 image_picker slots found (56 empty, 64 populated). Available images inventoried: 63 in `data/page-images/`, 80 in `data/oci-photos/`. Match quality on empty slots: 9 EXACT + 26 HIGH + 14 MEDIUM + 2 LOW + 3 NO-MATCH (91% actionable). Strongest matches: `page.about` hero → About-us-1.webp, `page.relocation` hero → OCI-Services-Relocation-management.jpg, `page.our-work` 12-photo grid → OCI photos. Output: `data/reports/image-slot-audit-2026-05-13.md` + `.csv`.

**Sub-step extension (PROMPT-5-EXTEND):** Classified 64 populated image slots → 49 KEEP-CURATED (already using BBI curated imagery) · 0 REPLACE-STOCK (Wave A was disciplined, no stock junk) · 4 REPLACE-WRONG-IMAGE (trust_image_1 duplicating hero on education/government/healthcare + Mattamy on non-profit) · 11 REVIEW (Steve decides). PAGE-IMG-1 total scope: up to 71 slot writes. Output: `data/reports/image-slot-audit-2026-05-13-extension.md`.

Commits: `790ec26`, `324df1f` (audit), `e7e0f4b` (extension)

---

## Phase 2 → 5 completion details

No done steps in Phases 2–5 yet. Phase 2 (PAGE-IMG-1) is the current next step after Phase 1 closes.

---

## Wave H history — 2026-05-10 through 2026-05-13

32 entries shipped across Wave H stabilization + enrichment arc. Listed in chronological order.

- **STAB-1** 2026-05-10 · Asset infrastructure recovery — 81 missing CSS/JS synced live→dev · cart chrome architectural fix (template==cart added to bbi_landing gate) · settings_data.json patched
- **PDP-BLACK-FIX** 2026-05-11 · Dark-mode JS guard on product template + CSS override with matching specificity
- **CART-FUNNEL** 2026-05-11 · Cart 404 + header cart badge + ds-cart-base section + polish + mini-cart dropdown · BBI logo v2 in nav/footer
- **PROMPT-2** 2026-05-11 · Buy Now + Quantity stepper wired to `/cart/add.js → /checkout`
- **PROMPT-3** 2026-05-11 · Best-sellers sort site-wide (19 smart collections) · PDP related rewired to 3-tier fallback with capture pattern
- **PDP-LIGHTBOX-1** 2026-05-11 · Gallery lightbox + related-card 4/5 aspect ratio match
- **COLLECTION-DS-1** 2026-05-11 · Default `/collections/*` pages on BBI design system
- **PE-PASS-1** 2026-05-11 · Triage CSV · 553 products audited · 98 A · 12 B · 383 C archive · 60 skip · 52 duplicate clusters · commit `76f109d`
- **PE-PASS-2** 2026-05-11 · All 4 phases complete · Other collection created (id 527013085497) · 336 products moved · 7 batch prompts built · commit `a734c9c`
- **SPEC-JSON-LD** 2026-05-11 · `additionalProperty` in Product JSON-LD on dev + live · commits `5be9b56`, `5f4a3bc`
- **KF-STRIP** 2026-05-11 · Key Features de-dup in About section · commit `5f4a3bc`
- **SPEC-HERO-PUSH** 2026-05-11 · Hero 100 spec gap-fill complete · 99 products pushed
- **HERO-SPEC-SESSIONS** 2026-05-11 · All 4 batches H1A/H1B/H2/H3 + bonus shipped
- **ICP-V2** 2026-05-11 · Approved + cascaded to SKILL.md + 8 enrichment prompts · commit `1d6684c`
- **BLOG-TPL-1** 2026-05-11 · Blog + Article templates shipped (empty, posts deferred)
- **SMART-1** 2026-05-11 · 14 smart collections via Admin API · 10 "view all" + 4 brand-filtered
- **AUDIT-1** 2026-05-12 · Pre-launch tech-debt + state audit · 15 findings · `data/reports/audit-tech-debt-2026-05-12.md` · `data/reports/empty-collections-snapshot-2026-05-12.csv` · 4 blockers promoted to Steps 1–4 · 11 deferred
- **BRAND-INVESTIGATION-1** 2026-05-12 · 593 active products audited · vendor field 89% placeholder · 152 products with specs.manufacturer metafield (20+ string variants per major brand) · real distribution: ~113 Global family / ~17 Heartwood / long tail · Keilhauer 0 + ergoCentric 1 despite brand pages existing · findings folded into `bbi-build-state.md` 'Known Data Hygiene Issues' · surfaced VENDOR-NORMALIZE-1 / -2 + TAG-AUDIT-1 as launch path steps
- **BRAND-INVENTORY-1** 2026-05-12 · Brand-page + collection audit · 3 existing pages found (Keilhauer empty, ergoCentric empty, bundled Global+Teknion healthy at 56 products) · 3 brands missing pages despite real catalog depth (OTG 54, Heartwood 17, ObusForme 5) · 3 legacy 0-product collections flagged for cleanup · `data/reports/brand-page-inventory-2026-05-12.md` · commit `6b51269` · scope for BRAND-PAGES-1 step
- **VENDOR-NORMALIZE-2** 2026-05-12 · Applied canonical brand map to 152 enriched products · vendor field + metafield + brand:* tag now agree per product · 8/8 verification sample passed · commit `5cdbb62`
- **TAG-AUDIT-1** 2026-05-12 · 593 active products audited · 40 unique tags · 4 anomalies flagged · key finding: industry:business mass-tag on 548/593 (new bug) · 3 brand canonical map gaps (Safco, Humanscale, Heartwood slug) · `data/reports/tag-audit-2026-05-12.md` · commit `fc8b4ff`
- **PUSH-FIX-1** 2026-05-12 · Surfaced + fixed 5 silent-failure bugs in `scripts/push-pe3-enrichment.py` · body_html / vendor field / brand:* tag writes restored · 88 products affected (69 Batch 1+2 + 19 Batch 3), all pushed live in same run · kody-mesh-chair body_html gap patched in `33a2c35` · commits `58e8a27`, `33a2c35`
- **PE-PASS-3-BATCH-3** 2026-05-12 · Chairs Part 3 batch enriched + pushed · 19 products live (13 GFG, 5 OTG, 1 ObusForme) · 0 fallbacks · 5/5 storefront verification clean · PE Pass 3 progress now 88/157 · commits `080cbe3` (enrichment), `58e8a27` (push script fixes), `33a2c35` (kody patch)
- **PE-PASS-3-BATCH-4** 2026-05-13 · Desks & Tables Part 1 batch enriched + pushed · 25 products live (9 OTG, 7 GFG, 2 Office Star, 1 Fellowes, 1 Heartwood, 5 BBI fallback) · 5/5 storefront verification · surfaced Victor Technology, Rocelco, HDL as canonical map additions · re-push idempotency confirmed safe · commit `d898b12`
- **INNOVATIONS-FIX** 2026-05-13 · Corrected canonical brand map — Innovations re-attributed from Global Furniture Group to Heartwood Manufacturing Ltd. (is_standalone=False, parent=Heartwood) · 5 products re-tagged (vendor + metafield + brand tag) · surfaced during Batch 4 research, confirmed via heartwooddl.com · 5/5 verification · commit `a4582ea`
- **PE-PASS-3-BATCH-6** 2026-05-13 · Storage & Accessories batch enriched + pushed · 30 products live (9 Heartwood, 7 OTG, 4 Fellowes, 1 Deflecto, 9 BBI fallback) · 5/5 storefront verification · surfaced Kensington, Sentry Safe, FireKing, Tayco as canonical map additions · LAST PE Pass 3 BATCH · Step 8 closes · final progress 143/157 · commit `a44d14c`
- **COLLECTION-CLEANUP-APPLY** 2026-05-13 · Unpublished 164 collections (161 ARCHIVE + 3 REDIRECT) · 18 unenriched stragglers stripped of brand:global-teknion tag · global-teknion smart collection rule converted to disjunctive (GFG OR Teknion), now 72 products · /collections/other unpublished (337 archived products no longer browsable) · 10 dead tile blocks removed from 4 category templates · 164 redirects added to `data/url-redirects-bulk.csv` · 5/5 verification clean · active collection count 371 → 207 · commit `737f6f6` · Steve must manually import redirects via Shopify Admin → Navigation → URL Redirects
- **BRAND-CALLOUT-AUDIT** 2026-05-13 · 10 Phase 2 category pages audited · 6 templates updated with 14 block edits · Keilhauer + ergoCentric callouts removed where empty; GFG callouts added on storage, tables, boardroom; ergonomic-products left clean · brand plates band deferred to BRAND-PAGES-1 (Step 24) · COLLECTION-CLEANUP arc (Sub-steps A → D) now closed · 6/6 DEV theme verification · commits `326241f` (templates), `af7f75f` (build-state)
- **TAG-INDUSTRY-CHECK** 2026-05-13 · Classified as PARTIALLY ALIVE · one real use (business-furniture smart collection exclusion rules) · 548 industry:business products are orphaned data with no storefront consumer · all 6 industry landing pages are editorial, no tag filtering · recommendation: fold remediation into BUG-FIX-3 scope (strip all 550 industry:* tags + replace exclusion rules with positive type:* inclusion) · output `data/strategy/industry-tag-decision.md` · commit `e669122`
- **PROMPT-5** 2026-05-13 · Image slot audit · 28 templates audited · 120 image_picker slots found (56 empty, 64 populated) · 63 page-images + 80 oci-photos inventoried · 91% empty-slot match rate (9 EXACT + 26 HIGH + 14 MEDIUM + 2 LOW + 3 NO-MATCH) · output `data/reports/image-slot-audit-2026-05-13.md` + `.csv` · ready for PAGE-IMG-1 (Phase 3 Step 16) · commits `790ec26`, `324df1f`
- **PROMPT-5-EXTEND** 2026-05-13 · Classified 64 populated image slots · 49 KEEP-CURATED · 0 REPLACE-STOCK · 4 REPLACE-WRONG-IMAGE · 11 REVIEW · PAGE-IMG-1 total scope: up to 71 slot writes · output `data/reports/image-slot-audit-2026-05-13-extension.md` · commit `e7e0f4b`
- **BUG-FIX-4** 2026-05-13 · 12 OCI photos uploaded to Shopify Files via GraphQL staged-upload pipeline · `page.our-work.json` patched with `shopify://shop_images/` GIDs for photo_1 through photo_12 · 12/12 slots verified · 3/3 spot-check URLs return HTTP 200 · DEBT-04 resolved · pattern reusable for PAGE-IMG-1's remaining 56 empty slots · commits `588ce31` (template), `71cdaf3` (build state)

---

## Earlier waves

Earlier waves are not fully reproduced here — see git history (`git log --oneline`) or `bbi-build-state.md` for the complete record. Summary of what shipped per wave:

- **Track D — Design System** · DS-0 through DS-4 · tokens · component spec v1
- **Phase 1** · All 11 landing pages: homepage, OECM, design services, quote, FAQ, industries hub, 5 industry pages
- **Phase 1b Hero 100** · PE-1/2/3/4/7 shipped · descriptions, specs, titles, SEO meta all LIVE
- **Wave A** · NAV-1..4 (canonical nav + nav/footer snippets + 10 ds-lp-* refactored + homepage onto shared nav) · 10 P2 category pages · PB-9..11 (collection template + sub-collection audit) · LEAD-1 + INTERLINK-1 + IND-PROP
- **Wave B** · PB-14 custom→smart collection migration · PB-15 `collection.json` + `ds-cs-base.liquid` · P3-rollout (~68 sub-collections) · INTERLINK-2
- **Wave C** · Brands hub + 3 brand pages (Keilhauer, ergoCentric, bundled Global+Teknion) · About · Our Work · Contact · Delivery · Relocation · Customer Stories
- **Wave G** · PDP template (`ds-pdp-base.liquid`) + JSON-LD snippets + smoke tests · Custom 404 · SMART-1 (14 smart collections) · Blog + Article templates
- **Wave G-Fixes 1 + 2** · 11 PDP fixes · `<dialog>`-based quote modal (`bbi-quote-modal.liquid`) · variant chip flex + price refresh · brand plates · emoji cleanup

---

## Decisions waiting / Decisions log

Current pending decisions (already counted as steps in the live tracker):

- **Steve — LEAD-INBOX-1 (Step 21)** referenced at Step 21 — Provision `quotes@/design@/info@brantbusinessinteriors.com` with SPF/DKIM/DMARC. Hard prereq for LEAD-3 (UI complete; routing deferred).
- **Leo — CONTENT-1 (Step 34)** referenced at Step 34 — Lock `bbi-logo-v2` (current Brant Basics wordmark) OR source a true "Brant Business Interiors" wordmark. Sourcing adds 1–2 days.
- **Leo — LAUNCH-0 (Step 37)** referenced at Step 37 — Row-by-row image CSV approval (`data/reports/page-images-audit.csv`). Hard gate before LAUNCH-1 can run. Claude generates CSV; Leo marks every row Approved / Reject / Replace.
- **Leo — LAUNCH-2 (Step 39)** referenced at Step 39 — The actual Publish click in Shopify Admin. Never automated. Claude Code runs the live-theme backup; Leo clicks Publish.

---

## Parallel work / cross-cutting concerns

Wave D SEO foundation — runs in parallel, doesn't block launch steps, but should be in flight before LAUNCH-2 so SEO compounds from day one.

- **W0-1** · Google Search Console + GA4 setup · *CRITICAL — no SEO data compounds without this*
- **W0-2** · Create / claim BBI Google Business Profile · `google.com/business`
- **W0-2b** · Google Reviews seeding strategy · output `docs/plan/reviews-seeding.md`
- **W0-3** · Product redirects CSV upload · `data/url-redirects.csv` exists, manual upload in Shopify Admin pending
- **W0-6** · Parent domain backlinks (officecentral.com, brantbasics.com) · coordinate with parent webmasters
- **W0-7** · Surface OECM + "Since 1964" trust signals site-wide (snippets + announcement bar)

---

## Ship notes

### 2026-05-13 evening ship-note

**Shipped 2026-05-13 evening:** PROMPT-5 classification extension (49 KEEP-CURATED, 0 REPLACE-STOCK, 4 REPLACE-WRONG-IMAGE, 11 REVIEW — Wave A's image hygiene was better than feared) + BUG-FIX-4 (12 OCI photos live, Our Work page no longer broken). Phase 1 advanced from 12/15 to 13/15 done in one evening session.

**Three parallel options for the next session:** (a) fire **BUG-FIX-2** (Step 2) — ~30 min OECM investigation, read-only · (b) fire **COMP-SCRAPE-1** (Step 24, Phase 3) — competitor structural audit, parallel-safe with Phase 1 work, prereq for BRAND-PAGES-1 · (c) start **LEAD-INBOX-1** (Step 21) — provision quotes@/design@/info@ with SPF/DKIM/DMARC (hard prereq for LEAD-3).

---

## Top card historical state

As of 2026-05-13 (the live tracker sync date):

- **Total steps to launch:** 41
- **Phase counts:** Phase 1 = 15, Phase 2 = 1, Phase 3 = 19, Phase 4 = 1, Phase 5 = 5
- **Phase 1 done:** 13 of 15 · 2 remaining (BUG-FIX-2, BUG-FIX-3)
- **Phases 2–5 done:** 0
- **Time estimate:** ~85–125 focused hours · 2–3 weeks at normal pace
- **Gates:** Critical gate: SEO-AUDIT-1 · Final click: Leo (LAUNCH-2)
- **Progress bar fill:** 14% (tracker was built pre-Phase-1-completion; fill is approximate)

---

## How to keep this archive in sync

When a tracker step completes:
1. Update the live tracker with status badge + `✅ Done <date>` + completion summary in the step's `<p class="step__meta">` block
2. In the same or follow-up Claude Code session, append the full completion details to this archive doc under the appropriate Phase section
3. If the step was historically significant, also add a Wave entry to the Wave H (or current wave) section above

When a new tracker update changes the ship-note:
1. Append the new ship-note to the "Ship notes" section above with today's date
2. The tracker can keep only the most recent ship-note inline
