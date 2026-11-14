"""Builds the textbook: python3 build.py [pdf] [docx]
Output: Applied_Technical_Math.pdf and Applied_Technical_Math.docx in this folder."""
import importlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import book  # noqa: E402

TITLE = "Applied Technical Math"
SUB = "Numbers, Measurement, Algebra and Geometry for the Trades"
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

for mod in ("ch_numbers", "ch_measure", "ch_algebra", "ch_geometry", "ch_back"):
    if os.path.exists(os.path.join(HERE, mod + ".py")):
        importlib.import_module(mod)

CSS = open(os.path.join(HERE, "style.css")).read()


def node(*args):
    subprocess.run(["node", os.path.join(HERE, "render.js"), *args], check=True, cwd=HERE,
                   env={**os.environ, "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()})


def toc_entries():
    ent = []
    for kind, b in book.BLOCKS:
        if kind == "part":
            ent.append(("part", b["title"], None, None))
        elif kind == "chapter":
            ent.append(("ch", b["title"], f'ch{b["n"]}', (b["n"], b["color"])))
        elif kind == "raw" and b.get("toc"):
            ent.append(("back", b["toc"][1], b["toc"][0], None))
    ent.append(("back", "Answers to practice sets and reviews", "answers", None))
    return ent


def toc_html(pages):
    rows = []
    for kind, title, anchor, extra in toc_entries():
        if kind == "part":
            rows.append(f'<span class="tpart">{book.fmt(title)}</span>')
            continue
        pg = pages.get(anchor, "")
        lead = f'<b style="background:{extra[1]}">{extra[0]}</b>' if extra else ""
        rows.append(f'<a class="tch" href="#{anchor}"><span>{lead}{book.fmt(title)}</span><span class="dots"></span>'
                    f'<span class="pg">{pg}</span></a>')
    return '<section class="front"><h1>Contents</h1><div class="toc">' + "".join(rows) + "</div></section>"


def main_html(pages):
    body = book.render_pdf()
    # markers so the page of each chapter can be found
    body = re.sub(r'<h1 id="(ch\d+)">', r'<span class="mk">@@\1@@</span><h1 id="\1">', body)
    ans = book.answers_pdf().replace('<h1 id="answers">', '<span class="mk">@@answers@@</span><h1 id="answers">')
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS}</style></head><body>'
            + toc_html(pages) + PREFACE + body + ans + "</body></html>")


PREFACE = """
<section class="front"><h1>How to use this book</h1>
<p>This book follows one semester of applied technical math, in the order the course is taught: numbers first, then
measurement, then algebra with formulas, then the geometry of flat shapes. Every topic is taught the same way.</p>
<div class="twocol">
<div class="box rule"><div class="boxhead"><span class="tag">KEY RULE</span><span class="boxtitle">Blue boxes</span></div>
<div class="boxbody"><p>The rule or formula to learn. If a page is read for one thing only, read these.</p></div></div>
<div class="box warn"><div class="boxhead"><span class="tag">WATCH OUT</span><span class="boxtitle">Red boxes</span></div>
<div class="boxbody"><p>The mistakes that cost the most points, and how to avoid each one.</p></div></div>
<div class="box tip"><div class="boxhead"><span class="tag">CALCULATOR TIP</span><span class="boxtitle">Purple boxes</span></div>
<div class="boxbody"><p>Which keys to press, and what the calculator will not do for you.</p></div></div>
<div class="box shop"><div class="boxhead"><span class="tag">ON THE JOB</span><span class="boxtitle">Green boxes</span></div>
<div class="boxbody"><p>Where the skill shows up in the trades: sheet metal, piping, electrical, machining, building.</p></div></div>
</div>
<div class="box handout"><div class="boxhead"><span class="tag">CLASS HANDOUT</span><span class="boxtitle">Teal boxes</span></div>
<div class="boxbody"><p>The instructor's own definitions and formulas, copied word for word from the class handouts.</p></div></div>
<p><b>Worked examples</b> show the work on the left and the reason for each line on the right. Cover the right-hand
column and explain each line yourself; that is the fastest way to find out what you do not yet understand.</p>
<p><b>Practice sets</b> follow each section and a <b>chapter review</b> closes each chapter. Answers to every
problem are at the back of the book.</p>
<h2><span class="secbar"></span>Conventions used in the course</h2>
<ul class="plain">
<li><b>Show the substitution.</b> When a formula is used, write the formula, then write it again with the numbers in
place of the letters, then calculate. Every example in this book does this.</li>
<li><b>Round only at the end,</b> and only as far as the problem says. If a problem does not say, do not round.</li>
<li><b>Use 3.14 for π</b> unless a problem says otherwise.</li>
<li><b>Write the unit.</b> A number without a unit is not a measurement: 12 could be inches, feet, or volts.</li>
<li><b>Fractions are given in lowest terms,</b> and a mixed number is preferred to an improper fraction
(1 <span class="fr"><span>3</span><span>8</span></span> in rather than <span class="fr"><span>11</span><span>8</span></span> in).</li>
</ul>
</section>
"""

