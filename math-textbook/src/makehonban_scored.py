"""本番テスト（採点あり・100点）を honban_scored.html に出力する。問題データは honban_data.py（新しい問題）。"""
from honban_data import *

WORD = [w[:6] for w in WORD]   # 確認テストと同じ形（読み直す場所の列は使わない）
RUBRIC = [
    ["「わり算はかけ算の逆」として、$(-4)\\times\\square=-12$ の形で考えている：3点",
     "$\\square=3$（プラス）になることにつなげて説明している：2点",
     "「マイナス÷マイナスはプラスだから」とルールをくり返すだけのもの：0点"],
    ["$-(a-b)=(-1)\\times(a-b)$ と見て分配法則を使っている（または「かっこの中の符号がすべて変わる」理由を述べている）：3点",
     "数を入れて $-(5-2)=-3=-5+2$ のように等しいことを確かめている：2点",
     "数で確かめているだけで、理由の説明がないもの：2点まで"],
    ["1本だけでは条件に合う組が無数にあることを示している（具体例を2組以上、または「グラフの直線上の点すべて」）：3点",
     "2本あると、両方を満たす組（2直線の交点）が1つに決まることを説明している：2点"],
]
EXPLAIN = [(q, model, rub) for (q, model, _talk, _where), rub in zip(EXPLAIN, RUBRIC)]

def m(s):
    s = s.replace("<", r"\lt ").replace(">", r"\gt ")
    return f"${s}$"

def fix(s):
    # 1(…) の 1 を消すなど表記を整える
    return re.sub(r"(?<![\d.])1\(", "(", s)

calc_q, calc_a = [], []
no = 0
for ch in ["1", "2", "3", "4"]:
    items = [D[ch]["items"][i] for i in PICK[ch]]
    qs = []
    for q, a in items:
        no += 1
        qs.append(f'<td><span class="qn">({no})</span> {m(fix(q))}<div class="blank"></div></td>')
        calc_a.append((no, ch, q, a))
    rows = "".join(f"<tr>{qs[i]}{qs[i+1] if i+1 < len(qs) else '<td></td>'}</tr>" for i in range(0, len(qs), 2))
    calc_q.append(f'<h3>{NAMES[ch]}（各3点・計15点）<small>{HOWTO[ch]}</small></h3><table class="qt">{rows}</table>')

word_q = "".join(
    f'<div class="wq"><span class="qn">({i})</span> <b>【{t}】</b>{body}<div class="wblank"><span>式</span></div><div class="wans">答え</div></div>'
    for i, (t, body, *_ ) in enumerate(WORD, 21))
exp_q = "".join(
    f'<div class="eq"><span class="qn">({i})</span> {q}<div class="lines"></div></div>'
    for i, (q, *_ ) in enumerate(EXPLAIN, 26))

ans_calc = []
for ch in ["1", "2", "3", "4"]:
    cells = "".join(f'<td><span class="qn">({n})</span> {m(a)}</td>' for n, c, q, a in calc_a if c == ch)
    ans_calc.append(f'<tr><th>{NAMES[ch]}</th>{cells}</tr>')
ans_word = "".join(
    f'<tr><td class="qn">({i})</td><td>{t}</td><td>{f}</td><td><b>{a}</b></td></tr>'
    for i, (t, _, _, f, a, _) in enumerate(WORD, 21))
ans_exp = "".join(
    f'<div class="box sol"><b>({i})</b> {model}<div class="rub"><b>採点基準（5点）</b><ul>' + "".join(f"<li>{r}</li>" for r in rub) + "</ul></div></div>"
    for i, (_, model, rub) in enumerate(EXPLAIN, 26))

