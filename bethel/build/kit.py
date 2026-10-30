"""Bethel Church — Cornerstone element kit.

Every element the pages use is built here, so the brand lives in one place:
colours are Global Color references, fonts are Global Font ids, and the
responsive values are set once per element type. Pages (pages.py) only pass
content.
"""
import copy

# ---- Global Colors (Cornerstone › Global Colors) --------------------------------
FOREST = "global-color:B7ceVL47LpDvaYK6dk"       # #344027 primary
FOREST_DEEP = "global-color:sHNSyYvVXqgfvZpv7M"  # #283220 footer / top bar
MOSS = "global-color:lHurVnfekcuhxlV7qo"         # #6B8452 accent on light
SAGE = "global-color:NdEdveZYCy4oMLSPDU"         # #B5C99A accent on dark
MIST = "global-color:bcSageMistPnl01xQ7"         # #E6ECDB soft panels
STONE = "global-color:ECl1g52Y1Ujv0516sO"        # #5E6652 body text on light
CREAM = "global-color:y4jVp1zaTsbSXZ8L6y"        # #F5F2E9 page background
WHITE = "global-color:VJJLxKNw7i9FypDmu7"
CREAM_SOFT = "global-color:ttLr5Ed8AvOVNphWJF"   # body text on Forest
LINE = "global-color:bcForestLine02kP4m"         # hairlines / card borders


def a(color, alpha):
    """Global colour with opacity, e.g. a(FOREST, .8)."""
    return f"{color}:{alpha}"


# ---- Global Fonts ---------------------------------------------------------------
LORA = "GhSmfsWPTjG6E6omNz"     # "Headings"
RALEWAY = "H8ac4P2nc985hfvLdT"  # "Body Copy"

DARK_BGS = {FOREST, FOREST_DEEP}


# ---- Responsive helper ----------------------------------------------------------
# Base breakpoint is XL (index 4). Arrays are [xs, sm, md, lg, xl]; a value set on
# md applies to md and everything smaller unless overridden.
BP = {"xs": 0, "sm": 1, "md": 2, "lg": 3}


def bp(el, key, **sizes):
    data = el.setdefault("_bp_data4_4", {})
    arr = data.setdefault(key, [None] * 5)
    for name, val in sizes.items():
        arr[BP[name]] = val
    return el


def el(_type, label=None, children=None, **props):
    e = {"_type": _type, "_bp_base": "4_4"}
    if label:
        e["_label"] = label
    e.update({k: v for k, v in props.items() if v is not None})
    e["_modules"] = children or []
    return e


# ---- Layout ---------------------------------------------------------------------
def section(label, rows, bg=CREAM, pad="120px 0px 120px 0px", pad_md="88px 0px 88px 0px",
            pad_xs="64px 0px 64px 0px", image=None, video=None, poster=None, overlay=None,
            anchor=None, **extra):
    s = el("section", label, rows, section_bg_color=bg, section_padding=pad, id=anchor, **extra)
    if image or video:
        s.update(section_bg_advanced=True, bg_lower_type="video" if video else "image",
                 bg_lower_image=image, bg_lower_video=video, bg_lower_video_poster=poster,
                 bg_upper_type="color" if overlay else "none", bg_upper_color=overlay)
        s = {k: v for k, v in s.items() if v is not None}
    bp(s, "section_padding", md=pad_md, xs=pad_xs)
    return s


def row(label, cols, layout="50% 50%", gap="72px", gap_row="48px", align="center",
        md_layout="100%", md_gap="40px", xs_layout="100%", anchor=None, **extra):
    r = el("layout-row", label, cols, layout_row_layout=layout, layout_row_gap_column=gap,
           layout_row_gap_row=gap_row, layout_row_flex_align=align,
           layout_row_global_container=True, id=anchor, **extra)
    bp(r, "layout_row_layout", md=md_layout)
    if xs_layout and xs_layout != md_layout:
        bp(r, "layout_row_layout", xs=xs_layout)  # phones: one card per row
    bp(r, "layout_row_gap_row", md=md_gap)
    return r


def col(label, children, **extra):
    return el("layout-column", label, children, **extra)


def div(label, children, **extra):
    return el("layout-div", label, children, **extra)


