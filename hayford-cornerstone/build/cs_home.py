"""Hayford homepage as native Cornerstone elements (modelled on the site's own element shapes)."""
import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad')
from hf import C, F, gc

M = json.load(open('/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad/cs/media.json'))
def img(k): return f"{M[k]['id']}:full"

# ---------------------------------------------------------------- primitives
def el(t, mods=None, **kw):
    d = {'_type': t, '_bp_base': '4_4'}
    d.update(kw)
    if mods is not None: d['_modules'] = mods
    return d

def bp(d, key, md=None, sm=None, xs=None, lg=None):
    """Desktop-first overrides. Slots = [xs, sm, md, lg, xl(base)]; a value cascades to smaller sizes."""
    d.setdefault('_bp_data4_4', {})[key] = [xs, sm, md, lg, None]
    return d

def reveal(d, delay=0):
    d.update(effects_scroll=True, effects_type_scroll='transform', effects_opacity_exit='0',
             effects_transform_exit='translate(0px, 28px)', effects_duration_scroll='900ms',
             effects_delay_scroll=f'{int(delay*1000)}ms', effects_offset_bottom='8%',
             effects_timing_function_scroll='cubic-bezier(0.2, 0.7, 0.2, 1)')
    return d

def lift(d):
    d.update(effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -4px)',
             effects_duration='400ms', effects_timing_function='cubic-bezier(0.2, 0.7, 0.2, 1)')
    return d

def H(text, tag='h2', size='clamp(38px, 4.6vw, 64px)', color='ink', lh='1', ls='-0.045em', weight='800', **kw):
    return el('headline', text_content=text, text_tag=tag, text_font_family=F['head'], text_font_weight=weight,
              text_font_size=size, text_line_height=lh, text_letter_spacing=ls, text_text_color=gc(color), **kw)

def T(html, color='ink_soft', size='16.5px', lh='1.85', **kw):
    return el('text', text_content=html, text_font_family=F['body'], text_font_weight='400', text_font_size=size,
              text_line_height=lh, text_text_color=gc(color), **kw)

def eyebrow(text, color='accent', margin='0px 0px 18px 0px'):
    return el('headline', text_content=text, text_tag='div', text_font_family=F['body'], text_font_weight='700',
              text_font_size='11px', text_letter_spacing='0.22em', text_text_transform='uppercase', text_line_height='1.4',
              text_text_color=gc(color), text_margin=margin,
              text_graphic=True, text_graphic_type='icon', text_graphic_icon='minus', text_graphic_icon_font_size='1.6em',
              text_graphic_icon_color=gc(color), text_graphic_margin='0em 0.75em 0em 0em')

