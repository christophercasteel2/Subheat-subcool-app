#!/usr/bin/env python3
"""Write the generated block of hp-prime/NECCALC.txt: the tool list, the
input-box ("slot") tables and the NEC tables of the class calculator.

Edit the tables here, not in the program, then run
    python3 tools/gen_nec_tables.py

Arkansas: the Board of Electrical Examiners adopted the 2026 NEC with
amendments, effective September 3, 2026 (17 CAR 210-401).  Section numbers
below follow the 2026 NEC (load calculations moved from Article 220 to
Article 120).  The table values are unchanged from the 2017 edition, except
that the 2026 Table 310.16 adds 60/75 C values for 16 AWG copper and a
14 AWG copper-clad aluminum row; those are not in this program (16 AWG
copper shows only its 90 C value), so check the code book for them.

NEC tables
  310.16  ampacity, raceway / cable / earth, 18 AWG - 2000 kcmil
  310.17  ampacity, single conductors in free air
          both copied from Omnicable's reproduction of the 2017 tables
  310.15(B)(1) ambient correction factors: the code's equation at the top
          of each 5 C band, rounded to 2 places (this reproduces the table)
  310.15(C)(1) adjustment for more than 3 current-carrying conductors
  Chapter 9 Table 1 (fill %), Table 4 (raceway area), Table 5 (conductor
          area), Table 8 (circular mils, dc resistance at 75 C)
  240.6(A) standard ratings, 240.4(D) small conductors
  314.16(A) box volumes, 314.16(B) volume per conductor
  250.122 equipment grounding conductors, 250.66 grounding electrode
          conductors, 310.12 (83% dwelling services and feeders)
  The appliance guide, NEMA list and state electric rates follow
  electricalcalctools.com, with wire sizes checked against 310.16.
"""
import math
import os

from ppltables import (check_slots, choice_slot, plist, pmatrix, slot, slot_functions,
                       slot_globals, write_block)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "hp-prime", "NECCALC.txt")

# ---------------------------------------------------------------------------
# conductor sizes (choice list 10) and their tables

SIZES = ["18", "16", "14", "12", "10", "8", "6", "4", "3", "2", "1", "1/0", "2/0",
         "3/0", "4/0", "250", "300", "350", "400", "500", "600", "700", "750", "800",
         "900", "1000", "1250", "1500", "1750", "2000"]
CMIL = [1620, 2580, 4110, 6530, 10380, 16510, 26240, 41740, 52620, 66360, 83690,
        105600, 133100, 167800, 211600] + [int(s) * 1000 for s in SIZES[15:]]

# Table 310.16 (raceway, cable or earth), Table 310.17 (free air): 0 = not listed
T16 = {
    ("Cu", 60): [0, 0, 15, 20, 30, 40, 55, 70, 85, 95, 110, 125, 145, 165, 195, 215, 240, 260, 280, 320, 350, 385, 400, 410, 435, 455, 495, 525, 545, 555],
    ("Cu", 75): [0, 0, 20, 25, 35, 50, 65, 85, 100, 115, 130, 150, 175, 200, 230, 255, 285, 310, 335, 380, 420, 460, 475, 490, 520, 545, 590, 625, 650, 665],
    ("Cu", 90): [14, 18, 25, 30, 40, 55, 75, 95, 115, 130, 145, 170, 195, 225, 260, 290, 320, 350, 380, 430, 475, 520, 535, 555, 585, 615, 665, 705, 735, 750],
    ("Al", 60): [0, 0, 0, 15, 25, 35, 40, 55, 65, 75, 85, 100, 115, 130, 150, 170, 195, 210, 225, 260, 285, 315, 320, 330, 355, 375, 405, 435, 455, 470],
    ("Al", 75): [0, 0, 0, 20, 30, 40, 50, 65, 75, 90, 100, 120, 135, 155, 180, 205, 230, 250, 270, 310, 340, 375, 385, 395, 425, 445, 485, 520, 545, 560],
    ("Al", 90): [0, 0, 0, 25, 35, 45, 55, 75, 85, 100, 115, 135, 150, 175, 205, 230, 260, 280, 305, 350, 385, 425, 435, 445, 480, 500, 545, 585, 615, 630],
}
T17 = {
    ("Cu", 60): [0, 0, 25, 30, 40, 60, 80, 105, 120, 140, 165, 195, 225, 260, 300, 340, 375, 420, 455, 515, 575, 630, 655, 680, 730, 780, 890, 980, 1070, 1155],
    ("Cu", 75): [0, 0, 30, 35, 50, 70, 95, 125, 145, 170, 195, 230, 265, 310, 360, 405, 445, 505, 545, 620, 690, 755, 785, 815, 870, 935, 1065, 1175, 1280, 1385],
    ("Cu", 90): [18, 24, 35, 40, 55, 80, 105, 140, 165, 190, 220, 260, 300, 350, 405, 455, 500, 570, 615, 700, 780, 850, 885, 920, 980, 1055, 1200, 1325, 1445, 1560],
    ("Al", 60): [0, 0, 0, 25, 35, 45, 60, 80, 95, 110, 130, 150, 175, 200, 235, 265, 290, 330, 355, 405, 455, 500, 515, 535, 580, 625, 710, 795, 875, 960],
    ("Al", 75): [0, 0, 0, 30, 40, 55, 75, 100, 115, 135, 155, 180, 210, 240, 280, 315, 350, 395, 425, 485, 545, 595, 620, 645, 700, 750, 855, 950, 1050, 1150],
    ("Al", 90): [0, 0, 0, 35, 45, 60, 85, 115, 130, 150, 175, 205, 235, 270, 315, 355, 395, 445, 480, 545, 615, 670, 700, 725, 790, 845, 965, 1070, 1185, 1295],
}
# Chapter 9 Table 8, dc resistance at 75 C, ohms per 1000 ft (stranded;
# 0 = not used here)
R8 = {
    "Cu": [8.08, 5.08, 3.14, 1.98, 1.24, 0.778, 0.491, 0.308, 0.245, 0.194, 0.154, 0.122,
           0.0967, 0.0766, 0.0608, 0.0515, 0.0429, 0.0367, 0.0321, 0.0258, 0.0214, 0.0184,
           0.0171, 0.0161, 0.0143, 0.0129, 0.0103, 0.00858, 0.00735, 0.00643],
    "Al": [0, 0, 0, 3.25, 2.04, 1.28, 0.808, 0.508, 0.403, 0.319, 0.253, 0.201, 0.159,
           0.126, 0.100, 0.0847, 0.0707, 0.0605, 0.0529, 0.0424, 0.0353, 0.0303, 0.0282,
           0.0265, 0.0235, 0.0212, 0.0169, 0.0141, 0.0121, 0.0106],
}

