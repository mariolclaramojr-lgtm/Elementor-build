from lc import *

ARROW = 'arrow-right'


# =============================================================== HOME
def home():
    hero_mods = [
        eyebrow('Welcome home', dark=True),
        heading("We're saving you a <em>seat.</em>", tag='h1', size='clamp(46px, 7.6vw, 96px)', color=WHITE,
                mb='28px', maxw='640px'),
        lead("Whoever you are and wherever you're coming from, there's a place for you here. Come as you are.",
             color='rgba(255, 255, 255, 0.82)', mb='40px', maxw='500px'),
        buttons(button('Plan Your Visit', '/plan-your-visit/'), button('Watch Live', '/watch-live/', 'ghost', arrow=False)),
    ]
    for i, m in enumerate(hero_mods):
        rise(m, i)

    def tcol(k, v, first=False):
        return col([label(k, color=ACCENT_LIGHT, size='11px', ls='0.22em', mb='6px'),
                    text(v, color='rgba(255, 255, 255, 0.78)', size='15px', mb='0px')],
                   layout_column_padding='26px 0px 34px 0px' if first else '26px 0px 34px 32px',
                   layout_column_border_width='0px' if first else '0px 0px 0px 1px',
                   layout_column_border_color=LINE_DARK,
                   **({} if first else bp(layout_column_padding=['18px 0px', '18px 0px', '18px 0px'],
                                          layout_column_border_width=['1px 0px 0px 0px'] * 3)))
    times = el('layout-row', [tcol('Sundays', '8:30 am &amp; 10:00 am', True), tcol('Wednesdays', '6:30 pm'),
                              tcol('Find us', '2200 Street, My Town')],
               layout_row_layout='33.33% 33.33% 33.33%', layout_row_gap_column='0px', layout_row_gap_row='0px',
               layout_row_margin='clamp(56px, 8vw, 96px) 0px 0px 0px', layout_row_border_width='1px 0px 0px 0px',
               layout_row_border_color=LINE_DARK, **bp(layout_row_layout=['100%', '100%', '100%']))
    rise(times, 4)
    hero = section([row([col(hero_mods + [times])])], video=url('hero.mp4'), poster=url('hero-poster.jpg'),
                   overlay='rgba(15, 12, 9, 0.6)', pad='clamp(220px, 26vh, 320px) 0px 0px 0px',
                   label='Hero', section_bg_color=ESP)

    welcome = section([row([
        col([framed_image('photo-1511632765486-a01980e01a18', 'Friends standing together at sunset', '4/5')],
            ),
        col([eyebrow('Welcome to Lewis Church'),
             heading('More than a place to go. A family to <em>belong</em> to.', mb='28px'),
             lead("We're a community of people who have been changed by the love of God, and we want to change our community in response."),
             text("Following the model of Jesus, it's the heart of our church to love those around us by meeting needs, sharing our lives, and offering the life-changing grace of the Christian faith."),
             el('quote', quote_content='Come to me, all you who are weary and burdened, and I will give you rest.',
                quote_cite_content='Matthew 11:28', quote_margin='16px 0px 40px 0px', quote_padding='0px 0px 0px 24px',
                quote_border_width='0px 0px 0px 2px', quote_border_style='solid', quote_border_color=ACCENT,
                quote_text_font_family=F_HEAD, quote_text_font_weight='400', quote_text_font_style='italic',
                quote_text_font_size='22px', quote_text_line_height='1.3', quote_text_text_align='left',
                quote_text_text_color=ESP, quote_marks_opening_graphic=False, quote_marks_closing_graphic=False,
                quote_cite_graphic=False, quote_cite_margin='10px 0px 0px 0px', quote_cite_font_family=F_BODY,
                quote_cite_font_weight='700', quote_cite_font_size='12px', quote_cite_letter_spacing='0.2em',
                quote_cite_text_align='left', quote_cite_text_color=ACCENT, quote_cite_flex_justify='flex-start'),
             button('Our Story', '/about/', 'dark')]),
    ], '52% 48%', md='100%', sm='100%', xs='100%', gap='clamp(48px, 8vw, 120px)', align='center')],
        label='Welcome')

    def card(title, body, more, href, pid):
        return col([
            h3(title, color=WHITE, mb='10px'),
            text(body, color='rgba(255, 255, 255, 0.8)', size='15px', lh='1.6', mb='22px', **{'class': 'lc-card-text'}),
            el('headline', text_tag='span', text_content=more, text_font_family=F_BODY, text_font_weight='700',
               text_font_size='11px', text_letter_spacing='0.2em', text_text_transform='uppercase',
               text_text_color=WHITE, text_width='100%', text_padding='16px 0px 0px 0px',
               text_border_width='1px 0px 0px 0px', text_border_color=LINE_DARK, text_flex_justify='space-between',
               text_graphic=True, text_graphic_type='icon', text_graphic_icon=ARROW, text_graphic_icon_alt=ARROW,
               text_graphic_icon_color=ACCENT_LIGHT, text_graphic_icon_font_size='16px', text_flex_direction='row-reverse',
               text_graphic_margin='0px', **{'class': 'lc-card-more'}),
        ], layout_column_tag='a', layout_column_href=href, layout_column_bg_advanced=True,
            bg_lower_type='image', bg_lower_image=url(pid), bg_upper_type='color', bg_upper_color='rgba(15, 12, 9, 0.5)',
            bg_border_radius='4px', layout_column_border_radius='4px', layout_column_overflow='hidden',
            layout_column_padding='28px', layout_column_min_height='clamp(360px, 28vw, 410px)',
            layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_justify='flex-end',
            layout_column_flex_wrap=False, layout_column_flex_align='stretch', **{'class': 'lc-card'},
            effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -4px)',
            **bp(layout_column_min_height=['300px', '340px', '360px']))

    cards = row([
        card('About Us', 'Learn who we are, our mission and vision, and meet our team.', 'Learn more', '/about/', 'photo-1529070538774-1843cb3265df'),
        card('Watch Live', "Can't make it in person? Worship with us from home.", 'Join online', '/watch-live/', 'photo-1478147427282-58a87a120781'),
        card('Events', "See what's happening at Lewis Church and stay up to date.", 'View calendar', '/events-calendar/', 'photo-1609234656388-0ff363383899'),
        card('Give', 'Your generosity helps us serve our community in many ways.', 'Give online', '/give/', 'photo-1532629345422-7515f3d16bb6'),
    ], '25% 25% 25% 25%', md='50% 50%', sm='50% 50%', xs='100%', gap='18px', **{'class': 'lc-cards'},
        css=CARDS_CSS)
    pathways = section([
        row([col([section_head('Get connected', 'Find your <em>next step.</em>',
                               "Whether you're new or have been around for years, here's where to start.")])]),
        cards], bg=LINEN, label='Pathways')

    return [hero, welcome, pathways, touch_section()]


