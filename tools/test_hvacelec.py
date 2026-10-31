#!/usr/bin/env python3
"""Simulator tests for hp-prime/HVACELEC.txt.

Every tool's answers are compared with an independent calculation, or with
values copied from the published tables (NEC 430.248 / 430.250 / 310.16,
BAPI's 10K-3 thermistor table), and the touch and keypad flow is played
through.  Screenshots of the home screen and every tool go to docs/screens/.

Usage
  python3 tools/test_hvacelec.py              # test hp-prime/HVACELEC.txt
  python3 tools/test_hvacelec.py FILE OUTDIR  # test another copy
"""
import csv
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, approx, num, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}
DEL, MENU = 19, 13
SQ3 = math.sqrt(3)

# spot values typed from the published tables (not from the generator)
NEC_FLC = [  # (HP index in the chooser, phase, volts index, amps)
    (10, 2, 3, 16.7),   # 430.250: 5 HP, 208 V
    (12, 2, 5, 14),     # 430.250: 10 HP, 460 V
    (6, 2, 2, 4.8),     # 430.250: 1 HP, 200 V
    (24, 2, 6, 192),    # 430.250: 200 HP, 575 V
    (8, 1, 4, 12),      # 430.248: 2 HP, 230 V
    (4, 1, 1, 9.8),     # 430.248: 1/2 HP, 115 V
    (12, 1, 3, 55),     # 430.248: 10 HP, 208 V
]
NEC_AMPACITY = [  # (wire index, material, column, amps) from Table 310.16
    (7, 1, 2, 65),      # 6 AWG Cu 75 C
    (15, 2, 2, 180),    # 4/0 Al 75 C
    (20, 1, 3, 430),    # 500 kcmil Cu 90 C
    (6, 2, 1, 35),      # 8 AWG Al 60 C
    (3, 1, 1, 15),      # 14 AWG Cu 60 C
]


def rnd(x, n=0):
    """round half up, as the calculator's ROUND does"""
    m = 10 ** n
    return math.copysign(math.floor(abs(x) * m + 0.5) / m, x)


def tile(k):
    """centre of home-screen tile k"""
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 43 + 20


