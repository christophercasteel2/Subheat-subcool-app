"""Chapter 7: triangle trigonometry (new material, written with the new numbering)."""
import math
from book import *  # noqa: F401,F403
from util import n
import figs

S = lambda d: math.sin(math.radians(d))  # noqa: E731
Co = lambda d: math.cos(math.radians(d))  # noqa: E731
Ta = lambda d: math.tan(math.radians(d))  # noqa: E731
AS = lambda x: math.degrees(math.asin(x))  # noqa: E731
AC = lambda x: math.degrees(math.acos(x))  # noqa: E731
AT = lambda x: math.degrees(math.atan(x))  # noqa: E731


def h2(x):
    return n(x, 2)


def d1(x):
    return n(x, 1) + "°"


def r4(x):
    return n(x, 4)


def dms(x):
    """decimal degrees -> d° m′ s″ to the nearest second"""
    tot = round(x * 3600)
    d, rem = divmod(tot, 3600)
    m, s = divmod(rem, 60)
    return f"{d}° {m}′ {s}″"


# ===================================================================== 7.1 Angles
chapter("Angles",
        ["Name an angle as acute, right, obtuse or straight.",
         "Use the fact that the angles of a triangle add to 180°.",
         "Change an angle between degrees-minutes-seconds and decimal degrees.",
         "Add and subtract angles written in degrees and minutes."],
        "Trigonometry is about angles, so it starts with how angles are measured and written. A roof pitch, a conduit bend and a "
        "machinist’s taper are all specified in degrees, and often in minutes and seconds as well.",
        [("angle", "The opening between two lines that meet at a point, the vertex."),
         ("degree", "The unit of angle: one 360th of a full turn, written °."),
         ("minute, second", "Parts of a degree: 1° = 60 minutes (60′), and 1′ = 60 seconds (60″)."),
         ("complementary", "Two angles that add to 90°.")])

sec("7.1 Measuring angles")
p("A full turn is divided into 360 equal parts called **degrees**. A quarter turn, the corner of a square, is 90°: a **right angle**. "
  "A half turn, a straight line, is 180°.")
table(["Name", "Size", "Example"],
      [["acute", "less than 90°", "the angle of a ramp"], ["right", "exactly 90°", "the corner of a sheet of plywood"],
       ["obtuse", "between 90° and 180°", "the inside corner of a hexagon, 120°"], ["straight", "exactly 180°", "a straight line"]], widths=[22, 34, 44])
rule("The angles of a triangle", "The three angles of any triangle add up to **180°**.",
     "In a right triangle one angle is 90°, so the other two add to 90°. They are **complementary**.")
example("A right triangle has one acute angle of 34°. Find the other acute angle.",
        [("90° − 34° = 56°", "The two acute angles of a right triangle add to 90°.")], "56°")
example("Two angles of a triangle are 47° and 68°. Find the third.",
        [("47° + 68° = 115°", "Add the known angles."), ("180° − 115° = 65°", "The three add to 180°.")], "65°")

sec("7.2 Degrees, minutes and seconds")
p("For finer measurement each degree is divided into 60 **minutes** (′) and each minute into 60 **seconds** (″). An angle on a drawing may read "
  "32° 15′, which is 32 degrees and 15 minutes. A calculator works in **decimal degrees**, so angles must be changed between the two forms.")
rule("Converting angles",
     "**To decimal degrees:** degrees + [[minutes|60]] + [[seconds|3600]].",
     "**To degrees and minutes:** multiply the decimal part by 60 to get minutes; multiply what is left after the minutes by 60 to get seconds.")
example("Change 32° 15′ to decimal degrees.",
        [("15 ÷ 60 = 0.25", "Minutes to degrees."), ("32 + 0.25 = 32.25", "Add the whole degrees.")], "32.25°")
example("Change 47.36° to degrees, minutes and seconds.",
        [("0.36 × 60 = 21.6′", "The decimal part of a degree, times 60, gives minutes."), ("0.6 × 60 = 36″", "The decimal part of a minute, times 60, gives seconds."),
         ("47° 21′ 36″", "Put the pieces together.")], "47° 21′ 36″")