# Element CSS (Cornerstone's per-element CSS) for the one interaction with no native control:
# on desktop the hovered card widens and the others narrow.
CARDS_CSS = """@media (min-width: 979px) {
  $el > .x-row-inner > .x-col { flex: 1 1 0; transition: flex 0.7s cubic-bezier(0.2, 0.7, 0.2, 1); }
  $el:hover > .x-row-inner > .x-col { flex-grow: 0.72; }
  $el > .x-row-inner > .x-col:hover { flex-grow: 2.4; }
  $el .lc-card-text { max-height: 7em; min-width: 240px; overflow: hidden; transition: opacity 0.35s ease, max-height 0.5s ease, margin 0.5s ease; }
  $el .lc-card-more { transition: opacity 0.35s ease; }
  $el:hover .x-col:not(:hover) .lc-card-text { opacity: 0; max-height: 0; margin-bottom: 0 !important; }
  $el:hover .x-col:not(:hover) .lc-card-more { opacity: 0; }
  $el h3 { white-space: nowrap; }
}"""




# =============================================================== ABOUT
def about():
    hero = page_hero('About us', 'Learn more about <em>Lewis Church.</em>',
                     'Who we are, what we believe, and the people who serve here.', 'photo-1519491050282-cf00c82424b4')

    video = div([
        div([], layout_div_position='absolute', layout_div_top='18px', layout_div_left='18px',
            layout_div_right='-18px', layout_div_bottom='-18px', layout_div_z_index='-1',
            layout_div_border_width='1px', layout_div_border_color=ACCENT, layout_div_border_radius='4px'),
        el('video', video_type='player', mejs_source_files=url('welcome.mp4') + "\n" + url('welcome.webm'),
           mejs_poster=url('welcome-poster.jpg'), mejs_preload='metadata', mejs_playsinline=True,
           frame_content_aspect_ratio_width='16', frame_content_aspect_ratio_height='10',
           frame_bg_color=ESP, frame_border_radius='4px', frame_overflow=True,
           mejs_controls_bg_color='rgba(31, 27, 23, 0.85)', mejs_controls_time_current_bg_color=ACCENT_LIGHT),
    ], layout_div_position='relative', layout_div_z_index='1', layout_div_width='100%',
        **bp(layout_div_margin=['0px 0px 18px 0px'] * 3, layout_div_width=['calc(100% - 18px)'] * 3))
    mission = section([row([
        col([eyebrow('Our mission &amp; vision'),
             heading('Connect people to a growing, <em>life&#8209;changing</em> relationship with Jesus.',
                     size='clamp(34px, 3.4vw, 46px)'),
             lead('Our vision is to create a church where people can experience God, connect in relationship with God and others, and respond to what God is doing.'),
             text('Press play to hear from our pastor and get a feel for a Sunday at Lewis Church before you visit.'),
             gap('16px'), button('Plan Your Visit', '/plan-your-visit/', 'dark')]),
        col([video]),
    ], '47% 53%', md='100%', sm='100%', xs='100%', gap='clamp(40px, 5vw, 72px)', align='center')],
        label='Mission & Vision')

    def value(num, title, body):
        return col([el('headline', text_tag='span', text_content=num, text_font_family=F_HEAD,
                       text_font_style='italic', text_font_size='22px', text_line_height='1.2',
                       text_text_color=ACCENT_LIGHT, text_margin='0px 0px 14px 0px'),
                    h3(title, size='32px', color=WHITE, mb='14px'),
                    text(body, color='rgba(255, 255, 255, 0.78)', mb='0px')],
                   layout_column_padding='28px 0px 0px 0px', layout_column_border_width='1px 0px 0px 0px',
                   layout_column_border_color=ACCENT_LIGHT)
    values = section([
        row([col([section_head('Our values', 'Experience. Connect. <em>Respond.</em>', dark=True)])]),
        row([value('01', 'Experience', "Experience a real God for your real life. You don't have to have it all figured out before you come to Him. God loves you right where you are, and we want our church to be a place where you truly experience His love."),
             value('02', 'Connect', 'Connect in relationship with God and others. Life is meant to be lived in close community with our Creator and the ones He created, so we help you grow closer to God and to our community of believers.'),
             value('03', 'Respond', 'Respond to what God is doing in your life by sharing with and serving others. We want our faith to show in the way we live, so we keep our eyes open for ways to serve.')],
            '33.33% 33.33% 33.33%', md='100%', sm='100%', xs='100%', gap='clamp(28px, 4vw, 56px)'),
    ], image=url('photo-1544027993-37dbfe43562a'), overlay='rgba(20, 16, 12, 0.72)', label='Values')

    def belief(t, b):
        return col([h3(t, size='24px', mb='8px'), text(b, size='16px', mb='0px')],
                   layout_column_padding='28px 0px', layout_column_border_width='1px 0px 0px 0px',
                   layout_column_border_color=LINE_LIGHT)
    beliefs = section([
        row([col([section_head('Our beliefs', 'What we <em>believe.</em>',
                               'The gospel of Christ is the hope of the world. This belief is the foundation of our church and shapes all we preach, teach, and practice.')])]),
        row([belief('The Trinity', 'In one God who exists eternally in three persons: Father, Son, and Holy Spirit.'),
             belief('Jesus', 'That Jesus is the Son of God, who took on our sins through death on a cross and rose again so that we might live eternally with God.'),
             belief('The Holy Spirit', 'That the Holy Spirit dwells in believers and empowers them to live Godly lives.'),
             belief('The Bible', 'That the Bible is the inspired word of God.'),
             belief('Prayer', 'In the power of prayer, and we encourage everyone to bring their hearts to God through prayer.'),
             belief('Salvation', 'That all people are made in the likeness of God and that salvation is available to them through Jesus.')],
            '33.33% 33.33% 33.33%', md='50% 50%', sm='50% 50%', xs='100%', gap='clamp(28px, 4vw, 56px)', rgap='0px'),
    ], label='Beliefs')

    def person(pid, alt, role):
        return col([el('image', image_src=img(pid), image_alt=alt, image_display='block', image_styled_width='100%',
                       image_object_fit='cover', image_aspect_ratio_value='4/5', image_outer_border_radius='4px',
                       image_inner_border_radius='4px', image_margin='0px 0px 20px 0px',
                       effects_filter='grayscale(0.15)', effects_alt=True, effects_type_alt='transform',
                       effects_filter_alt='grayscale(0)'),
                    h3('First &amp; Last Name', size='26px', mb='4px'), label(role)])
    team = section([
        row([col([section_head('Our team', 'Meet the <em>team.</em>',
                               'The people who lead our services, ministries and students each week.')])]),
        row([person('photo-1500648767791-00dcc994a43e', 'Portrait of the senior pastor', 'Senior Pastor'),
             person('photo-1573497019940-1c28c88b4f3e', 'Portrait of the worship director', 'Worship Director'),
             person('photo-1507003211169-0a1dd7228f2d', 'Portrait of the youth director', 'Youth Director')],
            '33.33% 33.33% 33.33%', md='50% 50%', sm='50% 50%', xs='100%', gap='clamp(20px, 3vw, 36px)'),
    ], bg=LINEN, label='Team')
    return [hero, mission, values, beliefs, team, touch_section()]


