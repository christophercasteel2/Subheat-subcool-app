#!/usr/bin/env python3
"""Write the generated block of hp-prime/ELECREV.txt: the tool list, the
input-box ("slot") tables and the wire tables of the electricity exam
review app (Unit 9 Kirchhoff, Thevenin, Norton and superposition; Unit 11
conductors; Unit 13 batteries and other small sources).

    python3 tools/gen_rev_tables.py

The ampacity and correction tables are the ones NECCALC uses (Table
310.15(B)(16)/(17) and the ambient correction factors; the same values as
the textbook's 2014 tables).  The circular mil areas and the resistivity
(K) of materials are the textbook's own tables (Figures 11-16 and 11-17).
"""
import os

from gen_nec_tables import CORR, INSULATION, SIZES, T16, T17
from ppltables import check_slots, choice_slot, plist, pmatrix, slot, slot_functions, slot_globals, write_block

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "ELECREV.txt")

# textbook Figure 11-17 American Wire Gauge table (circular mils), then kcmil
BOOK_CM = [1624, 2583, 4107, 6530, 10380, 16510, 26250, 41740, 52630, 66370, 83690,
           105500, 133100, 167800, 211600] + [int(s) * 1000 for s in SIZES[15:]]
# textbook Figure 11-16: ohms-CM per foot at 20 C, temperature coefficient
MATERIALS = [("Aluminum", 17, 0.004), ("Carbon", 22000, -0.0004), ("Constantan", 295, 0.000002),
             ("Copper", 10.4, 0.0039), ("Gold", 14, 0.004), ("Iron", 60, 0.0055),
             ("Lead", 126, 0.0043), ("Manganin", 265, 0.0), ("Mercury", 590, 0.00088),
             ("Nichrome", 675, 0.0002), ("Nickel", 52, 0.005), ("Platinum", 66, 0.0036),
             ("Silver", 9.6, 0.0038), ("Tungsten", 33.8, 0.005)]
SIZE_NAMES = [s + (" kcmil" if i >= 15 else " AWG") for i, s in enumerate(SIZES)]
INS_NAMES = [n + " " + ("60" if c == 1 else "75" if c == 2 else "90" if c == 3 else "NM") + "°C"
             if c < 4 else n for n, c, _ in INSULATION]

CHOICES = {
    1: ["In 1", "In 2", "In 3", "In 4", "Out 1", "Out 2", "Out 3", "Out 4", "None: check"],
    2: ["Same as E1 (aid)", "Opposite E1"],
    3: ["Thevenin ETH RTH", "Norton IN RN"],
    4: ["R (ohms)", "CM (wire size)", "L (length)", "K (material)"],
    5: [m[0] for m in MATERIALS] + ["Custom K"],
    6: SIZE_NAMES + ["Custom CM"],
    7: ["1-phase / DC", "3-phase"],
    8: ["Copper", "Aluminum"],
    9: INS_NAMES,
    10: ["Raceway (B)(16)", "Free air (B)(17)"],
    11: ["°F", "°C"],
    12: ["Amps", "Watts 1ph/DC", "kW 1ph/DC", "hp 1ph/DC", "Watts 3-ph", "kW 3-ph", "hp 3-ph"],
    13: ["Yes x 1.25", "No"],
    14: ["Unknown", "60°C", "75°C", "90°C"],
    15: ["mA-hr", "A-hr"],
    16: ["mA", "A"],
    17: SIZE_NAMES,
    18: [m[0] for m in MATERIALS],
}

S = slot
C = choice_slot(CHOICES, None, 0)


def N(num, label, unit, default, hlp, blank=0, lo=0, hi=1e9):
    return S(num, label, unit, -1, 1, lo, hi, default, hlp, blank=blank)