example("Add 28° 45′ and 16° 30′.",
        [("28° + 16° = 44°;  45′ + 30′ = 75′", "Add degrees to degrees and minutes to minutes."), ("75′ = 1° 15′", "60 minutes make a degree."), ("45° 15′", "")],
        "45° 15′", title="Carrying minutes")
example("Subtract 90° − 37° 25′.",
        [("90° = 89° 60′", "Borrow 1° as 60′."), ("89° 60′ − 37° 25′ = 52° 35′", "")], "52° 35′", title="Borrowing a degree")
warn("A minute is not a hundredth", "32° 15′ is 32.25°, not 32.15°. There are 60 minutes in a degree, just as there are 60 minutes in an hour.")
tip("Angles on the calculator",
    "Keep angles in decimal degrees on the calculator and round only at the end. Many calculators also have a key or menu item that converts "
    "between decimal degrees and degrees-minutes-seconds (marked DMS or ° ′ ″).")

its = []
for d_, m_ in [(18, 30), (42, 45), (65, 12), (7, 6), (89, 51)]:
    its.append((f"{d_}° {m_}′ to decimal degrees (nearest hundredth)", n(d_ + m_ / 60, 2) + "°"))
for x in [26.5, 53.75, 12.4, 71.125, 33.31]:
    its.append((f"{n(x)}° to degrees, minutes and seconds", dms(x)))
its += [("A right triangle has an acute angle of 27°. Find the other.", "63°"), ("A right triangle has an acute angle of 52.6°. Find the other.", "37.4°"),
        ("Two angles of a triangle are 72° and 41°. Find the third.", "67°"), ("Each angle of an equilateral triangle is how many degrees?", "60°"),
        ("31° 40′ + 25° 35′", "57° 15′"), ("90° − 64° 18′", "25° 42′"), ("180° − 112° 45′", "67° 15′"), ("Classify 135°.", "obtuse")]
practice("Angles", "", its, cols=2)
summary(["A full turn is 360°; a right angle is 90°; a straight angle is 180°.",
         "The angles of a triangle add to 180°; the acute angles of a right triangle add to 90°.",
         "1° = 60′ and 1′ = 60″. To decimal degrees: degrees + minutes ÷ 60 + seconds ÷ 3600."])
review([("Classify an angle of 90°.", "right"), ("Classify an angle of 17°.", "acute"), ("A right triangle has an acute angle of 38.5°. Find the other.", "51.5°"),
        ("Two angles of a triangle are 55° and 80°. Find the third.", "45°"), ("Change 24° 36′ to decimal degrees.", "24.6°"),
        ("Change 58.45° to degrees and minutes.", "58° 27′"), ("Change 15° 20′ 24″ to decimal degrees (nearest hundredth).", n(15 + 20 / 60 + 24 / 3600, 2) + "°"),
        ("46° 50′ + 18° 25′", "65° 15′")])

# ===================================================================== 7.2 Ratios
chapter("The Trigonometric Ratios",
        ["Name the hypotenuse, opposite side and adjacent side of a right triangle for a given angle.",
         "Write the sine, cosine and tangent of an angle as ratios of sides.",
         "Find the sine, cosine and tangent of an angle on a calculator in degree mode.",
         "Find an angle from a ratio with the inverse functions."],
        "In every right triangle with a 30° angle, the side across from that angle is exactly half the hypotenuse, whatever the size of the triangle. "
        "Ratios like this one depend only on the angle, and they are what let a technician turn an angle into a length.",
        [("hypotenuse", "The side across from the right angle; the longest side."),
         ("opposite side", "The side across from the angle being used."),
         ("adjacent side", "The side next to the angle being used that is not the hypotenuse."),
         ("sine, cosine, tangent", "The three ratios of the sides of a right triangle: sin, cos and tan."),
         ("inverse function", "A key such as sin⁻¹ that turns a ratio back into an angle.")])

sec("7.3 Naming the sides")
p("In a right triangle the **hypotenuse** is always the side across from the right angle. The other two names depend on **which acute angle** is being used, "
  "and that angle is usually called θ (the Greek letter theta).")
bullets(["The **opposite** side is across the triangle from θ; it does not touch θ.",
         "The **adjacent** side touches θ and is not the hypotenuse."])
fig(figs.side_by_side([figs.trig_triangle("A", size=0.85), figs.trig_triangle("B", size=0.85)], gap=10),
    "The same triangle twice. Moving θ to the other acute angle swaps the opposite and adjacent sides; the hypotenuse never changes.")
