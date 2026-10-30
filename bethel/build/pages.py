"""Bethel Church — page, component, header and footer trees.

Same section count per page as the original site; content carried over,
"Bethel Baptist" / "RR Bethel" renamed to "Bethel Church" (brand guidelines).
Component ids are filled in by the deploy script (COMPONENTS).
"""
from kit import *  # noqa: F401,F403

COMPONENTS = {"find_us": None, "visit_cta": None}

VIDEO = "/wp-content/uploads/2025/02/rr-cover-vid_1920x1080.mp4"
MAP = ('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3089.5315709284573'
       '!2d-76.816688!3d39.25350400000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2'
       '!1s0x89c81f8c491062f9%3A0x28f8d4b45d4f9e99!2sBethel%20Baptist%20Church%20-%20Ellicott'
       '%20City%2C%20MD!5e0!3m2!1sen!2sph!4v1781723417207!5m2!1sen!2sph" width="600" height="450" '
       'style="border:0;" allowfullscreen="" loading="lazy" '
       'referrerpolicy="no-referrer-when-downgrade"></iframe>')
DIRECTIONS = "https://maps.app.goo.gl/ENwadHsYQ4NQF4RBA"


# =============================================================================
# Components (edit once, every page updates)
# =============================================================================
def component_find_us():
    return [row("Content", [
        col("Text", [
            section_head("Find us", "We'd love to meet you",
                         "Whether you have a question, need directions, or just want to say hello, we're here."),
            div("Contact Details", [
                info_item("Address", "4261 Bethel Overlook<br>Ellicott City, MD 21043"),
                info_item("Sunday schedule", "Journey Groups · 9:15 AM<br>Worship Service · 10:30 AM"),
                info_item("Phone", '<a href="tel:+14104655690">(410) 465-5690</a>'),
            ], layout_div_flexbox=True, layout_div_flex_direction="column", layout_div_flex_gap="22px",
                layout_div_margin="36px 0px 0px 0px", layout_div_padding="28px 0px 0px 0px",
                layout_div_border_width="1px 0px 0px 0px", layout_div_border_style="solid",
                layout_div_border_color=LINE),
            buttons(button("Plan Your Visit", "/new-here/"), button("Get Directions", DIRECTIONS, "outline", blank=True)),
        ]),
        col("Map", [
            el("map", "Map", map_embed_code=MAP, frame_content_sizing="aspect-ratio",
               frame_content_aspect_ratio_width="4", frame_content_aspect_ratio_height="4.4",
               frame_border_radius="20px", frame_bg_color=MIST),
        ]),
    ])]


def component_visit_cta():
    return [row("Content", [
        col("Text", [
            heading("New here? Let's meet", "h2", align="center", margin="0px 0px 16px 0px"),
            text("We'd love to have you join us this Sunday. No perfect church experience required, just come as you are.",
                 align="center", max_width="560px"),
            buttons(button("Plan Your Visit", "/new-here/"), button("Get Directions", DIRECTIONS, "outline", blank=True),
                    justify="center"),
        ], layout_column_flexbox=True, layout_column_flex_direction="column", layout_column_flex_align="center"),
    ], layout="100%")]


def find_us_section(n):
    return section(f"{n}. Find Us (component)", [global_block(COMPONENTS["find_us"], "Find Us")], bg=WHITE)


def visit_cta_section(n):
    return section(f"{n}. Plan Your Visit (component)", [global_block(COMPONENTS["visit_cta"], "Plan Your Visit CTA")],
                   bg=MIST, pad="104px 0px 104px 0px")


def image_with_quote(img, alt, badge_big, badge_small, quote, cite):
    """Photo, a Forest badge on top, and a quote card overlapping the bottom edge."""
    return col("Image", [
        div("Image Frame", [
            image(img, alt, height="560px", height_md="420px"),
            div("Badge", [
                text(badge_big, label="Badge Number", font=LORA, weight="500", size="2.2rem", line="1",
                     color=CREAM, align="center"),
                label_text(badge_small, dark=True, margin="6px 0px 0px 0px", size="11px"),
            ], layout_div_flexbox=True, layout_div_flex_direction="column", layout_div_flex_align="center",
                layout_div_flex_justify="center", layout_div_width="132px", layout_div_height="132px",
                layout_div_border_radius="100px", layout_div_bg_color=FOREST,
                layout_div_position="absolute", layout_div_top="24px", layout_div_right="24px",
                layout_div_padding="12px 12px 12px 12px", layout_div_text_align="center"),
        ], layout_div_position="relative"),
        card("Quote Card", [
            quote_text(f"“{quote}”", size="1.3rem", margin="0px 0px 14px 0px"),
            label_text(f"— {cite}", margin="0px 0px 0px 0px"),
        ], pad="28px 30px 28px 30px", layout_div_margin="-72px 28px 0px 28px",
            layout_div_position="relative", layout_div_z_index="2",
            layout_div_box_shadow_dimensions="0px 24px 60px 0px", layout_div_box_shadow_color=a(FOREST_DEEP, .16)),
    ])


