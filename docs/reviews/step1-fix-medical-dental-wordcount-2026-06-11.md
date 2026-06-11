# Step 1 fix — medical-dental-clinic-furniture-ontario over the 2,200-word floor

**Date (UTC):** 2026-06-11 · **Article:** `689254498617` · handle `medical-dental-clinic-furniture-ontario` · Blog News `108557861177`
**Status:** stays a **DRAFT** (`published_at = null`). Nothing flipped, no `--live` on any gate.

## What changed
The draft was 2,085 words, 115 short of the 2,200 floor flagged in the Step 1(a) triage. Added one ~185-word paragraph of product-level clinic-seating-selection depth to the existing **"Seating for every patient"** section (after the accessibility paragraph, before "Furniture priorities by clinic type"). Furniture-buying depth only — no healthcare-segment essay, so the post stays the cross-link TARGET for Step 5 (healthcare page) and Step 6 (clinics review) without pre-empting their angle.

### Paragraph added (verbatim)
> Two further seating choices come up often enough to plan for from the start. The first is patient weight capacity: a standard commercial chair is typically rated in the range of 250 to 300 pounds, while bariatric models are built wider and to higher capacities, so a waiting room serving the general public should carry at least a few higher-capacity seats and confirm the exact rating by product line rather than assume it. The second is durability under constant turnover. A busy waiting room cycles through far more sit-and-stand events than an office chair ever sees, so beam or ganged tandem seating, with several seats on a shared steel beam, holds its alignment, leaves clear floor for cleaning underneath, and stands up to the traffic better than loose chairs in a high-volume practice. For behavioural-health or higher-acuity rooms, tamper-resistant, weighted, or otherwise specified seating may be required; these are manufacturer options to confirm by line rather than assumptions. The common thread is to match the seat to how hard the room works, and a clinic-experienced dealer specifies that capacity, durability, and finish mix up front.

## Constraints held
- **Carrier gate:** no brand or SKU named in the new text; weight-capacity range stated as "typically… confirm the exact rating by product line"; behavioural-health seating framed as "manufacturer options to confirm by line rather than assumptions." No assumed specs.
- **No new D3 links:** zero `/blogs/news` `<a>` in body (verified). The 6 catalog/page `<a>` links are unchanged.
- **OECM string** verbatim and intact. Full "Brant Business Interiors," never "BBI" (0 literal "BBI").
- **No em-dashes** (0). Canadian English.
- **FAQ untouched** — no FAQ answer changed, so `faq.items` byte-match is preserved (verified PASS).

## Verification (all DRY except the single draft-body `articleUpdate`)
| Check | Result |
|---|---|
| Word count (independent Admin-API readback) | **2,270** (was 2,085) ✓ ≥ 2,200 |
| `validate-meta` (title/meta unchanged) | PASS 46 / 137 |
| `check-handles` (6 links) | PASS 6/6 storefront 200 |
| `verify-faq` (live body vs `faq.items`) | PASS — 6/6 Q/A byte-match |
| `published_at` (independent readback) | `null` — still a draft ✓ |
| `image` (independent readback) | `null` — Leo adds it later ✓ |
| em-dashes / literal "BBI" / `/blogs/news` links in body | 0 / 0 / none ✓ |

The body was pushed via REST `PUT /blogs/108557861177/articles/689254498617.json` with `body_html` only (`published` omitted, so it stayed false). Confirmation is from a fresh independent `GET`, not the write echo. Live body is byte-equivalent to the pushed payload modulo Shopify's normal whitespace/entity normalization (22,365 vs 22,347 chars).

## File-sync / location note
- The PACK-equivalent source of truth for this batch is the create-payload backup `data/backups/articles/create-689254498617-20260604-225547.json`; its `body_html` was updated in lockstep with the pushed body and is **in sync on disk**. `data/backups/` is `.gitignore`d, so this tracked fix-record in `docs/reviews/` is the committable artifact (same pattern as the Step 1(a) triage PR).

## Build-state delta (NOT edited this session — for the next doc PR)
- `medical-dental-clinic-furniture-ontario` (`689254498617`) moves out of NEEDS-FIX → now **PUBLISH-READY-pending-image** (word count resolved at 2,270; all gates PASS; still no featured image / no `image.alt`, so it cannot flip until Leo adds both).
