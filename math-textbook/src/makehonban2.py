"""本番テスト（範囲：第1〜5章・採点あり100点）を honban2.html に出力する。
第1〜4章の計算は前回の本番（未配布）から各4問、第5章は本のドリルにない新しい問題。答えはすべて sympy で検算。"""
import json, re
import sympy as sp
from honban_data import D as POOLD, WORD as WORD4, EXPLAIN as EXPL4, _seen

x, y = sp.symbols("x y")
NAMES = {"1": "正負の数", "2": "文字式の計算", "3": "一次方程式", "4": "連立方程式", "5": "比例・反比例・一次関数"}
HOWTO = {"1": "次の計算をしなさい。", "2": "次の式を計算しなさい。", "3": "次の方程式を解きなさい。", "4": "次の連立方程式を解きなさい。", "5": "次の問いに答えなさい。"}
PICK = {"1": [19, 2, 36, 28], "2": [5, 31, 14, 19], "3": [0, 1, 15, 22], "4": [2, 7, 15, 13]}

def m(s):
    return "$" + s.replace("<", r"\lt ").replace(">", r"\gt ") + "$"

def fix(s):
    return re.sub(r"(?<![\d.])1\(", "(", s)

CALC = []  # (章, 問題HTML, 答えHTML)
for ch in "1234":
    for k in PICK[ch]:
        q, a = POOLD[ch]["items"][k]
        assert q not in _seen
        CALC.append((ch, m(fix(q)), m(a)))

# --- 第5章：本のドリルにない新しい問題 ---
P5 = json.load(open("pool5.json", encoding="utf-8"))
BOOK5 = set(q for q, a in json.load(open("drills.json", encoding="utf-8"))["5"]["items"])
# 比例
a1 = sp.Rational(12, -3); assert a1 == -4 and a1 * 5 == -20
CALC.append(("5", "$y$ は $x$ に比例し、$x=-3$ のとき $y=12$ です。$y$ を $x$ の式で表しなさい。また、$x=5$ のときの $y$ の値を求めなさい。",
             "$y=-4x$、$y=-20$（両方できて3点）"))
# 反比例
k5 = 4 * (-6); assert k5 == -24 and sp.Rational(k5, -3) == 8
CALC.append(("5", "$y$ は $x$ に反比例し、$x=4$ のとき $y=-6$ です。$x=-3$ のときの $y$ の値を求めなさい。", "$y=8$"))
# 2点を通る直線（pool5 の 44 番）
q, a = P5[44]; assert q not in BOOK5 and a == "y=- 3 x - 1"
assert -3 * (-2) - 1 == 5 and -3 * 2 - 1 == -7
CALC.append(("5", q.replace("を通る直線", "を通る直線の式を求めなさい。"), "$y=-3x-1$"))
# 交点（pool5 の 18 番）
q, a = P5[18]; assert q not in BOOK5
assert sp.solve([sp.Eq(y, -x - 2), sp.Eq(y, 2 * x + 7)], [x, y]) == {x: -3, y: 1}
CALC.append(("5", q.replace("の交点", "の交点の座標を求めなさい。"), "$(-3,\\ 1)$"))
assert len(CALC) == 20

# --- 文章題：第3・4章から3題（前回の本番から）、第5章から2題（新規） ---
WORD = [w[:6] for w in WORD4 if w[0] in ("代金", "速さ", "つるかめ算")]
WORD += [
    ("反比例", "ある仕事を 6 人ですると 8 日かかります。同じ仕事を 4 人ですると何日かかりますか。ただし、1人が1日にする仕事の量はみな同じとします。",
     sp.Eq(4 * x, 6 * 8), "日数を $x$ 日とすると　$4x=6\\times8$（または $y=\\frac{48}{x}$ に $x=4$ を代入）", "12 日", {x: 12}),
    ("一次関数の利用", "電話の料金プランが2つあります。Aプランは基本料金 800 円に、通話1分ごとに 20 円かかります。Bプランは基本料金 2000 円に、通話1分ごとに 5 円かかります。通話時間が何分より長いと、Bプランの方が安くなりますか。",
     sp.Eq(20 * x + 800, 5 * x + 2000), "通話時間を $x$ 分とすると　A：$y=20x+800$、B：$y=5x+2000$。等しくなるのは $20x+800=5x+2000$", "80 分より長いとき", {x: 80}),
]
for w in WORD:
    eq, sol = w[2], w[5]
    got = sp.solve(eq, list(sol)) if isinstance(eq, list) else {x: sp.solve(eq, x)[0]}
    assert got == sol, (w[0], got, sol)
