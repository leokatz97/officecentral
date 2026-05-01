"""
Render an HTML approval gate for the img2img + QA pipeline.

Input:
  data/reports/qa-vision-<batch>.csv  (lowercase columns, per-batch)

Output:
  previews/image-review-<batch>.html
  - Per product: source hero | pos2 (Scene A) | pos3 (Scene B) | pos4 (white-bg)
  - Vision score and one-sentence reason under each AI image
  - "approve pos2/3/4" checkboxes (default-checked when score >= 7)
  - Submit POSTs JSON to http://localhost:<port>/submit
    Companion: scripts/serve-review.py writes data/reports/approval-<batch>.json

Usage:
  python3 scripts/render-image-review.py --batch=batch-pilot
  python3 scripts/render-image-review.py --batch=batch-pilot --port=8765
"""
import csv
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
        sys.exit('Required: --batch=<name>  (e.g. --batch=batch-pilot)')
    return batch, qa_path, port


def load_qa(path):
    products = OrderedDict()
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            handle = row['handle']
            if handle not in products:
                products[handle] = {'positions': {}}
            try:
                pos = int(row['position'])
            except (ValueError, KeyError):
                continue
            products[handle]['positions'][pos] = row
    return products


def display_image_url(row):
    fal_url = row.get('fal_url') or ''
    local   = row.get('local_path') or ''
    if fal_url:
        return fal_url
    if local and os.path.exists(local):
        return 'file://' + local
    return ''


def cell_html(row, position):
    img_url = display_image_url(row)
    score   = row.get('score', '')
    reason  = html.escape((row.get('reason') or '')[:160])
    status  = row.get('status', '')
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
    img_tag = '<img src="{}" alt="pos-{}" loading="lazy">'.format(html.escape(img_url), position) if img_url else '<div class="missing">no image</div>'
    return (
        '<div class="cell ai">'
        '{img}'
        '<div class="score {sc}">score: {score} ({status})</div>'
        '<div class="reason">{reason}</div>'
        '<label class="approve"><input type="checkbox" name="approve-{pos}"{checked}>Approve pos-{pos}</label>'
        '<textarea name="comment-{pos}" placeholder="Leave a comment (optional)..." rows="3"></textarea>'
        '</div>'
    ).format(
        img=img_tag, score=score, sc=score_cls, status=html.escape(status),
        reason=reason, pos=position, checked=checked,
    )


def source_cell_html(row):
    src = html.escape(row.get('source_hero_url') or '')
    if src:
        return '<div class="cell src"><img src="{}" alt="source" loading="lazy"><div class="label">source hero (live — not uploaded)</div></div>'.format(src)
    return '<div class="cell src"><div class="missing">no hero</div></div>'


def product_html(handle, info):
    pos2  = info['positions'].get(2)
    pos3  = info['positions'].get(3)
    pos4  = info['positions'].get(4)
    ref_row = pos2 or pos3 or pos4
    src_cell = source_cell_html(ref_row) if ref_row else '<div class="cell src"><div class="missing">no data</div></div>'
    pos2_cell = cell_html(pos2, 2) if pos2 else '<div class="cell ai"><div class="missing">no pos-2</div></div>'
    pos3_cell = cell_html(pos3, 3) if pos3 else '<div class="cell ai"><div class="missing">no pos-3</div></div>'
    pos4_cell = cell_html(pos4, 4) if pos4 else '<div class="cell ai"><div class="missing">no pos-4</div></div>'
    return (
        '<section class="product" data-handle="{handle}">'
        '<header><h2><code>{handle}</code></h2></header>'
        '<div class="col-headers"><span>Source hero</span><span>Pos 2 — White Background</span><span>Pos 3 — Scene A (Institutional)</span><span>Pos 4 — Scene B (SMB Office)</span></div>'
        '<div class="row">{src}{p2}{p3}{p4}</div>'
        '</section>'
    ).format(
        handle=html.escape(handle),
        src=src_cell, p2=pos2_cell, p3=pos3_cell, p4=pos4_cell,
    )


CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f6f6f6; margin: 0; padding: 24px; color: #1a1a1a; }
h1 { margin: 0; font-size: 22px; }
.summary { color: #555; font-size: 14px; margin: 8px 0 24px; }
.toolbar { display: flex; gap: 8px; margin: 0 0 16px; }
.toolbar button { font-size: 12px; padding: 6px 12px; border: 1px solid #bbb;
                  background: white; border-radius: 4px; cursor: pointer; }
.toolbar button:hover { background: #f0f0f0; }
.product { background: white; border: 1px solid #e0e0e0; border-radius: 8px;
           padding: 16px; margin-bottom: 24px; }
.product header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px; }
.product h2 { margin: 0; font-size: 14px; font-weight: 500; }
.product code { background: #f0f0f0; padding: 4px 8px; border-radius: 3px; font-size: 13px; color: #333; }
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

document.getElementById('approve-all').addEventListener('click', () => {
  document.querySelectorAll('input[type=checkbox]').forEach(c => c.checked = true);
});
document.getElementById('reject-all').addEventListener('click', () => {
  document.querySelectorAll('input[type=checkbox]').forEach(c => c.checked = false);
});

document.getElementById('submit-btn').addEventListener('click', async () => {
  const approvals = {};
  document.querySelectorAll('.product').forEach(p => {
    const handle = p.dataset.handle;
    const p2 = p.querySelector('input[name=approve-2]');
    const p3 = p.querySelector('input[name=approve-3]');
    const p4 = p.querySelector('input[name=approve-4]');
    const c2 = p.querySelector('textarea[name=comment-2]');
    const c3 = p.querySelector('textarea[name=comment-3]');
    const c4 = p.querySelector('textarea[name=comment-4]');
    approvals[handle] = {
      pos2:     p2 ? p2.checked : false,
      pos3:     p3 ? p3.checked : false,
      pos4:     p4 ? p4.checked : false,
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
    qa_path = qa_arg or os.path.join(RPT_DIR, 'qa-vision-{}.csv'.format(batch))
    if not os.path.exists(qa_path):
        sys.exit('QA CSV not found: {}\nRun qa-vision-check.py --batch={} first.'.format(qa_path, batch))
    products = load_qa(qa_path)
    if not products:
        sys.exit('No products in {}.'.format(qa_path))

    output_path = os.path.join(PREV_DIR, 'image-review-{}.html'.format(batch))
    os.makedirs(PREV_DIR, exist_ok=True)

    img_count = sum(len(v['positions']) for v in products.values())
    parts = ['<!doctype html><meta charset="utf-8">']
    parts.append('<title>Image review {}</title>'.format(batch))
    parts.append('<style>{}</style>'.format(CSS))
    parts.append('<h1>Image review &mdash; batch {}</h1>'.format(html.escape(batch)))
    parts.append(
        '<p class="summary">{} product{} &middot; {} image{}. '
        'Approve checkboxes default to ticked when vision score &ge; 7. '
        'Click Submit when done &mdash; make sure '
        '<code>scripts/serve-review.py --batch={} --port={}</code> is running.</p>'.format(
            len(products), '' if len(products) == 1 else 's',
            img_count, '' if img_count == 1 else 's',
            html.escape(batch), port,
        )
    )
    parts.append('<div class="toolbar">'
                 '<button id="approve-all">Approve all</button>'
                 '<button id="reject-all">Reject all</button>'
                 '</div>')
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
