"""Helpers that build native Cornerstone elements with their look set in the elements' own settings
(Design / Typography / Border / Background controls). No page CSS: classes are kept only as labels.

Responsive values use Cornerstone's breakpoint data: _bp_data4_4 = {key: [xs, sm, md, lg, xl]},
None = inherit from the next larger breakpoint (xl is the base value stored in the key itself)."""
import json,copy,os
TPL=json.load(open(os.path.join(os.environ['MCPDIR'],'tpl_home.json')))
HEAD='48656164696e6773'   # Global Font: Headings (Bricolage Grotesque)
BODY='426f647920436f7079' # Global Font: Body Copy (DM Sans)
C=lambda i:'global-color:'+i
INK,CREAM,SAND,CYAN,WHITE,SOFT,CYANINK=C('sp-ink'),C('sp-cream'),C('sp-sand'),C('4272616e64205072696d617279'),C('sp-white'),C('sp-ink-soft'),C('sp-cyan-ink')
LINE,LINE_L,LINE_S='rgba(22,24,27,0.12)','rgba(255,255,255,0.16)','rgba(22,24,27,0.85)'
W90,W70,W60,W50='rgba(255,255,255,0.9)','rgba(255,255,255,0.7)','rgba(255,255,255,0.6)','rgba(255,255,255,0.5)'
TINT='rgba(61,182,219,0.14)'
DARK='rgba(22,24,27,0.88)'
PAD='clamp(64px,7.5vw,112px)'
UP='https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2026/10/'
MAPS='https://www.google.com/maps/search/?api=1&query=1221+My+Street,+My+Town,+XX+12212'
MAP_EMBED='<iframe title="Map to Spurgeon Church" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11382.654663635445!2d-88.06987513195857!3d44.50155797910129!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8802fa51d9541b0f%3A0x45828001c843dcdd!2sLambeau%20Field!5e0!3m2!1sen!2sus!4v1671504339317!5m2!1sen!2sus" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>'
NO_SHADOW='0px 0px 0px 0px'

KEEP_CLASSES={'sp-form-card'}   # the only widget class global CSS still uses (cream fields in the form card)
def clean(node):
    """Drop widget classes that no CSS uses: styling lives in the element settings."""
    if isinstance(node,list):
        for n in node: clean(n)
        return node
    if isinstance(node,dict):
        if 'class' in node:
            keep=' '.join(c for c in str(node['class']).split() if c in KEEP_CLASSES)
            if keep: node['class']=keep
            else: node.pop('class')
        for v in node.values():
            if isinstance(v,(list,dict)): clean(v)
    return node

def _strip(d): return {k:v for k,v in d.items() if not k.startswith('effects_') and k not in ('_order','_id','_region')}
def bp(el,key,xs=None,sm=None,md=None,lg=None):
    """Set responsive overrides for one setting."""
    el.setdefault('_bp_data4_4',{})[key]=[xs,sm,md,lg,None]; return el

# ---------- layout ----------
def accent_line():
    """Short cyan rule under section headings (native Line element)."""
    return {'_type':'line','_bp_base':'4_4','line_direction':'horizontal','line_width':'48px','line_size':'3px','line_color':CYAN,
            'line_style':'solid','line_border_radius':'2px','line_margin':'4px 0px 24px 0px','_modules':[]}

def _accent(node):
    """Insert an accent line after every section heading (H2 / statement) in the tree."""
    if isinstance(node,dict):
        mods=node.get('_modules')
        if isinstance(mods,list):
            out=[]
            for m in mods:
                _accent(m); out.append(m)
                if isinstance(m,dict) and m.get('_type')=='headline' and set(str(m.get('class','')).split())&{'sp-h2','sp-statement'}:
                    out.append(accent_line())
            node['_modules']=out
    return node

def section(cls,mods,id_=None,bg_image=None,bg_video=None,bg_color=None,overlay=None,pad='normal'):
    s=_strip(copy.deepcopy(TPL['section']))
    for k in ('bg_lower_image','bg_lower_type','section_bg_advanced','undefined','section_bg_color'): s.pop(k,None)
    s.update({'section_padding':{'normal':f'{PAD} 0px','tight-top':f'0px 0px {PAD} 0px','none':'0px'}[pad],'section_margin':'0px','class':cls,'_modules':[m for m in mods if m]})
    if bg_color: s['section_bg_color']=bg_color
    if id_: s['id']=id_
    if bg_image: s.update({'section_bg_advanced':True,'bg_lower_type':'image','bg_lower_image':bg_image,'bg_lower_image_size':'cover','bg_lower_image_position':'center'})
    if bg_video: s.update({'section_bg_advanced':True,'bg_lower_type':'video','bg_lower_video':bg_video,'bg_lower_video_poster':UP+'spurgeon-hero-poster.jpg','bg_lower_video_loop':True,'bg_lower_video_object_fit':'cover'})
    if overlay: s.update({'section_bg_advanced':True,'bg_upper_type':'color','bg_upper_color':overlay,'section_bg_color':INK})
    return _accent(s)

