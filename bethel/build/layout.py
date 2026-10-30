"""Bethel Church — header (id 13) and footer (id 458).

The header keeps its three bars (top bar, desktop, mobile) and the countdown /
off-canvas menu; colours, fonts, logo and sizes move to the brand. The footer is
rebuilt on the same section → container → rows shape.
"""
from kit import *  # noqa: F401,F403

LOGO_ON_LIGHT = "502:full"   # horizontal, Forest + Sage
LOGO_ON_DARK = "503:full"    # horizontal, Cream + Sage
NAV = [("About", "/about/"), ("Connect", "/connect/"), ("Ministries", "/ministries/"),
       ("Watch", "/watch/"), ("Events", "/events/"), ("Give", "/give/")]
YOUTUBE = "https://www.youtube.com/@BethelChurchEC"


def _strip(e):
    e = {k: v for k, v in e.items() if k not in ("_id",)}
    e["_modules"] = [_strip(m) for m in e.get("_modules", [])]
    return e


def header(original):
    top, desk, mob = [_strip(b) for b in original]

    # --- Top bar ------------------------------------------------------------
    top.update(bar_bg_color=FOREST_DEEP, bar_height="40px", bar_outer_spacing="40px", **{"class": "bc-topbar"})
    left, right = top["_modules"]
    for h in left["_modules"] + right["_modules"][1:2]:
        h.update(text_font_family=RALEWAY, text_font_size="11px", text_font_weight="600",
                 text_letter_spacing="0.14em", text_text_color=CREAM_SOFT, text_text_color_alt=SAGE)
        if h.get("text_content") == ".":
            h.update(text_content="·", text_text_color=SAGE)
    left["_modules"][0]["text_content"] = "Bethel Church"
    left["_modules"][4].update(text_href="tel:+14104655690", text_link=True)
    cd = right["_modules"][0]
    cd.update(countdown_complete_font_family=RALEWAY, countdown_complete_text_color=SAGE,
              countdown_digit_font_family=RALEWAY, countdown_digit_text_color=CREAM,
              countdown_label_font_family=RALEWAY, countdown_label_text_color=CREAM_SOFT)
    right["_modules"][2] = button("Watch Live", "/watch/", "primary-dark", small=True)
    right["_modules"][2].update(anchor_padding="5px 14px 5px 14px", anchor_primary_font_size="11px",
                                _region="top")

    # --- Desktop bar ----------------------------------------------------------
    desk.pop("bar_position_top", None)
    desk.update(bar_bg_color=WHITE, bar_height="84px", bar_outer_spacing="40px", bar_sticky=True,
                bar_box_shadow_dimensions="0px 1px 0px 0px", bar_box_shadow_color=LINE,
                **{"class": "bc-nav"})
    logo_c, nav_c, cta_c = desk["_modules"]
    logo_c["_modules"][0].update(image_src=LOGO_ON_LIGHT, image_alt="Bethel Church home",
                                 image_styled_width="172px", image_margin="0px 0px 0px 0px")
    nav_c.update(container_row_flex_gap="30px")
    for h, (label, href) in zip(nav_c["_modules"], NAV):
        h.update(text_content=label, text_href=href, text_font_family=RALEWAY, text_font_size="13px",
                 text_font_weight="600", text_letter_spacing="0.12em", text_text_color=FOREST,
                 text_text_color_alt=MOSS)
    cta = button("Plan Your Visit", "/new-here/", small=True, label="Button – Plan Your Visit")
    cta.update(_region="top", **{"class": "bc-nav-cta"})
    cta_c["_modules"] = [cta]

    # --- Mobile bar + off-canvas menu ------------------------------------------
    mob.update(bar_bg_color=WHITE, bar_height="72px", bar_sticky=True,
               bar_box_shadow_dimensions="0px 1px 0px 0px", bar_box_shadow_color=LINE,
               **{"class": "bc-nav"})
    mob["_modules"][0]["_modules"][0].update(image_src=LOGO_ON_LIGHT, image_alt="Bethel Church home",
                                             image_styled_max_width="150px", image_styled_width="150px")
    oc = mob["_modules"][1]["_modules"][0]
    oc.update(toggle_color=FOREST, toggle_color_alt=MOSS, off_canvas_close_color=a(CREAM, .7),
              off_canvas_close_color_alt=CREAM)
    head, links = oc["_modules"]
    head.update(layout_div_bg_color=FOREST_DEEP)
    head["_modules"][0].update(image_src=LOGO_ON_DARK, image_alt="Bethel Church home", image_styled_width="170px")
    links.update(layout_div_bg_color=FOREST, layout_div_flex_direction="column",
                 layout_div_flex_justify="flex-start", layout_div_flex_align="flex-start",
                 layout_div_flex_gap="22px", layout_div_padding="2.5em 2.25em 3em 2.25em")
    for h, (label, href) in zip(links["_modules"], NAV):
        h.update(text_content=label, text_href=href, text_font_family=LORA, text_font_size="24px",
                 text_font_weight="500", text_letter_spacing="0em", text_text_transform="none",
                 text_text_color=CREAM, text_text_color_alt=SAGE)
    menu_cta = button("Plan Your Visit", "/new-here/", "primary-dark", label="Button – Plan Your Visit")
    menu_cta.update(_region="top", anchor_margin="12px 0px 0px 0px")
    links["_modules"] = links["_modules"][:6] + [menu_cta]

    return [top, desk, mob]


