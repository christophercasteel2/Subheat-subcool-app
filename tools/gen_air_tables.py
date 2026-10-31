#!/usr/bin/env python3
"""Write the generated block of hp-prime/HVACAIR.txt: the tool list, the
input-box ("slot") tables and the small tables the airside tools use.

Edit the tables here, not in the program, then run
    python3 tools/gen_air_tables.py

Duct roughness (ASHRAE Fundamentals, Duct Design, Table 1 categories)
  galvanized steel, medium smooth  0.0003 ft
  fibrous glass duct board, medium rough  0.003 ft
  flexible duct, fully extended, rough  0.01 ft
"""
import os

from ppltables import (check_slots, choice_slot, plist, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "HVACAIR.txt")

UNITS = 8      # the converter's unit list depends on the kind chosen
CHOICES = {
    1: ["RH", "Wet bulb", "Dew point"],
    2: ["Mixed temp", "% outside air"],
    3: ["BTU/h", "CFM", "Temp diff"],
    4: ["Galvanized", "Duct board", "Flex, tight"],
    5: ["Round", "Rectangular"],
    6: ["New RPM", "New CFM"],
    7: ["Airflow", "Pressure", "Velocity", "Heat", "Temperature", "Humidity", "Area"],
}
CONV_UNITS_MAX = 6    # longest list returned by convUnits() in the program

S = slot
C = choice_slot(CHOICES, UNITS, CONV_UNITS_MAX)

