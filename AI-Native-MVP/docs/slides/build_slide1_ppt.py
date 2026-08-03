"""Generate Slide 1 PowerPoint — Blinkit's Market Landscape."""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent / "slide1-blinkit-market-landscape.pptx"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Margins (match HTML padding 44px / 32px / 24px at 1920×1080)
MARGIN_L = Inches(0.31)
MARGIN_R = Inches(0.31)
MARGIN_T = Inches(0.22)
MARGIN_B = Inches(0.17)
COL_GAP = Inches(0.14)

RED = RGBColor(196, 30, 58)
DARK = RGBColor(26, 26, 26)
GRAY = RGBColor(102, 102, 102)
WHITE = RGBColor(255, 255, 255)
BLUE = RGBColor(37, 99, 235)
PINK_BG = RGBColor(252, 232, 236)
PINK_DARK = RGBColor(139, 21, 56)
LIGHT_BLUE = RGBColor(219, 234, 254)
LIGHT_GRAY = RGBColor(229, 229, 229)
BOX_BG = RGBColor(250, 250, 250)
BOX_BORDER = RGBColor(221, 221, 221)
TENSION_BG = RGBColor(45, 45, 45)
LIGHT_TEXT = RGBColor(232, 232, 232)

CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R
COL_W = (CONTENT_W - COL_GAP) / 2
LEFT_X = MARGIN_L
RIGHT_X = MARGIN_L + COL_W + COL_GAP

FOOTER_H = Inches(0.72)
FOOTER_Y = SLIDE_H - MARGIN_B - FOOTER_H
MAIN_TOP = Inches(1.02)
MAIN_BOTTOM = FOOTER_Y - Inches(0.08)

SOURCES = {
    "Datum Intelligence": "https://reports.datumintell.in/reports/Consumer-insights/quick-commerce/quick-commerce-india-2024.html",
    "Redseer digest": "https://redseer.com/digests/quick-commerce-india-scale-dark-stores-growth/",
    "Blinkit annual return": "https://blinkit.com/annual-return",
    "Business Today": "https://www.businesstoday.in/latest/corporate/story/zomato-results-blinkits-expansion-outside-traditional-grocery-segments-next-target-2000-dark-stores-by-2026-says-ceo-dhindsa-zomato-online-food-delivery-major-announced-a-substantial-growth-in-its-439757-2024-08-01",
    "Redseer 2026": "https://redseer.com/articles/quick-commerce-finds-its-new-normal-with-scale-mix-and-momentum/",
    "Business Standard": "https://www.business-standard.com/companies/news/beyond-expansion-quick-commerce-seeks-more-growth-from-existing-assets-126080200252_1.html",
    "NDTV / NIQ": "https://www.ndtv.com/india-news/31-of-urban-indians-now-use-quick-commerce-for-grocery-survey-6645339",
    "Financial Express": "https://www.financialexpress.com/business/industry-category-expansion-for-q-commerce-firms-may-be-slow-3586885/",
}


def set_slide_size(prs: Presentation) -> None:
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H


