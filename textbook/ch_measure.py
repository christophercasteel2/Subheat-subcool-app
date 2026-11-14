"""Part 2: measurement (standard units, metric, rulers, gauges, tolerance)."""
from fractions import Fraction
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr, F, frtxt
import figs

part("Part 2 · Measurement", "Measuring is counting units. Part 2 covers the two systems of units used in American shops, "
     "how to move between them, and how to read the instruments that do the measuring.")

# =====================================================================  4
chapter("Standard Units of Measure",
        ["State the standard (U.S. customary) units of length, weight and liquid capacity and how they relate.",
         "Convert a measurement from one unit to another by multiplying or dividing by a conversion factor.",
         "Decide whether to multiply or divide.",
         "Convert square units of area and cubic units of volume.",
         "Convert between cubic measure and gallons."],
        "Carpet is sold by the square yard, concrete by the cubic yard, ductwork is laid out in inches and a tank is rated in gallons. "
        "The measurements on a job rarely arrive in the unit you need. This chapter is about changing the unit without changing the amount.",
        [("unit", "A fixed amount used for measuring, such as a foot or a pound."),
         ("conversion factor", "The number of smaller units that make one larger unit: 12 inches make 1 foot."),
         ("square unit", "A unit of area: a square that is one unit long on each side."),
         ("cubic unit", "A unit of volume: a cube that is one unit long on each edge."),
         ("capacity", "How much liquid a container holds.")])

sec("4.1 The standard units")
p("The standard system, also called the U.S. customary or English system, grew out of everyday objects and trade. "
  "Its conversion factors are not regular, so they have to be memorized or looked up.")
table(["Length", "Weight", "Liquid Capacity"],
      [["1 foot (ft.) = 12 inches (in.)", "1 pound (lb.) = 16 ounces (oz.)", "1 pint (pt.) = 2 cups"],
       ["1 yard (yd.) = 3 feet (ft.)", "1 Ton (T) = 2000 pounds (lbs.)", "1 quart (qt.) = 2 pts."],
       ["1 yard = 36 in.", "", "1 gallon (gal) = 4 qts."], ["1 mile (mi.) = 5280 ft.", "", ""], ["1 mile (mi.) = 1760 yds.", "", ""]],
      caption="Table 4.1  Standard Units (class handout)")
table(["Area Units", "Volume Units", ""],
      [["1 sq. ft. = 144 sq. in", "1 cu. ft. = 1728 cu in", "1 cu. ft. = 7.48 gallons"], ["1 sq. yd. = 9 sq. ft.", "1 cu. yd. = 27 cu ft.", "1 gallon = 231 cu. in."],
       ["1 sq. yd. = 1296 sq. in", "1 cu. yd. = 46,656 cu. in", ""]],
      caption="Table 4.1 (continued)  Standard Units: area and volume (class handout)")
p("A measurement has two parts, a **number** and a **unit**. Converting changes both: the same board is 8 feet or 96 inches. "
  "The number grew because the unit shrank.")

p("This chapter takes the standard system one **category** at a time. Each category has its own set of facts:")
table(["Category", "What it measures", "Units", "Section"],
      [["Length", "how long, how far", "in, ft, yd, mi", "4.3"], ["Weight", "how heavy", "oz, lb, T", "4.4"],
       ["Liquid capacity", "how much a container holds", "cup, pt, qt, gal", "4.5"], ["Area", "how much surface", "sq in, sq ft, sq yd", "4.6"],
       ["Volume", "how much space", "cu in, cu ft, cu yd, and gallons", "4.7"]], caption="Table 4.2  The five conversion categories", widths=[20, 32, 32, 16])

sec("4.2 Multiply or divide?")
rule("Converting units",
     "Going to a **smaller** unit, you will need **more** of them: **multiply** by the conversion factor.",
     "Going to a **larger** unit, you will need **fewer** of them: **divide** by the conversion factor.")
example("Convert 7.5 ft to inches.",
        [("1 ft = 12 in", "Find the fact that connects the two units."),
         ("feet → inches: larger → smaller", "Inches are smaller than feet, so there will be more of them. Multiply."),
         ("7.5 × 12 = 90", "Multiply by the conversion factor.")], "90 in")
example("Convert 150 oz to pounds. Round to the nearest tenth.",
        [("1 lb = 16 oz", "The connecting fact."), ("ounces → pounds: smaller → larger", "Pounds are larger, so there will be fewer. Divide."),
         ("150 ÷ 16 = 9.375", "Divide by the conversion factor."), ("9.4", "Round to the nearest tenth: the test digit 7 rounds the 3 up.")], "9.4 lb")
warn("The sanity check",
     "Before writing the answer, ask whether the number should have gone up or down. 150 ounces cannot be 2400 pounds. "
     "If the answer moved the wrong way, you multiplied when you should have divided.")
sub("Conversions that take two steps")
p("When no single fact joins the two units, go through a unit in between, one step at a time.")
example("How many cups are in 3 gallons?",
        [("3 × 4 = 12 qt", "Gallons to quarts: smaller unit, multiply by 4."), ("12 × 2 = 24 pt", "Quarts to pints: multiply by 2."),
         ("24 × 2 = 48 cups", "Pints to cups: multiply by 2.")], "48 cups")
sub("Unit fractions: a method that cannot go the wrong way")
p("A conversion fact can be written as a fraction equal to 1, such as [[12 in|1 ft]] or [[1 ft|12 in]]. Multiplying by 1 "
  "does not change an amount. Choose the fraction that has the unit you want to **get rid of on the bottom**, so that it cancels.")
eq("7.5 ft × [[12 in|1 ft]] = 90 in          (ft cancels ft, inches remain)",
   "150 oz × [[1 lb|16 oz]] = 9.375 lb          (oz cancels oz, pounds remain)")


sec("4.3 Category 1: length")
fig(figs.chain(["mile", "yard", "foot", "inch"], ["1760", "3", "12"], figs.BLUE, "LENGTH"),
    "The length chain. Move right (to a smaller unit) and multiply; move left (to a larger unit) and divide.")
table(["Fact", "To go to the smaller unit", "To go to the larger unit"],
      [["1 ft = 12 in", "ft → in: × 12", "in → ft: ÷ 12"], ["1 yd = 3 ft", "yd → ft: × 3", "ft → yd: ÷ 3"], ["1 yd = 36 in", "yd → in: × 36", "in → yd: ÷ 36"],
       ["1 mi = 5280 ft", "mi → ft: × 5280", "ft → mi: ÷ 5280"], ["1 mi = 1760 yd", "mi → yd: × 1760", "yd → mi: ÷ 1760"]], small=True)
example("A run of conduit is 46 ft long. How many yards is that, to the nearest tenth? How many inches?",
        [("46 ÷ 3 = 15.333…", "Feet to yards: a yard is larger, so divide by 3."), ("15.3 yd", "Round to the nearest tenth."),
         ("46 × 12 = 552 in", "Feet to inches: an inch is smaller, so multiply by 12.")], "15.3 yd;  552 in")
