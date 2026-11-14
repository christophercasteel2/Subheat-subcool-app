"""Added depth for Part 3 (algebra): more explanation, worked examples, practice and review."""
import random
from fractions import Fraction
from math import sqrt
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr
import figs

PI = 3.14


def ev(display, py, places=None):
    """a practice item whose answer is worked out from the Python form of the expression"""
    v = eval(py, {"sqrt": sqrt})
    return (display, r(v, places) if places is not None else n(rnd(v, 6)))


# =====================================================================  7
def ch7():
    rg = random.Random(707)
    sec("7.5 Working with negative numbers")
    p("A negative number is a number less than zero. On a number line the negatives lie to the left of zero. Temperatures below zero, a pressure below "
      "atmospheric and a dimension that is under size are all negative amounts. Four rules handle all the arithmetic.")
    fig(figs.number_line([-19, 11, 5], -20, 20, 5, ["−19", "11", "5"]), "A number line. Starting at 5 and subtracting 24 lands on −19; adding 30 from there lands on 11.")
    rule("Signed numbers",
         "**Adding:** same signs, add and keep the sign. Different signs, subtract the smaller size from the larger and keep the sign of the larger.   −19 + 30 = 11;   −8 + (−5) = −13",
         "**Subtracting:** add the opposite.   5 − 24 = 5 + (−24) = −19;   6 − (−4) = 6 + 4 = 10",
         "**Multiplying or dividing:** same signs give a **positive** answer; different signs give a **negative** answer.   (19)(−5) = −95;   (−38) ÷ (−0.002) = 19,000")
    example("Evaluate (a) 12 − 30   (b) −7 + 15   (c) (−6)(−9)   (d) 48 ÷ (−8)",
            [("12 − 30 = −18", "(a) The larger number is being taken away, so the result is negative. The difference is 18."), ("−7 + 15 = 8", "(b) Different signs: 15 − 7 = 8, and the larger size is positive."),
             ("(−6)(−9) = 54", "(c) Same signs: positive."), ("48 ÷ (−8) = −6", "(d) Different signs: negative.")], "(a) −18   (b) 8   (c) 54   (d) −6")
    tip("The negative key is not the minus key",
        "Calculators have one key for subtraction `−` and another for a negative sign, marked `(−)` or `+/−`. Use the negative key for a number such as −0.002. "
        "To square a negative number, put it in parentheses: `(−3)²` is 9, but −3² is read as −(3²) = −9.")
    its = [ev(d, p_) for d, p_ in [("8 − 15", "8-15"), ("−4 + 11", "-4+11"), ("−9 − 6", "-9-6"), ("−12 + 5", "-12+5"), ("3 − (−8)", "3+8"), ("−20 + 20", "0"),
                                   ("(7)(−6)", "-42"), ("(−5)(−5)", "25"), ("−36 ÷ 9", "-4"), ("(−63) ÷ (−7)", "9"), ("(−2)(3)(−4)", "24"), ("15 − 40 + 10", "15-40+10"),
                                   ("−3 − 3 − 3", "-9"), ("(−3)²", "9"), ("4(−2.5)", "-10"), ("−0.5 + 0.125", "-0.375")]]
    practice("Signed numbers", "", its, cols=4)

    sec("7.6 Absolute value and other grouping symbols")
    p("The class list of grouping symbols has five members: parentheses ( ), brackets [ ], braces { }, **absolute-value bars** | |, and the **fraction bar**. "
      "All five mean the same thing to the order of operations: work out what is inside first.")
    p("The **absolute value** of a number is its size without its sign: |−7| = 7 and |7| = 7. Work out everything between the bars, then drop any negative sign.")
    example("Evaluate 20 − 2|4 − 3²|.",
            [("20 − 2|4 − 9|", "Inside the bars, the exponent comes first."), ("20 − 2|−5|", "Still inside the bars: 4 − 9 = −5."), ("20 − 2(5)", "Take the absolute value: |−5| = 5. The bars now act as parentheses."),
             ("20 − 10", "Multiply."), ("10", "Subtract.")], "10")
    example("Evaluate {2[3 + (9 − 5)²] − 8} ÷ 6.",
            [("{2[3 + (4)²] − 8} ÷ 6", "Innermost first: the parentheses."), ("{2[3 + 16] − 8} ÷ 6", "Exponent inside the brackets."), ("{2[19] − 8} ÷ 6", "Finish the brackets."),
             ("{38 − 8} ÷ 6", "Inside the braces, multiply first."), ("30 ÷ 6", "Finish the braces."), ("5", "")], "5", title="Three kinds of grouping symbols")

    sec("7.7 Showing the work")
    p("On the chapter exam the instructions read: **“Must show 3 calculations before final evaluation.”** That means at least three lines of work, each a little simpler than the one above it, "
      "before the answer. The surest way to earn that credit is the habit already described: one level of PEMDAS per line.")
    example("Evaluate  [[40 − 4(6² ÷ 3²) + 8|4² − 8]].  Round to the nearest hundredth if needed. Show at least three calculations.",
            [("[[40 − 4(36 ÷ 9) + 8|16 − 8]]", "Calculation 1: every exponent, top and bottom."), ("[[40 − 4(4) + 8|8]]", "Calculation 2: finish the parentheses on top; finish the bottom."),
             ("[[40 − 16 + 8|8]]", "Calculation 3: multiply."), ("[[32|8]]", "Calculation 4: add and subtract left to right, 40 − 16 = 24, then 24 + 8 = 32."), ("4", "Final evaluation: divide.")], "4")
    warn("Five places where points are lost",
         "**1.** Adding before multiplying because the addition is written first.   3 + 5 × 2 is 13, not 16.",
         "**2.** Doing addition before a subtraction that comes first.   20 − 8 + 5 is 17, not 7.",
         "**3.** Multiplying the base by the exponent.   5² is 25, not 10.",
         "**4.** Dividing only part of a fraction’s top.   (6 + 12) ÷ 3 is 6, not 6 + 4 = 10.",
         "**5.** Distributing an exponent over a sum.   (3 + 4)² is 49, not 9 + 16 = 25.")
    example("Evaluate 2.5 + 1.5(8.4 − 2.4)² ÷ 0.9.",
            [("2.5 + 1.5(6)² ÷ 0.9", "Parentheses."), ("2.5 + 1.5(36) ÷ 0.9", "Exponent."), ("2.5 + 54 ÷ 0.9", "Multiplication and division, left to right: the multiplication comes first."),
             ("2.5 + 60", "Then the division."), ("62.5", "Addition last.")], "62.5", title="Decimals follow the same order")
    example("Evaluate  [[3|4]] + [[1|2]] × [[5|8]].",
            [("[[3|4]] + [[5|16]]", "Multiply before adding: [[1|2]] × [[5|8]] = [[5|16]]."), ("[[12|16]] + [[5|16]]", "Common denominator."), ("[[17|16]] = 1 [[1|16]]", "")],
            "1 [[1|16]]", title="Fractions follow the same order")

    its = [ev(d, p_, pl) for d, p_, pl in [
        ("14 − 6 ÷ 2", "14-6/2", None), ("9 × 2 − 12 ÷ 4", "9*2-12/4", None), ("30 ÷ 5 × 3", "30/5*3", None), ("16 − 9 + 4", "16-9+4", None), ("2 + 3 × 4²", "2+3*16", None),
        ("(2 + 3) × 4²", "5*16", None), ("6² ÷ 4 + 1", "36/4+1", None), ("50 − 3(2 + 4)", "50-18", None), ("4(9 − 5)² ÷ 8", "4*16/8", None), ("7 + 2[10 − 3(2)]", "7+2*4", None),
        ("√(49) + 3²", "7+9", None), ("√(7² + 24²)", "25", None), ("5√(100 − 36)", "5*8", None), ("18 − |3 − 10|", "18-7", None), ("3|2 − 8| ÷ 9", "3*6/9", None),
        ("[[20 + 16|4 + 5]]", "36/9", None), ("[[6² − 4²|2 × 5]]", "20/10", None), ("[[9 − 2(5 − 2)²|3]]", "(9-18)/3", None), ("[[15 + 3(4² ÷ 8)|3² − 2]]", "21/7", None),
        ("[[100|4(2 + 3)]] + 6", "100/20+6", None), ("12 − 3(2³ − 5) + 7", "12-9+7", None), ("2{5 + [12 ÷ (1 + 3)]}", "2*(5+3)", None), ("1.2 + 0.8(3.5 − 1.5)²", "1.2+0.8*4", None),
        ("(4.5 − 1.5) ÷ 0.6 × 2", "3/0.6*2", None), ("[[7 + 5 × 3 − 2²|5]]", "18/5", None), ("[[2(8 + 12)|2 + 8 + 12]]", "40/22", 2), ("[[5² + 12|3 × 7 − 4]]", "37/17", 2),
        ("[[9(4 + 11)|9 + 4 + 11]]", "135/24", 2), ("10 − 4² + 2(3)", "10-16+6", None), ("−8 + 6 × 3 − 20", "-8+18-20", None)]]
    practice("More order of operations", "Show at least three calculations before the final answer. Round to the nearest hundredth only where needed.", its, cols=3)

    more_review([ev("9 − 20 + 6", "9-20+6"), ev("(−4)(−7) − 30", "28-30"), ev("25 − 3|2 − 9|", "25-21"), ev("{3[2 + (7 − 4)²] − 3} ÷ 5", "(3*11-3)/5"),
                 ev("[[60 − 5(4² ÷ 2³) + 10|3² + 1]]", "(60-10+10)/10"), ev("3.5 + 2(1.5)²", "3.5+2*2.25"), ev("[[4(7 + 9)|4 + 7 + 9]]", "64/20"),
                 ("[[1|2]] + [[3|4]] × [[1|2]]", fr(Fraction(1, 2) + Fraction(3, 8))),
                 ("True or false: (2 + 5)² = 2² + 5². Show why.", "False. (7)² = 49, but 4 + 25 = 29."),
                 ("Name the five grouping symbols from the class notes.", "parentheses, brackets, braces, absolute-value bars and the fraction bar"),
                 ("Why is 18 − 6 + 2 equal to 14 and not 10?", "Addition and subtraction are done left to right: 18 − 6 = 12, then 12 + 2 = 14."),
                 ev("−3² + (−3)²", "-9+9")])


