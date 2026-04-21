"""
Phase F: Produce a manual-review table for the 31 real products that are
missing image and/or price. None have ever been sold (per Phase A).

Output: data/manual-review.md (markdown table Leo can skim).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, 'data', 'sold-history-flagged.json')) as f:
    data = json.load(f)

missing_img = {p['id']: p for p in data['real_missing_image']}
missing_price = {p['id']: p for p in data['real_missing_price']}

all_ids = sorted(set(missing_img) | set(missing_price))
rows = []
for pid in all_ids:
    p = missing_img.get(pid) or missing_price.get(pid)
    flags = []
    if pid in missing_img: flags.append('no-image')
    if pid in missing_price: flags.append('$0-price')
    rows.append((p['title'], p.get('handle'), ', '.join(flags), p.get('orders', 0)))

rows.sort(key=lambda r: r[0].lower())

out_path = os.path.join(ROOT, 'data', 'manual-review.md')
with open(out_path, 'w') as f:
    f.write('# Manual review — real products missing image and/or price\n\n')
    f.write(f'All {len(rows)} products below have never been ordered (full Orders API scanned 2024-10 → 2026-04).\n\n')
    f.write('Suggested default: archive all (none have sold). Scan the list and flag any you want to KEEP live — reply with product names.\n\n')
    f.write('| Title | Handle | Issue |\n')
    f.write('|---|---|---|\n')
    for title, handle, flags, _ in rows:
        f.write(f'| {title} | `{handle}` | {flags} |\n')

print(f'Wrote {out_path}')
print(f'{len(rows)} products for manual review')
