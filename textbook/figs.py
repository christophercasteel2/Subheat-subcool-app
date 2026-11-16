"""Drawings for the textbook, as SVG text."""
import math

INK = "#1c2440"
GRID = "#c9d3e6"
FILL = "#dfeaf9"
BLUE = "#1f6fb5"
RED = "#c8452f"
GREEN = "#2f8f4e"
GOLD = "#d98a14"
PURPLE = "#7453b8"
PALE = {"blue": "#dfeaf9", "red": "#fbe3de", "green": "#dff2e4", "gold": "#fdf0d2", "purple": "#ebe4f7", "grey": "#eef0f4"}


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="Inter, DejaVu Sans, sans-serif">{body}</svg>')


def T(x, y, s, size=13, fill=INK, anchor="middle", weight="400", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{st}>{s}</text>')


def L(x1, y1, x2, y2, c=INK, w=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} stroke-linecap="round"/>'


def R(x, y, w, h, fill=FILL, stroke=INK, sw=1.6, rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def P(pts, fill=FILL, stroke=INK, sw=1.8):
    return (f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linejoin="round"/>')


def C(x, y, r, fill=FILL, stroke=INK, sw=1.8):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def corner(x, y, dx=1, dy=-1, s=9):
    return f'<path d="M{x + s * dx:.1f} {y:.1f} v{s * dy} h{-s * dx}" fill="none" stroke="{INK}" stroke-width="1.1"/>'


def arrow(x1, y1, x2, y2, c=INK, w=1.6):
    a = math.atan2(y2 - y1, x2 - x1)
    h = 8
    p1 = (x2 - h * math.cos(a - 0.4), y2 - h * math.sin(a - 0.4))
    p2 = (x2 - h * math.cos(a + 0.4), y2 - h * math.sin(a + 0.4))
    return L(x1, y1, x2, y2, c, w) + f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>'


def pill(x, y, s, fill=GOLD, size=12, color="#fff"):
    w = 8 + 7.0 * len(s)
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 11}" width="{w:.1f}" height="20" rx="10" fill="{fill}"/>'
            + T(x, y + 4, s, size, color, weight="600"))


# ---------------------------------------------------------------- numbers

def place_value(digits_whole, digits_dec):
    names_w = ["millions", "hundred thousands", "ten thousands", "thousands", "hundreds", "tens", "ones"]
    names_d = ["tenths", "hundredths", "thousandths", "ten-thousandths"]
    vals_w = ["1,000,000", "100,000", "10,000", "1,000", "100", "10", "1"]
    vals_d = ["0.1", "0.01", "0.001", "0.0001"]
    cw = 54
    nw, nd = len(digits_whole), len(digits_dec)
    w = 40 + cw * (nw + nd) + 30
    b = []
    x0 = 20
    for i, d in enumerate(digits_whole):
        x = x0 + i * cw
        k = 7 - nw + i
        b.append(R(x, 60, cw, 54, PALE["blue"], BLUE, 1.2))
        b.append(T(x + cw / 2, 96, d, 30, INK, weight="700"))
        b.append(T(x + cw / 2, 50, vals_w[k], 10.5 if len(vals_w[k]) < 8 else 9, BLUE, weight="600"))
        b.append(f'<text transform="translate({x + cw / 2 + 4:.0f},126) rotate(60)" font-size="13" fill="{INK}">{names_w[k]}</text>')
    xd = x0 + nw * cw
    b.append(C(xd + 15, 108, 4.5, RED, RED))
    b.append(T(xd + 15, 50, "decimal", 9.5, RED, weight="600"))
    b.append(T(xd + 15, 40, "point", 9.5, RED, weight="600"))
    for i, d in enumerate(digits_dec):
        x = xd + 30 + i * cw
        b.append(R(x, 60, cw, 54, PALE["gold"], GOLD, 1.2))
        b.append(T(x + cw / 2, 96, d, 30, INK, weight="700"))
        b.append(T(x + cw / 2, 50, vals_d[i], 10, "#a36408", weight="600"))
        b.append(f'<text transform="translate({x + cw / 2 + 4:.0f},126) rotate(60)" font-size="13" fill="{INK}">{names_d[i]}</text>')
    b.append(T(x0 + nw * cw / 2, 22, "WHOLE NUMBER PLACES  (each is 10 times the one to its right)", 10.5, BLUE, weight="700"))
    b.append(T(xd + 30 + nd * cw / 2, 22, "DECIMAL PLACES", 10.5, "#a36408", weight="700"))
    return svg(w + 44, 250, "".join(b))


def rounding_line(lo, hi, x, label_lo, label_hi, label_x):
    b = [L(60, 70, 500, 70, INK, 2)]
    for k in range(11):
        xx = 60 + 44 * k
        big = k in (0, 5, 10)
        b.append(L(xx, 70 - (12 if big else 7), xx, 70 + (12 if big else 7), INK, 1.6 if big else 1))
    b.append(T(60, 104, label_lo, 14, BLUE, weight="700"))
    b.append(T(500, 104, label_hi, 14, BLUE, weight="700"))
    b.append(T(280, 104, "halfway", 11, "#666"))
    px = 60 + 440 * (x - lo) / (hi - lo)
    b.append(arrow(px, 22, px, 58, RED, 2))
    b.append(T(px, 16, label_x, 13, RED, weight="700"))
    return svg(560, 116, "".join(b))


def fdp_cycle():
    b = []
    pts = {"FRACTION": (120, 60), "DECIMAL": (480, 60), "PERCENT": (300, 218)}
    for name, (x, y) in pts.items():
        col = {"FRACTION": BLUE, "DECIMAL": GREEN, "PERCENT": RED}[name]
        b.append(R(x - 66, y - 24, 132, 48, "#fff", col, 2.2, 10))
        b.append(T(x, y + 5, name, 14, col, weight="700"))
    b.append(arrow(192, 48, 408, 48, INK))
    b.append(T(300, 38, "divide top by bottom", 12, INK, weight="600"))
    b.append(arrow(408, 74, 192, 74, INK))
    b.append(T(300, 94, "write over 10, 100, 1000 …", 12, INK, weight="600"))
    b.append(T(300, 109, "then reduce", 12, INK, weight="600"))
    b.append(arrow(492, 88, 372, 192, RED))
    b.append(T(452, 146, "point 2 places RIGHT,", 12, RED, anchor="start", weight="700"))
    b.append(T(452, 161, "add %", 12, RED, anchor="start", weight="700"))
    b.append(arrow(336, 192, 456, 88, GREEN))
    b.append(T(374, 146, "point 2 places LEFT,", 12, GREEN, anchor="end", weight="700"))
    b.append(T(374, 161, "drop %", 12, GREEN, anchor="end", weight="700"))
    return svg(620, 250, "".join(b))


def percent_bar(part, whole, pct, labels=("part", "whole")):
    w = 440
    px = w * pct / 100
    b = [R(60, 40, w, 46, "#fff", INK, 1.6, 4), R(60, 40, px, 46, PALE["red"], RED, 1.6, 4)]
    b.append(T(60 + px / 2, 68, f"{labels[0]}: {part}", 13, RED, weight="700"))
    b.append(T(60 + w / 2, 30, f"{labels[1]}: {whole}", 13, INK, weight="700"))
    for k in range(0, 101, 25):
        x = 60 + w * k / 100
        b.append(L(x, 86, x, 96, INK, 1))
        b.append(T(x, 112, f"{k}%", 11))
    b.append(L(60 + px, 86, 60 + px, 104, RED, 1.6))
    b.append(T(60 + px, 128, f"{pct}%", 12.5, RED, weight="700"))
    return svg(560, 138, "".join(b))


def proportion():
    b = [T(150, 52, "PART  (is)", 17, RED, weight="700"), L(70, 64, 230, 64, INK, 2.4),
         T(150, 92, "WHOLE  (of)", 17, BLUE, weight="700"),
         L(240, 44, 332, 86, GOLD, 2, "5 4"), L(240, 86, 332, 44, GOLD, 2, "5 4"),
         C(286, 65, 13, "#fff", "#fff"), T(286, 73, "=", 24, INK, weight="700"),
         T(410, 52, "PERCENT", 17, GREEN, weight="700"), L(340, 64, 480, 64, INK, 2.4),
         T(410, 92, "100", 17, INK, weight="700"),
         T(286, 124, "cross-multiply the diagonal pair, then divide by the number left over", 11.5, "#8a5a00", weight="600")]
    return svg(560, 136, "".join(b))


# ---------------------------------------------------------------- measurement

def stairs(base="m"):
    """the metric stairs with the length, weight and capacity unit on every step"""
    names = [("kilo", "k", "1000"), ("hecto", "h", "100"), ("deka", "da", "10"), ("UNIT", "", "1"),
             ("deci", "d", "0.1"), ("centi", "c", "0.01"), ("milli", "m", "0.001")]
    b = []
    sw, sh, x0, y0 = 84, 34, 26, 44
    bottom = y0 + 6 * sh + sh + 92
    for i, (nm, sym, val) in enumerate(names):
        x, y = x0 + i * sw, y0 + i * sh
        col = BLUE if i != 3 else RED
        b.append(R(x, y + sh, sw, bottom - y - sh, "#f6f8fc", GRID, 1))
        b.append(R(x, y, sw, sh, col, col, 1.4))
        b.append(T(x + sw / 2, y + 15, nm, 13, "#fff", weight="700"))
        b.append(T(x + sw / 2, y + 28, val, 10.5, "#fff", weight="600"))
        for k, (u, c2) in enumerate((("m", BLUE), ("g", GREEN), ("L", PURPLE))):
            b.append(T(x + sw / 2, bottom - 62 + k * 22, f"{sym}{u}", 15, c2, weight="700"))
    b.append(T(x0 - 4, bottom - 62, "", 10))
    for k, (lab, c2) in enumerate((("length", BLUE), ("weight", GREEN), ("capacity", PURPLE))):
        b.append(T(x0 + 7 * sw + 8, bottom - 62 + k * 22, lab, 11, c2, anchor="start", weight="600"))
    b.append(T(x0 + 3.5 * sw + 120, y0 + 20, "each step = one decimal place", 12, "#555", weight="600"))
    ya = bottom + 26
    b.append(arrow(x0 + 10, ya, x0 + 7 * sw - 10, ya, GREEN, 2.4))
    b.append(T(x0 + 3.5 * sw, ya - 8, "DOWN the stairs (toward milli): move the decimal point RIGHT, one place per step", 12, GREEN, weight="700"))
    yb = ya + 34
    b.append(arrow(x0 + 7 * sw - 10, yb, x0 + 10, yb, RED, 2.4))
    b.append(T(x0 + 3.5 * sw, yb - 8, "UP the stairs (toward kilo): move the decimal point LEFT, one place per step", 12, RED, weight="700"))
    return svg(x0 + 7 * sw + 70, yb + 14, "".join(b))


def chain(units, factors, col=BLUE, title=""):
    """units from largest to smallest with the number of the smaller in one of the larger;
    arrows show multiply going to the smaller unit and divide going to the larger"""
    bw, gap, x0, y0 = 104, 96, 20, 52 if title else 40
    b = []
    if title:
        b.append(T(x0, 18, title, 12.5, col, anchor="start", weight="700"))
    for i, u in enumerate(units):
        x = x0 + i * (bw + gap)
        b.append(R(x, y0, bw, 40, "#fff", col, 2.2, 8))
        b.append(T(x + bw / 2, y0 + 26, u, 15, INK, weight="700"))
        if i < len(factors):
            xa, xb = x + bw + 6, x + bw + gap - 6
            b.append(arrow(xa, y0 + 11, xb, y0 + 11, GREEN, 1.8))
            b.append(T((xa + xb) / 2, y0 + 3, f"× {factors[i]}", 12.5, GREEN, weight="700"))
            b.append(arrow(xb, y0 + 29, xa, y0 + 29, RED, 1.8))
            b.append(T((xa + xb) / 2, y0 + 46, f"÷ {factors[i]}", 12.5, RED, weight="700"))
    w = x0 * 2 + len(units) * bw + (len(units) - 1) * gap
    b.append(T(x0, y0 + 68, "larger unit", 10.5, "#666", anchor="start"))
    b.append(T(w - x0, y0 + 68, "smaller unit", 10.5, "#666", anchor="end"))
    return svg(max(w, 320), y0 + 76, "".join(b))


def stack(svgs, gap=8):
    """several drawings one under another, left aligned"""
    import re
    ys, body, w = 0, [], 0
    for sv in svgs:
        ww, hh = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', sv).groups()]
        body.append(f'<g transform="translate(0,{ys})">{sv[sv.index(">") + 1:sv.rindex("</svg>")]}</g>')
        ys += hh + gap
        w = max(w, ww)
    return svg(w, ys - gap, "".join(body))


def ruler(inch_marks=(), mm_marks=()):
    """a 4-inch ruler with a cm scale on top; marks are (letter, sixteenths) and (letter, mm)"""
    x0, w = 30, 500
    per_in = w / 4.0
    per_mm = per_in / 25.4
    b = [R(x0 - 8, 44, w + 16, 96, "#fbefc4", "#b8922a", 1.5, 4)]
    for k in range(0, 102):
        x = x0 + k * per_mm
        if x > x0 + w:
            break
        h = 16 if k % 10 == 0 else (11 if k % 5 == 0 else 6)
        b.append(L(x, 44, x, 44 + h, INK, 1.2 if k % 10 == 0 else 0.8))
        if k % 10 == 0 and k > 0:
            b.append(T(x, 74, str(k // 10), 11.5, INK, weight="600"))
    b.append(T(x0 + 6, 74, "cm", 10, "#7a5c00", anchor="start", weight="600"))
    for k in range(0, 65):
        x = x0 + k * per_in / 16
        h = 26 if k % 16 == 0 else 19 if k % 8 == 0 else 14 if k % 4 == 0 else 10 if k % 2 == 0 else 6
        b.append(L(x, 140 - h, x, 140, INK, 1.3 if k % 16 == 0 else 0.8))
        if k % 16 == 0 and k > 0:
            b.append(T(x, 108, str(k // 16), 13, INK, weight="700"))
    b.append(T(x0 + 6, 108, "in", 10, "#7a5c00", anchor="start", weight="600"))
    for name, s in inch_marks:
        x = x0 + s * per_in / 16
        b.append(arrow(x, 172, x, 144, RED, 1.8))
        b.append(T(x, 188, name, 14, RED, weight="700"))
    for name, mm in mm_marks:
        x = x0 + mm * per_mm
        b.append(arrow(x, 14, x, 40, BLUE, 1.8))
        b.append(T(x, 11, name, 14, BLUE, weight="700"))
    return svg(560, 196, "".join(b))


def inch_zoom():
    """one inch blown up, with the 16 marks named"""
    x0, w = 40, 480
    b = [R(x0 - 10, 30, w + 20, 80, "#fbefc4", "#b8922a", 1.5, 4)]
    names = ["0", "1/16", "1/8", "3/16", "1/4", "5/16", "3/8", "7/16", "1/2", "9/16", "5/8", "11/16", "3/4", "13/16", "7/8",
             "15/16", "1"]
    for k in range(17):
        x = x0 + k * w / 16
        h = 60 if k % 16 == 0 else 48 if k % 8 == 0 else 36 if k % 4 == 0 else 26 if k % 2 == 0 else 16
        col = INK if k % 16 == 0 else RED if k % 8 == 0 else BLUE if k % 4 == 0 else GREEN if k % 2 == 0 else "#666"
        b.append(L(x, 110 - h, x, 110, col, 1.8 if k % 4 == 0 else 1.1))
        b.append(T(x, 128 + (14 if k % 2 else 0), names[k], 10.5 if k % 2 else 11.5, col, weight="600"))
    b.append(T(280, 20, "ONE INCH, enlarged: the longer the mark, the bigger the fraction", 11.5, INK, weight="600"))
    return svg(560, 150, "".join(b))


def gauge(lo, hi, major, minor, value, unit, title="", start=210, sweep=240, size=250):
    """a dial from lo to hi with a numbered mark every `major` and a small mark every `minor`"""
    cx, cy, r = size / 2 + 10, size / 2 + 6, size / 2 - 22
    b = [C(cx, cy, r + 14, "#fff", INK, 2.4), C(cx, cy, r + 9, "#f6f8fc", GRID, 1)]
    n = round((hi - lo) / minor)
    for k in range(n + 1):
        v = lo + k * minor
        a = math.radians(start - sweep * (v - lo) / (hi - lo))
        big = abs((v - lo) / major - round((v - lo) / major)) < 1e-9
        r1 = r - (14 if big else 7)
        b.append(L(cx + r * math.cos(a), cy - r * math.sin(a), cx + r1 * math.cos(a), cy - r1 * math.sin(a), INK, 2 if big else 1))
        if big:
            b.append(T(cx + (r - 28) * math.cos(a), cy - (r - 28) * math.sin(a) + 4, f"{v:g}", 11.5, INK, weight="600"))
    a = math.radians(start - sweep * (value - lo) / (hi - lo))
    b.append(L(cx - 14 * math.cos(a), cy + 14 * math.sin(a), cx + (r - 10) * math.cos(a), cy - (r - 10) * math.sin(a), RED, 3))
    b.append(C(cx, cy, 6, INK, INK))
    b.append(T(cx, cy + r * 0.52, unit, 13, BLUE, weight="700"))
    if title:
        b.append(T(cx, cy + r * 0.52 + 16, title, 10.5, "#555"))
    return svg(size + 20, size + 14, "".join(b))


def side_by_side(svgs, gap=20):
    """several drawings in a row"""
    import re
    xs, body, h = 0, [], 0
    for s in svgs:
        w, hh = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
        inner = s[s.index(">") + 1:s.rindex("</svg>")]
        body.append(f'<g transform="translate({xs},0)">{inner}</g>')
        xs += w + gap
        h = max(h, hh)
    return svg(xs - gap, h, "".join(body))


def unit_square():
    """a square foot cut into 144 square inches"""
    b = [R(40, 20, 192, 192, PALE["blue"], BLUE, 2)]
    for k in range(1, 12):
        b.append(L(40 + 16 * k, 20, 40 + 16 * k, 212, GRID, 0.8))
        b.append(L(40, 20 + 16 * k, 232, 20 + 16 * k, GRID, 0.8))
    b.append(R(40, 196, 16, 16, PALE["red"], RED, 1.4))
    b.append(T(136, 232, "12 in", 13, INK, weight="600"))
    b.append(f'<text transform="translate(30,116) rotate(-90)" font-size="13" text-anchor="middle" fill="{INK}" font-weight="600">12 in</text>')
    b.append(T(390, 80, "1 square foot", 16, BLUE, weight="700"))
    b.append(T(390, 104, "= 12 in × 12 in", 14))
    b.append(T(390, 128, "= 144 square inches", 14, RED, weight="700"))
    b.append(T(390, 170, "Length factor 12, so the", 12, "#555"))
    b.append(T(390, 186, "area factor is 12 × 12.", 12, "#555"))
    return svg(540, 244, "".join(b))


def unit_cube():
    b = []
    fx, fy, s, d = 60, 70, 130, 46
    b.append(P([(fx, fy), (fx + s, fy), (fx + s, fy + s), (fx, fy + s)], PALE["green"], GREEN, 2))
    b.append(P([(fx, fy), (fx + d, fy - d), (fx + s + d, fy - d), (fx + s, fy)], "#cfead7", GREEN, 2))
    b.append(P([(fx + s, fy), (fx + s + d, fy - d), (fx + s + d, fy + s - d), (fx + s, fy + s)], "#bfe0c9", GREEN, 2))
    b.append(T(fx + s / 2, fy + s + 20, "12 in", 13, INK, weight="600"))
    b.append(T(fx - 22, fy + s / 2 + 4, "12 in", 13, INK, weight="600"))
    b.append(T(fx + s + d + 8, fy + s - d / 2 + 18, "12 in", 13, INK, anchor="start", weight="600"))
    b.append(T(400, 80, "1 cubic foot", 16, GREEN, weight="700"))
    b.append(T(400, 104, "= 12 × 12 × 12", 14))
    b.append(T(400, 128, "= 1,728 cubic inches", 14, RED, weight="700"))
    b.append(T(400, 170, "Volume uses the length", 12, "#555"))
    b.append(T(400, 186, "factor three times.", 12, "#555"))
    return svg(540, 236, "".join(b))


def tolerance(nominal, tol, test=None):
    lo, hi = nominal - tol, nominal + tol
    x0, w = 90, 380
    f = lambda v: x0 + w * (v - (lo - tol)) / (4 * tol)  # noqa: E731
    b = [L(60, 70, 500, 70, INK, 2), R(f(lo), 52, f(hi) - f(lo), 36, PALE["green"], GREEN, 1.6)]
    for v, lab, col in ((lo, f"{lo:g}", GREEN), (nominal, f"{nominal:g}", INK), (hi, f"{hi:g}", GREEN)):
        b.append(L(f(v), 46, f(v), 94, col, 1.6))
        b.append(T(f(v), 112, lab, 13, col, weight="700"))
    b.append(T(f(nominal), 38, "ACCEPTABLE", 11.5, GREEN, weight="700"))
    b.append(T(f(lo) - 48, 66, "too small", 11.5, RED, weight="600"))
    b.append(T(f(hi) + 48, 66, "too large", 11.5, RED, weight="600"))
    b.append(T(f(lo), 128, "lower limit", 10.5, "#555"))
    b.append(T(f(nominal), 128, "size called for", 10.5, "#555"))
    b.append(T(f(hi), 128, "upper limit", 10.5, "#555"))
    if test is not None:
        b.append(arrow(f(test), 8, f(test), 48, RED, 2))
    return svg(560, 136, "".join(b))


# ---------------------------------------------------------------- algebra

def pemdas():
    rows = [("P", "Parentheses and other grouping", "( )  [ ]  { }  | |  and a fraction bar", RED),
            ("E", "Exponents and roots", "x²   √x", GOLD),
            ("M D", "Multiply and Divide", "left to right, whichever comes first", GREEN),
            ("A S", "Add and Subtract", "left to right, whichever comes first", BLUE)]
    b = []
    for i, (k, name, note, col) in enumerate(rows):
        y = 16 + i * 50
        w = 520 - i * 40
        b.append(R(20 + i * 20, y, w, 42, "#fff", col, 2, 8))
        b.append(R(20 + i * 20, y, 70, 42, col, col, 2, 8))
        b.append(T(55 + i * 20, y + 28, k, 18, "#fff", weight="700"))
        b.append(T(104 + i * 20, y + 19, name, 13.5, INK, anchor="start", weight="700"))
        b.append(T(104 + i * 20, y + 35, note, 11.5, "#555", anchor="start"))
        b.append(T(8, y + 27, str(i + 1), 13, col, weight="700"))
    return svg(560, 222, "".join(b))


def pemdas_two_way():
    """evaluating runs down the PEMDAS list; solving undoes it from the bottom up"""
    rows = [("P", "Parentheses (grouping)", RED), ("E", "Exponents and roots", GOLD), ("M D", "Multiply or Divide, left to right", GREEN),
            ("A S", "Add or Subtract, left to right", BLUE)]
    b = []
    x0, w, y0, h = 190, 260, 62, 46
    for i, (k, name, col) in enumerate(rows):
        y = y0 + i * (h + 8)
        b.append(R(x0, y, w, h, "#fff", col, 2.2, 8))
        b.append(R(x0, y, 66, h, col, col, 2.2, 8))
        b.append(T(x0 + 33, y + 30, k, 18, "#fff", weight="700"))
        b.append(T(x0 + 78, y + 28, name, 12.5, INK, anchor="start", weight="600"))
    top, bot = y0 + 4, y0 + 4 * (h + 8) - 12
    b.append(arrow(150, top, 150, bot, GREEN, 5))
    b.append(T(92, 30, "EVALUATE", 16, GREEN, weight="800"))
    b.append(T(92, 48, "(calculate)", 11.5, GREEN, weight="600"))
    for k, s in enumerate(["Start at P", "and work DOWN", "to A S.", "", "You are DOING", "the operations."]):
        b.append(T(92, 110 + k * 17, s, 12, INK if k < 3 else "#555", weight="700" if k < 3 else "400"))
    b.append(arrow(490, bot, 490, top, RED, 5))
    b.append(T(552, 30, "SOLVE", 16, RED, weight="800"))
    b.append(T(552, 48, "(find the unknown)", 11.5, RED, weight="600"))
    for k, s in enumerate(["Start at A S", "and work UP", "to P.", "", "You are UNDOING", "the operations."]):
        b.append(T(552, 110 + k * 17, s, 12, INK if k < 3 else "#555", weight="700" if k < 3 else "400"))
    yb = bot + 40
    b.append(R(20, yb, 290, 78, PALE["green"], GREEN, 1.4, 8))
    b.append(T(165, yb + 20, "Evaluate 2x + 3 when x = 5", 12.5, GREEN, weight="700"))
    b.append(T(165, yb + 40, "2(5) + 3  →  multiply first: 10 + 3", 12, INK))
    b.append(T(165, yb + 60, "→  then add: 13", 12, INK))
    b.append(R(334, yb, 290, 78, PALE["red"], RED, 1.4, 8))
    b.append(T(479, yb + 20, "Solve 2x + 3 = 13", 12.5, RED, weight="700"))
    b.append(T(479, yb + 40, "undo the add first: 2x = 10", 12, INK))
    b.append(T(479, yb + 60, "→  then undo the multiply: x = 5", 12, INK))
    return svg(644, yb + 90, "".join(b))


def balance(left, right, note=""):
    b = [L(280, 40, 280, 150, INK, 4), P([(250, 166), (310, 166), (280, 146)], "#555", INK, 1.5), L(110, 60, 450, 60, INK, 4)]
    for x, txt, col in ((110, left, BLUE), (450, right, RED)):
        b.append(L(x, 60, x - 50, 112, INK, 1.2))
        b.append(L(x, 60, x + 50, 112, INK, 1.2))
        b.append(R(x - 70, 112, 140, 34, PALE["blue"] if col == BLUE else PALE["red"], col, 1.8, 6))
        b.append(T(x, 135, txt, 15, col, weight="700"))
    b.append(T(280, 30, "=", 22, INK, weight="700"))
    if note:
        b.append(T(280, 190, note, 12, "#555"))
    return svg(560, 198, "".join(b))


# ---------------------------------------------------------------- geometry

def rectangle(Lt="L", Wt="W", w=220, h=120, square=False):
    b = [R(60, 30, w, h, PALE["blue"], BLUE, 2.2), corner(60, 30 + h), corner(60 + w, 30 + h, -1), corner(60, 30, 1, 1),
         corner(60 + w, 30, -1, 1)]
    b.append(T(60 + w / 2, 30 + h + 22, Lt, 15, INK, weight="700", italic=True))
    b.append(T(60 + w + 18, 30 + h / 2 + 5, Wt, 15, INK, weight="700", italic=True))
    return svg(60 + w + 60, h + 66, "".join(b))


def parallelogram(bt="b", ht="h", at="a"):
    pts = [(50, 150), (250, 150), (310, 40), (110, 40)]
    b = [P(pts, PALE["green"], GREEN, 2.2), L(110, 40, 110, 150, INK, 1.3, "5 4"), corner(110, 150, 1, -1)]
    b.append(T(150, 172, bt, 15, INK, weight="700", italic=True))
    b.append(T(124, 100, ht, 15, INK, weight="700", italic=True))
    b.append(T(296, 100, at, 15, INK, weight="700", italic=True))
    return svg(360, 184, "".join(b))


def trapezoid(b1="b₁", b2="b₂", ht="h", c="c", d="d"):
    pts = [(40, 150), (320, 150), (250, 40), (110, 40)]
    b = [P(pts, PALE["gold"], GOLD, 2.2), L(140, 40, 140, 150, INK, 1.3, "5 4"), corner(140, 150, 1, -1)]
    b.append(T(180, 30, b1, 15, INK, weight="700", italic=True))
    b.append(T(180, 172, b2, 15, INK, weight="700", italic=True))
    b.append(T(154, 100, ht, 15, INK, weight="700", italic=True))
    b.append(T(62, 92, c, 15, INK, weight="700", italic=True))
    b.append(T(298, 92, d, 15, INK, weight="700", italic=True))
    return svg(360, 184, "".join(b))


def triangle(kind="scalene", labels=None, fs=15):
    lab = labels or {}
    if kind == "right":
        pts = [(60, 150), (300, 150), (60, 40)]
        b = [P(pts, PALE["purple"], PURPLE, 2.2), corner(60, 150, 1, -1)]
        b.append(T(44, 100, lab.get("a", "a"), fs, INK, weight="700", italic=True))
        b.append(T(180, 172, lab.get("b", "b"), fs, INK, weight="700", italic=True))
        b.append(T(196, 84, lab.get("c", "c"), fs, INK, weight="700", italic=True))
        return svg(340, 184, "".join(b))
    if kind == "equilateral":
        pts = [(80, 160), (260, 160), (170, 4.1)]
        apex = 170
    elif kind == "isosceles":
        pts = [(90, 160), (250, 160), (170, 20)]
        apex = 170
    else:
        pts = [(40, 160), (300, 160), (130, 30)]
        apex = 130
    b = [P(pts, PALE["purple"], PURPLE, 2.2)]
    if lab.get("h", "h"):
        b.append(L(apex, pts[2][1], apex, 160, INK, 1.3, "5 4"))
        b.append(corner(apex, 160, 1, -1))
        b.append(T(apex + 13, 110, lab.get("h", "h"), fs, INK, weight="700", italic=True))
    b.append(T((pts[0][0] + pts[1][0]) / 2 + 24, 180, lab.get("b", "b"), fs, INK, weight="700", italic=True))
    b.append(T((pts[0][0] + pts[2][0]) / 2 - 14, (pts[0][1] + pts[2][1]) / 2, lab.get("a", "a"), fs, INK, weight="700", italic=True))
    b.append(T((pts[1][0] + pts[2][0]) / 2 + 14, (pts[1][1] + pts[2][1]) / 2, lab.get("c", "c"), fs, INK, weight="700", italic=True))
    return svg(340, 190, "".join(b))


def circle(show=("r", "d")):
    cx, cy, r = 150, 110, 86
    b = [C(cx, cy, r, PALE["red"], RED, 2.2), C(cx, cy, 3, INK, INK)]
    if "d" in show:
        b.append(L(cx - r, cy, cx + r, cy, INK, 1.6))
        b.append(T(cx - 40, cy + 20, "d", 15, INK, weight="700", italic=True))
    if "r" in show:
        a = math.radians(50)
        b.append(L(cx, cy, cx + r * math.cos(a), cy - r * math.sin(a), INK, 1.6, "5 4"))
        b.append(T(cx + 20, cy - 34, "r", 15, INK, weight="700", italic=True))
    b.append(T(cx + r + 26, cy - 60, "C", 15, RED, weight="700", italic=True))
    b.append(f'<path d="M{cx + r + 16} {cy - 50} Q {cx + r + 4} {cy - 36} {cx + r - 2} {cy - 26}" fill="none" stroke="{RED}" stroke-width="1.2"/>')
    return svg(300, 216, "".join(b))


def hexagon():
    cx, cy, r = 150, 110, 90
    pts = [(cx + r * math.cos(math.radians(60 * k)), cy - r * math.sin(math.radians(60 * k))) for k in range(6)]
    b = [P(pts, PALE["green"], GREEN, 2.2), L(cx - r, cy, cx + r, cy, INK, 1.3, "5 4"),
         L(cx + 30, cy - 78, cx + 30, cy + 78, INK, 1.3, "5 4")]
    b.append(T(cx, cy + r * 0.866 + 20, "s", 15, INK, weight="700", italic=True))
    b.append(T(cx - 40, cy - 8, "d = 2s", 13, INK, weight="700", italic=True))
    b.append(L(cx + 30, cy + 46, cx + 100, cy + 46, INK, 0.8))
    b.append(T(cx + 104, cy + 50, "f = 1.732s", 13, INK, anchor="start", weight="700", italic=True))
    return svg(360, 214, "".join(b))


def composite_L(a, b_, c, d):
    """an L: a wide by b_ tall with a c by d corner removed"""
    s = 190 / max(a, b_)
    W, H, cw, ch = a * s, b_ * s, c * s, d * s
    x0, y0 = 60, 26
    pts = [(x0, y0), (x0 + W - cw, y0), (x0 + W - cw, y0 + ch), (x0 + W, y0 + ch), (x0 + W, y0 + H), (x0, y0 + H)]
    body = [P(pts, PALE["blue"], BLUE, 2.2), L(x0 + W - cw, y0 + ch, x0, y0 + ch, RED, 1.4, "5 4"),
            T(x0 + (W - cw) / 2, y0 + ch / 2 + 5, "A", 16, RED, weight="700"),
            T(x0 + W / 2, y0 + ch + (H - ch) / 2 + 5, "B", 16, RED, weight="700"),
            T(x0 + W / 2, y0 + H + 20, f"{a} ft", 13, INK, weight="600"),
            T(x0 - 26, y0 + H / 2 + 4, f"{b_} ft", 13, INK, weight="600"),
            T(x0 + (W - cw) / 2, y0 - 8, f"{a - c} ft", 13, INK, weight="600"),
            T(x0 + W + 26, y0 + ch + (H - ch) / 2 + 4, f"{b_ - d} ft", 13, INK, weight="600")]
    return svg(x0 + W + 70, y0 + H + 34, "".join(body))


def composite_house(w, h, roof):
    s = 150 / max(w, h + roof)
    W, H, Rf = w * s, h * s, roof * s
    x0, y0 = 70, 20 + Rf
    body = [R(x0, y0, W, H, PALE["blue"], BLUE, 2.2), P([(x0, y0), (x0 + W, y0), (x0 + W / 2, y0 - Rf)], PALE["gold"], GOLD, 2.2),
            L(x0 + W / 2, y0 - Rf, x0 + W / 2, y0, INK, 1.2, "5 4"),
            T(x0 + W / 2, y0 + H + 20, f"{w} ft", 13, INK, weight="600"),
            T(x0 - 26, y0 + H / 2 + 4, f"{h} ft", 13, INK, weight="600"),
            T(x0 + W / 2 + 22, y0 - Rf / 2 + 6, f"{roof} ft", 13, INK, weight="600")]
    return svg(x0 + W + 70, y0 + H + 34, "".join(body))


def composite_ring(R_, r_):
    cx, cy = 130, 120
    s = 96 / R_
    body = [C(cx, cy, R_ * s, PALE["green"], GREEN, 2.2), C(cx, cy, r_ * s, "#fff", GREEN, 2.2),
            L(cx, cy, cx + R_ * s, cy, INK, 1.4), L(cx, cy, cx, cy - r_ * s, INK, 1.4, "5 4"),
            T(cx + (r_ + R_) * s / 2, cy - 6, "R", 13, INK, weight="700", italic=True),
            T(cx + 9, cy - r_ * s / 2, "r", 13, INK, weight="700", italic=True),
            T(cx, cy + R_ * s + 18, f"R = {R_} ft,  r = {r_} ft", 12.5, INK, weight="600")]
    return svg(280, 246, "".join(body))


def composite_frame(W_, H_, w_, h_):
    s = 200 / W_
    x0, y0 = 50, 26
    body = [R(x0, y0, W_ * s, H_ * s, PALE["gold"], GOLD, 2.2),
            R(x0 + (W_ - w_) * s / 2, y0 + (H_ - h_) * s / 2, w_ * s, h_ * s, "#fff", GOLD, 2.2),
            T(x0 + W_ * s / 2, y0 + H_ * s + 20, f"{W_} in", 13, INK, weight="600"),
            T(x0 - 24, y0 + H_ * s / 2 + 4, f"{H_} in", 13, INK, weight="600"),
            T(x0 + W_ * s / 2, y0 + H_ * s / 2 + 4, f"{w_} in × {h_} in", 12.5, INK, weight="600")]
    return svg(x0 + W_ * s + 50, y0 + H_ * s + 34, "".join(body))


def pythag():
    a, b_, s = 3, 4, 26
    x0, y0 = 120, 200
    body = [P([(x0, y0), (x0 + b_ * s, y0), (x0, y0 - a * s)], PALE["purple"], PURPLE, 2.2),
            R(x0 - a * s, y0 - a * s, a * s, a * s, PALE["red"], RED, 1.6),
            R(x0, y0, b_ * s, b_ * s, PALE["blue"], BLUE, 1.6)]
    for k in range(1, a):
        body.append(L(x0 - a * s + k * s, y0 - a * s, x0 - a * s + k * s, y0, RED, 0.6))
        body.append(L(x0 - a * s, y0 - a * s + k * s, x0, y0 - a * s + k * s, RED, 0.6))
    for k in range(1, b_):
        body.append(L(x0 + k * s, y0, x0 + k * s, y0 + b_ * s, BLUE, 0.6))
        body.append(L(x0, y0 + k * s, x0 + b_ * s, y0 + k * s, BLUE, 0.6))
    c = 5 * s
    ux, uy = b_ / 5, -a / 5       # along the hypotenuse from (x0, y0-a*s) to (x0+b*s, y0): direction (b, a)/5
    p1, p2 = (x0, y0 - a * s), (x0 + b_ * s, y0)
    nx, ny = a / 5, -b_ / 5       # outward normal
    q1 = (p1[0] + nx * c, p1[1] + ny * c)
    q2 = (p2[0] + nx * c, p2[1] + ny * c)
    body.append(P([p1, p2, q2, q1], PALE["green"], GREEN, 1.6))
    for bx, by in ((x0 - a * s / 2, y0 - a * s / 2), (x0 + b_ * s / 2, y0 + b_ * s / 2)):
        body.append(f'<rect x="{bx - 30}" y="{by - 10}" width="60" height="20" rx="4" fill="#fff" opacity="0.9"/>')
    body.append(T(x0 - a * s / 2, y0 - a * s / 2 + 5, "a² = 9", 13, RED, weight="700"))
    body.append(T(x0 + b_ * s / 2, y0 + b_ * s / 2 + 5, "b² = 16", 13, BLUE, weight="700"))
    body.append(T((p1[0] + q2[0]) / 2, (p1[1] + q2[1]) / 2 + 5, "c² = 25", 13, GREEN, weight="700"))
    body.append(T(440, 200, "9 + 16 = 25", 16, INK, weight="700"))
    body.append(T(440, 224, "a² + b² = c²", 15, PURPLE, weight="700"))
    return svg(540, 320, "".join(body))


# ---------------------------------------------------------------- added drawings

def trapezoid_dims(b1, b2, h, c=None, d=None, unit="in"):
    """a trapezoid with its real measurements written on it"""
    pts = [(40, 150), (320, 150), (250, 40), (110, 40)]
    b = [P(pts, PALE["gold"], GOLD, 2.2), L(140, 40, 140, 150, INK, 1.3, "5 4"), corner(140, 150, 1, -1)]
    b.append(T(180, 30, f"{b1} {unit}", 14, INK, weight="700"))
    b.append(T(180, 172, f"{b2} {unit}", 14, INK, weight="700"))
    b.append(T(146, 100, f"{h} {unit}", 14, INK, anchor="start", weight="700"))
    if c:
        b.append(T(66, 92, f"{c} {unit}", 13, INK, anchor="end", weight="600"))
    if d:
        b.append(T(294, 92, f"{d} {unit}", 13, INK, anchor="start", weight="600"))
    return svg(380, 184, "".join(b))


def trapezoid_pair():
    """two equal trapezoids, one turned over, make a parallelogram"""
    a = [(40, 150), (240, 150), (200, 50), (100, 50)]
    c = [(240, 150), (340, 150), (400, 50), (200, 50)]
    b = [P(a, PALE["gold"], GOLD, 2.2), P(c, PALE["blue"], BLUE, 2.2), L(130, 50, 130, 150, INK, 1.2, "5 4"), corner(130, 150, 1, -1)]
    b.append(T(150, 42, "b₁", 14, INK, weight="700", italic=True))
    b.append(T(300, 42, "b₂", 14, INK, weight="700", italic=True))
    b.append(T(140, 172, "b₂", 14, INK, weight="700", italic=True))
    b.append(T(290, 172, "b₁", 14, INK, weight="700", italic=True))
    b.append(T(142, 104, "h", 14, INK, weight="700", italic=True))
    b.append(T(220, 198, "whole base = b₁ + b₂", 13, RED, weight="700"))
    b.append(T(520, 84, "parallelogram area = (b₁ + b₂)h", 12.5, INK, weight="600"))
    b.append(T(520, 108, "one trapezoid = half of it", 12.5, INK, weight="600"))
    b.append(T(520, 136, "A = (b₁ + b₂)h ÷ 2", 14, GOLD, weight="700"))
    return svg(640, 208, "".join(b))


def parallelogram_slide():
    """cut the end triangle off a parallelogram and slide it across: a rectangle"""
    b = [P([(40, 150), (220, 150), (270, 50), (90, 50)], PALE["green"], GREEN, 2.2), P([(40, 150), (90, 150), (90, 50)], "#bfe0c9", GREEN, 2.2),
         L(90, 50, 90, 150, INK, 1.2, "5 4"), T(130, 172, "b", 14, INK, weight="700", italic=True), T(102, 104, "h", 14, INK, weight="700", italic=True),
         arrow(292, 100, 348, 100, RED, 2.2), T(320, 90, "slide", 11.5, RED, weight="700"),
         R(400, 50, 180, 100, PALE["green"], GREEN, 2.2), P([(580, 150), (630, 150), (630, 50)], "#bfe0c9", GREEN, 2.2)]
    b[-2] = P([(420, 150), (600, 150), (600, 50), (420, 50)], PALE["green"], GREEN, 2.2)
    b[-1] = P([(550, 150), (600, 150), (600, 50)], "#bfe0c9", GREEN, 2.2)
    b += [L(550, 150, 600, 50, GREEN, 1.2, "4 3"), T(510, 172, "b", 14, INK, weight="700", italic=True), T(612, 104, "h", 14, INK, weight="700", italic=True),
          T(510, 38, "same base, same height: A = bh", 12, INK, weight="600")]
    return svg(650, 184, "".join(b))


def composite_L_trap(a, b_, c, d, unit="ft"):
    """an L (a wide, b_ tall, a c by d corner cut from the top right) split into two trapezoids
    by one cut from the inside corner to the far outside corner"""
    s = 200 / max(a, b_)
    W, H, cw, ch = a * s, b_ * s, c * s, d * s
    x0, y0 = 70, 34
    A = [(x0, y0), (x0 + W - cw, y0), (x0 + W - cw, y0 + ch), (x0, y0 + H)]
    B = [(x0, y0 + H), (x0 + W - cw, y0 + ch), (x0 + W, y0 + ch), (x0 + W, y0 + H)]
    body = [P(A, PALE["gold"], GOLD, 2.2), P(B, PALE["blue"], BLUE, 2.2), L(x0 + W - cw, y0 + ch, x0, y0 + H, RED, 2, "6 4"),
            T(x0 + (W - cw) * 0.36, y0 + H * 0.34, "A", 18, "#a36408", weight="700"),
            T(x0 + W * 0.66, y0 + ch + (H - ch) * 0.62, "B", 18, BLUE, weight="700"),
            T(x0 + W / 2, y0 + H + 20, f"{a} {unit}", 13, INK, weight="600"),
            T(x0 - 10, y0 + H / 2 + 4, f"{b_} {unit}", 13, INK, anchor="end", weight="600"),
            T(x0 + (W - cw) / 2, y0 - 9, f"{a - c} {unit}", 13, INK, weight="600"),
            T(x0 + W - cw + 8, y0 + ch / 2 + 4, f"{d} {unit}", 13, INK, anchor="start", weight="600"),
            T(x0 + W - cw / 2, y0 + ch - 9, f"{c} {unit}", 13, INK, weight="600"),
            T(x0 + W + 10, y0 + ch + (H - ch) / 2 + 4, f"{b_ - d} {unit}", 13, INK, anchor="start", weight="600")]
    return svg(x0 + W + 80, y0 + H + 34, "".join(body))


def composite_L_plain(a, b_, c, d, unit="ft"):
    """the same L with no cut lines, for practice"""
    s = 150 / max(a, b_)
    W, H, cw, ch = a * s, b_ * s, c * s, d * s
    x0, y0 = 60, 30
    pts = [(x0, y0), (x0 + W - cw, y0), (x0 + W - cw, y0 + ch), (x0 + W, y0 + ch), (x0 + W, y0 + H), (x0, y0 + H)]
    body = [P(pts, PALE["blue"], BLUE, 2.2),
            T(x0 + W / 2, y0 + H + 19, f"{a} {unit}", 12.5, INK, weight="600"),
            T(x0 - 8, y0 + H / 2 + 4, f"{b_} {unit}", 12.5, INK, anchor="end", weight="600"),
            T(x0 + (W - cw) / 2, y0 - 8, f"{a - c} {unit}", 12.5, INK, weight="600"),
            T(x0 + W + 8, y0 + ch + (H - ch) / 2 + 4, f"{b_ - d} {unit}", 12.5, INK, anchor="start", weight="600")]
    return svg(x0 + W + 66, y0 + H + 30, "".join(body))


def trap_on_rect(w, h, top, th, unit="ft"):
    """a rectangle w by h with a trapezoid (bases w and top, height th) on top"""
    s = 170 / max(w, h + th)
    W, H, Tp, Th = w * s, h * s, top * s, th * s
    x0, y0 = 70, 26 + Th
    tr = [(x0, y0), (x0 + W, y0), (x0 + (W + Tp) / 2, y0 - Th), (x0 + (W - Tp) / 2, y0 - Th)]
    body = [R(x0, y0, W, H, PALE["blue"], BLUE, 2.2), P(tr, PALE["gold"], GOLD, 2.2), L(x0 + W / 2, y0 - Th, x0 + W / 2, y0, INK, 1.2, "5 4"),
            T(x0 + W / 2, y0 + H + 19, f"{w} {unit}", 12.5, INK, weight="600"), T(x0 - 8, y0 + H / 2 + 4, f"{h} {unit}", 12.5, INK, anchor="end", weight="600"),
            T(x0 + W / 2, y0 - Th - 8, f"{top} {unit}", 12.5, INK, weight="600"), T(x0 + W / 2 + 8, y0 - Th / 2 + 4, f"{th} {unit}", 12.5, INK, anchor="start", weight="600")]
    return svg(x0 + W + 60, y0 + H + 30, "".join(body))


def trap_hole(b1, b2, h, dia, unit="in"):
    """a trapezoid plate with a round hole"""
    pts = [(40, 150), (320, 150), (250, 40), (110, 40)]
    b = [P(pts, PALE["gold"], GOLD, 2.2), C(180, 98, 30, "#fff", GOLD, 2.2), L(150, 98, 210, 98, INK, 1.2),
         T(180, 30, f"{b1} {unit}", 13, INK, weight="600"), T(180, 172, f"{b2} {unit}", 13, INK, weight="600"),
         L(292, 40, 292, 150, INK, 1.2, "5 4"), T(300, 100, f"{h} {unit}", 13, INK, anchor="start", weight="600"),
         T(180, 92, f"{dia} {unit}", 11.5, INK, weight="600")]
    return svg(380, 184, "".join(b))


def number_line(vals, lo, hi, step, labels=None):
    """points marked on a number line"""
    x0, w = 40, 520
    f = lambda v: x0 + w * (v - lo) / (hi - lo)  # noqa: E731
    b = [L(x0 - 14, 60, x0 + w + 14, 60, INK, 2)]
    k = 0
    while lo + k * step <= hi + 1e-9:
        v = lo + k * step
        b.append(L(f(v), 52, f(v), 68, INK, 1.4))
        b.append(T(f(v), 86, f"{v:g}", 11.5, INK, weight="600"))
        k += 1
    for i, v in enumerate(vals):
        b.append(C(f(v), 60, 4.5, RED, RED))
        b.append(T(f(v), 40 - (14 if i % 2 else 0), (labels[i] if labels else f"{v:g}"), 11.5, RED, weight="700"))
        b.append(L(f(v), 44 - (14 if i % 2 else 0), f(v), 55, RED, 0.8))
    return svg(600, 96, "".join(b))


def fraction_bars(rows):
    """equal bars cut into different numbers of pieces; rows are (shaded, pieces)"""
    b = []
    for i, (k, nn) in enumerate(rows):
        y = 14 + i * 42
        for j in range(nn):
            b.append(R(60 + j * 400 / nn, y, 400 / nn, 28, PALE["blue"] if j < k else "#fff", BLUE, 1.2))
        b.append(T(500, y + 20, f"{k}/{nn}", 15, INK, anchor="start", weight="700"))
    return svg(580, 14 + len(rows) * 42, "".join(b))


def right_tri_dims(a, b_, c, unit="ft", note=""):
    """a right triangle with measurements; any may be '?'"""
    pts = [(60, 150), (300, 150), (60, 40)]
    b = [P(pts, PALE["purple"], PURPLE, 2.2), corner(60, 150, 1, -1),
         T(50, 100, f"{a}" + ("" if a == "?" else f" {unit}"), 13.5, INK, anchor="end", weight="700"),
         T(180, 172, f"{b_}" + ("" if b_ == "?" else f" {unit}"), 13.5, INK, weight="700"),
         T(196, 84, f"{c}" + ("" if c == "?" else f" {unit}"), 13.5, INK, anchor="start", weight="700")]
    if note:
        b.append(T(180, 190, note, 11.5, "#555"))
    return svg(360, 196, "".join(b))


# ---------------------------------------------------------------- solids (oblique view, hidden edges dashed)

def _proj(p, c=0.42):
    x, d, z = p
    return (x + c * d, -(z + c * d))


def solid(bottom, top, H, color=BLUE, fill=None, labels=(), extra=(), scale=1.0, pad=46):
    """a prism, pyramid or frustum: bottom and top are plan polygons [(x, depth)] counter-clockwise,
    top at height H (a single point for a pyramid). labels: [((x, d, z), text, anchor, dx, dy)].
    extra: [((x,d,z), (x,d,z), dashed)] lines such as a height or a slant length"""
    B = [(x * scale, d * scale, 0) for x, d in bottom]
    if len(top) == 1:
        Tp = [(top[0][0] * scale, top[0][1] * scale, H * scale)] * len(bottom)
    else:
        Tp = [(x * scale, d * scale, H * scale) for x, d in top]
    v = (-0.42, 1, -0.42)
    n_ = len(B)

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def vis(nrm):
        return nrm[0] * v[0] + nrm[1] * v[1] + nrm[2] * v[2] < -1e-9

    side_vis = []
    for i in range(n_):
        j = (i + 1) % n_
        nrm = cross(sub(B[j], B[i]), sub(Tp[i] if Tp[i] != B[i] else Tp[j], B[i]))
        if Tp[i] == Tp[j] and len(top) == 1:
            nrm = cross(sub(B[j], B[i]), sub(Tp[i], B[i]))
        side_vis.append(vis(nrm))
    top_vis = len(top) > 1
    pts = [_proj(p) for p in B + Tp]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = pad - min(xs), pad - min(ys)
    P2 = lambda p: (_proj(p)[0] + ox, _proj(p)[1] + oy)  # noqa: E731
    pale = fill or PALE["blue"]
    body = []
    for i in range(n_):
        if side_vis[i]:
            j = (i + 1) % n_
            poly = [B[i], B[j], Tp[j]] + ([Tp[i]] if len(top) > 1 else [])
            body.append(P([P2(p) for p in poly], pale, "none", 0))
    if top_vis:
        body.append(P([P2(p) for p in Tp], "#ffffff", "none", 0))
        body.append(P([P2(p) for p in Tp], pale, "none", 0))
    edges = []
    for i in range(n_):
        j, k = (i + 1) % n_, (i - 1) % n_
        edges.append((B[i], B[j], side_vis[i]))
        if len(top) > 1:
            edges.append((Tp[i], Tp[j], True))
        edges.append((B[i], Tp[i], side_vis[i] or side_vis[k]))
    hidden = [L(*P2(a), *P2(b), color, 1.3, "5 4") for a, b, s in edges if not s]
    shown = [L(*P2(a), *P2(b), color, 2.1) for a, b, s in edges if s]
    for a, b, dashed in extra:
        body.append(L(*P2(tuple(t * scale for t in a)), *P2(tuple(t * scale for t in b)), RED, 1.6, "5 4" if dashed else None))
    body = body[:1] + body[1:]
    out = body[:]
    out[0:0] = []
    labs = []
    for p, text, anchor, dx, dy in labels:
        x, y = P2(tuple(t * scale for t in p))
        labs.append(T(x + dx, y + dy, text, 13, INK, anchor=anchor, weight="700"))
    w, h = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
    return svg(w, h, "".join(out[:len(out) - len(extra)] + hidden + shown + out[len(out) - len(extra):] + labs))


def rect_prism(L_, W_, H_, lab=("L", "W", "H"), s=None):
    s = s or 170 / max(L_, H_, W_ * 0.8)
    return solid([(0, 0), (L_, 0), (L_, W_), (0, W_)], [(0, 0), (L_, 0), (L_, W_), (0, W_)], H_, BLUE, PALE["blue"],
                 [((L_ / 2, 0, 0), lab[0], "middle", 0, 18), ((L_, W_ / 2, 0), lab[1], "start", 10, 12), ((0, 0, H_ / 2), lab[2], "end", -8, 4)], scale=s)


def tri_prism(s_, len_, lab=("s", "h")):
    """an equilateral-triangle prism lying on its side (the length is the prism's height)"""
    k = 240 / max(len_, s_ * 2)
    ht = s_ * 0.866
    # build in a rotated frame: triangle in the x-z plane at depth 0 and depth len_
    tri = [(0, 0), (s_, 0), (s_ / 2, ht)]
    lines, fillp = [], []
    def pp(x, d, z):
        X, Y = _proj((x * k, d * k * 0.9, z * k))
        return X, Y
    front = [pp(x, 0, z) for x, z in tri]
    back = [pp(x, len_, z) for x, z in tri]
    xs = [p[0] for p in front + back]; ys = [p[1] for p in front + back]
    ox, oy = 40 - min(xs), 40 - min(ys)
    F = [(x + ox, y + oy) for x, y in front]; Bk = [(x + ox, y + oy) for x, y in back]
    b = [P([F[1], Bk[1], Bk[2], F[2]], PALE["green"], "none", 0), P([F[2], Bk[2], Bk[0], F[0]], "#cfead7", "none", 0), P(F, PALE["green"], "none", 0)]
    b.append(L(*F[0], *Bk[0], GREEN, 1.3, "5 4")); b.append(L(*Bk[0], *Bk[1], GREEN, 1.3, "5 4"))
    for a_, c_ in [(F[0], F[1]), (F[1], F[2]), (F[2], F[0]), (F[1], Bk[1]), (F[2], Bk[2]), (Bk[1], Bk[2]), (Bk[2], Bk[0])]:
        b.append(L(*a_, *c_, GREEN, 2.1))
    b.append(T((F[0][0] + F[1][0]) / 2, F[0][1] + 18, lab[0], 13, INK, weight="700"))
    b.append(T((F[1][0] + Bk[1][0]) / 2 + 14, (F[1][1] + Bk[1][1]) / 2 + 12, lab[1], 13, INK, anchor="start", weight="700"))
    w, h = max(xs) - min(xs) + 80, max(ys) - min(ys) + 80
    return svg(w, h, "".join(b))


def hex_prism(s_, H_, lab=("s", "h")):
    import math as m
    hexp = [(s_ * m.cos(m.radians(60 * i + 30)), s_ * m.sin(m.radians(60 * i + 30)) * 1.25) for i in range(6)]
    k = 120 / max(H_, 2 * s_)
    return solid(hexp, hexp, H_, PURPLE, PALE["purple"],
                 [((s_ * 0.43, -s_ * 0.85, 0), lab[0], "middle", 0, 18), ((s_, 0, H_ / 2), lab[1], "start", 10, 4)], scale=k)


def cylinder3d(d_label="d", h_label="h", r=60, hh=150, color=RED, fill=None, show_r=True):
    cx, top, ry = r + 40, 30, r * 0.32
    bot = top + hh
    fill = fill or PALE["red"]
    b = [f'<path d="M{cx - r} {top} L{cx - r} {bot} A{r} {ry} 0 0 0 {cx + r} {bot} L{cx + r} {top} Z" fill="{fill}"/>',
         f'<ellipse cx="{cx}" cy="{top}" rx="{r}" ry="{ry}" fill="#fff" stroke="{color}" stroke-width="2.1"/>',
         f'<ellipse cx="{cx}" cy="{top}" rx="{r}" ry="{ry}" fill="{fill}" opacity="0.6"/>',
         L(cx - r, top, cx - r, bot, color, 2.1), L(cx + r, top, cx + r, bot, color, 2.1),
         f'<path d="M{cx - r} {bot} A{r} {ry} 0 0 0 {cx + r} {bot}" fill="none" stroke="{color}" stroke-width="2.1"/>',
         f'<path d="M{cx - r} {bot} A{r} {ry} 0 0 1 {cx + r} {bot}" fill="none" stroke="{color}" stroke-width="1.3" stroke-dasharray="5 4"/>',
         L(cx - r, bot, cx + r, bot, INK, 1.2, "5 4"), T(cx, bot + ry + 18, d_label, 13, INK, weight="700"),
         T(cx + r + 10, (top + bot) / 2 + 4, h_label, 13, INK, anchor="start", weight="700")]
    if show_r:
        b += [C(cx, top, 2.5, INK, INK), L(cx, top, cx + r, top, INK, 1.2), T(cx + r / 2, top - 6, "r", 12, INK, weight="700", italic=True)]
    return svg(2 * r + 130, bot + ry + 34, "".join(b))


def sphere3d(label="d", r=80, color=GOLD):
    cx, cy = r + 30, r + 20
    b = [f'<defs><radialGradient id="sg{r}" cx="38%" cy="35%" r="70%"><stop offset="0" stop-color="#fff"/>'
         f'<stop offset="1" stop-color="{PALE["gold"]}"/></radialGradient></defs>',
         C(cx, cy, r, f"url(#sg{r})", color, 2.2),
         f'<path d="M{cx - r} {cy} A{r} {r * 0.28} 0 0 0 {cx + r} {cy}" fill="none" stroke="{color}" stroke-width="1.6"/>',
         f'<path d="M{cx - r} {cy} A{r} {r * 0.28} 0 0 1 {cx + r} {cy}" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="5 4"/>',
         L(cx - r, cy, cx + r, cy, INK, 1.2, "5 4"), C(cx, cy, 2.5, INK, INK), T(cx, cy - 8, label, 13, INK, weight="700")]
    return svg(2 * r + 60, 2 * r + 44, "".join(b))


def square_pyramid(a, H_, s_lab="s", h_lab="h", base_lab="b", k=None):
    H_ = max(H_, a * 1.1)          # drawn taller than true scale so the height and slant can be seen
    k = k or 150 / max(a, H_)
    sq = [(0, 0), (a, 0), (a, a), (0, a)]
    ap = (a / 2, a / 2)
    return solid(sq, [ap], H_, BLUE, PALE["blue"],
                 [((a / 2, 0, 0), base_lab, "middle", 0, 18), ((a / 2, a / 2, H_ * 0.45), h_lab, "start", 6, 0),
                  ((a / 2, a / 4, H_ / 2), s_lab, "end", -16, 4)],
                 extra=[((a / 2, a / 2, H_), (a / 2, a / 2, 0), True), ((a / 2, a / 2, H_), (a / 2, 0, 0), False)], scale=k)


def tri_pyramid(a, H_, k=None):
    H_ = max(H_, a * 1.1)
    k = k or 150 / max(a, H_)
    tri = [(0, 0), (a, 0), (a / 2, a * 0.866)]
    cen = (a / 2, a * 0.2887)
    return solid(tri, [cen], H_, GREEN, PALE["green"],
                 [((a / 2, 0, 0), "side", "middle", 0, 18), ((cen[0], cen[1], H_ * 0.55), "h", "end", -6, 0),
                  ((a / 2, cen[1] / 2, H_ * 0.3), "s", "start", 14, 0)],
                 extra=[((cen[0], cen[1], H_), (cen[0], cen[1], 0), True), ((cen[0], cen[1], H_), (a / 2, 0, 0), False)], scale=k)


def frustum3d(A_, a_, H_, labs=("bottom side", "top side", "h", "s")):
    H_ = max(H_, A_ * 0.75)        # drawn taller than true scale
    k = 150 / max(A_, H_)
    off = (A_ - a_) / 2
    bot = [(0, 0), (A_, 0), (A_, A_), (0, A_)]
    tp = [(off, off), (off + a_, off), (off + a_, off + a_), (off, off + a_)]
    return solid(bot, tp, H_, GOLD, PALE["gold"],
                 [((A_ / 2, 0, 0), labs[0], "middle", 0, 18), ((A_ / 2, off + a_, H_), labs[1], "middle", 0, -8),
                  ((A_ / 2, A_ / 2, H_ * 0.2), labs[2], "start", 6, 0), ((A_ * 0.67, off / 2, H_ * 0.62), labs[3], "start", 10, 4)],
                 extra=[((A_ / 2, A_ / 2, H_), (A_ / 2, A_ / 2, 0), True), ((A_ * 0.65, off, H_), (A_ * 0.65, 0, 0), False)], scale=k)


def unfolded_prism(L_, W_, H_):
    """the net of a box: the four sides form one long rectangle p wide and h tall"""
    k = 30
    b = []
    x = 40
    for i, w_ in enumerate([L_, W_, L_, W_]):
        b.append(R(x, 70, w_ * k, H_ * k, PALE["blue"], BLUE, 1.8))
        b.append(T(x + w_ * k / 2, 70 + 18, f"{w_}", 12, INK, weight="600"))
        x += w_ * k
    b.append(R(40, 70 - W_ * k, L_ * k, W_ * k, PALE["gold"], GOLD, 1.8))
    b.append(R(40, 70 + H_ * k, L_ * k, W_ * k, PALE["gold"], GOLD, 1.8))
    b.append(T(40 + L_ * k / 2, 70 - W_ * k / 2 + 5, "base A", 12, "#8a5a00", weight="700"))
    b.append(T(40 + L_ * k / 2, 70 + H_ * k + W_ * k / 2 + 5, "base A", 12, "#8a5a00", weight="700"))
    b.append(T(x + 10, 70 + H_ * k / 2 + 4, f"h = {H_}", 12, INK, anchor="start", weight="700"))
    b.append(arrow(40 + L_ * k + 4, 58, x, 58, RED, 1.6))
    b.append(L(40 + L_ * k + 4, 58, 40 + L_ * k + 4, 66, RED, 1.2))
    b.append(T((40 + L_ * k + x) / 2, 50, f"p = {2 * L_ + 2 * W_}  (the perimeter of the base)", 12, RED, weight="700"))
    return svg(x + 90, 70 + H_ * k + W_ * k + 20, "".join(b))


# ---------------------------------------------------------------- ratio and trigonometry

def pulleys():
    b = [C(110, 100, 72, PALE["blue"], BLUE, 2.2), C(110, 100, 6, INK, INK), C(380, 100, 24, PALE["gold"], GOLD, 2.2), C(380, 100, 4, INK, INK),
         L(110 - 6, 28, 380 - 2, 76, INK, 2.4), L(110 - 6, 172, 380 - 2, 124, INK, 2.4),
         L(38, 100, 182, 100, INK, 1, "4 3"), T(110, 92, "D = 12 in", 12.5, INK, weight="700"), T(110, 126, "driving", 11, "#555"),
         T(110, 140, "N = 1,725 rpm", 11.5, BLUE, weight="700"), T(380, 148, "d = 4 in", 12.5, INK, weight="700"), T(380, 164, "driven", 11, "#555"),
         T(380, 180, "n = ?", 11.5, GOLD, weight="700"), T(245, 205, "D × N = d × n", 14, RED, weight="700")]
    return svg(440, 216, "".join(b))


def trig_triangle(at="A", show=("opp", "adj", "hyp"), labels=None, size=1.0):
    """a right triangle with the right angle at bottom left; theta at A (bottom right) or B (top left).
    The sides are coloured by their name relative to theta."""
    k = size
    Cp, Ap, Bp = (110 * k, 170 * k), (380 * k, 170 * k), (110 * k, 30 * k)
    if at == "A":
        names = {"opp": (Cp, Bp), "adj": (Cp, Ap), "hyp": (Bp, Ap)}
        ang = Ap
    else:
        names = {"opp": (Cp, Ap), "adj": (Cp, Bp), "hyp": (Bp, Ap)}
        ang = Bp
    col = {"opp": RED, "adj": BLUE, "hyp": GREEN}
    word = {"opp": "opposite", "adj": "adjacent", "hyp": "hypotenuse"}
    b = [P([Cp, Ap, Bp], "#fafbfe", INK, 1.2), corner(Cp[0], Cp[1], 1, -1, 12 * k)]
    for nm, (p1, p2) in names.items():
        b.append(L(*p1, *p2, col[nm], 4))
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        txt = (labels or {}).get(nm, word[nm])
        if nm == "hyp":
            b.append(T(mx + 14, my - 10, txt, 13, col[nm], anchor="start", weight="700"))
        elif p1[1] == p2[1]:
            b.append(T(mx, my + 22, txt, 13, col[nm], weight="700"))
        else:
            b.append(T(mx - 10, my + 4, txt, 13, col[nm], anchor="end", weight="700"))
    if at == "A":
        b.append(f'<path d="M{Ap[0] - 42 * k} {Ap[1]} A{42 * k} {42 * k} 0 0 1 {Ap[0] - 37 * k} {Ap[1] - 19 * k}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        b.append(T(Ap[0] - 58 * k, Ap[1] - 8 * k, "θ", 16, INK, weight="700", italic=True))
    else:
        b.append(f'<path d="M{Bp[0]} {Bp[1] + 42 * k} A{42 * k} {42 * k} 0 0 0 {Bp[0] + 35 * k} {Bp[1] + 23 * k}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        b.append(T(Bp[0] + 14 * k, Bp[1] + 62 * k, "θ", 16, INK, weight="700", italic=True))
    return svg(500 * k, 210 * k, "".join(b))


def labeled_right_triangle(a_txt, b_txt, c_txt, ang_txt, at="A"):
    """right angle bottom left, angle shown at A (bottom right) or B (top left); a vertical, b horizontal, c hypotenuse"""
    Cp, Ap, Bp = (60, 170), (330, 170), (60, 40)
    b = [P([Cp, Ap, Bp], PALE["purple"], PURPLE, 2.2), corner(60, 170, 1, -1, 12),
         T(50, 108, a_txt, 13.5, INK, anchor="end", weight="700"), T(195, 194, b_txt, 13.5, INK, weight="700"),
         T(204, 94, c_txt, 13.5, INK, anchor="start", weight="700")]
    if at == "A":
        b.append(f'<path d="M288 170 A42 42 0 0 1 293 151" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        b.append(T(282, 160, ang_txt, 13, RED, anchor="end", weight="700"))
    else:
        b.append(f'<path d="M60 82 A42 42 0 0 0 95 63" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        b.append(T(72, 100, ang_txt, 13, RED, anchor="start", weight="700"))
    return svg(400, 206, "".join(b))


def offset_bend():
    """a conduit offset: two bends at the same angle; the travel is the hypotenuse"""
    import math
    a = math.radians(30)
    x0, y0, off = 40, 180, 110
    trav = off / math.sin(a)
    x1 = x0 + 140
    x2, y2 = x1 + trav * math.cos(a), y0 - off
    b = [L(x0, y0, x1, y0, INK, 10), L(x1, y0, x2, y2, INK, 10), L(x2, y2, x2 + 140, y2, INK, 10),
         L(x0, y0, x1, y0, "#9aa3b8", 6), L(x1, y0, x2, y2, "#9aa3b8", 6), L(x2, y2, x2 + 140, y2, "#9aa3b8", 6),
         L(x2, y2 + 8, x2, y0, RED, 1.6, "5 4"), L(x1, y0 + 8, x2, y0 + 8, BLUE, 1.6, "5 4"),
         T(x2 + 10, (y0 + y2) / 2 + 4, "offset (opposite)", 12.5, RED, anchor="start", weight="700"),
         T((x1 + x2) / 2 - 6, (y0 + y2) / 2 - 12, "travel (hypotenuse)", 12.5, GREEN, anchor="end", weight="700"),
         T((x1 + x2) / 2, y0 + 26, "run (adjacent)", 12.5, BLUE, weight="700"),
         f'<path d="M{x1 + 46} {y0} A46 46 0 0 0 {x1 + 46 * math.cos(a)} {y0 - 46 * math.sin(a)}" fill="none" stroke="{INK}" stroke-width="1.6"/>',
         T(x1 + 56, y0 - 10, "30°", 12.5, INK, anchor="start", weight="700")]
    return svg(x2 + 200, y0 + 40, "".join(b))


def ramp():
    b = [P([(40, 160), (440, 160), (440, 120)], PALE["gold"], GOLD, 2.2), corner(440, 160, -1, -1, 10),
         T(240, 182, "run 20 ft", 13, INK, weight="700"), T(450, 144, "rise 20 in", 13, INK, anchor="start", weight="700"),
         T(240, 128, "ramp", 13, INK, weight="700"),
         '<path d="M110 160 A70 70 0 0 0 109.7 153" fill="none" stroke="#1c2440" stroke-width="1.6"/>', T(122, 152, "θ", 15, RED, anchor="start", weight="700", italic=True)]
    return svg(560, 196, "".join(b))


def oblique():
    A_, B_, C_ = (50, 170), (400, 170), (150, 40)
    b = [P([A_, B_, C_], PALE["green"], GREEN, 2.2),
         T(36, 184, "A", 15, INK, weight="700"), T(414, 184, "B", 15, INK, weight="700"), T(150, 30, "C", 15, INK, weight="700"),
         T(225, 192, "c", 15, RED, weight="700", italic=True), T(86, 100, "b", 15, RED, weight="700", italic=True),
         T(290, 100, "a", 15, RED, weight="700", italic=True)]
    return svg(460, 204, "".join(b))