example("A pipeline is 3960 ft long. What part of a mile is that?",
        [("1 mi = 5280 ft", "The fact."), ("3960 ÷ 5280 = 0.75", "Feet to miles: divide.")], "0.75 mi")

sec("4.4 Category 2: weight")
fig(figs.chain(["ton", "pound", "ounce"], ["2000", "16"], figs.GOLD, "WEIGHT"), "The weight chain.")
table(["Fact", "To go to the smaller unit", "To go to the larger unit"],
      [["1 lb = 16 oz", "lb → oz: × 16", "oz → lb: ÷ 16"], ["1 T = 2000 lb", "T → lb: × 2000", "lb → T: ÷ 2000"]], small=True)
example("A rooftop unit weighs 1.75 tons. How many pounds is that?",
        [("1 T = 2000 lb", "The fact."), ("1.75 × 2000 = 3500", "Tons to pounds: smaller unit, multiply.")], "3500 lb")
example("A system is charged with 6 lb 4 oz of refrigerant. Write the charge in ounces, and in pounds as a decimal.",
        [("6 × 16 = 96 oz", "Change the pounds to ounces."), ("96 + 4 = 100 oz", "Add the extra ounces."),
         ("4 ÷ 16 = 0.25 lb", "Or change the 4 ounces to pounds."), ("6 + 0.25 = 6.25 lb", "Add to the whole pounds.")], "100 oz, or 6.25 lb",
        title="A measurement in two units")

sec("4.5 Category 3: liquid capacity")
fig(figs.chain(["gallon", "quart", "pint", "cup"], ["4", "2", "2"], figs.PURPLE, "LIQUID CAPACITY"), "The capacity chain.")
table(["Fact", "To go to the smaller unit", "To go to the larger unit"],
      [["1 pt = 2 cups", "pt → cups: × 2", "cups → pt: ÷ 2"], ["1 qt = 2 pt", "qt → pt: × 2", "pt → qt: ÷ 2"], ["1 gal = 4 qt", "gal → qt: × 4", "qt → gal: ÷ 4"],
       ["1 gal = 8 pt = 16 cups", "gal → pt: × 8", "pt → gal: ÷ 8"]], small=True)
example("A compressor takes 54 fluid quarts of oil over a year. How many gallons is that?",
        [("1 gal = 4 qt", "The fact."), ("54 ÷ 4 = 13.5", "Quarts to gallons: larger unit, divide.")], "13.5 gal")
example("How many pints are in 2.5 gallons?",
        [("2.5 × 4 = 10 qt", "Gallons to quarts."), ("10 × 2 = 20 pt", "Quarts to pints.")], "20 pt")


def cv(val, a, b, factor, mult, places=1):
    ans = val * factor if mult else val / factor
    return (f"{n(val)} {a} to {b}", f"{r(ans, places)} {b}")


practice("Length, weight and capacity", "Convert. Round to the nearest tenth if needed. Problems 1 to 6 are length, 7 to 10 weight, 11 to 14 capacity, 15 and 16 length.",
         [cv(*t) for t in [(9, "ft", "in", 12, 1), (102, "in", "ft", 12, 0), (4.5, "yd", "ft", 3, 1), (50, "ft", "yd", 3, 0),
                           (2.5, "mi", "ft", 5280, 1), (9000, "ft", "mi", 5280, 0), (5, "lb", "oz", 16, 1), (72, "oz", "lb", 16, 0),
                           (3.2, "T", "lb", 2000, 1), (5500, "lb", "T", 2000, 0), (6, "gal", "qt", 4, 1), (18, "qt", "gal", 4, 0),
                           (7, "pt", "qt", 2, 0), (2, "gal", "pt", 8, 1), (180, "in", "yd", 36, 0), (0.75, "mi", "yd", 1760, 1)]], cols=2)

sec("4.6 Category 4: area")
p("Area is measured in **square units**. A square foot is a square that measures 1 foot on each side. Since each side is "
  "12 inches, the square holds 12 rows of 12 square inches: 144 of them, not 12.")
fig(figs.unit_square(), "One square foot holds 144 square inches. The small red square is one square inch.")
rule("Area conversion factors", "Square the length factor.",
     "1 sq ft = 12 × 12 = **144** sq in", "1 sq yd = 3 × 3 = **9** sq ft", "1 sq yd = 36 × 36 = **1296** sq in")
fig(figs.chain(["sq yd", "sq ft", "sq in"], ["9", "144"], figs.BLUE, "AREA"), "The area chain. From square yards straight to square inches the factor is 9 × 144 = 1296.")
example("A duct opening has an area of 1000 sq in. How many square feet is that, to the nearest tenth?",
        [("1 sq ft = 144 sq in", "The area fact, not the length fact."), ("sq in → sq ft: smaller → larger", "Divide."),
         ("1000 ÷ 144 = 6.944…", "Divide by 144."), ("6.9", "Round to the nearest tenth.")], "6.9 sq ft")
example("A room needs 15.5 sq yd of carpet. How many square feet is that?",
        [("1 sq yd = 9 sq ft", "The area fact."), ("15.5 × 9 = 139.5", "Larger unit to smaller: multiply.")], "139.5 sq ft")
warn("The most common conversion mistake",
     "Dividing square inches by 12 to get square feet. Twelve converts *lengths*. Areas use 144. "
     "Watch for the words “square” or “sq” or the exponent in in² and ft².")

sec("4.7 Category 5: volume")
p("Volume is measured in **cubic units**. A cubic foot is a cube 1 foot long on every edge. It holds 12 layers, each with "
  "144 cubic inches, so the length factor is used **three** times.")
fig(figs.unit_cube(), "One cubic foot holds 12 × 12 × 12 = 1,728 cubic inches.")
rule("Volume conversion factors", "Cube the length factor.",
     "1 cu ft = 12 × 12 × 12 = **1728** cu in", "1 cu yd = 3 × 3 × 3 = **27** cu ft", "1 cu yd = 36 × 36 × 36 = **46,656** cu in")
fig(figs.chain(["cu yd", "cu ft", "cu in"], ["27", "1728"], figs.GREEN, "VOLUME"), "The volume chain. From cubic yards straight to cubic inches the factor is 27 × 1728 = 46,656.")
example("An air handler cabinet has a volume of 5.5 cu ft. How many cubic inches is that?",
        [("1 cu ft = 1728 cu in", "The volume fact."), ("5.5 × 1728 = 9504", "Larger unit to smaller: multiply.")], "9504 cu in")
example("A slab needs 2500 cu ft of concrete. Concrete is ordered by the cubic yard. How many cubic yards, to the nearest tenth?",
        [("1 cu yd = 27 cu ft", "The volume fact."), ("2500 ÷ 27 = 92.592…", "Smaller unit to larger: divide."),
         ("92.6", "Round to the nearest tenth.")], "92.6 cu yd")
