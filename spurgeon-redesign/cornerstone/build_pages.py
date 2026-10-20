"""Native Cornerstone builds for each page, styled through element settings. Usage: python3 build_pages.py home about ..."""
import json,os,sys
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from csel import *
GIT={'_type':'global-block','_bp_base':'4_4','global_block_id':open(os.environ['MCPDIR']+'/git_component_id').read().strip(),'_modules':[]}
MP=json.load(open(os.environ['MCPDIR']+'/media_map.json'))
def P(i): return UP+MP[i]
HERO_H='calc(clamp(300px,42svh,460px) - 128px)'   # page hero height minus its 64px top/bottom padding

def centered_col(mods,min_h,pad='0px',cls=''):
    """Column that centres its content (Flexbox) and left-aligns it on phones."""
    c=col(mods,cls,flexbox=True,flex_direction='column',flex_justify='center',flex_align='center',text_align='center',min_height=min_h,padding=pad)
    bp(c,'layout_column_flex_align','flex-start','flex-start'); bp(c,'layout_column_text_align','left','left')
    return c

def page_hero(title,photo):
    h=headline(title,'h1','sp-page-title','page',color=WHITE,align='center'); bp(h,'text_text_align','left','left')
    return section('sp-page-hero',[row([centered_col([crumbs(),h],HERO_H)],'100%')],bg_image=photo,overlay='rgba(22,24,27,0.72)',pad='none') | {'section_padding':'64px 0px'}

def label_row(t,dark=False): return None   # section label rows removed site-wide; section() skips None

def lead(html,dark=False):
    return text(html,'sp-lead',color=WHITE if dark else INK,font_family=HEAD,font_weight='500',font_size='clamp(20px,1.7vw,24px)',
                line_height='1.4',letter_spacing='-0.015em',margin='0px 0px 14px 0px')

def copy_block(title,first,rest,btns,dark=False):
    mods=[headline(title,'h2','sp-h2','h2',color=WHITE if dark else INK)]
    if first: mods.append(lead(f'<p>{first}</p>',dark))
    if rest: mods.append(text(''.join(f'<p>{r}</p>' for r in rest),dark=dark))
    if btns: mods.append(actions(btns))
    return mods

def split(copy_mods,media_mods,flip=False,layout='45% 55%'):
    c=col(copy_mods); m=col(media_mods,'sp-split-media')
    if not flip: bp(m,'layout_column_order','-1','-1','-1')   # stacked (tablet + phones): photo first, text below
    return row([m,c] if flip else [c,m],(('55% 45%' if layout=='45% 55%' else layout) if flip else layout),'sp-split',md='100%',align='center')

def circle(i,alt,dark=False,url=None):
    im=round_image(url or P(i),alt,dark=dark,stack_md=True)
    return bp(im,'image_styled_max_width','100%','100%','100%')   # stacked (tablet + phones): fills the column width

def intro_with_form(title,blurb,photo,alt,form_id):
    """Heading + short intro + round photo | form in a white card (Prayer, Let Us Know You're Coming)."""
    ph=round_image(photo,alt,max_w='300px',center=False,cls='sp-circle sp-intro-photo'); ph['image_margin']='48px 0px 0px 10px'; ph['hide_bp']=' md sm xs'
    left=col([headline(title,'h2','sp-h2','h2',color=INK),text(f'<p>{blurb}</p>',max_width='420px'),ph],'sp-intro',padding='0px 48px 0px 0px')
    bp(left,'layout_column_padding','0px','0px','0px')
    right=col([form(form_id)],'sp-form-card',bg_color='#ffffff',border_width='1px',border_style='solid',border_color=LINE,border_radius='14px',padding='clamp(28px,3.4vw,48px)')
    return row([left,right],'40% 60%','sp-intro-form',md='100%',align='flex-start')

