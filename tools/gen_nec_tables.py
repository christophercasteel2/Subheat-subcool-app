#!/usr/bin/env python3
"""Write the generated block of hp-prime/NECCALC.txt: the tool list, the
input-box ("slot") tables and the NEC tables of the class calculator.

Edit the tables here, not in the program, then run
    python3 tools/gen_nec_tables.py

NEC tables (2020/2023 numbering; values unchanged from the 2017 edition)
  310.16  ampacity, raceway / cable / earth, 18 AWG - 2000 kcmil
  310.17  ampacity, single conductors in free air
          both copied from Omnicable's reproduction of the 2017 tables
  310.15(B)(1) ambient correction factors: the code's equation at the top
          of each 5 C band, rounded to 2 places (this reproduces the table)
  310.15(C)(1) adjustment for more than 3 current-carrying conductors
  Chapter 9 Table 1 (fill %), Table 4 (raceway area), Table 5 (conductor
          area), Table 8 (circular mils, dc resistance at 75 C)
  240.6(A) standard ratings, 240.4(D) small conductors
  314.16(B) box fill volume per conductor
"""
import math
import os

from ppltables import (check_slots, choice_slot, plist, pmatrix, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "NECCALC.txt")

# ---------------------------------------------------------------------------
# conductor sizes (choice list 10) and their tables

SIZES = ["18", "16", "14", "12", "10", "8", "6", "4", "3", "2", "1", "1/0", "2/0",
         "3/0", "4/0", "250", "300", "350", "400", "500", "600", "700", "750", "800",
         "900", "1000", "1250", "1500", "1750", "2000"]
CMIL = [1620, 2580, 4110, 6530, 10380, 16510, 26240, 41740, 52620, 66360, 83690,
        105600, 133100, 167800, 211600] + [int(s) * 1000 for s in SIZES[15:]]

# Table 310.16 (raceway, cable or earth), Table 310.17 (free air): 0 = not listed
T16 = {
    ("Cu", 60): [0, 0, 15, 20, 30, 40, 55, 70, 85, 95, 110, 125, 145, 165, 195, 215, 240, 260, 280, 320, 350, 385, 400, 410, 435, 455, 495, 525, 545, 555],
    ("Cu", 75): [0, 0, 20, 25, 35, 50, 65, 85, 100, 115, 130, 150, 175, 200, 230, 255, 285, 310, 335, 380, 420, 460, 475, 490, 520, 545, 590, 625, 650, 665],
    ("Cu", 90): [14, 18, 25, 30, 40, 55, 75, 95, 115, 130, 145, 170, 195, 225, 260, 290, 320, 350, 380, 430, 475, 520, 535, 555, 585, 615, 665, 705, 735, 750],
    ("Al", 60): [0, 0, 0, 15, 25, 35, 40, 55, 65, 75, 85, 100, 115, 130, 150, 170, 195, 210, 225, 260, 285, 315, 320, 330, 355, 375, 405, 435, 455, 470],
    ("Al", 75): [0, 0, 0, 20, 30, 40, 50, 65, 75, 90, 100, 120, 135, 155, 180, 205, 230, 250, 270, 310, 340, 375, 385, 395, 425, 445, 485, 520, 545, 560],
    ("Al", 90): [0, 0, 0, 25, 35, 45, 55, 75, 85, 100, 115, 135, 150, 175, 205, 230, 260, 280, 305, 350, 385, 425, 435, 445, 480, 500, 545, 585, 615, 630],
}
T17 = {
    ("Cu", 60): [0, 0, 25, 30, 40, 60, 80, 105, 120, 140, 165, 195, 225, 260, 300, 340, 375, 420, 455, 515, 575, 630, 655, 680, 730, 780, 890, 980, 1070, 1155],
    ("Cu", 75): [0, 0, 30, 35, 50, 70, 95, 125, 145, 170, 195, 230, 265, 310, 360, 405, 445, 505, 545, 620, 690, 755, 785, 815, 870, 935, 1065, 1175, 1280, 1385],
    ("Cu", 90): [18, 24, 35, 40, 55, 80, 105, 140, 165, 190, 220, 260, 300, 350, 405, 455, 500, 570, 615, 700, 780, 850, 885, 920, 980, 1055, 1200, 1325, 1445, 1560],
    ("Al", 60): [0, 0, 0, 25, 35, 45, 60, 80, 95, 110, 130, 150, 175, 200, 235, 265, 290, 330, 355, 405, 455, 500, 515, 535, 580, 625, 710, 795, 875, 960],
    ("Al", 75): [0, 0, 0, 30, 40, 55, 75, 100, 115, 135, 155, 180, 210, 240, 280, 315, 350, 395, 425, 485, 545, 595, 620, 645, 700, 750, 855, 950, 1050, 1150],
    ("Al", 90): [0, 0, 0, 35, 45, 60, 85, 115, 130, 150, 175, 205, 235, 270, 315, 355, 395, 445, 480, 545, 615, 670, 700, 725, 790, 845, 965, 1070, 1185, 1295],
}
# Chapter 9 Table 8, dc resistance at 75 C, ohms per 1000 ft (stranded;
# 0 = not used here)
R8 = {
    "Cu": [8.08, 5.08, 3.14, 1.98, 1.24, 0.778, 0.491, 0.308, 0.245, 0.194, 0.154, 0.122,
           0.0967, 0.0766, 0.0608, 0.0515, 0.0429, 0.0367, 0.0321, 0.0258, 0.0214, 0.0184,
           0.0171, 0.0161, 0.0143, 0.0129, 0.0103, 0.00858, 0.00735, 0.00643],
    "Al": [0, 0, 0, 3.25, 2.04, 1.28, 0.808, 0.508, 0.403, 0.319, 0.253, 0.201, 0.159,
           0.126, 0.100, 0.0847, 0.0707, 0.0605, 0.0529, 0.0424, 0.0353, 0.0303, 0.0282,
           0.0265, 0.0235, 0.0212, 0.0169, 0.0141, 0.0121, 0.0106],
}