# =============================================================================
# Home (10 sections)
# =============================================================================
def home():
    service = card("Service Card", [
        label_text("Join us this Sunday", dark=True, margin="0px 0px 22px 0px"),
        div("Times", [
            info_item("Journey Groups", "9:15 AM", dark=True),
            info_item("Worship Service", "10:30 AM", dark=True),
            info_item("Where", "4261 Bethel Overlook<br>Ellicott City, MD", dark=True),
        ], layout_div_flexbox=True, layout_div_flex_direction="column", layout_div_flex_gap="20px"),
        buttons(button("Get Directions", DIRECTIONS, "link-dark", blank=True), margin="28px 0px 0px 0px"),
    ], bg=a(FOREST_DEEP, .55), pad="36px 34px 36px 34px", border=False, effects_backdrop_filter="blur(10px)",
        layout_div_border_width="1px", layout_div_border_style="solid",
        layout_div_border_color=a(SAGE, .35), layout_div_max_width="380px")

    ticker = [
        "Find real community", "Sunday Worship · 10:30 AM", "Journey Groups · 9:15 AM",
        "Ellicott City, MD", "Kids · Youth · Groups · New Members", "All are welcome here",
    ]
    slides = []
    for t in ticker:
        slides.append(el("layout-slide", t, [label_text(t, color=FOREST, margin="0px 0px 0px 0px", size="12px")],
                         layout_slide_flexbox=True, layout_slide_flex_align="center",
                         layout_slide_flex_justify="center"))
        slides.append(el("layout-slide", "Dot", [text("•", label="Dot", color=MOSS, size="14px", line="1")],
                         layout_slide_flexbox=True, layout_slide_flex_align="center",
                         layout_slide_flex_justify="center"))
    marquee = el("layout-slide-container", "Marquee", slides,
                 layout_slide_container_autoplay="marquee", layout_slide_container_autoplay_start_in_view=False,
                 layout_slide_container_inline_align="center", layout_slide_container_inline_gap="1.6em",
                 layout_slide_container_inline_justify="center", layout_slide_container_inline_marquee_speed="0.1",
                 layout_slide_container_inline_page_count="6", layout_slide_container_inline_slide_basis="auto",
                 layout_slide_container_inline_wrap_around=True,
                 layout_slide_container_keyboard_navigation=False, layout_slide_container_starting_slide="1")

    path_cards = []
    for num, ic, title, body, link, href in [
        ("01", "church", "Show up",
         "Church is a gathering, and that's where your journey starts. Connect to Christ and build a relationship that becomes the foundation for everything you do.",
         "Get Started", "/new-here/"),
        ("02", "seedling", "Grow up",
         "Loneliness was never the long-term plan for your life. We're here to help you find your people and build friendships that last through every season.",
         "Find a Group", "/connect/#life-groups"),
        ("03", "hand-holding-heart", "Step up",
         "You're not just gifted, you're a gift. Discover the joy of using your unique influence to serve and impact others.",
         "Get Involved", "/ministries/"),
    ]:
        path_cards.append(col(f"Card – {title}", [card("Card", [
            flex("Card Top", [icon(ic), text(num, label="Number", font=LORA, weight="500", size="1.1rem",
                                            color=MOSS, line="1")],
                 justify="space-between", align="flex-start", wrap=False),
            heading(title, "h3", margin="0px 0px 12px 0px"),
            text(body, size="16px", margin="0px 0px 22px 0px"),
            button(link, href, "link"),
        ], lift=True, layout_div_height="100%")]))

    events = []
    for img, when, title, body in [
        ("485:full", "Every Sunday · 10:30 AM", "Sunday Worship",
         "Worship with us: songs, prayer and Bible teaching for every age and stage."),
        ("460:full", "Sundays · 9:15 AM", "Journey Groups",
         "Meet people, study the Bible and build friendships before worship."),
        ("461:full", "This summer", "KidsFest",
         "A week of games, music and Bible stories for the whole family."),
    ]:
        events.append(col(f"Card – {title}", [card("Card", [
            image(img, title, height="230px", height_md="230px", radius="0px"),
            div("Card Body", [
                label_text(when, margin="0px 0px 10px 0px"),
                heading(title, "h3", margin="0px 0px 10px 0px"),
                text(body, size="16px"),
            ], layout_div_padding="26px 28px 30px 28px"),
        ], pad="0px 0px 0px 0px", lift=True, layout_div_overflow_x="hidden",
            layout_div_overflow_y="hidden", layout_div_height="100%")]))

    connect_cards = [
        photo_card("488:full", "For families", "Kids", "A safe, fun space where children encounter the love of Jesus every Sunday.", "Learn More", "/connect/#kids-ministry"),
        photo_card("489:full", "Students", "Youth", "Middle and high schoolers finding community and growing in faith together.", "Learn More", "/connect/#youth-ministry"),
        photo_card("490:full", "Community", "Groups", "Journey Groups meet weekly for Bible study, prayer and real friendship.", "Learn More", "/connect/#life-groups"),
        photo_card("491:full", "Next step", "New Members", "Learn about Bethel, our beliefs and how to get connected with our church family.", "Learn More", "/new-here/"),
    ]

    hero_row = row("Content", [
        col("Text", [
            eyebrow("Ellicott City · Howard County", dark=True),
            heading("Find community and hope at Bethel Church.", "h1", dark=True,
                    size="clamp(2.8rem, 5.4vw, 4.5rem)", margin="0px 0px 24px 0px"),
            text("A place to belong, grow in faith and discover hope in Jesus, whether you're new to church, returning, or just exploring.",
                 dark=True, size="19px", max_width="560px"),
            buttons(button("Plan Your Visit", "/new-here/", "primary-dark"),
                    button("View Events", "/events/", "outline-dark")),
        ]),
        col("Service Times", [service], layout_column_flexbox=True, layout_column_flex_justify="center",
            layout_column_flex_align="flex-end"),
    ], layout="60% 40%", gap="64px")
    bp(hero_row["_modules"][1], "layout_column_flex_align", md="flex-start")

    return [
        section("1. Hero (video)", [hero_row], bg=FOREST, video=VIDEO, poster="323:full", image="485:full",
                overlay=a(FOREST_DEEP, .78), pad="150px 0px 150px 0px", pad_md="110px 0px 96px 0px",
                pad_xs="88px 0px 72px 0px"),
        section("2. Ticker + Announcement", [row("Content", [
            col("Ticker", [marquee], layout_column_overflow="hidden"),
            col("Announcement", [flex("Announcement", [
                text("KidsFest is coming this summer! Fun for the whole family.", size="15px", color=FOREST, weight="600"),
                button("Learn More", "/connect/#kids-ministry", "link"),
            ], gap="18px", justify="flex-end")]),
        ], layout="62% 38%", gap="32px", md_gap="14px")], bg=MIST, pad="18px 0px 18px 0px", pad_md="18px 0px 18px 0px",
            pad_xs="16px 0px 16px 0px"),
        section("3. Welcome", [row("Content", [
            col("Text", [
                section_head("Welcome to Bethel", "Community and hope start here"),
                text("At Bethel, we seek to provide a place for people to find community, grow in faith and find hope in Jesus. "
                     "Whether you're new to church, returning after time away, or looking for a church home in Ellicott City, we'd love to welcome you."),
                buttons(button("About Us", "/about/"), button("Plan a Visit", "/new-here/", "outline")),
            ]),
            image_with_quote("487:full", "Bethel Church members after Sunday worship", "10:30", "Sundays",
                             "Bethel is a church where people make friends quickly and hear the word of God every week.",
                             "Bill Sanders, Bethel member"),
        ])], bg=CREAM, anchor="about"),
        section("4. Connect (cards)", [
            row("Heading", [
                col("Text", [section_head("Find your people", "There's a place for you here",
                                          "From kids and youth to small groups and new members, find where you belong.", dark=True)]),
                col("Button", [button("Explore Ministries", "/ministries/", "outline-dark")],
                    layout_column_flexbox=True, layout_column_flex_justify="flex-end", layout_column_flex_align="flex-end"),
            ], layout="65% 35%", align="flex-end"),
            row("Cards", connect_cards, layout="25% 25% 25% 25%", gap="20px", gap_row="20px",
                md_layout="50% 50%", md_gap="20px", layout_row_margin="56px auto 0px auto"),
        ], bg=FOREST, anchor="connect"),
        section("5. Your Path", [
            row("Heading", [col("Text", [section_head("Your path at Bethel", "What does it mean to live in community?")])], layout="100%"),
            row("Cards", path_cards, layout="33.33% 33.33% 33.33%", gap="24px", gap_row="24px",
                align="stretch", md_gap="20px", layout_row_margin="48px auto 0px auto"),
        ], bg=CREAM, anchor="ministries"),
        section("6. Mission", [row("Content", [col("Quote", [
            el("line", "Line", line_color=SAGE, line_size="2px", line_width="48px", line_margin="0px auto 32px auto"),
            quote_text("“At Bethel, we seek to provide a place for people to find community, grow in faith, and find hope in Jesus.”",
                       dark=True, align="center", size="clamp(1.6rem, 3vw, 2.4rem)"),
            label_text("— Bethel Church", dark=True, margin="8px 0px 0px 0px"),
        ], layout_column_flexbox=True, layout_column_flex_direction="column", layout_column_flex_align="center",
            layout_column_max_width="880px", layout_column_text_align="center")],
            layout="100%", layout_row_flex_justify="center")], bg=FOREST_DEEP, image="476:full",
            overlay=a(FOREST_DEEP, .86), pad="128px 0px 128px 0px"),
        section("7. Watch & Listen", [row("Content", [
            col("Text", [
                section_head("Sermons", "Watch and listen",
                             "Our pastors bring the Word in a way that's honest, relevant and never boring. Missed a Sunday? We've got you covered."),
                card("Now Preaching", [
                    label_text("Now preaching"),
                    heading("Revelation: The Alpha and the Omega", "h3", margin="0px 0px 0px 0px"),
                ], bg=MIST, border=False, pad="24px 28px 24px 28px", radius="14px",
                    layout_div_margin="28px 0px 0px 0px"),
                buttons(button("Watch Live", "/watch/"), button("Previous Sermons", "/watch/", "outline")),
            ]),
            col("Image", [
                div("Series Tag", [label_text("Current series", color=FOREST, margin="0px 0px 0px 0px", size="11px")],
                    layout_div_bg_color=SAGE, layout_div_border_radius="999px", layout_div_padding="7px 14px 7px 14px"),
                div("Quote", [
                    quote_text("“Bethel is a church where people make friends quickly and hear the word of God every week.”",
                               dark=True, size="1.45rem", margin="0px 0px 14px 0px"),
                    label_text("— Bill Sanders, Bethel member", dark=True, margin="0px 0px 0px 0px"),
                ], layout_div_padding="22px 0px 0px 24px", layout_div_border_width="0px 0px 0px 2px",
                    layout_div_border_style="solid", layout_div_border_color=SAGE),
            ], layout_column_bg_advanced=True, bg_lower_type="image", bg_lower_image="459:full",
                bg_upper_type="color",
                bg_upper_color=a(FOREST_DEEP, .45),
                layout_column_flexbox=True, layout_column_flex_direction="column",
                layout_column_flex_justify="space-between", layout_column_flex_align="flex-start",
                layout_column_min_height="560px", layout_column_padding="32px 36px 40px 36px",
                layout_column_border_radius="20px", layout_column_overflow="hidden"),
        ])], bg=WHITE, anchor="watch"),
        section("8. Upcoming Events", [
            row("Heading", [
                col("Text", [section_head("What's coming up", "Upcoming events")]),
                col("Button", [button("View Full Calendar", "/events/", "outline")],
                    layout_column_flexbox=True, layout_column_flex_justify="flex-end", layout_column_flex_align="flex-end"),
            ], layout="65% 35%", align="flex-end"),
            row("Cards", events, layout="33.33% 33.33% 33.33%", gap="24px", gap_row="24px", align="stretch",
                md_gap="20px", layout_row_margin="48px auto 0px auto"),
        ], bg=CREAM, anchor="events"),
        section("9. Newsletter (form)", [row("Content", [
            col("Text", [
                eyebrow("Stay in the loop", dark=True),
                heading("Keep up with Bethel", "h2", dark=True),
                text("Info straight to your inbox. Never miss a thing: events, messages and community updates.", dark=True, max_width="460px"),
            ]),
            col("Form", [card("Form Box", [
                el("form-integration", "Form (Gravity Forms)", form_integration_type="gravity-forms",
                   form_integration_gravityforms_id="1", form_integration_width="100%"),
            ], bg=a(CREAM, .06), border=False, pad="36px 36px 36px 36px",
                layout_div_border_width="1px", layout_div_border_style="solid", layout_div_border_color=a(SAGE, .3))]),
        ], layout="45% 55%")], bg=FOREST, anchor="give"),
        find_us_section(10),
    ]


