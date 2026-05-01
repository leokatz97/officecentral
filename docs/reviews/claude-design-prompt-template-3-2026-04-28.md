# Claude Design — Phase 3 / Round 4: Template 3 (collection)

**Prototype name:** `4 — collection`
**Conversation:** fresh (do NOT continue any previous conversation)
**Attachments:** the 12 files in `data/design-photos/round4-template-3-attachments/`, listed at the end of this prompt
**Paste from the line below.**

---

You're picking up where round 3 left off. Templates 1 (homepage) and 2 (collection · category) are both locked — attached as `01-LOCKED-templates-1-2-standalone.html` plus their source files (`Homepage.jsx`, `CollectionCategory.jsx`, and the four CSS files) for code reference. **Open the locked standalone in a browser before designing.** It's the canonical visual + system reference. You'll see two sections in the design canvas:
- `01 — Homepage (locked)` — desktop 1440 + mobile 375 + audit panels
- `02 — Collection · category (locked)` — same shape

Add `03 — Collection (locked)` as your new section.

This is a fresh conversation, so the locked-system inheritance is restated in full below.

## Inheritance from rounds 1–3

- **Tokens:** v1 set including `--warningBackground: #E8A317;` (approved 2026-04-27). No new tokens. No renames.
- **Components:** Phase-2 patterns from `bbi-components.css` — `.bbi-btn`, `.bbi-badge`, `.bbi-card` (product / collection), `.bbi-section`, `.bbi-section-head`, `.bbi-cta-section`, `.bbi-crumbs`, header, footer (always `.scheme-inverse`). Compose only.
- **Schemes:** scheme-default unless explicitly inverse (CTA closer, footer).
- **Template-scoping pattern:** template-2 introduced the `cc-*` prefix in `collection-category.css`. Use the same pattern for template 3 — prefix `cn-*` (collection) — in a new `collection.css` file. Don't touch `bbi-components.css` unless you can demonstrate a system-wide need (and even then, ask first).
- **Footer separator pattern:** `.cc-page .bbi-footer { border-top: 1px solid var(--borderColor); }` solves the back-to-back inverse problem on template 2. Use the equivalent `.cn-page .bbi-footer { ... }` rule on template 3.
- **Positioning:** Two buyer paths in parallel — transactional (catalogue) and project (RFQ). OECM is the institutional differentiator. Mississauga = HQ only (footer plate); Ontario = market.

## What template 3 is

