#!/usr/bin/env python3
"""Simulator tests for hp-prime/GEOMETRY.txt (Chapter 8, Practical Plane
Geometry).

The expected answers are the textbook's worked examples and answers, the
class homework, and the same figures worked again here with plain
arithmetic, not taken from the program.  Each shape is filled in the way
the screen does it (setPart / setVal, then solveAll), and the touch and
keypad flow is played through: tapping the labels on the drawing, typing
on the keypad, the work page, combining two shapes.  Screenshots go to
docs/screens/.

Usage
  python3 tools/test_geometry.py              # test hp-prime/GEOMETRY.txt
  python3 tools/test_geometry.py FILE OUTDIR  # test another copy
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}
SQ3 = math.sqrt(3)

# shape number: (screen category, tile on that screen)
WHERE = {17: (1, 1), 18: (1, 2), 19: (1, 3), 20: (1, 4),
         1: (2, 1), 2: (2, 2), 3: (2, 3), 4: (2, 4),
         5: (3, 1), 6: (3, 2), 7: (3, 3), 8: (3, 4), 9: (3, 5),
         12: (4, 1), 13: (4, 2), 14: (4, 3), 15: (4, 4), 16: (4, 5),
         10: (5, 1), 11: (5, 2), 21: (7, 1), 22: (7, 2)}
SLUG = {1: "rectangle", 2: "square", 3: "parallelogram", 4: "trapezoid",
        5: "triangle_bh", 6: "right_triangle", 7: "heros_formula",
        8: "isosceles", 9: "equilateral", 10: "hexagon", 11: "polygon",
        12: "circle", 13: "semicircle", 14: "quarter_circle", 15: "ring",
        16: "sector", 17: "angle_math", 18: "angle_facts",
        19: "parallel_lines", 20: "triangle_angles", 21: "cost",
        22: "feet_inches"}


def tile(k):
    """centre of tile k (4 across, 2 down) on the home and shape screens"""
    return ((k - 1) % 4) * 80 + 40, 24 + ((k - 1) // 4) * 98 + 49


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def nums(text):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text.replace(",", ""))]


def close(a, b, rel=0.0001):
    """six significant figures on screen: agree to 1 part in 10,000"""
    return abs(a - b) <= rel * max(abs(b), 1e-12)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "GEOMETRY.txt")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "screens")
    os.makedirs(out, exist_ok=True)
    src = open(path, encoding="utf-8").read()
    checks = []

    def conv(a):
        if isinstance(a, (list, tuple)):
            return [conv(x) for x in a]
        return a if isinstance(a, str) else float(a)

    def fn_call(it, name, *args):
        params, body, _ = it.funcs[name]
        try:
            it.run_block(body, dict(zip(params, [conv(a) for a in args])))
        except ReturnSignal as r:
            return r.value
        return None

    def check(desc, fn):
        def run(it):
            try:
                ok = bool(fn(it))
            except Exception as exc:
                checks.append((f"{desc} ({type(exc).__name__}: {exc})", False))
                return
            checks.append((desc, ok))
        return ("check", run)

    def shot(name):
        return ("shot", os.path.join(out, name))

    class Res:
        """what the screen shows after solving: values by name, the answers
        and the steps of the work"""
        def __init__(self, it, p=1):
            t = int(it.g["gT"][p - 1])
            names = fn_call(it, "vNames", t)
            self.v = {}
            for k, nm in enumerate(names):
                if it.g["gK"][p - 1][k] == 1:
                    self.v[nm] = it.g["gC"][p - 1][k]
            self.ans = list(it.g["gAn"])
            self.work = list(it.g["gSt"])
            self.out = list(it.g["gOut"])

        def __getitem__(self, nm):
            return self.v[nm]

        def has(self, nm):
            return nm in self.v

        def a(self, text):
            """the first answer line that contains text"""
            for line in self.ans:
                if text in line:
                    return line
            raise KeyError(text)

        def anum(self, text, n=0):
            return nums(self.a(text).split("=", 1)[1] if "=" in self.a(text) else self.a(text))[n]

        def said(self, text):
            return any(text in line for line in self.out)

    def calc(it, t, vals=None, unit=None, **named):
        """shape t with only the given values (1-based index: value), the
        rest unknown, as if typed on the screen"""
        it.g["gCmb"] = 0.0
        fn_call(it, "loadEx", 1, t)
        fn_call(it, "clearVals")
        nm = fn_call(it, "vNames", t)
        kd = fn_call(it, "vKinds", t)
        for k, v in (vals or {}).items():
            fn_call(it, "setVal", 1, k, v)
        for key, v in named.items():
            k = nm.index(key.replace("_", " ").replace("pi", "π").replace("th", "θ")
                         if key not in nm else key) + 1
            fn_call(it, "setVal", 1, k, v)
        if unit is not None:
            it.g["gUnit"] = float(unit)
        assert kd is not None
        fn_call(it, "solveAll")
        return Res(it)

    def example(it, t):
        it.g["gCmb"] = 0.0
        fn_call(it, "loadEx", 1, t)
        fn_call(it, "solveAll")
        return Res(it)

    # ---- 8-1 angles ----------------------------------------------------
    def t_ang(it):
        r = example(it, 17)                            # 109°43' + 25°32'
        ok = "135°15'" in r.a("Answer") and r.said("134° 75'")
        r = calc(it, 17, {1: 109, 2: 43, 4: 25, 5: 32, 8: 5})   # third angle
        ok &= "44°45'" in r.a("Answer")
        r = calc(it, 17, {1: 14, 2: 32, 3: 48, 7: 2, 8: 3})     # BAD = 2 x BAC
        ok &= "29°5'36''" in r.a("Answer") and r.said("28° 64' 96''")
        r = calc(it, 17, {1: 62, 2: 12, 3: 37, 8: 9})
        ok &= close(r.anum("decimal") if "decimal" in " ".join(r.ans) else 0, 62 + 12 / 60 + 37 / 3600)
        r = calc(it, 17, {1: 90, 8: 9})
        ok &= any("right" in a for a in r.ans)
        r = calc(it, 17, {1: 52, 2: 10, 4: 23, 5: 45, 8: 2})    # borrow 60'
        return ok and "28°25'" in r.a("Answer")

    def t_facts(it):
        r = example(it, 18)                            # 125°
        ok = r.anum("Vertical") == 125 and r.anum("Adjacent") == 55
        ok &= r.anum("Each of") == 60                  # six bolt holes
        r = calc(it, 18, {1: 16, 2: 8})                # deck: 8 pieces in a half circle
        ok &= r.anum("Adjacent") == 164 and "22°30'" in r.a("180° in 8")
        r = calc(it, 18, {1: 42})                      # board joined at a right angle
        return ok and r.anum("Complement") == 48

    def t_par(it):
        r = example(it, 19)                            # 100° at angle 2
        ok = r.anum("1, 4, 5, 8") == 80 and r.anum("2, 3, 6, 7") == 100
        r = calc(it, 19, {1: 60, 2: 5})
        return ok and r.anum("1, 4, 5, 8") == 60 and r.anum("2, 3, 6, 7") == 120

    def t_tri(it):
        r = example(it, 20)                            # 60° and 52°
        ok = r["C"] == 68 and "Acute" in r.a("triangle")
        r = calc(it, 20, {1: 46.2, 2: 73 + 46 / 60, 4: 1})   # 46°12' and 73°46'
        ok &= close(r["C"], 180 - 46.2 - 73 - 46 / 60) and "C = 60°2'" in r.a("C =")
        r = calc(it, 20, {1: 109 + 43 / 60, 2: 25 + 32 / 60})
        ok &= close(r["C"], 44.75) and "Obtuse" in r.a("triangle")
        r = calc(it, 20, {2: 48, 4: 3})                # right triangle
        ok &= r["C"] == 90 and r["A"] == 42
        r = calc(it, 20, {1: 40, 4: 2})                # isosceles, apex 40°
        return ok and r["B"] == 70 and r["C"] == 70

    # ---- 8-2 polygons and quadrilaterals -------------------------------
    def t_peri(it):
        r = example(it, 11)                            # KLMN: 3 + 5 + 6 + 4
        ok = r["P"] == 18 and r.said("3 + 5 + 6 + 4")
        r = calc(it, 11, {1: 7.2, 2: 16.5, 3: 11.4, 4: 14.3, 10: 2})
        ok &= close(r["P"], 49.4)
        r = calc(it, 11, {1: 8.25, 2: 11.75, 3: 8.125, 4: 7.5, 5: 7, 10: 3})
        ok &= close(r["P"], 42.625)
        r = calc(it, 11, {1: 3, 2: 5, 3: 6, 9: 18, 10: 2})     # missing side
        return ok and r["s4"] == 4

    def t_rect(it):
        r = example(it, 1)                             # 9 in x 5 in
        ok = r["A"] == 45 and r["P"] == 28 and r.said("= 9 x 5")
        r = calc(it, 1, {1: 42, 2: 18})
        ok &= r["A"] == 756
        r = calc(it, 1, {1: 12, 3: 64})                # vents: W = A / L
        ok &= close(r["W"], 16 / 3)
        r = calc(it, 1, {1: 4.5, 2: 3.25})
        ok &= close(r["A"], 14.625)
        r = calc(it, 1, {1: 64.5, 2: 44.5})
        return ok and close(r["A"], 2870.25)

    def t_sq(it):
        r = example(it, 2)                             # 9 ft
        ok = r["A"] == 81 and r["P"] == 36
        r = calc(it, 2, {2: 64})
        ok &= r["s"] == 8
        r = calc(it, 2, {2: 927})
        ok &= close(r["s"], math.sqrt(927))
        r = calc(it, 2, {1: 7 / 3})
        ok &= close(r["A"], 49 / 9)
        r = calc(it, 2, {1: 24.5})                     # driveway
        return ok and close(r["A"], 600.25)

    def t_pgram(it):
        r = example(it, 3)                             # b 7 in, h 10 in
        ok = r["A"] == 70
        r = calc(it, 3, {1: 18, 2: 20, 3: 24})
        ok &= r["A"] == 360 and r["P"] == 84
        r = calc(it, 3, {1: 12, 2: 8, 3: 9})
        ok &= r["A"] == 96 and r["P"] == 42
        r = calc(it, 3, {1: 2.75, 2: 3.25})
        return ok and close(r["A"], 8.9375)

    def t_trap(it):
        r = example(it, 4)                             # 7, 19, h 6; sides 8, 9
        ok = r["A"] == 78 and r["P"] == 43 and r.said("(7 + 19) ÷ 2 x 6")
        r = calc(it, 4, {1: 8, 2: 26, 3: 12, 4: 15, 5: 15})
        ok &= r["A"] == 204 and r["P"] == 64
        r = calc(it, 4, {1: 11.75, 2: 8.25, 3: 10.5})
        return ok and r["A"] == 105

    def t_cost(it):
        r = example(it, 21)                            # 600.25 sq ft at $65 per sq yd
        ok = close(r.anum("Amount"), 600.25 / 9) and "$4335.14" in r.a("Cost")
        r = calc(it, 21, {1: 206, 2: 8, 3: 16, 4: 7})   # fence: 206 yd at $16 per ft
        ok &= r.anum("Amount") == 618 and "$9888.00" in r.a("Cost")
        r = calc(it, 21, {1: 400, 2: 7, 4: 7, 7: 8})   # posts every 8 ft around 400 ft
        ok &= r.anum("Posts") == 50
        r = calc(it, 21, {1: 210, 2: 2, 3: 0.59, 4: 2})
        ok &= "$123.90" in r.a("Cost")
        r = calc(it, 21, {1: 200, 2: 2, 4: 2, 5: 30, 6: 24})   # strip flooring
        ok &= r.anum("With waste") == 260 and r.anum("Packages") == 11
        r = calc(it, 21, {1: 200, 2: 2, 4: 7})
        return ok and any("do not match" in a for a in r.ans)

    # ---- 8-3 triangles, hexagons ---------------------------------------
    def t_pyth(it):
        r = example(it, 6)                             # 36 ft by 20 ft plot
        ok = close(r["c"], math.hypot(36, 20)) and r.said("√(20² + 36²)")
        r = calc(it, 6, {1: 8, 2: 15})
        ok &= r["c"] == 17
        r = calc(it, 6, {2: 13.8, 3: 22.3})
        ok &= close(r["a"], math.sqrt(22.3 ** 2 - 13.8 ** 2))
        r = calc(it, 6, {2: 10, 3: 12}, unit=2)        # ladder: 6.63 ft
        ok &= close(r["a"], math.sqrt(44)) and "6 ft 7 5/8 in" in r.a("a =")
        r = calc(it, 6, {1: 8.5, 2: 9.75})             # stairway
        ok &= close(r["c"], math.hypot(8.5, 9.75))
        r = calc(it, 6, {1: 15, 2: 20})                # homework 15-20-25
        ok &= r["c"] == 25 and r["A"] == 150 and r["P"] == 60
        r = calc(it, 6, {1: 8, 3: 17})
        ok &= r["b"] == 15
        r = calc(it, 6, {2: 24, 3: 25})
        ok &= r["a"] == 7
        r = calc(it, 6, {1: 3, 2: 4, 3: 5})
        ok &= "yes" in r.a("Right triangle?")
        r = calc(it, 6, {1: 3, 2: 4, 3: 6})
        return ok and "NOT a right triangle" in r.a("right triangle")

    def t_tria(it):
        r = example(it, 5)                             # b 13, h 8
        ok = r["A"] == 52 and r.said("13 x 8 ÷ 2")
        r = calc(it, 5, {1: 25, 2: 16})
        ok &= r["A"] == 200
        r = calc(it, 5, {1: 6.5, 2: 8})
        ok &= r["A"] == 26
        r = calc(it, 5, {1: 20, 5: 120})               # h from the area
        return ok and r["h"] == 12

    def t_hero(it):
        r = example(it, 7)                             # 13, 14, 15
        ok = r["A"] == 84 and r["s"] == 21 and r["P"] == 42 and r.said("7056")
        ok &= r.said("s - a = 21 - 13 = 8") and close(r["h"], 2 * 84 / 15)
        r = calc(it, 7, {1: 7, 2: 7, 3: 12})           # attic wall 7, 7, 12
        ok &= close(r["A"], 6 * math.sqrt(13))
        r = calc(it, 7, {1: 3, 2: 4, 3: 5})
        ok &= r["A"] == 6
        r = calc(it, 7, {1: 25, 2: 40, 3: 50})         # homework: P 115
        ok &= r["P"] == 115
        r = calc(it, 7, {1: 1, 2: 2, 3: 5})
        ok &= not r.has("A") and r.said("Not a triangle")
        r = calc(it, 7, {2: 4, 3: 5, 6: 12})           # a from the perimeter
        ok &= r["a"] == 3 and r["A"] == 6
        ok &= "Scalene, right" in r.a("triangle") and "90°" in r.a("Angles")
        r = calc(it, 7, {1: 25, 2: 40, 3: 50, 4: 18})  # homework: height 18 on side c
        ok &= r["A"] == 450 and r["P"] == 115 and "495.251" in r.a("Hero's")
        r = calc(it, 7, {1: 75, 2: 75, 3: 50, 4: 70})  # homework: 1,750 ft²
        ok &= r["A"] == 1750 and "Isosceles" in r.a("triangle")
        r = calc(it, 7, {1: 8, 2: 8, 3: 8})
        return ok and "60°, 60°, 60°" in r.a("Angles") and "Equilateral" in r.a("triangle")

    def t_iso(it):
        r = example(it, 8)                             # a 7, b 12
        ok = close(r["h"], math.sqrt(13)) and close(r["A"], 6 * math.sqrt(13)) and r["P"] == 26
        r = calc(it, 8, {1: 75, 2: 50})                # homework: P 200
        ok &= r["P"] == 200 and close(r["h"], math.sqrt(75 ** 2 - 25 ** 2))
        r = calc(it, 8, {2: 50, 3: 70})                # base and height
        return ok and r["A"] == 1750

    def t_equi(it):
        r = example(it, 9)                             # side 30
        ok = r["P"] == 90 and close(r["h"], 15 * SQ3) and close(r["A"], SQ3 / 4 * 900)
        r = calc(it, 9, {4: 90})
        ok &= r["s"] == 30
        r = calc(it, 9, {3: SQ3 / 4 * 900})
        ok &= close(r["s"], 30)
        r = calc(it, 9, {2: 15 * SQ3})
        return ok and close(r["s"], 30)

    def t_hex(it):
        r = calc(it, 10, {1: 0.4, 6: 1})               # side 0.40 in
        ok = close(r["A"], 1.5 * SQ3 * 0.16, 0.001) and close(r["P"], 2.4)
        r = example(it, 10)                            # 15 ft, handout 2.6 s²
        ok &= r["P"] == 90 and r["A"] == 585 and r["C"] == 30 and close(r["F"], 15 * SQ3)
        r = calc(it, 10, {5: 90, 6: 2})
        ok &= r["s"] == 15
        r = calc(it, 10, {4: 585, 6: 2})
        ok &= close(r["s"], 15)
        r = calc(it, 10, {3: 10, 6: 2})
        return ok and r["s"] == 5

    # ---- 8-4 circles ----------------------------------------------------
    def t_circ(it):
        r = example(it, 12)                            # r 2.70 in, π = 3.14
        ok = close(r["A"], 3.14 * 2.7 ** 2) and close(r["C"], 3.14 * 5.4) and r.said("3.14 x 2.7²")
        r = calc(it, 12, {2: 10, 5: 1})
        ok &= close(r["A"], math.pi * 25) and "= 25π" in r.a("A =") and "= 10π" in r.a("C =")
        ok &= "π" not in r.a("r =")                     # 5 is not a tidy number of π
        r = calc(it, 12, {3: 10 * math.pi, 5: 1})
        ok &= close(r["r"], 5)
        r = calc(it, 12, {4: 25 * math.pi, 5: 1})
        ok &= close(r["r"], 5)
        r = calc(it, 12, {2: 30, 5: 2})                # homework: d 30 m
        ok &= close(r["C"], 94.2) and close(r["A"], 706.5)
        r = calc(it, 12, {1: 10, 5: 2})
        ok &= close(r["C"], 62.8) and close(r["A"], 314)
        r = calc(it, 12, {4: 1000, 5: 1})              # 17.84 ft (the π key)
        ok &= abs(r["r"] - 17.84) < 0.005
        r = calc(it, 12, {3: 500, 5: 2})
        return ok and abs(r["r"] - 79.62) < 0.005

    def t_semi(it):
        r = example(it, 13)                            # d 10
        ok = r["r"] == 5 and close(r["arc"], 5 * math.pi) and close(r["A"], 12.5 * math.pi)
        ok &= close(r["P"], 5 * math.pi + 10)
        r = calc(it, 14, {1: 10, 5: 1})                # quarter circle r 10
        ok &= close(r["arc"], 5 * math.pi) and close(r["A"], 25 * math.pi) and close(r["P"], 5 * math.pi + 20)
        r = calc(it, 13, {5: 12.5 * math.pi, 6: 1})
        return ok and close(r["r"], 5)

    def t_ring(it):
        r = example(it, 15)                            # flowerbed 8.5 ft, lawn 12 ft wide
        ok = close(r["R"], 20.5) and close(r["A"], math.pi * (20.5 ** 2 - 8.5 ** 2))
        ok &= "= 348π" in r.a("A =")
        r = calc(it, 15, {1: 8.5, 3: 12, 5: 2})
        ok &= close(r["A"], 3.14 * 348)
        r = calc(it, 15, {1: 8.5, 2: 20.5, 5: 1})
        ok &= close(r["w"], 12)
        r = calc(it, 15, {1: 8.5, 4: math.pi * 348, 5: 1})
        ok &= close(r["R"], 20.5) and close(r["w"], 12)
        r = calc(it, 15, {3: 12, 4: math.pi * 348, 5: 1})
        return ok and close(r["r"], 8.5)

    def t_sect(it):
        r = example(it, 16)                            # r 10, 90°
        ok = close(r["arc"], 5 * math.pi) and close(r["A"], 25 * math.pi)
        ok &= close(r["chord"], 10 * math.sqrt(2)) and close(r["P"], 5 * math.pi + 20)
        r = calc(it, 16, {1: 10, 2: 180, 7: 1})
        ok &= close(r["arc"], 10 * math.pi)
        r = calc(it, 16, {1: 10, 3: 5 * math.pi, 7: 1})     # angle from the arc
        ok &= close(r["θ"], 90)
        r = calc(it, 16, {2: 90, 5: 25 * math.pi, 7: 1})
        ok &= close(r["r"], 10)
        r = calc(it, 16, {3: 5 * math.pi, 5: 25 * math.pi, 7: 1})
        return ok and close(r["r"], 10) and close(r["θ"], 90)

    def t_ftin(it):
        r = example(it, 22)                            # 4 ft 6 in
        ok = "4.5 ft" in r.a("4 ft 6 in") and "54 in" in r.a("4 ft 6 in")
        r = calc(it, 22, {1: 11, 2: 9})
        ok &= "11.75 ft" in r.a("11 ft 9 in")
        r = calc(it, 22, {3: 6.63})                    # 6.63 ft = 6 ft 7 9/16 in
        ok &= "6 ft 7" in r.a("6.63 ft")
        r = calc(it, 22, {4: 600.25, 5: 2})
        return ok and close(nums(r.a("sq yd").split("=")[-1])[0], 600.25 / 9)

    # ---- word problems: given an area, perimeter, ... find the rest ----
    def t_word(it):
        ok = True
        r = calc(it, 1, {3: 800, 4: 120})              # A and P: 40 x 20
        ok &= close(r["L"], 40) and close(r["W"], 20)
        r = calc(it, 1, {1: 40, 4: 120})
        ok &= r["W"] == 20 and r["A"] == 800
        r = calc(it, 1, {3: 48, 5: 10})                # A and diagonal: 8 x 6
        ok &= close(r["L"], 8) and close(r["W"], 6)
        r = calc(it, 1, {1: 8, 5: 10})
        ok &= close(r["W"], 6)
        r = calc(it, 2, {3: 80})                       # square from P
        ok &= r["s"] == 20 and r["A"] == 400
        r = calc(it, 2, {4: 10 * math.sqrt(2)})
        ok &= close(r["s"], 10)
        r = calc(it, 3, {1: 50, 4: 900})               # parallelogram h from A
        ok &= r["h"] == 18
        r = calc(it, 3, {2: 18, 3: 20, 5: 140})        # b from P
        ok &= r["b"] == 50 and r["A"] == 900
        r = calc(it, 4, {1: 10, 3: 18, 6: 360})        # trapezoid b2 from A
        ok &= r["b2"] == 30
        r = calc(it, 4, {1: 10, 2: 30, 6: 360})
        ok &= r["h"] == 18
        r = calc(it, 4, {1: 10, 2: 30, 3: 18, 5: 22, 7: 84})
        ok &= r["c"] == 22
        r = calc(it, 6, {1: 15, 4: 150})               # leg from the area
        ok &= r["b"] == 20 and r["c"] == 25
        r = calc(it, 6, {3: 25, 4: 150})               # hypotenuse and area
        ok &= close(max(r["a"], r["b"]), 20) and close(min(r["a"], r["b"]), 15)
        return ok

    # ---- combining two shapes -----------------------------------------
    def combo(it, n):
        fn_call(it, "openCombo")
        fn_call(it, "comboEx", n)
        fn_call(it, "solveAll")
        return list(it.g["gAn"]), list(it.g["gOut"])

    def total(ans, what):
        for a in ans:
            if a.startswith("TOTAL " + what):
                return nums(a.split("=")[1])[0]
        raise KeyError(what)

    def t_combo(it):
        ans, out = combo(it, 1)                        # house: 20 x 12 + roof b 20 h 8
        roof = math.sqrt(8 ** 2 + 10 ** 2)
        ok = total(ans, "AREA") == 320 and close(total(ans, "PERIMETER"), 20 + 2 * 12 + 2 * roof)
        ok &= any(s.startswith("Edge A and B share") for s in out)
        ans, out = combo(it, 2)                        # 30 x 16 + half circle d 16
        ok &= close(total(ans, "AREA"), 480 + 32 * math.pi)
        ok &= close(total(ans, "PERIMETER"), 30 + 30 + 16 + 8 * math.pi)
        ans, out = combo(it, 3)                        # L-shaped room
        ok &= total(ans, "AREA") == 492 and total(ans, "PERIMETER") == 2 * (21 + 36)
        ans, out = combo(it, 4)                        # square 20 with a hole r 5
        ok &= close(total(ans, "AREA"), 400 - 25 * math.pi)
        ans, out = combo(it, 5)                        # hexagon 20 (2.6 s²) minus square 20
        ok &= total(ans, "AREA") == 640
        ans, out = combo(it, 6)                        # room 20 x 14 + closet 6 x 4 + bay d 8
        ok &= close(total(ans, "AREA"), 280 + 24 + 8 * math.pi)
        ok &= close(total(ans, "PERIMETER"), 68 + 4 * math.pi)
        ok &= sum(x.startswith("Edge A and") for x in out) == 2
        # two holes: square 20 with round holes r 5 and r 3
        fn_call(it, "comboEx", 4)
        fn_call(it, "setPart", 3, 12, [3, 0, 0, 0, 1])
        it.g["gQm"] = 3.0
        fn_call(it, "solveAll")
        ans = list(it.g["gAn"])
        ok &= close(total(ans, "AREA"), 400 - 34 * math.pi) and total(ans, "PERIMETER") == 80
        # a notch: the L-room's 10 x 24 cut out of the side instead of added on
        fn_call(it, "comboEx", 3)
        it.g["gPm"] = 2.0
        fn_call(it, "solveAll")
        ans = list(it.g["gAn"])
        ok &= total(ans, "AREA") == 252 - 240
        it.g["gCmb"] = 0.0
        it.g["gScr"] = 1.0
        return ok

    # ---- the screens, played through ----------------------------------
    def hot_xy(it, name, p=1):
        """centre of the label for value name of part p on the screen"""
        t = int(it.g["gT"][p - 1])
        k = fn_call(it, "vNames", t).index(name) + 1
        for j in range(len(it.g["gHp"])):
            if it.g["gHp"][j] == p and it.g["gHi"][j] == k and it.g["gHk"][j] == 0:
                return ((it.g["gHx1"][j] + it.g["gHx2"][j]) / 2, (it.g["gHy1"][j] + it.g["gHy2"][j]) / 2)
        raise KeyError(name)

    def tap_hot(name, p=1):
        """a tap on a label, where the screen last drew it"""
        def find(it):
            x, y = hot_xy(it, name, p)
            it.events[0:0] = tap(round(x), round(y))
        return [("check", find)]

    def pick_hot(name, p=1):
        """press Right until the label is picked (yellow)"""
        def find(it):
            t = int(it.g["gT"][p - 1])
            k = fn_call(it, "vNames", t).index(name) + 1
            n = len(it.g["gHp"])
            reg = [(it.g["gHp"][j], it.g["gHi"][j], it.g["gHk"][j]) for j in range(n)]
            cur = reg.index((it.g["gSelP"], it.g["gSelI"], it.g["gSelK"]))
            want = reg.index((p, k, 0))
            it.events[0:0] = [KEY["right"]] * ((want - cur) % n)
        return [("check", find)]

    def labels_apart(it):
        """no two labels on the screen cover each other"""
        n = len(it.g["gHp"])
        b = [(it.g["gHx1"][j], it.g["gHy1"][j], it.g["gHx2"][j], it.g["gHy2"][j]) for j in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if b[i][0] < b[j][2] and b[j][0] < b[i][2] and b[i][1] < b[j][3] and b[j][1] < b[i][3]:
                    return False
        return n > 0

    def val(it, p, k):
        return it.g["gV"][p - 1][k - 1]

    tests = [("8-1 angles: degrees, minutes, seconds", t_ang),
             ("8-1 vertical, adjacent, complement, n equal parts", t_facts),
             ("8-1 parallel lines and a transversal", t_par),
             ("8-1 triangle angles add to 180°", t_tri),
             ("8-2 perimeter of a polygon, missing side", t_peri),
             ("8-2 rectangle", t_rect), ("8-2 square", t_sq),
             ("8-2 parallelogram", t_pgram), ("8-2 trapezoid", t_trap),
             ("8-2 cost of materials, posts, packages", t_cost),
             ("8-3 Pythagorean theorem", t_pyth), ("8-3 triangle b x h", t_tria),
             ("8-3 Hero's formula", t_hero), ("8-3 isosceles triangle", t_iso),
             ("8-3 equilateral triangle", t_equi), ("8-3 regular hexagon", t_hex),
             ("8-4 circle", t_circ), ("8-4 semicircle and quarter circle", t_semi),
             ("8-4 ring", t_ring), ("8-4 sector, arc and chord", t_sect),
             ("feet and inches, area units", t_ftin),
             ("word problems: work back from A, P, d ...", t_word),
             ("combined shapes: add, notch, hole", t_combo)]

    ev = [shot("geom_home.png"),
          check("home screen: 8 tiles", lambda it: it.g["gScr"] == 1)]
    ev += [check(d, f) for d, f in tests]
    # every shape: open it, no labels on top of each other, screenshot
    for t, (c, k) in sorted(WHERE.items(), key=lambda x: x[1]):
        if k == 1:
            ev += [*tap(*tile(c)), shot(f"geom_cat{c}.png")]
        ev += [*tap(*tile(k)),
               check(f"{SLUG[t]}: opens with the textbook example",
                     lambda it, t=t: it.g["gScr"] == 3 and it.g["gT"][0] == t and len(it.g["gOut"]) > 3),
               check(f"{SLUG[t]}: labels do not cover each other", labels_apart),
               shot(f"geom_{t}_{SLUG[t]}.png"),
               *tap(*menu(5))]
        if k == len([1 for cc, _ in WHERE.values() if cc == c]):
            ev += [*tap(290, 10)]
    # rectangle: tap the W label, type 8 in the box, then keypad entry on A
    ev += [*tap(*tile(2)), *tap(*tile(1)),
           check("rectangle: L is picked first and drawn yellow", lambda it: it.g["gSelI"] == 1),
           *tap_hot("W"), ("dialog", 8),
           check("tap W, enter 8: W = 8, A = 72", lambda it: val(it, 1, 2) == 8 and it.g["gC"][0][2] == 72),
           KEY["right"],
           check("Right picks the next label", lambda it: it.g["gSelI"] != 2),
           *tap_hot("L"), ("dialog", 0),
           check("0 in a box makes it unknown (?)", lambda it: it.g["gG"][0][0] == 0 and it.g["gK"][0][0] == 0),
           *tap_hot("A"), ("dialog", 96),
           check("word problem: A = 96 and W = 8 gives L = 12",
                 lambda it: it.g["gC"][0][0] == 12 and it.g["gK"][0][0] == 1),
           *pick_hot("P"), *keys("50"),
           check("typing on the keypad shows in the label", lambda it: it.g["gEnt"] == 1),
           shot("geom_typing.png"),
           KEY["enter"],
           check("Enter keeps it: P = 50", lambda it: val(it, 1, 4) == 50),
           *tap(*menu(3)),
           check("CLEAR: every size back to ?", lambda it: all(g == 0 for g in it.g["gG"][0][:5])),
           *tap(*menu(2)),
           check("EXAMPLE puts 9 x 5 back", lambda it: val(it, 1, 1) == 9 and val(it, 1, 2) == 5),
           *tap(*menu(1)), ("dialog", 1), ("dialog", 2),
           check("SETUP, units: ft", lambda it: it.g["gUnit"] == 2 and "ft²" in " ".join(it.g["gAn"])),
           *tap_hot("L"), ("dialog", [10, 6]),
           check("a length in feet and inches: L 10 ft 6 in = 10.5 ft",
                 lambda it: val(it, 1, 1) == 10.5 and it.g["gC"][0][2] == 52.5),
           *tap(*menu(1)), ("dialog", 2), ("dialog", 4),
           check("SETUP, round to hundredths: d = 11.6297 ft  ≈ 11.63",
                 lambda it: it.g["gRnd"] == 4 and any("≈ 11.63" in a for a in it.g["gAn"])),
           check("rounding shows in the work too", lambda it: any("≈ 11.63" in a for a in it.g["gSt"])),
           *tap(*menu(1)), ("dialog", 2), ("dialog", 1),
           *tap(*menu(2)),
           KEY["down"],
           check("Down scrolls the work", lambda it: it.g["gTop"] == 2),
           *tap(160, 180), shot("geom_work.png"),
           check("tap the work: the whole work on one page", lambda it: it.g["gScr"] == 3),
           KEY["esc"],
           *tap(*menu(4)), KEY["esc"],
           KEY["help"], shot("geom_help.png"), KEY["esc"],
           check("Help closes back to the shape", lambda it: it.g["gScr"] == 3),
           KEY["esc"], KEY["esc"]]
    # combined shapes on the screen
    ev += [*tap(*tile(6)),
           check("Combine 2 shapes opens the house example", lambda it: it.g["gCmb"] == 1 and it.g["gT"] == [1, 8, 0]),
           check("combined: labels do not cover each other", labels_apart),
           shot("geom_combo_house.png"),
           *tap(*menu(1)), ("dialog", 7), shot("geom_combo_halfcircle.png"),
           check("SHAPES: rectangle + half circle", lambda it: it.g["gT"] == [1, 13, 0] and it.g["gPs"] == 2),
           *tap(*menu(1)), ("dialog", 8),
           *tap(*menu(1)), ("dialog", 5), ("dialog", 4.75), shot("geom_combo_lroom.png"),
           check("L-shaped room at $4.75 per ft²: 492 x 4.75 = $2337.00",
                 lambda it: any(a.startswith("COST = $2337.00") for a in it.g["gAn"])),
           *tap(*menu(2)), ("dialog", 2), ("dialog", 2), ("dialog", 3), shot("geom_combo_notch.png"),
           check("PLACE: a notch out of the right side, at the end",
                 lambda it: it.g["gPm"] == 2 and it.g["gPs"] == 2 and it.g["gPa"] == 3),
           check("a 24 ft deep notch in a 21 ft wide room is flagged",
                 lambda it: "bigger than A" in it.g["gMsg"] and "bigger than A" in " ".join(it.g["gOut"])),
           *tap(*menu(1)), ("dialog", 9), shot("geom_combo_hole.png"),
           *tap(*menu(1)), ("dialog", 10), shot("geom_combo_hexagon.png"),
           *tap(*menu(1)), ("dialog", 11), shot("geom_combo_three.png"),
           check("SHAPES: a room with a closet and a bay window (3 shapes)",
                 lambda it: it.g["gT"] == [1, 1, 13] and close(total(it.g["gAn"], "AREA"), 304 + 8 * math.pi)),
           check("three shapes: labels do not cover each other", labels_apart),
           *tap(*menu(2)), ("dialog", 2), ("dialog", 3),
           check("PLACE asks which shape; C cut out as a hole", lambda it: it.g["gQm"] == 3 and it.g["gPm"] == 1),
           check("a hole takes its area off: 304 - 8π",
                 lambda it: close(total(it.g["gAn"], "AREA"), 304 - 8 * math.pi)),
           shot("geom_combo_three_hole.png"),
           *tap(*menu(1)), ("dialog", 3), ("dialog", 1),
           check("SHAPES: shape C taken away again", lambda it: it.g["gT"][2] == 0 and total(it.g["gAn"], "AREA") == 304),
           *tap(*menu(1)), ("dialog", 1), ("dialog", 3),
           check("SHAPES: change A to a parallelogram", lambda it: it.g["gT"][0] == 3),
           *tap(*menu(1)), ("dialog", 2), ("dialog", 12),
           check("SHAPES: change B to a semicircle", lambda it: it.g["gT"][1] == 13),
           *tap(*menu(1)), ("dialog", 6),
           *tap(*menu(4)), shot("geom_combo_work.png"), KEY["esc"],
           KEY["esc"],
           check("Esc: back to the home screen", lambda it: it.g["gScr"] == 1),
           *tap(*tile(8)), shot("geom_formulas.png"), KEY["esc"],
           KEY["help"], KEY["esc"],
           -1,
           *tap(295, 10)]

    it = Interp(src, ev)
    try:
        it.start("GEOMETRY")
        finished = True
    except StopSim:
        finished = False
    bad = [d for d, ok in checks if not ok]
    for d, ok in checks:
        print(("ok    " if ok else "FAIL  ") + d)
    print(f"{len(checks) - len(bad)}/{len(checks)} checks passed; program "
          + ("ended through EXIT" if finished else "did NOT end"))
    if bad or not finished:
        sys.exit(1)


if __name__ == "__main__":
    main()
