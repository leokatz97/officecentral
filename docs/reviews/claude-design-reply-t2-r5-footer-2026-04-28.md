# Reply to Claude Design — Footer / closer visual continuity

**Paste from the line below into the Claude Design conversation.**

---

Bundle fix verified — the patched standalone (`BBI Template 2 - Collection Category.html`) now carries 6 inline `<style>` blocks in the right order, the homepage.css block (11,234 chars, all `.hp-*` rules) is back, and source files (`Homepage.jsx`, `tokens.css`, `bbi-components.css`) remain byte-identical to the lock. Homepage renders correctly inside the canvas now.

The footer issue isn't the footer itself — the footer markup and CSS are unchanged. The problem is the **transition into the footer** on this template. CollectionCategory ends with two `.scheme-inverse` blocks back-to-back:

```
... → .bbi-cta-section.scheme-inverse  (charcoal, 96px top/bottom padding)
    → .bbi-footer.scheme-inverse       (charcoal, 64px top padding)
```

Both resolve `var(--background)` to `#0B0B0C` under `.scheme-inverse`, so they merge visually into one ~290px tall slab of charcoal with no edge between them. The eye reads it as a single oversized footer.

The homepage doesn't have this problem because its last content section (Testimonials) is `.bbi-section--alt` (light), giving a clean contrast break before the footer.

## Fix — pick one

**(a) Hairline top divider on the footer.** Add a 1px top border to `.bbi-footer` using the inverse `--borderColor` (which resolves to `#1F1F21` under `.scheme-inverse` — already defined). One-line change, scoped to bbi-components.css:

```css
.bbi-footer { border-top: 1px solid var(--borderColor); }
```

That gives a subtle separator line between the closer and the footer without changing the dark treatment of either. Same approach the spec uses everywhere else for "two stacked sections" hairlines.

**(b) Lift the CTA closer onto `--alternateBackground`.** Change `.bbi-cta-section`'s background from `var(--background)` to `var(--alternateBackground)`. Under `.scheme-inverse` that's `#161618` — slightly lifted from the footer's deeper `#0B0B0C`. Creates a "raised plate / deep base" hierarchy that's standard footer treatment.

Either works. (a) is the smaller change and stays closer to the spec; (b) is the more designed answer. Pick whichever lands cleaner — both are token-only fixes, no new hexes.

After this lands, ship the round-3 final and we'll open a fresh conversation for round 4 / template 3.