def flex(label, children, direction="row", gap="14px", wrap=True, align="center",
         justify="flex-start", margin=None, **extra):
    return div(label, children, layout_div_flexbox=True, layout_div_flex_direction=direction,
               layout_div_flex_wrap=wrap, layout_div_flex_gap=gap, layout_div_flex_align=align,
               layout_div_flex_justify=justify, layout_div_margin=margin, **extra)


# ---- Type -----------------------------------------------------------------------
def eyebrow(text, dark=False, line=True, margin="0px 0px 20px 0px"):
    """Line + small spaced caps label above a heading."""
    color = SAGE if dark else MOSS
    kids = []
    if line:
        kids.append(el("line", "Line", line_color=color, line_size="2px", line_width="28px"))
    kids.append(el("headline", "Label", text_content=text, text_tag="span",
                   text_font_family=RALEWAY, text_font_weight="600", text_font_size="13px",
                   text_letter_spacing="0.2em", text_line_height="1.4",
                   text_text_transform="uppercase", text_text_color=color))
    return flex("Eyebrow", kids, gap="12px", wrap=False, margin=margin)


SIZES = {
    "h1": ("clamp(2.6rem, 4.6vw, 3.75rem)", "1.1", "500"),
    "h2": ("clamp(2.1rem, 3.4vw, 2.75rem)", "1.15", "500"),
    "h3": ("1.5rem", "1.25", "600"),
    "h4": ("1.25rem", "1.3", "600"),
}


def heading(text, tag="h2", dark=False, label=None, align=None, margin="0px 0px 20px 0px",
            size=None, max_width=None):
    fs, lh, fw = SIZES[tag]
    h = el("headline", label or ("Heading" if tag in ("h1", "h2") else "Title"),
           text_content=text, text_tag=tag, text_font_family=LORA, text_font_weight=fw,
           text_font_size=size or fs, text_line_height=lh, text_letter_spacing="-0.01em",
           text_text_color=CREAM if dark else FOREST, text_margin=margin,
           text_text_align=align, text_max_width=max_width)
    return h


def text(html, dark=False, label="Text", size="17px", margin="0px 0px 0px 0px",
         max_width=None, align=None, color=None, font=RALEWAY, weight="400", line="1.65",
         style=None):
    return el("text", label, text_content=html, text_font_family=font, text_font_weight=weight,
              text_font_size=size, text_line_height=line,
              text_text_color=color or (CREAM_SOFT if dark else STONE),
              text_margin=margin, text_max_width=max_width, text_text_align=align,
              text_font_style=style)


def label_text(text_, dark=False, label="Label", color=None, margin="0px 0px 6px 0px", size="12px"):
    """Spaced caps label without the line (cards, info lists)."""
    return el("headline", label, text_content=text_, text_tag="span", text_font_family=RALEWAY,
              text_font_weight="600", text_font_size=size, text_letter_spacing="0.18em",
              text_line_height="1.4", text_text_transform="uppercase",
              text_text_color=color or (SAGE if dark else MOSS), text_margin=margin)


def quote_text(text_, dark=False, size="clamp(1.5rem, 2.6vw, 2.1rem)", align=None, label="Quote",
               margin="0px 0px 18px 0px"):
    """Large Lora quote set as Text, so the heading accent never touches it."""
    return text(text_, dark=dark, label=label, size=size, font=LORA, weight="500", line="1.35",
                color=CREAM if dark else FOREST, align=align, margin=margin)


# ---- Buttons --------------------------------------------------------------------
BTN_STYLES = {
    # bg, text, border, bg hover, text hover, border hover
    "primary": (FOREST, CREAM, FOREST, FOREST_DEEP, CREAM, FOREST_DEEP),
    "outline": ("transparent", FOREST, FOREST, FOREST, CREAM, FOREST),
    "primary-dark": (SAGE, FOREST, SAGE, CREAM, FOREST, CREAM),
    "outline-dark": ("transparent", CREAM, a(CREAM, .55), CREAM, FOREST, CREAM),
}


