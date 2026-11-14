"""A small kit for writing the textbook: chapters are written as calls
(chapter, sec, p, example, practice ...) that collect blocks, and the
blocks are turned into HTML for the print PDF or simpler HTML for Word."""
import html
import re

BLOCKS = []          # everything in the book, in order
ANSWERS = []         # (chapter number, chapter title, set title, [answers])
FIGS = []            # svg text of every figure (for the Word copy's pictures)
_state = {"ch": 0, "title": "", "color": "#1f5fbf", "fig": 0, "ex": 0, "set": 0}

COLORS = ["#c8452f", "#d98a14", "#2f8f4e", "#1f6fb5", "#7453b8", "#0f8a8a",
          "#b5376d", "#3f51b5", "#8a5a2b", "#2e7d6b", "#a63d40", "#4a6fa5"]


# ---------------------------------------------------------------- text

def fmt(t, mode="pdf"):
    """inline markup: **bold**, *italic*, `value`, [[a|b]] a stacked
    fraction, ^{..} raised, _{..} lowered"""
    t = html.escape(t, quote=False).replace("&lt;br&gt;", "<br>").replace("&amp;gt;", "&gt;").replace("&amp;lt;", "&lt;")
    if mode == "pdf":
        t = re.sub(r"\[\[(.+?)\|(.+?)\]\]", r'<span class="fr"><span>\1</span><span>\2</span></span>', t)
    else:
        t = re.sub(r"\[\[(.+?)\|(.+?)\]\]", r"\1/\2", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r'<span class="val">\1</span>', t)
    t = re.sub(r"\^\{(.+?)\}", r"<sup>\1</sup>", t)
    t = re.sub(r"_\{(.+?)\}", r"<sub>\1</sub>", t)
    return t


def num(x, places=None):
    """a number the way it is written in the book: no trailing zeros"""
    if places is not None:
        s = f"{x:,.{places}f}"
        return s
    s = f"{x:,.6f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


# ---------------------------------------------------------------- blocks

def add(_k, **kw):
    BLOCKS.append((_k, kw))


def part(title, blurb):
    add("part", title=title, blurb=blurb)


def chapter(title, objectives, intro, terms=None):
    _state["ch"] += 1
    _state.update(title=title, color=COLORS[(_state["ch"] - 1) % len(COLORS)], fig=0, ex=0, set=0)
    add("chapter", n=_state["ch"], title=title, objectives=objectives, intro=intro,
        terms=terms or [], color=_state["color"])


def sec(title):
    add("sec", title=title, n=_state["ch"])


def sub(title):
    add("sub", title=title)


def p(*paras):
    for t in paras:
        add("p", text=t)


def bullets(items, ordered=False):
    add("list", items=items, ordered=ordered)


def eq(*lines):
    """displayed work, a line under a line"""
    add("eq", lines=lines)


def rule(title, *body):
    add("box", box="rule", title=title, body=body)


def warn(title, *body):
    add("box", box="warn", title=title, body=body)


def tip(title, *body):
    add("box", box="tip", title=title, body=body)


def handout(title, *body):
    """the instructor's own wording, copied exactly from a class handout"""
    add("box", box="handout", title=title, body=body)


def shop(title, *body):
    add("box", box="shop", title=title, body=body)


def example(problem, steps, answer, title=None):
    """a worked example: steps are (work, why) pairs"""
    _state["ex"] += 1
    add("example", n=f'{_state["ch"]}.{_state["ex"]}', title=title, problem=problem, steps=steps, answer=answer)


def table(headers, rows, widths=None, caption=None, small=False):
    add("table", headers=headers, rows=rows, widths=widths, caption=caption, small=small)


def fig(svg, caption, width=None):
    _state["fig"] += 1
    FIGS.append(svg)
    add("fig", svg=svg, n=f'{_state["ch"]}.{_state["fig"]}', caption=caption, idx=len(FIGS) - 1, width=width)


