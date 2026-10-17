#!/usr/bin/env python3
"""Track-A — re-sync the 15 existing comparison/buying-guide articles to the
deepened content.

Updates EXISTING article IDs (no create) via Admin-API PUT, keeping the existing
handle (handle is NEVER sent in the PUT) and NEVER touching the `published` field
(so the article's live/draft state is preserved exactly). Reuses the
bbi-publish-post engine's body transform (FAQ chips + interlinks + byte-match) and
gates. Paced + 429-retry; backs up current body_html + metafields first; hardened
independent readback per article.

State expectation (`--expect`):
  draft  (default) — the article must currently be `published:false`; readback
                     asserts it is STILL `published:false`. (the original create-phase
                     flow, used to re-sync the 15 drafts before they were flipped live.)
  live             — the article must currently be PUBLISHED; readback asserts it is
                     STILL published. Use this for a post-flip re-sync of a live
                     article (e.g. slot 10, which missed the pre-flip re-sync and went
                     live on the shallow pre-deepen body). The PUT never sends
                     `published`, so published_at is untouched.

Subcommands:
  verify   --expect {draft,live}     readback every article: exists + state matches (no writes)
  update   --expect {draft,live}     per-slot: backup -> transform -> PUT body/title ->
                                     upsert metafields -> readback (DRY-RUN by default; --live to write)
Both accept `--only 10` (comma-separated slots) to restrict to specific slots.

Slot -> article_id map is the create-drafts record in BBI-Session-Kickoff/bbi-build-state.md.
"""
import os, sys, json, time, argparse, datetime, urllib.error

# import the proven engine
ENGINE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', '.claude', 'skills', 'bbi-publish-post', 'scripts')
sys.path.insert(0, ENGINE_DIR)
import faq_interlink_engine as eng  # noqa: E402

BLOG = eng.BLOG_DEFAULT  # 108557861177
DRAFTS = 'data/content-drafts'
BDIR = 'data/backups/articles'

# slot -> (article_id, pack_filename) ; handles intentionally NOT used in writes
SLOTS = [
    ("07", "689250926905", "07-choose-office-furniture-supplier-ontario-PACK.json"),
    ("08", "689250959673", "08-where-to-buy-office-furniture-dealer-bigbox-online-PACK.json"),
    ("09", "689250992441", "09-lease-vs-buy-office-furniture-canada-PACK.json"),
    ("10", "689251025209", "10-public-sector-institutional-office-furniture-ontario-PACK.json"),
    ("11", "689251057977", "11-commercial-vs-consumer-grade-office-furniture-PACK.json"),
    ("12", "689251090745", "12-sit-stand-vs-fixed-desks-office-PACK.json"),
    ("13", "689251123513", "13-open-plan-vs-private-offices-PACK.json"),
    ("14", "689251156281", "14-cubicles-vs-open-benching-workstations-PACK.json"),
    ("15", "689251189049", "15-office-pods-vs-building-meeting-rooms-PACK.json"),
    ("16", "689251221817", "16-mesh-vs-upholstered-office-chairs-PACK.json"),
    ("17", "689251254585", "17-task-chair-vs-executive-chair-PACK.json"),
    ("18", "689251287353", "18-filing-cabinets-vs-shelving-vs-pedestals-PACK.json"),
    ("19", "689251320121", "19-conference-table-boardroom-buying-guide-PACK.json"),
    ("20", "689251352889", "20-reception-area-furniture-guide-PACK.json"),
    ("21", "689251418425", "21-office-design-trends-2026-ontario-PACK.json"),
]


def selected_slots(a):
    if not getattr(a, 'only', None):
        return SLOTS
    want = {s.strip().lstrip('0') or '0' for s in a.only.split(',') if s.strip()}
    return [t for t in SLOTS if (t[0].lstrip('0') or '0') in want]


def api_retry(path, method='GET', payload=None, tries=5):
    """eng.api with paced 429/5xx retry (the create-pass lesson)."""
    delay = 3
    for attempt in range(1, tries + 1):
        try:
            return eng.api(path, method, payload)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < tries:
                wait = delay * attempt
                print(f"    {e.code} on {method} {path} -> retry {attempt}/{tries} after {wait}s")
                time.sleep(wait)
                continue
            raise