sub("Cubic measure and gallons")
p("Tanks, pans and sumps are built to dimensions in inches or feet but are filled in gallons. Two facts connect them.")
rule("Volume and liquid capacity", "1 cu ft = **7.48** gallons", "1 gallon = **231** cu in")
fig(figs.chain(["cu ft", "gallon", "cu in"], ["7.48", "231"], figs.PURPLE, "VOLUME AND GALLONS"), "A gallon sits between the cubic foot and the cubic inch.")
example("A condensate tank has a volume of 5 cu ft. How many gallons does it hold?",
        [("1 cu ft = 7.48 gal", "A gallon is smaller than a cubic foot, so there will be more gallons."), ("5 × 7.48 = 37.4", "Multiply.")], "37.4 gal")
example("A drain pan holds 1500 cu in. How many gallons is that, to the nearest tenth?",
        [("1 gal = 231 cu in", "A gallon is larger than a cubic inch."), ("1500 ÷ 231 = 6.493…", "Divide."), ("6.5", "Round.")], "6.5 gal")
table(["To convert", "Factor", "To convert", "Factor"],
      [["sq ft ↔ sq in", "144", "cu ft ↔ cu in", "1728"], ["sq yd ↔ sq ft", "9", "cu yd ↔ cu ft", "27"],
       ["sq yd ↔ sq in", "1296", "cu yd ↔ cu in", "46,656"], ["cu ft ↔ gal", "7.48", "gal ↔ cu in", "231"]],
      caption="Table 4.3  Area and volume factors. Multiply going to the smaller unit; divide going to the larger.", small=True)
shop("Ordering concrete",
     "A patio 20 ft long, 12 ft wide and 4 in thick has a volume of 20 × 12 × [[4|12]] = 80 cu ft. Divide by 27: 2.96 cu yd. "
     "The thickness had to be changed to feet first. All three dimensions must be in the same unit before multiplying.")

practice("Area and volume", "Convert. Round to the nearest tenth if needed.",
         [cv(*t) for t in [(850, "sq in", "sq ft", 144, 0), (12.5, "sq yd", "sq ft", 9, 1), (18, "sq ft", "sq in", 144, 1),
                           (2000, "sq in", "sq yd", 1296, 0), (400, "sq ft", "sq yd", 9, 0), (1800, "cu ft", "cu yd", 27, 0),
                           (4000, "cu in", "cu ft", 1728, 0), (16.5, "cu yd", "cu ft", 27, 1), (3.5, "cu ft", "cu in", 1728, 1),
                           (8, "cu ft", "gal", 7.48, 1), (2000, "cu in", "gal", 231, 0), (40, "gal", "cu ft", 7.48, 0),
                           (3, "gal", "cu in", 231, 1), (2, "cu yd", "cu in", 46656, 1), (120, "gal", "cu ft", 7.48, 0),
                           (0.5, "sq yd", "sq in", 1296, 1)]], cols=2)

summary(["Larger unit to smaller unit: multiply. Smaller unit to larger unit: divide.",
         "Length facts: 12 in per ft, 3 ft per yd, 36 in per yd, 5280 ft per mile.",
         "Area factors are length factors squared: 144, 9, 1296.",
         "Volume factors are length factors cubed: 1728, 27, 46,656.",
         "1 cu ft = 7.48 gal and 1 gal = 231 cu in.",
         "Check every answer: should the number have become larger or smaller?"])
review([cv(*t) for t in [(14, "ft", "in", 12, 1), (200, "in", "ft", 12, 0), (7, "lb", "oz", 16, 1), (7000, "lb", "T", 2000, 0),
                         (10, "qt", "gal", 4, 0), (600, "sq in", "sq ft", 144, 0), (25, "sq yd", "sq ft", 9, 1),
                         (500, "cu ft", "cu yd", 27, 0), (2.5, "cu ft", "cu in", 1728, 1), (12, "cu ft", "gal", 7.48, 1),
                         (1000, "cu in", "gal", 231, 0), (75, "gal", "cu ft", 7.48, 0)]]
       + [("Why is the factor from square feet to square inches 144 and not 12?",
           "A square foot is 12 in by 12 in, so it holds 12 × 12 = 144 square inches."),
          ("A floor is 270 sq ft. Tile is sold by the square yard. How many square yards are needed?", n(270 / 9) + " sq yd"),
          ("A trench needs 135 cu ft of gravel. How many cubic yards is that?", n(135 / 27) + " cu yd"),
          ("A rectangular tank has a volume of 30 cu ft. How many gallons does it hold?", n(30 * 7.48) + " gal"),
          ("How many inches are in 2 miles?", n(2 * 5280 * 12) + " in"),
          ("A 55-gallon drum has what volume in cubic inches?", n(55 * 231) + " cu in")])

# =====================================================================  5
chapter("The Metric System",
        ["Name the metric base units and the six common prefixes in order.",
         "Convert within the metric system by moving the decimal point.",
         "Convert between metric and standard units with the class conversion factors.",
         "Judge which of two units is larger.",
         "Carry out conversions that need more than one step."],
        "Refrigerant charge in grams, pipe in millimeters, pressure in kilopascals: metric units appear on nearly every "
        "piece of modern equipment. The good news is that the metric system was designed to be easy. Every conversion inside it is a move of the decimal point.",
        [("base unit", "The starting unit for a kind of measurement: meter (length), gram (weight), liter (capacity)."),
         ("prefix", "A word part put in front of the base unit that multiplies it by a power of ten."),
         ("metric stairs", "The seven prefixes written in order from kilo down to milli; also called the metric ladder.")])

sec("5.1 Base units and prefixes")
p("The metric system has one base unit for each kind of measurement, and the same set of prefixes works with all of them.")
table(["Measures", "Base unit", "Symbol", "About the size of"],
      [["length", "meter (meter)", "m", "a little more than a yard"], ["weight (mass)", "gram", "g", "a paper clip"],
       ["liquid capacity", "liter (liter)", "L", "a little more than a quart"]], widths=[22, 26, 14, 38])
table(["1,000<br>k", "100<br>h", "10<br>da", "1<br>one", "1/10 (.1)<br>d", "1/100 (.01)<br>c", "1/1000 (.001)<br>m"],
      [["kilometer **(km)**", "hectometer **(hm)**", "dekameter **(dam)**", "**meter (m)**", "decimeter **(dm)**", "centimeter **(cm)**", "millimeter **(mm)**"],
       ["kilogram **(kg)**", "hectogram **(hg)**", "dekagram **(dag)**", "**gram (g)**", "decigram **(dg)**", "centigram **(cg)**", "milligram **(mg)**"],
       ["kiloliter **(kL)**", "hectoliter **(hL)**", "dekaliter **(daL)**", "**liter (L)**", "deciliter **(dL)**", "centiliter **(cL)**", "milliliter **(mL)**"]],
      caption="Table 5.1  Metric Units (class handout)", small=True)
