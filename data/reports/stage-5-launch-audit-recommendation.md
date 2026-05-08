# Stage 5 Launch Audit — Synthesized Recommendations
**Date:** 2026-05-08
**Based on:** Audit categories 4.1–4.14

---

## BLOCK items — must fix before launch

These items prevent a functional or trustworthy launch. Nothing ships until these are resolved or explicitly waived.

| # | Issue | Source audit | Phase | Prompt sketch |
|---|---|---|---|---|
| B-1 | **PDP template missing** — 594 active products render on Starlite `main-product.liquid`. No BBI chrome, no spec table, no trust pills, no RFQ CTA for sold-out. | 4.5, 4.6, 4.12 | Phase 2 (Stage 4b) | "Build `ds-pdp-base.liquid` + `product.json` + 3 snippets per Stage 4a decision doc. Greenfield build from ds-lp-* pattern. Include visual swatch variant picker. Smoke-test 5 product states per PDP-3." |
| B-2 | **Variant picker is text-only** — All variant options render as borderless text. Colour swatches required per explicit design feedback. Affects every PDP. | 4.6 | Phase 2 (inside Stage 4b) | "Inside ds-pdp-base.liquid: build custom swatch picker with colour name→hex Liquid mapping. Non-colour pickers as styled pill buttons with active state and 44px touch targets." |
| B-3 | **SMART-1 "View all" collections not created** — All 10 "View all [Category]" CTAs on category hub pages 404. Every category page (T3) has a broken primary CTA. | 4.2, 4.3 | Phase 2 (concurrent with 4b) | "Run `scripts/create-smart-collections.py` (or use Admin API directly) to create 10 view-all smart collections per SMART-1 spec. Dry-run first. Verify each collection returns non-zero product count." |
| B-4 | **SMART-1 brand-filtered collections not created** — Brand pages (`/pages/brands-keilhauer` etc.) dead-end; no "Shop [Brand] products" destination exists. | 4.2, 4.3 | Phase 2 | "Create 4 brand-filtered smart collections: keilhauer (vendor=Keilhauer), global-teknion (vendor=Global OR Teknion), ergocentric (vendor=ergoCentric), oecm-eligible (tag=oecm-eligible)." |
| B-5 | **GSC + GA4 not set up** — No analytics tracking before launch means zero post-launch SEO signal. | 4.11 | Phase 4 (start early — async) | "Create GSC property at search.google.com for brantbusinessinteriors.com. Add DNS TXT verification record. Create GA4 property. Add GA4 snippet to theme.liquid. Note: GSC verification takes 5–14 calendar days — start at Phase 4 kickoff." |
| B-6 | **Product JSON-LD missing** — No Product schema on any PDP. Blocks Google Shopping and Rich Results. | 4.11 | Phase 2 (inside Stage 4b, PDP-2) | "Build `bbi-product-jsonld.liquid` snippet inside Stage 4b. Include name, description, image, offers (price, availability, currency=CAD), brand, sku. Validate with Google Rich Results Test on 3 PDPs." |
| B-7 | **DataForSEO SEO-AUDIT-1 not run** — Hard gate per CLAUDE.md. Cannot close before LAUNCH-0. | 4.11 | Phase 4 | "Run DataForSEO MCP `on_page_instant_pages` and `lighthouse` tools against dev theme preview URL. Crawl all bbi_landing pages. Output per-page issue list. Resolve all block-severity items." |
| B-8 | **Wave C pages' Shopify Page records unconfirmed** — 10 Wave C pages have templates+sections but Stage 0 audit found these were built outside worktree. Page records and template_suffix not verified via API. | 4.3 | Phase 1 (next session) | "Run Admin API: GET /pages.json?limit=250. For each of the 10 handles (about, brands, brands-keilhauer, brands-global-teknion, brands-ergocentric, our-work, contact, delivery, relocation, customer-stories): confirm published=true, template_suffix matches." |
| B-9 | **Policy pages empty** — No Privacy Policy, Terms of Service, Refund Policy, or Shipping Policy content. PIPEDA/CASL required. B2B site cannot launch without. | 4.12 | Phase 4 | "Steve: fill in policy pages via Shopify Admin → Settings → Policies. Claude Code can draft PIPEDA/CASL-compliant policy copy for Steve's review if needed." |

---

## FIX items — should fix before launch

These items degrade user experience, SEO, or brand consistency but do not prevent the site from functioning.

