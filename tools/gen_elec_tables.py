#!/usr/bin/env python3
"""Write the generated block of hp-prime/HVACELEC.txt: the tool list, the
input-box ("slot") tables and the code tables the electrical tools use.

Edit the tables here, not in the program, then run
    python3 tools/gen_elec_tables.py

Code tables (NEC 2020/2023 numbering; the values are the same in the 2017
edition)
  430.248  full-load current, single-phase AC motors
  430.250  full-load current, three-phase AC motors (induction type)
  310.16   allowable ampacity, 60/75/90 C, copper and aluminum
  Chapter 9 Table 8   conductor size in circular mils
  240.6(A) standard fuse and inverse-time breaker ratings
  430.7(B) locked-rotor code letters, kVA per horsepower
Thermistor curves (Steinhart-Hart coefficients)
  10K Type II   A, B, C as published for the BetaTherm 10K3A1 curve
                (32,650 ohms at 32 F); agrees with published Type II charts
  10K Type III  ACI "AN" coefficients; checked against BAPI's 10K-3 table
                in tools/data/thermistor_10k3_bapi.csv (max 0.02 F error)
"""
import csv
import math
import os

from ppltables import (check_slots, choice_slot, plist, pmatrix, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "HVACELEC.txt")
DATA = os.path.join(ROOT, "tools", "data")

# ---------------------------------------------------------------------------
# choice lists, numbered as the program's choiceList(c) numbers them

UNITS = 18     # the converter's unit list depends on the kind chosen
CHOICES = {
    1: ["1-phase", "3-phase"],
    2: ["Copper", "Aluminum"],
    3: ["18 AWG", "16 AWG", "14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG",
        "4 AWG", "3 AWG", "2 AWG", "1 AWG", "1/0 AWG", "2/0 AWG", "3/0 AWG",
        "4/0 AWG", "250 kcmil", "300 kcmil", "350 kcmil", "400 kcmil", "500 kcmil"],
    4: ["60°C", "75°C", "90°C"],
    5: ["60°C", "75°C"],
    6: ["No", "Yes"],
    7: ["60 Hz", "50 Hz"],
    8: ["±5%", "±6%", "±10%", "±20%"],
    9: ["1/6 HP", "1/4 HP", "1/3 HP", "1/2 HP", "3/4 HP", "1 HP", "1-1/2 HP",
        "2 HP", "3 HP", "5 HP", "7-1/2 HP", "10 HP", "15 HP", "20 HP", "25 HP",
        "30 HP", "40 HP", "50 HP", "60 HP", "75 HP", "100 HP", "125 HP",
        "150 HP", "200 HP"],
    10: ["115 V", "200 V", "208 V", "230 V", "460 V", "575 V"],
    11: ["1.0", "1.15 or more"],
    12: list("ABCDEFGHJKLMNPRSTUV"),
    13: ["115 V", "208-230 V", "230 V", "265 V", "277 V", "460 V", "575 V"],
    14: ["Resistors", "Capacitors"],
    15: ["Series", "Parallel"],
    16: ["10K Type II", "10K Type III", "Custom Beta"],
    17: ["Power", "Energy", "Current", "Voltage", "Resistance", "Capacitance",
         "Temperature"],
    19: ["Wye (star)", "Delta"],
    20: ["Watts", "kW", "HP", "BTU/h"],
}
CONV_UNITS_MAX = 6    # longest list returned by convUnits() in the program

# ---------------------------------------------------------------------------
# input boxes ("slots"); the number is the index the program uses
#   label, unit, decimals (-1 = as many as needed), Up/Down step, low, high,
#   default, help line, choice list (0 = a number), blank (1: 0 shows "--",
#   2: 0 shows "?")

S = slot
C = choice_slot(CHOICES, UNITS, CONV_UNITS_MAX)


