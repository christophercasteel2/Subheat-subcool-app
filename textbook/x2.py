"""Added depth for Part 2 (measurement): more explanation, worked examples, practice and review."""
import random
from fractions import Fraction
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr, F, frtxt
import figs

STD = [("ft", "in", 12), ("yd", "ft", 3), ("yd", "in", 36), ("mi", "ft", 5280), ("lb", "oz", 16), ("T", "lb", 2000), ("gal", "qt", 4), ("qt", "pt", 2),
       ("sq ft", "sq in", 144), ("sq yd", "sq ft", 9), ("sq yd", "sq in", 1296), ("cu ft", "cu in", 1728), ("cu yd", "cu ft", 27), ("cu ft", "gal", 7.48),
       ("gal", "cu in", 231)]
MET = [("in", "cm", 2.54), ("m", "ft", 3.28), ("mi", "km", 1.61), ("oz", "g", 28.35), ("kg", "lb", 2.205), ("L", "qt", 1.06), ("gal", "L", 3.785)]
STAIR = ["k", "h", "da", "", "d", "c", "m"]


def conv_items(rg, facts, count, vals=(2, 3.5, 5, 7.5, 12, 18, 25, 40, 64, 90, 150, 250, 400, 750, 1200, 2500)):
    """mixed conversions; answers that would round to almost nothing or run into the millions are skipped"""
    out, seen = [], set()
    while len(out) < count:
        big, small, f = rg.choice(facts)
        v = rg.choice(vals)
        down = rg.random() < 0.5
        ans = v * f if down else v / f
        q = f"{n(v)} {big} to {small}" if down else f"{n(v)} {small} to {big}"
        if not 1 <= ans <= 50000 or q in seen:
            continue
        seen.add(q)
        out.append((q, f"{r(ans, 1)} {small if down else big}"))
    return out


def ftin(total_in):
    f_, i_ = divmod(total_in, 12)
    return f"{f_} ft {i_} in"


