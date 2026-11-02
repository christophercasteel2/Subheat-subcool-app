#!/usr/bin/env python3
"""Checks that the JavaScript made by tools/ppl2js.py (the Android apps)
runs every program exactly as the simulator does.

For each app it plays the same random touches, drags, key presses and
dialog answers through the Python simulator (tools/ppl_sim.py) and
through the translated program in Node (tools/android/fuzz_driver.js),
then compares every global variable: the input values, the results, the
selected tool and screen.  The simulator is what the program tests run
against, so a match means those tests hold for the Android apps too.

    python3 tools/test_android.py            # all apps, 40 runs each
    python3 tools/test_android.py CIRCUITS 200
"""
import json
import math
import os
import random
import subprocess
import sys

from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl2js import translate  # noqa: E402
from ppl_sim import FONT_FILE, Interp, PPLError, StopSim  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(ROOT, "tools", "android", "fuzz_driver.js")
APPS = ["SUPERSUB", "HVACAIR", "NECCALC", "HVACELEC", "HVACGAS", "REFCYCLE", "CIRCUITS"]
KEYS = [2, 12, 7, 8, 30, 4, 3, 13, 19, 1, 6, 11, 45, 50, 27,
        47, 42, 43, 44, 37, 38, 39, 32, 33, 34, 48]
INPUT_VALUES = [0, 1, 2.5, 12, 40, 75, 100, 350, 1000, -5, 0.015, 7]


class FuzzInterp(Interp):
    """the simulator, answering dialogs from a list of random numbers"""

    def __init__(self, src, events, replies):
        super().__init__(src, events)
        self.replies = list(replies)

    def dialog(self, kind, vals, cur):
        r = self.replies.pop(0) if self.replies else None
        if r is None:
            return False, cur
        if kind == "CHOOSE":
            items = vals[1] if len(vals) == 2 and isinstance(vals[1], list) else vals[1:]
            return True, float(1 + math.floor(r * len(items)))
        return True, float(INPUT_VALUES[math.floor(r * len(INPUT_VALUES))])


def widths(src):
    chars = set(chr(c) for c in range(32, 127))
    for part in src.split('"')[1::2]:
        chars |= set(part)
    out = {}
    for n in range(1, 8):
        f = ImageFont.truetype(FONT_FILE, 8 + 2 * n)
        out[8 + 2 * n] = {ch: f.getlength(ch) for ch in chars}
    return out


def make_events(rng, n):
    ev = []
    while len(ev) < n:
        r = rng.random()
        if r < 0.45:
            x = rng.randrange(320)
            y = rng.randrange(21, 240) if rng.random() < 0.95 else rng.randrange(21)
            ev += [[0, x, y], [2], [3, x, y]]
        elif r < 0.52:
            x, y = rng.randrange(320), rng.randrange(21, 240)
            ev.append([0, x, y])
            for _ in range(rng.randrange(1, 6)):
                x = max(0, min(319, x + rng.randrange(-30, 31)))
                y = max(21, min(239, y + rng.randrange(-30, 31)))
                ev.append([1, x, y])
            ev.append([2])
        else:
            ev.append(rng.choice(KEYS))
    return ev


def run_py(src, name, events, replies):
    it = FuzzInterp(src, events, replies)
    status, msg = "ended", ""
    try:
        it.start(name)
    except StopSim:
        status = "stopped"
    except (PPLError, ZeroDivisionError, ValueError, TypeError, OverflowError) as exc:
        status, msg = "error", str(exc)
    used = len(events) - len(it.events)
    return {"status": status, "msg": msg, "events": used, "g": it.g}


def run_js(js, events, replies, wd):
    job = {"program": js, "events": events, "replies": replies, "widths": wd, "input_values": INPUT_VALUES}
    p = subprocess.run(["node", DRIVER], input=json.dumps(job), capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-2000:])
    return json.loads(p.stdout)


def same(a, b, path, diffs):
    if isinstance(a, list) or isinstance(b, list):
        if not (isinstance(a, list) and isinstance(b, list)) or len(a) != len(b):
            diffs.append(f"{path}: {str(a)[:80]} vs {str(b)[:80]}")
            return
        for k, (x, y) in enumerate(zip(a, b)):
            same(x, y, f"{path}({k + 1})", diffs)
    elif isinstance(a, str) or isinstance(b, str):
        if a != b:
            diffs.append(f"{path}: {a!r} vs {b!r}")
    else:
        a, b = float(a), float(b)
        if not (a == b or abs(a - b) <= 1e-9 * max(abs(a), abs(b))):
            diffs.append(f"{path}: {a!r} vs {b!r}")


def main():
    apps = [sys.argv[1]] if len(sys.argv) > 1 else APPS
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    bad = 0
    for app in apps:
        src = open(os.path.join(ROOT, "hp-prime", app + ".txt"), encoding="utf-8").read()
        js = translate(src)
        wd = widths(src)
        rng = random.Random(app)
        depth = []
        fails = 0
        for k in range(runs):
            events = make_events(rng, rng.randrange(20, 140))
            replies = [None if rng.random() < 0.1 else rng.random() for _ in range(300)]
            py = run_py(src, app, events, replies)
            js_ = run_js(js, events, replies, wd)
            diffs = []
            if py["status"] != js_["status"] or py["events"] != js_["events"]:
                diffs.append(f"status {py['status']} after {py['events']} events {py['msg'][:100]} "
                             f"vs {js_['status']} after {js_['events']} {js_.get('msg', '')[:300]}")
            for name, v in py["g"].items():
                same(v, js_["g"].get(name), name, diffs)
            depth.append(py["events"])
            if diffs:
                fails += 1
                if fails <= 3:
                    print(f"  {app} run {k}: " + "; ".join(diffs[:6]))
        bad += fails
        print(f"{app}: {runs - fails}/{runs} runs match (events played per run: "
              f"{min(depth)}-{max(depth)}, avg {sum(depth) / len(depth):.0f})")
    if bad:
        sys.exit(1)
    print("the translated programs match the simulator")


if __name__ == "__main__":
    main()
