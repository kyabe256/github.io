// HTML を Chromium で B5 の PDF に印刷する。
// usage: node render.js <input.html> <output.pdf>
const { chromium } = require('playwright');

(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  const style = (s) =>
    `<style>
       * { -webkit-print-color-adjust: exact; }
       .w { width: 100%; font-family: 'Noto Serif JP', serif; font-size: 7.4pt;
            color: #6b7280; padding: 0 17mm; display: flex; }
     </style>${s}`;

  await page.pdf({
    path: output,
    preferCSSPageSize: true,
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: style('<div class="w"></div>'),
    footerTemplate: style(
      '<div class="w" style="justify-content:center;align-items:flex-start">' +
      '<span class="pageNumber" style="font-variant-numeric:tabular-nums"></span></div>'),
  });
  await browser.close();
})();