SLOTS = [
    # shared by every tool that works with moist air
    S(1, "Elevation", "ft", 0, 100, -1000, 15000, 0, "Elevation above sea level, ft"),
    # air properties
    S(2, "Dry bulb", "°F", 1, 1, -40, 200, 75, "Air temperature (dry bulb)"),
    C(3, "Known", 1, 1, "The second reading you have"),
    S(4, "RH", "%", 1, 1, -60, 200, 50, "RH %, wet bulb or dew point, as chosen"),
    # dew point / sweating
    S(5, "Air temp", "°F", 1, 1, -40, 200, 75, "Air temperature near the surface"),
    S(6, "RH", "%", 1, 1, 1, 100, 55, "Relative humidity of that air, %"),
    S(7, "Surface", "°F", 1, 1, -40, 200, 58, "Surface temp: duct, pipe, glass"),
    # coil capacity
    S(8, "Airflow", "CFM", 0, 25, 0, 100000, 1200, "Airflow through the coil"),
    S(9, "Nominal", "tons", 1, 0.5, 0.5, 200, 3, "Rated size of the system"),
    S(10, "Return DB", "°F", 1, 1, 30, 120, 75, "Return air dry bulb"),
    S(11, "Return WB", "°F", 1, 1, 20, 100, 63, "Return air wet bulb"),
    S(12, "Supply DB", "°F", 1, 1, 20, 120, 55, "Supply air dry bulb"),
    S(13, "Supply WB", "°F", 1, 1, 20, 100, 53, "Supply air wet bulb"),
    # mixed air / economizer
    C(14, "Find", 2, 1, "Work out the mixed temp or the % outside"),
    S(15, "Outside DB", "°F", 1, 1, -40, 130, 90, "Outside air dry bulb"),
    S(16, "Outside RH", "%", 0, 1, 1, 100, 50, "Outside air relative humidity"),
    S(17, "Return DB", "°F", 1, 1, 30, 120, 75, "Return air dry bulb"),
    S(18, "Return RH", "%", 0, 1, 1, 100, 50, "Return air relative humidity"),
    S(19, "% outside", "%", 1, 1, -40, 150, 20, "% outside air, or the mixed air temp"),
    S(20, "Total CFM", "CFM", 0, 50, 0, 1000000, 4000, "Supply fan airflow"),
    # furnace temperature rise
    S(21, "Input", "BTU/h", 0, 1000, 0, 10000000, 80000, "Gas input from the plate (or clocked)"),
    S(22, "Efficiency", "%", 0, 1, 1, 100, 80, "AFUE or steady-state efficiency, %"),
    S(23, "Return", "°F", 1, 1, 0, 120, 68, "Return air temperature"),
    S(24, "Supply", "°F", 1, 1, 0, 250, 120, "Supply air temperature"),
    S(25, "Rise min", "°F", 0, 5, 0, 200, 35, "Low end of the plate's rise range"),
    S(26, "Rise max", "°F", 0, 5, 0, 200, 65, "High end of the plate's rise range"),
    # air heat formulas
    C(27, "Find", 3, 2, "Which one to work out"),
    S(28, "Sensible", "BTU/h", 0, 500, 0, 100000000, 24000, "Sensible heat, BTU/h"),
    S(29, "Airflow", "CFM", 0, 25, 0, 1000000, 1100, "Airflow, CFM"),
    S(30, "Temp diff", "°F", 1, 1, 0, 300, 20, "Temperature difference across"),
    S(31, "Grains diff", "gr/lb", 1, 1, 0, 1000, 0, "Moisture difference (0 = sensible only)", blank=1),
    # static pressure
    S(32, "Supply SP", "in.wc", 2, 0.01, -5, 5, 0.35, "Supply static, after the coil"),
    S(33, "Return SP", "in.wc", 2, 0.01, -5, 5, -0.25, "Return static, before the blower"),
    S(34, "Rated ESP", "in.wc", 2, 0.05, 0.05, 5, 0.5, "Max external static on the plate"),
    S(35, "Filter drop", "in.wc", 2, 0.01, 0, 5, 0, "Pressure drop across the filter", blank=1),
    S(36, "Coil drop", "in.wc", 2, 0.01, 0, 5, 0, "Pressure drop across the coil", blank=1),
    # ventilation (floor area and ceiling also used by the humidifier)
    S(37, "Floor area", "ft²", 0, 100, 0, 1000000, 2000, "Conditioned floor area"),
    S(38, "Bedrooms", "", 0, 1, 0, 50, 3, "Number of bedrooms"),
    S(39, "Ceiling", "ft", 1, 0.5, 6, 50, 8, "Average ceiling height"),
    S(40, "Fan CFM", "CFM", 0, 5, 0, 100000, 100, "Ventilation fan airflow (0 = skip)", blank=1),
    # duct sizer
    S(41, "Airflow", "CFM", 0, 25, 1, 1000000, 1000, "Airflow the duct must carry"),
    S(42, "Friction", "/100ft", 2, 0.01, 0.01, 2, 0.08, "Design friction rate, in.wc per 100 ft"),
    C(43, "Material", 4, 1, "Duct material"),
    S(44, "Rect height", "in", 0, 1, 3, 100, 8, "Height of a rectangular duct, in"),
    # duct check
    C(45, "Shape", 5, 1, "Round or rectangular duct"),
    S(46, "Diameter", "in", 1, 1, 2, 200, 10, "Inside diameter (or width), in"),
    S(47, "Height", "in", 1, 1, 2, 200, 8, "Inside height of a rectangular duct, in"),
    S(48, "Airflow", "CFM", 0, 10, 0, 1000000, 400, "Airflow in the duct"),
    C(49, "Material", 4, 1, "Duct material"),
    S(50, "Measured", "fpm", 0, 10, 0, 10000, 0, "Average velocity you measured (0 = skip)", blank=1),
    # friction rate (Manual D)
    S(51, "Blower ESP", "in.wc", 2, 0.05, 0, 5, 0.5, "Blower static at design CFM (fan table)"),
    S(52, "Coil", "in.wc", 2, 0.01, 0, 5, 0.2, "Coil pressure drop"),
    S(53, "Filter", "in.wc", 2, 0.01, 0, 5, 0.1, "Filter pressure drop"),
    S(54, "Supply reg.", "in.wc", 2, 0.01, 0, 5, 0.03, "Supply register drop"),
    S(55, "Ret. grille", "in.wc", 2, 0.01, 0, 5, 0.03, "Return grille drop"),
    S(56, "Other", "in.wc", 2, 0.01, 0, 5, 0, "Dampers, humidifier, UV light, etc."),
    S(57, "Total length", "ft", 0, 10, 1, 10000, 200, "Total effective length, supply + return"),
    # grille airflow
    S(58, "Ak factor", "ft²", 3, 0.01, 0, 100, 0, "Ak from the grille maker (0 = use size)", blank=1),
    S(59, "Width", "in", 1, 1, 1, 200, 10, "Grille width (nominal), in"),
    S(60, "Height", "in", 1, 1, 1, 200, 6, "Grille height (nominal), in"),
    S(61, "Free area", "%", 0, 5, 1, 100, 70, "Open part of the face, % (if no Ak)"),
    S(62, "Velocity", "fpm", 0, 10, 0, 10000, 400, "Average face velocity measured"),
    S(63, "Grilles", "", 0, 1, 1, 200, 1, "How many alike"),
    # fan laws
    C(64, "Change by", 6, 1, "Give the new RPM or the new CFM"),
    S(65, "CFM now", "CFM", 0, 25, 1, 1000000, 1600, "Airflow now"),
    S(66, "RPM now", "RPM", 0, 10, 1, 10000, 900, "Fan speed now"),
    S(67, "Static now", "in.wc", 2, 0.05, 0, 20, 0.6, "Static pressure now"),
    S(68, "BHP now", "HP", 2, 0.05, 0, 1000, 0.75, "Fan brake horsepower now"),
    S(69, "New RPM", "RPM", 0, 10, 1, 1000000, 1000, "The new RPM (or the new CFM)"),
    S(70, "Motor HP", "HP", 2, 0.25, 0, 1000, 1, "Motor nameplate HP (0 = skip)", blank=1),
    # pulleys and belts
    S(71, "Motor RPM", "RPM", 0, 5, 1, 10000, 1725, "Motor nameplate RPM"),
    S(72, "Motor pulley", "in", 2, 0.1, 0.5, 60, 3.5, "Motor sheave pitch diameter, in"),
    S(73, "Fan pulley", "in", 2, 0.1, 0.5, 100, 7, "Blower sheave pitch diameter, in"),
    S(74, "Centers", "in", 1, 0.5, 1, 200, 18, "Distance between shaft centers, in"),
    S(75, "Target RPM", "RPM", 0, 10, 0, 10000, 0, "Blower RPM you want (0 = skip)", blank=1),
    # fan power
    S(76, "Airflow", "CFM", 0, 25, 1, 1000000, 1200, "Fan airflow"),
    S(77, "Total SP", "in.wc", 2, 0.05, 0.01, 20, 0.8, "Total static across the fan"),
    S(78, "Fan eff.", "%", 0, 1, 1, 100, 50, "Fan efficiency, %"),
    S(79, "Motor eff.", "%", 0, 1, 1, 100, 80, "Motor (and drive) efficiency, %"),
    # unit converter
    C(80, "Convert", 7, 1, "What kind of value to convert"),
    C(81, "From", UNITS, 1, "Unit of that number"),
    S(82, "Value", "", -1, 1, -1000000000, 1000000000, 1200, "Number to convert"),
    # heat loss / gain (indoor and outdoor also used by the cooling load)
    S(83, "Indoor", "°F", 1, 1, -40, 150, 75, "Indoor design temperature"),
    S(84, "Outdoor", "°F", 1, 1, -60, 150, 95, "Outdoor design temperature"),
    S(85, "Walls", "ft²", 0, 10, 0, 1000000, 1200, "Net wall area (without windows)"),
    S(86, "Wall R", "", 1, 1, 0.5, 200, 13, "Wall R-value"),
    S(87, "Ceiling", "ft²", 0, 10, 0, 1000000, 1500, "Ceiling or roof area"),
    S(88, "Ceiling R", "", 1, 1, 0.5, 200, 38, "Ceiling R-value"),
    S(89, "Windows", "ft²", 0, 5, 0, 1000000, 200, "Window and glass door area"),
    S(90, "Window R", "", 2, 0.1, 0.5, 50, 2, "Window R-value (1 / U-factor)"),
    # cooling load
    S(91, "Indoor RH", "%", 0, 1, 1, 100, 50, "Indoor design humidity, %"),
    S(92, "Outdoor RH", "%", 0, 1, 1, 100, 45, "Outdoor design humidity, %"),
    S(93, "People", "", 0, 1, 0, 1000, 4, "Occupants (bedrooms + 1 for homes)"),
    S(94, "Appliances", "W", 0, 50, 0, 1000000, 500, "Lights and appliances running, watts"),
    S(95, "Outside air", "CFM", 0, 5, 0, 1000000, 100, "Infiltration plus ventilation air"),
    S(96, "Other", "BTU/h", 0, 100, 0, 100000000, 6000, "Window sun, duct gain, etc.", blank=1),
    # humidifier (also floor area, ceiling, elevation)
    S(97, "Air changes", "/h", 2, 0.05, 0, 20, 0.5, "Natural air changes per hour in winter"),
    S(98, "Indoor", "°F", 1, 1, 40, 100, 70, "Indoor temperature"),
    S(99, "Target RH", "%", 0, 1, 1, 100, 35, "Indoor humidity wanted, %"),
    S(100, "Outdoor", "°F", 1, 1, -60, 100, 20, "Outdoor temperature"),
    S(101, "Outdoor RH", "%", 0, 1, 1, 100, 60, "Outdoor humidity, %"),
    # evaporative cooler
    S(102, "Outside DB", "°F", 1, 1, 40, 140, 100, "Outside air dry bulb"),
    S(103, "Outside WB", "°F", 1, 1, 20, 100, 65, "Outside air wet bulb"),
    S(104, "Media eff.", "%", 0, 1, 1, 100, 80, "Pad effectiveness, % (see the media rating)"),
    S(105, "Airflow", "CFM", 0, 50, 0, 1000000, 3000, "Cooler airflow"),
]

