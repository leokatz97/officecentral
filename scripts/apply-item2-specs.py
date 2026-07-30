#!/usr/bin/env python3
"""ITEM 2 — write researched specs.weight / specs.dimensions (LIVE writes).

Consumes:
  data/reports/item2-research-worklist-2026-06-05.json  (needs + id per handle)
  data/reports/item2-research-results-2026-06-05.json    (workflow output: results[])

Trust bar (Leo): write a value ONLY if it has a MANUFACTURER-DOMAIN url AND a
non-empty verbatim snippet. Otherwise the field is left blank and the product is
flagged unsourceable. Only fills fields the product is actually MISSING (never
overwrites an existing specs value).

Per write: snapshot full state (backup) -> metafieldsSet(specs.weight/dimensions)
-> hardened INDEPENDENT readback (exact match). Checkpoints the log every 25
products. Paces to avoid 429s.

Usage:
  python3 scripts/apply-item2-specs.py            # DRY RUN — prints proposed fills
  python3 scripts/apply-item2-specs.py --live      # apply
"""
import json, sys, time, re, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = '2026-06-05'
ENV = ROOT / '.env'
TOKEN = next((l.split('=', 1)[1].strip().strip('"').strip("'")
              for l in ENV.read_text().splitlines() if l.startswith('SHOPIFY_TOKEN=')), None)
if not TOKEN:
    sys.exit('FATAL: SHOPIFY_TOKEN not loaded from .env')
SHOP = 'office-central-online.myshopify.com'
REST = f'https://{SHOP}/admin/api/2024-10'
GQL = f'{REST}/graphql.json'
HDR = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

# manufacturer-domain allowlist (a url must contain one of these to qualify)
MFR_DOMAINS = [
    'globalfurnituregroup.com', 'global-furniture', 'officestogo.com', 'offices-to-go',
    'heartwoodmfg.com', 'heartwood', 'officestarproducts.com', 'ospfurniture.com', 'officestar.com',
    'safcoproducts.com', 'safco.com', 'fellowes.com', 'mitybilt.com', 'iofurniture.com',
    'intelligentoffice', 'richelieu.com', 'tayco.com', 'kensington.com', 'horizonseating.com',
    'gardex', 'borgo', 'allseating.com', 'obusforme', 'linkscontractfurniture.com', 'links-contract',
]


def is_mfr_domain(url):
    u = (url or '').lower()
    return u.startswith('http') and any(d in u for d in MFR_DOMAINS)


def _open(req):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                wait = 2 ** attempt
                print(f"   (HTTP {e.code} backoff {wait}s)", flush=True)
                time.sleep(wait); continue
            print(f"HTTPError {e.code}: {e.read().decode()[:400]}", file=sys.stderr)
            raise


def gql(query, variables=None):
    req = urllib.request.Request(GQL, data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
                                 headers=HDR, method='POST')
    out = _open(req)
    if 'errors' in out:
        raise RuntimeError(f"GraphQL errors: {out['errors']}")
    return out['data']


MF_SET = '''
mutation($mf: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $mf) {
    metafields { namespace key value }
    userErrors { field message }
  }
}'''

PROD_Q = '''
{ product(id: "gid://shopify/Product/%s") {
    id legacyResourceId handle vendor
    metafields(first: 50) { edges { node { namespace key value } } }
} }'''


def fetch(pid):
    return gql(PROD_Q % pid)['product']


def spec_val(p, key):
    for e in p['metafields']['edges']:
        if e['node']['namespace'] == 'specs' and e['node']['key'] == key:
            return e['node']['value']
    return None