| # | Issue | Source audit | Phase | Prompt sketch |
|---|---|---|---|---|
| F-1 | **404 page uses Starlite** — No `404.json` template. Custom 404 experience missing. | 4.1, 4.12 | Phase 2 | "Build `ds-system-404.liquid` + `404.json` per Wave G row 404-1. H1 'Page not found' + search box + 4 category tiles + phone CTA + quote button. Add `template == '404'` to gate." |
| F-2 | **Blog/Article templates use Starlite** — Chrome continuity break even with zero posts. SEO template infrastructure missing. | 4.13 | Phase 2 | "Build `ds-blog-list.liquid` + `ds-article.liquid` + `blog.json` + `article.json` per BLOG-TPL-1. Shell only — no posts needed. Add blog/article to gate." |
| F-3 | **BreadcrumbList JSON-LD missing** — No shared `bbi-breadcrumb-jsonld.liquid` snippet. Breadcrumb rich results blocked. | 4.11 | Phase 3 (Wave E) | "Build `bbi-breadcrumb-jsonld.liquid` snippet per AI-6. Render from ds-cc-base, ds-cs-base, and ds-pdp-base. One snippet owns all breadcrumb schema." |
| F-4 | **Organization schema on homepage unconfirmed** — `bbi-org-schema.liquid` is rendered from `bbi-nav`. Homepage uses `bbi-nav-wrap.liquid` wrapper — confirm the nav snippet is actually called and the schema fires. | 4.11 | Phase 3 (Wave E) | "View-source on dev theme homepage. Confirm `<script type='application/ld+json'>` block with `@type: Organization` is present. If missing, add `{% render 'bbi-org-schema' %}` to `bbi-nav-wrap.liquid`." |
| F-5 | **INTERLINK-3 final audit not run** — No cross-link audit since Wave B. Wave C pages, Stage 3.2 sub-collections, and redirect inventory are all unverified. | 4.3 | Phase 3 (Wave E) | "Run `scripts/audit-interlinks.py` against dev theme. Expect 0 FAIL. Fix any broken href targets. Update bbi-interlinking-map.md with results." |
| F-6 | **Redirect CSVs not uploaded** — `url-redirects.csv` and `sector-collections-redirects-2026-04-28.csv` are ready but not in Shopify Admin. Old indexed URLs return 404. | 4.14 | Phase 3 | "Upload url-redirects.csv to Admin → Navigation → URL Redirects. Strip comment lines from sector-collections CSV then upload. Review willow-bariatric-chair row in sector-products CSV before upload." |
| F-7 | **T4 sub-collection reference not locked** — No pixel-diff baseline for sub-collection pages. Visual regressions cannot be detected programmatically. | 4.4 | Phase 3 | "Run capture-bbi-baselines.py against dev theme. Steve signs off on highback-seating at 1280px. Run again with --lock flag to capture locked/ baseline." |
| F-8 | **Cart page has wrong "Continue shopping" destination** — Empty cart routes to `/collections/all` (Shopify default) instead of `/collections/business-furniture`. | 4.8 | Phase 3 | "In `cart.liquid` or cart JSON template, change `routes.all_products_collection_url` to `/collections/business-furniture` for the empty-cart CTA." |
| F-9 | **ergonomic-products/panels/quiet-spaces collections use title-match rules** — Fragile; new products with different title phrasing won't auto-populate. | 4.2 | Phase 3 | "Add `type:ergonomic`, `type:panels-dividers`, `type:quiet-spaces` tags to relevant products. Update smart collection rules from title-match to tag-match. Dry-run first." |
| F-10 | **LEAD-INBOX-1 inboxes not provisioned** — Hard prereq for LEAD-3 RFQ modal. Steve must provision quotes@, design@, info@ inboxes. | 4.7 | Phase 3 (Steve action) | "Steve: provision 3 email addresses in your email provider. Forward all to steve@brantbusinessinteriors.com. Send test from external domain. Confirm receipt. Mark LEAD-INBOX-1 ✅." |
| F-11 | **FAQ schema not added to category pages** — AI-9 row (Wave E) not started. 9 category hub pages have no FAQPage schema. | 4.11 | Phase 3 (Wave E) | "Add 3–5 Q&A blocks to each of 9 ds-cc-base category hub templates, wrapped in FAQPage JSON-LD. Source questions from voice-samples.md and product FAQ patterns." |
| F-12 | **SYS-VERIFY-1 not run** — System pages (cart, search, account) not verified for chrome consistency. | 4.12 | Phase 3 (Wave E) | "DOM check: GET /cart, /search, /account/login. Assert: 0 bbi-header, 0 bbi-footer. Shopify chrome intact. No double nav." |
| F-13 | **`/pages/shop` redirect missing** — Old shop hub URL (removed in scope change 2026-04-25) has no redirect to `/collections/business-furniture`. | 4.14 | Phase 3 | "Add single redirect in Shopify Admin: /pages/shop → /collections/business-furniture." |

