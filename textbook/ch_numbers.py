"""Part 1: numbers (place value, rounding, fractions, decimals, percents)."""
from fractions import Fraction
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr, F, frtxt
import figs

PLACES = {"millions": 6, "hundred thousands": 5, "ten thousands": 4, "thousands": 3, "hundreds": 2, "tens": 1, "ones": 0,
          "tenths": -1, "hundredths": -2, "thousandths": -3, "ten-thousandths": -4}
NEAREST = {"thousand": 3, "hundred": 2, "ten": 1, "whole number": 0, "tenth": -1, "hundredth": -2, "thousandth": -3}


def digit(num, place):
    whole, dec = num.replace(",", "").split(".")
    k = PLACES[place]
    return whole[len(whole) - 1 - k] if k >= 0 else dec[-k - 1]


def rs(num, nearest):
    k = NEAREST[nearest]
    v = rnd(float(num.replace(",", "")), -k)
    return n(v, max(0, -k))


part("Part 1 · Numbers", "Every measurement, price and specification is a number written in the base ten system. "
     "Part 1 makes sure those numbers are read, rounded and rewritten correctly before any calculating begins.")

# =====================================================================  1
chapter("Place Value and Rounding",
        ["Name the place value of any digit, from millions down to ten-thousandths.",
         "Read and write decimal numbers the way they are spoken in a shop.",
         "Compare two decimals and say which is larger.",
         "Round any number to a named place using the five-step rule.",
         "Decide how far to round from the wording of a problem."],
        "A micrometer reads 0.3175 inch. A blueprint calls for 0.318. Are they the same? The answer depends on "
        "knowing what each digit is worth and how rounding works. This chapter is the foundation for everything else in the book.",
        [("digit", "One of the ten symbols 0 to 9."),
         ("place value", "What a digit is worth because of where it sits in the number."),
         ("decimal point", "The dot that separates the whole-number part from the part smaller than one."),
         ("rounding digit", "The digit in the place you are rounding to."),
         ("test digit", "The digit just to the right of the rounding digit. It decides whether to round up.")])

sec("1.1 The base ten system")
p("Our number system uses only ten digits, yet it can write any amount. It does this by giving each *position* in a "
  "number its own value. Moving one place to the left makes a digit worth **ten times as much**. Moving one place to the "
  "right makes it worth **one tenth as much**. That single idea runs straight through the decimal point without changing.")
fig(figs.place_value("3528416", "7359"), "Base 10 place values, shown with the number 3,528,416.7359.")
p("In the number above, the digit 5 sits in the hundred thousands place, so it is worth 500,000. Another 5 sits in the "
  "thousandths place and is worth only 0.005. Same digit, very different value.")
rule("Whole-number places end in s; decimal places end in ths",
     "To the **left** of the decimal point: ones, tens, hundreds, thousands, ten thousands, hundred thousands, millions.",
     "To the **right** of the decimal point: tenths, hundredths, thousandths, ten-thousandths.",
     "There is no “oneths” place. The first place to the right of the point is tenths.")
example("In the number 902,468.7351, name the digit in the (a) ten thousands place, (b) hundredths place, (c) ten-thousandths place.",
        [("902,468 **.** 7351", "Find the decimal point first. Every place is counted from it."),
         ("9 0 2, 4 6 8 → ones 8, tens 6, hundreds 4, thousands 2, ten thousands **0**", "Count left from the point: ones, tens, hundreds, thousands, ten thousands."),
         ("7 3 5 1 → tenths 7, hundredths **3**", "Count right from the point: tenths, hundredths."),
         ("thousandths 5, ten-thousandths **1**", "Keep counting right for the last two places.")],
        "(a) 0   (b) 3   (c) 1")
warn("A zero is still a digit",
     "In 902,468.7351 the ten thousands digit is 0. A zero holds its place so that the 9 stays in the hundred thousands "
     "place. Never skip over a zero when counting places.")

sec("1.2 Reading and writing decimals")
p("A decimal is read in three parts: the whole number, the word **and** for the decimal point, then the decimal part "
  "read as if it were a whole number followed by the name of its **last** place.")
table(["Number", "Read as"],
      [["0.7", "seven tenths"], ["0.25", "twenty-five hundredths"], ["3.125", "three and one hundred twenty-five thousandths"],
       ["12.06", "twelve and six hundredths"], ["0.0625", "six hundred twenty-five ten-thousandths"]], widths=[25, 75])
shop("How decimals are spoken in a machine shop",
     "Machinists measure in thousandths of an inch, so they read almost everything in thousandths. The dimension 0.250 in "
     "is “two hundred fifty thousandths,” and 0.0005 in is “five tenths” (short for five tenths of a thousandth). "
     "The value has not changed, only the way it is said.")
p("Zeros written at the right-hand end of a decimal do not change its value: 0.5, 0.50 and 0.500 are the same amount. "
  "On a drawing, however, the extra zeros tell the reader how precisely the part must be made, so copy them exactly.")

sec("1.3 Comparing decimals")
p("To decide which of two decimals is larger, line up the decimal points and compare digit by digit from the left. "
  "The first place where the digits differ settles it. Filling in zeros so that both numbers have the same number of "
  "decimal places makes the comparison easy to see.")
