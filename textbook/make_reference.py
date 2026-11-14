"""Makes reference.docx: the Word styles (fonts, colours, shaded boxes) the Word copy is built on."""
import os, subprocess
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

here = os.path.dirname(os.path.abspath(__file__))
ref = os.path.join(here, "reference.docx")
with open(ref, "wb") as f:
    f.write(subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], capture_output=True, check=True).stdout)
d = Document(ref)
class _S:
    def __init__(self, styles): self.s = styles
    def __iter__(self): return iter(self.s)
    def __getitem__(self, k): return next(x for x in self.s if x.name == k)
    def add_style(self, *a): return self.s.add_style(*a)


st = _S(d.styles)


def font(s, name, size, color=None, bold=None):
    s.font.name = name
    s.font.size = Pt(size)
    rpr = s.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    if color:
        s.font.color.rgb = RGBColor.from_string(color)
    if bold is not None:
        s.font.bold = bold


def shade(s, fill, border):
    ppr = s.element.get_or_add_pPr()
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill)
    bd = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    for k, v in (("w:val", "single"), ("w:sz", "24"), ("w:space", "6"), ("w:color", border)):
        left.set(qn(k), v)
    bd.append(left); ppr.append(bd); ppr.append(sh)


for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
    if name in [x.name for x in st]:
        font(st[name], "Cambria", 11)
font(st["Title"], "Calibri", 34, "1C2440", True)
font(st["Subtitle"], "Calibri", 15, "5A6278")
font(st["Heading 1"], "Calibri", 24, "1C2440", True)
st["Heading 1"].paragraph_format.page_break_before = True
st["Heading 1"].paragraph_format.space_after = Pt(10)
font(st["Heading 2"], "Calibri", 16, "1F6FB5", True)
font(st["Heading 3"], "Calibri", 12.5, "C8452F", True)
for name, fill, border, fnt in (("Objectives", "EEF4FB", "1F6FB5", None), ("Work", "F4F6FA", "1F6FB5", "Calibri"), ("BoxRule", "E6F0FB", "1F6FB5", None),
                                ("BoxWarn", "FBE7E3", "C8452F", None), ("BoxTip", "EEE8F8", "7453B8", None), ("BoxShop", "E3F3E8", "2F8F4E", None),
                                ("ExampleHead", "FFFFFF", "D98A14", "Calibri"), ("Answer", "FDF3DA", "D98A14", None), ("Caption", None, None, "Calibri")):
    s = st[name] if name in [x.name for x in st] else st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    s.base_style = st["Normal"]
    font(s, fnt or "Cambria", 9 if name == "Caption" else 10.5, "5A6278" if name == "Caption" else None)
    s.paragraph_format.space_before = Pt(2)
    s.paragraph_format.space_after = Pt(3)
    if fill:
        shade(s, fill, border)
        s.paragraph_format.left_indent = Inches(0.12)
for sec in d.sections:
    sec.left_margin = sec.right_margin = Inches(1)
    sec.top_margin = sec.bottom_margin = Inches(0.9)
d.save(ref)
print("reference.docx written")
