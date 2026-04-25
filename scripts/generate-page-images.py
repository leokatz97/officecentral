"""
Generate 2 hero images per BBI landing page using fal.ai flux/schnell.

For each page:
  - product.jpg: the featured SKU in a polished commercial setting
  - space.jpg:   a full room scene capturing the page atmosphere

Pages where a real OCI photo already covers the space concept are noted in
the manifest as SOURCE=OCI_PHOTO and skipped for space image generation.

Output:   data/page-images/{page-slug}/{page-slug}-product.jpg
                           {page-slug}/{page-slug}-space.jpg
Manifest: data/reports/generated-page-images-YYYY-MM-DD.csv
Log:      data/logs/page-image-generation-YYYYMMDD-HHMMSS.json

Usage:
  python3 scripts/generate-page-images.py              # dry run
  python3 scripts/generate-page-images.py --live       # call fal.ai + download
  python3 scripts/generate-page-images.py --limit=3 --live  # smoke test
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & credentials
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, '.env')) as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.strip().startswith('#'))

FAL_KEY = env['FAL_KEY']

IMG_DIR = os.path.join(ROOT, 'data', 'page-images')
RPT_DIR = os.path.join(ROOT, 'data', 'reports')
LOG_DIR = os.path.join(ROOT, 'data', 'logs')
OCI_CAT = os.path.join(ROOT, 'data', 'oci-photos', 'catalog.json')
TODAY   = datetime.now().strftime('%Y-%m-%d')
TS      = datetime.now().strftime('%Y%m%d-%H%M%S')

FAL_ENDPOINT = 'https://fal.run/fal-ai/flux-pro'

# ---------------------------------------------------------------------------
# Page specs: slug -> (product_prompt, space_prompt)
# ---------------------------------------------------------------------------
PAGE_SPECS = [
    ('homepage', (
        "Professional commercial photograph of a modern L-shape executive desk and an "
        "ObusForme ergonomic office chair, shot on a clean white studio background, "
        "crisp even lighting, sharp detail, slight drop shadow, catalogue style. "
        "No people, no text overlays.",

        "Wide-angle photograph of a bright, modern Canadian executive open-plan office. "
        "Floor-to-ceiling windows with natural light, neutral tones, polished concrete "
        "floors, a mix of ergonomic task chairs and sit-stand desks. Clean, professional, "
        "institutional feel. No people, no text overlays.",
    )),
    ('task-seating', (
        "Professional product photography of the ObusForme Comfort High Back ergonomic "
        "office chair on a clean white studio background, slight drop shadow, crisp "
        "lighting, commercial catalogue style. No people, no text overlays.",

        "Wide-angle photograph of a modern multi-desk office with multiple ergonomic task "
        "chairs at height-adjustable desks, warm natural light from large windows, neutral "
        "palette, healthy ergonomic workspace vibe. No people, no text overlays.",
    )),
    ('desks', (
        "Professional product photography of an L-shape office desk with an upper hutch "
        "storage unit, warm wood-grain finish, on a clean white studio background, "
        "commercial catalogue lighting. No people, no text overlays.",

        "Corner executive office with large L-shape desk bathed in natural window light, "
        "contemporary wood and metal finishes, potted plant accent, tidy desktop. "
        "Realistic architectural interior photography. No people, no text overlays.",
    )),
    ('storage', (
        "Professional product photography of a tall lateral file cabinet, Made in Canada, "
        "charcoal grey steel finish, on a clean white studio background, sharp catalogue "
        "lighting, slight drop shadow. No people, no text overlays.",

        "Institutional filing corridor with rows of lateral file cabinets in a modern "
        "government or hospital administrative office, fluorescent and natural light, "
        "clean neutral palette. Architectural interior photography. No people, no text overlays.",
    )),
    ('collaboration', (
        "Professional product photography of a large rectangular boardroom conference "
        "table paired with premium Keilhauer upholstered boardroom chairs, clean white "
        "studio background, commercial catalogue style. No people, no text overlays.",

        "Formal Canadian corporate boardroom with a long polished conference table, "
        "high-back upholstered chairs, floor-to-ceiling windows overlooking a city skyline, "
        "elegant neutral decor, warm ambient lighting. No people, no text overlays.",
    )),
    ('home-office', (
        "Professional product photography of a compact L-shape sit-stand desk in a white "
        "finish on a clean white studio background, commercial catalogue lighting. "
        "No people, no text overlays.",

        "Bright residential home office nook with a compact sit-stand desk, ergonomic "
        "chair, large window, built-in shelving, plants. Warm Scandinavian interior style. "
        "No people, no text overlays.",
    )),
    ('acoustic-pods', (
        "Professional product photography of a freestanding office acoustic privacy pod "
        "with upholstered walls and integrated seating, on a clean white studio background, "
        "commercial catalogue style. No people, no text overlays.",

        "Open-plan modern office with an acoustic privacy pod installed among workstations, "
        "warm interior lighting inside the pod contrasting the bright open office, "
        "contemporary Scandinavian style. No people, no text overlays.",
    )),
    ('healthcare', (
        "Professional product photography of a bariatric healthcare office chair with "
        "antimicrobial upholstery on a clean white studio background, catalogue lighting. "
        "No people, no text overlays.",

        "Modern clinical nursing station or hospital hallway with healthcare-grade furniture "
        "including a reception desk and chairs, clean white and blue palette, institutional "
        "lighting, spotless surfaces. No people, no text overlays.",
    )),
    ('education', (
        "Professional product photography of a rectangular training table with stackable "
        "educational chairs on a clean white studio background, commercial catalogue style. "
        "No people, no text overlays.",

        "Modern school library or classroom study space with collaborative training tables "
        "and chairs arranged in groups, bright natural light through windows, educational "
        "furniture in primary colours on a neutral background. No people, no text overlays.",
    )),
    ('government', (
        "Professional product photography of a panel workstation system with overhead "
        "storage and a task chair on a clean white studio background, commercial "
        "catalogue lighting. No people, no text overlays.",

        "Canadian government open-plan administrative office with rows of panel workstation "
        "systems, neutral grey fabric panels, institutional ceiling, fluorescent and natural "
        "light. Realistic interior photography. No people, no text overlays.",
    )),
    ('non-profit', (
        "Professional product photography of a simple task chair and a rectangular desk "
        "on a clean white studio background, commercial catalogue style. "
        "No people, no text overlays.",

        "Warm community organization office with modest task chairs, simple desks, "
        "motivational wall art, bright natural light, colourful accents. Inviting and "
        "friendly atmosphere. No people, no text overlays.",
    )),
    ('professional-services', (
        "Professional product photography of a height-adjustable sit-stand desk in a "
        "light oak finish on a clean white studio background, catalogue lighting. "
        "No people, no text overlays.",

        "Modern professional services office — law firm or consulting studio — with "
        "sit-stand desks, glass partitions, polished floors, city window view. "
        "Sophisticated neutral palette. No people, no text overlays.",
    )),
    ('design-services', (
        "Professional product photography of a space-planning model showing an office "
        "furniture layout concept on a clean white studio background, architectural "
        "scale model style. No people, no text overlays.",

        "Open-plan office in the space-planning stage with architectural drawings and "
        "furniture samples visible on a planning table, bright design studio, moodboard "
        "on the wall. Creative professional interior. No people, no text overlays.",
    )),
    ('collections-hub', (
        "Professional product photography collage of three office furniture categories — "
        "an ergonomic chair, a sit-stand desk, and a lateral file cabinet — arranged "
        "neatly on a clean white studio background. Commercial catalogue style. "
        "No people, no text overlays.",

        "Wide-angle multi-zone modern office showing a task-seating zone, a collaboration "
        "zone with a boardroom table, and a private office zone, all in one open-plan "
        "space, bright natural light. No people, no text overlays.",
    )),
    ('verticals-hub', (
        "Professional composite photograph showing four office environments side by side: "
        "a school classroom, a hospital nursing station, a government office, and a "
        "corporate boardroom — each with appropriate institutional furniture. "
        "No people, no text overlays.",

        "Split-panel wide-angle interior photograph: Canadian government open-plan office "
        "on the left, healthcare nursing station on the right, clean institutional "
        "environments, bright lighting. No people, no text overlays.",
    )),
    ('keilhauer', (
        "Professional product photography of a Keilhauer premium upholstered boardroom "
        "chair, warm leather finish, on a clean white studio background, editorial "
        "catalogue lighting. No people, no text overlays.",

        "Upscale Toronto corporate boardroom with Keilhauer chairs around a dark polished "
        "conference table, city skyline through floor-to-ceiling windows, sophisticated "
        "dark wood and steel finishes. No people, no text overlays.",
    )),
    ('global-teknion', (
        "Professional product photography of a modular panel workstation system with "
        "Global Upholstery and Teknion aesthetic — clean lines, fabric panels, integrated "
        "storage — on a white studio background. No people, no text overlays.",

        "Corporate systems-furniture open-plan office with rows of Teknion-style panel "
        "workstations, consistent grey fabric, glass partitions, abundant natural light. "
        "Clean architectural interior. No people, no text overlays.",
    )),
    ('ergocentric', (
        "Professional product photography of an ergoCentric all33 or TechONE ergonomic "
        "task chair, Canadian-made, on a clean white studio background, sharp catalogue "
        "lighting, slight drop shadow. No people, no text overlays.",

        "Ergonomics-focused modern office with ergoCentric task chairs at height-adjustable "
        "desks, monitor arms, keyboard trays, bright open workspace, motivational ergonomics "
        "poster on the wall. No people, no text overlays.",
    )),
    ('business-furniture', (
        "Professional product photography of a curated grouping of Canadian commercial office "
        "furniture — an executive desk, an ergonomic task chair, and a lateral file cabinet — "
        "arranged neatly on a clean white studio background, commercial catalogue lighting. "
        "No people, no text overlays.",

        "Wide-angle photograph of a modern Canadian open-plan business office showing multiple "
        "furniture zones: a workstation area, a collaboration table, and a private office nook, "
        "all in a cohesive neutral palette with abundant natural light. "
        "No people, no text overlays.",
    )),
    ('seating', (
        "Professional product photography of four distinct office seating types — a high-back "
        "executive chair, a mid-back mesh task chair, an upholstered lounge chair, and a "
        "stackable guest chair — arranged on a clean white studio background, commercial "
        "catalogue lighting. No people, no text overlays.",

        "Bright modern Canadian office interior showcasing multiple seating zones: ergonomic "
        "task chairs at desks, upholstered lounge seating near a window wall, and stackable "
        "chairs around a training table. Warm natural light, neutral palette. "
        "No people, no text overlays.",
    )),
    ('tables', (
        "Professional product photography of a rectangular meeting table with a wood-grain "
        "laminate top and metal legs on a clean white studio background, commercial catalogue "
        "lighting, slight drop shadow. No people, no text overlays.",

        "Modern corporate training room with flip-top tables configured in a classroom layout, "
        "bright overhead lighting, neutral grey carpet, clean institutional interior. "
        "Architectural interior photography. No people, no text overlays.",
    )),
    ('boardroom', (
        "Professional product photography of a large oval conference table with a dark walnut "
        "veneer finish and integrated cable management on a clean white studio background, "
        "commercial catalogue lighting. No people, no text overlays.",

        "Formal Canadian corporate boardroom with a long polished conference table, premium "
        "upholstered chairs, integrated AV credenza with screens, floor-to-ceiling windows "
        "overlooking a city. Sophisticated neutral decor, warm ambient lighting. "
        "No people, no text overlays.",
    )),
    ('ergonomic-products', (
        "Professional product photography of a height-adjustable sit-stand desk with a dual "
        "monitor arm and an ergonomic keyboard tray, clean white studio background, sharp "
        "commercial catalogue lighting. No people, no text overlays.",

        "Ergonomics-focused modern office with sit-stand desks at standing height, dual monitor "
        "arms, under-desk keyboard trays, anti-fatigue mats, warm open workspace with large "
        "windows. Healthy workplace interior photography. No people, no text overlays.",
    )),
    ('panels-room-dividers', (
        "Professional product photography of a freestanding fabric-wrapped room divider panel "
        "in a neutral grey finish on a clean white studio background, commercial catalogue "
        "lighting. No people, no text overlays.",

        "Open-plan Canadian office subdivided with full-height fabric room dividers and "
        "desktop privacy panels creating individual workstation zones, warm neutral palette, "
        "natural light filtering through. Modern institutional interior. "
        "No people, no text overlays.",
    )),
    ('accessories', (
        "Professional product photography of a curated grouping of office accessories — a "
        "clear chairmat, a power module strip, a sleek coat rack, and a modern LED desk lamp — "
        "arranged on a clean white studio background, catalogue lighting. "
        "No people, no text overlays.",

        "Well-appointed modern office workstation with a chairmat underfoot, integrated power "
        "module on the desk surface, coat rack in the corner, and task lighting, all in a "
        "clean neutral office environment. No people, no text overlays.",
    )),
    ('quiet-spaces', (
        "Professional product photography of a freestanding office phone booth pod with "
        "acoustic upholstered walls, glass door, and integrated ventilation on a clean white "
        "studio background, commercial catalogue style. No people, no text overlays.",

        "Modern open-plan office with a standalone acoustic phone booth and a larger "
        "two-person quiet pod installed among workstations, sound-dampening ceiling baffles "
        "overhead, warm interior lighting inside the pods. No people, no text overlays.",
    )),
    ('industries-hub', (
        "Professional composite photograph of four Canadian institutional furniture settings: "
        "a corporate office workstation, a healthcare reception desk, a government "
        "administrative workspace, and an educational training table, each on a clean white "
        "studio background arranged in a 2x2 grid. No people, no text overlays.",

        "Split wide-angle interior photograph showing a corporate open-plan office on the left "
        "and a modern institutional workspace on the right, both featuring Canadian commercial "
        "furniture, clean neutral environments, bright institutional lighting. "
        "No people, no text overlays.",
    )),
    ('brands-hub', (
        "Professional product photography showcase of three premium Canadian office chairs — "
        "a Keilhauer upholstered boardroom chair, a Global Upholstery executive chair, and an "
        "ergoCentric task chair — on a clean white studio background, editorial catalogue "
        "lighting. No people, no text overlays.",

        "Elegant office furniture showroom interior with curated displays of premium task "
        "chairs, executive seating, and ergonomic products on raised platforms, warm accent "
        "lighting, clean white walls and polished concrete floors. "
        "No people, no text overlays.",
    )),
    ('delivery', (
        "Professional product photography of neatly flat-packed office furniture boxes and "
        "hardware kits arranged on a clean white studio background with assembly tools laid "
        "out precisely, commercial catalogue lighting. No people, no text overlays.",

        "Freshly delivered and installed modern Canadian office — pristine workstations, "
        "chairs perfectly positioned, desks clear and ready, under warm overhead lighting, "
        "as if just completed by an installation team. Clean institutional interior. "
        "No people, no text overlays.",
    )),
]

# Pages where an OCI photo already covers the space concept well enough that
# we skip AI generation for the space image.
# Key = page slug, value = OCI catalog filename
OCI_SPACE_COVERAGE = {
    'homepage':       'office-sitting-room-executive-sitting-1.jpg',
    'collaboration':  'Subject-Areas-boardroom.jpg',
    'acoustic-pods':  'Pods-4-1.jpg',
    'healthcare':     'OCI-Healthcare-Carousel-3.jpg',
    'education':      'OCI-Education-1.jpg',
    'government':     'OCI-Government-Federal-Furniture-Gallery-Image-1.jpg',
    'design-services': 'OCI-Planning-Desogn.jpg',
    'relocation':      'OCI-Services-Relocation-management.jpg',
}


# ---------------------------------------------------------------------------
# fal.ai API
# ---------------------------------------------------------------------------
def call_fal(prompt, max_retries=3):
    body = json.dumps({
        'prompt':              prompt,
        'image_size':          'landscape_16_9',
        'num_images':          1,
    }).encode()
    headers = {
        'Authorization': 'Key ' + FAL_KEY,
        'Content-Type':  'application/json',
    }
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(FAL_ENDPOINT, data=body, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
                url  = data['images'][0]['url']
                time.sleep(1)
                return url
        except urllib.error.HTTPError as e:
            code = e.code
            msg  = e.read().decode()[:200]
            if code in (400, 401, 403):
                print('    fal.ai {} error (will not retry): {}'.format(code, msg[:100]))
                return None
            wait = 2 ** (attempt + 1)
            print('    fal.ai {} (attempt {}/{}), retrying in {}s'.format(
                code, attempt + 1, max_retries, wait))
            time.sleep(wait)
        except Exception as e:
            wait = 2 ** (attempt + 1)
            print('    fal.ai error (attempt {}/{}): {}, retrying in {}s'.format(
                attempt + 1, max_retries, e, wait))
            time.sleep(wait)
    return None


# ---------------------------------------------------------------------------
# Image download
# ---------------------------------------------------------------------------
def download_image(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print('    Download error: {}'.format(e))
        return False


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------
def parse_args():
    live  = '--live' in sys.argv
    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=', 1)[1])
    return live, limit


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    live, limit = parse_args()
    mode = 'LIVE' if live else 'DRY RUN'
    print('Mode: ' + mode)

    os.makedirs(RPT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    pages = list(PAGE_SPECS)
    if limit:
        pages = pages[:limit]
        print('Limiting to first {} page(s).'.format(limit))

    # Count pending (non-skipped) images
    pending = 0
    for slug, (prod_prompt, space_prompt) in pages:
        page_dir = os.path.join(IMG_DIR, slug)
        prod_path  = os.path.join(page_dir, '{}-product.jpg'.format(slug))
        space_path = os.path.join(page_dir, '{}-space.jpg'.format(slug))
        if not os.path.exists(prod_path):
            pending += 1
        if slug not in OCI_SPACE_COVERAGE and not os.path.exists(space_path):
            pending += 1

    cost_low  = pending * 0.045
    cost_high = pending * 0.055
    print('Pages: {} | Pending images: {} | Est. cost: ${:.2f}-${:.2f}'.format(
        len(pages), pending, cost_low, cost_high))

    if live and cost_high > 2.00:
        ans = input('\nEstimated cost exceeds $2. Type YES to continue: ')
        if ans.strip().upper() != 'YES':
            sys.exit('Aborted.')

    print()

    manifest_rows = []
    generated     = 0
    skipped       = 0
    errors        = []
    total         = len(pages)

    for i, (slug, (prod_prompt, space_prompt)) in enumerate(pages, 1):
        print('[{}/{}] {}'.format(i, total, slug))
        page_dir = os.path.join(IMG_DIR, slug)
        os.makedirs(page_dir, exist_ok=True)

        # --- Product image (Type A) ---
        prod_path = os.path.join(page_dir, '{}-product.jpg'.format(slug))
        if os.path.exists(prod_path):
            print('  product: SKIP (already exists)')
            skipped += 1
            manifest_rows.append({
                'Page': slug, 'Type': 'product', 'Local_Path': prod_path,
                'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': prod_prompt,
                'Status': 'SKIPPED_EXISTS',
            })
        elif not live:
            print('  product: DRY RUN -> {}-product.jpg'.format(slug))
            manifest_rows.append({
                'Page': slug, 'Type': 'product', 'Local_Path': prod_path,
                'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': prod_prompt,
                'Status': 'DRY_RUN',
            })
        else:
            fal_url = call_fal(prod_prompt)
            if not fal_url:
                print('  product: ERROR - fal.ai returned no URL')
                errors.append({'page': slug, 'type': 'product', 'stage': 'fal'})
                manifest_rows.append({
                    'Page': slug, 'Type': 'product', 'Local_Path': prod_path,
                    'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': prod_prompt,
                    'Status': 'ERROR',
                })
            else:
                ok = download_image(fal_url, prod_path)
                if ok:
                    size_kb = os.path.getsize(prod_path) // 1024
                    print('  product: OK ({} KB)'.format(size_kb))
                    generated += 1
                    manifest_rows.append({
                        'Page': slug, 'Type': 'product', 'Local_Path': prod_path,
                        'FAL_URL': fal_url, 'Source': 'GENERATED', 'Prompt': prod_prompt,
                        'Status': 'OK',
                    })
                else:
                    print('  product: ERROR - download failed')
                    errors.append({'page': slug, 'type': 'product', 'stage': 'download', 'fal_url': fal_url})
                    manifest_rows.append({
                        'Page': slug, 'Type': 'product', 'Local_Path': prod_path,
                        'FAL_URL': fal_url, 'Source': 'GENERATED', 'Prompt': prod_prompt,
                        'Status': 'ERROR',
                    })

        # --- Space image (Type B) ---
        space_path = os.path.join(page_dir, '{}-space.jpg'.format(slug))

        if slug in OCI_SPACE_COVERAGE:
            oci_file = OCI_SPACE_COVERAGE[slug]
            oci_full = os.path.join(ROOT, 'data', 'oci-photos', oci_file)
            print('  space:   SKIP (OCI photo covers this) -> {}'.format(oci_file))
            skipped += 1
            manifest_rows.append({
                'Page': slug, 'Type': 'space', 'Local_Path': oci_full,
                'FAL_URL': '', 'Source': 'OCI_PHOTO', 'Prompt': space_prompt,
                'Status': 'SKIPPED_OCI',
            })
        elif os.path.exists(space_path):
            print('  space:   SKIP (already exists)')
            skipped += 1
            manifest_rows.append({
                'Page': slug, 'Type': 'space', 'Local_Path': space_path,
                'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': space_prompt,
                'Status': 'SKIPPED_EXISTS',
            })
        elif not live:
            print('  space:   DRY RUN -> {}-space.jpg'.format(slug))
            manifest_rows.append({
                'Page': slug, 'Type': 'space', 'Local_Path': space_path,
                'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': space_prompt,
                'Status': 'DRY_RUN',
            })
        else:
            fal_url = call_fal(space_prompt)
            if not fal_url:
                print('  space:   ERROR - fal.ai returned no URL')
                errors.append({'page': slug, 'type': 'space', 'stage': 'fal'})
                manifest_rows.append({
                    'Page': slug, 'Type': 'space', 'Local_Path': space_path,
                    'FAL_URL': '', 'Source': 'GENERATED', 'Prompt': space_prompt,
                    'Status': 'ERROR',
                })
            else:
                ok = download_image(fal_url, space_path)
                if ok:
                    size_kb = os.path.getsize(space_path) // 1024
                    print('  space:   OK ({} KB)'.format(size_kb))
                    generated += 1
                    manifest_rows.append({
                        'Page': slug, 'Type': 'space', 'Local_Path': space_path,
                        'FAL_URL': fal_url, 'Source': 'GENERATED', 'Prompt': space_prompt,
                        'Status': 'OK',
                    })
                else:
                    print('  space:   ERROR - download failed')
                    errors.append({'page': slug, 'type': 'space', 'stage': 'download', 'fal_url': fal_url})
                    manifest_rows.append({
                        'Page': slug, 'Type': 'space', 'Local_Path': space_path,
                        'FAL_URL': fal_url, 'Source': 'GENERATED', 'Prompt': space_prompt,
                        'Status': 'ERROR',
                    })

    # Write manifest CSV
    manifest_path = os.path.join(RPT_DIR, 'generated-page-images-{}.csv'.format(TODAY))
    fieldnames = ['Page', 'Type', 'Source', 'Status', 'Local_Path', 'FAL_URL', 'Prompt']
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    # Write audit log
    log_path = os.path.join(LOG_DIR, 'page-image-generation-{}.json'.format(TS))
    with open(log_path, 'w') as f:
        json.dump({
            'mode':              mode,
            'total_pages':       total,
            'images_generated':  generated,
            'skipped':           skipped,
            'errors':            len(errors),
            'error_details':     errors,
            'cost_estimate_low':  round(generated * 0.045, 4),
            'cost_estimate_high': round(generated * 0.055, 4),
        }, f, indent=2)

    print()
    print('Summary: ' + mode)
    print('  Pages processed:     {}'.format(total))
    print('  Images generated:    {}'.format(generated))
    print('  Skipped:             {}'.format(skipped))
    print('  Errors:              {}'.format(len(errors)))
    if generated:
        print('  Actual cost (est):   ${:.2f}-${:.2f}'.format(
            generated * 0.045, generated * 0.055))
    print('  Manifest CSV:        ' + manifest_path)
    print('  Images folder:       ' + IMG_DIR)
    print('  Audit log:           ' + log_path)

    if not live:
        print('\n[DRY RUN] No API calls made. Re-run with --live to generate images.')


if __name__ == '__main__':
    main()
