# 複素関数論 演習問題集

理工系学部 2・3 年 〜 大学院入試レベルのオリジナル問題集。2 巻あわせて全 40 大問・小問 204 題。**解答は収録していません**（大問ごとの一行ヒントと、計算問題の最終値のみ）。

| ファイル | 内容 |
| --- | --- |
| `complex-analysis-problems.pdf` | 第 I 巻（20 大問 / 108 題、24 ページ） |
| `complex-analysis-problems-vol2.pdf` | 第 II 巻 基礎編＋挑戦編（20 大問 / 96 題、18 ページ） |
| `index.html`, `volume2.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/*.html`, `src2/*.html` | 素材。数式は `$…$` / `$$…$$` で記述 |
| `assets/style.css` | 2 巻共通のスタイル |
| `build.js` | 結合 → KaTeX でサーバサイド描画 → PDF 化（2 巻同時） |

## 第 I 巻の構成

- 第 I 部　正則性の基礎（Cauchy–Riemann、Liouville、べき級数、一致の定理）
- 第 II 部　Cauchy 理論の技法（積分公式、Morera・鏡像原理、Laurent 展開）
- 第 III 部　留数計算の華（実定積分 I・II、級数の総和）
- 第 IV 部　幾何学的関数論（偏角原理、Schwarz の補題、等角写像、Poisson 核）
- 第 V 部　発展（無限積と Γ、ζ、Jensen と Blaschke、鞍点法、Riemann の写像定理、Weierstrass の ℘）

## 第 II 巻の構成

- 第 0 部　基礎編（★☆☆☆☆〜★★★☆☆、44 題）複素数の代数と幾何、初等関数と多価性、正則性の判定、線積分、Cauchy の積分公式、Taylor / Laurent 展開、留数、零点の数え上げ、等角写像の基本
- 第 VI 部　挑戦編（★★★★★、52 題）Weierstrass の因数分解、Mittag-Leffler、Runge、Hadamard の因数分解、Bloch–Schottky–Picard、単葉関数と Koebe 1/4、θ と ζ の関数等式、素数定理、複素力学系、Schwarz–Christoffel

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
