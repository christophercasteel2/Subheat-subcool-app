#!/usr/bin/env python3
"""Write the generated block of hp-prime/GEOMETRY.txt: the tool list and the
input-box ("slot") tables of the plane geometry app (Chapter 8, Practical
Plane Geometry: angles, polygons and quadrilaterals, triangles, hexagons,
irregular figures and circles).

    python3 tools/gen_geom_tables.py

Lengths are typed in the unit chosen in each tool's Unit box; gUS(s) names
the box holding the unit of box s (0 = none), so the boxes and answers show
it.  Angles are in degrees, typed as degrees, minutes and seconds where the
book uses them.
"""
import os

from ppltables import check_slots, choice_slot, plist, slot, slot_functions, slot_globals, write_block

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "GEOMETRY.txt")

LENGTHS = ["in", "ft", "yd", "mm", "cm", "m"]
AMOUNTS = ["sq in", "sq ft", "sq yd", "sq m", "acre", "in", "ft", "yd", "m"]
CHOICES = {
    1: LENGTHS,
    2: ["A + B", "A - B", "A x n", "A ÷ n", "180° - (A + B)", "90° - A", "180° - A", "A only"],
    3: ["1 top, upper left", "2 top, upper right", "3 top, lower left", "4 top, lower right",
        "5 bottom, upper left", "6 bottom, upper right", "7 bottom, lower left",
        "8 bottom, lower right"],
    4: ["A and B", "Apex A (isosceles)"],
    5: AMOUNTS,
    6: ["Side", "Across flats", "Across corners", "Perimeter", "Area"],
    7: ["Add", "Subtract"],
    8: ["Radius", "Diameter", "Circumference", "Area"],
    9: ["π (exact)", "3.14", "3.1416", "22/7"],
    10: ["sq in", "sq ft", "sq yd", "sq m", "acre"],
    11: ["2.598 s² (exact)", "2.6 s² (handout)"],
    12: ["Side", "Perimeter", "Area", "Height"],
    13: ["Rectangle L x W", "Square s", "Triangle b x h", "Circle r", "Hexagon s",
         "Equilateral s", "None"],
}

S = slot
C = choice_slot(CHOICES, None, 0)


def U(num, default=2):
    return C(num, "Unit", 1, default, "Unit of the lengths")


def L(num, label, default, hlp, blank=0):
    """a length in the tool's unit"""
    return S(num, label, "L", -1, 1, 0, 1e9, default, hlp, blank=blank)


def D(num, label, default, hlp, hi=360):
    return S(num, label, "°", -1, 1, 0, hi, default, hlp)


def M(num, label, default, hlp):
    return S(num, label, "'", -1, 1, 0, 59.9999, default, hlp)


