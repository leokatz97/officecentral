"""
Purge fal.ai-generated files from the Shopify Files library.

Pass 2 of the fal.ai revert workflow. Run AFTER revert-fal-product-images.py
has detached the AI images from products. This script finds each file in
Shopify's Files library by filename (extracted from the original push CSV's
Shopify_CDN_URL) and deletes it via the Files GraphQL API.

Requires the SHOPIFY_TOKEN to have `write_files` scope. If it doesn't, the
fileDelete call returns an access-denied error and the script aborts loudly.

Usage:
  python3 scripts/purge-fal-files-library.py                                  # dry run
  python3 scripts/purge-fal-files-library.py --live                           # delete from Shopify
  python3 scripts/purge-fal-files-library.py --manifest=path/to.csv --live
  python3 scripts/purge-fal-files-library.py --limit=10 --live                # smoke test
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line)

TOKEN = env['SHOPIFY_TOKEN']
STORE = env.get('SHOPIFY_STORE', 'office-central-online.myshopify.com')
GRAPHQL = 'https://{}/admin/api/2026-04/graphql.json'.format(STORE)
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type':           'application/json',
}

RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
DEFAULT_MANIFEST = os.path.join(RPT_DIR, 'shopify-images-pushed-2026-04-25.csv')
TS = datetime.now().strftime('%Y%m%d-%H%M%S')


def parse_args():
    live     = '--live' in sys.argv
    limit    = None
    manifest = DEFAULT_MANIFEST
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
        elif arg.startswith('--manifest='):
            manifest = arg.split('=', 1)[1]
    return live, limit, manifest


def filename_from_cdn_url(cdn_url):
    """Extract bare filename from a Shopify CDN URL (may include UUID suffix)."""
    if not cdn_url:
        return ''
    path = urllib.parse.urlparse(cdn_url).path
    return path.rsplit('/', 1)[-1]


def slug_from_fal_url(fal_url):
    """Extract the bare slug Shopify indexes by — e.g.
    'SoaW7usHrBGuc7MJAWoSo' from 'https://v3b.fal.media/files/b/.../SoaW7usHrBGuc7MJAWoSo.jpg'.
    Shopify's Files library searches by this slug, NOT the UUID-suffixed CDN filename."""
    if not fal_url:
        return ''
    name = urllib.parse.urlparse(fal_url).path.rsplit('/', 1)[-1]
    return name.rsplit('.', 1)[0]


def gql(query, variables=None, retries=3):
    payload = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GRAPHQL, data=payload, headers=HEADERS, method='POST')
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = attempt * 5
                print('  429 rate limit — sleeping {}s'.format(wait))
                time.sleep(wait)
                last_err = e
                continue
            raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                wait = attempt * 5
                print('  network error (attempt {}/{}): {} — retrying in {}s'.format(attempt, retries, e, wait))
                time.sleep(wait)
    raise last_err


FILES_QUERY = '''
query findFile($q: String!) {
  files(first: 5, query: $q) {
    edges {
      node {
        id
        fileStatus
        ... on MediaImage {
          image { url }
        }
      }
    }
  }
}
'''

DELETE_MUTATION = '''
mutation purge($fileIds: [ID!]!) {
  fileDelete(fileIds: $fileIds) {
    deletedFileIds
    userErrors { field message }
  }
}
'''


def find_file_id(slug):
    """Return MediaImage GID matching the bare fal slug, or None if not found.
    Shopify auto-deletes most orphaned files when product image references go away,
    so 'not found' usually means it's already gone — not an error."""
    resp = gql(FILES_QUERY, {'q': 'filename:{}'.format(slug)})
    if 'errors' in resp:
        raise RuntimeError('GraphQL error: ' + json.dumps(resp['errors'])[:300])

    edges = resp.get('data', {}).get('files', {}).get('edges', [])
    for edge in edges:
        node = edge['node']
        url = node.get('image', {}).get('url') if node.get('image') else None
        # The Files-library URL contains the bare slug; the suffix may or may not be present
        if url and slug in url:
            return node['id']
    return None


def delete_file(file_id):
    """Returns list of deleted IDs, or raises on userErrors."""
    resp = gql(DELETE_MUTATION, {'fileIds': [file_id]})
    if 'errors' in resp:
        raise RuntimeError('GraphQL error: ' + json.dumps(resp['errors'])[:300])
    payload = resp.get('data', {}).get('fileDelete', {})
    user_errors = payload.get('userErrors') or []
    if user_errors:
        raise RuntimeError('userErrors: ' + json.dumps(user_errors)[:300])
    return payload.get('deletedFileIds', [])


