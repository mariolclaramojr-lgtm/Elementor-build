# Generates the inner pages (about, plan-your-visit, connect, sermons, events, give, watch-live)
# from shared pieces of index.html (header, footer, contact section). Usage:
#   python3 tools/build_pages.py .   (run from the edwards-redesign folder)
import re, sys, os
ROOT = sys.argv[1]
idx = open(os.path.join(ROOT, 'index.html')).read()
lines = idx.split('\n')
def block(start_marker, end_marker, include_end=True):
    a = idx.index(start_marker); b = idx.index(end_marker, a) + (len(end_marker) if include_end else 0)
    return idx[a:b]
HEADER = block('<!-- ======================= HEADER', '</header>')
FOOTER = block('<!-- ======================= 6. FOOTER', '</footer>').replace('6. FOOTER', 'FOOTER')
TOTOP = re.search(r'<a href="#top" class="to-top".*?</a>', idx, re.S).group(0)
VISIT = block('<!-- ======================= 5. PLAN YOUR VISIT', '</section>')

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PLUS = '<span class="acc-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span>'
FB = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.2c0-.8.2-1.2 1.4-1.2H17V2h-2.6C11.3 2 10 3.5 10 6v2H8v3h2v11h4V11h2.7l.3-3z"/></svg>'
XI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L2 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/></svg>'
LI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.2 21 14.5V21h-4v-5.8c0-1.4-.03-3.2-1.95-3.2-1.95 0-2.25 1.5-2.25 3.1V21H9z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
SIL = '<svg viewBox="0 0 200 180" fill="currentColor" aria-hidden="true"><circle cx="100" cy="62" r="38"/><path d="M28 180c4-46 34-72 72-72s68 26 72 72z"/></svg>'

def acc(q, a='This is the accordion body content. It is typically best to keep this area short and to the point so it isn\'t too overwhelming.', open_=False):
    return f'''      <details class="acc"{' open' if open_ else ''}>
        <summary>{q}{PLUS}</summary>
        <div class="acc-body"><p>{a}</p></div>
      </details>'''

def page(slug, title, desc, banner, sections, extra_js='', comment=''):
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | Edwards Church</title>
<meta name="description" content="{desc}">
<script>document.documentElement.classList.add('js');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<!--
  EDWARDS — {title.upper()} (redesign mockup)
{comment}
  Shared header/footer/styles with the home page. Photos: Unsplash.
-->
</head>
<body>

'''
    hdr = HEADER.replace(f'<a href="{slug}.html">', f'<a href="{slug}.html" aria-current="page">')
    if slug == 'plan-your-visit':
        hdr = hdr.replace('<a href="plan-your-visit.html" class="btn btn-accent">', '<a href="plan-your-visit.html" class="btn btn-accent" aria-current="page">')
    body = head + hdr + '\n\n<main id="top">\n\n' + banner + '\n\n' + '\n\n'.join(sections) + '\n\n</main>\n\n' + FOOTER + '\n\n' + TOTOP + '\n\n<script src="js/site.js"></script>\n' + extra_js + '</body>\n</html>\n'
    open(os.path.join(ROOT, slug + '.html'), 'w').write(body)

def banner(title_html, crumb, img, alt, lead='', extra='', cls=''):
    lead_html = f'\n    <p class="lead">{lead}</p>' if lead else ''
    return f'''<!-- ======================= 1. PAGE BANNER ======================= -->
<section class="page-banner{(' ' + cls) if cls else ''}" aria-label="{crumb}">
  <div class="page-banner-bg" aria-hidden="true"><img src="{img}" alt="{alt}" width="2000" height="1333"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true"></span><span>{crumb}</span></nav>
    <h1>{title_html}</h1>{lead_html}{extra}
  </div>
