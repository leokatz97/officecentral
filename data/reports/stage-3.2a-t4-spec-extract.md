# Stage 3.2a — T4 Sub-Collection Spec Extract

**Generated:** 2026-05-07  
**Source:** `docs/strategy/bbi-screens-audit-v1.md`, `docs/strategy/bbi-component-spec-v1.md`, `docs/strategy/design-system.md`  
**Read alongside:** `data/reports/stage-3.1a-t3-spec-extract.md`

---

## ⚠️ Critical Finding: No Locked Screen for Sub-Collection Template

The `bbi-screens-audit-v1.md` defines **5 locked screens** numbered T1–T5:

| Screen label | Route | Round |
|---|---|---|
| T1 | Homepage `/` | T4 |
| T2 | Collection · category `/collections/business-furniture` | T4 |
| T3 | Collection · sub `/collections/seating` | T3 |
| T4 | Landing · OECM `/pages/oecm` | T5 |
| T5 | PDP · unbuyable `/products/{handle}` | T5 |

**The 68 sub-collection pages (`/collections/active-seating`, `/collections/executive-desks`, etc.) do not correspond to any of the 5 locked screens.** Stage 3.2's "T4" designation is different from the design system's "T4" label. There is no Claude Design mockup for the sub-collection template.

The T3 screen (Collection · sub = the 9 hub pages) is the closest design analogue. The sub-collection spec below is inferred from:
1. T3 screen as a structural model (one level down)
2. `bbi-component-spec-v1.md` product card dimensions
3. Issues identified in the May 7 walkthrough

---

## Inferred T4 Layout — Section Inventory (top → bottom)

| # | Section | Inferred from | Notes |
|---|---|---|---|
| 1 | Header | T3 + all screens | `.bbi-header` shared, `active='shop'` |
| 2 | Breadcrumbs | T3 analogue | 4-level: Home → Shop Furniture → {parent hub} → {this sub} |
| 3 | Hero strip | Current ds-cs-base.liquid | Label · H1 · product count |
| 4 | Filter sidebar | Current ds-cs-base.liquid | Tag-based (type:, room:) + price range |
| 5 | Product grid | Component spec + T3 analogue | 2/3/4-col responsive, `.bbi-card--product` |
| 6 | Phone CTA band | Current ds-cs-base.liquid | Charcoal canvas, phone + consultation CTA |
| 7 | Footer | All screens | `.bbi-footer` shared |

---

## Per-Element Detail

### 1. Header
- Shared snippet: `bbi-nav.liquid`
- Active nav item: `shop`
- No change expected

### 2. Breadcrumbs
- 4-level: Home → Shop Furniture → {parent category} → {this sub-collection}
- `bbi-crumbs` snippet with c2/c3/c4 levels
- Currently implemented and correct in ds-cs-base.liquid
- Parent category handle/title must be set per-collection via schema settings