# =====================================================================  4
def ch4():
    rg = random.Random(404)
    sec("4.8 Measurements in two units")
    p("A tape measure reads feet **and** inches; a scale reads pounds **and** ounces. A measurement such as 5 ft 7 in is really an addition, 5 ft + 7 in, "
      "and it has to be turned into a single unit before it can go into a formula or a calculator.")
    rule("Feet and inches",
         "**To inches:** multiply the feet by 12 and add the inches.   5 ft 7 in = 5 × 12 + 7 = 67 in",
         "**To decimal feet:** divide the inches by 12 and add the feet.   5 ft 7 in = 5 + 7 ÷ 12 = 5.583… ft",
         "**Back from inches:** divide by 12. The whole number is feet and the remainder is inches.   67 ÷ 12 = 5 remainder 7")
    example("Change 8 ft 9 in to (a) inches and (b) decimal feet.",
            [("8 × 12 = 96;  96 + 9 = 105", "(a) Feet to inches, then add the extra inches."), ("9 ÷ 12 = 0.75;  8 + 0.75 = 8.75", "(b) Inches to feet, then add the whole feet.")],
            "(a) 105 in   (b) 8.75 ft")
    example("A board is 134 in long. Write its length in feet and inches.",
            [("134 ÷ 12 = 11.1666…", "The whole number, 11, is the feet."), ("11 × 12 = 132;  134 − 132 = 2", "Subtract the inches in 11 ft to find the remainder.")], "11 ft 2 in")
    warn("7 inches is not 0.7 foot",
         "5 ft 7 in is **not** 5.7 ft. There are 12 inches in a foot, not 10, so 7 in is 7 ÷ 12 = 0.583 ft. Typing feet-and-inches as a decimal is one of the most common errors in estimating.")
    sub("Adding and subtracting feet and inches")
    p("Add the feet to the feet and the inches to the inches. If the inches reach 12 or more, trade 12 inches for 1 foot. When subtracting, borrow 1 foot as 12 inches if needed.")
    example("Add 6 ft 8 in and 4 ft 9 in.",
            [("6 ft + 4 ft = 10 ft;  8 in + 9 in = 17 in", "Add like units."), ("17 in = 1 ft 5 in", "17 is more than 12: trade 12 in for 1 ft."), ("10 ft + 1 ft 5 in = 11 ft 5 in", "")], "11 ft 5 in")
    example("A 12-ft board has a piece 7 ft 5 in long cut from it. How much is left?",
            [("12 ft 0 in = 11 ft 12 in", "There are no inches to subtract from, so borrow 1 ft and write it as 12 in."), ("11 ft 12 in − 7 ft 5 in = 4 ft 7 in", "Subtract like units.")], "4 ft 7 in")
    p("The same trading works for other pairs: 16 ounces for a pound, 4 quarts for a gallon. A charge of 3 lb 14 oz plus 1 lb 6 oz is 4 lb 20 oz, which is 5 lb 4 oz.")
    its = []
    for f_, i_ in [(3, 4), (7, 11), (12, 6), (9, 3)]:
        its.append((f"{f_} ft {i_} in to inches", f"{f_ * 12 + i_} in"))
    for f_, i_ in [(4, 6), (10, 3), (6, 9), (15, 8)]:
        its.append((f"{f_} ft {i_} in to decimal feet" + (" (nearest hundredth)" if (i_ * 100) % 12 else ""), r(f_ + i_ / 12, 2) + " ft"))
    for t in [40, 77, 150, 209]:
        its.append((f"{t} in to feet and inches", ftin(t)))
    for a, b in [((5, 7), (3, 9)), ((8, 10), (6, 5)), ((2, 11), (2, 11))]:
        its.append((f"{a[0]} ft {a[1]} in + {b[0]} ft {b[1]} in", ftin(a[0] * 12 + a[1] + b[0] * 12 + b[1])))
    for a, b in [((9, 4), (3, 8)), ((16, 0), (9, 7)), ((7, 2), (4, 11))]:
        its.append((f"{a[0]} ft {a[1]} in − {b[0]} ft {b[1]} in", ftin(a[0] * 12 + a[1] - b[0] * 12 - b[1])))
    its += [("2 lb 9 oz to ounces", "41 oz"), ("75 oz to pounds and ounces", "4 lb 11 oz"), ("3 lb 14 oz + 1 lb 6 oz", "5 lb 4 oz"), ("5 gal 1 qt − 2 gal 3 qt", "2 gal 2 qt")]
    practice("Measurements in two units", "", its, cols=2)

    sec("4.9 From dimensions to volume to gallons")
    p("The volume of a box-shaped tank, pan or slab is length × width × height, **V = LWH**. All three dimensions must be in the same unit. "
      "The unit you choose decides which conversion comes next.")
    table(["If the dimensions are in", "the volume is in", "to get gallons", "to get cubic yards"],
          [["inches", "cubic inches", "÷ 231", "÷ 46,656"], ["feet", "cubic feet", "× 7.48", "÷ 27"]], widths=[28, 22, 22, 28])
    example("A rectangular tank is 4 ft long, 2 ft wide and 18 in deep. How many gallons does it hold?",
            [("18 in ÷ 12 = 1.5 ft", "Put the depth in feet to match the other two."), ("V = (4)(2)(1.5) = 12 cu ft", "Volume in cubic feet."), ("12 × 7.48 = 89.76", "Cubic feet to gallons: multiply.")],
            "89.76 gal")
    example("A drain pan is 30 in by 20 in by 3 in. How many gallons does it hold, to the nearest tenth?",
            [("V = (30)(20)(3) = 1800 cu in", "All in inches, so the volume is in cubic inches."), ("1800 ÷ 231 = 7.792…", "Cubic inches to gallons: divide."), ("7.8", "")], "7.8 gal")
    example("A driveway slab is 40 ft long, 12 ft wide and 4 in thick. How many cubic yards of concrete are needed, to the nearest tenth?",
            [("4 in ÷ 12 = 0.3333… ft", "Thickness in feet. Keep the digits in the calculator."), ("V = (40)(12)(4 ÷ 12) = 160 cu ft", ""), ("160 ÷ 27 = 5.925…", "Cubic feet to cubic yards."), ("5.9", "Round as directed. A real order would be rounded up to 6.")],
            "5.9 cu yd")
    sub("Conversions in two steps")
    p("If the factor you need is not in the table, use two that are. To go from square inches to square yards, go through square feet: ÷ 144, then ÷ 9 "
      "(the same as ÷ 1296). To go from cubic yards to gallons: × 27, then × 7.48.")
    example("A truck delivers 3 cu yd of water-treatment sand. How many gallons of space does it fill?",
            [("3 × 27 = 81 cu ft", "Cubic yards to cubic feet."), ("81 × 7.48 = 605.88", "Cubic feet to gallons.")], "605.88 gal")
    wp = [("A tank is 5 ft by 3 ft by 2 ft. Find its volume in cubic feet and its capacity in gallons.", f"30 cu ft; {n(30 * 7.48)} gal"),
          ("A tank is 6 ft by 2 ft by 30 in. How many gallons does it hold?", n(6 * 2 * 2.5 * 7.48) + " gal"),
          ("A pan is 24 in by 18 in by 2 in. How many gallons does it hold, to the nearest tenth?", r(24 * 18 * 2 / 231, 1) + " gal"),
          ("A sump is 18 in by 18 in by 24 in. How many gallons, to the nearest tenth?", r(18 * 18 * 24 / 231, 1) + " gal"),
          ("A slab is 30 ft by 20 ft by 6 in. How many cubic yards, to the nearest tenth?", r(30 * 20 * 0.5 / 27, 1) + " cu yd"),
          ("A footing is 60 ft long, 2 ft wide and 1 ft deep. How many cubic yards, to the nearest tenth?", r(120 / 27, 1) + " cu yd"),
          ("A sidewalk is 50 ft by 4 ft by 4 in. How many cubic yards, to the nearest tenth?", r(50 * 4 / 3 / 27, 1) + " cu yd"),
          ("A 275-gallon oil tank has what volume in cubic feet, to the nearest tenth?", r(275 / 7.48, 1) + " cu ft"),
          ("A 40-gallon water heater has what volume in cubic inches?", n(40 * 231) + " cu in"),
          ("How many gallons are in 2 cu yd?", n(2 * 27 * 7.48) + " gal"),
          ("A room is 12 ft by 15 ft. How many square yards of carpet does it need?", "20 sq yd"),
          ("A duct opening is 2,592 sq in. How many square yards is that?", "2 sq yd")]
    practice("Volume and capacity problems", "Make the units match before multiplying. Round only where told to.", wp, cols=1)
    practice("Mixed standard conversions", "Convert. Round to the nearest tenth if needed.", conv_items(rg, STD, 30), cols=3)

    more_review([("6 ft 5 in to inches", "77 in"), ("9 ft 6 in to decimal feet", "9.5 ft"), ("115 in to feet and inches", "9 ft 7 in"), ("7 ft 9 in + 5 ft 8 in", "13 ft 5 in"),
                 ("10 ft − 3 ft 4 in", "6 ft 8 in"), ("A tank is 4 ft by 3 ft by 2.5 ft. How many gallons does it hold?", n(30 * 7.48) + " gal"),
                 ("A pan is 36 in by 22 in by 3 in. How many gallons, to the nearest tenth?", r(36 * 22 * 3 / 231, 1) + " gal"),
                 ("A slab is 24 ft by 24 ft by 4 in. How many cubic yards, to the nearest tenth?", r(24 * 24 / 3 / 27, 1) + " cu yd"),
                 ("Why is 6 ft 3 in not equal to 6.3 ft?", "3 in is 3 ÷ 12 = 0.25 ft, so 6 ft 3 in = 6.25 ft."),
                 ("Convert 3,888 sq in to square yards.", "3 sq yd"), ("How many cubic inches are in 1.5 cu ft?", "2,592 cu in"), ("Convert 3 lb 5 oz to ounces.", "53 oz")])