def icon_col(ic,title,body_html,extra=None):
    """Top hairline + icon + title + text (Vision, Ways to Give)."""
    return col([icon(ic),headline(title,'h3','sp-h3','h3',color=INK),text(body_html)]+(extra or []),'sp-col',
               border_width='1px 0px 0px 0px',border_style='solid',border_color=LINE_S,padding='28px 0px 0px 0px')

TICK=[('Sundays','8:30 am &amp; 10:00 am','/plan-your-visit/'),('Wednesdays','6:30 pm','/plan-your-visit/'),
      ('New here?','Plan your visit, we’d love to meet you','/plan-your-visit/'),('Watch Live','Join the service online every Sunday','/watch-live/'),
      ('Find us','1221 My Street, My Town, XX 12212',MAPS)]

def ticker():
    """Scrolling schedule/announcement band: native Slider (Slide Container in Marquee mode), no HTML or CSS.
    Each item is a linked Slide holding a cyan label + white text; small dot icons sit between items."""
    def item(lbl,txt,href):
        sl={'_type':'layout-slide','_bp_base':'4_4','layout_slide_href':href,'layout_slide_blank':href.startswith('http'),
            'layout_slide_flexbox':True,'layout_slide_flex_direction':'row','layout_slide_flex_wrap':False,'layout_slide_flex_align':'center','layout_slide_flex_justify':'flex-start',
            '_modules':[headline(lbl,'div','','label',color=CYAN,margin='0px 12px 0px 0px'),
                        headline(txt,'div','','lead',color='rgba(255,255,255,0.88)',font=BODY,weight='400',font_size='16px',line_height='1.4',
                                 letter_spacing='0em',margin='0px',text_color_alt=WHITE)]}
        return sl
    def sep():
        return {'_type':'layout-slide','_bp_base':'4_4','layout_slide_flexbox':True,'layout_slide_flex_direction':'row','layout_slide_flex_align':'center',
                '_modules':[{'_type':'icon','_bp_base':'4_4','icon':'circle','icon_font_size':'6px','icon_width':'1em','icon_height':'1em',
                             'icon_color':CYAN,'icon_bg_color':'transparent','_modules':[]}]}
    slides=[]
    for _ in range(3):   # the set repeats so the marquee track is always longer than the screen and loops seamlessly
        for t in TICK: slides+= [item(*t),sep()]
    track={'_type':'layout-slide-container','_bp_base':'4_4','layout_slide_container_layout_type':'inline',
           'layout_slide_container_inline_slide_basis':'auto','layout_slide_container_inline_gap':'40px','layout_slide_container_inline_align':'center',
           'layout_slide_container_autoplay':'marquee','layout_slide_container_inline_marquee_speed':0.05,'layout_slide_container_inline_marquee_direction':'forward',
           'layout_slide_container_inline_wrap_around':True,'layout_slide_container_pause_on_hover':True,'layout_slide_container_autoplay_start_in_view':False,
           'layout_slide_container_content_width':'100%','_modules':slides}
    band=div([track],'',padding='16px 0px 16px 0px',bg_color='rgba(22,24,27,0.6)',border_width='1px 0px 0px 0px',border_style='solid',
             border_color=LINE_L,overflow_x='hidden',z_index='2',position='relative')
    band['effects_backdrop_filter']='blur(10px)'
    return band

