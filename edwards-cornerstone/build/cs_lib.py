"""Element builders for the Edwards Cornerstone build.
Native Cornerstone elements only; colours/fonts always reference the Cornerstone globals.
Breakpoints on this site: 5 (_bp_base "4_4"): xs<479, sm 479-766, md 767-978, lg 979-1198, xl base."""

FONT = 'edwards-sans'
def G(name, a=None):
    ids = {'white': 'e013c488-df27-4ba3-8b8a-b36f9d2a99ba', 'black': '391ca029-2e47-46af-a733-909ca2f1d996'}
    gid = ids.get(name, 'edwards-' + name)
    return f'global-color:{gid}' + (f':{a}' if a is not None else '')

def el(_type, title=None, children=None, bp=None, **props):
    e = {'_type': _type, '_bp_base': '4_4'}
    if title: e['title'] = title
    e.update(props)
    if bp:
        # site uses 5 breakpoints: [xs <479, sm 479-766, md 767-978, lg 979-1198, xl base]
        # 2-tuple (phone, tablet) -> phone on xs+sm, tablet on md+lg; 4-tuple given explicitly
        def expand(v):
            v = list(v)
            return v + [None] if len(v) == 4 else [v[0], v[0], v[1], v[1], None]
        e['_bp_data4_4'] = {k: expand(v) for k, v in bp.items()}
    e['_modules'] = children or []
    return e

def provider():
    """Native: hovering this element drives its children's hover colours / particles / effects."""
    return dict(effects_provider=True, effects_provider_targets='colors particles effects')

def reveal(delay=0, zoom=False):
    """Native Cornerstone scroll effect: fade up once."""
    return dict(effects_scroll=True, effects_type_scroll='transform', effects_opacity_exit='0', effects_opacity_enter='1',
                effects_transform_exit=('scale(1.06)' if zoom else 'translate(0px, 1.5rem)'), effects_transform_enter='translate(0px, 0px)',
                effects_duration_scroll='900ms', effects_delay_scroll=f'{delay}ms', effects_behavior_scroll='fire-once')

# ---------- layout ----------
def section(title, children, padding='130px 0px 130px 0px', bg=None, bp=None, **props):
    p = dict(section_padding=padding, section_bg_color=bg or 'transparent')
    p.update(props)
    b = {'section_padding': ['80px 0px 80px 0px', '100px 0px 100px 0px']}
    if bp: b.update(bp)
    return el('section', title, children, bp=b, **p)

def row(title, children, layout='100%', gap='20px', layout_phone='100%', layout_tablet='100%', container=True, bp=None, **props):
    p = dict(layout_row_global_container=container, layout_row_layout=layout, layout_row_gap_column=gap, layout_row_gap_row=gap)
    p.update(props)
    b = {'layout_row_layout': [layout_phone, layout_tablet]}
    if bp: b.update(bp)
    return el('layout-row', title, children, bp=b, **p)

def col(title, children, align='flex-start', justify='flex-start', gap='0px', bp=None, **props):
    p = dict(layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_wrap=False,
             layout_column_flex_align=align, layout_column_flex_justify=justify, layout_column_flex_gap=gap)
    p.update(props)
    return el('layout-column', title, children, bp=bp, **p)

def div(title, children, direction='column', gap='0px', align='flex-start', justify='flex-start', wrap=False, bp=None, **props):
    p = dict(layout_div_flexbox=True, layout_div_flex_direction=direction, layout_div_flex_gap=gap,
             layout_div_flex_align=align, layout_div_flex_justify=justify, layout_div_flex_wrap=wrap)
    p.update(props)
    return el('layout-div', title, children, bp=bp, **p)

# ---------- content ----------
def headline(title, content, tag='h2', size='3.2em', color='slate', weight='700', lh='1.1', ls='-0.022em',
             align='none', transform='none', bp=None, **props):
    p = dict(text_content=content, text_tag=tag, text_font_family=FONT, text_font_weight=weight, text_font_size=size,
             text_line_height=lh, text_letter_spacing=ls, text_text_color=G(color) if not color.startswith(('global', 'rgb', '#')) else color,
             text_text_align=align, text_text_transform=transform)
    p.update(props)
    return el('headline', title, bp=bp, **p)

def label(title, content, color='accent', size='0.72em', align='none', ls='0.24em', transform='uppercase', **props):
    """Small uppercase label (eyebrow text, card labels)."""
    return headline(title, content, tag='span', size=size, color=color, weight='700', lh='1.4', ls=ls,
                    align=align, transform=transform, **props)

def eyebrow(content, color='accent', center=False, **props):
    line = lambda t: el('line', t, line_width='2.75em', line_size='1px', line_color=G(color) if color != 'white' else G('white'))
    kids = [line('Line'), label('Eyebrow Text', content, color=color)]
    if center: kids.append(line('Line Right'))
    return div('Eyebrow', kids, direction='row', gap='1em', align='center', justify='center' if center else 'flex-start', **props)

