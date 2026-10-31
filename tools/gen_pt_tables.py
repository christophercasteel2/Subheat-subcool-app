#!/usr/bin/env python3
"""Generate the saturation (P-T) tables used by the HP Prime program.

The calculator stores, for every refrigerant, the absolute saturation
pressure (psia) at the bubble point (liquid) and dew point (vapor) from
-60 F to 150 F in 5 F steps.  Between rows the program interpolates
linearly in ln(P), which tracks the real curve to within about 0.1 psi.

Data sources (see the header of each CSV for the exact document)
  * pure and pseudo-pure fluids: CoolProp (pip install CoolProp)
  * blends: published tables in tools/data/*.csv (NIST REFPROP based
    manufacturer and distributor charts), resampled to the 5 F grid
  * R-407F, R-417A, R-421A: CoolProp blend model, checked against the
    liquid pressures in tools/data/check/

Usage
  python3 tools/gen_pt_tables.py            # rewrite the data block in the program
  python3 tools/gen_pt_tables.py --check    # also print accuracy checks

To add a refrigerant: add an entry to REFRIGERANTS (a CoolProp name, or a
CSV file in tools/data with columns temp_F,bubble,dew in psia or psig),
then re-run.  The program picks up the new count automatically.
"""
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "SUPERSUB.txt")
DATA = os.path.join(ROOT, "tools", "data")

T_MIN, T_MAX, T_STEP = -60, 150, 5
TEMPS = list(range(T_MIN, T_MAX + 1, T_STEP))
ATM = 14.696          # psia
PA_PER_PSI = 6894.757
MAX_EXTRAP = 20       # F a published table may be extended past its last row
                      # (Clausius-Clapeyron fit: about 0.01 F error over 20 F)
DEFAULT = "R-410A"    # refrigerant selected on first run

# name, data source, cylinder colour (r,g,b), chooser description
REFRIGERANTS = [
    ("R-12",    "coolprop:R12",        (235, 235, 235), "CFC, legacy (Freon 12)"),
    ("R-22",    "coolprop:R22",        (130, 200, 80),  "HCFC, legacy A/C"),
    ("R-32",    "coolprop:R32",        (70, 130, 230),  "HFC, A2L A/C"),
    ("R-134a",  "coolprop:R134a",      (120, 190, 235), "HFC, auto / med temp"),
    ("R-290",   "coolprop:Propane",    (230, 80, 60),   "Propane, A3"),
    ("R-401A",  "csv:R401A.csv",       (235, 130, 120), "MP39, R-12 retrofit"),
    ("R-402A",  "csv:R402A.csv",       (215, 185, 135), "HP80, R-502 retrofit"),
    ("R-404A",  "coolprop:R404A",      (245, 140, 40),  "HFC, low / med temp"),
    ("R-407A",  "csv:R407A.csv",       (160, 210, 60),  "HFC, R-22/R-502 retrofit"),
    ("R-407C",  "coolprop:R407C",      (175, 115, 70),  "HFC, R-22 replacement"),
    ("R-407F",  "coolprop:HEOS::R407F.mix", (90, 170, 200), "Performax LT"),
    ("R-408A",  "csv:R408A.csv",       (150, 110, 200), "FX-10, R-502 retrofit"),
    ("R-409A",  "csv:R409A.csv",       (190, 150, 90),  "FX-56, R-12 retrofit"),
    ("R-410A",  "coolprop:R410A",      (235, 110, 150), "HFC A/C (Puron)"),
    ("R-417A",  "coolprop:HEOS::R417A.mix", (110, 190, 120), "NU-22/MO59, R-22 retro"),
    ("R-421A",  "coolprop:HEOS::R421A.mix", (120, 200, 170), "Choice, R-22 retrofit"),
    ("R-422B",  "csv:R422B.csv",       (180, 200, 90),  "NU-22B, R-22 retrofit"),
    ("R-422D",  "csv:R422D.csv",       (110, 200, 110), "MO29, R-22 retrofit"),
    ("R-427A",  "csv:R427A.csv",       (90, 175, 90),   "FX-100, R-22 retrofit"),
    ("R-438A",  "csv:R438A.csv",       (200, 170, 70),  "MO99, R-22 retrofit"),
    ("R-448A",  "csv:R448A.csv",       (80, 120, 210),  "N40, R-404A replacement"),
    ("R-449A",  "csv:R449A.csv",       (130, 150, 190), "XP40, R-404A replacement"),
    ("R-452A",  "csv:R452A.csv",       (120, 160, 220), "XP44, transport refrig."),
    ("R-454B",  "csv:R454B.csv",       (170, 170, 175), "XL41 / Puron Advance A2L"),
    ("R-500",   "csv:R500.csv",        (240, 210, 70),  "CFC azeotrope, legacy"),
    ("R-502",   "csv:R502.csv",        (200, 150, 210), "CFC azeotrope, legacy"),
    ("R-507A",  "coolprop:R507A",      (60, 175, 165),  "AZ-50, low temp"),
    ("R-513A",  "csv:R513A.csv",       (130, 200, 230), "XP10, R-134a replacement"),
    ("R-600a",  "coolprop:IsoButane",  (225, 110, 90),  "Isobutane, A3"),
    ("R-1234yf", "coolprop:R1234yf",   (240, 240, 245), "HFO, auto A/C"),
]

