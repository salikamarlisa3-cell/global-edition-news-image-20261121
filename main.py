#!/usr/bin/env python3
"""The Global Edition — world news poster for Saturday 21 November 2026.

Fresh generator written for the news-image-20261121 entry. Pure Python
standard library + Pillow. Deterministic: same input -> byte-identical PNG.

Layout (1024x1024): masthead, 3 lead panels, dot-matrix world map with 7
numbered region pins + region key, 13 illustrated feature tiles, 56 numbered
stories in 7 region blocks (8 each), UTC timeline, by-the-numbers strip,
weather strip, footer. Every story was published or reported on 21 Nov 2026;
outlets are cited on the poster and full verification URLs live in SOURCES.md.
"""
import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
MUTED = (90, 88, 80)
PANEL = (255, 255, 255)
PANEL_EDGE = (205, 200, 185)
BLACK = (16, 16, 16)
WHITE = (255, 255, 255)
DOT = (44, 62, 80)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# (number, headline, outlet) — 8 per region, numbered 1..56.
REGIONS = [
    ("NORTH AMERICA", (192, 57, 43), [
        (1, "Mamdani unveils plan to close NYC's Rikers Island jail by 2032", "BBC"),
        (2, "Trump urges Nvidia to reinstate 'brilliant' Jensen Huang", "Al Jazeera"),
        (3, "Man who sparked deadly LA wildfire found guilty", "Guardian"),
        (4, "Trump turns press conference into 2028 succession audition", "Guardian"),
        (5, "Court: House unconstitutionally passed 2022 $1.7tn spending bill", "Reuters"),
        (6, "Senator blocks Trump cyber nominee over Jan 6 denial", "Guardian"),
        (7, "Trump: US flight systems 'ancient' but 'safe' after ground stop", "BBC"),
        (8, "Pair fined $811m for conning detained migrants \u2014 scams went on", "BBC"),
    ]),
    ("LATIN AMERICA", (230, 126, 34), [
        (9, "Two Salvadoran soldiers killed in Haiti explosives accident", "Al Jazeera"),
        (10, "Bukele registers bid for third term as El Salvador president", "AP"),
        (11, "Bolsonaro taken to hospital with severe abdominal pain", "Rio Times"),
        (12, "Mexico approves ballot for 2027 midterm election", "Rio Times"),
        (13, "Thousands protest Colombia tax plans amid US troops row", "Al Jazeera"),
        (14, "Lula visits ailing Chief Raoni as Brazil recognises Indigenous land", "Al Jazeera"),
        (15, "Trump: close to Mexico deal; more work to do with Canada", "Times of India"),
        (16, "Paraguay president impeached after Ueno Bank collapse", "Global Voice"),
    ]),
    ("EUROPE", (46, 95, 163), [
        (17, "Denmark expels Russian diplomat over 'plot to kill Ukrainian rapper'", "Al Jazeera"),
        (18, "NI health: further doctors' strike planned in pay dispute", "BBC"),
        (19, "French officers guilty of racist assault on producer Michel Zecler", "Guardian"),
        (20, "Kryvyi Rih strike: two dead, 42 injured, children among hurt", "AppiSToS"),
        (21, "UK and EU agree reset: food trade and youth mobility deals", "BBC"),
        (22, "Russia decries 'new Iron Curtain' as Estonia shuts borders", "Al Jazeera"),
        (23, "Belgrade mayor charged with assaulting opposition politician", "Al Jazeera"),
        (24, "Depardieu and French author investigated over sexual allegations", "BBC"),
    ]),
    ("MIDDLE EAST", (125, 60, 152), [
        (25, "Saudi coalition downs Houthi missiles fired at Riyadh", "Al Jazeera"),
        (26, "Iraq PM targets militia stronghold to assert state control", "Al Jazeera"),
        (27, "Fossil-fuel deadlock pushes COP31 summit into overtime", "Al Jazeera"),
        (28, "Israeli drone attacks kill seven Palestinians in central Gaza", "Al Jazeera"),
        (29, "Gaza's displaced children celebrate World Children's Day", "Al Jazeera"),
        (30, "Melania Trump calls for 'peace' for children of Gaza and Israel", "Variety"),
        (31, "US adds four Iranians to OFAC sanctions list over oil revenues", "AppiSToS"),
        (32, "Kataib Hezbollah faces deadline to quit Iraqi stronghold", "Al Jazeera"),
    ]),
    ("AFRICA", (166, 124, 0), [
        (33, "ANC fights to keep control of South Africa's key cities", "BBC"),
        (34, "Somalia orders UAE ambassador out in sovereignty row", "Benin Web TV"),
        (35, "Boat of mourners capsizes in Nigeria; at least four dead", "Al Jazeera"),
        (36, "581 women murdered in South Africa in three months", "EIN / Xinhua"),
        (37, "Sudan war leaves disabled children out of education", "Al Jazeera"),
        (38, "Ebola workers in DR Congo plan strike from today over unpaid wages", "Rio Times"),
        (39, "Congo offensive displaces 323,000 in South Kivu in four days", "Peter's World"),
        (40, "South Sudan candidate survives arrest attempt by gunmen in Juba", "21 Nov digest"),
    ]),
    ("ASIA", (20, 143, 119), [
        (41, "IndusInd Bank sacks ex-CEO Kathpalia, seeks to claw back pay", "Reuters"),
        (42, "South Korea tops UN e-government index for first time", "21 Nov digest"),
        (43, "Myanmar calls ICJ genocide ruling 'unfair'", "The Hindu"),
        (44, "Malaysia plans to resettle 10,000 Rohingya in Turkiye", "The Hindu"),
        (45, "Indian man jailed 19 years over plot to kill Sikh separatist in US", "Al Jazeera"),
        (46, "Nepal PM Balendra Shah to meet Modi on first trip abroad", "BBC"),
        (47, "Rahul Gandhi backs strong India\u2013Israel ties despite Gaza war", "Al Jazeera"),
        (48, "South Korea catches 111 students in exam-cheating crackdown", "BBC"),
    ]),
    ("OCEANIA", (30, 132, 73), [
        (49, "Victorian Greens seek injunction over copycat how-to-vote cards", "Guardian"),
        (50, "Australia's new insurance rules may upend home births", "Guardian"),
        (51, "A day with Padre Dave, the outback's flying minister", "Guardian"),
        (52, "Farmers warned: pay up or risk losing drivers licences", "ABC"),
        (53, "Dodgy visa scheme put NSW premier's secret partner behind bars", "ABC"),
        (54, "Citizen scientists hunt for bugs in Australia's backyards", "ABC"),
        (55, "Bougainville landowners 'overwhelmed' at Rio Tinto $370m pledge", "ABC"),
        (56, "Young Aussies stun Argentina at under-17 World Cup", "ABC"),
    ]),
]

