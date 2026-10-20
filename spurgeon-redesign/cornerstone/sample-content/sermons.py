import sys;sys.path.insert(0,__import__('os').environ['MCPDIR'])
import lib,json,datetime,calendar

 ("Rooted in Grace","rooted-in-grace","2026-10-18","Rooted","First and Last Name","Ephesians","Grace",197,
  "Before we can bear fruit, we need roots. In this message we look at how grace, not effort, is the soil every healthy life grows from, and what it looks like to stay planted when seasons change."),
 ("Known and Loved","known-and-loved","2026-10-11","Rooted","First and Last Name","Psalms","Identity",198,
  "Psalm 139 tells us we are fully known and still fully loved. We talk about how that truth reshapes the way we see ourselves, our past and the people around us."),
 ("Strength for the Weary","strength-for-the-weary","2026-10-04","Rooted","Guest Speaker","Isaiah","Hope",199,
  "Isaiah 40 was written to tired people. This week we unpack God's promise to renew our strength, and practical ways to wait on Him when life feels heavy."),
 ("The Way of Love","the-way-of-love","2026-09-27","Better Together","First and Last Name","1 Corinthians","Love",195,
  "Love is patient, love is kind. We move 1 Corinthians 13 from the wedding reading to everyday life: at home, at work and in the church family."),
 ("Better Together","better-together","2026-09-20","Better Together","First and Last Name","Acts","Community",193,
  "The early church devoted themselves to teaching, fellowship, breaking bread and prayer. Here is why we were never meant to follow Jesus alone."),
 ("Salt and Light","salt-and-light","2026-09-13","Better Together","Guest Speaker","Matthew","Mission",185,
  "Jesus calls ordinary people salt and light. We explore what it means to make a difference right where God has placed you, in your street, school and workplace."),
]
ids={'rooted-in-grace':221}
for t,slug,d,series,spk,book,topic,img,desc in S:
  if slug=='rooted-in-grace': continue
  ts=calendar.timegm(datetime.datetime.strptime(d+" 10:00","%Y-%m-%d %H:%M").timetuple())
  r=lib.call('cs_save_post',{'post_type':'wpfc_sermon','title':t,'slug':slug,'status':'publish',
    'date':d+' 12:00:00','content':desc,'excerpt':desc,'featured_image':img,
    'meta':{'sermon_date':str(ts),'sermon_date_auto':'0','sermon_description':desc,'post_content_temp':desc,
            'wpfc_service_type':'24','Views':'0'},
    'terms':{'wpfc_sermon_series':[series],'wpfc_preacher':[spk],'wpfc_bible_book':[book],
             'wpfc_sermon_topics':[topic],'wpfc_service_type':['Sunday Service']}})
  print(t,json.dumps(r)[:200]); ids[slug]=r.get('id') if isinstance(r,dict) else r
  if len(sys.argv)>1: break
json.dump(ids,open('sermon_ids.json','w'))
