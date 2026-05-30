#!/usr/bin/env python3
"""Build B4S2 enrichment payloads (8 products) in push-b4s1-enrichment.py shape.
Writes data/reports/b4s2-payloads/p1..p8.json. MISSING fields are omitted from metafields.
Source: web-sourced specs (session 2, 2026-05-30). who_its_for + body_html drafted to BBI voice."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data/reports/b4s2-payloads'
OUT.mkdir(parents=True, exist_ok=True)
PHONE = "1-800-835-9565"
CTA = (f'<p>Office Central and Brant Business Interiors are verified OECM partners, so '
       f'Ontario&rsquo;s public sector can buy without an open tender. Call '
       f'<strong>{PHONE}</strong> for a quote.</p>')

def body(hook, lede, features, who):
    feats = ''.join(f'<li>{f}</li>' for f in features)
    return (f'<p><strong>{hook}</strong></p>\n<p>{lede}</p>\n'
            f'<h3>Key features</h3>\n<ul>{feats}</ul>\n'
            f'<h3>Who it&rsquo;s for</h3>\n<p>{who}</p>\n{CTA}')

# Each draft: spec fields use sentinel None => MISSING (skipped from metafields)
DRAFTS = [
{
 'product_id':'9779951436089','handle':'fireking-storage-cabinet-72-high',
 'old_title':'Fireking storage cabinet 72" high — 72"',
 'title':'FireKing 72" Fire-Rated Storage Cabinet',
 'vendor':'FireKing','product_type':'Storage Cabinet',
 'tags':['brand:fireking','oecm-eligible','type:storage','feature:fire-rated','material:steel'],
 'seo_title':'FireKing 72" Fire-Rated Storage Cabinet',
 'seo_description':"FireKing's 72\" storage cabinet holds oversized documents, binders, and end-tab filing behind a UL Class 350 one-hour fire rating. OECM-eligible.",
 'image_alt':'FireKing 72-inch fire-rated steel storage cabinet, doors closed',
 'manufacturer':'FireKing','product_line':'Fire-Rated Storage Cabinet','model_codes':['CF7236-D'],
 'dimensions':'36"W x 19.3"D x 72"H exterior; 31-7/8"W x 15"D x 67-7/8"H interior',
 'weight':'892 lbs','weight_capacity':'Up to 160 lbs per shelf (evenly distributed)',
 'materials':'Welded steel body\n100% gypsum fire insulation reinforced with a 14-gauge galvanized steel wire lattice\nScratch-resistant powder-coat finish\nMedeco high-security keylock',
 'finishes_available':['Available in 11 cabinet colours'],
 'key_features':['UL Class 350 one-hour fire rating — interior stays below 350°F','Water-resistant against sprinklers and fire hoses','One fixed plus four adjustable shelves','Pull-out work tray and upright blueprint holder','High-security Medeco keylock'],
 'certifications':['UL Class 350 1-Hour Fire Rating'],
 'warranty':'Limited Lifetime Warranty (with in-fire replacement guarantee)',
 'country_of_manufacture':'United States',
 'who_its_for':'Records departments, municipal and hospital archives, and any institution that must protect oversized documents and media from fire.',
 'body': body('Fire-rated protection for the documents you can&rsquo;t afford to lose.',
   'This FireKing cabinet carries a U.L. Class 350 one-hour fire rating, shielding oversized documents, binders, end-tab filing, and banker&rsquo;s boxes from heat and water damage. A high-security Medeco keylock and water-resistant build keep contents secure long after the sprinklers stop.',
   ['UL Class 350 one-hour fire rating — interior stays below 350&deg;F','Water-resistant against sprinklers and fire hoses','One fixed plus four adjustable shelves, up to 160 lbs each','Pull-out work tray and upright blueprint holder','High-security Medeco keylock'],
   'Records departments, municipal and hospital archives, and any institution that must protect oversized documents and media from fire.'),
 'collects':[],'source':'good','source_url':'https://www.fireking.com/products/storage-cabinets',
 'missing':[],
},
{
 'product_id':'9702670467385','handle':'ranger-steel-4-post-table-42-w-x-30-d-with-drawer-safco',
 'old_title':'Ranger steel 4-post table 42”w x 30”d with drawer safco',
 'title':'Safco Ranger Steel 4-Post Drafting Table — 42"W × 30"D with Drawer',
 'vendor':'Safco','product_type':'Drafting Table',
 'tags':['brand:safco','oecm-eligible','type:drafting-tables','material:steel','feature:made-in-usa'],
 'seo_title':'Safco Ranger Steel 4-Post Drafting Table',
 'seo_description':"Safco's Ranger Steel 4-Post drafting table (42\"W × 30\"D, with tool drawer) tilts to 50° on a made-in-USA steel frame. OECM-eligible.",
 'image_alt':'Safco Ranger steel 4-post drafting table with tool drawer',
 'manufacturer':'Safco','product_line':'Ranger Steel 4-Post','model_codes':['7732A'],
 'dimensions':'42"W x 30"D x 37"H; worksurface tilts up to 50°; tool drawer 3-3/8"H x 10-3/8"W x 27-3/8"D',
 'weight':None,'weight_capacity':None,
 'materials':'Steel powder-coat frame\n1"-thick drawing board with steel end cleats\nReversible steel front apron',
 'finishes_available':['Custom paint colours','Custom laminate worksurface colours'],
 'key_features':['Worksurface tilts up to 50° from horizontal','1"-thick drawing board with steel end cleats','Reversible steel apron doubles as a pencil ledge','Lockable tool drawer for supplies','Custom paint and laminate finishes available'],
 'certifications':[],
 'warranty':'Limited Lifetime Warranty (Safco)',
 'country_of_manufacture':'United States',
 'who_its_for':'Architecture, engineering, and design studios that need a heavy-duty, made-to-order drafting surface.',
 'body': body('A made-in-USA drafting table built for daily studio punishment.',
   'The Ranger Steel 4-Post is a commercial-grade drafting table reinforced by a steel powder-coat frame and a 1&Prime;-thick drawing board with steel end cleats. The worksurface tilts up to 50&deg;, a reversible steel apron doubles as a pencil ledge, and a lockable tool drawer keeps supplies close.',
   ['Worksurface tilts up to 50&deg; from horizontal','1&Prime;-thick drawing board with steel end cleats','Reversible steel apron doubles as a pencil ledge','Lockable tool drawer for supplies','Custom paint and laminate finishes available'],
   'Architecture, engineering, and design studios that need a heavy-duty, made-to-order drafting surface.'),
 'collects':[],'source':'good','source_url':'https://www.safcoproducts.com/products/ranger-steel-4-post-table-42w-x-30d-with-tool-drawer-7732a',
 'missing':['weight','weight_capacity','certifications'],
},
{
 'product_id':'9982087758137','handle':'efloat-quattro-humanscale',
 'old_title':'Efloat quattro humanscale',
 'title':'Humanscale eFloat Quattro Sit-Stand Desk',
 'vendor':'Humanscale','product_type':'Sit-Stand Desk',
 'tags':['brand:humanscale','oecm-eligible','type:sit-stand-desks','feature:height-adjustable'],
 'seo_title':'Humanscale eFloat Quattro Sit-Stand Desk',
 'seo_description':'The Humanscale eFloat Quattro is a four-leg sit-stand desk with quiet motors, two presets, and 220 lb capacity — built for executive multi-monitor work.',
 'image_alt':'Humanscale eFloat Quattro four-leg sit-stand desk',
 'manufacturer':'Humanscale','product_line':'eFloat Quattro','model_codes':[],
 'dimensions':'Height 26.45"–44"; tops 23"x46", 23"x58", 29"x58", 29"x70"',
 'weight':None,'weight_capacity':'220 lbs (100 kg)',
 'materials':'Telescoping steel columns and structural steel frame\nLaminate or wood-veneer worksurface',
 'finishes_available':['Leg: White, Grey, Black','Top: White Oak, Continental Walnut, Natural Rift Oak, Stone Grey, and more'],
 'key_features':['Four-leg frame for stability under multi-monitor loads','Quiet electric height adjustment, 26.45"–44"','Two programmable height presets','220 lb lifting capacity','Tested to BIFMA standards'],
 'certifications':['BIFMA tested'],
 'warranty':'10-Year Warranty',
 'country_of_manufacture':None,
 'who_its_for':'Executive offices and design-forward workspaces where a premium four-leg sit-stand desk supports multi-monitor work.',
 'body': body('Premium four-leg design meets effortless sit-stand movement.',
   'With its refined four-leg frame, the eFloat Quattro brings executive-grade design to the sit/stand category without sacrificing stability. Quiet motors and two programmable presets make posture shifts effortless, and a 220 lb capacity handles even the heaviest multi-monitor setups.',
   ['Four-leg frame for stability under multi-monitor loads','Quiet electric height adjustment, 26.45&Prime;&ndash;44&Prime;','Two programmable height presets','220 lb lifting capacity','Tested to BIFMA standards'],
   'Executive offices and design-forward workspaces where a premium four-leg sit-stand desk supports multi-monitor work.'),
 'collects':[],'source':'good','source_url':'https://www.humanscale.com/products/standing-desks/efloat-quattro/custom',
 'missing':['weight','country_of_manufacture'],
},
{
 'product_id':'9827425616185','handle':'kensington-universal-charge-sync-tablet-cabinet',
 'old_title':'Kensington universal charge/sync tablet cabinet',
 'title':'Kensington Universal Charge & Sync Tablet Cabinet',
 'vendor':'Kensington','product_type':'Charging Cabinet',
 'tags':['brand:kensington','oecm-eligible','type:storage','feature:charging'],
 'seo_title':'Kensington Universal Charge & Sync Cabinet',
 'seo_description':'Store, charge, and sync up to 10 tablets at once with the Kensington Universal Cabinet — cooling fan, keyed security, and a universal cased-device fit.',
 'image_alt':'Kensington universal charge and sync cabinet for 10 tablets',
 'manufacturer':'Kensington','product_line':'Charge & Sync Cabinet','model_codes':['K67771'],
 'dimensions':'16.93"H x 15.75"W x 13.78"D (430 x 400 x 350 mm)',
 'weight':None,'weight_capacity':'Holds up to 10 tablets (stackable to 30)',
 'materials':'Steel cabinet construction\nTamper-resistant retracting front door',
 'finishes_available':['Black'],
 'key_features':['Stores, charges, and syncs up to 10 tablets at once','Stackable to manage up to 30 devices','Tamper-resistant retracting door with keyed lock','Built-in cooling fan prevents overheating','Universal fit — iPad, Galaxy Tab, Kindle and more, cases on'],
 'certifications':[],
 'warranty':'1-Year Limited Warranty',
 'country_of_manufacture':None,
 'who_its_for':'Schools, training rooms, and shared-device environments that store, secure, and charge a tablet fleet overnight.',
 'body': body('Ten tablets, charged, synced, and locked down overnight.',
   'This Kensington cabinet securely stores, charges, and syncs up to 10 tablets so a shared fleet is powered and ready each morning. Adjustable drawers fit devices in their cases, a tamper-resistant retracting door with keyed access keeps them safe, and a built-in cooling fan protects the hardware.',
   ['Stores, charges, and syncs up to 10 tablets at once','Stackable to manage up to 30 devices','Tamper-resistant retracting door with keyed lock','Built-in cooling fan prevents overheating','Universal fit &mdash; iPad, Galaxy Tab, Kindle and more, cases on'],
   'Schools, training rooms, and shared-device environments that store, secure, and charge a tablet fleet overnight.'),
 'collects':[],'source':'partial','source_url':'https://www.kensington.com/p/products/technology-device-security-products/charging-station-cables/charge-sync-cabinet-universal-tablet/',
 'missing':['weight','country_of_manufacture','warranty(confirm)'],
},
{
 'product_id':'10170179911993','handle':'alphabetter-stand-up-desk',
 'old_title':'Alphabetter stand-up desk',
 'title':'Safco AlphaBetter Height-Adjustable Student Desk',
 'vendor':'Safco','product_type':'Standing Desk',
 'tags':['brand:safco','oecm-eligible','type:standing-desks','feature:height-adjustable','segment:education'],
 'seo_title':'Safco AlphaBetter Height-Adjustable Desk',
 'seo_description':'The Safco AlphaBetter lets grade 3–12 students sit or stand through the day on a 16-gauge steel frame, with book box and swinging footrest. OECM-eligible.',
 'image_alt':'Safco AlphaBetter height-adjustable student stand-up desk with book box',
 'manufacturer':'Safco','product_line':'AlphaBetter','model_codes':['1224'],
 'dimensions':'28"W x 20"D top; height adjusts 29"–43"',
 'weight':None,'weight_capacity':'200 lbs',
 'materials':'16-gauge commercial-grade tubular steel frame, powder-coat finish\n1.2"-thick high-pressure laminate top\nMolded book box and swinging footrest bar',
 'finishes_available':['Premium laminate top colours','Frame: Black'],
 'key_features':['Height adjusts 29"–43" for seated or standing use','Swinging footrest bar lets students fidget without distraction','200 lb worksurface capacity','16-gauge commercial-grade steel frame','Molded book box keeps supplies organized'],
 'certifications':[],
 'warranty':'Limited Lifetime Warranty (5 years on mechanisms, glides, laminates, and electrical)',
 'country_of_manufacture':None,
 'who_its_for':'Grade 3–12 classrooms and active-learning environments that let students move, stand, and focus.',
 'body': body('Let students stand, move, and focus — without leaving their desk.',
   'The AlphaBetter adjustable-height desk gives grade 3&ndash;12 students the freedom to sit or stand through the school day and fidget without distracting the class. A 16-gauge commercial-grade steel frame stands up to the toughest classroom conditions, while the book box and swinging footrest bar keep students organized and engaged.',
   ['Height adjusts 29&Prime;&ndash;43&Prime; for seated or standing use','Swinging footrest bar lets students fidget without distraction','200 lb worksurface capacity','16-gauge commercial-grade steel frame','Molded book box keeps supplies organized'],
   'Grade 3&ndash;12 classrooms and active-learning environments that let students move, stand, and focus.'),
 'collects':[],'source':'good','source_url':'https://www.safcoproducts.com/products/alphabetter-adjustable-height-stand-up-desk-36-x-24-standard-top-and-swinging-footrest-bar-1206',
 'missing':['weight','country_of_manufacture','model_code(approx)'],
},
{
 'product_id':'9693072687417','handle':'drafting-table-safco-vista-drawing-table',
 'old_title':'Drafting table safco vista drawing table',
 'title':'Safco Vista Drafting Table',
 'vendor':'Safco','product_type':'Drafting Table',
 'tags':['brand:safco','oecm-eligible','type:drafting-tables','feature:height-adjustable'],
 'seo_title':'Safco Vista Drafting Table | Brant Business Interiors',
 'seo_description':'The Safco Vista drafting table adjusts 30"–46" and tilts to 45° on a lightweight tubular-steel frame with full-width footrest. Tool-free setup. OECM-eligible.',
 'image_alt':'Safco Vista white tubular-steel drafting and drawing table',
 'manufacturer':'Safco','product_line':'Vista','model_codes':['3960','3951'],
 'dimensions':'32-1/4"W x 27-1/2"D x 31-1/4"–47"H; 36"x48" top; tilts up to 45°',
 'weight':None,'weight_capacity':'50 lbs (evenly distributed)',
 'materials':'Lightweight tubular steel frame\nPowder-coat finish\nMelamine worksurface',
 'finishes_available':['Frame: White'],
 'key_features':['Height adjusts 30"–46" without tools','Worksurface tilts up to 45°','Full-width footrest for comfort','Easy-access adjustment knobs','Lightweight, durable tubular steel frame'],
 'certifications':[],
 'warranty':'Limited Lifetime Warranty (Safco)',
 'country_of_manufacture':None,
 'who_its_for':'Studios, classrooms, and drafting rooms needing an affordable, tool-free adjustable drawing table.',
 'body': body('A tool-free drawing table that adjusts to the way you work.',
   'The Safco Vista pairs a lightweight, durable tubular-steel frame with a full-width footrest for all-day comfort. Easy-access knobs adjust working height from 30&Prime; to 46&Prime; and tilt the surface up to 45&deg; &mdash; no tools required &mdash; so the table fits the task instead of the other way around.',
   ['Height adjusts 30&Prime;&ndash;46&Prime; without tools','Worksurface tilts up to 45&deg;','Full-width footrest for comfort','Easy-access adjustment knobs','Lightweight, durable tubular steel frame'],
   'Studios, classrooms, and drafting rooms needing an affordable, tool-free adjustable drawing table.'),
 'collects':[],'source':'good','source_url':'http://www.safcoproducts.com/vista-drawing-table-base-3960',
 'missing':['weight','certifications','country_of_manufacture'],
},
{
 'product_id':'9983576506681','handle':'humanscale-nova-lighting',
 'old_title':'Humanscale nova lighting',
 'title':'Humanscale Nova LED Task Light',
 'vendor':'Humanscale','product_type':'Task Light',
 'tags':['brand:humanscale','oecm-eligible','type:lighting','feature:led','feature:task-light'],
 'seo_title':'Humanscale Nova LED Task Light',
 'seo_description':'The Humanscale Nova delivers 91+ CRI, glare-free task light at just 7 watts, with touch dimming and an occupancy sensor. ENERGY STAR 2.0. OECM-eligible.',
 'image_alt':'Humanscale Nova LED task light on desktop base',
 'manufacturer':'Humanscale','product_line':'Nova','model_codes':[],
 'dimensions':'Reach 28.85"; lower arm 15.9", upper arm 15"',
 'weight':'12.5 lbs (packaged)','weight_capacity':None,
 'materials':'Aluminum and steel arm\nLED light engine with customized optical lens',
 'finishes_available':['White','Black','Light Grey'],
 'key_features':['91+ CRI, glare-free neutral light','Touch dimming, 14–100%, with occupancy sensor','440 lumens at just 7 watts','ENERGY STAR 2.0 certified, Red List–free','One-hand adjustability on a desktop base'],
 'certifications':['ENERGY STAR 2.0','Red List Free (Living Building Challenge)'],
 'warranty':'10-Year Warranty (24/7 use)',
 'country_of_manufacture':None,
 'who_its_for':'Private offices, workstations, and video-call setups that need precise, glare-free task lighting.',
 'body': body('Award-winning task light, engineered down to the last lumen.',
   'Humanscale&rsquo;s Nova combines advanced LED Light Guide technology with a 91+ CRI optical lens to cast a uniform, glare-free footprint that renders work vivid and clear. One-touch dimming and an occupancy sensor make it effortless to use and easy on energy &mdash; just 7 watts at full output.',
   ['91+ CRI, glare-free neutral light','Touch dimming, 14&ndash;100%, with occupancy sensor','440 lumens at just 7 watts','ENERGY STAR 2.0 certified, Red List&ndash;free','One-hand adjustability on a desktop base'],
   'Private offices, workstations, and video-call setups that need precise, glare-free task lighting.'),
 'collects':[],'source':'good','source_url':'https://www.humanscale.com/products/lighting/nova-desk-light/featured-products',
 'missing':['model_codes','country_of_manufacture'],
},
{
 'product_id':'9710313079097','handle':'safco-2130sl-desk-mount-for-monitor-keyboard',
 'old_title':'Safco 2130SL desk mount for monitor, keyboard',
 'title':'Safco 2130SL Sit-Stand Desktop Workstation',
 'vendor':'Safco','product_type':'Desktop Riser',
 'tags':['brand:safco','oecm-eligible','type:monitor-arms','feature:sit-stand'],
 'seo_title':'Safco 2130SL Sit-Stand Desktop Workstation',
 'seo_description':'The Safco 2130SL retrofits any desk into a sit-stand workstation — adjustable monitor and keyboard, concealed cables, 11 lb capacity. OECM-eligible.',
 'image_alt':'Safco 2130SL sit-stand desktop workstation converter, monitor and keyboard',
 'manufacturer':'Safco','product_line':'Active Collection','model_codes':['2130SL'],
 'dimensions':'26"W x 10-3/4"D platform; 28"D footprint; height adjusts 12-1/4"',
 'weight':None,'weight_capacity':'11 lbs',
 'materials':'Steel and aluminum construction',
 'finishes_available':['Silver'],
 'key_features':['Retrofits desks and worksurfaces up to 3" thick','Independently adjustable monitor and keyboard heights','26"W platform adjusts 12-1/4" in height','Concealed cable management','Holds up to 11 lbs; tool-free lift-and-tilt'],
 'certifications':[],
 'warranty':'Limited Lifetime Warranty (Safco)',
 'country_of_manufacture':None,
 'who_its_for':'Offices retrofitting existing desks into ergonomic sit-stand workstations without replacing furniture.',
 'body': body('Turn any desk into a sit-stand workstation — no new furniture required.',
   'Part of the Safco Active Collection, this desktop converter retrofits onto worksurfaces up to 3&Prime; thick and lifts your monitor and keyboard for healthier, standing work. Monitor and keyboard heights adjust independently with tool-free lift-and-tilt, and cables route through the arm for a clean, clutter-free desktop.',
   ['Retrofits desks and worksurfaces up to 3&Prime; thick','Independently adjustable monitor and keyboard heights','26&Prime;W platform adjusts 12-1/4&Prime; in height','Concealed cable management','Holds up to 11 lbs; tool-free lift-and-tilt'],
   'Offices retrofitting existing desks into ergonomic sit-stand workstations without replacing furniture.'),
 'collects':[],'source':'excellent','source_url':'https://www.safcoproducts.com (product spec block in current body_html)',
 'missing':['weight','country_of_manufacture'],
},
]

LIST_KEYS = {'model_codes','finishes_available','key_features','certifications'}
SINGLE_KEYS = ['manufacturer','product_line','dimensions','weight','weight_capacity','warranty','country_of_manufacture','who_its_for']

def mf_list(d):
    out=[]
    # ordered to mirror PDP spec table
    def add(key,typ,val):
        if val is None: return
        if isinstance(val,list):
            if not val: return
            out.append({'key':key,'type':typ,'value':json.dumps(val,ensure_ascii=False)})
        else:
            if str(val).strip()=='': return
            out.append({'key':key,'type':typ,'value':val})
    add('manufacturer','single_line_text_field',d['manufacturer'])
    add('product_line','single_line_text_field',d['product_line'])
    add('model_codes','list.single_line_text_field',d['model_codes'])
    add('dimensions','single_line_text_field',d['dimensions'])
    add('weight','single_line_text_field',d['weight'])
    add('weight_capacity','single_line_text_field',d['weight_capacity'])
    add('materials','multi_line_text_field',d['materials'])
    add('finishes_available','list.single_line_text_field',d['finishes_available'])
    add('key_features','list.single_line_text_field',d['key_features'])
    add('certifications','list.single_line_text_field',d['certifications'])
    add('warranty','single_line_text_field',d['warranty'])
    add('country_of_manufacture','single_line_text_field',d['country_of_manufacture'])
    add('who_its_for','single_line_text_field',d['who_its_for'])
    return out

for i,d in enumerate(DRAFTS,1):
    payload={
        'product_id':d['product_id'],'handle':d['handle'],
        'title':d['title'],'body_html':d['body'],
        'vendor':d['vendor'],'product_type':d['product_type'],
        'tags':d['tags'],'seo_title':d['seo_title'],'seo_description':d['seo_description'],
        'image_alt':d['image_alt'],'metafields':mf_list(d),'collects':d['collects'],
        # review metadata (ignored by push script)
        '_meta':{'old_title':d['old_title'],'source':d['source'],'source_url':d['source_url'],'missing':d['missing']},
    }
    (OUT/f'p{i}.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False))
    print(f"p{i}: {d['handle']}  title_len(seo)={len(d['seo_title'])} desc_len={len(d['seo_description'])} mf={len(payload['metafields'])} missing={d['missing']}")
print('written ->', OUT)
