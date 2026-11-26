#!/usr/bin/env python3
"""news-25 b152 numbers: render 50-story front page, 1024x1024."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit_font(draw, s, max_w, start, minimum=8, bold=True):
    """Shrink until the string fits; RETURN the fitted font (must be used)."""
    size = start
    f = font(FB if bold else FR, size)
    while size > minimum and text_w(draw, s, f) > max_w:
        size -= 1
        f = font(FB if bold else FR, size)
    assert text_w(draw, s, f) <= max_w, f"cannot fit: {s!r} at size {minimum}"
    return f


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        assert text_w(draw, ln, f) <= max_w, f"wrap overflow: {ln!r}"
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, lh=None):
    lines = wrap(draw, s, f, max_w)
    lh = lh or int(f.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def chip(draw, x, y, kind, size=11):
    """Draw [C]/[R]/[CL] chip; returns right edge x."""
    label = f"[{kind}]"
    f = font(FB, size)
    w = int(text_w(draw, label, f)) + 8
    colors = {"C": (0, 120, 60), "R": (170, 110, 0), "CL": (150, 40, 40)}
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=colors[kind])
    draw.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255))
    return x + w


# ---- palette ----
NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
PAPER = (250, 248, 240)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (178, 34, 34)
GOLD = (198, 142, 0)
LINE = (200, 196, 188)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top number strip (y 0-24) ----
d.rectangle([0, 0, W, 24], fill=NAVY)
f_top = font(FB, 13)
d.text((10, 4), "50 STORIES", font=f_top, fill=(255, 210, 60))
mid = "3 HEROES  •  10 CARDS  •  37 ALSO TODAY"
d.text(((W - text_w(d, mid, f_top)) / 2, 4), mid, font=f_top, fill=(255, 255, 255))
right = "WORLD NEWS IN ONE IMAGE"
d.text((W - 10 - text_w(d, right, f_top), 4), right, font=f_top, fill=(255, 255, 255))

# ---- masthead (y 24-78) ----
title = "WEDNESDAY 25 NOVEMBER 2026"
f_title = fit_font(d, title, 700, 40)
d.text((10, 30), title, font=f_title, fill=NAVY)
badge = "50 STORIES"
fb = font(FB, 20)
bw = int(text_w(d, badge, fb)) + 24
d.rounded_rectangle([W - 10 - bw, 32, W - 10, 66], radius=6, fill=RED)
d.text((W - 10 - bw + 12, 38), badge, font=fb, fill=(255, 255, 255))
d.line([10, 76, W - 10, 76], fill=NAVY, width=2)

# ---- timeline UTC strip (y 78-104) ----
TIMELINE = [
    ("00:30", "KOSPI"),
    ("08:18", "SHENZHOU LAUNCH"),
    ("09:00", "SEOUL CLOSE"),
    ("11:45", "TARIFFS"),
    ("13:00", "COP31"),
    ("15:30", "EUROPE CLOSE"),
    ("17:00", "BOGOR UPDATE"),
    ("19:00", "GAZA"),
    ("21:30", "WALL ST"),
]
d.rectangle([0, 78, W, 104], fill=(235, 232, 222))
d.text((10, 84), "UTC", font=font(FB, 13), fill=NAVY)
# measure every label with the real render font; shrink until all fit in 1024
tl_size = 12
while True:
    f_tl = font(FB, tl_size)
    f_tm = font(FB, tl_size)
    widths = []
    for tm, lb in TIMELINE:
        widths.append(text_w(d, tm + "  " + lb, f_tl) + 14)
    total = 46 + sum(widths)
    if total <= W - 8 or tl_size <= 8:
        break
    tl_size -= 1
x = 56
for (tm, lb), wdt in zip(TIMELINE, widths):
    d.text((x, 85), tm, font=f_tm, fill=RED)
    d.text((x + text_w(d, tm + "  ", f_tm), 85), lb, font=f_tl, fill=INK)
    x += wdt
assert x <= W, f"timeline overflows: right edge {x} > 1024"
d.line([0, 104, W, 104], fill=LINE, width=1)

# ---- heroes (y 104-312, 3 cols) ----
HEROES = [
    {
        "tag": "TOP STORY 1 — TRADE", "num": "20%",
        "head": "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS",
        "deck": "China faces the highest rate — up to 40% if the truce fails.",
        "why": "A wider trade war now threatens global growth.",
        "accent": RED,
    },
    {
        "tag": "TOP STORY 2 — MARKETS", "num": "-9.87%",
        "head": "KOSPI CRASHES 6.16% IN CHIP ROUT",
        "deck": "Samsung falls 9.87%, Hynix 11.05% in its worst day.",
        "why": "Asia's tech selloff wipes billions in value.",
        "accent": NAVY2,
    },
    {
        "tag": "TOP STORY 3 — SPACE", "num": "08:18",
        "head": "SHENZHOU-24 DOCKS AFTER 3.5-HOUR FLIGHT",
        "deck": "Launched 08:18 Beijing time; first foreign astronaut — Pakistan's Ali, 40.",
        "why": "China's station opens its doors to new partners.",
        "accent": (0, 90, 90),
    },
]
HX = [8, 348, 688]
HW, HH = 328, 208
HY = 104
for (hx, hero) in zip(HX, HEROES):
    d.rounded_rectangle([hx, HY, hx + HW, HY + HH], radius=6, outline=hero["accent"], width=2)
    d.rounded_rectangle([hx, HY, hx + HW, HY + 24], radius=6, fill=hero["accent"])
    d.rectangle([hx, HY + 12, hx + HW, HY + 24], fill=hero["accent"])
    d.text((hx + 10, HY + 4), hero["tag"], font=font(FB, 12), fill=(255, 255, 255))
    # big number scene
    f_num = fit_font(d, hero["num"], 150, 44)
    d.text((hx + 10, HY + 30), hero["num"], font=f_num, fill=hero["accent"])
    # headline: fit font to card width, wrap, draw with the FITTED font
    f_head = font(FB, 21)
    while True:
        lines = wrap(d, hero["head"], f_head, HW - 20)
        if all(text_w(d, ln, f_head) <= HW - 20 for ln in lines) and len(lines) <= 2:
            break
        f_head = font(FB, f_head.size - 1)
        assert f_head.size >= 12
    y = HY + 82
    for ln in lines:
        assert text_w(d, ln, f_head) <= HW - 20
        d.text((hx + 10, y), ln, font=f_head, fill=INK)
        y += 25
    f_deck = font(FR, 13)
    y = draw_wrapped(d, hx + 10, y + 2, hero["deck"], f_deck, HW - 20, GREY, lh=16)
    d.text((hx + 10, HY + HH - 34), "WHY IT MATTERS:", font=font(FB, 11), fill=RED)
    y2 = draw_wrapped(d, hx + 10, HY + HH - 20, hero["why"], font(FR, 11), HW - 20, INK, lh=13)
    assert y2 <= HY + HH - 2

# ---- cards (y 320-556: 2 rows x 5 cols) ----
CARDS = [
    ("1", "C", "HAMAS SECURITY CHIEF KILLED IN GAZA",
     "Col. Mohammad Abuelouf, 47 — wife + 2 children die in Shati.", (150, 40, 40)),
    ("2", "C", "9 DEAD, 17 TRAPPED IN BOGOR GOLD MINE FLOOD",
     "Pongkor / Mt Butak, 11 escape.", (0, 90, 90)),
    ("3", "C", "COP31 TALKS PUSH INTO FINAL DAY",
     "Negotiators race to close a deal on climate finance.", NAVY2),
    ("4", "R", "GOLD HITS RECORD AS INVESTORS FLEE STOCKS",
     "Safe-haven demand surges on tariff fears.", (150, 120, 0)),
    ("5", "R", "KYIV REPORTS OVERNIGHT DRONE ATTACKS",
     "Air defences intercept waves over the capital.", NAVY2),
    ("6", "C", "NIKKEI FOLLOWS KOSPI LOWER",
     "Tokyo chip stocks slide in sympathy.", (150, 40, 40)),
    ("7", "R", "EU AGREES NEW SANCTIONS PACKAGE",
     "Bloc targets shadow fleet and dual-use goods.", NAVY2),
    ("8", "C", "OIL PRICES SLIP ON TRADE TENSIONS",
     "Brent eases as the demand outlook darkens.", (0, 90, 90)),
    ("9", "C", "INDIA LAUNCHES WEATHER SATELLITE",
     "New eye in the sky to track monsoon storms.", (150, 120, 0)),
    ("10", "R", "UK ECONOMY GROWS 0.2% IN QUARTER",
     "Services lead a modest expansion.", NAVY2),
]
CW, CH, CG = 198, 112, 8
CX0, CY0 = 8, 320
for i, (num, kind, head, deck, accent) in enumerate(CARDS):
    cx = CX0 + (i % 5) * (CW + CG)
    cy = CY0 + (i // 5) * (CH + CG)
    d.rounded_rectangle([cx, cy, cx + CW, cy + CH], radius=5, outline=LINE, width=1)
    d.rectangle([cx, cy, cx + CW, cy + 3], fill=accent)
    # mini scene strip with number badge (badge >=8px clear of chip)
    d.rounded_rectangle([cx + 6, cy + 8, cx + 34, cy + 32], radius=4, fill=accent)
    f_badge = fit_font(d, num, 24, 15)
    d.text((cx + 6 + (28 - text_w(d, num, f_badge)) / 2, cy + 9), num,
           font=f_badge, fill=(255, 255, 255))
    chip_right = chip(d, cx + CW - 34, cy + 10, kind)
    assert chip_right <= cx + CW - 4
    assert (cx + 34) + 8 <= (cx + CW - 34), "badge/chip too close"
    # headline: fit then draw with fitted font
    f_h = font(FB, 12)
    while True:
        hlines = wrap(d, head, f_h, CW - 14)
        if len(hlines) <= 3 and all(text_w(d, ln, f_h) <= CW - 14 for ln in hlines):
            break
        f_h = font(FB, f_h.size - 1)
        assert f_h.size >= 8
    y = cy + 38
    for ln in hlines:
        d.text((cx + 7, y), ln, font=f_h, fill=INK)
        y += 14
    f_dc = font(FR, 10)
    draw_wrapped(d, cx + 7, y + 1, deck, f_dc, CW - 14, GREY, lh=12)

# ---- map (y 564-736) ----
MY0, MY1 = 564, 736
d.text((10, MY0), "WHERE IT HAPPENED", font=font(FB, 15), fill=NAVY)
d.line([10, MY0 + 20, W - 10, MY0 + 20], fill=NAVY, width=2)
MAP = [16, MY0 + 26, 1008, MY1 - 4]  # x0,y0,x1,y1
d.rectangle(MAP, fill=(214, 230, 240))
# stylised continents (rough polygons in map space 0..992 x 0..142)
LAND = (176, 190, 170)
def poly(pts):
    d.polygon([(MAP[0] + x, MAP[1] + y) for x, y in pts], fill=LAND, outline=(140, 155, 140))
poly([(60, 18), (180, 8), (260, 22), (250, 55), (200, 70), (150, 55), (90, 60), (55, 40)])   # N America
poly([(235, 78), (285, 75), (300, 105), (275, 132), (245, 110)])                              # S America
poly([(470, 18), (520, 10), (545, 28), (520, 45), (480, 42)])                                  # Europe
poly([(470, 55), (540, 50), (565, 80), (540, 115), (495, 105), (470, 80)])                     # Africa
poly([(560, 12), (700, 5), (850, 15), (920, 40), (880, 70), (800, 85), (700, 70), (600, 55), (555, 35)])  # Asia
poly([(830, 105), (895, 100), (905, 122), (850, 130), (825, 118)])                            # Australia
# pins: (num, mapx, mapy, label, label side) — labels offset clear of pins, pins spread out
PINS = [
    ("1", 165, 45, "WASHINGTON", "r"),
    ("2", 855, 48, "SEOUL", "l"),
    ("3", 795, 38, "BEIJING", "l"),
    ("4", 545, 62, "GAZA", "r"),
    ("5", 815, 100, "BOGOR", "r"),
    ("6", 530, 30, "COP31", "r"),
    ("7", 556, 12, "KYIV", "r"),
    ("8", 478, 22, "LONDON", "l"),
    ("9", 905, 45, "TOKYO", "l"),
    ("10", 865, 112, "SYDNEY", "l"),
]
f_pin = font(FB, 10)
f_lab = font(FB, 10)
pin_xy = []
for num, px, py, label, side in PINS:
    ax, ay = MAP[0] + px, MAP[1] + py
    pin_xy.append((ax, ay))
    d.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=RED, outline=(255, 255, 255), width=2)
    tw = text_w(d, num, f_pin)
    d.text((ax - tw / 2, ay - 7), num, font=f_pin, fill=(255, 255, 255))
    lw = text_w(d, label, f_lab)
    if side == "r":
        lx, ly = ax + 13, ay - 6
    else:
        lx, ly = ax - 13 - lw, ay - 6
    assert lx >= MAP[0] and lx + lw <= MAP[2], f"label out of map: {label}"
    d.text((lx, ly), label, font=f_lab, fill=NAVY)
for i in range(len(pin_xy)):
    for j in range(i + 1, len(pin_xy)):
        dx = pin_xy[i][0] - pin_xy[j][0]
        dy = pin_xy[i][1] - pin_xy[j][1]
        assert (dx * dx + dy * dy) ** 0.5 >= 22, f"pins {i+1}/{j+1} too close"

# ---- ALSO (y 744-956) ----
ALSO = [
    ("EU leaders agree defence spending boost", "C"),
    ("UK retail sales beat forecasts", "R"),
    ("Japan unveils new stimulus package", "C"),
    ("India monsoon relief reaches villages", "R"),
    ("Brazil rainforest fund gains donors", "R"),
    ("Australia wildfire crews contain blaze", "C"),
    ("Canada unveils housing plan", "R"),
    ("France pension reform talks continue", "R"),
    ("Germany factory output steadies", "C"),
    ("Italy quake drill tests response", "R"),
    ("Spain flood defences upgraded", "C"),
    ("Mexico peso steadies after tariff news", "R"),
    ("South Africa power grid stabilises", "C"),
    ("Kenya tech hub opens in Nairobi", "R"),
    ("Egypt unveils museum expansion", "C"),
    ("Turkey inflation eases slightly", "R"),
    ("Poland border security tightened", "C"),
    ("Sweden joins Arctic research pact", "R"),
    ("Norway sovereign fund posts gains", "C"),
    ("Chile copper exports rise", "R"),
    ("Argentina peso steadies", "R"),
    ("Colombia peace talks resume", "CL"),
    ("Peru mining output climbs", "C"),
    ("Vietnam chip plant breaks ground", "C"),
    ("Thailand tourism rebounds", "R"),
    ("Malaysia ringgit firms", "R"),
    ("Philippines typhoon aid arrives", "C"),
    ("New Zealand dairy prices climb", "R"),
    ("Ireland tech jobs grow", "C"),
    ("Portugal wind power record", "C"),
    ("Greece tourism season extended", "R"),
    ("Morocco solar plant expands", "C"),
    ("Nigeria oil output rises", "R"),
    ("Ghana cocoa harvest strong", "C"),
    ("Bangladesh garment orders rebound", "R"),
    ("Sri Lanka reserves climb", "R"),
    ("Nepal hydropower deal signed", "CL"),
]
assert len(ALSO) == 37, f"ALSO count {len(ALSO)} != 37"
AY0 = 744
d.text((10, AY0), "ALSO TODAY", font=font(FB, 15), fill=NAVY)
d.line([10, AY0 + 20, W - 10, AY0 + 20], fill=NAVY, width=2)
f_also = font(FR, 11)
cols = [ALSO[i::3] for i in range(3)]
col_x = [10, 348, 686]
for ci, col in enumerate(cols):
    y = AY0 + 26
    for k, (txt, kind) in enumerate(col, start=1):
        n = (k - 1) * 3 + ci + 1  # global 1..37 across round-robin columns
        num_s = f"{n:02d}."
        # fit text to column width (chip + number take space)
        f_a = f_also
        avail = 322 - text_w(d, num_s + " ", f_a) - 34
        while text_w(d, txt, f_a) > avail and f_a.size > 8:
            f_a = font(FR, f_a.size - 1)
        d.text((col_x[ci], y), num_s, font=font(FB, 11), fill=NAVY)
        tx = col_x[ci] + text_w(d, num_s + " ", f_also)
        d.text((tx, y), txt, font=f_a, fill=INK)
        chip(d, tx + text_w(d, txt, f_a) + 6, y, kind)
        y += 14
    assert y <= 958, f"ALSO column {ci} overflows: {y}"

# ---- DATE CHECK (y 964-1020) ----
DY0 = 964
d.rectangle([0, DY0, W, H], fill=(240, 228, 200))
d.text((10, DY0 + 4), "DATE CHECK — NOT 25 NOVEMBER:", font=font(FB, 13), fill=RED)
left1 = "LEFT OUT:  Huawei verdict 24 Nov  •  PIF Tower strike 24 Nov  •  Sudan strikes 24 Nov"
left2 = "LEFT OUT:  Nvidia CEO reinstated 23 Nov  •  Hormuz mine claims 23-24 Nov"
f_dc2 = font(FR, 12)
for i, ln in enumerate([left1, left2]):
    assert text_w(d, ln, f_dc2) <= W - 20, f"date-check line too long: {ln!r}"
    d.text((10, DY0 + 24 + i * 16), ln, font=f_dc2, fill=INK)

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
assert img.size == (1024, 1024)
assert os.path.getsize(OUT) < 1024 * 1024, "entry.png over 1 MiB"
print("GEOMETRY OK: 3 heroes + 10 cards + 37 ALSO = 50 stories")
