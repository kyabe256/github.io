// node test3/nearmsg.js : after a near miss the interrogation guide line says what to do next (case 001, statement k1)
const { chromium } = require('playwright'); const PORT = process.env.PORT || 8767;
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1600, height: 900 } }); let errs = 0, fails = 0;
  p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  await p.goto(`http://127.0.0.1:${PORT}/index.html`); await p.waitForTimeout(300);
  const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && (__g.mode === 'free' || (__g.mode === 'intr' && !document.querySelector('#intr').hidden)), null, { timeout: 60000 });
  await p.evaluate(() => { __g.fast(true); __g.start('001', false); }); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(800, 300); await idle();
  const D = await p.evaluate(() => JSON.parse(JSON.stringify(__g.D))), I = D.INTR.A;
  await p.evaluate(() => { __g.G.facts.push('f_plus2'); });
  if ((await p.evaluate(() => __g.G.loc)) !== I.at){ await p.click('#a-map'); await p.click(`.node[data-loc="${I.at}"]`); await p.waitForTimeout(60); await idle(); }
  await p.locator('#people .chip', { hasText: D.names[I.foe] }).first().click(); await p.waitForSelector('#choice'); await p.locator('#choice button.hot').click(); await p.waitForTimeout(100); await idle();
  const guide = () => p.locator('#intr .guide').innerText();
  const pres = async (ph, kind, item) => { await p.click(`.st[data-id="k1"] span[data-i="${ph}"]`); await p.click('#i-pres'); await p.click(`#pick .tabs button[data-t="${kind}"]`); await p.click(`#pick .pc[data-id="${item}"]`); await p.click('#p-ok'); await p.waitForTimeout(100); await idle(); };
  const want = async (label, re) => { const t = await guide(), ok = re.test(t); if (!ok) fails++; console.log(ok ? 'OK  ' : 'FAIL', label, '|', t); };
  const g0 = await p.evaluate(() => __g.G.intr.A.g);
  await pres(1, 'fact', 'f_plus2'); await want('near, no hypothesis yet', /カード1枚では崩せない/);
  await p.evaluate(() => __g.fast(false)); await p.waitForTimeout(500); await p.screenshot({ path: 'test3/nearmsg.png' }); await p.evaluate(() => __g.fast(true));
  await p.click('.st[data-id="k1"] span[data-i="1"]'); await want('phrase picked again', /ゆさぶる/);
  await p.evaluate(() => { __g.G.hyp.push('h_gap'); });
  await pres(1, 'fact', 'f_plus2'); await want('near, hypothesis owned', /もう持っている/);
  await pres(0, 'hyp', 'h_gap'); await want('right item, wrong phrase', /言葉がちがう/);
  const g1 = await p.evaluate(() => __g.G.intr.A.g); if (g0 !== g1){ fails++; console.log('FAIL trust changed', g0, g1); } else console.log('OK   trust unchanged', g1);
  await pres(1, 'hyp', 'h_gap'); const done = await p.evaluate(() => __g.G.intr.A.done); if (!done.includes('k1')){ fails++; console.log('FAIL k1 not broken'); } else { console.log('OK   k1 broken'); await want('after break', /まず、証言/); }
  console.log('errors', errs, 'fails', fails); await b.close(); process.exit(fails || errs ? 1 : 0);
})();