SLOTS = [
    # Ohm's law: enter any two
    S(1, "Volts (E)", "V", -1, 1, 0, 10000000, 120, "Voltage; leave 0 if unknown", blank=2),
    S(2, "Amps (I)", "A", -1, 0.1, 0, 10000000, 0, "Current; leave 0 if unknown", blank=2),
    S(3, "Ohms (R)", "Ω", -1, 1, 0, 1000000000, 12, "Resistance; leave 0 if unknown", blank=2),
    S(4, "Watts (P)", "W", -1, 10, 0, 1000000000, 0, "Power; leave 0 if unknown", blank=2),
    # power, load amps and energy cost share these
    S(5, "Volts", "V", 1, 1, 0, 100000, 230, "Volts at the load (line to line for 3-phase)"),
    S(6, "Amps", "A", 2, 0.1, 0, 100000, 10, "Measured amps (one line for 3-phase)"),
    C(7, "Phase", 1, 1, "Single phase or three phase"),
    S(8, "Power factor", "", 2, 0.01, 0.05, 1, 0.9, "PF: 1.0 for heaters, about 0.8-0.9 motors"),
    S(9, "Efficiency", "%", 0, 1, 1, 100, 85, "Motor efficiency in % (output / input)"),
    # load amps
    S(10, "Load", "", -1, 1, 0, 1000000000, 5, "Size of the load, in the unit below"),
    C(11, "Load unit", 20, 2, "W or kW input, HP motor output, or BTU/h"),
    # series / parallel
    C(12, "Parts", 14, 1, "Resistors or capacitors"),
    C(13, "Hookup", 15, 1, "Series (one path) or parallel"),
    S(14, "Source V", "V", 1, 1, 0, 100000, 24, "Volts across the whole circuit (0 = skip)", blank=1),
    S(15, "Part 1", "", -1, 1, 0, 1000000000, 10, "First value; 0 = not used", blank=1),
    S(16, "Part 2", "", -1, 1, 0, 1000000000, 20, "Second value; 0 = not used", blank=1),
    S(17, "Part 3", "", -1, 1, 0, 1000000000, 0, "Third value; 0 = not used", blank=1),
    S(18, "Part 4", "", -1, 1, 0, 1000000000, 0, "Fourth value; 0 = not used", blank=1),
    # amp check
    C(19, "Nameplate V", 13, 2, "Voltage on the unit's data plate"),
    S(20, "Measured V", "V", 1, 1, 0, 1000, 238, "Volts at the unit while it runs"),
    S(21, "Rated amps", "A", 1, 0.1, 0.1, 5000, 14.1, "RLA (compressor) or FLA (motor) from plate"),
    S(22, "Clamp reads", "A", 2, 0.1, 0, 10000, 11.2, "Amp clamp reading while running"),
    S(23, "Wraps", "", 0, 1, 1, 20, 1, "Turns of the wire through the clamp jaw"),
    # 3-phase balance
    S(24, "L1-L2", "V", 1, 1, 0, 1000, 230, "Volts between L1 and L2"),
    S(25, "L2-L3", "V", 1, 1, 0, 1000, 227, "Volts between L2 and L3"),
    S(26, "L1-L3", "V", 1, 1, 0, 1000, 223, "Volts between L1 and L3"),
    S(27, "L1 amps", "A", 2, 0.1, 0, 10000, 10.6, "Amps on L1"),
    S(28, "L2 amps", "A", 2, 0.1, 0, 10000, 10.1, "Amps on L2"),
    S(29, "L3 amps", "A", 2, 0.1, 0, 10000, 9.8, "Amps on L3"),
    # capacitor
    S(30, "Rated µF", "µF", 1, 0.5, 0.5, 5000, 45, "Microfarads printed on the capacitor"),
    C(31, "Tolerance", 8, 2, "Tolerance printed on the capacitor"),
    S(32, "Meter µF", "µF", 1, 0.5, 0, 5000, 0, "Capacitance meter reading; 0 = use A and V", blank=1),
    C(33, "Frequency", 7, 1, "Line frequency"),
    S(34, "Cap amps", "A", 2, 0.1, 0, 100, 6.4, "Amps through the capacitor while running", blank=1),
    S(35, "Cap volts", "V", 1, 1, 0, 1000, 375, "Volts across the capacitor while running", blank=1),
    # winding check
    C(36, "Motor", 1, 1, "Single-phase (C, S, R) or three-phase"),
    S(37, "T1-T2", "Ω", 2, 0.1, 0, 100000, 2.1, "Ohms between terminals 1 and 2 (OL: 99999)"),
    S(38, "T2-T3", "Ω", 2, 0.1, 0, 100000, 4.2, "Ohms between terminals 2 and 3 (OL: 99999)"),
    S(39, "T1-T3", "Ω", 2, 0.1, 0, 100000, 6.2, "Ohms between terminals 1 and 3 (OL: 99999)"),
    S(40, "Winding temp", "°F", 0, 1, -40, 300, 77, "Winding (shell) temperature"),
    # megohm test
    S(41, "1-min MΩ", "MΩ", -1, 10, 0, 1000000, 850, "Megohmmeter reading after 1 minute"),
    S(42, "Winding temp", "°F", 0, 1, -40, 300, 68, "Winding temperature during the test"),
    S(43, "10-min MΩ", "MΩ", -1, 10, 0, 1000000, 0, "Reading after 10 minutes (0 = skip PI)", blank=1),
    S(44, "30-sec MΩ", "MΩ", -1, 10, 0, 1000000, 0, "Reading after 30 seconds (0 = skip DAR)", blank=1),
    # motor NEC sizing
    C(45, "Horsepower", 9, 10, "Motor horsepower"),
    C(46, "Phase", 1, 2, "Single phase or three phase"),
    C(47, "Rated volts", 10, 3, "Motor voltage rating"),
    S(48, "Plate FLA", "A", 1, 0.1, 0, 5000, 16.2, "Full-load amps on the motor nameplate"),
    C(49, "Serv. factor", 11, 2, "Service factor on the nameplate"),
    # motor LRA and RPM
    C(50, "Code letter", 12, 8, "Locked-rotor code letter on the nameplate"),
    S(51, "Horsepower", "HP", 2, 0.25, 0.01, 2000, 5, "Motor horsepower"),
    S(52, "Rated volts", "V", 0, 1, 1, 15000, 208, "Motor voltage"),
    C(53, "Phase", 1, 2, "Single phase or three phase"),
    S(54, "Plate RPM", "RPM", 0, 5, 100, 3600, 1740, "Full-load speed on the nameplate"),
    C(55, "Frequency", 7, 1, "Line frequency"),
    # unit MCA / MOCP
    S(56, "Largest RLA", "A", 1, 0.1, 0, 5000, 14.1, "RLA of the compressor (largest motor)"),
    S(57, "Other motors", "A", 1, 0.1, 0, 5000, 1.2, "All other motor FLAs added (fans, blower)"),
    S(58, "Heat / other", "A", 1, 0.1, 0, 5000, 0, "Electric heat and other loads, amps"),
    # voltage drop
    S(59, "Load amps", "A", 1, 0.1, 0, 5000, 18.8, "Amps the circuit carries"),
    S(60, "One-way ft", "ft", 0, 5, 1, 20000, 75, "Length from the panel to the load, one way"),
    C(61, "Wire size", 3, 5, "Conductor size"),
    C(62, "Material", 2, 1, "Copper or aluminum conductors"),
    C(63, "Phase", 1, 1, "Single phase (or DC / 24 V) or three phase"),
    S(64, "Source V", "V", 1, 1, 1, 100000, 240, "Volts at the panel"),
    S(65, "Max drop", "%", 1, 0.5, 0.5, 20, 3, "NEC note: 3% branch, 5% feeder + branch"),
    # wire ampacity
    C(66, "Wire size", 3, 5, "Conductor size"),
    C(67, "Material", 2, 1, "Copper or aluminum conductors"),
    C(68, "Insulation", 4, 3, "Wire rating: THHN 90°C, THWN 75°C, NM 60°C"),
    C(69, "Terminals", 5, 2, "Lug rating; most HVAC equipment is 75°C"),
    S(70, "Ambient", "°F", 0, 1, -40, 200, 86, "Air temperature around the wires"),
    S(71, "Conductors", "", 0, 1, 1, 100, 3, "Current-carrying wires in the raceway"),
    C(72, "On roof", 6, 1, "Raceway in sun under 7/8 in above roof?"),
    # transformer
    S(73, "VA rating", "VA", 0, 5, 1, 10000000, 40, "Transformer rating in VA (kVA x 1000)"),
    C(74, "Phase", 1, 1, "Single phase or three phase"),
    S(75, "Primary V", "V", 0, 1, 1, 100000, 240, "Primary (line side) volts"),
    S(76, "Secondary V", "V", 0, 1, 1, 100000, 24, "Secondary (load side) volts"),
    S(77, "Load amps", "A", 2, 0.1, 0, 100000, 1.2, "Measured secondary amps (0 = skip)", blank=1),
    # electric heat
    S(78, "Rated kW", "kW", 1, 0.5, 0.1, 10000, 10, "Heater kW from the data plate"),
    S(79, "Rated volts", "V", 0, 1, 100, 1000, 240, "Voltage the kW rating is given at"),
    S(80, "Applied V", "V", 1, 1, 1, 1000, 208, "Measured volts at the heater"),
    C(81, "Phase", 1, 1, "Single phase or three phase"),
    S(82, "Measured A", "A", 1, 0.1, 0, 10000, 36.1, "Clamp reading, all strips on (0 = skip)", blank=1),
    S(83, "Temp rise", "°F", 1, 1, 0, 200, 25, "Supply minus return air temp (0 = skip)", blank=1),
    # thermistor
    C(84, "Sensor", 16, 1, "Thermistor curve; check the unit's chart"),
    S(85, "Reading", "kΩ", -1, 0.1, 0.001, 100000, 15.7, "Sensor kΩ, unplugged from the board"),
    S(86, "Actual temp", "°F", 1, 1, -60, 300, 59, "Temperature at the sensor (thermometer)"),
    S(87, "R at 77°F", "kΩ", -1, 0.5, 0.1, 10000, 10, "Custom curve: kΩ at 77°F (25°C)"),
    S(88, "Beta", "K", 0, 25, 1000, 10000, 3950, "Custom curve: Beta value from data sheet"),
    # energy cost (also uses 5-8)
    S(89, "Rate", "$/kWh", 3, 0.01, 0, 10, 0.15, "Electric rate with fees, $ per kWh"),
    S(90, "Hours/day", "h", 1, 0.5, 0, 24, 8, "Run time per day"),
    S(91, "Capacity", "BTU/h", 0, 500, 0, 100000000, 0, "Cooling output for EER (0 = skip)", blank=1),
    # unit converter
    C(92, "Convert", 17, 1, "What kind of value to convert"),
    S(93, "Value", "", -1, 1, -1000000000, 1000000000, 12000, "Number to convert"),
    C(94, "From", UNITS, 4, "Unit of that number"),
    # wye / delta
    C(95, "Hookup", 19, 1, "Wye (star) or delta transformer / motor"),
    S(96, "Line volts", "V", 1, 1, 1, 100000, 208, "Line-to-line volts"),
    S(97, "Line amps", "A", 2, 0.1, 0, 100000, 20, "Amps in each line"),
]

