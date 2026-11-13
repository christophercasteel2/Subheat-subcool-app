#!/usr/bin/env python3
"""A small HP PPL interpreter, just big enough to run SUPERSUB off the
calculator: it executes the program, renders its screens with Pillow and
feeds it scripted key presses / touches.  It is a development aid only;
the real calculator remains the reference (fonts and some edge cases of
the language differ).

Usage
  python3 tools/ppl_sim.py            # run the built-in test script,
                                      # screenshots go to docs/screens/
  python3 tools/ppl_sim.py FILE OUTDIR   # test another copy of the program
"""
import math
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEYWORDS = {"BEGIN", "END", "IF", "THEN", "ELSE", "FOR", "FROM", "TO", "STEP",
            "DO", "WHILE", "REPEAT", "UNTIL", "LOCAL", "RETURN", "EXPORT",
            "AND", "OR", "NOT", "MOD"}

TOKEN_RE = re.compile(r"""
    (?P<ws>\s+) | (?P<comment>//[^\n]*) | (?P<pragma>\#pragma[^\n]*) |
    (?P<str>"[^"]*") | (?P<num>\d+\.\d*|\d*\.\d+|\d+) |
    (?P<id>[A-Za-z_][A-Za-z0-9_]*) |
    (?P<op>:=|==|<>|<=|>=|[-+*/^(){}\[\],;<>=])
""", re.X)


class PPLError(Exception):
    pass


class StopSim(Exception):
    pass


