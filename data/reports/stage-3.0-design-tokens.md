# Stage 3.0 Design Tokens — Deliverable Report

**Date:** 2026-05-07  
**Branch:** feature/stage-3.0-design-tokens  
**Dev theme:** 186373570873  
**Live theme:** 186495992121 (NOT touched — confirmed)

---

## 1. Design System Findings (Step 1)

Read: `docs/strategy/design-system.md` v1 (DS-1 complete, locked 2026-05-04)

### OECM badge / "Vendor of Record" treatment
The design system lists "OECM dots" under **red usage — small accent use**:
> `✓ Eyebrow ticks, OECM dots, maple-leaf badge marks (small accent use)`

The existing badge implementation (`.lp-oecm-badge` — a charcoal-outlined pill with a red 6px dot and charcoal text) is **correct per spec**. No pill-level changes needed.

**Link colour**: `--linkColor: #0B0B0C` (charcoal). Body links default to charcoal. Red must not appear on body links.

### Logo specs
Design system references `data/logos/bbi-logo-hires.png` as the prior asset and `data/design-photos/components-v1-2026-04-27/bbi-logo-v2.png` (CLAUDE.md: "BBI logo v2 (new)"). Logo rules: horizontal lockup only, minimum 120px wide, always on white/near-white. No recolouring.

The v2 file was **already present** in `theme/assets/bbi-logo-v2.png` — no upload step required.

### Icon set
Design system does not reference Lucide or any named icon library. The footer (`bbi-footer.liquid`) has the canonical maple leaf SVG (`<svg class="bbi-footer__leaf" viewBox="0 0 13 13" ...>`). This SVG is the approved pattern. Used as the replacement target for all `&#127809;`/`&#x1F341;` instances.

### Customer Stories IA
Customer Stories does **not appear** in the design system navigation or footer mock. Per task fallback rule, added to:
- **Nav**: About dropdown, between Our Work and OECM Procurement
- **Footer**: Services column (only column without explicit "About" category; no design-system IA to contradict)

---

## 2. OECM Source Identified — CSS producing red/strikethrough

All BBI section wrappers (`.lp-gov`, `.lp-about`, `.lp-brands`, etc.) had a scoped rule:
```css
.lp-xxx a { color: var(--linkColor); }
```
This sets colour to charcoal but sets **no `text-decoration`**. The Starlite parent theme can supply `text-decoration: line-through` (from sale-price styling) via equal-specificity cascade rules on `a` elements. Since the BBI rule only overrides `color`, Starlite's `text-decoration` bleeds through.

The `bbi-nav.liquid` and `bbi-footer.liquid` were already clean — every link class (`.bbi-nav__dd-link`, `.bbi-footer__column a`, `.bbi-footer__trust a`) had explicit `text-decoration` rules.

---

## 3. OECM Fix Applied (Stage 3.0.1)

Added `text-decoration:none` to the scoped `a` rule in **9 sections**. Body-copy link underlines are preserved via more-specific rules already in the sections (e.g., `.lp-faq__cta a { text-decoration: underline; }`).

| File | Rule before | Rule after |
|---|---|---|
| `sections/ds-lp-government.liquid` | `.lp-gov a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-about.liquid` | `.lp-about a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-brands.liquid` | `.lp-brands a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-brands-ergocentric.liquid` | `.lp-ergo a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-brands-keilhauer.liquid` | `.lp-keilhauer a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-brands-global-teknion.liquid` | `.lp-global a{color:var(--linkColor);}` | + `text-decoration:none` |
| `sections/ds-lp-oecm.liquid` | `.bbi-lp-oecm a { color: var(--linkColor); }` | + `text-decoration: none` |
| `sections/ds-lp-quote.liquid` | `.bbi-lp-quote a { color: var(--linkColor); }` | + `text-decoration: none` |
| `sections/ds-lp-delivery.liquid` | `.lp-delivery a{color:var(--linkColor);}` | + `text-decoration:none` |

