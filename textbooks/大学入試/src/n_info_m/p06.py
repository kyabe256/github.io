"""問題集 第6章 アルゴリズムとプログラミングの基本。問題はすべて書き下ろし。
verify() は計算をすべて Python で検算し、プログラムは表示した文字列をそのまま Python に直訳して実行して答えと照合する。"""
import re, html
from fractions import Fraction as F

# ---------------- 書式の道具 ----------------


def B(s):
    return f'<div class="bun">{s}</div>'


def K(s):
    """空欄の枠"""
    return ('<span style="display:inline-block;border:1px solid #333;min-width:1.3em;padding:0 2px;'
            f'text-align:center;line-height:1.25;font-weight:bold;background:#fff">{s}</span>')


def CODE(src, start=1, num=True):
    """共通テスト用プログラム表記を <pre class="code"> にする。< > & は実体参照、【ア】は空欄の枠"""
    rows = []
    for i, ln in enumerate(src.strip("\n").split("\n"), start):
        e = html.escape(ln, quote=False)
        e = re.sub(r"【(.+?)】", lambda m: K(m.group(1)), e)
        rows.append(f"({i:02d}) {e}" if num else e)
    return '<pre class="code">' + "\n".join(rows) + "</pre>"


def TB(head, rows, cls=""):
    c = f' class="{cls}"' if cls else ""
    h = ("<tr>" + "".join(f"<th>{x}</th>" for x in head) + "</tr>") if head else ""
    r = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table{c}>{h}{r}</table>"


def run(src, **fill):
    """表示したプログラムの文字列をそのまま Python に直訳して実行する（検算用）。
    戻り値は (表示された行のリスト, 実行後の変数)。fill={'ア': '...'} で空欄を埋める。"""
    for k, v in fill.items():
        src = src.replace(f"【{k}】", v)
    assert "【" not in src, "空欄が残っている"
    py = []
    for ln in src.strip("\n").split("\n"):
        m = re.match(r"^((?:[｜⎿] )*)(.*)$", ln)
        d = len(m.group(1)) // 2
        s = m.group(2).strip()
        s = s.replace("÷", "//").replace("要素数(", "len(").replace("整数(", "int(")
        if (g := re.match(r"^もし (.+) ならば:$", s)):
            s = f"if {g.group(1)}:"
        elif (g := re.match(r"^そうでなくもし (.+) ならば:$", s)):
            s = f"elif {g.group(1)}:"
        elif s == "そうでなければ:":
            s = "else:"
        elif (g := re.match(r"^(\w+) を (.+?) から (.+?) まで (.+?) ずつ増やしながら繰り返す:$", s)):
            s = f"for {g.group(1)} in range({g.group(2)}, ({g.group(3)}) + 1, {g.group(4)}):"
        elif (g := re.match(r"^(\w+) を (.+?) から (.+?) まで (.+?) ずつ減らしながら繰り返す:$", s)):
            s = f"for {g.group(1)} in range({g.group(2)}, ({g.group(3)}) - 1, -({g.group(4)})):"
        elif (g := re.match(r"^(.+) の間繰り返す:$", s)):
            s = f"while {g.group(1)}:"
        elif (g := re.match(r"^表示する\((.*)\)$", s)):
            s = f"_out.append(_cat({g.group(1)}))"
        else:   # 代入文（「x = 1, y = 2」の形も分ける）
            assert re.match(r"^[A-Za-z_]\w*(\[.+?\])? = ", s), ("解釈できない行", s)
            s = "; ".join(re.split(r",\s*(?=[A-Za-z_]\w*(?:\[[^\]]*\])? = )", s))
        assert not re.search(r"[^\x00-\x7f]", re.sub(r'"[^"]*"', '""', s)), ("訳し残し", s)
        py.append("    " * d + s)
    env = {"_out": [], "_cat": lambda *a: "".join(str(x) for x in a)}
    exec("\n".join(py), env)
    return env["_out"], env


NOTE = "（プログラムは共通テスト用プログラム表記で書かれている。｜ と ⎿ は繰り返しや条件分岐の範囲を表す。÷ は商の整数部分、% は余りを求める演算子で、配列の添字は 0 から始まる。）"

# ---------------- 図（座標は Python で計算） ----------------

ST = 'fill="#fff" stroke="#000" stroke-width="1.3"'


def sym_terminal(cx, y, w, h, label):
    return (f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" {ST}/>'
            f'<text x="{cx}" y="{y + h / 2 + 4}" text-anchor="middle">{label}</text>')


def sym_process(cx, y, w, h, label):
    return (f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" {ST}/>'
            f'<text x="{cx}" y="{y + h / 2 + 4}" text-anchor="middle">{label}</text>')