# tools in tile order: full name, tile lines, colour group, input boxes
# (laid out two per row, left then right)
TOOLS = [
    ("Ohm's law", "Ohm's", "law", 1, [1, 2, 3, 4]),
    ("Power: watts, VA, PF", "Power", "W  VA  PF", 1, [5, 6, 7, 8, 9]),
    ("Load amps", "Load", "amps", 1, [10, 11, 5, 7, 8, 9]),
    ("Series / parallel", "Series /", "parallel", 1, [12, 13, 14, 15, 16, 17, 18]),
    ("Amp check vs nameplate", "Amp", "check", 2, [19, 20, 21, 22, 23]),
    ("3-phase balance", "3-phase", "balance", 2, [24, 27, 25, 28, 26, 29]),
    ("Capacitor test", "Capacitor", "test", 2, [30, 31, 32, 33, 34, 35]),
    ("Winding check", "Winding", "check", 2, [36, 40, 37, 38, 39]),
    ("Megohm insulation test", "Megohm", "test", 2, [41, 42, 43, 44]),
    ("Motor NEC sizing", "Motor", "NEC size", 2, [45, 46, 47, 48, 49]),
    ("Motor LRA and RPM", "Motor", "LRA  RPM", 2, [50, 51, 52, 53, 54, 55]),
    ("Unit MCA / MOCP", "MCA /", "MOCP", 3, [56, 57, 58]),
    ("Voltage drop", "Voltage", "drop", 3, [59, 60, 61, 62, 63, 64, 65]),
    ("Wire ampacity", "Wire", "ampacity", 3, [66, 67, 68, 69, 70, 71, 72]),
    ("Transformer", "Trans-", "former", 3, [73, 74, 75, 76, 77]),
    ("Wye / delta", "Wye /", "delta", 3, [95, 96, 97]),
    ("Electric heat", "Electric", "heat", 4, [78, 79, 80, 81, 82, 83]),
    ("Thermistor check", "Thermistor", "check", 4, [84, 85, 86, 87, 88]),
    ("Energy cost", "Energy", "cost", 5, [5, 6, 7, 8, 89, 90, 91]),
    ("Unit converter", "Unit", "convert", 5, [92, 94, 93]),
]

