import json, re
M = json.load(open('graham-media.json'))
def img(k): return f"{M[k]['id']}:full"
G = lambda t: 'global-color:' + t.encode().hex()
NAVY, DEEP, DARK, SLATE = G('Graham Navy'), G('Graham Navy Deep'), G('Graham Navy Darkest'), G('Graham Slate')
GOLD, GOLDD, GOLDS = G('Graham Gold'), G('Graham Gold Deep'), G('Graham Gold Soft')
IVORY, PAPER, SAND, INK, MUTED = G('Graham Ivory'), G('Graham Paper'), G('Graham Sand'), G('Graham Ink'), G('Graham Muted')
F_DISP, F_ACC, F_BODY = 'Graham Display'.encode().hex(), 'Graham Accent'.encode().hex(), 'Graham Body'.encode().hex()
BP = '3_4'
def bp(**kw):  # responsive overrides: value list [xs, sm, md, lg, xl]
    return {'_bp_data3_4': kw}

def el(t, title=None, mods=None, **kw):
    e = {'_type': t, '_bp_base': BP}
    if title: e['title'] = title
    e.update(kw)
    if mods is not None: e['_modules'] = mods
    return e

def section(title, mods, **kw):
    d = dict(section_base_font_size='1em', section_margin='0px', section_padding='8.5rem 0px 8.5rem 0px',
             section_z_index='1', **{'class': 'gc-section'},
             **bp(section_padding=['5.5rem 0px 5.5rem 0px', None, '6.5rem 0px 6.5rem 0px', None, None]))
    d.update(kw)
    return el('section', title, mods, **d)

def row(title, cols, layout='100%', gap='0px', align='stretch', stack=True, **kw):
    d = dict(layout_row_global_container=True, layout_row_layout=layout, layout_row_gap_column=gap,
             layout_row_gap_row='2.5rem', layout_row_flex_align=align, layout_row_padding='0px')
    if stack and layout != '100%':
        d.update(bp(layout_row_layout=['100%', '100%', '100%', None, None]))
    d.update(kw)
    if layout != '100%':
        bpd = d.setdefault('_bp_data3_4', {})
        g = list(bpd.get('layout_row_gap_column', [None] * 5))
        g[0] = '0px'; g[1] = '0px'
        bpd['layout_row_gap_column'] = g
    return el('layout-row', title, cols, **d)

def col(title, mods, **kw):
    d = dict(layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_align='flex-start',
             layout_column_flex_justify='flex-start', layout_column_flex_wrap=False)
    d.update(kw)
    return el('layout-column', title, mods, **d)

def div(title, mods, direction='column', gap='0px', align='flex-start', justify='flex-start', wrap=False, **kw):
    d = dict(layout_div_flexbox=True, layout_div_flex_direction=direction, layout_div_flex_gap=gap,
             layout_div_flex_align=align, layout_div_flex_justify=justify, layout_div_flex_wrap=wrap)
    d.update(kw)
    return el('layout-div', title, mods, **d)

def headline(text, tag='h2', size='clamp(2.4rem, 5vw, 4rem)', color=INK, font=F_DISP, weight='500',
             ls='-0.04em', lh='1.04', margin='0px', **kw):
    d = dict(text_type='standard', text_content=text, text_tag=tag, text_font_family=font, text_font_weight=weight,
             text_font_size=size, text_letter_spacing=ls, text_line_height=lh, text_text_color=color,
             text_margin=margin, text_padding='0px', text_text_align='left', text_overflow=False)
    if tag in ('h1', 'h2', 'h3'): d['text_width'] = '100%'
    d.update(kw)
    return el('headline', None, [], **d)