tip("Remembering the order",
    "A sentence whose words start with **k h da (unit) d c m** keeps the prefixes in order. A common one: "
    "**K**ing **H**enry **D**ied **U**nusually **D**rinking **C**hocolate **M**ilk.")

sec("5.2 Converting on the metric stairs")
p("Each step on the stairs is a factor of 10, and multiplying or dividing by 10 moves the decimal point one place. "
  "So a metric conversion is done by counting steps.")
fig(figs.stairs(), "The metric stairs. Every step holds a length unit, a weight unit and a capacity unit, and the same stairs serve all three.")
rule("Converting within the metric system",
     "**1.** Find the unit you have and the unit you want on the stairs.",
     "**2.** Count the steps between them.",
     "**3.** Move the decimal point that many places, **in the same direction you moved on the stairs**: "
     "going **down** toward milli (right on the chart), move the point **right**; going **up** toward kilo, move it **left**.",
     "Fill empty places with zeros.")
example("Convert 250 mm to centimeters.",
        [("mm → cm", "Centi is one step **up** the stairs from milli (one step left on the chart)."),
         ("250. → 25.0", "Move the decimal point one place left.")], "25 cm")
example("Convert 0.25 L to milliliters.",
        [("L → dL → cL → mL", "From the base unit to milli is three steps **down**."),
         ("0.25 → 0 250. ", "Move the point three places right. A zero must be added to fill the third place.")], "250 mL")
example("Convert 250 dg to dekagrams.",
        [("dg → g → dag", "Deci to deka is two steps **up**, passing the base unit."), ("250. → 2.50", "Move the point two places left.")],
        "2.5 dag")
warn("Count steps, not units",
     "From mm to m is **three** steps (mm → cm → dm → m), even though only two units are named in the problem. "
     "Point at each stair as you count. And remember the unit step: deka → base → deci is two moves.")
warn("m, mm and M",
     "Lowercase **m** alone is meter. As a prefix, lowercase **m** is milli (mm, mg, mL). Do not confuse millimeters with meters, "
     "or mg with g: the difference is a factor of 1000.")
sec("5.3 The stairs, one category at a time")
p("The stairs never change. Only the base unit changes with what is being measured.")
sub("Category 1: metric length (the meter)")
table(["km", "hm", "dam", "m", "dm", "cm", "mm"], [["kilometer", "hectometer", "dekameter", "**meter**", "decimeter", "centimeter", "millimeter"],
      ["1000 m", "100 m", "10 m", "1 m", "0.1 m", "0.01 m", "0.001 m"]], small=True)
p("The units used most are the **kilometer** (road distances), the **meter** (rooms and pipe runs), the **centimeter** and the **millimeter** (parts and drawings). "
  "Worth knowing by heart: 1 m = 100 cm = 1000 mm, 1 cm = 10 mm, 1 km = 1000 m.")
example("A pipe is 3.2 m long. Give its length in centimeters and in millimeters.",
        [("m → dm → cm: 2 steps down", "Move the point 2 places right."), ("3.2 → 320 cm", ""),
         ("m → dm → cm → mm: 3 steps down", "Move the point 3 places right."), ("3.2 → 3200 mm", "")], "320 cm;  3200 mm")
example("Convert 4750 m to kilometers.",
        [("m → dam → hm → km: 3 steps up", "Move the point 3 places left."), ("4750. → 4.750", "")], "4.75 km")
sub("Category 2: metric weight (the gram)")
table(["kg", "hg", "dag", "g", "dg", "cg", "mg"], [["kilogram", "hectogram", "dekagram", "**gram**", "decigram", "centigram", "milligram"],
      ["1000 g", "100 g", "10 g", "1 g", "0.1 g", "0.01 g", "0.001 g"]], small=True)
p("The **kilogram**, the **gram** and the **milligram** do nearly all the work: 1 kg = 1000 g and 1 g = 1000 mg.")
example("A refrigerant charge is 1.36 kg. How many grams is that?",
        [("kg → hg → dag → g: 3 steps down", "Move the point 3 places right."), ("1.36 → 1360", "Fill the empty place with a zero.")], "1360 g")
example("Convert 85 cg to grams.",
        [("cg → dg → g: 2 steps up", "Move the point 2 places left."), ("85. → 0.85", "")], "0.85 g")
sub("Category 3: metric capacity (the liter)")
table(["kL", "hL", "daL", "L", "dL", "cL", "mL"], [["kiloliter", "hectoliter", "dekaliter", "**liter**", "deciliter", "centiliter", "milliliter"],
      ["1000 L", "100 L", "10 L", "1 L", "0.1 L", "0.01 L", "0.001 L"]], small=True)
p("The **liter** and the **milliliter** are the everyday units: 1 L = 1000 mL.")
example("A sample bottle holds 475 mL. How many liters is that?",
        [("mL → cL → dL → L: 3 steps up", "Move the point 3 places left."), ("475. → 0.475", "")], "0.475 L")
example("Convert 2.6 daL to deciliters.",
        [("daL → L → dL: 2 steps down", "Deka to deci passes the base unit: two steps. Move the point 2 places right."), ("2.6 → 260", "")], "260 dL")
sub("The larger prefixes and the smaller ones")
p("Science and electronics reach beyond the seven stairs. These prefixes step by a factor of 1000, three decimal places at a time.")
table(["Name", "The Number", "Prefix", "Symbol"],
      [["trillion", "1,000,000,000,000", "tera", "T"], ["billion", "1,000,000,000", "giga", "G"], ["million", "1,000,000", "mega", "M"],
       ["thousand", "1,000", "kilo", "k"], ["hundred", "100", "hecto", "h"], ["ten", "10", "deka", "da"], ["**unit**", "**1**", "", ""],
       ["tenth", "0.1", "deci", "d"], ["hundredth", "0.01", "centi", "c"], ["thousandth", "0.001", "milli", "m"],
       ["millionth", "0.000 001", "micro", "µ"], ["billionth", "0.000 000 001", "nano", "n"], ["trillionth", "0.000 000 000 001", "pico", "p"]],
      caption="Table 5.2  Prefixes (class handout)", small=True)
p("Examples from the trades: megohm (MΩ), kilowatt (kW), milliamp (mA), microfarad (µF), picofarad (pF).")


def mc(val, a, b, steps):
    return (f"{n(val)} {a} to {b}", f"{n(val * 10 ** steps)} {b}")


practice("Metric to metric", "Convert by moving the decimal point.",
         [mc(*t) for t in [(4.5, "m", "cm", 2), (380, "mm", "cm", -1), (2.4, "km", "m", 3), (750, "g", "kg", -3),
                           (0.6, "L", "mL", 3), (1250, "mL", "L", -3), (35, "cm", "mm", 1), (8200, "m", "km", -3),
                           (460, "dg", "dag", -2), (3.2, "hL", "L", 2), (0.085, "kg", "g", 3), (95, "cm", "m", -2),
                           (7, "dam", "dm", 2), (12500, "mg", "g", -3), (0.4, "m", "mm", 3), (64, "cL", "L", -2)]], cols=2)