def button(text_, href, style="primary", label=None, small=False, blank=False):
    if style in ("link", "link-dark"):
        c = SAGE if style == "link-dark" else FOREST
        return el("button", label or f"Link – {text_}", anchor_text_primary_content=text_,
                  anchor_href=href, anchor_blank=blank or None, anchor_bg_color="transparent",
                  anchor_bg_color_alt="transparent", anchor_padding="4px 0px 4px 0px",
                  anchor_border_radius="0px", anchor_primary_font_family=RALEWAY,
                  anchor_primary_font_weight="700", anchor_primary_font_size="13px",
                  anchor_primary_letter_spacing="0.12em", anchor_primary_text_transform="uppercase",
                  anchor_primary_text_color=c, anchor_primary_text_color_alt=MOSS if c == FOREST else CREAM,
                  anchor_box_shadow_dimensions="0em 0em 0em 0em",
                  anchor_flexbox=True, anchor_flex_direction="row-reverse", anchor_flex_align="center",
                  anchor_graphic=True, anchor_graphic_type="icon", anchor_graphic_icon="arrow-right",
                  anchor_graphic_icon_alt="arrow-right", anchor_graphic_icon_font_size="0.85em",
                  anchor_graphic_icon_width="1em", anchor_graphic_icon_height="1em",
                  anchor_graphic_icon_color=c, anchor_graphic_icon_color_alt=MOSS if c == FOREST else CREAM,
                  anchor_graphic_margin="0px 0px 0px 8px")
    bg, fg, br, bg2, fg2, br2 = BTN_STYLES[style]
    return el("button", label or f"Button – {text_}", anchor_text_primary_content=text_,
              anchor_href=href, anchor_blank=blank or None,
              anchor_bg_color=bg, anchor_bg_color_alt=bg2,
              anchor_border_width="1.5px", anchor_border_style="solid",
              anchor_border_color=br, anchor_border_color_alt=br2,
              anchor_border_radius="999px",
              anchor_padding="11px 22px 11px 22px" if small else "16px 30px 16px 30px",
              anchor_primary_font_family=RALEWAY, anchor_primary_font_weight="700",
              anchor_primary_font_size="12px" if small else "14px",
              anchor_primary_letter_spacing="0.1em", anchor_primary_text_transform="uppercase",
              anchor_primary_text_color=fg, anchor_primary_text_color_alt=fg2,
              anchor_box_shadow_dimensions="0em 0em 0em 0em")


def buttons(*btns, margin="36px 0px 0px 0px", justify="flex-start"):
    return flex("Buttons", list(btns), gap="14px", margin=margin, justify=justify)


# ---- Media ----------------------------------------------------------------------
def image(src, alt, height="520px", height_md="380px", radius="20px", label="Image", fit="cover",
          position=None):
    i = el("image", label, image_src=src, image_alt=alt, image_retina=False,
           image_object_fit=fit, image_object_position=position, image_styled_width="100%",
           image_styled_height=height, image_outer_border_radius=radius,
           image_inner_border_radius=radius, image_display="block")
    bp(i, "image_styled_height", md=height_md)
    return i


def card(label, children, bg=WHITE, pad="36px 32px 36px 32px", radius="18px", border=True,
         lift=False, **extra):
    d = div(label, children, layout_div_bg_color=bg, layout_div_padding=pad,
            layout_div_border_radius=radius, **extra)
    if lift:  # hover: rise 6px + soft shadow (Effects › Interaction)
        d.update(layout_div_box_shadow_dimensions="0px 24px 60px 0px", layout_div_box_shadow_color="transparent",
                 layout_div_box_shadow_color_alt=a(FOREST_DEEP, .12), effects_alt=True,
                 effects_transform_alt="translate(0px, -6px)", effects_duration="350ms")
    if border:
        d.update(layout_div_border_width="1px", layout_div_border_style="solid",
                 layout_div_border_color=LINE)
    return d


def icon(name, dark=False):
    return el("icon", "Icon", icon=name, icon_width="56px", icon_height="56px",
              icon_font_size="1.35em", icon_border_radius="100px",
              icon_bg_color=a(SAGE, .18) if dark else MIST, icon_color=SAGE if dark else FOREST,
              icon_margin="0px 0px 24px 0px")


