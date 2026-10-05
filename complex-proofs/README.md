# 複素関数論 証明問題集 ― 授業 13 回の「計算」をすべて証明する 260 題

学部の「複素関数論」（全 13 回、計算中心の授業）の授業計画に章立てを合わせた**証明だけの問題集**。授業で計算の道具として使う事実を、一つ残らず自分で証明する。誘導なし、解答なし。難易度は ★★★☆☆（105 題、授業の定理そのもの）、★★★★☆（121 題、一歩先）、★★★★★（34 題、授業範囲の外）。A4 で 36 ページ。

| ファイル | 内容 |
| --- | --- |
| `complex-proofs-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/l01.txt` 〜 `src/l07.txt` | 問題の素材（簡易記法、1 ファイル 2 回分） |
| `src/*.html` | 表紙・前付け・付録 |
| `assets/style.css` | スタイル |
| `build.js` | 簡易記法の変換 → 採番・目次・索引の生成 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成（通し番号 1–260、13 章 × 20 題）

| 部 | 授業回 | 番号 | 主題 |
| --- | --- | --- | --- |
| I | 第 1〜4 回 | 1–80 | 複素数と複素平面、複素関数の視覚化（一次分数変換など）、初等関数、極限と連続性・級数 |
| II | 第 5〜6 回 | 81–120 | 複素微分、冪級数の項別微分、Cauchy–Riemann の方程式、調和関数 |
| III | 第 7〜9 回 | 121–180 | 複素積分、回転数、Goursat の補題と Cauchy の積分定理、Cauchy の積分公式とその帰結 |
| IV | 第 10〜12 回 | 181–240 | Taylor・Laurent 展開、孤立特異点、留数定理、偏角の原理と Rouché、実積分への応用 |
| V | 第 13 回 | 241–260 | 総合問題（整関数の分類、Phragmén–Lindelöf、Jensen、正弦積、Montel、最終問題） |

付録 A（依存の地図）、付録 B（授業回ごとの参考書対応表）、付録 C（定理名索引）。

## 素材の簡易記法

```
=part 第 I 部　複素数と初等関数 | NUMBERS AND ELEMENTARY FUNCTIONS &mdash; 1 to 80
リード文
=ch 第 1 回　複素数と複素平面
*3 de Moivre の公式 {demoivre}
主張（1 行）
```

`*3` / `*4` / `*5` が難易度、末尾の `{label}` は付録から `{{R:label}}` で参照するための名前（省略可）。番号・章範囲・目次・索引・題数はビルド時に自動生成される。各章が 20 題でなければ警告が出る。

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
