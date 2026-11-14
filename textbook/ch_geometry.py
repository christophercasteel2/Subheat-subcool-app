"""Part 4: geometry of flat shapes."""
from math import sqrt
from book import *  # noqa: F401,F403
from util import n, r, rnd
import figs

PI = 3.14

part("Part 4 · Geometry", "How much trim goes around it? How much material covers it? Part 4 answers those two questions, "
     "perimeter and area, for every flat shape met in the trades.")

# =====================================================================  10
chapter("Perimeter and Area of Quadrilaterals",
        ["Tell perimeter from area and use the correct unit for each.",
         "Find the perimeter and area of rectangles and squares.",
         "Find the perimeter and area of parallelograms and trapezoids.",
         "Identify the height of a figure and tell it from a slanted side.",
         "Work backward from an area or perimeter to a missing dimension."],
        "Baseboard is bought by the foot and flooring by the square foot, for the same room. One measures the distance around; "
        "the other measures the surface inside. Mixing them up is the costliest mistake in estimating.",
        [("perimeter", "The distance around a flat figure. Measured in length units: in, ft, m."),
         ("area", "The amount of surface inside a flat figure. Measured in square units: sq in, sq ft, m²."),
         ("quadrilateral", "A figure with four straight sides."),
         ("parallel", "Lines that run the same direction and never meet."),
         ("base", "The side a figure is thought of as resting on."),
         ("height", "The distance straight up from the base, measured at a right angle to it. Also called altitude.")])

sec("10.1 Perimeter and area")
p("**Perimeter** is a length: walk around the edge of the figure and measure how far you went. **Area** is a count of squares: "
  "how many 1-by-1 squares it takes to cover the figure.")
table(["", "Perimeter", "Area"],
      [["Measures", "distance around the edge", "surface inside the edge"], ["Units", "in, ft, yd, m, cm", "sq in, sq ft, sq yd, m², cm²"],
       ["Found by", "**adding** the sides", "**multiplying** two dimensions"], ["Used for", "trim, fence, gasket, weld length", "paint, flooring, sheet metal, insulation"]],
      widths=[16, 40, 44])
rule("The perimeter of any straight-sided figure", "Add the lengths of all its sides.",
     "The special perimeter formulas are only shortcuts for this.")
warn("Units tell you which one you have",
     "If two lengths in feet are multiplied, the answer is in **square feet**. If they are added, the answer is in **feet**. "
     "An area given in plain feet, or a perimeter given in square feet, is wrong before the number is even checked.")
p("All dimensions must be in the **same unit** before they are added or multiplied. A panel 4 ft by 18 in is 4 ft by 1.5 ft, or 48 in by 18 in.")

sec("10.2 Rectangles and squares")
p("A **rectangle** has four right angles. Its opposite sides are equal, so it has two lengths and two widths. "
  "A **square** is a rectangle with all four sides equal.")
fig(figs.side_by_side([figs.rectangle(), figs.rectangle("s", "s", 120, 120)], gap=50), "A rectangle with length L and width W, and a square with side s.")
rule("Rectangle", "Perimeter:  P = 2L + 2W", "Area:  A = LW")
rule("Square", "Perimeter:  P = 4s", "Area:  A = s²")
example("A rectangular return-air grille opening is 30 in long and 14 in wide. Find its perimeter and its area.",
        [("P = 2L + 2W", "Perimeter formula."), ("P = 2(30) + 2(14)", "Substitute."), ("P = 60 + 28 = 88", "Multiply, then add."),
         ("A = LW", "Area formula."), ("A = (30)(14) = 420", "Substitute and multiply.")], "P = 88 in;  A = 420 sq in")
example("A square concrete pad is 7.5 ft on a side. Find its perimeter and area.",
        [("P = 4s = 4(7.5) = 30", "Four equal sides."), ("A = s² = (7.5)² = 56.25", "7.5 × 7.5. Do not round unless told to.")], "P = 30 ft;  A = 56.25 sq ft")
sub("Working backward")
p("If the area or perimeter is known and one dimension is missing, substitute what is known and solve, exactly as in Chapter 9.")
example("A rectangular duct must have a cross-section of 216 sq in. It can be only 9 in deep. How wide must it be?",
        [("A = LW", "Formula."), ("216 = L(9)", "Substitute."), ("L = 216 ÷ 9 = 24", "Divide both sides by 9.")], "24 in wide")
example("A square room has an area of 196 sq ft. How long is each wall?",
        [("A = s²", "Formula."), ("196 = s²", "Substitute."), ("s = √196 = 14", "The inverse of squaring is the square root. Take the root of both sides.")], "14 ft")

sec("10.3 Parallelograms")
p("A **parallelogram** has two pairs of parallel sides. It looks like a rectangle pushed over. Its sides are a base *b* and a slanted side *a*.")
fig(figs.parallelogram(), "A parallelogram. The height h is perpendicular to the base; the side a is slanted.")
rule("Parallelogram", "Perimeter:  P = 2a + 2b", "Area:  A = bh")
p("Why base times **height** and not base times side? Cut the triangle off one end of a parallelogram and slide it to the other end. "
  "The result is a rectangle with the same base and the same height. The slanted side does not appear in the area at all.")
