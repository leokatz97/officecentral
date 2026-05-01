# Template 2 (Collection · category) — Round 3 Review

**Date:** 2026-04-28
**Source:** `02-collection-category-standalone.html` from Claude Design
**Reviewed against:** the round-3 prompt + locked round-2 homepage

---

## Summary

Solid round 1 on template 2. Strawman delivered, no token bloat, no invented `bbi-` components in `bbi-components.css`, locked homepage source files (tokens, components, Homepage.jsx) all UNCHANGED — the system inheritance held. Brand index is a real piece of work: three tiers, 19 brand rows, dealer-status indicators, maple-leaf badges on Canadian brands.

Three things to push back on before locking. None are systemic — all are workflow / consistency nits.

---

## Pass / Fail by Gate

| Gate | Status | Notes |
|---|---|---|
| Strawman structure delivered | PASS | All 9 sections present (header → footer) |
| Order matches prompt | **FAIL (defensible)** | Industry shortcut moved before brand index — unconfirmed |
| `tokens.css` unchanged | PASS | Byte-identical to round-2 locked file |
| `bbi-components.css` unchanged | PASS | Byte-identical |
| `Homepage.jsx` unchanged | PASS | Byte-identical |
| 9 canonical categories | PASS | Seating · Desks & Workstations · Storage & Filing · Tables · Boardroom · Ergonomic · Panels · Accessories · Quiet Spaces |
| 5 canonical sectors | PASS | Office & Corporate · Healthcare · Education · Government · Industrial |
| OECM copy verbatim | PASS | Same string, same target |
| Token discipline | PASS (1 nit) | One raw RGB triple should compose `--shadowColor-rgb` (line 166) |
| Audit panels — 4 same | PASS | Contrast, Red density, Token coverage, Cross-links |
| Red density 5–8% | PASS | Measured 5.3% at rest, 6.1% with one hover |
| Reply-contract confirmation | **FAIL** | Claude Design exported without confirming the 3 reply-contract items |
| Canvas shows homepage alongside template 2 | **FAIL** | DesignCanvas now renders ONLY template 2 — locked homepage artboards and audits dropped |

---

## Edits to push back on (round-3 r2)

### 1. Restore the locked-homepage section in DesignCanvas

`index.html` currently mounts only the cc section:

```jsx
<DesignCanvas>
  <DCSection id="cc" ...>
    cc-1440, cc-375, cc-audits
  </DCSection>
</DesignCanvas>
```

The locked round-2 canvas had a homepage section with `hp-1440`, `hp-375`, and a homepage audits artboard. Both should render alongside `02 — Collection · category` so the canvas keeps doubling as the visual reference for everything locked. `Homepage.jsx` is already loaded in the bundle — it's just not mounted.

### 2. Tokenize the one missed rgba triple

`collection-category.css` line 166:

```css
.cc-cat-grid .bbi-card--collection .bbi-card__num {
  ...
  background: rgba(11,11,12,0.55);   /* should be rgba(var(--shadowColor-rgb), 0.55) */
}
```

Same compose pattern as the homepage hero caption + collection-tile gradient. The two `rgba(255,255,255,0.85)` whites on lines 151 and 165 stay as defended literals — those are the same overlay-system whites already defended in `bbi-components.css`. Comments are fine.

### 3. Don't drop the homepage audits when redefining `window.Audits`

`Audits.jsx` redefines the global `Audits` component with template-2-only data. The round-2 homepage audits component is gone. Two options:

- **(a)** Namespace each template's audits explicitly: `window.AuditsHomepage` and `window.AuditsCollectionCategory`. Mount each in its own section's audit artboard.
- **(b)** Make `Audits` template-aware via a registry: `window.Audits.register("homepage", {...})`, `register("collection-category", {...})`, then `<Audits template="homepage" />` reads the right slice.

Either works. The point is the homepage audit data shouldn't disappear from the canvas every time a new template ships.

---

## Process — enforce the reply contract on round 4

Claude Design skipped the three reply-contract confirmations on round 3 (strawman, bbi-components.css additions, brand-strip composition) and went straight to export. The strawman re-order and the brand-strip "(c) hybrid" call are both defensible, but should have come back as a paragraph in chat first so we could redirect cheaply.

For round 4 (template 3 — `collection`), the reply contract is non-negotiable. Add a sentence to that prompt: "If the previous round skipped the reply contract, re-confirm before this round's export — three sentences, in chat, not in the deliverable."

---

## What's well-built and worth keeping

- **Brand index pattern.** Three-tier text list (Premium · Canadian-made · Specialist) with brand name + category list + dealer-status indicator. 19 brand rows cover the catalogue well. The mono "Authorized dealer" / "Stocked · quote available" status text is doing real work — it tells a procurement buyer whether BBI files the warranty claim or sub-quotes.
- **Intro spec plate** (Categories: 9 · Brands: 30+ · Models in catalogue: 1,200+ · Quote response: 1 business day). Not in the strawman, but adds a numerical anchor and reads as credibility, not flair.
- **Industry shortcut row.** 5 sectors as compact tiles with arrow CTAs. Clean.
- **CTA closer** uses the suggested copy verbatim and composes `.bbi-cta-section` + `.scheme-inverse` cleanly.
- **Audit panel architecture (ap-\*).** Nicely refactored — `AuditPanel` / `APRow` / `APTable` atoms make every panel uniform. Worth keeping for templates 3–5.
- **Token discipline overall.** 0 literals in audit-panels.css. 3 in collection-category.css (2 defended, 1 to fix).

---

## Files

- Standalone (Claude Design output): `data/design-photos/screens-t2-2026-04-28/02-collection-category-standalone.html`
- Decoded source: same folder — `CollectionCategory.jsx`, `Audits.jsx`, `collection-category.css`, `audit-panels.css`, `index.html`

---

## Next step

Open `docs/reviews/claude-design-reply-t2-r2-2026-04-28.md` and paste it into the same Claude Design conversation that produced this round.
