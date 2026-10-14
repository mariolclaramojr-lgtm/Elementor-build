from lc import *

HEADER_MENU = 'menu:14'
MOBILE_MENU = 'menu:15'
FOOTER_MENU = 'menu:2'


def logo(size='25px', icon='30px'):
    return el('headline', text_tag='div', text_content='Lewis Church', text_link=True, text_href='/',
              text_font_family=F_HEAD, text_font_weight='600', text_font_size=size, text_letter_spacing='0.01em',
              text_line_height='1', text_text_color=WHITE, text_text_color_alt=WHITE,
              text_graphic=True, text_graphic_type='icon', text_graphic_icon='cross', text_graphic_icon_alt='cross',
              text_graphic_icon_font_size=icon, text_graphic_icon_color=ACCENT_LIGHT,
              text_graphic_icon_color_alt=ACCENT_LIGHT, text_graphic_margin='0px 14px 0px 0px',
              text_graphic_icon_width='1.2em', text_graphic_icon_height='1.2em', text_graphic_icon_border_width='1px',
              text_graphic_icon_border_color='rgba(232, 93, 108, 0.6)', text_graphic_icon_border_radius='50%',
              **{'class': 'lc-logo'})


def nav_inline(menu, color='rgba(255, 255, 255, 0.85)', alt=ACCENT_LIGHT, size='12px', gap='34px', **kw):
    d = dict(menu=menu, menu_row_flex_justify='flex-end', menu_row_flex_gap=gap,
             anchor_padding='0px', anchor_text_margin='0px', anchor_primary_font_family=F_BODY,
             anchor_primary_font_weight='600', anchor_primary_font_size=size, anchor_primary_letter_spacing='0.16em',
             anchor_primary_text_transform='uppercase', anchor_primary_text_color=color,
             anchor_primary_text_color_alt=alt, anchor_sub_indicator=False, menu_active_links_highlight_current=True)
    d.update(kw)
    return el('nav-inline', **d)


def header_regions(solid=False, hero=None, nav_image=None):
    pill = el('headline', text_tag='span', text_content='This Sunday', text_font_family=F_BODY, text_font_weight='700',
              text_font_size='10px', text_letter_spacing='0.2em', text_text_transform='uppercase', text_line_height='1.4',
              text_text_color=WHITE, text_bg_color='rgba(255, 255, 255, 0.18)', text_padding='4px 10px',
              text_border_radius='999px')
    msg = el('headline', text_tag='span',
             text_content='Join us at 8:30 &amp; 10:00 am. Fall Kickoff picnic on the lawn after the 10 am service!',
             text_font_family=F_BODY, text_font_weight='400', text_font_size='14px', text_line_height='1.4',
             text_text_color=WHITE)
    link = el('headline', text_tag='span', text_content='Plan your visit &rarr;', text_link=True,
              text_href='/plan-your-visit/', text_font_family=F_BODY, text_font_weight='700', text_font_size='14px',
              text_line_height='1.4', text_text_color=WHITE, text_text_color_alt=WHITE,
              text_border_width='0px 0px 1px 0px', text_border_color='rgba(255, 255, 255, 0.55)',
              text_border_color_alt=WHITE)
    topbar = el('bar', [el('container', [pill, msg, link], container_flex='1 1 auto', container_row_flex_wrap=True,
                           container_row_flex_justify='center', container_row_flex_gap='6px 16px',
                           container_text_align='center')],
                _label='Top Bar', bar_height='auto', bar_padding='9px 0px', bar_bg_color=ACCENT,
                bar_global_container=True, bar_box_shadow_dimensions='!0px 0px 0px 0px', bar_z_index='10000',
                bar_row_flex_justify='center', **{'class': 'lc-topbar'})

    burger = el('nav-layered', menu=MOBILE_MENU, _label='Mobile Menu', hide_bp='lg xl',
                anchor_padding='0.8em 0em', anchor_text_margin='0px', anchor_primary_font_family=F_HEAD,
                anchor_primary_font_weight='500', anchor_primary_font_size='26px',
                anchor_primary_text_color=IVORY, anchor_primary_text_color_alt=ACCENT_LIGHT,
                anchor_sub_indicator_color=IVORY, menu_layered_back_label='Back',
                off_canvas_location='right', off_canvas_content_max_width='22em', off_canvas_body_scroll='disable',
                off_canvas_content_bg_color=ESP, off_canvas_bg_color='rgba(15, 12, 9, 0.6)',
                off_canvas_close_color='rgba(255, 255, 255, 0.6)', off_canvas_close_color_alt=WHITE,
                toggle_anchor_bg_color='transparent', toggle_anchor_box_shadow_dimensions='!0em 0em 0em 0em',
                toggle_anchor_padding='0.5em', toggle_color=WHITE, toggle_color_alt=ACCENT_LIGHT)
    nav = el('bar', [
        el('container', [logo()], container_flex='0 0 auto'),
        el('container', [
            nav_inline(HEADER_MENU, hide_bp='md sm xs'),
            button('Plan Your Visit', '/plan-your-visit/', 'primary', arrow=False, small=True,
                   hide_bp='md sm xs', **{'class': 'lc-nav-cta'}),
            burger,
        ], container_flex='0 1 auto', container_row_flex_gap='34px', container_row_flex_justify='flex-end'),
    ], _label='Navigation', bar_position_top='relative' if solid else 'absolute', bar_height='auto',
        bar_padding='26px 0px', bar_bg_color=ESP if solid else 'transparent', bar_global_container=True, bar_box_shadow_dimensions='!0px 0px 0px 0px',
        bar_border_width='0px 0px 1px 0px', bar_border_style='solid', bar_border_color=LINE_DARK,
        bar_sticky=True, bar_sticky_trigger_offset='160', bar_sticky_shrink='1', bar_sticky_slide_enabled=True,
        bar_sticky_hide_initially=False, bar_z_index='9999', **{'class': 'lc-nav'})
    if solid and nav_image:
        # Menu-only header for detail pages: the menu bar sits on the same darkened photo as the page heroes
        nav.update(bar_bg_advanced=True, bg_lower_type='image', bg_lower_image=nav_image, bg_lower_image_size='cover',
                   bg_lower_image_position='center 40%', bg_upper_type='color', bg_upper_color='rgba(15, 12, 9, 0.72)')
    bars = [topbar, nav]
    if hero:
        bars.append(hero_bar(**hero))
    return {'top': bars}


