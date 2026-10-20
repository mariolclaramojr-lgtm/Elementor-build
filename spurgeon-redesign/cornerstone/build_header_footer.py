"""Pro Header (updates 'Header - Main' #131) and a new site-wide Pro Footer."""
import json,os,sys,copy
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from csel import *
H=json.load(open(os.environ['MCPDIR']+'/backup/header131.json'))
old_bar=H['regions']['top'][0]
navd=copy.deepcopy(old_bar['_modules'][2]['_modules'][0])   # existing mobile nav-dropdown

def container(mods,hide=None,cls='',extra=None):
    c={'_type':'container','_bp_base':'4_4','_modules':mods}
    if hide: c['hide_bp']=hide
    if cls: c['class']=cls
    if extra: c.update(extra)
    return c

def logo(dark=False):
    """Text logo: Headline (Bricolage 27px) + Subheadline 'CHURCH' (11px, wide tracking)."""
    h=headline('Spurgeon','div','sp-logo','h3',color=WHITE if dark else INK,href='/',sub='Church',sub_color=W60 if dark else 'rgba(22,24,27,0.75)',
               font_size='27px',font_weight='700',letter_spacing='-0.04em',line_height='1',margin='0px')
    h.update({'text_subheadline_font_family':BODY,'text_subheadline_font_size':'11px','text_subheadline_font_weight':'600','text_subheadline_letter_spacing':'0.42em',
              'text_subheadline_text_transform':'uppercase','text_subheadline_line_height':'1','text_subheadline_spacing':'6px','text_text_color_alt':WHITE if dark else INK})
    return h
logo_h=logo()
nav_inline={'_type':'nav-inline','_bp_base':'4_4','menu':'menu:25','class':'sp-hnav',
  'anchor_padding':'0.5em 0em','anchor_margin':'0px 0px 0px 32px','anchor_primary_font_family':BODY,'anchor_primary_font_size':'15px','anchor_primary_font_weight':'500',
  'anchor_primary_letter_spacing':'0em','anchor_primary_text_transform':'none','anchor_primary_text_color':INK,'anchor_primary_text_color_alt':CYANINK,
  'anchor_primary_particle':True,'anchor_primary_particle_color':CYAN,'anchor_primary_particle_height':'1px','anchor_primary_particle_scale':'scale-x',
  'anchor_primary_particle_transform_origin':'0% 100%','anchor_primary_particle_width':'100%','_modules':[]}
cta=button('Plan Your Visit','/plan-your-visit/','cyan',arrow=False,height='44px',pad='0px 18px')
cta['anchor_margin']='0px 0px 0px 40px'
navd.update({'anchor_primary_font_family':BODY,'anchor_primary_font_size':'17px','anchor_primary_font_weight':'600','anchor_primary_letter_spacing':'0em',
  'anchor_primary_text_transform':'none','anchor_primary_text_color':INK,'anchor_primary_text_color_alt':CYANINK,'anchor_primary_particle':False,
  'dropdown_bg_color':CREAM,'dropdown_width':'calc(100vw - 40px)','toggle_anchor_bg_color':'transparent','toggle_anchor_box_shadow_dimensions':'!0em 0em 0em 0em',
  'menu':'menu:2','class':'sp-mnav'})
bar={'_type':'bar','_bp_base':'4_4','class':'sp-hbar','bar_height':'76px','bar_bg_color':CREAM,'bar_sticky':True,'bar_sticky_shrink':'1',
  'bar_box_shadow_dimensions':'0px 1px 0px 0px','bar_box_shadow_color':'rgba(22,24,27,0.12)','bar_content_length':'calc(100% - 64px)',
  'bar_content_max_length':'1240px','bar_outer_spacing':'0px','bar_z_index':'9999',
  '_modules':[container([logo_h]),
              container([nav_inline,cta],hide=' md sm xs',extra={'container_flex_direction':'row','container_flex_align':'center'}),
              container([navd],hide=' lg xl')]}
r=call('cs_save_layout',{'id':131,'type':'header','title':'Header - Main','regions':{'top':[clean(bar)]},'settings':H['settings']},timeout=120)
print('header',json.dumps(r)[:300])

# ---------------- FOOTER ----------------
def finfo(lbl,val,href=None):
    h=info_item(lbl,val,dark=True,href=href); h['text_margin']='0px 0px 14px 0px'
    if href and href.startswith('http'): h['text_blank']=True
    return h
FINFO=[finfo('Sundays','8:30 am &amp; 10:00 am'),finfo('Wednesdays','6:30 pm'),finfo('Address','1221 My Street, My Town, XX 12212',MAPS),
       finfo('Call','908-123-1234','tel:9081231234'),finfo('Email','info@yourdomain.com','mailto:info@yourdomain.com')]
