"""Added depth for Part 1 (numbers): more explanation, worked examples, practice and review."""
import random
from fractions import Fraction
from book import *  # noqa: F401,F403
from util import n, r, rnd, fr, F, frtxt
import figs

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
        "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
DEC = ["", "tenths", "hundredths", "thousandths", "ten-thousandths"]
PLACE_VAL = {"millions": 6, "hundred thousands": 5, "ten thousands": 4, "thousands": 3, "hundreds": 2, "tens": 1, "ones": 0,
             "tenths": -1, "hundredths": -2, "thousandths": -3, "ten-thousandths": -4}


def words(k):
    """a whole number below one million in words"""
    if k < 20:
        return ONES[k]
    if k < 100:
        return TENS[k // 10] + ("-" + ONES[k % 10] if k % 10 else "")
    if k < 1000:
        return ONES[k // 100] + " hundred" + (" " + words(k % 100) if k % 100 else "")
    return words(k // 1000) + " thousand" + (" " + words(k % 1000) if k % 1000 else "")


def dec_words(s):
    """'12.06' -> 'twelve and six hundredths'"""
    w, d = s.split(".")
    tail = words(int(d)) + " " + DEC[len(d)]
    if int(d) == 1:
        tail = tail[:-1]
    return tail if int(w) == 0 else words(int(w)) + " and " + tail


def digit_value(num, pos):
    """value of the digit at index pos of the string num"""
    w, d = num.split(".")
    if pos < len(w):
        return int(w[pos]) * 10 ** (len(w) - 1 - pos)
    k = pos - len(w) - 1
    return int(d[k]) / 10 ** (k + 1)


# =====================================================================  1
def ch1():
    import ch_numbers as C
    rg = random.Random(101)
    sec("1.6 The value of a digit and expanded form")
    p("Place value answers the question “which place is this digit in?” The **value** of a digit answers a different question: “how much is this digit worth?” "
      "The value is the digit multiplied by the worth of its place.")
    rule("Value of a digit", "value = digit × place value", "In 4,072.56 the 7 is in the tens place, so its value is 7 × 10 = 70. The 6 is in the hundredths place, so its value is 6 × 0.01 = 0.06.")
    p("Writing a number as the sum of the values of its digits is called **expanded form**. It shows exactly what the number is made of.")
    example("Write 4,072.56 in expanded form.",
            [("4 × 1000 = 4000", "Thousands digit."), ("0 × 100 = 0", "Hundreds digit. A zero adds nothing, but it holds the place."), ("7 × 10 = 70;  2 × 1 = 2", "Tens and ones."),
             ("5 × 0.1 = 0.5;  6 × 0.01 = 0.06", "Tenths and hundredths."), ("4000 + 70 + 2 + 0.5 + 0.06", "Add the values. The zero term is left out.")],
            "4000 + 70 + 2 + 0.5 + 0.06")
    example("What is the value of the 7 in 0.0375? What is the value of the 3?",
            [("0 . 0 3 7 5 → tenths 0, hundredths 3, thousandths 7", "Count places to the right of the point."), ("7 × 0.001 = 0.007", "The 7 is in the thousandths place."),
             ("3 × 0.01 = 0.03", "The 3 is in the hundredths place.")], "0.007 and 0.03")
    sub("Multiplying and dividing by 10, 100 and 1000")
    p("Because each place is ten times the next, multiplying by 10 slides every digit one place to the left, which looks like the decimal point "
      "moving one place to the **right**. Dividing by 10 moves the point one place to the **left**. This is the idea behind percent (Chapter 2) and the metric system (Chapter 5).")
    table(["Operation", "The decimal point moves", "Example"],
          [["× 10", "1 place right", "3.75 × 10 = 37.5"], ["× 100", "2 places right", "3.75 × 100 = 375"], ["× 1000", "3 places right", "3.75 × 1000 = 3750"],
           ["÷ 10", "1 place left", "3.75 ÷ 10 = 0.375"], ["÷ 100", "2 places left", "3.75 ÷ 100 = 0.0375"], ["÷ 1000", "3 places left", "3.75 ÷ 1000 = 0.00375"]], widths=[20, 36, 44])
    p("Count the zeros in 10, 100 or 1000: that is the number of places the point moves. Fill any empty places with zeros.")

    its = []
    for num in ["8,362.4175", "50,917.268", "704.9053"]:
        plain = num.replace(",", "")
        idx = [i for i, ch in enumerate(plain) if ch not in ".0"]
        for i in rg.sample(idx, 3):
            v = digit_value(plain, i)
            its.append((f"In {num}, what is the value of the digit {plain[i]}?" if plain.count(plain[i]) == 1 else None, n(v)))
    its = [t for t in its if t[0]]
    for num in ["3,208.45", "617.039", "90,050.6"]:
        plain = num.replace(",", "")
        parts = [n(digit_value(plain, i)) for i, ch in enumerate(plain) if ch not in ".0"]
        its.append((f"Write {num} in expanded form.", " + ".join(parts)))
    for v, op, k in [(4.82, "×", 10), (0.375, "×", 100), (62.5, "÷", 10), (7.4, "÷", 100), (0.0625, "×", 1000), (385, "÷", 1000), (12.07, "×", 100), (9, "÷", 10)]:
        ans = v * k if op == "×" else v / k
        its.append((f"{n(v)} {op} {n(k)}", n(rnd(ans, 6))))
    practice("Value and powers of ten", "Answer each question. For the last eight, move the decimal point.", its, cols=2)

    sec("1.7 Numbers in words and in digits")
    p("Work orders are read over a radio, sizes are called out across a shop, and checks are written in words. The rules for moving between words and digits are short.")
    bullets(["Read the whole-number part in groups of three digits: 52,307 is “fifty-two **thousand**, three hundred seven.”",
             "Say **and** only at the decimal point. 307 is “three hundred seven,” not “three hundred and seven.”",
             "Read the decimal part as a whole number, then name the place of its **last** digit: 0.045 is “forty-five thousandths.”",
             "Use a hyphen in two-word numbers from twenty-one to ninety-nine and in “ten-thousandths.”"])
    example("Write 6.005 in words.",
            [("6 → six", "The whole-number part."), ("and", "The decimal point."), ("005 → five", "Read the digits after the point as a whole number: 005 is 5."),
             ("last digit is in the thousandths place", "Three decimal places.")], "six and five thousandths")
    example("Write “two hundred four and thirty-six ten-thousandths” in digits.",
            [("two hundred four → 204", "Everything before “and.”"), ("ten-thousandths → 4 decimal places", "The place name tells how many digits follow the point."),
             ("thirty-six → 0036", "Write 36 so that it **ends** in the fourth place. Fill the front with zeros.")], "204.0036", title="Zeros as placeholders")
    warn("The place name sets the number of digits",
         "“Thirty-six ten-thousandths” is 0.0036, not 0.36 and not 0.036. Write the decimal places as blanks first ( _ _ _ _ ), put the number in at the right-hand end, "
         "and fill the empty blanks with zeros.")
    its = []
    for s in ["0.9", "0.37", "5.008", "14.25", "0.0125", "120.6", "3.075", "0.0004"]:
        its.append((f"Write {s} in words.", dec_words(s)))
    for s in ["0.6", "0.045", "7.02", "31.125", "0.0875", "400.09", "2.0005", "0.016"]:
        its.append((f"Write in digits: {dec_words(s)}.", s))
    practice("Words and digits", "", its, cols=2)

    sec("1.8 Putting decimals in order")
    p("Drill bits, feeler gauges and shim stock are sorted by size. To put several decimals in order, give them all the same number of decimal "
      "places by adding zeros, then compare them as if they were whole numbers.")
    fig(figs.number_line([0.3, 0.305, 0.35, 0.035 + 0.3], 0.30, 0.36, 0.01, ["0.3", "0.305", "0.35", "0.335"]),
        "Four decimals on a number line. The farther right, the larger the number.")
    example("Arrange from smallest to largest: 0.35, 0.305, 0.3, 0.335.",
            [("0.350, 0.305, 0.300, 0.335", "The longest has three decimal places, so write them all with three."),
             ("350, 305, 300, 335", "Now compare the digits after the point like whole numbers."), ("300 &lt; 305 &lt; 335 &lt; 350", "Put them in order."),
             ("0.3, 0.305, 0.335, 0.35", "Write each one the way it was given.")], "0.3, 0.305, 0.335, 0.35")
    example("Four drill bits measure 0.4375 in, 0.453 in, 0.44 in and 0.4219 in. Which is the largest? Which is the smallest?",
            [("0.4375, 0.4530, 0.4400, 0.4219", "Four decimal places for all."), ("4219 &lt; 4375 &lt; 4400 &lt; 4530", "Compare.")],
            "Largest 0.453 in; smallest 0.4219 in")
    sets = [[0.6, 0.56, 0.605, 0.065], [1.2, 1.02, 1.21, 1.012], [0.875, 0.8125, 0.9, 0.87], [3.07, 3.7, 3.007, 3.077], [0.25, 0.3125, 0.2, 0.28],
            [0.062, 0.0625, 0.06, 0.1], [12.5, 12.05, 12.55, 12.505], [0.75, 0.705, 0.7, 0.775]]
    practice("Ordering decimals", "Arrange each set from smallest to largest.",
             [(", ".join(n(v) for v in s), ", ".join(n(v) for v in sorted(s))) for s in sets], cols=2)

    sec("1.9 Rounding on the job")
    p("The five rules never change, but three situations come up so often that they deserve their own examples.")
    sub("Money: round to the nearest cent")
    p("A cent is one hundredth of a dollar, so “to the nearest cent” means “to the nearest hundredth.” Always show two decimal places in a money answer, even when they are zeros.")
    example("A job uses 37.5 ft of pipe at $2.189 per foot. Find the cost to the nearest cent.",
            [("37.5 × 2.189 = 82.0875", "Multiply."), ("82.0**8**75 → test digit 7", "The hundredths digit is 8. The next digit is 7, so round up."), ("82.09", "")], "$82.09")
    sub("Materials: round up")
    p("When the answer is a number of things to buy, any fraction means one more is needed.")
    example("A fence needs 187 ft of rail. Rails come in 16-ft lengths. How many rails must be bought?",
            [("187 ÷ 16 = 11.6875", "Divide."), ("12", "Eleven rails are not enough, so round **up**, whatever the test digit is.")], "12 rails")
    sub("Estimating to check a calculator answer")
    p("Round each number to one or two easy digits and work the problem in your head. The estimate will not match the exact answer, "
      "but it will catch a slipped decimal point or a wrong key.")
    example("A calculator shows 48.7 × 19.6 = 9545.2. Is that reasonable?",
            [("48.7 → 50;  19.6 → 20", "Round each number to one digit."), ("50 × 20 = 1000", "Multiply in your head."),
             ("9545.2 is about ten times too large", "The estimate says the answer should be near 1000."), ("48.7 × 19.6 = 954.52", "Re-enter. A decimal point was missed.")],
            "No. The correct product is 954.52.")
    ap = [("A part costs $14.3275 to make. Round to the nearest cent.", "$14.33"), ("Wire costs $0.4375 per foot. Find the cost of 250 ft to the nearest cent.", "$" + n(250 * 0.4375, 2)),
          ("A crew works 7.75 hours at $31.40 per hour. Find the pay to the nearest cent.", "$" + n(7.75 * 31.4, 2)),
          ("A job needs 212 ft of conduit in 10-ft lengths. How many lengths must be bought?", "22 lengths"),
          ("A floor needs 346.5 sq ft of plywood. Each sheet covers 32 sq ft. How many sheets?", "11 sheets"),
          ("Paint covers 350 sq ft per gallon. How many gallons are needed for 1,180 sq ft?", "4 gallons"),
          ("A measurement of 2.4687 in is to be recorded to the nearest thousandth.", "2.469 in"),
          ("A speed of 3,663.33 ft/min is to be reported to the nearest ten.", "3,660 ft/min"),
          ("A load of 71,428.57 psi is to be reported to the nearest thousand.", "71,000 psi"),
          ("Estimate 62.3 × 4.9 by rounding each number to one digit.", "about 300 (60 × 5)"),
          ("Estimate 795 ÷ 19.8 by rounding.", "about 40 (800 ÷ 20)"),
          ("A calculator shows 31.2 × 9.7 = 3026.4. Use an estimate to decide whether it is reasonable.", "No. 30 × 10 = 300; the answer should be 302.64.")]
    practice("Rounding on the job", "Round as each problem directs.", ap, cols=1)

    q = []
    for _ in range(24):
        whole = rg.randint(10, 99999)
        dec = rg.randint(1000, 9999)
        s = f"{whole:,}.{dec}"
        near = rg.choice(list(C.NEAREST)) if whole > 999 else rg.choice(["ten", "whole number", "tenth", "hundredth", "thousandth"])
        q.append((f"{s} to the nearest {near}", C.rs(s, near)))
    practice("More rounding", "Round each number to the place named.", q, cols=2)

    more_review([("What is the value of the 6 in 3,640.25?", "600"), ("What is the value of the 5 in 12.0457?", "0.005"),
                 ("Write 508.34 in expanded form.", "500 + 8 + 0.3 + 0.04"), ("Write 0.072 in words.", dec_words("0.072")),
                 ("Write in digits: sixteen and nine thousandths.", "16.009"), ("0.0625 × 100", "6.25"), ("47.5 ÷ 1000", "0.0475"),
                 ("Arrange from smallest to largest: 0.4, 0.375, 0.41, 0.3125.", "0.3125, 0.375, 0.4, 0.41"),
                 ("Round $128.4951 to the nearest cent.", "$128.50"), ("A job needs 95 ft of pipe sold in 20-ft lengths. How many lengths?", "5 lengths"),
                 ("Round 0.99962 to the nearest thousandth.", "1.000"), ("Estimate 412 × 19.5 by rounding.", "about 8,000 (400 × 20)")])


# =====================================================================  2
def ch2():
    rg = random.Random(202)
    sec("2.7 Equivalent fractions and comparing fractions")
    p("Multiplying the top and bottom of a fraction by the same number changes its looks but not its value. This is **raising to higher terms**, the reverse of reducing.")
    fig(figs.fraction_bars([(1, 2), (2, 4), (4, 8), (8, 16)]), "The same half of a bar, cut into more and more pieces: one half, two fourths, four eighths, eight sixteenths.")
    example("Write [[3|4]] as sixteenths.",
            [("4 × ? = 16  →  4", "What must the bottom be multiplied by?"), ("[[3 × 4|4 × 4]] = [[12|16]]", "Multiply the top by the same number.")], "[[12|16]]")
    p("To **compare** two fractions, either give them a common denominator and compare the tops, or change both to decimals.")
    example("Which wrench is larger, [[9|16]] in or [[5|8]] in?",
            [("[[5|8]] = [[10|16]]", "Change eighths to sixteenths."), ("[[10|16]] &gt; [[9|16]]", "Same denominator: the larger top is the larger fraction."),
             ("0.625 &gt; 0.5625", "Check with decimals.")], "[[5|8]] in is larger")
    example("Arrange from smallest to largest: [[3|8]], [[5|16]], [[11|32]], [[1|4]].",
            [("[[12|32]], [[10|32]], [[11|32]], [[8|32]]", "The largest denominator, 32, works for all of them."), ("8 &lt; 10 &lt; 11 &lt; 12", "Order the tops.")],
            "[[1|4]], [[5|16]], [[11|32]], [[3|8]]")
    cmp_ = [("3/8", "5/16"), ("7/16", "1/2"), ("11/16", "5/8"), ("13/32", "3/8"), ("3/4", "25/32"), ("9/16", "17/32"), ("7/8", "27/32"), ("15/64", "1/4")]
    its = [(f"Write {frtxt(a)} with a denominator of {d}.", "[[%d|%d]]" % (Fraction(a) * d, d)) for a, d in [("1/2", 16), ("3/4", 32), ("5/8", 64), ("7/16", 32), ("1/4", 64), ("3/8", 16)]]
    its += [(f"Which is larger, {frtxt(a)} or {frtxt(b)}?", frtxt(a if Fraction(a) > Fraction(b) else b)) for a, b in cmp_]
    practice("Equivalent fractions and comparing", "", its, cols=2)

    sec("2.8 Multiplying and dividing fractions")
    p("Laying out equal spaces, finding half of a dimension and counting how many pieces can be cut from a bar all call for multiplying or dividing fractions. "
      "No common denominator is needed for either one.")
    rule("Multiplying fractions", "Multiply the tops. Multiply the bottoms. Reduce.", "Change mixed numbers to improper fractions first, and write a whole number over 1.",
         "[[3|4]] × [[5|8]] = [[15|32]]")
    example("What is half of 5 [[3|8]] in?",
            [("5 [[3|8]] = [[43|8]]", "Mixed number to improper: 5 × 8 + 3 = 43."), ("[[1|2]] × [[43|8]] = [[43|16]]", "“Half of” means multiply by one half."),
             ("[[43|16]] = 2 [[11|16]]", "Back to a mixed number: 43 ÷ 16 = 2 remainder 11.")], "2 [[11|16]] in")
    example("Seven spacers are each 2 [[3|4]] in long. What is their total length?",
            [("2 [[3|4]] = [[11|4]]", "Mixed to improper."), ("[[7|1]] × [[11|4]] = [[77|4]]", "Write 7 as seven over one."), ("[[77|4]] = 19 [[1|4]]", "77 ÷ 4 = 19 remainder 1.")],
            "19 [[1|4]] in")
    rule("Dividing fractions", "Turn the second fraction upside down (its **reciprocal**) and multiply.", "[[3|4]] ÷ [[1|8]] = [[3|4]] × [[8|1]] = [[24|4]] = 6",
         "Dividing by 2 is multiplying by [[1|2]], which is why halving a fraction doubles its denominator.")
    example("How many pieces 1 [[3|8]] in long can be cut from a bar 22 in long? (Ignore the width of the cuts.)",
            [("1 [[3|8]] = [[11|8]]", "Mixed to improper."), ("22 ÷ [[11|8]] = [[22|1]] × [[8|11]]", "Invert the divisor and multiply."), ("[[176|11]] = 16", "")], "16 pieces")
    tip("Fractions on a calculator",
        "Put every mixed number in parentheses: `22 ÷ (1 + 3 ÷ 8)` gives 16. Without the parentheses the calculator divides 22 by 1 first and the answer is wrong.")
    md = [("1/2", "×", "3/4"), ("3/8", "×", "2/3"), ("5/16", "×", "4"), ("1/2", "×", "7 5/8"), ("3", "×", "2 5/16"), ("1 1/2", "×", "2 3/4"),
          ("3/4", "÷", "1/8"), ("7/8", "÷", "2"), ("5/8", "÷", "5/16"), ("4 1/2", "÷", "3/4"), ("15", "÷", "1 7/8"), ("6 3/4", "÷", "3")]
    its = []
    for a, op, b in md:
        v = F(a) * F(b) if op == "×" else F(a) / F(b)
        its.append((f"{frtxt(a)} {op} {frtxt(b)}", fr(v)))
    its += [("What is half of 9 [[7|8]] in?", fr(F("9 7/8") / 2) + " in"), ("Five shims are each [[3|32]] in thick. What is the total thickness?", fr(Fraction(15, 32)) + " in"),
            ("How many [[3|4]]-in pieces can be cut from a 24-in bar?", "32 pieces"), ("A 30-in board is cut into 8 equal pieces. How long is each?", fr(Fraction(30, 8)) + " in")]
    practice("Multiplying and dividing fractions", "Give answers in lowest terms as mixed numbers.", its, cols=2)

    sec("2.9 Special decimals and percents")
    sub("Repeating decimals")
    p("Some fractions never come out even. [[1|3]] = 0.3333…, [[2|3]] = 0.6666… and [[5|6]] = 0.8333… The digits repeat forever, so these must be rounded. "
      "Notice that 0.6666… rounds to 0.667, not 0.666, because the test digit is a 6.")
    sub("Percents larger than 100 and smaller than 1")
    p("A percent over 100 is more than the whole: 150% = 1.5, one and a half times as much. A percent under 1 is less than one hundredth: 0.5% = 0.005. "
      "The rule for moving the decimal point is exactly the same.")
    example("Write as decimals: (a) 250%   (b) 0.8%   (c) 12 [[1|2]]%",
            [("250% → 2.50", "(a) Two places left."), ("0.8% → 0.008", "(b) Two places left; fill with zeros."),
             ("12 [[1|2]]% = 12.5% → 0.125", "(c) Change the fraction to a decimal first, then move the point.")], "(a) 2.5   (b) 0.008   (c) 0.125")
    warn("One-half percent is not one-half",
         "[[1|2]]% means half of **one percent**: 0.5% = 0.005. It is one hundred times smaller than [[1|2]] = 0.5 = 50%.")
    its = []
    for v in ["1/3", "2/3", "1/6", "5/6", "1/12", "4/9"]:
        its.append((f"Change {frtxt(v)} to a decimal, rounded to the nearest thousandth.", n(rnd(float(Fraction(v)), 3), 3)))
    for v in [175, 300, 0.5, 0.25, 6.5, 112.5, 0.08, 1000]:
        its.append((f"Change {n(v)}% to a decimal.", n(v / 100)))
    for v in [1.4, 0.003, 2, 0.0075, 3.25, 0.0005]:
        its.append((f"Change {n(v)} to a percent.", n(v * 100) + "%"))
    practice("Special decimals and percents", "", its, cols=2)

    sec("2.10 More fraction work from the shop")
    example("Three spacers measure [[3|8]] in, [[5|16]] in and [[1|4]] in. What is their combined thickness?",
            [("[[6|16]] + [[5|16]] + [[4|16]]", "The largest denominator, 16, is the common denominator."), ("[[15|16]]", "Add the tops: 6 + 5 + 4 = 15.")], "[[15|16]] in",
            title="Adding three fractions")
    example("A bar 36 in long has pieces of 8 [[1|2]] in and 11 [[3|4]] in cut from it. Each cut wastes [[1|8]] in. How much of the bar is left?",
            [("8 [[1|2]] + 11 [[3|4]] = 8 [[2|4]] + 11 [[3|4]] = 19 [[5|4]] = 20 [[1|4]]", "Add the two pieces. [[5|4]] is 1 [[1|4]], so carry the 1."),
             ("2 × [[1|8]] = [[1|4]]", "Two cuts, each [[1|8]] in wide."), ("20 [[1|4]] + [[1|4]] = 20 [[1|2]]", "Total used."),
             ("36 − 20 [[1|2]] = 35 [[2|2]] − 20 [[1|2]] = 15 [[1|2]]", "Borrow 1 from 36 and write it as [[2|2]].")], "15 [[1|2]] in", title="Cutting stock")
    example("A pipe has an outside diameter of 2 [[3|8]] in and a wall thickness of [[5|32]] in. What is its inside diameter?",
            [("2 × [[5|32]] = [[10|32]] = [[5|16]]", "The wall is counted twice, once on each side."), ("2 [[3|8]] − [[5|16]] = 2 [[6|16]] − [[5|16]]", "Common denominator 16."),
             ("2 [[1|16]]", "")], "2 [[1|16]] in", title="Inside diameter")
    its = []
    for _ in range(12):
        d1, d2 = rg.choice([2, 4, 8, 16]), rg.choice([4, 8, 16, 32])
        a = Fraction(rg.randrange(1, d1, 2), d1) + rg.randint(0, 6)
        b = Fraction(rg.randrange(1, d2, 2), d2) + rg.randint(0, 4)
        if rg.random() < 0.5 or a <= b:
            its.append((f"{fr(a)} + {fr(b)}", fr(a + b)))
        else:
            its.append((f"{fr(a)} − {fr(b)}", fr(a - b)))
    its += [("Find the total thickness of shims [[1|8]] in, [[3|32]] in and [[1|16]] in.", fr(Fraction(1, 8) + Fraction(3, 32) + Fraction(1, 16)) + " in"),
            ("A 48-in bar has pieces of 12 [[3|8]] in and 20 [[5|16]] in cut from it. Ignoring the cuts, how much is left?", fr(48 - F("12 3/8") - F("20 5/16")) + " in"),
            ("A pipe has an outside diameter of 3 [[1|2]] in and a wall thickness of [[7|32]] in. Find the inside diameter.", fr(F("3 1/2") - Fraction(7, 16)) + " in"),
            ("A countertop is 25 [[1|4]] in deep with a [[3|4]]-in overhang. How deep is the cabinet under it?", fr(F("25 1/4") - Fraction(3, 4)) + " in")]
    practice("More adding and subtracting", "Give answers in lowest terms as mixed numbers.", its, cols=2)

    more_review([("Write [[5|8]] with a denominator of 32.", "[[20|32]]"), ("Which is larger, [[19|32]] or [[5|8]]?", "[[5|8]]"),
                 ("Arrange from smallest to largest: [[7|16]], [[3|8]], [[1|2]], [[13|32]].", "[[3|8]], [[13|32]], [[7|16]], [[1|2]]"),
                 (f"{frtxt('3/4')} × {frtxt('5/8')}", fr(Fraction(15, 32))), ("What is half of 7 [[5|8]] in?", fr(F("7 5/8") / 2) + " in"),
                 (f"{frtxt('5 1/4')} ÷ {frtxt('7/8')}", fr(F("5 1/4") / Fraction(7, 8))), ("How many 2 [[1|2]]-in pieces can be cut from a 40-in bar?", "16 pieces"),
                 ("Change [[2|3]] to a decimal rounded to the nearest hundredth.", "0.67"), ("Change 0.5% to a decimal.", "0.005"), ("Change 2.25 to a percent.", "225%"),
                 ("Change 37 [[1|2]]% to a fraction in lowest terms.", "[[3|8]]"),
                 (f"{frtxt('3/8')} + {frtxt('5/16')} + {frtxt('1/2')}", fr(Fraction(3, 8) + Fraction(5, 16) + Fraction(1, 2)))])


# =====================================================================  3
def ch3():
    import ch_numbers as C
    rg = random.Random(303)
    sec("3.5 Finding the three pieces")
    p("Setting up the proportion is the whole problem. Once the part, the whole and the percent are in the right seats, the arithmetic is one line. "
      "Practice naming the pieces **before** doing any calculating.")
    rule("Naming the pieces", "**Percent:** the number with the % sign, or the words “what percent.”",
         "**Whole:** the number right after the word **of**. It is the total, the original, the full amount, the 100%.",
         "**Part:** the number next to the word **is**. It is what is left when the other two are named.")
    table(["Statement", "Part (is)", "Whole (of)", "Percent", "Proportion"],
          [["What is 40% of 65?", "x", "65", "40", "[[x|65]] = [[40|100]]"], ["18 is 30% of what number?", "18", "x", "30", "[[18|x]] = [[30|100]]"],
           ["What percent of 250 is 45?", "45", "250", "x", "[[45|250]] = [[x|100]]"], ["12% of what number is 9?", "9", "x", "12", "[[9|x]] = [[12|100]]"],
           ["75 is what percent of 60?", "75", "60", "x", "[[75|60]] = [[x|100]]"]], widths=[32, 13, 14, 12, 29], small=True)
    p("The words do not always come in the same order. “What percent of 250 is 45?” has the whole first and the part last. Follow the words *of* and *is*, not the order.")
    its = []
    for kind, a, b in [(1, 15, 240), (2, 36, 45), (3, 28, 70), (1, 8.5, 400), (2, 54, 120), (3, 9, 150), (2, 6, 2.5), (3, 110, 88)]:
        if kind == 1:
            its.append((f"What is {n(a)}% of {n(b)}?", f"part x, whole {n(b)}, percent {n(a)};  [[x|{n(b)}]] = [[{n(a)}|100]]"))
        elif kind == 2:
            its.append((f"{n(a)} is {n(b)}% of what number?", f"part {n(a)}, whole x, percent {n(b)};  [[{n(a)}|x]] = [[{n(b)}|100]]"))
        else:
            its.append((f"What percent of {n(b)} is {n(a)}?", f"part {n(a)}, whole {n(b)}, percent x;  [[{n(a)}|{n(b)}]] = [[x|100]]"))
    practice("Naming the pieces", "Name the part, the whole and the percent, and write the proportion. Do not solve.", its, cols=1)

    sec("3.6 Percents that are not whole numbers")
    p("Fraction percents, decimal percents and percents over 100 all go into the proportion the same way. Change a fraction percent to a decimal first.")
    example("What is 12 [[1|2]]% of 640?",
            [("12 [[1|2]]% = 12.5%", "Change the fraction to a decimal."), ("[[x|640]] = [[12.5|100]]", "640 follows *of*: the whole."), ("12.5 × 640 ÷ 100 = 80", "Cross-multiply and divide.")], "80")
    example("3 is what percent of 800?",
            [("[[3|800]] = [[x|100]]", "3 is the part; 800 follows *of*."), ("3 × 100 ÷ 800 = 0.375", "Cross-multiply and divide."), ("0.375%", "Less than one percent. Do not move the decimal point again.")],
            "0.375%", title="A percent smaller than 1")
    example("What is 140% of 85?",
            [("[[x|85]] = [[140|100]]", "The percent is more than 100, so the part will be larger than the whole."), ("140 × 85 ÷ 100 = 119", "")], "119", title="A percent larger than 100")
    warn("Already a percent",
         "When *x* sits over 100 in the proportion, the answer that comes out **is** the percent. 0.375 means 0.375%. Moving the point two more places would give 37.5%, which is a hundred times too big.")

    sec("3.7 More percent on the job")
    example("The electrical code recommends that the voltage drop in a branch circuit be no more than 3% of the supply voltage. For a 120-V circuit, what is the largest drop allowed, and what is the lowest voltage at the load?",
            [("[[x|120]] = [[3|100]]", "The drop is 3% **of** the supply voltage."), ("3 × 120 ÷ 100 = 3.6", "The largest drop is 3.6 V."), ("120 − 3.6 = 116.4", "Subtract the drop from the supply.")],
            "3.6 V drop; 116.4 V at the load", title="Voltage drop")
    example("A hydronic system holds 80 gallons and must be filled with a mixture that is 35% glycol. How many gallons of glycol and how many gallons of water are needed?",
            [("35 × 80 ÷ 100 = 28", "Glycol is 35% of the total."), ("80 − 28 = 52", "The rest is water.")], "28 gal of glycol and 52 gal of water", title="A mixture")
    example("A gauge reads 147 psi when the true pressure is 150 psi. What is the percent error?",
            [("150 − 147 = 3", "The error is the difference between the reading and the true value."), ("[[3|150]] = [[x|100]]", "Compare the error to the **true** value."),
             ("3 × 100 ÷ 150 = 2", "")], "2% error", title="Percent error")
    example("A thermostat lists for $240. A contractor gets a 25% discount, and then 8% sales tax is added to the discounted price. What is the final cost?",
            [("240 × 0.75 = 180", "After a 25% discount, 75% is left."), ("180 × 0.08 = 14.40", "The tax is 8% of the **discounted** price."), ("180 + 14.40 = 194.40", "")],
            "$194.40", title="Discount, then tax")
    example("A motor is rated to carry 18 amps. It is drawing 15.3 amps. At what percent of its rating is it running?",
            [("[[15.3|18]] = [[x|100]]", "The rating is the whole; the actual current is the part."), ("15.3 × 100 ÷ 18 = 85", "")], "85% of rated load", title="Percent of capacity")
    ap = [("The voltage drop on a 240-V circuit must not exceed 3%. What is the largest drop allowed?", n(7.2) + " V"),
          ("A circuit supplied at 120 V measures 114 V at the load. What is the percent voltage drop?", "5%"),
          ("A 50-gallon system needs a 40% glycol mixture. How many gallons of glycol?", "20 gal"),
          ("A solution is made of 6 quarts of cleaner and 18 quarts of water. What percent of the solution is cleaner?", "25%"),
          ("A scale reads 49.2 lb for a 50-lb test weight. What is the percent error?", "1.6%"),
          ("A meter listed at $320 is discounted 15%, then 7% tax is added. Find the final cost.", "$" + n(320 * 0.85 * 1.07, 2)),
          ("A 20-amp breaker should be loaded to no more than 80% of its rating. How many amps is that?", "16 A"),
          ("A compressor rated at 24 amps is drawing 21 amps. At what percent of its rating is it running?", "87.5%"),
          ("A furnace has an input of 80,000 Btu per hour and is 92% efficient. What is its output?", n(73600) + " Btu per hour"),
          ("A boiler delivers 102,000 Btu per hour from an input of 120,000 Btu per hour. What is its efficiency?", "85%"),
          ("Of 240 fittings in a box, 6 are defective. What percent are defective?", "2.5%"),
          ("A crew finished 65% of a 180-ft trench. How many feet remain?", "63 ft"),
          ("Copper rises from $3.80 to $4.37 per pound. What is the percent increase?", "15%"),
          ("A filter cuts airflow from 1,200 cfm to 1,050 cfm. What is the percent decrease?", "12.5%"),
          ("After a 4% raise a technician earns $27.04 per hour. What was the hourly rate before the raise?", "$26.00"),
          ("A shop marks up parts 40% over cost. A part sells for $63. What did it cost the shop?", "$45.00")]
    practice("More applications", "Name the part, whole and percent, then solve.", ap, cols=1)

    q = []
    for _ in range(30):
        kind = rg.choice([1, 2, 3])
        if kind == 1:
            a, b = rg.choice([5, 8, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75, 110, 2.5, 7.5]), rg.choice([40, 60, 80, 120, 160, 200, 240, 360, 500, 640])
        elif kind == 2:
            pct = rg.choice([5, 10, 12, 15, 20, 25, 30, 40, 60, 75, 80])
            whole = rg.choice([40, 60, 80, 120, 150, 200, 300, 450])
            a, b = pct * whole / 100, pct
        else:
            whole = rg.choice([40, 50, 80, 120, 160, 200, 250, 400])
            pct = rg.choice([5, 12, 15, 22.5, 30, 37.5, 45, 62.5, 80, 125])
            a, b = pct * whole / 100, whole
        q.append(C.pp(kind, a, b))
    practice("Mixed percent problems", "Solve each with the percent proportion. Do not round.", q, cols=2)

    more_review([("In “What percent of 90 is 27?”, which number is the whole?", "90"), ("What is 12 [[1|2]]% of 320?", "40"), ("4 is what percent of 500?", "0.8%"),
                 ("What is 250% of 36?", "90"), ("21 is 3.5% of what number?", "600"),
                 ("A 208-V circuit may drop no more than 3%. What is the largest drop, to the nearest hundredth?", r(208 * 0.03, 2) + " V"),
                 ("A 60-gallon system needs 30% glycol. How many gallons of water are needed?", "42 gal"),
                 ("A gauge reads 196 psi when the true pressure is 200 psi. Find the percent error.", "2%"),
                 ("A $500 tool is discounted 20%, then 6% tax is added. Find the final cost.", "$" + n(500 * 0.8 * 1.06, 2)),
                 ("A motor rated at 30 amps draws 25.5 amps. At what percent of its rating is it running?", "85%"),
                 ("After a 5% raise a wage is $29.40 per hour. What was it before?", "$28.00"),
                 ("Explain why 6% tax on a total of $106 is not the tax that was charged on a $100 item.",
                  "The tax was 6% of the original $100 ($6.00), not 6% of the total. 6% of $106 is $6.36.")])


def part1():
    cumulative("Part 1 · Numbers", "Mixed problems from Chapters 1, 2 and 3.",
               [("In 80,652.9417, which digit is in the thousandths place?", "1"), ("Round 80,652.9417 to the nearest hundred.", "80,700"),
                ("Round 80,652.9417 to the nearest hundredth.", "80,652.94"), ("Which is larger, 0.5625 or 0.57?", "0.57"),
                ("Write 0.035 in words.", "thirty-five thousandths"), ("Reduce [[24|32]] to lowest terms.", "[[3|4]]"),
                ("Change [[9|16]] to a decimal.", "0.5625"), ("Change 0.875 to a fraction.", "[[7|8]]"), ("Change 0.045 to a percent.", "4.5%"),
                ("Change 162.5% to a decimal.", "1.625"), ("Change [[3|16]] to a percent.", "18.75%"),
                ("3 [[7|8]] + 2 [[5|16]]", fr(F("3 7/8") + F("2 5/16"))), ("9 [[1|4]] − 4 [[11|16]]", fr(F("9 1/4") - F("4 11/16"))),
                ("What is half of 6 [[3|4]] in?", fr(F("6 3/4") / 2) + " in"), ("What is 18% of 450?", "81"), ("63 is 45% of what number?", "140"),
                ("52 is what percent of 80?", "65%"), ("A $1,250 unit is sold at 12% off. Find the sale price.", "$1,100.00"),
                ("Pressure rises from 60 psi to 75 psi. Find the percent increase.", "25%"),
                ("A bar 30 in long has 11 [[5|8]] in and 9.75 in cut from it. How much is left, as a decimal?", n(30 - 11.625 - 9.75) + " in")], cols=2)
