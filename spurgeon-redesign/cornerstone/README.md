# Spurgeon — Cornerstone build

The HTML design in `../` rebuilt on the Spurgeon WordPress site (Themeco Pro 6.9 + Cornerstone 7.9) through the CSMCP plugin's MCP tools.

| File | What it does |
|---|---|
| `spurgeon-global.css` | All custom CSS. Lives in **Theme Options › Global CSS** between the `SPURGEON REDESIGN START/END` markers (existing sermon rules above it are kept). |
| `csel.py` | Helpers that build native Cornerstone elements (section, row, column, headline, text, button, image, accordion, map, video, form-integration, breadcrumbs, social). |
| `build_header_footer.py` | Updates **Header - Main** (#131) and creates **Footer - Main** (#181), both site-wide. |
| `build_git.py` | **Get in Touch** Cornerstone Component (#182), placed on Home and About as a global-block element. |
| `build_pages.py` | Rebuilds Home, Plan Your Visit, About, Connect, Get Connected, Watch Live, Messages, Events and Give on their existing page IDs (slugs unchanged). |
| `build_title_headers.py` | Pro Headers with a photo title band for sermon + event archives (#218), singles (#219) and the Messages archive (#220). |

Global Colors added: Cream, Sand, Ink, Ink Soft, Cyan Ink, White (Brand Primary is the Spurgeon cyan). Global Fonts: Headings → Bricolage Grotesque, Body Copy → DM Sans.
Every page write was backed up automatically by Cornerstone (`cs_list_backups` / `cs_restore_backup`).
