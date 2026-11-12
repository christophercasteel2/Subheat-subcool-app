#!/usr/bin/env python3
"""Simulator tests for hp-prime/TECHMATH.txt (Applied Technical Math, the
whole semester as a notebook).

The expected answers are the class's own: the graded Chapter 5 and
Chapter 7 exams, the classwork sheets, the conversion practice key, the
place-value worksheet and the handouts, worked again here with plain
arithmetic.  Pages are filled in the way the screen does it (the text of
each blank, then build), and the touch and keypad flow is played through.
Screenshots go to docs/screens/.

Usage
  python3 tools/test_techmath.py              # test hp-prime/TECHMATH.txt
  python3 tools/test_techmath.py FILE OUTDIR  # test another copy
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
ENTER, ESC, RIGHT, LEFT, DOWN, UP = 30, 4, 8, 7, 12, 2
DIV, SPACE, MINUS, PLUS, PAREN, SQ, POW, SHIFT, ALPHA, VIEW, MENU, DEL = 35, 49, 45, 50, 28, 26, 20, 41, 36, 9, 13, 19

# the class answer for the blank left empty in each formula's example
FORMULA = [math.sqrt(5 ** 5), 4 * 500 * 3 / 1.085, 3.14 * 25 * 9 / 4, 16 * 14 / 30, 3882 / (52.6 * 9), 1250,
           11 / 32, 3.14 * 6 * 2500 / 12, 6000 * 12 / (3.14 * 8), 25 * 6 ** 4 / 144, 12500 / 0.175,
           9 * 40000 / 87, 40, 170 * 224 * 3800 / 792000, 360, 1240 / 220, 800 / 62.4, 343 / 200, 18, 21,
           5.5, 22000, 32.5, 0.125, 28.75, 18.18, 10.3 / 0.52, 12, -95, 115.2, 1 / 48, 4, 270.641, 84.125]


def keys(text):
    return [DIGIT[ch] for ch in text]


def tabxy(k):
    return 308, 2 + (k - 1) * 37 + 17


def close(a, b, rel=0.0001):
    return abs(a - b) <= rel * max(abs(b), 1e-12)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "TECHMATH.txt")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "screens")
    os.makedirs(out, exist_ok=True)
    src = open(path, encoding="utf-8").read()
    prog = re.search(r"^EXPORT (\w+)\(\)", src, re.M).group(1)
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

    def page(it, t, p, texts=None, rnd=None, opt=None):
        """open a page, type the given blanks (1-based: text) and work it out"""
        fn_call(it, "openPage", t, p)
        it.g["gBt"] = [""] * 12
        for k, s in (texts or {}).items():
            it.g["gBt"][k - 1] = s
        if rnd is not None:
            it.g["gOpt"][0] = float(rnd)
        for k, v in (opt or {}).items():
            it.g["gOpt"][k - 1] = float(v)
        it.g["gDirty"] = 1.0
        fn_call(it, "build")
        return list(it.g["gBv"]), list(it.g["gWk"])

    def var(it, name):
        return it.g["gVv"][it.g["gVn"].index(name)]

    def home(it):
        fn_call(it, "openPage", 0, 0)

    # ---- the Chapter 7 exam ------------------------------------------
    def t_exam7(it):
        _, w = page(it, 4, 1, {1: "(12 - 3(4² ÷ 2³) + 9) ÷ (5² - 10)"})
        ok = w[0] == "(12 - 3(4² ÷ 2³) + 9) ÷ (5² - 10)" and w[-1] == "Answer = 1"
        ok &= "= (12 - 3(16 ÷ 8) + 9) ÷ (25 - 10)" in w and "= 15 ÷ 15" in w
        _, w = page(it, 4, 36)                         # 2C + 1.6(D + d) + (D + d)/(4C)
        it.g["gBt"][:4] = ["", "30", "10", "5"]
        it.g["gDirty"] = 1.0
        fn_call(it, "build")
        w = list(it.g["gWk"])
        ok &= "X = 2(30) + 1.6(10 + 5) + (10 + 5) ÷ (4(30))" in w and "X = 84.125" in w
        ok &= any("84 1/8" in x for x in w)
        b, w = page(it, 4, 3, {2: "15", 3: "3"}, rnd=1)       # pipes
        ok &= "N = √((15 ÷ 3)^5)" in w and w[-1] == "N ≈ 56  (nearest whole number)" and b[0] == "56"
        b, w = page(it, 4, 4, {2: "2", 3: "500", 4: "3"}, rnd=1)   # feeder belt
        ok &= "C = (2)²(500)(3) ÷ 1.085" in w and b[0] == "5530"
        b, w = page(it, 4, 5, {2: "25", 3: "3"}, rnd=1)       # piston
        ok &= "F = (3.14)(25)(3)² ÷ 4" in w and b[0] == "177"
        b, w = page(it, 4, 6, {2: "16", 3: "6", 4: "8"}, rnd=3)    # capacitors
        ok &= b[0] == "7.47"
        b, w = page(it, 4, 7, {1: "3882", 2: "52.6", 3: "9"}, rnd=2)   # trailer
        ok &= "3882 = (52.6)(9)H" in w and "3882 = 473.4H" in w and b[3] == "8.2"
        b, w = page(it, 4, 8, {1: "3500", 3: "500"}, rnd=2)   # fence
        ok &= "3500 = 2L + 1000" in w and "2500 = 2L" in w and b[1] == "1250"
        b, w = page(it, 4, 9, {1: "7/8"})                     # Pittsburgh lock
        ok &= w[:2] == ["A = 2W + 3/16", "7/8 = 2W + 3/16"] and "11/16 = 2W" in w
        ok &= "W = 11/32" in w and b[1] == "11/32"
        b, w = page(it, 5, 6, {1: "15", 2: "20", 3: "25"})    # bonus: Hero's formula
        return ok and var(it, "s") == 30 and var(it, "A") == 150

    # ---- every class formula with the class numbers --------------------
    def t_formulas(it):
        ok = int(fn_call(it, "fmN")) == len(FORMULA)
        bad = []
        for k, want in enumerate(FORMULA, 1):
            f = fn_call(it, "fmDef", k)
            texts = {j + 1: s for j, s in enumerate(f[5]) if s}
            page(it, 4, k + 2, texts, rnd=0)
            name = f[2][[j for j, s in enumerate(f[5]) if not s][0]]
            got = var(it, name)
            if not close(got, want):
                bad.append((k, f[0], got, want))
        if bad:
            raise AssertionError(bad)
        return ok

    def t_rounding_asked(it):
        b, _ = page(it, 4, 10, {2: "6", 3: "2500"}, rnd=6)    # grinding wheel, nearest hundred
        ok = b[0] == "3900"
        b, _ = page(it, 4, 13, {2: "12500", 3: "0.175"}, rnd=6)
        ok &= b[0] == "71400"
        b, _ = page(it, 4, 11, {1: "6000", 2: "8"}, rnd=6)
        ok &= b[2] == "2900"
        b, w = page(it, 4, 28, {1: "82", 3: "8", 4: "6"}, rnd=1)   # belt: nearest inch
        return ok and b[1] == "18" and "82 = 2d + 45.64" in w and "36.36 = 2d" in w

    def t_solve(it):
        b, w = page(it, 4, 24, {1: "32", 3: "76"})            # T = -0.002H + G
        ok = "-44 = -0.002H" in w and b[1] == "22000"
        b, w = page(it, 4, 17, {1: "0.8", 3: "450"})          # Ohm's law, E on top
        ok &= b[1] == "360"
        b, w = page(it, 4, 17, {1: "0.8", 2: "360"})          # R on the bottom
        ok &= b[2] == "450"
        b, w = page(it, 5, 8, {2: "5", 3: "13"})              # right triangle: a leg
        ok &= "square both sides" in w and "169 = a² + 25" in w and b[0] == "12"
        b, w = page(it, 5, 9, {4: "500"})                     # hexagon side from its area
        ok &= abs(var(it, "s") - math.sqrt(500 / 2.6)) < 1e-9 and "192.308 = s²" in w
        b, w = page(it, 4, 6, {1: "7.47", 3: "6", 4: "8"})    # a letter that appears twice
        return ok and any("more than once" in x for x in w) and abs(var(it, "C1") - 16.02) < 0.05

    def t_anyformula(it):
        b, w = page(it, 4, 2, {1: "R", 2: "0.02T + 5", 3: "5.24"})
        ok = it.g["gNB"] == 4 and b[3] == "12" and "0.24 = 0.02T" in w
        b, w = page(it, 4, 2, {1: "P + 2T", 2: "C", 3: "2.875", 5: "3.125"})
        ok &= b[3] == "0.125"
        b, w = page(it, 4, 2, {1: "A", 2: "s²", 3: "81"})
        ok &= b[3] == "9"
        b, w = page(it, 4, 2, {1: "R", 2: "0.02T +"})
        return ok and it.g["gBe"][1] == 1

    def t_order(it):
        _, w = page(it, 4, 1, {1: "5 - 3(4² ÷ 2) + 30"})      # the class notes
        ok = w == ["5 - 3(4² ÷ 2) + 30", "= 5 - 3(16 ÷ 2) + 30", "= 5 - 3 × 8 + 30", "= 5 - 24 + 30",
                   "= -19 + 30", "= 11", "Answer = 11"]
        _, w = page(it, 4, 1, {1: "6 + 4 ÷ 2"})
        ok &= w[-1] == "Answer = 8"
        _, w = page(it, 4, 1, {1: "78 3/4 - 31 3/8 - 11.25"})  # Ch. 5 exam, missing length
        ok &= "Answer = 36 1/8" in w and any("36.125" in x for x in w)
        _, w = page(it, 4, 1, {1: "5 ÷ 0"})
        ok &= any("divide by 0" in x for x in w)
        _, w = page(it, 4, 1, {1: "√(30(30 - 15)(30 - 20)(30 - 25))"})
        return ok and w[-1] == "Answer = 150"

    # ---- the Chapter 5 exam and its worksheets -------------------------
    def t_place(it):
        _, w = page(it, 1, 1, {1: "902468.7351"})
        want = {"9": "hundred-thousands", "0": "ten-thousands", "2": "thousands", "4": "hundreds", "6": "tens",
                "8": "ones", "7": "tenths", "3": "hundredths", "5": "thousandths", "1": "ten-thousandths"}
        got = {x.split()[0]: x.split()[1] for x in w if x[0].isdigit()}
        ok = got == want
        _, w = page(it, 1, 1, {1: "91,234.5678"})
        got = {x.split()[1]: x.split()[0] for x in w if x[0].isdigit()}
        return ok and got["hundredths"] == "6" and got["thousands"] == "1" and got["ten-thousandths"] == "8"

    def t_round(it):
        _, w = page(it, 1, 2, {1: "9372.6485"})
        r = dict(x.replace("nearest ", "").split(":  ") for x in w if x.startswith("nearest"))
        ok = r == {"thousand": "9000", "hundred": "9400", "ten": "9370", "whole number": "9373",
                   "tenth": "9372.6", "hundredth": "9372.65", "thousandth": "9372.649"}
        _, w = page(it, 1, 2, {1: "86.5478"})
        r = dict(x.replace("nearest ", "").split(":  ") for x in w if x.startswith("nearest"))
        ok &= r["tenth"] == "86.5" and r["whole number"] == "87" and r["thousandth"] == "86.548"
        ok &= r["hundredth"] == "86.55"
        _, w = page(it, 1, 2, {1: "999.96"})
        r = dict(x.replace("nearest ", "").split(":  ") for x in w if x.startswith("nearest"))
        return ok and r["tenth"] == "1000.0" and r["ten"] == "1000"

    def t_fdp(it):
        b, _ = page(it, 1, 3, {1: "5/8"})
        ok = b[1] == "0.625" and b[2] == "62.5"
        b, w = page(it, 1, 3, {3: "37.5"})
        ok &= b[1] == "0.375" and b[0] == "3/8" and "0.375 = 375/1000" in w
        b, _ = page(it, 1, 3, {2: ".167"})
        return ok and b[2] == "16.7" and b[0] == "167/1000"

    def t_tol(it):
        b, w = page(it, 1, 4, {1: "0.81", 2: "0.003", 5: "13/16"})
        ok = b[2] == "0.807" and b[3] == "0.813" and any(x.startswith("YES: 0.8125") for x in w)
        b, w = page(it, 1, 4, {1: "0.81", 2: "0.003", 5: "0.82"})
        ok &= any(x.startswith("NO") for x in w)
        b, w = page(it, 1, 5, {1: "78 3/4", 2: "11.25", 3: "31 3/8"})   # missing length
        return ok and b[4] == "36 1/8" and "78 3/4 = 42 5/8 + M" in w

    def t_convert(it):
        def cv(p, k, text, rnd=2):
            b, _ = page(it, 2, p, {k: text}, rnd=rnd)
            return b
        ok = cv(2, 1, "1000")[1] == "6.9"                     # the practice sheet
        ok &= cv(2, 3, "15.5")[1] == "139.5" and cv(2, 2, "24")[0] == "3456" and cv(2, 1, "1500")[2] == "1.2"
        ok &= cv(3, 2, "2500")[2] == "92.6" and cv(3, 1, "5000")[1] == "2.9" and cv(3, 3, "23.5")[1] == "634.5"
        ok &= cv(3, 2, "5.5")[0] == "9504" and cv(3, 2, "5")[3] == "37.4" and cv(3, 1, "1500")[3] == "6.5"
        ok &= cv(3, 4, "55")[1] == "7.4" and cv(3, 4, "5")[0] == "1155"
        ok &= cv(3, 3, "150")[1] == "4050" and cv(2, 2, "750")[2] == "83.3" and cv(3, 2, "50")[3] == "374"
        ok &= cv(1, 6, "50")[0] == "19.7" and cv(5, 5, "50")[2] == "53" and cv(4, 2, "185")[4] == "83.9"
        b, w = page(it, 2, 1, {8: "5"}, rnd=1)                # bonus: 5 km to inches
        ok &= b[0] == "196850" and "500000 cm ÷ 2.54 = 196850 in" in w
        b, w = page(it, 2, 3, {1: "5000"}, rnd=2)
        ok &= "5000 cu in ÷ 1728 = 2.89352 cu ft" in w        # 1728, not the key's 1296
        b, _ = page(it, 2, 6, {7: "250"})                     # metric stairs
        ok &= b[5] == "25"
        b, _ = page(it, 2, 6, {4: ".25"}, opt={3: 2})
        ok &= b[6] == "250"
        b, _ = page(it, 2, 6, {5: "250"}, opt={3: 1})
        return ok and b[2] == "2.5"

    def t_ruler(it):
        _, w = page(it, 2, 7, {1: "1", 2: "11", 3: "4", 4: "6"})
        ok = "= 1 11/16 in" in w and "= 46 mm" in w
        _, w = page(it, 2, 7, {1: "2", 2: "6"})
        ok &= "= 2 3/8 in" in w
        _, w = page(it, 2, 7, {1: "0", 2: "10", 3: "0", 4: "8"})
        ok &= "= 5/8 in" in w and "= 8 mm" in w
        b, _ = page(it, 2, 8, {1: "800", 2: "1000", 3: "4", 4: "1.5"})   # a gauge
        ok &= b[4] == "50" and b[5] == "875"
        b, _ = page(it, 2, 8, {1: "300", 2: "400", 3: "20", 4: "17"})    # the voltmeter: 385
        return ok and b[5] == "385"

    def t_percent(it):
        b, w = page(it, 3, 1, {2: "30", 3: "400"})            # the class notes
        ok = b[0] == "120" and "x/400 = 30/100" in w
        b, w = page(it, 3, 1, {1: "30", 3: "400"})
        ok &= b[1] == "7.5" and "30/400 = x/100" in w
        b, w = page(it, 3, 1, {1: "400", 2: "30"})
        ok &= close(float(b[2]), 400 / 0.3) and "400/x = 30/100" in w
        b, _ = page(it, 3, 1, {2: "25", 3: "180"})            # the handout
        ok &= b[0] == "45"
        b, _ = page(it, 3, 1, {1: "150", 2: "25"})
        ok &= b[2] == "600"
        b, _ = page(it, 3, 1, {1: "50", 3: "800"})
        ok &= b[1] == "6.25"
        b, _ = page(it, 3, 2, {1: "80", 4: "100"})            # percent change
        ok &= b[1] == "25" and b[2] == "20"
        b, _ = page(it, 3, 2, {2: "-20", 4: "60"})
        return ok and b[0] == "75"

    def t_geometry(it):
        def g(p, texts):
            page(it, 5, p, texts)
            return lambda nm: var(it, nm)
        v = g(1, {1: "40", 2: "20"})
        ok = v("A") == 800 and v("P") == 120
        v = g(2, {1: "20"})
        ok &= v("A") == 400 and v("P") == 80
        v = g(3, {1: "50", 2: "18", 3: "20"})
        ok &= v("A") == 900 and v("P") == 140
        v = g(4, {1: "10", 2: "30", 3: "18", 4: "22", 5: "22"})
        ok &= v("A") == 360 and v("P") == 84
        v = g(5, {1: "50", 2: "18", 3: "25", 4: "40"})
        ok &= v("A") == 450 and v("P") == 115
        v = g(7, {1: "30"})
        ok &= close(v("A"), 0.433 * 900) and v("P") == 90
        v = g(8, {1: "15", 2: "20"})
        ok &= v("c") == 25 and v("A") == 150 and v("P") == 60
        v = g(9, {1: "15"})
        ok &= v("P") == 90 and v("A") == 585 and v("d") == 30 and close(v("f"), 25.98)
        v = g(10, {2: "30"})
        ok &= close(v("C"), 94.2) and close(v("A"), 706.5)
        v = g(10, {4: "314"})
        ok &= close(v("r"), 10) and close(v("C"), 62.8)
        v = g(1, {1: "12", 3: "64"})
        ok &= close(v("W"), 64 / 12)
        # composite: a house (rectangle 20 x 12 + triangle 20 x 8), then a hexagon minus a square
        page(it, 5, 11, {1: "20", 2: "12", 4: "20", 5: "8"}, opt={3: 1, 4: 3, 5: 0, 6: 0, 7: 0})
        ok &= var(it, "T") == 320
        page(it, 5, 11, {1: "20", 4: "20"}, opt={3: 7, 4: 2, 5: 0, 6: 0, 7: 1})
        return ok and var(it, "T") == 640

    tests = [("Ch. 7 exam: every problem, with the substitutions shown", t_exam7),
             ("all 34 class formulas give the class answers", t_formulas),
             ("rounding the way each question asks (hundred, inch)", t_rounding_asked),
             ("solving for a letter: both sides, bottoms, roots, twice", t_solve),
             ("any formula typed in", t_anyformula),
             ("order of operations, a pass at a time", t_order),
             ("place value (worksheet and Ch. 5 exam)", t_place),
             ("rounding to every place, exact on the digits", t_round),
             ("fraction, decimal, percent", t_fdp),
             ("tolerance and missing length", t_tol),
             ("conversions: the practice key, the Ch. 5 exam, metric stairs", t_convert),
             ("ruler and gauge readings", t_ruler),
             ("percent proportion and percent change", t_percent),
             ("geometry handout formulas, homework answers, composite", t_geometry)]

    ev = [shot("tm_cover.png"), check("the cover", lambda it: it.g["gTab"] == 0)]
    ev += [check(d, f) for d, f in tests]
    ev += [("check", home)]
    # every page opens, draws and has a contents line
    for t in range(1, 7):
        ev += [*tap(*tabxy(t)), shot(f"tm_tab{t}.png"),
               check(f"tab {t}: its contents page", lambda it, t=t: it.g["gTab"] == t and it.g["gPg"] == 0)]
        ev += [RIGHT]
        n = {1: 5, 2: 8, 3: 2, 4: 36, 5: 11, 6: 8}[t]
        for p in range(1, n + 1):
            ev += [VIEW, shot(f"tm_{t}_{p}.png") if (t != 4 or p <= 9) else ("check", lambda it: None),
                   check(f"tab {t} page {p} draws", lambda it, t=t, p=p: it.g["gTab"] == t and it.g["gPg"] == p),
                   RIGHT]
        ev += [check(f"tab {t}: turning past the last page comes back to the contents",
                     lambda it, t=t: it.g["gPg"] == 0)]
    # filling a page in by hand: the rectangle
    ev += [*tap(*tabxy(5)), 42,
           check("contents: pressing 1 opens page 1", lambda it: it.g["gPg"] == 1),
           SHIFT, DEL, *keys("40"), ENTER, *keys("20"), ENTER,
           check("typed L 40, W 20: A = 800 and P = 120 written in",
                 lambda it: it.g["gBv"][2] == "800" and it.g["gBv"][3] == "120"),
           shot("tm_rectangle.png"),
           MENU, MENU,
           check("Menu key: round to the tenth", lambda it: it.g["gOpt"][0] == 2),
           *tap(120, 232), check("erase (foot of the page)", lambda it: it.g["gBt"][0] == ""),
           *tap(60, 232), check("example (foot of the page)", lambda it: it.g["gBt"][0] == "40"),
           *tap(118, 70), DEL, UP, UP, DEL, *keys("7"), DIV, *keys("8"),
           check("typing shows on the blank", lambda it: it.g["gTy"] == 1 and it.g["gTx"] == "7/8"),
           ESC, check("Esc while typing: nothing kept", lambda it: it.g["gTy"] == 0 and it.g["gBt"][0] == ""),
           ESC, check("Esc: back to the contents", lambda it: it.g["gPg"] == 0),
           SHIFT, LEFT, check("Shift Left: the tab before", lambda it: it.g["gTab"] == 4),
           # order of operations typed on the keys
           ENTER, SHIFT, DEL, *keys("5"), MINUS, *keys("3"), PAREN, *keys("4"), SQ, DIV, *keys("2"), PAREN, PLUS,
           *keys("30"), ENTER,
           check("order of operations typed on the keys: 11",
                 lambda it: it.g["gBt"][0] == "5 - 3(4² ÷ 2) + 30" and it.g["gWk"][-1] == "Answer = 11"),
           shot("tm_order.png"),
           # any formula, with letters from the Alpha key
           RIGHT, SHIFT, DEL, ALPHA, 33, ENTER, *keys("0.02"), ALPHA, 35, PLUS, *keys("5"), ENTER, *keys("5.24"), ENTER,
           check("any formula typed with ALPHA: R = 0.02T + 5, R 5.24 gives T 12",
                 lambda it: it.g["gBt"][:3] == ["R", "0.02T + 5", "5.24"] and it.g["gBv"][3] == "12"),
           shot("tm_anyformula.png"),
           *tap(280, 34), check("tapping abc shows the letters", lambda it: it.g["gAbc"] == 1),
           shot("tm_letters.png"), ESC,
           KEY["help"], check("Help: how to use the notebook", lambda it: it.g["gTab"] == 6 and it.g["gPg"] == 1),
           DOWN, DOWN, check("Down scrolls a page of notes", lambda it: it.g["gSy"] > 0),
           [0, 150, 100], [1, 40, 104], [2], [3, 40, 104],
           check("a swipe to the left turns the page", lambda it: it.g["gPg"] == 2),
           ESC, ESC, check("Esc, Esc: the cover", lambda it: it.g["gTab"] == 0),
           -1, ESC]

    it = Interp(src, ev)
    try:
        it.start(prog)
        finished = True
    except StopSim:
        finished = False
    bad = [d for d, ok in checks if not ok]
    for d, ok in checks:
        print(("ok    " if ok else "FAIL  ") + d)
    print(f"{len(checks) - len(bad)}/{len(checks)} checks passed; program "
          + ("ended through the cover" if finished else "did NOT end"))
    if bad or not finished:
        sys.exit(1)


if __name__ == "__main__":
    main()
