"""Inner pages (native Cornerstone elements; plugin lists via shortcodes; forms via Gravity Forms)."""
import json, os
from cs_lib import *
from home import visit_component  # noqa (component id comes from state)

MEDIA = json.load(open(os.environ['EDW_MEDIA'])); M = lambda k: MEDIA[k]
def bgimg(k): return f"{M(k)['id']}:full"
LOREM_ACC = "This is the accordion body content. It is typically best to keep this area short and to the point so it isn't too overwhelming."

# ---------------- shared pieces ----------------
def page_banner(crumb, title_, img_key, lead=None, extra=None, label_='1. Page Banner', pos='center'):
    kids = [
      div('Breadcrumb', [
        button('Crumb – Home', 'Home', '/', 'ghost', anchor_border_width='0px', anchor_padding='0em', anchor_primary_particle=False,
               anchor_primary_font_size='0.7em', anchor_primary_letter_spacing='0.24em', anchor_primary_text_color=G('white', 0.75), anchor_primary_text_color_alt=G('white')),
        el('line', 'Line', line_width='18px', line_size='1px', line_color=G('white', 0.6)),
        label('Crumb – Current', crumb, color='accent', size='0.7em'),
      ], direction='row', gap='0.7em', align='center', justify='center', **reveal(100)),
      headline('Page Title (H1)', title_, tag='h1', size='5em', color='white', lh='1.04', align='center', bp={'text_font_size': ['2.6em', '3.8em']}, **reveal(200)),
    ]
    if lead: kids.append(text('Lead', f'<p>{lead}</p>', color='on-dark', size='1.12em', align='center', max_width='52ch', **reveal(300)))
    if extra: kids += extra
    return section(label_, [row('Content', [col('Banner Text', kids, align='center', justify='flex-end', gap='1.1em',
                         layout_column_min_height='clamp(420px, 58vh, 580px)', layout_column_padding='9.5em 0em 4.5em 0em',
                         bp={'layout_column_padding': ['8em 0em 3em 0em', None], 'layout_column_min_height': ['380px', None]})])],
        padding='0px 0px 0px 0px', section_bg_advanced=True, section_bg_color=G('slate-deep'),
        bg_lower_type='image', bg_lower_image=bgimg(img_key), bg_lower_image_size='cover', bg_lower_image_position=pos,
        bg_upper_type='color', bg_upper_color=G('overlay-banner'), bp={'section_padding': ['0px 0px 0px 0px', '0px 0px 0px 0px']})

def accordion(title, items, open_first=True, columns=False):
    def item(q, a, i):
        return el('accordion-item', f'Item – {q}', _region='content', accordion_item_header_content=q, accordion_item_content=f'<p>{a}</p>',
                  accordion_item_starts_open=(open_first and i == 0))
    return el('accordion', title, [item(q, a, i) for i, (q, a) in enumerate(items)],
        accordion_width='100%', accordion_item_spacing='12px', accordion_item_bg_color=G('white'), accordion_item_border_width='1px',
        accordion_item_border_color=G('rule'), accordion_item_border_radius='12px', accordion_item_box_shadow_dimensions='0em 1.1em 2.5em -1.9em',
        accordion_item_box_shadow_color=G('slate', 0.45),
        accordion_header_bg_color='transparent', accordion_header_bg_color_alt='transparent', accordion_header_padding='1.25em 1.4em 1.25em 1.4em',
        accordion_header_font_family=FONT, accordion_header_font_weight='700', accordion_header_font_size='1.08em',
        accordion_header_text_color=G('slate'), accordion_header_text_color_alt=G('accent'),
        accordion_header_indicator=True, accordion_header_indicator_type='icon', accordion_header_indicator_icon='plus',
        accordion_header_indicator_rotation_start='0deg', accordion_header_indicator_rotation_end='45deg', accordion_header_content_reverse=True,
        accordion_header_indicator_color=G('slate'), accordion_header_indicator_color_alt=G('accent'), accordion_header_indicator_font_size='0.95em',
        accordion_content_border_width='0px', accordion_content_padding='0em 1.4em 1.35em 1.4em',
        accordion_content_font_family=FONT, accordion_content_text_color=G('text-soft'), accordion_content_line_height='1.75',
        **({'class': 'ed-acc-2col'} if columns else {}))

def gform(t, form_id):
    return el('form-integration', t, form_integration_type='gravity-forms', form_integration_gravityforms_id=str(form_id))

