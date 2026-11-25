// node test3/botstd.js <id> [id...] : plays each standard case from start to a correct report through the real UI
const { chromium } = require('playwright'); const fs = require('fs');
const PORT = process.env.PORT || 8767, SHOT = process.env.SHOT;
(async () => {
  const b = await chromium.launch(); let fails = 0;
  for (const id of process.argv.slice(2)){
    const p = await b.newPage({ viewport: { width: 1600, height: 900 } }); let errs = 0;
    p.on('console', m => { if (m.type() === 'error' && !/404|Failed to load resource/.test(m.text())){ errs++; console.log(id, 'console.error', m.text().slice(0, 240)); } }); p.on('pageerror', e => { errs++; console.log(id, 'PAGEERR', e.message, (e.stack || '').split('\n').slice(1, 3).join(' | ')); });
    try {
      await p.goto(`http://127.0.0.1:${PORT}/index.html`); await p.waitForTimeout(300);
      const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden)), null, { timeout: 60000 });
      const G = () => p.evaluate(() => __g.G), cnt = async () => { const g = await G(); return g.ev.length + g.facts.length + g.hyp.length + Object.keys(g.tk).length + Object.keys(g.seen).length; };
      await p.evaluate(id => { __g.fast(true); __g.start(id, false); }, id); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(800, 300); await idle();
      const D = await p.evaluate(() => JSON.parse(JSON.stringify(__g.D)));
      const allHs = async () => { for (;;){ const hs = (await p.evaluate(() => __g.hs())).filter(x => !x.seen); if (!hs.length) break; await p.mouse.click(hs[0].x, hs[0].y); await p.waitForTimeout(50); await idle(); if (!(await G()).seen[hs[0].id]) throw new Error('hotspot not seen ' + hs[0].id); } };
      const talkAll = async () => { const n = await p.locator('#people .chip').count(); for (let i = 0; i < n; i++){ if (i >= await p.locator('#people .chip').count()) break; await p.locator('#people .chip').nth(i).click(); for (;;){ await p.waitForSelector('#choice', { timeout: 30000 }); const t = p.locator('#choice button:not(.seen):not(.sub):not(.hot)'); if (await t.count()){ await t.first().click(); await p.waitForTimeout(60); await p.waitForFunction(() => document.querySelector('#choice') || (!__g.busy && __g.mode === 'free'), null, { timeout: 60000 }); if (!(await p.locator('#choice').count())) break; } else { await p.locator('#choice button.sub').click(); break; } } await idle(); } };
      const go = async loc => { if ((await G()).loc === loc) return; await p.click('#a-map'); await p.click(`.node[data-loc="${loc}"]`); await p.waitForTimeout(60); await idle(); };
      const facts = async () => { const g = await G(); if (!g.ev.length) return; await p.click('#t-ev'); for (const e of g.ev){ await p.evaluate(e => __ins.show(e), e); for (const face of [0, 1]){ const sel = face ? '#ins .face.back .h[data-f]' : '#ins .face:not(.back) .h[data-f]'; const n = await p.locator(sel).count(); if (!n) continue; if (face){ await p.evaluate(() => __ins.flip()); await p.waitForTimeout(600); } await p.evaluate(() => __ins.zoom(2.4)); for (let i = 0; i < n; i++){ await p.evaluate(([sel, i]) => __ins.center(document.querySelectorAll(sel)[i]), [sel, i]); const v = await p.locator('#ins .view').boundingBox(); await p.mouse.click(v.x + v.width / 2, v.y + v.height / 2); await p.waitForTimeout(30); } } } await p.click('#ins .x'); };
      const hyps = async () => { for (let round = 0; round < 8; round++){ const g = await G(), own = new Set([...g.facts, ...g.hyp]); const todo = Object.keys(D.HYPS).filter(h => !g.hyp.includes(h)).map(h => [h, D.HYPS[h].need.find(a => a.every(x => own.has(x)))]).filter(x => x[1]); if (!todo.length) break; await p.click('#t-brd'); for (const [, alt] of todo) for (let i = 0; i + 1 < alt.length; i++){ await p.evaluate(([a, c]) => __brd.link(a, c), [alt[i], alt[i + 1]]); await p.waitForTimeout(40); } await p.click('#brd .r .x:last-child'); } };
      for (let pass = 0; pass < 6; pass++){ const before = await cnt(); for (const l of D.locs){ await go(l); await allHs(); await talkAll(); } await facts(); await hyps(); if (await cnt() === before) break; }
      let g = await G(); const miss = [...D.ev.filter(x => !g.ev.includes(x)), ...D.facts.filter(x => !g.facts.includes(x))]; if (miss.length) throw new Error('not collected: ' + miss.join(','));
      if (SHOT){ fs.mkdirSync(SHOT, { recursive: true }); await p.evaluate(() => __g.fast(false)); await p.waitForTimeout(500); await p.screenshot({ path: `${SHOT}/${id}-room.png` }); await p.click('#t-ev'); await p.waitForTimeout(300); await p.screenshot({ path: `${SHOT}/${id}-ev.png` }); await p.click('#ins .x'); await p.evaluate(() => __g.fast(true)); }
      const I = D.INTR.A; await go(I.at); await p.locator('#people .chip', { hasText: D.names[I.foe] }).first().click(); await p.waitForSelector('#choice'); await p.locator('#choice button.hot').click(); await p.waitForTimeout(100); await idle();
      if (SHOT){ await p.waitForTimeout(300); await p.screenshot({ path: `${SHOT}/${id}-intr.png` }); }
      for (let step = 0; step < 12; step++){ g = await G(); if (g.intr.A.clear) break; const own = new Set([...g.ev, ...g.facts, ...g.hyp]), s = g.intr.A.open.find(x => I.st[x].ok && !g.intr.A.done.includes(x) && I.st[x].ok.some(o => own.has(o)));
        if (!s){ await hyps(); await facts(); await hyps(); g = await G(); const own2 = new Set([...g.ev, ...g.facts, ...g.hyp]); if (!g.intr.A.open.some(x => I.st[x].ok && !g.intr.A.done.includes(x) && I.st[x].ok.some(o => own2.has(o)))) throw new Error('interrogation stuck; open=' + g.intr.A.open + ' done=' + g.intr.A.done); continue; }
        const st = I.st[s], item = st.ok.find(o => own.has(o)), kind = D.HYPS[item] ? 'hyp' : D.facts.includes(item) ? 'fact' : 'ev';
        await p.click(`.st[data-id="${s}"] span[data-i="${st.ans[0]}"]`); await p.click('#i-pres'); await p.click(`#pick .tabs button[data-t="${kind}"]`); await p.click(`#pick .pc[data-id="${item}"]`); await p.click('#p-ok'); await p.waitForTimeout(100); await idle(); }
      g = await G(); if (!g.intr.A.clear) throw new Error('interrogation not cleared'); await facts(); await hyps(); g = await G(); const own = new Set([...g.ev, ...g.facts, ...g.hyp]);
      await p.click('#a-rep'); for (const R of D.REPORT){ const r = p.locator(`.fr:has(.sp[data-k="${R.k}"])`); await r.locator(`.op button[data-v="${R.a}"]`).click(); const sup = R.sup.find(x => own.has(x)); if (!sup) throw new Error('no support owned for ' + R.q); const kind = D.HYPS[sup] ? 'hyp' : D.facts.includes(sup) ? 'fact' : 'ev'; await r.locator('.sp').click(); await p.click(`#pick .tabs button[data-t="${kind}"]`); await p.click(`#pick .pc[data-id="${sup}"]`); await p.click('#p-ok'); }
      if (SHOT) await p.screenshot({ path: `${SHOT}/${id}-rep.png` });
      await p.click('#r-go'); await p.click('#r-go'); await p.waitForSelector('#res', { timeout: 90000 }); const res = await p.evaluate(() => __res);
      const ok = res.kind === 'CASE CLOSED' && res.rank === 'S' && !errs; if (!ok) fails++; console.log(id, ok ? 'OK' : 'FAIL', JSON.stringify(res), 'errors', errs);
    } catch (e) { fails++; console.log(id, 'FAIL', e.message.split('\n')[0]); if (SHOT) await p.screenshot({ path: `${SHOT || 'test3'}/${id}-fail.png` }).catch(() => {}); }
    await p.close();
  }
  await b.close(); process.exit(fails ? 1 : 0);
})();
