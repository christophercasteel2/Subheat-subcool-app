"""Section 2.1: ratio and proportion (new material, written with the new numbering)."""
from fractions import Fraction
from book import *  # noqa: F401,F403
from util import n, r, fr
import figs

chapter("Ratio and Proportion",
        ["Write a ratio in lowest terms, with both quantities in the same unit.",
         "Find a rate and a unit rate.",
         "Solve a proportion by cross-multiplying.",
         "Use proportions for scale drawings, mixtures and recipes.",
         "Solve gear and pulley problems, where the quantities are inversely proportional."],
        "A mixing ratio on a can of two-cycle oil, the pitch of a roof, the speed of a driven pulley: all are comparisons of two numbers. "
        "This section is about writing those comparisons and using them to find a missing value.",
        [("ratio", "A comparison of two quantities by division, written 3 to 4, 3:4 or [[3|4]]."),
         ("rate", "A ratio of two different kinds of quantity, such as miles per hour or dollars per foot."),
         ("unit rate", "A rate per one unit: 55 miles per **1** hour."),
         ("proportion", "A statement that two ratios are equal."),
         ("direct proportion", "Both quantities grow together: twice the length, twice the cost."),
         ("inverse proportion", "One quantity grows as the other shrinks: a larger pulley turns more slowly.")])

sec("2.1 Ratios")
p("A **ratio** compares two numbers by dividing one by the other. A drive pulley 12 in across turning a pulley 4 in across has a ratio of "
  "12 to 4. It can be written three ways, and all three mean the same thing:")
eq("12 to 4          12 : 4          [[12|4]]")
p("Like a fraction, a ratio is usually reduced to lowest terms. 12 : 4 reduces to 3 : 1, “three to one.” Unlike a fraction, a ratio such as "
  "[[3|1]] is left as a ratio; it is not rewritten as the whole number 3.")
rule("Writing a ratio",
     "**1.** Put the quantities in the order the words give them: “the ratio of A to B” is A : B, with A on top.",
     "**2.** Change both quantities to the **same unit**.",
     "**3.** Reduce to lowest terms. The unit cancels, so a ratio has no unit.")
example("A sheet of plywood is 8 ft long and 48 in wide. What is the ratio of its length to its width?",
        [("8 ft = 96 in", "The units must match before dividing."), ("[[96|48]]", "Length first, because the question names it first."),
         ("[[96 ÷ 48|48 ÷ 48]] = [[2|1]]", "Reduce. The inches cancel.")], "2 : 1")
warn("Same units first", "8 ft to 48 in is **not** 8 : 48 = 1 : 6. Comparing feet with inches gives a ratio that is wrong by a factor of 12.")
example("A two-cycle engine is fueled with 2.5 gal of gasoline mixed with 6.4 fl oz of oil. A gallon is 128 fl oz. What is the ratio of gasoline to oil?",
        [("2.5 × 128 = 320 fl oz", "Gasoline in fluid ounces."), ("[[320|6.4]] = 50", "Divide."), ("50 : 1", "Written as a ratio.")], "50 : 1",
        title="A mixing ratio")
sub("Rates")
p("When the two quantities are different kinds of thing, such as miles and hours or dollars and feet, the comparison is called a **rate**, and the units stay "
  "in the answer. A rate divided down to “per one” is a **unit rate**.")
example("A 250-ft coil of wire costs $112.50. What is the cost per foot?",
        [("[[$112.50|250 ft]]", "Cost over length."), ("112.50 ÷ 250 = 0.45", "Divide down to one foot.")], "$0.45 per ft", title="A unit rate")
example("A pump moves 1,350 gallons in 45 minutes. What is its rate in gallons per minute?",
        [("1,350 ÷ 45 = 30", "Gallons divided by minutes.")], "30 gal per min (gpm)")

practice("Ratios and rates", "Write ratios in lowest terms. Give rates with their units.",
         [("12 to 18", "2 : 3"), ("45 : 15", "3 : 1"), ("[[16|24]]", "2 : 3"), ("2 ft to 8 in", "3 : 1"), ("3 yd to 4 ft", "9 : 4"), ("1 gal to 3 qt", "4 : 3"),
          ("90 min to 2 h", "3 : 4"), ("1.5 to 4.5", "1 : 3"), ("A 15-in pulley drives a 5-in pulley. Ratio of the large to the small?", "3 : 1"),
          ("A gear with 48 teeth meshes with one of 18 teeth. Ratio of the large gear to the small?", "8 : 3"),
          ("A roof rises 6 in for every 12 in of run. Ratio of rise to run?", "1 : 2"),
          ("1 gal of gasoline (128 fl oz) is mixed with 3.2 fl oz of oil. Ratio of gasoline to oil?", "40 : 1"),
          ("A truck uses 18 gal of fuel in 324 mi. Find the miles per gallon.", "18 mi per gal"),
          ("A crew lays 840 sq ft of tile in 3.5 days. Find the square feet per day.", "240 sq ft per day"),
          ("50 ft of pipe costs $87.50. Find the cost per foot.", "$1.75 per ft"),
          ("A motor turns 10,500 revolutions in 6 minutes. Find the rpm.", "1,750 rpm")], cols=2)

