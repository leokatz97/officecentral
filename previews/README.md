# previews/

Browser-viewable HTML artifacts. Serve locally with:

```bash
python3 scripts/serve-previews.py
# → http://localhost:8080/
```

| File | What it is |
|---|---|
| `website-fix-checklist.html` | **The interactive fix checklist.** The `update-checklist` skill writes here. |
| `hero-100-lookup.html` | Per-product spec-lookup status dashboard for the Hero 100 enrichment. |

Older before/after and disposition-review previews lived here but were regenerable — delete-and-rebuild as needed using the matching `scripts/build-*.py` or `scripts/before-after.py`.
