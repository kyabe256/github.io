"""点数をつけない「理解度チェック」（第1〜4章）を check.html に出力する。
問題は確認テストと同じ。答えは drills.json（sympy で検算済み）と、ここでの sympy 検算による。"""
import json, re
import sympy as sp

D = json.load(open("drills.json", encoding="utf-8"))
NAMES = {"1": "正負の数", "2": "文字式の計算", "3": "一次方程式", "4": "連立方程式"}
HOWTO = {"1": "次の計算をしなさい。", "2": "次の式を計算しなさい。", "3": "次の方程式を解きなさい。", "4": "次の連立方程式を解きなさい。"}
PICK = {"1": [0, 1, 7, 8, 9], "2": [1, 3, 2, 13, 15], "3": [0, 1, 2, 3, 18], "4": [0, 1, 2, 4, 5]}
# 解き直し用の類題（同じタイプ）。None は下の CUSTOM を使う
RETRY = {"1": [15, 16, 12, None, 14], "2": [10, 6, 9, 18, 20], "3": [8, 9, 11, 10, 21], "4": [9, 6, 7, 11, 12]}
CUSTOM = {("1", 3): ("(-3)^2 - 2 \\times 4", str((-3) ** 2 - 2 * 4))}

# 各計算問題の「よくあるまちがい」と「読み直す場所」。数値は下で検算する
NOTES = {
    1: ("$-11+3$ を $-14$ や $8$ にしてしまう（たし算の向きの混乱）", "第1章 じっくり解説②（数直線の移動）"),
    2: ("$28$ と答える（マイナスが3個＝奇数なのに＋にした）", "第1章 ★ここだけ覚える（符号のルール）"),
    3: ("$-6$（わり算の符号ミス）や $6$（$+(-1)$ を $+1$ にした）", "第1章 ★（符号）・じっくり解説⑤"),
    4: ("$-7$（$(-2)^2$ を $-4$ にした）、$9$（$(4-1)\\times3$ と左から順に計算）", "第1章 累乗の注意・じっくり解説④（計算の順序）"),
    5: ("$16$（$-2^2$ を $4$ にした）", "第1章 累乗の注意"),
    6: ("$3x+3y$（$-3\\times(-4y)$ を $-12y$ にした）", "第2章 例題・⚠よくあるミス"),
    7: ("$2x$ など（$-2$ を後ろの $+3y$ にかけ忘れる、符号ミス）", "第2章 例題・⚠よくあるミス"),
    8: ("$-44x+30y$（$-(-6)$ を $-6$ のまま計算した）", "第1章 じっくり解説②（マイナスを引く）・第2章"),
    9: ("$\\frac{5-35x}{12}$（$-3(-5x-1)$ の符号をまちがえた）", "第2章 ⚠よくあるミス（通分後のかっこ）"),
    10: ("$\\frac{-11x-26}{10}$（$-2(-3x-3)$ の符号をまちがえた）", "第2章 ⚠よくあるミス（通分後のかっこ）"),
    11: ("$x=\\frac{21}{5}$（移項で符号を変え忘れ $10x=42$ にした）", "第3章 ★・じっくり解説②（等式の性質）"),
    12: ("$x=-4$（$-3x=-12$ を $-3$ でわるときの符号ミス）", "第3章 ★・第1章 ★（わり算の符号）"),
    13: ("$x=8$（$-3x=24$ のマイナスを落とした）", "第3章 ★・第1章 ★（わり算の符号）"),
    14: ("$x=3$（$-12$ を右へ移すとき符号を変え忘れ $4x=12$ にした）", "第3章 じっくり解説②（移項）"),
    15: ("$x=13$（右辺の「$+1$」に $12$ をかけ忘れた）", "第3章 じっくり解説③（係数が分数のとき）"),
}
SIMUL_NOTE = ("1つの文字を消すときの<b>ひき算で符号をまちがえる</b>、片方を求めたあとの<b>代入で計算ミス</b>が多い。"
              "求めた $x,y$ を<b>2本の式の両方に代入して確かめる</b>習慣をつけると防げる。", "第4章 例題・じっくり解説②（加減法と代入法）")

