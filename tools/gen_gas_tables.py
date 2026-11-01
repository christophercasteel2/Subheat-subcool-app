#!/usr/bin/env python3
"""Write the generated block of hp-prime/HVACGAS.txt: the tool list, the
input-box ("slot") tables and the code tables of the gas heating and
piping calculator.

Edit the tables here (or the data files they come from), then run
    python3 tools/gen_gas_tables.py

Sources (every number is copied, none is computed from a formula)
  tools/data/gas/ifgc_402_4.json      IFGC 2021 Tables 402.4(1)-(37), the gas
        pipe and tubing capacity tables, as printed in the 2021 Seattle Fuel
        Gas Code chapter 4 (the IFGC tables without amendment) and checked
        row by row against the 2018 edition
  tools/data/gas/ifgc_appendix_a.json IFGC Appendix A Table A102.2 (equivalent
        length of fittings and valves) and Table A102.4 (specific gravity
        multipliers)
  tools/data/gas/copper_tube.json     CDA Copper Tube Handbook Tables 14.2a,
        14.2b, 14.2c and 14.2e (Type K, L, M and ACR tube), checked against
        a mill's ASTM B88 / B280 dimension sheet
  BRAZING below                       CDA Copper Tube Handbook Table 14.12
  STEEL below                         Schedule 40 inside diameters from the
        IFGC tables, outside diameters from ASME B36.10, threads per inch from
        ASME B1.20.1
"""
import json
import os

from ppltables import (check_slots, choice_slot, plist, pmatrix, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "HVACGAS.txt")
DATA = os.path.join(ROOT, "tools", "data", "gas")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


PIPE = load("ifgc_402_4.json")["tables"]
APPA = load("ifgc_appendix_a.json")
COPPER = load("copper_tube.json")

# ---------------------------------------------------------------------------
# gas pipe tables

MAT_SHORT = {"SCHEDULE 40 METALLIC PIPE": "steel", "SEMIRIGID COPPER TUBING": "copper",
             "CORRUGATED STAINLESS STEEL TUBING (CSST)": "CSST",
             "POLYETHYLENE PLASTIC PIPE": "PE pipe", "POLYETHYLENE PLASTIC TUBING": "PE tube"}
MAT_LONG = {"steel": "Sch 40 steel pipe", "copper": "Copper tubing (K/L/ACR)",
            "CSST": "CSST (by EHD)", "PE pipe": "PE plastic pipe", "PE tube": "PE plastic tubing"}


def short_press(p):
    p = p.replace("Less than 2.0 psi", "<2 psi").replace("Less than 2 psi", "<2 psi")
    p = p.replace(" in. w.c.", " in w.c.").replace("2 psi", "2 psi")
    return p.replace(".0 ", " ")


def drop_tag(d):
    d = short_press(d)
    return d.replace(" in w.c.", "wc").replace(" psi", "psi")


MAT_TAG = {"steel": "stl", "copper": "Cu", "CSST": "CSST", "PE pipe": "PE", "PE tube": "PEt"}


def table_label(t):
    """short name for the table chooser, e.g. 2 NG stl 0.5wc or 13 NG Cu 2-1.5
    (inlet - drop, psi); the result rows spell the table out"""
    gas = "NG" if t["gas"] == "Natural" else "LP"
    mat = MAT_TAG[MAT_SHORT[t["material"]]]
    drop = drop_tag(t["drop"])
    if "psi" in t["inlet"] and "<" not in short_press(t["inlet"]):
        drop = short_press(t["inlet"]).replace(" psi", "") + "-" + drop.replace("psi", "")
    return f"{t['table']} {gas} {mat} {drop}"