</section>'''

CONTACT = VISIT.replace('5. PLAN YOUR VISIT — details cards + map', 'SERVICE TIMES & CONTACT — detail cards + map')

# ======================================================== PLAN YOUR VISIT
pyv_contact = CONTACT.replace(
  f'<a href="plan-your-visit.html" class="btn btn-primary">Plan Your Visit\n          {ARROW}</a>',
  f'<a href="#coming" class="btn btn-primary">Let Us Know You\'re Coming\n          {ARROW}</a>')
page('plan-your-visit', 'Plan Your Visit',
 'Plan your visit to Edwards Church: what to expect, FAQs, and let us know you are coming.',
 banner('What To <em>Expect</em>', 'Plan Your Visit', 'img/banner-visit.jpg', 'Church greeters welcoming people at the front doors',
        'Smiling faces, a cup of coffee and a place for your whole family.'),
 [f'''<!-- ======================= 2. A PLACE FOR YOU — video + text ======================= -->
<section class="section" aria-labelledby="place-title">
  <div class="wrap split">
    <div class="split-media reveal">
      <div class="video-card">
        <video autoplay muted loop playsinline preload="metadata" poster="img/visit-video-poster.jpg">
          <source src="hero.webm" type="video/webm">
          <source src="hero.mp4" type="video/mp4">
        </video>
        <button class="vc-toggle" type="button"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg><span>Pause</span></button>
      </div>
    </div>
    <div class="text-stack">
      <span class="eyebrow reveal">Welcome</span>
      <h2 id="place-title" class="reveal d1">There is a place <em>for you here.</em></h2>
      <p class="reveal d2">We want church to be a place where your entire family is encouraged to draw closer to Christ. Visiting somewhere new can be intimidating. We want to make sure that you feel comfortable and welcome when you walk into our doors. We have smiling faces waiting to greet you and we will show you where to go. Enjoy a cup of coffee and relax with us!</p>
      <a href="#coming" class="btn btn-primary reveal d3">Let Us Know You're Coming {ARROW}</a>
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 3. FAQS — accordion ======================= -->
<section class="section section-mist" aria-labelledby="faq-title">
  <div class="wrap faq-grid">
    <div class="text-stack">
      <span class="eyebrow reveal">FAQs</span>
      <h2 id="faq-title" class="reveal d1">Frequently Asked <em>Questions</em></h2>
      <p class="reveal d2">Still wondering about something? Send us a note and we'll be happy to help.</p>
      <a href="mailto:info@yourchurch.com" class="btn btn-outline reveal d3">Ask a Question</a>
    </div>
    <div class="accordion reveal" data-single>
{acc('What do I wear?', open_=True)}
{acc('What is a typical service like?')}
{acc('What do you have for my kids?')}
{acc('Where do I go when I arrive?')}
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 4. LET US KNOW YOU'RE COMING — list + form ======================= -->
<section class="section" id="coming" aria-labelledby="coming-title">
  <div class="wrap split">
    <div class="text-stack">
      <span class="eyebrow reveal">First Visit</span>
      <h2 id="coming-title" class="reveal d1">Let Us Know <em>You're Coming</em></h2>
      <p class="reveal d2">We can't wait to meet you! We want to make your first visit a great one, so let us know you're coming and we will:</p>
      <ul class="check-list reveal d3">
        <li>Meet you at our Welcome Center</li>
        <li>Help you get your kids checked into kids church</li>
        <li>Get you a cup of coffee and some refreshments</li>
        <li>Show you around our church building</li>
      </ul>
    </div>
    <div class="form-card reveal">
      <form class="form" data-success="We've got your details and we'll be watching for you. See you soon!">
        <div class="form-row">
          <label class="field"><span>First Name <em>*</em></span><input id="pyv-first" name="first" type="text" autocomplete="given-name" required></label>
          <label class="field"><span>Last Name</span><input id="pyv-last" name="last" type="text" autocomplete="family-name"></label>
        </div>
        <label class="field"><span>Email <em>*</em></span><input id="pyv-email" name="email" type="email" autocomplete="email" required></label>
        <label class="field"><span>When will you be visiting?</span><input id="pyv-date" name="date" type="date"><small>MM / DD / YYYY</small></label>
        <label class="field"><span>Will anybody be coming with you?</span><textarea id="pyv-guests" name="guests" placeholder="e.g. my spouse and two kids (ages 4 and 7)"></textarea></label>
        <button type="submit" class="btn btn-primary">Submit {ARROW}</button>
      </form>
    </div>
  </div>
