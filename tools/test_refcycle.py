#!/usr/bin/env python3
"""Simulator tests for hp-prime/REFCYCLE.txt (refrigeration cycle and
service records).

Refrigerant properties and whole cycles are checked against CoolProp
called directly (not the program's tables); the EPA tools against the
rules typed from 40 CFR 82.156, 82.157, 84.102 and 84.106; the service
tools against arithmetic done here.  The touch and keypad flow is played
through, and screenshots go to docs/screens/.

Usage
  python3 tools/test_refcycle.py              # test hp-prime/REFCYCLE.txt
  python3 tools/test_refcycle.py FILE OUTDIR  # test another copy
"""
import math
import os
import random
import re
import sys

import CoolProp.CoolProp as CP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import KEY, Interp, ReturnSignal, StopSim, approx, rows, tap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIGIT = {"0": 47, "1": 42, "2": 43, "3": 44, "4": 37, "5": 38, "6": 39,
         "7": 32, "8": 33, "9": 34, ".": 48}
FLUIDS = {"R-22": "R22", "R-410A": "R410A", "R-134a": "R134a", "R-404A": "R404A",
          "R-407C": "R407C", "R-32": "R32", "R-507A": "R507A", "R-290": "Propane", "R-12": "R12"}
NAMES = list(FLUIDS)
PSI = 6894.757


def K(t):
    return (t - 32) / 1.8 + 273.15


class Ref:
    """CoolProp in I-P units with the ASHRAE reference (h, s = 0 for
    saturated liquid at -40 F)"""

    def __init__(self, name):
        self.f = FLUIDS[name]
        self.h0 = CP.PropsSI("H", "T", K(-40), "Q", 0, self.f)
        self.s0 = CP.PropsSI("S", "T", K(-40), "Q", 0, self.f)

    def psat(self, t, q):
        return CP.PropsSI("P", "T", K(t), "Q", q, self.f) / PSI

    def tsat(self, p, q):
        return (CP.PropsSI("T", "P", p * PSI, "Q", q, self.f) - 273.15) * 1.8 + 32

    def h(self, **kw):
        return (CP.PropsSI("H", *self.args(kw), self.f) - self.h0) / 2326

    def s(self, **kw):
        return (CP.PropsSI("S", *self.args(kw), self.f) - self.s0) / 4186.8

    def v(self, **kw):
        return 1 / CP.PropsSI("D", *self.args(kw), self.f) / 0.0624279606

    def args(self, kw):
        out = []
        for k, v in kw.items():
            if k == "t":
                out += ["T", K(v)]
            elif k == "p":
                out += ["P", v * PSI]
            elif k == "q":
                out += ["Q", v]
            elif k == "s":
                out += ["S", v * 4186.8 + self.s0]
            elif k == "h":
                out += ["H", v * 2326 + self.h0]
        return out

    def cycle(self, te, tc, sh, sc, eff=1.0):
        pe, pc = self.psat(te, 1), self.psat(tc, 1)
        h1 = self.h(t=te + sh, p=pe) if sh > 0 else self.h(t=te, q=1)
        s1 = self.s(t=te + sh, p=pe) if sh > 0 else self.s(t=te, q=1)
        v1 = self.v(t=te + sh, p=pe) if sh > 0 else self.v(t=te, q=1)
        h2 = h1 + (self.h(p=pc, s=s1) - h1) / eff
        t2 = (CP.PropsSI("T", "P", pc * PSI, "H", h2 * 2326 + self.h0, self.f) - 273.15) * 1.8 + 32
        t3 = self.tsat(pc, 0) - sc
        h3 = self.h(t=t3, q=0)
        return dict(pe=pe, pc=pc, h1=h1, v1=v1, h2=h2, t2=t2, h3=h3, t3=t3)