LEADS = [
    # (story no., kicker, headline, deck, icon)
    (25, "LEAD 1 \u00b7 MIDDLE EAST \u00b7 AL JAZEERA",
     "Houthi missiles fired at Riyadh \u2014 Saudi coalition intercepts three",
     "Fresh wave of attacks on the Saudi capital as the Iran war escalates.",
     "missile"),
    (17, "LEAD 2 \u00b7 EUROPE \u00b7 AL JAZEERA",
     "Denmark expels Russian diplomat over 'plot to kill Ukrainian rapper'",
     "Copenhagen accuses Moscow of planning the killing with a banned gang.",
     "passport"),
    (1, "LEAD 3 \u00b7 NORTH AMERICA \u00b7 BBC",
     "Mamdani unveils plan to close Rikers Island jail by 2032",
     "Shuttering the troubled jail was first voted for in 2019; delays followed.",
     "jail"),
]

# 13 feature tiles: (story no., caption, icon) — with the 3 leads = 16 panels.
TILES = [
    (26, "IRAQ: MILITIA STANDOFF", "dome"),
    (27, "COP31 IN OVERTIME", "sun"),
    (33, "SOUTH AFRICA VOTES", "ballot"),
    (34, "SOMALIA EXPELS ENVOY", "plane"),
    (10, "BUKELE: THIRD TERM", "ballot"),
    (11, "BOLSONARO IN HOSPITAL", "cross"),
    (21, "UK\u2013EU RESET DEAL", "scales"),
    (20, "KRYVYI RIH HIT", "missile"),
    (41, "INDUSIND SACKS EX-CEO", "bank"),
    (49, "VICTORIA: VOTE ROW", "ballot"),
    (35, "NIGERIA BOAT TRAGEDY", "boat"),
    (45, "19 YEARS: SIKH PLOT", "gavel"),
    (5, "SPENDING BILL VOID", "gavel"),
]

