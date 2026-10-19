# Build prompt: church template redesign (Spurgeon method)

Copy everything below the line into a new session. Replace the items in [brackets].

---

You are redesigning one of our church website templates. We are ReachRight, a studio that builds church websites. The live sites run on WordPress with **Themeco Pro (or X) and the Cornerstone builder**, so design every section so it can be rebuilt with Cornerstone's own layout elements, content elements, Header/Footer Builders and Global Blocks.

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

### How it should feel
In one line: **premium and bold, made elegant through restraint.** It should feel like a well-funded modern church or a design-led brand, not a template.

- **Premium:** lots of whitespace, a strict grid, thin hairlines, high-quality photography and very few colours. Nothing feels crowded or cheap: no drop shadows on everything, no gradients for decoration, no stock icons used as filler.
- **Bold:** oversized, tightly spaced headlines, a full-screen video hero, and full-bleed dark photo sections. One strong accent colour used with confidence.
- **Elegant:** comes from restraint and precision, not from decoration. Consistent spacing, aligned edges, one corner radius, calm motion and short readable line lengths. Avoid the "luxury" clichés: script fonts, gold, thin serif everything.
- **Warm and welcoming:** real people smiling, gathering and worshipping; cream backgrounds instead of stark white; friendly, plain-spoken button labels. A first-time visitor should feel invited, not impressed from a distance.

**Where it sits on each scale:**
| Scale | Target |
|---|---|
| Elegant ←→ Bold | Bold headlines, elegant everything else (about 65% bold) |
| Minimal ←→ Rich | Minimal layout, rich photography |
| Traditional ←→ Modern | Clearly modern; faith shown through people and words, not ornament |
| Quiet ←→ Energetic | Energetic hero, calm sections below |
| Corporate ←→ Personal | Personal and human |

**Feel check before delivering.** Answer these honestly for every page and fix anything that's a "no":
1. Does it look premium, like a design studio built it, at a glance and at phone size?
2. Is there one clear bold moment per page (hero, a statement, a dark photo band), and is everything around it calmer?
3. Is it elegant: are edges aligned, spacing consistent, and nothing crowded or decorated for its own sake?
4. Does it feel warm and welcoming, with real people visible within the first screen or two?
5. Would it hold up next to the reference sites below?

### References
Study these for feel, not to copy. Look at the current versions yourself and note what to borrow (type scale, hero treatment, section rhythm, photo style) before designing.

**Modern church sites:**
- Elevation Church: https://elevationchurch.org
- Churchome: https://churchome.org
- Hillsong: https://hillsong.com
- VOUS Church: https://vous.church
- Mosaic: https://mosaic.org
- C3 Church: https://c3church.com
- Transformation Church: https://www.transformchurch.us
- Passion City Church: https://passioncitychurch.com
- Life.Church: https://www.life.church
- Gateway Church: https://www.gatewaypeople.com
- North Point: https://www.northpoint.org
- Red Rocks Church: https://www.redrocks.church

**Premium brand and editorial sites (for restraint, typography and whitespace):**
- Apple: https://www.apple.com
- Aesop: https://www.aesop.com
- Kinfolk: https://www.kinfolk.com

**Design galleries (for fresh layout ideas):**
- Godly: https://godly.website
- One Page Love: https://onepagelove.com
- Awwwards: https://www.awwwards.com

### Colour (set once as Cornerstone Global Colors)
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

### Type (set as Cornerstone Global Fonts)
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

## Build for Cornerstone (Themeco Pro / X)
Design and code with the way Cornerstone builds pages in mind, so the HTML mockup can be rebuilt element by element.

- **Layout:** each band is a **Section**. Inside it, use **Row › Column** for simple splits, or **Div / Grid / Cell** for the 12-column layouts (split 5 + 7 columns, three columns, four staggered cards). Keep the max width (1240px) and gutter (32px) as the Section/Row settings, not ad-hoc margins.
- **Elements to use:** Headline, Text, Button, Image, Accordion (FAQs and beliefs), Video (YouTube embed), Map (Google Map), Raw Content (only for the scrolling ticker markup). Forms use Cornerstone Forms or a Gravity Forms / WPForms element.
- **Backgrounds:** the hero video and the dark photo sections use the Section's **Background › Lower Layer** (video or image) with an **Upper Layer** ink colour at 85–95% as the overlay.
- **Header and footer:** build them in the **Pro Header Builder** and **Footer Builder**. Header: a transparent Bar over the hero that switches to cream with a hairline once sticky; **Navigation Inline** on desktop, **Navigation Modal** (full-screen menu) on mobile; the text logo is a Text element. Footer: logo + tagline, a Navigation element, social links, the credit line and the big wordmark.
- **Reuse:** the Get in Touch block and the footer wordmark band are **Global Blocks**, so they're edited once and appear on Home and About.
- **Global styles:** colours go into **Global Colors**, fonts into **Global Fonts**, and the few custom rules (hairlines, ticker, label rows) into Theme Options › CSS. Give elements a matching **Class** so the CSS applies.
- **Dynamic content:** the sermon list, single sermon page and events use the **Looper** (Looper Provider on the query, Looper Consumer on the card) and Dynamic Content for the title, date, series and speaker.
- **Motion:** use the element **Effects › Scroll** setting (fade up on enter), not custom scripts.
- In the mockup, keep JavaScript minimal and only for things Cornerstone does natively (sticky header, mobile menu, accordion), plus small helpers (form thank-you, sermon filters, ministry pre-select) that can move into the live site.

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
- Comment each page's HTML with its sections and the Cornerstone element each part maps to.
- Commit with clear messages, and send me the zip plus screenshots.
