# ReachRight church site build rules

How we redesign a church template and build it in WordPress with Themeco Pro and Cornerstone.
These rules come from the Spurgeon rebuild. Use them for every new site.

---

## 1. Process

1. **Audit the template.** List every page and its sections, headings, copy, buttons, forms and media.
2. **Set up globals:** Global Colors, Global Fonts, the header, the footer and the shared Components.
3. **Build the home page in Cornerstone first.** Send desktop and phone screenshots. Wait for approval.
4. **Build the other pages** in the same style once the home page is approved.
5. **Connect every link and button.**
6. **Check responsiveness** at every Cornerstone breakpoint.
7. **Run a full QA pass** (section 12) before calling it done.

Never say something is finished until it has been built and checked on the live site.

---

## 2. Content

- **Keep every section and its copy.** Same sections, same content, new look.
- **Use real copy, not placeholders.** Replace "lorem ipsum" and "This is the accordion body content…" with real, specific text. Flag any copy you write so the client can check it (service lengths, ministry nights and so on).
- **Sample content:** add 6 sermons and 6 events with real titles, descriptions, dates and photos, so archives and calendars never look empty.
- **Photos:**
  - Use real modern church photos: worship, Sunday school, youth, fellowship.
  - No street-kids photos.
  - Look at every photo before you use it.

---

## 3. Design style

