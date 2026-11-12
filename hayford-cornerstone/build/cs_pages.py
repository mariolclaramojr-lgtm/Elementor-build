"""Hayford inner pages as native Cornerstone elements (same building blocks as the homepage)."""
import json, sys
SP = '/tmp/claude-0/-home-user-Elementor-build/2669057d-5450-59fa-8123-d0e8df2fda12/scratchpad'
sys.path.insert(0, SP)
from hf import F, gc
from cs_home import el, bp, reveal, lift, H, T, eyebrow, btn, div, round_icon, card_shadow

M = json.load(open(f'{SP}/cs/media.json'))
FORMS = json.load(open(f'{SP}/cs/form_ids.json'))
def img(k): return f"{M[k]['id']}:full"
VISIT_BAND = {'_type': 'global-block', 'global_block_id': '592', '_label': 'Service Times + Contact + Map (component)'}
LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sed ex at lorem dignissim consectetur. Vestibulum ullamcorper quis ipsum a tincidunt. Morbi laoreet feugiat mi, vitae commodo magna. Curabitur malesuada faucibus velit, et dapibus libero mattis ac. Donec in varius mi, quis maximus urna. Phasellus sed lorem ut mauris luctus mattis vel in dolor. Sed efficitur laoreet ante et pharetra. Quisque tempor vulputate diam, a gravida justo pharetra sit amet. Sed fringilla varius tortor, a pulvinar mi pulvinar sed.'

# ---------------------------------------------------------------- shared pieces
def banner(title, crumb, image, pos='center'):
    crumbs = div([el('headline', text_content='Home', text_tag='div', text_font_family=F['body'], text_font_weight='700',
                     text_font_size='11px', text_letter_spacing='0.22em', text_text_transform='uppercase', text_line_height='1.4',
                     text_text_color='rgba(255, 255, 255, 0.72)', text_text_color_alt=gc('white'), text_link=True, text_href='/'),
                  eyebrow(crumb, color='accent_light', margin='0px')],
                 _label='Breadcrumb', layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_align='center',
                 layout_div_flex_gap='12px', layout_div_margin='0px 0px 24px 0px')
    col = el('layout-column', [reveal(crumbs), reveal(bp(H(title, tag='h1', size='clamp(54px, 7.8vw, 116px)', color='white', lh='0.92',
                                                          ls='-0.05em'), 'text_font_size', sm='clamp(46px, 13vw, 64px)'), .1)])
    row = el('layout-row', [col], layout_row_global_container=True, layout_row_layout='100%')
    s = el('section', [row], _label='1. Banner', section_padding='clamp(170px, 30vh, 300px) 0px 68px 0px',
           section_bg_color=gc('ink'), section_bg_advanced=True, section_overflow='hidden',
           bg_lower_type='image', bg_lower_image=img(image), bg_lower_image_size='cover', bg_lower_image_position=pos,
           bg_upper_type='color',
           bg_upper_color='linear-gradient(90deg, rgba(9, 10, 13, 0.78) 0%, rgba(9, 10, 13, 0.35) 60%, rgba(9, 10, 13, 0.45) 100%), linear-gradient(0deg, rgba(9, 10, 13, 0.85) 0%, rgba(9, 10, 13, 0) 60%)')
    bp(s, 'section_padding', sm='130px 0px 40px 0px')
    return s

def section(mods, label, bg='paper', sid=None, pad='clamp(72px, 8vw, 120px) 0px clamp(72px, 8vw, 120px) 0px'):
    d = el('section', mods, _label=label, section_padding=pad,
           section_bg_color=gc({'paper': 'paper', 'white': 'white', 'dark': 'ink'}[bg]))
    if bg == 'dark':
        d.update(section_bg_advanced=True, section_overflow='hidden', bg_lower_type='color',
                 bg_lower_color='radial-gradient(640px 640px at 100% 0%, rgba(110, 130, 255, 0.16), rgba(110, 130, 255, 0) 70%)')
    if sid: d['id'] = sid
    return d