</section>''',
 pyv_contact],
 comment='''  Sections (same as the original page):
    1. Banner "What To Expect"   2. There is a place for you here (video)   3. FAQs (accordion)
    4. Let Us Know You're Coming (list + form)   5. Service times, contact + map   + Footer''')

# ======================================================== ABOUT
values = [
 ('Worship &amp; Study', 'Through weekly Bible studies, worship gatherings, and small groups, we will learn more about God and grow in our knowledge and love for Him.', '<path d="M12 6c-2-1.5-5-2-8-2v14c3 0 6 .5 8 2 2-1.5 5-2 8-2V4c-3 0-6 .5-8 2zM12 6v14"/>'),
 ('Evangelism &amp; Outreach', 'By reaching out to and serving those around us, we will share God\'s love and His message of hope with the people in our community.', '<path d="M7 11.5V8a2 2 0 014 0v3M11 10V6a2 2 0 014 0v5M15 9a2 2 0 014 0v5a7 7 0 01-7 7h-1a7 7 0 01-6-3.4L3 15a2 2 0 013.4-2L7 14"/>'),
 ('Missions &amp; Sending', 'By making disciples and supporting fellow believers as they step out to launch new churches and ministries around the world, we will expand our reach to exhibit God\'s love to people across the globe.', '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/>'),
]
vcards = '\n'.join(f'''      <article class="value-card reveal{(' d' + str(i)) if i else ''}">
        <span class="value-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic}</svg></span>
        <h3>{t}</h3>
        <p>{d}</p>
      </article>''' for i, (t, d, ic) in enumerate(values))
members = '\n'.join(f'''      <article class="member reveal{(' d' + str(i % 3)) if i % 3 else ''}">
        <div class="member-photo">{SIL}
          <div class="member-social"><a href="mailto:info@yourchurch.com" aria-label="Email First &amp; Last Name">{MAIL}</a><a href="#" aria-label="Facebook">{FB}</a></div>
        </div>
        <div><h3>First &amp; Last Name</h3><p>Position / Title</p></div>
      </article>''' for i in range(6))
beliefs = ['Jesus', 'The Bible', 'Mankind', 'Salvation', 'Sin', 'The Trinity']
page('about', 'About', 'About Edwards Church: our values, our team and what we believe.',
 banner('About <em>Us</em>', 'About', 'img/banner-about.jpg', 'Congregation worshipping with hands raised', 'Love God. Love People.'),
 [f'''<!-- ======================= 2. OUR VALUES ======================= -->
<section class="section" aria-labelledby="values-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow eyebrow-center reveal">Who We Are</span>
      <h2 id="values-title" class="reveal d1">Our <em>Values</em></h2>
    </div>
    <div class="values">
{vcards}
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 3. OUR TEAM (placeholders until staff photos arrive) ======================= -->
<section class="section section-mist" aria-labelledby="team-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow eyebrow-center reveal">Leadership</span>
      <h2 id="team-title" class="reveal d1">Our <em>Team</em></h2>
    </div>
    <div class="team">
{members}
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 4. OUR BELIEFS — accordion ======================= -->
<section class="section" aria-labelledby="beliefs-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow eyebrow-center reveal">What We Believe</span>
      <h2 id="beliefs-title" class="reveal d1">Our <em>Beliefs</em></h2>
    </div>
    <div class="beliefs accordion reveal">
{chr(10).join(acc(b, open_=(i == 0)) for i, b in enumerate(beliefs))}
    </div>
  </div>
</section>''',
 CONTACT],
 comment='''  Sections (same as the original page):
    1. Banner "About Us"   2. Our Values (3)   3. Our Team (6 placeholders)   4. Our Beliefs (accordion, 6)
    5. Service times, contact + map   + Footer''')

