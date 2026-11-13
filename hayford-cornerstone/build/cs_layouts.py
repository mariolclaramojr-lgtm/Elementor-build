"""Hayford header (transparent + sticky) and footer as native Pro layout documents."""
import json, sys, copy
SP = '/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad'
sys.path.insert(0, SP)
from hf import C, F, gc
from cs_home import el, btn, H, T, round_icon, div, bp

MENUS = json.load(open(f'{SP}/cs/menus.json'))
LOGO_WHITE, LOGO_DARK = '538:full', '539:full'
SEARCH = json.load(open(f'{SP}/cs/searchmodal.json'))

# Sprout logo. One PNG per display size (2x for retina): Pro caps a scaling image at half its pixel height.
LOGO_SIZE = {34: 40, 30: 34, 46: 52}
LOGO_IDS = {('538:full', 40): '675:full', ('538:full', 34): '676:full', ('538:full', 52): '677:full',
            ('539:full', 40): '678:full', ('539:full', 34): '679:full'}
def logo(src, height=34):
    height = LOGO_SIZE.get(height, height)
    src = LOGO_IDS.get((src, height), src)
    w = round(height * 214 / 58)
    return el('image', image_src=src, image_type='scaling', image_width=w, image_height=height, image_max_width=f'{w}px',
              image_link=True, image_href='/', image_alt='Hayford Church', image_retina=True,
              image_box_shadow_dimensions='0em 0em 0em 0em', image_border_width='0px')

def main_nav(dark=False):
    txt = gc('ink') if dark else gc('white')
    return el('nav-inline', menu=MENUS['Main'], _label='Main menu', menu_row_flex_direction='row', menu_items_flex_grow=False,
              anchor_padding='0.5em 0em 0.5em 0em', anchor_margin='0em 0em 0em clamp(14px, 2vw, 30px)',
              anchor_bg_color='transparent', anchor_bg_color_alt='transparent', anchor_border_width='0px',
              anchor_box_shadow_dimensions='0em 0em 0em 0em',
              anchor_primary_font_family=F['body'], anchor_primary_font_weight='700', anchor_primary_font_size='11px',
              anchor_primary_letter_spacing='0.14em', anchor_primary_text_transform='uppercase',
              anchor_primary_text_color=txt, anchor_primary_text_color_alt=txt,
              anchor_primary_particle=True, anchor_primary_particle_location='b_c', anchor_primary_particle_placement='overlap',
              anchor_primary_particle_scale='scale-x', anchor_primary_particle_height='1px', anchor_primary_particle_width='100%',
              anchor_primary_particle_color=txt, anchor_primary_particle_transform_origin='0% 50%',
              anchor_graphic=False, anchor_sub_indicator=False)

def search(dark=False):
    s = copy.deepcopy(SEARCH)
    s.update(_bp_base='4_4', toggle_anchor_graphic_icon='magnifying-glass', toggle_anchor_graphic_icon_alt='magnifying-glass',
             toggle_anchor_graphic_icon_font_size='16px', toggle_anchor_box_shadow_dimensions='0em 0em 0em 0em',
             toggle_anchor_graphic_icon_color=gc('ink') if dark else gc('white'),
             toggle_anchor_graphic_icon_color_alt=gc('accent') if dark else gc('accent_light'),
             toggle_anchor_margin='0em 0.5em 0em clamp(14px, 2vw, 30px)', modal_bg_color='rgba(9, 10, 13, 0.92)')
    s.pop('_region', None)
    return s

def live_btn(dark=False):
    d = btn('Watch Live', '/watch-live/', style='glass', small=True, icon='circle')
    d.update(anchor_min_height='40px', anchor_padding='6px 18px 6px 16px', anchor_primary_font_size='11px',
             anchor_margin='0px 0px 0px clamp(14px, 2vw, 30px)')
    if dark:
        d.update(anchor_bg_color=gc('ink'), anchor_bg_color_alt=gc('accent'), anchor_border_color=gc('ink'),
                 anchor_primary_text_color=gc('white'), anchor_primary_text_color_alt=gc('white'))
    else:
        d.update(anchor_bg_color='transparent', anchor_border_color='rgba(255, 255, 255, 0.4)')
    return d

