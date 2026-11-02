"""Helpers shared by the generators that write the TABLES block of the tile
apps (tools/gen_elec_tables.py for HVACELEC, tools/gen_air_tables.py for
HVACAIR).

Each app describes its input boxes ("slots") and its tools in Python; these
helpers check them and turn them into the program's parallel lists, its
toolIns(t) and its choiceList(c).
"""
import re


def slot(num, label, unit, dec, step, lo, hi, default, hlp, choice=0, blank=0):
    """An input box.  dec: decimals shown (-1 = as many as needed); step: the
    Up/Down step; choice: the choiceList number (0 = a number); blank:
    1 shows -- and 2 shows ? while the value is 0."""
    return dict(num=num, label=label, unit=unit, dec=dec, step=step, lo=lo, hi=hi,
                default=default, help=hlp, choice=choice, blank=blank)


def choice_slot(choices, units_id, units_max):
    """A function making a choice box, given the app's choice lists and the
    number (and longest length) of its dynamic unit list."""
    def make(num, label, choice, default, hlp):
        n = units_max if choice == units_id else len(choices[choice])
        return slot(num, label, "", 0, 1, 1, n, default, hlp, choice)
    return make


def ppl_num(v):
    if isinstance(v, str):
        return v
    if float(v).is_integer():
        return str(int(v))
    s = repr(float(v))
    if "e" in s:
        s = f"{v:.12f}".rstrip("0")
    return s


def ppl_str(s):
    assert '"' not in s
    return '"' + s + '"'


def plist(vals):
    return "{" + ",".join(ppl_str(v) if isinstance(v, str) else ppl_num(v) for v in vals) + "}"


def pmatrix(rows):
    return "[" + ",".join("[" + ",".join(ppl_num(v) for v in r) + "]" for r in rows) + "]"


def check_slots(slots, tools, ntools=20, max_ins=8):
    nums = [s["num"] for s in slots]
    assert nums == list(range(1, len(slots) + 1)), "slots must be numbered 1, 2, 3, ..."
    for s in slots:
        assert s["lo"] <= s["default"] <= s["hi"], s
        if s["choice"]:
            assert s["dec"] == 0 and s["lo"] == 1, s
        assert len(s["help"]) <= 44, f"help too long for slot {s['num']}"
        assert len(s["label"]) <= 12, f"label too long for slot {s['num']}"
    used = sorted({k for t in tools for k in t[4]})
    assert used == nums, "every slot belongs to a tool"
    assert len(tools) == ntools
    for t in tools:
        assert len(t[4]) <= max_ins, f"{t[0]}: at most {max_ins} input boxes fit"


def slot_globals(tools, slots):
    """Program lines for the tool names and the input-box lists."""
    return [
        "gNT:=" + str(len(tools)) + ";",
        "gTName:=" + plist([t[0] for t in tools]) + ";",
        "gTile1:=" + plist([t[1] for t in tools]) + ";",
        "gTile2:=" + plist([t[2] for t in tools]) + ";",
        "gTCat:=" + plist([t[3] for t in tools]) + ";",
        "// input boxes: value, default, label, unit, decimals (-1 = as needed),",
        "// Up/Down step, lowest, highest, choice list (0 = number),",
        "// blank (1: 0 shows --, 2: 0 shows ?)",
        "gV:=" + plist([s["default"] for s in slots]) + ";",
        "gDef:=" + plist([s["default"] for s in slots]) + ";",
        "gSL:=" + plist([s["label"] for s in slots]) + ";",
        "gSU:=" + plist([s["unit"] for s in slots]) + ";",
        "gSD:=" + plist([s["dec"] for s in slots]) + ";",
        "gSS:=" + plist([s["step"] for s in slots]) + ";",
        "gSLo:=" + plist([s["lo"] for s in slots]) + ";",
        "gSHi:=" + plist([s["hi"] for s in slots]) + ";",
        "gSC:=" + plist([s["choice"] for s in slots]) + ";",
        "gSZ:=" + plist([s["blank"] for s in slots]) + ";",
        "gSH:=" + plist([s["help"] for s in slots]) + ";",
    ]


def slot_functions(tools, choices, units_id, kind_slot):
    """toolIns(t) and choiceList(c); list units_id is the converter's unit
    list for the kind chosen in box kind_slot."""
    out = ["// input boxes of each tool, two per row", "toolIns(t)", "BEGIN"]
    for k, t in enumerate(tools, 1):
        out.append(f"  IF t=={k} THEN RETURN {plist(t[4])}; END;")
    out += ["  RETURN {};", "END;", "",
            f"// fixed choice lists ({units_id} = the converter's units)" if units_id
            else "// choice lists",
            "choiceList(c)", "BEGIN"]
    for c in sorted(choices):
        out.append(f"  IF c=={c} THEN RETURN {plist(choices[c])}; END;")
    out += [f"  RETURN convUnits(gV({kind_slot}));" if units_id else "  RETURN {};", "END;"]
    return out


def write_block(path, block):
    """Replace the TABLES block of the program at path."""
    src = open(path, encoding="utf-8").read()
    pat = re.compile(r"// ---- BEGIN TABLES.*?// ---- END TABLES ----", re.S)
    if not pat.search(src):
        raise SystemExit("no table block in " + path)
    src = pat.sub(lambda m: block, src)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