# =============================================================== CONNECT
def ministry(pid, alt, eb, title, lead_t, body, reverse=False, bg=None):
    return split(pid, alt, [eyebrow(eb), heading(title), lead(lead_t), text(body), gap('16px'),
                            button('Get Connected', '/get-connected/')], reverse=reverse, bg=bg)


def connect():
    return [
        page_hero('Connect', 'Get plugged in at <em>Lewis Church.</em>',
                  "There's a place for every age and every season of life. Find yours below.",
                  'photo-1517486808906-6ca8b3f04846'),
        ministry('photo-1488521787991-ed7bbaae773c', 'Smiling children waving at the camera', 'Lewis Kids', 'Kids',
                 "No parent looks forward to the weekly battle of getting kids to church, and none of us wants church to be a place our kids dread going. The good news is, we don't think it has to be!",
                 "By creating fun, exciting environments where kids can experience God in new ways, we'll help you avoid the Sunday morning struggle and make church a place your kids can't wait to get to each week."),
        ministry('photo-1529156069898-49953e39b3ac', 'Teenagers sitting together with arms around each other',
                 'Student ministry', 'Students',
                 "We love students. They're smart. They're funny. They're bold. And they're bursting with potential.",
                 'Middle and high school are years when students most need kindness, community and someone to walk alongside them. Both groups meet weekly for worship, teaching and small groups.',
                 reverse=True, bg=LINEN),
        ministry('photo-1491438590914-bc09fcaaf77a', 'Women laughing together', "Women's ministry", 'Women',
                 "Women's ministry is designed to make the big Sunday morning experience feel a little smaller.",
                 "Through small groups, you'll connect with others in the same season of life and form close-knit communities to navigate its ups and downs together, while growing closer to Christ."),
        ministry('photo-1523240795612-9a054b0db644', 'Men talking around a table', "Men's ministry", 'Men',
                 'By meeting together, sharing meals, studying the Word and simply doing life with one another, the men in our church have a safe place to grow.',
                 "No matter your stage or season of life, we want you to join us. We can't wait to help you connect.",
                 reverse=True, bg=LINEN),
    ]