def mobile_nav(dark=False):
    c = gc('ink') if dark else gc('white')
    return el('nav-dropdown', menu=MENUS['Mobile Menu'], _label='Mobile menu',
              toggle_color=c, toggle_color_alt=c, toggle_anchor_bg_color='transparent', toggle_anchor_bg_color_alt='transparent',
              toggle_anchor_border_width='1px', toggle_anchor_border_style='solid',
              toggle_anchor_border_color=gc('line') if dark else 'rgba(255, 255, 255, 0.35)',
              toggle_anchor_border_radius='50%', toggle_anchor_width='44px', toggle_anchor_height='44px',
              toggle_anchor_box_shadow_dimensions='0em 0em 0em 0em', toggle_burger_width='16px', toggle_burger_spacing='5px',
              toggle_burger_size='1.5px',
              dropdown_bg_color=gc('paper'), dropdown_width='calc(100vw - 32px)', dropdown_margin='14px 0px 0px 0px',
              dropdown_padding='8px 22px 16px 22px', dropdown_border_radius='18px',
              dropdown_box_shadow_dimensions='0px 24px 40px -20px', dropdown_box_shadow_color='rgba(0, 0, 0, 0.3)',
              anchor_padding='16px 0px 16px 0px', anchor_border_width='0px 0px 1px 0px', anchor_border_style='solid',
              anchor_border_color=gc('line'), anchor_border_color_alt=gc('line'), anchor_bg_color='transparent',
              anchor_bg_color_alt='transparent', anchor_box_shadow_dimensions='0em 0em 0em 0em',
              anchor_primary_font_family=F['head'], anchor_primary_font_weight='700', anchor_primary_font_size='15px',
              anchor_primary_letter_spacing='-0.01em', anchor_primary_text_color=gc('ink'), anchor_primary_text_color_alt=gc('accent'),
              anchor_graphic=False, anchor_sub_indicator=False)

def bar(label, mods, sticky=False, dark=False, mobile=False):
    b = el('bar', mods, _label=label, bar_height='68px' if mobile else ('72px' if sticky else '92px'),
           bar_position_top='absolute', bar_content_length='92%', bar_content_max_length='1240px',
           bar_outer_spacing='0px', bar_padding='0px', bar_border_width='0px', bar_z_index='9999',
           bar_bg_color='rgba(255, 255, 255, 0.92)' if dark else 'transparent',
           bar_box_shadow_dimensions='0px 1px 0px 0px' if dark else '0em 0em 0em 0em',
           bar_box_shadow_color=gc('line') if dark else 'transparent',
           hide_bp='md sm xs' if not mobile else 'lg xl')
    if not dark:
        b.update(bar_bg_advanced=True, bg_upper_type='color',
                 bg_upper_color='linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%)')
    else:
        b['effects_backdrop_filter'] = 'saturate(1.6) blur(16px)'
    if sticky:
        b.update(bar_sticky=True, bar_sticky_hide_initially=True, bar_sticky_trigger_offset='160', bar_sticky_shrink='1',
                 bar_sticky_slide_enabled=True, bar_position_top='relative')
    return b

def container(mods, **kw):
    d = el('container', mods, container_padding='0px', container_margin='0px', container_border_width='0px',
           container_box_shadow_dimensions='0em 0em 0em 0em')
    d.update(kw)
    return d

def header_regions():
    def desk(dark, sticky):
        return bar('Desktop' + (' Sticky' if sticky else ''), [
            container([logo(LOGO_DARK if dark else LOGO_WHITE)], container_flex='0 0 auto'),
            container([main_nav(dark), live_btn(dark)], container_flex='1 0 0%', container_row_flex_justify='flex-end'),
        ], sticky=sticky, dark=dark)
    def mob(dark, sticky):
        return bar('Mobile' + (' Sticky' if sticky else ''), [
            container([logo(LOGO_DARK if dark else LOGO_WHITE, 30)], container_flex='1 0 0%'),
            container([mobile_nav(dark)], container_flex='0 0 auto', container_row_flex_justify='flex-end'),
        ], sticky=sticky, dark=dark, mobile=True)
    return {'top': [desk(False, False), desk(True, True), mob(False, False), mob(True, True)]}

def solid_header_regions():
    """Header for posts, archives, sermons and events (no dark banner behind it)."""
    def desk():
        b = bar('Desktop', [container([logo(LOGO_DARK)], container_flex='0 0 auto'),
                            container([main_nav(True), live_btn(True)], container_flex='1 0 0%',
                                      container_row_flex_justify='flex-end')], dark=True)
        b.update(bar_position_top='relative', bar_sticky=True, bar_sticky_trigger_offset='0', bar_height='76px')
        return b
    def mob():
        b = bar('Mobile', [container([logo(LOGO_DARK, 30)], container_flex='1 0 0%'),
                           container([mobile_nav(True)], container_flex='0 0 auto', container_row_flex_justify='flex-end')],
                dark=True, mobile=True)
        b.update(bar_position_top='relative', bar_sticky=True, bar_sticky_trigger_offset='0')
        return b
    return {'top': [desk(), mob()]}

