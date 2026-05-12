# BBI — Current Status
**Last updated:** 2026-05-11

---

## 🔴 Currently blocked — product page black background

**Symptom:** Every product page on the dev theme renders a black background.

**Root cause confirmed:** The dev theme's active colour scheme is dark (`#0B0B0C` body). Load order:

| Order | Source | Effect |
|---|---|---|
| 1st | `style-variables.liquid` | Sets `body { background: rgb(11,11,12) }` — black |
| 2nd | `bbi-homepage.css` | Reinforces dark background |
| 3rd | `ds-pdp-base.liquid` section `<style>` | `!important` override — does NOT win |

**Already tried and failed:**
- `body { background: #FFFFFF !important }` in `ds-pdp-base.liquid` section `<style>`
- `min-height: 100vh` on `.bbi-pdp`

**Fix:** Prompt 0 in `03-prompts-ready.md`. Patch `config/settings_data.json` via API to switch colour scheme to light, OR inject override in `theme/layout/theme.liquid` before any stylesheet loads.

**Also deployed but unverifiable until fixed:**
- Add to Cart promoted to first/dominant button; Buy Now demoted to slim outline
- Quote card compressed to one-line strip (outline button + phone, no heading/eyebrow)

---

## Critical rules

| Rule | Detail |
|---|---|
| **Dev theme only** | All pushes go to `186373570873`. Never touch `178274435385` (live). |
| **Push command** | `export $(grep -v '^#' .env | xargs) && BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873` |
| **Layout flag** | Add `--layout` when touching `theme/layout/theme.liquid` |
| **Snippets flag** | Add `--snippets` when touching `theme/snippets/bbi-*.liquid` |
| **Never bare push** | Never `shopify theme push` without `--theme 186373570873` |

---

## What was completed this session (2026-05-11)

### PDP design system — all 14 gaps closed
- Fix Group 1 — Right column: eyebrow CSS `::before` red rule, commerce card alternate background, sticky right column, standfirst metafield slot, sold-out gray pill badge
- Fix Group 2 — Below-fold typography: tagline H2, body 17px/1.6, 640px max-width, Best For semantic rebuild
- Fix Group 3 — Spec table: HTML `<table>` → CSS grid divs, dark top border, `<hr>` removed, dash bullets
- Fix Group 4 — Layout: 1320px container, 60/40 hero grid, 4:5 gallery, 6-col thumb strip

### PDP UX improvements (deployed, pending visual verification due to black page)
- Price moved above variant chips, below availability badge
- `.pdp-about` section stretched to full 1320px container width
- Quote modal pre-fills product name when opened from a product page
- Add to Cart promoted to first/dominant; Buy Now demoted to outline
- Quote card compressed to compact one-line strip

### Bug fixes
- Liquid "translation missing" — `compare-products-content` gated in `theme/layout/theme.liquid`
- Liquid "Could not find snippets/theme-variables" — stub created
- Collection "Shop All" + "All" filter now show flat product grid

---

## All waves complete

| Wave | What |
|---|---|
| Track D | Design system tokens + components ✅ |
| Phase 1 | All 10 landing pages (OECM, Healthcare, Education, etc.) ✅ |
| Wave A | Foundations, nav, footer, Phase 2 collection categories ✅ |
| Wave B | Smart collections + sub-collection product listings ✅ |
| Wave C | Trust pages (Brands, About, Contact, Delivery, Relocation, Our Work) ✅ |
| Wave G-Fixes | Visual review bug fixes, quote modal, PDP restructure, brand plates ✅ |
| Wave G | PDP template, 404 page, blog templates, Customer Stories, smart collections ✅ |
| Phase 1b | Hero 100 descriptions, spec metafields, SEO meta, normalized titles ✅ |

---

## Prompts remaining — run in this order

Full prompts are in `03-prompts-ready.md`.

| # | Prompt | Priority |
|---|---|---|
| **0** | **Fix black product page** | 🔴 First — blocking all PDP QA |
| 1 | Cart 404 fix | 🔴 Second — blocking purchases |
| 2 | Buy Now + Quantity selector | 🟠 Third — needs cart working first |
| 3 | Other products like this (3-tier fallback) | 🟡 Any time after #1 |
| 4 | Product descriptions + specs overhaul | 🟡 Any time — no theme files |
| 5 | Hero + sub-hero photo audit | 🟢 Any time — read only |
| 6 | Empty subcollections audit | 🟢 Any time — read only |

