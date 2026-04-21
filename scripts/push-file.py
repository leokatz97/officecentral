import urllib.request
import json
import sys

import os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
THEME_ID = '178274435385'

key = sys.argv[1]
local_path = sys.argv[2] if len(sys.argv) > 2 else f'theme/{key}'

with open(local_path) as f:
    content = f.read()

payload = json.dumps({'asset': {'key': key, 'value': content}}).encode()

req = urllib.request.Request(
    f'https://{STORE}/admin/api/2026-04/themes/{THEME_ID}/assets.json',
    data=payload,
    method='PUT',
    headers={
        'X-Shopify-Access-Token': TOKEN,
        'Content-Type': 'application/json',
    },
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f'✅ Pushed {key}')
        print(f'   updated_at: {data["asset"]["updated_at"]}')
except urllib.error.HTTPError as e:
    print(f'❌ Error {e.code}: {e.read().decode()}')
