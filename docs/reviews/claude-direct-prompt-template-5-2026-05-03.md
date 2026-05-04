# Claude (direct) — BBI Template 5 PDP build

**Use:** fresh Claude conversation (claude.ai chat or Claude Code). All chat-confirm decisions are baked in — Claude builds directly, no back-and-forth round needed.

**Attachments to drop in:** see end of this prompt.

**Paste from the line below.**

---

You are building the 5th and final design template for Brant Business Interiors (BBI), a Canadian B2B office furniture dealer on Shopify. Four templates are already locked from prior rounds. Your job is to design and implement the Product Detail Page (PDP) — specifically the unbuyable variant, which is BBI's flagship pattern.

Output is React JSX + plain CSS (CSS custom properties for tokens, no Tailwind, no styled-components, no framework). The pattern is "design comps as code" — you produce JSX components and template-scoped CSS that compose into a multi-section design canvas, viewable as a single self-contained HTML bundle. The locked attached standalone (`01-LOCKED-templates-1-4-standalone.html`) is your visual + system reference. Open it in a browser before you start.

## What's already locked (do NOT modify)

Four templates, ten source files. All byte-identical inputs:

- `Homepage.jsx` (template 1) + `homepage.css` (`.hp-*` prefix)
- `CollectionCategory.jsx` (template 2) + `collection-category.css` (`.cc-*` prefix)
- `Collection.jsx` (template 3) + `collection.css` (`.cn-*` prefix)
- `Landing.jsx` (template 4) + `landing.css` (`.lp-*` prefix) — **this is your closest pattern reference for what you're building**
- `Audits.jsx` (audit registry, extend by appending one slice)
- `tokens.css` (v1 token set — full design system, do not extend)
- `bbi-components.css` (Phase-2 shared components — `.bbi-btn`, `.bbi-badge`, `.bbi-card`, `.bbi-section`, `.bbi-cta-section`, `.bbi-crumbs`, header, footer)
- `audits.css` (audit-panel atoms, `.ap-*` prefix)

Lock-file SHA-256 (16 chars) match required at end. No additions to `bbi-components.css`. No new tokens.

## What you're building

### Template 5: PDP — unbuyable variant

The BBI flagship pattern. Most BBI products are sold-out, $0-priced, or showcase items — they exist as B2B lead-capture pages, not transactional listings. Per the BBI rule: *"Unbuyable items stay live. Sold-out, $0-price, and showcase products keep their page with a Request a Quote CTA — these are B2B lead-capture pages, not dead listings."* The unbuyable PDP has no price, no add-to-cart, no quantity stepper. Quote-request CTA replaces the entire commerce block.

The same component must also handle the buyable variant (stocked accessories) via a single prop toggle (`buyable: false | true`) — but you're rendering the unbuyable as the canonical example. The buyable swap is data-driven, not a separate component.

### Canonical product

Ibex Multi-Tilter MVL2803 (OTG / Offices to Go). Sold-out, OECM-eligible, Canadian-made, sparse spec fields. Real spec data:

```
title:           "Ibex | Upholstered Seat & Mesh Back Multi-Tilter MVL2803"
brand:           "OTG · Offices to Go"
brand_parent:    "a division of Global Furniture Group"
brand_href:      "/pages/brands-global-teknion"
product_line:    "Ibex"
model_codes:     ["MVL2803", "OTG2803", "MVL2801", "MVL2804", "MVL2806", "MVL2817", "MVL2819C", "MVL2831BSUU", "MVL2832C"]
dimensions:      '26"W x 27"D x 39.5"H; Seat Height: 17.5" - 21.5"'
weight:          "56 lbs / 25.4 kg"
weight_capacity: ""        ← empty, row hides
materials:       "Upholstered seat fabric, mesh back"
finishes:        []        ← empty, row hides
key_features: [
  "Multi-tilt mechanism",
  "Upholstered seat with mesh back",
  "Pneumatic seat height adjustment (17.5\" - 21.5\")",
  "Height-adjustable arms",
  "Adjustable lumbar support",
  "Five-star base with casters"
]
certifications:  []        ← empty, row hides
warranty:        ""        ← empty, row hides
country:         ""        ← empty, row hides
```

The canonical render exercises empty-state grace directly — the spec table renders only the populated rows (brand, product line, model codes, dimensions, weight, materials, key features). This is non-negotiable: the audit panel's empty-state row must observably reflect what hid vs what rendered.

### Page structure (final, no changes — agreed in pre-build chat)