# ======================================================== CONNECT
mins = [
 ('kids', 'Kids', 'img/kids.jpg', 'Children lifting their hands during kids church', 'We want church to be a place where your entire family is encouraged to draw closer to Christ—your kids included! That\'s why, during our Sunday morning worship services, we offer fun and engaging environments where children can learn and grow in faith as well. All our kids\' programs are designed to be safe places where children in our church can learn new and exciting things about God while being led and cared for by adult volunteers from our congregation. It\'s our hope to encourage children to not only discover new things about God, but also begin to understand how those things matter in their own lives.'),
 ('students', 'Students', 'img/students.jpg', 'Students worshipping together at a youth gathering', 'In student ministry, we strive to lead students to become passionate followers of Christ. By partnering with parents and trained leaders, our mission is to teach and inspire the next generation to be founded in their faith and confident in their Creator. Through regular Bible study and small group gatherings, we encourage students to walk boldly towards Christ, apply His truth to their lives, and develop strong, life-changing relationships with the God of the universe. We want our students to know Jesus so that they might be excited about sharing His name and making Him known to others. Our prayer is that the church would be the future of our world and our students, the future of the church.'),
 ('women', 'Women', 'img/women.jpg', 'A woman reading her Bible at a table', 'We offer several opportunities for women to get involved in ministries at our church designed to grow and strengthen their faith alongside others. It\'s our desire to create environments where other women in the same stages and phases of life can develop authentic relationships with one another while being encouraged to grab hold of how God\'s truth intersects with and impacts their lives. Be sure to check our our events page for any upcoming events!'),
 ('men', 'Men', 'img/men.jpg', 'A group of men praying together', 'Our Men\'s ministry programs all center on gathering as a community around the Word of God and living lives modeled after Christ. The goal of all of our Men\'s groups is to help challenge participants to live out their faith while impacting others with the power and truth of the Gospel. Be sure to stay connected and visit the events page for upcoming events and meeting times.'),
]
chips = '\n    <div class="banner-chips">' + ''.join(f'<a href="#{k}">{t}</a>' for k, t, *_ in mins) + '</div>'
msecs = []
for i, (k, t, img, alt, txt) in enumerate(mins):
    msecs.append(f'''<!-- ======================= {i + 2}. {t.upper()} ======================= -->
<section class="section{' section-mist' if i % 2 else ''} ministry-row" id="{k}" aria-labelledby="{k}-title">
  <div class="wrap split{' reverse' if i % 2 else ''}">
    <div class="split-media">
      <div class="photo reveal-img"><img src="{img}" alt="{alt}" width="1400" height="933" loading="lazy"></div>
    </div>
    <div class="text-stack">
      <span class="ministry-tag reveal">Ministries</span>
      <h2 id="{k}-title" class="reveal d1">{t}</h2>
      <p class="reveal d2">{txt}</p>
      <a href="#" data-build-href="/get-connected/" class="btn btn-primary reveal d3">Get Connected {ARROW}</a>
    </div>
  </div>
</section>''')
page('connect', 'Connect', 'Ministries at Edwards Church for kids, students, women and men.',
 banner('Our <em>Ministries</em>', 'Connect', 'gallery-7.jpg', 'Church members embracing in prayer', 'Find your place to grow in faith alongside others.', chips),
 msecs,
 comment='''  Sections (same as the original page):
    1. Banner "Our Ministries" (+ jump links)   2. Kids   3. Students   4. Women   5. Men   + Footer''')

# ======================================================== SERMONS
def sel(id_, label, opts):
    o = ''.join(f'<option value="{v}">{v}</option>' for v in opts)
    return f'<label class="field"><span>{label}</span><select id="{id_}" name="{id_}"><option value="">All</option>{o}</select></label>'
