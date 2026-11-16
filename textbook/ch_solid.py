"""Chapter 13: solid geometry (the class's Chapter 9 handout and classwork)."""
from math import sqrt
from book import *  # noqa: F401,F403
from util import n, r
import figs
import x4

PI = 3.14


def tr(x):
    """a calculator display cut to four decimal places, for lines that end in …"""
    import math
    return n(math.floor(x * 10000) / 10000)


def u(x, unit):
    return f"{n(x)} {unit}"


# ---- formulas as code, so every answer below is calculated
def rect_prism(L, W, H):
    p, A = 2 * L + 2 * W, L * W
    return p, A, p * H, p * H + 2 * A, A * H


def tri_prism(s, H):
    p, A = 3 * s, 0.433 * s * s
    return p, A, p * H, p * H + 2 * A, A * H


def hex_prism(s, H):
    p, A = 6 * s, 2.6 * s * s
    return p, A, p * H, p * H + 2 * A, A * H


def cyl(d, h):
    rr = d / 2
    lsa = PI * d * h
    return lsa, lsa + 2 * PI * rr * rr, PI * rr * rr * h


def sph(d):
    return PI * d * d, PI * d ** 3 / 6


def pyramid(p, A, s, h):
    lsa = p * s / 2
    return lsa, lsa + A, A * h / 3


def frustum(P, p, A, a, s, h):
    lsa = (P + p) * s / 2
    return lsa, lsa + A + a, h * (A + a + sqrt(A * a)) / 3


chapter("Solid Geometry",
        ["Tell lateral surface area, total surface area and volume apart, and give each its correct unit.",
         "Find the area of a base that is a rectangle, a square, an equilateral triangle, a regular hexagon or a circle.",
         "Find the LSA, TSA and volume of prisms, cylinders, pyramids and frustums, and the surface area and volume of spheres.",
         "Change a volume in cubic inches or cubic feet to gallons.",
         "Find the weight of an object from its volume and density.",
         "Solve a volume formula for a missing height or radius."],
        "Tanks, ducts, hoppers, pipe and bar stock are not flat. To know how much sheet metal wraps a tank, how many gallons it holds "
        "and how much a steel shaft weighs, the flat shapes of the last three chapters have to be stood up into solids. "
        "Every formula in this chapter is built from a base area that is already familiar.",
        [("solid", "A figure that takes up space: it has length, width and height."),
         ("base", "The face a solid is named for. A prism and a cylinder have two equal bases; a pyramid has one."),
         ("lateral face", "A side of a solid that is not a base."),
         ("LSA", "Lateral surface area: the area of the sides only."),
         ("TSA", "Total surface area: the sides and the base or bases."),
         ("volume", "The amount of space a solid contains, in cubic units."),
         ("slant length", "On a pyramid or frustum, the distance up the middle of a side face. It is longer than the height."),
         ("frustum", "What is left of a pyramid when its top is cut off level: two bases of different sizes."),
         ("density", "Weight per unit of volume, such as pounds per cubic inch.")])

# ===================================================================== 13.1
sec("13.1 Three measurements of a solid")
p("A box can be measured three ways, and each answers a different question. How much metal covers its **sides**? How much metal "
  "covers the whole thing, **sides and ends**? How much does it **hold**? The class handout names the three.")
handout("CHAPTER 9: SOLID GEOMETRY",
        "**LSA = Lateral Surface Area**..... this is the area of the *sides* of the solid figure",
        "**TSA = Total Surface Area**.....this is the area of the *sides* AND the *Base(s)*",
        "**V = Volume**.....this represents the amount of space *contained* by the solid figure")
table(["Measurement", "Answers the question", "Unit"],
      [["LSA", "How much material wraps the sides?", "square units: sq in, sq ft (in², ft²)"],
       ["TSA", "How much material covers everything, ends included?", "square units: sq in, sq ft (in², ft²)"],
       ["V", "How much does it hold?", "cubic units: cu in, cu ft (in³, ft³); or gallons"]], widths=[16, 50, 34])
warn("Square units or cubic units?",
     "LSA and TSA are **areas**, so they are in square units. Only volume is in cubic units. A TSA written as 463 in³ has the right number and the wrong unit.")
sub("The base comes first")
p("Every solid in this chapter has a base that is a shape from Chapters 10 to 12. Its area, *A*, and its perimeter, *p*, are worked out "
  "**before** anything else, and then substituted into the solid’s formulas.")
handout("AREA OF BASES",
        "**SQUARE/RECTANGLE**   A = L x W",
        "**EQUILATERAL TRIANGLE**   A = .433s^{2}  (**s** = length of a **side**)",
        "**HEXAGON**   A = 2.6s^{2}  (**s** = length of a **side**)",
        "**CIRCLE**   A = πr^{2}")
table(["Base", "Area A", "Perimeter p"],
      [["rectangle", "LW", "2L + 2W"], ["square", "s²", "4s"], ["equilateral triangle", ".433s²", "3s"], ["regular hexagon", "2.6s²", "6s"],
       ["circle", "πr²", "πd (the circumference)"]], caption="Table 13.1  Base areas and perimeters", widths=[34, 33, 33])

# ===================================================================== 13.2
sec("13.2 Prisms")
p("A **prism** has two identical, parallel bases joined by rectangular sides. It is named for the shape of its base: a rectangular prism (a box), "
  "an equilateral triangle prism, a hexagonal prism. One set of three formulas covers them all.")
