"""
Render the Tier 2 disposition CSV into a print-ready HTML doc for Steve.

Concise version — full detail for products that need active review
(Keep-Live, Keep-Live-Quote), compact listing for bulk-action groups
(Clearance, Archive) so Steve can spot-check without reading every row.

Input : data/tier-2-disposition-review.csv
Output: previews/tier-2-disposition-review.html
"""
import csv
import html
import os
from collections import defaultdict, Counter
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_IN = os.path.join(ROOT, 'data', 'tier-2-disposition-review.csv')
HTML_OUT = os.path.join(ROOT, 'previews', 'tier-2-disposition-review.html')

# Review order: the stuff Steve might want to flip comes first.
ACTION_ORDER = ['keep-live', 'keep-live-quote', 'clearance', 'archive']
DETAIL_ACTIONS = {'keep-live', 'keep-live-quote'}  # full decision table
COMPACT_ACTIONS = {'clearance', 'archive'}         # tight list

ACTION_LABEL = {
    'keep-live': 'Keep Live (Transactional)',
    'keep-live-quote': 'Keep Live (Quote-Only)',
    'clearance': 'Clearance — 10% off',
    'archive': 'Archive (ghost SKUs)',
}
ACTION_COLOUR = {
    'keep-live': '#166534',
    'keep-live-quote': '#7c3aed',
    'clearance': '#b45309',
    'archive': '#b91c1c',
}
ACTION_ONE_LINER = {
    'keep-live': 'No change — either sold in the last 18 months, or a protected brand line.',
    'keep-live-quote': 'Stays live, shows a Request-a-Quote button with the store phone and email instead of Add-to-Cart.',
    'clearance': 'Never sold. Moves to a dedicated Clearance / Last Chance collection at 10% off.',
    'archive': 'Genuine ghost / placeholder SKU — hidden from storefront, preserved in admin.',
}


def fmt_money(v):
    try:
        v = float(v)
    except (ValueError, TypeError):
        return ''
    if v <= 0:
        return ''
    return f'${v:,.0f}'


