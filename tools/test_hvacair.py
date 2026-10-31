#!/usr/bin/env python3
"""Simulator tests for hp-prime/HVACAIR.txt.

Moist-air answers are compared with CoolProp's humid-air model (ASHRAE
RP-1485), duct friction with a separate Colebrook solution and the Wright
duct-friction equation, and the other tools with their formulas worked out
here.  The touch and keypad flow is played through, and screenshots of the
home screen and every tool go to docs/screens/.

Usage
  python3 tools/test_hvacair.py              # test hp-prime/HVACAIR.txt
  python3 tools/test_hvacair.py FILE OUTDIR  # test another copy
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, approx, num, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}
MENU = 13
PSI = 6894.757
BTU_LB = 1 / 2326.0          # J/kg -> BTU/lb
FT3_LB = 16.018463           # m3/kg -> ft3/lb


def rnd(x, n=0):
    """round half up, as the calculator's ROUND does"""
    m = 10 ** n
    return math.copysign(math.floor(abs(x) * m + 0.5) / m, x)


def f2k(f):
    return (f - 32) / 1.8 + 273.15


def k2f(k):
    return (k - 273.15) * 1.8 + 32


def patm(z):
    return 14.696 * (1 - 6.8754e-6 * z) ** 5.2559


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 43 + 20


