"""第11章 図形と方程式（数学II）。図はすべて Python で座標を計算して SVG にする。"""
import math, random
from fractions import Fraction as Fr
from sympy import symbols, expand, simplify, sqrt, Rational as R, solve, factor, nsimplify

SEC = []
_V = []          # 節ごとの検算関数
_FIG = [0]

# ---------------------------------------------------------------- 図の道具
_COL = {"b": "#16367a", "r": "#c0392b", "g": "#888888", "k": "#333333"}


def _st(s):
    c = _COL[s[0]]
    w = 0.8 if s[0] == "g" else 1.3
    d = ' stroke-dasharray="4,3"' if "d" in s[1:] else ""
    return f'fill="none" stroke="{c}" stroke-width="{w}"{d}'


def _arc(cx, cy, r, a0, a1, n=80):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _fp(f, a, b, n=80):
    return [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]


def _fig(xr, yr, items, W=200, sy=None, axes=True, lab=("x", "y"), O=True):
    _FIG[0] += 1
    cid = f"c11f{_FIG[0]}"
    x0, x1 = xr
    y0, y1 = yr
    m = 12
    sx = (W - 2 * m) / (x1 - x0)
    sy = sx if sy is None else sy
    H = round(sy * (y1 - y0) + 2 * m)
    X = lambda x: m + (x - x0) * sx
    Y = lambda y: m + (y1 - y) * sy
    P = lambda p: f"{X(p[0]):.1f},{Y(p[1]):.1f}"
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Times New Roman,serif" font-size="11">',
         f'<defs><clipPath id="{cid}"><rect x="{m}" y="{m}" width="{W - 2 * m}" height="{H - 2 * m}"/></clipPath></defs>']
    if axes:
        if y0 <= 0 <= y1:
            o.append(f'<line x1="{m - 6}" y1="{Y(0):.1f}" x2="{W - 3}" y2="{Y(0):.1f}" stroke="#666" stroke-width="0.8"/>')
            o.append(f'<text x="{W - 9}" y="{Y(0) + 11:.1f}" font-style="italic">{lab[0]}</text>')
        if x0 <= 0 <= x1:
            o.append(f'<line x1="{X(0):.1f}" y1="{H - m + 6}" x2="{X(0):.1f}" y2="3" stroke="#666" stroke-width="0.8"/>')
            o.append(f'<text x="{X(0) + 4:.1f}" y="10" font-style="italic">{lab[1]}</text>')
        if O and x0 <= 0 <= x1 and y0 <= 0 <= y1:
            o.append(f'<text x="{X(0) - 10:.1f}" y="{Y(0) + 11:.1f}">O</text>')
    cl, top = [], []
    for it in items:
        k = it[0]
        if k == "fill":
            d = " ".join("M" + " L".join(P(p) for p in poly) + "Z" for poly in it[1])
            col = it[2] if len(it) > 2 else "#3d6fd1"
            cl.append(f'<path d="{d}" fill="{col}" fill-opacity="0.28" fill-rule="evenodd" stroke="none"/>')
        elif k == "pl":
            cl.append(f'<polyline points="{" ".join(P(p) for p in it[1])}" {_st(it[2] if len(it) > 2 else "b")}/>')
        elif k == "fn":
            cl.append(f'<polyline points="{" ".join(P(p) for p in _fp(it[1], it[2], it[3]))}" {_st(it[4] if len(it) > 4 else "b")}/>')
        elif k == "seg":
            cl.append(f'<line x1="{X(it[1][0]):.1f}" y1="{Y(it[1][1]):.1f}" x2="{X(it[2][0]):.1f}" y2="{Y(it[2][1]):.1f}" {_st(it[3] if len(it) > 3 else "b")}/>')
        elif k == "line":      # a x + b y + c = 0
            a, b, c = it[1], it[2], it[3]
            if abs(b) > 1e-12:
                p, q = (x0 - 1, -(a * (x0 - 1) + c) / b), (x1 + 1, -(a * (x1 + 1) + c) / b)
            else:
                p, q = (-c / a, y0 - 1), (-c / a, y1 + 1)
            cl.append(f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" y2="{Y(q[1]):.1f}" {_st(it[4] if len(it) > 4 else "b")}/>')
        elif k == "circ":
            (cx, cy), r = it[1], it[2]
            cl.append(f'<ellipse cx="{X(cx):.1f}" cy="{Y(cy):.1f}" rx="{r * sx:.1f}" ry="{r * sy:.1f}" {_st(it[3] if len(it) > 3 else "b")}/>')
        elif k == "dot":
            p, s = it[1], it[2]
            dx, dy = it[3] if len(it) > 3 else (3, -3)
            hol = len(it) > 4 and it[4]
            fill = "#fff" if hol else "#222"
            top.append(f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="1.9" fill="{fill}" stroke="#222" stroke-width="0.8"/>')
            if s:
                top.append(f'<text x="{X(p[0]) + dx:.1f}" y="{Y(p[1]) + dy:.1f}">{s}</text>')
        elif k == "txt":
            p, s = it[1], it[2]
            dx, dy = it[3] if len(it) > 3 else (0, 0)
            sty = ' font-style="italic"' if len(it) > 4 and it[4] else ""
            top.append(f'<text x="{X(p[0]) + dx:.1f}" y="{Y(p[1]) + dy:.1f}"{sty}>{s}</text>')
    o.append(f'<g clip-path="url(#{cid})">' + "".join(cl) + "</g>")
    o += top
    o.append("</svg>")
    return "".join(o)


def _close(a, b, eps=1e-9):
    return abs(a - b) < eps


# ---------------------------------------------------------------- 節1
SEC.append({"title": "点の座標",
"base": r"""・2点 $\mathrm{A}(x_1,\ y_1)$，$\mathrm{B}(x_2,\ y_2)$ 間の距離：$\mathrm{AB}=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$<br>
・線分 AB を $m:n$ に内分する点：$\left(\dfrac{nx_1+mx_2}{m+n},\ \dfrac{ny_1+my_2}{m+n}\right)$，外分する点：$\left(\dfrac{-nx_1+mx_2}{m-n},\ \dfrac{-ny_1+my_2}{m-n}\right)$<br>
・3点 A，B，C を頂点とする三角形の重心：$\left(\dfrac{x_1+x_2+x_3}{3},\ \dfrac{y_1+y_2+y_3}{3}\right)$<br>
・図形の性質の証明では、計算が簡単になるように座標軸を設定する（対称軸や辺を座標軸に重ねる）。""",
"items": [
 {"lv": 1, "title": "2点間の距離・内分点・外分点",
  "q": r"2点 $\mathrm{A}(-2,\ 5)$，$\mathrm{B}(4,\ -1)$ について、次のものを求めよ。<br>(1) 線分 AB の長さ　(2) 線分 AB を $2:1$ に内分する点 P　(3) 線分 AB を $2:1$ に外分する点 Q　(4) 線分 AB の中点 M",
  "hint": r"公式に代入するだけだが、内分と外分の違いは「$n$ を $-n$ に変える」だけと覚えておくと混乱しない。",
  "sol": r"(1) $\mathrm{AB}=\sqrt{\{4-(-2)\}^2+(-1-5)^2}=\sqrt{36+36}=\boldsymbol{6\sqrt2}$<br>"
         r"(2) $\mathrm{P}\left(\dfrac{1\cdot(-2)+2\cdot4}{2+1},\ \dfrac{1\cdot5+2\cdot(-1)}{2+1}\right)=\boldsymbol{(2,\ 1)}$<br>"
         r"(3) $\mathrm{Q}\left(\dfrac{-1\cdot(-2)+2\cdot4}{2-1},\ \dfrac{-1\cdot5+2\cdot(-1)}{2-1}\right)=\boldsymbol{(10,\ -7)}$<br>"
         r"(4) $\mathrm{M}\left(\dfrac{-2+4}{2},\ \dfrac{5+(-1)}{2}\right)=\boldsymbol{(1,\ 2)}$",
  "note": r"外分点 Q は「A から B の方向へ、AB の長さの2倍だけ進んだ点」である。実際 $\mathrm{Q}=\mathrm{A}+2(\mathrm{B}-\mathrm{A})$ の各成分を計算しても $(10,\ -7)$ になる。",
  "ex": r"2点 $\mathrm{A}(3,\ -4)$，$\mathrm{B}(-1,\ 2)$ について、線分 AB の長さ、$1:3$ に内分する点、$1:3$ に外分する点を求めよ。",
  "exa": r"$\mathrm{AB}=2\sqrt{13}$，内分点 $\left(2,\ -\dfrac52\right)$，外分点 $(5,\ -7)$"},
 {"lv": 1, "title": "三角形の重心・平行四辺形の頂点",
  "q": r"3点 $\mathrm{A}(1,\ 4)$，$\mathrm{B}(-3,\ -2)$，$\mathrm{C}(5,\ 1)$ がある。<br>(1) $\triangle\mathrm{ABC}$ の重心 G の座標を求めよ。<br>(2) 四角形 ABCD が平行四辺形となるような点 D の座標を求めよ。<br>(3) 4点 A，B，C，D が平行四辺形の4つの頂点となるような点 D の座標をすべて求めよ。",
  "hint": r"平行四辺形は「2本の対角線の中点が一致する」ことで式にする。(3) では、どの2点が対角線の両端になるかで3通りに分ける。",
  "sol": r"(1) $\mathrm{G}\left(\dfrac{1-3+5}{3},\ \dfrac{4-2+1}{3}\right)=\boldsymbol{(1,\ 1)}$<br>"
         r"(2) $\mathrm{D}(x,\ y)$ とする。対角線 AC と BD の中点が一致するから<br>　$\dfrac{1+5}{2}=\dfrac{-3+x}{2}$，$\dfrac{4+1}{2}=\dfrac{-2+y}{2}$　より　$\boldsymbol{\mathrm{D}(9,\ 7)}$<br>"
         r"(3) 対角線が AC と BD のとき (2) の $(9,\ 7)$。<br>"
         r"対角線が AB と CD のとき、$1+(-3)=5+x$，$4+(-2)=1+y$ より $(-7,\ 1)$。<br>"
         r"対角線が BC と AD のとき、$-3+5=1+x$，$-2+1=4+y$ より $(1,\ -5)$。<br>"
         r"よって　$\boldsymbol{\mathrm{D}(9,\ 7),\ (-7,\ 1),\ (1,\ -5)}$",
  "note": r"「四角形 ABCD」と頂点の順序が指定されれば D は1つ、「4点が平行四辺形の頂点」なら3つある。問題文の言い回しに注意する。",
  "ex": r"3点 $\mathrm{A}(2,\ 3)$，$\mathrm{B}(-1,\ 1)$，$\mathrm{C}(4,\ -2)$ について、$\triangle\mathrm{ABC}$ の重心と、4点 A，B，C，D が平行四辺形の頂点となる点 D をすべて求めよ。",
  "exa": r"重心 $\left(\dfrac53,\ \dfrac23\right)$，$\mathrm{D}(7,\ 0),\ (-3,\ 6),\ (1,\ -4)$"},
 {"lv": 2, "title": "座標を用いた証明（中線定理）",
  "q": r"$\triangle\mathrm{ABC}$ の辺 BC の中点を M とするとき、次の等式が成り立つことを証明せよ。<br>　$\mathrm{AB}^2+\mathrm{AC}^2=2(\mathrm{AM}^2+\mathrm{BM}^2)$",
  "hint": r"M を原点、直線 BC を $x$ 軸にとると、B，C の座標が $(\pm c,\ 0)$ と対称になり計算が最も簡単になる。",
  "sol": r"直線 BC を $x$ 軸、M を原点とする座標をとり、$\mathrm{B}(-c,\ 0)$，$\mathrm{C}(c,\ 0)$ $(c\gt0)$，$\mathrm{A}(a,\ b)$ とおく。<br>"
         r"$\mathrm{AB}^2+\mathrm{AC}^2=\{(a+c)^2+b^2\}+\{(a-c)^2+b^2\}=2(a^2+b^2+c^2)$<br>"
         r"$\mathrm{AM}^2+\mathrm{BM}^2=(a^2+b^2)+c^2$<br>"
         r"よって　$\mathrm{AB}^2+\mathrm{AC}^2=2(\mathrm{AM}^2+\mathrm{BM}^2)$　$\blacksquare$",
  "note": r"座標の設定で一般性が失われないことが大切。どんな三角形も、辺 BC を $x$ 軸、その中点を原点に置くことができる。BC を $m:n$ に内分する点 D について一般化すると $n\mathrm{AB}^2+m\mathrm{AC}^2=(m+n)\mathrm{AD}^2+n\mathrm{BD}^2+m\mathrm{CD}^2$（スチュワートの定理）。",
  "ex": r"$\triangle\mathrm{ABC}$ の辺 BC を $1:2$ に内分する点を D とするとき、$2\mathrm{AB}^2+\mathrm{AC}^2=3\mathrm{AD}^2+6\mathrm{BD}^2$ を証明せよ。",
  "exa": r"D を原点、$\mathrm{B}(-d,\ 0)$，$\mathrm{C}(2d,\ 0)$，$\mathrm{A}(a,\ b)$ とおくと、両辺とも $3a^2+3b^2+6d^2$ になる。"},
]})


def _v1():
    def div(A, B, m, n):
        return tuple((n * a + m * b) / (m + n) for a, b in zip(A, B))
    A, B = (Fr(-2), Fr(5)), (Fr(4), Fr(-1))
    assert (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2 == 72
    assert div(A, B, 2, 1) == (2, 1) and div(A, B, 2, -1) == (10, -7) and div(A, B, 1, 1) == (1, 2)
    A, B = (Fr(3), Fr(-4)), (Fr(-1), Fr(2))
    assert (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2 == 52
    assert div(A, B, 1, 3) == (2, Fr(-5, 2)) and div(A, B, 1, -3) == (5, -7)
    for (A, B, C, G, Ds) in [((1, 4), (-3, -2), (5, 1), (1, 1), {(9, 7), (-7, 1), (1, -5)}),
                             ((2, 3), (-1, 1), (4, -2), (Fr(5, 3), Fr(2, 3)), {(7, 0), (-3, 6), (1, -4)})]:
        assert (Fr(A[0] + B[0] + C[0], 3), Fr(A[1] + B[1] + C[1], 3)) == G
        got = {(A[0] + C[0] - B[0], A[1] + C[1] - B[1]), (A[0] + B[0] - C[0], A[1] + B[1] - C[1]), (B[0] + C[0] - A[0], B[1] + C[1] - A[1])}
        assert got == Ds
    assert (9, 7) == (1 + 5 + 3, 4 + 1 + 2)
    a, b, c, d = symbols("a b c d", real=True)
    assert expand((a + c) ** 2 + b ** 2 + (a - c) ** 2 + b ** 2 - 2 * (a ** 2 + b ** 2 + c ** 2)) == 0
    assert expand(2 * ((a + d) ** 2 + b ** 2) + (a - 2 * d) ** 2 + b ** 2 - (3 * (a ** 2 + b ** 2) + 6 * d ** 2)) == 0


_V.append(_v1)


# ---------------------------------------------------------------- 節2
_F27 = _fig((-3, 7), (-1, 5), [
    ("line", 1, 1, -2, "g"), ("seg", (-2, 0), (6, 2), "rd"), ("seg", (2, 4), (1.2, 0.8), "b"), ("seg", (1.2, 0.8), (6, 2), "b"),
    ("seg", (2, 4), (-2, 0), "gd"),
    ("dot", (2, 4), "A", (4, -2)), ("dot", (6, 2), "B", (3, -5)), ("dot", (-2, 0), "A′", (-6, -6)), ("dot", (1.2, 0.8), "P", (4, 10)),
    ("txt", (3.3, -0.9), "ℓ", (4, 0), True)], W=190)

SEC.append({"title": "直線の方程式",
"base": r"""・点 $(x_1,\ y_1)$ を通り傾き $m$：$y-y_1=m(x-x_1)$。2点を通る直線：$(y_2-y_1)(x-x_1)-(x_2-x_1)(y-y_1)=0$<br>
・2直線 $a_1x+b_1y+c_1=0$，$a_2x+b_2y+c_2=0$ が　平行 $\Longleftrightarrow a_1b_2-a_2b_1=0$，垂直 $\Longleftrightarrow a_1a_2+b_1b_2=0$（傾きでは $m_1=m_2$，$m_1m_2=-1$）<br>
・点 $(x_1,\ y_1)$ と直線 $ax+by+c=0$ の距離：$\dfrac{|ax_1+by_1+c|}{\sqrt{a^2+b^2}}$<br>
・2直線 $f=0$，$g=0$ の交点を通る直線は $kf+g=0$（$f=0$ 自身を除く）。$k$ の恒等式とみれば定点を通る直線の問題になる。""",
"items": [
 {"lv": 1, "title": "直線の方程式（傾きと1点・2点・切片）",
  "q": r"次の直線の方程式を求めよ。<br>(1) 点 $(2,\ -3)$ を通り、傾きが $\dfrac32$　(2) 2点 $(-1,\ 4)$，$(3,\ -2)$ を通る<br>(3) 2点 $(3,\ 1)$，$(3,\ 5)$ を通る　(4) $x$ 切片が $4$，$y$ 切片が $-2$",
  "hint": r"傾きがわかれば $y-y_1=m(x-x_1)$。$x$ 座標が等しい2点を通る直線は傾きが定義できないので $x=k$ の形になる。",
  "sol": r"(1) $y+3=\dfrac32(x-2)$ より　$\boldsymbol{y=\dfrac32x-6}$<br>"
         r"(2) 傾きは $\dfrac{-2-4}{3-(-1)}=-\dfrac32$。$y-4=-\dfrac32(x+1)$ より　$\boldsymbol{y=-\dfrac32x+\dfrac52}$<br>"
         r"(3) 2点の $x$ 座標がともに $3$ であるから　$\boldsymbol{x=3}$<br>"
         r"(4) $\dfrac x4+\dfrac y{-2}=1$ より　$\boldsymbol{x-2y-4=0}$",
  "note": r"2点を通る直線を $(y_2-y_1)(x-x_1)-(x_2-x_1)(y-y_1)=0$ と書くと、(3) のような $x_1=x_2$ の場合も1つの式で扱える。",
  "ex": r"次の直線の方程式を求めよ。(1) 点 $(-1,\ 2)$ を通り傾き $-2$　(2) 2点 $(2,\ 5)$，$(-4,\ -1)$ を通る　(3) 2点 $(-2,\ 1)$，$(4,\ 1)$ を通る　(4) $x$ 切片 $-3$，$y$ 切片 $6$",
  "exa": r"(1) $y=-2x$　(2) $y=x+3$　(3) $y=1$　(4) $2x-y+6=0$"},
 {"lv": 1, "title": "平行な直線・垂直な直線・垂線の足",
  "q": r"点 $\mathrm{A}(3,\ -1)$ と直線 $\ell:\ 2x-3y+1=0$ がある。<br>(1) A を通り $\ell$ に平行な直線　(2) A を通り $\ell$ に垂直な直線　(3) A から $\ell$ に下ろした垂線の足 H の座標　を求めよ。",
  "hint": r"$\ell$ の傾きは $\dfrac23$。垂直な直線の傾きは $m_1m_2=-1$ から $-\dfrac32$。垂線の足は「$\ell$ と (2) の直線の交点」。",
  "sol": r"$\ell$ は $y=\dfrac23x+\dfrac13$ で、傾きは $\dfrac23$。<br>"
         r"(1) $y+1=\dfrac23(x-3)$ より　$\boldsymbol{2x-3y-9=0}$<br>"
         r"(2) 傾きは $-\dfrac32$。$y+1=-\dfrac32(x-3)$ より　$\boldsymbol{3x+2y-7=0}$<br>"
         r"(3) H は $2x-3y+1=0$ と $3x+2y-7=0$ の交点。第1式 $\times2$ と第2式 $\times3$ を加えて $13x-19=0$，$x=\dfrac{19}{13}$，$y=\dfrac{2x+1}3=\dfrac{17}{13}$。　$\boldsymbol{\mathrm{H}\left(\dfrac{19}{13},\ \dfrac{17}{13}\right)}$",
  "note": r"$ax+by+c=0$ に平行な直線は $ax+by+c'=0$，垂直な直線は $bx-ay+c''=0$ とおけるので、傾きを経由しなくても (1) $2(x-3)-3(y+1)=0$，(2) $3(x-3)+2(y+1)=0$ とすぐ書ける。",
  "ex": r"点 $(-2,\ 4)$ を通り直線 $x+2y-3=0$ に平行な直線・垂直な直線、および点 $(-2,\ 4)$ からこの直線に下ろした垂線の足を求めよ。",
  "exa": r"平行 $x+2y-6=0$，垂直 $2x-y+8=0$，垂線の足 $\left(-\dfrac{13}5,\ \dfrac{14}5\right)$"},
 {"lv": 2, "title": "点と直線の距離・三角形の面積",
  "q": r"3点 $\mathrm{A}(1,\ 5)$，$\mathrm{B}(-2,\ -1)$，$\mathrm{C}(4,\ 1)$ について<br>(1) 直線 BC の方程式　(2) 点 A と直線 BC の距離　(3) $\triangle\mathrm{ABC}$ の面積　を求めよ。",
  "hint": r"BC を底辺とみれば、高さは A と直線 BC の距離。点と直線の距離の公式を使う。",
  "sol": r"(1) 傾き $\dfrac{1-(-1)}{4-(-2)}=\dfrac13$，$y+1=\dfrac13(x+2)$ より　$\boldsymbol{x-3y-1=0}$<br>"
         r"(2) $\dfrac{|1-3\cdot5-1|}{\sqrt{1^2+(-3)^2}}=\dfrac{15}{\sqrt{10}}=\boldsymbol{\dfrac{3\sqrt{10}}2}$<br>"
         r"(3) $\mathrm{BC}=\sqrt{6^2+2^2}=2\sqrt{10}$ であるから　$\triangle\mathrm{ABC}=\dfrac12\cdot2\sqrt{10}\cdot\dfrac{3\sqrt{10}}2=\boldsymbol{15}$",
  "note": r"1つの頂点を原点に移すと、$\mathrm{O}(0,\ 0)$，$(x_1,\ y_1)$，$(x_2,\ y_2)$ を頂点とする三角形の面積は $\dfrac12|x_1y_2-x_2y_1|$。本問で A を原点に移すと B，C は $(-3,\ -6)$，$(3,\ -4)$ となり、$\dfrac12|(-3)(-4)-3\cdot(-6)|=15$ で一致する。",
  "ex": r"3点 $\mathrm{A}(3,\ 4)$，$\mathrm{B}(-1,\ 0)$，$\mathrm{C}(5,\ -2)$ について、直線 BC の方程式、A と直線 BC の距離、$\triangle\mathrm{ABC}$ の面積を求めよ。",
  "exa": r"$x+3y+1=0$，$\dfrac{8\sqrt{10}}5$，$16$"},
 {"lv": 2, "title": "直線に関する対称点・対称な直線",
  "q": r"直線 $\ell:\ x-2y+3=0$ がある。<br>(1) $\ell$ に関して点 $\mathrm{A}(4,\ 1)$ と対称な点 B の座標を求めよ。<br>(2) $\ell$ に関して直線 $m:\ 3x-y-11=0$ と対称な直線の方程式を求めよ。",
  "hint": r"B$(p,\ q)$ とおき「AB の中点が $\ell$ 上」「$\mathrm{AB}\perp\ell$」の2条件を立てる。(2) では $m$ が A を通ることに着目し、$m$ と $\ell$ の交点（動かない点）と B を結ぶ。",
  "sol": r"(1) $\mathrm{B}(p,\ q)$ とする。AB の中点 $\left(\dfrac{4+p}2,\ \dfrac{1+q}2\right)$ が $\ell$ 上にあるから<br>　$\dfrac{4+p}2-2\cdot\dfrac{1+q}2+3=0$　すなわち　$p-2q+8=0$　…①<br>"
         r"$\ell$ の傾きは $\dfrac12$ なので、AB の傾きは $-2$：$\dfrac{q-1}{p-4}=-2$　すなわち　$2p+q-9=0$　…②<br>"
         r"①，② を解いて $p=2,\ q=5$。　$\boldsymbol{\mathrm{B}(2,\ 5)}$<br>"
         r"(2) $3\cdot4-1-11=0$ より $m$ は A を通る。$m$ と $\ell$ の交点は、$y=3x-11$ を $\ell$ に代入して $x-2(3x-11)+3=0$，$x=5$，$y=4$。<br>"
         r"点 $(5,\ 4)$ は $\ell$ 上にあるので対称移動で動かない。よって求める直線は 2点 $(5,\ 4)$，$\mathrm{B}(2,\ 5)$ を通り、傾き $-\dfrac13$：$y-4=-\dfrac13(x-5)$。　$\boldsymbol{x+3y-17=0}$",
  "note": r"対称な直線は「直線上の2点をそれぞれ対称移動して結ぶ」のが基本。交点が求まるなら、その点は動かないので1点の移動ですむ。$m\parallel\ell$ のときは交点がないので2点とも移す。",
  "ex": r"直線 $\ell:\ 2x+y-1=0$ に関して、点 $\mathrm{A}(-1,\ -2)$ と対称な点、および直線 $x-y-1=0$ と対称な直線を求めよ。",
  "exa": r"$(3,\ 0)$，$x-7y-3=0$"},
 {"lv": 2, "title": "3直線が三角形をつくらない条件",
  "q": r"3直線 $x-2y+2=0$，$2x+y-6=0$，$ax+y-3=0$ が三角形をつくらないような定数 $a$ の値をすべて求めよ。",
  "hint": r"三角形ができないのは (i) どれか2直線が平行（一致を含む）(ii) 3直線が1点で交わる　のどちらか。もれなく調べる。",
  "sol": r"3直線の傾きは順に $\dfrac12$，$-2$，$-a$。はじめの2直線は平行でなく、交点は連立して $(2,\ 2)$。<br>"
         r"(i) 第3の直線が第1の直線と平行：$-a=\dfrac12$ より $a=-\dfrac12$（このとき $x-2y+6=0$ で一致はしない）。<br>"
         r"　第2の直線と平行：$-a=-2$ より $a=2$（このとき $2x+y-3=0$ で一致はしない）。<br>"
         r"(ii) 第3の直線が $(2,\ 2)$ を通る：$2a+2-3=0$ より $a=\dfrac12$。<br>"
         r"よって　$\boldsymbol{a=-\dfrac12,\ \dfrac12,\ 2}$",
  "note": r"(ii) を忘れやすい。「三角形をつくる条件」を問われたら、これら3つ以外の $a$ と答える。",
  "ex": r"3直線 $x+y-3=0$，$x-2y=0$，$ax-y-1=0$ が三角形をつくらないような $a$ の値をすべて求めよ。",
  "exa": r"$a=-1,\ \dfrac12,\ 1$"},
 {"lv": 3, "title": "定点を通る直線・2直線の交点を通る直線",
  "q": r"(1) 直線 $(k+2)x+(2k-1)y-3k-1=0$ は、定数 $k$ の値にかかわらず定点を通る。その定点の座標を求めよ。<br>(2) 2直線 $2x+y-4=0$，$x-3y+5=0$ の交点と点 $(-2,\ 3)$ を通る直線の方程式を求めよ。",
  "hint": r"(1) $k$ について整理し、$k$ についての恒等式とみる。(2) 交点を求めずに、$k(2x+y-4)+(x-3y+5)=0$ が「交点を通る直線」を表すことを使う。",
  "sol": r"(1) 与式を $k$ について整理すると　$k(x+2y-3)+(2x-y-1)=0$<br>"
         r"これがすべての $k$ で成り立つ条件は　$x+2y-3=0$ かつ $2x-y-1=0$。解いて $x=1,\ y=1$。　$\boldsymbol{(1,\ 1)}$<br>"
         r"(2) $k$ を定数として　$k(2x+y-4)+(x-3y+5)=0$　…①<br>"
         r"は、2直線の交点の座標を代入すると成り立つから、交点を通る直線を表す。① が点 $(-2,\ 3)$ を通るとき $k(-4+3-4)+(-2-9+5)=0$，$k=-\dfrac65$。<br>"
         r"① に代入して5倍すると $-6(2x+y-4)+5(x-3y+5)=0$，すなわち　$\boldsymbol{x+3y-7=0}$",
  "note": r"① は直線 $2x+y-4=0$ 自身を表せない（どんな $k$ でも）。求める直線がこれと一致する可能性があるときは別に調べる。本問では点 $(-2,\ 3)$ がこの直線上にないので問題ない。交点 $(1,\ 2)$ を求めて2点を結んでも同じ結果になる。",
  "ex": r"(1) 直線 $(2k+1)x-(k-3)y-5k+1=0$ が $k$ の値にかかわらず通る定点を求めよ。(2) 2直線 $x+y-3=0$，$3x-y+1=0$ の交点と点 $(2,\ 4)$ を通る直線の方程式を求めよ。",
  "exa": r"(1) $(2,\ -1)$　(2) $x-y+2=0$"},
 {"lv": 3, "title": "折れ線の長さの最小（対称点の利用）",
  "q": r"2点 $\mathrm{A}(2,\ 4)$，$\mathrm{B}(6,\ 2)$ と直線 $\ell:\ x+y=2$ がある。点 P が $\ell$ 上を動くとき、$\mathrm{AP}+\mathrm{PB}$ の最小値と、そのときの P の座標を求めよ。",
  "hint": r"A，B は $\ell$ の同じ側にある。A を $\ell$ に関して対称移動した点 A′ をとれば $\mathrm{AP}=\mathrm{A'P}$ となり、折れ線 A′PB が一直線のとき最小。",
  "sol": _F27 + r"$x+y-2$ の値は A で $4$，B で $6$ でともに正なので、A，B は $\ell$ の同じ側にある。<br>"
         r"A の $\ell$ に関する対称点を $\mathrm{A'}(a,\ b)$ とすると、中点が $\ell$ 上にあるから $\dfrac{2+a}2+\dfrac{4+b}2=2$，AA′ は $\ell$（傾き $-1$）に垂直なので傾き $1$：$b-4=a-2$。<br>"
         r"これより $a=-2,\ b=0$，$\mathrm{A'}(-2,\ 0)$。<br>"
         r"P が $\ell$ 上にあるとき $\mathrm{AP}=\mathrm{A'P}$ だから　$\mathrm{AP}+\mathrm{PB}=\mathrm{A'P}+\mathrm{PB}\geqq\mathrm{A'B}=\sqrt{8^2+2^2}=2\sqrt{17}$<br>"
         r"等号は P が線分 A′B 上にあるとき。直線 A′B は $y=\dfrac14(x+2)$ で、$x+y=2$ と連立して $x=\dfrac65,\ y=\dfrac45$。<br>"
         r"よって　最小値 $\boldsymbol{2\sqrt{17}}$，$\boldsymbol{\mathrm{P}\left(\dfrac65,\ \dfrac45\right)}$",
  "note": r"A，B が $\ell$ の反対側にあれば、対称点をとらずに線分 AB と $\ell$ の交点で最小になる。逆に $|\mathrm{AP}-\mathrm{PB}|$ の最大は、同じ側ならそのまま直線 AB と $\ell$ の交点、反対側なら対称点を使う。",
  "ex": r"2点 $\mathrm{A}(1,\ 2)$，$\mathrm{B}(4,\ 5)$ と直線 $y=x-3$ 上の点 P について、$\mathrm{AP}+\mathrm{PB}$ の最小値とそのときの P を求めよ。",
  "exa": r"最小値 $5\sqrt2$，$\mathrm{P}\left(\dfrac92,\ \dfrac32\right)$"},
 {"lv": 4, "title": "外心・重心・垂心が一直線上にあること（座標による証明）",
  "q": r"$\triangle\mathrm{ABC}$ の外心を O，重心を G，垂心を H とする。G は線分 OH を $1:2$ に内分する点であること（したがって O，G，H は一直線上にあること）を、座標を用いて証明せよ。ただし O と H が一致するときは、G もそれらと一致することを示せ。",
  "hint": r"A から BC に下ろした垂線の足を原点、BC を $x$ 軸にとると、A$(0,\ a)$，B$(b,\ 0)$，C$(c,\ 0)$ と置けて垂心の計算が楽になる。示すべき式は $\mathrm{G}=\dfrac{2\mathrm{O}+\mathrm{H}}3$（各座標で）。",
  "sol": r"直線 BC を $x$ 軸、A から BC に下ろした垂線の足を原点にとり、$\mathrm{A}(0,\ a)$，$\mathrm{B}(b,\ 0)$，$\mathrm{C}(c,\ 0)$（$a\neq0$，$b\neq c$）とおく。<br>"
         r"<b>重心</b>　$\mathrm{G}\left(\dfrac{b+c}3,\ \dfrac a3\right)$<br>"
         r"<b>垂心</b>　A からの垂線は $x=0$。B を通り AC に垂直な直線は、AC の方向が $(c,\ -a)$ であるから $c(x-b)-ay=0$。$x=0$ とおいて $y=-\dfrac{bc}a$。よって $\mathrm{H}\left(0,\ -\dfrac{bc}a\right)$<br>"
         r"<b>外心</b>　BC の垂直二等分線は $x=\dfrac{b+c}2$。$\mathrm{OA}=\mathrm{OB}$ より $x^2+(y-a)^2=(x-b)^2+y^2$，すなわち $-2ay+a^2=-2bx+b^2$。$x=\dfrac{b+c}2$ を代入して $-2ay+a^2=-bc$，$y=\dfrac{a^2+bc}{2a}$。よって $\mathrm{O}\left(\dfrac{b+c}2,\ \dfrac{a^2+bc}{2a}\right)$<br>"
         r"線分 OH を $1:2$ に内分する点の座標は<br>"
         r"　$x=\dfrac{2\cdot\frac{b+c}2+1\cdot0}{3}=\dfrac{b+c}3$，　$y=\dfrac{2\cdot\frac{a^2+bc}{2a}+1\cdot\left(-\frac{bc}a\right)}{3}=\dfrac13\cdot\dfrac{a^2+bc-bc}a=\dfrac a3$<br>"
         r"となり G と一致する。よって G は線分 OH を $1:2$ に内分し、$\mathrm{O}\neq\mathrm{H}$ のとき O，G，H は一直線上にある。$\mathrm{O}=\mathrm{H}$ のときは、内分点 G も O，H と一致する。　$\blacksquare$",
  "note": r"この直線をオイラー線という。$\mathrm{O}=\mathrm{H}$ となるのは正三角形のときに限る。B を通る垂線を $c(x-b)-ay=0$ と書いたのは、AC が $y$ 軸に平行（$c=0$，C が直角）の場合も除外せずに扱うため。",
  "ex": r"上と同じ座標設定で、$\mathrm{AH}=2\times$（外心 O と直線 BC の距離）が成り立つことを示せ。",
  "exa": r"$\mathrm{AH}=\left|a+\dfrac{bc}a\right|=\dfrac{|a^2+bc|}{|a|}$，O と BC の距離 $=\dfrac{|a^2+bc|}{2|a|}$ より成り立つ。"},
]})


def _v2():
    x, y, k = symbols("x y k")
    # 2.1
    assert _close(1.5 * 2 - 6, -3)
    for (px, py) in [(-1, 4), (3, -2)]:
        assert _close(-1.5 * px + 2.5, py)
    assert 4 - 0 - 4 == 0 and 0 - 2 * (-2) - 4 == 0
    assert -2 * (-1) == 2 and all(px + 3 == py for px, py in [(2, 5), (-4, -1)]) and 2 * (-3) + 6 == 0 and -6 + 6 == 0
    # 2.2
    s = solve([2 * x - 3 * y + 1, 3 * x + 2 * y - 7], [x, y])
    assert s[x] == R(19, 13) and s[y] == R(17, 13)
    assert 2 * 3 - 3 * (-1) - 9 == 0 and 3 * 3 + 2 * (-1) - 7 == 0 and 2 * 3 + (-3) * 2 == 0
    s = solve([x + 2 * y - 3, 2 * x - y + 8], [x, y])
    assert s[x] == R(-13, 5) and s[y] == R(14, 5)
    assert -2 + 8 - 6 == 0 and 2 * (-2) - 4 + 8 == 0
    # 2.3
    def area(A, B, C):
        return abs((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])) / 2
    assert -2 + 3 - 1 == 0 and 4 - 3 - 1 == 0 and area((1, 5), (-2, -1), (4, 1)) == 15
    assert _close(15 / math.sqrt(10), 3 * math.sqrt(10) / 2)
    assert -1 + 0 + 1 == 0 and 5 - 6 + 1 == 0 and area((3, 4), (-1, 0), (5, -2)) == 16
    assert _close(16 / math.sqrt(10), 8 * math.sqrt(10) / 5)
    # 2.4 反射
    def refl(a, b, c, P):
        t = Fr(a * P[0] + b * P[1] + c, a * a + b * b)
        return (P[0] - 2 * a * t, P[1] - 2 * b * t)
    assert refl(1, -2, 3, (4, 1)) == (2, 5)
    assert refl(1, -2, 3, (5, 4)) == (5, 4) and 15 - 4 - 11 == 0
    Q = refl(1, -2, 3, (0, -11))            # m 上の別の点
    assert Q[0] + 3 * Q[1] - 17 == 0 and 5 + 12 - 17 == 0
    assert refl(2, 1, -1, (-1, -2)) == (3, 0)
    for P in [(1, 0), (0, -1)]:             # x-y-1=0 上の2点
        Q = refl(2, 1, -1, P)
        assert Q[0] - 7 * Q[1] - 3 == 0
    # 2.5
    for (L1, L2, f, ans) in [((1, -2, 2), (2, 1, -6), lambda a: (a, 1, -3), {Fr(-1, 2), Fr(1, 2), Fr(2)}),
                             ((1, 1, -3), (1, -2, 0), lambda a: (a, -1, -1), {Fr(-1), Fr(1, 2), Fr(1)})]:
        got = set()
        for num in range(-400, 401):
            a = Fr(num, 40)
            L3 = f(a)
            par = any(P[0] * L3[1] - L3[0] * P[1] == 0 for P in (L1, L2))
            d = L1[0] * L2[1] - L2[0] * L1[1]
            X0 = Fr(-L1[2] * L2[1] + L2[2] * L1[1], d)
            Y0 = Fr(-L1[0] * L2[2] + L2[0] * L1[2], d)
            con = L3[0] * X0 + L3[1] * Y0 + L3[2] == 0
            if par or con:
                got.add(a)
        assert got == ans
    # 2.6
    e = (k + 2) * x + (2 * k - 1) * y - 3 * k - 1
    assert expand(e - (k * (x + 2 * y - 3) + (2 * x - y - 1))) == 0 and e.subs({x: 1, y: 1}) == 0
    s = solve([2 * x + y - 4, x - 3 * y + 5], [x, y])
    assert s[x] + 3 * s[y] - 7 == 0 and -2 + 9 - 7 == 0 and 2 * (-2) + 3 - 4 != 0
    e = (2 * k + 1) * x - (k - 3) * y - 5 * k + 1
    assert expand(e.subs({x: 2, y: -1})) == 0
    s = solve([x + y - 3, 3 * x - y + 1], [x, y])
    assert s[x] - s[y] + 2 == 0 and 2 - 4 + 2 == 0
    # 2.7 数値で最小を確認
    for A, B, line, mn, P in [((2, 4), (6, 2), lambda t: (t, 2 - t), 2 * math.sqrt(17), (1.2, 0.8)),
                              ((1, 2), (4, 5), lambda t: (t, t - 3), 5 * math.sqrt(2), (4.5, 1.5))]:
        best = min((math.dist(A, line(t / 1000)) + math.dist(line(t / 1000), B), t / 1000) for t in range(-10000, 10000))
        assert abs(best[0] - mn) < 1e-5 and abs(best[1] - P[0]) < 2e-3
        assert _close(math.dist(A, P) + math.dist(P, B), mn)
    # 2.8 オイラー線
    a, b, c = symbols("a b c", real=True)
    Ox, Oy = symbols("Ox Oy")
    so = solve([Ox ** 2 + (Oy - a) ** 2 - (Ox - b) ** 2 - Oy ** 2, (Ox - b) ** 2 + Oy ** 2 - (Ox - c) ** 2 - Oy ** 2], [Ox, Oy], dict=True)[0]
    Hx, Hy = symbols("Hx Hy")
    sh = solve([Hx * (c - b) - 0 * Hy, (Hx - b) * c + (Hy - 0) * (-a)], [Hx, Hy], dict=True)[0]   # AH⊥BC, BH⊥AC
    assert simplify(sh[Hx]) == 0 and simplify(sh[Hy] + b * c / a) == 0
    assert simplify(so[Ox] - (b + c) / 2) == 0 and simplify(so[Oy] - (a ** 2 + b * c) / (2 * a)) == 0
    assert simplify((2 * so[Ox] + sh[Hx]) / 3 - (b + c) / 3) == 0 and simplify((2 * so[Oy] + sh[Hy]) / 3 - a / 3) == 0
    assert simplify((a - sh[Hy]) - 2 * so[Oy]) == 0      # AH = 2×(O の y 座標)（符号つき）


_V.append(_v2)


# ---------------------------------------------------------------- 節3
_F33 = _fig((-1, 10.5), (-1, 10.5), [
    ("circ", (1, 1), 1, "r"), ("circ", (5, 5), 5, "b"), ("dot", (2, 1), "(2, 1)", (5, -3)),
    ("dot", (1, 1), "", (0, 0)), ("dot", (5, 5), "", (0, 0))], W=150)
_F35 = _fig((-0.8, 6.8), (-0.8, 4.6), [
    ("pl", [(0, 0), (6, 0), (3, 4), (0, 0)], "b"), ("circ", (3, 1.5), 1.5, "r"), ("dot", (3, 1.5), "I", (4, -3)),
    ("dot", (6, 0), "", (0, 0)), ("dot", (3, 4), "(3, 4)", (5, 4)), ("txt", (6, 0), "6", (-3, 12))], W=180)

SEC.append({"title": "円の方程式",
"base": r"""・中心 $(a,\ b)$，半径 $r$ の円：$(x-a)^2+(y-b)^2=r^2$<br>
・一般形 $x^2+y^2+lx+my+n=0$ は、$\left(x+\dfrac l2\right)^2+\left(y+\dfrac m2\right)^2=\dfrac{l^2+m^2-4n}4$ と変形でき、右辺が正のとき円を表す。<br>
・3点を通る円は一般形に代入して $l,\ m,\ n$ を決める。中心や接する条件がわかっているときは標準形を使う。<br>
・$x$ 軸に接する円：半径 $=|$中心の $y$ 座標$|$。両軸に接する円の中心は $(r,\ r)$ などの形。""",
"items": [
 {"lv": 1, "title": "円の方程式と中心・半径",
  "q": r"(1) 中心 $(2,\ -3)$，半径 $4$ の円　(2) 中心 $(-1,\ 2)$ で点 $(3,\ 5)$ を通る円　(3) 2点 $\mathrm{A}(-3,\ 4)$，$\mathrm{B}(5,\ -2)$ を直径の両端とする円　の方程式を求めよ。また、(4) 円 $x^2+y^2-6x+4y-3=0$ の中心と半径を求めよ。",
  "hint": r"中心と半径がわかれば標準形。直径の両端が与えられたら、中心は中点、半径は直径の半分。(4) は平方完成。",
  "sol": r"(1) $\boldsymbol{(x-2)^2+(y+3)^2=16}$<br>"
         r"(2) 半径は中心と $(3,\ 5)$ の距離 $\sqrt{4^2+3^2}=5$。　$\boldsymbol{(x+1)^2+(y-2)^2=25}$<br>"
         r"(3) 中心は AB の中点 $(1,\ 1)$，半径は $\dfrac12\sqrt{8^2+6^2}=5$。　$\boldsymbol{(x-1)^2+(y-1)^2=25}$<br>"
         r"(4) $(x-3)^2+(y+2)^2=3+9+4=16$ より　<b>中心 $\boldsymbol{(3,\ -2)}$，半径 $\boldsymbol{4}$</b>",
  "ex": r"(1) 中心 $(-3,\ 1)$，半径 $\sqrt5$　(2) 中心 $(4,\ -1)$ で原点を通る　(3) 2点 $(1,\ 6)$，$(-5,\ -2)$ を直径の両端とする　円の方程式を求めよ。(4) 円 $x^2+y^2+8x-2y+8=0$ の中心と半径を求めよ。",
  "exa": r"(1) $(x+3)^2+(y-1)^2=5$　(2) $(x-4)^2+(y+1)^2=17$　(3) $(x+2)^2+(y-2)^2=25$　(4) 中心 $(-4,\ 1)$，半径 $3$"},
 {"lv": 1, "title": "3点を通る円",
  "q": r"3点 $\mathrm{A}(1,\ 6)$，$\mathrm{B}(5,\ 4)$，$\mathrm{C}(3,\ 0)$ を通る円の方程式を求めよ。また、その中心と半径を求めよ。",
  "hint": r"中心も半径もわからないので一般形 $x^2+y^2+lx+my+n=0$ に3点を代入し、連立1次方程式を解く。",
  "sol": r"求める円を $x^2+y^2+lx+my+n=0$ とおく。3点を代入して<br>"
         r"　A：$l+6m+n=-37$　…①　　B：$5l+4m+n=-41$　…②　　C：$3l+n=-9$　…③<br>"
         r"②－① より $4l-2m=-4$，すなわち $m=2l+2$。①－③ より $-2l+6m=-28$。<br>"
         r"代入して $-2l+12l+12=-28$，$l=-4$，$m=-6$，③ より $n=3$。<br>"
         r"よって　$\boldsymbol{x^2+y^2-4x-6y+3=0}$。$(x-2)^2+(y-3)^2=10$ より　<b>中心 $\boldsymbol{(2,\ 3)}$，半径 $\boldsymbol{\sqrt{10}}$</b>",
  "note": r"この円は $\triangle\mathrm{ABC}$ の外接円。中心は AB，BC の垂直二等分線の交点として求めることもできる。",
  "ex": r"3点 $\mathrm{O}(0,\ 0)$，$(2,\ 6)$，$(4,\ 2)$ を通る円の方程式を求めよ。",
  "exa": r"$x^2+y^2-2x-6y=0$（中心 $(1,\ 3)$，半径 $\sqrt{10}$）"},
 {"lv": 2, "title": "座標軸に接する円",
  "q": r"点 $(2,\ 1)$ を通り、$x$ 軸と $y$ 軸の両方に接する円の方程式を求めよ。",
  "hint": r"両軸に接する円は1つの象限に含まれる。$(2,\ 1)$ は第1象限の点なので、中心は $(r,\ r)$，半径は $r$ $(r\gt0)$ とおける。",
  "sol": _F33 + r"円は点 $(2,\ 1)$ を通り両軸に接するから第1象限にあり、中心 $(r,\ r)$，半径 $r$ $(r\gt0)$ とおける。<br>"
         r"$(2-r)^2+(1-r)^2=r^2$　より　$r^2-6r+5=0$，$(r-1)(r-5)=0$，$r=1,\ 5$<br>"
         r"よって　$\boldsymbol{(x-1)^2+(y-1)^2=1,\ \ (x-5)^2+(y-5)^2=25}$",
  "note": r"「$x$ 軸に接する」だけなら中心 $(a,\ b)$，半径 $|b|$。接する条件は「半径＝中心と接線の距離」と捉えると、一般の直線に接する場合にも同じ考え方が使える。",
  "ex": r"点 $(4,\ -2)$ を通り、$x$ 軸と $y$ 軸の両方に接する円の方程式を求めよ。",
  "exa": r"$(x-2)^2+(y+2)^2=4,\ \ (x-10)^2+(y+10)^2=100$"},
 {"lv": 2, "title": "方程式が円を表す条件・半径の最大",
  "q": r"方程式 $x^2+y^2-2ax+4ay+6a^2-2a-3=0$ について<br>(1) これが円を表すような定数 $a$ の値の範囲を求めよ。<br>(2) 円の半径が最大となるときの $a$ の値と、そのときの円の方程式を求めよ。",
  "hint": r"平方完成して $(x-p)^2+(y-q)^2=k$ の形にし、「右辺 $k\gt0$」が円を表す条件。$k$ は $a$ の2次式なので、その最大を考える。",
  "sol": r"$(x-a)^2+(y+2a)^2=a^2+4a^2-6a^2+2a+3=-a^2+2a+3$<br>"
         r"(1) 円を表す条件は $-a^2+2a+3\gt0$，すなわち $(a+1)(a-3)\lt0$。　$\boldsymbol{-1\lt a\lt3}$<br>"
         r"(2) 半径の2乗は $-a^2+2a+3=-(a-1)^2+4$ で、$a=1$ のとき最大値 $4$（$a=1$ は (1) の範囲内）。<br>"
         r"よって　$\boldsymbol{a=1}$，$\boldsymbol{(x-1)^2+(y+2)^2=4}$",
  "note": r"右辺が $0$ のときは1点 $(a,\ -2a)$ を表し、負のときは何も表さない。中心 $(a,\ -2a)$ は $a$ によらず直線 $y=-2x$ 上にある。",
  "ex": r"方程式 $x^2+y^2+2ax-4y+2a^2+2a-4=0$ が円を表す $a$ の範囲と、半径が最大となるときの円の方程式を求めよ。",
  "exa": r"$-4\lt a\lt2$，$a=-1$ のとき $(x-1)^2+(y-2)^2=9$"},
 {"lv": 3, "title": "3直線に接する円（三角形の内接円）",
  "q": r"3直線 $y=0$，$4x-3y=0$，$4x+3y-24=0$ で囲まれた三角形の内接円の方程式を求めよ。",
  "hint": r"中心を $(p,\ q)$，半径を $r$ とし「中心と各辺の距離 $=r$」。絶対値は、中心が三角形の<b>内部</b>にあることから符号を決めてはずす。",
  "sol": _F35 + r"3直線の交点は $(0,\ 0)$，$(6,\ 0)$，$(3,\ 4)$。内接円の中心を $(p,\ q)$，半径を $r$ とする。<br>"
         r"中心は三角形の内部にあり、内部の点では $y\gt0$，$4x-3y\gt0$（頂点 $(6,\ 0)$ と同じ側），$4x+3y-24\lt0$（頂点 $(0,\ 0)$ と同じ側）である。よって<br>"
         r"　$q=r$，　$\dfrac{4p-3q}5=r$，　$\dfrac{-(4p+3q-24)}5=r$<br>"
         r"第1，2式から $4p=8r$，$p=2r$。第3式に代入して $24-8r-3r=5r$，$r=\dfrac32$，$p=3$。<br>"
         r"よって　$\boldsymbol{(x-3)^2+\left(y-\dfrac32\right)^2=\dfrac94}$",
  "note": r"絶対値を符号を決めずに外すと、内接円のほかに3つの傍接円（三角形の外側で3直線に接する円）も現れる。面積 $S=12$，周の長さ $16$ から $r=\dfrac{2S}{a+b+c}=\dfrac32$ と確かめられる。",
  "ex": r"3直線 $y=0$，$12x-5y=0$，$12x+5y-120=0$ で囲まれた三角形の内接円の方程式を求めよ。",
  "exa": r"$(x-5)^2+\left(y-\dfrac{10}3\right)^2=\dfrac{100}9$"},
]})


def _v3():
    x, y, l, m, n, a = symbols("x y l m n a")
    # 3.1
    assert 4 ** 2 + 3 ** 2 == 25 and (8 ** 2 + 6 ** 2) == 100
    assert expand((x - 3) ** 2 + (y + 2) ** 2 - 16 - (x ** 2 + y ** 2 - 6 * x + 4 * y - 3)) == 0
    assert 16 + 1 == 17 and (6 ** 2 + 8 ** 2) == 100 and ((1 - 5) / 2, (6 - 2) / 2) == (-2, 2)
    assert expand((x + 4) ** 2 + (y - 1) ** 2 - 9 - (x ** 2 + y ** 2 + 8 * x - 2 * y + 8)) == 0
    # 3.2
    gen = x ** 2 + y ** 2 + l * x + m * y + n
    s = solve([gen.subs({x: p, y: q}) for p, q in [(1, 6), (5, 4), (3, 0)]], [l, m, n])
    assert (s[l], s[m], s[n]) == (-4, -6, 3)
    s = solve([gen.subs({x: p, y: q}) for p, q in [(0, 0), (2, 6), (4, 2)]], [l, m, n])
    assert (s[l], s[m], s[n]) == (-2, -6, 0)
    # 3.3
    r = symbols("r", positive=True)
    assert set(solve((2 - r) ** 2 + (1 - r) ** 2 - r ** 2, r)) == {1, 5}
    assert set(solve((4 - r) ** 2 + (-2 + r) ** 2 - r ** 2, r)) == {2, 10}
    # 3.4
    e = x ** 2 + y ** 2 - 2 * a * x + 4 * a * y + 6 * a ** 2 - 2 * a - 3
    assert expand(e - ((x - a) ** 2 + (y + 2 * a) ** 2 - (-a ** 2 + 2 * a + 3))) == 0
    assert set(solve(-a ** 2 + 2 * a + 3, a)) == {-1, 3}
    e = x ** 2 + y ** 2 + 2 * a * x - 4 * y + 2 * a ** 2 + 2 * a - 4
    assert expand(e - ((x + a) ** 2 + (y - 2) ** 2 - (-a ** 2 - 2 * a + 8))) == 0
    assert set(solve(-a ** 2 - 2 * a + 8, a)) == {-4, 2} and (-a ** 2 - 2 * a + 8).subs(a, -1) == 9
    # 3.5 内接円：3辺までの距離が等しく内部にある
    for lines, (cx, cy, rr) in [([(0, 1, 0), (4, -3, 0), (4, 3, -24)], (3, 1.5, 1.5)),
                                ([(0, 1, 0), (12, -5, 0), (12, 5, -120)], (5, 10 / 3, 10 / 3))]:
        for (A, B, C) in lines:
            assert _close(abs(A * cx + B * cy + C) / math.hypot(A, B), rr)
    # 内部の判定（頂点の重心と同じ側）
    for lines, cen, vs in [([(0, 1, 0), (4, -3, 0), (4, 3, -24)], (3, 1.5), [(0, 0), (6, 0), (3, 4)]),
                           ([(0, 1, 0), (12, -5, 0), (12, 5, -120)], (5, 10 / 3), [(0, 0), (10, 0), (5, 12)])]:
        gx, gy = sum(v[0] for v in vs) / 3, sum(v[1] for v in vs) / 3
        for (A, B, C) in lines:
            assert (A * cen[0] + B * cen[1] + C) * (A * gx + B * gy + C) > 0
    # 符号を外さないと4つ（内接円＋傍接円3つ）
    p, q, rr = symbols("p q rr")
    cnt = 0
    for s1 in (1, -1):
        for s2 in (1, -1):
            sol = solve([s1 * q - rr, s2 * (4 * p - 3 * q) / 5 - rr, (24 - 4 * p - 3 * q) / 5 - rr], [p, q, rr], dict=True)
            cnt += sum(1 for d in sol if d[rr] > 0)
    for s1 in (1, -1):
        for s2 in (1, -1):
            sol = solve([s1 * q - rr, s2 * (4 * p - 3 * q) / 5 - rr, -(24 - 4 * p - 3 * q) / 5 - rr], [p, q, rr], dict=True)
            cnt += sum(1 for d in sol if d[rr] > 0)
    assert cnt == 4


_V.append(_v3)


# ---------------------------------------------------------------- 節4
_F44 = _fig((-2.6, 4.8), (-2.5, 2.9), [
    ("circ", (0, 0), 2, "b"), ("seg", (4, 2), (0, 2), "g"), ("seg", (4, 2), (1.6, -1.2), "g"),
    ("seg", (0, 2), (1.6, -1.2), "r"), ("dot", (4, 2), "P", (3, -3)), ("dot", (0, 2), "A", (-11, -3)),
    ("dot", (1.6, -1.2), "B", (2, 11))], W=180)
_F45 = _fig((-3.6, 3.6), (-2.8, 4.4), [
    ("circ", (1, 2), 2, "b"), ("line", 3, 4, 9, "k"), ("seg", (2.2, 3.6), (-1.4, -1.2), "gd"),
    ("dot", (1, 2), "", (0, 0)), ("dot", (-0.2, 0.4), "", (0, 0)), ("dot", (2.2, 3.6), "P", (3, -3)),
    ("dot", (-3, 0), "A", (-2, -5)), ("dot", (0, -2.25), "B", (4, 10))], W=170)
_F46 = _fig((-2.6, 2.6), (-2.4, 2.6), [
    ("fn", lambda t: t * t - 2, -2.2, 2.2, "b"), ("circ", (0, 0), 2, "r"), ("circ", (0, 0), math.sqrt(7) / 2, "rd"),
    ], W=170)

SEC.append({"title": "円と直線",
"base": r"""・円の中心と直線の距離を $d$，半径を $r$ とすると　$d\lt r$：2点で交わる，$d=r$：接する，$d\gt r$：共有点なし（判別式 $D$ の符号でもよい）<br>
・円 $x^2+y^2=r^2$ 上の点 $(x_1,\ y_1)$ における接線：$x_1x+y_1y=r^2$<br>
・弦の長さ：$2\sqrt{r^2-d^2}$。弦の中点は中心から直線に下ろした垂線の足。<br>
・円外の点 $(p,\ q)$ から円 $x^2+y^2=r^2$ に引いた2本の接線の接点を通る直線：$px+qy=r^2$""",
"items": [
 {"lv": 1, "title": "円と直線の共有点の個数",
  "q": r"円 $x^2+y^2=5$ と直線 $y=2x+k$ について<br>(1) 共有点の個数を、定数 $k$ の値によって分類せよ。<br>(2) 円と直線が接するときの $k$ の値と、接点の座標を求めよ。",
  "hint": r"個数は「中心と直線の距離 $d$」と半径 $\sqrt5$ の大小で決まる。接点は、代入した2次方程式の重解として求める。",
  "sol": r"(1) 中心 $(0,\ 0)$ と直線 $2x-y+k=0$ の距離は $d=\dfrac{|k|}{\sqrt5}$。$d\lt\sqrt5 \Longleftrightarrow |k|\lt5$ であるから<br>"
         r"　<b>$\boldsymbol{-5\lt k\lt5}$ のとき2個，$\boldsymbol{k=\pm5}$ のとき1個，$\boldsymbol{k\lt-5,\ 5\lt k}$ のとき0個</b><br>"
         r"(2) $k=\pm5$。$y=2x+k$ を代入すると $5x^2+4kx+k^2-5=0$ で、接するとき重解 $x=-\dfrac{2k}5$。<br>"
         r"　$\boldsymbol{k=5}$ のとき接点 $\boldsymbol{(-2,\ 1)}$，$\boldsymbol{k=-5}$ のとき接点 $\boldsymbol{(2,\ -1)}$",
  "note": r"判別式なら $\dfrac D4=4k^2-5(k^2-5)=25-k^2$ で同じ結論。円と直線では距離の方が計算が軽いことが多いが、接点まで必要なら代入した式も使う。",
  "ex": r"円 $(x-1)^2+y^2=4$ と直線 $y=x+k$ の共有点の個数を、$k$ の値によって分類せよ。",
  "exa": r"$-1-2\sqrt2\lt k\lt-1+2\sqrt2$ のとき2個，$k=-1\pm2\sqrt2$ のとき1個，それ以外0個"},
 {"lv": 1, "title": "円が直線から切り取る弦の長さ",
  "q": r"円 $x^2+y^2-4x+2y-4=0$ が直線 $x-2y+1=0$ から切り取る弦の長さと、弦の中点の座標を求めよ。",
  "hint": r"中心から直線に下ろした垂線は弦を2等分する。三平方の定理で半分の長さ $\sqrt{r^2-d^2}$ を求める。",
  "sol": r"円は $(x-2)^2+(y+1)^2=9$，中心 $\mathrm{C}(2,\ -1)$，半径 $3$。C と直線の距離は $d=\dfrac{|2+2+1|}{\sqrt5}=\sqrt5$。<br>"
         r"弦の長さは　$2\sqrt{9-5}=\boldsymbol{4}$<br>"
         r"弦の中点は C から直線に下ろした垂線の足。C を通り直線（傾き $\dfrac12$）に垂直な直線 $y=-2x+3$ と $x-2y+1=0$ を連立して $\boldsymbol{(1,\ 1)}$",
  "ex": r"円 $x^2+y^2=10$ が直線 $x+y-2=0$ から切り取る弦の長さと、弦の中点を求めよ。",
  "exa": r"長さ $4\sqrt2$，中点 $(1,\ 1)$"},
 {"lv": 2, "title": "円の接線（円上の点・円外の点から）",
  "q": r"(1) 円 $x^2+y^2=25$ 上の点 $(3,\ -4)$ における接線の方程式を求めよ。<br>(2) 点 $(7,\ 1)$ から円 $x^2+y^2=25$ に引いた接線の方程式と、接点の座標を求めよ。",
  "hint": r"(2) 接点を $(p,\ q)$ とおくと接線は $px+qy=25$。これが $(7,\ 1)$ を通る条件と、接点が円上にある条件を連立する。",
  "sol": r"(1) $\boldsymbol{3x-4y=25}$<br>"
         r"(2) 接点を $(p,\ q)$ とすると $p^2+q^2=25$　…①，接線 $px+qy=25$ が $(7,\ 1)$ を通るから $7p+q=25$　…②<br>"
         r"② より $q=25-7p$。① に代入して $p^2+(25-7p)^2=25$，$50p^2-350p+600=0$，$(p-3)(p-4)=0$。<br>"
         r"$p=3$ のとき $q=4$，$p=4$ のとき $q=-3$。<br>"
         r"よって　<b>接線 $\boldsymbol{3x+4y=25}$（接点 $\boldsymbol{(3,\ 4)}$），$\boldsymbol{4x-3y=25}$（接点 $\boldsymbol{(4,\ -3)}$）</b>",
  "note": r"傾き $m$ を用いて $y-1=m(x-7)$ とおき「中心との距離 $=5$」から $12m^2-7m-12=0$，$m=-\dfrac34,\ \dfrac43$ としてもよい。ただしこの方法では $y$ 軸に平行な接線 $x=7$ が候補から漏れるので、別に調べる必要がある（本問では距離が $7$ で接線にならない）。",
  "ex": r"(1) 円 $x^2+y^2=10$ 上の点 $(-1,\ 3)$ における接線　(2) 点 $(4,\ 2)$ から円 $x^2+y^2=10$ に引いた接線と接点　を求めよ。",
  "exa": r"(1) $-x+3y=10$　(2) $x+3y=10$（接点 $(1,\ 3)$），$3x-y=10$（接点 $(3,\ -1)$）"},
 {"lv": 3, "title": "接点を結ぶ直線（極線）",
  "q": r"点 $\mathrm{P}(4,\ 2)$ から円 $x^2+y^2=4$ に2本の接線を引き、接点を A，B とする。<br>(1) 直線 AB の方程式を求めよ。　(2) 線分 AB の長さを求めよ。",
  "hint": r"接点の座標を求めなくても、接点 $(x_1,\ y_1)$ の接線 $x_1x+y_1y=4$ が P を通るという条件 $4x_1+2y_1=4$ は「A も B も直線 $4x+2y=4$ 上にある」と読める。",
  "sol": _F44 + r"(1) $\mathrm{A}(x_1,\ y_1)$ における接線 $x_1x+y_1y=4$ は P を通るから $4x_1+2y_1=4$。同様に $\mathrm{B}(x_2,\ y_2)$ について $4x_2+2y_2=4$。<br>"
         r"これは2点 A，B がともに直線 $4x+2y=4$ 上にあることを示す。異なる2点を通る直線はただ1つなので、直線 AB は　$\boldsymbol{2x+y=2}$<br>"
         r"(2) 原点と直線 AB の距離は $\dfrac{2}{\sqrt5}$ なので　$\mathrm{AB}=2\sqrt{4-\dfrac45}=2\cdot\dfrac4{\sqrt5}=\boldsymbol{\dfrac{8\sqrt5}5}$",
  "note": r"実際に連立すると $\mathrm{A}(0,\ 2)$，$\mathrm{B}\left(\dfrac85,\ -\dfrac65\right)$。一般に、円 $x^2+y^2=r^2$ の外の点 $(p,\ q)$ に対し直線 $px+qy=r^2$ を極線という。この「同じ形の式を2点が満たす」論法は、軌跡や通過領域でもくり返し使う。",
  "ex": r"点 $(-3,\ 1)$ から円 $x^2+y^2=5$ に引いた2本の接線の接点を A，B とするとき、直線 AB の方程式と AB の長さを求めよ。",
  "exa": r"$3x-y+5=0$，$\mathrm{AB}=\sqrt{10}$"},
 {"lv": 3, "title": "円周上の点と直線の距離の最大・最小",
  "q": r"円 $C:\ (x-1)^2+(y-2)^2=4$ 上を点 P が動く。直線 $\ell:\ 3x+4y+9=0$ と $x$ 軸，$y$ 軸の交点をそれぞれ A，B とする。<br>(1) P と $\ell$ の距離の最大値・最小値と、そのときの P の座標を求めよ。<br>(2) $\triangle\mathrm{PAB}$ の面積の最大値を求めよ。",
  "hint": r"中心と $\ell$ の距離を $d$ とすれば、円周上の点と $\ell$ の距離は $d-r$ 以上 $d+r$ 以下。端は中心を通り $\ell$ に垂直な直線と円の交点で実現する。",
  "sol": _F45 + r"(1) 中心 $(1,\ 2)$ と $\ell$ の距離は $d=\dfrac{|3+8+9|}5=4\gt2$ だから $\ell$ は円と交わらない。<br>"
         r"P と $\ell$ の距離は、P が中心を通り $\ell$ に垂直な直線と円の交点にあるとき最大 $d+2$・最小 $d-2$ となる。<br>"
         r"中心を通り $\ell$ に垂直な直線 $y-2=\dfrac43(x-1)$ と円の交点は $x=1\pm\dfrac65$，$y=2\pm\dfrac85$（複号同順）の2点で、$3x+4y+9$ の値が小さい $\left(-\dfrac15,\ \dfrac25\right)$ の方が $\ell$ に近い。よって<br>"
         r"　<b>最大値 $\boldsymbol{6}$，$\boldsymbol{\mathrm{P}\left(\dfrac{11}5,\ \dfrac{18}5\right)}$；最小値 $\boldsymbol{2}$，$\boldsymbol{\mathrm{P}\left(-\dfrac15,\ \dfrac25\right)}$</b><br>"
         r"(2) $\mathrm{A}(-3,\ 0)$，$\mathrm{B}\left(0,\ -\dfrac94\right)$，$\mathrm{AB}=\sqrt{9+\dfrac{81}{16}}=\dfrac{15}4$。高さの最大は (1) より $6$ なので<br>"
         r"　最大値 $\dfrac12\cdot\dfrac{15}4\cdot6=\boldsymbol{\dfrac{45}4}$",
  "note": r"「円周上の点と直線（あるいは定点）の距離」は、中心までの距離に $\pm r$ すると覚えてよいが、その値をとる点が実際に存在することを言い添える。",
  "ex": r"円 $x^2+y^2=9$ 上の点 P と直線 $x+y-6=0$ の距離の最大値・最小値、および直線と $x$ 軸，$y$ 軸の交点 A，B に対する $\triangle\mathrm{PAB}$ の面積の最大値を求めよ。",
  "exa": r"最大値 $3\sqrt2+3$（$\mathrm{P}\left(-\frac{3\sqrt2}2,\ -\frac{3\sqrt2}2\right)$），最小値 $3\sqrt2-3$（$\mathrm{P}\left(\frac{3\sqrt2}2,\ \frac{3\sqrt2}2\right)$），面積の最大値 $18+9\sqrt2$"},
 {"lv": 4, "title": "円と放物線の共有点の個数",
  "q": r"円 $x^2+y^2=r^2$ $(r\gt0)$ と放物線 $y=x^2-2$ の共有点の個数を、$r$ の値によって分類せよ。",
  "hint": r"$x^2=y+2$ を代入して $y$ の2次方程式にする。ただし $x^2=y+2\geqq0$ より<b>$y\geqq-2$ の解だけが有効</b>で、$y\gt-2$ の解1つに共有点2個（$x=\pm\sqrt{y+2}$），$y=-2$ の解には共有点1個が対応する。",
  "sol": _F46 + r"$x^2=y+2$ を代入して　$y^2+y+2-r^2=0$　…①<br>"
         r"共有点は、① の実数解 $y$ のうち $y\geqq-2$ を満たすものに対応し、$y\gt-2$ なら $x=\pm\sqrt{y+2}$ の2個、$y=-2$ なら $x=0$ の1個である。<br>"
         r"$f(y)=y^2+y+2-r^2=\left(y+\dfrac12\right)^2+\dfrac74-r^2$ とおく。軸 $y=-\dfrac12$ は $-2$ より大きく、$f(-2)=4-r^2$。<br>"
         r"(i) $r^2\lt\dfrac74$：① は実数解をもたない。<b>0個</b><br>"
         r"(ii) $r^2=\dfrac74$：重解 $y=-\dfrac12\ (\gt-2)$。<b>2個</b><br>"
         r"(iii) $\dfrac74\lt r^2\lt4$：$f(-2)\gt0$ で軸が $-2$ より右なので、2解はともに $-2$ より大きい。<b>4個</b><br>"
         r"(iv) $r^2=4$：$f(y)=(y+2)(y-1)$ で、$y=-2$ から1個、$y=1$ から2個。<b>3個</b><br>"
         r"(v) $r^2\gt4$：$f(-2)\lt0$ なので、$-2$ より大きい解はちょうど1つ。<b>2個</b><br>"
         r"まとめて　$\boldsymbol{0\lt r\lt\dfrac{\sqrt7}2}$ <b>のとき0個，</b>$\boldsymbol{r=\dfrac{\sqrt7}2}$ <b>のとき2個，</b>$\boldsymbol{\dfrac{\sqrt7}2\lt r\lt2}$ <b>のとき4個，</b>$\boldsymbol{r=2}$ <b>のとき3個，</b>$\boldsymbol{r\gt2}$ <b>のとき2個</b>",
  "note": r"「$y$ の解の個数」と「共有点の個数」は一致しない。$y$ の値1つに $x$ がいくつ対応するかを必ず確認する。図の破線は $r=\dfrac{\sqrt7}2$（2点で接する），実線は $r=2$（頂点を通る）。",
  "ex": r"放物線 $y=x^2+a$ と円 $x^2+y^2=1$ の共有点の個数を、定数 $a$ の値によって分類せよ。",
  "exa": r"$a\lt-\dfrac54$ で0個，$a=-\dfrac54$ で2個，$-\dfrac54\lt a\lt-1$ で4個，$a=-1$ で3個，$-1\lt a\lt1$ で2個，$a=1$ で1個，$a\gt1$ で0個"},
]})


def _npts(F, G, X, Y):
    """sympy で連立方程式の実数解の個数を数える"""
    sols = solve([F, G], [X, Y], dict=True)
    pts = set()
    for d in sols:
        xv, yv = complex(d[X].evalf(30)), complex(d[Y].evalf(30))
        if abs(xv.imag) < 1e-12 and abs(yv.imag) < 1e-12:
            pts.add((round(xv.real, 9), round(yv.real, 9)))
    return len(pts)


def _v4():
    x, y = symbols("x y")
    # 4.1
    for k in [R(-6), R(-5), R(-3), 0, R(49, 10), 5, R(51, 10)]:
        c = _npts(x ** 2 + y ** 2 - 5, y - 2 * x - k, x, y)
        assert c == (2 if abs(k) < 5 else 1 if abs(k) == 5 else 0)
    assert solve([x ** 2 + y ** 2 - 5, y - 2 * x - 5], [x, y]) == [(-2, 1)]
    assert solve([x ** 2 + y ** 2 - 5, y - 2 * x + 5], [x, y]) == [(2, -1)]
    for k in [-4.0, -1 - 2 * 2 ** .5 + 1e-3, 0.8, -1 + 2 * 2 ** .5 + 1e-3, -1 - 2 * 2 ** .5 - 1e-3]:
        d = abs(1 + k) / 2 ** .5
        D = (2 * k - 2) ** 2 - 8 * (k * k - 3)       # (x-1)^2+(x+k)^2=4 → 2x^2+(2k-2)x+k^2-3=0
        assert (D > 0) == (d < 2)
    # 4.2
    s = solve([x ** 2 + y ** 2 - 4 * x + 2 * y - 4, x - 2 * y + 1], [x, y])
    (a1, b1), (a2, b2) = s
    assert simplify((a1 - a2) ** 2 + (b1 - b2) ** 2 - 16) == 0 and ((a1 + a2) / 2, (b1 + b2) / 2) == (1, 1)
    s = solve([x ** 2 + y ** 2 - 10, x + y - 2], [x, y])
    (a1, b1), (a2, b2) = s
    assert simplify((a1 - a2) ** 2 + (b1 - b2) ** 2 - 32) == 0 and simplify((a1 + a2) / 2 - 1) == 0
    # 4.3
    assert 9 + 16 == 25
    for (p, q) in [(3, 4), (4, -3)]:
        assert p * p + q * q == 25 and 7 * p + q == 25
    m = symbols("m")
    assert set(solve(12 * m ** 2 - 7 * m - 12, m)) == {R(-3, 4), R(4, 3)}
    assert (-1) ** 2 + 9 == 10
    for (p, q) in [(1, 3), (3, -1)]:
        assert p * p + q * q == 10 and 4 * p + 2 * q == 10
    # 4.4
    s = solve([x ** 2 + y ** 2 - 4, 2 * x + y - 2], [x, y])
    assert set(s) == {(0, 2), (R(8, 5), R(-6, 5))}
    for (p, q) in s:         # 接線が P を通る
        assert p * 4 + q * 2 == 4
    assert (R(8, 5)) ** 2 + (R(-16, 5)) ** 2 == R(64 * 5, 25)
    s = solve([x ** 2 + y ** 2 - 5, 3 * x - y + 5], [x, y])
    for (p, q) in s:
        assert simplify(-3 * p + q - 5) == 0
    (a1, b1), (a2, b2) = s
    assert simplify((a1 - a2) ** 2 + (b1 - b2) ** 2 - 10) == 0
    # 4.5 数値
    N = 20000
    ds = [(abs(3 * (1 + 2 * math.cos(t)) + 4 * (2 + 2 * math.sin(t)) + 9) / 5, t) for t in [2 * math.pi * i / N for i in range(N)]]
    mx, mn = max(ds), min(ds)
    assert abs(mx[0] - 6) < 1e-7 and abs(mn[0] - 2) < 1e-7
    assert abs(1 + 2 * math.cos(mx[1]) - 2.2) < 1e-3 and abs(2 + 2 * math.sin(mx[1]) - 3.6) < 1e-3
    assert abs(1 + 2 * math.cos(mn[1]) + 0.2) < 1e-3 and abs(2 + 2 * math.sin(mn[1]) - 0.4) < 1e-3
    assert _close(math.dist((-3, 0), (0, -2.25)), 3.75) and _close(0.5 * 3.75 * 6, 45 / 4)
    ds = [abs(3 * math.cos(t) + 3 * math.sin(t) - 6) / 2 ** .5 for t in [2 * math.pi * i / N for i in range(N)]]
    assert abs(max(ds) - (3 * 2 ** .5 + 3)) < 1e-7 and abs(min(ds) - (3 * 2 ** .5 - 3)) < 1e-7
    assert _close(0.5 * 6 * 2 ** .5 * (3 * 2 ** .5 + 3), 18 + 9 * 2 ** .5)
    # 4.6 個数
    r2s = [R(1), R(7, 4), R(2), R(3), R(4), R(5), R(9)]
    want = [0, 2, 4, 4, 3, 2, 2]
    for r2, w in zip(r2s, want):
        assert _npts(x ** 2 + y ** 2 - r2, y - x ** 2 + 2, x, y) == w
    for a, w in [(R(-2), 0), (R(-5, 4), 2), (R(-9, 8), 4), (R(-1), 3), (R(0), 2), (R(1, 2), 2), (R(1), 1), (R(3, 2), 0)]:
        assert _npts(x ** 2 + y ** 2 - 1, y - x ** 2 - a, x, y) == w


_V.append(_v4)


# ---------------------------------------------------------------- 節5
_F52 = _fig((-2.6, 3.9), (-2.6, 2.9), [
    ("circ", (0, 0), math.sqrt(5), "b"), ("circ", (2, 1), math.sqrt(2), "b"), ("line", 2, 1, -4, "rd"),
    ("dot", (1, 2), "", (0, 0)), ("dot", (2.2, -0.4), "", (0, 0)), ("txt", (2.5, -1.6), "2x+y=4", (-6, 0), True)], W=170)
_F53 = _fig((-2.2, 7.6), (-2.2, 8.4), [
    ("circ", (0, 0), 1, "b"), ("circ", (3, 4), 4, "b"), ("line", 3, 4, -5, "r"), ("line", 1, 0, 1, "r"), ("line", 7, -24, -25, "r"),
    ("dot", (0.6, 0.8), "", (0, 0)), ("dot", (3, 4), "", (0, 0))], W=160)

SEC.append({"title": "2つの円",
"base": r"""・半径 $r_1,\ r_2$ $(r_1\gt r_2)$ の2円の中心間の距離を $d$ とすると<br>
　$d\gt r_1+r_2$：離れている，$d=r_1+r_2$：外接，$r_1-r_2\lt d\lt r_1+r_2$：2点で交わる，$d=r_1-r_2$：内接，$d\lt r_1-r_2$：一方が他方の内部<br>
・2円 $f=0$，$g=0$（$x^2,\ y^2$ の係数は1）が2点で交わるとき、$kf+g=0$ は $k\neq-1$ なら2交点を通る円，$k=-1$ なら2交点を通る直線（共通弦）を表す。<br>
・共通接線は「一方の円の接線の式を文字でおき、他方の円の中心との距離＝半径」とする。""",
"items": [
 {"lv": 2, "title": "2円の位置関係",
  "q": r"円 $C_1:\ x^2+y^2=4$ と円 $C_2:\ (x-3)^2+(y-4)^2=r^2$ $(r\gt0)$ について、次の条件を満たす $r$ の値または範囲を求めよ。<br>(1) 外接する　(2) 内接する　(3) 2点で交わる　(4) 共有点をもたない",
  "hint": r"中心間の距離 $d=5$ と、半径の和 $r+2$，差 $|r-2|$ を比べる。",
  "sol": r"中心間の距離は $d=\sqrt{3^2+4^2}=5$。<br>"
         r"(1) $r+2=5$ より　$\boldsymbol{r=3}$<br>"
         r"(2) $|r-2|=5$，$r\gt0$ より　$\boldsymbol{r=7}$<br>"
         r"(3) $|r-2|\lt5\lt r+2$ より　$\boldsymbol{3\lt r\lt7}$<br>"
         r"(4) $5\gt r+2$ または $5\lt|r-2|$ より　$\boldsymbol{0\lt r\lt3,\ 7\lt r}$",
  "note": r"(2) で $r-2=-5$ は $r\gt0$ に反する。$C_1$ の方が大きい内接（$C_2$ が $C_1$ の内側）は $2-r=5$ で起こりえない。$d$ と半径を比べる5つの場合を図で覚えておくとよい。",
  "ex": r"円 $x^2+y^2-2x-4y+1=0$ と円 $(x+5)^2+(y-10)^2=r^2$ $(r\gt0)$ が外接・内接するときの $r$ と、2点で交わる $r$ の範囲を求めよ。",
  "exa": r"外接 $r=8$，内接 $r=12$，2点で交わる $8\lt r\lt12$"},
 {"lv": 3, "title": "2円の交点を通る直線・円（共通弦）",
  "q": r"2円 $C_1:\ x^2+y^2=5$，$C_2:\ x^2+y^2-4x-2y+3=0$ は2点で交わる。<br>(1) 2つの交点を通る直線の方程式を求めよ。　(2) 共通弦の長さを求めよ。<br>(3) 2つの交点と点 $(1,\ 1)$ を通る円の方程式を求めよ。",
  "hint": r"交点の座標を求めなくても、$k(x^2+y^2-5)+(x^2+y^2-4x-2y+3)=0$ は2交点を通る図形を表す。$k=-1$ で $x^2,\ y^2$ が消えて直線になる。",
  "sol": _F52 + r"$k(x^2+y^2-5)+(x^2+y^2-4x-2y+3)=0$　…① は、2円の交点の座標を代入すると成り立つから、2交点を通る図形を表す。<br>"
         r"(1) ① で $k=-1$ とすると $-4x-2y+8=0$。　$\boldsymbol{2x+y-4=0}$<br>"
         r"(2) $C_1$ の中心 O と直線 $2x+y-4=0$ の距離は $\dfrac4{\sqrt5}$ なので、共通弦の長さは　$2\sqrt{5-\dfrac{16}5}=2\cdot\dfrac3{\sqrt5}=\boldsymbol{\dfrac{6\sqrt5}5}$<br>"
         r"(3) ① が点 $(1,\ 1)$ を通るとき $k(1+1-5)+(1+1-4-2+3)=0$，$-3k-1=0$，$k=-\dfrac13$。<br>"
         r"① に代入して3倍すると $-(x^2+y^2-5)+3(x^2+y^2-4x-2y+3)=0$，$2x^2+2y^2-12x-6y+14=0$。<br>"
         r"　$\boldsymbol{x^2+y^2-6x-3y+7=0}$",
  "note": r"実際の交点は $(1,\ 2)$，$\left(\dfrac{11}5,\ -\dfrac25\right)$ で、(2)(3) と合う。① は $C_1$ 自身を表せない。通る点として $C_1$ 上の点（交点以外）が与えられたら、求める円は $C_1$ そのものである。本問の点 $(1,\ 1)$ は $C_1$ 上にない（$1+1\neq5$）。",
  "ex": r"2円 $x^2+y^2=10$，$x^2+y^2+2x-6y+6=0$ の2交点を通る直線、共通弦の長さ、および2交点と原点を通る円の方程式を求めよ。",
  "exa": r"$x-3y+8=0$，$\dfrac{6\sqrt{10}}5$，$4x^2+4y^2+5x-15y=0$"},
 {"lv": 3, "title": "2円の共通接線",
  "q": r"2円 $C_1:\ x^2+y^2=1$，$C_2:\ (x-3)^2+(y-4)^2=16$ の共通接線の方程式をすべて求めよ。",
  "hint": r"$C_1$ の接線は、接点を $(a,\ b)$ として $ax+by=1$（$a^2+b^2=1$）とおける。これが $C_2$ に接する条件は「$C_2$ の中心との距離 $=4$」。",
  "sol": _F53 + r"$C_1$ 上の点 $(a,\ b)$ $(a^2+b^2=1)$ における接線 $ax+by=1$ が $C_2$ に接する条件は<br>"
         r"　$\dfrac{|3a+4b-1|}{\sqrt{a^2+b^2}}=4$　すなわち　$3a+4b=5$　または　$3a+4b=-3$<br>"
         r"(i) $3a+4b=5$ のとき：$b=\dfrac{5-3a}4$ を $a^2+b^2=1$ に代入して $25a^2-30a+9=0$，$(5a-3)^2=0$，$a=\dfrac35,\ b=\dfrac45$。接線 $3x+4y=5$。<br>"
         r"(ii) $3a+4b=-3$ のとき：$a=\dfrac{-3-4b}3$ を代入して $25b^2+24b=0$，$b=0,\ -\dfrac{24}{25}$。<br>"
         r"　$b=0$ のとき $a=-1$，接線 $-x=1$ すなわち $x=-1$。$b=-\dfrac{24}{25}$ のとき $a=\dfrac7{25}$，接線 $7x-24y=25$。<br>"
         r"よって　$\boldsymbol{3x+4y=5,\ \ x=-1,\ \ 7x-24y=25}$",
  "note": r"中心間の距離 $5=1+4$ なので2円は外接し、共通接線は3本（接点での接線1本と外側の2本）。離れていれば4本、2点で交われば2本、内接で1本、内部なら0本。接線を $y=mx+n$ とおくと $x=-1$ を見落とすので、接点でおく方が安全。",
  "ex": r"2円 $x^2+y^2=1$，$(x-4)^2+(y-3)^2=16$ の共通接線の方程式をすべて求めよ。",
  "exa": r"$4x+3y=5$，$y=-1$，$24x-7y+25=0$"},
 {"lv": 4, "title": "定点を通る円の族（円束）",
  "q": r"$a$ を実数の定数とし、方程式 $x^2+y^2-2ax-4ay+10a-10=0$　…① を考える。<br>(1) ① は $a$ の値にかかわらず円を表し、2つの定点を通ることを示し、その定点を求めよ。<br>(2) ① の表す円のうち、半径が最小のものを求めよ。<br>(3) ① の表す円が $x$ 軸に接するような $a$ の値を求めよ。",
  "hint": r"(1) $a$ について整理し、$a$ の恒等式とみる。(2) 中心は $(a,\ 2a)$ で、半径の2乗は $a$ の2次式。最小の円は2定点を直径の両端とする円になるはず。",
  "sol": r"(1) $(x-a)^2+(y-2a)^2=5a^2-10a+10=5(a-1)^2+5\gt0$ なので、① はつねに円を表す。<br>"
         r"① を $a$ について整理すると $(x^2+y^2-10)-2a(x+2y-5)=0$。これがすべての $a$ で成り立つ条件は<br>"
         r"　$x^2+y^2=10$ かつ $x+2y=5$。$x=5-2y$ を代入して $5y^2-20y+15=0$，$y=1,\ 3$。<br>"
         r"よって定点は　$\boldsymbol{(3,\ 1),\ \ (-1,\ 3)}$<br>"
         r"(2) 半径の2乗 $5(a-1)^2+5$ は $a=1$ で最小値 $5$。　$\boldsymbol{(x-1)^2+(y-2)^2=5}$<br>"
         r"(3) 中心 $(a,\ 2a)$ と $x$ 軸の距離 $|2a|$ が半径に等しいから $4a^2=5a^2-10a+10$，$a^2-10a+10=0$。　$\boldsymbol{a=5\pm\sqrt{15}}$",
  "note": r"(2) の円の中心 $(1,\ 2)$ は2定点の中点で、半径 $\sqrt5$ は2定点間の距離 $2\sqrt5$ の半分。2定点を通る円の中心は2定点の垂直二等分線 $y=2x$ 上にあり、① はそのすべてを表している。",
  "ex": r"方程式 $x^2+y^2-2ax+2ay+2a-5=0$ が $a$ の値にかかわらず通る2定点と、これが表す円のうち半径が最小のものを求めよ。",
  "exa": r"$(2,\ 1)$，$(-1,\ -2)$；$\left(x-\dfrac12\right)^2+\left(y+\dfrac12\right)^2=\dfrac92$"},
]})


def _v5():
    x, y, k, a = symbols("x y k a")
    # 5.1
    def rel(d, r1, r2):
        if d > r1 + r2: return "out"
        if d == r1 + r2: return "ext"
        if d > abs(r1 - r2): return "two"
        if d == abs(r1 - r2): return "int"
        return "in"
    for r, w in [(1, "out"), (3, "ext"), (5, "two"), (7, "int"), (8, "in")]:
        assert rel(5, 2, r) == w
    assert rel(10, 2, 8) == "ext" and rel(10, 2, 12) == "int" and rel(10, 2, 9) == "two"
    assert expand((x - 1) ** 2 + (y - 2) ** 2 - 4 - (x ** 2 + y ** 2 - 2 * x - 4 * y + 1)) == 0 and (1 + 5) ** 2 + (2 - 10) ** 2 == 100
    # 5.2
    for C1, C2, line, P, circ, L in [
            (x ** 2 + y ** 2 - 5, x ** 2 + y ** 2 - 4 * x - 2 * y + 3, 2 * x + y - 4, (1, 1), x ** 2 + y ** 2 - 6 * x - 3 * y + 7, 36 * 5 / 25),
            (x ** 2 + y ** 2 - 10, x ** 2 + y ** 2 + 2 * x - 6 * y + 6, x - 3 * y + 8, (0, 0), 4 * x ** 2 + 4 * y ** 2 + 5 * x - 15 * y, 36 * 10 / 25)]:
        s = solve([C1, C2], [x, y])
        assert len(s) == 2
        for (p, q) in s:
            assert simplify(line.subs({x: p, y: q})) == 0 and simplify(circ.subs({x: p, y: q})) == 0
        assert circ.subs({x: P[0], y: P[1]}) == 0
        (a1, b1), (a2, b2) = s
        assert abs(float((a1 - a2) ** 2 + (b1 - b2) ** 2) - L) < 1e-9
    assert set(solve([x ** 2 + y ** 2 - 5, x ** 2 + y ** 2 - 4 * x - 2 * y + 3], [x, y])) == {(1, 2), (R(11, 5), R(-2, 5))}
    # 5.3 共通接線：C1 の接線を全周で調べ、C2 にも接するものを数える
    for (cx, cy), lines in [((3, 4), [(3, 4, -5), (1, 0, 1), (7, -24, -25)]), ((4, 3), [(4, 3, -5), (0, 1, 1), (24, -7, 25)])]:
        for (A, B, C) in lines:
            nrm = math.hypot(A, B)
            assert _close(abs(C) / nrm, 1) and _close(abs(A * cx + B * cy + C) / nrm, 4)
        N = 200000
        f = lambda t: math.cos(t) * cx + math.sin(t) * cy - 1 + 4
        roots = 0
        for i in range(N):
            t0, t1 = 2 * math.pi * i / N, 2 * math.pi * (i + 1) / N
            if f(t0) == 0 or f(t0) * f(t1) < 0:
                roots += 1
        # 接する所（重解）は符号変化しないので別に数える
        # g(t)=cos t・cx+sin t・cy-1 の最大値は 5-1=4（ちょうど1つの t で g=4，外側の接点の接線），g=-4 は符号変化2回
        assert roots == 2 and len(lines) == 3
    # 5.4
    e = x ** 2 + y ** 2 - 2 * a * x - 4 * a * y + 10 * a - 10
    for p in [(3, 1), (-1, 3)]:
        assert expand(e.subs({x: p[0], y: p[1]})) == 0
    assert expand(e - ((x - a) ** 2 + (y - 2 * a) ** 2 - (5 * a ** 2 - 10 * a + 10))) == 0
    assert set(solve(4 * a ** 2 - (5 * a ** 2 - 10 * a + 10), a)) == {5 - sqrt(15), 5 + sqrt(15)}
    e = x ** 2 + y ** 2 - 2 * a * x + 2 * a * y + 2 * a - 5
    for p in [(2, 1), (-1, -2)]:
        assert expand(e.subs({x: p[0], y: p[1]})) == 0
    assert expand(e - ((x - a) ** 2 + (y + a) ** 2 - (2 * a ** 2 - 2 * a + 5))) == 0
    assert (2 * a ** 2 - 2 * a + 5).subs(a, R(1, 2)) == R(9, 2)


_V.append(_v5)


# ---------------------------------------------------------------- 節6
def _tan_pts(P):
    """円 x^2+y^2=1 の外の点 P から引いた接線の接点 A, B"""
    d2 = P[0] ** 2 + P[1] ** 2
    M = (P[0] / d2, P[1] / d2)
    h = math.sqrt(1 - 1 / d2)
    u = (-P[1] / math.sqrt(d2), P[0] / math.sqrt(d2))
    return (M[0] + h * u[0], M[1] + h * u[1]), (M[0] - h * u[0], M[1] - h * u[1]), M


_F61 = _fig((-3, 10.5), (-4.6, 4.6), [
    ("circ", (6, 0), 4, "r"), ("dot", (-2, 0), "A", (-4, -5)), ("dot", (4, 0), "B", (-3, -5)), ("dot", (6, 0), "", (0, 0)),
    ("dot", (2, 0), "", (0, 0)), ("dot", (10, 0), "", (0, 0)), ("txt", (2, 0), "2", (-8, 12)), ("txt", (10, 0), "10", (-14, 12))], W=170)
_F64 = _fig((-0.6, 2.6), (-1.3, 1.3), [
    ("circ", (1, 0), 1, "r"), ("line", 0.8, -1, 0, "gd"), ("line", 1, 0.8, -2, "gd"),
    ("dot", (0, 0), "", (0, 0), True), ("dot", (2, 0), "2", (2, 12))], W=150, O=False)
_F65 = _fig((-2.4, 2.4), (-2.4, 3.4), [
    ("circ", (0, 0), 2, "b"), ("circ", (0, 1.5), 1.5, "gd"),
    ("pl", _arc(0, 1.5, 1.5, math.pi + math.asin(1 / 9), 2 * math.pi - math.asin(1 / 9), 80), "r"),
    ("dot", (0, 3), "A", (4, 3)), ("dot", (0, 0), "", (0, 0), True),
    ("dot", (math.sqrt(3 * 4 / 3 - 16 / 9), 4 / 3), "", (0, 0), True), ("dot", (-math.sqrt(3 * 4 / 3 - 16 / 9), 4 / 3), "", (0, 0), True)], W=150, O=False)
_A66, _B66 = -0.4, 1.6
_F66 = _fig((-1.8, 2.2), (-1.3, 3.0), [
    ("fn", lambda t: t * t, -1.7, 1.7, "b"), ("fn", lambda t: t * t - 1, -1.95, 1.95, "rd"),
    ("fn", lambda t: 2 * _A66 * t - _A66 ** 2, -1.8, 2.2, "g"), ("fn", lambda t: 2 * _B66 * t - _B66 ** 2, -0.2, 2.2, "g"),
    ("dot", (_A66, _A66 ** 2), "A", (-11, -2)), ("dot", (_B66, _B66 ** 2), "B", (-12, 0)),
    ("dot", ((_A66 + _B66) / 2, _A66 * _B66), "P", (3, 11))], W=160)
_P67 = (1 + math.sqrt(14) / 2, 1 - math.sqrt(14) / 2)
_A67, _B67, _M67 = _tan_pts(_P67)
_d67 = math.hypot(*_P67)
_F67 = _fig((-1.3, 3.2), (-1.3, 2.4), [
    ("circ", (0, 0), 1, "b"), ("line", 1, 1, -2, "k"),
    ("pl", _arc(0, 0, 1, -math.pi / 4, 3 * math.pi / 4, 80), "r"), ("circ", (0.5, 0.5), math.sqrt(0.5), "rd"),
    ("pl", [_A67, _P67, _B67, _A67], "g"), ("seg", (0, 0), _P67, "g"),
    ("dot", _P67, "P", (2, 11)), ("dot", _A67, "A", (-3, -5)), ("dot", _B67, "B", (4, 11)),
    ("dot", (_P67[0] / _d67, _P67[1] / _d67), "I", (5, 4)), ("dot", (2 * _M67[0], 2 * _M67[1]), "H", (-12, -2))], W=190)

SEC.append({"title": "軌跡",
"base": r"""・軌跡の求め方：① 条件を満たす点を $\mathrm{P}(x,\ y)$ とおく　② 条件を $x,\ y$ の式で表す（媒介変数があれば消去する）　③ 逆に、その図形上の点が条件を満たすか確かめ、<b>除外点・範囲</b>を決める。<br>
・2定点 A，B からの距離の比が $m:n$ $(m\neq n)$ である点の軌跡は円（アポロニウスの円）。AB を $m:n$ に内分・外分する点を直径の両端とする。<br>
・動点 Q に連動して動く点 P：P$(x,\ y)$ から Q の座標を $x,\ y$ で表し、Q の満たす式に代入する。<br>
・媒介変数 $t$ を消去するときは、$t$ が実数として存在する条件（判別式・分母 $\neq0$ など）をつねに意識する。""",
"items": [
 {"lv": 2, "title": "2定点からの距離の条件（アポロニウスの円）",
  "q": r"2点 $\mathrm{A}(-2,\ 0)$，$\mathrm{B}(4,\ 0)$ について、次の条件を満たす点 P の軌跡を求めよ。<br>(1) $\mathrm{PA}:\mathrm{PB}=2:1$　(2) $\mathrm{PA}^2+\mathrm{PB}^2=26$",
  "hint": r"$\mathrm{P}(x,\ y)$ とおく。距離の比は「$\mathrm{PA}=2\mathrm{PB}$」として両辺を2乗（両辺とも0以上なので同値）。",
  "sol": _F61 + r"$\mathrm{P}(x,\ y)$ とする。<br>"
         r"(1) $\mathrm{PA}=2\mathrm{PB}\Longleftrightarrow\mathrm{PA}^2=4\mathrm{PB}^2$ であるから<br>"
         r"　$(x+2)^2+y^2=4\{(x-4)^2+y^2\}$，$3x^2+3y^2-36x+60=0$，$(x-6)^2+y^2=16$<br>"
         r"よって　<b>中心 $\boldsymbol{(6,\ 0)}$，半径 $\boldsymbol{4}$ の円</b><br>"
         r"(2) $(x+2)^2+y^2+(x-4)^2+y^2=26$，$2x^2-4x+2y^2+20=26$，$(x-1)^2+y^2=4$<br>"
         r"よって　<b>中心 $\boldsymbol{(1,\ 0)}$，半径 $\boldsymbol{2}$ の円</b>",
  "note": r"(1) の円は AB を $2:1$ に内分する点 $(2,\ 0)$ と外分する点 $(10,\ 0)$ を直径の両端とする。式変形がすべて同値変形なので、逆の確認は不要。(2) の円の中心は AB の中点（中線定理 $\mathrm{PA}^2+\mathrm{PB}^2=2(\mathrm{PM}^2+9)$ から $\mathrm{PM}=2$）。",
  "ex": r"2点 $\mathrm{A}(0,\ 0)$，$\mathrm{B}(3,\ 0)$ について、(1) $\mathrm{PA}:\mathrm{PB}=1:2$　(2) $\mathrm{PA}^2-\mathrm{PB}^2=3$　を満たす点 P の軌跡を求めよ。",
  "exa": r"(1) 中心 $(-1,\ 0)$，半径 $2$ の円　(2) 直線 $x=2$"},
 {"lv": 2, "title": "動点に連動する点の軌跡",
  "q": r"点 Q が円 $x^2+y^2=4$ 上を動くとき、点 $\mathrm{A}(4,\ 2)$ と Q を結ぶ線分 AQ を $1:2$ に内分する点 P の軌跡を求めよ。",
  "hint": r"$\mathrm{P}(x,\ y)$，$\mathrm{Q}(s,\ t)$ とおき、$s,\ t$ を $x,\ y$ で表して $s^2+t^2=4$ に代入する（つなぎの文字を消去する）。",
  "sol": r"$\mathrm{P}(x,\ y)$，$\mathrm{Q}(s,\ t)$ とすると $s^2+t^2=4$　…①<br>"
         r"P は AQ を $1:2$ に内分するから　$x=\dfrac{2\cdot4+1\cdot s}{3}$，$y=\dfrac{2\cdot2+1\cdot t}{3}$　すなわち　$s=3x-8$，$t=3y-4$<br>"
         r"① に代入して $(3x-8)^2+(3y-4)^2=4$，両辺を $9$ で割って　$\left(x-\dfrac83\right)^2+\left(y-\dfrac43\right)^2=\dfrac49$<br>"
         r"逆にこの円上の点 P に対し $\mathrm{Q}(3x-8,\ 3y-4)$ は円 $x^2+y^2=4$ 上にある。<br>"
         r"よって　<b>中心 $\boldsymbol{\left(\dfrac83,\ \dfrac43\right)}$，半径 $\boldsymbol{\dfrac23}$ の円</b>",
  "note": r"P は A を中心として Q を $\dfrac13$ 倍に縮めた点なので、軌跡は元の円を A を中心に $\dfrac13$ 倍に縮小した円になる。中心は A と原点を結ぶ線分を $1:2$ に内分する点 $\left(\dfrac{2\cdot4+0}3,\ \dfrac{2\cdot2+0}3\right)$，半径は $2\cdot\dfrac13=\dfrac23$。",
  "ex": r"点 Q が円 $x^2+y^2=9$ 上を動くとき、2点 $\mathrm{A}(6,\ 0)$，$\mathrm{B}(0,\ 6)$ と Q を頂点とする $\triangle\mathrm{ABQ}$ の重心 G の軌跡を求めよ。",
  "exa": r"中心 $(2,\ 2)$，半径 $1$ の円（直線 AB は円 $x^2+y^2=9$ と交わらないので除外点はない）"},
 {"lv": 3, "title": "放物線の頂点の軌跡（範囲の制限）",
  "q": r"$t$ を実数とし、放物線 $y=x^2-2(t+1)x+3t^2$ の頂点を P とする。<br>(1) $t$ が実数全体を動くとき、P の軌跡を求めよ。<br>(2) この放物線が $x$ 軸と異なる2点で交わるように $t$ が動くとき、P の軌跡を求めよ。",
  "hint": r"頂点を $(X,\ Y)$ とし $t$ を消去する。(2) では $t$ の範囲を $X$ の範囲に読みかえる。$X=t+1$ のように $t$ と $X$ が1対1に対応することを確認する。",
  "sol": r"$y=\{x-(t+1)\}^2+3t^2-(t+1)^2=\{x-(t+1)\}^2+2t^2-2t-1$ より　$\mathrm{P}(t+1,\ 2t^2-2t-1)$<br>"
         r"(1) $X=t+1$，$Y=2t^2-2t-1$ とおく。$t=X-1$ を代入して $Y=2(X-1)^2-2(X-1)-1=2X^2-6X+3$。<br>"
         r"$t$ が実数全体を動くと $X$ も実数全体を動くから　<b>放物線 $\boldsymbol{y=2x^2-6x+3}$</b><br>"
         r"(2) 条件は $\dfrac D4=(t+1)^2-3t^2\gt0$，すなわち $2t^2-2t-1\lt0$，$\dfrac{1-\sqrt3}2\lt t\lt\dfrac{1+\sqrt3}2$。<br>"
         r"$X=t+1$ より $\dfrac{3-\sqrt3}2\lt X\lt\dfrac{3+\sqrt3}2$。<br>"
         r"よって　<b>放物線 $\boldsymbol{y=2x^2-6x+3}$ の $\boldsymbol{\dfrac{3-\sqrt3}2\lt x\lt\dfrac{3+\sqrt3}2}$ の部分</b>",
  "note": r"(2) の条件は「頂点の $y$ 座標が負」と同じなので、答えは軌跡の放物線のうち $y\lt0$ の部分といってもよい（$2x^2-6x+3\lt0$ を解くと一致する）。媒介変数の範囲を必ず軌跡の範囲に反映させる。",
  "ex": r"放物線 $y=x^2+2tx+2t+3$ が $x$ 軸と共有点をもたないように実数 $t$ が動くとき、頂点の軌跡を求めよ。",
  "exa": r"放物線 $y=-x^2-2x+3$ の $-3\lt x\lt1$ の部分"},
 {"lv": 3, "title": "2直線の交点の軌跡（除外点）",
  "q": r"$t$ が実数全体を動くとき、2直線 $\ell:\ tx-y=0$，$m:\ x+ty-2=0$ の交点 P の軌跡を求めよ。",
  "hint": r"点 $(X,\ Y)$ が軌跡上にある $\Longleftrightarrow$ 「$tX-Y=0$ かつ $X+tY-2=0$ を満たす実数 $t$ が存在する」。$t=\dfrac YX$ と割るときは $X=0$ の場合を別に調べる。",
  "sol": _F64 + r"点 $(X,\ Y)$ が軌跡上にあるのは、$tX-Y=0$　…①，$X+tY-2=0$　…② を満たす実数 $t$ が存在するときである。<br>"
         r"$X=0$ のとき、① より $Y=0$ となり、② は $-2=0$ で成り立たない。よって $X\neq0$。<br>"
         r"$X\neq0$ のとき、① より $t=\dfrac YX$。② に代入して $X+\dfrac{Y^2}X-2=0$，すなわち $X^2+Y^2-2X=0$　…③<br>"
         r"逆に、③ を満たし $X\neq0$ である点に対して $t=\dfrac YX$ とおけば ①，② が成り立つ。<br>"
         r"よって　<b>円 $\boldsymbol{(x-1)^2+y^2=1}$，ただし原点 $\boldsymbol{(0,\ 0)}$ を除く</b>",
  "note": r"$\ell$ は原点を、$m$ は点 $(2,\ 0)$ を通り、$t\cdot1+(-1)\cdot t=0$ より $\ell\perp m$。よって P は原点と $(2,\ 0)$ を直径の両端とする円周上にある（直径に対する円周角は直角）。$\ell$ は $y$ 軸 $x=0$ を，$m$ は $x$ 軸 $y=0$ を表せないので、この2直線の交点である原点が除かれる。",
  "ex": r"$t$ が実数全体を動くとき、2直線 $tx-y-t=0$，$x+ty-3t=0$ の交点の軌跡を求めよ。",
  "exa": r"円 $x^2+y^2-x-3y=0$，ただし点 $(1,\ 3)$ を除く"},
 {"lv": 3, "title": "弦の中点の軌跡",
  "q": r"点 $\mathrm{A}(0,\ 3)$ を通る傾き $m$ の直線 $\ell$ が、円 $C:\ x^2+y^2=4$ と異なる2点 P，Q で交わるとき、線分 PQ の中点 M の軌跡を求めよ。",
  "hint": r"$\ell:\ y=mx+3$ を代入した2次方程式の解と係数の関係で M を $m$ で表し、$m$ を消去する。$m$ の範囲（判別式 $\gt0$）を M の範囲に直すのを忘れない。",
  "sol": _F65 + r"$y=mx+3$ を代入して　$(1+m^2)x^2+6mx+5=0$　…①<br>"
         r"異なる2点で交わる条件は $\dfrac D4=9m^2-5(1+m^2)=4m^2-5\gt0$，すなわち $m^2\gt\dfrac54$　…②<br>"
         r"$\mathrm{M}(X,\ Y)$ とすると、① の2解の和から　$X=-\dfrac{3m}{1+m^2}$，$Y=mX+3=\dfrac3{1+m^2}$　…③<br>"
         r"③ より $Y\gt0$ で、$X=-mY$ から $m=-\dfrac XY$。これを $Y(1+m^2)=3$ に代入して $Y+\dfrac{X^2}Y=3$，すなわち $X^2+Y^2=3Y$　…④<br>"
         r"② は $\dfrac{X^2}{Y^2}\gt\dfrac54$。④ より $X^2=3Y-Y^2$ なので $\dfrac{3Y-Y^2}{Y^2}\gt\dfrac54$，$\dfrac3Y\gt\dfrac94$，$0\lt Y\lt\dfrac43$。<br>"
         r"逆に ④ と $0\lt Y\lt\dfrac43$ を満たす点に対し $m=-\dfrac XY$ とおくと ②，③ が成り立つ。<br>"
         r"よって　<b>円 $\boldsymbol{x^2+\left(y-\dfrac32\right)^2=\dfrac94}$ の $\boldsymbol{0\lt y\lt\dfrac43}$ の部分</b>（図の赤線）",
  "note": r"図形的には $\mathrm{OM}\perp\mathrm{AM}$ なので M は OA を直径とする円上にあり、そのうち円 $C$ の内部の部分（2円の交点は $y=\dfrac43$）。$y$ 軸（傾きなし）は $\ell$ に含めていないので、そのときの中点 O は除かれる。",
  "ex": r"点 $\mathrm{A}(2,\ 0)$ を通る傾き $m$ の直線が円 $x^2+y^2=1$ と異なる2点で交わるとき、その2点を結ぶ線分の中点の軌跡を求めよ。",
  "exa": r"円 $(x-1)^2+y^2=1$ の $0\leqq x\lt\dfrac12$ の部分"},
 {"lv": 4, "title": "放物線の2接線の交点の軌跡",
  "q": r"放物線 $C:\ y=x^2$ 上の2点 $\mathrm{A}(\alpha,\ \alpha^2)$，$\mathrm{B}(\beta,\ \beta^2)$ $(\alpha\lt\beta)$ における $C$ の接線の交点を P とする。<br>(1) A における接線の方程式と、P の座標を $\alpha,\ \beta$ で表せ。<br>(2) $\triangle\mathrm{PAB}$ の面積が $2$ となるように A，B が動くとき、P の軌跡を求めよ。",
  "hint": r"(1) 放物線と直線が接する $\Longleftrightarrow$ 連立した2次方程式が重解をもつ。(2) 面積を $\alpha,\ \beta$ で表すと $\beta-\alpha$ だけで決まる。P の座標は $\alpha+\beta$，$\alpha\beta$ で表せるので、$(\beta-\alpha)^2=(\alpha+\beta)^2-4\alpha\beta$ で結ぶ。",
  "sol": _F66 + r"(1) 直線 $y=2\alpha x-\alpha^2$ と $C$ を連立すると $x^2-2\alpha x+\alpha^2=0$，$(x-\alpha)^2=0$ で重解 $x=\alpha$ をもつから、これが A における接線。<br>"
         r"同様に B における接線は $y=2\beta x-\beta^2$。辺々引いて $2(\alpha-\beta)x=\alpha^2-\beta^2$，$\alpha\neq\beta$ より $x=\dfrac{\alpha+\beta}2$，$y=\alpha\beta$。<br>"
         r"　$\boldsymbol{y=2\alpha x-\alpha^2}$，$\boldsymbol{\mathrm{P}\left(\dfrac{\alpha+\beta}2,\ \alpha\beta\right)}$<br>"
         r"(2) P を原点に移すと A，B はそれぞれ $\left(\dfrac{\alpha-\beta}2,\ \alpha(\alpha-\beta)\right)$，$\left(\dfrac{\beta-\alpha}2,\ \beta(\beta-\alpha)\right)$ に移る。よって<br>"
         r"　$\triangle\mathrm{PAB}=\dfrac12\left|\dfrac{\alpha-\beta}2\cdot\beta(\beta-\alpha)-\alpha(\alpha-\beta)\cdot\dfrac{\beta-\alpha}2\right|=\dfrac12\cdot\dfrac{(\beta-\alpha)^2|\alpha-\beta|}2=\dfrac{(\beta-\alpha)^3}4$<br>"
         r"これが $2$ なので $(\beta-\alpha)^3=8$，$\beta-\alpha=2$。<br>"
         r"$\mathrm{P}(X,\ Y)$ とすると $\alpha+\beta=2X$，$\alpha\beta=Y$ で、$(\beta-\alpha)^2=(\alpha+\beta)^2-4\alpha\beta$ より $4=4X^2-4Y$，$Y=X^2-1$。<br>"
         r"逆に、任意の実数 $X$ に対し $\alpha=X-1$，$\beta=X+1$ とすれば $\beta-\alpha=2$ で、P は $(X,\ X^2-1)$ となる。<br>"
         r"よって　<b>放物線 $\boldsymbol{y=x^2-1}$</b>",
  "note": r"2接線が直交する条件は $2\alpha\cdot2\beta=-1$，すなわち $Y=\alpha\beta=-\dfrac14$ で、P の軌跡は直線 $y=-\dfrac14$（放物線の準線）になる。微分を使わず「重解」で接線を求められることは、数学IIの範囲で放物線の接線を扱う基本である。",
  "ex": r"上の設定で、線分 AB の中点を M とする。$\mathrm{PM}=1$ となるように A，B が動くとき、P の軌跡を求めよ。",
  "exa": r"放物線 $y=x^2-\dfrac12$（$\mathrm{PM}=\dfrac{(\beta-\alpha)^2}2$ より）"},
 {"lv": 5, "title": "円外の点から引いた2接線がつくる三角形の内心・垂心の軌跡",
  "q": r"円 $C:\ x^2+y^2=1$ と直線 $\ell:\ x+y=2$ がある。$\ell$ 上の点 P から $C$ に2本の接線を引き、接点を A，B とする。P が $\ell$ 上を動くとき、次の点の軌跡を求めよ。<br>(1) $\triangle\mathrm{PAB}$ の内心 I　　(2) $\triangle\mathrm{PAB}$ の垂心 H",
  "hint": r"直接計算すると大変。図形の性質を見抜く：(1) 線分 OP と $C$ の交点が3辺から等距離になる（内心の候補）。(2) $\mathrm{AH}\perp\mathrm{PB}$，$\mathrm{OB}\perp\mathrm{PB}$ から $\mathrm{AH}\parallel\mathrm{OB}$。同様に $\mathrm{BH}\parallel\mathrm{OA}$ で、OAHB は平行四辺形。あとは「P を表す式に代入する」逆像の考え方で軌跡を出す。",
  "sol": _F67 + r"$\mathrm{P}(p,\ 2-p)$，$d=\mathrm{OP}$ とおく。$d^2=2(p-1)^2+2\geqq2$ より P はつねに $C$ の外部にある。<br>"
         r"接点を結ぶ直線 AB は、円と直線の節で見たように $px+(2-p)y=1$。O から AB に下ろした垂線の足は AB の中点 M で、$\mathrm{M}\left(\dfrac p{d^2},\ \dfrac{2-p}{d^2}\right)$（O，M，P は一直線上で $\mathrm{OM}=\dfrac1d$）。<br>"
         r"(1) 線分 OP と $C$ の交点を $\mathrm{I_0}\left(\dfrac pd,\ \dfrac{2-p}d\right)$ とする。<br>"
         r"・$\mathrm{I_0}$ と直線 AB の距離：$\dfrac{|p^2/d+(2-p)^2/d-1|}{d}=\dfrac{d-1}d$<br>"
         r"・$\mathrm{A}(a_1,\ a_2)$ における接線 $a_1x+a_2y=1$ は P を通るので $a_1p+a_2(2-p)=1$。よって $\mathrm{I_0}$ との距離は $\left|\dfrac{a_1p+a_2(2-p)}d-1\right|=\dfrac{d-1}d$。B における接線についても同じ。<br>"
         r"また $\mathrm{OM}=\dfrac1d\lt1=\mathrm{OI_0}\lt d=\mathrm{OP}$ より、$\mathrm{I_0}$ は辺 AB の中点 M と頂点 P を結ぶ線分上（端を除く）にあり、三角形の内部にある。内部にあって3辺から等距離の点は内心だから $\mathrm{I}=\mathrm{I_0}$。<br>"
         r"$\mathrm{I}(X,\ Y)$ とすると $X^2+Y^2=1$，$X+Y=\dfrac2d\gt0$。逆に $X^2+Y^2=1$，$X+Y\gt0$ を満たす点に対し $\mathrm{P}\left(\dfrac{2X}{X+Y},\ \dfrac{2Y}{X+Y}\right)$ は $\ell$ 上の点で、$d=\dfrac2{X+Y}$ となり I がこの点に一致する。<br>"
         r"よって　<b>円 $\boldsymbol{x^2+y^2=1}$ の $\boldsymbol{x+y\gt0}$ の部分</b><br>"
         r"(2) $\mathrm{PA}=\mathrm{PB}$ である。$\mathrm{AH}\perp\mathrm{PB}$，$\mathrm{OB}\perp\mathrm{PB}$（半径と接線）より $\mathrm{AH}\parallel\mathrm{OB}$。同様に $\mathrm{BH}\parallel\mathrm{OA}$。O，A，B は一直線上にないから四角形 OAHB は平行四辺形で、対角線 OH の中点は AB の中点 M と一致する。<br>"
         r"よって $\mathrm{H}=\left(\dfrac{2p}{d^2},\ \dfrac{2(2-p)}{d^2}\right)$。$\mathrm{H}(X,\ Y)$ とすると $X^2+Y^2=\dfrac4{d^2}$，$X+Y=\dfrac4{d^2}$ なので $X^2+Y^2=X+Y$ かつ $(X,\ Y)\neq(0,\ 0)$。<br>"
         r"逆に $X^2+Y^2=X+Y$，$(X,\ Y)\neq(0,\ 0)$ のとき、$X+Y=X^2+Y^2\gt0$ で、$\mathrm{P}\left(\dfrac{2X}{X^2+Y^2},\ \dfrac{2Y}{X^2+Y^2}\right)$ は $\ell$ 上にあり、$d^2=\dfrac4{X^2+Y^2}$ から H がこの点に一致する。<br>"
         r"よって　<b>円 $\boldsymbol{\left(x-\dfrac12\right)^2+\left(y-\dfrac12\right)^2=\dfrac12}$，ただし原点を除く</b>",
  "note": r"(1) の事実「内心は弧 AB の中点」は接弦定理からも示せる。(2) の関係 $\mathrm{H}=2\mathrm{M}$，$\mathrm{M}=\dfrac{\mathrm{P}}{d^2}$ は、「P と M は O を中心とする円 $C$ に関して互いに反転の位置にある」ことを表す。直線 $\ell$ を反転すると原点を通る円になる、というのが (2) の答えの背景である。図の赤い実線が I の軌跡、赤い破線が H の軌跡。",
  "ex": r"円 $x^2+y^2=1$ と直線 $y=2$ 上の点 P について、P から円に引いた2接線の接点を A，B とする。P が直線 $y=2$ 上を動くとき、$\triangle\mathrm{PAB}$ の内心と垂心の軌跡を求めよ。",
  "exa": r"内心：円 $x^2+y^2=1$ の $y\gt0$ の部分，垂心：円 $x^2+\left(y-\dfrac12\right)^2=\dfrac14$（原点を除く）"},
]})


def _incenter(A, B, C):
    a, b, c = math.dist(B, C), math.dist(C, A), math.dist(A, B)
    s = a + b + c
    return ((a * A[0] + b * B[0] + c * C[0]) / s, (a * A[1] + b * B[1] + c * C[1]) / s)


def _ortho(A, B, C):
    # (H-A)・(C-B)=0, (H-B)・(C-A)=0
    a1, b1, c1 = C[0] - B[0], C[1] - B[1], A[0] * (C[0] - B[0]) + A[1] * (C[1] - B[1])
    a2, b2, c2 = C[0] - A[0], C[1] - A[1], B[0] * (C[0] - A[0]) + B[1] * (C[1] - A[1])
    det = a1 * b2 - a2 * b1
    return ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)


def _v6():
    x, y, t = symbols("x y t")
    rnd = random.Random(11)
    # 6.1
    assert expand((x + 2) ** 2 + y ** 2 - 4 * ((x - 4) ** 2 + y ** 2) + 3 * ((x - 6) ** 2 + y ** 2 - 16)) == 0
    assert expand((x + 2) ** 2 + y ** 2 + (x - 4) ** 2 + y ** 2 - 26 - 2 * ((x - 1) ** 2 + y ** 2 - 4)) == 0
    assert expand(4 * (x ** 2 + y ** 2) - ((x - 3) ** 2 + y ** 2) - 3 * ((x + 1) ** 2 + y ** 2 - 4)) == 0
    assert expand(x ** 2 + y ** 2 - (x - 3) ** 2 - y ** 2 - 3 - 6 * (x - 2)) == 0
    # 6.2
    s, u = 3 * x - 8, 3 * y - 4
    assert expand(s ** 2 + u ** 2 - 4 - 9 * ((x - R(8, 3)) ** 2 + (y - R(4, 3)) ** 2 - R(4, 9))) == 0
    assert expand((3 * x - 6) ** 2 + (3 * y - 6) ** 2 - 9 - 9 * ((x - 2) ** 2 + (y - 2) ** 2 - 1)) == 0
    assert 6 / math.sqrt(2) > 3
    # 6.3
    e = x ** 2 - 2 * (t + 1) * x + 3 * t ** 2
    assert expand(e - ((x - (t + 1)) ** 2 + 2 * t ** 2 - 2 * t - 1)) == 0
    assert expand((2 * t ** 2 - 2 * t - 1) - (2 * (t + 1) ** 2 - 6 * (t + 1) + 3)) == 0
    rts = solve(2 * t ** 2 - 2 * t - 1, t)
    assert set(simplify(r + 1) for r in rts) == {(3 - sqrt(3)) / 2, (3 + sqrt(3)) / 2}
    e = x ** 2 + 2 * t * x + 2 * t + 3
    assert expand(e - ((x + t) ** 2 - t ** 2 + 2 * t + 3)) == 0
    assert expand((-t ** 2 + 2 * t + 3) - (-(-t) ** 2 - 2 * (-t) + 3)) == 0 and set(solve(-t ** 2 + 2 * t + 3, t)) == {-1, 3}
    # 6.4
    for _ in range(300):
        tt = rnd.uniform(-20, 20)
        X = 2 / (1 + tt * tt); Y = tt * X      # ℓ: y=tx, m: x+ty=2
        assert abs(tt * X - Y) < 1e-12 and abs(X + tt * Y - 2) < 1e-12 and abs((X - 1) ** 2 + Y ** 2 - 1) < 1e-12
        th = rnd.uniform(0.01, 2 * math.pi - 0.01)
        X, Y = 1 + math.cos(th + math.pi), math.sin(th + math.pi)
        if abs(X) > 1e-9:
            tt = Y / X
            assert abs(X + tt * Y - 2) < 1e-9
        # 練習：tx-y-t=0, x+ty-3t=0
        tt = rnd.uniform(-20, 20)
        sol = solve([tt * x - y - tt, x + tt * y - 3 * tt], [x, y])
        X, Y = float(sol[x]), float(sol[y])
        assert abs(X ** 2 + Y ** 2 - X - 3 * Y) < 1e-9 and math.dist((X, Y), (1, 3)) > 1e-6
    # (1,3) には到達しない：x=1 なら ℓ から y=0
    assert all(abs(tt * 1 - 3 - tt) > 0 for tt in [rnd.uniform(-9, 9) for _ in range(50)])
    # 6.5
    for _ in range(300):
        m = rnd.choice([-1, 1]) * rnd.uniform(math.sqrt(1.25) + 1e-6, 30)
        a, b, c = 1 + m * m, 6 * m, 5
        D = b * b - 4 * a * c
        x1, x2 = (-b + math.sqrt(D)) / (2 * a), (-b - math.sqrt(D)) / (2 * a)
        X = (x1 + x2) / 2; Y = m * X + 3
        assert abs(X * X + Y * Y - 3 * Y) < 1e-9 and 0 < Y < 4 / 3
        Y = rnd.uniform(1e-4, 4 / 3 - 1e-4); X = rnd.choice([-1, 1]) * math.sqrt(3 * Y - Y * Y)
        m = -X / Y
        assert m * m > 1.25 and abs(3 / (1 + m * m) - Y) < 1e-9
        # 練習
        m = rnd.uniform(-1 / math.sqrt(3) + 1e-6, 1 / math.sqrt(3) - 1e-6)
        a, b, c = 1 + m * m, -4 * m * m, 4 * m * m - 1
        D = b * b - 4 * a * c
        assert D > 0
        X = -b / (2 * a); Y = m * (X - 2)
        assert abs((X - 1) ** 2 + Y ** 2 - 1) < 1e-9 and 0 <= X < 0.5
    # 6.6
    for _ in range(300):
        al = rnd.uniform(-5, 5); be = al + rnd.uniform(0.01, 5)
        P = ((al + be) / 2, al * be)
        assert abs(2 * al * P[0] - al * al - P[1]) < 1e-9 and abs(2 * be * P[0] - be * be - P[1]) < 1e-9
        A, B = (al, al * al), (be, be * be)
        S = abs((A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0])) / 2
        assert abs(S - (be - al) ** 3 / 4) < 1e-7 * max(1, S)
        al = rnd.uniform(-5, 5); be = al + 2
        assert abs(al * be - (((al + be) / 2) ** 2 - 1)) < 1e-9
        al = rnd.uniform(-5, 5); be = al + math.sqrt(2)
        M = ((al + be) / 2, (al * al + be * be) / 2)
        assert abs(M[1] - al * be - 1) < 1e-9 and abs(al * be - (((al + be) / 2) ** 2 - 0.5)) < 1e-9
    # 6.7 内心・垂心（数値で直接計算して確認）
    for line in ["x+y=2", "y=2"]:
        for _ in range(300):
            p = rnd.uniform(-30, 30)
            P = (p, 2 - p) if line == "x+y=2" else (p, 2.0)
            A, B, M = _tan_pts(P)
            for Q in (A, B):
                assert abs(Q[0] ** 2 + Q[1] ** 2 - 1) < 1e-9 and abs(Q[0] * P[0] + Q[1] * P[1] - 1) < 1e-9
            I = _incenter(P, A, B)
            H = _ortho(P, A, B)
            d = math.hypot(*P)
            assert math.dist(I, (P[0] / d, P[1] / d)) < 1e-8 and abs(I[0] ** 2 + I[1] ** 2 - 1) < 1e-8
            assert math.dist(H, (2 * M[0], 2 * M[1])) < 1e-8
            if line == "x+y=2":
                assert I[0] + I[1] > 0 and abs(H[0] ** 2 + H[1] ** 2 - H[0] - H[1]) < 1e-9
            else:
                assert I[1] > 0 and abs(H[0] ** 2 + H[1] ** 2 - H[1]) < 1e-9
        # 逆：軌跡上の点が実現される
        for _ in range(200):
            th = rnd.uniform(-math.pi / 4 + 1e-3, 3 * math.pi / 4 - 1e-3)
            X, Y = math.cos(th), math.sin(th)
            if line == "x+y=2":
                P = (2 * X / (X + Y), 2 * Y / (X + Y))
                assert abs(P[0] + P[1] - 2) < 1e-9
                A, B, M = _tan_pts(P)
                assert math.dist(_incenter(P, A, B), (X, Y)) < 1e-7
            hx, hy = 0.5 + math.sqrt(0.5) * math.cos(4 * th), 0.5 + math.sqrt(0.5) * math.sin(4 * th)
            if math.hypot(hx, hy) > 1e-3 and line == "x+y=2":
                P = (2 * hx / (hx * hx + hy * hy), 2 * hy / (hx * hx + hy * hy))
                assert abs(P[0] + P[1] - 2) < 1e-7
                A, B, M = _tan_pts(P)
                assert math.dist(_ortho(P, A, B), (hx, hy)) < 1e-6


_V.append(_v6)


# ---------------------------------------------------------------- 節7
_s5 = math.sqrt(5)
_F71 = _fig((-0.8, 4.6), (-2.4, 2.6), [
    ("fill", [_arc(2, 0, 2, math.atan2(-2 / _s5, 4 / _s5), math.atan2(2 / _s5, -4 / _s5))]),
    ("circ", (2, 0), 2, "b"), ("line", 1, 2, -2, "bd"),
    ("dot", (2 - 4 / _s5, 2 / _s5), "", (0, 0), True), ("dot", (2 + 4 / _s5, -2 / _s5), "", (0, 0), True),
    ("dot", (4, 0), "4", (2, 12)), ("txt", (0, 1), "1", (-9, 4))], W=170)
_th72 = math.atan2(1.6, 1.2)
_F72a = _fig((-3.2, 3.2), (-2.6, 3.2), [
    ("fill", [_arc(0, 0, 2, math.pi, 2 * math.pi + _th72)]),
    ("fill", [[(-3.2, -0.6), (3.2, 2.6), (3.2, 3.2), (-3.2, 3.2)], _arc(0, 0, 2, _th72, math.pi)]),
    ("circ", (0, 0), 2, "bd"), ("line", 1, -2, 2, "bd"),
    ("dot", (-2, 0), "", (0, 0), True), ("dot", (1.2, 1.6), "", (0, 0), True), ("txt", (-3.1, 3.0), "(1)", (0, 4))], W=140)
_F72b = _fig((-2.6, 2.6), (-1.6, 3.6), [
    ("fill", [[(2, 1), (0, 3), (-2, 1), (0, -1)]]), ("pl", [(2, 1), (0, 3), (-2, 1), (0, -1), (2, 1)], "b"),
    ("txt", (2, 1), "2", (-2, 12)), ("txt", (0, 3), "3", (4, 4)), ("txt", (0, -1), "−1", (4, 8)), ("txt", (-2.5, 3.4), "(2)", (0, 4))], W=120)
_F73 = _fig((-0.8, 6.6), (-0.8, 6.4), [
    ("fill", [[(0, 0), (5, 0), (4, 3), (0, 5)]]), ("pl", [(0, 0), (5, 0), (4, 3), (0, 5), (0, 0)], "b"),
    ("line", 2, 3, -17, "rd"), ("dot", (4, 3), "(4, 3)", (4, -3)), ("txt", (5, 0), "5", (-3, 12)), ("txt", (0, 5), "5", (-9, 4))], W=160)
_F74 = _fig((-0.6, 5.6), (-0.8, 4.8), [
    ("fill", [_arc(3, 2, 2, 0, 2 * math.pi)]), ("circ", (3, 2), 2, "b"), ("line", 12, -5, 0, "rd"),
    ("seg", (0, 0), (3 * (1 + 2 / math.sqrt(13)), 2 * (1 + 2 / math.sqrt(13))), "gd"),
    ("dot", (15 / 13, 36 / 13), "", (0, 0)), ("dot", (3, 0), "", (0, 0)), ("dot", (3, 2), "", (0, 0))], W=150)
_F76 = _fig((-1.8, 1.8), (-0.4, 1.8), [
    ("fill", [_fp(lambda t: t * t, -1, 1, 60) + _arc(0, 0, math.sqrt(2), math.pi / 4, 3 * math.pi / 4, 60)]),
    ("fn", lambda t: t * t, -1.3, 1.3, "g"), ("circ", (0, 0), math.sqrt(2), "g"),
    ("pl", _fp(lambda t: t * t, -1, 1, 60) + _arc(0, 0, math.sqrt(2), math.pi / 4, 3 * math.pi / 4, 60), "b"),
    ("dot", (-1, 1), "(−1, 1)", (-38, -3)), ("dot", (1, 1), "(1, 1)", (5, 4))], W=170)
_F77 = _fig((-1.6, 1.6), (-1.5, 1.4), [
    ("fill", [_arc(0, 0, 1, 0, 2 * math.pi)]), ("circ", (0, 0), 1, "b"),
    ("fn", lambda t: t * t - 1.25, -1.6, 1.6, "r"), ("fn", lambda t: t * t - 1, -1.6, 1.6, "gd"),
    ("dot", (math.sqrt(3) / 2, -0.5), "", (0, 0)), ("dot", (-math.sqrt(3) / 2, -0.5), "", (0, 0))], W=150)
_F78 = _fig((-2.5, 0.7), (-0.9, 1.0), [
    ("fill", [_fp(lambda a: a * a / 4 - 0.5, -2, 0, 60) + [(-1, 0.5)]]),
    ("pl", _fp(lambda a: a * a / 4 - 0.5, -2, 0, 60) + [(-1, 0.5), (-2, 0.5)], "b"),
    ("fn", lambda a: a * a / 4 - 0.5, -2.5, 0.7, "gd"),
    ("dot", (-2, 0.5), "(−2, ½)", (-14, -6)), ("dot", (-1, 0.5), "(−1, ½)", (0, -6)), ("dot", (0, -0.5), "(0, −½)", (4, 10)),
    ("dot", (-1, 0.125), "", (0, 0))], W=200, lab=("a", "b"))

SEC.append({"title": "不等式の表す領域",
"base": r"""・$y\gt f(x)$：曲線 $y=f(x)$ の上側，$y\lt f(x)$：下側。$(x-a)^2+(y-b)^2\lt r^2$：円の内部，$\gt$：外部。等号を含めば境界も含む。<br>
・$AB\gt0\Longleftrightarrow(A\gt0$ かつ $B\gt0)$ または $(A\lt0$ かつ $B\lt0)$。境界をまたぐたびに符号が変わる。<br>
・領域 $D$ 上での $f(x,\ y)$ の最大最小：$f(x,\ y)=k$ とおき、図形 $f=k$ が $D$ と共有点をもつ $k$ の範囲を調べる（1次式なら直線の平行移動，$\dfrac yx$ なら傾き，$x^2+y^2$ なら原点中心の円）。<br>
・命題「$p\Rightarrow q$」が真 $\Longleftrightarrow$ $p$ の表す領域 $\subset$ $q$ の表す領域。""",
"items": [
 {"lv": 1, "title": "不等式の表す領域（直線と円）",
  "q": r"連立不等式 $\begin{cases}x+2y\gt2\\ x^2+y^2-4x\leqq0\end{cases}$ の表す領域を図示せよ。",
  "hint": r"それぞれの不等式の表す領域を求め、共通部分をとる。境界線を含むかどうかを必ず明示する。",
  "sol": _F71 + r"$x+2y\gt2 \Longleftrightarrow y\gt-\dfrac12x+1$：直線 $y=-\dfrac12x+1$ の上側。<br>"
         r"$x^2+y^2-4x\leqq0 \Longleftrightarrow (x-2)^2+y^2\leqq4$：中心 $(2,\ 0)$，半径 $2$ の円の周および内部。<br>"
         r"求める領域はこれらの共通部分で、<b>図の網目部分</b>。ただし境界は、<b>円周上の点は含み、直線上の点は含まない</b>（2つの交点も含まない）。",
  "note": r"円と直線の交点は $\left(2\mp\dfrac{4\sqrt5}5,\ \pm\dfrac{2\sqrt5}5\right)$（複号同順）。図示の問題では、境界を含むかどうかと、交点（白丸か黒丸か）を答えに書き添える。",
  "ex": r"連立不等式 $y\leqq x+1$，$x^2+y^2\lt9$ の表す領域を図示せよ。",
  "exa": r"円 $x^2+y^2=9$ の内部のうち、直線 $y=x+1$ およびその下側の部分（円周上の点は含まず、直線上の点は円の内部にあるものを含む）"},
 {"lv": 2, "title": "積の形・絶対値を含む不等式の表す領域",
  "q": r"次の不等式の表す領域を図示せよ。<br>(1) $(x-2y+2)(x^2+y^2-4)\lt0$　(2) $|x|+|y-1|\leqq2$",
  "hint": r"(1) 積が負 $\Longleftrightarrow$ 2つの因数が異符号。2つの場合の和集合になる。(2) $x\geqq0$ か，$y\geqq1$ かで4つに場合分けして絶対値をはずす。",
  "sol": _F72b + _F72a + r"(1) $x-2y+2\gt0 \Longleftrightarrow y\lt\dfrac12x+1$（直線の下側），$x^2+y^2-4\lt0$ は円 $x^2+y^2=4$ の内部。与えられた不等式は<br>"
         r"　「$y\lt\dfrac12x+1$ かつ $x^2+y^2\lt4$」または「$y\gt\dfrac12x+1$ かつ $x^2+y^2\gt4$」<br>"
         r"と同値で、<b>図の網目部分</b>（境界はすべて含まない）。直線と円の交点は $(-2,\ 0)$，$\left(\dfrac65,\ \dfrac85\right)$。<br>"
         r"(2) $x\geqq0,\ y\geqq1$ のとき $x+y-1\leqq2$，すなわち $y\leqq-x+3$。<br>"
         r"$x\geqq0,\ y\lt1$ のとき $x-y+1\leqq2$，すなわち $y\geqq x-1$。<br>"
         r"$x\lt0,\ y\geqq1$ のとき $y\leqq x+3$。$x\lt0,\ y\lt1$ のとき $y\geqq-x-1$。<br>"
         r"よって　<b>4点 $\boldsymbol{(2,\ 1),\ (0,\ 3),\ (-2,\ 1),\ (0,\ -1)}$ を頂点とする正方形の周および内部</b>",
  "note": r"(2) は $|x|+|y|\leqq2$ の表す正方形を $y$ 軸方向に $1$ 平行移動したもの。$|x|+|y|\leqq2$ は $x\to-x$，$y\to-y$ で不変なので、第1象限の部分を描いて折り返せばよい。",
  "ex": r"次の不等式の表す領域を図示せよ。(1) $(x-y)(x^2+y^2-1)\geqq0$　(2) $|x-1|+|y|\leqq1$",
  "exa": r"(1) 円 $x^2+y^2=1$ の外部で直線 $y=x$ の下側の部分と、円の内部で直線の上側の部分（境界を含む）　(2) 4点 $(0,\ 0),\ (1,\ 1),\ (2,\ 0),\ (1,\ -1)$ を頂点とする正方形の周および内部"},
 {"lv": 2, "title": "領域における1次式の最大・最小（線形計画法）",
  "q": r"$x,\ y$ が4つの不等式 $x\geqq0$，$y\geqq0$，$x+2y\leqq10$，$3x+y\leqq15$ を満たすとき、$2x+3y$ の最大値と最小値を求めよ。",
  "hint": r"$2x+3y=k$ とおくと、傾き $-\dfrac23$，$y$ 切片 $\dfrac k3$ の直線。これが領域と共有点をもつ範囲で平行移動し、$y$ 切片の最大・最小を見る。",
  "sol": _F73 + r"領域 $D$ は4点 $(0,\ 0)$，$(5,\ 0)$，$(4,\ 3)$，$(0,\ 5)$ を頂点とする四角形の周および内部（$(4,\ 3)$ は $x+2y=10$ と $3x+y=15$ の交点）。<br>"
         r"$2x+3y=k$　…① は傾き $-\dfrac23$ の直線で、$k$ は $y$ 切片の3倍。境界の直線の傾き $-\dfrac12$，$-3$ と比べて $-3\lt-\dfrac23\lt-\dfrac12$ だから、① が $D$ と共有点をもつ範囲で $y$ 切片が最大になるのは ① が点 $(4,\ 3)$ を通るとき、最小になるのは原点を通るときである。<br>"
         r"よって　<b>$\boldsymbol{x=4,\ y=3}$ のとき最大値 $\boldsymbol{17}$，$\boldsymbol{x=y=0}$ のとき最小値 $\boldsymbol{0}$</b>",
  "note": r"多角形の領域では、1次式の最大・最小は頂点でとる。頂点の値 $0,\ 10,\ 17,\ 15$ を比べてもよいが、傾きの比較で「なぜその頂点か」を説明できるようにしておく。",
  "ex": r"$x\geqq0$，$y\geqq0$，$2x+y\leqq8$，$x+3y\leqq9$ のとき、$x+y$ の最大値と最小値を求めよ。",
  "exa": r"$x=3,\ y=2$ のとき最大値 $5$，$x=y=0$ のとき最小値 $0$"},
 {"lv": 3, "title": r"円の領域での最大・最小（$\frac{y}{x}$ と $x^2+y^2$）",
  "q": r"点 $(x,\ y)$ が円 $(x-3)^2+(y-2)^2\leqq4$ の周および内部を動くとき、次の式の最大値・最小値を求めよ。<br>(1) $\dfrac yx$　(2) $x^2+y^2$",
  "hint": r"(1) $\dfrac yx=k$ は「原点を通る傾き $k$ の直線」。接するときが端。(2) $x^2+y^2$ は原点からの距離の2乗。原点と中心を結ぶ直線上で最大・最小。",
  "sol": _F74 + r"領域 $D$ の点は $1\leqq x\leqq5$ を満たすので $x\gt0$。<br>"
         r"(1) $\dfrac yx=k$ とおくと $y=kx$。$k$ のとり得る値は、直線 $y=kx$ が $D$ と共有点をもつ $k$ の値。境目は接するときで、$\dfrac{|3k-2|}{\sqrt{k^2+1}}=2$ より $5k^2-12k=0$，$k=0,\ \dfrac{12}5$。<br>"
         r"$k=0$ の接点は $(3,\ 0)$，$k=\dfrac{12}5$ の接点は $\left(\dfrac{15}{13},\ \dfrac{36}{13}\right)$。<br>"
         r"よって　<b>最大値 $\boldsymbol{\dfrac{12}5}$，最小値 $\boldsymbol{0}$</b><br>"
         r"(2) 原点と中心 $(3,\ 2)$ の距離は $\sqrt{13}\gt2$ なので、原点から $D$ の点までの距離は $\sqrt{13}-2$ 以上 $\sqrt{13}+2$ 以下で、両端は原点と中心を結ぶ直線と円の交点でとる。<br>"
         r"よって　<b>最大値 $\boldsymbol{(\sqrt{13}+2)^2=17+4\sqrt{13}}$，最小値 $\boldsymbol{(\sqrt{13}-2)^2=17-4\sqrt{13}}$</b>",
  "note": r"$\dfrac{y-q}{x-p}$ なら点 $(p,\ q)$ を通る直線の傾き、$(x-p)^2+(y-q)^2$ なら点 $(p,\ q)$ からの距離の2乗と読みかえる。式の「図形的な意味」を見抜くのがこの型の要点。",
  "ex": r"点 $(x,\ y)$ が $(x-3)^2+(y-4)^2\leqq5$ を満たすとき、$\dfrac yx$ と $x^2+y^2$ の最大値・最小値を求めよ。",
  "exa": r"$\dfrac yx$：最大値 $\dfrac{11}2$，最小値 $\dfrac12$；$x^2+y^2$：最大値 $30+10\sqrt5$，最小値 $30-10\sqrt5$"},
 {"lv": 3, "title": "線形計画法の応用（整数の条件）",
  "q": r"2種類の製品 P，Q を作る。1個あたりに必要な原料と利益は下の表の通りで、原料 A は $14\,\mathrm{kg}$，原料 B は $12\,\mathrm{kg}$ まで使える。製品は1個単位でしか作れないとき、利益を最大にするには P，Q をそれぞれ何個作ればよいか。また、そのときの利益を求めよ。"
       r"<table><tr><th></th><th>原料 A</th><th>原料 B</th><th>利益</th></tr><tr><td>P</td><td>$3\,\mathrm{kg}$</td><td>$1\,\mathrm{kg}$</td><td>5万円</td></tr><tr><td>Q</td><td>$1\,\mathrm{kg}$</td><td>$2\,\mathrm{kg}$</td><td>4万円</td></tr></table>",
  "hint": r"まず整数の条件を外して最大を求める。その点が整数でなければ、$y$ の値ごとに $x$ の最大値を調べるなどして、整数の点の中での最大を<b>確実に</b>求める（四捨五入では保証されない）。",
  "sol": r"P を $x$ 個、Q を $y$ 個作るとすると、$x,\ y$ は0以上の整数で　$3x+y\leqq14$，$x+2y\leqq12$。利益は $5x+4y$（万円）。<br>"
         r"整数の条件を外すと、境界の傾き $-3$，$-\dfrac12$ と $5x+4y=k$ の傾き $-\dfrac54$ の比較から、2直線の交点 $\left(\dfrac{16}5,\ \dfrac{22}5\right)$ で最大値 $\dfrac{168}5=33.6$。この点は整数でない。<br>"
         r"そこで $y=0,\ 1,\ \cdots,\ 6$（$x+2y\leqq12$ より $y\leqq6$）のそれぞれについて、条件を満たす $x$ の最大値と $5x+4y$ を調べる。"
         r"<table><tr><th>$y$</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr><tr><th>$x$ の最大</th><td>4</td><td>4</td><td>4</td><td>3</td><td>3</td><td>2</td><td>0</td></tr><tr><th>$5x+4y$</th><td>20</td><td>24</td><td>28</td><td>27</td><td>31</td><td>30</td><td>24</td></tr></table>"
         r"（$x$ の最大は $\dfrac{14-y}3$ と $12-2y$ の小さい方以下の最大の整数。）<br>"
         r"よって　<b>P を $\boldsymbol{3}$ 個、Q を $\boldsymbol{4}$ 個作るとき、利益は最大で $\boldsymbol{31}$ 万円</b>",
  "note": r"この例では交点 $(3.2,\ 4.4)$ に近い $(3,\ 4)$ が答えになったが、一般には最も近い格子点が条件を満たさなかったり、最適でなかったりする。1つの文字の値で分けてしらみつぶしにするのが確実。",
  "ex": r"$x,\ y$ が0以上の整数で $2x+3y\leqq13$，$4x+y\leqq15$ を満たすとき、$3x+2y$ の最大値と、そのときの $x,\ y$ を求めよ。",
  "exa": r"$x=3,\ y=2$ のとき最大値 $13$"},
 {"lv": 4, "title": "曲線を含む領域での1次式の最大・最小（係数に文字）",
  "q": r"連立不等式 $y\geqq x^2$，$x^2+y^2\leqq2$ の表す領域を $D$ とする。$a$ を実数の定数とし、点 $(x,\ y)$ が $D$ を動くときの $y-ax$ の最大値 $M$ と最小値 $m$ を、$a$ の値で場合分けして求めよ。",
  "hint": r"$y-ax=k$ は傾き $a$ の直線。最大は上側の円弧に接するか端点 $(\pm1,\ 1)$ を通るとき、最小は下側の放物線に接するか端点を通るとき。円弧・放物線の端での接線の傾きが場合分けの境目になる。",
  "sol": _F76 + r"$y=x^2$ と $x^2+y^2=2$ の交点は $y+y^2=2$，$y=1$ より $(\pm1,\ 1)$。$D$ の点は $x^2\leqq y$，$x^2+y^2\leqq2$ から $x^2+x^4\leqq2$，すなわち $|x|\leqq1$ を満たす。<br>"
         r"<b>最小値</b>　$D$ の点では $y\geqq x^2$ なので $y-ax\geqq x^2-ax$ $(|x|\leqq1)$。また放物線上の点 $(x,\ x^2)$ $(|x|\leqq1)$ は $D$ に属する。よって $m$ は $g(x)=x^2-ax=\left(x-\dfrac a2\right)^2-\dfrac{a^2}4$ の $-1\leqq x\leqq1$ における最小値で<br>"
         r"　$\boldsymbol{a\lt-2}$ <b>のとき</b> $\boldsymbol{m=g(-1)=1+a}$，$\boldsymbol{-2\leqq a\leqq2}$ <b>のとき</b> $\boldsymbol{m=-\dfrac{a^2}4}$，$\boldsymbol{a\gt2}$ <b>のとき</b> $\boldsymbol{m=g(1)=1-a}$<br>"
         r"<b>最大値</b>　(i) $|a|\leqq1$ のとき：$(y-ax)^2\leqq(a^2+1)(x^2+y^2)\leqq2(a^2+1)$（コーシー・シュワルツの不等式）より $y-ax\leqq\sqrt{2a^2+2}$。<br>"
         r"等号は $(x,\ y)=\dfrac{\sqrt2}{\sqrt{a^2+1}}(-a,\ 1)$ のときで、この点が $D$ に属する条件 $y\geqq x^2$ は $\dfrac{\sqrt2}{\sqrt{a^2+1}}\geqq\dfrac{2a^2}{a^2+1}$，すなわち $2(a^2+1)\geqq4a^4$，$(2a^2+1)(a^2-1)\leqq0$ で、$|a|\leqq1$ のとき成り立つ。よって $M=\sqrt{2a^2+2}$。<br>"
         r"(ii) $a\gt1$ のとき：直線 $y=x+2$ は円 $x^2+y^2=2$ に点 $(-1,\ 1)$ で接するから、$D$ の点は $y\leqq x+2$ を満たす。また $x+1\geqq0$ なので<br>"
         r"　$(y-ax)-(1+a)=(y-1)-a(x+1)\leqq(y-1)-(x+1)=y-x-2\leqq0$<br>"
         r"等号は $(-1,\ 1)$ で成り立つから $M=1+a$。(iii) $a\lt-1$ のときは、同様に $y\leqq-x+2$ を用いて $M=1-a$（点 $(1,\ 1)$）。<br>"
         r"まとめて　$\boldsymbol{a\lt-1}$ <b>のとき</b> $\boldsymbol{M=1-a}$，$\boldsymbol{-1\leqq a\leqq1}$ <b>のとき</b> $\boldsymbol{M=\sqrt{2a^2+2}}$，$\boldsymbol{a\gt1}$ <b>のとき</b> $\boldsymbol{M=1+a}$",
  "note": r"図形的には、傾き $a$ の直線を上下に動かす。$(\pm1,\ 1)$ での円の接線の傾きは $\pm1$，放物線の接線（重解の条件から $y=\pm2x-1$）の傾きは $\pm2$ で、これらが場合分けの境目 $|a|=1$，$|a|=2$ になる。$a=\pm1$，$\pm2$ で $M$，$m$ が連続につながることも検算になる。",
  "ex": r"連立不等式 $y\geqq\dfrac12x^2$，$x^2+y^2\leqq8$ の表す領域を点 $(x,\ y)$ が動くとき、$y-ax$ の最大値 $M$ と最小値 $m$ を求めよ。",
  "exa": r"$M$：$a\lt-1$ で $2-2a$，$|a|\leqq1$ で $2\sqrt{2a^2+2}$，$a\gt1$ で $2+2a$；$m$：$a\lt-2$ で $2+2a$，$|a|\leqq2$ で $-\dfrac{a^2}2$，$a\gt2$ で $2-2a$"},
 {"lv": 4, "title": "領域を利用した命題の証明（十分条件）",
  "q": r"実数 $x,\ y$ について、次の問いに答えよ。<br>(1) 命題「$x^2+y^2\leqq1$ ならば $x+2y\leqq k$」が真となるような定数 $k$ の最小値を求めよ。<br>(2) 命題「$x^2+y^2\leqq1$ ならば $y\geqq x^2+c$」が真となるような定数 $c$ の最大値を求めよ。",
  "hint": r"「$p\Rightarrow q$ が真」は「$p$ の領域が $q$ の領域に含まれる」こと。(2) は円の最下点 $(0,\ -1)$ だけ調べても不十分（放物線が円の内部に入り込む）。$y-x^2$ の円板上での最小値を求める。",
  "sol": _F77 + r"円板 $x^2+y^2\leqq1$ を $D$ とする。<br>"
         r"(1) 命題が真 $\Longleftrightarrow$ $D$ 上で $x+2y$ の最大値が $k$ 以下。$(x+2y)^2\leqq(1^2+2^2)(x^2+y^2)\leqq5$ より $x+2y\leqq\sqrt5$，等号は $(x,\ y)=\left(\dfrac1{\sqrt5},\ \dfrac2{\sqrt5}\right)$。よって最大値は $\sqrt5$ で、$k$ の最小値は　$\boldsymbol{\sqrt5}$<br>"
         r"(2) 命題が真 $\Longleftrightarrow$ $D$ 上で $y-x^2$ の最小値が $c$ 以上。$D$ の点では $x^2\leqq1-y^2$ なので<br>"
         r"　$y-x^2\geqq y-(1-y^2)=y^2+y-1=\left(y+\dfrac12\right)^2-\dfrac54\geqq-\dfrac54$<br>"
         r"等号は $y=-\dfrac12$，$x^2=\dfrac34$ のとき、すなわち $(x,\ y)=\left(\pm\dfrac{\sqrt3}2,\ -\dfrac12\right)$（$D$ に属する）で成り立つ。よって最小値は $-\dfrac54$ で、$c$ の最大値は　$\boldsymbol{-\dfrac54}$",
  "note": r"放物線 $y=x^2-\dfrac54$ は円 $x^2+y^2=1$ に2点 $\left(\pm\dfrac{\sqrt3}2,\ -\dfrac12\right)$ で接する（連立すると $\left(y+\dfrac12\right)^2=0$）。最下点だけを見て $c=-1$ とすると、放物線 $y=x^2-1$（破線）は円の内部を通り、たとえば $(0.8,\ -0.5)$ は $D$ に属するのに $y\geqq x^2-1$ を満たさない。",
  "ex": r"(1) 「$x^2+y^2\leqq4$ ならば $3x-4y\leqq k$」が真となる $k$ の最小値　(2) 「$x^2+y^2\leqq4$ ならば $y\geqq x^2+c$」が真となる $c$ の最大値　を求めよ。",
  "exa": r"(1) $10$　(2) $-\dfrac{17}4$"},
 {"lv": 5, "title": "区間でつねに成り立つ不等式と係数の存在範囲",
  "q": r"実数 $a,\ b$ に対し $f(x)=x^2+ax+b$ とする。<br>(1) $0\leqq x\leqq1$ を満たすすべての $x$ に対して $|f(x)|\leqq\dfrac12$ が成り立つような点 $(a,\ b)$ の存在範囲を、$ab$ 平面上に図示せよ。<br>(2) 正の数 $k$ に対し、「$0\leqq x\leqq1$ のすべての $x$ で $|f(x)|\leqq k$」となる実数 $a,\ b$ が存在するような $k$ の最小値を求めよ。",
  "hint": r"(1) $f$ は下に凸なので、区間での最大値は端点、最小値は軸の位置で3通りに分かれる。(2) 区間内の3点の値を組み合わせて $a,\ b$ を消去する：$f(0)+f(1)-2f\left(\dfrac12\right)$ は $a,\ b$ によらない定数。",
  "sol": _F78 + r"(1) $f$ は下に凸だから、$0\leqq x\leqq1$ での最大値は $f(0)$，$f(1)$ の大きい方。よって $f(x)\leqq\dfrac12$ がつねに成り立つ条件は<br>"
         r"　$b\leqq\dfrac12$　かつ　$1+a+b\leqq\dfrac12$，すなわち $b\leqq-a-\dfrac12$　…①<br>"
         r"最小値の条件 $f(x)\geqq-\dfrac12$ を、軸 $x=-\dfrac a2$ の位置で分ける。<br>"
         r"(i) $a\gt0$：最小値 $f(0)=b\geqq-\dfrac12$。① の $b\leqq-a-\dfrac12\lt-\dfrac12$ と矛盾し、不適。<br>"
         r"(ii) $a\lt-2$：最小値 $f(1)=1+a+b\geqq-\dfrac12$，$b\geqq-a-\dfrac32\gt\dfrac12$ となり ① の $b\leqq\dfrac12$ と矛盾し、不適。<br>"
         r"(iii) $-2\leqq a\leqq0$：最小値 $f\left(-\dfrac a2\right)=b-\dfrac{a^2}4\geqq-\dfrac12$，すなわち $b\geqq\dfrac{a^2}4-\dfrac12$。<br>"
         r"よって求める範囲は　$\boldsymbol{-2\leqq a\leqq0,\ \ \dfrac{a^2}4-\dfrac12\leqq b\leqq\dfrac12,\ \ b\leqq-a-\dfrac12}$<br>"
         r"放物線 $b=\dfrac{a^2}4-\dfrac12$ は直線 $b=\dfrac12$ と $a=-2$ で、直線 $b=-a-\dfrac12$ と $a=0$ で交わり（$\dfrac{a^2}4+a=0$），2直線は $(-1,\ \dfrac12)$ で交わる。<b>図の網目部分（境界を含む）</b>。<br>"
         r"(2) 条件を満たす $a,\ b$ があるとすると、$f(0)\leqq k$，$f(1)\leqq k$，$f\left(\dfrac12\right)\geqq-k$。一方<br>"
         r"　$f(0)+f(1)-2f\left(\dfrac12\right)=b+(1+a+b)-2\left(\dfrac14+\dfrac a2+b\right)=\dfrac12$<br>"
         r"であるから　$\dfrac12\leqq k+k+2k=4k$，$k\geqq\dfrac18$。<br>"
         r"逆に $k=\dfrac18$ のとき、$f(x)=x^2-x+\dfrac18=\left(x-\dfrac12\right)^2-\dfrac18$ は $0\leqq x\leqq1$ で $-\dfrac18\leqq f(x)\leqq\dfrac18$ を満たす。<br>"
         r"よって $k$ の最小値は　$\boldsymbol{\dfrac18}$",
  "note": r"(2) で等号が成り立つのは $f(0)=f(1)=k$，$f\left(\dfrac12\right)=-k$ のときだけで、$(a,\ b)=\left(-1,\ \dfrac18\right)$（図の黒点）に限る。$k$ を小さくすると (1) の曲線三角形が縮み、$k=\dfrac18$ でこの1点になる。「最大値の最小化」はチェビシェフの多項式の考え方につながる有名なテーマ。",
  "ex": r"$f(x)=x^2+ax+b$ について、(1) $-1\leqq x\leqq1$ のすべての $x$ で $|f(x)|\leqq1$ となる点 $(a,\ b)$ の存在範囲を求めよ。(2) $-1\leqq x\leqq1$ のすべての $x$ で $|f(x)|\leqq k$ となる $a,\ b$ が存在するような $k$ の最小値を求めよ。",
  "exa": r"(1) $\dfrac{a^2}4-1\leqq b\leqq-|a|$　(2) $\dfrac12$（$f(-1)+f(1)-2f(0)=2\leqq4k$，等号は $f(x)=x^2-\frac12$）"},
]})


def _v7():
    rnd = random.Random(7)
    # 7.1 交点
    for sgn in (1, -1):
        X, Y = 2 - sgn * 4 / _s5, sgn * 2 / _s5
        assert abs(X + 2 * Y - 2) < 1e-12 and abs(X * X + Y * Y - 4 * X) < 1e-12
    # 7.2 (1) 交点，(2) 正方形
    for (X, Y) in [(-2, 0), (1.2, 1.6)]:
        assert abs(X - 2 * Y + 2) < 1e-12 and abs(X * X + Y * Y - 4) < 1e-12
    for _ in range(20000):
        X, Y = rnd.uniform(-3, 3), rnd.uniform(-2, 4)
        sq = (Y <= -X + 3) and (Y >= X - 1) and (Y <= X + 3) and (Y >= -X - 1)
        assert (abs(X) + abs(Y - 1) <= 2) == sq
        sq2 = (abs(X - 1) + abs(Y) <= 1)
        assert sq2 == ((Y <= -X + 2) and (Y >= X - 2) and (Y <= X) and (Y >= -X))
    # 7.3 頂点と格子点で確認
    def lp(cons, obj):
        best = []
        for i in range(0, 601):
            for j in range(0, 601):
                X, Y = i / 100, j / 100
                if all(a * X + b * Y <= c + 1e-12 for a, b, c in cons):
                    best.append(obj(X, Y))
        return max(best), min(best)
    assert lp([(1, 2, 10), (3, 1, 15)], lambda X, Y: 2 * X + 3 * Y) == (17, 0)
    mx, mn = lp([(2, 1, 8), (1, 3, 9)], lambda X, Y: X + Y)
    assert abs(mx - 5) < 1e-9 and mn == 0
    assert 4 + 6 == 10 and 12 + 3 == 15 and 6 + 2 == 8 and 3 + 6 == 9
    # 7.4
    N = 40000
    for (cx, cy, r2, k1, k2, d1, d2) in [(3, 2, 4, 0, 12 / 5, 17 - 4 * 13 ** .5, 17 + 4 * 13 ** .5),
                                         (3, 4, 5, 1 / 2, 11 / 2, 30 - 10 * 5 ** .5, 30 + 10 * 5 ** .5)]:
        pts = [(cx + r2 ** .5 * math.cos(2 * math.pi * i / N), cy + r2 ** .5 * math.sin(2 * math.pi * i / N)) for i in range(N)]
        assert min(p[0] for p in pts) > 0
        ks = [p[1] / p[0] for p in pts]
        ds = [p[0] ** 2 + p[1] ** 2 for p in pts]
        assert abs(min(ks) - k1) < 1e-6 and abs(max(ks) - k2) < 1e-6 and abs(min(ds) - d1) < 1e-6 and abs(max(ds) - d2) < 1e-6
    assert _close((15 / 13 - 3) ** 2 + (36 / 13 - 2) ** 2, 4) and _close(36 / 15, 12 / 5)
    # 7.5 総当たり
    def ilp(cons, obj):
        vals = [(obj(X, Y), X, Y) for X in range(0, 50) for Y in range(0, 50) if all(a * X + b * Y <= c for a, b, c in cons)]
        m = max(vals)
        return m, [v for v in vals if v[0] == m[0]]
    m, arg = ilp([(3, 1, 14), (1, 2, 12)], lambda X, Y: 5 * X + 4 * Y)
    assert m[0] == 31 and [(v[1], v[2]) for v in arg] == [(3, 4)]
    tab = [max(X for X in range(0, 20) if 3 * X + Y <= 14 and X + 2 * Y <= 12) for Y in range(7)]
    assert tab == [4, 4, 4, 3, 3, 2, 0] and [5 * X + 4 * Y for Y, X in enumerate(tab)] == [20, 24, 28, 27, 31, 30, 24]
    s = solve([3 * symbols("p") + symbols("q") - 14, symbols("p") + 2 * symbols("q") - 12])
    assert list(s.values()) == [R(16, 5), R(22, 5)] or set(s.values()) == {R(16, 5), R(22, 5)}
    m, arg = ilp([(2, 3, 13), (4, 1, 15)], lambda X, Y: 3 * X + 2 * Y)
    assert m[0] == 13 and [(v[1], v[2]) for v in arg] == [(3, 2)]
    # 7.6 境界を細かく調べる（凸領域上の1次式は境界で最大最小）
    for (c, rr, M, mfun) in [(1.0, 2.0, lambda a: 1 - a if a < -1 else (math.sqrt(2 * a * a + 2) if a <= 1 else 1 + a),
                              lambda a: 1 + a if a < -2 else (-a * a / 4 if a <= 2 else 1 - a)),
                             (0.5, 8.0, lambda a: 2 - 2 * a if a < -1 else (2 * math.sqrt(2 * a * a + 2) if a <= 1 else 2 + 2 * a),
                              lambda a: 2 + 2 * a if a < -2 else (-a * a / 2 if a <= 2 else 2 - 2 * a))]:
        x0 = 1.0 if c == 1.0 else 2.0
        bd = [(-x0 + 2 * x0 * i / 4000, c * (-x0 + 2 * x0 * i / 4000) ** 2) for i in range(4001)]
        th0 = math.atan2(c * x0 * x0, x0)
        bd += [(math.sqrt(rr) * math.cos(th0 + (math.pi - 2 * th0) * i / 4000), math.sqrt(rr) * math.sin(th0 + (math.pi - 2 * th0) * i / 4000)) for i in range(4001)]
        assert all(p[1] >= c * p[0] ** 2 - 1e-9 and p[0] ** 2 + p[1] ** 2 <= rr + 1e-9 for p in bd)
        for a in [-3.5, -2.5, -2, -1.5, -1, -0.6, 0, 0.3, 1, 1.4, 2, 2.7, 4]:
            vals = [p[1] - a * p[0] for p in bd]
            assert abs(max(vals) - M(a)) < 1e-5 and abs(min(vals) - mfun(a)) < 1e-5
    # 7.7
    N = 20000
    vals = [math.cos(2 * math.pi * i / N) + 2 * math.sin(2 * math.pi * i / N) for i in range(N)]
    assert abs(max(vals) - _s5) < 1e-7
    for rad, cm in [(1, -1.25), (2, -17 / 4)]:
        best = min(r * math.sin(t) - (r * math.cos(t)) ** 2 for r in [rad * j / 200 for j in range(201)] for t in [2 * math.pi * i / 2000 for i in range(2000)])
        assert abs(best - cm) < 1e-4 and best >= cm - 1e-12
    vals = [6 * math.cos(2 * math.pi * i / N) - 8 * math.sin(2 * math.pi * i / N) for i in range(N)]
    assert abs(max(vals) - 10) < 1e-6
    assert 0.8 ** 2 + 0.25 <= 1 and -0.5 < 0.8 ** 2 - 1
    # 7.8 区間 [0,1] で |f|<=1/2 となる (a,b) と、領域の式の一致
    def maxabs(a, b, lo, hi):
        f = lambda t: t * t + a * t + b
        cand = [f(lo), f(hi)]
        if lo <= -a / 2 <= hi:
            cand.append(f(-a / 2))
        return max(abs(v) for v in cand)
    for _ in range(40000):
        a, b = rnd.uniform(-3, 1), rnd.uniform(-1, 1)
        ok = maxabs(a, b, 0, 1) <= 0.5
        reg = (-2 <= a <= 0) and (a * a / 4 - 0.5 <= b <= 0.5) and (b <= -a - 0.5)
        assert ok == reg
        a, b = rnd.uniform(-1.5, 1.5), rnd.uniform(-1.5, 0.5)
        assert (maxabs(a, b, -1, 1) <= 1) == (a * a / 4 - 1 <= b <= -abs(a))
    best = min(maxabs(i / 400, j / 400, 0, 1) for i in range(-800, 1) for j in range(-200, 201, 1))
    assert abs(best - 1 / 8) < 1e-12 and maxabs(-1, 1 / 8, 0, 1) == 1 / 8
    best = min(maxabs(i / 200, j / 200, -1, 1) for i in range(-200, 201) for j in range(-200, 201))
    assert abs(best - 1 / 2) < 1e-12
    a, b, x = symbols("a b x")
    f = x ** 2 + a * x + b
    assert expand(f.subs(x, 0) + f.subs(x, 1) - 2 * f.subs(x, R(1, 2))) == R(1, 2)
    assert expand(f.subs(x, -1) + f.subs(x, 1) - 2 * f.subs(x, 0)) == 2


_V.append(_v7)


# ---------------------------------------------------------------- 節8
_F81 = _fig((-2.4, 2.4), (-1.6, 3.4), [
    ("fill", [_fp(lambda t: t * t + 1, -2.4, 2.4, 60) + [(2.4, -1.6), (-2.4, -1.6)]]),
    ("fn", lambda t: t * t + 1, -2.4, 2.4, "b"), ("fn", lambda t: 2 * t, -2.4, 2.4, "g"), ("fn", lambda t: -2 * t, -2.4, 2.4, "g"),
    ("fn", lambda t: 1, -2.4, 2.4, "g"), ("txt", (0, 1), "1", (-9, -2))], W=150)
_F82 = _fig((-2.6, 2.6), (-3.3, 1.6), [
    ("fill", [_fp(lambda t: t * t / 4, -2, 2, 60) + _fp(lambda t: t * t - 3, 2, -2, 60)]),
    ("fn", lambda t: t * t / 4, -2, 2, "b"), ("fn", lambda t: t * t - 3, -2, 2, "b"),
    ("dot", (2, 1), "(2, 1)", (-30, -4)), ("dot", (-2, 1), "", (0, 0)), ("txt", (0, -3), "−3", (4, 10))], W=150, lab=("X", "Y"))


def _L83(x):
    return x * x + 2 * x + 2 if x < -2 else (x * x / 2 if x <= 4 else x * x - 4 * x + 8)


def _U83(x):
    return x * x - 4 * x + 8 if x <= 1 else x * x + 2 * x + 2


_F83 = _fig((-3, 4.6), (-0.6, 12), [
    ("fill", [_fp(_L83, -3, 4.6, 120) + _fp(_U83, 4.6, -3, 120)]),
    ("fn", _L83, -3, 4.6, "b"), ("fn", _U83, -3, 4.6, "b"), ("fn", lambda t: t * t / 2, -3, 4.6, "gd"),
    ("dot", (-2, 2), "", (0, 0)), ("dot", (4, 8), "", (0, 0)), ("dot", (1, 5), "", (0, 0)),
    ("txt", (-2, 0), "−2", (-8, 12)), ("txt", (4, 0), "4", (-3, 12)), ("txt", (1, 0), "1", (-3, 12))], W=190, sy=10.5)
_R84 = ([(0, 1), (0.5, 0.5)] + _fp(lambda t: 1 / (4 * t), 0.5, 1, 40) + [(2, 0), (1, 0), (2 / 3, 1 / 3), (0, 0.5)])
_F84 = _fig((-0.15, 2.25), (-0.12, 1.15), [
    ("fill", [_R84]), ("pl", _R84 + [(0, 1)], "b"),
    ("seg", (1.5, 0), (0, 1 / 1.5), "g"), ("fn", lambda t: 1 / (4 * t), 0.24, 2.2, "gd"),
    ("txt", (2, 0), "2", (-3, 12)), ("txt", (1, 0), "1", (-3, 12)), ("txt", (0, 1), "1", (-9, 4)), ("txt", (0, 0.5), "½", (-10, 4))], W=200)
_s3 = math.sqrt(3)
_K85 = _arc(0.25, 1, 0.5, -math.pi / 2, math.pi / 2, 40) + _arc(-0.25, 1, 0.5, math.pi / 2, 3 * math.pi / 2, 40)
_L85 = _arc(-0.25, 1, 0.5, -math.pi / 3, math.pi / 3, 30) + _arc(0.25, 1, 0.5, 2 * math.pi / 3, 4 * math.pi / 3, 30)
_F85 = _fig((-0.85, 0.85), (0.35, 1.65), [
    ("fill", [_K85, _L85]), ("pl", _K85 + _K85[:1], "b"), ("pl", _L85 + _L85[:1], "b"),
    ("seg", (-0.25, 1), (0.25, 1), "gd"), ("dot", (-0.25, 1), "", (0, 0)), ("dot", (0.25, 1), "", (0, 0)),
    ("txt", (0, 1), "1", (-9, 4))], W=170, O=False)
_W86a = [(0.5, 0), (-0.6, 0), (-0.6, -2.2)]
_W86b = [(0.5, 0), (1.6, 2.2), (1.6, 0)]
_N86 = _fp(lambda t: 0.0, 0, 0.5, 2) + _fp(lambda t: 2 * t - 1, 0.5, 1, 2) + _fp(lambda t: t * t, 1, 0, 50)
_F86 = _fig((-0.6, 1.6), (-1.2, 1.3), [
    ("fill", [_W86a]), ("fill", [_W86b]), ("fill", [_N86], "#c0392b"),
    ("line", 0, 1, 0, "b"), ("line", 2, -1, -1, "b"), ("fn", lambda t: t * t, -0.6, 1.25, "gd"), ("fn", lambda t: t * t, 0, 1, "r"),
    ("dot", (1, 1), "", (0, 0)), ("dot", (0.5, 0), "", (0, 0)), ("txt", (1, 1), "(1, 1)", (-34, -2)), ("txt", (0.5, 0), "½", (-2, 12))], W=160)

SEC.append({"title": "通過領域・点の存在範囲",
"base": r"""・<b>逆像法</b>：点 $(X,\ Y)$ が図形の族 $F(x,\ y,\ t)=0$ の通過領域に属する $\Longleftrightarrow$ $t$ の方程式 $F(X,\ Y,\ t)=0$ が、$t$ の動く範囲に実数解をもつ。<br>
・<b>$x$ を固定する方法</b>（順像法）：$x=k$ と固定し、$t$ を動かしたときの $y$ の値域を求めて、$k$ を動かす。$t$ の範囲が制限されているときに有効。<br>
・点 $(x+y,\ xy)$ の存在範囲：$x+y=X$，$xy=Y$ とすると $x,\ y$ は $s^2-Xs+Y=0$ の2解。<b>実数条件 $X^2-4Y\geqq0$</b> を必ず加える。<br>
・通過領域の境界には、族のすべての図形に接する曲線（包絡線）が現れることが多い。""",
"items": [
 {"lv": 3, "title": "直線の通過領域（パラメータが実数全体）",
  "q": r"$a$ が実数全体を動くとき、直線 $\ell_a:\ y=2ax-a^2+1$ が通過する領域を図示せよ。",
  "hint": r"点 $(X,\ Y)$ を通る $\ell_a$ がある $\Longleftrightarrow$ $a$ の2次方程式 $Y=2aX-a^2+1$ が実数解をもつ。判別式で判定する。",
  "sol": _F81 + r"点 $(X,\ Y)$ が通過領域に属する条件は、$Y=2aX-a^2+1$，すなわち<br>"
         r"　$a^2-2Xa+Y-1=0$<br>"
         r"を満たす実数 $a$ が存在することである。その条件は $\dfrac D4=X^2-(Y-1)\geqq0$，すなわち $Y\leqq X^2+1$。<br>"
         r"よって求める領域は　<b>放物線 $\boldsymbol{y=x^2+1}$ およびその下側</b>（境界を含む，図の網目部分）",
  "note": r"<b>別解</b>（$x$ を固定）：$x=X$ のとき $y=-(a-X)^2+X^2+1$ は $a$ を動かすと $X^2+1$ 以下のすべての値をとる。各 $\ell_a$ は放物線 $y=x^2+1$ に点 $(a,\ a^2+1)$ で接しており（$x^2+1-(2ax-a^2+1)=(x-a)^2$），この放物線が包絡線になっている。",
  "ex": r"$t$ が実数全体を動くとき、直線 $y=tx+t^2-2t$ が通過する領域を求めよ。",
  "exa": r"$y\geqq-\dfrac14(x-2)^2$（放物線とその上側）"},
 {"lv": 4, "title": r"点 $(x+y,\ xy)$ の存在範囲",
  "q": r"実数 $x,\ y$ が $x^2+xy+y^2\leqq3$ を満たしながら動く。<br>(1) 点 $(x+y,\ xy)$ の存在範囲を図示せよ。<br>(2) $x+y+xy$ の最大値と最小値を求めよ。",
  "hint": r"$X=x+y$，$Y=xy$ とおくと条件は $X^2-Y\leqq3$。これだけでは不十分で、$X,\ Y$ に対して実数 $x,\ y$ が存在する条件 $X^2-4Y\geqq0$ を加える。",
  "sol": _F82 + r"(1) $X=x+y$，$Y=xy$ とおく。$x^2+xy+y^2=X^2-Y$ なので条件は $Y\geqq X^2-3$。<br>"
         r"また、$x,\ y$ は $s$ の2次方程式 $s^2-Xs+Y=0$ の2解だから、$x,\ y$ が実数であるための条件は $X^2-4Y\geqq0$，すなわち $Y\leqq\dfrac{X^2}4$。<br>"
         r"逆にこの2条件を満たす $(X,\ Y)$ に対して、2次方程式の2解として実数 $x,\ y$ が定まり条件を満たす。<br>"
         r"よって存在範囲は　$\boldsymbol{X^2-3\leqq Y\leqq\dfrac{X^2}4}$（2曲線は $X=\pm2$ で交わる；図の網目部分，境界を含む）<br>"
         r"(2) $x+y+xy=X+Y$。<br>"
         r"最大：$Y\leqq\dfrac{X^2}4$ より $X+Y\leqq\dfrac{X^2}4+X=\dfrac{(X+2)^2}4-1$。$-2\leqq X\leqq2$ だから $\leqq3$，等号は $X=2,\ Y=1$，すなわち $x=y=1$。<br>"
         r"最小：$Y\geqq X^2-3$ より $X+Y\geqq X^2+X-3=\left(X+\dfrac12\right)^2-\dfrac{13}4\geqq-\dfrac{13}4$，等号は $X=-\dfrac12,\ Y=-\dfrac{11}4$（範囲内）で、$x,\ y=\dfrac{-1\pm3\sqrt5}4$。<br>"
         r"よって　<b>最大値 $\boldsymbol{3}$，最小値 $\boldsymbol{-\dfrac{13}4}$</b>",
  "note": r"実数条件を忘れると、$Y$ をいくらでも大きくできてしまい (2) の最大値が求まらない。対称式の問題は「和と積に置きかえ → 実数条件」が定石（数と式の章の対称式の値域と同じ考え方を、領域として図に表したもの）。",
  "ex": r"実数 $x,\ y$ が $x^2+y^2\leqq1$ を満たすとき、(1) 点 $(x+y,\ xy)$ の存在範囲を求めよ。(2) $x+y-xy$ の最大値と最小値を求めよ。",
  "exa": r"(1) $\dfrac{X^2-1}2\leqq Y\leqq\dfrac{X^2}4$　(2) 最大値 $1$，最小値 $-\sqrt2-\dfrac12$"},
 {"lv": 4, "title": "パラメータの範囲が制限された放物線の通過領域",
  "q": r"$a$ が $-1\leqq a\leqq2$ の範囲を動くとき、放物線 $C_a:\ y=x^2-2ax+2a^2$ が通過する領域を図示せよ。",
  "hint": r"$a$ の2次方程式の解の配置でもできるが、$x$ を固定して $a$ の2次関数 $y=2a^2-2xa+x^2$ の $-1\leqq a\leqq2$ における値域を調べる方が見通しがよい。軸 $a=\dfrac x2$ の位置で場合分けする。",
  "sol": _F83 + r"$x$ を固定すると $y=g(a)=2a^2-2xa+x^2=2\left(a-\dfrac x2\right)^2+\dfrac{x^2}2$ $(-1\leqq a\leqq2)$。<br>"
         r"$g$ は連続なので、$y$ は $g$ の最小値から最大値までのすべての値をとる。$g(-1)=x^2+2x+2$，$g(2)=x^2-4x+8$。<br>"
         r"<b>最小値</b>　軸 $\dfrac x2$ について、$x\lt-2$ なら $g(-1)$，$-2\leqq x\leqq4$ なら $\dfrac{x^2}2$，$x\gt4$ なら $g(2)$。<br>"
         r"<b>最大値</b>　$g(-1)-g(2)=6(x-1)$ より、$x\leqq1$ なら $g(2)$，$x\geqq1$ なら $g(-1)$。<br>"
         r"よって求める領域は（境界を含む，図の網目部分）<br>"
         r"　$\boldsymbol{x\leqq-2}$ <b>のとき</b> $\boldsymbol{x^2+2x+2\leqq y\leqq x^2-4x+8}$<br>"
         r"　$\boldsymbol{-2\leqq x\leqq1}$ <b>のとき</b> $\boldsymbol{\dfrac{x^2}2\leqq y\leqq x^2-4x+8}$<br>"
         r"　$\boldsymbol{1\leqq x\leqq4}$ <b>のとき</b> $\boldsymbol{\dfrac{x^2}2\leqq y\leqq x^2+2x+2}$<br>"
         r"　$\boldsymbol{x\geqq4}$ <b>のとき</b> $\boldsymbol{x^2-4x+8\leqq y\leqq x^2+2x+2}$",
  "note": r"$x^2-2ax+2a^2-\dfrac{x^2}2=\dfrac12(x-2a)^2\geqq0$ より、$C_a$ は放物線 $y=\dfrac{x^2}2$（破線）に点 $(2a,\ 2a^2)$ で接する。$a$ の範囲が $-1\leqq a\leqq2$ なので、接点の $x$ 座標 $-2\leqq x\leqq4$ の部分だけが境界に現れ、その外側は両端の放物線 $C_{-1}$，$C_2$ が境界になる。",
  "ex": r"$a$ が $0\leqq a\leqq2$ の範囲を動くとき、放物線 $y=(x-a)^2+a$ が通過する領域を求めよ。",
  "exa": r"$x\leqq\frac12$：$x^2\leqq y\leqq x^2-4x+6$；$\frac12\leqq x\leqq\frac32$：$x-\frac14\leqq y\leqq x^2-4x+6$；$\frac32\leqq x\leqq\frac52$：$x-\frac14\leqq y\leqq x^2$；$x\geqq\frac52$：$x^2-4x+6\leqq y\leqq x^2$"},
 {"lv": 5, "title": "線分の通過領域",
  "q": r"$t$ が $1\leqq t\leqq2$ の範囲を動くとき、2点 $\mathrm{P}(t,\ 0)$，$\mathrm{Q}\left(0,\ \dfrac1t\right)$ を結ぶ線分 PQ が通過する領域を図示せよ。",
  "hint": r"直線ではなく<b>線分</b>なので、$x$ の範囲 $0\leqq x\leqq t$ がつく。$x=k$ と固定すると $y=\dfrac1t\left(1-\dfrac kt\right)$ で、$u=\dfrac1t$ とおけば $u$ の2次関数 $u-ku^2$ になる。$u$ の範囲が $k$ によって変わることに注意して値域を調べる。",
  "sol": _F84 + r"線分 PQ は $\dfrac xt+ty=1$，$0\leqq x\leqq t$ と表される。$x=k$ と固定すると、PQ 上に $x$ 座標が $k$ の点があるのは $0\leqq k\leqq t$ のときで、その点の $y$ 座標は $y=\dfrac1t\left(1-\dfrac kt\right)$。<br>"
         r"$u=\dfrac1t$ とおくと $\dfrac12\leqq u\leqq1$，条件 $k\leqq t$ は $ku\leqq1$ で、$y=h(u)=u-ku^2$。$h$ は連続なので、$y$ の値域は $h$ の最小値から最大値まで。<br>"
         r"(i) $0\leqq k\leqq\dfrac12$：$u$ の範囲は $\dfrac12\leqq u\leqq1$。$k\gt0$ なら $h(u)=-k\left(u-\dfrac1{2k}\right)^2+\dfrac1{4k}$ で軸 $\dfrac1{2k}\geqq1$，$k=0$ なら $h(u)=u$。いずれも増加し　$\dfrac12-\dfrac k4\leqq y\leqq1-k$<br>"
         r"(ii) $\dfrac12\leqq k\leqq1$：$\dfrac12\leqq u\leqq1$ で軸 $\dfrac1{2k}$ はこの範囲内。最大値 $\dfrac1{4k}$，最小値は $h\left(\dfrac12\right)=\dfrac12-\dfrac k4$ と $h(1)=1-k$ の小さい方で、$\dfrac12-\dfrac k4\leqq1-k\Longleftrightarrow k\leqq\dfrac23$。<br>"
         r"(iii) $1\leqq k\leqq2$：$u$ の範囲は $\dfrac12\leqq u\leqq\dfrac1k$ で、軸 $\dfrac1{2k}\leqq\dfrac12$ より $h$ は減少。$h\left(\dfrac1k\right)=0$ から　$0\leqq y\leqq\dfrac12-\dfrac k4$<br>"
         r"$k\lt0$，$k\gt2$ では点はない。よって求める領域は（境界を含む，図の網目部分）<br>"
         r"　$\boldsymbol{0\leqq x\leqq\frac12}$ <b>のとき</b> $\boldsymbol{-\frac x4+\frac12\leqq y\leqq-x+1}$<br>"
         r"　$\boldsymbol{\frac12\leqq x\leqq\frac23}$ <b>のとき</b> $\boldsymbol{-\frac x4+\frac12\leqq y\leqq\frac1{4x}}$<br>"
         r"　$\boldsymbol{\frac23\leqq x\leqq1}$ <b>のとき</b> $\boldsymbol{-x+1\leqq y\leqq\frac1{4x}}$<br>"
         r"　$\boldsymbol{1\leqq x\leqq2}$ <b>のとき</b> $\boldsymbol{0\leqq y\leqq-\frac x4+\frac12}$",
  "note": r"境界に現れる直線 $y=-x+1$，$y=-\dfrac x4+\dfrac12$ は $t=1$，$t=2$ の線分、双曲線 $y=\dfrac1{4x}$（破線）は包絡線である。実際 $\dfrac xt+\dfrac t{4x}=1\Longleftrightarrow(2x-t)^2=0$ より、線分 PQ は双曲線に PQ の中点 $\left(\dfrac t2,\ \dfrac1{2t}\right)$ で接する。中点の $x$ 座標が $\dfrac12$ から $1$ を動くので、双曲線のその部分だけが境界になる。直線全体の通過領域と混同しないこと。",
  "ex": r"$t$ が $1\leqq t\leqq3$ の範囲を動くとき、2点 $(t,\ 0)$，$\left(0,\ \dfrac1t\right)$ を結ぶ線分が通過する領域を求めよ。",
  "exa": r"$0\leqq x\leqq\frac12$：$\frac13-\frac x9\leqq y\leqq1-x$；$\frac12\leqq x\leqq\frac34$：$\frac13-\frac x9\leqq y\leqq\frac1{4x}$；$\frac34\leqq x\leqq1$：$1-x\leqq y\leqq\frac1{4x}$；$1\leqq x\leqq\frac32$：$0\leqq y\leqq\frac1{4x}$；$\frac32\leqq x\leqq3$：$0\leqq y\leqq\frac13-\frac x9$"},
 {"lv": 5, "title": "円周上の点と線分上の点の中点の存在範囲（穴のある領域）",
  "q": r"点 P が円 $x^2+y^2=1$ 上を、点 Q が線分 $y=2$ $\left(-\dfrac12\leqq x\leqq\dfrac12\right)$ 上を、それぞれ独立に動くとき、線分 PQ の中点 M の存在範囲を図示し、その面積を求めよ。",
  "hint": r"$\mathrm{Q}(q,\ 2)$ を固定すると M は「中心 $\left(\dfrac q2,\ 1\right)$，半径 $\dfrac12$ の円周」上を動く。これらの円周を Q について合わせたものが答え。円<b>周</b>の和集合なので、中心たちのどれからも距離が $\dfrac12$ 未満の点（穴）が生じうる。$\mathrm{M}(X,\ Y)$ を固定し、中心までの距離の2乗が $\dfrac14$ をとるかを、中間値の考え方で判定する。",
  "sol": _F85 + r"$\mathrm{P}(u,\ v)$，$\mathrm{Q}(q,\ 2)$ $\left(-\dfrac12\leqq q\leqq\dfrac12\right)$，$\mathrm{M}(X,\ Y)$ とすると $X=\dfrac{u+q}2$，$Y=\dfrac{v+2}2$。Q を固定したとき、P が円上にある条件 $u^2+v^2=1$ は $(2X-q)^2+(2Y-2)^2=1$ となる。$s=\dfrac q2$ とおくと<br>"
         r"　$h(s)=(X-s)^2+(Y-1)^2=\dfrac14$，$-\dfrac14\leqq s\leqq\dfrac14$<br>"
         r"よって M$(X,\ Y)$ が存在範囲に属する $\Longleftrightarrow$ $h(s)=\dfrac14$ となる $s\in\left[-\dfrac14,\ \dfrac14\right]$ がある $\Longleftrightarrow$ （$h$ は連続なので）この区間での $h$ の最小値 $\leqq\dfrac14\leqq$ 最大値。<br>"
         r"・最小値 $\leqq\dfrac14$：点 M と線分 $y=1$ $\left(-\dfrac14\leqq x\leqq\dfrac14\right)$（以下 $\sigma$）の距離が $\dfrac12$ 以下。これは $\sigma$ からの距離が $\dfrac12$ 以下の部分 $K$（長方形と2つの半円を合わせた形）を表す。<br>"
         r"・最大値 $\geqq\dfrac14$：$h$ は $s$ の下に凸な2次関数なので最大値は $h\left(-\dfrac14\right)$，$h\left(\dfrac14\right)$ の大きい方。よって条件は「$h\left(-\dfrac14\right)\lt\dfrac14$ かつ $h\left(\dfrac14\right)\lt\dfrac14$」でないこと、すなわち M が2円 $\left(x\pm\dfrac14\right)^2+(y-1)^2=\dfrac14$ の内部の共通部分 $L$ に属さないこと。<br>"
         r"したがって存在範囲は　<b>$\boldsymbol{K}$ から $\boldsymbol{L}$ を除いた部分</b>（図の網目部分，$L$ の周は含む）。<br>"
         r"<b>面積</b>　$K$ は縦 $1$，横 $\dfrac12$ の長方形と半径 $\dfrac12$ の円で、面積 $\dfrac12+\dfrac\pi4$。<br>"
         r"$L$ をつくる2円は半径 $\dfrac12$，中心間の距離 $\dfrac12$ なので、2つの中心と交点 $\left(0,\ 1\pm\dfrac{\sqrt3}4\right)$ は正三角形をなし、各円で $L$ の弧に対する中心角は $120^\circ$。$L$ の面積は<br>"
         r"　$2\left(\pi\cdot\dfrac14\cdot\dfrac13-\dfrac12\cdot\dfrac{\sqrt3}2\cdot\dfrac14\right)=\dfrac\pi6-\dfrac{\sqrt3}8$<br>"
         r"よって求める面積は　$\dfrac12+\dfrac\pi4-\dfrac\pi6+\dfrac{\sqrt3}8=\boldsymbol{\dfrac12+\dfrac\pi{12}+\dfrac{\sqrt3}8}$",
  "note": r"P が円の<b>周および内部</b>を動くなら穴はできず、答えは $K$（面積 $\dfrac12+\dfrac\pi4$）。Q の線分が長く、両端の中心の距離が直径 $1$ 以上になると穴は消える。「1つを固定して動かし、次に固定したものを動かす」と考えたうえで、各点が実際に到達できるかを最大値・最小値ではさんで判定するのが要点。",
  "ex": r"点 P が円 $x^2+y^2=4$ 上を、点 Q が $x$ 軸上の線分 $-1\leqq x\leqq1$ 上を動くとき、線分 PQ の中点の存在範囲の面積を求めよ。",
  "exa": r"$\dfrac\pi3+2+\dfrac{\sqrt3}2$（線分 $y=0$，$-\frac12\leqq x\leqq\frac12$ からの距離が $1$ 以下の部分から、2円 $\left(x\pm\frac12\right)^2+y^2=1$ の内部の共通部分を除いたもの）"},
 {"lv": 5, "title": "点を通る直線の本数による平面の分類",
  "q": r"$t$ が $0\leqq t\leqq1$ の範囲を動くとき、直線 $\ell_t:\ y=2tx-t^2$ を考える。平面上の点 $(X,\ Y)$ を通る $\ell_t$ の本数を $N$ とする。<br>(1) $N\geqq1$ となる点の範囲（$\ell_t$ の通過領域）を図示せよ。<br>(2) $N=2$ となる点の範囲、$N=1$ となる点の範囲をそれぞれ求めよ。",
  "hint": r"$N$ は「$t$ の2次方程式 $g(t)=t^2-2Xt+Y=0$ の $0\leqq t\leqq1$ にある異なる解の個数」。$g(0)g(1)$ の符号で分けると見通しがよい：負なら区間内の解はちょうど1つ、正なら0個か2個（重解を含む）、0なら端点が解。",
  "sol": _F86 + r"$N$ は $g(t)=t^2-2Xt+Y=0$ の $0\leqq t\leqq1$ における異なる実数解の個数。$g(0)=Y$，$g(1)=1-2X+Y$，軸は $t=X$，$\dfrac D4=X^2-Y$。<br>"
         r"(1) $X$ を固定すると $Y=-(t-X)^2+X^2$ $(0\leqq t\leqq1)$ の値域は、最大値が $X\leqq0$ で $0$，$0\leqq X\leqq1$ で $X^2$，$X\geqq1$ で $2X-1$；最小値が $X\leqq\dfrac12$ で $2X-1$，$X\geqq\dfrac12$ で $0$。よって通過領域は<br>"
         r"　$X\leqq0$：$2X-1\leqq Y\leqq0$，$0\leqq X\leqq\dfrac12$：$2X-1\leqq Y\leqq X^2$，$\dfrac12\leqq X\leqq1$：$0\leqq Y\leqq X^2$，$X\geqq1$：$0\leqq Y\leqq2X-1$<br>"
         r"（図の網目部分全体，境界を含む）<br>"
         r"(2) (i) $g(0)g(1)\lt0$ のとき、$g$ は $0\lt t\lt1$ にちょうど1つの解をもち、他の解は区間外：$N=1$。<br>"
         r"(ii) $g(0)g(1)\gt0$ のとき、区間内の解は0個か2個（重解は1個と数える）。区間内に解があるのは $\dfrac D4\geqq0$ かつ $0\lt X\lt1$ のときで、$\dfrac D4\gt0$ なら $N=2$，$\dfrac D4=0$ なら重解 $t=X$ で $N=1$。<br>"
         r"(iii) $g(0)=0$（$Y=0$）のとき、解は $t=0,\ 2X$。$0\lt2X\leqq1$ なら $N=2$，それ以外は $N=1$。<br>"
         r"　$g(1)=0$（$Y=2X-1$）のとき、解は $t=1,\ 2X-1$。$0\leqq2X-1\lt1$ なら $N=2$，それ以外は $N=1$。<br>"
         r"以上をまとめると<br>"
         r"　<b>$\boldsymbol{N=2}$：$\boldsymbol{0\lt X\lt1,\ \ Y\lt X^2,\ \ Y\geqq0,\ \ Y\geqq2X-1}$</b>（図の赤い部分。放物線上は含まず、2つの線分上は含む）<br>"
         r"　<b>$\boldsymbol{N=1}$：2直線 $\boldsymbol{y=0}$，$\boldsymbol{y=2x-1}$ の間の部分 $\boldsymbol{Y(Y-2X+1)\leqq0}$ から2つの線分 $\boldsymbol{Y=0\ (0\lt X\leqq\frac12)}$，$\boldsymbol{Y=2X-1\ (\frac12\leqq X\lt1)}$ を除き、放物線の弧 $\boldsymbol{Y=X^2\ (0\leqq X\leqq1)}$ を加えたもの</b>（図の青い部分と赤い弧）",
  "note": r"$g(0)g(1)=Y(Y-2X+1)$ なので、(i) は2直線の「間」の部分。$\ell_0:\ y=0$，$\ell_1:\ y=2x-1$ はそれぞれ放物線 $y=x^2$ の原点，点 $(1,\ 1)$ における接線であり、各 $\ell_t$ は放物線に点 $(t,\ t^2)$ で接する。放物線の弧と2接線で囲まれた部分の点からは2本、その外の「くさび形」の部分からは1本の接線が引ける、と読むこともできる。端点の扱い（白丸・黒丸）までふくめて答えること。",
  "ex": r"$t$ が $-1\leqq t\leqq1$ の範囲を動くとき、点 $(X,\ Y)$ を通る直線 $y=2tx-t^2$ がちょうど2本あるような点の範囲を求めよ。",
  "exa": r"$|X|\lt1$，$2|X|-1\leqq Y\lt X^2$"},
]})


def _v8():
    rnd = random.Random(8)
    # 8.1 逆像法の結論を数値で
    for _ in range(4000):
        X, Y = rnd.uniform(-3, 3), rnd.uniform(-3, 10)
        if abs(Y - X * X - 1) < 1e-6:
            continue
        ok = any(abs(Y - (2 * a * X - a * a + 1)) < 1e-12 for a in [X + math.sqrt(max(X * X - Y + 1, 0)), X - math.sqrt(max(X * X - Y + 1, 0))]) and X * X - Y + 1 >= 0
        assert ok == (Y <= X * X + 1)
        D = (X - 2) ** 2 + 4 * Y
        assert (D >= 0) == (Y >= -(X - 2) ** 2 / 4)
    # 8.2
    x, y, s = symbols("x y s")
    assert expand(x ** 2 + x * y + y ** 2 - ((x + y) ** 2 - x * y)) == 0
    pts = []
    for _ in range(60000):
        a, b = rnd.uniform(-2.1, 2.1), rnd.uniform(-2.1, 2.1)
        if a * a + a * b + b * b <= 3:
            X, Y = a + b, a * b
            assert X * X - 3 - 1e-12 <= Y <= X * X / 4 + 1e-12
            pts.append(X + Y)
    assert max(pts) <= 3 + 1e-12 and min(pts) >= -13 / 4 - 1e-12 and max(pts) > 2.95 and min(pts) < -3.2
    r1, r2 = (-1 + 3 * 5 ** .5) / 4, (-1 - 3 * 5 ** .5) / 4
    assert _close(r1 * r1 + r1 * r2 + r2 * r2, 3) and _close(r1 + r2 + r1 * r2, -13 / 4)
    for _ in range(20000):        # 逆：範囲内の (X,Y) から実数 x,y が作れる
        X = rnd.uniform(-2, 2); Y = rnd.uniform(X * X - 3, X * X / 4)
        dd = X * X - 4 * Y
        a, b = (X + math.sqrt(dd)) / 2, (X - math.sqrt(dd)) / 2
        assert a * a + a * b + b * b <= 3 + 1e-9
    vals = [(math.cos(t) + math.sin(t)) - math.cos(t) * math.sin(t) for t in [2 * math.pi * i / 40000 for i in range(40000)]]
    assert abs(max(vals) - 1) < 1e-8 and abs(min(vals) - (-2 ** .5 - 0.5)) < 1e-8      # 境界上で最大最小（内部は X-Y の極値なし）
    for _ in range(20000):
        a, b = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if a * a + b * b <= 1:
            X, Y = a + b, a * b
            assert (X * X - 1) / 2 - 1e-12 <= Y <= X * X / 4 + 1e-12 and -2 ** .5 - 0.5 - 1e-12 <= X - Y <= 1 + 1e-12
    # 8.3 x を固定して a を細かく動かした値域と一致
    for (lo, hi, fam, L, U) in [(-1, 2, lambda xx, a: xx * xx - 2 * a * xx + 2 * a * a, _L83, _U83),
                                (0, 2, lambda xx, a: (xx - a) ** 2 + a,
                                 lambda xx: xx * xx if xx < 0.5 else (xx - 0.25 if xx <= 2.5 else xx * xx - 4 * xx + 6),
                                 lambda xx: xx * xx - 4 * xx + 6 if xx <= 1.5 else xx * xx)]:
        for i in range(-400, 601):
            xx = i / 100
            v = [fam(xx, lo + (hi - lo) * j / 3000) for j in range(3001)]
            assert abs(min(v) - L(xx)) < 1e-5 and abs(max(v) - U(xx)) < 1e-9
    # 8.4 線分の通過領域：(X,Y) を通る線分があるか（2次方程式 Y t^2 - t + X = 0 の解 t∈[lo,hi], X<=t）
    def seg_hit(X, Y, lo, hi):
        if X < 0 or Y < 0:
            return False
        if Y == 0:
            return lo <= X <= hi
        D = 1 - 4 * X * Y
        if D < 0:
            return False
        for t in [(1 + math.sqrt(D)) / (2 * Y), (1 - math.sqrt(D)) / (2 * Y)]:
            if lo - 1e-12 <= t <= hi + 1e-12 and X <= t + 1e-12:
                return True
        return False

    def reg84(X, Y):
        if 0 <= X <= 0.5: return -X / 4 + 0.5 <= Y <= 1 - X
        if 0.5 <= X <= 2 / 3: return -X / 4 + 0.5 <= Y <= 1 / (4 * X)
        if 2 / 3 <= X <= 1: return 1 - X <= Y <= 1 / (4 * X)
        if 1 <= X <= 2: return 0 <= Y <= 0.5 - X / 4
        return False

    def reg84e(X, Y):
        if 0 <= X <= 0.5: return 1 / 3 - X / 9 <= Y <= 1 - X
        if 0.5 <= X <= 0.75: return 1 / 3 - X / 9 <= Y <= 1 / (4 * X)
        if 0.75 <= X <= 1: return 1 - X <= Y <= 1 / (4 * X)
        if 1 <= X <= 1.5: return 0 <= Y <= 1 / (4 * X)
        if 1.5 <= X <= 3: return 0 <= Y <= 1 / 3 - X / 9
        return False
    n = 0
    for _ in range(60000):
        X, Y = rnd.uniform(-0.2, 3.2), rnd.uniform(-0.2, 1.2)
        a, b = seg_hit(X, Y, 1, 2), reg84(X, Y)
        if a != b:
            # 境界すれすれだけ許す
            assert min(abs(Y - (1 - X)), abs(Y + X / 4 - 0.5), abs(Y - 1 / (4 * X)) if X > 0 else 1, abs(Y), abs(X)) < 1e-9
        n += a
        a, b = seg_hit(X, Y, 1, 3), reg84e(X, Y)
        if a != b:
            assert min(abs(Y - (1 - X)), abs(Y + X / 9 - 1 / 3), abs(Y - 1 / (4 * X)) if X > 0 else 1, abs(Y), abs(X)) < 1e-9
    assert n > 1000
    # 8.5 存在範囲と面積
    def reach(X, Y, s0, rr):
        h = lambda s_: (X - s_) ** 2 + (Y - 1) ** 2 if rr == 0.5 else (X - s_) ** 2 + Y ** 2
        r2 = rr * rr
        sm = min(max(X, -s0), s0)
        return h(sm) <= r2 <= max(h(-s0), h(s0))
    for _ in range(3000):      # 実際の P,Q から作った中点はすべて範囲内
        th, q = rnd.uniform(0, 2 * math.pi), rnd.uniform(-0.5, 0.5)
        X, Y = (math.cos(th) + q) / 2, (math.sin(th) + 2) / 2
        assert reach(X, Y, 0.25, 0.5)
    for _ in range(3000):      # 範囲内の点から P,Q を復元できる
        X, Y = rnd.uniform(-0.8, 0.8), rnd.uniform(0.4, 1.6)
        if reach(X, Y, 0.25, 0.5):
            ok = False
            for j in range(2001):
                s_ = -0.25 + 0.5 * j / 2000
                if abs(math.hypot(2 * X - 2 * s_, 2 * Y - 2) - 1) < 2e-3:
                    ok = True
                    break
            assert ok
    for (s0, rr, yc, area) in [(0.25, 0.5, 1, 0.5 + math.pi / 12 + 3 ** .5 / 8), (0.5, 1.0, 0, math.pi / 3 + 2 + 3 ** .5 / 2)]:
        Nn = 700
        lo_x, hi_x = -s0 - rr, s0 + rr
        cnt = 0
        for i in range(Nn):
            for j in range(Nn):
                X = lo_x + (hi_x - lo_x) * (i + 0.5) / Nn
                Y = yc - rr + 2 * rr * (j + 0.5) / Nn
                if rr == 0.5:
                    cnt += reach(X, Y, s0, rr)
                else:
                    cnt += reach(X, Y, s0, rr)
        est = cnt * (hi_x - lo_x) * 2 * rr / Nn ** 2
        assert abs(est - area) < 3e-3
    # 8.6 本数の分類
    def N(X, Y, lo, hi):
        D = X * X - Y
        if D < 0:
            return 0
        rts = {X + math.sqrt(D), X - math.sqrt(D)}
        return sum(1 for t in rts if lo - 1e-12 <= t <= hi + 1e-12)
    for _ in range(40000):
        X, Y = rnd.uniform(-1, 2), rnd.uniform(-2, 2)
        n_ = N(X, Y, 0, 1)
        n2 = (0 < X < 1) and Y < X * X and Y >= 0 and Y >= 2 * X - 1
        n1 = (Y * (Y - 2 * X + 1) <= 0)
        if abs(X * X - Y) < 1e-9 or abs(Y) < 1e-9 or abs(Y - 2 * X + 1) < 1e-9:
            continue
        assert (n_ == 2) == n2 and (n_ == 1) == n1
        fixed = (2 * X - 1 <= Y <= 0) if X <= 0 else (2 * X - 1 <= Y <= X * X) if X <= 0.5 else (0 <= Y <= X * X) if X <= 1 else (0 <= Y <= 2 * X - 1)
        assert (n_ >= 1) == fixed
        n_e = N(X, Y, -1, 1)
        assert (n_e == 2) == (abs(X) < 1 and 2 * abs(X) - 1 <= Y < X * X)
    # 境界上の点（線分・弧）
    for X in [0.1, 0.3, 0.5]:
        assert N(X, 0.0, 0, 1) == 2
    for X in [0.6, 0.8, 0.95, -0.4]:
        assert N(X, 0.0, 0, 1) == (2 if 0 < 2 * X <= 1 else 1)
    for X in [0.5, 0.7, 0.9]:
        assert N(X, 2 * X - 1, 0, 1) == 2
    for X in [0.2, 1.0, 1.4]:
        assert N(X, 2 * X - 1, 0, 1) == 1
    for X in [0.0, 0.3, 0.7, 1.0]:
        assert N(X, X * X, 0, 1) == 1


_V.append(_v8)

CH = {"no": 11, "sections": SEC}


def verify():
    for f in _V:
        f()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 42 <= len(items) <= 48, len(items)
    assert cnt[5] >= 5 and all(cnt[k] >= 3 for k in cnt), cnt
    assert 4 <= len(SEC) <= 9
    for s in SEC:
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]
        for it in s["items"]:
            for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(k), (s["title"], it.get("title"), k)
            for k in ("q", "hint", "sol", "note", "ex", "exa", "title"):
                v = it.get(k) or ""
                assert "$$" not in v and v.count("$") % 2 == 0, (it["title"], k)
