import os
import re
import json
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

PAGES = [
    "https://officecentralinteriors.com/",
    "https://officecentralinteriors.com/inspiration/",
    "https://officecentralinteriors.com/references/",
    "https://officecentralinteriors.com/services/",
    "https://officecentralinteriors.com/industry-sector-furniture/",
]

PEXELS_PATTERN = re.compile(r'pexels', re.IGNORECASE)
LOGO_PATTERN = re.compile(r'(logo|icon|favicon)', re.IGNORECASE)
UPLOADS_PATTERN = re.compile(r'officecentralinteriors\.com/wp-content/uploads/(.+)')

CATEGORY_RULES = [
    (re.compile(r'^Mattamy-', re.IGNORECASE), 'project/mattamy', 'Our Work page'),
    (re.compile(r'^OCI-Healthcare-', re.IGNORECASE), 'sector/healthcare', 'Healthcare landing page'),
    (re.compile(r'^OCI-Government-', re.IGNORECASE), 'sector/government', 'Government landing page'),
    (re.compile(r'^OCI-Education-', re.IGNORECASE), 'sector/education', 'Education landing page'),
    (re.compile(r'^OCI-Workplace-', re.IGNORECASE), 'sector/workplace', 'Workplace landing page'),
    (re.compile(r'^OCi-Retail-|^OCI-Retail-', re.IGNORECASE), 'sector/retail', 'Retail landing page'),
    (re.compile(r'^OCI-Hospitality-', re.IGNORECASE), 'sector/hospitality', 'Hospitality landing page'),
    (re.compile(r'^OCI-Service-Excellence-', re.IGNORECASE), 'installation', 'Our Work page / homepage'),
    (re.compile(r'^Inspiration-', re.IGNORECASE), 'inspiration', 'Inspiration / homepage hero'),
    (re.compile(r'^About-us-', re.IGNORECASE), 'brand', 'About page / homepage'),
    (re.compile(r'^Pods-', re.IGNORECASE), 'product/pods', 'Acoustic pods category page'),
    (re.compile(r'^Lounge-', re.IGNORECASE), 'product/lounge', 'Lounge collection page'),
    (re.compile(r'^Subject-Areas-', re.IGNORECASE), 'inspiration', 'Inspiration / boardroom hero'),
    (re.compile(r'^Moss-wall-', re.IGNORECASE), 'inspiration', 'Inspiration / specialty'),
    (re.compile(r'^OCI-Services-', re.IGNORECASE), 'services', 'Services page'),
    (re.compile(r'^Smart-workspace-', re.IGNORECASE), 'services', 'Smart workspaces page'),
]


class ImgScraper(HTMLParser):
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.found = []

    def handle_starttag(self, tag, attrs):
        if tag in ('img', 'source'):
            for attr, val in attrs:
                if attr in ('src', 'srcset', 'data-src') and val:
                    for part in val.split(','):
                        url = part.strip().split(' ')[0]
                        if url:
                            self.found.append(urljoin(self.page_url, url))


def extract_oci_url(raw_url):
    """Convert CDN URL or direct URL to canonical wp-content/uploads URL."""
    m = UPLOADS_PATTERN.search(raw_url)
    if not m:
        return None
    path = m.group(1)
    # Strip CDN resize params (e.g. ?resize=300,200&ssl=1)
    path = path.split('?')[0]
    # Skip anything that looks like a scaled/resized intermediate
    if re.search(r'-\d+x\d+\.(jpg|jpeg|png|webp|gif)$', path, re.IGNORECASE):
        return None
    return f"https://officecentralinteriors.com/wp-content/uploads/{path}", path


def categorize(filename):
    for pattern, category, suggested_use in CATEGORY_RULES:
        if pattern.match(filename):
            return category, suggested_use
    return 'general', 'Homepage / general'


def fetch_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='replace')


def main():
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'oci-photos')
    os.makedirs(out_dir, exist_ok=True)

    seen_urls = {}  # canonical_url -> list of pages found on

    for page_url in PAGES:
        print(f"Fetching {page_url} ...")
        try:
            html = fetch_page(page_url)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        parser = ImgScraper(page_url)
        parser.feed(html)

        for raw in parser.found:
            result = extract_oci_url(raw)
            if not result:
                continue
            canonical, path = result
            filename = os.path.basename(path)
            if PEXELS_PATTERN.search(filename) or LOGO_PATTERN.search(filename):
                continue
            if canonical not in seen_urls:
                seen_urls[canonical] = []
            page_path = '/' + page_url.replace('https://officecentralinteriors.com', '').lstrip('/')
            if page_path not in seen_urls[canonical]:
                seen_urls[canonical].append(page_path)

    print(f"\nFound {len(seen_urls)} unique OCI photos. Downloading...")

    catalog = []
    for canonical_url, pages_found in sorted(seen_urls.items()):
        filename = os.path.basename(urlparse(canonical_url).path)
        dest = os.path.join(out_dir, filename)

        if os.path.exists(dest):
            print(f"  [skip] {filename} (already downloaded)")
        else:
            try:
                req = urllib.request.Request(canonical_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                with open(dest, 'wb') as f:
                    f.write(data)
                size_kb = len(data) // 1024
                print(f"  [ok]   {filename} ({size_kb} KB)")
            except Exception as e:
                print(f"  [err]  {filename}: {e}")
                continue

        category, suggested_use = categorize(filename)
        catalog.append({
            "filename": filename,
            "source_url": canonical_url,
            "found_on": pages_found,
            "category": category,
            "suggested_use": suggested_use,
        })

    catalog.sort(key=lambda x: (x['category'], x['filename']))
    catalog_path = os.path.join(out_dir, 'catalog.json')
    with open(catalog_path, 'w') as f:
        json.dump(catalog, f, indent=2)

    print(f"\nDone. {len(catalog)} photos saved to data/oci-photos/")
    print(f"Catalog written to data/oci-photos/catalog.json")

    by_category = {}
    for entry in catalog:
        by_category.setdefault(entry['category'], []).append(entry['filename'])
    print("\nBy category:")
    for cat, files in sorted(by_category.items()):
        print(f"  {cat}: {len(files)} photos")


if __name__ == '__main__':
    main()