def size_labels(t):
    mat = MAT_SHORT[t["material"]]
    if mat == "copper":
        return [f"{s} ({a if a != '—' else od_of(o)} OD)"
                for s, a, o in zip(t["sizes"], t["acr"], ["0.375", "0.500", "0.625", "0.750", "0.875",
                                                         "1.125", "1.375", "1.625", "2.125"])]
    if mat == "CSST":
        return ["EHD " + s for s in t["sizes"]]
    if mat in ("PE pipe", "PE tube"):
        return [f"{s} {d}" for s, d in zip(t["sizes"], t["sdr"])]
    return [s + " in" for s in t["sizes"]]


def od_of(o):
    return {"1.625": "1-5/8", "2.125": "2-1/8"}[o]


SDR = {"PE pipe": ["SDR 9", "SDR 11", "SDR 11", "SDR 10", "SDR 11", "SDR 11", "SDR 11", "SDR 11"],
       "PE tube": ["SDR 7", "SDR 11"]}
for t in PIPE:
    mat = MAT_SHORT[t["material"]]
    if mat in SDR:
        t["sdr"] = SDR[mat]

# the intended use printed on a table, shortened to fit one result row
USE = {3: "start at 8 in w.c. or more", 4: "start at 11 in w.c. or more",
       10: "house line regulator to appliance", 13: "delivery to house regulator",
       16: "start at 8 in w.c. or more", 17: "start at 11 in w.c. or more",
       25: "1st stage to 2nd stage regulator", 26: "1st stage to 2nd stage regulator",
       27: "2 psi service to line regulator", 28: "2nd stage regulator to appliance",
       29: "1st stage to 2nd stage regulator", 30: "2nd stage regulator to appliance",
       31: "2 psi service to line regulator", 32: "2nd stage regulator to appliance",
       33: "2 psi service to line regulator", 35: "2nd stage regulator to building",
       36: "2 psi service to line regulator", 37: "2nd stage regulator to building"}

# group the size rows and length columns that tables share
SIZE_SETS, LEN_SETS = [], []
for t in PIPE:
    sz = (tuple(size_labels(t)), tuple(t["ids"]))
    if sz not in SIZE_SETS:
        SIZE_SETS.append(sz)
    t["sset"] = SIZE_SETS.index(sz) + 1
    ln = tuple(t["lengths"])
    if ln not in LEN_SETS:
        LEN_SETS.append(ln)
    t["lset"] = LEN_SETS.index(ln) + 1

# ---------------------------------------------------------------------------
# steel pipe (choice list 4): 1/8 - 12 in Schedule 40

STEEL = ["1/8", "1/4", "3/8", "1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "4",
         "5", "6", "8", "10", "12"]
STEEL_OD = [0.405, 0.540, 0.675, 0.840, 1.050, 1.315, 1.660, 1.900, 2.375, 2.875, 3.500,
            4.500, 5.563, 6.625, 8.625, 10.750, 12.750]
STEEL_ID = [0.269, 0.364, 0.493] + [float(x) for x in PIPE[0]["ids"]]
STEEL_TPI = [27, 18, 18, 14, 14, 11.5, 11.5, 11.5, 11.5, 8, 8, 8, 8, 8, 8, 8, 8]
# Table 415.1 support spacing, ft (0 = smaller than the table lists)
STEEL_SUPPORT = [0, 0, 0, 6, 8, 8] + [10] * 11

# Appendix A Table A102.2, rows 1/2 - 12 in: 45 ell, 90 ell, 180 return, tee, gate valve
FIT = [r["screwed"] + [r["valves"][0]] for r in APPA["rows"] if r["size"] in STEEL[3:]]
SG = APPA["sg_multipliers"]

# ---------------------------------------------------------------------------
# copper tube


def num(s):
    return float(s) if s not in ("", "-") else 0.0


NOMINAL = ["1/4", "3/8", "1/2", "5/8", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3",
           "3-1/2", "4", "5", "6", "8", "10", "12"]
GLYPH = {"¼": "1/4", "⅜": "3/8", "½": "1/2", "⅝": "5/8", "¾": "3/4", "⅞": "7/8", "⅛": "1/8",
         "3⁄16": "3/16", "5⁄16": "5/16"}