def practice(title, intro, items, cols=2):
    """a practice set: items are (question, answer) pairs; the answers go
    to the key at the back"""
    _state["set"] += 1
    label = f'{_state["ch"]}.{_state["set"]}'
    add("practice", label=label, title=title, intro=intro, items=[q for q, _ in items], cols=cols)
    ANSWERS.append((_state["ch"], _state["title"], f"Practice {label}: {title}", [a for _, a in items]))


def review(items):
    """the chapter review: (question, answer) pairs"""
    add("review", n=_state["ch"], items=[q for q, _ in items])
    ANSWERS.append((_state["ch"], _state["title"], "Chapter review", [a for _, a in items]))


def summary(points):
    add("summary", points=points)


def pagebreak():
    add("break")


# ---------------------------------------------------------------- HTML for the PDF

def _box(kind, title, inner):
    label = {"rule": "KEY RULE", "warn": "WATCH OUT", "tip": "CALCULATOR TIP", "shop": "ON THE JOB", "handout": "CLASS HANDOUT"}[kind]
    return (f'<div class="box {kind}"><div class="boxhead"><span class="tag">{label}</span>'
            f'<span class="boxtitle">{fmt(title)}</span></div><div class="boxbody">{inner}</div></div>')


def render_pdf(toc_pages=None):
    out = []
    color = "#1f5fbf"
    for kind, b in BLOCKS:
        if kind == "part":
            out.append(f'<section class="part"><div class="partlabel">APPLIED TECHNICAL MATH</div><h1>{fmt(b["title"])}</h1>'
                       f'<p>{fmt(b["blurb"])}</p></section>')
        elif kind == "chapter":
            color = b["color"]
            obj = "".join(f"<li>{fmt(o)}</li>" for o in b["objectives"])
            terms = ""
            if b["terms"]:
                terms = ('<div class="terms"><div class="termhead">Key terms</div><dl>'
                         + "".join(f"<dt>{fmt(t)}</dt><dd>{fmt(d)}</dd>" for t, d in b["terms"]) + "</dl></div>")
            out.append(f'<section class="chapter" style="--c:{color}">'
                       f'<div class="chopen"><div class="chnum">CHAPTER {b["n"]}</div>'
                       f'<h1 id="ch{b["n"]}">{fmt(b["title"])}</h1>'
                       f'<p class="chintro">{fmt(b["intro"])}</p></div>'
                       f'<div class="objectives"><div class="objhead">After this chapter you will be able to</div>'
                       f'<ul>{obj}</ul></div>{terms}')
        elif kind == "sec":
            out.append(f'<h2><span class="secbar"></span>{fmt(b["title"])}</h2>')
        elif kind == "sub":
            out.append(f'<h3>{fmt(b["title"])}</h3>')
        elif kind == "p":
            out.append(f'<p>{fmt(b["text"])}</p>')
        elif kind == "list":
            tag = "ol" if b["ordered"] else "ul"
            out.append(f'<{tag} class="plain">' + "".join(f"<li>{fmt(i)}</li>" for i in b["items"]) + f"</{tag}>")
        elif kind == "eq":
            out.append('<div class="eq">' + "".join(f"<div>{fmt(x)}</div>" for x in b["lines"]) + "</div>")
        elif kind == "box":
            out.append(_box(b["box"], b["title"], "".join(f"<p>{fmt(x)}</p>" for x in b["body"])))
        elif kind == "example":
            steps = "".join(f'<tr><td class="work">{fmt(w)}</td><td class="why">{fmt(y)}</td></tr>' for w, y in b["steps"])
            ttl = f' <span class="extitle">{fmt(b["title"])}</span>' if b["title"] else ""
            out.append(f'<div class="example"><div class="exhead"><span class="exnum">EXAMPLE {b["n"]}</span>{ttl}</div>'
                       f'<div class="exprob">{fmt(b["problem"])}</div>'
                       f'<table class="steps">{steps}</table>'
                       f'<div class="exans"><span>Answer</span> {fmt(b["answer"])}</div></div>')
        elif kind == "table":
            cols = ""
            if b["widths"]:
                cols = "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in b["widths"]) + "</colgroup>"
            head = "<tr>" + "".join(f"<th>{fmt(h)}</th>" for h in b["headers"]) + "</tr>" if b["headers"] else ""
            rows = "".join("<tr>" + "".join(f"<td>{fmt(str(c))}</td>" for c in r) + "</tr>" for r in b["rows"])
            cap = f'<div class="tcap">{fmt(b["caption"])}</div>' if b["caption"] else ""
            out.append(f'<div class="tablewrap">{cap}<table class="data{" small" if b["small"] else ""}">{cols}{head}{rows}</table></div>')
        elif kind == "fig":
            w = f' style="max-width:{b["width"]}"' if b["width"] else ""
            out.append(f'<figure{w}>{b["svg"]}<figcaption><b>Figure {b["n"]}</b> {fmt(b["caption"])}</figcaption></figure>')
        elif kind == "practice":
            items = "".join(f"<li>{fmt(q)}</li>" for q in b["items"])
            out.append(f'<div class="practice"><div class="prhead"><span class="prnum">PRACTICE {b["label"]}</span> '
                       f'{fmt(b["title"])}</div><p class="printro">{fmt(b["intro"])}</p>'
                       f'<ol class="cols{b["cols"]}">{items}</ol></div>')
        elif kind == "review":
            items = "".join(f"<li>{fmt(q)}</li>" for q in b["items"])
            out.append(f'<div class="review"><div class="rvhead">Chapter {b["n"]} review</div>'
                       f'<ol class="cols2">{items}</ol></div></section>')
        elif kind == "summary":
            out.append('<div class="summary"><div class="sumhead">Chapter summary</div><ul>'
                       + "".join(f"<li>{fmt(x)}</li>" for x in b["points"]) + "</ul></div>")
        elif kind == "break":
            out.append('<div class="pb"></div>')
        elif kind == "raw":
            out.append(b["pdf"])
    return "\n".join(out)