def btn(text, href, style='light', small=False, icon='arrow-up-right', blank=False):
    """Pill button with a round arrow chip (native button graphic)."""
    pal = {'light': ('white', 'ink', 'ink', 'white', 'paper'),
           'dark': ('ink', 'white', 'accent_light', 'ink', 'ink2'),
           'glass': (None, 'white', 'white', 'ink', None)}[style]
    bgc, txt, chipbg, chipc, hover = pal
    chip = '34px' if small else '40px'
    d = el('button', anchor_text_primary_content=text, anchor_href=href, anchor_blank=blank,
           anchor_bg_color=gc(bgc) if bgc else 'rgba(255, 255, 255, 0.08)',
           anchor_bg_color_alt=gc(hover) if hover else 'rgba(255, 255, 255, 0.16)',
           anchor_border_width='1px' if style == 'glass' else '!0px', anchor_border_style='solid',
           anchor_border_color='rgba(255, 255, 255, 0.28)' if style == 'glass' else 'transparent',
           anchor_border_radius='999px', anchor_padding='6px 6px 6px 24px' if not small else '6px 6px 6px 20px',
           anchor_min_height='46px' if small else '52px', anchor_flex_justify='space-between',
           anchor_box_shadow_dimensions='0em 0em 0em 0em', anchor_box_shadow_color='transparent',
           anchor_box_shadow_color_alt='rgba(9, 10, 13, 0.25)',
           anchor_primary_font_family=F['body'], anchor_primary_font_weight='700',
           anchor_primary_font_size='11px' if small else '12px', anchor_primary_letter_spacing='0.12em',
           anchor_primary_text_transform='uppercase', anchor_primary_line_height='1',
           anchor_primary_text_color=gc(txt), anchor_primary_text_color_alt=gc(txt),
           anchor_text_margin='0px 14px 0px 0px',
           anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon=icon, anchor_graphic_icon_alt=icon,
           anchor_graphic_icon_font_size='14px', anchor_graphic_icon_width=chip, anchor_graphic_icon_height=chip,
           anchor_graphic_icon_color=gc(chipc), anchor_graphic_icon_color_alt=gc(chipc),
           anchor_graphic_icon_bg_color=gc(chipbg), anchor_graphic_icon_bg_color_alt=gc('accent') if style == 'light' else gc(chipbg),
           anchor_graphic_icon_border_radius='50%', anchor_graphic_margin='0px',
           anchor_flex_direction='row-reverse')
    if style == 'glass' and icon == 'circle':
        d.update(anchor_flex_direction='row', anchor_flex_justify='center', anchor_padding='6px 24px 6px 22px',
                 anchor_graphic_icon_font_size='8px', anchor_graphic_icon_width='8px', anchor_graphic_icon_height='8px',
                 anchor_graphic_icon_color=gc('live'), anchor_graphic_icon_color_alt=gc('live'),
                 anchor_graphic_icon_bg_color='transparent', anchor_graphic_icon_bg_color_alt='transparent',
                 anchor_graphic_margin='0px 10px 0px 0px', anchor_text_margin='0px')
    lift(d)
    return d

def div(mods, **kw): return el('layout-div', mods, **kw)

def round_icon(icon, dark=False, size='42px'):
    return el('icon', icon=icon, icon_font_size='17px', icon_width=size, icon_height=size,
              icon_color=gc('accent_light' if dark else 'accent'), icon_bg_color='transparent',
              icon_border_radius='50%', icon_border_width='1px', icon_border_style='solid',
              icon_border_color=gc('line_dark' if dark else 'line'))

def card_shadow(prefix, d):
    d[f'{prefix}_box_shadow_dimensions'] = '0px 18px 40px -18px'
    d[f'{prefix}_box_shadow_color'] = 'rgba(14, 16, 19, 0.18)'
    return d

def cell(mods, label, cols, md, sm=(1, 2), **kw):
    base = dict(layout_cell_flexbox=True, layout_cell_flex_direction='column', layout_cell_border_radius='22px',
                layout_cell_overflow='hidden')
    base.update(kw)
    d = el('layout-cell', mods, _label=label, layout_cell_column_start=cols[0], layout_cell_column_end=cols[1], **base)
    bp(d, 'layout_cell_column_start', md=md[0], sm=sm[0])
    bp(d, 'layout_cell_column_end', md=md[1], sm=sm[1])
    return d

# ---------------------------------------------------------------- 1. HERO
def times_row(day, time, first=False):
    return div([T(day, color='white', size='14px', lh='1.4', text_text_align='left'),
                H(time, tag='div', size='20px', color='white', lh='1', ls='-0.02em')],
               layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
               layout_div_flex_align='center', layout_div_width='100%', layout_div_padding='14px 0px 14px 0px',
               layout_div_border_width='1px 0px 0px 0px', layout_div_border_style='solid',
               layout_div_border_color='rgba(255, 255, 255, 0.14)')

times_card = el('layout-column', [
    div([div([H('Service Times', tag='h3', size='22px', color='white', lh='1.2', ls='-0.02em'),
              T("We can't wait to meet you!", color='white', size='13px', lh='1.5', text_margin='4px 0px 0px 0px')]),
         round_icon('clock', dark=True)],
        layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
        layout_div_flex_align='flex-start', layout_div_width='100%', layout_div_margin='0px 0px 18px 0px'),
    times_row('Sundays', '10AM'), times_row('Sunday Evenings', '6PM'), times_row('Wednesdays', '7PM'),
], _label='Service Times (glass card)', id='service-times',
   layout_column_bg_color='rgba(255, 255, 255, 0.08)', layout_column_border_width='1px', layout_column_border_style='solid',
   layout_column_border_color='rgba(255, 255, 255, 0.18)', layout_column_border_radius='22px',
   layout_column_padding='28px 28px 22px 28px', layout_column_flexbox=True, layout_column_flex_direction='column',
   layout_column_box_shadow_dimensions='0px 30px 60px -30px', layout_column_box_shadow_color='rgba(0, 0, 0, 0.6)',
   effects_backdrop_filter='blur(20px) saturate(1.3)')
