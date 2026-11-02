#!/usr/bin/env python3
"""Write the generated block of hp-prime/CIRCUITS.txt: the tool list and the
input-box ("slot") tables of the electricity-class circuit calculator.

    python3 tools/gen_circ_tables.py

The circuits follow the diagrams used in the class homework: series,
parallel, parallel branches of two resistors in series, the combination
chain R1 - (R2 || R3) - R4 - (R5 || R6) - R7, troubleshooting the
two-branch circuit, Kirchhoff's voltage and current laws and a two-source
Kirchhoff network.  Resistor colors follow the EIA/IEC 60062 code.
"""
import os

from ppltables import check_slots, choice_slot, slot, slot_functions, slot_globals, write_block

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "CIRCUITS.txt")

COLORS = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray", "White"]
CHOICES = {
    1: COLORS,
    2: COLORS + ["Gold", "Silver"],                       # multiplier band
    3: ["Brown 1%", "Red 2%", "Green 0.5%", "Blue 0.25%", "Violet 0.1%", "Gray 0.05%",
        "Gold 5%", "Silver 10%", "None 20%"],
    4: ["4 bands", "5 bands"],
    5: ["+ up (aiding)", "+ down (opposing)"],
    6: ["pico (p)", "nano (n)", "micro (µ)", "milli (m)", "(none)", "kilo (k)", "mega (M)", "giga (G)"],
    7: ["In 1", "In 2", "In 3", "In 4", "Out 1", "Out 2", "Out 3", "Out 4", "None: check"],
}

S = slot
C = choice_slot(CHOICES, None, 0)


def R(num, label, default, hlp="Resistance, 0 = not used"):
    return S(num, label, "Ω", -1, 10, 0, 1e9, default, hlp, blank=1)


