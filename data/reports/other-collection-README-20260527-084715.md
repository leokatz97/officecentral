# Other Collection — Steve's Classification Worksheet (with Claude pre-fills)

**Generated:** 20260527-084715
**Total products:** 338
**Estimated time:** ~45 min (338 × ~8 sec/row, mostly just typing Y)

---

## What changed since the first draft

Claude pre-filled three columns for you:
- `recommended_sub_collection_1/2/3` — best-guess collection handles
- `recommended_brand` — normalized vendor (only 1 change in 338 rows)
- `claude_confidence` — high / med / low / none
- `claude_reasoning` — short note on why Claude picked these

**Claude's confidence breakdown:**
- HIGH confidence: 39 rows (11%)  ← scan, type Y, move on
- MED confidence:  126 rows (37%)   ← glance, usually Y
- LOW confidence:  119 rows (35%)   ← actually look
- NONE:            54 rows (15%)  ← Claude couldn't guess, you fill from scratch

Estimated coverage where Claude got it ~right: **~48%** of rows.

---

## The new workflow

### For each row, do ONE of these three:

**Option A — Claude got it right (most common):**
- Type **Y** in the `accept_recommendations` column
- Done. Move on.

**Option B — Claude was partially right or wrong:**
- Leave `accept_recommendations` blank
- Type the correct collection handle(s) in `override_sub_collection_1/2/3`
- Optionally fix `override_brand`

**Option C — Product doesn't belong anywhere or should be discontinued:**
- Type **Y** in `leave_in_other` (keeps as-is, no routing) OR
- Type **Y** in `archive_this` (discontinues product)

---

## The "STEVE FILLS" columns

| Column | What to put |
|---|---|
| accept_recommendations | **Y** to accept all three sub-collection recs + brand rec. Blank = manual override below. |
| override_sub_collection_1 | Collection **handle** (e.g. `seating`, not `Seating`). From picklist file. |
| override_sub_collection_2 | Optional. |
| override_sub_collection_3 | Optional. |
| override_brand | Only if Claude's brand is wrong. From BRANDS picklist. |
| additional_tags | Comma-separated. Optional. |
| leave_in_other | **Y** = doesn't fit anywhere, keep in Other. |
| archive_this | **Y** = discontinue, archive product. |
| notes_for_leo | Free text. Anything weird for Leo to look at. |

**Don't fill `new_product_type`** — it's frozen taxonomy on the BBI store and Leo will handle that separately.

**Don't change titles, handles, or descriptions** — those are reference-only.

---

## How to open

1. Open `other-collection-products-20260527-084715-with-recs.csv` in **Google Sheets**:
   - File → Import → Upload → "Replace spreadsheet", separator Comma
2. Freeze header: View → Freeze → 1 row
3. **Filter by `claude_confidence`** to triage:
   - Start with `high` (fast Y-and-move-on)
   - Then `med`
   - Then `low` + `none` (the actual thinking)
4. Open `other-collection-picklists-20260527-084715.csv` in a second tab for valid handles when overriding

---

## When done

Save as CSV → email back to Leo (leo@venn.ca).
