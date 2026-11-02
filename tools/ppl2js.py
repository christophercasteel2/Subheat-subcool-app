#!/usr/bin/env python3
"""Translate an HP PPL program (hp-prime/*.txt) into JavaScript, so the
same program runs in a web page or an Android app (see tools/android/).

    python3 tools/ppl2js.py hp-prime/CIRCUITS.txt OUT.js

The parser is the one in ppl_sim.py, so the translated program follows the
same rules the simulator tests check.  The JavaScript keeps the PPL
meaning: lists are values (assigning one copies it), list indexes start at
1, AND / OR / IFTE evaluate both sides, a FOR loop counts up to its limit,
and a function without RETURN gives 0.

Functions that can reach WAIT, INPUT, CHOOSE or MSGBOX wait for the user,
so they become async functions and every call to them is awaited; the
rest stay plain functions.  The built-in functions (graphics, dialogs,
maths) come from the runtime object B (tools/android/runtime.js).

The output defines one function:  pplProgram(B) -> {start, g}
start() runs the EXPORTed main function (a Promise); g reads the globals.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppl_sim import Parser, PPLError, check_names, check_order, tokenize, walk_calls  # noqa: E402

BLOCKING = {"WAIT", "INPUT", "CHOOSE", "MSGBOX"}
BUILTINS = {"ABS", "ATAN", "BLIT_P", "CEILING", "CHAR", "CHOOSE", "COS", "DIM", "DIMGROB_P",
            "EXP", "FLOOR", "IFTE", "INPUT", "IP", "LEFT", "LINE_P", "LN", "LOG", "MAX", "MIN",
            "MSGBOX", "RECT_P", "RIGHT", "ROUND", "RGB", "SIN", "SIZE", "TEXTOUT_P",
            "TRIANGLE_P", "TYPE", "WAIT"}
SYSVARS = {"HAngle"}
GROBS = {f"G{k}" for k in range(10)}
CMP = {"==": "===", "=": "===", "<>": "!==", "<": "<", ">": ">", "<=": "<=", ">=": ">="}


def num_lit(v):
    if v == int(v) and abs(v) < 1e15:
        return str(int(v))
    return repr(v)


class Gen:
    def __init__(self, src):
        self.globs, self.funcs = Parser(tokenize(src)).program()
        check_order(self.funcs)
        check_names(self.globs, self.funcs)
        self.gnames = {n for n, _ in self.globs}
        self.async_funcs = self.find_async()
        self.tmp = 0

    def find_async(self):
        calls = {}
        for name, (params, body, _) in self.funcs.items():
            out = []
            walk_calls(body, out)
            calls[name] = {c for c, _ in out}
        sync = set()
        result = {n for n, c in calls.items() if c & BLOCKING}
        changed = True
        while changed:
            changed = False
            for n, c in calls.items():
                if n not in result and c & result:
                    result.add(n)
                    changed = True
        del sync
        return result

    # ---- names ----
    def ref(self, name, scope, line):
        if name in scope:
            return "l_" + name
        if name in self.gnames:
            return "g_" + name
        if name in SYSVARS:
            return "B.sys." + name
        if name in GROBS:
            return f"B.grob({name[1]})"
        raise PPLError(f"line {line}: unknown name {name}")

    def target(self, name, scope, line):
        if name in GROBS:
            raise PPLError(f"line {line}: cannot assign to {name}")
        return self.ref(name, scope, line)

    # ---- expressions ----
    def expr(self, e, scope, in_async):
        k = e[0]
        if k == "num":
            return num_lit(e[1])
        if k == "str":
            return json.dumps(e[1], ensure_ascii=False)
        if k == "var":
            return self.ref(e[1], scope, e[2])
        if k == "neg":
            return f"(-{self.expr(e[1], scope, in_async)})"
        if k == "not":
            return f"(B.truth({self.expr(e[1], scope, in_async)})?0:1)"
        if k == "list":
            return "[" + ",".join(self.expr(x, scope, in_async) for x in e[1]) + "]"
        if k == "mat":
            return "B.mat([" + ",".join(self.expr(x, scope, in_async) for x in e[1]) + "])"
        if k == "bin":
            op = e[1]
            a = self.expr(e[2], scope, in_async)
            b = self.expr(e[3], scope, in_async)
            if op == "+":
                return f"B.add({a},{b})"
            if op in ("-", "*"):
                return f"(B.num({a}){op}B.num({b}))"
            if op == "/":
                return f"B.div({a},{b})"
            if op == "^":
                return f"B.pow({a},{b})"
            if op == "MOD":
                return f"B.mod({a},{b})"
            if op in CMP:
                return f"B.cmp({a},{b},{json.dumps(op)})"
            if op == "AND":
                return f"B.and({a},{b})"
            if op == "OR":
                return f"B.or({a},{b})"
            raise PPLError(f"bad operator {op}")
        if k == "call":
            return self.call(e, scope, in_async)
        raise PPLError(f"bad expression {k}")

    def call(self, e, scope, in_async):
        _, name, args, line = e
        if name in ("INPUT", "CHOOSE"):
            ref = args[0]
            if ref[0] != "var":
                raise PPLError(f"line {line}: {name} needs a variable")
            t = self.target(ref[1], scope, line)
            vals = ",".join(self.expr(a, scope, in_async) for a in args[1:])
            return (f"(await (async()=>{{const r=await B.{name}({t},[{vals}]);"
                    f"if(r.ok){t}=r.val;return r.ret;}})())")
        vals = [self.expr(a, scope, in_async) for a in args]
        if name in scope or name in self.gnames:
            return f"B.idx({self.ref(name, scope, line)},[{','.join(vals)}],{json.dumps(name)},{line})"
        if name in self.funcs:
            params = self.funcs[name][0]
            if len(vals) != len(params):
                raise PPLError(f"line {line}: {name} takes {len(params)} arguments")
            c = f"f_{name}({','.join(vals)})"
            if name in self.async_funcs:
                if not in_async:
                    raise PPLError(f"line {line}: waiting call in a plain function")
                return f"(await {c})"
            return c
        if name not in BUILTINS:
            raise PPLError(f"line {line}: unknown function {name}")
        c = f"B.{name}({','.join(vals)})"
        return f"(await {c})" if name in BLOCKING else c

    # ---- statements ----
    def block(self, stmts, scope, in_async, ind):
        out = []
        for s in stmts:
            out += self.stmt(s, scope, in_async, ind)
        return out

    def stmt(self, s, scope, in_async, ind):
        p = "  " * ind
        k, line = s[0], s[1]
        E = lambda x: self.expr(x, scope, in_async)  # noqa: E731
        if k == "local":
            return [f"{p}l_{n}={'B.cp(' + E(init) + ')' if init else '0'};" for n, init in s[2]]
        if k == "assign":
            return [f"{p}{self.target(s[2], scope, line)}=B.cp({E(s[3])});"]
        if k == "expr":
            return [f"{p}{E(s[2])};"]
        if k == "setidx":
            t = self.target(s[2], scope, line)
            idx = ",".join(E(x) for x in s[3])
            return [f"{p}{t}=B.setIdx({t},[{idx}],{E(s[4])},{json.dumps(s[2])},{line});"]
        if k == "if":
            out = [f"{p}if(B.truth({E(s[2])})){{"] + self.block(s[3], scope, in_async, ind + 1)
            if s[4]:
                out += [f"{p}}}else{{"] + self.block(s[4], scope, in_async, ind + 1)
            return out + [f"{p}}}"]
        if k == "for":
            self.tmp += 1
            v = self.target(s[2], scope, line)
            hi, st = f"t{self.tmp}h", f"t{self.tmp}s"
            return ([f"{p}{{{v}={E(s[3])};const {hi}=B.num({E(s[4])}),{st}=B.num({E(s[5])});",
                     f"{p}while({v}<={hi}+1e-12){{"]
                    + self.block(s[6], scope, in_async, ind + 1)
                    + [f"{p}  {v}={v}+{st};", f"{p}}}}}"])
        if k == "while":
            return ([f"{p}while(B.truth({E(s[2])})){{"] + self.block(s[3], scope, in_async, ind + 1)
                    + [f"{p}}}"])
        if k == "repeat":
            return ([f"{p}do{{"] + self.block(s[2], scope, in_async, ind + 1)
                    + [f"{p}}}while(!B.truth({E(s[3])}));"])
        if k == "return":
            return [f"{p}return {E(s[2]) if s[2] else '0'};"]
        raise PPLError(f"bad statement {k}")

    def locals_of(self, body):
        names = []
        stack = list(body)
        while stack:
            st = stack.pop(0)
            if isinstance(st, tuple) and st and st[0] == "local":
                names += [n for n, _ in st[2]]
            if isinstance(st, (tuple, list)):
                stack.extend(x for x in st if isinstance(x, (tuple, list)))
        return names

    def program(self):
        out = ["function pplProgram(B){", '"use strict";']
        for n, _ in self.globs:
            out.append(f"let g_{n}=0;")
        main = None
        for name, (params, body, exported) in self.funcs.items():
            if exported:
                main = name
            is_async = name in self.async_funcs or exported
            scope = set(params) | set(self.locals_of(body))
            if exported and name not in self.async_funcs:
                self.async_funcs.add(name)
            loc = sorted(set(self.locals_of(body)) - set(params))
            out.append(f"{'async ' if is_async else ''}function f_{name}("
                       + ",".join("l_" + x for x in params) + "){")
            if loc:
                out.append("  let " + ",".join(f"l_{x}=0" for x in loc) + ";")
            out += self.block(body, scope, is_async, 1)
            out.append("  return 0;")
            out.append("}")
        for n, e in self.globs:
            out.append(f"g_{n}=B.cp({self.expr(e, set(), False)});")
        if main is None:
            raise PPLError("no EXPORT function")
        names = sorted(self.gnames)
        getters = ",".join(f"{json.dumps(n)}:()=>g_{n}" for n in names)
        setters = ",".join(f"{json.dumps(n)}:(v)=>{{g_{n}=v;}}" for n in names)
        funcs = ",".join(f"{json.dumps(n)}:f_{n}" for n in self.funcs)
        out.append(f"return {{name:{json.dumps(main)},start:f_{main},get:{{{getters}}},"
                   f"set:{{{setters}}},funcs:{{{funcs}}}}};")
        out.append("}")
        return "\n".join(out) + "\n"


def translate(src):
    return Gen(src).program()


def main():
    src = open(sys.argv[1], encoding="utf-8").read()
    js = translate(src)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w", encoding="utf-8").write(js)
    else:
        sys.stdout.write(js)


if __name__ == "__main__":
    main()
