"""問題集 第12章 データの分析。問題はすべて書き下ろし。
verify() は代表値・分散・四分位数（日本の高校の方法：中央値で上下に分け、個数が奇数なら中央値を除いてそれぞれの中央値）・
相関係数・回帰直線を fractions で厳密に計算して答えと照合し、プログラムと同じ処理も実行する。図の座標も計算で出す。"""
import re, html, math, random
from fractions import Fraction as Fr
from math import comb

# ---------------- 書式の道具 ----------------


def B(s):
    return f'<div class="bun">{s}</div>'


def K(s):
    """空欄の枠"""
    return ('<span style="display:inline-block;border:1px solid #333;min-width:1.3em;padding:0 2px;'
            f'text-align:center;line-height:1.25;font-weight:bold;background:#fff">{s}</span>')


def CODE(src, start=1):
    """共通テスト用プログラム表記。行番号をつけ、< > & を実体参照にし、【ア】を空欄の枠にする"""
    rows = []
    for i, ln in enumerate(src.strip("\n").split("\n"), start):
        e = html.escape(ln, quote=False)
        e = re.sub(r"【(.+?)】", lambda m: K(m.group(1)), e)
        rows.append(f"({i:02d}) {e}")
    return '<pre class="code">' + "\n".join(rows) + "</pre>"


def TB(head, rows, cls=""):
    c = f' class="{cls}"' if cls else ""
    h = ("<tr>" + "".join(f"<th>{x}</th>" for x in head) + "</tr>") if head else ""
    r = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table{c}>{h}{r}</table>"


