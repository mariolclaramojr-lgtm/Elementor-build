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
- **Visit Us – Service Times, Contact + Map** (id 354): place with `{"_type":"global-block","global_block_id":"354"}`.

## Pages
- Home (Redesign Draft) — page 355 (draft, template-blank-4.php). Built by `build/home.py`.

## Build scripts
`build/cs_lib.py` (element builders, native elements only), `build/home.py`, `build/run.py`.
`media.json` = Media Library ids, `state.json` = created ids. Credentials are NOT stored here.
