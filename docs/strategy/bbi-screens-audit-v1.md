# BBI Screens Audit v1

**Generated:** 2026-05-04  
**Status:** DS-0 complete — all 5 screens locked; inputs for DS-1  
**Gate:** feeds `docs/strategy/design-system.md` TBD resolution (DS-1)

---

## Screen inventory

| # | Template | Route | Round | Source | Lock status |
|---|---|---|---|---|---|
| T1 | Homepage | `/` | T4 | `round4-template-3-attachments/02-LOCKED-Homepage.jsx` | ✅ LOCKED |
| T2 | Collection — category | `/collections/business-furniture` | T4 | `round4-template-3-attachments/03-LOCKED-CollectionCategory.jsx` | ✅ LOCKED |
| T3 | Collection — sub | `/collections/seating` | T3 | `screens-t3-LOCKED-2026-04-29/src/Collection.jsx` | ✅ LOCKED |
| T4 | Landing — OECM | `/pages/oecm` | T5 | `screens-t5-2026-05-04/landing-oecm/src/Landing.jsx` | ✅ LOCKED |
| T5 | PDP — unbuyable | `/products/{handle}` | T5 | `screens-t5-2026-05-04/pdp-unbuyable/src/ProductDetail.jsx` | ✅ LOCKED |

All five screens compose **Phase-2 components only** — no new tokens, no invented components outside template-scoped CSS namespaces.

---

## Design tokens (canonical — all screens share)

Token file: `data/design-photos/screens-t5-2026-05-04/pdp-unbuyable/src/tokens.css`

### Typography

| Token | Value | Notes |
|---|---|---|
| `--bodyFont` | Inter, system-ui fallbacks | All body runs |
| `--headingFont` | Inter Tight → Inter fallback | All heading runs |
| `--bodyFontWeight` | 400 | |
| `--headingFontWeight` | 600 | |
| `--headingFontBase` | 48px | H1 desktop |
| `--bodyFontBase` | 16px | Body desktop |
| `--bodyFontLineHeight` | 1.55 | |
| `--headingFontLineHeight` | 1.1 | Tighter per brief |

### Spacing scale (4 px base)

`--space-1: 4px` · `--space-2: 8px` · `--space-3: 12px` · `--space-4: 16px` · `--space-6: 24px` · `--space-8: 32px` · `--space-12: 48px` · `--space-16: 64px` · `--space-24: 96px`

### Radius scale

| Token | Value | Where |
|---|---|---|
| `--buttonRadius` | 4 px | All CTAs — squared matches wordmark tone |
| `--inputRadius` | 4 px | Inputs, FAQ chip rings |
| `--cardRadius` | 8 px | Product cards, collection tiles, diff-cards |
| `--imageRadius` | 4 px | Inline images |
| `--productRadius` | 8 px | PDP gallery thumbnails |

### Color anchors

| Token | Hex | Contrast on white | Role |
|---|---|---|---|
| `--textColor` (ink) | `#0B0B0C` | 20.10 : 1 AAA | All body, headings, nav |
| `--saleBadgeBackground` (brand red) | `#D4252A` | 4.08 : 1 AA-large (white) | Eyebrow ticks, OECM dots, maple-leaf badges, CTA hover surface |
| `--headerHoverColor` / `--linkColor` (red-text) | `#A81E22` | 5.88 : 1 AA | Link + nav hover only — never default |
| `--background` | `#FFFFFF` | — | Default canvas |
| `--alternateBackground` | `#FAFAFA` | — | Alt sections, spec-table canvas |
| `--soldBadgeBackground` | `#5A5A5E` | 6.74 : 1 AA | Sold-out chip (PDP) |
| `--warningBackground` | `#E8A317` | 7.71 : 1 AA | Low-stock badge (PDP) |
| `--success` | `#1F6F3F` | 6.04 : 1 AA | Form success (quote page) |
| `--error` | `#B33A1A` | 5.93 : 1 AA | Form error (11° hue shift from brand red) |

