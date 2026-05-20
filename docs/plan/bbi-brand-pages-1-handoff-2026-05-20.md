# BRAND-PAGES-1 + A11Y — Claude Code Handoff (2026-05-20)

**Purpose:** This is a handoff brief for **building in Claude Code**. A Cowork session planned and scoped this work but made **no theme/Shopify changes**. Paste this into Claude Code (or tell it to `Read` this file + `docs/plan/wave-e-execution-plan-2026-05-20.md`), then have it write a build prompt and execute.

**This covers Link 1 of the Wave E chain** (BRAND-PAGES-1 + A11Y bundle). The full chain and its blockers are in `docs/plan/wave-e-execution-plan-2026-05-20.md`:
> BRAND-PAGES-1 + A11Y ↓ AI-7 homepage copy ↓ AI-8 OECM copy ↓ CONTENT-1 ↓ AI-9 + AI-5 schema ↓ SEO-AUDIT-1 ↓ A11Y Phase 1.5 PSI re-run

---

## Decisions locked (build to these)

1. **Approach A — copy per brand.** Do NOT build a generic schema-driven section. For each new brand: clone an existing per-brand section, rescope its CSS class, swap the copy.
2. **Global / Teknion → Option A.** Keep the existing `brands-global-teknion` page bundled; rename/expand it to a GFG-family experience. This is a copy/scope update, not a rebuild (page is healthy at 56 products).
3. **CONTENT-1 logo → lock `bbi-logo-v2`.** Reuse `shopify://shop_images/bbi-logo-v2_aa647658-6557-4dc8-abb7-f20f7b4c4a03.png` (the URL the existing brand templates already use). No new wordmark.

## Current repo state (start clean from here)

- Branch: `main` (ahead of origin by 53 commits — pre-existing, not from this session).
- Pre-existing uncommitted change `theme/snippets/bbi-quote-modal.liquid` is **not ours** — leave it.
- New untracked planning docs from this session (safe to keep): `docs/plan/wave-e-execution-plan-2026-05-20.md`, `docs/plan/bbi-brand-pages-1-handoff-2026-05-20.md`, `docs/strategy/competitor-audit-ugoburo.md`.
- A scratch `feature/brand-pages-1` branch and a placeholder `ds-lp-brands-otg.liquid` were created during scoping and then **removed** — none remain. Build fresh.
- Per CLAUDE.md: open a `feature/` branch before theme work.

---

## What to build

### 1. Three new brand pages (Approach A clone)

**Clone source:** `theme/sections/ds-lp-brands-ergocentric.liquid` (a complete, self-contained brand page: hero → intro → 4-card "why" grid → 3-tile category crosslinks → OECM bar → 5-item FAQ → inverse closer; CSS scoped to `.lp-ergo`; renders `bbi-nav`, `bbi-crumbs`, `bbi-footer`). Its template is `theme/templates/page.brands-ergocentric.json`.

**Per-brand procedure:**
1. `cp ds-lp-brands-ergocentric.liquid ds-lp-brands-<brand>.liquid`
2. Rescope CSS: replace `lp-ergo` → `lp-<brand>` throughout (sed is fine — it only hits the scope class, not other identifiers).
3. Fix the top `{%- comment -%}` header (section name, brand purpose, template suffix).
4. Swap all copy (hero H1/standfirst, intro, 4 "why" cards, FAQ, closer) for the brand. Update the breadcrumb `c3_label`. Point the 3 category-crosslink tiles at that brand's collections (see §3 — coupling).
5. Update `{% schema %}` `name` + `class` + default heading/subheading.
6. Create `theme/templates/page.brands-<brand>.json` (copy `page.brands-ergocentric.json`; set `type`/section key to `ds-lp-brands-<brand>`; set `logo` to the bbi-logo-v2 URL above; **leave `hero_image` out** so the built-in placeholder renders unless a real image is uploaded).
7. Register the suffix in the gate (see §2).

**Brands to build, with verified facts (source: `docs/strategy/brand-canonical-map.md`/`.csv`) and cautions:**

- **OTG / Offices to Go** — `page.brands-otg` (handle `/pages/brands-otg`). 54 enriched products — highest-volume brand, build first. The high-volume **value/budget tier of Global Furniture Group** (parent). Broad catalog: seating, desks, tables, storage, reception. Consumer-recognizable — buyers search "Offices to Go chair" directly. **Caution:** GFG is a Canadian company, but the OTG value line includes imported product — do **not** claim per-product "Made in Canada." Do **not** invent a specific warranty year. Lead on: broad catalog at institutional budgets, GFG backing, fast fulfillment, OECM eligibility, BBI volume pricing + design layout + Ontario install.
- **Heartwood Manufacturing Ltd.** — `page.brands-heartwood` (`/pages/brands-heartwood`). 17 products. **Canadian manufacturer in Kelowna, BC** (distribution via heartwooddl.com). Flagship **"Innovations" laminate desking line** (their most comprehensive series, 100+ components). Tables / casegoods / laminate desking specialist. **Made-in-Canada framing is accurate here.** Lead on: Canadian-made, Innovations desking, custom laminate program, OECM.
- **ObusForme** — `page.brands-obusforme` (`/pages/brands-obusforme`). 5 products (below the usual ≥10 threshold but **callable per ICP** — named directly in `docs/strategy/icp.md`; Hero 100 features the ObusForme 1240-3). Consumer-recognizable **ergonomic back-support / seating** brand; distributed in the GFG family. **Caution:** thin catalog — keep category crosslinks to what actually exists (likely seating/ergonomic only); don't imply a broad range. Don't invent warranty specifics.