SLOTS = [
    # 1 KCL
    C(1, "Unknown", 1, 9, "Which current to solve for"),
] + [N(2 + k, f"In {k + 1}", "A", v, "Current into the point (0 = unknown)", 2)
     for k, v in enumerate([4, 6, 0, 0])] + [
    N(6 + k, f"Out {k + 1}", "A", v, "Current leaving the point (0 = unknown)", 2)
    for k, v in enumerate([10, 0, 0, 0])] + [
    # 2 KVL
    N(10, "ET", "V", 120, "Source voltage (0 if unknown)", 2),
    S(11, "Drops", "", 0, 1, 1, 7, 5, "How many voltage drops in the loop"),
] + [N(12 + k, f"E{k + 1}", "V", v, "Voltage drop (0 = the unknown one)", 2)
     for k, v in enumerate([32, 18, 24, 6, 0, 0, 0])] + [
    # 3 two-source network
    N(19, "Es1", "V", 24, "Left source voltage"),
    N(20, "Es2", "V", 10, "Right source voltage"),
    C(21, "Es2 is", 2, 1, "Es2 turned the same way as Es1?"),
    N(22, "R1", "Ω", 330, "Left resistor (with Es1)"),
    N(23, "R2", "Ω", 200, "Right resistor (with Es2)"),
    N(24, "R3", "Ω", 100, "Middle resistor (top to bottom)"),
    # 18 Ohm's law
    N(25, "Volts E", "V", 24, "Voltage (0 if unknown)", 2),
    N(26, "Amps I", "A", 3, "Current (0 if unknown)", 2),
    N(27, "Ohms R", "Ω", 0, "Resistance (0 if unknown)", 2),
    N(28, "Watts P", "W", 0, "Power (0 if unknown)", 2),
    # 4 Thevenin / Norton of a circuit
    N(29, "Es", "V", 24, "Source voltage"),
    N(30, "R1", "Ω", 2, "Series resistor (source to A)"),
    N(31, "R2", "Ω", 6, "Resistor across terminals A-B"),
    N(32, "R3", "Ω", 0, "Extra series R to terminal A (0 none)", 1),
    N(33, "RL", "Ω", 10, "Load across A-B (0 = no load)", 1),
    # 5 equivalent with a load
    C(34, "Given", 3, 1, "Which equivalent you have"),
    N(35, "ETH / IN", "", 18, "ETH volts, or IN amps"),
    N(36, "RTH / RN", "Ω", 1.5, "RTH or RN"),
    N(37, "RL", "Ω", 10, "Load resistance"),
    # 6 superposition
    N(38, "Es1", "V", 24, "Left source"),
    N(39, "R1", "Ω", 600, "Left resistor (with Es1)"),
    N(40, "R2", "Ω", 300, "Middle resistor (find its current)"),
    N(41, "R3", "Ω", 1200, "Right resistor (with Es2)"),
    N(42, "Es2", "V", 12, "Right source"),
    C(43, "Es2 is", 2, 1, "Es2 turned the same way as Es1?"),
    # 7 wire resistance R = KL/CM
    C(44, "Find", 4, 1, "Which value to work out"),
    C(45, "Material", 5, 4, "Sets K (ohms-CM per ft at 20°C)"),
    N(46, "K custom", "", 10.4, "K when Material = Custom K"),
    C(47, "Size", 6, 7, "Wire size (sets CM)"),
    N(48, "CM custom", "CM", 26250, "CM when Size = Custom CM"),
    N(49, "Length L", "ft", 550, "Length of wire, ft"),
    N(50, "R", "Ω", 0.218, "Resistance (when finding CM, L or K)"),
    N(51, "Temp", "°C", 20, "Wire temperature, °C (K is at 20°C)", 0, -100, 1000),
    # 8 voltage drop
    C(52, "Phase", 7, 1, "Single-phase (2 KIL) or 3-phase (1.732 KIL)"),
    C(53, "Material", 5, 4, "Conductor material (K)"),
    C(54, "Size", 6, 5, "Conductor size (CM)"),
    N(55, "CM custom", "CM", 10380, "CM when Size = Custom CM"),
    N(56, "Amps I", "A", 24, "Load current"),
    N(57, "Length", "ft", 250, "One-way distance to the load, ft"),
    N(58, "Volts", "V", 240, "Source voltage (for % drop)", 1),
    # 9 conductor size for a long run
    C(59, "Phase", 7, 1, "Single-phase or 3-phase"),
    C(60, "Material", 5, 1, "Conductor material (K)"),
    N(61, "Volts", "V", 480, "Source voltage"),
    N(62, "Max drop", "%", 3, "Allowed voltage drop, percent"),
    N(63, "Amps I", "A", 86, "Load current"),
    N(64, "Length", "ft", 2800, "One-way distance to the load, ft"),
    C(65, "Parallel", 17, 15, "Size for parallel conductors"),
    # 10 ampacity with correction
    C(66, "Size", 17, 5, "Conductor size"),
    C(67, "Material", 8, 1, "Copper or aluminum"),
    C(68, "Insulat.", 9, 5, "Insulation type (sets the column)"),
    C(69, "Table", 10, 2, "Raceway/cable, or single in free air"),
    N(70, "Ambient", "", 40, "Ambient temperature", 0, -40, 400),
    C(71, "Amb. unit", 11, 2, "Unit of the ambient temperature"),
    S(72, "Conduct.", "", 0, 1, 1, 200, 1, "Current-carrying conductors together"),
    # 11 conductor for a load
    N(73, "Load", "", 50, "Load: amps, watts, kW or hp"),
    C(74, "Load is", 12, 3, "Unit of the load (and phase)"),
    N(75, "Volts", "V", 480, "Supply voltage"),
    C(76, "Contin.", 13, 1, "Continuous (3 h or more): x 1.25"),
    C(77, "Insulat.", 9, 18, "Insulation type"),
    C(78, "Material", 8, 1, "Copper or aluminum"),
    N(79, "Ambient", "", 125, "Ambient temperature", 0, -40, 400),
    C(80, "Amb. unit", 11, 1, "Unit of the ambient temperature"),
    S(81, "Conduct.", "", 0, 1, 1, 200, 3, "Current-carrying conductors in raceway"),
    C(82, "Termin.", 14, 1, "Termination temperature rating"),
    # 12 temperature coefficient
    C(83, "Material", 18, 4, "Conductor material"),
    C(84, "Size", 17, 2, "Wire size"),
    N(85, "Length", "ft", 250, "Length, ft"),
    N(86, "Temp", "", 87, "Conductor temperature", 0, -100, 2000),
    C(87, "Temp unit", 11, 2, "Unit of that temperature"),
    # 13 NEC 310.15(C) formula
    N(88, "TC", "°C", 90, "Conductor temperature, °C"),
    N(89, "TA", "°C", 20, "Ambient temperature, °C", 0, -50, 500),
    N(90, "ΔTD", "°C", 0, "Dielectric loss temperature rise", 0, -100, 500),
    N(91, "RDC", "", 25.7, "DC resistance at TC, microhm per ft"),
    N(92, "YC", "", 0.01, "AC component: skin and proximity"),
    N(93, "RCA", "", 60, "Thermal resistance, °C-cm/watt"),
    # 14 battery bank
    N(94, "Each V", "V", 12, "Voltage of one cell or battery"),
    N(95, "Each Ah", "Ah", 60, "Ampere-hours of one"),
    S(96, "In series", "", 0, 1, 1, 10000, 2, "How many in series in each string"),
    S(97, "Strings", "", 0, 1, 1, 10000, 2, "How many strings in parallel"),
    # 15 cells needed
    N(98, "Cell V", "V", 0.5, "Voltage of one cell (solar 0.5 V)"),
    N(99, "Cell A", "A", 0.25, "Current of one cell (or Ah)"),
    N(100, "Need V", "V", 14, "Voltage needed"),
    N(101, "Need A", "A", 0.5, "Current (or Ah) needed"),
    # 16 capacity and run time
    N(102, "Capacity", "", 10000, "Capacity rating"),
    C(103, "Cap. unit", 15, 1, "mA-hr or A-hr"),
    N(104, "Volts", "V", 1.5, "Cell or battery voltage"),
    N(105, "Load", "", 100, "Load current (0 = none)", 1),
    C(106, "Load unit", 16, 1, "mA or A"),
    # 17 internal resistance
    N(107, "V no load", "V", 1.5, "Open-circuit (no-load) voltage"),
    N(108, "V loaded", "V", 0.5, "Terminal voltage with the current"),
    N(109, "Current", "A", 4.5, "Current flowing (short: ammeter)"),
]

