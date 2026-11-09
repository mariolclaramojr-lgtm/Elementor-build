import json, sys, copy
sys.path.insert(0,'.')
exec(open('build_home.py').read().split('# ---------------- 1. HERO')[0])   # reuse helpers + tokens
PAGES = [int(x) for x in sys.argv[1:]] or [412]
ASSIGN = ([{'group': True, 'condition': 'single:front-page', 'value': ''}] if 8 in PAGES else []) + \
         [{'group': True, 'condition': 'single:specific-post-of-type|page', 'value': p} for p in PAGES]

def r(e, region):
    e['_region'] = region
    for c in e.get('_modules', []): r(c, region)
    return e

brand = div('Logo', [
  div('Logo Mark', [headline('G', tag='span', size='1.6rem', color=GOLDS, font=F_ACC, weight='400', ls='0em', lh='1')],
      align='center', justify='center', layout_div_width='42px', layout_div_height='42px',
      layout_div_border_width='1px', layout_div_border_style='solid', layout_div_border_color=GOLD),
  headline('Graham', tag='span', size='1.1rem', color='#ffffff', font=F_DISP, weight='700', ls='0.24em', lh='1',
           text_text_transform='uppercase', text_subheadline=True, text_subheadline_content='Church', text_subheadline_tag='span',
           text_subheadline_spacing='0.4em', text_subheadline_font_family=F_BODY, text_subheadline_font_weight='600',
           text_subheadline_font_size='0.55rem', text_subheadline_letter_spacing='0.32em',
           text_subheadline_text_transform='uppercase', text_subheadline_text_color=GOLD),
], direction='row', gap='13px', align='center', layout_div_tag='a', layout_div_href='/')

COMP = json.load(open('components.json'))
logo_gb = lambda: {'_type': 'global-block', '_bp_base': BP, 'title': 'Logo (component)', 'global_block_id': str(COMP['logo'])}

menu = {
  '_type': 'layout-dropdown', '_bp_base': BP, '_label': 'Menu',
  'toggle_anchor_text': True, 'toggle_anchor_text_primary_content': 'Menu',
  'toggle_anchor_graphic': True, 'toggle_anchor_graphic_type': 'icon', 'toggle_anchor_graphic_icon': 'bars',
  'toggle_anchor_graphic_icon_font_size': '1.05rem', 'toggle_anchor_graphic_icon_width': '1em', 'toggle_anchor_graphic_icon_height': '1em',
  'toggle_anchor_graphic_icon_color': GOLD, 'toggle_anchor_graphic_icon_color_alt': '#ffffff',
  'toggle_anchor_graphic_icon_bg_color': 'transparent',
  'toggle_burger_size': '1px', 'toggle_burger_spacing': '3.5em', 'toggle_burger_width': '11em',
  'toggle_color': GOLD, 'toggle_color_alt': '#ffffff',
  'toggle_anchor_flex_direction': 'row-reverse', 'toggle_anchor_flex_align': 'center', 'toggle_anchor_flex_justify': 'center',
  'toggle_anchor_graphic_margin': '0em 0em 0em 0.9em', 'toggle_anchor_text_margin': '0em',
  'toggle_anchor_width': 'auto', 'toggle_anchor_height': 'auto', 'toggle_anchor_min_width': '0px', 'toggle_anchor_min_height': '46px',
  'toggle_anchor_padding': '0.95em 1.1em 0.95em 1.1em', 'toggle_anchor_bg_color': 'rgba(15,24,40,0.3)',
  'toggle_anchor_bg_color_alt': 'rgba(15,24,40,0.6)',
  'toggle_anchor_border_width': '1px', 'toggle_anchor_border_style': 'solid', 'toggle_anchor_border_color': 'rgba(198,173,122,0.7)',
  'toggle_anchor_border_color_alt': GOLD, 'toggle_anchor_border_radius': '0px', 'toggle_anchor_box_shadow_dimensions': '0em 0em 0em 0em',
  'toggle_anchor_primary_font_family': F_BODY, 'toggle_anchor_primary_font_weight': '700', 'toggle_anchor_primary_font_size': '0.65rem',
  'toggle_anchor_primary_letter_spacing': '0.18em', 'toggle_anchor_primary_text_transform': 'uppercase',
  'toggle_anchor_primary_text_color': '#ffffff', 'toggle_anchor_primary_text_color_alt': '#ffffff',
  'dropdown_toggle_trigger': 'click', 'dropdown_width': '21rem', 'dropdown_max_width': 'calc(100vw - 36px)',
  'dropdown_bg_color': DEEP, 'dropdown_padding': '0.9rem 1.6rem 1.6rem 1.6rem', 'dropdown_margin': '1rem 0em 0em 0em',
  'dropdown_border_width': '1px', 'dropdown_border_style': 'solid', 'dropdown_border_color': 'rgba(198,173,122,0.25)',
  'dropdown_box_shadow_dimensions': '0em 1.9em 4.4em -1.25em', 'dropdown_box_shadow_color': 'rgba(0,0,0,0.5)',
  'dropdown_flex_align': 'stretch',
  '_modules': [
    {'_type': 'nav-inline', '_bp_base': BP, 'menu': 'menu:2', 'menu_row_flex_direction': 'column',
     'menu_row_flex_justify': 'flex-start', 'menu_row_flex_align': 'stretch', 'menu_items_flex': '0 0 auto', 'menu_flex': '0 0 auto',
     'anchor_base_font_size': '1em', 'anchor_padding': '1em 0em 1em 0em', 'anchor_margin': '0em',
     'anchor_border_width': '0px 0px 1px 0px', 'anchor_border_style': 'solid', 'anchor_border_color': 'rgba(255,255,255,0.14)',
     'anchor_border_color_alt': 'rgba(255,255,255,0.14)', 'anchor_flex_justify': 'space-between', 'anchor_flex_align': 'center',
     'anchor_primary_font_family': F_BODY, 'anchor_primary_font_weight': '600', 'anchor_primary_font_size': '0.75rem',
     'anchor_primary_letter_spacing': '0.12em', 'anchor_primary_text_transform': 'uppercase',
     'anchor_primary_text_color': 'rgba(255,255,255,0.85)', 'anchor_primary_text_color_alt': GOLDS,
     'anchor_bg_color': 'transparent', 'anchor_bg_color_alt': 'transparent', 'anchor_text_margin': '0em',
     'anchor_sub_indicator_color': GOLD, 'anchor_sub_indicator_color_alt': GOLDS,
     'sub_anchor_primary_text_color': INK, 'sub_anchor_primary_text_color_alt': GOLDD},
    {**button('Plan Your Visit  ↗', '/plan-your-visit/', 'gold'), 'anchor_margin': '1.25rem 0px 0px 0px', 'anchor_width': '100%'},
  ]}