def home():
    MIN=[('Kids','/connect/#kids','spurgeon-min-kids.jpg','Children in a Sunday school class'),
         ('Youth','/connect/#students','spurgeon-min-youth.jpg','A youth group gathering at church'),
         ('Men','/connect/#men','spurgeon-min-men.jpg','Men gathered for fellowship in the church hall'),
         ('Women','/connect/#women','spurgeon-min-women.jpg','Women praying together')]
    kicker=headline('Spurgeon Church','div','sp-kicker','label',color=WHITE,margin='0px 0px 24px 0px',letter_spacing='0.2em')
    h1=headline('Loving God.','h1','sp-h1','h1',color=WHITE,sub='Loving People.',sub_color=CYAN,align='center'); bp(h1,'text_text_align','left','left')
    acts=actions([button('Plan Your Visit','/plan-your-visit/','white'),button('Watch Live','/watch-live/','line')],center=True,mt='0px')
    bp(acts,'layout_div_flex_justify','flex-start','flex-start')
    hero_col=centered_col([kicker,h1,acts],'calc(88svh - 130px)','64px 0px 64px 0px','sp-hero-col')
    bp(hero_col,'layout_column_min_height','0px','0px'); bp(hero_col,'layout_column_padding','88px 0px 88px 0px','88px 0px 88px 0px')
    # Welcome photos: large round photo + smaller one overlapping bottom-left (Div › Position: absolute)
    small=round_image(UP+'spurgeon-welcome-support.jpg','People supporting one another during a church service',max_w='none',ring=False,center=False)
    small.update({'image_box_shadow_dimensions':'0px 0px 0px 8px','image_box_shadow_color':CREAM})
    photos=div([div([],'sp-welcome-ring',position='absolute',top='0px',right='0px',width='22%',height='0px',padding='0px 0px 22% 0px',
                    border_width='1px',border_style='solid',border_color=CYAN,border_radius='50%'),
                round_image(UP+'spurgeon-welcome-greeting.jpg','Church members greeting each other with smiles',max_w='none',center=False),
                div([small],'sp-welcome-small',position='absolute',left='0px',bottom='0px',width='44%')],
               'sp-welcome-photos',position='relative',padding='0px 0px 12% 12%',max_width='640px',margin='0px 0px 0px auto')
    bp(photos,'layout_div_margin','0px','0px','0px'); bp(photos,'layout_div_max_width','100%','100%','100%')
    def min_card(t,h,f,alt):
        im=round_image(UP+f,alt,max_w='240px',dark=True,href=h,ring_gap='8px')
        tt=headline(t,'h3','sp-card-title','card',color=WHITE,href=h,align='center',text_color_alt=CYAN); bp(tt,'text_text_align','left','left')
        im.update({'image_border_color_alt':CYAN})   # ring turns cyan on hover
        c=col([im,tt],'sp-card',text_align='center'); bp(c,'layout_column_text_align','left','left')
        # hover: card lifts (Effects › Alt)
        c.update({'effects_alt':True,'effects_transform_alt':'translate(0px, -6px)','effects_duration':'400ms',
                  'effects_timing_function':'cubic-bezier(0.400, 0.000, 0.200, 1.000)'})
        return c
    return [
     section('sp-hero',[row([hero_col],'100%'),ticker()],bg_video=UP+'spurgeon-hero.mp4',overlay='rgba(22,24,27,0.5)',pad='none'),
     section('sp-section',[label_row('About Us'),
       row([col([headline('Welcome Home','h2','sp-h2','h2',color=INK),
                 lead('<p>New to the community, our church is planting and putting down roots to reach the people in our neighborhood and the surrounding areas for Christ.</p>'),
                 text('<p>We are a place where the people in our community can be welcomed in, encouraged, and supported as they seek after God’s will for their life. We intend to work locally to bring the Gospel of Jesus to our neighbors, making a lasting impact on our city as we serve and love our people in Jesus’ name. By the grace of God, we look forward to growing as a church and seeing our community transformed by the power of Christ.</p>'),
                 actions([button('About Us','/about/','ink')])]),
            bp(col([photos]),'layout_column_order','-1','-1','-1')],'42% 58%','sp-split',md='100%',align='center')],id_='welcome',bg_color=CREAM),
     section('sp-section sp-dark',[label_row('Get Connected',True),
       row([col([headline('Our Ministries','h2','sp-h2','h2',color=WHITE)]),
            col([text('<p>Whether you\'re single or married, with children or without, young or old, male or female, we have a place for you! Take a look at all of our ministry opportunities to find the best fit for you and your family.</p>',dark=True),
                 actions([button('Get Connected','/connect/','cyan')])])],'45% 55%','',md='100%',align='center'),
       row([min_card(*m) for m in MIN],'25% 25% 25% 25%','sp-cards',md='25% 25% 25% 25%',sm='50% 50%',xs='50% 50%',align='flex-start',mt='48px')],
       id_='ministries',bg_image=UP+'spurgeon-bg-ministries.jpg',overlay=DARK),
     GIT]