# --- まちがい例の数値が本当にその誤りから出ることを検算 ---
x, y = sp.symbols("x y")
assert -11 + 3 - 12 == -20 and (-7) * (-1) * (-4) == -28 and -45 // -9 + (-1) == 4
assert (-2) ** 2 - 1 * 3 == 1 and -4 - 3 == -7 and (4 - 1) * 3 == 9
assert -(2 ** 2) + (-6) * (-2) == 8 and 4 + 12 == 16
assert sp.expand(5 * (3 * x + 3 * y) - 3 * (4 * x - 4 * y)) == 3 * x + 27 * y
assert sp.expand(15 * x + 15 * y - 12 * x - 12 * y) == 3 * x + 3 * y
assert sp.expand(-4 * (2 * x - 3 * y) + 6 * (6 * x - 3 * y)) == 28 * x - 6 * y
assert sp.expand(-4 * (2 * x - 3 * y) - 6 * (6 * x - 3 * y)) == -44 * x + 30 * y
assert sp.expand(4 * (2 - 5 * x) - 3 * (-5 * x - 1)) == 11 - 5 * x
assert sp.expand(4 * (2 - 5 * x) - (15 * x + 3)) == 5 - 35 * x
assert sp.expand(5 * (-x - 4) - 2 * (-3 * x - 3)) == x - 14
assert sp.expand(5 * (-x - 4) - (6 * x + 6)) == -11 * x - 26
assert sp.solve(10 * x - 42, x) == [sp.Rational(21, 5)]
assert sp.solve(sp.Eq(2 * (x + 4), 3 * (x - 2) + 1), x) == [13]
assert sp.solve(4 * x - 12, x) == [3]

# --- 文章題（確認テストと同じ） ---
WORD = [
    ("代金", "1個 150 円のパンと 1個 90 円のおにぎりを合わせて 12 個買ったら、代金は 1440 円でした。パンとおにぎりをそれぞれ何個買いましたか。",
     sp.Eq(150 * x + 90 * (12 - x), 1440), "パンを $x$ 個とすると　$150x+90(12-x)=1440$", "パン 6 個、おにぎり 6 個", {x: 6}, "第3章 例題（パンとおにぎり）"),
    ("過不足", "何人かの子どもにあめを配ります。1人に 4 個ずつ配ると 10 個余り、6 個ずつ配ると 8 個足りません。子どもの人数とあめの数を求めなさい。",
     sp.Eq(4 * x + 10, 6 * x - 8), "子どもを $x$ 人とすると　$4x+10=6x-8$", "子ども 9 人、あめ 46 個", {x: 9}, "第3章 じっくり解説④【過不足】"),
    ("速さ", "弟が家を出て分速 70 m で歩き始めました。その 12 分後に、兄が分速 210 m の自転車で同じ道を追いかけました。兄は出発してから何分後に弟に追いつきますか。",
     sp.Eq(210 * x, 70 * (x + 12)), "兄が出発して $x$ 分後に追いつくとすると　$210x=70(x+12)$", "6 分後", {x: 6}, "第3章 じっくり解説④【速さ】"),
    ("つるかめ算", "つるとかめが合わせて 25 匹います。足の数は合わせて 70 本です。つるとかめはそれぞれ何匹いますか。",
     [sp.Eq(x + y, 25), sp.Eq(2 * x + 4 * y, 70)], "つるを $x$ 羽、かめを $y$ 匹とすると　$\\begin{cases}x+y=25\\\\2x+4y=70\\end{cases}$", "つる 15 羽、かめ 10 匹", {x: 15, y: 10}, "第4章 じっくり解説③【つるかめ算】"),
    ("代金（連立）", "りんご 3 個となし 2 個を買うと 720 円、りんご 1 個となし 4 個を買うと 840 円です。りんご 1 個、なし 1 個の値段をそれぞれ求めなさい。",
     [sp.Eq(3 * x + 2 * y, 720), sp.Eq(x + 4 * y, 840)], "りんご 1 個を $x$ 円、なし 1 個を $y$ 円とすると　$\\begin{cases}3x+2y=720\\\\x+4y=840\\end{cases}$", "りんご 120 円、なし 180 円", {x: 120, y: 180}, "第4章 じっくり解説③"),
]
for w in WORD:
    eq, sol = w[2], w[5]
    got = sp.solve(eq, list(sol)) if isinstance(eq, list) else {x: sp.solve(eq, x)[0]}
    assert got == sol, (got, sol)
assert 4 * 9 + 10 == 46 == 6 * 9 - 8