def main():
    rows = list(csv.DictReader(open(CSV_IN)))
    rows.sort(key=lambda r: (
        ACTION_ORDER.index(r['proposed_action']),
        r['type_bucket'],
        r['title'].lower(),
    ))

    by_action = Counter(r['proposed_action'] for r in rows)
    by_type = defaultdict(Counter)
    for r in rows:
        by_type[r['type_bucket']][r['proposed_action']] += 1
    types_sorted = sorted(by_type.keys())

    groups = defaultdict(lambda: defaultdict(list))  # {action: {type: [rows]}}
    for r in rows:
        groups[r['proposed_action']][r['type_bucket']].append(r)

    out = []
    out.append('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">')
    out.append('<title>Tier 2 Disposition Review — Brant Business Interiors</title>')
    out.append('''<style>
@page { size: Letter; margin: 0.55in 0.6in; }
* { box-sizing: border-box; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1a1a1a; font-size: 10pt; line-height: 1.45; margin: 0; padding: 0; }

.cover { text-align: center; padding: 1.4in 0 0.8in; border-bottom: 3px solid #1a4d80; margin-bottom: 0.4in; page-break-after: always; }
.cover .eyebrow { font-size: 9.5pt; letter-spacing: 3px; text-transform: uppercase; color: #6b7280; margin-bottom: 16px; }
.cover h1 { font-size: 30pt; color: #1a4d80; margin: 0 0 10px; font-weight: 700; line-height: 1.15; }
.cover .subtitle { font-size: 12pt; color: #374151; margin: 0 0 32px; }
.cover .meta { display: inline-block; text-align: left; font-size: 10pt; color: #4b5563; border-top: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb; padding: 12px 28px; margin-top: 24px; }
.cover .meta div { margin: 3px 0; }
.cover .meta strong { color: #1a1a1a; display: inline-block; width: 90px; }

h2 { font-size: 16pt; color: #1a4d80; border-bottom: 2px solid #1a4d80; padding-bottom: 5px; margin-top: 0; }
h3 { font-size: 12pt; color: #1a4d80; margin: 16px 0 6px; }

.summary { padding: 0 0 0.3in; page-break-after: always; }
.summary p { margin: 8px 0; }
.summary ul { margin: 6px 0 12px; padding-left: 18px; }
.summary li { margin: 3px 0; }

table.tbl { width: 100%; border-collapse: collapse; margin: 8px 0 14px; font-size: 9.5pt; }
table.tbl th, table.tbl td { border: 1px solid #d6dfe8; padding: 6px 9px; text-align: left; vertical-align: top; }
table.tbl th { background: #f3f6fa; color: #1a4d80; font-weight: 700; text-transform: uppercase; font-size: 8pt; letter-spacing: 0.5px; }
table.tbl td.num, table.tbl th.num { text-align: right; white-space: nowrap; }
table.tbl tr.total td { background: #eef4fb; font-weight: 700; }

.action-section { page-break-before: always; }
.action-header { padding: 12px 16px; color: white; border-radius: 3px 3px 0 0; margin-bottom: 10px; }
.action-header .label { font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; }
.action-header h2 { color: white; border: none; margin: 2px 0 4px; padding: 0; font-size: 15pt; }
.action-header .oneliner { font-size: 9.5pt; opacity: 0.95; }

.type-block { margin: 12px 0; page-break-inside: auto; }
.type-block h3 { background: #f3f6fa; border: 1px solid #d6dfe8; border-bottom: none; padding: 6px 10px; margin: 0; font-size: 10.5pt; }
.type-block h3 .count { font-weight: 400; color: #6b7280; font-size: 9.5pt; margin-left: 6px; }

table.skus { width: 100%; border-collapse: collapse; font-size: 9pt; }
table.skus th, table.skus td { border: 1px solid #d6dfe8; padding: 4px 7px; vertical-align: top; }
table.skus th { background: #fafbfc; font-weight: 700; text-transform: uppercase; font-size: 7.5pt; color: #4b5563; }
table.skus td.num { text-align: right; white-space: nowrap; }
table.skus td.rule { color: #6b7280; font-size: 8.5pt; white-space: nowrap; }
table.skus tr { page-break-inside: avoid; }
table.skus tr:nth-child(even) td { background: #fbfcfd; }

.decision { white-space: nowrap; font-family: "SF Mono", Menlo, monospace; font-size: 8.5pt; color: #4b5563; }
.decision span { display: inline-block; margin-right: 6px; }
.check { color: #1a4d80; font-weight: 700; }

.compact-list { column-count: 2; column-gap: 20px; font-size: 8.5pt; line-height: 1.4; }
.compact-list div { break-inside: avoid; padding: 2px 0; border-bottom: 1px dotted #e5e7eb; }

.note { background: #fff8e6; border-left: 3px solid #d97706; padding: 10px 14px; margin: 10px 0; font-size: 10pt; }

.signoff { background: #eef4fb; border-left: 4px solid #1a4d80; padding: 14px 18px; margin: 0.3in 0; page-break-inside: avoid; }
.signoff h2 { border: none; margin-top: 0; padding: 0; }
.signoff ul { list-style: none; padding: 0; margin: 8px 0; }
.signoff li { padding: 5px 0 5px 22px; position: relative; font-size: 10.5pt; }
.signoff li::before { content: "☐"; position: absolute; left: 0; top: 3px; font-size: 12pt; color: #1a4d80; }

.footer { margin-top: 0.3in; padding-top: 12px; border-top: 1px solid #d6dfe8; font-size: 9pt; color: #6b7280; text-align: center; }

@media print {
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  a { color: inherit; text-decoration: none; }
}
</style></head><body>''')

    # ---- Cover ----
    out.append('<section class="cover">')
    out.append('  <div class="eyebrow">Tier 2 — Catalog Review</div>')
    out.append('  <h1>Disposition Review</h1>')
    out.append('  <div class="subtitle">One-page summary. Detail for what needs review. Full list on request.</div>')
    out.append('  <div class="meta">')
    out.append('    <div><strong>For:</strong> Steve Katz</div>')
    out.append('    <div><strong>From:</strong> Leo Katz</div>')
    out.append(f'    <div><strong>Date:</strong> {datetime.now().strftime("%B %-d, %Y")}</div>')
    out.append(f'    <div><strong>Products:</strong> {len(rows)} active</div>')
    out.append('  </div>')
    out.append('</section>')

    # ---- Summary page ----
    out.append('<section class="summary">')
    out.append('<h2>The Plan — At a Glance</h2>')
    out.append('<p>Every active product is placed into one of four buckets. <strong>Nothing is touched until you sign off.</strong></p>')
    out.append('<table class="tbl">')
    out.append('<thead><tr><th>Bucket</th><th class="num">Count</th><th>What happens</th></tr></thead><tbody>')
    for a in ACTION_ORDER:
        out.append(f'<tr><td><strong style="color:{ACTION_COLOUR[a]};">{html.escape(ACTION_LABEL[a])}</strong></td>'
                   f'<td class="num">{by_action.get(a, 0)}</td>'
                   f'<td>{html.escape(ACTION_ONE_LINER[a])}</td></tr>')
    out.append(f'<tr class="total"><td>Total</td><td class="num">{len(rows)}</td><td></td></tr>')
    out.append('</tbody></table>')

    out.append('<h3>By product type</h3>')
    out.append('<table class="tbl">')
    out.append('<thead><tr><th>Type</th><th class="num">Keep-Live</th><th class="num">Quote-Only</th><th class="num">Clearance</th><th class="num">Archive</th><th class="num">Total</th></tr></thead><tbody>')
    for t in types_sorted:
        c = by_type[t]
        total = sum(c.values())
        out.append(f'<tr><td>{html.escape(t)}</td>'
                   f'<td class="num">{c.get("keep-live", 0)}</td>'
                   f'<td class="num">{c.get("keep-live-quote", 0)}</td>'
                   f'<td class="num">{c.get("clearance", 0)}</td>'
                   f'<td class="num">{c.get("archive", 0)}</td>'
                   f'<td class="num">{total}</td></tr>')
    out.append('</tbody></table>')

    out.append('<h3>New collection structure</h3>')
    out.append('<p>Every kept product is tagged on four facets. Clearance gets its own top-level nav; Quote-Only sits inside the normal Type collections.</p>')
    out.append('<ul>')
    out.append('  <li><strong>Type</strong> — Chairs · Desks · Tables · Storage · Accessories · Lounge · Outdoor</li>')
    out.append('  <li><strong>Room</strong> — Private Office · Boardroom · Reception · Open Plan · Training Room · Break Room · Lounge</li>')
    out.append('  <li><strong>Industry</strong> — Health Centres · Schools · Government · First Nations Organizations · Engineering Firms · Small Businesses · Non-Profits</li>')
    out.append('  <li><strong>Brand</strong> — OTG · Basics · Concorde · Global · ObusForme · Teknion · Ryno · Auditorium Seating · Zira · Foundations · Fellowes · In-House. Each brand gets its own landing page.</li>')
    out.append('</ul>')

    out.append('<div class="note">')
    out.append('<strong>How to review:</strong> The next two sections (Keep-Live, Quote-Only) have full detail and a tick-box column so you can flip any row. ')
    out.append('The Clearance + Archive sections are a condensed list so you can spot-check — no need to review every row.')
    out.append('</div>')
    out.append('</section>')

    # ---- Per-action sections ----
    for action in ACTION_ORDER:
        type_groups = groups.get(action, {})
        if not type_groups:
            continue
        action_total = sum(len(v) for v in type_groups.values())
        out.append('<section class="action-section">')
        out.append(f'<div class="action-header" style="background:{ACTION_COLOUR[action]};">')
        out.append(f'  <div class="label">{action_total} products · Section</div>')
        out.append(f'  <h2>{html.escape(ACTION_LABEL[action])}</h2>')
        out.append(f'  <div class="oneliner">{html.escape(ACTION_ONE_LINER[action])}</div>')
        out.append('</div>')

        if action in DETAIL_ACTIONS:
            # Full table with decision column
            for t in sorted(type_groups.keys()):
                items = sorted(type_groups[t], key=lambda r: r['title'].lower())
                out.append('<div class="type-block">')
                out.append(f'<h3>{html.escape(t)}<span class="count">— {len(items)}</span></h3>')
                out.append('<table class="skus">')
                out.append('<thead><tr>')
                out.append('<th style="width:44%;">Product</th>')
                out.append('<th class="num">Sold</th>')
                out.append('<th class="num">Revenue</th>')
                out.append('<th>Why</th>')
                out.append('<th style="width:125px;">Flip?</th>')
                out.append('</tr></thead><tbody>')
                for r in items:
                    def mark(opt):
                        return '<span class="check">☑</span>' if opt == action else '☐'
                    rule = r['rule_applied'].replace('-', ' ')
                    sold_qty = r.get('sold_orders', '0')
                    rev = fmt_money(r.get('sold_revenue', ''))
                    out.append('<tr>')
                    out.append(f'<td><strong>{html.escape(r["title"])}</strong></td>')
                    out.append(f'<td class="num">{sold_qty}</td>')
                    out.append(f'<td class="num">{rev}</td>')
                    out.append(f'<td class="rule">{html.escape(rule)}</td>')
                    out.append(f'<td class="decision">'
                               f'<span>{mark("keep-live")} KEEP</span>'
                               f'<span>{mark("keep-live-quote")} QUOTE</span><br>'
                               f'<span>{mark("clearance")} CLR</span>'
                               f'<span>{mark("archive")} ARCH</span>'
                               f'</td>')
                    out.append('</tr>')
                out.append('</tbody></table>')
                out.append('</div>')
        else:
            # Compact two-column list — no decision column, no revenue
            out.append('<div class="note" style="background:#f8fafc; border-left-color:#6b7280;">')
            if action == 'clearance':
                out.append('These all move to Clearance at 10% off. Scan for anything that looks like it should stay at full price — mark it, and we\'ll flip those.')
            else:
                out.append('Genuine ghost SKU — not a real product. Safe to archive.')
            out.append('</div>')
            for t in sorted(type_groups.keys()):
                items = sorted(type_groups[t], key=lambda r: r['title'].lower())
                out.append('<div class="type-block">')
                out.append(f'<h3>{html.escape(t)}<span class="count">— {len(items)}</span></h3>')
                out.append('<div class="compact-list">')
                for r in items:
                    out.append(f'<div>{html.escape(r["title"])}</div>')
                out.append('</div>')
                out.append('</div>')

        out.append('</section>')

    # ---- Signoff ----
    out.append('<section class="signoff">')
    out.append('<h2>Sign-Off</h2>')
    out.append('<ul>')
    out.append('  <li>Reviewed the Keep-Live and Quote-Only sections and ticked any rows to flip.</li>')
    out.append('  <li>Spot-checked the Clearance list for anything that should stay at full price.</li>')
    out.append('  <li>Approved the Type / Room / Industry / Brand taxonomy and the Clearance-at-10% plan.</li>')
    out.append('</ul>')
    out.append('<p style="margin-top:12px;"><strong>Signature:</strong> ______________________________ &nbsp;&nbsp; <strong>Date:</strong> ______________</p>')
    out.append('</section>')

    out.append(f'<div class="footer">Brant Business Interiors · Tier 2 Disposition Review · {datetime.now().strftime("%B %-d, %Y")}</div>')

    out.append('</body></html>')

    os.makedirs(os.path.dirname(HTML_OUT), exist_ok=True)
    with open(HTML_OUT, 'w') as f:
        f.write('\n'.join(out))

    print(f'Wrote: {HTML_OUT}')
    print(f'       {len(rows)} products across {len(ACTION_ORDER)} actions')


if __name__ == '__main__':
    main()