warn("Height is never the slanted side",
     "The height is the straight-up distance between the two parallel sides. It is usually drawn as a dashed line with a small square where it "
     "meets the base. Use the slanted side for **perimeter** and the height for **area**.")
example("A parallelogram has a base of 18 in, a slanted side of 10 in and a height of 8 in. Find its perimeter and area.",
        [("P = 2a + 2b = 2(10) + 2(18)", "The perimeter uses the two side lengths."), ("P = 20 + 36 = 56", ""),
         ("A = bh = (18)(8) = 144", "The area uses the base and the height. The 10 is not used.")], "P = 56 in;  A = 144 sq in")

sec("10.4 Trapezoids")
p("A **trapezoid** has exactly one pair of parallel sides. Those two sides are its bases, b_{1} and b_{2}. They are different lengths. "
  "The height is the perpendicular distance between them.")
fig(figs.trapezoid(), "A trapezoid with bases b₁ and b₂, height h and slanted sides c and d.")
rule("Trapezoid", "Perimeter:  P = b_{1} + b_{2} + c + d   (the sum of the four sides)", "Area:  A = [[(b_{1} + b_{2})h|2]]")
p("The area formula says: average the two bases, then multiply by the height. Two identical trapezoids, one flipped, fit together into a "
  "parallelogram whose base is b_{1} + b_{2}. One trapezoid is half of that.")
example("A trapezoidal transition panel has parallel sides of 12 in and 20 in, a height of 9 in, and slanted sides of 9.8 in each. Find the perimeter and the area.",
        [("P = 12 + 20 + 9.8 + 9.8 = 51.6", "Add all four sides."), ("A = [[(b_{1} + b_{2})h|2]]", "Area formula."),
         ("A = [[(12 + 20)(9)|2]]", "Substitute."), ("A = [[(32)(9)|2]] = [[288|2]]", "Parentheses first, then multiply across the top."), ("A = 144", "Divide by 2.")],
        "P = 51.6 in;  A = 144 sq in")
warn("Add the bases before multiplying",
     "(12 + 20)(9) is 32 × 9 = 288. Typing 12 + 20 × 9 gives 192, because the calculator multiplies first. Keep the parentheses.")
example("A trapezoid has an area of 150 sq ft. Its bases are 10 ft and 15 ft. Find its height.",
        [("150 = [[(10 + 15)h|2]]", "Substitute."), ("150 = [[25h|2]]", "Simplify."), ("300 = 25h", "Multiply both sides by 2 to clear the fraction."),
         ("h = 12", "Divide both sides by 25.")], "12 ft", title="Working backward")
shop("Estimating materials",
     "Area tells how much to buy; unit price tells what it costs. A 12 ft by 15 ft room is 180 sq ft, or 180 ÷ 9 = 20 sq yd. "
     "Carpet at $32 per square yard costs 20 × 32 = $640. Convert the area to the unit the material is sold in before pricing.")

q = [("Rectangle: L = 16 ft, W = 9 ft. Find P and A.", f"P = {n(50)} ft; A = {n(144)} sq ft"),
     ("Rectangle: L = 8.5 in, W = 11 in. Find P and A.", f"P = {n(39)} in; A = {n(93.5)} sq in"),
     ("Square: s = 13 cm. Find P and A.", f"P = {n(52)} cm; A = {n(169)} cm²"),
     ("Square: s = 2.4 m. Find P and A.", f"P = {n(9.6)} m; A = {n(5.76)} m²"),
     ("Parallelogram: b = 22 in, a = 9 in, h = 7 in. Find P and A.", f"P = {n(62)} in; A = {n(154)} sq in"),
     ("Parallelogram: b = 6.5 ft, a = 4 ft, h = 3.2 ft. Find P and A.", f"P = {n(21)} ft; A = {n(20.8)} sq ft"),
     ("Trapezoid: b₁ = 8 in, b₂ = 14 in, h = 6 in, slanted sides 6.7 in each. Find P and A.", f"P = {n(35.4)} in; A = {n(66)} sq in"),
     ("Trapezoid: b₁ = 5 m, b₂ = 9 m, h = 4.5 m. Find A.", f"A = {n(31.5)} m²"),
     ("Trapezoid: b₁ = 3.5 ft, b₂ = 6 ft, h = 2 ft. Find A.", f"A = {n(9.5)} sq ft"),
     ("A rectangle has A = 322 sq in and W = 14 in. Find L.", n(23) + " in"),
     ("A rectangle has P = 76 ft and L = 23 ft. Find W.", n(15) + " ft"),
     ("A square has A = 529 sq cm. Find s.", n(23) + " cm"),
     ("A square has P = 58 in. Find s and A.", f"s = {n(14.5)} in; A = {n(210.25)} sq in"),
     ("A parallelogram has A = 195 sq in and b = 15 in. Find h.", n(13) + " in"),
     ("A trapezoid has A = 84 sq ft, b₁ = 9 ft and b₂ = 12 ft. Find h.", n(8) + " ft"),
     ("A room is 14 ft by 18 ft. How many square yards of carpet does it need?", n(28) + " sq yd"),
     ("A wall 24 ft long and 8 ft high has a door opening 3 ft by 7 ft. How many square feet are to be painted?", n(171) + " sq ft"),
     ("How many feet of baseboard go around a 12 ft by 15.5 ft room, ignoring doors?", n(55) + " ft")]
