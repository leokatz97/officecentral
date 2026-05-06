"""
Push BBI landing-page files into an unpublished Shopify theme.

Auto-discovers all BBI custom files in theme/:
  - assets/ds-*
  - assets/bbi-*.svg
  - assets/maple-leaf.svg
  - sections/ds-*.liquid
  - snippets/ds-*.liquid
  - templates/page.*.json   ← auto-discovered; a Shopify Page is created for each

Pages are created unpublished and assigned to their matching template suffix.
Page title comes from PAGE_TITLES below; unmapped slugs get a title-cased fallback.

Env:
  SHOPIFY_TOKEN — Admin API token with write_themes + write_content
  SHOPIFY_STORE — office-central-online.myshopify.com
  BBI_PUSH_ROOT — override repo root (default: auto-detected, see below)

Root auto-detection (in priority order):
  1. BBI_PUSH_ROOT env var — explicit override, always wins.
  2. cwd worktree rule — if the current working directory contains
     '.claude/worktrees/' it is a git worktree; use cwd as root so
     worktree files, not main-repo stale files, reach Shopify.
  3. __file__ fallback — parent.parent of this script file (original behaviour).
  A loud WARNING is printed whenever sources 2 and 3 disagree.

Usage:
  python3 scripts/bbi-push-landing.py <THEME_ID>                 # push everything
  python3 scripts/bbi-push-landing.py <THEME_ID> --slug oecm     # one page only
  python3 scripts/bbi-push-landing.py <THEME_ID> --layout        # also push theme.liquid
  python3 scripts/bbi-push-landing.py <THEME_ID> --snippets      # also push bbi-*.liquid snippets
  python3 scripts/bbi-push-landing.py <THEME_ID> --layout --snippets --slug oecm  # all three
"""
import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# ── Human-readable page titles keyed by slug ──────────────────────────────────
# Add an entry here whenever you add a new templates/page.{slug}.json file.
PAGE_TITLES = {
    'quote':        'Request a Quote',
    'oecm':         'OECM Purchasing',
    'brand-dealer': 'ergoCentric Authorized Dealer',
    'healthcare':   'Healthcare Furniture',
    'education':    'Education Furniture',
    'government':   'Government & Municipal Furniture',
    'about':        'About Brant Business Interiors',
    'design-services': 'Space Planning & Design Services',
    'delivery':     'Delivery & Installation',
    'brands':       'Brands We Carry',
    'industries':   'Industries We Serve',
    'non-profit':   'Non-Profit Office Furniture',
    'professional-services': 'Professional Services Office Furniture',
}
# ──────────────────────────────────────────────────────────────────────────────

TOKEN = os.environ['SHOPIFY_TOKEN']
STORE = os.environ.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
API_VERSION = '2026-04'


def _resolve_root() -> Path:
    """Return the repo root to use for this push, with worktree-awareness."""
    # 1. Explicit env override — always wins.
    if env_root := os.environ.get('BBI_PUSH_ROOT'):
        return Path(env_root).resolve()

    cwd = Path.cwd().resolve()
    file_root = Path(__file__).resolve().parent.parent

    # 2. Worktree rule — if cwd is inside a Claude worktree, trust it.
    #    This prevents the silent stale-push bug where the script resolves
    #    to the main repo when invoked from a .claude/worktrees/* context.
    cwd_is_worktree = '.claude/worktrees/' in str(cwd)
    if cwd_is_worktree:
        cwd_root = cwd
        if cwd_root != file_root:
            print(
                f'\n⚠️  ROOT MISMATCH DETECTED\n'
                f'   cwd  (worktree, used): {cwd_root}\n'
                f'   file (skipped):        {file_root}\n'
                f'   Worktree rule wins. Push will use worktree files.\n'
                f'   Set BBI_PUSH_ROOT to silence this warning.\n'
            )
        return cwd_root

    # 3. __file__ fallback — original behaviour.
    #    Warn if cwd looks like a different repo root (theme/ present in cwd
    #    but it differs from the file-derived root).
    if (cwd / 'theme').exists() and cwd != file_root:
        print(
            f'\n⚠️  ROOT MISMATCH DETECTED\n'
            f'   cwd  (has theme/, unused): {cwd}\n'
            f'   file (used):               {file_root}\n'
            f'   If you intended to push from cwd, set BBI_PUSH_ROOT=$(pwd).\n'
        )
    return file_root


