#!/usr/bin/env python3
"""Simulator tests for hp-prime/NECCALC.txt (the electrical-class app).

Answers are compared with values copied from the published tables (310.16,
310.17, 310.15(B)(1), Annex C conduit counts, 314.16(B)) and with the
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
    return ((k - 1) % 3) * 107 + 53, 23 + ((k - 1) // 3) * 72 + 34


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
        r = calc(it, 2)
        ok = r["Use"][0] == "8 AWG Cu"
        # 40 A continuous = 50 A; THHN at 40 C with 6 wires: 90 C column x 0.91 x 0.8
        r = calc(it, 2, v11=2, v13=3, v15=40, v16=6)
        ok &= r["By insulation"][0] == "6 AWG"        # 75 x 0.728 = 54.6 >= 50 (8 AWG: 40.0)
        ok &= r["By terminals"][0] == "8 AWG" and r["Use"][0] == "6 AWG Cu"
        r = calc(it, 2, v1=2, v15=104, v13=3, v16=6, v11=2)
        return ok and r["Use"][0] == "6 AWG Cu"

    def t_amp(it):
        ok = True
        for s, m, ins, a in T16:
            r = calc(it, 3, v17=si(s), v18=1 if m == "Cu" else 2, v19=INS.index(ins) + 1, v20=1)
            ok &= val(r, "Ampacity") == a
        for s, m, ins, a in T17:
            r = calc(it, 3, v17=si(s), v18=1 if m == "Cu" else 2, v19=INS.index(ins) + 1, v20=2)
            ok &= val(r, "Ampacity") == a
        # 310.15(B)(1) factors as printed: 90 C at 40 C 0.91, 75 C at 45 C 0.82
        r = calc(it, 3, v17=si("8"), v19=INS.index("THHN") + 1, v21=40)
        ok &= r["Temp factor"][0] == "0.91 x" and val(r, "Ampacity") == rnd(55 * 0.91, 1)
        r = calc(it, 3, v17=si("8"), v19=INS.index("THWN") + 1, v21=113, v1=2)
        ok &= r["Temp factor"][0] == "0.82 x"
        r = calc(it, 3, v17=si("10"), v19=INS.index("THHN") + 1, v22=9)
        ok &= val(r, "Ampacity") == 28 and val(r, "Breaker max") == 30
        r = calc(it, 3, v17=si("12"), v19=INS.index("THHN") + 1, v23=3)
        ok &= val(r, "Ampacity") == 25
        # NM-B: 90 C derating, 60 C cap
        r = calc(it, 3, v17=si("12"), v19=INS.index("NM-B cable") + 1, v22=6)
        ok &= val(r, "Ampacity") == 20
        r = calc(it, 3, v17=si("14"), v18=2)
        return ok and r["Table"][0] == "not listed"

    def t_brk(it):
        r = calc(it, 4)
        ok = val(r, "Min breaker") == 20 and r["Result"][0] == "20 A breaker"
        r = calc(it, 4, v24=40, v25=10, v26=si("8"), v28=2)
        ok &= val(r, "Min breaker") == 60 and r["Result"][0] == "larger wire"
        r = calc(it, 4, v24=40, v25=10, v26=si("6"), v28=2)
        return ok and r["Result"][0] == "60 A breaker" and val(r, "Max for wire") == 70

    def t_fill(it):
        ok = True
        conds = ["EMT", "FMC", "IMC", "RMC", "PVC Sch 40", "PVC Sch 80"]
        for c, t, g, s, n in ANNEX_C:
            r = calc(it, 5, v30=conds.index(c) + 1, v31=TRADE.index(t) + 1, v32=g, v33=FILL.index(s) + 1)
            ok &= val(r, "Max wires") == n
        # conduit size for 9 #12 THHN and a #12 ground: 10 x 0.0133 = 0.133 in2 -> 3/4 in EMT
        r = calc(it, 5, v29=2, v34=9, v36=1)
        ok &= r["Use"][0] == "3/4 in EMT"
        r = calc(it, 5, v29=2, v30=5, v33=FILL.index("1/0") + 1, v34=4)
        # 4 x 1/0 THHN: 1-1/4 in holds 3.13 of them, 1-1/2 in holds 4.28
        ok &= r["Use"][0] == "1-1/2 in PVC Sch 40"
        r = calc(it, 5, v32=5, v33=FILL.index("1/0") + 1)
        return ok and r["Table 5"][0] == "size not listed"

    def t_awg(it):
        r = calc(it, 6)
        ok = val(r, "Area") == 6530 and val(r, "Table 8 R") == 1.98 and r["Fill area"][0] == "0.0133 in²"
        r = calc(it, 6, v37=si("4"), v39=INS.index("THWN") + 1)
        return ok and r["Raceway"][0] == "70 / 85 / 95 A" and r["Free air"][0] == "105 / 125 / 140 A"

    def t_box(it):
        r = calc(it, 7)
        ok = val(r, "Box needs") == 16 and r["Your box"][0] == "big enough"
        r = calc(it, 7, v40=4, v41=6, v43=2, v46=18)
        return ok and val(r, "Box needs") == rnd(2.25 * (6 + 1 + 4 + 1), 2) and r["Your box"][0] == "TOO SMALL"

    def t_ohm(it):
        r = calc(it, 8)
        return val(r, "Amps (I)") == 10 and val(r, "Watts (P)") == 1200

    tool_checks = [t_vd, t_wire, t_amp, t_brk, t_fill, t_awg, t_box, t_ohm]
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
        *tap(*tile(9)), ("dialog", 3),
        shot("nec_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 9),
        # ampacity: free air, typed size via the chooser, ambient typed
        *tap(*tile(3)),
        *tap(*box(4)),
        check("tap flips to free air", lambda it: it.g["gV"][19] == 2),
        KEY["right"], *keys("40"), KEY["enter"],
        check("typed the ambient", lambda it: it.g["gV"][20] == 40),
        *tap(*box(3)), ("dialog", INS.index("THHN") + 1),
        check("chose THHN", lambda it: it.g["gV"][18] == INS.index("THHN") + 1),
        shot("nec_ampacity_free_air.png"),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][19] == 1 and it.g["gV"][20] == 30),
        [2], [3, 290, 230],
        check("left-over tap ignored", lambda it: it.g["gScr"] == 2),
        *tap(300, 10),
        shot("nec_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 4),
        KEY["esc"],
        KEY["right"], KEY["down"],
        check("arrows move on the 3 x 3 grid", lambda it: it.g["gHome"] == 8),
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
