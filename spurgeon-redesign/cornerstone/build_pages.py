"""Native Cornerstone builds for each page. Usage: python3 build_pages.py home about ..."""
import json,os,sys
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
from csel import *
GIT={'_type':'global-block','_bp_base':'4_4','global_block_id':open(os.environ['MCPDIR']+'/git_component_id').read().strip(),'_modules':[]}
DARK='rgba(22,24,27,0.88)'

def page_hero(title,photo):
    return section('sp-page-hero',[row([col([crumbs(),headline(title,'h1','sp-page-title',color=WHITE)])],'100%')],bg_image=photo,overlay='rgba(22,24,27,0.68)')

def label_row(t): return row([col([headline(t,'div','sp-label',font=BODY)])],'100%')

def split(copy_mods,media_mods,flip=False,layout='45% 55%'):
    c=col(copy_mods); m=col(media_mods,'sp-split-media')
    return row([m,c] if flip else [c,m],(('55% 45%' if layout=='45% 55%' else layout) if flip else layout),'sp-middle',md='100%')

TICK=[('Sundays','8:30 am &amp; 10:00 am','/plan-your-visit/'),('Wednesdays','6:30 pm','/plan-your-visit/'),
      ('New here?','Plan your visit, we’d love to meet you','/plan-your-visit/'),('Watch Live','Join the service online every Sunday','/watch-live/'),
      ('Find us','1221 My Street, My Town, XX 12212',MAPS)]
def tick_group(hidden):
    ah=' aria-hidden="true"' if hidden else ''; ti=' tabindex="-1"' if hidden else ''
    return f'<ul{ah}>'+''.join(f'<li><a href="{h}"{ti}{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}><b>{a}</b> {b}</a></li>' for a,b,h in TICK)+'</ul>'
TICKER=f'<div class="sp-ticker" role="region" aria-label="Schedule and announcements"><div class="sp-ticker-track">{tick_group(False)}{tick_group(True)}</div></div>'

def home():
    MIN=[('Kids','/connect/#kids','spurgeon-min-kids.jpg','Children in a Sunday school class'),
         ('Youth','/connect/#students','spurgeon-min-youth.jpg','A youth group gathering at church'),
         ('Men','/connect/#men','spurgeon-min-men.jpg','Men gathered for fellowship in the church hall'),
         ('Women','/connect/#women','spurgeon-min-women.jpg','Women praying together')]
    return [
     section('sp-hero',[
       row([col([headline('Spurgeon Church','div','sp-kicker',font=BODY),
                 headline('Loving God.','h1','sp-h1',sub='Loving People.',color=WHITE),
                 div([button('Plan Your Visit','/plan-your-visit/','white'),button('Watch Live','/watch-live/','line')],'sp-actions')])],'100%'),
       raw(TICKER)],bg_video=UP+'spurgeon-hero.mp4',overlay='rgba(22,24,27,0.45)'),
     section('sp-section',[label_row('About Us'),
       row([col([headline('Welcome Home','h2','sp-h2',color=INK),
                 text('<p class="first">New to the community, our church is planting and putting down roots to reach the people in our neighborhood and the surrounding areas for Christ.</p><p>We are a place where the people in our community can be welcomed in, encouraged, and supported as they seek after God’s will for their life. We intend to work locally to bring the Gospel of Jesus to our neighbors, making a lasting impact on our city as we serve and love our people in Jesus’ name. By the grace of God, we look forward to growing as a church and seeing our community transformed by the power of Christ.</p>'),
                 div([button('About Us','/about/','ink')],'sp-actions')]),
            col([div([image(UP+'spurgeon-welcome-greeting.jpg','Church members greeting each other with smiles','sp-circle sp-ring'),
                      image(UP+'spurgeon-welcome-support.jpg','People supporting one another during a church service')],'sp-welcome-photos')])],
           '42% 58%','sp-middle',md='100%')],id_='welcome',bg_color=CREAM),
     section('sp-section sp-dark',[label_row('Get Connected'),
       row([col([headline('Our Ministries','h2','sp-h2',color=WHITE)]),
            col([text('<p>Whether you\'re single or married, with children or without, young or old, male or female, we have a place for you! Take a look at all of our ministry opportunities to find the best fit for you and your family.</p>'),
                 div([button('Get Connected','/connect/','cyan')],'sp-actions')])],'45% 55%','sp-middle',md='100%'),
       row([col([image(UP+f,alt),headline(t,'h3','sp-card-title',font=HEAD,weight='500',color=WHITE,href=h)],'sp-card') for t,h,f,alt in MIN],
           '25% 25% 25% 25%','sp-cards sp-mt',md='25% 25% 25% 25%',sm='50% 50%',xs='50% 50%')],
       id_='ministries',bg_image=UP+'spurgeon-bg-ministries.jpg',overlay=DARK),
     GIT]