sec("5.4 Between metric and standard")
p("Moving between the two systems needs conversion factors again. The course uses the seven below. Each line is a fact, "
  "and the multiply-or-divide rule from Chapter 4 applies: toward the **smaller** unit multiply, toward the **larger** unit divide.")
table(["LENGTH", "WEIGHT", "CAPACITY"],
      [["1 in. = 2.54 cm", "1 oz. = 28.35 g", "1 liter = 1.06 qts."], ["1 meter = 3.28 ft.", "1 kg = 2.205 lbs.", "1 gal. = 3.785 L"], ["1 mile = 1.61 km", "", ""]],
      caption="Table 5.3  Standard / Metric Conversions (class handout)")
rule("Which unit is larger?",
     "In each fact, the unit with the **1** in front of it is the larger unit, because it takes more than one of the other to match it.",
     "An inch is larger than a centimeter. A meter is larger than a foot (and a yard). A mile is larger than a kilometer. "
     "An ounce is larger than a gram. A kilogram is larger than a pound. A liter is larger than a quart. A gallon is larger than a liter.")
example("Convert 50 cm to inches. Round to the nearest tenth.",
        [("1 in = 2.54 cm", "The connecting fact. The inch is the larger unit."), ("cm → in: smaller → larger", "Divide."),
         ("50 ÷ 2.54 = 19.685…", "Divide by the factor."), ("19.7", "Round.")], "19.7 in")
example("Convert 185 lb to kilograms. Round to the nearest tenth.",
        [("1 kg = 2.205 lb", "The kilogram is the larger unit."), ("lb → kg: smaller → larger", "Divide."),
         ("185 ÷ 2.205 = 83.900…", "Divide."), ("83.9", "Round.")], "83.9 kg")
example("Convert 50 L to quarts.",
        [("1 L = 1.06 qt", "The liter is the larger unit."), ("L → qt: larger → smaller", "Multiply."), ("50 × 1.06 = 53", "Multiply.")], "53 qt")
p("The three examples above come from the three categories. Each category is now set out in full, in both directions.")
sub("Category 1: length (inch and centimeter, meter and foot, mile and kilometer)")
fig(figs.stack([figs.chain(["inch", "centimeter"], ["2.54"], figs.BLUE), figs.chain(["meter", "foot"], ["3.28"], figs.BLUE),
                figs.chain(["mile", "kilometer"], ["1.61"], figs.BLUE)]), "Length between the systems.")
table(["Fact", "Multiply", "Divide"],
      [["1 in = 2.54 cm", "in → cm: × 2.54", "cm → in: ÷ 2.54"], ["1 m = 3.28 ft", "m → ft: × 3.28", "ft → m: ÷ 3.28"],
       ["1 mi = 1.61 km", "mi → km: × 1.61", "km → mi: ÷ 1.61"]], small=True)
example("A room is 4.5 m long. How many feet is that, to the nearest tenth?",
        [("1 m = 3.28 ft", "The meter is the larger unit."), ("4.5 × 3.28 = 14.76", "Meters to feet: multiply."), ("14.8", "Round.")], "14.8 ft")
example("A job site is 12 km away. How many miles is that, to the nearest tenth?",
        [("1 mi = 1.61 km", "The mile is the larger unit."), ("12 ÷ 1.61 = 7.453…", "Kilometers to miles: divide."), ("7.5", "Round.")], "7.5 mi")
sub("Category 2: weight (ounce and gram, kilogram and pound)")
fig(figs.stack([figs.chain(["ounce", "gram"], ["28.35"], figs.GOLD), figs.chain(["kilogram", "pound"], ["2.205"], figs.GOLD)]), "Weight between the systems.")
table(["Fact", "Multiply", "Divide"],
      [["1 oz = 28.35 g", "oz → g: × 28.35", "g → oz: ÷ 28.35"], ["1 kg = 2.205 lb", "kg → lb: × 2.205", "lb → kg: ÷ 2.205"]], small=True)
example("A nameplate gives a charge of 14 oz. How many grams is that?",
        [("1 oz = 28.35 g", "The ounce is the larger unit."), ("14 × 28.35 = 396.9", "Ounces to grams: multiply.")], "396.9 g")
example("A motor has a mass of 32 kg. How many pounds is that, to the nearest tenth?",
        [("1 kg = 2.205 lb", "The kilogram is the larger unit."), ("32 × 2.205 = 70.56", "Kilograms to pounds: multiply."), ("70.6", "Round.")], "70.6 lb")
sub("Category 3: capacity (liter and quart, gallon and liter)")
fig(figs.stack([figs.chain(["liter", "quart"], ["1.06"], figs.PURPLE), figs.chain(["gallon", "liter"], ["3.785"], figs.PURPLE)]), "Capacity between the systems.")
table(["Fact", "Multiply", "Divide"],
      [["1 L = 1.06 qt", "L → qt: × 1.06", "qt → L: ÷ 1.06"], ["1 gal = 3.785 L", "gal → L: × 3.785", "L → gal: ÷ 3.785"]], small=True)
example("A sump holds 12 gal. How many liters is that, to the nearest tenth?",
        [("1 gal = 3.785 L", "The gallon is the larger unit."), ("12 × 3.785 = 45.42", "Gallons to liters: multiply."), ("45.4", "Round.")], "45.4 L")
example("An oil charge is 8 qt. How many liters is that, to the nearest tenth?",
        [("1 L = 1.06 qt", "The liter is the larger unit."), ("8 ÷ 1.06 = 7.547…", "Quarts to liters: divide."), ("7.5", "Round.")], "7.5 L")
sub("Conversions with more than one step")
p("If the unit you have is not one of the units in the table, first move along the metric stairs or use a standard fact "
  "to reach a unit that is. Write down each step with its unit.")
example("Convert 5 km to inches. Round to the nearest whole number.",
        [("5 km = 500,000 cm", "The table joins inches to **centimeters**. From kilo to centi is five steps down: move the point five places right."),
         ("500,000 ÷ 2.54 = 196,850.39…", "Centimeters to inches: smaller to larger, divide by 2.54."),
         ("196,850", "Round to the nearest whole number.")], "196,850 in")
example("A recovery cylinder holds 30 lb of refrigerant. How many grams is that? Round to the nearest whole number.",
        [("30 ÷ 2.205 = 13.6054… kg", "Pounds to kilograms: divide. Keep the digits in the calculator."),
         ("13.6054… kg = 13,605.4… g", "Kilograms to grams: three steps down the stairs."), ("13,605", "Round at the end.")], "13,605 g")