# =============================================================================
# About (6 sections)
# =============================================================================
def about():
    beliefs = []
    for ic, title, body in [
        ("book-bible", "The Bible", "We believe the Bible is God's inspired Word, fully trustworthy and our final authority for faith and life."),
        ("cross", "The Trinity", "We believe in one God, eternally existing in three persons: Father, Son and Holy Spirit."),
        ("heart", "Salvation by grace", "We believe salvation is a gift, received by faith in Jesus Christ alone, not earned through good works."),
        ("church", "The church", "We believe the church is God's family, gathered to worship, grow together in His Word and serve our neighbors."),
        ("dove", "Baptism and communion", "We practice believer's baptism and communion as ongoing, meaningful expressions of faith in Christ."),
        ("sun", "Christ's return", "We believe Jesus will return in glory to fully establish His kingdom and make all things new."),
    ]:
        beliefs.append(col(f"Card – {title}", [card("Card", [
            icon(ic), heading(title, "h3", margin="0px 0px 12px 0px"), text(body, size="16px"),
        ], lift=True, layout_div_height="100%")]))

    team = []
    for img, name, role in [("499:full", "Ken Cavey", "Senior Pastor"), ("498:full", "Del Morgan", "Worship Pastor"),
                            ("497:full", "Jimmy Jackson", "Adult Pastor Emeritus"), ("374:full", "David Whitman", "Senior Pastor")]:
        team.append(col(f"Card – {name}", [
            image(img, f"{name}, {role}", height="380px", height_md="340px", radius="18px", position="center top"),
            heading(name, "h3", margin="22px 0px 6px 0px"),
            label_text(role, margin="0px 0px 0px 0px"),
        ]))

    return [
        page_hero("476:full", "About", "About Bethel",
                  "A church in Ellicott City built on Scripture, shaped by community, and devoted to helping people find real, lasting faith in Jesus.",
                  "Who we are"),
        section("2. Our Story", [row("Content", [
            col("Text", [
                section_head("Our story", "Rooted here since 1961"),
                text("Bethel Church has been serving the Ellicott City community since February 2, 1961. For more than sixty years, "
                     "we've grown into a multigenerational church family rooted in Scripture and committed to making disciples who make disciples. "
                     "What started as a small gathering of believers has become a thriving community of faith, welcoming people from Ellicott City, "
                     "Dunloggin, Autumn Hill, Wheatfield Way and beyond. We believe every person deserves a place to belong, and we'd love for that place to be Bethel."),
                flex("Counters", [counter("1961", "Founded"), counter("12", "Ministries", "+"), counter("3", "Weekly gatherings")],
                     gap="48px", margin="40px 0px 0px 0px", align="flex-start",
                     layout_div_padding="32px 0px 0px 0px", layout_div_border_width="1px 0px 0px 0px",
                     layout_div_border_style="solid", layout_div_border_color=LINE),
            ]),
            image_with_quote("477:full", "Bethel Church family", "65", "Years strong",
                             "We want Bethel to feel less like an event you attend and more like a family you belong to.",
                             "David Whitman, Senior Pastor"),
        ])], bg=WHITE, anchor="about"),
        section("3. What We Believe", [
            row("Heading", [col("Text", [section_head("What we believe", "The truths we stand on",
                                                      "Our beliefs are rooted in Scripture and shape how we worship, teach and live as a church family.")])],
                layout="100%"),
            row("Cards", beliefs, layout="33.33% 33.33% 33.33%", gap="24px", gap_row="24px", align="stretch",
                md_layout="50% 50%", md_gap="20px", layout_row_margin="48px auto 0px auto"),
        ], bg=CREAM, anchor="beliefs"),
        section("4. Scripture", [row("Content", [col("Quote", [
            el("line", "Line", line_color=SAGE, line_size="2px", line_width="48px", line_margin="0px auto 32px auto"),
            quote_text("“And they continued stedfastly in the apostles' doctrine and fellowship, and in breaking of bread, and in prayers.”",
                       dark=True, align="center", size="clamp(1.6rem, 3vw, 2.3rem)"),
            label_text("— Acts 2:42, KJV", dark=True, margin="8px 0px 0px 0px"),
        ], layout_column_flexbox=True, layout_column_flex_direction="column", layout_column_flex_align="center",
            layout_column_max_width="900px", layout_column_text_align="center")],
            layout="100%", layout_row_flex_justify="center")], bg=FOREST, pad="112px 0px 112px 0px"),
        section("5. Pastors & Staff", [
            row("Heading", [col("Text", [section_head("Meet our team", "Pastors and staff",
                                                      "The people who lead, teach and serve alongside our church family every week.")])],
                layout="100%"),
            row("Team", team, layout="25% 25% 25% 25%", gap="24px", gap_row="40px", align="flex-start",
                md_layout="50% 50%", xs_layout="50% 50%", md_gap="32px", layout_row_margin="48px auto 0px auto"),
        ], bg=WHITE, anchor="team"),
        visit_cta_section(6),
    ]