def tokenize(src):
    toks, pos, line = [], 0, 1
    while pos < len(src):
        m = TOKEN_RE.match(src, pos)
        if not m:
            raise PPLError(f"line {line}: bad character {src[pos]!r}")
        kind = m.lastgroup
        text = m.group()
        if kind == "id" and text in KEYWORDS:
            kind = "kw"
        if kind not in ("ws", "comment", "pragma"):
            toks.append((kind, text, line))
        line += text.count("\n")
        pos = m.end()
    toks.append(("eof", "", line))
    return toks


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self, o=0):
        return self.t[self.i + o]

    def next(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def accept(self, text):
        if self.peek()[1] == text and self.peek()[0] in ("kw", "op"):
            self.i += 1
            return True
        return False

    def expect(self, text):
        tok = self.next()
        if tok[1] != text:
            raise PPLError(f"line {tok[2]}: expected {text!r}, got {tok[1]!r}")
        return tok

    def ident(self):
        tok = self.next()
        if tok[0] != "id":
            raise PPLError(f"line {tok[2]}: expected a name, got {tok[1]!r}")
        return tok[1]

    # ---- program ----
    def program(self):
        globs, funcs = [], {}
        while self.peek()[0] != "eof":
            exported = self.accept("EXPORT")
            name = self.ident()
            if self.peek()[1] == "(":
                self.expect("(")
                params = []
                if not self.accept(")"):
                    params.append(self.ident())
                    while self.accept(","):
                        params.append(self.ident())
                    self.expect(")")
                self.expect("BEGIN")
                body = self.block(("END",))
                self.expect("END")
                self.expect(";")
                if name in funcs:
                    raise PPLError(f"function {name} defined twice")
                funcs[name] = (params, body, exported)
            else:
                self.expect(":=")
                globs.append((name, self.expr()))
                self.expect(";")
        return globs, funcs

    def block(self, enders):
        out = []
        while self.peek()[1] not in enders:
            out.append(self.stmt())
        return out

    def stmt(self):
        tok = self.peek()
        line = tok[2]
        if self.accept("LOCAL"):
            decls = []
            while True:
                name = self.ident()
                init = self.expr() if self.accept(":=") else None
                decls.append((name, init))
                if not self.accept(","):
                    break
            self.expect(";")
            if len(decls) > 8:
                # the calculator stops with a syntax error at the ninth name
                raise PPLError(f"line {line}: one LOCAL can declare at most 8 names")
            return ("local", line, decls)
        if self.accept("IF"):
            cond = self.expr()
            self.expect("THEN")
            a = self.block(("ELSE", "END"))
            b = []
            if self.accept("ELSE"):
                b = self.block(("END",))
            self.expect("END")
            self.expect(";")
            return ("if", line, cond, a, b)
        if self.accept("FOR"):
            var = self.ident()
            self.expect("FROM")
            lo = self.expr()
            self.expect("TO")
            hi = self.expr()
            step = self.expr() if self.accept("STEP") else ("num", 1)
            self.expect("DO")
            body = self.block(("END",))
            self.expect("END")
            self.expect(";")
            return ("for", line, var, lo, hi, step, body)
        if self.accept("WHILE"):
            cond = self.expr()
            self.expect("DO")
            body = self.block(("END",))
            self.expect("END")
            self.expect(";")
            return ("while", line, cond, body)
        if self.accept("REPEAT"):
            body = self.block(("UNTIL",))
            self.expect("UNTIL")
            cond = self.expr()
            self.expect(";")
            return ("repeat", line, body, cond)
        if self.accept("RETURN"):
            val = None if self.peek()[1] == ";" else self.expr()
            self.expect(";")
            return ("return", line, val)
        if tok[0] == "id" and self.peek(1)[1] == ":=":
            name = self.ident()
            self.expect(":=")
            val = self.expr()
            self.expect(";")
            return ("assign", line, name, val)
        e = self.expr()
        if self.accept(":="):
            # element assignment L(i):=v (or M(r,c):=v)
            if e[0] != "call":
                raise PPLError(f"line {line}: cannot assign to that")
            val = self.expr()
            self.expect(";")
            return ("setidx", line, e[1], e[2], val)
        self.expect(";")
        return ("expr", line, e)

    # ---- expressions ----
    def expr(self):
        return self.or_()

    def binary(self, sub, ops):
        left = sub()
        while self.peek()[1] in ops and self.peek()[0] in ("op", "kw"):
            op = self.next()[1]
            left = ("bin", op, left, sub())
        return left

    def or_(self):
        return self.binary(self.and_, ("OR",))

    def and_(self):
        return self.binary(self.not_, ("AND",))

    def not_(self):
        if self.accept("NOT"):
            return ("not", self.not_())
        return self.cmp()

    def cmp(self):
        return self.binary(self.add, ("==", "<>", "<", ">", "<=", ">=", "="))

    def add(self):
        return self.binary(self.mul, ("+", "-"))

    def mul(self):
        return self.binary(self.unary, ("*", "/", "MOD"))

    def unary(self):
        if self.accept("-"):
            return ("neg", self.unary())
        return self.power()

    def power(self):
        base = self.postfix()
        if self.accept("^"):
            return ("bin", "^", base, self.unary())
        return base

    def postfix(self):
        tok = self.next()
        kind, text, line = tok
        if kind == "num":
            return ("num", float(text))
        if kind == "str":
            return ("str", text[1:-1])
        if text == "(":
            e = self.expr()
            self.expect(")")
            return e
        if text == "{":
            items = []
            if not self.accept("}"):
                items.append(self.expr())
                while self.accept(","):
                    items.append(self.expr())
                self.expect("}")
            return ("list", items)
        if text == "[":
            items = [self.expr()]
            while self.accept(","):
                items.append(self.expr())
            self.expect("]")
            return ("mat", items)
        if kind == "id":
            if self.accept("("):
                args = []
                if not self.accept(")"):
                    args.append(self.expr())
                    while self.accept(","):
                        args.append(self.expr())
                    self.expect(")")
                return ("call", text, args, line)
            return ("var", text, line)
        raise PPLError(f"line {line}: unexpected {text!r}")


def walk_calls(node, out):
    if isinstance(node, tuple):
        if node and node[0] == "call":
            out.append((node[1], node[3]))
        for x in node:
            walk_calls(x, out)
    elif isinstance(node, list):
        for x in node:
            walk_calls(x, out)


# names a program should not reuse: Home/app variables and common CAS commands
RESERVED = (set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") | {"e", "i"} |
            {f"{p}{k}" for p in "GLMZFXYRUVCD" for k in range(10)} |
            {f"{p}{k}" for p in "HS" for k in range(1, 6)} |
            {"ln", "log", "exp", "sin", "cos", "tan", "max", "min", "abs", "floor",
             "ceil", "round", "size", "sum", "len", "int", "string", "char", "left",
             "right", "mid", "dim", "type", "sqrt", "solve", "det", "sign", "mod",
             "Ans", "Xmin", "Xmax", "Ymin", "Ymax",
             # more CAS commands that make poor variable names
             "row", "col", "cat", "base", "part", "head", "tail", "sort", "trn",
             "rank", "normal", "eval", "approx", "exact", "frac", "re", "im",
             "conj", "arg", "subst", "expand", "factor", "simplify", "series",
             "limit", "diff", "mean", "median", "zeros", "concat", "inv", "ins",
             "out", "id", "count",
             # language words, which the calculator does not let you reuse
             # in lower case either
             "begin", "end", "if", "then", "else", "for", "from", "to", "step",
             "do", "while", "repeat", "until", "local", "return", "export",
             "and", "or", "not", "xor", "mod", "case", "default", "break",
             "continue", "kill", "iferr", "pi", "in"})


def check_names(globs, funcs):
    names = [(n, "global") for n, _ in globs] + [(n, "function") for n in funcs]
    for fname, (params, body, _) in funcs.items():
        names += [(n, f"parameter of {fname}") for n in params]
        stack = list(body)
        while stack:
            st = stack.pop()
            if isinstance(st, tuple) and st and st[0] == "local":
                names += [(n, f"local in {fname}") for n, _ in st[2]]
            if isinstance(st, (tuple, list)):
                stack.extend(x for x in st if isinstance(x, (tuple, list)))
    # the calculator reads its language words in any mix of capitals, so
    # a name like tO is the word TO to it
    words = {"begin", "end", "if", "then", "else", "for", "from", "to", "step", "do", "while", "repeat",
             "until", "local", "return", "export", "and", "or", "not", "xor", "mod", "case", "default",
             "break", "continue", "kill", "iferr", "downto"}
    for n, where in names:
        if n in RESERVED or n.lower() in words:
            raise PPLError(f"{where}: name {n!r} clashes with a calculator name")


def check_order(funcs):
    """HP PPL compiles in one pass: a program function has to be defined
    (or forward declared) above the first function that calls it."""
    order = list(funcs)
    for i, name in enumerate(order):
        calls = []
        walk_calls(funcs[name][1], calls)
        for callee, line in calls:
            if callee in funcs and order.index(callee) > i:
                raise PPLError(f"line {line}: {name} calls {callee} before it is defined")


class Matrix(list):
    pass


class Grob:
    def __init__(self, w=320, h=240):
        self.img = Image.new("RGB", (w, h), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


def rgb_tuple(c):
    c = int(c)
    return ((c >> 16) & 255, (c >> 8) & 255, c & 255)


FONT_FILE = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_fonts = {}


def font(n):
    n = int(n) or 3
    if n not in _fonts:
        _fonts[n] = ImageFont.truetype(FONT_FILE, 8 + 2 * n)
    return _fonts[n]


def ppl_round(x, n=0):
    m = 10 ** int(n)
    return math.copysign(math.floor(abs(x) * m + 0.5) / m, x)


def ppl_str(v):
    if isinstance(v, str):
        return v
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return repr(v)


class Interp:
    def __init__(self, src, events):
        self.src = src
        self.globs, self.funcs = Parser(tokenize(src)).program()
        check_order(self.funcs)
        check_names(self.globs, self.funcs)
        self.events = list(events)
        self.g = {}
        self.sysvars = {"HAngle": 0.0}
        self.grobs = {f"G{k}": Grob() for k in range(10)}
        self.shots = []
        self.trace = []
        for name, e in self.globs:
            self.g[name] = self.eval(e, {})

    # ---- names ----
    def lookup(self, name, frame, line):
        if name in frame:
            v = frame[name]
            if v is None:
                return 0.0
            return v
        if name in self.g:
            return self.g[name]
        if name in self.sysvars:
            return self.sysvars[name]
        if name in self.grobs:
            return self.grobs[name]
        raise PPLError(f"line {line}: unknown name {name}")

    def assign(self, name, val, frame, line):
        if isinstance(val, list):
            val = type(val)(val)
        if name in frame:
            frame[name] = val
        elif name in self.g:
            self.g[name] = val
        elif name in self.sysvars:
            self.sysvars[name] = val
        else:
            raise PPLError(f"line {line}: assignment to undeclared {name}")

    # ---- statements ----
    def run_block(self, stmts, frame):
        for s in stmts:
            self.exec(s, frame)

    def exec(self, s, frame):
        kind, line = s[0], s[1]
        if kind == "local":
            for name, init in s[2]:
                frame[name] = self.eval(init, frame) if init else 0.0
        elif kind == "assign":
            self.assign(s[2], self.eval(s[3], frame), frame, line)
        elif kind == "expr":
            self.eval(s[2], frame)
        elif kind == "setidx":
            name, idx = s[2], [self.eval(x, frame) for x in s[3]]
            val = self.eval(s[4], frame)
            obj = self.lookup(name, frame, line)
            if not isinstance(obj, list):
                raise PPLError(f"line {line}: {name} is not a list")
            new = type(obj)(list(x) if isinstance(x, list) else x for x in obj)
            target = new
            for depth, ix in enumerate(idx):
                k = int(ix)
                if k != ix or k < 1 or k > len(target) + (1 if depth == len(idx) - 1 else 0):
                    raise PPLError(f"line {line}: {name}: bad index {ix}")
                if depth == len(idx) - 1:
                    if k == len(target) + 1:
                        target.append(val)          # storing at SIZE+1 appends
                    else:
                        target[k - 1] = val
                else:
                    target = target[k - 1]
            self.assign(name, new, frame, line)
        elif kind == "if":
            if self.truth(self.eval(s[2], frame), line):
                self.run_block(s[3], frame)
            else:
                self.run_block(s[4], frame)
        elif kind == "for":
            var = s[2]
            lo, hi, st = (self.eval(e, frame) for e in s[3:6])
            self.assign(var, lo, frame, line)
            while self.lookup(var, frame, line) <= hi + 1e-12:
                self.run_block(s[6], frame)
                self.assign(var, self.lookup(var, frame, line) + st, frame, line)
        elif kind == "while":
            n = 0
            while self.truth(self.eval(s[2], frame), line):
                self.run_block(s[3], frame)
                n += 1
                if n > 100000:
                    raise PPLError(f"line {line}: runaway WHILE")
        elif kind == "repeat":
            while True:
                self.run_block(s[2], frame)
                if self.truth(self.eval(s[3], frame), line):
                    break
        elif kind == "return":
            raise ReturnSignal(self.eval(s[2], frame) if s[2] else 0.0)
        else:
            raise PPLError(f"bad statement {kind}")

    def truth(self, v, line):
        if isinstance(v, (int, float)):
            return v != 0
        raise PPLError(f"line {line}: condition is not a number: {v!r}")

    # ---- expressions ----
    def eval(self, e, frame):
        kind = e[0]
        if kind == "num":
            return e[1]
        if kind == "str":
            return e[1]
        if kind == "var":
            return self.lookup(e[1], frame, e[2])
        if kind == "neg":
            return -self.num(self.eval(e[1], frame))
        if kind == "not":
            return 0.0 if self.eval(e[1], frame) else 1.0
        if kind == "list":
            return [self.eval(x, frame) for x in e[1]]
        if kind == "mat":
            return Matrix(self.eval(x, frame) for x in e[1])
        if kind == "bin":
            return self.binop(e[1], self.eval(e[2], frame), self.eval(e[3], frame))
        if kind == "call":
            return self.call(e[1], e[2], frame, e[3])
        raise PPLError(f"bad expression {kind}")

    def num(self, v):
        if not isinstance(v, (int, float)):
            raise PPLError(f"number expected, got {v!r}")
        return v

    def binop(self, op, a, b):
        if op == "+" and (isinstance(a, str) or isinstance(b, str)):
            return ppl_str(a) + ppl_str(b)
        if op in ("==", "=", "<>") and isinstance(a, str) and isinstance(b, str):
            return float((a == b) == (op != "<>"))
        a, b = self.num(a), self.num(b)
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/":
            if b == 0:
                raise PPLError("division by zero")
            return a / b
        if op == "^": return a ** b
        if op == "MOD": return a - b * math.floor(a / b)
        if op in ("==", "="): return float(a == b)
        if op == "<>": return float(a != b)
        if op == "<": return float(a < b)
        if op == ">": return float(a > b)
        if op == "<=": return float(a <= b)
        if op == ">=": return float(a >= b)
        if op == "AND": return float(bool(a) and bool(b))
        if op == "OR": return float(bool(a) or bool(b))
        raise PPLError(f"bad operator {op}")

    def call(self, name, args, frame, line):
        # by-reference builtins
        if name == "INPUT" and args[0][0] == "list":
            # INPUT({a, b, ...}, title, {labels}, {help}): one box per variable
            refs = args[0][1]
            if any(r[0] != "var" for r in refs):
                raise PPLError(f"line {line}: INPUT needs variables")
            vals = [self.eval(a, frame) for a in args[1:]]
            cur = [self.lookup(r[1], frame, line) for r in refs]
            ev = self.events.pop(0) if self.events else None
            if not (isinstance(ev, tuple) and ev[0] == "dialog"):
                raise PPLError(f"script expected a reply for INPUT {vals[:1]}")
            self.trace.append(("INPUT", vals[0], ev[1]))
            if ev[1] is None:
                return 0.0
            new = ev[1] if isinstance(ev[1], (list, tuple)) else [ev[1]]
            for r, v in zip(refs, list(new) + cur[len(new):]):
                self.assign(r[1], float(v), frame, line)
            return 1.0
        if name in ("INPUT", "CHOOSE"):
            ref = args[0]
            if ref[0] != "var":
                raise PPLError(f"line {line}: {name} needs a variable")
            vals = [self.eval(a, frame) for a in args[1:]]
            ok, val = self.dialog(name, vals, self.lookup(ref[1], frame, line))
            if ok:
                self.assign(ref[1], val, frame, line)
            return float(ok)
        vals = [self.eval(a, frame) for a in args]
        # indexing a variable
        if name in frame or name in self.g:
            obj = self.lookup(name, frame, line)
            try:
                for ix in vals:
                    k = int(ix)
                    if k < 1 or k > len(obj) or k != ix:
                        raise PPLError(f"line {line}: {name}: bad index {ix}")
                    obj = obj[k - 1]
            except TypeError:
                raise PPLError(f"line {line}: {name} is not a list")
            return obj
        if name in self.funcs:
            params, body, _ = self.funcs[name]
            if len(vals) != len(params):
                raise PPLError(f"line {line}: {name} takes {len(params)} arguments")
            new = dict(zip(params, vals))
            try:
                self.run_block(body, new)
            except ReturnSignal as r:
                return r.value
            return 0.0
        fn = getattr(self, "b_" + name, None)
        if fn is None:
            raise PPLError(f"line {line}: unknown function {name}")
        return fn(*vals)

    # ---- maths builtins ----
    def ang_in(self, a):
        return math.radians(a) if self.sysvars["HAngle"] == 1 else a

    def b_SIN(self, a): return math.sin(self.ang_in(a))
    def b_COS(self, a): return math.cos(self.ang_in(a))

    def b_ATAN(self, x):
        r = math.atan(x)
        return math.degrees(r) if self.sysvars["HAngle"] == 1 else r

    def b_LN(self, x):
        if x <= 0:
            raise PPLError(f"LN of {x}")
        return math.log(x)

    def b_EXP(self, x): return math.exp(x)

    def b_LOG(self, x):
        if x <= 0:
            raise PPLError(f"LOG of {x}")
        return math.log10(x)
    def b_ABS(self, x): return abs(x)
    def b_IP(self, x): return float(math.trunc(x))
    def b_FLOOR(self, x): return float(math.floor(x))
    def b_CEILING(self, x): return float(math.ceil(x))
    def b_ROUND(self, x, n=0): return ppl_round(x, n)
    def b_MAX(self, a, b): return max(a, b)
    def b_MIN(self, a, b): return min(a, b)
    def b_IFTE(self, c, a, b): return a if c else b
    def b_CHAR(self, c): return chr(int(c))
    def b_DIM(self, s): return float(len(s))
    def b_SIZE(self, s): return float(len(s))
    def b_LEFT(self, s, n): return s[:int(n)]
    def b_RIGHT(self, s, n): return s[len(s) - int(n):] if int(n) > 0 else ""
    def b_MID(self, s, k, n=None):
        k = max(int(k), 1) - 1
        return s[k:] if n is None else s[k:k + max(int(n), 0)]
    def b_INSTRING(self, s, t): return float(s.find(t) + 1)

    def b_TYPE(self, v):
        if isinstance(v, str): return 2.0
        if isinstance(v, Matrix): return 4.0
        if isinstance(v, list): return 6.0
        return 0.0

    def b_RGB(self, r, g, b, a=0):
        return float((int(r) << 16) | (int(g) << 8) | int(b))

    # ---- graphics builtins ----
    def grob(self, g):
        if not isinstance(g, Grob):
            raise PPLError(f"graphic expected, got {g!r}")
        return g

    def b_DIMGROB_P(self, g, w, h, c=0xFFFFFF):
        g = self.grob(g)
        g.img = Image.new("RGB", (int(w), int(h)), rgb_tuple(c))
        g.draw = ImageDraw.Draw(g.img)

    def b_BLIT_P(self, dst, src):
        self.grob(dst).img.paste(self.grob(src).img, (0, 0))

    def b_RECT_P(self, g, x1, y1, x2, y2, edge, fill=None):
        d = self.grob(g).draw
        box = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
        if fill is None:
            d.rectangle(box, fill=rgb_tuple(edge))
        else:
            d.rectangle(box, fill=rgb_tuple(fill), outline=rgb_tuple(edge))

    def b_LINE_P(self, g, x1, y1, x2, y2, c):
        self.grob(g).draw.line([x1, y1, x2, y2], fill=rgb_tuple(c))

    def b_TRIANGLE_P(self, g, x1, y1, x2, y2, x3, y3, c):
        self.grob(g).draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=rgb_tuple(c))

    def b_TEXTOUT_P(self, s, g, x, y, fnt=0, c=0):
        s = ppl_str(s)
        f = font(fnt)
        w = f.getlength(s)
        self.grob(g).draw.text((x, y), s, font=f, fill=rgb_tuple(c), anchor="la")
        return x + w

    # ---- interaction builtins ----
    def b_WAIT(self, n):
        while self.events:
            ev = self.events.pop(0)
            if isinstance(ev, tuple) and ev[0] == "shot":
                self.shots.append(ev[1])
                self.grobs["G0"].img.save(ev[1])
                continue
            if isinstance(ev, tuple) and ev[0] == "check":
                ev[1](self)
                continue
            self.trace.append(ev)
            return ev
        raise StopSim()

    def dialog(self, kind, vals, cur):
        ev = self.events.pop(0) if self.events else None
        if not (isinstance(ev, tuple) and ev[0] == "dialog"):
            raise PPLError(f"script expected a reply for {kind} {vals[:1]}")
        self.trace.append((kind, vals[0], ev[1]))
        if ev[1] is None:
            return False, cur
        return True, float(ev[1])

    def b_MSGBOX(self, s):
        self.trace.append(("MSGBOX", s))
        return 1.0

    def start(self, name):
        params, body, _ = self.funcs[name]
        try:
            self.run_block(body, {})
        except ReturnSignal:
            pass


# ---------------------------------------------------------------------------
# test script

KEY = {"up": 2, "down": 12, "left": 7, "right": 8, "enter": 30, "esc": 4,
       "plus": 50, "minus": 45, "symb": 1, "num": 11, "help": 3, "plot": 6}


def tap(x, y):
    return [[0, x, y], [2], [3, x, y]]


def drag(points):
    out = [[0] + list(points[0])]
    out += [[1] + list(p) for p in points[1:]]
    return out + [[2]]


def approx(a, b, tol=0.05):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
# tools screen tests: every number is compared with an independent
# calculation (CoolProp, CoolProp humid air, Murphy-Koop ice, gas law)

def rows(it):
    """{label: (value, note)} of the current tool's result rows."""
    out = {}
    for l, v, n in zip(it.g["gRL"], it.g["gRV"], it.g["gRN"]):
        out.setdefault(l, (v, n))
    return out


def num(text):
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(m.group()) if m else None


def set_state(it, ref_name=None, **g):
    names = re.search(r'gRName:=\{(.*?)\};', it.src).group(1).replace('"', "").split(",")
    if ref_name:
        it.g["gRef"] = float(names.index(ref_name) + 1)
    for k, v in g.items():
        if k.startswith("v"):
            it.g["gV"][int(k[1:]) - 1] = float(v)
        else:
            it.g[k] = float(v)
    it.g["gBgRef"] = 0.0


def tool_events(out, check, ref, fn_call):
    import CoolProp.CoolProp as CP

    def f2k(t):
        return (t - 32) / 1.8 + 273.15

    def coolprop_sat_f(fluid, psig, q):
        return (CP.PropsSI("T", "P", (psig + 14.696) * 6894.757, "Q", q, fluid) - 273.15) * 1.8 + 32

    def calc(it, tool):
        fn_call(it, "toolCalc", float(tool))
        return rows(it)

    def full_cooling(it):
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v31=1, v3=80, v4=75, v5=55, v7=180)
        r = calc(it, 1)
        te = coolprop_sat_f("R410A", 118, 1)
        tc = coolprop_sat_f("R410A", 319, 0)
        td = coolprop_sat_f("R410A", 319, 1)
        return (approx(num(r["Superheat"][0]), 50 - te, 0.15)
                and approx(num(r["Subcool"][0]), tc - 90, 0.15)
                and approx(num(r["Disch. SH"][0]), 180 - td, 0.15)
                and approx(num(r["Evap TD"][0]), 75 - te, 0.15)
                and approx(num(r["Cond split"][0]), tc - 80, 0.15)
                and r["Air ΔT"][0] == "20.0°F" and r["Approach"][0] == "10.0°F"
                and r["Comp. ratio"][0] == "2.51 : 1" and it.g["gRV"][-1] == "Readings look normal")

    def full_diagnosis(it):
        # R-22, return 75 F, outdoor 95 F: normal evap TD 30-40, split 10-30
        cases = [  # suction, head, SLT, LLT -> likely
            (55, 200, 60, 99, "Low charge: leak check"),      # SH high, SC low, both pressures low
            (80, 300, 48, 100, "Overcharged"),               # SH low, SC high, both high
            (50, 260, 60, 95, "Restriction: drier/meter"),   # SH high, SC high
            (80, 190, 60, 95, "Weak compressor (valves)"),   # suction high, head low
            (50, 220, 34, 100, "Low indoor airflow"),        # suction low, SH low
            (75, 300, 50, 120, "Dirty condenser / low air"), # head high, SC low
        ]
        for lp, hp, st, lt, want in cases:
            set_state(it, "R-22", gLP=lp, gHP=hp, gST=st, gLT=lt, v31=1, v3=95, v4=75, v5=55, v7=180)
            calc(it, 1)
            if it.g["gRV"][-1] != want:
                print("full check", lp, hp, st, lt, "->", it.g["gRV"][-1], "wanted", want)
                return False
        return True

    def full_heating(it):
        # heat pump heating: outdoor 35 F, return 70 F, supply 95 F
        set_state(it, "R-410A", gLP=90, gHP=380, gST=35, gLT=95, v31=2, v3=35, v4=70, v5=95, v7=190)
        r = calc(it, 1)
        te = coolprop_sat_f("R410A", 90, 1)
        tc = coolprop_sat_f("R410A", 380, 0)
        return (r["Air ΔT"][0] == "25.0°F" and approx(num(r["Evap TD"][0]), 35 - te, 0.15)
                and approx(num(r["Cond split"][0]), tc - 70, 0.15)
                and r["Approach"][0] == "25.0°F")

    def whole_degrees(it):
        # R-410A 118 psig: dew 39.85 F exact, 40 F read from a chart
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v31=1, v3=80, v4=75, v5=55, v7=180, v36=2)
        r = calc(it, 1)
        ok = r["Evap sat"][0] == "40.0°F" and r["Superheat"][0] == "10.0°F" and r["Subcool"][0] == "10.0°F"
        set_state(it, v36=1)
        r = calc(it, 1)
        return ok and r["Superheat"][0] == "10.2°F"

    def charge_fixed(it):
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v1=1, v2=63, v3=95, v30=3, v29=0)
        fn_call(it, "setAtm")
        r = calc(it, 2)
        te = coolprop_sat_f("R410A", 118, 1)
        return (r["Charge"][0] == "ADD refrigerant" and r["Superheat"][1] == "target 7.0"
                and approx(num(r["Superheat"][0]), 50 - te, 0.15)
                and r["Likely"][0] == "Underfeeding: charge/meter")

    def charge_txv(it):
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v1=2, v6=10)
        r = calc(it, 2)
        tc = coolprop_sat_f("R410A", 319, 0)
        ok1 = r["Charge"][0] == "OK" and approx(num(r["Subcooling"][0]), tc - 90, 0.15)
        set_state(it, gLT=95)
        r = calc(it, 2)
        return ok1 and r["Charge"][0] == "ADD refrigerant" and r["Likely"][0] == "Possibly low charge"

    def system(it):
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v3=95, v4=75, v5=55, v7=180)
        r = calc(it, 3)
        te = coolprop_sat_f("R410A", 118, 1)
        tc = coolprop_sat_f("R410A", 319, 0)
        return (approx(num(r["Evap TD"][0]), 75 - te, 0.15)
                and approx(num(r["Cond split"][0]), tc - 95, 0.15)
                and r["Comp. ratio"][0] == "2.51 : 1" and r["Coil ΔT"][0] == "20.0°F")

    def capacity(it):
        set_state(it, v9=1200, v10=3, v4=75, v2=63, v5=55, v8=53, v29=0)
        fn_call(it, "setAtm")
        r = calc(it, 4)
        h = lambda db, wb: CP.HAPropsSI("H", "T", f2k(db), "B", f2k(wb), "P", 101325) / 2326
        tot = 4.5 * 1200 * (h(75, 63) - h(55, 53))
        rh = CP.HAPropsSI("R", "T", f2k(75), "B", f2k(63), "P", 101325) * 100
        sen = 1.08 * 1200 * 20
        return (abs(num(r["Total"][0]) / tot - 1) < 0.015 and abs(num(r["Return air"][0]) - rh) <= 1.5
                and num(r["Sensible"][0]) == round(sen))

    def lineset(it):
        set_state(it, "R-410A", gLT=90, v11=3, v12=25, v13=15, v14=0)
        r = calc(it, 5)
        rho = CP.PropsSI("D", "T", f2k(90), "Q", 0, "R410A") * 0.0624280
        ozft = rho * 3.14159265 * 0.311 ** 2 / 4 * 12 / 1728 * 16
        return (abs(num(r["Charge per ft"][0]) / ozft - 1) < 0.02
                and abs(num(r["Add charge"][0]) / (10 * ozft) - 1) < 0.02)

    def nitrogen(it):
        set_state(it, v15=300, v16=75, v17=70, v18=297, v29=0)
        fn_call(it, "setAtm")
        r = calc(it, 6)
        expected = (300 + 14.696) * (70 + 459.67) / (75 + 459.67) - 14.696
        ok1 = approx(num(r["Expected now"][0]), expected, 0.05) and r["Result"][0] == "HOLDING"
        set_state(it, v18=290)
        r = calc(it, 6)
        return ok1 and r["Result"][0] == "LOST 7.1 psi"

    def vacuum(it):
        set_state(it, v19=500, v20=400, v21=600, v22=10)
        r = calc(it, 7)
        # Murphy & Koop (2005) vapour pressure of ice, solved for 500 microns
        pa = 500 / 1000 * 133.322
        lo, hi = 200.0, 273.16
        for _ in range(60):
            t = (lo + hi) / 2
            p = math.exp(9.550426 - 5723.265 / t + 3.53068 * math.log(t) - 0.00728332 * t)
            lo, hi = (t, hi) if p < pa else (lo, t)
        tf = (t - 273.15) * 1.8 + 32
        return approx(num(r["Water boils"][0]), tf, 0.6) and r["Decay test"][0] == "Rose: moisture?"

    def cylinder(it):
        set_state(it, "R-22", v23=47.7, v24=33, v25=80)
        r = calc(it, 8)
        sg = CP.PropsSI("D", "T", f2k(77), "Q", 0, "R22") * 0.0624280 / 62.4
        mx = 47.7 * 0.8 * sg
        return (abs(num(r["Max refrigerant"][0]) - mx) <= 0.15
                and abs(num(r["Max gross wt"][0]) - (33 + mx)) <= 0.15
                and r["Room left"][1] == "OVERFILLED")

    def info(it):
        set_state(it, "R-410A")
        r = calc(it, 9)
        ok1 = r["Safety class"][0] == "A1" and r["GWP (AR4)"][0] == "2088" and num(r["Glide"][0]) < 0.5
        set_state(it, "R-454B")
        r = calc(it, 9)
        return ok1 and r["Safety class"][0] == "A2L" and r["Charge as"][0] == "liquid only"

    def converter(it):
        set_state(it, v26=1, v27=100, v28=1, v29=0)
        fn_call(it, "setAtm")
        r = calc(it, 10)
        ok1 = r["psia"][0] == "114.7" and r["kPa gauge"][0] == "689.5" and r["bar gauge"][0] == "6.89"
        set_state(it, v26=2, v27=0, v28=2)
        r = calc(it, 10)
        ok2 = r["°F"][0] == "32.00" and r["K"][0] == "273.2" and r["°C"][0] == "0"
        set_state(it, v26=3, v27=1, v28=2)
        r = calc(it, 10)
        return ok1 and ok2 and r["BTU/h"][0] == "12000" and r["kW"][0] == "3.52"

    def settings(it):
        set_state(it, "R-410A", v29=0)
        fn_call(it, "setAtm")
        sea = fn_call(it, "tsat", ref("R-410A"), 118.0, 0.0)
        set_state(it, v29=5000)
        fn_call(it, "setAtm")
        hi = fn_call(it, "tsat", ref("R-410A"), 118.0, 0.0)
        r = calc(it, 11)
        atm = 14.696 * (1 - 6.8754e-6 * 5000) ** 5.2559
        te = (CP.PropsSI("T", "P", (118 + atm) * 6894.757, "Q", 1, "R410A") - 273.15) * 1.8 + 32
        ok = (approx(it.g["gAtm"], atm, 0.005) and approx(hi, te, 0.15) and sea - hi > 1
              and abs(num(r["Water boils"][0]) - 203.0) < 1.0)
        set_state(it, v29=0)
        fn_call(it, "setAtm")
        return ok

    def sat_method(it):
        # a test question: sat 110 F and LLT 100 F give 10 F of subcooling;
        # sat 40 F and SLT 52 F give 12 F of superheat; no pressures used
        set_state(it, "R-410A", gST=52, gLT=100, v37=40, v38=110)
        r = calc(it, 12)
        ok = r["Superheat"][0] == "12.0°F" and r["Subcooling"][0] == "10.0°F"
        p_dew = CP.PropsSI("P", "T", f2k(40), "Q", 1, "R410A") / 6894.757 - 14.696
        p_bub = CP.PropsSI("P", "T", f2k(110), "Q", 0, "R410A") / 6894.757 - 14.696
        ok &= abs(num(r["Suction"][0]) - p_dew) < 0.15 and abs(num(r["Head"][0]) - p_bub) < 0.15
        set_state(it, "R-22", gST=35.5, gLT=96.4, v37=38.2, v38=104.9)
        r = calc(it, 12)
        ok &= r["Superheat"][0] == "-2.7°F" and r["Subcooling"][0] == "8.5°F"
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90, v37=40, v38=110)
        return ok

    def every_refrigerant(it):
        names = re.search(r'gRName:=\{(.*?)\};', it.src).group(1).replace('"', "").split(",")
        for n in names:
            set_state(it, n, gLP=60, gHP=200, gST=50, gLT=90)
            for tool in range(1, 13):
                fn_call(it, "toolCalc", float(tool))
                if not it.g["gRL"]:
                    return False
        set_state(it, "R-410A", gLP=118, gHP=319, gST=50, gLT=90)
        return True

    shot = lambda name: ("shot", os.path.join(out, name))
    return [
        check("full check: cooling readings vs CoolProp", full_cooling),
        check("full check: diagnosis of the six classic faults", full_diagnosis),
        check("full check: heat pump heating mode", full_heating),
        check("settings: whole-degree saturation like a P-T chart", whole_degrees),
        check("charge check: fixed orifice target and verdict", charge_fixed),
        check("charge check: TXV subcooling verdict", charge_txv),
        check("system check: TD, split, ratio, coil dT", system),
        check("capacity check vs CoolProp humid air", capacity),
        check("line set charge vs CoolProp density", lineset),
        check("nitrogen test: gas law and leak verdict", nitrogen),
        check("vacuum: boiling point vs Murphy-Koop ice", vacuum),
        check("recovery cylinder: 80% fill vs CoolProp SG", cylinder),
        check("refrigerant info: class, GWP, glide", info),
        check("unit converter: pressure, temperature, capacity", converter),
        check("settings: altitude correction", settings),
        check("sat temp SH/SC: straight from saturation temps", sat_method),
        check("every tool runs for every refrigerant", every_refrigerant),
        # drive the screens: TOOLS button, pick a tool, edit boxes
        *tap(2 * 64 + 30, 230), ("dialog", 2),
        check("TOOLS opens the charge check", lambda it: it.g["gScr"] == 3 and it.g["gTool"] == 2),
        *tap(100, 30), ("dialog", 2),
        check("tap a choice box", lambda it: it.g["gV"][0] == 2),
        KEY["right"], KEY["up"],
        check("Right selects, Up steps a box", lambda it: it.g["gTSel"] == 2 and it.g["gV"][5] == 11),
        *tap(64 + 30, 230), ("dialog", 10),
        check("EDIT types into the selected box", lambda it: it.g["gV"][5] == 10),
        shot("tool_charge.png"),
        *tap(4 * 64 + 30, 230),
        shot("tool_help.png"),
        KEY["enter"],
        *tap(2 * 64 + 30, 230), ("dialog", 3), shot("tool_system.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 4), shot("tool_capacity.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 5), shot("tool_lineset.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 6), shot("tool_nitrogen.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 7), shot("tool_vacuum.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 8), shot("tool_cylinder.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 9), shot("tool_info.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 10), shot("tool_converter.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 11), shot("tool_settings.png"),
        *tap(2 * 64 + 30, 230), ("dialog", 12),
        *tap(100, 24 + 8), ("dialog", 110),
        check("sat temp tool: type sat suction", lambda it: it.g["gV"][36] == 110 and it.g["gTool"] == 12),
        *tap(100, 24 + 8), ("dialog", 40),
        *tap(100, 44 + 8), ("dialog", 110),
        *tap(260, 44 + 8), ("dialog", 100),
        check("sat temp tool: LLT box moves the gauge screen reading", lambda it: it.g["gLT"] == 100),
        check("sat temp tool: 110 - 100 = 10 F subcooling", lambda it: it.g["gRV"][1] == "10.0°F"),
        shot("tool_sat.png"),
        *tap(4 * 64 + 30, 230),
        shot("tool_sat_help.png"),
        KEY["enter"],
        *tap(2 * 64 + 30, 230), ("dialog", 1),
        *tap(100, 24 + 1 * 21 + 8), ("dialog", 121),
        check("full check: typing suction moves the gauge", lambda it: it.g["gLP"] == 121 and it.g["gTool"] == 1),
        *tap(100, 24 + 5 * 21 + 8), ("dialog", 185),
        check("full check: DLT box", lambda it: it.g["gV"][6] == 185),
        shot("tool_full.png"),
        *tap(4 * 64 + 30, 230),
        shot("tool_full_help.png"),
        KEY["enter"],
        *tap(2 * 64 + 30, 230), ("dialog", 11),
        *tap(100, 30), ("dialog", 5280),
        check("elevation box updates the atmosphere", lambda it: approx(it.g["gAtm"], 12.1, 0.1)),
        *tap(100, 30), ("dialog", 0),
        *tap(3 * 64 + 30, 230),
        check("GAUGES returns to the gauge screen", lambda it: it.g["gScr"] == 1),
        # tap a reading twice to type a value
        KEY["right"], KEY["right"],
        *tap(40, 178), *tap(40, 178), ("dialog", 120),
        check("second tap on a reading types a value", lambda it: it.g["gLP"] == 120 and it.g["gSel"] == 1),
    ]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "hp-prime", "SUPERSUB.txt")
    src = open(path, encoding="utf-8").read()
    names = re.search(r"gRName:=\{(.*?)\};", src).group(1).replace('"', "").split(",")

    def ref(name):
        return float(names.index(name) + 1)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "docs", "screens")
    os.makedirs(out, exist_ok=True)
    checks = []

    def check(desc, fn):
        def run(it):
            ok = fn(it)
            checks.append((desc, ok))
        return ("check", run)

    def fn_call(it, name, *args):
        params, body, _ = it.funcs[name]
        try:
            it.run_block(body, dict(zip(params, args)))
        except ReturnSignal as r:
            return r.value

    ev = [
        ("shot", os.path.join(out, "gauges.png")),
        check("R-410A 118 psig dew = 39.8 F",
              lambda it: approx(fn_call(it, "tsat", ref("R-410A"), 118.0, 0.0), 39.8, 0.1)),
        check("R-410A 40 F bubble = 118.8 psig",
              lambda it: approx(fn_call(it, "psat", ref("R-410A"), 40.0, 1.0), 118.8, 0.1)),
        check("R-407C 63.2 psig dew = 40 F",
              lambda it: approx(fn_call(it, "tsat", ref("R-407C"), 63.2, 0.0), 40.0, 0.1)),
        check("R-134a vacuum -40 F = 14.8 inHg",
              lambda it: approx(-fn_call(it, "psat", ref("R-134a"), -40.0, 0.0) * 2.03602, 14.8, 0.1)),
        check("fmt1 formats", lambda it: [fn_call(it, "fmt1", v) for v in (0.0, -0.04, 9.96, -12.345, 1184.0)]
              == ["0.0", "0.0", "10.0", "-12.3", "1184.0"]),
        # drag the low needle to about 9 o'clock and back up
        *drag([(30, 96), (20, 80), (40, 40)]),
        check("dragging low needle sets pressure", lambda it: it.g["gSel"] == 1 and 60 < it.g["gLP"] < 200),
        # set the high needle by tapping the dial at 12 o'clock -> 400 psig
        *tap(240, 40),
        check("tap high dial at top = 400 psig", lambda it: it.g["gSel"] == 3 and it.g["gHP"] == 400),
        KEY["right"], KEY["up"], KEY["up"],
        check("liquid temp +2 via keys", lambda it: it.g["gSel"] == 4 and it.g["gLT"] == 92),
        KEY["enter"], ("dialog", 95),
        check("typed liquid temp", lambda it: it.g["gLT"] == 95),
        # slider on the suction side
        *drag([(130, 193), (140, 193)]),
        check("suction slider", lambda it: it.g["gSel"] == 2 and it.g["gST"] == round(-40 + 140 * 44 / 58)),
        KEY["left"], KEY["minus"],
        # change refrigerant through the chooser
        *tap(64 * 0 + 30, 230), ("dialog", ref("R-407C")),
        check("refrigerant chooser", lambda it: it.g["gRef"] == ref("R-407C")),
        ("shot", os.path.join(out, "gauges_r407c.png")),
        KEY["help"],
        ("shot", os.path.join(out, "help.png")),
        KEY["enter"],
        # P-T chart
        KEY["num"],
        ("shot", os.path.join(out, "ptchart.png")),
        *drag([(160, 200), (160, 120)]),
        check("drag scrolls chart", lambda it: it.g["gPTTop"] == 35),
        *tap(64 + 30, 230),
        check("step 5", lambda it: it.g["gPTStep"] == 5 and it.g["gPTTop"] == 35),
        *tap(128 + 30, 230), ("dialog", 2), ("dialog", 63.2),
        check("look up pressure highlights 40 F", lambda it: approx(it.g["gFindT"], 40, 0.1) and it.g["gPTTop"] == 15),
        ("shot", os.path.join(out, "ptchart_find.png")),
        KEY["left"], KEY["left"],
        check("left/right changes refrigerant", lambda it: it.g["gRef"] == ref("R-404A")),
        KEY["up"], KEY["up"], KEY["up"], KEY["up"], KEY["up"], KEY["up"], KEY["up"],
        ("shot", os.path.join(out, "ptchart_scroll.png")),
        KEY["esc"],
        check("esc returns to gauges", lambda it: it.g["gScr"] == 1),
        -1,                       # WAIT timeout is ignored
        *tool_events(out, check, ref, fn_call),
        *tap(4 * 64 + 30, 230),   # EXIT
    ]
    it = Interp(src, ev)
    try:
        it.start("SUPERSUB")
        finished = True
    except StopSim:
        finished = False
    checks.append(("EXIT button ends the program", finished))
    checks.append(("angle setting left alone", it.sysvars["HAngle"] == 0))

    # the dials must come out the same whatever the calculator's angle mode
    pics = []
    for mode in (0, 1):
        it.sysvars["HAngle"] = mode
        fn_call(it, "angInit")
        it.g["gBgRef"] = 0
        fn_call(it, "drawMain")
        pics.append(it.grobs["G0"].img.tobytes())
    checks.append(("same picture in radians and degrees mode", pics[0] == pics[1]))

    # draw the gauge screen for every refrigerant into one contact sheet
    sheet = Image.new("RGB", (5 * 320, ((len(names) + 4) // 5) * 240), (0, 0, 0))
    for k, name in enumerate(names):
        it.g["gRef"] = float(k + 1)
        fn_call(it, "drawMain")
        sheet.paste(it.grobs["G0"].img, ((k % 5) * 320, (k // 5) * 240))
    sheet.save(os.path.join(out, "all_refrigerants.png"))
    checks.append((f"gauge screen draws for all {len(names)} refrigerants", True))
    bad = 0
    for desc, ok in checks:
        print(("ok    " if ok else "FAIL  ") + desc)
        bad += not ok
    for t in it.trace:
        if isinstance(t, tuple) and t[0] == "MSGBOX":
            print("MSGBOX:", t[1].replace("\n", " | "))
    print(f"screens written to {out}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
