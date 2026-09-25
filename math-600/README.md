# 数学 600 大問 ― 複素関数論・関数解析・調和解析・確率論

**定理の主張だけ**を 600 個並べた問題集。誘導なし、解答なし、準備章なし。全問が名前のついた大定理で、難易度は ★★★★☆（229 題）と ★★★★★（371 題）の二段階のみ。A4 で 72 ページ。

| ファイル | 内容 |
| --- | --- |
| `math-600-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/*.html` | 素材。数式は `$…$` / `$$…$$` で記述 |
| `assets/style.css` | スタイル |
| `build.js` | 結合 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成（通し番号 1–600、各部 150 題・12 章）

| 部 | 番号 | 章 |
| --- | --- | --- |
| I　複素関数論 | 1–150 | 正則性の剛性／Cauchy 理論と冪級数／特異点と留数／偏角原理と値分布／Schwarz–Pick と双曲計量／等角写像と Riemann の写像定理／調和関数と境界挙動／無限積・Γ・Hadamard／正規族と複素力学系／解析接続と Riemann 面／ζ と Dirichlet 級数／楕円関数とモジュラー形式 |
| II　関数解析 | 151–300 | Hahn–Banach／Baire 三大定理／弱位相と凸性／Hilbert 空間と作用素／コンパクト作用素と Fredholm／Banach 環と Gelfand／C\*-環とスペクトル定理／非有界作用素／作用素半群／位相ベクトル空間と超関数／Banach 空間の幾何／Schatten クラス |
| III　調和解析 | 301–450 | 級数の収束論／総和法と核／Fourier 変換／補間定理／極大関数／Calderón–Zygmund／Littlewood–Paley／Hardy 空間と BMO／Sobolev 空間／群上の調和解析／不確定性と時間周波数／加法的組合せ論 |
| IV　確率論 | 451–600 | 独立性と 0-1 法則／大数の法則／特性関数と CLT／マルチンゲール／Brown 運動／伊藤解析／SDE／Markov 過程／大偏差原理／エルゴード理論／集中不等式とランダム行列／Lévy 過程 |

付録 A（分野横断の依存地図）、付録 B（章ごとの参考書対応表）、付録 C（600 題の定理名索引・2 段組）。

## 使用許可のルール

第 0 章は置かない代わりに、前付けで次の一行を定めている。

> 番号 *n* の問題を解くとき、1…*n*−1 のすべての結果と、各分野の学部標準の基礎事実は自由に使ってよい。*n* 以降の結果は使ってはならない。

これにより、誘導なしでも「何を仮定してよいか」が完全に決まる。

## 流儀

$\mathbb{T}$ 上は $\hat f(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}fe^{-inx}dx$、$\mathbb{R}^n$ 上は $\hat f(\xi)=\int f(x)e^{-2\pi i x\xi}dx$。記号表は PDF 前付けにある。

## 姉妹編

`../fourier-100/` は同じ主題を**誘導つき・準備章つき**で扱った 100 題。記号や定義が曖昧になったらそちらの第 0 章（定義 36 項目＋前提定理 12 項目）へ戻ること。

## ビルド

```sh
npm install katex puppeteer-core @fontsource/noto-serif-jp

mkdir -p build/vendor/files
cp node_modules/@fontsource/noto-serif-jp/japanese-{400,700}.css build/vendor/
cp node_modules/@fontsource/noto-serif-jp/files/noto-serif-jp-japanese-{400,700}-normal.woff2 build/vendor/files/
cp -r node_modules/katex/dist/katex.min.css node_modules/katex/dist/fonts build/vendor/

MODULES=$PWD/node_modules OUT_DIR=$PWD/build CHROME=/path/to/chrome node build.js
```

付録 C の索引は本文から機械的に生成している（`src/97-appendix-c.html`）。本文の定理名を変更したら索引も再生成すること。
