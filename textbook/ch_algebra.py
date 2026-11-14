"""Part 3: algebra (order of operations, evaluating and solving formulas)."""
from fractions import Fraction
from math import sqrt
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr, F, frtxt
import figs

part("Part 3 · Algebra", "A formula is a set of instructions written in symbols. Part 3 covers the order in which those "
     "instructions are carried out, how to put numbers into a formula, and how to run a formula backward to find a missing value.")

# =====================================================================  7
chapter("Order of Operations",
        ["State the order of operations and explain why an agreed order is needed.",
         "Recognize every kind of grouping symbol, including the fraction bar.",
         "Evaluate expressions with exponents and square roots.",
         "Work multiplication with division, and addition with subtraction, from left to right.",
         "Show the work for a multi-step evaluation one operation at a time."],
        "Ask two people to work out 6 + 4 ÷ 2 and you may get 5 from one and 8 from the other. Only one of them is right. "
        "Mathematics settles the question with a fixed order of operations, and every formula in the trades depends on it.",
        [("expression", "Numbers and operations written together, such as 6 + 4 ÷ 2."),
         ("evaluate", "To work an expression down to a single number."),
         ("exponent", "The small raised number that tells how many times the base is multiplied by itself: 4² = 4 × 4."),
         ("square root", "The number that, multiplied by itself, gives the number under the √ sign: √25 = 5."),
         ("grouping symbol", "Anything that says “do this part first”: parentheses, brackets, braces, absolute-value bars, a fraction bar, a root sign.")])

sec("7.1 Why an order is needed")
p("Consider 6 + 4 ÷ 2. Working from left to right gives 10 ÷ 2 = 5. Dividing first gives 6 + 2 = 8. An expression must have "
  "one value, so everyone agrees to the same order. Under that agreement division comes before addition, and the answer is **8**.")
eq("Wrong:   6 + 4 ÷ 2 = 10 ÷ 2 = 5", "Right:   6 + 4 ÷ 2 = 6 + 2 = 8")
fig(figs.pemdas(), "The order of operations. Four levels, worked from the top down.")
rule("The order of operations (PEMDAS)",
     "**1. P: Parentheses** and every other grouping symbol: ( ), [ ], { }, absolute-value bars, and the top and bottom of a fraction bar.",
     "**2. E: Exponents** and roots.",
     "**3. M D: Multiplication and division,** whichever comes first, working from **left to right**.",
     "**4. A S: Addition and subtraction,** whichever comes first, working from **left to right**.")
warn("PEMDAS has four steps, not six",
     "Multiplication does **not** come before division, and addition does **not** come before subtraction. Each pair shares a level and is "
     "worked in the order it appears, left to right. 24 ÷ 4 × 2 is 6 × 2 = 12, not 24 ÷ 8 = 3.")

fig(figs.pemdas_two_way(), "PEMDAS runs both ways. To evaluate, start at P and work down. To solve, start at A S and work up to P, undoing each operation.")
p("This chapter is about the left-hand arrow: **evaluating**. Chapter 9 uses the right-hand arrow: **solving**.")

sec("7.2 Exponents and roots")
p("An **exponent** is shorthand for repeated multiplication. In 4², the 4 is the **base** and the 2 is the exponent: use 4 as a "
  "factor twice. A **square root** undoes a square.")
eq("4² = 4 × 4 = 16          2³ = 2 × 2 × 2 = 8          6⁴ = 6 × 6 × 6 × 6 = 1296", "√16 = 4  because  4 × 4 = 16          √2.25 = 1.5  because  1.5 × 1.5 = 2.25")
warn("An exponent is not multiplication by the exponent", "4² is 4 × 4 = 16, not 4 × 2 = 8. And 2³ is 8, not 6.")
p("A root sign is also a grouping symbol. Everything under the bar must be worked out **before** the root is taken: "
  "√(9 + 16) is √25 = 5. It is not 3 + 4.")
tip("Powers and roots on a calculator",
    "Use the `x²` key for squares and the `^` or `xʸ` key for other powers: 6⁴ is `6 ^ 4`. For a root, press `√` and then put the whole "
    "quantity in parentheses: `√(9 + 16)`. On some calculators the root key is the shifted function of `x²`.")

sec("7.3 Multiplying without a times sign")
p("In algebra the × sign is usually left out, because it looks like the letter x. A number written directly against a parenthesis, "
  "or against a letter, means multiply.")
eq("3(8)  means  3 × 8          2(5 + 1)  means  2 × (5 + 1)          4C  means  4 × C          (3)(7)  means  3 × 7")
tip("Some calculators need the times sign",
    "Many calculators accept 3(8) as typed. Others report a syntax error or, worse, read it as something else. "
    "If yours does, key in the × yourself: `3 × (8)`.")

sec("7.4 Working an expression step by step")
p("Do one operation per line and copy everything else down unchanged. It feels slow, but it is how errors are found, and it is "
  "the work an instructor expects to see.")
