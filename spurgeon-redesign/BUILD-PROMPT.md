# Build prompt: church template redesign (Spurgeon method)

Copy everything below the line into a new session. Replace the items in [brackets].

---

You are redesigning one of our church website templates. We are ReachRight, a studio that builds church websites, and the site will be rebuilt in WordPress + Elementor, so design it in a way that maps cleanly to stock Elementor widgets.

## The job

- Source template: [TEMPLATE URL, e.g. https://spurgeon.wpengine.com/]
- Pages: Home, Plan Your Visit, About Us, Get Connected, Watch Live, Messages, Events, Give, plus a single-message (sermon) page.
- Deliver static HTML/CSS/JS: one HTML file per page, one shared `styles.css`, one shared `site.js`. No frameworks or build tools.
- Put everything in a folder named `[template]-redesign/` and also give me the whole site as one zip.

## The rule: same sections, same content, new design

1. First fetch every page of the source template and list each page's sections in order, with their headings, body copy, buttons, forms, images and embeds (maps, YouTube).
2. Keep every section and keep the copy word for word, including placeholder text (accordion bodies, "First & Last Name", the sample sermon, the map location). Don't invent new sections.
3. You may re-lay out a section (for example turning the "single or married, with children or without…" sentence into captions on four photo cards), split a paragraph into a large lead sentence plus body text, and add small section labels like "01 / Welcome Home". Tell me each piece of copy you add.
4. Don't repeat the same layout section after section. Vary between split (text | photo), three columns, statement plus wide photo, centred heading plus accordion, and photo cards.

## Design direction: "sunlit editorial"

Warm, modern and calm, not churchy-clip-art. Big confident type, generous whitespace, real photography, and one bright accent colour.

### Colour (set once as Elementor Global Colors)
| Token | Hex | Use |
|---|---|---|
| Cream | `#F6F2EA` | page background, light sections |
| Sand | `#ECE6DA` | alternate light band, image placeholders |
| Ink | `#16181B` | text, dark sections, footer |
| Ink soft | `#5E6166` | secondary text |
| Accent (brand) | `#3DB6DB` | buttons and highlights on dark, the second line of the hero headline |
| Accent ink | `#1B7FA0` | small accent text on cream (readable) |
| Hairline | Ink at 12% | dividers |

Use the template's own brand colour as the accent. Light and dark sections alternate; dark sections are Ink with a photo behind an Ink overlay at 85–95%, so text stays readable.

### Type (set as Elementor Global Fonts)
- Headings: **Bricolage Grotesque**, weight 600, letter-spacing −0.03em, line-height 1.
- Body: **DM Sans** 17px, line-height 1.7.
- Scale: hero display `clamp(56px, 9.2vw, 148px)` · H2 `clamp(40px, 5.2vw, 76px)` · statement/lead `clamp(28px, 3.1vw, 44px)` · H3 `clamp(20px, 1.7vw, 24px)` · labels 12px uppercase, letter-spacing 0.16em.

### Layout system
- 12-column grid, max width 1240px, 32px gutter (20px under 600px).
- Section padding `clamp(88px, 11vw, 168px)` top and bottom; spacing in 8px steps.
- Every section opens with a label row: number in accent ink, a "/", the section name, then a 1px hairline underneath.
- 1px hairlines for all dividers and list rows.
- Images: 14px corner radius. Buttons: 8px radius, 52px tall, 15px semibold, with a small arrow that nudges right on hover.
- **No circles** anywhere: no round photos, no round icons or buttons. Rectangles and rounded rectangles only.

### Components
- **Header:** fixed, transparent over the hero with white text; turns cream with a hairline once you scroll 40px. Nav links get a thin underline on hover and for the current page. "Plan Your Visit" is an accent button. On mobile it becomes a full-width dropdown menu.
- **Logo:** text only. "[Church name]" in Bricolage 700 at 27px, letter-spacing −0.04em, with "CHURCH" underneath in 10.5px caps, letter-spacing 0.42em. White over the hero, ink on cream. Export `logo.svg` and `logo-white.svg` with the text outlined, plus a favicon (a letter on an accent square).
- **Home hero:** full-screen background video of a modern worship service (free stock, e.g. Pexels; compress to about 1–2 MB as MP4 + WebM with a poster image). Dark overlay plus a soft centre vignette. Centred: small label, two-line headline (second line in the accent colour), two buttons (Plan Your Visit, Watch Live).
- **Ticker:** a slim scrolling strip along the bottom of the hero with service times and announcements, each item linked; pauses on hover; still for reduced-motion users.
- **Inner page hero:** about 62% of the screen tall, photo behind a dark overlay, centred breadcrumb ("Home / Page") and a big title.
- **Split section:** heading, a large lead sentence, body text in soft ink, button | photo. Flip sides from one section to the next.
- **Photo cards:** four staggered portrait cards (alternate cards sit lower), caption row with hairline and number.
- **Accordion** (FAQs, beliefs): heading rows with a small square +/− icon.
- **Get in Touch** (home and About): heading, text and button | a simple label/value list (Sundays, Wednesdays, Address, Phone, Email). Below it a full-width greyscale Google Map.
- **Forms:** labels in small caps above white 52px fields, two columns on desktop, validation, then a thank-you message.
- **Footer:** Ink with a photo behind it; logo + tagline, Explore links, social icons in squares, address and "church web design by REACHRIGHT" credit, and a huge accent-coloured wordmark across the bottom.
- **Motion:** sections fade up as they scroll into view; nothing else animates.

### Photography
- Modern churches and real people: worship with stage lighting, people greeting, small groups, families in pews. Avoid old cathedrals, stained glass and candles.
- Use free stock (Unsplash, Pexels). Look at every photo before using it and give it real alt text.

## Linking
- Every button, card and link must go somewhere real: a page, or a specific section on a page (for example the home ministry cards go to `connect.html#kids`, `#students`, `#women` and `#men`).
- Get Connected buttons jump to a sign-up form with that ministry pre-selected. Sermon cards open the sermon page; series and speaker links filter the Messages page.
- Address opens Google Maps; phone and email use `tel:` and `mailto:`.
- Anchor jumps must clear the fixed header.
- Run a check that every internal link and `#section` target exists, with zero `href="#"` left. List anything that needs a real URL from the church (giving platform, social profiles).

## Quality bar
- Check every page at desktop (1440px) and phone (390px) widths, with full-page screenshots.
- No horizontal scrolling on phones.
- Text on photos must be readable.
- Keyboard focus is visible, and the mobile menu works.
- Comment each page's HTML with its sections and the Elementor widget each part maps to.
- Commit with clear messages, and send me the zip plus screenshots.
