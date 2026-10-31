# Proclaim Christ Church — brand

Applied to rrproclaimcc.wpenginepowered.com through Global Colors / Global Fonts (same ids as the
Lewis build, so every element picked up the change), global CSS/JS, headers and footer.

## Church details
- 4036 Cox Rd, Glen Allen, VA 23060 · 804-881-4673 · office@proclaimchristchurch.com
- Website: https://www.proclaimchristchurch.com/
- Map: https://maps.app.goo.gl/A9XunQwKf1pGyntt9
- Facebook: https://www.facebook.com/proclaimchristchurch/
- Instagram: https://www.instagram.com/proclaimchrist_church
- YouTube: https://www.youtube.com/@ProclaimChristChurch

## Global Colors
| Name | Value | Use |
|---|---|---|
| Navy (Brand) | `#162144` | Buttons, sticky header, accent words on light |
| Navy Light (Hover) | `#2A3A72` | Button hover |
| Gold (Accent on dark) | `#ECCF8C` | Accent words, buttons and header CTA on dark/photo |
| Deep Navy (Ink) | `#0F1730` | Headings, dark sections, footer |
| Deep Navy 2 | `#1A2650` | Secondary dark |
| Ink Soft | `#4A5470` | Body text |
| Cream (Page) | `#FBF9F4` | Page background |
| Sand | `#F3EEE2` | Alternate sections |
| White | `#FFFFFF` | |
| Line Light / Line Dark | `rgba(15,23,48,.12)` / `rgba(255,255,255,.14)` | Dividers |
| Photo Overlay | `rgba(12,18,40,.62)` | Over hero photos |

**Linked to Global Colors:** the global CSS, header CSS and element CSS write brand colours as
`%%post color%%global-color:<id>%%/post%%` (optionally `global-color:<id>:0.35` for alpha). Cornerstone
resolves these to the current Global Color, so changing a colour in Cornerstone › Global Colors
updates the heading accents, buttons on dark, sticky header and forms too.

## Font
**Plus Jakarta Sans** (Google) for headings and body — closest Google match to the logo wordmark.
Heading accent words are italic: Navy on light, Gold on dark (automatic, global JS).

## Buttons on dark
Solid Navy buttons on a dark section/photo turn Gold with navy text automatically
(`lc-btn-invert`, global JS + CSS). The header "Plan Your Visit" button is always Gold.

## Logo files (transparent PNG, Media Library ids)
- `pcc-mark-white.png` (313) — header/footer logo (headline graphic)
- `pcc-mark-black.png` (314)
- `pcc-logo-white.png` (315), `pcc-logo-black.png` (316) — full stacked logo
- `pcc-favicon-navy-512.png` (331) — favicon: white P mark on Navy. Sizes 32/180/192/270 uploaded as
  ids 332–335; the WordPress Site Icon attachment (295) points at them.

## Contact links
Addresses link to the Google Maps place (new tab), phone numbers to `tel:8048814673`, email to
`mailto:`. Links inherit the text colour; hover is Gold on dark sections, Navy on light.

## Photos
Stock photos from Pexels (free for commercial use, no attribution required — Pexels License).
Uploaded at 2000px wide to the Media Library and swapped in on every page and header.

| File (Media id) | Subject | Source |
|---|---|---|
| `pcc-worship-pews.jpg` (336) | People reading the Bible in church pews | https://www.pexels.com/photo/5874952/ |
| `pcc-open-bible.jpg` (337) | Open Bible | https://www.pexels.com/photo/2294878/ |
| `pcc-community-sunset.jpg` (338) | Friends enjoying time together outdoors | https://www.pexels.com/photo/708392/ |
| `pcc-worship-lights.jpg` (339) | Raised hand during worship | https://www.pexels.com/photo/2774551/ |
| `pcc-friends-group.jpg` (340) | Group of friends laughing together | https://www.pexels.com/photo/9287491/ |
| `pcc-bible-coffee.jpg` (341) | Open Bible with coffee | https://www.pexels.com/photo/22711047/ |
| `pcc-give-phone.jpg` (342) | Giving online on a phone | https://www.pexels.com/photo/892757/ |
| `pcc-praying-together.jpg` (343) | People praying together | https://www.pexels.com/photo/8674871/ |
| `pcc-sanctuary-scaled.jpg` (344) | Church sanctuary with cross | https://www.pexels.com/photo/34553833/ |
| `pcc-reading-in-church-scaled.jpg` (345) | People reading the Bible in church | https://www.pexels.com/photo/8675096/ |
| `pcc-worship-hands.jpg` (346) | Congregation worshipping | https://www.pexels.com/photo/21782633/ |
| `pcc-small-group.jpg` (347) | Small group praying in a living room | https://www.pexels.com/photo/6860385/ |
| `pcc-kids.jpg` (348) | Kids smiling together | https://www.pexels.com/photo/8087930/ |
| `pcc-women.jpg` (349) | Women talking over coffee | https://www.pexels.com/photo/6457519/ |
| `pcc-men.jpg` (350) | Men talking over coffee | https://www.pexels.com/photo/8344906/ |
| `pcc-serving.jpg` (351) | Volunteers serving food | https://www.pexels.com/photo/6995244/ |
| `pcc-serving-meals.jpg` (352) | Preparing meals to serve | https://www.pexels.com/photo/6995247/ |
| `pcc-friends-smiling.jpg` (353) | Friends smiling together | https://www.pexels.com/photo/3756513/ |
| `pcc-bible-morning-scaled.jpg` (354) | Bible and coffee | https://www.pexels.com/photo/7987075/ |
| `pcc-family-walk.jpg` (355) | Family walking together | https://www.pexels.com/photo/5290403/ |

Kept from the previous build: Give › "Why we give" mountains background, Plan Your Visit › coffee
photo, the hidden Ways-to-Give card images, the home hero video and the staff headshot placeholders.