# =====================================================================  5
def ch5():
    rg = random.Random(505)
    sec("5.5 Prefixes that step by thousands")
    p("Electrical and electronic work uses the prefixes on the handout table that are **1000 apart**: mega, kilo, (unit), milli, micro. "
      "Each step between neighbors on this list moves the decimal point **three** places.")
    table(["mega (M)", "kilo (k)", "unit", "milli (m)", "micro (µ)"],
          [["1,000,000", "1,000", "1", "0.001", "0.000 001"], ["megohm, megawatt", "kilohm, kilowatt, kilovolt", "ohm, watt, volt, amp, farad", "milliamp, millivolt", "microamp, microfarad"]],
          caption="Table 5.4  The thousand-step prefixes. Moving right, the point moves 3 places right for each step; moving left, 3 places left.", small=True)
    example("Convert: (a) 4.7 kΩ to ohms   (b) 250 mA to amps   (c) 0.000047 F to microfarads   (d) 2,200 kΩ to megohms",
            [("4.7 kΩ → 4700 Ω", "(a) Kilo to unit: one step right, point 3 places right."), ("250 mA → 0.250 A", "(b) Milli to unit: one step left, point 3 places left."),
             ("0.000047 F → 47 µF", "(c) Unit to micro: two steps right, point 6 places right."), ("2,200 kΩ → 2.2 MΩ", "(d) Kilo to mega: one step left, point 3 places left.")],
            "(a) 4,700 Ω   (b) 0.25 A   (c) 47 µF   (d) 2.2 MΩ")
    warn("Capital M and small m",
         "**M** is mega, one million. **m** is milli, one thousandth. A 5 MΩ resistor and a 5 mΩ resistor differ by a factor of a billion. Copy the capital or small letter exactly.")
    its = [("3.3 kΩ to Ω", "3,300 Ω"), ("680 Ω to kΩ", "0.68 kΩ"), ("1.5 MΩ to kΩ", "1,500 kΩ"), ("470,000 Ω to MΩ", "0.47 MΩ"), ("35 mA to A", "0.035 A"), ("0.8 A to mA", "800 mA"),
           ("120 mV to V", "0.12 V"), ("13.8 kV to V", "13,800 V"), ("2,400 W to kW", "2.4 kW"), ("0.75 kW to W", "750 W"), ("0.00001 F to µF", "10 µF"), ("330 µF to F", "0.00033 F"),
           ("500 µA to mA", "0.5 mA"), ("2.5 MW to kW", "2,500 kW")]
    practice("Thousand-step prefixes", "Convert by moving the decimal point three places per step.", its, cols=2)

    sec("5.6 A feel for metric sizes")
    p("Converting is only half of knowing a unit. The other half is being able to tell whether an answer is sensible. A few benchmarks help.")
    table(["Unit", "About the size of"],
          [["1 millimeter", "the thickness of a dime"], ["1 centimeter", "the width of a fingernail; a little less than half an inch"], ["1 meter", "a long step; a yard plus about 3 inches"],
           ["1 kilometer", "about six tenths of a mile"], ["1 gram", "a paper clip"], ["1 kilogram", "a little over 2 pounds"], ["1 milliliter", "about 20 drops"],
           ["1 liter", "a little more than a quart"]], widths=[30, 70])
    example("Which is the sensible measurement? (a) The thickness of a sheet of 16-gauge steel: 1.5 mm, 1.5 cm or 1.5 m.   (b) The mass of a hand tool: 600 mg, 600 g or 600 kg.",
            [("1.5 mm", "(a) 1.5 cm is more than half an inch and 1.5 m is nearly five feet. Sheet metal is thin."), ("600 g", "(b) 600 mg is less than a paper clip or two; 600 kg is over half a ton.")],
            "(a) 1.5 mm   (b) 600 g")

    sec("5.7 More conversions between the systems")
    p("Shop drawings from overseas are in millimeters, and the handout gives the inch in **centimeters**. So a millimeter dimension takes two steps: "
      "up one stair to centimeters, then divide by 2.54.")
    example("A shaft is 38 mm in diameter. What is that in inches, to the nearest thousandth?",
            [("38 mm = 3.8 cm", "One step up the stairs: point one place left."), ("3.8 ÷ 2.54 = 1.4960…", "Centimeters to inches: divide."), ("1.496", "Round.")], "1.496 in", title="Millimeters to inches")
    example("A doorway is 6 ft 8 in high. What is that in centimeters?",
            [("6 × 12 + 8 = 80 in", "Feet and inches to inches first."), ("80 × 2.54 = 203.2", "Inches to centimeters: multiply.")], "203.2 cm", title="Feet and inches to centimeters")
    example("A container holds 2.5 gal. How many milliliters is that?",
            [("2.5 × 3.785 = 9.4625 L", "Gallons to liters: multiply."), ("9.4625 L = 9462.5 mL", "Liters to milliliters: three steps down, point three places right.")], "9,462.5 mL", title="Gallons to milliliters")
    example("A part has a mass of 500 g. What is its weight in pounds, to the nearest hundredth?",
            [("500 g = 0.5 kg", "The handout joins pounds to **kilograms**. Three steps up: point three places left."), ("0.5 × 2.205 = 1.1025", "Kilograms to pounds: multiply."), ("1.10", "")],
            "1.10 lb", title="Grams to pounds")
    rule("Plan a multi-step conversion", "**1.** Find the handout fact that crosses between the systems (2.54, 3.28, 1.61, 28.35, 2.205, 1.06 or 3.785).",
         "**2.** Convert what you have into the unit that appears in that fact.", "**3.** Cross to the other system.", "**4.** Convert to the unit asked for. Round only at the end.")
    wp = [("A bolt is 12 mm in diameter. What is that in inches, to the nearest thousandth?", r(1.2 / 2.54, 3) + " in"),
          ("A pipe is 2 in in diameter. What is that in millimeters?", n(2 * 25.4) + " mm"),
          ("A ceiling is 9 ft 6 in high. What is that in centimeters, to the nearest tenth?", r(114 * 2.54, 1) + " cm"),
          ("A panel is 1.2 m wide. What is that in inches, to the nearest tenth?", r(120 / 2.54, 1) + " in"),
          ("A cable run is 250 ft. What is that in meters, to the nearest tenth?", r(250 / 3.28, 1) + " m"),
          ("A road sign says 80 km. What is that in miles, to the nearest tenth?", r(80 / 1.61, 1) + " mi"),
          ("A charge is 2 lb 4 oz of refrigerant. How many grams is that, to the nearest whole number?", r(36 * 28.35, 0) + " g"),
          ("A motor has a mass of 18 kg. What is its weight in pounds, to the nearest tenth?", r(18 * 2.205, 1) + " lb"),
          ("A part has a mass of 850 g. What is that in pounds, to the nearest hundredth?", r(0.85 * 2.205, 2) + " lb"),
          ("A tank holds 30 gal. How many liters is that, to the nearest tenth?", r(30 * 3.785, 1) + " L"),
          ("A bottle holds 750 mL. How many quarts is that, to the nearest hundredth?", r(0.75 * 1.06, 2) + " qt"),
          ("A sump holds 1.5 gal. How many milliliters is that?", n(1.5 * 3785) + " mL"),
          ("How many centimeters are in 1 yard?", n(36 * 2.54) + " cm"), ("How many feet are in 1 kilometer?", n(3280) + " ft")]
    practice("Multi-step conversions", "Write each step with its unit.", wp, cols=1)

    q = []
    for _ in range(24):
        base = rg.choice(["m", "g", "L"])
        i, j = rg.sample(range(7), 2)
        v = rg.choice([0.45, 1.2, 3.6, 7, 12.5, 48, 96, 250, 380, 1500, 4200])
        q.append((f"{n(v)} {STAIR[i]}{base} to {STAIR[j]}{base}", f"{n(rnd(v * 10 ** (j - i), 8))} {STAIR[j]}{base}"))
    practice("More metric to metric", "Count the steps on the stairs and move the decimal point.", q, cols=3)
    practice("More metric and standard", "Convert. Round to the nearest tenth if needed.",
             conv_items(rg, MET, 24, (2, 5, 8, 12, 20, 36, 50, 75, 100, 150, 250, 400)), cols=3)

    more_review([("2.2 kΩ to Ω", "2,200 Ω"), ("45 mA to A", "0.045 A"), ("0.000022 F to µF", "22 µF"), ("3,300 kΩ to MΩ", "3.3 MΩ"),
                 ("Which is the sensible length of a room: 5 mm, 5 cm or 5 m?", "5 m"), ("A shaft is 25 mm in diameter. Convert to inches, to the nearest thousandth.", r(2.5 / 2.54, 3) + " in"),
                 ("Convert 5 ft 10 in to centimeters.", n(70 * 2.54) + " cm"), ("Convert 250 g to pounds, to the nearest hundredth.", r(0.25 * 2.205, 2) + " lb"),
                 ("Convert 4 gal to milliliters.", n(4 * 3785) + " mL"), ("Convert 3 km to feet.", n(9840) + " ft"),
                 ("0.36 hm to dm", "360 dm"), ("7,500 cg to dag", "7.5 dag")])


