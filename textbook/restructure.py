"""Regroups the written material into the instructor's seven chapters.

The content modules are written as small 'source chapters' (place value, fractions, the percent
proportion ...). This pass gathers them into seven chapters, each made of numbered sections,
renumbers every example, figure, table and practice set by its new chapter, and rewrites the
cross-references inside the text to the new numbers."""
import re
import book

# ---------------------------------------------------------------- the plan
# each chapter: number, title, (unused note), colour, intro, sections
# each section: (title, source chapter, which source sections (None = all), split filter or None)
PCT = re.compile(r"%|percent|Percent")
TOL = re.compile(r"^(?!.*(?:gauge|mark|[Rr]ule|scale|sixteenths|[Gg]raduation))(?:.|\n)*?(?:[Ll]imit|[Tt]olerance|[Mm]issing|Overall|overall length|spaces|holes|spacing|acceptable|±|nominal)")

CHAPTERS = [
    (1, "Whole Numbers, Fractions and Decimals", None, "#c8452f",
     "Every measurement, price and specification is a number written in the base ten system. This chapter makes sure those numbers "
     "are read, rounded and rewritten correctly, that fractions and decimals can be added, subtracted and compared, and that a "
     "toleranced dimension can be checked, before any formula work begins.",
     [("Place Value and Rounding", 1, None, None),
      ("Fractions and Decimals", 2, ["2.1", "2.2", "2.3", "2.6", "2.7", "2.8", "2.10"], ("not", PCT)),
      ("Tolerance and Missing Dimensions", 6, ["6.4", "6.5", "6.8", "6.9"], ("only", TOL))]),
    (2, "Ratio, Proportion and Percent", None, "#d98a14",
     "Ratios compare two quantities, proportions say that two ratios are equal, and a percent is a ratio to 100. One idea, "
     "cross-multiplying, solves gear and pulley problems, scale drawings, mixtures and every kind of percent problem.",
     [("Ratio and Proportion", 14, None, None),
      ("Fractions, Decimals and Percents", 2, ["2.4", "2.5", "2.9"], ("only", PCT)),
      ("The Percent Proportion", 3, None, None)]),
    (3, "Measurement", None, "#2f8f4e",
     "Measuring is counting units. This chapter covers the two systems of units used in American shops, the metric stairs, "
     "conversions between the systems, and how to read the rules, meters and gauges that do the measuring.",
     [("Standard Units of Measure", 4, None, None),
      ("The Metric System", 5, None, None),
      ("Rulers, Meters and Gauges", 6, ["6.1", "6.2", "6.3", "6.6", "6.7"], ("not", TOL))]),
    (4, "Basic Algebra", None, "#1f6fb5",
     "A formula is a set of instructions written in symbols. This chapter covers the order in which those instructions are carried "
     "out (PEMDAS), how to put numbers into a formula and evaluate it, and how to run a formula backward to solve for a missing value.",
     [("Order of Operations", 7, None, None),
      ("Evaluating Formulas", 8, None, None),
      ("Solving Formulas", 9, None, None)]),
    (5, "Practical Plane Geometry", None, "#7453b8",
     "How much trim goes around it? How much material covers it? This chapter answers those two questions, perimeter and area, "
     "for every flat shape met in the trades, from the rectangle to the hexagon and the composite figure.",
     [("Perimeter and Area of Quadrilaterals", 10, None, None),
      ("Triangles", 11, None, None),
      ("Circles, Hexagons and Composite Figures", 12, None, None)]),
    (6, "Solid Figures", None, "#0f8a8a",
     "Tanks, ducts, hoppers, pipe and bar stock are not flat. This chapter stands the flat shapes of Chapter 5 up into solids "
     "and finds how much material covers them, how much they hold, and how much they weigh.",
     [("Solid Geometry", 13, None, None)]),
    (7, "Triangle Trigonometry", None, "#b5376d",
     "Trigonometry finds the parts of a triangle that cannot be measured with a tape: the angle of a ramp, the length of a rafter "
     "from its pitch, the travel of a conduit offset. It starts with angles and three ratios of the sides of a right triangle.",
     [("Angles", 15, None, None),
      ("The Trigonometric Ratios", 16, None, None),
      ("Solving Right Triangles", 17, None, None),
      ("Oblique Triangles", 18, None, None)]),
]

# where each cumulative review goes, with its new title
MIXED = {"Part 1 · Numbers": (2, "Mixed review: Chapters 1 and 2", "Mixed problems from Chapters 1 and 2."),
         "Part 2 · Measurement": (3, "Mixed review: Chapter 3", "Mixed problems from Chapter 3, with tolerance from Chapter 1. Round to the nearest tenth if needed."),
         "Part 3 · Algebra": (4, "Mixed review: Chapter 4", "Mixed problems from Sections 4.1, 4.2 and 4.3."),
         "Part 4 · Geometry": (6, "Mixed review: Chapters 5 and 6", "Mixed problems from Chapters 5 and 6. Use π = 3.14. Round only where told to.")}

