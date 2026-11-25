// wrong paths from the pre-report save: bad ending, gauge loss, near, break, hints, small screen
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const out = 'test3/wr'; fs.mkdirSync(out, { recursive: true }); let errs = 0;
  const open = async (vp) => { const p = await b.newPage({ viewport: vp || { width: 1600, height: 900 } }); p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message, (e.stack || '').split('\n')[1]); }); await p.goto('http://127.0.0.1:8767/index.html'); await p.evaluate(s => localStorage.setItem('kagi-no-nai-heya-1', s), fs.readFileSync('test3/run2/pre.json', 'utf8')); await p.reload(); await p.waitForTimeout(400); await p.click('#t-cont'); await p.evaluate(() => __g.fast(true)); await p.waitForTimeout(500); return p; };
  const idle = p => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden)), null, { timeout: 60000 });
  const fill = async (p, ans) => { await p.click('#a-rep'); for (const k in ans){ const r = p.locator(`.fr:has(.sp[data-k="${k}"])`); await r.locator(`.op button[data-v="${ans[k]}"]`).click(); } await p.click('#r-go'); await p.click('#r-go'); };
  const present = async (p, st, i, item, kind) => { await p.click(`.st[data-id="${st}"] span[data-i="${i}"]`); await p.click('#i-pres'); await p.click(`#pick .tabs button[data-t="${kind}"]`); await p.click(`#pick .pc[data-id="${item}"]`); await p.click('#p-ok'); await p.waitForTimeout(100); await p.waitForFunction(() => document.querySelector('#choice') || document.querySelector('#res') || (!__g.busy && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden))), null, { timeout: 60000 }); };
  // 1. accuse Cole -> bad ending -> rewrite
  let p = await open(); await fill(p, { doer: 'cole', mole: 'cole', boss: 'cole', entry: 'app', camera: 'broken', weapon: 'tub', motive: 'money' }); await p.waitForSelector('#res', { timeout: 60000 }); await p.waitForTimeout(900); await p.screenshot({ path: out + '/bad.png' }); console.log('bad', JSON.stringify(await p.evaluate(() => __res)));
  await p.click('#rs-re'); await p.waitForTimeout(300); await idle(p); console.log('after rewrite', await p.evaluate(() => [__g.G.wrongRep, __g.G.loc, __g.mode].join()));
  // 2. right mole, wrong doer -> C interrogation with misses, near, break, retry -> normal end
  await fill(p, { doer: 'cole', mole: 'mashiba', boss: 'unknown', entry: 'master', camera: 'swap', weapon: 'board', motive: 'brother' }); await p.waitForTimeout(300); await idle(p);
  await present(p, 'c_s2', 0, 'f_gateM', 'fact'); console.log('near gauge', await p.evaluate(() => __g.G.intr.C.g));
  await present(p, 'c_s2', 1, 'h_alibi', 'hyp'); console.log('wrong phrase gauge', await p.evaluate(() => __g.G.intr.C.g));
  for (let i = 0; i < 5; i++){ if (await p.evaluate(() => __g.mode) !== 'intr') break; await present(p, 'c_s1', 0, 'lock', 'ev'); console.log('miss', i, await p.evaluate(() => [__g.G.intr.C.g, __g.G.miss, __g.G.brk, __g.mode].join())); }
  await idle(p); console.log('after break loc', await p.evaluate(() => [__g.G.loc, __g.mode].join()));
  await p.click('#a-map'); await p.click('.node[data-loc="renraku"]').catch(() => p.click('#map .x')); await p.waitForTimeout(200); await idle(p);
  await p.locator('#people .chip').first().click(); await p.waitForSelector('#choice'); await p.locator('#choice button.hot').click(); await p.waitForTimeout(200); await idle(p);
  for (const a of [['c_s2', 0, 'h_alibi', 'hyp'], ['c_s3', 2, 'h_same', 'hyp'], ['c_s4', 0, 'h_three', 'hyp'], ['c_s5', 1, 'slip', 'ev'], ['c_s6', 1, 'h_trade', 'hyp']]) await present(p, ...a);
  await p.waitForSelector('#choice'); await p.locator('#choice button').nth(1).click(); await p.waitForSelector('#res', { timeout: 60000 }); await p.waitForTimeout(900); await p.screenshot({ path: out + '/normal.png' }); console.log('normal', JSON.stringify(await p.evaluate(() => __res)));
  await p.close();
  // 3. hints on, dialogue look, small screens
  p = await open(); await p.evaluate(() => __g.fast(false)); await p.click('#t-set2'); await p.click('.seg[data-k="hint"] button[data-v="1"]'); await p.click('#set .x'); await p.click('#a-map'); await p.click('.node[data-loc="living"]'); await p.waitForTimeout(1200); await p.evaluate(() => { __g.G.seen = {}; }); await p.click('#a-hint'); await p.waitForTimeout(500); await p.screenshot({ path: out + '/hint.png' });
  await p.locator('#people .chip').first().click(); await p.waitForSelector('#choice'); await p.waitForTimeout(500); await p.screenshot({ path: out + '/talk-choice.png' }); await p.locator('#choice button').first().click(); await p.waitForTimeout(2500); await p.screenshot({ path: out + '/talk.png' });
  await p.close();
  for (const [n, vp] of [['phone-land', { width: 844, height: 390 }], ['phone-port', { width: 390, height: 780 }], ['ipad', { width: 1024, height: 768 }]]){ p = await open(vp); await p.waitForTimeout(600); await p.screenshot({ path: `${out}/${n}.png` }); await p.close(); }
  console.log('errors', errs); await b.close(); })().catch(e => { console.log('FAIL', e.message); process.exit(1); });
