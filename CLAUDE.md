# Office Central / BBI — Claude Code Guidelines

This file governs Claude Code behaviour for the Brant Business Interiors (BBI) Shopify project.
Follows standard Shopify theme best practices plus BBI-specific rules that override generic defaults.

**Store:** [brantbusinessinteriors.com](https://www.brantbusinessinteriors.com) · **Admin:** [office-central-online](https://admin.shopify.com/store/office-central-online)
**Buyer context:** B2B institutional Canadian buyers — school boards, hospitals, municipalities. OECM-eligible supplier.

---

## BBI-Specific Rules (highest priority — override everything below)

- **Never delete products.** Archive or unpublish only. Prefer unpublish when sold history exists.
- **Unbuyable items stay live.** Sold-out, $0-price, and showcase products keep their page with a **Request a Quote** CTA — these are B2B lead-capture pages, not dead listings.
- **OECM status is a key differentiator.** Office Central and Brant Basics are verified OECM partners. Ontario institutional buyers can purchase without open tender. Surface this in copy whenever relevant.
- **Dry-run first.** All `push-*` scripts default to dry run. Always confirm output before passing `--live`.
- **Credentials.** API token lives in `.env` (`SHOPIFY_TOKEN=...`). Never commit `.env`. Scripts back up to `data/backups/` and log to `data/logs/` before writing.

---

## Project Structure

```
.
├── docs/            Plans, strategy, workflows, review artifacts
│   ├── plan/        Active fix plan + status snapshots + idea backlog
│   ├── strategy/    Brand voice, ICP, segment analysis, competitor research
│   ├── workflows/   How-to runbooks (shipping tiers, taxonomy, design)
│   └── reviews/     Auto-generated review artifacts (for Steve's approval)
├── scripts/         50 Python/Node helpers — read/write Shopify, clean data
├── data/            Everything scripts read/write (CSVs, JSON, logs, backups)
│   ├── specs/       Per-product spec JSON from lookup-specs.py (Hero 100)
│   ├── reports/     Proposal CSVs (tags, industry) — source of truth for pushes
│   ├── redirects/   URL redirect CSVs for Shopify Admin upload
│   ├── exports/     Full Shopify product/order exports (reference snapshots)
│   ├── backups/     Pre-change snapshots (menus, products, collections)
│   ├── logs/        Push audit trails (timestamped JSON)
│   ├── oci-photos/  48 real project photos from officecentral.com
│   └── page-images/ AI-generated hero images per page (fal.ai flux/dev)
├── previews/        Browser-viewable HTML — checklists, review pages, strategy docs
├── theme/           Shopify theme code (layouts/sections/snippets/templates)
└── .claude/         Launch configs + agent tooling
```

- Follow the standard Shopify theme directory structure inside `theme/`: `assets/`, `config/`, `layout/`, `sections/`, `snippets/`, `templates/`, `locales/`.
- Never create directories outside this structure without justification.
- Keep `layout/theme.liquid` lean — load scripts and styles via `{% render %}` snippets.
- Use `templates/` for JSON templates (OS 2.0). Avoid `.liquid` templates unless supporting a legacy theme.

---

## Liquid Templating

- Prefer `{% render %}` over `{% include %}`. `render` has sandboxed scope; `include` leaks parent variables and is deprecated. Never use `{% include %}` in new code.
- Keep logic out of templates — move conditional blocks and loops into snippets.
- Avoid deeply nested Liquid logic (>3 levels). Refactor into named snippets.
- Use `{% liquid %}` blocks to group multiple tags without extra whitespace output.
- Strip whitespace with `{%- -%}` and `{{- -}}` in loops and large partials.
- Always provide fallback values: `{{ product.title | default: 'Untitled' }}`.
- Never output raw user-controlled data without appropriate filters (`escape`, `strip_html`).

---

## Sections & Blocks (Online Store 2.0)

- Every merchant-editable area must be a section or a block inside a section.
- Define schema settings for all configurable content — never hardcode merchant-facing copy.
- Use `presets` so sections appear in the Theme Editor.
- Sections must be self-contained and re-renderable in isolation (section rendering API).
- Use `blocks` for repeatable elements (slides, tabs, FAQ items); set a reasonable `max_blocks`.
- Always define `name` and `class` in section schema for Editor discoverability.
- Validate that schema `type` values match Shopify's supported input types.
- Declare `"blocks": [{ "type": "@app" }]` in section schemas to support app integrations.

---

## Metafields & Metaobjects

- Themes can only **read** metafields — never attempt to write them from Liquid or client-side JS.
- Access via `product.metafields.namespace.key`. Never construct dynamic metafield keys at runtime.
- Always check existence before outputting: `{% if product.metafields.custom.tagline != blank %}`.
- Metafield values have a 16 KB cap. If a value appears truncated, flag it — fix is on the data side.
- Document every custom metafield namespace and key the theme depends on in `README.md`.

---

## Performance

- Lazy-load all images below the fold using `loading="lazy"` and Shopify's `image_url` filter with explicit `width` and `height`.
- Always use `image_url` with a `width` parameter — never output raw CDN URLs.
- Use `srcset` for responsive images; `image_tag` generates srcset automatically.
- Defer non-critical JS with `defer` or `type="module"`. Never use `document.write()`.
- Avoid loading third-party scripts in `<head>` — use `async` or move to end of `<body>`.
- Consolidate theme JS into `assets/` rather than per-section `<script>` tags.
- Target Lighthouse performance ≥ 80 on mobile for all new features.

---

## JavaScript

- Write vanilla JS unless the project already uses a framework. Do not introduce React, Vue, or Alpine.js without approval.
- Use Web Components for encapsulated interactive UI (carousels, modals, accordions) — consistent with Dawn pattern.
- No jQuery. Not included in modern Shopify themes.
- Namespace globals under a project-specific prefix (e.g., `window.BBI`).
- Use `CustomEvent` for cross-component communication dispatched on `document`.
- Always use `addEventListener` — never inline `onclick` attributes.
- Wrap Fetch and Cart API calls in try/catch with user-visible fallback messaging.

---

## Cart (Client-Side)

- Use the Cart API (`/cart/add.js`, `/cart/update.js`, `/cart/change.js`) for all cart mutations.
- Dispatch standard cart events (`cart:refresh`, `cart:updated`) after mutations.
- Optimistically update UI and roll back on API error with a visible message.
- Never redirect to `/checkout` directly from JS — use `window.location` only after confirmed cart state.

---

## CSS & Styling

- Use CSS custom properties for all design tokens: colors, spacing, typography, border-radius.
- Define theme color and font settings in `config/settings_schema.json` and expose as CSS variables in `layout/theme.liquid`.
- No `!important`. If needed, it signals a specificity problem — fix the selector instead.
- No inline styles in Liquid templates except for dynamically injected CSS custom properties.
- Scope component styles with BEM-like convention or web component selectors — avoid broad tag selectors.
- Minify production CSS via Shopify CLI's build pipeline.

---

## Localization & Accessibility

- All customer-facing strings must use `{{ 'key' | t }}` keys defined in `locales/`. Never hardcode English strings.
- Always provide `alt` text for images using the product/image alt attribute, a metafield, or a schema setting fallback.
- All interactive elements must be keyboard accessible with visible focus styles.
- Use semantic HTML: `<nav>`, `<main>`, `<header>`, `<footer>`, `<article>`, `<section>`, `<button>`.
- Every form input must have an associated `<label>` (visible or `.visually-hidden`).
- Modals and drawers must trap focus and support `Escape` to close.
- Target WCAG 2.1 AA compliance as a minimum baseline.

---

## Shopify CLI

- Use **Shopify CLI 3.x** (`shopify theme dev`, `shopify theme push`, `shopify theme pull`) for local development.
- Never push directly to the live theme. Use a development theme or a duplicate.
- Add `config/settings_data.json` to `.gitignore` — it contains live merchant customizations.
- Always include `.shopifyignore` to prevent pushing files that should not overwrite the remote theme.

---

## Git

- Feature branches for all work. Never commit directly to `main`. Branch naming: `feature/`, `fix/`, `chore/` prefixes.
- Small, focused commits — one logical change per commit.
- Commit messages in imperative mood referencing the theme area: `Add sticky header behaviour`, `Fix cart drawer on mobile`.
- Open a PR for every change — creates intent record and scopes rollbacks.
- Squash commits on merge to keep `main` history linear.
- Tag releases on `main` with semantic versioning: `v1.0.0`, `v1.1.0`.
- Never commit `.env`, `config/settings_data.json`, `node_modules/`, `.DS_Store`, or build artefact directories.
- Run `shopify theme check` before opening a PR and resolve all errors.

---

## Testing & Quality

- Run `shopify theme check` before every commit. Resolve all errors; treat warnings as errors for new code.
- Validate all schema JSON — malformed schema silently breaks the Theme Editor.
- Test on real Shopify preview URLs, not just `localhost` — cart, redirects, and some Liquid objects behave differently locally.
- Test across: Chrome, Firefox, Safari (desktop + iOS), Chrome Android.
- Test with VoiceOver (macOS/iOS) or NVDA (Windows) for accessibility-critical flows.
- Test Theme Editor: every section must be addable, removable, and reorderable without JS errors.

---

## Documentation

- Every section must have a comment block at the top describing its purpose and any non-obvious schema settings.
- Document all metafield namespaces and keys the theme reads in `README.md`.
- Add inline `{% comment %}` blocks for non-obvious Liquid workarounds explaining the reason.
- Maintain `CHANGELOG.md` using [Keep a Changelog](https://keepachangelog.com/) format.

---

## Key Reference Files

| Need | File |
|---|---|
| Live task list | [docs/plan/shopify-fix-plan.md](docs/plan/shopify-fix-plan.md) |
| Status snapshot | [docs/plan/status-snapshot-2026-04-20.md](docs/plan/status-snapshot-2026-04-20.md) |
| Interactive checklist | [docs/plan/website-fix-checklist.html](docs/plan/website-fix-checklist.html) |
| Site build checklist | [previews/bbi-site-build-checklist.html](previews/bbi-site-build-checklist.html) |
| Ideas backlog | [docs/plan/ideas-backlog.md](docs/plan/ideas-backlog.md) |
| Brand voice + ICP | [docs/strategy/icp.md](docs/strategy/icp.md) |
| Approved copy samples | [docs/strategy/voice-samples.md](docs/strategy/voice-samples.md) |
| Script reference | [scripts/README.md](scripts/README.md) |
| Page image generator | [scripts/generate-page-images.py](scripts/generate-page-images.py) |
| AI image library | [data/page-images/](data/page-images/) |
