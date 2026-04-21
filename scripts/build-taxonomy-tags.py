"""
Phase A of the taxonomy rebuild — generate the proposed tag CSV for Steve's review.

Reads data/reports/tier-2-disposition-review.csv (the source of truth — has
type_bucket already auto-classified) and produces data/reports/taxonomy-tags-
proposed.csv with three facet columns (type_tag, room_tag, industry_tag) plus
a bestseller flag derived from sold_orders.

READ-ONLY against Shopify. Writes one file.
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_CSV = os.path.join(ROOT, 'data', 'reports', 'tier-2-disposition-review.csv')
OUT_CSV = os.path.join(ROOT, 'data', 'reports', 'taxonomy-tags-proposed.csv')


TYPE_TAG_BY_BUCKET = {
    'Chairs': 'type:chairs',
    'Desks': 'type:desks',
    'Tables': 'type:tables',
    'Storage': 'type:storage',
    'Accessories': 'type:accessories',
    'Lounge': 'type:lounge',
    'Outdoor': 'type:outdoor',
}


ROOM_KEYWORDS = [
    ('room:boardroom',     ['boardroom', 'conference', 'meeting room', 'meeting table']),
    ('room:training-room', ['training', 'classroom', 'flip top', 'nesting table']),
    ('room:reception',     ['reception', 'guest', 'waiting', 'lobby']),
    ('room:break-room',    ['break room', 'cafeteria', 'lunchroom', 'cafe table', 'breakroom']),
    ('room:lounge',        ['lounge', 'sofa', 'loveseat', 'ottoman', 'club chair']),
    ('room:private-office',['executive', 'u-shape', 'u shape', 'l-shape', 'l shape',
                            'private office', 'managers', 'manager\'s', 'director']),
    ('room:open-plan',     ['workstation', 'cubicle', 'open plan', 'panel system',
                            'bench desk', 'benching']),
]


ROOM_DEFAULT_BY_BUCKET = {
    'Desks':   'room:private-office',
    'Tables':  'room:boardroom',
    'Storage': 'room:private-office',
    'Lounge':  'room:lounge',
}


INDUSTRY_KEYWORDS = [
    ('industry:first-nations', ['medicine wheel', 'indigenous', 'first nation']),
]


OTHER_BUCKET_HINTS = [
    # Accessories & parts first — catch hardware before falling through to desks
    ('type:accessories', ['monitor', ' arm', 'mat', 'cushion', 'hook', 'lamp',
                          'tray', 'rack', 'holder', 'divider', 'screen',
                          'partition', 'caster', 'power', 'usb', 'charging',
                          'whiteboard', 'white board', 'acoustic', 'planter',
                          'hutch only', 'shelf only', 'coat', 'footrest',
                          'keyboard', 'lectern', 'podium', 'phone booth',
                          'air purifier', 'air purification', 'av stand',
                          'machine stand', 'grommet', 'cord cover', 'keys',
                          'ionic feet', 'cross base', 'metal base',
                          'round metal base', 'dolly', 'door -', 'efloat',
                          'pod phone', 'soft pods', 'lighting', 'nova lighting',
                          'humanscale']),
    ('type:storage',     ['cabinet', 'pedestal', 'bookcase', 'bookshelf',
                          'credenza', 'locker', 'drawer', 'filing', 'file ',
                          'wardrobe', 'safe']),
    # Desks & workstation suites — L/U shape, reception unit, stand-up converters
    ('type:desks',       ['desk', 'workstation', 'l-shape', 'u-shape',
                          'l shape', 'u shape', 'lshape', 'ushape',
                          'reception unit', 'suite', 'sit to stand',
                          'sit-to-stand', 'sit-stand', 'innovation',
                          'boulevard']),
    ('type:tables',      ['table', 'bar leaner', 'round unit',
                          'square unit', 'wedge unit', 'rectangle unit',
                          'curve-', 'half round', 'medicine wheel', 'huddl',
                          'aktivity puddle']),
    ('type:chairs',      ['chair', 'stool', 'seating', 'tilter']),
]


# Titles that indicate service SKUs (not real products). Tag them so Steve
# knows to skip them rather than leaving them as "missing type".
SERVICE_KEYWORDS = ['installation', 'delivery charge', 'disposal program',
                    'additional services', 'dismantle', 'diet', 'carpeted floor',
                    'please select', 'colour$']


def infer_room(title_lower: str, type_bucket: str) -> str:
    for tag, keywords in ROOM_KEYWORDS:
        if any(k in title_lower for k in keywords):
            return tag
    return ROOM_DEFAULT_BY_BUCKET.get(type_bucket, '')


def infer_industry(title_lower: str) -> str:
    for tag, keywords in INDUSTRY_KEYWORDS:
        if any(k in title_lower for k in keywords):
            return tag
    return ''


def infer_type_for_other(title_lower: str) -> str:
    for tag, keywords in OTHER_BUCKET_HINTS:
        if any(k in title_lower for k in keywords):
            return tag
    return ''


def is_service_sku(title_lower: str) -> bool:
    return any(k in title_lower for k in SERVICE_KEYWORDS)


def main() -> None:
    rows_out = []
    type_tag_hits = 0
    room_tag_hits = 0
    industry_tag_hits = 0
    bestseller_hits = 0
    still_missing_type = 0

    with open(IN_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            handle = row['handle']
            title = row['title']
            type_bucket = row['type_bucket']
            sold_orders = int(row['sold_orders'] or 0)
            sold_revenue = float(row['sold_revenue'] or 0)
            admin_url = row['admin_url']

            title_lower = title.lower()

            type_tag = TYPE_TAG_BY_BUCKET.get(type_bucket, '')
            if not type_tag:
                type_tag = infer_type_for_other(title_lower)

            room_tag = infer_room(title_lower, type_bucket)
            industry_tag = infer_industry(title_lower)
            bestseller = 'true' if sold_orders >= 1 else ''

            notes = ''
            if not type_tag:
                if is_service_sku(title_lower):
                    notes = 'SERVICE SKU — not a real product, consider unpublishing or leave untagged'
                else:
                    notes = 'NEEDS MANUAL TYPE — in "Other" bucket and no keyword match'
                still_missing_type += 1

            if type_tag:
                type_tag_hits += 1
            if room_tag:
                room_tag_hits += 1
            if industry_tag:
                industry_tag_hits += 1
            if bestseller:
                bestseller_hits += 1

            rows_out.append({
                'handle': handle,
                'title': title,
                'type_bucket': type_bucket,
                'type_tag': type_tag,
                'room_tag': room_tag,
                'industry_tag': industry_tag,
                'bestseller': bestseller,
                'sold_orders': sold_orders,
                'sold_revenue': f'{sold_revenue:.2f}',
                'admin_url': admin_url,
                'notes': notes,
            })

    rows_out.sort(key=lambda r: (-float(r['sold_revenue']), r['title']))

    fieldnames = ['handle', 'title', 'type_bucket', 'type_tag', 'room_tag',
                  'industry_tag', 'bestseller', 'sold_orders', 'sold_revenue',
                  'admin_url', 'notes']

    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    total = len(rows_out)
    print(f'Wrote {OUT_CSV}')
    print(f'  Rows:            {total}')
    print(f'  type_tag set:    {type_tag_hits}  ({type_tag_hits/total*100:.1f}%)')
    print(f'  room_tag set:    {room_tag_hits}  ({room_tag_hits/total*100:.1f}%)')
    print(f'  industry_tag:    {industry_tag_hits}')
    print(f'  bestseller=true: {bestseller_hits}')
    print(f'  still missing type: {still_missing_type}')


if __name__ == '__main__':
    main()