example("Evaluate 5 − 3(4² ÷ 2) + 30.",
        [("5 − 3(**16** ÷ 2) + 30", "Start inside the parentheses. Inside, the exponent comes first: 4² = 16."),
         ("5 − 3(**8**) + 30", "Still inside the parentheses: 16 ÷ 2 = 8."),
         ("5 − **24** + 30", "The parentheses now hold one number. Multiply: 3(8) = 24."),
         ("**−19** + 30", "Add and subtract from left to right: 5 − 24 = −19."), ("11", "−19 + 30 = 11.")], "11")
warn("Subtraction before addition, when it comes first",
     "In 5 − 24 + 30, do **not** add 24 + 30 first. That gives 5 − 54 = −49, which is wrong. Work left to right: 5 − 24, then + 30.")
example("Evaluate 18 − 12 ÷ 3 × 2 + 5².",
        [("18 − 12 ÷ 3 × 2 + **25**", "No grouping symbols. Exponent first."),
         ("18 − **4** × 2 + 25", "Multiplication and division left to right: the division comes first, 12 ÷ 3 = 4."),
         ("18 − **8** + 25", "Then 4 × 2 = 8."), ("**10** + 25", "Left to right: 18 − 8 = 10."), ("35", "")], "35")
sub("The fraction bar")
p("A long fraction bar groups everything above it and everything below it. Work the entire top to one number, work the entire "
  "bottom to one number, and divide last.")
example("Evaluate  [[12 − 3(4² ÷ 2³) + 9|5² − 10]].  Round to the nearest hundredth if needed.",
        [("top: 12 − 3(16 ÷ 8) + 9", "Inside the parentheses, exponents first: 4² = 16 and 2³ = 8."),
         ("top: 12 − 3(2) + 9 = 12 − 6 + 9 = 15", "Finish the parentheses, multiply, then go left to right."),
         ("bottom: 25 − 10 = 15", "Exponent, then subtract."), ("[[15|15]] = 1", "Only now divide the top by the bottom.")], "1")
tip("Entering a fraction bar",
    "A calculator does not see a fraction bar unless you tell it. Put the whole top in parentheses and the whole bottom in parentheses: "
    "`(12 − 3 × (4² ÷ 2³) + 9) ÷ (5² − 10)`. Without them the calculator divides only the 9 by the 25.")
sub("Grouping inside grouping")
p("When grouping symbols are nested, begin with the innermost pair and work outward.")
example("Evaluate 2[7 + 3(10 − 6)]².",
        [("2[7 + 3(**4**)]²", "Innermost parentheses first."), ("2[7 + **12**]²", "Inside the brackets, multiply before adding."),
         ("2[**19**]²", "Finish the brackets."), ("2 × **361**", "Exponent before multiplication: 19² = 361."), ("722", "")], "722")
sub("Negative numbers")
p("The Chapter 7 work occasionally passes through a negative number, as −19 did above. Two facts are enough: "
  "subtracting a larger number from a smaller one gives a negative result (5 − 24 = −19), and a negative times a positive is negative "
  "((19)(−5) = −95).")

practice("Order of operations", "Evaluate. Show one operation per line. Round to the nearest hundredth only if needed.",
         [("6 + 4 ÷ 2", n(6 + 4 / 2)), ("20 − 8 + 5", n(20 - 8 + 5)), ("24 ÷ 4 × 2", n(24 / 4 * 2)), ("3 + 5 × 2²", n(3 + 5 * 4)),
          ("(3 + 5) × 2²", n(8 * 4)), ("40 ÷ (2 + 3) × 4", n(40 / 5 * 4)), ("7 − 2(3² − 4) + 15", n(7 - 2 * 5 + 15)),
          ("5 + 12 ÷ 4 × 15 − 3²", n(5 + 12 / 4 * 15 - 9)), ("√(36 + 64)", n(sqrt(100))), ("4 + √81 × 2", n(4 + 9 * 2)),
          ("[[18 + 6|2 × 3]]", n(24 / 6)), ("[[5² − 1|4 + 2²]]", n(24 / 8)), ("[[5 + 12 ÷ 4 × 15 + 15²|6]]", r((5 + 45 + 225) / 6, 2)),
          ("3[20 − 2(4 + 3)]", n(3 * 6)), ("100 − 4(2 + 3)²", n(100 - 4 * 25)), ("2³ + 6(9 − 5) ÷ 8", n(8 + 24 / 8)),
          ("(7 + 12)(7 − 12)", n(19 * -5)), ("[[8(6 + 14)|8 + 6 + 14]]", r(160 / 28, 2))], cols=3)

summary(["Order: grouping symbols, then exponents and roots, then × and ÷ left to right, then + and − left to right.",
         "A fraction bar and a root sign are grouping symbols.",
         "A number against a parenthesis means multiply.",
         "Write one operation per line and copy the rest unchanged.",
         "On a calculator, a fraction needs parentheses around its top and around its bottom."])
