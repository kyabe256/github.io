// node test3/bot.js <outdir> [stopAfter]   full correct walkthrough through the real UI
const { chromium } = require('playwright'); const fs = require('fs');
const out = process.argv[2] || 'test3/run1'; fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1600, height: 900 } }); let errs = 0;
  p.on('console', m => { if (m.type() === 'error' && !/404/.test(m.text())){ errs++; console.log('console.error', m.text().slice(0, 300)); } }); p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message, (e.stack || '').split('\n').slice(1, 3).join(' | ')); });
  await p.goto('http://127.0.0.1:8767/index.html'); await p.waitForTimeout(500);
  const shot = n => p.screenshot({ path: `${out}/${n}.png` });
  const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden)), null, { timeout: 90000 });
  const G = () => p.evaluate(() => __g.G);
  await p.click('#t-new'); await p.evaluate(() => __g.fast(true)); await p.waitForTimeout(200); await p.mouse.click(800, 840); await idle();
  const clickHs = async id => { const h = (await p.evaluate(() => __g.hs())).find(x => x.id === id); if (!h) throw new Error('no hs ' + id); await p.mouse.click(h.x, h.y); await p.waitForTimeout(60); await idle(); const g = await G(); if (!g.seen[id]) throw new Error('hs not seen ' + id); };
  const allHs = async () => { for (;;){ const hs = (await p.evaluate(() => __g.hs())).filter(x => !x.seen && !x.desk); if (!hs.length) break; const h = hs[0]; await clickHs(h.id); if (h.enter){ await allHs(); await p.click('#zoomout'); await p.waitForTimeout(80); await idle(); } } };
  const talkAll = async () => { const n = await p.locator('#people .chip').count(); for (let i = 0; i < n; i++){ await p.locator('#people .chip').nth(i).click(); for (;;){ await p.waitForSelector('#choice', { timeout: 30000 }); const t = p.locator('#choice button:not(.seen):not(.sub):not(.hot)'); if (await t.count()){ await t.first().click(); await p.waitForTimeout(80); await p.waitForFunction(() => document.querySelector('#choice') || (!__g.busy && __g.mode === 'free'), null, { timeout: 60000 }); if (!(await p.locator('#choice').count())) break; } else { await p.locator('#choice button.sub').click(); break; } } await idle(); } };
  const go = async loc => { await p.click('#a-map'); await p.click(`.node[data-loc="${loc}"]`); await p.waitForTimeout(80); await idle(); };
  const facts = async (ids) => { await p.click('#t-ev'); for (const id of ids){ await p.evaluate(id => __ins.show(id), id);
      if (id === 'video'){ for (const [t, sel] of [[8400, 'rect[data-cond="lamp"]'], [10560, '#vfig']]){ await p.evaluate(t => { const s = document.querySelector('#vt'); s.value = t; s.dispatchEvent(new Event('input')); }, t); const r = await p.locator(sel).boundingBox(); await p.mouse.click(r.x + r.width / 2, r.y + r.height / 2); await p.waitForTimeout(50); } continue; }
      for (const face of [0, 1]){ const sel = face ? '#ins .face.back .h[data-f]' : '#ins .face:not(.back) .h[data-f]'; const n = await p.locator(sel).count(); if (!n) continue; if (face){ await p.evaluate(() => __ins.flip()); await p.waitForTimeout(650); }
        await p.evaluate(() => __ins.zoom(2.4)); for (let i = 0; i < n; i++){ await p.evaluate(([sel, i]) => __ins.center(document.querySelectorAll(sel)[i]), [sel, i]); const v = await p.locator('#ins .view').boundingBox(); await p.mouse.click(v.x + v.width / 2, v.y + v.height / 2); await p.waitForTimeout(40); } } }
    await p.click('#ins .x'); };
  const link = async pairs => { await p.click('#t-brd'); for (const [a, b] of pairs){ await p.evaluate(([a, b]) => __brd.link(a, b), [a, b]); await p.waitForTimeout(60); } await p.click('#brd .r .x:last-child'); };
  const need = async (arr, kind) => { const g = await G(); const miss = arr.filter(x => !g[kind].includes(x)); if (miss.length) throw new Error('missing ' + kind + ': ' + miss); };
  const startIntr = async () => { await p.locator('#people .chip').first().click(); await p.waitForSelector('#choice'); await p.locator('#choice button.hot').click(); await p.waitForTimeout(100); await idle(); };
  const present = async (st, i, item, kind) => { await p.click(`.st[data-id="${st}"] span[data-i="${i}"]`); await p.click('#i-pres'); await p.click(`#pick .tabs button[data-t="${kind}"]`); await p.click(`#pick .pc[data-id="${item}"]`); await p.click('#p-ok'); await p.waitForTimeout(100); await p.waitForFunction(() => document.querySelector('#choice') || document.querySelector('#res') || (!__g.busy && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden))), null, { timeout: 90000 }); };

  // day 1
  await shot('01-genkan'); await allHs(); await talkAll();
  await go('living'); await shot('02-living'); await allHs(); await talkAll();
  await go('bath'); await allHs(); await go('hall'); await shot('03-hall'); await allHs(); await talkAll(); await go('kanri'); await allHs(); await talkAll();
  await need(['lock', 'phone', 'video', 'loginlog', 'elev', 'form', 'parking', 'elcam', 'conf', 'gate'], 'ev');
  await p.click('#a-map'); await shot('04-map'); await p.click('.node[data-loc="next"]'); await p.waitForTimeout(100); await idle();
  await need(['autopsy', 'locklog', 'volt', 'mail'], 'ev');
  await go('cyber'); await talkAll(); await go('kasouken'); await talkAll();
  await facts(['lock', 'phone', 'video', 'loginlog', 'elev', 'form', 'parking', 'elcam', 'conf', 'gate', 'autopsy', 'locklog', 'volt', 'mail']);
  let g = await G(); console.log('facts after day2 sweep', g.facts.length, g.facts.join(','));
  await need(['f_board', 'f_wound', 'f_tod', 'f_addr', 'f_count', 'f_log212', 'f_volt', 'f_voltS', 'f_msg158', 'f_msgMon', 'f_missed', 'f_elev', 'f_elev2', 'f_lamp', 'f_figure', 'f_login', 'f_two', 'f_bag', 'f_utc', 'f_confRow', 'f_etc', 'f_parkC', 'f_parkS', 'f_scar', 'f_dipl', 'f_gateS', 'f_gateM', 'f_mailR', 'f_mailIP', 'f_acct'], 'facts');
  await link([['f_board', 'f_wound'], ['f_count', 'f_log212'], ['h_ghost', 'f_volt'], ['f_lamp', 'f_elev'], ['h_time', 'f_two'], ['f_utc', 'f_confRow'], ['f_etc', 'f_parkC']]);
  await need(['h_weapon', 'h_ghost', 'h_time', 'h_loop', 'h_window', 'h_conf', 'h_coleLate'], 'hyp');
  await go('fbi'); await allHs(); await startIntr(); await shot('05-intrA');
  await present('a_s2', 2, 'h_conf', 'hyp'); await present('a_s3', 1, 'h_coleLate', 'hyp'); await present('a_s4', 2, 'phone', 'ev'); await idle();
  g = await G(); if (!g.intr.A.clear) throw new Error('A not clear'); await need(['f_sched'], 'facts');
  await go('keibi'); await allHs(); await startIntr(); await present('b_s2', 1, 'gate', 'ev'); await present('b_s3', 1, 'f_scar', 'fact'); await need(['note'], 'ev');
  await facts(['note']); await link([['h_window', 'f_note']]); await need(['h_coleClear'], 'hyp');
  await present('b_s4', 0, 'h_coleClear', 'hyp'); await idle();
  g = await G(); if (!g.flags.mid || g.day !== 3 || g.loc !== 'soukan') throw new Error('mid not reached ' + JSON.stringify([g.flags, g.day, g.loc]));
  await need(['carlist'], 'ev'); await go('renraku'); await shot('06-renraku'); await allHs(); await need(['slip', 'news'], 'ev');
  await facts(['carlist', 'slip', 'news']); await link([['f_mailR', 'f_gateM'], ['f_mailIP', 'f_login'], ['f_addr', 'f_acct'], ['f_acct', 'f_sched'], ['f_slip', 'f_news'], ['f_dipl', 'f_khalid']]);
  await need(['h_alibi', 'h_same', 'h_three', 'h_trade', 'h_embassy'], 'hyp');
  g = await G(); console.log('all facts', g.facts.length, 'hyp', g.hyp.length);
  if (process.argv[3] === 'pre') { await p.evaluate(() => localStorage.setItem('pre-report', localStorage.getItem('kagi-no-nai-heya-1'))); fs.writeFileSync(out + '/pre.json', await p.evaluate(() => localStorage.getItem('kagi-no-nai-heya-1'))); }
  // report
  await p.click('#a-rep'); const ans = { doer: ['two', 'h_window'], mole: ['mashiba', 'h_three'], boss: ['khalid', 'h_embassy'], entry: ['master', 'h_time'], camera: ['swap', 'h_loop'], weapon: ['board', 'h_weapon'], motive: ['brother', 'h_trade'] };
  for (const k in ans){ const r = p.locator(`.fr:has(.sp[data-k="${k}"])`); await r.locator(`.op button[data-v="${ans[k][0]}"]`).click(); await r.locator('.sp').click(); await p.click('#pick .tabs button[data-t="hyp"]'); await p.click(`#pick .pc[data-id="${ans[k][1]}"]`); await p.click('#p-ok'); }
  await shot('07-report'); await p.click('#r-go'); await p.click('#r-go'); await p.waitForTimeout(200); await idle();
  await shot('08-intrC');
  await present('c_s2', 0, 'h_alibi', 'hyp'); await present('c_s3', 2, 'h_same', 'hyp'); await present('c_s4', 0, 'h_three', 'hyp'); await present('c_s5', 1, 'slip', 'ev'); await present('c_s6', 1, 'h_trade', 'hyp');
  await p.waitForSelector('#choice'); await p.locator('#choice button').first().click(); await p.waitForSelector('#res', { timeout: 90000 }); await p.waitForTimeout(1200); await shot('09-result');
  console.log('RESULT', JSON.stringify(await p.evaluate(() => __res)), 'errors', errs);
  await b.close();
})().catch(e => { console.log('BOT FAIL', e.message); process.exit(1); });
