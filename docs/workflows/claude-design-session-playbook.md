# Claude Design Session Playbook — BBI Design System Rebuild

**Goal:** Run three sequential Claude Design chats (Tokens → Components → Screens) in ≤6 prompts each. Pull every output back into **BBI Landing Dev** (`theme/186373570873`). No code refactor required for tokens — the audit confirms it's a settings-configuration job.

**Locked anchors (from [`docs/strategy/design-system.md`](../strategy/design-system.md) — do not relitigate in any chat):**
- Brand red `#D4252A` (logo "BASICS" + vertical rule)
- Brand charcoal `#0B0B0C` (logo "Brant" + "BUSINESS INTERIORS")
- Brand white `#FFFFFF` (canvas)
- Surface tier `#FAFAFA` (warmer than that = banned)
- `red-surface` = `#D4252A` exact (buttons/banners/badges); `red-text` = darker variant ~`#A81E22` TBD-test for AA on white
- Anchor neutral is **charcoal `#0B0B0C`** — NOT navy. Earlier `#1a2744` is superseded.
- No beige / tan / cream / sand. No warm tones. No dark mode. No gradients on red. No red as body link color. No red headings.
- Token names: consume `design-system.md` vocabulary as-is — do not propose new tokens.

---

## 1. Pre-flight checklist

**Theme & settings**
- [ ] Open **BBI Landing Dev** directly: [Theme Editor](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor) — this theme was built specifically for this work; no duplication needed.
- [ ] Verify `.env` has `SHOPIFY_TOKEN` (only needed if helper scripts run post-session).

**Screenshots to capture from brantbusinessinteriors.com — anti-reference only (1440px desktop)**

The new site architecture ([`docs/plan/site-architecture-2026-04-25.md`](../plan/site-architecture-2026-04-25.md)) is largely greenfield: 5-item nav, 4 page templates, ~110 pages, Shop Hub removed, Educational/Daycare/Healthcare verticals archived. **Live screenshots are anti-reference (the beige problem to fix), not layout source.** Capture only 2:

1. Homepage hero + a section or two below — shows the beige + warm-tone problem
2. Header close-up — shows the current header you're replacing

Save to `data/design-photos/baseline-2026-04-27/` and label both filenames with the prefix `ANTI-REF-`.