def plain(s):
    for g, r in GLYPH.items():
        if s == g:
            return r
        if s.endswith(g) and len(s) > len(g):
            return s[:-len(g)] + "-" + r
    return s


def klm(rows):
    by = {plain(r[0]): r for r in rows}
    return [[num(by[s][1]), num(by[s][2]), num(by[s][3]), num(by[s][5])] if s in by else [0, 0, 0, 0]
            for s in NOMINAL]


CU = {k: klm(COPPER[k]) for k in ("K", "L", "M")}
ACR_OD = ["1/8", "3/16", "1/4", "5/16", "3/8", "1/2", "5/8", "3/4", "7/8", "1-1/8", "1-3/8",
          "1-5/8", "2-1/8", "2-5/8", "3-1/8", "3-5/8", "4-1/8"]


def acr(temper):
    by = {plain(r[0]): r for r in COPPER["ACR"] if r[1] == temper}
    return [[num(by[s][2]), num(by[s][3]), num(by[s][4]), num(by[s][8])] if s in by else [0, 0, 0, 0]
            for s in ACR_OD]


ACR_A, ACR_D = acr("A"), acr("D")

# CDA Table 14.12 brazing filler metals, plus two common solders (ASTM B32)
# name, silver %, phosphorus %, other, solidus F, liquidus F, note
BRAZING = [
    ("BCuP-2", "0", "7.0-7.5", "", 1310, 1460, "close fits; no flux Cu to Cu"),
    ("BCuP-3", "4.8-5.2", "5.8-6.2", "", 1190, 1495, "fills gaps; no flux Cu to Cu"),
    ("BCuP-4", "5.8-6.2", "7.0-7.5", "", 1190, 1325, "fluid; no flux Cu to Cu"),
    ("BCuP-5", "14.5-15.5", "4.8-5.2", "", 1190, 1475, "15% silver; no flux Cu to Cu"),
    ("BCuP-6", "1.8-2.2", "6.8-7.2", "", 1190, 1450, "2% silver; no flux Cu to Cu"),
    ("BCuP-7", "4.8-5.2", "6.5-7.0", "", 1190, 1420, "5% silver; no flux Cu to Cu"),
    ("BCuP-8", "17.2-18.0", "6.0-6.7", "", 1190, 1230, "18% silver; no flux Cu to Cu"),
    ("BCuP-9", "0", "6.0-7.0", "Sn 6.0-7.0", 1178, 1247, "tin added; no flux Cu to Cu"),
    ("BAg-5", "44.0-46.0", "0", "Zn 23-27", 1225, 1370, "flux needed"),
    ("BAg-6", "49.0-51.0", "0", "Zn 14-18", 1270, 1425, "flux needed"),
    ("BAg-7", "55.0-57.0", "0", "Zn 15-19, Sn 4.5-5.5", 1145, 1205, "flux; no-cadmium BAg-1"),
    ("BAg-20", "29.0-31.0", "0", "Zn 30-34", 1250, 1410, "flux needed"),
    ("BAg-28", "39.0-41.0", "0", "Zn 26-30, Sn 1.5-2.5", 1200, 1310, "flux needed"),
    ("BAg-34", "37.0-39.0", "0", "Zn 26-30, Sn 1.5-2.5", 1200, 1330, "flux; no-cadmium BAg-2"),
    ("Solder 50-50", "0", "0", "Sn 50, Pb 50", 361, 421, "lead: never on drinking water"),
    ("Solder 95-5", "0", "0", "Sn 95, Sb 5", 452, 464, "lead-free tin-antimony"),
]

# expansion, in/in/F: copper from the CDA handbook; the others are
# common handbook values (the tool shows the number it uses)
EXPANSION = [("Copper", 9.4), ("Carbon steel", 6.5), ("PVC", 30.0), ("CPVC", 34.0),
             ("Aluminum", 12.8), ("Custom", 0)]

