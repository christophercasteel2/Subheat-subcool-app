#!/usr/bin/env python3
"""Build the ready-to-install calculator files for every app in hp-prime/.

For each app NAME (SUPERSUB, HVACAIR, NECCALC, HVACELEC, HVACGAS, REFCYCLE, CIRCUITS):
  calculator/NAME.hpappdir/   app folder: drag onto the Connectivity
                              Kit's Application Library
  calculator/NAME.hpprgm      plain program: drag onto Programs
  calculator/NAME.zip         both of the above, for one download

The program files use the record format that current firmware and the
Connectivity Kit use (see tools/hpfile.py), with the full readable source.
Files in the older plain format (a 20-byte header and the source) did
not show up on a G1 running firmware 2.4.2.  See tools/hpapp/README.md for
the template files.

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
OUT = os.path.join(ROOT, "calculator")
REPO = "github.com/christophercasteel2/Subheat-subcool-app"


def icon_gauges(path):
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


def icon_bolt(path):
    """38 x 38 app icon: a yellow lightning bolt over the app's five tile
    colours."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    tiles = [(32, 104, 206), (214, 110, 22), (30, 142, 74), (196, 52, 52), (124, 74, 192)]
    for k, col in enumerate(tiles):
        x = 4 + k * 6.2
        d.rounded_rectangle([x * big, 30 * big, (x + 5.2) * big, 34 * big], big, fill=col)
    # the same bolt the app draws in its title bar, scaled up
    pts = [(7, 0), (1, 9), (6, 9), (4, 16), (11, 6), (6, 6)]
    s, ox, oy = 1.62, 10.1, 2.5
    d.polygon([((ox + x * s) * big, (oy + y * s) * big) for x, y in pts], fill=(255, 210, 0))
    im.resize((38, 38), Image.LANCZOS).save(path)


def icon_air(path):
    """38 x 38 app icon: three moving-air arrows over the app's tile colours."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    tiles = [(32, 104, 206), (30, 142, 74), (124, 74, 192), (196, 52, 52), (214, 110, 22)]
    for k, col in enumerate(tiles):
        x = 4 + k * 6.2
        d.rounded_rectangle([x * big, 30 * big, (x + 5.2) * big, 34 * big], big, fill=col)
    # the same mark the app draws in its title bar, scaled up
    s, ox, oy = 1.55, 7.5, 4.5
    for x0, y0, length in ((0, 2, 10), (3, 7, 8), (0, 12, 7)):
        d.rectangle([(ox + x0 * s) * big, (oy + y0 * s) * big,
                     (ox + (x0 + length) * s) * big, (oy + (y0 + 1.4) * s) * big], fill=(120, 200, 255))
        tip = x0 + length
        d.polygon([((ox + tip * s) * big, (oy + (y0 - 2) * s) * big),
                   ((ox + tip * s) * big, (oy + (y0 + 3.4) * s) * big),
                   ((ox + (tip + 4) * s) * big, (oy + (y0 + 0.7) * s) * big)], fill=(120, 200, 255))
    im.resize((38, 38), Image.LANCZOS).save(path)


def icon_nec(path):
    """38 x 38 app icon: NEC in a code-book cover over the tile colours."""
    from PIL import ImageFont
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    d.rounded_rectangle([6 * big, 4 * big, 32 * big, 26 * big], 2 * big, fill=(32, 104, 206))
    d.rectangle([6 * big, 4 * big, 8.5 * big, 26 * big], fill=(20, 70, 150))
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 11 * big)
    d.text((20.5 * big, 15.5 * big), "NEC", font=fnt, fill=(255, 255, 255), anchor="mm")
    for k, col in enumerate([(32, 104, 206), (30, 142, 74), (124, 74, 192), (214, 110, 22), (20, 128, 140)]):
        x = 4 + k * 6.2
        d.rounded_rectangle([x * big, 30 * big, (x + 5.2) * big, 34 * big], big, fill=col)
    im.resize((38, 38), Image.LANCZOS).save(path)


def icon_gas(path):
    """38 x 38 app icon: a gas flame over a pipe and the tile colours."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))

    def flame(cx, base, w, h, col):
        pts = []
        for k in range(41):
            a = math.pi * k / 40
            pts.append((cx - w * math.cos(a) * (1 - 0.15 * math.sin(a)), base - h * 0.42 * math.sin(a)))
        pts += [(cx + w * 0.55, base - h * 0.62), (cx + w * 0.15, base - h * 0.78), (cx, base - h),
                (cx - w * 0.35, base - h * 0.7), (cx - w * 0.6, base - h * 0.55)]
        d.polygon([(x * big, y * big) for x, y in pts], fill=col)
    flame(19, 22, 9, 19, (60, 120, 235))
    flame(19, 22, 5.5, 12, (120, 200, 255))
    d.rounded_rectangle([5 * big, 23.5 * big, 33 * big, 27 * big], big, fill=(170, 172, 180))
    for k, col in enumerate([(32, 104, 206), (124, 74, 192), (214, 110, 22), (30, 142, 74), (196, 52, 52)]):
        x = 4 + k * 6.2
        d.rounded_rectangle([x * big, 30 * big, (x + 5.2) * big, 34 * big], big, fill=col)
    im.resize((38, 38), Image.LANCZOS).save(path)