**Reference for the new structure** (this is what you're actually designing toward — open in a tab):
- [`docs/plan/site-architecture-2026-04-25.md`](../plan/site-architecture-2026-04-25.md) — nav structure (§1), template list (§3), homepage section order (Rule 6), interconnection rules (§4)

**Brand assets**
- [ ] [`data/logos/bbi-logo-hires.png`](../../data/logos/bbi-logo-hires.png) (cleaned hi-res mark — black "Brant" + red "BASICS" with paperclip + Canadian maple leaf accent + "BUSINESS INTERIORS" wordmark)

**Tabs to keep open while running sessions**
- claude.ai/design (one tab per phase — three total)
- [`docs/strategy/design-system.md`](../strategy/design-system.md) — canonical spec; fill TBDs as outputs land
- [`docs/strategy/design-system-brief.md`](../strategy/design-system-brief.md) — reference
- [`docs/reviews/design-system-audit-2026-04-27.md`](../reviews/design-system-audit-2026-04-27.md) — Shopify schema mapping + code hotspots
- [`docs/plan/site-architecture-2026-04-25.md`](../plan/site-architecture-2026-04-25.md) — nav, templates, page interconnection
- [BBI Landing Dev Theme Editor](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor) → Theme settings → Colors
- A contrast checker (webaim.org/resources/contrastchecker)

---

## 2. Three sequential Claude Design chats

> **Why one chat per phase:** Tokens are a numeric problem. Components are a state-matrix problem. Screens are a composition problem. Mixing them blows context and burns credits on re-grounding.

---

### Phase 1 — Tokens chat

**Attach:** `data/logos/bbi-logo-hires.png` + the 5 baseline screenshots.

**Opening message (paste verbatim):**

> I'm rebuilding the design system for **Brant Business Interiors (BBI)** — a Canadian B2B office furniture dealer on Shopify. Audience: institutional procurement (school boards, hospitals, municipalities). OECM-verified supplier (quiet trust signal). Live: brantbusinessinteriors.com
>
> **This chat = tokens only.** Components and screens come in separate chats. Don't draft components yet.
>
> **Locked anchors (from the brand mark — do not change):**
> - Brand red `#D4252A` exact for `red-surface` (buttons/banners/badges).
> - `red-text` for any red text on white — propose a darker variant (~`#A81E22`-ish) that hits AA 4.5:1 on `#FFFFFF`. State the contrast ratio.
> - Anchor neutral `#0B0B0C` charcoal for body + headings (NOT navy — earlier `#1a2744` superseded by the logo).
> - Canvas `#FFFFFF`. Surface `#FAFAFA` (warmer than that = banned).
> - **No beige / tan / cream / sand. No warm tones. No dark mode. No gradients on red. No red as body link color. No red headings.**
> - Red density 5–8% per screen. Body links default to charcoal.
>
> **Output format:** A single block of CSS custom properties using the **exact `--camelCase` token names in the Token Map below.** Two color schemes: `scheme-default` (white canvas, used 90% of pages) and `scheme-inverse` (charcoal canvas, hero/feature blocks only). For each color output `#hex` AND `r,g,b` triplet (the theme uses both for `rgba()` math). After every text/bg pair, print the contrast ratio + AA verdict.
>
> Also output, in the same message: typography scale (H0/H1/H2/H3/Body/Small/Button × mobile + desktop, heading line-height tighter than body), spacing scale (4px base: 4/8/12/16/24/32/48/64/96), radius scale (`--inputRadius`, `--buttonRadius`, `--cardRadius`, `--imageRadius`, `--productRadius` — values from {4px, 8px, pill}), shadow scale (`shadow-sm` for cards on white, `shadow-md` for modal/drawer — ≤8% opacity).
>
> **Do not propose new token names.** Use only the names below.
>
> **Per-scheme tokens (define for both `scheme-default` and `scheme-inverse`):**
> `--background, --alternateBackground, --cardBackground, --textColor, --linkColor, --headingColor, --buttonBackground, --buttonColor, --buttonBorder, --buttonBackgroundHover, --buttonColorHover, --buttonBorderHover, --alternateButtonBackground, --alternateButtonColor, --alternateButtonBorder, --alternateButtonBackgroundHover, --alternateButtonColorHover, --alternateButtonBorderHover, --inputBackground, --inputColor, --inputBorder, --productBorder, --borderColor, --ratingStarColor, --sliderArrowBackground, --sliderArrowColor, --shadowColor, --productIconColor, --productIconBg, --line-color`
>
> **Global tokens (define once):**
> `--success, --error, --saleBadgeBackground, --newBadgeBackground, --preorderBadgeBackground, --soldBadgeBackground, --customBadgeBackground, --headerBg, --headerColor, --headerHoverColor, --headerIconColor, --cartCountBg, --cartCountColor, --submenuBg, --submenuColor, --submenuHoverColor`
>
> **Typography globals:** `--bodyFont, --bodyFontWeight, --bodyFontLineHeight, --bodyFontBase, --headingFont, --headingFontWeight, --headingFontLineHeight, --headingFontBase`
>
> Attached: brand mark + 5 baseline screenshots of today's beige site.
>
> Begin with `scheme-default` per-scheme tokens + all global tokens + typography + spacing/radius/shadow scales in one message. Stop after that — I'll ask for `scheme-inverse` next.

**Stress-test follow-ups (use only if needed — each costs a credit):**
1. "Print a contrast table: every text token × every background/surface in `scheme-default`. Flag any pair < 4.5:1 for body or < 3:1 for large text."
2. "Confirm `red-surface` vs `red-text` are perceptually one color family — show me the two hexes side-by-side and the delta."
3. "Now output `scheme-inverse` with the same Token Map. Inverse canvas = charcoal anchor; red accent stays the same family."
4. "Audit: what % of pixels would be red if we used `--buttonBackground` for a 200×56px CTA on a 1440×900 hero with one badge? Confirm we're under 8%."
5. "Output sale-badge text contrast assuming Shopify's `color_brightness` filter auto-picks white-on-red — would it flip black-on-red at any of your proposed badge hexes?"

**Pass/fail gates (verify before opening Phase 2 chat):**
- [ ] Every per-scheme token has a hex + rgb triplet for both schemes
- [ ] `red-text` on `#FFFFFF` ≥ 4.5:1 (AA body)
- [ ] `--textColor` on `--background` ≥ 7:1 (AAA preferred for body)
- [ ] `--linkColor` is visually distinct from `--textColor` AND not red
- [ ] `--line-color` ≥ 3:1 on `#FFFFFF` (focus ring requirement)
- [ ] No beige/tan/warm-cream values anywhere — eyeball every neutral
- [ ] `--shadowColor` opacity ≤ 8%
- [ ] All 5 badge bg colors named with their semantic role (`--saleBadgeBackground` = brand red `#D4252A`; `--soldBadgeBackground` = gray, deemphasized; others use complementary cool tones — never warm)
- [ ] `--error` is distinct from brand red (slightly oranger or darker)

**Pushback phrases (paste if quality slips):**
- "The red-text value you proposed (`#XXXXXX`) is 4.1:1 on white — below AA 4.5:1. Push it 8–12% darker and re-check."
- "I don't see a focus ring color that contrasts on white. White-on-white focus is unacceptable. Specify `--line-color` ≥ 3:1 on `#FFFFFF`."
- "Red density on the proposed buttons exceeds 8% on a typical hero. Either shrink the CTA spec or move to outline secondary."
- "`--linkColor` and `--textColor` are the same hue family — links won't read as interactive. Underline by default or shift link to a discriminable charcoal-derived tone (NOT navy, NOT red)."
- "You proposed a new token name (`brand_accent`). I can't add tokens. Map it onto a name in the list or drop it."
- "You drifted to a beige/cream surface. Banned. Use `#FAFAFA` or `#F7F7F8` for `--cardBackground`."

---

### Phase 2 — Components chat

**Attach:** brand mark + the same 5 screenshots + the CSS block produced in Phase 1.

**Opening message (paste verbatim):**

> Continuing the BBI design system rebuild. **This chat = components only.** Tokens are locked from the previous chat (CSS attached). Don't redefine tokens. Don't draft full screens.
>
> Use only the CSS custom properties from the attached file. If a component needs a value not in the file, **stop and ask** — don't invent a new token.
>
> **Build, in this exact order, all states side-by-side, on `scheme-default` (white canvas) AND `scheme-inverse` (charcoal canvas):**
> 1. **Buttons** — primary (red surface, white text), secondary (charcoal outline, charcoal text, white bg), tertiary (text-only, charcoal). States: default, hover, focus (visible ring), active, disabled. **Disabled = 40% opacity AND grayscale** (preserves contrast — never opacity alone). Show focus ring against white explicitly.
> 2. **Form inputs** — text, select, textarea, checkbox, radio. States: default, focus (charcoal 2px ring, no fill change), error (red border + helper text), disabled.
> 3. **Cards** — basic, product card, feature card. Product card MUST have a 16:9 image slot at the top (hard project rule). White bg, 1px gray border, no shadow at rest, subtle shadow on hover.
> 4. **Badges** — sale (BBI red `#D4252A`), new, preorder, sold (gray, deemphasized), custom. Sale top-left, sold top-right (separate corner = different meaning). Verify legibility — watch the `color_brightness` flip threshold called out in the audit.
> 5. **Header** — desktop and mobile. Use the attached BBI logo. **Lockup rules: clear space ≥ half the height of "B" in "Brant" on all sides; min 120px wide; never on red; never on photo without white plate; never recolored; never reflowed to stacked.**
>    - **Desktop layout (left → right):** `[Logo]  Shop Furniture ▾  Industries ▾  Brands ▾  Services ▾  About ▾  1-800-835-9565  [Request Quote →]`
>    - **Shop Furniture** opens a single-column megamenu with 9 items: Seating, Desks & Workstations, Storage & Filing, Tables, Boardroom, Ergonomic Products, Panels & Dividers, Accessories, Quiet Spaces. Header of the megamenu is "Business Furniture" linking to `/collections/business-furniture`.
>    - **Industries / Brands / Services / About** open simple dropdowns (Industries: Healthcare · Education · Government · Non-Profit · Professional Services. Brands: Keilhauer · Global/Teknion · ergoCentric. Services: Design Services · Delivery & Installation · Relocation Management · OECM Procurement. About: Our Work · About Us · Contact · Request a Quote).
>    - **Phone number** styled as charcoal text, click-to-call (`tel:`). **Request Quote** is the only red CTA in the header (primary button style).
>    - **Cart count badge** uses `--cartCountBg` red — only other red element in the header.
>    - **Mobile (375px):** hamburger → vertical accordion with the same 5-item structure. Phone + Request Quote pinned to the top of the drawer. Mobile drawer uses the secondary header token set.
> 6. **Footer** — uses inverse scheme (charcoal bg, white text). 4-column layout: (a) Shop Furniture (9 categories), (b) Industries (5 sectors), (c) Services (4 items) + About (4 items), (d) Contact block (phone, address, hours, OECM trust strip, Canadian-owned line with maple-leaf accent per BBI canadian-flag-accent rule). Red on hover for primary nav links only. Bottom bar: copyright + policy links (Privacy, Returns, Shipping, Terms).
> 7. **Quote-request CTA block** — BBI's primary conversion pattern. Two variants: (a) standalone section — charcoal bg, white heading, red CTA, OECM trust line below; (b) inline PDP variant — replaces add-to-cart entirely on unbuyable items, larger button, "Request a Quote" wording, "We respond within 1 business day" microcopy.
>
> **Output format per component:** rendered visual (all states, both schemes) + CSS class structure + tokens consumed. Markdown spec sheet at the end listing usage rules.
>
> Begin with Buttons. Stop after Buttons — I'll confirm before you proceed to Inputs.

**Stress-test follow-ups:**
1. "Show the focus ring on a primary button with a white-canvas screenshot zoomed 200%. Confirm it's visible with my eyes closed (i.e. ≥3:1 against white AND against the red button)."
2. "The product card — render one with a sold-out item using `--soldBadgeBackground`. The image slot must be at top, 16:9. Quote CTA replaces the price/add-to-cart row."
3. "Render the mobile header (375px) with the hamburger open. Use secondary header tokens. Confirm submenu text contrast."
4. "Quote-request CTA: render at 1440px and 375px. It must read as the primary action — heavier visual weight than any link on the page."
5. "Audit: across all components on `scheme-default`, what % of total pixels are red? Target 5–8%. If higher, propose which red surface to demote to outline."

**Pass/fail gates:**
- [ ] All button states visible side-by-side on white AND charcoal canvas
- [ ] Focus rings clearly visible on every interactive component (button, input, link, checkbox, radio)
- [ ] Product card has 16:9 image slot at top — no exceptions
- [ ] Quote-request CTA visually outranks every secondary action on its block
- [ ] All 5 badges legible (no auto-computed text-color near the white/black flip threshold)
- [ ] Mobile header submenu uses secondary tokens cleanly
- [ ] Canadian maple leaf appears at least once in footer

**Pushback phrases:**
- "Focus ring on the input is invisible against `--inputBackground`. Bump to `--line-color` and re-render."
- "Product card has no image slot at top. Project rule: 16:9 image slot is mandatory. Re-render."
- "Quote CTA looks like a secondary button. It's our primary conversion pattern for unbuyable items — match the visual weight of the homepage hero CTA."
- "The sale badge text auto-flipped to black on red — that's the brightness-filter trap from the audit. Pick a darker red or force white text in the spec."
- "Red density on the components board exceeds 12%. Demote secondary buttons to outline; reserve red surface for primary CTAs and badges only."

---

### Pre-Phase-3 data check (run BEFORE opening the Screens chat)

Phase 3 renders are visual-only — they don't pull live Shopify data — but the screens reference URLs the architecture doc *plans* to exist. Confirm the four URLs you'll mock so the post-session Shopify build doesn't hit a missing-page surprise.

Run from project root:

```bash
for url in \
  "https://www.brantbusinessinteriors.com/collections/business-furniture" \
  "https://www.brantbusinessinteriors.com/collections/highback-seating" \
  "https://www.brantbusinessinteriors.com/pages/oecm" \
  "https://www.brantbusinessinteriors.com/pages/quote"; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' "$url")  $url"
done
```

Expected: all `200`. If any return `404`:

| URL | If 404, do this before Phase 3 |
|---|---|
| `/collections/business-furniture` | Create the collection in Shopify Admin (smart collection: `tag contains business-furniture`). Without this, the homepage Shop entry banner has nowhere to point. |
| `/collections/highback-seating` | Confirm via [`docs/plan/site-architecture-2026-04-25.md`](../plan/site-architecture-2026-04-25.md) §2c that this sub-collection still exists. If renamed, swap the example sub-collection in the Phase 3 opening message to one that exists (e.g. `/collections/medium-back-seating`). |
| `/pages/oecm` | Note in the Phase 3 opening message that this page is a *new build* — Claude Design isn't constrained by an existing page. Render is greenfield. |
| `/pages/quote` | Same — greenfield render, no existing page to honor. |

Also confirm the four "smart collections to create" tables in architecture §2l (brand-filtered) and §4 Rule 2 ("View all" per category) — these don't need to exist for Phase 3 (the renders don't link to them), but should be on the post-session Shopify build punchlist before the new theme goes live.

