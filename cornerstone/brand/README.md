# Proclaim Christ Church — brand (black & white)

Applied to rrproclaimcc.wpenginepowered.com through Global Colors / Global Fonts (same ids as the
Lewis build, so every element picked up the change), global CSS/JS, headers and footer.

## Global Colors
| Name | Value | Use |
|---|---|---|
| Black (Accent) | `#111111` | Buttons, sticky header, accent lines |
| Charcoal (Hover) | `#3A3A3A` | Button hover |
| Silver (Accent on dark) | `#C8C8C8` | Accents on dark/photo sections |
| Ink | `#141414` | Headings, dark sections |
| Ink 2 | `#1E1E1E` | Secondary dark |
| Ink Soft | `#555555` | Body text |
| Off-White (Page) | `#FAFAFA` | Page background |
| Light Grey | `#F0F0F0` | Alternate sections |
| White | `#FFFFFF` | |
| Line Light / Line Dark | `rgba(0,0,0,.12)` / `rgba(255,255,255,.14)` | Dividers |
| Photo Overlay | `rgba(0,0,0,.62)` | Over hero photos |

## Font
**Plus Jakarta Sans** (Google) for headings and body — closest Google match to the logo wordmark.
Heading accent words: italic, `#6E6E6E` on light, `#C8C8C8` on dark (automatic, global JS).

## Buttons on dark
Solid black buttons on a dark section/photo are flipped to white automatically (`lc-btn-invert`,
global JS + CSS). The header "Plan Your Visit" button is always white.

## Logo files (transparent PNG, Media Library ids)
- `pcc-mark-white.png` (313) — used in the header/footer logo (headline graphic)
- `pcc-mark-black.png` (314)
- `pcc-logo-white.png` (315), `pcc-logo-black.png` (316) — full stacked logo