def icon_cycle(path):
    """38 x 38 app icon: a pressure-enthalpy dome with the cycle drawn on it."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    dome = [(5 + 26 * k / 40, 27 - 19 * math.sin(math.pi * k / 40) ** 0.7) for k in range(41)]
    d.line([(x * big, y * big) for x, y in dome], fill=(150, 156, 172), width=int(1.4 * big))
    d.line([(11 * big, 10.5 * big), (27 * big, 10.5 * big)], fill=(245, 70, 70), width=int(1.8 * big))
    d.line([(27 * big, 10.5 * big), (33 * big, 4.5 * big)], fill=(245, 70, 70), width=int(1.8 * big))
    d.line([(11 * big, 10.5 * big), (11 * big, 25 * big)], fill=(255, 210, 0), width=int(1.8 * big))
    d.line([(11 * big, 25 * big), (24 * big, 25 * big)], fill=(60, 140, 240), width=int(1.8 * big))
    d.line([(24 * big, 25 * big), (33 * big, 4.5 * big)], fill=(240, 240, 240), width=int(1.8 * big))
    for k, col in enumerate([(32, 104, 206), (124, 74, 192), (214, 110, 22), (30, 142, 74), (196, 52, 52)]):
        x = 4 + k * 6.2
        d.rounded_rectangle([x * big, 30 * big, (x + 5.2) * big, 34 * big], big, fill=col)
    im.resize((38, 38), Image.LANCZOS).save(path)


def icon_circuit(path):
    """38 x 38 app icon: a battery, a resistor in series and two in
    parallel."""
    big = 4
    im = Image.new("RGBA", (38 * big, 38 * big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 38 * big - 1, 38 * big - 1], 7 * big, fill=(24, 27, 38, 255))
    wire = (236, 236, 236)

    def ln(*pts, col=wire, w=1.4):
        d.line([(x * big, y * big) for x, y in pts], fill=col, width=int(w * big), joint="curve")

    def zig(p0, p1, col):
        (x0, y0), (x1, y1) = p0, p1
        n, a = 6, 2.4
        nx, ny = (y1 - y0), -(x1 - x0)
        ln_ = (nx * nx + ny * ny) ** 0.5
        pts = [p0] + [(x0 + (x1 - x0) * (k + 0.5) / n + nx / ln_ * a * (1 if k % 2 else -1),
                       y0 + (y1 - y0) * (k + 0.5) / n + ny / ln_ * a * (1 if k % 2 else -1))
                      for k in range(n)] + [p1]
        ln(*pts, col=col, w=1.5)

    ln((6, 16), (6, 7), (10, 7))
    zig((10, 7), (21, 7), (255, 210, 0))
    ln((21, 7), (31, 7), (31, 12))
    ln((23, 7), (23, 12))
    zig((23, 12), (23, 25), (110, 170, 250))
    zig((31, 12), (31, 25), (190, 150, 250))
    ln((23, 25), (23, 31))
    ln((31, 25), (31, 31), (6, 31), (6, 22))
    ln((2, 16), (10, 16), col=(245, 70, 70), w=1.6)
    ln((4, 22), (8, 22), w=2.4)
    im.resize((38, 38), Image.LANCZOS).save(path)


APPS = [
    dict(name="SUPERSUB", icon=icon_gauges,
         test=os.path.join(ROOT, "tools", "ppl_sim.py"),
         note="""SUPERSUB - superheat and subcooling with manifold gauges

