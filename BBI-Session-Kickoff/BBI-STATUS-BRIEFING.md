# BBI — Status Briefing
**Last updated:** 2026-05-11 | **Use this to get up to speed after switching Claude accounts.**

---

## Critical rules — read first

| Rule | Detail |
|---|---|
| **Dev theme only** | All pushes go to `186373570873` (BBI Landing Dev). Never touch `178274435385` (live). |
| **Push command** | `export $(grep -v '^#' .env | xargs) && BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873` |
| **Layout flag** | Add `--layout` whenever touching `theme/layout/theme.liquid` |
| **Snippets flag** | Add `--snippets` whenever touching `theme/snippets/bbi-*.liquid` |
| **Never bare push** | Never run `shopify theme push` without `--theme 186373570873` — it may default to live |
| **Dry run first** | All `push-*` scripts default to dry run. Always confirm output before `--live` |

---

## 🔴 Currently blocked — product page black background

**Symptom:** Every product page on the dev theme renders a black background.

**Root cause confirmed by audit:** The dev theme's active colour scheme is dark (`#0B0B0C` body background). The load order is:

| Order | Source | Rule | Result |
|---|---|---|---|
| 1st | `style-variables.liquid` (inline) | `body { background-color: rgb(11,11,12) }` | Black |
| 2nd | `bbi-homepage.css` (global) | `body { background: var(--background) }` | Black |
| 3rd | `ds-pdp-base.liquid` (section) | `body { background: #FFFFFF !important }` | Still black |

**What was already tried and failed:**
- Added `body { background: #FFFFFF !important }` to the section `<style>` block in `ds-pdp-base.liquid`
- Added `min-height: 100vh` to `.bbi-pdp`
- Neither worked — section-level CSS is losing to the global dark scheme

**Fix needed (Prompt 0 in prompts file):** Patch `config/settings_data.json` on the dev theme via API to switch the active colour scheme to light, OR inject the override in `theme/layout/theme.liquid` before any other stylesheet loads.

**Also deployed but unverifiable until fixed:**
- Button hierarchy: Add to Cart is now first (dominant primary), Buy Now demoted to slim outline
- Quote card compressed to a single-line strip (outline button + phone, no heading/eyebrow)

---

## What was recently completed (this session — 2026-05-11)

### PDP design system — all 14 gaps closed
- Fix Group 1 — Right column: eyebrow CSS `::before` red rule, commerce card alternate background, sticky right column, standfirst metafield slot, sold-out gray pill badge
- Fix Group 2 — Below-fold typography: tagline H2, body 17px/1.6, 640px max-width, Best For semantic rebuild
- Fix Group 3 — Spec table: HTML `<table>` → CSS grid divs, dark top border, `<hr>` removed, dash bullets
- Fix Group 4 — Layout: 1320px container, 60/40 hero grid, 4:5 gallery, 6-col thumb strip

### PDP UX improvements (deployed, pending visual verification)
- Price moved above variant chips, below availability badge
- "Ordering 5 or more?" label added above quote card CTA
- `.pdp-about` section stretched to full 1320px container width
- Quote modal pre-fills product name when opened from a product page
- Add to Cart promoted to first/dominant button; Buy Now demoted to outline
- Quote card compressed to compact one-line strip

### Bug fixes
- Liquid error "translation missing" — `compare-products-content` gated in `theme/layout/theme.liquid`
- Liquid error "Could not find snippets/theme-variables" — stub created
- Collection "Shop All" + "All" filter now show flat product grid

---

## Waves complete (reference)

| Wave | What | Status |
|---|---|---|
| Track D | Design system tokens + components | ✅ |
| Phase 1 | All 10 landing pages | ✅ |
| Wave A | Foundations, nav, footer, Phase 2 collection categories | ✅ |
| Wave B | Smart collections + sub-collection product listings | ✅ |
| Wave C | Trust pages (Brands, About, Contact, Delivery, Relocation, Our Work) | ✅ |
| Wave G-Fixes | Visual review bug fixes, quote modal, PDP restructure, brand plates | ✅ |
| Wave G | PDP template, 404 page, blog templates, Customer Stories, smart collections | ✅ |
| Phase 1b | Hero 100 descriptions, spec metafields, SEO meta, normalized titles | ✅ |

---

## Prompts ready to run — in this exact order

All prompts are in `BBI-PROMPTS-READY.md` on this desktop.

| # | Prompt | Priority | Can parallel? |
|---|---|---|---|
| **0** | **🔴 Fix black product page background** | **First — blocking all PDP QA** | No |
| 1 | Cart 404 fix | 🔴 Second — blocking purchases | No |
| 2 | Buy Now + Quantity selector | 🟠 Third — needs cart working | No |
| 3 | Other products like this (3-tier fallback) | 🟡 Any time after #1 | Yes |
| 4 | Product descriptions + specs overhaul | 🟡 Any time | Yes — no theme files |
| 5 | Hero + sub-hero photo audit | 🟢 Any time | Yes — read only |
| 6 | Empty subcollections audit | 🟢 Any time | Yes — read only |

