#!/usr/bin/env python3
"""B4S4 Phase 2.6/4 — assemble push-b4s1-enrichment payloads from the workflow drafts.
Reads /tmp/b4s4-drafts.json (array of structured drafts from the draft workflow),
writes data/reports/b4s4-payloads/p{n}.json in the exact push-b4s1-enrichment shape.
Body + metafields built via the canonical Session-2 builders. MISSING fields (null/[]) are skipped."""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data/reports/b4s4-payloads'
OUT.mkdir(parents=True, exist_ok=True)
PHONE = "1-800-835-9565"
CTA = (f'<p>Office Central and Brant Business Interiors are verified OECM partners, so '
       f'Ontario&rsquo;s public sector can buy without an open tender. Call '
       f'<strong>{PHONE}</strong> for a quote.</p>')

def esc(s):
    return html.escape(str(s), quote=False).replace('"', '&Prime;') if s else s

def body(hook, lede, features, who):
    feats = ''.join(f'<li>{html.escape(f, quote=False)}</li>' for f in features)
    parts = [f'<p><strong>{html.escape(hook, quote=False)}</strong></p>',
             f'<p>{html.escape(lede, quote=False)}</p>']
    if feats:
        parts.append(f'<h3>Key features</h3>\n<ul>{feats}</ul>')
    if who:
        parts.append(f'<h3>Who it&rsquo;s for</h3>\n<p>{html.escape(who, quote=False)}</p>')
    parts.append(CTA)
    return '\n'.join(parts)

def mf_list(d):
    out = []
    def add(key, typ, val):
        if val is None: return
        if isinstance(val, list):
            if not val: return
            out.append({'key': key, 'type': typ, 'value': json.dumps(val, ensure_ascii=False)})
        else:
            if str(val).strip() == '': return
            v = str(val)
            if typ == 'single_line_text_field' and '\n' in v:
                v = ' / '.join(s.strip() for s in v.split('\n') if s.strip())
            out.append({'key': key, 'type': typ, 'value': v})
    add('manufacturer', 'single_line_text_field', 'Global Furniture Group')
    add('product_line', 'single_line_text_field', d.get('product_line'))
    add('model_codes', 'list.single_line_text_field', d.get('model_codes'))
    add('dimensions', 'single_line_text_field', d.get('dimensions'))
    add('weight', 'single_line_text_field', d.get('weight'))
    add('weight_capacity', 'single_line_text_field', d.get('weight_capacity'))
    add('materials', 'multi_line_text_field', d.get('materials'))
    add('finishes_available', 'list.single_line_text_field', d.get('finishes_available'))
    add('key_features', 'list.single_line_text_field', d.get('key_features'))
    add('certifications', 'list.single_line_text_field', d.get('certifications'))
    add('warranty', 'single_line_text_field', d.get('warranty'))
    add('country_of_manufacture', 'single_line_text_field', d.get('country_of_manufacture'))
    add('who_its_for', 'single_line_text_field', d.get('who_its_for'))
    return out

def norm_tags(tags):
    seen, out = set(), []
    for t in (tags or []):
        t = t.strip().lower()
        if t and t not in seen:
            seen.add(t); out.append(t)
    for must in ('brand:global-furniture-group', 'oecm-eligible'):
        if must not in seen:
            out.append(must); seen.add(must)
    return out

# manifest gives product_id per handle
manifest = {m['handle']: m for m in json.loads(Path('/tmp/b4s4-batch.json').read_text())}
drafts = json.loads(Path('/tmp/b4s4-drafts.json').read_text())
drafts.sort(key=lambda d: d.get('_n', 999))

skipped = []
for d in drafts:
    h = d['handle']
    if d.get('source_quality') in ('REQUIRES_LEO_SOURCE',) or d.get('boilerplate_corrupted'):
        skipped.append((d.get('_n'), h, d.get('source_quality'), d.get('boilerplate_corrupted')))
    n = d.get('_n')
    pid = str(manifest[h]['product_id'])
    payload = {
        'product_id': pid, 'handle': h,
        'title': d['title'], 'body_html': body(d['hook'], d['lede'], d.get('key_features', []), d.get('who_its_for')),
        'vendor': 'Global Furniture Group', 'product_type': d['product_type'],
        'tags': norm_tags(d.get('tags')),
        'seo_title': d['seo_title'], 'seo_description': d['seo_description'],
        'image_alt': d['image_alt'], 'metafields': mf_list(d), 'collects': d.get('collects', []),
        '_meta': {'source': d.get('source_quality'), 'source_url': d.get('source_url'),
                  'missing': d.get('missing', []), 'boilerplate_corrupted': d.get('boilerplate_corrupted', False),
                  'notes': d.get('notes')},
    }
    (OUT / f'p{n}.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    flag = ''
    if len(payload['seo_title']) > 60: flag += ' !SEOTITLE>60'
    if len(payload['seo_description']) > 160: flag += ' !SEODESC>160'
    print(f"p{n:<2} {h[:40]:42} src={d.get('source_quality'):>10} mf={len(payload['metafields'])} "
          f"seoT={len(payload['seo_title'])} seoD={len(payload['seo_description'])} miss={len(d.get('missing',[]))}{flag}")

print(f"\nwritten -> {OUT}  ({len(drafts)} payloads)")
if skipped:
    print("\n!! FLAGGED (review before write):")
    for n, h, sq, bp in skipped:
        print(f"   p{n} {h}  source={sq} boilerplate={bp}")