shop("Why technicians need both systems",
     "Refrigerant charge on a nameplate may be given in ounces and in grams. Torque specs appear in foot-pounds and newton-meters. "
     "Imported equipment is dimensioned in millimeters, but the tape on your belt reads inches. A quick mental check helps: "
     "an inch is about 25 mm, a kilogram is a little over 2 lb, and a liter is about a quart.")


def xc(val, a, b, factor, mult, places=1):
    ans = val * factor if mult else val / factor
    return (f"{n(val)} {a} to {b}", f"{r(ans, places)} {b}")


practice("Metric and standard", "Convert. Round to the nearest tenth if needed. For 13 to 16, circle (name) the larger unit.",
         [xc(*t) for t in [(12, "in", "cm", 2.54, 1), (80, "cm", "in", 2.54, 0), (25, "m", "ft", 3.28, 1), (100, "ft", "m", 3.28, 0),
                           (26.2, "mi", "km", 1.61, 1), (10, "km", "mi", 1.61, 0), (8, "oz", "g", 28.35, 1), (500, "g", "oz", 28.35, 0),
                           (70, "kg", "lb", 2.205, 1), (220, "lb", "kg", 2.205, 0), (20, "L", "qt", 1.06, 1), (15, "gal", "L", 3.785, 1)]]
         + [("centimeter or inch", "inch"), ("liter or quart", "liter"), ("gram or ounce", "ounce"), ("kilometer or mile", "mile")], cols=2)

practice("Conversions by category", "Convert. Round to the nearest tenth if needed. 1 to 6 length, 7 to 12 weight, 13 to 18 capacity.",
         [mc(*t) for t in [(2.75, "m", "cm", 2), (640, "mm", "m", -3), (3.4, "km", "m", 3)]]
         + [xc(*t) for t in [(18, "in", "cm", 2.54, 1), (60, "ft", "m", 3.28, 0), (55, "mi", "km", 1.61, 1)]]
         + [mc(*t) for t in [(2.2, "kg", "g", 3), (350, "mg", "g", -3), (48, "g", "cg", 2)]]
         + [xc(*t) for t in [(24, "oz", "g", 28.35, 1), (1000, "g", "oz", 28.35, 0), (45, "kg", "lb", 2.205, 1)]]
         + [mc(*t) for t in [(1.5, "L", "mL", 3), (2400, "mL", "L", -3), (36, "dL", "L", -1)]]
         + [xc(*t) for t in [(30, "qt", "L", 1.06, 0), (60, "L", "gal", 3.785, 0), (7.5, "gal", "L", 3.785, 1)]], cols=3)

summary(["Base units: meter, gram, liter. Prefixes in order: kilo, hecto, deka, (unit), deci, centi, milli.",
         "Inside the metric system, count the steps on the stairs and move the decimal point that many places, the same direction.",
         "Between systems use the facts 2.54, 3.28, 1.61, 28.35, 2.205, 1.06 and 3.785.",
         "The unit written with the 1 is the larger unit; multiply toward smaller units, divide toward larger ones.",
         "For multi-step conversions, write each step with its unit and round only at the end."])
review([mc(*t) for t in [(6.8, "m", "mm", 3), (425, "cm", "m", -2), (0.75, "kg", "g", 3), (900, "mL", "L", -3), (52, "dg", "dag", -2),
                         (1.2, "km", "cm", 5)]]
       + [xc(*t) for t in [(36, "in", "cm", 2.54, 1), (150, "cm", "in", 2.54, 0), (5, "kg", "lb", 2.205, 1), (160, "lb", "kg", 2.205, 0),
                           (40, "L", "qt", 1.06, 1), (5, "gal", "L", 3.785, 1), (26, "qt", "L", 1.06, 0), (400, "km", "mi", 1.61, 0)]]
       + [("Which is larger, a meter or a yard?", "a meter (1 m = 3.28 ft, and a yard is 3 ft)"),
          ("Which is larger, a gallon or a cubic foot?", "a cubic foot (it holds 7.48 gallons)"),
          ("Convert 2 m to inches, to the nearest tenth. (Hint: go through centimeters.)", r(200 / 2.54, 1) + " in"),
          ("Convert 3 lb to grams, to the nearest whole number.", r(3 / 2.205 * 1000, 0) + " g"),
          ("A pipe is 19 mm in diameter. What is that in inches, to the nearest hundredth?", r(1.9 / 2.54, 2) + " in"),
          ("How many steps, and in which direction, does the decimal point move from hectoliters to centiliters?", "4 places to the right")])

# =====================================================================  6
chapter("Rulers, Gauges and Tolerance",
        ["Read a metric rule in millimeters and centimeters.",
         "Read an inch rule to the nearest sixteenth and give the reading in lowest terms.",
         "Estimate the reading of a dial gauge, including a gauge with two scales.",
         "Find the upper and lower limits of a toleranced dimension and decide whether a part is acceptable.",
         "Find a missing dimension on a drawing."],
        "A calculation is only as good as the measurement that goes into it. This chapter is about reading instruments "
        "correctly, and about deciding whether a measurement is close enough.",
        [("graduation", "One of the marks on a scale."),
         ("scale value", "What the space between two neighboring marks is worth."),
         ("tolerance", "How far a dimension is allowed to vary from the size called for."),
         ("limits", "The largest and smallest acceptable sizes."),
         ("nominal size", "The size called for on the drawing, before the tolerance is applied.")])

sec("6.1 The metric rule")
p("On a metric rule the numbered marks are **centimeters**. Each centimeter is divided into 10 equal parts, and each "
  "small part is one **millimeter**. A slightly longer mark shows the halfway point, 5 mm.")
rule("Reading a metric rule in millimeters",
     "Multiply the last numbered centimeter mark before the point by 10, then add the small marks past it.",
     "A point 6 small marks past the 4 is 40 + 6 = 46 mm, which is also 4.6 cm.")
fig(figs.ruler(inch_marks=[("F", 10), ("G", 27), ("H", 38), ("I", 52)], mm_marks=[("A", 8), ("B", 29), ("C", 46), ("D", 66), ("E", 93)]),
    "A rule with a centimeter scale on the top edge and an inch scale in sixteenths on the bottom edge.")
example("Read points A to E on the metric scale of Figure 6.1, in millimeters.",
        [("A: 8 marks from zero", "Before the 1 cm mark, so just count: 8 mm."), ("B: 2 cm + 9 marks = 29", "One mark short of 3 cm."),
         ("C: 4 cm + 6 marks = 46", "One mark past the long 5 mm mark."), ("D: 6 cm + 6 marks = 66", ""), ("E: 9 cm + 3 marks = 93", "")],
        "A 8 mm, B 29 mm, C 46 mm, D 66 mm, E 93 mm")

sec("6.2 The inch rule")
p("An inch rule is divided by halving, again and again. Half of an inch is [[1|2]], half of that is [[1|4]], then [[1|8]], then "
  "[[1|16]]. The marks are made in different lengths so the eye can pick them out: **the longer the mark, the larger the fraction.**")