def upsert_metafield(article_id, namespace, key, mtype, value):
    """PUT existing metafield by id, else POST a new one."""
    mfs = api_retry(f"blogs/{BLOG}/articles/{article_id}/metafields.json")['metafields']
    match = [m for m in mfs if m['namespace'] == namespace and m['key'] == key]
    if match:
        mid = match[0]['id']
        api_retry(f"metafields/{mid}.json", 'PUT',
                  {'metafield': {'id': mid, 'value': value, 'type': mtype}})
        return 'updated'
    api_retry(f"blogs/{BLOG}/articles/{article_id}/metafields.json", 'POST',
              {'metafield': {'namespace': namespace, 'key': key,
                             'type': mtype, 'value': value}})
    return 'created'


def cmd_verify(a):
    want_live = (a.expect == 'live')
    label = 'published:true' if want_live else 'published:false'
    print(f"expect={a.expect} ({label})")
    print(f"{'slot':<5}{'article_id':<14}{'exists':<8}{'published_at':<28}{'state'}")
    allok = True
    for slot, aid, _pack in selected_slots(a):
        try:
            art = api_retry(f"blogs/{BLOG}/articles/{aid}.json")['article']
            pub = art.get('published_at')
            is_live = pub is not None
            ok = (is_live == want_live)
            allok = allok and ok
            print(f"{slot:<5}{aid:<14}{'YES':<8}{str(pub):<28}"
                  f"{label + ' OK' if ok else 'WARNING: state mismatch'}")
            time.sleep(1)
        except Exception as e:
            allok = False
            print(f"{slot:<5}{aid:<14}{'NO':<8}{'-':<28}ERROR {e}")
    print(f"\nALL {label} ->", 'PASS' if allok else 'FAIL')
    sys.exit(0 if allok else 1)


