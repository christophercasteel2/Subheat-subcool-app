# Applied Technical Math: the course textbook

A full-colour textbook covering the whole semester: place value and rounding, fractions/decimals/percents,
the percent proportion, standard and metric measurement, rulers/gauges/tolerance, order of operations,
evaluating and solving formulas, and the perimeter and area of flat shapes.

- `Applied_Technical_Math.pdf`: the print-ready book (about 205 pages, Letter size).
- `Applied_Technical_Math.docx`: the same text as an editable Word document.

## Rebuilding

    python3 make_reference.py     # Word styles (once)
    python3 build.py              # both files;  `build.py pdf` or `build.py docx` for one

The text lives in `ch_numbers.py`, `ch_measure.py`, `ch_algebra.py`, `ch_geometry.py`, `ch_solid.py` (Chapter 13, solid geometry) and `ch_back.py`, with the added sections, practice and reviews in `x1.py` to `x4.py`.
Drawings are in `figs.py`, the page design in `style.css`. Answers in the key are calculated by the
code from the numbers in each question, so a changed question gets a correct answer automatically.
Needs Node with Playwright (PDF), pandoc and python-docx (Word), and pypdf.

## Teacher's edition

    TEACHER=1 python3 build.py     # writes Applied_Technical_Math_Teachers_Edition.pdf and .docx

The same book with the answer printed in red after every question, a notes box at the start of
each chapter (sessions, big idea, teaching sequence, common errors, activity, exit ticket, what to
assign), a sixteen-week pacing guide, and a one-page test with key for each chapter. The notes and
tests are in `teacher.py`.

## Structure

The book is built on the class handouts, homework and quizzes, in seven chapters: 1 whole numbers, fractions
and decimals; 2 ratio, proportion and percent; 3 measurement and the metric stairs; 4 basic algebra;
5 practical plane geometry; 6 solid figures; 7 triangle trigonometry. Each chapter ends with one short
chapter review (about 20 problems) chosen from the review questions written for each topic. `restructure.py`
regroups the topic files into these chapters and renumbers every section, example, figure, table and
practice set; `ch_ratio.py` and `ch_trig.py` hold Sections 2.1 and 7.1 to 7.4.
