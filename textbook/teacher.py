"""The teacher's edition: teaching notes for each chapter, a pacing guide and a test with key for each chapter.
Built with  TEACHER=1 python3 build.py"""
from fractions import Fraction
from math import sqrt
import book
from book import fmt
from util import n, r, fr, F

# chapter: (class sessions, big idea, how to teach it, common errors, activity, exit ticket [(q, a)], which sets to assign)
NOTES = {
    1: ("3 sessions", "Every digit has a value set by its place, and rounding asks which round value a number is closest to.",
        ["Start with the place-value chart (Figure 1.1) and have students name places aloud, moving left and right from the decimal point.",
         "Teach rounding with the class handout, The Basic Rules, exactly as worded. Have students underline the rounding digit and circle the digit to its right.",
         "Do sections 1.6 to 1.8 only if the class needs the review; 1.9 (money, rounding up, estimating) is worth the time for every group."],
        ["Confusing **ten** with **tenth** and **hundred** with **hundredth**. Have students say the last three letters out loud.",
         "Rounding in stages (2.3491 → 2.35 → 2.4).", "Skipping a zero when counting places.", "Dropping the zero in 4.40 or 20.00 after rounding."],
        "Hand out catalog pages or a parts price list. Each student rounds five prices to the nearest dollar, ten dollars and hundred dollars and totals each column. Compare the three totals with the exact total.",
        [("In 5,307.9146, which digit is in the hundredths place?", "1"), ("Round 5,307.9146 to the nearest tenth.", "5,307.9"), ("Round 5,307.9146 to the nearest hundred.", "5,300")],
        "Core: Practice 1.1, 1.2. Extra: 1.3 to 1.7. Assessment: Chapter 1 review, odd numbers in class and even numbers as homework."),
    2: ("4 sessions", "A fraction, a decimal and a percent are three names for the same amount, and the decimal is the bridge between the other two.",
        ["Use the handout wording: fraction to decimal, divide top by bottom; decimal to percent, move the decimal 2 places right and add %; percent to decimal, 2 places left and drop %.",
         "Draw Figure 2.1 on the board and leave it up all week.", "Have students build Table 2.1 themselves on a calculator before they see it printed.",
         "Section 2.8 (multiplying and dividing fractions) can be delayed until Chapter 9, where the lock-seam problem needs dividing a fraction by 2."],
        ["Moving the decimal point the wrong way. Remind them that the percent is always the bigger-looking number.", "Writing 6% as 0.6.",
         "Adding denominators (1/4 + 1/4 = 2/8).", "Leaving a ruler fraction unreduced (6/16)."],
        "Give each pair a tape measure and five objects. They record each length as a fraction, a decimal and a percent of an inch or foot, then swap lists and check each other.",
        [("Change 7/8 to a decimal and a percent.", "0.875; 87.5%"), ("Change 4.5% to a decimal.", "0.045"), ("3 5/8 + 1 3/4", "5 3/8")],
        "Core: Practice 2.1, 2.2, 2.3. Extra: 2.4 to 2.7. The mixed decimal-and-fraction subtraction in 2.3 (problems 9 to 12) prepares for the missing-length exam question."),
    3: ("4 sessions", "Every percent problem is one sentence, the part is a percent of the whole, with one number missing.",
        ["Teach the percent proportion exactly as on the handout: PART (is) over (of) WHOLE equals PCT# over 100; cross-multiply and divide.",
         "Spend a full session on Practice 3.3, naming the pieces without solving. Setup is where the errors are.",
         "Show the three board examples in order: What is 30% of 400? 30 is what % of 400? 400 is 30% of what number?",
         "Offer the decimal shortcut (3.3) as an alternative only after the proportion is secure."],
        ["Putting the bigger number on the bottom automatically.", "Moving the decimal again after the proportion has already given a percent (0.375% becomes 37.5%).",
         "Taking a percent of the total instead of the original when working backward (the sales-tax problem).", "Using the new value instead of the original as the whole in percent change."],
        "Bring in a store flyer or a supply-house invoice. Students find the discount percent on five items, then the price after an 8% tax.",
        [("What is 15% of 240?", "36"), ("18 is what percent of 72?", "25%"), ("54 is 45% of what number?", "120")],
        "Core: Practice 3.1, 3.2, 3.3. Extra: 3.4, 3.5. The cumulative review for Part 1 follows this chapter and works as a practice test."),
    4: ("5 sessions", "Converting changes the unit and the number together: going to a smaller unit there are more of them, so multiply; going to a larger unit, divide.",
        ["Give out the Standard Units handout (Table 4.1). Students should keep it out for every problem; the goal is choosing the operation, not memorizing.",
         "Teach one category a day in the order of the book: length, weight, capacity, area, volume.",
         "For area and volume, build the factors with the pictures (Figures 4.4 and 4.6) before stating 144 and 1728.",
         "Require the sanity check out loud: should the number get bigger or smaller?"],
        ["Dividing square inches by 12, or cubic inches by 1296. Note that the class answer sheet for the conversion practice prints “1296” for two cubic-inch problems; the factor is 1728.",
         "Multiplying when they should divide.", "Writing 5 ft 7 in as 5.7 ft.", "Mixing feet and inches inside a volume formula."],
        "Tape a 1-foot square on the floor and fill it with 1-inch tiles or grid paper to count 144. Then stack 12 layers in the mind to reach 1728.",
        [("Convert 900 sq in to sq ft, to the nearest tenth.", "6.3 sq ft"), ("Convert 4 cu yd to cu ft.", "108 cu ft"), ("Convert 20 cu ft to gallons.", "149.6 gal")],
        "Core: Practice 4.1, 4.2. Extra: 4.3, 4.4, 4.5. Practice 4.2 mirrors the class conversion worksheet (nearest tenth)."),
    5: ("5 sessions", "Inside the metric system every conversion is a move of the decimal point; between systems, the seven handout facts and the multiply-or-divide rule do the work.",
        ["Draw the metric stairs (Figure 5.1) with meter, gram and liter on every step. Students point at each stair as they count.",
         "Teach direction with the stairs: down toward milli, the point moves right; up toward kilo, the point moves left.",
         "Give out the Standard / Metric Conversions handout (Table 5.3). The unit written with the 1 is the larger unit.",
         "Do the bonus-style problem (5 km to inches) together to model a multi-step plan."],
        ["Counting units named instead of steps (mm to m is three steps).", "Forgetting the base-unit step between deka and deci.",
         "Moving the point the wrong direction.", "Using 2.54 directly on millimeters."],
        "Circle the larger unit: call out pairs (centimeter or inch, liter or quart, gram or ounce) and have students hold up a card. Follow with real objects: a paper clip, a liter bottle, a meter stick.",
        [("Convert 250 mm to cm.", "25 cm"), ("Convert 50 cm to inches, to the nearest tenth.", "19.7 in"), ("Which is larger, a kilogram or a pound?", "a kilogram")],
        "Core: Practice 5.1, 5.2, 5.3. Extra: 5.4 to 5.7."),
    6: ("4 sessions", "Reading any scale starts with one question: what is each small space worth?",
        ["Use real rules. Have students find 1/2, 1/4, 1/8 and 1/16 marks by length before reading any point.",
         "For gauges, insist on the four steps in the Key Rule box and on counting by the scale value to check it.",
         "Spend extra time on the dual-scale gauge: one needle, two rings, two scale values. This is a known trouble spot on the Chapter 5 exam.",
         "For tolerance, always write the nominal size with the same number of decimal places as the tolerance (0.810 ± 0.003)."],
        ["Counting marks instead of spaces.", "Leaving 2 6/16 unreduced.", "Reading the psi needle position against the kPa numbers.",
         "0.81 + 0.003 = 0.84.", "Counting holes instead of spaces in equal-spacing problems."],
        "Set up stations with a tape measure, a steel rule, a pressure gauge or multimeter and a set of drill bits. Students rotate, record five readings at each station and compare.",
        [("A point is 10 sixteenths past the 3-inch mark. Give the reading.", "3 5/8 in"), ("A gauge is numbered every 200 with 4 spaces between numbers. What is each space worth?", "50"),
         ("Find the limits of 0.81 in ± 0.003 in.", "0.807 in to 0.813 in")],
        "Core: Practice 6.1, 6.2, 6.3. Extra: 6.4 to 6.7. The cumulative review for Part 2 follows this chapter."),
    7: ("4 sessions", "An expression has one value because everyone follows the same order: P, E, M or D left to right, A or S left to right.",
        ["Open with the board example: 6 + 4 ÷ 2 worked the wrong way (5) and the right way (8).",
         "List the grouping symbols as in the class notes: ( ), [ ], { }, absolute value, fraction bar.",
         "Model one operation per line with 5 − 3(4² ÷ 2) + 30 = 11.",
         "Use Figure 7.2 to preview solving: evaluating runs down the list, solving runs back up."],
        ["Treating PEMDAS as six steps (multiplying before dividing, adding before subtracting).", "4² = 8.", "Dividing only the last term of a fraction’s top on the calculator.",
         "Adding 24 + 30 first in 5 − 24 + 30."],
        "Give four students the same expression on cards with one operation each. They must line up in the order the operations are done and perform them in turn.",
        [("Evaluate 20 − 8 + 5.", "17"), ("Evaluate 3 + 5 × 2².", "23"), ("Evaluate (12 − 3(4² ÷ 2³) + 9) ÷ (5² − 10).", "1")],
        "Core: Practice 7.1. Extra: 7.2, 7.3. Require at least three calculations shown, as on the chapter exam."),
    8: ("4 sessions", "A formula is a set of instructions: write it, substitute with parentheses, then evaluate by the order of operations.",
        ["Require three lines every time: the formula, the substitution, the evaluation. Grade the substitution line.",
         "Have students list each letter with its value and unit before substituting.",
         "Work the pipe formula N = √(D ÷ d)⁵ on the calculator together, including the keystrokes.",
         "Point out the rounding instruction in each problem before any calculating starts."],
        ["Writing 2C with C = 30 as 230.", "Applying an exponent to the wrong quantity (25T⁴).", "Confusing D and d, or the subscripts in C₁, C₂, C₃.",
         "Rounding in the middle of the problem.", "Ignoring “nearest hundred” and giving the unrounded answer."],
        "Formula scavenger hunt: students bring one formula from their own trade class or a nameplate, explain each letter and evaluate it with real numbers.",
        [("Evaluate L = 3A + 4(B + C) for A = 2, B = 3, C = 4.", "34"), ("N = √(D ÷ d)⁵ for D = 15, d = 3, to the nearest whole number.", "56"),
         ("C_T = C₁(C₂ + C₃) ÷ (C₁ + C₂ + C₃) for 16, 6, 8, to the nearest hundredth.", "7.47")],
        "Core: Practice 8.1. Extra: 8.2."),
    9: ("5 sessions", "Solving runs a formula backward: undo the operations in the reverse of PEMDAS, doing the same thing to both sides.",
        ["Use the balance picture (Figure 9.1) and the two-way PEMDAS diagram (Figure 9.2).",
         "Always substitute and simplify before undoing anything.",
         "Teach two-step equations as: undo the add or subtract, then undo the multiply or divide.",
         "Work the lock-seam problem, A = 2w + 3/16 with A = 7/8, slowly and twice. It is the most-missed item on the Chapter 7 exam (answer 11/32)."],
        ["Adding instead of subtracting the 3/16.", "Multiplying by 2 instead of dividing (answer 1 3/8).", "Dividing before clearing the added number.",
         "Dropping the negative sign with −0.002H.", "Not checking the answer in the original formula."],
        "Pairs: one student evaluates a formula for a chosen value and passes only the result; the partner solves backward to recover the value. Swap roles.",
        [("Solve 3200 = 2L + 2(450) for L.", "1150"), ("V = LWH: V = 3882, L = 52.6, W = 9. Find H to the nearest tenth.", "8.2"), ("A = 2w + 3/16 with A = 7/8. Find w.", "11/32")],
        "Core: Practice 9.1, 9.2. Extra: 9.3 to 9.6. The cumulative review for Part 3 follows this chapter."),
    10: ("4 sessions", "Perimeter is a length found by adding; area is a count of squares found by multiplying a base by a height.",
         ["Give out the Chapter 8 handout, page 1 (rectangle, square, parallelogram, trapezoid). The teal boxes reproduce its wording.",
          "Use the slide picture (Figure 10.3) and the two-trapezoid picture (Figure 10.5) so the formulas are understood, not just memorized.",
          "Make students say the unit with every answer: inches or square inches.",
          "Run each formula backward once the forward direction is secure (section 10.8)."],
         ["Using the slanted side as the height.", "Typing 12 + 20 × 9 without parentheses for a trapezoid.", "Forgetting to divide by 2.", "Multiplying feet by inches.",
          "Rounding down when buying material."],
         "Cut two identical paper trapezoids, turn one over and fit them into a parallelogram. Measure the base and height and confirm the area formula.",
         [("Trapezoid: bases 12 in and 20 in, height 9 in. Find A.", "144 sq in"), ("Rectangle: P = 76 ft, L = 23 ft. Find W.", "15 ft"), ("Parallelogram: b = 18 in, a = 10 in, h = 8 in. Find P and A.", "P = 56 in; A = 144 sq in")],
         "Core: Practice 10.1. Extra: 10.2, 10.3, 10.4."),
    11: ("4 sessions", "Any triangle’s area is bh ÷ 2; when the height is missing, Hero’s Formula or the Pythagorean theorem supplies what is needed.",
         ["Give out the Chapter 8 handout, page 2 (triangles, Hero’s Formula, right triangle).",
          "Teach Hero’s Formula as two lines: semi-perimeter first, then the root. Have students write s down before keying the root.",
          "For the Pythagorean theorem, find the right angle first, then label c across from it.",
          "The 3-4-5 check with a tape measure makes the theorem real."],
         ["Forgetting the 2 in bh ÷ 2.", "Using s for both the side (.433s²) and the semi-perimeter.", "Adding the squares when a leg is wanted.", "√(a² + b²) = a + b.",
          "A missing parenthesis that leaves part of the product outside the root."],
         "Outdoors or in a hallway, lay out a 6-8-10 triangle with tapes and check the corner with a framing square. Then measure a real triangular brace and find its area with Hero’s Formula.",
         [("Hero’s Formula: sides 15, 20, 25 m. Find A.", "150 m²"), ("Right triangle: legs 5 ft and 12 ft. Find c.", "13 ft"), ("Equilateral triangle: s = 8 in. Find A.", "27.712 sq in")],
         "Core: Practice 11.1. Extra: 11.2, 11.3, 11.4."),
    12: ("5 sessions", "Circles use π = 3.14 with the radius squared for area; composite figures are taken apart into shapes already known, and the trapezoid is the most useful of them.",
         ["Give out the Chapter 8 handout, pages 3 and 4 (regular hexagon, circles, composite figures).",
          "Use π = 3.14 throughout, and have students type 3.14 rather than the π key so answers match the key.",
          "For composite figures, require a sketch with the cut lines drawn and each part labeled before any arithmetic.",
          "Teach the L as two trapezoids (Figure 12.3): one cut from the inside corner to the far corner. Then check with rectangles.",
          "Work a hexagon backward: 500 = 2.6s², s² = 192.3, s = 13.9."],
         ["Using the diameter in πr².", "Doubling instead of squaring the radius.", "Subtracting radii instead of areas for a ring.",
          "Choosing the slanted cut line as a base or height of a trapezoid.", "Counting inside cut lines in a composite perimeter."],
         "Give each group a floor plan of the classroom or shop drawn as an L or a T. One group splits it into rectangles, one into trapezoids, one subtracts from a big rectangle. All three must agree.",
         [("Circle: d = 14 in. Find A.", "153.86 sq in"), ("Hexagon: s = 4 in. Find A.", "41.6 sq in"),
          ("An L is 20 ft by 14 ft overall with an 8 ft by 6 ft corner missing. Find its area.", "232 sq ft")],
         "Core: Practice 12.1, 12.2, 12.5. Extra: 12.3, 12.4. The cumulative review for Part 4 follows this chapter and works as a final-exam review for geometry."),
}

