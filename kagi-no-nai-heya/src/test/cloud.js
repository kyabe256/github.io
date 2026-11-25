// node test3/cloud.js : saves reach the account store and come back after the browser storage is wiped
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const store = {}; let errs = 0;
  const ctx = await b.newContext({ viewport: { width: 1600, height: 900 } });
  await ctx.exposeFunction('__dbGet', p => store[p] || null);
  await ctx.exposeFunction('__dbSet', (p, d) => { store[p] = d; return true; });
  await ctx.addInitScript(() => { window.claude = { use: async n => n === 'user' ? { id: async () => 'u1' } : n === 'db' ? { doc: path => ({ get: async () => { const d = await window.__dbGet(path); return { exists: !!d, data: () => d || undefined }; }, set: async d => { await window.__dbSet(path, JSON.parse(JSON.stringify(d))); } }) } : null }; });
  const p = await ctx.newPage(); p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  await p.goto('http://127.0.0.1:8767/index.html'); await p.waitForTimeout(500);
  await p.evaluate(() => { __g.fast(true); __g.start('012', false); }); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(800, 300);
  await p.waitForFunction(() => !__g.busy && __g.mode === 'free', null, { timeout: 60000 });
  const h = (await p.evaluate(() => __g.hs()))[0]; await p.mouse.click(h.x, h.y); await p.waitForFunction(() => !__g.busy && __g.mode === 'free', null, { timeout: 60000 });
  await p.waitForTimeout(5500);
  console.log('cloud state', await p.evaluate(() => __g.cloud), 'docs', Object.keys(store).join(' '));
  await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(1500);
  console.log('title offers:', await p.evaluate(() => { const c = document.querySelector('#t-cont'); return c.hidden ? '(hidden)' : c.textContent; }));
  await p.click('#t-cont'); await p.waitForFunction(() => __g.G && !__g.busy && __g.mode === 'free', null, { timeout: 30000 });
  console.log('restored seen:', JSON.stringify(await p.evaluate(() => Object.keys(__g.G.seen))), 'loc', await p.evaluate(() => __g.G.loc), 'errors', errs);
  await p.click('#t-set2'); await p.waitForTimeout(300); await p.screenshot({ path: 'test3/std/settings.png' });
  await b.close();
})().catch(e => { console.log('FAIL', e.message); process.exit(1); });