header_bar = r({'_type': 'bar', '_bp_base': BP, 'class': 'gc-header', 'bar_position_top': 'absolute', 'bar_height': '92px',
  'bar_bg_color': 'transparent', 'bar_box_shadow_dimensions': '0px 0px 0px 0px', 'bar_global_container': True,
  'bar_padding': '0px', 'bar_z_index': '9999', 'bar_sticky': True, 'bar_sticky_trigger_offset': '120',
  'bar_sticky_shrink': '0.82', 'bar_sticky_slide_enabled': True, 'bar_row_flex_justify': 'space-between', 'bar_row_flex_align': 'center',
  '_bp_data3_4': {'bar_height': ['76px', '76px', None, None, None]},
  '_modules': [{'_type': 'container', '_bp_base': BP, 'container_flex': '1 0 auto', 'container_row_flex_justify': 'space-between',
                'container_row_flex_align': 'center', '_modules': [logo_gb(), menu]}]}, 'top')

solid_bar = copy.deepcopy(header_bar)
solid_bar.update({'class': 'gc-header gc-header-solid', 'bar_position_top': 'relative', 'bar_bg_color': DARK,
                  'bar_box_shadow_dimensions': '0px 10px 30px -18px', 'bar_box_shadow_color': 'rgba(0,0,0,0.5)'})
header_solid = {'type': 'header', 'title': 'Graham Header – Solid (posts, events, archives)', 'regions': {'top': [solid_bar]},
                'settings': {'assignments': [{'group': True, 'condition': 'site:entire-site', 'value': ''}], 'assignment_priority': 20}}
header = {'type': 'header', 'title': 'Graham Header', 'regions': {'top': [header_bar]},
          'settings': {'assignments': ASSIGN,
                       'assignment_priority': 1}}

# ---------------- footer ----------------
def flink(label, href):
    e = text_link(label, href, color='rgba(255,255,255,0.72)', hover='#ffffff', line='transparent')
    if href.startswith('http'): e['anchor_blank'] = True
    e.update(anchor_border_width='0px', anchor_padding='0em', anchor_primary_font_size='0.85rem', anchor_primary_letter_spacing='0em',
             anchor_primary_text_transform='none', anchor_primary_font_weight='400', anchor_primary_line_height='1.6')
    return e

def social(icon, option, label):
    return {'_type': 'social', '_bp_base': BP, 'anchor_href': '{{dc:theme:' + option + '}}', 'anchor_blank': True,
            'anchor_graphic_icon': icon, 'anchor_graphic_icon_alt': icon, 'anchor_aria_label': label,
            'anchor_width': '2.6em', 'anchor_height': '2.6em', 'anchor_base_font_size': '0.85rem',
            'anchor_bg_color': 'transparent', 'anchor_bg_color_alt': GOLD, 'anchor_border_width': '1px', 'anchor_border_style': 'solid',
            'anchor_border_color': 'rgba(198,173,122,0.45)', 'anchor_border_color_alt': GOLD, 'anchor_border_radius': '100em',
            'anchor_box_shadow_dimensions': '0em 0em 0em 0em', 'anchor_graphic_icon_font_size': '1em',
            'anchor_graphic_icon_color': GOLDS, 'anchor_graphic_icon_color_alt': DARK, 'anchor_graphic_margin': '0em'}

