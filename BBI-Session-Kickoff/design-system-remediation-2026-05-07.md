# Design System Remediation Plan — 2026-05-07

**Owner:** Steve
**Trigger:** May 7 walkthrough of the live dev theme after the overnight build sprint.
**Premise:** The overnight sprint shipped scaffolding, not finished pages. Rows are marked ✅ on the basis of "committed + 200 response," not on parity with the locked design system. Several pages also 404. We need to **stop closing rows**, audit what's actually built, and execute a focused remediation pass before any further build work.

**Until this plan is complete, treat every ✅ row in `bbi-build-state.md` as 🟡 (provisional).** Do not check additional boxes.

---

## 0. Stage 0 audit — done (2026-05-07)

Audit artifacts in `data/reports/`. Read `stage-0-summary-2026-05-07.md` for the full picture. Headline findings:

- **Original hypothesis was wrong.** Wave C 404s are *not* caused by missing Shopify Page records. 8 of 9 DRAFT pages have correct Page records + correct `template_suffix` — they just need to be published.
- **`customer-stories`** is the only genuine missing-Page-record root cause.
- **Worktree gate ≠ dev theme gate.** Pushing `theme.liquid` from this worktree right now would overwrite the dev theme and break BBI chrome on every Wave C page + every PDP. **No `theme.liquid` push until reconciled.**
- **20 files exist on the dev theme but not in git.** All Wave C sections, templates, and gate entries.
- **404 chrome bug**: `template == '404'` missing from the gate in both worktree and dev theme — every 404 shows Starlite header above the BBI 404 content.
- **Wave B build-state lag**: PB-14, PB-15, P3-rollout, INTERLINK-2 are committed but still ⬜ in `bbi-build-state.md`.
- **Row truth pass**: 0 fully regressed, 5 provisional 🟡, 23 fully verified ✅.

---

## 1. What the May 7 walkthrough actually showed

The categories below are pulled directly from the walkthrough transcript and grouped by failure mode.

### A. Routability failures (P0)
Pages exist as templates but the route 404s.
- Wave C pages: **Our Work**, **About**, **Global** brand page, plus other brand/about variants
- **Customer Stories** 404
- Sub-collection product pages 404 (e.g. **task seating** under `/collections/seating`)
- Many of the "build state ✅" pages are not actually reachable from the browser

Most likely root cause: pushing a section + JSON template does **not** create a Shopify Page record. Many Wave C templates have no matching `/pages/<handle>` Page in Shopify Admin, or the Page exists but its `template_suffix` was never set.

### B. Navigation + chrome inconsistency (P0)
- The header drifts between pages — sometimes it's the BBI header, sometimes the Starlite chrome bleeds through.
- The footer differs page to page.
- The breadcrumbs don't follow a stable pattern — "going back and forth" rather than clean hierarchy.
- Active nav state is wrong on several pages.

### B-bis. OECM "Vendor of Record" badge styling (P1, not a bug)
The strikethrough renders consistently across every page where it appears. It's not broken HTML — it's just **the wrong style vs the locked design system**. Treat as a design-parity fix in Stage 3+, not a P0 chrome bug. Restyle to match whatever the locked design system specifies in `docs/strategy/design-system.md` and the T1–T6 mocks.

### C. Category-hub design mismatches — `/collections/seating`, `/collections/desks`, etc. (P1)
- Hero CTA reads **"Get a free design consultation"** → should be **"Shop all"** routing into the parent shop-all hub (`/collections/business-furniture` or the relevant smart collection).
- Missing the **"skip the catalog, buy by sector"** bar that links into the 5 industry pages.
- Missing the **"30+ brands · 3 tiers · Ontario OECM partner"** brand band ("the shelf behind the shelf").
- Doesn't match the **T3 collection-template** layout: photo → headline → subhead → "order direct from the catalog" → brand list → filterable product grid.
- No filter rail (subcategory, brand, height, fabric, warranty).
- Header itself looks off.

### D. Sub-collection design mismatches — `/collections/highback-seating`, `/collections/guest-seating`, etc. (P1)
- Hero CTA reads **"Get a free seating recommendation"** → should be **"Shop all seating"** pointing at the parent Level-2 collection.
- No filter rail at the top (subcategory, brand, height, fabric, warranty).
- No "Brands carried" strip below the filters.
- Header off — not matching the T4 mock.
- Product image tiles are inconsistent: photos zoomed in too far so chairs are cropped, sizing varies card-to-card, layout differs.
- Tile buttons route to **quote** when they should route to the **PDP**. Quote is the fallback only when the PDP itself is unbuyable.

