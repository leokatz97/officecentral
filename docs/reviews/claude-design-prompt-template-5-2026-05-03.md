# Claude Design — Phase 3 / Round 7: Template 5 (PDP — unbuyable variant)

**Prototype name:** `6 — pdp`
**Conversation:** fresh (do NOT continue any previous conversation)
**Attachments:** the 18 files in `data/design-photos/round6-template-5-attachments/`, listed at the end of this prompt
**Paste from the line below.**

---

You're picking up where round 6 left off. Templates 1 (Homepage), 2 (Collection · Category), 3 (Collection / sub-collection), and 4 (Landing · OECM) are all locked — attached as `01-LOCKED-templates-1-4-standalone.html` plus their source files (`Homepage.jsx`, `CollectionCategory.jsx`, `Collection.jsx`, `Landing.jsx`, `Audits.jsx`, and the six CSS files) for code reference. **Open the locked standalone in a browser before designing.** It's the canonical visual + system reference. You'll see four sections in the design canvas:
- `01 — Homepage (locked)` — desktop 1440 + mobile 375 + audit panels
- `02 — Collection · category (locked)` — same shape
- `03 — Collection (locked)` — same shape
- `04 — Landing · OECM (locked)` — same shape

Add `05 — PDP · unbuyable (locked)` as your new section.

This is a fresh conversation, so the locked-system inheritance is restated in full below.

## Inheritance from rounds 1–6

- **Tokens:** v1 set including `--warningBackground: #E8A317;`. No new tokens. No renames.
- **Components:** Phase-2 patterns from `bbi-components.css` — `.bbi-btn`, `.bbi-badge`, `.bbi-card` (product / collection), `.bbi-section`, `.bbi-section-head`, `.bbi-cta-section`, `.bbi-crumbs`, header, footer (always `.scheme-inverse`). Compose only.
- **Schemes:** scheme-default unless explicitly inverse (CTA closer, footer).
- **Template-scoping pattern:** template-2 uses `cc-*`. Template-3 uses `cn-*`. Template-4 uses `lp-*`. Use the same pattern for template 5 — prefix `pd-*` (product-detail) — in a new `pdp.css` file. Don't touch `bbi-components.css` unless you can demonstrate a system-wide need (and even then, ask first).
- **Footer separator pattern:** `.pd-page .bbi-footer { border-top: 1px solid var(--borderColor); }` solves the back-to-back inverse problem (same fix templates 2/3/4 use).
- **Positioning:** Two buyer paths in parallel — transactional (catalogue) and project (RFQ). OECM is the institutional differentiator. Mississauga = HQ only (footer plate); Ontario = market.
- **Data-driven prop pattern (round-6 lock):** Landing.jsx ships with `OECM_DEFAULTS` and `function Landing({ mobile, data = OECM_DEFAULTS })`. ProductDetail follows the same pattern — defaults baked, prop-overridable, present/absent toggles for optional sections.

## What template 5 is

A single product detail page. There are 645 products in BBI's catalogue. The template must handle two variants from a single component:

- **Unbuyable variant** (the canonical render, the BBI flagship pattern): no price, no Add-to-Cart, no quantity selector. Quote-request CTA replaces the entire commerce block. Used for sold-out products, $0-priced products, and any product flagged as showcase. This pattern matters because BBI is a B2B dealer — most product pages exist as lead-capture surfaces, not transactional ones.
- **Buyable variant**: classic e-commerce — price, quantity stepper, Add-to-Cart primary, Request-a-Quote secondary. Used for stocked accessories and any product priced and in stock.

Both variants share the same template; the variant difference is one prop toggle (`buyable: false | true`) plus the data swap (price exists or doesn't, stock exists or doesn't). Per the BBI rule from `CLAUDE.md`: *"Unbuyable items stay live. Sold-out, $0-price, and showcase products keep their page with a Request a Quote CTA — these are B2B lead-capture pages, not dead listings."*

For this round, design the **unbuyable canonical** as the primary render, and confirm the buyable variant is a single prop toggle with a brief swap-summary in chat (no separate render needed unless you find a structural issue).