PAGES={'home':(8,home)}
MP=json.load(open(os.environ['MCPDIR']+'/media_map.json'))
def P(i): return UP+MP[i]
ACC_NOTE=None
def circle(i,alt,ring=True): return image(P(i),alt,'sp-circle'+(' sp-ring' if ring else ''))
def copy_block(title,first,rest,btns,dark=False):
    mods=[headline(title,'h2','sp-h2',color=WHITE if dark else INK)]
    html=(f'<p class="first">{first}</p>' if first else '')+(''.join(f'<p>{r}</p>' for r in rest))
    if html: mods.append(text(html))
    if btns: mods.append(div(btns,'sp-actions'))
    return mods

def plan_your_visit():
    return [
     page_hero('Plan Your Visit',P('1695938746747-ec185ea81325')),
     section('sp-section',[label_row('Welcome'),
       split(copy_block('We say “Welcome!”','We want church to be a place where your entire family is encouraged to draw closer to Christ.',
              ['Visiting somewhere new can be intimidating. We want to make sure that you feel comfortable and welcome when you walk into our doors. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!'],
              [button('Let us know you’re coming','#coming','ink')]),
             [circle('1577975039920-8fbb74e58527','Friends sharing coffee around a table with open Bibles')])],bg_color=CREAM),
     section('sp-section sp-dark',[label_row('Questions'),
       row([col([headline('FAQs','h2','sp-h2',color=WHITE),text('<p>Everything you might want to know before your first Sunday.</p>')]),
            col([accordion(['What should I wear?','What do you have for Kids/Students?','What style of worship do you have?','Do you have small groups?'])])],
           '35% 65%','',md='100%')],bg_image=P('1647476427592-c78c1e363683'),overlay=DARK),
     section('sp-section',[label_row('Plan Ahead'),
       split([headline('Let Us Know You’re Coming','h2','sp-h2',color=INK),form(2)],
             [circle('1565813086292-604790c8a97b','Two church members greeting each other with a hug')],layout='60% 40%')],id_='coming',bg_color=CREAM)]