# insulation types (choice list 11): label, temperature column 1 60 C,
# 2 75 C, 3 90 C, 4 = NM cable (90 C wire, 60 C ampacity, 334.80);
# Table 5 group for conduit fill (0 = not in the fill tables here)
INSULATION = [
    ("TW", 1, 3), ("UF", 1, 0), ("RHW", 2, 4), ("THHW wet", 2, 3), ("THW", 2, 3),
    ("THWN", 2, 1), ("XHHW wet", 2, 2), ("USE", 2, 0), ("ZW", 2, 0), ("TBS", 3, 0),
    ("SA", 3, 0), ("SIS", 3, 0), ("FEP", 3, 5), ("FEPB", 3, 5), ("MI", 3, 0),
    ("RHH", 3, 4), ("RHW-2", 3, 4), ("THHN", 3, 1), ("THHW dry", 3, 3), ("THW-2", 3, 3),
    ("THWN-2", 3, 1), ("USE-2", 3, 2), ("XHH", 3, 2), ("XHHW dry", 3, 2), ("XHHW-2", 3, 2),
    ("ZW-2", 3, 0), ("NM-B cable", 4, 0),
]

# Table 310.15(B)(1): top of each ambient band, C
AMB_TOP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]


def corr_factor(top, tc):
    if top >= tc:
        return 0
    # the code's equation, rounded as the table prints it
    f = math.sqrt((tc - top) / (tc - 30))
    return round(f + 1e-9, 2)


CORR = [[corr_factor(t, tc) for t in AMB_TOP] for tc in (60, 75, 90)]
# spot values as printed in the table, typed separately
CORR_CHECK = {(60, 40): 0.82, (75, 40): 0.88, (90, 40): 0.91, (75, 45): 0.82,
              (90, 50): 0.82, (60, 55): 0.41, (75, 70): 0.33, (90, 85): 0.29,
              (60, 10): 1.29, (75, 20): 1.11, (90, 35): 0.96}

# conduit fill: Table 5 sizes 14 AWG - 500 kcmil (choice list 16)
FILL_SIZES = SIZES[2:20]
FILL_AREA = [  # in2; 0 = not listed for that group here
    [0.0097, 0.0133, 0.0211, 0.0366, 0.0507, 0.0824, 0.0973, 0.1158, 0.1562, 0.1855,
     0.2223, 0.2679, 0.3237, 0.3970, 0.4608, 0.5242, 0.5863, 0.7073],     # THHN, THWN, THWN-2
    [0.0139, 0.0181, 0.0243, 0.0437, 0.0590, 0.0814, 0.0962, 0.1146, 0.1534, 0.1825,
     0.2190, 0.2642, 0.3197, 0.3904, 0.4536, 0.5166, 0.5782, 0.6984],     # XHHW, XHHW-2, XHH, USE-2
    [0.0139, 0.0181, 0.0243, 0.0437, 0.0726, 0.0973, 0.1134, 0.1333, 0.1901, 0.2223,
     0.2624, 0.3117, 0.3718, 0.4596, 0.5281, 0.5958, 0.6619, 0.7901],     # TW, THW, THHW, THW-2
    [0.0209, 0.0260, 0.0333, 0.0556, 0.0726, 0.0973, 0.1134, 0.1333, 0.1901, 0.2223,
     0.2624, 0.3117, 0.3718, 0.4596, 0.5281, 0.5958, 0.6619, 0.7901],     # RHH, RHW, RHW-2 no jacket
    [0.0100, 0.0137, 0.0191, 0.0333, 0.0468, 0.0670, 0.0804, 0.0973, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0],                                             # FEP, FEPB
]
# Table 4: total (100 %) area, in2, trade sizes of choice list 14; 0 = none
TRADE = ["3/8", "1/2", "3/4", "1", "1-1/4", "1-1/2", "2", "2-1/2", "3", "3-1/2", "4", "5", "6"]
CONDUIT = [
    [0, 0.304, 0.533, 0.864, 1.496, 2.036, 3.356, 5.858, 8.846, 11.545, 14.753, 0, 0],      # EMT
    [0.116, 0.317, 0.533, 0.817, 1.277, 1.858, 3.269, 4.909, 7.069, 9.621, 12.566, 0, 0],  # FMC
    [0, 0.342, 0.586, 0.959, 1.647, 2.225, 3.630, 5.135, 7.922, 10.584, 13.631, 0, 0],     # IMC
    [0, 0.314, 0.549, 0.887, 1.526, 2.071, 3.408, 4.866, 7.499, 10.010, 12.882, 20.212, 29.158],  # RMC
    [0, 0.285, 0.508, 0.832, 1.453, 1.986, 3.291, 4.695, 7.268, 9.737, 12.554, 19.761, 28.567],   # PVC 40
    [0, 0.217, 0.409, 0.688, 1.237, 1.711, 2.874, 4.119, 6.442, 8.688, 11.258, 17.855, 25.598],   # PVC 80
]
STD_SIZES = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175,
             200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1600,
             2000, 2500, 3000, 4000, 5000, 6000]