def plan_your_visit():
    # FAQ answers are the template's placeholder copy, kept word for word; shown open (no accordion)
    FAQ_BODY='This is the accordion body content. It is typically best to keep this area short and to the point so it isn’t too overwhelming.'
    QS=['What should I wear?','What do you have for Kids/Students?','What style of worship do you have?','Do you have small groups?']
    def faq_item(q):
        d=div([headline(q,'h3','sp-h3','h3',color=WHITE),text(f'<p>{FAQ_BODY}</p>',dark=True,size='16px')],'sp-faq-item',
              width='calc(50% - 24px)',padding='28px 0px 32px 0px',border_width='1px 0px 0px 0px',border_style='solid',border_color=LINE_L)
        return bp(d,'layout_div_width','100%','100%')
    return [
     page_hero('Plan Your Visit',P('1695938746747-ec185ea81325')),
     section('sp-section',[label_row('Welcome'),
       split(copy_block('We say “Welcome!”','We want church to be a place where your entire family is encouraged to draw closer to Christ.',
              ['Visiting somewhere new can be intimidating. We want to make sure that you feel comfortable and welcome when you walk into our doors. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!'],
              [button('Let us know you’re coming','#coming','ink')]),
             [circle('1577975039920-8fbb74e58527','Friends sharing coffee around a table with open Bibles')])],bg_color=CREAM),
     section('sp-section sp-dark',[label_row('Questions',True),
       row([col([headline('FAQs','h2','sp-h2','h2',color=WHITE),text('<p>Everything you might want to know before your first Sunday.</p>',dark=True)]),
            col([div([faq_item(q) for q in QS],'sp-faq',flexbox=True,flex_direction='row',flex_wrap=True,flex_gap='0px 48px',flex_align='flex-start')])],
           '35% 65%','',md='100%')],bg_image=P('1647476427592-c78c1e363683'),overlay=DARK),
     section('sp-section',[label_row('Plan Ahead'),
       intro_with_form('Let Us Know You’re Coming','Tell us when you plan to visit and we’ll be ready to welcome you, help get your kids settled and show you around.',
                       P('1565813086292-604790c8a97b'),'Two church members greeting each other with a hug',2)],id_='coming',bg_color=CREAM)]