def about():
    VIS=[('o-book-open','Worship &amp; Study','Through weekly Bible studies, worship gatherings, and small groups, we will learn more about God and grow in our knowledge and love for Him.'),
         ('o-hand-holding-heart','Evangelism &amp; Outreach','By reaching out to and serving those around us, we will share God’s love and His message of hope with the people in our community.'),
         ('o-paper-plane','Multiplication &amp; Sending','By making disciples and supporting fellow believers as they step out to launch new churches and ministries around the world, we will expand our reach to exhibit God’s love to people across the globe.')]
    # Beliefs: open card grid (all content visible). Body copy is the template's placeholder, kept word for word.
    BELIEF_BODY='This is the accordion body content. It is typically best to keep this area short and to the point so it isn’t too overwhelming.'
    BELIEFS=[('o-book-bible','The Bible'),('o-crown','The Father'),('o-cross','The Son'),('o-dove','The Holy Spirit'),
             ('o-infinity','Eternity'),('o-user','Man'),('o-heart','Salvation'),('o-church','The Church')]
    return [
     page_hero('About Us',P('1623533733598-0782b7157763')),
     section('sp-section',[label_row('Our Mission'),
       split([headline('We want to be a people who care for, welcome, and support those around us in a way that can only be inspired by God.','h2','sp-statement',weight='500',color=INK),
              text('<p>It’s our hope that people who visit our church or interact with our people walk away feeling encouraged, refreshed, and drawn closer to God. We want every man, woman, and child in our community to have the chance to experience and respond to the Gospel in action through our church.</p>')],
             [circle('1717278087114-c9a3efc29e1e','A worship gathering in a modern church')],layout='55% 45%')],bg_color=CREAM),
     section('sp-section sp-tight-top',[label_row('Our Vision'),
       row([col([icon(i),headline(t,'h3','sp-h3',color=INK),text(f'<p>{d}</p>')],'sp-col') for i,t,d in VIS],'33.33% 33.33% 33.34%','',md='100%')],bg_color=CREAM),
     section('sp-section sp-dark',[label_row('What We Believe'),
       row([col([headline('Our Beliefs','h2','sp-h2',color=WHITE),text('<p>This is how we view God, Jesus, the Bible, man, and many significant aspects of our faith. Firmly rooted in Scripture, our beliefs guide our decisions as a church.</p>','sp-copy sp-maxw')])],'100%'),
       row([col([icon(i,'sp-icon sp-belief-icon'),headline(t,'h3','sp-h3',color=WHITE),text(f'<p>{BELIEF_BODY}</p>','sp-copy sp-belief-copy')],'sp-belief') for i,t in BELIEFS],
           '25% 25% 25% 25%','sp-mt sp-beliefs',md='50% 50%',sm='50% 50%',xs='100%')],
       bg_image=P('1478147427282-58a87a120781'),overlay=DARK),
     section('sp-section',[label_row('Our Leadership'),row([col([headline('Our Leadership','h2','sp-h2',color=INK)])],'100%'),
       row([col([image('https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2018/05/400x400-white.png','Leader photo','sp-circle'),
                 headline('First &amp; Last Name','h3','sp-h3',color=INK),headline('Position / Title','div','sp-member-role',font=BODY)],'sp-member') for _ in range(6)],
           '33.33% 33.33% 33.34%','sp-mt',md='50% 50%',sm='50% 50%',xs='100%')],bg_color=CREAM),
     GIT]

KIDS='We want church to be a place where your entire family is encouraged to draw closer to Christ—your kids included!'
KIDS2='That’s why, during our Sunday morning worship services, we offer fun and engaging environments where children can learn and grow in faith as well. All our kids’ programs are designed to be safe places where children in our church can learn new and exciting things about God while being led and cared for by adult volunteers from our congregation. It’s our hope to encourage children to not only discover new things about God, but also begin to understand how those things matter in their own lives.'
STU='In student ministry, we strive to lead students to become passionate followers of Christ.'
STU2='By partnering with parents and trained leaders, our mission is to teach and inspire the next generation to be founded in their faith and confident in their Creator. Through regular Bible study and small group gatherings, we encourage students to walk boldly towards Christ, apply His truth to their lives, and develop strong, life-changing relationships with the God of the universe. We want our students to know Jesus so that they might be excited about sharing His name and making Him known to others. Our prayer is that the church would be the future of our world and our students, the future of the church.'
WOM='Women’s ministries at our church is designed to make the big Sunday morning church experience feel a little smaller.'
WOM2='We’ve crafted our environments to help you connect with others who are in the same season of life, forming close-knit communities to navigate the ups and downs of those seasons together. Through small group programs, our main goal is to make women’s ministries at our church a place where anyone in our congregation can grow closer to community while ultimately growing closer to Christ.'
MEN='By meeting together, sharing meals, walking through curriculum, studying the Word, and simply doing life with another, the men in our congregation have a safe place where they can get connected with the resources, support, and friendships to help them live fuller lives in Christ.'
MEN2='No matter your stage or season of life, we want you to join us! Take a look at all the options we have for adult ministries to find what best suits you. We can’t wait to help you connect with others in our church.'
def connect():
    def m(anchor,title,first,rest,photo,alt,dark,bg=None):
        mods=[label_row(title),split(copy_block(title,first,rest,[button('Get Connected','/get-connected/','cyan' if dark else 'ink')],dark),[circle(photo,alt)],flip=dark)]
        return section('sp-section'+(' sp-dark' if dark else ''),mods,id_=anchor,bg_image=P(bg) if bg else None,overlay=DARK if dark else None,bg_color=None if dark else CREAM)
    return [page_hero('Get Connected',P('1569292567777-e5d61a759322')),
      m('kids','Kids',KIDS,[KIDS2],'1588075592446-265fd1e6e76f','Children in a Sunday school class',False),
      m('students','Students',STU,[STU2],'1762158007836-25d13ab34c1c','A youth group gathering at church',True,'1609234656432-603fd648adf8'),
      m('women','Women',WOM,[WOM2],'1520857014576-2c4f4c972b57','Women praying together',False),
      m('men','Men',MEN,[MEN2],'1785225486940-cdf8b2b9b8f1','Men gathered for fellowship in the church hall',True,'1647476427592-c78c1e363683')]