def footer(original):
    socials = [_strip(s) for s in original[0]["_modules"][0]["_modules"][1]["_modules"][1]["_modules"]]
    for s in socials:
        s.update(anchor_bg_color="transparent", anchor_bg_color_alt=SAGE,
                 anchor_border_color=a(CREAM, .3), anchor_border_color_alt=SAGE,
                 anchor_graphic_icon_color=CREAM_SOFT, anchor_graphic_icon_color_alt=FOREST)
    socials[1].update(anchor_href=YOUTUBE, anchor_blank=True)

    def link(label, href):
        return el("headline", f"Link – {label}", text_content=label, text_href=href, text_link=True,
                  text_tag="p", text_font_family=RALEWAY, text_font_size="15px", text_font_weight="500",
                  text_line_height="1.5", text_text_color=CREAM_SOFT, text_text_color_alt=SAGE)

    def links_col(title, items):
        return col(f"Links – {title}", [label_text(title, dark=True, margin="0px 0px 18px 0px")] +
                   [link(*i) for i in items],
                   layout_column_flexbox=True, layout_column_flex_direction="column",
                   layout_column_flex_gap="12px", layout_column_flex_align="flex-start")

    main = row("Columns", [
        col("Brand", [
            el("image", "Logo", image_src=LOGO_ON_DARK, image_alt="Bethel Church", image_href="/",
               image_link=True, image_styled_width="210px", image_margin="0px 0px 22px 0px"),
            text("A welcoming church in Ellicott City, MD, centered on Christ, Bible teaching, worship and real community.",
                 dark=True, size="15px", max_width="340px"),
            flex("Social", socials, gap="10px", margin="26px 0px 0px 0px"),
        ]),
        links_col("Visit", [("Plan Your Visit", "/new-here/"), ("Sunday Schedule", "/new-here/#welcome"),
                            ("Directions & Parking", "https://maps.app.goo.gl/ENwadHsYQ4NQF4RBA"),
                            ("New Members", "/connect/#new-members")]),
        links_col("Ministries", [("Kids", "/connect/#kids-ministry"), ("Youth", "/connect/#youth-ministry"),
                                 ("Life Groups", "/connect/#life-groups"), ("Local Outreach", "/ministries/#local"),
                                 ("Global Missions", "/ministries/#missions")]),
        links_col("Resources", [("Watch Live", "/watch/"), ("Sermons", "/watch/"), ("Give Online", "/give/"),
                                ("Events Calendar", "/events/"), ("About Us", "/about/")]),
    ], layout="37% 21% 21% 21%", gap="40px", align="flex-start", md_layout="50% 50%", md_gap="40px")

    bottom = row("Bottom", [
        col("Copyright", [text('© 2026 Bethel Church · 4261 Bethel Overlook, Ellicott City, MD 21043 · '
                               '<a href="tel:+14104655690">(410) 465-5690</a>', dark=True, size="13px")]),
        col("Site", [text('<a href="mailto:office@meetbethel.org">office@meetbethel.org</a>', dark=True, size="13px")],
            layout_column_flexbox=True, layout_column_flex_justify="flex-end"),
    ], layout="70% 30%", gap="24px", gap_row="8px", md_gap="8px",
        layout_row_margin="64px auto 0px auto", layout_row_padding="28px 0px 0px 0px",
        layout_row_border_width="1px 0px 0px 0px", layout_row_border_style="solid",
        layout_row_border_color=a(CREAM, .14))

    s = section("Footer", [main, bottom], bg=FOREST_DEEP, pad="88px 0px 36px 0px", pad_md="72px 0px 32px 0px",
                pad_xs="56px 0px 28px 0px")
    return [s]