def hero_bar(eyebrow_txt, title, image='', lead_txt=None):
    """Page-title hero for templates that are not built in Cornerstone (posts, sermons, events, archives).
    Same look as the page heroes: photo + overlay, eyebrow, big Fraunces title; the nav floats over it."""
    mods = [eyebrow(eyebrow_txt, dark=True),
            heading(title, tag='h1', size='clamp(40px, 6.2vw, 80px)', color=WHITE, mb='0px', maxw='900px')]
    if lead_txt:
        mods.append(lead(lead_txt, color='rgba(255, 255, 255, 0.82)', mb='0px', maxw='560px',
                         text_margin='22px 0px 0px 0px'))
    d = dict(_label='Page Hero', bar_height='auto', bar_padding='clamp(190px, 17vw, 240px) 0px clamp(56px, 7vw, 96px) 0px',
             bar_bg_color=ESP, bar_global_container=True, bar_box_shadow_dimensions='!0px 0px 0px 0px',
             bar_z_index='1', bar_row_flex_justify='flex-start', bar_row_flex_align='flex-end')
    if image:
        d.update(bar_bg_advanced=True, bg_lower_type='image', bg_lower_image=image, bg_lower_image_size='cover',
                 bg_lower_image_position='center', bg_upper_type='color', bg_upper_color=OVERLAY)
    return el('bar', [el('container', mods, container_flex='1 1 auto', container_row_flex_direction='column',
                         container_row_flex_align='flex-start', container_row_flex_justify='flex-end')], **d)


# The only header rule Cornerstone has no control for: the bar turns red once it is stuck.
HEADER_CSS = """.lc-nav.x-bar-fixed > .x-bg { display: none; }
.lc-nav.x-bar-fixed { background-color: #A51C30; border-bottom-color: transparent; box-shadow: 0 10px 30px rgba(31, 27, 23, 0.22); }
.lc-nav.x-bar-fixed .lc-nav-cta { background-color: #fff; }
.lc-nav.x-bar-fixed .lc-nav-cta .x-anchor-text-primary { color: #A51C30; }
.lc-nav.x-bar-fixed .x-menu .x-anchor .x-anchor-text-primary { color: #fff; }"""


def footer_regions():
    social = hstack([
        el('social', anchor_graphic_icon=i, anchor_graphic_icon_alt=i, anchor_href='#', anchor_blank=True,
           anchor_share_enabled=False, anchor_width='42px', anchor_height='42px', anchor_bg_color='transparent',
           anchor_bg_color_alt=ACCENT, anchor_border_width='1px', anchor_border_color=LINE_DARK,
           anchor_border_color_alt=ACCENT, anchor_box_shadow_dimensions='!0em 0em 0em 0em',
           anchor_graphic_icon_font_size='16px', anchor_graphic_icon_color=WHITE, anchor_graphic_icon_color_alt=WHITE)
        for i in ('facebook-f', 'instagram', 'youtube')], gap='10px')
    top = el('bar', [
        el('container', [logo(),
                         nav_inline(FOOTER_MENU, color='rgba(255, 255, 255, 0.7)', gap='10px 30px',
                                    menu_row_flex_wrap=True, menu_row_flex_justify='center', menu_flex='0 1 auto'),
                         social],
           container_flex='1 1 auto', container_row_flex_wrap=True, container_row_flex_gap='28px',
           container_row_flex_justify='space-between', container_padding='44px 0px',
           **bp(container_row_flex_justify=['center', 'center', 'center']),
           container_border_width='1px 0px 0px 0px', container_border_style='solid',
           container_border_color=LINE_DARK)],
        _label='Footer Top', bar_height='auto', bar_bg_color=ESP, bar_global_container=True,
        bar_box_shadow_dimensions='!0px 0px 0px 0px', bar_z_index='auto')
    small = dict(text_font_family=F_BODY, text_font_size='12px', text_line_height='1.6',
                 text_text_color='rgba(255, 255, 255, 0.45)', text_margin='0px')
    bottom = el('bar', [
        el('container', [
            el('text', text_content='© 2026 Lewis Church. All rights reserved.', **small),
            el('text', text_content='<a href="https://reachrightstudios.com" target="_blank" rel="noopener">Church websites</a> by REACHRIGHT',
               css='$el a { color: inherit; } $el a:hover { color: #E85D6C; }', **small),
        ], container_flex='1 1 auto', container_row_flex_wrap=True, container_row_flex_gap='12px',
            container_row_flex_justify='space-between', container_padding='24px 0px 32px 0px',
            container_border_width='1px 0px 0px 0px', container_border_style='solid', container_border_color=LINE_DARK)],
        _label='Footer Bottom', bar_height='auto', bar_bg_color=ESP, bar_global_container=True,
        bar_box_shadow_dimensions='!0px 0px 0px 0px', bar_z_index='auto')
    return {'footer': [top, bottom]}