reveal(times_card, .3)

hero_copy = el('layout-column', [
    reveal(eyebrow('A place to belong · A faith to grow', color='accent_light', margin='0px 0px 26px 0px')),
    reveal(bp(H('Join Us<br>This Weekend', tag='h1', size='clamp(56px, 8vw, 116px)', color='white', lh='0.9', ls='-0.05em'),
              'text_font_size', sm='clamp(50px, 15vw, 72px)'), .1),
    reveal(div([btn('Plan Your Visit', '/plan-your-visit/'),
                btn('Watch Live', '/watch-live/', style='glass', icon='circle')],
               layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_wrap=True,
               layout_div_flex_justify='flex-start', layout_div_flex_align='center', layout_div_flex_gap='12px',
               layout_div_margin='40px 0px 0px 0px'), .2),
], _label='Hero copy', layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_justify='flex-end')

hero_row = el('layout-row', [hero_copy, times_card], _label='Hero content', layout_row_global_container=True,
              layout_row_layout='62% 38%', layout_row_gap_column='56px', layout_row_gap_row='40px',
              layout_row_flex_align='flex-end')
bp(hero_row, 'layout_row_layout', md='100%')
bp(hero_row, 'layout_row_gap_column', md='0px')
# keep the glass card at max 380px wide on desktop
times_card['layout_column_max_width'] = '380px'
times_card['layout_column_width'] = '100%'
bp(times_card, 'layout_column_max_width', md='440px')

hero = el('section', [hero_row], _label='1. Hero', id='visit',
          section_padding='clamp(160px, 26vh, 300px) 0px 72px 0px', section_bg_color=gc('ink'),
          section_bg_advanced=True, section_overflow='hidden',
          bg_lower_type='video', bg_lower_video=M['hero_mp4']['url'], bg_lower_video_poster=img('hero_poster'),
          bg_lower_video_loop=True,
          bg_upper_type='color',
          bg_upper_color='linear-gradient(0deg, rgba(9, 10, 13, 0.88) 0%, rgba(9, 10, 13, 0.25) 55%, rgba(9, 10, 13, 0.45) 100%)')
bp(hero, 'section_padding', md='150px 0px 48px 0px', sm='130px 0px 32px 0px')

# ---------------------------------------------------------------- 2. WELCOME + BENTO
intro = el('layout-row', [
    el('layout-column', [eyebrow('Welcome to Hayford'), H('Find your place. Grow your faith.', tag='h2', size='clamp(38px, 4.6vw, 64px)')]),
    el('layout-column', [T("There's a place for you here.", size='17px', lh='1.6',
                           text_padding='0px 0px 0px 20px', text_border_width='0px 0px 0px 1px', text_border_style='solid',
                           text_border_color=gc('accent'))],
       layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_justify='flex-end',
       layout_column_flex_align='flex-end'),
], _label='Intro', layout_row_global_container=True, layout_row_layout='60% 40%', layout_row_gap_column='40px',
   layout_row_gap_row='20px', layout_row_margin='0px auto 36px auto')
bp(intro, 'layout_row_layout', md='100%')
bp(intro, 'layout_row_gap_column', md='0px')
bp(intro['_modules'][1], 'layout_column_flex_align', md='flex-start')
reveal(intro)

def card_head(title, sub, icon):
    return div([div([H(title, tag='h3', size='26px', lh='1.2', ls='-0.035em'),
                     T(sub, size='14.5px', lh='1.5', text_margin='8px 0px 0px 0px')]),
                round_icon(icon)],
               layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
               layout_div_flex_align='flex-start', layout_div_width='100%', layout_div_margin='0px 0px 26px 0px')