def form_card(t, form_id):
    return div(f'Form Box – {t}', [gform(f'Form – {t} (Gravity Forms #{form_id})', form_id)],
        layout_div_width='100%', layout_div_padding='2.4em 2.4em 2.4em 2.4em', layout_div_bg_color=G('white'), layout_div_border_radius='18px',
        layout_div_border_width='1px', layout_div_border_color=G('rule'), layout_div_box_shadow_dimensions='0em 2em 4em -2em',
        layout_div_box_shadow_color=G('slate-deep', 0.45), bp={'layout_div_padding': ['1.5em 1.3em 1.5em 1.3em', None]}, **reveal(200))

def photo(t, key, ratio='4/3.4'):
    return image(f'Photo – {t}', M(key), alt=t, ratio=ratio, radius='18px', image_box_shadow_dimensions='0em 2em 4em -2em',
                 image_box_shadow_color=G('slate-deep', 0.45), **reveal(0, zoom=True))

def split(t, media_col, text_kids, reverse=False, bg='white', layout='50% 50%'):
    cols = [col('Image', media_col, align='stretch'), col('Text', text_kids, gap='1.5em', justify='center')]
    return section(t, [row('Content', cols, layout=layout, gap='80px', layout_row_flex_align='center', layout_row_reverse=reverse,
                           bp={'layout_row_reverse': [False, False]})], bg=G(bg))

def head_center(eb, h, intro=None):
    kids = [eyebrow(eb, center=True, **reveal()), headline('Heading', h, align='center', **reveal(100))]
    if intro: kids.append(text('Intro', f'<p>{intro}</p>', align='center', max_width='46rem', **reveal(200)))
    return row('Heading', [col('Heading', kids, align='center', gap='1.1em')], layout_row_margin='0px auto 3.5em auto')

def visit(component_id, title='5. Visit Us (Component)'):
    return el('global-block', title, global_block_id=str(component_id))

# ---------------- PLAN YOUR VISIT (204) ----------------
def plan_your_visit(cid):
    faq = [(q, LOREM_ACC) for q in ['What do I wear?', 'What is a typical service like?', 'What do you have for my kids?', 'Where do I go when I arrive?']]
    video = el('video', 'Video (welcome)', video_type='player', mejs_type='video', mejs_source_files=M('hero.mp4')['url'], mejs_poster=M('visit-video-poster')['url'],
               mejs_autoplay=True, mejs_loop=True, mejs_muted=True, mejs_playsinline=True, mejs_object_fit='cover', mejs_hide_controls=True,
               frame_content_sizing='aspect-ratio', frame_content_aspect_ratio_width='16', frame_content_aspect_ratio_height='9',
               frame_border_radius='18px', frame_overflow=True, frame_bg_color=G('black'),
               frame_box_shadow_dimensions='0em 2em 4em -2em', frame_box_shadow_color=G('slate-deep', 0.45), **reveal(0, zoom=True))
    return [
      page_banner('Plan Your Visit', 'What To Expect', 'banner-visit', 'Smiling faces, a cup of coffee and a place for your whole family.', pos='50% 20%'),
      split('2. A Place For You (video + text)', [video], [
          eyebrow('Welcome', **reveal()),
          headline('Heading', 'There is a place for you here.', **reveal(100)),
          text('Text', "<p>We want church to be a place where your entire family is encouraged to draw closer to Christ. Visiting somewhere new can be intimidating. We want to make sure that you feel comfortable and welcome when you walk into our doors. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!</p>", **reveal(200)),
          button("Button – Let Us Know You're Coming", "Let Us Know You're Coming", '#coming', 'primary', arrow=True, **reveal(300))]),
      section('3. FAQs (accordion)', [row('Content', [
          col('Text', [eyebrow('FAQs', **reveal()), headline('Heading', 'Frequently Asked Questions', **reveal(100)),
                       text('Text', "<p>Still wondering about something? Send us a note and we'll be happy to help.</p>", **reveal(200)),
                       button('Button – Ask a Question', 'Ask a Question', 'mailto:info@yourchurch.com', 'outline', **reveal(300))], gap='1.5em'),
          col('Accordion', [accordion('FAQ Accordion', faq)], align='stretch', **reveal(200)),
        ], layout='36% 64%', gap='80px')], bg=G('mist')),
      section("4. Let Us Know You're Coming (form)", [row('Content', [
          col('Text', [eyebrow('First Visit', **reveal()), headline('Heading', "Let Us Know You're Coming", **reveal(100)),
                       text('Text', "<p>We can't wait to meet you! We want to make your first visit a great one, so let us know you're coming and we will:</p>", **reveal(200)),
                       text('Checklist', '<ul><li>Meet you at our Welcome Center</li><li>Help you get your kids checked into kids church</li><li>Get you a cup of coffee and some refreshments</li><li>Show you around our church building</li></ul>',
                            color='slate', **{'class': 'ed-checklist'}, **reveal(300)),
                       image('Photo – Coffee', M('coffee'), alt='Two church members talking over coffee', ratio='16/9', radius='18px', **reveal(300))], gap='1.5em', justify='center'),
          col('Form', [form_card("Let Us Know You're Coming", 3)], align='stretch'),
        ], layout='50% 50%', gap='80px', layout_row_flex_align='center')], bg=G('white'), id='coming'),
      visit(cid),
    ]

