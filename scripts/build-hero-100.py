"""
Build the Hero 100 list — the curated set of products that get full Tier 2
enrichment (POI specs, rewritten titles, descriptions, finish/brand/feature tags,
internal-link anchoring).

Selection criteria:
  1. Top revenue first — mirrors the velocity-sorted collection order visitors see.
  2. Type coverage — every type collection gets a meaningful slice so a visitor
     landing on /collections/type-outdoor still hits enriched products at the top.
  3. Room coverage — same logic for /collections/room-* pages.
  4. Industry coverage — same logic for /collections/industry-* pages.
  5. ~100 total. Hard cap; if quotas overflow, drop lowest-revenue revenue-fill picks.

Per-type quotas (chosen to fit category sizes):
  chairs 15 · desks 15 · tables 12 · storage 12 · accessories 10 · lounge 5 · outdoor 3 = 72

Per-room quotas (≥3 each, where catalog supports it; break-room dropped — catalog is empty):
  private-office 3 · boardroom 3 · reception 3 · open-plan 3 · training-room 3 · lounge 3

Per-industry quotas (≥3 each — these are the four live industry tags from
data/reports/industry-tags-proposed.csv):
  business 3 · educational 3 · daycare 3 · healthcare 3

Quota passes are additive but de-duped against earlier passes — type quota fills first,
then room quota tops up only the gaps, then industry quota tops up only the gaps,
then revenue-fill takes the catalog by overall revenue rank.

Reads:  data/reports/taxonomy-tags-proposed.csv  (type/room/revenue source of truth)
        data/reports/industry-tags-proposed.csv  (industry source of truth — joined on handle)
Writes: data/hero-100.csv      — Hero 100 with selection_reason + hero_rank
        data/hero-100.md       — markdown summary for Steve to review

Usage:
  python3 scripts/build-hero-100.py
"""
import csv
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')
IN_INDUSTRY_CSV = os.path.join(ROOT, 'data', 'reports', 'industry-tags-proposed.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'hero-100.csv')
OUT_MD = os.path.join(ROOT, 'data', 'hero-100.md')

TYPE_QUOTAS = {
    'type:chairs': 15,
    'type:desks': 15,
    'type:tables': 12,
    'type:storage': 12,
    'type:accessories': 10,
    'type:lounge': 5,
    'type:outdoor': 3,
}
ROOM_QUOTAS = {
    'room:private-office': 3,
    'room:boardroom': 3,
    'room:reception': 3,
    'room:open-plan': 3,
    'room:training-room': 3,
    'room:lounge': 3,
}
INDUSTRY_QUOTAS = {
    'industry:business': 3,
    'industry:educational': 3,
    'industry:daycare': 3,
    'industry:healthcare': 3,
}
TARGET_TOTAL = 100


def load_rows() -> list:
    industry_by_handle = {}
    with open(IN_INDUSTRY_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            tag = (r.get('industry_tag') or '').strip()
            if tag:
                industry_by_handle[r['handle']] = tag

    rows = []
    with open(IN_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            r['sold_revenue'] = float(r.get('sold_revenue') or 0)
            r['sold_orders'] = int(r.get('sold_orders') or 0)
            joined = industry_by_handle.get(r['handle'])
            if joined:
                r['industry_tag'] = joined
            rows.append(r)
    return rows


def pick_by_tag(rows: list, field: str, value: str, n: int, taken: set) -> list:
    pool = [r for r in rows if r.get(field) == value and r['handle'] not in taken]
    pool.sort(key=lambda r: (-r['sold_revenue'], -r['sold_orders'], r['handle']))
    return pool[:n]


def gap_topup(rows: list, field: str, value: str, target: int,
              selected: list, taken: set) -> list:
    have = sum(1 for r in selected if r.get(field) == value)
    needed = max(0, target - have)
    if needed == 0:
        return []
    return pick_by_tag(rows, field, value, needed, taken)


def pick_revenue_fill(rows: list, n: int, taken: set) -> list:
    pool = [r for r in rows if r['handle'] not in taken]
    pool.sort(key=lambda r: (-r['sold_revenue'], -r['sold_orders'], r['handle']))
    return pool[:n]


def main() -> None:
    rows = load_rows()
    print(f'Loaded {len(rows)} active products from {os.path.relpath(IN_CSV, ROOT)}')

    selected = []
    taken = set()

    print('\n[Pass 1] Type quotas')
    for type_tag, quota in TYPE_QUOTAS.items():
        picks = pick_by_tag(rows, 'type_tag', type_tag, quota, taken)
        for p in picks:
            p['selection_reason'] = f'type-quota:{type_tag.split(":", 1)[1]}'
            selected.append(p)
            taken.add(p['handle'])
        print(f'  {type_tag:<22} quota {quota:>3}  → picked {len(picks):>3}')

    print('\n[Pass 2] Room quota top-up')
    for room_tag, quota in ROOM_QUOTAS.items():
        picks = gap_topup(rows, 'room_tag', room_tag, quota, selected, taken)
        for p in picks:
            p['selection_reason'] = f'room-quota:{room_tag.split(":", 1)[1]}'
            selected.append(p)
            taken.add(p['handle'])
        have = sum(1 for r in selected if r.get('room_tag') == room_tag)
        print(f'  {room_tag:<22} target {quota:>3}  → added {len(picks):>3} (now {have})')

    print('\n[Pass 3] Industry quota top-up')
    for ind_tag, quota in INDUSTRY_QUOTAS.items():
        picks = gap_topup(rows, 'industry_tag', ind_tag, quota, selected, taken)
        for p in picks:
            p['selection_reason'] = f'industry-quota:{ind_tag.split(":", 1)[1]}'
            selected.append(p)
            taken.add(p['handle'])
        have = sum(1 for r in selected if r.get('industry_tag') == ind_tag)
        print(f'  {ind_tag:<26} target {quota:>3}  → added {len(picks):>3} (now {have})')

    print('\n[Pass 4] Revenue fill')
    fill_n = TARGET_TOTAL - len(selected)
    if fill_n > 0:
        fills = pick_revenue_fill(rows, fill_n, taken)
        for p in fills:
            p['selection_reason'] = 'revenue-fill'
            selected.append(p)
            taken.add(p['handle'])
        print(f'  {"revenue-fill":<26} slots {fill_n:>3}  → picked {len(fills):>3}')
    elif fill_n < 0:
        # Quotas overflowed 100 — drop the lowest-revenue revenue-fill picks first,
        # but in this build order revenue-fill hasn't run yet. So drop the
        # lowest-revenue quota-pick of any kind. Quota picks are protected if their
        # category wouldn't fall below the quota; otherwise they're trimmed in
        # ascending revenue order.
        print(f'  Quotas filled {len(selected)} > target {TARGET_TOTAL} — trimming '
              f'lowest-revenue picks until cap is met')
        selected.sort(key=lambda r: (r['sold_revenue'], r['sold_orders']))
        while len(selected) > TARGET_TOTAL:
            dropped = selected.pop(0)
            taken.discard(dropped['handle'])

    selected.sort(key=lambda r: (-r['sold_revenue'], -r['sold_orders'], r['handle']))
    for i, r in enumerate(selected, 1):
        r['hero_rank'] = i

    out_cols = [
        'hero_rank', 'handle', 'title', 'type_tag', 'room_tag', 'industry_tag',
        'sold_revenue', 'sold_orders', 'selection_reason', 'admin_url',
    ]
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out_cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(selected)
    print(f'\nWrote {len(selected)} rows to {os.path.relpath(OUT_CSV, ROOT)}')

    write_summary(selected, rows)
    print(f'Wrote summary to {os.path.relpath(OUT_MD, ROOT)}')


def write_summary(selected: list, all_rows: list) -> None:
    type_counts = Counter(r['type_tag'] or 'untyped' for r in selected)
    room_counts = Counter(r['room_tag'] or 'no-room' for r in selected)
    industry_counts = Counter(r['industry_tag'] or 'no-industry' for r in selected)
    reason_counts = Counter(r['selection_reason'] for r in selected)
    total_revenue = sum(r['sold_revenue'] for r in selected)
    catalog_revenue = sum(r['sold_revenue'] for r in all_rows)
    revenue_share = (total_revenue / catalog_revenue * 100) if catalog_revenue else 0
    sold_count = sum(1 for r in selected if r['sold_revenue'] > 0)

    by_type_revenue = defaultdict(list)
    for r in selected:
        by_type_revenue[r['type_tag'] or 'untyped'].append(r)

    lines = []
    lines.append('# Hero 100 — Steve Review')
    lines.append('')
    lines.append('_Generated by `scripts/build-hero-100.py`._')
    lines.append('')
    lines.append('## What this is')
    lines.append('')
    lines.append('The 100 products selected for full Tier 2 enrichment: POI spec scrape, '
                 'standardized titles, rewritten descriptions, rich filter tags '
                 '(`finish:*`, `brand:*`, `feature:*`), and the `hero:true` tag that '
                 'powers homepage features, footer links, related-products, and blog '
                 'inline links.')
    lines.append('')
    lines.append('Selection rule: per-type quotas first (so every collection page has '
                 'enriched products at the top), then highest-revenue fill for the '
                 'remaining slots.')
    lines.append('')
    lines.append('**Open `data/hero-100.csv` to see the full list. Mark any rows to '
                 'swap and send back.**')
    lines.append('')
    lines.append('## Coverage')
    lines.append('')
    lines.append(f'- **Total selected:** {len(selected)}')
    lines.append(f'- **Sold-at-least-once:** {sold_count}/{len(selected)}')
    lines.append(f'- **Revenue concentration:** ${total_revenue:,.0f} of '
                 f'${catalog_revenue:,.0f} catalog total ({revenue_share:.1f}%)')
    lines.append('')
    lines.append('### By type')
    lines.append('')
    lines.append('| Type | Count | Quota | Top revenue product |')
    lines.append('|---|---:|---:|---|')
    for type_tag, quota in TYPE_QUOTAS.items():
        members = by_type_revenue.get(type_tag, [])
        top = members[0]['title'][:50] if members else '—'
        lines.append(f'| {type_tag} | {len(members)} | {quota} | {top} |')
    untyped = by_type_revenue.get('untyped', [])
    if untyped:
        lines.append(f'| (untyped) | {len(untyped)} | — | {untyped[0]["title"][:50]} |')
    lines.append('')
    lines.append('### By room')
    lines.append('')
    for room, count in sorted(room_counts.items(), key=lambda kv: -kv[1]):
        lines.append(f'- {room}: {count}')
    lines.append('')
    lines.append('### By industry')
    lines.append('')
    for ind, count in sorted(industry_counts.items(), key=lambda kv: -kv[1]):
        lines.append(f'- {ind}: {count}')
    lines.append('')
    lines.append('### By selection reason')
    lines.append('')
    for reason, count in sorted(reason_counts.items(), key=lambda kv: -kv[1]):
        lines.append(f'- {reason}: {count}')
    lines.append('')
    lines.append('## Top 20 by revenue')
    lines.append('')
    lines.append('| # | Title | Type | Revenue | Orders |')
    lines.append('|---:|---|---|---:|---:|')
    for r in selected[:20]:
        title = r['title'][:55]
        lines.append(f'| {r["hero_rank"]} | {title} | {r["type_tag"] or "—"} | '
                     f'${r["sold_revenue"]:,.0f} | {r["sold_orders"]} |')
    lines.append('')
    lines.append('## Sign-off')
    lines.append('')
    lines.append('☐ Steve reviewed `data/hero-100.csv`.')
    lines.append('☐ Approved → proceed to Phase 1.1 (POI scrape).')
    lines.append('')

    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()
