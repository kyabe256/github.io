# 複素関数論で登る大定理 ― 授業の道具だけで、18 の大定理の山頂へ

学部の複素関数論で習う道具（Cauchy の積分定理・積分公式、Laurent 展開、留数定理、Rouché の定理）だけを足場に、数学史に残る大定理まで登る証明問題集。1 章 = 1 本の登山道（12 題）で、補題を登って章末で大定理を証明する。誘導なし、解答なし。難易度は ★★★★☆（154 題）と ★★★★★（62 題）。A4 で 34 ページ。

| ファイル | 内容 |
| --- | --- |
| `complex-summits-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/b01.txt` 〜 `src/b09.txt` | 問題の素材（簡易記法、1 ファイル 2 章 24 題） |
| `src/*.html` | 表紙・前付け・付録 |
| `assets/style.css` | スタイル |
| `build.js` | 簡易記法の変換 → 採番・目次・索引の生成 → KaTeX でサーバサイド描画 → PDF 化 |

## 18 の山頂（通し番号 1–216、18 章 × 12 題）

| 部 | 章 | 山頂 |
| --- | --- | --- |
| I　位相と等角写像 | 1–4 | Brouwer・Borsuk–Ulam・ハムサンドイッチ／Riemann の写像定理／Koebe の 1/4 定理と Bieberbach の不等式／Picard の大定理 |
| II　関数の構造 | 5–9 | Weierstrass・Mittag-Leffler／Hadamard の因数分解と Laguerre の定理／Gamma 関数と Stirling の公式／楕円関数と三次曲線の群構造／テータ関数と Jacobi の四平方定理 |
| III　解析学 | 10–13 | $e,\pi$ の超越性と Gelfond–Schneider／Paley–Wiener と Hardy の不確定性原理／Runge の近似定理／Riesz–Thorin・Carlson・Müntz–Szász |
| IV　数論 | 14–18 | ゼータ関数の関数等式と Riemann–von Mangoldt／Gauss 和と平方剰余の相互法則／分割数の Hardy–Ramanujan 公式／Dirichlet の算術級数定理／素数定理 |

付録 A（依存の地図）、付録 B（章ごとの参考書）、付録 C（定理名索引）。

## 素材の簡易記法

```
=part 第 I 部　位相と等角写像の大定理 | TOPOLOGY AND CONFORMAL MAPS &mdash; 1 to 48
リード文
=ch 第 2 章　Riemann の写像定理
*5 Riemann の写像定理 {rmt}
主張（1 行）
```

`*3` / `*4` / `*5` が難易度、末尾の `{label}` は付録から `{{R:label}}` で参照するための名前（省略可）。番号・章範囲・目次・索引・題数はビルド時に自動生成される。各章が 12 題でなければ警告が出る。

## ビルド

```sh
npm install katex puppeteer-core @fontsource/noto-serif-jp

mkdir -p build/vendor/files
cp node_modules/@fontsource/noto-serif-jp/japanese-{400,700}.css build/vendor/
cp node_modules/@fontsource/noto-serif-jp/files/noto-serif-jp-japanese-{400,700}-normal.woff2 build/vendor/files/
cp -r node_modules/katex/dist/katex.min.css node_modules/katex/dist/fonts build/vendor/

MODULES=$PWD/node_modules OUT_DIR=$PWD/build CHROME=/path/to/chrome node build.js
# HTML だけ確認するとき: NO_PDF=1 を付ける
```
