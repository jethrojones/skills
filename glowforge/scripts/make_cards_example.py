"""Optimization Doc metal business cards -> Glowforge-ready SVGs (86x54mm, text outlined)."""
import qrcode
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

import os
F = os.environ.get("FONT_DIR", "./fonts/")  # folder with the Archivo / JetBrains Mono .ttf files
W, H = 338.6, 212.6  # units = 0.01in; card is 86x54mm

def text_path(s, font, size, x, y, anchor="start", track=0):
    f = TTFont(F + font); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm; k = size / upm
    adv = [gs[cmap[ord(c)]].width * k + track for c in s]
    total = sum(adv) - track
    cx = x - (total if anchor == "end" else total / 2 if anchor == "middle" else 0)
    pen = SVGPathPen(gs); 
    for c, a in zip(s, adv):
        tp = TransformPen(pen, (k, 0, 0, -k, cx, y))
        gs[cmap[ord(c)]].draw(tp); cx += a
    return pen.getCommands(), total

def path(d): return f'<path d="{d}"/>'
import re as _re
def _merge(body):
    ds = _re.findall(r'<path[^>]* d="([^"]+)"', body)
    out = []
    for m_ in _re.finditer(r'<path([^>]*?) d="([^"]+)"|<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', body):
        if m_.group(2):
            tr = _re.search(r'translate\(([\d.]+),([\d.]+)\) scale\(([\d.]+)\)', m_.group(1) or "")
            if tr:
                tx_, ty_, sc = map(float, tr.groups())
                nums = _re.findall(r'(-?[\d.]+),(-?[\d.]+)', m_.group(2))
                out.append("M" + " L".join(f"{tx_+float(a)*sc:.3f},{ty_+float(b)*sc:.3f}" for a, b in nums) + " Z")
            else:
                out.append(m_.group(2))
        else:
            x, y, w, h = map(float, m_.groups()[2:])
            out.append(f"M{x},{y} h{w} v{h} h{-w} Z")
    return '<path d="' + " ".join(out) + '"/>'
def svg(body): body = _merge(body); return (f'<svg xmlns="http://www.w3.org/2000/svg" width="86mm" height="54mm" viewBox="0 0 {W} {H}">'
                       f'<g fill="#000" fill-rule="evenodd">{body}</g></svg>')

BOLT = "M0,0 L-14,24 L-4,24 L-9,42 L13,16 L3,16 L9,0 Z"  # lightning bolt

# ---------- FRONT ----------
m = 20
b = ""
d, w1 = text_path("OPTIMIZATION", "ArchivoBlack-Regular.ttf", 29, m, 70); b += path(d)
d, w2 = text_path("DOC", "ArchivoBlack-Regular.ttf", 29, m, 102, track=2); b += path(d)
b += f'<path transform="translate({m + w2 + 24},76) scale(0.9)" d="{BOLT}"/>'
b += f'<rect x="{m}" y="116" width="46" height="3"/>'
d, _ = text_path("Working systems. Smoother for customers.", "Archivo-SemiBold.ttf", 12.5, m, 139); b += path(d)
d, _ = text_path("Better for employees.", "Archivo-SemiBold.ttf", 12.5, m, 154); b += path(d)
d, _ = text_path("JETHRO JONES", "Archivo-Bold.ttf", 12, m, 178, track=1.2); b += path(d)
d, _ = text_path("hello@optimizationdoc.com", "JetBrainsMono-Bold.ttf", 11, W - m, 178, anchor="end"); b += path(d)
d, _ = text_path("optimizationdoc.com", "JetBrainsMono-Bold.ttf", 11, W - m, 194, anchor="end"); b += path(d)
open("front.svg", "w").write(svg(b))

# ---------- BACK ----------
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=0, box_size=1)
q.add_data("https://optimizationdoc.com/next15"); q.make(fit=True)
mat = q.get_matrix(); n = len(mat)
qs = 112            # QR block incl. quiet zone (1.18in)
quiet = 8
cell = (qs - 2 * quiet) / n
qx, qy = W - m - qs, (H - qs) / 2
# bright (engraved) square with dark modules knocked out -> normal QR polarity
from shapely.geometry import box
from shapely.ops import unary_union
mods = unary_union([box(qx + quiet + c * cell, qy + quiet + r * cell, qx + quiet + (c + 1) * cell, qy + quiet + (r + 1) * cell)
                    for r, row in enumerate(mat) for c, v in enumerate(row) if v]).buffer(0.001)
shape = box(qx, qy, qx + qs, qy + qs).difference(mods)
def ring(cs): return "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in cs) + " Z "
d = ""
for g in getattr(shape, "geoms", [shape]):
    d += ring(g.exterior.coords)
    for i in g.interiors: d += ring(i.coords)
b0 = path(d)
VARIANTS = {
    "A": ["Scan to get 15 new deals", "for free."],
    "B": ["Scan to find them.", "Free, takes 2 minutes."],
    "C": ["Scan to meet your next 15", "customers. No cost."],
    "D": ["Scan for the free playbook", "to surface and win them."],
}
tx = m
lines = ["YOUR NEXT 15", "CUSTOMERS ARE", "ALREADY IN", "YOUR BUSINESS."]
for key, sub in VARIANTS.items():
    b = b0; y = 60
    for ln in lines:
        d, _ = text_path(ln, "ArchivoBlack-Regular.ttf", 17.5, tx, y); b += path(d); y += 22
    b += f'<rect x="{tx}" y="{y - 8}" width="46" height="3"/>'
    for i, t in enumerate(sub):
        d, _ = text_path(t, "Archivo-SemiBold.ttf", 12, tx, y + 18 + 15 * i); b += path(d)
    pass
    if key == "C": open("back.svg", "w").write(svg(b))
print("modules:", n)