def flabel(t): return headline(t,'div','sp-flabel','label',color=W50,margin='0px 0px 16px 0px')
fnav={'_type':'nav-inline','_bp_base':'4_4','menu':'menu:2','class':'sp-fnav','menu_row_flexbox':True,'menu_row_flex_direction':'column','menu_row_flex_align':'flex-start','menu_row_flex_justify':'flex-start','menu_row_flex_wrap':False,
  'anchor_padding':'5px 0px','anchor_primary_font_family':BODY,'anchor_primary_font_size':'15px','anchor_primary_font_weight':'400','anchor_primary_text_transform':'none',
  'anchor_primary_letter_spacing':'0em','anchor_primary_text_color':'rgba(255,255,255,0.85)','anchor_primary_text_color_alt':CYAN,'anchor_primary_particle':False,'_modules':[]}
def fcol(mods):
    c=container(mods,extra={'container_col_flexbox':True,'container_row_flexbox':True,'container_row_flex_direction':'column','container_row_flex_align':'flex-start',
        'container_row_flex_justify':'flex-start','container_flex':'0 0 25%','container_width':'25%','container_padding':'0px 32px 0px 0px','container_margin':'0px'})
    c['_bp_data4_4']={'container_flex':['0 0 100%','0 0 50%','0 0 50%',None,None],'container_width':['100%','50%','50%',None,None],
                      'container_margin':['0px 0px 40px 0px','0px 0px 40px 0px','0px 0px 40px 0px',None,None]}
    return c
logo_f=logo(True); logo_f['text_margin']='0px 0px 24px 0px'
row1={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-top','bar_height':'auto','bar_bg_color':INK,'bar_padding':'72px 0px 56px 0px',
  'bar_content_length':'calc(100% - 64px)','bar_content_max_length':'1240px','bar_row_flex_align':'flex-start','bar_row_flex_wrap':True,
  'bar_bg_advanced':True,'bg_lower_type':'image','bg_lower_image':UP+'spurgeon-bg-footer.jpg','bg_upper_type':'color','bg_upper_color':'rgba(22,24,27,0.92)',
  '_modules':[fcol([logo_f,headline('Loving God. Loving People.','p','sp-tagline','h3',color=W90,font_size='24px',font_weight='500',line_height='1.25',margin='0px')]),
              fcol([flabel('Explore'),fnav]),
              fcol([flabel('Visit')]+FINFO),
              fcol([flabel('Follow'),container([social('facebook','https://www.facebook.com/','facebook-f'),social('x','https://x.com/','x-twitter')],extra={'container_flex_direction':'row'})])]}
row2={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-credit','bar_height':'auto','bar_bg_color':INK,'bar_padding':'24px 0px',
  'bar_content_length':'calc(100% - 64px)','bar_content_max_length':'1240px','bar_border_width':'1px 0px 0px 0px','bar_border_style':'solid','bar_border_color':'rgba(255,255,255,0.16)',
  'bar_box_shadow_dimensions':'0px 0px 0px 0px',
  '_modules':[container([headline('&copy; Spurgeon Church','div','sp-fcredit','label',color=W50,font_size='13px',letter_spacing='0em',text_transform='none')]),
              container([headline('church web design by REACHRIGHT','div','sp-fcredit','label',color=W50,href='https://reachrightstudios.com',font_size='13px',letter_spacing='0em',text_transform='none',text_color_alt=CYAN)])]}
row2['_bp_data4_4']={'bar_row_flex_direction':['column','column',None,None,None],'bar_row_flex_align':['flex-start','flex-start',None,None,None]}
wordmark=headline('Spurgeon','div','sp-wordmark','h1',color=CYAN,align='center',width='100%',font_size='clamp(72px,17.5vw,272px)',font_weight='700',letter_spacing='-0.05em',line_height='0.9',padding='0px 0px 0.14em 0px',margin='0px')
bp(wordmark,'text_text_align','left','left')
row3={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-mark','bar_height':'auto','bar_bg_color':INK,'bar_padding':'8px 0px 0px 0px','bar_scroll':False,'bar_overflow':'hidden',
  'bar_content_length':'100%','bar_row_flex_justify':'center','bar_box_shadow_dimensions':'0px 0px 0px 0px',
  '_modules':[container([wordmark],extra={'container_flex_align':'center','container_width':'100%'})]}
fsettings={'customCSS':'','customJS':'','assignments':[{'group':True,'condition':'site:entire-site','value':''}],'assignment_priority':0}
r=call('cs_save_layout',{'id':181,'type':'footer','title':'Footer - Main','regions':{'footer':clean([row1,row2,row3])},'settings':fsettings},timeout=120)
print('footer',json.dumps(r)[:300])