# =====================================================================  8
def ch8():
    sec("8.4 Reading a formula problem")
    p("A formula problem from the trades is a short paragraph, and all the information needed is in it. Read it with a pencil, in this order.")
    rule("Before you calculate",
         "**1. Find the formula** and the letter it is solved for.", "**2. Match each letter with its number.** Write them as a list: W = 2, D = 500, S = 3.",
         "**3. Check the units.** A formula built for inches will not work with feet. If the description says “d in inches,” the diameter must be in inches.",
         "**4. Find the rounding instruction** (nearest whole number, nearest hundredth, do not round) and the unit of the answer.",
         "Then write the formula, substitute, and evaluate.")
    example("**HVAC.** The sensible heat carried by moving air is Q = 1.08 × cfm × ΔT, where Q is in Btu per hour, cfm is the airflow in cubic feet per minute and ΔT is the temperature "
            "change in °F. Find Q when a system moves 1,200 cfm and heats the air from 68°F to 110°F.",
            [("cfm = 1200;  ΔT = 110 − 68 = 42", "List the values. ΔT (“delta T”) is a single variable meaning the temperature **difference**, so it must be found first."),
             ("Q = 1.08 × cfm × ΔT", "Formula."), ("Q = 1.08(1200)(42)", "Substitute."), ("Q = 54,432", "Multiply.")], "54,432 Btu per hour", title="A value that must be found first")
    example("**Temperature.** Celsius temperature is found from C = [[5(F − 32)|9]]. Convert 95°F to Celsius.",
            [("C = [[5(F − 32)|9]]", "Formula."), ("C = [[5(95 − 32)|9]]", "Substitute."), ("C = [[5(63)|9]]", "Parentheses first."), ("C = [[315|9]] = 35", "Multiply the top, then divide.")],
            "35°C")
    example("**Temperature.** Fahrenheit temperature is found from F = [[9C|5]] + 32. Convert −10°C to Fahrenheit.",
            [("F = [[9(−10)|5]] + 32", "Substitute. The parentheses keep the negative sign with its number."), ("F = [[−90|5]] + 32", "Multiply: positive times negative is negative."),
             ("F = −18 + 32", "Divide."), ("F = 14", "Add.")], "14°F", title="A negative value")
    sub("More formulas from the trades")
    example("**Electrical.** Two resistors in parallel have a total resistance R_{T} = [[R_{1}R_{2}|R_{1} + R_{2}]]. Find R_{T} for R_{1} = 60 Ω and R_{2} = 40 Ω.",
            [("R_{T} = [[(60)(40)|60 + 40]]", "Substitute."), ("R_{T} = [[2400|100]]", "Multiply the top; add the bottom."), ("R_{T} = 24", "Divide.")], "24 Ω")
    example("**Carpentry.** The number of board feet in a piece of lumber is bf = [[TWL|12]], where T is the thickness in inches, W is the width in inches and L is the length in feet. "
            "How many board feet are in a board 2 in thick, 8 in wide and 14 ft long? Round to the nearest tenth.",
            [("bf = [[(2)(8)(14)|12]]", "Substitute. Note the mixed units the formula expects: inches, inches, feet."), ("bf = [[224|12]] = 18.666…", ""), ("bf = 18.7", "")], "18.7 board feet")
    example("**Machine trades.** Horsepower is hp = [[T × rpm|5252]], where T is the torque in pound-feet. Find the horsepower of an engine producing 310 lb-ft of torque at 4,000 rpm. Round to the nearest whole number.",
            [("hp = [[(310)(4000)|5252]]", "Substitute."), ("hp = [[1,240,000|5252]] = 236.1…", ""), ("hp = 236", "")], "236 hp")
    example("**Sheet metal.** The allowance for a Pittsburgh lock is A = 2w + [[3|16]] in. Find A when the pocket width is w = [[5|16]] in. Give a fraction in lowest terms.",
            [("A = 2([[5|16]]) + [[3|16]]", "Substitute."), ("A = [[10|16]] + [[3|16]]", "Multiply first: 2 × [[5|16]] = [[10|16]]. Leave it in sixteenths so it can be added."), ("A = [[13|16]]", "Add.")],
            "[[13|16]] in", title="A formula with fractions")
    tip("Check with an estimate",
        "In the horsepower example, 310 × 4000 is about 300 × 4000 = 1,200,000, and 1,200,000 ÷ 5000 = 240. The exact answer, 236, is close, so no key was mistyped.")

    its = [("**HVAC.** Q = 1.08 × cfm × ΔT. cfm = 800, ΔT = 25°F.", n(1.08 * 800 * 25) + " Btu per hour"),
           ("**HVAC.** Q = 1.08 × cfm × ΔT. A system moves 1,600 cfm and cools the air from 78°F to 58°F.", n(1.08 * 1600 * 20) + " Btu per hour"),
           ("**HVAC.** Air velocity V = [[Q|A]] ft/min, where Q is airflow in cfm and A is the duct area in sq ft. Q = 900 cfm, A = 1.5 sq ft.", "600 ft/min"),
           ("**Temperature.** C = [[5(F − 32)|9]]. F = 212°.", "100°C"), ("**Temperature.** C = [[5(F − 32)|9]]. F = 41°.", "5°C"),
           ("**Temperature.** C = [[5(F − 32)|9]]. F = 70°. Round to the nearest tenth.", r(5 * 38 / 9, 1) + "°C"),
           ("**Temperature.** F = [[9C|5]] + 32. C = 25°.", "77°F"), ("**Temperature.** F = [[9C|5]] + 32. C = −40°.", "−40°F"),
           ("**Electrical.** P = EI watts. E = 240 V, I = 12.5 A.", "3,000 W"), ("**Electrical.** P = I²R. I = 4 A, R = 15 Ω.", "240 W"),
           ("**Electrical.** P = [[E²|R]]. E = 120 V, R = 48 Ω.", "300 W"),
           ("**Electrical.** R_{T} = [[R_{1}R_{2}|R_{1} + R_{2}]]. R_{1} = 30 Ω, R_{2} = 20 Ω.", "12 Ω"),
           ("**Electrical.** R_{T} = [[R_{1}R_{2}|R_{1} + R_{2}]]. R_{1} = 100 Ω, R_{2} = 150 Ω.", "60 Ω"),
           ("**Electrical.** Series circuit R_{T} = R_{1} + R_{2} + R_{3}. R_{1} = 47 Ω, R_{2} = 68 Ω, R_{3} = 120 Ω.", "235 Ω"),
           ("**Carpentry.** bf = [[TWL|12]]. T = 1 in, W = 6 in, L = 10 ft.", "5 board feet"),
           ("**Carpentry.** bf = [[TWL|12]]. T = 2 in, W = 10 in, L = 16 ft. Round to the nearest tenth.", r(320 / 12, 1) + " board feet"),
           ("**Machine trades.** hp = [[T × rpm|5252]]. T = 250 lb-ft, rpm = 3,500. Round to the nearest whole number.", r(250 * 3500 / 5252, 0) + " hp"),
           ("**Machine trades.** Cutting speed S = [[πdn|12]] ft/min. d = 4 in, n = 600 rpm, π = 3.14.", n(3.14 * 4 * 600 / 12) + " ft/min"),
           ("**Sheet metal.** A = 2w + [[3|16]]. w = [[1|4]] in.", "[[11|16]] in"), ("**Sheet metal.** A = 2w + [[3|16]]. w = [[3|8]] in.", "[[15|16]] in"),
           ("**Machine trades.** Belt length L = 2d + 3.26(r + R). d = 20 in, r = 3 in, R = 7 in.", n(40 + 32.6) + " in"),
           ("**Water.** Pressure P = 0.52D + 14.7 psi. D = 40 ft.", n(0.52 * 40 + 14.7) + " psi"),
           ("**Physics.** Distance fallen d = 16t² ft. t = 2.5 s.", "100 ft"),
           ("**Geometry.** Hero's Formula A = √(s(s − a)(s − b)(s − c)) with s = 24, a = 12, b = 16, c = 20.", "96")]
    practice("More formulas", "List the values, write the formula, show the substitution and evaluate. Do not round unless told to.", its, cols=1)

    more_review([("Q = 1.08 × cfm × ΔT. cfm = 1,000, air heated from 65°F to 105°F.", n(1.08 * 1000 * 40) + " Btu per hour"), ("C = [[5(F − 32)|9]]. F = 86°.", "30°C"),
                 ("F = [[9C|5]] + 32. C = −5°.", "23°F"), ("R_{T} = [[R_{1}R_{2}|R_{1} + R_{2}]]. R_{1} = 90 Ω, R_{2} = 45 Ω.", "30 Ω"),
                 ("bf = [[TWL|12]]. T = 2 in, W = 6 in, L = 12 ft.", "12 board feet"), ("hp = [[T × rpm|5252]]. T = 400, rpm = 2,626.", "200 hp"),
                 ("A = 2w + [[3|16]]. w = [[7|32]] in.", "[[5|8]] in"), ("P = I²R. I = 0.5 A, R = 220 Ω.", "55 W"),
                 ("In Q = 1.08 × cfm × ΔT, what does ΔT stand for?", "the temperature difference (change in temperature)"),
                 ("A formula says “d in inches.” The diameter is given as 1.5 ft. What must be done first?", "Convert it to inches: 18 in.")])