def sym_decision(cx, cy, hw, hh, label):
    return (f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" {ST}/>'
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle">{label}</text>')


def sym_data(cx, y, w, h, label, k=10):
    x0 = cx - w / 2
    return (f'<polygon points="{x0 + k},{y} {x0 + w},{y} {x0 + w - k},{y + h} {x0},{y + h}" {ST}/>'
            f'<text x="{cx}" y="{y + h / 2 + 4}" text-anchor="middle">{label}</text>')


def sym_loop(cx, y, w, h, label, c=8):
    x0 = cx - w / 2
    return (f'<polygon points="{x0 + c},{y} {x0 + w - c},{y} {x0 + w},{y + c} {x0 + w},{y + h} {x0},{y + h} {x0},{y + c}" {ST}/>'
            f'<text x="{cx}" y="{y + h / 2 + 5}" text-anchor="middle">{label}</text>')


def fig_symbols():
    W, H = 470, 70
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="11">']
    xs = [47 + 94 * k for k in range(5)]
    o.append(sym_terminal(xs[0], 8, 74, 28, ""))
    o.append(sym_process(xs[1], 8, 74, 28, ""))
    o.append(sym_decision(xs[2], 22, 38, 16, ""))
    o.append(sym_loop(xs[3], 8, 74, 28, ""))
    o.append(sym_data(xs[4], 8, 74, 28, ""))
    for k, nm in enumerate("アイウエオ"):
        o.append(f'<text x="{xs[k]}" y="60" text-anchor="middle" font-size="12">{nm}</text>')
    o.append("</svg>")
    return "".join(o)


def fig_flow():
    W, H, cx, rx = 300, 300, 110, 232
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="11">',
         '<defs><marker id="ahIM1f" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>']
    A = 'fill="none" stroke="#000" marker-end="url(#ahIM1f)"'
    dy, dh = 132, 24                                  # 判断記号の中心と半分の高さ
    o.append(f'<line x1="{cx}" y1="34" x2="{cx}" y2="52" {A}/>')
    o.append(f'<line x1="{cx}" y1="80" x2="{cx}" y2="{dy - dh}" {A}/>')
    o.append(f'<line x1="{cx}" y1="{dy + dh}" x2="{cx}" y2="180" {A}/>')
    o.append(f'<line x1="{cx}" y1="208" x2="{cx}" y2="226" {A}/>')
    o.append(f'<polyline points="{cx},254 {cx},270 30,270 30,94 {cx},94" {A}/>')       # 繰り返しの戻り
    o.append(f'<polyline points="{cx + 58},{dy} {rx},{dy} {rx},180" {A}/>')
    o.append(f'<line x1="{rx}" y1="208" x2="{rx}" y2="226" {A}/>')
    o.append(sym_terminal(cx, 8, 80, 26, "開始"))
    o.append(sym_process(cx, 52, 116, 28, "x = 1, s = 0"))
    o.append(sym_decision(cx, dy, 58, dh, "s &lt; 20"))
    o.append(sym_process(cx, 180, 116, 28, "s = s + x"))
    o.append(sym_process(cx, 226, 116, 28, "x = x + 2"))
    o.append(sym_data(rx, 180, 112, 28, "x と s を表示"))
    o.append(sym_terminal(rx, 226, 80, 26, "終了"))
    o.append(f'<text x="{cx + 6}" y="{dy + dh + 13}">Yes</text><text x="{cx + 64}" y="{dy - 6}">No</text>')
    o.append("</svg>")
    return "".join(o)


FIG_SYM = fig_symbols()
FIG_FLOW = fig_flow()

# ---------------- プログラム ----------------

P_SWAP = """
x = 3
y = 5
x = x + y
y = x - y
x = x - y
表示する(x, " ", y)
"""
P_SWAP2 = """
tmp = x
x = 【ア】
y = 【イ】
"""

P_BUNKI = """
もし tokuten >= 80 ならば:
｜ 表示する("A")
そうでなくもし tokuten >= 60 ならば:
｜ 表示する("B")
そうでなければ:
⎿ 表示する("C")
"""
P_BUNKI2 = """
もし tokuten >= 60 ならば:
｜ 表示する("B")
そうでなくもし tokuten >= 80 ならば:
｜ 表示する("A")
そうでなければ:
⎿ 表示する("C")
"""

P_LOOP1 = """
goukei = 0
i を 1 から 10 まで 3 ずつ増やしながら繰り返す:
⎿ goukei = goukei + i
表示する(goukei)
"""
P_LOOP2 = """
n = 100, kaisu = 0
n > 1 の間繰り返す:
｜ n = n ÷ 2
⎿ kaisu = kaisu + 1
表示する(kaisu)
"""

P_MAX = """
Data = [12, 45, 7, 45, 30]
saidai = Data[0], ichi = 0
i を 1 から 要素数(Data) - 1 まで 1 ずつ増やしながら繰り返す:
｜ もし Data[i] > saidai ならば:
｜ ｜ saidai = Data[i]
⎿ ⎿ ichi = i
表示する(saidai, " ", ichi)
"""

P_FLOW = """
x = 1, s = 0
s < 20 の間繰り返す:
｜ s = s + x
⎿ x = x + 2
表示する(x, " ", s)
"""

P_NEST = """
kosu = 0
i を 1 から 4 まで 1 ずつ増やしながら繰り返す:
｜ j を i から 4 まで 1 ずつ増やしながら繰り返す:
｜ ｜ もし (i + j) % 2 == 0 ならば:
⎿ ⎿ ⎿ kosu = kosu + 1
表示する(kosu)
"""

P_REV = """
A = [3, 8, 1, 6, 4]
n = 要素数(A)
i を 0 から n ÷ 2 - 1 まで 1 ずつ増やしながら繰り返す:
｜ tmp = A[i]
｜ A[i] = A[n - 1 - i]
⎿ A[n - 1 - i] = tmp
"""

