---
name: bbi-lp-audit
description: >
  Batch-audits all BBI landing page sections matching `theme/sections/ds-lp-*.liquid`.
  Runs every check from the cross-page CSS & markup audit checklist, produces a
  per-file PASS/FAIL/WARN report, then outputs a consolidated fix list sorted by
  severity. Use before a deploy, after a batch of page builds, or any time you want
  a full health-check of the landing page inventory.

  Invoked as `/bbi-lp-audit` (audits all ds-lp-*.liquid) or
  `/bbi-lp-audit ds-lp-oecm` (single file, no extension needed).

  Do NOT auto-trigger. Only fire when Leo explicitly invokes `/bbi-lp-audit`.
---

# BBI Landing Page Audit

Runs the full cross-page CSS & markup checklist against every (or one specific)
`theme/sections/ds-lp-*.liquid` file and produces a structured report.

---

## Usage

Leo invokes:
- `/bbi-lp-audit` — audit all `theme/sections/ds-lp-*.liquid` files
- `/bbi-lp-audit ds-lp-oecm` — audit a single named section (no path, no extension)

Parse the argument. If no argument, default to glob `theme/sections/ds-lp-*.liquid`.

---

## Execution

### Step 1 — Discover files

```bash
ls theme/sections/ds-lp-*.liquid
```

Report the list to Leo. If a specific file was named, confirm it exists first.

### Step 2 — Run checks on each file

For each file, run every check in the **Checklist** section below. Read the file
once at the start; run all grep/read operations against that content.

Report results per file in this format:

```
── ds-lp-{name}.liquid ──────────────────────────────────
PASS  [check name]
FAIL  [check name] — line N: [exact issue]  Fix: [one-line fix]
WARN  [check name] — line N: [note]
```

After all files, emit the **Consolidated Fix List**.

### Step 3 — Consolidated Fix List

One line per fix needed, sorted: FAILs first (highest to lowest severity), then
WARNs. Format:

```
[FAIL|WARN]  ds-lp-{name}.liquid : line N  [check ID]  [one-line description and fix]
```

End with a summary count:
```
Files audited: N   FAILs: N   WARNs: N
```

If FAILs > 0, ask Leo: **"Fix all FAILs now, or flag and move on?"**
- "Fix now" → apply the auto-fix policy below for mechanical fixes; list non-mechanical fixes for Leo to approve
- "Flag" → save the consolidated list to `docs/reviews/lp-audit-{YYYY-MM-DD}.md` and stop

---

## Checklist

Run every check. Check IDs match those in Step 5.5 of `/bbi-build-page` so the two tools stay in sync.

---

### CSS / Style

**CSS-1 — `!important` banned**
`grep -n '!important'`
FAIL if any match.

**CSS-2 — Inline `style=""` banned**
`grep -n 'style="'`
FAIL for any match not inside a `<style>` or `{% style %}` block. Check line context.

**CSS-3 — Single-class img rules below base-reset specificity**
Read the `<style>` block. The base reset is `.bbi-lp-{name} img` (specificity 0,1,1).
Any rule setting `height`, `width`, or `object-fit` on an `<img>` with a selector
specificity of 0,1,0 or lower will be silently overridden.
FAIL if such a rule exists without a wrapper-class prefix.

**CSS-4 — Flex/grid children with text missing `min-width: 0`**
Scan each `display: grid` or `display: flex` declaration for children that render
text content. Grid children in `1fr` columns and flex children with `flex: 1` that
carry text but have no `min-width: 0` can cause single-character vertical wrapping
on narrow viewports.
WARN if found.

---

### Color Tokens

**COL-1 — No disallowed hardcoded hex outside `:root {}`**
`grep -n '#[0-9A-Fa-f]\{3,6\}'` across the CSS outside `:root`.
Allowed exceptions: `#D4252A`, `#A81E22`, `#0B0B0C`, `#FFFFFF`, `#FAFAFA`,
`#fff`, `#000`, `#F0F4FF`, `#CBD5F0`, `#2563EB`, `rgba(255,255,255,…)`,
`rgba(0,0,0,…)`.
FAIL for anything else.

