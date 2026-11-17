"""Footer Component (native elements) + the footer layout that places it site-wide."""
import json, os
from cs_lib import *
MEDIA = json.load(open(os.environ['EDW_MEDIA'])); M = lambda k: MEDIA[k]

def flink(t, href):
    p = dict(anchor_text_primary_content=t, anchor_href=href, anchor_bg_color='transparent', anchor_bg_color_alt='transparent',
             anchor_padding='0.3em 0em 0.3em 0em', anchor_border_width='0px', anchor_box_shadow_dimensions='!0em 0em 0em 0em',
             anchor_primary_font_family=FONT, anchor_primary_font_size='0.95em', anchor_primary_font_weight='400', anchor_primary_line_height='1.4',
             anchor_primary_text_color=G('on-dark'), anchor_primary_text_color_alt=G('accent'), anchor_graphic=False,
             effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0.4em, 0px)')
    return el('button', f'Link – {t}', **p)

def fcol(t, kids):
    return col(t, [label('Heading', t, size='0.68em', text_margin='0em 0em 1em 0em')] + kids, gap='0.2em')

def social(net, icon, href):
    return el('social', f'Social – {net}', anchor_graphic_icon=icon, anchor_graphic_icon_alt=icon, anchor_href=href, anchor_blank=True,
              anchor_width='2.75em', anchor_height='2.75em', anchor_bg_color='transparent', anchor_bg_color_alt=G('accent'),
              anchor_border_width='1px', anchor_border_style='solid', anchor_border_color=G('white', 0.2), anchor_border_color_alt=G('accent'),
              anchor_box_shadow_dimensions='!0em 0em 0em 0em', anchor_graphic_icon_font_size='1em',
              anchor_graphic_icon_color=G('white'), anchor_graphic_icon_color_alt=G('white'))

def plain(t, html):
    return text(t, html, color='on-dark', size='0.95em', text_line_height='1.6')

footer_component = [section('Footer', [
  row('Invitation', [
    col('Text', [
      headline('Heading', "We'd love to see you Sunday.", tag='h2', size='3em', color='white', bp={'text_font_size': ['1.9em', '2.4em']}),
      text('Text', '<p>Join us Sundays at 10am and Wednesday at 7pm.</p>', color='on-dark', size='1em'),
    ], gap='0.7em', justify='center'),
    col('Buttons', [div('Buttons', [
        button('Button – Plan Your Visit', 'Plan Your Visit', '/plan-your-visit/', 'light', arrow=True),
        button('Button – Give', 'Give', '/give/', 'ghost'),
      ], direction='row', wrap=True, gap='1em')], align='flex-end', justify='center',
      bp={'layout_column_flex_align': ['flex-start', 'flex-start']}),
  ], layout='62% 38%', gap='2em', layout_row_padding='4.5em 0em 3.5em 0em',
     layout_row_border_width='0px 0px 1px 0px', layout_row_border_color=G('white', 0.12)),
  row('Columns', [
    col('Brand', [
      image('Logo', M('logo-white'), alt='Edwards Church', radius='0px', image_styled_width='195px', image_link=True, image_href='/'),
      headline('Tagline', 'Love God. Love People.', tag='p', size='1.1em', color='white', weight='700', ls='0em', text_margin='1.4em 0em 0em 0em'),
      div('Social', [social('Facebook', 'facebook-f', '#'), social('X', 'x-twitter', '#')], direction='row', gap='0.7em', layout_div_margin='1.4em 0em 0em 0em'),
    ]),
    fcol('Visit', [flink('Plan Your Visit', '/plan-your-visit/'), flink('About', '/about/'), flink('Connect', '/connect/')]),
    fcol('Engage', [flink('Sermons', '/sermons/'), flink('Events', '/events/'), flink('Give', '/give/'), flink('Watch Live', '/watch-live/')]),
    fcol('Service Times', [plain('Times', '<p>Sundays at 10am<br>Wednesday at 7pm</p>')]),
    fcol('Contact', [plain('Address', '<p>1234 Street<br>My Town, XX 12345</p>'),
                     flink('(555) 555-5555', 'tel:5555555555'), flink('info@yourchurch.com', 'mailto:info@yourchurch.com')]),
  ], layout='26% 18.5% 18.5% 18.5% 18.5%', gap='2.5em', layout_phone='100%', layout_tablet='50% 50%', layout_row_padding='3.75em 0em 3.75em 0em'),
  row('Bottom Bar', [
    col('Copyright', [text('Copyright', '<p>&copy; 2026 Edwards Church. All rights reserved.</p>', color='on-dark', size='0.82em')]),
    col('Credit', [flink('church websites by REACHRIGHT', 'https://reachrightstudios.com')], align='flex-end',
        bp={'layout_column_flex_align': ['flex-start', 'flex-start']}),
  ], layout='50% 50%', gap='1em', container=False, layout_row_bg_color=G('black', 0.18), layout_row_padding='1.2em max(24px, calc((100% - 1240px) / 2)) 1.2em max(24px, calc((100% - 1240px) / 2))'),
], padding='0px 0px 0px 0px', section_bg_advanced=True, section_bg_color=G('slate-deep'),
   bg_lower_type='image', bg_lower_image=f"{M('footer-bg')['id']}:full", bg_lower_image_size='cover', bg_lower_image_position='center 30%',
   bg_upper_type='color', bg_upper_color=G('overlay-footer'),
   bp={'section_padding': ['0px 0px 0px 0px', '0px 0px 0px 0px']})]

def footer_regions(component_id):
    return {'footer': [{'_type': 'bar', '_region': 'footer', '_label': 'Footer', 'bar_height': 'auto', 'bar_padding': '0px',
                        'bar_bg_color': 'transparent', 'bar_content_max_length': '100%', 'bar_outer_spacing': '0px', 'bar_width': '100%',
                        'bar_box_shadow_dimensions': '!0em 0em 0em 0em',
        '_modules': [{'_type': 'container', '_region': 'footer', 'title': 'Footer Content', 'container_flex': '1 1 auto', 'container_width': '100%',
                      'container_row_flex_direction': 'column', 'container_row_flex_align': 'stretch', 'container_row_flex_justify': 'flex-start', 'container_padding': '0px',
            '_modules': [{'_type': 'global-block', '_region': 'footer', 'title': 'Footer (Component)', 'global_block_id': str(component_id)}]}]}]}
