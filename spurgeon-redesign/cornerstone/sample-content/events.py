import sys;sys.path.insert(0,__import__('os').environ['MCPDIR'])
import lib,json
E_=[
 ("Fall Family Festival","2026-10-31",(4,0,'PM'),(7,0,'PM'),"Families","Games, food trucks, a bounce house and a trunk-or-treat for kids of every age. Bring the whole family and a friend. Free for everyone.",162),
 ("Women's Night of Worship","2026-11-06",(7,0,'PM'),(9,0,'PM'),"Women","An evening of worship, prayer and encouragement for women of all ages. Desserts and coffee from 6:30 PM in the lobby.",165),
 ("Men's Breakfast","2026-11-14",(8,0,'AM'),(9,30,'AM'),"Men","A hot breakfast, a short talk and honest conversation around the tables. All men welcome, no sign-up needed.",164),
 ("Youth Game Night","2026-11-20",(6,30,'PM'),(9,0,'PM'),"Youth","Students in grades 6–12: pizza, games, worship and small groups. Bring a friend for a night of fun and real talk.",163),
 ("Thanksgiving Community Dinner","2026-11-24",(6,0,'PM'),(8,0,'PM'),"Community","Join us for a free Thanksgiving meal with our church family and neighbors. Everyone has a seat at the table.",196),
 ("Christmas Eve Candlelight Service","2026-12-24",(5,0,'PM'),(6,15,'PM'),"Services","Carols, the Christmas story and candlelight. A special service for the whole family, with childcare for little ones.",191),
]
ids={}
ids["Fall Family Festival"]=227
for t,d,s,e,cat,desc,img in E_:
  if t=="Fall Family Festival": continue
  ev={'title':t,'content':desc,'status':'publish','start':d,'start_time_hour':s[0],'start_time_minutes':s[1],'start_time_ampm':s[2],
      'end':d,'end_time_hour':e[0],'end_time_minutes':e[1],'end_time_ampm':e[2],'allday':0,'repeat_status':0,
      'location_id':1,'organizer_id':1}
  r=lib.call('mec_save_event',{'event':ev,'featured_image':img,'categories':[cat]})
  print(t,json.dumps(r)[:300]); ids[t]=r.get('id')
  if len(sys.argv)>1: break
json.dump(ids,open('event_ids.json','w'))
