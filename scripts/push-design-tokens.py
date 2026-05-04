"""
Push BBI design tokens to a Shopify theme's settings_data.json.

Patches:
  - Top-level settings: header, footer, buttons, badge colors
  - color_schemes['primary']  → BBI default (white canvas)
  - color_schemes['inverse']  → BBI inverse (charcoal canvas)

Env:
  SHOPIFY_TOKEN — Admin API token with write_themes scope
  SHOPIFY_STORE — office-central-online.myshopify.com

Usage:
  python3 scripts/push-design-tokens.py [--live]

  Without --live: prints a diff and exits (safe dry-run).
  With    --live: applies the diff and pushes to the theme.

Target theme: BBI Landing Dev (186373570873) — NEVER the live theme.
"""

import os, sys, json, copy, urllib.request, urllib.error
from datetime import datetime

TOKEN  = os.environ['SHOPIFY_TOKEN']
STORE  = os.environ.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API    = '2026-04'
THEME_ID = '186373570873'   # BBI Landing Dev — dev-only, never publish to live
LIVE   = '--live' in sys.argv

BASE    = f'https://{STORE}/admin/api/{API}'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

# ── Design token values (source of truth: docs/strategy/design-system.md) ──

# Charcoal anchor
CHARCOAL   = '#0B0B0C'
# White
WHITE      = '#FFFFFF'
# Brand red (surface)
RED        = '#D4252A'
# Red text (hover only)
RED_TEXT   = '#A81E22'
# Alt surface
ALT_BG     = '#FAFAFA'
# Decorative border
BORDER     = '#E5E5E7'
# Sold badge
SOLD_GREY  = '#5A5A5E'
# Inverse bg
INV_BG     = '#0B0B0C'
INV_PLATE  = '#161618'
INV_BORDER = '#1F1F21'

# ── Top-level setting patches ──
TOP_LEVEL_PATCH = {
    # Header — white bg, charcoal nav text, red cart badge
    'background_header':          WHITE,
    'header_text':                CHARCOAL,
    'header_text_hover':          RED_TEXT,
    'secondary_background_header': WHITE,
    'secondary_header_text':      CHARCOAL,
    'secondary_header_text_hover': RED_TEXT,
    'header_icon':                CHARCOAL,
    'header_cart_count_bg':       RED,
    'header_cart_count':          WHITE,
    'search_input_color':         CHARCOAL,
    # Footer — charcoal canvas, white text
    'background_footer':          CHARCOAL,
    'footer_text':                WHITE,
    'footer_link':                WHITE,
    'footer_text_hover':          WHITE,    # #A81E22 fails 2.32:1 on charcoal — keep white
    'footer_divider':             INV_BORDER,
    # Buttons — charcoal at rest, red on hover
    'btn_bg_color':               CHARCOAL,
    'btn_text_color':             WHITE,
    'btn_border_color':           CHARCOAL,
    'btn_hover_color':            RED,
    'btn_hover_text_color':       WHITE,
    'btn_hover_border_color':     RED,
    # Badges — normalize to brand anchors
    'saleBadgeBg':                RED,
    'newBadgeBg':                 CHARCOAL,
    'soldBadgeBg':                SOLD_GREY,   # fix broken Liquid template reference
    'marquee_text':               RED,
    # Button radius — squared per brief (0 = sharp, 4px is minimal)
    'button_radius':              True,        # keep enabled; range controls the px value
    'button_radius_desktop':      4,
    'button_radius_mobile':       4,
}

# ── color_schemes patches ──
PRIMARY_SCHEME = {
    'background':                  WHITE,
    'alternate_background':        ALT_BG,
    'background_gradient':         '',
    'heading':                     CHARCOAL,
    'highlight_color':             RED,
    'highlight_solid_color':       WHITE,
    'highlight_text_color':        WHITE,
    'text':                        CHARCOAL,
    'link_text':                   CHARCOAL,
    # Primary button: charcoal → red on hover
    'button_bg':                   CHARCOAL,
    'button_shadow':               CHARCOAL,
    'button_text':                 WHITE,
    'button_border':               CHARCOAL,
    'button_bg_hover':             RED,
    'button_text_hover':           WHITE,
    'button_border_hover':         RED,
    # Secondary button: charcoal outline → invert on hover
    'secondary_button_bg':         WHITE,
    'secondary_button_shadow':     CHARCOAL,
    'secondary_button_text':       CHARCOAL,
    'secondary_button_border':     CHARCOAL,
    'secondary_button_bg_hover':   CHARCOAL,
    'secondary_button_text_hover': WHITE,
    'secondary_button_border_hover': CHARCOAL,
    # Inputs — full-ink border (high-trust procurement treatment)
    'input_bg':                    WHITE,
    'input_text':                  CHARCOAL,
    'input_border':                CHARCOAL,
    # Product
    'product_border':              BORDER,
    'product_media_background':    '',
    # Dividers / misc
    'line_divider':                BORDER,
    'rating_color':                CHARCOAL,   # no goldenrod; charcoal stars
    'arrow_bg':                    WHITE,
    'arrow_color':                 CHARCOAL,
    'card_bg':                     WHITE,
    'card_shadow':                 CHARCOAL,
    'product_card_icon':           CHARCOAL,
    'product_card_icon_background': ALT_BG,
}