review([("In your own words, list the four levels of the order of operations.",
         "1 grouping symbols; 2 exponents and roots; 3 multiplication and division, left to right; 4 addition and subtraction, left to right."),
        ("15 − 6 + 4", n(13)), ("36 ÷ 6 × 3", n(18)), ("9 + 3 × 4²", n(57)), ("(9 + 3) × 4²", n(192)), ("50 − 2(3 + 4²)", n(50 - 38)),
        ("8 − 5(6² ÷ 9) + 20", n(8 - 20 + 20)), ("√(5² + 12²)", n(13)), ("3√49 − 2³", n(21 - 8)),
        ("[[30 − 2(3² − 4)|2² + 1]]", n(20 / 5)), ("[[14 − 2(5² ÷ 5) + 8|3² − 5]]", n(12 / 4)),
        ("4[2 + 3(8 − 6)²]", n(4 * 14)), ("[[6² + 8²|2 × 5]]", n(10)), ("2.5(4.2 − 1.7)²  (do not round)", n(2.5 * 2.5 ** 2)),
        ("[[16(6 + 8)|16 + 6 + 8]]  (nearest hundredth)", r(224 / 30, 2)),
        ("A student evaluates 30 − 10 + 5 and gets 15. What was the mistake, and what is the answer?",
         "The student added 10 + 5 first. Left to right: 30 − 10 = 20, then 20 + 5 = 25."),
        ("Write the keystrokes, with parentheses, for [[7 + 9|2 × 4]].", "(7 + 9) ÷ (2 × 4) = 2"),
        ("Does 3(4)² equal 144 or 48? Explain.", "48. The exponent applies to the 4 only and is done before multiplying: 3 × 16.")])

# =====================================================================  8
chapter("Evaluating Formulas",
        ["Explain what a formula is and what its letters stand for.",
         "Substitute given values into a formula, showing the substitution.",
         "Evaluate the result using the order of operations.",
         "Evaluate formulas containing exponents, roots and fraction bars.",
         "Round and label the answer as a problem directs."],
        "The trades run on formulas: for the load a post will carry, the speed of a grinding wheel, the capacitance of a circuit. "
        "Nobody memorizes them all. What matters is the skill of putting the right numbers in and working them out correctly.",
        [("formula", "A rule written with letters that tells how to calculate one quantity from others."),
         ("variable", "A letter that stands for a number."),
         ("substitute", "To replace each letter with its given number."),
         ("subscript", "A small lowered label that tells similar letters apart, as in C_{1} and C_{2}."),
         ("constant", "A number in a formula that never changes, such as the 12 in L = πdr ÷ 12.")])

sec("8.1 What a formula says")
p("A **formula** is a sentence in shorthand. The formula *A = LW* says “the area of a rectangle equals its length times its width.” "
  "Each letter is a **variable**: a placeholder waiting for a number. Letters written side by side are multiplied.")
bullets(["Capital and lowercase letters are **different** variables. In N = √(D ÷ d)⁵, *D* and *d* are two different diameters.",
         "A **subscript** makes a new variable name. C_{1}, C_{2} and C_{3} are three different capacitors. The subscript is a label, not a number to calculate with.",
         "Numbers that appear in a formula, such as 1.085 or 12, are **constants**. Leave them exactly as they are."])

sec("8.2 Substitute, then evaluate")
rule("Three lines for every formula problem",
     "**1. Write the formula.**",
     "**2. Substitute.** Rewrite the formula with each letter replaced by its number **in parentheses**. Change nothing else.",
     "**3. Evaluate** by the order of operations, then round and write the unit.")
p("The parentheses in step 2 matter. They keep a multiplication from disappearing (2*C* with *C* = 30 must become 2(30), not 230) "
  "and they keep negative numbers and fractions together.")
example("Evaluate L = 3A + 4(B + C) for A = 2, B = 3 and C = 4.",
        [("L = 3A + 4(B + C)", "Write the formula."), ("L = 3(2) + 4(3 + 4)", "Substitute. Every letter is replaced; nothing else moves."),
         ("L = 3(2) + 4(7)", "Parentheses first."), ("L = 6 + 28", "Multiply."), ("L = 34", "Add.")], "L = 34")
example("Evaluate  2C + 1.6(D + d) + [[D + d|4C]]  for C = 30 in, D = 10 in and d = 5 in. Give a mixed number or a non-rounded decimal.",
        [("2(30) + 1.6(10 + 5) + [[10 + 5|4(30)]]", "Substitute."), ("2(30) + 1.6(15) + [[15|120]]", "Grouping: the parentheses, and the top and bottom of the fraction."),
         ("60 + 24 + 0.125", "Multiply and divide."), ("84.125", "Add. The problem forbids rounding, so every digit stays.")],
        "84.125 in, or 84 [[1|8]] in", title="Two variables that look alike")
warn("Show the substitution line",
     "Going straight from the formula to the answer hides where an error happened and usually costs credit. "
     "The substitution line is the proof that the right number went in the right place.")

sec("8.3 Formulas from the trades")
p("The examples that follow use real formulas. In each one, read the description to match every letter with its number, and note how the answer is to be rounded.")
example("**Machine trades.** The linear speed of a grinding wheel in feet per minute is L = [[πdr|12]], where d is the wheel diameter in inches and r is the speed in rpm. "
        "Find the linear speed of an 8-in wheel turning at 1750 rpm. Use π = 3.14 and round to the nearest whole number.",
        [("L = [[πdr|12]]", "Formula."), ("L = [[(3.14)(8)(1750)|12]]", "Substitute."), ("L = [[43,960|12]]", "Multiply across the top."),
         ("L = 3663.33…", "Divide."), ("L = 3663", "Round as directed.")], "3663 ft/min")
