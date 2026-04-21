import urllib.request
import urllib.parse
import json
import re
import os

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
THEME_ID = '178274435385'
API = f'https://{STORE}/admin/api/2026-04'

def fetch_asset_list():
    req = urllib.request.Request(
        f'{API}/themes/{THEME_ID}/assets.json',
        headers={'X-Shopify-Access-Token': TOKEN},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['assets']

def fetch_asset(key):
    url = f'{API}/themes/{THEME_ID}/assets.json?asset[key]={urllib.parse.quote(key)}'
    req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())['asset']

os.makedirs('theme', exist_ok=True)

print('Listing assets...')
assets = fetch_asset_list()
liquid_assets = [a for a in assets if a['key'].endswith(('.liquid', '.js', '.css'))]
print(f'Found {len(liquid_assets)} source files\n')

suspicious = []
for i, asset in enumerate(liquid_assets):
    key = asset['key']
    if not key.endswith('.liquid'):
        continue
    try:
        data = fetch_asset(key)
        content = data.get('value', '')
        # Save locally
        local_path = f'theme/{key}'
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'w') as f:
            f.write(content)
        # Search for division patterns
        for m in re.finditer(r'\|\s*divided_by[^|]*', content):
            matched = m.group(0)
            line_num = content[:m.start()].count('\n') + 1
            line = content.split('\n')[line_num - 1].strip()
            suspicious.append((key, line_num, line, matched))
    except Exception as e:
        print(f'  ERROR {key}: {e}')
    if (i+1) % 20 == 0:
        print(f'  {i+1}/{len(liquid_assets)}...')

print(f'\n=== SUSPICIOUS DIVISIONS (potential divided-by-zero) ===')
for key, ln, line, match in suspicious:
    print(f'\n  {key}:{ln}')
    print(f'    {line}')
