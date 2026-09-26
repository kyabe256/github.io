# 非線形最適化 2000 大問 ― 凸解析から最適輸送まで

非線形最適化の**定理の主張だけ**を 2000 個並べた問題集。誘導なし、解答なし、準備章なし。全問が名前のついた定理（あるいは名前のついた方法の収束・計算量・最適性の定理）で、難易度は ★★★★☆（1374 題）と ★★★★★（626 題）の二段階のみ。A4 で 227 ページ。

| ファイル | 内容 |
| --- | --- |
| `optimization-2000-problems.pdf` | 本体（PDF） |
| `index.html` | Web 版（KaTeX / Noto Serif JP を CDN から読み込む） |
| `src/p01a.txt` 〜 `src/p10e.txt` | 問題の素材（簡易記法、1 ファイル 2 章 40 題） |
| `src/*.html` | 表紙・前付け・付録 |
| `assets/style.css` | スタイル |
| `build.js` | 簡易記法の変換 → 採番・目次・索引の生成 → KaTeX でサーバサイド描画 → PDF 化 |

## 構成（通し番号 1–2000、10 部 × 10 章 × 20 題）

| 部 | 番号 | 主題 |
| --- | --- | --- |
| I　凸解析 | 1–200 | 分離定理、錐と選択肢定理、多面体、凸幾何、凸関数、共役、劣微分、平滑化、単調作用素、無限次元 |
| II　最適性条件 | 201–400 | 存在、無制約の条件、Lagrange 乗数、KKT、制約想定、二階条件、感度解析、誤差限界、二次計画、多目的 |
| III　双対理論 | 401–600 | Lagrange 双対、minimax、摂動双対、LP・錐計画・SDP の双対、拡張 Lagrangian、S-補題、離散と無限次元の双対 |
| IV　無制約アルゴリズム | 601–800 | 直線探索、勾配法、Newton・準 Newton、信頼領域、CG、最小二乗、三次正則化、非凸一階法、導関数不要法 |
| V　制約付きアルゴリズム | 801–1000 | ペナルティ・障壁、ALM、SQP、LP と錐の内点法、有効制約法、Frank–Wolfe、楕円体法、単体法、変分不等式 |
| VI　一次法と計算量 | 1001–1200 | 加速、劣勾配、近接勾配、ミラー降下、主双対法、演算子分割、座標降下、PEP、分散最適化、適応的方法 |
| VII　非平滑・変分解析 | 1201–1400 | Clarke・Mordukhovich、変分原理、計量正則性、エピ収束、prox-regularity、定義可能最適化、二階変分解析、DC |
| VIII　錐計画と緩和 | 1401–1600 | SOCP、SDP、SOS、Positivstellensatz、共正値、SDP 近似、圧縮センシング、低ランク回復、非凸景観、凸代数幾何 |
| IX　確率・オンライン・ロバスト | 1601–1800 | 確率近似、確率的凸最適化、分散削減、オンライン学習、バンディット、確率計画、ロバスト・DRO、RL、学習理論 |
| X　変分法・制御・均衡 | 1801–2000 | 古典変分法、直接法、最大原理、HJB と粘性解、LQ 制御、変分不等式、ゲーム、最適輸送、二段階最適化、合流 |

付録 A（依存の地図）、付録 B（章ごとの参考書対応表）、付録 C（2000 題の定理名索引・2 段組）。

## 素材の簡易記法

```
=part 第 I 部　凸解析 | CONVEX ANALYSIS &mdash; 1 to 200
リード文
=ch I-1　凸集合と分離
*4 最近点射影定理 {proj}
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
