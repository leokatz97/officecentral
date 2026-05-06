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
├── scripts/         60+ Python/Node helpers — read/write Shopify, clean data
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
| **🔴 Single source of truth — current build state** | [docs/plan/bbi-build-state.md](docs/plan/bbi-build-state.md) |
| **🔴 Page interlinking matrix + 12-point audit pattern** | [docs/plan/bbi-interlinking-map.md](docs/plan/bbi-interlinking-map.md) |
| **Track D — Design System (DS-0 → DS-4 COMPLETE)** | [docs/plan/track-d-design-system/README.md](docs/plan/track-d-design-system/README.md) |
| Screen audit — 5 locked screens (DS-0 output) | [docs/strategy/bbi-screens-audit-v1.md](docs/strategy/bbi-screens-audit-v1.md) |
| Design token push script | [scripts/push-design-tokens.py](scripts/push-design-tokens.py) |
| Status snapshot | [docs/plan/status-snapshot-2026-04-20.md](docs/plan/status-snapshot-2026-04-20.md) |
| Site architecture (post-2026-04-25 scope) | [docs/plan/site-architecture-2026-04-25.md](docs/plan/site-architecture-2026-04-25.md) |
| Ideas backlog | [docs/plan/ideas-backlog.md](docs/plan/ideas-backlog.md) |
| Brand voice + ICP | [docs/strategy/icp.md](docs/strategy/icp.md) |
| Approved copy samples | [docs/strategy/voice-samples.md](docs/strategy/voice-samples.md) |
| **Design system (canonical visual reference)** | [docs/strategy/design-system.md](docs/strategy/design-system.md) |
| Design system audit (pre-rebuild) | [docs/reviews/design-system-audit-2026-04-27.md](docs/reviews/design-system-audit-2026-04-27.md) |
| Claude Design constraint brief | [docs/strategy/design-system-brief.md](docs/strategy/design-system-brief.md) |
| **Component spec — v1** | [docs/strategy/bbi-component-spec-v1.md](docs/strategy/bbi-component-spec-v1.md) |
| Component design photos — v1 | [data/design-photos/components-v1-2026-04-27/](data/design-photos/components-v1-2026-04-27/) |
| Script reference | [scripts/README.md](scripts/README.md) |
| **AI image pipeline — Phase 1 audit** | [scripts/audit-current-images.py](scripts/audit-current-images.py) |
| **AI image pipeline — Phase 2 hero audit** | [scripts/audit-hero-images.py](scripts/audit-hero-images.py) |
| **AI image pipeline — hero review HTML** | [scripts/render-hero-review.py](scripts/render-hero-review.py) |
| Hero audit report (2026-04-28) | [data/reports/hero-audit-2026-04-28.csv](data/reports/hero-audit-2026-04-28.csv) |
| **AI image pipeline — Phase 3a img2img generator** | [scripts/generate-img2img-product-images.py](scripts/generate-img2img-product-images.py) |
| **AI image pipeline — Phase 3b vision QA** | [scripts/qa-vision-check.py](scripts/qa-vision-check.py) |
| **AI image pipeline — Phase 3c review HTML** | [scripts/render-image-review.py](scripts/render-image-review.py) |
| **AI image pipeline — Phase 3c approval server** | [scripts/serve-review.py](scripts/serve-review.py) |
| **AI image pipeline — Phase 3d push (approved only)** | [scripts/push-img2img-images.py](scripts/push-img2img-images.py) |
| Wave 0 pilot manifest (2026-04-28) | [data/reports/generated-img2img-2026-04-28.csv](data/reports/generated-img2img-2026-04-28.csv) |
| Page image generator | [scripts/generate-page-images.py](scripts/generate-page-images.py) |
| Page image sharpener | [scripts/sharpen-page-images.py](scripts/sharpen-page-images.py) |
| Image reorder (full-product to pos 1) | [scripts/reorder-product-images.py](scripts/reorder-product-images.py) |
| Logo cleaner (clarity-upscaler) | [scripts/clean-bbi-logo.py](scripts/clean-bbi-logo.py) |
| AI image library | [data/page-images/](data/page-images/) |
| Cleaned BBI logo (hi-res) | [data/logos/bbi-logo-hires.png](data/logos/bbi-logo-hires.png) |
| BBI logo — transparent background | [data/logos/bbi-logo-hires-transparent.png](data/logos/bbi-logo-hires-transparent.png) |
| **BBI logo v2 (new)** | [data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png](data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png) |
| Components v1 HTML deliverable | [data/design-photos/components-v1-2026-04-27/Components.html](data/design-photos/components-v1-2026-04-27/Components.html) |
| Components v1 tokens CSS | [data/design-photos/components-v1-2026-04-27/tokens.css](data/design-photos/components-v1-2026-04-27/tokens.css) |
| **Landing page deploy script** | [scripts/bbi-push-landing.py](scripts/bbi-push-landing.py) |
| **P1-2 OECM page — section** | [theme/sections/ds-lp-oecm.liquid](theme/sections/ds-lp-oecm.liquid) |
| **P1-2 OECM page — template** | [theme/templates/page.oecm.json](theme/templates/page.oecm.json) |
| **P1-4 Quote page — section** | [theme/sections/ds-lp-quote.liquid](theme/sections/ds-lp-quote.liquid) |
| **P1-4 Quote page — template** | [theme/templates/page.quote.json](theme/templates/page.quote.json) |
| **P1-5 Industries Hub — section** | [theme/sections/ds-lp-industries.liquid](theme/sections/ds-lp-industries.liquid) |
| **P1-5 Industries Hub — template** | [theme/templates/page.industries.json](theme/templates/page.industries.json) |
| Industries Hub draft preview | [previews/industries-hub-draft-v1.html](previews/industries-hub-draft-v1.html) |
| **P1-6 Healthcare — section** | [theme/sections/ds-lp-healthcare.liquid](theme/sections/ds-lp-healthcare.liquid) |
| **P1-6 Healthcare — template** | [theme/templates/page.healthcare.json](theme/templates/page.healthcare.json) |
| Healthcare draft preview | [previews/healthcare-draft-v1.html](previews/healthcare-draft-v1.html) |
| **P1-7 Education — section** | [theme/sections/ds-lp-education.liquid](theme/sections/ds-lp-education.liquid) |
| **P1-7 Education — template** | [theme/templates/page.education.json](theme/templates/page.education.json) |
| **P1-8 Government — section** | [theme/sections/ds-lp-government.liquid](theme/sections/ds-lp-government.liquid) |
| **P1-8 Government — template** | [theme/templates/page.government.json](theme/templates/page.government.json) |
| **P1-9 Non-Profit — section** | [theme/sections/ds-lp-non-profit.liquid](theme/sections/ds-lp-non-profit.liquid) |
| **P1-9 Non-Profit — template** | [theme/templates/page.non-profit.json](theme/templates/page.non-profit.json) |
| **P1-10 Professional Services — section** | [theme/sections/ds-lp-professional-services.liquid](theme/sections/ds-lp-professional-services.liquid) |
| **P1-10 Professional Services — template** | [theme/templates/page.professional-services.json](theme/templates/page.professional-services.json) |
