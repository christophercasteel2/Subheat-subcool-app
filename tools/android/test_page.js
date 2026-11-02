// Plays an app page (android/web/NAME.html) in headless Chromium on a
// phone-sized screen: taps on the calculator screen, keypad presses and
// the INPUT / CHOOSE dialogs, and saves screenshots.
//   node tools/android/test_page.js NAME OUTDIR
"use strict";
const { chromium } = require("playwright");
const path = require("path");
const name = process.argv[2] || "CIRCUITS";
const out = process.argv[3] || ".";
const file = path.resolve(__dirname, "..", "..", "android", "web", name + ".html");

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 412, height: 860 }, deviceScaleFactor: 2.625,
    isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  await page.goto("file://" + file);
  await page.waitForFunction(() => window.PPL && window.PPL.prog);
  await page.waitForTimeout(400);
  const g = (n) => page.evaluate((n) => window.PPL.prog.get[n](), n);
  const box = await page.locator("#scr").boundingBox();
  const tap = async (x, y) => {
    await page.mouse.click(box.x + (x + 0.5) * box.width / 320, box.y + (y + 0.5) * box.height / 240);
    await page.waitForTimeout(120);
  };
  const key = async (label) => {
    await page.locator("#pad button", { hasText: new RegExp("^" + label.replace(/[.+]/g, "\\$&") + "$") }).dispatchEvent("pointerdown");
    await page.locator("#pad button", { hasText: new RegExp("^" + label.replace(/[.+]/g, "\\$&") + "$") }).dispatchEvent("pointerup");
    await page.waitForTimeout(80);
  };
  const shot = (n) => page.screenshot({ path: path.join(out, n) });
  const checks = [];
  const check = (d, ok) => { checks.push([d, ok]); console.log((ok ? "ok    " : "FAIL  ") + d); };

  await shot(name.toLowerCase() + "_phone_home.png");
  check("starts on the tiles", (await g("gScr")) === 1);
  if (name === "CIRCUITS") {
    await tap(200, 45);                          // tile 3, series-parallel
    check("tap opens Series-parallel", (await g("gScr")) === 2 && (await g("gTool")) === 3);
    await shot("circuits_phone_tool.png");
    await tap(110, 23 + 3 * 19 + 9);             // R2 box -> INPUT dialog
    check("INPUT dialog opens", await page.locator("#ov.on").isVisible());
    await shot("circuits_phone_input.png");
    await page.locator("#body input").fill("390");
    await page.locator("#btns button.ok").click();
    await page.waitForTimeout(120);
    check("dialog sets R2 = 390", (await g("gV"))[21] === 390);
    await key("▶"); await key("1"); await key("."); await key("5"); await key("Enter");
    check("keypad types R3 = 1.5", (await g("gV"))[22] === 1.5);
    await tap(30, 230);                          // EDIT on R3 (number) then cancel
    await page.locator("#btns button", { hasText: "Cancel" }).click();
    await tap(94, 230);                          // RESET
    check("RESET", (await g("gV"))[21] === 360);
    await key("Menu");                           // tools list (CHOOSE)
    check("Menu opens the tools list", await page.locator("#ov.on .item").count() === 12);
    await shot("circuits_phone_choose.png");
    await page.locator("#ov .item", { hasText: "Troubleshoot" }).click();
    await page.waitForTimeout(150);
    check("picked Troubleshoot", (await g("gTool")) === 5);
    await shot("circuits_phone_trouble.png");
    const rv = await g("gRV");
    check("answer R1 is OPEN", rv.includes("R1 is OPEN"));
    await page.evaluate(() => window.pplBack());   // Android back = Esc
    await page.waitForTimeout(120);
    check("Back goes home", (await g("gScr")) === 1);
    await page.setViewportSize({ width: 860, height: 412 });
    await page.waitForTimeout(200);
    await shot("circuits_phone_landscape.png");
  }
  check("no page errors " + errors.join(" | "), errors.length === 0);
  await browser.close();
  process.exit(checks.every((c) => c[1]) ? 0 : 1);
})();
