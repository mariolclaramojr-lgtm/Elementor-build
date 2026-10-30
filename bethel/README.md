# Bethel Church rebrand (rrbethelchurch.wpenginepowered.com)

Rebrand to the Bethel Church brand guidelines (Olive Grove palette, Lora + Raleway), rebuilt
in native Cornerstone elements. Same section count per page as before.

| File | What it is | Where it lives on the site |
|---|---|---|
| `global.css` | Heading accent, Gravity Forms (Lewis rules), Sermon Manager Pro + MEC shortcode output | Theme Options › CSS (`x_custom_styles`) |
| `global.js` | Heading accent (last word / last two words), form light/dark | Theme Options › JS (`x_custom_scripts`) |
| `build/kit.py` | Element kit: every colour is a Global Color, every font a Global Font | — |
| `build/pages.py` | Page trees (Home, About, New Here, Ministries, Connect, Give, Events, Watch) + components | Pages 15, 463, 468, 467, 462, 466, 441, 333; components 508, 509 |
| `build/layout.py` | Header (13) and footer (458) | Pro › Headers / Footers |

## Global settings
- **Global Colors:** Forest `#344027`, Forest Deep `#283220`, Moss `#6B8452`, Sage `#B5C99A`,
  Sage Mist `#E6ECDB`, Fieldstone `#5E6652`, Cream `#F5F2E9`, White, Cream Soft (text on Forest),
  Forest Line (borders). The old Navy/Gold ids were repurposed, so anything still pointing at them
  picks up the new palette.
- **Global Fonts:** Headings → Lora, Body Copy → Raleway (same ids as before).
  Stored as slashed JSON strings, the format Cornerstone expects. An array breaks `GlobalFonts.php`.
- **Components:** `Find Us (map + contact)` (Home, New Here, Connect) and `Plan Your Visit CTA`
  (About, Ministries). Edit once, every page updates.
- **Logos** (Media Library): 502 horizontal Forest + Sage (header), 503 horizontal Cream + Sage
  (footer, menu), 504 white, 505 vertical Cream, 506 mark 02 (favicon), 507 mark 01 (social avatar).

## Rules
- Cornerstone elements and settings first: no custom classes or element CSS in any page, header
  or footer tree. Hovers, blur, icons and overlays use the elements' own settings.
- Global CSS only for what Cornerstone can't reach: the heading accent and plugin output.
- Gravity Forms: same rules as the Lewis site. Orbital theme, styled globally in `global.css`
  (light/dark from the global JS), inserted with the Form Integration element, no `styles=` in
  shortcodes. Forms › Settings › Default Form Theme must be Orbital.
- Plugins use their own shortcodes in Raw Content: `[MEC id="446"]` (Grid skin, Classic) and
  `[smpro_archive per_page="15"]`.