def row(cols,layout,cls='',md=None,sm='100%',xs='100%',align=None,mt=None,gap_row='40px'):
    """Content row: 1240px wide with a 32px gutter (20px on phones)."""
    r=_strip(copy.deepcopy(TPL['layout-row'])); r.pop('_bp_data4_4',None)
    md=md or layout
    for k in ('layout_row_layout_xl','layout_row_layout_lg','layout_row_layout_md','layout_row_layout_sm','layout_row_layout_xs'): r.pop(k,None)
    r['_bp_data4_4']={'layout_row_layout':[xs,sm,(md if md!=layout else None),None,None]}
    r.update({'layout_row_layout':layout,'layout_row_reverse':False,'layout_row_gap_column':'32px','layout_row_gap_row':gap_row,
              'layout_row_global_container':False,'layout_row_width':'calc(100% - 64px)','layout_row_max_width':'1240px',
              'layout_row_padding':'0px','layout_row_margin':f'{mt or "0px"} auto 0px auto','_modules':cols})
    bp(r,'layout_row_width','calc(100% - 40px)','calc(100% - 40px)')
    if align: r['layout_row_flex_align']=align
    if cls: r['class']=cls
    return r

def col(mods,cls='',**st):
    """st: any layout_column_* setting without the prefix, e.g. bg_color=..., padding=..."""
    c=_strip(copy.deepcopy(TPL['layout-column'])); c.pop('layout_column_flex_justify',None)
    c.update({'layout_column_flexbox':False,'_modules':mods})
    for k,v in st.items(): c['layout_column_'+k]=v
    if cls: c['class']=cls
    return c

def card(mods,dark=False,cls='',pad='32px 28px 30px 28px'):
    """Column styled as a card: background, 1px border, 14px radius."""
    return col(mods,cls,bg_color='rgba(255,255,255,0.04)' if dark else '#ffffff',bg_color_alt='rgba(255,255,255,0.07)' if dark else '#ffffff',
               border_width='1px',border_style='solid',border_color=LINE_L if dark else LINE,border_color_alt='rgba(61,182,219,0.5)' if dark else LINE,
               border_radius='14px',padding=pad)

def card_div(mods,dark=False,cls='',pad='32px 28px 30px 28px',mb='0px'):
    """Div styled as a card (same look as card()); stack several in one column for a masonry layout."""
    return div(mods,cls,bg_color='rgba(255,255,255,0.04)' if dark else '#ffffff',bg_color_alt='rgba(255,255,255,0.07)' if dark else '#ffffff',
               border_width='1px',border_style='solid',border_color=LINE_L if dark else LINE,border_color_alt='rgba(61,182,219,0.5)' if dark else LINE,
               border_radius='14px',padding=pad,margin=f'0px 0px {mb} 0px')

def div(mods,cls='',**st):
    d={'_type':'layout-div','_bp_base':'4_4','layout_div_flexbox':False,'layout_div_padding':'0px','layout_div_margin':'0px','_modules':mods}
    for k,v in st.items(): d['layout_div_'+k]=v
    if cls: d['class']=cls
    return d

def actions(btns,center=False,mt='24px'):
    """Button group: flex row with 12px gap."""
    return div(btns,'sp-actions',flexbox=True,flex_direction='row',flex_wrap=True,flex_gap='12px',flex_align='center',
               flex_justify='center' if center else 'flex-start',margin=f'{mt} 0px 0px 0px')

