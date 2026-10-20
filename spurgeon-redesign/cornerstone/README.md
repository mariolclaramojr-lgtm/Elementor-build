# Spurgeon — Cornerstone build

The HTML design in `../` rebuilt on the Spurgeon WordPress site (Themeco Pro 6.9 + Cornerstone 7.9) through the CSMCP plugin's MCP tools.

| File | What it does |
|---|---|
| `spurgeon-global.css` | Global CSS (**Theme Options › CSS**, between the `SPURGEON REDESIGN START/END` markers). Only what Cornerstone settings can't reach: Gravity Forms, Sermon Manager Pro and MEC output. |
| `csel.py` | Helpers that build native Cornerstone elements with their look in the elements' own settings: section padding/background, row width, card columns (bg, border, radius, padding), headline/text typography, button colors and hover states, round images, icons, breadcrumbs, map/video frames. Responsive values use Cornerstone breakpoint data. |
| `square_images.py` | Uploads square copies of photos used in round images (the circle comes from the Image element's border radius). Cached in `square_images.json`. |
| `build_header_footer.py` | **Header - Main** (#131, priority 10) and **Footer - Main** (#181). The header logo and Plan Your Visit button are Components (**Logo** #288, **Plan Your Visit Button** #289) shared by both headers. Footer Follow icons read Theme Options › Social. |
| `build_git.py` | **Get in Touch** Cornerstone Component (#182), placed on Home and About as a global-block element. |
| `build_pages.py` | Rebuilds Home, Plan Your Visit, About, Connect, Get Connected, Watch Live, Messages, Events and Give on their existing page IDs (slugs unchanged). |
| `sample-content/` | `sermons.py` / `events.py`: the 6 sample sermons (Sermon Manager Pro) and 6 sample events (MEC, via its own save routine). Run with `MCPDIR` pointing at the folder holding `lib.py`. |
| `build_title_headers.py` | **Header - Sermons & Events** (#287): one Pro Header for every sermon/event archive and single. The title is chosen by element Show Conditions (post title on singles, archive title on taxonomy pages, "Messages"/"Events" on the post-type archives). |

Global Colors added: Cream, Sand, Ink, Ink Soft, Cyan Ink, White (Brand Primary is the Spurgeon cyan). Global Fonts: Headings → Bricolage Grotesque, Body Copy → DM Sans.
Every page write was backed up automatically by Cornerstone (`cs_list_backups` / `cs_restore_backup`).

## Plugin output styling (shortcodes)

All in `spurgeon-global.css`, no plugin files touched:

- **Sermon Manager Pro**: filter row (Filter label + 4 hairline selects), 3/2/1-column cards (rounded 16:10 image, date + series tag, title, speaker, 3-line excerpt, book/topic/service chips; AddToAny hidden on cards), single message (meta chips, lead paragraph, share row; title lives in the page header).
- **Modern Events Calendar**: minimal toolbar (search, month/year, Monthly/List/Tile toggle), list cards with date block and View Detail, monthly grid with cyan event dots and a day panel, tile cards with photo overlay, single event (photo, meta card, export buttons, dark countdown, share icons).
- Archive/single title bars match the page hero height (378px at 1440 and 390).

## Styling approach

Pages, the Get in Touch component, header, footer and title headers carry their design in Cornerstone element settings
(Design, Typography, Border, Background, Flexbox, Position), editable in the builder's Inspector. Classes such as
`sp-label` or `sp-card` are kept only as labels. Global CSS is limited to plugin output. The hero ticker is a native Slider in Marquee mode.