---

## Wave E remaining — Claude Code can do these

All ⬜ (not started). Run after the prompts above are done.

| ID | Task |
|---|---|
| AI-4 | Organization schema on homepage + About page |
| AI-6 | BreadcrumbList JSON-LD shared snippet |
| AI-7 | Entity-clarity copy on homepage |
| AI-8 | OECM page copy hardening |
| AI-9 | FAQ blocks + FAQPage schema on all 9 category pages |
| AI-5 | FAQ schema on OECM + Design Services |
| LEAD-2 | Lead routing gap analysis |
| LEAD-3 | Wire quote form routing (**blocked on Steve — LEAD-INBOX-1**) |
| INTERLINK-3 | Final cross-link audit |
| SEO-AUDIT-1 | 🔴 DataForSEO technical audit — **hard gate before launch** |
| NAV-VERIFY | Confirm homepage + collection pages render shared nav |
| DS-VERIFY | Design system pre-launch screenshot diff |
| IMG-PHASE2 | Product image regen to ≥80% coverage |
| PERF-AUDIT-1 | Lighthouse + Core Web Vitals on top 10 pages |
| A11Y-AUDIT-1 | WCAG 2.1 AA audit on top 10 pages |
| LINK-ROT-1 | Internal + external link 200/404 sweep |
| SYS-VERIFY-1 | Cart, search, account, password pages chrome check |
| W0-7 | OECM + "Since 1964" trust signals site-wide |
| CONTENT-1 | 🔔 Finalize BBI logo — **needs your decision** |

---

## Decisions only you or Steve can make

| Who | What | Blocks |
|---|---|---|
| **Steve** | `LEAD-INBOX-1` — provision `quotes@`, `design@`, `info@brantbusinessinteriors.com`, verify SPF/DKIM/DMARC | Quote form routing (LEAD-3) |
| **You** | `CONTENT-1` — lock `bbi-logo-v2` as BBI logo OR source a real BBI wordmark | Final design sign-off |
| **You** | `LAUNCH-0` — review and approve the product image CSV row by row | GO/NO-GO report |
| **You** | `LAUNCH-2` — click Publish in Shopify Admin | Launch |

---

## Your manual tasks (Wave D — parallel, no Claude needed)

| ID | Task |
|---|---|
| W0-1 | Set up Google Search Console + GA4 |
| W0-2 | Create BBI Google Business Profile |
| W0-2b | Google Reviews seeding strategy |
| W0-3 | Upload product redirects CSV in Shopify Admin (`data/url-redirects.csv` exists) |
| W0-6 | Coordinate backlinks from officecentral.com + brantbasics.com |

---

## Critical path to launch

```
🔴 Fix black product page (Prompt 0)
  → Cart 404 fix (Prompt 1)
    → Buy Now + Quantity (Prompt 2)
      → Remaining prompts (3–6, parallel OK)
        → Wave E hardening (AI-4..AI-9, audits)
          → Steve provisions email inboxes (LEAD-INBOX-1)
            → LEAD-3 quote routing closes
              → SEO-AUDIT-1 passes (hard gate)
                → LAUNCH-0 image review (you)
                  → GO/NO-GO → You click Publish
```

---

## Key files

| Need | File |
|---|---|
| Build state (single source of truth) | `docs/plan/bbi-build-state.md` |
| Interlinking matrix | `docs/plan/bbi-interlinking-map.md` |
| Brand voice + ICP | `docs/strategy/icp.md` |
| Design system | `docs/strategy/design-system.md` |
| Lead routing plan | `docs/plan/bbi-lead-routing.md` |
| All prompts ready to run | `BBI-PROMPTS-READY.md` (this folder) |
| Dev theme settings backup | `data/backups/settings_data-backup-pre-lightmode.json` (after Prompt 0 runs) |

---

## Dev theme review links (currently render black — fix Prompt 0 first)

| Page | URL |
|---|---|
| In-stock PDP | `https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873` |
| Filing cabinet PDP | `https://office-central-online.myshopify.com/products/vertical-file-2-drawer-letter?preview_theme_id=186373570873` |
| $0 showcase PDP | `https://office-central-online.myshopify.com/products/additional-services-dismantle-re-assemble?preview_theme_id=186373570873` |
| Homepage | `https://office-central-online.myshopify.com/?preview_theme_id=186373570873` |
| Business Furniture | `https://office-central-online.myshopify.com/collections/business-furniture?preview_theme_id=186373570873` |
| Healthcare | `https://office-central-online.myshopify.com/pages/healthcare?preview_theme_id=186373570873` |
| OECM | `https://office-central-online.myshopify.com/pages/oecm?preview_theme_id=186373570873` |