# opening text for sections that are split out of a source chapter
SPLIT_INTRO = {
    ("Fractions and Decimals", 2): "Five-eighths of an inch and 0.625 inch are the same length written two ways. Tape measures use fractions "
                                   "and calculators use decimals, so a technician has to move between them without hesitation.",
    ("Fractions, Decimals and Percents", 2): "A percent is a fraction with a denominator of 100. Specifications, efficiencies and discounts are given "
                                             "as percents, so every percent problem starts by moving between the three forms.",
    ("Tolerance and Missing Dimensions", 6): "Nothing can be made to an exact size. This section is about deciding whether a measurement is close "
                                             "enough, and about finding the dimension a drawing leaves out.",
    ("Rulers, Meters and Gauges", 6): None,
}

SEC_ID = re.compile(r"^(\d+)\.(\d+)\s+")
MAPS = {"Figure": {}, "Example": {}, "Practice": {}, "Table": {}, "Chapter": {}}


def _split(items, filt):
    if not filt:
        return list(items)
    mode, rx = filt
    return [x for x in items if bool(rx.search(x if isinstance(x, str) else " ".join(map(str, x)))) == (mode == "only")]


def _collect():
    """cut the written material into source chapters"""
    src = {}
    cur, curid = None, None
    for kind, b in book.BLOCKS:
        if kind == "part":
            continue
        if kind == "chapter":
            cur = src.setdefault(b["n"], {"open": b, "secs": [], "summary": None, "review": None, "pre": []})
            curid = None
            continue
        if kind == "raw":
            src.setdefault("back", []).append((kind, b))
            continue
        if kind == "practice" and b["tag"] == "CUMULATIVE REVIEW":
            src.setdefault("mixed", []).append((kind, b))
            continue
        if kind == "sec":
            m = SEC_ID.match(b["title"])
            curid = f"{m.group(1)}.{m.group(2)}" if m else b["title"]
            cur["secs"].append((curid, [(kind, b)]))
            continue
        if kind == "summary":
            cur["summary"] = b
            curid = None
            continue
        if kind == "review":
            cur["review"] = b
            continue
        if curid is None:
            cur["pre"].append((kind, b))
        else:
            cur["secs"][-1][1].append((kind, b))
    return src


def build():
    src = _collect()
    out = []
    for cn, ctitle, tnote, color, intro, sections in CHAPTERS:
        units = []
        pool = []
        for i, (stitle, s, ids, filt) in enumerate(sections, start=1):
            units.append((f"{cn}.{i}", stitle))
        out.append(("chapter", dict(n=cn, title=ctitle, textbook=tnote, color=color, intro=intro, units=units,
                                    objectives=[], terms=[], _fresh=True)))
        for i, (stitle, s, ids, filt) in enumerate(sections, start=1):
            sid = f"{cn}.{i}"
            c = src[s]
            op = c["open"]
            MAPS["Chapter"].setdefault(op["n"], f"Section {sid}")
            intro_u = SPLIT_INTRO.get((stitle, s), op["intro"]) or op["intro"]
            out.append(("unit", dict(n=sid, title=stitle, intro=intro_u, color=color, src=s,
                                     objectives=_split(op["objectives"], filt), terms=_split(op["terms"], filt))))
            out += _keep(c["pre"]) if ids is None or i == 1 else []
            for secid, blocks in c["secs"]:
                if ids is None or secid in ids:
                    k, b0 = blocks[0]
                    out.append(("sec", dict(b0, title=SEC_ID.sub("", b0["title"]))))
                    out += _keep(blocks[1:])
            if c["summary"]:
                pts = _split(c["summary"]["points"], filt)
                if pts:
                    out.append(("summary", dict(points=pts, n=sid)))
            if c["review"]:
                rv = c["review"]
                pool.append([(q, a) for q, a in zip(rv["items"], rv["answers"])
                             if (not filt or _split([q], filt)) and not ALONE.search(q)])
        out.append(("review", dict(n=cn, items=[], answers=[], _pool=pool, _fresh=True)))
    out += src.get("back", [])
    for kind, b in out:
        if kind == "review":
            b["items"], b["answers"] = _choose(b.pop("_pool"))
    _renumber(out)
    book.BLOCKS[:] = out
    _answers()