def menu_list(menu_ref):
    """Vertical WordPress menu with dividers and an arrow (editable under Appearance › Menus)."""
    return el('nav-inline', menu=menu_ref, menu_row_flex_direction='column', menu_items_flex_grow=True,
              anchor_flex_justify='space-between', anchor_width='100%',
              anchor_padding='17px 0px 17px 0px', anchor_border_width='1px 0px 0px 0px', anchor_border_style='solid',
              anchor_border_color=gc('line'), anchor_border_color_alt=gc('line'),
              anchor_primary_font_family=F['head'], anchor_primary_font_weight='700', anchor_primary_font_size='16px',
              anchor_primary_letter_spacing='-0.01em', anchor_primary_text_color=gc('ink'),
              anchor_primary_text_color_alt=gc('accent_dark'),
              anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon='arrow-right', anchor_graphic_icon_alt='arrow-right',
              anchor_graphic_icon_font_size='16px', anchor_graphic_icon_color=gc('muted'),
              anchor_graphic_icon_color_alt=gc('accent_dark'), anchor_graphic_margin='0px',
              anchor_flex_direction='row-reverse', anchor_text_margin='0px', anchor_sub_indicator=False)

def image_card(label, image, eyebrow_t, title, body, button, cols, md, minh='420px', title_size='clamp(28px, 2.6vw, 38px)', extra=None):
    mods = ([extra] if extra else []) + [
        div([eyebrow(eyebrow_t, color='accent_light', margin='0px 0px 14px 0px'),
             H(title, tag='h3', size=title_size, color='white', lh='1', ls='-0.04em', text_margin='0px 0px 12px 0px'),
             T(body, color='white', size='15px', lh='1.6', text_margin='0px 0px 24px 0px', text_max_width='460px'),
             button], layout_div_padding='34px', layout_div_width='100%')]
    c = cell(mods, label, cols, md, layout_cell_min_height=minh, layout_cell_flex_justify='flex-end',
             layout_cell_bg_color=gc('ink'), layout_cell_bg_advanced=True,
             bg_lower_type='image', bg_lower_image=image, bg_lower_image_size='cover', bg_lower_image_position='center',
             bg_upper_type='color',
             bg_upper_color='linear-gradient(0deg, rgba(9, 10, 13, 0.92) 0%, rgba(9, 10, 13, 0.55) 50%, rgba(9, 10, 13, 0.15) 100%)',
             bg_border_radius='22px')
    bp(c['_modules'][-1], 'layout_div_padding', sm='26px 24px 26px 24px')
    card_shadow('layout_cell', c)
    return lift(c)

welcome = cell([
    div([eyebrow('Welcome home', color='accent_light', margin='0px'),
         H('Faith.<br>Community.<br><span class="hf-accent is-on-dark">Hope.</span>', tag='div', size='clamp(38px, 4.2vw, 58px)', color='white', lh='0.98', ls='-0.045em')],
        _label='Label', layout_div_flexbox=True, layout_div_flex_direction='column', layout_div_flex_justify='space-between',
        layout_div_flex_align='flex-start', layout_div_flex='0 0 35%', layout_div_padding='clamp(36px, 4.5vw, 64px)',
        layout_div_border_width='0px 1px 0px 0px', layout_div_border_style='solid', layout_div_border_color=gc('line_dark'),
        layout_div_min_height='100%'),
    div([H('Welcome', tag='h2', size='clamp(30px, 2.8vw, 40px)', color='white', lh='1.1', ls='-0.035em', text_margin='0px 0px 20px 0px'),
         T('<p>We are a congregation of believers committed to sharing the message of Christ and guiding others towards faith in Him. As a church, we aim to love those in our community with the same love Christ has given to us. The work of our church is aimed at directing others towards the Savior in the hopes that they will encounter the one true God and be transformed by His gracious love for them. Through all we do, say, and preach, we pray that we will shine the light of Christ to all those we encounter.</p>',
           color='white', size='16.5px', lh='1.85', text_max_width='640px', text_margin='0px 0px 32px 0px', effects_opacity='0.75'),
         btn('About Us', '/about/', style='glass', small=True)],
        _label='Copy', layout_div_flex='1 1 0%', layout_div_padding='clamp(36px, 4.5vw, 64px)'),
], 'Welcome', (1, 13), (1, 3), layout_cell_flex_direction='row', layout_cell_min_height='520px',
   layout_cell_bg_color=gc('ink2'), layout_cell_bg_advanced=True, bg_lower_type='image', bg_lower_image=img('img_welcome'),
   bg_lower_image_size='cover', bg_lower_image_position='center 40%', bg_upper_type='color',
   bg_upper_color='linear-gradient(90deg, rgba(9, 10, 13, 0.25) 0%, rgba(9, 10, 13, 0.5) 34%, rgba(9, 10, 13, 0.86) 56%, rgba(9, 10, 13, 0.92) 100%)',
   bg_border_radius='22px')