Open the app to start. Tap HELP inside the app for the controls.

Drag a needle or tap a dial to set pressure. Drag the SUCT and LIQ sliders to set the line temperatures. Up/Down change the selected value, Enter types an exact one.

Superheat uses the dew point at suction pressure; subcooling uses the bubble point at liquid pressure.

Source and instructions: """ + REPO),
    dict(name="HVACAIR", icon=icon_air,
         test=os.path.join(ROOT, "tools", "test_hvacair.py"),
         note="""HVACAIR - airside calculator for HVAC/R service (the rebuilt HVAC Suite)

Open the app and tap a tile. 20 tools: air properties, dew point / sweating, coil capacity, mixed air / economizer, furnace temperature rise, air heat formulas, static pressure, ventilation and ACH, duct sizer, duct check, friction rate (Manual D), grille airflow, fan laws, pulleys and belts, fan power, unit converter, heat loss / gain, cooling load, humidifier sizing and evaporative cooler.

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. HELP explains each tool.

Source and instructions: """ + REPO),
    dict(name="NECCALC", icon=icon_nec,
         test=os.path.join(ROOT, "tools", "test_neccalc.py"),
         note="""NECCALC - NEC calculator for electrical classes

Follows the 2026 NEC as adopted in Arkansas. Open the app and tap a tile. 19 tools, the calculators, charts and guides of electricalcalctools.com: voltage drop, wire size, ampacity (Table 310.16 raceway or 310.17 free air, every insulation type), breaker size, conduit fill, AWG chart, feeder size, ground wire, box fill, MCA / MOCP, power, Ohm's law, kWh, electricity cost, derating, voltage drop table, breaker / wire chart, appliance circuits and NEMA receptacles, plus Learn (short NEC reference pages).

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. HELP shows the rule each tool uses.

Source and instructions: """ + REPO),
    dict(name="HVACELEC", icon=icon_bolt,
         test=os.path.join(ROOT, "tools", "test_hvacelec.py"),
         note="""HVACELEC - electrical calculator for HVAC/R service

Open the app and tap a tile. 20 tools: Ohm's law, power, load amps, series / parallel, amp check, 3-phase balance, capacitor test, winding check, megohm test, motor NEC sizing, motor LRA and RPM, unit MCA / MOCP, voltage drop, wire ampacity, transformer, wye / delta, electric heat, thermistor check, energy cost and unit converter.

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. HELP explains each tool.

Source and instructions: """ + REPO),
    dict(name="HVACGAS", icon=icon_gas,
         test=os.path.join(ROOT, "tools", "test_hvacgas.py"),
         note="""HVACGAS - gas heating and piping calculator for HVACR classes

Open the app and tap a tile. Set up for Arkansas (2018 Arkansas Fuel Gas Code). 19 tools: gas pipe size (the eight Arkansas Table 402.4 natural gas tables, plus IFGC propane tables as a reference), pipe capacity, fitting allowance, gas load, clock the meter, manifold pressure, altitude derate, combustion air, flue gas analysis, furnace output, oil nozzle, gas pressure test, fuel cost, unit converter, copper tube, steel pipe, pipe offsets, expansion and brazing alloys, plus Learn (code and trade notes).

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. HELP explains each tool.

Source and instructions: """ + REPO),
    dict(name="REFCYCLE", icon=icon_cycle,
         test=os.path.join(ROOT, "tools", "test_refcycle.py"),
         note="""REFCYCLE - refrigeration cycle and service calculator for HVACR classes

