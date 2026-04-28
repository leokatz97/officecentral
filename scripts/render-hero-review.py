"""
Generate a triage HTML page for flagged hero images.

Reads data/reports/hero-audit-{date}.csv and writes
previews/hero-audit-{date}.html — cards grouped by flag reason,
each with the live pos-1 image (or MISSING placeholder), dims,
and a direct Shopify Admin edit link.

Usage:
  python3 scripts/render-hero-review.py
  python3 scripts/render-hero-review.py --input=data/reports/hero-audit-2026-04-28.csv
"""
import argparse
import csv
import glob
import html
import os
import sys
from datetime import datetime

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPT_DIR   = os.path.join(ROOT, 'data', 'reports')
PREV_DIR  = os.path.join(ROOT, 'previews')
TODAY     = datetime.now().strftime('%Y-%m-%d')
ADMIN_URL = 'https://admin.shopify.com/store/office-central-online/products/{}'
STORE_URL = 'https://www.brantbusinessinteriors.com/products/{}'

REASON_LABELS = {
    'no_image':   ('No Image', '#c0392b'),
    'ai_residual': ('AI Residual', '#8e44ad'),
    'dimensions': ('Below 400×400', '#d35400'),
}

SERVICE_HANDLES = {
    'delivery', 'installation', 'colour', 'color',
    'caster-options', 'please-select-a-finish', 'finish',
}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f5f5f5; color: #222; padding: 24px; }
h1 { font-size: 22px; margin-bottom: 4px; }
.meta { color: #666; font-size: 13px; margin-bottom: 28px; }
h2 { font-size: 16px; font-weight: 600; margin: 32px 0 12px;
     padding: 6px 12px; border-radius: 4px; color: #fff; display: inline-block; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.card { background: #fff; border-radius: 8px; overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,.1); }
.card img { width: 100%; height: 180px; object-fit: contain;
            background: #fafafa; border-bottom: 1px solid #eee; }
.missing-img { width: 100%; height: 180px; display: flex; align-items: center;
               justify-content: center; background: #fdecea; color: #c0392b;
               font-weight: 600; font-size: 13px; border-bottom: 1px solid #eee; }
.card-body { padding: 12px; }
.card-title { font-size: 13px; font-weight: 600; margin-bottom: 4px;
              white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-handle { font-size: 11px; color: #888; margin-bottom: 6px; }
.dims { font-size: 11px; color: #555; margin-bottom: 8px; }
.badge { display: inline-block; font-size: 10px; font-weight: 700;
         padding: 2px 6px; border-radius: 3px; color: #fff; margin-bottom: 8px; }
.actions { display: flex; gap: 8px; }
.btn { flex: 1; text-align: center; font-size: 11px; font-weight: 600;
       padding: 5px 8px; border-radius: 4px; text-decoration: none; }
.btn-admin { background: #5c6ac4; color: #fff; }
.btn-live  { background: #e8f4ec; color: #27ae60; border: 1px solid #a9d9b5; }
.exempt { opacity: .55; }
.exempt-label { font-size: 10px; color: #888; font-style: italic; margin-bottom: 6px; }
"""


def is_service_item(handle, title):
    h = handle.lower()
    t = title.lower()
    for kw in ('delivery', 'installation', 'colour', 'color', 'caster', 'finish', 'please-select'):
        if kw in h or kw in t:
            return True
    return False


def render_card(row):
    handle    = html.escape(row['handle'])
    title     = html.escape(row['title'])
    product_id = row['product_id']
    src       = row['pos1_src']
    w         = row['pos1_width']
    h_val     = row['pos1_height']
    reason    = row['flag_reason']
    exempt    = is_service_item(row['handle'], row['title'])

    label, color = REASON_LABELS.get(reason, (reason, '#555'))
    exempt_class = ' exempt' if exempt else ''
    exempt_html  = '<div class="exempt-label">⚠ Likely service/admin item — review before fixing</div>' if exempt else ''

    if src:
        img_html = f'<img src="{html.escape(src)}" alt="{title}" loading="lazy">'
    else:
        img_html = '<div class="missing-img">NO IMAGE</div>'

    dims = f'{w}×{h_val}px' if (w or h_val) else 'unknown dims'

    admin_link = ADMIN_URL.format(product_id)
    live_link  = STORE_URL.format(handle)

    return f"""
<div class="card{exempt_class}">
  {img_html}
  <div class="card-body">
    <div class="badge" style="background:{color}">{html.escape(label)}</div>
    {exempt_html}
    <div class="card-title" title="{title}">{title}</div>
    <div class="card-handle">{handle}</div>
    <div class="dims">{dims}</div>
    <div class="actions">
      <a class="btn btn-admin" href="{admin_link}" target="_blank">Edit in Admin</a>
      <a class="btn btn-live"  href="{live_link}"  target="_blank">Live page</a>
    </div>
  </div>
</div>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=None)
    args = parser.parse_args()

    if args.input:
        csv_path = args.input
    else:
        pattern = os.path.join(RPT_DIR, 'hero-audit-*.csv')
        files = sorted(glob.glob(pattern))
        if not files:
            print('No hero-audit CSV found. Run audit-hero-images.py first.')
            sys.exit(1)
        csv_path = files[-1]

    print(f'Reading {csv_path}')

    with open(csv_path, newline='') as f:
        rows = list(csv.DictReader(f))

    flagged = [r for r in rows if r['needs_review'] == 'True']
    if not flagged:
        print('0 flagged rows — nothing to render.')
        sys.exit(0)

    # Group by reason in priority order
    order = ['no_image', 'ai_residual', 'dimensions']
    groups = {k: [] for k in order}
    for r in flagged:
        groups.setdefault(r['flag_reason'], []).append(r)

    os.makedirs(PREV_DIR, exist_ok=True)
    out_path = os.path.join(PREV_DIR, f'hero-audit-{TODAY}.html')

    date_str = TODAY
    total    = len(flagged)

    sections_html = ''
    for reason in order:
        group = groups.get(reason, [])
        if not group:
            continue
        label, color = REASON_LABELS.get(reason, (reason, '#555'))
        cards = ''.join(render_card(r) for r in group)
        sections_html += f'<h2 style="background:{color}">{label} ({len(group)})</h2>\n<div class="grid">{cards}</div>\n'

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BBI Hero Audit — {date_str}</title>
<style>{CSS}</style>
</head>
<body>
<h1>BBI Hero Image Audit</h1>
<div class="meta">Generated {date_str} · {total} products flagged · threshold 400×400px</div>
{sections_html}
</body>
</html>"""

    with open(out_path, 'w') as f:
        f.write(html_out)

    print(f'Written: {out_path}')
    print(f'{total} cards rendered ({len(groups.get("no_image",[]))} no-image, '
          f'{len(groups.get("ai_residual",[]))} AI residual, '
          f'{len(groups.get("dimensions",[]))} dimension issues)')


if __name__ == '__main__':
    main()