def tile(k):
    return ((k - 1) % 4) * 80 + 40, 23 + ((k - 1) // 4) * 43 + 20


def box(k):
    return ((k - 1) % 2) * 160 + 115, 24 + ((k - 1) // 2) * 20 + 8


def menu(k):
    return (k - 1) * 64 + 30, 230


def keys(text):
    return [DIGIT[ch] for ch in text]


def num(text):
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", text)
    return float(m.group().replace(",", ""))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "REFCYCLE.txt")
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

    def ri(name):
        return NAMES.index(name) + 1

    def t_props(it):
        # saturation pressures, liquid and vapor enthalpy, superheated h, s, v
        # at random states of every refrigerant, against CoolProp
        random.seed(7)
        worst = {"p": 0, "h": 0, "s": 0, "v": 0}
        for name in NAMES:
            ref, r = Ref(name), ri(name)
            for _ in range(12):
                t = random.uniform(-40, 140)
                sh = random.uniform(0, 200)
                worst["p"] = max(worst["p"], abs(fn_call(it, "satP", r, t, 1) - ref.psat(t, 0)),
                                 abs(fn_call(it, "satP", r, t, 2) - ref.psat(t, 1)))
                worst["h"] = max(worst["h"], abs(fn_call(it, "satP", r, t, 3) - ref.h(t=t, q=0)))
                pd = ref.psat(t, 1)
                worst["h"] = max(worst["h"], abs(fn_call(it, "vapP", r, t, sh, 2) - ref.h(t=t + sh, p=pd)))
                worst["s"] = max(worst["s"], abs(fn_call(it, "vapP", r, t, sh, 3) - ref.s(t=t + sh, p=pd)))
                worst["v"] = max(worst["v"], abs(fn_call(it, "vapP", r, t, sh, 4) / ref.v(t=t + sh, p=pd) - 1))
        print("worst property errors vs CoolProp:", {k: round(v, 5) for k, v in worst.items()})
        return worst["p"] < 0.05 and worst["h"] < 0.06 and worst["s"] < 0.0001 and worst["v"] < 0.002

    def t_cycle(it):
        # whole cycles against CoolProp: (refrigerant, evap, cond, SH, SC, efficiency %)
        cases = [("R-410A", 40, 110, 10, 10, 100), ("R-22", 40, 120, 15, 8, 100),
                 ("R-134a", 20, 110, 10, 5, 100), ("R-404A", -20, 100, 20, 10, 70),
                 ("R-407C", 45, 115, 12, 10, 100), ("R-32", 45, 105, 8, 12, 80),
                 ("R-12", 5, 86, 0, 0, 100), ("R-290", 30, 100, 10, 10, 100),
                 ("R-507A", -10, 95, 25, 5, 100)]
        bad = []
        for name, te, tc, sh, sc, eff in cases:
            x = Ref(name).cycle(te, tc, sh, sc, eff / 100)
            calc(it, 1, v1=ri(name), v2=1, v3=te, v4=tc, v5=sh, v6=sc, v7=eff)
            cy = it.g["gCy"]
            got = dict(h1=cy[4], v1=cy[6], h2=cy[7], t2=cy[8], h3=cy[9], t3=cy[10])
            tol = dict(h1=0.03, v1=0.002 * x["v1"], h2=0.06, t2=0.3, h3=0.03, t3=0.05)
            for k, tl in tol.items():
                if abs(got[k] - x[k]) > tl:
                    bad.append((name, k, round(got[k], 3), round(x[k], 3)))
        if bad:
            print("cycle mismatches:", bad)
        return not bad

    def t_perf(it):
        # R-410A 40/110 F, 10/10: RE, HOC, COP and flow from CoolProp
        x = Ref("R-410A").cycle(40, 110, 10, 10)
        re_, hoc = x["h1"] - x["h3"], x["h2"] - x["h1"]
        r = calc(it, 2)
        ok = approx(val(r, "Refrig. effect"), re_, 0.03) and approx(val(r, "Heat of comp."), hoc, 0.03)
        ok &= approx(val(r, "COP"), re_ / hoc, 0.011) and approx(val(r, "Mass flow"), 200 / re_, 0.002)
        ok &= approx(val(r, "Comp. ratio"), x["pc"] / x["pe"], 0.011)
        # gauge pressures give the same cycle: 118.4 psig suction, 365.4 head
        r2 = calc(it, 2, v2=2, v3=x["pe"] - 14.696, v4=x["pc"] - 14.696)
        return ok and approx(val(r2, "Refrig. effect"), re_, 0.03)

    def t_mode(it):
        # flipping the boxes to psig and back keeps the temperatures
        reset(it)
        fn_call(it, "setSlot", 2, 2)
        p3 = it.g["gV"][2]
        fn_call(it, "setSlot", 2, 1)
        return approx(p3, Ref("R-410A").psat(40, 1) - 14.696, 0.06) and approx(it.g["gV"][2], 40, 0.06)

    def t_sat(it):
        ref = Ref("R-407C")
        r = calc(it, 3, v9=ri("R-407C"), v10=40)
        glide = ref.tsat(ref.psat(40, 0), 1) - 40
        return (approx(val(r, "Liquid psig"), ref.psat(40, 0) - 14.696, 0.06)
                and approx(val(r, "Glide"), glide, 0.06)
                and approx(val(r, "hg - hf"), ref.h(t=40, q=1) - ref.h(t=40, q=0), 0.02))

    def t_super(it):
        ref = Ref("R-22")
        r = calc(it, 4, v11=ri("R-22"), v12=20, v13=55)
        p = ref.psat(20, 1)
        return (approx(val(r, "Enthalpy"), ref.h(t=75, p=p), 0.011)
                and approx(val(r, "Volume"), ref.v(t=75, p=p), 0.0002))

    def t_flow(it):
        r = calc(it, 5)
        return val(r, "Capacity") == 12600 and approx(val(r, "Flow needed"), 200 / 70, 0.0006)

    def t_disp(it):
        r = calc(it, 6)
        disp = math.pi / 4 * 2 ** 2 * 1.5 * 2 * 1750 / 1728
        x = Ref("R-410A").cycle(40, 110, 10, 10)
        fl = disp * 0.85 / x["v1"]
        return (approx(val(r, "Displacement"), disp, 0.006)
                and abs(val(r, "Capacity") / (fl * (x["h1"] - x["h3"]) * 60) - 1) < 0.002)

    def t_ve(it):
        r = calc(it, 7)
        cr = (365 + 14.696) / (118 + 14.696)
        return approx(val(r, "Vol. eff."), 100 * (1 - 0.05 * (cr ** (1 / 1.15) - 1)), 0.06)

    def t_rate(it):
        r = calc(it, 8, v26=3.5, v27=2)
        return approx(val(r, "EER"), 3.5 * 3.41214, 0.006) and approx(val(r, "kW per ton"), 12 / (3.5 * 3.41214), 0.0006)

    def t_water(it):
        # tower: 95 F in, 85 F out, 78 F wet bulb: range 10, approach 7
        r = calc(it, 9, v29=95, v30=85, v32=78)
        return val(r, "Load") == 120000 and val(r, "Range") == 10 and val(r, "Approach") == 7

    def t_wall(it):
        r = calc(it, 10)
        a = 2 * (80 + 80 + 64)
        return val(r, "Surface") == a and val(r, "Heat gain") == round(a / 32 * 55)

    def t_prod(it):
        # 1,000 lb of water from 70 F to 0 F: 38,000 + 144,000 + 16,000 Btu
        r = calc(it, 11, v41=0)
        return (val(r, "Above freezing") == 38000 and val(r, "Freezing") == 144000
                and val(r, "Below freezing") == 16000 and val(r, "Total") == 198000)

    def t_box(it):
        r = calc(it, 12)
        return val(r, "Equipment") == round(82500 / 16)

    def t_leak(it):
        # annualizing: 8 lb into 60 lb, 365 days: 13.3% > 10% comfort cooling
        r = calc(it, 13)
        ok = val(r, "Leak rate") == 13.3 and r["Over limit"][0] == "repair"
        # 90 days: 8/60 x 365/90 = 54.1%, commercial refrigeration limit 20%
        r = calc(it, 13, v53=2, v58=90)
        ok &= val(r, "Leak rate") == round(8 / 60 * 365 / 90 * 100, 1) and val(r, "Limit") == 20
        # residential A/C is excluded from the HFC rule; HCFC under 50 lb too
        r = calc(it, 13, v53=5)
        ok &= r["Rule"][0] == "does not apply"
        r = calc(it, 13, v54=2, v55=40)
        ok &= r["Rule"][0] == "does not apply"
        # rolling average, 80 lb added to a 60 lb system: chronic leaker
        r = calc(it, 13, v56=80, v57=2)
        return ok and r["Chronic"][0] == "report" and val(r, "Leak rate") == round(80 / 60 * 100, 1)

    def t_evac(it):
        names = fn_call(it, "choiceList", 7)
        r = calc(it, 14)
        ok = r["Evacuate to"][0] == "0 in Hg vac."
        r = calc(it, 14, v59=names.index("R-22") + 1, v60=250)
        ok &= r["Evacuate to"][0] == "10 in Hg vac."
        r = calc(it, 14, v59=names.index("R-134a") + 1, v60=250)
        ok &= r["Evacuate to"][0] == "15 in Hg vac." and r["Class"][0] == "medium-pressure"
        r = calc(it, 14, v59=names.index("R-134a") + 1, v61=2)
        ok &= r["Evacuate to"][0] == "4 in Hg vac."
        r = calc(it, 14, v59=names.index("R-123") + 1)
        ok &= r["Evacuate to"][0] == "25 mm Hg abs."
        r = calc(it, 14, v59=names.index("R-32") + 1, v60=500)
        ok &= r["Class"][0] == "very high-pressure" and r["Evacuate to"][0] == "0 in Hg vac."
        r = calc(it, 14, v62=3)
        return ok and r["Small appl."][0] == "recover 80%"

    def t_charge(it):
        r = calc(it, 15, v65=10, v66=11.25)
        return r["Added"][1] == "3 lb 8.0 oz" and val(r, "Recovered") == 1.25 and val(r, "Net") == 2.25

    def t_inv(it):
        r = calc(it, 16, v74=9.5)
        tax = (180 + 90) * 0.095
        return val(r, "Subtotal") == 491.5 and val(r, "Tax") == round(tax, 2) and val(r, "Total") == round(491.5 + tax, 2)

    def t_mark(it):
        r = calc(it, 17, v76=0, v77=40)
        return approx(val(r, "Price"), 100 / 0.6, 0.006) and approx(val(r, "Markup"), 66.7, 0.051)

    def t_time(it):
        r = calc(it, 18)
        return r["Worked"][0] == "8 h 45 min" and val(r, "Overtime") == 0.75 and val(r, "Pay") == round(8 * 22 + 0.75 * 33, 2)

    def t_conv(it):
        r = calc(it, 19, v85=4, v86=1, v87=2)
        ok = val(r, "Btu/h") == 12000 and approx(val(r, "kW"), 3.51685, 0.0001)
        r = calc(it, 19, v85=6, v86=60, v87=2)
        return ok and approx(val(r, "lb/min"), 1, 1e-6)

    tool_checks = [t_cycle, t_perf, t_sat, t_super, t_flow, t_disp, t_ve, t_rate, t_water, t_wall,
                   t_prod, t_box, t_leak, t_evac, t_charge, t_inv, t_mark, t_time, t_conv]
    names = re.findall(r'"([^"]*)"', re.search(r"gTName:=\{(.*?)\};", src).group(1))

    ev = [shot("cycle_home.png"), check("properties of all 9 refrigerants vs CoolProp", t_props),
          check("temperature / psig boxes convert both ways", t_mode)]
    for k, fn in enumerate(tool_checks, 1):
        slug = re.sub(r"[^a-z0-9]+", "_", names[k - 1].lower()).strip("_")
        ev += [*tap(*tile(k)),
               check(f"tile {k} opens {names[k - 1]}", lambda it, k=k: it.g["gScr"] == 2 and it.g["gTool"] == k),
               check(f"{names[k - 1]}: results", fn),
               ("check", reset), -1,
               shot(f"cycle_{k}_{slug}.png"),
               *tap(*menu(5))]
    ev += [
        *tap(*tile(20)), ("dialog", 6),
        shot("cycle_learn.png"),
        KEY["enter"],
        check("Learn returns to the tiles", lambda it: it.g["gScr"] == 1 and it.g["gHome"] == 20),
        # cycle: switch to gauge pressures, type the suction pressure
        *tap(*tile(1)),
        *tap(*box(2)),
        check("Enter as flips to psig", lambda it: it.g["gV"][1] == 2 and approx(it.g["gV"][2], 118.4, 0.06)),
        KEY["right"], *keys("130"), KEY["enter"],
        check("typed the suction psig", lambda it: it.g["gV"][2] == 130),
        shot("cycle_psig.png"),
        *tap(*menu(2)),
        check("RESET", lambda it: it.g["gV"][1] == 1 and it.g["gV"][2] == 40),
        *tap(300, 10),
        shot("cycle_help_tool.png"),
        *tap(160, 120),
        *tap(*menu(4)),
        check("NEXT", lambda it: it.g["gTool"] == 2),
        KEY["esc"],
        KEY["right"], KEY["down"],
        check("arrows move on the 4 x 5 grid", lambda it: it.g["gHome"] == 7),
        KEY["help"],
        shot("cycle_help.png"),
        KEY["enter"],
        -1,
        *tap(295, 10),
    ]
    it = Interp(src, ev)
    try:
        it.start("REFCYCLE")
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