Open the app and tap a tile. 19 tools: cycle state points and performance (R-22, R-410A, R-134a, R-404A, R-407C, R-32, R-507A, R-290, R-12; from saturation temperatures or gauge pressures), saturated and superheated properties, capacity and mass flow, compressor displacement, volumetric efficiency, EER / COP / kW per ton, water load and cooling tower, walk-in box wall, product and equipment loads, EPA leak rate (40 CFR 84.106 / 82.157), EPA evacuation levels (82.156), charge record, service invoice, markup and margin, time sheet and a unit converter, plus Learn.

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. HELP explains each tool.

Source and instructions: """ + REPO),
    dict(name="CIRCUITS", icon=icon_circuit,
         test=os.path.join(ROOT, "tools", "test_circuits.py"),
         note="""CIRCUITS - DC circuit calculator for electricity classes

Open the app and tap a tile. 12 tools: series, parallel, series-parallel (branches of two resistors) and combination circuits (R1 - R2||R3 - R4 - R5||R6 - R7) with RT, IT, ET, PT and every resistor's voltage, current and power; troubleshooting (which resistor is open or shorted, from voltmeter readings); Kirchhoff's voltage law; Kirchhoff's current law (with what a negative answer means); a two-source Kirchhoff network; Ohm's law and power; voltage and current dividers; the resistor color code and metric prefixes, plus Learn (formulas and rules).

In a tool, tap a box to change it, or select it with Left/Right and type the number on the keypad. A resistor of 0 is left out. Give ET or IT and the other is worked out. HELP shows the formulas.

Source and instructions: """ + REPO),
]

APP_START = """
// runs when the app is opened from the Application Library
EXPORT START()
BEGIN
  {name}();
END;
"""


def program_file(text):
    """The program in the calculator's file format, listing every function
    in source order as the Connectivity Kit does."""
    _, funcs = Parser(tokenize(text)).program()
    return hpfile.build(text, [(n, f[2], len(f[0])) for n, f in funcs.items()])


def build(app):
    name = app["name"]
    src = open(os.path.join(ROOT, "hp-prime", name + ".txt"), encoding="utf-8").read()
    app_src = src + APP_START.format(name=name)
    appdir = os.path.join(OUT, name + ".hpappdir")
    os.makedirs(appdir)

    prgm = program_file(src)
    app_prgm = program_file(app_src)
    with open(os.path.join(OUT, name + ".hpprgm"), "wb") as fh:
        fh.write(prgm)
    with open(os.path.join(appdir, name + ".hpappprgm"), "wb") as fh:
        fh.write(app_prgm)
    shutil.copyfile(os.path.join(ROOT, "tools", "hpapp", "template.hpapp"),
                    os.path.join(appdir, name + ".hpapp"))
    with open(os.path.join(appdir, name + ".hpappnote"), "wb") as fh:
        fh.write(app["note"].encode("utf-16-le") + b"\0\0")
    app["icon"](os.path.join(appdir, "icon.png"))

    with zipfile.ZipFile(os.path.join(OUT, name + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, name + ".hpprgm"), name + ".hpprgm")
        for f in sorted(os.listdir(appdir)):
            z.write(os.path.join(appdir, f), f"{name}.hpappdir/{f}")

    # check: the files decode back to exactly what we meant to write,
    # and both versions of the program pass the app's simulator tests
    for blob, text in ((prgm, src), (app_prgm, app_src)):
        back, names = hpfile.read(blob)
        assert back == text and name in names
    with tempfile.TemporaryDirectory() as tmp:
        for label, text in (("program", src), ("app", app_src)):
            path = os.path.join(tmp, label + ".txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            res = subprocess.run([sys.executable, app["test"], path, tmp], capture_output=True, text=True)
            if res.returncode:
                sys.exit(f"{name}: simulator failed on the {label} file:\n{res.stdout}{res.stderr}")
    print(f"{name}.hpprgm      {len(prgm):6d} bytes")
    print(f"{name}.hpappprgm   {len(app_prgm):6d} bytes")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for app in APPS:
        build(app)
    print(f"written to {OUT}; every program and app copy passes its simulator tests")


if __name__ == "__main__":
    main()
