"""Added depth for Part 4 (geometry): more explanation, worked examples, practice and review."""
import random
from math import sqrt
from book import *  # noqa: F401,F403
from util import n, r
import figs

PI = 3.14


def hero(a, b, c):
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


def L_item(a, b, c, d, unit="ft"):
    """an L-shaped figure a by b overall with a c by d corner missing, done as two trapezoids"""
    A = (b + d) * (a - c) / 2
    B = (c + a) * (b - d) / 2
    return (f"An L-shaped figure is {a} {unit} by {b} {unit} overall, with a {c} {unit} by {d} {unit} corner missing "
            f"(the {c}-{unit} side of the notch runs along the {a}-{unit} side). Split it into two trapezoids and find the area.",
            f"Trapezoids: ({b} + {d})({a - c}) ÷ 2 = {n(A)} and ({c} + {a})({b - d}) ÷ 2 = {n(B)}; total {n(A + B)} sq {unit}")


# =====================================================================  10
def ch10():
    rg = random.Random(1010)
    sec("10.5 Units inside an area problem")
    p("An area formula multiplies two lengths, and it only works when both lengths are in the **same unit**. A drawing may give one side in feet "
      "and the other in inches. Decide which unit the answer should be in, convert first, and multiply second.")
    rule("Convert, then calculate",
         "**1.** Choose the unit the answer needs (the unit the material is sold in is usually the best choice).",
         "**2.** Convert every dimension to that unit.",
         "**3.** Use the formula.",
         "If the area is already calculated in the wrong square unit, convert it with the area factors 144, 9 and 1296 from Chapter 4.")
    example("A sheet-metal panel is 4 ft long and 18 in wide. Find its area in square feet and in square inches.",
            [("18 in ÷ 12 = 1.5 ft", "For square feet, change the inches to feet."), ("A = LW = (4)(1.5) = 6", "Both sides are now in feet."),
             ("4 ft × 12 = 48 in", "For square inches, change the feet to inches instead."), ("A = (48)(18) = 864", "Both sides in inches."),
             ("864 ÷ 144 = 6 ✓", "Check: the two answers must agree when converted.")], "6 sq ft, or 864 sq in")
    example("A rectangular duct is 30 in by 18 in. What is its cross-sectional area in square feet?",
            [("A = (30)(18) = 540 sq in", "It is easiest to multiply in inches first."), ("540 ÷ 144 = 3.75", "Square inches to square feet: divide by 144, not 12.")],
            "3.75 sq ft", title="Convert the area afterward")
    warn("Never multiply feet by inches",
         "4 × 18 = 72 is neither square feet nor square inches. It is a meaningless number. Make the units match before any multiplying is done.")
    example("A trapezoidal gusset has bases of 1 ft 6 in and 2 ft 3 in and a height of 10 in. Find its area in square inches.",
            [("1 ft 6 in = 18 in;  2 ft 3 in = 27 in", "Change each base to inches: 12 + 6 and 24 + 3."),
             ("A = [[(18 + 27)(10)|2]]", "Substitute into the trapezoid formula."), ("A = [[(45)(10)|2]] = [[450|2]] = 225", "Add the bases, multiply, halve.")],
            "225 sq in", title="Feet and inches together")

    sec("10.6 Estimating material and cost")
    p("Most real area problems end with a purchase. The pattern is always the same: find the area, subtract what is not covered, add waste if "
      "the job calls for it, divide by what one unit of material covers, and **round up** to a whole unit, because stores do not sell part of a sheet or part of a can.")
    example("A wall 22 ft long and 8 ft high has a 3 ft by 7 ft door and a 4 ft by 5 ft window. One gallon of paint covers 350 sq ft. How many gallons are needed for two coats?",
            [("Wall: (22)(8) = 176 sq ft", "The whole wall."), ("Openings: (3)(7) + (4)(5) = 21 + 20 = 41 sq ft", "The door and the window are not painted."),
             ("176 − 41 = 135 sq ft", "Area to paint, one coat."), ("135 × 2 = 270 sq ft", "Two coats."),
             ("270 ÷ 350 = 0.77…", "Divide by the coverage of one gallon."), ("1 gallon", "Round up to a whole can.")], "1 gallon", title="Paint")
    example("A floor 15 ft by 21 ft is to be covered with plywood sheets 4 ft by 8 ft. Allow 10% for waste. How many sheets should be ordered?",
            [("Floor: (15)(21) = 315 sq ft", ""), ("Waste: 315 × 0.10 = 31.5;  315 + 31.5 = 346.5 sq ft", "Add 10% of the area."),
             ("One sheet: (4)(8) = 32 sq ft", ""), ("346.5 ÷ 32 = 10.83", "Divide by the area of one sheet."), ("11 sheets", "Round **up**.")],
            "11 sheets", title="Sheet goods")
    example("A lot 85 ft by 140 ft is to be fenced on all four sides. Fencing costs $6.75 per foot installed. Find the cost.",
            [("P = 2L + 2W = 2(140) + 2(85)", "A fence goes around: perimeter, not area."), ("P = 280 + 170 = 450 ft", ""),
             ("450 × 6.75 = 3037.50", "Feet times dollars per foot.")], "$3,037.50", title="Perimeter and cost")
    shop("Round up, not off",
         "10.2 sheets means 11 sheets. 10.83 sheets also means 11. In ordering, any fraction of a unit rounds **up**, even 0.01. "
         "Rounding to the nearest whole number is for measurements, not for purchases.")

    sec("10.7 A closer look at trapezoids")
    p("Trapezoids turn up wherever one size has to change into another: duct transitions, hoppers, roof sections, ramp sides, dam and ditch cross-sections. "
      "A few facts make them easier to handle.")
    bullets(["The **bases are the two parallel sides**. They are not always the top and bottom. Turn the page until the parallel sides are level and the picture looks familiar.",
             "The **height** is the perpendicular distance between the bases. It is drawn dashed, with a square corner mark.",
             "In a **right trapezoid** one side is square to the bases, and that side **is** the height.",
             "In an **isosceles trapezoid** the two slanted sides are equal, and the figure is the same on the left and the right.",
             "The slanted sides are used for **perimeter only**."])
    fig(figs.side_by_side([figs.trapezoid_dims(8, 14, 6, 6.7, 6.7), figs.trapezoid_dims(10, 16, 7)], gap=10),
        "Two trapezoids. In both, the bases are the parallel top and bottom and the height is the dashed line.")
    example("An isosceles trapezoid has bases 8 in and 14 in, height 6 in and slanted sides 6.7 in (Figure 10.7, left). Find its perimeter and area.",
            [("P = 8 + 14 + 6.7 + 6.7 = 35.4", "All four sides."), ("A = [[(8 + 14)(6)|2]] = [[(22)(6)|2]]", "Bases added, times height."),
             ("A = [[132|2]] = 66", "Divide by 2.")], "P = 35.4 in;  A = 66 sq in")
    example("The cross-section of a drainage ditch is a trapezoid 3 ft wide at the bottom, 9 ft wide at the top and 2.5 ft deep. Find the area of the cross-section.",
            [("b_{1} = 3, b_{2} = 9, h = 2.5", "The top and bottom of the ditch are parallel, so they are the bases. The depth is the height."),
             ("A = [[(3 + 9)(2.5)|2]] = [[(12)(2.5)|2]]", "Substitute."), ("A = [[30|2]] = 15", "")], "15 sq ft")
    example("A trapezoid has an area of 126 sq in, a height of 9 in and one base of 11 in. Find the other base.",
            [("126 = [[(11 + b)(9)|2]]", "Substitute what is known."), ("252 = (11 + b)(9)", "Multiply both sides by 2."), ("28 = 11 + b", "Divide both sides by 9."),
             ("b = 17", "Subtract 11 from both sides."), ("Check: (11 + 17)(9) ÷ 2 = 126 ✓", "")], "17 in", title="Finding a missing base")
    tip("One line for a trapezoid",
        "Key the area as `(b1 + b2) × h ÷ 2`, with the parentheses. For Example 10.15: `(3 + 9) × 2.5 ÷ 2` gives 15.")

    sec("10.8 Working backward: a summary")
    p("Every formula in this chapter can be run backward. Substitute what is known, then undo the operations in reverse order, as in Chapter 9.")
    table(["Known", "Wanted", "Steps"],
          [["rectangle: A and W", "L", "L = A ÷ W"], ["rectangle: P and W", "L", "subtract 2W, then divide by 2"], ["square: P", "s", "s = P ÷ 4"],
           ["square: A", "s", "s = √A"], ["parallelogram: A and b", "h", "h = A ÷ b"], ["parallelogram: P and b", "a", "subtract 2b, then divide by 2"],
           ["trapezoid: A, b_{1}, b_{2}", "h", "multiply by 2, then divide by (b_{1} + b_{2})"],
           ["trapezoid: A, h, b_{1}", "b_{2}", "multiply by 2, divide by h, subtract b_{1}"]], widths=[34, 14, 52])
    example("A parallelogram has a perimeter of 74 in and a base of 22 in. Find its slanted side.",
            [("74 = 2a + 2(22)", "Substitute into P = 2a + 2b."), ("74 = 2a + 44", ""), ("30 = 2a", "Subtract 44."), ("a = 15", "Divide by 2.")], "15 in")
    example("A square pad has a perimeter of 180 ft. Find its side and its area.",
            [("180 = 4s", "Substitute into P = 4s."), ("s = 45", "Divide by 4."), ("A = s² = (45)² = 2025", "Then the area.")], "s = 45 ft;  A = 2,025 sq ft")

    q = []
    for _ in range(4):
        L_, W_ = rg.randint(12, 60), rg.randint(5, 30)
        q.append((f"Rectangle: L = {L_} in, W = {W_} in. Find P and A.", f"P = {n(2 * L_ + 2 * W_)} in; A = {n(L_ * W_)} sq in"))
    for _ in range(3):
        s_ = rg.choice([6.5, 8.25, 11, 14.5, 19, 2.75])
        q.append((f"Square: s = {n(s_)} ft. Find P and A.", f"P = {n(4 * s_)} ft; A = {n(s_ * s_)} sq ft"))
    for _ in range(4):
        b_, a_, h_ = rg.randint(10, 40), rg.randint(6, 20), 0
        h_ = rg.randint(4, a_ - 1)
        q.append((f"Parallelogram: b = {b_} cm, a = {a_} cm, h = {h_} cm. Find P and A.", f"P = {n(2 * a_ + 2 * b_)} cm; A = {n(b_ * h_)} cm²"))
    for _ in range(7):
        b1 = rg.randint(4, 20)
        b2 = b1 + rg.randint(2, 14)
        h_ = rg.choice([3, 4, 5, 6, 7.5, 8, 9, 10, 12])
        q.append((f"Trapezoid: b₁ = {b1} in, b₂ = {b2} in, h = {n(h_)} in. Find A.", f"A = {n((b1 + b2) * h_ / 2)} sq in"))
    practice("More quadrilaterals", "Write the formula, substitute and calculate. Do not round.", q, cols=2)

    ap = [("A panel is 5 ft long and 30 in wide. Find its area in square feet.", n(5 * 2.5) + " sq ft"),
          ("A duct is 24 in by 16 in. Find its cross-sectional area in square feet, to the nearest hundredth.", r(24 * 16 / 144, 2) + " sq ft"),
          ("A room is 13 ft 6 in by 18 ft. Find its area in square feet.", n(13.5 * 18) + " sq ft"),
          ("Find the area of the room in problem 3 in square yards.", n(13.5 * 18 / 9) + " sq yd"),
          ("A trapezoid has bases of 2 ft and 3 ft 6 in and a height of 18 in. Find its area in square feet.", n((2 + 3.5) * 1.5 / 2) + " sq ft"),
          ("A wall 30 ft by 9 ft has three windows, each 3 ft by 4 ft. How many square feet are to be painted?", n(270 - 36) + " sq ft"),
          ("Paint covers 400 sq ft per gallon. How many gallons are needed for two coats on the wall in problem 6?", "2 gallons (468 ÷ 400 = 1.17, round up)"),
          ("A ceiling 24 ft by 32 ft is covered with 4 ft by 8 ft drywall sheets. How many sheets, with no waste?", n(24 * 32 / 32) + " sheets"),
          ("With 12% waste, how many sheets are needed for the ceiling in problem 8?", "27 sheets (860.16 ÷ 32 = 26.88, round up)"),
          ("A garden 40 ft by 65 ft is fenced at $4.20 per foot. Find the cost.", "$" + n(210 * 4.2, 2)),
          ("A 12 ft by 14 ft room is tiled with tiles 1 ft square that cost $2.85 each. Find the cost of the tile.", "$" + n(168 * 2.85, 2)),
          ("A ditch cross-section is a trapezoid 2 ft wide at the bottom, 7 ft wide at the top and 3 ft deep. Find its area.", n(9 * 3 / 2) + " sq ft"),
          ("A hopper side is a trapezoid with bases 48 in and 12 in and height 36 in. How many square feet of steel is that?", n(60 * 36 / 2 / 144) + " sq ft"),
          ("A parallelogram-shaped lot has a base of 120 ft and a height of 75 ft. How many square yards is it?", n(120 * 75 / 9) + " sq yd")]
    practice("Units, materials and cost", "Show each step. Round only where the problem says, and round purchases up.", ap, cols=1)

    wb = [("Rectangle: A = 432 sq in, W = 18 in. Find L.", "24 in"), ("Rectangle: A = 97.5 sq ft, L = 13 ft. Find W.", "7.5 ft"),
          ("Rectangle: P = 96 in, W = 17 in. Find L.", "31 in"), ("Rectangle: P = 250 ft, L = 80 ft. Find W.", "45 ft"),
          ("Square: P = 92 cm. Find s.", "23 cm"), ("Square: A = 361 sq in. Find s.", "19 in"), ("Square: A = 12.25 sq m. Find s.", "3.5 m"),
          ("Parallelogram: A = 221 sq in, b = 17 in. Find h.", "13 in"), ("Parallelogram: P = 110 cm, b = 35 cm. Find a.", "20 cm"),
          ("Trapezoid: A = 96 sq in, b₁ = 10 in, b₂ = 14 in. Find h.", "8 in"), ("Trapezoid: A = 210 sq ft, b₁ = 12 ft, b₂ = 23 ft. Find h.", "12 ft"),
          ("Trapezoid: A = 90 sq in, h = 6 in, b₁ = 11 in. Find b₂.", "19 in"), ("Trapezoid: A = 175 sq cm, h = 10 cm, b₁ = 13 cm. Find b₂.", "22 cm"),
          ("A rectangular duct must have an area of 288 sq in and can be only 12 in deep. How wide is it?", "24 in")]
    practice("Working backward", "Substitute what is known and solve. Show the steps.", wb, cols=2)

    more_review([("A panel is 6 ft by 20 in. Find its area in square feet.", n(10) + " sq ft"),
                 ("Trapezoid: bases 9 in and 15 in, height 7 in. Find A.", n(84) + " sq in"),
                 ("Trapezoid: bases 1 ft 3 in and 2 ft 1 in, height 8 in. Find A in square inches.", n((15 + 25) * 8 / 2) + " sq in"),
                 ("A right trapezoid has bases 6 ft and 10 ft and its square side is 5 ft. Find A.", n(40) + " sq ft"),
                 ("Trapezoid: A = 154 sq in, bases 10 in and 18 in. Find h.", "11 in"),
                 ("Trapezoid: A = 120 sq ft, h = 8 ft, one base 12 ft. Find the other base.", "18 ft"),
                 ("Parallelogram: P = 88 in, b = 26 in. Find a.", "18 in"), ("Square: P = 70 ft. Find A.", n(17.5 ** 2) + " sq ft"),
                 ("A 16 ft by 20 ft floor is covered with 4 ft by 8 ft sheets, with no waste. How many sheets?", "10 sheets"),
                 ("A wall 18 ft by 8 ft has a 6 ft by 7 ft opening. Paint covers 350 sq ft per gallon. How many gallons for one coat?", "1 gallon (102 sq ft)"),
                 ("A yard 55 ft by 90 ft is fenced at $5.50 per foot. Find the cost.", "$" + n(290 * 5.5, 2)),
                 ("In a trapezoid, which sides are the bases?", "the two parallel sides")])