EXPLAIN = [
    ("$(-3)\\times(-2)$ の答えはなぜプラス（$+6$）になるのですか。理由を説明しなさい。",
     "$(-3)\\times2=-6,\\ (-3)\\times1=-3,\\ (-3)\\times0=0$ と、かける数が 1 減るごとに答えは 3 ずつ増えている。このきまりを続けると $(-3)\\times(-1)=3$、$(-3)\\times(-2)=6$ になる。"
     "（または「$-$ をかける＝向きを反対にする」ので、反対を 2 回するとプラスの向きに戻る）",
     "「$(-3)\\times2,\\ (-3)\\times1,\\ (-3)\\times0$ と順に計算してみよう。答えはどう変わっていく？」", "第1章 じっくり解説③"),
    ("方程式で、項を等号の反対側へ移す（移項する）と符号が変わるのはなぜですか。$2x+3=11$ を例にして説明しなさい。",
     "等式は両辺に同じことをしても成り立つ。$2x+3=11$ の両辺から 3 をひくと $2x=11-3$。結果として左辺の $+3$ が右辺に $-3$ として移ったように見える。",
     "「天秤の両側から、おもりを 3 個ずつ取ったらどうなる？ 式で書くとどうなる？」", "第3章 じっくり解説②"),
    ("$-3^2$ と $(-3)^2$ の値をそれぞれ求めなさい。また、なぜ答えが違うのかを説明しなさい。",
     "$-3^2=-9$、$(-3)^2=9$。$-3^2$ は $3$ を 2 回かけてからマイナスをつける（$-(3\\times3)$）。$(-3)^2$ は $-3$ を 2 回かける（$(-3)\\times(-3)$）。かっこがあるかで、2 乗される数が違う。",
     "「$-3^2$ では、何を 2 回かけている？ $(-3)^2$ では？」", "第1章 累乗の注意"),
]

def m(s):
    s = s.replace("<", r"\lt ").replace(">", r"\gt ")
    return f"${s}$"

def fix(s):
    return re.sub(r"(?<![\d.])1\(", "(", s)

CONF = '<div class="conf">自信　◎ ・ ○ ・ △</div>'

def calc_tables(pick, custom, with_conf, numbering_start, blank="blank"):
    out, answers = [], []
    no = numbering_start - 1
    for ch in ["1", "2", "3", "4"]:
        qs = []
        for j, i in enumerate(pick[ch]):
            q, a = custom[(ch, j)] if i is None else D[ch]["items"][i]
            no += 1
            qs.append(f'<td><span class="qn">({no})</span> {m(fix(q))}<div class="{blank}"></div>{CONF if with_conf else ""}</td>')
            answers.append((no, ch, a))
        rows = "".join(f"<tr>{qs[k]}{qs[k+1] if k+1 < len(qs) else '<td></td>'}</tr>" for k in range(0, len(qs), 2))
        out.append(f'<h3>{NAMES[ch]}<small>{HOWTO[ch]}</small></h3><table class="qt">{rows}</table>')
    return "".join(out), answers

calc_q, calc_a = calc_tables(PICK, {}, True, 1)
retry_q, retry_a = calc_tables(RETRY, CUSTOM, False, 1, blank="blank2")
# 確認テストの答えが NOTES で想定している値と一致するか
expect = {1: "-20", 2: "-28", 3: "4", 4: "1", 5: "8", 6: "3 x + 27 y", 7: "6 x - 12 y", 8: "28 x - 6 y",
          9: "\\frac{11 - 5 x}{12}", 10: "\\frac{x - 14}{10}", 11: "x=3", 12: "x=4", 13: "x=-8", 14: "x=9", 15: "x=2"}
for n, ch, a in calc_a:
    if n in expect:
        assert a == expect[n], (n, a)

word_q = "".join(
    f'<div class="wq"><span class="qn">({i})</span> <b>【{w[0]}】</b>{w[1]}<div class="wblank"><span>式</span></div><div class="wans">答え</div>{CONF}</div>'
    for i, w in enumerate(WORD, 21))
exp_q = "".join(
    f'<div class="eq"><span class="qn">({i})</span> {e[0]}<div class="lines"></div></div>'
    for i, e in enumerate(EXPLAIN, 26))

