#!/usr/bin/env python3
"""Simulator tests for hp-prime/HVACGAS.txt (gas heating and piping).

The pipe sizing answers are checked against the IFGC Table 402.4 data file
for the eight Arkansas tables (which are also compared with the printed
2018 Arkansas Fuel Gas Code) and the propane reference tables (every size
boundary at several lengths);
the other tools against the code text (sections 304 and 406), the CDA
Copper Tube Handbook values, published Schedule 40 weights and formulas
worked out here.  The touch and keypad flow is played through, and
screenshots go to docs/screens/.

Usage
  python3 tools/test_hvacgas.py              # test hp-prime/HVACGAS.txt
  python3 tools/test_hvacgas.py FILE OUTDIR  # test another copy
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, approx, num, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "data", "gas")
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}
PIPE = json.load(open(os.path.join(DATA, "ifgc_402_4.json"), encoding="utf-8"))["tables"]
# the tables as printed in the 2018 Arkansas Fuel Gas Code
ARK = json.load(open(os.path.join(DATA, "arkansas_402_4.json"), encoding="utf-8"))["tables"]
CU = json.load(open(os.path.join(DATA, "copper_tube.json"), encoding="utf-8"))
STEEL = ["1/8", "1/4", "3/8", "1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "4",
         "5", "6", "8", "10", "12"]
# Schedule 40 plain-end weights, lb/ft, as printed in pipe data tables (12 in
# is Schedule 40, 0.406 in wall, heavier than standard weight)
STEEL_WT = {"1/2": 0.85, "3/4": 1.13, "1": 1.68, "1-1/4": 2.27, "1-1/2": 2.72, "2": 3.65,
            "2-1/2": 5.79, "3": 7.58, "4": 10.79, "6": 18.97, "8": 28.55, "10": 40.48,
            "12": 53.52}


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


def fmt_in(x):
    """inches to the nearest 1/16, written the way the program writes them"""
    n = int(rnd(abs(x) * 16))
    w, f, d = n // 16, n % 16, 16
    while f and f % 2 == 0:
        f, d = f // 2, d // 2
    s = str(w) if not f else (f"{w}-{f}/{d}" if w else f"{f}/{d}")
    return s + " in"


def nums(text):
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", text)
    return float(m.group().replace(",", ""))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "HVACGAS.txt")
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
        return nums(r[label][0])

    def tables(it):
        """(chooser index, code table number, Arkansas?, sizes kept)"""
        return [(k, int(n), it.g["gTAR"][k - 1] == 1, len(fn_call(it, "sizeSet", it.g["gTSz"][k - 1])))
                for k, n in enumerate(it.g["gTNo"], 1)]

    def t_arkansas(it):
        # the chooser holds exactly the eight Arkansas tables, then propane
        # references; each Arkansas table matches the printed Arkansas code
        tl = tables(it)
        ok = [n for _, n, ar, _ in tl if ar] == [2, 5, 7, 9, 12, 14, 21, 22]
        ok &= all(not ar and PIPE[n - 1]["gas"] != "Natural" for _, n, ar, _ in tl[8:])
        for k, n, ar, nsz in tl[:8]:
            m = fn_call(it, "pipeTab", k)
            rows = ARK[str(n)]
            ok &= len(m) == len(rows) and nsz == len(rows[0]) - 1
            for row, mrow in zip(rows, m):
                ok &= [v or 0 for v in row[1:]] == [int(x) for x in mrow]
        return ok

    def t_size(it):
        # every table: at three lengths, a load equal to each size's capacity
        # picks that size, and one more picks the next size
        bad = []
        for k, n, ar, nsz in tables(it):
            t = PIPE[n - 1]
            names = fn_call(it, "sizeSet", it.g["gTSz"][k - 1])
            unit = 1 if t["units"] == "CFH" else 2
            for li in (0, len(t["lengths"]) // 2, len(t["lengths"]) - 1):
                L = t["lengths"][li]
                caps = t["capacity"][li][:nsz]
                for j, cap in enumerate(caps):
                    if not cap:
                        continue
                    r = calc(it, 1, v1=k, v2=L, v3=cap, v4=unit)
                    if r.get("Size", ("",))[0] != names[j]:
                        bad.append((n, L, cap, r.get("Size")))
                    later = [k for k in range(j + 1, len(caps)) if caps[k] > cap]
                    r = calc(it, 1, v1=k, v2=L, v3=cap + 1, v4=unit)
                    want = names[later[0]] if later else "none big enough"
                    if r.get("Size", ("",))[0] != want:
                        bad.append((n, L, cap + 1, r.get("Size")))
        if bad:
            print("pipe size mismatches:", bad[:5])
        return not bad

    def t_size_rules(it):
        # 52 ft uses the 60 ft row; 3/4 in carries 137 CFH there, 1 in 257
        r = calc(it, 1, v2=52, v3=150)
        ok = r["Length row"][0] == "60 ft" and r["Size"][0] == "1 in" and r["One smaller"][1] == "only 137"
        # 200,000 Btu/h at 1,000 Btu/ft3 is 200 CFH
        r = calc(it, 1, v3=200000, v4=3)
        ok &= r["Load"][0] == "200 CFH" and r["Size"][0] == "1 in"
        # Table A102.4: SG 0.70 x 0.93, SG 0.72 takes the next higher (0.75: x 0.90)
        r = calc(it, 1, v6=0.7)
        ok &= r["SG factor"][0] == "x 0.93"
        r = calc(it, 1, v6=0.72, v3=240)
        ok &= r["SG factor"][0] == "x 0.90" and r["Size"][0] == "1-1/4 in"   # 257 x 0.9 = 231 < 240
        # propane table 402.4(28) in kBtu/h; 100 CFH of propane = 251.6 kBtu/h
        t28 = PIPE[27]
        lp28 = it.g["gTNo"].index(28) + 1
        r = calc(it, 1, v1=lp28, v2=50, v3=100, v4=1)
        caps = t28["capacity"][t28["lengths"].index(50)]
        want = next(j for j, c in enumerate(caps) if c >= 251.6)
        ok &= r["Load"][0] == "251.6 kBtu/h" and r["Size"][0] == t28["sizes"][want] + " in"
        ok &= r["Table"][1].startswith("LP ref")
        # longer than the table
        r = calc(it, 1, v2=2500)
        return ok and r["Length"][0] == "past the table"

    def t_capacity(it):
        t = PIPE[1]
        r = calc(it, 2, v8=100)
        row = t["capacity"][t["lengths"].index(100)]
        return (r["Row 100 ft"][0] == "CFH" and val(r, "1/2 in") == row[0]
                and r["1/2 in"][1] == f"3/4 in:  {row[1]}" and val(r, "10 in") == row[12])

    def t_fittings(it):
        # Table A102.2 3/4 in: 90 ell 2.06, 45 ell 0.96, tee 4.12, gate 0.48
        r = calc(it, 3, v12=2)
        eq = 4 * 2.06 + 2 * 0.96 + 4.12 + 0.48
        return val(r, "Fittings") == rnd(eq, 2) and val(r, "Total length") == rnd(40 + eq, 1)

    def t_load(it):
        r = calc(it, 4)
        ok = r["Total load"][0] == "240,000 Btu/h" and val(r, "Gas flow") == 240
        r = calc(it, 4, v21=2)
        return ok and val(r, "Gas flow") == rnd(240000 / 2516, 1) and val(r, "Gallons/h") == rnd(240000 / 91500, 3)

    def t_clock(it):
        r = calc(it, 5)
        ok = val(r, "Gas flow") == 100 and r["Input"][0] == "100,000 Btu/h" and r["Verdict"][0] == "on rate"
        # 2 ft3 dial, 1 rev in 50 s, 1,030 Btu/ft3: 144 CFH, 148,320 Btu/h
        r = calc(it, 5, v23=2, v25=50, v26=1030, v27=125000)
        return ok and r["Input"][0] == "148,320 Btu/h" and r["Verdict"][0] == "overfired"

    def t_manifold(it):
        r = calc(it, 6)
        return val(r, "Set to") == rnd(3.5 * (100000 / 90000) ** 2, 2)

    def t_altitude(it):
        r = calc(it, 7)
        ok = r["Derated input"][0] == "80,000 Btu/h"
        r = calc(it, 7, v33=1500)
        return ok and val(r, "Derate") == 0

    def t_air(it):
        # 140,000 Btu/h: 7,000 ft3; indoor openings 140 in2; outdoor 35, 70, 46.7
        r = calc(it, 8, v42=1)
        ok = (val(r, "Needed") == 7000 and val(r, "Indoor opngs") == 140 and val(r, "Out direct") == 35
              and val(r, "Out horiz.") == 70 and val(r, "One opening") == 46.7)
        ok &= val(r, "Combination") == rnd(1 - 960 / 7000, 2)
        # 60,000 Btu/h: indoor openings 100 in2 minimum; metal louvers 75%
        r = calc(it, 8, v36=60000)
        ok &= val(r, "Indoor opngs") == 100 and r["Out direct"][1] == "each of 2, louver 20"
        # Arkansas 304.6: no outdoor opening under 12 in2 (30,000 / 4,000 = 7.5)
        r = calc(it, 8, v36=30000, v42=1)
        ok &= val(r, "Out direct") == 12 and val(r, "One opening") == 12 and val(r, "Out horiz.") == 15
        # known infiltration: 0.5 ACH, 60,000 other + 40,000 fan-assisted
        r = calc(it, 8, v36=100000, v37=40000, v41=0.5)
        return ok and val(r, "Needed") == rnd(21 / 0.5 * 60 + 15 / 0.5 * 40, 0)

    def t_flue(it):
        r = calc(it, 9, v44=6, v45=25)
        ok = (val(r, "Excess air") == rnd(100 * 6 / 14.9) and val(r, "CO air-free") == rnd(25 * 20.9 / 14.9)
              and val(r, "CO2") == rnd(11.7 * 14.9 / 20.9, 1))
        r = calc(it, 9, v43=3, v44=3, v45=300)
        return ok and val(r, "CO2") == rnd(15.4 * 17.9 / 20.9, 1) and val(r, "CO air-free") == 350

    def t_furnace(it):
        r = calc(it, 10)
        ok = r["Output"][0] == "64,000 Btu/h" and val(r, "Temp rise") == rnd(64000 / 1080, 1)
        r = calc(it, 10, v50=50)
        return ok and val(r, "Airflow") == rnd(64000 / (1.08 * 50))

    def t_oil(it):
        r = calc(it, 11, v52=126000, v54=140)
        gph = 126000 / 140000
        return (val(r, "Firing rate") == rnd(gph, 2) and val(r, "Nozzle") == rnd(gph / math.sqrt(1.4), 2)
                and val(r, "Your nozzle") == rnd(math.sqrt(1.4), 3))

    def t_test(it):
        # 2 psi system (not single-family): 3 psig; 2 in x 2,000 ft + 1 in x 500 ft
        r = calc(it, 12, v56=2, v57=1, v58=9, v59=2000, v60=6, v61=500)
        vol = 2.067 ** 2 * math.pi / 4 / 144 * 2000 + 1.049 ** 2 * math.pi / 4 / 144 * 500
        # 49.6 ft3: 250 ft3 or less, so the Arkansas minimum of 15 minutes
        ok = val(r, "Test pressure") == 3 and val(r, "Pipe volume") == rnd(vol, 2) and val(r, "Duration") == 15
        # 5 psig working: 7.5 psig test; 600 ft3 of 4 in pipe: 1/2 hour per
        # 500 ft3 = 36 minutes (IFGC, rounding up each 500 ft3: 60)
        L = 600 / (4.026 ** 2 * math.pi / 4 / 144)
        r = calc(it, 12, v56=5, v57=1, v58=12, v59=L)
        ok &= val(r, "Test pressure") == 7.5 and val(r, "Duration") == 36 and val(r, "Gauge") == 37.5
        ok &= r["Duration"][1].endswith("rounds up: 60")
        r = calc(it, 12, v56=5, v57=2, v58=12, v59=L)
        return ok and val(r, "Duration") == 15

    def t_cost(it):
        r = calc(it, 13)
        return (val(r, "Natural gas") == rnd(1.2 * 10 / 0.95, 2) and val(r, "Electric") == rnd(0.15 * 1e6 / 3412.14 / 3, 2)
                and r["Cheapest"][0] == "Natural gas")

    def t_conv(it):
        r = calc(it, 14, v71=27.7)
        ok = val(r, "psi") == 1 and val(r, "oz/in²") == 16
        r = calc(it, 14, v70=2, v71=1, v72=2)
        return ok and val(r, "Btu") == 100000 and r["kWh"][0] == "29.3071"

    def t_copper(it):
        names = {"K": 1, "L": 2, "M": 3}
        nominal = ["¼", "⅜", "½", "⅝", "¾", "1", "1¼", "1½", "2", "2½", "3", "3½", "4", "5", "6", "8", "10", "12"]
        ok = True
        for k, ty in names.items():
            for row in CU[k]:
                r = calc(it, 15, v73=ty, v74=nominal.index(row[0]) + 1)
                ok &= (r["Outside"][0] == f"{float(row[1]):.3f} in" and r["Inside"][0] == f"{float(row[2]):.3f} in"
                       and r["Inside"][1] == f"wall {float(row[3]):.3f} in" and val(r, "Weight") == float(row[5]))
        r = calc(it, 15, v73=3, v74=1)
        ok &= r["Size"][1] == "not made in Type M"
        r = calc(it, 15, v73=4, v75=8)          # 3/4 OD soft: .750 x .680, wall .035
        ok &= r["Inside"][0] == "0.680 in" and r["Inside"][1] == "wall 0.035 in"
        r = calc(it, 15, v73=3)
        return ok and r["Fuel gas"][0] == "not allowed"

    def t_steel(it):
        ok = True
        for s, w in STEEL_WT.items():
            r = calc(it, 16, v77=STEEL.index(s) + 1)
            ok &= abs(val(r, "Weight") / w - 1) <= 0.003     # tables round older weights
        r = calc(it, 16, v77=STEEL.index("1/2") + 1)
        return ok and r["Inside"][0] == "0.622 in" and val(r, "Threads") == 14 and r["Support"][0] == "every 6 ft"

    def t_offset(it):
        r = calc(it, 17)
        ok = val(r, "Travel") == 17 and r["Travel"][1].startswith(f"{12 * math.sqrt(2):.3f}")
        r = calc(it, 17, v79=9, v80=12, v81=2, v82=0.5)     # rolling: 15 in true offset, 22-1/2 deg
        tr = 15 / math.sin(math.radians(22.5))
        return (ok and val(r, "True offset") == 15 and r["Travel"][1].startswith(f"{tr:.3f}")
                and r["Travel"][0] == fmt_in(tr) and r["Cut length"][0] == fmt_in(tr - 1))

    def t_expansion(it):
        r = calc(it, 18)
        return r["Expansion"][1] == "1.128 in" and r["Expansion"][0] == "1-1/8 in"

    def t_brazing(it):
        r = calc(it, 19, v87=1)
        ok = val(r, "Solidus") == 1310 and val(r, "Liquidus") == 1460
        r = calc(it, 19, v87=16)
        return ok and r["Solder 95-5"][0] == "solder" and val(r, "Liquidus") == 464

    tool_checks = [t_size, t_capacity, t_fittings, t_load, t_clock, t_manifold, t_altitude, t_air,
                   t_flue, t_furnace, t_oil, t_test, t_cost, t_conv, t_copper, t_steel, t_offset,
                   t_expansion, t_brazing]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))

    ev = [shot("gas_home.png"), check("Arkansas tables match the printed Arkansas code", t_arkansas),
          check("pipe size rules: rows, units, gravity, propane", t_size_rules)]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset), -1,
               shot(f"gas_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        *tap(*tile(20)), ("dialog", 3),
        shot("gas_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 20),
        # pipe size: pick a table, type a length and a load
        *tap(*tile(1)),
        *tap(*box(1)), ("dialog", 9),
        check("chose propane Table 402.4(28)", lambda it: it.g["gV"][0] == 9 and it.g["gTNo"][8] == 28),
        KEY["right"], *keys("85"), KEY["enter"],
        check("typed the length", lambda it: it.g["gV"][1] == 85),
        *tap(*box(3)), ("dialog", 150),
        check("typed the load", lambda it: it.g["gV"][2] == 150),
        shot("gas_pipe_lp.png"),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][0] == 1 and it.g["gV"][1] == 60),
        *tap(300, 10),
        shot("gas_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 2),
        KEY["esc"],
        KEY["right"], KEY["down"],
        check("arrows move on the 4 x 5 grid", lambda it: it.g["gHome"] == 7),
        KEY["help"],
        shot("gas_help.png"),
        KEY["enter"],
        -1,
        *tap(295, 10),
    ]
    it = Interp(src, ev)
    try:
        it.start("HVACGAS")
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