# ---------- typography ----------
H_STYLES={  # font, size, weight, line-height, letter-spacing, transform, margin
 'h1':     (HEAD,'clamp(48px,7.6vw,120px)','600','0.9','-0.04em','none','0px 0px 32px 0px'),
 'page':   (HEAD,'clamp(46px,7vw,100px)','600','0.92','-0.04em','none','0px'),
 'h2':     (HEAD,'clamp(34px,4.2vw,58px)','600','1','-0.03em','none','0px 0px 20px 0px'),
 'h3':     (HEAD,'clamp(20px,1.7vw,24px)','600','1.2','-0.015em','none','0px 0px 12px 0px'),
 'statement':(HEAD,'clamp(28px,3.1vw,44px)','500','1.2','-0.02em','none','0px 0px 20px 0px'),
 'lead':   (HEAD,'clamp(20px,1.7vw,24px)','500','1.4','-0.015em','none','0px 0px 14px 0px'),
 'card':   (HEAD,'19px','500','1.2','-0.01em','none','20px 0px 0px 0px'),
 'label':  (BODY,'12px','600','1.4','0.16em','uppercase','0px'),
 'role':   (BODY,'12px','600','1.4','0.16em','uppercase','0px'),
}
def headline(html,tag,cls='',kind='h2',color=None,sub=None,sub_color=None,href=None,font=None,weight=None,align=None,**st):
    h=_strip(copy.deepcopy(TPL['headline']))
    for k in list(h):
        if k.startswith('text_subheadline') or 'shadow' in k: h.pop(k)
    f,size,w,lh,ls,tt,mg=H_STYLES[kind]
    h.update({'text_content':html,'text_tag':tag,'text_margin':mg,'text_padding':'0px','text_font_family':font or f,'text_font_size':size,
              'text_font_weight':weight or w,'text_line_height':lh,'text_letter_spacing':ls,'text_text_transform':tt,
              'text_text_shadow_dimensions':NO_SHADOW,'text_subheadline':False,'_modules':[]})
    if color: h['text_text_color']=color
    if align: h['text_text_align']=align
    if sub is not None:
        h.update({'text_subheadline':True,'text_subheadline_content':sub,'text_subheadline_font_family':font or f,'text_subheadline_font_size':size,
                  'text_subheadline_font_weight':weight or w,'text_subheadline_line_height':lh,'text_subheadline_letter_spacing':ls,
                  'text_subheadline_text_transform':tt,'text_subheadline_text_color':sub_color or color or INK,'text_subheadline_spacing':'0px',
                  'text_subheadline_text_shadow_dimensions':NO_SHADOW})
    if href: h.update({'text_link':True,'text_href':href})
    for k,v in st.items(): h['text_'+k]=v
    if cls: h['class']=cls
    return h

def label(t,dark=False,mb='40px'):
    """Section label: small caps with a hairline under it (Border + Padding settings)."""
    return headline(t,'div','sp-label','label',color=W60 if dark else SOFT,border_width='0px 0px 1px 0px',border_style='solid',
                    border_color=LINE_L if dark else LINE,padding='0px 0px 16px 0px',margin=f'0px 0px {mb} 0px')

def text(html,cls='sp-copy',dark=False,size='17px',lh='1.7',color=None,**st):
    t=_strip(copy.deepcopy(TPL['text']))
    t.update({'text_content':html,'text_font_family':BODY,'text_font_weight':'400','text_font_size':size,'text_line_height':lh,
              'text_text_color':color or (W70 if dark else SOFT),'text_text_shadow_dimensions':NO_SHADOW,'_modules':[]})
    for k,v in st.items(): t['text_'+k]=v
    if cls: t['class']=cls
    return t

