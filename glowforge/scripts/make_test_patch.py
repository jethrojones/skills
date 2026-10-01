"""Power/speed test patch for the 86x54mm blank. One color per swatch -> one Glowforge setting group each.
Label is knocked out of each engraved swatch (evenodd) so it stays readable."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

import os
F = os.environ.get("FONT_DIR", "./fonts/")  # folder with ArchivoBlack-Regular.ttf, Archivo-Medium.ttf, Archivo-Bold.ttf, JetBrainsMono-Medium.ttf
W, H = 338.6, 212.6

def text_path(s, font, size, x, y, anchor="start"):
    f = TTFont(F + font); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    k = size / f["head"].unitsPerEm
    adv = [gs[cmap[ord(c)]].width * k for c in s]; total = sum(adv)
    cx = x - total / 2 if anchor == "middle" else x
    pen = SVGPathPen(gs)
    for c, a in zip(s, adv):
        gs[cmap[ord(c)]].draw(TransformPen(pen, (k, 0, 0, -k, cx, y))); cx += a
    return pen.getCommands()

# (color, id, speed, power, passes)
TESTS = [("#ff0000", "1", 1000, 50, 1), ("#00aa00", "2", 1000, 60, 1), ("#0000ff", "3", 1000, 70, 1),
         ("#ff00ff", "4", 1000, 80, 1), ("#00aaaa", "5", 800, 70, 1), ("#ff8000", "6", 1000, 60, 2)]
m, gap = 15, 8
sw = (W - 2 * m - 2 * gap) / 3; sh = (H - 2 * m - gap) / 2
body = ""
for i, (col, n, spd, pwr, ps) in enumerate(TESTS):
    r, c = divmod(i, 3)
    x = m + c * (sw + gap); y = m + r * (sh + gap)
    d = f"M{x:.2f},{y:.2f} h{sw:.2f} v{sh:.2f} h{-sw:.2f} Z "
    cx = x + sw / 2
    d += text_path(n, "ArchivoBlack-Regular.ttf", 38, cx, y + 42, "middle")
    d += text_path(f"{spd} / {pwr}", "Archivo-Bold.ttf", 15, cx, y + 62, "middle")
    d += text_path(f"{ps} PASS" if ps == 1 else f"{ps} PASSES", "Archivo-Bold.ttf", 11, cx, y + 77, "middle")
    body += f'<path fill="{col}" fill-rule="evenodd" d="{d}"/>'
open("test_patch.svg", "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="86mm" height="54mm" viewBox="0 0 {W} {H}">{body}</svg>')