practice("Quadrilaterals", "Show the formula and the substitution. Do not round.", q, cols=1)

summary(["Perimeter is the distance around (add; length units). Area is the surface inside (multiply; square units).",
         "Rectangle: P = 2L + 2W, A = LW. Square: P = 4s, A = s².",
         "Parallelogram: P = 2a + 2b, A = bh. Trapezoid: P = sum of the sides, A = (b₁ + b₂)h ÷ 2.",
         "The height is perpendicular to the base and is never a slanted side.",
         "To find a missing dimension, substitute what is known and solve."])
review([("Would you use perimeter or area to order (a) weather-stripping, (b) roofing felt?", "(a) perimeter  (b) area"),
        ("Rectangle: L = 27 in, W = 16 in. Find P.", n(86) + " in"), ("Rectangle: L = 27 in, W = 16 in. Find A.", n(432) + " sq in"),
        ("Square: s = 9.5 ft. Find P.", n(38) + " ft"), ("Square: s = 9.5 ft. Find A.", n(90.25) + " sq ft"),
        ("Parallelogram: b = 30 cm, a = 12 cm, h = 10 cm. Find P.", n(84) + " cm"), ("Parallelogram: b = 30 cm, a = 12 cm, h = 10 cm. Find A.", n(300) + " cm²"),
        ("Trapezoid: bases 16 in and 24 in, height 11 in. Find A.", n(220) + " sq in"),
        ("Trapezoid: sides 16 in, 24 in, 11.7 in and 11.7 in. Find P.", n(63.4) + " in"),
        ("A rectangle has A = 247 sq ft and L = 19 ft. Find W.", n(13) + " ft"), ("A square has A = 2.25 sq m. Find s.", n(1.5) + " m"),
        ("A rectangle has P = 130 in and W = 22 in. Find L.", n(43) + " in"),
        ("A trapezoid has A = 135 sq in and bases 12 in and 18 in. Find h.", n(9) + " in"),
        ("A rectangular sheet is 4 ft by 30 in. Find its area in square feet.", n(10) + " sq ft"),
        ("A 20 ft by 24 ft floor is tiled at $4.50 per square foot. Find the cost.", "$" + n(2160)),
        ("Why does the slanted side of a parallelogram not appear in its area formula?",
         "Sliding the end triangle across turns it into a rectangle with the same base and height; only the perpendicular height matters.")])

# =====================================================================  11
chapter("Triangles",
        ["Classify a triangle as scalene, isosceles, equilateral or right.",
         "Find the perimeter of any triangle and its area from base and height.",
         "Find the area of a triangle from its three sides with Hero’s formula.",
         "Use the shortcut area formula for an equilateral triangle.",
         "Use the Pythagorean theorem to find a missing side of a right triangle."],
        "Roof trusses, gussets, braces and offsets are all triangles. The triangle is the one shape that cannot be pushed out of square, "
        "which is why it holds up so much of what is built.",
        [("scalene", "A triangle with no equal sides."), ("isosceles", "A triangle with two equal sides (and two equal angles)."),
         ("equilateral", "A triangle with three equal sides. Every angle is 60°."),
         ("right triangle", "A triangle with one 90° angle."), ("hypotenuse", "The longest side of a right triangle, opposite the right angle."),
         ("leg", "Either of the two sides that form the right angle."), ("semi-perimeter", "Half the perimeter.")])

sec("11.1 Kinds of triangles")
p("Triangles are named by their sides. The angles of any triangle add up to 180°.")
fig(figs.side_by_side([figs.triangle("scalene", fs=22), figs.triangle("isosceles", fs=22), figs.triangle("equilateral", fs=22)], gap=6),
    "Scalene (no sides equal), isosceles (two sides equal), equilateral (all sides equal). The dashed line is the height.")
rule("Any triangle", "Perimeter:  P = a + b + c", "Area:  A = [[bh|2]]",
     "where *b* is the base and *h* is the height measured at a right angle to that base.")
p("A triangle is half of a parallelogram with the same base and height. That is where the “divide by 2” comes from.")
example("A triangular gusset has a base of 16 in and a height of 9 in. Its other two sides are 15 in and 9.85 in. Find its area and perimeter.",
        [("A = [[bh|2]] = [[(16)(9)|2]]", "Substitute base and height."), ("A = [[144|2]] = 72", "Multiply, then halve."),
         ("P = 16 + 15 + 9.85 = 40.85", "Perimeter is the sum of the three sides. The height is not a side.")], "A = 72 sq in;  P = 40.85 in")
warn("Do not forget the 2", "The most common triangle error is stopping at base × height. That is the area of the whole parallelogram, twice the triangle.")

