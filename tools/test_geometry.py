#!/usr/bin/env python3
"""Simulator tests for hp-prime/GEOMETRY.txt (Chapter 8, Practical Plane
Geometry).

The expected answers are the textbook's worked examples and answers, and
the same figures worked again here with plain arithmetic, not from the
program.  The touch and keypad flow is played through, and screenshots go
to docs/screens/.

Usage
  python3 tools/test_geometry.py              # test hp-prime/GEOMETRY.txt
  python3 tools/test_geometry.py FILE OUTDIR  # test another copy
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 43 + 20


def box(k):
    return 110, 23 + (k - 1) * 19 + 9


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def nums(text):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]


def close(a, b, rel=0.0001):
    """six significant figures on screen: agree to 1 part in 10,000"""
    return abs(a - b) <= rel * max(abs(b), 1e-12)


def par(*r):
    return 1 / sum(1 / x for x in r)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "GEOMETRY.txt")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "screens")
    os.makedirs(out, exist_ok=True)
    src = open(path, encoding="utf-8").read()
    checks = []

    def fn_call(it, name, *args):
        params, body, _ = it.funcs[name]
        try:
            it.run_block(body, dict(zip(params, [float(a) for a in args])))
        except ReturnSignal as r:
            return r.value

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

    def reset(it):
        it.g["gV"] = list(it.g["gDef"])

    def calc(it, tool, **v):
        reset(it)
        for k, x in v.items():
            it.g["gV"][int(k[1:]) - 1] = float(x)
        fn_call(it, "toolCalc", tool)
        return rows(it)

    def val(r, label, n=0):
        return nums(r[label][0])[n]

    def text(r, label):
        return r[label][0]

    # ---- 8-1 angles ----------------------------------------------------
    def t_ang(it):
        r = calc(it, 1)                                # 109°43' + 25°32'
        ok = text(r, "A + B") == "135°15'"
        r = calc(it, 1, v4=5)                          # third angle of the triangle
        ok &= text(r, "180 - (A + B)") == "44°45'"
        r = calc(it, 1, v1=14, v2=32, v3=48, v4=3, v8=2)   # BAD = 2 x BAC
        ok &= text(r, "A x n") == "29°5'36''"
        r = calc(it, 1, v1=62, v2=12, v3=37, v4=8)
        ok &= close(val(r, "Decimal"), 62 + 12 / 60 + 37 / 3600)
        r = calc(it, 1, v1=90, v2=0, v4=8)
        return ok and text(r, "Type") == "right"

    def t_facts(it):
        r = calc(it, 2)                                # 125°: a, b, c
        ok = val(r, "Adjacent") == 55 and val(r, "Vertical") == 125
        ok &= val(r, "360° / n") == 60                 # six bolt holes
        r = calc(it, 2, v9=16, v10=8)                  # deck: 8 pieces in a half circle
        ok &= val(r, "Adjacent") == 164 and r["180° / n"][0] == "22°30'"
        r = calc(it, 2, v9=42)                         # board joined at a right angle
        return ok and val(r, "Complement") == 48

    def t_par(it):
        r = calc(it, 3)                                # 100° at angle 2
        ok = val(r, "1, 4, 5, 8") == 80 and val(r, "2, 3, 6, 7") == 100
        r = calc(it, 3, v11=60, v12=5)
        return ok and val(r, "1, 4, 5, 8") == 60 and val(r, "2, 3, 6, 7") == 120

    def t_tri(it):
        r = calc(it, 4)                                # 60° and 52°
        ok = val(r, "Decimal") == 68
        r = calc(it, 4, v14=46, v15=12, v16=73, v17=46)
        ok &= text(r, "Angle C") == "60°2'"
        r = calc(it, 4, v14=109, v15=43, v16=25, v17=32)
        ok &= text(r, "Angle C") == "44°45'" and text(r, "Triangle") == "obtuse"
        r = calc(it, 4, v14=90, v16=48)
        ok &= val(r, "Decimal") == 42 and text(r, "Triangle") == "right"
        r = calc(it, 4, v13=2, v14=40)                 # isosceles, apex 40°
        return ok and text(r, "Base angles") == "70°"

    # ---- 8-2 polygons and quadrilaterals -------------------------------
    def t_peri(it):
        r = calc(it, 5)                                # KLMN: 3 + 5 + 6 + 4
        ok = val(r, "Perimeter") == 18 and text(r, "Ft-in") == "1 ft 6 in"
        r = calc(it, 5, v18=5, v19=7.2, v20=16.5, v21=11.4, v22=14.3)
        ok &= close(val(r, "Perimeter"), 49.4)
        r = calc(it, 5, v19=8.25, v20=11.75, v21=8.125, v22=7.5, v23=7)
        ok &= close(val(r, "Perimeter"), 42.625) and text(r, "Ft-in") == "3 ft 6 5/8 in"
        r = calc(it, 5, v19=3, v20=0, v21=0, v22=0)
        return ok and "3 or more" in " ".join(it.g["gRV"])

    def t_rect(it):
        r = calc(it, 6)                                # 9 in x 5 in
        ok = val(r, "Area") == 45 and val(r, "Perimeter") == 28
        r = calc(it, 6, v27=5, v28=42, v29=18)
        ok &= val(r, "Area") == 756
        r = calc(it, 6, v28=12, v29=0, v30=64)         # vents: W = A / L
        ok &= close(val(r, "Width W"), 16 / 3)
        r = calc(it, 6, v27=2, v28=4.5, v29=3.25)
        ok &= close(val(r, "Area"), 14.625)
        r = calc(it, 6, v27=2, v28=64.5, v29=44.5)
        return ok and close(val(r, "Area"), 2870.25)

    def t_sq(it):
        r = calc(it, 7)                                # 9 ft
        ok = val(r, "Area") == 81 and val(r, "Perimeter") == 36
        r = calc(it, 7, v32=0, v33=64)
        ok &= val(r, "Side s") == 8
        r = calc(it, 7, v32=0, v33=927)
        ok &= close(val(r, "Side s"), math.sqrt(927))
        r = calc(it, 7, v31=3, v32=7 / 3)
        ok &= close(val(r, "Area"), 49 / 9)
        r = calc(it, 7, v32=24.5)                      # driveway
        return ok and close(val(r, "Area"), 600.25) and close(val(r, "In sq yd"), 600.25 / 9)

    def t_pgram(it):
        r = calc(it, 8)                                # b 7 in, h 10 in
        ok = val(r, "Area") == 70
        r = calc(it, 8, v34=5, v35=18, v36=20, v37=24)
        ok &= val(r, "Area") == 360 and val(r, "Perimeter") == 84
        r = calc(it, 8, v35=12, v36=8, v37=9)
        ok &= val(r, "Area") == 96 and val(r, "Perimeter") == 42
        r = calc(it, 8, v34=2, v35=2.75, v36=3.25)
        return ok and close(val(r, "Area"), 8.9375)

    def t_trap(it):
        r = calc(it, 9)                                # 7, 19, h 6; sides 8, 9
        ok = val(r, "Area") == 78 and val(r, "Perimeter") == 43
        r = calc(it, 9, v39=8, v40=26, v41=12, v42=15, v43=15)
        ok &= val(r, "Area") == 204 and val(r, "Perimeter") == 64
        r = calc(it, 9, v38=2, v39=11.75, v40=8.25, v41=10.5)
        return ok and val(r, "Area") == 105

    def t_cost(it):
        r = calc(it, 10)                               # 600.25 sq ft at $65 per sq yd
        ok = close(val(r, "In sq yd"), 600.25 / 9) and text(r, "Cost") == "$4335.14"
        r = calc(it, 10, v44=206, v45=8, v46=16, v47=7)   # fence: 206 yd at $16 per ft
        ok &= val(r, "In ft") == 618 and text(r, "Cost") == "$9888.00"
        r = calc(it, 10, v44=400, v45=7, v46=0, v47=7, v50=8)
        ok &= val(r, "Posts, loop") == 50
        r = calc(it, 10, v44=210, v45=2, v46=0.59, v47=2)
        ok &= text(r, "Cost") == "$123.90"
        r = calc(it, 10, v44=200, v45=2, v46=0, v47=2, v48=30, v49=24)   # strip flooring
        ok &= val(r, "With waste") == 260 and val(r, "Packages") == 11
        r = calc(it, 10, v45=2, v47=7)
        return ok and "mix" in r["Units"][0]

    # ---- 8-3 triangles, hexagons, irregular figures --------------------
    def t_pyth(it):
        r = calc(it, 11)                               # 36 ft by 20 ft plot
        ok = close(val(r, "Hyp. c"), math.hypot(36, 20))
        r = calc(it, 11, v51=1, v52=8, v53=15)
        ok &= val(r, "Hyp. c") == 17
        r = calc(it, 11, v52=0, v53=13.8, v54=22.3)
        ok &= close(val(r, "Leg a"), math.sqrt(22.3 ** 2 - 13.8 ** 2))
        r = calc(it, 11, v52=0, v53=10, v54=12)        # ladder
        ok &= close(val(r, "Leg a"), math.sqrt(44)) and text(r, "Ft-in") == "6 ft 7 5/8 in"
        r = calc(it, 11, v52=8.5, v53=9.75, v54=0)     # stairway
        ok &= text(r, "Ft-in") == "12 ft 11 1/4 in"        # 11.219 in; the book rounds to 11 in
        r = calc(it, 11, v52=3, v53=4, v54=5)
        ok &= r["Right angle?"][0].startswith("yes")
        r = calc(it, 11, v52=0, v53=0, v54=5)
        return ok and "Enter" in r

    def t_tria(it):
        r = calc(it, 12)                               # b 13, h 8
        ok = val(r, "Area") == 52
        r = calc(it, 12, v56=25, v57=16)
        ok &= val(r, "Area") == 200
        r = calc(it, 12, v55=2, v56=6.5, v57=8)
        ok &= val(r, "Area") == 26
        r = calc(it, 12, v56=20, v57=0, v58=120)
        return ok and val(r, "Height h") == 12

    def t_tri3(it):
        r = calc(it, 13)                               # attic wall 7, 7, 12
        ok = close(val(r, "Area"), 6 * math.sqrt(13)) and text(r, "Sides") == "isosceles"
        r = calc(it, 13, v59=1, v60=9, v61=9, v62=6)
        ok &= close(val(r, "Area"), 3 * math.sqrt(72)) and close(val(r, "Height to c"), math.sqrt(72))
        r = calc(it, 13, v60=3, v61=4, v62=5)
        ok &= val(r, "Area") == 6 and text(r, "Angles") == "right" and text(r, "Sides") == "scalene"
        r = calc(it, 13, v60=8, v61=8, v62=8)
        ok &= text(r, "Sides") == "equilateral" and text(r, "A, B, C") == "60.0, 60.0, 60.0°"
        r = calc(it, 13, v60=1, v61=2, v62=5)
        return ok and "Not a triangle" in r

    def t_hex(it):
        r = calc(it, 14)                               # side 0.40 in
        ok = close(val(r, "Area"), 1.5 * math.sqrt(3) * 0.16) and close(val(r, "Perimeter"), 2.4)
        r = calc(it, 14, v64=2, v65=math.sqrt(3))
        ok &= close(val(r, "Side s"), 1)
        r = calc(it, 14, v64=3, v65=10)
        return ok and val(r, "Side s") == 5

    def t_irr(it):
        r = calc(it, 15)                               # L-shaped room, $4.75 per sq ft
        ok = val(r, "Total area") == 492 and text(r, "Cost") == "$2337.00"
        r = calc(it, 15, v72=2, v73=3, v74=4)          # cut out a 3 x 4 piece
        return ok and val(r, "Total area") == 480

    # ---- 8-4 circles ----------------------------------------------------
    def t_circ(it):
        r = calc(it, 16)                               # r 2.70 in, π = 3.14
        ok = close(val(r, "Area"), 3.14 * 2.7 ** 2) and close(val(r, "Circumf."), 3.14 * 5.4)
        r = calc(it, 16, v76=2, v77=10, v79=1)
        ok &= close(val(r, "Area"), math.pi * 25)
        r = calc(it, 16, v76=3, v77=10 * math.pi, v79=1)
        ok &= close(val(r, "Radius r"), 5)
        r = calc(it, 16, v76=4, v77=25 * math.pi, v79=1)
        return ok and close(val(r, "Radius r"), 5)

    def t_ring(it):
        r = calc(it, 17)                               # flowerbed 8.5 ft, lawn 12 ft wide
        ar = math.pi * (20.5 ** 2 - 8.5 ** 2)
        ok = close(val(r, "Ring area"), ar) and text(r, "Cost") == "$" + f"{ar * 9.5:.2f}"
        r = calc(it, 17, v83=2)
        return ok and close(val(r, "Ring area"), 3.14 * 348)

    def t_sect(it):
        r = calc(it, 18)                               # r 10, 90°
        ok = close(val(r, "Arc length"), 5 * math.pi) and close(val(r, "Sector area"), 25 * math.pi)
        ok &= close(val(r, "Chord"), 10 * math.sqrt(2))
        r = calc(it, 18, v87=180)
        return ok and close(val(r, "Arc length"), 10 * math.pi)

    def t_ftin(it):
        r = calc(it, 19)                               # 4 ft 6 in
        ok = val(r, "Decimal ft") == 4.5 and val(r, "Inches") == 54
        r = calc(it, 19, v89=11, v90=9)
        ok &= val(r, "Decimal ft") == 11.75
        r = calc(it, 19, v89=0, v90=14)
        return ok and text(r, "Ft-in") == "1 ft 2 in" and close(val(r, "Area sq yd"), 600.25 / 9)

    tool_checks = [t_ang, t_facts, t_par, t_tri, t_peri, t_rect, t_sq, t_pgram, t_trap, t_cost,
                   t_pyth, t_tria, t_tri3, t_hex, t_irr, t_circ, t_ring, t_sect, t_ftin]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))
    assert len(names) == len(tool_checks)

    ev = [shot("geom_home.png")]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: book answers", fn),
               ("check", reset), KEY["right"], -1,
               shot(f"geom_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        *tap(*tile(20)), ("dialog", 9),
        shot("geom_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 20),
        # rectangle: tap the width box, enter 0 and the area 64: W = 64 / L
        *tap(*tile(6)),
        *tap(*box(3)), ("dialog", 0),
        *tap(*box(4)), ("dialog", 64),
        check("rectangle: width found from the area", lambda it: it.g["gRV"][0].startswith("7.11111")),
        KEY["left"], KEY["left"], *keys("12"), KEY["enter"],
        check("keypad types L = 12", lambda it: it.g["gV"][27] == 12 and it.g["gRV"][0].startswith("5.33333")),
        shot("geom_rect_find.png"),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][28] == 5 and it.g["gV"][29] == 0),
        *tap(300, 10),
        shot("geom_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 7),
        KEY["esc"],
        KEY["down"], KEY["down"], KEY["down"], KEY["right"],
        check("arrows on the 4 x 5 tiles", lambda it: it.g["gHome"] == 20),
        KEY["help"],
        shot("geom_help.png"),
        KEY["enter"],
        -1,
        *tap(295, 10),
    ]
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
          + ("ended through EXIT" if finished else "did NOT end")
          + f"; angle setting put back: {it.sysvars['HAngle'] == 0}")
    if bad or not finished or it.sysvars["HAngle"] != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