def raw(pdf, docx=None, toc=None):
    """toc is (anchor, title) when the block starts a back-matter section"""
    add("raw", pdf=pdf, docx=docx if docx is not None else pdf, toc=toc)


def answers_pdf():
    out = ['<section class="answers"><h1 id="answers">Answers to practice sets and reviews</h1>'
           '<p>Every answer here was worked by the rules in its chapter. Rounded answers say how they were rounded '
           'in the question.</p>']
    last = None
    for ch, title, label, ans in ANSWERS:
        if ch != last:
            out.append(f'<h2 class="anshead">Chapter {ch}: {fmt(title)}</h2>')
            last = ch
        items = "".join(f"<li>{fmt(a)}</li>" for a in ans)
        out.append(f'<div class="ansset"><div class="anslabel">{fmt(label)}</div><ol>{items}</ol></div>')
    out.append("</section>")
    return "\n".join(out)


# ---------------------------------------------------------------- simpler HTML for Word

def render_docx():
    f = lambda t: fmt(t, "docx")  # noqa: E731
    out = []
    for kind, b in BLOCKS:
        if kind == "part":
            out.append(f'<h1 class="part">{f(b["title"])}</h1><p>{f(b["blurb"])}</p>')
        elif kind == "chapter":
            out.append(f'<h1>Chapter {b["n"]}: {f(b["title"])}</h1><p><i>{f(b["intro"])}</i></p>')
            out.append('<div custom-style="Objectives"><p><b>After this chapter you will be able to</b></p><ul>'
                       + "".join(f"<li>{f(o)}</li>" for o in b["objectives"]) + "</ul></div>")
            if b["terms"]:
                out.append("<p><b>Key terms</b></p><ul>"
                           + "".join(f"<li><b>{f(t)}</b>: {f(d)}</li>" for t, d in b["terms"]) + "</ul>")
        elif kind == "sec":
            out.append(f'<h2>{f(b["title"])}</h2>')
        elif kind == "sub":
            out.append(f'<h3>{f(b["title"])}</h3>')
        elif kind == "p":
            out.append(f'<p>{f(b["text"])}</p>')
        elif kind == "list":
            tag = "ol" if b["ordered"] else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{f(i)}</li>" for i in b["items"]) + f"</{tag}>")
        elif kind == "eq":
            out.append("".join(f'<div custom-style="Work"><p>{f(x)}</p></div>' for x in b["lines"]))
        elif kind == "box":
            label = {"rule": "KEY RULE", "warn": "WATCH OUT", "tip": "CALCULATOR TIP", "shop": "ON THE JOB", "handout": "CLASS HANDOUT"}[b["box"]]
            style = {"rule": "BoxRule", "warn": "BoxWarn", "tip": "BoxTip", "shop": "BoxShop", "handout": "BoxHandout"}[b["box"]]
            body = "".join(f"<p>{f(x)}</p>" for x in b["body"])
            out.append(f'<div custom-style="{style}"><p><b>{label}: {f(b["title"])}</b></p>{body}</div>')
        elif kind == "example":
            ttl = f': {f(b["title"])}' if b["title"] else ""
            rows = "".join(f"<tr><td>{f(w)}</td><td>{f(y)}</td></tr>" for w, y in b["steps"])
            out.append(f'<div custom-style="ExampleHead"><p><b>EXAMPLE {b["n"]}{ttl}</b></p></div>'
                       f'<p>{f(b["problem"])}</p><table><tr><th>Work</th><th>Why</th></tr>{rows}</table>'
                       f'<div custom-style="Answer"><p><b>Answer:</b> {f(b["answer"])}</p></div>')
        elif kind == "table":
            cap = f'<p><b>{f(b["caption"])}</b></p>' if b["caption"] else ""
            head = "<tr>" + "".join(f"<th>{f(h)}</th>" for h in b["headers"]) + "</tr>" if b["headers"] else ""
            rows = "".join("<tr>" + "".join(f"<td>{f(str(c))}</td>" for c in r) + "</tr>" for r in b["rows"])
            out.append(f"{cap}<table>{head}{rows}</table>")
        elif kind == "fig":
            vw = float(re.search(r'viewBox="0 0 ([\d.]+)', b["svg"]).group(1))
            out.append(f'<p><img src="figs/fig{b["idx"]:03d}.png" style="width:{min(6.0, vw / 105):.2f}in"/></p>'
                       f'<div custom-style="Caption"><p><b>Figure {b["n"]}</b> {f(b["caption"])}</p></div>')
        elif kind == "practice":
            out.append(f'<h3>Practice {b["label"]}: {f(b["title"])}</h3><p>{f(b["intro"])}</p><ol>'
                       + "".join(f"<li>{f(q)}</li>" for q in b["items"]) + "</ol>")
        elif kind == "review":
            out.append(f'<h2>Chapter {b["n"]} review</h2><ol>' + "".join(f"<li>{f(q)}</li>" for q in b["items"]) + "</ol>")
        elif kind == "summary":
            out.append('<div custom-style="BoxRule"><p><b>Chapter summary</b></p><ul>'
                       + "".join(f"<li>{f(x)}</li>" for x in b["points"]) + "</ul></div>")
        elif kind == "raw":
            out.append(b["docx"])
    out.append("<h1>Answers to practice sets and reviews</h1>")
    last = None
    for ch, title, label, ans in ANSWERS:
        if ch != last:
            out.append(f"<h2>Chapter {ch}: {f(title)}</h2>")
            last = ch
        out.append(f"<p><b>{f(label)}</b></p><ol>" + "".join(f"<li>{f(a)}</li>" for a in ans) + "</ol>")
    return "\n".join(out)