sec("11.2 Hero’s formula: area from three sides")
p("On a job the three sides of a triangle can be measured with a tape, but the height usually cannot. **Hero’s formula** "
  "(also written Heron’s) gives the area from the sides alone. It works for every triangle.")
rule("Hero’s formula", "First find the semi-perimeter:  s = [[a + b + c|2]]", "Then:  A = √(s(s − a)(s − b)(s − c))")
example("Find the area of a triangle with sides 15 m, 20 m and 25 m. Round to the nearest tenth if needed.",
        [("s = [[15 + 20 + 25|2]] = [[60|2]] = 30", "Semi-perimeter: add the sides and halve."),
         ("A = √(30(30 − 15)(30 − 20)(30 − 25))", "Substitute s and each side."), ("A = √(30(15)(10)(5))", "Do the three subtractions."),
         ("A = √22,500", "Multiply the four numbers."), ("A = 150", "Take the square root.")], "150 m²")
example("A triangular lot has sides of 70 ft, 90 ft and 110 ft. Find its area to the nearest square foot.",
        [("s = [[70 + 90 + 110|2]] = 135", "Semi-perimeter."), ("A = √(135(65)(45)(25))", "135 − 70 = 65, 135 − 90 = 45, 135 − 110 = 25."),
         ("A = √9,871,875", "Multiply."), ("A = 3141.9…", "Square root."), ("A = 3142", "Round.")], "3142 sq ft")
tip("Keying Hero’s formula",
    "Find s first and write it down. Then enter `√( s × (s − a) × (s − b) × (s − c) )` with the outer parentheses, so the root covers the whole product. "
    "A negative number under the root means a subtraction was entered backward or the three sides cannot form a triangle.")

sec("11.3 The equilateral triangle")
p("Because all three sides of an equilateral triangle are the same length *s*, its area depends on that one number.")
rule("Equilateral triangle", "Perimeter:  P = 3s", "Area:  A = 0.433s²")
example("Find the area of an equilateral triangle 8 in on a side.",
        [("A = 0.433s²", "Formula."), ("A = 0.433(8)²", "Substitute."), ("A = 0.433(64)", "Exponent first."), ("A = 27.712", "Multiply.")], "27.712 sq in")
p("The 0.433 is a rounded constant (it is √3 ÷ 4), so this shortcut and Hero’s formula agree to about three digits. Here *s* means the "
  "side. In Hero’s formula *s* means the semi-perimeter. Check which formula you are in.")

sec("11.4 Right triangles and the Pythagorean theorem")
p("A **right triangle** has one square corner. The two sides that form the corner are the **legs**, *a* and *b*. The side across "
  "from the right angle is the **hypotenuse**, *c*, and it is always the longest side.")
fig(figs.triangle("right"), "A right triangle. The legs a and b form the right angle; the hypotenuse c is opposite it.", width="3.2in")
fig(figs.pythag(), "The squares built on the two legs of a 3-4-5 triangle together equal the square built on the hypotenuse.")
rule("The Pythagorean theorem", "a² + b² = c²",
     "To find the hypotenuse:  c = √(a² + b²)", "To find a leg:  a = √(c² − b²)", "It is true **only** for right triangles.")
example("A ladder’s foot is 5 ft from a wall and its top touches the wall 12 ft up. How long is the ladder?",
        [("c = √(a² + b²)", "The ladder is the hypotenuse."), ("c = √(5² + 12²)", "Substitute the legs."), ("c = √(25 + 144) = √169", "Square, then add."),
         ("c = 13", "Square root.")], "13 ft")
example("A 20-ft brace is fastened to a post at a point 16 ft above the ground. How far from the foot of the post does the brace meet the ground?",
        [("a = √(c² − b²)", "The brace is the hypotenuse; a leg is missing."), ("a = √(20² − 16²)", "Substitute. The hypotenuse goes first."),
         ("a = √(400 − 256) = √144", "Square, then **subtract**."), ("a = 12", "Square root.")], "12 ft", title="Finding a leg")
warn("Add for the hypotenuse, subtract for a leg",
     "The hypotenuse is the longest side, so finding it means adding the squares. A leg is shorter than the hypotenuse, so finding it means subtracting. "
     "If a “leg” comes out longer than the hypotenuse, the wrong operation was used.",
     "And √(a² + b²) is **not** a + b. The squares must be added before the root is taken.")
p("In a right triangle the legs are perpendicular, so one leg is the base and the other is the height: A = [[ab|2]].")
shop("Squaring a corner with 3-4-5",
     "Builders check a corner by measuring 3 ft along one wall and 4 ft along the other. If the diagonal between the marks is exactly 5 ft, the corner is square, "
     "because 3² + 4² = 5². Any multiple works: 6-8-10, 9-12-15, 12-16-20.")


def hero(a, b, c):
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


