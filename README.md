# HP Prime HVAC apps

Color, touchscreen apps for HVAC/R work on the **HP Prime G1**. All of them also run on the G2.

| App | What it does | Download |
|---|---|---|
| **[SUPERSUB](#supersub-superheat-and-subcooling-for-the-hp-prime)** | Superheat and subcooling on draggable manifold gauges, a P-T chart for 30 refrigerants, and service tools for the refrigerant circuit | [`SUPERSUB.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/SUPERSUB.zip) |
| **[HVACAIR](#hvacair-airside-tools-the-rebuilt-hvac-suite)** | The rebuilt HVAC Suite: 20 airside tools, including psychrometrics, coil capacity, furnace temperature rise, static pressure, duct sizing, fan laws, pulleys and quick loads | [`HVACAIR.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/HVACAIR.zip) |
| **[HVACELEC](#hvacelec-electrical-tools-for-the-hp-prime)** | 20 electrical tools: Ohm's law, motor and compressor checks, capacitor and thermistor tests, NEC wire and breaker sizing, MCA / MOCP, voltage drop and more | [`HVACELEC.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/HVACELEC.zip) |
| **[NECCALC](#neccalc-nec-calculator-for-electrical-class)** | A study app for electrical class with every calculator, chart and guide of electricalcalctools.com (19 tools: voltage drop, wire size, ampacity for every insulation type in a raceway or free air, breaker, conduit fill, AWG, feeder, ground wire, box fill, MCA/MOCP, power, Ohm's law, kWh, cost, derating, drop table, breaker/wire chart, appliances, NEMA) plus NEC notes. Separate from HVACELEC, so you can delete it after the class | [`NECCALC.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/NECCALC.zip) |

They all install the same way (see [Install](#install-drag-and-drop-no-typing)), and you can have all of them on the calculator at once.

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
- **Service tools.** Full check (every reading on one screen, A/C cooling or heat pump heating), charge check, system check, capacity check, line set charge, nitrogen test, vacuum, recovery cylinder, refrigerant info, unit converter and an altitude setting. See [Tools](#tools) below.
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
| **Full check** | Mode (A/C cooling or heat pump heating), suction and head pressure, SLT, LLT, DLT, return, supply and outdoor air | Every reading on one screen: evaporator saturation (dew at suction), condensing saturation (bubble at head), superheat (SLT − dew), subcooling (bubble − LLT), discharge superheat (DLT − dew at head), air ΔT, evaporator TD, condenser split, approach, compression ratio, and the likely problem from superheat, subcooling, suction and head together (low charge, overcharge, restriction, weak compressor, low indoor airflow, dirty condenser). In heating mode the indoor coil is the condenser, so the split and approach use return air and the evaporator TD uses outdoor air. Suction, head, SLT and LLT are the same values as on the gauge screen. Supply and return are air temperatures, not dew or bubble points |
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

# HVACAIR: airside tools (the rebuilt HVAC Suite)

HVACAIR replaces the HVAC Suite with something a service tech can use on every call. It covers the same ground (psychrometrics, loads, air processes, ducts and fans), but each job is its own tool with a handful of boxes, the same way HVACELEC works. The answers update as you type, colored green (OK), yellow (check it) or red (problem). It has a different name, so installing it does not replace your old HVAC Suite; delete that one when you no longer need it.

![Home screen](docs/screens/air_home.png) ![Coil capacity](docs/screens/air_03_coil_capacity.png)

![Furnace temp rise](docs/screens/air_05_furnace_temp_rise.png) ![Duct sizer](docs/screens/air_09_duct_sizer.png)

## Installing HVACAIR

Download [`HVACAIR.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/HVACAIR.zip), unzip it, and drag the `HVACAIR.hpappdir` folder onto **Application Library** under your calculator in the Connectivity Kit. If the app doesn't show up, drag `HVACAIR.hpprgm` onto **Programs** instead. On the calculator, press **Apps** and tap **HVACAIR**. It is used exactly like HVACELEC (see [Using HVACELEC](#using-hvacelec)). One extra: the **Elevation** box is shared, so set it once and every moist-air tool corrects for the thinner air.

## HVACAIR tools

| Tile | Inputs | What you get |
|---|---|---|
| **Air properties** | Dry bulb plus RH, wet bulb or dew point; elevation | RH, wet bulb, dew point, grains, enthalpy, specific volume, density, air pressure, and the 1.08 / 4.5 factors at that elevation |
| **Dew point / sweating** | Air temperature, RH, surface temperature | Dew point, the margin, WILL SWEAT / close / OK, and the humidity at which that surface starts to sweat |
| **Coil capacity** | CFM, nominal tons, return and supply dry and wet bulb | Total, sensible and latent BTU/h, tons and % of rated, SHR, split, CFM per ton, and condensate in gal/h |
| **Mixed air / economizer** | Outside and return temperature and RH, % outside air or the measured mixed temperature, CFM | Mixed temperature or % outside air, outside CFM, mixed RH, wet bulb and enthalpy, and whether outside air can help cool |
| **Furnace temp rise** | Input BTU/h, efficiency, return and supply temperature, the plate's rise range | Output, rise checked against the range, CFM = output ÷ (1.08 × rise), and the CFM at mid-range |
| **Air heat formulas** | Find BTU/h, CFM or ΔT; the other two; optional grains difference | Sensible (1.08), latent (0.68) and total heat, corrected for elevation |
| **Static pressure** | Supply and return static, rated ESP, optional filter and coil drops | Total external static, % of rated, and how much each part uses |
| **Ventilation and ACH** | Floor area, bedrooms, ceiling height, fan CFM | ASHRAE 62.2-2016 rate (0.03 × ft² + 7.5 × (bedrooms + 1)), air changes per hour, run time |
| **Duct sizer** | CFM, friction rate, material, rectangular height | Exact and next standard round size, a rectangular size of that height, velocity, friction and aspect ratio |
| **Duct check / traverse** | Round or rectangular size, CFM, material, measured velocity | Area, velocity, velocity pressure, friction, equal round diameter, and CFM from a traverse |
| **Friction rate (Manual D)** | Blower static, coil, filter, register, grille and other drops, total effective length | Available static and the design friction rate (ASP × 100 ÷ TEL), checked against Manual D's 0.06–0.18 band |
| **Grille airflow** | Face velocity, Ak factor or size and free area, number of grilles | CFM per grille and in total |
| **Fan laws** | CFM, RPM, static and BHP now; the new RPM or CFM; motor HP | New CFM, RPM, static and BHP, and whether the motor is overloaded |
| **Pulleys and belts** | Motor RPM, both pulley diameters, center distance, target RPM | Blower RPM, ratio, belt pitch length, belt speed, deflection, and the pulley for a target speed |
| **Fan power** | CFM, total static, fan and motor efficiency | Air HP, brake HP, motor watts, watts per CFM and the motor size |
| **Unit converter** | Kind, number, unit | Airflow, pressure (in.wc, Pa, psi, inHg), velocity, heat, temperature, humidity and area |
| **Heat loss / gain** | Indoor and outdoor temperature; wall, ceiling and window areas and R-values | Conduction through each (area × ΔT ÷ R), total, and UA |
| **Cooling load** | Indoor and outdoor temperature and RH, people, appliance watts, outside air CFM, other gains | Walls (from Heat loss / gain), people (230 + 200 BTU/h each), appliances, outside air sensible and latent, total, tons, SHR and airflow |
| **Humidifier sizing** | Floor area, ceiling, air changes, indoor temperature and target RH, outdoor temperature and RH | Air leaking in, the water needed in lb/h and gal/day, and the indoor dew point |
| **Evaporative cooler** | Outside dry and wet bulb, pad effectiveness, CFM | Leaving temperature and RH, cooling BTU/h, and water evaporated |

Compared with the old HVAC Suite, this version leaves out the engineering-design parts: multi-zone hourly loads, duct networks with static regain and critical paths, the fitting library, Pareto optimization, NC/RC acoustics and SI input. Ask if you want any of them back.

## HVACAIR sources

| Data | Used by | Source / check |
|---|---|---|
| Moist-air relations (Hyland-Wexler saturation pressure, wet-bulb equation, enthalpy, volume) | Every air tool | ASHRAE Fundamentals, I-P. The tests compare humidity ratio, wet bulb, dew point, RH and volume with CoolProp's humid-air model at several states and elevations |
| Standard atmosphere pressure from elevation | Elevation box | Same formula as SUPERSUB's settings |
| Duct friction: Darcy-Weisbach with the Colebrook friction factor, standard air; equal-friction rectangular diameter 1.30 (ab)^0.625 / (a+b)^0.25 | Duct sizer, duct check | ASHRAE Fundamentals, Duct Design. Roughness: galvanized 0.0003 ft ([ASHRAE](https://www.ashrae.org/news/esociety/determining-the-absolute-roughness-of-phenolic-duct)), duct board 0.003 ft, flex pulled tight 0.01 ft. Checked against a separate Colebrook solution; the older Wright equation (rougher duct) reads 6–9% higher |
| Duct velocity limits: 900 fpm supply, 700 fpm return | Duct colors | ACCA Manual D maximums ([Energy Vanguard](https://energyvanguard.com/blog/duct-design-5-sizing-ducts)) |
| Friction rate = ASP × 100 / TEL, design band 0.06–0.18 | Friction rate | ACCA Manual D ([ACCA](https://hvac-blog.acca.org/definitive-design-accas-manual-d-revised/)) |
| Ventilation 0.03 × floor area + 7.5 × (bedrooms + 1) | Ventilation | ASHRAE 62.2-2016 ([ACCA](https://hvac-blog.acca.org/2016-update-ashrae-62-2/)) |
| 230 sensible + 200 latent BTU/h per person | Cooling load | ACCA Manual J ([Green Building Advisor](https://www.greenbuildingadvisor.com/article/understanding-manual-j-occupant-loads)) |

The cooling load is a quick estimate for checking and for class work, not a Manual J. The maker's data and your local code come first.

# HVACELEC: electrical tools for the HP Prime

An electrical calculator for HVAC/R service: 20 tools behind one colorful home screen, from Ohm's law to NEC motor-circuit sizing. Every tool works the same way. The input boxes are at the top, and the answers underneath update as soon as you change anything, colored green (OK), yellow (check it) or red (problem).

![Home screen](docs/screens/elec_home.png) ![Motor NEC sizing](docs/screens/elec_10_motor_nec_sizing.png)

![Capacitor test](docs/screens/elec_07_capacitor_test.png) ![Unit MCA / MOCP](docs/screens/elec_12_unit_mca_mocp.png)

## Installing HVACELEC

Follow the [SUPERSUB steps](#install-drag-and-drop-no-typing) with the HVACELEC files. Download [`HVACELEC.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/HVACELEC.zip) and unzip it. Then, in the Connectivity Kit, drag the `HVACELEC.hpappdir` folder onto **Application Library** under your calculator. If the app doesn't show up, drag `HVACELEC.hpprgm` onto **Programs** instead. On the calculator, press **Apps** and tap **HVACELEC**.

## Using HVACELEC

| Action | Touch | Keys |
|---|---|---|
| Open a tool | Tap its tile | Arrows, then Enter. Menu lists every tool |
| Change a value | Tap its box. A number box opens a number entry, a list opens a chooser, and a two-way choice (1-phase / 3-phase) just flips | Select the box with Left/Right, type the number on the keypad, press Enter |
| Step a value | | Up / Down |
| Fix typing | | Del erases a digit, Esc cancels, − makes it negative |
| Put the example values back | **RESET** | |
| Next or previous tool | **NEXT >** / **< PREV** | |
| How the tool works | **HELP** (top right) | Help |
| Back to the tiles / quit | **HOME** / **EXIT** | Esc |

A box showing `--` is optional and is ignored while it is 0. In Ohm's law, `?` marks the values to work out. Your values are kept between runs.

## HVACELEC tools

| Tile | Inputs | What you get |
|---|---|---|
| **Ohm's law** | Any two of volts, amps, ohms and watts | The other two, and the formulas used |
| **Power** | Volts, amps, phase, power factor, efficiency | Watts, VA, VAR, BTU/h and motor output HP |
| **Load amps** | A load in W, kW, HP (motor output) or BTU/h; volts, phase, PF, efficiency | Amps, input watts and VA, the 125% continuous-load figure and the copper wire for it |
| **Series / parallel** | Up to four resistors or capacitors, and the source voltage | Total resistance or capacitance. For resistors: the current, power, and each part's volts or amps. For capacitors in series: the volts on each |
| **Amp check** | Nameplate voltage, measured volts, RLA or FLA, clamp reading, wraps through the clamp | The allowed voltage range (nameplate ±10%: 187–253 V for 208-230 V), a voltage verdict, the running amps and the % of rated load |
| **3-phase balance** | Three line voltages and three line currents | % voltage unbalance (NEMA method), the NEMA derating factor, % current unbalance, and the high and low legs |
| **Capacitor test** | Rated µF and tolerance; a meter reading, or the running amps through and volts across the capacitor | Measured µF (2652 × A ÷ V at 60 Hz), GOOD / WEAK / HIGH against the tolerance, % off rating, and the amps a good capacitor draws |
| **Winding check** | 1- or 3-phase, ohms between each pair of terminals, winding temperature | Single phase: which terminal is common, run and start, whether C-R + C-S equals S-R, and the open-overload and open-winding patterns. Three phase: whether the windings match. Readings corrected to 77°F for comparing with the spec |
| **Megohm test** | 1-minute reading and winding temperature; optional 10-minute and 30-second readings | The reading corrected to 40°C and checked against the IEEE 43 minimum (5 MΩ for windings under 1000 V), the polarization index and the dielectric absorption ratio |
| **Motor NEC sizing** | HP, phase, voltage, nameplate FLA, service factor | Table full-load current (NEC 430.248 / 430.250), the 125% wire size, the largest breaker and fuses (430.52, next standard size up), the disconnect (115%) and the overload setting (430.32) |
| **Motor LRA and RPM** | Code letter, HP, volts, phase, nameplate RPM, Hz | Locked-rotor kVA per HP and the LRA range (NEC 430.7(B)), poles, synchronous speed and slip |
| **Unit MCA / MOCP** | Largest motor's RLA, the other motors' FLAs, electric heat amps | MCA = 1.25 × largest + other motors + 1.25 × heat. MOCP = 2.25 × largest + the rest, rounded down to a standard size but never below the MCA. Copper wire at 60°C and 75°C, and the disconnect rating |
| **Voltage drop** | Amps, one-way length, wire size and material, phase, source volts, allowed % | Volts and % dropped, volts at the load, the smallest wire within the limit, and the wire's ampacity |
| **Wire ampacity** | Size, copper or aluminum, insulation and terminal ratings, ambient temperature, number of current-carrying wires, rooftop exposure | The Table 310.16 ampacity, the ambient and bundling factors, the derated and terminal-limited ampacity, and the largest breaker (240.4(B) and (D)) |
| **Transformer** | VA, phase, primary and secondary volts, measured secondary amps | Turns ratio, primary and secondary full-load amps, % loaded, and the largest primary fuse (NEC 450.3(B)) |
| **Wye / delta** | Hookup, line volts, line amps | Line-to-neutral or phase voltage, phase current, kVA, and the high leg of a center-tapped delta |
| **Electric heat** | Rated kW and volts, applied volts, phase, measured amps, temperature rise | Output at the applied voltage (kW goes with V²), BTU/h, amps, element resistance, measured kW, airflow (CFM = BTU/h ÷ (1.08 × rise)) and the 125% circuit amps |
| **Thermistor check** | Curve (10K Type II, 10K Type III, or custom R at 77°F and Beta), reading in kΩ, actual temperature | The temperature the reading means, the resistance it should have, the difference, and the curve's resistance at 32°F, 77°F and 100°F |
| **Energy cost** | Volts, amps, phase, PF, $/kWh, hours a day, optional cooling capacity | kW, and the cost per hour, day, month and year. With the capacity: EER, COP and kW per ton |
| **Unit converter** | Kind of value, the number and its unit | Power (W, kW, HP, BTU/h, MBH, tons), energy, current, voltage, resistance, capacitance (MFD = µF) and temperature |

## HVACELEC code tables and sources

The tables are typed into `tools/gen_elec_tables.py`, which writes them into the program. The tests check spot values copied from the sources separately.

| Data | Used by | Checked against |
|---|---|---|
| NEC Table 430.248 and 430.250, motor full-load current | Motor NEC sizing | [Elliott Electric's 430.248 table](https://elliottelectric.com/StaticPages/ElectricalReferences/ElectricalTables/Amperes_Single_Phase_Alternate.aspx), [Transcat's full-load current reference](https://www.transcat.ca/media/pdf/FullLoadCurrent.pdf) (both tables), [VoltageLab](https://www.voltagelab.com/?p=10433) |
| NEC Table 310.16 ampacity, copper and aluminum, 60/75/90°C, 14 AWG to 500 kcmil | Every wire size, Wire ampacity | [Cerrowire's ampacity chart](https://www.cerrowire.com/products/resources/tables-calculators/ampacity-charts/) and [Omnicable's NEC ampacity data](https://www.omnicable.com/docs/default-source/technical-resources/nec-ampacity-data.pdf). Both reproduce the 2017 table, which has the same values as 2020/2023 Table 310.16 |
| NEC Chapter 9 Table 8 conductor areas; K = 12.9 (copper), 21.2 (aluminum) | Voltage drop | |
| NEC 240.6(A) standard sizes, 240.4(D) small-conductor limits | Breaker and fuse sizes | |
| NEC Table 430.7(B) code letters | Motor LRA | A–P and V from [EEPower](https://eepower.com/technical-articles/the-meaning-behind-motor-and-multi-motor-marking/); R–U fill the gap between them |
| NEMA MG 1 voltage-unbalance derating curve: 1.00 up to 1%, then 0.95 at 2%, 0.88 at 3%, 0.82 at 4% and 0.75 at 5% | 3-phase balance | Approximate. Published copies of the curve differ by about 0.01 ([electrical-engineering-portal](https://electrical-engineering-portal.com/voltage-unbalance-nema-motor-performance)) |
| Ambient correction from the NEC 310.15(B) equation | Wire ampacity | Gives the code's correction-factor tables (for example 0.91 for 90°C wire at 104°F) |
| 10K Type III thermistor, Steinhart-Hart | Thermistor check | Within 0.02°F of BAPI's 10K-3 table from −39°F to 187°F (`tools/data/thermistor_10k3_bapi.csv`) |
| 10K Type II thermistor, Steinhart-Hart (32,650 Ω at 32°F) | Thermistor check | Within 0.1% of published 10K Type II charts from 32°F to 68°F |
| IEEE 43 temperature correction, 5 MΩ minimum and PI guide | Megohm test | |

The NEC values are for checking and learning. The equipment nameplate, the manufacturer's instructions and your local code come first. Lock out the power and prove it dead before you test resistance, capacitors or insulation.

# NECCALC: NEC calculator for electrical class

A separate app built for an electrical class. It has every calculator, chart and guide on [electricalcalctools.com](https://electricalcalctools.com) as a tile, plus **Learn** pages, with the same tap-a-box or type-on-the-keypad entry as HVACELEC. It shares nothing with the other apps, so deleting it from the calculator after the class leaves them untouched.

![Home screen](docs/screens/nec_home.png) ![Ampacity in free air](docs/screens/nec_ampacity_free_air.png)

Download [`NECCALC.zip`](https://github.com/christophercasteel2/Subheat-subcool-app/raw/ccr-d1b6c2f8-hvvb6p/calculator/NECCALC.zip), unzip it, and drag `NECCALC.hpappdir` onto **Application Library** (or `NECCALC.hpprgm` onto **Programs**). To remove it later, delete it from the Application Library (or Programs) in the Connectivity Kit or on the calculator.

| Tile | What it does |
|---|---|
| **Voltage drop** | VD, % drop and volts at the load for 1- or 3-phase, by K (12.9 Cu, 21.2 Al) or Chapter 9 Table 8 resistance; the smallest wire and longest run for your % limit |
| **Wire size** | Smallest wire for a load (125% if continuous): the insulation column after the temperature factor, the terminal column, 240.4(D) for the breaker, and 3% / 5% voltage drop for the run and system (120–600 V, 1- or 3-phase) |
| **Ampacity** | Any size 18 AWG–2000 kcmil, copper or aluminum, any insulation type (TW, UF, RHW, THHW, THW, THWN, XHHW, USE, ZW, TBS, SA, SIS, FEP, FEPB, MI, RHH, RHW-2, THHN, THW-2, THWN-2, USE-2, XHH, XHHW-2, ZW-2, NM-B), in a raceway or cable (Table 310.16) or **free air (Table 310.17)**; ambient correction (310.15(B)(1), in °C or °F), bundling (310.15(C)(1)), optional terminal limit, and 240.4(D) |
| **Breaker size** | 125% of continuous + noncontinuous to the next standard size, whether the wire is big enough, and the largest breaker the wire allows |
| **Conduit fill** | How many wires fit (with Note 7 rounding), or the smallest conduit for your wires (with a second group, such as a ground), for EMT, FMC, IMC, RMC and PVC 40/80; THHN/THWN, XHHW, TW/THW, RHW (no jacket) and FEP areas |
| **AWG chart** | Circular mils, mm², diameter, Table 8 resistance, 310.16 and 310.17 ampacities in all three columns, your insulation's ampacity, its Table 5 area and the size's common use |
| **Feeder size** | Feeder or service wire by ampacity (with the 83% dwelling rule of 310.12) and by a 2, 3 or 5% voltage drop; the drop at the chosen size and the 250.122 ground |
| **Ground wire** | Equipment ground from the breaker rating (Table 250.122, up to 4000 A) or grounding electrode conductor from the service wire (Table 250.66), in copper and aluminum, with the rod / concrete-encased / ring limits |
| **Box fill** | 314.16(B) counts (wires, clamps, yokes, grounds, fittings) × volume per wire, for 20 Table 314.16(A) boxes or a custom volume |
| **MCA / MOCP** | MCA = 1.25 × RLA + fans + other, the wire for it (Cu and Al 75°C, Cu 60°C), and the MOCP from 175% (next standard size) capped at 225%, or the nameplate MOP |
| **Power calc** | Any two of V, I, R, W, with power factor and 1- or 3-phase: watts, VA, VAR, kW, kVA |
| **Ohm's law** | Any two of E, I, R, P |
| **kWh** | Daily, monthly and yearly kWh and cost of a device; amps at 120 and 240 V |
| **Elec. cost** | Monthly, yearly and daily cost from kWh, with the site's average rate for each state or your own rate |
| **Derating** | Base ampacity × 310.15(B)(1) temperature factor × 310.15(C)(1) bundling factor |
| **VD table** | % and volts dropped at 25–300 ft for a size, load and system, colored by the 3% / 5% limits, and the longest run for each |
| **Breaker / wire chart** | For each standard breaker 15–800 A: copper and aluminum wire in the 60°C and 75°C columns (240.4(D) included, parallel sets above 2000 kcmil), the 250.122 ground and the 80% continuous load |
| **Appliances** | Breaker, copper and aluminum wire, outlet and NEC section for dryers, ranges, ovens, cooktops, water heaters, tankless heaters, hot tubs, EV chargers (16–80 A), mini-splits, A/C, well pumps, subpanels and 100/200 A dwelling services |
| **NEMA plugs** | Voltage, amps, wires, typical use and locking type of 23 NEMA configurations (1-15 to L15-30), with the 80% cord-load limit |
| **Learn** | 18 pages: Ohm's law and power, voltage drop, ampacity steps, terminals, 240.4(D), insulation letters, conduit fill, box fill, breaker sizing, AWG, GFCI vs AFCI, nameplates (MCA, MOCP, RLA, FLA, LRA), feeders and 310.12, grounding, NEMA names, temperature factors, energy and cost, appliance circuits |

**Where the numbers come from.** Tables 310.16 and 310.17 (18 AWG–2000 kcmil) are copied from [Omnicable's reproduction of the NEC ampacity tables](https://www.omnicable.com/docs/default-source/technical-resources/nec-ampacity-data.pdf) (2017 numbering 310.15(B)(16)/(17); same values in 2020 and 2023). The temperature correction factors come from the code's own equation and match the printed table at every row. Chapter 9 Table 5 areas for THHN/THWN and XHHW were checked against a [published Table 5 listing](https://conduit-fill-calc.pages.dev/wire-sizes) from 14 AWG to 500 kcmil, and TW, RHW and FEP at 14–4 AWG. Table 4 areas for EMT, FMC, IMC and RMC (½–2 in) were checked against a [conduit-fill dataset](https://huggingface.co/datasets/anthonymeo/conduitFill), and PVC at several sizes. The tests also reproduce Annex C counts (for example 26 #12 THHN in 1 in EMT). Table 8 copper resistances for 14–6 AWG match a [Mike Holt sample](https://www.mikeholt.com/instructor2/img/product/pdf/1220452413sample.pdf); every value passes resistance × circular mils ≈ 12.9 (Cu) or 21.2 (Al). The larger TW/THW areas and the remaining Table 8 values were not checked against a second source, so compare with your code book if an answer looks off. Tables 250.122, 250.66, 314.16(A) and 310.12 were typed from the code and spot-checked by the tests. The appliance guide, NEMA list and state rates follow the website, but the wire sizes are recomputed from Table 310.16 and 240.4(D): where the site's own charts disagree with the NEC (for example its 3 AWG copper at 90°C and parts of its ground and EV charts), the app uses the NEC value.

Use the app only where your instructor allows calculators with programs or stored tables.

# Development

## Repository layout

```
calculator/               ready-to-install files (built, do not edit by hand)
  SUPERSUB.hpappdir/        app: drag onto Application Library
  SUPERSUB.hpprgm           program: drag onto Programs
  SUPERSUB.zip              both, for one download
  HVACELEC.hpappdir/, HVACELEC.hpprgm, HVACELEC.zip   the same for HVACELEC
  HVACAIR.hpappdir/, HVACAIR.hpprgm, HVACAIR.zip      the same for HVACAIR
  NECCALC.hpappdir/, NECCALC.hpprgm, NECCALC.zip      the same for NECCALC
hp-prime/SUPERSUB.txt     SUPERSUB's readable source (HP PPL)
hp-prime/HVACELEC.txt     HVACELEC's readable source (HP PPL)
hp-prime/HVACAIR.txt      HVACAIR's readable source (HP PPL)
hp-prime/NECCALC.txt      NECCALC's readable source (HP PPL)
tools/gen_pt_tables.py    builds the P-T data block inside SUPERSUB.txt
tools/gen_elec_tables.py  builds the tool, input-box and NEC table block inside HVACELEC.txt
tools/gen_air_tables.py   builds the tool and input-box block inside HVACAIR.txt
tools/gen_nec_tables.py   builds the tool, input-box and NEC table block inside NECCALC.txt
tools/ppltables.py        helpers both table generators share
tools/build_calc_files.py builds the calculator/ folder from both sources
tools/hpfile.py           writes the calculator's program-file format
tools/hpapp/              format templates for the program and app files
tools/data/*.csv          published P-T tables used for the blends, liquid densities,
                          and BAPI's 10K-3 thermistor table
tools/data/check/         published liquid pressures used to check CoolProp blend models
tools/ppl_sim.py          small PPL interpreter: runs SUPERSUB, checks it, renders screenshots
tools/test_hvacelec.py    the same for HVACELEC
tools/test_hvacair.py     the same for HVACAIR (checked against CoolProp)
tools/test_neccalc.py     the same for NECCALC (checked against published NEC values)
docs/screens/             screenshots made by the simulator
```

The calculator files contain the full readable source, so you can also read and edit the programs on the calculator. To change one here, edit its file in `hp-prime/`, then rebuild with `python3 tools/build_calc_files.py`. For HVACELEC's and HVACAIR's tools, input boxes and tables, edit `tools/gen_elec_tables.py` or `tools/gen_air_tables.py` and run it first; it writes the table block into the program.

### Adding a refrigerant

1. Add a line to `REFRIGERANTS` in `tools/gen_pt_tables.py`. Give it the display name, a source (a CoolProp fluid name, or a CSV file in `tools/data` with `temp_F,bubble,dew` columns in psia or psig), a cylinder color and a short description.
2. Run `pip install CoolProp`, then `python3 tools/gen_pt_tables.py --check`.
3. Run `python3 tools/ppl_sim.py` to re-run the checks and regenerate the screenshots.
4. Run `python3 tools/build_calc_files.py` to rebuild the files in `calculator/`. It checks that the files read back correctly and runs the simulator on both the app and the program.

### Simulator

`tools/ppl_sim.py` runs the real program source with scripted key presses and touches. It checks the saturation math, the controls and the screen flow, and checks every tool's answers against an independent calculation (CoolProp refrigerant and humid-air properties, the Murphy-Koop ice vapor pressure equation and the gas law). `tools/test_hvacelec.py` and `tools/test_hvacair.py` use the same interpreter for the other two apps; HVACAIR's moist-air answers are compared with CoolProp's humid-air model. The simulator also rejects a `LOCAL` with more than 8 names, which the calculator refuses. It checks each tool against its own calculation or values copied from the published tables, and plays through the tiles, typed entry, dialogs and buttons. It also enforces two PPL rules: functions must be defined before they are used, and names must not clash with calculator variables. It is a development aid. The calculator itself is the final test, so please report anything that behaves differently on real hardware. The program and app files use the same format the Connectivity Kit writes: the builder reproduces existing Connectivity Kit files byte for byte when given their contents.