# tools in tile order: full name, tile lines, colour group, input boxes
# (laid out two per row, left then right)
TOOLS = [
    ("Air properties", "Air", "properties", 1, [2, 3, 4, 1]),
    ("Dew point / sweating", "Dew point", "sweating", 1, [5, 6, 7]),
    ("Coil capacity", "Coil", "capacity", 1, [8, 9, 10, 11, 12, 13, 1]),
    ("Mixed air / economizer", "Mixed air", "economizer", 1, [14, 19, 15, 16, 17, 18, 20, 1]),
    ("Furnace temp rise", "Furnace", "temp rise", 2, [21, 22, 23, 24, 25, 26, 1]),
    ("Air heat formulas", "Heat", "formulas", 2, [27, 1, 28, 29, 30, 31]),
    ("Static pressure", "Static", "pressure", 2, [32, 33, 34, 35, 36]),
    ("Ventilation and ACH", "Ventilation", "and ACH", 2, [37, 38, 39, 40]),
    ("Duct sizer", "Duct", "sizer", 3, [41, 42, 43, 44]),
    ("Duct check / traverse", "Duct", "check", 3, [45, 49, 46, 47, 48, 50]),
    ("Friction rate (Manual D)", "Friction", "rate", 3, [51, 52, 53, 54, 55, 56, 57]),
    ("Grille airflow", "Grille", "airflow", 3, [62, 63, 58, 61, 59, 60]),
    ("Fan laws", "Fan", "laws", 4, [64, 69, 65, 66, 67, 68, 70]),
    ("Pulleys and belts", "Pulleys", "and belts", 4, [71, 72, 73, 74, 75]),
    ("Fan power", "Fan", "power", 4, [76, 77, 78, 79]),
    ("Unit converter", "Unit", "convert", 6, [80, 81, 82]),
    ("Heat loss / gain", "Heat loss", "/ gain", 5, [83, 84, 85, 86, 87, 88, 89, 90]),
    ("Cooling load", "Cooling", "load", 5, [83, 84, 91, 92, 93, 94, 95, 96]),
    ("Humidifier sizing", "Humidifier", "sizing", 5, [37, 39, 97, 99, 98, 100, 101, 1]),
    ("Evaporative cooler", "Evap", "cooler", 5, [102, 103, 104, 105, 1]),
]

