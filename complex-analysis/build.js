#!/usr/bin/env node
/*
 * 複素関数論 演習問題集 — ビルドスクリプト
 *
 *   src/*.html, src2/*.html （$…$ / $$…$$ で数式を書いた素材）をそれぞれ結合し、
 *   KaTeX でサーバサイド描画して巻ごとに 2 つの成果物を作る。
 *
 *     1. <巻>.html             … Web 版（CDN の KaTeX / Google Fonts を参照）
 *     2. <OUT_DIR>/print.html  … 印刷版（ローカルの woff2 / KaTeX を参照）
 *        → puppeteer-core + Chromium で PDF 化
 *
 *   CSS は assets/style.css に一本化し、各巻の head の /*STYLE*_/ を差し替える。
 *
 * 使い方:
 *   MODULES=/path/to/node_modules OUT_DIR=/path/to/build \
 *   CHROME=/path/to/chrome node build.js
 */
const fs = require('fs');
const path = require('path');

const MODULES = process.env.MODULES || path.join(__dirname, 'node_modules');
const OUT_DIR = process.env.OUT_DIR || path.join(__dirname, 'build');
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const BOOKS = [
  { src: 'src', html: 'index.html', pdf: 'complex-analysis-problems.pdf' },
  { src: 'src2', html: 'volume2.html', pdf: 'complex-analysis-problems-vol2.pdf' },
];

const katex = require(path.join(MODULES, 'katex'));
const STYLE = fs.readFileSync(path.join(__dirname, 'assets', 'style.css'), 'utf8');

const render = (tex, displayMode) => {
  try {
    return katex.renderToString(tex.trim(), { displayMode, throwOnError: true, strict: false });
  } catch (e) {
    console.error(`\n[KaTeX error] ${e.message}\n  in: ${tex.slice(0, 120)}\n`);
    process.exitCode = 1;
    return `<span style="color:red">${tex}</span>`;
  }
};

// 素材を結合し、数式を描画した 1 枚の HTML にする
const compose = (srcDir) => {
  const dir = path.join(__dirname, srcDir);
  const parts = fs.readdirSync(dir).filter((f) => f.endsWith('.html')).sort();
  let doc = parts.map((f) => fs.readFileSync(path.join(dir, f), 'utf8')).join('\n');
  doc = doc.replace('/*STYLE*/', () => STYLE);
  doc = doc.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => render(tex, true));
  doc = doc.replace(/\$([^$]{1,400}?)\$/g, (_, tex) => render(tex, false));
  if (doc.includes('$')) {
    console.error(`[warn] ${srcDir}: 対応の取れていない $ が残っています`);
    process.exitCode = 1;
  }
  return { doc, parts };
};

// ---- 出力先ごとの CSS リンク ------------------------------------------------
const WEB_LINKS = [
  '<meta name="viewport" content="width=device-width, initial-scale=1">',
  '<link rel="preconnect" href="https://fonts.googleapis.com">',
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap">',
  '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">',
  '<style>@media screen{body{max-width:52em;margin:0 auto;padding:2.5em 1.4em 6em}.cover{height:auto;padding:3em 0 4em}}</style>',
].join('\n');

const PRINT_LINKS = [
  '<link rel="stylesheet" href="vendor/japanese-400.css">',
  '<link rel="stylesheet" href="vendor/japanese-700.css">',
  '<link rel="stylesheet" href="vendor/katex.min.css">',
].join('\n');

fs.mkdirSync(OUT_DIR, { recursive: true });

(async () => {
  const puppeteer = require(path.join(MODULES, 'puppeteer-core'));
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-gpu', '--font-render-hinting=none'],
  });
  const foot =
    '<div style="width:100%;font-size:8px;color:#8a929c;font-family:sans-serif;' +
    'text-align:center;padding:0 0 4mm"><span class="pageNumber"></span></div>';

  for (const book of BOOKS) {
    const { doc, parts } = compose(book.src);
    fs.writeFileSync(path.join(__dirname, book.html), doc.replace('<!--CSSLINKS-->', WEB_LINKS));
    const printPath = path.join(OUT_DIR, `print-${book.src}.html`);
    fs.writeFileSync(printPath, doc.replace('<!--CSSLINKS-->', PRINT_LINKS));

    const page = await browser.newPage();
    await page.goto('file://' + printPath, { waitUntil: 'networkidle0' });
    await page.evaluateHandle('document.fonts.ready');
    const pdfPath = path.join(__dirname, book.pdf);
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: foot,
      margin: { top: '17mm', bottom: '17mm', left: '17mm', right: '17mm' },
    });
    await page.close();
    const kb = (fs.statSync(pdfPath).size / 1024).toFixed(0);
    console.log(`${book.src} (${parts.length} ファイル) → ${book.html}, ${book.pdf} (${kb} KB)`);
  }
  await browser.close();
})();
