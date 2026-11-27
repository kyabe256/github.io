// node test/scene.js <out.png> scene:era[,scene:era...] [file] : whole panoramas, scaled to the page width
const { chromium } = require('playwright'); const path = require('path'); const S = path.join(__dirname, '..', 'src');
const A = require(S + '/scenes_a.js'); let SC = A.SC; try { Object.assign(global, A); const B = require(S + '/scenes_b.js'); SC = Object.assign(SC, B.SCB || {}); } catch (e) { if (!/Cannot find module/.test(e.message)) throw e; }
(async () => { const out = process.argv[2], list = process.argv[3].split(','); let h = '<body style="margin:0;background:#000">';
  for (const it of list){ const [n, e] = it.split(':'), s = SC[n](+e), k = 1560 / s.w;
    h += `<div style="position:relative;width:1560px;height:${900 * k}px;overflow:hidden;margin-bottom:6px"><div style="transform:scale(${k});transform-origin:0 0;position:absolute;width:${s.w}px;height:900px">` +
      `<div style="position:absolute;left:0;top:0;transform:scaleX(${s.w / s.bw});transform-origin:0 0">${A.svgw(s.bw, s.bg, s.defs)}</div><div style="position:absolute;left:0;top:0">${A.svgw(s.w, s.main, s.defs)}</div><div style="position:absolute;left:0;top:0;transform:scaleX(${s.w / s.fw});transform-origin:0 0;opacity:${process.env.NOFORE ? 0 : 1}">${A.svgw(s.fw, s.fore, s.defs)}</div></div></div>`; }
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1560, height: 600 } }); await p.setContent(h); await p.screenshot({ path: out, fullPage: true }); await b.close(); })();
