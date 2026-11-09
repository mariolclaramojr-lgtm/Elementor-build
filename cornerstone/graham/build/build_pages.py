import json, re, copy, sys
exec(open('build_home.py').read().split('# ---------------- 1. HERO')[0])
HOME = json.load(open('home-tree-new.json'))
GET_IN_TOUCH = HOME[4]          # identical content on About / Plan Your Visit
def P(pid): return json.load(open([f for f in __import__('glob').glob(f'pages/{pid}-*.json')][0]))['tree']
def find_all(e, t, out=None):
    out = [] if out is None else out
    if e.get('_type') == t: out.append(e)
    for c in e.get('_modules', []) or e.get('elements', []) or []: find_all(c, t, out)
    return out
def orig(e):  # copy an original element (forms, video, raw content) without its old ids
    e = copy.deepcopy(e); e.pop('_id', None); e.pop('_region', None); return e
def strip_p(s): return re.sub(r'^\s*<p>(.*?)</p>\s*$', r'\1', s.strip(), flags=re.S).replace('<br />\n', ' ').replace('<br />', ' ')

LIGHT_TEXT = 'rgba(255,255,255,0.75)'
def gold_rule(): return el('line', None, [], line_width='48px', line_size='1px', line_color=GOLD, line_margin='1.4rem 0px 1.6rem 0px')

def banner(title, eyebrow_txt='Graham Church', sub=None, image='373:full', overlay='rgba(15, 24, 40, 0.7)', body=None):
    kids = [eyebrow(eyebrow_txt, GOLD),
            headline(title, tag='h1', size='clamp(3rem, 6.5vw, 5.5rem)', color='#ffffff', ls='-0.05em', lh='0.98', margin='1.5rem 0px 0px 0px')]
    if sub: kids.append(text(f'<p>{sub}</p>', color='rgba(255,255,255,0.8)', size='1.1rem', lh='1.7', text_margin='1.25rem 0px 0px 0px'))
    if body: kids.append(text(body, color='rgba(255,255,255,0.8)', size='1.02rem', lh='1.85', maxw='40rem', text_margin='1.4rem 0px 0px 0px'))
    return section('1. Page Banner', [row('Content', [col('Text', kids)])],
        section_padding='13rem 0px 6.5rem 0px', **{'_bp_data3_4': {'section_padding': ['9.5rem 0px 4.5rem 0px', None, '11rem 0px 5.5rem 0px', None, None]}},
        section_bg_advanced=True, bg_border_radius='inherit', bg_lower_type='image', bg_lower_image=image,
        bg_lower_image_size='cover', bg_lower_image_position='center', bg_lower_image_repeat='no-repeat',
        bg_upper_type='color', bg_upper_color=overlay, section_bg_color=DARK)

def media_frame(image, minh='32rem', label=None):
    kids = [headline(label, tag='span', size='0.65rem', color='#ffffff', font=F_BODY, weight='700', ls='0.22em', lh='1.2',
                     text_text_transform='uppercase')] if label else []
    return div('Image Frame', kids, layout_div_width='100%', layout_div_min_height=minh, layout_div_padding='1.6rem',
               layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.35)',
               **bgimg('layout_div', image, 'rgba(15, 24, 40, 0.08)'), **bp(layout_div_min_height=['22rem', '26rem', None, None, None]))

def boxed(elem):  # frame for a video / embed
    return div('Media Frame', [elem], layout_div_width='100%', layout_div_bg_color=DARK,
               layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.35)')

def text_block(title, html, buttons=(), dark=False, tag='h2', extra=()):
    kids = [headline(title, tag=tag, color='#ffffff' if dark else INK), gold_rule(),
            text(html, color=LIGHT_TEXT if dark else MUTED, maxw='34rem')]
    kids += list(extra)
    if buttons:
        kids.append(div('Buttons', [button(l, h, ('gold' if dark else 'navy') if i == 0 else ('ghost' if dark else 'outline'))
                                    for i, (l, h) in enumerate(buttons)], direction='row', gap='12px', wrap=True,
                        layout_div_margin='2rem 0px 0px 0px'))
    return kids

