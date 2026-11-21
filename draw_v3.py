#!/usr/bin/env python3
"""Render the v3 front page: Saturday 21 November 2026 world news, 1024x1024.

Fresh build for news-image-20261121 v3. Design goal: fix the v2 judge
complaint (density at 300px) by using fewer stories (20) at much larger type,
with a stronger hierarchy: giant date, 6 big lead cards, 14 one-line briefs,
a schematic world map and a DATE CHECK box. All body text >= 15px on the
1024 canvas; headlines 27px bold; date 52px.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Lexend[wght].ttf")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 249, 242)
CARD = (255, 255, 255)
INK = (22, 20, 18)
RED = (200, 16, 46)
MUTED = (92, 88, 80)
LINE = (214, 208, 194)
OCEAN = (218, 231, 243)
LAND = (205, 197, 168)
LANDLINE = (122, 112, 90)
NAVY = (31, 62, 96)
GOLD = (176, 124, 24)
GREEN = (46, 125, 70)

_cache = {}


def F(size, weight=400):
    key = (size, weight)
    if key not in _cache:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_axes([weight])
        _cache[key] = f
    return _cache[key]


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, s, font, max_w):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, xy, s, font, fill, tracking=2):
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


# ---------------------------------------------------------------- stories
LEADS = [
    dict(
        num=1, kicker="1 · WAR — UKRAINE & POLAND",
        head="Russia's 400-drone barrage hits Kyiv",
        deck="110 missiles fired; 8 killed in Kyiv. Two land in Poland.",
        src="Sources: France 24 · CBS · El País",
        icon="missiles", lat=50.45, lon=30.52,
    ),
    dict(
        num=2, kicker="2 · JUSTICE — THE HAGUE",
        head="Myanmar defies World Court ruling",
        deck="Myanmar calls the verdict unfair; UN presses Rohingya return.",
        src="Sources: Reuters · AP",
        icon="scales", lat=52.07, lon=4.30,
    ),
    dict(
        num=3, kicker="3 · CLIMATE — ANTALYA",
        head="COP31 overtime as fossil fuels cut",
        deck="Nearly 200 nations deadlocked; a new draft is due Saturday.",
        src="Sources: AFP · AP · Al Jazeera",
        icon="sun", lat=36.90, lon=30.70,
    ),
    dict(
        num=4, kicker="4 · MARKETS — NEW YORK",
        head="AI rout drags S&P into correction",
        deck="Stocks fall 3.7%; Nasdaq drops 5.3% as chip shares plunge.",
        src="Sources: Horizon · OneTurn",
        icon="chart", lat=40.70, lon=-74.0,
    ),
    dict(
        num=5, kicker="5 · DISASTER — PERU",
        head="Strong quake shakes Peru's Andes",
        deck="Peru's Geophysical Institute puts the tremor at magnitude 6.7.",
        src="Sources: Peru Geophysical Institute",
        icon="quake", lat=-13.5, lon=-72.0,
    ),
    dict(
        num=6, kicker="6 · SPORT — WELLINGTON",
        head="Rahul's hundred makes Test history",
        deck="First Indian opener with Test tons in all four SENA nations.",
        src="Sources: IANS · mykhel",
        icon="cricket", lat=-41.29, lon=174.78,
    ),
]

BRIEFS = [
    ("RIYADH", "3 Houthi missiles downed (AFP)", 24.7, 46.7),
    ("GAZA", "Drone strike wounds 3 (Outlook)", 31.5, 34.45),
    ("BRUSSELS", "Brexit deals signed (Xinhua)", 50.85, 4.35),
    ("USA", "FBI database hacked (Horizon)", 38.9, -77.0),
    ("GERMANY", "Roundup bill $7.25bn (Horizon)", 51.03, 6.98),
    ("LONDON", "Cancer pill helps 1 in 12 (OneTurn)", 51.5, -0.12),
    ("EUROPE", "Gen Z protests in 25 nations (Dawn)", 52.5, 13.4),
    ("LA", "Palisades fire verdict (Horizon)", 34.05, -118.25),
    ("INDONESIA", "Forest fires rage on (Horizon)", -6.2, 106.8),
    ("HORMUZ", "Tanker hit by projectile (UKMTO)", 26.5, 56.3),
    ("BRAZIL", "Storm kills 3, 5,000 homes hit (RTL)", -29.0, -53.8),
    ("INDIA", "11 dead in toxic liquor (Straits Times)", 28.6, 77.2),
    ("PACIFIC", "Cyclone Xavier weakens (RNZ)", -21.2, -159.8),
    ("GOMA", "M23 pullout agreed (Defence Web)", -1.66, 29.22),
]

DATE_CHECK = [
    "World Court ruling — 19 Nov",
    "Anthropic IPO — 19 Nov",
    "GTA VI pre-orders — 19 Nov",
    "Cyclone Akvan — 19 Nov",
    "Voyager 1 — 18 Nov",
]

TALLY = "EUROPE 6 · N AMERICA 3 · S AMERICA 2 · ASIA 6 · AFRICA 1 · OCEANIA 2"

# Rough schematic continent outlines as (lon, lat) points.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-75, 62), (-70, 45), (-75, 35), (-80, 25), (-85, 30),
     (-90, 20), (-95, 18), (-105, 20), (-115, 28), (-125, 40), (-125, 50),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 0), (-70, -10), (-60, -20), (-50, -30), (-40, -25),
     (-35, -10), (-40, 0), (-50, 5), (-60, 8), (-70, 10)],
    [(-10, 36), (0, 38), (10, 38), (20, 40), (28, 36), (30, 42), (20, 45),
     (15, 55), (10, 58), (5, 60), (-5, 58), (-10, 50), (-10, 43)],
    [(-18, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (43, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, -5), (9, 4), (0, 5), (-8, 5),
     (-15, 10)],
    [(30, 36), (40, 38), (50, 40), (60, 45), (70, 50), (80, 55), (90, 60),
     (100, 65), (110, 70), (130, 72), (150, 70), (170, 66), (178, 65),
     (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (120, 30),
     (110, 20), (105, 10), (100, 5), (95, 15), (90, 22), (85, 20),
     (80, 10), (75, 8), (70, 20), (60, 25), (50, 28), (45, 30), (40, 32),
     (35, 36)],
    [(113, -22), (122, -15), (132, -12), (142, -11), (150, -20), (153, -27),
     (150, -37), (140, -38), (130, -32), (120, -34), (113, -30)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (75.0 - lat) / 135.0 * (y1 - y0)
    return (x, y)


def draw_icon(d, kind, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "missiles":
        d.rectangle(box, fill=(24, 32, 54))
        for i, dx in enumerate((-28, 0, 28)):
            d.line([(cx + dx, y1 - 18), (cx + dx - 6, y0 + 30)], fill=(255, 214, 90), width=3)
            d.ellipse([cx + dx - 5, y0 + 22, cx + dx + 5, y0 + 32], fill=(255, 214, 90))
        d.ellipse([cx - 26, cy - 6, cx + 26, cy + 26], fill=(232, 90, 40))
        d.ellipse([cx - 14, cy + 2, cx + 14, cy + 18], fill=(255, 214, 90))
    elif kind == "scales":
        d.rectangle(box, fill=(238, 232, 214))
        d.line([(cx, y0 + 18), (cx, y1 - 22)], fill=NAVY, width=4)
        d.line([(cx - 32, y0 + 30), (cx + 32, y0 + 30)], fill=NAVY, width=4)
        for sx in (cx - 32, cx + 32):
            d.line([(sx, y0 + 30), (sx, y0 + 52)], fill=NAVY, width=3)
            d.polygon([(sx - 14, y0 + 52), (sx + 14, y0 + 52), (sx, y0 + 68)],
                      fill=GOLD)
        d.rectangle([cx - 16, y1 - 22, cx + 16, y1 - 14], fill=NAVY)
    elif kind == "sun":
        d.rectangle(box, fill=(222, 238, 224))
        d.ellipse([cx - 24, y0 + 22, cx + 24, y0 + 70], fill=(240, 164, 40))
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line([(cx + 30 * math.cos(ang), cy - 22 + 30 * math.sin(ang)),
                    (cx + 40 * math.cos(ang), cy - 22 + 40 * math.sin(ang))],
                   fill=(240, 164, 40), width=4)
        d.polygon([(x0 + 8, y1 - 10), (cx, y1 - 52), (x1 - 8, y1 - 10)], fill=GREEN)
    elif kind == "chart":
        d.rectangle(box, fill=(250, 235, 235))
        pts = [(x0 + 10, y0 + 34), (x0 + 30, y0 + 30), (x0 + 48, y0 + 48),
               (x0 + 66, y0 + 44), (x0 + 86, y0 + 78)]
        d.line(pts, fill=RED, width=5, joint="curve")
        d.polygon([(pts[-1][0] - 12, pts[-1][1]), (pts[-1][0] + 12, pts[-1][1]),
                   (pts[-1][0], pts[-1][1] + 16)], fill=RED)
    elif kind == "quake":
        d.rectangle(box, fill=(238, 228, 208))
        d.line([(x0 + 8, y1 - 34), (x1 - 8, y1 - 34)], fill=(120, 84, 40), width=5)
        pts = []
        for i in range(9):
            px = x0 + 8 + i * 10
            py = y0 + 44 + (18 if i % 2 == 0 else -18)
            pts.append((px, py))
        d.line(pts, fill=RED, width=4, joint="curve")
        d.text((x0 + 10, y0 + 6), "6.7", font=F(26, 800), fill=INK)
    elif kind == "cricket":
        d.rectangle(box, fill=(214, 232, 200))
        d.ellipse([cx - 34, cy - 10, cx + 34, cy + 58], fill=(240, 238, 220))
        d.rounded_rectangle([cx - 8, y0 + 22, cx + 8, cy + 10], radius=6,
                            fill=(146, 94, 48))
        d.ellipse([cx + 22, y0 + 18, cx + 40, y0 + 36], fill=RED)
        d.text((x0 + 10, y1 - 34), "100", font=F(24, 800), fill=GREEN)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 26  # side margin
    CW = W - 2 * MX  # 972

    # Top red bar + masthead
    d.rectangle([0, 10, W, 16], fill=RED)
    draw_tracked(d, (MX, 24), "THE WORLD IN ONE PAGE", F(30, 700), INK, tracking=2)
    right = "MAKE.FUN · NEWS-IMAGE"
    d.text((W - MX - text_w(d, right, F(18, 600)), 30), right,
           font=F(18, 600), fill=MUTED)

    # Giant date
    date = "SATURDAY 21 NOVEMBER 2026"
    df = F(52, 800)
    d.text(((W - text_w(d, date, df)) / 2, 58), date, font=df, fill=INK)
    sub = "20 stories  ·  6 world regions  ·  Every story sourced"
    sf = F(20, 500)
    d.text(((W - text_w(d, sub, sf)) / 2, 122), sub, font=sf, fill=MUTED)
    d.line([(MX, 150), (W - MX, 150)], fill=INK, width=2)

    # Lead cards: 2 cols x 3 rows
    gap = 8
    card_w = (CW - gap) // 2
    card_h = 156
    y = 158
    for row in range(3):
        for col in range(2):
            lead = LEADS[row * 2 + col]
            x = MX + col * (card_w + gap)
            d.rounded_rectangle([x, y, x + card_w, y + card_h], radius=6,
                                fill=CARD, outline=LINE, width=1)
            d.rounded_rectangle([x, y, x + 100, y + card_h], radius=6,
                                fill=CARD)
            d.rectangle([x + 94, y + 6, x + 100, y + card_h - 6],
                        fill=LINE)
            draw_icon(d, lead["icon"], (x + 4, y + 4, x + 96, y + card_h - 4))
            tx = x + 112
            tw = card_w - 112 - 12
            d.text((tx, y + 8), lead["kicker"], font=F(18, 700), fill=RED)
            head_lines = wrap(d, lead["head"], F(27, 700), tw)
            assert len(head_lines) <= 2, lead["head"]
            yy = y + 29
            for ln in head_lines:
                d.text((tx, yy), ln, font=F(27, 700), fill=INK)
                yy += 30
            deck_lines = wrap(d, lead["deck"], F(19, 400), tw)
            assert len(deck_lines) <= 2, lead["deck"]
            yy = y + 92
            for ln in deck_lines:
                d.text((tx, yy), ln, font=F(19, 400), fill=INK)
                yy += 22
            d.text((tx, y + 138), lead["src"], font=F(15, 500),
                   fill=MUTED)
        y += card_h + gap
    # y is now 158 + 3*156 + 2*8 = 642

    # Briefs header
    d.text((MX, 650), "ALSO TODAY — 14 MORE STORIES", font=F(21, 700), fill=INK)
    tw = text_w(d, TALLY, F(15, 600))
    d.text((W - MX - tw, 654), TALLY, font=F(15, 600), fill=MUTED)
    d.line([(MX, 678), (W - MX, 678)], fill=LINE, width=1)

    # Briefs: 2 cols x 7 rows, place tag bold
    bf = F(20, 400)
    bfb = F(20, 700)
    bcol_w = (CW - gap) // 2
    by = 686
    for i, (place, text, _lat, _lon) in enumerate(BRIEFS):
        col = i % 2
        r = i // 2
        bx = MX + col * (bcol_w + gap)
        head = "• %s — " % place
        w_head = text_w(d, head, bfb)
        w_rest = text_w(d, text, bf)
        assert w_head + w_rest <= bcol_w, (head + text, w_head + w_rest)
        yy = by + r * 27
        d.text((bx, yy), head, font=bfb, fill=INK)
        d.text((bx + w_head, yy), text, font=bf, fill=INK)
    # briefs end: 686 + 6*27 + 20 = 868

    # Bottom row: schematic map (left) + DATE CHECK (right)
    top = 876
    d.line([(MX, top), (W - MX, top)], fill=INK, width=2)
    map_w = 260
    d.text((MX, top + 8), "WHERE IT HAPPENED", font=F(19, 700), fill=INK)
    map_box = (MX, top + 32, MX + map_w, top + 124)
    d.rounded_rectangle(map_box, radius=4, fill=OCEAN, outline=LINE, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, map_box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    for lead in LEADS:
        px, py = project(lead["lon"], lead["lat"], map_box)
        if lead["num"] == 3:  # Antalya sits close under Kyiv at this scale
            py += 5
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 6), str(lead["num"]), font=F(10, 800),
               fill=(255, 255, 255))
    for _place, _text, lat, lon in BRIEFS:
        px, py = project(lon, lat, map_box)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=MUTED)

    dx = MX + map_w + 16
    dw = W - MX - dx
    d.rounded_rectangle([dx, top + 8, W - MX, top + 124], radius=4,
                        fill=(245, 238, 226), outline=LINE, width=1)
    d.text((dx + 12, top + 14), "DATE CHECK — NOT TODAY", font=F(19, 700),
           fill=RED)
    d.text((dx + 12, top + 38), "First reported before today — excluded above:",
           font=F(16, 500), fill=MUTED)
    col_w = (dw - 24) // 2
    for i, item in enumerate(DATE_CHECK):
        c = i % 2
        r = i // 2
        d.text((dx + 12 + c * col_w, top + 60 + r * 22),
               "• " + item, font=F(19, 400), fill=INK)

    # Footer
    foot = "Sources: Reuters · AP · AFP · BBC · France 24 · CBS · El País · Xinhua · Dawn · IANS · RNZ · UKMTO · OneTurn · Horizon"
    ff = F(15, 500)
    d.text(((W - text_w(d, foot, ff)) / 2, 1006), foot, font=ff, fill=MUTED)

    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("saved", OUT, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])
    print("size ok (<=1048576):", len(data) <= 1048576)
    print("dimensions:", img.size)
    # 300px preview for the readability check (kept out of the repo)
    prev = img.resize((300, 300), Image.LANCZOS)
    prev.save("/tmp/news-v3-300.png")
    print("300px preview: /tmp/news-v3-300.png")


if __name__ == "__main__":
    render()