def label_head(primary, sub, pcolor='#ffffff', scolor=GOLD, psize='0.95rem', tag='p', link=None, **kw):
    """Small label above a value: Headline with a reversed subheadline."""
    d = dict(text_subheadline=True, text_subheadline_content=sub, text_subheadline_tag='span',
             text_subheadline_reverse=True, text_subheadline_spacing='0.55em',
             text_subheadline_font_family=F_BODY, text_subheadline_font_weight='700',
             text_subheadline_font_size='0.66rem', text_subheadline_letter_spacing='0.22em',
             text_subheadline_line_height='1.2', text_subheadline_text_transform='uppercase',
             text_subheadline_text_color=scolor)
    if link: d.update(text_link=True, text_href=link)
    d.update(kw)
    return headline(primary, tag=tag, size=psize, color=pcolor, font=F_BODY, weight='500', ls='0em', lh='1.45', **d)

def eyebrow(text, color=GOLDD):
    return div('Eyebrow', [
        el('line', None, [], line_width='32px', line_size='1px', line_color=color, line_margin='0px'),
        headline(text, tag='span', size='0.7rem', color=color, font=F_BODY, weight='700', ls='0.24em', lh='1.2',
                 text_text_transform='uppercase'),
    ], direction='row', gap='14px', align='center')

def text(html, color=MUTED, size='1rem', lh='1.85', maxw='38rem', font=F_BODY, **kw):
    d = dict(text_type='standard', text_content=html, text_font_family=font, text_font_weight='400',
             text_font_size=size, text_line_height=lh, text_text_color=color, text_max_width=maxw,
             text_margin='0px', text_padding='0px', text_text_align='left')
    d.update(kw)
    return el('text', None, [], **d)

def button(label, href, style='gold'):
    s = {
      'gold':    (GOLD, '#ffffff', GOLD, '#ffffff', DARK, DARK, '0em 0.6em 1.6em -0.6em', 'rgba(198,173,122,0.6)'),
      'ghost':   ('transparent', '#ffffff', 'rgba(255,255,255,0.45)', '#ffffff', '#ffffff', DEEP, '0em 0em 0em 0em', 'transparent'),
      'navy':    (NAVY, GOLD, NAVY, GOLD, '#ffffff', DARK, '0em 0.75em 1.75em -0.75em', 'rgba(15,24,40,0.55)'),
      'outline': ('transparent', NAVY, NAVY, NAVY, NAVY, '#ffffff', '0em 0em 0em 0em', 'transparent'),
    }[style]
    bg, bga, bc, bca, tc, tca, sh, shc = s
    return el('button', None, [], anchor_type='button', anchor_has_link_control=True, anchor_href=href,
              anchor_text=True, anchor_text_primary_content=label, anchor_base_font_size='1em',
              anchor_bg_color=bg, anchor_bg_color_alt=bga, anchor_border_width='1px', anchor_border_style='solid',
              anchor_border_color=bc, anchor_border_color_alt=bca, anchor_border_radius='0px',
              anchor_padding='1.3em 1.9em 1.3em 1.9em', anchor_margin='0px', anchor_text_margin='0px',
              anchor_box_shadow_dimensions=sh, anchor_box_shadow_color=shc, anchor_box_shadow_color_alt=shc,
              anchor_primary_font_family=F_BODY, anchor_primary_font_weight='700', anchor_primary_font_size='0.75rem',
              anchor_primary_letter_spacing='0.12em', anchor_primary_line_height='1', anchor_primary_text_transform='uppercase',
              anchor_primary_text_color=tc, anchor_primary_text_color_alt=tca, anchor_primary_text_align='center',
              anchor_flex_direction='row', anchor_flex_justify='center', anchor_flex_align='center',
              effects_duration='350ms')

