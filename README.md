# SUPERSUB: superheat and subcooling for the HP Prime

A color, touchscreen superheat and subcooling calculator for the **HP Prime G1** (it also runs on the G2). It is built around a pair of analog manifold gauges that you set by dragging the needles, plus a full pressure-temperature (P-T) chart and a set of service tools for the refrigerant circuit.

![Gauge screen](docs/screens/gauges.png) ![P-T chart](docs/screens/ptchart_find.png)

![Charge check](docs/screens/tool_charge.png) ![Capacity check](docs/screens/tool_capacity.png)

*Screens rendered by the development simulator (`tools/ppl_sim.py`). On the calculator, fonts look slightly different.*

## Features

- **Manifold gauges.** The low side is a blue compound gauge that reads from 30 inHg of vacuum up to 350 psig. The high side is a red gauge that reads 0–800 psig. Each dial has a temperature ring for the selected refrigerant, like the scales printed on a real gauge face. The low ring shows dew-point temperatures and the high ring shows bubble-point temperatures.
- **Touch control.** Drag a needle, or tap anywhere on a dial, to set the pressure. Drag the SUCT and LIQ sliders to set the line temperatures. You can also use the arrow keys, or type an exact value.
- **Live results.** Superheat and subcooling update as you move the needles and sliders, color-coded green, yellow or red.
- **P-T chart.** A scrolling table of liquid (bubble) and vapor (dew) pressures with °C, in 1°F or 5°F rows. Vacuum readings show in red as inHg. You can look up a value by temperature or by pressure, and pressure look-ups also report the glide.
- **Service tools.** Charge check, system check, capacity check, line set charge, nitrogen test, vacuum, recovery cylinder, refrigerant info, unit converter and an altitude setting. See [Tools](#tools) below.
- **30 refrigerants, including phased-out ones still found in the field.** See [Refrigerants](#refrigerants) below.

## Install (drag and drop, no typing)

The ready-made calculator files are in the [`calculator`](calculator) folder.

1. **Download** [`SUPERSUB.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/SUPERSUB.zip) and unzip it. On Windows, right-click it and choose **Extract All**; on a Mac, double-click it. You get a folder called `SUPERSUB.hpappdir` and a file called `SUPERSUB.hpprgm`. Drag from the unzipped copy; dragging straight out of the zip often fails.
2. **Connect** the calculator to the computer with its USB cable, turn it on, and open the free **HP Connectivity Kit**. Your calculator appears in the **Calculators** panel on the left. Click the small arrow next to it to see its contents.
3. **Drag the `SUPERSUB.hpappdir` folder** onto **Application Library** under your calculator.
4. On the calculator, press the **Apps** key and tap the **SUPERSUB** icon. It opens straight onto the gauges.

**If the app doesn't appear or won't open:** try the plain program instead. Drag `SUPERSUB.hpprgm` onto **Programs** under your calculator, then on the calculator press **Shift** then **1** (Program), select **SUPERSUB** and tap **Run**. The files are built for current firmware (2.4 and later); if your calculator is older, update it through the Connectivity Kit first.

Install one or the other, not both. To update later, drag the new copy over the old one and accept the replace prompt. Your last pressures, temperatures and refrigerant are kept between runs, but they reset when you install a new version.

To try it without a calculator, drag the same files into HP's free **HP Prime Virtual Calculator**, which appears in the Connectivity Kit too.

## Using it

**Gauge screen**

| Action | Touch | Keys |
|---|---|---|
| Set suction or liquid pressure | Drag the needle, or tap the dial | Select the gauge, then use Up/Down (±1) or + / − (±10) |
| Set suction or liquid line temp | Drag the SUCT or LIQ slider | Select the slider, then use Up/Down or + / − |
| Choose which control the keys change | Tap it | Left / Right (the selection is outlined in yellow) |
| Type an exact value | **SET VALUE**, or tap a reading a second time | Enter |
| Change refrigerant | **REFRIG**, or tap the refrigerant name | Symb |
| Open the P-T chart | **P-T CHART** | Num |
| Open the service tools | **TOOLS** | Menu |
| Help / quit | Tools list → Help / **EXIT** | Help / Esc |

To enter a vacuum on the low side, type a negative psig value: 1 psi = 2.036 inHg, so 10 inHg is −4.9 psig.

**P-T chart:** scroll with Up/Down, + / −, or by dragging. Left/Right changes the refrigerant. **STEP** switches between 1°F and 5°F rows. **LOOK UP** (or Enter) finds the saturation values for a temperature or a pressure and highlights them in the table.

**Tools:** pick a tool from the **TOOLS** list. The boxes at the top are the inputs: tap one to change it, or use Left/Right to select a box, Up/Down to step it and Enter (or **EDIT**) to type a value. Answers update below the boxes as you go. **HELP** explains how each tool works. Inputs are shared, so the return air readings entered for the charge check are already there in the capacity check, and everything is remembered between runs.

### How it is calculated

- **Superheat** = suction line temp − **dew** temperature at the suction pressure
- **Subcooling** = **bubble** temperature at the liquid pressure − liquid line temp

Using dew on the low side and bubble on the high side keeps the answer correct for blends with glide, such as R-407C, R-448A and R-454B.

Color guide (a reminder only; always use the manufacturer's charging chart):

| | Green | Yellow | Red |
|---|---|---|---|
| Superheat | 5–20°F | 2–5°F or 20–30°F | below 2°F or above 30°F |
| Subcooling | 5–15°F | 2–5°F or 15–25°F | below 2°F or above 25°F |

## Tools

The tools work from the gauge screen's pressures and line temperatures plus a few readings of their own. Typical ranges are for residential and light-commercial comfort cooling; the manufacturer's data always wins.

| Tool | Inputs | What you get |
|---|---|---|
| **Charge check** | Metering device, target subcooling, return air wet bulb, outdoor dry bulb | Fixed orifice: target superheat from the standard charging chart, (3 × return WB − 80 − outdoor DB) ÷ 2, valid for 50–76°F WB and 55–115°F outdoor. TXV/EEV: target subcooling from the data plate. An ADD / REMOVE / OK verdict (±3°F by default), the likely cause from the superheat and subcooling pattern, and the evaporator and condensing saturation temperatures |
| **System check** | Return and supply dry bulb, outdoor dry bulb, discharge line temperature | Evaporator TD, condenser split, approach, coil ΔT, compression ratio, and a discharge temperature check (keep under 225°F) |
| **Capacity check** | Airflow, rated tons, return and supply dry bulb and wet bulb | Total, sensible and latent BTU/h, SHR, CFM per ton, % of rated capacity, and the relative humidity and enthalpy of both airstreams (ASHRAE psychrometrics, corrected for elevation) |
| **Line set charge** | Liquid line size, line length, length included in the factory charge, optional oz/ft from the manual | Ounces to add or remove, from the tube's inside diameter and the refrigerant's liquid density at the liquid line temperature |
| **Nitrogen test** | Start pressure and temperature, pressure and temperature now | The pressure expected from the temperature change alone, and whether the system is holding |
| **Vacuum / evacuation** | Microns, and the start, end and minutes of a decay test | The temperature water boils at that vacuum (500 microns ≈ −12°F), the same vacuum in inHg and psia, and a decay test verdict |
| **Recovery cylinder** | Water capacity (WC), tare weight (TW), weight now | Maximum refrigerant by the 80% rule (WC × 0.8 × specific gravity) and the gross weight to stop at |
| **Refrigerant info** | — | Safety class, usual oil, GWP, glide, whether it must be charged as liquid, boiling point, pressures at 40°F and liquid density |
| **Unit converter** | Kind of value, the number and its unit | Pressure (psig, psia, inHg vacuum, kPa, bar, microns), temperature, capacity (BTU/h, tons, MBH, kW, W), airflow, length and weight |
| **Settings** | Elevation, charge tolerance | Gauges read against the local air, so saturation temperatures, the P-T chart and the dials are corrected for altitude (12.2 psia at 5,000 ft) |

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

The program stores the bubble and dew pressure of each refrigerant every 5°F from −60°F to 150°F. Between rows it interpolates in ln(P), which stays within about 0.06 psi of the source data. A pressure whose saturation temperature falls well outside that range shows `--` instead of a guess. Where a published chart stops at −40°F or −50°F, the table is extended with a Clausius-Clapeyron fit of the chart's lowest rows; tested on CoolProp data, that extension is within 0.01°F over 20°F.

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

In Arkema's chart, the vacuum readings for R-448A, R-449A, R-452A and R-513A are printed in psi below atmosphere, although every other column (and the chart's note) uses inHg. Checked against CoolProp and Hudson's charts, they are now stored as psi. Earlier versions of this app read them as inHg, which made R-513A read about 3 psi too high in deep vacuum (below about −20°F). The other three were not affected, because their vacuum rows fell below the old −40°F table limit.

The tools use these extra properties:

| Property | Source |
|---|---|
| Saturated liquid density (line set charge, cylinder fill) | CoolProp for every refrigerant it models (within 0.4 % of Hudson's charts where both exist); Hudson's charts for R-401A, R-402A, R-408A, R-438A, R-500 and R-502; National Refrigerants for R-409A (`tools/data/liquid_density.csv`) |
| GWP | IPCC AR4 values (the basis of the EPA's HFC rules), weighted by each blend's ASHRAE 34 composition |
| Safety class, usual oil | ASHRAE 34 and the refrigerant makers' literature |
| Moist-air properties (capacity check) | ASHRAE Fundamentals relations; checked against CoolProp's humid-air model within 1.5 % |

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
tools/hpfile.py           writes the calculator's program-file format
tools/hpapp/              format templates for the program and app files
tools/data/*.csv          published P-T tables used for the blends, and liquid densities
tools/data/check/         published liquid pressures used to check CoolProp blend models
tools/ppl_sim.py          small PPL interpreter: runs the program, checks it, renders screenshots
docs/screens/             screenshots made by the simulator
```

The calculator files contain the full readable source, so you can also read and edit the program on the calculator. To change it here, edit `hp-prime/SUPERSUB.txt`, then rebuild.

### Adding a refrigerant

1. Add a line to `REFRIGERANTS` in `tools/gen_pt_tables.py`. Give it the display name, a source (a CoolProp fluid name, or a CSV file in `tools/data` with `temp_F,bubble,dew` columns in psia or psig), a cylinder color and a short description.
2. Run `pip install CoolProp`, then `python3 tools/gen_pt_tables.py --check`.
3. Run `python3 tools/ppl_sim.py` to re-run the checks and regenerate the screenshots.
4. Run `python3 tools/build_calc_files.py` to rebuild the files in `calculator/`. It checks that the files read back correctly and runs the simulator on both the app and the program.

### Simulator

`tools/ppl_sim.py` runs the real program source with scripted key presses and touches. It checks the saturation math, the controls and the screen flow, and checks every tool's answers against an independent calculation (CoolProp refrigerant and humid-air properties, the Murphy-Koop ice vapor pressure equation and the gas law). It also enforces two PPL rules: functions must be defined before they are used, and names must not clash with calculator variables. It is a development aid. The calculator itself is the final test, so please report anything that behaves differently on real hardware. The program and app files use the same format the Connectivity Kit writes: the builder reproduces existing Connectivity Kit files byte for byte when given their contents.
