"""Home page + Visit component trees (native Cornerstone elements)."""
import json, os
from cs_lib import *

MEDIA = json.load(open(os.environ['EDW_MEDIA']))
M = lambda k: MEDIA[k]
def bgimg(k): return f"{M(k)['id']}:full"

# ============ COMPONENT: Visit Us (contact details + map) ============
def info_card(t, ic, label_, value_html, delay):
    return div(f'Card – {t}', [
        icon('Icon', ic, color='accent', size='1.05em', bg='accent', box='2.6em', icon_bg_color=G('accent', 0.12), icon_bg_color_alt=G('accent'), icon_color_alt=G('white'),
             icon_box_shadow_dimensions='0em 0.4em 0.9em -0.5em', icon_box_shadow_color=G('slate', 0.35)),
        label('Label', label_, size='0.7em'),
        text('Value', value_html, color='slate', size='1.05em', text_font_weight='500', text_line_height='1.55'),
    ], gap='0.55em', layout_div_flex='1 1 calc(50% - 8px)', layout_div_padding='1.6em 1.6em 1.7em 1.6em',
       layout_div_bg_color=G('white'), layout_div_bg_color_alt=G('white'), layout_div_border_radius='18px',
       layout_div_border_width='1px', layout_div_border_color=G('rule'), layout_div_border_color_alt=G('accent', 0.45),
       layout_div_box_shadow_dimensions='0em 1.5em 2.5em -1.75em', layout_div_box_shadow_color='transparent',
       layout_div_box_shadow_color_alt=G('slate', 0.45),
       effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -4px)', **provider(), **reveal(delay),
       bp={'layout_div_flex': ['1 1 100%', None]})

MAP_EMBED = ('<iframe title="Map to Edwards Church" src="https://maps.google.com/maps?q=Franklin,+TN&z=14&output=embed" '
             'width="100%" height="100%" style="border:0;" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>')

visit_component = [section('Visit Us – Service Times, Contact + Map', [
  row('Content', [
    col('Text + Contact Details', [
      eyebrow('Get In Touch', **reveal()),
      headline('Heading', 'Join us this week', tag='h2', **reveal(100)),
      text('Intro', '<p>We can\'t wait to meet you. Here\'s everything you need for your first visit.</p>', **reveal(200)),
      div('Contact Details', [
        info_card('Service Times', 'clock', 'Service Times', '<p>Sundays at 10am<br>Wednesday at 7pm</p>', 0),
        info_card('Location', 'location-dot', 'Location', '<p>1234 Street<br>My Town, XX 12345</p>', 100),
        info_card('Email', 'envelope', 'Email', '<p><a href="mailto:info@yourchurch.com">info@yourchurch.com</a></p>', 200),
        info_card('Phone', 'phone', 'Phone', '<p><a href="tel:5555555555">(555) 555-5555</a></p>', 300),
      ], direction='row', wrap=True, gap='16px', align='stretch', layout_div_width='100%', layout_div_margin='1em 0em 0.5em 0em'),
      div('Buttons', [
        button('Button – Plan Your Visit', 'Plan Your Visit', '/plan-your-visit/', 'primary', arrow=True),
        button('Button – Get Directions', 'Get Directions', 'https://www.google.com/maps/search/?api=1&query=Franklin,+TN', 'outline', blank=True),
      ], direction='row', wrap=True, gap='1em', **reveal(200)),
    ], gap='1.6em', justify='center'),
    col('Map', [
      el('map', 'Map (Google embed)', map_type='embed', map_embed_code=MAP_EMBED, frame_content_sizing='fixed-height', frame_content_height='560px',
         frame_bg_color=G('mist'), frame_border_radius='18px', frame_overflow=True,
         frame_box_shadow_dimensions='0em 2em 4em -2em', frame_box_shadow_color=G('slate-deep', 0.45),
         bp={'frame_content_height': ['320px', '400px']}),
    ], align='stretch', justify='center', **reveal(200)),
  ], layout='50% 50%', gap='70px', layout_row_flex_align='center'),
], bg=G('soft'))]