# =====================================================================  9
def ch9():
    rg = random.Random(909)
    sec("9.5 When the unknown is in the denominator")
    p("In Ohm’s law, I = [[E|R]], the resistance is on the **bottom**. To find R, it first has to be brought up off the bottom. Multiply both sides by R; then finish as a one-step equation.")
    example("I = [[E|R]]. A heater draws I = 12.5 A from E = 240 V. Find its resistance R.",
            [("12.5 = [[240|R]]", "Substitute."), ("12.5R = 240", "Multiply both sides by R. On the right the R’s cancel."), ("R = 240 ÷ 12.5 = 19.2", "Divide both sides by 12.5.")], "R = 19.2 Ω")
    p("The shortcut is to **cross-multiply**, exactly as in the percent proportion. Write the left side over 1: [[12.5|1]] = [[240|R]]. The diagonals give 12.5 × R = 240 × 1.")
    example("Tensile strength is T = [[L|A]]. A rod must have T = 60,000 psi under a load L = 9,000 lb. Find the cross-sectional area A.",
            [("60,000 = [[9000|A]]", "Substitute."), ("60,000A = 9000", "Cross-multiply."), ("A = 9000 ÷ 60,000 = 0.15", "Divide.")], "A = 0.15 sq in")

    sec("9.6 Equations with parentheses")
    p("When the unknown is inside parentheses, undo what is **outside** the parentheses first, one operation at a time, and open the parentheses last. "
      "This is the solve direction of PEMDAS: A S first, then M D, and P at the end.")
    example("L = 2d + 3.26(r + R). A belt is L = 86.08 in long. With d = 20 in and r = 5 in, find R.",
            [("86.08 = 2(20) + 3.26(5 + R)", "Substitute."), ("86.08 = 40 + 3.26(5 + R)", "Simplify."), ("46.08 = 3.26(5 + R)", "A S: subtract 40 from both sides."),
             ("14.134… = 5 + R", "M D: divide both sides by 3.26."), ("R = 9.134…", "P: the parentheses can now be dropped. Subtract 5."), ("R = 9.1", "Round to the nearest tenth.")], "R = 9.1 in")
    example("C = [[5(F − 32)|9]]. What Fahrenheit temperature is 20°C?",
            [("20 = [[5(F − 32)|9]]", "Substitute."), ("180 = 5(F − 32)", "Multiply both sides by 9."), ("36 = F − 32", "Divide both sides by 5."), ("F = 68", "Add 32 to both sides.")], "68°F")

    sec("9.7 Equations with squares and roots")
    p("Squaring and taking a square root undo each other. If the unknown is squared, get the squared term alone, then take the square root of both sides.")
    example("The force on a piston is F = [[πPD²|4]]. What diameter D is needed to produce F = 2,512 lb at P = 50 psi? Use π = 3.14.",
            [("2512 = [[(3.14)(50)D²|4]]", "Substitute."), ("2512 = [[157D²|4]]", "Simplify: 3.14 × 50 = 157."), ("10,048 = 157D²", "Multiply both sides by 4."),
             ("64 = D²", "Divide both sides by 157."), ("D = √64 = 8", "Take the square root of both sides.")], "D = 8 in")
    example("An object falls d = 16t² feet in t seconds. How long does it take to fall 400 ft?",
            [("400 = 16t²", "Substitute."), ("25 = t²", "Divide both sides by 16."), ("t = √25 = 5", "Square root of both sides.")], "t = 5 seconds")
    warn("Divide before the root",
         "In 400 = 16t², do not take the square root first. √400 = 20 = 16t gives t = 1.25, which is wrong. The 16 is not squared, so it must be divided away before the root is taken.")

    sec("9.8 Rearranging a formula")
    p("If the same formula will be used many times for the same unknown, it saves work to solve it once **with the letters**, before any numbers go in. "
      "The steps are identical; the letters are treated as if they were numbers.")
    example("Solve P = 2L + 2W for L.",
            [("P − 2W = 2L", "Subtract 2W from both sides."), ("[[P − 2W|2]] = L", "Divide both sides by 2.")], "L = [[P − 2W|2]]")
    example("Solve I = [[E|R]] for E, and then for R.",
            [("IR = E", "Multiply both sides by R."), ("R = [[E|I]]", "Starting again from IR = E, divide both sides by I.")], "E = IR   and   R = [[E|I]]")
    table(["Formula", "Solved for", "Result"],
          [["A = LW", "W", "W = [[A|L]]"], ["D = RT", "T", "T = [[D|R]]"], ["P = 2L + 2W", "W", "W = [[P − 2L|2]]"], ["A = 2w + [[3|16]]", "w", "w = [[A − 3/16|2]]"],
           ["C = πd", "d", "d = [[C|π]]"], ["A = πr²", "r", "r = √([[A|π]])"], ["A = [[bh|2]]", "h", "h = [[2A|b]]"]],
          caption="Table 9.1  Some formulas rearranged", widths=[34, 22, 44])

    sec("9.9 Checking, and a plan for word problems")
    rule("A plan for “substitute and solve” problems",
         "**1.** Write the formula.", "**2.** Substitute every value that is given. One letter is left.", "**3.** Simplify each side.",
         "**4.** Undo addition or subtraction, then multiplication or division, then exponents, then parentheses.", "**5.** Round as directed and write the unit.",
         "**6.** Check: put the answer back into the original formula.")
    example("A = RT + M gives the amount A of a repair bill when R is the hourly rate, T is the time in hours and M is the cost of materials. A bill is $1,261, materials were $445 and the rate is $68 per hour. How many hours were billed?",
            [("1261 = 68T + 445", "Substitute."), ("816 = 68T", "Subtract 445 from both sides."), ("T = 12", "Divide both sides by 68."), ("Check: 68(12) + 445 = 816 + 445 = 1261 ✓", "")], "12 hours")

    one = []
    for _ in range(4):
        a, x = rg.choice([3, 4, 6, 7, 8, 12, 15, 25]), rg.choice([4, 6.5, 9, 11, 12.5, 20])
        one.append((f"{a}x = {n(a * x)}", n(x)))
    for _ in range(4):
        a, x = rg.choice([2.5, 7.25, 9, 14.5, 30]), rg.choice([4, 6.5, 9, 11, 12.5, 20])
        one.append((f"y + {n(a)} = {n(a + x)}", n(x)))
    for _ in range(4):
        a, x = rg.choice([1.5, 4.75, 8, 13]), rg.choice([4, 6.5, 9, 11, 12.5, 20])
        one.append((f"m − {n(a)} = {n(x - a)}", n(x)))
    for _ in range(4):
        a, x = rg.choice([3, 4, 5, 8]), rg.choice([12, 20, 36, 2.4, 60])
        one.append((f"[[k|{a}]] = {n(x / a)}", n(x)))
    practice("More one-step equations", "Solve. Show the step that undoes the operation.", one, cols=4)

    two = []
    for _ in range(20):
        a, x, b = rg.choice([2, 3, 4, 5, 6, 8, 0.5, 1.5, 12]), rg.choice([3, 5, 7, 8, 10, 12, 2.5, 4.5, 20]), rg.choice([4, 7, 9, 12, 15, 2.5, 30])
        v = rg.choice("xymt")
        if rg.random() < 0.5:
            two.append((f"{n(a)}{v} + {n(b)} = {n(a * x + b)}", n(x)))
        else:
            two.append((f"{n(a)}{v} − {n(b)} = {n(a * x - b)}", n(x)))
    practice("More two-step equations", "Solve. Undo the addition or subtraction first.", two, cols=4)

    sp = [("I = [[E|R]]. I = 8 A, E = 120 V. Find R.", "15 Ω"), ("I = [[E|R]]. I = 0.25 A, E = 12 V. Find R.", "48 Ω"),
          ("T = [[L|A]]. T = 50,000 psi, L = 12,500 lb. Find A.", "0.25 sq in"), ("V = [[Q|A]]. V = 800 ft/min, Q = 1,200 cfm. Find A.", "1.5 sq ft"),
          ("C = [[5(F − 32)|9]]. C = 40°. Find F.", "104°F"), ("C = [[5(F − 32)|9]]. C = −15°. Find F.", "5°F"),
          ("L = 2d + 3.26(r + R). L = 72.6 in, d = 20 in, r = 4 in. Find R.", "6 in"), ("3(x + 4) = 27", "5"), ("5(y − 2) + 6 = 31", "7"),
          ("A = s². A = 6.25 sq ft. Find s.", "2.5 ft"), ("d = 16t². d = 144 ft. Find t.", "3 s"), ("A = πr². A = 78.5 sq in, π = 3.14. Find r.", "5 in"),
          ("F = [[πPD²|4]]. F = 1,256 lb, P = 100 psi, π = 3.14. Find D.", "4 in"), ("P = I²R. P = 180 W, R = 20 Ω. Find I.", "3 A"),
          ("a² + b² = c². a = 9, c = 15. Find b.", "12"), ("Solve A = LW for L.", "L = [[A|W]]"), ("Solve P = 4s for s.", "s = [[P|4]]"),
          ("Solve A = RT + M for T.", "T = [[A − M|R]]"), ("Solve C = 2πr for r.", "r = [[C|2π]]"), ("Solve P = 0.52D + 14.7 for D.", "D = [[P − 14.7|0.52]]")]
    practice("Special cases", "Substitute and solve, or rearrange as asked.", sp, cols=2)

    wp = [("**Electrical.** P = EI. A 1,500-W heater runs on 120 V. Find the current I.", "12.5 A"),
          ("**HVAC.** Q = 1.08 × cfm × ΔT. Q = 43,200 Btu per hour, ΔT = 20°F. Find the cfm.", "2,000 cfm"),
          ("**HVAC.** Q = 1.08 × cfm × ΔT. Q = 32,400 Btu per hour, cfm = 1,000. Find ΔT.", "30°F"),
          ("**Carpentry.** bf = [[TWL|12]]. bf = 16, T = 2 in, W = 8 in. Find L.", "12 ft"),
          ("**Office services.** T = 45 + 60H. T = $405. Find H.", "6 h"), ("**Trades management.** A = RT + M. A = $2,074, M = $610, R = $61 per hour. Find T.", "24 h"),
          ("**Water.** P = 0.52D + 14.7. P = 53.7 psi. Find D.", "75 ft"), ("**Meteorology.** T = −0.002H + G. G = 64°F, T = 40°F. Find H.", "12,000 ft"),
          ("**Sheet metal.** A = 2w + [[3|16]]. A = [[9|16]] in. Find w in lowest terms.", "[[3|16]] in"),
          ("**Sheet metal.** A = 2w + [[3|16]]. A = [[5|8]] in. Find w in lowest terms.", "[[7|32]] in"),
          ("**Geometry.** P = 2L + 2W. P = 318 ft, L = 96 ft. Find W.", "63 ft"),
          ("**Machine trades.** hp = [[T × rpm|5252]]. hp = 150, rpm = 5,252. Find T.", "150 lb-ft")]
    practice("Formulas run backward", "Write the formula, substitute, solve and check.", wp, cols=1)

    more_review([("I = [[E|R]]. I = 6 A, E = 240 V. Find R.", "40 Ω"), ("T = [[L|A]]. T = 40,000 psi, L = 8,000 lb. Find A.", "0.2 sq in"),
                 ("C = [[5(F − 32)|9]]. C = 30°. Find F.", "86°F"), ("4(x − 3) = 28", "10"), ("d = 16t². d = 256 ft. Find t.", "4 s"),
                 ("F = [[πPD²|4]]. F = 1,570 lb, P = 80 psi, π = 3.14. Find D.", "5 in"), ("Solve D = RT for R.", "R = [[D|T]]"), ("Solve A = [[bh|2]] for b.", "b = [[2A|h]]"),
                 ("Q = 1.08 × cfm × ΔT. Q = 27,000 Btu per hour, ΔT = 25°F. Find the cfm.", "1,000 cfm"),
                 ("When solving, which is undone first: multiplication or addition?", "addition (or subtraction)"),
                 ("In 144 = 16t², why must you divide before taking the square root?", "Only t is squared. The 16 must be divided away so that t² stands alone."),
                 ("A = 2w + [[3|16]]. A = 1 in. Find w in lowest terms.", "[[13|32]] in")])