Canonical example: a Keilhauer task chair, sold-out, OECM-eligible, Canadian-made. URL pattern `/products/[handle]`.

## Real product data shape (so you build for actual content, not lorem ipsum)

Sample from `data/specs/ibex-upholstered-seat-mesh-back-multi-tilter-1.json`:

```
title:           "Ibex | Upholstered Seat & Mesh Back Multi-Tilter MVL2803"
brand_hint:      "OTG / Offices to Go (a division of Global Furniture Group)"
product_line:    "Ibex"
model_codes:     ["MVL2803", "OTG2803", "MVL2801", "MVL2804", ...] (often 5–10 codes)
dimensions:      '26"W x 27"D x 39.5"H; Seat Height: 17.5" - 21.5"'
weight:          "56 lbs / 25.4 kg"
weight_capacity: "" (often empty)
materials:       "Upholstered seat fabric, mesh back"
finishes_available: [] (often empty for unbuyable showcase items)
key_features:    [5–10 bullets]
certifications:  [] (often empty)
warranty:        "" (often empty)
country_of_manufacture: "" (often empty)
```

Build for this reality: many spec fields are empty or sparse for unbuyable showcase products. The template must degrade gracefully — empty fields hide entirely (not "Warranty: —"), fields with content render. The spec table can't assume any field is present.

## Page structure (strawman — adjust if a better composition emerges, but confirm in chat first)

1. Header (locked, reuse).
2. Breadcrumbs — `Home / Shop Furniture / Seating / Task Chairs / Ibex Multi-Tilter MVL2803`.
3. **Product hero band** — split layout, the most important section on the page:
   - **Left (60%)**: Image gallery. Main image (4:5 or 1:1), thumbnail strip below (4–6 thumbs visible, scroll if more). Click thumb to swap main. No lightbox required for this round (mark as "future enhancement" in audit). Mobile: gallery stacks above text, thumb strip becomes a horizontal scroller.
   - **Right (40%)**: Title block — brand mono-eyebrow ("OTG · Offices to Go" or "Keilhauer · Authorized Dealer") → H1 product name → model code line ("MVL2803 · 9 model variants available") → badge row (OECM-eligible if applicable, Canadian-made if applicable, Sold-out chip if applicable). Standfirst (1–2 sentences positioning the product). Then the **commerce block** (the unbuyable/buyable swap point) — see structure below.
4. **Commerce block — unbuyable variant** (the BBI flagship):
   - Eyebrow: `Project quote`
   - Heading: `Request a quote on this product`
   - Sub: `Volume pricing, lead time, OECM PO eligibility, freight, install — all confirmed within 1 business day. We respond from the same Ontario team that quotes weekly.`
   - Primary CTA (full-width): `Request a quote →`
   - Secondary CTA inline: `Call 1-800-835-9565`
   - Trust microcopy below CTA: `OECM purchasers welcome · Quotes within 1 business day · Same Ontario team since 1962`
   - **NO price. NO add-to-cart. NO quantity stepper.** This is non-negotiable.
