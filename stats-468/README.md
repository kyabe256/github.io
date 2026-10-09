# 確率と統計的推測 468 大問 ― 確率・統計／統計的推測 I／統計的推測 II

学部の三科目「確率・統計」「統計的推測 I」「統計的推測 II」の授業計画全 39 回を 39 章にした証明問題集。授業で公式として使う事実を証明し、各章はその回の主題の先にある大定理で終わる。誘導なし、解答なし。難易度は ★★★☆☆（75 題）、★★★★☆（310 題）、★★★★★（83 題）。A4 で 62 ページ。

| ファイル | 内容 |
| --- | --- |
| `stats-468-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/s01.txt` 〜 `src/s13.txt` | 問題の素材（簡易記法、1 ファイル 3 章 36 題） |
| `src/*.html` | 表紙・前付け・付録 |
| `assets/style.css` | スタイル |
| `build.js` | 簡易記法の変換 → 採番・目次・索引の生成 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成（通し番号 1–468、3 部 × 13 章 × 12 題）

| 部 | 科目 | 番号 | 主な山頂 |
| --- | --- | --- | --- |
| I | 確率・統計 | 1–156 | Kolmogorov の 0-1 法則、Galton–Watson の絶滅定理、Cramér の大偏差定理、Pólya の再帰定理、Sanov、Raikov、Lukacs、Cramér の分解定理、Darmois–Skitovich、Glivenko–Cantelli |
| II | 統計的推測 I | 157–312 | 極値分布、Etemadi の強法則、Berry–Esseen、Geary、Hotelling の $T^2$、Basu、Stein のパラドックス、有効推定量と指数型分布族、Le Cam の超有効性定理、Wald の一致性、MLE の漸近有効性、Wald–Wolfowitz、Chernoff–Stein |
| III | 統計的推測 II | 313–468 | 両側 $z$ 検定の UMPU 性、Hodges–Lehmann の 108/125、Benjamini–Hochberg、Stein の二段階法、Box の非頑健性、二標本 $t$ の UMPU 性、Bartlett、Fisher の正確検定の UMPU 性、Pearson の定理、Chernoff–Lehmann、線形仮説の $F$ 検定、Hoerl–Kennard、Wilks の定理 |

付録 A（依存の地図）、付録 B（授業回ごとの参考書対応表、テキストの節はシラバスの記載に従う）、付録 C（定理名索引）。

## 素材の簡易記法

```
=part 第 I 部　確率・統計 ― 確率変数と確率分布 | PROBABILITY AND DISTRIBUTIONS &mdash; 1 to 156
リード文
=ch I-1　確率・条件付き確率・独立性
*3 確率の公理からの基本性質 {axioms}
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
