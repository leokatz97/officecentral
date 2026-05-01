"""
One-off: regenerate a single (handle, position) under the current generate
script's prompts, replace the matching row in the batch manifest, and overwrite
the local file.

Usage:
  python3 scripts/regen-single-image.py --batch=batch-pilot \
          --handle=teknion-boardroom --position=2
"""
import csv
import importlib.util
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reuse the live generate script's helpers without re-implementing.
gen_path = os.path.join(ROOT, 'scripts', 'generate-img2img-product-images.py')
spec = importlib.util.spec_from_file_location('gen_img2img', gen_path)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


def parse_args():
    batch = handle = position = None
    phase = 'phase1'
    for a in sys.argv[1:]:
        if a.startswith('--batch='):    batch    = a.split('=', 1)[1]
        elif a.startswith('--handle='): handle   = a.split('=', 1)[1]
        elif a.startswith('--position='): position = int(a.split('=', 1)[1])
        elif a.startswith('--phase='):  phase    = a.split('=', 1)[1]
    if not (batch and handle and position):
        sys.exit('Required: --batch=<n> --handle=<h> --position=<2|3|4>')
    return batch, phase, handle, position


def main():
    batch, phase, handle, position = parse_args()
    manifest_path = os.path.join(ROOT, 'data', 'reports', 'generated-img2img-{}.csv'.format(batch))
    img_dir       = os.path.join(ROOT, 'data', 'img2img', phase, batch)

    if not os.path.exists(manifest_path):
        sys.exit('Manifest not found: ' + manifest_path)

    # Lookup live product info
    pid, title, pos1_src = gen.fetch_product(handle)
    if not pid:
        sys.exit('Handle not found in Shopify: ' + handle)
    if not pos1_src:
        sys.exit('Product has no pos-1 image: ' + handle)

    # Build the right prompt for this position using gen helpers
    category = gen.categorize(title)
    ctx_a, ctx_b = gen.CONTEXT_PAIRS.get(category, gen.CONTEXT_PAIRS['default'])
    spec_data = gen.load_spec(handle)
    if position == 2:
        prompt = gen.build_prompt_white_bg(title, spec_data)
    elif position == 3:
        prompt = gen.build_prompt(title, ctx_a, spec_data)
    elif position == 4:
        prompt = gen.build_prompt(title, ctx_b, spec_data)
    else:
        sys.exit('Invalid position: must be 2, 3, or 4')

    scene = gen.SCENES[position]
    filename = '{}__pos{}__{}.jpg'.format(handle, position, scene)
    local_path = os.path.join(img_dir, filename)

    print('Regenerating: {} pos {} ({})'.format(handle, position, scene))
    print('Prompt: {}'.format(prompt[:140]))

    fal_url, gen_id, err = gen.call_fal(prompt, pos1_src)
    if not fal_url:
        sys.exit('FAL call failed: ' + str(err))
    gen.download(fal_url, local_path)
    print('Wrote {}'.format(local_path))
    print('FAL URL: {}'.format(fal_url))

    # Rewrite the matching row in the manifest CSV.
    rows = []
    replaced = False
    with open(manifest_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            if r['handle'] == handle and str(r['position']) == str(position):
                r['scene']           = scene
                r['filename']        = filename
                r['source_hero_url'] = pos1_src
                r['fal_url']         = fal_url
                r['prompt']          = prompt
                r['generation_id']   = gen_id or ''
                r['status']          = 'OK'
                r['timestamp']       = datetime.now().strftime('%Y%m%d-%H%M%S')
                replaced = True
            rows.append(r)
    if not replaced:
        sys.exit('No matching row in manifest for {} pos {}'.format(handle, position))
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print('Manifest row replaced.')


if __name__ == '__main__':
    main()
