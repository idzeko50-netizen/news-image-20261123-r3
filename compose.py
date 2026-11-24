#!/usr/bin/env python3
"""Draw the news-image-20261123 round-3 entry: a one-page newspaper front
page summing up Monday 23 November 2026 in 30 verified stories.

Written fresh in this session. Every illustration is drawn in code with PIL;
no photographs, no downloaded images. Output: entry/entry.png, 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
INK = (26, 26, 26)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GOLD = (176, 141, 44)
GREY = (110, 105, 92)
LIGHT = (232, 224, 205)
SKY = (174, 214, 233)
GREEN = (46, 125, 50)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_I = lambda s: font("DejaVuSans-Oblique.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")) else SANS(s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text; assert it fits max_lines (shorten copy, never overflow)."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, f"OVERFLOW: {text!r} -> {lines}"
    return lines


def draw_lines(draw, lines, fnt, x, y, fill=INK, leading=None, align="left",
                box_w=None):
    lh = leading or int(fnt.size * 1.25)
    for i, line in enumerate(lines):
        lx = x
        if align == "center" and box_w is not None:
            lx = x + (box_w - draw.textlength(line, font=fnt)) // 2
        draw.text((lx, y + i * lh), line, font=fnt, fill=fill)
    return y + len(lines) * lh


def panel(draw, x, y, w, h, num=None):
    """Panel outline with a number chip; returns inner box (x, y, w, h)."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2,
                   fill=PAPER)
    if num is not None:
        chip = 22
        draw.rectangle([x, y, x + chip - 1, y + chip - 1], fill=RED)
        draw.text((x + 6, y + 3), str(num), font=SANS_B(13), fill=(255, 255, 255))
    return (x, y, w, h)