warn("Name the sides from the angle", "“Opposite” and “adjacent” have no meaning until the angle is chosen. Mark θ first, then label the sides.")

sec("7.4 Sine, cosine and tangent")
rule("The three trigonometric ratios",
     "sin θ = [[opposite|hypotenuse]]          cos θ = [[adjacent|hypotenuse]]          tan θ = [[opposite|adjacent]]",
     "Memory aid: **SOH CAH TOA**: Sine is Opposite over Hypotenuse, Cosine is Adjacent over Hypotenuse, Tangent is Opposite over Adjacent.")
example("A right triangle has sides 6, 8 and 10. For the angle θ across from the side 6, find sin θ, cos θ and tan θ.",
        [("hypotenuse = 10;  opposite = 6;  adjacent = 8", "The longest side is the hypotenuse; 6 is across from θ."),
         ("sin θ = [[6|10]] = 0.6", "Opposite over hypotenuse."), ("cos θ = [[8|10]] = 0.8", "Adjacent over hypotenuse."), ("tan θ = [[6|8]] = 0.75", "Opposite over adjacent.")],
        "sin θ = 0.6;  cos θ = 0.8;  tan θ = 0.75")
sub("Finding the ratios on a calculator")
p("A calculator gives the sine, cosine or tangent of any angle. It must be in **degree mode**; in radian mode sin 30 gives −0.988 instead of 0.5. "
  "Round ratios to four decimal places.")
tip("Degree mode on the HP Prime",
    "Press **Shift**, then **Home** (Settings), and set **Angle Measure** to **Degrees**. Check it with sin(30): the answer must be 0.5.")
table(["Angle", "sin", "cos", "tan"], [[f"{a}°", r4(S(a)), r4(Co(a)), r4(Ta(a))] for a in (15, 30, 45, 60, 75)],
      caption="Table 7.1  Values worth recognizing (rounded to four places)", small=True)
sub("Finding an angle from a ratio")
p("The **inverse** functions run the other way: given a ratio, they return the angle. They are written sin⁻¹, cos⁻¹ and tan⁻¹ "
  "(read “inverse sine”, also called arcsine). On most calculators they are the shifted functions of the SIN, COS and TAN keys.")
example("tan θ = 0.75. Find θ to the nearest tenth of a degree.",
        [("θ = tan⁻¹(0.75)", "Inverse tangent."), (f"θ = {n(AT(0.75), 4)}…", "Calculator in degree mode."), (d1(AT(0.75)), "Round.")], d1(AT(0.75)))
example("In a right triangle the side opposite θ is 7 and the hypotenuse is 12. Find θ.",
        [("sin θ = [[7|12]]", "Opposite and hypotenuse: sine."), (f"θ = sin⁻¹([[7|12]]) = {n(AS(7 / 12), 4)}…", "Enter sin⁻¹(7 ÷ 12) with the parentheses."),
         (d1(AS(7 / 12)), "Round.")], d1(AS(7 / 12)))
warn("sin⁻¹ is not 1 ÷ sin", "The small −1 means “inverse function,” not “reciprocal.” sin⁻¹(0.5) is 30°; 1 ÷ sin(0.5) is a different number altogether.")

its = []
for o, a_, h in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (20, 21, 29)]:
    its.append((f"Sides {o}, {a_}, {h}; θ is across from {o}. Find sin θ, cos θ, tan θ (four places).",
                f"sin θ = {r4(o / h)}; cos θ = {r4(a_ / h)}; tan θ = {r4(o / a_)}"))
for a in (20, 35, 52, 68, 81):
    its.append((f"sin {a}°, cos {a}°, tan {a}° (four places)", f"{r4(S(a))}; {r4(Co(a))}; {r4(Ta(a))}"))
for f_, v, name in [(AS, 0.4226, "sin θ = 0.4226"), (AC, 0.5, "cos θ = 0.5"), (AT, 1.8, "tan θ = 1.8"), (AS, 0.9, "sin θ = 0.9"), (AC, 0.2588, "cos θ = 0.2588"),
                    (AT, 0.3, "tan θ = 0.3")]:
    its.append((f"{name}. Find θ to the nearest tenth of a degree.", d1(f_(v))))