def cmd_update(a):
    want_live = (a.expect == 'live')
    os.makedirs(BDIR, exist_ok=True)
    ts = eng._ts()
    results = []
    for slot, aid, pack in selected_slots(a):
        print(f"\n=== Slot {slot} (article {aid}) [expect={a.expect}] ===")
        spec = eng.load_spec(os.path.join(DRAFTS, pack))
        # meta gates
        tlen, mlen = len(spec['title']), len(spec['meta_description'])
        if not (tlen < 60 and mlen <= 155):
            print(f"  META GATE FAIL title={tlen} meta={mlen} -> SKIP")
            results.append((slot, aid, 'META-FAIL'))
            continue
        # pre-read existing + confirm expected publish state
        art = api_retry(f"blogs/{BLOG}/articles/{aid}.json")['article']
        is_live = art.get('published_at') is not None
        if is_live != want_live:
            cur = 'PUBLISHED' if is_live else 'published:false'
            print(f"  ABORT: article state is {cur} but --expect {a.expect}. SKIP "
                  f"(published_at={art.get('published_at')}).")
            results.append((slot, aid, 'STATE-MISMATCH-SKIP'))
            continue
        # backup current body + metafields
        if a.live:
            open(f"{BDIR}/resync-{aid}-body-before-{ts}.html", 'w').write(art['body_html'] or '')
            mfs = api_retry(f"blogs/{BLOG}/articles/{aid}/metafields.json")['metafields']
            json.dump(mfs, open(f"{BDIR}/resync-{aid}-metafields-before-{ts}.json", 'w'),
                      indent=2, ensure_ascii=False)
        # transform deepened body (FAQ chips + interlinks + byte-match)
        new_body, items, linkrep, ok, msg, canonical = eng._transform(spec)
        print(f"  transform: {len(items)} FAQ items; links: {', '.join(linkrep)}")
        print(f"  BYTE-MATCH (pre-write): {'PASS' if ok else 'FAIL'} - {msg}")
        if not ok:
            print("  ABORT slot: byte-match failed before write.")
            results.append((slot, aid, 'BYTEMATCH-FAIL'))
            continue
        print(f"  body len live={len(art['body_html'] or '')} -> new={len(new_body)} "
              f"| title: {art['title']!r} -> {spec['title']!r}")
        if not a.live:
            print("  DRY RUN: would PUT title+body (handle untouched), upsert "
                  f"faq.items + global.title_tag + global.description_tag, keep {'published:true' if want_live else 'published:false'}.")
            results.append((slot, aid, 'DRYRUN-OK'))
            continue
        # PUT body + title only (NO handle, NO published -> publish state preserved)
        api_retry(f"blogs/{BLOG}/articles/{aid}.json", 'PUT',
                  {'article': {'id': int(aid), 'title': spec['title'], 'body_html': new_body}})
        # upsert metafields
        fi = upsert_metafield(aid, 'faq', 'items', 'list.single_line_text_field',
                              json.dumps(spec['faq_items'], ensure_ascii=False))
        tt = upsert_metafield(aid, 'global', 'title_tag', 'single_line_text_field', spec['title'])
        dt = upsert_metafield(aid, 'global', 'description_tag', 'single_line_text_field',
                              spec['meta_description'])
        print(f"  metafields: faq.items={fi} title_tag={tt} description_tag={dt}")
        # hardened independent readback
        rb = api_retry(f"blogs/{BLOG}/articles/{aid}.json")['article']
        rb_pairs, _ = eng.faq_items_metafield(BLOG, aid)
        # Shopify normalizes whitespace at tag boundaries, so a byte-exact body == is a
        # known false-negative. Authoritative body checks: visible-text equivalence +
        # every interlink href present. faq.items is byte-matched separately.
        import re as _re
        from bs4 import BeautifulSoup as _BS
        def _txt(h): return _re.sub(r'\s+', ' ', _BS(h or '', 'html.parser').get_text(' ')).strip()
        def _hrefs(h): return {x.get('href') for x in _BS(h or '', 'html.parser').find_all('a') if x.get('href')}
        body_text_ok = (_txt(rb['body_html']) == _txt(new_body))
        links_ok = _hrefs(new_body).issubset(_hrefs(rb['body_html']))
        body_ok = body_text_ok and links_ok
        faq_ok, faq_msg = eng.bytematch(eng.parse_visible_faq(rb['body_html']), rb_pairs)
        title_ok = (rb['title'] == spec['title'])
        rb_live = rb.get('published_at') is not None
        state_ok = (rb_live == want_live)
        # meta readback
        rb_mfs = api_retry(f"blogs/{BLOG}/articles/{aid}/metafields.json")['metafields']
        def mval(ns, k):
            x = [m for m in rb_mfs if m['namespace'] == ns and m['key'] == k]
            return x[0]['value'] if x else None
        tt_ok = (mval('global', 'title_tag') == spec['title'])
        dt_ok = (mval('global', 'description_tag') == spec['meta_description'])
        json.dump({'article': rb, 'metafields': rb_mfs},
                  open(f"{BDIR}/resync-{aid}-AFTER-{ts}.json", 'w'), indent=2, ensure_ascii=False)
        allok = body_ok and faq_ok and title_ok and state_ok and tt_ok and dt_ok
        statelbl = 'published:true' if want_live else 'published:false'
        print(f"  READBACK body_text={body_text_ok} links={links_ok} faq={faq_ok}({faq_msg}) "
              f"title={title_ok} title_tag={tt_ok} desc_tag={dt_ok} {statelbl}={state_ok} "
              f"-> {'PASS' if allok else 'FAIL'}")
        results.append((slot, aid, 'PASS' if allok else 'FAIL'))
        if not allok:
            print("  WARNING: readback FAIL — investigate before continuing.")
        time.sleep(a.pace)  # space the calls (create-pass 429 lesson)

    print("\n================ SUMMARY ================")
    for slot, aid, st in results:
        print(f"  slot {slot}  {aid}  {st}")
    npass = sum(1 for _, _, s in results if s in ('PASS', 'DRYRUN-OK'))
    print(f"  {npass}/{len(results)} OK")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('verify')
    v.add_argument('--expect', choices=('draft', 'live'), default='draft')
    v.add_argument('--only', help='comma-separated slots, e.g. 10')
    v.set_defaults(fn=cmd_verify)
    u = sub.add_parser('update')
    u.add_argument('--live', action='store_true')
    u.add_argument('--expect', choices=('draft', 'live'), default='draft')
    u.add_argument('--only', help='comma-separated slots, e.g. 10')
    u.add_argument('--pace', type=float, default=5.0, help='seconds between articles')
    u.set_defaults(fn=cmd_update)
    a = p.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