Keep the existing OECM-bar pattern on every page (BBI edge — the competitor audit notes ugoburo never links brand pages to its procurement page). Reuse phone `1-800-835-9565` and `/pages/quote` CTAs already in the ergoCentric template.

### 2. Gate edits — `theme/layout/theme.liquid`

The `bbi_landing` gate is an `elsif template.suffix == '...'` chain (~lines 111–119, alphabetical among the `brands-*` entries). Add three branches:

```liquid
elsif template.suffix == 'brands-heartwood'
  assign bbi_landing = true
elsif template.suffix == 'brands-obusforme'
  assign bbi_landing = true
elsif template.suffix == 'brands-otg'
  assign bbi_landing = true
```

Without this, Starlite header/footer/cart chrome leaks onto the new pages.

### 3. 24 brand×category smart collections (catalog-navigability Option A)

These are the "View all" destinations from the brand-page category tiles. Per `data/strategy/catalog-navigability-investigation.md` (Option A hybrid).

- Use/extend `scripts/create-smart-collections.py`. **Dry-run first** (CLAUDE.md: scripts default to dry run; back up the collection list; only pass `--live` after confirming output).
- Rules key off `brand:*` tags (these now agree per product after APPLY-MAP-ADDITIONS). **Confirm the exact slugs** before writing rules — Heartwood is `brand:heartwood-manufacturing-ltd` (legacy `brand:heartwood` was migrated); confirm `brand:otg` and `brand:obusforme` against `data/reports/tag-audit-2026-05-12.csv` or live products.
- Naming convention: `<brand>-<category>` (e.g. `otg-seating`, `otg-desks`, `heartwood-tables`). Rule: tagged `brand:<brand>` AND `type:<category>`.
- **Coupling:** the brand-page category tiles should link to these handles, so create the collections **before/with** the page push to avoid broken links. (If you'd rather decouple, point the tiles at the general category collections — `/collections/seating` etc. — instead.)

### 4. Global / Teknion (Option A) + Brands Hub

- **Global/Teknion:** copy/scope update on `theme/sections/ds-lp-brands-global-teknion.liquid` to read as a GFG-family experience. No rebuild.
- **Brands Hub:** add OTG / Heartwood / ObusForme tiles to `theme/sections/ds-lp-brands.liquid` so the new pages are linked from `/pages/brands`.

### 5. A11Y-AUDIT-1 (the "A11Y" half of the bundle)

WCAG 2.1 AA audit on the top 10 pages via `axe-core` or `pa11y` CLI. **Run against `shopify theme dev` (localhost:9292)** to dodge the dev-theme preview-auth problem (external crawlers can't reach `?preview_theme_id`). Hard fails: missing alt text, unlabeled form inputs, contrast < 4.5:1, broken focus traps, keyboard gaps. Output `data/reports/a11y-audit-2026-05-2x.csv` (per-page issue list), fix block-level issues, re-check. Note: the new brand-page FAQ accordions use `<details>`/`<summary>` (keyboard-accessible by default) — verify focus-visible styles.

---

## Verification & push (CLAUDE.md rules)

- **Dev theme only:** `186373570873`. Never push to live (`178274435385`). Preflight-print `THEME_ID`.
- Push with: `BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873 --sections --templates --layout` (confirm the exact flags in the script header).
- **Verify after every push** (don't trust 200/OK): `curl '<url>?preview_theme_id=186373570873' -H 'User-Agent: Mozilla/5.0'` and assert exactly 1 `.bbi-header`, 1 `.bbi-footer`, 0 `.shopify-section-group-header-group` (no Starlite leak), correct breadcrumb, OECM bar present, no `Liquid syntax error`.
- Shopify **page objects** for `/pages/brands-otg|heartwood|obusforme` must exist with the matching `template_suffix` (the P4 brand pages were created via Admin API / Admin UI and published — replicate that). Don't delete anything (BBI Rule #1).
- Commit per CLAUDE.md (feature branch, focused commits, `shopify theme check` clean). Update the BBI build state in the same commit and add a `BRAND-PAGES-1` row.

## Blockers (not for this link, but plan around them)

- **SEO-AUDIT-1 (Link 6) is blocked:** the DataForSEO MCP isn't available in Cowork and isn't in its connector registry; external crawlers also can't reach the dev-theme preview. In Claude Code, run SEO-AUDIT-1 where the DataForSEO MCP is configured, and decide how it reaches the dev theme (local crawl, temporary password lift, or a waiver to run post-LAUNCH-2). Resolve before Phase 6.

## Reference files

- Full sequenced plan: `docs/plan/wave-e-execution-plan-2026-05-20.md`
- Brand facts + tag slugs: `docs/strategy/brand-canonical-map.md` / `.csv`
- Brand-page audit (build vs keep, Approach A/B analysis): `data/reports/brand-page-inventory-2026-05-12.md`
- Two-tier brand-hub pattern + OECM cross-link edge: `docs/strategy/competitor-audit-ugoburo.md` (§3, "Step 25")
- Smart-collection Option A: `data/strategy/catalog-navigability-investigation.md`
- Clone source: `theme/sections/ds-lp-brands-ergocentric.liquid` + `theme/templates/page.brands-ergocentric.json`

## Suggested Claude Code kickoff

> Read `docs/plan/bbi-brand-pages-1-handoff-2026-05-20.md` and `docs/plan/wave-e-execution-plan-2026-05-20.md`, plus the clone source `theme/sections/ds-lp-brands-ergocentric.liquid`. Write me a build prompt for BRAND-PAGES-1 + A11Y to the locked decisions (Approach A; Global/Teknion Option A; lock bbi-logo-v2), then build it on a `feature/` branch, push to dev `186373570873`, and curl-verify each page.