ROOT = _resolve_root()
THEME = ROOT / 'theme'
if not THEME.exists():
    raise SystemExit(f'theme/ not found at {THEME} — set BBI_PUSH_ROOT if running from a non-standard location')

TEXT_SUFFIXES = {'.liquid', '.json', '.css', '.js', '.svg'}
BINARY_SUFFIXES = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.ico'}


def make_headers():
    return {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}


def api(method, path, body=None, *, base):
    url = f'{base}{path}'
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=make_headers(), method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode() or '{}'
            return json.loads(raw), resp.status
    except urllib.error.HTTPError as e:
        return {'_error': e.read().decode(), '_code': e.code}, e.code


def upload_file(path: Path, key: str, *, theme_id, base):
    if path.suffix.lower() in BINARY_SUFFIXES:
        data = base64.b64encode(path.read_bytes()).decode()
        body = {'asset': {'key': key, 'attachment': data}}
    else:
        body = {'asset': {'key': key, 'value': path.read_text(encoding='utf-8')}}
    result, code = api('PUT', f'/themes/{theme_id}/assets.json', body, base=base)
    ok = code < 300
    print(f"  {'OK ' if ok else 'FAIL'} {key} ({code})")
    if not ok:
        print(f"       {result.get('_error', result)[:300]}")
    return ok


def files_to_push(slug_filter=None, push_layout=False, push_snippets=False):
    """Yield (Path, shopify_key) pairs for all BBI theme files.

    slug_filter   — if set, only yields the matching section + template for that slug.
                    Always yields shared assets/snippets (no per-slug concept).
    push_layout   — also yield layout/theme.liquid (needed after bbi_landing gate edits).
    push_snippets — also yield snippets/bbi-*.liquid (BBI shared snippets only;
                    Starlite legacy snippets are deliberately excluded).
    """
    shared_patterns = [
        ('assets', 'ds-*'),
        ('assets', 'bbi-*.svg'),
        ('assets', 'maple-leaf.svg'),
        ('snippets', 'ds-*.liquid'),
    ]
    if slug_filter is None:
        # Also push all sections and templates
        shared_patterns += [
            ('sections', 'ds-*.liquid'),
        ]
        template_glob = 'page.*.json'
    else:
        # Only push the section + template for this slug
        shared_patterns += [
            ('sections', f'ds-lp-{slug_filter}.liquid'),
        ]
        template_glob = f'page.{slug_filter}.json'

    for subdir, pattern in shared_patterns:
        target = THEME / subdir
        if not target.exists():
            continue
        for p in sorted(target.glob(pattern)):
            yield p, f'{subdir}/{p.name}'

    templates_dir = THEME / 'templates'
    if templates_dir.exists():
        for p in sorted(templates_dir.glob(template_glob)):
            yield p, f'templates/{p.name}'

    # Optional extras — only when flags are explicitly passed.
    if push_layout:
        layout_file = THEME / 'layout' / 'theme.liquid'
        if layout_file.exists():
            yield layout_file, 'layout/theme.liquid'
        else:
            print(f'  WARN layout/theme.liquid not found at {layout_file} — skipping')

    if push_snippets:
        snippets_dir = THEME / 'snippets'
        if snippets_dir.exists():
            # bbi-*.liquid only — never touch Starlite legacy snippets
            for p in sorted(snippets_dir.glob('bbi-*.liquid')):
                yield p, f'snippets/{p.name}'


def slug_from_template(p: Path) -> str:
    """templates/page.oecm.json → 'oecm'"""
    return p.stem.removeprefix('page.')


def page_title_for(slug: str) -> str:
    return PAGE_TITLES.get(slug, slug.replace('-', ' ').title())