INVERSE_SCHEME = {
    'background':                  INV_BG,
    'alternate_background':        INV_PLATE,
    'background_gradient':         '',
    'heading':                     WHITE,
    'highlight_color':             RED,
    'highlight_solid_color':       WHITE,
    'highlight_text_color':        WHITE,
    'text':                        WHITE,
    'link_text':                   WHITE,      # NEVER red-text on charcoal (2.32:1 fail)
    # Primary button on charcoal: white → red on hover
    'button_bg':                   WHITE,
    'button_shadow':               INV_PLATE,
    'button_text':                 CHARCOAL,
    'button_border':               WHITE,
    'button_bg_hover':             RED,
    'button_text_hover':           WHITE,
    'button_border_hover':         RED,
    # Secondary button: white outline → invert on hover
    'secondary_button_bg':         INV_BG,     # transparent — effective canvas
    'secondary_button_shadow':     INV_PLATE,
    'secondary_button_text':       WHITE,
    'secondary_button_border':     WHITE,
    'secondary_button_bg_hover':   WHITE,
    'secondary_button_text_hover': CHARCOAL,
    'secondary_button_border_hover': WHITE,
    # Inputs on charcoal
    'input_bg':                    INV_PLATE,
    'input_text':                  WHITE,
    'input_border':                WHITE,
    # Product / dividers
    'product_border':              INV_BORDER,
    'product_media_background':    '',
    'line_divider':                INV_BORDER,
    'rating_color':                WHITE,
    'arrow_bg':                    INV_PLATE,
    'arrow_color':                 WHITE,
    'card_bg':                     INV_PLATE,
    'card_shadow':                 '#000000',
    'product_card_icon':           WHITE,
    'product_card_icon_background': INV_PLATE,
}

# ── helpers ──
def api_get(path):
    req = urllib.request.Request(f'{BASE}{path}', headers={**HEADERS, 'Content-Type': 'application/json'})
    req.get_method = lambda: 'GET'
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def api_put(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f'{BASE}{path}', data=data, method='PUT', headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def diff_dict(label, old, new):
    changes = []
    for k, v in new.items():
        old_v = old.get(k, '(missing)')
        if str(old_v).lower() != str(v).lower():
            changes.append((k, old_v, v))
    if changes:
        print(f'\n  [{label}]')
        for k, old_v, new_v in changes:
            print(f'    {k}: {old_v!r}  →  {new_v!r}')
    return len(changes)

# ── main ──
print(f'Fetching settings_data.json from theme {THEME_ID}...')
resp = api_get(f'/themes/{THEME_ID}/assets.json?asset[key]=config/settings_data.json')
raw   = resp['asset']['value']
settings = json.loads(raw)
original  = copy.deepcopy(settings)

current  = settings['current']
schemes  = current.get('color_schemes', {})

# Apply top-level patch
total = 0
print('\n── Dry-run diff ────────────────────────────────────────')
total += diff_dict('top-level', current, TOP_LEVEL_PATCH)
current.update(TOP_LEVEL_PATCH)

# Apply primary scheme patch
primary_old = copy.deepcopy(schemes.get('primary', {}).get('settings', {}))
if 'primary' not in schemes:
    schemes['primary'] = {'settings': {}}
schemes['primary']['settings'].update(PRIMARY_SCHEME)
total += diff_dict('color_schemes.primary', primary_old, PRIMARY_SCHEME)

# Apply inverse scheme patch
inverse_old = copy.deepcopy(schemes.get('inverse', {}).get('settings', {}))
if 'inverse' not in schemes:
    schemes['inverse'] = {'settings': {}}
schemes['inverse']['settings'].update(INVERSE_SCHEME)
total += diff_dict('color_schemes.inverse', inverse_old, INVERSE_SCHEME)

print(f'\n── {total} field(s) will change ────────────────────────')

if not LIVE:
    print('\n  Dry-run only. Run with --live to push.')
    sys.exit(0)

# ── live push ──
ts = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_path = f'data/backups/settings_data_dev_{THEME_ID}_pre-ds2-{ts}.json'
with open(backup_path, 'w') as f:
    json.dump(original, f, indent=2)
print(f'\n  Backup written → {backup_path}')

current['color_schemes'] = schemes
payload = {
    'asset': {
        'key': 'config/settings_data.json',
        'value': json.dumps(settings, indent=2),
    }
}
print(f'  Pushing to theme {THEME_ID}...')
result = api_put(f'/themes/{THEME_ID}/assets.json', payload)
print(f'  ✅ Done — updated_at: {result["asset"]["updated_at"]}')
print(f'\n  ⚠  Theme {THEME_ID} is a dev theme. Never publish to live until LAUNCH-2.')