def text_link(label, href, color=NAVY, hover=GOLDD, line=GOLD):
    return el('button', None, [], anchor_type='button', anchor_has_link_control=True, anchor_href=href,
              anchor_text=True, anchor_text_primary_content=label, anchor_base_font_size='1em',
              anchor_bg_color='transparent', anchor_bg_color_alt='transparent',
              anchor_border_width='0px 0px 1px 0px', anchor_border_style='solid', anchor_border_color=line,
              anchor_border_color_alt=line, anchor_border_radius='0px', anchor_padding='0em 0em 0.75em 0em',
              anchor_margin='0px', anchor_text_margin='0px', anchor_box_shadow_dimensions='0em 0em 0em 0em',
              anchor_primary_font_family=F_BODY, anchor_primary_font_weight='700', anchor_primary_font_size='0.7rem',
              anchor_primary_letter_spacing='0.16em', anchor_primary_line_height='1', anchor_primary_text_transform='uppercase',
              anchor_primary_text_color=color, anchor_primary_text_color_alt=hover)

def bgimg(prefix, image, overlay):
    return {f'{prefix}_bg_advanced': True, 'bg_border_radius': 'inherit',
            'bg_lower_type': 'image', 'bg_lower_image': image, 'bg_lower_image_size': 'cover',
            'bg_lower_image_position': 'center', 'bg_lower_image_repeat': 'no-repeat',
            'bg_upper_type': 'color', 'bg_upper_color': overlay}

hover_lift = dict(effects_alt=True, effects_transform_alt='translate(0px, -6px)', effects_duration='450ms',
                  effects_timing_function='cubic-bezier(0.2, 0.7, 0.2, 1)')

# ---------------- 1. HERO ----------------
hero = section('1. Hero (video)', [
  row('Content', [col('Text', [
    eyebrow('A community centered on Christ', GOLD),
    headline('A Church For the City.', tag='h1', size='clamp(3.4rem, 8.4vw, 7.25rem)', color='#ffffff',
             ls='-0.05em', lh='0.95', margin='1.75rem 0rem 1.6rem 0rem'),
    text("<p>A place to belong, grow in faith, and discover the hope of Jesus. There's a place for you here.</p>",
         color='rgba(255,255,255,0.82)', size='1.05rem', lh='1.8', maxw='30rem'),
    div('Service Times', [
      div('Sunday', [label_head('Sunday Morning · 10 AM', 'Sunday Service')], layout_div_padding='0px 2rem 0px 0px'),
      div('Midweek', [label_head('Wednesday · 6 PM', 'Midweek Gathering')],
          layout_div_padding='0px 2rem 0px 2rem', layout_div_border_width='0px 0px 0px 1px',
          layout_div_border_style='solid', layout_div_border_color='rgba(198,173,122,0.4)',
          **bp(layout_div_padding=['0px', '0px', None, None, None], layout_div_border_width=['0px', '0px', None, None, None])),
      div('Address', [label_head('1000 West Highway, City, ST 55555 ↗', 'Visit Us', link='#visit')],
          layout_div_padding='0px 0px 0px 2rem', layout_div_border_width='0px 0px 0px 1px',
          layout_div_border_style='solid', layout_div_border_color='rgba(198,173,122,0.4)',
          **bp(layout_div_padding=['0px', '0px', None, None, None], layout_div_border_width=['0px', '0px', None, None, None])),
    ], direction='row', gap='1.1rem', wrap=True, layout_div_margin='2.2rem 0px 2.4rem 0px',
       **bp(layout_div_flex_direction=['column', 'column', None, None, None])),
    div('Buttons', [button('Plan Your Visit  ↗', '/plan-your-visit/', 'gold'),
                    button('Get to Know Us  →', '/about/', 'ghost')], direction='row', gap='14px', wrap=True),
  ])]),
], section_padding='12rem 0px 9rem 0px', **{'_bp_data3_4': {'section_padding': ['8rem 0px 6rem 0px', None, '10rem 0px 7rem 0px', None, '13rem 0px 10rem 0px']}},
   section_bg_advanced=True, bg_border_radius='inherit', bg_lower_type='video',
   bg_lower_video=M['herovideo']['url'], bg_lower_video_poster=img('heroposter'),
   bg_upper_type='color', bg_upper_color='rgba(15, 24, 40, 0.72)', section_bg_color=DEEP)

