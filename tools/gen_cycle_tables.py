#!/usr/bin/env python3
"""Write the generated block of hp-prime/REFCYCLE.txt: the tool list, the
input-box ("slot") tables and the refrigerant property tables of the
refrigeration cycle and service calculator.

    python3 tools/gen_cycle_tables.py            # needs CoolProp

Refrigerant properties (CoolProp, the same reference-quality equations of
state as NIST REFPROP for these fluids), in I-P units with the ASHRAE
reference state: enthalpy and entropy are 0 for saturated liquid at -40 F.
Grid: saturation temperature -40 ... 140 F every 5 F; superheat 0 ... 200 F
every 10 F at the dew-point pressure.  The program interpolates with
quadratics in both directions (log of specific volume), which stays within
about 0.01 Btu/lb of CoolProp at normal suction and discharge states (0.05
Btu/lb next to the critical point).

Codes and rules typed from their source:
  EPA leak repair, 40 CFR 84.106 (HFC appliances of 15 lb or more, from
  January 1, 2026) and 40 CFR 82.157 (CFC/HCFC appliances of 50 lb or more);
  leak rate methods, 40 CFR 84.102; evacuation levels, 40 CFR 82.156
  Table 1, with the appliance pressure classes of 40 CFR 82.152.
"""
import math
import os

import CoolProp.CoolProp as CP

from ppltables import (check_slots, choice_slot, plist, pmatrix, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "REFCYCLE.txt")

# name, CoolProp fluid
REFRIGERANTS = [("R-22", "R22"), ("R-410A", "R410A"), ("R-134a", "R134a"), ("R-404A", "R404A"),
                ("R-407C", "R407C"), ("R-32", "R32"), ("R-507A", "R507A"), ("R-290", "Propane"),
                ("R-12", "R12")]
DEFAULT_REF = 2      # R-410A
T_GRID = list(range(-40, 141, 5))
SH_GRID = list(range(0, 201, 10))
PSI = 6894.757
BTU_LB = 2326.0          # J/kg per Btu/lb
BTU_LBR = 4186.8         # J/kg-K per Btu/lb-R
FT3_LB = 0.0624279606    # m3/kg -> ft3/lb divides by this


def F2K(t):
    return (t - 32) / 1.8 + 273.15


def props(fluid):
    """saturation rows (bubble psia, dew psia, bubble liquid h) and the
    superheated grid (h, s, v) at each dew pressure, ASHRAE reference"""
    h0 = CP.PropsSI("H", "T", F2K(-40), "Q", 0, fluid)
    s0 = CP.PropsSI("S", "T", F2K(-40), "Q", 0, fluid)
    sat, H, S, V = [], [], [], []
    for t in T_GRID:
        pb = CP.PropsSI("P", "T", F2K(t), "Q", 0, fluid)
        pd = CP.PropsSI("P", "T", F2K(t), "Q", 1, fluid)
        hf = CP.PropsSI("H", "T", F2K(t), "Q", 0, fluid)
        sat.append([pb / PSI, pd / PSI, (hf - h0) / BTU_LB])
        hr, sr, vr = [], [], []
        for sh in SH_GRID:
            if sh == 0:
                h = CP.PropsSI("H", "T", F2K(t), "Q", 1, fluid)
                s = CP.PropsSI("S", "T", F2K(t), "Q", 1, fluid)
                d = CP.PropsSI("D", "T", F2K(t), "Q", 1, fluid)
            else:
                h = CP.PropsSI("H", "T", F2K(t + sh), "P", pd, fluid)
                s = CP.PropsSI("S", "T", F2K(t + sh), "P", pd, fluid)
                d = CP.PropsSI("D", "T", F2K(t + sh), "P", pd, fluid)
            hr.append((h - h0) / BTU_LB)
            sr.append((s - s0) / BTU_LBR)
            vr.append(1 / d / FT3_LB)
        H.append(hr)
        S.append(sr)
        V.append(vr)
    p104 = CP.PropsSI("P", "T", F2K(104), "Q", 0, fluid) / PSI
    return sat, H, S, V, p104


def epa_class(p104):
    """40 CFR 82.152 appliance class from the liquid saturation pressure at 104 F"""
    if p104 < 45:
        return 1      # low
    if p104 < 170:
        return 2      # medium
    if p104 <= 355:
        return 3      # high
    return 4          # very high