bp(welcome, 'layout_cell_flex_direction', md='column')
bp(welcome, 'layout_cell_min_height', md='0px')
lbl = welcome['_modules'][0]
bp(lbl, 'layout_div_border_width', md='0px 0px 1px 0px')
bp(lbl, 'layout_div_flex', md='0 0 auto')
bp(lbl, 'layout_div_min_height', md='300px')
bp(lbl, 'layout_div_padding', sm='30px 26px 30px 26px')
bp(welcome['_modules'][1], 'layout_div_padding', sm='30px 26px 30px 26px')
card_shadow('layout_cell', welcome)
reveal(welcome)

play = div([el('button', anchor_href='/messages/', anchor_text=False, anchor_bg_color='rgba(255, 255, 255, 0.16)',
               anchor_bg_color_alt='rgba(255, 255, 255, 0.28)', anchor_border_width='1px', anchor_border_style='solid',
               anchor_border_color='rgba(255, 255, 255, 0.35)', anchor_border_radius='50%', anchor_width='76px', anchor_height='76px',
               anchor_padding='0px', anchor_box_shadow_dimensions='0em 0em 0em 0em', anchor_box_shadow_color='transparent',
               anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon='play', anchor_graphic_icon_alt='play',
               anchor_graphic_icon_font_size='22px', anchor_graphic_icon_color=gc('white'), anchor_graphic_icon_color_alt=gc('white'),
               anchor_graphic_margin='0px 0px 0px 4px', effects_backdrop_filter='blur(10px)')],
           _label='Play button', layout_div_position='absolute', layout_div_top='28px', layout_div_right='28px', layout_div_z_index='2')

messages = image_card('Recent Messages', img('img_messages'), 'Watch and grow', 'Recent Messages',
                      "Miss a message or can't make it to church? Watch with us from home.",
                      btn('Listen Now', '/messages/', small=True), (1, 9), (1, 3), title_size='clamp(36px, 4vw, 56px)', extra=play)
reveal(messages)

connect = cell([card_head('Get Connected', "Life is better when we're connected.", 'users'), menu_list('menu:11')],
               'Get Connected', (9, 13), (1, 2), layout_cell_bg_color=gc('white'), layout_cell_padding='34px 34px 20px 34px')
bp(connect, 'layout_cell_padding', sm='28px 24px 14px 24px')
card_shadow('layout_cell', connect)
reveal(connect, .1)

events = image_card('Upcoming Events', img('img_events'), 'Be part of it', 'Upcoming Events',
                    'See what is happening here at Hayford Church and stay up-to-date.',
                    btn("See What's Next", '/events-page/', small=True), (1, 5), (2, 3))
reveal(events)