SLOTS = [
    # series
    S(1, "ET", "V", -1, 1, 0, 1e7, 0, "Source voltage (0 if unknown)", blank=2),
    S(2, "IT", "A", -1, 0.01, 0, 1e6, 1, "Total current (0 if unknown)", blank=2),
    R(3, "R1", 10), R(4, "R2", 20), R(5, "R3", 30), R(6, "R4", 40), R(7, "R5", 50),
    R(8, "R6", 40), R(9, "R7", 50),
    # parallel
    S(10, "ET", "V", -1, 1, 0, 1e7, 120, "Source voltage (0 if unknown)", blank=2),
    S(11, "IT", "A", -1, 0.01, 0, 1e6, 0, "Total current (0 if unknown)", blank=2),
    R(12, "R1", 470), R(13, "R2", 360), R(14, "R3", 510), R(15, "R4", 430), R(16, "R5", 0),
    R(17, "R6", 0), R(18, "R7", 0),
    # series-parallel: branches of two in series
    S(19, "ET", "V", -1, 1, 0, 1e7, 0, "Source voltage (0 if unknown)", blank=2),
    S(20, "IT", "A", -1, 0.01, 0, 1e6, 0.6, "Total current (0 if unknown)", blank=2),
    R(21, "R1", 470, "Branch A top (0 = wire)"), R(22, "R2", 360, "Branch A bottom (0 = wire)"),
    R(23, "R3", 510, "Branch B top (0 = wire)"), R(24, "R4", 430, "Branch B bottom (0 = wire)"),
    R(25, "R5", 0, "Branch C top (0 = no branch C)"), R(26, "R6", 0, "Branch C bottom"),
    # combination chain
    S(27, "ET", "V", -1, 1, 0, 1e7, 63, "Source voltage (0 if unknown)", blank=2),
    S(28, "IT", "A", -1, 0.001, 0, 1e6, 0, "Total current (0 if unknown)", blank=2),
    R(29, "R1", 1000, "Series, before the 1st pair (0 = wire)"),
    R(30, "R2", 2200, "1st parallel pair (0 = none)"), R(31, "R3", 1800, "1st parallel pair (0 = none)"),
    R(32, "R4", 910, "Series, between the pairs (0 = wire)"),
    R(33, "R5", 3300, "2nd parallel pair (0 = none)"), R(34, "R6", 4300, "2nd parallel pair (0 = none)"),
    R(35, "R7", 860, "Series, after the 2nd pair (0 = wire)"),
    # troubleshooting
    S(36, "ET", "V", -1, 1, 0, 1e7, 12, "Source voltage"),
    S(37, "IT meas.", "A", -1, 0.001, 0, 1e6, 0.015, "Measured total current (15 mA = 0.015)", blank=2),
    R(38, "R1", 270, "Branch A top"), R(39, "R2", 510, "Branch A bottom"),
    R(40, "R3", 470, "Branch B top"), R(41, "R4", 330, "Branch B bottom"),
    S(42, "E1 meas.", "V", -1, 0.1, 0, 1e7, 12, "Voltmeter across R1"),
    S(43, "E2 meas.", "V", -1, 0.1, 0, 1e7, 0, "Voltmeter across R2"),
    S(44, "E3 meas.", "V", -1, 0.1, 0, 1e7, 7, "Voltmeter across R3"),
    S(45, "E4 meas.", "V", -1, 0.1, 0, 1e7, 5, "Voltmeter across R4"),
    # Kirchhoff's voltage law
    S(46, "ET", "V", -1, 1, 0, 1e7, 120, "Source voltage (0 if unknown)", blank=2),
    S(47, "Resistors", "", 0, 1, 1, 7, 5, "How many resistors in the loop"),
] + [S(48 + k, f"E{k + 1}", "V", -1, 1, 0, 1e7, v, "Voltage drop (0 = the unknown one)", blank=2)
     for k, v in enumerate([35, 28, 22, 15, 0, 0, 0])] + [
    # Kirchhoff's current law
] + [S(55 + k, f"In {k + 1}", "A", -1, 0.1, 0, 1e6, v, "Current into the junction (0 = unknown)", blank=2)
     for k, v in enumerate([3, 2, 0, 0])] + [
    S(59 + k, f"Out {k + 1}", "A", -1, 0.1, 0, 1e6, v, "Current out of the junction (0 = unknown)", blank=2)
    for k, v in enumerate([4, 0, 0, 0])] + [
    # two-source network
    S(63, "E1", "V", -1, 1, 0, 1e7, 12, "Left source voltage"),
    S(64, "E2", "V", -1, 1, 0, 1e7, 6, "Right source voltage"),
    C(65, "E2 polarity", 5, 1, "Right source + toward the top node?"),
    R(66, "R1", 4, "Left resistor (in series with E1)"),
    R(67, "R2", 2, "Right resistor (in series with E2)"),
    R(68, "R3", 6, "Middle resistor (top node to bottom)"),
    # Ohm's law and power
    S(69, "Volts E", "V", -1, 1, 0, 1e9, 48, "Voltage (0 if unknown)", blank=2),
    S(70, "Amps I", "A", -1, 0.1, 0, 1e9, 0, "Current (0 if unknown)", blank=2),
    S(71, "Ohms R", "Ω", -1, 1, 0, 1e12, 0, "Resistance (0 if unknown)", blank=2),
    S(72, "Watts P", "W", -1, 1, 0, 1e12, 96, "Power (0 if unknown)", blank=2),
    # dividers
    S(73, "ET", "V", -1, 1, 0, 1e7, 12, "Voltage across the pair in series"),
    S(74, "IT", "A", -1, 0.01, 0, 1e6, 0.6, "Current into the pair in parallel"),
    R(75, "R1", 470, "First resistor"), R(76, "R2", 360, "Second resistor"),
    # color code
    C(77, "Bands", 4, 1, "4-band or 5-band resistor"),
    C(78, "Band 1", 1, 5, "First digit"),
    C(79, "Band 2", 1, 8, "Second digit"),
    C(80, "Band 3", 1, 1, "Third digit (5-band resistors only)"),
    C(81, "Multiplier", 2, 3, "Multiplier band"),
    C(82, "Tolerance", 3, 7, "Tolerance band"),
    # prefixes
    S(83, "Value", "", -1, 1, -1e15, 1e15, 15, "Number to convert"),
    C(84, "Prefix", 6, 4, "Prefix of that number (15 mA: milli)"),
    # Kirchhoff's current law: which current is the unknown
    C(85, "Unknown", 7, 6, "Which current to solve for"),
]

TOOLS = [
    ("Series circuit", "Series", "circuit", 1, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ("Parallel circuit", "Parallel", "circuit", 1, [10, 11, 12, 13, 14, 15, 16, 17, 18]),
    ("Series-parallel", "Series-", "parallel", 1, [19, 20, 21, 22, 23, 24, 25, 26]),
    ("Combination", "Combi-", "nation", 1, [27, 28, 29, 30, 31, 32, 33, 34, 35]),
    ("Troubleshoot", "Trouble-", "shoot", 2, [36, 37, 38, 39, 40, 41, 42, 43, 44, 45]),
    ("Kirchhoff voltage", "KVL", "voltage", 2, list(range(46, 55))),
    ("Kirchhoff current", "KCL", "current", 2, [85] + list(range(55, 63))),
    ("Two-source network", "Kirchhoff", "2 sources", 2, [63, 64, 65, 66, 67, 68]),
    ("Ohm's law / power", "Ohm's", "law", 3, [69, 70, 71, 72]),
    ("Dividers", "Dividers", "", 3, [73, 74, 75, 76]),
    ("Color code", "Color", "code", 3, [77, 78, 79, 80, 81, 82]),
    ("Metric prefixes", "Prefixes", "mA kΩ", 3, [83, 84]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=len(TOOLS), max_ins=10)   # one column of boxes
    for t in TOOLS:
        assert len(t[4]) <= 10, t[0]


def main():
    check()
    out = ["// ---- BEGIN TABLES (generated by tools/gen_circ_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [l.replace("two per row", "one column down the left") for l in slot_functions(TOOLS, CHOICES, None, 0)]
    out += ["// ---- END TABLES ----"]
    write_block(PROGRAM, "\n".join(out))
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
