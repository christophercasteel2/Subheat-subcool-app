"""Back matter: the reference pages."""
from book import raw, fmt


def T(title, head, rows, small=True):
    h = "<tr>" + "".join(f"<th>{fmt(x)}</th>" for x in head) + "</tr>"
    b = "".join("<tr>" + "".join(f"<td>{fmt(c)}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="tablewrap"><div class="tcap">{fmt(title)}</div><table class="data{" small" if small else ""}">{h}{b}</table></div>',
            f"<p><b>{fmt(title, 'docx')}</b></p><table><tr>" + "".join(f"<th>{fmt(x, 'docx')}</th>" for x in head) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{fmt(c, 'docx')}</td>" for c in r) + "</tr>" for r in rows) + "</table>")


tabs = [
    T("Standard units", ["Length", "Weight", "Liquid capacity"],
      [["1 ft = 12 in", "1 lb = 16 oz", "1 pt = 2 cups"], ["1 yd = 3 ft = 36 in", "1 T = 2000 lb", "1 qt = 2 pt"],
       ["1 mi = 5280 ft = 1760 yd", "", "1 gal = 4 qt"]]),
    T("Area and volume", ["Area", "Volume", "Volume and capacity"],
      [["1 sq ft = 144 sq in", "1 cu ft = 1728 cu in", "1 cu ft = 7.48 gal"], ["1 sq yd = 9 sq ft", "1 cu yd = 27 cu ft", "1 gal = 231 cu in"],
       ["1 sq yd = 1296 sq in", "1 cu yd = 46,656 cu in", ""]]),
    T("Metric stairs (each step is one decimal place)", ["kilo", "hecto", "deka", "unit", "deci", "centi", "milli"],
      [["1000", "100", "10", "1", "0.1", "0.01", "0.001"], ["km", "hm", "dam", "m", "dm", "cm", "mm"], ["kg", "hg", "dag", "g", "dg", "cg", "mg"],
       ["kL", "hL", "daL", "L", "dL", "cL", "mL"]]),
    T("Standard and metric", ["Length", "Weight", "Capacity"],
      [["1 in = 2.54 cm", "1 oz = 28.35 g", "1 L = 1.06 qt"], ["1 m = 3.28 ft", "1 kg = 2.205 lb", "1 gal = 3.785 L"], ["1 mi = 1.61 km", "", ""]]),
    T("Every conversion in both directions", ["Category", "Multiply by the factor", "Divide by the factor", "Factor"],
      [["Length", "ft → in", "in → ft", "12"], ["Length", "yd → ft", "ft → yd", "3"], ["Length", "mi → ft", "ft → mi", "5280"],
       ["Weight", "lb → oz", "oz → lb", "16"], ["Weight", "T → lb", "lb → T", "2000"],
       ["Capacity", "gal → qt;  qt → pt;  pt → cups", "qt → gal;  pt → qt;  cups → pt", "4;  2;  2"],
       ["Area", "sq ft → sq in", "sq in → sq ft", "144"], ["Area", "sq yd → sq ft", "sq ft → sq yd", "9"], ["Area", "sq yd → sq in", "sq in → sq yd", "1296"],
       ["Volume", "cu ft → cu in", "cu in → cu ft", "1728"], ["Volume", "cu yd → cu ft", "cu ft → cu yd", "27"],
       ["Volume", "cu ft → gal", "gal → cu ft", "7.48"], ["Volume", "gal → cu in", "cu in → gal", "231"],
       ["Metric length", "in → cm", "cm → in", "2.54"], ["Metric length", "m → ft", "ft → m", "3.28"], ["Metric length", "mi → km", "km → mi", "1.61"],
       ["Metric weight", "oz → g", "g → oz", "28.35"], ["Metric weight", "kg → lb", "lb → kg", "2.205"],
       ["Metric capacity", "L → qt", "qt → L", "1.06"], ["Metric capacity", "gal → L", "L → gal", "3.785"]]),
    T("Percent", ["To find", "Proportion", "Shortcut"],
      [["the part", "[[x|whole]] = [[percent|100]]", "whole × percent as a decimal"], ["the whole", "[[part|x]] = [[percent|100]]", "part ÷ percent as a decimal"],
       ["the percent", "[[part|whole]] = [[x|100]]", "part ÷ whole, point 2 places right"]]),
    T("Geometry formulas (π = 3.14)", ["Figure", "Perimeter", "Area"],
      [["Rectangle", "P = 2L + 2W", "A = LW"], ["Square", "P = 4s", "A = s²"], ["Parallelogram", "P = 2a + 2b", "A = bh"],
       ["Trapezoid", "P = sum of the sides", "A = (b_{1} + b_{2})h ÷ 2"], ["Triangle", "P = a + b + c", "A = bh ÷ 2"],
       ["Triangle from three sides (Hero)", "s = (a + b + c) ÷ 2", "A = √(s(s − a)(s − b)(s − c))"], ["Equilateral triangle", "P = 3s", "A = 0.433s²"],
       ["Right triangle", "a² + b² = c²", "A = ab ÷ 2"], ["Regular hexagon", "P = 6s;  d = 2s;  f = 1.732s", "A = 2.6s²"],
       ["Circle", "C = πd = 2πr;  d = 2r", "A = πr²"]]),
    T("Trade formulas used in this book", ["Trade", "Formula", "Meaning"],
      [["Machine trades", "L = πdr ÷ 12", "linear speed of a wheel, ft/min (d in, r rpm)"], ["Construction", "L = 25T⁴ ÷ H²", "crushing load of a square post, tons"],
       ["Welding", "T = L ÷ A", "tensile strength, psi"], ["Plumbing", "N = √(D ÷ d)⁵", "small pipes equal to one large pipe"],
       ["Manufacturing", "C = W²DS ÷ 1.085", "feeder belt capacity, metric tons per hour"], ["Hydraulics", "F = πPD² ÷ 4", "force on a piston, lb"],
       ["Electronics", "C_{T} = C_{1}(C_{2} + C_{3}) ÷ (C_{1} + C_{2} + C_{3})", "series-parallel capacitance"],
       ["Electronics", "L_{T} = L_{1}L_{2} ÷ (L_{1} + L_{2})", "two inductors in parallel"], ["Electronics", "L = R²N² ÷ (9R + 10D)", "inductance of a coil, µH"],
       ["Electrical", "I = E ÷ R", "Ohm’s law"], ["Automotive", "ihp = MEP × D × S ÷ 792,000", "indicated horsepower"],
       ["Machine trades", "L = 2d + 3.26(r + R)", "belt length around two pulleys"], ["Sheet metal", "A = 2w + [[3|16]]", "Pittsburgh lock allowance, in"],
       ["Water/wastewater", "P = 0.52D + 14.7", "pressure at depth D ft, psi"]]),
    T("Order of operations and rounding", ["Rule", "Remember"],
      [["Order of operations", "1 grouping symbols; 2 exponents and roots; 3 × and ÷ left to right; 4 + and − left to right"],
       ["Rounding", "Find the rounding digit; look one digit right; 5 or more rounds up, 4 or less stays; zeros for whole places, drop decimal places"],
       ["Solving", "Substitute, simplify, undo + and − first, then × and ÷; do the same to both sides; check"]]),
]
raw('<section class="appendix"><span class="mk">@@ref@@</span><h1 id="ref">Reference tables and formulas</h1>'
    '<p>Everything on these pages is developed in the chapters. They are collected here for quick use.</p>'
    + "".join(t[0] for t in tabs) + "</section>",
    "<h1>Reference tables and formulas</h1>" + "".join(t[1] for t in tabs), toc=("ref", "Reference tables and formulas"))