1. Header (locked, reuse from Homepage shared atoms)
2. Breadcrumbs — `Home / Shop Furniture / Seating / Task Chairs / Ibex Multi-Tilter MVL2803`
3. **Product hero band** — split layout:
   - Left (60% on desktop): Image gallery — main image (4:5 or 1:1) + thumb strip (4–8 thumbs, click to swap, no lightbox/zoom this round). Mobile: gallery stacks above text, thumb strip becomes horizontal scroller. Use placeholder fills for images (label text inside).
   - Right (40%): Brand mono-eyebrow → H1 product name → model code line (`MVL2803 · 9 model variants available`) → badge row → standfirst (1–2 sentences) → commerce block.
4. **Commerce block — unbuyable canonical:**
   - Eyebrow: `Project quote`
   - Heading: `Request a quote on this product`
   - Sub: `Volume pricing, lead time, OECM PO eligibility, freight, install — all confirmed within 1 business day. We respond from the same Ontario team that quotes weekly.`
   - Primary CTA full-width: `Request a quote →` (links to `/pages/quote`)
   - Secondary CTA inline: `Call 1-800-835-9565` (tel: link)
   - Trust microcopy below CTA: `OECM purchasers welcome · Quotes within 1 business day · Same Ontario team since 1962`
   - **NO price. NO add-to-cart. NO quantity stepper.**
   - For the buyable variant (data toggle, not separate component): price prominent, qty stepper, primary `Add to cart`, secondary `Request a quote` (kept), stock indicator. Trust microcopy stays.
5. **Description / story block** — single column max-width ~640px. 2–3 paragraphs of brand-voice copy. End with 1–2 sentence "Best for:" line.
6. **Spec table** — full-width, label column ~28% (`.bbi-mono`), value column ~72%. Rows render conditionally on field presence. Entire section hides if all rows empty.
7. **Variant / configuration selector** (only if product has variants) — fabric tier picker, finish swatch, with-or-without arms toggle. Renders as "What you'll quote" summary box. Hides entirely for products with no variants. Ibex canonical: hidden (variants is null in defaults).
8. **OECM bar** — reuse from Homepage / templates 2/3/4 verbatim (the `hp-oecm` block reused across templates).
9. **Related products row** — 3–4 cards using `.bbi-card--product` from `bbi-components.css`. Heading: `More from this category`. Mobile: horizontal scroller.
10. **Brand block** (optional) — `About OTG · Offices to Go` mini-card with one paragraph + link to `/pages/brands-global-teknion`. Hides for brands without dealer pages.
11. **Bottom CTA closer** — `.bbi-cta-section.scheme-inverse`:
    - Eyebrow: `Specifying for a project?`
    - Heading: `Outfitting more than one room?`
    - Sub: `Send us the floor plan or the spec list. We'll quote it as one project — products, freight, install, OECM paperwork. Same Ontario team. We respond within 1 business day.`
    - Primary CTA: `Request a quote`
    - Trust line: `or call 1-800-835-9565`
12. Footer (locked, reuse) with `.pd-page .bbi-footer { border-top: 1px solid var(--borderColor); }` separator rule per template-5 scope.

### Strict order

Hero → commerce → **description first, spec table after** (chat-confirmed deviation from initial strawman: editorial story before deep reference, matches Steelcase / Knoll / Herman Miller pattern). Sticky info rail deferred to a future round (no evidence of need on unbuyable PDP; bottom closer covers persistent action).

## Constraints

- **Template-scoping:** new prefix `pd-*` (product-detail) in a new `pdp.css` file. Mirror the Landing.jsx + landing.css `lp-*` pattern from round 6.
- **No additions to `bbi-components.css`.** Reuse `.bbi-btn`, `.bbi-badge`, `.bbi-card`, `.bbi-card--product`, `.bbi-cta-section`, `.bbi-crumbs`. Skin product-detail-specific patterns under `pd-*`.
- **Sold-out chip** — important: `.bbi-badge--sold` does **not** exist in `bbi-components.css` (the existing variants are `--sale`, `--new`, `--canadian`, `--oem`, `--oecm`). Build the sold-out treatment as `.pd-badge--sold` inside `pdp.css`. Don't add it to the locked components file.
- **Token discipline.** No new hardcoded hex literals. If a token exists for it, use the token. Defended literals carry a one-line comment naming why the token doesn't apply.
- **Empty-state grace.** Every conditional section (spec table rows, variant selector, brand block, gallery thumb strip with single image) hides cleanly when data is absent. No "Warranty: —" placeholders. The Ibex canonical exercises this directly — the spec table renders only populated rows.
- **Red density 5–8% at rest.** Audit must measure it. Watch the badge row (OECM + Canadian-made + Sold-out can stack red), commerce block primary CTA, related-products row CTAs, breadcrumb-active state.
- **Brand voice — match templates 1–4.** Plainspoken, B2B-savvy, both buyer paths in view, no fluff. OECM positioning is quiet, factual, institutional — never sale-tag loud.
- **Don't change:** tokens, components, scheme rules, header, footer, OECM bar copy, the 5 canonical sectors, the 9-category list, the brand-tier classification, dual-buyer positioning, audit panel structure (`ap-*` atoms in audits.css), DesignCanvas wrapper.

