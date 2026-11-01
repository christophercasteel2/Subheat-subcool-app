#!/usr/bin/env python3
"""Simulator tests for hp-prime/NECCALC.txt (the electrical-class app).

Answers are compared with values copied from the published tables (310.16,
310.17, 310.15(B)(1), Annex C conduit counts, 314.16, 250.122, 250.66,
310.12), with worked examples from electricalcalctools.com and with the
formulas worked out here; the touch and keypad flow is played through, and
screenshots go to docs/screens/.

Usage
  python3 tools/test_neccalc.py              # test hp-prime/NECCALC.txt
  python3 tools/test_neccalc.py FILE OUTDIR  # test another copy
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
SIZES = ["18", "16", "14", "12", "10", "8", "6", "4", "3", "2", "1", "1/0", "2/0",
         "3/0", "4/0", "250", "300", "350", "400", "500", "600", "700", "750", "800",
         "900", "1000", "1250", "1500", "1750", "2000"]
INS = ["TW", "UF", "RHW", "THHW wet", "THW", "THWN", "XHHW wet", "USE", "ZW", "TBS",
       "SA", "SIS", "FEP", "FEPB", "MI", "RHH", "RHW-2", "THHN", "THHW dry", "THW-2",
       "THWN-2", "USE-2", "XHH", "XHHW dry", "XHHW-2", "ZW-2", "NM-B cable"]
FILL = SIZES[2:20]
TRADE = ["3/8", "1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "3-1/2", "4", "5", "6"]

# spot values typed from the published tables, separately from the generator
T16 = [("4", "Cu", "THWN", 85), ("12", "Cu", "THHN", 30), ("1/0", "Al", "XHHW wet", 120),
       ("500", "Cu", "TW", 320), ("2000", "Al", "XHHW-2", 630), ("14", "Cu", "TW", 15),
       ("3/0", "Cu", "THW", 200), ("250", "Al", "THHN", 230)]
T17 = [("4", "Cu", "THWN", 125), ("12", "Cu", "THHN", 40), ("1/0", "Al", "XHHW wet", 180),
       ("500", "Cu", "TW", 515), ("2000", "Cu", "THWN-2", 1560), ("16", "Cu", "THHN", 24)]
# Annex C counts: (conduit, trade size, insulation group, wire size, count)
ANNEX_C = [("EMT", "1", 1, "12", 26), ("EMT", "1", 1, "10", 16), ("EMT", "1", 1, "8", 9),
           ("EMT", "1/2", 1, "12", 9), ("EMT", "1/2", 2, "12", 6), ("EMT", "3/4", 1, "12", 16),
           ("EMT", "1/2", 1, "14", 12)]


def rnd(x, n=0):
    m = 10 ** n
    return math.copysign(math.floor(abs(x) * m + 0.5) / m, x)


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 43 + 20


def box(k):
    return ((k - 1) % 2) * 160 + 115, 24 + ((k - 1) // 2) * 20 + 8


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "NECCALC.txt")
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

    def val(r, label):
        return num(r[label][0])

    def si(s):
        return SIZES.index(s) + 1

    def t_vd(it):
        r = calc(it, 1)
        vd = 2 * 12.9 * 20 * 100 / 6530
        ok = val(r, "Voltage drop") == rnd(vd, 2) and r["Smallest OK"][0] == "8 AWG"
        r = calc(it, 1, v8=2)
        ok &= val(r, "Voltage drop") == rnd(2 * 20 * 100 * 1.98 / 1000, 2)
        r = calc(it, 1, v2=100, v3=200, v4=si("2"), v5=2, v6=2, v7=480)
        return ok and val(r, "Voltage drop") == rnd(math.sqrt(3) * 21.2 * 100 * 200 / 66360, 2)

    def t_wire(it):
        # 20 A at 120 V, 50 ft: 14 AWG carries it, 240.4(D) needs 12 AWG for
        # the 20 A breaker, and 3% drop needs 10 AWG (12 AWG: 3.30%)
        r = calc(it, 2)
        ok = r["By insulation"][0] == "14 AWG" and r["3% drop"][0] == "10 AWG"
        ok &= r["5% drop"][0] == "12 AWG" and r["Use"][0] == "10 AWG Cu"
        ok &= r["3% drop"][1].startswith(f"{rnd(100 * 2 * 20 * 50 * 1.24 / 1000 / 120, 2):.2f}%")
        r = calc(it, 2, v16=0)
        ok &= r["Use"][0] == "12 AWG Cu" and "240.4(D)" in r["Use"][1]
        # 40 A continuous = 50 A; THHN at 40 C: 8 AWG 55 x 0.91 = 50.05 A
        r = calc(it, 2, v10=40, v11=2, v13=3, v15=40, v16=0)
        ok &= r["By insulation"][0] == "8 AWG" and r["Use"][0] == "8 AWG Cu"
        r = calc(it, 2, v10=40, v11=2, v13=3, v1=2, v15=104, v16=0)
        ok &= r["Use"][0] == "8 AWG Cu"
        # 100 A aluminum, 200 ft, 480 V 3-phase: 3% needs R <= 0.4157 -> 3 AWG,
        # 75 C ampacity needs 1 AWG (100 A)
        r = calc(it, 2, v10=100, v12=2, v16=200, v17=7)
        return ok and r["3% drop"][0] == "3 AWG" and r["Use"][0] == "1 AWG Al"

    def t_amp(it):
        ok = True
        for s, m, ins, a in T16:
            r = calc(it, 3, v18=si(s), v19=1 if m == "Cu" else 2, v20=INS.index(ins) + 1, v21=1)
            ok &= val(r, "Ampacity") == a
        for s, m, ins, a in T17:
            r = calc(it, 3, v18=si(s), v19=1 if m == "Cu" else 2, v20=INS.index(ins) + 1, v21=2)
            ok &= val(r, "Ampacity") == a
        # 310.15(B)(1) factors as printed: 90 C at 40 C 0.91, 75 C at 45 C 0.82
        r = calc(it, 3, v18=si("8"), v20=INS.index("THHN") + 1, v22=40)
        ok &= r["Temp factor"][0] == "0.91 x" and val(r, "Ampacity") == rnd(55 * 0.91, 1)
        r = calc(it, 3, v18=si("8"), v20=INS.index("THWN") + 1, v22=113, v1=2)
        ok &= r["Temp factor"][0] == "0.82 x"
        r = calc(it, 3, v18=si("10"), v20=INS.index("THHN") + 1, v23=9)
        ok &= val(r, "Ampacity") == 28 and val(r, "Breaker max") == 30
        r = calc(it, 3, v18=si("12"), v20=INS.index("THHN") + 1, v24=3)
        ok &= val(r, "Ampacity") == 25
        # NM-B: 90 C derating, 60 C cap
        r = calc(it, 3, v18=si("12"), v20=INS.index("NM-B cable") + 1, v23=6)
        ok &= val(r, "Ampacity") == 20
        r = calc(it, 3, v18=si("14"), v19=2)
        return ok and r["Table"][0] == "not listed"

    def t_brk(it):
        r = calc(it, 4)
        ok = val(r, "Min breaker") == 20 and r["Result"][0] == "20 A breaker"
        r = calc(it, 4, v25=40, v26=10, v27=si("8"), v29=2)
        ok &= val(r, "Min breaker") == 60 and r["Result"][0] == "larger wire"
        r = calc(it, 4, v25=40, v26=10, v27=si("6"), v29=2)
        return ok and r["Result"][0] == "60 A breaker" and val(r, "Max for wire") == 70

    def t_fill(it):
        ok = True
        conds = ["EMT", "FMC", "IMC", "RMC", "PVC Sch 40", "PVC Sch 80"]
        for c, t, g, s, n in ANNEX_C:
            r = calc(it, 5, v31=conds.index(c) + 1, v32=TRADE.index(t) + 1, v33=g, v34=FILL.index(s) + 1)
            ok &= val(r, "Max wires") == n
        # conduit size for 9 #12 THHN and a #12 ground: 10 x 0.0133 = 0.133 in2 -> 3/4 in EMT
        r = calc(it, 5, v30=2, v35=9, v37=1)
        ok &= r["Use"][0] == "3/4 in EMT"
        r = calc(it, 5, v30=2, v31=5, v34=FILL.index("1/0") + 1, v35=4)
        # 4 x 1/0 THHN: 1-1/4 in holds 3.13 of them, 1-1/2 in holds 4.28
        ok &= r["Use"][0] == "1-1/2 in PVC Sch 40"
        r = calc(it, 5, v33=5, v34=FILL.index("1/0") + 1)
        return ok and r["Table 5"][0] == "size not listed"

    def t_awg(it):
        r = calc(it, 6)
        ok = val(r, "Area") == 6530 and val(r, "Table 8 R") == 1.98 and r["Fill area"][0] == "0.0133 in²"
        ok &= "20 A" in r["Common use"][1]
        r = calc(it, 6, v38=si("4"), v40=INS.index("THWN") + 1)
        return ok and r["Raceway"][0] == "70 / 85 / 95 A" and r["Free air"][0] == "105 / 125 / 140 A"

    def t_feed(it):
        # 100 A, 240 V, 100 ft copper, 3%: 3 AWG for 100 A; drop 2 x 100 x 100 x 0.245
        r = calc(it, 7)
        ok = r["By ampacity"][0] == "3 AWG" and r["By drop"][0] == "4 AWG" and r["Use"][0] == "3 AWG Cu"
        ok &= val(r, "Drop") == rnd(100 * 2 * 100 * 100 * 0.245 / 1000 / 240, 2)
        ok &= r["EGC"][0] == "8 AWG Cu"
        # 200 A dwelling: 166 A -> 2/0 Cu (175 A), 4/0 Al (180 A) (310.12)
        r = calc(it, 7, v41=200, v43=50, v45=2)
        ok &= val(r, "Required") == 166 and r["Use"][0] == "2/0 AWG Cu"
        r = calc(it, 7, v41=200, v43=50, v45=2, v44=2)
        ok &= r["Use"][0] == "4/0 AWG Al"
        # 2026 NEC 310.12: no 83% sizing with 60 C wire, or outside 100-400 A
        r = calc(it, 7, v41=200, v43=50, v45=2, v47=1)
        ok &= val(r, "Required") == 200 and "75°C" in r["Required"][1]
        r = calc(it, 7, v41=60, v43=50, v45=2)
        ok &= val(r, "Required") == 60
        # a long run: 100 A, 300 ft, 2%: R <= 0.02 x 240 x 1000 / (2 x 100 x 300) = 0.08 -> 3/0 (0.0766)
        r = calc(it, 7, v43=300, v46=1)
        return ok and r["Use"][0] == "3/0 AWG Cu"

    def t_gnd(it):
        ok = True
        for a, cu, al in [(60, "10", "8"), (200, "6", "4"), (225, "4", "2"), (400, "3", "1"),
                          (15, "14", "12"), (2000, "250", "400"), (800, "1/0", "3/0")]:
            r = calc(it, 8, v49=a)
            ok &= r["Copper EGC"][0].split()[0] == cu and r["Aluminum EGC"][0].split()[0] == al
        for sz, mat, cu, al in [("2/0", 1, "4", "2"), ("4/0", 2, "4", "2"), ("3/0", 2, "6", "4"),
                                ("500", 1, "1/0", "3/0"), ("1/0", 1, "6", "4"), ("2", 1, "8", "6"),
                                ("1250", 1, "3/0", "250")]:
            r = calc(it, 8, v48=2, v51=si(sz), v52=mat)
            ok &= r["Copper GEC"][0].split()[0] == cu and r["Aluminum GEC"][0].split()[0] == al
        return ok

    def t_box(it):
        r = calc(it, 9)
        ok = val(r, "Box volume") == 21 and val(r, "Box needs") == 16 and r["Result"][0] == "big enough"
        boxes = fn_call(it, "choiceList", 7)
        for name, vol in [("4-11/16x2-1/8 sq", 42), ("3x2x3-1/2 device", 18), ("4x1-1/4 rnd/oct", 12.5)]:
            r = calc(it, 9, v53=boxes.index(name) + 1)
            ok &= val(r, "Box volume") == vol
        r = calc(it, 9, v53=1, v54=18, v55=4, v56=6, v58=2)
        return ok and val(r, "Box needs") == rnd(2.25 * (6 + 1 + 4 + 1), 2) and r["Result"][0] == "TOO SMALL"

    def t_mca(it):
        # the site's worked example: RLA 18.5 A, fan 0.7 A
        r = calc(it, 10)
        ok = approx(val(r, "MCA"), 1.25 * 18.5 + 0.7, 0.006) and val(r, "MOCP") == 35
        ok &= r["Wire Cu 75°C"][0] == "12 AWG (25 A)"
        r = calc(it, 10, v61=28, v62=1.2)
        ok &= val(r, "MOCP") == 50
        # 175% = 15.4 -> 20 A, over 225% = 19.8 -> 15 A
        r = calc(it, 10, v61=8.8, v62=0)
        ok &= val(r, "MOCP") == 15
        r = calc(it, 10, v64=40)
        return ok and val(r, "MOCP") == 40 and "nameplate" in r["MOCP"][1]

    def t_pow(it):
        r = calc(it, 11)
        ok = val(r, "Real power") == 4800 and val(r, "Ohms") == 12
        r = calc(it, 11, v65=480, v66=0, v68=10000, v69=0.8, v70=2)
        i = 10000 / (math.sqrt(3) * 480 * 0.8)
        ok &= approx(val(r, "Amps"), i, 0.001) and approx(val(r, "Apparent"), 12500, 0.01)
        ok &= approx(val(r, "Reactive"), 7500, 0.01)
        return ok

    def t_ohm(it):
        r = calc(it, 12)
        return val(r, "Amps (I)") == 10 and val(r, "Watts (P)") == 1200

    def t_kwh(it):
        # the site's example: 1500 W, 8 h a day, 30 days, $0.13
        r = calc(it, 13, v75=1500, v79=0.13)
        return (val(r, "Daily") == 12 and val(r, "Monthly") == 360 and val(r, "Yearly") == 4380
                and r["Monthly cost"][0] == "$46.80")

    def t_cost(it):
        st = fn_call(it, "choiceList", 22)
        r = calc(it, 14, v80=st.index("Texas") + 1)
        ok = r["Monthly"][0] == f"${850 * 0.132:.2f}" and r["Rate"][0].startswith("$0.132")
        r = calc(it, 14, v81=0.2, v82=1000)
        return ok and r["Monthly"][0] == "$200.00" and r["Yearly"][0] == "$2400.00"

    def t_der(it):
        r = calc(it, 15, v84=3, v85=40, v86=6)
        return r["Temp factor"][0] == "0.91 x" and val(r, "Derated") == rnd(35 * 0.91 * 0.8, 1)

    def t_vdt(it):
        r = calc(it, 16)
        ok = val(r, "100 ft") == rnd(100 * 2 * 15 * 100 * 3.14 / 1000 / 120, 2)
        ok &= val(r, "Longest run") == math.floor(0.03 * 120 / (2 * 15 * 3.14 / 1000))
        r = calc(it, 16, v87=6, v88=30, v89=2, v90=si("8"))
        pc = 100 * math.sqrt(3) * 30 * 250 * 1.28 / 1000 / 240
        return ok and val(r, "250 ft") == rnd(pc, 2)

    def t_bw(it):
        brk = fn_call(it, "choiceList", 23)
        r = calc(it, 17)
        ok = r["Cu 60°C"][0] == "12 AWG (20 A)" and r["Al 75°C"][0] == "10 AWG (30 A)"
        r = calc(it, 17, v91=brk.index("60 A") + 1)
        ok &= r["Cu 60°C"][0] == "4 AWG (70 A)" and r["Cu 75°C"][0] == "6 AWG (65 A)"
        ok &= r["EGC"][0] == "10 AWG Cu"
        r = calc(it, 17, v91=brk.index("400 A") + 1)
        ok &= r["Cu 75°C"][0] == "600 kcmil (420 A)"
        r = calc(it, 17, v91=brk.index("800 A") + 1)
        return ok and r["Cu 75°C"][0] == "2 sets of 600 kcmil"

    def t_app(it):
        ap = fn_call(it, "choiceList", 24)
        r = calc(it, 18)
        ok = r["Breaker"][0] == "30 A 2-pole" and r["Outlet"][0] == "14-30"
        r = calc(it, 18, v92=ap.index("EV charger 48 A") + 1)
        ok &= r["Breaker"][0] == "60 A 2-pole (125%)" and r["Copper"][0].startswith("#6 AWG")
        r = calc(it, 18, v92=ap.index("EV charger 16 A") + 1)
        return ok and r["Copper"][0].startswith("#12 AWG")

    def t_nema(it):
        nm = fn_call(it, "choiceList", 25)
        r = calc(it, 19)
        ok = r["Voltage"][0] == "125/250 V" and val(r, "Rating") == 50 and r["Type"][0] == "straight blade"
        r = calc(it, 19, v93=nm.index("NEMA L14-30") + 1)
        return ok and r["Type"][0] == "locking (twist)" and val(r, "Cord load") == 24

    tool_checks = [t_vd, t_wire, t_amp, t_brk, t_fill, t_awg, t_feed, t_gnd, t_box, t_mca,
                   t_pow, t_ohm, t_kwh, t_cost, t_der, t_vdt, t_bw, t_app, t_nema]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))

    ev = [shot("nec_home.png")]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset), -1,
               shot(f"nec_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        # Learn tile: pick a page from the list
        *tap(*tile(20)), ("dialog", 11),
        shot("nec_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 20),
        # ampacity: free air, typed size via the chooser, ambient typed
        *tap(*tile(3)),
        *tap(*box(4)),
        check("tap flips to free air", lambda it: it.g["gV"][20] == 2),
        KEY["right"], *keys("40"), KEY["enter"],
        check("typed the ambient", lambda it: it.g["gV"][21] == 40),
        *tap(*box(3)), ("dialog", INS.index("THHN") + 1),
        check("chose THHN", lambda it: it.g["gV"][19] == INS.index("THHN") + 1),
        shot("nec_ampacity_free_air.png"),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][20] == 1 and it.g["gV"][21] == 30),
        [2], [3, 290, 230],
        check("left-over tap ignored", lambda it: it.g["gScr"] == 2),
        *tap(300, 10),
        shot("nec_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 4),
        KEY["esc"],
        KEY["right"], KEY["down"],
        check("arrows move on the 4 x 5 grid", lambda it: it.g["gHome"] == 9),
        KEY["up"], KEY["up"], KEY["up"],
        check("Up wraps to the bottom row", lambda it: it.g["gHome"] == 17),
        KEY["down"],
        check("Down wraps to the top row", lambda it: it.g["gHome"] == 1),
        KEY["help"],
        shot("nec_help.png"),
        KEY["enter"],
        -1,
        *tap(295, 10),
    ]
    it = Interp(src, ev)
    try:
        it.start("NECCALC")
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