example("**Construction.** The crushing load in tons of a square wooden post is L = [[25T⁴|H²]], where T is the thickness in inches and H is the height in feet. "
        "Find the crushing load of a 4-in post 8 ft high.",
        [("L = [[25T⁴|H²]]", "Formula."), ("L = [[25(4)⁴|(8)²]]", "Substitute."), ("L = [[25(256)|64]]", "Exponents first: 4⁴ = 256 and 8² = 64."),
         ("L = [[6400|64]] = 100", "Multiply the top, then divide.")], "100 tons", title="Exponents")
warn("The exponent belongs only to what it touches",
     "In 25T⁴ the exponent applies to T alone. Raise 4 to the fourth power **first**, then multiply by 25. Multiplying 25 × 4 first and then raising 100 to the fourth power gives one hundred million.")
example("**Plumbing.** To carry the same flow as one pipe of diameter D, the number of smaller pipes of diameter d needed is N = √(D ÷ d)⁵. "
        "How many 2-in pipes are needed to equal one 6-in pipe? Round to the nearest whole number.",
        [("N = √([[D|d]])⁵", "Formula."), ("N = √([[6|2]])⁵", "Substitute."), ("N = √(3)⁵", "Innermost grouping first: 6 ÷ 2 = 3."),
         ("N = √243", "The exponent is under the root sign, so it is done before the root: 3⁵ = 243."), ("N = 15.588…", "Take the square root."),
         ("N = 16", "Round to the nearest whole number.")], "16 pipes", title="A root")
tip("Keying a root of a power",
    "Enter it the way it is grouped: `√( (6 ÷ 2) ^ 5 )`. Open a parenthesis after the root sign and close it at the very end, so the root covers the whole power.")
example("**Electronics.** For one capacitor in series with two in parallel, the total capacitance is C_{T} = [[C_{1}(C_{2} + C_{3})|C_{1} + C_{2} + C_{3}]]. "
        "Find C_{T} when C_{1} = 12 µF, C_{2} = 5 µF and C_{3} = 7 µF. Round to the nearest hundredth.",
        [("C_{T} = [[12(5 + 7)|12 + 5 + 7]]", "Substitute. The subscripts only say which capacitor is which."),
         ("C_{T} = [[12(12)|24]]", "Parentheses on top; add across the bottom."), ("C_{T} = [[144|24]] = 6", "Multiply the top, then divide.")],
        "6 µF", title="Subscripts and a fraction bar")
example("**Manufacturing.** The capacity of a feeder belt in metric tons per hour is C = [[W²DS|1.085]], where W is the belt width in meters, D is the density of the material in kg/m³ and S is the belt speed in m/s. "
        "Find the capacity for W = 1.2 m, D = 800 kg/m³ and S = 2.5 m/s. Round to the nearest whole number.",
        [("C = [[(1.2)²(800)(2.5)|1.085]]", "Substitute."), ("C = [[(1.44)(800)(2.5)|1.085]]", "Exponent first."), ("C = [[2880|1.085]]", "Multiply across the top."),
         ("C = 2654.37…", "Divide."), ("C = 2654", "Round.")], "2654 metric tons per hour")