### 3. Hero Strip
- Eyebrow: parent category label (mono/uppercase)
- H1: collection title (or `hero_title` override)
- Subtitle: product count or custom `hero_subtitle`
- Hero image: optional 180px accent image (right-aligned on desktop)
- **GAP-T4-1:** No hero CTA button. Brief specifies "Shop all [parent-category]" → parent hub URL. Not present in current code or spec.
- **GAP-T4-2:** Hero stats line (analogous to T3's "brand count + warranty headline") not specified and not present.

### 4. Filter Sidebar
- Collapsible on mobile, always-visible on ≥900px
- Groups: Product Type (`type:` tags), Room / Setting (`room:` tags), Price (min/max inputs)
- **Deferred to 3.1c.2:** Tag census at 0% for `subcategory:`, `brand:`, `height:`, `fabric:`, `warranty:`. The current `type:` and `room:` tag filters have some coverage (87.9% and 46.2% respectively) and are functional in the existing code.
- No spec entry for T4 filter rail. Existing implementation is reasonable.

### 5. Product Grid
- From component spec: `.bbi-card--product` with **4:5 image** (portrait), 16px body padding, 14px title
- Grid columns: 2-col mobile → 3-col ≥640px → 4-col ≥1024px (current implementation)
- Pagination: 24 per page (current; spec doesn't specify for T4)
- Sort: dropdown (best-selling, name A-Z, price asc/desc)
- **GAP-T4-3:** Component spec says 4:5 image ratio. Current code uses 4:3. Actual catalog images are 1:1 square. See image cropping diagnosis.
- **GAP-T4-4:** CTA routing bug. Quote-only tiles link to `/pages/quote` directly instead of PDP. See CTA routing diagnosis.
- **GAP-T4-5:** No badge rendering (sale, new, sold-out) on current cards. T3/T5 spec includes badge system.

### 6. Phone CTA Band (closer)
- Charcoal inverse canvas (`#0B0B0C`)
- H2 heading + body copy + "Call a Consultant" + "Free Design Consultation" CTAs
- Toggled via `show_phone_cta` schema setting (default: true)
- Functionally equivalent to T3's `.bbi-cta-section .scheme-inverse`
- **GAP-T4-6:** Missing OECM trust line below CTA. T3 spec shows OECM trust line in the CTA closer. Current phone CTA band has no OECM copy.

### 7. Footer
- Shared snippet: `bbi-footer.liquid`
- No change expected

---

## Missing T3 Sections (Not Present in T4)

T3 has these sections; T4 spec is silent on them:

| T3 Section | In T4? | Notes |
|---|---|---|
| Brand plates (`cn-brand-section`, 8 brands) | **No** | **GAP-T4-7:** Not specified for T4. Logical to omit (sub-collection is narrower) but needs decision. Brand-coupled sub-collections (keilhauer, ergocentric, global-furniture) could be exceptions. |
| OECM bar | **No** | **GAP-T4-8:** Shared `.bbi-oecm-bar` referenced in T3 + T4 (OECM page) + T5. Not present in ds-cs-base.liquid. |
| Sub-category filter pills | N/A | T3 pills link to T4 sub-collections. T4 has no equivalent drill-down. Correct to omit. |

---

## T4 Spec Gaps Summary

| ID | Element | Gap | Severity | Blocker for 3.2b? |
|---|---|---|---|---|
| GAP-T4-1 | Hero | No CTA button specified or present | Medium | No — can add "Shop all X" using existing schema settings |
| GAP-T4-2 | Hero | Stats line (brand count + warranty) not specified for T4 | Medium | No — decision: ship analog or skip |
| GAP-T4-3 | Product grid | Image ratio: spec says 4:5, code is 4:3, source images are 1:1 | High | Yes — need ratio decision before card CSS change |
| GAP-T4-4 | Product grid | Quote-only CTA routes to /pages/quote, not PDP | High | Yes — BBI rule #2 violation |
| GAP-T4-5 | Product grid | Sale/new/sold badges not implemented | Low | No — defer; catalog badge coverage unknown |
| GAP-T4-6 | CTA closer | OECM trust line missing from phone CTA band | Low | No — schema override workaround |
| GAP-T4-7 | Brands strip | Not specified for T4; not present | Low | No — decision: omit, add, or special-case brand sub-collections |
| GAP-T4-8 | OECM bar | Not present (no shared snippet yet; deferred from T3 work) | Low | No — deferred to T3 phase (bbi-oecm-bar.liquid not yet created) |

**Total spec gaps: 8** (2 high, 2 medium, 4 low)

---

## Component Dependencies

| Component | Status | Notes |
|---|---|---|
| `bbi-nav.liquid` | ✅ Exists | No change |
| `bbi-crumbs.liquid` | ✅ Exists | No change |
| `bbi-footer.liquid` | ✅ Exists | No change |
| `bbi-oecm-bar.liquid` | ❌ Doesn't exist | Deferred from 3.1b; needed for GAP-T4-8 |
| Product card (inline) | ⚠️ Exists with bugs | Fix image ratio + CTA routing |
| Filter sidebar (inline) | ✅ Functional | Defer enhancement |