## Data-prop pattern (mirror Landing.jsx exactly)

`Landing.jsx` (locked, attached) ships with `OECM_DEFAULTS` and `function Landing({ mobile, data = OECM_DEFAULTS })`. Mirror this pattern for ProductDetail. `<ProductDetail />` no-prop renders the canonical Ibex unbuyable page; `<ProductDetail data={someBuyableProductData} />` renders any other PDP without a structural rewrite. 645 products will eventually use this template.

The 9 prop slots:

```js
const IBEX_DEFAULTS = {
  product:    { title, brand, brandParent, brandHref, productLine, modelCodes, standfirst, badges },
  gallery:    { images, placeholderLabel },                              // images: [{ label }] for placeholders
  commerce:   { buyable: false, price?, unit?, stock?, leadTime?, qty? }, // buyable:true swaps the block
  description:{ paragraphs, bestFor? },
  specs:      { dimensions?, weight?, weightCapacity?, materials?, finishes?, features?, certifications?, warranty?, country?, leadTime?, compliance? }, // every key optional
  variants:   null | { items },                                          // null hides whole section
  related:    { heading, items },                                        // items reuse .bbi-card--product
  brandBlock: null | { name, blurb, href },                              // null hides
  closer:     { eyebrow, heading, sub, primaryCta, trustLine },          // PDP defaults baked
};

function ProductDetail({ mobile = false, data = IBEX_DEFAULTS }) {
  const showSpecs       = Object.values(data.specs || {}).some(v => Array.isArray(v) ? v.length > 0 : !!v);
  const showVariants    = !!data.variants;
  const showBrandBlock  = !!data.brandBlock;
  // … render
}
window.ProductDetail = ProductDetail;
window.PDP_IBEX_DEFAULTS = IBEX_DEFAULTS;
```

## Audit registry extension

Existing `Audits.jsx` keys (verbatim, in order): `"homepage"`, `"collection-category"`, `"collection"`, `"landing"`. Append a fifth `register("product", { ... })` block. Existing four slices stay byte-identical.

The `product` slice carries six audit panels — the standard four plus two bespoke. The standard four go in the canonical fields (`contrast`, `red`, `tokens`, `crosslinks`). The two bespoke panels go into a new optional `extras: []` array on the registry entry — this lets future templates add bespoke panels without touching the root render. Existing four slices get `extras: []` (no-op for them; the root iterates and renders nothing).

The two bespoke panels:

- **Empty-state behavior** (`extras[0]`) — table showing each conditional section (spec rows, variant selector, brand block, gallery thumb-strip-with-single-image, sticky rail) and which behavior the canonical render exercises (rendered / hid). The Ibex canonical: spec rows hidden = `weight_capacity, finishes, certifications, warranty, country, leadTime, compliance`; spec rows shown = `brand, productLine, modelCodes, dimensions, weight, materials, features`; variants section hidden; brand block shown.
- **Variant toggle** (`extras[1]`) — table showing the unbuyable→buyable swap diff. Rows: commerce eyebrow (changes), heading (changes), sub (changes), primary CTA (Request a quote → Add to cart), secondary CTA (Call → Request a quote), price block (absent → present), qty stepper (absent → present), stock indicator (absent → present), trust microcopy (unchanged — present in both).

The standard four panels for the product slice (write actual values, not placeholders):
- **Contrast** — every text/bg pair on the PDP (hero title, brand eyebrow, model code line, badge text, commerce block heading + sub + CTA + microcopy, spec label/value, description body, related card title + CTA, brand block, closer). Measure ratios at the rendered cascade. AAA target.
- **Red density** — at rest with one-hover delta. 5–8% target. Measure per section: header / breadcrumbs / hero text / hero badges / commerce block / description / spec table / variants / OECM bar / related row / brand block / closer / footer.
- **Token coverage** — list every token consumed (with the rule that uses it) and every token reserved-but-unused on this template. Flag any defended literal with its one-line reason.
- **Cross-links** — every link surface on the page resolves to a real route. Up to `/`, sideways to `/collections/business-furniture`, back to `/collections/seating` and `/collections/task-chairs`, down to `/pages/quote` (CTA target), `/pages/brands-global-teknion` (brand block), other PDP routes via related-row, OECM bar self-link, phone CTA mandatory.

## Bundle verification — non-negotiable

Before delivering, verify the standalone bundle itself, not just the source files. Round 5 shipped a Template-4-only standalone instead of the 4-section DesignCanvas; round 6 caught and fixed it. Don't repeat.