ev = [("N = (a + b)(a − b);  a = 9, b = 14", n((9 + 14) * (9 - 14))),
      ("L = [[s(P + p)|2]];  s = 4.5, P = 42, p = 30", n(4.5 * 72 / 2)),
      ("f = [[1|8N]];  N = 5  (answer as a fraction)", "[[1|40]]"),
      ("t = [[D − d|L]];  D = 15, d = 6, L = 3", n(3)),
      ("V = [[gt²|2]];  g = 32.2, t = 2.5", n(32.2 * 6.25 / 2)),
      ("P = 2L + 2W;  L = 18.5 ft, W = 12.25 ft", n(2 * 18.5 + 2 * 12.25) + " ft"),
      ("A = [[(b_{1} + b_{2})h|2]];  b_{1} = 9, b_{2} = 14, h = 6", n(23 * 6 / 2)),
      ("c = √(a² + b²);  a = 9, b = 12", n(15)),
      ("**Welding.** Tensile strength T = [[L|A]] psi. L = 9,800 lb, A = 0.14 sq in.", n(9800 / 0.14) + " psi"),
      ("**Electrical.** Power P = I²R watts. I = 2.5 A, R = 48 Ω.", n(2.5 ** 2 * 48) + " W"),
      ("**Machine trades.** L = [[πdr|12]]. d = 10 in, r = 1200 rpm, π = 3.14.", n(3.14 * 10 * 1200 / 12) + " ft/min"),
      ("**Construction.** L = [[25T⁴|H²]]. T = 6 in, H = 10 ft.", n(25 * 6 ** 4 / 100) + " tons"),
      ("**Plumbing.** N = √(D ÷ d)⁵. D = 4 in, d = 1 in.", n(sqrt(4 ** 5)) + " pipes"),
      ("**Plumbing.** N = √(D ÷ d)⁵. D = 3 in, d = [[3|4]] in. Round to the nearest whole number.", r(sqrt(4 ** 5), 0) + " pipes"),
      ("**Electronics.** Two inductors in parallel: L_{T} = [[L_{1}L_{2}|L_{1} + L_{2}]]. L_{1} = 300 mH, L_{2} = 60 mH.", n(300 * 60 / 360) + " mH"),
      ("**Electronics.** C_{T} = [[C_{1}(C_{2} + C_{3})|C_{1} + C_{2} + C_{3}]]. C_{1} = 20, C_{2} = 4, C_{3} = 9 (µF). Nearest hundredth.", r(20 * 13 / 33, 2) + " µF"),
      ("**Electronics.** Inductance of a coil L = [[R²N²|9R + 10D]] µH. R = 2 in, D = 5 in, N = 150 turns. Nearest whole number.",
       r(4 * 150 ** 2 / (18 + 50), 0) + " µH"),
      ("**Automotive.** Indicated horsepower ihp = [[MEP × D × S|792,000]]. MEP = 150 psi, D = 300 cu in, S = 3300 rpm.", n(150 * 300 * 3300 / 792000) + " hp"),
      ("**Hydraulics.** Force on a piston F = [[πPD²|4]] lb. P = 40 psi, D = 2.5 in, π = 3.14. Nearest whole number.", r(3.14 * 40 * 2.5 ** 2 / 4, 0) + " lb"),
      ("**Manufacturing.** C = [[W²DS|1.085]]. W = 0.9 m, D = 1500 kg/m³, S = 2 m/s. Nearest whole number.", r(0.81 * 1500 * 2 / 1.085, 0) + " t/h")]
practice("Substitute and evaluate", "Write the formula, show the substitution, and evaluate. Do not round unless told to.", ev, cols=1)

summary(["A formula is a rule; its letters are placeholders for numbers.",
         "Write the formula, substitute with parentheses, then evaluate by the order of operations.",
         "Capital and lowercase letters, and letters with different subscripts, are different variables.",
         "An exponent applies only to the quantity it touches.",
         "Round only at the end, as the problem directs, and write the unit."])
review([("Evaluate L = 5A + 2(B + C) for A = 3, B = 6, C = 2.", n(15 + 16)),
        ("Evaluate 3C + 2.4(D − d) for C = 12, D = 9, d = 4.", n(36 + 12)),
        ("Evaluate [[D + d|2C]] for D = 14, d = 6, C = 8. Give a decimal.", n(20 / 16)),
        ("Evaluate N = (a + b)(a − b) for a = 5, b = 11.", n(16 * -6)),
        ("Evaluate V = [[gt²|2]] for g = 32.2 and t = 3.", n(32.2 * 9 / 2)),
        ("Evaluate A = √(s(s − a)(s − b)(s − c)) for s = 12, a = 6, b = 8, c = 10.", n(sqrt(12 * 6 * 4 * 2))),
        ("Tensile strength T = [[L|A]]. L = 15,000 lb, A = 0.21 sq in. Round to the nearest hundred psi.", r(15000 / 0.21, -2) + " psi"),
        ("Grinding wheel L = [[πdr|12]]. d = 7 in, r = 3000 rpm, π = 3.14.", n(3.14 * 7 * 3000 / 12) + " ft/min"),
        ("Crushing load L = [[25T⁴|H²]]. T = 8 in, H = 16 ft.", n(25 * 8 ** 4 / 256) + " tons"),
        ("Pipes N = √(D ÷ d)⁵. D = 12 in, d = 4 in. Nearest whole number.", r(sqrt(3 ** 5), 0) + " pipes"),
        ("Feeder belt C = [[W²DS|1.085]]. W = 1.5 m, D = 600, S = 3. Nearest whole number.", r(2.25 * 600 * 3 / 1.085, 0) + " t/h"),
        ("Piston force F = [[πPD²|4]]. P = 30 psi, D = 4 in, π = 3.14.", n(3.14 * 30 * 16 / 4) + " lb"),
        ("C_{T} = [[C_{1}(C_{2} + C_{3})|C_{1} + C_{2} + C_{3}]] for C_{1} = 18, C_{2} = 7, C_{3} = 5. Nearest hundredth.", r(18 * 12 / 30, 2) + " µF"),
        ("L_{T} = [[L_{1}L_{2}|L_{1} + L_{2}]] for L_{1} = 120 mH and L_{2} = 80 mH.", n(120 * 80 / 200) + " mH"),
        ("In the formula C = [[W²DS|1.085]], which symbols are variables and which is a constant?", "W, D, S and C are variables; 1.085 is a constant."),
        ("A student substitutes C = 30 into 2C and writes 230. What should have been written?", "2(30), which is 60.")])

