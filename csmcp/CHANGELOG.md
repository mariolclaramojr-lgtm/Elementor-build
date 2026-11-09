# CSMCP changelog

## 0.8.0 — catch up with Cornerstone 7.6–7.9.8 (Pro 6.6–6.9.8)

**Content storage (Cornerstone 7.6+, default on new sites since 7.7)**
- Detects the site's storage mode (`cs_document_build_as_html`) and checks, for each page, whether
  post_content is HTML or `[cs_content]` shortcodes and whether it belongs to that page.
- `cs_create_page` with `clone_from` now regenerates post_content and compiled CSS for the new page.
  Before, the clone kept the source page's HTML (element ids `e<source>-e…`), so SEO and search
  plugins read the wrong page's content.
- Saves clear Cornerstone's render caches first, so HTML storage doesn't pick up stale output.
- `cs_save_element_tree` ignores `post_content` on HTML-storage sites and whenever Cornerstone's
  own save ran, and says so in the response.
- New tool **`cs_content_storage`**: report the mode, list stale or mismatched pages, and rebuild
  them through Cornerstone (`repair` / `repair_invalid`). It backs up each page first.
- `cs_environment`, `cs_list_pages`, `cs_get_page`, `cs_save_element_tree`, `cs_update_element` and
  `cs_restore_backup` now report storage status.

**Globals and components**
- New tool **`cs_globals`**: Global Colors, Fonts and font config. It uses `cs_color_get_stored()`
  and `cs_fonts_get_config()` (7.7.9+) when present. It also lists any Global Variables options
  (7.9.0); their option names are guessed from a name pattern, not confirmed.
- New tool **`cs_component_usage`**: lists the pages, headers, footers, layouts and components that
  place a component, like the usage list in Cornerstone 7.9.4.

**Other**
- `cs_purge_cache` also fires `cs_purge_all` and clears Cornerstone's per-post render state.
- The agent instructions now cover the newer elements (Table, Menu Looper, User Looper), Global
  Variables, Custom Document Assets and the Library tab (formerly Templates).
- MCP protocol version `2025-11-25` is accepted.