def breadcrumbs():
    return el("breadcrumbs", "Breadcrumbs", breadcrumbs_font_family=RALEWAY,
              breadcrumbs_font_size="12px", breadcrumbs_font_weight="600",
              breadcrumbs_links_base_font_size="12px", breadcrumbs_links_letter_spacing="0.14em",
              breadcrumbs_links_text_transform="uppercase", breadcrumbs_links_color=a(CREAM, .7),
              breadcrumbs_links_color_alt=SAGE, breadcrumbs_delimiter_type="icon",
              breadcrumbs_delimiter_ltr_icon="slash-forward", breadcrumbs_delimiter_spacing="8px",
              breadcrumbs_delimiter_color=a(CREAM, .4), breadcrumbs_links_margin="!0px 0px 0px 0px",
              breadcrumbs_margin="0em 0em 28px 0em")


def counter(end, label, suffix=None, dark=False):
    return el("counter", f"Counter – {label}", counter_start="0", counter_end=end,
              counter_number_suffix_content=suffix, counter_duration="1400",
              counter_before_after=True, counter_after_content=label,
              counter_number_font_family=LORA, counter_number_font_weight="500",
              counter_number_font_size="2.6rem", counter_number_line_height="1",
              counter_number_text_color=CREAM if dark else FOREST,
              counter_number_margin="0px 0px 8px 0px",
              counter_before_after_font_family=RALEWAY, counter_before_after_font_weight="600",
              counter_before_after_font_size="12px", counter_before_after_letter_spacing="0.16em",
              counter_before_after_text_transform="uppercase",
              counter_before_after_text_color=SAGE if dark else MOSS,
              counter_number_text_align="left", counter_before_after_text_align="left")


def raw(content, label):
    return el("raw-content", label, raw_content=content)


# ---- Recurring blocks -----------------------------------------------------------
def page_hero(img, crumb_label, title, intro, eyebrow_text):
    """Inner-page hero: photo + Forest overlay, breadcrumbs, eyebrow, H1, intro."""
    return section("1. Hero", [
        row("Content", [
            col("Text", [
                breadcrumbs(),
                eyebrow(eyebrow_text, dark=True),
                heading(title, "h1", dark=True, margin="0px 0px 22px 0px"),
                text(intro, dark=True, size="19px", max_width="640px"),
            ]),
        ], layout="100%"),
    ], bg=FOREST, image=img, overlay=a(FOREST_DEEP, .8), pad="150px 0px 130px 0px",
        pad_md="120px 0px 96px 0px", pad_xs="96px 0px 72px 0px")


def section_head(eyebrow_text, title, intro=None, dark=False, max_width="720px", label="Heading Group"):
    kids = [eyebrow(eyebrow_text, dark=dark), heading(title, "h2", dark=dark, max_width=max_width)]
    if intro:
        kids.append(text(intro, dark=dark, max_width="640px"))
    return div(label, kids)


def info_item(lbl, value, dark=False):
    return div(f"Info – {lbl}", [
        label_text(lbl, dark=dark),
        text(value, dark=dark, size="17px", color=CREAM if dark else FOREST, weight="500", line="1.55"),
    ])


def global_block(block_id, label):
    return el("global-block", label, global_block_id=str(block_id))


def photo_card(img, tag, title, body, link_text, href):
    """Image card: photo background, Forest gradient, text at the bottom."""
    c = col(f"Card – {title}", [
        label_text(tag, dark=True, margin="0px 0px 10px 0px"),
        heading(title, "h3", dark=True, margin="0px 0px 10px 0px"),
        text(body, dark=True, size="15px", line="1.6", margin="0px 0px 18px 0px"),
        button(link_text, href, "link-dark"),
    ], layout_column_bg_advanced=True, bg_lower_type="image", bg_lower_image=img,
        bg_upper_type="color", bg_upper_color=a(FOREST_DEEP, .55),
        layout_column_flexbox=True, layout_column_flex_direction="column",
        layout_column_flex_justify="flex-end", layout_column_min_height="460px",
        layout_column_padding="32px 28px 32px 28px", layout_column_border_radius="18px",
        layout_column_overflow="hidden")
    bp(c, "layout_column_min_height", md="380px")
    return c


def strip_ids(tree):
    """Drop element ids so Cornerstone assigns fresh ones."""
    if isinstance(tree, list):
        return [strip_ids(t) for t in tree]
    t = {k: v for k, v in tree.items() if k != "_id"}
    t["_modules"] = [strip_ids(m) for m in t.get("_modules", [])]
    return t


def deep(x):
    return copy.deepcopy(x)