# insulation types (choice list 11): label, temperature column 1 60 C,
# 2 75 C, 3 90 C, 4 = NM cable (90 C wire, 60 C ampacity, 334.80);
# Table 5 group for conduit fill (0 = not in the fill tables here)
INSULATION = [
    ("TW", 1, 3), ("UF", 1, 0), ("RHW", 2, 4), ("THHW wet", 2, 3), ("THW", 2, 3),
    ("THWN", 2, 1), ("XHHW wet", 2, 2), ("USE", 2, 0), ("ZW", 2, 0), ("TBS", 3, 0),
    ("SA", 3, 0), ("SIS", 3, 0), ("FEP", 3, 5), ("FEPB", 3, 5), ("MI", 3, 0),
    ("RHH", 3, 4), ("RHW-2", 3, 4), ("THHN", 3, 1), ("THHW dry", 3, 3), ("THW-2", 3, 3),
    ("THWN-2", 3, 1), ("USE-2", 3, 2), ("XHH", 3, 2), ("XHHW dry", 3, 2), ("XHHW-2", 3, 2),
    ("ZW-2", 3, 0), ("NM-B cable", 4, 0),
]

# Table 310.15(B)(1): top of each ambient band, C
AMB_TOP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]


def corr_factor(top, tc):
    if top >= tc:
        return 0
    # the code's equation, rounded as the table prints it
    f = math.sqrt((tc - top) / (tc - 30))
    return round(f + 1e-9, 2)


CORR = [[corr_factor(t, tc) for t in AMB_TOP] for tc in (60, 75, 90)]
# spot values as printed in the table, typed separately
CORR_CHECK = {(60, 40): 0.82, (75, 40): 0.88, (90, 40): 0.91, (75, 45): 0.82,
              (90, 50): 0.82, (60, 55): 0.41, (75, 70): 0.33, (90, 85): 0.29,
              (60, 10): 1.29, (75, 20): 1.11, (90, 35): 0.96}

