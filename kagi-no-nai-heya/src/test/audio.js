// node test3/audio.js : the music scheduler survives a stalled page, voices play, touch devices start in light mode
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  let errs = 0;
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  p.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  await p.goto('http://127.0.0.1:8767/index.html');
  await p.waitForTimeout(400);
  const r = await p.evaluate(async () => {
    // count every oscillator the page starts, with its start time relative to "now"
    const starts = [];
    const orig = OscillatorNode.prototype.start;
    OscillatorNode.prototype.start = function (t) { starts.push([this.context.currentTime, t || 0]); return orig.apply(this, arguments); };
    AudioSys.init();
    AudioSys.bgm('battle');
    await new Promise(r => setTimeout(r, 1500));
    const before = starts.length;
    const t0 = performance.now();
    while (performance.now() - t0 < 2500) { /* stall the page for 2.5 seconds */ }
    await new Promise(r => setTimeout(r, 400));
    const after = starts.slice(before);
    const late = after.filter(x => x[1] < x[0] - 0.01).length; // notes scheduled in the past would all sound at once
    const ok = await AudioSys.loadPack('voice-011.mp3', VIDX);
    const ln = CASE.story.op_1.find(l => l.who === 'yuki');
    const dur = await AudioSys.speak('yuki', ln.t);
    await new Promise(r => setTimeout(r, 600));
    const lvl = AudioSys.level();
    return { notesBeforeStall: before, notesAfterStall: after.length, lateNotes: late, packLoaded: ok, voiceSeconds: +dur.toFixed(2), voiceLevel: +lvl.toFixed(2) };
  });
  console.log(JSON.stringify(r));
  await p.close();
  const ctx = await b.newContext({ viewport: { width: 1024, height: 768 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const q = await ctx.newPage();
  q.on('pageerror', e => { errs++; console.log('PAGEERR', e.message); });
  await q.goto('http://127.0.0.1:8767/index.html');
  await q.waitForTimeout(400);
  console.log('touch device starts light:', await q.evaluate(() => document.querySelector('#stage').classList.contains('lite')));
  console.log('errors', errs);
  await b.close();
})().catch(e => { console.log('FAIL', e.message); process.exit(1); });