def about():
    VIS=[('o-book-open','Worship &amp; Study','Through weekly Bible studies, worship gatherings, and small groups, we will learn more about God and grow in our knowledge and love for Him.'),
         ('o-hand-holding-heart','Evangelism &amp; Outreach','By reaching out to and serving those around us, we will share God’s love and His message of hope with the people in our community.'),
         ('o-paper-plane','Multiplication &amp; Sending','By making disciples and supporting fellow believers as they step out to launch new churches and ministries around the world, we will expand our reach to exhibit God’s love to people across the globe.')]
    # Beliefs: open card grid, all content visible. Statements vary in length; the masonry layout absorbs it.
    BELIEFS=[('o-book-bible','The Bible','We believe the Bible is the inspired and trustworthy Word of God. It is our final authority for faith and life. Through its pages God shows us who He is, tells the story of His rescue through Jesus, and teaches us how to love Him and love our neighbors. We read it together, study it in small groups and build our lives on it.'),
             ('o-crown','The Father','We believe in one God, the loving Father and Creator of all things.'),
             ('o-cross','The Son','We believe Jesus Christ is fully God and fully man. He lived a sinless life, died on the cross for our sins, rose bodily from the grave and is coming again in glory.'),
             ('o-dove','The Holy Spirit','We believe the Holy Spirit lives in every believer from the moment they trust in Jesus. He comforts us in hard seasons, guides us into truth and gives us power to live for God. He produces His fruit in our lives, such as love, joy and peace, and gives each believer gifts to serve and build up the church.'),
             ('o-infinity','Eternity','We believe every person was created to live forever, and one day God will make all things new.'),
             ('o-user','Man','We believe every person is made in the image of God and deeply loved by Him. Yet all of us have sinned and fallen short, and we need a Savior to restore us.'),
             ('o-heart','Salvation','We believe salvation is a free gift of God’s grace. It is received through faith in Jesus Christ alone and cannot be earned by good works. When we turn from sin and trust in Him, we are forgiven, made new and welcomed into God’s family. Nothing can separate us from His love.'),
             ('o-church','The Church','We believe the church is the family of God. We gather to worship, grow in the Word and care for one another.')]
    def belief(ic,t,d):
        return card_div([icon(ic,dark=True,mb='28px'),headline(t,'h3','sp-h3','h3',color=WHITE,margin='0px 0px 10px 0px'),
                         text(f'<p>{d}</p>',size='15.5px',lh='1.65',color='rgba(255,255,255,0.68)')],dark=True)
    def member():
        ph=round_image('https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2018/05/400x400-white.png','Leader photo',max_w='240px',ring_gap='8px')
        bp(ph,'image_styled_max_width','100%','100%','100%')   # tablet + phones: fill the column
        ph['image_margin']='0px auto 24px auto'; bp(ph,'image_margin','0px 0px 24px 0px','0px 0px 24px 0px')
        n=headline('First &amp; Last Name','h3','sp-h3','h3',color=INK,align='center'); r=headline('Position / Title','div','sp-member-role','role',color=CYANINK,align='center')
        for h in (n,r): bp(h,'text_text_align','left','left')
        return col([ph,n,r],'sp-member')
    return [
     page_hero('About Us',P('1623533733598-0782b7157763')),
     section('sp-section',[label_row('Our Mission'),
       split([headline('We want to be a people who care for, welcome, and support those around us in a way that can only be inspired by God.','h2','sp-statement','statement',color=INK),
              text('<p>It’s our hope that people who visit our church or interact with our people walk away feeling encouraged, refreshed, and drawn closer to God. We want every man, woman, and child in our community to have the chance to experience and respond to the Gospel in action through our church.</p>')],
             [circle('1717278087114-c9a3efc29e1e','A worship gathering in a modern church')],layout='55% 45%')],bg_color=CREAM),
     section('sp-section',[label_row('Our Vision'),
       row([col([headline('Our Vision','h2','sp-h2','h2',color=INK)])],'100%'),
       row([icon_col(i,t,f'<p>{d}</p>') for i,t,d in VIS],'33.33% 33.33% 33.34%','',md='100%',mt='28px')],bg_color=CREAM,pad='tight-top'),
     section('sp-section sp-dark',[label_row('What We Believe',True),
       row([col([headline('Our Beliefs','h2','sp-h2','h2',color=WHITE),text('<p>This is how we view God, Jesus, the Bible, man, and many significant aspects of our faith. Firmly rooted in Scripture, our beliefs guide our decisions as a church.</p>',dark=True,max_width='640px')])],'100%'),
       # Masonry: 4 columns; each holds a 'stack' Div (Flexbox column, 32px gap) of card Divs, so uneven text never
       # leaves empty space in a box. To add a belief, duplicate a card inside the shortest column's stack: the gap is automatic.
       # Order runs down each column (Bible, Father | Son, Spirit | ...), which keeps phones in the original order.
       row([col([div([belief(*BELIEFS[c*2]),belief(*BELIEFS[c*2+1])],'',flexbox=True,flex_direction='column',flex_align='stretch',flex_gap='32px')]) for c in range(4)],
           '25% 25% 25% 25%','sp-beliefs',md='50% 50%',sm='50% 50%',xs='100%',mt='48px',gap_row='32px',align='flex-start')],
       bg_image=P('1478147427282-58a87a120781'),overlay=DARK),
     section('sp-section',[label_row('Our Leadership'),row([col([headline('Our Leadership','h2','sp-h2','h2',color=INK)])],'100%'),
       row([member() for _ in range(6)],'33.33% 33.33% 33.34%','',md='50% 50%',sm='50% 50%',xs='50% 50%',mt='48px')],bg_color=CREAM),
     GIT]

