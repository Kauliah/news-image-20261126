#!/usr/bin/env python3
"""Draw the news-image-20261126 entry: a newspaper front page for Thursday 26 November 2026.

Layout (deliberately NOT the equal 6-panel grid of the 23 Nov entry):
  masthead with the day in huge type, one dominant LEAD story with a drawn
  illustration, a 2x2 grid of medium stories, an ALSO strip, a full-width
  weather banner, and a footer line. All six stories verified against at
  least two independent sources as happening / first reported on 26 Nov 2026.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (28, 32, 48)
NAVY = (28, 43, 74)
MUTED = (90, 92, 102)
RULE = (180, 172, 150)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
PURPLE = (96, 60, 140)
ORANGE = (196, 90, 20)
BLUE = (30, 80, 160)
SLATE = (70, 90, 110)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_eu_emblem(draw, cx, cy, r):
    """EU circle of twelve gold stars on a blue disc."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 130))
    for k in range(12):
        ang = -math.pi / 2 + k * math.pi / 6
        star(draw, cx + 0.72 * r * math.cos(ang), cy + 0.72 * r * math.sin(ang),
             r * 0.13, (255, 204, 0))


def draw_drone(draw, x, y, s, col):
    """Simple quadcopter seen from above."""
    draw.ellipse([x + 0.32 * s, y + 0.30 * s, x + 0.68 * s, y + 0.70 * s], fill=col)
    for dx, dy in [(0, 0), (0.72, 0), (0, 0.72), (0.72, 0.72)]:
        px, py = x + dx * s, y + dy * s
        draw.line([px, py, x + 0.5 * s, y + 0.5 * s], fill=col, width=4)
        draw.ellipse([px - 0.14 * s, py - 0.14 * s, px + 0.14 * s, py + 0.14 * s],
                     outline=col, width=4)


def draw_ship(draw, x, y, s, col):
    """Container ship: hull + stacked boxes."""
    draw.polygon([(x, y + 0.62 * s), (x + s, y + 0.62 * s), (x + 0.86 * s, y + 0.92 * s),
                  (x + 0.14 * s, y + 0.92 * s)], fill=col)
    for i, (bx, by, bw, bh, c) in enumerate([
            (0.12, 0.30, 0.24, 0.28, (200, 60, 40)),
            (0.40, 0.30, 0.24, 0.28, (40, 120, 180)),
            (0.68, 0.30, 0.20, 0.28, (220, 160, 40)),
            (0.26, 0.02, 0.24, 0.26, (60, 140, 90))]):
        draw.rectangle([x + bx * s, y + by * s, x + (bx + bw) * s, y + (by + bh) * s],
                       fill=c, outline=(255, 255, 255), width=2)
    draw.rectangle([x + 0.74 * s, y + 0.05 * s, x + 0.80 * s, y + 0.30 * s], fill=col)


def draw_virus(draw, x, y, s, col):
    cx, cy, r = x + 0.5 * s, y + 0.5 * s, 0.30 * s
    for k in range(10):
        ang = k * math.pi / 5
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + (r + 0.16 * s) * math.cos(ang), cy + (r + 0.16 * s) * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=col, width=5)
        draw.ellipse([x2 - 0.05 * s, y2 - 0.05 * s, x2 + 0.05 * s, y2 + 0.05 * s], fill=col)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    draw.ellipse([cx - 0.10 * s, cy - 0.12 * s, cx + 0.02 * s, cy], fill=(255, 255, 255))
    draw.ellipse([cx + 0.05 * s, cy + 0.04 * s, cx + 0.16 * s, cy + 0.15 * s], fill=(255, 255, 255))