# CoolProp blend models checked against published liquid pressures
BLEND_CHECKS = {"R-407F": "R407F_bubble.csv", "R-417A": "R417A_bubble.csv",
                "R-421A": "R421A_bubble.csv"}

# ---- properties for the refrigerant info, line set and cylinder tools ----

# saturated liquid density is stored at these temperatures (F)
DENS_T = (0, 40, 80, 120)

# CoolProp fluid used for liquid density; anything not listed (or a point
# CoolProp cannot solve) comes from tools/data/liquid_density.csv
DENSITY_FLUID = {
    "R-12": "R12", "R-22": "R22", "R-32": "R32", "R-134a": "R134a",
    "R-290": "Propane", "R-404A": "R404A", "R-407A": "HEOS::R407A.mix",
    "R-407C": "R407C", "R-407F": "HEOS::R407F.mix", "R-410A": "R410A",
    "R-417A": "HEOS::R417A.mix", "R-421A": "HEOS::R421A.mix",
    "R-422B": "HEOS::R422B.mix", "R-422D": "HEOS::R422D.mix",
    "R-427A": "HEOS::R427A.mix", "R-448A": "HEOS::R448A.mix",
    "R-449A": "HEOS::R449A.mix", "R-452A": "HEOS::R452A.mix",
    "R-454B": "HEOS::R454B.mix", "R-507A": "R507A", "R-513A": "HEOS::R513A.mix",
    "R-600a": "IsoButane", "R-1234yf": "R1234yf",
}

# composition, mass % (ASHRAE 34; matches the Hudson and National charts)
COMPOSITION = {
    "R-12": {"R-12": 100}, "R-22": {"R-22": 100}, "R-32": {"R-32": 100},
    "R-134a": {"R-134a": 100}, "R-290": {"R-290": 100},
    "R-401A": {"R-22": 53, "R-152a": 13, "R-124": 34},
    "R-402A": {"R-125": 60, "R-290": 2, "R-22": 38},
    "R-404A": {"R-125": 44, "R-143a": 52, "R-134a": 4},
    "R-407A": {"R-32": 20, "R-125": 40, "R-134a": 40},
    "R-407C": {"R-32": 23, "R-125": 25, "R-134a": 52},
    "R-407F": {"R-32": 30, "R-125": 30, "R-134a": 40},
    "R-408A": {"R-125": 7, "R-143a": 46, "R-22": 47},
    "R-409A": {"R-22": 60, "R-124": 25, "R-142b": 15},
    "R-410A": {"R-32": 50, "R-125": 50},
    "R-417A": {"R-125": 46.6, "R-134a": 50, "R-600": 3.4},
    "R-421A": {"R-125": 58, "R-134a": 42},
    "R-422B": {"R-125": 55, "R-134a": 42, "R-600a": 3},
    "R-422D": {"R-125": 65.1, "R-134a": 31.5, "R-600a": 3.4},
    "R-427A": {"R-32": 15, "R-125": 25, "R-143a": 10, "R-134a": 50},
    "R-438A": {"R-32": 8.5, "R-125": 45, "R-134a": 44.2, "R-600": 1.7, "R-601a": 0.6},
    "R-448A": {"R-32": 26, "R-125": 26, "R-1234yf": 20, "R-134a": 21, "R-1234ze(E)": 7},
    "R-449A": {"R-32": 24.3, "R-125": 24.7, "R-1234yf": 25.3, "R-134a": 25.7},
    "R-452A": {"R-32": 11, "R-125": 59, "R-1234yf": 30},
    "R-454B": {"R-32": 68.9, "R-1234yf": 31.1},
    "R-500": {"R-12": 73.8, "R-152a": 26.2},
    "R-502": {"R-22": 48.8, "R-115": 51.2},
    "R-507A": {"R-125": 50, "R-143a": 50},
    "R-513A": {"R-1234yf": 56, "R-134a": 44},
    "R-600a": {"R-600a": 100}, "R-1234yf": {"R-1234yf": 100},
}