# =============================================================== PLAN YOUR VISIT
def plan():
    faq = el('accordion', [
        el('accordion-item', accordion_item_header_content=q, accordion_item_content=a, accordion_item_starts_open=(i == 0))
        for i, (q, a) in enumerate([
            ('What should I wear?', "Whatever you're comfortable in. You'll see everything from jeans to dresses on a Sunday morning, so come as you are."),
            ('What should I expect when I arrive?', 'Our greeters will meet you at the front doors, help you find a seat and point you to the coffee bar. Services include worship music, a short welcome and a message from the Bible.'),
            ('What do you have for my kids?', 'Lewis Kids runs during both Sunday services for children from birth through 5th grade. Check-in is in the main lobby, and every volunteer is background-checked.'),
            ('How long is a service?', 'About 75 minutes, start to finish. Feel free to stay afterwards to meet people and grab another cup of coffee.'),
        ])],
        accordion_item_spacing='0px', accordion_item_bg_color='transparent', accordion_item_border_radius='0px',
        accordion_item_box_shadow_dimensions='!0em 0em 0em 0em', accordion_item_border_width='1px 0px 0px 0px',
        accordion_item_border_style='solid', accordion_item_border_color=LINE_LIGHT,
        accordion_border_width='0px 0px 1px 0px', accordion_border_style='solid', accordion_border_color=LINE_LIGHT,
        accordion_header_bg_color='transparent', accordion_header_bg_color_alt='transparent',
        accordion_header_padding='26px 0px', accordion_header_font_family=F_HEAD, accordion_header_font_weight='400',
        accordion_header_font_size='23px', accordion_header_line_height='1.3', accordion_header_text_color=ESP,
        accordion_header_text_color_alt=ACCENT, accordion_header_content_reverse=True,
        accordion_header_content_spacing='24px', accordion_header_indicator_type='icon',
        accordion_header_indicator_icon='plus', accordion_header_indicator_font_size='13px',
        accordion_header_indicator_width='34px', accordion_header_indicator_height='34px',
        accordion_header_indicator_color=ACCENT, accordion_header_indicator_color_alt=ACCENT,
        accordion_header_indicator_rotation_start='0deg', accordion_header_indicator_rotation_end='45deg',
        accordion_content_padding='0px 56px 26px 0px', accordion_content_border_width='0px',
        accordion_content_font_family=F_BODY, accordion_content_font_size='17px', accordion_content_line_height='1.75',
        accordion_content_text_color=INK_SOFT, accordion_faq_schema=True)
    faq_sec = section([row([
        col([eyebrow('Good to know'), heading('Frequently asked <em>questions.</em>'),
             lead("Still wondering about something? Call us at 111-123-4567 and we'll help.", mb='36px'),
             el('image', image_src=img('photo-1529070538774-1843cb3265df'), image_alt='People seated together during a Sunday service',
                image_display='block', image_styled_width='100%', image_object_fit='cover', image_aspect_ratio_value='4/3',
                image_outer_border_radius='4px', image_inner_border_radius='4px')]),
        col([faq]),
    ], '40% 60%', md='100%', sm='100%', xs='100%', gap='clamp(40px, 7vw, 96px)', align='flex-start')],
        bg=LINEN, label='FAQ')
    return [
        page_hero('Plan your visit', "Let's make your first visit a <em>great one.</em>",
                  'Sundays at 8:30 &amp; 10:00 am · Wednesdays at 6:30 pm', 'photo-1511895426328-dc8714191300'),
        split('photo-1495474472287-4d71bcdd2085', 'Two people sharing coffee',
              [eyebrow('Welcome home'), heading('Come as you <em>are.</em>'),
               lead('We want church to be a place where your entire family is encouraged to draw closer to Christ.'),
               text('Visiting somewhere new can be intimidating. We want you to feel comfortable and welcome when you walk through our doors. Smiling faces will greet you and show you where to go. Enjoy a cup of coffee and relax with us!', mb='0px')]),
        faq_sec,
        form_section('Plan ahead', "Let us know you're <em>coming!</em>",
                     "Tell us when you're planning to visit and we'll have someone ready to welcome you and show you around.",
                     5, 'photo-1511632765486-a01980e01a18'),
    ]


