"""
Write descriptions for the 6 'review' products flagged in junk-inspection.json
(real products that just had empty bodies). Descriptions are hand-written
from the product title + price context. Push with --confirm.
"""
import urllib.request
import urllib.error
import json
import sys
import time

with open('.env') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)
TOKEN = env['SHOPIFY_TOKEN']
STORE = env['SHOPIFY_STORE']
API = f'https://{STORE}/admin/api/2026-04'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

# Title-keyed descriptions (title must match exactly in junk-inspection.json)
DESCRIPTIONS = {
    'Desk Top Divider DIVIDE': (
        '<p>Freestanding desk-top privacy divider that adds acoustic separation and visual '
        'privacy between workstations without modifying the desk. Clamps or slots into place '
        'on standard and benching desk configurations.</p>'
        '<ul><li>Tool-free installation — no holes or hardware in the desk</li>'
        '<li>Multiple widths and heights to match your workstation footprint</li>'
        '<li>Fabric-wrapped surface softens ambient noise in open-plan offices</li></ul>'
    ),
    'Fax, Printer, Machine Stand': (
        '<p>Heavy-duty mobile stand built for printers, fax machines, and multi-function '
        'copiers. A stable steel base and lockable casters make it easy to reposition without '
        'unplugging or lifting the machine.</p>'
        '<ul><li>Supports typical office-machine weights</li>'
        '<li>Lower shelf for paper stock and toner storage</li>'
        '<li>Locking casters keep the unit in place during printing</li></ul>'
    ),
    'Hardware for Ceiling Tiles': (
        '<p>Mounting and suspension hardware for acoustic ceiling tiles and drop-ceiling '
        'panels. Includes the clips, wires, and brackets required for a clean installation.</p>'
        '<ul><li>Compatible with standard T-grid ceiling systems</li>'
        '<li>Sized options for small patch jobs through full-room installations</li>'
        '<li>Order to match the tile count and grid spacing of your space</li></ul>'
    ),
    'Honor Roll -DSQ-1824-PB Table Desk - Square Leg Base - 4 Legs x 24" Table Top Width x 18" Table Top Depth 5 EACH': (
        '<p>Honor Roll series square-leg base table desk with a 24" × 18" work surface. Its '
        'compact footprint makes it a fit for training rooms, breakout spaces, touchdown '
        'stations, and child-sized work areas.</p>'
        '<ul><li>Four-leg steel square base for stability on uneven floors</li>'
        '<li>Laminate top resists scratches and daily cleaning</li>'
        '<li>Sold in packs of 5 — ideal for classroom or training-room fit-outs</li></ul>'
    ),
    'Laptop Holder for 100-MA1C & 100-MA2C Monitor Arms only': (
        '<p>Laptop mounting tray that attaches to the 100-MA1C and 100-MA2C monitor arms '
        '<strong>only</strong>. Swap the tray onto the arm in place of a monitor to mount a '
        'laptop for flexible dual-use workstations.</p>'
        '<ul><li>Secure retention clip keeps the laptop in place at any arm angle</li>'
        '<li>Ventilation cutouts prevent overheating during long sessions</li>'
        '<li>Not compatible with other monitor arm models — check your arm SKU before ordering</li></ul>'
    ),
    'Monitor Arms': (
        '<p>Single-monitor articulating arm that frees up desk space and supports ergonomic '
        'screen positioning. Fits most VESA-compatible displays up to standard office '
        'monitor sizes.</p>'
        '<ul><li>Full-motion tilt, swivel, and height adjustment</li>'
        '<li>Clamp and grommet mounts included</li>'
        '<li>Integrated cable management keeps the workstation tidy</li></ul>'
    ),
}


def api_put(pid, body_html, attempt=0):
    payload = json.dumps({'product': {'id': pid, 'body_html': body_html}}).encode()
    req = urllib.request.Request(f'{API}/products/{pid}.json', data=payload, headers=HEADERS, method='PUT')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 5:
            time.sleep(2 ** attempt)
            return api_put(pid, body_html, attempt + 1)
        return e.code, e.read().decode()


def main():
    confirm = '--confirm' in sys.argv
    with open('junk-inspection.json') as f:
        report = json.load(f)
    by_title = {r['title']: r for r in report}

    plan = []
    missing = []
    for title, desc in DESCRIPTIONS.items():
        if title not in by_title:
            missing.append(title)
            continue
        r = by_title[title]
        plan.append({'id': r['id'], 'title': title, 'desc_len': len(desc), 'desc': desc})

    print(f'Will write descriptions for {len(plan)} products:')
    for x in plan:
        print(f'  {x["id"]:18}  {x["title"][:60]}  ({x["desc_len"]} chars)')
    if missing:
        print(f'\nMissing from inspection (title mismatch?): {missing}')

    if not confirm:
        print(f'\nDRY RUN. Pass --confirm to push {len(plan)} descriptions.')
        return

    results = []
    for x in plan:
        status, body = api_put(x['id'], x['desc'])
        ok = status in (200, 201)
        results.append({'id': x['id'], 'title': x['title'], 'status': status, 'ok': ok})
        print(f'  [{"OK" if ok else f"FAIL {status}"}] {x["title"][:55]}')
        time.sleep(0.55)

    succeeded = sum(1 for r in results if r['ok'])
    with open('descriptions-log.json', 'w') as f:
        json.dump({'attempted': len(results), 'succeeded': succeeded, 'results': results}, f, indent=2)
    print(f'\nDone: {succeeded}/{len(results)} pushed.')


if __name__ == '__main__':
    main()
