# Spurgeon Church: redesign handoff

Source template: https://spurgeon.wpengine.com/ · Direction: "sunlit editorial", with multi-ethnic photography throughout.
Static mockup: one HTML file per page, shared `styles.css` and `site.js`, and `assets/` for the video, logo and favicon.
Each page's `<head>` comment lists its sections and the Cornerstone element each part maps to.

| Page | File |
|---|---|
| Home | `index.html` |
| Plan Your Visit | `plan-your-visit.html` |
| About Us | `about.html` |
| Get Connected | `connect.html` |
| Watch Live | `watch-live.html` |
| Messages | `messages.html` |
| Single message (Sample Sermon) | `sermon.html` |
| Events | `events.html` |
| Give | `give.html` |

## Copy added or changed (everything else is word for word from the template)
- **Section labels** on every page ("01 / Welcome Home" and so on), plus the breadcrumbs.
- **Home hero:** the original H1 "Spurgeon Church" became the small label. The tagline "Loving God. Loving People." is now the two-line headline. Added two buttons: Plan Your Visit and Watch Live.
- **Home ticker:** reuses existing copy (service times, "Join us Sundays at 10am", Sample Sermon, ministry names, the address).
- **Home ministry cards:** titles are the Connect page ministries (Kids, Students, Women, Men). Each caption is one phrase from the Ministries sentence, which also stays in full above the cards.
- **Lead + body splits:** a paragraph's first sentence is set large. The text itself is unchanged.
- **Plan Your Visit:** a "Let us know You're coming" button in the Welcome band, which jumps to the form.
- **Get Connected:** a sign-up section, required by the brief, with heading "Get Connected", one intro line, Name/Email/Phone/Ministry fields and a thank-you message.
- **Watch Live › Give Online:** the template's button reads "Get Connected". It now reads **Give Now** and goes to the Give page.
- **Messages:** "All" filter options, a "Clear" button and an empty-state message. **Single message:** detail labels and an "All Messages" button.
- **Events:** weekday headers, plus year options 2026 and 2027 (the template only offers 2022).
- **Forms:** a thank-you message for each, plus "This field is required." validation text.
- **Footer:** "Visit" column heading and the © line.

## Needs real URLs or content from the church
- **Giving platform:** both "Give Now" buttons on `give.html` (marked `data-needs-url="giving platform"`).
- **Social profiles:** Facebook and X in the footer currently point to the network home pages.
- **Address, phone and email** are the template placeholders. The map embed is still the template's (Lambeau Field).
- **Live stream:** the YouTube embed is the template's video (`dlhA0AmTVf0`).
- Leadership names and photos, the FAQ and belief answers, and the sermon content are template placeholders.
- Form submissions: wire up Gravity Forms or Cornerstone Forms (the mockup only shows the thank-you message).

## Media
- **Photos:** Unsplash, loaded from images.unsplash.com and chosen for real, multi-ethnic church life. Each has alt text in the HTML.
- **Home hero video:** Mixkit #48509 (free licence), worshippers with raised hands under stage lights, compressed to 1.5 MB MP4 and 1.4 MB WebM, with a poster image.
- **Plan Your Visit band video:** the template's own `Film-set.mp4`, compressed to 0.25 MB.
- **Logo:** `assets/logo.svg` and `logo-white.svg` (Bricolage Grotesque 700, text outlined). Favicon: `favicon.svg` and `.png`.
