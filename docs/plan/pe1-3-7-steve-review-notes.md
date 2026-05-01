# PE-1/3/7 — Items Needing Steve's Manual Review

## PE-7 Luxhide misrenders (2)
The model rendered "Luxhide" as "Leather" — Luxhide is Global
Furniture's branded faux leather, not real leather. Fix titles
and descriptions on:

- `mvl2732-annapolis-high-back-luxhide-tilter` — draft_meta_title
  says "Leather Tilter Chair", should be "Luxhide Tilter Chair"
- `basics-elora-chair-high-back-black-leather-luxhide-mvl1893upu30bl20`
  — draft_meta_desc references "leather", should reference
  "Luxhide" (faux leather)

## PE-7 persistent NEEDS_RERUN (1)
One row failed to draft after retry — likely missing source
data. Manual draft required:

- `dual-coloured-bookcase-15-sizes-available`