def text(title, html, color='text-soft', size='1em', align='none', max_width='none', **props):
    p = dict(text_content=html, text_font_family=FONT, text_font_size=size, text_line_height='1.75',
             text_text_color=G(color), text_text_align=align, text_max_width=max_width)
    p.update(props)
    return el('text', title, **p)

BTN_BASE = dict(anchor_primary_font_family=FONT, anchor_primary_font_weight='600', anchor_primary_font_size='0.8em',
                anchor_primary_letter_spacing='0.16em', anchor_primary_text_transform='uppercase', anchor_primary_line_height='1',
                anchor_padding='1.15em 1.9em 1.15em 1.9em', anchor_border_radius='8px', anchor_border_width='1px', anchor_border_style='solid',
                anchor_box_shadow_dimensions='!0em 0em 0em 0em', anchor_text_margin='0px',
                # hover: accent fill sweeps in from the left (native particle)
                anchor_primary_particle=True, anchor_primary_particle_location='c_c', anchor_primary_particle_placement='inside',
                anchor_primary_particle_scale='scale-x', anchor_primary_particle_transform_origin='0% 50%',
                anchor_primary_particle_width='100%', anchor_primary_particle_height='100%', anchor_primary_particle_delay='0ms',
                anchor_primary_particle_border_radius='0px', effects_duration='450ms',
                anchor_graphic=False)
ARROW = dict(anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon='arrow-right', anchor_graphic_icon_alt='arrow-right',
             anchor_graphic_icon_font_size='1em', anchor_graphic_margin='0em 0em 0em 0.75em', anchor_flex_direction='row-reverse',
             anchor_graphic_has_interactions=True, anchor_graphic_interaction='x-anchor-slide-right')
BTN = {
 'primary': dict(anchor_bg_color=G('slate'), anchor_bg_color_alt=G('slate'), anchor_border_color=G('slate'), anchor_border_color_alt=G('accent'),
                 anchor_primary_text_color=G('white'), anchor_primary_text_color_alt=G('white'), anchor_primary_particle_color=G('accent'),
                 anchor_graphic_icon_color=G('white'), anchor_graphic_icon_color_alt=G('white')),
 'light':   dict(anchor_bg_color=G('white'), anchor_bg_color_alt=G('white'), anchor_border_color=G('white'), anchor_border_color_alt=G('accent'),
                 anchor_primary_text_color=G('slate-deep'), anchor_primary_text_color_alt=G('white'), anchor_primary_particle_color=G('accent'),
                 anchor_graphic_icon_color=G('slate-deep'), anchor_graphic_icon_color_alt=G('white')),
 'ghost':   dict(anchor_bg_color='transparent', anchor_bg_color_alt='transparent', anchor_border_color=G('white', 0.55), anchor_border_color_alt=G('white'),
                 anchor_primary_text_color=G('white'), anchor_primary_text_color_alt=G('slate-deep'), anchor_primary_particle_color=G('white'),
                 anchor_graphic_icon_color=G('white'), anchor_graphic_icon_color_alt=G('slate-deep')),
 'outline': dict(anchor_bg_color='transparent', anchor_bg_color_alt='transparent', anchor_border_color=G('slate'), anchor_border_color_alt=G('slate'),
                 anchor_primary_text_color=G('slate'), anchor_primary_text_color_alt=G('white'), anchor_primary_particle_color=G('slate'),
                 anchor_graphic_icon_color=G('slate'), anchor_graphic_icon_color_alt=G('white')),
}
def button(title, label_, href, style='primary', blank=False, arrow=False, **props):
    p = dict(BTN_BASE); p.update(BTN[style])
    if arrow: p.update(ARROW)
    p.update(anchor_text_primary_content=label_, anchor_href=href, anchor_blank=blank)
    p.update(props)
    return el('button', title, **p)

def image(title, media, alt='', ratio='auto', radius='12px', fill=False, link=None, **props):
    p = dict(image_type='standard', image_src=f"{media['id']}:full", image_alt=alt, image_retina=False,
             image_display='block', image_styled_width='100%', image_outer_border_radius=radius, image_inner_border_radius=radius,
             image_object_fit='cover', image_object_position='50% 50%', image_aspect_ratio_value=ratio)
    if fill: p.update(image_styled_height='100%')
    if link: p.update(image_link=True, image_href=link)
    p.update(props)
    return el('image', title, **p)

def icon(title, name, color='accent', size='1.25em', bg='transparent', box=None, **props):
    p = dict(icon=name, icon_color=G(color), icon_font_size=size, icon_bg_color=bg if bg == 'transparent' else G(bg))
    if box: p.update(icon_width=box, icon_height=box, icon_border_radius='50%')
    p.update(props)
    return el('icon', title, **p)
