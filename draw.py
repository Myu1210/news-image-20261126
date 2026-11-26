#!/usr/bin/env python3
"""news-image-20261126: front-page newspaper, 1024x1024, PIL only.
Draws from the prose spec: 13 drawn scenes + stories 14-36 + map +
UTC timeline + date-check box. No AI generation, no invented stories.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser("~/workspace/makefun/entries/news-image-20261126/entry.png")

# ---------- palette ----------
PAPER = (245, 239, 224)
INK = (27, 42, 74)
RED = (176, 42, 48)
GOLD = (176, 141, 60)
RULE = (190, 178, 150)
LIGHT = (237, 228, 206)
SEA = (214, 230, 240)
LAND = (232, 220, 192)
GREEN = (31, 107, 58)
AMBER = (138, 109, 0)
GREY = (120, 120, 120)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    try:
        return ImageFont.truetype(FDIR + name, size)
    except OSError:
        return ImageFont.truetype(FDIR + "DejaVuSans.ttf", size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# ---------- data (exact copy from the brief) ----------
SCENES = [
    (1, "MACY'S PARADE POSTPONED",
     "100th Thanksgiving parade moved to Saturday as a storm hits New York \u2014 a first in its history.",
     "CNN", "CONFIRMED", "parade"),
    (2, "18 YEARS SINCE 26/11",
     "India marks the Mumbai attacks and Constitution Day with ceremonies across the country.",
     "PTI", "CONFIRMED", "candles"),
    (3, "GAME 3 IN GENEVA",
     "Gukesh and Sindarov meet tied 1\u20131 after two draws in the world title match.",
     "FIDE", "ONGOING", "chess"),
    (4, "MISSILES OVER RIYADH",
     "Houthis strike Saudi ports and the Ras Tanura refinery; defences down missiles over the capital.",
     "REUTERS", "REPORTED", "refinery"),
    (5, "TANKERS HIT BY MINES",
     "Two tankers struck by naval mines in the Strait of Hormuz.",
     "REUTERS", "REPORTED", "tanker"),
    (6, "HAMAS SECURITY CHIEF KILLED",
     "Israeli strike kills Mohammed Abu al-Ouf in Gaza.",
     "AP", "REPORTED", "building"),
    (7, "FIVE JETS DAMAGED",
     "Ukraine strikes Russia's Savasleyka airbase: three MiG-31s and two Su-34s hit.",
     "KYIV", "REPORTED", "jets"),
    (8, "KYIV MALL HIT",
     "Russian strikes hit a Kyiv shopping mall; four hurt and power cut.",
     "KYIV POST", "REPORTED", "mall"),
    (9, "TARIFFS ON 14 PARTNERS",
     "US proposes new tariffs on 14 trading partners, including China, the EU, Japan and India.",
     "REUTERS", "CONFIRMED", "tariffs"),
    (10, "KOREA LIFTS RATE TO 3.25%",
     "Bank of Korea raises its key rate as the won steadies.",
     "BANK OF KOREA", "CONFIRMED", "bank"),
    (11, "FIRST PAKISTANI IN ORBIT",
     "Shenzhou-24 docks; Muhammad Zeeshan Ali reaches the Tiangong station.",
     "XINHUA", "CONFIRMED", "space"),
    (12, "WAR DEAD NEAR 500,000",
     "Leaked data put Russia's war dead at almost half a million.",
     "BBC", "REPORTED", "docs"),
    (13, "SOLOMONS SIGNS SECURITY PACT",
     "Solomon Islands signs a security pact with Australia.",
     "AP", "CONFIRMED", "pact"),
]

ALSO = [
    (14, "Pyongyang", "Kim orders wider tactical nuclear deployment", "KCNA"),
    (15, "Washington", "Second judge blocks Trump's birthright order", "REUTERS"),
    (16, "Tehran", "US tells citizens to leave Iran as war fears grow", "REUTERS"),
    (17, "Santa Clara", "Jensen Huang returns to Nvidia amid US scrutiny", "REUTERS"),
    (18, "Madrid", "Spain heads to snap vote Sunday, right favoured", "REUTERS"),
    (19, "Washington", "FCC approves SpaceX plan for one million satellites", "REUTERS"),
    (20, "Bogot\u00e1", "Police free 76 supermarket hostages", "AP"),
    (21, "Washington", "Huawei guilty of stealing US trade secrets", "REUTERS"),
    (22, "Canary Islands", "Nearly 2,000 migrants arrive in a day", "AP"),
    (23, "Liverpool", "Liverpool beat Club Brugge 3\u20130", "UEFA"),
    (24, "San Juan", "Jennifer Barreto of Puerto Rico wins Miss Universe 2026", "AP"),
    (25, "New York", "AI sell-off nears Nasdaq bear market; Brent $91.19", "ONETURN"),
    (26, "Brussels", "EU leaders clash over \u20ac45bn Ukraine loan", "REUTERS"),
    (27, "Bogor", "13 miners trapped in flooded gold mine", "AFP"),
    (28, "San Juan", "Puerto Rico court cancels Luma Energy contract", "AP"),
    (29, "Hasakah", "ISIL attack kills two security personnel", "REUTERS"),
    (30, "Lusaka", "Zambia bans protest over term-limit push", "REUTERS"),
    (31, "Beirut", "Lebanon to open second airport next month", "REUTERS"),
    (32, "Geneva", "Dozens of nations urge Russia to halt riot-agent use", "REUTERS"),
    (33, "Murmansk", "Governor held in detention over corruption", "REUTERS"),
    (34, "Hong Kong", "A year since the Tai Po fire that killed 168", "BBC"),
    (35, "Benin City", "Gunmen fire on Peter Obi rally in Edo", "PREMIUM TIMES"),
    (36, "Blue Nile", "Sudan drone strikes kill 19", "RADIO GENERATION"),
]

TIMELINE = [
    ("00:00", "Thanksgiving Day begins in the US"),
    ("13:30", "Macy's parade was due to step off (8:30 ET)"),
    ("14:00", "Chess Game 3 begins, Geneva (15:00 CET)"),
    ("15:00", "NYC high-wind warning begins (10:00 ET)"),
    ("23:00", "The day's 36 stories filed"),
]

DATECHECK = [
    ("Bangladesh garment wage agreed, Tk 17,000", "25 Nov"),
    ("Cairo tanker fire, 31 dead", "25 Nov"),
    ("Pete Edochie dies at 79", "25 Nov"),
    ("Ramaphosa Phala Phala case thrown out", "25 Nov"),
    ("Chess Game 2 ends in a draw", "25 Nov"),
    ("Chess Game 1 ends in a draw", "24 Nov"),
]

CHIPS = [("N. AMERICA", 9), ("EUROPE", 9), ("MIDDLE EAST", 7), ("EAST ASIA", 4),
         ("AFRICA", 3), ("SOUTH ASIA", 1), ("SE ASIA", 1), ("OCEANIA", 1), ("S. AMERICA", 1)]

SOURCES_LINE = ("AP \u00b7 REUTERS \u00b7 AFP \u00b7 BBC \u00b7 CNN \u00b7 USA TODAY \u00b7 PTI \u00b7 FIDE \u00b7 "
                "XINHUA \u00b7 KCNA \u00b7 KYIV POST \u00b7 BANK OF KOREA \u00b7 PREMIUM TIMES \u00b7 "
                "RADIO GENERATION \u00b7 ONETURN \u00b7 DAILYSUMMARY \u00b7 UEFA")

# map pins: (lon, lat) per scene number; display offset (dx, dy) in px where crowded
PINS = {1: (-74, 41, 0, 0), 2: (73, 19, 0, 0), 3: (6, 46, 0, 0), 4: (47, 25, 0, 0),
        5: (56, 26, 0, 0), 6: (34, 31, 0, 0), 7: (43, 55, 0, 0), 8: (31, 50, 0, 0),
        9: (-77, 39, -11, 9), 10: (127, 38, 0, 0), 11: (115, 32, 0, -12),
        12: (70, 60, 0, 0), 13: (160, -9, 0, 0)}

# ---------- helpers ----------
def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def tracked(draw, cx, y, text, fnt, fill, tracking=3):
    w = sum(draw.textlength(c, font=fnt) for c in text) + tracking * (len(text) - 1)
    x = cx - w / 2
    for c in text:
        draw.text((x, y), c, font=fnt, fill=fill)
        x += draw.textlength(c, font=fnt) + tracking

def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)

# ---------- flat-vector icons, drawn in a 50x50 box at (x0, y0) ----------
def icon_parade(d, x0, y0):
    d.rectangle([x0, y0 + 30, x0 + 10, y0 + 50], fill=INK)
    d.rectangle([x0 + 12, y0 + 22, x0 + 22, y0 + 50], fill=INK)
    d.rectangle([x0 + 24, y0 + 34, x0 + 34, y0 + 50], fill=INK)
    for wx in (x0 + 3, x0 + 15, x0 + 27):
        for wy in (y0 + 34, y0 + 40, y0 + 46):
            d.rectangle([wx, wy, wx + 3, wy + 3], fill=(245, 239, 224))
    d.ellipse([x0 + 28, y0 + 2, x0 + 48, y0 + 18], fill=RED)
    d.polygon([(x0 + 38, y0 + 18), (x0 + 34, y0 + 24), (x0 + 42, y0 + 24)], fill=RED)
    d.line([x0 + 38, y0 + 24, x0 + 38, y0 + 30], fill=INK, width=1)

def icon_candles(d, x0, y0):
    d.rectangle([x0 + 2, y0 + 2, x0 + 30, y0 + 7], fill=(255, 153, 51))
    d.rectangle([x0 + 2, y0 + 7, x0 + 30, y0 + 12], fill=(255, 255, 255), outline=INK)
    d.rectangle([x0 + 2, y0 + 12, x0 + 30, y0 + 17], fill=(19, 136, 8))
    d.ellipse([x0 + 13, y0 + 6, x0 + 19, y0 + 12], outline=INK, width=1)
    for cx in (x0 + 36, x0 + 45):
        d.polygon([(cx, y0 + 22), (cx - 3, y0 + 28), (cx + 3, y0 + 28)], fill=(255, 180, 0))
        d.rectangle([cx - 3, y0 + 28, cx + 3, y0 + 48], fill=(250, 240, 210), outline=INK)

def icon_chess(d, x0, y0):
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x0 + c * 7, y0 + 8 + r * 7, x0 + c * 7 + 7, y0 + 8 + r * 7 + 7], fill=INK)
    d.rectangle([x0, y0 + 8, x0 + 28, y0 + 36], outline=INK, width=1)
    d.ellipse([x0 + 32, y0 + 10, x0 + 49, y0 + 27], outline=INK, width=2)
    d.line([x0 + 40, y0 + 18, x0 + 40, y0 + 12], fill=RED, width=2)
    d.line([x0 + 40, y0 + 18, x0 + 45, y0 + 20], fill=RED, width=2)
    d.rectangle([x0 + 30, y0 + 40, x0 + 50, y0 + 48], outline=INK, width=1)
    d.text((x0 + 33, y0 + 40), "1-1", font=SANS_B(8), fill=INK)

def icon_refinery(d, x0, y0):
    d.rectangle([x0 + 4, y0 + 20, x0 + 12, y0 + 50], fill=INK)
    d.rectangle([x0 + 16, y0 + 28, x0 + 26, y0 + 50], fill=INK)
    d.rectangle([x0 + 30, y0 + 36, x0 + 38, y0 + 50], fill=INK)
    d.polygon([(x0 + 8, y0 + 12), (x0 + 4, y0 + 20), (x0 + 12, y0 + 20)], fill=(255, 140, 0))
    d.polygon([(x0 + 21, y0 + 20), (x0 + 17, y0 + 28), (x0 + 25, y0 + 28)], fill=(255, 140, 0))
    d.line([x0 + 34, y0 + 8, x0 + 44, y0 + 16], fill=RED, width=2)
    d.line([x0 + 38, y0 + 4, x0 + 48, y0 + 12], fill=RED, width=2)
    d.ellipse([x0 + 44, y0 + 12, x0 + 48, y0 + 16], fill=RED)

def icon_tanker(d, x0, y0):
    d.polygon([(x0 + 2, y0 + 26), (x0 + 40, y0 + 26), (x0 + 36, y0 + 40), (x0 + 6, y0 + 40)], fill=INK)
    d.rectangle([x0 + 30, y0 + 16, x0 + 38, y0 + 26], fill=RED)
    d.rectangle([x0 + 8, y0 + 20, x0 + 14, y0 + 26], fill=RED)
    d.line([x0, y0 + 44, x0 + 12, y0 + 44], fill=(90, 140, 180), width=2)
    d.line([x0 + 16, y0 + 47, x0 + 34, y0 + 47], fill=(90, 140, 180), width=2)
    cx, cy = x0 + 43, y0 + 10
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(60, 60, 60))
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([cx + 5 * math.cos(a), cy + 5 * math.sin(a),
                cx + 9 * math.cos(a), cy + 9 * math.sin(a)], fill=(60, 60, 60), width=2)

def icon_building(d, x0, y0):
    d.rectangle([x0 + 8, y0 + 16, x0 + 34, y0 + 50], fill=INK)
    for r in range(3):
        for c in range(3):
            d.rectangle([x0 + 12 + c * 8, y0 + 20 + r * 9, x0 + 16 + c * 8, y0 + 24 + r * 9],
                        fill=(245, 239, 224))
    d.ellipse([x0 + 34, y0 + 4, x0 + 42, y0 + 12], fill=(160, 160, 160))
    d.ellipse([x0 + 40, y0 + 8, x0 + 48, y0 + 16], fill=(160, 160, 160))
    d.ellipse([x0 + 30, y0 + 10, x0 + 38, y0 + 18], fill=(190, 190, 190))

def icon_jets(d, x0, y0):
    d.polygon([(x0 + 2, y0 + 44), (x0 + 48, y0 + 38), (x0 + 48, y0 + 44), (x0 + 2, y0 + 50)], fill=(90, 90, 90))
    for t in (x0 + 8, x0 + 26):
        d.polygon([(t, y0 + 14), (t + 12, y0 + 20), (t + 2, y0 + 22), (t - 2, y0 + 18)], fill=INK)
        d.polygon([(t + 4, y0 + 20), (t + 8, y0 + 26), (t + 10, y0 + 20)], fill=INK)
    d.polygon([(x0 + 40, y0 + 4), (x0 + 43, y0 + 10), (x0 + 46, y0 + 4), (x0 + 43, y0 + 2)], fill=(255, 140, 0))

def icon_mall(d, x0, y0):
    d.rectangle([x0 + 4, y0 + 18, x0 + 46, y0 + 48], fill=INK)
    d.rectangle([x0 + 8, y0 + 24, x0 + 42, y0 + 34], fill=(140, 190, 220))
    d.line([x0 + 19, y0 + 24, x0 + 19, y0 + 34], fill=INK, width=1)
    d.line([x0 + 30, y0 + 24, x0 + 30, y0 + 34], fill=INK, width=1)
    d.rectangle([x0 + 20, y0 + 38, x0 + 30, y0 + 48], fill=(245, 239, 224))
    d.polygon([(x0 + 22, y0 + 6), (x0 + 18, y0 + 14), (x0 + 22, y0 + 18), (x0 + 26, y0 + 12),
               (x0 + 30, y0 + 16), (x0 + 28, y0 + 8)], fill=(255, 140, 0))

def icon_tariffs(d, x0, y0):
    d.ellipse([x0 + 2, y0 + 4, x0 + 30, y0 + 32], outline=INK, width=2)
    d.line([x0 + 16, y0 + 4, x0 + 16, y0 + 32], fill=INK, width=1)
    d.ellipse([x0 + 9, y0 + 4, x0 + 23, y0 + 32], outline=INK, width=1)
    d.line([x0 + 2, y0 + 18, x0 + 30, y0 + 18], fill=INK, width=1)
    d.rectangle([x0 + 32, y0 + 8, x0 + 49, y0 + 24], fill=RED)
    d.text((x0 + 35, y0 + 10), "%", font=SANS_B(13), fill=(255, 255, 255))
    d.rectangle([x0 + 32, y0 + 30, x0 + 49, y0 + 46], fill=INK)
    d.text((x0 + 35, y0 + 32), "%", font=SANS_B(13), fill=(255, 255, 255))

def icon_bank(d, x0, y0):
    d.polygon([(x0 + 4, y0 + 18), (x0 + 25, y0 + 6), (x0 + 46, y0 + 18)], fill=INK)
    for cx in (x0 + 10, x0 + 22, x0 + 34):
        d.rectangle([cx, y0 + 22, cx + 4, y0 + 40], fill=INK)
    d.rectangle([x0 + 4, y0 + 42, x0 + 46, y0 + 46], fill=INK)
    d.line([x0 + 4, y0 + 12, x0 + 14, y0 + 4, x0 + 24, y0 + 10, x0 + 34, y0 + 2],
           fill=GREEN, width=2)
    d.polygon([(x0 + 34, y0 + 2), (x0 + 30, y0 + 2), (x0 + 34, y0 + 6)], fill=GREEN)

def icon_space(d, x0, y0):
    d.rectangle([x0, y0, x0 + 50, y0 + 50], fill=(20, 30, 60))
    for sx, sy in ((x0 + 6, y0 + 8), (x0 + 42, y0 + 6), (x0 + 10, y0 + 40), (x0 + 44, y0 + 42)):
        d.polygon([(sx, sy - 3), (sx + 1, sy - 1), (sx + 3, sy), (sx + 1, sy + 1),
                   (sx, sy + 3), (sx - 1, sy + 1), (sx - 3, sy), (sx - 1, sy - 1)], fill=(255, 255, 255))
    d.rectangle([x0 + 4, y0 + 22, x0 + 16, y0 + 28], fill=(90, 140, 200))
    d.rectangle([x0 + 34, y0 + 22, x0 + 46, y0 + 28], fill=(90, 140, 200))
    d.rectangle([x0 + 20, y0 + 20, x0 + 30, y0 + 30], fill=(200, 200, 200), outline=INK)
    d.line([x0 + 16, y0 + 25, x0 + 20, y0 + 25], fill=(200, 200, 200), width=2)
    d.line([x0 + 30, y0 + 25, x0 + 34, y0 + 25], fill=(200, 200, 200), width=2)
    d.ellipse([x0 + 8, y0 + 44, x0 + 42, y0 + 58], fill=(90, 140, 180))

def icon_docs(d, x0, y0):
    d.rectangle([x0 + 10, y0 + 4, x0 + 38, y0 + 44], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x0 + 4, y0 + 10, x0 + 32, y0 + 48], fill=(255, 255, 255), outline=INK, width=1)
    for i, wy in enumerate((y0 + 18, y0 + 24, y0 + 30, y0 + 36)):
        d.line([x0 + 8, wy, x0 + 28, wy], fill=INK, width=1)
    d.ellipse([x0 + 30, y0 + 34, x0 + 46, y0 + 50], fill=RED)
    d.text((x0 + 34, y0 + 38), "!", font=SANS_B(11), fill=(255, 255, 255))

def icon_pact(d, x0, y0):
    d.rectangle([x0 + 2, y0 + 4, x0 + 24, y0 + 18], fill=(0, 60, 140))
    d.polygon([(x0 + 2, y0 + 4), (x0 + 24, y0 + 4), (x0 + 24, y0 + 8), (x0 + 2, y0 + 8)], fill=(255, 255, 255))
    d.ellipse([x0 + 6, y0 + 11, x0 + 9, y0 + 14], fill=(255, 255, 255))
    d.ellipse([x0 + 16, y0 + 12, x0 + 19, y0 + 15], fill=(255, 255, 255))
    d.rectangle([x0 + 26, y0 + 4, x0 + 48, y0 + 18], fill=(0, 120, 60))
    d.polygon([(x0 + 26, y0 + 18), (x0 + 48, y0 + 4), (x0 + 48, y0 + 9), (x0 + 26, y0 + 18)], fill=(255, 210, 0))
    d.rectangle([x0 + 10, y0 + 26, x0 + 40, y0 + 48], fill=(255, 255, 255), outline=INK, width=1)
    for wy in (y0 + 31, y0 + 36, y0 + 41):
        d.line([x0 + 14, wy, x0 + 36, wy], fill=INK, width=1)
    d.ellipse([x0 + 40, y0 + 40, x0 + 48, y0 + 48], fill=RED)

ICONS = {"parade": icon_parade, "candles": icon_candles, "chess": icon_chess,
         "refinery": icon_refinery, "tanker": icon_tanker, "building": icon_building,
         "jets": icon_jets, "mall": icon_mall, "tariffs": icon_tariffs,
         "bank": icon_bank, "space": icon_space, "docs": icon_docs, "pact": icon_pact}

TAG_COLOUR = {"CONFIRMED": GREEN, "REPORTED": RED, "ONGOING": AMBER}

# ---------- layout ----------
W, H = 1024, 1024
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 20  # side margin

# --- masthead ---
d.line([MX, 10, W - MX, 10], fill=INK, width=2)
d.line([MX, 13, W - MX, 13], fill=INK, width=1)
tracked(d, W // 2, 20, "THE WORLD IN ONE DAY", SANS_B(16), INK, tracking=4)
centre(d, W // 2, 42, "Thursday 26 November 2026", SERIF_B(52), INK)
tracked(d, W // 2, 100, "36 STORIES \u00b7 9 REGIONS \u00b7 13 DRAWN SCENES \u00b7 17 SOURCES",
        SANS_B(13), RED, tracking=2)
d.line([MX, 118, W - MX, 118], fill=INK, width=1)
centre(d, W // 2, 126, "Macy's 100th parade postponed by storm \u00b7 US proposes tariffs on 14 partners \u00b7 Gukesh\u2013Sindarov Game 3 tied 1\u20131 in Geneva",
       SERIF_I(15), INK)

# --- region chips ---
cx = MX
for name, n in CHIPS:
    label = f"{name} {n}"
    wch = d.textlength(label, font=SANS_B(11)) + 16
    d.rounded_rectangle([cx, 148, cx + wch, 168], radius=10, fill=LIGHT, outline=RULE, width=1)
    d.text((cx + 8, 153), label, font=SANS_B(11), fill=INK)
    cx += wch + 6
d.line([MX, 176, W - MX, 176], fill=INK, width=1)

# --- 13 scenes grid: 3 cols x 5 rows ---
CW, CH, GX, GY = 321, 80, 10, 5
GY0 = 184
for idx, (num, head, deck, src, tag, icon) in enumerate(SCENES):
    r, c = divmod(idx, 3)
    x = MX + c * (CW + GX)
    y = GY0 + r * (CH + GY)
    # number badge + icon box
    d.ellipse([x, y, x + 20, y + 20], fill=RED)
    num_txt = str(num)
    d.text((x + 10 - d.textlength(num_txt, font=SANS_B(11)) / 2, y + 3),
           num_txt, font=SANS_B(11), fill=(255, 255, 255))
    d.rectangle([x, y + 24, x + 50, y + 74], fill=LIGHT, outline=RULE, width=1)
    ICONS[icon](d, x, y + 24)
    tx = x + 58
    tw = CW - 58 - 2
    # headline (bold >=15px; wraps to 2 lines if it cannot fit one)
    hlines = wrap(d, head, SANS_B(15), tw)
    for i, hl in enumerate(hlines):
        d.text((tx, y + 2 + i * 17), hl, font=SANS_B(15), fill=INK)
    deck_y = y + 22 if len(hlines) == 1 else y + 40
    deck_lh = 15 if len(hlines) == 1 else 14
    lines = wrap(d, deck, SANS(12), tw)[:3]
    for i, ln in enumerate(lines):
        d.text((tx, deck_y + i * deck_lh), ln, font=SANS(12), fill=INK)
    print(f"scene {num}: headline lines {len(hlines)}  deck lines: {len(lines)}")
    tag_col = TAG_COLOUR[tag]
    d.text((tx, y + 68), src, font=SANS_B(10), fill=INK)
    d.text((tx + d.textlength(src + "  ", font=SANS_B(10)), y + 68),
           "\u2014 " + tag, font=SANS_B(10), fill=tag_col)
# grid rules
for gx in (MX + CW + GX // 2, MX + 2 * CW + 3 * GX // 2):
    d.line([gx, GY0, gx, GY0 + 5 * CH + 4 * GY], fill=RULE, width=1)
for ry in range(1, 5):
    yy = GY0 + ry * CH + (ry - 1) * GY + GY // 2
    d.line([MX, yy, W - MX, yy], fill=RULE, width=1)

# --- AND ALSO: stories 14-36, two columns ---
AY = 612
d.text((MX, AY), "AND ALSO \u2014 STORIES 14\u201336", font=SANS_B(13), fill=INK)
d.line([MX, AY + 18, W - MX, AY + 18], fill=INK, width=1)
for i, (num, city, head, src) in enumerate(ALSO):
    col, row = divmod(i, 12)
    x = MX + col * 492
    y = AY + 24 + row * 13
    line = f"{num}. {city} \u2014 {head} \u2014 {src}"
    lw = d.textlength(line, font=SANS(11))
    if lw > 484:
        print(f"ALSO {num} OVERFLOW: {lw:.0f}")
    d.text((x, y), line, font=SANS(11), fill=INK)

# --- bottom band ---
BY = 796
BH = 192
# map panel
d.rectangle([MX, BY, MX + 470, BY + BH], outline=INK, width=1)
d.text((MX + 8, BY + 5), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
sea = (MX + 6, BY + 24, MX + 464, BY + BH - 6)
d.rectangle(sea, fill=SEA)
sx0, sy0, sx1, sy1 = sea
def proj(lon, lat):
    return (sx0 + (lon + 180) / 360 * (sx1 - sx0),
            sy0 + (85 - lat) / 145 * (sy1 - sy0))
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-97, 16), (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-85, 11), (-90, 14), (-95, 16), (-100, 18), (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-140, 60), (-150, 61), (-158, 58), (-165, 60)],
    [(-79, 9), (-72, 11), (-64, 10), (-60, 8), (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35), (-58, -38), (-65, -45), (-68, -52), (-70, -54), (-73, -50), (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -6), (-81, 0), (-80, 5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (16, -28), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70), (25, 71), (30, 70), (36, 68), (34, 63), (30, 62), (30, 66), (34, 60), (38, 56), (36, 52), (33, 48), (30, 46), (28, 44), (23, 40), (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    [(30, 62), (35, 68), (45, 68), (55, 69), (65, 70), (75, 72), (85, 74), (95, 76), (105, 77), (115, 76), (125, 74), (135, 72), (145, 71), (155, 68), (160, 62), (158, 55), (150, 59), (142, 52), (138, 46), (132, 43), (127, 40), (122, 37), (120, 31), (118, 24), (110, 20), (107, 12), (104, 8), (100, 7), (97, 12), (94, 17), (90, 22), (86, 20), (81, 15), (77, 8), (74, 14), (70, 20), (66, 25), (61, 25), (57, 27), (54, 26), (51, 28), (49, 30), (47, 30), (44, 29), (41, 28), (39, 27), (36, 30), (36, 36), (33, 36), (30, 36), (28, 37), (27, 40), (30, 44), (33, 45), (36, 48), (39, 52), (41, 56), (38, 60)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9), (130, -3), (135, -4), (140, -8), (138, -2), (130, 0), (120, 2), (110, 3)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=INK)
for num, (lon, lat, dx, dy) in PINS.items():
    px, py = proj(lon, lat)
    qx, qy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, qx, qy], fill=INK, width=1)
    d.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED, outline=(255, 255, 255), width=1)
    t = str(num)
    d.text((qx - d.textlength(t, font=SANS_B(9)) / 2, qy - 5), t, font=SANS_B(9), fill=(255, 255, 255))

# right column: UTC timeline + date-check
RX, RW = MX + 482, 502
d.rectangle([RX, BY, RX + RW, BY + 90], outline=INK, width=1)
d.text((RX + 8, BY + 5), "THE DAY IN UTC", font=SANS_B(12), fill=INK)
for i, (t, txt) in enumerate(TIMELINE):
    y = BY + 24 + i * 13
    d.text((RX + 8, y), t, font=SANS_B(11), fill=RED)
    d.text((RX + 56, y), txt, font=SANS(11), fill=INK)
DY = BY + 96
d.rectangle([RX, DY, RX + RW, DY + 96], outline=INK, width=1)
d.text((RX + 8, DY + 5), "DATE CHECK \u2014 THESE ARE NOT 26 NOVEMBER", font=SANS_B(12), fill=RED)
for i, (txt, when) in enumerate(DATECHECK):
    y = DY + 24 + i * 12
    d.text((RX + 8, y), "\u2022  " + txt, font=SANS(11), fill=INK)
    wwhen = d.textlength(when, font=SANS_B(11))
    d.text((RX + RW - 8 - wwhen, y), when, font=SANS_B(11), fill=RED)

# --- footer ---
centre(d, W // 2, 994, "Every story here happened or was first reported on Thursday 26 November 2026.",
       SANS(11), INK)
centre(d, W // 2, 1010, SOURCES_LINE, SANS(10), INK)

# --- save ---
img.save(OUT)
size = os.path.getsize(OUT)
print("RGB size:", size)
if size > 1048576:
    pal = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    pal.save(OUT)
    print("palette size:", os.path.getsize(OUT))
print("saved", OUT)