BOX_SIZES = ["18 AWG", "16 AWG", "14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG"]
BOX_VOL = [1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 5.0]       # Table 314.16(B), in3
# Table 314.16(A) metal boxes: name, volume in3
BOXES = [("Custom volume", 0), ("4x1-1/4 rnd/oct", 12.5), ("4x1-1/2 rnd/oct", 15.5),
         ("4x2-1/8 rnd/oct", 21.5), ("4x1-1/4 square", 18.0), ("4x1-1/2 square", 21.0),
         ("4x2-1/8 square", 30.3), ("4-11/16x1-1/4 sq", 25.5), ("4-11/16x1-1/2 sq", 29.5),
         ("4-11/16x2-1/8 sq", 42.0), ("3x2x1-1/2 device", 7.5), ("3x2x2 device", 10.0),
         ("3x2x2-1/4 device", 10.5), ("3x2x2-1/2 device", 12.5), ("3x2x2-3/4 device", 14.0),
         ("3x2x3-1/2 device", 18.0), ("4x2-1/8x1-1/2 dev", 10.3), ("4x2-1/8x1-7/8 dev", 13.0),
         ("4x2-1/8x2-1/8 dev", 14.5), ("3-3/4x2x2-1/2 mas", 14.0), ("3-3/4x2x3-1/2 mas", 21.0)]

# systems: label, volts, phase (1 or 3)
SYSTEMS = [("120V 1-ph", 120, 1), ("208V 1-ph", 208, 1), ("240V 1-ph", 240, 1),
           ("277V 1-ph", 277, 1), ("208V 3-ph", 208, 3), ("240V 3-ph", 240, 3),
           ("480V 3-ph", 480, 3), ("600V 3-ph", 600, 3)]

# Table 250.122 equipment grounding conductors: OCPD up to, Cu size, Al size
EGC = [(15, "14", "12"), (20, "12", "10"), (60, "10", "8"), (100, "8", "6"), (200, "6", "4"),
       (300, "4", "2"), (400, "3", "1"), (500, "2", "1/0"), (600, "1", "2/0"),
       (800, "1/0", "3/0"), (1000, "2/0", "4/0"), (1200, "3/0", "250"), (1600, "4/0", "350"),
       (2000, "250", "400"), (2500, "350", "600"), (3000, "400", "600"),
       (4000, "500", "750")]
# Table 250.66 grounding electrode conductor: largest service conductor up to
# (circular mils for Cu, for Al) -> GEC Cu, Al
GEC = [(66360, 105600, "8", "6"), (105600, 167800, "6", "4"), (167800, 250000, "4", "2"),
       (350000, 500000, "2", "1/0"), (600000, 900000, "1/0", "3/0"),
       (1100000, 1750000, "2/0", "4/0"), (10 ** 9, 10 ** 9, "3/0", "250")]

# average residential rates used by the site's cost calculator, $/kWh
STATE_RATES = [("Alabama", 0.136), ("Alaska", 0.237), ("Arizona", 0.130), ("Arkansas", 0.111),
    ("California", 0.259), ("Colorado", 0.137), ("Connecticut", 0.246), ("Delaware", 0.134),
    ("Florida", 0.129), ("Georgia", 0.130), ("Hawaii", 0.390), ("Idaho", 0.102),
    ("Illinois", 0.135), ("Indiana", 0.143), ("Iowa", 0.116), ("Kansas", 0.137),
    ("Kentucky", 0.116), ("Louisiana", 0.108), ("Maine", 0.214), ("Maryland", 0.152),
    ("Massachusetts", 0.252), ("Michigan", 0.176), ("Minnesota", 0.144), ("Mississippi", 0.119),
    ("Missouri", 0.115), ("Montana", 0.108), ("Nebraska", 0.110), ("Nevada", 0.116),
    ("New Hampshire", 0.228), ("New Jersey", 0.175), ("New Mexico", 0.133), ("New York", 0.210),
    ("North Carolina", 0.121), ("North Dakota", 0.102), ("Ohio", 0.133), ("Oklahoma", 0.107),
    ("Oregon", 0.117), ("Pennsylvania", 0.153), ("Rhode Island", 0.248),
    ("South Carolina", 0.135), ("South Dakota", 0.115), ("Tennessee", 0.122), ("Texas", 0.132),
    ("Utah", 0.108), ("Vermont", 0.213), ("Virginia", 0.132), ("Washington", 0.106),
    ("West Virginia", 0.131), ("Wisconsin", 0.149), ("Wyoming", 0.094), ("Washington DC", 0.152)]