practice("The ratios", "Calculator in degree mode.", its, cols=1)
summary(["Hypotenuse: across from the right angle. Opposite: across from θ. Adjacent: touches θ, not the hypotenuse.",
         "SOH CAH TOA: sin = opp ÷ hyp, cos = adj ÷ hyp, tan = opp ÷ adj.",
         "Use degree mode; sin 30° = 0.5 is the check.", "sin⁻¹, cos⁻¹ and tan⁻¹ turn a ratio back into an angle."])
review([("Which side of a right triangle is always the longest?", "the hypotenuse"), ("Write the ratio for cos θ.", "adjacent ÷ hypotenuse"),
        ("Write the ratio for tan θ.", "opposite ÷ adjacent"),
        ("Sides 9, 12, 15; θ across from 9. Find sin θ and tan θ.", "sin θ = 0.6; tan θ = 0.75"),
        ("Find sin 42° to four places.", r4(S(42))), ("Find cos 18° to four places.", r4(Co(18))), ("Find tan 63° to four places.", r4(Ta(63))),
        ("sin θ = 0.6. Find θ to the nearest tenth.", d1(AS(0.6))), ("tan θ = 2.5. Find θ to the nearest tenth.", d1(AT(2.5))),
        ("A calculator gives sin 30 = −0.988. What is wrong?", "It is in radian mode. Switch to degrees.")])

# ===================================================================== 7.3 Solving right triangles
chapter("Solving Right Triangles",
        ["Choose the ratio that connects a known side, a wanted side and a known angle.",
         "Find a missing side of a right triangle from an angle and one side.",
         "Find a missing angle from two sides.",
         "Solve trade problems: roof pitch, ramps, ladders, heights and conduit offsets."],
        "To **solve** a triangle is to find all of its sides and angles. With trigonometry, one acute angle and one side of a right triangle are enough "
        "to find everything else, and two sides are enough to find the angles.",
        [("solve a triangle", "To find all its missing sides and angles."),
         ("angle of elevation", "The angle measured up from the horizontal to a line of sight."),
         ("offset", "In conduit and pipe, the sideways distance a run is moved by two equal bends."),
         ("multiplier", "For an offset, the number that times the offset gives the travel: 1 ÷ sin θ.")])

sec("7.5 Finding a side")
rule("Solving for a side",
     "**1.** Sketch the triangle. Mark the known angle θ, the known side and the wanted side.",
     "**2.** Name the two sides you are working with: opposite, adjacent or hypotenuse.",
     "**3.** Pick the ratio that uses exactly those two sides (SOH CAH TOA).",
     "**4.** Substitute and solve. If the unknown is on top, multiply; if it is on the bottom, divide.")
o = 20 * S(35)
fig(figs.side_by_side([figs.labeled_right_triangle("x", "", "20 in", "35°"), figs.labeled_right_triangle("9 ft", "x", "", "28°")], gap=14),
    "Left: Example 7.10, the side opposite the 35° angle. Right: Example 7.11, the side adjacent to the 28° angle.")
example("A right triangle has a hypotenuse of 20 in and an acute angle of 35°. Find the side opposite the 35° angle.",
        [("opposite and hypotenuse → sine", "The wanted side is opposite 35°; the known side is the hypotenuse."),
         ("sin 35° = [[x|20]]", "Set up the ratio."), (f"x = 20 × sin 35° = 20 × {r4(S(35))}", "The unknown is on top: multiply both sides by 20."),
         (f"x = {h2(o)}", "Round to the nearest hundredth.")], f"{h2(o)} in", title="Unknown on top")
a = 9 / Ta(28)
example("In a right triangle the side opposite a 28° angle is 9 ft. Find the side adjacent to the 28° angle.",
        [("opposite and adjacent → tangent", ""), ("tan 28° = [[9|x]]", "The unknown is on the bottom."),
         ("x × tan 28° = 9", "Multiply both sides by x."), (f"x = [[9|tan 28°]] = [[9|{r4(Ta(28))}]] = {h2(a)}", "Divide by tan 28°.")], f"{h2(a)} ft",
        title="Unknown on the bottom")