5. **Commerce block — buyable variant** (data toggle, NOT a separate render):
   - Price prominent (large), unit label below.
   - Quantity stepper.
   - Primary CTA: `Add to cart`. Secondary outline: `Request a quote` (kept — buyable doesn't kill the project-buyer path).
   - Stock indicator: `In stock · Ships in 3–5 days` or `Backorder · Ships in 4 weeks`.
6. **Sticky info rail** (optional, desktop only, your call) — appears after user scrolls past the hero. Persistent quote-request CTA + product title in a slim band. If you choose not to build this, justify in chat.
7. **Spec table** — full-width, structured, but **graceful with empty fields**. Suggested rows (only render if the field has content):
   - Brand · Product line · Model codes (list)
   - Dimensions · Seat height · Weight · Weight capacity
   - Materials · Finishes available · Fabric tier
   - Key features (bulleted list, not row-per-feature)
   - Certifications (BIFMA, GREENGUARD, etc.)
   - Warranty · Country of manufacture · Lead time
   - Compliance (OECM-eligible, AODA-compliant, etc.)
   Group visually with subtle horizontal rules; use the locked `.bbi-mono` style for label cells, body font for value cells. Width: full container, label column ~28%, value column ~72%.
8. **Description / story block** — single-column, max-width ~640px. 2–3 paragraphs of brand-voice copy ("Quoted weekly for school boards and admin floors. The Ibex is OTG's workhorse multi-tilter — adjustable everything, mesh back, no learning curve. Procurement officers like it because it carries on existing OECM contracts; specifiers like it because it doesn't fight the room.") End with a 1–2 sentence "Best for:" line ("Best for: admin floors, training rooms, classrooms, hot-desk pools.").
9. **Variant / configuration selector** (only if product has variants) — fabric tier picker, finish swatch, with-or-without arms toggle. Renders as a "What you'll quote" summary box that updates the model-code line in the title above. For products with no variants, this section hides entirely.
10. **OECM bar** — reuse the homepage / template 2 / template 3 / template 4 component verbatim, same target.
11. **Related products row** — 3–4 product cards from the same sub-category. Reuse `.bbi-card--product` from `bbi-components.css` (the same card used in template 3). Heading: `More from this category` or `Other Multi-Tilters`. Mobile: horizontal scroller.
12. **Brand block** (optional small strip) — `About OTG / Offices to Go` mini-card with one paragraph, link to `/pages/brands-global-teknion` (or appropriate brand page). For brands without a dealer page, this section hides.
13. **Bottom CTA closer** — `.bbi-cta-section.scheme-inverse` with PDP-specific copy:
    - Eyebrow: `Specifying for a project?`
    - Heading: `Outfitting more than one room?`
    - Sub: `Send us the floor plan or the spec list. We'll quote it as one project — products, freight, install, OECM paperwork. Same Ontario team. We respond within 1 business day.`
    - Primary CTA: `Request a quote`
    - Trust line: `or call 1-800-835-9565`
14. Footer (locked, reuse, with the `.pd-page .bbi-footer { border-top: 1px solid var(--borderColor); }` separator rule per template-5 scope).

## Constraints

- **No new tokens.** Full v1 set is in `06-tokens.css`.
- **No new bbi-* components in `bbi-components.css`.** Template-scoped classes go in a new `pdp.css` file with `pd-*` prefix.
- **Token discipline.** No new hardcoded hex literals. Defended literals from rounds 1–6 carry over. Each defended literal in `pdp.css` needs a one-line comment, AND if the token exists, just use it (round-6 retro: every literal you "defended" was actually tokenizable).
- **Red density 5–8% at rest** — same target as previous rounds. Audit must measure it. Watch the badge row (OECM + Canadian-made + Sold-out can stack red), the commerce-block primary CTA, and the related-products row CTAs.
- **Unbuyable variant has NO price and NO add-to-cart.** This is the BBI rule — non-negotiable. The Quote-request CTA is the *only* commerce surface.
- **Spec table must degrade gracefully on empty fields.** Don't render "Warranty: —" or "Certifications: not specified." If the field is empty, the row hides entirely. Same for the entire spec table — if a product has zero spec fields populated, the spec section hides.
- **Brand voice — match templates 1, 2, 3, 4.** Plainspoken, B2B-savvy, both buyer paths in view, no fluff. Examples already in the locked files.
- **Don't change:** tokens, components, scheme rules, header, footer, OECM bar copy, the 5 canonical sectors, the 9-category list, the brand-tier classification, dual-buyer positioning, audit panel structure (`ap-*` atoms in audits.css), DesignCanvas wrapper. Lock includes `Homepage.jsx`, `CollectionCategory.jsx`, `Collection.jsx`, `Landing.jsx`, `Audits.jsx`, `tokens.css`, `bbi-components.css`, `homepage.css`, `collection-category.css`, `collection.css`, `landing.css`, `audits.css`.

## Audit panels — same four, same shape, same `ap-*` atoms

Use the `ap-*` audit-panel atoms from the locked `audits.css`. Extend the existing `Audits` component to add a `template="product"` slice (don't replace — keep the round-3 registry pattern). Specific to template 5:

- **Contrast** — every text/bg pair on this template, measured at the rendered cascade. Pay attention to the spec-table label/value rows, the sticky info rail (if built), the badge row in the hero, and the unbuyable commerce block (heading + sub + CTA + microcopy).
- **Red density** — at rest, with a one-hover delta. Target 5–8%. The badge row + commerce block primary CTA + related-products row + breadcrumb-active-state all add red.
- **Token coverage** — exercised + reserve.
- **Cross-links** — every link surface resolves to a real route. Up to `/`, sideways to `/collections/business-furniture` (template 2), back to `/collections/seating` (template 2 child) and `/collections/task-chairs` (template 3, locked), down to `/pages/quote` (CTA target), `/pages/brands-global-teknion` (brand block, if rendered), phone CTA mandatory. Also: related-products row links resolve to other PDP routes (`/products/[handle]`).
- **Empty-state behavior** — explicit audit pass confirming the spec table, variant selector, and brand block all hide cleanly when their data is absent (this is the spec-grace requirement; show the audit row stating each section's empty-state was tested).
- **Variant toggle** — explicit audit pass confirming the unbuyable→buyable swap is a single prop toggle, not a structural rebuild. Show the diff between the two renders in the audit (price + qty stepper + add-to-cart appear; unbuyable trust microcopy stays).

## Reply contract — non-negotiable this round

Before you design, **confirm in chat** (four or five sentences, in chat, not in code comments):

1. The strawman page structure — agreed, or what you'd shift and why. Specifically: do you want the spec table mid-page (as positioned, between commerce and description) or after the description? And is the sticky info rail worth building this round, or defer to a future round once we see real product traffic patterns?
2. **Unbuyable vs buyable strategy** — single component with `buyable: false | true` data toggle, or two distinct sub-components with a shared shell? I want the single-component approach (matches the Landing data-prop pattern from round 6) but if there's a structural reason to split, say so.
3. **Spec table treatment** — single flat table (rows render conditionally on field presence), or grouped accordion (Dimensions / Materials / Certifications, each collapsible)? I want flat for this round — easier to scan for procurement specifiers — but flag if your judgment differs.
4. **Image gallery treatment** — main image + thumb strip below (no lightbox, no zoom this round), or do you propose adding zoom-on-hover or a lightbox? I want the simpler version this round; B2B specifiers download spec sheets, they don't pinch-zoom product photos. Flag if you disagree.
5. Whether template 5 needs any addition to `bbi-components.css` (it shouldn't — `.bbi-card--product` is reused from template 3 for the related-products row, and `.bbi-cta-section.scheme-inverse` is reused for the bottom closer).
6. Audit registry pattern — how you'll extend `Audits` to add the `template="product"` slice without dropping the homepage / collection-category / collection / landing slices. Open `13-LOCKED-Audits.jsx` and name the existing registry keys verbatim before you append.
7. **Generalization check** — name the 4–5 prop slots that need to take props so the same template renders 645 products without a structural rewrite. At minimum: product (title, brand, model codes, badges, gallery), specs (the conditional fields object), variants (or null), description (rich text), related (array of product cards), brandBlock (or null), buyable (boolean toggle that swaps the commerce block). I want to see you've thought about reuse before you build the canonical render.

Wait for my reply before exporting. Round 6's first delivery skipped the generalization implementation despite agreeing to it in chat — converted module constants to props only after a fix round. Don't repeat.

## Bundle verification — also non-negotiable this round

Before you export the standalone, verify **the standalone bundle itself**, not just the source files. Round 5's first delivery shipped a Template-4-only standalone instead of the 5-section DesignCanvas; round 6 caught and fixed it. Keep that discipline this round — first export must be the 5-section bundle.

Verification target: open the new standalone in a browser, scroll through all five sections in DesignCanvas, and confirm every section renders with no missing styles, no unstyled flash-of-content, no broken layout. Specifically check that the four previously locked sections (`01 Homepage`, `02 Collection · category`, `03 Collection`, `04 Landing · OECM`) render byte-equivalent to the attached `01-LOCKED-templates-1-4-standalone.html` — the new bundle should add `05 PDP · unbuyable` without altering any rule that affects 01–04. State this in chat before exporting:

> "Standalone bundle verified: opens cleanly in a browser, all 5 DesignCanvas sections (`01 Homepage`, `02 Collection · category`, `03 Collection`, `04 Landing · OECM`, `05 PDP · unbuyable`) render with no missing styles. CSS present in the bundle: tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, landing.css, **pdp.css (new)**, audits.css. `.hp-*`, `.cc-*`, `.cn-*`, `.lp-*`, and `.pd-*` rules all present and scoped to their respective sections (no `.pd-*` rule leaks into 01–04). Source files byte-identical to the locked versions attached: Homepage.jsx, CollectionCategory.jsx, Collection.jsx, Landing.jsx, Audits.jsx (extended only by adding the `product` slice — homepage/collection-category/collection/landing slices unchanged), tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, landing.css, audits.css. SHA-256 (16 chars) for each: ___."

If anything fails verification, list the divergence with line numbers and fix before export.

## Deliverable

Same shape as round 6 — three artifacts:
- `index.html` — DesignCanvas driver, 5 sections (`01 Homepage`, `02 Collection · category`, `03 Collection`, `04 Landing · OECM`, `05 PDP · unbuyable`), with artboards `pd-1440`, `pd-375`, and `pd-audits` for the new section. Mirror the round-6 `index.html` pattern exactly. Sanity-check artboard heights against your final render before exporting.
- `BBI Templates Bundle.html` — single self-contained 5-section standalone, all CSS + JSX inlined. Round-6 pattern: project assets inlined, React/ReactDOM/Babel UMDs stay as `<script src>` to unpkg.com with their existing SHA integrity hashes.
- `Template 5 - PDP (unbuyable).html` — isolated review file (the PDP page only + audits, mirrors `Template 4 - Landing (OECM).html` shape).

Plus `src/*` with:
- `ProductDetail.jsx` (the page component, accepts `data` prop with `IBEX_DEFAULTS` or similar; `<ProductDetail />` no-prop renders the canonical Ibex unbuyable page)
- `pdp.css` (template-scoped patterns, `pd-*` prefix)
- `Audits.jsx` extended with the `product` slice
- All 11 prior locked files byte-identical to the round-7 attached versions

---

## Files attached (drop all 18 into the new conversation)

| # | File | Purpose |
|---|---|---|
| 1 | `01-LOCKED-templates-1-4-standalone.html` | Visual + code reference for all four locked templates |
| 2 | `02-LOCKED-Homepage.jsx` | Homepage source — locked, do not edit |
| 3 | `03-LOCKED-CollectionCategory.jsx` | Collection-category source — locked, do not edit |
| 4 | `04-LOCKED-Collection.jsx` | Collection source — locked, do not edit |
| 5 | `05-LOCKED-Landing.jsx` | Landing source — locked, do not edit; study the data-prop pattern (`OECM_DEFAULTS` + present/absent toggles) |
| 6 | `06-tokens.css` | v1 tokens — extend, do not rewrite |
| 7 | `07-bbi-components.css` | Phase-2 components — locked |
| 8 | `08-homepage.css` | Homepage CSS — locked |
| 9 | `09-collection-category.css` | Template-2 CSS — locked, study the `cc-*` pattern |
| 10 | `10-collection.css` | Template-3 CSS — locked, study the `cn-*` pattern |
| 11 | `11-landing.css` | Template-4 CSS — locked, study the `lp-*` pattern (closest analogue for `pd-*`) |
| 12 | `12-audits.css` | Audit-panel atoms (`ap-*`) — locked |
| 13 | `13-LOCKED-Audits.jsx` | Audit registry — extend, do not rewrite. Open this and name the 4 existing registry keys before appending. |
| 14 | `14-bbi-component-spec-v1.md` | Phase-2 component spec |
| 15 | `15-design-system-brief.md` | Original constraint brief |
| 16 | `16-bbi-logo-v2.png` | Logo asset |
| 17 | `17-ANTI-REF-homepage.png` | Anti-pattern: do NOT design like this |
| 18 | `18-ANTI-REF-nav.png` | Anti-pattern: do NOT design like this |
