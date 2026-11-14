// node render.js pdf in.html out.pdf [footer-title]   |   node render.js figs in.html outdir
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [mode, src, out, title] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);
  if (mode === 'pdf') {
    const foot = title
      ? `<div style="width:100%;font-family:Inter,sans-serif;font-size:10px;color:#5a6278;padding:0 0.85in;display:flex;justify-content:space-between;">
           <span>${title}</span><span style="font-weight:700;font-size:12px;color:#1c2440"><span class="pageNumber"></span></span></div>`
      : '<span></span>';
    await page.pdf({
      path: out, format: 'Letter', printBackground: true, displayHeaderFooter: !!title,
      headerTemplate: '<span></span>', footerTemplate: foot,
      margin: title ? { top: '0.75in', bottom: '0.85in', left: '0.85in', right: '0.85in' } : { top: 0, bottom: 0, left: 0, right: 0 },
    });
  } else if (mode === 'figs') {
    const els = await page.$$('div.f');
    for (let i = 0; i < els.length; i++) {
      await els[i].screenshot({ path: path.join(out, 'fig' + String(i).padStart(3, '0') + '.png') });
    }
  } else if (mode === 'png') {
    await page.setViewportSize({ width: 816, height: 1056 });
    await page.screenshot({ path: out, fullPage: false });
  }
  await browser.close();
})();
