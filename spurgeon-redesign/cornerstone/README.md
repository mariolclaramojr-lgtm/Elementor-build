# Spurgeon — Cornerstone build

The HTML design in `../` rebuilt on the Spurgeon WordPress site (Themeco Pro 6.9 + Cornerstone 7.9) through the CSMCP plugin's MCP tools.

| File | What it does |
|---|---|
| `spurgeon-global.css` | All custom CSS. Lives in **Theme Options › Global CSS** between the `SPURGEON REDESIGN START/END` markers (existing sermon rules above it are kept). |
| `csel.py` | Helpers that build native Cornerstone elements (section, row, column, headline, text, button, image, accordion, map, video, form-integration, breadcrumbs, social). |
| `build_header_footer.py` | Updates **Header - Main** (#131) and creates **Footer - Main** (#181), both site-wide. |
| `build_git.py` | **Get in Touch** Cornerstone Component (#182), placed on Home and About as a global-block element. |
| `build_pages.py` | Rebuilds Home, Plan Your Visit, About, Connect, Get Connected, Watch Live, Messages, Events and Give on their existing page IDs (slugs unchanged). |
| `sample-content/` | `sermons.py` / `events.py`: the 6 sample sermons (Sermon Manager Pro) and 6 sample events (MEC, via its own save routine). Run with `MCPDIR` pointing at the folder holding `lib.py`. |
| `build_title_headers.py` | Pro Headers with a photo title band for sermon + event archives (#218), singles (#219) and the Messages archive (#220). |

Global Colors added: Cream, Sand, Ink, Ink Soft, Cyan Ink, White (Brand Primary is the Spurgeon cyan). Global Fonts: Headings → Bricolage Grotesque, Body Copy → DM Sans.
Every page write was backed up automatically by Cornerstone (`cs_list_backups` / `cs_restore_backup`).

## Plugin output styling (shortcodes)

All in `spurgeon-global.css`, no plugin files touched:

- **Sermon Manager Pro**: filter row (Filter label + 4 hairline selects), 3/2/1-column cards (rounded 16:10 image, date + series tag, title, speaker, 3-line excerpt, book/topic/service chips; AddToAny hidden on cards), single message (meta chips, lead paragraph, share row; title lives in the page header).
- **Modern Events Calendar**: minimal toolbar (search, month/year, Monthly/List/Tile toggle), list cards with date block and View Detail, monthly grid with cyan event dots and a day panel, tile cards with photo overlay, single event (photo, meta card, export buttons, dark countdown, share icons).
- Archive/single title bars match the page hero height (378px at 1440 and 390).
