# Template redesign prompt

## Quick version (chat style)

Copy all six paragraphs, change the bits in [brackets], and paste them into a new session. Each paragraph is one step, so you can update one step without touching the rest.

> **The job.** Hey! I run ReachRight, we build church websites, and I want to give one of our least-popular templates a fresh, premium look. It's [TEMPLATE NAME] at [TEMPLATE URL], for [CHURCH NAME]. Our live sites run on WordPress with Themeco Pro/X and the Cornerstone builder, so design it in a way that's easy to rebuild there.
>
> **Step 1: Study the template.** Go through every page of the template and note each section and its content: headings, copy, buttons, forms, images and embeds. The rule is same sections, same content, word for word. You can change the layout and make it way more creative, just don't add or drop sections, and tell me if you add any copy.
>
> **Step 2: Design the home page first, in HTML.** I want it premium and bold but elegant through restraint, warm and welcoming, clearly modern and never churchy: big confident headlines, a full-screen worship video in the hero with a scrolling ticker for service times and announcements, real photos of people in modern churches, lots of whitespace, a clean 12-column grid, thin divider lines, light cream sections alternating with dark photo sections, no circles anywhere, and a simple text-only logo. Use the template's brand colour as the one accent, with cream, sand and near-black around it, Bricolage Grotesque for headings and DM Sans for body text. For inspiration, look at elevationchurch.org, churchome.org, hillsong.com, vous.church and mosaic.org, plus apple.com and kinfolk.com for that premium restraint.
>
> **Step 3: Show me and wait.** Send me desktop and phone screenshots of the home page and wait for my OK before going further. I'll probably ask for changes, so keep it easy to adjust.
>
> **Step 4: Build the other pages.** Once I approve the home page, build Plan Your Visit, About, Connect, Watch Live, Messages (with a single-message page), Events and Give in the same style. Same rule: same sections, same content. Mix up the layouts so pages don't feel repetitive.
>
> **Step 5: Connect everything.** Make sure every button, card and link goes to a real page or to the right section (for example the home ministry cards go to the matching part of the Connect page). No dead links. The address opens Google Maps, the phone number calls and the email opens an email. Tell me about any links the church needs to give us, like the online giving page.
>
> **Step 6: Check and deliver.** Check every page on desktop and phone, make sure text is readable over photos and nothing scrolls sideways, then send me everything in one zip with screenshots.

---

## Detailed version (structured)

Same instructions as a checklist: fill in the PROJECT block and copy everything inside the box.

```text
PROJECT
- Template: [TEMPLATE NAME]  —  [TEMPLATE URL]
- Church name: [NAME]  ·  Brand accent colour: [HEX, from the template]
- Pages: Home, Plan Your Visit, About, Connect, Watch Live, Messages (+ single message), Events, Give
- Hero video / photos: [optional: a Pexels or Unsplash link, or "find one"]

YOU ARE
A senior web designer at ReachRight, a studio that builds church websites. We redesign our least-popular
templates to give them a fresh, premium look. Live sites run on WordPress + Themeco Pro/X with the
Cornerstone builder.

PROCESS
1. Fetch every page of the template and list each page's sections, headings, copy, buttons, forms and media.
2. Build the HOME PAGE FIRST, in HTML. Show it to me (desktop + phone screenshots) and wait for my approval.
3. Only after I approve the home page, build the other pages using the same design system.
4. Then connect every link and button, check everything, and send me one zip.

CONTENT RULES
- Same sections, same content: keep every section and keep the copy word for word, placeholders included.
- You may re-lay out a section and split long paragraphs into a lead sentence + body. Tell me any copy you add.
- Don't repeat the same layout back to back. Mix: text | photo splits, 3 columns, statement + wide photo,
  photo cards, accordions. Alternate light and dark sections.

FEEL
- Premium and bold, made elegant through restraint. Warm and welcoming, clearly modern, never churchy-clip-art.
- Bold: oversized headlines, a full-screen video hero, full-bleed dark photo bands. One bold moment per page.
- Elegant: whitespace, strict grid, aligned edges, thin hairlines, one corner radius, calm motion. No gold, script
  fonts or decoration for its own sake.
- Feel check before you send anything: Does it look premium? One clear bold moment? Clean and aligned?
  Warm, with real people on the first screen? Would it hold up next to the references?

REFERENCES (study the feel, don't copy)
- Churches: elevationchurch.org · churchome.org · hillsong.com · vous.church · mosaic.org · c3church.com ·
  transformchurch.us · passioncitychurch.com · life.church · gatewaypeople.com · northpoint.org · redrocks.church
- Premium brands: apple.com · aesop.com · kinfolk.com
- Galleries: godly.website · onepagelove.com · awwwards.com

DESIGN SYSTEM
- Colours: cream #F6F2EA (page) · sand #ECE6DA (alt band) · ink #16181B (text, dark bands) · soft ink #5E6166 ·
  accent = brand colour (darker shade of it for small text on cream).
- Fonts: Bricolage Grotesque 600 for headings (tight, -0.03em) · DM Sans 17px / 1.7 for body.
- Sizes: hero clamp(56px, 9.2vw, 148px) · H2 clamp(40px, 5.2vw, 76px) · lead clamp(28px, 3.1vw, 44px) ·
  H3 ~24px · labels 12px caps, +0.16em.
- Layout: 12-column grid, 1240px max, 32px gutter (20px on phones), section padding clamp(88px, 11vw, 168px),
  8px spacing steps, 1px hairlines. Each section opens with a label row like "01 / Welcome Home".
- Shapes: images 14px radius, buttons 8px radius and 52px tall. No circles anywhere.
- Logo: text only. Church name in Bricolage 700, "CHURCH" small and widely spaced underneath.

KEY COMPONENTS
- Header: fixed, transparent over the hero, turns cream on scroll. Text logo, nav, accent "Plan Your Visit" button.
- Home hero: full-screen modern worship video (compress to about 1–2 MB), dark overlay, centred two-line
  headline (second line in the accent), 2 buttons, and a scrolling ticker of service times and announcements.
- Inner pages: photo hero with breadcrumb and big title.
- Dark sections: photo behind an ink overlay (85–95%).
- Get in Touch: text + button | simple details list, then a full-width greyscale map.
- Footer: dark photo band, links, socials, credit "church web design by REACHRIGHT", giant accent wordmark.
- Photos: modern churches and real people (Unsplash / Pexels). Look at every photo before using it.

BUILD FOR CORNERSTONE
- Sections › Rows/Columns or Grid for layout; Headline, Text, Button, Image, Accordion, Video, Map elements.
- Section background layers for the video/photo + overlay. Pro Header & Footer Builders. Global Colors/Fonts.
- Get in Touch as a Global Block. Sermons and events through the Looper. Fade-ins via Effects › Scroll.
- Note in each page's HTML which Cornerstone element each part becomes.

LINKS & DELIVERY
- Every button, card and link goes to a real page or section (e.g. ministry cards → connect.html#kids).
  No href="#". Address → Google Maps, phone → tel:, email → mailto:. List any URLs the church must supply.
- Files: one HTML per page + shared styles.css + site.js, in [template]-redesign/. Check desktop (1440px)
  and phone (390px), no sideways scrolling. Commit, then send me the zip and screenshots.
```
