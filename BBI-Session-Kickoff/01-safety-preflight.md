# Step 1 — Safety Preflight
**Paste this as your first message in every new Claude Code session. Do not skip.**

---

> **Why this exists:** On 2026-05-10, a session pushed `theme.liquid` and two snippet stubs to the live theme (`178274435385`), breaking brantbusinessinteriors.com for ~30 minutes. These rules and the preflight check prevent that from happening again.

---

```
You are working on the Brant Business Interiors Shopify theme.

BEFORE doing anything else, read and lock in these rules:

THEME IDs:
  DEV  (write target) → 186373570873  "BBI Landing Dev"
  LIVE (read-only)    → 178274435385  "BBI Live" — brantbusinessinteriors.com

HARD RULES — no exceptions:
1. Every theme file write (PUT /themes/.../assets.json) must target 186373570873.
2. Every `shopify theme push` must include `--theme 186373570873` explicitly.
3. `push-file.py` is hardcoded to DEV — do not change its THEME_ID.
4. If bbi-push-landing.py shows "WARNING: This is the LIVE theme" → abort immediately. Never type "yes".
5. `fetch-file.py` and `find-liquid-bug.py` may read live for comparison — they never write.
6. Before running any script that touches Shopify, print its THEME_ID and confirm it is 186373570873.

PUSH COMMAND (always use this form):
  export $(grep -v '^#' .env | xargs) && \
    BBI_PUSH_ROOT=$(pwd) python3 scripts/bbi-push-landing.py 186373570873
  Add --layout when touching theme/layout/theme.liquid
  Add --snippets when touching theme/snippets/bbi-*.liquid

PREFLIGHT CHECK — run this now:
  python3 -c "
  import urllib.request, json, os
  TOKEN = os.environ['SHOPIFY_TOKEN']
  STORE = 'office-central-online.myshopify.com'
  for name, tid in [('DEV', '186373570873'), ('LIVE', '178274435385')]:
      req = urllib.request.Request(
          f'https://{STORE}/admin/api/2026-04/themes/{tid}.json',
          headers={'X-Shopify-Access-Token': TOKEN}
      )
      t = json.loads(urllib.request.urlopen(req).read())['theme']
      print(f'{name}: {t[\"name\"]}  role={t[\"role\"]}  id={t[\"id\"]}')
  print('Write target confirmed: 186373570873 (DEV only)')
  "

Now read docs/plan/bbi-build-state.md and BBI-Session-Kickoff/02-current-status.md
to understand current state before starting any work.
```
