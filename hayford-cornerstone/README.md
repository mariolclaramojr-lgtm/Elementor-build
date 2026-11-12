# Hayford — Cornerstone build (rrnewhayford.wpenginepowered.com)

Rebuild of `hayford-redesign/` (HTML mockup) in Themeco Pro 6.9.8 / Cornerstone 7.9.8, Integrity stack.

## Global layer
- **Global Colors** (Cornerstone › Global Colors): Ink, Ink 2, Ink Soft, Paper, Sand, Muted, Accent, Accent Dark,
  Accent Light, Line, Line on Dark, Live, White. Existing ids kept (Brand Primary = Ink, Accent color = Accent …).
- **Global Fonts**: Body Copy = DM Sans, Headings = Manrope, Accent Serif = Instrument Serif.
- **Theme Options**: page bg Paper, body Ink Soft, headings Ink 800 with negative tracking, links Accent,
  classic buttons pill Ink→Accent, container 92% / 1240px.
- **Global CSS** (`global.css` here = Theme Options › CSS, between HAYFORD markers): maps every global colour/font to
  `var(--hf-…)` via `%%post color%%global-color:<id>%%/post%%`, heading accent style, Gravity Forms styling.
- **Global JS** (`global.js` = Theme Options › JS): heading accent (H1/H2 last word / last two words). Editors type plain text.

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