P_OTSURI = """
Kouka = [500, 100, 50, 10]
Zaiko = [3, 1, 2, 20]
otsuri = 780
i を 0 から 3 まで 1 ずつ増やしながら繰り返す:
｜ maisu = 【ア】
｜ もし maisu > Zaiko[i] ならば:
｜ ⎿ maisu = 【イ】
｜ otsuri = otsuri - Kouka[i] * maisu
｜ Zaiko[i] = Zaiko[i] - maisu
⎿ 表示する(Kouka[i], "円：", maisu, "枚")
もし otsuri > 0 ならば:
⎿ 表示する("おつりが足りません")
"""
OTSURI_A = {"①": "otsuri % Kouka[i]", "②": "otsuri ÷ Kouka[i]", "③": "Kouka[i] ÷ otsuri", "④": "otsuri - Kouka[i]"}
OTSURI_I = {"①": "Zaiko[i]", "②": "maisu - Zaiko[i]", "③": "0", "④": "Zaiko[i] - maisu"}
OTSURI_OUT = ["500円：1枚", "100円：1枚", "50円：2枚", "10円：8枚"]

P_TOHYO = """
Hyou = [2, 0, 2, 3, 1, 2, 3, 0, 3, 2, 3, 0]
Tokuhyo = [0, 0, 0, 0]
i を 0 から 要素数(Hyou) - 1 まで 1 ずつ増やしながら繰り返す:
⎿ Tokuhyo[【ア】] = Tokuhyo[【ア】] + 1
saita = 0
j を 1 から 3 まで 1 ずつ増やしながら繰り返す:
｜ もし Tokuhyo[j] > Tokuhyo[saita] ならば:
⎿ ⎿ saita = j
表示する("最多得票は候補", saita, "で", Tokuhyo[saita], "票")
"""
P_DOHYO = """
dosu = 0
j を 0 から 3 まで 1 ずつ増やしながら繰り返す:
｜ もし Tokuhyo[j] == 【イ】 ならば:
⎿ ⎿ dosu = dosu + 1
もし dosu >= 2 ならば:
⎿ 表示する("最多得票の候補が", dosu, "人いるので決選投票を行う")
"""
TOHYO_A = {"①": "i", "②": "Hyou[i]", "③": "Tokuhyo[i]", "④": "Hyou[Tokuhyo[i]]"}
DOHYO_I = {"①": "saita", "②": "Tokuhyo[saita]", "③": "Tokuhyo[j]", "④": "j"}

