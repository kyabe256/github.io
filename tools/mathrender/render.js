/**
 * TeX の数式を SVG に変換する。
 *
 * WeasyPrint は MathML を組めないため、数式は事前にベクタ化して本文へ埋め込む。
 * 図版がすでにインラインSVGで確実に組めているので、同じ経路に載せる。
 *
 * 標準入力から JSON を受け取り、標準出力へ JSON を返す。
 *   入力: [{ "id": "...", "tex": "x \\in X", "display": false }, ...]
 *   出力: [{ "id": "...", "svg": "<svg .../>" }, ...]
 *
 * フォントは各SVGの内部にパスとして閉じ込める（fontCache: 'none'）。
 * グリフを文書全体で共有する 'global' は <use> の跨ぎ参照になり、
 * WeasyPrint で解決される保証がないため採らない。
 */
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { SVG } = require('mathjax-full/js/output/svg.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'none' });
const doc = mathjax.document('', { InputJax: tex, OutputJax: svg });

function readStdin() {
  return new Promise((resolve, reject) => {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (d) => { buf += d; });
    process.stdin.on('end', () => resolve(buf));
    process.stdin.on('error', reject);
  });
}

async function main() {
  const items = JSON.parse(await readStdin());
  const out = [];
  for (const it of items) {
    try {
      const node = doc.convert(it.tex, { display: !!it.display, em: 16, ex: 8 });
      out.push({ id: it.id, svg: adaptor.innerHTML(node) });
    } catch (e) {
      out.push({ id: it.id, error: String(e && e.message ? e.message : e) });
    }
  }
  process.stdout.write(JSON.stringify(out));
}

main().catch((e) => { console.error(e); process.exit(1); });