KIDS='We want church to be a place where your entire family is encouraged to draw closer to Christ—your kids included!'
KIDS2='That’s why, during our Sunday morning worship services, we offer fun and engaging environments where children can learn and grow in faith as well. All our kids’ programs are designed to be safe places where children in our church can learn new and exciting things about God while being led and cared for by adult volunteers from our congregation. It’s our hope to encourage children to not only discover new things about God, but also begin to understand how those things matter in their own lives.'
STU='In student ministry, we strive to lead students to become passionate followers of Christ.'
STU2='By partnering with parents and trained leaders, our mission is to teach and inspire the next generation to be founded in their faith and confident in their Creator. Through regular Bible study and small group gatherings, we encourage students to walk boldly towards Christ, apply His truth to their lives, and develop strong, life-changing relationships with the God of the universe. We want our students to know Jesus so that they might be excited about sharing His name and making Him known to others. Our prayer is that the church would be the future of our world and our students, the future of the church.'
WOM='Women’s ministries at our church is designed to make the big Sunday morning church experience feel a little smaller.'
WOM2='We’ve crafted our environments to help you connect with others who are in the same season of life, forming close-knit communities to navigate the ups and downs of those seasons together. Through small group programs, our main goal is to make women’s ministries at our church a place where anyone in our congregation can grow closer to community while ultimately growing closer to Christ.'
MEN='By meeting together, sharing meals, walking through curriculum, studying the Word, and simply doing life with another, the men in our congregation have a safe place where they can get connected with the resources, support, and friendships to help them live fuller lives in Christ.'
MEN2='No matter your stage or season of life, we want you to join us! Take a look at all the options we have for adult ministries to find what best suits you. We can’t wait to help you connect with others in our church.'
YT='<iframe width="560" height="315" src="https://www.youtube.com/embed/dlhA0AmTVf0" title="Spurgeon Church live stream" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
GIVE1='We appreciate your generous gift to our church.'
GIVE2='As we grow, we know that it will be the grace of God that leads us and the continued support of our people that carries us. We are so thankful to have you as a part of our church family.'

def connect():
    def m(anchor,title,first,rest,photo,alt,dark,bg=None):
        mods=[label_row(title,dark),split(copy_block(title,first,rest,[button('Get Connected','/get-connected/','cyan' if dark else 'ink')],dark),[circle(photo,alt,dark)],flip=dark)]
        return section('sp-section'+(' sp-dark' if dark else ''),mods,id_=anchor,bg_image=P(bg) if bg else None,overlay=DARK if dark else None,bg_color=None if dark else CREAM)
    return [page_hero('Get Connected',P('1569292567777-e5d61a759322')),
      m('kids','Kids',KIDS,[KIDS2],'1588075592446-265fd1e6e76f','Children in a Sunday school class',False),
      m('students','Students',STU,[STU2],'1762158007836-25d13ab34c1c','A youth group gathering at church',True,'1609234656432-603fd648adf8'),
      m('women','Women',WOM,[WOM2],'1520857014576-2c4f4c972b57','Women praying together',False),
      m('men','Men',MEN,[MEN2],'1785225486940-cdf8b2b9b8f1','Men gathered for fellowship in the church hall',True,'1647476427592-c78c1e363683'),
      GIT]