def draw_chip(draw, x, y, s, col):
    draw.rectangle([x + 0.22 * s, y + 0.22 * s, x + 0.78 * s, y + 0.78 * s], fill=col)
    draw.rectangle([x + 0.36 * s, y + 0.36 * s, x + 0.64 * s, y + 0.64 * s],
                   fill=(255, 255, 255))
    for i in range(4):
        t = 0.30 + i * 0.14
        draw.line([x + t * s, y + 0.08 * s, x + t * s, y + 0.22 * s], fill=col, width=4)
        draw.line([x + t * s, y + 0.78 * s, x + t * s, y + 0.92 * s], fill=col, width=4)
        draw.line([x + 0.08 * s, y + t * s, x + 0.22 * s, y + t * s], fill=col, width=4)
        draw.line([x + 0.78 * s, y + t * s, x + 0.92 * s, y + t * s], fill=col, width=4)


def draw_storm(draw, x, y, s, col):
    draw.ellipse([x + 0.05 * s, y + 0.18 * s, x + 0.55 * s, y + 0.62 * s], fill=col)
    draw.ellipse([x + 0.35 * s, y + 0.08 * s, x + 0.90 * s, y + 0.58 * s], fill=col)
    draw.rectangle([x + 0.12 * s, y + 0.45 * s, x + 0.88 * s, y + 0.62 * s], fill=col)
    for i, dx in enumerate([0.22, 0.48, 0.74]):
        draw.line([x + dx * s, y + 0.70 * s, x + (dx - 0.06) * s, y + 0.92 * s],
                  fill=col, width=5)
    draw.polygon([(x + 0.52 * s, y + 0.62 * s), (x + 0.68 * s, y + 0.62 * s),
                  (x + 0.56 * s, y + 0.86 * s), (x + 0.66 * s, y + 0.86 * s),
                  (x + 0.46 * s, y + 1.06 * s)], fill=(255, 190, 0))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 30  # page margin