# =============================================================== WATCH LIVE
def watch():
    player = el('video', video_type='embed',
                video_embed_code='<iframe title="Lewis Church live stream" src="https://www.youtube.com/embed/4FZBkcOA6jI" loading="lazy" allow="accelerometer; autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>',
                frame_bg_color='#000000', frame_border_radius='4px', frame_overflow=True,
                frame_margin='clamp(40px, 6vw, 64px) 0px 0px 0px', frame_box_shadow_dimensions='0px 0px 0px 10px',
                frame_box_shadow_color='rgba(255, 255, 255, 0.06)')
    hero = page_hero('Watch live', 'Join us Sundays at <em>10 am.</em>',
                     'Worship with us from wherever you are. The stream starts a few minutes before service.',
                     'photo-1478147427282-58a87a120781', extra=[player], badge=True)

    def tile(title, body, href, pid):
        return col([
            div([h3(title, size='clamp(26px, 3vw, 34px)', color=WHITE, mb='6px'),
                 text(body, color='rgba(255, 255, 255, 0.8)', size='15px', mb='0px')]),
            el('icon', icon='arrow-right', icon_font_size='18px', icon_color=WHITE, icon_width='52px',
               icon_height='52px', icon_bg_color=ACCENT, icon_bg_color_alt=ACCENT_DARK, icon_border_radius='50%'),
        ], layout_column_tag='a', layout_column_href=href, layout_column_bg_advanced=True, bg_lower_type='image',
            bg_lower_image=url(pid), bg_upper_type='color', bg_upper_color='rgba(15, 12, 9, 0.55)',
            bg_border_radius='4px', layout_column_border_radius='4px', layout_column_overflow='hidden',
            layout_column_min_height='300px', layout_column_padding='clamp(28px, 4vw, 44px)',
            layout_column_flexbox=True, layout_column_flex_direction='row', layout_column_flex_wrap=False,
            layout_column_flex_justify='space-between', layout_column_flex_align='flex-end', layout_column_flex_gap='24px',
            effects_alt=True, effects_type_alt='transform', effects_transform_alt='translate(0px, -4px)')
    tiles = section([row([tile('Get Connected', 'Find a group, a class or a place to serve.', '/connect/', 'photo-1529156069898-49953e39b3ac'),
                          tile('Previous Messages', 'Missed a Sunday? Catch up on past messages.', '/messages/', 'photo-1445445290350-18a3b86e0b5a')],
                         '50% 50%', md='100%', sm='100%', xs='100%', gap='18px')], bg=LINEN, label='Next Steps')
    give = split('photo-1532629345422-7515f3d16bb6', 'Open hands holding coins and a note',
                 [eyebrow('Give online'), heading('Thank you for <em>giving.</em>'),
                  lead('None of the work we do would be possible without God moving the hearts of our people to give.'),
                  text('Your generosity helps create a church where people feel welcomed, led, and loved: a place where life-changing stories are being written every week. Thank you for giving from your heart.'),
                  gap('16px'), button('Give Now', '/give/')])
    prayer = form_section('Prayer', 'How can we pray <em>for you?</em>',
                          'Our prayer team reads every request and prays over it this week. Share as much or as little as you like.',
                          6, 'photo-1490730141103-6cac27aaab94')
    return [hero, tiles, give, prayer]