q = [("Triangle: b = 14 in, h = 9 in. Find A.", n(63) + " sq in"), ("Triangle: b = 7.5 ft, h = 4 ft. Find A.", n(15) + " sq ft"),
     ("Triangle with sides 9 cm, 12 cm and 17 cm. Find P.", n(38) + " cm"),
     ("Hero’s formula: sides 6, 8, 10 in. Find A.", n(hero(6, 8, 10)) + " sq in"),
     ("Hero’s formula: sides 13, 14, 15 ft. Find A.", n(hero(13, 14, 15)) + " sq ft"),
     ("Hero’s formula: sides 7, 10, 12 m. Find A to the nearest tenth.", r(hero(7, 10, 12), 1) + " m²"),
     ("Hero’s formula: sides 20, 30, 40 ft. Find A to the nearest tenth.", r(hero(20, 30, 40), 1) + " sq ft"),
     ("Equilateral triangle: s = 10 in. Find P and A.", f"P = 30 in; A = {n(43.3)} sq in"),
     ("Equilateral triangle: s = 6.5 cm. Find A to the nearest tenth.", r(0.433 * 6.5 ** 2, 1) + " cm²"),
     ("Right triangle: legs 9 in and 12 in. Find c.", n(15) + " in"), ("Right triangle: legs 8 ft and 15 ft. Find c.", n(17) + " ft"),
     ("Right triangle: legs 7 m and 9 m. Find c to the nearest tenth.", r(sqrt(130), 1) + " m"),
     ("Right triangle: c = 25 in, one leg 7 in. Find the other leg.", n(24) + " in"),
     ("Right triangle: c = 30 ft, one leg 18 ft. Find the other leg.", n(24) + " ft"),
     ("Right triangle: c = 14 cm, one leg 9 cm. Find the other leg to the nearest tenth.", r(sqrt(196 - 81), 1) + " cm"),
     ("Right triangle: legs 10 in and 24 in. Find A and P.", f"A = {n(120)} sq in; P = {n(60)} in"),
     ("A rafter rises 6 ft over a horizontal run of 14 ft. Find the rafter length to the nearest tenth.", r(sqrt(36 + 196), 1) + " ft"),
     ("A rectangular gate is 4 ft by 7 ft. How long is its diagonal brace, to the nearest hundredth?", r(sqrt(65), 2) + " ft")]
practice("Triangles", "Show the formula and the substitution. Round only where the problem says.", q, cols=1)

summary(["Any triangle: P = a + b + c and A = bh ÷ 2, with h perpendicular to b.",
         "Hero’s formula finds area from the three sides: s = (a + b + c) ÷ 2, A = √(s(s − a)(s − b)(s − c)).",
         "Equilateral triangle: P = 3s, A = 0.433s².",
         "Right triangle: a² + b² = c². Add the squares to find the hypotenuse; subtract to find a leg.",
         "The hypotenuse is always the longest side."])
review([("A triangle has sides 5, 5 and 8 in. What kind of triangle is it?", "isosceles"),
        ("Each angle of an equilateral triangle measures how many degrees?", "60°"),
        ("Triangle: b = 18 ft, h = 11 ft. Find A.", n(99) + " sq ft"), ("Triangle with sides 14, 17 and 21 in. Find P.", n(52) + " in"),
        ("Hero’s formula: sides 9, 12, 15 m. Find A.", n(hero(9, 12, 15)) + " m²"),
        ("Hero’s formula: sides 10, 17, 21 cm. Find A.", n(hero(10, 17, 21)) + " cm²"),
        ("Hero’s formula: sides 8, 11, 13 ft. Find A to the nearest tenth.", r(hero(8, 11, 13), 1) + " sq ft"),
        ("Equilateral triangle: s = 12 in. Find A.", n(0.433 * 144) + " sq in"), ("Equilateral triangle: s = 4.2 m. Find P.", n(12.6) + " m"),
        ("Right triangle: legs 12 ft and 16 ft. Find c.", n(20) + " ft"), ("Right triangle: legs 5 in and 9 in. Find c to the nearest hundredth.", r(sqrt(106), 2) + " in"),
        ("Right triangle: c = 26 cm, leg 10 cm. Find the other leg.", n(24) + " cm"),
        ("Right triangle: c = 12 ft, leg 7 ft. Find the other leg to the nearest tenth.", r(sqrt(95), 1) + " ft"),
        ("A 16-ft ladder leans against a wall with its foot 4 ft from the wall. How high does it reach, to the nearest tenth?", r(sqrt(256 - 16), 1) + " ft"),
        ("Is a triangle with sides 10, 24 and 26 a right triangle? Show why.", "Yes: 10² + 24² = 100 + 576 = 676 = 26²."),
        ("A triangle has area 54 sq in and base 12 in. Find its height.", n(9) + " in")])