# ---------------------------------------------------------------------------
# NEC tables

# motor horsepower rows, as in choice list 9
HP_ROWS = ["1/6", "1/4", "1/3", "1/2", "3/4", "1", "1-1/2", "2", "3", "5", "7-1/2",
           "10", "15", "20", "25", "30", "40", "50", "60", "75", "100", "125", "150", "200"]
VOLT_COLS = [115, 200, 208, 230, 460, 575]

# NEC Table 430.248, single phase: HP -> amps at 115, 200, 208, 230 V
FLC_1PH = {
    "1/6": (4.4, 2.5, 2.4, 2.2), "1/4": (5.8, 3.3, 3.2, 2.9), "1/3": (7.2, 4.1, 4.0, 3.6),
    "1/2": (9.8, 5.6, 5.4, 4.9), "3/4": (13.8, 7.9, 7.6, 6.9), "1": (16, 9.2, 8.8, 8.0),
    "1-1/2": (20, 11.5, 11, 10), "2": (24, 13.8, 13.2, 12), "3": (34, 19.6, 18.7, 17),
    "5": (56, 32.2, 30.8, 28), "7-1/2": (80, 46, 44, 40), "10": (100, 57.5, 55, 50),
}
# NEC Table 430.250, three phase (induction type): HP -> amps at
# 115, 200, 208, 230, 460, 575 V (0 = no table value)
FLC_3PH = {
    "1/2": (4.4, 2.5, 2.4, 2.2, 1.1, 0.9), "3/4": (6.4, 3.7, 3.5, 3.2, 1.6, 1.3),
    "1": (8.4, 4.8, 4.6, 4.2, 2.1, 1.7), "1-1/2": (12.0, 6.9, 6.6, 6.0, 3.0, 2.4),
    "2": (13.6, 7.8, 7.5, 6.8, 3.4, 2.7), "3": (0, 11.0, 10.6, 9.6, 4.8, 3.9),
    "5": (0, 17.5, 16.7, 15.2, 7.6, 6.1), "7-1/2": (0, 25.3, 24.2, 22, 11, 9),
    "10": (0, 32.2, 30.8, 28, 14, 11), "15": (0, 48.3, 46.2, 42, 21, 17),
    "20": (0, 62.1, 59.4, 54, 27, 22), "25": (0, 78.2, 74.8, 68, 34, 27),
    "30": (0, 92, 88, 80, 40, 32), "40": (0, 120, 114, 104, 52, 41),
    "50": (0, 150, 143, 130, 65, 52), "60": (0, 177, 169, 154, 77, 62),
    "75": (0, 221, 211, 192, 96, 77), "100": (0, 285, 273, 248, 124, 99),
    "125": (0, 359, 343, 312, 156, 125), "150": (0, 414, 396, 360, 180, 144),
    "200": (0, 552, 528, 480, 240, 192),
}