# =============================================================== GIVE
def give():
    band = section([row([col([
        eyebrow('Why we give', dark=True, center=True),
        heading('We give because He <em>first gave.</em>', color=WHITE, align='center'),
        text('We give out of obedience for what Jesus has done for us and out of love for those around us. What our offerings do for our ministry and our communities, locally and globally, is done through each one of us. Thank you for partnering with us to show the love of Christ.',
             color='rgba(255, 255, 255, 0.75)', mb='36px', maxw='40em', align='center'),
        button('Give Now', '#'),
    ], layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_align='center',
        layout_column_text_align='center')], layout_row_max_width='900px')],
        image=url('photo-1506905925346-21bda4d32df4'), overlay='rgba(20, 16, 12, 0.7)', label='Why We Give')

    P = 'clamp(28px, 3.5vw, 40px)'

    def way(pid, alt, icon, title, body, btn=None):
        mods = [el('image', image_src=img(pid, 'large'), image_alt=alt, image_display='block',
                   image_styled_width=f'calc(100% + 2 * {P})', image_styled_max_width='none', image_object_fit='cover',
                   image_aspect_ratio_value='16/10', image_margin=f'calc(-1 * {P}) calc(-1 * {P}) 28px calc(-1 * {P})'),
                el('icon', icon=icon, icon_font_size='20px', icon_color=ACCENT, icon_width='46px', icon_height='46px',
                   icon_bg_color='rgba(165, 28, 48, 0.08)', icon_border_radius='50%', icon_margin='0px 0px 22px 0px'),
                h3(title, size='28px', mb='12px'), text(body, mb='24px')]
        if btn:
            mods.append(div([btn], layout_div_margin='auto 0px 0px 0px'))
        return col(mods, layout_column_bg_color=WHITE, layout_column_padding=P, layout_column_border_radius='4px',
                   layout_column_border_width='3px 0px 0px 0px', layout_column_border_color=ACCENT,
                   layout_column_overflow='hidden', layout_column_flexbox=True,
                   layout_column_flex_direction='column', layout_column_flex_wrap=False)
    ways = section([
        row([col([section_head('Ways to give', 'Three easy ways to <em>give.</em>')])]),
        row([way('photo-1438232992991-995b7058bbb3', 'Congregation worshipping on a Sunday', 'church', 'On Sunday',
                 'During service, place your offering in the giving baskets as they are passed.'),
             way('photo-1556742049-0cfed4f6a45d', 'Giving with a phone', 'mobile-screen', 'Online',
                 'Our safe, secure online giving platform lets you give once or set up recurring gifts. Log in to get started.',
                 button('Give Now', '#')),
             way('photo-1473186505569-9c61870c11f9', 'A handwritten letter and pen', 'envelope', 'By Mail',
                 'Lewis Church<br>1000 West Highway<br>City, ST 55555')],
            '33.33% 33.33% 33.33%', md='100%', sm='100%', xs='100%', gap='18px'),
    ], bg=LINEN, label='Ways To Give')
    return [
        page_hero('Give', 'Your generosity is making a <em>difference.</em>',
                  'Thank you for partnering with us to share the love of Christ, here and around the world.',
                  'photo-1543702404-38c2035462ad'),
        split('photo-1512941937669-90a1b58e7e9c', 'A phone ready for online giving',
              [eyebrow('Live generously'), heading('Every gift tells a <em>story.</em>'),
               lead('None of the work we do at our church would be possible without God moving the hearts of our people to give.'),
               text('Your generosity helps create a church where people feel welcomed, led, and loved: a place where life-changing stories are being written every week. On behalf of those stories, thank you for giving from your heart.', mb='0px')]),
        band, ways,
    ]


