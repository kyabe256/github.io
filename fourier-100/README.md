# フーリエ解析 100 大問 ― 定義から大定理まで

フーリエ解析を**まったく習っていない人**が、フーリエ解析の大定理を自分の手で証明していくための問題集。全 100 大問すべてが証明問題で、すべてが名前のついた定理。A4 で 51 ページ。**解答は収録していません**（各大問に 3〜6 段の誘導つき）。

予備知識は不要。集合の記号・上限・距離空間・コンパクト性・σ-加法族・ルベーグ積分・収束定理・$L^p$・Hilbert 空間まで、使うものはすべて**第 0 章（10 ページ）に定義 36 項目＋前提定理 12 項目**として収録し、各大問から `(D-12)` `(T-5)` のように参照している。

| ファイル | 内容 |
| --- | --- |
| `fourier-100-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/*.html` | 素材。数式は `$…$` / `$$…$$` で記述 |
| `assets/style.css` | スタイル（`../complex-analysis/assets/style.css` と同系） |
| `build.js` | 結合 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成

| 章・部 | 大問 | 内容 |
| --- | --- | --- |
| 第 0 章 | — | 記号・定義・前提定理（辞書として使う） |
| 第 I 部 | 1–12 | Hölder / Riesz–Fischer / 直交射影 / Parseval / Riesz 表現 / $L^p$ 双対 / Baire / 一様有界性 |
| 第 II 部 | 13–30 | Riemann–Lebesgue / Dirichlet 核 / 局所化 / Dini / Jordan / Fejér / Weierstrass / 完全性 / Bernstein / Gibbs / Cantor–Lebesgue |
| 第 III 部 | 31–38 | du Bois-Reymond / Kolmogorov / Menshov–Rademacher / Riemann の形式積分 / Cantor の一意性 / Stein の最大原理 |
| 第 IV 部 | 39–58 | 反転公式 / Plancherel / Hermite / Riesz–Thorin / Marcinkiewicz / Hausdorff–Young / Poisson 和公式 / 標本化 / Paley–Wiener / Wiener の補題 / Bochner / タウバー型 / HLS |
| 第 V 部 | 59–68 | Vitali / Hardy–Littlewood 極大 / Lebesgue 微分 / Calderón–Zygmund / Hilbert 変換 / M. Riesz / Mikhlin–Hörmander |
| 第 VI 部 | 69–80 | 緩増加超関数 / Dirac 櫛 / Sobolev 空間と埋め込み / Rellich–Kondrachov / 熱・波動・Laplace・Schrödinger / Gagliardo–Nirenberg |
| 第 VII 部 | 81–88 | Haar 測度 / 双対群 / Pontryagin / 有限群と FFT / Peter–Weyl / Stone / Herglotz / Weyl と van der Corput |
| 第 VIII 部 | 89–100 | 等周不等式 / Heisenberg / Hardy / Benedicks / Balian–Low / Landau 密度 / ランダム級数 / Rudin–Shapiro / 空隙級数 / Wiener–Ikehara / 素数定理 / **Roth の定理** |
| 付録 | — | A 学習ルートと依存関係／B 参考書対応表／C 第 0 章の索引 |

分量の目安は 300〜500 時間（週 10 時間で 1 年弱）。

## 流儀

$\mathbb{T}$ 上は $\hat f(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}f e^{-inx}dx$、$\mathbb{R}$ 上は $\hat f(\xi)=\int f(x)e^{-2\pi i x\xi}dx$。Plancherel と Poisson の和公式が定数なしになる。

## ビルド

```sh
npm install katex puppeteer-core @fontsource/noto-serif-jp

mkdir -p build/vendor/files
cp node_modules/@fontsource/noto-serif-jp/japanese-{400,700}.css build/vendor/
cp node_modules/@fontsource/noto-serif-jp/files/noto-serif-jp-japanese-{400,700}-normal.woff2 build/vendor/files/
cp -r node_modules/katex/dist/katex.min.css node_modules/katex/dist/fonts build/vendor/

MODULES=$PWD/node_modules OUT_DIR=$PWD/build CHROME=/path/to/chrome node build.js
```