# --- 大人用：答えとつまずきメモ ---
rows = []
for n, ch, a in calc_a:
    if n <= 15:
        note, where = NOTES[n]
        rows.append(f'<tr><td class="qn">({n})</td><td class="ansc">{m(a)}</td><td>{note}</td><td class="where">{where}</td></tr>')
    else:
        extra = (f'<td rowspan="5">{SIMUL_NOTE[0]}</td><td rowspan="5" class="where">{SIMUL_NOTE[1]}</td>' if n == 16 else "")
        rows.append(f'<tr><td class="qn">({n})</td><td class="ansc">{m(a)}</td>{extra}</tr>')
    if n in (5, 10, 15):
        rows.append(f'<tr class="sep"><td colspan="4"></td></tr>')
calc_ans = "".join(rows)

word_ans = "".join(
    f'<tr><td class="qn">({i})</td><td>{w[0]}</td><td>{w[3]}</td><td><b>{w[4]}</b></td><td class="where">{w[6]}</td></tr>'
    for i, w in enumerate(WORD, 21))
exp_ans = "".join(
    f'<div class="box sol"><b>({i})</b> {e[1]}<div class="look"><b>声かけの例：</b>{e[2]}<br><b>読み直す場所：</b>{e[3]}</div></div>'
    for i, e in enumerate(EXPLAIN, 26))

retry_ans = []
for ch in ["1", "2", "3", "4"]:
    cells = "".join(f'<td><span class="qn">({n})</span> {m(a)}</td>' for n, c, a in retry_a if c == ch)
    retry_ans.append(f'<tr><th>{NAMES[ch]}</th>{cells}</tr>')

