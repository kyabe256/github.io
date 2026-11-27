// node test/montage.js out.png a.png b.png ... : several screenshots on one sheet, two per row
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [out, ...files] = process.argv.slice(2); let h = '<body style="margin:0;background:#222;display:flex;flex-wrap:wrap;gap:6px;padding:6px">'; for (const f of files) h += `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:770px;display:block">`;
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1560, height: 600 } }); await p.setContent(h); await p.waitForTimeout(300); await p.screenshot({ path: out, fullPage: true }); await b.close(); })();
