"""Small helpers that build native Cornerstone elements, shaped like the site's own examples."""
import json,copy,os
TPL=json.load(open(os.path.join(os.environ['MCPDIR'],'tpl_home.json')))
HEAD='48656164696e6773'   # Global Font: Headings (Bricolage Grotesque)
BODY='426f647920436f7079' # Global Font: Body Copy (DM Sans)
C=lambda i:'global-color:'+i
INK,CREAM,CYAN,WHITE,SOFT,CYANINK=C('sp-ink'),C('sp-cream'),C('4272616e64205072696d617279'),C('sp-white'),C('sp-ink-soft'),C('sp-cyan-ink')
UP='https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2026/10/'
MAPS='https://www.google.com/maps/search/?api=1&query=1221+My+Street,+My+Town,+XX+12212'
MAP_EMBED='<iframe title="Map to Spurgeon Church" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11382.654663635445!2d-88.06987513195857!3d44.50155797910129!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8802fa51d9541b0f%3A0x45828001c843dcdd!2sLambeau%20Field!5e0!3m2!1sen!2sus!4v1671504339317!5m2!1sen!2sus" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'

def _strip(d): return {k:v for k,v in d.items() if not k.startswith('effects_') and k not in ('_order','_id','_region')}

def section(cls,mods,id_=None,bg_image=None,bg_video=None,bg_color=None,overlay=None):
    s=_strip(copy.deepcopy(TPL['section']))
    for k in ('bg_lower_image','bg_lower_type','section_bg_advanced','undefined','section_bg_color'): s.pop(k,None)
    s.update({'section_padding':'0px','section_margin':'0px','class':cls,'_modules':mods})
    if bg_color: s['section_bg_color']=bg_color
    if id_: s['id']=id_
    if bg_image: s.update({'section_bg_advanced':True,'bg_lower_type':'image','bg_lower_image':bg_image,'bg_lower_image_size':'cover','bg_lower_image_position':'center'})
    if bg_video: s.update({'section_bg_advanced':True,'bg_lower_type':'video','bg_lower_video':bg_video,'bg_lower_video_poster':UP+'spurgeon-hero-poster.jpg','bg_lower_video_loop':True,'bg_lower_video_object_fit':'cover'})
    if overlay: s.update({'section_bg_advanced':True,'bg_upper_type':'color','bg_upper_color':overlay})
    return s

def row(cols,layout,cls='',md=None,sm='100%',xs='100%'):
    r=_strip(copy.deepcopy(TPL['layout-row'])); r.pop('_bp_data4_4',None)
    md=md or layout
    for k in ('layout_row_layout_xl','layout_row_layout_lg','layout_row_layout_md','layout_row_layout_sm','layout_row_layout_xs'): r.pop(k,None)
    # responsive layouts live in _bp_data (order: xs, sm, md, lg, xl; null = inherit the base/desktop value)
    r['_bp_data4_4']={'layout_row_layout':[xs,sm,(md if md!=layout else None),None,None]}
    r.update({'layout_row_layout':layout,'layout_row_reverse':False,'layout_row_gap_column':'32px',
              'layout_row_gap_row':'40px','layout_row_global_container':False,'layout_row_margin':'0px auto 0px auto','_modules':cols})
    if cls: r['class']=cls
    return r

def col(mods,cls=''):
    c=_strip(copy.deepcopy(TPL['layout-column'])); c.pop('layout_column_flex_justify',None)
    c.update({'layout_column_flexbox':False,'_modules':mods})
    if cls: c['class']=cls
    return c

def div(mods,cls):
    return {'_type':'layout-div','_bp_base':'4_4','layout_div_flexbox':False,'layout_div_padding':'0px','layout_div_margin':'0px','class':cls,'_modules':mods}

def headline(html,tag,cls,sub=None,font=HEAD,weight='600',color=None,href=None):
    h=_strip(copy.deepcopy(TPL['headline']))
    for k in list(h):
        if k.startswith('text_subheadline') and k!='text_subheadline_text_shadow_dimensions': h.pop(k)
    h.update({'text_content':html,'text_tag':tag,'class':cls,'text_margin':'0em','text_padding':'0em','text_font_family':font,
              'text_font_weight':weight,'text_font_size':'1em','text_line_height':'1.1','_modules':[]})
    if color: h['text_text_color']=color
    if sub is not None:
        h.update({'text_subheadline':True,'text_subheadline_content':sub,'text_subheadline_font_family':font,'text_subheadline_font_weight':weight})
    else: h['text_subheadline']=False
    if href: h.update({'text_link':True,'text_href':href})
    return h

def text(html,cls='sp-copy'):
    t=_strip(copy.deepcopy(TPL['text']))
    t.update({'text_content':html,'class':cls,'text_font_family':BODY,'text_font_weight':'400','text_line_height':'1.7','_modules':[]})
    return t