def split(title_lbl, media, kids, dark=False, reverse=False, bg=None, image_bg=None):
    cols = [col('Media', [media]), col('Text', kids)]
    if reverse: cols = cols[::-1]
    lay = '48% 52%' if not reverse else '52% 48%'
    kw = dict(section_bg_color=bg or (DARK if dark else IVORY))
    if image_bg:
        kw.update(section_bg_advanced=True, bg_border_radius='inherit', bg_lower_type='image', bg_lower_image=image_bg,
                  bg_lower_image_size='cover', bg_lower_image_position='center', bg_lower_image_repeat='no-repeat',
                  bg_upper_type='color', bg_upper_color='rgba(15, 24, 40, 0.86)')
    r = row('Content', cols, layout=lay, gap='5.5rem', align='center',
            **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None], 'layout_row_gap_column': [None, None, '3rem', '4rem', None],
                               'layout_row_reverse': [reverse, reverse, reverse, None, None] if reverse else [None]*5}})
    if reverse:  # keep the image first when stacked
        r['_bp_data3_4']['layout_row_reverse'] = [True, True, True, None, None]
    return section(title_lbl, [r], **kw)

def heading_row(title, intro=None, dark=False, center=False):
    left = col('Heading Group', [headline(title, color='#ffffff' if dark else INK), gold_rule()])
    cols = [left]
    if intro: cols.append(col('Intro', [text(f'<p>{intro}</p>', color=LIGHT_TEXT if dark else MUTED, size='0.95rem', maxw='25rem')], layout_column_flex_justify='flex-end'))
    return row('Heading', cols, layout='60% 40%' if intro else '100%', gap='3rem', align='flex-end', layout_row_margin='0px auto 2.5rem auto')

def icon_card(icon, title, html, btn=None, dark_section=False):
    bg, tcol, bcol, icol, ibg = (('#ffffff', NAVY, MUTED, NAVY, IVORY) if not dark_section else
                                 (DEEP, '#ffffff', LIGHT_TEXT, GOLD, 'rgba(198,173,122,0.14)'))
    kids = [el('icon', None, [], icon=icon, icon_font_size='1.35rem', icon_width='3.4rem', icon_height='3.4rem',
               icon_color=icol, icon_bg_color=ibg, icon_border_radius='50%'),
            headline(title, tag='h3', size='1.35rem', color=tcol, weight='700', ls='-0.02em', lh='1.2', margin='1.6rem 0px 0.75rem 0px'),
            text(html, color=bcol, size='0.92rem', maxw='none')]
    if btn: kids.append(div('Buttons', [text_link(btn[0] + '  →', btn[1], color='#ffffff' if dark_section else NAVY, hover=GOLDS if dark_section else GOLDD)],
                            layout_div_margin='1.5rem 0px 0px 0px'))
    return col(f'Card – {title}', kids, layout_column_bg_color=bg, layout_column_padding='2.4rem 2.2rem 2.3rem 2.2rem',
               layout_column_border_width='1px', layout_column_border_style='solid',
               layout_column_border_color='rgba(36,52,77,0.14)' if not dark_section else 'rgba(198,173,122,0.18)', **hover_lift)