def _renumber(blocks):
    ch = None
    cnt = {}
    for i, (kind, b) in enumerate(blocks):
        if kind == "chapter":
            ch = b["n"]
            cnt = {"ex": 0, "fig": 0, "set": 0, "tab": 0}
            b["ch"] = ch
        elif kind == "example":
            cnt["ex"] += 1
            new = f"{ch}.{cnt['ex']}"
            MAPS["Example"].setdefault(b["n"], new)
            blocks[i] = (kind, dict(b, n=new, _old=b["n"]))
        elif kind == "fig":
            cnt["fig"] += 1
            new = f"{ch}.{cnt['fig']}"
            MAPS["Figure"].setdefault(b["n"], new)
            blocks[i] = (kind, dict(b, n=new, _old=b["n"]))
        elif kind == "practice" and b["tag"] != "CUMULATIVE REVIEW":
            cnt["set"] += 1
            new = f"{ch}.{cnt['set']}"
            MAPS["Practice"].setdefault(b["label"], new)
            blocks[i] = (kind, dict(b, label=new, tag=f"PRACTICE {new}", _old=b["label"]))
        elif kind == "table" and b.get("caption"):
            m = re.match(r"Table (\d+\.\d+)( \(continued\))?\s+", b["caption"])
            if m:
                if not m.group(2):
                    cnt["tab"] += 1
                new = f"{ch}.{cnt['tab']}"
                MAPS["Table"].setdefault(m.group(1), new)
                blocks[i] = (kind, dict(b, caption=f"Table {new}{m.group(2) or ''}  " + b["caption"][m.end():]))
    # the new chapters' own material was written with new numbers already; only the regrouped text is rewritten
    for i, (kind, b) in enumerate(blocks):
        if not b.get("_fresh"):
            blocks[i] = (kind, _rewrite(b))


REF = re.compile(r"\b(Figures?|Examples?|Practice|Tables?)\s+(\d+\.\d+(?:\s*(?:,|and|to)\s*\d+\.\d+)*)")
CHREF = re.compile(r"\bChapters? (\d+)((?:,? (?:and|to) \d+)?)(?! (?:exam|handout|classwork|Test|test))(?!:)")


def rewrite_text(t):
    if not isinstance(t, str):
        return t

    def one(m):
        word = m.group(1)
        kind = {"Figure": "Figure", "Figures": "Figure", "Example": "Example", "Examples": "Example", "Practice": "Practice",
                "Table": "Table", "Tables": "Table"}[word]
        nums = re.sub(r"\d+\.\d+", lambda x: MAPS[kind].get(x.group(0), x.group(0)), m.group(2))
        return f"{word} {nums}"

    def chap(m):
        a = int(m.group(1))
        rest = m.group(2)
        if a not in MAPS["Chapter"]:
            return m.group(0)
        if rest:
            b = int(re.search(r"\d+", rest).group(0))
            joiner = " and " if "and" in rest else " to "
            first, last = MAPS["Chapter"][a].split()[1], MAPS["Chapter"].get(b, f"Section {b}").split()[1]
            if first.split(".")[0] != last.split(".")[0]:
                return f"Chapters {first.split('.')[0]}{joiner}{last.split('.')[0]}"
            return f"Sections {first}{joiner}{last}"
        return MAPS["Chapter"][a]

    t = REF.sub(one, t)
    t = CHREF.sub(chap, t)
    t = t.replace("This chapter", "This section").replace("this chapter", "this section")
    return t


def _rewrite(o):
    if isinstance(o, str):
        return rewrite_text(o)
    if isinstance(o, dict):
        return {k: (v if k in ("svg",) else _rewrite(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [_rewrite(x) for x in o]
    if isinstance(o, tuple):
        return tuple(_rewrite(x) for x in o)
    return o


# questions that only make sense next to the question before them, or that need a practice-set figure
ALONE = re.compile(r"previous|Same |that gauge|problem \d|above|Figure|\bthat (prism|cylinder|gauge)")
REVIEW_SIZE = 20


def _keep(blocks):
    """drop section practice sets and the figures drawn only for them"""
    return [(k, b) for k, b in blocks
            if k != "practice" and not (k == "fig" and "for Practice" in b.get("caption", ""))]


def _choose(pools):
    """a short chapter review: questions spread evenly through each section's review"""
    pools = [p for p in pools if p]
    per = -(-REVIEW_SIZE // max(1, len(pools)))
    out = []
    for p in pools:
        k = min(per, len(p))
        idx = sorted({round(i * (len(p) - 1) / max(1, k - 1)) for i in range(k)}) if k > 1 else [0]
        out += [p[i] for i in idx]
    seen, uniq = set(), []
    for q, a in out:
        if q not in seen:
            seen.add(q)
            uniq.append((q, a))
    return [q for q, _ in uniq], [a for _, a in uniq]


def _answers():
    book.ANSWERS[:] = []
    title = ""
    ch = 0
    for kind, b in book.BLOCKS:
        if kind == "chapter":
            ch, title = b["n"], b["title"]
        elif kind == "review":
            book.ANSWERS.append((ch, title, f"Chapter {b['n']} review", b["answers"]))