def get_connected():
    return [page_hero('Contact Us',P('1569292567777-e5d61a759322')),
      section('sp-section',[label_row('Connect Card'),
        intro_with_form('Connect Card','Thank you for connecting with us. We would love to answer any questions you may have and we have a free gift for you taking the time to give us some information.',
                        'https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2020/07/rod-long-TzgZrZQFVPc-unsplash.jpg','A welcoming church gathering',4)],bg_color=CREAM)]

def watch_live():
    return [page_hero('Watch Live',P('1630449151135-6db9690cbda4')),
      section('sp-section',[label_row('Live Stream'),
        row([col([headline('Join us Sundays at 10am','h2','sp-h2','h2',color=INK),video(None,None,embed=YT)])],'100%')],bg_color=CREAM),
      section('sp-section sp-dark',[label_row('Generosity',True),
        split(copy_block('Give Online',GIVE1,[GIVE2],[button('Give Now','/give/','cyan')],True),[circle('1529070538774-1843cb3265df','Church members following along with open Bibles',True)])],
        bg_image=P('1622598453695-4fbaf151aadc'),overlay=DARK),
      section('sp-section',[label_row('Prayer'),
        intro_with_form('How can we pray for you?','Share your request below. Our team will be praying for you, and everything you share stays confidential.',
                        P('1609234656432-603fd648adf8'),'Two people embracing in prayer at church',3)],bg_color=SAND)]

def messages():
    return [page_hero('Messages',P('1507692049790-de58290a4334')),
      section('sp-section',[label_row('Sermon Library'),row([col([raw('[smpro_archive]','sp-sermons')])],'100%')],bg_color=CREAM)]

def events():
    return [page_hero('Events',P('1442504028989-ab58b5f29a4a')),
      section('sp-section',[label_row('Calendar'),row([col([raw('[MEC id="48"]','sp-events')])],'100%')],bg_color=CREAM)]

def give():
    W=[('o-calendar','Give on Sunday','<p>During service, feel free to place your offering in our giving baskets as they are passed during service.</p>',None),
       ('o-lock','Give Online','<p>Using our safe, secure online giving platform, you can feel safe about your gift. Login to get started.</p>',button('Give Now','','ink')),
       ('o-envelope','Give by Mail','<p>Spurgeon Church<br>1234 My Street<br>My Town, XX 12345</p>',None)]
    return [page_hero('Give',P('1698768676413-e49b729dafa6')),
      section('sp-section',[label_row('Generosity'),
        split(copy_block('Live Generously',GIVE1,[GIVE2],[button('Give Now','#ways-to-give','ink')]),[circle('1762013728402-69cff78f29fd','A congregation seated together during a church service')])],bg_color=CREAM),
      section('sp-section',[label_row('Ways to Give'),row([col([headline('Ways to Give','h2','sp-h2','h2',color=INK)])],'100%'),
        row([card([icon(i),headline(t,'h3','sp-h3','h3',color=INK),text(d)]+([actions([b])] if b else []),pad='36px 32px 36px 32px') for i,t,d,b in W],
            '33.33% 33.33% 33.34%','',md='100%',mt='48px',gap_row='24px',align='stretch')],
        id_='ways-to-give',bg_color=SAND)]

PAGES={'home':(8,home),'plan-your-visit':(79,plan_your_visit),'about':(11,about),'connect':(12,connect),'get-connected':(113,get_connected),
       'watch-live':(90,watch_live),'messages':(71,messages),'events':(76,events),'give':(14,give)}

if __name__=='__main__':
    for name in (sys.argv[1:] if sys.argv[1:]!=['all'] else list(PAGES)):
        pid,fn=PAGES[name]
        r=call('cs_save_element_tree',{'id':pid,'tree':clean(fn())},timeout=180)
        print(name,pid,json.dumps(r)[:120])
    call('cs_purge_cache',{},timeout=60)
