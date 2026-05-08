# Stage 5 Launch Audit — 4.13 Blog Templates
**Date:** 2026-05-08
**Sources:** `theme/templates/` (directory listing), `theme/sections/main-blog.liquid`, `theme/sections/main-article.liquid`, `docs/plan/bbi-build-state.md` (BLOG-TPL-1)
**Auditor:** Claude Code (read-only pass)

---

## Current state

### `blog.json` — Does NOT exist
No `theme/templates/blog.json` exists. The blog hub (`/blogs/news`) renders via the Starlite default mechanism using `main-blog.liquid`.

### `article.json` — Does NOT exist
No `theme/templates/article.json` exists. Individual articles render via `main-article.liquid` (Starlite).

### What `main-blog.liquid` and `main-article.liquid` provide (Starlite)
- Generic blog listing with Starlite color scheme
- No BBI nav/footer (Starlite chrome)
- No BBI design tokens
- Standard Shopify blog pagination
- No related products module
- No FAQPage schema
- No "buy by sector" crosslinks

---

## BLOG-TPL-1 scope (from `bbi-build-state.md`)

> BBI-styled templates only — no posts yet. **Resources hub** (paginated list, category filter chips, optional tag filter, related products from collection metafield). **Article** (hero image, prose body, related products module, FAQPage schema if `article.metafields.faq` exists, share buttons, author/date metadata). Add `template == 'blog'` and `template == 'article'` to `bbi_landing` gate.

### Files to create

| File | Type | Notes |
|---|---|---|
| `theme/templates/blog.json` | Template | Points to `ds-blog-list.liquid` |
| `theme/templates/article.json` | Template | Points to `ds-article.liquid` |
| `theme/sections/ds-blog-list.liquid` | Section | BBI Resources hub layout |
| `theme/sections/ds-article.liquid` | Section | BBI article layout |
| Gate update: `theme/layout/theme.liquid` | Gate | Add `template == 'blog'` and `template == 'article'` |

---

## Content status

- **No blog posts exist yet.** The blog templates are shells — content comes after launch per the build plan.
- Per `CLAUDE.md`: *"First posts (BL-1..BL-6 + B1..B10) stay in post-launch backlog. Every blog post must start with DataForSEO MCP keyword research."*
- Blog hub (`/blogs/news`) will render an empty list on a BBI-styled template — this is acceptable for launch.

---

## Why this matters before launch

1. **SEO benefit** — Even with zero posts, a BBI-styled blog hub with correct meta, H1, and schema establishes the page in GSC and signals content intent.
2. **Chrome consistency** — A customer navigating to `/blogs/news` from the nav currently sees Starlite. This is a continuity break even with zero posts.
3. **AEO / AI readiness** — Articles will need FAQPage schema and structured data from day 1. Building the template correctly now avoids retrofitting.

---

## Effort estimate (BLOG-TPL-1)

Per `bbi-build-state.md` row BLOG-TPL-1:

| Task | Estimate |
|---|---|
| `blog.json` template | 10 min |
| `article.json` template | 10 min |
| `ds-blog-list.liquid` section | 2–3 hours |
| `ds-article.liquid` section | 2–3 hours |
| Gate update + push | 15 min |
| Smoke test (empty blog, no article edge case) | 30 min |
| **Total** | **~6 hours** |

---

## Severity

**FIX** — Blog templates are required before launch for chrome consistency and SEO foundation. No blog posts are needed to launch (empty hub is acceptable). However, a Starlite-rendered `/blogs/news` at launch is a visible brand inconsistency.

The specific note in `bbi-build-state.md`: BLOG-TPL-1 is in Wave G (pre-Wave E hardening). Build must complete before PERF-AUDIT-1 and SEO-AUDIT-1 run — otherwise the DataForSEO crawl will find Starlite pages for blog/article templates.

---

## DataForSEO note

Per `CLAUDE.md` mandatory SEO workflow — blog posts require keyword research:
> "Every blog post must start with DataForSEO MCP keyword research — pull search volume, difficulty, related keywords, SERP competitors, and 'people also ask' before drafting."

This applies to posts, not the template itself. The template can be built without DataForSEO. The first posts (BL-1..BL-6) must go through the keyword research workflow before drafting.