# 100-year GWP of the components, IPCC AR4 (the values the EPA uses for
# HFC limits); hydrocarbons and HFOs use the EPA SNAP figures
GWP_AR4 = {"R-12": 10900, "R-22": 1810, "R-32": 675, "R-115": 7370,
           "R-124": 609, "R-125": 3500, "R-134a": 1430, "R-142b": 2310,
           "R-143a": 4470, "R-152a": 124, "R-290": 3, "R-600": 4,
           "R-600a": 3, "R-601a": 4, "R-1234yf": 4, "R-1234ze(E)": 6}

# ASHRAE 34 safety class and the usual lubricant
SAFETY = {"R-32": "A2L", "R-454B": "A2L", "R-1234yf": "A2L",
          "R-290": "A3", "R-600a": "A3"}            # everything else A1
OIL = {
    "R-12": "Mineral", "R-22": "Mineral / AB", "R-32": "POE / PVE",
    "R-134a": "POE (PAG auto)", "R-290": "Mineral / POE",
    "R-401A": "AB / MO mix, POE", "R-402A": "AB / POE", "R-404A": "POE",
    "R-407A": "POE", "R-407C": "POE", "R-407F": "POE",
    "R-408A": "AB / MO mix, POE", "R-409A": "AB / MO mix, POE",
    "R-410A": "POE / PVE", "R-417A": "MO / AB / POE", "R-421A": "MO / POE",
    "R-422B": "MO / AB / POE", "R-422D": "MO / AB / POE", "R-427A": "POE",
    "R-438A": "MO / AB / POE", "R-448A": "POE", "R-449A": "POE",
    "R-452A": "POE", "R-454B": "POE", "R-500": "Mineral",
    "R-502": "Mineral / AB", "R-507A": "POE", "R-513A": "POE",
    "R-600a": "Mineral", "R-1234yf": "PAG (auto) / POE",
}


def f_to_k(t):
    return (t - 32) * 5 / 9 + 273.15


def sat_psia(fluid, k, q):
    """Saturation pressure, or None.  The blend flash occasionally fails to
    converge at one exact temperature, so first fall back to the mean of
    two points a few millikelvin either side."""
    import CoolProp.CoolProp as CP
    try:
        return CP.PropsSI("P", "T", k, "Q", q, fluid) / PA_PER_PSI
    except ValueError:
        for dk in (0.002, 0.005, 0.02):
            try:
                lo = CP.PropsSI("P", "T", k - dk, "Q", q, fluid)
                hi = CP.PropsSI("P", "T", k + dk, "Q", q, fluid)
                return (lo + hi) / 2 / PA_PER_PSI
            except ValueError:
                pass
        return None


def polyfit(xs, ys, deg):
    """Least-squares polynomial, coefficients lowest order first."""
    n = deg + 1
    a = [[sum(x ** (i + j) for x in xs) for j in range(n)] for i in range(n)]
    b = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p], b[c], b[p] = a[p], a[c], b[p], b[c]
        for r in range(n):
            if r != c:
                f = a[r][c] / a[c][c]
                a[r] = [u - f * v for u, v in zip(a[r], a[c])]
                b[r] -= f * b[c]
    return [b[i] / a[i][i] for i in range(n)]


def resample(points, name):
    """points: {temp_F: psia}.  Returns psia on the TEMPS grid.  Inside the
    data, 4-point Lagrange interpolation of ln(P) against T; past either end
    (at most MAX_EXTRAP F), a quadratic fit of ln(P) against 1/T over the
    last five rows, the Clausius-Clapeyron form of the vapour pressure curve."""
    ts = sorted(points)
    out = []
    for t in TEMPS:
        if t in points:
            out.append(points[t])
            continue
        if ts[0] < t < ts[-1]:
            j = next(i for i, x in enumerate(ts) if x > t)
            lo = max(0, min(len(ts) - 4, j - 2))
            xs = ts[lo:lo + 4]
            lp = 0.0
            for a in xs:
                w = 1.0
                for b in xs:
                    if b != a:
                        w *= (t - b) / (a - b)
                lp += w * math.log(points[a])
            out.append(math.exp(lp))
            continue
        if t < ts[0] - MAX_EXTRAP or t > ts[-1] + MAX_EXTRAP:
            sys.exit(f"{name}: table does not reach {t} F")
        end = ts[:5] if t < ts[0] else ts[-5:]
        c = polyfit([1000 / f_to_k(x) for x in end], [math.log(points[x]) for x in end], 2)
        u = 1000 / f_to_k(t)
        out.append(math.exp(c[0] + c[1] * u + c[2] * u * u))
    return out


