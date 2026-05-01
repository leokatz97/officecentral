# Reply to Claude Design — Round 2 final + Round 3 confirmations

**Paste from the line below into the Claude Design conversation.** The Homepage.jsx and CSS files in `data/design-photos/screens-r2-2026-04-28/` already have edit (a) applied locally if you want to attach the patched copy.

---

Round 2 verified — all items from the round-2 prompt landed cleanly. Cache-buster doing its job.

Pre-round-3 confirmations:

1. **Keep `.bbi-cta-section` defined.** Templates 2, 4, and 5 will all use it (collection bottom CTA, landing closer, PDP unbuyable RFQ block). Retiring and re-adding just churns the system; cost of keeping it idle on template 1 is zero.

2. **Open round 3 with template 2 (collection.category).** Funnel order — index/hub → individual collection → PDP → landing. Each template uses the previous as known-good reference, and the cross-link audit already names template 2 first.

One last batch of round-2 edits before you ship final and start round 3:

**(a) New hero stack** — replace the current `Buy by the chair...` block:

```
H1:    Office furniture for Ontario — your way.
Deck:  Order single pieces online, or have us plan and install the whole office.
Body:  One team handles both paths. Same warehouse, same brands, same project lead when you need one.
```

Same `hp-hero__title` / `hp-hero__deck` / `hp-hero__sub` markup. No CSS or CTA changes.

**(b) Hero eyebrow** (line 99): change `"Commercial furniture · Mississauga, ON"` → `"Commercial furniture · Ontario"`. The new H1 promises Ontario-wide; Mississauga belongs on Contact / About, not the homepage hero. Footer plate "Canadian-owned · Mississauga, ON" stays — HQ signal in the footer is fine.

**(c) Services sub copy** (line 340): `"BBI is not a marketplace. Every order ships with planning, install, and warranty handled by the same Mississauga team that quoted it."` reads defensive now that the hero explicitly invites the catalogue path. Rewrite positively:

> Every order — single chair or full fit-out — ships with planning, install, and warranty handled by the same Ontario team that quoted it.

After (a)–(c) land, ship round 2 final. Start a fresh conversation for round 3 / template 2 with this homepage as the locked reference.