**COL-2 — No warm tones**
`grep -ni 'beige\|#FFF8\|#FEF\|#FDF\|cream\|tan\|sand\|ivory'`
FAIL if any match.

**COL-3 — No red headings**
`grep -n 'h[1-4].*color.*D4252A\|h[1-4].*saleBadgeBackground'`
FAIL if any match.

**COL-4 — No red as body link color on white**
Check `.{wrapper} a { color: … }` — confirm it resolves to charcoal (`--linkColor`
or `#0B0B0C`), not `#D4252A` or `var(--saleBadgeBackground)`.
FAIL if body link color is red.

---

### Copy & Trust Signals

**COPY-1 — No "BBI" abbreviation in customer-facing copy**
`grep -n '\bBBI\b'`
Exclude: CSS class definitions (`.bbi-`), HTML class attributes (`class="…bbi…"`),
HTML comments, Liquid comments, CSS comment blocks.
FAIL for any remaining match — must be replaced with "Brant Business Interiors".

**COPY-2 — Phone present in hero CTA row AND closer section**
`grep -n '1-800-835-9565\|18008359565'`
FAIL if phone appears fewer than 2 times on a page that has both a hero and a closer.
WARN if page has only one of those sections and phone appears at least once.

**COPY-3 — OECM placement on Primary-ICP pages**
`grep -ni 'oecm'`
For pages targeting institutional Ontario buyers (school boards, hospitals,
municipalities, not-for-profits): FAIL if OECM appears 0 times.
WARN if OECM appears only in body copy and not in the hero standfirst or a trust row.
Check placement: OECM badge/text must appear in the trust row or hero standfirst —
NOT as marketing-claim phrasing ("we're proud to be…").

---

### Section Structure Order

Canon: breadcrumbs → hero → intro → differentiators → [conditional sections] → FAQ → CTA closer

**STRUCT-1 — Exactly one `<h1>` in the hero, none elsewhere**
`grep -c '<h1'`
FAIL if count ≠ 1.
FAIL if the single `<h1>` is outside the `.lp-hero` section.

**STRUCT-2 — Page ends with `.bbi-cta-section.scheme-inverse` closer**
`grep -n 'bbi-cta-section.*scheme-inverse\|scheme-inverse.*bbi-cta-section'`
FAIL if no match.
WARN if the closer is present but not the last `<section>` before the closing `</div>`.

**STRUCT-3 — FAQ immediately before closer**
Read the HTML structure. Confirm `lp-faq` section appears directly before
`bbi-cta-section.scheme-inverse`.
WARN if another section sits between FAQ and the closer.

---

### Liquid / Shopify Correctness

**LIQ-1 — No `{% include %}` tags**
`grep -n '{%.*include'`
FAIL if any match. All partials must use `{% render %}`.

