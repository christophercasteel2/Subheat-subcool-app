# Applied Technical Math: the course textbook

A full-colour textbook covering the whole semester: place value and rounding, fractions/decimals/percents,
the percent proportion, standard and metric measurement, rulers/gauges/tolerance, order of operations,
evaluating and solving formulas, and the perimeter and area of flat shapes.

- `Applied_Technical_Math.pdf`: the print-ready book (115 pages, Letter size).
- `Applied_Technical_Math.docx`: the same text as an editable Word document.

## Rebuilding

    python3 make_reference.py     # Word styles (once)
    python3 build.py              # both files;  `build.py pdf` or `build.py docx` for one

The text lives in `ch_numbers.py`, `ch_measure.py`, `ch_algebra.py`, `ch_geometry.py` and `ch_back.py`.
Drawings are in `figs.py`, the page design in `style.css`. Answers in the key are calculated by the
code from the numbers in each question, so a changed question gets a correct answer automatically.
Needs Node with Playwright (PDF), pandoc and python-docx (Word), and pypdf.