def scene_canvas(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


# ---------------------------------------------------------------- scenes
# Each scene draws into a box of size (w, h) and returns the image.

def scene_cop31(w, h):
    img, d = scene_canvas(w, h, (24, 44, 66))
    d.ellipse([w // 2 - 34, 6, w // 2 + 34, 74], fill=(46, 125, 180))
    d.ellipse([w // 2 - 22, 16, w // 2 + 2, 34], fill=(76, 175, 80))
    d.ellipse([w // 2 + 6, 40, w // 2 + 26, 58], fill=(76, 175, 80))
    d.rectangle([w // 2 - 52, h - 26, w // 2 + 52, h - 8], fill=(252, 248, 238))
    d.line([w // 2 - 52, h - 26, w // 2 + 52, h - 8], fill=RED, width=5)
    d.line([w // 2 - 52, h - 8, w // 2 + 52, h - 26], fill=RED, width=5)
    return img


def scene_nato(w, h):
    img, d = scene_canvas(w, h, SKY)
    d.ellipse([18, 8, 62, 26], fill=(255, 255, 255))
    d.ellipse([w - 70, 14, w - 26, 30], fill=(255, 255, 255))
    # AWACS: fuselage + radar dome disc on top + tail fin + wing
    cy = h // 2
    d.ellipse([w // 2 - 30, cy - 30, w // 2 + 30, cy - 14],
              fill=(235, 235, 235), outline=INK)
    d.rounded_rectangle([24, cy - 12, w - 24, cy + 6], radius=8,
                        fill=(215, 215, 215), outline=INK)
    d.polygon([(w - 44, cy - 12), (w - 20, cy - 30), (w - 14, cy - 12)],
              fill=(200, 200, 200), outline=INK)
    d.polygon([(w // 2 - 6, cy + 6), (w // 2 + 22, cy + 6),
               (w // 2 + 8, cy + 22)], fill=(200, 200, 200), outline=INK)
    d.line([0, h - 12, w, h - 12], fill=GREEN, width=6)
    return img


def scene_democrats(w, h):
    img, d = scene_canvas(w, h, (31, 78, 121))
    # Capitol dome
    d.rectangle([w // 2 - 34, h - 34, w // 2 + 34, h - 8], fill=(252, 248, 238))
    d.pieslice([w // 2 - 26, h - 62, w // 2 + 26, h - 22], 180, 360,
               fill=(252, 248, 238))
    d.rectangle([w // 2 - 3, h - 72, w // 2 + 3, h - 60], fill=(252, 248, 238))
    d.text((w // 2 - 26, 4), "258", font=SANS_B(26), fill=(255, 255, 255))
    return img


def scene_markets(w, h):
    img, d = scene_canvas(w, h, (252, 248, 238))
    d.line([8, h - 14, w - 8, h - 14], fill=INK, width=2)
    d.line([8, 8, 8, h - 14], fill=INK, width=2)
    pts = [(14, 26), (w // 4, 40), (w // 2, 22), (3 * w // 4, 58),
           (w - 14, h - 26)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(w - 14, h - 26), (w - 30, h - 30), (w - 22, h - 14)],
              fill=RED)
    d.line([(w // 2, 58), (w - 14, 44)], fill=GREEN, width=3)
    d.polygon([(w - 14, 44), (w - 28, 40), (w - 20, 54)], fill=GREEN)
    return img


def scene_cricket(w, h):
    img, d = scene_canvas(w, h, (120, 180, 90))
    d.rectangle([0, h - 22, w, h], fill=(90, 140, 70))
    d.rectangle([w // 2 - 40, 10, w // 2 + 40, h - 22], fill=(210, 190, 140))
    for dx in (-8, 0, 8):
        d.rectangle([w // 2 + dx - 2, 14, w // 2 + dx + 2, 34], fill=(240, 220, 120))
    d.line([w // 2 - 44, 44, w // 2 + 10, 66], fill=(120, 72, 20), width=7)
    d.ellipse([w // 2 + 22, 60, w // 2 + 34, 72], fill=RED)
    d.text((6, h - 20), "720/9", font=SANS_B(13), fill=(255, 255, 255))
    return img


def scene_mexico(w, h):
    img, d = scene_canvas(w, h, (232, 200, 140))
    d.ellipse([10, h - 18, w - 10, h + 30], fill=(200, 160, 90))
    # badge star
    cx, cy = w // 2, h // 2 - 6
    d.polygon([(cx, cy - 26), (cx + 8, cy - 8), (cx + 26, cy - 6),
               (cx + 12, cy + 6), (cx + 16, cy + 24), (cx, cy + 12),
               (cx - 16, cy + 24), (cx - 12, cy + 6), (cx - 26, cy - 6),
               (cx - 8, cy - 8)], fill=GOLD, outline=INK)
    # handcuffs
    d.ellipse([w // 2 - 44, h - 26, w // 2 - 20, h - 6], outline=INK, width=3)
    d.ellipse([w // 2 + 20, h - 26, w // 2 + 44, h - 6], outline=INK, width=3)
    d.line([w // 2 - 20, h - 16, w // 2 + 20, h - 16], fill=INK, width=3)
    return img

def scene_fifa(w, h):
    img, d = scene_canvas(w, h, (15, 118, 110))
    # football
    cx, cy, r = w // 2, h // 2 - 4, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=2)
    d.polygon([(cx, cy - 12), (cx + 11, cy - 4), (cx + 7, cy + 10),
               (cx - 7, cy + 10), (cx - 11, cy - 4)], fill=INK)
    d.text((6, h - 20), "2035", font=SANS_B(15), fill=(255, 255, 255))
    d.text((w - 52, h - 20), "UK", font=SANS_B(15), fill=(255, 255, 255))
    return img


def scene_fire(w, h):
    img, d = scene_canvas(w, h, (60, 60, 66))
    d.rectangle([14, h - 40, w - 14, h - 8], fill=(120, 120, 130))
    d.rectangle([w // 2 - 6, h - 52, w // 2 + 6, h - 40], fill=(90, 90, 100))
    for i, fx in enumerate([w // 2 - 26, w // 2, w // 2 + 26]):
        col = [(255, 120, 0), (255, 180, 0), (255, 90, 0)][i]
        d.polygon([(fx - 12, h - 38), (fx, h - 66), (fx + 12, h - 38)],
                  fill=col)
    d.ellipse([w // 2 - 40, 6, w // 2 - 8, 26], fill=(200, 200, 200))
    d.ellipse([w // 2 + 4, 2, w // 2 + 38, 24], fill=(180, 180, 180))
    return img


def scene_nepal(w, h):
    img, d = scene_canvas(w, h, SKY)
    # India flag (left) and Nepal flag (right, crimson pennant)
    d.rectangle([12, 14, 66, 26], fill=(255, 153, 51))
    d.rectangle([12, 26, 66, 38], fill=(255, 255, 255))
    d.rectangle([12, 38, 66, 50], fill=(19, 136, 8))
    d.ellipse([32, 28, 46, 40], outline=BLUE, width=2)
    d.polygon([(w - 66, 12), (w - 66, 52), (w - 14, 52), (w - 40, 34),
               (w - 20, 32)], fill=(220, 20, 60), outline=BLUE)
    # train
    d.rectangle([w // 2 - 40, h - 30, w // 2 + 40, h - 12], fill=RED)
    d.rectangle([w // 2 - 30, h - 26, w // 2 - 12, h - 16], fill=SKY)
    d.rectangle([w // 2 - 6, h - 26, w // 2 + 12, h - 16], fill=SKY)
    d.rectangle([w // 2 + 18, h - 26, w // 2 + 34, h - 16], fill=SKY)
    d.line([0, h - 8, w, h - 8], fill=INK, width=3)
    return img


def scene_belgium(w, h):
    img, d = scene_canvas(w, h, (200, 200, 205))
    d.rectangle([0, h - 16, w, h], fill=(120, 120, 125))
    d.polygon([(20, h // 2), (w - 20, h // 2), (w - 40, h // 2 + 12),
               (40, h // 2 + 12)], fill=(240, 240, 240))
    d.polygon([(w - 40, h // 2), (w - 12, h // 2 - 4), (w - 20, h // 2 + 8)],
              fill=(220, 220, 220))
    # red no-entry circle over the plane
    cx, cy = w // 2 + 16, h // 2 + 4
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=RED, width=5)
    d.line([cx - 17, cy - 17, cx + 17, cy + 17], fill=RED, width=5)
    d.text((6, 4), "NO FLIGHTS", font=SANS_B(12), fill=RED)
    return img


def scene_gaza(w, h):
    img, d = scene_canvas(w, h, (24, 64, 96))
    d.rectangle([0, h - 26, w, h], fill=(20, 90, 120))
    # LNG tanker
    d.rectangle([16, h - 52, w - 16, h - 26], fill=(180, 60, 40))
    for i in range(3):
        d.ellipse([30 + i * 30, h - 50, 52 + i * 30, h - 28],
                  fill=(230, 230, 230))
    d.rectangle([w - 34, h - 66, w - 22, h - 52], fill=(200, 200, 200))
    # smoke plume
    d.ellipse([w // 2 - 34, 4, w // 2 - 6, 26], fill=(120, 120, 120))
    d.ellipse([w // 2 - 8, 0, w // 2 + 26, 22], fill=(150, 150, 150))
    return img


def scene_benghazi(w, h):
    img, d = scene_canvas(w, h, (24, 64, 96))
    d.rectangle([0, h - 24, w, h], fill=(20, 90, 120))
    d.rectangle([18, h - 44, w - 18, h - 24], fill=(110, 120, 130))
    d.rectangle([w // 2 - 8, h - 62, w // 2 + 8, h - 44], fill=(90, 100, 110))
    d.polygon([(w // 2 - 16, h - 62), (w // 2 - 16, h - 44),
               (w // 2 + 16, h - 44)], fill=(90, 100, 110))
    for fx in (w // 2 - 22, w // 2 + 4, w // 2 + 26):
        d.polygon([(fx - 10, h - 44), (fx, h - 68), (fx + 10, h - 44)],
                  fill=(255, 140, 0))
    d.ellipse([w - 52, 6, w - 20, 26], fill=(200, 200, 200))
    return img


def scene_tennis(w, h):
    img, d = scene_canvas(w, h, (40, 110, 70))
    d.rectangle([10, 8, w - 10, h - 8], fill=(70, 140, 200), outline=(255, 255, 255),
                width=2)
    d.line([w // 2, 8, w // 2, h - 8], fill=(255, 255, 255), width=2)
    d.line([10, h // 2, w - 10, h // 2], fill=(255, 255, 255), width=2)
    d.ellipse([w // 2 - 24, h // 2 - 24, w // 2 - 4, h // 2 - 4],
              fill=(200, 230, 60), outline=INK)
    d.arc([w // 2 - 24, h // 2 - 24, w // 2 - 4, h // 2 - 4], 300, 60,
          fill=INK, width=2)
    d.ellipse([w // 2 + 12, h - 30, w // 2 + 30, h - 12], fill=(200, 230, 60),
              outline=INK)
    return img


SCENES = [scene_cop31, scene_nato, scene_democrats, scene_markets,
          scene_cricket, scene_mexico, scene_fifa, scene_fire,
          scene_nepal, scene_belgium, scene_gaza, scene_benghazi,
          scene_tennis]

FEATURED = [
    ("COP31 collapses — no deal",
     "Antalya talks end with no fossil-fuel deal; 200 nations fail to agree."),
    ("NATO sends AWACS to Poland",
     "Council meets today; radar plane to watch skies after 3 Russian missiles."),
    ("Democrats take 258 seats",
     "Biggest House majority since 1992; NC recount flips Foxx seat."),
    ("Markets rout, then bounce",
     "S&P −8.6% in a week; Bitcoin under $60k."),
    ("India 720/9 — Test drawn",
     "Record total in NZ; NZ bat out 239/5, drawn."),
    ("'El Chapo Isidro' captured",
     "FBI top-10 fugitive held; 11 killed in raid."),
    ("UK to host 2035 World Cup",
     "UK hosts women's 2035; USA group gets 2031."),
    ("24 dead in factory fire",
     "Candy plant blaze; ~30 still missing."),
    ("Modi meets Nepal's Shah",
     "₹15,000-crore package; 8 pacts; new train."),
    ("Belgium strike grounds flights",
     "Flights off 07:00–21:00; 404 cancelled."),
    ("Strikes kill 8 in Gaza",
     "LNG carrier Al Mayeda hit; no crew hurt."),
    ("Warship ablaze at Benghazi",
     "Drone hits Russian corvette Merkury."),
    ("Alcaraz wins ATP Finals",
     "Beats Zverev 6–2, 7–6 in Turin."),
]

INDEX = [
    "Poland: all 3 were Russian Kh-101 missiles",
    "Trump warns of Iran strikes after New Year",
    "Kyiv-region strike kills 3; boy, 7, survives",
    "Sparta II towed after Baltic drone attack",
    "Iran claims 2 US drones downed; US denies",
    "Iran calls UK Navy, RAF terrorist groups",
    "Netanyahu–Eisenkot unity talks collapse",
    "Settler arson hits 5 West Bank villages",
    "Yemen strikes kill 5, injure 18",
    "India inflows hit record $13bn in Nov",
    "Delta fault delays 1,000+ flights",
    "Verstappen wins Las Vegas GP",
    "Miley Cyrus announces her marriage",
    "Manchester arena evacuated, tear gas fear",
    "Liverpool beat 10-man Man Utd",
    "Sudan drones kill 5 children in Khartoum",
    "South Sudan camp attack kills 21",
]

NUMBERS = [
    ("258", "Dem House seats"),
    ("3", "missiles in Poland"),
    ("24", "dead, Indonesia fire"),
    ("720/9", "India's Test total"),
    ("$13bn", "India inflows in Nov"),
    ("404", "flights cut, Brussels"),
]

REGIONS = [("Europe", 9, (31, 78, 121)), ("Americas", 5, (179, 38, 30)),
           ("Asia", 3, (176, 141, 44)), ("Middle East", 7, (15, 118, 110)),
           ("Africa", 3, (120, 72, 20)), ("Oceania", 1, (90, 90, 150)),
           ("Global", 2, (110, 105, 92))]

# Map pins: (lon, lat) for the 13 featured stories.
# COP31 is in Antalya, Türkiye (31E); markets is global, pinned mid-Atlantic.
PINS = [(31, 37), (19, 52), (-77, 39), (-30, 25), (175, -41), (-105, 24),
        (-1, 52), (106, -6), (78, 28), (4, 51), (35, 31), (20, 32),
        (7, 45)]
# Display offsets (dx, dy) in px to un-crowd the Europe/Mediterranean pins.
PIN_OFF = {1: (12, -12), 2: (-16, -12), 4: (0, 0), 7: (-18, 4),
           10: (2, -16), 11: (14, 12), 12: (-14, 12), 13: (16, -8)}


# ---------------------------------------------------------------- layout
def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2,
                   fill=(214, 232, 240))
    title = "WHERE IT HAPPENED — 13 FEATURED STORIES"
    draw.text((x + 6, y + 4), title, font=SANS_B(11), fill=INK)
    mx, my, mw, mh = x + 4, y + 22, w - 8, h - 26
    # Rough continents (equirectangular blobs).
    conts = [
        [(0.05, 0.15), (0.28, 0.12), (0.30, 0.38), (0.18, 0.42),
         (0.12, 0.55), (0.06, 0.40)],  # N America
        [(0.24, 0.58), (0.33, 0.56), (0.36, 0.72), (0.30, 0.88),
         (0.26, 0.72)],  # S America
        [(0.46, 0.14), (0.55, 0.12), (0.56, 0.30), (0.48, 0.34)],  # Europe
        [(0.47, 0.36), (0.57, 0.34), (0.60, 0.52), (0.55, 0.70),
         (0.49, 0.58)],  # Africa
        [(0.58, 0.12), (0.82, 0.10), (0.90, 0.26), (0.86, 0.44),
         (0.70, 0.48), (0.60, 0.34)],  # Asia
        [(0.82, 0.66), (0.92, 0.64), (0.94, 0.76), (0.84, 0.78)],  # Oceania
    ]
    for poly in conts:
        pts = [(mx + fx * mw, my + fy * mh) for fx, fy in poly]
        draw.polygon(pts, fill=(140, 190, 120), outline=(90, 140, 90))
    for i, (lon, lat) in enumerate(PINS, start=1):
        px = mx + (lon + 180) / 360 * mw
        py = my + (90 - lat) / 180 * mh
        dx, dy = PIN_OFF.get(i, (0, 0))
        qx, qy = px + dx, py + dy
        qx = min(max(qx, mx + 9), mx + mw - 9)
        qy = min(max(qy, my + 9), my + mh - 9)
        if (dx, dy) != (0, 0):
            draw.line([px, py, qx, qy], fill=RED, width=1)
        r = 8
        draw.ellipse([qx - r, qy - r, qx + r, qy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((qx - 3, qy - 6), str(i), font=SANS_B(9),
                  fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # Masthead
    d.line([12, 10, 1012, 10], fill=INK, width=2)
    d.text((12, 14), "THE WORLD IN ONE PAGE", font=SANS_B(12), fill=GREY)
    d.text((1012 - d.textlength("30 STORIES · 7 REGIONS", font=SANS_B(12)),
            14), "30 STORIES · 7 REGIONS", font=SANS_B(12), fill=GREY)
    headline = "Monday 23 November 2026"
    hf = SERIF_B(46)
    d.text(((W - d.textlength(headline, font=hf)) // 2, 34), headline,
           font=hf, fill=INK)
    strap = ("Every story below happened or was first reported today, "
             "Monday 23 November 2026.")
    sf = SANS_I(14)
    d.text(((W - d.textlength(strap, font=sf)) // 2, 88), strap, font=sf,
           fill=INK)
    # Number strip
    y0, y1 = 108, 150
    bw = 1000 // 6
    for i, (num, label) in enumerate(NUMBERS):
        x = 12 + i * bw
        d.rectangle([x, y0, x + bw - 6, y1], outline=INK, width=1, fill=PAPER)
        nf = SANS_B(20)
        d.text((x + (bw - 6 - d.textlength(num, font=nf)) // 2, y0 + 2), num,
               font=nf, fill=RED)
        lab = fit_lines(d, label, SANS(11), bw - 16, 1)
        draw_lines(d, lab, SANS(11), x + 8, y0 + 26, fill=INK)
    # Region bar
    ry = 160
    total = sum(n for _, n, _ in REGIONS)
    x = 12
    for name, n, col in REGIONS:
        seg = int(1000 * n / total)
        d.rectangle([x, ry, x + seg - 2, ry + 16], fill=col)
        x += seg
    legend = ("Europe 9  ·  Americas 5  ·  Asia 3  ·  Middle East 7  ·  "
              "Africa 3  ·  Oceania 1  ·  Global 2  —  30 stories")
    lf = SANS(12)
    d.text(((W - d.textlength(legend, font=lf)) // 2, ry + 20), legend,
           font=lf, fill=INK)
    # Large panels: 3 across, y 210..408
    for i in range(3):
        x = 12 + i * 338
        panel(d, x, 210, 326, 198, num=i + 1)
        scene = SCENES[i](326 - 4, 108)
        img.paste(scene, (x + 2, 212))
        head, deck = FEATURED[i]
        hl = fit_lines(d, head, SANS_B(15), 326 - 16, 2)
        draw_lines(d, hl, SANS_B(15), x + 8, 322, fill=INK)
        dl = fit_lines(d, deck, SANS(12), 326 - 16, 2)
        draw_lines(d, dl, SANS(12), x + 8, 322 + len(hl) * 19, fill=INK)
    # Small panels: 5 across x 2 rows
    for row in range(2):
        for col in range(5):
            i = 3 + row * 5 + col
            x = 12 + col * 202
            y = 418 + row * 158
            panel(d, x, y, 192, 148, num=i + 1)
            scene = SCENES[i](192 - 4, 72)
            img.paste(scene, (x + 2, y + 2))
            head, deck = FEATURED[i]
            hl = fit_lines(d, head, SANS_B(12), 192 - 14, 2)
            draw_lines(d, hl, SANS_B(12), x + 7, y + 78, fill=INK)
            dl = fit_lines(d, deck, SANS(12), 192 - 14, 2)
            draw_lines(d, dl, SANS(12), x + 7, y + 78 + len(hl) * 15,
                       fill=INK)
    # Bottom section
    draw_map(d, 12, 734, 348, 168)
    # DATE CHECK box
    d.rectangle([12, 910, 360, 986], outline=RED, width=2, fill=PAPER)
    d.text((20, 916), "DATE CHECK — NOT TODAY:", font=SANS_B(12), fill=RED)
    dc = ["Pete Rose pardon — 19 Nov",
          "Anthropic IPO debut — 19 Nov",
          "Jensen Huang resigns — 12 Nov",
          "Missiles enter Poland — 20 Nov"]
    for j, line in enumerate(dc):
        d.text((20, 934 + j * 13), line, font=SANS(11), fill=INK)
    # Index: 17 items, 2 columns
    d.text((372, 736), "ALSO TODAY — 17 MORE STORIES", font=SANS_B(13),
           fill=INK)
    d.line([372, 756, 1012, 756], fill=INK, width=1)
    col_w = 314
    for k, item in enumerate(INDEX):
        col = 0 if k < 9 else 1
        row = k if k < 9 else k - 9
        x = 372 + col * 326
        y = 764 + row * 25
        num = str(k + 14)
        d.text((x, y), num + ".", font=SANS_B(11), fill=RED)
        lines = fit_lines(d, item, SANS(11), col_w - 26, 1)
        draw_lines(d, lines, SANS(11), x + 26, y, fill=INK)
    # Footer
    d.line([12, 994, 1012, 994], fill=INK, width=1)
    foot = ("Sources: Reuters, AP, BBC, Al Jazeera, The Hindu, Dawn, CNA. "
            "Drawn in code — no photographs.")
    ff = SANS(11)
    d.text(((W - d.textlength(foot, font=ff)) // 2, 1000), foot, font=ff,
           fill=GREY)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build().save(out, "PNG")
    print("wrote", out)