def ensure_page(title, handle, template_suffix, *, base):
    existing, code = api('GET', f'/pages.json?handle={handle}&limit=1', base=base)
    if code >= 300:
        print(f'  FAIL lookup {handle}: {existing}')
        return None
    pages = existing.get('pages', [])
    if pages:
        page_id = pages[0]['id']
        api('PUT', f'/pages/{page_id}.json',
            {'page': {'id': page_id, 'template_suffix': template_suffix}},
            base=base)
        print(f'  OK  page updated  handle={handle} (id={page_id})')
        return page_id
    result, code = api('POST', '/pages.json', {
        'page': {
            'title': title,
            'handle': handle,
            'body_html': '',
            'template_suffix': template_suffix,
            'published': False,
        }
    }, base=base)
    if code >= 300:
        print(f'  FAIL create {handle}: {result}')
        return None
    page_id = result['page']['id']
    print(f'  OK  page created  handle={handle} (id={page_id})')
    return page_id


def main():
    parser = argparse.ArgumentParser(
        description='Push BBI landing-page files to a Shopify dev theme.')
    parser.add_argument('theme_id', help='Shopify theme ID (numeric)')
    parser.add_argument('--slug', default=None,
                        help='Deploy only this slug (e.g. oecm). Omit for all.')
    parser.add_argument('--layout', action='store_true',
                        help='Also push layout/theme.liquid (needed after bbi_landing gate edits).')
    parser.add_argument('--snippets', action='store_true',
                        help='Also push snippets/bbi-*.liquid (BBI shared snippets only).')
    args = parser.parse_args()

    theme_id = args.theme_id
    slug_filter = args.slug
    push_layout = args.layout
    push_snippets = args.snippets
    base = f'https://{STORE}/admin/api/{API_VERSION}'

    print(f'Store   : {STORE}')
    print(f'Root    : {ROOT}')
    print(f'Theme ID: {theme_id}')
    print(f'Slug    : {slug_filter or "all"}')
    print(f'Layout  : {"yes" if push_layout else "no"}')
    print(f'Snippets: {"yes" if push_snippets else "no"}')
    print()

    # Preflight
    info, code = api('GET', f'/themes/{theme_id}.json', base=base)
    if code >= 300:
        print(f'FAIL preflight — theme {theme_id} not reachable: {info}')
        return 1
    theme_info = info['theme']
    print(f'Theme   : {theme_info["name"]}  role={theme_info["role"]}')
    if theme_info['role'] == 'main':
        print('WARNING : This is the LIVE theme. Only dev themes should be used here.')
        answer = input('Type "yes" to continue anyway, or anything else to abort: ').strip().lower()
        if answer != 'yes':
            print('Aborted.')
            return 1
    print()

    # Upload files
    print('Uploading files:')
    ok_count, fail_count = 0, 0
    for path, key in files_to_push(slug_filter, push_layout=push_layout, push_snippets=push_snippets):
        if upload_file(path, key, theme_id=theme_id, base=base):
            ok_count += 1
        else:
            fail_count += 1
    print()
    print(f'Upload: {ok_count} ok, {fail_count} failed')
    if fail_count:
        return 1

    # Ensure pages
    print()
    print('Ensuring Shopify pages exist and are bound to templates:')
    templates_dir = THEME / 'templates'
    template_glob = f'page.{slug_filter}.json' if slug_filter else 'page.*.json'
    created_slugs = []
    if templates_dir.exists():
        for p in sorted(templates_dir.glob(template_glob)):
            slug = slug_from_template(p)
            title = page_title_for(slug)
            ensure_page(title, slug, slug, base=base)
            created_slugs.append(slug)
    print()

    # Preview URLs
    host = STORE.replace('.myshopify.com', '')
    preview_base = f'https://{host}.myshopify.com'
    print('Preview URLs (dev theme only — share via Shopify Preview link):')
    for slug in created_slugs:
        print(f'  {preview_base}/pages/{slug}?preview_theme_id={theme_id}')
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