**Red rule:** brand red (`#D4252A`) is a surface/accent only — never used as a heading or large text fill. Red-text (`#A81E22`) is hover-only. Total red pixel density across all templates ≤ 6.5%.

---

## Per-screen sections

### T1 — Homepage

**Route:** `/`  **Round:** T4  **File:** `02-LOCKED-Homepage.jsx`

| Section | Component class | Notes |
|---|---|---|
| Header (desktop + mobile) | `.bbi-header` | Logo · 5-item nav · phone pill · RFQ CTA |
| Hero | `.hp-hero` | H1 · deck · sub · 2 CTAs · micro trust line |
| Shop entry | `.hp-shop-entry` | 4 featured category tiles with image overlay |
| Featured products | `.hp-products` | 4 `.bbi-card--product` with buyable/unbuyable CTA split |
| OECM bar | `.hp-oecm-bar` | Badge + proof statement + tertiary CTA |
| Industries | `.hp-industries` | 5 industry shortcut tiles |
| Services | `.hp-services` | 3 service tiles |
| Our Work | `.hp-our-work` | 3 OCI project photo slots |
| Brands | `.hp-brands` | Logo grid + authorized badge row |
| CTA closer | `.bbi-cta-section` | Inverse canvas (`.scheme-inverse`) |
| Footer | `.bbi-footer` | 4-column · legal · maple-leaf plate |

**Red density at rest:** ≈ 5.6%  **With CTA hover:** ≈ 6.4%  
**Contrast check:** 11 pairs audited — 10 pass AAA, 1 AA-large (CTA hover), 1 N/A (reserved hover on inverse)

---

### T2 — Collection · category

**Route:** `/collections/business-furniture`  **Round:** T4  **File:** `03-LOCKED-CollectionCategory.jsx`

| Section | Component class | Notes |
|---|---|---|
| Header | `.bbi-header` | Shared with T1 |
| Breadcrumbs | `.cc-crumb-band` | Home → Shop |
| Intro band | `.cc-intro` | H1 · deck · sub · 4:5 catalogue image |
| 9-category grid | `.cc-cat-section / .cc-cat-grid` | `.bbi-card--collection` × 9 with image overlay + numbered chip |
| Industry shortcut | `.cc-industry-section` | 5 industry shortcut tiles |
| Brand index | `.cc-brand-section` | 12 brands in table rows by tier |
| OECM bar | (shared) | Reused from T1 |
| CTA closer | `.bbi-cta-section .scheme-inverse` | |
| Footer | `.bbi-footer` | |

**Red density at rest:** ≈ 3.8%  **With CTA hover:** ≈ 4.6%  
**Contrast check:** 14 pairs audited — all pass (AAA or AA-large)

---

### T3 — Collection · sub

**Route:** `/collections/seating` (canonical; generalizes to all 9 sub-collections)  **Round:** T3  **File:** `Collection.jsx`

| Section | Component class | Notes |
|---|---|---|
| Header | `.bbi-header` | Shared |
| Breadcrumbs | `.cn-crumb-band` | Home → Shop → {Category} |
| Intro band | `.cn-intro` | H1 · standfirst · brand count · warranty headline |
| Sub-category filter | `.cn-filter-bar` | Pill-style filter strip for sub-cats |
| Product grid | `.cn-product-grid` | `.bbi-card--product` data-driven; buyable vs. unbuyable CTA split |
| Brand plates | `.cn-brand-section` | 8 brands with Canadian + authorized badges |
| Pagination | `.cn-pagination` | 5-page strip |
| OECM bar | (shared) | |
| CTA closer | `.bbi-cta-section .scheme-inverse` | |
| Footer | `.bbi-footer` | |

**Data-driven:** swap `CN_CATEGORY` + `CN_PRODUCTS` data block — same component renders Desks, Storage, Tables, etc.  
**Contrast check:** all pairs AAA or AA-large (per T3 audit panel)