example("Which is larger, 0.8125 or 0.813?",
        [("0.8125<br>0.8130", "Write both with four decimal places. Adding a zero to 0.813 does not change it."),
         ("0.81**2**5<br>0.81**3**0", "The tenths (8) and hundredths (1) match. The thousandths differ: 2 against 3."),
         ("3 &gt; 2", "The number with the larger digit in that place is the larger number.")],
        "0.813 is larger.")
warn("More digits does not mean a bigger number",
     "0.8125 has more digits than 0.813 but it is the smaller number. Length only matters for whole numbers.")

practice("Place value", "For problems 1 to 10 use the number 4,107,538.2069. Name the digit in each place. "
         "For 11 to 16, tell which number is larger.",
         [(f"the {pl} place", digit("4,107,538.2069", pl)) for pl in
          ["thousands", "tenths", "ten-thousandths", "millions", "hundredths", "ten thousands", "ones", "thousandths",
           "hundred thousands", "tens"]]
         + [(f"{a} or {b}", n(max(a, b))) for a, b in
            [(0.5, 0.45), (0.062, 0.0625), (1.3, 1.29), (0.4375, 0.44), (2.005, 2.05), (0.75, 0.705)]], cols=3)

sec("1.4 Rounding")
p("Rounding replaces a number with a nearby number that is easier to use. A tape measure cannot show 37.4286 inches, "
  "and a supplier will not sell 71,428.57 psi steel. The question is always the same: **which round value is the number closest to?**")
fig(figs.rounding_line(9370, 9380, 9372.6, "9370", "9380", "9372.6"),
    "Rounding 9372.6 to the nearest ten. It lies between 9370 and 9380, and it is closer to 9370.")
handout("The Basic Rules",
        "**1. Identify the rounding digit:** Find the digit in the place value you want to round to",
        "**2. Look at the next digit:** Examine the digit immediately to the right of your rounding digit.",
        "**3. Round Up (Increase by One):** If the digit to the right is 5, 6, 7, 8, or 9, increase the rounding digit by one.",
        "**4. (Keep it the Same):** If the digit to the right is 0, 1, 2, 3, or 4, leave the rounding digit as it is.",
        "**5. Replace Remaining Digits:** Change all digits to the right of the rounded digit to zeros (for whole numbers) or drop them (for decimals).")
p("In this book the digit to the right of the rounding digit is also called the **test digit**, because it decides which way to round.")
example("Round 9372.6485 to the nearest (a) ten, (b) hundredth, (c) thousand.",
        [("93**7**2.6485 → test digit 2", "(a) The tens digit is 7. The digit to its right is 2, which is 4 or less, so the 7 stays."),
         ("9370", "The ones digit becomes a zero and the decimal part is dropped."),
         ("9372.6**4**85 → test digit 8", "(b) The hundredths digit is 4. The test digit 8 is 5 or more, so the 4 becomes 5."),
         ("9372.65", "Everything after the hundredths place is dropped."),
         ("**9**372.6485 → test digit 3", "(c) The thousands digit is 9. The test digit 3 leaves it alone."),
         ("9000", "The three whole-number places after it become zeros.")],
        "(a) 9370   (b) 9372.65   (c) 9000")
example("Round 4.3972 to the nearest hundredth.",
        [("4.3**9**72 → test digit 7", "The hundredths digit is 9 and the test digit says round up."),
         ("9 + 1 = 10", "Adding one to 9 makes ten, so write 0 and carry 1 to the tenths place."),
         ("4.40", "The tenths digit 3 becomes 4. Keep the zero: it shows the number was rounded to hundredths.")],
        "4.40", title="When the rounding digit is 9")
warn("Round once, from the original number",
     "To round 2.3491 to the nearest tenth, the test digit is 4, so the answer is 2.3. Do not round in stages "
     "(2.3491 → 2.35 → 2.4). Rounding twice gives the wrong answer.")
p("The names used for rounding places vary. All of these mean the same thing:")
table(["The problem says", "Round to this place", "Decimal places kept"],
      [["nearest whole number, nearest unit, nearest one", "ones", "0"], ["nearest tenth, nearest 10th, one decimal place", "tenths", "1"],
       ["nearest hundredth, nearest 100th, two decimal places", "hundredths", "2"],
       ["nearest thousandth, three decimal places", "thousandths", "3"], ["nearest ten", "tens", "none; ends in 0"],
       ["nearest hundred", "hundreds", "none; ends in 00"]], widths=[46, 27, 27])
warn("Ten or tenth? Hundred or hundredth?",
     "Read the last three letters. “Nearest **hundred**” rounds 3925 to 3900. “Nearest **hundredth**” rounds 3.925 to 3.93. "
     "Mixing these up is one of the most common ways to lose points on a correct calculation.")
tip("Let the calculator do the arithmetic, not the rounding",
    "Write down more digits than you need from the display, then round by hand using the five steps. Keep the full "
    "number in the calculator if the result is needed for another step: rounding in the middle of a problem can change the final answer.")