fig(figs.inch_zoom(), "One inch divided into sixteenths. Every mark has a name in lowest terms.")
rule("Reading an inch rule",
     "**1.** Write down the last whole inch before the point.",
     "**2.** Count the sixteenth spaces from that inch mark to the point.",
     "**3.** Write the count over 16 and reduce: keep halving top and bottom until the top is odd.")
example("Read points F to I on the inch scale of Figure 6.1.",
        [("F: 0 in + 10 sixteenths = [[10|16]] = [[5|8]]", "Ten spaces from zero. Reduce by 2."),
         ("G: 1 in + 11 sixteenths = 1 [[11|16]]", "Eleven is odd, so it is already in lowest terms."),
         ("H: 2 in + 6 sixteenths = 2 [[6|16]] = 2 [[3|8]]", "Reduce by 2."),
         ("I: 3 in + 4 sixteenths = 3 [[4|16]] = 3 [[1|4]]", "Reduce by 4. This is the quarter-inch mark, the third-longest line.")],
        "F [[5|8]] in, G 1 [[11|16]] in, H 2 [[3|8]] in, I 3 [[1|4]] in")
tip("Count from the nearest long mark",
    "Counting eleven tiny spaces invites mistakes. Instead, find the nearest half-inch mark (that is [[8|16]]) and count from there: "
    "three marks past the half is [[11|16]]. One mark before the next inch is [[15|16]].")
warn("Always reduce",
     "An answer of 2 [[6|16]] is the right place on the ruler but is not finished. Readings are given in lowest terms: 2 [[3|8]].")
sub("Rules with other divisions")
p("Some rules are divided into 8ths, 32nds or 64ths, and engineers’ and machinists’ rules are divided into 10ths and 100ths. "
  "The method never changes: **count how many spaces make one inch**, and that count is the denominator.")

sixt = [3, 12, 22, 29, 40, 46, 57, 62]
mms = [14, 37, 52, 78, 95]
fig(figs.ruler(inch_marks=list(zip("FGHJKLMN", sixt)), mm_marks=list(zip("ABCDE", mms))), "Rule for Practice 6.1.")
practice("Reading a rule", "Use Figure 6.3. Give A to E in millimeters. Give F to N in inches, in lowest terms.",
         [(f"Point {c}", f"{m} mm") for c, m in zip("ABCDE", mms)]
         + [(f"Point {c}", fr(Fraction(s, 16)) + " in") for c, s in zip("FGHJKLMN", sixt)]
         + [("Write the reading for point C in centimeters.", n(mms[2] / 10) + " cm"),
            ("How many millimeters is it from point A to point D?", f"{mms[3] - mms[0]} mm"),
            ("How far is it from point G to point K, in inches?", fr(Fraction(sixt[4] - sixt[1], 16)) + " in")], cols=3)

sec("6.3 Reading gauges and meters")
p("A dial is a ruler bent into an arc. The same question unlocks every one of them: **what is each small space worth?**")
rule("Finding the scale value",
     "**1.** Pick two neighboring **numbered** marks and subtract them.",
     "**2.** Count the **spaces** between them (spaces, not marks).",
     "**3.** Divide: value of one space = difference ÷ number of spaces.",
     "**4.** Read the needle: last numbered mark + spaces past it × value of a space. If the needle is between two marks, estimate.")
fig(figs.side_by_side([figs.gauge(0, 1000, 200, 50, 870, "mbar", "pressure"), figs.gauge(0, 500, 100, 25, 385, "VOLTS", "voltmeter")]),
    "Two dials. Left: numbered every 200 with 4 spaces between numbers. Right: numbered every 100 with 4 spaces.")
example("Estimate the reading of the pressure gauge on the left of Figure 6.4.",
        [("200 − 0 = 200", "Two neighboring numbers differ by 200."), ("200 ÷ 4 spaces = 50 per space", "There are four spaces between numbered marks."),
         ("800 + 1 space = 850", "The needle is past 800 and past the first small mark."),
         ("850 + a little less than half a space ≈ 870", "It sits not quite halfway to 900. Half a space would be 25, so estimate about 20.")],
        "about 870 mbar")
p("On the voltmeter at the right, each space is 100 ÷ 4 = 25 volts. The needle is three spaces past 300 (that is 375) and a bit "
  "more, so the reading is about 385 volts. An estimate between marks will differ slightly from person to person; "
  "385 and 390 are both reasonable, 350 is not.")
warn("Count spaces, and check your scale value",
     "If you think each space is worth 20, count by 20s from one number to the next. If you do not land exactly on the next number, "
     "the scale value is wrong. On the gauge above: 0, 50, 100, 150, 200. It lands, so 50 is right.")
sub("Gauges with two scales")
p("Many pressure gauges carry two scales on one face, for example **kPa** on the outer ring and **psi** on the inner ring. "
  "There is one needle but two readings, and each scale has its **own** numbers and its own scale value.")
bullets(["Decide which scale the question asks for, and look only at that ring of numbers.",
         "Work out the scale value for that ring separately. The outer ring might be worth 1000 per space while the inner is worth 100.",
         "Follow the needle to the ring you are reading. Do not read the psi position against the kPa numbers.",
         "As a check, 1 psi is about 6.9 kPa, so the kPa reading should be roughly 7 times the psi reading."])
example("A dual-scale gauge reads 6000 kPa on its outer scale. Use the check above to estimate what the inner psi scale should read.",
        [("6000 ÷ 6.9 = 869.6", "kPa is the smaller unit, so the psi number is smaller: divide."), ("≈ 870", "A reading between 860 and 880 psi is consistent.")],
        "about 870 psi")

gs = [(0, 100, 20, 5, 65, "psi"), (0, 1000, 200, 40, 340, "°F"), (8, 18, 2, 0.5, 13.5, "volts"), (0, 300, 100, 20, 210, "psi"),
      (0, 60, 10, 2, 47, "amps"), (0, 500, 100, 25, 140, "kPa")]
fig(figs.side_by_side([figs.gauge(a, b, c, d, v, u, size=200) for a, b, c, d, v, u in gs[:3]]), "Gauges A, B and C for Practice 6.2.")
fig(figs.side_by_side([figs.gauge(a, b, c, d, v, u, size=200) for a, b, c, d, v, u in gs[3:]]), "Gauges D, E and F for Practice 6.2.")
its = []
for c, g in zip("ABCDEF", gs):
    its.append((f"Gauge {c}: what is one small space worth?", f"{n(g[3])} {g[5]}"))
    its.append((f"Gauge {c}: estimate the reading.", f"about {n(g[4])} {g[5]}"))
practice("Reading gauges", "Use Figures 6.5 and 6.6. Estimates within half a space of the answer are acceptable.", its, cols=2)

