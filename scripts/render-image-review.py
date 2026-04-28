"""
Render an HTML approval gate for the img2img + QA pipeline.

Input:
  data/reports/qa-vision-{date}.csv  (one row per generated image, scored)

Output:
  previews/image-review-{date}-batch-{N}.html
  - Per product: source hero (real) | gen-2 (AI office A) | gen-3 (AI office B)
  - Vision score and one-sentence reason under each AI image
  - "approve gen-2" / "approve gen-3" checkboxes (checked by default when score >= 7)
  - Submit button POSTs JSON to http://localhost:{PORT}/submit
    Companion: scripts/serve-review.py captures the POST and writes
    data/reports/approval-{date}-batch-{N}.json.

Usage:
  python3 scripts/render-image-review.py --batch=pilot-5
  python3 scripts/render-image-review.py --batch=pilot-20 --qa=data/reports/qa-vision-2026-04-28.csv
  python3 scripts/render-image-review.py --batch=wave2-001 --port=8765
"""
import csv
import glob
import html
import os
import sys
from collections import OrderedDict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPT_DIR  = os.path.join(ROOT, 'data', 'reports')
PREV_DIR = os.path.join(ROOT, 'previews')
TODAY    = datetime.now().strftime('%Y-%m-%d')

DEFAULT_PORT = 8765


def parse_args():
    batch    = None
    qa_path  = None
    port     = DEFAULT_PORT
    for arg in sys.argv[1:]:
        if arg.startswith('--batch='):
            batch = arg.split('=', 1)[1]
        elif arg.startswith('--qa='):
            qa_path = arg.split('=', 1)[1]
        elif arg.startswith('--port='):
            port = int(arg.split('=', 1)[1])
    if not batch:
        sys.exit('Required: --batch=<name>  (e.g. --batch=pilot-5)')
    return batch, qa_path, port


def latest_qa():
    matches = sorted(glob.glob(os.path.join(RPT_DIR, 'qa-vision-*.csv')))
    if not matches:
        sys.exit('No qa-vision-*.csv found. Run qa-vision-check.py first.')
    return matches[-1]


def load_qa(path):
    """Group rows by handle: {handle: {'title': str, 'positions': {2: row, 3: row}}}"""
    products = OrderedDict()
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            handle = row['Handle']
            if handle not in products:
                products[handle] = {'title': row.get('Title', ''), 'positions': {}}
            try:
                pos = int(row['Image_Position'])
            except (ValueError, KeyError):
                continue
            products[handle]['positions'][pos] = row
    return products


def display_image_url(row):
    fal_url = row.get('FAL_URL') or ''
    local   = row.get('Local_Path') or ''
    if fal_url:
        return fal_url
    if local and os.path.exists(local):
        return 'file://' + local
    return ''


def cell_html(row, position):
    img_url = display_image_url(row)
    score   = row.get('Score', '')
    reason  = html.escape((row.get('Reason') or '')[:160])
    status  = row.get('Status', '')
    try:
        s = int(score)
    except (ValueError, TypeError):
        s = -1
    if s >= 8:
        score_cls = 'score-good'
    elif s >= 7:
        score_cls = 'score-ok'
    elif s >= 0:
        score_cls = 'score-bad'
    else:
        score_cls = 'score-na'

    checked = ' checked' if s >= 7 else ''
    img_tag = '<img src="{}" alt="gen-{}" loading="lazy">'.format(html.escape(img_url), position) if img_url else '<div class="missing">no image</div>'

    return (
        '<div class="cell ai">'
        '{img}'
        '<div class="score {sc}">score: {score} ({status})</div>'
        '<div class="reason">{reason}</div>'
        '<label class="approve"><input type="checkbox" name="approve-{pos}"{checked}>Approve gen-{pos}</label>'
        '<textarea name="comment-{pos}" placeholder="Leave a comment (optional)..." rows="3"></textarea>'
        '</div>'
    ).format(
        img=img_tag, score=score, sc=score_cls, status=html.escape(status),
        reason=reason, pos=position, checked=checked,
    )


