#!/usr/bin/env python3
"""Draw the front page for 25 November 2026 as a 1024x1024 PNG.

Vector art only (PIL primitives), no photographs, no network, no fonts
outside the machine. Run: python3 compose.py  ->  writes entry.png
next to this file. Deterministic: same input, same bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (30, 64, 110)
TEAL = (14, 94, 90)
GOLD = (198, 142, 22)
GREY = (110, 110, 105)
LIGHT = (226, 219, 203)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading, fill=INK):
    return para(draw, x, y, text, fnt, max_w, leading, fill)


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def art_ship(draw, x, y, w, h):
    """Gulf of Finland: grey cargo ship, drone above, orange blast."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    draw.rectangle([x, y, x + w, y + int(h * 0.52)], fill=(58, 90, 128))
    # sun / sky glint
    draw.ellipse([x + w - 52, y + 10, x + w - 18, y + 44], fill=(240, 200, 90))
    # sea
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(38, 74, 110))
    for i, wy in enumerate((0.68, 0.80, 0.92)):
        yy = y + int(h * wy)
        draw.arc([x + 8 + i * 30, yy - 8, x + 58 + i * 30, yy + 8],
                 180, 360, fill=(214, 228, 240), width=3)
    # ship hull + superstructure
    hx, hy = x + int(w * 0.12), y + int(h * 0.52)
    draw.polygon([(hx, hy), (hx + int(w * 0.72), hy),
                  (hx + int(w * 0.64), hy + 26), (hx + 8, hy + 26)],
                 fill=(70, 70, 72))
    draw.rectangle([hx + 18, hy - 22, hx + 70, hy], fill=(200, 200, 195))
    draw.rectangle([hx + 74, hy - 14, hx + 96, hy], fill=(178, 34, 34))
    draw.line([(hx + 40, hy - 22), (hx + 40, hy - 38)], fill=INK, width=3)
    # drone
    dx, dy = x + int(w * 0.66), y + int(h * 0.16)
    draw.line([(dx - 12, dy - 8), (dx + 12, dy + 8)], fill=INK, width=3)
    draw.line([(dx - 12, dy + 8), (dx + 12, dy - 8)], fill=INK, width=3)
    draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
    # blast
    bx, by = x + int(w * 0.30), y + int(h * 0.42)
    for r, col in ((26, (240, 140, 40)), (17, (245, 190, 60)), (9, (255, 235, 150))):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)


def art_globe_crack(draw, x, y, w, h):
    """COP31: globe with a crack, empty deal."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 222))
    cx, cy, r = x + w // 2, y + h // 2 - 4, min(w, h) // 2 - 14
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 160))
    draw.ellipse([cx - r + 14, cy - r + 22, cx - r + 52, cy - r + 52],
                 fill=(86, 150, 80))
    draw.ellipse([cx + 6, cy + 8, cx + r - 8, cy + r - 12], fill=(86, 150, 80))
    draw.ellipse([cx - r + 30, cy + r - 34, cx - r + 62, cy + r - 10],
                 fill=(86, 150, 80))
    # crack
    draw.line([(cx - r + 18, cy - r + 30), (cx - 6, cy - 2),
               (cx + 12, cy + 18), (cx + r - 22, cy + r - 26)],
              fill=(250, 250, 245), width=5)
    # red no-deal slash
    draw.line([(cx - r - 4, cy + r + 2), (cx + r + 4, cy - r - 2)],
              fill=RED, width=7)


def art_skyline_smoke(draw, x, y, w, h):
    """Gaza skyline with smoke plume."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 204))
    # buildings
    heights = [0.62, 0.45, 0.72, 0.52, 0.66]
    bw = w // 5
    for i, hh in enumerate(heights):
        bx = x + i * bw + 3
        by = y + int(h * (1 - hh))
        draw.rectangle([bx, by, bx + bw - 6, y + h], fill=(96, 96, 92))
        for wy in range(by + 8, y + h - 8, 14):
            draw.rectangle([bx + 5, wy, bx + 11, wy + 7], fill=(240, 210, 90))
    # smoke
    sx = x + int(w * 0.62)
    for i, (r, yy) in enumerate(((16, 0.30), (22, 0.20), (28, 0.10))):
        draw.ellipse([sx - r, y + int(h * yy), sx + r, y + int(h * yy) + 2 * r],
                     fill=(150, 148, 142))
    # orange glow at base of plume
    draw.ellipse([sx - 14, y + int(h * 0.42) - 8, sx + 14, y + int(h * 0.42) + 8],
                 fill=(240, 140, 40))