# =============================================================================
# New Here (4 sections)
# =============================================================================
def new_here():
    faq = [
        ("How can I contact Bethel Church?",
         "You can call us at (410) 465-5690, email office@meetbethel.org, or send a message through the form on our home page."),
        ("What are the church office hours?", "Our church office is open Monday through Thursday from 9:00 AM to 4:00 PM."),
        ("How quickly will you respond to my message?",
         "We aim to respond to messages within 24 hours. Messages received outside office hours are answered on the next business day."),
        ("Where is Bethel Church located?", "Bethel Church is at 4261 Bethel Overlook, Ellicott City, MD 21043."),
    ]

    def accordion(items, label):
        return el("accordion", label, [
            el("accordion-item-elements", q, [text(ans, size="16px")], _region="content",
               accordion_item_header_content=q) for q, ans in items
        ], accordion_grouped=True, accordion_item_spacing="12px", accordion_item_bg_color=WHITE,
            accordion_item_border_width="1px", accordion_item_border_style="solid",
            accordion_item_border_color=LINE, accordion_item_border_radius="14px", accordion_item_overflow=True,
            accordion_header_bg_color=WHITE, accordion_header_bg_color_alt=WHITE,
            accordion_header_padding="20px 24px 20px 24px", accordion_header_font_family=LORA,
            accordion_header_font_weight="600", accordion_header_font_size="1.1rem",
            accordion_header_text_color=FOREST, accordion_header_text_color_alt=MOSS,
            accordion_header_indicator_color=MOSS, accordion_header_indicator_color_alt=FOREST,
            accordion_content_padding="0px 24px 22px 24px", accordion_content_bg_color=WHITE)

    return [
        page_hero("478:full", "New Here", "Welcome home",
                  "Whether you're visiting for the first time or looking for a church to call home, we're glad you're here. "
                  "Bethel Church is a place to grow in faith, build meaningful relationships and experience the love of God in community.",
                  "Start here"),
        section("2. Welcome + FAQ", [
            row("Welcome", [
                col("Text", [
                    section_head("Welcome", "Welcome to our community"),
                    text("<p>We're so glad you're here. Whether you're visiting for the first time, exploring our programs, or looking for a place to belong, you are welcome here.</p>"
                         "<p>Our heart is to create a safe, encouraging and faith-filled environment where individuals and families can grow together, build meaningful connections and experience genuine community.</p>"),
                    flex("Counters", [counter("1961", "Founded"), counter("12", "Ministries", "+"), counter("3", "Weekly gatherings")],
                         gap="48px", margin="32px 0px 0px 0px", align="flex-start",
                         layout_div_padding="28px 0px 0px 0px", layout_div_border_width="1px 0px 0px 0px",
                         layout_div_border_style="solid", layout_div_border_color=LINE),
                ]),
                col("Video", [el("video", "Welcome Video", video_type="player", mejs_type="video",
                                 mejs_source_files=VIDEO, mejs_poster="323:full", mejs_preload="metadata",
                                 frame_content_sizing="aspect-ratio", frame_content_aspect_ratio_width="16",
                                 frame_content_aspect_ratio_height="10", frame_border_radius="20px",
                                 frame_bg_color=FOREST)]),
            ]),
            row("FAQ Heading", [col("Text", [section_head("FAQ", "Frequently asked questions")])],
                layout="100%", layout_row_margin="104px auto 0px auto"),
            row("FAQ", [col("Accordion", [accordion(faq[:2], "Accordion – Contact")]),
                        col("Accordion", [accordion(faq[2:], "Accordion – Visiting")])],
                layout="50% 50%", gap="20px", gap_row="12px", align="flex-start", md_gap="12px",
                layout_row_margin="36px auto 0px auto"),
        ], bg=WHITE, anchor="welcome"),
        section("3. Families", [row("Content", [
            col("Text", [
                section_head("Families", "A place for every family"),
                text("<p>Families are at the heart of our community. We believe strong families create strong communities, and we're committed to supporting every stage of life.</p>"
                     "<p>From children and students to parents and grandparents, we provide opportunities for families to grow together, build friendships and create lasting memories.</p>"),
                buttons(button("Get Connected", "/connect/")),
            ]),
            col("Image", [
                div("Quote", [
                    quote_text("“As for me and my house, we will serve the Lord.”", dark=True, size="1.6rem",
                               margin="0px 0px 14px 0px"),
                    label_text("— Joshua 24:15", dark=True, margin="0px 0px 0px 0px"),
                ], layout_div_padding="4px 0px 4px 24px", layout_div_border_width="0px 0px 0px 2px",
                    layout_div_border_style="solid", layout_div_border_color=SAGE),
            ], layout_column_bg_advanced=True, bg_lower_type="image", bg_lower_image="460:full",
                bg_upper_type="color",
                bg_upper_color=a(FOREST_DEEP, .45),
                layout_column_flexbox=True, layout_column_flex_direction="column", layout_column_flex_justify="flex-end",
                layout_column_min_height="520px", layout_column_padding="36px 36px 40px 36px",
                layout_column_border_radius="20px", layout_column_overflow="hidden"),
        ])], bg=CREAM, anchor="families"),
        find_us_section(4),
    ]