MAPQ = '1265+Lombardi+Ave,+Green+Bay,+WI+54304'
location = cell([
    el('map', map_embed_code=f'<iframe title="Map to Hayford Church, 1265 Lombardi Ave, Green Bay, WI 54304" src="https://maps.google.com/maps?q={MAPQ}&z=15&output=embed" width="600" height="450" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>',
       frame_content_sizing='fixed-height', frame_content_height='260px', _label='Map'),
    div([div([round_icon('location-dot'),
              el('headline', text_content='1265 Lombardi Ave, Green Bay, WI 54304', text_tag='div', text_font_family=F['body'],
                 text_font_weight='600', text_font_size='14.5px', text_line_height='1.4', text_text_color=gc('ink'),
                 text_subheadline=True, text_subheadline_content='Visit us', text_subheadline_reverse=True,
                 text_subheadline_font_family=F['body'], text_subheadline_font_weight='700', text_subheadline_font_size='10.5px',
                 text_subheadline_letter_spacing='0.18em', text_subheadline_text_transform='uppercase',
                 text_subheadline_text_color=gc('muted'), text_subheadline_spacing='3px')],
             layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_align='center', layout_div_flex_gap='14px',
             layout_div_flex_wrap=False),
         dict(btn('Get Directions', f'https://www.google.com/maps/dir/?api=1&destination={MAPQ}', style='dark', small=True, blank=True),
              anchor_width='100%')],
        _label='Address + directions', layout_div_flexbox=True, layout_div_flex_direction='column', layout_div_flex_gap='14px',
        layout_div_flex_align='stretch', layout_div_padding='18px 20px 20px 20px', layout_div_width='100%'),
], 'Location (map)', (5, 9), (1, 2), layout_cell_bg_color=gc('white'), layout_cell_min_height='420px')
card_shadow('layout_cell', location)
reveal(location, .1)

step = cell([card_head('Take a Step', 'See what God can do through you.', 'stairs'), menu_list('menu:12')],
            'Take a Step', (9, 13), (2, 3), layout_cell_bg_color=gc('white'), layout_cell_padding='34px 34px 20px 34px')
bp(step, 'layout_cell_padding', sm='28px 24px 14px 24px')
card_shadow('layout_cell', step)
reveal(step, .2)

def contact_tile(icon, label, value, href=None):
    d = div([round_icon(icon, size='42px'),
             el('headline', text_content=value, text_tag='div', text_font_family=F['body'], text_font_weight='600',
                text_font_size='14.5px', text_line_height='1.4', text_text_color=gc('ink'),
                text_subheadline=True, text_subheadline_content=label, text_subheadline_reverse=True,
                text_subheadline_font_family=F['body'], text_subheadline_font_weight='700', text_subheadline_font_size='10.5px',
                text_subheadline_letter_spacing='0.18em', text_subheadline_text_transform='uppercase',
                text_subheadline_text_color=gc('muted'), text_subheadline_spacing='3px')],
            _label=label, layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_align='center',
            layout_div_flex_gap='16px', layout_div_flex_wrap=False, layout_div_padding='18px 20px', layout_div_border_radius='14px',
            layout_div_bg_color=gc('paper'), layout_div_bg_color_alt=gc('sand'), layout_div_flex='1 1 200px')
    d['_modules'][0]['icon_bg_color'] = gc('white')
    d['_modules'][0]['icon_border_width'] = '0px'
    if href: d['layout_div_href'] = href
    bp(d, 'layout_div_flex', sm='0 0 auto')
    bp(d, 'layout_div_width', sm='100%')
    return d

# Plan Your Visit CTA (replaces the Contact Us card; contact details live in the footer + visit band)
visit_icon = el('icon', icon='door-open', icon_font_size='22px', icon_width='64px', icon_height='64px',
                icon_color=gc('accent'), icon_bg_color=gc('paper'), icon_border_radius='50%')
visit_copy = div([eyebrow('New here?', margin='0px 0px 10px 0px'),
                  H('Plan Your Visit', tag='h3', size='clamp(26px, 2.4vw, 32px)', lh='1.15', ls='-0.035em'),
                  T('Visiting somewhere new can be intimidating. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!',
                    size='15.5px', lh='1.7', text_margin='10px 0px 0px 0px', text_max_width='620px')],
                 _label='Copy', layout_div_flex='1 1 320px')
bp(visit_copy, 'layout_div_flex', md='0 0 auto')
contact = cell([
    div([visit_icon, visit_copy], _label='Icon + copy', layout_div_flexbox=True, layout_div_flex_direction='row',
        layout_div_flex_align='center', layout_div_flex_gap='28px', layout_div_flex_wrap=False, layout_div_flex='1 1 480px'),
    div([btn("Let Us Know You're Coming", '/plan-your-visit/#register-form', style='dark')], _label='Button',
        layout_div_flex='0 0 auto'),
], 'Plan Your Visit (CTA)', (1, 13), (1, 3), id='plan-your-visit', layout_cell_bg_color=gc('white'),
   layout_cell_flex_direction='row', layout_cell_flex_align='center', layout_cell_flex_justify='space-between',
   layout_cell_flex_wrap=True, layout_cell_flex_gap='32px', layout_cell_padding='34px 38px')
