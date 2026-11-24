"""Broadsheet renderer for the 23 November 2026 world-news front page.

Draws a newspaper front page on a 1024x1024 canvas with PIL only:
a masthead, a lead story with a stat panel, two featured sport stories,
an eight-story grid, and a two-column IN BRIEF strip.

All copy lives in the STORIES tables below. The picture is fully
deterministic: fixed fonts, fixed geometry, no network, no clock, so
two runs produce byte-identical PNGs.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT = W - 2 * MARGIN

PAPER = (246, 241, 231)
INK = (17, 17, 17)
MUTED = (96, 92, 84)
RULE = (17, 17, 17)
RED = (164, 30, 34)
GREEN = (30, 107, 52)
BLUE = (29, 78, 158)
PURPLE = (106, 63, 160)
TEAL = (13, 105, 105)

FONT_DIRS = [
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def find_font(names):
    """Return the first existing font file from a list of filenames."""
    for name in names:
        for d in FONT_DIRS:
            path = os.path.join(d, name)
            if os.path.exists(path):
                return path
    return None


def font(names, size):
    path = find_font(names)
    if path is None:
        return ImageFont.load_default(size)
    return ImageFont.truetype(path, size)


SERIF_BLACK = ["NotoSerif-Black.ttf", "DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"]
SERIF = ["NotoSerif-Bold.ttf", "DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"]
SERIF_REG = ["NotoSerif-Regular.ttf", "DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"]
SANS = ["LiberationSans-Regular.ttf", "DejaVuSans.ttf"]
SANS_BOLD = ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_tag(draw, x, y, label, fill):
    """Small coloured chip with white bold capitals; returns chip width."""
    fnt = font(SANS_BOLD, 12)
    tw = draw.textlength(label, font=fnt)
    pad_x, pad_y = 8, 3
    w = int(tw + 2 * pad_x)
    h = 18
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    draw.text((x + pad_x, y + pad_y), label, font=fnt, fill=(255, 255, 255))
    return w


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw stacked lines; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_spaced(draw, cx, y, text, fnt, fill=INK, tracking=6):
    """Centre text with extra letter spacing (used for the dateline)."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


# ---------------------------------------------------------------- stories

LEAD = {
    "tag": "CLIMATE",
    "colour": GREEN,
    "headline": "COP31 COLLAPSES: NO\nCLIMATE DEAL",
    "deck": "Talks in Antalya end without agreement after the EU and about "
            "130 nations reject a pact that omits fossil fuels.",
    "stat_big": "\u2248130",
    "stat_mid": "nations backed a\nfossil-fuel mention",
    "stat_year": "2009",
    "stat_note": "last summit collapse",
}

FEATURED = [
    {
        "tag": "CRICKET",
        "colour": TEAL,
        "headline": "India post a record 720/9 \u2014 then NZ hold on for a draw",
        "deck": "Rahul 136 and Pant 128 power the highest Test total ever on "
                "New Zealand soil; the first seven partnerships all pass 50 \u2014 "
                "a first in Test history. Mitchell and Phillips bat out 120 "
                "overs to save it.",
    },
    {
        "tag": "FORMULA 1",
        "colour": RED,
        "headline": "Verstappen wins a Las Vegas thriller",
        "deck": "Thirty-five lead changes and 352 overtakes on the Strip; the "
                "four-time champion beats Norris by 0.639s for his 75th win "
                "\u2014 his third in Vegas.",
    },
]