CH = {6: {
"goal": "共通テスト用プログラム表記を正しく読み、変数や配列の値の変化をトレースで追えるようにする。順次・分岐・反復を組み合わせて処理を組み立て、境界の値でも正しく動くかを確かめる力をつける。"
        "（この章のプログラムでは、｜ と ⎿ は繰り返しや条件分岐の範囲を表す。÷ は商の整数部分、% は余り、/ はふつうの割り算。配列の添字は 0 から始まる。表示する(…) は ( ) 内の値や文字列をつなげて1行に表示する。）",
"items": [
 {"lv": "A", "tag": "トレース（代入）",
  "q": "次のプログラムについて答えよ。" + CODE(P_SWAP) +
       "（1）実行したときに表示される内容を答えよ。<br>"
       "（2）（03）〜（05）行目は、全体としてどのような処理をしているか。<br>"
       "（3）同じ処理を、変数 tmp を使って次のように書きたい。空欄 " + K("ア") + "・" + K("イ") + " に入る変数名を答えよ。" + CODE(P_SWAP2, start=3),
  "a": "（1）5 3　（2）x と y の値を入れかえている。　（3）ア y　イ tmp",
  "s": "（1）代入のたびに値を追う。(03) x ＝ 3 ＋ 5 ＝ 8、(04) y ＝ 8 − 5 ＝ 3、(05) x ＝ 8 − 3 ＝ 5。<br>"
       "（2）はじめ x ＝ 3, y ＝ 5 だったものが x ＝ 5, y ＝ 3 になっている。<br>"
       "（3）x の値を tmp に避難させてから、x に y の値を入れ、y に避難させておいた tmp（もとの x）を入れる。"
       "x = y と y = x の2行だけでは、1行目で x のもとの値が失われ、両方とも 5 になってしまう。<br>"
       "<b>ポイント</b>：「=」は等しいという意味ではなく、右辺の値を左辺の変数に入れる（代入する）という意味。代入すると変数のもとの値は消える。"},

 {"lv": "A", "tag": "演算子",
  "q": "次の（1）〜（5）の式の値を求めよ。また、（6）に答えよ。<br>"
       "（1）<code>17 ÷ 5</code>　（2）<code>17 % 5</code>　（3）<code>17 / 5</code>　（4）<code>2 ** 5</code>　（5）<code>整数(7 / 2)</code><br>"
       "（6）整数の変数 x の値が3の倍数のときに成り立つ条件を、% を用いて書け。<br>"
       "ただし、** はべき乗、整数( ) は小数点以下を切り捨てた整数を返す関数である。",
  "a": "（1）3　（2）2　（3）3.4　（4）32　（5）3　（6）x % 3 == 0",
  "s": "（1）$17=5\\times3+2$ なので商は3、（2）余りは2。（3）ふつうの割り算で 3.4。（4）$2^5=32$。（5）$7\\div2=3.5$ の小数点以下を切り捨てて3。"
       "（6）3で割った余りが0なら3の倍数。偶数かどうかなら x % 2 == 0。<br>"
       "<b>ポイント</b>：÷（商）と %（余り）は、桁を取り出す（123 % 10 ＝ 3、123 ÷ 10 ＝ 12）、偶数・奇数を判定するなど、プログラムでよく使う。比較は「==」、代入は「=」と区別する。"},

 {"lv": "A", "tag": "基本構造・フローチャート",
  "q": "（1）アルゴリズムを組み立てる3つの基本構造を答えよ。<br>"
       "（2）次のア〜オはフローチャートで使う記号である。それぞれの名称と意味を、下の語群から選べ。" + FIG_SYM +
       "語群：処理（計算や代入）　判断（条件による分岐）　端子（開始・終了）　データ（入力・出力）　ループ端（繰り返しの始まり）",
  "a": "（1）順次・分岐（選択）・反復（繰り返し）　（2）ア 端子（開始・終了）　イ 処理（計算や代入）　ウ 判断（条件による分岐）　エ ループ端（繰り返しの始まり）　オ データ（入力・出力）",
  "s": "（1）順次＝上から順に実行する、分岐＝条件によって実行する処理を変える、反復＝条件を満たす間などに同じ処理をくり返す。どんなアルゴリズムも、この3つの組合せで表せる。<br>"
       "（2）ループ端は、上の角を切った形で繰り返しの始まりを、それを上下逆にした形で終わりを表し、対にして使う。判断の記号からは、条件が成り立つ（Yes）・成り立たない（No）の2本の矢印が出る。<br>"
       "<b>ポイント</b>：共通テスト用プログラム表記では、分岐は「もし〜ならば:」、反復は「〜の間繰り返す:」「〜を…から…まで…ずつ増やしながら繰り返す:」で書く。"},

 {"lv": "A", "tag": "トレース（分岐）",
  "q": "変数 tokuten に整数が入っているとき、次のプログラムについて答えよ。" + CODE(P_BUNKI) +
       "（1）tokuten が 80、79、60、59 のとき、表示される文字をそれぞれ答えよ。<br>"
       "（2）次のように条件の順番を入れかえると、tokuten が 85 のときに表示される文字は何か。また、このプログラムで A が表示されることはあるか。" + CODE(P_BUNKI2),
  "a": "（1）80：A　79：B　60：B　59：C　（2）B、A が表示されることはない。",
  "s": "（1）条件は上から順に調べ、最初に成り立ったところの処理だけを実行する。80 は「80 以上」が成り立つので A。79 は「80 以上」が成り立たず「60 以上」が成り立つので B。60 も B。59 はどちらも成り立たないので C。<br>"
       "（2）85 は最初の「60 以上」が成り立つので B が表示され、その後の条件は調べない。80 以上の数は必ず 60 以上なので、「そうでなくもし tokuten >= 80」が調べられることはなく、A は決して表示されない。<br>"
       "<b>ポイント</b>：「そうでなくもし」は、それより上の条件がすべて成り立たなかったときだけ調べる。範囲で場合分けするときは、条件の順番と境界の値（80, 60）に注意する。"},

 {"lv": "B", "tag": "トレース（反復）",
  "q": "（1）次のプログラムを実行したときに表示される値を答えよ。また、繰り返しの中で i がとる値をすべて答えよ。" + CODE(P_LOOP1) +
       "（2）次のプログラムを実行したときに表示される値を答えよ。また、繰り返しの中で n が変わっていく値を順に答えよ。" + CODE(P_LOOP2) +
       "（3）（2）のプログラムの（01）行目を <code>n = 1000, kaisu = 0</code> に変えると、表示される値はいくつになるか。",
  "a": "（1）22、i は 1, 4, 7, 10　（2）6、n は 50, 25, 12, 6, 3, 1　（3）9",
  "s": "（1）i は 1 から 3 ずつ増え、10 を超えない範囲で 1, 4, 7, 10 の4回。goukei ＝ 1 ＋ 4 ＋ 7 ＋ 10 ＝ 22。<br>"
       "（2）÷ は商の整数部分なので、25 ÷ 2 ＝ 12、3 ÷ 2 ＝ 1。n が 1 になると条件 n ＞ 1 が成り立たなくなり、繰り返しを終える。繰り返しは6回。<br>"
       "（3）n は 500, 250, 125, 62, 31, 15, 7, 3, 1 と変わり、9回。これは「2で何回割ると1になるか」を数えており、$2^9=512\\leqq1000\\lt1024=2^{10}$ と対応している。<br>"
       "<b>ポイント</b>：繰り返しのトレースは、1回ごとに変数の値を表に書き出す。「〜の間繰り返す」は条件を繰り返しの<b>前</b>に調べ、成り立たなくなった時点で終わる。"},

 {"lv": "B", "tag": "トレース（配列）",
  "q": "次のプログラムについて答えよ。" + CODE(P_MAX) +
       "（1）実行したときに表示される内容を答えよ。<br>"
       "（2）（04）行目の <code>&gt;</code> を <code>&gt;=</code> に変えると、表示される内容はどうなるか。<br>"
       "（3）（04）行目の条件をどのように変えると、最小値とその添字を求めるプログラムになるか。また、そのとき表示される内容を答えよ。<br>"
       "（4）（02）行目を <code>saidai = 0, ichi = 0</code> にすると、配列の値によっては正しい最大値が求められない。どのような場合か。",
  "a": "（1）45 1　（2）45 3　（3）<code>Data[i] &lt; saidai</code>、表示は 7 2　（4）配列の値がすべて負の数の場合（例：[−5, −2, −9] では最大値 −2 ではなく 0 が表示される）。",
  "s": "（1）saidai は 12 → 45（i ＝ 1）と変わり、i ＝ 3 の 45 は「45 ＞ 45」が成り立たないので更新されない。i ＝ 4 の 30 も更新しない。<br>"
       "（2）「45 ≧ 45」が成り立つので、i ＝ 3 で ichi が 3 に更新される。同じ最大値が複数あるとき、最初の位置を求めるか最後の位置を求めるかが変わる。<br>"
       "（3）より小さい値が見つかったら更新する。12 → 7（i ＝ 2）となり、45, 45, 30 では更新されない。変数名は saidai のままでも動くが、saisho などに変えると読みやすい。<br>"
       "（4）saidai ＝ 0 から始めると、0 より大きい要素がない限り一度も更新されない。最初の要素 Data[0] を仮の最大値にすれば、どんな値の配列でも正しく求められる。<br>"
       "<b>ポイント</b>：比較の「＞」と「≧」のちがいは、同じ値（境界）が現れたときに表れる。初期値は「データの中の値」にするのが安全。"},

 {"lv": "B", "tag": "フローチャート",
  "q": "次のフローチャートで表される処理について答えよ。" + FIG_FLOW +
       "（1）表示される x と s の値を答えよ。<br>"
       "（2）「s = s + x」の処理は何回実行されるか。<br>"
       "（3）「s = s + x」を実行した直後の s の値を順に書き、s の値にどのような規則があるかを答えよ。<br>"
       "（4）判断の条件を「s &lt; 100」に変えると、表示される x と s の値はどうなるか。",
  "a": "（1）x ＝ 11、s ＝ 25　（2）5回　（3）1, 4, 9, 16, 25。s は奇数を1から順に足した和で、$k$ 回目には $k^2$（平方数）になる。　（4）x ＝ 21、s ＝ 100",
  "s": "（1）（3）x は 1, 3, 5, … と奇数になり、s は $1,\\ 1+3=4,\\ 4+5=9,\\ 9+7=16,\\ 16+9=25$ と増える。s ＝ 25 になった時点で x ＝ 11 で、条件 s ＜ 20 が成り立たないので表示する。<br>"
       "（2）s が 1, 4, 9, 16, 25 になる5回。<br>"
       "（4）$k^2\\geqq100$ となる最初の $k$ は10なので、s ＝ 100、x ＝ $2\\times10+1=21$。<br>"
       "このフローチャートを共通テスト用プログラム表記で書くと次のようになる。" + CODE(P_FLOW) +
       "<b>ポイント</b>：フローチャートの「判断から上に戻る矢印」は「〜の間繰り返す」に対応する。条件を調べるのは繰り返しの最初で、条件が成り立たなくなったときに抜ける。"},

 {"lv": "B", "tag": "トレース（二重ループ）",
  "q": "次のプログラムについて答えよ。" + CODE(P_NEST) +
       "（1）実行したときに表示される値を答えよ。<br>"
       "（2）（04）行目の条件を取り除き、（05）行目を毎回実行するようにすると、表示される値はいくつになるか。<br>"
       "（3）（1）のプログラムで、（03）行目の <code>j を i から 4 まで</code> を <code>j を 1 から 4 まで</code> に変えると、表示される値はいくつになるか。",
  "a": "（1）6　（2）10　（3）8",
  "s": "（1）i ≦ j の組 (i, j) のうち、i ＋ j が偶数のものを数える。(1,1)(1,3)(2,2)(2,4)(3,3)(4,4) の6組。<br>"
       "（2）i ＝ 1 のとき j は 1〜4 の4回、i ＝ 2 で3回、i ＝ 3 で2回、i ＝ 4 で1回、合計 $4+3+2+1=10$ 回。<br>"
       "（3）4×4 ＝ 16 組のうち i ＋ j が偶数のものは、i と j がともに奇数（2×2 ＝ 4組）か、ともに偶数（4組）の8組。<br>"
       "<b>ポイント</b>：二重ループの内側の繰り返しは、外側の1回ごとに最初から実行される。内側の範囲が外側の変数で変わる（j を i から）ときは、外側の値ごとに回数を数える。"},

 {"lv": "B", "tag": "トレース（配列の操作）",
  "q": "次のプログラムについて答えよ。" + CODE(P_REV) +
       "（1）実行した後の配列 A の内容を答えよ。<br>"
       "（2）（03）〜（06）行目の繰り返しは何回実行されるか。<br>"
       "（3）（03）行目の <code>n ÷ 2 - 1</code> を <code>n - 1</code> に変えると、実行した後の配列 A の内容はどうなるか。また、その理由を説明せよ。<br>"
       "（4）（01）行目を <code>A = [1, 2, 3, 4, 5, 6]</code> に変えて（もとのプログラムで）実行すると、A の内容はどうなるか。",
  "a": "（1）[4, 6, 1, 8, 3]　（2）2回　（3）[3, 8, 1, 6, 4]（もとのまま）。前半で入れかえた組を、後半でもう一度入れかえて元に戻してしまうから。　（4）[6, 5, 4, 3, 2, 1]",
  "s": "（1）（2）n ＝ 5 なので i は 0 から 5 ÷ 2 − 1 ＝ 1 まで、2回。i ＝ 0 で A[0] と A[4] を、i ＝ 1 で A[1] と A[3] を入れかえる。真ん中の A[2] はそのまま。配列を逆順に並べかえる処理である。<br>"
       "（3）i ＝ 0〜4 の5回になり、i ＝ 3 で A[3] と A[1]、i ＝ 4 で A[4] と A[0] をふたたび入れかえて元に戻る（i ＝ 2 は A[2] どうし）。<br>"
       "（4）n ＝ 6 で i は 0〜2 の3回。A[0]⇔A[5]、A[1]⇔A[4]、A[2]⇔A[3] で逆順になる。<br>"
       "<b>ポイント</b>：入れかえには一時的な変数（tmp）を使う。繰り返しの範囲（終わりの値）を1つ間違えるだけで結果が変わるので、要素数が奇数・偶数の両方で確かめる。"},

 {"lv": "C", "tag": "総合（おつりの計算）",
  "q": "生徒と先生の会話を読み、問いに答えよ。" +
       B("生徒A：自動販売機が、おつりをできるだけ少ない枚数の硬貨で払うようにしたいです。<br>"
         "先生：日本の硬貨なら、金額の大きい硬貨から順に、使えるだけ使っていけば枚数が最も少なくなります。ただし、機械の中の硬貨の数（在庫）には限りがありますね。<br>"
         "生徒A：配列 Kouka に硬貨の金額を大きい順に、Zaiko にそれぞれの硬貨の在庫の枚数を入れて、プログラムを作ってみます。") +
       NOTE + CODE(P_OTSURI) +
       "（1）硬貨の在庫が十分にあるとき、780円のおつりを最も少ない枚数で払うには、500円・100円・50円・10円の硬貨をそれぞれ何枚使えばよいか。また、合計は何枚か。<br>"
       "（2）空欄 " + K("ア") + "・" + K("イ") + " に入れるものとして最も適切なものを、それぞれの解答群のうちから一つずつ選べ。<br>" +
       K("ア") + " の解答群　" + "　".join(f"{c} <code>{e}</code>" for c, e in OTSURI_A.items()) + "<br>" +
       K("イ") + " の解答群　" + "　".join(f"{c} <code>{e}</code>" for c, e in OTSURI_I.items()) + "<br>"
       "（3）空欄を正しく埋めて実行したとき、表示される内容をすべて答えよ。また、実行した後の配列 Zaiko の内容を答えよ。<br>"
       "（4）続けて、Zaiko が（3）の実行後の内容のまま、（03）行目を <code>otsuri = 160</code> にして実行したとき、最後に表示される内容を答えよ。また、そのとき払えなかった金額はいくらか。",
  "a": "（1）500円1枚、100円2枚、50円1枚、10円3枚、合計7枚　（2）ア ②　イ ①　（3）500円：1枚／100円：1枚／50円：2枚／10円：8枚、Zaiko は [2, 0, 0, 12]　（4）おつりが足りません、40円",
  "s": "（1）$780=500\\times1+100\\times2+50\\times1+10\\times3$ で7枚。<br>"
       "（2）その硬貨を最大何枚使えるかは、おつりを硬貨の金額で割った<b>商</b>。それが在庫より多ければ、在庫の枚数だけ使う。<br>"
       "（3）500円：780 ÷ 500 ＝ 1 枚（残り 280）。100円：280 ÷ 100 ＝ 2 だが在庫1枚なので1枚（残り 180）。50円：180 ÷ 50 ＝ 3 だが在庫2枚なので2枚（残り 80）。10円：80 ÷ 10 ＝ 8 枚（残り 0）。在庫は [3−1, 1−1, 2−2, 20−8] ＝ [2, 0, 0, 12]。合計12枚で、在庫が十分なとき（7枚）より多い。<br>"
       "（4）500円は 160 ÷ 500 ＝ 0 枚、100円・50円は在庫0枚、10円は 160 ÷ 10 ＝ 16 だが在庫12枚なので12枚。残り $160-120=40$ 円が払えず、（11）行目の条件が成り立って「おつりが足りません」と表示される。<br>"
       "<b>ポイント</b>：「使えるだけ使う」は割り算の商、「在庫が上限」は条件分岐で表す。実際の自動販売機でも、つり銭が少なくなると「つり銭切れ」などと表示して、おつりが出ないように受け付けを制限することがある。"},

 {"lv": "C", "tag": "総合（投票の集計）",
  "q": "クラスで、文化祭の出し物を候補0〜3の中から投票で選ぶ。生徒と先生の会話を読み、問いに答えよ。" +
       B("生徒A：12人の投票を、配列 Hyou に投票した候補の番号として入れました。候補ごとの得票数を配列 Tokuhyo に数えて、最多得票の候補を表示します。<br>"
         "先生：同じ得票数の候補が出たときのことも考えておきましょう。") +
       NOTE + CODE(P_TOHYO) +
       "（1）空欄 " + K("ア") + "（2か所とも同じものが入る）に入れるものとして最も適切なものを、次の①〜④のうちから一つ選べ。<br>"
       + "　".join(f"{c} <code>{e}</code>" for c, e in TOHYO_A.items()) + "<br>"
       "（2）空欄を正しく埋めて実行したとき、（03）〜（04）行目の繰り返しが終わった後の配列 Tokuhyo の内容と、表示される内容を答えよ。<br>"
       "（3）候補3も候補2と同じ得票数なのに、候補2が表示される。その理由を説明せよ。<br>"
       "（4）最多得票の候補が複数あるときに決選投票を知らせるため、プログラムの最後に次の処理を加えた。空欄 " + K("イ") + " に入れるものとして最も適切なものを、下の①〜④のうちから一つ選べ。また、このとき追加した部分で表示される内容を答えよ。"
       + CODE(P_DOHYO, start=10) + "　".join(f"{c} <code>{e}</code>" for c, e in DOHYO_I.items()),
  "a": "（1）②　（2）Tokuhyo は [3, 1, 4, 4]、表示は「最多得票は候補2で4票」　（3）（07）行目の条件が「＞」なので、候補3の得票数4は、それまでの最多の候補2の4票より大きくなく、saita が更新されないから。　（4）②、「最多得票の候補が2人いるので決選投票を行う」",
  "s": "（1）i 番目の票は候補 Hyou[i] への票なので、Tokuhyo[Hyou[i]] を1増やす。①③④は、添字が 0〜3 の範囲をこえて誤りになる（例：①は i ＝ 4 のとき Tokuhyo[4] を参照する）。<br>"
       "（2）候補0が3票（2番目・8番目・12番目）、候補1が1票、候補2が4票、候補3が4票で、合計12票。saita は 0 → 2（j ＝ 2 で 4 ＞ 3）となり、j ＝ 3 では 4 ＞ 4 が成り立たない。<br>"
       "（3）（2）の「4 ＞ 4 が成り立たない」ため。≧ にすると、同票のうち最後の候補3が表示される。<br>"
       "（4）最多得票数 Tokuhyo[saita] と同じ得票数の候補を数える。① saita（＝2）は得票数ではなく候補の番号、③ は常に成り立つ、④ は候補の番号と得票数を比べていて意味がない。dosu ＝ 2 なので表示される。<br>"
       "<b>ポイント</b>：「値を添字に使って数える」（Tokuhyo[Hyou[i]]）は集計の定番。最大値を求める処理では、同じ値が複数あるときの扱いを必ず確かめる。"},
]}}