def cards_row(cards, n=3):
    return row('Cards', cards, layout=' '.join([f'{100/n:.4g}%'] * n), gap='1.4rem',
               **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%' if n > 2 else None, None, None]}})

def dark_bg(image='373:full', overlay='rgba(15, 24, 40, 0.86)'):
    return dict(section_bg_advanced=True, bg_border_radius='inherit', bg_lower_type='image', bg_lower_image=image,
                bg_lower_image_size='cover', bg_lower_image_position='center', bg_lower_image_repeat='no-repeat',
                bg_upper_type='color', bg_upper_color=overlay, section_bg_color=DARK)

def faq_accordion(items):
    acc = el('accordion', None, [el('accordion-item', None, [], accordion_item_header_content=h) for h in items],
             accordion_margin='0em', accordion_padding='0em', accordion_border_width='0px', accordion_border_style='none',
             accordion_border_radius='0px', accordion_box_shadow_dimensions='0em 0em 0em 0em',
             accordion_item_bg_color='transparent', accordion_item_padding='0em', accordion_item_border_width='0px 0px 1px 0px',
             accordion_item_border_style='solid', accordion_item_border_color='rgba(255,255,255,0.16)',
             accordion_item_box_shadow_dimensions='0em 0em 0em 0em',
             accordion_header_bg_color='transparent', accordion_header_bg_color_alt='transparent',
             accordion_header_padding='1.4em 0em 1.4em 0em', accordion_header_margin='0em', accordion_header_border_width='0px',
             accordion_header_border_style='none', accordion_header_box_shadow_dimensions='0em 0em 0em 0em',
             accordion_header_font_family=F_DISP, accordion_header_font_weight='500', accordion_header_font_size='1.2rem',
             accordion_header_text_color='#ffffff', accordion_header_text_color_alt=GOLDS,
             accordion_header_indicator_type='icon', accordion_header_indicator_icon='plus', accordion_header_indicator_font_size='1rem',
             accordion_header_indicator_color=GOLD, accordion_header_indicator_color_alt=GOLDS, accordion_header_content_spacing='1em',
             accordion_header_text_shadow_dimensions='0px 0px 0px',
             accordion_content_text_color=LIGHT_TEXT, accordion_content_padding='0em 0em 1.4em 0em', accordion_content_margin='0em',
             accordion_content_border_width='0px', accordion_content_box_shadow_dimensions='0em 0em 0em 0em')
    return acc

def form_box(title, form_el, intro_html=None, dark=False):
    kids = [headline(title, color='#ffffff' if dark else INK), gold_rule()]
    if intro_html: kids.append(text(intro_html, color=LIGHT_TEXT if dark else MUTED, maxw='34rem', text_margin='0px 0px 1.5rem 0px'))
    kids.append(div('Form Box', [orig(form_el)], layout_div_width='100%'))
    return kids

def raw_section(title_lbl, raw_el, eyebrow_txt=None, title=None, intro=None):
    rows = []
    if title:
        cols = [col('Heading Group', [eyebrow(eyebrow_txt), headline(title, margin='1.4rem 0px 0px 0px')])]
        if intro: cols.append(col('Intro', [text(f'<p>{intro}</p>', size='0.95rem', maxw='25rem')], layout_column_flex_justify='flex-end'))
        rows.append(row('Heading', cols, layout='60% 40%' if intro else '100%', gap='3rem', align='flex-end',
                        layout_row_margin='0px auto 3rem auto'))
    rows.append(row('Content', [col('Plugin Output', [orig(raw_el)], layout_column_flex_align='stretch')]))
    return section(title_lbl, rows, section_bg_color=PAPER)

def relabel(sec, title): s = copy.deepcopy(sec); s['title'] = title; return s

# ===================================== PAGES =====================================
def about():
    t = P(11); s1, s2 = t[1], t[2]
    mission = find_all(s1, 'text')[0]['text_content']
    vals = [(c['_modules'][0]['icon'], find_all(c, 'headline')[0]['text_content'], find_all(c, 'text')[0]['text_content'])
            for c in s1['_modules'][1]['_modules']]
    team = [(find_all(c, 'image')[0]['image_src'], find_all(c, 'headline')[0]) for c in s2['_modules'][1]['_modules']]
    sec2 = section('2. Mission & Values', [
        row('Mission', [col('Heading Group', [headline('Our Mission'), gold_rule()]),
                        col('Text', [div('Photo', [media_frame('461:full', minh='19rem')], layout_div_width='100%',
                                         **bp(layout_div_width=['100%', None, None, None, None])),
                                     text(mission, color=INK, size='1.15rem', lh='1.75', maxw='40rem', text_margin='1.75rem 0px 0px 0px')],
                            layout_column_flex_align='stretch')],
            layout='40% 60%', gap='4rem', align='flex-start', layout_row_margin='0px auto 4.5rem auto'),
        row('Values Heading', [col('Heading Group', [headline('Our Values'), gold_rule()])], layout_row_margin='0px auto 1rem auto'),
        cards_row([icon_card(i, h, x) for i, h, x in vals]),
    ], section_bg_color=IVORY)
    team_cols = [col(f'Card – Team {n+1}', [
        div('Photo', [], layout_div_width='100%', layout_div_min_height='22rem', **bgimg('layout_div', img_src, 'rgba(15,24,40,0.05)')),
        label_head(h['text_content'], h.get('text_subheadline_content', ''), pcolor='#ffffff', psize='1.2rem', tag='h3',
                   text_font_family=F_DISP, text_font_weight='600', text_margin='1.25rem 0px 0px 0px'),
    ], **hover_lift) for n, (img_src, h) in enumerate(team)]
    team_row = cards_row(team_cols); team_row['_bp_data3_4']['layout_row_layout'] = ['100%', '100%', '33.33% 33.33% 33.33%', None, None]
    sec3 = section('3. Our Team', [heading_row('Our Team', dark=True), team_row], **dark_bg('451:full'))
    return [banner('About Us', image='450:full'), sec2, sec3, relabel(GET_IN_TOUCH, '4. Get In Touch (component)')]

def connect_page():
    t = P(12); out = [banner('Connect', image='446:full')]
    for n, s in enumerate(t[1:], start=2):
        img_src = find_all(s, 'image')[0]['image_src']; h = find_all(s, 'headline')[0]['text_content']
        body = find_all(s, 'text')[0]['text_content']; b = find_all(s, 'button')[0]
        dark = n % 2 == 1
        out.append(split(f'{n}. {h}', media_frame(img_src),
                         text_block(h, body, [(b['anchor_text_primary_content'], b['anchor_href'])], dark=dark),
                         dark=dark, reverse=dark, image_bg={3: '456:full', 5: '443:full'}.get(n) if dark else None))
    return out

def gold_frame(inner, title='Video Frame'):
    return div(title, [div('Player', [inner], layout_div_width='100%', layout_div_bg_color=DARK,
                           layout_div_box_shadow_dimensions='0em 2.5em 5em -1.9em', layout_div_box_shadow_color='rgba(15,24,40,0.5)')],
               layout_div_width='100%', layout_div_padding='14px', layout_div_border_width='1px', layout_div_border_style='solid',
               layout_div_border_color='rgba(198,173,122,0.55)', layout_div_bg_color='rgba(255,255,255,0.4)',
               **bp(layout_div_padding=['8px', None, None, None, None]))

def checklist(items):
    return div('Checklist', [div(f'Item – {i[:24]}', [
        el('icon', None, [], icon='check', icon_font_size='0.8rem', icon_width='1.9rem', icon_height='1.9rem',
           icon_color=DARK, icon_bg_color=GOLD, icon_border_radius='50%'),
        text(f'<p>{i}</p>', color=INK, size='0.98rem', lh='1.5', maxw='none', layout_div_flex=None)],
        direction='row', gap='0.9rem', align='center', layout_div_width='100%', layout_div_padding='0.85rem 0px 0.85rem 0px',
        layout_div_border_width='0px 0px 1px 0px', layout_div_border_style='solid', layout_div_border_color='rgba(36,52,77,0.12)')
        for i in items], layout_div_width='100%', layout_div_margin='1.25rem 0px 0px 0px',
        layout_div_border_width='1px 0px 0px 0px', layout_div_border_style='solid', layout_div_border_color='rgba(36,52,77,0.12)')

def plan_visit():
    t = P(272)
    vid = find_all(t[1], 'video')[0]; h = find_all(t[1], 'headline')[0]['text_content']; body = find_all(t[1], 'text')[0]['text_content']
    b = find_all(t[1], 'button')[0]
    intro = re.search(r'<p>(.*?)</p>', body, re.S).group(1)
    items = [re.sub(r'\s+', ' ', x).strip() for x in re.findall(r'<li>(.*?)</li>', body, re.S)]
    faqs = [i['accordion_item_header_content'] for i in find_all(t[2], 'accordion-item')]
    form = find_all(t[3], 'classic:gravity-forms')[0]
    kids = [headline(h, color=INK), gold_rule(), text(f'<p>{intro}</p>', maxw='34rem'), checklist(items),
            div('Buttons', [button(b['anchor_text_primary_content'] + '  ↗', b['anchor_href'], 'navy')], layout_div_margin='2rem 0px 0px 0px')]
    sec2 = split('2. Thinking About Visiting', gold_frame(orig(vid)), kids)
    sec3 = section('3. FAQs', [heading_row('Faqs', dark=True),
                               row('Accordion', [col('Accordion', [faq_accordion(faqs[:2])], layout_column_flex_align='stretch'),
                                                 col('Accordion', [faq_accordion(faqs[2:])], layout_column_flex_align='stretch')],
                                   layout='50% 50%', gap='3rem')], **dark_bg('452:full'))
    form_title = find_all(t[3], 'headline')[0]['text_content']
    sec4 = section('4. Let Us Know (form)', [row('Content', [
        col('Heading Group', [eyebrow('Plan ahead'), headline(form_title, margin='1.4rem 0px 0px 0px'), gold_rule(),
                              text("<p>Tell us when you're planning to visit and we'll be ready to welcome you.</p>", maxw='24rem')]),
        col('Form', [div('Form Box', [orig(form)], layout_div_width='100%', layout_div_bg_color='#ffffff',
                         layout_div_padding='2.5rem 2.5rem 2.5rem 2.5rem', layout_div_border_width='2px 0px 0px 0px',
                         layout_div_border_style='solid', layout_div_border_color=GOLD,
                         layout_div_box_shadow_dimensions='0em 1.9em 4em -1.9em', layout_div_box_shadow_color='rgba(15,24,40,0.3)',
                         **bp(layout_div_padding=['1.6rem 1.4rem 1.8rem 1.4rem', None, None, None, None]))], layout_column_flex_align='stretch'),
    ], layout='40% 60%', gap='4.5rem', align='flex-start',
       **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None], 'layout_row_gap_column': [None, None, '2.5rem', None, None]}})],
       section_bg_color=SAND)
    return [banner('Plan Your Visit', image='462:full'), sec2, sec3, sec4, relabel(GET_IN_TOUCH, '5. Get In Touch (component)')]

