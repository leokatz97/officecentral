# Claude Design — Phase 3 (Screens) Round 2 Prompt

**For:** the same conversation that produced `3 - Screens.zip` on 2026-04-28.
**Paste from the line below.** No attachments needed beyond what you already gave me — but re-attach the latest tokens.css if you'd like.

---

Round 1 review is done. Three correctness issues, one positioning rewrite, one scope question. Address all of them in round 2 and re-export the same canvas (Homepage 1440 + 375 + Audits panel). Keep everything else.

## 1. Replace the hero copy with this exact stack

```
H1:    Buy by the chair, or by the office.
Deck:  One Ontario team for whatever you need.
Body:  Shop online for workstations, seating, and storage — or bring us your space and we'll plan, quote, and install the full fit-out.
```

This is the locked stack. Render the deck as a separate paragraph between H1 and body — heading-font, weight 500, 22px desktop / 18px mobile, full-strength ink, no opacity, max-width ~42ch. Use a new class `hp-hero__deck` styled in `homepage.css` only — no new tokens, no edits to `bbi-components.css`.

Keep the existing CTA pair (Request a quote + Shop furniture). They map onto the two buyer paths in the new hero and don't need changes.

The hero promises BBI serves two buyer types simultaneously:
- **Transactional buyer** — clicks Shop furniture, browses catalogue, buys a chair.
- **Project buyer** — clicks Request a quote, hands over a floor plan, BBI plans/quotes/installs the fit-out.

Every other section on the page should now reinforce that both paths exist. See item 4.

## 2. Fix the header "Request a quote" cascade bug

In `bbi-components.css` you wrote:

```css
.bbi-header__utility a { color: var(--headerColor); text-decoration: none; }
```

That selector has specificity (0,1,1), which beats `.bbi-btn--primary { color: var(--buttonColor); }` at (0,1,0). The header CTA renders charcoal text on charcoal background at rest — invisible — and only becomes white-on-charcoal on hover (because `.bbi-btn--primary:hover` is (0,2,0) and finally wins).

Replace the rule with:

```css
.bbi-header__utility a:not(.bbi-btn) { color: var(--headerColor); text-decoration: none; }
```

Then update Audits.jsx row 25 ("Header request-quote") so its reported pairing reflects the rendered cascade rather than the intended one. Audit values must measure what the cascade actually produces — never restate the spec.

## 3. Token discipline — add the missing token, retire the literals

**Missing token.** `tokens.css` is missing `--warningBackground`. It was approved 2026-04-27 (#E8A317 amber, ink label 7.71:1 AA). Even though no screen on this canvas surfaces a low-stock badge yet, every shipped tokens.css must contain the full v1 set. Add under `:root` in the badge block:

```css
--warningBackground:     #E8A317;
--warningBackground-rgb: 232, 163, 23;
```

Add it to the Audits "Reserved (defined, not exercised)" list as well.

**Hardcoded hexes.** Your own header comment says "Composes ONLY tokens from tokens.css. No new tokens, no overrides." But there are roughly 25 hardcoded hex literals in `bbi-components.css` (footer block lines ~216–312, CTA section lines ~460–527) and 5 in `homepage.css` (hero red CTA hover, hero caption).

For the footer and `.bbi-cta-section`: apply `.scheme-inverse` to the container and let the token cascade do the work — same pattern the brief specifies for hero / feature blocks. Stop hardcoding `#0B0B0C`, `#FFFFFF`, `#1F1F21`, `#D4252A`, `rgba(255,255,255,0.78)`, etc.

For the homepage `.hp-hero__cta-red` hover: compose `--saleBadgeBackground` and `--headerHoverColor` instead of literal `#A81E22`. The hero caption can keep `rgba(var(--shadowColor-rgb), 0.92)` — that's still composed.

If any literal genuinely has no token to compose against, leave a one-line comment explaining why. Don't ship literals silently.

## 4. Positioning rewrite — Industries section + footer tagline

The hero now serves both buyer types. The Industries section as written contradicts that — it leads with "Built for institutional procurement" and lists only school boards, hospitals, and municipalities. Rewrite to keep the institutional credibility but admit private buyers:

```
H2:    Five sectors. One Ontario partner.
Sub:   From private offices to school boards to hospitals — we've quoted and installed across Ontario since 1962. Each sector below has its own catalogue page with sector-specific brands and warranty terms.
```

Keep the 5 canonical sector tiles unchanged (Office & Corporate · Healthcare · Education · Government · Industrial — locked 2026-04-27).

Footer brand tagline: change `"Commercial furniture, specced and installed. Quoting since 1962."` to `"Commercial furniture, sold or installed. Ontario since 1962."` — same dual-path promise, footer-sized.

## 5. Scope clarification — which screens are in Phase 3?

Round 1 delivered Homepage only. The cross-link audit references templates 2 (collection.category), 3 (collection), 4 (landing), and 5 (PDP unbuyable). Confirm:

- **(a)** Phase 3 is homepage-only by design — in which case approve round 2 and we'll start a new conversation for the next template, or
- **(b)** The remaining templates are still in your queue — in which case ship them in round 2 alongside the homepage corrections.

Tell me which before round 2 export.

## 6. Don't change

- The 5-sector Industries grid (sector list is locked).
- OECM copy ("OECM vendor of record" + the bar copy verbatim).
- All other Phase-2 component patterns (`.bbi-btn`, `.bbi-badge`, `.bbi-card`, `.bbi-section-head`, header structure, footer column structure).
- Token names — no renames, no new tokens beyond `--warningBackground`.
- The DesignCanvas wrapper and Audits panel structure.

## Output

Re-export the same canvas (Homepage desktop + mobile + Audits) as a fresh zip. Re-state in your reply: which of the 6 items above you addressed verbatim, which you adjusted (and why), and what you want me to confirm before round 3.