A single collection page — for example `/collections/seating`. NOT the catalogue hub (that's template 2). This page shows actual products inside one category, with filters, sort, pagination, and brand sub-navigation.

The audit cross-links from round 3 already name template 3 as the destination of every category tile on the homepage shop-entry banner and on template 2's 9-category grid.

For this round, design `Seating` as the canonical example. The pattern should generalize — anything you build must work for `Desks & Workstations`, `Storage & Filing`, etc., without structural rewrites (just data swaps).

## Page structure (strawman — adjust if a better composition emerges, but confirm in chat first)

1. Header (locked, reuse).
2. Breadcrumbs — `Home / Shop / Seating`.
3. Page intro band (smaller and tighter than template-2's intro):
   - Eyebrow: `Collection`
   - H1: `Seating`
   - Standfirst: 1–2 sentences positioning this category. Example for seating: `Task chairs, stacking, lounge, and 24/7 industrial — 120+ models across 12 brands. All Canadian-made tier carry a 12-year warranty; we file the claim.`
   - Optional small "what's inside" summary (model count, brand count, warranty headline).
4. **Filter bar** — facet filters relevant to the category. For seating: Sub-category (Task / Stacking / Lounge / Conference / 24/7), Brand, Height range, Fabric tier, Warranty length, Canadian-made toggle. Place above the grid as a horizontal bar (preferred for catalogue scanning) OR as a left sidebar (acceptable, but mobile must stack). Both filter chips and current sort must be readable at a glance.
5. **Sort + result count** — a one-line strip: `Showing 24 of 120 models · Sort by: Featured ▾`. Integrates with the filter bar.
6. **Product grid** — reuse `.bbi-card--product` from `bbi-components.css`. 3-up at 1440 desktop, 2-up at 768–1023, 1-up below. Each card shows: 16:9 image placeholder, brand mono-eyebrow, title, badges (Canadian-owned · OEM-ships if applicable), and primary CTA. CTA is `Request a quote` for showcase products and `Add to cart` for buyable products — make the badge/CTA pair data-driven so it generalizes per the BBI rule that unbuyable items still get pages.
7. **Pagination** — bottom of grid. Numeric pagination preferred over infinite scroll for a B2B catalogue. Include current page indicator and "showing X–Y of Z" microcopy.
8. **Sub-category quick-links** (optional but recommended) — a strip below the grid: `Browse by chair type: Task · Stacking · Lounge · Conference · 24/7`. Hard-link each to a filtered URL so it's a real navigation aid, not just decoration.
9. **Brand strip (this category only)** — 4–8 logo placeholders or text-list of the brands carried in this category. Use the tier classifications from template 2 (Premium · Canadian-made · Specialist) so the visual language is consistent.
10. **OECM bar** — reuse the homepage / template 2 component verbatim, same target.
11. **Bottom CTA closer** — `.bbi-cta-section.scheme-inverse` with category-aware copy:
    - Eyebrow: `Quoting in volume`
    - Heading: `Outfitting a whole floor of seating?`
    - Sub: `100+ chairs, mixed brands, OECM paperwork, install. Same Ontario team. We respond within 1 business day.`
    - Primary CTA: `Request a quote`
    - Trust line: phone fallback.
12. Footer (locked, reuse, with the `.cn-page .bbi-footer { border-top: 1px solid var(--borderColor); }` separator rule per template-3 scope).

## Constraints

- **No new tokens.** Full v1 set is in `04-tokens.css`. `--warningBackground` already covers low-stock states.
- **No new bbi-* components in `bbi-components.css`.** Template-scoped classes go in a new `collection.css` file with `cn-*` prefix.
- **Token discipline.** No new hardcoded hex literals. Defended literals from rounds 1–3 carry over (badge label whites, placeholder texture alphas, the two `rgba(255,255,255,0.85)` overlay whites in collection-category.css). Each defended literal needs a one-line comment.
- **Red density 5–8% at rest** — same target as previous rounds. Audit must measure it.
- **Brand voice — match templates 1 + 2.** Plainspoken, B2B-savvy, both buyer paths in view, no fluff. Examples already in the locked files: `"Three workhorse models we quote weekly."` · `"Five sectors. One Ontario partner."` · `"30+ brands. Three tiers. One Ontario partner."` · `"Order what you need today, or hand us the floor plan."`
- **Don't change:** tokens, components, scheme rules, header, footer, OECM bar copy, the 5 canonical sectors, the 9-category list, the brand-tier classification, dual-buyer positioning, audit panel structure (`ap-*` atoms in audits.css), DesignCanvas wrapper. Lock includes `Homepage.jsx`, `CollectionCategory.jsx`, `tokens.css`, `bbi-components.css`, `homepage.css`, `collection-category.css`.

## Audit panels — same four, same shape, same `ap-*` atoms

Use the `ap-*` audit-panel atoms from the locked `audits.css`. Extend the existing `Audits` component to add a `template="collection"` slice (don't replace — round 3 fixed this; keep the registry pattern). Specific to template 3:

- **Contrast** — every text/bg pair on this template, measured at the rendered cascade.
- **Red density** — at rest, with a one-hover delta. Target 5–8%.
- **Token coverage** — exercised + reserve.
- **Cross-links** — every link surface resolves to a real route. Up to `/`, sideways to `/collections/business-furniture` (template 2), down to PDP (template 5, future), down to brand pages (template 4, future), `/pages/industries/{slug}`, OECM bar, RFQ, phone CTA mandatory.

## Reply contract — non-negotiable this round

Before you design, **confirm in chat** (three or four sentences, in chat, not in code comments):

1. The strawman page structure — agreed, or what you'd shift and why.
2. Filter UI choice — horizontal bar (above grid) or left sidebar.
3. Whether template 3 needs any addition to `bbi-components.css` (it shouldn't).
4. Audit registry pattern — how you'll extend `Audits` to add the `template="collection"` slice without dropping the homepage and collection-category slices.

Wait for my reply before exporting. Round 3's first delivery skipped this and we ate two extra rounds correcting things that should have been resolved in chat.

## Bundle verification — also non-negotiable this round

Before you export the standalone, verify **the standalone bundle itself**, not just the source files. Round 3 shipped with the source files byte-identical to the lock but the homepage CSS dropped from the bundle's inline `<style>` blocks, which broke the homepage render inside the canvas.

Verification target: open the new standalone, count its inline `<style>` blocks, and confirm they include — in order — fonts, tokens.css, bbi-components.css, homepage.css, collection-category.css, **collection.css (new)**, audits.css. Seven blocks. State this in chat before exporting:

> "Standalone bundle verified: 7 inline `<style>` blocks present in order [fonts · tokens · bbi-components · homepage · collection-category · collection · audits]. `.hp-*`, `.cc-*`, and `.cn-*` rules all present in their respective blocks. SHA-256 (16 chars) for source files: Homepage.jsx ___, CollectionCategory.jsx ___, tokens.css ___, bbi-components.css ___, homepage.css ___, collection-category.css ___ — all match the locks."

If anything fails verification, list the divergence with line numbers and fix before export.

## Deliverable

Same shape as round 3:
- `Collection.jsx` (the page component)
- `collection.css` (template-scoped patterns, `cn-*` prefix)
- `Audits.jsx` extended with the `template="collection"` slice
- `index.html` driving DesignCanvas — add `03 — Collection (locked)` section with artboards `cn-1440`, `cn-375`, and `cn-audits`
- Standalone HTML bundle that contains all 7 inline `<style>` blocks verified above
- Zip with all source files + the standalone

---

## Files attached (drop all 12 into the new conversation)

| # | File | Purpose |
|---|---|---|
| 1 | `01-LOCKED-templates-1-2-standalone.html` | Visual + code reference for both locked templates |
| 2 | `02-LOCKED-Homepage.jsx` | Homepage source — locked, do not edit |
| 3 | `03-LOCKED-CollectionCategory.jsx` | Collection-category source — locked, do not edit |
| 4 | `04-tokens.css` | v1 tokens — extend, do not rewrite |
| 5 | `05-bbi-components.css` | Phase-2 components — locked |
| 6 | `06-homepage.css` | Homepage CSS — locked |
| 7 | `07-collection-category.css` | Template-2 CSS — locked, study the `cc-*` pattern |
| 8 | `08-bbi-component-spec-v1.md` | Phase-2 component spec |
| 9 | `09-design-system-brief.md` | Original constraint brief |
| 10 | `10-bbi-logo-v2.png` | Logo asset |
| 11 | `11-ANTI-REF-homepage.png` | Anti-pattern: do NOT design like this |
| 12 | `12-ANTI-REF-nav.png` | Anti-pattern: do NOT design like this |