def row(cols, layout='50% 50%', gap='clamp(36px, 5.5vw, 88px)', align='center', **kw):
    r = el('layout-row', cols, layout_row_global_container=True, layout_row_layout=layout, layout_row_gap_column=gap,
           layout_row_gap_row='36px', layout_row_flex_align=align, **kw)
    bp(r, 'layout_row_layout', md='100%')
    bp(r, 'layout_row_gap_column', md='0px')
    return r

def column(mods, **kw):
    base = dict(layout_column_flexbox=True, layout_column_flex_direction='column', layout_column_flex_justify='center')
    base.update(kw)
    return el('layout-column', mods, **base)

def h2(text, dark=False, **kw):
    return H(text, tag='h2', size='clamp(38px, 4.6vw, 64px)', color='white' if dark else 'ink', lh='1', ls='-0.045em', **kw)

def body(html, dark=False, **kw):
    t = T(html if html.startswith('<') else f'<p>{html}</p>', color='white' if dark else 'ink_soft', size='16.5px', lh='1.85',
          text_margin='20px 0px 0px 0px', **kw)
    if dark: t['effects_opacity'] = '0.7'
    return t

def lead(text):
    return H(text, tag='p', size='clamp(21px, 2vw, 28px)', color='ink', lh='1.4', ls='-0.02em', weight='600')

def sec_head(eb, title, center=False, dark=False, text=None):
    mods = [eyebrow(eb, color='accent_light' if dark else 'accent'), h2(title, dark)]
    if text: mods.append(body(text, dark))
    d = div(mods, _label='Section heading', layout_div_max_width='760px', layout_div_margin='0px 0px clamp(36px, 4vw, 56px) 0px')
    if center:
        d.update(layout_div_flexbox=True, layout_div_flex_direction='column', layout_div_flex_align='center',
                 layout_div_text_align='center', layout_div_margin='0px auto clamp(36px, 4vw, 56px) auto')
        for m in mods:
            if m['_type'] == 'headline': m['text_text_align'] = 'center'; m['text_flex_justify'] = 'center'
    return reveal(d)

def media_box(image, ratio='4/3', alt='', label='Image'):
    return reveal(div([el('image', image_src=image, image_alt=alt, image_object_fit='cover', image_width='100%',
                          image_type='image', image_retina=False, image_box_shadow_dimensions='0em 0em 0em 0em')],
                      _label=label, layout_div_width='100%', layout_div_border_radius='22px', layout_div_overflow='hidden',
                      layout_div_aspect_ratio_value=ratio,
                      layout_div_box_shadow_dimensions='0px 18px 40px -18px', layout_div_box_shadow_color='rgba(14, 16, 19, 0.18)',
                      layout_div_bg_color=gc('sand'), layout_div_bg_advanced=True, bg_lower_type='image', bg_lower_image=image,
                      bg_lower_image_size='cover', bg_lower_image_position='center', layout_div_min_height='320px'))

def image_panel(image, minh='520px', label='Image', pos='center'):
    """Photo as a rounded panel (background image fills the column on every screen size)."""
    d = div([], _label=label, layout_div_width='100%', layout_div_min_height=minh, layout_div_border_radius='22px',
            layout_div_overflow='hidden', layout_div_bg_color=gc('sand'), layout_div_bg_advanced=True,
            bg_lower_type='image', bg_lower_image=image, bg_lower_image_size='cover', bg_lower_image_position=pos,
            bg_border_radius='22px', layout_div_box_shadow_dimensions='0px 18px 40px -18px',
            layout_div_box_shadow_color='rgba(14, 16, 19, 0.18)')
    bp(d, 'layout_div_min_height', md='420px', sm='320px')
    return reveal(d)