sermon_js = '''<script>
(function () {
  /* Sermon filters (mockup: filters the sermons listed on this page) */
  var form = document.getElementById('sermon-filters'), cards = document.querySelectorAll('.sermon'), empty = document.getElementById('no-sermons');
  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = ['speaker', 'series', 'topic', 'book'].every(function (k) { var v = form.elements[k].value; return !v || c.dataset[k] === v; });
      c.hidden = !ok; if (ok) shown++;
    });
    empty.hidden = shown > 0;
  }
  form.addEventListener('change', apply);
  form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
  form.addEventListener('reset', function () { setTimeout(apply); });
})();
</script>
'''
page('sermons', 'Sermons', 'Watch or listen to messages from Edwards Church.',
 banner('Sermons', 'Sermons', 'img/banner-sermons.jpg', 'Pastor preaching from the stage', 'Watch or listen to previous messages anytime.'),
 [f'''<!-- ======================= 2. SERMON ARCHIVE — filters + list (Sermon Manager shortcode in the build) ======================= -->
<section class="section section-mist" aria-label="Sermon archive">
  <div class="wrap">
    <form class="filters reveal" id="sermon-filters" aria-label="Filter sermons">
      {sel('speaker', 'Speaker', ['First and Last Name'])}
      {sel('series', 'Series', [])}
      {sel('topic', 'Topic', [])}
      {sel('book', 'Book', ['John'])}
      <button type="reset" class="btn btn-outline">Clear Filters</button>
    </form>

    <article class="sermon reveal" data-speaker="First and Last Name" data-series="" data-topic="" data-book="John">
      <a href="#" data-build-href="/sermon-archive/sample-sermon/" class="sermon-media" aria-label="Watch Sample Sermon">
        <img src="gallery-2.jpg" alt="" width="1400" height="933" loading="lazy">
        <span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l12.5-7.5z"/></svg></span>
      </a>
      <div class="sermon-body">
        <span class="sermon-date">Sunday, December 18, 2022</span>
        <h2><a href="#" data-build-href="/sermon-archive/sample-sermon/">Sample Sermon</a></h2>
        <div class="sermon-meta">
          <span><strong>Speaker:</strong> <a href="#">First and Last Name</a></span>
          <span><strong>Scripture:</strong> John 3:16</span>
        </div>
        <p>Lorem ipsum dolor sit amet, ex has autem posse percipitur, esse ullamcorper an eos, cum quod dolor a...</p>
        <div class="sermon-foot">
          <a href="#" class="pill">Sunday Morning</a>
          <div class="share">Share
            <a href="https://www.facebook.com/sharer/sharer.php?u=" target="_blank" rel="noopener" aria-label="Share on Facebook">{FB}</a>
            <a href="https://twitter.com/share?url=" target="_blank" rel="noopener" aria-label="Share on X">{XI}</a>
            <a href="mailto:?subject=Sample%20Sermon" aria-label="Share by email">{MAIL}</a>
          </div>
        </div>
      </div>
    </article>
    <p class="empty-state" id="no-sermons" hidden>No sermons match those filters. Try clearing them.</p>
  </div>
</section>'''],
 extra_js=sermon_js,
 comment='''  Sections (same as the original page):
    1. Banner "Sermons"   2. Filters (speaker, series, topic, book) + sermon list   + Footer
  In the build this is the Sermon Manager shortcode, styled to match.''')