---

### T4 — Landing · OECM

**Route:** `/pages/oecm`  **Round:** T5  **File:** `Landing.jsx`

| Section | Component class | Notes |
|---|---|---|
| Header | `.bbi-header` | `current="services"` active state |
| Breadcrumbs | `.lp-crumb-band` | Home → Services (stub) → OECM |
| Hero | `.lp-hero` | H1 · standfirst · 2 CTAs · OECM badge + caption dot |
| Intro | `.lp-intro` | Paragraph body + inline OECM agreement link (stub) |
| Differentiator cards (2×2) | `.lp-diff-section / .lp-diff-grid` | 4 cards: Compliance · Supply · Delivery · Service |
| Trust-photo row | `.lp-trust-section` | 3 OCI project photos with captions |
| Proof bar | `.lp-proof-bar` | 3 stats: 60+ yr · 500+ accounts · 1 day |
| Cross-links strip | `.lp-cross-section` | `.bbi-card--collection` × 3 → Seating/Desks/Storage |
| OECM bar | `.bbi-oecm-bar` | Shared component |
| FAQ accordion | `.lp-faq-section` | 6 Q&A pairs; open-state chip on `.scheme-inverse` |
| CTA closer | `.bbi-cta-section .scheme-inverse` | |
| Footer | `.bbi-footer` | |

**Data-driven:** pass `data` prop shaped like `OECM_DEFAULTS` to render `/pages/healthcare`, `/pages/brands-keilhauer`, `/pages/about`, etc. Three sections toggle on `data.{trustPhotos|crosslinks}.length` and `data.proofStats`.  
**Red density at rest:** ≈ 5.5%  **With CTA hover:** ≈ 6.4%  **All FAQs open:** ≈ 5.7%  
**Contrast check:** 15 pairs audited — all AAA or AA-large  
**Stub links (2):** `/pages/services` hub (crumb), `/pages/oecm-agreement` (intro inline link)

---

### T5 — PDP · unbuyable

**Route:** `/products/{handle}` (canonical: Ibex MVL2803)  **Round:** T5 (T6 in Audits.jsx naming)  **File:** `ProductDetail.jsx`

| Section | Component class | Notes |
|---|---|---|
| Header | `.bbi-header` | `current="shop"` |
| Breadcrumbs | `.pd-crumb-band` | Home → Shop → Seating → Task Chairs → Product |
| Hero — gallery | `.pd-gallery` | 6-image thumbnail strip + main 4:5 slot |
| Hero — product info | `.pd-info` | Title · brand parent line · model code · standfirst · badge row (OECM · Canadian-made · Sold-out) |
| Commerce block | `.pd-commerce` (`.scheme-alt`) | Quote-mode: eyebrow + heading + sub + primary RFQ CTA + phone link + trust line |
| Description | `.pd-description` | 3 paragraphs + `bestFor` callout |
| Spec table | `.pd-spec-table` | Dimensions · weight · materials · features · certifications (hidden when empty) |
| Variants section | `.pd-variants` | Hidden on canonical (null on Ibex); shown for multi-variant products |
| OECM bar | `.bbi-oecm-bar` | Shared |
| Related products | `.pd-related` | 4 `.bbi-card--product` cards |
| Brand block | `.pd-brand-block` | Brand logo + blurb + authorized badge |
| CTA closer | `.bbi-cta-section .scheme-inverse` | |
| Footer | `.bbi-footer` | |