# conduit fill: Table 5 sizes 14 AWG - 500 kcmil (choice list 16)
FILL_SIZES = SIZES[2:20]
FILL_AREA = [  # in2; 0 = not listed for that group here
    [0.0097, 0.0133, 0.0211, 0.0366, 0.0507, 0.0824, 0.0973, 0.1158, 0.1562, 0.1855,
     0.2223, 0.2679, 0.3237, 0.3970, 0.4608, 0.5242, 0.5863, 0.7073],     # THHN, THWN, THWN-2
    [0.0139, 0.0181, 0.0243, 0.0437, 0.0590, 0.0814, 0.0962, 0.1146, 0.1534, 0.1825,
     0.2190, 0.2642, 0.3197, 0.3904, 0.4536, 0.5166, 0.5782, 0.6984],     # XHHW, XHHW-2, XHH, USE-2
    [0.0139, 0.0181, 0.0243, 0.0437, 0.0726, 0.0973, 0.1134, 0.1333, 0.1901, 0.2223,
     0.2624, 0.3117, 0.3718, 0.4596, 0.5281, 0.5958, 0.6619, 0.7901],     # TW, THW, THHW, THW-2
    [0.0209, 0.0260, 0.0333, 0.0556, 0.0726, 0.0973, 0.1134, 0.1333, 0.1901, 0.2223,
     0.2624, 0.3117, 0.3718, 0.4596, 0.5281, 0.5958, 0.6619, 0.7901],     # RHH, RHW, RHW-2 no jacket
    [0.0100, 0.0137, 0.0191, 0.0333, 0.0468, 0.0670, 0.0804, 0.0973, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0],                                             # FEP, FEPB
]
# Table 4: total (100 %) area, in2, trade sizes of choice list 14; 0 = none
TRADE = ["3/8", "1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "3-1/2", "4", "5", "6"]
CONDUIT = [
    [0, 0.304, 0.533, 0.864, 1.496, 2.036, 3.356, 5.858, 8.846, 11.545, 14.753, 0, 0],      # EMT
    [0.116, 0.317, 0.533, 0.817, 1.277, 1.858, 3.269, 4.909, 7.069, 9.621, 12.566, 0, 0],  # FMC
    [0, 0.342, 0.586, 0.959, 1.647, 2.225, 3.630, 5.135, 7.922, 10.584, 13.631, 0, 0],     # IMC
    [0, 0.314, 0.549, 0.887, 1.526, 2.071, 3.408, 4.866, 7.499, 10.010, 12.882, 20.212, 29.158],  # RMC
    [0, 0.285, 0.508, 0.832, 1.453, 1.986, 3.291, 4.695, 7.268, 9.737, 12.554, 19.761, 28.567],   # PVC 40
    [0, 0.217, 0.409, 0.688, 1.237, 1.711, 2.874, 4.119, 6.442, 8.688, 11.258, 17.855, 25.598],   # PVC 80
]
STD_SIZES = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175,
             200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1600,
             2000, 2500, 3000, 4000, 5000, 6000]
BOX_SIZES = ["18 AWG", "16 AWG", "14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG"]
BOX_VOL = [1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 5.0]       # Table 314.16(B), in3

CHOICES = {
    1: ["°C", "°F"],
    2: ["Copper", "Aluminum"],
    3: ["1-phase", "3-phase"],
    4: ["K factor", "Table 8 R"],
    5: ["No", "Yes"],
    6: ["60°C", "75°C", "90°C"],
    8: ["not given", "60°C", "75°C", "90°C"],
    9: ["Raceway/cable", "Free air"],
    10: [s + (" kcmil" if i >= 15 else " AWG") for i, s in enumerate(SIZES)],
    11: [t[0] for t in INSULATION],
    12: ["Wires that fit", "Conduit size"],
    13: ["EMT", "FMC", "IMC", "RMC", "PVC Sch 40", "PVC Sch 80"],
    14: [t + " in" for t in TRADE],
    15: ["THHN, THWN", "XHHW, XHH", "TW, THW", "RHW no jkt", "FEP, FEPB"],
    16: [s + (" kcmil" if i >= 13 else " AWG") for i, s in enumerate(FILL_SIZES)],
    17: BOX_SIZES,
}

S = slot
C = choice_slot(CHOICES, None, 0)