# other refrigerants named as examples in the 40 CFR 82.152 definitions
EPA_EXAMPLES = [("R-11", 1), ("R-123", 1), ("R-113", 1), ("R-245fa", 1), ("R-114", 2),
                ("R-124", 2), ("R-500", 2), ("R-407A", 3), ("R-502", 3), ("R-13", 4),
                ("R-23", 4), ("R-503", 4), ("R-508B", 4)]

DATA = {name: props(fluid) for name, fluid in REFRIGERANTS}

CONV_UNITS_MAX = 6
UNITS = 12

CHOICES = {
    1: [n for n, _ in REFRIGERANTS],
    2: ["Sat temps °F", "Gauge psig"],
    3: ["EER", "COP", "kW per ton"],
    4: ["Comfort cooling", "Commercial refrig.", "Industrial process", "Other / transport",
        "Res./light comm. AC"],
    5: ["HFC / HFO", "CFC / HCFC"],
    6: ["Annualizing", "Rolling average"],
    7: [n for n, _ in REFRIGERANTS] + [n for n, _ in EPA_EXAMPLES],
    8: ["1993 or later", "Before 1993"],
    9: ["No", "Yes, runs", "Yes, dead"],
    11: ["Enthalpy", "Entropy / cp", "Volume", "Capacity", "Pressure", "Mass flow"],
}

S = slot
C = choice_slot(CHOICES, UNITS, CONV_UNITS_MAX)

