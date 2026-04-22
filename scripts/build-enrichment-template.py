import csv
import re
from pathlib import Path

IN_CSV = Path(__file__).resolve().parent.parent / 'data' / 'enrichment-priorities.csv'
OUT_CSV = Path(__file__).resolve().parent.parent / 'data' / 'tier-a-enrichment-template.csv'

COLUMNS = [
    'Handle',
    'Title',
    'Category',          # chair | desk | table | storage | other — I pre-fill
    'SourceURL',         # Leo: competitor URL scraped from
    'Body_HTML',         # Leo: HTML description (only if current Body is empty/short)
    'SEO_Title',         # Leo: plaintext, ~60 chars
    'SEO_Description',   # Leo: plaintext, ~155 chars
    'Type',              # Leo: canonical Shopify type — see cheat sheet
    'Color',             # Leo: semicolon-separated, lowercase, hyphenated
    'Material',          # Leo: semicolon-separated, lowercase, hyphenated
    'Style',             # Leo: single value — modern | traditional | industrial | etc.
    'Suitable_Location', # Leo: semicolon-separated — office | home-office | etc.
    'Furniture_Fixture_Material',  # Leo: detailed — wood; metal; fabric; etc.
    'Upholstery_Material',         # Leo: chairs/sofas only — leatherette | vinyl | polyester | etc.
    'Seat_Type',         # Leo: chairs/stools only — upholstered | hard | upholstered-padded | etc.
    'Back_Type',         # Leo: chairs only — backless | full-back | low-back
    'Backrest_Type',     # Leo: chairs only — hard | upholstered | upholstered-padded
    'Wood_Finish',       # Leo: desks/tables with wood — walnut | oak | maple | etc.
    'Tabletop_Color',    # Leo: desks/tables — color name
    'Leg_Color',         # Leo: desks/tables — color name
    'Notes',             # Leo: anything I should know (dimensions, variants, etc.)
]


def categorize(title, type_or_cat):
    t = (title + ' ' + type_or_cat).lower()
    if any(k in t for k in ['chair', 'tilter', 'stool', 'seating', 'seat', 'sofa', 'lounge']):
        return 'chair'
    if any(k in t for k in ['desk', 'workstation']):
        return 'desk'
    if any(k in t for k in ['table', 'bench']):
        return 'table'
    if any(k in t for k in ['cabinet', 'file', 'pedestal', 'storage', 'bookcase', 'credenza']):
        return 'storage'
    return 'other'


def main():
    with IN_CSV.open(newline='', encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f) if r['Tier'] == 'A']
    rows.sort(key=lambda r: -float(r['Revenue']))

    out_rows = []
    for r in rows:
        cat = categorize(r['Title'], r['Type'])
        out_rows.append({
            'Handle': r['Handle'],
            'Title': r['Title'],
            'Category': cat,
            'SourceURL': '',
            'Body_HTML': '',
            'SEO_Title': '',
            'SEO_Description': '',
            'Type': '',
            'Color': '',
            'Material': '',
            'Style': '',
            'Suitable_Location': '',
            'Furniture_Fixture_Material': '',
            'Upholstery_Material': 'N/A' if cat not in ('chair',) else '',
            'Seat_Type': 'N/A' if cat not in ('chair',) else '',
            'Back_Type': 'N/A' if cat != 'chair' else '',
            'Backrest_Type': 'N/A' if cat != 'chair' else '',
            'Wood_Finish': 'N/A' if cat == 'chair' else '',
            'Tabletop_Color': 'N/A' if cat not in ('desk', 'table') else '',
            'Leg_Color': 'N/A' if cat not in ('desk', 'table', 'chair') else '',
            'Notes': '',
        })

    with OUT_CSV.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out_rows)
    print(f'Wrote {len(out_rows)} Tier A rows to {OUT_CSV}')


if __name__ == '__main__':
    main()
