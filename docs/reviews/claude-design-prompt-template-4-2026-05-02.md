# Claude Design — Phase 3 / Round 5: Template 4 (Landing page — OECM)

**Prototype name:** `5 — landing`
**Conversation:** fresh (do NOT continue any previous conversation)
**Attachments:** the 16 files in `data/design-photos/round5-template-4-attachments/`, listed at the end of this prompt
**Paste from the line below.**

---

You're picking up where round 4 left off. Templates 1 (Homepage), 2 (Collection · Category), and 3 (Collection / sub-collection) are all locked — attached as `01-LOCKED-templates-1-3-standalone.html` plus their source files (`Homepage.jsx`, `CollectionCategory.jsx`, `Collection.jsx`, `Audits.jsx`, and the five CSS files) for code reference. **Open the locked standalone in a browser before designing.** It's the canonical visual + system reference. You'll see three sections in the design canvas:
- `01 — Homepage (locked)` — desktop 1440 + mobile 375 + audit panels
- `02 — Collection · category (locked)` — same shape
- `03 — Collection (locked)` — same shape

Add `04 — Landing · OECM (locked)` as your new section.

This is a fresh conversation, so the locked-system inheritance is restated in full below.

## Inheritance from rounds 1–4

- **Tokens:** v1 set including `--warningBackground: #E8A317;` (approved 2026-04-27). No new tokens. No renames.
- **Components:** Phase-2 patterns from `bbi-components.css` — `.bbi-btn`, `.bbi-badge`, `.bbi-card` (product / collection), `.bbi-section`, `.bbi-section-head`, `.bbi-cta-section`, `.bbi-crumbs`, header, footer (always `.scheme-inverse`). Compose only.
- **Schemes:** scheme-default unless explicitly inverse (CTA closer, footer).
- **Template-scoping pattern:** template-2 introduced `cc-*` (collection-category.css). Template-3 introduced `cn-*` (collection.css). Use the same pattern for template 4 — prefix `lp-*` (landing) — in a new `landing.css` file. Don't touch `bbi-components.css` unless you can demonstrate a system-wide need (and even then, ask first).
- **Footer separator pattern:** `.lp-page .bbi-footer { border-top: 1px solid var(--borderColor); }` solves the back-to-back inverse problem (same fix template 2 and 3 use).
- **Positioning:** Two buyer paths in parallel — transactional (catalogue) and project (RFQ). OECM is the institutional differentiator. Mississauga = HQ only (footer plate); Ontario = market.

## What template 4 is

A single landing page — for example `/pages/oecm`. This template gets reused for ~20 pages across four families:
- **Industries** (6): hub + Healthcare, Education, Government, Non-Profit, Professional Services
- **Brands** (4): hub + Keilhauer, Global/Teknion, ergoCentric
- **Services** (4): Design Services, Delivery & Installation, Relocation Management, OECM Procurement
- **About & Trust** (~7): About, Our Work, Customer Stories, Request a Quote, FAQ, Contact, plus the FAQ-schema variant

For this round, design the **OECM page** (`/pages/oecm`) as the canonical example. It's the highest-priority instance of the template (Phase 1 build per [`docs/plan/site-architecture-2026-04-25.md`](../plan/site-architecture-2026-04-25.md) §5) and exercises the hardest copy: institutional procurement positioning, "Verified OECM supplier" trust block, cross-links into Business Furniture and the Quote page.

The pattern must generalize — anything you build must work for `/pages/healthcare`, `/pages/brands-keilhauer`, `/pages/design-services`, `/pages/about` without structural rewrites (just data swaps + an FAQ-accordion variant).

## OECM context (so your copy isn't generic)

**OECM = Ontario Education Collaborative Marketplace.** A non-profit central buying group for Ontario's broader public sector — school boards, colleges, universities, hospitals, municipalities, social-service agencies. BBI is a **verified OECM supplier** for office furniture. Practical impact for the buyer: Ontario institutions can purchase from BBI **without running an open tender** (the OECM agreement is the tender). That cuts months off procurement and is the single biggest reason an OPS buyer chooses BBI over a generic dealer.

