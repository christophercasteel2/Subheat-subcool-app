// Runs a translated PPL program in Node with scripted events, for
// tools/test_android.py.  Reads a JSON job on stdin:
//   {program: "...js...", events: [...], replies: [...], widths: {size: {char: w}}}
// and prints the globals as JSON when the events run out or the program ends.
"use strict";
const { makeRuntime } = require("./runtime.js");
const job = JSON.parse(require("fs").readFileSync(0, "utf8"));

class Stop extends Error {}
function fakeCanvas(w, h) {
  const ctx = {
    font: "10px x", setTransform() {}, fillRect() {}, save() {}, restore() {}, drawImage() {},
    beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, closePath() {}, fill() {}, fillText() {},
    measureText(s) {
      const size = parseInt(this.font, 10);
      const tab = job.widths[size] || {};
      let w = 0;
      for (const ch of s) w += tab[ch] !== undefined ? tab[ch] : size * 0.55;
      return { width: w };
    },
  };
  return { width: w, height: h, getContext: () => ctx };
}
let ev = 0, rp = 0, dialogs = 0;
const pickReply = () => (rp < job.replies.length ? job.replies[rp++] : null);
const host = {
  scale: 1,
  screen: fakeCanvas(320, 240),
  newCanvas: fakeCanvas,
  nextEvent: () => (ev < job.events.length ? Promise.resolve(job.events[ev++]) : Promise.reject(new Stop())),
  msgbox: () => Promise.resolve(),
  choose: (title, items, cur) => {
    dialogs++;
    const r = pickReply();
    if (r === null) return Promise.resolve(0);
    return Promise.resolve(1 + Math.floor(r * items.length));
  },
  input: (title, label, help, cur) => {
    dialogs++;
    const r = pickReply();
    if (r === null) return Promise.resolve(null);
    const vals = job.input_values;
    return Promise.resolve(vals[Math.floor(r * vals.length)]);
  },
};
const B = makeRuntime(host);
const prog = new Function("B", job.program + "\nreturn pplProgram(B);")(B);
function dump(status, msg) {
  const g = {};
  for (const [k, get] of Object.entries(prog.get)) {
    const v = get();
    g[k] = Array.isArray(v) ? JSON.parse(JSON.stringify(v)) : v;
  }
  process.stdout.write(JSON.stringify({ status, msg, events: ev, dialogs, g }));
}
prog.start().then(() => dump("ended"), (e) => {
  if (e instanceof Stop) dump("stopped");
  else dump("error", String(e && e.stack || e));
});