def _f(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")


def _t(x, y, s, size=10.5, anchor="start", c="#222"):
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" text-anchor="{anchor}" fill="{c}">{s}</text>'


def _l(x1, y1, x2, y2, c="#555", w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{c}" stroke-width="{w}"{d}/>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def FN_NOTE():
    return "（関数の定義は「関数 名前(引数):」の行で始め、「〜 を返す」でその値を戻り値として返し、関数の処理を終える。）"


# ---------------- 統計の道具（検算用・図用） ----------------


def med(v):
    v = sorted(v)
    n = len(v)
    return Fr(v[n // 2]) if n % 2 else Fr(v[n // 2 - 1] + v[n // 2], 2)


def quartiles(v):
    """日本の高校の方法：中央値で下半分・上半分に分ける（奇数個なら中央値を除く）"""
    v = sorted(v)
    n = len(v)
    lo, hi = v[:n // 2], v[(n + 1) // 2:]
    return med(lo), med(v), med(hi)


def mean(v):
    return Fr(sum(v), len(v))


def var(v):
    m = mean(v)
    return sum((x - m) ** 2 for x in v) / len(v)


def corr_parts(x, y):
    mx, my = mean(x), mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxx, syy, sxy


def corr(x, y):
    sxx, syy, sxy = corr_parts(x, y)
    return float(sxy) / math.sqrt(sxx * syy)


# ---------------- 図 ----------------


def fig_boxes(rows, lo=0, hi=100, step=10, unit="点", W=430):
    """横向きの箱ひげ図。rows = [(ラベル, (最小, Q1, 中央値, Q3, 最大)), ...]"""
    left, right, top, rh = 50, W - 20, 12, 40
    X = lambda v: left + (right - left) * (v - lo) / (hi - lo)
    H = top + rh * len(rows) + 30
    p = []
    yb = top + rh * len(rows)
    for v in range(lo, hi + 1, step):
        p.append(_l(X(v), top, X(v), yb, "#e2e2e2"))
        p.append(_l(X(v), yb, X(v), yb + 4, "#333"))
        p.append(_t(X(v), yb + 16, str(v), 10, "middle"))
    p.append(_l(X(lo), yb, X(hi), yb, "#333"))
    p.append(_t(right + 2, yb + 28, f"（{unit}）", 10, "end"))
    for i, (lab, (mn, q1, q2, q3, mx)) in enumerate(rows):
        yc = top + rh * i + rh / 2
        p.append(_t(left - 10, yc + 4, lab, 10.5, "end"))
        p.append(_l(X(mn), yc, X(q1), yc, "#333", 1.2))
        p.append(_l(X(q3), yc, X(mx), yc, "#333", 1.2))
        p.append(_l(X(mn), yc - 7, X(mn), yc + 7, "#333", 1.2))
        p.append(_l(X(mx), yc - 7, X(mx), yc + 7, "#333", 1.2))
        p.append(f'<rect x="{_f(X(q1))}" y="{_f(yc - 11)}" width="{_f(X(q3) - X(q1))}" height="22" fill="#e6f2f8" stroke="#333" stroke-width="1.2"/>')
        p.append(_l(X(q2), yc - 11, X(q2), yc + 11, "#0b5f84", 2))
    return _svg(W, H, p)


def fig_scatter(xs, ys, xr, yr, xt, yt, xlab, ylab, labels=None, line=None, W=330, Hh=250):
    """散布図。xr, yr は軸の範囲 (min, max)、xt, yt は目盛りの間隔。line = (傾き, 切片)"""
    left, bottom, right, top = 46, Hh - 36, W - 16, 14
    X = lambda v: left + (right - left) * (v - xr[0]) / (xr[1] - xr[0])
    Y = lambda v: bottom - (bottom - top) * (v - yr[0]) / (yr[1] - yr[0])
    p = []
    v = xr[0]
    while v <= xr[1] + 1e-9:
        p.append(_l(X(v), top, X(v), bottom, "#e8e8e8"))
        p.append(_l(X(v), bottom, X(v), bottom + 4, "#333"))
        p.append(_t(X(v), bottom + 15, _f(v), 10, "middle"))
        v += xt
    v = yr[0]
    while v <= yr[1] + 1e-9:
        p.append(_l(left, Y(v), right, Y(v), "#e8e8e8"))
        p.append(_l(left - 4, Y(v), left, Y(v), "#333"))
        p.append(_t(left - 7, Y(v) + 4, _f(v), 10, "end"))
        v += yt
    p.append(_l(left, bottom, right, bottom, "#333"))
    p.append(_l(left, top, left, bottom, "#333"))
    p.append(_t((left + right) / 2, bottom + 30, xlab, 10.5, "middle"))
    p.append(f'<text x="12" y="{_f((top + bottom) / 2)}" font-size="10.5" text-anchor="middle" fill="#222" '
             f'transform="rotate(-90 12 {_f((top + bottom) / 2)})">{ylab}</text>')
    if line:
        a, b = line
        x1, x2 = xr[0], xr[1]
        p.append(_l(X(x1), Y(a * x1 + b), X(x2), Y(a * x2 + b), "#d27a00", 1.6))
    for i, (x, y) in enumerate(zip(xs, ys)):
        p.append(f'<circle cx="{_f(X(x))}" cy="{_f(Y(y))}" r="3.4" fill="#0b5f84"/>')
        if labels:
            p.append(_t(X(x) + 6, Y(y) - 5, labels[i], 10, "start"))
    return _svg(W, Hh, p)


# ---------------- データ ----------------
D1 = [3, 7, 5, 8, 5, 9, 4, 5, 8]
D2 = [5, 9, 1, 7, 3]
D3 = [12, 15, 18, 20, 22, 25, 27, 30, 34, 41]
BOX3 = [("A組", (22, 45, 58, 70, 92)), ("B組", (30, 50, 62, 68, 85)), ("C組", (15, 38, 52, 75, 98))]
CX, CY = [2, 4, 6, 8, 10], [3, 5, 4, 8, 10]
RX, RY = [22, 24, 26, 28, 30, 32], [28, 29, 39, 45, 47, 58]
CROSS = [[36, 84], [44, 36]]      # 行：毎日食べる／食べない、列：眠い／眠くない
SEED, NSET = 9, 1000
DOKU = [10, 25, 30, 35, 40, 45, 50, 55, 60, 70, 150]
BOX_OPT = [("①", (10, 32.5, 45, 57.5, 150)), ("②", (10, 30, 50, 60, 150)), ("③", (10, 30, 45, 60, 150))]
SX = [2, 6, 7, 1, 9, 5, 8, 10]
SY = [58, 80, 79, 57, 91, 79, 90, 50]
SLAB = list("ABCDEFGH")


def coin_sim():
    rng = random.Random(SEED)
    cnt = [0] * 21
    for _ in range(NSET):
        cnt[sum(rng.random() < 0.5 for _ in range(20))] += 1
    return cnt


COIN = [14, 32, 78, 131, 157, 177, 163, 123, 69, 34, 22]   # 5回以下, 6, 7, …, 14, 15回以上
COIN_LAB = ["5以下"] + [str(k) for k in range(6, 15)] + ["15以上"]

P_Q = """
関数 chuoti(Data, hidari, migi):
｜ kosu = migi - hidari + 1
｜ naka = (hidari + migi) ÷ 2
｜ もし kosu % 2 == 1 ならば:
｜ ｜ Data[naka] を返す
｜ そうでなければ:
⎿ ⎿ 【ア】 を返す
Data = [10, 25, 30, 35, 40, 45, 50, 55, 60, 70, 150]
n = 要素数(Data)
q2 = chuoti(Data, 0, n - 1)
q1 = chuoti(Data, 0, 【イ】)
q3 = chuoti(Data, 【ウ】, n - 1)
表示する(q1, q2, q3)
"""

P_R = f"""
X = {SX}
Y = {SY}
n = 要素数(X)
gx = 0, gy = 0
i を 0 から n - 1 まで 1 ずつ増やしながら繰り返す:
｜ gx = gx + X[i]
⎿ gy = gy + Y[i]
mx = gx / n, my = gy / n
sxx = 0, syy = 0, sxy = 0
i を 0 から n - 1 まで 1 ずつ増やしながら繰り返す:
｜ sxx = sxx + (X[i] - mx) ** 2
｜ syy = syy + (Y[i] - my) ** 2
⎿ sxy = sxy + 【ア】
r = 【イ】
表示する(r)
"""

QDEF = "四分位数は、データを小さい順に並べて中央値を境に下半分と上半分に分け（データの個数が奇数のときは中央値を除く）、下半分の中央値を第1四分位数、上半分の中央値を第3四分位数とする。"

CH = {12: {
"goal": "平均値・中央値・最頻値、分散・標準偏差、四分位数と箱ひげ図、相関係数と回帰直線を正確に計算し、図や表から言えること・言えないことを区別する。クロス集計と仮説検定の考え方で、データから判断する手順を身につける。",
"items": [
 {"lv": "A", "tag": "代表値",
  "q": "次の9個のデータの平均値・中央値・最頻値を求めよ。<br>" + "、".join(map(str, D1)),
  "a": "平均値 6、中央値 5、最頻値 5",
  "s": "合計は54なので平均値は $\\dfrac{54}{9}=6$。小さい順に 3, 4, 5, 5, 5, 7, 8, 8, 9 と並べると、中央（5番目）は5。最も多く現れる値は5（3回）。<br>"
       "<b>ポイント</b>：中央値は<b>必ず並べかえてから</b>。データの個数が偶数のときは、中央の2つの平均をとる。"},

 {"lv": "A", "tag": "分散と標準偏差",
  "q": "（1）次の5個のデータの平均値・分散・標準偏差を求めよ。<br>" + "、".join(map(str, D2)) + "<br>"
       "（2）（1）の各データを2倍して3を足した5個のデータの、平均値・分散・標準偏差を求めよ。",
  "a": "（1）平均値 5、分散 8、標準偏差 $2\\sqrt2\\fallingdotseq2.83$　（2）平均値 13、分散 32、標準偏差 $4\\sqrt2\\fallingdotseq5.66$",
  "s": "（1）合計25で平均5。偏差は 0, 4, −4, 2, −2、その2乗は 0, 16, 16, 4, 4 で合計40。分散 $\\dfrac{40}{5}=8$、標準偏差 $\\sqrt8=2\\sqrt2\\fallingdotseq2.83$。<br>"
       "（2）データは 13, 21, 5, 17, 9。平均は $2\\times5+3=13$。偏差はすべて2倍になるので、分散は $2^2=4$ 倍の32、標準偏差は2倍の $4\\sqrt2\\fallingdotseq5.66$。3を足しても散らばりは変わらない。<br>"
       "<b>ポイント</b>：$y=ax+b$ と変換すると、平均値は $a\\bar{x}+b$、分散は $a^2$ 倍、標準偏差は $|a|$ 倍。足した $b$ は散らばりに影響しない。"},

 {"lv": "A", "tag": "四分位数",
  "q": QDEF + "<br>（1）次の10個のデータの最小値・第1四分位数・中央値・第3四分位数・最大値と、四分位範囲を求めよ。<br>" + "、".join(map(str, D3)) +
       "<br>（2）（1）のデータに 45 を加えた11個のデータの、第1四分位数・中央値・第3四分位数を求めよ。",
  "a": "（1）最小値12、第1四分位数18、中央値23.5、第3四分位数30、最大値41、四分位範囲12　（2）第1四分位数18、中央値25、第3四分位数34",
  "s": "（1）中央値は5番目と6番目の平均 $\\dfrac{22+25}{2}=23.5$。下半分 12, 15, 18, 20, 22 の中央値18が第1四分位数、上半分 25, 27, 30, 34, 41 の中央値30が第3四分位数。四分位範囲は $30-18=12$。<br>"
       "（2）11個の中央値は6番目の25。これを除いた下半分 12, 15, 18, 20, 22 から18、上半分 27, 30, 34, 41, 45 から34。<br>"
       "<b>ポイント</b>：個数が奇数のときは中央値を両側から除いて半分ずつに分ける。四分位範囲＝第3四分位数－第1四分位数は、外れ値の影響を受けにくい散らばりの指標。"},

 {"lv": "A", "tag": "相関",
  "q": "相関についての記述として正しいものを、次の①〜④のうちから一つ選べ。<br>"
       "① 相関係数が −0.9 のときは、0.5 のときよりも相関が弱い。<br>"
       "② 相関係数が0に近いとき、2つの変量の間にはどのような関係もない。<br>"
       "③ 2つの変量の間に強い正の相関があれば、一方が他方の原因であるといえる。<br>"
       "④ 相関係数は −1 以上 1 以下の値をとる。",
  "a": "④",
  "s": "④ 正しい。<br>"
       "① 誤り。相関の強さは絶対値で判断する。$|-0.9|\\gt0.5$ なので −0.9 のほうが強い（強い負の相関）。<br>"
       "② 誤り。相関係数は<b>直線的な</b>関係の強さを表す。点が放物線の形に並ぶなど、直線的でない関係があっても0に近くなることがある。<br>"
       "③ 誤り。相関関係があっても因果関係があるとは限らない。両方に影響する別の要因（たとえば気温）があると、直接の関係がなくても相関が現れる（疑似相関）。<br>"
       "<b>ポイント</b>：相関係数の読み方は「符号で向き、絶対値で強さ、直線的な関係だけを測る、因果は別問題」。"},

 {"lv": "B", "tag": "箱ひげ図",
  "q": "ある学校の A組・B組・C組（各40人）の数学のテストの得点を、箱ひげ図に表した。"
       + fig_boxes(BOX3) + TB(["", "最小値", "第1四分位数", "中央値", "第3四分位数", "最大値"], [[lab, *v] for lab, v in BOX3]) +
       "（1）箱ひげ図から読み取れることとして正しいものを、次の①〜④のうちから一つ選べ。<br>"
       "① 四分位範囲が最も大きいのは C組である。<br>② 範囲（最大値－最小値）が最も小さいのは A組である。<br>"
       "③ B組の平均点は62点である。<br>④ C組では、75点以上の生徒が必ず11人以上いる。<br>"
       "（2）A組で、45点以下の生徒は少なくとも何人いるか。",
  "a": "（1）①　（2）10人",
  "s": "40人のデータを小さい順に $x_1\\leqq x_2\\leqq\\cdots\\leqq x_{40}$ とすると、中央値は $\\dfrac{x_{20}+x_{21}}{2}$、第1四分位数は $\\dfrac{x_{10}+x_{11}}{2}$、第3四分位数は $\\dfrac{x_{30}+x_{31}}{2}$。<br>"
       "（1）① 四分位範囲は A 25、B 18、C 37 で C が最大。正しい。<br>"
       "② 範囲は A 70、B 55、C 83 で、最も小さいのは B。誤り。<br>"
       "③ 箱ひげ図から平均値は分からない（62点は中央値）。誤り。<br>"
       "④ 第3四分位数が75なので $x_{31}\\geqq75$ で、$x_{31}$〜$x_{40}$ の10人は75点以上。しかし $x_{30}=74,\\ x_{31}=76$ のような場合は75点以上がちょうど10人なので、「必ず11人以上」とはいえない。誤り。<br>"
       "（2）$\\dfrac{x_{10}+x_{11}}{2}=45$ で $x_{10}\\leqq x_{11}$ なので $x_{10}\\leqq45$。$x_1$〜$x_{10}$ の10人は45点以下。$x_{10}=44,\\ x_{11}=46$ のときはちょうど10人なので、「少なくとも10人」。<br>"
       "<b>ポイント</b>：箱ひげ図から確実に言えるのは、5つの値と「その値で区切られた各部分にほぼ4分の1ずつ入る」ことだけ。人数は、四分位数が何番目と何番目の平均かを考えて「少なくとも」で答える。"},

 {"lv": "B", "tag": "相関係数",
  "q": "5人の生徒について、1週間の読書時間 $x$（時間）と、漢字テストの得点 $y$（点）を調べた。"
       + TB(["生徒", "1", "2", "3", "4", "5"], [["$x$", *CX], ["$y$", *CY]]) +
       "（1）$x$ と $y$ の共分散を求めよ。<br>"
       "（2）$x$ と $y$ の相関係数を、小数第3位を四捨五入して求めよ。必要なら $\\sqrt{1360}\\fallingdotseq36.88$ を用いてよい。<br>"
       "（3）$x$ をすべて分の単位（60倍）に直したとき、共分散と相関係数はそれぞれどうなるか。",
  "a": "（1）6.8　（2）0.92　（3）共分散は60倍の408になり、相関係数は変わらない（0.92）",
  "s": "平均は $\\bar{x}=6,\\ \\bar{y}=6$。<br>"
       + TB(["生徒", "1", "2", "3", "4", "5", "合計"],
            [["$x-\\bar{x}$", -4, -2, 0, 2, 4, ""], ["$y-\\bar{y}$", -3, -1, -2, 2, 4, ""],
             ["$(x-\\bar{x})^2$", 16, 4, 0, 4, 16, 40], ["$(y-\\bar{y})^2$", 9, 1, 4, 4, 16, 34],
             ["$(x-\\bar{x})(y-\\bar{y})$", 12, 2, 0, 4, 16, 34]]) +
       "（1）共分散は $\\dfrac{34}{5}=6.8$。<br>"
       "（2）$r=\\dfrac{34}{\\sqrt{40}\\sqrt{34}}=\\dfrac{34}{\\sqrt{1360}}\\fallingdotseq\\dfrac{34}{36.88}\\fallingdotseq0.92$。強い正の相関がある。<br>"
       "（3）$x$ の偏差がすべて60倍になるので共分散も60倍の $6.8\\times60=408$。標準偏差も60倍になり、相関係数の分子と分母が同じく60倍になるので、相関係数は変わらない。<br>"
       "<b>ポイント</b>：相関係数 $r=\\dfrac{\\text{共分散}}{(x\\text{ の標準偏差})(y\\text{ の標準偏差})}=\\dfrac{\\sum(x-\\bar{x})(y-\\bar{y})}{\\sqrt{\\sum(x-\\bar{x})^2}\\sqrt{\\sum(y-\\bar{y})^2}}$。共分散は単位によって変わるが、相関係数は単位によらない。"},

 {"lv": "B", "tag": "回帰直線",
  "q": "ある店で、6日間の最高気温 $x$（℃）とアイスクリームの販売数 $y$（個）を調べた。"
       + TB(["日", "1", "2", "3", "4", "5", "6"], [["$x$", *RX], ["$y$", *RY]])
       + fig_scatter(RX, RY, (20, 34), (20, 60), 2, 10, "最高気温 x（℃）", "販売数 y（個）") +
       "（1）$x$ と $y$ の平均値を求めよ。<br>"
       "（2）$y$ を $x$ で予測する回帰直線 $y=ax+b$ を求めよ。回帰直線の傾きは $a=\\dfrac{\\sum(x-\\bar{x})(y-\\bar{y})}{\\sum(x-\\bar{x})^2}$ で、直線は点 $(\\bar{x},\\ \\bar{y})$ を通る。<br>"
       "（3）最高気温が31℃の日の販売数を、回帰直線を使って予測せよ。<br>"
       "（4）この回帰直線で最高気温40℃の日を予測するときに注意すべきことを述べよ。",
  "a": "（1）$\\bar{x}=27,\\ \\bar{y}=41$　（2）$y=3x-40$　（3）53個　（4）調べた範囲（22〜32℃）の外の予測（外挿）なので、同じ関係が成り立つとは限らず、予測が大きく外れるおそれがある",
  "s": "（1）$\\bar{x}=\\dfrac{162}{6}=27$、$\\bar{y}=\\dfrac{246}{6}=41$。<br>"
       "（2）偏差は $x$ が −5, −3, −1, 1, 3, 5、$y$ が −13, −12, −2, 4, 6, 17。"
       "$\\sum(x-\\bar{x})(y-\\bar{y})=65+36+2+4+18+85=210$、$\\sum(x-\\bar{x})^2=25+9+1+1+9+25=70$。$a=\\dfrac{210}{70}=3$、$b=41-3\\times27=-40$。<br>"
       + fig_scatter(RX, RY, (20, 34), (20, 60), 2, 10, "最高気温 x（℃）", "販売数 y（個）", line=(3, -40)) +
       "（3）$3\\times31-40=53$（個）。<br>"
       "（4）回帰直線は、データのある範囲での傾向を表すもの。40℃では、暑すぎて客足が減るなど、別の要因が強くはたらく可能性がある。<br>"
       "<b>ポイント</b>：回帰直線は $(\\bar{x},\\ \\bar{y})$ を通る。傾きは「$x$ が1増えると $y$ が平均的にどれだけ増えるか」を表す。データの範囲外への予測は慎重に。"},

 {"lv": "B", "tag": "クロス集計",
  "q": "ある高校の生徒200人に、朝食を毎日食べるかどうかと、1時間目の授業中に眠いと感じることが多いかどうかを尋ね、クロス集計表にまとめた。"
       + TB(["", "眠いと感じる", "感じない", "計"],
            [["毎日食べる", CROSS[0][0], CROSS[0][1], sum(CROSS[0])], ["毎日は食べない", CROSS[1][0], CROSS[1][1], sum(CROSS[1])],
             ["計", CROSS[0][0] + CROSS[1][0], CROSS[0][1] + CROSS[1][1], 200]]) +
       "（1）朝食を毎日食べる生徒のうち、眠いと感じる生徒の割合を百分率で求めよ。毎日は食べない生徒についても求めよ。<br>"
       "（2）眠いと感じる生徒のうち、朝食を毎日は食べない生徒の割合を百分率で求めよ。<br>"
       "（3）この表から「朝食を食べないことが、授業中の眠気の原因である」と結論づけてよいか。理由とともに答えよ。",
  "a": "（1）毎日食べる 30%、毎日は食べない 55%　（2）55%　（3）結論づけられない。関連があることは分かるが、睡眠時間など別の要因が両方に影響している可能性があり、因果関係は示されていないから",
  "s": "（1）$\\dfrac{36}{120}=0.30$ で30%、$\\dfrac{44}{80}=0.55$ で55%。毎日は食べない生徒のほうが、眠いと感じる割合が高い。<br>"
       "（2）眠いと感じる生徒は80人で、そのうち毎日は食べない生徒は44人。$\\dfrac{44}{80}=0.55$ で55%。（1）の「毎日は食べない生徒のうち眠い生徒」（$\\dfrac{44}{80}$）と分母の意味が違うが、ここではたまたま分母がどちらも80人なので同じ値になる。<br>"
       "（3）たとえば「夜ふかしをする」ことが、朝食を食べないことと眠気の両方の原因になっているかもしれない。原因と結果の関係を確かめるには、ほかの条件をそろえた調査や実験が必要。<br>"
       "<b>ポイント</b>：クロス集計では「何を分母にした割合か」を必ず確認する。人数の比較ではなく、グループごとの割合で比べる。"},

 {"lv": "B", "tag": "仮説検定の考え方",
  "q": "あるコインを20回投げたところ、表が15回出た。このコインは表が出やすいといえるかを調べるため、「表と裏はどちらも確率0.5で出る」と仮定し、その仮定のもとで「20回投げて表の回数を数える」ことを、コンピュータで1000セットシミュレーションした。表の回数ごとのセット数は次のとおりであった。"
       + TB(["表の回数", *COIN_LAB], [["セット数", *COIN]]) +
       "（1）表が15回以上出たセットの割合を求めよ。<br>"
       "（2）「仮定のもとで、実際に起きたこと以上に極端なことが起こる割合が5%未満なら、仮定は正しくなかったと判断する」という基準で考えるとき、このコインは表が出やすいと判断できるか。<br>"
       "（3）表が14回だった場合はどう判断されるか。<br>"
       "（4）（2）で「表が出やすい」と判断したとき、その判断が誤っている可能性はあるか。",
  "a": "（1）2.2%　（2）判断できる（2.2% は5%未満）　（3）14回以上は5.6%で5%以上なので、表が出やすいとは判断できない　（4）ある（確率0.5のコインでも、まれに15回以上出ることがある）",
  "s": "（1）$\\dfrac{22}{1000}=0.022$ で2.2%。<br>"
       "（2）仮定が正しければ、表が15回以上出ることは約2.2%しか起こらない、めったにないこと。それが実際に起きたので、仮定（確率0.5）は正しくなかった、つまり表が出やすいと判断する。<br>"
       "（3）14回以上は $\\dfrac{34+22}{1000}=0.056$ で5.6%。5%以上なので、偶然でも起こりうる範囲と考え、表が出やすいとは判断しない（「確率0.5である」と証明されたわけでもない）。<br>"
       "（4）ある。確率0.5のコインでも、およそ2%の確率で15回以上表が出る。基準の5%は、こうした誤りを許す割合の目安である。<br>"
       "なお、確率の計算で求めると、15回以上となる確率は $\\dfrac{_{20}\\mathrm{C}_{15}+\\cdots+{}_{20}\\mathrm{C}_{20}}{2^{20}}=\\dfrac{21700}{1048576}\\fallingdotseq0.021$、14回以上は約0.058 で、シミュレーションの結果とほぼ一致する。<br>"
       "<b>ポイント</b>：仮説検定は「仮定のもとでは起こりにくいことが起きた → 仮定を疑う」という考え方。判断できないことは、仮定が正しいことの証明にはならない。"},

 {"lv": "C", "tag": "共通テスト型",
  "q": B("生徒：11人の1日の読書時間（分）を調べ、四分位数を求めるプログラムを作っています。<br>"
         "先生：配列の一部分の中央値を求める関数を作ると便利ですね。添字 hidari から migi までの要素の中央値を返す関数にしましょう。<br>"
         "生徒：データの個数が偶数でも奇数でも正しく求められるようにしたいです。")
       + QDEF + "次のプログラムで、配列 Data は小さい順に並んでいる。÷ は商の整数部分、% は余りを求める演算である。" + FN_NOTE() + CODE(P_Q) +
       "（1）空欄 " + K("ア") + "〜" + K("ウ") + " に入るものを、次のうちからそれぞれ一つずつ選べ。ただし、" + K("イ") + "・" + K("ウ") + " は n が偶数でも奇数でも正しく求められるものとする。<br>"
       + K("ア") + "：① (Data[naka] + Data[naka + 1]) / 2　　② (Data[naka - 1] + Data[naka]) / 2<br>　　③ Data[naka] / 2　　④ (Data[hidari] + Data[migi]) / 2<br>"
       + K("イ") + "・" + K("ウ") + "：① n ÷ 2　② n ÷ 2 - 1　③ (n + 1) ÷ 2　④ (n - 1) ÷ 2　⑤ n ÷ 2 + 1<br>"
       "（2）空欄を正しく埋めて実行したときに表示される3つの値を答えよ。<br>"
       "（3）このデータの箱ひげ図として正しいものを、次の①〜③のうちから一つ選べ。" + fig_boxes(BOX_OPT, 0, 160, 20, "分") +
       "（4）「第1四分位数 − 1.5 × 四分位範囲」より小さい値、または「第3四分位数 ＋ 1.5 × 四分位範囲」より大きい値を外れ値とする。このデータの外れ値をすべて答えよ。<br>"
       "（5）（4）の外れ値を除いて (08)行目の配列を10個のデータにして実行したとき、表示される3つの値を答えよ。また、外れ値を除く前後で、平均値はどのように変わるか。",
  "a": "（1）ア ①　イ ②　ウ ③　（2）30、45、60　（3）③　（4）150　（5）30、42.5、55。平均値は約51.8分から42分に下がる",
  "s": "（1）kosu が偶数のとき、naka = (hidari + migi) ÷ 2 は中央の2つのうち左側の添字なので、中央値は (Data[naka] + Data[naka + 1]) / 2（ア ①）。"
       "下半分の右端は、n = 11 なら添字4、n = 10 でも添字4。n ÷ 2 - 1 はどちらも4になる（イ ②）。④ (n - 1) ÷ 2 は n = 11 のとき5で、中央値を含んでしまう。"
       "上半分の左端は、n = 11 なら添字6、n = 10 なら添字5。(n + 1) ÷ 2 は6と5になる（ウ ③）。⑤ n ÷ 2 + 1 は n = 10 のとき6となり誤り、① n ÷ 2 は n = 11 のとき5で中央値を含む。<br>"
       "（2）q2 = chuoti(Data, 0, 10) は個数11で Data[5] = 45。q1 = chuoti(Data, 0, 4) は Data[2] = 30。q3 = chuoti(Data, 6, 10) は Data[8] = 60。<br>"
       "（3）最小値10、第1四分位数30、中央値45、第3四分位数60、最大値150 なので③。①は中央値を両側に含めて四分位数を求めたもの（32.5、57.5）、②は中央値が誤り。<br>"
       "（4）四分位範囲は $60-30=30$。$30-1.5\\times30=-15$、$60+1.5\\times30=105$ なので、105より大きい150が外れ値。<br>"
       "（5）10個 [10, 25, 30, 35, 40, 45, 50, 55, 60, 70] では、q2 = (40 + 45) / 2 = 42.5、q1 = chuoti(Data, 0, 4) = 30、q3 = chuoti(Data, 5, 9) = 55。"
       "平均値は $\\dfrac{570}{11}\\fallingdotseq51.8$ 分から $\\dfrac{420}{10}=42$ 分へ大きく下がる。中央値は45分から42.5分で、変化が小さい。<br>"
       "<b>ポイント</b>：添字の範囲を式で書く空欄は、<b>偶数個と奇数個の両方</b>で具体的に代入して確かめる。外れ値の判定は四分位範囲を使うので、外れ値そのものの影響を受けにくい。"},

 {"lv": "C", "tag": "共通テスト型",
  "q": B("生徒：8人の1週間の学習時間 $x$（時間）と、小テストの得点 $y$（点）の相関係数を求めるプログラムを作りました。<br>"
         "先生：散布図もかいてみましょう。1人だけ、ほかと離れた位置にいる人がいますね。<br>"
         "生徒：H さんは、テストの日に体調をくずしていたそうです。")
       + '<div class="two"><div>' + fig_scatter(SX, SY, (0, 11), (40, 100), 1, 10, "学習時間 x（時間）", "得点 y（点）", labels=SLAB, W=300, Hh=228)
       + "</div><div>" + TB(["生徒", "$x$", "$y$"], [[a, b, c] for a, b, c in zip(SLAB, SX, SY)]) + "</div></div>" + CODE(P_R) +
       "（1）空欄 " + K("ア") + "・" + K("イ") + " に入るものを、次のうちからそれぞれ一つずつ選べ。** はべき乗を表す。<br>"
       + K("ア") + "：① (X[i] - mx) * (Y[i] - my)　　② (X[i] - mx) ** 2 * (Y[i] - my) ** 2<br>　　③ X[i] * Y[i]　　④ (X[i] * Y[i] - mx * my) ** 2<br>"
       + K("イ") + "：① sxy / (sxx * syy)　② sxy / (sxx * syy) ** 0.5　③ sxy / n　④ (sxy / n) ** 0.5<br>"
       "（2）空欄を正しく埋めて実行したとき、繰り返しが終わった時点での sxx、syy、sxy の値を求めよ。また、表示される r の値を小数第3位を四捨五入して答えよ。必要なら $\\sqrt{125568}\\fallingdotseq354.4$ を用いてよい。<br>"
       "（3）H さんのデータを除いた7人で同じプログラムを実行した。表示される値に最も近いものを、次の①〜④のうちから一つ選べ。<br>"
       "① −0.38　② 0.38　③ 0.66　④ 0.97<br>"
       "（4）この分析からいえることとして最も適当なものを、次の①〜③のうちから一つ選べ。<br>"
       "① 8人の相関係数が小さいので、学習時間と得点の間には関係がないと結論できる。<br>"
       "② 相関係数は外れ値の影響を大きく受けるので、散布図で外れた点を確認し、その理由も考えて分析する必要がある。<br>"
       "③ 7人では強い正の相関があるので、学習時間を2倍にすれば、どの生徒も得点が2倍になる。",
  "a": "（1）ア ①　イ ②　（2）sxx = 72、syy = 1744、sxy = 136、r ≒ 0.38　（3）④　（4）②",
  "s": "（1）相関係数は $r=\\dfrac{\\sum(x-\\bar{x})(y-\\bar{y})}{\\sqrt{\\sum(x-\\bar{x})^2}\\sqrt{\\sum(y-\\bar{y})^2}}$。sxy には偏差の積を足していき（ア ①）、r = sxy / (sxx * syy) ** 0.5（イ ②、0.5乗は平方根）。<br>"
       "（2）平均は $\\bar{x}=\\dfrac{48}{8}=6$、$\\bar{y}=\\dfrac{584}{8}=73$。<br>"
       + TB(["生徒", *SLAB, "合計"],
            [["$x-\\bar{x}$", *[x - 6 for x in SX], ""], ["$y-\\bar{y}$", *[y - 73 for y in SY], ""],
             ["$(x-\\bar{x})^2$", *[(x - 6) ** 2 for x in SX], 72], ["$(y-\\bar{y})^2$", *[(y - 73) ** 2 for y in SY], 1744],
             ["積", *[(x - 6) * (y - 73) for x, y in zip(SX, SY)], 136]]) +
       "$r=\\dfrac{136}{\\sqrt{72\\times1744}}=\\dfrac{136}{\\sqrt{125568}}\\fallingdotseq\\dfrac{136}{354.4}\\fallingdotseq0.38$。<br>"
       "（3）H さんを除くと、残りの7人は散布図でほぼ右上がりの直線の近くに並ぶ。H さんの偏差の積 $4\\times(-23)=-92$ が sxy を大きく減らしていたので、除くと相関係数は1に近い大きな値になる（計算すると約0.97）。④。<br>"
       "（4）①：8人の r が小さいのは H さん1人の影響で、関係がないとはいえない。③：相関係数は直線的な関係の強さを表すだけで、「2倍にすれば2倍」という比例関係や、因果関係を示すものではない。②が適当。ただし、外れ値は理由があるときに除くのであり、都合のよい結果を得るために除いてはいけない。<br>"
       "<b>ポイント</b>：相関係数を計算する前に必ず散布図をかく。少数の外れ値で相関係数は大きく変わる。外れ値を除くかどうかは、その理由（測定の誤り、条件の違いなど）を確かめて決める。"},
]}}

# ---------------- 検算 ----------------


def _check(ch):
    items = ch["items"]
    lv = [it["lv"] for it in items]
    assert lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2, lv
    assert lv == sorted(lv), lv
    for it in items:
        for k in ("tag", "q", "a", "s"):
            assert it.get(k), (k, it.get("q", "")[:40])
        assert "<b>ポイント</b>：" in it["s"], it["q"][:40]
        for k in ("q", "a", "s"):
            s = it[k]
            assert "$$" not in s and s.count("$") % 2 == 0, s[:60]
            for t in ("div", "pre", "table", "tr", "td", "th", "b", "span", "svg", "u", "code"):
                o = len(re.findall(rf"<{t}[\s>]", s))
                c = s.count(f"</{t}>")
                assert o == c, (t, o, c, s[:60])
            plain = re.sub(r"\$[^$]*\$", "", s)
            plain = re.sub(r"<svg.*?</svg>", "", plain, flags=re.S)
            plain = re.sub(r"<[^<>]+>", "", plain)
            assert "<" not in plain and ">" not in plain, plain[:80]
            assert not re.search(r"&(?!(lt|gt|amp|nbsp);)", plain), plain[:80]
            assert "【" not in s and "】" not in s, s[:60]


def verify():
    _check(CH[12])
    # 12-1
    assert mean(D1) == 6 and med(D1) == 5 and max(set(D1), key=D1.count) == 5 and D1.count(5) == 3
    assert sorted(D1) == [3, 4, 5, 5, 5, 7, 8, 8, 9]
    # 12-2
    assert mean(D2) == 5 and var(D2) == 8
    E = [2 * x + 3 for x in D2]
    assert E == [13, 21, 5, 17, 9] and mean(E) == 13 and var(E) == 32
    assert round(math.sqrt(8), 2) == 2.83 and round(math.sqrt(32), 2) == 5.66
    # 12-3
    assert quartiles(D3) == (18, Fr(47, 2), 30) and min(D3) == 12 and max(D3) == 41
    assert quartiles(D3 + [45]) == (18, 25, 34)
    # 12-4 ②の例：放物線上の点は相関係数0
    xs = [-2, -1, 0, 1, 2]
    assert corr_parts(xs, [x * x for x in xs])[2] == 0
    # 12-5 箱ひげ図
    iqr = {lab: v[3] - v[1] for lab, v in BOX3}
    rng_ = {lab: v[4] - v[0] for lab, v in BOX3}
    assert iqr == {"A組": 25, "B組": 18, "C組": 37} and max(iqr, key=iqr.get) == "C組"
    assert rng_ == {"A組": 70, "B組": 55, "C組": 83} and min(rng_, key=rng_.get) == "B組"

    def five(v):
        q1, q2, q3 = quartiles(v)
        return (min(v), q1, q2, q3, max(v))

    def build(mn, a10, a11, a20, a21, a30, a31, mx):
        """40人の例を作る（x1=mn, x10, x11, x20, x21, x30, x31, x40=mx を指定し、間を単調に埋める）"""
        v = [mn] + [a10] * 8 + [a10, a11] + [a11] * 8 + [a20, a21] + [a21] * 8 + [a30, a31] + [a31] * 8 + [mx]
        assert len(v) == 40 and v == sorted(v)
        return v
    c1 = build(15, 37, 39, 51, 53, 74, 76, 98)
    assert five(c1) == (15, 38, 52, 75, 98) and sum(1 for x in c1 if x >= 75) == 10
    c2 = build(15, 37, 39, 51, 53, 75, 75, 98)
    assert five(c2) == (15, 38, 52, 75, 98) and sum(1 for x in c2 if x >= 75) >= 11
    a1 = build(22, 44, 46, 57, 59, 69, 71, 92)
    assert five(a1) == (22, 45, 58, 70, 92) and sum(1 for x in a1 if x <= 45) == 10
    for v in (c1, c2, a1):         # どの例でも x10 <= Q1, x31 >= Q3
        q1, _, q3 = quartiles(v)
        assert v[9] <= q1 and v[30] >= q3
    # 12-6 相関係数
    sxx, syy, sxy = corr_parts(CX, CY)
    assert (mean(CX), mean(CY), sxx, syy, sxy) == (6, 6, 40, 34, 34) and sxy / 5 == Fr(34, 5)
    assert round(corr(CX, CY), 2) == 0.92 and round(math.sqrt(1360), 2) == 36.88 and round(34 / 36.88, 2) == 0.92
    X60 = [60 * x for x in CX]
    assert corr_parts(X60, CY)[2] / 5 == 408 and abs(corr(X60, CY) - corr(CX, CY)) < 1e-12
    # 12-7 回帰直線
    sxx, syy, sxy = corr_parts(RX, RY)
    assert mean(RX) == 27 and mean(RY) == 41 and sum(RX) == 162 and sum(RY) == 246 and (sxx, sxy) == (70, 210)
    a = sxy / sxx
    b = mean(RY) - a * mean(RX)
    assert (a, b) == (3, -40) and a * 31 + b == 53
    assert [x - 27 for x in RX] == [-5, -3, -1, 1, 3, 5] and [y - 41 for y in RY] == [-13, -12, -2, 4, 6, 17]
    # 12-8 クロス集計
    assert Fr(CROSS[0][0], sum(CROSS[0])) == Fr(30, 100) and Fr(CROSS[1][0], sum(CROSS[1])) == Fr(55, 100)
    assert CROSS[0][0] + CROSS[1][0] == 80 and Fr(CROSS[1][0], 80) == Fr(55, 100) and sum(map(sum, CROSS)) == 200
    # 12-9 仮説検定（表は実際のシミュレーション結果）
    cnt = coin_sim()
    grouped = [sum(cnt[:6])] + cnt[6:15] + [sum(cnt[15:])]
    assert grouped == COIN and sum(COIN) == NSET
    assert Fr(COIN[-1], NSET) == Fr(22, 1000) and Fr(COIN[-1] + COIN[-2], NSET) == Fr(56, 1000)
    p15 = Fr(sum(comb(20, k) for k in range(15, 21)), 2 ** 20)
    p14 = Fr(sum(comb(20, k) for k in range(14, 21)), 2 ** 20)
    assert p15 == Fr(21700, 1048576) and round(float(p15), 3) == 0.021 and round(float(p14), 3) == 0.058
    # 12-10 四分位数のプログラム
    def chuoti(D, h, m, a=1):
        kosu = m - h + 1
        naka = (h + m) // 2
        if kosu % 2 == 1:
            return Fr(D[naka])
        return {1: lambda: Fr(D[naka] + D[naka + 1], 2), 2: lambda: Fr(D[naka - 1] + D[naka], 2),
                3: lambda: Fr(D[naka], 2), 4: lambda: Fr(D[h] + D[m], 2)}[a]()
    opt = {1: lambda n: n // 2, 2: lambda n: n // 2 - 1, 3: lambda n: (n + 1) // 2, 4: lambda n: (n - 1) // 2, 5: lambda n: n // 2 + 1}

    def prog(D, a=1, i_=2, u=3):
        n = len(D)
        return chuoti(D, 0, opt[i_](n), a), chuoti(D, 0, n - 1, a), chuoti(D, opt[u](n), n - 1, a)
    assert prog(DOKU) == (30, 45, 60) == quartiles(DOKU)
    D10 = DOKU[:-1]
    assert prog(D10) == (30, Fr(85, 2), 55) == quartiles(D10)
    tests = [DOKU, D10] + [sorted(random.Random(s).sample(range(200), n)) for s in range(30) for n in (6, 7, 8, 9, 12, 13)]
    good = [(a, i_, u) for a in range(1, 5) for i_ in range(1, 6) for u in range(1, 6)
            if all(prog(D, a, i_, u) == quartiles(D) for D in tests)]
    assert good == [(1, 2, 3)], good
    q1, q2, q3 = quartiles(DOKU)
    lo_f, hi_f = q1 - Fr(3, 2) * (q3 - q1), q3 + Fr(3, 2) * (q3 - q1)
    assert (lo_f, hi_f) == (-15, 105) and [x for x in DOKU if x < lo_f or x > hi_f] == [150]
    assert BOX_OPT[2][1] == (min(DOKU), *quartiles(DOKU), max(DOKU))
    assert quartiles(DOKU)[0] != BOX_OPT[0][1][1] and med(DOKU) != BOX_OPT[1][1][2]
    inc_lo, inc_hi = med(DOKU[:6]), med(DOKU[5:])   # 中央値を含めて分けた場合
    assert (inc_lo, inc_hi) == (Fr(65, 2), Fr(115, 2))
    assert sum(DOKU) == 570 and round(570 / 11, 1) == 51.8 and mean(D10) == 42
    # 12-11 相関係数のプログラム
    sxx, syy, sxy = corr_parts(SX, SY)
    assert (mean(SX), mean(SY), sxx, syy, sxy) == (6, 73, 72, 1744, 136) and 72 * 1744 == 125568
    assert round(math.sqrt(125568), 1) == 354.4 and round(corr(SX, SY), 2) == 0.38 and round(136 / 354.4, 2) == 0.38
    r7 = corr(SX[:7], SY[:7])
    assert round(r7, 2) == 0.97 and min(abs(r7 - v) for v in (-0.38, 0.38, 0.66)) > 0.3
    assert (SX[7] - 6) * (SY[7] - 73) == -92
    # 選択肢の確認：ア①・イ② の組だけが相関係数（−1〜1、0.38）になる
    mx, my = mean(SX), mean(SY)
    A_opts = {1: lambda x, y: (x - mx) * (y - my), 2: lambda x, y: (x - mx) ** 2 * (y - my) ** 2,
              3: lambda x, y: x * y, 4: lambda x, y: (x * y - mx * my) ** 2}
    I_opts = {1: lambda a_, b_, c_: float(c_) / float(a_ * b_), 2: lambda a_, b_, c_: float(c_) / math.sqrt(a_ * b_),
              3: lambda a_, b_, c_: float(c_) / 8, 4: lambda a_, b_, c_: math.sqrt(abs(float(c_) / 8))}
    hits = [(i, j) for i in A_opts for j in I_opts
            if round(I_opts[j](sxx, syy, sum(A_opts[i](x, y) for x, y in zip(SX, SY))), 2) == 0.38]
    assert hits == [(1, 2)], hits


if __name__ == "__main__":
    verify()
    print("ok", len(CH[12]["items"]))