def feature_card(num, icon, title, text, dark=False, button=None, delay=0):
    top = div([H(num, tag='div', size='24px', color='white' if dark else 'muted', weight='400', ls='0em', lh='1',
                 text_font_style='italic', effects_opacity='0.55' if dark else '1'),
               round_icon(icon, dark=dark)],
              layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
              layout_div_flex_align='center', layout_div_width='100%', layout_div_margin='0px 0px 22px 0px')
    top['_modules'][0]['text_font_family'] = F['serif']
    mods = [top, H(title, tag='h3', size='24px', color='white' if dark else 'ink', lh='1.2', ls='-0.03em', text_margin='0px 0px 14px 0px'),
            T(text if text.startswith('<') else f'<p>{text}</p>', color='white' if dark else 'ink_soft', size='15.5px', lh='1.75',
              **({'effects_opacity': '0.72'} if dark else {}))]
    if button: mods.append(div([button], layout_div_margin='24px 0px 0px 0px'))
    c = el('layout-cell', mods, _label=title, layout_cell_flexbox=True, layout_cell_flex_direction='column',
           layout_cell_padding='34px', layout_cell_border_radius='22px', layout_cell_bg_color=gc('ink2' if dark else 'white'))
    bp(c, 'layout_cell_padding', sm='28px 24px')
    return reveal(lift(card_shadow('layout_cell', c)), delay)

def grid3(cells, md=2, sm=1, label='Cards'):
    g = el('layout-grid', cells, _label=label, layout_grid_global_container=True,
           layout_grid_template_columns='repeat(3, minmax(0, 1fr))', layout_grid_template_rows='auto',
           layout_grid_gap_column='20px', layout_grid_gap_row='20px')
    bp(g, 'layout_grid_template_columns', md=f'repeat({md}, minmax(0, 1fr))', sm=f'repeat({sm}, minmax(0, 1fr))' if sm > 1 else 'minmax(0, 1fr)')
    return g

def accordion(items, dark=False, first_open=True):
    fg = 'white' if dark else 'ink'
    acc = el('accordion', [el('accordion-item', accordion_item_header_content=q, accordion_item_content=a,
                              accordion_item_starts_open=(first_open and i == 0)) for i, (q, a) in enumerate(items)],
             _label='Accordion', accordion_grouped=True, accordion_item_spacing='0px', accordion_item_bg_color='transparent',
             accordion_item_border_width='1px 0px 0px 0px', accordion_item_border_style='solid',
             accordion_item_border_color=gc('line_dark' if dark else 'line'), accordion_item_border_radius='0px',
             accordion_item_box_shadow_dimensions='0em 0em 0em 0em', accordion_item_box_shadow_color='transparent',
             accordion_border_width='0px 0px 1px 0px', accordion_border_style='solid', accordion_border_color=gc('line_dark' if dark else 'line'),
             accordion_header_bg_color='transparent', accordion_header_bg_color_alt='transparent', accordion_header_padding='24px 0px',
             accordion_header_font_family=F['head'], accordion_header_font_weight='700', accordion_header_font_size='clamp(17px, 1.5vw, 20px)',
             accordion_header_letter_spacing='-0.02em', accordion_header_text_transform='none',
             accordion_header_text_color=gc(fg), accordion_header_text_color_alt=gc('accent_light' if dark else 'accent'),
             accordion_header_content_reverse=True, accordion_header_content_spacing='20px',
             accordion_header_indicator_type='icon', accordion_header_indicator_icon='plus', accordion_header_indicator_font_size='14px',
             accordion_header_indicator_width='38px', accordion_header_indicator_height='38px',
             accordion_header_indicator_rotation_start='0deg', accordion_header_indicator_rotation_end='45deg',
             accordion_header_indicator_color=gc(fg), accordion_header_indicator_color_alt=gc('accent_light' if dark else 'accent'),
             accordion_content_padding='0px 64px 28px 0px', accordion_content_border_width='0px',
             accordion_content_font_family=F['body'], accordion_content_font_size='15.5px', accordion_content_line_height='1.85',
             accordion_content_text_color='rgba(255, 255, 255, 0.68)' if dark else gc('ink_soft'))
    bp(acc, 'accordion_content_padding', sm='0px 0px 24px 0px')
    return reveal(acc, .1)