SLOTS = [
    C(1, "Temp unit", 1, 1, "Unit for the ambient temperature"),
    # voltage drop
    S(2, "Amps", "A", 1, 1, 0, 100000, 20, "Load current"),
    S(3, "One-way ft", "ft", 0, 5, 1, 100000, 100, "Length from source to load, one way"),
    C(4, "Wire size", 10, 4, "Conductor size"),
    C(5, "Material", 2, 1, "Copper or aluminum"),
    C(6, "Phase", 3, 1, "Single phase (or DC) or three phase"),
    S(7, "Source V", "V", 1, 1, 1, 100000, 120, "Voltage at the source"),
    C(8, "Method", 4, 1, "K = 12.9 Cu / 21.2 Al, or Table 8 R"),
    S(9, "Max drop", "%", 1, 0.5, 0.5, 20, 3, "3% branch, 5% feeder + branch (note)"),
    # wire size
    S(10, "Load amps", "A", 1, 1, 0, 100000, 40, "Load current"),
    C(11, "Continuous", 5, 1, "3 hours or more: wire for 125%"),
    C(12, "Material", 2, 1, "Copper or aluminum"),
    C(13, "Wire rating", 6, 2, "Insulation temperature rating"),
    C(14, "Terminals", 6, 2, "Terminal rating (60°C if 100 A or less)"),
    S(15, "Ambient", "", 0, 1, -40, 200, 30, "Ambient temperature"),
    S(16, "Conductors", "", 0, 1, 1, 100, 3, "Current-carrying conductors together"),
    # ampacity
    C(17, "Wire size", 10, 8, "Conductor size"),
    C(18, "Material", 2, 1, "Copper or aluminum"),
    C(19, "Insulation", 11, 6, "Insulation type on the wire"),
    C(20, "Installed", 9, 1, "Raceway / cable / buried, or free air"),
    S(21, "Ambient", "", 0, 1, -40, 200, 30, "Ambient temperature"),
    S(22, "Conductors", "", 0, 1, 1, 100, 3, "Current-carrying conductors together"),
    C(23, "Terminals", 8, 1, "Terminal rating, if the question gives one"),
    # breaker size
    S(24, "Continuous", "A", 1, 1, 0, 100000, 16, "Continuous load, amps"),
    S(25, "Noncontin.", "A", 1, 1, 0, 100000, 0, "Noncontinuous load, amps"),
    C(26, "Wire size", 10, 4, "Conductor size"),
    C(27, "Material", 2, 1, "Copper or aluminum"),
    C(28, "Column", 6, 2, "Ampacity column (lowest rated part)"),
    # conduit fill
    C(29, "Find", 12, 1, "How many wires fit, or the conduit size"),
    C(30, "Conduit", 13, 1, "Raceway type"),
    C(31, "Trade size", 14, 3, "Raceway trade size"),
    C(32, "Insulation", 15, 1, "Insulation group (Table 5)"),
    C(33, "Wire size", 16, 2, "Size of the main wires"),
    S(34, "How many", "", 0, 1, 0, 1000, 9, "Number of those wires"),
    C(35, "2nd size", 16, 2, "Size of a second group (e.g. ground)"),
    S(36, "2nd count", "", 0, 1, 0, 1000, 0, "Number of second-group wires", blank=1),
    # AWG chart
    C(37, "Wire size", 10, 4, "Conductor size"),
    C(38, "Material", 2, 1, "Copper or aluminum"),
    C(39, "Insulation", 11, 18, "Insulation type"),
    # box fill
    C(40, "Wire size", 17, 3, "Largest conductor in the box"),
    S(41, "Conductors", "", 0, 1, 0, 100, 4, "Insulated wires entering (count each)"),
    C(42, "Clamps", 5, 2, "Any internal cable clamps (count 1)"),
    S(43, "Devices", "", 0, 1, 0, 20, 1, "Yokes: switches, receptacles (2 each)"),
    C(44, "Grounds", 5, 2, "Any equipment grounds (count 1)"),
    S(45, "Fittings", "", 0, 1, 0, 20, 0, "Fixture studs or hickeys (1 each)"),
    S(46, "Box volume", "in³", 1, 0.5, 0, 1000, 18, "Box volume (0 = skip)", blank=1),
    # Ohm's law
    S(47, "Volts (E)", "V", -1, 1, 0, 10000000, 120, "Voltage; leave 0 if unknown", blank=2),
    S(48, "Amps (I)", "A", -1, 0.1, 0, 10000000, 0, "Current; leave 0 if unknown", blank=2),
    S(49, "Ohms (R)", "Ω", -1, 1, 0, 1000000000, 12, "Resistance; leave 0 if unknown", blank=2),
    S(50, "Watts (P)", "W", -1, 10, 0, 1000000000, 0, "Power; leave 0 if unknown", blank=2),
]

