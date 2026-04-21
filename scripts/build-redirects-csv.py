"""
Build a CSV of 301 redirects for the 9 renamed product handles.
Upload via Shopify Admin -> Online Store -> Navigation -> URL Redirects -> Import.
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, 'data', 'handle-rename-log.json')) as f:
    log = json.load(f)

out_path = os.path.join(ROOT, 'data', 'url-redirects.csv')
rows = 0
with open(out_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Redirect from', 'Redirect to'])
    for entry in log:
        if 'rename_error' in entry:
            continue
        old = f"/products/{entry['old_handle']}"
        new = f"/products/{entry['new_handle']}"
        w.writerow([old, new])
        rows += 1

print(f'Wrote {rows} redirects to {out_path}')
print('\nUpload: Shopify Admin → Online Store → Navigation → URL Redirects → Import')
