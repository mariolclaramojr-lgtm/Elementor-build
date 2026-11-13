# Hayford — Cornerstone build (rrnewhayford.wpenginepowered.com)

Rebuild of `hayford-redesign/` (HTML mockup) in Themeco Pro 6.9.8 / Cornerstone 7.9.8, Integrity stack.

## Global layer
- **Global Colors** (Cornerstone › Global Colors): Ink, Ink 2, Ink Soft, Paper, Sand, Muted, Accent, Accent Dark,
  Accent Light, Line, Line on Dark, Live, White. Existing ids kept (Brand Primary = Ink, Accent color = Accent …).
- **Global Fonts**: Body Copy = DM Sans, Headings = Manrope, Accent (headings italic) = Fraunces.
- **Theme Options**: page bg Paper, body Ink Soft, headings Ink 800 with negative tracking, links Accent,
  classic buttons pill Ink→Accent, container 92% / 1240px.
- **Global CSS** (`global.css` here = Theme Options › CSS, between HAYFORD markers): maps every global colour/font to
  `var(--hf-…)` via `%%post color%%global-color:<id>%%/post%%`, heading accent style, Gravity Forms styling.
- **Heading accent**: an italic word (`<em>`) in a heading is styled by global CSS as the serif accent (light tint over photos /
  dark backgrounds). It shows in the Cornerstone editor and on the site; editors use the italic button. No global JS is needed.

## Documents
| What | ID |
|---|---|
| Home — Redesign (draft) | 548 |
| Thank You page (published, /thank-you/) | 613 |
| Components preview (internal draft — delete when done) | 594 |
| Header — Main (transparent over banner) | 585 |
| Header — Solid (posts, sermons, events) | 586 |
| Footer (entire site) | 587 |
| Component — Closing CTA | 591 |
| Component — Service Times + Contact + Map | 592 |
| Component — Give Online (used on Watch Live) | 631 |
| Gravity Forms — Contact / Connection Card | 1 |
| Gravity Forms — Let Us Know You're Coming | 9 |
| Gravity Forms — Prayer Request | 10 |
| Sample sermons (meta `_hf_sample`=1) | 605, 606, 607, 608 |
| Sample events (meta `_hf_sample`=1) | 609, 610, 611, 612 |

Menus: Main (menu:2), Mobile Menu (menu:13), Footer Explore (menu:14), Footer Join Us (menu:15), Footer Quick Links (menu:16), get-connected (menu:11), take-a-step (menu:12).
Media: logo-white=538, logo-dark=539, site-icon=540, hero_poster=541, hero_mp4=542, hero_webm=543, img_messages=544, img_events=545, img_welcome=546, img_cta=547, logo-white-header=588, logo-dark-header=589, logo-white-footer=590, sermon1=597, sermon2=598, sermon3=599, sermon4=600, event1=601, event2=602, event3=603, event4=604.

## Published (2026-11-12)
- The new homepage is live on Home (page 8, the front page). The previous Home layout is in Cornerstone backups (index 0) for page 8.
- Header 585 is assigned to the front page, Home (8), draft 548 and Thank You (613). Header 186 keeps the other old pages until they are rebuilt.

## Remaining checklist
1. As each inner page is rebuilt, move it from header 186 to header 585 assignments.
2. Appearance › Customize › Site Identity › Site Icon → `hayford-site-icon.png` (media 540).
3. MEC › Locations → "Hayford Church": add the address (events already point at it).
4. Delete page 594 and the "Test Submission (QA)" form entries.

## Rebuilding
`build/` holds the generators (`cs_home.py`, `cs_layouts.py`, `cs_components.py`, `cs_thanks.py`); `hf.py` talks to the
CSMCP endpoint using the cs-mcp server registered in Claude Code (credentials are read from the local Claude config,
never stored here).

## Inner pages (built 2026-11-12, `build/cs_pages.py`)
Written onto the existing pages so URLs are unchanged (previous trees backed up by Cornerstone and locally):
About (11), Plan Your Visit (487), Connect (12), Get Connected (492), Events (63), Give (14), Messages (167), Watch Live (490).
All are assigned to header 585; the old header 186 has no assignments left.
- Plugins: Events = `[MEC id="53"]` (Monthly View), Messages = `[smpro_archive per_page="15"]` — both in Raw Content,
  styled from global CSS sections 3 (Sermon Manager) and 4 (Modern Events Calendar).