# wire sizes, as in choice list 3, with Chapter 9 Table 8 circular mils
WIRES = ["18", "16", "14", "12", "10", "8", "6", "4", "3", "2", "1", "1/0", "2/0",
         "3/0", "4/0", "250", "300", "350", "400", "500"]
CMIL = [1620, 2580, 4110, 6530, 10380, 16510, 26240, 41740, 52620, 66360, 83690,
        105600, 133100, 167800, 211600, 250000, 300000, 350000, 400000, 500000]
# NEC Table 310.16 (0 = not listed)
AMPACITY = {
    ("Cu", 60): [0, 0, 15, 20, 30, 40, 55, 70, 85, 95, 110, 125, 145, 165, 195, 215, 240, 260, 280, 320],
    ("Cu", 75): [0, 0, 20, 25, 35, 50, 65, 85, 100, 115, 130, 150, 175, 200, 230, 255, 285, 310, 335, 380],
    ("Cu", 90): [14, 18, 25, 30, 40, 55, 75, 95, 115, 130, 145, 170, 195, 225, 260, 290, 320, 350, 380, 430],
    ("Al", 60): [0, 0, 0, 15, 25, 35, 40, 55, 65, 75, 85, 100, 115, 130, 150, 170, 195, 210, 225, 260],
    ("Al", 75): [0, 0, 0, 20, 30, 40, 50, 65, 75, 90, 100, 120, 135, 155, 180, 205, 230, 250, 270, 310],
    ("Al", 90): [0, 0, 0, 25, 35, 45, 55, 75, 85, 100, 115, 135, 150, 175, 205, 230, 260, 280, 305, 350],
}
# NEC 240.6(A) standard ampere ratings
STD_SIZES = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175,
             200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1600,
             2000, 2500, 3000, 4000, 5000, 6000]