def form_card(eb, title, form_key, intro=None):
    mods = [eyebrow(eb), H(title, tag='h2', size='clamp(32px, 3.4vw, 46px)', lh='1.02', ls='-0.04em')]
    if intro: mods.append(T(f'<p>{intro}</p>', size='15.5px', lh='1.75', text_margin='14px 0px 0px 0px'))
    mods.append(div([{'_type': 'classic:gravity-forms', 'form_id': str(FORMS[form_key])}], _label='Gravity Form',
                    layout_div_margin='30px 0px 0px 0px', layout_div_width='100%'))
    c = el('layout-column', mods, _label='Form card', layout_column_bg_color=gc('white'),
           layout_column_padding='clamp(28px, 4vw, 48px)', layout_column_border_radius='22px')
    return reveal(card_shadow('layout_column', c), .1)

def shortcode(code, label):
    return el('raw-content', raw_content=code, _label=label)

# ---------------------------------------------------------------- ABOUT
def about():
    values = [('Worship & Study', 'book-open', "By reaching out to and serving those around us, we will share God's love and His message of hope with the people in our community."),
              ('Evangelism & Outreach', 'heart', 'Through weekly Bible studies, worship gatherings, and small groups, we will learn more about God and grow in our knowledge and love for Him.'),
              ('Missions & Sending', 'earth-americas', "By making disciples and supporting fellow believers as they step out to launch new churches and ministries around the world, we will expand our reach to exhibit God's love to people across the globe.")]
    beliefs = [('The Bible', "The Bible is God’s Word to all people. It was written by human authors under the supernatural guidance of the Holy Spirit. Because it was inspired by God, the Bible is truth without any mixture of error and is completely relevant to our daily lives."),
               ('The Father', "God is great: He is all powerful, all knowing, ever present, unchanging, completely worthy of our trust, and above all, Holy. It is in Him that we live, move and exist. God is good. He is our Father. He is loving, compassionate, and faithful to His people and His promises."),
               ('The Son', "Jesus Christ is completely human but, at the same time, completely God. He is the only plan for bringing people who are far from God back into a right relationship with God. He lived a perfect life, so that He could be a substitution for us in satisfying God’s demands for perfection. He defeated death in His resurrection so that we can have life."),
               ('The Holy Spirit', "The Holy Spirit’s presence assures us of our relationship with Christ. He guides believers into all truth and exalts Christ. He convicts people of their sin, God’s righteousness, and the coming judgment. He comforts us, gives us spiritual gifts, and makes us more like Christ."),
               ('Eternity', "Man was created to exist forever. He will exist either eternally separated from God by sin or in union with God through forgiveness and salvation. To be eternally separated from God is Hell. To be eternally in union with Him is Heaven. Heaven and Hell are places of eternal existence."),
               ('Man', "The Bible is God’s Word to all people. It was written by human authors under the supernatural guidance of the Holy Spirit. Because it was inspired by God, the Bible is truth without any mixture of error and is completely relevant to our daily lives."),
               ('Salvation', "God has existed in relationship with Himself for all eternity. He exists as one substance in three persons: the Father, the Son and the Holy Spirit. Although each member of the Trinity serves different functions, they each possess equal power and authority."),
               ('The Church', "The Church is a local community of believers unified through faith in Christ. It is committed to the teachings of Christ and obeying all of His commands, and it seeks to bring the Gospel to the world. The Church works together in love and unity, intent on the ultimate purpose of glorifying Christ.")]
    why = row([column([reveal(eyebrow('Our purpose')), reveal(h2('Why We Exist'), .1)], layout_column_flex_justify='flex-start'),
               column([reveal(lead('We exist to help people move from where they are to where God wants them to be.')),
                       reveal(body("We want to be a people who care for, welcome, and support those around us in a way that can only be inspired by God. It's our hope that people who visit our church or interact with our people walk away feeling encouraged, refreshed, and drawn closer to God. We want every man, woman, and child in our community to have the chance to experience and respond to the Gospel in action through our church."), .1)])],
              align='flex-start')
    vals = el('layout-row', [el('layout-column', [sec_head('What drives us', 'Our Values')])], layout_row_global_container=True,
              layout_row_margin='clamp(64px, 7vw, 104px) auto 0px auto')
    s2 = section([why, vals, grid3([feature_card(f'0{i+1}', ic, t, p, delay=i * .1) for i, (t, ic, p) in enumerate(values)], label='Values')],
                 '2. Why We Exist + Our Values')
    believe = row([column([reveal(eyebrow('Firmly rooted in Scripture', color='accent_light')), reveal(h2('What We Believe', dark=True), .1),
                           reveal(body('This is how we view God, Jesus, the Bible, man, and many significant aspects of our faith. Firmly rooted in Scripture, our beliefs guide our decisions as a church.', dark=True), .2)],
                          layout_column_flex_justify='flex-start'),
                   column([accordion(beliefs, dark=True)])], layout='42% 58%', align='flex-start')
    s3 = section([believe], '3. What We Believe', bg='dark')
    def team(i):
        c = el('layout-cell', [
            div([el('image', image_src=img('staff'), image_alt='Staff photo placeholder', image_object_fit='cover',
                    image_width='100%', image_retina=False, image_box_shadow_dimensions='0em 0em 0em 0em')],
                _label='Photo', layout_div_width='100%', layout_div_aspect_ratio_value='1/1',
                layout_div_overflow='hidden', layout_div_bg_color='rgb(242, 242, 242)'),
            div([div([H('First & Last Name', tag='h3', size='18px', lh='1.25', ls='-0.02em'),
                      el('headline', text_content='Title', text_tag='div', text_font_family=F['body'], text_font_weight='600',
                         text_font_size='13px', text_letter_spacing='0.14em', text_text_transform='uppercase',
                         text_text_color=gc('muted'), text_margin='4px 0px 0px 0px')]),
                 round_icon('envelope')],
                _label='Name + title', layout_div_flexbox=True, layout_div_flex_direction='row', layout_div_flex_justify='space-between',
                layout_div_flex_align='center', layout_div_padding='22px 24px', layout_div_width='100%')],
            _label=f'Team member {i+1}', layout_cell_border_radius='22px', layout_cell_overflow='hidden', layout_cell_bg_color=gc('white'))
        bp(c['_modules'][1], 'layout_div_padding', sm='16px')
        return reveal(lift(card_shadow('layout_cell', c)), (i % 3) * .1)
    lead_row = el('layout-row', [el('layout-column', [sec_head('Meet the team', 'Our Leadership')])], layout_row_global_container=True)
    s4 = section([lead_row, grid3([team(i) for i in range(6)], md=2, sm=2, label='Leadership')], '4. Our Leadership')
    return [banner('Who We are', 'About', 'ban_about'), s2, s3, s4, VISIT_BAND]

