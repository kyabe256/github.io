// node test/look.js : pictures of the talking, menu, notebook and settings screens at a tablet size
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1180, height: 760 } }); p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto('http://127.0.0.1:8770/index.html'); await p.waitForFunction(() => window.__g); await p.waitForTimeout(500); await p.screenshot({ path: 'out/l-title.png' });
  await p.click('#t-new'); await p.waitForTimeout(4200); await p.mouse.click(500, 300); await p.waitForTimeout(2500); await p.screenshot({ path: 'out/l-dlg.png' });
  await p.evaluate(() => __g.fast(true)); for (let i = 0; i < 60; i++){ await p.mouse.click(500, 300); await p.waitForTimeout(40); if (await p.evaluate(() => __g.mode === 'drive' && !__g.busy)) break; }
  await p.waitForFunction(() => __g.mode === 'drive' && !__g.busy, null, { timeout: 20000 }); await p.evaluate(() => { __g.fast(false); }); await p.locator('#dv-panel .big', { hasText: '走り出す' }).click(); await p.waitForTimeout(5000); await p.screenshot({ path: 'out/l-drive.png' });
  await p.evaluate(() => { __g.fast(true); const G = __g.G; G.F.met_akari = 1; G.F.body_done = 1; G.scene = 'forest'; G.x = 2610; G.mode = 'walk'; __g.enterWalk(); __g.fast(false); }); await p.waitForTimeout(900); await p.click('#w-act'); await p.waitForTimeout(700); await p.screenshot({ path: 'out/l-menu.png' });
  await p.locator('#menu .big.alt').click(); await p.waitForTimeout(400); await p.evaluate(() => { __g.addEv('e_dash'); __g.addFact('f_rencar'); }); await p.click('#h-note'); await p.waitForTimeout(500); await p.screenshot({ path: 'out/l-note.png' }); await p.click('#note .x'); await p.waitForTimeout(400);
  await p.click('#h-set'); await p.waitForTimeout(500); await p.screenshot({ path: 'out/l-set.png' }); await b.close(); })();
