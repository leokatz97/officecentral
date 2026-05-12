# BBI Interlinking Map

**Last updated:** 2026-05-06
**Companion to:** `docs/plan/bbi-build-state.md`
**Consumed by:** `scripts/audit-interlinks.py` (to build, INTERLINK-1)
**Audit pattern source:** P1-11 — see commits `905db28`, `0fe3de9`, `0d452eb`, `b4ae936`

---

## What this file is

The single source of truth for **every cross-link that must exist on every BBI page.** One row per page, three columns:

- **Outbound (must exist)** — links the page must contain. If missing → bug.
- **Inbound (should exist)** — pages that should link to this one. If missing → opportunity gap.
- **Verified** — last audit run that confirmed all outbound links return 200 + all inbound coverage holds.

When a new page launches, add its row + update the inbound column on every existing page that should link to it. Then run `/scripts/audit-interlinks.py` (when built) to confirm reality matches the map.

---

## Audit pattern (the 12-point check)

Battle-tested in P1-11 and `9c8b7db`. Re-run on every Phase 2/3/4 page set.

1. **Nav consistency** — every page renders the same `bbi-nav` with the same items, in the same order.
2. **Active nav state** — the nav item matching the current page is marked `is-current`.
3. **Breadcrumbs** — `Home > [Section] > [Page]`. Middle crumb is the parent hub, not a raw slug.
4. **Crosslinks unique** — each crosslink tile on a page points to a distinct destination (Healthcare's tile-2 bug taught this).
5. **Crosslink hrefs return 200** — no dead `/pages/#` or stale slugs from removed verticals.
6. **Industries Hub crosslinks** — `/pages/industries` cards link to all 5 vertical pages (no archived ones).
7. **Footer industries column** — every page's footer lists all 5 verticals (Healthcare, Education, Government, Non-Profit, Professional Services).
8. **Footer Services column** — every page's footer lists `/pages/design-services`, `/pages/delivery`, `/pages/relocation`, `/pages/oecm`, `/pages/faq`. (FAQ-on-industries-hub gap surfaced in `9c8b7db` — audit caught it.)
9. **Footer parity** — same footer on every page. Spot-check 2–3 pages.
10. **Phone CTA presence** — `tel:18008359565` in header + every CTA band.
11. **Quote modal works** — clicking "Get a Quote" opens modal or navigates to `/pages/quote` (not a 404).
12. **🔴 Live-DOM matches worktree source.** Audit must compare what's on the dev theme to what's in the worktree's section file. Drift means a stale push happened (worktree-root bug, see lesson #4 in `bbi-build-state.md`). Symptom: industries page lost embedded header/footer between commits when single-slug pushes from main repo overwrote worktree work.

---

## Pre-deploy DOM checks (per page)

These are the one-line JS assertions every new page must pass before its row is marked ✅ in `bbi-build-state.md`:

```javascript
// run in dev preview console
({
  headers:        document.querySelectorAll('.bbi-header').length,           // expect 1
  footers:        document.querySelectorAll('.bbi-footer').length,           // expect 1
  starlite:       !!document.querySelector('.shopify-section-group-header-group'), // expect false
  nav_links:      document.querySelectorAll('.bbi-nav-item').length,         // expect ≥5
  logo_src:       document.querySelector('.bbi-header__logo img')?.src || '', // expect non-empty
  footer_industries: Array.from(document.querySelectorAll('.bbi-footer a'))
                       .map(a => a.getAttribute('href'))
                       .filter(h => h?.startsWith('/pages/'))
                       .filter(h => ['/pages/healthcare','/pages/education','/pages/government','/pages/non-profit','/pages/professional-services'].includes(h))
                       .length,                                              // expect 5
  footer_services:   Array.from(document.querySelectorAll('.bbi-footer a'))
                       .map(a => a.getAttribute('href'))
                       .filter(h => ['/pages/design-services','/pages/delivery','/pages/relocation','/pages/oecm','/pages/faq'].includes(h))
                       .length,                                              // expect 5 (FAQ gap surfaced 9c8b7db)
  phone:          !!document.querySelector('a[href="tel:18008359565"]'),     // expect true
  breadcrumb_3:   document.querySelectorAll('.bbi-crumbs li').length,        // expect ≥2 (Home > X)
  crosslinks_unique: (() => {
                      const hrefs = Array.from(document.querySelectorAll('.lp-crosslinks__tile')).map(a => a.getAttribute('href'));
                      return hrefs.length === new Set(hrefs).size;
                    })(),                                                    // expect true
})
```

---

## Page interlinking matrix — Phase 1 (live on dev)

### `/` — Homepage

| | |
|---|---|
| Outbound (must exist) | `/pages/quote`, `/collections/business-furniture`, `/collections/seating`, `/collections/desks`, `/collections/storage`, `/collections/boardroom`, `/pages/oecm`, `/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/non-profit`, `/pages/professional-services`, `/pages/design-services`, `/pages/delivery`, `/pages/our-work`, `tel:18008359565` |
| Inbound (should exist) | nav logo on every page; footer "Home" |
| Verified | ⬜ — pending NAV-4 (homepage nav unification) |

### `/pages/oecm` — OECM Supplier Partner

| | |
|---|---|
| Outbound (must exist) | `/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Homepage trust bar, every industry page (OECM mention), Services nav dropdown |
| Verified | ✅ commit `905db28` (header/footer + breadcrumb), `b4ae936` (logo) |

### `/pages/design-services` — Free Design Layout

| | |
|---|---|
| Outbound (must exist) | `/pages/quote`, `/pages/our-work`, `/collections/business-furniture`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Every category page ("Free design layout" CTA), Homepage services strip, Services nav |
| Verified | ✅ commit `905db28`, `b4ae936` |

### `/pages/quote` — Request a Quote

| | |
|---|---|
| Outbound (must exist) | `/pages/design-services`, `/pages/oecm`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Site-wide floating Quote button, every page's CTA, header right-rail button |
| Verified | ✅ commit `0fe3de9`, `b4ae936` |

### `/pages/faq` — FAQ

| | |
|---|---|
| Outbound (must exist) | `/pages/quote`, `/pages/oecm`, `/pages/design-services`, `/pages/delivery`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Every product page sticky "Questions?" link, Services nav, footer |
| Verified | ✅ commit `0d452eb`, `b4ae936` |

### `/pages/industries` — Industries Hub

| | |
|---|---|
| Outbound (must exist) | `/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/non-profit`, `/pages/professional-services`, `/collections/business-furniture`, all 9 category collections (in Browse the catalogue section), nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Nav "Industries" item, homepage industries strip, every industry page breadcrumb |
| Verified | ✅ commit `e98f91f` (Browse + FAQ added), `905db28` |

### `/pages/healthcare`

| | |
|---|---|
| Outbound (must exist) | `/collections/seating`, `/collections/tables`, `/collections/desks`, `/pages/oecm`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Industries Hub card, nav Industries dropdown, homepage industries strip, OECM page (Healthcare buyers mention), 4 sibling industry pages (footer industries column) |
| Verified | ✅ commit `905db28` (crosslink fix tile-2 → tables, footer pro-services) |

### `/pages/education`

| | |
|---|---|
| Outbound (must exist) | `/collections/training-flip-top-tables`, `/collections/stacking-seating`, `/collections/storage`, `/collections/panels-room-dividers`, `/pages/oecm`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | same as healthcare pattern |
| Verified | ✅ commit `905db28` (footer pro-services) |

### `/pages/government`

| | |
|---|---|
| Outbound (must exist) | `/collections/desks`, `/collections/storage`, `/collections/panels-room-dividers`, `/collections/boardroom`, `/pages/oecm`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | same as healthcare pattern |
| Verified | ✅ commit `905db28` |

### `/pages/non-profit`

| | |
|---|---|
| Outbound (must exist) | `/collections/seating`, `/collections/tables`, `/collections/storage`, `/collections/desks`, `/pages/oecm`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | same as healthcare pattern |
| Verified | ✅ commit `905db28` |

### `/pages/professional-services`

| | |
|---|---|
| Outbound (must exist) | `/collections/desks`, `/collections/seating`, `/collections/ergonomic-products`, `/collections/boardroom`, `/pages/quote`, `/pages/industries`, nav, footer industries (×5), `tel:18008359565` (no OECM emphasis — private sector) |
| Inbound (should exist) | same as healthcare pattern + brand pages (Keilhauer, ergoCentric callouts) |
| Verified | ✅ commit `ee44b06` (built), no OECM bar by design |

---

## Page interlinking matrix — Phase 2 (collection-category pages, to build)

These rows should be filled in as PB-10/P2-* land. Spec from `docs/plan/site-architecture-2026-04-25.md`.

### `/collections/business-furniture` — Business Furniture vertical (P2-1)

| | |
|---|---|
| Outbound (must exist) | All 9 category collections (Seating, Desks, Storage, Tables, Boardroom, Ergonomic, Panels, Accessories, Quiet Spaces), `/pages/design-services`, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Nav "Shop Furniture" item, every category page breadcrumb, homepage shop grid, every sub-collection breadcrumb |
| Verified | ⬜ |

### `/collections/seating` — Seating category (P2-2)

| | |
|---|---|
| Outbound (must exist) | 16 sub-collections (highback-seating, mesh-seating, lounge-chairs-seating, etc.), `/collections/all-seating` (smart), `/pages/brands-ergocentric`, `/collections/business-furniture` (breadcrumb), `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical tile, homepage shop grid, Industries Hub Browse the catalogue, healthcare/non-profit/pro-services crosslinks |
| Verified | ⬜ |

### `/collections/desks` — Desks & Workstations (P2-3)

| | |
|---|---|
| Outbound (must exist) | 9 sub-collections (l-shape-desks, u-shape-desks, height-adjustable, benching, etc.), `/collections/all-desks` (smart), `/pages/brands-global-teknion`, `/collections/business-furniture` (breadcrumb), `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, Industries Hub Browse, education/government/pro-services crosslinks |
| Verified | ⬜ |

### `/collections/storage` — Storage & Filing (P2-4)

| | |
|---|---|
| Outbound (must exist) | 14 sub-collections, `/collections/all-storage` (smart), breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, healthcare/education/government/non-profit crosslinks |
| Verified | ⬜ |

### `/collections/tables` — Tables (P2-5)

| | |
|---|---|
| Outbound (must exist) | 10 sub-collections, `/collections/all-tables` (smart), breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, healthcare crosslinks |
| Verified | ⬜ |

### `/collections/boardroom` — Boardroom (P2-6)

| | |
|---|---|
| Outbound (must exist) | 3 sub-collections (boardroom-conference-meeting, lecterns-podiums, audio-visual-equipment), `/collections/all-boardroom` (smart), `/pages/brands-keilhauer`, `/pages/design-services`, breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, government/pro-services crosslinks |
| Verified | ⬜ |

### `/collections/ergonomic-products` — Ergonomic (P2-7)

| | |
|---|---|
| Outbound (must exist) | 4 sub-collections, `/collections/all-ergonomic` (smart), `/pages/brands-ergocentric`, breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, pro-services crosslinks |
| Verified | ⬜ |

### `/collections/panels-room-dividers` — Panels & Dividers (P2-8)

| | |
|---|---|
| Outbound (must exist) | 3 sub-collections, `/collections/all-panels` (smart), `/collections/quiet-spaces` (cross-link), breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, education/government crosslinks |
| Verified | ⬜ |

### `/collections/accessories` — Accessories (P2-9)

| | |
|---|---|
| Outbound (must exist) | 4 sub-collections, `/collections/all-accessories` (smart), breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical |
| Verified | ⬜ |

### `/collections/quiet-spaces` — Quiet Spaces (P2-10)

| | |
|---|---|
| Outbound (must exist) | 5 sub-collections (telephone-booths, walls, sound-dampeners, av-stand, planters), `/collections/all-quiet-spaces` (smart), breadcrumb, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Business Furniture vertical, homepage shop grid, panels & dividers cross-link |
| Verified | ⬜ |

---

## Page interlinking matrix — Phase 4 (trust pages, to build)

### `/pages/brands` — Brands Hub (P4-1)

| | |
|---|---|
| Outbound (must exist) | `/pages/brands-keilhauer`, `/pages/brands-global-teknion`, `/pages/brands-ergocentric`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Nav "Brands" item, homepage (consider adding a brands strip), every brand-relevant category page |
| Verified | ⬜ |

### `/pages/brands-keilhauer` (P4-2)

| | |
|---|---|
| Outbound (must exist) | `/collections/boardroom`, `/collections/seating`, `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Brands Hub, Boardroom category callout, pro-services page |
| Verified | ⬜ |

### `/pages/brands-global-teknion` (P4-3)

| | |
|---|---|
| Outbound (must exist) | `/collections/desks`, `/collections/panels-room-dividers`, `/collections/boardroom`, `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Brands Hub, Desks category callout, government page |
| Verified | ⬜ |

### `/pages/brands-ergocentric` (P4-4)

| | |
|---|---|
| Outbound (must exist) | `/collections/seating`, `/collections/ergonomic-products`, `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Brands Hub, Seating + Ergonomic category callouts, pro-services page |
| Verified | ⬜ — confirm against PB-13 reconciliation outcome |

### `/pages/about` (P4-5)

| | |
|---|---|
| Outbound (must exist) | `/pages/our-work`, `/pages/contact`, `/pages/oecm`, `/pages/quote`, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Nav "About" dropdown, footer, homepage |
| Verified | ⬜ |

### `/pages/our-work` (P4-6)

| | |
|---|---|
| Outbound (must exist) | Each case study links to relevant collection or industry page; `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | About page, homepage testimonial section, Industries pages, Brands pages |
| Verified | ⬜ |

### `/pages/contact` (P4-7)

| | |
|---|---|
| Outbound (must exist) | `/pages/quote`, `/pages/design-services`, `tel:18008359565`, mailto:sales@brantbusinessinteriors.com, breadcrumb, nav, footer industries (×5) |
| Inbound (should exist) | Footer (every page), nav About dropdown, every product page sticky "Questions?" link |
| Verified | ⬜ |

### `/pages/delivery` — Delivery & Installation (P4-8)

| | |
|---|---|
| Outbound (must exist) | `/pages/relocation`, `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Every PDP delivery trust block, Services nav dropdown, FAQ delivery answer |
| Verified | ⬜ |

### `/pages/relocation` — Relocation Management (P4-9)

| | |
|---|---|
| Outbound (must exist) | `/pages/delivery`, `/pages/contact`, `/pages/quote`, breadcrumb, nav, footer industries (×5), `tel:18008359565` |
| Inbound (should exist) | Delivery page, Services nav dropdown, About page |
| Verified | ⬜ |

---

## Slug existence audit (collections referenced in maps above)

Every slug below must exist as a Shopify collection and return 200. Audit before P2-* rows can be marked done.

| Slug | Used by | Exists? | Notes |
|---|---|---|---|
| `/collections/business-furniture` | Homepage, all P2 pages, all industry pages | ⬜ verify | Vertical entry point |
| `/collections/seating` | Healthcare, Non-Profit, Pro-Services, P2-2, P4-2, P4-4 | ⬜ verify | |
| `/collections/desks` | Healthcare, Education, Government, Pro-Services, P2-3, P4-3 | ⬜ verify | |
| `/collections/storage` | Healthcare, Education, Government, Non-Profit, P2-4 | ⬜ verify | |
| `/collections/tables` | Healthcare (post-fix), Non-Profit, P2-5 | ⬜ verify | |
| `/collections/boardroom` | Government, Pro-Services, P2-6, P4-2, P4-3 | ⬜ verify | |
| `/collections/ergonomic-products` | Pro-Services, P2-7, P4-4 | ⬜ verify | |
| `/collections/panels-room-dividers` | Education, Government, P2-8, P4-3 | ⬜ verify | |
| `/collections/accessories` | P2-9 | ⬜ verify | |
| `/collections/quiet-spaces` | P2-10, P2-8 cross-link | ⬜ verify | |
| `/collections/training-flip-top-tables` | Education | ⬜ verify | |
| `/collections/stacking-seating` | Education | ⬜ verify | |
| All ~68 sub-collections | P3 rollout, sub-pages of each P2 page | ⬜ verify | PB-11 audit |

---

## Inbound-coverage gap analysis (snapshot)

Quick scan of inbound coverage gaps based on current matrix:

- **Brands pages have weak inbound** — no inbound from category pages until brand callouts get added in NAV-3 / Wave A. Currently only Brands Hub links to them.
- **Quiet Spaces / Panels & Dividers** — no industry page cross-links to either; only Business Furniture vertical and homepage. Consider adding to Healthcare ("waiting room privacy") and Pro-Services ("private offices").
- **Our Work portfolio** — single inbound from Homepage testimonial. Add to About page narrative + every industry page ("see [vertical] case studies").
- **Contact** — no current page has prominent Contact link; lives only in nav About dropdown and footer. Consider a "Talk to a real person" closer on every page.

These aren't bugs — they're optimization candidates for INTERLINK-2 / INTERLINK-3 in Wave E.

---

## Update protocol

When you ship a new page or change an existing one:

1. Add or update the page's row above with current outbound/inbound.
2. For every page that should link **to** this one, update its inbound column.
3. Update the slug existence audit if new collection slugs are referenced.
4. Run `/scripts/audit-interlinks.py` (when built) — expect green.
5. Mark the corresponding row in `bbi-build-state.md` ✅ with the audit timestamp.

When the audit script (INTERLINK-1) is built, it should:

- Parse this file → list of (page, expected_outbound[], expected_inbound[])
- Crawl dev preview → fetch every page → extract all `<a href>`
- For each page: confirm every `expected_outbound` href is present + returns 200
- For each page: confirm every `expected_inbound` source page actually links to this page
- Output: `data/reports/interlink-audit-<date>.md` with per-row pass/fail + drift summary