def part3():
    cumulative("Part 3 · Algebra", "Mixed problems from Chapters 7, 8 and 9.",
               [ev("7 + 18 ÷ 3 × 2", "7+18/3*2"), ev("45 − 5(2 + 3²)", "45-55"), ev("[[18 − 2(4² ÷ 8) + 6|2² + 1]]", "(18-4+6)/5"), ev("√(8² + 15²)", "17"), ev("3[4 + 2(7 − 5)²]", "3*12"),
                ("Evaluate L = 4A + 3(B + C) for A = 5, B = 2, C = 6.", "44"), ("Evaluate 2C + 1.6(D + d) for C = 20, D = 12, d = 8.", "72"),
                ("N = √(D ÷ d)⁵. D = 8 in, d = 2 in.", "32 pipes"), ("C = [[W²DS|1.085]]. W = 1 m, D = 1,085 kg/m³, S = 2 m/s.", "2,000 t/h"),
                ("C_{T} = [[C_{1}(C_{2} + C_{3})|C_{1} + C_{2} + C_{3}]]. C_{1} = 10, C_{2} = 4, C_{3} = 6.", "5 µF"), ("F = [[πPD²|4]]. P = 20 psi, D = 10 in, π = 3.14.", "1,570 lb"),
                ("Q = 1.08 × cfm × ΔT. cfm = 1,400, ΔT = 30°F.", n(1.08 * 1400 * 30) + " Btu per hour"),
                ("x − 12.5 = 30", "42.5"), ("9y = 58.5", "6.5"), ("6m + 11 = 59", "8"), ("V = LWH. V = 1,440 cu ft, L = 20 ft, W = 9 ft. Find H.", "8 ft"),
                ("P = 2L + 2W. P = 540 ft, W = 95 ft. Find L.", "175 ft"), ("T = 45 + 60H. T = $285. Find H.", "4 h"),
                ("A = 2w + [[3|16]]. A = [[7|8]] in. Find w.", "[[11|32]] in"), ("I = [[E|R]]. I = 4 A, E = 120 V. Find R.", "30 Ω")], cols=2)
