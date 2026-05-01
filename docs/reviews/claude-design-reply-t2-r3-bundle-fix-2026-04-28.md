# Reply to Claude Design — Bundle missing homepage CSS

**Paste from the line below into the Claude Design conversation.**

---

The source files are byte-identical to the lock — your hashes are correct and I confirmed them three ways. But the **bundled standalone is missing the homepage CSS**, which is why the homepage renders with stacked tiles, plain typography, and broken grids inside the canvas.

Your lock-check verbatim said: *"Homepage styles are inline inside Homepage.jsx's `<style>` block (no separate homepage.css file), so the style block is byte-identical by transitivity."*

That's wrong on two counts:

1. There is no `<style>` block inside `Homepage.jsx`. Grep returns 0 hits.
2. The homepage CSS has always been a **separate** file (`homepage.css`) that was *inlined alongside* tokens.css and bbi-components.css in the round-2 standalone. The round-2 standalone had **6** inline `<style>` blocks; the round-3 standalone has **5**. The 11,234-char block containing every `.hp-*` rule (`.hp-hero`, `.hp-shop__tiles`, `.hp-industries`, `.hp-services`, `.hp-products`, `.hp-work`, `.hp-case`, `.hp-service`, `.hp-industry`) is gone — replaced rather than supplemented by `collection-category.css`.

Without `.hp-shop__tiles { grid-template-columns: repeat(4, 1fr) }`, the Shop-entry tiles fall back to default block layout and stack vertically. Same fallback explains every other layout drift in the homepage artboard.

## Fix

Add the round-2 `homepage.css` block back as a 6th `<style>` block in the bundled standalone — between `bbi-components.css` and `collection-category.css`. Pull it verbatim from the inline `<style>` blocks of `01-LOCKED-homepage-standalone.html` (it's the block whose first rule is `.hp-root { background: var(--background); ... }`).

After that lands, the canvas should render six inline `<style>` blocks in this order:

1. fonts (`@font-face` Inter / Inter Tight / JetBrains Mono)
2. tokens.css
3. bbi-components.css
4. **homepage.css** ← reinstate this
5. collection-category.css
6. audits.css

Re-run the lock-check before exporting. The verification target is: **the round-3 standalone contains every CSS rule the round-2 standalone contained, plus the new template-2 rules** — not just byte-identical source files.

After this single patch lands, ship the round-3 final and we open a fresh conversation for round 4 / template 3.