# =====================================================================  11
def ch11():
    rg = random.Random(1111)
    sec("11.5 Which area formula?")
    p("There are three ways to find the area of a triangle. Which one to use depends only on what measurements you have.")
    table(["You know", "Use", "Formula"],
          [["a base and the height to that base", "base and height", "A = [[bh|2]]"], ["all three sides, no height", "Hero's Formula", "A = √(s(s − a)(s − b)(s − c))"],
           ["the side of an equilateral triangle", "the shortcut", "A = .433s²"], ["the two legs of a right triangle", "base and height (the legs)", "A = [[ab|2]]"]],
          widths=[40, 26, 34])
    p("When a triangle can be done two ways, both must agree. The next example proves it.")
    example("A triangle has sides 13 in, 14 in and 15 in. The height drawn to the 14-in side is 12 in. Find the area two ways.",
            [("A = [[bh|2]] = [[(14)(12)|2]] = [[168|2]] = 84", "Way 1: base 14 with its own height 12."),
             ("s = [[13 + 14 + 15|2]] = [[42|2]] = 21", "Way 2: Hero's Formula. Semi-perimeter first."),
             ("A = √(21(21 − 13)(21 − 14)(21 − 15))", "Substitute."), ("A = √(21(8)(7)(6)) = √7056", "Subtract, then multiply."), ("A = 84", "The same area.")],
            "84 sq in, both ways")
    warn("The height must belong to the base",
         "In A = bh ÷ 2 the height has to be the one drawn **to the side used as the base**. Using the 12-in height with the 13-in side gives a wrong answer. "
         "If the height you have does not match any base you have, use Hero's Formula.")

    sec("11.6 Finding a height with the Pythagorean theorem")
    p("The height of an isosceles or equilateral triangle splits it into two matching right triangles. The height is one leg, **half the base** is the "
      "other leg, and a slanted side is the hypotenuse. So the height can be calculated instead of measured.")
    example("An isosceles triangle has two sides of 13 ft and a base of 10 ft. Find its height and its area.",
            [("half the base = 10 ÷ 2 = 5", "The height lands in the middle of the base."), ("h = √(c² − b²) = √(13² − 5²)", "The 13-ft side is the hypotenuse; a leg is wanted, so subtract."),
             ("h = √(169 − 25) = √144 = 12", ""), ("A = [[bh|2]] = [[(10)(12)|2]] = 60", "Use the **whole** base for the area.")], "h = 12 ft;  A = 60 sq ft")
    example("Find the height of an equilateral triangle 10 in on a side, to the nearest hundredth. Then find the area with A = bh ÷ 2 and compare it with A = .433s².",
            [("h = √(10² − 5²) = √(100 − 25) = √75", "Half the base is 5; the side is the hypotenuse."), ("h = 8.660… → 8.66", "Round."),
             ("A = [[(10)(8.66)|2]] = 43.3", "Base and height."), ("A = .433(10)² = .433(100) = 43.3", "The shortcut."), ("43.3 = 43.3 ✓", "They agree.")],
            "h = 8.66 in;  A = 43.3 sq in")
    p("The same idea finds the slanted side of an isosceles trapezoid. The overhang on each side is half the difference of the bases, and the "
      "height and the overhang are the legs of a right triangle.")
    example("An isosceles trapezoid has bases 12 in and 20 in and a height of 9 in. Find the length of each slanted side to the nearest tenth, and the perimeter.",
            [("overhang = (20 − 12) ÷ 2 = 4", "The longer base sticks out equally on both sides."), ("c = √(a² + b²) = √(9² + 4²)", "The slanted side is the hypotenuse; add."),
             ("c = √(81 + 16) = √97 = 9.848…", ""), ("c = 9.8", "Round."), ("P = 12 + 20 + 9.8 + 9.8 = 51.6", "Now the perimeter can be found.")],
            "9.8 in;  P = 51.6 in", title="The slanted side of a trapezoid")

    sec("11.7 Right triangles on the job")
    p("Any time two measurements are square to each other, the straight-line distance between their far ends is a hypotenuse. "
      "Look for the right angle first; it tells you which side is c.")
    fig(figs.side_by_side([figs.right_tri_dims("6", "14", "?", "ft", "rafter: rise 6, run 14"), figs.right_tri_dims("?", "9", "15", "in", "offset: travel 15, run 9")], gap=10),
        "Left: the rafter is the hypotenuse. Right: the travel piece is the hypotenuse and a leg is missing.")
    example("A roof rises 6 ft over a horizontal run of 14 ft. How long is the rafter, to the nearest hundredth?",
            [("c = √(6² + 14²)", "Rise and run are square to each other. The rafter is the hypotenuse."), ("c = √(36 + 196) = √232", ""), ("c = 15.231… → 15.23", "")],
            "15.23 ft", title="Rafter")
    example("A pipe offset uses a travel piece 15 in long. The run of the offset is 9 in. How far does the pipe move sideways?",
            [("a = √(15² − 9²)", "The travel piece is the hypotenuse. A leg is wanted: subtract."), ("a = √(225 − 81) = √144", ""), ("a = 12", "")], "12 in", title="Pipe offset")
    example("A rectangular door frame is 36 in wide and 80 in high. What should its diagonal measure if the frame is square? Round to the nearest tenth.",
            [("c = √(36² + 80²)", "The diagonal of a rectangle is the hypotenuse of a right triangle whose legs are the sides."),
             ("c = √(1296 + 6400) = √7696", ""), ("c = 87.726… → 87.7", "")], "87.7 in", title="Diagonal of a rectangle")
    example("A triangle has sides 9 ft, 12 ft and 16 ft. Is it a right triangle?",
            [("9² + 12² = 81 + 144 = 225", "Square the two shorter sides and add."), ("16² = 256", "Square the longest side."),
             ("225 ≠ 256", "They are not equal, so the corner is not square.")], "No. (With a 15-ft third side it would be.)", title="Testing for a right angle")
    shop("Checking a layout",
         "To check that a foundation is square, measure both diagonals of the rectangle. They must be equal, and each must equal √(L² + W²). "
         "For a 24 ft by 32 ft foundation each diagonal is √(576 + 1024) = √1600 = 40 ft.")

    q = []
    trip = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
    for k in range(5):
        a, b, c = rg.choice(trip)
        m = rg.choice([1, 2, 3])
        q.append((f"Right triangle: legs {a * m} in and {b * m} in. Find c.", f"{c * m} in"))
    for k in range(5):
        a, b, c = rg.choice(trip)
        m = rg.choice([1, 2, 3])
        q.append((f"Right triangle: c = {c * m} ft, one leg {a * m} ft. Find the other leg.", f"{b * m} ft"))
    for k in range(5):
        a, b = rg.randint(3, 15), rg.randint(4, 20)
        q.append((f"Right triangle: legs {a} cm and {b} cm. Find c to the nearest tenth.", r(sqrt(a * a + b * b), 1) + " cm"))
    for k in range(5):
        c = rg.randint(12, 30)
        a = rg.randint(4, c - 3)
        q.append((f"Right triangle: c = {c} in, one leg {a} in. Find the other leg to the nearest tenth.", r(sqrt(c * c - a * a), 1) + " in"))
    practice("Pythagorean theorem", "Decide first whether you are finding the hypotenuse (add) or a leg (subtract).", q, cols=2)

    hq = []
    for a, b, c in [(5, 12, 13), (7, 15, 20), (9, 10, 17), (11, 13, 20), (6, 25, 29), (8, 9, 11), (12, 15, 21), (10, 10, 12), (16, 20, 24), (7, 7, 7)]:
        v = hero(a, b, c)
        exact = abs(v - round(v)) < 1e-9
        hq.append((f"Sides {a}, {b}, {c} m. Find A" + ("." if exact else " to the nearest tenth."), (n(round(v)) if exact else r(v, 1)) + " m²"))
    practice("Hero's Formula", "Find the semi-perimeter first, then the area.", hq, cols=2)

    ap = [("An isosceles triangle has sides 17 in, 17 in and a base of 16 in. Find its height.", "15 in"),
          ("Find the area of the triangle in problem 1.", "120 sq in"),
          ("An isosceles triangle has sides 10 ft, 10 ft and a base of 12 ft. Find its height and area.", "h = 8 ft; A = 48 sq ft"),
          ("Find the height of an equilateral triangle 6 in on a side, to the nearest hundredth.", r(sqrt(27), 2) + " in"),
          ("Find the area of the triangle in problem 4 with A = .433s².", n(0.433 * 36) + " sq in"),
          ("A roof rises 5 ft over a run of 12 ft. Find the rafter length.", "13 ft"),
          ("A roof rises 4 ft over a run of 13 ft. Find the rafter length to the nearest hundredth.", r(sqrt(185), 2) + " ft"),
          ("A 25-ft guy wire is anchored 7 ft from the base of a pole. How high on the pole is it attached?", "24 ft"),
          ("A pipe offset has a travel of 20 in and a run of 16 in. Find the offset.", "12 in"),
          ("A slab is 30 ft by 40 ft. What should each diagonal measure?", "50 ft"),
          ("A gate is 5 ft by 4 ft. How long is its diagonal brace, to the nearest hundredth?", r(sqrt(41), 2) + " ft"),
          ("Is a triangle with sides 15, 20 and 25 a right triangle? Show why.", "Yes: 225 + 400 = 625 = 25²."),
          ("Is a triangle with sides 8, 14 and 16 a right triangle? Show why.", "No: 64 + 196 = 260, but 16² = 256."),
          ("An isosceles trapezoid has bases 10 in and 22 in and height 8 in. Find each slanted side.", "10 in (overhang 6; √(64 + 36))"),
          ("Find the perimeter and area of the trapezoid in problem 14.", "P = 52 in; A = 128 sq in"),
          ("A triangular lot has sides 50 ft, 60 ft and 70 ft. Find its area to the nearest square foot.", r(hero(50, 60, 70), 0) + " sq ft")]
    practice("Triangles on the job", "Sketch the triangle and mark the right angle before you start.", ap, cols=1)

    more_review([("Triangle: sides 13, 14, 15 in; height to the 14-in side is 12 in. Find A.", "84 sq in"),
                 ("Isosceles triangle: sides 13, 13 and base 24 cm. Find the height.", "5 cm"),
                 ("Find the area of the triangle in the previous problem.", "60 cm²"),
                 ("Hero's Formula: sides 15, 15, 18 ft. Find A.", n(hero(15, 15, 18)) + " sq ft"),
                 ("Equilateral triangle: s = 20 in. Find A.", n(0.433 * 400) + " sq in"),
                 ("Right triangle: legs 15 in and 36 in. Find c.", "39 in"), ("Right triangle: c = 34 ft, leg 16 ft. Find the other leg.", "30 ft"),
                 ("A roof rises 7 ft over a run of 24 ft. Find the rafter length.", "25 ft"),
                 ("A 12 ft by 16 ft deck is square if its diagonal measures what?", "20 ft"),
                 ("Right triangle: legs 6 ft and 11 ft. Find A and c (nearest tenth).", f"A = 33 sq ft; c = {r(sqrt(157), 1)} ft"),
                 ("An isosceles trapezoid has bases 14 in and 30 in and height 6 in. Find each slanted side.", "10 in"),
                 ("Which formula finds the area of a triangle when only the three sides are known?", "Hero's Formula")])


