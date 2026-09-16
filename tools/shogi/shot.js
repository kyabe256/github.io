// デバッグ用: HTML を B5 幅で表示してスクリーンショットを撮る。
// usage: node shot.js <html> <out.png> [full|<y>]
const { chromium } = require('playwright');
(async () => {
  const [, , input, output, mode] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 688, height: 972 }, deviceScaleFactor: 2 });
  await page.goto('file://' + input, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);
  if (mode === 'full') await page.screenshot({ path: output, fullPage: true });
  else await page.screenshot({ path: output, clip: { x: 0, y: Number(mode || 0), width: 688, height: 972 } });
  await browser.close();
})();
