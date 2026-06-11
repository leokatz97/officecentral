# Step 2.2 — Category Copy Push (ADMIN/MCP) — Review Artifact

**Date:** 2026-06-11 · **Channel:** Shopify Admin GraphQL (`collectionUpdate`), no theme write, no branch/PR
**Copy source:** `data/content-drafts/step-2-2-category-copy.md` (locked, voice-approved; transcribed verbatim)
**Builder:** `scripts/build-step-2-2-payloads.py` → `data/working/step-2-2-payloads.json`
**Rendered verifier:** `scripts/verify-step-2-2-render.py`
**Theme target:** role=main `186373570873` (read-only here; writes were Admin-API collection data only)

## Result: 8/8 PASS — descriptionHtml + faq.items pushed, independently read back, rendered byte-match confirmed

| # | Collection (handle) | GID | Write userErrors | Admin readback | Intro links (200) | Visible/JSON-LD FAQ | byte-match |
|---|---|---|---|---|---|---|---|
| 1 | lecterns-podiums | 487507231033 | 0 | desc✓ faq=4 | boardroom-conference-meeting, training-flip-top-tables | 4 / 4 | ✓ |
| 2 | boardroom-conference-meeting | 473198788921 | 0 | desc✓ faq=4 | meeting-tables | 4 / 4 | ✓ |
| 3 | height-adjustable-tables | 473195905337 | 0 | desc✓ faq=4 | best-standing-desks-canada, sit-stand-vs-fixed-desks-office | 4 / 4 | ✓ |
| 4 | meeting-tables | 473196560697 | 0 | desc✓ faq=4 | training-flip-top-tables | 4 / 4 | ✓ |
| 5 | training-flip-top-tables | 486802522425 | 0 | desc✓ faq=4 | (none) | 4 / 4 | ✓ |
| 6 | pedestal-drawers-storage | 473278906681 | 0 | desc✓ faq=4 | (none) | 4 / 4 | ✓ |
| 7 | fire-resistant-file-cabinets-storage | 473349620025 | 0 | desc✓ faq=4 (GARDEX copy) | (none) | 4 / 4 | ✓ |
| 8 | nesting-chairs-chair | 473350930745 | 0 | desc✓ faq=4 | training-flip-top-tables | 4 / 4 | ✓ |

Each page verified rendered (FPC-bypassed fresh render): answer-first intro renders above the grid; visible FAQ accordion = 4 Q/A; exactly **one** FAQPage JSON-LD; visible `<summary>`/answer **decode-equal** to FAQPage Q/A; all embedded internal links HTTP 200.

## Encoding spot-check (escape vs json decode-equal, as 2.1)
Boardroom FAQ: JSON-LD emits apostrophes straight (`'`, 3×) + literal em-dash (`| json`); visible band emits apostrophes as `&#39;` (3×) + literal em-dash (`| escape`). `html.unescape()` of both sides is identical → decode-equal. Holds for all 32 pairs (`byte_match=True`).

## De-conflict findings (read-only, pre-push)
- All 10 cross-link targets re-confirmed HTTP 200 before embedding.
- **height-adjustable** LINKS to `best-standing-desks-canada` + `sit-stand-vs-fixed-desks-office` (anchors "choose between electric and manual lift" / "move between sitting and standing height") — links, does not restate. ✓
- **boardroom** names Global/Teknion/OTG **factually** (dealer status); does **not** duplicate the `global-vs-teknion` / `offices-to-go-vs-global` comparison posts. Those comparison URLs were not in the verified target set and the locked copy has no anchor for them → none embedded; no-duplication test passes.
- No intro targets a `batch-ledger.md` / `priority-keywords.yaml` claimed primary keyword. No collision.

## DOC-PR NOTES (record for next doc PR; not edited here)
1. 8 category pages now carry answer-first intro + 4-pair FAQ; `faq.items` (`list.single_line_text_field`) populated on each.
2. Carrier-list ruling: **Gardex** added as a named carried brand (fire-resistant); **IOF / Uline / Lesro / Horizon** remain unnamed; **bariatric-seating HELD** (mostly archived; copy parked until Global bariatric product is live).
3. **~~🔴 Leaf-accent sizing gap~~ ✅ RESOLVED — flag was stale-cache (verified 2026-06-11, doc-PR reconciliation).** This note was raised against **stale full-page cache**; the sizing rule had already shipped to live `ds-cs-base.liquid`. **Gate (Admin-API readback, role=main `186373570873`):** `.ds-cs__intro .bbi-icon--leaf{display:inline-block;width:14px;height:14px;vertical-align:-2px;color:#D4252A;flex-shrink:0;}` is **byte-present** (asset `updated_at = 2026-06-11T13:51:11-04:00`). **Storefront render (FPC-bypassed, session-cookie + retry):** 3/3 leaf pages (`height-adjustable-tables`, `lecterns-podiums`, `fire-resistant-file-cabinets-storage`) serve the rule in scope once the path-keyed cache rolls over. No theme fix needed. *(Original note retained below for history.)* Original: the maple-leaf accent appeared **unsized** on `ds-cs-*` pages because `.bbi-icon--leaf` sizing lived only inside individual `ds-lp-*` section `<style>` blocks, not in `ds-cs-base.liquid`; the inline `<svg>` carried no width/height attrs → it fell back to default replaced-element size. The scoped `.ds-cs__intro .bbi-icon--leaf` rule (now live) fixes exactly this. **⚠️ The live fix was pushed via `push-file.py` without a branch→PR → `main` is behind live for this `<style>` block; a retroactive theme PR is needed before Step 3 (tracked in build-state).**
4. Cosmetic: Shopify's HTML sanitizer lowercased `viewBox`→`viewbox` and expanded self-closing `<svg/>`/`<path/>` on store; HTML5 parser auto-corrects SVG attribute casing on render — no action.

## Excluded
- **bariatric-seating** — HELD (not in this batch).