assert 20 * 100 + 800 > 5 * 100 + 2000 and 20 * 60 + 800 < 5 * 60 + 2000  # 80分をこえると B が安い
assert [w[0] for w in WORD] == ["代金", "速さ", "つるかめ算", "反比例", "一次関数の利用"]

# --- 説明問題：第1章・第4章（前回の本番から）、第5章（新規） ---
EXPLAIN = [
    (EXPL4[0][0], EXPL4[0][1],
     ["「わり算はかけ算の逆」として、$(-4)\\times\\square=-12$ の形で考えている：3点",
      "$\\square=3$（プラス）になることにつなげて説明している：2点",
      "「マイナス÷マイナスはプラスだから」とルールをくり返すだけのもの：0点"]),
    (EXPL4[2][0], EXPL4[2][1],
     ["1本だけでは条件に合う組が無数にあることを示している（具体例を2組以上、または「グラフの直線上の点すべて」）：3点",
      "2本あると、両方を満たす組（2直線の交点）が1つに決まることを説明している：2点"]),
    ("一次関数 $y=2x+3$ の「$2$」と「$3$」は、それぞれグラフのどんなことを表していますか。説明しなさい。",
     "「$3$」は<b>切片</b>：$x=0$ のとき $y=3$ なので、グラフが $y$ 軸と交わる点 $(0,3)$ を表す。"
     "「$2$」は<b>傾き</b>：$x$ が 1 増えると $y$ が 2 増える。グラフでは、右へ 1 進むと上へ 2 上がる右上がりの直線になる。",
     ["「$3$」が $y$ 軸との交点（$x=0$ のときの $y$ の値）であることを説明している：2点",
      "「$2$」が「$x$ が 1 増えると $y$ が 2 増える」（右へ1・上へ2）ことを説明している：3点",
      "「切片」「傾き」という言葉だけで、意味の説明がないもの：それぞれ1点まで"]),
]
assert "(-12)" in EXPLAIN[0][0] and "x+y=5" in EXPLAIN[1][0]
assert all(2 * xx + 3 - (2 * (xx - 1) + 3) == 2 for xx in range(-3, 4))

# ---------------- HTML ----------------
qcells, no = {}, 0
for ch, q, a in CALC:
    no += 1
    qcells.setdefault(ch, []).append(f'<td><span class="qn">({no})</span> {q}<div class="blank"></div></td>')
calc_q = ""
for ch in "12345":
    cs = qcells[ch]
    if ch == "5":  # 文章が長いので1列
        rows = "".join(f"<tr>{c.replace('<td>', '<td colspan=2>')}</tr>" for c in cs)
    else:
        rows = "".join(f"<tr>{cs[i]}{cs[i+1]}</tr>" for i in range(0, 4, 2))
    calc_q += f'<h3>{NAMES[ch]}（各3点・計12点）<small>{HOWTO[ch]}</small></h3><table class="qt">{rows}</table>'

word_q = "".join(
    f'<div class="wq"><span class="qn">({i})</span> <b>【{w[0]}】</b>{w[1]}<div class="wblank"><span>式</span></div><div class="wans">答え</div></div>'
    for i, w in enumerate(WORD, 21))