nums = [("638.2749", "tenth"), ("638.2749", "hundredth"), ("638.2749", "ten"), ("638.2749", "hundred"),
        ("15,862.0953", "thousand"), ("15,862.0953", "thousandth"), ("15,862.0953", "whole number"), ("15,862.0953", "tenth"),
        ("0.9968", "hundredth"), ("0.9968", "tenth"), ("7,449.5", "whole number"), ("7,449.5", "hundred"),
        ("86.0451", "hundredth"), ("249.96", "tenth"), ("3,925", "hundred"), ("71,428.57", "hundred"),
        ("55.901", "whole number"), ("0.04449", "thousandth")]
practice("Rounding", "Round each number to the place named.",
         [(f"{a} to the nearest {b}", rs(a, b)) for a, b in nums], cols=2)

sec("1.5 How far should an answer be rounded?")
p("In this course the problem always says. Look for the instruction in parentheses or at the top of the page, and "
  "follow it exactly. When there is no instruction, give the full answer.")
bullets(["**“Round to the nearest tenth if needed”** means: if the answer comes out even (139.5) or whole (3456), leave it alone. Round only if there are more digits than asked for.",
         "**“Give a non-rounded decimal or a fraction in lowest terms”** means rounding is not allowed. Write every digit, or use a fraction.",
         "**“Nearest whole number”** in a counting problem (how many pipes, how many sheets) may really mean *round up*, because 15.6 pipes cannot be bought. The problem will say if it wants that."])
shop("Rounding costs money",
     "A concrete order of 92.59 cubic yards rounded *down* to 92 leaves the pour short. Rounded to the nearest tenth it is 92.6. "
     "On the job, know whether being a little over or a little under is the safer mistake.")

summary(["Each place is worth ten times the place to its right. Places left of the point end in **s**; places right of it end in **ths**.",
         "To compare decimals, line up the points and compare from the left.",
         "To round: find the rounding digit, look only at the next digit, 5 or more rounds up, 4 or less stays.",
         "After rounding, whole-number places fill with zeros and decimal places are dropped.",
         "Round once, at the end, and only as far as the problem says."])

review([(f"In 6,052,917.3084, which digit is in the {pl} place?", digit("6,052,917.3084", pl)) for pl in
        ["hundredths", "ten thousands", "thousandths", "hundred thousands", "ten-thousandths", "tenths"]]
       + [(f"Round 5,274.9638 to the nearest {b}.", rs("5,274.9638", b)) for b in
          ["tenth", "hundred", "thousandth", "whole number", "ten", "hundredth"]]
       + [("Which is larger, 0.3125 or 0.32?", "0.32"), ("Which is smaller, 1.07 or 1.068?", "1.068"),
          ("Write in digits: forty-two and seven hundredths.", "42.07"),
          ("Write in digits: three hundred seventy-five thousandths.", "0.375"),
          ("A calculation gives 2,866.2 rpm. Round to the nearest hundred rpm.", rs("2,866.2", "hundred") + " rpm"),
          ("A calculation gives 7.4667 microfarads. Round to the nearest hundredth.", rs("7.4667", "hundredth") + " µF"),
          ("A student rounds 6.2481 to the nearest tenth and writes 6.3. What went wrong, and what is the answer?",
           "The student rounded twice (6.2481 → 6.25 → 6.3). The test digit is 4, so the answer is 6.2."),
          ("Round 19.996 to the nearest hundredth.", "20.00")])

# =====================================================================  2
chapter("Fractions, Decimals and Percents",
        ["Reduce a fraction to lowest terms and change between improper fractions and mixed numbers.",
         "Change a fraction to a decimal and a decimal to a fraction.",
         "Change a decimal to a percent and a percent to a decimal.",
         "Move freely among all three forms and recognize the common shop equivalents.",
         "Add and subtract measurements that mix fractions and decimals."],
        "Five-eighths of an inch, 0.625 inch and 62.5% of an inch are the same length written three ways. Tape measures "
        "use fractions, calculators use decimals, and specifications use percents. A technician has to translate among them without hesitation.",
        [("numerator", "The top number of a fraction: how many parts are counted."),
         ("denominator", "The bottom number: how many equal parts make one whole."),
         ("lowest terms", "A fraction whose top and bottom share no common factor except 1."),
         ("mixed number", "A whole number and a fraction together, such as 2 [[3|8]]."),
         ("improper fraction", "A fraction whose top is as large as or larger than its bottom, such as [[19|8]]."),
         ("percent", "Parts out of one hundred. 25% means 25 out of every 100.")])

sec("2.1 Fractions in lowest terms")
p("A fraction names part of a whole. The **denominator** says how many equal parts the whole was cut into, and the "
  "**numerator** says how many of those parts are being counted. On an inch ruler cut into sixteenths, the mark "
  "[[12|16]] is the same mark as [[6|8]] and [[3|4]]. All three are **equivalent fractions**, but only [[3|4]] is in lowest terms.")
rule("Reducing to lowest terms",
     "Divide the top and the bottom by the same number, and keep going until no number divides both.",
     "Ruler fractions have denominators 2, 4, 8, 16, 32 and 64, so for them the rule is short: "
     "**keep halving top and bottom until the top is odd.**")
example("Reduce [[20|32]] to lowest terms.",
        [("[[20|32]] = [[20 ÷ 2|32 ÷ 2]] = [[10|16]]", "Both are even, so divide both by 2."),
         ("[[10|16]] = [[5|8]]", "Still both even. Divide by 2 again."),
         ("[[5|8]]", "The top is odd, so the fraction is in lowest terms.")], "[[5|8]]")
