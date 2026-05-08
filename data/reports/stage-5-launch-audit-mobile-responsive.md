# Stage 5 Launch Audit — 4.10 Mobile Responsive
**Date:** 2026-05-08
**Auditor:** Claude Code (read-only pass)

---

## Overview

Mobile responsiveness verification requires live screenshots using `scripts/capture-bbi-baselines.py` (Phase 3 tooling). This audit documents the scope, test targets, and known risks at 375px. Actual screenshots cannot be taken until `shopify theme dev` is running.

---

## 5 pages to test at 375px (iPhone SE viewport)

| Page | URL | Template | Priority | Known risks |
|---|---|---|---|---|
| Homepage | `/` | `index.json` | P0 | Hero image cropping; "Shop by Industry" section tile wrapping |
| Seating hub | `/collections/seating` | `collection.seating.json` → `ds-cc-base.liquid` | P0 | Brand plate overflow; tile grid wraps to 1-column or 2-column correctly? |
| Highback Seating sub-collection | `/collections/highback-seating` | `collection.base.json` → `ds-cs-base.liquid` | P0 | Product card image cropping; filter sidebar must collapse; pagination |
| Healthcare industry page | `/pages/healthcare` | `page.healthcare.json` → `ds-lp-healthcare.liquid` | P1 | Hero image resize; crosslink tile overflow; footer 4-column → single column |
| Quote page | `/pages/quote` | `page.quote.json` → `ds-lp-quote.liquid` | P1 | Form layout; input focus behaviour; submit button full-width |

---

## What to check at 375px per page

### All pages
- [ ] Single `<bbi-header>` visible, no Starlite double-header
- [ ] Hamburger menu icon visible and tappable (44px min touch target)
- [ ] Mobile nav opens: full-screen overlay, correct 5-item structure
- [ ] Logo visible in header
- [ ] Footer collapses to single column (not 4-column)
- [ ] Phone CTA is tappable (`tel:` link works on mobile)
- [ ] No horizontal scroll at 375px
- [ ] Text is readable (≥16px body, no sub-12px text)

### Homepage additional
- [ ] Hero CTA button is full-width on mobile
- [ ] Product grid wraps to 2-column (not 4-column)
- [ ] Industry tiles wrap gracefully

### Category hub (Seating)
- [ ] Sub-collection tile grid wraps to 2-column or 1-column
- [ ] Brand plates don't overflow container
- [ ] "View all" CTA reachable

### Sub-collection (Highback Seating)
- [ ] Product cards: 2-column at 375px
- [ ] Product images fill card correctly (no cropping to white/empty)
- [ ] Filter sidebar collapses to a toggle button (not displayed as left rail)
- [ ] "Request a Quote" pill on sold-out products renders correctly

### Industry page (Healthcare)
- [ ] Hero image crops to center on mobile
- [ ] Crosslink tiles wrap to 1-column
- [ ] OECM bar readable

### Quote page
- [ ] Form inputs are full-width
- [ ] Labels visible above inputs
- [ ] Submit button full-width

---

## Known pre-existing mobile issues (from remediation plan)

Per `design-system-remediation-2026-05-07.md` Stage D:
- Product image tiles had cropping issues (zoomed in too far on chairs) — root cause identified as `image_url` filter parameters too narrow. Stage 3.2a.5 addressed this in `ds-cs-base.liquid`. Verify fix holds at 375px.
- Category hubs had header inconsistency — Stage 3.1b/NAV-3 refactor should have resolved this. Verify at 375px.

---

## How to run

1. Start dev theme: `shopify theme dev --store=office-central-online`
2. Note the preview URL (typically `http://127.0.0.1:9292`)
3. Run: `python3 scripts/capture-bbi-baselines.py`
   - Captures all 14 URLs × 3 viewports (375px, 768px, 1280px) = 42 screenshots
4. Inspect `data/baselines/current/` PNG files for the 5 priority pages at 375px
5. Flag any layout breaks in this document

---

## Additional test devices recommended (manual)

Per CLAUDE.md testing requirements:
- Chrome Android (real device or DevTools emulation)
- Safari iOS (real device — viewport handling differs from Chrome)
- Firefox mobile

---

## Status

⬜ Not tested — requires `shopify theme dev` running. Run capture-bbi-baselines.py during Phase 3 of the launch plan.