SLOTS = [
    # refrigeration cycle (tools 1 and 2)
    C(1, "Refrigerant", 1, DEFAULT_REF, "Refrigerant in the system"),
    C(2, "Enter as", 2, 1, "Saturation temperatures or gauge pressures"),
    S(3, "Evaporator", "", 1, 1, -60, 700, 40, "Evaporating (dew) temp, or suction psig"),
    S(4, "Condenser", "", 1, 1, -60, 900, 110, "Condensing (dew) temp, or head psig"),
    S(5, "Superheat", "°F", 1, 1, 0, 150, 10, "Superheat at the compressor inlet"),
    S(6, "Subcooling", "°F", 1, 1, 0, 60, 10, "Subcooling at the metering device"),
    S(7, "Comp. eff.", "%", 0, 5, 30, 100, 100, "Isentropic efficiency (100 = ideal)"),
    S(8, "Capacity", "tons", 1, 0.5, 0.1, 10000, 1, "Cooling capacity to size the flow for"),
    # saturated properties
    C(9, "Refrigerant", 1, DEFAULT_REF, "Refrigerant"),
    S(10, "Sat temp", "°F", 1, 1, -40, 140, 40, "Saturation temperature, -40 to 140 °F"),
    # superheated vapor
    C(11, "Refrigerant", 1, DEFAULT_REF, "Refrigerant"),
    S(12, "Sat temp", "°F", 1, 1, -40, 140, 40, "Dew temperature (sets the pressure)"),
    S(13, "Superheat", "°F", 1, 1, 0, 200, 20, "Superheat above that dew temperature"),
    # capacity and mass flow
    S(14, "Refrig. eff.", "Btu/lb", 2, 1, 0.1, 1000, 70, "Refrigeration effect, Btu per lb"),
    S(15, "Mass flow", "lb/min", 2, 0.5, 0, 100000, 3, "Refrigerant flow, lb per minute", blank=1),
    S(16, "Capacity", "tons", 2, 0.5, 0, 100000, 1, "Capacity wanted (0 = skip)", blank=1),
    # compressor displacement
    S(17, "Bore", "in", 3, 0.125, 0.1, 50, 2, "Cylinder bore, inches"),
    S(18, "Stroke", "in", 3, 0.125, 0.1, 50, 1.5, "Piston stroke, inches"),
    S(19, "Cylinders", "", 0, 1, 1, 64, 2, "Number of cylinders"),
    S(20, "Speed", "RPM", 0, 50, 1, 100000, 1750, "Compressor speed"),
    S(21, "Vol. eff.", "%", 0, 1, 1, 100, 85, "Volumetric efficiency"),
    # volumetric efficiency
    S(22, "Clearance", "%", 1, 0.5, 0, 50, 5, "Clearance volume, % of swept volume"),
    S(23, "Suction", "psig", 1, 1, -14, 1000, 118, "Suction pressure"),
    S(24, "Discharge", "psig", 1, 5, -14, 2000, 365, "Discharge pressure"),
    S(25, "Exponent n", "", 2, 0.01, 1, 2, 1.15, "Re-expansion exponent (about 1.1-1.2)"),
    # efficiency ratings
    S(26, "Value", "", 2, 0.1, 0.01, 1000, 12, "Efficiency number"),
    C(27, "Unit", 3, 1, "What that number is"),
    # water load
    S(28, "Flow", "GPM", 1, 1, 0.1, 1000000, 24, "Water flow, GPM"),
    S(29, "Entering", "°F", 1, 1, 0, 250, 54, "Entering water temperature"),
    S(30, "Leaving", "°F", 1, 1, 0, 250, 44, "Leaving water temperature"),
    S(31, "Factor", "", 0, 1, 100, 1000, 500, "500 for water (lb/h per GPM x cp)"),
    S(32, "Wet bulb", "°F", 1, 1, 0, 120, 0, "Air wet bulb for a tower (0 = skip)", blank=1),
    # wall heat gain
    S(33, "Length", "ft", 1, 1, 0.1, 1000, 10, "Inside length of the box, ft"),
    S(34, "Width", "ft", 1, 1, 0.1, 1000, 8, "Inside width, ft"),
    S(35, "Height", "ft", 1, 0.5, 0.1, 100, 8, "Inside height, ft"),
    S(36, "R-value", "", 1, 1, 1, 200, 32, "Insulation R-value (ft²·°F·h/Btu)"),
    S(37, "Outside", "°F", 1, 1, -40, 150, 90, "Temperature around the box"),
    S(38, "Inside", "°F", 1, 1, -60, 80, 35, "Box temperature"),
    # product load
    S(39, "Product", "lb", 0, 50, 0, 10000000, 1000, "Weight of product brought in, lb"),
    S(40, "Enters at", "°F", 1, 1, -60, 200, 70, "Product temperature coming in"),
    S(41, "Final", "°F", 1, 1, -60, 200, 35, "Product temperature wanted"),
    S(42, "Freezes", "°F", 1, 1, -40, 40, 32, "Freezing point (32 for water)"),
    S(43, "cp above", "Btu/lb°F", 2, 0.05, 0.05, 2, 1, "Specific heat above freezing (water 1.0)"),
    S(44, "Latent", "Btu/lb", 1, 1, 0, 200, 144, "Latent heat of freezing (water 144)"),
    S(45, "cp below", "Btu/lb°F", 2, 0.05, 0.05, 2, 0.5, "Specific heat below freezing (ice 0.5)"),
    S(46, "Pull-down", "h", 1, 1, 1, 240, 24, "Hours to bring it down"),
    # box equipment size
    S(47, "Walls", "Btu/24h", 0, 1000, 0, 1000000000, 20000, "Transmission load per 24 h"),
    S(48, "Product", "Btu/24h", 0, 1000, 0, 1000000000, 35000, "Product load per 24 h"),
    S(49, "Air changes", "Btu/24h", 0, 1000, 0, 1000000000, 15000, "Infiltration (door) load per 24 h"),
    S(50, "Other", "Btu/24h", 0, 1000, 0, 1000000000, 5000, "Lights, people, fans per 24 h"),
    S(51, "Safety", "%", 0, 5, 0, 100, 10, "Safety factor added, %"),
    S(52, "Run time", "h/day", 0, 1, 1, 24, 16, "Hours the unit may run per day"),
    # EPA leak rate
    C(53, "Appliance", 4, 1, "Type of appliance"),
    C(54, "Refrigerant", 5, 1, "HFC/HFO (GWP over 53) or CFC/HCFC"),
    S(55, "Full charge", "lb", 1, 1, 0.1, 1000000, 60, "Full charge of the appliance, lb"),
    S(56, "Added", "lb", 2, 0.5, 0, 1000000, 8, "Refrigerant added to refill it, lb"),
    C(57, "Method", 6, 1, "Leak rate method used at the facility"),
    S(58, "Days", "", 0, 1, 1, 3650, 365, "Days since refrigerant was last added"),
    # evacuation levels
    C(59, "Refrigerant", 7, DEFAULT_REF, "Refrigerant in the appliance"),
    S(60, "Full charge", "lb", 1, 1, 0.1, 1000000, 60, "Full charge, lb"),
    C(61, "Recov. unit", 8, 1, "Recovery machine made before Nov 15, 1993?"),
    C(62, "Small appl.", 9, 1, "Sealed, 5 lb or less? Does the comp. run?"),
    # charge record
    S(63, "Cyl. before", "lb", 2, 0.25, 0, 10000, 25, "Charging cylinder weight before, lb"),
    S(64, "Cyl. after", "lb", 2, 0.25, 0, 10000, 21.5, "Charging cylinder weight after, lb"),
    S(65, "Rec. before", "lb", 2, 0.25, 0, 10000, 0, "Recovery cylinder before (0 = none)", blank=1),
    S(66, "Rec. after", "lb", 2, 0.25, 0, 10000, 0, "Recovery cylinder after", blank=1),
    # invoice
    S(67, "Labor", "h", 2, 0.25, 0, 1000, 1.5, "Labor hours"),
    S(68, "Labor rate", "$/h", 2, 5, 0, 10000, 95, "Labor rate, $ per hour"),
    S(69, "Parts cost $", "", 2, 5, 0, 1000000, 120, "What the parts cost you"),
    S(70, "Markup", "%", 1, 5, 0, 1000, 50, "Markup on parts, %"),
    S(71, "Refrigerant", "lb", 2, 0.5, 0, 10000, 2, "Refrigerant charged, lb"),
    S(72, "$ per lb", "", 2, 1, 0, 10000, 45, "Refrigerant price per lb"),
    S(73, "Trip $", "", 2, 5, 0, 100000, 79, "Trip / diagnostic charge"),
    S(74, "Tax", "%", 3, 0.25, 0, 30, 0, "Sales tax on parts + refrigerant, %"),
    # markup and margin
    S(75, "Cost $", "", 2, 5, 0, 10000000, 100, "Your cost"),
    S(76, "Markup", "%", 1, 5, 0, 10000, 50, "Markup on cost, % (0 = use margin)", blank=1),
    S(77, "Margin", "%", 1, 5, 0, 99.9, 0, "Gross margin, % (used if markup 0)", blank=1),
    # time sheet
    S(78, "Start hour", "", 0, 1, 0, 23, 7, "Start, hour of the day (0-23)"),
    S(79, "Start min", "", 0, 5, 0, 59, 30, "Start, minutes"),
    S(80, "End hour", "", 0, 1, 0, 23, 16, "End, hour of the day (0-23)"),
    S(81, "End min", "", 0, 5, 0, 59, 45, "End, minutes"),
    S(82, "Unpaid break", "min", 0, 5, 0, 600, 30, "Unpaid lunch / break, minutes"),
    S(83, "Pay rate", "$/h", 2, 0.5, 0, 10000, 22, "Hourly pay"),
    S(84, "Week so far", "h", 2, 1, 0, 168, 32, "Hours already worked this week"),
    # unit converter
    C(85, "Convert", 11, 1, "Kind of value"),
    S(86, "Value", "", -1, 1, -1000000000, 1000000000, 100, "Number to convert"),
    C(87, "From", UNITS, 1, "Unit of that number"),
]