sub("Mixed numbers and improper fractions")
p("A measurement such as 2 [[3|8]] inches is a **mixed number**. For multiplying and dividing it is easier to use the "
  "**improper fraction** [[19|8]]. Both say the same thing: nineteen eighths.")
eq("Mixed → improper:   2 [[3|8]] = [[2 × 8 + 3|8]] = [[19|8]]     (whole × bottom + top, over the same bottom)",
   "Improper → mixed:   [[19|8]] = 19 ÷ 8 = 2 remainder 3 = 2 [[3|8]]     (divide; the remainder goes on top)")

fracs = ["6/8", "12/16", "10/32", "24/64", "14/16", "28/32", "36/64", "4/16"]
practice("Fractions", "Reduce 1 to 8 to lowest terms. Write 9 to 12 as improper fractions and 13 to 16 as mixed numbers.",
         [(frtxt(f), fr(Fraction(f))) for f in fracs]
         + [(frtxt(m), "[[%d|%d]]" % (F(m).numerator, F(m).denominator)) for m in ["1 3/4", "2 5/8", "3 7/16", "5 1/2"]]
         + [(frtxt(m), fr(Fraction(m))) for m in ["11/8", "9/4", "37/16", "45/32"]], cols=4)

sec("2.2 Fraction to decimal")
p("The fraction bar is a division sign. To change any fraction to a decimal, do the division it shows.")
rule("Fraction → decimal", "Divide the top by the bottom.", "[[5|8]] = 5 ÷ 8 = 0.625")
p("For a mixed number, keep the whole number and convert only the fraction: 3 [[5|8]] = 3 + 0.625 = 3.625. "
  "Some divisions never end. [[1|3]] = 0.3333… and [[1|6]] = 0.1666… For those, round as the problem directs.")
example("Change 31 [[3|8]] in to a decimal.",
        [("3 ÷ 8 = 0.375", "Divide the top of the fraction by the bottom."),
         ("31 + 0.375 = 31.375", "Put the whole number back in front.")], "31.375 in")
tip("Entering a mixed number",
    "On any calculator, 31 [[3|8]] can be keyed as `31 + 3 ÷ 8`. The calculator divides before it adds, so the answer is 31.375. "
    "Inside a longer calculation, put it in parentheses: `(31 + 3 ÷ 8)`.")

sec("2.3 Decimal to fraction")
p("Read the decimal by its place value and write exactly what you say. Then reduce.")
rule("Decimal → fraction",
     "Write the digits after the point over 10, 100, 1000 or 10,000: a 1 followed by one zero for each decimal place. Then reduce.",
     "0.375 = “375 thousandths” = [[375|1000]] = [[3|8]]")
example("Write 0.4375 as a fraction in lowest terms.",
        [("0.4375 = [[4375|10,000]]", "Four decimal places, so the bottom is 1 with four zeros."),
         ("[[4375 ÷ 625|10,000 ÷ 625]] = [[7|16]]", "Divide top and bottom by 5 four times (5 × 5 × 5 × 5 = 625)."),
         ("7 ÷ 16 = 0.4375 ✓", "Check by dividing.")], "[[7|16]]")
tip("The fraction key",
    "Most scientific calculators have a key that converts a decimal answer to a fraction (often marked `a b/c`, `F↔D` or `▸Frac`). "
    "It is the fastest way to reduce, but know the hand method too: the key cannot help when the decimal has been rounded.")
sub("Decimal to the nearest ruler fraction")
p("A calculated length such as 2.70 in is not a mark on a tape. To find the nearest 16th, multiply the decimal part by 16 and round to a whole number.")
example("What is 2.70 in to the nearest 16th of an inch?",
        [("0.70 × 16 = 11.2", "Multiply only the decimal part by the denominator wanted."),
         ("11.2 → 11", "Round to the nearest whole number. That is the number of sixteenths."),
         ("2 [[11|16]] in", "Put the whole inches back. Reduce if the top came out even.")], "2 [[11|16]] in")

sec("2.4 Decimals and percents")
p("**Percent** means “per hundred.” The symbol % stands for “÷ 100,” so 37.5% is 37.5 ÷ 100 = 0.375. Because dividing "
  "or multiplying by 100 only shifts the decimal point two places, the conversions can be done by sight.")
rule("Decimal ↔ percent",
     "**Decimal → percent:** move the decimal point **2 places right** and add the % sign (the same as × 100).   0.167 = 16.7%",
     "**Percent → decimal:** move the decimal point **2 places left** and drop the % sign (the same as ÷ 100).   37.5% = 0.375")
fig(figs.fdp_cycle(), "The three forms and how to move between them. To go from a fraction to a percent, go through the decimal.")
example("Write each as a percent: (a) 0.08   (b) 1.25   (c) 0.004",
        [("0.08 → 0 0 8. → 8%", "(a) Two places right. The point lands after the 8."),
         ("1.25 → 1 2 5. → 125%", "(b) A decimal larger than 1 is a percent larger than 100."),
         ("0.004 → 0 0 0.4 → 0.4%", "(c) Two places only. This is less than one percent.")],
        "(a) 8%   (b) 125%   (c) 0.4%")
