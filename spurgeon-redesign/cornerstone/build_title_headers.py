"""Pro Headers for sermon + event archives/singles: main nav bar + photo title band (dynamic title, breadcrumbs)."""
import json,os,sys,copy
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from csel import *
MP=json.load(open(os.environ['MCPDIR']+'/media_map.json'))
main=call('cs_get_layout',{'id':131},timeout=90)
navbar=copy.deepcopy(main['regions']['top'][0])
def strip_ids(n):
    if isinstance(n,list):
        for x in n: strip_ids(x)
        return
    for k in ('_id','_m'): n.pop(k,None)
    strip_ids(n.get('_modules',[]))
strip_ids(navbar)
def title_bar(dc):
    """Photo title band, same height and type as the page hero: bar padding + container min-height (no CSS)."""
    h=headline(dc,'h1','sp-page-title','page',color=WHITE,align='center'); bp(h,'text_text_align','left','left')
    wrap={'_type':'container','_bp_base':'4_4','class':'sp-title-wrap','_modules':[crumbs(),h],
          'container_row_flexbox':True,'container_col_flexbox':True,'container_row_flex_direction':'column','container_row_flex_justify':'center',
          'container_row_flex_align':'center','container_text_align':'center','container_flex':'1 1 100%','container_width':'100%',
          'container_min_height':'calc(clamp(300px,42svh,460px) - 128px)'}
    bp(wrap,'container_row_flex_align','flex-start','flex-start'); bp(wrap,'container_text_align','left','left')
    return {'_type':'bar','_bp_base':'4_4','class':'sp-title-bar','bar_height':'auto','bar_padding':'64px 0px 64px 0px','bar_bg_color':INK,
      'bar_content_length':'calc(100% - 64px)','bar_content_max_length':'1240px','bar_row_flex_justify':'center','bar_box_shadow_dimensions':'0px 0px 0px 0px',
      'bar_bg_advanced':True,'bg_lower_type':'image','bg_lower_image':UP+MP['1507692049790-de58290a4334'],'bg_upper_type':'color','bg_upper_color':'rgba(22,24,27,0.72)',
      '_modules':[wrap]}
SERMON_TAX=['wpfc_sermon_series','wpfc_preacher','wpfc_sermon_topics','wpfc_bible_book','wpfc_service_type']
def a(cond,val=''): return {'group':True,'condition':cond,'value':val}
archive_assign=[a('archive:post-type','mec-events')]+[a(f'archive:post-type-with-term|wpfc_sermon|{t}') for t in SERMON_TAX]+[a('archive:post-type-with-term|mec-events|mec_category')]
single_assign=[a('single:post-type','wpfc_sermon'),a('single:post-type','mec-events')]
ids={}
p=os.environ['MCPDIR']+'/title_header_ids.json'
if os.path.exists(p): ids=json.load(open(p))
for key,title,dc,assign in [('archive','Header - Sermon & Event Archives','{{dc:archive:title}}',archive_assign),('single','Header - Sermon & Event Single','{{dc:post:title}}',single_assign),('messages','Header - Messages Archive','Messages',[a('archive:post-type','wpfc_sermon')])]:
    args={'type':'header','title':title,'regions':{'top':[copy.deepcopy(navbar),title_bar(dc)]},
          'settings':{'customCSS':'','customJS':'','assignments':assign,'assignment_priority':(2 if key=='messages' else 1),'multi_region':False}}
    if key in ids: args['id']=ids[key]
    r=call('cs_save_layout',args,timeout=120); ids[key]=r['id']; print(key,r['id'],json.dumps(r['settings'])[:200])
json.dump(ids,open(p,'w'))
# main header: make sure it loses to these (lowest priority wins)
m=call('cs_get_layout',{'id':131},timeout=90)
s=m['settings']; s['assignment_priority']=10
r=call('cs_save_layout',{'id':131,'type':'header','title':'Header - Main','regions':m['regions'],'settings':s},timeout=120); print('main priority',r['settings'].get('assignment_priority'))
call('cs_purge_cache',{},timeout=60)