hyp = 15 / Co(40)
example("A right triangle has an angle of 40° and the side adjacent to it is 15 cm. Find the hypotenuse.",
        [("adjacent and hypotenuse → cosine", ""), ("cos 40° = [[15|x]]", ""), (f"x = [[15|cos 40°]] = {h2(hyp)}", "Unknown on the bottom: divide.")], f"{h2(hyp)} cm")
warn("Multiply or divide?", "When the unknown side is on the bottom of the ratio, the answer is the known side **divided** by the trig value. "
     "A hypotenuse found this way must come out longer than either leg; if it does not, the division was done upside down.")

sec("7.6 Finding an angle")
p("When two sides are known, the matching ratio gives a number, and the inverse function turns that number into the angle.")
th = AT(7 / 12)
example("A right triangle has legs of 7 in and 12 in. Find the angle across from the 7-in leg, and the other acute angle.",
        [("tan θ = [[7|12]]", "Opposite and adjacent."), (f"θ = tan⁻¹([[7|12]]) = {n(th, 4)}… → {d1(th)}", "Inverse tangent."),
         (f"90° − {d1(th)} = {n(90 - round(th, 1), 1)}°", "The acute angles add to 90°.")], f"{d1(th)} and {n(90 - round(th, 1), 1)}°")
sub("Solving a triangle completely")
c = math.hypot(5, 8)
example("Solve the right triangle with legs 5 ft and 8 ft: find the hypotenuse and both acute angles.",
        [(f"c = √(5² + 8²) = √89 = {h2(c)}", "The Pythagorean theorem from Section 5.2."),
         (f"θ = tan⁻¹([[5|8]]) = {d1(AT(5 / 8))}", "The angle across from the 5-ft leg."),
         (f"90° − {d1(AT(5 / 8))} = {n(90 - round(AT(5 / 8), 1), 1)}°", "The other acute angle.")],
        f"c = {h2(c)} ft; angles {d1(AT(5 / 8))} and {n(90 - round(AT(5 / 8), 1), 1)}°")

sec("7.7 Right triangles on the job")
sub("Roof pitch")
pitch = AT(6 / 12)
example("A roof has a 6-in-12 pitch (it rises 6 in for every 12 in of run). Find the roof angle and the length of a rafter over a 14-ft run.",
        [(f"θ = tan⁻¹([[6|12]]) = {d1(pitch)}", "Rise is opposite the roof angle, run is adjacent."),
         (f"rafter = [[14|cos {n(pitch, 2)}°]] = {h2(14 / Co(pitch))}", "The run is adjacent to the angle; the rafter is the hypotenuse."),
         (f"Check: √(14² + 7²) = {h2(math.hypot(14, 7))} ✓", "A 6-in-12 pitch over a 14-ft run rises 7 ft.")],
        f"{d1(pitch)}; {h2(14 / Co(pitch))} ft")
sub("Ramps")
fig(figs.ramp(), "A ramp rising 20 in over a 20-ft run. The angle is small, so the drawing is exaggerated.", width="4.6in")
ra = AT(20 / 240)
example("A ramp rises 20 in over a run of 20 ft. Find its angle.",
        [("20 ft = 240 in", "Same units."), (f"θ = tan⁻¹([[20|240]]) = {n(ra, 3)}…", "Rise over run is opposite over adjacent."), (d1(ra), "")], d1(ra))
sub("Ladders and heights")
example("A 20-ft ladder is set at 75° to the ground. How high up the wall does it reach, and how far is its foot from the wall?",
        [(f"height = 20 sin 75° = {h2(20 * S(75))}", "The ladder is the hypotenuse; the height is opposite 75°."),
         (f"foot = 20 cos 75° = {h2(20 * Co(75))}", "The distance out is adjacent.")], f"{h2(20 * S(75))} ft up; {h2(20 * Co(75))} ft out")
example("From a point 50 ft from the base of a tower, the angle of elevation to the top is 38°. How tall is the tower?",
        [(f"tan 38° = [[x|50]]", "Height opposite, distance adjacent."), (f"x = 50 tan 38° = {h2(50 * Ta(38))}", "")], f"{h2(50 * Ta(38))} ft")
sub("Conduit and pipe offsets")
p("An **offset** moves a run of conduit or pipe sideways around an obstruction with two equal bends. The piece between the bends, the **travel**, is the hypotenuse "
  "of a right triangle whose opposite side is the offset. So travel = offset ÷ sin θ. The number 1 ÷ sin θ is the bend’s **multiplier**.")