handout("PRISMS",
        "*p*= perimeter of **base**   *h*= height   *A*= area of the **base**",
        "**LSA = ph**     **TSA = LSA + 2A**     **VOL = Ah**",
        "Use these formulas for **ALL** prisms",
        "**Rectangular Prism**  A = L x W     **Equilateral Triangle Prism**  A =.433s^{2}  s = length of a side of the base     "
        "**Hexagonal Prism**  A = 2.6s^{2}  s = length of a side of the base",
        "These formulas are for the area of the **BASE**",
        "**You must calculate these base areas in order to substitute into the above TSA and VOL Formulas**")
fig(figs.side_by_side([figs.rect_prism(3, 2, 5, ("L", "W", "H")), figs.tri_prism(6, 20, ("s", "h")), figs.hex_prism(10, 26, ("s", "h"))], gap=16),
    "A rectangular prism, an equilateral triangle prism and a hexagonal prism. In each one, h is the distance between the two bases.")
p("Why does LSA = *ph* work? Unfold the sides of a prism and they lie flat as one long rectangle. Its length is the distance around the base, *p*, "
  "and its width is the height, *h*. The two bases are the extra pieces that TSA adds on: 2*A*.")
fig(figs.unfolded_prism(3, 2, 5), "A 3 by 2 by 5 box opened flat. The four sides make one rectangle p = 10 long and h = 5 high, so LSA = ph = 50.")
P_, A_, LSA, TSA, V = rect_prism(4, 2, 3)
example("A rectangular base prism is 4 ft long, 2 ft wide and 3 ft high. Find its LSA, TSA and volume.",
        [("A = L x W = (4)(2) = 8;  p = 2(4) + 2(2) = 12", "The base first: its area and its perimeter."),
         (f"LSA = ph = (12)(3) = {n(LSA)}", "Perimeter of the base times the height."),
         (f"TSA = LSA + 2A = {n(LSA)} + 2(8) = {n(TSA)}", "Add both bases."),
         (f"VOL = Ah = (8)(3) = {n(V)}", "Area of the base times the height.")],
        f"LSA = {u(LSA, 'sq ft')};  TSA = {u(TSA, 'sq ft')};  V = {u(V, 'cu ft')}", title="Rectangular base prism")
P_, A_, LSA, TSA, V = tri_prism(8, 30)
example("An equilateral triangle prism has base sides of 8 in. It is 30 in long. Find its LSA, TSA and volume.",
        [(f"A = .433s² = .433(8)² = .433(64) = {n(A_)}", "The base is the triangle. Square the side first."),
         ("p = 3(8) = 24", "Perimeter of the triangle."),
         (f"LSA = ph = (24)(30) = {n(LSA)}", "The 30-in length is the prism’s height: the distance between the two triangles."),
         (f"TSA = {n(LSA)} + 2({n(A_)}) = {n(TSA)}", ""),
         (f"VOL = Ah = ({n(A_)})(30) = {n(V)}", "")],
        f"LSA = {u(LSA, 'sq in')};  TSA = {u(TSA, 'sq in')};  V = {u(V, 'cu in')}", title="Triangle prism lying on its side")
warn("The height of a prism is the distance between its bases",
     "A triangle prism is often drawn lying down, like a tent. Its height *h* is then the long dimension, from one triangle to the other, "
     "not how tall the triangle stands.")
P_, A_, LSA, TSA, V = hex_prism(4, 20)
example("A hexagonal bar has base sides of 4 in and is 20 in tall. Find its LSA, TSA and volume.",
        [(f"A = 2.6s² = 2.6(4)² = 2.6(16) = {n(A_)}", "Hexagon base."), ("p = 6(4) = 24", "Six equal sides."),
         (f"LSA = (24)(20) = {n(LSA)}", ""), (f"TSA = {n(LSA)} + 2({n(A_)}) = {n(TSA)}", ""), (f"VOL = ({n(A_)})(20) = {n(V)}", "")],
        f"LSA = {u(LSA, 'sq in')};  TSA = {u(TSA, 'sq in')};  V = {u(V, 'cu in')}", title="Hexagonal prism")
tip("Write A and p beside the drawing",
    "Before any formula, write the two base numbers next to the figure: “A = 8, p = 12.” Every prism, cylinder and pyramid formula uses one or both of them.")

# ===================================================================== 13.3
sec("13.3 Volume in gallons")
p("Tanks, pans and sumps are measured in inches or feet but filled in gallons. Chapter 4 gave the two facts; the handout puts them to work.")
handout("Volume Conversions for Gallons",
        "1 cubic foot (ft^{3}) = 1728 cubic inches (in^{3})  ≈ 7.48 gallons",
        "1 gallon = 231 cubic inches (in^{3})",
        "**HOW TO CONVERT TO GALLONS!!!!!**",
        "If the **volume** calculated is in **cubic inches**>>>>>**divide by 231** to determine gallons",
        "If the **volume** calculated is in **cubic feet**>>>>>>>**multiply by 7.48** to determine gallons")
V = 36 * 24 * 30
example("A rectangular tank is 36 in long, 24 in wide and 30 in deep. How many gallons does it hold, to the nearest tenth?",
        [("A = (36)(24) = 864", "Area of the base."), (f"VOL = Ah = (864)(30) = {n(V)} cu in", "Volume in cubic inches."),
         (f"{n(V)} ÷ 231 = {tr(V / 231)}…", "Cubic inches: divide by 231."), (n(V / 231, 1), "Round.")], f"{n(V / 231, 1)} gal")