TIMELINE = [
    ("00:00", "Houthi missiles intercepted over Riyadh"),
    ("00:01", "Mamdani unveils Rikers closure plan"),
    ("00:34", "ANC battles to hold South Africa's big cities"),
    ("02:00", "Iraq PM moves on militia stronghold"),
    ("02:27", "Kryvyi Rih toll: 2 dead, 42 injured"),
    ("03:34", "US sanctions four Iranians over oil cash"),
]

NUMBERS = [
    ("$7.25bn", "Bayer Roundup settlement approved by US judge"),
    ("581", "women murdered in South Africa, Jul\u2013Sep 2026"),
    ("323,000", "people fled South Kivu fighting in four days"),
    ("1,000", "long-range drones UK will send Ukraine (\u00a3260m)"),
    ("10,000", "Rohingya Malaysia plans to resettle in Turkiye"),
    ("111", "students caught in South Korea exam crackdown"),
]

# Day highs / lows for 21 Nov 2026, Open-Meteo forecast.
WEATHER = [
    ("NEW YORK", "18\u00b0", "6\u00b0"),
    ("MEXICO CITY", "23\u00b0", "22\u00b0"),
    ("LONDON", "10\u00b0", "7\u00b0"),
    ("RIYADH", "30\u00b0", "19\u00b0"),
    ("JOHANNESBURG", "27\u00b0", "16\u00b0"),
    ("NEW DELHI", "24\u00b0", "15\u00b0"),
    ("SYDNEY", "27\u00b0", "18\u00b0"),
]

LEFT_OUT = [
    "ICJ Rohingya genocide ruling (19 Nov) \u2014 led yesterday's edition; Myanmar's reply is story #43.",
    "Trump\u2013Xi\u2013Putin 'peace declaration' (19\u201320 Nov) \u2014 led yesterday's edition.",
    "Anthropic's $81.3bn IPO debut (20 Nov) \u2014 led yesterday's edition; day-2 slide: Nasdaq erased all 2026 gains.",
    "GTA 6's $3.79bn first-day sales (20 Nov) \u2014 entertainment, tracked by our GTA6 watch, not world news.",
    "COP31 draft with no fossil fuels (20 Nov) \u2014 superseded by today's overtime deadlock, story #27.",
]

# Region pin positions on the map (lon, lat) and story-number ranges.
PINS = [
    (1, -74, 41),    # North America
    (2, -58, -15),   # Latin America
    (3, 10, 50),     # Europe
    (4, 47, 25),     # Middle East
    (5, 20, 0),      # Africa
    (6, 100, 25),    # Asia
    (7, 150, -27),   # Oceania
]

# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def panel(draw, x, y, w, h, fill=PANEL):
    rrect(draw, [x, y, x + w, y + h], 4, fill=fill, outline=PANEL_EDGE, width=1)


def dark(c, f=0.72):
    return tuple(int(v * f) for v in c)



def tint(c, amt=0.88):
    """Mix colour toward white; amt=1 keeps colour."""
    return tuple(int(v * amt + 255 * (1 - amt)) for v in c)


# ---------------------------------------------------------------- map
# Land approximated by ellipses in (lon, lat) space — a stylised dot map.
LAND = [
    # North America
    (-125, 62, 35, 12), (-85, 55, 20, 10), (-100, 40, 22, 8),
    (-102, 22, 10, 5), (-86, 13, 8, 3), (-42, 74, 10, 5),
    # South America
    (-60, -5, 18, 12), (-62, -25, 12, 12), (-70, -35, 6, 10),
    # Europe
    (10, 55, 15, 8), (15, 45, 12, 6), (30, 60, 15, 8), (22, 42, 6, 4),
    (-2, 54, 5, 5), (20, 68, 12, 6),
    # Africa
    (10, 15, 18, 12), (20, 0, 12, 10), (25, -15, 10, 10),
    (40, 5, 8, 8), (48, 10, 5, 5),
    # Middle East / Asia
    (45, 30, 10, 7), (55, 32, 10, 6), (60, 65, 25, 10),
    (100, 62, 35, 10), (115, 50, 15, 8), (78, 22, 8, 8),
    (101, 15, 7, 7), (105, 35, 8, 8), (122, 30, 6, 6),
    (139, 37, 4, 6), (127, 40, 4, 4), (100, 5, 5, 4),
    (135, -5, 8, 5), (113, -3, 6, 4), (120, 0, 4, 5),
    # Oceania
    (134, -25, 14, 8), (146, -39, 4, 4), (172, -41, 4, 5),
]