def give():
    t = P(14); s1, s2 = t[1], t[2]
    hs = find_all(s1, 'headline'); ts = find_all(s1, 'text'); b = find_all(s1, 'button')[0]
    sec2 = section('2. Live Generously', [row('Content', [
        col('Live Generously', [headline(hs[0]['text_content']), gold_rule(), text(ts[0]['text_content'], color=INK, size='1.1rem', lh='1.75')]),
        col('Why We Give', [headline(hs[1]['text_content']), gold_rule(), text(ts[1]['text_content']),
                            div('Buttons', [button(b['anchor_text_primary_content'], b.get('anchor_href') or '#', 'navy')], layout_div_margin='2rem 0px 0px 0px')]),
    ], layout='50% 50%', gap='5rem', align='flex-start')], section_bg_color=IVORY)
    cards = []
    for c in s2['_modules'][1]['_modules']:
        btn = find_all(c, 'button')
        cards.append(icon_card(c['_modules'][0]['icon'], find_all(c, 'headline')[0]['text_content'], find_all(c, 'text')[0]['text_content'],
                               (btn[0]['anchor_text_primary_content'], btn[0].get('anchor_href') or '#') if btn else None, dark_section=True))
    sec3 = section('3. Ways to Give', [heading_row('Ways to Give', dark=True), cards_row(cards)], **dark_bg('467:full'))
    return [banner('Giving', image='445:full'), sec2, sec3]