def button(label,href,kind,blank=False,cls_extra=''):
    b=_strip(copy.deepcopy(TPL['button']))
    b.pop('anchor_bg_color',None)
    b.update({'anchor_text_primary_content':label,'anchor_href':href,'class':('sp-btn sp-btn--'+kind+' '+cls_extra).strip(),
              'anchor_margin':'0px','anchor_padding':'0em 1.5em','anchor_box_shadow_dimensions':'0px 0px 0px 0px','anchor_border_radius':'8px',
              'anchor_primary_text_transform':'none','anchor_primary_letter_spacing':'0em','anchor_primary_font_family':BODY,'anchor_primary_font_weight':'600',
              'anchor_graphic_icon':'arrow-right','anchor_graphic_icon_alt':'arrow-right','_modules':[]})
    if blank: b['anchor_blank']=True
    return b

def image(url,alt,cls='sp-circle',w=1600,h=1600):
    i=_strip(copy.deepcopy(TPL['image']))
    i.update({'image_src':url,'image_alt':alt,'image_width':w,'image_height':h,'image_inner_border_radius':'0px','class':cls,'_modules':[]})
    return i

def raw(html,cls=''):
    r={'_type':'raw-content','_bp_base':'4_4','raw_content':html,'_modules':[]}
    if cls: r['class']=cls
    return r

def form(gf_id,cls='sp-form'):
    return {'_type':'form-integration','_bp_base':'4_4','form_integration_type':'gravity-forms','form_integration_gravityforms_id':str(gf_id),'class':cls,'_modules':[]}

def gmap(cls='sp-map'):
    return {'_type':'map','_bp_base':'4_4','map_type':'embed','map_embed_code':MAP_EMBED,'class':cls,'frame_width':'100%','frame_content_sizing':'fixed-height','frame_content_height':'560px','_modules':[]}

def accordion(items,cls='sp-accordion'):
    a=_strip(copy.deepcopy(TPL['accordion']))
    a.update({'class':cls,'_modules':[{'_type':'accordion-item','_bp_base':'4_4','accordion_item_header_content':t,'_modules':[]} for t in items]})
    return a

def video(src,poster,cls='sp-video',embed=None):
    v=_strip(copy.deepcopy(TPL['video']))
    if embed:
        v.update({'video_type':'embed','video_embed_code':embed})
    else:
        v.update({'mejs_source_files':src,'mejs_poster':poster})
    v.update({'class':cls,'_modules':[]})
    return v

def icon(name,cls='sp-icon'):
    return {'_type':'icon','_bp_base':'4_4','icon':name,'icon_width':'48px','icon_height':'48px','icon_font_size':'22px','icon_border_radius':'10px','icon_color':CYANINK,'icon_bg_color':'rgba(61,182,219,0.14)','class':cls,'_modules':[]}

def crumbs(cls='sp-crumbs'):
    return {'_type':'breadcrumbs','_bp_base':'4_4','breadcrumbs_home_label_type':'text','breadcrumbs_home_label_text':'Home','class':cls,'_modules':[]}

def social(network,href,icon_name):
    return {'_type':'social','_bp_base':'4_4','anchor_href':href,'anchor_blank':True,'anchor_graphic_icon':icon_name,'anchor_graphic_icon_alt':icon_name,
            'anchor_width':'44px','anchor_height':'44px','anchor_bg_color':'transparent','anchor_bg_color_alt':CYAN,'anchor_border_width':'1px','anchor_border_style':'solid',
            'anchor_border_color':'rgba(255,255,255,0.16)','anchor_border_color_alt':CYAN,'anchor_border_radius':'8px','anchor_box_shadow_dimensions':'0px 0px 0px 0px',
            'anchor_graphic_icon_color':'#ffffff','anchor_graphic_icon_color_alt':INK,'anchor_graphic_icon_font_size':'16px','anchor_margin':'0px 8px 0px 0px','class':'sp-social','_modules':[]}

# ---- shared content ----
def ic_svg(p): return f'<span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{p}</svg></span>'
I_PIN='<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><path d="M12 12.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>'
I_PHONE='<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'
I_AT='<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'
TIMES_HTML='<div class="sp-times"><div class="sp-time"><span>Sunday Mornings</span><strong>8:30 <i>&amp;</i> 10:00<small>am</small></strong></div><div class="sp-time"><span>Wednesday Evenings</span><strong>6:30<small>pm</small></strong></div></div>'
CONTACT_HTML=(f'<ul class="sp-contact"><li>{ic_svg(I_PIN)}<a href="{MAPS}" target="_blank" rel="noopener">1221 My Street, My Town, XX&nbsp;12212</a></li>'
              f'<li>{ic_svg(I_PHONE)}<a href="tel:9081231234">908-123-1234</a></li><li>{ic_svg(I_AT)}<a href="mailto:info@yourdomain.com">info@yourdomain.com</a></li></ul>')
