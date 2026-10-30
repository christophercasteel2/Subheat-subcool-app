# SUPERSUB: superheat and subcooling for the HP Prime

A color, touchscreen superheat and subcooling calculator for the **HP Prime G1** (it also runs on the G2). It is built around a pair of analog manifold gauges that you set by dragging the needles, plus a full pressure-temperature (P-T) chart.

![Gauge screen](docs/screens/gauges.png) ![P-T chart](docs/screens/ptchart_find.png)

*Screens rendered by the development simulator (`tools/ppl_sim.py`). On the calculator, fonts look slightly different.*

## Features

- **Manifold gauges.** The low side is a blue compound gauge that reads from 30 inHg of vacuum up to 350 psig. The high side is a red gauge that reads 0–800 psig. Each dial has a temperature ring for the selected refrigerant, like the scales printed on a real gauge face. The low ring shows dew-point temperatures and the high ring shows bubble-point temperatures.
- **Touch control.** Drag a needle, or tap anywhere on a dial, to set the pressure. Drag the SUCT and LIQ sliders to set the line temperatures. You can also use the arrow keys, or type an exact value.
- **Live results.** Superheat and subcooling update as you move the needles and sliders, color-coded green, yellow or red.
- **P-T chart.** A scrolling table of liquid (bubble) and vapor (dew) pressures with °C, in 1°F or 5°F rows. Vacuum readings show in red as inHg. You can look up a value by temperature or by pressure, and pressure look-ups also report the glide.
- **Refrigerants:** R-22, R-410A, R-454B, R-32, R-134a, R-404A, R-407C, R-448A.

## Install

1. Install the free **HP Connectivity Kit** and connect the calculator by USB. To try the program first, you can also use HP's free **HP Prime Virtual Calculator**.
2. In the Connectivity Kit's *Calculators* pane, right-click **Programs**, choose **New**, and name the program `SUPERSUB`.
3. Open [`hp-prime/SUPERSUB.txt`](hp-prime/SUPERSUB.txt), copy all of it, paste it into the program editor, and save.
4. On the calculator, press **Shift + 1 (Program)**, select **SUPERSUB**, and tap **Run**. You can also type `SUPERSUB` on the Home screen. The program needs firmware 2.x, so update older calculators first.

Your last pressures, temperatures and refrigerant are kept between runs.

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

## Accuracy and data sources

The program stores the bubble and dew pressure of each refrigerant every 5°F from −40°F to 150°F. Between rows it interpolates in ln(P), which stays within about 0.06 psi of the full equation of state.

| Refrigerants | Source |
|---|---|
| R-22, R-32, R-134a, R-404A, R-407C, R-410A | [CoolProp](http://www.coolprop.org), checked against Arkema's NIST REFPROP 10 chart: within 0.15 psi everywhere, 0.07 psi or better for all except R-410A |
| R-454B | Chemours *Opteon XL41 Thermodynamic Properties* (NIST REFPROP 10) |
| R-448A | Arkema Forane refrigerant P-T chart, 05-2025 (NIST REFPROP 10) |

## Repository layout

```
hp-prime/SUPERSUB.txt     the calculator program (HP PPL source)
tools/gen_pt_tables.py    builds the P-T data block inside SUPERSUB.txt
tools/data/*.csv          published tables used for R-454B and R-448A
tools/ppl_sim.py          small PPL interpreter: runs the program, checks it, renders screenshots
docs/screens/             screenshots made by the simulator
```

### Adding a refrigerant

1. Add a line to `REFRIGERANTS` in `tools/gen_pt_tables.py`. Give it the display name, a source (a CoolProp fluid name, or a CSV file in `tools/data` with `temp_F,bubble,dew` columns), and a cylinder color.
2. Run `pip install CoolProp`, then `python3 tools/gen_pt_tables.py --check`.
3. Run `python3 tools/ppl_sim.py` to re-run the checks and regenerate the screenshots, then copy the updated program to the calculator.

### Simulator

`tools/ppl_sim.py` runs the real program source with scripted key presses and touches. It checks the saturation math, the controls and the screen flow. It also enforces two PPL rules: functions must be defined before they are used, and names must not clash with calculator variables. It is a development aid. The calculator itself is the final test, so please report anything that behaves differently on real hardware.
