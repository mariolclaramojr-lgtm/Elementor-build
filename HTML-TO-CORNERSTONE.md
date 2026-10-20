# HTML → Cornerstone Playbook

How we take a church-site design from an HTML mockup to an editable Themeco Pro / Cornerstone site,
based on the Lewis rebuild (lewistheme.wpengine.com). Follow it top to bottom for a new design.

---

## 1. Ground rules (non-negotiable)

1. **Keep the client's section count.** Redesign each page with the same number of sections as the
   original; restyle, don't restructure.
2. **Clients never touch code.** No HTML in headings, no inline styles, no hand-typed classes the
   editor has to remember. If a look needs code, it goes in the global CSS/JS and applies
   automatically.
3. **Global before local.** Colours → Global Colors, fonts → Global Fonts, shared styling → global
   CSS, shared header pieces → Components. Page-level custom CSS is a last resort.
4. **Native elements over Raw Content.** Build with Headline, Text, Button, Image, Div, Row/Column,
   Accordion, Video, Map, Form Integration. Raw Content only for plugin shortcodes.
5. **Draft first, then live.** Test risky changes on a draft clone; every write is backed up.
6. **Use stock photos** (Unsplash) in the mockup; upload them to the Media Library when building.

---

## 2. Setup

### MCP connection (per site)
The site runs the **CSMCP** plugin (`pro-extended`). Connect Claude Code to it:

```bash
claude mcp add --transport http --scope user cs-mcp \
  https://<site>/wp-json/cs-mcp/v1/mcp \
  --header "Authorization: Basic <base64 of email:application-password>"
```

- Create a **WordPress Application Password** (Users › Profile) just for this, and **revoke it when
  the build is done**. Never paste it into a repo, a commit, or a shared doc.
- WP Engine blocks unknown user agents: send a normal one (e.g. `curl/8.5.0`) if you call the
  endpoint from a script.

### First calls on a new site (read-only)
| Call | Why |
|---|---|
| `cs_environment` | WP / Pro / Cornerstone versions, active plugins |
| `cs_list_pages` | Pages and which are built with Cornerstone |
| `cs_element_catalog` | Every element type in use + real examples — **copy these key shapes, never invent keys** |
| `cs_list_options` → `cs_get_option x_custom_styles / x_custom_scripts` | Existing global CSS/JS (back it up locally) |
| `cs_get_option cs_assignment_cache_layout_header` | Which header goes where |
| `gf_list_forms`, `cs_list_menus` | Forms and menus available |
| `cs_dev_source` (grep) | Read Pro/Cornerstone/plugin source when a key or feature is unclear |

---

## 3. Phase 1 — The HTML mockup

Build the design as static HTML first; it's fast to iterate and easy to share.

**Structure**
- One `.html` per page + one shared `styles.css`. Home first, inner pages after approval.
- Every section wrapped in a comment: `<!-- ===== 2. WELCOME ===== -->` with the same numbering
  you'll use for Cornerstone labels.
- Design tokens in `:root` (colours, fonts, spacing) — these become Global Colors/Fonts.
- Comment each block with the Cornerstone element it maps to.

**Sharing**
- Push to the repo branch and share the browser link:
  `https://raw.githack.com/<owner>/<repo>/<branch>/<folder>/index.html`
- Zip download: `https://github.com/<owner>/<repo>/archive/refs/heads/<branch>.zip`

**QA before handing over a mockup** (Playwright, Chromium is preinstalled):
- Desktop 1440px and phone 390px screenshots of every page.
- No horizontal scroll (`scrollWidth` = viewport width).
- Every section's content starts at the same left edge (measure it — catches narrow/centred
  wrappers like the Lewis "Mission" bug).
- Section after a dark hero is light (avoid dark-on-dark).
- Hover/interaction states actually tested (move the mouse in steps; the first move is sometimes
  missed by headless Chromium).

---

## 4. Phase 2 — Global layer (do this before building pages)

### Global Colors & Fonts
Create them from the mockup tokens (Lewis: Ivory, Sand, Ink, Lewis Red `#A51C30`, Red Dark
`#7F1424`, Red on Dark `#E85D6C`; Fraunces + Inter). Elements reference them as
`global-color:<id>` / font ids.

### Global CSS (`x_custom_styles`)
- Wrap everything you add between markers so it can be found and replaced safely:
  `/* ===== <PROJECT> REDESIGN START ===== */ … /* ===== <PROJECT> REDESIGN END ===== */`
- Only put here what Cornerstone has no control for: heading accent colour, plugin output
  (Gravity Forms, Sermon Manager, MEC), sticky header states, small fixes.