# ---------- buttons ----------
BTN={ # bg, bg hover, text, text hover, border, border hover
 'ink':     (INK,CYANINK,'#ffffff','#ffffff',INK,CYANINK),
 'cyan':    (CYAN,'#ffffff',INK,INK,CYAN,'#ffffff'),
 'white':   ('#ffffff',CYAN,INK,INK,'#ffffff',CYAN),
 'line':    ('transparent','rgba(255,255,255,0.08)','#ffffff','#ffffff','rgba(255,255,255,0.5)','#ffffff'),
 'line-ink':('transparent',INK,INK,'#ffffff',LINE_S,INK),
}
def button(label,href,kind,blank=False,arrow=True,height='52px',pad='0px 24px'):
    bg,bga,tc,tca,bc,bca=BTN[kind]
    b=_strip(copy.deepcopy(TPL['button']))
    b.update({'anchor_text_primary_content':label,'anchor_href':href,'class':'sp-btn sp-btn--'+kind,
              'anchor_margin':'0px','anchor_padding':pad,'anchor_height':height,'anchor_flex_direction':'row-reverse','anchor_flex_align':'center','anchor_flex_justify':'center',
              'anchor_bg_color':bg,'anchor_bg_color_alt':bga,'anchor_border_width':'1px','anchor_border_style':'solid','anchor_border_color':bc,'anchor_border_color_alt':bca,
              'anchor_border_radius':'8px','anchor_text_margin':'0px',
              'anchor_primary_font_family':BODY,'anchor_primary_font_size':'15px','anchor_primary_font_weight':'600','anchor_primary_line_height':'1',
              'anchor_primary_letter_spacing':'0em','anchor_primary_text_transform':'none','anchor_primary_text_color':tc,'anchor_primary_text_color_alt':tca,
              'anchor_graphic':arrow,'anchor_graphic_icon':'arrow-right','anchor_graphic_icon_alt':'arrow-right','anchor_graphic_icon_font_size':'14px',
              'anchor_graphic_icon_color':tc,'anchor_graphic_icon_color_alt':tca,'anchor_graphic_margin':'0px 0px 0px 12px',
              # hover: lift (Effects › Alt), soft shadow (Box Shadow alt colour) and arrow scale (Graphic › Interaction)
              'anchor_box_shadow_dimensions':'0px 12px 24px -12px','anchor_box_shadow_color':'transparent','anchor_box_shadow_color_alt':'rgba(22,24,27,0.35)',
              'anchor_graphic_interaction':'x-anchor-scale-up','effects_alt':True,'effects_transform_alt':'translate(0px, -3px)',
              'effects_duration':'300ms','effects_timing_function':'cubic-bezier(0.400, 0.000, 0.200, 1.000)','_modules':[]})
    if blank: b['anchor_blank']=True
    return b

# ---------- media ----------
def image(url,alt,cls='',w=1600,h=1600,**st):
    i=_strip(copy.deepcopy(TPL['image']))
    i.update({'image_src':url,'image_alt':alt,'image_width':w,'image_height':h,'image_inner_border_radius':'0px','image_display':'block','_modules':[]})
    for k,v in st.items(): i['image_'+k]=v
    if cls: i['class']=cls
    return i

def round_image(url,alt,max_w='460px',ring=True,dark=False,center=True,href=None,ring_gap='10px',mobile_max=None,cls='sp-circle'):
    """Round photo: square source + 50% radius; the ring is the element's own padding + 1px border."""
    from square_images import sq
    st=dict(styled_width='100%',styled_max_width=max_w,outer_border_radius='50%',inner_border_radius='50%',object_fit='cover',
            margin='0px auto 0px auto' if center else '0px')
    if ring: st.update(padding=ring_gap,border_width='1px',border_style='solid',border_color=LINE_L if dark else LINE,bg_color='transparent')
    if href: st.update(link=True,href=href)
    i=image(sq(url),alt,cls,1000,1000,**st)
    if center: bp(i,'image_margin','0px','0px')
    if mobile_max: bp(i,'image_styled_max_width',mobile_max,mobile_max)
    return i

def raw(html,cls=''):
    r={'_type':'raw-content','_bp_base':'4_4','raw_content':html,'_modules':[]}
    if cls: r['class']=cls
    return r

def form(gf_id,cls='sp-form'):
    return {'_type':'form-integration','_bp_base':'4_4','form_integration_type':'gravity-forms','form_integration_gravityforms_id':str(gf_id),'class':cls,'_modules':[]}

def gmap(cls='sp-map'):
    m={'_type':'map','_bp_base':'4_4','map_type':'embed','map_embed_code':MAP_EMBED,'class':cls,'frame_width':'100%','frame_content_sizing':'fixed-height',
       'frame_content_height':'560px','frame_border_radius':'14px','frame_overflow':'hidden','_modules':[]}
    return bp(m,'frame_content_height','380px','380px','380px')

def video(src,poster,cls='sp-video',embed=None):
    v=_strip(copy.deepcopy(TPL['video']))
    if embed: v.update({'video_type':'embed','video_embed_code':embed})
    else: v.update({'mejs_source_files':src,'mejs_poster':poster})
    v.update({'class':cls,'frame_width':'100%','frame_content_sizing':'aspect-ratio','frame_content_aspect_ratio_width':'16','frame_content_aspect_ratio_height':'9',
              'frame_border_radius':'14px','frame_overflow':'hidden','frame_margin':'32px 0px 0px 0px','_modules':[]})
    return v

