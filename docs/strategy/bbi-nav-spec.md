# BBI Nav Spec — Canonical Navigation v1.0

**Decision locked:** 2026-05-06  
**Source:** NAV-1 acceptance (Wave A row 4) + `docs/plan/site-architecture-2026-04-25.md §1`  
**Status:** ✅ Locked — do not change without a new NAV decision row

---

## 1. Top-bar layout

```
[Brant Business Interiors logo]
  Shop Furniture ▾  |  Industries ▾  |  Brands ▾  |  Services ▾  |  About ▾
                                              [1-800-835-9565]  [Request Quote →]
```

5 top-level nav items. Phone number and Quote CTA are right-aligned in the same bar, visually separated from the nav links.

| Element | Type | Notes |
|---|---|---|
| Logo | Link → `/` | Use `bbi-logo-v2` asset until CONTENT-1 resolves |
| Shop Furniture | Click → `/collections/business-furniture`, Hover → dropdown | Only item that navigates on click |
| Industries | Hover/click → dropdown | No standalone page — dropdown only |
| Brands | Hover/click → dropdown | No standalone page — dropdown only |
| Services | Hover/click → dropdown | No standalone page — dropdown only |
| About | Hover/click → dropdown | No standalone page — dropdown only |
| Phone | `tel:18008359565` | Plain text link, not a button |
| Request Quote | Button → `/pages/quote` | Primary CTA, brand-red background |

---

## 2. Dropdown contents

### Shop Furniture → `/collections/business-furniture`

Single-column dropdown. Header text "Business Furniture" links to `/collections/business-furniture`.

| Label | URL |
|---|---|
| Seating | `/collections/seating` |
| Desks & Workstations | `/collections/desks` |
| Storage & Filing | `/collections/storage` |
| Tables | `/collections/tables` |
| Boardroom | `/collections/boardroom` |
| Ergonomic Products | `/collections/ergonomic-products` |
| Panels & Dividers | `/collections/panels-room-dividers` |
| Accessories | `/collections/accessories` |
| Quiet Spaces | `/collections/quiet-spaces` |

### Industries

| Label | URL |
|---|---|
| Industries Hub | `/pages/industries` |
| Healthcare | `/pages/healthcare` |
| Education | `/pages/education` |
| Government | `/pages/government` |
| Non-Profit | `/pages/non-profit` |
| Professional Services | `/pages/professional-services` |

### Brands

| Label | URL | Notes |
|---|---|---|
| Brands Hub | `/pages/brands` | |
| Keilhauer | `/pages/brands-keilhauer` | |
| Global / Teknion | `/pages/brands-global-teknion` | |
| ergoCentric | `/pages/brands-ergocentric` | |
| *(trust line)* | — | "Authorized Canadian Dealer" — non-linked italicized sub-line at bottom of dropdown |

### Services

| Label | URL |
|---|---|
| Design Services | `/pages/design-services` |
| Delivery & Installation | `/pages/delivery` |
| Relocation Management | `/pages/relocation` |
| Request a Quote | `/pages/quote` |
| FAQ | `/pages/faq` |

### About

| Label | URL |
|---|---|
| About Us | `/pages/about` |
| Our Work | `/pages/our-work` |
| OECM Procurement | `/pages/oecm` |
| Contact | `/pages/contact` |

---

## 3. Active state rules

The nav item is highlighted (border-bottom in brand-red, or bold weight) when the current page matches:

| Active item | Triggered by |
|---|---|
| **Shop Furniture** | Any `/collections/*` page |
| **Industries** | `/pages/industries`, `/pages/healthcare`, `/pages/education`, `/pages/government`, `/pages/non-profit`, `/pages/professional-services` |
| **Brands** | `/pages/brands`, `/pages/brands-keilhauer`, `/pages/brands-global-teknion`, `/pages/brands-ergocentric` |
| **Services** | `/pages/design-services`, `/pages/delivery`, `/pages/relocation`, `/pages/quote`, `/pages/faq` |
| **About** | `/pages/about`, `/pages/our-work`, `/pages/oecm`, `/pages/contact` |
| *(none)* | Homepage `/` — no item active |

In `bbi-nav.liquid` the active item is passed via render context: `{% render 'bbi-nav', active: 'industries' %}`. The snippet compares the `active` parameter against these keys.

---

## 4. Mobile nav

**Pattern: hamburger → full-screen overlay with vertical accordion.**

- Hamburger icon (top-right, 44×44 px tap target) opens a full-screen overlay (z-index above all content).
- Overlay shows 5 accordion items matching the desktop top-level labels.
- Each accordion item expands to show the same links as the desktop dropdown.
- "Authorized Canadian Dealer" trust line appears under Brands, same as desktop.
- Phone number and Request Quote CTA appear at the bottom of the overlay, always visible (sticky footer inside overlay).
- Close button (×) top-right of overlay. Escape key also closes.
- Active item is highlighted using the same `active` parameter as desktop.

Rationale: accordion is the standard Shopify Dawn pattern, keeps parity with desktop structure, and avoids a separate bottom-sheet component that would require extra JS.

---

## 5. Phone CTA placement

Phone number (`1-800-835-9565`) sits **inside the nav bar**, right-aligned between the 5 nav items and the Quote CTA button. It is always visible on desktop — not hidden in a dropdown or a separate announcement bar.

On mobile it moves to the sticky footer of the hamburger overlay.

---

## 6. Implementation notes (for NAV-2)

- Build `theme/snippets/bbi-nav.liquid` as the single source. All 10 `ds-lp-*` sections + homepage render it via `{% render 'bbi-nav', active: '<key>' %}`.
- Deploy via `BBI_PUSH_ROOT=$(pwd) python scripts/bbi-push-landing.py --snippets` (PB-12's `--snippets` flag).
- CSS tokens: background `--color-nav-bg` (white), active indicator `--color-brand-red` (`#D4252A`), CTA button uses `--color-brand-red`.
- Dropdown open/close via CSS `:hover` + a JS fallback for touch devices (no hover). Use `CustomEvent` to broadcast open/close state for accessibility.
- Focus trap inside mobile overlay. Escape closes. WCAG 2.1 AA required.

---

## 7. Follow-ups (non-blocking)

- **Click-behavior consistency.** Currently Shop Furniture click → navigates to `/collections/business-furniture`; Industries / Brands / Services / About click → open dropdown only. Decide before NAV-2 builds the snippet whether to make all 5 dropdown-only (predictable, fewer footguns), or all 5 click-navigate to a hub (Industries Hub, Brands Hub, etc. would each become click-navigable from the top bar). RECOMMENDATION: all 5 dropdown-only. Open at top of NAV-2.

- **OECM prominence.** OECM is buried at About > OECM Procurement (3rd item in dropdown). `CLAUDE.md` flags OECM as the single biggest institutional-buyer differentiator. Track as part of W0-7 (site-wide OECM trust signals) — consider an OECM badge in the top bar or promoting OECM to first-item position in the About dropdown.

- **Search input.** Spec doesn't include a search input. B2B catalogs usually have one. DECISION NEEDED: does v1 launch include search? If yes, queue a NAV-5 row (search input position + autocomplete wiring). If no, document here that search is post-launch backlog.
