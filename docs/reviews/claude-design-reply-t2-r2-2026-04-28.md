# Reply to Claude Design — Template 2 round-3 r2

**Paste from the line below into the same Claude Design conversation that produced `02-collection-category-standalone.html`.**

---

Strong round on template 2. System inheritance held — `tokens.css`, `bbi-components.css`, and `Homepage.jsx` all byte-identical to round-2 locked. No new bbi-* components. Brand index is a real piece of work and the audit panel refactor (`ap-*`) is keepable across templates 3–5.

Three things to fix before this locks:

**1. Restore the locked-homepage section in the DesignCanvas.**
Round-2 had a homepage section (`hp-1440`, `hp-375`, homepage audits) sitting alongside everything new. Round-3's `index.html` mounts only the `cc` section, so the locked homepage and its audits drop off the canvas entirely. `Homepage.jsx` is still loaded — it's just not mounted. Re-add the homepage `<DCSection>` so the canvas keeps doubling as the visual reference for everything locked.

**2. Tokenize the one missed rgba triple.**
`collection-category.css` line 166:

```css
.cc-cat-grid .bbi-card--collection .bbi-card__num {
  background: rgba(11,11,12,0.55);   /* compose --shadowColor-rgb instead */
}
```

Should be `rgba(var(--shadowColor-rgb), 0.55)` — same compose pattern as the homepage hero caption and the collection-tile gradient. The two `rgba(255,255,255,0.85)` whites on lines 151 and 165 stay as defended literals; the comments justifying them are fine.

**3. Don't drop the homepage audits when redefining `window.Audits`.**
The new `Audits.jsx` overwrites the global `Audits` component with template-2-only data — the round-2 homepage audits are gone from the canvas. Two acceptable patterns:

- (a) Namespace explicitly: `window.AuditsHomepage` + `window.AuditsCollectionCategory`. Mount each in its own section's audit artboard.
- (b) Template-aware registry: `window.Audits.register("homepage", {...})`, `register("collection-category", {...})`, then `<Audits template="homepage" />` reads the right slice.

Either works. Keep both templates' audit data live on the canvas going forward.

**One process note for round 4.**
You skipped the reply-contract confirmation step on this round (strawman, `bbi-components.css` additions, brand-strip composition). The strawman re-order (industry before brand index) and the brand-strip "(c) hybrid" call are both defensible, but should land as a three-sentence chat note before export, not buried in code comments. On round 4 / template 3, please confirm in chat before exporting.

After (1)–(3) land, ship the round-3 final and we'll open a fresh conversation for round 4 / template 3 (`collection` — single category like `/collections/seating`) with this template 2 added to the locked stack.
