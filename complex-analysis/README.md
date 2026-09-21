# 複素関数論 演習問題集

理工系学部 2・3 年 〜 大学院入試レベルのオリジナル問題集。全 20 大問・小問 108 題、A4 で 24 ページ。**解答は収録していません**（付録 A に大問ごとの一行ヒント、付録 B に計算問題の最終値のみ）。

| ファイル | 内容 |
| --- | --- |
| `complex-analysis-problems.pdf` | 問題集本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/*.html` | 素材。数式は `$…$` / `$$…$$` で記述 |
| `build.js` | 結合 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成

- 第 I 部　正則性の基礎（Cauchy–Riemann、Liouville、べき級数、一致の定理）
- 第 II 部　Cauchy 理論の技法（積分公式、Morera・鏡像原理、Laurent 展開）
- 第 III 部　留数計算の華（実定積分 I・II、級数の総和）
- 第 IV 部　幾何学的関数論（偏角原理、Schwarz の補題、等角写像、Poisson 核）
- 第 V 部　発展（無限積と Γ、ζ、Jensen と Blaschke、鞍点法、Riemann の写像定理、Weierstrass の ℘）

## ビルド

```sh
npm install katex puppeteer-core @fontsource/noto-serif-jp

# 印刷版が参照するローカル資源を用意する
mkdir -p build/vendor/files
cp node_modules/@fontsource/noto-serif-jp/japanese-{400,700}.css build/vendor/
cp node_modules/@fontsource/noto-serif-jp/files/noto-serif-jp-japanese-{400,700}-normal.woff2 build/vendor/files/
cp -r node_modules/katex/dist/katex.min.css node_modules/katex/dist/fonts build/vendor/

MODULES=$PWD/node_modules OUT_DIR=$PWD/build CHROME=/path/to/chrome node build.js
```

`CHROME` には Chromium/Chrome の実行ファイルを指定する。`index.html` と `complex-analysis-problems.pdf` が更新される。