def watch_live():
    t = P(307)
    h = find_all(t[1], 'headline')[0]['text_content']; b = find_all(t[1], 'button')[0]
    M2 = json.load(open('graham-media.json'))
    vid = orig(find_all(P(272)[1], 'video')[0])          # the site's own video player element
    vid.update(mejs_source_files=M2['wlvideo']['url'], mejs_poster=M2['wlposter']['url'], frame_bg_color=DARK)
    player = div('Video Frame', [div('Player', [vid], layout_div_width='100%', layout_div_bg_color=DARK,
                                     layout_div_box_shadow_dimensions='0em 2.5em 5em -1.9em', layout_div_box_shadow_color='rgba(15,24,40,0.5)')],
                 layout_div_width='100%', layout_div_padding='14px', layout_div_border_width='1px', layout_div_border_style='solid',
                 layout_div_border_color='rgba(198,173,122,0.55)', layout_div_bg_color='rgba(255,255,255,0.4)',
                 **bp(layout_div_padding=['8px', None, None, None, None]))
    live = headline('Live Sundays · 10 AM', tag='span', size='0.62rem', color=GOLDD, font=F_BODY, weight='700', ls='0.2em', lh='1',
                    text_text_transform='uppercase', text_padding='0.7em 1em 0.7em 1em', text_border_width='1px',
                    text_border_style='solid', text_border_color='rgba(163,133,78,0.45)')
    strip_item = lambda t_, s_, link=None, first=False: div(t_, [label_head(s_, t_, pcolor=INK, scolor=GOLDD, psize='1rem', link=link)],
        layout_div_flex='1 1 12rem', layout_div_padding='0px' if first else '0px 0px 0px 1.75rem',
        layout_div_border_width='0px' if first else '0px 0px 0px 1px', layout_div_border_style='solid', layout_div_border_color='rgba(36,52,77,0.14)',
        **bp(layout_div_padding=['0px', None, None, None, None], layout_div_border_width=['0px', None, None, None, None]))
    sec2 = section('2. Watch Live (video)', [
        row('Heading', [
            col('Heading Group', [live, headline(h, margin='1.5rem 0px 0px 0px'), gold_rule()]),
            col('Buttons', [div('Buttons', [button(b['anchor_text_primary_content'] + '  →', b['anchor_href'], 'navy')])],
                layout_column_flex_justify='flex-end', layout_column_flex_align='flex-end',
                **bp(layout_column_flex_align=['flex-start', 'flex-start', 'flex-start', None, None])),
        ], layout='65% 35%', gap='3rem', align='flex-end', layout_row_margin='0px auto 2.25rem auto'),
        row('Video', [col('Video', [player], layout_column_flex_align='stretch')]),
        row('Service Times', [col('Strip', [div('Service Times', [
            strip_item('Sunday Service', 'Sunday Morning · 10 AM', first=True),
            strip_item('Midweek Gathering', 'Wednesday · 6 PM'),
            strip_item('Missed a Sunday?', 'Previous Sermons  ↗', link='/sermon-manager/'),
        ], direction='row', gap='1.25rem', wrap=True, layout_div_width='100%', layout_div_padding='1.75rem 0px 0px 0px',
           **bp(layout_div_flex_direction=['column', None, None, None, None]))], layout_column_flex_align='stretch')],
            layout_row_margin='1.5rem auto 0px auto'),
    ], section_bg_color=IVORY)
    g = t[2]; gh = find_all(g, 'headline')[0]['text_content']; gt = find_all(g, 'text')[0]['text_content']; gb = find_all(g, 'button')[0]
    sec3 = split('3. Give', media_frame(find_all(g, 'image')[0]['image_src']),
                 text_block(gh, gt, [(gb['anchor_text_primary_content'], gb['anchor_href'])], dark=True), dark=True, reverse=True, image_bg='465:full')
    p_ = t[3]
    sec4 = split('4. Prayer (form)', media_frame(find_all(p_, 'image')[0]['image_src']),
                 form_box(find_all(p_, 'headline')[0]['text_content'], find_all(p_, 'classic:gravity-forms')[0]), bg=PAPER)
    return [banner('Watch Live', image='453:full'), sec2, sec3, sec4]