# NEMA configurations: name, volts, amps, wires, typical use
NEMA = [("1-15", "125 V", 15, "hot + neutral, no ground", "old 2-prong outlets"),
        ("5-15", "125 V", 15, "hot, neutral, ground", "standard household outlet"),
        ("5-20", "125 V", 20, "hot, neutral, ground", "kitchen, garage (T slot)"),
        ("5-30", "125 V", 30, "hot, neutral, ground", "RV, heavy 120 V tools"),
        ("5-50", "125 V", 50, "hot, neutral, ground", "large 120 V equipment"),
        ("6-15", "250 V", 15, "2 hots, ground", "small 240 V tools, A/C"),
        ("6-20", "250 V", 20, "2 hots, ground", "window A/C, shop tools"),
        ("6-30", "250 V", 30, "2 hots, ground", "welders, compressors"),
        ("6-50", "250 V", 50, "2 hots, ground", "welders, EV chargers"),
        ("10-30", "125/250 V", 30, "2 hots, neutral, NO ground", "old dryers (existing only)"),
        ("10-50", "125/250 V", 50, "2 hots, neutral, NO ground", "old ranges (existing only)"),
        ("14-20", "125/250 V", 20, "2 hots, neutral, ground", "small 120/240 V loads"),
        ("14-30", "125/250 V", 30, "2 hots, neutral, ground", "electric dryers"),
        ("14-50", "125/250 V", 50, "2 hots, neutral, ground", "ranges, EV chargers, RVs"),
        ("14-60", "125/250 V", 60, "2 hots, neutral, ground", "large ranges, EVSE"),
        ("15-50", "250 V 3-ph", 50, "3 hots, ground", "3-phase equipment"),
        ("L5-20", "125 V", 20, "hot, neutral, ground", "locking 120 V equipment"),
        ("L5-30", "125 V", 30, "hot, neutral, ground", "locking: RV, marine"),
        ("L6-20", "250 V", 20, "2 hots, ground", "locking 240 V equipment"),
        ("L6-30", "250 V", 30, "2 hots, ground", "locking: compressors, UPS"),
        ("L14-20", "125/250 V", 20, "2 hots, neutral, ground", "locking: small generators"),
        ("L14-30", "125/250 V", 30, "2 hots, neutral, ground", "generator inlets"),
        ("L15-30", "250 V 3-ph", 30, "3 hots, ground", "locking 3-phase equipment")]


def wire_for(amps, metal, brk, col=75, start=2):
    """smallest size from SIZES[start:] with a 310.16 ampacity of at least
    amps that breaker brk may protect (240.4(D) for small wire)"""
    small = {"Cu": {"14": 15, "12": 20, "10": 30}, "Al": {"12": 15, "10": 25}}[metal]
    t = T16[(metal, col)]
    for i in range(start, len(SIZES)):
        if t[i] and t[i] >= amps and small.get(SIZES[i], 10 ** 6) >= brk:
            return SIZES[i], t[i]
    return None, None


def awg(sz):
    if "/" in sz:
        return f"{sz} AWG"
    return f"#{sz} AWG" if sz in SIZES[:15] else f"{sz} kcmil"


def ev_row(evse):
    brk = next(s for s in STD_SIZES if s >= 1.25 * evse)
    cu, cua = wire_for(1.25 * evse, "Cu", brk)
    al, ala = wire_for(1.25 * evse, "Al", brk, start=3)
    return (f"EV charger {evse} A", f"240V, {evse} A continuous", f"{brk} A 2-pole (125%)",
            f"{awg(cu)} ({cua} A at 75°C)", f"{awg(al)} ({ala} A at 75°C)",
            "14-50 or hardwired" if brk <= 50 else "hardwired", "625.40, 625.42", "")