# ---------------------------------------------------------------- PLAN YOUR VISIT
def plan():
    video = reveal(div([el('video', video_type='player', mejs_source_files=M['visit_mp4']['url'], mejs_poster=img('visit_poster'),
                          frame_border_radius='22px', frame_bg_color=gc('ink'))],
                       _label='Welcome video', layout_div_width='100%', layout_div_border_radius='22px', layout_div_overflow='hidden',
                       layout_div_box_shadow_dimensions='0px 18px 40px -18px', layout_div_box_shadow_color='rgba(14, 16, 19, 0.25)'), .1)
    welcome = row([column([reveal(eyebrow('First time here?')), reveal(h2('Welcome to church'), .1),
                           reveal(body('We want church to be a place where your entire family is encouraged to draw closer to Christ. Visiting somewhere new can be intimidating. We want to make sure that you feel comfortable and welcome when you walk into our doors. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!'), .2),
                           reveal(div([btn("Let Us Know You're Coming", '#register-form', style='dark')], layout_div_margin='32px 0px 0px 0px'), .3)]),
                   column([video])], layout='52% 48%')
    faqs = [(q, LOREM) for q in ['What do I wear?', 'What is a typical service like?', 'How long is a typical service?',
                                 'What do you have for my kids?', 'Where do I go when I arrive?', 'Should I bring anything with me?']]
    faq = row([column([reveal(eyebrow('Good to know')), reveal(h2('Frequently Asked Questions'), .1)], layout_column_flex_justify='flex-start'),
               column([accordion(faqs)])], layout='42% 58%', align='flex-start')
    reg = row([column([image_panel(img('plan_form'), minh='640px', label='Photo')]),
               column([form_card('Plan ahead', "Let Us Know You're Coming", 'visit')])], align='stretch')
    return [banner('Plan Your Visit', 'Plan Your Visit', 'sermon3'),
            section([welcome], '2. Welcome to church'),
            section([faq], '3. Frequently Asked Questions', bg='white'),
            section([reg], "4. Let Us Know You're Coming", sid='register-form'),
            VISIT_BAND]