def get_connected():
    return [page_hero('Contact Us',P('1569292567777-e5d61a759322')),
      section('sp-section',[label_row('Connect Card'),
        split([headline('Connect Card','h2','sp-h2',color=INK),text('<p>Thank you for connecting with us. We would love to answer any questions you may have and we have a free gift for you taking the time to give us some information.</p>'),form(4)],
              [image('https://rrnewspurgeon.wpenginepowered.com/wp-content/uploads/2020/07/rod-long-TzgZrZQFVPc-unsplash.jpg','A welcoming church gathering','sp-circle sp-ring')],layout='60% 40%')],bg_color=CREAM)]

YT='<iframe width="560" height="315" src="https://www.youtube.com/embed/dlhA0AmTVf0" title="Spurgeon Church live stream" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
GIVE1='We appreciate your generous gift to our church.'
GIVE2='As we grow, we know that it will be the grace of God that leads us and the continued support of our people that carries us. We are so thankful to have you as a part of our church family.'
def watch_live():
    return [page_hero('Watch Live',P('1630449151135-6db9690cbda4')),
      section('sp-section',[label_row('Live Stream'),
        row([col([headline('Join us Sundays at 10am','h2','sp-h2',color=INK),video(None,None,embed=YT),div([button('Get Connected','/connect/','ink')],'sp-actions')])],'100%')],bg_color=CREAM),
      section('sp-section sp-dark',[label_row('Generosity'),
        split(copy_block('Give Online',GIVE1,[GIVE2],[button('Give Now','/give/','cyan')],True),[circle('1529070538774-1843cb3265df','Church members following along with open Bibles')])],
        bg_image=P('1622598453695-4fbaf151aadc'),overlay=DARK),
      section('sp-section sp-sand',[label_row('Prayer'),
        row([col([headline('How can we pray for you?','h2','sp-h2',color=INK),
                  text('<p>Share your request below. Our team will be praying for you, and everything you share stays confidential.</p>','sp-copy sp-prayer-copy'),
                  image(P('1609234656432-603fd648adf8'),'Two people embracing in prayer at church','sp-circle sp-ring sp-prayer-photo')],'sp-prayer-intro'),
             col([form(3)],'sp-form-card')],'40% 60%','sp-prayer',md='100%')],bg_color=C('sp-sand'))]

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
        split(copy_block('Live Generously',GIVE1,[GIVE2],[button('Give Now','#ways-to-give','ink')]),[circle('1762013728402-69cff78f29fd','A congregation seated together during a church service')],flip=True)],bg_color=CREAM),
      section('sp-section sp-sand',[label_row('Ways to Give'),row([col([headline('Ways to Give','h2','sp-h2',color=INK)])],'100%'),
        row([col([icon(i),headline(t,'h3','sp-h3',color=INK),text(d)]+([div([b],'sp-actions')] if b else []),'sp-col') for i,t,d,b in W],'33.33% 33.33% 33.34%','sp-mt',md='100%')],
        id_='ways-to-give',bg_color=C('sp-sand'))]

PAGES.update({'plan-your-visit':(79,plan_your_visit),'about':(11,about),'connect':(12,connect),'get-connected':(113,get_connected),
              'watch-live':(90,watch_live),'messages':(71,messages),'events':(76,events),'give':(14,give)})

if __name__=='__main__':
    for name in sys.argv[1:]:
        pid,fn=PAGES[name]
        r=call('cs_save_element_tree',{'id':pid,'tree':fn()},timeout=180)
        print(name,pid,json.dumps(r)[:200])
    call('cs_purge_cache',{},timeout=60)