---

## NIT items — post-launch OK

These are improvements that do not affect launch viability.

| # | Issue | Source audit | Notes |
|---|---|---|---|
| N-1 | RFQ modal (LEAD-3) | 4.7 | `/pages/quote` works as fallback. Modal is a conversion improvement. Do after LEAD-INBOX-1 (Steve action). |
| N-2 | Cart page full BBI redesign | 4.8 | Currently Starlite per architecture intent. Rebuild post-launch as CART-1 backlog item. |
| N-3 | `room-break-room` empty collection | 4.2 | Orphaned; not user-facing. Clean up in post-launch maintenance pass. |
| N-4 | W0-2 Google Business Profile | 4.11 | Create post-launch or in parallel with Phase 4. |
| N-5 | OECM tagging pass (0% coverage) | 4.6 | Wire badge logic in Stage 4b; run tagging pass post-launch. |
| N-6 | Brand logo uploads for brand block | — | Stage 4b ships text+badge only; logo assets are content work. |
| N-7 | IMG-PHASE2 product image regen | 4.9 | Soft gate. Waiver CSV acceptable if coverage < 80%. |
| N-8 | W0-6 parent domain backlinks | 4.11 | Coordinate with officecentral.com and brantbasics.com webmasters. Post-launch. |

---

## Items not in the current plan (gaps found by audit)

| Item | Source audit | Recommendation |
|---|---|---|
| `capture-bbi-baselines.py` + `diff-bbi-baselines.py` tooling | 4.4, 4.5 | Created this session. Add to CLAUDE.md Definition of Done. |
| Stage 3.2c handle redirect audit | 4.14 | New: compare old sub-collection handles (pre-migration) to new canonical handles (`stage-3.2c.6-canonical-handles.csv`). Generate redirect CSV. Estimate: 0.5 dev days. |
| T4 sub-collection locked reference | 4.4 | New: lock dev-theme screenshot of sub-collection after Steve QA. Tooling now available. |
| `willow-bariatric-chair` redirect conflict | 4.14 | Conflict found: redirect CSV says route to collection, but product was re-published. Resolve before uploading. |

---

## Critical path

```
Phase 1 (next session)
  └── B-8: Verify Wave C Shopify Page records [0.5 day]
      └── Unblocks: Wave C page visibility on dev theme

Phase 2 [3-4 dev days]
  ├── B-1+B-2+B-6: Stage 4b — PDP build (ds-pdp-base.liquid + product.json + snippets)
  ├── B-3+B-4: SMART-1 — Create 14 smart collections
  └── F-1+F-2: 404-1 + BLOG-TPL-1 — missing system templates

Phase 3 [2-3 dev days]
  ├── F-3: AI-6 BreadcrumbList JSON-LD
  ├── F-5: INTERLINK-3 final audit
  ├── F-6: Upload redirect CSVs
  ├── F-7+F-8+F-9: Polish items
  └── F-11+F-12: FAQ schema + SYS-VERIFY-1

Phase 4 [1 dev day + up to 14 calendar days]
  ├── B-5: GSC + GA4 setup (start early — async verification)
  ├── B-9: Policy pages (Steve content)
  ├── F-10: LEAD-INBOX-1 (Steve action)
  └── B-7: SEO-AUDIT-1 via DataForSEO MCP

Phase 5 [0.5 dev day]
  └── LAUNCH-0 → LAUNCH-1 → LAUNCH-2 (Steve manual publish)
```

**Total dev time estimate:** 8–10 dev days
**Total calendar time:** 8–10 dev days + up to 14 calendar days for GSC verification (async, does not block dev work)

**Calendar critical path bottleneck:** GSC DNS verification. Start it on Phase 4 day 1. Everything else can proceed in parallel.