# =============================================================================
# Ministries (4 sections)
# =============================================================================
def split(n, label, img, alt, eb, title, body, btn, href, bg, image_first=True, anchor=None):
    img_col = col("Image", [image(img, alt)])
    txt_col = col("Text", [section_head(eb, title), text(body), buttons(button(btn, href))])
    r = row("Content", [img_col, txt_col] if image_first else [txt_col, img_col])
    if not image_first:
        r["layout_row_reverse"] = False
    return section(f"{n}. {label}", [r], bg=bg, anchor=anchor)


def ministries():
    return [
        page_hero("480:full", "Ministries", "Grow in community",
                  "God created us to live in relationship, with Him and with one another. Our ministries help every person, "
                  "at every stage of life, grow in faith, build meaningful connections and discover their God-given purpose.",
                  "Find your place"),
        split(2, "Serving Our Community", "481:full", "Bethel Church volunteers serving in Ellicott City", "Local programs",
              "Serving our community",
              "Through local outreach programs, Bethel Church shares God's love by serving families, supporting those in need "
              "and bringing hope to our community through practical care and ministry.",
              "Get Connected", "/connect/", WHITE, anchor="local"),
        split(3, "Global Missions", "482:full", "Global missions partners", "Global missions", "Reaching the nations",
              "We believe in sharing the Gospel beyond our walls. Through global missions, we support ministry efforts, "
              "partnerships and outreach that help bring the message of Jesus to people around the world.",
              "Get Connected", "/connect/", CREAM, image_first=False, anchor="missions"),
        visit_cta_section(4),
    ]