# ---------------------------------------------------------------- CONNECT
def connect():
    ministries = [('kids', 'Kids', 'kids', "We want church to be a place where your entire family is encouraged to draw closer to Christ—your kids included! That's why, during our Sunday morning worship services, we offer fun and engaging environments where children can learn and grow in faith as well. All our kids' programs are designed to be safe places where children in our church can learn new and exciting things about God while being led and cared for by adult volunteers from our congregation. It's our hope to encourage children to not only discover new things about God, but also begin to understand how those things matter in their own lives."),
                  ('students', 'Students', 'event2', "In student ministry, we strive to lead students to become passionate followers of Christ. By partnering with parents and trained leaders, our mission is to teach and inspire the next generation to be founded in their faith and confident in their Creator. Through regular Bible study and small group gatherings, we encourage students to walk boldly towards Christ, apply His truth to their lives, and develop strong, life-changing relationships with the God of the universe. We want our students to know Jesus so that they might be excited about sharing His name and making Him known to others. Our prayer is that the church would be the future of our world and our students, the future of the church."),
                  ('women', 'Women', 'women', "We offer several opportunities for women to get involved in ministries at our church designed to grow and strengthen their faith alongside others. It's our desire to create environments where other women in the same stages and phases of life can develop authentic relationships with one another while being encouraged to grab hold of how God's truth intersects with and impacts their lives. Be sure to check our our events page for any upcoming events!"),
                  ('men', 'Men', 'men', "Our Men's ministry programs all center on gathering as a community around the Word of God and living lives modeled after Christ. The goal of all of our Men's groups is to help challenge participants to live out their faith while impacting others with the power and truth of the Gospel.  Be sure to stay connected and visit the events page for upcoming events and meeting times.")]
    out = [banner('Take a Step', 'Connect', 'ban_connect')]
    for i, (sid, name, image, txt) in enumerate(ministries):
        r = row([column([image_panel(img(image), minh='480px', label='Photo')]),
                 column([reveal(eyebrow(f'Ministry 0{i+1} / 04')),
                         reveal(H(name, tag='h2', size='clamp(44px, 5.4vw, 76px)', lh='0.95', ls='-0.05em'), .1),
                         reveal(body(txt), .2),
                         reveal(div([btn('Get Connected', '/get-connected/', style='dark')], layout_div_margin='32px 0px 0px 0px'), .3)])],
                layout='52% 48%')
        if i % 2:
            r['layout_row_reverse'] = True
            bp(r, 'layout_row_reverse', md=False)
        out.append(section([r], f'{i+2}. {name}', bg='white' if i % 2 else 'paper', sid=sid))
    return out

# ---------------------------------------------------------------- GET CONNECTED
def get_connected():
    r = row([column([image_panel(img('connection'), minh='620px', label='Photo')]),
             column([form_card("We'd love to hear from you", 'Connection Card', 'contact',
                               intro='Thank you for connecting with us. We would love to answer any questions you may have and we have a free gift for you taking the time to give us some information.')])],
            align='stretch')
    return [banner('Get Connected', 'Get Connected', 'ban_getconnected'), section([r], '2. Connection Card')]

# ---------------------------------------------------------------- EVENTS
def events():
    card = el('layout-column', [shortcode('[MEC id="53"]', 'Modern Events Calendar — Monthly View')], _label='Calendar card',
              layout_column_bg_color=gc('white'), layout_column_padding='clamp(20px, 3vw, 36px)', layout_column_border_radius='22px')
    r = el('layout-row', [reveal(card_shadow('layout_column', card))], layout_row_global_container=True)
    return [banner("See What's Next", 'Events', 'event1'), section([r], '2. Events calendar (MEC)')]