# ---------------- 2. WELCOME ----------------
welcome = section('2. Welcome', [
  row('Content', [
    col('Image', [
      div('Image Frame', [
        headline('01 / A place to begin', tag='span', size='0.65rem', color='#ffffff', font=F_BODY, weight='700',
                 ls='0.22em', lh='1.2', text_text_transform='uppercase'),
      ], justify='flex-start', layout_div_width='100%', layout_div_min_height='36rem',
         layout_div_padding='1.6rem 1.6rem 1.6rem 1.6rem',
         layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.35)',
         **bgimg('layout_div', img('bible'), 'rgba(15, 24, 40, 0.12)'),
         **bp(layout_div_min_height=['24rem', '28rem', None, None, None])),
      div('Quote Card', [
        headline('Shining the light of Christ to all those we encounter.', tag='p', size='1.45rem', color='#ffffff',
                 font=F_ACC, weight='400', ls='0em', lh='1.3', text_font_style='italic',
                 text_subheadline=True, text_subheadline_content='Our heart', text_subheadline_tag='span',
                 text_subheadline_spacing='1em', text_subheadline_font_family=F_BODY, text_subheadline_font_weight='700',
                 text_subheadline_font_size='0.65rem', text_subheadline_letter_spacing='0.2em',
                 text_subheadline_text_transform='uppercase', text_subheadline_text_color=GOLD),
      ], layout_div_bg_color=DEEP, layout_div_max_width='19rem', layout_div_padding='1.9rem 1.9rem 1.75rem 1.9rem',
         layout_div_margin='-7rem -2rem 0px auto', layout_div_border_width='2px 0px 0px 0px',
         layout_div_border_style='solid', layout_div_border_color=GOLD, layout_div_z_index='2',
         layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.35)',
         **bp(layout_div_margin=['-3rem 1rem 0px 1rem', '-4rem 1.5rem 0px auto', None, None, None])),
    ]),
    col('Text', [
      eyebrow('Welcome'),
      headline("We're glad you're here.", margin='1.4rem 0px 1.75rem 0px'),
      text('<p>We are a congregation of believers committed to sharing the message of Christ and guiding others towards faith in Him.</p>',
           color=INK, size='1.15rem', lh='1.75'),
      text('<p>As a church, we aim to love those in our community with the same love Christ has given to us. The work of our church is aimed at directing others towards the Savior in the hopes that they will encounter the one true God and be transformed by His gracious love for them. Through all we do, say, and preach, we pray that we will shine the light of Christ to all those we encounter.</p>',
           layout_margin=None, text_margin='1.1rem 0px 0px 0px'),
      div('Pillars', [
        div(f'Pillar – {name}', [label_head(name, num, pcolor=NAVY, scolor=GOLDD, psize='1rem', text_font_family=F_DISP,
                                            text_font_weight='700', text_subheadline_font_family=F_ACC,
                                            text_subheadline_font_style='italic', text_subheadline_font_size='0.95rem',
                                            text_subheadline_letter_spacing='0em', text_subheadline_text_transform='none',
                                            text_subheadline_font_weight='400')],
            layout_div_flex='1 1 0%', layout_div_padding=pad, layout_div_border_width=bw,
            layout_div_border_style='solid', layout_div_border_color='rgba(36,52,77,0.14)',
            **bp(layout_div_padding=['1rem 0px 1rem 0px', None, None, None, None],
                 layout_div_border_width=[bwx, None, None, None, None]))
        for name, num, pad, bw, bwx in [
          ('Belong', 'i.', '1.4rem 1rem 1.4rem 0px', '0px', '0px'),
          ('Grow in Faith', 'ii.', '1.4rem 1rem 1.4rem 1.25rem', '0px 0px 0px 1px', '1px 0px 0px 0px'),
          ('Discover Hope', 'iii.', '1.4rem 1rem 1.4rem 1.25rem', '0px 0px 0px 1px', '1px 0px 0px 0px')]
      ], direction='row', layout_div_width='100%', layout_div_margin='2.4rem 0px 2.5rem 0px',
         layout_div_border_width='1px 0px 1px 0px', layout_div_border_style='solid',
         layout_div_border_color='rgba(36,52,77,0.14)',
         **bp(layout_div_flex_direction=['column', None, None, None, None])),
      text_link('About Us  →', '/about/'),
    ]),
  ], layout='45% 55%', gap='6rem', align='center', **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None], 'layout_row_gap_column': [None, None, '3rem', '4rem', None]}}),
], section_bg_color=IVORY)