def box(k):
    """centre of input box k on a tool screen"""
    return ((k - 1) % 2) * 160 + 115, 24 + ((k - 1) // 2) * 20 + 8


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "HVACELEC.txt")
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
            except Exception as exc:          # a failed check, not a crash
                ok = False
                desc_ = f"{desc} ({type(exc).__name__}: {exc})"
                checks.append((desc_, ok))
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

    # ---- tool checks: each compares the program with its own sum ----
    def t_ohm(it):
        r = calc(it, 1)
        ok = val(r, "Amps (I)") == 10 and val(r, "Watts (P)") == 1200
        r = calc(it, 1, v1=0, v2=2.5, v3=8, v4=0)
        ok &= val(r, "Volts (E)") == 20 and val(r, "Watts (P)") == 50
        r = calc(it, 1, v1=0, v2=0, v3=10, v4=1000)
        ok &= val(r, "Volts (E)") == 100 and val(r, "Amps (I)") == 10
        r = calc(it, 1, v1=0, v2=0, v3=10, v4=0)
        return ok and r["Enter"][0] == "any two values"

    def t_power(it):
        r = calc(it, 2)
        ok = (val(r, "Real power") == 2070 and val(r, "Apparent") == 2300
              and approx(val(r, "Reactive"), 2300 * math.sqrt(1 - 0.81), 0.6)
              and approx(val(r, "Heat"), 2070 * 3.41214, 0.6)
              and approx(val(r, "Motor output"), 2070 * 0.85 / 746, 0.006))
        r = calc(it, 2, v5=460, v6=20, v7=2, v8=0.85)
        return ok and r["Apparent"][0] == f"{460 * 20 * SQ3 / 1000:.1f} kVA" \
            and r["Real power"][0] == f"{460 * 20 * SQ3 * 0.85 / 1000:.1f} kW"

    def t_load(it):
        r = calc(it, 3)
        ok = approx(val(r, "Load amps"), 5000 / (230 * 0.9), 0.05)
        r = calc(it, 3, v10=3, v11=3, v5=208, v7=2, v8=0.85, v9=85)
        ok &= approx(val(r, "Load amps"), 3 * 746 / 0.85 / (208 * 0.85 * SQ3), 0.01)
        r = calc(it, 3, v10=34121.4, v11=4, v5=240, v7=1, v8=1)
        return ok and approx(val(r, "Load amps"), 10000 / 240, 0.05) and r["Copper 75°C"][0] == "6 AWG"

    def t_serpar(it):
        r = calc(it, 4)
        ok = (val(r, "Total") == 30 and val(r, "Current") == 0.8
              and val(r, "R1 10.0 Ω") == 8 and val(r, "R2 20.0 Ω") == 16)
        r = calc(it, 4, v13=2)
        ok &= approx(val(r, "Total"), 1 / (1 / 10 + 1 / 20), 0.01) and val(r, "R1 10.0 Ω") == 2.4
        r = calc(it, 4, v12=2, v13=2, v15=40, v16=5)
        ok &= val(r, "Total") == 45
        r = calc(it, 4, v12=2, v13=1, v15=10, v16=10, v14=370)
        return ok and val(r, "Total") == 5 and val(r, "C1 gets") == 185

    def t_ampchk(it):
        r = calc(it, 5)
        ok = (r["Allowed"][0] == "187.2 - 253 V" and r["Voltage"][0].endswith("OK")
              and val(r, "Load") == rnd(100 * 11.2 / 14.1))
        r = calc(it, 5, v20=180, v22=22.4, v23=2)
        return ok and r["Voltage"][0].endswith("LOW") and val(r, "Running amps") == 11.2

    def t_3ph(it):
        r = calc(it, 6)
        v = [230, 227, 223]
        a = [10.6, 10.1, 9.8]
        vu = 100 * max(abs(x - sum(v) / 3) for x in v) / (sum(v) / 3)
        au = 100 * max(abs(x - sum(a) / 3) for x in a) / (sum(a) / 3)
        return (approx(val(r, "V unbalance"), vu, 0.006) and approx(val(r, "A unbalance"), au, 0.06)
                and r["NEMA derate"][0] == f"{1 - 0.05 * (vu - 1):.2f} x HP"
                and r["Legs"][0] == "high L1, low L3")

    def t_cap(it):
        r = calc(it, 7)
        uf = 6.4 * 1e6 / (2 * math.pi * 60 * 375)
        ok = approx(val(r, "From A and V"), uf, 0.05) and r["Capacitor"][0] == "GOOD"
        ok &= r["Rated range"][0] == "42.3 - 47.7 µF"
        r = calc(it, 7, v32=40)
        return ok and r["Capacitor"][0] == "WEAK: replace"

    def t_wind(it):
        r = calc(it, 8)
        ok = (r["Common (C)"][0] == "terminal 2" and r["Run (R)"][0] == "terminal 1"
              and r["Start (S)"][0] == "terminal 3" and r["Windings"][0] == "look normal")
        # same motor, leads numbered differently
        r = calc(it, 8, v37=6.2, v38=2.1, v39=4.2)
        ok &= r["Common (C)"][0] == "terminal 3" and r["Run (R)"][0] == "terminal 2"
        r = calc(it, 8, v37=99999, v38=99999, v39=6.2)
        ok &= r["If it is S-R"][0] == "overload open"
        r = calc(it, 8, v36=2, v37=1.2, v38=1.2, v39=1.25)
        ok &= r["Windings"][0] == "Balanced"
        r = calc(it, 8, v40=120)
        f = (234.5 + 25) / (234.5 + (120 - 32) / 1.8)
        return ok and r["At 77°F"][0] == f"R {2.1 * f:.2f} Ω  S {4.2 * f:.2f} Ω"

    def t_meg(it):
        r = calc(it, 9)
        ok = val(r, "At 40°C") == rnd(850 * 0.5 ** ((40 - 20) / 10)) and r["IEEE 43 min"][0].startswith("PASS")
        r = calc(it, 9, v41=3, v42=104, v43=4, v44=2.5)
        return (ok and r["IEEE 43 min"][0].startswith("FAIL") and val(r, "PI 10/1 min") == 1.33
                and r["PI 10/1 min"][1] == "questionable" and val(r, "DAR 60/30 s") == 1.2)

    def t_motor(it):
        ok = True
        for h, ph, vi, amps in NEC_FLC:
            r = calc(it, 10, v45=h, v46=ph, v47=vi)
            ok &= val(r, "Table FLC") == amps
        r = calc(it, 10, v46=1, v47=5)
        ok &= r["Table FLC"][0] == "none"
        r = calc(it, 10)
        return (ok and r["Breaker max"][0] == "45 A" and r["TD fuse max"][0] == "30 A"
                and r["Non-TD fuse"][0] == "60 A" and r["Copper 75°C"][0] == "12 AWG"
                and val(r, "Overload max") == rnd(16.2 * 1.25, 1))

    def t_lra(it):
        r = calc(it, 11)
        lo, hi = 6.3 * 5000 / (208 * SQ3), 7.09 * 5000 / (208 * SQ3)
        ok = r["LRA"][0] == f"{lo:.1f} - {hi:.1f} A"
        ok &= r["Poles"][0] == "4" and val(r, "Slip") == rnd(100 * 60 / 1800, 1)
        r = calc(it, 11, v54=1075)
        return ok and r["Sync speed"][0] == "1200 RPM" and val(r, "Slip") == rnd(100 * 125 / 1200, 1)

    def t_mca(it):
        r = calc(it, 12)
        ok = val(r, "MCA") == rnd(1.25 * 14.1 + 1.2, 1) and r["MOCP"][0] == "30 A"
        # air handler: 10 kW strip heat + blower
        r = calc(it, 12, v56=3.5, v57=0, v58=41.7)
        return ok and val(r, "MCA") == rnd(1.25 * (3.5 + 41.7), 1) and r["MOCP"][0] == "60 A"

    def t_vd(it):
        r = calc(it, 13)
        vd = 2 * 12.9 * 18.8 * 75 / 10380
        ok = val(r, "Voltage drop") == rnd(vd, 2) and val(r, "Drop") == rnd(100 * vd / 240, 2)
        ok &= r["Smallest OK"][0] == "12 AWG"
        r = calc(it, 13, v62=2, v63=2, v61=12, v59=100, v60=200, v64=480)
        vd = SQ3 * 21.2 * 100 * 200 / 105600
        return ok and val(r, "Voltage drop") == rnd(vd, 2)

    def t_ampac(it):
        ok = all(fn_call(it, "ampac", k, m, c) == a for k, m, c, a in NEC_AMPACITY)
        r = calc(it, 14)
        ok &= val(r, "Allowable") == 35 and r["Max breaker"][0] == "30 A"
        r = calc(it, 14, v66=4, v70=104, v71=6)
        a = 30 * math.sqrt(50 / 60) * 0.8
        ok &= r["Ambient"][0] == "0.91 x" and val(r, "Allowable") == rnd(a, 1)
        ok &= r["Max breaker"][0] == "20 A"
        r = calc(it, 14, v66=9, v68=2, v70=100, v72=2)
        cf = math.sqrt((75 - ((100 - 32) / 1.8 + 33)) / 45)
        return ok and val(r, "Derated") == rnd(100 * cf, 1)

    def t_xfmr(it):
        r = calc(it, 15)
        ok = (val(r, "Primary FLA") == rnd(40 / 240, 3) and val(r, "Secondary FLA") == rnd(40 / 24, 2)
              and val(r, "Load") == rnd(100 * 1.2 * 24 / 40) and val(r, "Primary OCPD") == 0.5)
        r = calc(it, 15, v73=45000, v74=2, v75=480, v76=208, v77=0)
        return ok and val(r, "Primary FLA") == rnd(45000 / (480 * SQ3), 1) and r["Primary OCPD"][0] == "70 A max"

    def t_wye(it):
        r = calc(it, 16)
        ok = val(r, "Line-neutral") == rnd(208 / SQ3, 1) and r["System"][0] == "208Y/120 V"
        r = calc(it, 16, v95=2, v96=240)
        return ok and val(r, "High leg-N") == rnd(240 * SQ3 / 2, 1)

    def t_heat(it):
        r = calc(it, 17)
        kw = 10 * (208 / 240) ** 2
        cfm = 208 * 36.1 * 3.41214 / (1.08 * 25)
        return (val(r, "Output now") == rnd(kw, 2) and val(r, "Amps now") == rnd(kw * 1000 / 208, 1)
                and val(r, "Element") == rnd(240 ** 2 / 10000, 2) and val(r, "Airflow") == rnd(cfm))

    def t_therm(it):
        with open(os.path.join(ROOT, "tools", "data", "thermistor_10k3_bapi.csv")) as fh:
            table = list(csv.DictReader(l for l in fh if not l.startswith("#")))
        worst_r = worst_t = 0
        for row in table:
            f, ohm = float(row["temp_F"]), float(row["ohms"])
            worst_r = max(worst_r, abs(fn_call(it, "thRes", 2, f) / ohm - 1))
            worst_t = max(worst_t, abs(fn_call(it, "thTemp", 2, ohm) - f))
        ok = worst_r < 0.002 and worst_t < 0.05
        ok &= approx(fn_call(it, "thRes", 1, 32) / 32650, 1, 0.001)
        reset(it)
        ok &= approx(fn_call(it, "thRes", 3, 32), 10000 * math.exp(3950 * (1 / 273.15 - 1 / 298.15)), 1)
        r = calc(it, 18, v84=2, v85=29.49, v86=40)
        return ok and val(r, "Reads as") == 32.0 and r["Difference"][1] == "bad sensor / curve"

    def t_cost(it):
        r = calc(it, 19)
        kw = 230 * 10 * 0.9 / 1000
        ok = r["Per hour"][0] == f"${kw * 0.15:.2f}" and r["Per month"][0] == f"${kw * 0.15 * 8 * 30:.2f}"
        r = calc(it, 19, v91=24000)
        return ok and val(r, "EER now") == rnd(24000 / (kw * 1000), 1)

    def t_conv(it):
        r = calc(it, 20)
        w = 12000 * 0.29307107
        ok = r["Tons"][0] == "1" and r["W"][0] == "3516.85" and approx(val(r, "HP"), w / 745.7, 0.00001)
        r = calc(it, 20, v92=7, v93=77, v94=1)
        ok &= r["°C"][0] == "25" and r["K"][0] == "298.15"
        r = calc(it, 20, v92=6, v93=45, v94=1)
        return ok and r["F"][0] == "4.5E-5" and r["pF"][0] == "4.5E7" and r["nF"][0] == "45000"

    tool_checks = [t_ohm, t_power, t_load, t_serpar, t_ampchk, t_3ph, t_cap, t_wind, t_meg,
                   t_motor, t_lra, t_mca, t_vd, t_ampac, t_xfmr, t_wye, t_heat, t_therm,
                   t_cost, t_conv]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))

    ev = [shot("elec_home.png")]
    # every tool: open its tile, check its sums, screenshot it, go home
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset),
               -1,                            # redraw with the example values
               shot(f"elec_{k:02d}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        check("HOME returns to the tiles", lambda it: it.g["gScr"] == 1),
        # keypad typing on Ohm's law: 240 Enter
        *tap(*tile(1)), *keys("240"),
        check("typing shows in the box", lambda it: it.g["gEnt"] == 1 and fn_call(it, "entText") == "240"),
        shot("elec_typing.png"),
        KEY["enter"],
        check("Enter stores the typed volts", lambda it: it.g["gV"][0] == 240 and it.g["gEnt"] == 0),
        *keys("123"), DEL, KEY["enter"],
        check("Del erases a digit", lambda it: it.g["gV"][0] == 12),
        *keys("1.5.5"), KEY["enter"],
        check("only one decimal point", lambda it: it.g["gV"][0] == 1.55),
        *keys("9"), KEY["esc"],
        check("Esc cancels typing", lambda it: it.g["gV"][0] == 1.55 and it.g["gScr"] == 2),
        KEY["right"], *keys("3"), KEY["right"],
        check("moving on keeps the typed number", lambda it: it.g["gV"][1] == 3 and it.g["gTSel"] == 3),
        *tap(*menu(2)),
        check("RESET restores the examples", lambda it: it.g["gV"][0] == 120 and it.g["gV"][1] == 0),
        *tap(*menu(3)),
        check("PREV wraps to the last tool", lambda it: it.g["gTool"] == 20),
        *tap(*menu(4)), *tap(*menu(4)),
        check("NEXT steps forward", lambda it: it.g["gTool"] == 2),
        # a two-way choice flips when tapped
        *tap(*box(3)),
        check("tap flips 1-phase / 3-phase", lambda it: it.g["gV"][6] == 2),
        *tap(*box(3)),
        check("tap flips it back", lambda it: it.g["gV"][6] == 1),
        KEY["esc"],
        # a number box opens the entry dialog, a list opens the chooser
        *tap(*tile(10)), *tap(*box(4)), ("dialog", 28.5),
        check("dialog sets plate FLA", lambda it: it.g["gV"][47] == 28.5),
        # the lift from tapping the dialog's OK (over HOME) must not count
        [2], [3, 290, 230],
        check("a tap left over from a dialog is ignored", lambda it: it.g["gScr"] == 2 and it.g["gTool"] == 10),
        *tap(*box(1)), ("dialog", 12),
        check("chooser sets 10 HP", lambda it: it.g["gV"][44] == 12),
        KEY["up"],
        check("Up steps the list", lambda it: it.g["gV"][44] == 13),
        *tap(*menu(1)), ("dialog", None),
        check("cancelled chooser keeps the value", lambda it: it.g["gV"][44] == 13),
        *tap(*menu(2)),
        # minus starts a negative number
        *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)), *tap(*menu(4)),
        check("on wire ampacity", lambda it: it.g["gTool"] == 14),
        KEY["right"], KEY["right"], KEY["right"], KEY["right"],
        KEY["minus"], *keys("10"), KEY["enter"],
        check("minus key types a negative ambient", lambda it: it.g["gV"][69] == -10),
        *tap(*menu(2)),
        # help from the title bar and the Help key
        *tap(300, 10),
        shot("elec_help_tool.png"),
        *tap(160, 120),
        check("tool help closes", lambda it: it.g["gScr"] == 2),
        KEY["esc"],
        KEY["help"],
        shot("elec_help.png"),
        KEY["enter"],
        # Menu key: list of tools
        MENU, ("dialog", 13),
        check("Menu key opens a tool from the list", lambda it: it.g["gTool"] == 13 and it.g["gScr"] == 2),
        KEY["esc"],
        check("Esc goes back to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 13),
        KEY["down"], KEY["down"],
        check("Down wraps around the tiles", lambda it: it.g["gHome"] == 1),
        KEY["left"],
        check("Left wraps to the last tile", lambda it: it.g["gHome"] == 20),
        KEY["enter"],
        check("Enter opens the tile", lambda it: it.g["gTool"] == 20 and it.g["gScr"] == 2),
        KEY["esc"],
        -1,                                 # WAIT timeout is ignored
        *tap(295, 10),                      # EXIT
    ]
    it = Interp(src, ev)
    try:
        it.start("HVACELEC")
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