V = 6 * 4 * 3
example("A tank is 6 ft by 4 ft by 3 ft. How many gallons does it hold?",
        [(f"VOL = (6)(4)(3) = {V} cu ft", "Dimensions in feet give cubic feet."), (f"{V} × 7.48 = {n(V * 7.48)}", "Cubic feet: multiply by 7.48.")],
        f"{n(V * 7.48)} gal")
warn("Match the factor to the unit",
     "7.48 goes with cubic **feet**, 231 goes with cubic **inches**. Multiplying cubic inches by 7.48 gives an answer about 13,000 times too large.")

# ===================================================================== 13.4
sec("13.4 Cylinders")
p("A **cylinder** is a prism with a circle for its base. The prism formulas still apply: LSA is the perimeter of the base (the circumference, πd) times the height, "
  "and the volume is the base area (πr²) times the height.")
handout("CYLINDERS",
        "*d* = diameter of **base**   *r* = radius of **base**   *h* = height of cylinder",
        "**LSA = πdh**     **TSA = LSA + 2πr^{2}**     **V = πr^{2}h**")
fig(figs.side_by_side([figs.cylinder3d("d", "h"), figs.cylinder3d("d", "h", r=95, hh=60, color=figs.BLUE, fill=figs.PALE["blue"])], gap=30),
    "Tall or short, a cylinder has two circular bases. LSA uses the diameter; the base area and the volume use the radius.")
LSA, TSA, V = cyl(20, 48)
example("A water-heater tank is 20 in in diameter and 48 in tall. Find its LSA, TSA, volume and capacity in gallons. Round gallons to the nearest tenth.",
        [("d = 20;  r = 10;  h = 48", "List the dimensions. The radius is half the diameter."),
         (f"LSA = πdh = (3.14)(20)(48) = {n(LSA)}", "The sides: circumference times height."),
         (f"TSA = {n(LSA)} + 2(3.14)(10)² = {n(LSA)} + 628 = {n(TSA)}", "Add the top and the bottom: two circles of πr² = 314 each."),
         (f"V = πr²h = (3.14)(10)²(48) = {n(V)}", "Square the radius first."),
         (f"{n(V)} ÷ 231 = {tr(V / 231)}… → {n(V / 231, 1)}", "Cubic inches to gallons: divide by 231.")],
        f"LSA = {u(LSA, 'sq in')};  TSA = {u(TSA, 'sq in')};  V = {u(V, 'cu in')};  {n(V / 231, 1)} gal")
V = cyl(30, 16)[2]
example("A storage tank is 30 ft across and 16 ft high. How many gallons does it hold?",
        [("r = 30 ÷ 2 = 15", "Halve the diameter."), (f"V = (3.14)(15)²(16) = (3.14)(225)(16) = {n(V)}", "Volume in cubic feet."),
         (f"{n(V)} × 7.48 = {n(V * 7.48)}", "Cubic feet to gallons: multiply by 7.48.")], f"{n(V * 7.48)} gal")
warn("Radius or diameter?",
     "Drawings usually give the **diameter**. LSA = πdh uses it as given, but πr² needs the **radius**, half of it. "
     "Using the diameter in πr²h makes the volume four times too large.")

# ===================================================================== 13.5
sec("13.5 Spheres")
p("A **sphere** is a ball: every point of its surface is the same distance from the center. It has no sides and no bases, so it has a single surface area.")
handout("SPHERES",
        "**SURFACE AREA**   (SA) = 4πr^{2}  *or*  (SA) = πd^{2}",
        "**VOLUME**   V = [[πd^{3}|6]]")
fig(figs.sphere3d("d"), "A sphere. Both handout formulas use the diameter d.", width="2.4in")
SA, V = sph(10)
example("A float ball is 10 in in diameter. Find its surface area and its volume to the nearest tenth.",
        [(f"SA = πd² = (3.14)(10)² = (3.14)(100) = {n(SA)}", "Diameter form of the surface area."),
         ("Check: 4πr² = 4(3.14)(5)² = 4(3.14)(25) = 314 ✓", "The radius form gives the same answer."),
         (f"V = [[πd³|6]] = [[(3.14)(10)³|6]] = [[3140|6]] = {tr(V)}…", "Cube the diameter: 10 × 10 × 10 = 1000."), (n(V, 1), "Round.")],
        f"SA = {u(SA, 'sq in')};  V = {n(V, 1)} cu in")
SA, V = sph(8)
example("A spherical tank is 8 ft in diameter. How many gallons does it hold, to the nearest tenth?",
        [(f"V = [[(3.14)(8)³|6]] = [[(3.14)(512)|6]] = [[{n(PI * 512)}|6]] = {tr(V)}…", "Volume in cubic feet. Keep every digit."),
         (f"{tr(V)}… × 7.48 = {tr(V * 7.48)}…", "Cubic feet to gallons."), (n(V * 7.48, 1), "Round only at the end.")], f"{n(V * 7.48, 1)} gal")
warn("Cube, do not triple", "d³ means d × d × d. For d = 8 that is 512, not 24.")

# ===================================================================== 13.6
sec("13.6 Pyramids")
p("A **pyramid** has one base and triangular sides that meet at a point. Two different lengths go up a pyramid, and each formula uses a different one.")
bullets(["The **height** (altitude) *h* goes straight down from the point to the center of the base. It is used for **volume**.",
         "The **slant length** *s* runs down the middle of a side face to the base. It is the height of each triangular side, and it is used for **LSA**."])