warn("Which way does the point move?",
     "A percent is always the bigger-looking number: 0.25 is 25%. If you are going **to** percent the number should look larger, "
     "so the point moves right. Going **from** percent it should look smaller, so the point moves left.",
     "A single-digit percent needs a zero filled in: 6% = 0.06, not 0.6.")

sec("2.5 All three forms together")
p("Any one form leads to the other two. The path always passes through the decimal.")
example("Complete the row: fraction [[5|8]] → decimal → percent.",
        [("5 ÷ 8 = 0.625", "Top divided by bottom."), ("0.625 → 62.5%", "Point two places right, add %.")], "[[5|8]] = 0.625 = 62.5%")
example("Complete the row: 37.5% → decimal → fraction.",
        [("37.5% → 0.375", "Point two places left, drop %."), ("0.375 = [[375|1000]]", "Three decimal places: over 1000."),
         ("[[375 ÷ 125|1000 ÷ 125]] = [[3|8]]", "Reduce.")], "37.5% = 0.375 = [[3|8]]")
eqv = ["1/16", "1/8", "3/16", "1/4", "5/16", "3/8", "7/16", "1/2", "9/16", "5/8", "11/16", "3/4", "13/16", "7/8", "15/16", "1/3", "2/3", "1/5"]
rows = []
for i in range(0, 18, 2):
    a, b = Fraction(eqv[i]), Fraction(eqv[i + 1])
    rows.append([frtxt(eqv[i]), n(rnd(float(a), 4)), n(rnd(float(a) * 100, 2)) + "%",
                 frtxt(eqv[i + 1]), n(rnd(float(b), 4)), n(rnd(float(b) * 100, 2)) + "%"])
table(["Fraction", "Decimal", "Percent", "Fraction", "Decimal", "Percent"], rows, small=True,
      caption="Table 2.1  Equivalents worth knowing by heart (thirds rounded to four places)")

trip = [("frac", "3/8"), ("dec", "0.8"), ("pct", "45"), ("frac", "7/16"), ("dec", "0.065"), ("pct", "12.5"),
        ("frac", "9/20"), ("dec", "1.5"), ("pct", "2"), ("frac", "13/16"), ("dec", "0.3125"), ("pct", "87.5")]
items = []
for kind, v in trip:
    x = Fraction(v) if kind != "pct" else Fraction(v) / 100
    full = f"{fr(x)} = {n(float(x))} = {n(float(x) * 100)}%"
    q = {"frac": f"{frtxt(v)}  (to a decimal and a percent)", "dec": f"{v}  (to a fraction and a percent)",
         "pct": f"{v}%  (to a decimal and a fraction)"}[kind]
    items.append((q, full))
practice("Changing forms", "Write each number in the other two forms. Give fractions in lowest terms and do not round.", items, cols=2)

sec("2.6 Adding and subtracting mixed measurements")
p("Drawings often give some dimensions as fractions and others as decimals. Before adding or subtracting, put every "
  "number in the same form. Decimals are usually quicker; fractions are exact and match the tape.")
sub("Method 1: change everything to decimals")
example("A bracket is 11.25 in long. A second piece 31 [[3|8]] in long is welded to it. What is the total length?",
        [("31 [[3|8]] = 31.375", "Change the mixed number to a decimal: 3 ÷ 8 = 0.375."),
         ("11.250 + 31.375 = 42.625", "Line up the decimal points and add."),
         ("0.625 = [[5|8]]", "If a fraction is wanted, change the decimal part back.")], "42.625 in, or 42 [[5|8]] in")
sub("Method 2: keep everything in fractions")
p("Fractions can be added or subtracted only when their denominators match. For ruler fractions the common "
  "denominator is simply the **larger** of the two, because each denominator is a multiple of the smaller ones.")
example("[[7|8]] − [[3|16]]",
        [("[[7|8]] = [[7 × 2|8 × 2]] = [[14|16]]", "Change eighths to sixteenths: multiply top and bottom by 2."),
         ("[[14|16]] − [[3|16]] = [[11|16]]", "Same denominator, so subtract the tops. The bottom does not change.")], "[[11|16]]")
example("5 [[1|4]] − 2 [[5|8]]",
        [("5 [[2|8]] − 2 [[5|8]]", "Common denominator 8."),
         ("4 [[10|8]] − 2 [[5|8]]", "2 is smaller than 5, so borrow 1 from the 5. One whole is [[8|8]], and [[8|8]] + [[2|8]] = [[10|8]]."),
         ("2 [[5|8]]", "Subtract the whole numbers (4 − 2) and the fractions ([[10|8]] − [[5|8]]).")], "2 [[5|8]]",
        title="Borrowing")
warn("Never add the denominators",
     "[[1|4]] + [[1|4]] is [[2|4]] = [[1|2]], not [[2|8]]. The denominator names the size of the pieces, and the size does not change when pieces are added.")
adds = [("3/8", "+", "1/4"), ("5/16", "+", "1/2"), ("7/8", "-", "3/16"), ("3/4", "-", "5/16"), ("2 1/2", "+", "1 3/8"),
        ("4 3/16", "+", "2 7/8"), ("6 1/4", "-", "2 5/8"), ("10", "-", "3 7/16")]
