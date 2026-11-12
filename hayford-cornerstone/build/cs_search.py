"""Search results layout (Pro archive layout assigned to archive:search) — native elements + main-query looper."""
import json, sys, copy
SP = '/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad'
sys.path.insert(0, SP)
from hf import F, gc
from cs_home import el, bp, reveal, lift, H, T, eyebrow, btn, div, card_shadow
from cs_pages import section

SEARCH_SRC = json.load(open(f'{SP}/cs/searchmodal.json'))['_modules'][0]

def search_form(dark=True):
    s = {k: v for k, v in copy.deepcopy(SEARCH_SRC).items() if k not in ('_region', '_modules', '_id')}
    s.update(_type='search-inline', _bp_base='4_4', _label='Search form', search_base_font_size='16px',
             search_max_width='560px', search_margin='28px 0px 0px 0px', search_bg_color=gc('white'),
             search_border_radius='999px', search_box_shadow_dimensions='0px 18px 40px -18px',
             search_box_shadow_color='rgba(0, 0, 0, 0.35)', search_input_font_family=F['body'],
             search_input_font_size='16px', search_input_text_color=gc('ink_soft'), search_input_text_color_alt=gc('ink'), search_placeholder='Search sermons, events, ministries…',
             search_submit_color=gc('accent'), search_submit_color_alt=gc('accent_dark'), search_submit_font_size='1.1em',
             search_clear_color=gc('muted'))
    bp(s, 'search_max_width', sm='100%')
    return s

def has_posts(show=True):
    return [{'group': True, 'condition': 'archive:have-posts', 'value': '', 'toggle': show}]

def banner():
    crumbs = div([el('headline', text_content='Home', text_tag='div', text_font_family=F['body'], text_font_weight='700',
                     text_font_size='11px', text_letter_spacing='0.22em', text_text_transform='uppercase', text_line_height='1.4',
                     text_text_color='rgba(255, 255, 255, 0.72)', text_text_color_alt=gc('white'), text_link=True, text_href='/'),
                  eyebrow('Search', color='accent_light', margin='0px')],
                 _label='Breadcrumb', layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_align='center',
                 layout_div_flex_gap='12px', layout_div_margin='0px 0px 22px 0px')
    title = H('Search results for “{{dc:query:search_query}}”', tag='h1', size='clamp(40px, 5.4vw, 76px)', color='white', lh='1', ls='-0.045em')
    bp(title, 'text_font_size', sm='clamp(34px, 10vw, 48px)')
    col = el('layout-column', [crumbs, title, search_form()])
    row = el('layout-row', [col], layout_row_global_container=True, layout_row_layout='100%')
    s = el('section', [row], _label='1. Search banner', section_padding='clamp(160px, 24vh, 240px) 0px 64px 0px',
           section_bg_color=gc('ink'), section_bg_advanced=True, section_overflow='hidden', bg_lower_type='color',
           bg_lower_color='radial-gradient(800px 600px at 85% 0%, rgba(110, 130, 255, 0.28), rgba(110, 130, 255, 0) 70%)')
    bp(s, 'section_padding', sm='130px 0px 40px 0px')
    return s

def result_card():
    c = el('layout-cell', [
        H('{{dc:post:title}}', tag='h2', size='clamp(22px, 2vw, 28px)', lh='1.15', ls='-0.03em', text_margin='0px 0px 12px 0px'),
        T('{{dc:post:excerpt}}', size='15px', lh='1.75', text_margin='0px 0px 22px 0px'),
        el('headline', text_content='Read more', text_tag='div', text_font_family=F['body'], text_font_weight='700',
           text_font_size='11.5px', text_letter_spacing='0.14em', text_text_transform='uppercase', text_text_color=gc('accent'),
           text_graphic=True, text_graphic_type='icon', text_graphic_icon='arrow-right', text_graphic_icon_font_size='14px',
           text_graphic_icon_color=gc('accent'), text_graphic_margin='0em 0em 0em 0.6em', text_flex_direction='row-reverse',
           text_flex_justify='flex-end', text_margin='auto 0px 0px 0px')],
        _label='Result (looper consumer)', looper_consumer=True, layout_cell_tag='a', layout_cell_href='{{dc:post:permalink}}',
        layout_cell_flexbox=True, layout_cell_flex_direction='column', layout_cell_padding='30px 32px',
        layout_cell_border_radius='22px', layout_cell_bg_color=gc('white'))
    bp(c, 'layout_cell_padding', sm='26px 24px')
    return lift(card_shadow('layout_cell', c))

def results():
    count = el('headline', text_content='{{dc:query:found_posts}} results for “{{dc:query:search_query}}”', text_tag='div', text_font_family=F['body'],
               text_font_weight='700', text_font_size='11px', text_letter_spacing='0.22em', text_text_transform='uppercase',
               text_text_color=gc('muted'), text_margin='0px 0px 24px 0px')
    grid = el('layout-grid', [result_card()], _label='Results grid', layout_grid_global_container=True,
              layout_grid_template_columns='repeat(2, minmax(0, 1fr))', layout_grid_template_rows='auto',
              layout_grid_gap_column='20px', layout_grid_gap_row='20px')
    bp(grid, 'layout_grid_template_columns', md='minmax(0, 1fr)')
    head = el('layout-row', [el('layout-column', [count])], layout_row_global_container=True)
    s = section([head, grid], '2. Results (shown when the search finds something)')
    s['show_condition'] = has_posts(True)
    return s

def no_results():
    card = el('layout-column', [
        eyebrow('Nothing found'),
        H("We couldn't find a match", tag='h2', size='clamp(30px, 3.4vw, 44px)', lh='1.05', ls='-0.04em'),
        T("Try a different word or a shorter phrase — or jump to one of these popular pages.", size='16px', lh='1.75',
          text_margin='16px 0px 0px 0px', text_max_width='560px'),
        div([btn('Plan Your Visit', '/plan-your-visit/', style='dark', small=True),
             btn('Sermons', '/messages/', style='light', small=True),
             btn('Events', '/events-page/', style='light', small=True),
             btn('Get Connected', '/get-connected/', style='light', small=True)],
            _label='Popular pages', layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_wrap=True,
            layout_div_flex_gap='12px', layout_div_margin='30px 0px 0px 0px')],
        _label='No results card', layout_column_bg_color=gc('white'), layout_column_padding='clamp(30px, 4vw, 48px)',
        layout_column_border_radius='22px')
    for b in card['_modules'][3]['_modules'][1:]:
        b.update(anchor_border_width='1px', anchor_border_style='solid', anchor_border_color=gc('line'), anchor_bg_color=gc('paper'))
    row = el('layout-row', [card_shadow('layout_column', card)], layout_row_global_container=True)
    s = section([row], '2b. No results (shown when the search finds nothing)')
    s['show_condition'] = has_posts(False)
    return s

def regions():
    return {'layout': [banner(), results(), no_results()]}

if __name__ == '__main__':
    json.dump(regions(), open(f'{SP}/cs/search_layout.json', 'w'), indent=1)
    print('ok')