def art_tower(draw, x, y, w, h):
    """Riyadh's tallest tower, drone strike."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    cx = x + w // 2
    # tower: tapered, with spire
    draw.polygon([(cx - 34, y + h), (cx - 16, y + 18),
                  (cx + 16, y + 18), (cx + 34, y + h)], fill=(70, 86, 104))
    draw.line([(cx, y + 18), (cx, y + 4)], fill=INK, width=4)
    for i in range(5):
        yy = y + 34 + i * 16
        draw.line([(cx - 26 + i * 2, yy), (cx + 26 - i * 2, yy)],
                  fill=(214, 226, 238), width=3)
    # small buildings
    draw.rectangle([x + 6, y + h - 34, x + 34, y + h], fill=(96, 96, 92))
    draw.rectangle([x + w - 34, y + h - 26, x + w - 6, y + h], fill=(96, 96, 92))
    # blast near the top
    bx, by = cx + 26, y + 30
    for r, col in ((16, (240, 140, 40)), (10, (245, 190, 60)), (5, (255, 235, 150))):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)


def art_chip(draw, x, y, w, h):
    """Semiconductor chip / trade-secret theft."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 34))
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) - 16
    # pins
    for i in range(4):
        px = cx - s // 2 + 8 + i * (s - 16) // 3
        draw.line([(px, y + 8), (px, cy - s // 2)], fill=(180, 180, 170), width=3)
        draw.line([(px, cy + s // 2), (px, y + h - 8)], fill=(180, 180, 170), width=3)
        py = cy - s // 2 + 8 + i * (s - 16) // 3
        draw.line([(x + 8, py), (cx - s // 2, py)], fill=(180, 180, 170), width=3)
        draw.line([(cx + s // 2, py), (x + w - 8, py)], fill=(180, 180, 170), width=3)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(46, 92, 140), outline=(150, 190, 230), width=3)
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                   fill=(24, 28, 34), outline=(150, 190, 230), width=2)
    # gavel-ish red stamp
    draw.ellipse([cx + s // 2 - 26, cy - s // 2 - 4, cx + s // 2 + 14, cy - s // 2 + 36],
                 outline=RED, width=4)


def art_shanghai(draw, x, y, w, h):
    """Shanghai skyline: Pearl Tower spheres + blocks. Stays inside panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    cx = x + w // 2
    # Pearl Tower
    draw.line([(cx, y + 4), (cx, y + h - 4)], fill=INK, width=4)
    draw.ellipse([cx - 11, y + 12, cx + 11, y + 34], fill=RED)
    draw.ellipse([cx - 17, y + 38, cx + 17, y + 72], fill=RED)
    # blocks
    draw.rectangle([x + 8, y + h - 30, x + 44, y + h], fill=(96, 96, 92))
    draw.rectangle([x + w - 44, y + h - 38, x + w - 8, y + h], fill=(70, 70, 72))
    draw.rectangle([x + 48, y + h - 20, x + 76, y + h], fill=(120, 118, 112))
    # red seal stamp
    draw.rectangle([x + w - 46, y + 8, x + w - 10, y + 44], outline=RED, width=4)
    draw.line([(x + w - 46, y + 8), (x + w - 10, y + 44)], fill=RED, width=4)
    draw.line([(x + w - 10, y + 8), (x + w - 46, y + 44)], fill=RED, width=4)


def art_medal(draw, x, y, w, h):
    """Medal of Freedom on a ribbon."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx = x + w // 2
    # ribbon
    draw.polygon([(cx - 26, y + 4), (cx - 8, y + 4), (cx - 15, y + 30),
                  (cx - 33, y + 30)], fill=(178, 34, 34))
    draw.polygon([(cx + 26, y + 4), (cx + 8, y + 4), (cx + 15, y + 30),
                  (cx + 33, y + 30)], fill=(30, 64, 110))
    # medal
    cy = y + h - 30
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=GOLD,
                 outline=(140, 100, 10), width=3)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(140, 100, 10),
                 width=2)
    # star
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 16 if i % 2 == 0 else 7
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(250, 240, 200))


def story_block(draw, x, y, w, kicker, head, body, art, art_h=84):
    """One column story: art panel, kicker, headline, body text."""
    art(draw, x, y, w, art_h)
    y2 = y + art_h + 6
    draw.text((x, y2), kicker, font=font(F_SANS_BOLD, 16), fill=RED)
    y2 += 22
    y2 = headline(draw, x, y2, head, font(F_SERIF_BOLD, 24), w, 28)
    y2 = para(draw, x, y2 + 3, body, font(F_SANS, 17), w, 21)
    return y2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    # ---- masthead ----
    rule(d, M, 26, W - M, 3)
    d.text((W // 2, 34), "THE WORLD TODAY",
           font=font(F_SERIF_BLACK, 88), fill=INK, anchor="ma")
    d.text((W // 2, 128), "WEDNESDAY 25 NOVEMBER 2026",
           font=font(F_SANS_BOLD, 26), fill=INK, anchor="ma")
    # black date bar
    d.rectangle([M, 164, W - M, 196], fill=INK)
    d.text((W // 2, 170), "14 STORIES  ·  6 REGIONS  ·  THE DAY IN ONE PAGE",
           font=font(F_SANS_BOLD, 20), fill=(247, 242, 231), anchor="ma")
    # ---- lead story ----
    y = 206
    lead_w = 560
    d.text((M, y), "UKRAINE WAR  ·  LEAD", font=font(F_SANS_BOLD, 19), fill=RED)
    y += 28
    y = headline(d, M, y, "KYIV CONFIRMS DRONE HIT ON RUSSIAN SHIP",
                 font(F_SERIF_BLACK, 44), lead_w, 48)
    y = para(d, M, y + 6,
             "Zelenskyy confirms the drone strikes in the Gulf of Finland "
             "and off Libya. Moscow calls them \u201cterrorism\u201d.",
             font(F_SERIF, 20), lead_w, 26)
    ax = M + lead_w + 24
    aw = W - M - ax
    art_ship(d, ax, 206, aw, 150)
    d.text((ax, 206 + 150 + 6), "A Ukrainian sea drone nears a Russian cargo ship.",
           font=font(F_SANS, 15), fill=GREY)
    rule(d, M, 438, W - M, 2)
    # ---- middle row: 3 stories ----
    y = 454
    col_w = (W - 2 * M - 2 * 24) // 3
    xs = [M, M + col_w + 24, M + 2 * (col_w + 24)]
    story_block(d, xs[0], y, col_w,
                "CLIMATE  ·  COP31",
                "CLIMATE TALKS COLLAPSE",
                "No deal in Antalya — producers blocked fossil-fuel language.",
                art_globe_crack)
    story_block(d, xs[1], y, col_w,
                "MIDDLE EAST  ·  GAZA",
                "STRIKE KILLS HAMAS OFFICIAL",
                "At least six die in Gaza as the reported toll reaches 74,746.",
                art_skyline_smoke)
    story_block(d, xs[2], y, col_w,
                "MIDDLE EAST  ·  RIYADH",
                "HOUTHI DRONE HITS RIYADH TOWER",
                "Eleven wounded in the second drone hit on the capital in days.",
                art_tower)
    rule(d, M, 686, W - M, 2)
    # ---- lower row: 3 stories ----
    y = 702
    story_block(d, xs[0], y, col_w,
                "TECH  ·  UNITED STATES",
                "HUAWEI GUILTY OF TRADE THEFT",
                "A US jury convicts the firm, but clears it of racketeering.",
                art_chip)
    story_block(d, xs[1], y, col_w,
                "CHINA  ·  SHANGHAI",
                "SHANGHAI PARTY CHIEF PROBED",
                "Beijing opens a corruption inquiry into Chen Jining.",
                art_shanghai)
    story_block(d, xs[2], y, col_w,
                "WASHINGTON  ·  THANKSGIVING",
                "TRUMP HONOURS GIULIANI",
                "Medal of Freedom for Giuliani — and a turkey pardon too.",
                art_medal)
    # ---- also today strip ----
    d.rectangle([M, 924, W - M, 952], fill=INK)
    d.text((M + 10, 928), "ALSO TODAY",
           font=font(F_SANS_BOLD, 19), fill=(247, 242, 231))
    para(d, M, 958,
         "Nepal quake, magnitude 5.3  ·  US blacklists Singapore chip firm "
         "Megaspeed  ·  Nvidia brings back Jensen Huang as chief executive  ·  "
         "Iran: 74 lashes for singer Parastoo Ahmadi  ·  CIA and ODNI hit by "
         "cyber breach  ·  Sarkozy ordered to stand trial  ·  "
         "UN: 47,000 women killed by partners or family in a year",
         font(F_SANS, 17), W - 2 * M, 21)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