# ---------------------------------------------------------------- FOOTER
def footer_heading(t):
    return H(t, tag='h3', size='11px', color='accent_light', lh='1.3', ls='0.22em', weight='700',
             text_text_transform='uppercase', text_margin='6px 0px 22px 0px')

def footer_menu(ref):
    return el('nav-inline', menu=ref, menu_row_flex_direction='column', menu_items_flex_grow=False,
              anchor_padding='7px 0px 7px 0px', anchor_bg_color='transparent', anchor_bg_color_alt='transparent',
              anchor_border_width='0px', anchor_box_shadow_dimensions='0em 0em 0em 0em', anchor_flex_justify='flex-start',
              anchor_primary_font_family=F['body'], anchor_primary_font_weight='400', anchor_primary_font_size='15px',
              anchor_primary_line_height='1.5', anchor_primary_text_color='rgba(255, 255, 255, 0.68)',
              anchor_primary_text_color_alt=gc('white'), anchor_graphic=False, anchor_sub_indicator=False)

def contact_line(icon, text, href=None):
    d = el('headline', text_content=text, text_tag='div', text_font_family=F['body'], text_font_weight='400',
           text_font_size='15px', text_line_height='1.5', text_text_color='rgba(255, 255, 255, 0.68)',
           text_text_color_alt=gc('white'), text_margin='0px 0px 12px 0px',
           text_graphic=True, text_graphic_type='icon', text_graphic_icon=icon, text_graphic_icon_font_size='15px',
           text_graphic_icon_color=gc('accent_light'), text_graphic_margin='3px 12px 0px 0px', text_flex_align='flex-start')
    if href: d.update(text_link=True, text_href=href)
    return d

def social(icon, href, label):
    return el('button', anchor_href=href, anchor_text=False, anchor_bg_color='transparent', anchor_bg_color_alt=gc('white'),
              anchor_border_width='1px', anchor_border_style='solid', anchor_border_color='rgba(255, 255, 255, 0.16)',
              anchor_border_color_alt=gc('white'), anchor_border_radius='50%', anchor_width='44px', anchor_height='44px',
              anchor_padding='0px', anchor_box_shadow_dimensions='0em 0em 0em 0em', anchor_margin='0px 10px 0px 0px',
              anchor_graphic=True, anchor_graphic_type='icon', anchor_graphic_icon=icon, anchor_graphic_icon_alt=icon,
              anchor_graphic_icon_font_size='16px', anchor_graphic_icon_color=gc('white'), anchor_graphic_icon_color_alt=gc('ink'),
              anchor_graphic_margin='0px')

# Social links come from Theme Options › Social (x_social_*). Each button only shows when its field has a URL.
SOCIALS = [('x_social_facebook', 'facebook-f', 'Facebook'), ('x_social_instagram', 'instagram', 'Instagram'),
           ('x_social_youtube', 'youtube', 'YouTube'), ('x_social_twitter', 'x-twitter', 'X'),
           ('x_social_tiktok', 'tiktok', 'TikTok'), ('x_social_vimeo', 'vimeo-v', 'Vimeo'),
           ('x_social_linkedin', 'linkedin-in', 'LinkedIn'), ('x_social_pinterest', 'pinterest-p', 'Pinterest'),
           ('x_social_whatsapp', 'whatsapp', 'WhatsApp'), ('x_social_soundcloud', 'soundcloud', 'SoundCloud'),
           ('x_social_rss', 'rss', 'RSS')]

def social_links():
    out = []
    for key, icon, label in SOCIALS:
        b = social(icon, '{{dc:theme:%s}}' % key, label)
        b.update(_label=label, anchor_blank=True, anchor_margin='0px',
                 show_condition=[{'group': True, 'condition': 'expression:string', 'operand': '{{dc:theme:%s}}' % key,
                                  'operator': 'is-not', 'value': ''}])
        out.append(b)
    return out

def col(mods, flex, label):
    return div(mods, _label=label, layout_div_flex=flex, layout_div_min_width='180px')