handout("PYRAMIDS",
        "*p*= perimeter of base   *s*= slant length of lateral face   *h*= altitude (height)   *A*= area of the base",
        "**LSA =** [[ps|2]]     **TSA = LSA + *A***     **V =** [[Ah|3]]",
        "**Triangle Pyramid**     **Square Pyramid**",
        "FOR THE AREA OF THE BASE, USE THE FORMULAS THAT MATCH THE SHAPE OF THE BASE")
fig(figs.side_by_side([figs.square_pyramid(12, 8, "s", "h", "side"), figs.tri_pyramid(18, 20)], gap=24),
    "A square pyramid and a triangle pyramid. The dashed line is the height h; the solid red line is the slant length s.")
p("Each side of a pyramid is a triangle whose base is one side of the pyramid’s base and whose height is *s*. Adding up those triangles gives *ps* ÷ 2. "
  "A pyramid has only **one** base, so TSA adds *A* once, not twice. And a pyramid holds exactly one third as much as a prism with the same base and height.")
LSA, TSA, V = pyramid(64, 256, 10, 6)
example("A square pyramid has base sides of 16 ft, a height of 6 ft and a slant length of 10 ft. Find its LSA, TSA and volume.",
        [("A = s² = (16)² = 256;  p = 4(16) = 64", "The base first."), (f"LSA = [[ps|2]] = [[(64)(10)|2]] = {n(LSA)}", "Slant length for the sides."),
         (f"TSA = LSA + A = {n(LSA)} + 256 = {n(TSA)}", "One base."), (f"V = [[Ah|3]] = [[(256)(6)|3]] = {n(V)}", "Height for the volume.")],
        f"LSA = {u(LSA, 'sq ft')};  TSA = {u(TSA, 'sq ft')};  V = {u(V, 'cu ft')}", title="Square pyramid")
A_ = 0.433 * 144
LSA, TSA, V = pyramid(36, A_, 10.6, 10)
example("A triangle pyramid has an equilateral base with 12-in sides. Its height is 10 in and its slant length is 10.6 in. Find its LSA, TSA and volume.",
        [(f"A = .433(12)² = .433(144) = {n(A_)};  p = 3(12) = 36", "Match the base formula to the shape of the base: an equilateral triangle."),
         (f"LSA = [[(36)(10.6)|2]] = {n(LSA)}", ""), (f"TSA = {n(LSA)} + {n(A_)} = {n(TSA)}", ""), (f"V = [[({n(A_)})(10)|3]] = {n(V)}", "")],
        f"LSA = {u(LSA, 'sq in')};  TSA = {u(TSA, 'sq in')};  V = {u(V, 'cu in')}", title="Triangle pyramid")
warn("Slant length for surface, height for volume",
     "The slant length is always longer than the height. Using *s* in the volume formula, or *h* in the LSA formula, is the most common pyramid mistake.")
sub("Finding a slant length")
p("In a square pyramid the height, half of a base side, and the slant length make a right triangle, with the slant length as the hypotenuse. "
  "So if the slant length is not given, the Pythagorean theorem from Chapter 11 supplies it: s = √(h² + (half the side)²).")
example("A square pyramid has base sides of 10 in and a height of 12 in. Find its slant length and its LSA.",
        [("half the side = 10 ÷ 2 = 5", ""), ("s = √(12² + 5²) = √(144 + 25) = √169 = 13", "Height and half-side are the legs."),
         ("LSA = [[(40)(13)|2]] = 260", "p = 4(10) = 40.")], "s = 13 in;  LSA = 260 sq in")

# ===================================================================== 13.7
sec("13.7 The frustum of a pyramid")
p("Cut the top off a pyramid with a level cut and what remains is a **frustum**: a larger base on the bottom, a smaller base on top, and sloping sides. "
  "Hoppers, duct transitions, chimney caps and concrete footings are frustums.")
handout("FRUSTUM OF A PYRAMID",
        "***Lateral Surface Area*** (LSA) = [[(P+ p) s|2]]     *P*.....*perimeter* of larger base     *p*.....*perimeter* of smaller base     *s*.....*slant length*",
        "***Total Surface Area*** (TSA) = LSA + A + a     A....*area* of larger base     a.....*area* of smaller base",
        "***Volume*** (V) = [[h(A + a + √(A * a))|3]]     *A*.....area of larger base     *a*.....area of smaller base     *h*.....(height)")
fig(figs.frustum3d(16, 10, 4, ("16 in", "10 in", "h", "s")), "A frustum with a 16-in square bottom and a 10-in square top. Each sloping side is a trapezoid.", width="3.4in")
shop("Every side of a frustum is a trapezoid",
     "Look at one sloping side of the frustum: its two parallel edges are a side of the bottom base and a side of the top base, and its height is the slant length. "
     "It is a trapezoid, and the LSA formula is nothing more than the trapezoid formula from Chapter 10 applied to all the sides at once.")