# ---------------- 3. CONNECT ----------------
def card(label, title, body, link_label, href, image, pos='center'):
    c = col(f'Card – {title}', [
      headline(label, tag='span', size='0.66rem', color=GOLD, font=F_BODY, weight='700', ls='0.22em', lh='1.2',
               text_text_transform='uppercase'),
      headline(title, tag='h3', size='clamp(1.9rem, 3.2vw, 2.75rem)', color='#ffffff', ls='-0.04em', lh='1.05',
               margin='0.75rem 0px 0.75rem 0px'),
      text(f'<p>{body}</p>', color='rgba(255,255,255,0.8)', size='0.92rem', lh='1.8', maxw='28rem',
           text_margin='0px 0px 1.5rem 0px'),
      text_link(link_label, href, color='#ffffff', hover=GOLDS, line=GOLD),
    ], layout_column_flex_justify='flex-end', layout_column_min_height='31rem',
       layout_column_padding='2.5rem 2.5rem 2.4rem 2.5rem',
       layout_column_box_shadow_dimensions='0em 2.5em 5em -1.9em', layout_column_box_shadow_color='rgba(0,0,0,0.6)',
       **bgimg('layout_column', image, 'rgba(15, 24, 40, 0.58)'),
       **bp(layout_column_min_height=['25rem', None, None, None, None], layout_column_padding=['1.75rem 1.6rem 1.75rem 1.6rem', None, None, None, None]))
    c['bg_lower_image_position'] = pos
    return c