---

## 4. Logo v2 — Upload path, files modified, fallback behaviour

**Asset already present:** `theme/assets/bbi-logo-v2.png` (no upload needed).

**Files modified:**
- `theme/snippets/bbi-nav.liquid` — desktop logo fallback (line ~266) and mobile overlay logo fallback (line ~403–405): replaced `<span class="bbi-header__logo-text">...</span>` / `<span class="bbi-mobile-nav__header-logo-text">...</span>` with `<img src="{{ 'bbi-logo-v2.png' | asset_url }}" height="36/30" alt="Brant Business Interiors" loading="eager/lazy">`.
- `theme/snippets/bbi-footer.liquid` — brand plate fallback (line ~159–161): replaced `<span class="bbi-footer__brand-plate-text">...</span>` with `<img src="{{ 'bbi-logo-v2.png' | asset_url }}" height="44" alt="Brant Business Interiors" loading="lazy">`.

**Fallback behaviour:** When `section.settings.logo` is blank (merchant hasn't uploaded via Theme Editor), v2 is shown. When the merchant uploads a logo via Theme Editor, that takes precedence — v2 remains as guaranteed fallback.

**Mobile inversion:** `.bbi-mobile-nav__header-logo img { filter: brightness(0) invert(1); }` applies automatically to the `<img>` tag in the mobile overlay, rendering the logo white on the dark mobile nav background. This matches the existing behaviour.

**Footer plate:** Logo renders on the white `#FFFFFF` brand plate card (`bbi-footer__brand-plate`). No filter applied — v2 shows in full colour as intended.

---

## 5. Emoji Audit

Full scan: `&#127809;`, `&#x1F341;`, literal emoji, HTML entities in emoji range.

### Maple leaf instances replaced (13 total)

| File | Instances | Context |
|---|---|---|
| `sections/ds-lp-about.liquid` | 3 | Hero eyebrow, trust plate, diff-card num |
| `sections/ds-lp-brands.liquid` | 1 | Brand tile meta text |
| `sections/ds-lp-brands-keilhauer.liquid` | 3 | Hero eyebrow, trust plate, diff-card num |
| `sections/ds-lp-brands-ergocentric.liquid` | 4 | Hero eyebrow, trust plate, diff-card num, closing trust line |
| `sections/ds-lp-quote.liquid` | 2 | Diff-card sentence, closing trust line |

**Replacement:** All 13 instances replaced with:
```html
<svg class="bbi-icon bbi-icon--leaf" viewBox="0 0 13 13" fill="currentColor" aria-hidden="true">
  <path d="M6.5 0 L7.6 3.5 L11 2 L9 5 L13 6.5 L9.5 7 L11 10.5 L6.5 8.5 L2 10.5 L3.5 7 L0 6.5 L4 5 L2 2 L5.4 3.5 Z"/>
</svg>
```
CSS `.bbi-icon--leaf { display:inline-block; width:14px; height:14px; vertical-align:-2px; color:#D4252A; flex-shrink:0; }` added to each section's `<style>` block.

### Emoji left unreplaced (with reason)

| File | Line | Emoji | Reason |
|---|---|---|---|
| `sections/ds-lp-delivery.liquid` | 151 | 🚚 (truck) | Not a maple leaf; design system doesn't specify a delivery truck SVG equivalent — flag for DS-3 icon pass |
| `sections/ds-lp-delivery.liquid` | 156 | 🔧 (wrench) | Same — flag for icon pass |
| `sections/ds-lp-delivery.liquid` | 161 | 📋 (clipboard) | Same — flag for icon pass |
| `sections/product-short-videos.liquid` | 136 | `🔹-Icon-Color` | Inside an SVG `id=""` attribute — not rendered emoji, no change needed |

---

## 6. Customer Stories Nav + Footer

### Desktop nav — About dropdown (before/after)
```html
<!-- BEFORE -->
<ul class="bbi-nav__panel" role="menu">
  <li ...><a ... href="/pages/about">About Us</a></li>
  <li ...><a ... href="/pages/our-work">Our Work</a></li>
  <li ...><a ... href="/pages/oecm">OECM Procurement</a></li>
  <li ...><a ... href="/pages/contact">Contact</a></li>
</ul>

<!-- AFTER -->
<ul class="bbi-nav__panel" role="menu">
  <li ...><a ... href="/pages/about">About Us</a></li>
  <li ...><a ... href="/pages/our-work">Our Work</a></li>
  <li ...><a ... href="/pages/customer-stories">Customer Stories</a></li>  ← added
  <li ...><a ... href="/pages/oecm">OECM Procurement</a></li>
  <li ...><a ... href="/pages/contact">Contact</a></li>
</ul>
```

### Mobile nav — About accordion (same position added)

### Footer Services column (before/after)
```html
<!-- BEFORE: 6 links -->
<li><a href="/pages/oecm">OECM Procurement</a></li>

<!-- AFTER: 7 links — Customer Stories appended at bottom -->
<li><a href="/pages/oecm">OECM Procurement</a></li>
<li><a href="/pages/customer-stories">Customer Stories</a></li>  ← added
```

**Placement rationale:** Design system has no explicit IA for Customer Stories in the footer. No "About" footer column exists. Customer Stories added to Services column per task fallback rule ("default to the Services column or whichever column already lists About-adjacent links"). Placed last to minimise disruption to existing visual weight.

---

## 7. Push Results

All 11 files pushed to theme `186373570873`. All returned HTTP 200.

| File | HTTP |
|---|---|
| `snippets/bbi-nav.liquid` | 200 |
| `snippets/bbi-footer.liquid` | 200 |
| `sections/ds-lp-oecm.liquid` | 200 |
| `sections/ds-lp-government.liquid` | 200 |
| `sections/ds-lp-about.liquid` | 200 |
| `sections/ds-lp-brands.liquid` | 200 |
| `sections/ds-lp-brands-ergocentric.liquid` | 200 |
| `sections/ds-lp-brands-keilhauer.liquid` | 200 |
| `sections/ds-lp-brands-global-teknion.liquid` | 200 |
| `sections/ds-lp-quote.liquid` | 200 |
| `sections/ds-lp-delivery.liquid` | 200 |

---

## 8. Spot-Check Results

Five files pulled back from dev theme and compared byte-for-byte against worktree:

| File | Worktree ≡ Dev theme | Required strings present |
|---|---|---|
| `snippets/bbi-nav.liquid` | ✓ | `/pages/customer-stories`, `bbi-logo-v2.png` |
| `snippets/bbi-footer.liquid` | ✓ | `/pages/customer-stories`, `bbi-logo-v2.png` |
| `sections/ds-lp-about.liquid` | ✓ | `bbi-icon--leaf`, `text-decoration:none` |
| `sections/ds-lp-brands-ergocentric.liquid` | ✓ | `bbi-icon--leaf` |
| `sections/ds-lp-oecm.liquid` | ✓ | `text-decoration: none` |

Live theme `186495992121`: confirmed Customer Stories NOT present in nav — **live theme untouched**.

---

## 9. Unexpected Drift / Halts

None. All four sub-tasks proceeded without ambiguity.

- OECM badge spec was clear (charcoal text, no strikethrough, red dot accent) — existing `.lp-oecm-badge` implementation already matched; the fix was purely defensive CSS.
- Logo v2 was already in `theme/assets/` — no file upload required.
- Icon set: design system does not specify non-leaf icons; delivery emoji (🚚🔧📋) left in place and flagged.
- Customer Stories footer IA: no design-system column specified; defaulted to Services per task rule.

---

## 10. Confirmation

- Theme `186495992121` (live) was **NOT touched**.
- All changes target `186373570873` (BBI Landing Dev) only.
- Branch: `feature/stage-3.0-design-tokens` — not merged.
