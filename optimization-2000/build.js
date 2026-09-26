#!/usr/bin/env node
/*
 * 非線形最適化 2000 大問 — ビルドスクリプト
 *
 *   src/*.html を結合し、次の順に処理して HTML / PDF を作る。
 *
 *     1. 採番      {{H:label}} を出現順に 1, 2, … へ。label は旧版の番号か任意の名前、
 *                  "+" は参照されない匿名の問題。
 *     2. 参照解決  {{R:label}} を 1. で決まった番号へ（未定義ならビルド失敗）。
 *     3. 章範囲    <h3 class="ch"> 内の {{RANGE}} を、その章に属する問題番号の範囲へ。
 *     4. 目次      <!--TOC--> を h2.part / h3.ch から生成。
 *     5. 索引      <!--INDEX--> を問題の見出しから生成（欧文と和文の 2 群、2 段組）。
 *     6. 統計      {{STAT:TOTAL}} {{STAT:S4}} {{STAT:S5}} {{STAT:LATIN}} {{STAT:OTHER}}。
 *     7. 数式      $…$ / $$…$$ を KaTeX でサーバサイド描画。
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
const HTML_OUT = path.join(__dirname, 'index.html');
const PDF_OUT = path.join(__dirname, 'optimization-2000-problems.pdf');

const katex = require(path.join(MODULES, 'katex'));
const STYLE = fs.readFileSync(path.join(__dirname, 'assets', 'style.css'), 'utf8');

const fail = (msg) => {
  console.error(`[error] ${msg}`);
  process.exitCode = 1;
};

// ---- 結合 -------------------------------------------------------------------
const SRC = path.join(__dirname, 'src');
const parts = fs.readdirSync(SRC).filter((f) => /\.(html|txt)$/.test(f)).sort();

/*
 * 問題の素材は簡易記法の .txt で書く（2000 題分の HTML の定型を省くため）。
 *
 *   =part 第 I 部　凸解析 | CONVEX ANALYSIS &mdash; 1 to 200
 *   リード文（次の = 行か * 行まで）
 *   =ch I-1　凸集合と分離
 *   *4 Carathéodory の定理 {car}
 *   主張（次の * 行か = 行まで。複数行は空白でつなぐ）
 *
 * *4 / *5 が難易度、末尾の {label} は参照用の名前（省略時は匿名）。
 */
const fromTxt = (src, file) => {
  const out = [];
  let cur = null; // { kind, head, body[] }
  const flush = () => {
    if (!cur) return;
    const body = cur.body.join(' ').trim();
    if (cur.kind === 'part') {
      const [title, en] = cur.head.split('|').map((s) => s.trim());
      out.push(`<div class="partbox">\n<h2 class="part" style="break-before:auto">${title}<span class="en">${en}</span></h2>\n<p class="part-lead">${body}</p>\n</div>`);
    } else if (cur.kind === 'ch') {
      out.push(`<h3 class="ch">${cur.head}<span class="rg">{{RANGE}}</span></h3>`);
      if (body) out.push(`<p class="ch-lead">${body}</p>`);
    } else {
      const m = cur.head.match(/^([45])\s+(.*?)(?:\s*\{([^}]+)\})?$/);
      if (!m) { fail(`${file}: 見出しの書式が不正: ${cur.head}`); return; }
      if (!body) fail(`${file}: 主張が空: ${m[2]}`);
      const stars = m[1] === '5' ? '★★★★★' : '★★★★☆';
      out.push(`<div class="prob line"><div class="prob-head"><span class="no">大問 {{H:${m[3] || '+'}}}</span><span class="ttl">${m[2]}</span><span class="stars">${stars}</span></div>\n<p class="st">${body}</p></div>`);
    }
    cur = null;
  };
  for (const raw of src.split('\n')) {
    const line = raw.trim();
    if (line.startsWith('//')) continue;
    let m;
    if ((m = line.match(/^=part\s+(.*)$/))) { flush(); cur = { kind: 'part', head: m[1], body: [] }; }
    else if ((m = line.match(/^=ch\s+(.*)$/))) { flush(); cur = { kind: 'ch', head: m[1], body: [] }; }
    else if ((m = line.match(/^\*([45]\s.*)$/))) { flush(); cur = { kind: 'prob', head: m[1], body: [] }; }
    else if (line) { if (cur) cur.body.push(line); else fail(`${file}: 見出しの前に本文: ${line.slice(0, 40)}`); }
  }
  flush();
  return out.join('\n\n');
};

