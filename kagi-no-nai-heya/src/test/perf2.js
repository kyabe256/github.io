// node test3/perf2.js : CPU spent on style, layout, paint and raster per second in each state (1024x768 @2x)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1024, height: 768 }, deviceScaleFactor: 2 }); p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto('http://127.0.0.1:8767/index.html'); await p.evaluate(s => localStorage.setItem('kagi-no-nai-heya-1', s), fs.readFileSync('test3/run3/pre.json', 'utf8')); await p.reload(); await p.waitForTimeout(500);
  if (process.argv[2]) await p.evaluate(q => { localStorage.setItem('kagi-no-nai-heya-opt', JSON.stringify({ q })); }, process.argv[2]), await p.reload(), await p.waitForTimeout(500);
  const trace = async (label, ms) => { await b.startTracing(p, { categories: ['devtools.timeline', 'cc', 'disabled-by-default-devtools.timeline'] }); await p.waitForTimeout(ms); const ev = JSON.parse((await b.stopTracing()).toString()).traceEvents; const sum = {}; for (const e of ev) if (e.ph === 'X' && e.dur) sum[e.name] = (sum[e.name] || 0) + e.dur / 1000;
    const g = k => Math.round((sum[k] || 0) / (ms / 1000)); console.log(label.padEnd(9), 'per second ms:', 'style', g('UpdateLayoutTree'), 'layout', g('Layout'), 'paint', g('Paint'), 'raster', g('RasterTask'), 'script', g('FunctionCall') + g('FireAnimationFrame') + g('TimerFire'), 'layerize', g('Layerize') + g('UpdateLayerTree'), '| total', g('UpdateLayoutTree') + g('Layout') + g('Paint') + g('RasterTask') + g('Layerize') + g('UpdateLayerTree')); };
  await trace('title', 3000);
  await p.click('#t-cont'); await p.waitForTimeout(1500); await trace('soukan', 3000);
  await p.click('#a-map'); await p.click('.node[data-loc="living"]'); await p.waitForTimeout(2500); await trace('living', 3000);
  await p.locator('#people .chip').first().click(); await p.waitForSelector('#choice'); await p.locator('#choice button').first().click(); await p.waitForTimeout(600); await trace('dialogue', 3000);
  await b.close(); })().catch(e => { console.log('FAIL', e.message); process.exit(1); });