def form_card(form_el):
    return div('Form Box', [orig(form_el)], layout_div_width='100%', layout_div_bg_color='#ffffff',
               layout_div_padding='2.5rem 2.5rem 2.5rem 2.5rem', layout_div_border_width='2px 0px 0px 0px',
               layout_div_border_style='solid', layout_div_border_color=GOLD,
               layout_div_box_shadow_dimensions='0em 1.9em 4em -1.9em', layout_div_box_shadow_color='rgba(15,24,40,0.3)',
               **bp(layout_div_padding=['1.6rem 1.4rem 1.8rem 1.4rem', None, None, None, None]))

def get_connected():
    t = P(345); s = t[1]
    title = find_all(s, 'headline')[0]['text_content'].strip()
    intro = re.sub(r'</?span>', '', find_all(s, 'text')[0]['text_content']).replace('\u00a0', ' ').strip()
    gift = div('Gift Card', [
        el('icon', None, [], icon='gift', icon_font_size='1.1rem', icon_width='2.75rem', icon_height='2.75rem',
           icon_color=DARK, icon_bg_color=GOLD, icon_border_radius='50%'),
        headline('A free gift for you', tag='p', size='1.35rem', color='#ffffff', font=F_ACC, weight='400', ls='0em', lh='1.25',
                 text_font_style='italic', text_margin='1rem 0px 0px 0px', text_subheadline=True,
                 text_subheadline_content='When you fill out the connect card', text_subheadline_tag='span', text_subheadline_spacing='0.6em',
                 text_subheadline_font_family=F_BODY, text_subheadline_font_weight='700', text_subheadline_font_size='0.62rem',
                 text_subheadline_letter_spacing='0.2em', text_subheadline_text_transform='uppercase', text_subheadline_text_color=GOLD),
    ], layout_div_bg_color=DEEP, layout_div_max_width='17rem', layout_div_padding='1.6rem 1.75rem 1.6rem 1.75rem',
       layout_div_margin='-6rem -1.5rem 0px auto', layout_div_border_width='2px 0px 0px 0px', layout_div_border_style='solid',
       layout_div_border_color=GOLD, layout_div_z_index='2',
       layout_div_box_shadow_dimensions='0em 1.9em 4.4em -1.25em', layout_div_box_shadow_color='rgba(15,24,40,0.4)',
       **bp(layout_div_margin=['-3rem 1rem 0px 1rem', '-4rem 1.5rem 0px auto', None, None, None]))
    sec2 = section('2. Connect Card (form)', [row('Content', [
        col('Text', [eyebrow('We would love to meet you'), headline(title, margin='1.4rem 0px 0px 0px'), gold_rule(),
                     text(f'<p>{intro}</p>', color=INK, size='1.05rem', lh='1.75', maxw='30rem'),
                     div('Image', [media_frame('464:full', minh='22rem'), gift], layout_div_width='100%', layout_div_margin='2.5rem 0px 0px 0px')]),
        col('Form', [form_card(find_all(s, 'classic:gravity-forms')[0])], layout_column_flex_align='stretch'),
    ], layout='45% 55%', gap='5rem', align='flex-start',
       **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None], 'layout_row_gap_column': [None, None, '2.5rem', '3.5rem', None]}})],
       section_bg_color=IVORY)
    return [banner('Get Connected', image='442:full'), sec2]