# appliance guides: name, circuit, breaker, copper, aluminum, outlet, NEC, note
APPLIANCES = [
    ("15A receptacles", "120V general outlets", "15 A 1-pole", "#14 AWG", "-", "5-15", "210.19, 240.4(D)", ""),
    ("20A receptacles", "120V kitchen, bath, garage", "20 A 1-pole", "#12 AWG", "#10 AWG Al", "5-20", "210.11(C), 210.52", ""),
    ("Electric dryer", "240V, 4-wire", "30 A 2-pole", "#10 AWG (35 A at 75°C)", "#8 AWG (40 A)", "14-30", "120.54, 250.140", "dryer load 5000 W min."),
    ("Range up to 12 kW", "120/240V, 4-wire", "50 A 2-pole", "#6 AWG (65 A)", "#4 AWG (65 A)", "14-50", "120.55, 210.19", "8.75 kW+: 40 A min."),
    ("Range under 8.75 kW", "120/240V, 4-wire", "40 A 2-pole", "#8 AWG (50 A)", "#6 AWG (50 A)", "14-50", "120.55", ""),
    ("Wall oven 5-7 kW", "240V", "30 A 2-pole", "#10 AWG", "#8 AWG", "hardwired", "422.10, nameplate", ""),
    ("Cooktop 7-9 kW", "240V", "40 A 2-pole", "#8 AWG", "#6 AWG", "hardwired", "422.10, nameplate", ""),
    ("Water heater 4500W", "240V, 18.75 A", "30 A 2-pole", "#10 AWG", "#8 AWG", "hardwired", "422.13 (125%)", "18.75 x 1.25 = 23.4 A"),
    ("Water heater 5500W", "240V, 22.9 A", "30 A 2-pole", "#10 AWG", "#8 AWG", "hardwired", "422.13 (125%)", "22.9 x 1.25 = 28.6 A"),
    ("Tankless 18 kW", "240V, 2 heating circuits", "2 x 40 A 2-pole", "2 runs of #8 AWG", "-", "hardwired", "422.13", ""),
    ("Tankless 27 kW", "240V, 3 heating circuits", "3 x 40 A 2-pole", "3 runs of #8 AWG", "-", "hardwired", "422.13", "check the service size"),
    ("Tankless 36 kW", "240V, 4 heating circuits", "4 x 40 A 2-pole", "4 runs of #8 AWG", "-", "hardwired", "422.13", "check the service size"),
    ("Hot tub 50 A", "120/240V, 4-wire", "50 A GFCI 2-pole", "#6 AWG (65 A)", "#4 AWG (65 A)", "spa disconnect", "Article 680", "GFCI still required in Arkansas"),
    ("Hot tub 60 A", "120/240V, 4-wire", "60 A GFCI 2-pole", "#6 AWG (65 A)", "#4 AWG (65 A)", "spa disconnect", "Article 680", "long runs: #4 Cu"),
    ev_row(16), ev_row(24), ev_row(32), ev_row(40), ev_row(48), ev_row(80),
    ("Mini-split 9-12k BTU", "115V or 230V", "15-20 A", "#14 or #12 AWG", "-", "disconnect", "440.22, 440.32", "use plate MCA / MOCP"),
    ("Mini-split 18-24k BTU", "230V", "20-25 A", "#12 or #10 AWG", "-", "disconnect", "440.22, 440.32", "use plate MCA / MOCP"),
    ("Mini-split 36k+ BTU", "230V multi-zone", "30-40 A", "#10 or #8 AWG", "-", "disconnect", "440.22, 440.32", "use plate MCA / MOCP"),
    ("Central A/C example", "MCA 19.7 A, MOCP 35 A", "30 or 35 A HACR", "#12 AWG (25 A)", "#10 AWG (30 A)", "disconnect", "440.22, 440.32", "never above MOCP"),
    ("Well pump 240V", "motor circuit", "20 A 2-pole (common)", "#14 AWG short runs", "-", "hardwired", "Article 430", "long runs: check VD"),
    ("Subpanel 60 A", "120/240V feeder", "60 A 2-pole", "#6 AWG (65 A)", "#4 AWG (65 A)", "4-wire feeder", "215.2, 250.32", "detached: ground rods"),
    ("Subpanel 100 A", "120/240V feeder", "100 A 2-pole", "#3 AWG (100 A)", "#1 AWG (100 A)", "4-wire feeder", "215.2, 250.32", "VD over ~75 ft"),
    ("Service 100 A dwelling", "120/240V, 310.12", "100 A main", "#4 AWG (83 A needed)", "#2 AWG (90 A)", "service", "310.12 (83%)", "dwelling only"),
    ("Service 200 A dwelling", "120/240V, 310.12", "200 A main", "2/0 AWG (166 A needed)", "4/0 AWG (180 A)", "service", "310.12 (83%)", "dwelling only"),
]

CHOICES = {
    1: ["°C", "°F"],
    2: ["Copper", "Aluminum"],
    3: ["1-phase", "3-phase"],
    4: ["K factor", "Table 8 R"],
    5: ["No", "Yes"],
    6: ["60°C", "75°C", "90°C"],
    7: [b[0] for b in BOXES],
    8: ["not given", "60°C", "75°C", "90°C"],
    9: ["Raceway/cable", "Free air"],
    10: [s + (" kcmil" if i >= 15 else " AWG") for i, s in enumerate(SIZES)],
    11: [t[0] for t in INSULATION],
    12: ["Wires that fit", "Conduit size"],
    13: ["EMT", "FMC", "IMC", "RMC", "PVC Sch 40", "PVC Sch 80"],
    14: [t + " in" for t in TRADE],
    15: ["THHN, THWN", "XHHW, XHH", "TW, THW", "RHW no jkt", "FEP, FEPB"],
    16: [s + (" kcmil" if i >= 13 else " AWG") for i, s in enumerate(FILL_SIZES)],
    17: BOX_SIZES,
    18: [x[0] for x in SYSTEMS],
    19: ["2%", "3%", "5%"],
    20: ["EGC 250.122", "GEC 250.66"],
    21: ["W", "kW"],
    22: ["Custom rate"] + [x[0] for x in STATE_RATES],
    23: [str(x) + " A" for x in STD_SIZES[:28]],
    24: [a[0] for a in APPLIANCES],
    25: ["NEMA " + n[0] for n in NEMA],
}

S = slot
C = choice_slot(CHOICES, None, 0)