PACING = [("1", "Chapter 1", "Place value; rounding; The Basic Rules", "Practice 1.1, 1.2"),
          ("2", "Chapter 2", "Fractions, decimals, percents and back", "Practice 2.1 to 2.3"),
          ("3", "Chapter 3", "The percent proportion; the three types", "Practice 3.1 to 3.3"),
          ("4", "Chapters 1 to 3", "Applications; cumulative review, Part 1; Test 1, 2, 3", "Practice 3.2, 3.4; review"),
          ("5", "Chapter 4", "Standard units: length, weight, capacity", "Practice 4.1, 4.3"),
          ("6", "Chapter 4", "Area and volume factors; gallons", "Practice 4.2, 4.4"),
          ("7", "Chapter 5", "Metric stairs; standard and metric facts", "Practice 5.1 to 5.3"),
          ("8", "Chapter 6", "Rulers, gauges, tolerance, missing lengths", "Practice 6.1 to 6.3"),
          ("9", "Chapters 4 to 6", "Cumulative review, Part 2; Tests 4, 5, 6 (the Chapter 5 exam)", "review"),
          ("10", "Chapter 7", "Order of operations", "Practice 7.1, 7.3"),
          ("11", "Chapter 8", "Substitute and evaluate", "Practice 8.1, 8.2"),
          ("12", "Chapter 9", "Substitute and solve; equations with fractions", "Practice 9.1, 9.2"),
          ("13", "Chapters 7 to 9", "Cumulative review, Part 3; Tests 7, 8, 9 (the Chapter 7 exam)", "review"),
          ("14", "Chapters 10, 11", "Quadrilaterals; triangles; Hero’s Formula; right triangles", "Practice 10.1, 11.1"),
          ("15", "Chapter 12", "Circles, hexagons, composite figures", "Practice 12.1, 12.2, 12.5"),
          ("16", "All", "Cumulative review, Part 4; Tests 10, 11, 12; final exam", "review")]