def thank_you():
    steps = [('calendar', 'Plan Your Visit', '<p>Join us Sunday mornings at 10 AM. We will save you a seat.</p>', ('Plan your visit', '/plan-your-visit/')),
             ('play', 'Watch Live', '<p>Can not make it in person? Worship with us online every Sunday.</p>', ('Watch live', '/watch-live/')),
             ('book-open', 'Recent Messages', '<p>Catch up on recent sermons and hear what we have been learning together.</p>', ('Listen now', '/sermon-manager/'))]
    sec1 = banner('Thank You', sub="We've received your message. Someone from our team will be in touch with you soon.", image='458:full')
    sec2 = section("2. What's Next", [
        row('Heading', [col('Heading Group', [eyebrow('While you wait'), headline("Here's what's next", margin='1.4rem 0px 0px 0px')]),
                        col('Buttons', [div('Buttons', [button('Back to home  →', '/', 'navy')])], layout_column_flex_justify='flex-end',
                            layout_column_flex_align='flex-end', **bp(layout_column_flex_align=['flex-start', 'flex-start', 'flex-start', None, None]))],
            layout='65% 35%', gap='3rem', align='flex-end', layout_row_margin='0px auto 3rem auto'),
        cards_row([icon_card(i, t_, x, btn) for i, t_, x, btn in steps]),
    ], section_bg_color=IVORY)
    return [sec1, sec2, relabel(GET_IN_TOUCH, '3. Get In Touch (component)')]

def events():
    t = P(235); return [banner('Events', image='441:full'), raw_section('2. Calendar (MEC shortcode)', find_all(t[1], 'classic:raw-content')[0],
            'Join us', 'Upcoming events', 'Find out what is happening at Graham and plan to join us. Tap an event to see the details.')]

def sermons():
    t = P(267); return [banner('Sermons', image='460:full'), raw_section('2. Sermon List (shortcode)', find_all(t[1], 'classic:raw-content')[0],
            'Listen and grow', 'Recent messages', 'Missed a Sunday, or want to hear a message before you visit? Catch up on recent messages here.')]

def christmas():
    t = P(288)
    h0 = find_all(t[0], 'headline')[0]
    sec1 = banner(strip_p(h0['text_content']), eyebrow_txt=h0['text_subheadline_content'].strip(), image=t[0]['bg_lower_image'])
    sec1['title'] = '1. Christmas Eve (banner)'
    s1 = t[1]; h1 = find_all(s1, 'headline')[0]; b1 = find_all(s1, 'button')[0]
    sec2 = split('2. Christmas Eve Service', media_frame(find_all(s1, 'classic:image')[0]['src']),
                 [eyebrow(h1['text_subheadline_content'].strip())] + text_block(strip_p(h1['text_content']), find_all(s1, 'text')[0]['text_content'].replace('<p></p>', ''),
                 [(b1['anchor_text_primary_content'], b1['anchor_href'])]), reverse=False)
    sec2['_modules'][0]['_modules'] = sec2['_modules'][0]['_modules'][::-1]   # text left, image right (as the original)
    q = find_all(t[2], 'headline')[0]
    qtext = re.sub(r'<br />\s*', ' ', strip_p(q['text_content']))
    m = re.match(r"\s*'?(.*?)\"?\s*-\s*(Matthew.*)$", qtext)
    sec3 = section('3. Scripture', [row('Content', [col('Quote', [
        eyebrow(q['text_subheadline_content'].strip(), GOLD),
        headline('“' + (m.group(1) if m else qtext).strip() + '”', tag='p', size='clamp(2rem, 4.2vw, 3.4rem)', color='#ffffff', ls='-0.04em',
                 lh='1.2', margin='1.75rem 0px 1.25rem 0px', text_text_align='center'),
        headline(m.group(2) if m else '', tag='span', size='0.7rem', color='rgba(255,255,255,0.65)', font=F_BODY, weight='700', ls='0.26em',
                 lh='1', text_text_transform='uppercase', text_text_align='center'),
    ], layout_column_flex_align='center')], layout_row_max_width='56rem')], **dark_bg(t[2]['bg_lower_image'], 'rgba(15, 24, 40, 0.82)'))
    s3 = t[3]; h3 = find_all(s3, 'headline')[0]; b3 = find_all(s3, 'button')[0]
    sec4 = split('4. Candlelight Service', media_frame(find_all(s3, 'classic:image')[0]['src']),
                 [eyebrow(h3['text_subheadline_content'].strip())] + text_block(strip_p(h3['text_content']),
                 find_all(s3, 'text')[0]['text_content'].replace(' class="rtecenter"', ''), [(b3['anchor_text_primary_content'], b3['anchor_href'])]), bg=PAPER)
    return [sec1, sec2, sec3, sec4]

