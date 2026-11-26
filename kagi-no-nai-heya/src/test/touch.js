// node test3/touch.js : on an emulated iPad, a finger can move the evidence sheet, move and link board cards, and scroll a tall board
const { chromium, devices } = require('playwright'); const PORT = process.env.PORT || 8767;
(async () => {
  const b = await chromium.launch(), ctx = await b.newContext({ ...devices['iPad (gen 7) landscape'] }), p = await ctx.newPage(), cdp = await ctx.newCDPSession(p); let errs = 0, fails = 0;
  p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  const ok = (c, label, extra = '') => { if (!c) fails++; console.log(c ? 'OK  ' : 'FAIL', label, extra); };
  const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts.map(([x, y], i) => ({ x, y, id: i })) });
  const drag = async (x, y, dx, dy, steps = 8) => { await touch('touchStart', [[x, y]]); for (let i = 1; i <= steps; i++){ await touch('touchMove', [[x + dx * i / steps, y + dy * i / steps]]); await p.waitForTimeout(16); } await touch('touchEnd', []); await p.waitForTimeout(60); };
  const tap = async (x, y) => { await touch('touchStart', [[x, y]]); await touch('touchEnd', []); await p.waitForTimeout(80); };
  const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && __g.mode === 'free', null, { timeout: 60000 });
  const mid = async sel => { const r = await p.locator(sel).first().boundingBox(); return [r.x + r.width / 2, r.y + r.height / 2, r]; };
  await p.goto(`http://127.0.0.1:${PORT}/index.html`); await p.waitForTimeout(300);
  await p.evaluate(() => { __g.fast(true); __g.start('001', false); }); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(500, 250); await idle();
  ok(await p.evaluate(() => document.querySelector('#stage').classList.contains('lite')), 'light drawing mode is on, as on a touch device');
  const D = await p.evaluate(() => JSON.parse(JSON.stringify(__g.D)));
  await p.evaluate(D => { const G = __g.G; for (const e of D.ev) if (!G.ev.includes(e)) G.ev.push(e); for (const f of D.facts) if (!G.facts.includes(f)) G.facts.push(f); }, D);
  // evidence sheet
  await p.click('#t-ev'); await p.waitForSelector('#ins .view'); let [vx, vy] = await mid('#ins .view');
  const sheetAt = async () => { const r = await p.locator('#ins .sheet > *').first().boundingBox(); return [Math.round(r.x), Math.round(r.y)]; };
  let a = await sheetAt(); await drag(vx, vy, 90, 60); let c = await sheetAt(); ok(Math.abs(c[0] - a[0] - 90) < 6 && Math.abs(c[1] - a[1] - 60) < 6, 'finger moves the evidence sheet', `${a} -> ${c}`);
  a = c; await drag(vx, vy, -140, -80); c = await sheetAt(); ok(Math.abs(c[0] - a[0] + 140) < 6 && Math.abs(c[1] - a[1] + 80) < 6, 'and back the other way', `${a} -> ${c}`);
  await touch('touchStart', [[vx - 40, vy], [vx + 40, vy]]); for (let i = 1; i <= 6; i++){ await touch('touchMove', [[vx - 40 - i * 15, vy], [vx + 40 + i * 15, vy]]); await p.waitForTimeout(16); } await touch('touchEnd', []); await p.waitForTimeout(60);
  const z = await p.evaluate(() => __ins.V().z); ok(z > 1.5, 'two fingers zoom the sheet', 'zoom ' + z.toFixed(2));
  for (let i = 0; i < 5; i++) await drag(vx, vy, -400, -300, 5); const vis = await p.evaluate(() => { const v = document.querySelector('#ins .view').getBoundingClientRect(), f = document.querySelector('#ins .sheet').firstElementChild.getBoundingClientRect(); return [Math.round(Math.min(v.right, f.right) - Math.max(v.left, f.left)), Math.round(Math.min(v.bottom, f.bottom) - Math.max(v.top, f.top))]; }); ok(vis[0] > 80 && vis[1] > 80, 'flung sheet stays in sight', vis.join('x'));
  a = await sheetAt(); await drag(vx, vy, 100, 70); c = await sheetAt(); ok(c[0] > a[0] + 50 && c[1] > a[1] + 30, 'sheet at the edge still comes back by finger', `${a} -> ${c}`);
  await p.click('#ins .x');
  // board, small
  await p.click('#t-brd'); await p.waitForSelector('#brd .card');
  let [cx, cy, r0] = await mid('#brd .card[data-id="f_med"]'); await drag(cx, cy, 120, 150); let [, , r1] = await mid('#brd .card[data-id="f_med"]'); ok(Math.abs(r1.x - r0.x - 120) < 6 && Math.abs(r1.y - r0.y - 150) < 6, 'finger moves a board card', `${Math.round(r0.x)},${Math.round(r0.y)} -> ${Math.round(r1.x)},${Math.round(r1.y)}`);
  let m1 = await mid('#brd .card[data-id="f_stop"]'), m2 = await mid('#brd .card[data-id="f_plus2"]'); await tap(m1[0], m1[1]); await tap(m2[0], m2[1]); await p.waitForTimeout(200);
  const g = await p.evaluate(() => ({ links: __g.G.links.length, hyp: __g.G.hyp })); ok(g.links === 1 && g.hyp.includes('h_gap'), 'two taps tie a string and make the hypothesis', JSON.stringify(g));
  await p.locator('#brd .r .x').last().click();
  // board, tall (FILE 011 has 49 cards)
  const p2 = await ctx.newPage(), cdp2 = await ctx.newCDPSession(p2); p2.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  const touch2 = (type, pts) => cdp2.send('Input.dispatchTouchEvent', { type, touchPoints: pts.map(([x, y], i) => ({ x, y, id: i })) });
  const drag2 = async (x, y, dx, dy, steps = 8) => { await touch2('touchStart', [[x, y]]); for (let i = 1; i <= steps; i++){ await touch2('touchMove', [[x + dx * i / steps, y + dy * i / steps]]); await p2.waitForTimeout(16); } await touch2('touchEnd', []); await p2.waitForTimeout(60); };
  await p2.goto(`http://127.0.0.1:${PORT}/index.html`); await p2.waitForTimeout(300);
  await p2.evaluate(() => { __g.fast(true); __g.start('011', false); }); await p2.waitForTimeout(300); await p2.evaluate(() => __g.fast(true)); await p2.waitForTimeout(200); await p2.mouse.click(500, 500);
  await p2.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && __g.mode === 'free', null, { timeout: 90000 });
  await p2.evaluate(() => { const D = __g.D, G = __g.G; for (const f of D.facts) if (!G.facts.includes(f)) G.facts.push(f); for (const h of Object.keys(D.HYPS)) if (!G.hyp.includes(h)) G.hyp.push(h); });
  await p2.click('#t-brd'); await p2.waitForSelector('#brd .card'); const info = await p2.evaluate(() => { const c = document.querySelector('#brd .canvas'); return { n: document.querySelectorAll('#brd .card').length, sh: c.scrollHeight, ch: c.clientHeight }; }); ok(info.sh > info.ch + 50, 'the 011 board is taller than the screen', JSON.stringify(info));
  const cvb = await p2.locator('#brd .canvas').boundingBox(), top = () => p2.evaluate(() => document.querySelector('#brd .canvas').scrollTop);
  const tap2 = async sel => { const r = await p2.locator(sel).boundingBox(); await touch2('touchStart', [[r.x + r.width / 2, r.y + r.height / 2]]); await touch2('touchEnd', []); await p2.waitForTimeout(120); };
  ok(await p2.locator('#brd .bnav').isVisible(), 'a tall board shows the up and down buttons');
  await tap2('#brd .bnav button[data-d="1"]'); let st = await top(); ok(st > 100, 'the down button scrolls the board', 'scrollTop ' + Math.round(st));
  await tap2('#brd .bnav button[data-d="-1"]'); st = await top(); ok(st === 0, 'the up button scrolls it back', 'scrollTop ' + Math.round(st));
  const hole = await p2.evaluate(() => { const id = Object.keys(__g.G.pos).find(k => __g.G.pos[k][0] === 22 + 3 * 219 && __g.G.pos[k][1] === 26 + 2 * 122); __g.G.pos[id] = [22 + 3 * 219, 26]; return id; }); await p2.locator('#brd .tabs button[data-t="tl"]').click(); await p2.locator('#brd .tabs button[data-t="board"]').click(); await p2.waitForSelector('#brd .card');
  const s = cvb.width / 1600; await drag2(cvb.x + (22 + 3 * 219 + 103) * s, cvb.y + (26 + 2 * 122 + 49) * s, 0, -160); st = await top(); ok(st > 100, 'finger on an empty part of the board scrolls it', `scrollTop ${Math.round(st)} (hole left by ${hole})`);
  const last = await p2.evaluate(() => { const c = document.querySelector('#brd .canvas').getBoundingClientRect(); const d = [...document.querySelectorAll('#brd .card')].map(d => [d.dataset.id, d.getBoundingClientRect()]).filter(([, r]) => r.top > c.top + 120 && r.bottom < c.bottom - 20 && r.left > c.left + 300 && r.right < c.right - 300).pop(); return [d[0], d[1].x + d[1].width / 2, d[1].y + d[1].height / 2, d[1].x, d[1].y]; });
  await drag2(last[1], last[2], -80, -60); const after = await p2.locator(`#brd .card[data-id="${last[0]}"]`).boundingBox(); ok(Math.abs(after.x - last[3] + 80) < 6 && Math.abs(after.y - last[4] + 60) < 6, 'a card on the scrolled board moves by finger', `${last[0]} ${Math.round(last[3])},${Math.round(last[4])} -> ${Math.round(after.x)},${Math.round(after.y)}`);
  st = await p2.evaluate(() => document.querySelector('#brd .canvas').scrollTop); ok(st > 100, 'moving a card does not scroll the board', 'scrollTop ' + Math.round(st));
  await p2.screenshot({ path: 'test3/touch-brd.png' }); void cvb;
  console.log('errors', errs, 'fails', fails); await b.close(); process.exit(fails || errs ? 1 : 0);
})();