sec("2.2 Proportions")
p("A **proportion** says that two ratios are equal: [[3|4]] = [[9|12]]. Proportions are true when the **cross products** are equal: 3 × 12 = 36 and 4 × 9 = 36. "
  "That fact is what solves them. If one of the four numbers is unknown, cross-multiply and divide, exactly as in the percent proportion of Section 2.3.")
rule("Solving a proportion", "**1.** Set up the two ratios with **like quantities in the same position** (the same unit on top on both sides).",
     "**2.** Multiply the two numbers that are diagonal from each other.", "**3.** Divide by the number that is left over.")
example("Solve [[x|15]] = [[8|24]].",
        [("8 × 15 = 120", "Multiply the diagonal pair with two numbers."), ("120 ÷ 24 = 5", "Divide by the number left over.")], "x = 5")
example("If 5 gallons of paint cover 1,750 sq ft, how many gallons are needed for 4,900 sq ft?",
        [("[[5 gal|1,750 sq ft]] = [[x gal|4,900 sq ft]]", "Gallons on top on both sides, square feet on the bottom."),
         ("5 × 4,900 = 24,500", "Cross-multiply."), ("24,500 ÷ 1,750 = 14", "Divide.")], "14 gal", title="A direct proportion")
sub("Scale drawings")
p("A blueprint is drawn to a **scale**, such as [[1|4]] in = 1 ft. Every length on the drawing is in the same ratio to the real length, so a proportion converts one to the other.")
example("On a drawing at [[1|4]] in = 1 ft, a wall measures 6 [[3|8]] in. How long is the real wall?",
        [("[[0.25 in|1 ft]] = [[6.375 in|x ft]]", "Drawing inches on top, real feet on the bottom."), ("6.375 × 1 = 6.375", "Cross-multiply."),
         ("6.375 ÷ 0.25 = 25.5", "Divide.")], "25.5 ft, or 25 ft 6 in")
tip("A quick check", "At [[1|4]] in = 1 ft, every inch on the drawing is 4 ft. 6 [[3|8]] in × 4 = 25.5 ft. The proportion and the shortcut must agree.")

practice("Proportions", "Solve. Give the unit in word problems.",
         [("[[x|12]] = [[3|4]]", "9"), ("[[5|x]] = [[15|21]]", "7"), ("[[6|9]] = [[x|24]]", "16"), ("[[2.5|x]] = [[10|36]]", "9"), ("[[x|7]] = [[18|42]]", "3"),
          ("[[14|x]] = [[3.5|5]]", "20"),
          ("Concrete is mixed 1 part cement to 2 parts sand. How much sand goes with 7 bags of cement?", "14 bags"),
          ("A recipe for a cleaning solution uses 3 oz of concentrate per gallon of water. How much concentrate for 15 gal?", "45 oz"),
          ("If 12 fittings cost $40.20, what do 30 fittings cost?", "$100.50"),
          ("A drawing is at [[1|4]] in = 1 ft. A duct run is 3 [[1|2]] in on the drawing. How long is it?", "14 ft"),
          ("A drawing is at [[1|8]] in = 1 ft. A room is 2 [[1|4]] in long on the drawing. How long is it?", "18 ft"),
          ("A real wall is 30 ft long. How long is it on a [[1|4]] in = 1 ft drawing?", "7 [[1|2]] in"),
          ("A truck travels 210 mi on 14 gal. How far will it go on 22 gal?", "330 mi"),
          ("A pump fills 120 gal in 8 min. How long will it take to fill 450 gal?", "30 min")], cols=2)

sec("2.3 Gears and pulleys: inverse proportion")
p("When a large pulley drives a small one, the small pulley turns **faster**. The bigger the pulley, the slower it turns. Quantities that change in "
  "opposite directions like this are **inversely proportional**, and the proportion is set up differently.")
fig(figs.pulleys(), "A 12-in driving pulley and a 4-in driven pulley. The small pulley turns three times as fast.", width="4.4in")
rule("Pulleys and gears",
     "**Pulleys:**  D × N = d × n     (diameter times rpm is the same for both pulleys)",
     "**Gears:**  T × N = t × n     (number of teeth times rpm is the same for both gears)",
     "Capital letters are the driving pulley or gear; small letters are the driven one.")
