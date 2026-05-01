# Reply to Claude Design — Template 3 r3 (badge overlap + cc artboard height)

**Paste from the line below into the Claude Design conversation.**

---

The r2 fixes landed cleanly: class collision resolved (pagination uses `.cn-pagination__page`, page wrapper keeps `.cn-page` ✓), `assets/bbi-logo-v2.png` present ✓, `audits.css` linked + shipped ✓, all six locked source files (Homepage.jsx, CollectionCategory.jsx, tokens.css, bbi-components.css, homepage.css, collection-category.css) byte-identical to the round-3 lock ✓, bundle has all 7 inline `<style>` blocks ✓, audit registry carries all three templates' slices ✓.

Two more fixes for r3, then this round closes.

## 1. Badge overlap on template-3 product cards

The Canadian-made badge is being absolutely positioned to top-left, overlapping the sub-category chip, while the Low-stock badge sits alone in the bottom flex container. Root cause: `.bbi-card__media .bbi-badge` in `bbi-components.css` (line 350) sets:

```css
.bbi-card__media .bbi-badge {
  position: absolute;
  top: 12px;
  left: 12px;
}
```

That rule cascades into every `.bbi-badge` inside `.bbi-card__media` — including the ones you've placed inside the `.cn-product__badges` flex container (which is itself absolute at `bottom: 12px; left: 12px;`). The cascade pulls each `.bbi-badge` out of the flex flow and pins it to the top-left corner — that's why Canadian-made and the sub-cat chip stack on top of each other.

Don't edit `bbi-components.css` (locked). Fix in `collection.css` by bumping specificity:

```css
.cn-product .cn-product__badges .bbi-badge {
  position: static;
  top: auto;
  left: auto;
  /* keep the existing background + border-color overrides */
  background: rgba(255,255,255,0.92);
  border-color: rgba(var(--textColor-rgb), 0.15);
}
```

`.cn-product .cn-product__badges .bbi-badge` is specificity (0,3,0); the `.bbi-card__media .bbi-badge` rule it's overriding is (0,2,0), so this wins regardless of source order. Badges will then flow inside the flex container at `bottom: 12px;` with `gap: 6px;` between them, and the sub-cat chip stays alone at top-left.

While you're there, audit the bundle render to confirm the Low-stock badge (`.cn-product__low`) sits cleanly to the right of the Canadian-made badge inside the flex container, with no wrap on the wider product cards.

## 2. Collection-category footer cut off — bump the cc-1440 artboard

`cc-1440` is set to `height={4640}` in `index.html`. The collection-category page renders ~4830px tall (intro 640 + cat-grid 1190 + industry 330 + brand-index 1146 + OECM 200 + CTA closer 500 + footer 700, plus header/crumbs). The footer overflows the artboard by ~190px and gets clipped by the canvas — that's why I can't see it. Source files for template 2 are byte-identical to the lock, so this isn't content drift; the artboard was always slightly under-sized.

Bump:

- `cc-1440` height: `4640` → `5000`
- `cc-375` height: `5520` → `6100`

While we're at it, sanity-check `cn-1440` (`5360`) and `cn-375` (`6240`) — current Collection content estimates ~4500px desktop; should fit. But re-measure with a working render (after fix #1 lands) and bump if needed.

## 3. Pending — clarify "Ontario" vs "Canada" copy

Steve flagged that the templates "say Ontario everywhere instead of Canada." Current locked copy is mostly Ontario (positioning) with Canadian highlighting where products warrant it (Canadian-made tier, maple leaf badges, brand rows). The Ontario phrases that exist:

- Hero eyebrow: `Commercial furniture · Ontario`
- Hero H1: `Office furniture for Ontario — your way.`
- OECM bar: `Ontario's broader public sector` (locked OECM phrasing)
- Industries H2: `Five sectors. One Ontario partner.`
- Industries sub: `quoted and installed across Ontario since 1962`
- Services sub: `same Ontario team that quoted it`
- Footer tagline: `Commercial furniture, sold or installed. Ontario since 1962.`
- CC brand-strip head: `30+ brands. Three tiers. One Ontario partner.`
- CC closer: `Same Ontario team`
- CC plate label: `Catalogue cover · Ontario showroom · 4:5`
- CC brand row: `Authorized · Ontario territory` (ergoCentric)
- CN closer: `Same Ontario team`

Hold this round until Steve specifies which instances should swap to Canada/Canadian. Most are locked positioning that ships across all templates; changing them is a global copy decision, not a template-3 fix.

## Reply contract for r3

Before re-export, confirm:

1. Badge override rule landed and visually verified (Canadian-made + Low-stock side-by-side at bottom; sub-cat chip alone at top-left).
2. cc-1440 / cc-375 artboard heights bumped, footer visible at the bottom of the cc-1440 viewport.
3. Locked source files (templates 1+2) still byte-identical post-build.

Then re-export. Templates 1 + 2 source files should not change — only `collection.css` and `index.html` get edits this round.