LSA, TSA, V = frustum(64, 40, 256, 100, 5, 4)
example("A sheet-metal hopper is a frustum. The bottom base is a square with 16-in sides, the top base is a square with 10-in sides, the height is 4 in and the slant length is 5 in. "
        "Find its LSA, TSA and volume.",
        [("P = 4(16) = 64;  p = 4(10) = 40", "Perimeters of the larger and smaller bases."),
         ("A = (16)² = 256;  a = (10)² = 100", "Areas of the larger and smaller bases."),
         (f"LSA = [[(64 + 40)(5)|2]] = [[(104)(5)|2]] = {n(LSA)}", "Add the perimeters, times the slant length, divide by 2."),
         ("Check: one side = [[(16 + 10)(5)|2]] = 65;  4 × 65 = 260 ✓", "Each side is a trapezoid with bases 16 and 10 and height 5."),
         (f"TSA = {n(LSA)} + 256 + 100 = {n(TSA)}", "Both bases."),
         ("√(A * a) = √((256)(100)) = √25,600 = 160", "Multiply the two areas, then take the square root."),
         (f"V = [[4(256 + 100 + 160)|3]] = [[4(516)|3]] = {n(V)}", "Height for the volume.")],
        f"LSA = {u(LSA, 'sq in')};  TSA = {u(TSA, 'sq in')};  V = {u(V, 'cu in')}")
V2 = frustum(80, 48, 400, 144, 0, 15)[2]
example("A concrete footing is a frustum 15 in high, with a 20-in square bottom and a 12-in square top. Find its volume and the number of gallons of space it fills, to the nearest tenth.",
        [("A = 400;  a = 144;  √((400)(144)) = √57,600 = 240", "Areas, then the root of their product."),
         (f"V = [[15(400 + 144 + 240)|3]] = [[15(784)|3]] = {n(V2)}", "Volume in cubic inches."),
         (f"{n(V2)} ÷ 231 = {tr(V2 / 231)}… → {n(V2 / 231, 1)}", "Cubic inches: divide by 231.")], f"V = {u(V2, 'cu in')};  {n(V2 / 231, 1)} gal")
tip("Keying the frustum volume",
    "Enter it in one line with the root in parentheses: `15 × (400 + 144 + √(400 × 144)) ÷ 3`. Without the parentheses around A × a, the calculator takes the root of 400 only.")

# ===================================================================== 13.8
sec("13.8 Density and weight")
handout("DENSITY",
        "**DENSITY** IS A MEASURE OF MASS PER VOLUME. THE AVERAGE **DENSITY** OF AN OBJECT EQUALS ITS TOTAL MASS DIVIDED BY ITS TOTAL VOLUME. "
        "IT IS COMMONLY EXPRESSED IN TERMS OF: LBS. per CUBIC INCH (**lbs./in.^{3}**) or GRAMS per CUBIC CM. (**g/cm^{3}**).",
        "To determine the total weight of an object, **multiply the total volume of the object by its density.**",
        "**EX: Calculate the weight of the stainless-steel rod if it has a density of 0.285 lbs/cu. in. It is 60 inches long with a diameter of 4 inches.**",
        "*Vol* = πr^{2}h     *Vol* = 3.14 x 2^{2} x 60     *Vol* = 753.6 cubic inches     **Weight = 753.6 x .285  = 214.8 lbs.**")
rule("Weight from density", "weight = volume × density",
     "The volume must be in the same cubic unit as the density. A density in pounds per **cubic inch** needs a volume in **cubic inches**.")
table(["Material", "Density, lb per cu in", "Material", "Density, lb per cu in"],
      [["aluminum", "0.098", "copper", "0.323"], ["brass", "0.307", "lead", "0.410"], ["cast iron", "0.260", "steel", "0.284"],
       ["stainless steel", "0.285", "titanium", "0.16"]], caption="Table 13.2  Approximate densities of common metals", small=True)
W1 = 24 * 12 * 0.5 * 0.098
example("An aluminum plate is 24 in by 12 in by [[1|2]] in thick. Aluminum weighs 0.098 lb per cu in. Find the weight to the nearest tenth of a pound.",
        [("V = (24)(12)(0.5) = 144 cu in", "A plate is a rectangular prism."), (f"weight = (144)(0.098) = {n(W1)}", "Volume times density."), (n(W1, 1), "")],
        f"{n(W1, 1)} lb")
Vb = PI * 1 * 72
example("A copper round bar is 2 in in diameter and 6 ft long. Copper weighs 0.323 lb per cu in. Find its weight to the nearest tenth of a pound.",
        [("6 ft × 12 = 72 in", "The density is per cubic **inch**, so the length must be in inches first."),
         (f"V = πr²h = (3.14)(1)²(72) = {n(Vb)} cu in", "Radius = 1 in."), (f"weight = ({n(Vb)})(0.323) = {tr(Vb * 0.323)}…", ""), (n(Vb * 0.323, 1), "")],
        f"{n(Vb * 0.323, 1)} lb", title="Convert the length first")
warn("Feet and cubic inches do not mix",
     "A bar “8 feet” long with a density in lb per cu in must be worked with h = 96 in. Using h = 8 makes the weight twelve times too small.")
Vh = 2.6 * 36
example("A brass hexagonal bar has sides of 1 in and is 36 in long. Brass weighs 0.307 lb per cu in. Find its weight to the nearest tenth.",
        [("A = 2.6(1)² = 2.6", "Hexagon base."), (f"V = (2.6)(36) = {n(Vh)} cu in", "Prism volume."), (f"weight = ({n(Vh)})(0.307) = {n(Vh * 0.307)} → {n(Vh * 0.307, 1)}", "")],
        f"{n(Vh * 0.307, 1)} lb")

# ===================================================================== 13.9
sec("13.9 Solving for a missing dimension")
p("A volume formula can be run backward, exactly as in Chapter 9. Substitute everything that is known, simplify, and undo what has been done to the unknown. "
  "When the unknown is a radius, it is squared, so the last step is a square root.")