GRID = [
    {
        "tag": "CONFLICT",
        "colour": RED,
        "headline": "Russian strike north of Kyiv kills at least 11",
        "deck": "A boy of 7 was pulled alive from the rubble after 14 hours; "
                "a 79-year-old woman also survived.",
    },
    {
        "tag": "MARKETS",
        "colour": BLUE,
        "headline": "AI sell-off sweeps global markets",
        "deck": "Friday's rout: Nikkei -5.1%, S&P 500 -3.7%. On Monday, gold "
                "rebounded about 2% and Brent held near $92.",
    },
    {
        "tag": "JUSTICE",
        "colour": PURPLE,
        "headline": "'El Chapo Isidro' captured in Mexico",
        "deck": "FBI most-wanted fugitive Fausto Isidro Meza Flores was seized "
                "in Sinaloa; 11 died in the operation.",
    },
    {
        "tag": "POLITICS",
        "colour": BLUE,
        "headline": "Democrats win 258 House seats",
        "deck": "Their largest US House majority since 1992, sealed by a North "
                "Carolina win; 44 seats gained.",
    },
    {
        "tag": "SPORT",
        "colour": GREEN,
        "headline": "Alcaraz wins first ATP Finals title",
        "deck": "The Spaniard beat world No. 1 Zverev 6-2, 7-6 in Turin for "
                "his sixth title of 2026.",
    },
    {
        "tag": "CONFLICT",
        "colour": RED,
        "headline": "Children killed as drones strike Khartoum",
        "deck": "Strikes hit homes in Khartoum and Omdurman and damaged a UN "
                "building.",
    },
    {
        "tag": "POLITICS",
        "colour": TEAL,
        "headline": "Bolsonaro in intensive care in Brazil",
        "deck": "The ex-president, 71, is stable with an intestinal "
                "obstruction; doctors diagnosed pneumonia on Monday.",
    },
    {
        "tag": "CONFLICT",
        "colour": RED,
        "headline": "Ukraine sinks Russian warship off Libya",
        "deck": "Kyiv says naval drones sank a corvette off Benghazi \u2014 the "
                "naval war spreads overseas.",
    },
]

BRIEF_LEFT = [
    ("POLAND", "Three Russian missiles landed; NATO meets in emergency."),
    ("TECH", "Nvidia brings back Jensen Huang as CEO; shares fell ~23%."),
    ("GAZA", "Oxfam: war left a 'toxic wasteland' across 99% of the Strip."),
    ("YEMEN", "Houthis claim a Saudi refinery hit; Saudi jets strike back."),
]

BRIEF_RIGHT = [
    ("IRAN", "Trump: heaviest Iranian missile week in over a year."),
    ("TRAVEL", "Belgian airports shut; Delta outage delays 3,500+ flights."),
    ("INDONESIA", "Dozens missing after a candy factory fire kills 3."),
    ("TURKEY", "Istanbul rally against a media takeover."),
]

FOOTER = ("Sources: Reuters \u00b7 BBC \u00b7 AP \u00b7 CNN \u00b7 Oxfam \u00b7 "
          "US Dept. of Justice \u2014 Monday, 23 November 2026")


# ---------------------------------------------------------------- drawing

