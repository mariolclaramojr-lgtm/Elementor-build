"""Pro Header (updates 'Header - Main' #131) and a new site-wide Pro Footer."""
import json,os,sys,copy
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
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

logo=headline('Spurgeon','div','sp-logo',sub='Church',font=HEAD,weight='700',color=INK,href='/')
nav_inline={'_type':'nav-inline','_bp_base':'4_4','menu':'menu:25','class':'sp-hnav',
  'anchor_padding':'0.5em 0em','anchor_margin':'0px 0px 0px 32px','anchor_primary_font_family':BODY,'anchor_primary_font_size':'15px','anchor_primary_font_weight':'500',
  'anchor_primary_letter_spacing':'0em','anchor_primary_text_transform':'none','anchor_primary_text_color':INK,'anchor_primary_text_color_alt':CYANINK,
  'anchor_primary_particle':True,'anchor_primary_particle_color':CYAN,'anchor_primary_particle_height':'1px','anchor_primary_particle_scale':'scale-x',
  'anchor_primary_particle_transform_origin':'0% 100%','anchor_primary_particle_width':'100%','_modules':[]}
cta=button('Plan Your Visit','/plan-your-visit/','cyan',cls_extra='sp-hbtn')
cta['anchor_graphic']=False; cta['anchor_margin']='0px 0px 0px 40px'
navd.update({'anchor_primary_font_family':BODY,'anchor_primary_font_size':'17px','anchor_primary_font_weight':'600','anchor_primary_letter_spacing':'0em',
  'anchor_primary_text_transform':'none','anchor_primary_text_color':INK,'anchor_primary_text_color_alt':CYANINK,'anchor_primary_particle':False,
  'dropdown_bg_color':CREAM,'dropdown_width':'calc(100vw - 40px)','toggle_anchor_bg_color':'transparent','toggle_anchor_box_shadow_dimensions':'!0em 0em 0em 0em',
  'menu':'menu:2','class':'sp-mnav'})
bar={'_type':'bar','_bp_base':'4_4','class':'sp-hbar','bar_height':'76px','bar_bg_color':CREAM,'bar_sticky':True,'bar_sticky_shrink':'1',
  'bar_box_shadow_dimensions':'0px 1px 0px 0px','bar_box_shadow_color':'rgba(22,24,27,0.12)','bar_content_length':'calc(100% - 64px)',
  'bar_content_max_length':'1240px','bar_outer_spacing':'0px','bar_z_index':'9999',
  '_modules':[container([logo]),
              container([nav_inline,cta],hide=' md sm xs',extra={'container_flex_direction':'row','container_flex_align':'center'}),
              container([navd],hide=' lg xl')]}
r=call('cs_save_layout',{'id':131,'type':'header','title':'Header - Main','regions':{'top':[bar]},'settings':H['settings']},timeout=120)
print('header',json.dumps(r)[:300])

# ---------------- FOOTER ----------------
FINFO=('<ul class="sp-finfo"><li><span>Sundays</span>8:30 am &amp; 10:00 am</li><li><span>Wednesdays</span>6:30 pm</li>'
       f'<li><a href="{MAPS}" target="_blank" rel="noopener">1221 My Street<br>My Town, XX 12212</a></li>'
       '<li><a href="tel:9081231234">908-123-1234</a><br><a href="mailto:info@yourdomain.com">info@yourdomain.com</a></li></ul>')
fnav={'_type':'nav-inline','_bp_base':'4_4','menu':'menu:2','class':'sp-fnav','menu_items_flex_direction':'column','menu_flex_direction':'column','menu_flex_align':'flex-start',
  'anchor_padding':'5px 0px','anchor_primary_font_family':BODY,'anchor_primary_font_size':'15px','anchor_primary_font_weight':'400','anchor_primary_text_transform':'none',
  'anchor_primary_letter_spacing':'0em','anchor_primary_text_color':'rgba(255,255,255,0.85)','anchor_primary_text_color_alt':CYAN,'anchor_primary_particle':False,'_modules':[]}
def fcol(mods): return container(mods,extra={'container_flex_direction':'column','container_flex_align':'flex-start','container_flex_justify':'flex-start','container_width':'25%','container_padding':'0px 32px 0px 0px'})
logo_f=headline('Spurgeon','div','sp-logo',sub='Church',font=HEAD,weight='700',color=WHITE,href='/')
row1={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-top','bar_height':'auto','bar_bg_color':INK,'bar_padding':'72px 0px 56px 0px',
  'bar_content_length':'calc(100% - 64px)','bar_content_max_length':'1240px','bar_row_flex_align':'flex-start','bar_row_flex_wrap':True,
  'bar_bg_advanced':True,'bg_lower_type':'image','bg_lower_image':UP+'spurgeon-bg-footer.jpg','bg_upper_type':'color','bg_upper_color':'rgba(22,24,27,0.92)',
  '_modules':[fcol([logo_f,headline('Loving God. Loving People.','p','sp-tagline',font=HEAD,weight='500',color=WHITE)]),
              fcol([headline('Explore','div','sp-flabel',font=BODY),fnav]),
              fcol([headline('Visit','div','sp-flabel',font=BODY),text(FINFO,'sp-finfo-wrap')]),
              fcol([headline('Follow','div','sp-flabel',font=BODY),container([social('facebook','https://www.facebook.com/','facebook-f'),social('x','https://x.com/','x-twitter')],extra={'container_flex_direction':'row'})])]}
row2={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-credit','bar_height':'auto','bar_bg_color':INK,'bar_padding':'24px 0px',
  'bar_content_length':'calc(100% - 64px)','bar_content_max_length':'1240px','bar_border_width':'1px 0px 0px 0px','bar_border_style':'solid','bar_border_color':'rgba(255,255,255,0.16)',
  'bar_box_shadow_dimensions':'0px 0px 0px 0px',
  '_modules':[container([text('<span>&copy; Spurgeon Church</span>','sp-fcredit')]),container([text('<a href="https://reachrightstudios.com">church web design by REACHRIGHT</a>','sp-fcredit')])]}
row3={'_type':'bar','_bp_base':'4_4','class':'sp-footer-bar sp-fbar-mark','bar_height':'auto','bar_bg_color':INK,'bar_padding':'8px 0px 0px 0px','bar_scroll':False,'bar_overflow':'hidden',
  'bar_content_length':'100%','bar_row_flex_justify':'center','bar_box_shadow_dimensions':'0px 0px 0px 0px',
  '_modules':[container([headline('Spurgeon','div','sp-wordmark',font=HEAD,weight='700',color=CYAN)],extra={'container_flex_align':'center'})]}
fsettings={'customCSS':'','customJS':'','assignments':[{'group':True,'condition':'site:entire-site','value':''}],'assignment_priority':0}
r=call('cs_save_layout',{'type':'footer','title':'Footer - Main','regions':{'footer':[row1,row2,row3]},'settings':fsettings},timeout=120)
print('footer',json.dumps(r)[:300])
