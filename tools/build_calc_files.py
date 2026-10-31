#!/usr/bin/env python3
"""Build the ready-to-install calculator files from hp-prime/SUPERSUB.txt.

  calculator/SUPERSUB.hpappdir/   app folder: drag onto the Connectivity
                                  Kit's Application Library
  calculator/SUPERSUB.hpprgm      plain program: drag onto Programs
  calculator/SUPERSUB.zip         both of the above, for one download

The program files use the record format that current firmware and the
Connectivity Kit use (see tools/hpfile.py), with the full readable source.
Files in the older plain format (a 20-byte header and the source) did
not show up on a G1 running firmware 2.4.2.  See tools/hpapp/README.md for the template files.

Usage: python3 tools/build_calc_files.py
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hpfile
from ppl_sim import Parser, tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "hp-prime", "SUPERSUB.txt")
OUT = os.path.join(ROOT, "calculator")
NAME = "SUPERSUB"
REPO = "github.com/christophercasteel2/Subheat-subcool-app"

APP_START = """
// runs when the app is opened from the Application Library
EXPORT START()
BEGIN
  SUPERSUB();
END;
"""

NOTE = """SUPERSUB - superheat and subcooling with manifold gauges

Open the app to start. Tap HELP inside the app for the controls.

Drag a needle or tap a dial to set pressure. Drag the SUCT and LIQ sliders to set the line temperatures. Up/Down change the selected value, Enter types an exact one.

Superheat uses the dew point at suction pressure; subcooling uses the bubble point at liquid pressure.

Source and instructions: """ + REPO


def program_file(text):
    """The program in the calculator's file format, listing every function
    in source order as the Connectivity Kit does."""
    _, funcs = Parser(tokenize(text)).program()
    return hpfile.build(text, [(n, f[2], len(f[0])) for n, f in funcs.items()])


def icon(path):
    """38 x 38 app icon: a blue and a red gauge."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    for cx, col, ang in ((10, (40, 110, 230), 130), (28, (220, 45, 45), 60)):
        cx, cy, r = cx * big, 17 * big, 8.5 * big
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        r2 = r - 1.6 * big
        d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(250, 248, 240))
        a = math.radians(ang)
        d.line([cx, cy, cx + (r2 - big) * math.cos(a), cy - (r2 - big) * math.sin(a)],
               fill=(25, 25, 25), width=int(1.4 * big))
        d.ellipse([cx - 1.3 * big, cy - 1.3 * big, cx + 1.3 * big, cy + 1.3 * big], fill=(25, 25, 25))
    # manifold body with the blue, yellow and red hose connections
    d.rounded_rectangle([5 * big, 27 * big, 33 * big, 31 * big], big, fill=(175, 178, 186))
    for x, col in ((10, (40, 110, 230)), (19, (240, 200, 40)), (28, (220, 45, 45))):
        d.rectangle([(x - 1.5) * big, 31 * big, (x + 1.5) * big, 35 * big], fill=col)
    im.resize((38, 38), Image.LANCZOS).save(path)


def main():
    src = open(SOURCE, encoding="utf-8").read()
    app_src = src + APP_START
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    appdir = os.path.join(OUT, NAME + ".hpappdir")
    os.makedirs(appdir)

    prgm = program_file(src)
    app_prgm = program_file(app_src)
    with open(os.path.join(OUT, NAME + ".hpprgm"), "wb") as fh:
        fh.write(prgm)
    with open(os.path.join(appdir, NAME + ".hpappprgm"), "wb") as fh:
        fh.write(app_prgm)
    shutil.copyfile(os.path.join(ROOT, "tools", "hpapp", "template.hpapp"),
                    os.path.join(appdir, NAME + ".hpapp"))
    with open(os.path.join(appdir, NAME + ".hpappnote"), "wb") as fh:
        fh.write(NOTE.encode("utf-16-le") + b"\0\0")
    icon(os.path.join(appdir, "icon.png"))

    with zipfile.ZipFile(os.path.join(OUT, NAME + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, NAME + ".hpprgm"), NAME + ".hpprgm")
        for f in sorted(os.listdir(appdir)):
            z.write(os.path.join(appdir, f), f"{NAME}.hpappdir/{f}")

    # check: the files decode back to exactly what we meant to write,
    # and both versions of the program pass the simulator's tests
    for blob, text in ((prgm, src), (app_prgm, app_src)):
        back, names = hpfile.read(blob)
        assert back == text and "SUPERSUB" in names
    sim = os.path.join(ROOT, "tools", "ppl_sim.py")
    with tempfile.TemporaryDirectory() as tmp:
        for label, text in (("program", src), ("app", app_src)):
            path = os.path.join(tmp, label + ".txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            res = subprocess.run([sys.executable, sim, path, tmp], capture_output=True, text=True)
            if res.returncode:
                sys.exit(f"simulator failed on the {label} file:\n{res.stdout}{res.stderr}")
    print(f"{NAME}.hpprgm      {len(prgm):6d} bytes")
    print(f"{NAME}.hpappprgm   {len(app_prgm):6d} bytes")
    print(f"written to {OUT}; both copies pass the simulator")


if __name__ == "__main__":
    main()
