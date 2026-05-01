# Reply to Claude Design — Template 3 r2 (CSS class collision + missing assets)

**Paste from the line below into the Claude Design conversation.**

---

The bundle has 7 inline `<style>` blocks ✓ and source files for templates 1 + 2 are byte-identical to the round-3 lock ✓ — verification on those gates passed. Three problems break the actual render.

## 1. CSS class collision — `.cn-page` is doing two jobs

This is the root cause of every visual issue you're seeing on template 3 (the squished header, the cut-off CTA + footer, the 36px-tall page). In `Collection.jsx` you've used `.cn-page` for **both**:

- The page wrapper (line 422): `<div className="scheme-default cn-page cn-page--mobile">`
- Each pagination button (lines 310–315): `<span className="cn-page is-current">`, `<a className="cn-page">`, etc.

In `collection.css` line 476 the rule for the pagination button is:

```css
.cn-page {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--borderColor);
  border-radius: var(--inputRadius);
  font-family: var(--bodyFont);
  font-size: 13px;
  font-weight: 500;
  color: var(--textColor);
  text-decoration: none;
  background: var(--background);
}
```

That rule also applies to the page wrapper because it shares the class. The page wrapper becomes `display: inline-flex` with `height: 36px`, `font-size: 13px`, a 1px border, a border-radius, and 0/10px padding. That's why the entire collection page is collapsing into a 36px-tall inline strip — the header is cramming inside it, the CTA closer is bleeding out the side, and font sizes are wrong everywhere.

`.cn-page--next` collides too (pagination "Next" button vs the page wrapper's `--mobile` modifier are unrelated, which is fine, but the convention is broken).

### Fix

Rename every pagination use of `.cn-page` to `.cn-pagination__page` (BEM child of `.cn-pagination`). Specifically:

**`Collection.jsx`** — change lines 310–315 from:

```jsx
<li><span className="cn-page is-current" aria-current="page">1</span></li>
<li><a className="cn-page" href="?page=2">2</a></li>
<li><a className="cn-page" href="?page=3">3</a></li>
<li className="cn-page-sep" aria-hidden="true">…</li>
<li><a className="cn-page" href="?page=14">14</a></li>
<li><a className="cn-page cn-page--next" href="?page=2">Next <span className="arrow">→</span></a></li>
```

To:

```jsx
<li><span className="cn-pagination__page is-current" aria-current="page">1</span></li>
<li><a className="cn-pagination__page" href="?page=2">2</a></li>
<li><a className="cn-pagination__page" href="?page=3">3</a></li>
<li className="cn-pagination__sep" aria-hidden="true">…</li>
<li><a className="cn-pagination__page" href="?page=14">14</a></li>
<li><a className="cn-pagination__page cn-pagination__page--next" href="?page=2">Next <span className="arrow">→</span></a></li>
```

**`collection.css`** — rename the rules at lines 476–507:

- `.cn-page { ... }` → `.cn-pagination__page { ... }`
- `.cn-page:hover { ... }` → `.cn-pagination__page:hover { ... }`
- `.cn-page.is-current { ... }` → `.cn-pagination__page.is-current { ... }`
- `.cn-page-sep { ... }` → `.cn-pagination__sep { ... }`
- `.cn-page--next { ... }` → `.cn-pagination__page--next { ... }`

Leave the page-wrapper rules untouched: `.cn-page { ... }` (page wrapper, line ???), `.cn-page--mobile`, `.cn-page .bbi-footer { ... }`, and all `.cn-page--mobile .*` rules. Also leave line 422 of `Collection.jsx` (the wrapper) as-is.

After the rename, every `.cn-page*` selector should resolve to either the page wrapper (top of file) or the pagination buttons (`.cn-pagination__*`) — never both.

## 2. Logo asset broken — `assets/bbi-logo-v2.png` missing from the zip

`Homepage.jsx` references the logo at three places (lines 33, 57, 435) as `<img src="assets/bbi-logo-v2.png" />`. The round-3 zip shipped that file at `assets/bbi-logo-v2.png` and it rendered correctly. The round-4 zip doesn't contain an `assets/` folder at all — only the original logo input at `uploads/10-bbi-logo-v2.png`.

The bundled standalone (`BBI-Templates-1-3-standalone.html`) probably doesn't carry the logo as a manifest entry either, so the image fails on every header (homepage, collection-category, AND collection — all three templates). That's why screenshot 3 shows the broken-image icon + alt text instead of the logo.

### Fix

Re-add the logo to the deliverable at `assets/bbi-logo-v2.png` (copy from `uploads/10-bbi-logo-v2.png`), and embed it in the bundled standalone's manifest so the `<img src="assets/bbi-logo-v2.png">` reference resolves both in dev mode (linked CSS + on-disk PNG) and in the bundle.

## 3. `audits.css` not in the index.html link tags

`index.html` lines 14–18 link tokens, bbi-components, homepage, collection-category, and collection — but not audits. The standalone bundle's 7th `<style>` block carries the audit styling, so the bundle renders fine, but if anyone opens `index.html` directly the audit panels render unstyled. Add `<link rel="stylesheet" href="src/audits.css">` and ship `src/audits.css` as a separate file (extract it from the bundle's 7th style block — the `.ap-*` rules).

## Reply contract for r2

Before you re-export, confirm in chat:

1. Class collision fix landed — `.cn-page*` resolves cleanly between page wrapper and pagination button, no shared selectors.
2. Logo present at `assets/bbi-logo-v2.png` and rendering on all three templates.
3. `audits.css` linked in `index.html` and shipped as a file.
4. Bundle re-verified: 7 inline `<style>` blocks in order, all `.hp-*`, `.cc-*`, `.cn-*`, `.ap-*` selectors present, source-file SHA-256s for the locks still match round-3.

Then re-export. Templates 1 + 2 source files should remain byte-identical to the lock — you only need to touch `Collection.jsx`, `collection.css`, the asset folder, and the index.html link tags.
