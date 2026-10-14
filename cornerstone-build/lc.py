"""Lewis Church — native Cornerstone element builders (global colors + fonts, element style keys)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = json.load(open(os.path.join(HERE, 'media.json')))

hx = lambda s: s.encode().hex()
# Global colors
ACCENT = 'global-color:4272616e64205365636f6e64617279'
ACCENT_DARK = 'global-color:4c696e6b'
ACCENT_LIGHT = 'global-color:4272616e64205072696d617279'
ESP = 'global-color:32b99313-937c-45b5-a6e4-6f57cce68eee'
ESP2 = 'global-color:4c696e6b20496e746572616374696f6e'
INK_SOFT = 'global-color:' + hx('Ink Soft')
IVORY = 'global-color:' + hx('Ivory')
LINEN = 'global-color:' + hx('Linen')
WHITE = 'global-color:50ddadf6-aee0-46f7-9b1c-c4304f61a36b'
LINE_LIGHT = 'global-color:' + hx('Line Light')
LINE_DARK = 'global-color:' + hx('Line Dark')
OVERLAY = 'global-color:' + hx('Photo Overlay')
# Global fonts
F_HEAD = '48656164696e6773'
F_BODY = '426f647920436f7079'

PAD = 'clamp(88px, 11vw, 152px) 0px'
NOSHADOW = '!0em 0em 0em 0em'


def img(pid, size='full'):
    return f"{MEDIA[pid]['id']}:{size}"


def url(pid):
    return MEDIA[pid]['url']


def bp(**kw):
    """Responsive overrides: bp(key=[xs, sm, md]) -> _bp_data3_4 (base = lg, xl inherits)."""
    out = {}
    for k, v in kw.items():
        v = list(v) + [None] * (5 - len(v))
        out[k] = v[:5]
    return {'_bp_data3_4': out}


def el(t, mods=None, **kw):
    d = {'_type': t}
    d.update(kw)
    if mods is not None:
        d['_modules'] = mods
    return d


# ---------------------------------------------------------------- layout
def section(mods, bg=None, pad=PAD, image=None, overlay=OVERLAY, video=None, poster=None, label=None, **kw):
    d = dict(section_padding=pad, section_z_index='1')
    if bg:
        d['section_bg_color'] = bg
    if image or video:
        d.update(section_bg_advanced=True)
        if video:
            d.update(bg_lower_type='video', bg_lower_video=video, bg_lower_video_poster=poster or '',
                     bg_lower_video_object_fit='cover')
        else:
            d.update(bg_lower_type='image', bg_lower_image=image, bg_lower_image_size='cover',
                     bg_lower_image_position='center')
        if overlay:
            d.update(bg_upper_type='color', bg_upper_color=overlay)
    if label:
        d['title'] = label
    d.update(kw)
    return el('section', mods, **d)


def row(cols, layout='100%', xs=None, sm=None, md=None, gap='clamp(40px, 7vw, 96px)', rgap=None,
        align='stretch', **kw):
    d = dict(layout_row_global_container=True, layout_row_layout=layout,
             layout_row_gap_column=gap, layout_row_gap_row=rgap or gap, layout_row_flex_align=align)
    if xs or sm or md:
        d.update(bp(layout_row_layout=[xs, sm, md]))
    d.update(kw)
    return el('layout-row', cols, **d)


def col(mods, **kw):
    return el('layout-column', mods, **kw)


def div(mods, **kw):
    return el('layout-div', mods, **kw)


def hstack(mods, gap='14px', justify='flex-start', align='center', wrap=True, **kw):
    d = dict(layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_wrap=wrap,
             layout_div_flex_gap=gap, layout_div_flex_justify=justify, layout_div_flex_align=align)
    d.update(kw)
    return div(mods, **d)


def gap(size):
    return el('gap', gap_size=size)


# ---------------------------------------------------------------- typography
def eyebrow(text, dark=False, mb='22px', center=False):
    c = ACCENT_LIGHT if dark else ACCENT
    return hstack([
        el('line', line_width='32px', line_size='1px', line_color=c),
        el('headline', text_tag='span', text_content=text, text_font_family=F_BODY, text_font_weight='700',
           text_font_size='12px', text_letter_spacing='0.24em', text_text_transform='uppercase',
           text_line_height='1.4', text_text_color=c),
    ], justify='center' if center else 'flex-start', layout_div_margin=f'0px 0px {mb} 0px')


def heading(html, tag='h2', size='clamp(36px, 4.8vw, 60px)', color=ESP, mb='24px', lh='1.05', align=None,
            maxw=None, **kw):
    d = dict(text_tag=tag, text_content=html, text_font_family=F_HEAD, text_font_weight='500',
             text_font_size=size, text_line_height=lh, text_letter_spacing='-0.02em', text_text_color=color,
             text_margin=f'0px 0px {mb} 0px')
    if align:
        d['text_text_align'] = align
    if maxw:
        d['text_max_width'] = maxw
    if color == WHITE:
        d['class'] = 'lc-on-dark'
    d.update(kw)
    return el('headline', **d)


def h3(html, size='25px', color=ESP, mb='10px', lh='1.15', **kw):
    return heading(html, tag='h3', size=size, color=color, mb=mb, lh=lh, **kw)


def text(html, color=INK_SOFT, size='17px', lh='1.75', mb='20px', maxw=None, align=None, **kw):
    if not html.lstrip().startswith('<'):
        html = f'<p>{html}</p>'
    d = dict(text_content=html, text_font_family=F_BODY, text_font_weight='400', text_font_size=size,
             text_line_height=lh, text_text_color=color, text_margin=f'0px 0px {mb} 0px')
    if maxw:
        d['text_max_width'] = maxw
    if align:
        d['text_text_align'] = align
    d.update(kw)
    return el('text', **d)


def lead(html, color=ESP, **kw):
    kw.setdefault('maxw', '34em')
    return text(html, color=color, size='clamp(17px, 1.5vw, 19px)', **kw)


def label(txt, color=ACCENT, size='12px', ls='0.2em', mb='0px', **kw):
    return el('headline', text_tag='span', text_content=txt, text_font_family=F_BODY, text_font_weight='700',
              text_font_size=size, text_letter_spacing=ls, text_text_transform='uppercase', text_line_height='1.4',
              text_text_color=color, text_margin=f'0px 0px {mb} 0px', **kw)


# ---------------------------------------------------------------- buttons
BTN = {
    'primary': dict(bg=ACCENT, bg_alt=ACCENT_DARK, fg=WHITE, fg_alt=WHITE, border=None),
    'dark': dict(bg=ESP, bg_alt=ACCENT_DARK, fg=IVORY, fg_alt=IVORY, border=None),
    'ghost': dict(bg='transparent', bg_alt='rgba(255, 255, 255, 0.08)', fg=WHITE, fg_alt=WHITE,
                  border=('rgba(255, 255, 255, 0.45)', WHITE)),
    'white': dict(bg=WHITE, bg_alt=ESP, fg=ACCENT, fg_alt=WHITE, border=None),
}


def button(txt, href, variant='primary', arrow=True, small=False, blank=False, **kw):
    v = BTN[variant]
    d = dict(anchor_text_primary_content=txt, anchor_href=href, anchor_blank=blank,
             anchor_bg_color=v['bg'], anchor_bg_color_alt=v['bg_alt'],
             anchor_border_radius='999px', anchor_box_shadow_dimensions=NOSHADOW,
             anchor_padding='13px 22px' if small else '17px 30px', anchor_text_margin='0px',
             anchor_primary_font_family=F_BODY, anchor_primary_font_weight='600',
             anchor_primary_font_size='12px' if small else '13px', anchor_primary_letter_spacing='0.12em',
             anchor_primary_text_transform='uppercase', anchor_primary_line_height='1',
             anchor_primary_text_color=v['fg'], anchor_primary_text_color_alt=v['fg_alt'])
    if v['border']:
        d.update(anchor_border_width='1px', anchor_border_style='solid',
                 anchor_border_color=v['border'][0], anchor_border_color_alt=v['border'][1])
    if arrow:
        d.update(anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon='arrow-right',
                 anchor_graphic_icon_alt='arrow-right', anchor_graphic_margin='0px 0px 0px 12px',
                 anchor_graphic_icon_font_size='14px', anchor_graphic_icon_color=v['fg'],
                 anchor_graphic_icon_color_alt=v['fg_alt'], anchor_flex_direction='row-reverse',
                 anchor_graphic_interaction='x-anchor-scale-up')
    d.update(kw)
    return el('button', **d)


def buttons(*btns, mt='0px'):
    return hstack(list(btns), layout_div_margin=f'{mt} 0px 0px 0px')


# ---------------------------------------------------------------- media
def framed_image(pid, alt='', ratio='4/5', offset='22px', color=ACCENT, reverse=False, mr=True):
    """Image with the offset outline frame (two native Divs + Image)."""
    o = offset
    left, right = ('-' + o, o) if reverse else (o, '-' + o)
    frame = div([], layout_div_position='absolute', layout_div_top=o, layout_div_bottom='-' + o,
                layout_div_left=left, layout_div_right=right, layout_div_z_index='-1',
                layout_div_border_width='1px', layout_div_border_color=color, layout_div_border_radius='4px')
    im = el('image', image_src=img(pid), image_alt=alt, image_display='block', image_styled_width='100%',
            image_object_fit='cover', image_aspect_ratio_value=ratio, image_outer_border_radius='4px',
            image_inner_border_radius='4px')
    m = f'0px 0px {o} 0px' if not reverse else f'0px 0px {o} {o}'
    w = f'calc(100% - {o})'
    return div([frame, im], layout_div_position='relative', layout_div_z_index='1', layout_div_width='100%',
               **bp(layout_div_margin=[m, m, m], layout_div_width=[w, w, w]))


# ---------------------------------------------------------------- shared blocks
def page_hero(eyebrow_txt, title_html, lead_html, pid, extra=None, badge=False):
    mods = []
    if badge:
        mods.append(hstack([
            el('icon', icon='circle', icon_font_size='9px', icon_color=ACCENT_LIGHT, icon_width='9px',
               icon_height='9px', icon_border_radius='50%', icon_box_shadow_dimensions='0px 0px 0px 5px',
               icon_box_shadow_color='rgba(232, 93, 108, 0.25)'),
            label(eyebrow_txt, color=WHITE)], gap='10px', layout_div_margin='0px 0px 22px 0px'))
    else:
        mods.append(eyebrow(eyebrow_txt, dark=True))
    mods.append(heading(title_html, tag='h1', size='clamp(46px, 7.6vw, 96px)', color=WHITE, mb='22px',
                        maxw='820px'))
    mods.append(lead(lead_html, color='rgba(255, 255, 255, 0.82)', mb='0px', maxw='500px'))
    mods += extra or []
    for i, m in enumerate(mods):
        rise(m, i)
    return section([row([col(mods)])], image=url(pid), overlay=OVERLAY,
                   pad='clamp(190px, 18vw, 260px) 0px clamp(64px, 8vw, 104px) 0px', label='Page Header')


def rise(e, i):
    """Native entrance animation, staggered."""
    e.update(effects_scroll=True, effects_type_scroll='animation', effects_animation_enter='fadeInUp',
             effects_duration_scroll='900ms', effects_delay_scroll=f'{i * 80}ms',
             effects_offset_top='0%', effects_offset_bottom='0%')
    return e


def info_item(dt, dd_html, dark=True):
    """Definition row = Headline with reversed subheadline (dt above dd)."""
    return el('headline', text_tag='div', text_content=dd_html, text_font_family=F_BODY, text_font_size='16px',
              text_font_weight='400', text_line_height='1.6', text_text_color=WHITE if dark else ESP,
              text_subheadline=True, text_subheadline_reverse=True, text_subheadline_content=dt,
              text_subheadline_tag='span', text_subheadline_spacing='4px', text_subheadline_font_family=F_BODY,
              text_subheadline_font_weight='700', text_subheadline_font_size='11px',
              text_subheadline_letter_spacing='0.2em', text_subheadline_text_transform='uppercase',
              text_subheadline_text_color='rgba(255, 255, 255, 0.5)' if dark else INK_SOFT,
              text_padding='14px 0px 14px 0px', text_border_width='1px 0px 0px 0px', text_border_style='solid',
              text_border_color=LINE_DARK if dark else LINE_LIGHT, text_width='100%',
              css='$el a { color: inherit; } $el a:hover { color: #E85D6C; }')


def info_heading(txt, icon):
    return el('headline', text_tag='h3', text_content=txt, text_font_family=F_HEAD, text_font_weight='500',
              text_font_size='22px', text_line_height='1.15', text_text_color=WHITE,
              text_margin='0px 0px 12px 0px', text_graphic=True, text_graphic_type='icon',
              text_graphic_icon=icon, text_graphic_icon_alt=icon, text_graphic_margin='0px 14px 0px 0px',
              text_graphic_icon_font_size='16px', text_graphic_icon_width='38px', text_graphic_icon_height='38px',
              text_graphic_icon_color=WHITE, text_graphic_icon_color_alt=WHITE,
              text_graphic_icon_bg_color=ACCENT, text_graphic_icon_border_radius='50%', text_flex_justify='flex-start')


def touch_section():
    left = col([
        eyebrow('Get in touch', dark=True),
        heading("We'd love to <em>meet you.</em>", color=WHITE),
        lead('Join us at a service this week, or reach out with any question. A real person will get back to you.',
             color='rgba(255, 255, 255, 0.72)', mb='48px', maxw='440px'),
        el('layout-row', [
            col([info_heading('Service Times', 'clock'), info_item('Sunday Mornings', '8:30 am &amp; 10:00 am'),
                 info_item('Wednesday Evenings', '6:30 pm')], layout_column_flex_align='stretch'),
            col([info_heading('Contact', 'location-dot'),
                 info_item('Address', '2200 Street, My Town, XX 12345'),
                 info_item('Phone / Email', '<a href="tel:1111234567">111-123-4567</a><br><a href="mailto:info@yourdomain.org">info@yourdomain.org</a>')],
                layout_column_flex_align='stretch'),
        ], layout_row_layout='50% 50%', layout_row_gap_column='36px', layout_row_gap_row='36px',
            layout_row_margin='0px 0px 48px 0px', **bp(layout_row_layout=['100%'])),
        buttons(button('Plan Your Visit', '/plan-your-visit/'),
                button('Get Directions', 'https://maps.google.com/?q=Franklin,TN', 'ghost', arrow=False, blank=True)),
    ])
    right = col([
        div([el('map', map_type='embed', frame_content_sizing='fixed-height', frame_content_height='500px',
                **bp(frame_content_height=['340px', '340px', '340px']),
                frame_bg_color=ESP2, frame_border_radius='4px',
                map_embed_code='<iframe title="Map to Lewis Church" loading="lazy" src="https://maps.google.com/maps?q=Franklin%2C%20TN&amp;z=15&amp;output=embed" style="border:0" allowfullscreen></iframe>',
                )],
            layout_div_width='100%',
            layout_div_border_width='1px', layout_div_border_color='rgba(255, 255, 255, 0.22)',
            layout_div_border_radius='4px', layout_div_padding='10px', layout_div_flexbox=True,
            layout_div_flex_direction='column', layout_div_flex_align='stretch',
            effects_filter='grayscale(1) sepia(0.25) contrast(1.05)', **{'class': 'lc-map'}),
    ], layout_column_flexbox=True, layout_column_flex_align='stretch')
    return section([row([left, right], '50% 50%', md='100%', sm='100%', xs='100%')],
                   image=url('photo-1470252649378-9c29740c9fa8'), overlay='rgba(20, 16, 12, 0.72)',
                   label='Get In Touch')


def split(image_pid, alt, content, reverse=False, bg=None, ratio='5/4', dark=False):
    imgcol = col([framed_image(image_pid, alt, ratio=ratio, offset='18px', reverse=reverse,
                               color=ACCENT_LIGHT if dark else ACCENT)])
    txt = col(content, layout_column_flexbox=True, layout_column_flex_direction='column',
              layout_column_flex_justify='center')
    cols = [imgcol, txt]
    r = row(cols, '50% 50%', md='100%', sm='100%', xs='100%', gap='clamp(48px, 8vw, 112px)', align='center',
            layout_row_reverse=reverse, **({}))
    if reverse:
        # reverse visually on desktop only (image right); stacked: image first
        r.update(bp(layout_row_layout=['100%', '100%', '100%'], layout_row_reverse=[False, False, False]))
    return section([r], bg=bg)


def section_head(eyebrow_txt, title_html, aside=None, dark=False, center=False, mb='56px'):
    left = [eyebrow(eyebrow_txt, dark=dark, center=center),
            heading(title_html, color=WHITE if dark else ESP, mb='0px', align='center' if center else None)]
    if center:
        mods = left + ([text(aside, mb='0px', maxw='560px', align='center')] if aside else [])
        return div(mods, layout_div_flexbox=True, layout_div_flex_direction='column', layout_div_flex_align='center',
                   layout_div_width='100%', layout_div_margin=f'0px 0px {mb} 0px')
    mods = [div(left)]
    if aside:
        mods.append(text(aside, mb='0px', maxw='360px',
                         color='rgba(255, 255, 255, 0.72)' if dark else INK_SOFT))
    return hstack(mods, gap='24px 48px', justify='space-between', align='flex-end', layout_div_width='100%',
                  layout_div_margin=f'0px 0px {mb} 0px')


# Gravity Forms "Orbital" theme + its own Form Style settings (passed on the shortcode), tuned to the palette.
GF_STYLES = {"theme": "orbital", "inputSize": "lg", "inputBorderRadius": 4, "inputBorderColor": "#4A433E",
             "inputBackgroundColor": "#2E2925", "inputColor": "#FFFFFF", "inputPrimaryColor": "#E85D6C",
             "labelFontSize": 11, "labelColor": "#A9A39E", "descriptionColor": "#8E8781",
             "buttonPrimaryBackgroundColor": "#A51C30", "buttonPrimaryColor": "#FFFFFF"}


def gf_shortcode(form_id):
    return ('[gravityform id="%s" title="false" description="false" ajax="true" theme="orbital" styles=\'%s\']'
            % (form_id, json.dumps(GF_STYLES, separators=(',', ':'))))


def form_panel(form_id):
    return div([el('raw-content', raw_content=gf_shortcode(form_id))],
               **{'class': 'lc-form'}, layout_div_width='100%', layout_div_padding='clamp(28px, 4vw, 44px)',
               layout_div_bg_color='rgba(31, 27, 23, 0.7)', layout_div_border_width='1px',
               layout_div_border_color=LINE_DARK, layout_div_border_radius='4px',
               effects_backdrop_filter='blur(8px)')


def form_section(eyebrow_txt, title_html, lead_html, form_id, pid):
    left = col([eyebrow(eyebrow_txt, dark=True), heading(title_html, color=WHITE),
                lead(lead_html, color='rgba(255, 255, 255, 0.72)', mb='0px')])
    return section([row([left, col([form_panel(form_id)])], '45% 55%', md='100%', sm='100%', xs='100%',
                        align='flex-start')], image=url(pid), overlay='rgba(20, 16, 12, 0.72)', label='Form')