STD_ROUND = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36,
             38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60]
ROUGHNESS = [0.0003, 0.003, 0.01]      # ft, in the order of choice list 4
MOTOR_HP = [1 / 6, 1 / 4, 1 / 3, 1 / 2, 3 / 4, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25,
            30, 40, 50, 60, 75, 100]
MOTOR_TXT = ["1/6", "1/4", "1/3", "1/2", "3/4", "1", "1-1/2", "2", "3", "5", "7-1/2",
             "10", "15", "20", "25", "30", "40", "50", "60", "75", "100"]


def check():
    check_slots(SLOTS, TOOLS)
    assert len(ROUGHNESS) == len(CHOICES[4])
    assert len(MOTOR_HP) == len(MOTOR_TXT)


def build_block():
    out = ["// ---- BEGIN TABLES (generated by tools/gen_air_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// standard round duct sizes, in",
        "gRound:=" + plist(STD_ROUND) + ";",
        "// duct roughness, ft: galvanized, duct board, flex pulled tight (ASHRAE)",
        "gRough:=" + plist(ROUGHNESS) + ";",
        "// standard motor sizes, HP",
        "gMotHP:=" + plist([round(h, 6) for h in MOTOR_HP]) + ";",
        "gMotTx:=" + plist(MOTOR_TXT) + ";",
        "",
    ]
    out += slot_functions(TOOLS, CHOICES, UNITS, 80)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