fig(figs.offset_bend(), "A 30° offset. The travel is the hypotenuse and the offset is the side opposite the bend angle.", width="5in")
table(["Bend angle", "Multiplier (1 ÷ sin θ)", "Travel for a 10-in offset"],
      [[f"{a}°", n(1 / S(a), 3), f"{h2(10 / S(a))} in"] for a in (10, 22.5, 30, 45, 60)], caption="Table 7.2  Offset multipliers", widths=[24, 38, 38])
example("A conduit run must offset 8 in to clear a beam, using two 30° bends. How far apart are the bends (the travel)?",
        [("sin 30° = [[8|x]]", "Offset is opposite; travel is the hypotenuse."), ("x = [[8|0.5]] = 16", "Divide: unknown on the bottom.")], "16 in",
        title="Travel of an offset")
shop("Why 30° bends are popular", "For a 30° bend the multiplier is exactly 2: the travel is twice the offset, easy to lay out with a tape and no calculator.")

its = []
for ang, known, side, want in [(32, "hypotenuse", 18, "opposite"), (55, "hypotenuse", 24, "adjacent"), (40, "adjacent", 12, "opposite"),
                               (25, "opposite", 7, "hypotenuse"), (62, "adjacent", 9, "hypotenuse"), (48, "opposite", 15, "adjacent"),
                               (17, "hypotenuse", 40, "opposite"), (71, "opposite", 30, "adjacent")]:
    fn = {("hypotenuse", "opposite"): lambda: side * S(ang), ("hypotenuse", "adjacent"): lambda: side * Co(ang),
          ("adjacent", "opposite"): lambda: side * Ta(ang), ("opposite", "hypotenuse"): lambda: side / S(ang),
          ("adjacent", "hypotenuse"): lambda: side / Co(ang), ("opposite", "adjacent"): lambda: side / Ta(ang)}[(known, want)]
    its.append((f"Angle {ang}°, {known} {side} in. Find the {want} side (nearest hundredth).", h2(fn()) + " in"))
for o_, a_ in [(4, 9), (10, 6), (3, 3), (12, 5)]:
    its.append((f"Legs: opposite {o_}, adjacent {a_}. Find θ (nearest tenth).", d1(AT(o_ / a_))))
for o_, h_ in [(5, 13), (11, 20)]:
    its.append((f"Opposite {o_}, hypotenuse {h_}. Find θ (nearest tenth).", d1(AS(o_ / h_))))
for a_, h_ in [(8, 17), (14, 25)]:
    its.append((f"Adjacent {a_}, hypotenuse {h_}. Find θ (nearest tenth).", d1(AC(a_ / h_))))
practice("Sides and angles", "Sides to the nearest hundredth, angles to the nearest tenth of a degree.", its, cols=1)

ap = [("A roof has a 4-in-12 pitch. Find the roof angle.", d1(AT(4 / 12))),
      ("A roof has an 8-in-12 pitch over a 12-ft run. Find the rafter length.", h2(12 / Co(AT(8 / 12))) + " ft"),
      ("A ramp must not be steeper than 1 in of rise per 12 in of run. What is the largest angle?", d1(AT(1 / 12))),
      ("A ramp rises 30 in over a run of 30 ft. Find its angle.", d1(AT(30 / 360))),
      ("A 24-ft ladder stands at 72°. How high does it reach?", h2(24 * S(72)) + " ft"),
      ("A 16-ft ladder reaches 15 ft up a wall. What angle does it make with the ground?", d1(AS(15 / 16))),
      ("From 80 ft away, the angle of elevation to the top of a stack is 30°. How tall is the stack?", h2(80 * Ta(30)) + " ft"),
      ("A guy wire makes a 58° angle with the ground and is fastened 40 ft up a pole. How long is the wire?", h2(40 / S(58)) + " ft"),
      ("A 45° offset must clear 12 in. Find the travel.", h2(12 / S(45)) + " in"),
      ("A 22.5° offset must clear 6 in. Find the travel.", h2(6 / S(22.5)) + " in"),
      ("Two 30° bends are 18 in apart along the conduit. How much offset do they make?", "9 in"),
      ("A brace runs from a point 6 ft up a post to a point 4 ft out on the beam. Find the angle the brace makes with the post.", d1(AT(4 / 6)))]