html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>1か月 理解度チェック</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<script src="node_modules/katex/dist/katex.min.js"></script>
<script src="node_modules/katex/dist/contrib/auto-render.min.js"></script>
<style>
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:#222; font-size:11pt; line-height:1.7; margin:0; background:#fff; }}
h1 {{ font-size:18pt; margin:0; color:#2e8b57; }}
.head {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid #2e8b57; padding-bottom:2mm; margin-bottom:3mm; }}
.meta td {{ border:1px solid #999; padding:1mm 3mm; font-size:10pt; }} .meta td.w {{ width:48mm; }}
.note {{ font-size:10pt; background:#ecf8f1; border-radius:4px; padding:2mm 4mm; margin-bottom:3mm; }}
h2 {{ font-size:13.5pt; background:#2e8b57; color:#fff; padding:1mm 4mm; border-radius:4px; margin:5mm 0 2mm; }}
h2.p {{ page-break-before:always; margin-top:0; }}
h2.adult {{ background:#555; }}
h2 small {{ font-size:10pt; font-weight:normal; }}
h3 {{ font-size:11.5pt; color:#2e8b57; border-left:5px solid #2e8b57; padding-left:2mm; margin:3mm 0 1mm; page-break-after:avoid; }}
h3 small {{ font-weight:normal; color:#444; margin-left:3mm; font-size:10pt; }}
h3.a {{ color:#444; border-left-color:#555; }}
table {{ border-collapse:collapse; }}
table.qt {{ width:100%; }} table.qt td {{ width:50%; vertical-align:top; padding:1mm 2mm; border:1px solid #ccc; position:relative; }}
.blank {{ height:13mm; }} .blank2 {{ height:6mm; }}
.conf {{ text-align:right; font-size:8.5pt; color:#888; }}
.qn {{ font-weight:bold; color:#2e8b57; }}
.wq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.wblank {{ height:19mm; }} .wblank span {{ color:#888; font-size:9pt; }}
.wans {{ border-top:1px dashed #999; color:#888; font-size:9pt; padding-top:1mm; height:6mm; }}
.eq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.lines {{ height:42mm; background:repeating-linear-gradient(#fff 0 9.5mm,#bbb 9.5mm 10mm); margin-top:2mm; }}
table.at {{ width:100%; font-size:9.8pt; }} table.at td, table.at th {{ border:1px solid #999; padding:1mm 2mm; text-align:left; vertical-align:top; }}
table.at th {{ background:#eee; white-space:nowrap; }} table.at tr {{ page-break-inside:avoid; }}
table.at td.ansc {{ white-space:nowrap; }} table.at td.where {{ font-size:9pt; color:#2e5e8b; width:34mm; }}
table.at tr.sep td {{ border:none; height:1.5mm; padding:0; }}
.box {{ border-radius:5px; padding:2.5mm 4mm; margin:2.5mm 0; page-break-inside:avoid; }}
.sol {{ background:#f6f6f6; border-left:6px solid #2e8b57; }}
.look {{ background:#fff; border:1px solid #2e8b57; border-radius:4px; padding:1mm 3mm; margin-top:2mm; font-size:10pt; }}
.steps {{ background:#fff8e8; border:1.5px solid #e0a02a; border-radius:6px; padding:2mm 4mm; margin:2mm 0; }}
.steps ol {{ margin:0; padding-left:6mm; }}
table.mx {{ width:100%; font-size:10pt; margin:1mm 0 2mm; }} table.mx td, table.mx th {{ border:1px solid #999; padding:1.5mm 2mm; text-align:left; vertical-align:top; }}
table.mx th {{ background:#eee; text-align:center; }}
table.sheet {{ width:100%; font-size:10pt; }} table.sheet td, table.sheet th {{ border:1px solid #666; padding:1.5mm 2mm; }}
table.sheet th {{ background:#ecf8f1; }} table.sheet td.f {{ height:9mm; }}
.rule {{ font-size:10pt; }} .rule li {{ margin:0.8mm 0; }}
</style></head><body>

<!-- ===== 子ども用：問題 ===== -->
<div class="head"><div><div style="font-size:10pt;color:#666">中学数学 第1〜4章</div><h1>1か月 理解度チェック</h1></div>
<table class="meta"><tr><td>日付</td><td class="w"></td></tr><tr><td>名前</td><td class="w"></td></tr></table></div>
<div class="note"><b>点数はつけません。</b>どこがわかっていて、どこでつまずいているかを見つけるためのチェックです。<br>
・時間は気にしなくてOK（目安は50分）。本は見ずに、自分の力でやってみよう。<br>
・途中の式は消さずに残そう。<b>まちがい方がわかると、直し方もわかります。</b><br>
・わからない問題は「わからない」と書いてOK。<br>
・各問題の右下の「自信」に、<b>◎（自信あり）○（たぶん）△（自信なし）</b>のどれかに丸をつけよう。</div>

<h2>Ⅰ　計算問題</h2>
{calc_q}

<h2 class="p">Ⅱ　文章題<small>　わからないものを $x$ などの文字でおいて、方程式をつくって解こう。</small></h2>
{word_q}

<h2 class="p">Ⅲ　説明問題<small>　友だちに教えるつもりで、言葉や式で説明しよう。</small></h2>
{exp_q}

<!-- ===== 大人用 ===== -->
<h2 class="p adult">答え合わせ・つまずき診断（大人用）</h2>
<div class="steps"><b>進め方</b><ol>
<li>答えを見て、各問題に <b>○ か × だけ</b>をつける（点数は出さない）。</li>
<li>× の問題は、途中の式を見て、下の「よくあるまちがい」のどれに近いかを探す。</li>
<li>最後のページの「診断シート」に × の数を書き込み、次にやることを決める。</li>
<li>× の問題は、本書の「読み直す場所」を一緒に開いて解き直す。そのあと「解き直しプリント」（同じタイプの類題）で確かめる。</li></ol></div>

<h3 class="a">「自信」と「正しいか」の組み合わせで見る</h3>
<table class="mx"><tr><th></th><th>正しかった（○）</th><th>まちがえた（×）</th></tr>
<tr><th>自信 ◎</th><td><b>身についている。</b>この調子でOK。</td><td><b>思い込みのまちがい（一番大事）。</b>本人は正しいと思っているので、自分では気づけない。どこで考え違いをしたか、一緒に途中の式をたどる。</td></tr>
<tr><th>自信 ○・△</th><td><b>わかりかけ。</b>理解はできているので、ドリルで回数を重ねれば自信がつく。</td><td><b>まだわかっていない。</b>その章の前半（★〜🔁）から読み直す。あせらなくてOK。</td></tr></table>

<h3 class="a">Ⅰ　計算問題の答えと、よくあるまちがい</h3>
<table class="at"><tr><th style="width:9mm">番号</th><th>答え</th><th>よくあるまちがい（原因）</th><th>読み直す場所</th></tr>{calc_ans}</table>
<p style="font-size:9pt;color:#555">文字式は、同じ式になっていれば形が違っても正解（例：$\\frac{{11-5x}}{{12}}$ と $\\frac{{-5x+11}}{{12}}$）。連立方程式は $x$ と $y$ の両方が合っていれば ○。</p>

<h3 class="a">Ⅱ　文章題の答え</h3>
<table class="at"><tr><th style="width:9mm">番号</th><th style="width:18mm">型</th><th>式の例</th><th style="width:40mm">答え</th><th>読み直す場所</th></tr>{word_ans}</table>
<p style="font-size:9.5pt"><b>× のときは「どこで止まったか」を見る：</b></p>
<table class="mx"><tr><th style="width:42%">止まったところ</th><th>次にやること</th></tr>
<tr><td>① 何を $x$ とおけばいいか決められない</td><td>「聞かれているもの」を $x$ にする練習。問題文の最後の一文に線を引かせる。</td></tr>
<tr><td>② $x$ はおけたが、式（＝）が作れない</td><td>「同じものを2通りに表す」がコツ（第3章 文章題のコツ）。例：代金の合計、あめの数、2人の進んだ道のり。</td></tr>
<tr><td>③ 式は合っているが、答えがちがう</td><td>文章題ではなく<b>計算</b>のつまずき。Ⅰの同じ章の結果と合わせて見る。</td></tr>
<tr><td>④ 片方しか答えていない（人数だけ、など）</td><td>理解はOK。最後に「聞かれたものを全部答えたか」を見直すくせをつける。</td></tr></table>
<p style="font-size:9pt;color:#555">線分図や表など、算数の方法で正しく解けていても ○ でかまいません。</p>

<h3 class="a">Ⅲ　説明問題の見方</h3>
<p style="font-size:10pt">説明問題は ○× ではなく、次の3段階で様子を見ます。言葉がつたなくても、<b>理由を言おうとしていれば十分</b>です。</p>
<table class="mx"><tr><th style="width:24%">様子</th><th>次にやること</th></tr>
<tr><td>◎ 理由まで説明できた</td><td>しっかり理解している。ほめて次へ。</td></tr>
<tr><td>○ ルールや答えは言えたが、理由があいまい</td><td>下の「声かけの例」で問いかけて、口で説明してもらう。</td></tr>
<tr><td>△ 説明できなかった</td><td>「読み直す場所」を一緒に読み、そのあと同じ質問をもう一度する。</td></tr></table>
{exp_ans}

<h2 class="p adult">診断シート</h2>
<table class="sheet"><tr><th>分野</th><th>問題</th><th style="width:22mm">× の数</th><th style="width:30mm">「◎なのに×」の数</th><th>次にやること（メモ）</th></tr>
<tr><td>正負の数</td><td>(1)〜(5)</td><td class="f"></td><td></td><td></td></tr>
<tr><td>文字式の計算</td><td>(6)〜(10)</td><td class="f"></td><td></td><td></td></tr>
<tr><td>一次方程式</td><td>(11)〜(15)</td><td class="f"></td><td></td><td></td></tr>
<tr><td>連立方程式</td><td>(16)〜(20)</td><td class="f"></td><td></td><td></td></tr>
<tr><td>文章題</td><td>(21)〜(25)</td><td class="f"></td><td></td><td>止まったところ：① ② ③ ④</td></tr>
<tr><td>説明</td><td>(26)〜(28)</td><td colspan="2" class="f">◎　・　○　・　△</td><td></td></tr></table>
<div class="steps rule"><b>次にやることの決め方（計算の各分野）</b><ul>
<li><b>× が 0 個</b>：その分野はOK。</li>
<li><b>× が 1 個</b>：まちがえた問題を解き直し、「解き直しプリント」の同じ番号の類題をやる。</li>
<li><b>× が 2 個以上</b>：その章の前半（★〜🔁）を読み直してから、章末の計算ドリルをもう1周する。</li>
<li><b>「◎なのに×」がある</b>：思い込みのまちがい。どこで考え違いをしたかを、本人に言葉で説明してもらう。</li>
<li>4つの分野すべてで × が 1 個以下になったら、<b>第5章（比例・一次関数）へ進んでOK</b>。</li>
<li>文字式・方程式で × が多いときは、<b>原因が第1章（符号）にある</b>ことがよくあります。まず第1章の結果を見てください。</li></ul></div>

<h2 class="p">解き直しプリント（類題）<small>　Ⅰ と同じ番号が、同じタイプの問題です。× だった番号だけやればOK。計算はノートに書いてね。</small></h2>
{retry_q}
<h3 class="a" style="page-break-before:always">解き直しプリントの答え（大人用）</h3>
<table class="at">{''.join(retry_ans)}</table>

<script>renderMathInElement(document.body,{{delimiters:[{{left:"$",right:"$",display:false}}],throwOnError:false}});document.body.setAttribute('data-done','1');</script>
</body></html>"""
open("check.html", "w", encoding="utf-8").write(html)
print("ok")