# ======================================================== EVENTS
events_js = '''<script>
(function () {
  /* Events calendar (mockup of the Modern Events Calendar views: Monthly / List / Tile).
     Weekly event: Sunday Service, Sundays 10:00–11:30 am. */
  var EVENT = { title: 'Sunday Service', repeat: 'Weekly', desc: 'Join us Sundays at 10am as we worship together!', start: '10:00 am', end: '11:30 am', img: 'gallery-1.jpg', url: 'upcoming-events/sunday-service/' };
  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var now = new Date(), view = 'month', cur = new Date(now.getFullYear(), now.getMonth(), 1);
  var out = document.getElementById('cal-out'), title = document.getElementById('cal-title'), mSel = document.getElementById('cal-month'), ySel = document.getElementById('cal-year');
  MONTHS.forEach(function (m, i) { mSel.add(new Option(m, i)); });
  for (var y = 2022; y <= 2034; y++) ySel.add(new Option(y, y));
  function sundays(d) { var r = [], x = new Date(d.getFullYear(), d.getMonth(), 1); while (x.getMonth() === d.getMonth()) { if (x.getDay() === 0) r.push(new Date(x)); x.setDate(x.getDate() + 1); } return r; }
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function dateBadge(d) { return '<span class="ev-date"><b>' + d.getDate() + '</b><span>' + MONTHS[d.getMonth()].slice(0, 3) + '</span></span>'; }
  function render() {
    title.textContent = MONTHS[cur.getMonth()] + ' ' + cur.getFullYear();
    mSel.value = cur.getMonth(); ySel.value = cur.getFullYear();
    var list = sundays(cur), html = '';
    if (view === 'month') {
      html = '<div class="cal-grid" role="grid">' + ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(function (d) { return '<div class="cal-dow" role="columnheader">' + d + '</div>'; }).join('');
      var start = new Date(cur); start.setDate(1 - cur.getDay());
      for (var i = 0; i < 42; i++) {
        var d = new Date(start); d.setDate(start.getDate() + i);
        if (i >= 35 && d.getMonth() !== cur.getMonth()) break;
        var other = d.getMonth() !== cur.getMonth(), today = d.toDateString() === now.toDateString();
        html += '<div class="cal-day' + (other ? ' other' : '') + (today ? ' today' : '') + '" role="gridcell"><span class="cal-num">' + d.getDate() + '</span>';
        if (d.getDay() === 0 && !other) html += '<button type="button" class="cal-event" data-date="' + d.toISOString() + '">' + EVENT.title + '<small>' + EVENT.start + '</small></button>';
        html += '</div>';
      }
      html += '</div>';
    } else if (view === 'list') {
      html = '<div class="ev-list">' + list.map(function (d) {
        return '<article class="ev-item">' + dateBadge(d) + '<div><h3>' + EVENT.title + '</h3><p>' + EVENT.desc + '</p><div class="ev-time"><span>' + EVENT.start + ' – ' + EVENT.end + '</span><span class="badge">' + EVENT.repeat + '</span></div></div><button type="button" class="btn btn-outline" data-date="' + d.toISOString() + '">View Detail</button></article>';
      }).join('') + '</div>';
    } else {
      html = '<div class="ev-tiles">' + list.map(function (d) {
        return '<article class="ev-tile"><div class="ev-tile-img"><img src="' + EVENT.img + '" alt="" loading="lazy">' + dateBadge(d) + '</div><div class="ev-tile-body"><h3>' + EVENT.title + '</h3><p>' + EVENT.desc + '</p><div class="ev-time"><span>' + EVENT.start + ' – ' + EVENT.end + '</span><span class="badge">' + EVENT.repeat + '</span></div><button type="button" class="btn btn-primary" data-date="' + d.toISOString() + '">View Detail</button></div></article>';
      }).join('') + '</div>';
    }
    if (!list.length) html = '<p class="empty-state">No event found!</p>';
    out.innerHTML = html;
  }
  function move(n) { cur = new Date(cur.getFullYear(), cur.getMonth() + n, 1); render(); }
  document.getElementById('cal-prev').addEventListener('click', function () { move(-1); });
  document.getElementById('cal-next').addEventListener('click', function () { move(1); });
  document.getElementById('cal-today').addEventListener('click', function () { cur = new Date(now.getFullYear(), now.getMonth(), 1); render(); });
  mSel.addEventListener('change', function () { cur = new Date(cur.getFullYear(), +mSel.value, 1); render(); });
  ySel.addEventListener('change', function () { cur = new Date(+ySel.value, cur.getMonth(), 1); render(); });
  document.querySelectorAll('.seg button').forEach(function (b) {
    b.addEventListener('click', function () {
      view = b.dataset.view;
      document.querySelectorAll('.seg button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      render();
    });
  });
  /* Event detail dialog */
  var dlg = document.getElementById('ev-dialog');
  out.addEventListener('click', function (e) {
    var t = e.target.closest('[data-date]'); if (!t) return;
    var d = new Date(t.dataset.date);
    dlg.querySelector('[data-f="date"]').textContent = d.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  });
  dlg.querySelector('.close').addEventListener('click', function () { dlg.close ? dlg.close() : dlg.removeAttribute('open'); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  render();
})();
</script>
'''
CHEV_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
page('events', 'Events', 'Upcoming events at Edwards Church.',
 banner('Events', 'Events', 'gallery-4.jpg', 'Congregation standing in worship', 'There is always something happening. Come and be part of it.'),
 [f'''<!-- ======================= 2. CALENDAR — Monthly / List / Tile (Modern Events Calendar shortcode in the build) ======================= -->
<section class="section" aria-label="Events calendar">
  <div class="wrap">
    <div class="cal-bar reveal">
      <div class="cal-nav">
        <button type="button" class="icon-btn" id="cal-prev" aria-label="Previous month">{CHEV_L}</button>
        <h2 id="cal-title" aria-live="polite">Month</h2>
        <button type="button" class="icon-btn" id="cal-next" aria-label="Next month">{CHEV_R}</button>
        <button type="button" class="pill" id="cal-today" style="border:0;cursor:pointer;font:inherit;font-size:.78rem;font-weight:600">Today</button>
      </div>
      <div class="cal-nav">
        <div class="cal-selects">
          <select id="cal-month" aria-label="Select Month"></select>
          <select id="cal-year" aria-label="Select Year"></select>
        </div>
        <div class="seg" role="group" aria-label="Calendar view">
          <button type="button" data-view="month" aria-pressed="true">Monthly</button>
          <button type="button" data-view="list" aria-pressed="false">List</button>
          <button type="button" data-view="tile" aria-pressed="false">Tile</button>
        </div>
      </div>
    </div>
    <div id="cal-out" class="reveal"></div>
  </div>
</section>

<dialog class="ev-dialog" id="ev-dialog" aria-label="Event details">
  <button type="button" class="close" aria-label="Close">{CLOSE}</button>
  <img src="gallery-1.jpg" alt="" width="1800" height="1185">
  <div class="ev-dialog-body">
    <span class="sermon-date" data-f="date">Sunday</span>
    <h3>Sunday Service</h3>
    <div class="ev-time"><span>10:00 am – 11:30 am</span><span class="badge">Weekly</span></div>
    <p>Join us Sundays at 10am as we worship together!</p>
    <div class="sermon-foot">
      <a href="#" class="btn btn-primary">View Detail {ARROW}</a>
      <div class="share">Share
        <a href="https://www.facebook.com/sharer/sharer.php?u=" target="_blank" rel="noopener" aria-label="Share on Facebook">{FB}</a>
        <a href="https://twitter.com/share?url=" target="_blank" rel="noopener" aria-label="Share on X">{XI}</a>
        <a href="https://www.linkedin.com/shareArticle?mini=true&amp;url=" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{LI}</a>
        <a href="mailto:?subject=Sunday%20Service" aria-label="Share by email">{MAIL}</a>
      </div>
    </div>
  </div>
</dialog>'''],
 extra_js=events_js,
 comment='''  Sections (same as the original page):
    1. Banner "Events"   2. Calendar with Monthly / List / Tile views + event detail   + Footer
  In the build this is the Modern Events Calendar shortcode, styled to match.''')