# =====================================================================  6
def ch6():
    rg = random.Random(606)
    sec("6.6 Measuring between two points")
    p("A worn or damaged end makes the zero of a rule unreliable, so careful workers often start at the 1-inch mark and subtract 1 from the reading. "
      "In general, the distance between any two points on a rule is the **larger reading minus the smaller reading**.")
    example("One end of a part lines up with the 1 [[3|8]]-in mark and the other end with the 3 [[13|16]]-in mark. How long is the part?",
            [("3 [[13|16]] − 1 [[3|8]]", "Larger reading minus smaller."), ("3 [[13|16]] − 1 [[6|16]]", "Common denominator 16."), ("2 [[7|16]]", "Subtract whole numbers and fractions.")], "2 [[7|16]] in")
    example("On a metric rule, a part reaches from the 14-mm mark to the 8.6-cm mark. How long is it in millimeters?",
            [("8.6 cm = 86 mm", "Put both readings in the same unit."), ("86 − 14 = 72", "")], "72 mm")
    sub("Rules divided into 32nds and 64ths")
    p("A machinist’s rule may be divided into 32 or 64 parts per inch. Count the spaces, write the count over 32 or 64, and reduce by halving. "
      "Twenty spaces on a 32nds scale is [[20|32]] = [[10|16]] = [[5|8]].")
    marks = [5, 14, 21, 35, 44, 51, 59]
    mm = [6, 23, 41, 57, 84]
    fig(figs.ruler(inch_marks=list(zip("PQRSTUV", marks)), mm_marks=list(zip("ABCDE", mm))), "Rule for Practice 6.4.")
    its = [(f"Read point {c} in millimeters.", f"{m} mm") for c, m in zip("ABCDE", mm)]
    its += [(f"Read point {c} in inches, in lowest terms.", fr(Fraction(s, 16)) + " in") for c, s in zip("PQRSTUV", marks)]
    its += [("How far is it from P to S, in inches?", fr(Fraction(marks[3] - marks[0], 16)) + " in"), ("How far is it from Q to V, in inches?", fr(Fraction(marks[6] - marks[1], 16)) + " in"),
            ("How far is it from R to T, in inches?", fr(Fraction(marks[4] - marks[2], 16)) + " in"), ("How far is it from A to E, in millimeters?", f"{mm[4] - mm[0]} mm"),
            ("How far is it from B to D, in centimeters?", n((mm[3] - mm[1]) / 10) + " cm"),
            ("A part reaches from the 1-in mark to the 4 [[5|16]]-in mark. How long is it?", "3 [[5|16]] in"),
            ("A part reaches from the 2 [[3|4]]-in mark to the 7 [[1|8]]-in mark. How long is it?", fr(F("7 1/8") - F("2 3/4")) + " in"),
            ("Reduce [[28|32]], [[12|64]] and [[40|64]] to lowest terms.", "[[7|8]], [[3|16]], [[5|8]]")]
    practice("More rule reading", "Use Figure 6.8 for problems 1 to 17.", its, cols=2)

    sec("6.7 More about gauges")
    p("Not every scale starts at zero, and not every scale has the same number of spaces between its numbers. Always work out the scale value on the gauge in front of you; never assume it.")
    gs = [(30, 120, 30, 5, 85, "°F"), (0, 160, 40, 10, 95, "psi"), (0, 15, 5, 1, 11.5, "amps")]
    fig(figs.side_by_side([figs.gauge(a, b, c, d, v, u, size=200) for a, b, c, d, v, u in gs]), "Three more dials. Left: a scale that starts at 30. Center and right: different numbers of spaces between numbers.")
    example("Read the three gauges in Figure 6.9.",
            [("Left: 60 − 30 = 30;  30 ÷ 6 spaces = 5 per space", "Numbered 30, 60, 90, 120 with six spaces between numbers."),
             ("60 + 5 spaces × 5 = 85", "The needle is five spaces past 60."),
             ("Center: 40 ÷ 4 spaces = 10 per space;  80 + 1.5 spaces × 10 = 95", "The needle is halfway between the first and second marks past 80."),
             ("Right: 5 ÷ 5 spaces = 1 per space;  10 + 1.5 = 11.5", "Halfway between the first and second marks past 10.")],
            "85°F, about 95 psi, about 11.5 amps")
    rule("When the needle is between two marks",
         "Decide whether it is about one quarter, one half or three quarters of the way across the space, and add that fraction of the scale value. "
         "An estimate should always be reported with the word **about** or **approximately**.")
    gs2 = [(0, 200, 50, 10, 130, "psi"), (0, 30, 10, 2, 17, "in. Hg"), (40, 100, 20, 5, 75, "°F"), (0, 600, 100, 20, 460, "volts"), (0, 80, 20, 4, 50, "psi"), (0, 2000, 500, 100, 1250, "rpm")]
    fig(figs.side_by_side([figs.gauge(a, b, c, d, v, u, size=200) for a, b, c, d, v, u in gs2[:3]]), "Gauges G, H and J for Practice 6.5.")
    fig(figs.side_by_side([figs.gauge(a, b, c, d, v, u, size=200) for a, b, c, d, v, u in gs2[3:]]), "Gauges K, L and M for Practice 6.5.")
    its = []
    for c, g in zip("GHJKLM", gs2):
        its.append((f"Gauge {c}: what is one small space worth?", f"{n(g[3])} {g[5]}"))
        its.append((f"Gauge {c}: estimate the reading.", f"about {n(g[4])} {g[5]}"))
    its += [("A gauge is numbered 0, 25, 50, 75, 100 with 5 spaces between numbers. What is each space worth?", "5"),
            ("On that gauge the needle is 2 spaces past 50. What is the reading?", "60"),
            ("A dual-scale gauge reads 50 psi. About what should its kPa scale read?", "about 345 kPa"),
            ("A dual-scale gauge reads 1,380 kPa. About what should its psi scale read?", "about 200 psi")]
    practice("More gauge reading", "Use Figures 6.10 and 6.11 for problems 1 to 12.", its, cols=2)

    sec("6.8 More about tolerance")
    sub("Unequal tolerances")
    p("Sometimes a part may be allowed to run farther over than under, or the other way round. The drawing then gives two tolerances, one with a plus sign and one with a minus sign.")
    example("A shaft is dimensioned 1.250 in, +0.005 in, −0.002 in. Find its limits. Is a shaft measuring 1.2475 in acceptable?",
            [("1.250 + 0.005 = 1.255", "Upper limit uses the plus tolerance."), ("1.250 − 0.002 = 1.248", "Lower limit uses the minus tolerance."),
             ("1.2475 &lt; 1.2480", "Compare with four decimal places. It is below the lower limit.")], "1.248 in to 1.255 in; no, it is too small")
    sub("Total tolerance")
    p("The **total tolerance** is the distance between the limits: upper limit − lower limit. For 0.81 ± 0.003 it is 0.813 − 0.807 = 0.006 in, twice the ± value.")
    sub("Fraction and percent tolerances")
    example("A stud is to be cut 92 [[5|8]] in ± [[1|16]] in. Find the limits.",
            [("92 [[5|8]] = 92 [[10|16]]", "Common denominator."), ("92 [[10|16]] + [[1|16]] = 92 [[11|16]]", "Upper limit."), ("92 [[10|16]] − [[1|16]] = 92 [[9|16]]", "Lower limit.")],
            "92 [[9|16]] in to 92 [[11|16]] in")
    example("A 680-Ω resistor has a tolerance of ±5%. Find its limits. Is a resistor that measures 712 Ω within tolerance?",
            [("5 × 680 ÷ 100 = 34", "The tolerance is 5% **of** the marked value."), ("680 + 34 = 714;  680 − 34 = 646", "Limits."), ("646 ≤ 712 ≤ 714", "")], "646 Ω to 714 Ω; yes")
    its = []
    for _ in range(8):
        nom = rg.choice([0.25, 0.375, 0.5, 0.625, 0.75, 1.125, 1.5, 2.0, 2.75])
        t = rg.choice([0.001, 0.002, 0.003, 0.005, 0.01])
        test = round(nom + rg.choice([-1.6, -0.8, -0.4, 0.5, 0.9, 1.4]) * t, 4)
        ok = nom - t - 1e-9 <= test <= nom + t + 1e-9
        its.append((f"{n(nom)} in ± {n(t)} in. Find the limits. Is {n(test)} in acceptable?", f"{n(rnd(nom - t, 4))} in to {n(rnd(nom + t, 4))} in; {'yes' if ok else 'no'}"))
    its += [("2.000 in, +0.004 in, −0.001 in. Find the limits.", "1.999 in to 2.004 in"), ("0.875 in, +0.000 in, −0.003 in. Find the limits.", "0.872 in to 0.875 in"),
            ("What is the total tolerance of 1.5 in ± 0.004 in?", "0.008 in"), ("36 [[1|2]] in ± [[1|8]] in. Find the limits.", "36 [[3|8]] in to 36 [[5|8]] in"),
            ("14 [[3|4]] in ± [[1|32]] in. Find the limits.", "14 [[23|32]] in to 14 [[25|32]] in"), ("A 1,000-Ω resistor is rated ±10%. Find its limits.", "900 Ω to 1,100 Ω"),
            ("A 47-µF capacitor is rated ±20%. Find its limits.", "37.6 µF to 56.4 µF"),
            ("A hole must be 0.50 in ± 0.004 in. Is a [[1|2]]-in drill acceptable? Is a [[33|64]]-in drill (0.5156 in)?", "The 1/2-in drill is (0.5000). The 33/64-in drill is not (over 0.504).")]
    practice("More tolerance", "Do not round.", its, cols=1)

    sec("6.9 More missing dimensions")
    p("Two patterns cover nearly every missing-dimension problem.")
    rule("Two patterns", "**Parts in a row:** missing part = overall length − sum of the known parts.",
         "**Equal spaces:** each space = (overall length − the end margins) ÷ number of spaces.")
    example("A plate 15 [[1|2]] in long has five holes equally spaced. The first and last holes are each [[3|4]] in from an end. Find the distance between hole centers.",
            [("15 [[1|2]] − [[3|4]] − [[3|4]] = 14", "Take off the two end margins."), ("5 holes → 4 spaces", "Count the **spaces**, not the holes."), ("14 ÷ 4 = 3.5", "")], "3 [[1|2]] in")
    warn("Holes and spaces", "Five holes in a row have four spaces between them. Ten fence posts have nine gaps. The number of spaces is always one less than the number of marks.")
    example("A shaft 9.375 in long has four sections. Three of them measure 2 [[1|4]] in, 1 [[7|8]] in and 3.5 in. Find the fourth as a fraction.",
            [("2.25 + 1.875 + 3.5 = 7.625", "Change to decimals and add the known parts."), ("9.375 − 7.625 = 1.75", "Subtract from the overall length."), ("1.75 = 1 [[3|4]]", "Back to a fraction.")], "1 [[3|4]] in")
    its = []
    for tot, parts in [("48", ["12 1/2", "17 3/8"]), ("72 1/4", ["20.5", "33 1/8"]), ("25.5", ["6 3/4", "7 1/8", "4.25"]), ("100", ["27 5/8", "31 1/4", "18.5"]), ("18 3/8", ["5 1/2", "5 1/2", "3 3/16"])]:
        v = F(tot) - sum(F(x) for x in parts)
        its.append((f"Overall {frtxt(tot)} in; known parts " + ", ".join(frtxt(x) + " in" for x in parts) + ". Find the missing part.", f"{n(float(v))} in" + ("" if v.denominator == 1 else f" = {fr(v)} in")))
    its += [("A 24-in bar has 7 holes equally spaced, with the end holes 1.5 in from each end. Find the spacing.", "3.5 in"),
            ("A 10-ft wall gets studs at each end and 6 more equally spaced between them. Find the center-to-center spacing in inches, to the nearest tenth.", r(120 / 7, 1) + " in"),
            ("A 36-in rail has 9 equal spaces between balusters and no end margins. How wide is each space?", "4 in"),
            ("Three equal shelves and four [[3|4]]-in dividers fill a 30-in opening. How wide is each shelf space?", "9 in"),
            ("A panel 42 in wide has two equal end margins and a 30 [[1|2]]-in opening centered in it. How wide is each margin?", "5 [[3|4]] in")]
    practice("More missing dimensions", "Do not round unless told to.", its, cols=1)

    more_review([("A part reaches from the 1 [[1|4]]-in mark to the 4 [[1|16]]-in mark. How long is it?", fr(F("4 1/16") - F("1 1/4")) + " in"),
                 ("Reduce [[36|64]] to lowest terms.", "[[9|16]]"), ("A gauge is numbered 30, 60, 90 with 6 spaces between numbers. What is each space worth?", "5"),
                 ("On that gauge the needle is 4 spaces past 30. What is the reading?", "50"),
                 ("1.750 in, +0.003 in, −0.001 in. Find the limits.", "1.749 in to 1.753 in"), ("What is the total tolerance of 0.625 in ± 0.002 in?", "0.004 in"),
                 ("A 220-Ω resistor is rated ±5%. Find its limits.", "209 Ω to 231 Ω"), ("22 [[1|4]] in ± [[1|16]] in. Find the limits.", "22 [[3|16]] in to 22 [[5|16]] in"),
                 ("A 20-in plate has 6 holes equally spaced, with the end holes 1.25 in from each end. Find the spacing.", "3.5 in"),
                 ("How many spaces are there between 8 equally spaced holes?", "7")])