SLOTS = [
    C(1, "Temp unit", 1, 1, "Unit for the ambient temperature"),
    # voltage drop
    S(2, "Amps", "A", 1, 1, 0, 100000, 20, "Load current"),
    S(3, "One-way ft", "ft", 0, 5, 1, 100000, 100, "Length from source to load, one way"),
    C(4, "Wire size", 10, 4, "Conductor size"),
    C(5, "Material", 2, 1, "Copper or aluminum"),
    C(6, "Phase", 3, 1, "Single phase (or DC) or three phase"),
    S(7, "Source V", "V", 1, 1, 1, 100000, 120, "Voltage at the source"),
    C(8, "Method", 4, 1, "K = 12.9 Cu / 21.2 Al, or Table 8 R"),
    S(9, "Max drop", "%", 1, 0.5, 0.5, 20, 3, "3% branch, 5% feeder + branch (note)"),
    # wire size
    S(10, "Load amps", "A", 1, 1, 0, 100000, 20, "Load current"),
    C(11, "Continuous", 5, 1, "3 hours or more: wire for 125%"),
    C(12, "Material", 2, 1, "Copper or aluminum"),
    C(13, "Wire rating", 6, 2, "Insulation temperature rating"),
    C(14, "Terminals", 6, 2, "Terminal rating (60°C if 100 A or less)"),
    S(15, "Ambient", "", 0, 1, -40, 200, 30, "Ambient (unit set in the Ampacity tool)"),
    S(16, "One-way ft", "ft", 0, 5, 0, 100000, 50, "Run length for voltage drop (0 = skip)", blank=1),
    C(17, "System", 18, 1, "Voltage and phase"),
    # ampacity
    C(18, "Wire size", 10, 8, "Conductor size"),
    C(19, "Material", 2, 1, "Copper or aluminum"),
    C(20, "Insulation", 11, 6, "Insulation type on the wire"),
    C(21, "Installed", 9, 1, "Raceway / cable / buried, or free air"),
    S(22, "Ambient", "", 0, 1, -40, 200, 30, "Ambient temperature"),
    S(23, "Conductors", "", 0, 1, 1, 100, 3, "Current-carrying conductors together"),
    C(24, "Terminals", 8, 1, "Terminal rating, if the question gives one"),
    # breaker size
    S(25, "Continuous", "A", 1, 1, 0, 100000, 16, "Continuous load, amps"),
    S(26, "Noncontin.", "A", 1, 1, 0, 100000, 0, "Noncontinuous load, amps"),
    C(27, "Wire size", 10, 4, "Conductor size"),
    C(28, "Material", 2, 1, "Copper or aluminum"),
    C(29, "Column", 6, 2, "Ampacity column (lowest rated part)"),
    # conduit fill
    C(30, "Find", 12, 1, "How many wires fit, or the conduit size"),
    C(31, "Conduit", 13, 1, "Raceway type"),
    C(32, "Trade size", 14, 3, "Raceway trade size"),
    C(33, "Insulation", 15, 1, "Insulation group (Table 5)"),
    C(34, "Wire size", 16, 2, "Size of the main wires"),
    S(35, "How many", "", 0, 1, 0, 1000, 9, "Number of those wires"),
    C(36, "2nd size", 16, 2, "Size of a second group (e.g. ground)"),
    S(37, "2nd count", "", 0, 1, 0, 1000, 0, "Number of second-group wires", blank=1),
    # AWG chart
    C(38, "Wire size", 10, 4, "Conductor size"),
    C(39, "Material", 2, 1, "Copper or aluminum"),
    C(40, "Insulation", 11, 18, "Insulation type"),
    # feeder size
    S(41, "Amps", "A", 0, 5, 1, 100000, 100, "Feeder or service rating, amps"),
    C(42, "System", 18, 3, "Voltage and phase"),
    S(43, "One-way ft", "ft", 0, 5, 1, 100000, 100, "Length, one way"),
    C(44, "Material", 2, 1, "Copper or aluminum"),
    C(45, "Dwelling", 5, 1, "Dwelling service/feeder: 83% (310.12)"),
    C(46, "Max drop", 19, 2, "Allowed voltage drop"),
    C(47, "Column", 6, 2, "Ampacity column (usually 75°C)"),
    # ground wire
    C(48, "Type", 20, 1, "Equipment ground or electrode conductor"),
    S(49, "OCPD", "A", 0, 5, 1, 4000, 60, "Breaker or fuse rating ahead of circuit"),
    C(50, "Material", 2, 1, "Ground wire material"),
    C(51, "Service wire", 10, 15, "Largest service conductor (for the GEC)"),
    C(52, "Service mat.", 2, 1, "Service conductor material"),
    # box fill
    C(53, "Box", 7, 6, "Box from Table 314.16(A), or custom"),
    S(54, "Custom vol.", "in³", 1, 0.5, 0, 1000, 18, "Volume when the box is Custom"),
    C(55, "Wire size", 17, 3, "Largest conductor in the box"),
    S(56, "Conductors", "", 0, 1, 0, 100, 4, "Insulated wires entering (count each)"),
    C(57, "Clamps", 5, 2, "Any internal cable clamps (count 1)"),
    S(58, "Devices", "", 0, 1, 0, 20, 1, "Yokes: switches, receptacles (2 each)"),
    C(59, "Grounds", 5, 2, "Any equipment grounds (count 1)"),
    S(60, "Fittings", "", 0, 1, 0, 20, 0, "Fixture studs or hickeys (1 each)"),
    # MCA / MOCP
    S(61, "Comp RLA", "A", 1, 0.5, 0, 10000, 18.5, "Compressor RLA (or largest motor)"),
    S(62, "Fan FLA", "A", 1, 0.5, 0, 10000, 0.7, "Fan motor FLA (all fans added)"),
    S(63, "Other", "A", 1, 0.5, 0, 10000, 0, "Other loads, amps"),
    S(64, "Plate MOCP", "A", 0, 5, 0, 10000, 0, "MOCP on the nameplate (0 = work out)", blank=1),
    # power calculator
    S(65, "Volts", "V", -1, 1, 0, 10000000, 240, "Voltage; leave 0 if unknown", blank=2),
    S(66, "Amps", "A", -1, 0.1, 0, 10000000, 20, "Current; leave 0 if unknown", blank=2),
    S(67, "Ohms", "Ω", -1, 1, 0, 1000000000, 0, "Resistance; leave 0 if unknown", blank=2),
    S(68, "Watts", "W", -1, 10, 0, 1000000000, 0, "Real power; leave 0 if unknown", blank=2),
    S(69, "Power factor", "", 2, 0.01, 0.01, 1, 1, "PF, 1 for resistive loads"),
    C(70, "Phase", 3, 1, "Single or three phase"),
    # Ohm's law
    S(71, "Volts (E)", "V", -1, 1, 0, 10000000, 120, "Voltage; leave 0 if unknown", blank=2),
    S(72, "Amps (I)", "A", -1, 0.1, 0, 10000000, 0, "Current; leave 0 if unknown", blank=2),
    S(73, "Ohms (R)", "Ω", -1, 1, 0, 1000000000, 12, "Resistance; leave 0 if unknown", blank=2),
    S(74, "Watts (P)", "W", -1, 10, 0, 1000000000, 0, "Power; leave 0 if unknown", blank=2),
    # kWh
    S(75, "Power", "", -1, 10, 0, 100000000, 100, "Power of the device"),
    C(76, "Unit", 21, 1, "Watts or kilowatts"),
    S(77, "Hours/day", "h", 1, 0.5, 0, 24, 8, "Hours of use per day"),
    S(78, "Days/month", "", 0, 1, 1, 31, 30, "Days of use per month"),
    S(79, "Rate", "$/kWh", 3, 0.01, 0, 10, 0.16, "Electric rate, $ per kWh"),
    # electricity cost
    C(80, "State", 22, 1, "State average rate, or custom"),
    S(81, "Rate", "$/kWh", 3, 0.01, 0, 10, 0.16, "Custom rate, $ per kWh"),
    S(82, "kWh/month", "kWh", 0, 10, 0, 100000000, 850, "Energy used per month"),
    # derating
    S(83, "Base amps", "A", 0, 5, 1, 10000, 35, "Table ampacity before derating"),
    C(84, "Column", 6, 2, "Insulation temperature column"),
    S(85, "Ambient", "", 0, 1, -40, 200, 30, "Ambient temperature"),
    S(86, "Conductors", "", 0, 1, 1, 100, 3, "Current-carrying conductors together"),
    # voltage drop table
    C(87, "System", 18, 1, "Voltage and phase"),
    S(88, "Amps", "A", 1, 1, 0.1, 100000, 15, "Load current"),
    C(89, "Material", 2, 1, "Copper or aluminum"),
    C(90, "Wire size", 10, 3, "Conductor size"),
    # breaker / wire chart
    C(91, "Breaker", 23, 2, "Breaker size"),
    # appliances
    C(92, "Appliance", 24, 3, "Appliance or circuit"),
    # NEMA
    C(93, "Receptacle", 25, 14, "NEMA configuration"),
]

