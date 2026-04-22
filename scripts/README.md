# Scripts — quick reference

All scripts are invoked as `python3 scripts/<name>.py` from the project root. Most accept `--live` (writes to Shopify) vs. default dry-run, and many support `--limit=N` or `--handle=<product-handle>` for smoke-testing.

Credentials: `.env` must contain `SHOPIFY_TOKEN=...`. Never commit `.env`.

Every `push-*` script backs up state to `data/backups/` and logs the full write trail to `data/logs/<script>-<timestamp>.json`.

---

## 1. Auth + setup

| Script | Purpose |
|---|---|
| `shopify-oauth.py` | Python OAuth callback server. Run once to mint the Admin API token. |
| `shopify-oauth.js` | Node equivalent of the same flow. |

---

## 2. Audit + scan (read-only)

Scans the live store and writes reports to `data/` or `data/reports/`. Never modifies Shopify.

| Script | Purpose |
|---|---|
| `audit-products.py` | Snapshot all products + flag missing fields. |
| `scan-broken-products.py` | Find 404/missing-image/$0-price products → `data/broken-products-report.json`. |
| `check-sold-history.py` | Cross-reference broken products against Orders → `data/sold-history-flagged.json`. |
| `inspect-junk.py` | Drill into a specific set of junk/test products. |
| `find-liquid-bug.py` | Grep theme `.liquid` files for known divided-by-zero patterns. |
| `analyze-orders.py` | Orders API summary (revenue, taxes, regions, payment methods). |
| `top-sellers.py` | Rank products by units × revenue. |
| `fetch-sample-products.py` | Pull N random product JSONs to `data/` for schema inspection. |
| `fetch-file.py` | Download a single theme file (`python3 scripts/fetch-file.py <key>`). |

---

## 3. Build (generate review artifacts)

Produces CSVs / JSON / Markdown for Steve to review before anything is pushed.

| Script | Purpose |
|---|---|
| `build-hero-100.py` | Select the Hero 100 products for enrichment → `data/hero-100.csv`, `data/hero-100.md`. |
| `build-taxonomy-tags.py` | Propose `type:*` / `room:*` tags for every active SKU → `data/reports/taxonomy-tags-proposed.csv`. |
| `build-industry-tags.py` | Propose `industry:*` tags → `data/reports/industry-tags-proposed.csv`. |
| `build-tier2-disposition.py` | Classify every SKU into archive / keep-live-quote / keep-live → `data/tier-2-disposition-review.csv` + `docs/reviews/tier-2-disposition-summary.md`. |
| `build-tier2-disposition-html.py` | Render the disposition CSV as a reviewable HTML page → `previews/tier-2-disposition-review.html`. |
| `build-redirects-csv.py` | Emit Shopify-compatible redirect CSV for renamed handles. |
| `build-manual-review.py` | Markdown table of products needing human review → `data/manual-review.md`. |
| `lookup-specs.py` | Per-Hero-100 web spec lookup via Claude API → `data/specs/<handle>.json` → aggregated `data/specs.json`. Resumable. |

---

## 4. Clean + fix (data transforms)

Transforms the proposal CSVs or HTML bodies. Read-only against Shopify; modifies local CSVs.

| Script | Purpose |
|---|---|
| `clean-html.py` | Strip boilerplate + junk HTML out of product descriptions. |
| `clean-top-revenue.py` | Targeted HTML cleanup on the top-revenue subset. |
| `clean-legacy-tags.py` | Remove legacy tags that predate the `type:*`/`room:*`/`industry:*` scheme. |
| `dedup-boilerplate.py` | Detect identical boilerplate blocks across products. |
| `fix-bad-handles.py` | Rename product handles containing ™/® + emit redirect rows. |
| `fix-industry-tag-corrections.py` | Apply the industry-tag correction list. |
| `apply-industry-corrections.py` | Merge the correction set into the proposed CSV. |
| `purge-junk.py` | Mark junk/test/draft products for archive. |
| `archive-drafts.py` | Archive draft products (stays in admin, hidden from storefront). |
| `retire-services.py` | Unpublish service pseudo-products. |
| `consolidate-shipping.py` | Normalize shipping rate tiers. |

---

## 5. Push (writes to Shopify — use with care)

Every script here requires `--live` to actually write. Default is dry-run.

| Script | Purpose |
|---|---|
| `push-cleanup.py` | Push cleaned product HTML bodies. |
| `push-html-cleanup.py` | HTML-specific variant of push-cleanup. |
| `push-top-revenue.py` | Push cleaned bodies for the top-revenue subset only. |
| `push-taxonomy-tags.py` | Push `type:*` / `room:*` tags from `data/reports/taxonomy-tags-proposed.csv`. |
| `push-industry-tags.py` | Push `industry:*` tags from `data/reports/industry-tags-proposed.csv`. |
| `push-file.py` | Push one theme file (`python3 scripts/push-file.py <key> [local_path]`). |
| `update-homepage.py` | Update homepage sections (hero, testimonials). |
| `update-main-menu.py` | Rebuild the main navigation from the 8-item facet design. |
| `delete-menu-item.py` | Remove a single menu item by title. |
| `create-collections.py` | Create the 14 automated collections (7 type × 7 room). |
| `set-collection-sort.py` | Set each collection's sort order (velocity). |
| `add-breadcrumbs.py` | Add BreadcrumbList JSON-LD + collection breadcrumb template. |
| `write-review-descriptions.py` | Push the AI-written descriptions for the Hero 100. |

---

## 6. Verify (post-push sanity checks)

| Script | Purpose |
|---|---|
| `verify-all.py` | End-to-end sweep across every push target. |
| `verify-cleanup.py` | Confirm cleaned bodies are live on the PDPs. |
| `verify-taxonomy.py` | Sample N random products and confirm expected tags → default `--sample=20`. |
| `verify-notifications.py` | Confirm order-confirmation + admin emails are firing. |
| `verify-tax-payments.py` | Spot-check tax rates against expected provincial HST/GST. |

---

## 7. Content helpers

| Script | Purpose |
|---|---|
| `scrape-oci-photos.py` | Scrape 48 real project photos from officecentral.com → `data/oci-photos/` + `catalog.json`. |
| `before-after.py` | Render a before/after HTML diff for product body changes → `previews/before-after.html`. |
| `serve-previews.py` | Local static HTTP server for `previews/*.html` at `http://localhost:8080/`. |