sec("6.4 Tolerance")
p("Nothing can be made to an exact size. A drawing therefore gives a **nominal** size and a **tolerance**, the amount the part "
  "may be over or under. The sign **±** is read “plus or minus.”")
rule("Limits of a dimension", "upper limit = nominal size + tolerance", "lower limit = nominal size − tolerance",
     "A part is acceptable if its size is anywhere from the lower limit to the upper limit, including the limits themselves.")
fig(figs.tolerance(0.81, 0.003, 0.8125), "The tolerance band for 0.81 ± 0.003 in. The arrow marks a 13/16-in hole at 0.8125 in.")
example("A hole is specified as 0.81 in ± 0.003 in. (a) What are the limits? (b) Will a hole drilled with a [[13|16]]-in bit be within specification?",
        [("0.810 + 0.003 = 0.813", "(a) Upper limit. Write 0.81 as 0.810 so the decimal places line up."),
         ("0.810 − 0.003 = 0.807", "Lower limit."),
         ("13 ÷ 16 = 0.8125", "(b) Change the drill size to a decimal so it can be compared."),
         ("0.807 ≤ 0.8125 ≤ 0.813", "Compare using four decimal places: 0.8070, 0.8125, 0.8130. It lies between the limits.")],
        "(a) 0.807 in to 0.813 in   (b) Yes")
warn("Line up the decimal places before adding",
     "0.81 + 0.003 is not 0.84 and not 0.813 by luck. Write 0.810 + 0.003. A tolerance usually has more decimal places than the nominal size.")
sub("Fraction and percent tolerances")
p("Tolerances on a tape-measure job are fractions: 24 [[1|2]] in ± [[1|16]] in gives limits of 24 [[7|16]] in and 24 [[9|16]] in. "
  "Electrical parts are often toleranced by percent: a 200-ohm resistor at ±5% may be off by 5% of 200 = 10 ohms, so its limits are 190 and 210 ohms.")

sec("6.5 Finding a missing dimension")
p("Drawings rarely repeat information. If the overall length and all but one of the parts are given, the missing part is found by "
  "subtracting. The idea is simply: **the parts add up to the whole.**")
rule("Missing length", "missing part = overall length − (sum of the known parts)",
     "Change every dimension to the same form first: all decimals or all fractions.")
example("A bar is 78 [[3|4]] in long overall. It is marked in three sections. The first is 11.25 in and the third is 31 [[3|8]] in. "
        "How long is the middle section? Do not round.",
        [("78 [[3|4]] = 78.75;  31 [[3|8]] = 31.375", "Change the fractions to decimals."),
         ("78.750 − 11.250 − 31.375", "Subtract each known part from the overall length."),
         ("= 36.125", "No rounding is needed or allowed."), ("0.125 = [[1|8]]", "As a mixed number, if wanted.")],
        "36.125 in, or 36 [[1|8]] in")
tol = [("2.50", "0.01", "2.495"), ("0.375", "0.005", "0.382"), ("1.25", "0.002", "1.2485"), ("4.0", "0.05", "3.94"),
       ("0.62", "0.003", "5/8"), ("0.44", "0.004", "7/16")]
its = []
for nom, t, test in tol:
    lo, hi = F(nom) - F(t), F(nom) + F(t)
    ok = lo <= F(test) <= hi
    tv = frtxt(test)
    extra = f" ({n(float(F(test)))})" if "/" in test else ""
    its.append((f"{nom} in ± {t} in. Find the limits. Is a part measuring {tv} in acceptable?",
                f"{n(float(lo))} in to {n(float(hi))} in; {'yes' if ok else 'no'}{extra}"))
miss = [("60", ["14.5", "22 3/8"]), ("96 1/2", ["18.25", "40 5/8"]), ("42 3/8", ["9.75", "12 1/2", "6.125"]), ("120", ["33 7/8", "33 7/8", "20.5"])]
for tot, parts in miss:
    v = F(tot) - sum(F(x) for x in parts)
    its.append((f"Overall length {frtxt(tot)} in; known parts " + ", ".join(frtxt(x) + " in" for x in parts) + ". Find the missing part.",
                f"{n(float(v))} in = {fr(v)} in"))
its += [("A 150-Ω resistor has a tolerance of ±10%. What are its limits?", "135 Ω to 165 Ω"),
        ("A stud is to be cut 92 [[5|8]] in ± [[1|8]] in. What are the limits?", f"{fr(F('92 5/8') - Fraction(1, 8))} in to {fr(F('92 5/8') + Fraction(1, 8))} in")]
practice("Tolerance and missing lengths", "Do not round.", its, cols=1)

summary(["Metric rule: the numbers are centimeters and each small space is 1 mm.",
         "Inch rule: count sixteenths past the last whole inch, then reduce the fraction.",
         "Gauge: scale value = difference between numbered marks ÷ number of spaces between them.",
         "On a dual-scale gauge, read each scale with its own numbers and its own scale value.",
         "Limits = nominal ± tolerance. A part on or between the limits is acceptable.",
         "A missing dimension is the overall length minus the known parts."])
review([("How many millimeters are in 7.3 cm?", "73 mm"),
        ("A point is 4 small marks past the 6 on a centimeter scale. Give the reading in mm.", "64 mm"),
        ("On an inch rule in sixteenths, a point is 12 spaces past the 2. Give the reading in lowest terms.", "2 [[3|4]] in"),
        ("A point is 14 sixteenths past the 5-inch mark. Give the reading in lowest terms.", "5 [[7|8]] in"),
        ("Which mark is longer on an inch rule, [[3|8]] or [[3|4]]?", "[[3|4]] (quarter marks are longer than eighth marks)"),
        ("A gauge is numbered 0, 40, 80, 120 with 8 spaces between numbers. What is each space worth?", "5"),
        ("On that gauge the needle is 3 spaces past 80. What is the reading?", "95"),
        ("A gauge is numbered every 500 with 5 spaces between numbers. The needle is halfway between the 2nd and 3rd marks past 1500. Estimate the reading.", "about 1750"),
        ("A dual-scale gauge reads 100 psi. About what should the kPa scale read?", "about 690 kPa"),
        ("Find the limits of 1.75 in ± 0.015 in.", "1.735 in to 1.765 in"),
        ("A shaft must be 0.50 in ± 0.002 in. Is a shaft measuring 0.5025 in acceptable?", "No. The upper limit is 0.502 in."),
        ("A hole must be 0.69 in ± 0.005 in. Is an [[11|16]]-in hole acceptable?", "Yes. 11/16 = 0.6875, and the limits are 0.685 to 0.695."),
        ("Overall length 54 [[1|4]] in; known parts 20.5 in and 16 [[3|8]] in. Find the missing part without rounding.",
         f"{n(float(F('54 1/4') - F('20.5') - F('16 3/8')))} in"),
        ("Four equal spaces and two end margins of 1.25 in make up a 30-in panel. How wide is each space?", n((30 - 2.5) / 4) + " in")])