- Forms: Plan Your Visit = GF 9, Get Connected = GF 1, Watch Live = GF 10 (all redirect to /thank-you/).
- Components reused: Service Times + Contact + Map on About and Plan Your Visit; Give Online on Watch Live.

## Image review (2026-11-12)
Every image on the site was checked for church-appropriate content (modest dress; no parties or alcohol; focus on worship,
fellowship and community). Replaced:
- Thanksgiving Community Dinner event: photo with beer/wine glasses → church potluck line (media 648).
- Plan Your Visit "Let Us Know You're Coming": party-style photo → greeters welcoming guests at the church doors (649).
- "Love" sermon series artwork (unrelated marketing graphic) → sermons moved to series "Love Never Fails" (no artwork),
  so their own church photos show; Demo Sermon given the sanctuary photo (650).
- Sunday Service event: grey 1200x628 placeholder → sanctuary photo (650).

## Search (2026-11-12)
- Search results = Pro archive layout 657 "Hayford — Search Results" (`build/cs_search.py`), assigned to `archive:search`:
  dark banner with the query + search box, result cards (main-query looper, linked cards with excerpt + "Read more"),
  and a "We couldn't find a match" panel with popular links (both switched by the `archive:have-posts` condition).
- Header 586 (solid) is now the site-wide fallback; header 585 also covers search results.
- Every page has a short excerpt (used in results). Global CSS section 5 hides Sermon Manager's injected card in excerpts.
- About beliefs + Plan Your Visit FAQ use "Accordion Item (Elements)" so answers are real Text elements.
- Test: `node build/searchtest.js` (23 queries, every result link, header icon, results-page box, mobile width).
- Known: accordion answers are not searchable while Cornerstone content storage is "shortcode" (Settings › Advanced).
  The 2017 theme demo portfolio item "Demo Sermon" (id 29) still shows in results — set it to draft to hide it.

## Footer social icons
Linked to Theme Options › Social (x_social_*) via {{dc:theme:x_social_...}}. Each icon (Facebook, Instagram, YouTube, X, TikTok,
Vimeo, LinkedIn, Pinterest, WhatsApp, SoundCloud, RSS) shows only when its Theme Options field has a URL; opens in a new tab.

## Favicon
Set via global JS (Theme Options › JS, global.js): adds favicon + apple-touch-icon pointing to media 540 on every page.
Recommended permanent fix: Appearance › Customize › Site Identity › Site Icon › hayford-site-icon.png (the JS steps aside automatically once that is set).

## Logo (2026-11-13)
Sprout-in-arch mark + "Hayford" (Fraunces) / CHURCH (DM Sans). Vector files in hayford-redesign/logo/. Site PNGs (2x per display size,
because Pro caps a scaling image at half its pixel height): white 40/34/52 = media 675/676/677, dark 40/34 = 678/679, site icon 674.

## Event cards (2026-11-13)
Events page (63) gets a 3-column card grid of upcoming events **below** the calendar: section "3. Upcoming events (cards)"
(`#upcoming-events`, `build/cs_pages.py` `events()`): "Mark your calendar" eyebrow + "Upcoming *Events*" heading, then a Raw Content
element with `[hf_event_cards count="6" columns="3"]`.
- The shortcode comes from the small site plugin **Hayford Event Cards** (`plugin/hayford-event-cards/`, upload `plugin/hayford-event-cards.zip`
  at Plugins › Add New › Upload). CSS ships with the plugin (`assets/event-cards.css`) and uses the global `var(--hf-…)` tokens.
- Data: MEC's occurrence table (`{prefix}mec_dates`), so cards are ordered by next occurrence; a repeating event shows once with its next
  date and an "Every Sunday"-style label, linking to `?occurrence=Y-m-d`. Featured image (16:10), date badge, category pill, date + time,
  location (MEC location), 22-word excerpt, "Event details". Whole card is the link.
- Attributes: `count` (6, max 24), `columns` (3; 1–4 — tablet ≤978px caps at 2, mobile ≤767px is 1), `category` (mec_category slugs/names/ids,
  comma-separated), `excerpt` (words, 0 hides), `group` ("no" = one card per occurrence), `image` ("no" hides photos), `heading` (h2/h3/h4), `class`.
- Usable anywhere (pages, Global Blocks, homepage): e.g. `[hf_event_cards count="3" category="worship"]`.