def links(title, items):
    kids = []
    for i in items:
        if isinstance(i, tuple): kids.append(flink(*i))
        else: kids.append(text(f'<p>{i}</p>', color='rgba(255,255,255,0.72)', size='0.85rem', lh='1.6', maxw='none'))
    return div(f'Column – {title}', [
      headline(title, tag='span', size='0.65rem', color=GOLD, font=F_BODY, weight='700', ls='0.24em', lh='1',
               text_text_transform='uppercase', text_margin='0.4rem 0px 0.6rem 0px'),
    ] + kids, gap='0.7rem', layout_div_flex='1 1 10rem')

footer_main = div('Footer Columns', [
  div('Column – Brand', [logo_gb(),
     text('<p>A church for the city. Sharing the message of Christ and living out His love in our community.</p>',
          color='rgba(255,255,255,0.58)', size='0.82rem', lh='1.85', maxw='19rem', text_margin='1.4rem 0px 0px 0px'),
     div('Social', [social(i, k, t) for i, k, t in [('facebook-f', 'x_social_facebook', 'Facebook'), ('instagram', 'x_social_instagram', 'Instagram'),
                                                    ('youtube', 'x_social_youtube', 'YouTube'), ('x-twitter', 'x_social_twitter', 'X')]],
         direction='row', gap='10px', layout_div_margin='1.6rem 0px 0px 0px')],
     layout_div_flex='1.5 1 16rem'),
  links('Explore', [('About', '/about/'), ('Connect', '/connect/'), ('Sermons', '/sermon-manager/'), ('Events', '/event/')]),
  links('Gather', ['Sunday · 10 AM', 'Wednesday · 6 PM', ('Give', '/give/'), ('Plan Your Visit', '/plan-your-visit/')]),
  links('Contact', [('1000 West Highway, City, ST 55555', 'https://www.google.com/maps/search/?api=1&query=1000+West+Highway+City+ST+55555'), ('411.123.1234', 'tel:4111231234'), ('info@yourchurch.org', 'mailto:info@yourchurch.org')]),
], direction='row', gap='3rem', wrap=True, layout_div_width='100%', layout_div_padding='5.5rem 0px 4rem 0px')

footer_bottom = div('Footer Bottom', [
  text('<p>© 2026 Graham Church. All rights reserved.</p>', color='rgba(255,255,255,0.45)', size='0.7rem', maxw='none',
       text_letter_spacing='0.08em'),
  div('Credit', [
    text('<p>church web design by</p>', color='rgba(255,255,255,0.45)', size='0.7rem', maxw='none', text_letter_spacing='0.08em'),
    {**text_link('REACHRIGHT', 'https://reachrightstudios.com', color=GOLD, hover='#ffffff', line='transparent'),
     'anchor_border_width': '0px', 'anchor_padding': '0em', 'anchor_primary_font_size': '0.7rem', 'anchor_primary_letter_spacing': '0.14em',
     'anchor_blank': True},
  ], direction='row', gap='0.4rem', align='center'),
], direction='row', justify='space-between', align='center', gap='1rem', wrap=True, layout_div_width='100%',
   layout_div_padding='1.6rem 0px 2rem 0px', layout_div_border_width='1px 0px 0px 0px', layout_div_border_style='solid',
   layout_div_border_color='rgba(198,173,122,0.2)')

footer_bar = r({'_type': 'bar', '_bp_base': BP, 'bar_height': 'auto', 'bar_bg_color': DARK, 'bar_global_container': True,
  'bar_padding': '0px', 'bar_z_index': '1', 'bar_row_flex_direction': 'column', 'bar_row_flex_align': 'stretch',
  '_modules': [{'_type': 'container', '_bp_base': BP, 'container_flex': '1 0 auto', 'container_row_flex_direction': 'column',
                'container_row_flex_align': 'stretch', '_modules': [footer_main, footer_bottom]}]}, 'footer')
footer = {'type': 'footer', 'title': 'Graham Footer', 'regions': {'footer': [footer_bar]},
          'settings': {'assignments': ASSIGN,
                       'assignment_priority': 1}}

def clean(e):
    if isinstance(e, dict):
        for k in [k for k, v in e.items() if v is None]: del e[k]
        for v in e.values(): clean(v)
    elif isinstance(e, list):
        for x in e: clean(x)
clean(header); clean(footer)
footer['settings']['assignments'] = [{'group': True, 'condition': 'site:entire-site', 'value': ''}]
clean(header_solid)
json.dump({'header': header, 'footer': footer, 'header_solid': header_solid}, open('hf.json', 'w'), indent=1)
print('ok')