html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>1か月テスト 本番</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<script src="node_modules/katex/dist/katex.min.js"></script>
<script src="node_modules/katex/dist/contrib/auto-render.min.js"></script>
<style>
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:#222; font-size:11pt; line-height:1.7; margin:0; background:#fff; }}
h1 {{ font-size:18pt; margin:0; color:#1f5fa8; }}
.head {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid #1f5fa8; padding-bottom:2mm; margin-bottom:3mm; }}
.meta td {{ border:1px solid #999; padding:1mm 3mm; font-size:10pt; }}
.meta td.w {{ width:42mm; }} .meta td.s {{ width:22mm; }}
.note {{ font-size:9.5pt; background:#e8f0fb; border-radius:4px; padding:2mm 4mm; margin-bottom:3mm; }}
h2 {{ font-size:13.5pt; background:#1f5fa8; color:#fff; padding:1mm 4mm; border-radius:4px; margin:5mm 0 2mm; }}
h2.p {{ page-break-before:always; margin-top:0; }}
h3 {{ font-size:11.5pt; color:#1f5fa8; border-left:5px solid #1f5fa8; padding-left:2mm; margin:3mm 0 1mm; }}
h3 small {{ font-weight:normal; color:#444; margin-left:3mm; font-size:10pt; }}
table {{ border-collapse:collapse; }}
table.qt {{ width:100%; }} table.qt td {{ width:50%; vertical-align:top; padding:1mm 2mm; border:1px solid #ccc; }}
.blank {{ height:15mm; }}
.qn {{ font-weight:bold; color:#1f5fa8; }}
.wq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.wblank {{ height:20mm; position:relative; }} .wblank span {{ color:#888; font-size:9pt; }}
.wans {{ border-top:1px dashed #999; color:#888; font-size:9pt; padding-top:1mm; height:8mm; }}
.eq {{ border:1px solid #ccc; padding:2mm 3mm; margin:2mm 0; page-break-inside:avoid; }}
.lines {{ height:42mm; background:repeating-linear-gradient(#fff 0 9.5mm,#bbb 9.5mm 10mm); margin-top:2mm; }}
table.at {{ width:100%; font-size:10.5pt; }} table.at td, table.at th {{ border:1px solid #999; padding:1mm 2mm; text-align:left; }}
table.at th {{ background:#e8f0fb; width:22mm; }}
.box {{ border-radius:5px; padding:2.5mm 4mm; margin:2.5mm 0; page-break-inside:avoid; }}
.sol {{ background:#ecf8f1; border-left:6px solid #2e8b57; }}
.rub {{ background:#fff; border:1px solid #2e8b57; border-radius:4px; padding:1mm 3mm; margin-top:2mm; font-size:10pt; }}
.rub ul {{ margin:0; padding-left:6mm; }}
.score {{ width:100%; font-size:9.5pt; }} .score td, .score th {{ border:1px solid #666; padding:1.5mm 1mm; white-space:nowrap; text-align:center; }}
.score th {{ background:#e8f0fb; }}
.pass {{ background:#fff3ea; border:2px solid #e0702a; border-radius:6px; padding:2mm 4mm; margin:3mm 0; }}
</style></head><body>

<div class="head"><div><div style="font-size:10pt;color:#666">中学数学 第1〜4章</div><h1>1か月テスト（本番）</h1></div>
<table class="meta"><tr><td>日付</td><td class="w"></td></tr><tr><td>名前</td><td class="w"></td></tr><tr><td>点数</td><td class="w" style="text-align:right">／100点</td></tr></table></div>
<div class="note">制限時間 <b>50分</b>。計算の途中の式も消さずに残しておこう。わからない問題は飛ばして、できる問題から解こう。<br>
<b>合格ライン：計算問題（1〜20）で 48点以上（8割）</b></div>

<h2>Ⅰ　計算問題（60点）</h2>
{''.join(calc_q)}

<h2 class="p">Ⅱ　文章題（25点）<small style="font-size:10pt;font-weight:normal">　各5点（式 2点・答え 3点）。わからないものを $x$ などの文字でおいて、方程式をつくって解きなさい。</small></h2>
{word_q}

<h2 class="p">Ⅲ　説明問題（15点）<small style="font-size:10pt;font-weight:normal">　各5点。友だちに教えるつもりで、言葉や式で説明しなさい。</small></h2>
{exp_q}

<h2 class="p">解答と採点基準（先生・保護者用）</h2>
<h3>得点集計</h3>
<table class="score"><tr><th>区分</th><th>正負の数</th><th>文字式</th><th>一次方程式</th><th>連立方程式</th><th>計算 小計</th><th>文章題</th><th>説明</th><th>合計</th></tr>
<tr><td>配点</td><td>15</td><td>15</td><td>15</td><td>15</td><td><b>60</b></td><td>25</td><td>15</td><td><b>100</b></td></tr>
<tr><td>得点</td><td style="height:9mm"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>
<div class="pass"><b>合格判定：計算 小計が 48点以上 → 合格</b>（各問 3点、部分点なし）。<br>
不合格の場合は、<b>15点中 9点以下だった章</b>（＝5問中2問以上まちがえた章）を本書で読み直し、その章の計算ドリルをもう一周してから再テストしましょう。</div>

<h3>Ⅰ　計算問題（各3点）</h3>
<table class="at">{''.join(ans_calc)}</table>
<p style="font-size:9.5pt;color:#555">連立方程式は $x$ と $y$ の両方が正しくて 3点。文字式は同じ式になっていれば形が違っても正解（例：$\\frac{{19-11x}}{{12}}$ と $\\frac{{-11x+19}}{{12}}$）。</p>

<h3>Ⅱ　文章題（式2点・答え3点）</h3>
<table class="at"><tr><th style="width:12mm">番号</th><th style="width:24mm">型</th><th>式の例</th><th style="width:48mm">答え</th></tr>{ans_word}</table>
<p style="font-size:9.5pt;color:#555">式は、正しい方程式が立っていれば文字のおき方が違っても2点。答えは問われているものをすべて答えて3点（片方のみ：1点）。単位の書き忘れは減点しない。算数の方法（線分図・表など）で正しく解けていても満点とする。</p>

<h3>Ⅲ　説明問題（各5点）</h3>
{ans_exp}
<script>renderMathInElement(document.body,{{delimiters:[{{left:"$",right:"$",display:false}}],throwOnError:false}});document.body.setAttribute('data-done','1');</script>
</body></html>"""
open("honban_scored.html", "w", encoding="utf-8").write(html)
print("ok")
