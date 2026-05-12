# PE Pass 2 — Enrichment Session Master Instructions
# Read this before running any batch prompt

---

## What these sessions do

Each session works through one batch of BBI products one at a time.
For each product you type: `yes` / `skip` / `edit` / `other`
If `edit`, just dump your notes — Claude writes the copy.
Progress saves after every product. Sessions are resumable.

---

## Files involved (never delete these)

| File | Purpose |
|---|---|
| `data/reports/pe-pass2-batches.json` | Which handles are in each batch |
| `data/reports/pe-pass2-products.json` | Pre-filled data for all 157 products |
| `data/reports/pe-pass2-checkpoint.json` | Your decisions so far (written after every product) |
| `data/reports/pe-pass2-output.json` | Final descriptions + specs (written after every product) |

---

## The 4 options

| Input | Meaning | What Claude does |
|---|---|---|
| `yes` | Draft is fine as-is | Writes pre-filled description + specs to output |
| `skip` | Don't touch this product | Logs as skipped, moves on |
| `edit` | Rewrite using my notes | Takes your raw notes, writes full BBI-voice copy (About This Product → Key Features → Who It's For) + fills all spec fields it can |
| `other` | Move to Other collection | Flags for tag-strip + Other collection move in PE-PASS-3 |

---

## What Claude shows for each product

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5 of 26 — Batch 1: Chairs Part 1 of 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NAME:     Armless low back stacking chair
  CODE:     MVL2748            ← Google this on the manufacturer site
  VENDOR:   Brant Business Interiors  (override → type "vendor: X")
  PRICE:    $139.99  ·  Tier A  ·  OECM ✓

  DESC:     thin (43 chars) — needs rewrite
  SPECS:    2 / 12 filled  (manufacturer ✓ · country ✓ · 10 × ✗)

  🔍 Web:   [what Claude found from searching the product code]

  → yes / skip / edit / other
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Shortcuts during a session

- `yes` — approve as-is
- `skip` — skip
- `other` — move to Other
- `edit` + your notes (can be one line or a paragraph)
- `vendor: Safco` — override vendor without a full edit
- `next` — same as `yes` (shorthand)
- `done` — end session early, save checkpoint, commit

---

## Description format Claude always writes (matching Hero 100)

```html
<p><strong>[Bold hook sentence.]</strong></p>
<p>[2-3 sentences about the product — what it does, who it's built for, why it matters in Ontario institutional context.]</p>

<h3>Key features</h3>
<ul>
  <li>[Feature 1]</li>
  <li>[Feature 2]</li>
  <li>[Feature 3]</li>
</ul>

<h3>Who it's for</h3>
<p>[Specific buyer type in Ontario institutional context.]</p>

<p>Available from Brant Business Interiors — Canada's OECM-eligible commercial furniture supplier since 1964. Delivery across Canada; installation available in Ontario and Western Canada. Call <strong>1-800-835-9565</strong> for current pricing, lead times, or volume quotes.</p>
```

---

## Batch map

| Batch | File | Products |
|---|---|---|
| 1 | `batch-1-chairs-part1.md` | 26 chairs (Tier A first) |
| 2 | `batch-2-chairs-part2.md` | 26 chairs |
| 3 | `batch-3-chairs-part3.md` | 25 chairs |
| 4 | `batch-4-desks-tables-part1.md` | 27 desks + tables |
| 5 | `batch-5-desks-tables-part2.md` | 10 desks + tables |
| 6 | `batch-6-storage-accessories.md` | 30 storage + accessories |
| 7 | `batch-7-uncategorized.md` | 13 uncategorized |