- `cs_update_option` returns the previous value — **save it locally before every write**.
- After any global change: `cs_purge_cache {"all": true}`.

### Global JS (`x_custom_scripts`)
Reusable copy lives in `cornerstone/global.js`. It does two things automatically:

**Heading accent (H1/H2)** — editors type plain text, the script colours it:
| Heading length | Coloured |
|---|---|
| 1 word | nothing |
| 2–5 words | last word |
| 6+ words | last two words |

- Bright red on dark backgrounds, decided from the heading's own text colour (no class needed).
- Skips: top bar, menu bar, off-canvas menu, forms, tooltips, search/blog result titles, plugin
  listing titles (sermons, event lists). Add `data-lc-no-accent` to opt any element out.
- A heading that already contains `<em>` is left as typed (manual override).

**Form context** — marks every Gravity Form `lc-gf-dark` or `lc-gf-light` from the background it
sits on, so the global form CSS picks the right variant. Re-runs on AJAX content (calendar month
change, form confirmation) via a MutationObserver.

### Gravity Forms (global)
- Style **all** `.gform_wrapper.gform-theme--orbital` forms in global CSS, light + dark variants.
  Use `!important` on the `--gf-*` variables so they beat the per-form defaults GF prints.
- **Set Forms › Settings › Default Form Theme = Orbital** (the MCP can't change it). Otherwise forms
  added with the native element render in the old "Gravity Forms 2.5" theme.
- Never pass `styles='{…}'` in shortcodes; insert forms with the **Form Integration** element
  (`form_integration_type: "gravity-forms"`, `form_integration_gravityforms_id`).

---

## 5. Phase 3 — Build the pages

### Workflow
1. Upload images: `cs_upload_media` (from Unsplash URL).
2. Build each page as native elements modelled on `cs_element_catalog` examples.
3. Save with `cs_save_element_tree` (whole tree) or `cs_update_element` (one element by path).
4. `cs_purge_cache {"id": <page>}` → check in the browser **and** in the Cornerstone editor.
5. For risky experiments: `cs_create_page {"clone_from": <id>, "status": "draft"}` +
   `cs_preview_link`. Delete the test page afterwards.

### HTML → Cornerstone element map
| Mockup | Cornerstone element | Notes |
|---|---|---|
| `<section>` band | **Section** | Background colour/image/video + overlay on the section |
| 2-col split | **Row** + 2 **Columns** | Image column / Text column |
| Eyebrow (line + small caps) | **Div** (flex row) › **Line** + **Headline** (`span`) | |
| H1 / H2 | **Headline** (`text_tag` h1/h2) | Plain text only — accent is automatic |
| Paragraph | **Text** | `<p>` written by the editor is fine |
| Button / ghost button | **Button** | |
| Card grid | **Row** + N **Columns** | Each column = one card |
| FAQ | **Accordion** + **Accordion Item** | |
| Scripture | **Quote** | |
| Video hero | Section background › Video | Image as fallback |
| Welcome video | **Video** element | |
| Map | **Map** (embed) | |
| Form | **Form Integration** (Gravity Forms) | Not Raw Content |
| Plugin list (sermons, calendar) | **Raw Content** with the shortcode only | Style in global CSS |

### Useful element keys
- Element label shown in Layers: **`title`** (not `_label` on page elements; bars in headers use `_label`).
- Headline: `text_content`, `text_tag`, `text_href` + `text_link: true`.
- Div flex: `layout_div_flexbox`, `layout_div_flex_direction`, `_wrap`, `_justify`, `_align`, `_gap`.
- Custom class: `class` (only for global-CSS hooks, never something editors must type).
- Component placement: `{"_type": "global-block", "global_block_id": "<id>"}`.
- Dynamic content with fallback: `{{dc:post:title fallback="Page not found"}}`,
  `{{dc:post:featured_image fallback="https://…/photo.jpg"}}`,
  `{{dc:archive:title fallback="dc:query:search_query"}}` (a nested second fallback does **not** work).

### Labels (do this on every page)
Editors navigate by the Layers panel, so name everything (`title` key):
- **Sections:** numbered in page order — `1. Hero (video)`, `2. Welcome`, `3. FAQ`, `4. Plan Your Visit (form)`.
- **Rows:** `Content`, `Cards`, `Tiles`, `Service Times`, `Contact Details`.
- **Columns:** `Text`, `Image`, `Video`, `Map`, `Form`, `Accordion`; grid columns `Card – <title>`.
- **Divs:** `Eyebrow`, `Heading Group`, `Buttons`, `Image Frame`, `Frame Outline`, `Form Box`,
  `Calendar (MEC shortcode)`, `Sermon List (shortcode)`.
- Before saving a relabelled tree, diff it against the original with `title` keys stripped —
  nothing else may change.

---

## 6. Phase 4 — Headers, footer, components

### Header set (keep it minimal)
| Header | Assign to | Shape |
|---|---|---|
| **Transparent (hero pages)** | Pages that build their own hero section | Top bar + nav floating over the page |
| **Default (title hero)** | Entire site (fallback, priority 10) | + banner: `{{dc:post:title fallback="Page not found"}}` on `{{dc:post:featured_image fallback=…}}` |
| **Archives** | All archive + search conditions | + banner: `{{dc:archive:title fallback="dc:query:search_query"}}` |
| **Single (menu only)** | Single sermon / event post types | Top bar + nav, no banner |

One archive header covers series, speakers, topics, books, post-type archives, blog, categories,
authors and search. Two global-CSS rules fill the gaps WordPress leaves:
`.search .lc-archive-title …::before { content: "Results for “" }` and
`.lc-archive-title …:empty::before { content: "Messages" }`.

### Components (edit once, every header updates)
- `Top Bar – Announcement` (label, text, link)
- `Header – Logo`
- `Header – Plan Your Visit Button` — keep its `lc-nav-cta` class (sticky CSS targets it)
- **Not the mobile menu**: `nav-layered` / off-canvas elements don't render inside a component.
  Its links already come from the WordPress menu, so it doesn't need one.

Roll a component out to the least-visited header first, compare positions/sizes against an
untouched header (top + sticky, desktop + phone), then do the rest.

### Sticky header
Nav bar: Sticky on, trigger offset ~160, shrink + slide. Red sticky state via header custom CSS on
`.lc-nav.x-bar-fixed` (background red, CTA white with red text, menu text white).

---

## 7. Plugins

| Plugin | How we handle it |
|---|---|
| **Gravity Forms** | Orbital theme, global CSS, Form Integration element (see §4) |
| **Sermon Manager Pro** | `[smpro_archive]` in Raw Content; style `.smpro-*` in global CSS, scoped to the page wrapper class *and* the archive templates |
| **Modern Events Calendar** | `[MEC id="…"]` in Raw Content; restyle monthly view + minimal list in global CSS. Navigator arrows: the link also holds a hidden month name — absolutely centre the icon |

---

## 8. QA checklist (run after every round)

- [ ] `cs_purge_cache {"all": true}`
- [ ] Every page, desktop 1440 + phone 390: no horizontal scroll, nothing overlapping
- [ ] Section left edges all equal (measure; centred bands are the only exception)
- [ ] Every H1/H2 accent correct (script check: word count vs coloured words, colour per background)
- [ ] Code scan of all page trees: no HTML in headings, no `styles=` in form shortcodes, no
      editor-typed helper classes; `<p>` in Text elements is fine
- [ ] Forms: correct light/dark variant, submit + confirmation styled
- [ ] Header on each type of page (hero page, archive, search, single, 404); sticky state; phone
      menu opens with all links
- [ ] Hero video plays (note: headless Chromium has no H.264 — ship a WebM too, test with it)
- [ ] Layers panel readable in the Cornerstone editor

---

## 9. Backups & rollback

- Page writes → automatic backups: `cs_list_backups` / `cs_restore_backup`.
- Headers/components → backed up by `cs_save_layout` / `cs_save_component`; also save the JSON
  locally before editing.
- Global CSS/JS → `cs_update_option` returns the previous value; keep it in a local file.
- Retired headers/components → `cs_save_post {"status": "trash"}` (restorable), after clearing
  their assignments.
- Commit the final `global.css` / `global.js` to the repo (`cornerstone/`) — never the credentials.

---

## 10. Lessons from Lewis (avoid repeating)

- Centred, narrower wrappers (`max-width` on the wrap) break left alignment — constrain the
  children instead.
- Don't put a dark photo band right after a dark hero.
- `.lc-on-dark` / `.lc-form` style classes that editors must add by hand are a trap — detect
  context in JS instead.
- Per-form `styles='{…}'` in GF shortcodes overrides global CSS (id-specific) — remove it.
- Seven near-identical headers = seven places to edit the announcement. Merge headers, share
  pieces through Components.
- `{{dc:archive:name}}` is empty on post-type archives and search; use `dc:archive:title` + fallbacks.
- When a plugin re-renders content (calendar months, AJAX forms), global JS must re-run
  (MutationObserver).
- When the client says a heading rule, codify it in the global JS — never hand-edit headings.

---

## 11. Handover

- Share the live URL and a `cs_preview_link` for any drafts.
- List the Components and what each controls.
- Remind the client: revoke the application password used for the build.
- Delete test/draft pages (e.g. "TEST – … (delete me)").
