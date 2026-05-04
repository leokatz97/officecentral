#!/usr/bin/env python3
"""
Create the specs.* product metafield definitions in Shopify Admin.
Idempotent — checks existing definitions first, only creates missing ones.

Usage:
  python3 scripts/create-specs-metafield-definitions.py             # DRY RUN
  python3 scripts/create-specs-metafield-definitions.py --live      # apply
"""
import json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / '.env'
for line in ENV_PATH.read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip())

SHOP = os.environ['SHOPIFY_STORE'].replace('.myshopify.com', '')
TOKEN = os.environ['SHOPIFY_TOKEN']
GQL = f'https://{SHOP}.myshopify.com/admin/api/2024-10/graphql.json'

# 12 specs.* definitions to create
DEFINITIONS = [
    ('manufacturer',           'Manufacturer',          'single_line_text_field',           'Manufacturer / brand name (e.g. "Global Furniture Group").'),
    ('product_line',           'Product Line',          'single_line_text_field',           'Product line / family (e.g. "2600 Series").'),
    ('model_codes',            'Model Codes',           'list.single_line_text_field',      'Manufacturer SKU(s) / model number(s).'),
    ('dimensions',             'Dimensions',            'single_line_text_field',           'Overall dimensions (e.g. "18.15\\"W x 26.56\\"D x 52\\"H").'),
    ('weight',                 'Weight',                'single_line_text_field',           'Product weight (e.g. "128 lbs (58.06 kg)").'),
    ('weight_capacity',        'Weight Capacity',       'single_line_text_field',           'Maximum load / weight rating.'),
    ('materials',              'Materials',             'multi_line_text_field',            'Materials and construction notes (long-form).'),
    ('finishes_available',     'Finishes Available',    'list.single_line_text_field',      'Finish / colour options.'),
    ('key_features',           'Key Features',          'list.single_line_text_field',      'Bulleted highlights for the PDP.'),
    ('certifications',         'Certifications',        'list.single_line_text_field',      'BIFMA, GREENGUARD, etc.'),
    ('warranty',               'Warranty',              'single_line_text_field',           'Warranty terms (e.g. "Limited Lifetime Warranty").'),
    ('country_of_manufacture', 'Country of Manufacture','single_line_text_field',           'ISO country name where the product is made.'),
]

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if 'errors' in data:
        raise RuntimeError(f'GraphQL errors: {data["errors"]}')
    return data['data']

def list_existing():
    q = '''
    {
      metafieldDefinitions(first: 50, namespace: "specs", ownerType: PRODUCT) {
        edges { node { key type { name } } }
      }
    }'''
    d = gql(q)
    return {e['node']['key']: e['node']['type']['name']
            for e in d['metafieldDefinitions']['edges']}

def create(key, name, type_name, description):
    m = '''
    mutation($d: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $d) {
        createdDefinition { id key type { name } }
        userErrors { field message code }
      }
    }'''
    inp = {
        'name': name,
        'namespace': 'specs',
        'key': key,
        'description': description,
        'type': type_name,
        'ownerType': 'PRODUCT',
        'pin': True,
    }
    d = gql(m, {'d': inp})
    res = d['metafieldDefinitionCreate']
    if res['userErrors']:
        raise RuntimeError(f'userErrors creating specs.{key}: {res["userErrors"]}')
    return res['createdDefinition']

def main():
    live = '--live' in sys.argv
    print(f'Mode: {"LIVE" if live else "DRY RUN"}')
    existing = list_existing()
    print(f'Existing specs.* definitions in Shopify: {len(existing)}')

    to_create = []
    skipped = []
    for key, name, type_name, desc in DEFINITIONS:
        if key in existing:
            skipped.append((key, existing[key]))
        else:
            to_create.append((key, name, type_name, desc))

    print(f'\n  To create: {len(to_create)}\n  Already exists: {len(skipped)}')
    if skipped:
        print('  Already exists:')
        for k, t in skipped:
            print(f'    specs.{k:25s}[{t}]')
    if to_create:
        print('  Will create:')
        for k, n, t, _ in to_create:
            print(f'    specs.{k:25s}[{t:35s}]  {n}')

    if not live:
        print(f'\n(Pass --live to create {len(to_create)} definitions)')
        return 0

    print('\n=== APPLYING LIVE ===')
    ok = fail = 0
    for k, n, t, d in to_create:
        try:
            res = create(k, n, t, d)
            ok += 1
            print(f'  OK   specs.{k}  ({res["type"]["name"]})')
        except Exception as e:
            fail += 1
            print(f'  FAIL specs.{k} — {e}')
    print(f'\n{"="*60}\nDone: {ok} OK, {fail} FAIL')
    return 0 if fail == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