TOOLS = [
    ("Cycle state points", "Cycle", "points", 1, [1, 2, 3, 4, 5, 6, 7, 8]),
    ("Cycle performance", "Cycle", "perform.", 1, [1, 2, 3, 4, 5, 6, 7, 8]),
    ("Saturated properties", "Sat.", "props", 1, [9, 10]),
    ("Superheated vapor", "Super-", "heated", 1, [11, 12, 13]),
    ("Capacity and flow", "Capacity", "and flow", 2, [14, 15, 16]),
    ("Compressor displacement", "Comp.", "displace.", 2, [17, 18, 19, 20, 21]),
    ("Volumetric efficiency", "Vol.", "efficiency", 2, [22, 23, 24, 25]),
    ("Efficiency ratings", "EER", "COP kW/t", 2, [26, 27]),
    ("Water load / tower", "Water", "load", 3, [28, 29, 30, 31, 32]),
    ("Box wall heat gain", "Box", "walls", 3, [33, 34, 35, 36, 37, 38]),
    ("Product load", "Product", "load", 3, [39, 40, 41, 42, 43, 44, 45, 46]),
    ("Box equipment size", "Box", "equipment", 3, [47, 48, 49, 50, 51, 52]),
    ("EPA leak rate", "EPA", "leak rate", 4, [53, 54, 55, 56, 57, 58]),
    ("EPA evacuation levels", "EPA", "evacuation", 4, [59, 60, 61, 62]),
    ("Charge record", "Charge", "record", 4, [63, 64, 65, 66]),
    ("Service invoice", "Service", "invoice", 4, [67, 68, 69, 70, 71, 72, 73, 74]),
    ("Markup and margin", "Markup", "margin", 5, [75, 76, 77]),
    ("Time sheet", "Time", "sheet", 5, [78, 79, 80, 81, 82, 83, 84]),
    ("Unit converter", "Units", "", 5, [85, 86, 87]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=19)
    for name, (sat, H, S_, V, p104) in DATA.items():
        for row in sat:
            assert row[0] >= row[1] - 1e-9, name          # bubble >= dew pressure
        for hr, sr, vr in zip(H, S_, V):
            assert all(b > a for a, b in zip(hr, hr[1:])), name
            assert all(b > a for a, b in zip(sr, sr[1:])), name
            assert all(b > a for a, b in zip(vr, vr[1:])), name
        assert abs(sat[0][2]) < 1e-6, name                    # ASHRAE reference
    assert len(CHOICES[7]) == len(REFRIGERANTS) + len(EPA_EXAMPLES)
    # the EPA definitions name R-22, R-407C, R-410A as high-pressure and R-12,
    # R-134a as medium-pressure; the computed classes agree
    for n, cls in (("R-22", 3), ("R-407C", 3), ("R-410A", 3), ("R-12", 2), ("R-134a", 2)):
        assert epa_class(DATA[n][4]) == cls, n


def ints(rows, scale):
    return [[int(round(v * scale)) for v in r] for r in rows]


def build_block():
    out = ["// ---- BEGIN TABLES (generated by tools/gen_cycle_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// property grid: saturation -40..140 F every 5 F (rows), superheat 0..200 F",
        "// every 10 F (columns) at the dew-point pressure; ASHRAE reference state",
        "gNRef:=" + str(len(REFRIGERANTS)) + ";",
        "// EPA appliance class (1 low, 2 medium, 3 high, 4 very high pressure, 40 CFR",
        "// 82.152) and liquid pressure at 104 F (psia) for the evacuation list",
        "gEpaCls:=" + plist([epa_class(DATA[n][4]) for n, _ in REFRIGERANTS] + [c for _, c in EPA_EXAMPLES]) + ";",
        "gEpaP:=" + plist([round(DATA[n][4], 1) for n, _ in REFRIGERANTS] + [0] * len(EPA_EXAMPLES)) + ";",
    ]
    for k, (name, _) in enumerate(REFRIGERANTS, 1):
        sat, H, S_, V, _ = DATA[name]
        out += [f"// {name}: bubble psia x1000, dew psia x1000, bubble liquid h x1000 (Btu/lb)",
                f"gSat{k}:=" + pmatrix(ints(sat, 1000)) + ";",
                f"// {name}: vapor h x1000 (Btu/lb), s x100000 (Btu/lb R), v x100000 (ft3/lb)",
                f"gH{k}:=" + pmatrix(ints(H, 1000)) + ";",
                f"gS{k}:=" + pmatrix(ints(S_, 100000)) + ";",
                f"gV{k}:=" + pmatrix(ints(V, 100000)) + ";"]
    out += ["", "// property table of refrigerant r: 1 saturation, 2 h, 3 s, 4 v", "refTab(r,k)", "BEGIN"]
    for k in range(1, len(REFRIGERANTS) + 1):
        out.append(f"  IF r=={k} THEN")
        out.append(f"    IF k==1 THEN RETURN gSat{k}; END;")
        out.append(f"    IF k==2 THEN RETURN gH{k}; END;")
        out.append(f"    IF k==3 THEN RETURN gS{k}; END;")
        out.append(f"    RETURN gV{k};")
        out.append("  END;")
    out += ["  RETURN gSat1;", "END;", ""]
    out += slot_functions(TOOLS, CHOICES, UNITS, 85)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes, {len(TOOLS)} tools and {len(REFRIGERANTS)} refrigerants into {PROGRAM}")


if __name__ == "__main__":
    main()