example("A 12-in pulley on a motor turning 1,725 rpm drives a 4-in pulley. How fast does the 4-in pulley turn?",
        [("D × N = d × n", "Pulley formula."), ("(12)(1,725) = (4)n", "Substitute."), ("20,700 = 4n", "Multiply."), ("n = 5,175", "Divide by 4.")],
        "5,175 rpm")
example("A 36-tooth gear turning 240 rpm drives a 60-tooth gear. Find the speed of the 60-tooth gear.",
        [("(36)(240) = (60)n", "T × N = t × n."), ("8,640 = 60n", ""), ("n = 144", "The larger gear turns more slowly.")], "144 rpm")
warn("Do not set up a direct proportion",
     "Writing [[12|4]] = [[1,725|n]] gives n = 575 rpm, slower instead of faster. Ask first: should the answer be larger or smaller? For pulleys and gears, the smaller one turns faster.")
example("A motor turns at 1,750 rpm with a 3-in pulley. What size pulley is needed on a fan to make it turn at 1,050 rpm?",
        [("(3)(1,750) = d(1,050)", "Substitute; the fan pulley size is unknown."), ("5,250 = 1,050d", ""), ("d = 5", "Divide.")], "5-in pulley", title="Finding a pulley size")

practice("Gears and pulleys", "Use D × N = d × n for pulleys and T × N = t × n for gears.",
         [("A 10-in pulley at 1,200 rpm drives a 6-in pulley. Find the speed of the 6-in pulley.", "2,000 rpm"),
          ("A 4-in pulley at 1,725 rpm drives a 10-in pulley. Find the speed of the 10-in pulley.", "690 rpm"),
          ("A 3.5-in motor pulley at 1,750 rpm drives a blower at 875 rpm. Find the blower pulley size.", "7 in"),
          ("A blower must turn 1,100 rpm with an 8-in pulley. The motor turns 1,760 rpm. Find the motor pulley size.", "5 in"),
          ("A 40-tooth gear at 600 rpm drives a 24-tooth gear. Find the speed of the 24-tooth gear.", "1,000 rpm"),
          ("A 15-tooth gear at 900 rpm drives a 45-tooth gear. Find the speed of the 45-tooth gear.", "300 rpm"),
          ("A gear turning 150 rpm drives a 30-tooth gear at 450 rpm. How many teeth does the driving gear have?", "90 teeth"),
          ("A 6-in pulley turns 1,400 rpm. What size pulley will it drive at 2,100 rpm?", "4 in")], cols=1)

summary(["A ratio compares two quantities by division. Use the same unit for both and reduce; a ratio has no unit.",
         "A rate compares different kinds of quantity and keeps its units; a unit rate is per one.",
         "A proportion says two ratios are equal. Solve by cross-multiplying and dividing.",
         "Keep like quantities in the same position on both sides of a proportion.",
         "Pulleys and gears are inversely proportional: D × N = d × n and T × N = t × n. The smaller one turns faster."])
review([("Write 20 : 35 in lowest terms.", "4 : 7"), ("Write the ratio of 3 ft to 9 in.", "4 : 1"), ("Write the ratio of 2 gal to 6 qt.", "4 : 3"),
        ("Find the unit rate: $63 for 15 ft of molding.", "$4.20 per ft"), ("Find the unit rate: 1,125 gal in 25 min.", "45 gpm"),
        ("[[x|9]] = [[10|15]]", "6"), ("[[4|x]] = [[14|35]]", "10"), ("[[7.5|12]] = [[x|20]]", "12.5"),
        ("Mortar is mixed 1 part cement to 3 parts sand. How much sand goes with 4 bags of cement?", "12 bags"),
        ("A drawing is at [[1|4]] in = 1 ft. A wall is 4 [[3|4]] in on the drawing. How long is the wall?", "19 ft"),
        ("If 8 filters cost $54, what do 20 filters cost?", "$135"),
        ("An 8-in pulley at 1,725 rpm drives a 12-in pulley. Find the speed of the 12-in pulley.", "1,150 rpm"),
        ("A 2.5-in motor pulley at 1,750 rpm drives a 7-in pulley. Find its speed.", "625 rpm"),
        ("A 20-tooth gear at 1,200 rpm drives a 48-tooth gear. Find its speed.", "500 rpm"),
        ("A fan must turn 900 rpm. The motor turns 1,800 rpm with a 4-in pulley. What size fan pulley is needed?", "8 in"),
        ("Why does a direct proportion give the wrong answer for pulley speed?", "Pulley speed is inversely proportional to size: the smaller pulley turns faster.")])
