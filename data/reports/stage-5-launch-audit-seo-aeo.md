# Stage 5 Launch Audit — 4.11 SEO / AEO
**Date:** 2026-05-08
**Sources:** `theme/snippets/bbi-org-schema.liquid`, `theme/snippets/meta-tags.liquid`, `docs/plan/bbi-build-state.md` (Wave D + Wave E SEO rows), `CLAUDE.md` SEO rules
**Auditor:** Claude Code (read-only pass)

---

## Important constraint

Per `CLAUDE.md` SEO rules:
> **SEO-AUDIT-1** is a hard gate before LAUNCH-0. Use the DataForSEO MCP to crawl every page in the `bbi_landing` gate. All `block`-severity issues must be resolved before LAUNCH-0 can run.

This audit documents current state based on static file inspection. **DataForSEO MCP crawl is required before marking SEO-AUDIT-1 done.**

---

## What exists today

### Organization schema (`bbi-org-schema.liquid`)
- ✓ Built and deployed (commit `f1b85c3`, pre-Stage-3 drift fix)
- ✓ `@type: ["Organization", "LocalBusiness"]`
- ✓ `name`, `url`, `logo`, `telephone`, `email`, `address`, `geo`, `openingHours`, `areaServed`, `sameAs`, `hasOfferCatalog`, `parentOrganization`
- ✓ OECM described in `description` field
- ✓ Rendered via `bbi-nav.liquid` → fires on every BBI page
- ⚠️ `alternateName: "BBI"` — per brand voice rules, "BBI" should not appear to customers. This is a schema field not visible to users; AI crawlers will read it. Acceptable per JSON-LD spec context.

### `llms.txt` (AI-1)
- ✓ Deployed (commit `a2118f3`)

### `robots.txt` (AI-2)
- ✓ Audited (commit `24ab01e`)

### `audit-ai-readability.py` script (AI-12)
- ✓ Built (commit `a752eb3`)

### SEO meta titles + descriptions (PE-4)
- ✓ 100 Hero SKUs have SEO meta set (commit `a2118f3`)

### Product redirects (W0-3)
- 🟡 `data/url-redirects.csv` exists but manual upload in Shopify Admin is pending
- `data/redirects/sector-collections-redirects-2026-04-28.csv` — PARKED (comment in file: do not import until `/collections/business-furniture` is live)
- `data/redirects/sector-products-redirects-2026-04-28.csv` — 2 redirects

---

## What is missing

### Wave D — SEO foundation (all ⬜)
| Row | Task | Severity |
|---|---|---|
| W0-1 | Google Search Console + GA4 setup | BLOCK — no SEO measurement without this |
| W0-2 | Create BBI Google Business Profile | FIX |
| W0-2b | Google Reviews seeding strategy | NIT (post-launch) |
| W0-6 | Parent domain backlinks (officecentral.com, brantbasics.com) | FIX |
| W0-7 | OECM + "Since 1964" trust signals site-wide | NIT — already on landing pages |
| W0-3 | Upload product redirects CSV | FIX (manual Admin action) |

### Wave E — SEO hardening (all ⬜)
| Row | Task | Severity |
|---|---|---|
| AI-4 | Organization schema on homepage + About | ⚠️ Already in bbi-org-schema.liquid — confirm it renders from index.json |
| AI-6 | BreadcrumbList JSON-LD shared snippet | FIX |
| AI-7 | Entity-clarity copy on homepage | FIX |
| AI-8 | OECM page copy hardening | FIX |
| AI-9 | FAQ blocks on category pages | FIX |
| AI-5 | FAQ schema on OECM, Design Services, top posts | FIX |
| SEO-AUDIT-1 | Technical SEO via DataForSEO MCP | BLOCK (hard gate) |

### PDP schema (Wave G)
| Row | Task | Severity |
|---|---|---|
| PDP-2 | Product JSON-LD (name, description, image, offers, brand, sku) | BLOCK for PDPs |

---

## Known SEO gaps (non-schema)

| Gap | Where | Severity |
|---|---|---|
| H1 hierarchy not audited | All pages | FIX (DataForSEO will surface this) |
| Meta description completeness | Wave C pages + collection pages | FIX |
| Canonical tags | All pages | FIX (DataForSEO will check) |
| Internal link depth (some pages 4+ clicks from homepage) | Sub-collections | FIX |
| Image alt text — product images | Sub-collection and PDP pages | FIX |
| Core Web Vitals not measured | All pages | FIX (Lighthouse in PERF-AUDIT-1) |

---

## GSC verification async note

Google Search Console verification can take 5–14 calendar days after the DNS TXT record is added. Per the launch plan, W0-1 should be started at Phase 4 kickoff to run asynchronously. Only the GSC verification status blocks Phase 7 (LAUNCH-3 sitemap resubmission).

---

## DataForSEO MCP — required crawl before SEO-AUDIT-1 can close

Per CLAUDE.md mandatory SEO workflow:
1. Use `on_page_instant_pages` or `on_page_lighthouse` tools against the BBI Landing Dev preview URL
2. Crawl every published page in `bbi_landing` gate
3. Check: meta titles/descriptions, H1 hierarchy, schema validation, canonicals, broken links, Lighthouse mobile perf ≥80, Core Web Vitals
4. Output per-page issue list with severity (block / fix / waive)
5. All `block` items resolved or waived before LAUNCH-0

**This crawl cannot run until Stage 4b (PDPs) and Wave C (trust pages) are deployed to the dev theme.**

---

## Summary

| Category | Status |
|---|---|
| Organization schema | ✓ Built + deployed |
| llms.txt, robots.txt | ✓ Done |
| Hero 100 SEO metas | ✓ Done (100 products) |
| GSC + GA4 setup | ✗ BLOCK — W0-1 not started |
| BreadcrumbList JSON-LD | ✗ FIX — AI-6 not built |
| Product JSON-LD | ✗ BLOCK — PDP-2 (needs ds-pdp-base.liquid first) |
| FAQ schema | ✗ FIX — AI-5/AI-9 not started |
| DataForSEO audit | ✗ BLOCK hard gate — cannot run until Wave C + Stage 4b deployed |
| Redirect CSV upload | 🟡 Pending Admin manual action |