### E. PDP design mismatches (P1)
- **Specs not populated** — `product.metafields.specs.*` is empty for the bulk of the catalog, so the spec table renders mostly blank.
- "About this product" block formatting is wrong vs T5.
- Missing the trust pills: **OECM Eligible** badge and **Canadian Made 🍁** badge. (The logic is in `ds-pdp-base.liquid` but it's not surfacing.)
- Sub-hero / brand line / variant area doesn't match the locked T5 layout.
- Specs table formatting is off even where data exists.
- The related-products morph block is present but not styled per spec.
- Bottom of PDP is missing the **"About the Brand"** block (brand photo + blurb + "View all <brand>" link).

### F. Missing shop-all landing (P2)
- No `/collections/business-furniture` page exists as a designed hub. The "Shop Furniture" entry from nav has no proper destination — currently it renders a generic Shopify collection or 404s.

### G. Content / data debt (P2/P3)
- Most product photos cropped too aggressively, partly an image-source issue and partly an `image_url` filter parameter issue.
- Spec metafields empty for most SKUs (the data is in `data/specs/` from `lookup-specs.py` but never pushed).
- Some CTAs phrased to push toward quote when they should push toward purchase.

---

## 2. Root causes (revised after Stage 0 audit)

The Stage 0 audit replaced the original hypothesis. Three drift mechanisms account for the design-system gap:

1. **The push-root bug (pre-PB-12, fixed in commit `5888659`).** Before that commit, `bbi-push-landing.py` silently pushed files from the main repo instead of the worktree. Pages built in worktree sessions — with the latest design tokens, shared nav snippets, gate edits — pushed *stale* main-repo versions to Shopify. Design-system work existed in git but never reached the dev theme. This is documented in `lessons-learned §4`.
2. **The `bbi_landing` gate is split across files.** The gate lives in `theme/layout/theme.liquid`. Adding a page requires (a) writing the section/template *and* (b) editing `theme.liquid` *and* (c) pushing `theme.liquid` separately because `bbi-push-landing.py` only pushes `assets/`, `sections/`, and `templates/` — not `layout/`. That two-step is easy to miss. When missed, the gate edit lives in git but never reaches the dev theme. Documented in `lessons-learned §3`.
3. **Wave C was built outside the worktree workflow.** All 9 Wave C pages (about, brands hub, the 3 brand sub-pages, our-work, delivery, relocation, contact) were pushed to Shopify directly, not through the worktree git flow. Their sections, templates, and gate entries exist *only* on the dev theme — the worktree doesn't have them. Any worktree-side design-system update can't reach those pages because they're on a diverged track.

Net effect: design-system improvements ship to git, never make it to the live store, the walkthrough finds drift, and we conclude "it doesn't match the design system." It does match — in git. Just not on the dev theme.

Two contributing process gaps from the original plan that still apply:

4. **Definition of done was too loose.** Rows closed when (a) the file was committed and (b) a smoke check returned 200. That doesn't catch chrome drift or design-parity drift.
5. **Spec metafields were treated as a separate workstream and never landed.** PDP template assumes them; the data is in `data/specs/` but never pushed.

---

## 3. Sequenced remediation plan

### Stage 0 — Freeze and measure (≈2 hours, today)
**Stop pushing new build rows.** Just measure.

1. **Route audit.** Crawl every URL referenced in `bbi-nav.liquid`, `bbi-footer.liquid`, every section's CTAs, and `audit-interlinks.py`. For each: HTTP status, has `bbi-nav`, has `bbi-footer`, gate evaluated as `true`, rendered template suffix. → `data/reports/audit-routes-2026-05-07.csv`.
2. **Visual baseline.** Take screenshots of: homepage, one Level-2 hub, one sub-collection, one in-stock PDP, one quote-only PDP, About, Customer Stories, one brand page, 404, Contact. Drop into `data/reports/design-baseline-2026-05-07/`. These become the "before" state.
3. **Page-record audit.** Pull the full list of Pages from Shopify Admin (handle + template_suffix). Cross-reference with `theme/templates/page.*.json`. Any template with no matching Page record = a 404 root cause.
4. **Build-state truth pass.** Walk every row currently ✅ in `bbi-build-state.md`. Mark each row's true status in `data/reports/row-reverify-2026-05-07.md` — `verified ✅`, `provisional 🟡`, or `regressed ⬜`. Do **not** edit the build state itself yet; the audit artifact is the source of truth until Stage 7.

**Exit criteria:** complete picture of what's broken, by category and by row.

### Stage 1 — P0: reconcile worktree with dev theme (≈0.5 day, do this BEFORE anything else)

This stage didn't exist in the original plan. The audit revealed it's the precondition for everything downstream — until worktree and dev theme are reconciled, every push is a footgun.

1. **Pull the 20 dev-only files into the worktree.** `theme/sections/ds-lp-*.liquid` and `theme/templates/page.*.json` for: about, brands, brands-keilhauer, brands-global-teknion, brands-ergocentric, our-work, delivery, relocation, contact, and any others the audit flagged. Use `shopify theme pull` (filtered) or a direct API fetch to grab them from dev theme `186373570873`. Commit on a branch named `chore/reconcile-dev-theme`.
2. **Reconcile `theme/layout/theme.liquid`.** The worktree gate is missing suffixes that the dev theme gate has. Pull the dev theme's `theme.liquid`, diff against worktree, and either (a) merge dev-theme additions into worktree or (b) generate the union and push it back. Result: worktree gate ≡ dev theme gate. After this, `theme.liquid` is safe to push from the worktree again.
3. **Add `template == '404'` to the gate** while we're in there. Push `theme.liquid` to the dev theme. The 404 page now renders BBI chrome instead of Starlite header above BBI body.
4. **Publish the 8 DRAFT Wave C pages.** Templates + Page records + gate entries already exist — this is one Admin API call per page (`PUT /pages/<id>.json` with `published: true`). Verify each returns 200 and renders BBI chrome.
5. **Create the missing `customer-stories` Page record.** The only genuine missing-Page case. Handle = `customer-stories`, `template_suffix = customer-stories`, then publish.
6. **Update `bbi-build-state.md` for Wave B.** PB-14, PB-15, P3-rollout, INTERLINK-2 are committed and live — flip them to ✅ with the correct commit SHAs from the audit.

(OECM badge styling is now a Stage 3+ design-parity fix, not a P0 chrome bug — see §1.B-bis.)

**Exit criteria:**
- Worktree `theme.liquid` ≡ dev theme `theme.liquid`
- Worktree contains all sections + templates that exist on the dev theme (no more drift)
- All 9 Wave C pages return 200
- 404 page renders BBI chrome (no Starlite header)
- Wave B rows correctly marked ✅ in `bbi-build-state.md`
- Route audit re-run shows zero 404s

### Stage 1.5 — P0: resolve sub-collection 404s (≈0.5 day)
Run/extend `scripts/audit-sub-collections.py`. For every sub-collection handle referenced in nav or category-hub tiles: confirm the collection exists. Create missing collections, or fix the hrefs that point at non-existent handles.

**Exit criteria:** every sub-collection link in the nav and on category hubs returns 200.

### Stage 2 — P0: stabilize chrome (≈1 day)
1. **Refactor the `bbi_landing` gate.** Move the suffix list into a single snippet `snippets/bbi-landing-gate.liquid` that returns true/false. Adding a new BBI page becomes a one-line change. Cuts the "I forgot to add the suffix to the gate" failure mode.
2. **Header parity.** Snapshot the rendered `bbi-nav` HTML on every BBI page. Diff. They must be identical except for the active-state class. Fix any drift.
3. **Footer parity.** Same exercise for `bbi-footer`.
4. **Crumbs snippet.** Lock the breadcrumb pattern: 4-level on category/sub/PDP, 3-level on hubs, 2-level on top-level pages. Build `snippets/bbi-crumbs.liquid`, render it from every section. Remove inline breadcrumb HTML elsewhere.

**Exit criteria:** structural HTML diff across all 25+ BBI pages shows identical header, footer, and crumb skeletons.

### Stage 3 — P1: category hubs match T3 (≈2 days)
For each of the 9 Level-2 collections (`seating`, `desks`, `storage`, `tables`, `boardroom`, `ergonomic-products`, `panels-room-dividers`, `accessories`, `quiet-spaces`):

1. Replace the "Get a free design consultation" hero CTA with **"Shop all <category>"** routing into the smart collection from SMART-1.
2. Add the **"buy by sector"** skip-bar with links to the 5 industry pages.
3. Add the **"30+ brands · 3 tiers · Ontario OECM partner"** band linking to `/pages/brands`.
4. Implement the T3 visual layout: photo → headline → subhead → "order direct from the catalog" → brand list → filterable product grid.
5. Wire the filter rail (subcategory / brand / height / fabric / warranty) using tag filters.

**Exit criteria:** each Level-2 collection page passes side-by-side visual diff against T3 with ≤ 5% delta.

### Stage 4 — P1: sub-collections match T4 (≈3 days, may stretch)
Roll out across all 68 sub-collections. The work is one section template (`ds-cs-base.liquid`) — fix it once, applies everywhere.

**Stage 4 prerequisite — confirm filter-rail tag data exists.** Before writing any filter UI, run a tag census across the 645+ SKUs. Required namespaces: `subcategory:*`, `brand:*`, `height:*`, `fabric:*`, `warranty:*`. Output → `data/reports/tag-census-2026-05-07.csv`. If any namespace is sparse, **a tagging push becomes a Stage 4 prereq workstream** — that's where the timeline can stretch. Filters that show empty options or filter to nothing are worse than no filters.

1. Hero CTA: "Get a free <type> recommendation" → **"Shop all <category>"** routing to the parent Level-2 collection.
2. Filter rail at top of grid: subcategory, brand, height, fabric, warranty (tag-driven). Build the rail; if a namespace from the census is sparse, ship that filter as a Phase-2 backlog item rather than a half-empty filter.
3. "Brands carried" strip below the filter rail.
4. **Fix product-tile image cropping** — confirmed root cause is the `image_url` filter parameters being too narrow on the source side, not the source photos. Loosen the filter: use `image_url` with adequate width (`width: 800` or larger) and `crop: 'center'` (or remove the crop entirely if the source aspect already matches). Test against the 10 worst examples first (the highback-seating chairs Steve flagged), then verify on 10 random sub-collections.
5. Tile button CTAs: route to PDP, not to quote. Quote is the fallback only when the PDP is unbuyable.

**Exit criteria:** 5 random sub-collections pass T4 visual diff. Filter rail returns sensible facets, no empty namespaces shipped.

### Stage 5 — P1: PDPs match T5 (≈3 days)
1. Verify the OECM Eligible + Canadian Made 🍁 badge logic in `ds-pdp-base.liquid` actually fires. Tag enough SKUs to make this visible.
2. Re-style "About this product" block per T5.
3. Re-style the spec table per T5.
4. Re-style the related-products morph per T5.
5. Add the "About the Brand" block at the bottom per the locked design system. **Layout follows `docs/strategy/design-system.md` and the T5 mock — do not reinterpret.** If we don't have a brand photo for a given vendor, ship a **placeholder** in the same slot (the design system's empty-state for image slots) — never skip the block or change the layout. Populate real photos in a follow-up content pass. Hardcode the blurb copy for the 3 priority brands (ergoCentric, Keilhauer, Global/Teknion); generic fallback for the rest.
6. **Push spec metafields.** Top-100 Hero SKUs first. Source data is already in `data/specs/`. Build `scripts/push-specs.py`, dry-run, then `--live`.