# ---------- masthead ----------
d.text((W // 2, 26), "THE WORLD IN ONE IMAGE", font=SANS_B(21), fill=MUTED, anchor="mt")
date_f = SERIF_B(66)
d.text((W // 2, 52), "26 NOVEMBER 2026", font=date_f, fill=NAVY, anchor="mt")
d.text((W // 2, 126), "T H U R S D A Y   ·   T H E   D A Y ' S   N E W S   F R O M   E V E R Y   C O N T I N E N T",
       font=SANS_B(16), fill=MUTED, anchor="mt")
d.line([MX, 158, W - MX, 158], fill=INK, width=3)
d.line([MX, 164, W - MX, 164], fill=INK, width=1)

# ---------- LEAD: EU summit ----------
LY = 178
d.rectangle([MX, LY, W - MX, LY + 236], fill=(255, 255, 255), outline=RULE, width=2)
d.text((MX + 18, LY + 12), "LEAD  ·  EUROPE  ·  BRUSSELS", font=SANS_B(17), fill=RED)
lead_head = ["EU SUMMIT ENDS", "IN DEADLOCK"]
y = LY + 40
y = text_block(d, MX + 18, y, lead_head, SERIF_B(46), INK, 52)
lead_body = ("EU leaders fail to agree a \u20ac1.58 trillion budget and a \u20ac45 billion "
             "loan for Ukraine on day one of their Brussels summit. Talks resume Friday.")
y = text_block(d, MX + 18, y + 8, wrap(d, lead_body, SANS(21), 560), SANS(21), (60, 62, 74), 27)
# illustration: EU emblem + summit table
ix, iy = W - MX - 320, LY + 14
d.rounded_rectangle([ix, iy, ix + 302, iy + 208], radius=10, fill=(232, 238, 248), outline=RULE)
draw_eu_emblem(d, ix + 151, iy + 88, 62)
d.text((ix + 151, iy + 168), "27 LEADERS  ·  NO DEAL", font=SANS_B(16), fill=NAVY, anchor="mm")
d.text((ix + 151, iy + 192), "BUDGET 2028\u20132034", font=SANS(14), fill=MUTED, anchor="mm")

# ---------- 2x2 grid of medium stories ----------
GY = LY + 252
CW, CH, GAP = 466, 176, 14
stories = [
    ("MIDDLE EAST  ·  KUWAIT", RED, draw_drone,
     "DRONE ATTACK KILLS",
     "TWO ITALIANS IN KUWAIT",
     "Drones hit an air-defence site, killing two Italian technicians. "
     "Italy and Kuwait blame Iran; Tehran denies it."),
    ("TRADE  ·  WORLD", ORANGE, draw_ship,
     "WORLD PUSHES BACK",
     "ON NEW US TARIFFS",
     "China, the EU and Brazil condemn Washington's new tariffs on 14 "
     "partners over factory overcapacity."),
    ("HEALTH  ·  AFRICA", TEAL, draw_virus,
     "EBOLA PASSES 12,000",
     "CASES IN CONGO",
     "Confirmed cases in eastern DR Congo reach 12,021, with 5,904 dead. "
     "Fighting hampers the response."),
    ("TECH  ·  ASIA", BLUE, draw_chip,
     "NVIDIA HALTS AI SERVER",
     "SHIPMENTS TO 4 STATES",
     "Nvidia tells partners to stop shipping AI servers to Malaysia, "
     "Singapore, Thailand and Indonesia, the FT reports."),
]
for i, (kick, col, icon, h1, h2, body) in enumerate(stories):
    cx = MX + (i % 2) * (CW + GAP)
    cy = GY + (i // 2) * (CH + GAP)
    d.rectangle([cx, cy, cx + CW, cy + CH], fill=(255, 255, 255), outline=RULE, width=2)
    d.rectangle([cx, cy, cx + CW, cy + 5], fill=col)
    icon(d, cx + 14, cy + 26, 58, col)
    d.text((cx + 84, cy + 16), kick, font=SANS_B(15), fill=col)
    y = text_block(d, cx + 84, cy + 38, [h1, h2], SANS_B(25), INK, 30)
    text_block(d, cx + 16, cy + 106,
               wrap(d, body, SANS(17), CW - 32), SANS(17), (60, 62, 74), 22)

# ---------- ALSO strip ----------
AY = GY + 2 * CH + GAP + 8
d.rectangle([MX, AY, W - MX, AY + 44], fill=NAVY)
d.text((MX + 16, AY + 22),
       "ALSO:  Hern\u00e1ndez de Cos picked to lead the ECB  ·  Kim Jong Un urges wider nuclear deployment",
       font=SANS_B(16), fill=(255, 255, 255), anchor="lm")

# ---------- weather banner: Thanksgiving storm ----------
SY = AY + 58
d.rectangle([MX, SY, W - MX, SY + 108], fill=(226, 234, 242), outline=RULE, width=2)
draw_storm(d, MX + 16, SY + 12, 84, SLATE)
d.text((MX + 116, SY + 12), "WEATHER  ·  UNITED STATES", font=SANS_B(15), fill=SLATE)
d.text((MX + 116, SY + 34), "STORM DARKENS THANKSGIVING", font=SANS_B(27), fill=INK)
storm_body = ("A nor'easter batters the US East Coast on Thanksgiving; nearly 800,000 lose power "
              "and the Macy's parade moves to Saturday \u2014 a first in 100 years.")
text_block(d, MX + 116, SY + 68, wrap(d, storm_body, SANS(17), W - 2 * MX - 132),
           SANS(17), (60, 62, 74), 22)

# ---------- footer ----------
FY = SY + 122
d.line([MX, FY, W - MX, FY], fill=RULE, width=1)
d.text((W // 2, FY + 10),
       "Every story above happened or was first reported on Thursday 26 November 2026.",
       font=SANS(16), fill=MUTED, anchor="mt")

img.save("/home/hatch/workspace/makefun/news-image-20261126/entry.png", optimize=True)
print("saved", img.size)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun/news-image-20261126/entry.png"))