# =====================================================================  9
chapter("Solving Formulas",
        ["Explain what it means to solve an equation.",
         "Undo an operation with its inverse, keeping the equation balanced.",
         "Solve one-step and two-step equations.",
         "Substitute into a formula and solve for the unknown that is left.",
         "Solve equations that contain fractions without rounding."],
        "In Chapter 8 the unknown always stood alone on the left: put the numbers in and calculate. On the job it is often "
        "the other way round. You know the volume a tank must hold and need its height; you know the perimeter of a fence and need its length. "
        "Then the formula has to be run backward.",
        [("equation", "A statement that two expressions are equal."),
         ("solve", "To find the value of the unknown that makes the equation true."),
         ("inverse operation", "The operation that undoes another: + and −, × and ÷, square and square root."),
         ("isolate", "To get the unknown alone on one side of the equals sign."),
         ("coefficient", "The number multiplying a variable: the 2 in 2L.")])

sec("9.1 Equations and balance")
p("An equation is like a balance scale: the two sides weigh the same. Whatever is done to one side must be done to the other, "
  "or the scale tips and the equation is no longer true.")
fig(figs.balance("2L + 1000", "3500", "Take 1000 from both pans and the scale stays level: 2L = 2500."), "An equation is a balance.")
rule("The golden rule of equations", "Do the same thing to both sides.",
     "You may add the same number to both sides, subtract the same number from both sides, multiply both sides by the same number, "
     "or divide both sides by the same number (except zero).")
p("To **solve** an equation is to get the unknown letter alone: *x* = a number. That is done by removing everything else from "
  "its side, one operation at a time, using **inverse operations**.")
table(["If the unknown has had this done to it", "Undo it by", "Example"],
      [["a number added:  x + 7 = 19", "subtracting it from both sides", "x = 19 − 7 = 12"],
       ["a number subtracted:  x − 7 = 19", "adding it to both sides", "x = 19 + 7 = 26"],
       ["multiplied by a number:  7x = 21", "dividing both sides by it", "x = 21 ÷ 7 = 3"],
       ["divided by a number:  [[x|7]] = 21", "multiplying both sides by it", "x = 21 × 7 = 147"]], widths=[42, 32, 26])

sec("9.2 One-step equations")
example("Ohm’s law is I = [[E|R]]. A circuit carries a current I = 0.60 A through a resistance R = 400 Ω. Find the voltage E.",
        [("I = [[E|R]]", "Formula."), ("0.60 = [[E|400]]", "Substitute what is known. One letter is left."),
         ("0.60 × 400 = [[E|400]] × 400", "E is divided by 400. Undo it: multiply both sides by 400."), ("240 = E", "The 400s cancel on the right.")],
        "E = 240 V")
example("A semi-trailer’s volume is V = LWH. It holds V = 3600 cu ft and is L = 50 ft long and W = 8.5 ft wide. Find its height to the nearest tenth.",
        [("3600 = (50)(8.5)H", "Substitute."), ("3600 = 425H", "Simplify the right side first: 50 × 8.5 = 425."),
         ("[[3600|425]] = [[425H|425]]", "H is multiplied by 425. Divide both sides by 425."), ("8.4705… = H", ""), ("H = 8.5", "Round to the nearest tenth.")],
        "H = 8.5 ft")
rule("Simplify before you solve",
     "After substituting, combine everything that can be combined on each side. Then start undoing. "
     "In the trailer example, multiplying 50 × 8.5 first left a simple one-step equation.")
p("It makes no difference which side the unknown ends up on: 240 = *E* says the same thing as *E* = 240.")

one = [("**Aviation.** D = RT. D = 1,400 mi, R = 250 mph. Find T.", n(1400 / 250) + " h"),
       ("**Sheet metal.** Water pressure P = 62.4D lb/sq ft at depth D ft. P = 936. Find D.", n(936 / 62.4) + " ft"),
       ("**Physics.** fw = 343. f = 250. Find w.", n(343 / 250) + " m"),
       ("**Physics.** PV = 1080. V = 45 cu ft. Find P.", n(1080 / 45) + " psi"),
       ("**Electrical.** Transformer E = 40W. E = 1,000 V. Find W.", n(1000 / 40) + " windings"),
       ("**Electrical.** I = [[E|R]]. I = 1.5 A, R = 80 Ω. Find E.", n(120) + " V"),
       ("**Welding.** T = [[L|A]]. T = 60,000 psi, A = 0.25 sq in. Find L.", n(15000) + " lb"),
       ("A = LW. A = 187 sq ft, W = 11 ft. Find L.", n(17) + " ft"),
       ("V = LWH. V = 2,880 cu ft, L = 40 ft, H = 9 ft. Find W.", n(8) + " ft"),
       ("x + 14.5 = 32", n(17.5)), ("y − 3.75 = 12", n(15.75)), ("[[n|6]] = 4.5", n(27))]
practice("One-step equations", "Substitute and solve. Show the step that undoes the operation.", one, cols=2)

sec("9.3 Two-step equations")
p("When the unknown has been multiplied **and** something has been added or subtracted, there are two operations to undo. "
  "Undo them in the **reverse** of the order of operations: first the addition or subtraction, then the multiplication or division. "
  "Think of taking off shoes and socks: the last thing put on is the first thing taken off.")