def load_manifest(path):
    print('Loading manifest: ' + path)
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('Status') != 'PUSHED':
                continue
            if not row.get('Shopify_CDN_URL'):
                continue
            rows.append(row)
    print('Found {} PUSHED rows with CDN URLs.'.format(len(rows)))
    return rows


def main():
    live, limit, manifest_path = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)

    os.makedirs(LOG_DIR, exist_ok=True)

    rows = load_manifest(manifest_path)

    if limit:
        rows = rows[:limit]
        print('Limiting to first {} files.'.format(limit))

    # Dedup by CDN URL (some files might be referenced from multiple manifest rows)
    seen_urls = set()
    unique_rows = []
    for row in rows:
        url = row['Shopify_CDN_URL']
        if url in seen_urls:
            continue
        seen_urls.add(url)
        unique_rows.append(row)
    rows = unique_rows
    print('{} unique CDN URLs to purge.\n'.format(len(rows)))

    deleted     = []
    not_found   = []
    errors      = []
    result_rows = []

    for i, row in enumerate(rows, 1):
        cdn_url  = row['Shopify_CDN_URL']
        fal_url  = row.get('FAL_Source_URL', '')
        slug     = slug_from_fal_url(fal_url) or filename_from_cdn_url(cdn_url).rsplit('.', 1)[0]
        handle   = row['Handle']
        print('[{}/{}] {} — slug {}'.format(i, len(rows), handle, slug))

        if not live:
            print('  DRY RUN — would lookup + delete via fileDelete')
            result_rows.append({
                'Handle':          handle,
                'Filename':        slug,
                'Shopify_CDN_URL': cdn_url,
                'File_GID':        '',
                'Outcome':         'DRY_RUN',
            })
            continue

        try:
            file_id = find_file_id(slug)
            time.sleep(0.3)
            if not file_id:
                print('  not found in library')
                not_found.append(slug)
                result_rows.append({
                    'Handle':          handle,
                    'Filename':        slug,
                    'Shopify_CDN_URL': cdn_url,
                    'File_GID':        '',
                    'Outcome':         'NOT_FOUND',
                })
                continue

            ids = delete_file(file_id)
            deleted.append(slug)
            print('  DELETED {}'.format(file_id))
            result_rows.append({
                'Handle':          handle,
                'Filename':        slug,
                'Shopify_CDN_URL': cdn_url,
                'File_GID':        file_id,
                'Outcome':         'DELETED',
            })
            time.sleep(0.5)

        except Exception as e:
            msg = str(e)[:300]
            print('  ERROR — {}'.format(msg[:150]))
            errors.append({'handle': handle, 'slug': slug, 'msg': msg})
            result_rows.append({
                'Handle':          handle,
                'Filename':        slug,
                'Shopify_CDN_URL': cdn_url,
                'File_GID':        '',
                'Outcome':         'ERROR',
            })
            # If first attempt fails with access-denied, abort early
            if 'access' in msg.lower() and 'denied' in msg.lower() and len(deleted) == 0:
                print('\nAccess denied on first delete — token likely missing write_files scope. Aborting.')
                break

    out_csv = os.path.join(RPT_DIR, 'fal-files-purge-{}.csv'.format(TS))
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Handle', 'Filename', 'Shopify_CDN_URL',
                                                'File_GID', 'Outcome'])
        writer.writeheader()
        writer.writerows(result_rows)

    log_path = os.path.join(LOG_DIR, 'purge-fal-files-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':          mode,
            'manifest':      manifest_path,
            'unique_files':  len(rows),
            'deleted':       len(deleted),
            'not_found':     len(not_found),
            'errors':        len(errors),
            'error_details': errors,
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Unique files: {}'.format(len(rows)))
    print('  Deleted:      {}'.format(len(deleted)))
    print('  Not found:    {}'.format(len(not_found)))
    print('  Errors:       {}'.format(len(errors)))
    print('  Results CSV:  ' + out_csv)
    print('  Audit log:    ' + log_path)

    if not live:
        print('\n[DRY RUN] No deletes performed. Re-run with --live to purge.')


if __name__ == '__main__':
    main()