Open the new standalone in a browser. Scroll through all five sections. Confirm every section renders with no missing styles, no unstyled flash-of-content, no broken layout. Confirm the four previously locked sections render byte-equivalent to `01-LOCKED-templates-1-4-standalone.html` — adding section 5 must not alter any rule that affects 01–04.

State the verification line before delivering files:

> Standalone bundle verified: opens cleanly in a browser, all 5 DesignCanvas sections (`01 Homepage`, `02 Collection · category`, `03 Collection`, `04 Landing · OECM`, `05 PDP · unbuyable`) render with no missing styles. CSS present in the bundle: tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, landing.css, **pdp.css (new)**, audits.css. `.hp-*`, `.cc-*`, `.cn-*`, `.lp-*`, and `.pd-*` rules all present and scoped to their respective sections (no `.pd-*` rule leaks into 01–04). Source files byte-identical to the locked versions attached: Homepage.jsx, CollectionCategory.jsx, Collection.jsx, Landing.jsx, Audits.jsx (extended only by adding the `product` slice — homepage/collection-category/collection/landing slices unchanged), tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, landing.css, audits.css. SHA-256 (16 chars) for each: ___.

## Deliverables

Three HTML files + updated `src/`:

1. `index.html` — DesignCanvas driver, 5 sections (`hp`, `cc`, `cn`, `lp`, `pd`). Mirror the round-6 `index.html` pattern in attached locks. Each section gets desktop / mobile / audit artboards (`pd-1440`, `pd-375`, `pd-audits`). Sanity-check artboard heights against the final render before delivering — round 3 shipped with `cc-1440` undersized by ~190px; don't repeat.
2. `BBI Templates Bundle.html` — single self-contained 5-section standalone, all CSS + JSX inlined, ~3MB. React + ReactDOM + Babel UMDs stay as `<script src>` to unpkg.com (round-6 pattern).
3. `Template 5 - PDP (unbuyable).html` — isolated review file (the PDP page only + audits, mirrors `Template 4 - Landing (OECM).html` shape).

`src/` files updated:
- `ProductDetail.jsx` — the page component, accepts `data` prop with `IBEX_DEFAULTS`. `<ProductDetail />` no-prop renders the canonical Ibex unbuyable page byte-identically every time.
- `pdp.css` — template-scoped patterns, `pd-*` prefix.
- `Audits.jsx` — extended with the `product` slice, existing four slices byte-identical.
- All 11 prior locked files byte-identical to attached versions.

---

## Files attached (drop all 18 into the new conversation)

| # | File | Purpose |
|---|---|---|
| 1 | `01-LOCKED-templates-1-4-standalone.html` | Visual + code reference for all four locked templates. Open in a browser before designing. |
| 2 | `02-LOCKED-Homepage.jsx` | Homepage source — locked, do not edit |
| 3 | `03-LOCKED-CollectionCategory.jsx` | Collection-category source — locked, do not edit |
| 4 | `04-LOCKED-Collection.jsx` | Collection source — locked, do not edit |
| 5 | `05-LOCKED-Landing.jsx` | Landing source — locked, do not edit. **Study this carefully — your data-prop pattern (`OECM_DEFAULTS` + `data = OECM_DEFAULTS` default + present/absent toggles) mirrors this file exactly.** |
| 6 | `06-tokens.css` | v1 tokens — extend, do not rewrite. Use existing tokens; do not add new ones. |
| 7 | `07-bbi-components.css` | Phase-2 components — locked. **Do not modify, do not add to.** Reuse `.bbi-btn`, `.bbi-badge`, `.bbi-card`, `.bbi-card--product`, `.bbi-cta-section`, `.bbi-crumbs`. |
| 8 | `08-homepage.css` | Homepage CSS — locked, study `.hp-*` pattern |
| 9 | `09-collection-category.css` | Template-2 CSS — locked, study `.cc-*` pattern |
| 10 | `10-collection.css` | Template-3 CSS — locked, study `.cn-*` pattern |
| 11 | `11-landing.css` | Template-4 CSS — locked, study `.lp-*` pattern (your closest analogue for `.pd-*`) |
| 12 | `12-audits.css` | Audit-panel atoms (`ap-*`) — locked |
| 13 | `13-LOCKED-Audits.jsx` | Audit registry — extend by appending one slice. Existing four registry keys (`homepage`, `collection-category`, `collection`, `landing`) stay byte-identical. Add `extras: []` array support to the root render. |
| 14 | `14-bbi-component-spec-v1.md` | Phase-2 component spec |
| 15 | `15-design-system-brief.md` | Original constraint brief |
| 16 | `16-bbi-logo-v2.png` | Logo asset |
| 17 | `17-ANTI-REF-homepage.png` | Anti-pattern: do NOT design like this (the beige + dramatic-photo combo we're eliminating) |
| 18 | `18-ANTI-REF-nav.png` | Anti-pattern: do NOT design like this |