# =====================================================================  12
def ch12():
    rg = random.Random(1212)
    sec("12.4 Circles on the job")
    p("Two ideas explain most circle problems in the trades. The **circumference** tells how far it is around a pipe, tank or wheel. "
      "The **area** tells how much can flow through an opening or how much material a round part contains.")
    example("A 10-in round duct is replaced by a 20-in round duct. How many times as much cross-sectional area does the larger duct have?",
            [("10-in duct: r = 5;  A = (3.14)(5)² = 78.5", "Radius is half of the diameter."), ("20-in duct: r = 10;  A = (3.14)(10)² = 314", ""),
             ("314 ÷ 78.5 = 4", "Compare by dividing.")], "4 times the area", title="Doubling the diameter")
    p("Doubling the diameter does not double the area. It multiplies it by **four**, because the radius is squared. Tripling the diameter multiplies the area by nine.")
    example("Insulation is to be wrapped once around a tank 6 ft in diameter. How long a piece is needed, allowing 3 in for overlap? Answer in feet.",
            [("C = πd = (3.14)(6) = 18.84 ft", "Once around is the circumference."), ("3 in = 0.25 ft", "Same unit before adding."), ("18.84 + 0.25 = 19.09", "")],
            "19.09 ft", title="Circumference")
    example("A service truck has tires 30 in in diameter. How many feet does it travel in 100 turns of the wheel?",
            [("C = (3.14)(30) = 94.2 in", "One turn rolls out one circumference."), ("94.2 × 100 = 9420 in", "100 turns."), ("9420 ÷ 12 = 785", "Inches to feet.")],
            "785 ft", title="A rolling wheel")
    example("A semicircular window is 5 ft across its flat side. Find its area and the length of trim needed to go all the way around it.",
            [("r = 5 ÷ 2 = 2.5", "The flat side is a diameter."), ("A = [[πr²|2]] = [[(3.14)(2.5)²|2]] = [[19.625|2]] = 9.8125", "Half of a full circle."),
             ("curved edge = [[πd|2]] = [[(3.14)(5)|2]] = 7.85", "Half the circumference."), ("trim = 7.85 + 5 = 12.85", "The curved edge **plus** the flat side.")],
            "A = 9.8125 sq ft;  trim = 12.85 ft", title="Half a circle")
    warn("A half circle still has a straight edge",
         "The perimeter of a semicircle is half the circumference **plus the diameter**. A quarter circle is a quarter of the circumference plus **two radii**.")

    sec("12.5 Hexagons on the job")
    p("Hex bar stock, bolt heads and nuts are specified by the distance **across the flats**, because that is what a wrench or a vise grips. "
      "The distance across the corners decides what size round bar a hexagon can be cut from.")
    example("A hexagonal nut must measure 0.75 in across the flats. (a) How long is each side, to the nearest thousandth? (b) What is the smallest round bar it can be cut from?",
            [("f = 1.732s  →  0.75 = 1.732s", "(a) Substitute into the across-flats formula."), ("s = 0.75 ÷ 1.732 = 0.4330…", "Divide."), ("s = 0.433", "Round."),
             ("d = 2s = 2(0.433) = 0.866", "(b) The corners must fit inside the round bar, so its diameter is the distance across corners.")],
            "(a) 0.433 in   (b) 0.866 in diameter")
    example("A hexagonal paving stone has sides of 8 in. Find its perimeter, its area, and how wide a row of stones is when they are laid flat side to flat side.",
            [("P = 6s = 6(8) = 48", ""), ("A = 2.6s² = 2.6(8)² = 2.6(64) = 166.4", ""), ("f = 1.732s = 1.732(8) = 13.856", "Flat to flat is the across-flats distance.")],
            "P = 48 in;  A = 166.4 sq in;  row width 13.856 in")

    sec("12.6 More composite figures")
    p("The plan never changes: separate, find the missing dimensions, calculate each area, then add or subtract. What takes practice is **seeing** the simple shapes. "
      "The trapezoid is the most useful of them, because it handles any figure with one pair of parallel sides and slanted or stepped ends.")
    fig(figs.side_by_side([figs.trap_on_rect(20, 8, 12, 5), figs.trap_hole(10, 18, 9, 4)], gap=10),
        "Left: a wall with a trapezoid on top of a rectangle. Right: a trapezoid plate with a round hole.")
    example("The end wall of a building (Figure 12.6, left) is a rectangle 20 ft wide and 8 ft high with a trapezoid on top. The trapezoid is 20 ft wide at the bottom, 12 ft wide at the top and 5 ft high. Find the total area.",
            [("Rectangle: (20)(8) = 160", "The lower part."), ("Trapezoid: [[(20 + 12)(5)|2]] = [[(32)(5)|2]] = 80", "Its bases are the 20-ft bottom and the 12-ft top."),
             ("160 + 80 = 240", "Joined parts are added.")], "240 sq ft", title="Rectangle plus trapezoid")
    example("A trapezoidal plate (Figure 12.6, right) has bases of 10 in and 18 in and a height of 9 in. A hole 4 in in diameter is drilled through it. Find the area of metal that remains.",
            [("Trapezoid: [[(10 + 18)(9)|2]] = [[(28)(9)|2]] = 126", "The whole plate."), ("Hole: r = 2;  (3.14)(2)² = 12.56", "Radius is half of the 4-in diameter."),
             ("126 − 12.56 = 113.44", "A hole is subtracted.")], "113.44 sq in", title="Trapezoid minus circle")
    fig(figs.composite_L_trap(30, 18, 12, 8), "A second L-shaped floor split into trapezoids A and B.")
    example("Find the area of the L-shaped floor in Figure 12.7 by splitting it into two trapezoids. Check by subtraction.",
            [("A: bases 18 ft and 8 ft, height 18 ft", "A’s parallel sides are vertical: the 18-ft left wall and the 8-ft step. They are 30 − 12 = 18 ft apart."),
             ("Area A = [[(18 + 8)(18)|2]] = [[(26)(18)|2]] = 234", ""),
             ("B: bases 12 ft and 30 ft, height 10 ft", "B’s parallel sides are horizontal: the 12-ft ledge and the 30-ft bottom. They are 18 − 8 = 10 ft apart."),
             ("Area B = [[(12 + 30)(10)|2]] = [[(42)(10)|2]] = 210", ""), ("234 + 210 = 444", "Add."),
             ("Check: (30)(18) − (12)(8) = 540 − 96 = 444 ✓", "Whole rectangle minus the missing corner.")], "444 sq ft", title="An L as two trapezoids")
    rule("Splitting an L into two trapezoids",
         "**1.** Draw one line from the inside corner to the outside corner farthest from it.",
         "**2.** One trapezoid has the two **vertical** edges as bases, and its height is measured across.",
         "**3.** The other has the two **horizontal** edges as bases, and its height is measured up and down.",
         "**4.** Find each area with A = (b_{1} + b_{2})h ÷ 2 and add.")
    sub("Perimeter of a composite figure")
    example("Find the perimeter of the L-shaped floor in Figure 12.7.",
            [("missing sides: 30 − 12 = 18 and 18 − 8 = 10", "Find the edges that are not labeled."), ("18 + 8 + 12 + 10 + 30 + 18 = 96", "Walk around the outside: top, step down, ledge, right side, bottom, left side.")],
            "96 ft")
    p("A shortcut for any L: its perimeter equals the perimeter of the full rectangle around it, 2(30) + 2(18) = 96 ft, because the two notch edges are the same length as the edges they replaced.")

    q = []
    for _ in range(5):
        d = rg.choice([4, 6, 8, 12, 14, 16, 20, 24, 30])
        q.append((f"Circle: d = {d} in. Find C and A.", f"C = {n(PI * d)} in; A = {n(PI * d * d / 4)} sq in"))
    for _ in range(4):
        r_ = rg.choice([1.5, 2.5, 3, 4.5, 7, 11, 15])
        q.append((f"Circle: r = {n(r_)} ft. Find C and A.", f"C = {n(2 * PI * r_)} ft; A = {n(PI * r_ * r_)} sq ft"))
    for d in [12, 35, 8.5]:
        q.append((f"Circle: C = {n(PI * d)} cm. Find d.", f"{n(d)} cm"))
    for r_ in [6, 20, 1.5]:
        q.append((f"Circle: A = {n(PI * r_ * r_)} sq in. Find r.", f"{n(r_)} in"))
    for A in [75, 150, 500]:
        q.append((f"Circle: A = {A} sq ft. Find r to the nearest hundredth.", r(sqrt(A / PI), 2) + " ft"))
    q += [("A semicircle has a diameter of 12 in. Find its area.", n(PI * 36 / 2) + " sq in"),
          ("Find the perimeter of the semicircle in the previous problem.", n(PI * 12 / 2 + 12) + " in")]
    practice("More circles", "Use π = 3.14. Do not round unless told to.", q, cols=2)

    hq = []
    for s_ in [3, 5, 1.25, 9, 0.5]:
        hq.append((f"Hexagon: s = {n(s_)} in. Find P, A, d and f.", f"P = {n(6 * s_)} in; A = {n(2.6 * s_ * s_)} sq in; d = {n(2 * s_)} in; f = {n(1.732 * s_)} in"))
    for A in [260, 1000]:
        hq.append((f"Hexagon: A = {A} sq cm. Find s to the nearest tenth.", r(sqrt(A / 2.6), 1) + " cm"))
    for f_ in [1, 2.5]:
        hq.append((f"Hexagon: f = {n(f_)} in across flats. Find s to the nearest thousandth.", r(f_ / 1.732, 3) + " in"))
    hq.append(("What is the smallest round bar from which a hexagon with 0.6-in sides can be cut?", "1.2 in diameter"))
    practice("More hexagons", "Use P = 6s, A = 2.6s², d = 2s and f = 1.732s.", hq, cols=1)

    fig(figs.side_by_side([figs.composite_L_plain(24, 16, 10, 6), figs.composite_L_plain(18, 12, 6, 4), figs.composite_L_plain(40, 30, 16, 12)], gap=4),
        "L-shaped figures for Practice 12.5, problems 1 to 3.")
    cq = [L_item(24, 16, 10, 6), L_item(18, 12, 6, 4), L_item(40, 30, 16, 12), L_item(15, 10, 5, 4, "in"), L_item(50, 36, 20, 16),
          ("Find the perimeter of the figure in problem 1.", "80 ft"), ("Find the perimeter of the figure in problem 3.", "140 ft"),
          ("A wall is a rectangle 24 ft wide and 9 ft high with a trapezoid on top that is 24 ft wide at the bottom, 10 ft wide at the top and 6 ft high. Find the total area.",
           n(216 + 34 * 6 / 2) + " sq ft"),
          ("A trapezoidal plate with bases 12 in and 20 in and height 10 in has a round hole 6 in in diameter. Find the remaining area.", n(160 - PI * 9) + " sq in"),
          ("A trapezoid with bases 8 ft and 14 ft and height 6 ft has a rectangle 14 ft by 5 ft attached to its longer base. Find the total area.", n(66 + 70) + " sq ft"),
          ("A rectangle 30 in by 16 in has a trapezoid cut from it whose bases are 10 in and 6 in and whose height is 5 in. Find the remaining area.", n(480 - 40) + " sq in"),
          ("A hopper side is made of a rectangle 40 in by 12 in above a trapezoid with bases 40 in and 10 in and height 24 in. Find the total area.", n(480 + 600) + " sq in"),
          ("A round table 5 ft in diameter has a square hole 1 ft on a side at its center. Find the area of the top.", n(PI * 6.25 - 1) + " sq ft"),
          ("A track is a rectangle 100 ft by 40 ft with a semicircle on each 40-ft end. Find its area.", n(4000 + PI * 400) + " sq ft"),
          ("Find the perimeter of the track in the previous problem.", n(200 + PI * 40) + " ft"),
          ("A gasket is a 6 in by 6 in square with a 4-in diameter hole. Find its area.", n(36 - PI * 4) + " sq in")]
    practice("Composite figures with trapezoids", "For problems 1 to 5, draw the cut from the inside corner to the far corner and show both trapezoid areas.", cq, cols=1)

    more_review([L_item(22, 14, 8, 5), L_item(36, 20, 12, 8),
                 ("A rectangle 18 ft by 7 ft has a trapezoid on top with bases 18 ft and 8 ft and height 4 ft. Find the total area.", n(126 + 52) + " sq ft"),
                 ("A trapezoidal plate with bases 14 in and 22 in and height 8 in has a 5-in diameter hole. Find the remaining area.", n(144 - PI * 6.25) + " sq in"),
                 ("A 16-in duct is replaced by an 8-in duct. What fraction of the original area remains?", "one fourth"),
                 ("A wheel 24 in in diameter makes 50 turns. How many feet does it roll?", n(PI * 24 * 50 / 12) + " ft"),
                 ("A semicircular window is 6 ft across. Find its area.", n(PI * 9 / 2) + " sq ft"),
                 ("Find the trim needed all the way around the window in the previous problem.", n(PI * 6 / 2 + 6) + " ft"),
                 ("A hexagon measures 2 in across the flats. Find s to the nearest thousandth.", r(2 / 1.732, 3) + " in"),
                 ("In an L split into two trapezoids, which edges are the bases of the trapezoid whose height is measured across?", "the two vertical edges")])


