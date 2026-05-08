# Stage 5 Launch Audit — 4.7 RFQ Modal Design System
**Date:** 2026-05-08
**Sources:** `theme/snippets/bbi-nav.liquid`, `docs/plan/bbi-build-state.md` (LEAD-3), `docs/plan/bbi-lead-routing.md`
**Auditor:** Claude Code (read-only pass)

---

## Current state

There is **no standalone RFQ modal** implemented. The current lead-capture pattern is:

1. **"Request a Quote" button** in the nav header → navigates directly to `/pages/quote` (full page)
2. **"Request a Quote" link** in the About dropdown → same destination
3. **Mobile nav quote button** → same destination
4. **Phase 1 CTAs across ds-lp-* sections** → hard link to `/pages/quote`

The nav does contain a mobile drawer using `role="dialog"` and `aria-modal="true"` (the hamburger menu overlay — `<bbi-nav-mobile>` Web Component built in NAV-2). This is the mobile nav, not an RFQ modal.

No `bbi-lead-form.liquid` snippet exists. No `<dialog>` element for inline quote collection exists anywhere in the theme snippets.

---

## What LEAD-3 specifies (from `bbi-build-state.md`)

> Modal pattern (Web Component + `<dialog>` + focus trap, mirrors NAV-2's `bbi-nav-mobile`). On submit: in-modal success screen with secondary CTA. Auto-reply per type. Three inboxes: `quotes@`, `design@`, `info@brantbusinessinteriors.com`. Lead-type → inbox: quote→quotes, design→design, contact→info, oecm→quotes.

LEAD-3 is **Wave E** (pre-launch hardening). It has not started. Pre-req: `LEAD-INBOX-1` (provision email inboxes — Steve action, not done).

---

## Design system specification for modals (from `docs/strategy/design-system.md`)

The design system defines a Web Component modal pattern:
- `<dialog>` element with BBI design tokens applied
- Focus trap (mirrors `bbi-nav-mobile` pattern)
- Escape-to-close
- In-modal success screen, not a redirect
- Secondary CTA after submission

---

## Gap analysis: current vs DS modal spec

| Requirement | Current state | Gap |
|---|---|---|
| `<dialog>` + Web Component | Not built | Full build (LEAD-3) |
| Focus trap | Not applicable (no modal) | LEAD-3 |
| BBI design tokens on modal frame | Not applicable | LEAD-3 |
| Per-type routing (quote/design/contact) | Not built | LEAD-3 |
| In-modal success screen | Not built | LEAD-3 |
| Auto-reply email | Not built | LEAD-3 |
| WCAG compliance | Not applicable | LEAD-3 |

---

## Current workaround assessment

The `/pages/quote` page (ds-lp-quote.liquid) provides a functional quote request page. For launch purposes, the direct-navigation pattern is acceptable as a functional MVP — users can still submit RFQ requests. The modal is an enhancement that improves conversion rate and reduces bounce but is not a hard launch blocker for the quote flow itself.

**However:** The `main-product.liquid` PDP (Starlite) surfaces a `query_form` block that can be added optionally but is not auto-wired to the unbuyable state. This means sold-out products currently show Add-to-Cart with no fallback CTA. This IS a BLOCK issue — covered in audit 4.6.

---

## Severity assessment

| Item | Severity | Notes |
|---|---|---|
| RFQ modal (LEAD-3) | FIX (not BLOCK) | `/pages/quote` works as fallback; modal is conversion improvement |
| LEAD-INBOX-1 (inbox provisioning) | BLOCK | Hard prereq for LEAD-3; Steve must provision `quotes@`, `design@`, `info@` and verify SPF/DKIM |
| Sold-out PDP has no quote CTA | BLOCK | Covered in audit 4.6 (PDP build required) |

---

## Pre-LEAD-3 checklist

- [ ] Steve provisions `quotes@brantbusinessinteriors.com`
- [ ] Steve provisions `design@brantbusinessinteriors.com`
- [ ] Steve provisions `info@brantbusinessinteriors.com`
- [ ] SPF/DKIM/DMARC verified on outbound
- [ ] Test receipt confirmed from external domain
- [ ] Mark LEAD-INBOX-1 ✅ in `bbi-build-state.md`
- [ ] Then LEAD-3 can start (build `bbi-lead-form.liquid` snippet)