**Buyable variant:** same component; `data.commerce.buyable = true` adds qty stepper + price + stock dot. Red density unchanged (green stock dot, not red).  
**Data-driven:** `IBEX_DEFAULTS` shape covers all 645 PDPs — swap `data` prop, no structural rewrite needed.  
**Red density at rest:** ≈ 5.4%  **With CTA hover:** ≈ 6.5%  
**Contrast check:** 18 pairs audited — all pass (AAA, AA, or AA-large); 1 N/A (reserved hover-on-inverse)  
**Key token first-use on this template:** `--soldBadgeBackground` (#5A5A5E), `--productBorder`, `--productIconColor/Bg`

---

## Token coverage matrix

| Token group | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| `--bodyFont / --headingFont` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--fs-* / --lh-*` type scale | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--space-*` rhythm | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--buttonRadius / --cardRadius` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--background / --alternateBackground` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--textColor / --headingColor / --linkColor` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--buttonBackground/Color/Border (+Hover)` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--alternateButton*` set | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--saleBadgeBackground` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--borderColor` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--headerBg / --headerColor / --headerHoverColor` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--shadowColor` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `--warningBackground` (low-stock) | — | — | ✅ | — | ✅ |
| `--soldBadgeBackground` | — | — | — | — | ✅ |
| `--newBadgeBackground` | — | — | — | — | — |
| `--success / --error` | — | — | — | — | — |
| `--inputBackground/Color/Border` | — | — | — | — | — |
| `--productBorder / --productIconColor/Bg` | — | — | — | — | ✅ |
| `--cartCountBg/Color` | — | — | — | — | — |

`—` = reserved; not present on this template by design. `--newBadgeBackground`, `--success/--error`, `--inputBackground*`, and `--cartCountBg/Color` are unreferenced across all 5 screens — confirmed intentional (badges, forms, cart live elsewhere).

---

## Red density summary

| Template | At rest | CTA hover | Max state |
|---|---|---|---|
| T1 Homepage | 5.6% | 6.4% | 6.4% |
| T2 Collection cat | 3.8% | 4.6% | 4.6% |
| T3 Collection sub | ~4.2% | ~5.0% | ~5.0% |
| T4 Landing OECM | 5.5% | 6.4% | 5.7% (all FAQs open) |
| T5 PDP unbuyable | 5.4% | 6.5% | 6.5% |

All templates stay within the informal ≤ 7% red-density ceiling under all states. No red headings anywhere. Brand red (`#D4252A`) is surface + accent only.

---

## Contrast audit summary

All 5 templates pass WCAG 2.1 AA as a minimum. Most pairs are AAA. The one recurring AA-large pair (`#FFFFFF on #D4252A`, CTA hover) is intentional — large text / bold 16 px satisfies AA-large.

No failures across any template. The single `na` row (red-text `#A81E22` on inverse `#0B0B0C`) is explicitly reserved and never rendered.

---

## Navigation link audit summary

| Template | Pass | Stub | Notes |
|---|---|---|---|
| T1 Homepage | All | — | — |
| T2 Collection cat | All | — | — |
| T3 Collection sub | All | — | — |
| T4 Landing OECM | 15 | 2 | `/pages/services` hub + `/pages/oecm-agreement` — both placeholder anchors, OK at launch |
| T5 PDP unbuyable | All | — | — |

---

## DS-1 inputs (TBD resolution targets)

These screen audit findings directly feed the 53 TBDs in `docs/strategy/design-system.md`:

- **Typography tokens** — `--headingFont`, `--bodyFont`, full `--fs-*` / `--lh-*` scale now confirmed from tokens.css
- **Color palette** — all hex values, contrast ratios, and role assignments confirmed
- **Spacing + radius scales** — complete values from `--space-*` and `--*Radius` tokens
- **Component inventory** — all section/block names confirmed across 5 templates
- **Red density rule** — ≤ 7% ceiling, surface-only, never heading-fill
- **Contrast baseline** — WCAG 2.1 AA minimum; AA-large for CTA hover pair
- **Data-driven PDP pattern** — `IBEX_DEFAULTS` shape is the canonical data contract for 645 PDPs

---

## Changelog

| Date | Change |
|---|---|
| 2026-05-04 | v1 created — DS-0 complete; all 5 screens locked; T5 OECM + PDP extracted from Design System Zips |