def icon(name,dark=False,cls='sp-icon',mb='24px'):
    return {'_type':'icon','_bp_base':'4_4','icon':name,'icon_width':'48px','icon_height':'48px','icon_font_size':'22px','icon_border_radius':'10px',
            'icon_color':CYAN if dark else CYANINK,'icon_bg_color':'rgba(61,182,219,0.16)' if dark else TINT,'icon_margin':f'0px 0px {mb} 0px','class':cls,'_modules':[]}

def crumbs(cls='sp-crumbs',center=True):
    c={'_type':'breadcrumbs','_bp_base':'4_4','breadcrumbs_home_label_type':'text','breadcrumbs_home_label_text':'Home','class':cls,
       'breadcrumbs_flex_justify':'center' if center else 'flex-start','breadcrumbs_margin':'0px 0px 20px 0px',
       'breadcrumbs_font_family':BODY,'breadcrumbs_font_size':'12px','breadcrumbs_font_weight':'600','breadcrumbs_line_height':'1.4',
       'breadcrumbs_links_letter_spacing':'0.2em','breadcrumbs_links_text_transform':'uppercase','breadcrumbs_links_color':'rgba(255,255,255,0.75)',
       'breadcrumbs_links_color_alt':'#ffffff','breadcrumbs_delimiter_color':CYAN,'breadcrumbs_delimiter_spacing':'10px','_modules':[]}
    if center: bp(c,'breadcrumbs_flex_justify','flex-start','flex-start')
    return c

def social(network,href,icon_name):
    return {'_type':'social','_bp_base':'4_4','anchor_href':href,'anchor_blank':True,'anchor_graphic_icon':icon_name,'anchor_graphic_icon_alt':icon_name,
            'anchor_width':'44px','anchor_height':'44px','anchor_bg_color':'transparent','anchor_bg_color_alt':CYAN,'anchor_border_width':'1px','anchor_border_style':'solid',
            'anchor_border_color':LINE_L,'anchor_border_color_alt':CYAN,'anchor_border_radius':'8px','anchor_box_shadow_dimensions':NO_SHADOW,
            'anchor_graphic_icon_color':'#ffffff','anchor_graphic_icon_color_alt':INK,'anchor_graphic_icon_font_size':'16px','anchor_margin':'0px 8px 0px 0px','class':'sp-social','_modules':[]}

# ---------- shared content as native elements ----------
def info_item(lbl,value,dark=False,href=None,big=False):
    """Small caps label + value, one Headline element (primary = label, subheadline = value)."""
    h=headline(lbl,'div','sp-info','label',color=W50 if dark else SOFT,sub=value,href=href,margin='0px')
    if big: h.update({'text_subheadline_font_family':HEAD,'text_subheadline_font_size':'clamp(26px,2.3vw,34px)','text_subheadline_font_weight':'600',
                      'text_subheadline_letter_spacing':'-0.04em','text_subheadline_line_height':'1','text_subheadline_spacing':'12px'})
    else: h.update({'text_subheadline_font_family':BODY,'text_subheadline_font_size':'15px','text_subheadline_font_weight':'400','text_subheadline_letter_spacing':'0em',
                    'text_subheadline_line_height':'1.5','text_subheadline_spacing':'2px'})
    h.update({'text_subheadline_text_transform':'none','text_subheadline_text_color':W90 if dark else INK})
    if href: h['text_subheadline_text_color_alt']=CYAN if dark else CYANINK
    return h

def contact_row(icon_name,value,href,blank=False):
    """Icon tile + link with a hairline under it (Headline with Graphic)."""
    h=headline(value,'div','sp-contact-row','lead',color=INK,href=href,font=BODY,weight='500',font_size='17px',line_height='1.4',letter_spacing='0em',
               margin='0px',padding='14px 0px 14px 0px',border_width='0px 0px 1px 0px',border_style='solid',border_color=LINE,
               flexbox=True,flex_direction='row',flex_align='center',text_color_alt=CYANINK,
               graphic=True,graphic_type='icon',graphic_icon=icon_name,graphic_icon_alt=icon_name,graphic_icon_font_size='18px',
               graphic_icon_width='40px',graphic_icon_height='40px',graphic_icon_border_radius='10px',graphic_icon_bg_color=TINT,
               graphic_icon_color=CYANINK,graphic_margin='0px 12px 0px 0px')
    if blank: h['text_blank']=True
    return h