**LIQ-2 — No inline `default:` in HTML attributes**
`grep -n 'default:'` — then check the line context.
FAIL if `| default:` appears inside an HTML attribute value (href, src, alt param in
image_tag, aria-label, aria-describedby, etc.).
The `{% schema %}` block's `"default":` key is where defaults belong.
Extract to a `{%- assign -%}` variable if the setting has no schema default
(e.g. URL-type fields which don't support `"default"` in schema).

**LIQ-3 — `image_url: width:` present before every `image_tag`**
`grep -n 'image_tag'`
For each hit, walk back up the filter chain and confirm `image_url: width:` appears
before it. FAIL if any `image_tag` lacks an upstream `image_url: width: N` filter.

**LIQ-4 — Schema `"name"` ≤ 25 characters**
Extract the `"name":` value from the `{% schema %}` block.
`echo -n "name value" | wc -c`
FAIL if > 25 — Shopify returns 422 on push.

**LIQ-5 — Schema has `"presets"` array**
`grep -n '"presets"'` inside the schema block.
FAIL if missing — sections without presets don't appear in the Theme Editor.

**LIQ-6 — `{{ block.shopify_attributes }}` in every block loop**
For each `{% for block in section.blocks %}` or `{% for block in %}` loop, confirm
the rendered wrapper element for that block includes `{{ block.shopify_attributes }}`.
FAIL if any block loop is missing it.

**LIQ-7 — Broken `alt:` default pattern in `image_tag`**
`grep -n 'alt:.*| default:'`
FAIL if `| default:` appears inside a named argument to `image_tag`.
In Shopify Liquid the `| default:` filter applies to the entire tag output, not the
argument value — the fallback never fires for the alt attribute.
Fix: `{%- assign _alt = var | default: 'fallback' -%}` then `alt: _alt`.

---

### Accessibility

**A11Y-1 — `:focus { outline: none }` always paired with `:focus-visible`**
`grep -n ':focus'`
For every rule containing `outline: none` or `outline: 0`, confirm a corresponding
`:focus-visible` rule exists for the same selector with a visible outline.
FAIL if any `:focus` removes the outline without a `:focus-visible` replacement.
This is a WCAG 2.4.7 violation — keyboard users lose their visible focus indicator.

**A11Y-2 — FAQ accordion buttons have `aria-expanded`**
`grep -n 'lp-faq__trigger\|faq.*trigger\|accordion.*button'`
FAIL if the FAQ trigger `<button>` element has no `aria-expanded` attribute.

**A11Y-3 — Every `<img>` has an `alt` attribute**
`grep -n '<img'`
FAIL if any `<img>` tag has no `alt=` attribute.
NOTE: decorative images inside a parent with `aria-hidden="true"` should use
`alt=""`. Any other image must have meaningful alt text.

**A11Y-4 — Form inputs have associated `<label>`**
`grep -n '<input\|<textarea\|<select'`
For each hit, confirm a `<label for="…">` with a matching `id` exists.
FAIL if any input is missing a label.

**A11Y-5 — Interactive elements have `:focus-visible` styles**
Beyond the button/link checks in A11Y-1, scan for `<button>` elements that are
NOT covered by the `.bbi-btn` class (e.g. `.lp-faq__trigger`, `.lp-accordion__btn`)
and for `<a>` elements acting as interactive cards. Confirm `:focus-visible` exists
for each class.
WARN if any interactive element class has no `:focus-visible` rule.

---

### JSON-LD

**JLDL-1 — Pages with FAQ blocks have FAQPage JSON-LD**
If `"type": "faq_item"` blocks exist in the schema, confirm the `<script type="application/ld+json">` block includes `"@type":"FAQPage"`.
FAIL if FAQ blocks are present but no FAQPage JSON-LD exists.

**JLDL-2 — FAQPage JSON-LD is dynamically built from blocks**
In the JSON-LD script block, look for a `{%- for block in faq_blocks -%}` Liquid loop.
FAIL if the FAQPage `mainEntity` array is hardcoded — divergence from editable blocks
makes the schema stale whenever an editor changes a FAQ answer.

---

## Auto-Fix Policy

When a FAIL has a deterministic mechanical fix, apply it immediately without asking:

| Check | Auto-fix |
|-------|----------|
| CSS-1 | Remove `!important`; document why the specificity needs fixing |
| CSS-2 | Move inline property to the `<style>` block under the correct selector |
| COPY-1 | Replace `BBI` with `Brant Business Interiors` |
| LIQ-1 | Replace `{% include 'x' %}` with `{% render 'x' %}` |
| LIQ-2 | Extract `| default: '...'` to a `{%- assign -%}` variable; update the attribute |
| LIQ-7 | Extract broken alt default to `{%- assign _alt -%}` pattern |
| A11Y-1 | Add `:focus-visible` rule for the same selector with `outline: 2px solid var(--textColor); outline-offset: 2px;` |
| STRUCT-1 | Demote extra `<h1>` elements to `<h2>` |

For all other FAILs and all WARNs: list them, provide the exact fix, and wait for
Leo's decision before touching the file.

---

## Output

After all checks and any auto-fixes:

1. Print the per-file report (PASS/FAIL/WARN per check, with line numbers)
2. Print the Consolidated Fix List (sorted by severity)
3. Print the summary count
4. If FAILs remain after auto-fixes: ask Leo "Fix remaining FAILs now, or save report and stop?"
5. If only WARNs remain: ask Leo "WARNs noted — proceed or save report?"

When saving a report, write it to:
`docs/reviews/lp-audit-{YYYY-MM-DD}.md`

This file can be handed off to `/bbi-build-page` Step 5.5 as historical context.
