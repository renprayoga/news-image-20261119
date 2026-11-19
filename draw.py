#!/usr/bin/env python3
"""Draw entry.png — one image summing up 19 November 2026's world news.

Original artwork drawn from scratch with PIL only. No network, no randomness:
every run produces the same pixels. Canvas is drawn at 2x and downscaled with
LANCZOS for clean edges and text.

Layout (1024 x 1024, all coordinates in final-image pixels, scaled by S):
  header   0..212    date, huge and unmistakable
  hero   228..556    Vice City neon sunset + top-story headline
  rows   576..920    three stories, each with a small drawn picture + label
  footer 936..1008   news sources + also-in-the-news line
"""

import os

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024, 1024          # final size
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---------------------------------------------------------------
NAVY = (10, 26, 46)
NAVY2 = (16, 38, 62)
GOLD = (232, 178, 74)
WHITE = (255, 255, 255)
MIST = (205, 220, 232)
DIM = (148, 168, 186)
RED = (198, 52, 44)
ORANGE = (238, 120, 34)
YELLOW = (250, 196, 70)
SEA = (13, 47, 74)
SKY = (27, 58, 92)
INK = (8, 12, 18)
TEAL = (18, 122, 110)
WINE = (122, 30, 44)
SLATE = (52, 68, 86)
PANEL = (21, 48, 76)
PINK = (238, 90, 160)
PURPLE = (88, 44, 130)
SUNSET = (252, 140, 70)
DUSK = (46, 20, 80)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, int(size * S))


def x(v):
    return int(v * S)


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([x(x0), x(y0), x(x1), x(y1)], fill=fill)