# ---------------------------------------------------------------- GIVE
def give():
    why = row([column([reveal(eyebrow('An act of worship')), reveal(h2('Why We Give'), .1)], layout_column_flex_justify='flex-start'),
               column([reveal(lead("Giving is an an act of worship and obedience from a heart surrendered to Christ ... a choice we make to follow God's instruction for us.")),
                       reveal(body("The church doesn't need anything from you. We want something for you. God certainly doesn't need anything from us, it's all His anyway. We give out of our need to act on our faith."), .1)])],
              align='flex-start')
    ways = [feature_card('01', 'hand-holding-heart', 'Give on Sunday', 'During service, feel free to place your offering in our giving baskets as they are passed during service.'),
            feature_card('02', 'credit-card', 'Give Online', 'Using our safe, secure online giving platform, you can feel safe about your gift. Login to get started.',
                         dark=True, button=btn('Give Now', '#', small=True), delay=.1),
            feature_card('03', 'envelope', 'Give By Mail', 'Hayford Church<br>1265 Lombardi Ave<br>Green Bay, WI 54304', delay=.2)]
    head = el('layout-row', [el('layout-column', [sec_head('Choose what works for you', 'Ways to give')])], layout_row_global_container=True)
    return [banner('Live Generously', 'Give', 'ban_give'), section([why], '2. Why We Give'),
            section([head, grid3(ways, md=1, label='Ways to give')], '3. Ways to give', bg='white')]

# ---------------------------------------------------------------- SERMONS
def messages():
    r = el('layout-row', [el('layout-column', [shortcode('[smpro_archive per_page="15"]', 'Sermon Manager — archive with filters')])],
           layout_row_global_container=True, _label='Sermon archive')
    return [banner('Sermons', 'Sermons', 'sermon2'), section([r], '2. Sermon archive (Sermon Manager)')]

# ---------------------------------------------------------------- GIVE ONLINE (component) + WATCH LIVE
def give_online_component():
    r = row([column([image_panel(img('giving'), minh='460px', label='Photo')]),
             column([reveal(eyebrow('Partner with us')), reveal(h2('Give Online'), .1),
                     reveal(body("Thank you for your partnership in ministry with us. We're so grateful for the financial gifts given to allow us to continue the work of accomplishing God's mission and vision for our church. Please know your generous giving is making a difference for the glory of God at our church."), .2),
                     reveal(div([btn('Give Now', '/give/', style='dark')], layout_div_margin='32px 0px 0px 0px'), .3)])])
    return [section([r], 'Give Online (component)', bg='white')]

def watch_live(give_component_id):
    live_head = el('layout-row', [el('layout-column', [sec_head('Live stream', 'Join Us Live Sundays @ 10AM', center=True)])],
                   layout_row_global_container=True)
    vid = el('layout-row', [el('layout-column', [reveal(div([el('video', video_type='embed',
              video_embed_code='<iframe src="https://www.youtube.com/embed/4FZBkcOA6jI" title="Hayford Church live stream" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
              frame_content_sizing='aspect-ratio', frame_bg_color=gc('ink'))],
              _label='Live video', layout_div_width='100%', layout_div_border_radius='22px', layout_div_overflow='hidden',
              layout_div_box_shadow_dimensions='0px 40px 80px -40px', layout_div_box_shadow_color='rgba(14, 16, 19, 0.55)'), .1),
              reveal(div([btn('Get Connected', '/get-connected/', style='dark')], layout_div_flexbox=True, layout_div_flex_direction='row',
                         layout_div_flex_justify='center', layout_div_width='100%', layout_div_margin='32px 0px 0px 0px'), .2)])],
              layout_row_global_container=True)
    prayer = row([column([form_card('Prayer requests', 'How Can We Pray For YOU?', 'prayer')]),
                  column([image_panel(img('event4'), minh='620px', label='Photo')])], align='stretch')
    return [banner('Watch Live', 'Watch Live', 'sermon4'),
            section([live_head, vid], '2. Live stream'),
            {'_type': 'global-block', 'global_block_id': str(give_component_id), '_label': '3. Give Online (component)'},
            section([prayer], '4. Prayer request')]