bp(contact, 'layout_cell_flex_direction', md='column')
bp(contact, 'layout_cell_flex_align', md='flex-start')
bp(contact, 'layout_cell_flex_gap', md='24px')
bp(contact, 'layout_cell_padding', sm='28px 24px')
bp(contact['_modules'][0], 'layout_div_flex_direction', sm='column')
bp(contact['_modules'][0], 'layout_div_flex_align', sm='flex-start')
bp(contact['_modules'][0], 'layout_div_flex_gap', sm='18px')
bp(contact['_modules'][0], 'layout_div_flex', md='0 0 auto')
card_shadow('layout_cell', contact)
reveal(contact)

grid = el('layout-grid', [welcome, messages, connect, events, location, step, contact], _label='Bento',
          layout_grid_template_columns='repeat(12, minmax(0, 1fr))', layout_grid_template_rows='auto',
          layout_grid_gap_column='20px', layout_grid_gap_row='20px', layout_grid_global_container=True)
bp(grid, 'layout_grid_template_columns', md='repeat(2, minmax(0, 1fr))', sm='minmax(0, 1fr)')
bp(grid, 'layout_grid_gap_column', md='16px', sm='14px')
bp(grid, 'layout_grid_gap_row', md='16px', sm='14px')

# Closing CTA (inside the same section, like the mockup)
cta = el('layout-row', [
    el('layout-column', [eyebrow('Come as you are', color='accent_light'),
                         H("We'd love to see you this Sunday.", tag='h2', size='clamp(36px, 4.6vw, 64px)', color='white',
                           text_max_width='720px', text_margin='0px 0px 18px 0px'),
                         T('Come as you are. There\'s a place for you at Hayford Church.', color='white', size='17px', lh='1.6',
                           effects_opacity='0.75')]),
    el('layout-column', [btn('Plan Your Visit', '/plan-your-visit/')], layout_column_flexbox=True,
       layout_column_flex_direction='column', layout_column_flex_justify='flex-end', layout_column_flex_align='flex-end'),
], _label='Closing CTA', id='live', layout_row_global_container=True, layout_row_layout='70% 30%', layout_row_gap_column='40px',
   layout_row_gap_row='32px', layout_row_flex_align='flex-end', layout_row_margin='20px auto 0px auto',
   layout_row_padding='clamp(56px, 7vw, 96px) clamp(28px, 6vw, 80px)', layout_row_border_radius='22px',
   layout_row_overflow='hidden', layout_row_bg_color=gc('ink'), layout_row_bg_advanced=True,
   bg_lower_type='image', bg_lower_image=img('img_cta'), bg_lower_image_size='cover', bg_lower_image_position='center 60%',
   bg_upper_type='color', bg_upper_color='linear-gradient(90deg, rgba(9, 10, 13, 0.92) 0%, rgba(9, 10, 13, 0.7) 55%, rgba(9, 10, 13, 0.45) 100%)',
   bg_border_radius='22px')
bp(cta, 'layout_row_layout', md='100%')
bp(cta, 'layout_row_gap_column', md='0px')
bp(cta, 'layout_row_padding', sm='48px 26px')
bp(cta['_modules'][1], 'layout_column_flex_align', md='flex-start')
reveal(cta)

bento = el('section', [intro, grid], _label='2. Welcome + bento', id='main',
           section_padding='clamp(48px, 5vw, 72px) 0px 20px 0px', section_bg_color=gc('paper'))

# 3. Closing CTA = reusable Component (edit it once under Components; every page updates)
cta_component = {'_type': 'global-block', 'global_block_id': '591', '_label': '3. Closing CTA (component)'}

TREE = [hero, bento, cta_component]

if __name__ == '__main__':
    json.dump(TREE, open('/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad/cs/home_tree.json', 'w'), indent=1)
    print('elements:', json.dumps(TREE).count('"_type"'))