**Exit criteria:** Hero 100 SKUs pass T5 visual diff with populated spec table and brand block.

### Stage 6 — P2: build the shop-all hub (≈1 day)
1. Create `/collections/business-furniture` template (`collection.business-furniture.json`) with the T2 layout: hero → 5-industry skip-bar → 9-category tile grid → 3-tier brand band → filter rail → full product grid.
2. Wire it as the "Shop Furniture" destination in the nav.
3. Confirm the "Shop all" CTAs from Stages 3 and 4 route here correctly.

### Stage 7 — Re-verify and reset the build state (≈0.5 day)
1. Walk every row in `bbi-build-state.md` currently ✅. For each, decide:
   - Page renders + matches design + is reachable → **keep ✅**
   - Page renders but design differs → **🟡 with link to the remediation issue**
   - Page 404s or has a chrome bug → **⬜ and reopen**
2. Update `bbi-build-state.md` accordingly. This is the only point where checkboxes move.
3. Update the Cowork artifact at `~/Documents/Claude/Artifacts/bbi-status/index.html`.

### Stage 8 — Lock the process so this doesn't happen again
Add to `CLAUDE.md` under a new **Definition of Done** section:

A row only closes when **all** of the following are true:
- Live dev-theme URL returns 200
- `bbi-nav` and `bbi-footer` render and structurally match the snapshot
- Visual diff against the locked T1–T6 mocks ≤ 5% pixel delta on the relevant template
- Active nav state is correct on the rendered page
- Every `<a href>` on the page resolves to a 200 (no internal 404s)
- The corresponding Shopify Page record exists with the correct `template_suffix`
- Spec metafields populated (PDPs only)
- A screenshot of the live page is attached to the commit message or PR

