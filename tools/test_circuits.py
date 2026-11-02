#!/usr/bin/env python3
"""Simulator tests for hp-prime/CIRCUITS.txt (DC circuits for an
electricity class).

The expected answers come from the class homework (the screenshots the
app was built from) and from the circuit worked out again here with
plain arithmetic, not from the program.  The touch and keypad flow is
played through, and screenshots go to docs/screens/.

Usage
  python3 tools/test_circuits.py              # test hp-prime/CIRCUITS.txt
  python3 tools/test_circuits.py FILE OUTDIR  # test another copy
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 50 + 22


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
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "CIRCUITS.txt")
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

    def text(it):
        return " | ".join(it.g["gRV"])

    def t_fmt(it):
        cases = [(0.0111958, "0.0111958"), (0.31864407, "0.318644"), (0.000503812, "0.000503812"),
                 (5627.105, "5627.11"), (12, "12"), (0.0000012345678, "0.00000123457"),
                 (-0.25, "-0.25"), (0.00000012345, "1.2345E-7")]
        got = [fn_call(it, "fmtE", v) for v, _ in cases]
        if got != [s for _, s in cases]:
            print("fmtE:", got)
        return got == [s for _, s in cases]

    # ---- series: the homework questions --------------------------------
    def t_series(it):
        rs = [10, 20, 30, 40, 50, 40, 50]
        rt = sum(rs)
        r = calc(it, 1)
        ok = close(val(r, "RT"), rt) and close(val(r, "ET"), rt * 1) and close(val(r, "IT"), 1)
        ok &= close(val(r, "E3 P3"), 30) and close(val(r, "E3 P3", 1), 30)
        # four equal resistors on 60 V: each one drops 15 V; 1 A total
        # means 15 W each and 60 W total
        r = calc(it, 1, v1=60, v2=0, v3=15, v4=15, v5=15, v6=15, v7=0, v8=0, v9=0)
        ok &= close(val(r, "IT"), 1) and close(val(r, "PT"), 60) and close(val(r, "E2 P2", 1), 15)
        # 120 V across 2 A: RT = 60 ohms
        r = calc(it, 1, v1=120, v2=2, v3=60, v4=0, v5=0, v6=0, v7=0, v8=0, v9=0)
        return ok and close(val(r, "IT"), 2) and close(val(r, "RT"), 60)

    def t_parallel(it):
        rt = par(470, 360, 510, 430)
        r = calc(it, 2)
        ok = close(val(r, "RT"), rt) and close(val(r, "IT"), 120 / rt)
        ok &= close(val(r, "I2 P2"), 120 / 360) and close(val(r, "I2 P2", 1), 120 ** 2 / 360)
        r = calc(it, 2, v10=0, v11=2, v12=10, v13=10, v14=0, v15=0)
        return ok and close(val(r, "RT"), 5) and close(val(r, "ET"), 10) and close(val(r, "I1 P1"), 1)

    def t_sp(it):
        # Q1 / Q4: (470 + 360) || (510 + 430), IT = 0.6 A
        rt = par(470 + 360, 510 + 430)
        r = calc(it, 3)
        et = 0.6 * rt
        ok = close(val(r, "RT"), rt) and close(rt, 440.79, 0.00002) and close(val(r, "ET"), et)
        ok &= close(val(r, "E2 I2", 1), et / 830) and close(et / 830, 0.31864, 0.00002)
        ok &= close(val(r, "E2 I2"), et / 830 * 360) and close(val(r, "E4 I4"), et / 940 * 430)
        ok &= close(val(r, "Branch B", 1), et / 940)
        # a third branch, and ET given instead of IT
        r = calc(it, 3, v19=24, v20=0, v25=100, v26=20)
        rt3 = par(830, 940, 120)
        return ok and close(val(r, "RT"), rt3) and close(val(r, "IT"), 24 / rt3) and close(val(r, "Branch C", 1), 0.2)

    def t_comb(it):
        # Q6: R1 - (R2 || R3) - R4 - (R5 || R6) - R7 on 63 V
        p1, p2 = par(2200, 1800), par(3300, 4300)
        rt = 1000 + p1 + 910 + p2 + 860
        it_ = 63 / rt
        r = calc(it, 4)
        ok = close(val(r, "RT"), rt) and close(rt, 5627.1, 0.00002) and close(val(r, "IT"), it_)
        ok &= close(val(r, "E1 I1"), it_ * 1000) and close(val(r, "E3 I3"), it_ * p1)
        ok &= close(val(r, "E3 I3", 1), it_ * p1 / 1800) and close(val(r, "E6 I6", 1), it_ * p2 / 4300)
        ok &= close(val(r, "E7 I7"), it_ * 860)
        drops = [val(r, f"E{k} I{k}") for k in (1, 2, 4, 5, 7)]
        return ok and close(sum(drops), 63)

    def t_trb(it):
        # Q10: 12 V, (270 + 510) || (470 + 330); E1 12, E2 0, E3 7, E4 5 V, 15 mA
        r = calc(it, 5)
        ok = r["Answer"][0] == "R1 is OPEN" and r["Match"][0] == "close"
        ok &= close(val(r, "IT normal"), (12 / 780 + 12 / 800) * 1000)
        # R2 shorted: E1 = 12, E2 = 0 too, but the current goes up
        it2 = (12 / 270 + 12 / 800) * 1000
        r = calc(it, 5, v37=it2 / 1000)
        ok &= r["Answer"][0] == "R2 is SHORTED"
        # R4 open: E4 = 12 V, E3 = 0
        r = calc(it, 5, v37=12 / 780, v42=12 * 270 / 780, v43=12 * 510 / 780, v44=0, v45=12)
        ok &= r["Answer"][0] == "R4 is OPEN"
        r = calc(it, 5, v37=0, v42=12 * 270 / 780, v43=12 * 510 / 780, v44=12 * 470 / 800, v45=12 * 330 / 800)
        return ok and r["Answer"][0] == "All resistors OK"

    def t_kvl(it):
        # 120 V, drops of 35, 28, 22 and 15 V: the fifth is 20 V
        r = calc(it, 6)
        ok = val(r, "E5") == 20 and val(r, "Known drops") == 100
        r = calc(it, 6, v46=0, v47=3, v48=5, v49=7, v50=12)
        ok &= val(r, "ET") == 24
        r = calc(it, 6, v47=4, v48=0, v49=40, v50=40, v51=40)
        ok &= val(r, "E1") == 0
        r = calc(it, 6, v46=50, v47=2, v48=0, v49=0)
        return ok and r["Enter"][0] == "one unknown only"

    def t_kcl(it):
        r = calc(it, 7)
        ok = val(r, "Out 2") == 1
        r = calc(it, 7, v85=2, v55=3, v56=0, v59=4, v60=0)
        ok &= val(r, "In 2") == 1
        # negative: the assumed direction was wrong (homework answer C)
        r = calc(it, 7, v85=2, v55=5, v56=0, v59=4, v60=0)
        ok &= val(r, "In 2") == -1 and "Negative" in text(it) and "OUT of the junction, 1 A" in text(it)
        r = calc(it, 7, v85=9, v55=3, v56=2, v59=4, v60=1)
        return ok and val(r, "In - out") == 0

    def t_net(it):
        v = (12 / 4 + 6 / 2) / (1 / 4 + 1 / 2 + 1 / 6)
        r = calc(it, 8)
        ok = close(val(r, "Top node"), v) and close(val(r, "I1"), (12 - v) / 4)
        ok &= close(val(r, "I2"), (6 - v) / 2) and val(r, "I2") < 0 and close(val(r, "I3"), v / 6)
        ok &= "Negative" in text(it)
        # checked by KVL on each loop
        i1, i2, i3 = val(r, "I1"), val(r, "I2"), val(r, "I3")
        ok &= close(i1 * 4 + i3 * 6, 12, 0.0002) and close(i2 * 2 + i3 * 6, 6, 0.0002)
        r = calc(it, 8, v65=2)
        v = (12 / 4 - 6 / 2) / (1 / 4 + 1 / 2 + 1 / 6)
        return ok and abs(val(r, "Top node") - v) < 1e-6

    def t_ohm(it):
        r = calc(it, 9)                     # 48 V at 96 W
        ok = val(r, "Amps I") == 2 and val(r, "Ohms R") == 24
        r = calc(it, 9, v69=0, v70=0.5, v71=100, v72=0)
        ok &= val(r, "Volts E") == 50 and val(r, "Watts P") == 25
        r = calc(it, 9, v69=0, v70=0, v71=8, v72=200)
        return ok and close(val(r, "Volts E"), 40) and close(val(r, "Amps I"), 5)

    def t_div(it):
        r = calc(it, 10)
        return (close(val(r, "E1"), 12 * 470 / 830) and close(val(r, "E2"), 12 * 360 / 830)
                and close(val(r, "I1"), 0.6 * 360 / 830) and close(val(r, "R1 || R2"), par(470, 360)))

    def t_color(it):
        r = calc(it, 11)                    # yellow violet red gold
        ok = r["Value"][0] == "4.7 kΩ" and val(r, "In ohms") == 4700 and r["Tolerance"][0] == "± 5%"
        ok &= r["Lowest"][0] == "4.465 kΩ"
        # brown black black brown brown: 1 kΩ 1%
        r = calc(it, 11, v77=2, v78=2, v79=1, v80=1, v81=2, v82=1)
        ok &= r["Value"][0] == "1 kΩ"
        r = calc(it, 11, v78=2, v79=1, v81=11)   # brown black gold: 1 ohm
        return ok and val(r, "In ohms") == 1

    def t_pre(it):
        r = calc(it, 12)                    # 15 milli
        ok = val(r, "(none)") == 0.015 and val(r, "micro (µ)") == 15000
        r = calc(it, 12, v83=4.7, v84=6)
        return ok and val(r, "(none)") == 4700 and val(r, "mega (M)") == 0.0047

    tool_checks = [t_series, t_parallel, t_sp, t_comb, t_trb, t_kvl, t_kcl, t_net,
                   t_ohm, t_div, t_color, t_pre]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))
    assert len(names) == len(tool_checks)

    ev = [shot("circ_home.png"), check("six significant figures, small currents too", t_fmt)]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset), -1,
               shot(f"circ_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        *tap(*tile(13)), ("dialog", 3),
        shot("circ_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 13),
        # series-parallel: tap the R2 box and enter 390, then type 1.5
        # into R3 straight from the keypad
        *tap(*tile(3)),
        *tap(*box(4)), ("dialog", 390),
        check("tapped R2 and entered 390", lambda it: it.g["gV"][21] == 390 and it.g["gTSel"] == 4),
        KEY["right"], *keys("1.5"), KEY["enter"],
        check("Right moves to R3 and types 1.5", lambda it: it.g["gV"][22] == 1.5 and it.g["gTSel"] == 5),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][21] == 360 and it.g["gV"][22] == 510),
        *tap(300, 10),
        shot("circ_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 4),
        *tap(*menu(3)), *tap(*menu(3)), *tap(*menu(3)), *tap(*menu(3)),
        check("PREV wraps to the last tool", lambda it: it.g["gTool"] == 12),
        KEY["esc"],
        check("Esc goes home on tile 12", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 12),
        KEY["down"],
        check("Down wraps to the top row", lambda it: it.g["gHome"] == 4),
        KEY["up"],
        check("Up wraps to the bottom row", lambda it: it.g["gHome"] == 12),
        KEY["left"], KEY["left"], KEY["left"], KEY["down"],
        check("arrows reach the Learn tile", lambda it: it.g["gHome"] == 13),
        KEY["right"],
        check("Right wraps past Learn to tile 1", lambda it: it.g["gHome"] == 1),
        KEY["help"],
        shot("circ_help.png"),
        KEY["enter"],
        -1,
        *tap(295, 10),
    ]
    it = Interp(src, ev)
    try:
        it.start("CIRCUITS")
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