# ============ HOME ============
def times_item(t, ic, lab, val, cls='', dark=False, grow='1'):
    return div(f'Times – {t}', [
        icon('Icon', ic, color='white', size='1.1em', bg='transparent', box='2.6em',
             icon_border_width='1px', icon_border_color=G('white', 0.4), icon_bg_color=G('white', 0.18),
             icon_bg_color_alt=G('white'), icon_color_alt=G('accent')),
        div('Text', [label('Label', lab, color='white', size='0.66em'),
                     headline('Value', val, tag='span', size='0.98em', color='white', weight='600', lh='1.3', ls='0em', **({'class': cls} if cls else {}))],
            gap='0.15em'),
    ], direction='row', gap='0.9em', align='center', layout_div_flex=f'{grow} 1 0', layout_div_padding='1.15em 1.4em 1.15em 1.4em', **provider(),
       layout_div_bg_color=G('black', 0.14) if dark else 'transparent', layout_div_bg_color_alt=G('black', 0.2),
       bp={'layout_div_flex': ['1 1 calc(50% - 1px)', '1 1 calc(50% - 1px)'], 'layout_div_padding': ['0.9em 0.6em 0.9em 0.6em', None]},
       **({'class': 'ed-next-service'} if cls else {}))

hero = section('1. Hero (video)', [
  row('Hero Content', [
    col('Content', [
      eyebrow('Love God. Love People.', center=True, **reveal(150)),
      headline('Heading (H1)', 'Where real people find Jesus.', tag='h1', size='4.4em', color='white', lh='1.08', align='center', text_max_width='780px',
               bp={'text_font_size': ['2.4em', '2.6em', '3.4em', '3.8em']}, **reveal(300)),
      div('Buttons', [
        button('Button – New Here', 'New Here?', '/plan-your-visit/', 'light', arrow=True),
        button('Button – Watch Live', 'Watch Live', '/watch-live/', 'ghost'),
      ], direction='row', wrap=True, gap='1em', justify='center', **reveal(450)),
    ], align='center', justify='center', gap='2em', layout_column_min_height='calc(100vh - 90px)', layout_column_padding='9em 0em 4em 0em',
       bp={'layout_column_min_height': ['0px', '0px'], 'layout_column_padding': ['8em 0em 3em 0em', '9em 0em 4em 0em']}),
  ]),
  row('Service Times Bar', [
    col('Bar', [
      div('Items', [
        times_item('Next Service', 'clock', 'Next Service', 'Sunday at 10am', cls='ed-next-value', dark=True, grow='1.3'),
        times_item('Sundays', 'calendar', 'Sundays', '10am Worship'),
        times_item('Wednesdays', 'calendar', 'Wednesdays', '7pm Midweek'),
        times_item('Location', 'location-dot', 'Location', '1234 Street, My Town, XX 12345', grow='1.35'),
      ], direction='row', wrap=True, gap='0px', align='stretch', layout_div_width='100%',
         layout_div_max_width='1240px', layout_div_margin='0px auto 0px auto'),
    ], align='stretch'),
  ], container=False, layout_row_bg_color=G('accent'), layout_row_width='100%'),
], padding='0px 0px 0px 0px', section_bg_advanced=True, section_bg_color=G('slate-deep'),
   bg_lower_type='video', bg_lower_video=M('hero-bw.mp4')['url'], bg_lower_video_poster=M('hero-poster')['url'],
   bg_upper_type='color', bg_upper_color=G('black', 0.55), section_z_index='1',
   bp={'section_padding': ['0px 0px 0px 0px', '0px 0px 0px 0px']})

def gimg(t, k, ratio='1/1', fill=False):
    return image(f'Photo – {t}', M(k), alt=t, ratio=ratio, radius='12px', fill=fill, link=M(k)['url'], **{'class': 'ed-lightbox'}, **reveal(0, zoom=True))