OECM positioning anywhere in BBI copy: **quiet, factual, institutional.** Never sale-tag loud. The audience is procurement officers, not consumers — they recognize "verified supplier" and "no open tender required" as competitive language; they read past it if it's hyped.

Locked phrases already in use (do not paraphrase, reuse verbatim):
- Homepage OECM bar: `"Verified OECM supplier. Ontario institutions can purchase without open tender."`
- Footer plate: `"Mississauga, Ontario · Since 1962"`
- Industries headline pattern: `"Five sectors. One Ontario partner."`

## Page structure (strawman — adjust if a better composition emerges, but confirm in chat first)

1. Header (locked, reuse).
2. Breadcrumbs — `Home / Services / OECM Procurement`.
3. **Hero band** — eyebrow `Service`, H1 `OECM Procurement — purchase without open tender`, standfirst (1–2 sentences positioning OECM for the procurement officer audience), primary CTA `Request a quote`, secondary outline CTA `Call 1-800-835-9565`. Hero image slot at right (16:9, AI-generated institutional/government interior — placeholder for now). Quiet OECM badge inline near the H1, not pinned to a corner. **Anti-pattern:** giant hero photo with red overlay — Steve hates the beige + dramatic-photo combo.
4. **Intro / what-it-is band** — 2–3 short paragraphs in a single column (max-width ~640px), explaining what OECM is, who's eligible, and what changes for the buyer. End with a single inline link `See the full OECM agreement details →` (placeholder href, no real link yet — Steve will supply the OECM PDF). This is the band that has to read like a procurement memo, not a sales page.
5. **Differentiator cards** — 3–4 cards in a grid (2×2 at 1440 desktop, 1-up at mobile). Each card = icon + 3–5 word label + one-sentence proof. Strawman content:
    - `Verified supplier` — `BBI is on the OECM agreement for office furniture; no separate vendor approval needed.`
    - `No open tender required` — `Use the OECM contract as your tender of record. Skip months of RFP cycles.`
    - `Single Ontario partner` — `Quoted, delivered, and installed by the same Ontario team since 1962.`
    - `Brand range covered` — `30+ brands across seating, desks, storage, ergonomics — all OECM-eligible.`
    Cards reuse `.bbi-card`-family tokens but get their own `lp-diff-card` skin (no image, icon-led).