# tools in tile order; tile 20 (Learn) opens reference pages instead
TOOLS = [
    ("Voltage drop", "Voltage", "drop", 1, [2, 3, 4, 5, 6, 7, 8, 9]),
    ("Wire size", "Wire", "size", 1, [10, 11, 12, 13, 14, 15, 16, 17]),
    ("Ampacity", "Ampacity", "310.16/17", 1, [18, 19, 20, 21, 22, 1, 23, 24]),
    ("Breaker size", "Breaker", "size", 1, [25, 26, 27, 28, 29]),
    ("Conduit fill", "Conduit", "fill", 2, [30, 31, 32, 33, 34, 35, 36, 37]),
    ("AWG chart", "AWG", "chart", 2, [38, 39, 40]),
    ("Feeder size", "Feeder", "size", 2, [41, 42, 43, 44, 45, 46, 47]),
    ("Ground wire", "Ground", "wire", 2, [48, 49, 50, 51, 52]),
    ("Box fill", "Box", "fill", 3, [53, 54, 55, 56, 57, 58, 59, 60]),
    ("MCA / MOCP", "MCA /", "MOCP", 3, [61, 62, 63, 64]),
    ("Power calculator", "Power", "calc", 3, [65, 66, 67, 68, 69, 70]),
    ("Ohm's law", "Ohm's", "law", 3, [71, 72, 73, 74]),
    ("kWh calculator", "kWh", "", 4, [75, 76, 77, 78, 79]),
    ("Electricity cost", "Elec.", "cost", 4, [80, 81, 82]),
    ("Wire derating", "Derating", "", 4, [83, 84, 85, 1, 86]),
    ("Voltage drop table", "VD", "table", 4, [87, 88, 89, 90]),
    ("Breaker / wire chart", "Breaker", "wire chart", 5, [91]),
    ("Appliance circuits", "Appli-", "ances", 5, [92]),
    ("NEMA receptacles", "NEMA", "plugs", 5, [93]),
]