# ---------------------------------------------------------------------------
# choice lists and input boxes

CONV_UNITS_MAX = 8
UNITS = 9

CHOICES = {
    1: [table_label(t) for t in PIPE],
    2: ["CFH", "kBtu/h", "Btu/h"],
    3: ["Natural gas", "Propane (LP)"],
    4: [s + " in" for s in STEEL],
    5: ["No", "Yes"],
    6: ["None (open)", "Metal 75%", "Wood 25%"],
    7: ["Natural gas", "Propane", "#2 fuel oil"],
    8: ["Pressure", "Energy", "Heat rate"],
    10: ["Type K", "Type L", "Type M", "ACR soft", "ACR hard"],
    11: [s + " nominal" for s in NOMINAL],
    12: [s + " OD" for s in ACR_OD],
    13: ["11-1/4°", "22-1/2°", "30°", "45°", "60°"],
    14: [m for m, _ in EXPANSION],
    15: [b[0] for b in BRAZING],
}

S = slot
C = choice_slot(CHOICES, UNITS, CONV_UNITS_MAX)

SLOTS = [
    # gas pipe size
    C(1, "Table", 1, 2, "IFGC Table 402.4( ): gas, material, drop"),
    S(2, "Length", "ft", 0, 5, 1, 5000, 60, "Longest length (or branch length), ft"),
    S(3, "Load", "", -1, 10, 0, 100000000, 200, "Gas load of the section"),
    C(4, "Load unit", 2, 1, "Unit of the load"),
    S(5, "Heat value", "Btu/ft³", 0, 10, 0, 4000, 0, "0 = 1,000 natural / 2,516 propane", blank=3),
    S(6, "Gas SG", "", 2, 0.05, 0.35, 2.1, 0.6, "Natural gas specific gravity (0.60)"),
    # pipe capacity
    C(7, "Table", 1, 2, "IFGC Table 402.4( ): gas, material, drop"),
    S(8, "Length", "ft", 0, 5, 1, 5000, 60, "Length to look up, ft"),
    # fitting allowance
    C(9, "Pipe size", 4, 5, "Schedule 40 pipe size"),
    S(10, "Pipe length", "ft", 0, 5, 0, 5000, 40, "Measured length of pipe, ft"),
    S(11, "90° ells", "", 0, 1, 0, 100, 4, "Number of screwed 90° elbows"),
    S(12, "45° ells", "", 0, 1, 0, 100, 0, "Number of screwed 45° elbows"),
    S(13, "Tees", "", 0, 1, 0, 100, 1, "Tees (flow through the branch)"),
    S(14, "Gate valves", "", 0, 1, 0, 100, 1, "Open gate (or similar) valves"),
    # gas load
    S(15, "Appliance 1", "Btu/h", 0, 1000, 0, 100000000, 100000, "Input rating of an appliance", blank=1),
    S(16, "Appliance 2", "Btu/h", 0, 1000, 0, 100000000, 40000, "Input rating of an appliance", blank=1),
    S(17, "Appliance 3", "Btu/h", 0, 1000, 0, 100000000, 65000, "Input rating of an appliance", blank=1),
    S(18, "Appliance 4", "Btu/h", 0, 1000, 0, 100000000, 35000, "Input rating of an appliance", blank=1),
    S(19, "Appliance 5", "Btu/h", 0, 1000, 0, 100000000, 0, "Input rating of an appliance", blank=1),
    S(20, "Appliance 6", "Btu/h", 0, 1000, 0, 100000000, 0, "Input rating of an appliance", blank=1),
    C(21, "Gas", 3, 1, "Natural gas or propane"),
    S(22, "Heat value", "Btu/ft³", 0, 10, 0, 4000, 0, "0 = 1,000 natural / 2,516 propane", blank=3),
    # clock the meter
    S(23, "Dial size", "ft³", -1, 0.5, 0.01, 1000, 1, "Test dial: cubic feet per revolution"),
    S(24, "Revolutions", "", 0, 1, 1, 100, 1, "Revolutions timed"),
    S(25, "Seconds", "s", 1, 1, 1, 10000, 36, "Seconds for those revolutions"),
    S(26, "Heat value", "Btu/ft³", 0, 10, 100, 4000, 1000, "From the gas supplier (1,000 typical)"),
    S(27, "Rated input", "Btu/h", 0, 1000, 0, 100000000, 100000, "Nameplate input (0 = skip)", blank=1),
    # manifold pressure
    S(28, "Measured", "Btu/h", 0, 1000, 1, 100000000, 90000, "Input clocked at the meter"),
    S(29, "Rated input", "Btu/h", 0, 1000, 1, 100000000, 100000, "Nameplate input"),
    S(30, "Manifold", "in wc", 2, 0.1, 0.1, 40, 3.5, "Manifold pressure now, in w.c."),
    C(31, "Gas", 3, 1, "Natural gas or propane"),
    # altitude
    S(32, "Rated input", "Btu/h", 0, 1000, 1, 100000000, 100000, "Sea-level nameplate input"),
    S(33, "Elevation", "ft", 0, 100, 0, 15000, 5000, "Elevation above sea level, ft"),
    S(34, "Derate", "%/kft", 1, 0.5, 0, 10, 4, "Percent per 1,000 ft (4 typical)"),
    S(35, "Starts above", "ft", 0, 500, 0, 10000, 2000, "No derate at or below this elevation"),
    # combustion air
    S(36, "Total input", "Btu/h", 0, 1000, 1, 100000000, 140000, "All appliances in the space"),
    S(37, "Fan-assisted", "Btu/h", 0, 1000, 0, 100000000, 0, "Part of that which is fan-assisted", blank=1),
    S(38, "Room length", "ft", 1, 1, 0, 10000, 12, "Space length, ft"),
    S(39, "Room width", "ft", 1, 1, 0, 10000, 10, "Space width, ft"),
    S(40, "Ceiling", "ft", 1, 0.5, 0, 100, 8, "Space height, ft"),
    S(41, "Known ACH", "", 2, 0.05, 0, 0.6, 0, "Air changes/h if known (0 = standard)", blank=1),
    C(42, "Louvers", 6, 2, "Louver or grille free area"),
    # combustion analysis
    C(43, "Fuel", 7, 1, "Fuel burned"),
    S(44, "O2", "%", 1, 0.1, 0, 20.8, 6, "Oxygen in the flue gas, %"),
    S(45, "CO", "ppm", 0, 5, 0, 100000, 25, "Carbon monoxide as measured, ppm"),
    S(46, "Flue temp", "°F", 0, 5, -40, 2000, 400, "Flue gas temperature, °F"),
    S(47, "Air temp", "°F", 0, 1, -40, 200, 70, "Combustion air temperature, °F"),
    # furnace
    S(48, "Input", "Btu/h", 0, 1000, 1, 100000000, 80000, "Nameplate input"),
    S(49, "Efficiency", "%", 1, 1, 1, 100, 80, "AFUE or steady-state efficiency, %"),
    S(50, "Temp rise", "°F", 1, 1, 0, 200, 0, "Supply - return (0 = work out)", blank=1),
    S(51, "Airflow", "CFM", 0, 25, 0, 100000, 1000, "Blower CFM (0 = work out)", blank=1),
    # oil nozzle
    S(52, "Input", "Btu/h", 0, 1000, 1, 100000000, 140000, "Burner input wanted, Btu/h"),
    S(53, "Nozzle", "GPH", 2, 0.05, 0.1, 100, 1, "Nozzle rating (at 100 psi)"),
    S(54, "Pump", "psi", 0, 5, 1, 400, 100, "Pump pressure, psi"),
    S(55, "Oil value", "Btu/gal", 0, 500, 100000, 200000, 140000, "Heat in a gallon (140,000 typical)"),
    # pressure test
    S(56, "Working", "psig", 2, 0.25, 0, 1000, 0.25, "Max working pressure (7 in wc = 0.25)"),
    C(57, "1-family", 5, 2, "Single-family dwelling?"),
    C(58, "Size 1", 4, 6, "Pipe size of the first section"),
    S(59, "Length 1", "ft", 0, 10, 0, 100000, 100, "Length of the first section, ft"),
    C(60, "Size 2", 4, 4, "Pipe size of a second section"),
    S(61, "Length 2", "ft", 0, 10, 0, 100000, 0, "Length of the second section, ft", blank=1),
    # fuel cost
    S(62, "Gas price", "$/thm", 2, 0.05, 0, 100, 1.2, "Natural gas, $ per therm"),
    S(63, "Gas eff.", "%", 0, 1, 1, 100, 95, "Gas furnace AFUE, %"),
    S(64, "LP price", "$/gal", 2, 0.05, 0, 100, 2.5, "Propane, $ per gallon"),
    S(65, "LP eff.", "%", 0, 1, 1, 100, 95, "Propane furnace AFUE, %"),
    S(66, "Oil price", "$/gal", 2, 0.05, 0, 100, 3.75, "#2 fuel oil, $ per gallon"),
    S(67, "Oil eff.", "%", 0, 1, 1, 100, 85, "Oil furnace AFUE, %"),
    S(68, "Electric", "$/kWh", 3, 0.01, 0, 10, 0.15, "Electricity, $ per kWh"),
    S(69, "COP", "", 1, 0.1, 1, 10, 3, "Heat pump COP (1 = resistance heat)"),
    # units
    C(70, "Convert", 8, 1, "Pressure, energy or heat rate"),
    S(71, "Value", "", -1, 1, -1000000000, 1000000000, 7, "Number to convert"),
    C(72, "From", UNITS, 1, "Unit of that number"),
    # copper tube
    C(73, "Tube type", 10, 2, "K, L, M (by nominal size) or ACR (by OD)"),
    C(74, "Nominal", 11, 3, "Nominal size, for Type K, L and M"),
    C(75, "ACR size", 12, 6, "Outside diameter, for ACR tube"),
    S(76, "Length", "ft", 0, 10, 0, 100000, 100, "Length for weight and volume, ft"),
    # steel pipe
    C(77, "Pipe size", 4, 6, "Schedule 40 pipe size"),
    S(78, "Length", "ft", 0, 10, 0, 100000, 100, "Length for weight and volume, ft"),
    # offsets
    S(79, "Offset", "in", -1, 0.25, 0, 10000, 12, "Offset (set) between centerlines, in"),
    S(80, "Roll", "in", -1, 0.25, 0, 10000, 0, "Roll for a rolling offset (0 = none)", blank=1),
    C(81, "Fittings", 13, 4, "Angle of the two fittings"),
    S(82, "Take-off", "in", -1, 0.125, 0, 100, 0, "Fitting take-off each end (0 = none)", blank=1),
    # expansion
    C(83, "Material", 14, 1, "Pipe or tube material"),
    S(84, "Length", "ft", 0, 10, 0, 100000, 100, "Length of the run, ft"),
    S(85, "Temp change", "°F", 0, 5, 0, 1000, 100, "Temperature change, °F"),
    S(86, "Custom", "µin/°F", 2, 0.1, 0, 1000, 9.4, "Custom coefficient, millionths in/in/°F"),
    # brazing
    C(87, "Alloy", 15, 4, "Brazing filler metal or solder"),
]