fig(figs.pemdas_two_way(), "The same list, read in opposite directions. Evaluating does the operations from P down; solving undoes them from A S up.")
p("When you **evaluate**, the value of the letter is known and you do the operations in PEMDAS order, starting at P and finishing with A S. "
  "When you **solve**, the letter is unknown and has already had those operations done to it, so you take them off again in the opposite order: "
  "start at **A S** (whichever comes first), then **M D**, then **E**, and finish with **P**.")
rule("Solving a two-step equation",
     "**1.** Substitute and simplify each side.",
     "**2.** Undo the **addition or subtraction**: move the plain number away from the unknown’s side.",
     "**3.** Undo the **multiplication or division**: divide by the coefficient.",
     "**4.** Check by putting the answer back into the original equation.")
example("The perimeter of a rectangle is P = 2L + 2W. A pasture is to be fenced with P = 3200 ft of fence and is W = 450 ft wide. Find its length.",
        [("3200 = 2L + 2(450)", "Substitute."), ("3200 = 2L + 900", "Simplify: 2(450) = 900."),
         ("3200 − 900 = 2L + 900 − 900", "900 is added to the 2L. Subtract 900 from both sides."), ("2300 = 2L", ""),
         ("[[2300|2]] = [[2L|2]]", "L is multiplied by 2. Divide both sides by 2."), ("1150 = L", ""),
         ("Check: 2(1150) + 2(450) = 2300 + 900 = 3200 ✓", "The answer makes the original equation true.")], "L = 1150 ft")
example("A service call is billed as T = 45 + 60H dollars, where H is the number of hours. A bill came to T = $345. How many hours were worked?",
        [("345 = 45 + 60H", "Substitute."), ("345 − 45 = 60H", "Subtract 45 from both sides."), ("300 = 60H", ""), ("H = 300 ÷ 60 = 5", "Divide both sides by 60.")],
        "H = 5 hours")
example("The length of a belt around two pulleys is L = 2d + 3.26(r + R). With r = 5 in, R = 9 in and L = 90 in, find the distance d between centers to the nearest inch.",
        [("90 = 2d + 3.26(5 + 9)", "Substitute."), ("90 = 2d + 3.26(14)", "Simplify inside the parentheses."), ("90 = 2d + 45.64", "Multiply."),
         ("90 − 45.64 = 2d", "Subtract 45.64 from both sides."), ("44.36 = 2d", ""), ("d = 22.18", "Divide both sides by 2."), ("d = 22", "Round to the nearest inch.")],
        "d = 22 in")
warn("Subtract first, then divide",
     "In 3200 = 2L + 900, dividing 3200 by 2 first is wrong unless the 900 is divided too. Clear the added number first, and the mistake cannot happen.")
sub("When the coefficient is negative")
p("Some formulas subtract a multiple of the unknown. The steps are the same; just carry the negative sign along.")
example("Air temperature falls with altitude: T = −0.002H + G, where G is the ground temperature in °F and H is the height in feet. If G = 70°F, at what height is T = 32°F?",
        [("32 = −0.002H + 70", "Substitute."), ("32 − 70 = −0.002H", "Subtract 70 from both sides."), ("−38 = −0.002H", "A smaller number minus a larger one is negative."),
         ("H = [[−38|−0.002]] = 19,000", "Divide both sides by −0.002. A negative divided by a negative is positive.")], "H = 19,000 ft")

sec("9.4 Equations with fractions")
p("Sheet-metal and carpentry formulas are full of fractions, and the answers are expected as exact fractions. The steps do not change. "
  "Only the arithmetic does, so take it slowly.")
example("The allowance for a Pittsburgh lock seam is A = 2w + [[3|16]] in, where w is the width of the pocket. If A = [[7|8]] in, find w as a fraction in lowest terms.",
        [("[[7|8]] = 2w + [[3|16]]", "Substitute."), ("[[7|8]] − [[3|16]] = 2w", "Subtract [[3|16]] from both sides."),
         ("[[14|16]] − [[3|16]] = [[11|16]] = 2w", "Common denominator 16: [[7|8]] = [[14|16]]."),
         ("w = [[11|16]] ÷ 2 = [[11|32]]", "Divide both sides by 2. Dividing a fraction by 2 **doubles its denominator**."),
         ("Check: 2([[11|32]]) + [[3|16]] = [[11|16]] + [[3|16]] = [[14|16]] = [[7|8]] ✓", "")], "w = [[11|32]] in")
warn("Two traps in the lock-seam problem",
     "**Adding instead of subtracting.** The [[3|16]] is added to 2w, so it must be *subtracted* from both sides. Adding gives [[17|16]], and the final answer comes out far too large.",
     "**Multiplying instead of dividing.** 2w means 2 times w, so undo it by dividing by 2. Half of [[11|16]] is [[11|32]], a smaller piece. "
     "An answer bigger than A itself cannot be right: the pocket is only part of the allowance.")
tip("Checking with decimals",
    "Even when the answer must be a fraction, a decimal check takes seconds: 0.875 − 0.1875 = 0.6875, and 0.6875 ÷ 2 = 0.34375. "
    "Then 11 ÷ 32 = 0.34375. They agree.")