# =============================================================== MESSAGES (Sermon Manager Pro shortcode)
def messages():
    return [
        page_hero('Messages', "Here's what we've been <em>talking about.</em>",
                  'Watch or listen to recent Sunday messages, or filter by speaker, series, topic or book.',
                  'photo-1504052434569-70ad5836ab65'),
        section([row([col([div([el('raw-content', raw_content='[smpro_archive]')], layout_div_width='100%', **{'class': 'lc-sermons'})],
                          layout_column_flex_align='stretch')])], bg=LINEN, label='Sermons'),
    ]


# =============================================================== EVENTS (Modern Events Calendar shortcodes)
def events():
    return [
        page_hero('Upcoming events', "Here's what's happening <em>next.</em>",
                  'Services, groups and gatherings at Lewis Church. Everyone is welcome.',
                  'photo-1609234656388-0ff363383899'),
        section([
            row([col([div([el('raw-content', raw_content='[MEC id="250"]')], layout_div_width='100%', **{'class': 'lc-mec lc-mec-month'})],
                     layout_column_flex_align='stretch')]),
            row([col([h3('Coming up', size='26px', mb='6px'),
                      text('The next few things on the calendar.', size='15px', mb='18px'),
                      div([el('raw-content', raw_content='[MEC id="252"]')], layout_div_width='100%', **{'class': 'lc-mec lc-mec-list'})],
                     layout_column_flex_align='stretch')], layout_row_margin='clamp(40px, 5vw, 64px) auto 0px auto'),
        ], bg=LINEN, label='Calendar'),
    ]


