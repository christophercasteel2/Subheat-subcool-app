# SUPERSUB: superheat and subcooling for the HP Prime

A color, touchscreen superheat and subcooling calculator for the **HP Prime G1** (it also runs on the G2). It is built around a pair of analog manifold gauges that you set by dragging the needles, plus a full pressure-temperature (P-T) chart.

![Gauge screen](docs/screens/gauges.png) ![P-T chart](docs/screens/ptchart_find.png)

*Screens rendered by the development simulator (`tools/ppl_sim.py`). On the calculator, fonts look slightly different.*

## Features

- **Manifold gauges.** The low side is a blue compound gauge that reads from 30 inHg of vacuum up to 350 psig. The high side is a red gauge that reads 0–800 psig. Each dial has a temperature ring for the selected refrigerant, like the scales printed on a real gauge face. The low ring shows dew-point temperatures and the high ring shows bubble-point temperatures.
- **Touch control.** Drag a needle, or tap anywhere on a dial, to set the pressure. Drag the SUCT and LIQ sliders to set the line temperatures. You can also use the arrow keys, or type an exact value.
- **Live results.** Superheat and subcooling update as you move the needles and sliders, color-coded green, yellow or red.
- **P-T chart.** A scrolling table of liquid (bubble) and vapor (dew) pressures with °C, in 1°F or 5°F rows. Vacuum readings show in red as inHg. You can look up a value by temperature or by pressure, and pressure look-ups also report the glide.
- **30 refrigerants, including phased-out ones still found in the field.** See [Refrigerants](#refrigerants) below.

## Install (drag and drop, no typing)

The ready-made calculator files are in the [`calculator`](calculator) folder.

1. **Download** [`SUPERSUB.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/SUPERSUB.zip) and unzip it. On Windows, right-click it and choose **Extract All**; on a Mac, double-click it. You get a folder called `SUPERSUB.hpappdir` and a file called `SUPERSUB.hpprgm`. Drag from the unzipped copy; dragging straight out of the zip often fails.
2. **Connect** the calculator to the computer with its USB cable, turn it on, and open the free **HP Connectivity Kit**. Your calculator appears in the **Calculators** panel on the left. Click the small arrow next to it to see its contents.
3. **Drag the `SUPERSUB.hpappdir` folder** onto **Application Library** under your calculator.
4. On the calculator, press the **Apps** key and tap the **SUPERSUB** icon. It opens straight onto the gauges.

**If the app doesn't appear or won't open:** first update the calculator to the latest firmware. The Connectivity Kit offers this when a calculator is connected; 2.1.14730 was the newest G1 release when this was written. Then try the plain program instead: drag `SUPERSUB.hpprgm` onto **Programs** under your calculator. On the calculator, press **Shift** then **1** (Program), select **SUPERSUB** and tap **Run**.

Install one or the other, not both. To update later, drag the new copy over the old one and accept the replace prompt. Your last pressures, temperatures and refrigerant are kept between runs, but they reset when you install a new version.

To try it without a calculator, drag the same files into HP's free **HP Prime Virtual Calculator**, which appears in the Connectivity Kit too.

## Using it

**Gauge screen**

| Action | Touch | Keys |
|---|---|---|
| Set suction or liquid pressure | Drag the needle, or tap the dial | Select the gauge, then use Up/Down (±1) or + / − (±10) |
| Set suction or liquid line temp | Drag the SUCT or LIQ slider | Select the slider, then use Up/Down or + / − |
| Choose which control the keys change | Tap it | Left / Right (the selection is outlined in yellow) |
| Type an exact value | **SET VALUE** | Enter |
| Change refrigerant | **REFRIG**, or tap the refrigerant name | Symb |
| Open the P-T chart | **P-T CHART** | Num |
| Help / quit | **HELP** / **EXIT** | Help / Esc |

To enter a vacuum on the low side, type a negative psig value: 1 psi = 2.036 inHg, so 10 inHg is −4.9 psig.

**P-T chart:** scroll with Up/Down, + / −, or by dragging. Left/Right changes the refrigerant. **STEP** switches between 1°F and 5°F rows. **LOOK UP** (or Enter) finds the saturation values for a temperature or a pressure and highlights them in the table.

### How it is calculated

- **Superheat** = suction line temp − **dew** temperature at the suction pressure
- **Subcooling** = **bubble** temperature at the liquid pressure − liquid line temp

Using dew on the low side and bubble on the high side keeps the answer correct for blends with glide, such as R-407C, R-448A and R-454B.

Color guide (a reminder only; always use the manufacturer's charging chart):

| | Green | Yellow | Red |
|---|---|---|---|
| Superheat | 5–20°F | 2–5°F or 20–30°F | below 2°F or above 30°F |
| Subcooling | 5–15°F | 2–5°F or 15–25°F | below 2°F or above 25°F |

## Refrigerants

The chooser lists them in numeric order with their common trade names. R-410A is selected the first time the program runs.

| Group | Refrigerants |
|---|---|
| Current A/C and heat pump | R-32, R-410A, R-454B |
| Legacy A/C | R-22 |
| R-22 retrofit blends | R-407A, R-407C, R-417A (NU-22/MO59), R-421A, R-422B (NU-22B), R-422D (MO29), R-427A (FX-100), R-438A (MO99) |
| Commercial refrigeration | R-404A, R-407F, R-448A (N40), R-449A (XP40), R-452A (XP44), R-507A (AZ-50) |
| Legacy CFCs | R-12, R-500, R-502 |
| R-12 and R-502 retrofit blends | R-401A (MP39), R-402A (HP80), R-408A (FX-10), R-409A (FX-56) |
| Auto and medium temperature | R-134a, R-513A (XP10), R-1234yf |
| Hydrocarbons | R-290 (propane), R-600a (isobutane) |

R-414B (HotShot) is not included yet. The only table I found for it is from a source that read 3–5 psi high on the other HCFC blends. It can be added once a trustworthy chart is available.

![All refrigerants](docs/screens/all_refrigerants.png)

## Accuracy and data sources

The program stores the bubble and dew pressure of each refrigerant every 5°F from −40°F to 150°F. Between rows it interpolates in ln(P), which stays within about 0.06 psi of the source data. A pressure whose saturation temperature falls well outside that range shows `--` instead of a guess.

Each refrigerant's data comes from the most authoritative source I could find. Where possible it was cross-checked against a second source:

| Refrigerants | Source | Check |
|---|---|---|
| R-12, R-22, R-32, R-134a, R-290, R-600a, R-1234yf, R-404A, R-407C, R-410A, R-507A | [CoolProp](http://www.coolprop.org) reference equations of state | Within 0.15 psi of Arkema's NIST REFPROP 10 chart, where Arkema lists the refrigerant |
| R-427A, R-448A, R-449A, R-452A, R-513A | Arkema Forane P-T chart (NIST REFPROP 10) | |
| R-408A, R-409A | Arkema Forane P-T wall chart (NIST REFPROP) | R-408A's vapor side is derived from National Refrigerants' glide (about 1°F) |
| R-454B | Chemours *Opteon XL41 Thermodynamic Properties* (NIST REFPROP 10) | Matches Arkema within 0.06 psi |
| R-407A, R-422B, R-500 | National Refrigerants *Refrigerant Reference Guide* | Matches Hudson Technologies' charts within 0.7 psi |
| R-401A, R-402A, R-422D, R-502 | Hudson Technologies P-T charts | R-402A's and R-502's vapor sides are derived from National Refrigerants' glide |
| R-438A | IGAS P-T chart | Matches Hudson's liquid pressures within 0.25 psi |
| R-407F, R-417A, R-421A | CoolProp blend models | Within 0.05 psi (R-407F, R-421A) and 1 psi (R-417A) of Hudson's liquid pressures |

National's full property tables for the HCFC blends (R-401A, R-402A, R-408A, R-409A) read 3–5 psi higher than Arkema's REFPROP data and Hudson's charts. Those tables were not used for these blends.

Every source document is named, with its link, at the top of its CSV in `tools/data/`.

## Repository layout

```
calculator/               ready-to-install files (built, do not edit by hand)
  SUPERSUB.hpappdir/        app: drag onto Application Library
  SUPERSUB.hpprgm           program: drag onto Programs
  SUPERSUB.zip              both, for one download
hp-prime/SUPERSUB.txt     the program's readable source (HP PPL)
tools/gen_pt_tables.py    builds the P-T data block inside SUPERSUB.txt
tools/build_calc_files.py builds the calculator/ folder from SUPERSUB.txt
tools/hpapp/              app container template (from the MIT-licensed Xprime project)
tools/data/*.csv          published P-T tables used for the blends
tools/data/check/         published liquid pressures used to check CoolProp blend models
tools/ppl_sim.py          small PPL interpreter: runs the program, checks it, renders screenshots
docs/screens/             screenshots made by the simulator
```

The calculator copy of the program has its comments and indentation removed. The Prime cuts off program files larger than 64 KB, and the full source is over that limit. Edit `hp-prime/SUPERSUB.txt`, then rebuild.

### Adding a refrigerant

1. Add a line to `REFRIGERANTS` in `tools/gen_pt_tables.py`. Give it the display name, a source (a CoolProp fluid name, or a CSV file in `tools/data` with `temp_F,bubble,dew` columns in psia or psig), a cylinder color and a short description.
2. Run `pip install CoolProp`, then `python3 tools/gen_pt_tables.py --check`.
3. Run `python3 tools/ppl_sim.py` to re-run the checks and regenerate the screenshots.
4. Run `python3 tools/build_calc_files.py` to rebuild the files in `calculator/`. It also runs the simulator on the compact app and program copies, and stops if the program would exceed the 64 KB limit. Each extra refrigerant adds about 0.8 KB, so there is room for roughly eight more.

### Simulator

`tools/ppl_sim.py` runs the real program source with scripted key presses and touches. It checks the saturation math, the controls and the screen flow. It also enforces two PPL rules: functions must be defined before they are used, and names must not clash with calculator variables. It is a development aid. The calculator itself is the final test, so please report anything that behaves differently on real hardware. The app and program file formats follow Xprime's documentation and example apps, but they have not been loaded onto a real calculator from here.
