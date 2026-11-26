// node test3/edge.js : evidence sheets and board cards can never be dragged out of sight; lost cards from old saves come back
const { chromium } = require('playwright'); const PORT = process.env.PORT || 8767;
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1600, height: 900 } }); let errs = 0, fails = 0;
  p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  const ok = (c, label, extra = '') => { if (!c) fails++; console.log(c ? 'OK  ' : 'FAIL', label, extra); };
  await p.goto(`http://127.0.0.1:${PORT}/index.html`); await p.waitForTimeout(300);
  const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && __g.mode === 'free', null, { timeout: 60000 });
  await p.evaluate(() => { __g.fast(true); __g.start('001', false); }); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(800, 300); await idle();
  const D = await p.evaluate(() => JSON.parse(JSON.stringify(__g.D)));
  await p.evaluate(D => { const G = __g.G; for (const e of D.ev) if (!G.ev.includes(e)) G.ev.push(e); for (const f of D.facts) if (!G.facts.includes(f)) G.facts.push(f); G.pos.f_plus2 = [1354, 5000]; G.pos.f_door = [-900, -40]; }, D);
  // evidence viewer
  await p.click('#t-ev'); await p.waitForSelector('#ins .view');
  const inView = () => p.evaluate(() => { const v = document.querySelector('#ins .view').getBoundingClientRect(), f = document.querySelector('#ins .sheet').firstElementChild.getBoundingClientRect(); return [Math.round(Math.min(v.right, f.right) - Math.max(v.left, f.left)), Math.round(Math.min(v.bottom, f.bottom) - Math.max(v.top, f.top))]; });
  const fling = async (dx, dy) => { const v = await p.locator('#ins .view').boundingBox(), cx = v.x + v.width / 2, cy = v.y + v.height / 2; for (let i = 0; i < 6; i++){ await p.mouse.move(cx, cy); await p.mouse.down(); await p.mouse.move(cx + dx, cy + dy, { steps: 4 }); await p.mouse.up(); } };
  for (const e of D.ev.slice(0, 3)){ await p.evaluate(e => __ins.show(e), e);
    for (const [dx, dy, n] of [[-700, 0, 'left'], [700, 0, 'right'], [0, -420, 'up'], [0, 420, 'down'], [-700, -420, 'corner']]){ await fling(dx, dy); const [w, h] = await inView(); ok(w >= 150 && h >= 150, `sheet ${e} flung ${n}`, `visible ${w}x${h}`); }
    await p.evaluate(() => __ins.zoom(3)); await fling(-900, -500); let [w, h] = await inView(); ok(w >= 150 && h >= 150, `sheet ${e} zoomed and flung`, `visible ${w}x${h}`);
    await p.click('#ins .ctl button[data-z="0"]'); [w, h] = await inView(); ok(w >= 500, `sheet ${e} after 戻す`, `visible ${w}x${h}`); }
  await p.screenshot({ path: 'test3/edge-ins.png' }); await p.click('#ins .x');
  // board
  await p.click('#t-brd'); await p.waitForSelector('#brd .card');
  const out = () => p.evaluate(() => { const c = document.querySelector('#brd .canvas'), v = c.getBoundingClientRect(); c.scrollTop = 0; return [...document.querySelectorAll('#brd .card')].filter(d => { const r = d.getBoundingClientRect(); return r.left < v.left - 1 || r.right > v.right + 1 || r.top < v.top - 1 || r.bottom > v.bottom + 1; }).map(d => d.dataset.id); });
  let o = await out(); ok(!o.length, 'old save with lost cards: all cards on the board', o.join(','));
  const card = p.locator('#brd .card[data-id="f_med"]'), bb = await card.boundingBox();
  for (const [dx, dy, n] of [[2000, 2000, 'down-right'], [-3000, -2000, 'up-left'], [0, 3000, 'down']]){ const r = await card.boundingBox(); await p.mouse.move(r.x + 20, r.y + 20); await p.mouse.down(); await p.mouse.move(r.x + 20 + dx, r.y + 20 + dy, { steps: 6 }); await p.mouse.up(); o = await out(); ok(!o.length, `card dragged ${n} stays on the board`, o.join(',')); }
  await p.screenshot({ path: 'test3/edge-brd.png' });
  await p.evaluate(() => __brd.link('f_stop', 'f_plus2')); await p.waitForTimeout(100);
  await p.click('#b-tidy'); await p.waitForTimeout(100); o = await out(); const st = await p.evaluate(() => ({ pos: __g.G.pos.f_med, links: __g.G.links.length, hyp: __g.G.hyp.length, n: document.querySelectorAll('#brd .card').length }));
  ok(!o.length && st.pos[0] % 219 === 22 && (st.pos[1] - 26) % 122 === 0, '並べ直す puts cards back on the grid', JSON.stringify(st)); ok(st.links >= 1 && st.hyp >= 1, 'links and hypotheses kept');
  await p.screenshot({ path: 'test3/edge-tidy.png' });
  console.log('errors', errs, 'fails', fails); await b.close(); process.exit(fails || errs ? 1 : 0);
})();