# tools in tile order; tile 20 (Learn) opens reference pages instead
TOOLS = [
    ("Gas pipe size", "Pipe", "size", 1, [1, 2, 3, 4, 5, 6]),
    ("Pipe capacity", "Pipe", "capacity", 1, [7, 8]),
    ("Fitting allowance", "Fitting", "allowance", 1, [9, 10, 11, 12, 13, 14]),
    ("Gas load", "Gas", "load", 1, [15, 16, 17, 18, 19, 20, 21, 22]),
    ("Clock the meter", "Clock", "meter", 2, [23, 24, 25, 26, 27]),
    ("Manifold pressure", "Manifold", "pressure", 2, [28, 29, 30, 31]),
    ("Altitude derate", "Altitude", "derate", 2, [32, 33, 34, 35]),
    ("Combustion air", "Comb.", "air", 2, [36, 37, 38, 39, 40, 41, 42]),
    ("Combustion analysis", "Flue gas", "analysis", 3, [43, 44, 45, 46, 47]),
    ("Furnace output", "Furnace", "output", 3, [48, 49, 50, 51]),
    ("Oil nozzle", "Oil", "nozzle", 3, [52, 53, 54, 55]),
    ("Gas pressure test", "Pressure", "test", 3, [56, 57, 58, 59, 60, 61]),
    ("Fuel cost", "Fuel", "cost", 4, [62, 63, 64, 65, 66, 67, 68, 69]),
    ("Unit converter", "Units", "", 4, [70, 71, 72]),
    ("Copper tube", "Copper", "tube", 4, [73, 74, 75, 76]),
    ("Steel pipe", "Steel", "pipe", 4, [77, 78]),
    ("Pipe offsets", "Pipe", "offsets", 5, [79, 80, 81, 82]),
    ("Expansion", "Expan-", "sion", 5, [83, 84, 85, 86]),
    ("Brazing and solder", "Brazing", "solder", 5, [87]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=19)
    assert len(PIPE) == 37 and [t["table"] for t in PIPE] == list(range(1, 38))
    for t in PIPE:
        assert len(t["capacity"]) == len(t["lengths"])
        for row in t["capacity"]:
            assert len(row) == len(t["sizes"])
        for col in zip(*t["capacity"]):
            nz = [v for v in col if v]
            # capacities fall with length, except two printed entries that
            # break the pattern in the code book itself (kept as printed)
            bad = [(a, b) for a, b in zip(nz, nz[1:]) if b > a]
            assert len(bad) <= 1, (t["table"], bad)
        assert t["units"] in ("CFH", "kBtu/h")
    assert all(len(lbl) <= 17 for lbl in CHOICES[1]), max(CHOICES[1], key=len)
    assert len(STEEL_OD) == len(STEEL_ID) == len(STEEL) == len(STEEL_TPI) == len(STEEL_SUPPORT)
    for od, i in zip(STEEL_OD, STEEL_ID):
        assert 0.05 < (od - i) / 2 < 0.5
    assert len(FIT) == 14 and SG[5] == [0.6, 1.0]
    for k in "KLM":
        for od, i, w, lb in CU[k]:
            assert od == 0 or abs((od - i) / 2 - w) < 0.0011, (k, od, i, w)
    for rows in (ACR_A, ACR_D):
        for od, i, w, lb in rows:
            assert od == 0 or abs((od - i) / 2 - w) < 0.0011, (od, i, w)
    for b in BRAZING:
        assert b[4] < b[5] and len(b[6]) <= 34


def build_block():
    out = ["// ---- BEGIN TABLES (generated by tools/gen_gas_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// IFGC Table 402.4(n): material, gas (1 natural, 2 propane), inlet pressure,",
        "// pressure drop, units (1 CFH, 2 thousands of Btu/h), size set, length set",
        "gTMat:=" + plist([MAT_LONG[MAT_SHORT[t["material"]]] for t in PIPE]) + ";",
        "gTGas:=" + plist([1 if t["gas"] == "Natural" else 2 for t in PIPE]) + ";",
        "gTIn:=" + plist([short_press(t["inlet"]) for t in PIPE]) + ";",
        "gTDrop:=" + plist([short_press(t["drop"]) for t in PIPE]) + ";",
        "gTUnit:=" + plist([1 if t["units"] == "CFH" else 2 for t in PIPE]) + ";",
        "gTSz:=" + plist([t["sset"] for t in PIPE]) + ";",
        "gTLn:=" + plist([t["lset"] for t in PIPE]) + ";",
        "gTUse:=" + plist([USE.get(t["table"], "") for t in PIPE]) + ";",
        "// capacities: rows are the lengths, columns the sizes (0 = NA)",
    ]
    for t in PIPE:
        out.append(f"gP{t['table']}:=" + pmatrix(t["capacity"]) + ";")
    out += [
        "// Appendix A Table A102.4: gas specific gravity and capacity multiplier",
        "gSG:=" + plist([s for s, _ in SG]) + ";",
        "gSGm:=" + plist([m for _, m in SG]) + ";",
        "// Schedule 40 steel 1/8 - 12 in: OD, ID, threads per inch, Table 415.1 support (ft)",
        "gStOD:=" + plist(STEEL_OD) + ";",
        "gStID:=" + plist(STEEL_ID) + ";",
        "gStTPI:=" + plist(STEEL_TPI) + ";",
        "gStSup:=" + plist(STEEL_SUPPORT) + ";",
        "// Table A102.2, 1/2 - 12 in: 45 ell, 90 ell, 180 return, tee, gate valve (ft)",
        "gFit:=" + pmatrix(FIT) + ";",
        "// copper tube: OD, ID, wall (in), lb per ft; 0 = not made",
        "gCuK:=" + pmatrix(CU["K"]) + ";",
        "gCuL:=" + pmatrix(CU["L"]) + ";",
        "gCuM:=" + pmatrix(CU["M"]) + ";",
        "gAcrA:=" + pmatrix(ACR_A) + ";",
        "gAcrD:=" + pmatrix(ACR_D) + ";",
        "// brazing filler metals and solders",
        "gBzAg:=" + plist([b[1] for b in BRAZING]) + ";",
        "gBzP:=" + plist([b[2] for b in BRAZING]) + ";",
        "gBzX:=" + plist([b[3] for b in BRAZING]) + ";",
        "gBzSol:=" + plist([b[4] for b in BRAZING]) + ";",
        "gBzLiq:=" + plist([b[5] for b in BRAZING]) + ";",
        "gBzN:=" + plist([b[6] for b in BRAZING]) + ";",
        "// expansion coefficients, millionths of an inch per inch per F",
        "gExp:=" + plist([c for _, c in EXPANSION]) + ";",
        "",
        "// capacity table n",
        "pipeTab(n)",
        "BEGIN",
    ]
    for t in PIPE:
        out.append(f"  IF n=={t['table']} THEN RETURN gP{t['table']}; END;")
    out += ["  RETURN gP2;", "END;", "", "// size names and inside diameters of size set s", "sizeSet(s)", "BEGIN"]
    for k, (labels, _) in enumerate(SIZE_SETS, 1):
        out.append(f"  IF s=={k} THEN RETURN {plist(list(labels))}; END;")
    out += ["  RETURN {};", "END;", "", "idSet(s)", "BEGIN"]
    for k, (_, ids) in enumerate(SIZE_SETS, 1):
        out.append(f"  IF s=={k} THEN RETURN {plist(list(ids))}; END;")
    out += ["  RETURN {};", "END;", "", "// table lengths (ft) of length set s", "lenSet(s)", "BEGIN"]
    for k, lens in enumerate(LEN_SETS, 1):
        out.append(f"  IF s=={k} THEN RETURN {plist(list(lens))}; END;")
    out += ["  RETURN {};", "END;", ""]
    out += slot_functions(TOOLS, CHOICES, UNITS, 70)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes, {len(TOOLS)} tools and {len(PIPE)} pipe tables into {PROGRAM}")


if __name__ == "__main__":
    main()
