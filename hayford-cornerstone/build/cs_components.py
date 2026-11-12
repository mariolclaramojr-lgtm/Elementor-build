"""Reusable Cornerstone Components: Closing CTA + Service Times / Contact / Map band."""
import json, sys
SP = '/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad'
sys.path.insert(0, SP)
from hf import F, gc
from cs_home import el, bp, reveal, H, T, eyebrow, btn, div, round_icon, card_shadow, cta, times_row, MAPQ

# ---- Closing CTA (section wrapper so it can be dropped on any page)
def cta_component():
    row = json.loads(json.dumps(cta))
    row['layout_row_margin'] = '0px auto 0px auto'
    return [el('section', [row], _label='Closing CTA (component)', section_padding='0px 0px clamp(64px, 7vw, 96px) 0px',
               section_bg_color=gc('paper'))]

# ---- Service Times + Contact Information + Map (About, Plan Your Visit)
def info_line(icon, text, href=None):
    d = el('headline', text_content=text, text_tag='div', text_font_family=F['body'], text_font_weight='600',
           text_font_size='15px', text_line_height='1.4', text_text_color=gc('ink'), text_text_color_alt=gc('accent'),
           text_padding='14px 0px', text_border_width='1px 0px 0px 0px', text_border_style='solid', text_border_color=gc('line'),
           text_width='100%', text_flex_justify='flex-start',
           text_graphic=True, text_graphic_type='icon', text_graphic_icon=icon, text_graphic_icon_font_size='15px',
           text_graphic_icon_width='38px', text_graphic_icon_height='38px', text_graphic_icon_border_radius='50%',
           text_graphic_icon_bg_color=gc('paper'), text_graphic_icon_color=gc('accent'), text_graphic_margin='0px 14px 0px 0px')
    if href: d.update(text_link=True, text_href=href)
    return d

def head(title, sub, icon, dark):
    return div([div([H(title, tag='h2', size='clamp(26px, 2.4vw, 32px)', color='white' if dark else 'ink', lh='1.15', ls='-0.035em'),
                     T(sub, color='white' if dark else 'ink_soft', size='14.5px', lh='1.5', text_margin='8px 0px 0px 0px',
                       effects_opacity='0.65' if dark else '1')]),
                round_icon(icon, dark=dark)],
               layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
               layout_div_flex_align='flex-start', layout_div_width='100%', layout_div_margin='0px 0px 22px 0px')

def visit_band_component():
    def cellx(mods, label, cols, md, **kw):
        d = el('layout-cell', mods, _label=label, layout_cell_column_start=cols[0], layout_cell_column_end=cols[1],
               layout_cell_flexbox=True, layout_cell_flex_direction='column', layout_cell_border_radius='22px',
               layout_cell_overflow='hidden', **kw)
        bp(d, 'layout_cell_column_start', md=md[0], sm=1)
        bp(d, 'layout_cell_column_end', md=md[1], sm=2)
        return card_shadow('layout_cell', d)
    times = cellx([head('Service Times', "We can't wait to meet you!", 'clock', True),
                   div([times_row('Sundays', '@ 10AM'), times_row('Sunday evenings', '@ 6PM'), times_row('Wednesdays', '@ 7PM')],
                       layout_div_width='100%', layout_div_margin='auto 0px 0px 0px')],
                  'Service Times', (1, 2), (1, 2), layout_cell_bg_color=gc('ink2'), layout_cell_padding='34px')
    contact = cellx([head('Contact Information', 'Want to chat? Get in Touch!', 'envelope', False),
                     div([info_line('envelope', 'info@yourchurch.com', 'mailto:info@yourchurch.com'),
                          info_line('phone', '(555) 555-5555', 'tel:5555555555'),
                          info_line('location-dot', '1265 Lombardi Ave, Green Bay, WI 54304',
                                    f'https://www.google.com/maps/dir/?api=1&destination={MAPQ}')],
                         layout_div_width='100%', layout_div_margin='auto 0px 0px 0px')],
                    'Contact Information', (2, 3), (2, 3), layout_cell_bg_color=gc('white'), layout_cell_padding='34px')
    mapc = cellx([el('map', map_embed_code=f'<iframe title="Map to Hayford Church, 1265 Lombardi Ave, Green Bay, WI 54304" src="https://maps.google.com/maps?q={MAPQ}&z=15&output=embed" width="600" height="450" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>',
                     frame_content_sizing='fixed-height', frame_content_height='380px', _label='Map')],
                 'Map', (3, 4), (1, 3), layout_cell_bg_color=gc('sand'), layout_cell_min_height='380px')
    mapc['_modules'][0]['frame_content_height'] = '380px'
    for i, c in enumerate([times, contact, mapc]): reveal(c, i * .1)
    grid = el('layout-grid', [times, contact, mapc], _label='Visit band', layout_grid_global_container=True,
              layout_grid_template_columns='repeat(3, minmax(0, 1fr))', layout_grid_template_rows='auto',
              layout_grid_gap_column='20px', layout_grid_gap_row='20px')
    bp(grid, 'layout_grid_template_columns', md='repeat(2, minmax(0, 1fr))', sm='minmax(0, 1fr)')
    return [el('section', [grid], _label='Service Times + Contact + Map (component)',
               section_padding='clamp(72px, 8vw, 120px) 0px clamp(72px, 8vw, 120px) 0px', section_bg_color=gc('white'))]

if __name__ == '__main__':
    json.dump({'cta': cta_component(), 'visit': visit_band_component()}, open(f'{SP}/cs/components.json', 'w'), indent=1)
    print('ok')
