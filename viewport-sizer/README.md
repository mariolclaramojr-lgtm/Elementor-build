# Viewport Sizer (Chrome extension)

Load any site or page at an exact browser width or resolution.

## Install

1. Open `chrome://extensions`.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked** and pick this `viewport-sizer` folder.
4. Pin the extension from the puzzle-piece menu.

## Modes

| Mode | What it does | Best for |
| --- | --- | --- |
| **Resize window** | Resizes the current window so the page's viewport (what CSS media queries see) is exactly the width × height you set. It measures toolbars, borders, docked DevTools and page zoom and corrects for them. | Desktop / laptop widths |
| **Emulate** | Emulates the viewport inside the tab using Chrome's DevTools protocol: any size (even wider than your screen, scaled down to fit), pixel ratio, touch, and a mobile user agent. Chrome shows a "started debugging this browser" bar while it's on. | Phones, tablets, widths below ~500px or above your screen |
| **New window** | Opens the current page (or a URL you type) in a new window with that exact viewport. | Side-by-side comparisons |

Leave **Height** empty to keep the current height. **Reset** stops emulation and puts the window back to its original size.

## Presets

Phones, tablets, common desktop resolutions and Elementor's default breakpoints (767, 880, 1024, 1200, 1366, 2400). Click one to apply it in the current mode. **Save** stores the current fields as a custom preset (synced to your Chrome profile); right-click a saved preset to delete it.

## Shortcuts

- `Alt+Shift+V` — re-apply the last size to the current tab
- `Alt+Shift+R` — reset

Change them at `chrome://extensions/shortcuts`.

## Notes

- Operating systems stop windows at a minimum width (around 500px), and a window can't be much bigger than the screen. When Resize can't reach the exact size it tells you what it got — use **Emulate** for those sizes.
- With **Mobile** on, pages without a `<meta name="viewport">` tag lay out at 980px, the same as a real phone.
- Chrome blocks extensions from `chrome://` pages and the Chrome Web Store, so Emulate won't run there.