two = [("P = 2L + 2W. P = 2,600 ft, W = 350 ft. Find L.", n((2600 - 700) / 2) + " ft"),
       ("P = 2L + 2W. P = 94 in, L = 28.5 in. Find W.", n((94 - 57) / 2) + " in"),
       ("**Office services.** T = 45 + 60H. T = $435. Find H.", n(390 / 60) + " h"),
       ("**Water/wastewater.** P = 0.52D + 14.7. P = 30.3 psi. Find D.", n(15.6 / 0.52) + " ft"),
       ("**Electronics.** R = 0.02T + 5. R = 5.36. Find T.", n(0.36 / 0.02)),
       ("**Meteorology.** T = −0.002H + G. G = 80°F, T = 44°F. Find H.", n(36 / 0.002) + " ft"),
       ("**Sports.** Maximum heart rate R = −0.8A + 176. R = 140. Find the age A.", n(36 / 0.8) + " years"),
       ("**Automotive.** P + 2T = C. P = 3.250 in, C = 3.625 in. Find T (do not round).", n(0.375 / 2) + " in"),
       ("**Trades management.** A = RT + M. A = $2,900, M = $740, R = $72 per hour. Find T.", n(2160 / 72) + " h"),
       ("**Machine trades.** L = 2d + 3.26(r + R). r = 4 in, R = 6 in, L = 70 in. Find d to the nearest inch.", r((70 - 32.6) / 2, 0) + " in"),
       ("**Sheet metal.** A = 2w + [[3|16]]. A = [[11|16]] in. Find w in lowest terms.", fr((Fraction(11, 16) - Fraction(3, 16)) / 2) + " in"),
       ("**Sheet metal.** A = 2w + [[3|16]]. A = [[15|16]] in. Find w in lowest terms.", fr((Fraction(15, 16) - Fraction(3, 16)) / 2) + " in"),
       ("**Sheet metal.** A = 2w + [[3|16]]. A = 1 [[1|8]] in. Find w in lowest terms.", fr((Fraction(9, 8) - Fraction(3, 16)) / 2) + " in"),
       ("3x + 8 = 29", n(7)), ("5y − 12 = 48", n(12)), ("[[n|4]] + 6 = 15", n(36))]
practice("Two-step equations", "Substitute and solve. Show every substitution and the steps.", two, cols=1)

summary(["An equation stays true when the same thing is done to both sides.",
         "Solve by undoing operations with their inverses until the unknown stands alone.",
         "Substitute first, simplify each side, then solve.",
         "In a two-step equation undo addition or subtraction first, then multiplication or division.",
         "With fractions, find a common denominator to subtract; dividing a fraction by 2 doubles its denominator.",
         "Always check the answer in the original formula."])
review([("x + 9.5 = 21", n(11.5)), ("7m = 94.5", n(13.5)), ("[[k|12]] = 2.5", n(30)), ("4x + 7 = 39", n(8)), ("6y − 15 = 57", n(12)),
        ("D = RT. D = 1,050 mi, R = 420 mph. Find T.", n(2.5) + " h"),
        ("I = [[E|R]]. I = 2.4 A, R = 50 Ω. Find E.", n(120) + " V"),
        ("V = LWH. V = 4,200 cu ft, L = 48 ft, W = 8.5 ft. Find H to the nearest tenth.", r(4200 / (48 * 8.5), 1) + " ft"),
        ("P = 2L + 2W. P = 4,100 ft, W = 600 ft. Find L.", n((4100 - 1200) / 2) + " ft"),
        ("T = 45 + 60H. T = $255. Find H.", n(3.5) + " h"),
        ("P = 0.52D + 14.7. P = 40.7 psi. Find D.", n(26 / 0.52) + " ft"),
        ("R = −0.8A + 176. R = 152. Find A.", n(30) + " years"),
        ("A = RT + M. A = $4,150, M = $1,030, R = $78. Find T.", n(3120 / 78) + " h"),
        ("L = 2d + 3.26(r + R). r = 7 in, R = 7 in, L = 100 in. Find d to the nearest inch.", r((100 - 45.64) / 2, 0) + " in"),
        ("A = 2w + [[3|16]]. A = [[13|16]] in. Find w in lowest terms.", fr((Fraction(13, 16) - Fraction(3, 16)) / 2) + " in"),
        ("A = 2w + [[3|16]]. A = [[3|4]] in. Find w in lowest terms.", fr((Fraction(3, 4) - Fraction(3, 16)) / 2) + " in"),
        ("S = [[πdn|12]]. S = 5,000 ft/min, d = 6 in, π = 3.14. Find n to the nearest hundred rpm.", r(5000 * 12 / (3.14 * 6), -2) + " rpm"),
        ("A student solves [[5|8]] = 2w + [[1|8]] and gets w = 1 [[1|2]]. Find the correct answer and name the likely mistakes.",
         "w = [[1|4]]. The student added 1/8 instead of subtracting it and multiplied by 2 instead of dividing.")])