def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN

    # Masthead
    mast = font(SERIF_BLACK, 62)
    d.text((W / 2, 26), "WORLD NEWS", font=mast, fill=INK, anchor="ma")
    date_fnt = font(SANS, 17)
    draw_spaced(d, W / 2, 100, "MONDAY, 23 NOVEMBER 2026", date_fnt, INK, 7)
    d.line([(x0, 128), (x1, 128)], fill=RULE, width=3)
    d.line([(x0, 134), (x1, 134)], fill=RULE, width=1)

    # Lead story with stat panel on the right
    lead_y = 148
    draw_tag(d, x0, lead_y, LEAD["tag"], LEAD["colour"])
    head_fnt = font(SERIF_BLACK, 40)
    lead_lines = LEAD["headline"].split("\n")
    y = draw_lines(d, x0, lead_y + 26, lead_lines, head_fnt, INK, 48)
    deck_fnt = font(SANS, 15)
    deck_lines = wrap(d, LEAD["deck"], deck_fnt, 740)
    draw_lines(d, x0, y + 4, deck_lines, deck_fnt, INK, 19)

    px0, px1 = 812, x1
    d.rounded_rectangle([px0, lead_y, px1, lead_y + 148], radius=6,
                        outline=GREEN, width=2)
    big_fnt = font(SANS_BOLD, 40)
    d.text(((px0 + px1) / 2, lead_y + 8), LEAD["stat_big"], font=big_fnt,
           fill=GREEN, anchor="ma")
    mid_fnt = font(SANS, 13)
    my = draw_lines(d, px0 + 12, lead_y + 60,
                    LEAD["stat_mid"].split("\n"), mid_fnt, INK, 15)
    d.line([(px0 + 12, my + 4), (px1 - 12, my + 4)], fill=MUTED, width=1)
    yr_fnt = font(SANS_BOLD, 20)
    note_fnt = font(SANS, 12)
    d.text((px0 + 12, my + 10), LEAD["stat_year"], font=yr_fnt, fill=INK)
    yw = d.textlength(LEAD["stat_year"], font=yr_fnt)
    d.text((px0 + 18 + yw, my + 14), LEAD["stat_note"], font=note_fnt,
           fill=MUTED)

    d.line([(x0, 312), (x1, 312)], fill=RULE, width=1)

    # Featured row: two sport stories
    feat_y = 324
    col_w = (CONTENT - 24) // 2
    feat_head = font(SERIF_BLACK, 23)
    feat_deck = font(SANS, 13)
    for i, story in enumerate(FEATURED):
        cx = x0 + i * (col_w + 24)
        draw_tag(d, cx, feat_y, story["tag"], story["colour"])
        lines = wrap(d, story["headline"], feat_head, col_w)
        y = draw_lines(d, cx, feat_y + 26, lines, feat_head, INK, 27)
        deck = wrap(d, story["deck"], feat_deck, col_w)
        draw_lines(d, cx, y + 3, deck, feat_deck, INK, 16)

    d.line([(x0, 458), (x1, 458)], fill=RULE, width=1)

    # Eight-story grid, four rows of two
    grid_y = 470
    row_h = 98
    grid_head = font(SERIF_BLACK, 19)
    grid_deck = font(SANS, 12)
    for i, story in enumerate(GRID):
        row, col = divmod(i, 2)
        cx = x0 + col * (col_w + 24)
        cy = grid_y + row * row_h
        draw_tag(d, cx, cy, story["tag"], story["colour"])
        lines = wrap(d, story["headline"], grid_head, col_w)[:2]
        y = draw_lines(d, cx, cy + 25, lines, grid_head, INK, 22)
        deck = wrap(d, story["deck"], grid_deck, col_w)[:2]
        draw_lines(d, cx, y + 2, deck, grid_deck, INK, 15)

    d.line([(x0, 874), (x1, 874)], fill=RULE, width=1)

    # IN BRIEF strip, two columns of one-liners
    brief_y = 886
    brief_head = font(SANS_BOLD, 14)
    d.text((x0, brief_y), "IN BRIEF", font=brief_head, fill=INK)
    d.line([(x0 + 92, brief_y + 8), (x1, brief_y + 8)], fill=RULE, width=1)
    brief_fnt = font(SANS, 12)
    brief_bold = font(SANS_BOLD, 12)
    item_y = brief_y + 24
    for col_items in (BRIEF_LEFT, BRIEF_RIGHT):
        cx = x0 + (0 if col_items is BRIEF_LEFT else col_w + 24)
        y = item_y
        for label, text in col_items:
            lab = label + " \u2014 "
            d.text((cx, y), lab, font=brief_bold, fill=INK)
            lw = d.textlength(lab, font=brief_bold)
            d.text((cx + lw, y), text, font=brief_fnt, fill=INK)
            y += 17

    # Footer
    foot_fnt = font(SANS, 12)
    d.text((W / 2, 996), FOOTER, font=foot_fnt, fill=MUTED, anchor="ma")

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out)