def footer_regions():
    brand = col([div([logo(LOGO_WHITE, 46)], _label='Logo', layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_align='center', layout_div_height='52px'),
                 T('A place to belong. A faith to grow. We would love to welcome you and your family this weekend.',
                   color='white', size='15px', lh='1.75', text_max_width='320px', text_margin='24px 0px 0px 0px', effects_opacity='0.62'),
                 div(social_links(), _label='Social (Theme Options)',
                     layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_wrap=True, layout_div_flex_gap='10px', layout_div_margin='28px 0px 0px 0px')],
                '1.6 1 280px', 'Brand')
    explore = col([footer_heading('Explore'), footer_menu(MENUS['Footer Explore'])], '1 1 180px', 'Explore')
    join = col([footer_heading('Join Us'), footer_menu(MENUS['Footer Join Us'])], '1 1 180px', 'Join Us')
    touch = col([footer_heading('Get in Touch'),
                 contact_line('envelope', 'info@yourchurch.com', 'mailto:info@yourchurch.com'),
                 contact_line('phone', '(555) 555-5555', 'tel:5555555555'),
                 contact_line('location-dot', '1265 Lombardi Ave,<br>Green Bay, WI 54304')], '1.2 1 220px', 'Get in Touch')
    main = el('bar', [container([div([brand, explore, join, touch], _label='Columns', layout_div_flexbox=True,
                                     layout_div_flex_direction='row', layout_div_flex_wrap=True, layout_div_flex_gap='48px',
                                     layout_div_width='100%', layout_div_flex_align='flex-start')],
                                container_flex='1 0 0%')],
              _label='Footer main', bar_height='auto', bar_padding='88px 0px 56px 0px', bar_bg_color=gc('ink'),
              bar_content_length='92%', bar_content_max_length='1240px', bar_outer_spacing='0px', bar_border_width='0px',
              bar_box_shadow_dimensions='0em 0em 0em 0em')
    bp(main, 'bar_padding', md='72px 0px 40px 0px', sm='56px 0px 24px 0px')
    word = el('bar', [container([H('HAYFORD', tag='div', size='clamp(72px, 18.6vw, 262px)', color='white', lh='0.78',
                                   ls='-0.05em', text_text_align='center', effects_opacity='0.07', text_overflow=True)],
                                container_flex='1 0 0%', container_row_flex_justify='center')],
              _label='Wordmark', bar_height='auto', bar_padding='0px', bar_bg_color=gc('ink'), bar_content_length='92%',
              bar_content_max_length='1240px', bar_outer_spacing='0px', bar_border_width='0px', bar_overflow='hidden',
              bar_box_shadow_dimensions='0em 0em 0em 0em')
    copy_t = T('© Hayford Church. All rights reserved. · Church websites by <a href="https://reachrightstudios.com" target="_blank" rel="noopener">ReachRight</a>',
               color='white', size='11px', lh='1.6', text_letter_spacing='0.12em', text_text_transform='uppercase', effects_opacity='0.45')
    quick = el('nav-inline', menu=MENUS['Footer Quick Links'], menu_row_flex_direction='row',
               anchor_padding='0.25em 0em', anchor_margin='0em 28px 0em 0em', anchor_bg_color='transparent',
               anchor_bg_color_alt='transparent', anchor_border_width='0px',
               anchor_box_shadow_dimensions='0em 0em 0em 0em', anchor_primary_font_family=F['body'],
               anchor_primary_font_weight='700', anchor_primary_font_size='11px',
               anchor_primary_letter_spacing='0.14em', anchor_primary_text_transform='uppercase',
               anchor_primary_text_color='rgba(255, 255, 255, 0.7)', anchor_primary_text_color_alt=gc('white'),
               anchor_graphic=False, anchor_sub_indicator=False)
    row = div([copy_t, quick], _label='Copyright + quick links', layout_div_flexbox=True, layout_div_flex_direction='row',
              layout_div_flex_wrap=True, layout_div_flex_justify='space-between', layout_div_flex_align='center',
              layout_div_flex_gap='12px 24px', layout_div_width='100%')
    bp(row, 'layout_div_flex_direction', sm='column')
    bp(row, 'layout_div_flex_align', sm='flex-start')
    bottom = el('bar', [container([row], container_flex='1 0 0%')],
                _label='Footer bottom', bar_height='auto', bar_padding='26px 0px 30px 0px', bar_bg_color=gc('ink'),
                bar_content_length='92%', bar_content_max_length='1240px', bar_outer_spacing='0px',
                bar_border_width='1px 0px 0px 0px', bar_border_style='solid', bar_border_color='rgba(255, 255, 255, 0.1)',
                bar_box_shadow_dimensions='0em 0em 0em 0em')
    return {'footer': [main, word, bottom]}

if __name__ == '__main__':
    json.dump({'header': header_regions(), 'solid': solid_header_regions(), 'footer': footer_regions()},
              open(f'{SP}/cs/layouts.json', 'w'), indent=1)
    print('ok')