6. **Trust block / project photos** — a row of 3–4 institutional project photos (placeholders for now, real photos from `data/oci-photos/` later). Each photo gets a one-line caption: `Mattamy Homes · 2023 · 4-floor relocation, 600+ workstations`. The captions are the trust signal, not the photos themselves — photos are stock-feeling without the data.
7. **Proof bar** — single horizontal band: `60+ years · 30+ brands · 1,000+ Ontario institutions served`. Quiet, not pinned-to-corner-loud. Use the same scheme as the homepage OECM trust bar (subtle-tinted, not full-inverse).
8. **Cross-links to relevant collections** — a 3-tile strip directing the procurement reader into product browsing: `Shop seating →` `Shop desks →` `Shop storage →`. Each tile is text-led with a small icon; no product imagery (we don't want this band to compete with the differentiator cards above). Hard-link each to `/collections/seating`, `/collections/desks`, `/collections/storage`.
9. **FAQ-variant slot** — for OECM specifically, include 4–6 FAQ items in an accordion (closed by default). Strawman questions:
    - `Who can buy from BBI under the OECM agreement?`
    - `Do I still need to issue a PO?`
    - `Does the OECM agreement cover delivery and installation?`
    - `What payment terms are available — NET 30, credit account?`
    - `How do I confirm BBI is the right OECM supplier for my project?`
    Build the accordion as `lp-faq-*` so the same component slots into `/pages/faq` later (where it'll get JSON-LD schema markup added in the Liquid template). For this round, just render the visual — schema markup is a Liquid concern, not a design concern.
10. **OECM bar** — reuse the homepage / template 2 / template 3 component verbatim, same target. (Yes, on the OECM page itself — it's the same trust signal, surfaced at the conversion-decision point.)
11. **Bottom CTA closer** — `.bbi-cta-section.scheme-inverse` with OECM-specific copy:
    - Eyebrow: `Quoting under OECM`
    - Heading: `Outfitting a public-sector floor?`
    - Sub: `OECM agreement covers it. We handle the paperwork, the install, the warranty. Same Ontario team since 1962. We respond within 1 business day.`
    - Primary CTA: `Request a quote`
    - Trust line: phone fallback `or call 1-800-835-9565`
12. Footer (locked, reuse, with the `.lp-page .bbi-footer { border-top: 1px solid var(--borderColor); }` separator rule per template-4 scope).

## Constraints

- **No new tokens.** Full v1 set is in `05-tokens.css`.
- **No new bbi-* components in `bbi-components.css`.** Template-scoped classes go in a new `landing.css` file with `lp-*` prefix.
- **Token discipline.** No new hardcoded hex literals. Defended literals from rounds 1–4 carry over (badge label whites, placeholder texture alphas, the two `rgba(255,255,255,0.85)` overlay whites in collection-category.css, the `.cn-product__badges` background overrides). Each defended literal in `landing.css` needs a one-line comment.
- **Red density 5–8% at rest** — same target as previous rounds. Audit must measure it. Watch the differentiator-card grid and the FAQ accordion — both can over-red if every label gets a chip.
- **FAQ accordion = visual only.** No JSON-LD schema markup in the JSX (that's a Liquid template concern in production). Just the open/close behaviour and the typography.
- **Brand voice — match templates 1, 2, 3.** Plainspoken, B2B-savvy, both buyer paths in view, no fluff. Examples already in the locked files: `"Three workhorse models we quote weekly."` · `"Five sectors. One Ontario partner."` · `"30+ brands. Three tiers. One Ontario partner."` · `"Order what you need today, or hand us the floor plan."`
- **Don't change:** tokens, components, scheme rules, header, footer, OECM bar copy, the 5 canonical sectors, the 9-category list, the brand-tier classification, dual-buyer positioning, audit panel structure (`ap-*` atoms in audits.css), DesignCanvas wrapper. Lock includes `Homepage.jsx`, `CollectionCategory.jsx`, `Collection.jsx`, `Audits.jsx`, `tokens.css`, `bbi-components.css`, `homepage.css`, `collection-category.css`, `collection.css`, `audits.css`.

## Audit panels — same four, same shape, same `ap-*` atoms

Use the `ap-*` audit-panel atoms from the locked `audits.css`. Extend the existing `Audits` component to add a `template="landing"` slice (don't replace — round 3 fixed the registry pattern; keep it). Specific to template 4:

- **Contrast** — every text/bg pair on this template, measured at the rendered cascade. Pay attention to the FAQ accordion's expanded state and any tinted differentiator-card backgrounds.
- **Red density** — at rest, with a one-hover delta. Target 5–8%. The CTA closer + breadcrumbs + diff-card chips + FAQ chevrons all add up — measure carefully.
- **Token coverage** — exercised + reserve.
- **Cross-links** — every link surface resolves to a real route. Up to `/`, sideways to `/pages/services` (hub, future), down to `/collections/seating`, `/collections/desks`, `/collections/storage` (template 3, locked), `/pages/quote` (CTA target, future), phone CTA mandatory. Also confirm the OECM bar links to `/pages/oecm` itself (self-link is fine on the OECM page — the bar appears site-wide and the link target is OECM).

## Reply contract — non-negotiable this round

Before you design, **confirm in chat** (three or four sentences, in chat, not in code comments):

1. The strawman page structure — agreed, or what you'd shift and why. Specifically: do you want the FAQ slot mid-page (as positioned) or as the second-last section before the CTA closer?
2. Differentiator-card visual treatment — icon + label + sentence in a 2×2 grid, or do you propose a different composition (e.g., a 3-up row with a wider middle "anchor" card)?
3. Whether template 4 needs any addition to `bbi-components.css` (it shouldn't — `.bbi-card` should skin into a `lp-diff-card` variant in `landing.css`).
4. Audit registry pattern — how you'll extend `Audits` to add the `template="landing"` slice without dropping the homepage / collection-category / collection slices.
5. **Generalization check** — name the 2–3 places where the OECM-specific copy will need a slot/prop so the same template renders cleanly for `/pages/healthcare` (industry variant) and `/pages/brands-keilhauer` (brand variant). I want to see you've thought about reuse before you build the OECM render.

Wait for my reply before exporting. Round 3's first delivery skipped this and we ate two extra rounds correcting things that should have been resolved in chat.

## Bundle verification — also non-negotiable this round

Before you export the standalone, verify **the standalone bundle itself**, not just the source files. Round 3 shipped with the source files byte-identical to the lock but the homepage CSS dropped from the bundle, which broke the homepage render inside the canvas. Round 4 caught the bundle-vs-source divergence early — keep that discipline.

Verification target: open the new standalone in a browser, scroll through all four sections in DesignCanvas, and confirm every section renders with no missing styles, no unstyled flash-of-content, no broken layout. Specifically check that the three previously locked sections (`01 Homepage`, `02 Collection · category`, `03 Collection`) render byte-equivalent to the attached `01-LOCKED-templates-1-3-standalone.html` — the new bundle should add `04 Landing · OECM` without altering any rule that affects 01–03. State this in chat before exporting:

> "Standalone bundle verified: opens cleanly in a browser, all 4 DesignCanvas sections (`01 Homepage`, `02 Collection · category`, `03 Collection`, `04 Landing · OECM`) render with no missing styles. CSS present in the bundle: tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, **landing.css (new)**, audits.css. `.hp-*`, `.cc-*`, `.cn-*`, and `.lp-*` rules all present and scoped to their respective sections (no `.lp-*` rule leaks into 01–03). Source files byte-identical to the locked versions attached: Homepage.jsx, CollectionCategory.jsx, Collection.jsx, Audits.jsx (extended only by adding the `landing` slice — homepage/collection-category/collection slices unchanged), tokens.css, bbi-components.css, homepage.css, collection-category.css, collection.css, audits.css. SHA-256 (16 chars) for each: ___."

If anything fails verification, list the divergence with line numbers and fix before export.

## Deliverable

Same shape as round 4:
- `Landing.jsx` (the page component)
- `landing.css` (template-scoped patterns, `lp-*` prefix)
- `Audits.jsx` extended with the `template="landing"` slice
- `index.html` driving DesignCanvas — add `04 — Landing · OECM (locked)` section with artboards `lp-1440`, `lp-375`, and `lp-audits`. Sanity-check the artboard heights against your final render before exporting (round 3's cc-1440 was under-sized by ~190px; we don't want a repeat).
- Standalone HTML bundle that contains all 8 inline `<style>` blocks verified above
- Zip with all source files + the standalone

---

## Files attached (drop all 16 into the new conversation)

| # | File | Purpose |
|---|---|---|
| 1 | `01-LOCKED-templates-1-3-standalone.html` | Visual + code reference for all three locked templates |
| 2 | `02-LOCKED-Homepage.jsx` | Homepage source — locked, do not edit |
| 3 | `03-LOCKED-CollectionCategory.jsx` | Collection-category source — locked, do not edit |
| 4 | `04-LOCKED-Collection.jsx` | Collection source — locked, do not edit; study the `cn-*` pattern |
| 5 | `05-tokens.css` | v1 tokens — extend, do not rewrite |
| 6 | `06-bbi-components.css` | Phase-2 components — locked |
| 7 | `07-homepage.css` | Homepage CSS — locked |
| 8 | `08-collection-category.css` | Template-2 CSS — locked, study the `cc-*` pattern |
| 9 | `09-collection.css` | Template-3 CSS — locked, study the `cn-*` pattern (closest analogue for `lp-*`) |
| 10 | `10-audits.css` | Audit-panel atoms (`ap-*`) — locked |
| 11 | `11-LOCKED-Audits.jsx` | Audit registry — extend, do not rewrite |
| 12 | `12-bbi-component-spec-v1.md` | Phase-2 component spec |
| 13 | `13-design-system-brief.md` | Original constraint brief |
| 14 | `14-bbi-logo-v2.png` | Logo asset |
| 15 | `15-ANTI-REF-homepage.png` | Anti-pattern: do NOT design like this |
| 16 | `16-ANTI-REF-nav.png` | Anti-pattern: do NOT design like this |