# =====================================================================  cumulative
def part4(extra=()):
    cumulative("Part 4 · Geometry", "Mixed problems from Chapters 10 to 13. Use π = 3.14. Round only where told to.",
               [("Rectangle 26 in by 15 in: find P and A.", "P = 82 in; A = 390 sq in"), ("Square with s = 12.5 ft: find P and A.", "P = 50 ft; A = 156.25 sq ft"),
                ("Parallelogram with b = 24 cm, a = 13 cm, h = 12 cm: find P and A.", "P = 74 cm; A = 288 cm²"),
                ("Trapezoid with bases 11 in and 19 in, height 8 in: find A.", "120 sq in"),
                ("Trapezoid with A = 200 sq ft and bases 18 ft and 22 ft: find h.", "10 ft"),
                ("Triangle with b = 22 in and h = 9 in: find A.", "99 sq in"), ("Hero's Formula, sides 8, 15, 17 ft: find A.", n(hero(8, 15, 17)) + " sq ft"),
                ("Equilateral triangle with s = 14 cm: find A.", n(0.433 * 196) + " cm²"), ("Right triangle with legs 20 in and 21 in: find c.", "29 in"),
                ("Right triangle with c = 41 ft and a leg of 9 ft: find the other leg.", "40 ft"),
                ("Circle with d = 16 in: find C and A.", f"C = {n(PI * 16)} in; A = {n(PI * 64)} sq in"), ("Circle with A = 113.04 sq ft: find r.", "6 ft"),
                ("Hexagon with s = 6 in: find P, A, d and f.", f"P = 36 in; A = {n(2.6 * 36)} sq in; d = 12 in; f = {n(1.732 * 6)} in"),
                L_item(28, 20, 10, 8),
                ("A ring has an outside diameter of 20 in and an inside diameter of 12 in. Find its area.", n(PI * 100 - PI * 36) + " sq in"),
                ("A 14 ft by 20 ft floor is covered with 4 ft by 8 ft sheets. With 10% waste, how many sheets?", "10 sheets (308 ÷ 32 = 9.6, round up)"),
                ("A roof rises 8 ft over a run of 15 ft. Find the rafter length.", "17 ft"),
                ("A window is a rectangle 3 ft by 5 ft with a trapezoid on top (bases 3 ft and 2 ft, height 1 ft). Find its area.", n(15 + 2.5) + " sq ft"),
                ("An isosceles triangle has sides 25, 25 and a base of 14 in. Find its height and area.", "h = 24 in; A = 168 sq in"),
                ("A tank is 31.4 ft around. Find its diameter.", "10 ft")] + list(extra), cols=1)