def add_rect(slide, left, top, width, height, fill_rgb, line_rgb=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if line_rgb:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(0.75)
    else:
        shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text, font_size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(0)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    p.space_after = Pt(0)
    p.line_spacing = 1.15
    return box


def add_run(p, text, *, size=14, bold=False, color=DARK, link=None, underline=False):
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.underline = underline
    if link:
        run.hyperlink.address = link
    return run


def add_box(slide, left, top, width, height, fill=BOX_BG, border=BOX_BORDER):
    return add_rect(slide, left, top, width, height, fill, border)


def add_stat_card(slide, left, top, w, h, num, label, num_color):
    add_box(slide, left, top, w, h, WHITE, RGBColor(204, 204, 204))
    pad = Inches(0.06)
    add_textbox(slide, left, top + pad, w, Inches(0.42), num, 32, True, num_color, PP_ALIGN.CENTER)
    add_textbox(slide, left + pad, top + Inches(0.46), w - 2 * pad, h - Inches(0.52), label, 14, False, GRAY, PP_ALIGN.CENTER)


def add_funnel_tier(slide, left, top, width, title, body, fill, text_color=DARK, tier_h=Inches(0.46)):
    add_rect(slide, left, top, width, tier_h, fill, RGBColor(187, 187, 187))
    inner = Inches(0.06)
    add_textbox(slide, left + inner, top + Inches(0.03), width - 2 * inner, Inches(0.18), title, 14, True, text_color, PP_ALIGN.CENTER)
    add_textbox(slide, left + inner, top + Inches(0.2), width - 2 * inner, tier_h - Inches(0.22), body, 14, False, text_color, PP_ALIGN.CENTER)


def add_footer(slide):
    add_rect(slide, MARGIN_L, FOOTER_Y - Inches(0.06), CONTENT_W, Pt(0.75), WHITE, BOX_BORDER)

    box = slide.shapes.add_textbox(MARGIN_L, FOOTER_Y, CONTENT_W, FOOTER_H)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(0)

    p1 = tf.paragraphs[0]
    p1.line_spacing = 1.2
    add_run(p1, "Sources: ", size=14, bold=True, color=GRAY)
    add_run(p1, "[1] ", size=14, color=GRAY)
    add_run(p1, "Datum Intelligence", size=14, color=BLUE, link=SOURCES["Datum Intelligence"], underline=True)
    add_run(p1, " · [2] ", size=14, color=GRAY)
    add_run(p1, "Redseer digest", size=14, color=BLUE, link=SOURCES["Redseer digest"], underline=True)
    add_run(p1, " · [3] ", size=14, color=GRAY)
    add_run(p1, "Blinkit annual return", size=14, color=BLUE, link=SOURCES["Blinkit annual return"], underline=True)
    add_run(p1, " · [4] ", size=14, color=GRAY)
    add_run(p1, "Business Today", size=14, color=BLUE, link=SOURCES["Business Today"], underline=True)

    p2 = tf.add_paragraph()
    p2.line_spacing = 1.2
    add_run(p2, "[5] ", size=14, color=GRAY)
    add_run(p2, "Redseer 2026", size=14, color=BLUE, link=SOURCES["Redseer 2026"], underline=True)
    add_run(p2, " · [6] ", size=14, color=GRAY)
    add_run(p2, "Business Standard", size=14, color=BLUE, link=SOURCES["Business Standard"], underline=True)
    add_run(p2, " · [7] ", size=14, color=GRAY)
    add_run(p2, "NDTV / NIQ", size=14, color=BLUE, link=SOURCES["NDTV / NIQ"], underline=True)
    add_run(p2, " · [8] ", size=14, color=GRAY)
    add_run(p2, "Financial Express", size=14, color=BLUE, link=SOURCES["Financial Express"], underline=True)


def build() -> None:
    prs = Presentation()
    set_slide_size(prs)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    pad = Inches(0.1)

    # Header
    add_rect(slide, MARGIN_L, MARGIN_T + Inches(0.04), Inches(0.06), Inches(0.52), RED)
    add_textbox(slide, MARGIN_L + Inches(0.14), MARGIN_T, Inches(9), Inches(0.46), "Blinkit's Market Landscape", 36, True, DARK)
    add_textbox(slide, MARGIN_L + Inches(0.14), MARGIN_T + Inches(0.46), Inches(9), Inches(0.28), "Quick commerce · Growth team · Cross-category MAC", 16, False, GRAY)

    box_gap = Inches(0.07)

    # ── LEFT COLUMN ──────────────────────────────────────────────
    y = MAIN_TOP

    h1 = Inches(1.48)
    add_box(slide, LEFT_X, y, COL_W, h1)
    add_textbox(slide, LEFT_X + pad, y + Inches(0.06), COL_W - 2 * pad, Inches(0.22), "WHAT QUICK COMMERCE IS NOW [1][2]", 18, True, DARK)
    add_textbox(
        slide, LEFT_X + pad, y + Inches(0.28), COL_W - 2 * pad, h1 - Inches(0.34),
        "Indian QC has moved from emergency top-up to weekly habit — 10–15 min delivery. "
        "Assortment spans electronics, beauty, baby care, pharma.\n\n"
        "Blinkit positions as \"beyond grocery\" — filings cite cosmetics, mobiles, electronics, baby care, bakery. [3][4]",
        14,
    )

    y += h1 + box_gap
    h2 = Inches(2.18)
    add_box(slide, LEFT_X, y, COL_W, h2)
    add_textbox(slide, LEFT_X + pad, y + Inches(0.06), COL_W - 2 * pad, Inches(0.22), "THE GROWTH REALITY [1][5][6][7][8]", 18, True, DARK)
    bullets = (
        "• 53% place 5+ orders/mo; 26% place 10+; 63% order weekly [1]\n"
        "• 79% grocery · 42% beauty; NIQ: 31% primary grocery · 42% RTE [1][7]\n"
        "• Non-grocery ~1.6× faster than grocery (Redseer 2026) [5]\n"
        "• ~₹11,000 cr monthly GMV — growth from breadth [5][6]\n"
        "• Trust gaps: stockouts, returns, quality, CS [8]"
    )
    add_textbox(slide, LEFT_X + pad, y + Inches(0.28), COL_W - 2 * pad, h2 - Inches(0.34), bullets, 14)

    y += h2 + box_gap
    h3 = Inches(0.92)
    add_box(slide, LEFT_X, y, COL_W, h3, PINK_BG, RGBColor(240, 196, 204))
    add_textbox(slide, LEFT_X + pad, y + Inches(0.06), COL_W - 2 * pad, Inches(0.2), "THE GOAL", 18, True, PINK_DARK)
    add_textbox(
        slide, LEFT_X + pad, y + Inches(0.26), COL_W - 2 * pad, h3 - Inches(0.32),
        "North star: ↑ % MACs buying ≥1 new non-grocery category / month.\n"
        "Measure: new-category MAC · repeat rate · non-grocery share.",
        14,
    )

    # ── RIGHT COLUMN ─────────────────────────────────────────────
    ry = MAIN_TOP
    sw = (COL_W - Inches(0.08)) / 2
    sh = Inches(0.82)
    sg = Inches(0.08)

    add_stat_card(slide, RIGHT_X, ry, sw, sh, "53%", "5+ orders/month", RED)
    add_stat_card(slide, RIGHT_X + sw + sg, ry, sw, sh, "1.6×", "Non-grocery vs grocery", RED)
    add_stat_card(slide, RIGHT_X, ry + sh + sg, sw, sh, "₹11K cr", "Monthly QC GMV", DARK)
    add_stat_card(slide, RIGHT_X + sw + sg, ry + sh + sg, sw, sh, "42%", "QC ready-to-eat buyers", BLUE)

    ty = ry + 2 * sh + sg + Inches(0.06)
    th = Inches(1.92)
    callout_h = Inches(0.38)
    callout_y = ty + th - callout_h - Inches(0.08)
    add_rect(slide, RIGHT_X, ty, COL_W, th, TENSION_BG)
    add_textbox(slide, RIGHT_X + pad, ty + Inches(0.06), COL_W - 2 * pad, Inches(0.22), "ECOSYSTEM & CENTRAL TENSION", 18, True, WHITE)
    eco = (
        "QC platforms → Higher AOV via non-grocery\n"
        "Brands / D2C → Channel beyond Amazon / Nykaa\n"
        "Grocery-regular users → Speed for daily needs\n"
        "Considered buyers → Trust before repeat\n\n"
        "Industry expanded catalog breadth faster than repeat confidence. [5][8]"
    )
    eco_h = callout_y - (ty + Inches(0.28)) - Inches(0.04)
    add_textbox(slide, RIGHT_X + pad, ty + Inches(0.28), COL_W - 2 * pad, eco_h, eco, 14, False, LIGHT_TEXT)

    add_rect(slide, RIGHT_X + pad, callout_y, COL_W - 2 * pad, callout_h, RED)
    add_textbox(
        slide, RIGHT_X + pad + Inches(0.04), callout_y + Inches(0.06), COL_W - 2 * pad - Inches(0.08), callout_h - Inches(0.1),
        "Gap: catalog breadth vs. repeat confidence — not catalog size.",
        14, True, WHITE, PP_ALIGN.CENTER,
    )

    fy = ty + th + Inches(0.07)
    tier_h = Inches(0.44)
    fw = COL_W
    add_funnel_tier(slide, RIGHT_X, fy, fw, "TAM — Habitual QC users", "~26M+ · 53% order 5+/month [1][2]", LIGHT_GRAY, tier_h=tier_h)
    sam_w = fw * 0.88
    add_funnel_tier(slide, RIGHT_X + (fw - sam_w) / 2, fy + tier_h, sam_w, "SAM — Multi-category basket", "42% RTE · 42% beauty [1][7]", LIGHT_BLUE, tier_h=tier_h)
    som_w = fw * 0.76
    add_funnel_tier(slide, RIGHT_X + (fw - som_w) / 2, fy + 2 * tier_h, som_w, "SOM — Cross-category MAC", "↑ % MAC with ≥1 new non-grocery category / mo", PINK_BG, PINK_DARK, tier_h=tier_h)

    add_footer(slide)

    prs.save(OUT)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    build()
