// node test/sheet.js <out.png> [ids,comma] [emos] [width] : contact sheet of portraits
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const S = path.join(__dirname, '..', 'src'); const { PORT } = require(S + '/chars.js'), { CAST } = require(S + '/cast.js');
(async () => { const out = process.argv[2], ids = (process.argv[3] || Object.keys(CAST).join(',')).split(','), emos = (process.argv[4] || 'n').split(','), w = +(process.argv[5] || 250);
  let h = '<body style="margin:0;background:#3b4148;display:flex;flex-wrap:wrap;gap:6px;padding:6px;font:12px sans-serif;color:#fff">';
  for (const id of ids) for (const e of emos) h += `<div style="width:${w}px;background:linear-gradient(#8fa3ad,#4d5c66)">${PORT.svg(CAST[id], e, { wet: CAST[id].wet, attr: 'style="width:100%;display:block"' })}<div style="padding:2px 6px">${id} ${e}</div></div>`;
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1560, height: 900 } }); await p.setContent(h); await p.screenshot({ path: out, fullPage: true }); await b.close(); })();
