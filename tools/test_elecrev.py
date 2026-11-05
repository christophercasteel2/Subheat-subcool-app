#!/usr/bin/env python3
"""Simulator tests for hp-prime/ELECREV.txt (electricity exam review,
Units 9, 11 and 13).

The expected answers are the textbook's worked examples and the review
answers worked again here with plain arithmetic.  Every notes page is
checked to fit the screen, and the touch flow is played through;
screenshots go to docs/screens/.

Usage
  python3 tools/test_elecrev.py              # test hp-prime/ELECREV.txt
  python3 tools/test_elecrev.py FILE OUTDIR  # test another copy
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, font, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 36 + 16


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
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "ELECREV.txt")
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

    def size_idx(it, name):
        return it.g["gSize"].index(name) + 1 if "gSize" in it.g else None

    sizes = ["18", "16", "14", "12", "10", "8", "6", "4", "3", "2", "1", "1/0", "2/0", "3/0", "4/0",
             "250", "300", "350", "400", "500", "600", "700", "750", "800", "900", "1000", "1250",
             "1500", "1750", "2000"]

    def sz(name):
        return sizes.index(name) + 1

    def ins(it, name):
        names = fn_call(it, "choiceList", 9)
        return [n.split(" ")[0] for n in names].index(name) + 1

    # ---- Unit 9 --------------------------------------------------------
    def t_kcl(it):
        r = calc(it, 1)                                 # 4 + 6 - 10 = 0
        ok = val(r, "In - out") == 0
        r = calc(it, 1, v1=6, v2=2, v3=0, v6=0.8, v7=0)   # point B: I4 = 2 - 0.8
        ok &= close(val(r, "Out 2"), 1.2)
        r = calc(it, 1, v1=2, v2=6, v3=0, v6=5, v7=0)   # In 2 = -1: wrong direction
        return ok and "Negative" in " ".join(it.g["gRV"])

    def t_kvl(it):
        r = calc(it, 2)                                 # loop ACDF: E3 = 40
        ok = val(r, "E5") == 40
        r = calc(it, 2, v10=120, v11=3, v12=32, v13=48, v14=40)
        return ok and val(r, "-drops + ET") == 0

    def t_net(it):
        e1, e2, r1, r2, r3 = 24, 10, 330, 200, 100      # review Q6-10
        v = (e1 / r1 + e2 / r2) / (1 / r1 + 1 / r2 + 1 / r3)
        r = calc(it, 3)
        txt = " | ".join(it.g["gRV"])
        return (close(val(r, "I1"), (e1 - v) / r1) and close(val(r, "I2"), (e2 - v) / r2)
                and close(val(r, "E3 (R3)"), v) and close(val(r, "E1 (R1)"), e1 - v)
                and "L1: 24 = 430 I1 + 100 I2" in txt and "L2: 10 = 100 I1 + 300 I2" in txt)

    def t_thev(it):
        r = calc(it, 4)                                 # Fig 9-9: 18 V, 1.5 ohm, 1.565 A
        ok = val(r, "ETH") == 18 and val(r, "RTH") == 1.5 and close(val(r, "I load"), 18 / 11.5)
        r = calc(it, 4, v29=48, v30=4, v31=20, v33=0)   # review 11, 12
        ok &= close(val(r, "ETH"), 40) and close(val(r, "RTH"), 10 / 3)
        r = calc(it, 4, v29=20, v30=2.5, v31=16, v33=8)  # review 13-15
        rn = 2.5 * 16 / 18.5
        return ok and close(val(r, "IN"), 8) and close(val(r, "RN"), rn) and close(val(r, "I load"), 8 * rn / (rn + 8))

    def t_eqv(it):
        r = calc(it, 5)
        ok = close(val(r, "I load"), 18 / 11.5) and close(val(r, "E load"), 180 / 11.5)
        r = calc(it, 5, v34=2, v35=12, v36=1.5, v37=6)  # Fig 9-19
        return ok and close(val(r, "E load"), 14.4) and close(val(r, "I load"), 2.4) and close(val(r, "I in RN"), 9.6)

    def t_sup(it):
        r = calc(it, 6)                                 # Example 9-1
        ok = close(val(r, " IT, I2", 1), 6.857142857 / 300) and val(r, "1 Es2 short") == 840
        v = (24 / 600 + 12 / 1200) / (1 / 600 + 1 / 300 + 1 / 1200)
        ok &= close(val(r, "3 I2 total"), v / 300)
        r = calc(it, 6, v43=2)
        return ok and close(val(r, "3 I2 total"), 6.857142857 / 300 - 1.714285714 / 300)

    # ---- Unit 11 -------------------------------------------------------
    def t_wire(it):
        r = calc(it, 7)                                 # Example 11-9
        ok = abs(val(r, "R") - 0.218) < 0.0005
        r = calc(it, 7, v47=sz("2"), v49=450)
        ok &= close(val(r, "R"), 10.4 * 450 / 66370)
        r = calc(it, 7, v44=4, v47=sz("8"), v49=500, v50=1.817)
        ok &= r["Closest"][0].startswith("Iron")
        r = calc(it, 7, v44=2, v45=1, v49=4330, v50=0.167)   # 440,778 CM -> 500 kcmil
        ok &= abs(val(r, "CM") - 440778) < 1 and r["Use size"][0].startswith("500 kcmil")
        r = calc(it, 7, v51=75, v47=sz("6"))
        return ok and close(val(r, "K at 75°C"), 12.6308)

    def t_vd(it):
        r = calc(it, 8)                                 # Example 11-13
        ok = abs(val(r, "ED") - 12.023) < 0.0005
        r = calc(it, 8, v52=2, v53=1, v54=sz("1/0"), v56=88, v57=175)   # Example 11-14
        return ok and abs(val(r, "ED") - 4.298) < 0.0005

    def t_run(it):
        r = calc(it, 9)                                 # review 11, 12
        ok = r["Use size"][0] == "600 kcmil" and r["Or parallel"][0].startswith("3 x 4/0")
        r = calc(it, 9, v59=2, v60=4, v61=480, v62=6, v63=235, v64=1800)   # review 13
        ok &= r["Use size"][0] == "300 kcmil"
        r = calc(it, 9, v59=2, v60=4, v61=480, v62=5, v63=522, v64=300)    # practice 5
        return ok and r["Use size"][0] == "2/0 AWG"

    def t_amp(it):
        r = calc(it, 10)                                # review 3: 44 A
        ok = val(r, "Ampacity") == 44
        r = calc(it, 10, v66=sz("1/0"), v67=2, v68=ins(it, "THWN"), v69=1, v70=30, v72=6)
        ok &= val(r, "Ampacity") == 96                  # review 4
        r = calc(it, 10, v66=sz("12"), v67=1, v68=ins(it, "THHN"), v69=1, v70=95, v71=1, v72=25)
        ok &= close(val(r, "Ampacity"), 12.96)          # review 10
        r = calc(it, 10, v66=sz("500"), v67=1, v68=ins(it, "RHH"), v69=1, v70=58, v71=2, v72=3)
        ok &= close(val(r, "Ampacity"), 305.3)          # practice 3
        r = calc(it, 10, v66=sz("10"), v67=1, v68=ins(it, "TW"), v69=1, v70=65, v71=2)
        return ok and "not allowed" in r["Temp factor"][0]   # review 7

    def t_load(it):
        r = calc(it, 11)                                # Example 11-8: 2/0
        ok = close(val(r, "÷ factors"), 171.326754) and r["Use size"][0] == "2/0 AWG"
        r = calc(it, 11, v73=50, v74=4, v75=250, v77=ins(it, "RHW-2"), v79=112, v81=2)
        ok &= r["Use size"][0] == "4/0 AWG"             # practice 6
        r = calc(it, 11, v73=25, v74=3, v75=480, v77=ins(it, "THWN-2"), v78=2, v79=48, v80=2, v81=6)
        ok &= r["Use size"][0] == "1/0 AWG" and r["Column"][0] == "60°C"   # practice 7
        r = calc(it, 11, v73=25, v74=3, v75=240, v77=ins(it, "TW"), v79=90, v81=2)
        return ok and r["Use size"][0] == "2/0 AWG"     # heater

    def t_temp(it):
        r = calc(it, 12)                                # practice 9
        ok = close(val(r, "R at T"), 1.2696, 0.0001)
        r = calc(it, 12, v83=1, v86=40)                 # practice 10
        return ok and close(val(r, "K at T"), 18.36)

    def t_neh(it):
        r = calc(it, 13)
        return close(val(r, "= amperes"), 1000 * math.sqrt(70 / (25.7 * 1.01 * 60)))

    # ---- Unit 13 -------------------------------------------------------
    def t_bank(it):
        r = calc(it, 14)                                # 24 V 120 A-hr
        ok = val(r, "Voltage") == 24 and val(r, "A-hr") == 120
        r = calc(it, 14, v96=4, v97=1)
        ok &= val(r, "Voltage") == 48 and val(r, "A-hr") == 60
        r = calc(it, 14, v96=1, v97=4)
        return ok and val(r, "Voltage") == 12 and val(r, "A-hr") == 240

    def t_need(it):
        r = calc(it, 15)                                # solar: 28 x 2 = 56
        return val(r, "In series") == 28 and val(r, "Strings") == 2 and val(r, "Total cells") == 56

    def t_cap(it):
        r = calc(it, 16)                                # D cell: 100 h, 15 W-hr
        ok = val(r, "Run time") == 100 and val(r, "Watt-hours") == 15
        r = calc(it, 16, v102=80, v103=2, v104=12, v105=0)
        ok &= val(r, "Max charge") == 8 and val(r, "20-hr rate") == 4
        r = calc(it, 16, v102=60, v103=2, v104=12, v105=0)   # load test slide
        return ok and val(r, "Load test") == 180 and val(r, "Must stay") == 9.6

    def t_ri(it):
        r = calc(it, 17)
        ok = close(val(r, "Book way"), 0.5 / 4.5)
        r = calc(it, 17, v107=1.595, v108=1.493, v110=4)      # handout: 0.273 ohm
        i = 1.493 / 4
        return ok and close(val(r, "I = VL/RL"), i) and close(val(r, "RI = VI/I"), 0.102 / i)

    def t_small(it):                                         # 240.4(D) on the chart
        r = calc(it, 10, v66=sz("12"), v67=1, v69=1, v70=30)
        ok = val(r, "Max breaker") == 20
        r = calc(it, 10, v66=sz("10"), v67=2, v69=1, v70=30)
        ok &= val(r, "Max breaker") == 25
        r = calc(it, 10, v66=sz("8"))
        return ok and "Max breaker" not in r

    def t_ohm(it):
        r = calc(it, 18)
        return val(r, "Ohms R") == 8 and val(r, "Watts P") == 72

    # every notes page fits: at most 15 lines, each within the screen width
    def t_pages(it):
        f = font(1)
        bad = []
        n = len(it.g["gLearn"])
        for k in range(1, n + 1):
            h = fn_call(it, "pageLines", k)
            for j, line in enumerate(h):
                if line.startswith("@"):
                    if line != "@":                  # a drawing: "@n" and 5 more lines
                        ok_dg = line[1:].isdigit() and 1 <= int(line[1:]) <= 42 and h[j + 1:j + 6] == ["@"] * 5
                        if not ok_dg:
                            bad.append((k, "drawing", line))
                    continue
                if 6 + f.getlength(line) > 316:
                    bad.append((k, line))
        if bad:
            print("page problems:", bad[:8])
        used = sorted(int(x) for g in it.g["gGrp"] for x in g)
        ok = used == list(range(1, n + 1))          # every page in exactly one notes tile
        if not ok:
            print("pages not grouped once:", used)
        return not bad and n == 69 and ok

    tool_checks = [t_kcl, t_kvl, t_net, t_thev, t_eqv, t_sup, t_wire, t_vd, t_run, t_amp, t_load,
                   t_temp, t_neh, t_bank, t_need, t_cap, t_ri, t_ohm]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))
    assert len(names) == len(tool_checks)

    ev = [shot("rev_home.png"), check("every notes page fits the screen", t_pages),
          check("ampacity: 240.4(D) small-conductor breaker limits", t_small)]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: book answers", fn),
               ("check", reset), -1,
               shot(f"rev_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        # Unit 9 notes: pick page 5 (Thevenin), back to the list, pick 12, leave
        # Unit 9 notes: one long page; arrows, + / -, sections, drag, tap
        *tap(*tile(19)), shot("rev_notes_unit9.png"),
        KEY["down"], KEY["down"], KEY["down"],
        check("Down scrolls a line at a time", lambda it: it.g["gSTop"] == 4),
        KEY["up"],
        check("Up scrolls back", lambda it: it.g["gSTop"] == 3),
        [0, 160, 200], [1, 160, 172], [1, 160, 144], [2], [3, 160, 144],
        check("dragging the text up 56 px scrolls 4 lines (no page jump)", lambda it: it.g["gSTop"] == 7),
        KEY["right"], KEY["right"], KEY["right"], KEY["right"], KEY["right"],
        check("Right jumps to the next section (Thevenin)",
              lambda it: it.g["gSTop"] == sum(len(fn_call(it, "pageLines", k)) + 1 for k in (1, 2, 3, 4, 65)) + 1),
        shot("rev_notes_thevenin.png"),
        KEY["left"],
        check("Left jumps back a section (HW #6)",
              lambda it: it.g["gSTop"] == sum(len(fn_call(it, "pageLines", k)) + 1 for k in range(1, 5)) + 1),
        shot("rev_notes_hw6.png"),
        KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"],
        KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"], KEY["plus"],
        check("+ pages down and stops at the end", lambda it: it.g["gSTop"] > 150),
        shot("rev_notes_review9.png"),
        *tap(160, 60),
        check("tap the top half pages up", lambda it: it.g["gSTop"] > 140),
        *tap(290, 10),
        check("CLOSE returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 19),
        *tap(*tile(20)), KEY["minus"], KEY["right"], KEY["right"], KEY["right"], KEY["right"],
        KEY["right"], KEY["right"], KEY["right"], KEY["right"], KEY["right"], KEY["right"], KEY["right"],
        KEY["right"], shot("rev_notes_voltage_drop.png"), KEY["esc"],
        check("Esc returns to the tiles", lambda it: it.g["gScr"] == 1),
        *tap(*tile(21)), KEY["right"] , *[KEY["right"]] * 16, shot("rev_notes_series_parallel.png"), KEY["enter"],
        *tap(*tile(22)), shot("rev_key_terms.png"), KEY["esc"],
        check("key terms tile", lambda it: it.g["gHome"] == 22),
        *tap(*tile(8)), *tap(*box(5)), ("dialog", 24),
        check("tap a box: amps 24", lambda it: it.g["gV"][55] == 24),
        *tap(300, 10), shot("rev_help_tool.png"), KEY["esc"],
        check("tool HELP closes back to the tool", lambda it: it.g["gScr"] == 2 and it.g["gTool"] == 8),
        *tap(*menu(2)), KEY["esc"],
        KEY["right"], KEY["right"],
        check("arrows on the tiles", lambda it: it.g["gHome"] == 10),
        KEY["help"], shot("rev_help.png"), KEY["enter"],
        -1,
        *tap(295, 10),
    ]
    it = Interp(src, ev)
    try:
        it.start("ELECREV")
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