Operational changes:
- `/bbi-build-page` is reserved for **new** pages only.
- Add `/bbi-fix-page <slug>` (new skill) for remediation. It always: (a) screenshots current state, (b) compares to the locked mock, (c) emits a diff list, (d) fixes, (e) re-screenshots, (f) re-diffs.
- Pre-flight gate before merging any build-row PR: must include before/after screenshots.

Three guardrails specifically for the drift mechanisms uncovered in the audit:
- **No direct dev-theme edits.** Every page change goes through the worktree, full stop. The 20 dev-only files were the worst single source of drift in the project.
- **`bbi-push-landing.py` must push `theme/layout/theme.liquid` too**, or its companion gate-push script must run automatically alongside it. Single command, no two-step. The split-push pattern caused gate edits to silently never reach Shopify.
- **Reconciliation check on every push.** Before any push of `theme.liquid`, the script diffs worktree vs dev theme and refuses to push if the worktree would clobber dev-theme content. Hard fail, not a warning.

---

## 4. Rough timeline

| Stage | Work | Effort |
|---|---|---|
| 0 | Freeze + audit | ✅ done |
| 1 | P0 reconcile worktree ↔ dev theme | 0.5 day |
| 1.5 | P0 sub-collection 404s | 0.5 day |
| 2 | P0 chrome stabilization | 1 day |
| 3 | Category hubs (9) | 2 days |
| 4 | Sub-collections (68 via shared template) | 3 days |
| 5 | PDPs + specs push | 3 days |
| 6 | Shop-all hub | 1 day |
| 7 | Re-verify + reset build state | 0.5 day |
| 8 | Lock process | 0.25 day |

