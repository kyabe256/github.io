// node test3/roomshot.js outdir 038:gate 097:kaidan ... : screenshot one location of a standard case
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [out, ...pairs] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const pr of pairs){
    const [id, loc] = pr.split(':'); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
    try {
      await p.goto('http://127.0.0.1:8767/index.html'); await p.waitForTimeout(300);
      const idle = () => p.waitForFunction(() => !__g.busy && !document.querySelector('#choice') && __g.mode === 'free', null, { timeout: 60000 });
      await p.evaluate(id => { __g.fast(true); __g.start(id, false); }, id); await p.waitForTimeout(400); await p.evaluate(() => __g.fast(true)); await p.mouse.click(800, 300); await idle();
      if ((await p.evaluate(() => __g.G.loc)) !== loc){ await p.click('#a-map'); await p.click(`.node[data-loc="${loc}"]`); await p.waitForTimeout(80); await idle(); }
      await p.evaluate(() => __g.fast(false)); await p.waitForTimeout(700); await p.screenshot({ path: `${out}/${id}-${loc}.png` }); console.log(pr, 'ok');
    } catch (e) { console.log(pr, 'FAIL', e.message.split('\n')[0]); }
    await p.close();
  }
  await b.close();
})();
