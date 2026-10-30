#!/usr/bin/env python3
"""Build the ready-to-install calculator files from hp-prime/SUPERSUB.txt.

  calculator/SUPERSUB.hpappdir/   app folder: drag into the Connectivity
                                  Kit's Application Library
  calculator/SUPERSUB.hpprgm      plain program: drag into Programs
  calculator/SUPERSUB.zip         both of the above, for one download

The calculator copy of the program is compacted (comments, indentation
and blank lines removed) because the Prime truncates program files over
64 KB.  The readable source stays in hp-prime/SUPERSUB.txt.

Files use the original (G1) program format: a 20-byte header (0x0C, 15
zero bytes, then the UTF-16 byte count) followed by the UTF-16LE source
with a 2-byte terminator.  See tools/hpapp/README.md for the .hpapp file.

Usage: python3 tools/build_calc_files.py   (then run tools/ppl_sim.py on
calculator/SUPERSUB-compact.txt, which the build does for you)
"""
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "hp-prime", "SUPERSUB.txt")
OUT = os.path.join(ROOT, "calculator")
NAME = "SUPERSUB"
LIMIT = 65536            # bytes; the Prime truncates larger program files
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


def strip_comment(line):
    """Remove a // comment that is not inside a string."""
    quoted = False
    for i, ch in enumerate(line):
        if ch == '"':
            quoted = not quoted
        elif not quoted and line.startswith("//", i):
            return line[:i]
    return line


def compact(src):
    lines = src.split("\n")
    out = [lines[0], "// SUPERSUB, readable source: " + REPO]
    for line in lines[1:]:
        line = strip_comment(line).strip()
        if line:
            out.append(line)
    return "\n".join(out) + "\n"


def g1_program(text):
    data = text.encode("utf-16-le") + b"\0\0"
    if len(data) + 20 >= LIMIT:
        sys.exit(f"program is {len(data)} bytes, over the {LIMIT}-byte calculator limit")
    return b"\x0c" + bytes(15) + struct.pack("<I", len(data)) + data


def read_g1_program(blob):
    """Inverse of g1_program, used to check what was written."""
    assert blob[0] == 0x0C and blob[1:16] == bytes(15)
    size = struct.unpack("<I", blob[16:20])[0]
    assert size == len(blob) - 20
    return blob[20:-2].decode("utf-16-le")


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
    small = compact(src)
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    appdir = os.path.join(OUT, NAME + ".hpappdir")
    os.makedirs(appdir)

    prgm = g1_program(small)
    app_prgm = g1_program(small + APP_START.lstrip("\n"))
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
    assert read_g1_program(prgm) == small
    app_src = read_g1_program(app_prgm)
    assert app_src == small + APP_START.lstrip("\n")
    sim = os.path.join(ROOT, "tools", "ppl_sim.py")
    with tempfile.TemporaryDirectory() as tmp:
        for label, text in (("program", small), ("app", app_src)):
            path = os.path.join(tmp, label + ".txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            res = subprocess.run([sys.executable, sim, path, tmp], capture_output=True, text=True)
            if res.returncode:
                sys.exit(f"simulator failed on the {label} file:\n{res.stdout}{res.stderr}")
    print(f"{NAME}.hpprgm      {len(prgm):6d} bytes (limit {LIMIT})")
    print(f"{NAME}.hpappprgm   {len(app_prgm):6d} bytes")
    print(f"written to {OUT}; both copies pass the simulator")


if __name__ == "__main__":
    main()