def notes_pdf(ch):
    t = NOTES[ch]
    li = lambda xs: "".join(f"<li>{fmt(x)}</li>" for x in xs)  # noqa: E731
    exit_ = "".join(f'<li>{fmt(q)} <span class="ta">{fmt(a)}</span></li>' for q, a in t[5])
    return (f'<div class="tnotes"><div class="th"><span>TEACHER’S NOTES · CHAPTER {ch}</span><span>{t[0]}</span></div><div class="tb">'
            f'<h4>The big idea</h4><p>{fmt(t[1])}</p><h4>Teaching the chapter</h4><ul>{li(t[2])}</ul>'
            f'<h4>Errors to watch for</h4><ul>{li(t[3])}</ul><h4>Activity</h4><p>{fmt(t[4])}</p>'
            f'<h4>Exit ticket</h4><ol>{exit_}</ol><h4>Assigning the practice</h4><p>{fmt(t[6])}</p></div></div>')


def notes_docx(ch):
    t = NOTES[ch]
    f = lambda x: fmt(x, "docx")  # noqa: E731
    li = lambda xs: "".join(f"<li>{f(x)}</li>" for x in xs)  # noqa: E731
    return (f'<div custom-style="TeacherNote"><p><b>TEACHER’S NOTES, CHAPTER {ch} ({t[0]})</b></p><p><b>The big idea.</b> {f(t[1])}</p>'
            f'<p><b>Teaching the chapter</b></p><ul>{li(t[2])}</ul><p><b>Errors to watch for</b></p><ul>{li(t[3])}</ul>'
            f'<p><b>Activity.</b> {f(t[4])}</p><p><b>Exit ticket</b></p><ol>' + "".join(f"<li>{f(q)}  <b>[{f(a)}]</b></li>" for q, a in t[5])
            + f'</ol><p><b>Assigning the practice.</b> {f(t[6])}</p></div>')


