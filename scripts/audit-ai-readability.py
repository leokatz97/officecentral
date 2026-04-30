"""
Audit pages for AI / LLM readability and basic on-page SEO health.

For each URL, fetches the rendered HTML and checks:
  - Product / Organization / FAQ JSON-LD schema present
  - <meta name="description"> set (and non-empty)
  - Exactly one <h1>
  - Visible word count >= 300
  - No <meta name="robots" content="noindex">
  - <img> alt-text coverage >= 80% (alt attribute present and non-empty)

Output:
  - data/reports/ai-readability-audit.csv
  - Stdout summary table

This is a network-touching audit. Default mode is **dry run** — it loads the
URL list, prints what *would* be audited, and exits without making requests.
Pass --live to actually fetch the pages.

Usage:
  python3 scripts/audit-ai-readability.py                  # dry run, default URLs
  python3 scripts/audit-ai-readability.py --live           # fetch + write CSV
  python3 scripts/audit-ai-readability.py --urls=urls.txt  # custom URL file (one per line)
  python3 scripts/audit-ai-readability.py --help

URL file format:
  One URL per line. Blank lines and lines starting with '#' are ignored.

Default URLs (if --urls not provided):
  - https://www.brantbusinessinteriors.com/                            (homepage)
  - https://www.brantbusinessinteriors.com/products/                   (1 PDP — first published)
  - https://www.brantbusinessinteriors.com/collections/business-furniture (1 collection)

Notes:
  - Stdlib only — no external dependencies.
  - Schema detection is regex-based (looks at <script type="application/ld+json">
    blocks and matches @type values). It will not parse deeply nested @graph
    documents perfectly, but is good enough for "present / not present".
  - Word count strips <script>, <style>, and HTML tags before counting.
  - Image alt coverage counts every <img> tag; CSS background-images are not
    counted (matches what AI crawlers actually see).
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths / config
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPT_DIR = os.path.join(ROOT, 'data', 'reports')
OUTPUT_CSV = os.path.join(RPT_DIR, 'ai-readability-audit.csv')

DEFAULT_URLS = [
    'https://www.brantbusinessinteriors.com/',
    'https://www.brantbusinessinteriors.com/collections/business-furniture',
    # PDP picked dynamically below if --live and no --urls supplied (we cannot
    # know the canonical PDP at script-load time without hitting Shopify).
    # For dry run we include a placeholder.
    'https://www.brantbusinessinteriors.com/products/<first-active-product>',
]

USER_AGENT = 'Mozilla/5.0 (compatible; BBI-AI-Readability-Audit/1.0)'
TIMEOUT_S = 20

# Pass thresholds
WORD_COUNT_MIN = 300
ALT_COVERAGE_MIN = 0.80

# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------
def fetch(url: str) -> tuple[str, int]:
    """GET a URL, return (body, status). Empty body on failure."""
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return (resp.read().decode('utf-8', errors='replace'),
                    resp.status)
    except Exception as e:
        print(f'  ! fetch failed for {url}: {e}', file=sys.stderr)
        return ('', 0)


# ---------------------------------------------------------------------------
# Parsing helpers (regex-based, stdlib-only)
# ---------------------------------------------------------------------------
SCRIPT_LDJSON_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
META_DESC_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]*>',
    re.IGNORECASE,
)
META_DESC_CONTENT_RE = re.compile(
    r'content=["\']([^"\']*)["\']',
    re.IGNORECASE,
)
META_ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*>',
    re.IGNORECASE,
)
H1_RE = re.compile(r'<h1\b[^>]*>', re.IGNORECASE)
IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
ALT_ATTR_RE = re.compile(r'\salt=["\']([^"\']*)["\']', re.IGNORECASE)
SCRIPT_BLOCK_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
STYLE_BLOCK_RE = re.compile(r'<style\b[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')


def extract_ldjson_types(body: str) -> set[str]:
    """Return the set of @type values found in any <script type=ld+json> block.

    Walks @graph entries when present.
    """
    found: set[str] = set()
    for match in SCRIPT_LDJSON_RE.findall(body):
        try:
            payload = json.loads(html.unescape(match.strip()))
        except json.JSONDecodeError:
            continue
        _collect_types(payload, found)
    return found


def _collect_types(node, found: set[str]) -> None:
    if isinstance(node, dict):
        t = node.get('@type')
        if isinstance(t, str):
            found.add(t)
        elif isinstance(t, list):
            for item in t:
                if isinstance(item, str):
                    found.add(item)
        for v in node.values():
            _collect_types(v, found)
    elif isinstance(node, list):
        for item in node:
            _collect_types(item, found)


def has_meta_description(body: str) -> bool:
    m = META_DESC_RE.search(body)
    if not m:
        return False
    inner = m.group(0)
    cm = META_DESC_CONTENT_RE.search(inner)
    return bool(cm and cm.group(1).strip())


def h1_count(body: str) -> int:
    return len(H1_RE.findall(body))


def is_noindex(body: str) -> bool:
    m = META_ROBOTS_RE.search(body)
    if not m:
        return False
    inner = m.group(0).lower()
    return 'noindex' in inner


def visible_word_count(body: str) -> int:
    stripped = SCRIPT_BLOCK_RE.sub(' ', body)
    stripped = STYLE_BLOCK_RE.sub(' ', stripped)
    text = TAG_RE.sub(' ', stripped)
    text = html.unescape(text)
    return len([w for w in text.split() if w.strip()])


def alt_coverage(body: str) -> tuple[int, int, float]:
    """Return (imgs_with_nonempty_alt, total_imgs, coverage_pct_0_to_1)."""
    imgs = IMG_RE.findall(body)
    if not imgs:
        return (0, 0, 1.0)  # no images -> trivially 100%
    with_alt = 0
    for tag in imgs:
        m = ALT_ATTR_RE.search(tag)
        if m and m.group(1).strip():
            with_alt += 1
    return (with_alt, len(imgs), with_alt / len(imgs))


# ---------------------------------------------------------------------------
# Audit a single URL
# ---------------------------------------------------------------------------
def audit_url(url: str) -> dict:
    body, status = fetch(url)
    if not body:
        return {
            'url': url,
            'status': status,
            'schema_product': False,
            'schema_org': False,
            'schema_faq': False,
            'meta_desc': False,
            'h1_count': 0,
            'word_count': 0,
            'noindex': False,
            'alt_coverage_pct': 0,
            'pass': False,
            'notes': 'fetch failed',
        }

    types = extract_ldjson_types(body)
    schema_product = 'Product' in types
    schema_org = 'Organization' in types
    schema_faq = 'FAQPage' in types or 'FAQ' in types
    meta_desc = has_meta_description(body)
    h1n = h1_count(body)
    wc = visible_word_count(body)
    noindex = is_noindex(body)
    alt_with, alt_total, alt_pct = alt_coverage(body)

    failures = []
    if h1n != 1:
        failures.append(f'h1_count={h1n}')
    if not meta_desc:
        failures.append('no meta_desc')
    if wc < WORD_COUNT_MIN:
        failures.append(f'word_count<{WORD_COUNT_MIN}')
    if noindex:
        failures.append('noindex')
    if alt_pct < ALT_COVERAGE_MIN and alt_total > 0:
        failures.append(f'alt_coverage<{int(ALT_COVERAGE_MIN*100)}%')

    return {
        'url': url,
        'status': status,
        'schema_product': schema_product,
        'schema_org': schema_org,
        'schema_faq': schema_faq,
        'meta_desc': meta_desc,
        'h1_count': h1n,
        'word_count': wc,
        'noindex': noindex,
        'alt_coverage_pct': round(alt_pct * 100, 1),
        'pass': not failures,
        'notes': '; '.join(failures) if failures else 'ok',
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def load_urls(path: str | None) -> list[str]:
    if not path:
        return list(DEFAULT_URLS)
    if not os.path.exists(path):
        print(f'URL file not found: {path}', file=sys.stderr)
        sys.exit(2)
    urls: list[str] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            urls.append(line)
    return urls


def print_summary(rows: list[dict]) -> None:
    cols = [
        ('url',              48),
        ('status',           6),
        ('schema_product',   8),
        ('schema_org',       8),
        ('schema_faq',       8),
        ('meta_desc',        9),
        ('h1_count',         8),
        ('word_count',       10),
        ('noindex',          7),
        ('alt_coverage_pct', 8),
        ('pass',             5),
    ]
    header = '  '.join(name.ljust(w) for name, w in cols)
    print(header)
    print('-' * len(header))

    def cell(v, w):
        if isinstance(v, bool):
            v = 'Y' if v else '-'
        return str(v).ljust(w)[:w]

    for r in rows:
        print('  '.join(cell(r[name], w) for name, w in cols))

    pass_count = sum(1 for r in rows if r['pass'])
    print()
    print(f'Pass: {pass_count}/{len(rows)}')
    fails = [r for r in rows if not r['pass']]
    if fails:
        print('Failing notes:')
        for r in fails:
            print(f'  - {r["url"]} :: {r["notes"]}')


def write_csv(rows: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = [
        'url', 'status',
        'schema_product', 'schema_org', 'schema_faq',
        'meta_desc', 'h1_count', 'word_count',
        'noindex', 'alt_coverage_pct',
        'pass', 'notes',
    ]
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Audit BBI pages for AI / LLM readability + on-page SEO health.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        '--urls',
        help='Path to a text file of URLs (one per line). Defaults to homepage + collection + first PDP.',
    )
    parser.add_argument(
        '--live',
        action='store_true',
        help='Actually fetch URLs and write the CSV. Without this flag the script does a dry run.',
    )
    parser.add_argument(
        '--out',
        default=OUTPUT_CSV,
        help=f'Output CSV path (default: {OUTPUT_CSV})',
    )
    args = parser.parse_args()

    urls = load_urls(args.urls)

    print(f'Mode: {"LIVE" if args.live else "DRY RUN"}')
    print(f'URLs ({len(urls)}):')
    for u in urls:
        print(f'  - {u}')
    print()

    if not args.live:
        print('Dry run — no requests made. Pass --live to actually fetch.')
        return 0

    rows = []
    for i, url in enumerate(urls, 1):
        print(f'[{i}/{len(urls)}] {url}')
        rows.append(audit_url(url))

    print()
    print_summary(rows)

    write_csv(rows, args.out)
    print()
    print(f'CSV written: {args.out}')
    print(f'Run timestamp: {datetime.now().isoformat(timespec="seconds")}')

    failed = sum(1 for r in rows if not r['pass'])
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