COVER = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: Letter; margin: 0; }}
html {{ -webkit-print-color-adjust: exact; }}
body {{ margin: 0; font-family: Inter, sans-serif; color: #fff; }}
.cv {{ width: 8.5in; height: 11in; background: #1c2440; position: relative; overflow: hidden; }}
.band {{ position: absolute; left: 0; right: 0; top: 0; height: 0.34in; display: flex; }}
.band i {{ flex: 1; }}
.t {{ position: absolute; left: 0.9in; top: 1.5in; right: 0.9in; }}
.k {{ font-weight: 700; letter-spacing: 0.34em; font-size: 11pt; color: #f2b84b; }}
h1 {{ font-size: 62pt; line-height: 0.98; font-weight: 800; margin: 14pt 0 18pt; letter-spacing: -0.01em; }}
.s {{ font-size: 16pt; font-weight: 400; color: #cfd6ea; max-width: 5.4in; line-height: 1.35; }}
svg {{ position: absolute; left: 0; bottom: 0.9in; }}
.f {{ position: absolute; left: 0.9in; right: 0.9in; bottom: 0.55in; font-size: 10pt; color: #9fa9c6; display: flex;
     justify-content: space-between; letter-spacing: 0.06em; }}
</style></head><body><div class="cv">
<div class="band"><i style="background:#c8452f"></i><i style="background:#d98a14"></i><i style="background:#2f8f4e"></i>
<i style="background:#1f6fb5"></i><i style="background:#7453b8"></i><i style="background:#0f8a8a"></i></div>
<div class="t"><div class="k">A FULL-COLOR COURSE TEXT</div><h1>Applied<br>Technical<br>Math</h1>
<div class="s">{SUB}</div></div>
<svg width="816" height="400" viewBox="0 0 816 400">
<g fill="none" stroke-width="3">
<rect x="70" y="150" width="210" height="150" stroke="#1f6fb5" fill="rgba(31,111,181,.22)"/>
<polygon points="250,300 470,300 250,90" stroke="#7453b8" fill="rgba(116,83,184,.25)"/>
<circle cx="560" cy="210" r="112" stroke="#c8452f" fill="rgba(200,69,47,.22)"/>
<polygon points="770,300 715,395 605,395 550,300 605,205 715,205" stroke="#2f8f4e" fill="rgba(47,143,78,.25)"/>
<line x1="560" y1="210" x2="672" y2="210" stroke="#f2b84b"/>
<line x1="70" y1="330" x2="520" y2="330" stroke="#f2b84b"/>
</g>
<g stroke="#f2b84b" stroke-width="2">{"".join(f'<line x1="{70 + 15 * k}" y1="330" x2="{70 + 15 * k}" y2="{346 if k % 2 == 0 else 339}"/>' for k in range(31))}</g>
<g fill="#cfd6ea" font-family="Inter" font-size="15" font-weight="600">
<text x="150" y="232">A = LW</text><text x="300" y="262">a² + b² = c²</text><text x="520" y="190">A = πr²</text>
<text x="622" y="330">A = 2.6s²</text></g></svg>
<div class="f"><span>NUMBERS · MEASUREMENT · ALGEBRA · GEOMETRY</span><span>FALL 2026</span></div>
</div></body></html>"""


def find_pages(pdf):
    from pypdf import PdfReader
    pages = {}
    for i, pg in enumerate(PdfReader(pdf).pages):
        for m in re.findall(r"@@(\w+)@@", pg.extract_text() or ""):
            pages.setdefault(m, i + 1)
    return pages


def build_pdf():
    from pypdf import PdfReader, PdfWriter
    html = os.path.join(OUT, "main.html")
    main = os.path.join(OUT, "main.pdf")
    pages = {}
    for _ in range(2):
        open(html, "w").write(main_html(pages))
        node("pdf", html, main, TITLE)
        pages = find_pages(main)
    open(os.path.join(OUT, "cover.html"), "w").write(COVER)
    node("pdf", os.path.join(OUT, "cover.html"), os.path.join(OUT, "cover.pdf"))
    w = PdfWriter()
    w.append(os.path.join(OUT, "cover.pdf"))
    w.append(main)
    w.add_metadata({"/Title": f"{TITLE}: {SUB}"})
    final = os.path.join(HERE, "Applied_Technical_Math.pdf")
    w.write(final)
    print("PDF pages:", len(PdfReader(final).pages), pages)


def build_docx():
    figdir = os.path.join(OUT, "figs")
    os.makedirs(figdir, exist_ok=True)
    fh = os.path.join(OUT, "figs.html")
    open(fh, "w").write('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}'
                        '.f{display:inline-block;padding:4px;background:#fff}</style></head><body>'
                        + "".join(f'<div><div class="f">{s}</div></div>' for s in book.FIGS) + "</body></html>")
    node("figs", fh, figdir)
    body = book.render_docx()
    dh = os.path.join(OUT, "docx.html")
    open(dh, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><title>{TITLE}</title></head><body>{body}</body></html>')
    ref = os.path.join(HERE, "reference.docx")
    cmd = ["pandoc", dh, "-f", "html", "-t", "docx", "-o", os.path.join(HERE, "Applied_Technical_Math.docx"),
           "--resource-path", OUT, "--toc", "--toc-depth=1",
           "-M", f"title={TITLE}", "-M", f"subtitle={SUB}"]
    if os.path.exists(ref):
        cmd += ["--reference-doc", ref]
    subprocess.run(cmd, check=True, cwd=OUT)
    print("DOCX written")


if __name__ == "__main__":
    what = sys.argv[1:] or ["pdf", "docx"]
    if "pdf" in what:
        build_pdf()
    if "docx" in what:
        build_docx()