# =====================================================================  12
chapter("Circles, Hexagons and Composite Figures",
        ["Name the parts of a circle and convert between radius and diameter.",
         "Find the circumference and area of a circle using π = 3.14.",
         "Work backward from circumference or area to the radius or diameter.",
         "Find the perimeter, area and across-corner and across-flat distances of a regular hexagon.",
         "Find the area of a composite figure by adding or subtracting simple shapes."],
        "Pipe, duct, shafting, tanks and bolt heads: round and six-sided shapes are everywhere in mechanical work. "
        "And real parts are seldom one simple shape. The last skill in the book is taking a complicated figure apart into shapes you already know.",
        [("radius", "The distance from the centre of a circle to its edge."), ("diameter", "The distance across a circle through its centre: two radii."),
         ("circumference", "The distance around a circle; its perimeter."), ("π (pi)", "The circumference of any circle divided by its diameter; about 3.14."),
         ("regular hexagon", "A six-sided figure with all sides equal and all angles 120°."),
         ("composite figure", "A figure made of two or more simple shapes.")])

sec("12.1 The circle")
fig(figs.circle(), "The radius r, the diameter d and the circumference C of a circle.")
p("Measure around any circle, divide by the distance across, and the answer is always the same number, a little more than 3. "
  "That number is called **π** (pi). Its decimal never ends; this course uses **3.14**.")
rule("Circle", "d = 2r     and     r = [[d|2]]", "Circumference:  C = πd   or   C = 2πr", "Area:  A = πr²", "Use π = 3.14.")
example("A round duct has a diameter of 14 in. Find its circumference and its cross-sectional area.",
        [("C = πd = (3.14)(14) = 43.96", "The circumference formula takes the diameter directly."),
         ("r = [[d|2]] = [[14|2]] = 7", "The area formula needs the **radius**. Halve the diameter first."),
         ("A = πr² = (3.14)(7)²", "Substitute."), ("A = (3.14)(49) = 153.86", "Square the radius first, then multiply by π.")],
        "C = 43.96 in;  A = 153.86 sq in")
warn("Three circle mistakes",
     "**Using the diameter in A = πr².** Halve it first. Using d makes the area four times too large.",
     "**Doubling instead of squaring.** r² is r × r. For r = 7, r² is 49, not 14.",
     "**Squaring π.** In πr² only the r is squared: 3.14 × 49, not (3.14 × 7)².")
sub("Working backward")
example("A tank measures 157 in around. What is its diameter?",
        [("C = πd", "Formula."), ("157 = 3.14d", "Substitute."), ("d = 157 ÷ 3.14 = 50", "Divide both sides by 3.14.")], "50 in")
example("A circular opening must have an area of 200 sq in. Find the radius to the nearest tenth.",
        [("A = πr²", "Formula."), ("200 = 3.14r²", "Substitute."), ("r² = 200 ÷ 3.14 = 63.694…", "Divide both sides by 3.14."),
         ("r = √63.694… = 7.98…", "Take the square root of both sides."), ("r = 8.0", "Round to the nearest tenth.")], "8.0 in")
tip("The π key",
    "The calculator’s `π` key uses 3.14159265…, which gives slightly different answers from 3.14 (153.94 instead of 153.86 above). "
    "When the course says to use 3.14, type 3.14.")

sec("12.2 The regular hexagon")
p("A **regular hexagon** has six equal sides and six equal 120° angles. Bolt heads and nuts are hexagons. It can be measured two ways: "
  "**across the corners** (the distance *d* from one point to the opposite point) and **across the flats** (the distance *f* between opposite sides, "
  "which is the wrench size).")
fig(figs.hexagon(), "A regular hexagon with side s, distance across corners d and distance across flats f.")
rule("Regular hexagon", "Perimeter:  P = 6s", "Area:  A = 2.6s²", "Across corners:  d = 2s", "Across flats:  f = 1.732s")
example("A hexagonal bar has sides of 0.75 in. Find its perimeter, area, distance across corners and distance across flats.",
        [("P = 6s = 6(0.75) = 4.5", "Six equal sides."), ("A = 2.6s² = 2.6(0.75)² = 2.6(0.5625) = 1.4625", "Square the side first."),
         ("d = 2s = 2(0.75) = 1.5", "Across corners."), ("f = 1.732s = 1.732(0.75) = 1.299", "Across flats.")],
        "P = 4.5 in;  A = 1.4625 sq in;  d = 1.5 in;  f = 1.299 in")
example("A hexagonal patio is to cover 500 sq m. How long is each side, to the nearest tenth?",
        [("A = 2.6s²", "Formula."), ("500 = 2.6s²", "Substitute."), ("s² = 500 ÷ 2.6 = 192.307…", "Divide both sides by 2.6."),
         ("s = √192.307… = 13.867…", "Square root of both sides."), ("s = 13.9", "Round.")], "13.9 m", title="Working backward")
example("A nut measures 1.5 in across the flats. How long is each side, to the nearest hundredth?",
        [("f = 1.732s", "Formula."), ("1.5 = 1.732s", "Substitute."), ("s = 1.5 ÷ 1.732 = 0.866…", "Divide."), ("s = 0.87", "Round.")], "0.87 in")