# ---------------- 検算 ----------------


def _check(ch):
    items = ch["items"]
    lv = [it["lv"] for it in items]
    assert lv == sorted(lv) and lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2, lv
    for it in items:
        for k in ("tag", "q", "a", "s"):
            assert it[k].strip(), k
        for k in ("q", "a", "s"):
            assert it[k].count("$") % 2 == 0 and "$$" not in it[k], it[k][:40]
            assert "【" not in it[k], it[k][:40]
            assert "　 " not in it[k]
        assert "<b>ポイント</b>" in it["s"]
        assert it["q"].count("<pre") == it["q"].count("</pre>")
        for pre in re.findall(r"<pre.*?</pre>", it["q"], re.S):
            assert "$" not in pre


def verify():
    _check(CH[6])
    items = CH[6]["items"]
    from itertools import product
    import random

    # 6-1 代入
    out, env = run(P_SWAP)
    assert out == ["5 3"]
    good = [(a, b) for a in ("x", "y", "tmp") for b in ("x", "y", "tmp")
            if (lambda e: (e["x"], e["y"]) == (5, 3))(run("x = 3\ny = 5\n" + P_SWAP2.lstrip("\n"), ア=a, イ=b)[1])]
    assert good == [("y", "tmp")], good
    e = run("x = 3\ny = 5\nx = y\ny = x\n")[1]
    assert (e["x"], e["y"]) == (5, 5)
    assert CODE(P_SWAP2, start=3).count("(03) tmp = x") == 1

    # 6-2 演算子
    assert (17 // 5, 17 % 5, 17 / 5, 2 ** 5, int(7 / 2)) == (3, 2, 3.4, 32, 3)
    assert run("x = 17 ÷ 5\ny = 整数(7 / 2)")[1]["x"] == 3 and run("y = 整数(7 / 2)")[1]["y"] == 3
    assert (123 % 10, 123 // 10) == (3, 12)

    # 6-4 分岐
    res = {v: run(f"tokuten = {v}\n" + P_BUNKI.lstrip("\n"))[0] for v in (80, 79, 60, 59)}
    assert res == {80: ["A"], 79: ["B"], 60: ["B"], 59: ["C"]}
    assert run("tokuten = 85\n" + P_BUNKI2.lstrip("\n"))[0] == ["B"]
    assert all(run(f"tokuten = {v}\n" + P_BUNKI2.lstrip("\n"))[0] != ["A"] for v in range(0, 101))

    # 6-5 反復
    out, env = run(P_LOOP1)
    assert out == ["22"] and list(range(1, 11, 3)) == [1, 4, 7, 10]
    ns, n = [], 100
    while n > 1:
        n //= 2
        ns.append(n)
    assert run(P_LOOP2)[0] == ["6"] and ns == [50, 25, 12, 6, 3, 1]
    assert run(P_LOOP2.replace("n = 100,", "n = 1000,"))[0] == ["9"]
    ns, n = [], 1000
    while n > 1:
        n //= 2
        ns.append(n)
    assert ns == [500, 250, 125, 62, 31, 15, 7, 3, 1]

    # 6-6 最大値
    assert run(P_MAX)[0] == ["45 1"]
    assert run(P_MAX.replace("Data[i] > saidai", "Data[i] >= saidai"))[0] == ["45 3"]
    assert run(P_MAX.replace("Data[i] > saidai", "Data[i] < saidai"))[0] == ["7 2"]
    neg = P_MAX.replace("[12, 45, 7, 45, 30]", "[-5, -2, -9]")
    assert run(neg)[0] == ["-2 1"] and run(neg.replace("saidai = Data[0]", "saidai = 0"))[0] == ["0 0"]
    assert P_MAX.strip("\n").split("\n")[3].startswith("｜ もし Data[i] > saidai")

    # 6-7 フローチャート（同じ処理のプログラム）
    out, env = run(P_FLOW)
    assert out == ["11 25"]
    cnt, ss, x, s = 0, [], 1, 0
    while s < 20:
        s += x; x += 2; cnt += 1; ss.append(s)
    assert cnt == 5 and ss == [1, 4, 9, 16, 25] and all(v == (k + 1) ** 2 for k, v in enumerate(ss))
    assert run(P_FLOW.replace("s < 20", "s < 100"))[0] == ["21 100"]
    assert "s &lt; 20" in FIG_FLOW and "x = 1, s = 0" in FIG_FLOW

    # 6-8 二重ループ
    assert run(P_NEST)[0] == ["6"]
    assert [(i, j) for i in range(1, 5) for j in range(i, 5) if (i + j) % 2 == 0] == [(1, 1), (1, 3), (2, 2), (2, 4), (3, 3), (4, 4)]
    nocond = P_NEST.replace("｜ ｜ もし (i + j) % 2 == 0 ならば:\n⎿ ⎿ ⎿ kosu = kosu + 1", "⎿ ⎿ kosu = kosu + 1")
    assert nocond != P_NEST and run(nocond)[0] == ["10"]
    assert run(P_NEST.replace("j を i から 4 まで", "j を 1 から 4 まで"))[0] == ["8"]

    # 6-9 逆順
    assert run(P_REV)[1]["A"] == [4, 6, 1, 8, 3]
    assert len(range(0, 5 // 2 - 1 + 1)) == 2
    assert run(P_REV.replace("n ÷ 2 - 1", "n - 1"))[1]["A"] == [3, 8, 1, 6, 4]
    assert run(P_REV.replace("[3, 8, 1, 6, 4]", "[1, 2, 3, 4, 5, 6]"))[1]["A"] == [6, 5, 4, 3, 2, 1]

    # 6-10 おつり
    unlimited = P_OTSURI.replace("Zaiko = [3, 1, 2, 20]", "Zaiko = [99, 99, 99, 99]")
    o1 = run(unlimited, ア="otsuri ÷ Kouka[i]", イ="Zaiko[i]")[0]
    assert o1 == ["500円：1枚", "100円：2枚", "50円：1枚", "10円：3枚"] and 1 + 2 + 1 + 3 == 7
    good = []
    for a, b in product(OTSURI_A, OTSURI_I):
        try:
            if run(P_OTSURI, ア=OTSURI_A[a], イ=OTSURI_I[b])[0] == OTSURI_OUT and \
               run(unlimited, ア=OTSURI_A[a], イ=OTSURI_I[b])[0] == o1:
                good.append((a, b))
        except ZeroDivisionError:
            pass
    assert good == [("②", "①")], good
    out, env = run(P_OTSURI, ア="otsuri ÷ Kouka[i]", イ="Zaiko[i]")
    assert out == OTSURI_OUT and env["Zaiko"] == [2, 0, 0, 12] and env["otsuri"] == 0 and 1 + 1 + 2 + 8 == 12
    P4 = P_OTSURI.replace("Zaiko = [3, 1, 2, 20]", "Zaiko = [2, 0, 0, 12]").replace("otsuri = 780", "otsuri = 160")
    out, env = run(P4, ア="otsuri ÷ Kouka[i]", イ="Zaiko[i]")
    assert out == ["500円：0枚", "100円：0枚", "50円：0枚", "10円：12枚", "おつりが足りません"] and env["otsuri"] == 40
    assert "（3）" + "／".join(OTSURI_OUT) in items[9]["a"]
    assert P_OTSURI.strip("\n").split("\n")[10] == "もし otsuri > 0 ならば:" and P_OTSURI.strip("\n").split("\n")[2] == "otsuri = 780"

    # 6-11 投票
    hyou = [2, 0, 2, 3, 1, 2, 3, 0, 3, 2, 3, 0]
    assert f"Hyou = {hyou}" in P_TOHYO and len(hyou) == 12
    assert [hyou.count(k) for k in range(4)] == [3, 1, 4, 4] and [i + 1 for i, v in enumerate(hyou) if v == 0] == [2, 8, 12]
    good = []
    for c, e in TOHYO_A.items():
        try:
            o, env = run(P_TOHYO, ア=e)
            if env["Tokuhyo"] == [3, 1, 4, 4]:
                good.append(c)
        except IndexError:
            pass
    assert good == ["②"], good
    o, env = run(P_TOHYO, ア="Hyou[i]")
    assert o == ["最多得票は候補2で4票"] and env["Tokuhyo"] == [3, 1, 4, 4]
    assert run(P_TOHYO.replace("Tokuhyo[j] > Tokuhyo[saita]", "Tokuhyo[j] >= Tokuhyo[saita]"), ア="Hyou[i]")[0] == ["最多得票は候補3で4票"]
    full = P_TOHYO.rstrip("\n") + P_DOHYO
    good = []
    random.seed(1)
    datasets = [hyou] + [[random.randrange(4) for _ in range(12)] for _ in range(300)]
    for c, e in DOHYO_I.items():
        ok = True
        for h in datasets:
            o = run(full.replace(f"Hyou = {hyou}", f"Hyou = {h}"), ア="Hyou[i]", イ=e)[0]
            cnt = [h.count(k) for k in range(4)]
            d = cnt.count(max(cnt))
            want = [f"最多得票は候補{cnt.index(max(cnt))}で{max(cnt)}票"] + ([f"最多得票の候補が{d}人いるので決選投票を行う"] if d >= 2 else [])
            if o != want:
                ok = False
                break
        if ok:
            good.append(c)
    assert good == ["②"], good
    assert run(full, ア="Hyou[i]", イ="Tokuhyo[saita]")[0][1] == "最多得票の候補が2人いるので決選投票を行う"
    assert P_TOHYO.strip("\n").split("\n")[6].startswith("｜ もし Tokuhyo[j] > Tokuhyo[saita]")
