import urllib.request
import json
import sys
import os

# ⚠️  LABEL CORRECTION (2026-06-26) — the old "LIVE"/"DEV" names here read backwards.
# Ground truth (verify role via GET /themes.json before any push):
#   • 186373570873 ("BBI Landing Dev") = role=main = the LIVE production theme.
#     The name is historical; post-LAUNCH-2 this IS the intended push target.
#   • 178274435385 ("BBI Live")         = UNPUBLISHED, never the target.
# The hard block below exists to stop this script from ever writing to the
# unpublished theme — NOT to keep it off the live theme. IDs are correct as-is;
# only the wording was wrong before. Do not swap the ID values.
BLOCKED_THEME_ID = '178274435385'   # ("BBI Live") UNPUBLISHED — hard-blocked, never push here
TARGET_THEME_ID  = '186373570873'   # ("BBI Landing Dev") role=main — LIVE production target

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = 'office-central-online.myshopify.com'
THEME_ID = TARGET_THEME_ID

if THEME_ID == BLOCKED_THEME_ID:
    print('⛔  BLOCKED: push-file.py would write to the unpublished BBI Live theme (178274435385).')
    print('   THEME_ID must be 186373570873 (role=main, live production) before running.')
    sys.exit(1)

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