---

## Wave E remaining — Claude Code tasks (after prompts above)

| ID | Task |
|---|---|
| AI-4 | Organization schema on homepage + About |
| AI-6 | BreadcrumbList JSON-LD shared snippet |
| AI-7 | Entity-clarity copy on homepage |
| AI-8 | OECM page copy hardening |
| AI-9 | FAQ blocks + FAQPage schema on all 9 category pages |
| AI-5 | FAQ schema on OECM + Design Services |
| LEAD-2 | Lead routing gap analysis |
| LEAD-3 | Quote form routing — **blocked on Steve (LEAD-INBOX-1)** |
| INTERLINK-3 | Final cross-link audit |
| SEO-AUDIT-1 | 🔴 DataForSEO technical audit — **hard gate before launch** |
| NAV-VERIFY | Confirm shared nav renders correctly |
| DS-VERIFY | Design system pre-launch screenshot diff |
| IMG-PHASE2 | Product image regen ≥80% coverage |
| PERF-AUDIT-1 | Lighthouse + Core Web Vitals on top 10 pages |
| A11Y-AUDIT-1 | WCAG 2.1 AA audit on top 10 pages |
| LINK-ROT-1 | Internal + external link sweep |
| SYS-VERIFY-1 | Cart, search, account, password pages chrome check |
| W0-7 | OECM + "Since 1964" trust signals site-wide |
| CONTENT-1 | 🔔 Finalize BBI logo — **needs Leo's decision** |

---

## Decisions only Leo or Steve can make

| Who | What | Blocks |
|---|---|---|
| **Steve** | Provision `quotes@`, `design@`, `info@brantbusinessinteriors.com` + verify SPF/DKIM/DMARC | LEAD-3 quote routing |
| **Leo** | Lock `bbi-logo-v2` as BBI logo OR source a real wordmark | CONTENT-1 |
| **Leo** | Review and approve product image CSV row by row | LAUNCH-0 |
| **Leo** | Click Publish in Shopify Admin | LAUNCH-2 |

---

## Leo's manual tasks (no Claude needed)

| Task |
|---|
| Set up Google Search Console + GA4 (W0-1) |
| Create BBI Google Business Profile (W0-2) |
| Upload product redirects CSV in Shopify Admin — `data/url-redirects.csv` exists (W0-3) |
| Coordinate backlinks from officecentral.com + brantbasics.com (W0-6) |

---

## Critical path to launch

```
🔴 Fix black product page (Prompt 0)
  → Cart 404 fix (Prompt 1)
    → Buy Now + Quantity (Prompt 2)
      → Remaining prompts 3–6 (parallel OK)
        → Wave E hardening
          → Steve provisions inboxes (LEAD-INBOX-1)
            → LEAD-3 routing closes
              → SEO-AUDIT-1 passes (hard gate)
                → Leo approves image CSV (LAUNCH-0)
                  → GO/NO-GO report
                    → Leo clicks Publish
```

---

## Dev theme review links (black until Prompt 0 is run)

| Page | URL |
|---|---|
| In-stock PDP | `https://office-central-online.myshopify.com/products/alphabetter-stand-up-desk?preview_theme_id=186373570873` |
| Filing cabinet PDP | `https://office-central-online.myshopify.com/products/vertical-file-2-drawer-letter?preview_theme_id=186373570873` |
| $0 showcase PDP | `https://office-central-online.myshopify.com/products/additional-services-dismantle-re-assemble?preview_theme_id=186373570873` |
| Homepage | `https://office-central-online.myshopify.com/?preview_theme_id=186373570873` |
| Business Furniture | `https://office-central-online.myshopify.com/collections/business-furniture?preview_theme_id=186373570873` |
| Healthcare | `https://office-central-online.myshopify.com/pages/healthcare?preview_theme_id=186373570873` |
| OECM | `https://office-central-online.myshopify.com/pages/oecm?preview_theme_id=186373570873` |