def text_c(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((x(cx) - w / 2, x(y)), s, font=f, fill=fill)


def text_l(d, px, y, s, f, fill):
    d.text((x(px), x(y)), s, font=f, fill=fill)


def shrink_to_fit(d, s, f, max_w):
    """Return (string, font) with the font shrunk until the string fits."""
    size = f.size // S
    while d.textlength(s, font=f) > x(max_w) and size > 10:
        size -= 1
        f = ImageFont.truetype(BOLD, int(size * S))
    return s, f


# --- mini pictures ---------------------------------------------------------

def draw_vice_city(d, x0, y0, x1, y1):
    """Vice City at sunset: gradient sky, big sun, neon skyline, palms."""
    # sunset gradient bands (top purple -> pink -> orange at horizon)
    bands = [(DUSK, 0, 44), (PURPLE, 44, 88), ((150, 60, 130), 88, 128),
             (PINK, 128, 164), (SUNSET, 164, 196), ((252, 190, 110), 196, 224)]
    for col, a, b in bands:
        box(d, x0, y0 + a, x1, y0 + b, col)
    # sea strip at the bottom of the scene
    box(d, x0, y0 + 196, x1, y1, (24, 18, 60))
    # big low sun, top-right, clear of the neon plate
    scx, scy = x0 + 836, y0 + 62
    for r, col in ((62, (252, 170, 120)), (48, (255, 205, 130)),
                   (34, (255, 235, 170))):
        d.ellipse([x(scx - r), x(scy - r), x(scx + r), x(scy + r)], fill=col)
    # skyline silhouettes (dark purple buildings, lit windows)
    skyline = [(0, 150, 70, 224), (70, 110, 130, 224), (130, 160, 190, 224),
               (190, 96, 250, 224), (620, 120, 690, 224), (690, 84, 760, 224),
               (760, 140, 830, 224), (830, 100, 900, 224), (900, 150, 960, 224)]
    for bx0, by, bx1, by1 in skyline:
        box(d, x0 + bx0, y0 + by, x0 + bx1, y0 + by1, (28, 12, 48))
    # lit windows, deterministic grid
    for wx in range(80, 250, 18):
        for wy in (120, 148, 176):
            box(d, x0 + wx, y0 + wy, x0 + wx + 7, y0 + wy + 9, GOLD)
    for wx in range(700, 890, 18):
        for wy in (112, 140, 168):
            box(d, x0 + wx, y0 + wy, x0 + wx + 7, y0 + wy + 9, PINK)
    # neon "VICE CITY" sign band across the middle, on a dark plate
    box(d, x0 + 250, y0 + 96, x0 + 710, y0 + 152, (16, 8, 32))
    box(d, x0 + 250, y0 + 96, x0 + 710, y0 + 100, PINK)
    box(d, x0 + 250, y0 + 148, x0 + 710, y0 + 152, PINK)
    text_c(d, x0 + 480, y0 + 102, "VICE CITY", font(38), (255, 120, 200))
    # palm trees framing the sign, trunks leaning outward
    for px, lean in ((262, -1), (698, 1)):
        tx = x0 + px + 16 * lean
        ty = y0 + 128
        d.line([x(x0 + px), x(y0 + 196), x(tx), x(ty)],
               fill=(20, 10, 36), width=x(7))
        # five fronds fanning from the crown
        for dx, dy in ((-44, -18), (-30, -34), (0, -40), (30, -34), (44, -18)):
            d.line([x(tx), x(ty), x(tx + dx * lean), x(ty + dy)],
                   fill=(24, 110, 66), width=x(5))
    # reflections on the water
    for rx in (300, 380, 460, 540, 620):
        box(d, x0 + rx, y0 + 204, x0 + rx + 34, y0 + 208, (120, 70, 110))
        box(d, x0 + rx + 12, y0 + 214, x0 + rx + 40, y0 + 217, (90, 60, 100))


def draw_flags(d, x0, y0, size):
    """Three flags side by side: USA, China, Russia — the trilateral."""
    box(d, x0, y0, x0 + size, y0 + size, (18, 30, 52))
    # USA flag (left third): red/white stripes + blue canton
    fx, fw = x0 + 4, 30
    for i in range(7):
        box(d, fx, y0 + 18 + i * 11, fx + fw, y0 + 18 + (i + 1) * 11,
            RED if i % 2 == 0 else WHITE)
    box(d, fx, y0 + 18, fx + 14, y0 + 52, (30, 60, 130))
    for sx in (6, 11):
        for sy in (24, 32, 40):
            d.ellipse([x(fx + sx - 1), x(y0 + sy - 1),
                       x(fx + sx + 1), x(y0 + sy + 1)], fill=WHITE)
    # China flag (middle third): red field, gold stars
    fx = x0 + 37
    box(d, fx, y0 + 18, fx + fw, y0 + 95, (206, 30, 30))
    d.ellipse([x(fx + 8), x(y0 + 24), x(fx + 18), x(y0 + 34)], fill=GOLD)
    for vx, vy in ((24, 28), (26, 40), (20, 48)):
        d.ellipse([x(fx + vx - 2), x(y0 + vy - 2),
                   x(fx + vx + 2), x(y0 + vy + 2)], fill=GOLD)
    # Russia flag (right third): white / blue / red tricolour
    fx = x0 + 70
    box(d, fx, y0 + 18, fx + fw, y0 + 44, WHITE)
    box(d, fx, y0 + 44, fx + fw, y0 + 70, (30, 80, 180))
    box(d, fx, y0 + 70, fx + fw, y0 + 95, RED)


def draw_gulf(d, x0, y0, size):
    """Airbase under attack: radar dish, night sky, incoming drones."""
    box(d, x0, y0, x0 + size, y0 + size, (12, 20, 38))
    # night sky dots (stars)
    for sx, sy in ((12, 12), (30, 22), (88, 10), (70, 26), (52, 8), (94, 34)):
        d.ellipse([x(x0 + sx - 1), x(y0 + sy - 1),
                   x(x0 + sx + 1), x(y0 + sy + 1)], fill=MIST)
    # radar sweep arc
    d.arc([x(x0 + 18), x(y0 + 30), x(x0 + 86), x(y0 + 98)], 200, 340,
          fill=(90, 200, 170), width=x(4))
    # radar dish on a mast
    d.line([x(x0 + 52), x(y0 + 96), x(x0 + 52), x(y0 + 66)],
           fill=SLATE, width=x(5))
    d.pieslice([x(x0 + 34), x(y0 + 44), x(x0 + 70), x(y0 + 80)], 200, 340,
               fill=(140, 160, 180))
    # runway + hangar at the bottom
    box(d, x0 + 6, y0 + 96, x0 + 98, y0 + 100, DIM)
    box(d, x0 + 10, y0 + 78, x0 + 34, y0 + 96, SLATE)
    # three incoming drones with red trails
    for dx, dy in ((18, 40), (44, 30), (78, 52)):
        d.line([x(x0 + dx), x(y0 + dy), x(x0 + dx + 16), x(y0 + dy + 8)],
               fill=RED, width=x(3))
        d.ellipse([x(x0 + dx - 3), x(y0 + dy - 3),
                   x(x0 + dx + 3), x(y0 + dy + 3)], fill=(255, 90, 70))


def draw_europe(d, x0, y0, size):
    """EU circle of gold stars on blue, with a gold-blue Ukraine bar."""
    box(d, x0, y0, x0 + size, y0 + size, (20, 50, 130))
    import math
    cx, cy = x0 + size // 2, y0 + 44
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        sx = cx + int(30 * math.cos(ang))
        sy = cy + int(30 * math.sin(ang))
        d.ellipse([x(sx - 3), x(sy - 3), x(sx + 3), x(sy + 3)], fill=GOLD)
    d.ellipse([x(cx - 4), x(cy - 4), x(cx + 4), x(cy + 4)], fill=GOLD)
    # Ukraine blue/yellow bar at the bottom
    box(d, x0 + 14, y0 + 82, x0 + 90, y0 + 90, (40, 110, 200))
    box(d, x0 + 14, y0 + 90, x0 + 90, y0 + 98, (250, 210, 60))


# --- full image ------------------------------------------------------------

def build():
    img = Image.new("RGB", (W * S, H * S), NAVY)
    d = ImageDraw.Draw(img)

    # header
    text_c(d, 512, 26, "THE WORLD IN ONE IMAGE", font(26), GOLD)
    _, df = shrink_to_fit(d, "19 NOVEMBER 2026", font(96), 950)
    text_c(d, 512, 62, "19 NOVEMBER 2026", df, WHITE)
    box(d, 332, 178, 692, 182, GOLD)
    text_c(d, 512, 190, "THURSDAY  •  WHAT HAPPENED TODAY", font(24), MIST)

    # hero: Vice City scene on top, headline band below it
    draw_vice_city(d, 32, 228, 992, 452)
    box(d, 32, 452, 992, 556, NAVY2)
    box(d, 32, 452, 992, 456, GOLD)
    _, hf = shrink_to_fit(d, "GTA VI IS HERE", font(50), 920)
    text_c(d, 512, 466, "GTA VI IS HERE", hf, WHITE)
    text_c(d, 512, 522, "After 13 years, Rockstar's Vice City epic unlocks worldwide",
           font(26, bold=False), MIST)

    # three story rows
    rows = [
        (576, draw_flags, "TRUMP, XI & PUTIN MEET TODAY",
         "First-ever trilateral of the three nuclear powers, at APEC in Shenzhen"),
        (696, draw_gulf, "GULF WAR WIDENS",
         "Iran strikes U.S. bases in Kuwait and Bahrain after U.S. hit Qeshm Island"),
        (816, draw_europe, "EUROPE RALLIES FOR UKRAINE",
         "Allies meet in Berlin; U.S. envoys Witkoff and Kushner attend"),
    ]
    for y, drawer, title, sub in rows:
        box(d, 32, y, 992, y + 104, PANEL)
        drawer(d, 32, y, 104)
        _, tf = shrink_to_fit(d, title, font(36), 820)
        text_l(d, 152, y + 12, title, tf, WHITE)
        _, sf = shrink_to_fit(d, sub, font(24, bold=False), 820)
        text_l(d, 152, y + 58, sub, sf, MIST)

    # footer
    text_c(d, 512, 944,
           "Sources: AP  •  Reuters  •  BBC  •  NASA  •  The Hindu",
           font(21, bold=False), DIM)
    text_c(d, 512, 972,
           "Also: NASA briefs Voyager 1, one light-day away  •  Cyclone Akvan nears India's coast",
           font(21, bold=False), DIM)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