# ======================================================== GIVE
page('give', 'Give', 'Give to Edwards Church on Sunday, online or by mail.',
 banner('Give', 'Give', 'give/wheat-field.jpg', 'Golden wheat field ready for harvest', 'Giving is an act of worship.'),
 [f'''<!-- ======================= 2. WHY WE GIVE ======================= -->
<section class="section" aria-labelledby="why-title">
  <div class="wrap split">
    <div class="split-media">
      <div class="photo reveal-img"><img src="give/plant-in-hands.jpg" alt="Cupped hands holding a young green plant" width="1600" height="1067" loading="lazy"></div>
    </div>
    <div class="text-stack">
      <span class="eyebrow reveal">Generosity</span>
      <h2 id="why-title" class="reveal d1">Why We <em>Give</em></h2>
      <p class="reveal d2">Giving is an an act of worship and obedience from a heart surrendered to Christ. It is a choice we make to follow God's instruction for us. The church doesn't need anything from you. God wants to do something in you. God certainly doesn't need anything from us, it's all His anyway. We give out of our need to act on our faith.</p>
      <a href="#give-online" class="btn btn-primary reveal d3">Give Now {ARROW}</a>
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 3. WAYS TO GIVE ======================= -->
<section class="section section-mist" aria-labelledby="ways-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow eyebrow-center reveal">Ways to Give</span>
      <h2 id="ways-title" class="reveal d1">Ways to <em>Give</em></h2>
    </div>
    <div class="ways">
      <article class="way reveal">
        <span class="value-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10h18l-2 10H5z"/><path d="M8 10l4-6 4 6"/></svg></span>
        <h3>Give on Sunday</h3>
        <p>During service, feel free to place your offering in our giving baskets as they are passed during service.</p>
      </article>
      <article class="way featured reveal d1" id="give-online">
        <span class="value-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="12" rx="2"/><path d="M2 20h20M9 11l2 2 4-4"/></svg></span>
        <h3>Give Online</h3>
        <p>Using our safe, secure online giving platform, you can feel safe about your gift. Login to get started.</p>
        <a href="#" class="btn btn-accent">Give Now {ARROW}</a>
      </article>
      <article class="way reveal d2">
        <span class="value-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span>
        <h3>Give By Mail</h3>
        <address><strong>Edwards Church</strong><br>1234 Street<br>My Town, XX 12345</address>
      </article>
    </div>
  </div>
</section>'''],
 comment='''  Sections (same as the original page):
    1. Banner "Give"   2. Why We Give (image + text + Give Now)   3. Ways to Give (Sunday, Online, Mail)   + Footer''')