h_ = 12000 / (PI * 225)
example("What is the height of a cylinder with a volume of 12,000 cubic feet and a radius of 15 feet? Round to the tenth.",
        [("V = πr²h", "Formula."), ("12,000 = (3.14)(15)²h", "Substitute."), ("12,000 = 706.5h", "Simplify: (3.14)(225) = 706.5."),
         (f"h = 12,000 ÷ 706.5 = {tr(h_)}…", "Divide both sides."), (n(h_, 1), "Round to the tenth.")], f"{n(h_, 1)} ft", title="Finding a height")
example("What is the radius of a cylinder with a volume of 9,420 cubic feet and a height of 30 feet? Round to the tenth.",
        [("9,420 = (3.14)r²(30)", "Substitute."), ("9,420 = 94.2r²", "Simplify: (3.14)(30) = 94.2."), ("r² = 9,420 ÷ 94.2 = 100", "Divide both sides by 94.2."),
         ("r = √100 = 10.0", "Undo the square with a square root.")], "10.0 ft", title="Finding a radius")
hg = 500 / 7.48 / 12
example("A rectangular tank with a 4 ft by 3 ft base must hold 500 gallons. How tall must it be, to the nearest tenth of a foot?",
        [(f"500 ÷ 7.48 = {tr(500 / 7.48)}… cu ft", "Gallons back to cubic feet: divide by 7.48."), ("A = (4)(3) = 12", "Area of the base."),
         (f"h = V ÷ A = {tr(500 / 7.48)}… ÷ 12 = {tr(hg)}…", "V = Ah, so h = V ÷ A."), (n(hg, 1), "")], f"{n(hg, 1)} ft")
table(["Solid", "To find h", "To find r"],
      [["cylinder", "h = [[V|πr²]]", "r = √([[V|πh]])"], ["prism", "h = [[V|A]]", ""], ["pyramid", "h = [[3V|A]]", ""]],
      caption="Table 13.3  Volume formulas run backward", widths=[30, 35, 35])

# ===================================================================== practice
q = []
for L_, W_, H_, un in [(5, 3, 4, "ft"), (8, 6, 10, "in"), (12, 4, 3, "ft"), (2.5, 2, 6, "ft")]:
    pp_, a_, l_, t_, v_ = rect_prism(L_, W_, H_)
    q.append((f"Rectangular prism {n(L_)} {un} by {n(W_)} {un} base, {n(H_)} {un} high. Find LSA, TSA and V.",
              f"LSA = {n(l_)} sq {un}; TSA = {n(t_)} sq {un}; V = {n(v_)} cu {un}"))
for s_, H_ in [(14, 40), (9, 25)]:
    pp_, a_, l_, t_, v_ = rect_prism(s_, s_, H_)
    q.append((f"Square base prism, base sides {s_} in, height {H_} in. Find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"))
for s_, H_ in [(10, 36), (5, 18), (7, 40)]:
    pp_, a_, l_, t_, v_ = tri_prism(s_, H_)
    q.append((f"Equilateral triangle prism, base sides {s_} in, length {H_} in. Find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"))
for s_, H_ in [(6, 24), (3, 15), (10, 30)]:
    pp_, a_, l_, t_, v_ = hex_prism(s_, H_)
    q.append((f"Hexagonal prism, base sides {s_} in, height {H_} in. Find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"))
practice("Prisms", "Find the base area and perimeter first. Do not round.", q, cols=1)

q = [("A tank is 48 in by 24 in by 20 in. How many gallons does it hold, to the nearest tenth?", n(48 * 24 * 20 / 231, 1) + " gal"),
     ("A tank is 5 ft by 4 ft by 2.5 ft. How many gallons does it hold?", n(50 * 7.48) + " gal"),
     ("A duct section is 12 in by 12 in by 60 in. How many gallons of space is that, to the nearest tenth?", n(12 * 12 * 60 / 231, 1) + " gal"),
     ("A pan is 30 in by 18 in by 2 in. How many gallons does it hold, to the nearest tenth?", n(30 * 18 * 2 / 231, 1) + " gal"),
     ("A pit is 10 ft by 8 ft by 6 ft. How many gallons does it hold?", n(480 * 7.48) + " gal"),
     ("A hexagonal tank has 2-ft sides and is 5 ft tall. How many gallons does it hold, to the nearest tenth?", n(2.6 * 4 * 5 * 7.48, 1) + " gal"),
     ("A triangle prism trough has 18-in sides and is 96 in long. How many gallons does it hold, to the nearest tenth?", n(0.433 * 324 * 96 / 231, 1) + " gal"),
     ("A tank holds 80 cu ft. How many gallons is that?", n(80 * 7.48) + " gal")]
practice("Gallons", "Round to the nearest tenth where the problem says.", q, cols=1)

q = []
for d_, h_, un in [(18, 42, "in"), (12, 30, "in"), (8, 10, "ft"), (24, 36, "in")]:
    l_, t_, v_ = cyl(d_, h_)
    q.append((f"Cylinder: d = {d_} {un}, h = {h_} {un}. Find LSA, TSA and V.", f"LSA = {n(l_)} sq {un}; TSA = {n(t_)} sq {un}; V = {n(v_)} cu {un}"))
q += [(f"Cylinder: d = 14 in, h = 40 in. Find V and the gallons, to the nearest tenth.", f"V = {n(cyl(14, 40)[2])} cu in; {n(cyl(14, 40)[2] / 231, 1)} gal"),
      (f"Cylinder: d = 50 ft, h = 20 ft. Find V and the gallons.", f"V = {n(cyl(50, 20)[2])} cu ft; {n(cyl(50, 20)[2] * 7.48)} gal")]
