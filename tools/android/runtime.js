// Runtime for HP PPL programs translated by tools/ppl2js.py: the language
// rules (1-based lists that are values, numbers and strings), the maths
// built-ins, the graphics built-ins on HTML canvases, and WAIT / INPUT /
// CHOOSE / MSGBOX through the host page.
//
// makeRuntime(host) -> B.  The host gives:
//   scale              device pixels per calculator pixel
//   newCanvas(w, h)    a canvas of w x h device pixels
//   screen             the visible canvas (the calculator's G0)
//   nextEvent()        Promise of the next key code or touch list
//   choose(title, items, cur)        Promise of the picked index, or 0
//   input(title, label, help, cur)   Promise of a number, or null
//   msgbox(text)       Promise, resolved when dismissed
// It follows tools/ppl_sim.py, which the program tests run against.
"use strict";

function makeRuntime(host) {
  const S = host.scale;
  const B = {};
  const err = (m) => new Error(m);

  // ---- values ----
  B.num = (v) => {
    if (typeof v === "number") return v;
    throw err("number expected, got " + B.str(v));
  };
  B.truth = (v) => {
    if (typeof v === "number") return v !== 0;
    throw err("condition is not a number: " + B.str(v));
  };
  B.mat = (items) => { items.mat = true; return items; };
  B.cp = (v) => {
    if (Array.isArray(v)) { const c = v.slice(); if (v.mat) c.mat = true; return c; }
    return v;
  };
  // numbers as text: whole numbers without a decimal point, others as
  // Python's repr (the simulator's), e.g. 0.1, 1e-05, 1.5e+16
  B.str = (v) => {
    if (typeof v === "string") return v;
    if (typeof v === "number") {
      if (Number.isInteger(v)) return Math.abs(v) < 1e21 ? String(v) : BigInt(v).toString();
      if (!isFinite(v)) return isNaN(v) ? "nan" : (v > 0 ? "inf" : "-inf");
      const ex = v.toExponential();               // shortest digits
      const m = /^(-?)(\d)(?:\.(\d+))?e([+-]\d+)$/.exec(ex);
      const sign = m[1], digits = m[2] + (m[3] || ""), e = parseInt(m[4], 10);
      if (e >= -4 && e < 16) {
        if (e < 0) return sign + "0." + "0".repeat(-e - 1) + digits;
        if (digits.length <= e + 1) return sign + digits + "0".repeat(e + 1 - digits.length) + ".0";
        return sign + digits.slice(0, e + 1) + "." + digits.slice(e + 1);
      }
      const mant = digits.length > 1 ? digits[0] + "." + digits.slice(1) : digits;
      const es = Math.abs(e) < 10 ? "0" + Math.abs(e) : String(Math.abs(e));
      return sign + mant + "e" + (e < 0 ? "-" : "+") + es;
    }
    if (Array.isArray(v)) return "[" + v.map(B.str).join(", ") + "]";
    return String(v);
  };
  B.add = (a, b) => {
    if (typeof a === "string" || typeof b === "string") return B.str(a) + B.str(b);
    return B.num(a) + B.num(b);
  };
  B.div = (a, b) => {
    if (B.num(b) === 0) throw err("division by zero");
    return B.num(a) / b;
  };
  B.pow = (a, b) => Math.pow(B.num(a), B.num(b));
  B.mod = (a, b) => B.num(a) - B.num(b) * Math.floor(a / b);
  B.cmp = (a, b, op) => {
    if ((op === "==" || op === "=" || op === "<>") && typeof a === "string" && typeof b === "string") {
      return ((a === b) === (op !== "<>")) ? 1 : 0;
    }
    a = B.num(a); b = B.num(b);
    switch (op) {
      case "==": case "=": return a === b ? 1 : 0;
      case "<>": return a !== b ? 1 : 0;
      case "<": return a < b ? 1 : 0;
      case ">": return a > b ? 1 : 0;
      case "<=": return a <= b ? 1 : 0;
      default: return a >= b ? 1 : 0;
    }
  };
  B.and = (a, b) => (B.num(a) !== 0 && B.num(b) !== 0) ? 1 : 0;
  B.or = (a, b) => (B.num(a) !== 0 || B.num(b) !== 0) ? 1 : 0;
  B.idx = (obj, ixs, name, line) => {
    for (const ix of ixs) {
      if (!Array.isArray(obj) && typeof obj !== "string") throw err(`line ${line}: ${name} is not a list`);
      const k = Math.trunc(ix);
      if (k !== ix || k < 1 || k > obj.length) throw err(`line ${line}: ${name}: bad index ${B.str(ix)}`);
      obj = obj[k - 1];
    }
    return obj;
  };
  B.setIdx = (obj, ixs, val, name, line) => {
    if (!Array.isArray(obj)) throw err(`line ${line}: ${name} is not a list`);
    const top = obj.map(B.cp);
    if (obj.mat) top.mat = true;
    let t = top;
    ixs.forEach((ix, depth) => {
      const last = depth === ixs.length - 1;
      const k = Math.trunc(ix);
      if (k !== ix || k < 1 || k > t.length + (last ? 1 : 0)) throw err(`line ${line}: ${name}: bad index ${B.str(ix)}`);
      if (last) t[k - 1] = val;          // storing at SIZE+1 appends
      else t = t[k - 1];
    });
    return top;
  };

  // ---- maths ----
  B.sys = { HAngle: 0 };
  const angIn = (a) => B.sys.HAngle === 1 ? a * Math.PI / 180 : a;
  B.SIN = (a) => Math.sin(angIn(a));
  B.COS = (a) => Math.cos(angIn(a));
  B.ATAN = (x) => { const r = Math.atan(x); return B.sys.HAngle === 1 ? r * 180 / Math.PI : r; };
  B.LN = (x) => { if (x <= 0) throw err("LN of " + B.str(x)); return Math.log(x); };
  B.LOG = (x) => { if (x <= 0) throw err("LOG of " + B.str(x)); return Math.log10(x); };
  B.EXP = (x) => Math.exp(x);
  B.ABS = (x) => Math.abs(x);
  B.IP = (x) => Math.trunc(x);
  B.FLOOR = (x) => Math.floor(x);
  B.CEILING = (x) => Math.ceil(x);
  B.ROUND = (x, n = 0) => {
    const m = Math.pow(10, Math.trunc(n));
    const r = Math.floor(Math.abs(x) * m + 0.5) / m;
    return x < 0 ? -r : r;
  };
  B.MAX = (a, b) => Math.max(B.num(a), B.num(b));
  B.MIN = (a, b) => Math.min(B.num(a), B.num(b));
  B.IFTE = (c, a, b) => (B.truth(c) ? a : b);
  B.CHAR = (c) => String.fromCharCode(Math.trunc(c));
  B.DIM = (s) => s.length;
  B.SIZE = (s) => s.length;
  B.LEFT = (s, n) => s.slice(0, Math.max(0, Math.trunc(n)));
  B.RIGHT = (s, n) => (Math.trunc(n) > 0 ? s.slice(Math.max(0, s.length - Math.trunc(n))) : "");
  B.TYPE = (v) => (typeof v === "string" ? 2 : Array.isArray(v) ? (v.mat ? 4 : 6) : 0);
  B.RGB = (r, g, b) => ((Math.trunc(r) << 16) | (Math.trunc(g) << 8) | Math.trunc(b));

  // ---- graphics: G0 is the screen, G1-G9 are off-screen ----
  const css = new Map();
  const color = (c) => {
    c = Math.trunc(c);
    let s = css.get(c);
    if (!s) { s = "rgb(" + ((c >> 16) & 255) + "," + ((c >> 8) & 255) + "," + (c & 255) + ")"; css.set(c, s); }
    return s;
  };
  function makeGrob(canvas, w, h) {
    const g = { c: canvas, w, h, x: canvas.getContext("2d") };
    g.x.setTransform(S, 0, 0, S, 0, 0);
    return g;
  }
  const grobs = [makeGrob(host.screen, 320, 240)];
  for (let k = 1; k < 10; k++) grobs.push(makeGrob(host.newCanvas(320 * S, 240 * S), 320, 240));
  B.grob = (k) => grobs[k];
  const G = (g) => { if (!g || !g.x) throw err("graphic expected"); return g; };

  B.DIMGROB_P = (g, w, h, c = 0xFFFFFF) => {
    g = G(g);
    g.c.width = Math.round(w * S);
    g.c.height = Math.round(h * S);
    g.w = w; g.h = h;
    g.x = g.c.getContext("2d");
    g.x.setTransform(S, 0, 0, S, 0, 0);
    g.x.fillStyle = color(c);
    g.x.fillRect(0, 0, w, h);
    return 0;
  };
  B.BLIT_P = (dst, src) => {
    dst = G(dst); src = G(src);
    dst.x.save();
    dst.x.setTransform(1, 0, 0, 1, 0, 0);
    dst.x.drawImage(src.c, 0, 0);
    dst.x.restore();
    return 0;
  };
  // like Pillow: the corners are both inside the rectangle
  B.RECT_P = (g, x1, y1, x2, y2, edge, fill) => {
    const x = G(g).x;
    const l = Math.min(x1, x2), t = Math.min(y1, y2), r = Math.max(x1, x2), b = Math.max(y1, y2);
    x.fillStyle = color(edge);
    x.fillRect(l, t, r - l + 1, b - t + 1);
    if (fill !== undefined && r - l >= 2 && b - t >= 2) {
      x.fillStyle = color(fill);
      x.fillRect(l + 1, t + 1, r - l - 1, b - t - 1);
    }
    return 0;
  };
  B.LINE_P = (g, x1, y1, x2, y2, c) => {
    const x = G(g).x;
    if (y1 === y2 || x1 === x2) {
      x.fillStyle = color(c);
      x.fillRect(Math.min(x1, x2), Math.min(y1, y2), Math.abs(x2 - x1) + 1, Math.abs(y2 - y1) + 1);
      return 0;
    }
    x.strokeStyle = color(c);
    x.lineWidth = 1;
    x.lineCap = "square";
    x.beginPath();
    x.moveTo(x1 + 0.5, y1 + 0.5);
    x.lineTo(x2 + 0.5, y2 + 0.5);
    x.stroke();
    return 0;
  };
  B.TRIANGLE_P = (g, x1, y1, x2, y2, x3, y3, c) => {
    const x = G(g).x;
    x.fillStyle = color(c);
    x.beginPath();
    x.moveTo(x1 + 0.5, y1 + 0.5);
    x.lineTo(x2 + 0.5, y2 + 0.5);
    x.lineTo(x3 + 0.5, y3 + 0.5);
    x.closePath();
    x.fill();
    return 0;
  };
  // font n is Liberation Sans at 8 + 2n pixels (n = 0 means 3), drawn
  // from the top of the letters, as in the simulator
  const FONT = host.fontFamily || "PPLSans, Arial, sans-serif";
  B.TEXTOUT_P = (s, g, x, y, fnt = 0, c = 0) => {
    s = B.str(s);
    const ctx = G(g).x;
    const size = 8 + 2 * (Math.trunc(fnt) || 3);
    ctx.font = size + "px " + FONT;
    if ("fontKerning" in ctx) ctx.fontKerning = "none";
    ctx.fillStyle = color(c);
    ctx.textBaseline = "alphabetic";
    ctx.fillText(s, x, y + Math.ceil(0.905 * size - 0.001));
    return x + ctx.measureText(s).width;
  };

  // ---- the user ----
  B.WAIT = () => host.nextEvent();
  B.MSGBOX = async (s) => { await host.msgbox(B.str(s)); return 1; };
  B.CHOOSE = async (cur, args) => {
    const items = (args.length === 2 && Array.isArray(args[1])) ? args[1] : args.slice(1);
    const k = await host.choose(B.str(args[0]), items.map(B.str), typeof cur === "number" ? cur : 1);
    return k >= 1 ? { ok: true, val: k, ret: k } : { ok: false, ret: 0 };
  };
  B.INPUT = async (cur, args) => {
    const v = await host.input(B.str(args[0] || ""), B.str(args[1] || ""), B.str(args[2] || ""), cur);
    return v === null || v === undefined ? { ok: false, ret: 0 } : { ok: true, val: v, ret: 1 };
  };
  return B;
}

if (typeof module !== "undefined") module.exports = { makeRuntime };
