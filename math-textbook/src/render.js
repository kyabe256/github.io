const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file://'+process.cwd()+'/'+(process.argv[3]||'book.html'));
 await p.waitForSelector('body[data-done]'); await p.waitForTimeout(800);
 const errs=await p.$$eval('.katex-error',e=>e.map(x=>x.title||x.textContent));
 console.log('katex errors:',errs.length, errs.slice(0,5));
 await p.pdf({path:process.argv[2],format:'A4',printBackground:true,displayHeaderFooter:true,
  headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#888"><span class="pageNumber"></span></div>',
  margin:{top:'14mm',bottom:'16mm',left:'14mm',right:'14mm'}});
 await b.close();})();
