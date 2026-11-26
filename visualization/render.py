#!/usr/bin/env python3
"""Render the four rational witnesses inside a rotating unit cube."""
from itertools import combinations, product
from math import cos, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (664, 418)
COLORS = ["#0e1821", "#132532", "#314b5d", "#eef6fa", "#b2c6d3", "#85dfc3", "#ffc078", "#5f859b"]
HERE = Path(__file__).resolve().parent
VERTICES = list(product((0, 1), repeat=3))
EDGES = [(a, b) for a, b in combinations(VERTICES, 2) if sum(x != y for x, y in zip(a, b)) == 1]
POINTS = [(1/4, 1/4, 1/4), (0, 1/4, 3/4), (3/4, 0, 1/4), (1/4, 3/4, 0)]
LABELS = ["A", "B1", "B2", "B3"]
COORDINATES = ["(1/4, 1/4, 1/4)", "(0, 1/4, 3/4)", "(3/4, 0, 1/4)", "(1/4, 3/4, 0)"]


def font(size, bold=False):
    names = ("Arial Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Arial.ttf", "DejaVuSans.ttf")
    for name in names:
        for root in (Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")):
            path = root / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    raise RuntimeError("Arial or DejaVu Sans is required to render the GIF")


FONTS = {"title": font(32, True), "subtitle": font(19), "tag": font(18, True),
         "x": font(22), "output": font(25, True), "body": font(18), "footer": font(19, True)}


def project(point, angle):
    x, y, z = (u - .5 for u in point)
    x, z = x * cos(angle) + z * sin(angle), -x * sin(angle) + z * cos(angle)
    y, z = y * cos(.42) - z * sin(.42), y * sin(.42) + z * cos(.42)
    scale = 156 * 5 / (5 - z)
    return 208 + x * scale, 225 - y * scale, z


def frame(angle, selected):
    im = Image.new("RGB", SIZE, COLORS[0])
    d = ImageDraw.Draw(im)
    d.text((26, 18), "Four inputs rule out a betting mixture", font=FONTS["title"], fill=COLORS[3])
    d.text((26, 61), "Three independent e-values  ·  Exact four-point certificate", font=FONTS["subtitle"], fill=COLORS[4])
    d.rounded_rectangle((26, 100, 392, 354), radius=17, fill=COLORS[1], outline=COLORS[2])
    d.rounded_rectangle((405, 100, 638, 354), radius=17, fill=COLORS[1], outline=COLORS[2])

    vertices = {point: project(point, angle) for point in VERTICES}
    for a, b in sorted(EDGES, key=lambda edge: vertices[edge[0]][2] + vertices[edge[1]][2]):
        qa, qb = vertices[a], vertices[b]
        color = COLORS[7 if qa[2] + qb[2] > 0 else 2]
        d.line((*qa[:2], *qb[:2]), fill=color, width=2)
    witnesses = [(i, *project(point, angle)) for i, point in enumerate(POINTS)]
    for i, x, y, _ in sorted(witnesses, key=lambda item: item[3]):
        if i == selected:
            continue
        color = COLORS[5 if i == 0 else 6]
        d.ellipse((x-6, y-6, x+6, y+6), fill=COLORS[1], outline=color, width=2)
    i, x, y, _ = witnesses[selected]
    color = COLORS[5 if i == 0 else 6]
    d.ellipse((x-11, y-11, x+11, y+11), fill=COLORS[1], outline=color, width=2)
    d.ellipse((x-6, y-6, x+6, y+6), fill=color)
    d.text((425, 115), f"WITNESS {LABELS[i]}", font=FONTS["tag"], fill=color)
    d.text((425, 153), COORDINATES[i], font=FONTS["x"], fill=COLORS[3])
    d.text((425, 195), f"Merger output {int(i == 0)}", font=FONTS["output"], fill=color)
    if i == 0:
        caption = ("All inputs are below 1.", "Matching 1 forces", "zero first stake.")
    else:
        caption = (f"If x{i} is read first,", "the zero is read for free.", "Positive wealth survives.")
    for j, line in enumerate(caption):
        d.text((425, 249 + 24*j), line, font=FONTS["body"], fill=COLORS[3])
    d.text((26, 373), "Any mixture has maximum error at least 3/52 on these four points.",
           font=FONTS["footer"], fill=COLORS[4])
    return im


def main():
    palette = Image.new("P", (1, 1))
    palette.putpalette([int(c[i:i+2], 16) for c in COLORS for i in (1,3,5)] + [0,0,0]*(256-len(COLORS)))
    frames = [frame(tau*i/48 + pi/8, i//12).quantize(palette=palette, dither=Image.Dither.NONE) for i in range(48)]
    frames[0].save(HERE / "four-input-witnesses.gif", save_all=True, append_images=frames[1:],
                   loop=0, duration=135, disposal=1, optimize=True)


if __name__ == "__main__":
    main()
