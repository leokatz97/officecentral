# Stage 5 Launch Audit — 4.1 Inventory Verification
**Date:** 2026-05-08
**Auditor:** Claude Code (read-only pass)

---

## Template inventory

Templates present in `theme/templates/` as of 2026-05-08:

### Collection templates (10)
| Template | Purpose |
|---|---|
| `collection.business-furniture.json` | Vertical hub — 9 category tiles |
| `collection.category.json` | Shared category-level template (Seating, Desks, etc.) |
| `collection.accessories.json` | Accessories category override |
| `collection.boardroom.json` | Boardroom category override |
| `collection.desks.json` | Desks category override |
| `collection.ergonomic-products.json` | Ergonomic Products category override |
| `collection.panels-room-dividers.json` | Panels & Dividers category override |
| `collection.quiet-spaces.json` | Quiet Spaces category override |
| `collection.seating.json` | Seating category override |
| `collection.storage.json` | Storage category override |
| `collection.tables.json` | Tables category override |
| `collection.base.json` | Sub-collection product listing (template_suffix = "base") |
| `collection.json` | Starlite default collection fallback |

Total collection templates: **13**

### Page templates (22)
| Template | Purpose | Wave |
|---|---|---|
| `page.about.json` | About Us | Wave C |
| `page.brands.json` | Brands Hub | Wave C |
| `page.brands-ergocentric.json` | ergoCentric brand page | Wave C |
| `page.brands-global-teknion.json` | Global/Teknion brand page | Wave C |
| `page.brands-keilhauer.json` | Keilhauer brand page | Wave C |
| `page.contact.json` | Contact | Wave C |
| `page.customer-stories.json` | Customer Stories | Wave G |
| `page.delivery.json` | Delivery & Installation | Wave C |
| `page.design-services.json` | Design Services | Phase 1 |
| `page.education.json` | Education industry page | Phase 1 |
| `page.faq.json` | FAQ | Phase 1 |
| `page.government.json` | Government industry page | Phase 1 |
| `page.healthcare.json` | Healthcare industry page | Phase 1 |
| `page.industries.json` | Industries Hub | Phase 1 |
| `page.non-profit.json` | Non-Profit industry page | Phase 1 |
| `page.oecm.json` | OECM Procurement | Phase 1 |
| `page.our-work.json` | Our Work / Portfolio | Wave C |
| `page.professional-services.json` | Professional Services | Phase 1 |
| `page.quote.json` | Request a Quote | Phase 1 |
| `page.relocation.json` | Relocation Management | Wave C |
| `page.json` | Starlite default page fallback | — |

Total page templates: **21 BBI + 1 Starlite fallback**

### Other templates
| Template | Notes |
|---|---|
| `index.json` | Homepage |
| `gift_card.liquid` | Shopify gift card (Starlite) |

### Missing templates (required before launch)
| Template | Row ID | Needed for |
|---|---|---|
| `product.json` (BBI) | PDP-1 | All 594 active products |
| `404.json` | 404-1 | Custom 404 page |
| `blog.json` | BLOG-TPL-1 | Resources hub |
| `article.json` | BLOG-TPL-1 | Blog articles |

---

## DS section inventory

BBI design-system sections in `theme/sections/ds-*.liquid`:

### Landing page sections (ds-lp-*) — 22 files
All Phase 1 + Wave C pages have corresponding section files.

| Section | Status |
|---|---|
| `ds-lp-about.liquid` | File exists |
| `ds-lp-brands.liquid` | File exists |
| `ds-lp-brands-ergocentric.liquid` | File exists |
| `ds-lp-brands-global-teknion.liquid` | File exists |
| `ds-lp-brands-keilhauer.liquid` | File exists |
| `ds-lp-contact.liquid` | File exists |
| `ds-lp-customer-stories.liquid` | File exists |
| `ds-lp-delivery.liquid` | File exists |
| `ds-lp-design-services.liquid` | File exists |
| `ds-lp-education.liquid` | File exists |
| `ds-lp-faq.liquid` | File exists |
| `ds-lp-government.liquid` | File exists |
| `ds-lp-healthcare.liquid` | File exists |
| `ds-lp-industries.liquid` | File exists |
| `ds-lp-non-profit.liquid` | File exists |
| `ds-lp-oecm.liquid` | File exists |
| `ds-lp-our-work.liquid` | File exists |
| `ds-lp-professional-services.liquid` | File exists |
| `ds-lp-quote.liquid` | File exists |
| `ds-lp-relocation.liquid` | File exists |

### Collection sections
| Section | Purpose |
|---|---|
| `ds-cc-base.liquid` | Category-hub section (T3 layout) |
| `ds-cs-base.liquid` | Sub-collection product listing (T4 layout) |

### Missing sections (required before launch)
| Section | Row ID | Notes |
|---|---|---|
| `ds-pdp-base.liquid` | PDP-1 | Greenfield build confirmed by Stage 4a audit |
| `ds-system-404.liquid` | 404-1 | Custom 404 branded page |
| `ds-blog-list.liquid` | BLOG-TPL-1 | Blog listing section |
| `ds-article.liquid` | BLOG-TPL-1 | Article section |

---

## Sub-collection template_suffix status

Per `stage-3.2c-migration-execution.md` and commit `d3eb79c`:
- **62+ sub-collections** have `template_suffix = "base"` applied via Shopify API
- These render via `collection.base.json` → `ds-cs-base.liquid`
- 2 empty collections (`metal-shelving`, `audio-visual-equipment`) had no products at time of audit — these are `WARN` not `FAIL` per PB-11 audit

---

## Summary

| Category | Count |
|---|---|
| Total templates in repo | 36 |
| BBI-custom templates | 35 |
| Starlite fallback templates | 2 (collection.json, page.json) |
| Missing templates (pre-launch blockers) | 4 |
| DS sections present | 24 |
| DS sections missing (pre-launch) | 4 |
| Sub-collections with BBI suffix | 62+ |