cq = [("Circle: d = 10 in. Find C.", n(31.4) + " in"), ("Circle: r = 6 ft. Find C.", n(2 * PI * 6) + " ft"), ("Circle: r = 5 cm. Find A.", n(78.5) + " cm²"),
      ("Circle: d = 18 in. Find A.", n(PI * 81) + " sq in"), ("Circle: d = 3.5 m. Find C and A.", f"C = {n(PI * 3.5)} m; A = {n(PI * 1.75 ** 2)} m²"),
      ("Circle: C = 94.2 in. Find d.", n(30) + " in"), ("Circle: C = 50 ft. Find r to the nearest hundredth.", r(50 / PI / 2, 2) + " ft"),
      ("Circle: A = 314 sq in. Find r.", n(10) + " in"), ("Circle: A = 120 sq ft. Find d to the nearest tenth.", r(2 * sqrt(120 / PI), 1) + " ft"),
      ("Hexagon: s = 4 in. Find P and A.", f"P = 24 in; A = {n(41.6)} sq in"), ("Hexagon: s = 2.5 cm. Find d and f.", f"d = 5 cm; f = {n(4.33)} cm"),
      ("Hexagon: s = 12 ft. Find A.", n(2.6 * 144) + " sq ft"), ("Hexagon: A = 650 sq in. Find s to the nearest tenth.", r(sqrt(650 / 2.6), 1) + " in"),
      ("Hexagon: d = 3 in across corners. Find s and f.", f"s = 1.5 in; f = {n(2.598)} in"),
      ("Hexagon: f = 2 in across flats. Find s to the nearest hundredth.", r(2 / 1.732, 2) + " in"),
      ("How far does a 26-in diameter wheel roll in one turn?", n(PI * 26) + " in")]
practice("Circles and hexagons", "Use π = 3.14. Do not round unless told to.", cq, cols=2)

sec("12.3 Composite figures")
p("A **composite figure** is built from two or more simple shapes. No new formula is needed, only a plan.")
rule("Area of a composite figure",
     "**1. Separate** the figure into shapes you know: rectangles, triangles, circles, trapezoids.",
     "**2. Find** any dimension that is not given, by adding or subtracting the ones that are.",
     "**3. Calculate** the area of each shape.",
     "**4. Add** the areas of shapes that are joined. **Subtract** the areas of holes and cut-outs.")
sub("Adding parts")
fig(figs.side_by_side([figs.composite_L(20, 14, 8, 6), figs.composite_house(16, 10, 6)], gap=30),
    "Left: an L-shaped floor split into rectangles A and B. Right: a gable wall, a rectangle with a triangle on top.")
example("Find the area of the L-shaped floor in Figure 12.3.",
        [("A: 12 ft by 6 ft;  B: 20 ft by 8 ft", "Split along the dashed line. Rectangle A is 12 ft wide. Its height is 14 − 8 = 6 ft."),
         ("Area A = (12)(6) = 72", ""), ("Area B = (20)(8) = 160", ""), ("72 + 160 = 232", "The parts are joined, so add.")], "232 sq ft")
p("The same floor can be done by subtraction: a full 20 by 14 rectangle is 280 sq ft, and the missing corner is 8 by 6 = 48 sq ft. "
  "280 − 48 = 232 sq ft. Either plan must give the same answer, which makes a good check.")
example("Find the area of the gable wall in Figure 12.3.",
        [("Rectangle: (16)(10) = 160", "The lower part."), ("Triangle: [[(16)(6)|2]] = 48", "The triangle’s base is the width of the wall, 16 ft; its height is 6 ft."),
         ("160 + 48 = 208", "Add.")], "208 sq ft")
sub("Subtracting holes")
fig(figs.side_by_side([figs.composite_frame(30, 20, 18, 10), figs.composite_ring(8, 5)], gap=30),
    "Left: a plate with a rectangular opening. Right: a ring (a circle with a circular hole).")
example("A 30 in by 20 in plate has an 18 in by 10 in opening cut from it. Find the area of metal that remains.",
        [("Outside: (30)(20) = 600", "The whole plate."), ("Opening: (18)(10) = 180", "The piece removed."), ("600 − 180 = 420", "A hole is subtracted.")], "420 sq in")
example("A flat ring gasket has an outside radius of 8 ft and an inside radius of 5 ft. Find its area.",
        [("Outer circle: (3.14)(8)² = 200.96", ""), ("Inner circle: (3.14)(5)² = 78.5", ""), ("200.96 − 78.5 = 122.46", "Subtract the hole.")], "122.46 sq ft")
warn("Subtract areas, not radii",
     "The ring is **not** a circle of radius 8 − 5 = 3. That would give 28.26 sq ft. Find each full area first, then subtract.")
sub("Half circles and quarter circles")
p("A semicircle has half the area of the full circle: A = [[πr²|2]]. Its curved edge is half the circumference, [[πd|2]]. "
  "When a semicircle sits on the end of a rectangle, its diameter equals the width of the rectangle.")
example("A window is a rectangle 4 ft wide and 5 ft tall with a semicircle on top. Find its area.",
        [("Rectangle: (4)(5) = 20", ""), ("r = 4 ÷ 2 = 2", "The semicircle’s diameter is the 4-ft width."),
         ("Semicircle: [[(3.14)(2)²|2]] = [[12.56|2]] = 6.28", "Half of a full circle."), ("20 + 6.28 = 26.28", "Add.")], "26.28 sq ft")
