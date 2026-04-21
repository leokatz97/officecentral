"""
Build a before/after HTML comparison for one cleaned product.
Uses the preview file for 'before' and fetches current live for 'after'.
"""
import urllib.request
import json
import re
import html as html_lib

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'

# Pick a dramatic word_junk example
TARGET_ID = 9943309746489  # "New" Pneumatic Single-Arm Monitor Stand

# Extract "before" from the preview HTML
with open('html-cleanup-preview.html') as f:
    preview = f.read()

# Each sample block starts with <h2>Title<...>ID: <id>...</h2> followed by rendered + pre blocks
m = re.search(
    r'<h2>([^<]+)<span[^>]*>([^<]+)</span></h2>\s*<div class="meta">ID: ' + str(TARGET_ID)
    + r'[^<]*</div>\s*<div class="pair">\s*<div class="col before">\s*<h3>BEFORE</h3>\s*'
    r'<div class="rendered">(.*?)</div>\s*<pre>(.*?)</pre>',
    preview, re.DOTALL,
)
title = html_lib.unescape(m.group(1)).strip()
category = m.group(2).strip()
before_html = m.group(3)
before_escaped = m.group(4)

# Fetch current live
req = urllib.request.Request(
    f'{API}/products/{TARGET_ID}.json',
    headers={'X-Shopify-Access-Token': TOKEN},
)
with urllib.request.urlopen(req) as resp:
    p = json.loads(resp.read().decode())['product']
after_html = p.get('body_html') or ''
handle = p['handle']
storefront_url = f'https://www.brantbusinessinteriors.com/products/{handle}'

before_len = len(before_html)
after_len = len(after_html)
shrink = (1 - after_len / max(before_len, 1)) * 100

out = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Before / After — {html_lib.escape(title)}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; color: #222; }}
h1 {{ color: #111; }}
h2 {{ color: #444; border-bottom: 2px solid #ddd; padding-bottom: 6px; margin-top: 30px; }}
.meta {{ background: #f4f4f4; padding: 16px; border-radius: 6px; margin-bottom: 24px; font-size: 14px; }}
.pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
.col {{ border: 1px solid #ccc; border-radius: 6px; padding: 14px; overflow: auto; background: #fff; }}
.col.before {{ background: #fff5f5; }}
.col.after {{ background: #f5fff5; }}
.col h3 {{ margin-top: 0; font-size: 13px; text-transform: uppercase; color: #666; letter-spacing: 1px; }}
.rendered {{ border-top: 1px dashed #aaa; margin-top: 10px; padding-top: 10px; max-height: 420px; overflow: auto; }}
pre {{ white-space: pre-wrap; word-break: break-all; font-size: 11px; background: #fafafa; padding: 8px; border-radius: 4px; max-height: 240px; overflow: auto; }}
a {{ color: #2a6df5; }}
</style></head>
<body>
<h1>Before / After — {html_lib.escape(title)}</h1>
<div class="meta">
<strong>Product:</strong> {html_lib.escape(title)} <span style="color:#888">({category})</span><br>
<strong>ID:</strong> {TARGET_ID}<br>
<strong>Size:</strong> {before_len} chars → {after_len} chars ({shrink:.0f}% smaller)<br>
<strong>Live storefront:</strong> <a href="{storefront_url}" target="_blank">{storefront_url}</a>
</div>

<h2>How it renders</h2>
<div class="pair">
  <div class="col before">
    <h3>Before (old heavy HTML / Word paste)</h3>
    <div class="rendered">{before_html}</div>
  </div>
  <div class="col after">
    <h3>After (live on the site right now)</h3>
    <div class="rendered">{after_html}</div>
  </div>
</div>

<h2>Raw HTML source</h2>
<div class="pair">
  <div class="col before">
    <h3>Before source</h3>
    <pre>{before_escaped}</pre>
  </div>
  <div class="col after">
    <h3>After source</h3>
    <pre>{html_lib.escape(after_html)}</pre>
  </div>
</div>
</body></html>
'''

with open('before-after.html', 'w') as f:
    f.write(out)
print(f'Wrote before-after.html')
print(f'Product: {title}')
print(f'Before: {before_len} chars  |  After: {after_len} chars  ({shrink:.0f}% smaller)')
print(f'Storefront: {storefront_url}')