welcome = section('2. Welcome Home (gallery + text)', [
  row('Content', [
    col('Gallery (7 photos, opens full-size)', [
      div('Gallery Row 1', [
        div('Cell A', [gimg('Worship', 'gallery-1', ratio='38/39')], layout_div_flex='2 1 0'),
        div('Cell B + D', [gimg('Bible', 'gallery-2'), gimg('Praying together', 'gallery-4')], gap='10px', layout_div_flex='1 1 0'),
        div('Cell C', [gimg('Prayer during service', 'gallery-3', ratio='19/39')], layout_div_flex='1 1 0'),
      ], direction='row', gap='10px', align='stretch', layout_div_width='100%'),
      div('Gallery Row 2', [
        div('Cell E', [gimg('Hands folded in prayer', 'gallery-5')], layout_div_flex='1 1 0'),
        div('Cell F', [gimg('Embracing in prayer', 'gallery-7', ratio='2/1')], layout_div_flex='2 1 0'),
        div('Cell G', [gimg('Greeting', 'gallery-6')], layout_div_flex='1 1 0'),
      ], direction='row', gap='10px', align='stretch', layout_div_width='100%'),
    ], gap='10px', align='stretch'),
    col('Text', [
      eyebrow('Welcome Home', **reveal()),
      headline('Heading', "We are so glad you're here.", **reveal(100)),
      text('Text', '<p>We are a congregation of believers committed to sharing the message of Christ and guiding others towards faith in Him. As a church, we aim to love those in our community with the same love Christ has given to us.</p>'
                   '<p>The work of our church is aimed at directing others towards the Savior in the hopes that they will encounter the one true God and be transformed by His gracious love for them. Through all we do, say, and preach, we pray that we will shine the light of Christ to all those we encounter.</p>', **reveal(200)),
      button('Button – Plan Your Visit', 'Plan Your Visit', '/plan-your-visit/', 'primary', arrow=True, **reveal(300)),
    ], gap='1.6em', justify='center'),
  ], layout='66.66% 33.33%', gap='70px', layout_row_flex_align='center'),
], bg=G('white'))

def card(t, k, title_, line_):
    return div(f'Card – {t}', [
        headline('Title', title_, tag='h3', size='1.3em', color='white', lh='1.2', ls='0em'),
        text('Text', f'<p>{line_}</p>', color='on-dark', size='0.88em', text_line_height='1.5'),
    ], gap='0.4em', justify='flex-end', layout_div_flex='1 1 0', layout_div_height='100%', layout_div_padding='1.6em 1.5em 1.6em 1.5em',
       layout_div_border_radius='18px', layout_div_overflow='hidden', layout_div_href='/connect/',
       layout_div_bg_advanced=True, bg_lower_type='image', bg_lower_image=bgimg(k), bg_lower_image_size='cover', bg_lower_image_position='center',
       bg_upper_type='color', bg_upper_color=G('overlay-bottom'),
       layout_div_primary_particle=True, layout_div_primary_particle_location='b_c', layout_div_primary_particle_scale='scale-x',
       layout_div_primary_particle_transform_origin='0% 50%', layout_div_primary_particle_width='100%', layout_div_primary_particle_height='3px',
       layout_div_primary_particle_color=G('accent'), effects_duration='600ms',
       bp={'layout_div_flex': ['0 0 auto', None], 'layout_div_height': ['280px', None]}, **{'class': 'ed-expand-card'})

connection = section('3. Find Connection (intro + cards)', [
  row('Content', [
    col('Text', [
      eyebrow('Ministries', **reveal()),
      headline('Heading', 'Find Connection', **reveal(100)),
      text('Text', '<p>We offer several opportunities for you and your family to get involved in ministries at our church designed to grow and strengthen your faith alongside others.</p>', **reveal(200)),
      button('Button – Our Ministries', 'Our Ministries', '/connect/', 'outline', arrow=True, **reveal(300)),
    ], gap='1.6em', justify='center'),
    col('Cards (hover to expand)', [
      div('Cards', [
        card('The Word', 'ministry-word', 'The Word', "Gathered around God's Word."),
        card('Community', 'ministry-community', 'Community', 'For every stage of life.'),
        card('Discipleship', 'ministry-prayer', 'Discipleship', 'Lives modeled after Christ.'),
      ], direction='row', gap='1.25em', align='stretch', layout_div_width='100%', layout_div_height='460px',
         bp={'layout_div_flex_direction': ['column', None], 'layout_div_height': ['auto', '400px']}, **{'class': 'ed-expand-cards'}, **reveal(100)),
    ], align='stretch'),
  ], layout='31% 69%', gap='70px', layout_row_flex_align='center'),
], bg=G('mist'))