def box(k):
    return ((k - 1) % 2) * 160 + 115, 24 + ((k - 1) // 2) * 20 + 8


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def colebrook(q, d_in, eps):
    """in.wc per 100 ft, solved here by bisection on 1/sqrt(f)"""
    d = d_in / 12
    v = q / (math.pi * d * d / 4)
    re_ = 8.56 * d_in * v
    lo, hi = 1.0, 20.0                     # bounds for x = 1/sqrt(f)
    for _ in range(80):
        x = (lo + hi) / 2
        if x + 2 * math.log10(eps / (3.7 * d) + 2.51 * x / re_) > 0:
            hi = x
        else:
            lo = x
    f = 1 / ((lo + hi) / 2) ** 2
    return 100 * f / d * (v / 4005) ** 2


def wright(q, d_in):
    """empirical friction for galvanized duct, in.wc per 100 ft"""
    return 0.109136 * q ** 1.9 / d_in ** 5.02


def main():
    import CoolProp.CoolProp as CP
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "HVACAIR.txt")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "screens")
    os.makedirs(out, exist_ok=True)
    src = open(path, encoding="utf-8").read()
    checks = []

    def ha(prop, t_f, p_psia, key, val):
        return CP.HAPropsSI(prop, "T", f2k(t_f), "P", p_psia * PSI, key, val)

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
            except Exception as exc:          # a failed check, not a crash
                checks.append((f"{desc} ({type(exc).__name__}: {exc})", False))
                return
            checks.append((desc, ok))
        return ("check", run)

    def shot(name):
        return ("shot", os.path.join(out, name))

    def setv(it, **v):
        for k, x in v.items():
            it.g["gV"][int(k[1:]) - 1] = float(x)

    def reset(it):
        it.g["gV"] = list(it.g["gDef"])

    def calc(it, tool, **v):
        reset(it)
        setv(it, **v)
        fn_call(it, "toolCalc", tool)
        return rows(it)

    def val(r, label):
        return num(r[label][0])

    # ---- moist air against CoolProp ----
    def t_props(it):
        ok = True
        cases = [  # (dry bulb, kind, value, elevation)
            (75, 1, 50, 0), (95, 1, 40, 0), (55, 1, 90, 0), (100, 2, 70, 0),
            (80, 3, 60, 0), (30, 1, 70, 0), (75, 1, 50, 5000), (110, 2, 75, 3000)]
        for db, kind, x, z in cases:
            p = patm(z)
            key, v = {1: ("R", x / 100), 2: ("B", f2k(x)), 3: ("D", f2k(x))}[kind]
            r = calc(it, 1, v1=z, v2=db, v3=kind, v4=x)
            w = ha("W", db, p, key, v)
            ok &= approx(val(r, "Moisture"), w * 7000, max(0.15, 0.006 * w * 7000))
            if kind != 1:
                ok &= approx(val(r, "Rel. humidity"), 100 * ha("R", db, p, key, v), 0.4)
            if kind != 2:
                ok &= approx(val(r, "Wet bulb"), k2f(ha("B", db, p, key, v)), 0.25)
            if kind != 3:
                ok &= approx(val(r, "Dew point"), k2f(ha("D", db, p, key, v)), 0.25)
            ok &= approx(val(r, "Volume"), ha("V", db, p, key, v) * FT3_LB, 0.02)
            ok &= approx(val(r, "Air pressure"), p, 0.0015)
        r = calc(it, 1, v3=2, v4=80)
        return ok and r["Check"][0] == "wet bulb above dry bulb"

    def t_dew(it):
        r = calc(it, 2)
        dp = k2f(ha("D", 75, 14.696, "R", 0.55))
        ok = approx(val(r, "Dew point"), dp, 0.2) and r["Surface"][0] == "close: may sweat"
        r = calc(it, 2, v7=50)
        ok &= r["Surface"][0] == "WILL SWEAT"
        r = calc(it, 2, v7=65)
        # humidity at which a 65 F surface sweats in 75 F air
        rh = 100 * CP.HAPropsSI("R", "T", f2k(75), "P", 101325, "D", f2k(65))
        return ok and r["Surface"][0] == "no sweating" and approx(val(r, "Sweats above"), rh, 0.4)

    def t_coil(it):
        r = calc(it, 3)
        hr = ha("H", 75, 14.696, "B", f2k(63)) * BTU_LB
        hs = ha("H", 55, 14.696, "B", f2k(53)) * BTU_LB
        wr = ha("W", 75, 14.696, "B", f2k(63))
        ws = ha("W", 55, 14.696, "B", f2k(53))
        tot = 4.5 * 1200 * (hr - hs)
        ok = approx(val(r, "Total"), tot, 0.012 * tot) and val(r, "Sensible") == rnd(1.08 * 1200 * 20)
        ok &= approx(val(r, "Condensate"), 4.5 * 1200 * (wr - ws) / 8.34, 0.02)
        ok &= val(r, "CFM per ton") == 400
        r = calc(it, 3, v1=5000)
        return ok and val(r, "Sensible") == rnd(1.08 * patm(5000) / 14.696 * 1200 * 20)

    def t_mix(it):
        r = calc(it, 4)
        ok = val(r, "Mixed air") == rnd(0.2 * 90 + 0.8 * 75, 1) and val(r, "Outside CFM") == 800
        r = calc(it, 4, v14=2, v19=80)
        ok &= approx(val(r, "Outside air"), 100 * (80 - 75) / (90 - 75), 0.05)
        r = calc(it, 4, v14=2, v19=95)
        ok &= r["Check"][0] == "mixed not between"
        r = calc(it, 4, v15=60, v16=50)
        return ok and r["Economizer"][0] == "outside air helps"

    def t_furn(it):
        r = calc(it, 5)
        ok = val(r, "Airflow") == rnd(64000 / (1.08 * 52)) and r["Temp rise"][1].startswith("in range")
        r = calc(it, 5, v24=140)
        ok &= r["Temp rise"][1].startswith("HIGH")
        r = calc(it, 5, v1=5000)
        return ok and val(r, "Airflow") == rnd(64000 / (1.08 * patm(5000) / 14.696 * 52))

    def t_heatf(it):
        r = calc(it, 6)
        ok = val(r, "Airflow") == rnd(24000 / (1.08 * 20))
        r = calc(it, 6, v27=1, v29=1000, v30=18)
        ok &= val(r, "Sensible") == rnd(1.08 * 1000 * 18)
        r = calc(it, 6, v27=3, v28=30000, v29=1250)
        ok &= val(r, "Temp diff") == rnd(30000 / (1.08 * 1250), 1)
        r = calc(it, 6, v31=30)
        return ok and val(r, "Latent") == rnd(0.68 * (24000 / 21.6) * 30)

    def t_static(it):
        r = calc(it, 7)
        ok = val(r, "Total ESP") == 0.6 and val(r, "Of rated") == 120
        r = calc(it, 7, v35=0.15, v36=0.2)
        return ok and val(r, "Ducts + rest") == 0.25 and val(r, "Filter") == 0.15

    def t_vent(it):
        r = calc(it, 8)
        ok = val(r, "62.2 needs") == 0.03 * 2000 + 7.5 * 4 and val(r, "Run time") == rnd(60 * 90 / 100)
        r = calc(it, 8, v40=50)
        return ok and r["Run time"][0] == "all the time"

    def t_dsize(it):
        r = calc(it, 9)
        d = val(r, "Round")
        ok = approx(colebrook(1000, d, 0.0003), 0.08, 0.0006)
        # a ductulator check: 1000 CFM at 0.10 in.wc is about a 14 in round
        r = calc(it, 9, v42=0.1)
        ok &= 13.4 <= val(r, "Round") <= 14.2
        r = calc(it, 9)
        w = num(r["Rectangular"][0])
        de = 1.30 * (w * 8) ** 0.625 / (w + 8) ** 0.25
        ok &= de >= d - 0.01 and 1.30 * ((w - 1) * 8) ** 0.625 / (w - 1 + 8) ** 0.25 < d
        r = calc(it, 9, v43=3)
        return ok and r["Flex"][0] == "pull it tight" and val(r, "Round") > d

    def t_dcheck(it):
        ok = True
        for q, d in ((400, 10), (1000, 14), (150, 6), (2000, 18)):
            r = calc(it, 10, v46=d, v48=q)
            f = val(r, "Friction")
            ok &= approx(f, colebrook(q, d, 0.0003), 0.0015)
            # Wright's older equation assumes rougher duct: 6-9% higher
            ok &= abs(f / wright(q, d) - 1) < 0.10
            ok &= val(r, "Velocity") == rnd(q / (math.pi * d * d / 576))
        r = calc(it, 10, v45=2, v46=20, v47=8, v48=1000, v50=850)
        de = 1.30 * 160 ** 0.625 / 28 ** 0.25
        ok &= val(r, "Area") == rnd(160 / 144, 3) and approx(val(r, "Friction"), colebrook(1000, de, 0.0003), 0.0015)
        return ok and val(r, "Measured") == rnd(850 * 160 / 144)

    def t_fr(it):
        r = calc(it, 11)
        ok = val(r, "Friction rate") == rnd((0.5 - 0.36) * 100 / 200, 3) and r["Friction rate"][1].startswith("in the")
        r = calc(it, 11, v57=400)
        ok &= r["Friction rate"][1].startswith("low")
        r = calc(it, 11, v51=0.3)
        return ok and r["Friction rate"][0] == "none left"

    def t_grille(it):
        r = calc(it, 12)
        ok = val(r, "Each grille") == rnd(10 * 6 / 144 * 0.7 * 400)
        r = calc(it, 12, v58=0.25, v63=4)
        return ok and val(r, "Each grille") == 100 and val(r, "All 4") == 400

    def t_fanlaw(it):
        r = calc(it, 13)
        q = 1000 / 900
        ok = (val(r, "Airflow") == rnd(1600 * q) and val(r, "Static") == rnd(0.6 * q * q, 2)
              and val(r, "Power") == rnd(0.75 * q ** 3, 2) and r["Motor"][1] == "OVERLOADED")
        r = calc(it, 13, v64=2, v69=1400)
        q = 1400 / 1600
        return ok and val(r, "Fan speed") == rnd(900 * q) and r["Motor"][1] == "OK"

    def t_pulley(it):
        r = calc(it, 14, v75=950)
        ln = 2 * 18 + math.pi / 2 * 10.5 + 3.5 ** 2 / 72
        return (val(r, "Blower RPM") == rnd(1725 * 3.5 / 7) and val(r, "Belt length") == rnd(ln, 1)
                and r["For 950 RPM"][0] == f"motor {7 * 950 / 1725:.2f} in")

    def t_fanpow(it):
        r = calc(it, 15)
        bhp = 1200 * 0.8 / 6356 / 0.5
        return (val(r, "Shaft power") == rnd(bhp, 3) and val(r, "Motor input") == rnd(bhp * 745.7 / 0.8)
                and r["Motor size"][0] == "1/3 HP")

    def t_conv(it):
        r = calc(it, 16)
        ok = approx(val(r, "L/s"), 1200 * 0.47194745, 0.002)
        r = calc(it, 16, v80=2, v81=1, v82=1)
        ok &= approx(val(r, "Pa"), 249.0889, 0.01)
        r = calc(it, 16, v80=3, v81=2, v82=5)
        ok &= approx(val(r, "fpm"), 5 * 196.850394, 0.001)
        r = calc(it, 16, v80=6, v81=1, v82=70)
        return ok and val(r, "g/kg") == 10

    def t_loss(it):
        r = calc(it, 17)
        ua = 1200 / 13 + 1500 / 38 + 200 / 2
        ok = val(r, "Heat gain") == rnd(ua * 20)
        r = calc(it, 17, v84=10)
        return ok and val(r, "Heat loss") == rnd(ua * 65)

    def t_load(it):
        r = calc(it, 18)
        ua = 1200 / 13 + 1500 / 38 + 200 / 2
        dw = 7000 * (ha("W", 95, 14.696, "R", 0.45) - ha("W", 75, 14.696, "R", 0.50))
        sen = ua * 20 + 230 * 4 + 500 * 3.41214 + 6000 + 1.08 * 100 * 20
        lat = 200 * 4 + 0.68 * 100 * dw
        return approx(val(r, "Total"), sen + lat, 0.004 * (sen + lat)) and approx(val(r, "Size"), (sen + lat) / 12000, 0.011)

    def t_humid(it):
        r = calc(it, 19)
        wi = ha("W", 70, 14.696, "R", 0.35)
        wo = ha("W", 20, 14.696, "R", 0.60)
        cfm = 16000 * 0.5 / 60
        gal = 4.5 * cfm * (wi - wo) * 24 / 8.34
        ok = approx(val(r, "Per day"), gal, 0.02 * gal + 0.05)
        ok &= approx(val(r, "Indoor dew pt"), k2f(ha("D", 70, 14.696, "R", 0.35)), 0.25)
        r = calc(it, 19, v101=100, v100=60)
        return ok and r["Humidifier"][0] == "not needed"

    def t_evap(it):
        r = calc(it, 20)
        la = 100 - 0.8 * 35
        rh = 100 * CP.HAPropsSI("R", "T", f2k(la), "P", 101325, "B", f2k(65))
        return val(r, "Leaving air") == la and approx(val(r, "Leaving RH"), rh, 1.0)

    tool_checks = [t_props, t_dew, t_coil, t_mix, t_furn, t_heatf, t_static, t_vent,
                   t_dsize, t_dcheck, t_fr, t_grille, t_fanlaw, t_pulley, t_fanpow, t_conv,
                   t_loss, t_load, t_humid, t_evap]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))

    ev = [shot("air_home.png")]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset),
               -1,                            # redraw with the example values
               shot(f"air_{k:02d}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        check("HOME returns to the tiles", lambda it: it.g["gScr"] == 1),
        # air properties: the second reading's name follows the choice
        *tap(*tile(1)),
        check("value box is RH", lambda it: fn_call(it, "slotName", 4) == "RH"),
        *tap(*box(2)), ("dialog", 2),
        check("choose wet bulb", lambda it: it.g["gV"][2] == 2 and fn_call(it, "slotName", 4) == "Wet bulb"),
        KEY["right"], *keys("62"), KEY["enter"],
        check("type the wet bulb", lambda it: it.g["gV"][3] == 62),
        shot("air_typing.png"),
        KEY["right"], *keys("5280"), KEY["enter"],
        check("elevation typed", lambda it: it.g["gV"][0] == 5280),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][0] == 0 and it.g["gV"][2] == 1),
        # the box being solved for shows ?
        *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)),
        check("on heat formulas", lambda it: it.g["gTool"] == 6),
        check("CFM box shows ?", lambda it: fn_call(it, "slotText", 29) == "?"),
        *tap(*box(1)), ("dialog", 1),
        check("find BTU/h", lambda it: it.g["gV"][26] == 1 and fn_call(it, "slotText", 28) == "?"),
        *tap(*menu(2)),
        # duct check: height is not used for a round duct
        *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)),
        check("on duct check", lambda it: it.g["gTool"] == 10),
        check("round: height shows --", lambda it: fn_call(it, "slotText", 47) == "--"),
        *tap(*box(1)),
        check("tap flips to rectangular", lambda it: it.g["gV"][44] == 2 and fn_call(it, "slotName", 46) == "Width"),
        *tap(*menu(2)),
        # a tap left over from a dialog is ignored
        *tap(*box(3)), ("dialog", 12),
        check("dialog sets the diameter", lambda it: it.g["gV"][45] == 12),
        [2], [3, 290, 230],
        check("left-over tap ignored", lambda it: it.g["gScr"] == 2 and it.g["gTool"] == 10),
        *tap(*menu(2)),
        # help pages
        *tap(300, 10),
        shot("air_help_tool.png"),
        *tap(160, 120),
        check("tool help closes", lambda it: it.g["gScr"] == 2),
        KEY["esc"],
        KEY["help"],
        shot("air_help.png"),
        KEY["enter"],
        MENU, ("dialog", 18),
        check("Menu key opens a tool", lambda it: it.g["gTool"] == 18 and it.g["gScr"] == 2),
        KEY["esc"],
        check("Esc goes home", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 18),
        -1,
        *tap(295, 10),                      # EXIT
    ]
    it = Interp(src, ev)
    try:
        it.start("HVACAIR")
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