its = []
for a, op, b in adds:
    v = F(a) + F(b) if op == "+" else F(a) - F(b)
    its.append((f"{frtxt(a)} {'+' if op == '+' else '−'} {frtxt(b)}", fr(v)))
mix = [("14.5", "+", "6 3/4"), ("22 5/8", "+", "9.25"), ("48 3/4", "-", "17.125"), ("60.5", "-", "24 7/8")]
for a, op, b in mix:
    v = F(a) + F(b) if op == "+" else F(a) - F(b)
    its.append((f"{frtxt(a)} in {'+' if op == '+' else '−'} {frtxt(b)} in  (decimal answer)", n(float(v)) + " in"))
practice("Adding and subtracting", "Give fraction answers in lowest terms as mixed numbers.", its, cols=2)

summary(["A fraction is a division: top ÷ bottom gives the decimal.",
         "A decimal becomes a fraction by writing it over 10, 100, 1000 … and reducing.",
         "Decimal to percent: point 2 places right, add %. Percent to decimal: point 2 places left, drop %.",
         "To go between a fraction and a percent, pass through the decimal.",
         "Add or subtract fractions only after giving them the same denominator; never add denominators."])

rv = []
for f in ["18/32", "40/64"]:
    rv.append((f"Reduce {frtxt(f)} to lowest terms.", fr(Fraction(f))))
for f in ["7/8", "3/16", "2 9/16"]:
    rv.append((f"Change {frtxt(f)} to a decimal.", n(float(F(f)))))
for d in ["0.625", "0.35", "0.1875"]:
    rv.append((f"Change {d} to a fraction in lowest terms.", fr(Fraction(d))))
for d in ["0.42", "0.075", "1.8"]:
    rv.append((f"Change {d} to a percent.", n(float(Fraction(d) * 100)) + "%"))
for d in ["64", "7", "112.5", "0.5"]:
    rv.append((f"Change {d}% to a decimal.", n(float(Fraction(d) / 100))))
rv += [("Change [[11|16]] to a percent.", n(float(Fraction(11, 16) * 100)) + "%"),
       ("Change 62.5% to a fraction in lowest terms.", fr(Fraction("0.625"))),
       ("What is 5.40 in to the nearest 16th of an inch?", "5 [[3|8]] in  (0.40 × 16 = 6.4 → [[6|16]])"),
       (f"{frtxt('3 5/8')} + {frtxt('2 9/16')}", fr(F("3 5/8") + F("2 9/16"))),
       (f"{frtxt('8 1/8')} − {frtxt('3 3/4')}", fr(F("8 1/8") - F("3 3/4"))),
       ("A shaft 18.375 in long has [[7|16]] in cut from one end. What length is left, as a decimal?", n(18.375 - 7 / 16) + " in"),
       ("Three spacers measure [[3|8]] in, 0.25 in and [[9|16]] in. What is their total thickness as a fraction?",
        fr(Fraction(3, 8) + Fraction(1, 4) + Fraction(9, 16)) + " in"),
       ("Which is larger, [[13|16]] or 0.81?", "[[13|16]]  (it is 0.8125)")]
review(rv)

# =====================================================================  3
chapter("The Percent Proportion",
        ["Identify the part, the whole and the percent in a percent statement.",
         "Set up the percent proportion and solve it by cross-multiplying.",
         "Solve all three types of percent problem with one method.",
         "Use the decimal shortcut for each type.",
         "Solve applied problems: efficiency, discount, tax, waste and percent change."],
        "Every percent problem is the same sentence with one number missing: *the part is some percent of the whole*. "
        "Learn to find the three pieces in that sentence, and one proportion solves them all.",
        [("part", "The piece being compared. It goes with the word **is**."),
         ("whole", "The total or original amount the part is compared to. It follows the word **of**. Also called the base."),
         ("percent", "The number with the % sign. It always sits over 100 in the proportion."),
         ("proportion", "A statement that two fractions are equal."),
         ("cross-multiply", "Multiply the two numbers that sit diagonally across the equals sign.")])

sec("3.1 Part, whole and percent")
p("Read this sentence slowly: **45 is 25% of 180.** It has three numbers, and each has a job.")
bullets(["**180** is the **whole**. It comes right after the word *of*. It is the total, the starting amount, the 100%.",
         "**45** is the **part**. It goes with the word *is*. It is the piece of the whole being talked about.",
         "**25%** is the **percent**. It is the easiest to find because it wears the % sign."])
fig(figs.percent_bar(45, 180, 25), "45 is 25% of 180. The part fills 25 hundredths of the whole.")
rule("The percent proportion",
     "[[PART (is)|WHOLE (of)]] = [[PERCENT|100]]",
     "The part compared to the whole is the same comparison as the percent compared to 100.")
fig(figs.proportion(), "Is over of equals percent over 100.")
p("In a problem, one of the three is unknown. Call it *x*, put the two known numbers in their places, and solve.")
warn("The whole is not always the bigger number",
     "In “150 is 125% of what number?” the part (150) is larger than the whole (120). Do not decide by size. "
     "Decide by the words: the whole follows **of**, the part goes with **is**.")