# NEC Table 430.7(B): lowest kVA/HP of each code letter (A starts at 0;
# each letter ends 0.01 below the next one; V is 22.4 and up)
CODE_LO = [0, 3.15, 3.55, 4.0, 4.5, 5.0, 5.6, 6.3, 7.1, 8.0, 9.0, 10.0, 11.2, 12.5,
           14.0, 16.0, 18.0, 20.0, 22.4]

# Steinhart-Hart coefficients 1/T = A + B ln R + C (ln R)^3, T in K, R in ohms
THERMISTORS = [
    ("10K Type II", 1.129241e-3, 2.341077e-4, 8.775468e-8),
    ("10K Type III", 1.028444e-3, 2.392435e-4, 1.562216e-7),
]


# ---------------------------------------------------------------------------
# output

def check():
    check_slots(SLOTS, TOOLS)
    assert set(FLC_1PH) <= set(HP_ROWS) and set(FLC_3PH) <= set(HP_ROWS)
    assert len(CHOICES[9]) == len(HP_ROWS) and len(CHOICES[3]) == len(WIRES) == len(CMIL)
    assert all(len(v) == len(WIRES) for v in AMPACITY.values())
    assert len(CHOICES[12]) == len(CODE_LO)
    for col in AMPACITY.values():
        nz = [a for a in col if a]
        assert nz == sorted(nz)
    # the Type III coefficients reproduce BAPI's published table
    with open(os.path.join(DATA, "thermistor_10k3_bapi.csv")) as fh:
        rows = list(csv.DictReader(l for l in fh if not l.startswith("#")))
    _, a, b, c = THERMISTORS[1]
    worst = 0
    for r in rows:
        x = math.log(float(r["ohms"]))
        tf = (1 / (a + b * x + c * x ** 3) - 273.15) * 1.8 + 32
        worst = max(worst, abs(tf - float(r["temp_F"])))
    assert worst < 0.05, worst


def build_block():
    flc1, flc3 = [], []
    for hp in HP_ROWS:
        flc1.append(list(FLC_1PH.get(hp, ())) + [0] * (6 - len(FLC_1PH.get(hp, ()))))
        flc3.append(list(FLC_3PH.get(hp, (0,) * 6)))
    amp = [AMPACITY[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]
    out = ["// ---- BEGIN TABLES (generated by tools/gen_elec_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// NEC 430.248 (1-phase) and 430.250 (3-phase) motor full-load amps:",
        "// rows = horsepower list, columns 115 200 208 230 460 575 V, 0 = none",
        "gFlc1:=" + pmatrix(flc1) + ";",
        "gFlc3:=" + pmatrix(flc3) + ";",
        "// wire sizes, circular mils (Ch. 9 Table 8) and NEC 310.16 ampacity:",
        "// rows Cu 60/75/90 C then Al 60/75/90 C, 0 = not listed",
        "gWire:=" + plist(WIRES) + ";",
        "gCM:=" + plist(CMIL) + ";",
        "gAmp:=" + pmatrix(amp) + ";",
        "// NEC 240.6(A) standard fuse and breaker ratings",
        "gStd:=" + plist(STD_SIZES) + ";",
        "// NEC 430.7(B) code letters: lowest kVA per HP of each letter",
        "gCodeLo:=" + plist(CODE_LO) + ";",
        "// thermistor Steinhart-Hart coefficients: " + ", ".join(t[0] for t in THERMISTORS),
        "gShA:=" + plist([t[1] for t in THERMISTORS]) + ";",
        "gShB:=" + plist([t[2] for t in THERMISTORS]) + ";",
        "gShC:=" + plist([t[3] for t in THERMISTORS]) + ";",
        "",
    ]
    out += slot_functions(TOOLS, CHOICES, UNITS, 92)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