let doc = parts.map((f) => {
  const s = fs.readFileSync(path.join(SRC, f), 'utf8');
  return f.endsWith('.txt') ? fromTxt(s, f) : s;
}).join('\n');
doc = doc.replace('/*STYLE*/', () => STYLE);

// ---- 1. 採番 ------------------------------------------------------------------
const labelToNo = new Map();
let counter = 0;
doc = doc.replace(/\{\{H:([^}]+)\}\}/g, (_, label) => {
  counter += 1;
  if (label !== '+') {
    if (labelToNo.has(label)) fail(`ラベルの重複: ${label}`);
    labelToNo.set(label, counter);
  }
  return `{{HN:${counter}}}`;
});

// ---- 2. 参照解決 --------------------------------------------------------------
doc = doc.replace(/\{\{R:([^}]+)\}\}/g, (_, label) => {
  if (!labelToNo.has(label)) {
    fail(`未定義の参照: ${label}`);
    return '??';
  }
  return String(labelToNo.get(label));
});

// ---- 3. 章範囲 ----------------------------------------------------------------
{
  const segs = doc.split('<h3 class="ch">');
  for (let i = 1; i < segs.length; i++) {
    const nums = [...segs[i].matchAll(/\{\{HN:(\d+)\}\}/g)].map((m) => +m[1]);
    // 次の部の扉が混ざっていても、章の問題はその前にしかない
    const cut = segs[i].indexOf('<h2 class="part"');
    const own = cut < 0 ? nums : [...segs[i].slice(0, cut).matchAll(/\{\{HN:(\d+)\}\}/g)].map((m) => +m[1]);
    if (!own.length) fail(`問題のない章: ${segs[i].slice(0, 40)}`);
    // 各章 20 題の規格（崩れていれば警告だけ出す）
    if (own.length !== 20) console.warn(`[warn] 章の題数 ${own.length}: ${segs[i].slice(0, 40)}`);
    segs[i] = segs[i].replace('{{RANGE}}', own.length ? `${own[0]}–${own[own.length - 1]}` : '');
  }
  doc = segs.join('<h3 class="ch">');
}
doc = doc.replace(/\{\{HN:(\d+)\}\}/g, '$1');

// ---- 見出しの抽出（目次・索引・統計で共有）----------------------------------
const heads = [...doc.matchAll(
  /<span class="no">大問 (\d+)<\/span><span class="ttl">(.*?)<\/span><span class="stars">(★+☆*)<\/span>/g,
)].map((m) => ({ no: +m[1], title: m[2], stars: m[3] }));
if (heads.length !== counter) fail(`見出し数 ${heads.length} と採番数 ${counter} が一致しません`);
heads.forEach((h, i) => { if (h.no !== i + 1) fail(`番号が連続していません: ${h.no}`); });

// ---- 4. 目次 ------------------------------------------------------------------
{
  const rows = [];
  const re = /<h2 class="part"[^>]*>(.*?)<span class="en">|<h3 class="ch">(.*?)<span class="rg">(.*?)<\/span>/g;
  let m;
  let partIdx = -1;
  const partRows = [];
  while ((m = re.exec(doc))) {
    if (m[1] !== undefined) {
      partIdx = rows.length;
      rows.push({ head: true, t: m[1].trim(), s: '' });
      partRows.push(partIdx);
    } else {
      rows.push({ head: false, t: m[2].trim(), s: m[3] });
    }
  }
  // 部の範囲 = 最初の章の始点〜最後の章の終点
  partRows.forEach((pi, k) => {
    const end = k + 1 < partRows.length ? partRows[k + 1] : rows.length;
    const chs = rows.slice(pi + 1, end);
    if (chs.length) rows[pi].s = `${chs[0].s.split('–')[0]}–${chs[chs.length - 1].s.split('–')[1]}`;
  });
  const li = rows.map((r) =>
    `<li${r.head ? ' class="head"' : ''}><span class="t">${r.t}</span><span class="s">${r.s}</span></li>`);
  li.push('<li class="head"><span class="t">付録</span><span class="s"></span></li>');
  li.push('<li><span class="t">付録 A　依存の地図</span><span class="s"></span></li>');
  li.push('<li><span class="t">付録 B　参考書対応表</span><span class="s"></span></li>');
  li.push('<li><span class="t">付録 C　定理名索引</span><span class="s"></span></li>');
  doc = doc.replace('<!--TOC-->', `<ul class="toc">\n${li.join('\n')}\n</ul>`);
}