# =============================================================== GET CONNECTED
def get_connected():
    steps = [('01', 'Fill out the card', 'Tell us a little about yourself and what you are looking for.'),
             ('02', 'We reach out', 'Someone from our team will get in touch with you this week.'),
             ('03', 'Find your place', 'We will help you find a group, a class or a place to serve.')]

    def step(num, title, body):
        return col([el('headline', text_tag='span', text_content=num, text_font_family=F_HEAD,
                       text_font_style='italic', text_font_size='22px', text_line_height='1.2',
                       text_text_color=ACCENT, text_margin='0px 0px 14px 0px'),
                    h3(title, size='28px', mb='12px'), text(body, mb='0px')],
                   layout_column_padding='28px 0px 0px 0px', layout_column_border_width='1px 0px 0px 0px',
                   layout_column_border_color=ACCENT)
    how = section([
        row([col([section_head('How it works', 'Three simple <em>steps.</em>',
                               "Whether you're brand new or have been around for a while, we'd love to help you take your next step.")])]),
        row([step(*s) for s in steps], '33.33% 33.33% 33.33%', md='100%', sm='100%', xs='100%',
            gap='clamp(28px, 4vw, 56px)'),
    ], label='How It Works')
    card = form_section('Connection card', "Let's get you <em>connected.</em>",
                        'Thank you for connecting with us. We would love to answer any questions you may have, '
                        'and we have a free gift for you for taking the time to share a little about yourself.',
                        7, 'photo-1529156069898-49953e39b3ac')
    return [
        page_hero('Get connected', "We'd love to get to <em>know you.</em>",
                  "Fill out a connection card and we'll help you find your next step at Lewis Church.",
                  'photo-1517486808906-6ca8b3f04846'),
        how, card,
    ]


PAGES = {'home': home, 'about': about, 'connect': connect, 'plan': plan, 'watch': watch, 'give': give,
         'messages': messages, 'events': events, 'get_connected': get_connected}
