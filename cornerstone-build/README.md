# Lewis Church — Cornerstone build

Rebuilds the `lewis-redesign/` HTML design on the WordPress site (Pro 6.7 / Cornerstone 7.7)
with native Cornerstone elements, through the site's CSMCP endpoint.

Set `CS_MCP_AUTH` to `Basic <base64 of user:application-password>` before running anything.

| File | What it does |
|---|---|
| `globals.py` | Global Colors, Global Fonts (Fraunces / Inter), theme options |
| `upload.py` | Uploads the design images and videos to the Media Library (`media.json` maps them) |
| `lc.py` | Element builders: sections, rows, eyebrows, headings, buttons, framed images, shared blocks |
| `pages.py` | One function per page (home, about, connect, plan, watch, give, messages, events) |
| `layouts.py` | Pro header bars (top bar, nav, title hero) and footer |
| `forms.py` | Creates the Gravity Forms used on Plan Your Visit, Watch Live (prayer) and Get Connected |
| `header_main.py` | Transparent header and the list of pages it is assigned to |
| `headers.py` | Creates the title-hero headers for posts, sermons, events and archives, with their assignments |
| `run.py` | `python3 run.py <page> <post id>` saves a page tree |
| `lewis.css` / `applycss.py` | The only global CSS: heading accent word + Gravity Forms, Sermon Manager Pro and MEC styling |

Page IDs: home 8, about 11, connect 12, plan 92, watch 103, give 14, messages 82, events 88, get_connected 113.
Every page save is backed up by the plugin first (`cs_list_backups` / `cs_restore_backup`).