def is_land(lon, lat):
    for cx, cy, rx, ry in LAND:
        if ((lon - cx) / rx) ** 2 + ((lat - cy) / ry) ** 2 <= 1.0:
            return True
    return False


def draw_map(draw, x, y, w, h):
    """Dot-matrix world map; returns lon/lat -> pixel mapper."""
    lon0, lon1, lat0, lat1 = -170.0, 190.0, 75.0, -55.0
    cols, rows = 102, 26
    cw, chh = w / cols, h / rows

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for r in range(rows):
        lat = lat0 - (r + 0.5) * (lat0 - lat1) / rows
        for c in range(cols):
            lon = lon0 + (c + 0.5) * (lon1 - lon0) / cols
            if is_land(lon, lat):
                px = x + (c + 0.5) * cw
                py = y + (r + 0.5) * chh
                draw.ellipse([px - 2.1, py - 2.1, px + 2.1, py + 2.1], fill=DOT)
    return proj


# ---------------------------------------------------------------- icons
def icon(draw, kind, x, y, w, h, color):
    """Flat pictogram inside box (x, y, w, h)."""
    cx, cy = x + w / 2, y + h / 2
    if kind == "missile":
        draw.line([x + 4, y + h - 4, x + w - 8, y + 6], fill=color, width=5)
        draw.polygon([(x + w - 8, y + 6), (x + w - 2, y + 12), (x + w - 14, y + 14)],
                     fill=color)
        draw.line([x + 2, y + h - 10, x + 12, y + h - 2], fill=color, width=2)
        draw.line([x + 8, y + h - 2, x + 16, y + h - 12], fill=color, width=2)
    elif kind == "passport":
        rrect(draw, [x + 6, y + 2, x + w - 6, y + h - 2], 2, fill=color)
        draw.rectangle([x + 10, y + 6, x + w - 10, y + 10], fill=WHITE)
        draw.line([x + 10, y + 14, x + w - 10, y + 14], fill=WHITE, width=2)
        draw.line([x + 10, y + 19, x + w - 16, y + 19], fill=WHITE, width=2)
        draw.line([x + w - 4, y + h - 12, x + w + 4, y + h - 4], fill=(192, 57, 43), width=4)
        draw.line([x + w + 4, y + h - 12, x + w - 4, y + h - 4], fill=(192, 57, 43), width=4)
    elif kind == "jail":
        for i in range(5):
            bx = x + 4 + i * (w - 8) / 4
            draw.line([bx, y + 2, bx, y + h - 2], fill=color, width=3)
        draw.line([x + 2, y + 2, x + w - 2, y + 2], fill=color, width=3)
        draw.line([x + 2, y + h - 2, x + w - 2, y + h - 2], fill=color, width=3)
    elif kind == "dome":
        draw.polygon([(cx, y + 2), (x + 4, y + h - 12), (x + w - 4, y + h - 12)], fill=color)
        draw.rectangle([x + 4, y + h - 12, x + w - 4, y + h - 6], fill=color)
        for i in range(3):
            bx = x + 8 + i * (w - 16) / 2
            draw.line([bx, y + h - 6, bx, y + h - 1], fill=color, width=3)
    elif kind == "sun":
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=color)
        for a in range(0, 360, 45):
            import math
            r1, r2 = 11, 15
            x1 = cx + r1 * math.cos(math.radians(a))
            y1 = cy + r1 * math.sin(math.radians(a))
            x2 = cx + r2 * math.cos(math.radians(a))
            y2 = cy + r2 * math.sin(math.radians(a))
            draw.line([x1, y1, x2, y2], fill=color, width=2)
    elif kind == "ballot":
        rrect(draw, [x + 4, y + 8, x + w - 4, y + h - 2], 2, fill=color)
        draw.rectangle([x + w / 2 - 8, y + 5, x + w / 2 + 8, y + 9], fill=WHITE)
        draw.polygon([(cx - 3, y + 2), (cx + 3, y + 2), (cx, y + 7)], fill=(192, 57, 43))
        draw.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=WHITE, width=2)
    elif kind == "plane":
        draw.polygon([(x + 2, cy), (x + w - 2, cy - 6), (x + w - 2, cy + 6)], fill=color)
        draw.polygon([(cx, cy - 4), (cx + 10, cy - 14), (cx + 14, cy - 4)], fill=color)
        draw.polygon([(cx, cy + 4), (cx + 10, cy + 14), (cx + 14, cy + 4)], fill=color)
    elif kind == "cross":
        draw.rectangle([cx - 4, y + 3, cx + 4, y + h - 3], fill=color)
        draw.rectangle([x + 3, cy - 4, x + w - 3, cy + 4], fill=color)
    elif kind == "scales":
        draw.line([cx, y + 2, cx, y + h - 4], fill=color, width=3)
        draw.line([x + 4, y + 6, x + w - 4, y + 6], fill=color, width=3)
        draw.polygon([(x + 2, y + 8), (x + 12, y + 8), (x + 7, y + 18)], fill=color)
        draw.polygon([(x + w - 12, y + 8), (x + w - 2, y + 8), (x + w - 7, y + 18)], fill=color)
        draw.line([x + 2, y + h - 2, x + w - 2, y + h - 2], fill=color, width=3)
    elif kind == "bank":
        draw.polygon([(x + 2, y + 10), (cx, y + 2), (x + w - 2, y + 10)], fill=color)
        for i in range(4):
            bx = x + 5 + i * (w - 10) / 3
            draw.line([bx, y + 13, bx, y + h - 5], fill=color, width=3)
        draw.rectangle([x + 2, y + h - 4, x + w - 2, y + h - 1], fill=color)
    elif kind == "boat":
        draw.polygon([(x + 3, y + h - 10), (x + w - 3, y + h - 10),
                      (x + w - 8, y + h - 2), (x + 8, y + h - 2)], fill=color)
        draw.line([cx, y + 2, cx, y + h - 10], fill=color, width=3)
        draw.polygon([(cx, y + 3), (cx + 12, y + 14), (cx, y + 14)], fill=color)
    elif kind == "gavel":
        draw.line([x + 4, y + h - 6, x + w - 8, y + 8], fill=color, width=4)
        draw.rectangle([x + w - 16, y + 2, x + w - 2, y + 12], fill=color)
        draw.line([x + 2, y + h - 2, x + 14, y + h - 2], fill=color, width=3)

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_mast = font(F_BOLD, 27)
    f_sub = font(F_REG, 11)
    f_sub_b = font(F_BOLD, 11)
    f_tiny = font(F_REG, 8)
    f_tiny_b = font(F_BOLD, 8)
    f_lead_h = font(F_BOLD, 13)
    f_lead_d = font(F_REG, 9)
    f_kick = font(F_BOLD, 8)
    f_blk_h = font(F_BOLD, 10)
    f_brief = font(F_REG, 9)
    f_brief_b = font(F_BOLD, 9)
    f_num = font(F_BOLD, 16)
    f_cap = font(F_BOLD, 7)
    f_time = font(F_BOLD, 10)
    f_lab = font(F_REG, 8)

    # ---- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 56], fill=BLACK)
    d.text((10, 6), "THE GLOBAL EDITION", font=f_mast, fill=WHITE)
    d.text((10, 38), "SATURDAY 21 NOVEMBER 2026  \u00b7  THE WORLD IN ONE IMAGE",
           font=f_sub, fill=(210, 205, 190))
    right1 = "56 STORIES  \u00b7  7 REGIONS  \u00b7  16 PANELS"
    d.text((W - 10 - d.textlength(right1, font=f_sub_b), 8), right1,
           font=f_sub_b, fill=(255, 214, 90))
    right2 = "make.fun  \u00b7  news-image-20261121  \u00b7  @salikamarlisa3-cell"
    d.text((W - 10 - d.textlength(right2, font=f_tiny), 38), right2,
           font=f_tiny, fill=(190, 185, 172))

    # ---- 3 lead panels --------------------------------------------
    lead_y, lead_h, lead_w, gap = 62, 130, 330, 9
    for i, (no, kicker, head, deck, ic) in enumerate(LEADS):
        x = 6 + i * (lead_w + gap)
        region = REGIONS[[r[0] for r in REGIONS].index(
            "MIDDLE EAST" if i == 0 else "EUROPE" if i == 1 else "NORTH AMERICA")]
        color = region[1]
        panel(d, x, lead_y, lead_w, lead_h)
        d.rectangle([x, lead_y, x + lead_w, lead_y + 17], fill=color)
        d.text((x + 8, lead_y + 4), kicker, font=f_kick, fill=WHITE)
        d.text((x + lead_w - 26, lead_y + 3), f"#{no}", font=f_lead_h, fill=WHITE)
        icon(d, ic, x + lead_w - 66, lead_y + 24, 56, 40, tint(color, 0.55))
        lines = wrap_text(d, head, f_lead_h, lead_w - 80)
        ly = lead_y + 24
        for ln in lines[:3]:
            d.text((x + 8, ly), ln, font=f_lead_h, fill=INK)
            ly += 15
        deck_lines = wrap_text(d, deck, f_lead_d, lead_w - 16)
        dy = lead_y + lead_h - 8 - 11 * len(deck_lines[:2])
        for ln in deck_lines[:2]:
            d.text((x + 8, dy), ln, font=f_lead_d, fill=MUTED)
            dy += 11

    # ---- dot-matrix map + region key -------------------------------
    map_y, map_h = 198, 164
    panel(d, 6, map_y, 624, map_h)
    d.text((14, map_y + 5), "THE WORLD IN DOTS \u2014 7 REGION PINS",
           font=f_blk_h, fill=INK)
    proj = draw_map(d, 14, map_y + 24, 608, 128)
    for i, (no, lon, lat) in enumerate(PINS):
        px, py = proj(lon, lat)
        color = REGIONS[i][1]
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=color,
                  outline=WHITE, width=2)
        label = str(i + 1)
        d.text((px - d.textlength(label, font=f_brief_b) / 2, py - 6),
               label, font=f_brief_b, fill=WHITE)
    panel(d, 638, map_y, 380, map_h)
    d.text((648, map_y + 5), "REGION KEY \u2014 STORY NUMBERS", font=f_blk_h, fill=INK)
    for i, (name, color, stories) in enumerate(REGIONS):
        ry = map_y + 24 + i * 19
        d.ellipse([650, ry + 1, 662, ry + 13], fill=color)
        d.text((650, ry + 1), f"  {i + 1}", font=f_brief_b, fill=WHITE)
        d.text((668, ry), f"{name}  \u00b7  #{stories[0][0]}\u2013#{stories[-1][0]}",
               font=f_brief, fill=INK)
        tag = f"{len(stories)} stories"
        d.text((1012 - d.textlength(tag, font=f_tiny), ry), tag, font=f_tiny, fill=MUTED)

    # ---- 13 feature tiles (with 3 leads = 16 panels) ---------------
    tile_y, tile_h, tile_w, tgap = 368, 68, 74, 4
    for i, (no, cap, ic) in enumerate(TILES):
        x = 6 + i * (tile_w + tgap)
        region = next(r for r in REGIONS if r[2][0][0] <= no <= r[2][-1][0])
        color = region[1]
        panel(d, x, tile_y, tile_w, tile_h)
        d.rectangle([x, tile_y, x + tile_w, tile_y + 13], fill=tint(color, 0.8))
        d.text((x + 4, tile_y + 2), f"#{no}", font=f_tiny_b, fill=WHITE)
        icon(d, ic, x + 17, tile_y + 17, 40, 26, tint(color, 0.6))
        cap_lines = wrap_text(d, cap, f_cap, tile_w - 8)
        cy = tile_y + tile_h - 4 - 8 * len(cap_lines[:2])
        for ln in cap_lines[:2]:
            d.text((x + 4, cy), ln, font=f_cap, fill=INK)
            cy += 8

    # ---- region story blocks ---------------------------------------
    blk_h, blk_gap = 100, 5
    col_w = 502
    stories_y0 = 442

    def draw_block(col_x, row, name, color, stories):
        y = stories_y0 + row * (blk_h + blk_gap)
        panel(d, col_x, y, col_w, blk_h)
        d.rectangle([col_x, y, col_x + col_w, y + 16], fill=color)
        d.text((col_x + 6, y + 3), f"{name}  \u00b7  #{stories[0][0]}\u2013#{stories[-1][0]}",
               font=f_blk_h, fill=WHITE)
        d.text((col_x + col_w - 62, y + 3), "8 STORIES", font=f_tiny_b, fill=WHITE)
        sub_w = (col_w - 12 - 8) // 2
        for k, (no, text, outlet) in enumerate(stories):
            sx = col_x + 6 + (k % 2) * (sub_w + 8)
            sy = y + 20 + (k // 2) * 20
            d.text((sx, sy), f"{no}.", font=f_brief_b, fill=color)
            full = f"{text} \u2014 {outlet}"
            lines = wrap_text(d, full, f_brief, sub_w - 20)
            ly = sy
            for ln in lines[:2]:
                d.text((sx + 20, ly), ln, font=f_brief, fill=INK)
                ly += 10
            if len(lines) > 2:
                print(f"WARN story #{no} truncated: {full}")
        return y + blk_h

    left_names = ["NORTH AMERICA", "LATIN AMERICA", "EUROPE", "MIDDLE EAST"]
    right_names = ["AFRICA", "ASIA", "OCEANIA"]
    by_name = {r[0]: r for r in REGIONS}
    for i, nm in enumerate(left_names):
        name, color, stories = by_name[nm]
        draw_block(6, i, name, color, stories)
    for i, nm in enumerate(right_names):
        name, color, stories = by_name[nm]
        draw_block(516, i, name, color, stories)

    # ---- left-out box (bottom of right column) ---------------------
    lo_y = stories_y0 + 3 * (blk_h + blk_gap) + 1
    lo_h = stories_y0 + 4 * (blk_h + blk_gap) - blk_gap - lo_y
    panel(d, 516, lo_y, col_w, lo_h, fill=(252, 244, 224))
    d.text((524, lo_y + 4), "LEFT OUT & WHY \u2014 DATE-CHECKED", font=f_blk_h, fill=INK)
    ly = lo_y + 20
    for item in LEFT_OUT:
        lines = wrap_text(d, "\u2022  " + item, f_lab, col_w - 18)
        for ln in lines[:2]:
            d.text((524, ly), ln, font=f_lab, fill=MUTED)
            ly += 10
        ly += 1

    # ---- UTC timeline ----------------------------------------------
    tl_y, tl_h = 862, 46
    panel(d, 6, tl_y, 1012, tl_h)
    d.text((12, tl_y + 4), "21 NOV \u2014 UTC TIMELINE", font=f_blk_h, fill=INK)
    seg_w = (1012 - 12 - 190) // 6
    for i, (t, txt) in enumerate(TIMELINE):
        sx = 200 + i * seg_w
        d.text((sx, tl_y + 4), t, font=f_time, fill=(192, 57, 43))
        lines = wrap_text(d, txt, f_lab, seg_w - 8)
        ly = tl_y + 19
        for ln in lines[:2]:
            d.text((sx, ly), ln, font=f_lab, fill=INK)
            ly += 10

    # ---- by the numbers --------------------------------------------
    nb_y, nb_h = 912, 44
    panel(d, 6, nb_y, 1012, nb_h)
    d.text((12, nb_y + 4), "BY THE NUMBERS", font=f_blk_h, fill=INK)
    for i, (num, lab) in enumerate(NUMBERS):
        sx = 150 + i * 143
        d.text((sx, nb_y + 3), num, font=f_num, fill=(46, 95, 163))
        lines = wrap_text(d, lab, f_lab, 136)
        ly = nb_y + 22
        for ln in lines[:2]:
            d.text((sx, ly), ln, font=f_lab, fill=INK)
            ly += 10

    # ---- weather ----------------------------------------------------
    wx_y, wx_h = 960, 38
    panel(d, 6, wx_y, 1012, wx_h)
    d.text((12, wx_y + 12), "WEATHER \u2014 DAY HIGHS 21 NOV", font=f_blk_h, fill=INK)
    for i, (city, hi, lo) in enumerate(WEATHER):
        sx = 210 + i * 114
        d.text((sx, wx_y + 5), city, font=f_tiny_b, fill=INK)
        d.text((sx, wx_y + 17), f"{hi} / {lo}", font=f_brief, fill=MUTED)

    # ---- footer -----------------------------------------------------
    foot = ("Every story dated 21 Nov 2026 \u00b7 sources + verification URLs in SOURCES.md  \u00b7  "
            "Just Security Early Edition for 21 Nov not yet published at build time (02:30 UTC) \u2014 "
            "stories verified against Reuters / AP / BBC / Al Jazeera / Guardian + outlets in SOURCES.md")
    d.text(((W - d.textlength(foot, font=f_tiny)) / 2, 1006), foot,
           font=f_tiny, fill=MUTED)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print(f"wrote {OUT} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    assert img.size == (1024, 1024), img.size


if __name__ == "__main__":
    main()