practice("On the job", "Sketch the triangle first. Sides to the nearest hundredth, angles to the nearest tenth.", ap, cols=1)
summary(["Mark θ, name the two sides involved, and choose sin, cos or tan by SOH CAH TOA.",
         "Unknown side on top of the ratio: multiply. Unknown on the bottom: divide.",
         "Two sides give an angle with sin⁻¹, cos⁻¹ or tan⁻¹; the other acute angle is 90° minus it.",
         "Pitch and slope are rise over run: tan θ. Offset travel = offset ÷ sin θ."])
review([("Angle 36°, hypotenuse 25 ft. Find the opposite side.", h2(25 * S(36)) + " ft"), ("Angle 52°, adjacent 10 in. Find the opposite side.", h2(10 * Ta(52)) + " in"),
        ("Angle 23°, opposite 6 m. Find the hypotenuse.", h2(6 / S(23)) + " m"), ("Angle 65°, adjacent 14 in. Find the hypotenuse.", h2(14 / Co(65)) + " in"),
        ("Legs 9 and 16. Find the angle across from the 9.", d1(AT(9 / 16))), ("Opposite 7, hypotenuse 25. Find θ.", d1(AS(7 / 25))),
        ("A roof has a 9-in-12 pitch. Find its angle.", d1(AT(9 / 12))), ("A 30-ft ladder stands at 70°. How far is its foot from the wall?", h2(30 * Co(70)) + " ft"),
        ("A 30° offset clears 14 in. Find the travel.", "28 in"), ("From 120 ft away the angle of elevation to a roof edge is 21°. How high is the edge?", h2(120 * Ta(21)) + " ft")])

# ===================================================================== 7.4 Oblique triangles
chapter("Oblique Triangles",
        ["Use the law of sines to find sides and angles of any triangle.",
         "Use the law of cosines when two sides and the angle between them, or all three sides, are known.",
         "Find the area of a triangle from two sides and the angle between them."],
        "Many triangles in layout and surveying have no right angle. Two laws extend trigonometry to every triangle.",
        [("oblique triangle", "A triangle with no right angle."),
         ("law of sines", "In any triangle, a ÷ sin A = b ÷ sin B = c ÷ sin C."),
         ("law of cosines", "In any triangle, c² = a² + b² − 2ab cos C.")])

sec("7.8 Labeling an oblique triangle")
p("The angles are named with capital letters A, B and C, and each side is named with the small letter of the angle **across** from it: side *a* is opposite angle A, and so on.")
fig(figs.oblique(), "An oblique triangle. Each side carries the small letter of the angle across from it.", width="3.8in")

sec("7.9 The law of sines")
rule("Law of sines", "[[a|sin A]] = [[b|sin B]] = [[c|sin C]]",
     "Use it when you know **two angles and a side**, or **two sides and the angle across from one of them**.")
A_, B_, a_ = 40, 65, 12
C_ = 180 - A_ - B_
b_, c_ = a_ * S(B_) / S(A_), a_ * S(C_) / S(A_)
example("In triangle ABC, A = 40°, B = 65° and a = 12 ft. Find C, b and c.",
        [(f"C = 180° − 40° − 65° = {C_}°", "Angles add to 180°."),
         (f"[[b|sin 65°]] = [[12|sin 40°]]  →  b = [[12 sin 65°|sin 40°]] = {h2(b_)}", "Pair the side you want with the known pair a and A."),
         (f"c = [[12 sin 75°|sin 40°]] = {h2(c_)}", "The same way for c.")], f"C = {C_}°; b = {h2(b_)} ft; c = {h2(c_)} ft")
warn("Two possible triangles", "When two sides and an angle opposite one of them are given, there can sometimes be two different triangles that fit. "
     "Problems in this book give enough information for only one; in the field, sketch the triangle to see which one is meant.")

sec("7.10 The law of cosines")
rule("Law of cosines", "c² = a² + b² − 2ab cos C",
     "Use it when you know **two sides and the angle between them**, or **all three sides**.",
     "To find an angle from three sides: cos C = [[a² + b² − c²|2ab]]")
