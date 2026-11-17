# Edwards — Cornerstone build

Site: rrnewedwards.wpenginepowered.com (Pro 6.9.8 / Cornerstone 7.9.8). Follows `../HTML-TO-CORNERSTONE.md`.

## Global layer (done)
- **Global Colors** added (existing ones kept): Edwards Slate, Slate Deep, Accent `#DB783C`, Mist, Text, Text Soft,
  Rule, On Dark, plus gradient overlays (Overlay – Bottom Fade / Left Fade / Tile).
- **Global Font**: Edwards Sans (Plus Jakarta Sans 400/500/600/700).
- **Global site settings** (`cs_option_data`): body font/colour, H1–H6, links, inputs, submit buttons, 1240px container —
  all pointing at the Global Colors/Font.
- **Global CSS / JS**: `global.css`, `global.js` (between `EDWARDS REDESIGN START/END` markers). Colours in CSS use
  `%%post color%%global-color:…%%/post%%`, fonts `%%post font-family%%edwards-sans%%/post%%`.
- Originals backed up in `backups/2026-11-17-original/`.

## Components
- **Footer – Edwards** (id 376) — placed in the Pro footer **Edwards Footer** (377, entire site).
- **Visit Us – Service Times, Contact + Map** (id 354): place with `{"_type":"global-block","global_block_id":"354"}`.

## Header
- **Main Header** (186) rebuilt in place: Edwards logo (Media 361), Main menu (menu:2), Social ×2, Plan Your Visit button,
  mobile off-canvas menu (menu:21), sticky bar — solid on scroll via global CSS `.ed-header-bar.x-bar-fixed`.
  Original JSON in `backups/2026-11-17-original/header-186-main.json`.

## Demo content
- 4 sermons (Sermon Manager, ids 378–381) and 4 events (MEC, ids 382–385) — `build/demo_content.py`.

## Pages
- **Home — live** (page 8, template-blank-4.php), published 2026-11-17 from `build/home.py`. Previous version: `cs_list_backups 8` index 0.
- Home (Redesign Draft) — page 355, draft copy used for review.

## Build scripts
`build/cs_lib.py` (element builders, native elements only), `build/home.py`, `build/run.py`.
`media.json` = Media Library ids, `state.json` = created ids. Credentials are NOT stored here.

## Inner pages (live, 2026-11-17) — `build/inner.py`, `build/run_inner.py`
Plan Your Visit 204 · About 11 · Connect 12 · Sermons 167 (`[smpro_archive per_page="9"]`) · Events 63 (`[MEC id="52"]`) ·
Give 14 · Watch Live 221. Forms: Gravity Forms #3 (Let Us Know You're Coming) and #7 (Prayer Request) via Form Integration.
Plugin styling (Gravity Forms, Sermon Manager, MEC) is in `global.css` (PLUGINS block), all colours/fonts as Cornerstone globals.

## Headers
Main Header 186 · Archive Header 280 (dynamic archive title) · Blog Header 267 · Single Header 414 (sermons + events, post title).
Sample Sermon (166) moved to trash; Sunday Service event (65) got a featured image.