def coolprop_table(fluid, name):
    out = []
    for q in (0, 1):
        pts = {}
        for t in TEMPS:
            p = sat_psia(fluid, f_to_k(t), q)
            if p is not None:
                pts[t] = p
        if len(pts) < len(TEMPS) - 6:
            sys.exit(f"{name}: too many failed CoolProp points")
        out.append(resample(pts, name))   # rebuilds any points that failed
    return tuple(out)


def read_csv(fname):
    unit, rows = None, []
    with open(os.path.join(DATA, fname)) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("# temp_F"):
                unit = line.rsplit("_", 1)[1]
            if not line or line.startswith("#"):
                continue
            rows.append([float(x) for x in line.split(",")])
    if unit not in ("psia", "psig"):
        sys.exit(f"{fname}: header must end in _psia or _psig")
    off = ATM if unit == "psig" else 0.0
    return [[r[0]] + [v + off for v in r[1:]] for r in rows]


def csv_table(fname, name):
    rows = read_csv(fname)
    bub = resample({r[0]: r[1] for r in rows}, name)
    dew = resample({r[0]: r[2] for r in rows}, name)
    return bub, dew


def load(name, src):
    kind, rest = src.split(":", 1)
    if kind == "coolprop":
        return coolprop_table(rest, name)
    return csv_table(rest, name)


def gwp_ar4(name):
    comp = COMPOSITION[name]
    if abs(sum(comp.values()) - 100) > 0.01:
        sys.exit(f"{name}: composition does not add up to 100 %")
    return int(sum(pct / 100 * GWP_AR4[c] for c, pct in comp.items()) + 0.5)


def density_tables():
    """{name: [lb/ft^3 at each DENS_T]} for every refrigerant."""
    import CoolProp.CoolProp as CP
    csv = {}
    with open(os.path.join(DATA, "liquid_density.csv")) as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                f = line.strip().split(",")
                csv[f[0]] = [float(x) for x in f[1:5]]
    out = {}
    for name, _, _, _ in REFRIGERANTS:
        vals = []
        for i, t in enumerate(DENS_T):
            v = None
            if name in DENSITY_FLUID:
                try:
                    v = CP.PropsSI("D", "T", f_to_k(t), "Q", 0, DENSITY_FLUID[name]) * 0.0624280
                except ValueError:
                    v = None
            if v is None:
                if name not in csv:
                    sys.exit(f"{name}: no liquid density at {t} F")
                v = csv[name][i]
            vals.append(v)
        if any(b >= a for a, b in zip(vals, vals[1:])):
            sys.exit(f"{name}: liquid density should fall with temperature")
        out[name] = vals
    return out


def ppl_matrix(rows):
    """Pressures in hundredths of a psi as whole numbers, which keeps the
    calculator file small; the program divides by 100."""
    body = ",\n".join(
        "[" + ",".join(str(round(v * 100)) for v in r) + "]" for r in rows)
    return "[" + body + "]"


def dark(rgb):
    """Darker shade of a cylinder colour, readable on the white dial face."""
    r, g, b = rgb
    f = min(0.6, 95 / (0.3 * r + 0.59 * g + 0.11 * b))
    return int(r * f), int(g * f), int(b * f)