def part2():
    cumulative("Part 2 · Measurement", "Mixed problems from Chapters 4, 5 and 6. Round to the nearest tenth if needed.",
               [("8.5 ft to in", "102 in"), ("90 oz to lb", "5.6 lb"), ("14 qt to gal", "3.5 gal"), ("900 sq in to sq ft", "6.3 sq ft"), ("6 sq yd to sq ft", "54 sq ft"),
                ("3,000 cu in to cu ft", "1.7 cu ft"), ("7 cu yd to cu ft", "189 cu ft"), ("15 cu ft to gal", "112.2 gal"), ("800 cu in to gal", "3.5 gal"),
                ("4 ft 7 in + 6 ft 9 in", "11 ft 4 in"), ("3.4 m to cm", "340 cm"), ("65 mm to cm", "6.5 cm"), ("0.9 kg to g", "900 g"), ("450 mL to L", "0.45 L"),
                ("10 in to cm", "25.4 cm"), ("75 kg to lb", "165.4 lb"), ("10 gal to L", "37.9 L"), ("30 km to mi", "18.6 mi"),
                ("Which is larger, a kilogram or a pound?", "a kilogram"), ("A point is 13 sixteenths past the 2-in mark. Give the reading.", "2 [[13|16]] in"),
                ("A gauge is numbered every 100 with 5 spaces between numbers. The needle is 3 spaces past 400. Give the reading.", "460"),
                ("Find the limits of 2.25 in ± 0.005 in.", "2.245 in to 2.255 in"), ("Is a [[3|4]]-in part acceptable for 0.76 in ± 0.008 in?", "No. 0.75 is below the lower limit, 0.752."),
                ("Overall 40 in; known parts 13 [[3|4]] in and 9.5 in. Find the missing part.", "16.75 in"),
                ("A tank 3 ft by 2 ft by 2 ft holds how many gallons?", n(12 * 7.48) + " gal")], cols=2)
