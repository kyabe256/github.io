# 大学入試 数学シリーズ 執筆ブリーフ（全エージェント共通）

作業ディレクトリ（以下 SP）: /tmp/claude-0/-home-user-github-io/3e455572-8e58-53b8-8091-3d8aa7fa47ea/scratchpad
本のフォルダ: SP/books/n_math_k（教科書・講義編）, SP/books/n_math_s（参考書・解法整理編）, SP/books/n_math_m（問題集・演習編）
ビルダー: SP/books/nyushi.py（読むだけ。**変更禁止**）。meta.json も**変更禁止**。git 操作も**禁止**。
自分に割り当てられたファイル以外は**書き換えない**（他のエージェントが同時に作業している）。

## 読者と水準
- 大学入試（共通テスト〜国公立二次・難関私大）を目指す高校生。新課程（数学I・A・II・B・III・C）。
- 数学B＝数列・統計的な推測、数学C＝ベクトル・複素数平面・2次曲線（媒介変数・極座標を含む）、数学A＝図形の性質・場合の数と確率・数学と人間の活動（整数）、数学I のデータの分析には外れ値・仮説検定の考え方を含む。
- 日本語で、わかりやすく、しかし数学的に正確に。高校の標準的な記号を使う（≧ は `\geqq`、≦ は `\leqq`、≒ は `\fallingdotseq`、組合せ `{}_n\mathrm{C}_r`、ベクトル `\vec{a}` や `\overrightarrow{\mathrm{AB}}`）。
- **問題はすべてオリジナル**。特定の大学名・年度を出典として書かない（「典型」「頻出」「共通テスト形式」「二次試験レベル」などのタグは可）。

## 共通の書式ルール（必ず守る）
- 数式はインライン `$...$` のみ。**`$$...$$` は使わない**（大きく見せたいときは `$\displaystyle ...$`）。
- 数式中の `<` `>` はビルダーが自動で `\lt` `\gt` に直すのでそのまま書いてよい（数式の外で不等号を書くときは `&lt;` `&gt;` か全角 ＜ ＞）。
- `\begin{cases} ... \end{cases}` などは使ってよい。KaTeX で通る記法だけを使う。
- 太字は `<b>`、答えの強調は `\boldsymbol{...}` か `<b>`。
- 図が有効なところ（グラフ・図形）は `<svg class="fig" width=".." height=".." viewBox="..">` で描いてよい。座標は Python で計算して正確に。文字は font-size 10〜12。
- 1つの章の分量の目安は見本（第1章）と同程度〜1.5倍。

## 書式の見本（まず必ず読む）
- 教科書: SP/books/n_math_k/part01.html
- 参考書: SP/books/n_math_s/part01.html
- 問題集: SP/books/n_math_m/p01.py
- ビルダーで使える class: nyushi.py の CSS を参照（point, lect, ex(+solx), chk, ans, aim, warn, memo / pat(when, how, pex, pnote) / problems は p01.py の形式）。

### 教科書（n_math_k）の章の構成
`<!--CH n-->` で始め、
1. `<div class="box point">` 章の要点（定理・公式を3〜5行）
2. `<h3>講義k　見出し</h3>` + `<div class="box lect">`（なぜそうなるか・導出・考え方）+ `<div class="box ex">例題… <div class="solx"><b>解</b>…</div></div>` を3〜4セット
3. `<div class="box chk">` 確認問題（4問前後）
4. `<div class="box aim">` 入試の着眼点
5. `<h3 class="deep">講義k　…</h3>` 発展的な話題（証明・背景・応用）1つ
6. `<div class="box warn">` よくあるミス
7. 最後に `<div class="box ans">` 確認問題の答え（略解）

### 参考書（n_math_s）の章の構成
`<!--CH n-->` で始め、解法カードを 7〜9 枚：
```
<div class="pat"><h4>カードの題名（解法の要点を一言で）</h4>
<div class="when">どんな問題のときに使うか</div>
<div class="how">解き方の手順・公式・判断基準</div>
<div class="pex">例題文<br><b>解</b>　簡潔な解答</div>
<div class="pnote">失点しやすい注意点（任意）</div>
</div>
```
番号はビルダーが自動でつけるので書かない。章の最後に `<div class="box memo">` で公式の一覧表（`<table class="l w">`）を入れてもよい。

### 問題集（n_math_m）の章の構成
章ごとに Python ファイル `pNN.py`（NN は2桁の章番号）。p01.py と同じ形式：
- `CH = {n: {"goal": "...", "items": [ {"lv":"A|B|C", "tag":"任意", "q": r"...", "a": r"答えの要約", "s": r"くわしい解説（<b>ポイント</b>：… で締める）"}, ... ]}}`
- 1章あたり **A 4問・B 4〜5問・C 2問**（合計10〜11問）。A＝教科書・共通テストの基礎、B＝入試の典型、C＝難関大レベル。
- `def verify():` で、**数値・式で答えが出る問題はすべて sympy 等で検算**する（assert）。証明問題は、使う等式や数値例を検算する。確率は Fraction や全列挙で、整数問題は総当たりで確認する。
- 文字列は raw 文字列 `r"..."` で書く（バックスラッシュのため）。

## 正確さの確認（最重要）
- 例題・確認問題・カードの例題・問題の答えは、**すべて Python（sympy / fractions / 総当たり）で検算してから**書く。検算スクリプトは SP/books/scratch_<自分の担当名>/ に置いてよい。
- 解答の途中式も、その通りに計算すると答えになることを確かめる。自己矛盾した解説（「…ではなく」「と迷ったら」など書きながら訂正する文）を残さない。
- 定義・定理の記述が教科書的に正しいか、条件（$a\gt0$、$a\neq1$ など）が抜けていないかを確認。

## 試し刷り（自分の担当章だけ）
SP/books で：
- 教科書・参考書: `ONLY=a-b OUT=book_<担当名>.html python3 -I nyushi.py n_math_k`（参考書なら n_math_s）
- 問題集: `python3 -I merge_probs.py n_math_m a-b probs_<担当名>.json`（a-b は担当の章範囲。p{a..b}.py を検算しながら結合する）→ `ONLY=a-b OUT=book_<担当名>.html PROBS=probs_<担当名>.json python3 -I nyushi.py n_math_m`
SP で：`node render_n.js books/<フォルダ>/<担当名>.pdf books/<フォルダ>/book_<担当名>.html` → 出力の `katex errors: 0` を確認。
`pdftoppm -r 60 -png -f 1 -l 4 books/<フォルダ>/<担当名>.pdf SP/books/scratch_<担当名>/pg` などで画像にし、Read で数ページ目視（数式の崩れ・図・レイアウト）。
最後に試し刷りの html/pdf/json は消してよい（担当の part/p ファイルは残す）。

## 完了報告（最終メッセージ）
- 書いたファイル名、章ごとの分量（教科書：講義数・例題数／参考書：カード枚数／問題集：A/B/C の問題数）
- 検算した内容の要約、KaTeX エラー数、目視で直した点
- 自信のない箇所があれば正直に列挙
