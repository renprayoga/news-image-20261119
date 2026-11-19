#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news poster as a single 1024x1024 PNG.

Everything here is drawn by hand with Pillow: no downloaded pictures, no
network access, no random numbers. Running this file twice gives the same
bytes both times, because every colour, coordinate and letter is fixed.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (18, 18, 20)
RED = (178, 34, 34)
NAVY = (16, 32, 64)
GOLD = (255, 196, 66)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrapped(draw, text, face, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, y, text, face, colour):
    draw.text((W // 2, y), text, font=face, fill=colour, anchor="mt")


def sunset(draw, x, y, w, h):
    """Paint a Vice City dusk: orange at the top fading to violet below."""
    top = (255, 154, 61)
    mid = (232, 74, 122)
    bottom = (91, 42, 134)
    for row in range(h):
        t = row / max(h - 1, 1)
        if t < 0.55:
            k = t / 0.55
            col = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            col = tuple(int(mid[i] + (bottom[i] - mid[i]) * k) for i in range(3))
        draw.line([(x, y + row), (x + w, y + row)], fill=col)
    # Low sun, pale and glowing.
    draw.ellipse([x + w - 205, y + 28, x + w - 95, y + 138], fill=(255, 236, 170))
    draw.ellipse([x + w - 218, y + 15, x + w - 82, y + 151], outline=(255, 220, 130), width=3)


def skyline(draw, x, y, w, h):
    """A dark city silhouette with lit windows along the hero bottom."""
    base = y + h
    towers = [
        (0, 190, 92, 62), (96, 158, 78, 88), (178, 205, 110, 48),
        (292, 142, 84, 102), (380, 188, 96, 62), (480, 162, 88, 84),
        (572, 200, 104, 52), (680, 150, 80, 96), (764, 186, 92, 62),
        (860, 166, 92, 80),
    ]
    for dx, th, tw, _ in towers:
        draw.rectangle([x + dx, base - th, x + dx + tw, base], fill=(24, 12, 44))
    # A few warm windows, placed on a fixed grid so nothing moves, and only
    # inside a tower so none of them floats in the open sky.
    def inside_tower(gx, gy):
        for dx, th, tw, _ in towers:
            if x + dx <= gx <= x + dx + tw - 8 and base - th <= gy <= base - 10:
                return True
        return False

    for gx in range(x + 14, x + w - 14, 34):
        for gy in range(base - 190, base - 8, 26):
            if (gx * 7 + gy * 13) % 5 == 0 and inside_tower(gx, gy):
                draw.rectangle([gx, gy, gx + 7, gy + 9], fill=(255, 214, 110))


def flag_trio(draw, x, y):
    """Three tiny flags side by side: United States, China, Russia."""
    # United States: stripes with a blue corner.
    draw.rectangle([x, y, x + 52, y + 34], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * 5, x + 52, y + i * 5 + 5], fill=(178, 34, 52))
    draw.rectangle([x, y, x + 22, y + 18], fill=(60, 59, 110))
    # China: red field, one gold star.
    draw.rectangle([x + 60, y, x + 112, y + 34], fill=(222, 41, 16), outline=INK, width=2)
    draw.regular_polygon((x + 72, y + 12, 6), 5, rotation=90, fill=GOLD)
    # Russia: white, blue and red bands.
    draw.rectangle([x + 120, y, x + 172, y + 34], fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([x + 120, y + 11, x + 172, y + 23], fill=(0, 57, 166))
    draw.rectangle([x + 120, y + 23, x + 172, y + 34], fill=(213, 0, 50))


def base_icon(draw, x, y):
    """A dark square holding a radar dish and a star: a military base."""
    draw.rectangle([x, y, x + 56, y + 56], fill=NAVY, outline=INK, width=2)
    draw.ellipse([x + 12, y + 12, x + 44, y + 44], outline=(255, 255, 255), width=3)
    draw.line([(x + 28, y + 28), (x + 44, y + 12)], fill=(255, 255, 255), width=3)
    draw.regular_polygon((x + 28, y + 28, 7), 5, rotation=90, fill=GOLD)


def eu_icon(draw, x, y):
    """A blue square ringed with gold stars: the European Union."""
    draw.rectangle([x, y, x + 56, y + 56], fill=(0, 51, 153), outline=INK, width=2)
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        cx = x + 28 + int(17 * math.cos(a))
        cy = y + 28 + int(17 * math.sin(a))
        draw.regular_polygon((cx, cy, 3), 5, rotation=90, fill=GOLD)


def story_row(draw, y, icon_fn, headline, body):
    icon_fn(draw, 48, y + 8)
    face_h = font(SANS_BOLD, 28)
    face_b = font(SANS, 20)
    draw.text((228, y), headline, font=face_h, fill=INK)
    lines = wrapped(draw, body, face_b, 748)
    for i, line in enumerate(lines):
        draw.text((228, y + 38 + i * 25), line, font=face_b, fill=(52, 52, 56))
    return y + 38 + len(lines) * 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    centred(d, 26, "THE WORLD IN ONE IMAGE", font(SANS_BOLD, 33), RED)
    centred(d, 66, "19 NOVEMBER 2026", font(SERIF_BOLD, 74), INK)
    d.line([(36, 158), (988, 158)], fill=INK, width=3)
    centred(d, 168, "THURSDAY  \u2022  WHAT HAPPENED TODAY", font(SANS_BOLD, 25), (70, 70, 74))

    # --- Hero: GTA VI ---------------------------------------------------
    hx, hy, hw, hh = 36, 206, 952, 296
    sunset(d, hx, hy, hw, hh)
    skyline(d, hx, hy, hw, hh)
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=3)
    # A dark band at the hero bottom keeps the white type readable.
    d.rectangle([hx, hy + 196, hx + hw, hy + hh], fill=(16, 8, 32))
    d.text((hx + 28, hy + 202), "VICE CITY", font=font(SANS_BOLD, 24), fill=GOLD)
    d.text((hx + hw - 28, hy + 202), "PS5  \u2022  XBOX", font=font(SANS_BOLD, 22),
           fill=(255, 255, 255), anchor="ra")
    d.text((hx + 28, hy + 226), "GTA VI IS HERE", font=font(SERIF_BOLD, 48), fill=(255, 255, 255))
    d.text((hx + 28, hy + 274), "After 13 years of waiting \u2014 playable from midnight local time.",
           font=font(SANS, 19), fill=(235, 235, 240))

    # --- Three stories --------------------------------------------------
    y = 518
    y = story_row(d, y, flag_trio,
                  "TRUMP, XI & PUTIN MEET IN SHENZHEN",
                  "First trilateral meeting of the three nuclear powers, at APEC "
                  "in Shenzhen \u2014 nuclear arms, Iran and Ukraine on the agenda. "
                  "No outcome yet.")
    d.line([(36, y + 10), (988, y + 10)], fill=(190, 184, 170), width=2)
    y = story_row(d, y + 20, base_icon,
                  "GULF WAR WIDENS: IRAN HITS US BASES",
                  "Iran hit US bases in Kuwait (Ali Al Salem) and Bahrain, "
                  "answering the US strike on Qeshm Island. Intercepted; no "
                  "casualties or damage reported.")
    d.line([(36, y + 10), (988, y + 10)], fill=(190, 184, 170), width=2)
    y = story_row(d, y + 20, eu_icon,
                  "EUROPE UNITES FOR UKRAINE IN BERLIN",
                  "European allies of the Coalition of the Willing met in Berlin, "
                  "with US envoys Witkoff and Kushner.")

    # --- Also strip + footer --------------------------------------------
    ay = 884
    d.rectangle([36, ay, 988, ay + 54], fill=NAVY)
    also = ("ALSO:  NASA briefs on Voyager 1, now one light-day from Earth  \u2022  "
            "Cyclone Akvan nears India\u2019s coast")
    lines = wrapped(d, also, font(SANS_BOLD, 20), 920)
    for i, line in enumerate(lines):
        d.text((52, ay + 6 + i * 26), line, font=font(SANS_BOLD, 20), fill=(255, 255, 255))
    centred(d, 952, "Sources: AP  \u2022  Reuters  \u2022  BBC  \u2022  NASA  \u2022  The Hindu",
            font(SANS, 19), (70, 70, 74))

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
