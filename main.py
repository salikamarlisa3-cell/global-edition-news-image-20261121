# The Global Edition — Saturday 21 November 2026.
# A one-image summary of the day's world news, drawn with Pillow.
# 56 stories, 7 regions, 16 illustrated panels, a dot-matrix world
# map, a UTC timeline, a by-the-numbers strip, a weather strip and a
# "left out & why" box. Deterministic: fixed data, fixed layout, no
# clocks, no randomness — two runs produce a byte-identical PNG.
# Story data + verification URLs: see SOURCES.md.
from PIL import Image, ImageDraw, ImageFont

W = 1024
MARGIN = 16
CW = W - 2 * MARGIN  # content width

INK = (16, 24, 43)
PAPER = (250, 248, 243)
CARD = (255, 255, 255)
LINE = (198, 202, 210)
MUTE = (96, 104, 120)
NAVY = (13, 20, 38)

REGIONS = [
    ("NORTH AMERICA", "#1–#8", (192, 57, 43), [
        (1, "Mamdani unveils plan to close NYC's Rikers Island jail by 2032", "BBC"),
        (2, "Trump urges Nvidia to reinstate 'brilliant' Jensen Huang", "Al Jazeera"),
        (3, "Man who sparked deadly LA wildfire found guilty", "Guardian"),
        (4, "Trump turns press conference into 2028 succession audition", "Guardian"),
        (5, "Court: House unconstitutionally passed 2022 $1.7tn spending bill", "Reuters"),
        (6, "Senator blocks Trump cyber nominee over Jan 6 denial", "Guardian"),
        (7, "Trump: US flight systems 'ancient' but 'safe' after ground stop", "BBC"),
        (8, "Pair fined $811m for conning detained migrants", "BBC"),
    ]),
    ("LATIN AMERICA", "#9–#16", (211, 119, 32), [
        (9, "Two Salvadoran soldiers killed in Haiti explosives accident", "Al Jazeera"),
        (10, "Bukele registers bid for third term as El Salvador president", "AP"),
        (11, "Bolsonaro taken to hospital with severe abdominal pain", "Rio Times"),
        (12, "Mexico approves ballot for 2027 midterm election", "Rio Times"),
        (13, "Thousands protest Colombia tax plans amid US troops row", "Al Jazeera"),
        (14, "Lula visits ailing Chief Raoni as Brazil recognises Indigenous land", "Al Jazeera"),
        (15, "Trump: close to Mexico deal; more work to do with Canada", "Times of India"),
        (16, "Paraguay president impeached after Ueno Bank collapse", "Global Voice"),
    ]),
    ("EUROPE", "#17–#24", (36, 86, 166), [
        (17, "Denmark expels Russian diplomat over 'plot to kill Ukrainian rapper'", "Al Jazeera"),
        (18, "NI health: further doctors' strike planned in pay dispute", "BBC"),
        (19, "French officers guilty of racist assault on producer Michel Zecler", "Guardian"),
        (20, "Kryvyi Rih strike: two dead, 42 injured, children among hurt", "AppiSToS"),
        (21, "UK and EU agree reset: food trade and youth mobility deals", "BBC"),
        (22, "Russia decries 'new Iron Curtain' as Estonia shuts borders", "Al Jazeera"),
        (23, "Belgrade mayor charged with assaulting opposition politician", "Al Jazeera"),
        (24, "Depardieu and French author investigated over sexual allegations", "BBC"),
    ]),
    ("MIDDLE EAST", "#25–#32", (125, 60, 152), [
        (25, "Saudi coalition downs Houthi missiles fired at Riyadh", "Al Jazeera"),
        (26, "Iraq PM targets militia stronghold to assert state control", "Al Jazeera"),
        (27, "Fossil-fuel deadlock pushes COP31 summit into overtime", "Al Jazeera"),
        (28, "Israeli drone attacks kill seven Palestinians in central Gaza", "Al Jazeera"),
        (29, "Gaza's displaced children celebrate World Children's Day", "Al Jazeera"),
        (30, "Melania Trump calls for 'peace' for children of Gaza and Israel", "Variety"),
        (31, "US adds four Iranians to OFAC sanctions list over oil revenues", "AppiSToS"),
        (32, "Kataib Hezbollah faces deadline to quit Iraqi stronghold", "Al Jazeera"),
    ]),
    ("AFRICA", "#33–#40", (169, 134, 16), [
        (33, "ANC fights to keep control of South Africa's key cities", "BBC"),
        (34, "Somalia orders UAE ambassador out in sovereignty row", "Benin Web TV"),
        (35, "Boat of mourners capsizes in Nigeria; at least four dead", "Al Jazeera"),
        (36, "581 women murdered in South Africa in three months", "EIN / Xinhua"),
        (37, "Sudan war leaves disabled children out of education", "Al Jazeera"),
        (38, "Ebola workers in DR Congo plan strike over unpaid wages", "Rio Times"),
        (39, "Congo offensive displaces 323,000 in South Kivu in four days", "Peter's World"),
        (40, "South Sudan candidate survives arrest attempt by gunmen in Juba", "21 Nov digest"),
    ]),
    ("ASIA", "#41–#48", (30, 132, 73), [
        (41, "IndusInd Bank sacks ex-CEO Kathpalia, seeks to claw back pay", "Reuters"),
        (42, "South Korea tops UN e-government index for first time", "21 Nov digest"),
        (43, "Myanmar calls ICJ genocide ruling 'unfair'", "The Hindu"),
        (44, "Malaysia plans to resettle 10,000 Rohingya in Turkiye", "The Hindu"),
        (45, "Indian man jailed 19 years over plot to kill Sikh separatist in US", "Al Jazeera"),
        (46, "Nepal PM Balendra Shah to meet Modi on first trip abroad", "BBC"),
        (47, "Rahul Gandhi backs strong India–Israel ties despite Gaza war", "Al Jazeera"),
        (48, "South Korea catches 111 students in exam-cheating crackdown", "BBC"),
    ]),
    ("OCEANIA", "#49–#56", (20, 143, 119), [
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
    ("LEAD 1", 3, 25, "Houthi missiles fired at Riyadh — Saudi coalition intercepts three",
     "Fresh wave of attacks on the Saudi capital as the Iran war escalates.", "missile"),
    ("LEAD 2", 2, 17, "Denmark expels Russian diplomat over 'plot to kill Ukrainian rapper'",
     "Copenhagen accuses Moscow of planning the killing with a banned gang.", "envoy"),
    ("LEAD 3", 0, 1, "Mamdani unveils plan to close Rikers Island jail by 2032",
     "Shuttering the troubled jail was first voted for in 2019; delays followed.", "jail"),
]

TILES = [
    (26, "IRAQ: MILITIA STANDOFF", "house"),
    (27, "COP31 IN OVERTIME", "sun"),
    (33, "SOUTH AFRICA VOTES", "ballot"),
    (34, "SOMALIA EXPELS ENVOY", "envoy"),
    (10, "BUKELE: THIRD TERM", "flag"),
    (11, "BOLSONARO IN HOSPITAL", "cross"),
    (21, "UK–EU RESET DEAL", "scales"),
    (20, "KRYVYI RIH HIT", "burst"),
    (41, "INDUSIND SACKS EX-CEO", "bank"),
    (49, "VICTORIA: VOTE ROW", "ballot"),
    (35, "NIGERIA BOAT TRAGEDY", "boat"),
    (45, "19 YEARS: SIKH PLOT", "key"),
    (5, "SPENDING BILL VOID", "doc"),
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
    ("581", "women murdered in South Africa, Jul–Sep 2026"),
    ("323,000", "people fled South Kivu fighting in four days"),
    ("1,000", "long-range drones UK will send Ukraine (£260m)"),
    ("10,000", "Rohingya Malaysia plans to resettle in Türkiye"),
    ("111", "students caught in South Korea exam crackdown"),
]

# Day highs / lows for 21 Nov 2026, Open-Meteo forecast (fetched 21 Nov).
WEATHER = [
    ("NEW YORK", 18, 6),
    ("MEXICO CITY", 24, 11),
    ("LONDON", 10, 6),
    ("RIYADH", 30, 19),
    ("JOHANNESBURG", 27, 16),
    ("NEW DELHI", 24, 15),
    ("SYDNEY", 27, 18),
]

LEFTOUT = [
    "ICJ Rohingya genocide ruling (19 Nov) — led yesterday's edition; Myanmar's reply is story #43.",
    "Trump–Xi–Putin 'peace declaration' (19–20 Nov) — led yesterday's edition.",
    "Anthropic's $81.3bn IPO debut (20 Nov) — led yesterday's edition; day-2 slide: Nasdaq erased all 2026 gains.",
    "GTA 6's $3.79bn first-day sales (20 Nov) — entertainment, not world news.",
    "COP31 draft with no fossil fuels (20 Nov) — superseded by today's overtime deadlock, story #27.",
]

# Stylised world land grid, built from span runs per row
# (row 0 is the high Arctic, row 43 the far south; each row is
# 100 columns of longitude). Pins are grid coordinates per region.
MAPSPANS = {
    0: [(8, 14), (36, 42)],
    1: [(6, 16), (35, 43)],
    2: [(4, 20), (34, 44), (62, 63)],
    3: [(3, 24), (35, 43), (61, 70), (74, 84), (88, 97)],
    4: [(3, 28), (36, 42), (53, 57), (61, 99)],
    5: [(4, 29), (37, 41), (47, 47), (53, 58), (60, 99)],
    6: [(5, 30), (38, 40), (46, 47), (52, 99)],
    7: [(6, 30), (50, 60), (61, 99)],
    8: [(7, 29), (49, 59), (62, 97), (90, 90)],
    9: [(7, 28), (48, 58), (62, 90), (89, 91)],
    10: [(8, 27), (48, 57), (63, 88), (90, 91)],
    11: [(8, 26), (48, 56), (64, 86)],
    12: [(9, 25), (47, 55), (65, 85)],
    13: [(9, 24), (53, 55), (58, 64), (66, 84)],
    14: [(10, 23), (47, 49), (54, 57), (58, 61), (67, 82)],
    15: [(10, 21), (60, 66), (68, 80)],
    16: [(11, 20), (46, 66), (69, 76), (77, 81)],
    17: [(12, 19), (46, 62), (60, 65), (69, 75), (76, 80)],
    18: [(13, 18), (47, 62), (70, 74), (76, 79), (83, 84)],
    19: [(14, 17), (47, 61), (70, 73), (76, 78), (83, 84)],
    20: [(48, 61), (70, 72), (74, 88)],
    21: [(48, 60), (75, 89)],
    22: [(49, 60), (80, 90)],
    23: [(29, 34), (49, 59)],
    24: [(29, 37), (50, 59), (63, 63)],
    25: [(29, 38), (50, 58), (63, 63)],
    26: [(30, 39), (50, 58), (62, 63)],
    27: [(30, 39), (51, 57), (62, 63)],
    28: [(30, 38), (51, 57), (62, 62)],
    29: [(31, 37), (51, 56)],
    30: [(31, 37), (52, 56)],
    31: [(31, 36), (52, 55), (82, 88)],
    32: [(32, 36), (52, 55), (81, 91)],
    33: [(32, 35), (52, 54), (81, 92)],
    34: [(32, 35), (52, 54), (82, 92)],
    35: [(32, 34), (52, 53), (82, 91)],
    36: [(32, 34), (83, 90)],
    37: [(32, 33), (84, 89)],
    38: [(32, 33), (85, 88)],
    39: [(32, 33)],
    40: [(32, 33), (90, 90), (96, 96)],
    41: [(32, 32), (95, 96)],
    42: [(95, 95)],
    43: [(95, 95)],
}
MAPGRID = []
for _r in range(44):
    _row = [" "] * 100
    for _a, _b in MAPSPANS.get(_r, []):
        for _c in range(_a, _b + 1):
            _row[_c] = "#"
    MAPGRID.append("".join(_row))
PINS = [(18, 10), (33, 29), (52, 9), (63, 17), (55, 25), (76, 13), (87, 34)]

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(text, font, maxw):
    words = text.split()
    lines = []
    cur = ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if font.getlength(trial) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None):
    lines = wrap(text, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and font.getlength(last + "…") > maxw:
            last = last[:-1]
        lines[-1] = last + "…"
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def icon(d, kind, x, y, s, col):
    """Tiny geometric glyphs drawn in an s-by-s box at (x, y)."""
    w = max(2, s // 14)
    cx, cy = x + s // 2, y + s // 2
    if kind == "missile":
        d.polygon([(x + s * 0.62, y + s * 0.06), (x + s * 0.94, y + s * 0.38),
                   (x + s * 0.72, y + s * 0.60), (x + s * 0.40, y + s * 0.28)], outline=col, width=w)
        d.polygon([(x + s * 0.40, y + s * 0.28), (x + s * 0.16, y + s * 0.30),
                   (x + s * 0.28, y + s * 0.52)], outline=col, width=w)
        d.polygon([(x + s * 0.72, y + s * 0.60), (x + s * 0.70, y + s * 0.84),
                   (x + s * 0.48, y + s * 0.72)], outline=col, width=w)
        d.polygon([(x + s * 0.30, y + s * 0.70), (x + s * 0.06, y + s * 0.94),
                   (x + s * 0.16, y + s * 0.62)], fill=col)
    elif kind == "envoy":
        d.rectangle([x + s * 0.08, y + s * 0.24, x + s * 0.92, y + s * 0.78], outline=col, width=w)
        d.line([x + s * 0.08, y + s * 0.24, cx, y + s * 0.58], fill=col, width=w)
        d.line([x + s * 0.92, y + s * 0.24, cx, y + s * 0.58], fill=col, width=w)
        d.line([x + s * 0.66, y + s * 0.60, x + s * 0.88, y + s * 0.82], fill=(192, 57, 43), width=w)
        d.line([x + s * 0.88, y + s * 0.60, x + s * 0.66, y + s * 0.82], fill=(192, 57, 43), width=w)
    elif kind == "jail":
        d.rectangle([x + s * 0.14, y + s * 0.10, x + s * 0.86, y + s * 0.90], outline=col, width=w)
        for i in range(4):
            bx = x + s * (0.30 + 0.14 * i)
            d.line([bx, y + s * 0.10, bx, y + s * 0.90], fill=col, width=w)
    elif kind == "house":
        d.polygon([(x + s * 0.10, y + s * 0.48), (cx, y + s * 0.12), (x + s * 0.90, y + s * 0.48)], outline=col, width=w)
        d.rectangle([x + s * 0.24, y + s * 0.48, x + s * 0.76, y + s * 0.88], outline=col, width=w)
    elif kind == "sun":
        r = s * 0.20
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
            d.line([cx + dx * r * 1.35, cy + dy * r * 1.35, cx + dx * r * 1.9, cy + dy * r * 1.9], fill=col, width=w)
    elif kind == "ballot":
        d.rectangle([x + s * 0.14, y + s * 0.44, x + s * 0.86, y + s * 0.86], outline=col, width=w)
        d.rectangle([x + s * 0.32, y + s * 0.12, x + s * 0.68, y + s * 0.48], outline=col, width=w)
        d.line([x + s * 0.30, y + s * 0.62, x + s * 0.70, y + s * 0.62], fill=col, width=w)
    elif kind == "flag":
        d.line([x + s * 0.26, y + s * 0.08, x + s * 0.26, y + s * 0.92], fill=col, width=w)
        d.polygon([(x + s * 0.26, y + s * 0.10), (x + s * 0.84, y + s * 0.20),
                   (x + s * 0.26, y + s * 0.36)], outline=col, width=w)
    elif kind == "cross":
        d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], outline=col, width=w)
        d.rectangle([cx - w, y + s * 0.30, cx + w, y + s * 0.70], fill=col)
        d.rectangle([x + s * 0.30, cy - w, x + s * 0.70, cy + w], fill=col)
    elif kind == "scales":
        d.line([cx, y + s * 0.16, cx, y + s * 0.84], fill=col, width=w)
        d.line([x + s * 0.16, y + s * 0.24, x + s * 0.84, y + s * 0.24], fill=col, width=w)
        for px in (0.16, 0.84):
            d.line([x + s * px, y + s * 0.24, x + s * (px - 0.09), y + s * 0.52], fill=col, width=w)
            d.line([x + s * px, y + s * 0.24, x + s * (px + 0.09), y + s * 0.52], fill=col, width=w)
            d.arc([x + s * (px - 0.11), y + s * 0.40, x + s * (px + 0.11), y + s * 0.62], 0, 180, fill=col, width=w)
        d.line([x + s * 0.34, y + s * 0.86, x + s * 0.66, y + s * 0.86], fill=col, width=w)
    elif kind == "burst":
        pts = []
        for i in range(16):
            ang = 3.14159 * i / 8
            rr = s * 0.44 if i % 2 == 0 else s * 0.18
            pts.append((cx + rr * __import__("math").cos(ang), cy + rr * __import__("math").sin(ang)))
        d.polygon(pts, outline=col, width=w)
    elif kind == "bank":
        d.polygon([(x + s * 0.08, y + s * 0.30), (cx, y + s * 0.10), (x + s * 0.92, y + s * 0.30)], outline=col, width=w)
        for i in range(3):
            bx = x + s * (0.24 + 0.22 * i)
            d.line([bx, y + s * 0.38, bx, y + s * 0.72], fill=col, width=w + 1)
        d.line([x + s * 0.12, y + s * 0.80, x + s * 0.88, y + s * 0.80], fill=col, width=w)
        d.line([x + s * 0.12, y + s * 0.88, x + s * 0.88, y + s * 0.88], fill=col, width=w)
    elif kind == "boat":
        d.polygon([(x + s * 0.10, y + s * 0.62), (x + s * 0.90, y + s * 0.62),
                   (x + s * 0.74, y + s * 0.86), (x + s * 0.26, y + s * 0.86)], outline=col, width=w)
        d.line([cx, y + s * 0.14, cx, y + s * 0.62], fill=col, width=w)
        d.polygon([(cx, y + s * 0.16), (cx, y + s * 0.56), (x + s * 0.72, y + s * 0.56)], outline=col, width=w)
    elif kind == "key":
        d.ellipse([x + s * 0.10, y + s * 0.26, x + s * 0.52, y + s * 0.68], outline=col, width=w)
        d.line([x + s * 0.48, y + s * 0.56, x + s * 0.88, y + s * 0.88], fill=col, width=w)
        d.line([x + s * 0.70, y + s * 0.70, x + s * 0.82, y + s * 0.60], fill=col, width=w)
        d.line([x + s * 0.80, y + s * 0.80, x + s * 0.92, y + s * 0.70], fill=col, width=w)
    elif kind == "doc":
        d.rectangle([x + s * 0.24, y + s * 0.08, x + s * 0.78, y + s * 0.92], outline=col, width=w)
        for i in range(3):
            ly = y + s * (0.32 + 0.18 * i)
            d.line([x + s * 0.36, ly, x + s * 0.66, ly], fill=col, width=w)
    else:
        d.ellipse([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8], outline=col, width=w)


def build():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    f_title = F("DejaVuSerif-Bold.ttf", 30)
    f_sub = F("DejaVuSans.ttf", 11)
    f_meta = F("DejaVuSans-Bold.ttf", 12)
    f_lead_k = F("DejaVuSans-Bold.ttf", 10)
    f_lead = F("DejaVuSans-Bold.ttf", 16)
    f_dek = F("DejaVuSans.ttf", 10)
    f_h = F("DejaVuSans-Bold.ttf", 11)
    f_story = F("DejaVuSans.ttf", 9)
    f_story_n = F("DejaVuSans-Bold.ttf", 9)
    f_cap = F("DejaVuSans-Bold.ttf", 8)
    f_time = F("DejaVuSans-Bold.ttf", 11)
    f_small = F("DejaVuSans.ttf", 9)
    f_num = F("DejaVuSans-Bold.ttf", 19)
    f_wx = F("DejaVuSans-Bold.ttf", 10)

    # Header
    d.rectangle([0, 0, W, 60], fill=NAVY)
    d.text((MARGIN, 8), "THE GLOBAL EDITION", font=f_title, fill=(255, 255, 255))
    d.text((MARGIN, 44), "SATURDAY 21 NOVEMBER 2026 · THE WORLD IN ONE IMAGE", font=f_sub, fill=(178, 190, 214))
    right1 = "56 STORIES · 7 REGIONS · 16 PANELS"
    d.text((W - MARGIN - f_meta.getlength(right1), 12), right1, font=f_meta, fill=(255, 255, 255))
    right2 = "make.fun · news-image-20261121 · @salikamarlisa3-cell"
    d.text((W - MARGIN - f_sub.getlength(right2), 36), right2, font=f_sub, fill=(178, 190, 214))

    # Lead cards
    y = 68
    lead_w = (CW - 2 * 8) // 3
    for i, (kick, ridx, num, head, dek, ic) in enumerate(LEADS):
        x = MARGIN + i * (lead_w + 8)
        col = REGIONS[ridx][2]
        d.rectangle([x, y, x + lead_w, y + 124], fill=CARD, outline=LINE)
        d.rectangle([x, y, x + lead_w, y + 20], fill=col)
        outlet = next(s[2] for s in REGIONS[ridx][3] if s[0] == num)
        d.text((x + 8, y + 5), f"{kick} · {REGIONS[ridx][0]} · {outlet.upper()}", font=f_lead_k, fill=(255, 255, 255))
        chip = f"#{num}"
        d.text((x + lead_w - 8 - f_lead_k.getlength(chip), y + 5), chip, font=f_lead_k, fill=(255, 255, 255))
        icon(d, ic, x + lead_w - 62, y + 34, 48, col)
        text_block(d, x + 8, y + 28, head, f_lead, INK, lead_w - 78, 19, max_lines=3)
        text_block(d, x + 8, y + 96, dek, f_dek, MUTE, lead_w - 16, 12, max_lines=2)

    # Map + region key
    y = 200
    d.rectangle([MARGIN, y, 660, y + 156], fill=CARD, outline=LINE)
    d.text((MARGIN + 10, y + 7), "THE WORLD IN DOTS — 7 REGION PINS", font=f_h, fill=INK)
    ox, oy = MARGIN + 26, y + 30
    px_, py_ = 5.9, 2.7
    land = (104, 116, 138)
    for r, row in enumerate(MAPGRID):
        for c, ch in enumerate(row):
            if ch == "#":
                cxp, cyp = ox + c * px_, oy + r * py_
                d.ellipse([cxp - 1.35, cyp - 1.35, cxp + 1.35, cyp + 1.35], fill=land)
    for i, (gx, gy) in enumerate(PINS):
        cxp, cyp = ox + gx * px_, oy + gy * py_
        col = REGIONS[i][2]
        d.ellipse([cxp - 9, cyp - 9, cxp + 9, cyp + 9], fill=col, outline=(255, 255, 255), width=2)
        t = str(i + 1)
        d.text((cxp - f_cap.getlength(t) / 2, cyp - 5), t, font=f_cap, fill=(255, 255, 255))
    kx = 668
    d.rectangle([kx, y, W - MARGIN, y + 156], fill=CARD, outline=LINE)
    d.text((kx + 10, y + 7), "REGION KEY — STORY NUMBERS", font=f_h, fill=INK)
    for i, reg in enumerate(REGIONS):
        ry = y + 32 + i * 17.5
        col = reg[2]
        d.ellipse([kx + 10, ry, kx + 24, ry + 14], fill=col)
        t = str(i + 1)
        d.text((kx + 17 - f_cap.getlength(t) / 2, ry + 2), t, font=f_cap, fill=(255, 255, 255))
        d.text((kx + 32, ry + 1), reg[0], font=f_small, fill=INK)
        d.text((kx + 168, ry + 1), reg[1], font=f_small, fill=MUTE)
        lab = "8 stories"
        d.text((W - MARGIN - 10 - f_small.getlength(lab), ry + 1), lab, font=f_small, fill=MUTE)

    # Feature tiles
    y = 364
    tile_w = 71
    step = (CW - tile_w) / 12
    for i, (num, label, ic) in enumerate(TILES):
        x = MARGIN + i * step
        ridx = (num - 1) // 8
        col = REGIONS[ridx][2]
        d.rectangle([x, y, x + tile_w, y + 76], fill=CARD, outline=LINE)
        d.rectangle([x, y, x + tile_w, y + 13], fill=col)
        chip = f"#{num}"
        d.text((x + 4, y + 2), chip, font=f_cap, fill=(255, 255, 255))
        icon(d, ic, x + tile_w / 2 - 13, y + 17, 26, col)
        lines = wrap(label, f_cap, tile_w - 6)
        ly = y + 47
        for ln in lines[:3]:
            d.text((x + tile_w / 2 - f_cap.getlength(ln) / 2, ly), ln, font=f_cap, fill=INK)
            ly += 9

    # Region columns
    y = 448
    col_w = (CW - 8) // 2
    stacks = [[0, 1, 2, 3], [4, 5, 6, 7]]
    for si, stack in enumerate(stacks):
        x = MARGIN + si * (col_w + 8)
        for bi, ridx in enumerate(stack):
            by = y + bi * 95
            if ridx < 7:
                name, rng, col, stories = REGIONS[ridx]
                d.rectangle([x, by, x + col_w, by + 90], fill=CARD, outline=LINE)
                d.rectangle([x, by, x + col_w, by + 15], fill=col)
                d.text((x + 7, by + 3), name, font=f_cap, fill=(255, 255, 255))
                mid = f"#{stories[0][0]}–#{stories[-1][0]}"
                d.text((x + 96, by + 3), mid, font=f_cap, fill=(255, 255, 255))
                lab = "8 STORIES"
                d.text((x + col_w - 7 - f_cap.getlength(lab), by + 3), lab, font=f_cap, fill=(255, 255, 255))
                half = (col_w - 14) // 2
                for k, (num, head, outlet) in enumerate(stories):
                    cxp = x + 7 + (k // 4) * half
                    cyp = by + 20 + (k % 4) * 17.5
                    d.text((cxp, cyp), f"{num}.", font=f_story_n, fill=col)
                    text_block(d, cxp + 15, cyp, f"{head} — {outlet}", f_story, INK, half - 17, 9, max_lines=2)
            else:
                d.rectangle([x, by, x + col_w, by + 90], fill=(244, 241, 233), outline=LINE)
                d.rectangle([x, by, x + col_w, by + 15], fill=INK)
                d.text((x + 7, by + 3), "LEFT OUT & WHY — DATE-CHECKED", font=f_cap, fill=(255, 255, 255))
                ly = by + 19
                for item in LEFTOUT:
                    ly = text_block(d, x + 7, ly, "• " + item, f_story, INK, col_w - 14, 9, max_lines=2) + 1

    # Timeline
    y = 832
    d.text((MARGIN, y), "21 NOV · UTC TIMELINE", font=f_h, fill=INK)
    d.line([MARGIN, y + 17, W - MARGIN, y + 17], fill=LINE, width=1)
    cell = CW / 6
    for i, (tm, label) in enumerate(TIMELINE):
        x = MARGIN + i * cell
        d.ellipse([x, y + 14, x + 6, y + 20], fill=INK)
        d.text((x, y + 24), tm, font=f_time, fill=INK)
        text_block(d, x, y + 40, label, f_small, MUTE, cell - 10, 10, max_lines=2)

    # By the numbers
    y = 898
    d.text((MARGIN, y), "BY THE NUMBERS", font=f_h, fill=INK)
    for i, (num, cap) in enumerate(NUMBERS):
        x = MARGIN + i * cell
        d.text((x, y + 15), num, font=f_num, fill=INK)
        text_block(d, x, y + 40, cap, f_small, MUTE, cell - 10, 10, max_lines=2)

    # Weather + footer
    y = 972
    d.line([MARGIN, y - 6, W - MARGIN, y - 6], fill=LINE, width=1)
    d.text((MARGIN, y), "WEATHER — DAY HIGHS 21 NOV", font=f_wx, fill=INK)
    wx = MARGIN + 218
    for name, hi, lo in WEATHER:
        seg = f"{name} {hi}°/{lo}°"
        d.text((wx, y), seg, font=f_small, fill=MUTE)
        wx += f_small.getlength(seg) + 13
    foot = ("Every story dated 21 Nov 2026 · sources + verification URLs in SOURCES.md · Just Security Early Edition for 21 Nov "
            "not yet published at build time (02:30 UTC) — stories verified against Reuters / AP / BBC / Al Jazeera / Guardian + outlets in SOURCES.md")
    text_block(d, MARGIN, y + 17, foot, F("DejaVuSans.ttf", 8), MUTE, CW, 10, max_lines=2)
    return img


if __name__ == "__main__":
    build().save("entry.png")