for d_, un in [(6, "in"), (20, "in"), (3, "ft"), (5, "ft")]:
    sa, vv = sph(d_)
    q.append((f"Sphere: d = {d_} {un}. Find SA and V, to the nearest tenth.", f"SA = {n(sa, 1)} sq {un}; V = {n(vv, 1)} cu {un}"))
q += [("Sphere: d = 18 in. Find the gallons it holds, to the nearest tenth.", n(sph(18)[1] / 231, 1) + " gal"),
      ("Sphere: d = 6 ft. Find the gallons it holds, to the nearest tenth.", n(sph(6)[1] * 7.48, 1) + " gal")]
practice("Cylinders and spheres", "Use π = 3.14.", q, cols=1)

q = []
for a_, h_, s_ in [(10, 12, 13), (12, 8, 10), (30, 20, 25), (6, 4, 5)]:
    l_, t_, v_ = pyramid(4 * a_, a_ * a_, s_, h_)
    q.append((f"Square pyramid: base sides {a_} in, height {h_} in, slant length {s_} in. Find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"))
for a_, h_, s_ in [(9, 12, 12.3), (24, 30, 30.8)]:
    l_, t_, v_ = pyramid(3 * a_, 0.433 * a_ * a_, s_, h_)
    q.append((f"Triangle pyramid: equilateral base with {a_}-ft sides, height {h_} ft, slant length {s_} ft. Find LSA, TSA and V.",
              f"LSA = {n(l_)} sq ft; TSA = {n(t_)} sq ft; V = {n(v_)} cu ft"))
