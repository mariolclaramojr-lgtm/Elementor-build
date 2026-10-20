# Working rules (ReachRight church sites)

## Cornerstone / Themeco Pro builds — style with widget settings, not CSS
- Style every element through its own Cornerstone settings: Design, Typography, Border, Background,
  Flexbox, Position, Effects, and per-breakpoint values. This applies to sections, rows, columns, divs,
  headlines, text, buttons, images, icons, header/footer bars and containers.
- Don't add classes to widgets, and don't write custom CSS for anything a setting can do.
  Leave the Class and Element CSS fields empty unless a remaining CSS rule really needs the class.
- Use Global Colors and Global Fonts instead of hard-coded values.
- Global CSS (Theme Options › CSS) is only for what the builder can't reach. Examples: plugin/shortcode
  output (Gravity Forms, Sermon Manager, Modern Events Calendar) and animations with no native element.
  Keep it small. Give a class only to the elements those rules need.
- Before finishing, check every page for leftover classes or CSS no longer used, and remove them.
- Prefer native elements over Raw Content/HTML blocks so the client can edit content in the builder.
- Use real, specific copy for content blocks instead of placeholder text unless told otherwise.