# =============================================================================
# Connect (6 sections)
# =============================================================================
def connect():
    return [
        page_hero("470:full", "Connect", "Find your place",
                  "At Bethel Church, life is better together. Whether you're new, looking for community, or ready to grow in faith, "
                  "there's a place for you here. Take your next step and get connected.",
                  "Connect with us"),
        split(2, "Kids Ministry", "471:full", "Kids ministry at Bethel Church", "Kids", "Kids ministry",
              "A fun, safe and faith-filled environment where children learn about Jesus, build friendships and grow in God's love. "
              "Our Kids Ministry helps every child feel welcomed, valued and excited to grow in their faith each week.",
              "Get Connected", "/new-here/", WHITE, image_first=False, anchor="kids-ministry"),
        split(3, "Youth Ministry", "472:full", "Youth ministry at Bethel Church", "Youth", "Youth ministry",
              "A place where students belong, grow and discover their purpose in Christ. Through worship, Bible teaching, events "
              "and real friendships, we help young people build a strong foundation of faith for everyday life.",
              "Get Connected", "/new-here/", CREAM, anchor="youth-ministry"),
        split(4, "Life Groups", "473:full", "A Bethel Church life group", "Groups", "Life groups",
              "We were never meant to do life alone. Life Groups are where real relationships happen: a place to pray together, "
              "study God's Word, encourage one another and grow in community throughout the week.",
              "Get Connected", "/new-here/", WHITE, image_first=False, anchor="life-groups"),
        split(5, "New Members", "474:full", "New members at Bethel Church", "New members", "New here?",
              "We'd love to help you get connected at Bethel Church. Whether you're visiting for the first time or ready to make this "
              "your church home, our New Members process helps you learn who we are, what we believe and how you can grow with us.",
              "Get Connected", "/new-here/", CREAM, anchor="new-members"),
        find_us_section(6),
    ]