q.append(("A square pyramid has base sides of 16 in and a height of 15 in. Find its slant length.", "17 in"))
for A1, a1, h_, s_ in [(14, 8, 4, 5), (20, 10, 12, 13), (30, 18, 8, 10)]:
    l_, t_, v_ = frustum(4 * A1, 4 * a1, A1 * A1, a1 * a1, s_, h_)
    q.append((f"Frustum: bottom square {A1} in, top square {a1} in, height {h_} in, slant length {s_} in. Find LSA, TSA and V.",
              f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"))
V3 = frustum(0, 0, 900, 324, 0, 20)[2]
q.append(("Frustum: bottom square 30 in, top square 18 in, height 20 in. Find V and the gallons, to the nearest tenth.", f"V = {n(V3)} cu in; {n(V3 / 231, 1)} gal"))
practice("Pyramids and frustums", "Use the slant length for surface area and the height for volume.", q, cols=1)

q = [("A steel bar is 2 in by 3 in by 48 in. Steel weighs 0.284 lb per cu in. Find its weight to the nearest tenth.", n(288 * 0.284, 1) + " lb"),
     ("An aluminum round bar is 3 in in diameter and 40 in long (0.098 lb per cu in). Find its weight to the nearest tenth.", n(cyl(3, 40)[2] * 0.098, 1) + " lb"),
     ("A brass round bar is 1.5 in in diameter and 4 ft long (0.307 lb per cu in). Find its weight to the nearest tenth.", n(cyl(1.5, 48)[2] * 0.307, 1) + " lb"),
     ("A lead sphere is 4 in in diameter (0.410 lb per cu in). Find its weight to the nearest tenth.", n(sph(4)[1] * 0.41, 1) + " lb"),
     ("A cast-iron plate is 18 in by 18 in by 1 in (0.260 lb per cu in). Find its weight to the nearest tenth.", n(324 * 0.26, 1) + " lb"),
     ("A copper hexagonal bar has 0.5-in sides and is 30 in long (0.323 lb per cu in). Find its weight to the nearest tenth.", n(2.6 * 0.25 * 30 * 0.323, 1) + " lb"),
     ("A stainless-steel shaft is 2 in in diameter and 3 ft long (0.285 lb per cu in). Find its weight to the nearest tenth.", n(cyl(2, 36)[2] * 0.285, 1) + " lb"),
     ("A titanium bar is 5 in in diameter and 30 in long (0.16 lb per cu in). Find its weight to the nearest tenth.", n(cyl(5, 30)[2] * 0.16, 1) + " lb")]
practice("Density", "Volume times density. Change feet to inches first. Round to the nearest tenth.", q, cols=1)

q = [("What is the height of a cylinder with a volume of 15,000 cubic feet and a radius of 25 feet? Round to the tenth.", n(15000 / (PI * 625), 1) + " ft"),
     ("What is the height of a cylinder with a volume of 5,000 cubic inches and a radius of 8 inches? Round to the tenth.", n(5000 / (PI * 64), 1) + " in"),
     ("What is the radius of a cylinder with a volume of 18,840 cubic feet and a height of 15 feet? Round to the tenth.", n(sqrt(18840 / (PI * 15)), 1) + " ft"),
     ("What is the radius of a cylinder with a volume of 2,000 cubic inches and a height of 20 inches? Round to the tenth.", n(sqrt(2000 / (PI * 20)), 1) + " in"),
     ("A prism has a volume of 840 cu in and a base area of 35 sq in. Find its height.", "24 in"),
     ("A square pyramid has a volume of 1,200 cu ft and a base 15 ft on a side. Find its height.", n(3 * 1200 / 225) + " ft"),
     ("A rectangular tank with a 5 ft by 4 ft base must hold 1,000 gallons. How tall must it be, to the nearest tenth?", n(1000 / 7.48 / 20, 1) + " ft"),
     ("A cylindrical tank 6 ft in diameter must hold 2,000 gallons. How tall must it be, to the nearest tenth?", n(2000 / 7.48 / (PI * 9), 1) + " ft")]
practice("Solving", "Round to the tenth.", q, cols=1)

summary(["LSA is the sides, TSA is the sides and the base(s), and V is the space contained. Areas are square units; volume is cubic units.",
         "Find the base area A and the base perimeter p first.",
         "Prisms: LSA = ph, TSA = LSA + 2A, VOL = Ah. Cylinders: LSA = πdh, TSA = LSA + 2πr², V = πr²h.",
         "Spheres: SA = 4πr² or πd², V = πd³ ÷ 6.",
         "Pyramids: LSA = ps ÷ 2, TSA = LSA + A, V = Ah ÷ 3. Slant length for surface, height for volume.",
         "Frustums: LSA = (P + p)s ÷ 2, TSA = LSA + A + a, V = h(A + a + √(A × a)) ÷ 3. Each side is a trapezoid.",
         "Gallons: cubic inches ÷ 231; cubic feet × 7.48. Weight = volume × density."])

rv = []
pp_, a_, l_, t_, v_ = rect_prism(6, 4, 5)
rv += [("Rectangular prism 6 ft by 4 ft base, 5 ft high: find LSA.", u(l_, "sq ft")), ("Same prism: find TSA.", u(t_, "sq ft")), ("Same prism: find V and the gallons.", f"{u(v_, 'cu ft')}; {n(v_ * 7.48)} gal")]
pp_, a_, l_, t_, v_ = tri_prism(12, 20)
rv += [("Equilateral triangle prism, 12-in sides, 20 in long: find A and p of the base.", f"A = {n(a_)} sq in; p = 36 in"), ("Same prism: find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in")]
pp_, a_, l_, t_, v_ = hex_prism(8, 25)
rv += [("Hexagonal prism, 8-in sides, 25 in tall: find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in")]
l_, t_, v_ = cyl(16, 30)
rv += [("Cylinder d = 16 in, h = 30 in: find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"),
       ("Same cylinder: how many gallons, to the nearest tenth?", n(v_ / 231, 1) + " gal")]
sa, vv = sph(12)
rv += [("Sphere d = 12 in: find SA and V.", f"SA = {n(sa)} sq in; V = {n(vv)} cu in"), ("Sphere d = 4 ft: find the gallons, to the nearest tenth.", n(sph(4)[1] * 7.48, 1) + " gal")]
l_, t_, v_ = pyramid(80, 400, 26, 24)
rv += [("Square pyramid: base 20 ft, height 24 ft, slant length 26 ft. Find LSA, TSA and V.", f"LSA = {n(l_)} sq ft; TSA = {n(t_)} sq ft; V = {n(v_)} cu ft")]
l_, t_, v_ = frustum(48, 24, 144, 36, 5, 4)
rv += [("Frustum: bottom square 12 in, top square 6 in, height 4 in, slant 5 in. Find LSA, TSA and V.", f"LSA = {n(l_)} sq in; TSA = {n(t_)} sq in; V = {n(v_)} cu in"),
       ("Find the area of one side of the frustum in the previous problem using the trapezoid formula.", "(12 + 6)(5) ÷ 2 = 45 sq in"),
       ("A steel rod (0.284 lb per cu in) is 2 in in diameter and 5 ft long. Find its weight to the nearest tenth.", n(cyl(2, 60)[2] * 0.284, 1) + " lb"),
       ("What is the height of a cylinder with a volume of 25,000 cu ft and a radius of 20 ft? Round to the tenth.", n(25000 / (PI * 400), 1) + " ft"),
       ("What is the radius of a cylinder with a volume of 47,100 cu ft and a height of 15 ft? Round to the tenth.", n(sqrt(47100 / (PI * 15)), 1) + " ft"),
       ("Which length is used in a pyramid’s volume formula, the slant length or the height?", "the height"),
       ("A student writes the TSA of a box as 62 ft³. What is wrong?", "TSA is an area, so the unit is ft² (sq ft)."),
       ("Why does a pyramid’s TSA add A once while a prism’s adds 2A?", "A pyramid has one base; a prism has two."),
       ("A volume is 4,620 cu in. How many gallons is that?", "20 gal")]
review(rv)

# the Part 4 cumulative review now follows this chapter
x4.part4(extra=[("Rectangular prism 5 ft by 3 ft base, 4 ft high: find TSA and V.", "TSA = 94 sq ft; V = 60 cu ft"),
                ("Cylinder d = 10 in, h = 24 in: find V and the gallons to the nearest tenth.", f"V = {n(cyl(10, 24)[2])} cu in; {n(cyl(10, 24)[2] / 231, 1)} gal"),
                ("Sphere d = 9 in: find SA and V to the nearest tenth.", f"SA = {n(sph(9)[0], 1)} sq in; V = {n(sph(9)[1], 1)} cu in"),
                ("Square pyramid: base 12 in, height 8 in, slant 10 in. Find TSA and V.", "TSA = 384 sq in; V = 384 cu in"),
                ("Frustum: bottom square 10 in, top square 4 in, height 4 in, slant 5 in. Find V.", n(frustum(0, 0, 100, 16, 0, 4)[2]) + " cu in"),
                ("A copper bar (0.323 lb per cu in) is 1 in in diameter and 3 ft long. Find its weight to the nearest tenth.", n(cyl(1, 36)[2] * 0.323, 1) + " lb")])