live = section('4. Watch Us Live', [
  row('Content', [
    col('Text', [
      eyebrow('Online', **reveal()),
      headline('Heading', 'Watch Us Live', color='white', **reveal(100)),
      text('Text', '<p>We want to stay connected with you! You can join us LIVE on Sundays at 10am, or you can watch or listen to previous messages anytime.</p>', color='on-dark', **reveal(200)),
      div('Buttons', [
        button('Button – Watch Live', 'Watch Live', '/watch-live/', 'light', arrow=True),
        button('Button – Previous Messages', 'Previous Messages', '/sermons/', 'ghost'),
      ], direction='row', wrap=True, gap='1em', **reveal(300)),
      div('Service Facts', [
        div('Fact – Live', [label('Label', 'Live', size='0.66em'), headline('Value', 'Sundays, 10am', tag='span', size='1.3em', color='white', weight='600', ls='0em')], gap='0.2em'),
        div('Fact – On Demand', [label('Label', 'On Demand', size='0.66em'), headline('Value', 'Watch or listen', tag='span', size='1.3em', color='white', weight='600', ls='0em')], gap='0.2em'),
      ], direction='row', gap='2.5em', layout_div_width='100%', layout_div_padding='1.6em 0em 0em 0em',
         layout_div_border_width='1px 0px 0px 0px', layout_div_border_color=G('accent', 0.28), **reveal(300)),
    ], gap='1.6em', justify='center'),
    col('Live Stream Tile', [
      div('Tile', [
        label('Badge', '● Live Stream', color='white', size='0.66em', text_bg_color=G('slate-deep', 0.7), text_padding='0.6em 0.9em 0.6em 0.9em', text_border_radius='999px'),
        div('Play', [icon('Play Icon', 'play', color='white', size='1.4em', bg='accent', box='3.4em', icon_bg_color_alt=G('white'), icon_color_alt=G('accent'),
                          effects_alt=True, effects_type_alt='transform', effects_transform_alt='scale(1.12)')],
            align='center', justify='center', layout_div_width='100%', layout_div_flex='1 1 auto'),
        div('Caption', [headline('Caption', 'Join us Sundays at 10am', tag='span', size='1.5em', color='white', weight='700', ls='0em'),
                        label('Sub', 'Previous messages anytime', size='0.66em')],
            direction='row', wrap=True, gap='1em', justify='space-between', align='flex-end', layout_div_width='100%'),
      ], gap='1em', align='flex-start', justify='space-between', layout_div_width='100%', layout_div_min_height='420px',
         layout_div_padding='2em 2.2em 2em 2.2em', layout_div_border_radius='18px', layout_div_overflow='hidden', layout_div_href='/watch-live/',
         layout_div_bg_advanced=True, bg_lower_type='image', bg_lower_image=bgimg('watch-live'), bg_lower_image_size='cover',
         bg_upper_type='color', bg_upper_color=G('overlay-tile'),
         layout_div_box_shadow_dimensions='0em 2.5em 5em -1.9em', layout_div_box_shadow_color=G('black', 0.7),
         effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -4px)', **provider(),
         bp={'layout_div_min_height': ['300px', None], 'layout_div_padding': ['1.3em 1.3em 1.3em 1.3em', None]}, **reveal(200)),
    ], align='stretch'),
  ], layout='44.44% 55.56%', gap='70px', layout_row_flex_align='center'),
], section_bg_advanced=True, section_bg_color=G('slate-deep'),
   bg_lower_type='image', bg_lower_image=bgimg('live-bg'), bg_lower_image_size='cover', bg_lower_image_position='center',
   bg_upper_type='color', bg_upper_color=G('overlay-left'))

def home_tree(visit_component_id):
    visit = el('global-block', '5. Visit Us (Component)', global_block_id=str(visit_component_id))
    return [hero, welcome, connection, live, visit]