# =============================================================================
# Give (3 sections)
# =============================================================================
def give():
    ways = []
    for ic, title, body, btn in [
        ("church", "Give on Sunday", "Give during our worship services through the offering boxes or designated giving areas.", None),
        ("mobile-screen-button", "Give online", "Give securely and conveniently through our online giving platform, anytime.", ("Give Now", "#give-online")),
        ("envelope", "Give by mail", "Bethel Church<br>4261 Bethel Overlook<br>Ellicott City, MD 21043", None),
    ]:
        kids = [icon(ic), heading(title, "h3", margin="0px 0px 12px 0px"), text(body, size="16px")]
        if btn:
            kids.append(buttons(button(*btn, small=True), margin="22px 0px 0px 0px"))
        ways.append(col(f"Card – {title}", [card("Card", kids, lift=True, layout_div_height="100%")]))
    return [
        page_hero("484:full", "Give", "Give with purpose",
                  "Giving is worship. Through your generosity, lives are changed and the mission of Bethel Church continues "
                  "to reach our community and beyond.",
                  "Faith in action"),
        section("2. Why We Give", [row("Content", [
            col("Text", [
                section_head("Why we give", "A heart of generosity"),
                text("We give because God has first given to us. Generosity is a reflection of our faith, gratitude and trust in Him. "
                     "Every gift supports ministry, outreach, discipleship and the ongoing work of sharing God's love with others."),
                buttons(button("Give Now", "#give-online")),
            ]),
            image_with_quote("483:full", "Giving at Bethel Church", "Live", "Generously",
                             "We give because God has given so much to us. Every gift helps bring hope, build faith and impact lives.",
                             "Bethel Church"),
        ])], bg=WHITE, anchor="why"),
        section("3. Ways to Give", [
            row("Heading", [col("Text", [section_head("Ways to give", "Simple ways to give")])], layout="100%"),
            row("Cards", ways, layout="33.33% 33.33% 33.33%", gap="24px", gap_row="24px", align="stretch",
                md_gap="20px", layout_row_margin="48px auto 0px auto", anchor="give-online"),
        ], bg=CREAM, anchor="ways"),
    ]


# =============================================================================
# Plugin pages (2 sections each)
# =============================================================================
def events():
    return [
        page_hero("464:full", "Events", "Upcoming events",
                  "Be part of what God is doing at Bethel Church. From special services to community gatherings, "
                  "there's always something happening for every season of life.",
                  "Join us"),
        section("2. Calendar (MEC shortcode)", [row("Content", [col("Calendar", [
            raw('[MEC id="446"]', "Calendar (MEC shortcode)")])], layout="100%")], bg=WHITE),
    ]


def watch():
    return [
        page_hero("492:full", "Watch", "Watch messages",
                  "Watch sermons, worship services and encouraging messages from Bethel Church anytime, anywhere. "
                  "Stay connected and grow in faith throughout the week.",
                  "Watch anytime"),
        section("2. Sermon Archive (shortcode)", [row("Content", [col("Archive", [
            raw('[smpro_archive per_page="15"]', "Sermon List (shortcode)")])], layout="100%")], bg=WHITE),
    ]


PAGES = {15: home, 463: about, 468: new_here, 467: ministries, 462: connect, 466: give, 441: events, 333: watch}
