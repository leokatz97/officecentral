# Claude Design — Phase 3 / Round 3: Template 2 (collection.category)

**Prototype name:** `3 — collection.category`
**Conversation:** fresh (do NOT continue the homepage conversation)
**Attachments:** the 9 files in `data/design-photos/round3-template-2-attachments/`, listed at the end of this prompt
**Paste from the line below.**

---

You're picking up where round 2 left off. The homepage (template 1) is locked — attached as `01-LOCKED-homepage-standalone.html` plus its source files (Homepage.jsx, tokens.css, bbi-components.css) for code reference. Read them once before designing — they are the canonical visual + system reference for everything that follows.

This is a fresh conversation, so the locked-system inheritance is restated in full below.

## Inheritance from rounds 1–2

- **Tokens:** v1 set including `--warningBackground: #E8A317;` (approved 2026-04-27) and its `-rgb` pair. No new tokens. No renames.
- **Components:** Phase-2 patterns from `bbi-components.css` — `.bbi-btn` (primary / secondary / tertiary, with `--sm` `--lg` `--full`), `.bbi-badge` (sale / new / canadian / oem / oecm), `.bbi-card` (product / collection), `.bbi-section`, `.bbi-section-head`, `.bbi-cta-section` (defined and ready for templates 2/4/5 to consume), `.bbi-crumbs`, header, footer (always `.scheme-inverse`). Compose only.
- **Schemes:** scheme-default unless a section explicitly calls for `.scheme-inverse` (CTA closer, footer).
- **Positioning:** Two buyer paths in parallel — transactional (catalogue) and project (RFQ). OECM stays the institutional differentiator. Mississauga = HQ only (footer plate); Ontario = market.

## What template 2 is

`/collections/business-furniture` — the shop hub. Index page that fans out to specific collection pages (template 3). Both `Header → Shop` and `Shop entry → Browse all` from the homepage resolve here per the round-2 cross-link audit.

This is NOT a single collection — no facet filters, no product grid for one category. This page is the **catalogue map**: nine categories, the brands behind them, and the institutional shortcut.

## Page structure (strawman — adjust if a better composition emerges)

1. Header (locked, reuse).
2. Breadcrumbs — `Home / Shop`.
3. Page intro band —
   - Eyebrow: `Shop the catalogue`
   - H1: `Business furniture, every category.`
   - Standfirst: `9 categories from seating to quiet rooms — Steelcase, Allsteel, ergoCentric, Global, AMQ, and 30+ more brands.`
   - Subline mirroring the hero positioning: `Order direct from any collection, or request a quote on a full fit-out.`
4. **9-category grid** — the canonical list (already in the homepage footer's "Shop Furniture" column):
   Seating · Desks & Workstations · Storage & Filing · Tables · Boardroom · Ergonomic Products · Panels & Dividers · Accessories · Quiet Spaces.
   3-up on desktop (3×3), 2-up on mobile. Reuse `.bbi-card--collection` from the homepage. Each tile: image placeholder + title + model count + 3-word descriptor.
5. **Brand strip / index** — surface the 30+ brands. Two reasonable compositions; pick whichever holds <8% red density:
   (a) tiered list (Premium · Canadian-made · Specialist), or
   (b) text-list logo wall with category labels.
6. **Industry shortcut row** — for institutional buyers who'd rather skip the catalogue and route by sector. Five canonical sectors (Office & Corporate · Healthcare · Education · Government · Industrial), compact tile pattern, links to `/pages/industries/{slug}`. Red density budget: zero.
7. **OECM bar** — reuse the homepage component verbatim. Same copy, same target.
8. **Bottom CTA section** — `.bbi-cta-section` with dual-path framing. Suggested copy:
   - Eyebrow: `Two ways to buy`
   - Heading: `Order what you need today, or hand us the floor plan.`
   - Sub: `Same Ontario team, same warehouse, same brands either way.`
   - Primary CTA: `Request a quote`
   - Trust line: 1-business-day response + phone fallback.
9. Footer (locked, reuse).

## Constraints

- **No new tokens.** Full v1 set is in `03-tokens.css`.
- **No invented components in `bbi-components.css`.** If template 2 demonstrably needs a new pattern (e.g. a brand-strip), add it as a *template-scoped* class in a new `collection-category.css` file, never in `bbi-components.css`.
- **Token discipline.** No new hardcoded hex literals. Only the defended literals from round 2 carry over: badge label whites (`#fff` on `.bbi-badge--sale/--new`), placeholder texture alphas on `.bbi-ph`. Each defended literal needs a one-line comment.
- **Red density 5–8% at rest** — same target as homepage. Audit must measure it.
- **Brand voice — match the homepage.** Plainspoken, B2B-savvy, both buyer paths in view, no fluff. Examples already in the locked file: `"Three workhorse models we quote weekly."` · `"Five sectors. One Ontario partner."` · `"Commercial furniture, sold or installed. Ontario since 1962."`
- **Don't change:** tokens, components, scheme rules, header, footer, OECM bar copy, the 5 canonical sectors, the 9-category list, dual-buyer positioning, audit panel structure, DesignCanvas wrapper.

## Audit panels — same four, same shape

Mirror round 2's Audits.jsx structure: Contrast · Red density · Token coverage · Cross-links. Specific to template 2:

- **Contrast** — every text/bg pair on this template. Values must reflect the rendered cascade, not the spec.
- **Red density** — measured at rest, with a one-hover delta. Target 5–8%.
- **Token coverage** — list every token this template exercises and what it lights up. Reserve list for tokens defined but unused on this screen.
- **Cross-links** — every link surface resolves to a real route. Up to `/`, sideways to `/collections/{slug}` (template 3), down to `/pages/industries/{slug}`, the OECM bar to `/pages/oecm`, RFQ to `/pages/quote`, phone CTA mandatory.

## Deliverable

Same shape as round 2:
- `CollectionCategory.jsx` (the page component)
- `collection-category.css` (only if template-scoped patterns are needed)
- Patches to `tokens.css` and `bbi-components.css` ONLY if you've justified an addition
- `Audits.jsx` extended with this template's pairs
- `index.html` driving DesignCanvas — add a section `02 — Collection · category` with artboards `cc-1440` and `cc-375`, plus an audit-panels artboard
- Standalone HTML bundle (same format as round 2)

Same DesignCanvas wrapper. Same artboard naming convention.

## Reply contract

Before you design, confirm in chat:
1. The strawman page structure — agreed, or what you'd shift and why.
2. Whether template 2 needs any addition to `bbi-components.css` or whether everything composes from existing patterns.
3. Whether you intend brand-strip composition (a) or (b) — or something better.

Then export.

---

## Files attached (drop all 9 into the new conversation)

| # | File | Purpose |
|---|---|---|
| 1 | `01-LOCKED-homepage-standalone.html` | Visual + code reference for the locked homepage |
| 2 | `02-LOCKED-Homepage.jsx` | Homepage source for direct code reading |
| 3 | `03-tokens.css` | v1 tokens — extend, do not rewrite |
| 4 | `04-bbi-components.css` | Phase-2 components — extend, do not rewrite |
| 5 | `05-bbi-component-spec-v1.md` | Phase-2 component spec |
| 6 | `06-design-system-brief.md` | Original constraint brief |
| 7 | `07-bbi-logo-v2.png` | Logo asset |
| 8 | `08-ANTI-REF-homepage.png` | Anti-pattern: do NOT design like this |
| 9 | `09-ANTI-REF-nav.png` | Anti-pattern: do NOT design like this |