# ======================================================== WATCH LIVE
live_extra = f'''
    <span class="live-status"><i aria-hidden="true"></i>Sundays at 10am</span>
    <div class="live-player video-card">
      <iframe src="https://www.youtube.com/embed/4FZBkcOA6jI" title="Edwards Church live stream" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>'''
page('watch-live', 'Watch Live', 'Watch the Edwards Church live stream on Sundays at 10am.',
 banner('Watch <em>Live</em>', 'Watch Live', 'watch-live.jpg', 'Congregation worshipping during a service', '', live_extra, cls='live-banner'),
 [f'''<!-- ======================= 2. GIVE ONLINE ======================= -->
<section class="section" aria-labelledby="giveonline-title">
  <div class="wrap split">
    <div class="split-media">
      <div class="photo reveal-img"><img src="give/harvest-field.jpg" alt="Wheat stalks ready for harvest" width="2000" height="1333" loading="lazy"></div>
    </div>
    <div class="text-stack">
      <span class="eyebrow reveal">Generosity</span>
      <h2 id="giveonline-title" class="reveal d1">Give <em>Online</em></h2>
      <p class="reveal d2">Thank you for your partnership in ministry with us. We're so grateful for the financial gifts given to allow us to continue the work of accomplishing God's mission and vision for our church. Please know your generous giving is making a difference for the glory of God at our church.</p>
      <a href="give.html" class="btn btn-primary reveal d3">Give Now {ARROW}</a>
    </div>
  </div>
</section>''',
 f'''<!-- ======================= 3. LET US PRAY FOR YOU — image + form ======================= -->
<section class="section section-mist" aria-labelledby="pray-title">
  <div class="wrap split reverse">
    <div class="split-media">
      <div class="photo reveal-img"><img src="gallery-5.jpg" alt="Hands folded in prayer over an open Bible" width="1400" height="933" loading="lazy"></div>
    </div>
    <div class="text-stack">
      <span class="eyebrow reveal">Prayer</span>
      <h2 id="pray-title" class="reveal d1">Let Us <em>Pray for You</em></h2>
      <div class="form-card reveal d2" style="width:100%">
        <form class="form" data-success="Our prayer team has received your request and will be praying for you.">
          <div class="form-row">
            <label class="field"><span>First Name <em>*</em></span><input id="pr-first" name="first" type="text" autocomplete="given-name" required></label>
            <label class="field"><span>Last Name <em>*</em></span><input id="pr-last" name="last" type="text" autocomplete="family-name" required></label>
          </div>
          <div class="form-row">
            <label class="field"><span>Phone</span><input id="pr-phone" name="phone" type="tel" autocomplete="tel"></label>
            <label class="field"><span>Email <em>*</em></span><input id="pr-email" name="email" type="email" autocomplete="email" required></label>
          </div>
          <label class="field"><span>How can we pray for you? <em>*</em></span><textarea id="pr-request" name="request" required></textarea></label>
          <button type="submit" class="btn btn-primary">Submit {ARROW}</button>
        </form>
      </div>
    </div>
  </div>
</section>'''],
 comment='''  Sections (same as the original page):
    1. Banner "Watch Live" + Sundays at 10am + YouTube player   2. Give Online   3. Let Us Pray for You (form)   + Footer''')
print('built')