def check():
    check_slots(SLOTS, TOOLS, ntools=19)
    for a in APPLIANCES:
        assert len(a) == 8 and all(len(x) <= 34 for x in a), a
    for n in NEMA:
        assert len(n) == 5 and len(n[3]) <= 34 and len(n[4]) <= 34, n
    assert len(CHOICES[23]) == 28 and EGC[-1][0] == 4000
    for col in list(T16.values()) + list(T17.values()):
        assert len(col) == len(SIZES)
        nz = [a for a in col if a]
        assert nz == sorted(nz)
    assert len(CMIL) == len(SIZES) and all(len(v) == len(SIZES) for v in R8.values())
    # Table 8: resistance x area is nearly constant for each metal
    for metal, k in (("Cu", 12.9), ("Al", 21.2)):
        for r, cm in zip(R8[metal], CMIL):
            if r:
                assert abs(r * cm / 1000 / k - 1) < 0.02, (metal, r, cm)
    for (tc, top), v in CORR_CHECK.items():
        assert CORR[(60, 75, 90).index(tc)][AMB_TOP.index(top)] == v, (tc, top)
    assert all(len(g) == len(FILL_SIZES) for g in FILL_AREA)
    assert all(len(c) == len(TRADE) for c in CONDUIT)
    # conduit areas follow from round inside diameters, so each type grows
    for c in CONDUIT:
        nz = [a for a in c if a]
        assert nz == sorted(nz)


def build_block():
    out = ["// ---- BEGIN TABLES (generated by tools/gen_nec_tables.py) ----"]
    out += slot_globals(TOOLS, SLOTS)
    out += [
        "// conductor sizes: circular mils, Table 8 dc resistance (ohm/kft, 75 C)",
        "gCM:=" + plist(CMIL) + ";",
        "gR8:=" + pmatrix([R8["Cu"], R8["Al"]]) + ";",
        "// Table 310.16 then 310.17: rows Cu 60/75/90 C, Al 60/75/90 C; 0 = not listed",
        "gA16:=" + pmatrix([T16[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "gA17:=" + pmatrix([T17[(m, t)] for m in ("Cu", "Al") for t in (60, 75, 90)]) + ";",
        "// insulation types: temperature column (4 = NM cable) and Table 5 group",
        "gInsCol:=" + plist([t[1] for t in INSULATION]) + ";",
        "gInsGrp:=" + plist([t[2] for t in INSULATION]) + ";",
        "// Table 310.15(B)(1): top of each ambient band (C), factors for 60/75/90 C",
        "gAmbTop:=" + plist(AMB_TOP) + ";",
        "gCorr:=" + pmatrix(CORR) + ";",
        "// Chapter 9 Table 5 areas (in2) by group, 14 AWG - 500 kcmil",
        "gFill:=" + pmatrix(FILL_AREA) + ";",
        "// Chapter 9 Table 4 total areas (in2) by raceway and trade size",
        "gCond:=" + pmatrix(CONDUIT) + ";",
        "gStd:=" + plist(STD_SIZES) + ";",
        "gBoxV:=" + plist(BOX_VOL) + ";",
        "// Table 314.16(A) box volumes, in3 (first = custom)",
        "gBoxes:=" + plist([b[1] for b in BOXES]) + ";",
        "// systems: volts and phase",
        "gSysV:=" + plist([s[1] for s in SYSTEMS]) + ";",
        "gSysP:=" + plist([s[2] for s in SYSTEMS]) + ";",
        "// Table 250.122: OCPD up to (A), Cu and Al size (index into the sizes)",
        "gEgcA:=" + plist([e[0] for e in EGC]) + ";",
        "gEgcCu:=" + plist([SIZES.index(e[1]) + 1 for e in EGC]) + ";",
        "gEgcAl:=" + plist([SIZES.index(e[2]) + 1 for e in EGC]) + ";",
        "// Table 250.66: largest service conductor up to (cmil, Cu / Al), GEC Cu / Al",
        "gGecSc:=" + plist([g[0] for g in GEC]) + ";",
        "gGecSa:=" + plist([g[1] for g in GEC]) + ";",
        "gGecCu:=" + plist([SIZES.index(g[2]) + 1 for g in GEC]) + ";",
        "gGecAl:=" + plist([SIZES.index(g[3]) + 1 for g in GEC]) + ";",
        "// average residential rates, $/kWh (first = custom)",
        "gRate:=" + plist([0] + [r[1] for r in STATE_RATES]) + ";",
        "// appliance guides: circuit, breaker, copper, aluminum, outlet, NEC, note",
        "gApC:=" + plist([a[1] for a in APPLIANCES]) + ";",
        "gApB:=" + plist([a[2] for a in APPLIANCES]) + ";",
        "gApCu:=" + plist([a[3] for a in APPLIANCES]) + ";",
        "gApAl:=" + plist([a[4] for a in APPLIANCES]) + ";",
        "gApO:=" + plist([a[5] for a in APPLIANCES]) + ";",
        "gApN:=" + plist([a[6] for a in APPLIANCES]) + ";",
        "gApX:=" + plist([a[7] for a in APPLIANCES]) + ";",
        "// NEMA configurations: voltage, amps, wires, typical use",
        "gNmV:=" + plist([n[1] for n in NEMA]) + ";",
        "gNmA:=" + plist([n[2] for n in NEMA]) + ";",
        "gNmW:=" + plist([n[3] for n in NEMA]) + ";",
        "gNmU:=" + plist([n[4] for n in NEMA]) + ";",
        "",
    ]
    out += slot_functions(TOOLS, CHOICES, None, 0)
    out += ["// ---- END TABLES ----"]
    return "\n".join(out)


def main():
    check()
    write_block(PROGRAM, build_block())
    print(f"wrote {len(SLOTS)} input boxes and {len(TOOLS)} tools into {PROGRAM}")


if __name__ == "__main__":
    main()
