"""Rebuild the Main Header (186) from its own element shapes: new logo, Edwards colours/fonts, social icons,
Plan Your Visit button, sticky bar (solid on scroll via global CSS .ed-header-bar.x-bar-fixed)."""
import json, copy, os
from cs_lib import G, FONT, BTN_BASE, BTN, ARROW

def build(orig, media):
    regions = copy.deepcopy(orig['regions'])
    logo = media['logo-white']
    def fix_logo(img):
        img.update(image_src=f"{logo['id']}:full", image_type='standard', image_styled_width='180px', image_width=585, image_height=162, image_retina=False,
                   image_href='/', image_link=True, image_alt='Edwards Church', title='Logo')
    def fix_collapsed(nc, menu):
        nc.update(menu=menu, title='Mobile Menu (off-canvas)',
          toggle_color=G('white'), toggle_color_alt=G('accent'), toggle_anchor_primary_particle=False, toggle_anchor_secondary_particle=False,
          off_canvas_bg_color=G('slate-deep', 0.6), off_canvas_content_bg_color=G('slate-deep'), off_canvas_close_color=G('white'), off_canvas_close_color_alt=G('accent'),
          anchor_bg_color='transparent', anchor_bg_color_alt=G('white', 0.06),
          anchor_border_color=f"{G('white', 0.08)} transparent transparent transparent", anchor_border_color_alt=f"{G('white', 0.08)} transparent transparent transparent",
          anchor_primary_font_family=FONT, anchor_primary_font_weight='600', anchor_primary_letter_spacing='0.16em', anchor_primary_font_size='0.85em',
          anchor_primary_text_color=G('white'), anchor_primary_text_color_alt=G('accent'), anchor_primary_particle_color=G('accent', 0.12),
          sub_anchor_primary_text_color=G('white'), sub_anchor_primary_text_color_alt=G('accent'))
    def social(net, icon, href):
        return {'_type': 'social', '_bp_base': '4_4', '_region': 'top', 'title': f'Social – {net}',
                'anchor_graphic_icon': icon, 'anchor_graphic_icon_alt': icon, 'anchor_href': href, 'anchor_blank': True,
                'anchor_width': '2.15em', 'anchor_height': '2.15em', 'anchor_margin': '0em 0.5em 0em 0em',
                'anchor_bg_color': 'transparent', 'anchor_bg_color_alt': G('accent'),
                'anchor_border_width': '1px', 'anchor_border_style': 'solid', 'anchor_border_color': G('white', 0.3), 'anchor_border_color_alt': G('accent'),
                'anchor_box_shadow_dimensions': '!0em 0em 0em 0em', 'anchor_graphic_icon_font_size': '0.95em',
                'anchor_graphic_icon_color': G('white'), 'anchor_graphic_icon_color_alt': G('white'), '_modules': []}
    for bi, bar in enumerate(regions['top']):
        bar.update(bar_bg_color='transparent', bar_position_top='absolute', bar_sticky=True, bar_sticky_trigger_offset='60', bar_sticky_shrink='0.82', bar_sticky_slide_enabled=False,
                   bar_content_max_length='1288px', bar_outer_spacing='24px', bar_height='6.5em',
                   _label='Desktop Bar' if bi == 0 else 'Mobile Bar')
        bar['class'] = 'ed-header-bar'
        cont = bar['_modules'][0]
        cont['title'] = 'Header Content'
        cont.update(container_row_flex_justify='flex-start')
        mods = []
        for e in cont['_modules']:
            t = e['_type']
            if t == 'image': fix_logo(e); mods.append(e)
            elif t == 'nav-inline':
                e.update(menu='menu:2', title='Main Menu', menu_margin='0px 1.25em 0px auto', anchor_margin='2em 0.9em 2em 0.9em',
                  anchor_primary_font_family=FONT, anchor_primary_font_weight='500', anchor_primary_font_size='0.76em', anchor_primary_letter_spacing='0.16em',
                  anchor_primary_text_color=G('white', 0.86), anchor_primary_text_color_alt=G('white'),
                  anchor_primary_particle=True, anchor_primary_particle_color=G('accent'), anchor_primary_particle_width='100%', anchor_primary_particle_height='1px',
                  anchor_primary_particle_transform_origin='50% 50%', anchor_primary_particle_location='b_c', anchor_primary_particle_scale='scale-x',
                  dropdown_bg_color=G('slate-deep'), sub_anchor_bg_color=G('slate-deep'), sub_anchor_bg_color_alt=G('slate'),
                  sub_anchor_primary_text_color=G('white'), sub_anchor_primary_text_color_alt=G('accent'), sub_anchor_primary_font_family=FONT)
                mods.append(e)
                if bi == 0:
                    mods += [social('Facebook', 'facebook-f', '#'), social('X', 'x-twitter', '#')]
            elif t == 'nav-collapsed':
                fix_collapsed(e, 'menu:21'); mods.append(e)
            elif t == 'button':
                p = dict(BTN_BASE); p.update(BTN['light'])
                p.update(anchor_text_primary_content='Plan Your Visit', anchor_href='/plan-your-visit/', anchor_padding='1em 1.4em 1em 1.4em', anchor_primary_font_size='0.74em',
                         anchor_margin='0em 0em 0em 1.75em', title='Button – Plan Your Visit', anchor_graphic=False)
                p['class'] = 'ed-nav-cta'
                for k in [k for k in e if k.startswith('anchor_')]: del e[k]
                e.update(p); mods.append(e)
            else: mods.append(e)
        cont['_modules'] = mods
    return regions


def build_with_banner(orig, media, banner_text, banner_bar_label='Title Banner'):
    """Archive/Blog headers: same nav bars as the Main Header + a slate title banner (dynamic content)."""
    regions = build(orig, media)
    top = regions['top']
    # drop any old banner bars (bars that hold a headline), keep nav bars
    navs = [b for b in top if not any(e.get('_type') == 'headline' for e in b['_modules'][0]['_modules'])]
    for i, b in enumerate(navs):
        b['_label'] = 'Desktop Bar' if i == 0 else 'Mobile Bar'
        b['bar_z_index'] = '9999'
    banner = {'_type': 'bar', '_bp_base': '4_4', '_region': 'top', '_label': banner_bar_label, 'bar_height': 'auto',
              'bar_bg_color': G('slate-deep'), 'bar_padding': '9em 0em 4em 0em', 'bar_content_max_length': '1288px', 'bar_outer_spacing': '24px',
              'bar_box_shadow_dimensions': '!0em 0em 0em 0em', 'bar_position_top': 'relative', 'bar_z_index': '1',
              '_modules': [{'_type': 'container', '_bp_base': '4_4', '_region': 'top', 'title': 'Banner Content', 'container_flex': '1 1 auto',
                            'container_row_flex_justify': 'center',
                            '_modules': [{'_type': 'headline', '_bp_base': '4_4', '_region': 'top', 'title': 'Page Title (dynamic)',
                                          'text_content': banner_text, 'text_tag': 'h1', 'text_font_family': FONT, 'text_font_weight': '700',
                                          'text_font_size': '3.4em', 'text_line_height': '1.1', 'text_letter_spacing': '-0.022em',
                                          'text_text_color': G('white'), 'text_text_align': 'center', 'class': 'ed-archive-title',
                                          '_modules': []}]}]}
    regions['top'] = navs + [banner]
    return regions