def build_block(tables):
    dens = density_tables()
    names = ",".join(f'"{n}"' for n, _, _, _ in REFRIGERANTS)
    descs = ",".join(f'"{n}  {d}"' for n, _, _, d in REFRIGERANTS)
    colors = ",".join("RGB({},{},{})".format(*c) for _, _, c, _ in REFRIGERANTS)
    darks = ",".join("RGB({},{},{})".format(*dark(c)) for _, _, c, _ in REFRIGERANTS)
    default = [n for n, _, _, _ in REFRIGERANTS].index(DEFAULT) + 1
    out = [
        "// ---- BEGIN PT DATA (generated by tools/gen_pt_tables.py) ----",
        f"// saturation pressure in psia x 100, {T_MIN}..{T_MAX} F every {T_STEP} F",
        f"gTmin:={T_MIN}; gTstep:={T_STEP}; gNpt:={len(TEMPS)};",
        f"gNref:={len(REFRIGERANTS)}; gDefRef:={default};",
        f"gRName:={{{names}}};",
        f"gRDesc:={{{descs}}};",
        f"gRCol:={{{colors}}};",
        f"gRDk:={{{darks}}};",
        "// bubble point (liquid line / subcooling)",
        "gBub:=" + ppl_matrix([b for b, _ in tables]) + ";",
        "// dew point (suction line / superheat)",
        "gDew:=" + ppl_matrix([d for _, d in tables]) + ";",
        f"// saturated liquid density, lb/ft3 x 100, at {', '.join(map(str, DENS_T))} F",
        "gDen:=" + ppl_matrix([dens[n] for n, _, _, _ in REFRIGERANTS]) + ";",
        "// ASHRAE 34 safety class, usual oil, GWP (IPCC AR4, from composition)",
        "gRSafe:={" + ",".join(f'"{SAFETY.get(n, "A1")}"' for n, _, _, _ in REFRIGERANTS) + "};",
        "gROil:={" + ",".join(f'"{OIL[n]}"' for n, _, _, _ in REFRIGERANTS) + "};",
        "gRGwp:={" + ",".join(str(gwp_ar4(n)) for n, _, _, _ in REFRIGERANTS) + "};",
        "// ---- END PT DATA ----",
    ]
    return "\n".join(out)


def interp(table, t):
    """Same ln(P) interpolation the calculator uses."""
    x = (t - T_MIN) / T_STEP
    k = min(max(int(math.floor(x)), 0), len(TEMPS) - 2)
    f = x - k
    return math.exp(math.log(table[k]) * (1 - f) + math.log(table[k + 1]) * f)


def check(tables):
    by_name = dict(zip([n for n, _, _, _ in REFRIGERANTS], tables))
    print("Calculator interpolation vs CoolProp, worst error at 0.5 F steps (psi):")
    for name, src, _, _ in REFRIGERANTS:
        if not src.startswith("coolprop:"):
            continue
        fluid = src.split(":", 1)[1]
        bub, dew = by_name[name]
        worst = 0.0
        t = T_MIN
        while t <= T_MAX:
            for q, tab in ((0, bub), (1, dew)):
                ref = sat_psia(fluid, f_to_k(t), q)
                if ref is not None:
                    worst = max(worst, abs(interp(tab, t) - ref))
            t += 0.5
        print(f"  {name:8s} {worst:.3f}")
    print("CoolProp blend models vs published liquid pressures (psi):")
    for name, fname in BLEND_CHECKS.items():
        bub = by_name[name][0]
        worst = max(abs(interp(bub, r[0]) - r[1])
                    for r in read_csv("check/" + fname) if T_MIN <= r[0] <= T_MAX)
        print(f"  {name:8s} {worst:.2f}")
    print("Saturation at 40 F, psig (bubble / dew):")
    i = TEMPS.index(40)
    for name, _, _, _ in REFRIGERANTS:
        bub, dew = by_name[name]
        print(f"  {name:8s} {bub[i] - ATM:6.1f} / {dew[i] - ATM:6.1f}")


def main():
    tables = [load(name, src) for name, src, _, _ in REFRIGERANTS]
    for (name, _, _, _), (bub, dew) in zip(REFRIGERANTS, tables):
        for tab in (bub, dew):
            if any(b <= a for a, b in zip(tab, tab[1:])):
                sys.exit(f"{name}: table is not increasing")
        if any(d > b * 1.001 for b, d in zip(bub, dew)):
            sys.exit(f"{name}: dew pressure above bubble pressure")
    block = build_block(tables)
    with open(PROGRAM, encoding="utf-8") as fh:
        src = fh.read()
    pat = re.compile(r"// ---- BEGIN PT DATA.*?// ---- END PT DATA ----", re.S)
    if not pat.search(src):
        sys.exit("data markers not found in " + PROGRAM)
    src = pat.sub(lambda _: block, src)
    with open(PROGRAM, "w", encoding="utf-8") as fh:
        fh.write(src)
    print(f"wrote {len(REFRIGERANTS)} refrigerants x {len(TEMPS)} points to {PROGRAM}")
    if "--check" in sys.argv:
        check(tables)


if __name__ == "__main__":
    main()