- **Feel:** premium, warm and modern. Bold where it counts, elegant through restraint.
- **Colours** (as Global Colors):
  - **Cream** `#F6F2EA` for the page.
  - **Cream Light** `#FBF9F5` for Get in Touch.
  - **Sand** `#ECE6DA` for alternate sections.
  - **Ink** `#16181B` for text and dark sections.
  - **Ink Soft** for body text.
  - **Brand Primary** (the template's accent) and a darker **Cyan Ink** for small text.
- **Fonts** (as Global Fonts): **Headings** use Bricolage Grotesque; **Body Copy** uses DM Sans.
- **Headings:** left-aligned. A short accent line goes under each section heading (native Line element, 48×3px, brand colour).
- **No section labels.** Don't put small-caps label rows with hairlines above sections.
- **Images:** round photos (square source with 50% radius) with a thin ring. On tablets and phones they fill the column.
- **Cards:** white or translucent boxes with a 1px border and 14px radius. Use masonry stacks (Flexbox column with a gap) when the text lengths vary.
- **Buttons:** 52px tall with 8px radius and an arrow. On hover they lift 3px, show a soft shadow and change colour.
- **Logo:** text only. Church name in Bricolage, "CHURCH" small and widely spaced underneath.
- **Header:** solid (not transparent), with the nav and an accent "Plan Your Visit" button.
- **Footer:** four columns (logo and tagline, Explore, Visit, Follow) and a credit bar. No giant wordmark.
- **Home hero:** a centred worship video, a two-line headline and a scrolling ticker of service times and announcements.

---

## 4. Cornerstone: style with widget settings, not CSS

- **Element settings:** style every element in its own settings: Design, Typography, Border, Background, Flexbox, Position, Effects, and per-breakpoint values.
- **No classes or CSS on widgets.** Leave the Class and Element CSS fields empty unless a remaining global CSS rule really needs the class.
- **Global values:** use Global Colors and Global Fonts, never hard-coded values.
- **Native elements:** prefer them over Raw Content or HTML blocks so the client can edit everything in the builder.
  - The ticker is a Slider set to Marquee.
  - Contact rows are Headlines with a Graphic.
  - Service times are Divs.
- **Hover effects:** use Effects › Alt (transform) plus the hover colours on border, background and text.
- **Responsive:** use breakpoint values (Row layout, Column Order, image max-width, margins, text align), not media queries.
- **Clean up before finishing:** check every page, header, footer and component for leftover classes or unused CSS, and remove them.

---

## 5. Global CSS (Theme Options › CSS)

Only for what the builder can't reach:

- **Gravity Forms:** fields, labels, buttons, validation, date icon.
- **Sermon Manager Pro:** archive filters and cards, single sermon.
- **Modern Events Calendar:** toolbar, list, monthly, tile, single event and archive.

Keep it inside the `SPURGEON REDESIGN START/END` markers. Keep it small. Use tokens (`--sp-*`) for colours and spacing.

---

## 6. Reusable pieces (Components)

- **Get in Touch:** one component, placed on Home, About and Connect. Edit it once and every page updates.
- **Logo** and **Plan Your Visit button:** components shared by both headers.
- **Two headers only:**
  - **Header - Main** (priority 10) for regular pages.
  - **Header - Sermons & Events** (priority 1) for every sermon and event archive and single page. Element Show Conditions pick its title:
    - Single pages show the post title.
    - Taxonomy pages show the archive title.
    - Post-type archives fall back to "Messages" or "Events".
- **Priority:** the lowest priority number wins. After any header rebuild, check that each page gets the right header.

---

## 7. Plugins

- **Sermons:** Sermon Manager Pro `[smpro_archive]`. Single URLs are `/messages/<slug>/`.
- **Events:** Modern Events Calendar `[MEC id="…"]`. Single URLs are `/upcoming-events/<slug>/`. Create events through MEC's own save routine so their dates are stored.
- **Forms:** Gravity Forms through the Form Integration element. All forms are styled globally.
- **Placement:** shortcodes go in a Raw Content element. That's the only acceptable Raw Content.
- **Archive and single headers:** sermon and event pages get a photo title band the same height as the page hero.
- **MEC categories:** avoid them unless the MEC category slug is changed. `/category/` clashes with WordPress blog categories and gives 404s.

---

## 8. Theme Options

- **Social links:** footer Follow icons read **Theme Options › Social** (`{{dc:theme:x_social_*}}`). Each icon has a Show Condition that hides it when its field is empty, so adding a URL makes the icon appear.
- **Favicon:** set it in **Settings › General › Site Icon**. Pro's old Theme Options favicon field no longer does anything.

---

## 9. Links

- **No `#` placeholders.** Every button, card and link goes to a real page or section, e.g. ministry cards link to `/connect/#kids`.
- **Special links:** addresses go to Google Maps, phone numbers use `tel:`, emails use `mailto:`.
- **Keep URLs:** don't change existing URL slugs.
- **Protect the site:** never edit plugin core files or overwrite unrelated work.

---

## 10. Responsive (check in Cornerstone's screen preview)

Breakpoints: phone 375, large phone 600, tablet 860, small laptop 1100, desktop 1440.

- **Side margins:** 20px on phones and 32px on tablet and up, for the header, footer, title bars and rows.
- **Stacked text and photo sections:** photo first, then text (Column Order -1). The photo fills the column width.
- **Ministry cards:** centred on phones and tablets.
- **Hero height:** every page hero and title band is the same height.
- **Map height:** the Get in Touch map is as tall as its text column. Set the Map height per breakpoint.
- **No sideways scrolling** at any width.

---

## 11. Safety

- **Credentials:** never commit or expose site credentials. Keep them out of the repo.
- **Backups:** back up options before changing them (global CSS, colours, theme options) and restore anything you only changed to test.
- **Forms:** test them with an empty submit only. Never send real submissions.
- **Deleting:** move old headers or pages to the trash; don't delete them permanently.

---

## 12. QA checklist (run before handover)

- [ ] Every page and sample single, archive and taxonomy page returns 200.
- [ ] No sideways scroll at 375, 600, 860, 1100 or 1440.
- [ ] No broken images. Exactly one H1 per page, with the right title.
- [ ] No raw shortcodes, no lorem ipsum, no placeholder copy.
- [ ] Every internal link and `#anchor` resolves. Phone, email and map links work.
- [ ] Desktop nav and the mobile menu open and link correctly.
- [ ] Each form shows validation on an empty submit.
- [ ] Sermon filters work.
- [ ] MEC list, monthly and tile views work. Search works. The export buttons work.
- [ ] The ticker scrolls and loops. The video, map and live-stream embed load.
- [ ] Footer social icons follow Theme Options. The favicon is set.
- [ ] Each page gets the right header.
- [ ] No leftover classes or custom CSS on pages, headers, footers or components. Global CSS only targets plugin output.
- [ ] Commit and push, then report what was fixed and what is still open.
