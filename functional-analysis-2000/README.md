# 関数解析 2000 大問 ― Hahn–Banach から指数定理まで

関数解析の**定理の主張だけ**を 2000 個並べた問題集。誘導なし、解答なし、準備章なし。全問が名前のついた定理（あるいは名前のついた空間・作用素・不等式に関する定理）で、難易度は ★★★★☆（1394 題）と ★★★★★（606 題）の二段階のみ。A4 で 219 ページ。

| ファイル | 内容 |
| --- | --- |
| `functional-analysis-2000-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/p01a.txt` 〜 `src/p10e.txt` | 問題の素材（簡易記法、1 ファイル 2 章 40 題） |
| `src/*.html` | 表紙・前付け・付録 |
| `assets/style.css` | スタイル |
| `build.js` | 簡易記法の変換 → 採番・目次・索引の生成 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成（通し番号 1–2000、10 部 × 10 章 × 20 題）

| 部 | 番号 | 主題 |
| --- | --- | --- |
| I　基礎原理 | 1–200 | ノルム空間、Hahn–Banach、Baire と三大定理、双対と弱位相、Krein–Milman・Choquet、局所凸空間、樽型空間、Fréchet 空間、不動点、Bochner 積分 |
| II　Hilbert 空間と有界作用素 | 201–400 | Hilbert 幾何、作用素の基本、数域と作用素不等式、コンパクト作用素、Fredholm 指数、Schatten クラス、積分作用素、RKHS、膨張理論、不変部分空間 |
| III　スペクトル理論 | 401–600 | Banach 環、Gelfand 理論、スペクトル定理、非有界作用素、摂動論、スペクトルの分類、散乱理論、半古典解析、非自己共役、第二量子化 |
| IV　半群と発展方程式 | 601–800 | Hille–Yosida、Lumer–Phillips、解析半群、近似と積公式、漸近挙動、正値半群、非線形半群、最大正則性と $H^\infty$ 計算、双曲系、制御 |
| V　Banach 空間の幾何 | 801–1000 | 基底、古典的空間、凸性と平滑性、型と余型、局所理論、作用素イデアル、漸近構造、非線形幾何、Banach 束、記述集合論 |
| VI　関数空間と超関数 | 1001–1200 | $L^p$ と再配置不変空間、超関数、Fourier、Sobolev、補間、核型空間、楕円型作用素、擬微分作用素、Hardy 空間と BMO、関数空間上の作用素 |
| VII　作用素環 | 1201–1400 | C*-環、表現と状態、von Neumann 環、型分類、冨田–竹崎、単射性と核型性、K 理論、分類理論、部分因子と剛性、自由確率論 |
| VIII　非線形関数解析 | 1401–1600 | 微分法、写像度、分岐、直接法、臨界点理論、単調作用素、凸解析、非線形楕円型、分散型・流体、無限次元力学系 |
| IX　確率と関数解析 | 1601–1800 | 確率測度の空間、ガウス測度、chaining、マルチンゲール、Markov 半群と関数不等式、Malliavin、SPDE、大偏差と集中、最適輸送、エルゴードとランダム行列 |
| X　群・幾何・指数と合流 | 1801–2000 | 調和解析、ユニタリ表現、非可換幾何、指数定理、Baum–Connes、数論、距離空間と幾何、量子情報、古典的大定理、大定理の合流 |

付録 A（依存の地図）、付録 B（章ごとの参考書対応表）、付録 C（2000 題の定理名索引・2 段組）。

## 素材の簡易記法

```
=part 第 I 部　位相ベクトル空間と基礎原理 | FOUNDATIONS &mdash; 1 to 200
リード文
=ch I-1　ノルム空間と Banach 空間
*4 Riesz の補題と有限次元性 {riesz-lemma}
主張（1 行）
```

`*4` / `*5` が難易度、末尾の `{label}` は付録から `{{R:label}}` で参照するための名前（省略可）。番号・章範囲・目次・索引・題数はビルド時に自動生成される。各章が 20 題でなければ警告が出る。

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