sec("3.2 Solving the proportion")
rule("Cross-multiply and divide",
     "**1.** Multiply the two numbers that are diagonal from each other.",
     "**2.** Divide by the number that is left over (the one diagonal from *x*).",
     "This works wherever *x* happens to be.")
sub("Type 1: finding the part")
example("What is 25% of 180?",
        [("[[x|180]] = [[25|100]]", "180 follows *of*, so it is the whole. 25 has the % sign. The part is unknown."),
         ("25 × 180 = 4500", "Cross-multiply the diagonal pair that has two numbers."),
         ("4500 ÷ 100 = 45", "Divide by the number left over.")], "45")
sub("Type 2: finding the whole")
example("150 is 25% of what number?",
        [("[[150|x]] = [[25|100]]", "150 goes with *is*: the part. “What number” follows *of*: the whole is unknown."),
         ("150 × 100 = 15,000", "Cross-multiply."), ("15,000 ÷ 25 = 600", "Divide by the number left over.")], "600")
sub("Type 3: finding the percent")
example("50 is what percent of 800?",
        [("[[50|800]] = [[x|100]]", "50 is the part, 800 follows *of*, and the percent is unknown."),
         ("50 × 100 = 5000", "Cross-multiply."), ("5000 ÷ 800 = 6.25", "Divide by the number left over."),
         ("6.25%", "The answer sits in the percent position, so it already is a percent. Just add the sign.")], "6.25%")
tip("One line on the calculator",
    "Each example is a single chain: `25 × 180 ÷ 100`, `150 × 100 ÷ 25`, `50 × 100 ÷ 800`. "
    "Multiply the diagonal pair, divide by the third number. No parentheses are needed.")
table(["The question", "Proportion", "Keystrokes"],
      [["What is P% of W?", "[[x|W]] = [[P|100]]", "P × W ÷ 100"], ["A is P% of what number?", "[[A|x]] = [[P|100]]", "A × 100 ÷ P"],
       ["A is what percent of W?", "[[A|W]] = [[x|100]]", "A × 100 ÷ W"]], caption="Table 3.1  The three types at a glance",
      widths=[36, 32, 32])
warn("Check that the answer makes sense",
     "25% is one quarter. One quarter of 180 should be less than 180, and 45 is. If the percent is under 100, the part must be "
     "smaller than the whole. If your answer breaks that rule, two numbers are in the wrong seats.")


def pp(kind, a, b):
    if kind == 1:
        return (f"What is {n(a)}% of {n(b)}?", n(rnd(a * b / 100, 4)))
    if kind == 2:
        return (f"{n(a)} is {n(b)}% of what number?", n(rnd(a * 100 / b, 4)))
    return (f"{n(a)} is what percent of {n(b)}?", n(rnd(a * 100 / b, 4)) + "%")


practice("The three types", "Set up the percent proportion for each and solve. Do not round.",
         [pp(*t) for t in [(1, 30, 400), (3, 30, 400), (2, 400, 80), (1, 15, 60), (2, 18, 12), (3, 9, 72),
                           (1, 6.5, 240), (3, 45, 36), (2, 21, 3.5), (1, 120, 85), (3, 3, 480), (2, 7.2, 16),
                           (1, 0.5, 900), (3, 66, 240), (2, 250, 125), (1, 37.5, 64)]], cols=2)

sec("3.3 The decimal shortcut")
p("Since percent means “÷ 100,” the proportion can be shortened by changing the percent to a decimal first. "
  "These three rules give exactly the same answers as the proportion. Use whichever method you trust most.")
rule("Percent problems with decimals",
     "**Part** = whole × percent (as a decimal)       25% of 180 = 180 × 0.25 = 45",
     "**Whole** = part ÷ percent (as a decimal)       150 ÷ 0.25 = 600",
     "**Percent** = part ÷ whole, then move the point 2 places right       50 ÷ 800 = 0.0625 = 6.25%")

sec("3.4 Percent on the job")
p("Word problems hide the words *is* and *of*. Find the three pieces by asking: What is the total or original amount "
  "(the whole)? What piece of it is being described (the part)? Which number is the percent?")
example("An air conditioner draws 3,500 watts of electrical power and delivers 2,870 watts of useful work at the compressor. What is its efficiency as a percent?",
        [("whole = 3,500 W;  part = 2,870 W", "The power going in is the total. The useful output is the part of it that is not lost."),
         ("[[2870|3500]] = [[x|100]]", "Efficiency asks: the output is what percent of the input?"),
         ("2870 × 100 ÷ 3500 = 82", "Cross-multiply and divide.")], "82% efficient", title="Efficiency")
example("A roll of copper tubing lists for $186.00. The supply house gives contractors a 15% discount. What is the contractor price?",
        [("[[x|186]] = [[15|100]]", "The discount is 15% **of** the list price. The list price is the whole."),
         ("15 × 186 ÷ 100 = 27.90", "The discount is $27.90."),
         ("186.00 − 27.90 = 158.10", "The question asks for the price, not the discount. Subtract.")], "$158.10", title="Discount")
