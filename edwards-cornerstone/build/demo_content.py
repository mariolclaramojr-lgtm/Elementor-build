"""Demo content: 4 sample sermons (Sermon Manager) + 4 sample events (Modern Events Calendar)."""
import json, os, sys, time, datetime, importlib.util
spec = importlib.util.spec_from_file_location('m', os.environ['EDW_MCP']); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MEDIA = json.load(open(os.environ['EDW_MEDIA'])); STATE = os.environ['EDW_STATE']; st = json.load(open(STATE))
def tool(n, **a):
    r = m.call('tools/call', {'name': n, 'arguments': a}); t = r['result']['content'][0]['text']
    if r['result'].get('isError'): raise SystemExit(n + ' ERROR ' + t[:1500])
    try: return json.loads(t)
    except Exception: return t
VIDEO = 'https://www.youtube.com/watch?v=4FZBkcOA6jI'
sermons = [
 ('Rooted in Love', '2026-11-15 10:00:00', 'Rooted', 'Love', 'John', 'John 15:9-17', 'gallery-1',
  'Jesus invites us to remain in His love. In this message we look at what it means to be rooted in Christ, and how His love shapes the way we love one another.'),
 ('The Good Shepherd', '2026-11-08 10:00:00', 'Rooted', 'Faith', 'Psalms', 'Psalm 23', 'gallery-2',
  'The Lord is our shepherd. Psalm 23 reminds us that God leads, restores and walks with us through every season, even the darkest valley.'),
 ('A Harvest of Grace', '2026-11-01 10:00:00', 'Generosity', 'Giving', '2 Corinthians', '2 Corinthians 9:6-15', 'ministry-word',
  'Whoever sows generously will also reap generously. We explore cheerful giving as an act of worship and a response to the grace we have received.'),
 ('Walking in the Light', '2026-10-25 10:00:00', 'Rooted', 'Discipleship', '1 John', '1 John 1:5-10', 'live-bg',
  'God is light, and in Him there is no darkness at all. What does it look like to walk in the light, in honest fellowship with God and with each other?'),
]
st.setdefault('sermons', {})
for title, date, series, topic, book, passage, img, desc in sermons:
    ts = int(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp())
    args = dict(post_type='wpfc_sermon', title=title, status='publish', content=desc, date=date,
                meta={'sermon_date': ts, 'sermon_date_auto': 0, 'sermon_description': desc, 'bible_passage': passage, 'sermon_video_link': VIDEO},
                terms={'wpfc_preacher': ['First and Last Name'], 'wpfc_sermon_series': [series], 'wpfc_sermon_topics': [topic],
                       'wpfc_bible_book': [book], 'wpfc_service_type': ['Sunday Morning']},
                featured_image=MEDIA[img]['id'])
    if title in st['sermons']: args['id'] = st['sermons'][title]
    r = tool('cs_save_post', **args); st['sermons'][title] = r['id']; print('sermon', r['id'], title)

def t12(h):
    return (str(h % 12 or 12), 'AM' if h < 12 else 'PM')
events = [
 ('Community Thanksgiving Dinner', '2026-11-25', 18, 20, 'gallery-6', 'Bring a side dish and join us for a Thanksgiving meal together in the fellowship hall. Everyone is welcome!'),
 ("Women's Bible Study", '2026-12-02', 19, 20, 'ministry-word', "An evening of study, prayer and encouragement for women of every stage of life. Childcare available."),
 ('Youth Night', '2026-12-05', 18, 21, 'gallery-4', 'Worship, games and a short message for students in grades 6–12. Pizza is on us!'),
 ('Christmas Eve Candlelight Service', '2026-12-24', 18, 19, 'gallery-1', 'Celebrate the birth of Jesus with carols, scripture and candlelight. Invite your family and friends.'),
]
st.setdefault('events', {})
for title, day, sh, eh, img, desc in events:
    sh12, sap = t12(sh); eh12, eap = t12(eh)
    ev = dict(title=title, content=desc, status='publish', start=day, start_time_hour=sh12, start_time_minutes='0', start_time_ampm=sap,
              end=day, end_time_hour=eh12, end_time_minutes='0', end_time_ampm=eap, allday=0, repeat_status=0)
    args = dict(event=ev, featured_image=MEDIA[img]['id'])
    if title in st['events']: args['post_id'] = st['events'][title]
    r = tool('mec_save_event', **args); pid = r.get('post_id') or r.get('id'); st['events'][title] = pid
    print('event', pid, title, json.dumps(r.get('dates', r))[:160])
json.dump(st, open(STATE, 'w'), indent=1)