USING = [("Answers beside every question", "In practice sets, chapter reviews and cumulative reviews, the answer is printed in red directly after each question. The complete key also remains at the back, as in the student book."),
         ("Teacher’s notes", "Each chapter opens with a dark box giving the number of class sessions, the big idea, a teaching sequence, the errors students make most often, a hands-on activity, a three-question exit ticket and advice on which practice sets to assign."),
         ("Class handout boxes", "Teal boxes reproduce the wording of the class handouts word for word, so the book and the handouts never disagree."),
         ("Chapter tests", "A one-page test for every chapter, with a full key, is at the back. The tests follow the style of the course exams: show the work, show all substitutions, and round as each question directs."),
         ("Section and problem numbers", "Chapter, section, example, figure and practice numbers are identical in the student and teacher’s editions. Page numbers differ, because the notes and printed answers take space; assign work by practice number, not page.")]


def front_pdf():
    rows = "".join(f"<tr><td>{w}</td><td>{fmt(c)}</td><td>{fmt(t)}</td><td>{fmt(a)}</td></tr>" for w, c, t, a in PACING)
    use = "".join(f"<li><b>{fmt(h)}.</b> {fmt(x)}</li>" for h, x in USING)
    return ('<section class="front"><h1>Using the teacher’s edition</h1>'
            '<p>This edition contains the complete student text. Everything added for the instructor is listed below.</p>'
            f'<ul class="plain">{use}</ul>'
            '<h2><span class="secbar"></span>A sixteen-week pacing guide</h2>'
            '<p>The guide assumes two or three class meetings a week. Sections numbered 5 and higher in each chapter are enrichment and extra practice; '
            'a class that is short of time can skip them without losing anything the later chapters need.</p>'
            '<div class="tablewrap"><table class="data small"><colgroup><col style="width:8%"><col style="width:17%"><col style="width:47%"><col style="width:28%"></colgroup>'
            f'<tr><th>Week</th><th>Chapter</th><th>Topics</th><th>Assign</th></tr>{rows}</table></div>'
            '<h2><span class="secbar"></span>Grading the work shown</h2>'
            '<p>The course exams give credit for work, not only for answers. A workable scheme for a formula problem worth 10 points: '
            '2 points for writing the formula, 3 for a correct substitution, 3 for the evaluation or solving steps, 1 for rounding as directed and 1 for the unit.</p>'
            '</section>')


