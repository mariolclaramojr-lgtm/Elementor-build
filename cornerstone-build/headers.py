import cs, json, layouts
from lc import url
ids = json.load(open('layout_ids.json'))
site = lambda c, v='': {'group': True, 'condition': c, 'value': v}
FEAT = '{{dc:post:featured_image}}'
SPECS = [
    # key, title, hero, assignments, priority
    ('header_solid', 'Lewis Header – Default (title hero)',
     dict(eyebrow_txt='Lewis Church', title='{{dc:post:title}}', image=FEAT),
     [site('site:entire-site')], 10),
    ('header_sermon', 'Lewis Header – Sermon (menu only)',
     dict(nav_image=url('photo-1504052434569-70ad5836ab65')),
     [site('single:post-type', 'wpfc_sermon')], 1),
    ('header_sermon_archive', 'Lewis Header – Sermon Archives',
     dict(eyebrow_txt='Messages', title='{{dc:archive:name}}', image=url('photo-1504052434569-70ad5836ab65'),
          lead_txt='Watch or listen to messages from this collection.'),
     [site('archive:post-type-with-term|wpfc_sermon|' + t) for t in
      ('wpfc_sermon_series', 'wpfc_preacher', 'wpfc_sermon_topics', 'wpfc_bible_book', 'wpfc_service_type')], 1),
    ('header_sermon_all', 'Lewis Header – All Sermons',
     dict(eyebrow_txt='Messages', title="Here's what we've been <em>talking about.</em>",
          image=url('photo-1504052434569-70ad5836ab65')),
     [site('archive:post-type', 'wpfc_sermon')], 2),
    ('header_event', 'Lewis Header – Event (menu only)',
     dict(nav_image=url('photo-1609234656388-0ff363383899')),
     [site('single:post-type', 'mec-events')], 1),
    ('header_archive', 'Lewis Header – Archives',
     dict(eyebrow_txt='Archive', title='{{dc:archive:name}}', image=url('photo-1438232992991-995b7058bbb3')),
     [site('archive:term'), site('archive:post-type', 'mec-events'), site('archive:post-type', 'post'),
      site('archive:author'), site('archive:search')], 3),
]
for key, title, hero, asg, prio in SPECS:
    regions = (layouts.header_regions(solid=True, nav_image=hero['nav_image']) if 'nav_image' in hero
               else layouts.header_regions(hero=hero))
    kw = dict(type='header', title=title, regions=regions,
              settings={'customCSS': layouts.HEADER_CSS, 'assignments': asg, 'assignment_priority': prio})
    if ids.get(key):
        kw['id'] = ids[key]
    r = cs.call('cs_save_layout', **kw)
    ids[key] = r.get('id') or ids.get(key)
    print(key, ids[key], r.get('summary'))
json.dump(ids, open('layout_ids.json', 'w'), indent=1)
cs.call('cs_purge_cache', all=True)