def prayer():
    t = P(58)
    h1 = find_all(t[0], 'custom-headline')[0]['content']; body = find_all(t[0], 'text')[0]['content']
    body_html = ''.join(f'<p>{p.strip()}</p>' for p in body.split('\n\n') if p.strip())
    sec1 = banner(h1, body=body_html, image='459:full'); sec1['title'] = '1. Prayer Changes Everything'
    s2 = t[1]; hh = find_all(s2, 'custom-headline'); items = find_all(s2, 'feature-list-item'); gf = find_all(s2, 'gravity-forms')[0]
    qa = [div(f'Item – {i["title"]}', [
            el('icon', None, [], icon=i.get('graphic_icon', 'circle'), icon_font_size='1rem', icon_width='2.75rem', icon_height='2.75rem',
               icon_color=NAVY, icon_bg_color=IVORY, icon_border_radius='50%', layout_margin=None),
            div('Text', [headline(i['title'], tag='h3', size='1.15rem', color=NAVY, weight='700', ls='-0.01em', lh='1.3'),
                         text(f'<p>{i["content"].strip()}</p>', size='0.92rem', maxw='30rem', text_margin='0.4rem 0px 0px 0px')],
                layout_div_flex='1 1 0%')],
          direction='row', gap='1.25rem', layout_div_width='100%', layout_div_padding='1.4rem 0px 1.4rem 0px',
          layout_div_border_width='0px 0px 1px 0px', layout_div_border_style='solid', layout_div_border_color='rgba(36,52,77,0.14)')
          for i in items]
    form_el = {'_type': 'classic:gravity-forms', '_bp_base': BP, 'form_id': '8'}  # form 2 no longer exists; 8 = Prayer Request
    sec2 = section('2. Pray With You (form)', [row('Content', [
        col('Questions', [headline(hh[0]['content']), gold_rule()] + qa),
        col('Form', [div('Form Box', form_box(hh[1]['content'], form_el), layout_div_width='100%', layout_div_bg_color='#ffffff',
                         layout_div_padding='2.5rem 2.25rem 2.5rem 2.25rem', layout_div_border_width='2px 0px 0px 0px',
                         layout_div_border_style='solid', layout_div_border_color=GOLD,
                         layout_div_box_shadow_dimensions='0em 1.5em 3.5em -1.5em', layout_div_box_shadow_color='rgba(15,24,40,0.25)')]),
    ], layout='55% 45%', gap='4.5rem', align='flex-start',
       **{'_bp_data3_4': {'layout_row_layout': ['100%', '100%', '100%', None, None]}})], section_bg_color=IVORY)
    return [sec1, sec2]

THANKS_ID = int(open('thanks_id').read()) if __import__('os').path.exists('thanks_id') else 0
PAGES = {11: about, 12: connect_page, 272: plan_visit, 14: give, 307: watch_live, 345: get_connected,
         235: events, 267: sermons, 288: christmas, 58: prayer, THANKS_ID: thank_you}

def clean(e):
    if isinstance(e, dict):
        for k in [k for k, v in e.items() if v is None]: del e[k]
        for v in e.values(): clean(v)
    elif isinstance(e, list):
        for x in e: clean(x)

if __name__ == '__main__':
    out = {}
    for pid, fn in PAGES.items():
        tree = fn(); clean(tree); out[pid] = tree
        print(pid, fn.__name__, [s['title'] for s in tree])
    json.dump(out, open('pages-new.json', 'w'), indent=1)