def front_docx():
    f = lambda x: fmt(x, "docx")  # noqa: E731
    rows = "".join(f"<tr><td>{w}</td><td>{f(c)}</td><td>{f(t)}</td><td>{f(a)}</td></tr>" for w, c, t, a in PACING)
    return ("<h1>Using the teacher’s edition</h1><ul>" + "".join(f"<li><b>{f(h)}.</b> {f(x)}</li>" for h, x in USING) + "</ul>"
            f"<h2>A sixteen-week pacing guide</h2><table><tr><th>Week</th><th>Chapter</th><th>Topics</th><th>Assign</th></tr>{rows}</table>")


# ---------------------------------------------------------------- chapter tests

def hero(a, b, c):
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


TESTS = {
    1: ("MUST SHOW SOME WORK FOR FULL CREDIT.",
        [("In the number 73,580.2946, name the digit in each place: (a) hundredths (b) thousands (c) tenths (d) ten-thousandths (e) hundreds (f) ten thousands", "(a) 9 (b) 3 (c) 2 (d) 6 (e) 5 (f) 7", 12),
         ("Round 4,618.3572 to the nearest: (a) tenth (b) whole number (c) thousandth (d) hundred (e) ten (f) hundredth", "(a) 4,618.4 (b) 4,618 (c) 4,618.357 (d) 4,600 (e) 4,620 (f) 4,618.36", 18),
         ("Which is larger, 0.4375 or 0.44?", "0.44", 6), ("Arrange from smallest to largest: 0.6, 0.065, 0.56, 0.605", "0.065, 0.56, 0.6, 0.605", 8),
         ("Write in digits: twenty-four and thirty-seven thousandths.", "24.037", 6), ("Write 0.0625 in words.", "six hundred twenty-five ten-thousandths", 6),
         ("What is the value of the 8 in 3,480.25?", "80", 6), ("Round 19.997 to the nearest hundredth.", "20.00", 8),
         ("A calculation gives 71,428.57 psi. Round to the nearest hundred psi.", "71,400 psi", 8),
         ("A job needs 137 ft of pipe sold in 20-ft lengths. How many lengths must be bought?", "7 lengths", 8),
         ("List the five steps of The Basic Rules of rounding.", "1 identify the rounding digit; 2 look at the next digit to the right; 3 round up if it is 5 to 9; 4 keep it the same if it is 0 to 4; 5 replace the remaining digits (zeros for whole numbers, drop them for decimals)", 14),
         ("BONUS. A student rounds 8.3482 to the nearest tenth and writes 8.4. Explain the error.", "The student rounded twice. The digit to the right of the 3 is 4, so the answer is 8.3.", 0)]),
    2: ("MUST SHOW SOME WORK FOR FULL CREDIT. Give fractions in lowest terms.",
        [("Reduce to lowest terms: (a) 12/16 (b) 20/32 (c) 36/64", "(a) 3/4 (b) 5/8 (c) 9/16", 9),
         ("Change to decimals: (a) 5/8 (b) 3/16 (c) 2 3/4", "(a) 0.625 (b) 0.1875 (c) 2.75", 12),
         ("Change to fractions: (a) 0.375 (b) 0.8 (c) 0.4375", "(a) 3/8 (b) 4/5 (c) 7/16", 12),
         ("Change to percents: (a) 0.167 (b) 0.08 (c) 1.25", "(a) 16.7% (b) 8% (c) 125%", 9),
         ("Change to decimals: (a) 37.5% (b) 6% (c) 0.5%", "(a) 0.375 (b) 0.06 (c) 0.005", 9),
         ("Complete: 5/8 = ____ (decimal) = ____ (percent)", "0.625 = 62.5%", 8),
         ("Complete: 87.5% = ____ (decimal) = ____ (fraction)", "0.875 = 7/8", 8),
         ("7/8 − 3/16", "11/16", 7), ("5 1/4 + 2 5/8", "7 7/8", 7), ("9 1/8 − 3 3/4", "5 3/8", 7),
         ("A bar is 78 3/4 in long overall. Two sections measure 11.25 in and 31 3/8 in. Find the third section. No rounding.", "36.125 in (36 1/8 in)", 12),
         ("BONUS. What is 3.70 in to the nearest 16th of an inch?", "3 11/16 in (0.70 × 16 = 11.2)", 0)]),
    3: ("MUST SHOW THE PROPORTION FOR FULL CREDIT.",
        [("What is 25% of 180?", "45", 9), ("150 is 25% of what number?", "600", 9), ("50 is what percent of 800?", "6.25%", 9),
         ("What is 6.5% of 240?", "15.6", 9), ("45 is what percent of 36?", "125%", 9), ("21 is 3.5% of what number?", "600", 9),
         ("In “18 is 30% of 60,” name the part, the whole and the percent.", "part 18, whole 60, percent 30", 6),
         ("A motor draws 1,800 W and delivers 1,530 W. Find its efficiency.", "85%", 10),
         ("A $640 meter is sold at 25% off. Find the sale price.", "$480.00", 10),
         ("A job needs 320 sq ft of material. Add 10% for waste. How much is ordered?", "352 sq ft", 10),
         ("Line voltage falls from 240 V to 228 V. Find the percent decrease.", "5%", 10),
         ("BONUS. With 8% sales tax a compressor costs $702. Find the price before tax.", "$650.00", 0)]),
    4: ("MUST SHOW SOME WORK FOR FULL CREDIT. Round to the nearest tenth if needed.",
        [("1000 sq in = ____ sq ft", r(1000 / 144, 1) + " sq ft (divide by 144)", 8), ("15.5 sq yd = ____ sq ft", "139.5 sq ft (multiply by 9)", 8),
         ("24 sq ft = ____ sq in", "3,456 sq in (multiply by 144)", 8), ("1500 sq in = ____ sq yd", r(1500 / 1296, 1) + " sq yd (divide by 1296)", 8),
         ("2500 cu ft = ____ cu yd", r(2500 / 27, 1) + " cu yd (divide by 27)", 8), ("5000 cu in = ____ cu ft", r(5000 / 1728, 1) + " cu ft (divide by 1728)", 8),
         ("23.5 cu yd = ____ cu ft", "634.5 cu ft (multiply by 27)", 8), ("5.5 cu ft = ____ cu in", "9,504 cu in (multiply by 1728)", 8),
         ("5 cu ft = ____ gallons", "37.4 gal (multiply by 7.48)", 8), ("1500 cu in = ____ gallons", r(1500 / 231, 1) + " gal (divide by 231)", 8),
         ("55 gallons = ____ cu ft", r(55 / 7.48, 1) + " cu ft (divide by 7.48)", 8), ("5 gallons = ____ cu in", "1,155 cu in (multiply by 231)", 6),
         ("Convert 8 ft 9 in to inches.", "105 in", 6),
         ("BONUS. A slab is 40 ft by 12 ft by 4 in. How many cubic yards of concrete, to the nearest tenth?", "5.9 cu yd", 0)]),
    5: ("MUST SHOW SOME WORK FOR FULL CREDIT. Round to the nearest tenth if needed.",
        [("Convert on the metric stairs: (a) 250 mm = ____ cm (b) 0.25 L = ____ mL (c) 250 dg = ____ dag", "(a) 25 cm (b) 250 mL (c) 2.5 dag", 18),
         ("Convert: (a) 4.5 m = ____ cm (b) 750 g = ____ kg (c) 2.4 km = ____ m", "(a) 450 cm (b) 0.75 kg (c) 2,400 m", 18),
         ("Circle the larger unit: (a) centimeter or inch (b) liter or quart (c) gallon or cubic foot (d) ounce or gram (e) kilometer or mile (f) meter or yard",
          "(a) inch (b) liter (c) cubic foot (d) ounce (e) mile (f) meter", 18),
         ("50 cm = ____ in", "19.7 in (divide by 2.54)", 8), ("50 L = ____ qt", "53 qt (multiply by 1.06)", 8), ("185 lb = ____ kg", "83.9 kg (divide by 2.205)", 8),
         ("12 in = ____ cm", "30.5 cm", 7), ("15 gal = ____ L", "56.8 L", 7), ("26.2 mi = ____ km", "42.2 km", 8),
         ("BONUS. Convert 5 km to inches, to the nearest whole number.", "196,850 in (500,000 cm ÷ 2.54)", 0)]),
    6: ("MUST SHOW SOME WORK FOR FULL CREDIT.",
        [("On a metric rule a point is 6 small marks past the 4. Give the reading in millimeters and in centimeters.", "46 mm; 4.6 cm", 8),
         ("On an inch rule in sixteenths, give each reading in lowest terms: (a) 10 spaces past 0 (b) 11 spaces past 1 (c) 6 spaces past 2 (d) 4 spaces past 3 (e) 2 spaces past 4",
          "(a) 5/8 in (b) 1 11/16 in (c) 2 3/8 in (d) 3 1/4 in (e) 4 1/8 in", 20),
         ("A gauge is numbered 0, 200, 400 … with 4 spaces between numbers. What is each space worth?", "50", 8),
         ("On that gauge the needle is a little less than half a space past 850. Estimate the reading.", "about 870", 8),
         ("A voltmeter is numbered every 100 with 4 spaces between numbers. The needle is 3 spaces past 300. Give the reading.", "375 volts", 8),
         ("A dual-scale gauge reads 6,000 kPa. About what should its psi scale read? (1 psi is about 6.9 kPa.)", "about 870 psi", 8),
         ("A hole is specified as 0.81 in ± 0.003 in. Find the limits.", "0.807 in to 0.813 in", 10),
         ("Will a 13/16-in hole be within the specification in the previous question? Show why.", "Yes. 13/16 = 0.8125, which is between 0.807 and 0.813.", 10),
         ("Overall length 78 3/4 in; known parts 11.25 in and 31 3/8 in. Find the missing length. No rounding.", "36.125 in", 12),
         ("A 150-Ω resistor has a tolerance of ±10%. Find its limits.", "135 Ω to 165 Ω", 8),
         ("BONUS. A 24-in bar has 7 holes equally spaced, with the end holes 1.5 in from each end. Find the spacing.", "3.5 in", 0)]),
    7: ("MUST SHOW 3 CALCULATIONS BEFORE FINAL EVALUATION.",
        [("Describe the sequence of steps in the order of operations.", "Parentheses (grouping symbols); exponents and roots; multiply or divide, whichever comes first, left to right; add or subtract, whichever comes first, left to right", 12),
         ("6 + 4 ÷ 2", "8", 6), ("20 − 8 + 5", "17", 6), ("24 ÷ 4 × 2", "12", 6), ("3 + 5 × 2²", "23", 8),
         ("5 − 3(4² ÷ 2) + 30", "11", 10), ("7 − 2(3² − 4) + 15", "12", 10), ("√(36 + 64)", "10", 8),
         ("(12 − 3(4² ÷ 2³) + 9) ÷ (5² − 10)   Round to the nearest 100th if needed.", "1", 12),
         ("(5 + 12 ÷ 4 × 15 + 15²) ÷ 6   Round to the nearest 100th if needed.", r(275 / 6, 2), 12),
         ("3[20 − 2(4 + 3)]", "18", 10),
         ("BONUS. Is 3(4)² equal to 144 or 48? Explain.", "48. The exponent applies only to the 4: 3 × 16.", 0)]),
    8: ("YOU MUST SHOW ALL SUBSTITUTIONS.",
        [("Substitute and evaluate: L = 3A + 4(B + C);  A = 2, B = 3, C = 4", "34", 9),
         ("Substitute and evaluate (mixed number or non-rounded decimal): 2C + 1.6(D + d) + (D + d)/(4C);  C = 30 in, D = 10 in, d = 5 in", "84.125 in (84 1/8 in)", 11),
         ("N = (a + b)(a − b);  a = 7, b = 12", "−95", 9), ("V = gt²/2;  g = 32.2, t = 4.1", n(32.2 * 4.1 ** 2 / 2), 9),
         ("Plumbing. N = √(D ÷ d)⁵. How many 3-in pipes equal one 15-in pipe? Nearest whole number.", "56 pipes", 11),
         ("Manufacturing. C = W²DS ÷ 1.085;  W = 2 m, D = 500 kg/m³, S = 3 m/s. Nearest whole number.", r(4 * 500 * 3 / 1.085, 0) + " metric tons per hour", 11),
         ("Hydraulics. F = πPD² ÷ 4;  P = 25 psi, D = 3 in, π = 3.14. Nearest whole number.", r(3.14 * 25 * 9 / 4, 0) + " lb", 10),
         ("Electronics. C_{T} = C_{1}(C_{2} + C_{3}) ÷ (C_{1} + C_{2} + C_{3});  C_{1} = 16, C_{2} = 6, C_{3} = 8. Nearest 100th.", r(16 * 14 / 30, 2) + " µF", 10),
         ("Machine trades. L = πdr ÷ 12;  d = 6.0 in, r = 2500 rpm, π = 3.14. Round to the nearest hundred.", "3,900 ft/min (3,925 before rounding)", 10),
         ("Construction. L = 25T⁴ ÷ H²;  T = 6 in, H = 12 ft.", "225 tons", 10),
         ("BONUS. Hero’s Formula A = √(s(s − a)(s − b)(s − c)) for sides 15 m, 20 m, 25 m.", "150 m² (s = 30)", 0)]),
    9: ("SHOW ALL SUBSTITUTIONS AND SOME WORK.",
        [("x + 14.5 = 32", "17.5", 6), ("7m = 94.5", "13.5", 6), ("4x + 7 = 39", "8", 8),
         ("Electrical. I = E/R;  I = 0.80 A, R = 450 Ω. Find E.", "360 V", 9), ("Aviation. D = RT;  D = 1240 mi, R = 220 mph. Find T to the nearest thousandth.", r(1240 / 220, 3) + " h", 9),
         ("V = LWH;  V = 3882 cu ft, L = 52.6 ft, W = 9.0 ft. Find H to the nearest 10th.", "8.2 ft", 11),
         ("P = 2L + 2W;  W = 500 ft, P = 3500 ft. Find L.", "1,250 ft", 11),
         ("Office services. T = 45 + 60H;  T = $375. Find H.", "5.5 h", 10),
         ("Machine trades. L = 2d + 3.26(r + R);  r = 8 in, R = 6 in, L = 82 in. Find d to the nearest inch.", "18 in (18.18)", 10),
         ("Meteorology. T = −0.002H + G;  G = 76°F, T = 32°F. Find H.", "22,000 ft", 10),
         ("Sheet metal. A = 2w + 3/16;  A = 7/8 in. Find w as a fraction in lowest terms or a non-rounded decimal.", "11/32 in (0.34375 in)", 10),
         ("BONUS. Sheet metal. A = 2w + 3/16;  A = 11/16 in. Find w.", "1/4 in", 0)]),
    10: ("SHOW THE FORMULA AND THE SUBSTITUTION.",
         [("Rectangle: L = 30 in, W = 14 in. Find P and A.", "P = 88 in; A = 420 sq in", 12), ("Square: s = 7.5 ft. Find P and A.", "P = 30 ft; A = 56.25 sq ft", 12),
          ("Parallelogram: b = 18 in, a = 10 in, h = 8 in. Find P and A.", "P = 56 in; A = 144 sq in", 12),
          ("Trapezoid: b₁ = 12 in, b₂ = 20 in, h = 9 in, slanted sides 9.8 in each. Find P and A.", "P = 51.6 in; A = 144 sq in", 12),
          ("Trapezoid: bases 5 m and 9 m, height 4.5 m. Find A.", "31.5 m²", 8), ("A rectangle has A = 216 sq in and W = 9 in. Find L.", "24 in", 8),
          ("A square has A = 196 sq ft. Find s.", "14 ft", 8), ("A trapezoid has A = 150 sq ft and bases 10 ft and 15 ft. Find h.", "12 ft", 10),
          ("A room is 12 ft by 15 ft. How many square yards of carpet does it need?", "20 sq yd", 9),
          ("A wall 24 ft by 8 ft has a door 3 ft by 7 ft. How many square feet are painted?", "171 sq ft", 9),
          ("BONUS. A trapezoid has A = 126 sq in, h = 9 in and one base 11 in. Find the other base.", "17 in", 0)]),
    11: ("SHOW THE FORMULA AND THE SUBSTITUTION.",
         [("Name the triangle with (a) no equal sides (b) two equal sides (c) three equal sides.", "(a) scalene (b) isosceles (c) equilateral", 9),
          ("Triangle: b = 16 in, h = 9 in. Find A.", "72 sq in", 9), ("Triangle with sides 9 cm, 12 cm, 17 cm. Find P.", "38 cm", 7),
          ("Hero’s Formula: sides 15 m, 20 m, 25 m. Find A.", "150 m²", 12), ("Hero’s Formula: sides 13, 14, 15 ft. Find A.", "84 sq ft", 12),
          ("Hero’s Formula: sides 7, 10, 12 m. Find A to the nearest tenth.", r(hero(7, 10, 12), 1) + " m²", 12),
          ("Equilateral triangle: s = 8 in. Find P and A.", "P = 24 in; A = 27.712 sq in", 10),
          ("Right triangle: legs 5 ft and 12 ft. Find the hypotenuse.", "13 ft", 9), ("Right triangle: c = 20 ft, one leg 16 ft. Find the other leg.", "12 ft", 10),
          ("A roof rises 6 ft over a run of 14 ft. Find the rafter length to the nearest hundredth.", r(sqrt(232), 2) + " ft", 10),
          ("BONUS. An isosceles triangle has sides 13, 13 and base 10 ft. Find its height and area.", "h = 12 ft; A = 60 sq ft", 0)]),
    12: ("SHOW THE FORMULA AND THE SUBSTITUTION. Use π = 3.14.",
         [("Circle: d = 14 in. Find C and A.", "C = 43.96 in; A = 153.86 sq in", 12), ("Circle: r = 5 cm. Find A.", "78.5 cm²", 7),
          ("Circle: C = 157 in. Find d.", "50 in", 8), ("Circle: A = 200 sq in. Find r to the nearest tenth.", "8.0 in", 9),
          ("Hexagon: s = 0.75 in. Find P, A, d and f.", "P = 4.5 in; A = 1.4625 sq in; d = 1.5 in; f = 1.299 in", 12),
          ("A hexagon has an area of 500 sq m. Find s to the nearest tenth.", "13.9 m", 9),
          ("An L-shaped floor is 20 ft by 14 ft overall with an 8 ft by 6 ft corner missing. Split it into two trapezoids and find the area.",
           "(14 + 6)(12) ÷ 2 = 120 and (8 + 20)(8) ÷ 2 = 112; total 232 sq ft", 12),
          ("A 30 in by 20 in plate has an 18 in by 10 in opening. Find the remaining area.", "420 sq in", 8),
          ("A ring has an outside radius of 8 ft and an inside radius of 5 ft. Find its area.", "122.46 sq ft", 9),
          ("A window is a rectangle 4 ft wide and 5 ft tall with a semicircle on top. Find its area.", "26.28 sq ft", 9),
          ("Find the perimeter of the L-shaped floor above.", "68 ft", 5),
          ("BONUS. A nut measures 1.5 in across the flats. Find the length of a side to the nearest hundredth.", "0.87 in", 0)]),
}