def main():
    live = '--live' in sys.argv
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    work = json.loads((ROOT / 'data' / 'reports' / f'item2-research-worklist-{DATE}.json').read_text())
    needs = {w['handle']: w['needs'] for w in work}
    ids = {w['handle']: w['id'] for w in work}
    res = json.loads((ROOT / 'data' / 'reports' / f'item2-research-results-{DATE}.json').read_text())
    results = res['results'] if isinstance(res, dict) else res

    # Build the proposed-fill plan, honoring the trust bar + only-fill-missing.
    plan = []          # rows we will write
    unsourceable = []  # rows we will flag
    for r in results:
        h = r['handle']
        need = needs.get(h, [])
        fills = {}
        rej = []
        if 'dimensions' in need:
            v, u, s = r.get('dimensions_value', ''), r.get('dimensions_url', ''), r.get('dimensions_snippet', '')
            if v.strip() and is_mfr_domain(u) and s.strip():
                fills['dimensions'] = {'value': v.strip(), 'url': u, 'snippet': s.strip()}
            else:
                rej.append('dimensions')
        if 'weight' in need:
            v, u, s = r.get('weight_value', ''), r.get('weight_url', ''), r.get('weight_snippet', '')
            if v.strip() and is_mfr_domain(u) and s.strip():
                fills['weight'] = {'value': v.strip(), 'url': u, 'snippet': s.strip()}
            else:
                rej.append('weight')
        if fills:
            plan.append({'handle': h, 'id': ids.get(h, r.get('id')), 'fills': fills,
                         'still_missing': rej, 'notes': r.get('notes', '')})
        else:
            unsourceable.append({'handle': h, 'needs': need, 'notes': r.get('notes', '')})

    print(f"=== ITEM 2 specs write {'[LIVE]' if live else '[DRY RUN]'} ===")
    print(f"Research results: {len(results)} | products with >=1 qualifying fill: {len(plan)} | "
          f"unsourceable: {len(unsourceable)}")
    nd = sum(1 for p in plan if 'dimensions' in p['fills'])
    nw = sum(1 for p in plan if 'weight' in p['fills'])
    print(f"Field fills: dimensions={nd}  weight={nw}\n")
    for p in plan:
        print(f"[{p['handle']}]")
        for k, fv in p['fills'].items():
            print(f"   specs.{k} = {fv['value']!r}")
            print(f"       url: {fv['url']}")
            print(f"       snip: {fv['snippet'][:140]!r}")
    # persist the plan + unsourceable list for the report
    (ROOT / 'data' / 'reports' / f'item2-fill-plan-{DATE}.json').write_text(
        json.dumps({'plan': plan, 'unsourceable': unsourceable}, indent=2))

    if not live:
        print(f"\nDRY RUN — {len(plan)} products would be written. Re-run with --live to apply.")
        return

    scopes = [s['handle'] for s in gql('{currentAppInstallation{accessScopes{handle}}}')['currentAppInstallation']['accessScopes']]
    if 'write_products' not in scopes:
        sys.exit("FATAL: token lacks write_products — aborting before any write.")

    bdir = ROOT / 'data' / 'backups'; bdir.mkdir(exist_ok=True)
    ldir = ROOT / 'data' / 'logs'; ldir.mkdir(exist_ok=True)
    logpath = ldir / f'item2-specs-{ts}.log'
    logf = logpath.open('a')
    done = 0
    for i, p in enumerate(plan, 1):
        pid = str(p['id'])
        gid = f'gid://shopify/Product/{pid}'
        cur = fetch(pid)
        # safety: never overwrite an existing specs value
        mset = []
        skipped = []
        for k, fv in p['fills'].items():
            if (spec_val(cur, k) or '').strip():
                skipped.append(k); continue
            mset.append({'ownerId': gid, 'namespace': 'specs', 'key': k,
                         'type': 'single_line_text_field', 'value': fv['value']})
        if not mset:
            print(f"  [{i}/{len(plan)}] SKIP {p['handle']} (already populated: {skipped})")
            continue
        (bdir / f'item2-{p["handle"]}-pre-{ts}.json').write_text(
            json.dumps({'fetched': ts, 'product': cur}, indent=2))
        r = gql(MF_SET, {'mf': mset})
        errs = r['metafieldsSet']['userErrors']
        if errs:
            logf.write(json.dumps({'ts': ts, 'handle': p['handle'], 'error': errs}) + '\n'); logf.flush()
            sys.exit(f"\nXX HALT: metafieldsSet userErrors on {p['handle']}: {errs}")
        time.sleep(0.6)
        rb = fetch(pid)
        ok = True
        rbvals = {}
        for m in mset:
            got = spec_val(rb, m['key'])
            rbvals[m['key']] = got
            if got != m['value']:
                ok = False
        rec = {'ts': ts, 'handle': p['handle'], 'pid': pid,
               'wrote': {m['key']: m['value'] for m in mset},
               'readback': rbvals, 'ok': ok, 'sources': {k: p['fills'][k]['url'] for k in p['fills']}}
        logf.write(json.dumps(rec) + '\n'); logf.flush()
        if not ok:
            sys.exit(f"\nXX HALT: readback MISMATCH on {p['handle']}: {rbvals}")
        done += 1
        print(f"  [{i}/{len(plan)}] OK {p['handle']}  wrote {list(rbvals.keys())}  ✓")
        if done % 25 == 0:
            print(f"   --- checkpoint: {done} written (log flushed) ---")
        time.sleep(0.5)
    logf.close()
    print(f"\n=== DONE: {done} products written, readbacks EXACT-MATCH. Log: {logpath.relative_to(ROOT)} ===")


if __name__ == '__main__':
    main()
