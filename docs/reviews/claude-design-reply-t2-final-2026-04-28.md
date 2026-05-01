# Reply to Claude Design — Template 2 final lock

**Paste from the line below into the Claude Design conversation.**

---

Two final patches and we lock template 2. Nothing else changes.

**1. Homepage stays byte-identical to round-2 final.**

`01-LOCKED-homepage-standalone.html` is the source of truth. `Homepage.jsx`, `tokens.css`, `bbi-components.css`, and `homepage.css` (its inlined style block) must be byte-identical to that lock. If the current build's homepage layout has drifted from r2-final at all — section structure, grid columns, tile sizes, anything — revert it. Template-2 work cannot edit template-1.

Note: the homepage's Shop-entry H2 ("Business furniture, every category.") and template 2's H1 use the **same string**. That duplication is intentional — the homepage's section 2 is the *teaser* that points at template 2. Do not "deduplicate" by changing the homepage. If you want to vary the homepage H2, that's a separate decision for a different round.

Before you export, confirm in chat:

> "I have re-checked Homepage.jsx, tokens.css, bbi-components.css, and the homepage style block against the round-2 lock. They are byte-identical. The Shop-entry banner renders as 4 tiles in a 1-row × 4-column grid at 1440 desktop, identical to r2-final."

If anything was different, list every divergence with line numbers and revert it.

**2. Halve the height of the collection.category hero right-column visual.**

Currently roughly twice as tall as the left-column copy block — drags the page down before the 9-category grid even appears. Bring its rendered height down to roughly the height of the copy block. Easiest path: change the aspect ratio (e.g. 4:5 → 3:2, or whatever lands the visual inline with the writing). Keep it as a placeholder, keep the caption, just shorten it.

After (1) and (2) land, ship the round-3 final and we'll open a fresh conversation for round 4 / template 3 (`collection` — single category like `/collections/seating`) with locked homepage + locked template 2 as the reference stack.
