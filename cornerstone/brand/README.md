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
| Slate Blue (Brand) | `#32485B` | Buttons, sticky header, accent words on light |
| Slate Dark (Hover) | `#243645` | Button hover |
| Gold (Accent on dark) | `#ECCF8C` | Accent words, buttons and header CTA on dark/photo |
| Navy Ink | `#1B2733` | Headings, dark sections, footer |
| Navy Ink 2 | `#233240` | Secondary dark |
| Ink Soft | `#4F5B66` | Body text |
| Cream (Page) | `#FBF9F4` | Page background |
| Sand | `#F3EEE2` | Alternate sections |
| White | `#FFFFFF` | |
| Line Light / Line Dark | `rgba(27,39,51,.12)` / `rgba(255,255,255,.14)` | Dividers |
| Photo Overlay | `rgba(20,30,40,.62)` | Over hero photos |

## Font
**Plus Jakarta Sans** (Google) for headings and body — closest Google match to the logo wordmark.
Heading accent words are italic: Slate on light, Gold on dark (automatic, global JS).

## Buttons on dark
Solid Slate buttons on a dark section/photo turn Gold with navy text automatically
(`lc-btn-invert`, global JS + CSS). The header "Plan Your Visit" button is always Gold.

## Logo files (transparent PNG, Media Library ids)
- `pcc-mark-white.png` (313) — header/footer logo (headline graphic)
- `pcc-mark-black.png` (314)
- `pcc-logo-white.png` (315), `pcc-logo-black.png` (316) — full stacked logo
- `pcc-favicon-512.png` (324) — favicon: white P mark on Slate. Sizes 32/180/192/270 uploaded as
  ids 325–328; the WordPress Site Icon attachment (295) points at them.

## Contact links
Addresses link to the Google Maps place (new tab), phone numbers to `tel:8048814673`, email to
`mailto:`. Links inherit the text colour; hover is Gold on dark sections, Slate on light.