**~12 working days** of focused remediation before LAUNCH-0 is realistic. The overnight sprint accelerated scaffolding but did not produce launch-ready pages.

---

## 5. What stays untouched

Not all of the overnight work is wasted — most of it is good scaffolding. Don't redo:
- `scripts/migrate-to-smart-collections.py` and the SMART-1 plan — works as designed, just blocked on Leo's go-ahead for the live run
- `scripts/set-sub-collection-suffix.py` and the P3-rollout — base template suffix is correctly set on 62 sub-collections
- The shared `bbi-nav` / `bbi-footer` snippets exist; they need parity hardening (Stage 2), not a rewrite
- Section files exist for every Wave C / Wave G page; the Liquid parses; the issue is design fidelity, not "we have nothing"
- The `ds-pdp-base.liquid` PDP scaffolding — JSON-LD wiring, gallery JS, gate logic. Visual styling needs the T5 pass

---

## 6. Decisions (resolved 2026-05-07)

1. **OECM strikethrough** — appears everywhere, consistently. Not a chrome bug. Treat as design-system parity work in Stage 3+. Restyle to match the locked design system; don't hunt a CSS bug.
2. **Filter-rail tag data** — must be confirmed before Stage 4 builds the UI. Tag census is a Stage 4 prerequisite. If namespaces are sparse, the tagging push extends Stage 4.
3. **Image cropping** — root cause is `image_url` filter parameters too narrow, not the source photos. Stage 4 step 4 loosens the filter (width / crop arguments) and verifies.
4. **Brand block** — follow the locked design system layout. Use placeholder image slots where we don't have brand photos yet. Don't skip the block, don't change the layout.
5. **Definition of Done with screenshots** — adopted. Stage 8 wires this into `CLAUDE.md` as a hard requirement on every build-row commit.