p("A shortcut for the last example: if 15% comes off, 85% is left. So the price is 85% of 186, or 186 × 0.85 = 158.10 in one step.")
example("A sheet-metal job needs 240 square feet of material. The shop adds 12% for waste. How much should be ordered?",
        [("12 × 240 ÷ 100 = 28.8", "The waste allowance is 12% of the amount needed."),
         ("240 + 28.8 = 268.8", "Add the allowance to the original amount.")], "268.8 sq ft", title="Waste allowance")
example("After a 6% sales tax, a tool costs $84.80. What was the price before tax?",
        [("100% + 6% = 106%", "The total is the original price **plus** 6% of it, so $84.80 is 106% of the price."),
         ("[[84.80|x]] = [[106|100]]", "84.80 is the part (it *is* 106% *of* the price). The price is the whole."),
         ("84.80 × 100 ÷ 106 = 80", "Cross-multiply and divide.")], "$80.00", title="Working backward")
warn("Do not take the percent of the wrong number",
     "In the last example, 6% of $84.80 is $5.09, and 84.80 − 5.09 = $79.71, which is wrong. The tax was 6% of the *original* price, "
     "not of the total. When the whole is the unknown, set up the proportion; do not guess with subtraction.")

sub("Percent change")
p("A percent increase or decrease always compares the **amount of change** to the **original** value.")
rule("Percent change", "percent change = [[amount of change|original amount]] × 100",
     "The original amount is the whole, no matter whether the value went up or down.")
example("A supply-air temperature drops from 75°F to 57°F. What is the percent decrease?",
        [("75 − 57 = 18", "Find the amount of change."), ("[[18|75]] = [[x|100]]", "The change is the part. The **original** value is the whole."),
         ("18 × 100 ÷ 75 = 24", "Cross-multiply and divide.")], "24% decrease")

wp = [("A 250-ft spool of wire has had 85 ft used. What percent has been used?", n(85 * 100 / 250) + "%"),
      ("A motor rated at 1,200 W input is 88% efficient. What is its output power?", n(1200 * 0.88) + " W"),
      ("A technician earns $24.50 per hour and receives a 6% raise. What is the new hourly rate, to the nearest cent?", "$" + n(24.5 * 1.06, 2)),
      ("A furnace listed at $1,450 is sold at a 20% discount. What is the sale price?", "$" + n(1450 * 0.8, 2)),
      ("A job needs 320 sq ft of drywall. Add 10% for waste. How much is ordered?", n(320 * 1.1) + " sq ft"),
      ("18 of 150 welds failed inspection. What percent failed? What percent passed?", "12% failed; 88% passed"),
      ("A down payment of $1,260 is 15% of the price of a used service van. What is the price?", "$" + n(1260 * 100 / 15)),
      ("A tank holds 60 gallons when it is 75% full. What is its full capacity?", n(60 * 100 / 75) + " gal"),
      ("Line voltage falls from 240 V to 228 V. What is the percent decrease?", n(12 * 100 / 240) + "%"),
      ("The price of a fitting rises from $8.00 to $9.20. What is the percent increase?", n(1.2 * 100 / 8) + "%"),
      ("A resistor marked 470 Ω has a tolerance of ±5%. What are its lowest and highest acceptable values?",
       f"{n(470 * 0.95)} Ω to {n(470 * 1.05)} Ω"),
      ("With 8% sales tax a compressor costs $702. What was the price before tax?", "$" + n(702 * 100 / 108, 2))]
practice("Applications", "Solve each problem. Round only where the problem says.", wp, cols=1)

summary(["Every percent problem fits one sentence: the **part** *is* a **percent** *of* the **whole**.",
         "The percent proportion is part over whole equals percent over 100.",
         "Cross-multiply the diagonal pair of numbers, then divide by the third number.",
         "Decimal shortcut: part = whole × percent; whole = part ÷ percent; percent = part ÷ whole.",
         "Percent change compares the amount of change to the **original** amount."])
review([pp(*t) for t in [(1, 35, 260), (2, 84, 70), (3, 27, 180), (1, 4.5, 800), (3, 150, 120), (2, 9, 0.6)]]
       + [("What is the whole in the statement “12 is 40% of 30”?", "30"),
          ("Write the proportion for “What percent of 64 is 24?” Do not solve.", "[[24|64]] = [[x|100]]"),
          ("Use the decimal shortcut: find 18% of 350.", n(350 * 0.18)),
          ("Use the decimal shortcut: 91 is 65% of what number?", n(91 / 0.65)),
          ("A pump delivers 1,530 W of output for 1,800 W of input. What is its efficiency?", n(1530 * 100 / 1800) + "%"),
          ("A $640 meter is on sale for 25% off. What is the sale price?", "$" + n(640 * 0.75)),
          ("Static pressure rises from 0.50 to 0.62 inch of water. What is the percent increase?", n(0.12 * 100 / 0.5) + "%"),
          ("A crew has installed 45 of 125 light fixtures. What percent remain to be installed?", n(80 * 100 / 125) + "%"),
          ("A bill of $1,391 includes 7% sales tax. What was the amount before tax?", "$" + n(1391 * 100 / 107)),
          ("A student says 8% of 50 is 40. Explain the error and give the correct answer.",
           "8% was used as 0.8 instead of 0.08 (or the ÷ 100 was skipped). 8 × 50 ÷ 100 = 4.")])
