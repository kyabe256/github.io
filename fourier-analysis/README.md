# フーリエ解析 演習問題集

理工系学部 2・3 年 〜 大学院入試レベルのオリジナル問題集。全 22 大問・小問 109 題、A4 で 22 ページ。**解答は収録していません**（付録 A に基礎編の答え、付録 B に第 I 部以降への一行ヒントのみ）。

| ファイル | 内容 |
| --- | --- |
| `fourier-analysis-problems.pdf` | 問題集本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/*.html` | 素材。数式は `$…$` / `$$…$$` で記述 |
| `assets/style.css` | スタイル（`../complex-analysis/assets/style.css` と同じもの） |
| `build.js` | 結合 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成

- 第 0 部　基礎編（★☆☆☆☆〜★★★☆☆、24 題）Fourier 級数の計算、Parseval と級数の和、係数の減衰と滑らかさ、Dirichlet 核と Gibbs 現象、Fourier 変換の計算
- 第 I 部　収束論（40 題のうち 20 題）局所化原理、Dini、Fejér、$L^2$ 理論、du Bois-Reymond の発散例、Bernstein の定理
- 第 II 部　Fourier 変換　反転公式と Schwartz 空間、Plancherel、Poisson の和公式、不確定性原理（Heisenberg・Hardy）
- 第 III 部　応用　熱・波動・Laplace 方程式、標本化定理と Paley–Wiener、等周不等式、Weyl の一様分布定理
- 第 IV 部　発展　緩増加超関数、DFT と FFT、Hilbert 変換、Bochner・Wiener、特性関数と中心極限定理

## 流儀

$\hat f(\xi)=\int f(x)e^{-2\pi i x\xi}dx$ に統一（Plancherel と Poisson の和公式が定数なしの形になる）。詳細は PDF の前付けを参照。

## ビルド

```sh
npm install katex puppeteer-core @fontsource/noto-serif-jp

mkdir -p build/vendor/files
cp node_modules/@fontsource/noto-serif-jp/japanese-{400,700}.css build/vendor/
cp node_modules/@fontsource/noto-serif-jp/files/noto-serif-jp-japanese-{400,700}-normal.woff2 build/vendor/files/
cp -r node_modules/katex/dist/katex.min.css node_modules/katex/dist/fonts build/vendor/

MODULES=$PWD/node_modules OUT_DIR=$PWD/build CHROME=/path/to/chrome node build.js
```