SLOTS = [
    # 1 angle arithmetic (degrees, minutes, seconds)
    D(1, "A deg", 109, "Angle A: degrees", hi=100000),
    M(2, "A min", 43, "Angle A: minutes (0-59)"),
    S(3, "A sec", "''", -1, 1, 0, 59.9999, 0, "Angle A: seconds (0-59)"),
    C(4, "Do", 2, 1, "What to work out"),
    D(5, "B deg", 25, "Angle B: degrees", hi=100000),
    M(6, "B min", 32, "Angle B: minutes (0-59)"),
    S(7, "B sec", "''", -1, 1, 0, 59.9999, 0, "Angle B: seconds (0-59)"),
    S(8, "n", "", -1, 1, 0, 1e6, 2, "Multiply or divide A by n"),
    # 2 angle facts
    D(9, "Angle x", 125, "The angle you know", hi=360),
    S(10, "Parts n", "", 0, 1, 1, 1000, 6, "Equal parts of a circle (bolt holes)"),
    # 3 parallel lines cut by a transversal
    D(11, "Known", 100, "The angle you know", hi=180),
    C(12, "It is at", 3, 2, "Which numbered angle it is"),
    # 4 angles of a triangle
    C(13, "Known", 4, 1, "Two angles, or the apex of isosceles"),
    D(14, "A deg", 60, "Angle A: degrees", hi=180),
    M(15, "A min", 0, "Angle A: minutes"),
    D(16, "B deg", 52, "Angle B: degrees", hi=180),
    M(17, "B min", 0, "Angle B: minutes"),
    # 5 perimeter of a polygon
    U(18, 1),
    L(19, "Side 1", 3, "Side length (0 = not used)", 1),
    L(20, "Side 2", 5, "Side length (0 = not used)", 1),
    L(21, "Side 3", 6, "Side length (0 = not used)", 1),
    L(22, "Side 4", 4, "Side length (0 = not used)", 1),
    L(23, "Side 5", 0, "Side length (0 = not used)", 1),
    L(24, "Side 6", 0, "Side length (0 = not used)", 1),
    L(25, "Side 7", 0, "Side length (0 = not used)", 1),
    L(26, "Side 8", 0, "Side length (0 = not used)", 1),
    # 6 rectangle
    U(27, 1),
    L(28, "Length L", 9, "Length (0 = find it from the area)", 2),
    L(29, "Width W", 5, "Width (0 = find it from the area)", 2),
    S(30, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, only to find L or W (0 = find)", blank=2),
    # 7 square
    U(31, 2),
    L(32, "Side s", 9, "Side (0 = find it from the area)", 2),
    S(33, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, only to find the side", blank=2),
    # 8 parallelogram
    U(34, 1),
    L(35, "Base b", 7, "Base (0 = find it)", 2),
    L(36, "Height h", 10, "Height, square to the base (0 = find)", 2),
    L(37, "Side a", 12.2, "Slant side (0 = find from perimeter)", 2),
    # 9 trapezoid
    U(38, 1),
    L(39, "Top b1", 7, "One parallel side (0 = find it)", 2),
    L(40, "Bottom b2", 19, "Other parallel side (0 = find it)", 2),
    L(41, "Height h", 6, "Between the parallel sides (0 = find)", 2),
    L(42, "Side c", 8, "Slant side (0 = find from perimeter)", 2),
    L(43, "Side d", 9, "Other slant side (0 = find)", 2),
    # 10 cost and material
    S(44, "Amount", "", -1, 1, 0, 1e12, 600.25, "Area or length you have"),
    C(45, "It is in", 5, 2, "Unit of that amount"),
    S(46, "Price $", "", -1, 1, 0, 1e9, 65, "Price per unit (0 = no cost)"),
    C(47, "Per", 5, 3, "The unit the price is quoted per"),
    S(48, "Waste %", "%", -1, 1, 0, 500, 0, "Extra to allow for waste"),
    S(49, "Per pkg", "", -1, 1, 0, 1e9, 0, "One bag/bundle covers (price unit)", blank=1),
    S(50, "Spacing", "", -1, 1, 0, 1e9, 0, "Post spacing, amount unit", blank=1),
    # 11 Pythagorean theorem
    U(51, 2),
    L(52, "Leg a", 36, "One leg (0 = find it)", 2),
    L(53, "Leg b", 20, "Other leg (0 = find it)", 2),
    L(54, "Hyp. c", 0, "Hypotenuse (0 = find it)", 2),
    # 12 triangle from base and height
    U(55, 1),
    L(56, "Base b", 13, "Base (0 = find it from the area)", 2),
    L(57, "Height h", 8, "Height to that base (0 = find)", 2),
    S(58, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, only to find b or h", blank=2),
    # 13 triangle from three sides
    U(59, 2),
    L(60, "Side a", 7, "First side (0 = find from perimeter)", 2),
    L(61, "Side b", 7, "Second side (0 = find from perimeter)", 2),
    L(62, "Side c", 12, "Third side, the base (0 = find)", 2),
    # 14 regular hexagon
    U(63, 1),
    C(64, "Known", 6, 1, "The size you know"),
    L(65, "Size", 0.4, "Its length"),
    # 15 irregular figure from rectangles
    U(66, 2),
    L(67, "L1", 21, "Piece 1 length", 1),
    L(68, "W1", 12, "Piece 1 width", 1),
    C(69, "Piece 2", 7, 1, "Add piece 2 or cut it out"),
    L(70, "L2", 10, "Piece 2 length", 1),
    L(71, "W2", 24, "Piece 2 width", 1),
    C(72, "Piece 3", 7, 2, "Add piece 3 or cut it out"),
    L(73, "L3", 0, "Piece 3 length", 1),
    L(74, "W3", 0, "Piece 3 width", 1),
    S(75, "$ per", "A", -1, 0.25, 0, 1e9, 4.75, "Cost per square unit (0 = none)", blank=1),
    # 16 circle
    C(76, "Known", 8, 1, "The size you know"),
    L(77, "Size", 2.7, "Its value"),
    U(78, 1),
    C(79, "π", 9, 2, "Value of π the problem says to use"),
    # 17 ring
    U(80, 2),
    L(81, "Inner r", 8.5, "Radius of the inside circle (0 = find)", 2),
    L(82, "Width w", 12, "Width of the ring (0 = find)", 2),
    C(83, "π", 9, 1, "Value of π the problem says to use"),
    S(84, "$ per", "A", -1, 0.25, 0, 1e9, 9.5, "Cost per square unit (0 = none)", blank=1),
    # 18 sector and arc
    U(85, 1),
    L(86, "Radius r", 10, "Radius (0 = find it)", 2),
    S(87, "Angle", "°", -1, 1, 0, 360, 90, "Central angle (0 = find it)", blank=2),
    C(88, "π", 9, 1, "Value of π the problem says to use"),
    # 19 feet and inches, area units
    S(89, "Feet", "ft", -1, 1, 0, 1e9, 4, "Feet"),
    S(90, "Inches", "in", -1, 1, 0, 1e9, 6, "Inches (fractions as decimals)"),
    S(91, "Area", "", -1, 1, 0, 1e12, 600.25, "An area to convert"),
    C(92, "Area unit", 10, 2, "Unit of that area"),
    # ---- added: word problems (give what you know, 0 = find) ----
    L(93, "Perim. P", 0, "Total, to find one missing side", 1),
    L(94, "Perim. P", 0, "Perimeter, to find L or W (0 = find)", 2),
    L(95, "Diag. d", 0, "Diagonal, to find L or W (0 = find)", 2),
    L(96, "Perim. P", 0, "Perimeter, to find the side", 2),
    L(97, "Diag. d", 0, "Diagonal, to find the side", 2),
    S(98, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, to find b or h (0 = find)", blank=2),
    L(99, "Perim. P", 0, "Perimeter, to find a or b (0 = find)", 2),
    S(100, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, to find a base or h", blank=2),
    L(101, "Perim. P", 0, "Perimeter, to find one side", 2),
    S(102, "Area A", "A", -1, 1, 0, 1e12, 0, "Area, to find a leg (0 = find)", blank=2),
    L(103, "Height h", 0, "Height to side c (0 = use the sides)", 1),
    L(104, "Perim. P", 0, "Perimeter, to find one side", 2),
    C(105, "Area x", 11, 1, "Area formula: exact or the handout's"),
    L(106, "Outer R", 0, "Outside radius (0 = find)", 2),
    S(107, "Ring A", "A", -1, 1, 0, 1e12, 0, "Ring area, to find a size", blank=2),
    L(108, "Arc s", 0, "Arc length, to find r or angle", 2),
    S(109, "Sector A", "A", -1, 1, 0, 1e12, 0, "Sector area, to find r or angle", blank=2),
    # 20 equilateral triangle
    U(110, 6),
    C(111, "Known", 12, 1, "The size you know"),
    L(112, "Size", 30, "Its value"),
    # 21 Hero's formula
    U(113, 6),
    L(114, "Side a", 13, "First side"),
    L(115, "Side b", 14, "Second side"),
    L(116, "Side c", 15, "Third side"),
    # 22 composite: one shape with another added or cut out
    U(117, 2),
    C(118, "Shape 1", 13, 5, "The outside shape"),
    L(119, "1: size", 20, "L, s, b or r of shape 1"),
    L(120, "1: size 2", 0, "W or h of shape 1 (if it has one)", 1),
    C(121, "Then", 7, 2, "Add shape 2 or cut it out"),
    C(122, "Shape 2", 13, 2, "The shape added or cut out"),
    L(123, "2: size", 20, "L, s, b or r of shape 2"),
    L(124, "2: size 2", 0, "W or h of shape 2 (if it has one)", 1),
    C(125, "π", 9, 2, "Value of π the problem says to use"),
    C(126, "Hex. area", 11, 2, "Hexagon area: exact or the handout's"),
]

TOOLS = [
    ("Angle math", "Angle", "° ' ''", 1, [1, 2, 3, 4, 5, 6, 7, 8]),
    ("Angle facts", "Angle", "facts", 1, [9, 10]),
    ("Parallel lines", "Parallel", "lines", 1, [11, 12]),
    ("Triangle angles", "Triangle", "angles", 1, [13, 14, 15, 16, 17]),
    ("Perimeter", "Peri-", "meter", 2, [18, 19, 20, 21, 22, 23, 24, 25, 26, 93]),
    ("Rectangle", "Rect-", "angle", 2, [27, 28, 29, 30, 94, 95]),
    ("Square", "Square", "", 2, [31, 32, 33, 96, 97]),
    ("Parallelogram", "Parallel-", "ogram", 2, [34, 35, 36, 37, 98, 99]),
    ("Trapezoid", "Trape-", "zoid", 2, [38, 39, 40, 41, 42, 43, 100, 101]),
    ("Cost and material", "Cost &", "material", 2, [44, 45, 46, 47, 48, 49, 50]),
    ("Pythagorean", "Pythag-", "orean", 3, [51, 52, 53, 54, 102]),
    ("Triangle area", "Triangle", "b x h", 3, [55, 56, 57, 58]),
    ("Triangle 3 sides", "Triangle", "3 sides", 3, [59, 60, 61, 62, 103, 104]),
    ("Regular hexagon", "Hexagon", "", 3, [63, 64, 65, 105]),
    ("Irregular figure", "Irregular", "L-shapes", 3, [66, 67, 68, 69, 70, 71, 72, 73, 74, 75]),
    ("Circle", "Circle", "", 4, [76, 77, 78, 79]),
    ("Ring", "Ring", "", 4, [80, 81, 82, 106, 107, 83, 84]),
    ("Sector and arc", "Sector", "& arc", 4, [85, 86, 87, 108, 109, 88]),
    ("Feet and inches", "Feet &", "inches", 5, [89, 90, 91, 92]),
    ("Equilateral triangle", "Equilat-", "eral", 3, [110, 111, 112]),
    ("Hero's formula", "Hero's", "formula", 3, [113, 114, 115, 116]),
    ("Composite figure", "Composite", "shapes", 3, [117, 118, 119, 120, 121, 122, 123, 124, 125, 126]),
]


def unit_slots():
    """gUS(s): the Unit box of the tool that box s belongs to (0 = none)"""
    out = [0] * len(SLOTS)
    for t in TOOLS:
        unit = [s for s in t[4] if SLOTS[s - 1]["choice"] == 1]
        for s in t[4]:
            if unit:
                out[s - 1] = unit[0]
    return out


def check():
    check_slots(SLOTS, TOOLS, ntools=len(TOOLS), max_ins=10)
    for t in TOOLS:
        for s in t[4]:
            if SLOTS[s - 1]["unit"] in ("L", "A"):
                assert any(SLOTS[u - 1]["choice"] == 1 for u in t[4]), t[0]


def main():
    check()
    out = ["// ---- BEGIN TABLES (generated by tools/gen_geom_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += ["// the Unit box of each box's tool (0 = none)", "gUS:=" + plist(unit_slots()) + ";"]
    out += [l.replace("two per row", "one column down the left") for l in slot_functions(TOOLS, CHOICES, None, 0)]
    out += ["// ---- END TABLES ----"]
    write_block(PROGRAM, "\n".join(out))
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