cc = math.sqrt(81 + 196 - 2 * 9 * 14 * Co(50))
example("Two sides of a triangle are 9 in and 14 in, and the angle between them is 50°. Find the third side.",
        [("c² = 9² + 14² − 2(9)(14) cos 50°", "Substitute: a = 9, b = 14, C = 50°."),
         (f"c² = 81 + 196 − 252({r4(Co(50))}) = {n(cc * cc, 2)}", "Work the multiplication before subtracting."), (f"c = {h2(cc)}", "Square root.")],
        f"{h2(cc)} in")
Cang = AC((49 + 100 - 144) / 140)
example("A triangle has sides 7, 10 and 12 ft. Find the largest angle.",
        [("The largest angle is across from the longest side, 12.", ""), ("cos C = [[7² + 10² − 12²|2(7)(10)]] = [[5|140]]", ""),
         (f"C = cos⁻¹([[5|140]]) = {d1(Cang)}", "")], d1(Cang), title="An angle from three sides")
sub("Area from two sides and the angle between them")
rule("Area of any triangle", "A = ½ab sin C", "where C is the angle between sides a and b.")
Ci = AC((169 + 196 - 225) / 364)
example("A triangle has sides 13 in and 14 in with an angle of 67.38° between them. Find its area, and check it with Hero’s Formula for sides 13, 14 and 15.",
        [(f"A = ½(13)(14) sin 67.38° = {h2(0.5 * 13 * 14 * S(67.38))}", "Two sides and the included angle."),
         ("Hero: s = 21; √(21 × 8 × 7 × 6) = √7056 = 84 ✓", "The third side of this triangle is 15, so Section 5.2’s formula applies too.")],
        f"about {n(round(0.5 * 13 * 14 * S(67.38)))} sq in")

its = []
for A1, B1, a1 in [(50, 60, 10), (35, 80, 20), (72, 48, 15)]:
    C1 = 180 - A1 - B1
    its.append((f"A = {A1}°, B = {B1}°, a = {a1}. Find C, b and c.", f"C = {C1}°; b = {h2(a1 * S(B1) / S(A1))}; c = {h2(a1 * S(C1) / S(A1))}"))
for a1, b1, C1 in [(8, 11, 60), (20, 15, 110), (6, 9, 35)]:
    its.append((f"a = {a1}, b = {b1}, C = {C1}°. Find c.", h2(math.sqrt(a1 * a1 + b1 * b1 - 2 * a1 * b1 * Co(C1)))))
for a1, b1, c1 in [(5, 7, 9), (10, 12, 15), (8, 8, 10)]:
    its.append((f"Sides {a1}, {b1}, {c1}. Find the largest angle.", d1(AC((a1 * a1 + b1 * b1 - c1 * c1) / (2 * a1 * b1)))))
its += [("Sides 10 ft and 16 ft with 42° between them. Find the area.", h2(0.5 * 160 * S(42)) + " sq ft"),
        ("A surveyor measures two sides of a lot, 120 ft and 95 ft, with 74° between them. How long is the third side?",
         h2(math.sqrt(120 ** 2 + 95 ** 2 - 2 * 120 * 95 * Co(74))) + " ft")]
practice("Oblique triangles", "Sides to the nearest hundredth, angles to the nearest tenth.", its, cols=1)
summary(["Side a is across from angle A, side b from B, side c from C.",
         "Law of sines: a ÷ sin A = b ÷ sin B = c ÷ sin C. Use with two angles and a side.",
         "Law of cosines: c² = a² + b² − 2ab cos C. Use with two sides and the included angle, or three sides.",
         "Area of any triangle: ½ab sin C."])
review([("A = 45°, B = 70°, a = 20. Find b.", h2(20 * S(70) / S(45))), ("A = 30°, C = 100°, a = 8. Find c.", h2(8 * S(100) / S(30))),
        ("a = 12, b = 9, C = 75°. Find c.", h2(math.sqrt(144 + 81 - 216 * Co(75)))), ("Sides 6, 8, 11. Find the largest angle.", d1(AC((36 + 64 - 121) / 96))),
        ("Sides 9 m and 12 m with 30° between them. Find the area.", h2(0.5 * 108 * S(30)) + " m²"),
        ("Which law would you use with three sides known?", "the law of cosines")])
