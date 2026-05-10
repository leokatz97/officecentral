import urllib.request
import urllib.parse
import json
import sys

import os
TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
# Read-only fetch — defaults to live for comparison; pass DEV_THEME_ID to fetch from dev.
LIVE_THEME_ID = '178274435385'
DEV_THEME_ID  = '186373570873'
THEME_ID = LIVE_THEME_ID  # read-only: change to DEV_THEME_ID if fetching from dev

key = sys.argv[1] if len(sys.argv) > 1 else 'snippets/product-blocks.liquid'
url = f'https://{STORE}/admin/api/2026-04/themes/{THEME_ID}/assets.json?asset%5Bkey%5D={urllib.parse.quote(key, safe="")}'
req = urllib.request.Request(url, headers={'X-Shopify-Access-Token': TOKEN})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(data['asset']['value'])