connect = section('3. Connect', [
  row('Heading', [
    col('Heading Group', [eyebrow('Find your people', GOLD),
                          headline('Faith grows better together.', color='#ffffff', margin='1.4rem 0px 0px 0px')]),
    col('Intro', [text('<p>We offer several opportunities for you and your family to get involved in ministries at our church designed to grow and strengthen your faith alongside others.</p>',
                       color='rgba(255,255,255,0.72)', size='0.95rem', maxw='25rem')], layout_column_flex_justify='flex-end'),
  ], layout='60% 40%', gap='3rem', align='flex-end', layout_row_margin='0px auto 3.75rem auto'),
  row('Cards', [
    card('Life together', 'Connect With Us', "Develop authentic relationships with people in the same stages and phases of life, and be encouraged by God's truth.",
         'Learn More  →', '/connect/', img('communion'), '30% center'),
    card('Grow in faith', 'Life in Community', 'Our ministry programs center on gathering around the Word of God and living lives modeled after Christ.',
         'Explore Ministries  →', '/get-connected/', img('fellowship')),
  ], layout='50% 50%', gap='1.75rem', **{'class': 'gc-expand'}, **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', None, None, None]}}),
  row('Closing Line', [col('Text', [
    text("<p>It's our desire to create environments where other people in the same stages and phases of life can develop authentic relationships with one another while being encouraged to grab hold of how God's truth intersects with and impacts their lives.</p>",
         color='rgba(255,255,255,0.86)', font=F_ACC, size='clamp(1.25rem, 2.1vw, 1.65rem)', lh='1.5', maxw='54rem',
         text_font_style='italic'),
  ], layout_column_padding='2.5rem 0px 0px 0px', layout_column_border_width='1px 0px 0px 0px',
     layout_column_border_style='solid', layout_column_border_color='rgba(255,255,255,0.14)')],
     layout_row_margin='3.5rem auto 0px auto'),
], section_bg_advanced=True, bg_border_radius='inherit', bg_lower_type='image', bg_lower_image='450:full',
   bg_lower_image_size='cover', bg_lower_image_position='center', bg_lower_image_repeat='no-repeat',
   bg_upper_type='color', bg_upper_color='rgba(15, 24, 40, 0.86)', section_bg_color=DARK)

# ---------------- 4. SERMONS ----------------
sermons = section('4. Sermons', [
  row('Content', [
    col('Media', [
      div('Sermon Card', [
        headline('Live Sundays · 10 AM', tag='span', size='0.62rem', color='#ffffff', font=F_BODY, weight='700',
                 ls='0.18em', lh='1', text_text_transform='uppercase', text_bg_color='rgba(15,24,40,0.72)',
                 text_padding='0.75em 1.1em 0.75em 1.1em'),
        div('Play Button', [
          el('icon', None, [], icon='play', icon_font_size='1.6rem', icon_width='5.5rem', icon_height='5.5rem',
             icon_color=DARK, icon_bg_color=GOLD, icon_border_radius='50%',
             icon_box_shadow_dimensions='0em 0em 0em 0.7em', icon_box_shadow_color='rgba(198,173,122,0.25)',
             **hover_lift),
        ], align='center', layout_div_width='100%'),
        label_head('Truth for Every Season', 'Latest message', psize='1.15rem', text_font_family=F_DISP, text_font_weight='600'),
      ], layout_div_tag='a', layout_div_href='/watch-live/', justify='space-between', layout_div_width='100%',
         layout_div_min_height='27rem', layout_div_padding='1.5rem 1.75rem 1.6rem 1.75rem',
         layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.35)',
         **bgimg('layout_div', img('worship'), 'rgba(15, 24, 40, 0.45)'),
         **bp(layout_div_min_height=['20rem', '23rem', None, None, None])),
    ]),
    col('Text', [
      eyebrow('Listen and grow'),
      headline('Truth for every season.', margin='1.4rem 0px 1.6rem 0px'),
      text('<p>Want to hear a message before you visit? Miss a Sunday and need to catch up? Visit our Sermons page and take some time to hear the powerful messages that are preached every week!</p>',
           maxw='30rem', text_margin='0px 0px 2.1rem 0px'),
      div('Buttons', [button('Watch Live  ↗', '/watch-live/', 'navy'),
                      button('Previous Sermons  →', '/sermon-manager/', 'outline')], direction='row', gap='12px', wrap=True),
    ]),
  ], layout='52% 48%', gap='6rem', align='center', **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None], 'layout_row_gap_column': [None, None, '3rem', '4rem', None]}}),
], section_bg_color=SAND)

# ---------------- 5. GET IN TOUCH ----------------
def contact_link(label, href):
    e = text_link(label, href, color='rgba(255,255,255,0.78)', hover=GOLDS, line='transparent')
    e.update(anchor_border_width='0px', anchor_padding='0em', anchor_primary_font_size='0.9rem', anchor_primary_letter_spacing='0em',
             anchor_primary_text_transform='none', anchor_primary_font_weight='400', anchor_primary_line_height='1.6', anchor_primary_text_align='left')
    if href.startswith('http'): e['anchor_blank'] = True
    return e

def vcard(title, sub, big, icon, num):
    return col(f'Card – {title}', [
      div('Card Top', [
        headline(num, tag='span', size='1.25rem', color=GOLDD, font=F_ACC, weight='400', ls='0em', lh='1', text_font_style='italic'),
        el('icon', None, [], icon=icon, icon_font_size='1.05rem', icon_width='2.75rem', icon_height='2.75rem',
           icon_color=NAVY, icon_bg_color=IVORY, icon_border_radius='50%'),
      ], direction='row', justify='space-between', align='center', layout_div_width='100%'),
      headline(title, tag='h3', size='1.3rem', color=NAVY, weight='700', ls='-0.02em', lh='1.2', margin='1.9rem 0px 0.6rem 0px'),
      text(f'<p>{sub}</p>', size='0.9rem'),
      headline(big, tag='p', size='2.5rem', color=INK, ls='-0.05em', lh='1.1', margin='0.35rem 0px 0px 0px'),
    ], layout_column_bg_color='#ffffff', layout_column_padding='2.25rem 2.1rem 2.1rem 2.1rem',
       layout_column_border_width='1px', layout_column_border_style='solid', layout_column_border_color='rgba(36,52,77,0.14)',
       **hover_lift)

