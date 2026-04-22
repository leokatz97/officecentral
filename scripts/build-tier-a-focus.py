import csv
from pathlib import Path

IN_CSV = Path(__file__).resolve().parent.parent / 'data' / 'enrichment-priorities.csv'
OUT_MD = Path(__file__).resolve().parent.parent / 'data' / 'tier-a-focus.md'


def main():
    with IN_CSV.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    tier_a = [r for r in rows if r['Tier'] == 'A']
    tier_a.sort(key=lambda r: -float(r['Revenue']))

    total_a_rev = sum(float(r['Revenue']) for r in tier_a)
    total_rev = sum(float(r['Revenue']) for r in rows if r['Revenue'])

    lines = []
    lines.append('# Tier A — Immediate Scrape Queue')
    lines.append('')
    lines.append(f'**{len(tier_a)} products** representing **${total_a_rev:,.0f}** '
                 f'({total_a_rev/total_rev*100:.0f}% of all revenue since 2023-01-01).')
    lines.append('')
    lines.append('These get every field filled — Body, SEO, and all spec metafields.')
    lines.append('')
    lines.append('| # | Title | Handle | Revenue | Units | Gaps |')
    lines.append('|---|---|---|---:|---:|---:|')
    for i, r in enumerate(tier_a, 1):
        title = r['Title'].replace('|', '\\|')
        lines.append(f'| {i} | {title} | `{r["Handle"]}` | ${float(r["Revenue"]):,.0f} | {r["Units"]} | {r["MissingCount"]} |')

    lines.append('')
    lines.append('## What each Tier A product is missing')
    lines.append('')
    for r in tier_a:
        gaps = r['MissingFields'].split('; ')
        lines.append(f'### {r["Title"]}')
        lines.append(f'*${float(r["Revenue"]):,.0f} · {r["Units"]} units · `{r["Handle"]}`*')
        lines.append('')
        content_gaps = [g for g in gaps if not g.startswith('mf:')]
        metafield_gaps = [g[3:] for g in gaps if g.startswith('mf:')]
        if content_gaps:
            lines.append(f'- **Content/taxonomy:** {", ".join(content_gaps)}')
        if metafield_gaps:
            lines.append(f'- **Spec metafields:** {", ".join(metafield_gaps)}')
        lines.append('')

    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT_MD}')


if __name__ == '__main__':
    main()