# tools (tile 9, Learn, opens reference pages instead of a tool)
TOOLS = [
    ("Voltage drop", "Voltage", "drop", 1, [2, 3, 4, 5, 6, 7, 8, 9]),
    ("Wire size", "Wire", "size", 1, [10, 11, 12, 13, 14, 16, 15, 1]),
    ("Ampacity", "Ampacity", "", 2, [17, 18, 19, 20, 21, 1, 22, 23]),
    ("Breaker size", "Breaker", "size", 2, [24, 25, 26, 27, 28]),
    ("Conduit fill", "Conduit", "fill", 3, [29, 30, 31, 32, 33, 34, 35, 36]),
    ("AWG chart", "AWG", "chart", 3, [37, 38, 39]),
    ("Box fill", "Box", "fill", 4, [40, 41, 42, 43, 44, 45, 46]),
    ("Ohm's law", "Ohm's", "law", 4, [47, 48, 49, 50]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=8)
    for col in list(T16.values()) + list(T17.values()):
        assert len(col) == len(SIZES)
        nz = [a for a in col if a]
        assert nz == sorted(nz)
    assert len(CMIL) == len(SIZES) and all(len(v) == len(SIZES) for v in R8.values())
    # Table 8: resistance x area is nearly constant for each metal
    for metal, k in (("Cu", 12.9), ("Al", 21.2)):
        for r, cm in zip(R8[metal], CMIL):
            if r:
                assert abs(r * cm / 1000 / k - 1) < 0.02, (metal, r, cm)
    for (tc, top), v in CORR_CHECK.items():
        assert CORR[(60, 75, 90).index(tc)][AMB_TOP.index(top)] == v, (tc, top)
    assert all(len(g) == len(FILL_SIZES) for g in FILL_AREA)
    assert all(len(c) == len(TRADE) for c in CONDUIT)
    # conduit areas follow from round inside diameters, so each type grows
    for c in CONDUIT:
        nz = [a for a in c if a]
        assert nz == sorted(nz)


def build_block():
    out = ["// ---- BEGIN TABLES (generated by tools/gen_nec_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// conductor sizes: circular mils, Table 8 dc resistance (ohm/kft, 75 C)",
        "gCM:=" + plist(CMIL) + ";",
        "gR8:=" + pmatrix([R8["Cu"], R8["Al"]]) + ";",
        "// Table 310.16 then 310.17: rows Cu 60/75/90 C, Al 60/75/90 C; 0 = not listed",
        "gA16:=" + pmatrix([T16[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "gA17:=" + pmatrix([T17[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "// insulation types: temperature column (4 = NM cable) and Table 5 group",
        "gInsCol:=" + plist([t[1] for t in INSULATION]) + ";",
        "gInsGrp:=" + plist([t[2] for t in INSULATION]) + ";",
        "// Table 310.15(B)(1): top of each ambient band (C), factors for 60/75/90 C",
        "gAmbTop:=" + plist(AMB_TOP) + ";",
        "gCorr:=" + pmatrix(CORR) + ";",
        "// Chapter 9 Table 5 areas (in2) by group, 14 AWG - 500 kcmil",
        "gFill:=" + pmatrix(FILL_AREA) + ";",
        "// Chapter 9 Table 4 total areas (in2) by raceway and trade size",
        "gCond:=" + pmatrix(CONDUIT) + ";",
        "gStd:=" + plist(STD_SIZES) + ";",
        "gBoxV:=" + plist(BOX_VOL) + ";",
        "",
    ]
    out += slot_functions(TOOLS, CHOICES, None, 0)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