visit = section('5. Get In Touch (map)', [
  row('Heading', [
    col('Heading Group', [eyebrow('Get in touch'), headline("We'd love to meet you.", margin='1.4rem 0px 0px 0px')]),
    col('Intro', [text("<p>Whether it's your first Sunday or you're finding your way back, we'd be glad to welcome you.</p>",
                       size='0.95rem', maxw='23rem')], layout_column_flex_justify='flex-end'),
  ], layout='60% 40%', gap='3rem', align='flex-end', layout_row_margin='0px auto 3.5rem auto'),
  row('Service Times & Contact', [
    vcard('Sunday Service', 'Sunday Morning', '10 am', 'clock', '01'),
    vcard('Midweek Gathering', 'Wednesday Evenings', '6 pm', 'calendar', '02'),
    col('Card – Get In Touch', [
      div('Card Top', [
        headline('03', tag='span', size='1.25rem', color=GOLD, font=F_ACC, weight='400', ls='0em', lh='1', text_font_style='italic'),
        el('icon', None, [], icon='envelope', icon_font_size='1.05rem', icon_width='2.75rem', icon_height='2.75rem',
           icon_color=GOLD, icon_bg_color='rgba(198,173,122,0.14)', icon_border_radius='50%'),
      ], direction='row', justify='space-between', align='center', layout_div_width='100%'),
      headline('Get In Touch', tag='h3', size='1.3rem', color='#ffffff', weight='700', ls='-0.02em', lh='1.2', margin='1.9rem 0px 0.6rem 0px'),
      div('Contact Links', [contact_link(l, u) for l, u in [('1000 West Highway, City, ST 55555', 'https://www.google.com/maps/search/?api=1&query=1000+West+Highway+City+ST+55555'),
                                                           ('411.123.1234', 'tel:4111231234'), ('info@yourchurch.org', 'mailto:info@yourchurch.org')]],
          gap='0.45rem'),
    ], layout_column_bg_color=DEEP, layout_column_padding='2.25rem 2.1rem 2.1rem 2.1rem', **hover_lift),
  ], layout='30% 30% 40%', gap='1.4rem', **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '50% 50%', None, None]}}),
  row('Map', [col('Map', [
    el('map', None, [], map_type='embed', frame_content_sizing='fixed-height', frame_content_height='340px',
       map_embed_code=None, **{'class': 'gc-map'}),
  ])], layout_row_margin='1.4rem auto 0px auto'),
], section_bg_color=PAPER, id='visit')

COMP = json.load(open('components.json'))
GB = lambda key, title: {'_type': 'global-block', '_bp_base': BP, 'title': title, 'global_block_id': str(COMP[key])}
tree = [hero, welcome, connect, sermons, GB('gettouch', '5. Get In Touch (component)')]
# keep the client's own map embed from the live Home page
orig = json.load(open('graham-backup/home-tree.json'))['tree']
embed = re.search(r'"map_embed_code": (".*?(?<!\\)")', json.dumps(orig)).group(1)
def fix(e):
    if e.get('_type') == 'map': e['map_embed_code'] = json.loads(embed)
    for k in [k for k, v in e.items() if v is None]: del e[k]
    for c in e.get('_modules', []): fix(c)
for s in tree: fix(s)
json.dump(tree, open('home-tree-new.json', 'w'), indent=1)
print('ok', len(json.dumps(tree)))