exp_q = "".join(f'<div class="eq"><span class="qn">({i})</span> {e[0]}<div class="lines"></div></div>' for i, e in enumerate(EXPLAIN, 26))

ans_calc = ""
no = 0
for ch in "12345":
    cells = ""
    for c, q, a in CALC:
        if c == ch:
            no += 1
    nums = [i for i, (c, _, _) in enumerate(CALC, 1) if c == ch]
    cells = "".join(f'<td><span class="qn">({i})</span> {CALC[i-1][2]}</td>' for i in nums)
    ans_calc += f"<tr><th>{NAMES[ch]}</th>{cells}</tr>"
ans_word = "".join(f'<tr><td class="qn">({i})</td><td>{w[0]}</td><td>{w[3]}</td><td><b>{w[4]}</b></td></tr>' for i, w in enumerate(WORD, 21))
ans_exp = "".join(
    f'<div class="box sol"><b>({i})</b> {e[1]}<div class="rub"><b>採点基準（5点）</b><ul>' + "".join(f"<li>{r}</li>" for r in e[2]) + "</ul></div></div>"
    for i, e in enumerate(EXPLAIN, 26))

html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>1か月テスト 本番（第1〜5章）</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<script src="node_modules/katex/dist/katex.min.js"></script>
<script src="node_modules/katex/dist/contrib/auto-render.min.js"></script>
<style>
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:#222; font-size:11pt; line-height:1.7; margin:0; background:#fff; }}
h1 {{ font-size:18pt; margin:0; color:#1f5fa8; }}
.head {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid #1f5fa8; padding-bottom:2mm; margin-bottom:3mm; }}
.meta td {{ border:1px solid #999; padding:1mm 3mm; font-size:10pt; }} .meta td.w {{ width:42mm; }}
.note {{ font-size:9.5pt; background:#e8f0fb; border-radius:4px; padding:2mm 4mm; margin-bottom:3mm; }}
h2 {{ font-size:13.5pt; background:#1f5fa8; color:#fff; padding:1mm 4mm; border-radius:4px; margin:5mm 0 2mm; }}
h2.p {{ page-break-before:always; margin-top:0; }}
h2 small {{ font-size:10pt; font-weight:normal; }}
h3 {{ font-size:11.5pt; color:#1f5fa8; border-left:5px solid #1f5fa8; padding-left:2mm; margin:3mm 0 1mm; page-break-after:avoid; }}
h3 small {{ font-weight:normal; color:#444; margin-left:3mm; font-size:10pt; }}
table {{ border-collapse:collapse; }}
table.qt {{ width:100%; }} table.qt td {{ width:50%; vertical-align:top; padding:1mm 2mm; border:1px solid #ccc; }}
table.qt tr {{ page-break-inside:avoid; }}
.blank {{ height:13mm; }}
.qn {{ font-weight:bold; color:#1f5fa8; }}
.wq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.wblank {{ height:16mm; }} .wblank span {{ color:#888; font-size:9pt; }}
.wans {{ border-top:1px dashed #999; color:#888; font-size:9pt; padding-top:1mm; height:8mm; }}
.eq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.lines {{ height:42mm; background:repeating-linear-gradient(#fff 0 9.5mm,#bbb 9.5mm 10mm); margin-top:2mm; }}
table.at {{ width:100%; font-size:10pt; }} table.at td, table.at th {{ border:1px solid #999; padding:1mm 2mm; text-align:left; vertical-align:top; }}
table.at th {{ background:#e8f0fb; white-space:nowrap; }}
.box {{ border-radius:5px; padding:2.5mm 4mm; margin:2.5mm 0; page-break-inside:avoid; }}
.sol {{ background:#ecf8f1; border-left:6px solid #2e8b57; }}
.rub {{ background:#fff; border:1px solid #2e8b57; border-radius:4px; padding:1mm 3mm; margin-top:2mm; font-size:10pt; }}
.rub ul {{ margin:0; padding-left:6mm; }}
.score {{ width:100%; font-size:9pt; }} .score td, .score th {{ border:1px solid #666; padding:1.5mm 1mm; text-align:center; }}
.score th {{ background:#e8f0fb; }}
.pass {{ background:#fff3ea; border:2px solid #e0702a; border-radius:6px; padding:2mm 4mm; margin:3mm 0; }}
</style></head><body>

<div class="head"><div><div style="font-size:10pt;color:#666">中学数学 第1〜5章</div><h1>1か月テスト（本番）</h1></div>
<table class="meta"><tr><td>日付</td><td class="w"></td></tr><tr><td>名前</td><td class="w"></td></tr><tr><td>点数</td><td class="w" style="text-align:right">／100点</td></tr></table></div>
<div class="note">制限時間 <b>50分</b>。計算の途中の式も消さずに残しておこう。わからない問題は飛ばして、できる問題から解こう。<br>
<b>合格ライン：計算問題（1〜20）で 48点以上（8割）</b></div>

<h2>Ⅰ　計算問題（60点）</h2>
{calc_q}

<h2 class="p">Ⅱ　文章題（25点）<small>　各5点（式 2点・答え 3点）。わからないものを $x$ などの文字でおいて、方程式や式をつくって解きなさい。<b>「それぞれ」と聞かれたら、全部答えること。</b></small></h2>
{word_q}

<h2 class="p">Ⅲ　説明問題（15点）<small>　各5点。友だちに教えるつもりで、言葉や式で説明しなさい。</small></h2>
{exp_q}

<h2 class="p">解答と採点基準（先生・保護者用）</h2>
<h3>得点集計</h3>
<table class="score"><tr><th>区分</th><th>正負の数</th><th>文字式</th><th>一次方程式</th><th>連立方程式</th><th>比例・一次関数</th><th>計算 小計</th><th>文章題</th><th>説明</th><th>合計</th></tr>
<tr><td>配点</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td><b>60</b></td><td>25</td><td>15</td><td><b>100</b></td></tr>
<tr><td>得点</td><td style="height:9mm"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div class="pass"><b>合格判定：計算 小計が 48点以上 → 合格</b>（各問 3点、部分点なし）。<br>
不合格の場合は、<b>12点中 6点以下だった章</b>（＝4問中2問以上まちがえた章）を本書で読み直し、その章の計算ドリルをもう一周してから再テストしましょう。</div>

<h3>Ⅰ　計算問題（各3点）</h3>
<table class="at">{ans_calc}</table>
<p style="font-size:9.5pt;color:#555">連立方程式・交点は $x$ と $y$ の両方が正しくて 3点。(17) は式と値の両方が正しくて 3点。文字式は同じ式になっていれば形が違っても正解（例：$\\frac{{19-11x}}{{12}}$ と $\\frac{{-11x+19}}{{12}}$）。直線の式は $y=-3x-1$ と同じ式なら形が違っても正解。</p>

<h3>Ⅱ　文章題（式2点・答え3点）</h3>
<table class="at"><tr><th style="width:12mm">番号</th><th style="width:26mm">型</th><th>式の例</th><th style="width:44mm">答え</th></tr>{ans_word}</table>
<p style="font-size:9.5pt;color:#555">式は、正しい式が立っていれば文字のおき方が違っても2点。答えは問われているものをすべて答えて3点（片方のみ：1点）。(25) は「80分」とだけ書いた場合は2点。単位の書き忘れは減点しない。算数の方法（線分図・表など）で正しく解けていても満点とする。</p>

<h3>Ⅲ　説明問題（各5点）</h3>
{ans_exp}
<script>renderMathInElement(document.body,{{delimiters:[{{left:"$",right:"$",display:false}}],throwOnError:false}});document.body.setAttribute('data-done','1');</script>
</body></html>"""
open("honban2.html", "w", encoding="utf-8").write(html)
print("ok")