# ---------------- ABOUT (11) ----------------
def about(cid):
    values = [('Worship & Study', 'book-open', 'Through weekly Bible studies, worship gatherings, and small groups, we will learn more about God and grow in our knowledge and love for Him.'),
              ('Evangelism & Outreach', 'hand-holding-heart', "By reaching out to and serving those around us, we will share God's love and His message of hope with the people in our community."),
              ('Missions & Sending', 'globe', "By making disciples and supporting fellow believers as they step out to launch new churches and ministries around the world, we will expand our reach to exhibit God's love to people across the globe.")]
    def value_card(t, ic, d, i):
        return col(f'Card – {t}', [
            icon('Icon', ic, color='accent', size='1.5em', bg='accent', box='2.4em', icon_bg_color=G('accent', 0.12), icon_bg_color_alt=G('accent'), icon_color_alt=G('white'),
                 icon_border_radius='16px', effects_alt=True, effects_type_alt='transform', effects_transform_alt='rotate(-6deg)'),
            headline('Title', t, tag='h3', size='1.4em', lh='1.25', ls='0em', text_margin='0.4em 0em 0em 0em'),
            text('Text', f'<p>{d}</p>')], gap='0.9em', layout_column_padding='2.2em 2em 2.4em 2em', layout_column_bg_color=G('white'),
            layout_column_border_width='1px', layout_column_border_color=G('rule'), layout_column_border_color_alt='transparent', layout_column_border_radius='18px',
            layout_column_box_shadow_dimensions='0em 2em 4em -2em', layout_column_box_shadow_color='transparent', layout_column_box_shadow_color_alt=G('slate-deep', 0.45),
            layout_column_primary_particle=True, layout_column_primary_particle_location='b_c', layout_column_primary_particle_scale='scale-x',
            layout_column_primary_particle_transform_origin='0% 50%', layout_column_primary_particle_width='100%', layout_column_primary_particle_height='3px',
            layout_column_primary_particle_color=G('accent'), layout_column_overflow='hidden',
            effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -6px)', **provider(), **reveal(i * 100))
    def member(i):
        return col(f'Card – Team Member {i + 1}', [
            div('Photo (placeholder)', [icon('Placeholder', 'user', color='rule', size='7em', effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -6px) scale(1.03)')],
                align='center', justify='flex-end', layout_div_width='100%', layout_div_height='300px', layout_div_bg_color=G('white'), layout_div_border_radius='18px', layout_div_overflow='hidden',
                layout_div_padding='0em 0em 0em 0em'),
            headline('Name', 'First & Last Name', tag='h3', size='1.2em', align='center', ls='0em', text_margin='0.8em 0em 0em 0em'),
            label('Position', 'Position / Title', align='center', size='0.72em')], align='center', gap='0.35em', **provider(), **reveal((i % 3) * 100))
    beliefs = [(b, LOREM_ACC) for b in ['Jesus', 'The Bible', 'Mankind', 'Salvation', 'Sin', 'The Trinity']]
    return [
      page_banner('About', 'About Us', 'banner-about', 'Love God. Love People.'),
      section('2. Our Values', [head_center('Who We Are', 'Our Values'),
        row('Cards', [value_card(t, ic, d, i) for i, (t, ic, d) in enumerate(values)], layout='33.33% 33.33% 33.33%', gap='20px', layout_row_flex_align='stretch')], bg=G('white')),
      section('3. Our Team', [head_center('Leadership', 'Our Team'),
        row('Cards', [member(i) for i in range(6)], layout='33.33% 33.33% 33.33%', gap='24px', layout_tablet='50% 50%', layout_phone='100%')], bg=G('mist')),
      section('4. Our Beliefs (accordion)', [head_center('What We Believe', 'Our Beliefs'),
        row('Accordions', [col('Accordion – Left', [accordion('Beliefs 1–3', beliefs[:3])], align='stretch'),
                           col('Accordion – Right', [accordion('Beliefs 4–6', beliefs[3:], open_first=False)], align='stretch')],
            layout='50% 50%', gap='20px', **reveal(100))], bg=G('white')),
      visit(cid),
    ]

# ---------------- CONNECT (12) ----------------
MIN = [('kids', 'Kids', "We want church to be a place where your entire family is encouraged to draw closer to Christ—your kids included! That's why, during our Sunday morning worship services, we offer fun and engaging environments where children can learn and grow in faith as well. All our kids' programs are designed to be safe places where children in our church can learn new and exciting things about God while being led and cared for by adult volunteers from our congregation. It's our hope to encourage children to not only discover new things about God, but also begin to understand how those things matter in their own lives."),
       ('students', 'Students', "In student ministry, we strive to lead students to become passionate followers of Christ. By partnering with parents and trained leaders, our mission is to teach and inspire the next generation to be founded in their faith and confident in their Creator. Through regular Bible study and small group gatherings, we encourage students to walk boldly towards Christ, apply His truth to their lives, and develop strong, life-changing relationships with the God of the universe. We want our students to know Jesus so that they might be excited about sharing His name and making Him known to others. Our prayer is that the church would be the future of our world and our students, the future of the church."),
       ('women', 'Women', "We offer several opportunities for women to get involved in ministries at our church designed to grow and strengthen their faith alongside others. It's our desire to create environments where other women in the same stages and phases of life can develop authentic relationships with one another while being encouraged to grab hold of how God's truth intersects with and impacts their lives. Be sure to check our our events page for any upcoming events!"),
       ('men', 'Men', "Our Men's ministry programs all center on gathering as a community around the Word of God and living lives modeled after Christ. The goal of all of our Men's groups is to help challenge participants to live out their faith while impacting others with the power and truth of the Gospel. Be sure to stay connected and visit the events page for upcoming events and meeting times.")]
def connect():
    chips = [div('Jump Links', [button(f'Chip – {t}', t, f'#{k}', 'ghost', anchor_padding='0.75em 1.2em 0.75em 1.2em', anchor_border_radius='999px',
                     anchor_bg_color=G('white', 0.08), anchor_primary_font_size='0.74em', anchor_primary_particle_color=G('accent'),
                     anchor_border_color_alt=G('accent'), anchor_primary_text_color_alt=G('white'),
                     effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -2px)') for k, t, _ in MIN],
                 direction='row', wrap=True, gap='0.6em', justify='center', layout_div_margin='0.6em 0em 0em 0em', **reveal(400))]
    out = [page_banner('Connect', 'Our Ministries', 'gallery-7', 'Find your place to grow in faith alongside others.', extra=chips)]
    for i, (k, t, txt) in enumerate(MIN):
        s = split(f'{i + 2}. {t}', [photo(t, k, ratio='5/4')], [
              label('Tag', 'Ministries', size='0.7em', text_bg_color=G('accent', 0.12), text_padding='0.5em 0.9em 0.5em 0.9em', text_border_radius='999px', **reveal()),
              headline('Heading', t, **reveal(100)), text('Text', f'<p>{txt}</p>', **reveal(200)),
              button('Button – Get Connected', 'Get Connected', '/get-connected/', 'primary', arrow=True, **reveal(300))],
              reverse=bool(i % 2), bg='mist' if i % 2 else 'white')
        s['id'] = k
        out.append(s)
    return out

# ---------------- SERMONS (167) — Sermon Manager shortcode ----------------
def sermons():
    return [page_banner('Sermons', 'Sermons', 'banner-sermons', 'Watch or listen to previous messages anytime.', pos='50% 15%'),
            section('2. Sermon Archive (Sermon Manager shortcode)', [row('Content', [col('Sermons', [
                el('raw-content', 'Sermon List (shortcode)', raw_content='[smpro_archive per_page="9"]', **{'class': 'ed-sermons'})], align='stretch')])], bg=G('mist'))]

# ---------------- EVENTS (63) — Modern Events Calendar shortcode ----------------
def events():
    return [page_banner('Events', 'Events', 'gallery-4', 'There is always something happening. Come and be part of it.'),
            section('2. Calendar (MEC shortcode)', [row('Content', [col('Calendar', [
                el('raw-content', 'Calendar (MEC shortcode)', raw_content='[MEC id="52"]', **{'class': 'ed-events'})], align='stretch')])], bg=G('white'))]

# ---------------- GIVE (14) ----------------
def give():
    ways = [('Give on Sunday', 'basket-shopping', '<p>During service, feel free to place your offering in our giving baskets as they are passed during service.</p>', False, None),
            ('Give Online', 'laptop', '<p>Using our safe, secure online giving platform, you can feel safe about your gift. Login to get started.</p>', True, '#'),
            ('Give By Mail', 'envelope', '<p><strong>Edwards Church</strong><br>1234 Street<br>My Town, XX 12345</p>', False, None)]
    def way(t, ic, html, featured, href, i):
        dark = featured
        kids = [icon('Icon', ic, color='white' if dark else 'accent', size='1.5em', box='2.4em', icon_border_radius='16px',
                     icon_bg_color=G('accent') if dark else G('accent', 0.12), icon_bg_color_alt=G('accent'), icon_color_alt=G('white')),
                headline('Title', t, tag='h3', size='1.45em', color='white' if dark else 'slate', ls='0em', lh='1.25', text_margin='0.4em 0em 0em 0em'),
                text('Text', html, color='on-dark' if dark else 'text-soft')]
        if href: kids.append(button('Button – Give Now', 'Give Now', href, 'light', arrow=True, anchor_margin='0.4em 0em 0em 0em'))
        return col(f'Card – {t}', kids, gap='0.9em', layout_column_padding='2.4em 2em 2.4em 2em',
            layout_column_bg_color=G('slate') if dark else G('white'), layout_column_border_radius='18px',
            layout_column_box_shadow_dimensions='0em 2em 4em -2em', layout_column_box_shadow_color='transparent', layout_column_box_shadow_color_alt=G('slate-deep', 0.45),
            effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -6px)', **provider(), **reveal(i * 100))
    return [page_banner('Give', 'Give', 'give-wheat', 'Giving is an act of worship.'),
            split('2. Why We Give', [photo('Hands holding a young plant', 'give-plant')], [
                eyebrow('Generosity', **reveal()), headline('Heading', 'Why We Give', **reveal(100)),
                text('Text', "<p>Giving is an an act of worship and obedience from a heart surrendered to Christ. It is a choice we make to follow God's instruction for us. The church doesn't need anything from you. God wants to do something in you. God certainly doesn't need anything from us, it's all His anyway. We give out of our need to act on our faith.</p>", **reveal(200)),
                button('Button – Give Now', 'Give Now', '#give-online', 'primary', arrow=True, **reveal(300))]),
            section('3. Ways to Give', [head_center('Ways to Give', 'Ways to Give'),
                row('Cards', [way(*w, i) for i, w in enumerate(ways)], layout='33.33% 33.33% 33.33%', gap='20px', layout_row_flex_align='stretch')], bg=G('mist'), id='give-online')]

# ---------------- WATCH LIVE (221) ----------------
def watch_live():
    player = el('video', 'Live Stream (YouTube)', video_type='embed', video_embed_code='https://www.youtube.com/watch?v=4FZBkcOA6jI',
                frame_content_sizing='aspect-ratio', frame_content_aspect_ratio_width='16', frame_content_aspect_ratio_height='9',
                frame_width='100%', frame_max_width='1000px', frame_border_radius='18px', frame_overflow=True, frame_bg_color=G('black'),
                frame_margin='1.4em auto 0em auto', frame_box_shadow_dimensions='0em 2.5em 5em -1.9em', frame_box_shadow_color=G('black', 0.7), **reveal(400))
    status = label('Live Status', '● Sundays at 10am', color='white', size='0.8em', ls='0.04em', transform='none',
                   text_bg_color=G('white', 0.1), text_padding='0.6em 1.1em 0.6em 1.1em', text_border_radius='999px',
                   text_border_width='1px', text_border_color=G('white', 0.25), **reveal(300))
    return [page_banner('Watch Live', 'Watch Live', 'watch-live', extra=[status, player], label_='1. Page Banner + Live Stream'),
            split('2. Give Online', [photo('Wheat ready for harvest', 'give-harvest')], [
                eyebrow('Generosity', **reveal()), headline('Heading', 'Give Online', **reveal(100)),
                text('Text', "<p>Thank you for your partnership in ministry with us. We're so grateful for the financial gifts given to allow us to continue the work of accomplishing God's mission and vision for our church. Please know your generous giving is making a difference for the glory of God at our church.</p>", **reveal(200)),
                button('Button – Give Now', 'Give Now', '/give/', 'primary', arrow=True, **reveal(300))]),
            split('3. Let Us Pray for You (form)', [photo('Hands folded in prayer', 'gallery-5')], [
                eyebrow('Prayer', **reveal()), headline('Heading', 'Let Us Pray for You', **reveal(100)),
                form_card('Prayer Request', 7)], reverse=True, bg='mist')]

PAGES = {'plan-your-visit': (204, plan_your_visit), 'about': (11, about), 'connect': (12, connect), 'sermons': (167, sermons),
         'events': (63, events), 'give': (14, give), 'watch-live': (221, watch_live)}