This is a one-time ~30-second check. Don't skip — a 404 on the Shop entry banner is the most embarrassing live bug you can ship.

---

### Phase 3 — Screens chat

**Attach:** brand mark + 2 anti-reference screenshots + the Phase 1 CSS + the Phase 2 component spec.

**Opening message (paste verbatim):**

> Final chat for the BBI design system rebuild. **This chat = five template-driven reference screens only.** Tokens and components are locked from the previous chats (both attached). Compose screens from the existing components — don't redesign them. Don't propose new tokens.
>
> The new BBI site has **5 templates driving ~110 pages.** Render one canonical example of each template (plus the Homepage). The site architecture is fully specified — no live-site reference is needed; the attached screenshots are the *anti-reference* (the beige we're eliminating).
>
> **Render each at 1440px desktop AND 375px mobile, on `scheme-default` unless noted:**
>
> 1. **Homepage** (custom) — sections in this exact order per architecture Rule 6:
>    1. Hero — headline, image, red primary CTA ("Shop Furniture") + secondary outline CTA ("Request a Quote").
>    2. Shop entry banner → `/collections/business-furniture` with 4 featured category tiles (Seating, Desks, Storage, Boardroom).
>    3. Featured products row (3 cards, 16:9 image slot at top).
>    4. **OECM trust bar** — single full-width band: "Verified OECM supplier. Ontario institutions can purchase without open tender." Quiet, not loud.
>    5. Industries we serve — 5 sector thumbnails (Healthcare, Education, Government, Non-Profit, Professional Services) → industry landing pages.
>    6. Services overview (Design Services · Delivery · Relocation) — 3 cards.
>    7. Testimonials / Our Work preview + "Read customer stories →" link.
>    8. Footer (from Phase 2).
>
> 2. **`collection.category.json`** — render the **Business Furniture vertical** (`/collections/business-furniture`): hero banner, breadcrumbs (`Home > Shop Furniture`), 9-tile category grid (Seating, Desks, Storage, Tables, Boardroom, Ergonomics, Panels, Accessories, Quiet Spaces), "View all Business Furniture →" link, "Can't find it? Call 1-800-835-9565" CTA. **No product grid on this template.**
>
> 3. **`collection.json`** — render a **sub-collection** (e.g. `/collections/highback-seating`): hero image, breadcrumbs (`Home > Shop Furniture > Seating > High-back Seating`), left filter sidebar (desktop) / bottom-sheet drawer (mobile), product grid (3 across desktop, 2 across mobile, every card with 16:9 image slot), pagination, **mandatory phone CTA block at bottom** ("Can't find exactly what you need? Our team can help. Call 1-800-835-9565" + "Request a Quote →" secondary button — Rule 5).
>
> 4. **Landing page template** — render the **OECM page** (`/pages/oecm`): hero, intro copy, featured cards (3–4 differentiators), trust block / project photos, cross-links to relevant collections, primary CTA to `/pages/quote`. This template is reused for ~20 pages (industries, brands, services, about, FAQ).
>
> 5. **PDP — unbuyable variant** (custom `product.json`): image gallery, title, OECM badge, **Quote-request CTA block replaces Add-to-Cart entirely** — no price, no buy button — with "We respond within 1 business day" microcopy, spec table, related products row. This is BBI's flagship pattern.
>
> **Audits to include in the same message:**
> - **Red density audit** per screen — target 5–8%.
> - **Contrast audit** — every text/bg pair appearing across the 5 screens, AA pass/fail.
> - **Token coverage audit** — every token from the Phase 1 map; flag any unused.
> - **Cross-link audit** — confirm interconnection rules (breadcrumbs on screens 2 & 3; phone CTA on screen 3; cross-link to industry/category on screen 4; related products on screen 5).
>
> Start with the Homepage desktop + mobile in one message. Stop after that — I'll confirm before screen 2.

**Stress-test follow-ups:**
1. "Re-render the PDP with the Quote-request CTA at 2× weight — it should be the only thing the eye lands on above the fold."
2. "`collection.json` mobile: filters must collapse into a bottom-sheet drawer, not a left rail. Re-render and confirm the phone CTA block at bottom is intact."
3. "Red density on the homepage came in at 11%. Show me which element to demote (likely the OECM trust bar or the industries thumbnails). Re-render at ≤8%."
4. "`collection.category.json` tile grid — confirm tiles use section blocks (not metafields) and each tile has image + label + blurb + link. Show the empty-state of an unfilled tile."
5. "OECM landing page hero — propose 3 visual treatments for the OECM badge: quiet inline, banded across hero, and corner ribbon. I want quiet inline; show all three for comparison so I can confirm."

**Pass/fail gates:**
- [ ] All 5 screens rendered at both 1440px and 375px
- [ ] **Homepage section order matches Rule 6 exactly** (hero → shop entry → featured products → OECM bar → industries → services → testimonials → footer)
- [ ] Header on every screen shows the 5-item nav + phone + Quote CTA exactly as specced in Phase 2
- [ ] **`collection.category.json` shows zero products** — only category tiles
- [ ] **`collection.json` has the phone CTA block at bottom** (architecture Rule 5 — non-negotiable)
- [ ] Breadcrumbs visible on screens 2 and 3
- [ ] PDP unbuyable has NO add-to-cart and NO price — only Quote-request CTA
- [ ] Every product card on every screen has a 16:9 image slot at top
- [ ] Red density 5–8% on every screen
- [ ] Contrast audit shows zero AA failures
- [ ] OECM trust signal present on Homepage and OECM landing page, quiet inline (never sale-tag loud)
- [ ] Maple leaf accent on Canadian-owned copy in footer
- [ ] Token coverage audit returns: every token used OR flagged with intended location

**Pushback phrases:**
- "PDP shows a price field — unbuyable PDPs have no price. Remove."
- "`collection.category.json` is showing products — this template is tile-grid only. Products only appear on the `collection.json` template (screen 3). Re-render with tiles only."
- "`collection.json` is missing the bottom phone CTA — this is mandatory per architecture Rule 5. Re-add."
- "Homepage section order is wrong (services before industries). Per Rule 6, industries come first. Re-render."
- "Header dropped the phone number. Phone is a top-level header element next to the Quote CTA. Re-add."
- "Megamenu under Shop Furniture is showing 4 columns of educational/healthcare/etc. Those verticals were archived 2026-04-25 — Business Furniture only, single column with 9 categories. Re-render."
- "OECM badge on the homepage looks like a sale tag. Tone it down — quiet trust, not loud promo."
- "Mobile `collection.json`: 3 across at 375px is too dense. Drop to 2."
- "Hero overlay text is 4.2:1 on the image — bump overlay opacity until it clears 4.5:1 or move text off the photo."
- "You introduced a beige tone on the testimonial card background. We banned beige. Use `--cardBackground` from the token file."

---

## 3. Post-session steps

### A. Fill `docs/strategy/design-system.md` (canonical spec)

The skeleton already exists with TBD slots. Walk top-to-bottom and replace TBDs with Phase outputs:

| `design-system.md` section | Source |
|---|---|
| **Color tokens → Scheme: default** table — every TBD hex/rgb/contrast cell | Phase 1 — `scheme-default` block |
| **Color tokens → Scheme: inverse** table | Phase 1 — `scheme-inverse` block |
| **Color tokens → Global tokens** table | Phase 1 — global block |
| **Typography** table — H0/H1/H2/H3/Body/Small/Button × mobile + desktop | Phase 1 — typography scale |
| **Spacing, radius, shadow** — `--inputRadius` / `--buttonRadius` / `--cardRadius` / `--imageRadius` / `--productRadius` + `shadow-sm` / `shadow-md` | Phase 1 — radius + shadow scales |
| **Components** sections — usage notes per component | Phase 2 — markdown spec sheet |
| **Changelog** — append `2026-XX-XX — Token values populated from Claude Design v1 session.` | self |

Save the Phase 3 PNG exports to `data/design-photos/design-system-v1-2026-XX-XX/` and link from the design-system.md "Implementation notes" section.

### B. Enter values in Shopify Admin (BBI Landing Dev)

1. Open [BBI Landing Dev Theme Editor](https://admin.shopify.com/store/office-central-online/themes/186373570873/editor) → Theme settings → Colors.
2. For each color scheme in the schema (`scheme-default`, `scheme-inverse`, etc.): paste the per-scheme token values from Phase 1. (Shopify maps the `--camelCase` names to its internal snake_case schema — see [`docs/reviews/design-system-audit-2026-04-27.md`](../reviews/design-system-audit-2026-04-27.md) if you need the mapping.)
3. Theme settings → Header / Badges / States / Search / Overlay / Marquee: paste global tokens.
4. Theme settings → Typography: enter the body and heading font + scales.
5. Theme settings → Layout (radius/shadow): enter the radius and shadow scales.
6. Save. Open the BBI Landing Dev preview URL.
7. Visual diff against live: homepage, a PDP (unbuyable), collection, contact, footer.

### C. One-time code edits (per the audit)

Do these on a feature branch targeting BBI Landing Dev BEFORE publishing. design-system.md says "no dark mode" — recommended path is **delete**, not recolor.

| File | Line(s) | Change |
|---|---|---|
| [`theme/snippets/style-variables.liquid`](../../theme/snippets/style-variables.liquid) | 83–154 | **Delete the dark-mode block entirely** (design-system.md disables dark mode). Fallback if you want to keep it: replace `#ffca10` → `#D4252A` and re-test contrast on dark canvas. |
| [`theme/snippets/style-variables.liquid`](../../theme/snippets/style-variables.liquid) | 301–334 | Delete dark-mode header overrides (or map to BBI red if dark mode kept). |
| [`theme/sections/blinking-icons.liquid`](../../theme/sections/blinking-icons.liquid) | line 205 — `#f00f00` typo | Replace → `#D4252A` (BBI red). |
| [`theme/sections/shapes.liquid`](../../theme/sections/shapes.liquid) | lines 333, 339 — `#FFCA10` × 2 | Replace yellow → `#D4252A`, OR remove the section if unused (confirm via theme-editor usage check first). |

Run `shopify theme check` before commit; resolve all errors. Open a PR with before/after screenshots of homepage, PDP, collection, and footer.

---

## 4. Credit-budget table

Target: ≤6 prompts per phase. Front-load every constraint in the opening message so follow-ups are reserved for stress-tests and pushback only.

| Phase | Opening message | Continuations (gated) | Stress-tests | Pushback (worst-case) | **Budget** |
|---|---|---|---|---|---|
| Tokens | 1 | 1 (request inverse scheme) | 1–2 (contrast table, density check) | 1 (re-do red-text contrast) | **≤5** |
| Components | 1 | 5 (one continuation per component group: inputs, cards, badges, header, footer/quote CTA — gated) | 1 (focus-ring zoom audit) | 1 (re-do quote CTA weight) | **≤8** |
| Screens | 1 (Homepage) | 4 (collection.category.json, collection.json, landing, PDP) | 1 (red density rebalance) | 1 (e.g. PDP price removal, megamenu fix) | **≤7** |
| **Total** | | | | | **≤20 prompts across all 3 chats** |

**Note:** Phase 2 budget grew from ≤6 to ≤8 because the Header alone is 5 distinct sub-elements (megamenu + 4 dropdowns + phone + Quote CTA + mobile drawer) that shouldn't be re-rendered on a fix. Phase 3 grew from ≤5 to ≤7 because there are 5 templates to render (Homepage + 4 templates), not 3 generic screens. If you want to stay under 16 total, drop the Landing page render from Phase 3 and design it manually after the session — it's the lowest-risk template (close to a static brochure page).

**Rules to stay under budget:**
- Never re-explain locked anchors; reference them by name.
- Bundle multiple gates into a single follow-up ("audit contrast AND density AND token coverage in one message").
- If a gate fails twice in a row on the same component, abandon Claude Design for that piece and design it manually — don't burn credits debugging the model.
- If you find yourself typing a clarifying question, the opening message was under-specified. Note it for next time; don't send the question this time unless blocking.