def source_cell_html(row):
    src = html.escape(row.get('Source_Hero_URL') or '')
    if src:
        return '<div class="cell src"><img src="{}" alt="source" loading="lazy"><div class="label">source hero (live — not uploaded)</div></div>'.format(src)
    return '<div class="cell src"><div class="missing">no hero</div></div>'


def product_html(handle, info):
    title = html.escape(info['title'] or '(untitled)')
    pos2  = info['positions'].get(2)
    pos3  = info['positions'].get(3)
    pos4  = info['positions'].get(4)

    ref_row = pos2 or pos3 or pos4
    src_cell = source_cell_html(ref_row) if ref_row else '<div class="cell src"><div class="missing">no data</div></div>'

    pos2_cell = cell_html(pos2, 2) if pos2 else '<div class="cell ai"><div class="missing">no scene-A</div></div>'
    pos3_cell = cell_html(pos3, 3) if pos3 else '<div class="cell ai"><div class="missing">no scene-B</div></div>'
    pos4_cell = cell_html(pos4, 4) if pos4 else '<div class="cell ai"><div class="missing">no white-bg</div></div>'

    return (
        '<section class="product" data-handle="{handle}">'
        '<header>'
        '<h2>{title}</h2>'
        '<code>{handle}</code>'
        '</header>'
        '<div class="col-headers"><span>Source hero</span><span>Scene A — Institutional</span><span>Scene B — SMB Office</span><span>White Background</span></div>'
        '<div class="row">{src}{p2}{p3}{p4}</div>'
        '</section>'
    ).format(
        handle=html.escape(handle), title=title,
        src=src_cell, p2=pos2_cell, p3=pos3_cell, p4=pos4_cell,
    )


CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f6f6f6; margin: 0; padding: 24px; color: #1a1a1a; }
h1 { margin: 0; font-size: 22px; }
.summary { color: #555; font-size: 14px; margin: 8px 0 24px; }
.product { background: white; border: 1px solid #e0e0e0; border-radius: 8px;
           padding: 16px; margin-bottom: 24px; }
.product header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px; }
.product h2 { margin: 0; font-size: 16px; }
.product code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 12px; color: #555; }
.row { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; }
.cell { display: flex; flex-direction: column; gap: 6px; }
.cell img { width: 100%; aspect-ratio: 4/3; object-fit: contain;
            background: #fafafa; border: 1px solid #eee; border-radius: 4px; }
.cell .label { font-size: 12px; color: #666; text-align: center; }
.col-headers { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px;
               margin-bottom: 4px; }
.col-headers span { font-size: 11px; font-weight: 700; text-transform: uppercase;
                    letter-spacing: 0.05em; color: #888; text-align: center; }
.cell .missing { width: 100%; aspect-ratio: 4/3;
                 display: flex; align-items: center; justify-content: center;
                 background: #fff5f5; color: #c00; font-weight: 600;
                 border: 1px solid #fdd; border-radius: 4px; }
.score { font-size: 13px; font-weight: 600; padding: 4px 8px; border-radius: 4px;
         display: inline-block; align-self: flex-start; }
.score-good { background: #e6f5ea; color: #0a6b1f; }
.score-ok   { background: #fff7e6; color: #9a4a00; }
.score-bad  { background: #fbeaea; color: #b00020; }
.score-na   { background: #eee; color: #555; }
.reason { font-size: 12px; color: #555; line-height: 1.4; }
.approve { font-size: 13px; cursor: pointer; user-select: none; }
.approve input { margin-right: 6px; transform: translateY(1px); }
.cell textarea { width: 100%; font-size: 12px; font-family: inherit; border: 1px solid #ddd;
                 border-radius: 4px; padding: 6px 8px; resize: vertical; color: #333;
                 background: #fafafa; line-height: 1.4; }
.cell textarea:focus { outline: none; border-color: #0a64c4; background: #fff; }
#submit-bar { position: sticky; bottom: 0; background: white; padding: 12px 16px;
              border-top: 2px solid #0a64c4; display: flex; gap: 12px; align-items: center;
              margin: 24px -24px -24px; }
#submit-bar button { background: #0a64c4; color: white; border: 0; padding: 10px 20px;
                     border-radius: 6px; font-size: 14px; cursor: pointer; }
#submit-bar button:hover { background: #084e9b; }
#status { font-size: 13px; color: #555; }
"""


JS_TEMPLATE = """
const PORT  = __PORT__;
const BATCH = "__BATCH__";
const SUBMIT_URL = `http://localhost:${PORT}/submit`;

document.getElementById('submit-btn').addEventListener('click', async () => {
  const approvals = {};
  document.querySelectorAll('.product').forEach(p => {
    const handle = p.dataset.handle;
    const g2 = p.querySelector('input[name=approve-2]');
    const g3 = p.querySelector('input[name=approve-3]');
    const g4 = p.querySelector('input[name=approve-4]');
    const c2 = p.querySelector('textarea[name=comment-2]');
    const c3 = p.querySelector('textarea[name=comment-3]');
    const c4 = p.querySelector('textarea[name=comment-4]');
    approvals[handle] = {
      gen2:     g2 ? g2.checked : false,
      gen3:     g3 ? g3.checked : false,
      gen4:     g4 ? g4.checked : false,
      comment2: c2 ? c2.value.trim() : '',
      comment3: c3 ? c3.value.trim() : '',
      comment4: c4 ? c4.value.trim() : '',
    };
  });
  const status = document.getElementById('status');
  status.textContent = 'Submitting...';
  try {
    const resp = await fetch(SUBMIT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ batch: BATCH, approvals }),
    });
    if (resp.ok) {
      status.textContent = 'Submitted. You can close this tab.';
      status.style.color = '#0a6b1f';
    } else {
      status.textContent = 'Submit failed (HTTP ' + resp.status + ').';
      status.style.color = '#b00020';
    }
  } catch (e) {
    status.textContent = 'Submit failed: ' + e.message + ' — is serve-review.py running on port ' + PORT + '?';
    status.style.color = '#b00020';
  }
});
"""


def main():
    batch, qa_arg, port = parse_args()
    qa_path = qa_arg or latest_qa()
    products = load_qa(qa_path)

    if not products:
        sys.exit('No products in {}.'.format(qa_path))

    output_path = os.path.join(PREV_DIR, 'image-review-{}-batch-{}.html'.format(TODAY, batch))
    os.makedirs(PREV_DIR, exist_ok=True)

    pair_count = sum(len(v['positions']) for v in products.values())
    parts = ['<!doctype html><meta charset="utf-8">']
    parts.append('<title>Image review {} {}</title>'.format(TODAY, batch))
    parts.append('<style>{}</style>'.format(CSS))
    parts.append('<h1>Image review &mdash; {} batch {}</h1>'.format(TODAY, html.escape(batch)))
    parts.append(
        '<p class="summary">{} product{} &middot; {} image pair{}. '
        'Approve checkboxes default to ticked when vision score &ge; 7. '
        'Click Submit when done &mdash; make sure '
        '<code>scripts/serve-review.py --batch={} --port={}</code> is running.</p>'.format(
            len(products), '' if len(products) == 1 else 's',
            pair_count, '' if pair_count == 1 else 's',
            html.escape(batch), port,
        )
    )

    for handle, info in products.items():
        parts.append(product_html(handle, info))

    parts.append('<div id="submit-bar"><button id="submit-btn">Submit approvals</button>'
                 '<span id="status">Awaiting submit&hellip;</span></div>')
    js = JS_TEMPLATE.replace('__PORT__', str(port)).replace('__BATCH__', batch)
    parts.append('<script>{}</script>'.format(js))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))

    print('Wrote {} products to {}'.format(len(products), output_path))
    print('Open in browser: file://' + output_path)
    print()
    print('Then in another terminal:')
    print('  python3 scripts/serve-review.py --batch={} --port={}'.format(batch, port))


if __name__ == '__main__':
    main()