def _frac(t):
    """3/8 -> stacked fraction markup, leaving dates and units such as ft/min alone"""
    import re
    return re.sub(r"(?<![\w/.])(\d+)/(\d+)(?![\w/])", r"[[\1|\2]]", t)


def add_tests():
    titles = {b["n"]: b["title"] for k, b in book.BLOCKS if k == "chapter"}
    pdf = ['<section class="appendix"><h1 id="tests">Chapter tests and keys</h1>'
           '<p>One test for each chapter, each followed by its key. The tests follow the wording and rounding instructions of the course exams. '
           'Point values total 100 without the bonus. Permission is given to copy the test pages for classroom use.</p></section>']
    docx = ["<h1>Chapter tests and keys</h1>"]
    for ch in sorted(TESTS):
        inst, items = TESTS[ch]
        total = sum(p for _, _, p in items)
        assert total == 100, (ch, total)
        qs = "".join(f'<li>{fmt(_frac(q))}<span class="pts">({p} points)</span></li>' if p else f"<li>{fmt(_frac(q))}</li>" for q, a, p in items)
        ks = "".join(f'<li><span class="ta" style="margin-left:0">{fmt(_frac(a))}</span></li>' for q, a, p in items)
        head = (f'<div class="thead"><h2>Chapter {ch} Test: {fmt(titles[ch])}</h2><div class="sm">APPLIED TECHNICAL MATH</div></div>')
        pdf.append(f'<section class="test">{head}<div class="nm">Name&nbsp;<span></span>Date&nbsp;<span></span>Score&nbsp;<span style="flex:0 0 60pt"></span></div>'
                   f'<div class="inst">{fmt(inst)}</div><ol>{qs}</ol></section>')
        pdf.append(f'<section class="test key">{head.replace("Test:", "Test KEY:")}<ol style="column-count:2;column-gap:24pt">{ks}</ol></section>')
        f = lambda x: fmt(_frac(x), "docx")  # noqa: E731
        docx.append(f"<h2>Chapter {ch} Test: {f(titles[ch])}</h2><p>Name ______________________   Date ____________   Score ______</p><p><b>{f(inst)}</b></p><ol>"
                    + "".join(f"<li>{f(q)}" + (f" ({p} points)" if p else "") + "</li>" for q, a, p in items) + "</ol>"
                    + f"<h3>Chapter {ch} Test: key</h3><ol>" + "".join(f"<li>{f(a)}</li>" for q, a, p in items) + "</ol>")
    book.raw("".join(pdf), "".join(docx), toc=("tests", "Chapter tests and keys"))