// ---- 5. 索引 ------------------------------------------------------------------
const sortKey = (t) => t.replace(/\$[^$]*\$/g, '').replace(/[（）()・。、,.\s]/g, '');
const latin = [];
const other = [];
for (const h of heads) {
  const k = sortKey(h.title);
  (/^[A-Za-z]/.test(k) ? latin : other).push({ k, ...h });
}
latin.sort((a, b) => a.k.toLowerCase().localeCompare(b.k.toLowerCase(), 'en') || a.no - b.no);
other.sort((a, b) => (a.k < b.k ? -1 : a.k > b.k ? 1 : a.no - b.no));
{
  const block = (arr) => arr.map((h) => `<div><span class="n">${h.no}</span>${h.title}</div>`).join('\n');
  doc = doc.replace('<!--INDEX-->', [
    `<div class="idxhead">A–Z（人名・欧文）　${latin.length} 題</div>`,
    `<div class="idx">\n${block(latin)}\n</div>`,
    `<div class="idxhead">その他（日本語・記号）　${other.length} 題</div>`,
    `<div class="idx">\n${block(other)}\n</div>`,
  ].join('\n'));
}

// ---- 6. 統計 ------------------------------------------------------------------
{
  const s5 = heads.filter((h) => h.stars === '★★★★★').length;
  const s4 = heads.filter((h) => h.stars === '★★★★☆').length;
  if (s4 + s5 !== heads.length) fail('★4/★5 以外の難易度が混ざっています');
  const stat = { TOTAL: heads.length, S4: s4, S5: s5, LATIN: latin.length, OTHER: other.length };
  doc = doc.replace(/\{\{STAT:(\w+)\}\}/g, (_, k) => (k in stat ? String(stat[k]) : (fail(`未知の統計 ${k}`), '??')));
  console.log(`大問 ${heads.length}（★4 ${s4} / ★5 ${s5}）、索引 欧文 ${latin.length} / 和文 ${other.length}`);
}

if (/\{\{[A-Z]+:?[^}]*\}\}/.test(doc)) fail('未解決のトークンが残っています');

// ---- 7. 数式 ------------------------------------------------------------------
const render = (tex, displayMode) => {
  try {
    return katex.renderToString(tex.trim(), { displayMode, throwOnError: true, strict: false });
  } catch (e) {
    fail(`KaTeX: ${e.message}\n  in: ${tex.slice(0, 120)}`);
    return `<span style="color:red">${tex}</span>`;
  }
};
doc = doc.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => render(tex, true));
doc = doc.replace(/\$([^$]{1,400}?)\$/g, (_, tex) => render(tex, false));
if (doc.includes('$')) fail('対応の取れていない $ が残っています');

// ---- 出力 ---------------------------------------------------------------------
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

if (process.exitCode) {
  console.error('エラーがあるため出力を中止しました');
  process.exit(1);
}
fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(HTML_OUT, doc.replace('<!--CSSLINKS-->', WEB_LINKS));
const printPath = path.join(OUT_DIR, 'print-optimization-2000.html');
fs.writeFileSync(printPath, doc.replace('<!--CSSLINKS-->', PRINT_LINKS));

if (process.env.NO_PDF) process.exit(0); // HTML だけ確認したいとき

(async () => {
  const puppeteer = require(path.join(MODULES, 'puppeteer-core'));
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-gpu', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  await page.goto('file://' + printPath, { waitUntil: 'networkidle0', timeout: 0 });
  await page.evaluateHandle('document.fonts.ready');
  await page.pdf({
    path: PDF_OUT,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="width:100%;font-size:8px;color:#8a929c;font-family:sans-serif;' +
      'text-align:center;padding:0 0 4mm"><span class="pageNumber"></span></div>',
    margin: { top: '17mm', bottom: '17mm', left: '17mm', right: '17mm' },
    timeout: 0,
  });
  await browser.close();
  console.log(`PDF: ${PDF_OUT} (${(fs.statSync(PDF_OUT).size / 1024).toFixed(0)} KB)`);
})();