sub("Perimeter of a composite figure")
p("The perimeter of a composite figure is the distance around its **outside edge only**. Do not count the dashed lines where the "
  "parts were split; those lines are inside the figure. For the L-shaped floor: 20 + 8 + 8 + 6 + 12 + 14 = 68 ft. "
  "For the window above: 4 + 5 + 5 plus the half circumference (3.14)(4) ÷ 2 = 6.28, for 20.28 ft in all.")

comp = [("An L-shaped room is 24 ft by 18 ft overall with a 10 ft by 6 ft corner missing. Find its area.", n(24 * 18 - 60) + " sq ft"),
        ("Find the perimeter of the room in problem 1.", n(2 * 24 + 2 * 18) + " ft"),
        ("A gable wall is 28 ft wide and 9 ft high to the eaves, with a triangular gable 7 ft high. Find its area.", n(28 * 9 + 28 * 7 / 2) + " sq ft"),
        ("A 36 in by 24 in panel has a 12 in by 12 in square opening. Find the remaining area.", n(36 * 24 - 144) + " sq in"),
        ("A 20 in by 20 in plate has a circular hole 8 in in diameter. Find the remaining area.", n(400 - PI * 16) + " sq in"),
        ("A ring has an outside diameter of 12 in and an inside diameter of 6 in. Find its area.", n(PI * 36 - PI * 9) + " sq in"),
        ("A table top is a rectangle 6 ft by 3 ft with a semicircle on each 3-ft end. Find its area.", n(18 + PI * 1.5 ** 2) + " sq ft"),
        ("Find the perimeter of the table top in problem 7.", n(12 + PI * 3) + " ft"),
        ("A wall 30 ft by 9 ft has two windows 4 ft by 5 ft and a door 3 ft by 7 ft. How much wall is left to paint?", n(270 - 40 - 21) + " sq ft"),
        ("A trapezoid with bases 10 in and 16 in and height 8 in has a rectangle 16 in by 5 in attached to its longer base. Find the total area.", n(104 + 80) + " sq in"),
        ("A square 10 cm on a side has a quarter circle of radius 10 cm removed from one corner. Find the remaining area.", n(100 - PI * 100 / 4) + " cm²"),
        ("A hexagonal nut has sides of 0.5 in and a round hole 0.5 in in diameter. Find the area of its face to the nearest hundredth.",
         r(2.6 * 0.25 - PI * 0.0625, 2) + " sq in")]
practice("Composite figures", "Sketch each figure, split it into simple shapes, and show each area. Use π = 3.14.", comp, cols=1)

summary(["Circle: d = 2r, C = πd, A = πr², with π = 3.14. Use the radius for area.",
         "Regular hexagon: P = 6s, A = 2.6s², across corners d = 2s, across flats f = 1.732s.",
         "To work backward from an area with a squared term, divide first, then take the square root.",
         "Composite area: separate, find each area, add joined parts and subtract holes.",
         "Composite perimeter: follow the outside edge only."])
review([("Circle: r = 9 in. Find d and C.", f"d = 18 in; C = {n(PI * 18)} in"), ("Circle: d = 22 ft. Find A.", n(PI * 121) + " sq ft"),
        ("Circle: C = 78.5 cm. Find d.", n(25) + " cm"), ("Circle: A = 50.24 sq in. Find r.", n(4) + " in"),
        ("Circle: A = 90 sq ft. Find r to the nearest hundredth.", r(sqrt(90 / PI), 2) + " ft"),
        ("Hexagon: s = 7 in. Find P.", n(42) + " in"), ("Hexagon: s = 7 in. Find A.", n(2.6 * 49) + " sq in"),
        ("Hexagon: s = 7 in. Find d and f.", f"d = 14 in; f = {n(1.732 * 7)} in"),
        ("Hexagon: A = 400 sq m. Find s to the nearest tenth.", r(sqrt(400 / 2.6), 1) + " m"),
        ("Hexagon: f = 3 in. Find s to the nearest hundredth.", r(3 / 1.732, 2) + " in"),
        ("An L-shaped slab is 30 ft by 20 ft overall with a 12 ft by 8 ft corner missing. Find its area.", n(600 - 96) + " sq ft"),
        ("A 48 in by 30 in sheet has two round holes, each 10 in in diameter. Find the remaining area.", n(1440 - 2 * PI * 25) + " sq in"),
        ("A ring has an outside radius of 10 cm and an inside radius of 7 cm. Find its area.", n(PI * 100 - PI * 49) + " cm²"),
        ("A window is a 3 ft by 4 ft rectangle topped by a semicircle on the 3-ft side. Find its area.", n(12 + PI * 2.25 / 2) + " sq ft"),
        ("A gable end is 24 ft wide, 8 ft to the eaves and 5 ft more to the peak. Find its area.", n(192 + 60) + " sq ft"),
        ("Why is the area of a ring with radii 10 and 7 not the area of a circle with radius 3?",
         "Areas depend on the square of the radius: 10² − 7² = 51, but 3² = 9. Subtract the areas, not the radii.")])
