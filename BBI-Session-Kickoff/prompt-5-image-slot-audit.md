# Prompt 5 — Hero + Sub-Hero Image Slot Audit

**Run AFTER** PROMPT-4 Pass 3 + COLLECTION-CLEANUP-1 complete. Auditing before cleanup means re-auditing slots whose collection templates may be pruned. Run when the collection set is stable.

**Paste the safety preflight first** (from `BBI-Session-Kickoff/01-safety-preflight.md`), then paste this prompt.

---

## The prompt

```
You are working on the BBI Shopify theme (dev only — 186373570873).
Store: office-central-online.myshopify.com.

PROMPT-5: hero + sub-hero image slot audit. READ-ONLY. No theme
writes, no Shopify mutations, no template JSON edits. Output is a
single CSV that Steve uses with the upcoming PAGE-IMG-1 fill prompt
to populate any empty image slots across the BBI design system.

PREREQUISITE: COLLECTION-CLEANUP-1 must have completed before this
runs. Cleanup archives sub-collections whose template JSONs may
contain image slots — auditing before cleanup means re-auditing
those slots after. If you're reading this before COLLECTION-CLEANUP-1
has shipped, confirm with Steve before proceeding.

— READ FIRST —

  1. CLAUDE.md (auto-loaded — project rules)
  2. BBI-Session-Kickoff/01-safety-preflight.md (preflight check)
  3. BBI-Session-Kickoff/bbi-build-state.md (current state)
  4. ls -la data/page-images/  (AI-generated photo library)
  5. ls -la data/oci-photos/   (48 real project photos)

Confirm reads before running code.

— STEP 1: Find every image slot in sections + snippets —

python3 - <<'EOF'
import os, re, json, glob

slots = []

# Scan sections and snippets for image_picker schemas
for path in glob.glob('theme/sections/*.liquid') + \
            glob.glob('theme/snippets/*.liquid'):
    try:
        content = open(path).read()
    except Exception:
        continue

    if '"image_picker"' not in content:
        continue

    # Pull out the schema block(s)
    schema_blocks = re.findall(
        r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',
        content, re.DOTALL
    )

    for schema_raw in schema_blocks:
        try:
            schema = json.loads(schema_raw)
        except json.JSONDecodeError:
            continue

        def extract_pickers(obj, parent_label='root'):
            found = []
            if isinstance(obj, dict):
                if obj.get('type') == 'image_picker':
                    found.append({
                        'id': obj.get('id', ''),
                        'label': obj.get('label', ''),
                        'parent_label': parent_label,
                    })
                for k, v in obj.items():
                    found += extract_pickers(v, parent_label=obj.get('name', parent_label))
            elif isinstance(obj, list):
                for item in obj:
                    found += extract_pickers(item, parent_label=parent_label)
            return found

        for picker in extract_pickers(schema):
            slots.append({
                'section_file': os.path.basename(path),
                'section_type': os.path.basename(path).replace('.liquid', ''),
                'setting_id': picker['id'],
                'setting_label': picker['label'],
                'parent_label': picker['parent_label'],
            })

# De-dupe (same section + setting id)
seen = set()
unique = []
for s in slots:
    key = (s['section_file'], s['setting_id'])
    if key in seen:
        continue
    seen.add(key)
    unique.append(s)

os.makedirs('data/reports', exist_ok=True)
with open('data/reports/_image-slot-schemas.json', 'w') as f:
    json.dump(unique, f, indent=2)

print(f'Found {len(unique)} image_picker slots across '
      f'{len(set(s["section_file"] for s in unique))} files.')
EOF

— STEP 2: Cross-reference with template JSONs —

python3 - <<'EOF'
import os, json, glob

with open('data/reports/_image-slot-schemas.json') as f:
    slots = json.load(f)

# Build lookup: section_type -> [slot dicts]
slot_by_type = {}
for s in slots:
    slot_by_type.setdefault(s['section_type'], []).append(s)

# Walk every template JSON
findings = []
for path in glob.glob('theme/templates/*.json'):
    try:
        with open(path) as f:
            tpl = json.load(f)
    except Exception:
        continue

    template_name = os.path.basename(path)
    sections = tpl.get('sections', {})

    for section_key, section_data in sections.items():
        section_type = section_data.get('type', '')
        if section_type not in slot_by_type:
            continue

        settings = section_data.get('settings', {})
        blocks = section_data.get('blocks', {})

        for slot in slot_by_type[section_type]:
            val = settings.get(slot['setting_id'])
            findings.append({
                'template_json': template_name,
                'section_key': section_key,
                'section_type': section_type,
                'section_file': slot['section_file'],
                'setting_id': slot['setting_id'],
                'setting_label': slot['setting_label'],
                'current_value': val if val else '',
                'is_populated': bool(val),
            })

# Also surface "orphan" slots — defined in section/snippet but
# never referenced in any template JSON
referenced = {(f['section_type'], f['setting_id']) for f in findings}
for s in slots:
    key = (s['section_type'], s['setting_id'])
    if key not in referenced:
        findings.append({
            'template_json': '(no template uses this section)',
            'section_key': '',
            'section_type': s['section_type'],
            'section_file': s['section_file'],
            'setting_id': s['setting_id'],
            'setting_label': s['setting_label'],
            'current_value': '',
            'is_populated': False,
        })

with open('data/reports/_image-slot-findings.json', 'w') as f:
    json.dump(findings, f, indent=2)

populated = sum(1 for f in findings if f['is_populated'])
empty = sum(1 for f in findings if not f['is_populated'])
print(f'Template cross-ref complete: {len(findings)} slots')
print(f'  Populated: {populated}')
print(f'  Empty:     {empty}')
EOF

— STEP 3: Suggest matches from photo libraries —

python3 - <<'EOF'
import os, json, glob, re
from difflib import SequenceMatcher

with open('data/reports/_image-slot-findings.json') as f:
    findings = json.load(f)

# Inventory both photo libraries
photo_paths = []
for root in ('data/page-images', 'data/oci-photos'):
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        photo_paths += glob.glob(f'{root}/**/*.{ext}', recursive=True)

photo_index = []
for p in photo_paths:
    name = os.path.basename(p).lower()
    # tokenize filename: split on -, _, spaces, drop extension
    base = os.path.splitext(name)[0]
    tokens = re.split(r'[-_\s]+', base)
    photo_index.append({
        'path': p,
        'filename': os.path.basename(p),
        'tokens': set(t for t in tokens if t and not t.isdigit()),
    })

def score_match(slot, photo):
    """Match score by token overlap between section/setting and filename."""
    slot_text = f"{slot['section_type']} {slot['setting_id']} {slot.get('setting_label', '')}"
    slot_tokens = set(re.split(r'[-_\s]+', slot_text.lower()))
    slot_tokens = {t for t in slot_tokens if t and len(t) > 2}
    if not slot_tokens or not photo['tokens']:
        return 0.0
    overlap = slot_tokens & photo['tokens']
    return len(overlap) / max(len(slot_tokens), 1)

# Annotate each finding with best suggested photo
for f in findings:
    if f['is_populated']:
        f['suggested_photo'] = ''
        f['suggestion_confidence'] = ''
        f['library_path'] = ''
        continue
    scored = sorted(
        ((score_match(f, p), p) for p in photo_index),
        key=lambda x: x[0], reverse=True
    )
    if not scored or scored[0][0] == 0:
        f['suggested_photo'] = 'NEEDS NEW PHOTO'
        f['suggestion_confidence'] = 'none'
        f['library_path'] = ''
    else:
        score, photo = scored[0]
        f['suggested_photo'] = photo['filename']
        f['library_path'] = photo['path']
        if score >= 0.5:
            f['suggestion_confidence'] = 'high'
        elif score >= 0.25:
            f['suggestion_confidence'] = 'medium'
        else:
            f['suggestion_confidence'] = 'low'

# Sort by status (empty first), then by template, then by section
findings.sort(key=lambda f: (
    f['is_populated'],
    f['template_json'],
    f['section_type'],
    f['setting_id'],
))

with open('data/reports/_image-slot-with-matches.json', 'w') as f:
    json.dump(findings, f, indent=2)
print(f'Match suggestions added for {sum(1 for f in findings if not f["is_populated"])} empty slots.')
EOF

— STEP 4: Write the audit CSV —

python3 - <<'EOF'
import csv, json, os
from datetime import datetime

with open('data/reports/_image-slot-with-matches.json') as f:
    findings = json.load(f)

cols = [
    'template_json', 'section_key', 'section_type', 'section_file',
    'setting_id', 'setting_label',
    'is_populated', 'current_value',
    'suggested_photo', 'library_path', 'suggestion_confidence',
    'steve_action', 'steve_notes',
]

for row in findings:
    row['steve_action'] = ''   # blank for Steve: use-suggested / pick-different / generate-new / needs-real-photo
    row['steve_notes'] = ''

ts = datetime.now().strftime('%Y-%m-%d')
out = f'data/reports/image-slot-audit-{ts}.csv'

with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(findings)

print(f'Output: {out}')
print(f'Rows: {len(findings)}')
EOF

— STEP 5: Summary report to chat —

Print to chat:
  1. CSV path
  2. Total slot count, populated count, empty count
  3. Top 10 empty slots with their suggested photo and confidence
  4. Count of "NEEDS NEW PHOTO" rows (no library match) — these will
     need AI generation or real photo sourcing in PAGE-IMG-1
  5. Count of "orphan" slots (defined in section but no template
     uses them) — flag for possible cleanup

— STEP 6: Sanity checks —

Verify before handoff:
  ✓ CSV exists at the path printed
  ✓ Header row matches the column list
  ✓ Every "populated = False" row has a non-empty
    suggested_photo OR "NEEDS NEW PHOTO"
  ✓ Every "populated = True" row has empty suggested_photo

— STEP 7: Commit —

Stage and commit only the new CSV. Skip the _*.json scratch files.

  git add data/reports/image-slot-audit-*.csv
  git commit -m "PROMPT-5: image slot audit — N empty, M need new photo"

— STEP 8: Handoff —

Steve will:
  1. Open the CSV in Google Sheets
  2. For each empty row, fill steve_action with one of:
       - use-suggested  (accept Claude's match)
       - pick-different (Steve specifies a different file)
       - generate-new   (route to fal.ai pipeline)
       - needs-real-photo (Steve/Leo sources manually)
       - skip          (leave empty intentionally)
  3. Save reviewed CSV back to data/reports/
  4. Trigger PAGE-IMG-1 with the reviewed file
```