TOOLS = [
    ("Kirchhoff current", "KCL", "current", 1, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ("Kirchhoff voltage", "KVL", "voltage", 1, list(range(10, 19))),
    ("Two-source network", "Kirchhoff", "2 sources", 1, [19, 20, 21, 22, 23, 24]),
    ("Thevenin / Norton", "Thevenin", "Norton", 1, [29, 30, 31, 32, 33]),
    ("Equivalent + load", "Equiv.", "+ load", 1, [34, 35, 36, 37]),
    ("Superposition", "Super-", "position", 1, [38, 39, 40, 41, 42, 43]),
    ("Wire R = KL/CM", "Wire R", "K L / CM", 2, [44, 45, 46, 47, 48, 49, 50, 51]),
    ("Voltage drop", "Voltage", "drop", 2, [52, 53, 54, 55, 56, 57, 58]),
    ("Size for long run", "Long run", "wire size", 2, [59, 60, 61, 62, 63, 64, 65]),
    ("Ampacity derating", "Ampacity", "derate", 2, [66, 67, 68, 69, 70, 71, 72]),
    ("Conductor for load", "Wire for", "a load", 2, [73, 74, 75, 76, 77, 78, 79, 80, 81, 82]),
    ("Temp coefficient", "Temp", "coeff.", 2, [83, 84, 85, 86, 87]),
    ("NEC 310.15(C)", "310.15(C)", "formula", 2, [88, 89, 90, 91, 92, 93]),
    ("Battery bank", "Battery", "bank", 3, [94, 95, 96, 97]),
    ("Cells needed", "Cells", "needed", 3, [98, 99, 100, 101]),
    ("Capacity / run time", "Capacity", "run time", 3, [102, 103, 104, 105, 106]),
    ("Internal resistance", "Internal", "resist.", 3, [107, 108, 109]),
    ("Ohm's law / power", "Ohm's", "law", 3, [25, 26, 27, 28]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=len(TOOLS), max_ins=10)
    assert len(BOOK_CM) == len(SIZES) == 30


def main():
    check()
    out = ["// ---- BEGIN TABLES (generated by tools/gen_rev_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [l.replace("two per row", "one column down the left") for l in slot_functions(TOOLS, CHOICES, None, 0)]
    out += [
        "// textbook AWG table (Figure 11-17): circular mils of each size",
        "gCM:=" + plist(BOOK_CM) + ";",
        "// textbook resistivity table (Figure 11-16): K at 20 C and temperature coefficient",
        "gK:=" + plist([m[1] for m in MATERIALS]) + ";",
        "gAl:=" + plist([m[2] for m in MATERIALS]) + ";",
        "// Table 310.15(B)(16) and (B)(17): rows Cu 60/75/90 C, Al 60/75/90 C; 0 = not listed",
        "gA16:=" + pmatrix([T16[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "gA17:=" + pmatrix([T17[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "// ambient correction: tops of the 5 C bands, factors for 60/75/90 C (0 = not allowed)",
        "gAmbTop:={10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85};",
        "gCorr:=" + pmatrix(CORR) + ";",
        "// insulation column: 1 60 C, 2 75 C, 3 90 C, 4 NM cable",
        "gInsCol:=" + plist([c for _, c, _ in INSULATION]) + ";",
    ]
    out += ["// ---- END TABLES ----"]
    write_block(PROGRAM, "\n".join(out))
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
