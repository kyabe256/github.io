r"""第24章 微分法の応用（数学III）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。
範囲：接線・法線、平均値の定理、増減・極値、凹凸・変曲点・漸近線・グラフの概形、最大最小、
方程式の実数解の個数、不等式の証明、速度・加速度、近似式（積分は使わない）。図の座標はすべて Python で計算する。"""
import math
import random
from sympy import (symbols, Rational, sqrt, sin, cos, tan, exp, log, pi, E, S, oo,
                   diff, limit, simplify, expand, factor, solve, series, cbrt, nsimplify, N, lambdify)

SEC = []

# ---------------------------------------------------------------- 図の道具
C1, C2, CG, CF = "#16367a", "#d9701e", "#888888", "#c9daf3"
DASH = ' stroke-dasharray="3,2"'


class _G:
    """数学座標で描いて SVG 文字列にする小さな道具。"""

    def __init__(s, W, H, xr, yr, m=12):
        s.W, s.H, s.m = W, H, m
        s.x0, s.x1 = xr
        s.y0, s.y1 = yr
        s.sx = (W - 2 * m) / (s.x1 - s.x0)
        s.sy = (H - 2 * m) / (s.y1 - s.y0)
        s.o = []

    def X(s, x):
        return round(s.m + (x - s.x0) * s.sx, 1)

    def Y(s, y):
        return round(s.m + (s.y1 - y) * s.sy, 1)

    def axes(s, xl="x", yl="y", o="O"):
        X0, Y0 = s.X(0), s.Y(0)
        xa, xb, ya, yb = s.X(s.x0), s.X(s.x1), s.Y(s.y0), s.Y(s.y1)
        s.o.append(f'<line x1="{xa}" y1="{Y0}" x2="{xb}" y2="{Y0}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{xb + 3},{Y0} {xb - 3},{Y0 - 2.6} {xb - 3},{Y0 + 2.6}" fill="#333"/>')
        s.o.append(f'<line x1="{X0}" y1="{ya}" x2="{X0}" y2="{yb}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{X0},{yb - 3} {X0 - 2.6},{yb + 3} {X0 + 2.6},{yb + 3}" fill="#333"/>')
        s.o.append(f'<text x="{xb - 1}" y="{Y0 - 4}" text-anchor="end" font-style="italic" font-family="serif" font-size="11">{xl}</text>')
        s.o.append(f'<text x="{X0 + 5}" y="{yb + 6}" font-style="italic" font-family="serif" font-size="11">{yl}</text>')
        if o:
            s.o.append(f'<text x="{X0 - 3}" y="{Y0 + 10}" text-anchor="end" font-style="italic" font-family="serif" font-size="10">{o}</text>')

    def _poly(s, pts, col, w, dash):
        if len(pts) > 1:
            s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{dash} points="'
                       + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts) + '"/>')

    def curve(s, f, a, b, col=C1, w=1.4, dash="", n=300):
        """y=f(x)（a≦x≦b，連続な部分ごとに呼ぶ）。枠の上下からはみ出す部分は切る。"""
        segs, cur, prev = [], [], None
        for i in range(n + 1):
            x = a + (b - a) * i / n
            y = f(x)
            ins = s.y0 <= y <= s.y1
            if prev is not None and ins != prev[2]:
                px, py, _ = prev
                yb = s.y1 if max(py, y) > s.y1 else s.y0
                xb = px + (x - px) * (yb - py) / (y - py)
                cur.append((xb, yb))
                if not ins:
                    segs.append(cur)
                    cur = []
            if ins:
                cur.append((x, y))
            prev = (x, y, ins)
        if cur:
            segs.append(cur)
        for sg in segs:
            s._poly(sg, col, w, dash)

    def pcurve(s, fx, fy, t0, t1, col=C1, w=1.4, dash="", n=300):
        s._poly([(fx(t0 + (t1 - t0) * i / n), fy(t0 + (t1 - t0) * i / n)) for i in range(n + 1)], col, w, dash)

    def seg(s, p, q, col=CG, w=0.8, dash=DASH):
        s.o.append(f'<line x1="{s.X(p[0])}" y1="{s.Y(p[1])}" x2="{s.X(q[0])}" y2="{s.Y(q[1])}" stroke="{col}" stroke-width="{w}"{dash}/>')

    def arrow(s, p, q, col=C2, w=1.2):
        x1, y1, x2, y2 = s.X(p[0]), s.Y(p[1]), s.X(q[0]), s.Y(q[1])
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"/>')
        a1 = (round(x2 - 6 * ux + 2.6 * uy, 1), round(y2 - 6 * uy - 2.6 * ux, 1))
        a2 = (round(x2 - 6 * ux - 2.6 * uy, 1), round(y2 - 6 * uy + 2.6 * ux, 1))
        s.o.append(f'<polygon points="{x2},{y2} {a1[0]},{a1[1]} {a2[0]},{a2[1]}" fill="{col}"/>')

    def pt(s, x, y, col=C1, r=1.9, hollow=False):
        if hollow:
            s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="#fff" stroke="{col}" stroke-width="1"/>')
        else:
            s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="{col}"/>')

    def txt(s, x, y, t, dx=0, dy=0, anc="middle", it=False, size=10, col="#222"):
        if it:
            st = ' font-style="italic" font-family="serif"'
        else:
            st = "" if any(ord(ch) > 0x3000 for ch in t) else ' font-family="serif"'
        s.o.append(f'<text x="{round(s.X(x) + dx, 1)}" y="{round(s.Y(y) + dy, 1)}" text-anchor="{anc}" font-size="{size}" fill="{col}"{st}>{t}</text>')

    def fill(s, P, col=CF, op=0.85):
        s.o.append('<polygon points="' + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in P)
                   + f'" fill="{col}" fill-opacity="{op}" stroke="none"/>')

    def xtick(s, x, t, dy=11, it=True):
        s.o.append(f'<line x1="{s.X(x)}" y1="{s.Y(0) - 2}" x2="{s.X(x)}" y2="{s.Y(0) + 2}" stroke="#333" stroke-width="0.8"/>')
        s.txt(x, 0, t, dy=dy, size=10, it=it)

    def ytick(s, y, t, dx=-4, it=True):
        s.o.append(f'<line x1="{s.X(0) - 2}" y1="{s.Y(y)}" x2="{s.X(0) + 2}" y2="{s.Y(y)}" stroke="#333" stroke-width="0.8"/>')
        s.txt(0, y, t, dx=dx, dy=3.5, anc="end", size=10, it=it)

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" font-size="10">'
                + "".join(s.o) + "</svg>")


def _tb(*rows):
    """増減表。rows の各行は [見出し, セル, ...]。"""
    h = "<table>"
    for r in rows:
        h += "<tr><th>" + r[0] + "</th>" + "".join("<td>" + c + "</td>" for c in r[1:]) + "</tr>"
    return h + "</table>"


UP, DN, DOT = r"$\nearrow$", r"$\searrow$", r"$\cdots$"

x, y, t, a, b, u = symbols("x y t a b u", real=True)


def _z(e, lo=0.3, hi=2.5):
    """式 e が恒等的に 0 か（sympy で簡約できなければ数値で多点確認）。"""
    if simplify(e) == 0:
        return True
    fs = sorted(e.free_symbols, key=str)
    f = lambdify(fs, e, "math")
    for _ in range(40):
        v = [random.uniform(lo, hi) for _ in fs]
        if abs(f(*v)) > 1e-9:
            return False
    return True


def _count(F, xs):
    """標本点 xs 上で F の符号の変化の回数（解の個数の数値確認用。重解の場合には使わない）。"""
    vals = [w for w in (F(v) for v in xs) if w != 0]
    return sum(1 for p, q in zip(vals, vals[1:]) if (p < 0) != (q < 0))


def _grid(lo, hi, n=20000):
    return [lo + (hi - lo) * i / n for i in range(n + 1)]


def _geo(lo, hi, n=20000):
    """正の区間 [lo, hi] の対数的に等間隔な標本点。"""
    return [lo * (hi / lo) ** (i / n) for i in range(n + 1)]


def _bis(F, lo, hi, it=200):
    flo = F(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = F(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- 節1 の図
def _fig15():
    g = _G(200, 140, (-0.25, 3.4), (-0.75, 1.45))
    g.axes("t", "u")
    h = lambda v: v * (1 - math.log(v))
    g.curve(h, 1e-6, 3.4)
    g.seg((0, 1), (1, 1))
    g.seg((1, 0), (1, 1))
    g.pt(1, 1)
    g.xtick(1, "1")
    g.txt(math.e, 0, "e", dx=2, dy=-4, it=True)
    g.ytick(1, "1")
    g.seg((-0.2, 0.55), (3.35, 0.55), col=C2, w=1.0, dash="")
    g.txt(3.35, 0.55, "u=a", dy=-4, anc="end", it=True, col=C2)
    g.txt(2.3, -0.55, "u=t(1−log t)", it=True, size=9.5, col=C1)
    return g.svg()


# ---------------------------------------------------------------- 節1
SEC.append({"title": r"接線と法線",
"base": r"""・曲線 $y=f(x)$ 上の点 $(a,\ f(a))$ における接線：$y-f(a)=f'(a)(x-a)$<br>
・法線：$f'(a)\neq0$ のとき $y-f(a)=-\dfrac{1}{f'(a)}(x-a)$（$f'(a)=0$ のときは $x=a$）<br>
・曲線外の点から引く接線：接点を $(t,\ f(t))$ とおき、接線がその点を通る条件から $t$ を決める<br>
・2曲線 $y=f(x)$，$y=g(x)$ が $x=t$ の点で接する $\iff$ $f(t)=g(t)$ かつ $f'(t)=g'(t)$<br>
・陰関数・媒介変数表示の曲線も、$\dfrac{dy}{dx}$ を求めれば同じ式で接線が書ける""",
"items": [
 {"lv": 1, "title": r"曲線上の点における接線と法線",
  "q": r"曲線 $y=x\log x$ 上の点 $(e,\ e)$ における接線と法線の方程式を求めよ。",
  "hint": r"接線の傾きは $y'$ の $x=e$ での値 $m$。法線は接線に垂直なので、傾きは $-\dfrac1m$ になる。",
  "sol": r"$y'=\log x+x\cdot\dfrac1x=\log x+1$ より、$x=e$ のとき $y'=2$。<br>"
         r"接線：$y-e=2(x-e)$ より　$\boldsymbol{y=2x-e}$<br>"
         r"法線：$y-e=-\dfrac12(x-e)$ より　$\boldsymbol{y=-\dfrac12x+\dfrac32e}$",
  "note": r"法線の方程式は $(x-a)+f'(a)\{y-f(a)\}=0$ と書くと、$f'(a)=0$ の場合（法線 $x=a$）も含めて1つの式で表せる。",
  "ex": r"曲線 $y=xe^{x}$ 上の点 $(1,\ e)$ における接線と法線の方程式を求めよ。",
  "exa": r"接線 $y=2ex-e$，法線 $y=-\dfrac{1}{2e}x+e+\dfrac{1}{2e}$"},
 {"lv": 1, "title": r"曲線外の点から引いた接線",
  "q": r"点 $(1,\ 0)$ から曲線 $y=e^{x}$ に引いた接線の方程式と、接点の座標を求めよ。",
  "hint": r"点 $(1,\ 0)$ は曲線上にない。接点を $(t,\ e^t)$ とおいて接線の方程式をつくり、それが $(1,\ 0)$ を通る条件から $t$ を決める。",
  "sol": r"$y'=e^x$ より、接点 $(t,\ e^t)$ における接線は $y-e^t=e^t(x-t)$，すなわち $y=e^tx+(1-t)e^t$。<br>"
         r"これが点 $(1,\ 0)$ を通るから　$0=e^t+(1-t)e^t=(2-t)e^t$<br>"
         r"$e^t>0$ より $t=2$。よって　接線 $\boldsymbol{y=e^2x-e^2}$，接点 $\boldsymbol{(2,\ e^2)}$",
  "note": r"「点 $(1,\ 0)$ における接線」と取り違えて $x=1$ での微分係数を使うのは典型的な誤り。曲線外の点を通る接線は、必ず接点を文字でおく。",
  "ex": r"原点から曲線 $y=\log x$ に引いた接線の方程式と、接点の座標を求めよ。",
  "exa": r"$y=\dfrac1ex$，接点 $(e,\ 1)$"},
 {"lv": 2, "title": r"2曲線が接する条件",
  "q": r"2曲線 $y=ax^2$ と $y=\log x$ が接するとき、定数 $a$ の値と接点の座標を求めよ。また、接点における共通の接線の方程式を求めよ。",
  "hint": r"$x=t$ の点で接する $\iff$ 「$y$ 座標が等しい」かつ「接線の傾きが等しい」。2つの式から $a$ を消去して $t$ を求める。",
  "sol": r"$f(x)=ax^2$，$g(x)=\log x$ とすると $f'(x)=2ax$，$g'(x)=\dfrac1x$。$x=t\ (t>0)$ の点で接するとすると<br>"
         r"$at^2=\log t$ …①，　$2at=\dfrac1t$ …②<br>"
         r"②より $at^2=\dfrac12$。①に代入して $\log t=\dfrac12$，$t=\sqrt e$。よって $a=\dfrac{1}{2t^2}=\boldsymbol{\dfrac{1}{2e}}$，接点は $\boldsymbol{\left(\sqrt e,\ \dfrac12\right)}$。<br>"
         r"接線の傾きは $g'(\sqrt e)=\dfrac{1}{\sqrt e}$ だから　$y-\dfrac12=\dfrac{1}{\sqrt e}(x-\sqrt e)$，すなわち　$\boldsymbol{y=\dfrac{x}{\sqrt e}-\dfrac12}$",
  "note": r"異なる点で接する共通接線を求めるときは、それぞれの接点を $(s,\ f(s))$，$(t,\ g(t))$ とおき、2本の接線の方程式の傾きと切片を比べる。「同じ点で接する」と「共通接線をもつ」の区別に注意。",
  "ex": r"2曲線 $y=\sqrt x$ と $y=a\log x$ が接するとき、定数 $a$ の値と接点の座標を求めよ。",
  "exa": r"$a=\dfrac e2$，接点 $(e^2,\ e)$"},
 {"lv": 3, "title": r"陰関数で表された曲線の接線",
  "q": r"$a$ を正の定数とする。曲線 $\sqrt x+\sqrt y=\sqrt a$ 上の点 $(p,\ q)$（$p>0$，$q>0$）における接線が $x$ 軸，$y$ 軸と交わる点をそれぞれ $\mathrm A$，$\mathrm B$ とするとき、$\mathrm{OA}+\mathrm{OB}$ は点のとり方によらず一定であることを示せ。",
  "hint": r"$y$ を $x$ の関数とみて、両辺を $x$ で微分する（陰関数の微分）と $\dfrac{dy}{dx}$ が $x,\ y$ で表せる。接線の切片を求め、条件 $\sqrt p+\sqrt q=\sqrt a$ を使う。",
  "sol": r"$x>0,\ y>0$ で両辺を $x$ で微分すると　$\dfrac{1}{2\sqrt x}+\dfrac{1}{2\sqrt y}\cdot\dfrac{dy}{dx}=0$，よって $\dfrac{dy}{dx}=-\dfrac{\sqrt y}{\sqrt x}$。<br>"
         r"点 $(p,\ q)$ における接線は　$y-q=-\dfrac{\sqrt q}{\sqrt p}(x-p)$<br>"
         r"$y=0$ とおくと $x=p+\sqrt p\sqrt q=\sqrt p(\sqrt p+\sqrt q)=\sqrt{a}\sqrt{p}$，<br>"
         r"$x=0$ とおくと $y=q+\sqrt p\sqrt q=\sqrt q(\sqrt p+\sqrt q)=\sqrt{a}\sqrt{q}$。<br>"
         r"よって　$\mathrm{OA}+\mathrm{OB}=\sqrt a(\sqrt p+\sqrt q)=\sqrt a\cdot\sqrt a=\boldsymbol{a}$（一定）　$\blacksquare$",
  "note": r"接線は $\dfrac{x}{\sqrt p}+\dfrac{y}{\sqrt q}=\sqrt a$ と整理できる。曲線を $y=(\sqrt a-\sqrt x)^2$（$0\leqq x\leqq a$）と表して普通に微分してもよいが、陰関数のまま微分する方が計算が軽い。",
  "ex": r"曲線 $x^{\frac23}+y^{\frac23}=1$（$x>0$，$y>0$）上の点 $\mathrm P$ における接線が $x$ 軸，$y$ 軸と交わる点を $\mathrm A$，$\mathrm B$ とするとき、線分 $\mathrm{AB}$ の長さは一定であることを示せ。",
  "exa": r"$\mathrm P(p,\ q)$ における接線は $\dfrac{x}{\sqrt[3]p}+\dfrac{y}{\sqrt[3]q}=1$。$\mathrm{OA}=\sqrt[3]p$，$\mathrm{OB}=\sqrt[3]q$ より $\mathrm{AB}^2=p^{\frac23}+q^{\frac23}=1$，$\mathrm{AB}=1$（一定）"},
 {"lv": 3, "title": r"曲線外の点から引ける接線の本数",
  "q": r"$a$ を定数とする。点 $(a,\ 0)$ から曲線 $y=\log x$ に引ける接線の本数を求めよ。",
  "hint": r"接点を $(t,\ \log t)$ とおくと、接線が $(a,\ 0)$ を通る条件は $t$ の方程式になる。「接点が異なれば接線も異なる」ことを確かめれば、接線の本数＝その方程式の実数解 $t\ (t>0)$ の個数。定数 $a$ を分離してグラフで数える。",
  "sol": _fig15() +
         r"接点 $(t,\ \log t)$（$t>0$）における接線は $y=\dfrac1t(x-t)+\log t$。これが $(a,\ 0)$ を通る条件は<br>"
         r"$0=\dfrac at-1+\log t$，すなわち　$a=t(1-\log t)$ …①<br>"
         r"接線の傾き $\dfrac1t$ は $t$ ごとに異なるから、接点が異なれば接線も異なる。よって、接線の本数は①を満たす $t>0$ の個数に等しい。<br>"
         r"$h(t)=t(1-\log t)$ とおくと $h'(t)=(1-\log t)-1=-\log t$。$0<t<1$ で $h'(t)>0$，$t>1$ で $h'(t)<0$ だから、$h(t)$ は $t=1$ で最大値 $h(1)=1$ をとる。<br>"
         r"また $\displaystyle\lim_{t\to+0}h(t)=\lim_{t\to+0}(t-t\log t)=0$，$\displaystyle\lim_{t\to\infty}h(t)=-\infty$。<br>"
         r"$u=h(t)$ のグラフ（図）と直線 $u=a$ の共有点の個数を調べて<br>"
         r"$\boldsymbol{a>1}$ のとき $\boldsymbol{0}$ 本，$\boldsymbol{a=1}$ のとき $\boldsymbol{1}$ 本，$\boldsymbol{0<a<1}$ のとき $\boldsymbol{2}$ 本，$\boldsymbol{a\leqq0}$ のとき $\boldsymbol{1}$ 本",
  "note": r"変曲点をもつ曲線（3次関数のグラフなど）では、1本の直線が2点で接することがないかを別に確かめる必要がある。$y=\log x$ は傾き $\dfrac1x$ が単調に変化する（つねに上に凸）ので、その心配はない。$0<a<1$ のとき点 $(a,\ 0)$ は曲線の上側にあって2本、$a>1$ のとき下側にあって0本。$a\leqq0$ のときは、$t\to+0$ で $h(t)\to0$ となるため $0<t<1$ の側の接点が現れず1本になる（$y$ 軸が漸近線であることに対応する）。",
  "ex": r"$b$ を定数とする。点 $(0,\ b)$ から曲線 $y=e^{x}$ に引ける接線の本数を求めよ。",
  "exa": r"$b>1$ のとき0本，$b=1$ のとき1本，$0<b<1$ のとき2本，$b\leqq0$ のとき1本"},
]})


def _v1():
    # 接線・法線
    f = x * log(x)
    m = diff(f, x).subs(x, E)
    assert m == 2
    assert simplify((2 * x - E).subs(x, E) - E) == 0
    assert simplify((-x / 2 + Rational(3, 2) * E).subs(x, E) - E) == 0
    g = x * exp(x)
    m = diff(g, x).subs(x, 1)
    assert simplify(m - 2 * E) == 0
    assert simplify((2 * E * x - E).subs(x, 1) - E) == 0
    nl = -x / (2 * E) + E + 1 / (2 * E)
    assert simplify(nl.subs(x, 1) - E) == 0 and simplify(diff(nl, x) * m + 1) == 0
    # 外の点から
    T = exp(t) * x + (1 - t) * exp(t)
    assert simplify(T.subs(x, 1)) == simplify((2 - t) * exp(t))
    assert solve((2 - t) * exp(t), t) == [2]
    assert simplify(T.subs(t, 2) - (exp(2) * x - exp(2))) == 0
    Tl = (x - t) / t + log(t)
    assert solve(Tl.subs(x, 0), t) == [E]
    assert simplify(Tl.subs(t, E) - x / E) == 0
    # 2曲線が接する
    tt = sqrt(E)
    aa = 1 / (2 * E)
    assert simplify(aa * tt**2 - log(tt)) == 0 and simplify(2 * aa * tt - 1 / tt) == 0
    assert simplify((1 / sqrt(E) * (x - sqrt(E)) + Rational(1, 2)) - (x / sqrt(E) - Rational(1, 2))) == 0
    tt, aa = E**2, E / 2
    assert simplify(sqrt(tt) - aa * log(tt)) == 0 and simplify(1 / (2 * sqrt(tt)) - aa / tt) == 0
    # 陰関数：√x+√y=√a の接線の切片和
    for _ in range(200):
        A = random.uniform(0.5, 9)
        p = random.uniform(0.01, A * 0.99)
        q = (math.sqrt(A) - math.sqrt(p)) ** 2
        mm = -math.sqrt(q) / math.sqrt(p)
        h = 1e-6
        num = ((math.sqrt(A) - math.sqrt(p + h)) ** 2 - (math.sqrt(A) - math.sqrt(p - h)) ** 2) / (2 * h)
        assert abs(num - mm) < 1e-5 * max(1, abs(mm))
        xA = p - q / mm
        yB = q - mm * p
        assert abs(xA + yB - A) < 1e-9 * A
        assert abs(p / math.sqrt(p) + q / math.sqrt(q) - math.sqrt(A)) < 1e-9
        # アステロイド
        P = random.uniform(0.01, 0.99)
        Q = (1 - P ** (2 / 3)) ** 1.5
        mm = -(Q / P) ** (1 / 3)
        num = ((1 - (P + h) ** (2 / 3)) ** 1.5 - (1 - (P - h) ** (2 / 3)) ** 1.5) / (2 * h)
        assert abs(num - mm) < 1e-5 * max(1, abs(mm))
        xA, yB = P - Q / mm, Q - mm * P
        assert abs(xA - P ** (1 / 3)) < 1e-9 and abs(yB - Q ** (1 / 3)) < 1e-9
        assert abs(math.hypot(xA, yB) - 1) < 1e-9
    # 接線の本数：a = t(1 - log t) の解の個数
    h = lambda v: v * (1 - math.log(v))
    assert simplify(diff(t * (1 - log(t)), t) + log(t)) == 0
    assert limit(t * (1 - log(t)), t, 0, "+") == 0
    ts = _geo(1e-12, 1e6, 40000)
    for A in [3, 1.5, 1.01, 0.99, 0.5, 0.1, 0.001, -0.001, -1, -50]:
        n = _count(lambda v: h(v) - A, ts)
        exp_n = 0 if A > 1 else (2 if A > 0 else 1)
        assert n == exp_n, (A, n)
    assert max(h(v) for v in ts) <= 1 + 1e-12
    # 練習：b = e^t(1-t)
    k = lambda v: math.exp(v) * (1 - v)
    ts = _grid(-60, 60, 40000)
    for B in [3, 1.01, 0.99, 0.5, 1e-6, 0, -0.5, -100]:
        n = _count(lambda v: k(v) - B, ts)
        exp_n = 0 if B > 1 else (2 if B > 0 else 1)
        assert n == exp_n, (B, n)
    assert max(k(v) for v in ts) <= 1 + 1e-12


# ---------------------------------------------------------------- 節2
SEC.append({"title": r"平均値の定理",
"base": r"""・<b>平均値の定理</b>：$f(x)$ が $a\leqq x\leqq b$ で連続、$a<x<b$ で微分可能ならば、$\dfrac{f(b)-f(a)}{b-a}=f'(c)$，$a<c<b$ を満たす $c$ が存在する（$c=a+\theta(b-a)$，$0<\theta<1$ とも書ける）。<br>
・$f(a)=f(b)$ のときがロルの定理（$f'(c)=0$ となる $c$ が $a$ と $b$ の間にある）。<br>
・使い方：差 $f(b)-f(a)$ を「$f'(c)\times$ 区間の幅」に直す。$c$ の範囲から $f'(c)$ をはさめば不等式、$c$ をはさみうちにすれば極限、$|f'(c)|\leqq k<1$ と評価すれば漸化式 $a_{n+1}=f(a_n)$ の収束が示せる。""",
"items": [
 {"lv": 1, "title": r"平均値の定理を満たす c の値",
  "q": r"関数 $f(x)=\log x$ と区間 $1\leqq x\leqq e$ について、平均値の定理の式 $\dfrac{f(e)-f(1)}{e-1}=f'(c)$，$1<c<e$ を満たす $c$ の値を求めよ。",
  "hint": r"$f'(c)$ を $c$ で表し、弦の傾き $\dfrac{f(e)-f(1)}{e-1}$ と等しいとおく。最後に $c$ が区間の内部にあることを確かめる。",
  "sol": r"$f'(x)=\dfrac1x$ より　$\dfrac{1-0}{e-1}=\dfrac1c$　よって　$\boldsymbol{c=e-1}$<br>"
         r"$e=2.71\cdots$ より $e-1=1.71\cdots$ であり、$1<c<e$ を満たしている。",
  "note": r"平均値の定理は「曲線上の2点を結ぶ弦と平行な接線が、2点の間のどこかで引ける」ことを表している。$c$ の値を具体的に求められるのはこのような特別な場合で、ふつうは $c$ の<b>存在</b>と<b>範囲</b>だけを使う。",
  "ex": r"関数 $f(x)=e^{x}$ と区間 $0\leqq x\leqq1$ について、平均値の定理を満たす $c$ の値を求めよ。",
  "exa": r"$c=\log(e-1)$"},
 {"lv": 2, "title": r"平均値の定理を用いた不等式の証明",
  "q": r"$0<a<b$ のとき、次の不等式を証明せよ。<br>$\dfrac{b-a}{b}<\log\dfrac ba<\dfrac{b-a}{a}$",
  "hint": r"中辺 $\log b-\log a$ は $f(x)=\log x$ の値の差。平均値の定理で $(b-a)f'(c)$ に直し、$a<c<b$ から $f'(c)=\dfrac1c$ をはさむ。",
  "sol": r"$f(x)=\log x$ は $x>0$ で微分可能で $f'(x)=\dfrac1x$。区間 $a\leqq x\leqq b$ で平均値の定理を用いると<br>"
         r"$\log b-\log a=\dfrac{b-a}{c}$，$a<c<b$<br>"
         r"を満たす $c$ が存在する。$0<a<c<b$ より $\dfrac1b<\dfrac1c<\dfrac1a$ で、$b-a>0$ を掛けると<br>"
         r"$\dfrac{b-a}{b}<\dfrac{b-a}{c}<\dfrac{b-a}{a}$<br>"
         r"$\log b-\log a=\log\dfrac ba$ だから　$\dfrac{b-a}{b}<\log\dfrac ba<\dfrac{b-a}{a}$　$\blacksquare$",
  "note": r"$a=1$，$b=1+x$（$x>0$）とすると $\dfrac{x}{1+x}<\log(1+x)<x$ が得られる。差の形 $f(b)-f(a)$ を含む不等式は、まず平均値の定理を疑うとよい。",
  "ex": r"$a<b$ のとき、$e^a(b-a)<e^b-e^a<e^b(b-a)$ を証明せよ。",
  "exa": r"$f(x)=e^x$ に平均値の定理を用いると $e^b-e^a=e^c(b-a)$（$a<c<b$）。$e^a<e^c<e^b$ に $b-a>0$ を掛ければよい。"},
 {"lv": 3, "title": r"平均値の定理を用いた極限",
  "q": r"極限 $\displaystyle\lim_{x\to0}\frac{e^x-e^{\sin x}}{x-\sin x}$ を求めよ。",
  "hint": r"分子は $f(t)=e^t$ の $t=x$ と $t=\sin x$ での値の差。平均値の定理で $e^c(x-\sin x)$ と書けば分母と約分できる。$c$ は $\sin x$ と $x$ の間にあるので、はさみうちで $c\to0$。",
  "sol": r"$x\neq0$ のとき $\sin x\neq x$（$x>0$ で $\sin x<x$，$x<0$ で $\sin x>x$）である。<br>"
         r"$f(t)=e^t$ に、$\sin x$ と $x$ を両端とする区間で平均値の定理を用いると<br>"
         r"$e^x-e^{\sin x}=e^{c}(x-\sin x)$<br>"
         r"を満たす $c$ が $\sin x$ と $x$ の間に存在する。よって　$\dfrac{e^x-e^{\sin x}}{x-\sin x}=e^{c}$<br>"
         r"$x\to0$ のとき $\sin x\to0$ であるから、はさみうちの原理により $c\to0$。したがって<br>"
         r"$\displaystyle\lim_{x\to0}\frac{e^x-e^{\sin x}}{x-\sin x}=e^0=\boldsymbol{1}$",
  "note": r"$\dfrac{f(p)-f(q)}{p-q}$ の形の極限は、平均値の定理で $f'(c)$ に直すのが定石。別解として、分子を $e^{\sin x}\left(e^{x-\sin x}-1\right)$ と変形し、$\displaystyle\lim_{h\to0}\frac{e^h-1}{h}=1$（$h=x-\sin x$）を使ってもよい。",
  "ex": r"極限 $\displaystyle\lim_{x\to\infty}x^2\left(e^{\frac1x}-e^{\frac1{x+1}}\right)$ を求めよ。",
  "exa": r"$1$（平均値の定理より $e^{\frac1x}-e^{\frac1{x+1}}=\dfrac{e^c}{x(x+1)}$，$\dfrac{1}{x+1}<c<\dfrac1x$）"},
 {"lv": 4, "title": r"平均値の定理と漸化式の極限",
  "q": r"数列 $\{a_n\}$ を $a_1=0$，$a_{n+1}=e^{-a_n}$（$n=1,\ 2,\ 3,\ \cdots$）で定める。<br>"
       r"(1) 方程式 $x=e^{-x}$ はただ1つの実数解 $\alpha$ をもち、$\dfrac1e<\alpha<1$ であることを示せ。<br>"
       r"(2) $n\geqq2$ のとき $\dfrac1e\leqq a_n\leqq1$ であることを示せ。<br>"
       r"(3) $n\geqq2$ のとき $|a_{n+1}-\alpha|\leqq e^{-\frac1e}|a_n-\alpha|$ であることを示し、$\displaystyle\lim_{n\to\infty}a_n=\alpha$ を証明せよ。",
  "hint": r"(3) $a_{n+1}-\alpha=e^{-a_n}-e^{-\alpha}$ は $f(x)=e^{-x}$ の値の差なので、平均値の定理で $f'(c)(a_n-\alpha)$ と書ける。$|f'(c)|=e^{-c}$ を、$c$ のある範囲（(2) で用意）から $1$ より小さい定数で抑えるのが要点。",
  "sol": r"(1) $g(x)=x-e^{-x}$ とおくと $g'(x)=1+e^{-x}>0$ より $g(x)$ は単調に増加する。<br>"
         r"$g\left(\dfrac1e\right)=e^{-1}-e^{-\frac1e}<0$（$-1<-\dfrac1e$ より），$g(1)=1-\dfrac1e>0$ であり、$g$ は連続だから中間値の定理より $g(x)=0$ は $\dfrac1e<x<1$ に解をもつ。単調増加だから実数解はただ1つである。<br>"
         r"(2) 数学的帰納法で示す。$a_2=e^0=1$ で成り立つ。$\dfrac1e\leqq a_k\leqq1$ と仮定すると、$e^{-x}$ は減少関数だから $e^{-1}\leqq e^{-a_k}\leqq e^{-\frac1e}<1$，すなわち $\dfrac1e\leqq a_{k+1}\leqq1$。<br>"
         r"(3) $n\geqq2$ とする。$a_n=\alpha$ のときは両辺とも $0$ で成り立つ。$a_n\neq\alpha$ のとき、$f(x)=e^{-x}$ に $a_n$ と $\alpha$ を両端とする区間で平均値の定理を用いると<br>"
         r"$a_{n+1}-\alpha=e^{-a_n}-e^{-\alpha}=-e^{-c}(a_n-\alpha)$<br>"
         r"を満たす $c$ が $a_n$ と $\alpha$ の間に存在する。(1)，(2) より $a_n,\ \alpha$ はともに $\dfrac1e$ 以上だから $c>\dfrac1e$，よって $e^{-c}<e^{-\frac1e}$ で　$|a_{n+1}-\alpha|\leqq e^{-\frac1e}|a_n-\alpha|$<br>"
         r"これをくり返し用いて　$0\leqq|a_n-\alpha|\leqq\left(e^{-\frac1e}\right)^{n-2}|a_2-\alpha|$（$n\geqq2$）<br>"
         r"$0<e^{-\frac1e}<1$ より右辺 $\to0$（$n\to\infty$）だから、はさみうちの原理により $\displaystyle\lim_{n\to\infty}a_n=\alpha$　$\blacksquare$",
  "note": r"要点は「$|f'(x)|\leqq k<1$ となる区間に、数列の項と $\alpha$ がすべて入っている」ことの確認。$a_1=0$ では $|f'(0)|=1$ となって評価が効かないので、$n\geqq2$ に限った。$\alpha=0.567\cdots$ は式では表せないが、極限としては確定する。",
  "ex": r"$a_1=1$，$a_{n+1}=1+\dfrac{1}{a_n}$ で定まる数列 $\{a_n\}$ について、$n\geqq2$ のとき $\dfrac32\leqq a_n\leqq2$ が成り立つことを用いて、平均値の定理により $\displaystyle\lim_{n\to\infty}a_n$ を求めよ。",
  "exa": r"$\dfrac{1+\sqrt5}{2}$（$\alpha=\dfrac{1+\sqrt5}2$ とすると $|a_{n+1}-\alpha|\leqq\dfrac49|a_n-\alpha|$）"},
 {"lv": 5, "title": r"平均値の定理による関数の決定（論証）",
  "q": r"関数 $f(x)$ はすべての実数 $x$ で微分可能で、$f(0)=0$ であり、すべての実数 $x$ について $|f'(x)|\leqq2|f(x)|$ を満たす。このとき、すべての実数 $x$ について $f(x)=0$ であることを証明せよ。",
  "hint": r"幅 $\dfrac14$ の閉区間で $|f(x)|$ の最大値 $M$ を考える。平均値の定理で $|f(x)|=|f'(c)|\cdot|x-p|\leqq2M\cdot\dfrac14$ とすると $M\leqq\dfrac M2$，よって $M=0$。これを隣の区間へ次々と広げていく。",
  "sol": r"<b>補題</b>　実数 $p$ について $f(p)=0$ ならば、$p\leqq x\leqq p+\dfrac14$ で $f(x)=0$ である。<br>"
         r"（証明）$f$ は微分可能だから連続であり、閉区間 $I:\ p\leqq x\leqq p+\dfrac14$ で $|f(x)|$ は最大値 $M\ (\geqq0)$ をとる。$x\in I$，$x\neq p$ とすると、平均値の定理より $f(x)=f(x)-f(p)=f'(c)(x-p)$ を満たす $c$ が $p<c<x$ に存在する。$c\in I$ だから<br>"
         r"$|f(x)|=|f'(c)|(x-p)\leqq2|f(c)|\cdot\dfrac14\leqq\dfrac M2$<br>"
         r"$x=p$ のときも $|f(p)|=0\leqq\dfrac M2$。よって $I$ のすべての $x$ で $|f(x)|\leqq\dfrac M2$ となり、最大値について $M\leqq\dfrac M2$，すなわち $M\leqq0$。$M\geqq0$ と合わせて $M=0$，つまり $I$ で $f(x)=0$。<br>"
         r"同様に（$c$ を $x<c<p$ にとって）$p-\dfrac14\leqq x\leqq p$ でも $f(x)=0$ である。<br>"
         r"<b>本題</b>　$f(0)=0$ に補題を用いると $0\leqq x\leqq\dfrac14$ で $f(x)=0$，特に $f\left(\dfrac14\right)=0$。再び補題を用いると $\dfrac14\leqq x\leqq\dfrac24$ で $f(x)=0$。これをくり返すと、数学的帰納法により、すべての自然数 $k$ について $0\leqq x\leqq\dfrac k4$ で $f(x)=0$。負の側も同様に $-\dfrac k4\leqq x\leqq0$ で $f(x)=0$。<br>"
         r"任意の実数 $x$ に対し $|x|\leqq\dfrac k4$ となる自然数 $k$ があるから、すべての実数 $x$ について $f(x)=0$　$\blacksquare$",
  "note": r"区間の幅 $\dfrac14$ は「$2\times$（幅）$<1$」となるように選んだ。条件が $|f'(x)|\leqq K|f(x)|$ なら幅を $\dfrac{1}{2K}$ にすればよい。$f(x)=e^{2x}$ は $f'(x)=2f(x)$ を満たすが $f(0)=1$ であり、$f(0)=0$ の条件が本質的であることがわかる。いきなり全区間で最大値を考えると、最大値が存在するとは限らない（区間が有界でない）ので、有界な閉区間に区切るのがポイント。",
  "ex": r"関数 $f(x)$ はすべての実数 $x$ で微分可能で、$f(1)=0$ であり、すべての実数 $x$ について $|f'(x)|\leqq3|f(x)|$ を満たす。すべての実数 $x$ について $f(x)=0$ であることを証明せよ。",
  "exa": r"幅 $\dfrac16$ の区間 $p\leqq x\leqq p+\dfrac16$（$f(p)=0$）で $|f|$ の最大値を $M$ とすると、平均値の定理より $M\leqq3M\cdot\dfrac16=\dfrac M2$，$M=0$。$x=1$ から両側へ区間を広げる。"},
]})


def _v2():
    # c の値
    c = E - 1
    assert simplify((1 - 0) / (E - 1) - 1 / c) == 0 and 1 < N(c) < N(E)
    c = log(E - 1)
    assert simplify((E - 1) / 1 - exp(c)) == 0 and 0 < N(c) < 1
    # 不等式（数値）
    for _ in range(2000):
        A = random.uniform(0.01, 10)
        B = A + random.uniform(1e-3, 10)
        L = math.log(B / A)
        assert (B - A) / B < L < (B - A) / A
        A = random.uniform(-5, 5)
        B = A + random.uniform(1e-3, 5)
        D = math.exp(B) - math.exp(A)
        assert math.exp(A) * (B - A) < D < math.exp(B) * (B - A)
    # 極限
    assert limit((exp(x) - exp(sin(x))) / (x - sin(x)), x, 0) == 1
    assert limit(x**2 * (exp(1 / x) - exp(1 / (x + 1))), x, oo) == 1
    # 漸化式 a_{n+1}=e^{-a_n}
    F = lambda v: v - math.exp(-v)
    al = _bis(F, 1 / math.e, 1)
    assert F(1 / math.e) < 0 < F(1) and 1 / math.e < al < 1
    assert math.exp(-1) < math.exp(-1 / math.e) < 1
    an, k = 0.0, math.exp(-1 / math.e)
    seq = [an]
    for n in range(200):
        an = math.exp(-an)
        seq.append(an)
    for n in range(1, 200):
        assert 1 / math.e - 1e-15 <= seq[n] <= 1 + 1e-15
        assert abs(seq[n + 1] - al) <= k * abs(seq[n] - al) + 1e-15
    assert abs(seq[-1] - al) < 1e-12
    # 練習 a_{n+1}=1+1/a_n
    phi = (1 + math.sqrt(5)) / 2
    an, seq = 1.0, [1.0]
    for n in range(100):
        an = 1 + 1 / an
        seq.append(an)
    for n in range(1, 100):
        assert 1.5 - 1e-15 <= seq[n] <= 2 + 1e-15
        assert abs(seq[n + 1] - phi) <= 4 / 9 * abs(seq[n] - phi) + 1e-15
    assert abs(seq[-1] - phi) < 1e-12 and 1.5 <= phi <= 2
    # 関数の決定：区間の幅の選び方と注意の例
    assert Rational(2) * Rational(1, 4) == Rational(1, 2) and Rational(3) * Rational(1, 6) == Rational(1, 2)
    assert simplify(diff(exp(2 * x), x) - 2 * exp(2 * x)) == 0


# ---------------------------------------------------------------- 節3 の図
def _fig35():
    g = _G(200, 150, (-3.6, 2.9), (-4.6, 7.2))
    g.axes()
    q = lambda v: math.exp(v) / v
    g.curve(q, -3.6, -0.02)
    g.curve(q, 0.02, 2.9)
    g.seg((0, math.e), (1, math.e))
    g.seg((1, 0), (1, math.e))
    g.pt(1, math.e)
    g.xtick(1, "1")
    g.ytick(math.e, "e")
    g.seg((-3.5, 5.2), (2.85, 5.2), col=C2, w=1.0, dash="")
    g.seg((-3.5, -2.2), (2.85, -2.2), col=C2, w=1.0, dash="")
    g.txt(-3.4, 5.2, "y=2a", dy=-4, anc="start", it=True, col=C2)
    g.txt(2.2, -2.2, "y=2a", dy=12, anc="middle", it=True, col=C2)
    g.txt(1.95, 6.6, "y=", it=True, anc="end", size=9.5)
    g.txt(1.95, 6.6, "eˣ/x", it=True, anc="start", size=9.5)
    return g.svg()


# ---------------------------------------------------------------- 節3
SEC.append({"title": r"関数の増減と極値",
"base": r"""・ある区間で $f'(x)>0$ ならば $f(x)$ はその区間で増加し、$f'(x)<0$ ならば減少する。<br>
・$f'(x)$ の符号が $x=a$ の前後で正から負に変われば $f(a)$ は極大値、負から正に変われば極小値。<br>
・$f(x)$ が $x=a$ で微分可能で極値をとるならば $f'(a)=0$。ただし逆は成り立たない（符号が変わるかを必ず調べる）。<br>
・微分可能でない点で極値をとることもある。増減表には $f'(x)=0$ の点と微分可能でない点の両方を入れる。""",
"items": [
 {"lv": 1, "title": r"増減表と極値（指数関数を含む）",
  "q": r"関数 $f(x)=(x^2-3)e^{x}$ の極値を求めよ。",
  "hint": r"積の微分法で $f'(x)$ を求めて因数分解する。$e^x>0$ だから、符号は多項式部分だけで決まる。",
  "sol": r"$f'(x)=2xe^x+(x^2-3)e^x=(x^2+2x-3)e^x=(x+3)(x-1)e^x$<br>"
         r"$e^x>0$ だから、$f'(x)$ の符号は $(x+3)(x-1)$ の符号と一致する。<br>"
         + _tb([r"$x$", DOT, r"$-3$", DOT, r"$1$", DOT],
               [r"$f'(x)$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$f(x)$", UP, r"極大<br>$6e^{-3}$", DN, r"極小<br>$-2e$", UP]) +
         r"よって　$\boldsymbol{x=-3}$ で極大値 $\boldsymbol{6e^{-3}}$，$\boldsymbol{x=1}$ で極小値 $\boldsymbol{-2e}$",
  "note": r"極値は「どの $x$ で」「極大か極小か」「その値」の3つをそろえて答える。$6e^{-3}=\dfrac{6}{e^3}$ と書いてもよい。",
  "ex": r"関数 $f(x)=x^2e^{-x}$ の極値を求めよ。",
  "exa": r"$x=0$ で極小値 $0$，$x=2$ で極大値 $\dfrac4{e^2}$"},
 {"lv": 2, "title": r"微分可能でない点を含む極値",
  "q": r"関数 $f(x)=x^{\frac23}(x-5)$ の極値を求めよ。ただし、$x^{\frac23}=\sqrt[3]{x^2}$ とする。",
  "hint": r"$x=0$ では $f'(x)$ が存在しない。微分可能でない点も増減表に入れ、その前後の増減から極値かどうかを判断する。",
  "sol": r"$f(x)=x^{\frac53}-5x^{\frac23}$ で、$x\neq0$ のとき<br>"
         r"$f'(x)=\dfrac53x^{\frac23}-\dfrac{10}3x^{-\frac13}=\dfrac{5(x-2)}{3\sqrt[3]{x}}$<br>"
         r"$x=0$ では、$\dfrac{f(h)-f(0)}{h}=\dfrac{h-5}{\sqrt[3]{h}}$ が $h\to0$ で収束しないので微分可能でない。<br>"
         + _tb([r"$x$", DOT, r"$0$", DOT, r"$2$", DOT],
               [r"$f'(x)$", r"$+$", r"", r"$-$", r"$0$", r"$+$"],
               [r"$f(x)$", UP, r"極大<br>$0$", DN, r"極小<br>$-3\sqrt[3]4$", UP]) +
         r"$f(2)=\sqrt[3]{4}\cdot(-3)=-3\sqrt[3]4$。よって　$\boldsymbol{x=0}$ で極大値 $\boldsymbol{0}$，$\boldsymbol{x=2}$ で極小値 $\boldsymbol{-3\sqrt[3]{4}}$",
  "note": r"極値をとりうる点は「$f'(x)=0$ の点」と「微分可能でない点」。$y=|x|$ の $x=0$ と同じく、$f'(x)$ の符号が変われば微分可能でない点でも極値になる。",
  "ex": r"関数 $f(x)=x^{\frac13}(x-4)$ の極値を調べよ。ただし、$x^{\frac13}=\sqrt[3]{x}$ とする。",
  "exa": r"$x=1$ で極小値 $-3$。$x=0$ では極値をとらない（前後で $f'(x)<0$）。"},
 {"lv": 2, "title": r"極値の条件から関数を決定する",
  "q": r"関数 $f(x)=\dfrac{ax+b}{x^2+1}$ が $x=2$ で極大値 $1$ をとるように、定数 $a,\ b$ の値を定めよ。また、そのときの極小値を求めよ。",
  "hint": r"「$x=2$ で極値 $\Rightarrow$ $f'(2)=0$」は必要条件にすぎない。$f'(2)=0$，$f(2)=1$ から $a,\ b$ を求めたあと、実際に $x=2$ で極大になることを増減表で確かめる（十分性の確認）。",
  "sol": r"$f'(x)=\dfrac{a(x^2+1)-(ax+b)\cdot2x}{(x^2+1)^2}=\dfrac{-ax^2-2bx+a}{(x^2+1)^2}$<br>"
         r"$x=2$ で極大値 $1$ をとるならば $f'(2)=0$，$f(2)=1$ であるから　$-3a-4b=0$，$\dfrac{2a+b}5=1$<br>"
         r"これを解いて　$a=4,\ b=-3$<br>"
         r"逆にこのとき　$f'(x)=\dfrac{-4x^2+6x+4}{(x^2+1)^2}=\dfrac{-2(2x+1)(x-2)}{(x^2+1)^2}$<br>"
         + _tb([r"$x$", DOT, r"$-\dfrac12$", DOT, r"$2$", DOT],
               [r"$f'(x)$", r"$-$", r"$0$", r"$+$", r"$0$", r"$-$"],
               [r"$f(x)$", DN, r"極小<br>$-4$", UP, r"極大<br>$1$", DN]) +
         r"確かに $x=2$ で極大値 $1$ をとる。よって　$\boldsymbol{a=4,\ b=-3}$，極小値は $\boldsymbol{f\left(-\dfrac12\right)=-4}$",
  "note": r"逆の確認を省くと、$f'(2)=0$ であっても極小値になる場合や極値でない場合を見落とす。答案では「逆に」として必ず増減表を書く。",
  "ex": r"関数 $f(x)=\dfrac{ax+b}{x^2+3}$ が $x=1$ で極大値 $\dfrac12$ をとるように、定数 $a,\ b$ の値を定めよ。また、そのときの極小値を求めよ。",
  "exa": r"$a=1,\ b=1$，極小値 $f(-3)=-\dfrac16$"},
 {"lv": 3, "title": r"極値をもたないための条件",
  "q": r"関数 $f(x)=x+a\sin x$（$a$ は定数）が極値をもたないような $a$ の値の範囲を求めよ。",
  "hint": r"極値をもたない $\iff$ $f'(x)$ の符号が変化しない。$f'(x)=1+a\cos x$ がつねに $0$ 以上となる条件を考える。「$f'(x)=0$ となる点はあるが符号は変わらない」場合（等号の場合）に注意。",
  "sol": r"$f'(x)=1+a\cos x$<br>"
         r"(i) $|a|\leqq1$ のとき　$|a\cos x|\leqq|a|\leqq1$ より $f'(x)\geqq0$。$f'(x)=0$ となるのは $|a|=1$ で $\cos x=-a$ となる飛び飛びの $x$ だけだから、$f(x)$ は単調に増加し、極値をもたない。<br>"
         r"(ii) $a>1$ のとき　$-1<-\dfrac1a<0$ だから $\cos\theta=-\dfrac1a$ となる $\theta$ が $\dfrac\pi2<\theta<\pi$ にある。$f'(x)=a(\cos x-\cos\theta)$ で、$0<x<\pi$ において $\cos x$ は減少するから、$f'(x)$ は $x=\theta$ の前後で正から負に変わり、$f(x)$ は $x=\theta$ で極大となる。<br>"
         r"(iii) $a<-1$ のとき　同様に $\cos\theta=-\dfrac1a$ となる $\theta$ が $0<\theta<\dfrac\pi2$ にあり、$f'(x)=a(\cos x-\cos\theta)$ は $x=\theta$ の前後で負から正に変わるので、極小となる。<br>"
         r"以上より　$\boldsymbol{-1\leqq a\leqq1}$",
  "note": r"「$f'(x)=0$ となる $x$ が存在しない」として $-1<a<1$ と答えるのは誤り。$a=\pm1$ のときは $f'(x)=0$ となる $x$ があるが、符号は変わらないので極値をもたない。",
  "ex": r"関数 $f(x)=ax+\log(x^2+1)$（$a$ は定数）が極値をもつような $a$ の値の範囲を求めよ。",
  "exa": r"$-1<a<1$"},
 {"lv": 4, "title": r"極値の個数（文字定数の分離）",
  "q": r"$a$ を定数とする。関数 $f(x)=e^x-ax^2$ の極値の個数を求めよ。",
  "hint": r"$f'(x)=e^x-2ax$ の符号が変わる点の個数を数える。$x=0$ は $f'(x)=0$ の解でないので $\dfrac{e^x}{x}=2a$ と分離し、$y=\dfrac{e^x}{x}$ のグラフと直線 $y=2a$ の交わり方を調べる。接する場合は符号が変わらないことに注意。",
  "sol": _fig35() +
         r"$f'(x)=e^x-2ax$。$x\neq0$ のとき $f'(x)=x\left\{g(x)-2a\right\}$，$g(x)=\dfrac{e^x}{x}$ と書ける。$f'(0)=1\neq0$ だから、$f'(x)$ の符号が変わる点は、$x\neq0$ で $g(x)-2a$ の符号が変わる点と一致する。<br>"
         r"$g'(x)=\dfrac{(x-1)e^x}{x^2}$ より、$g(x)$ は $x<0$ と $0<x<1$ で減少、$x>1$ で増加し、$g(1)=e$。<br>"
         r"また $\displaystyle\lim_{x\to-\infty}g(x)=0$，$\displaystyle\lim_{x\to-0}g(x)=-\infty$，$\displaystyle\lim_{x\to+0}g(x)=\infty$，$\displaystyle\lim_{x\to\infty}g(x)=\infty$ で、$x<0$ では $g(x)<0$。<br>"
         r"グラフ（図）と直線 $y=2a$ の交わり方を調べる。<br>"
         r"・$2a<0$：$x<0$ の部分とただ1点で交わり、そこで符号が変わる → 極値1個<br>"
         r"・$0\leqq2a<e$：共有点がない → 0個<br>"
         r"・$2a=e$：点 $(1,\ e)$ で接するが、$x>0$ で $g(x)-e\geqq0$ なので符号は変わらない → 0個<br>"
         r"・$2a>e$：$0<x<1$ と $x>1$ で1回ずつ交わる → 2個<br>"
         r"答　$\boldsymbol{a<0}$ のとき $\boldsymbol1$ 個，$\boldsymbol{0\leqq a\leqq\dfrac e2}$ のとき $\boldsymbol0$ 個，$\boldsymbol{a>\dfrac e2}$ のとき $\boldsymbol2$ 個",
  "note": r"定数を分離するとき $x$ で割ると、$x<0$ の部分で不等号の向き（符号）が逆になる。$f'(x)=x\{g(x)-2a\}$ と積の形にしておけば、符号の変化だけを見ればよいことがはっきりする。",
  "ex": r"$a$ を定数とする。関数 $f(x)=x^2-ae^{-x}$ の極値の個数を求めよ。",
  "exa": r"$a\leqq0$ のとき1個，$0<a<\dfrac2e$ のとき2個，$a\geqq\dfrac2e$ のとき0個"},
]})


def _v3():
    f = (x**2 - 3) * exp(x)
    assert simplify(diff(f, x) - (x + 3) * (x - 1) * exp(x)) == 0
    assert simplify(f.subs(x, -3) - 6 * exp(-3)) == 0 and simplify(f.subs(x, 1) + 2 * E) == 0
    g = x**2 * exp(-x)
    assert simplify(diff(g, x) - x * (2 - x) * exp(-x)) == 0 and simplify(g.subs(x, 2) - 4 * exp(-2)) == 0
    # x^{2/3}(x-5)：実数の3乗根で数値確認
    cr = lambda v: math.copysign(abs(v) ** (1 / 3), v)
    F = lambda v: cr(v) ** 2 * (v - 5)
    Fp = lambda v: 5 * (v - 2) / (3 * cr(v))
    for v in [-3, -1, -0.2, 0.3, 1, 1.9, 2.5, 7]:
        h = 1e-6
        assert abs((F(v + h) - F(v - h)) / (2 * h) - Fp(v)) < 1e-4
    assert abs(F(2) + 3 * 4 ** (1 / 3)) < 1e-12
    assert F(-1e-3) < 0 and F(1e-3) < 0 and F(0) == 0          # x=0 で極大
    G = lambda v: cr(v) * (v - 4)
    Gp = lambda v: 4 * (v - 1) / (3 * cr(v) ** 2)
    for v in [-3, -0.5, 0.4, 2, 6]:
        h = 1e-6
        assert abs((G(v + h) - G(v - h)) / (2 * h) - Gp(v)) < 1e-4
    assert G(1) == -3 and G(-1e-3) > G(0) > G(1e-3)
    # (ax+b)/(x^2+1)
    A, B = symbols("A B")
    f = (A * x + B) / (x**2 + 1)
    fp = diff(f, x)
    sol = solve([fp.subs(x, 2), f.subs(x, 2) - 1], [A, B], dict=True)
    assert sol == [{A: 4, B: -3}]
    f1 = f.subs({A: 4, B: -3})
    assert simplify(diff(f1, x) - (-2 * (2 * x + 1) * (x - 2)) / (x**2 + 1)**2) == 0
    assert f1.subs(x, Rational(-1, 2)) == -4
    f = (A * x + B) / (x**2 + 3)
    sol = solve([diff(f, x).subs(x, 1), f.subs(x, 1) - Rational(1, 2)], [A, B], dict=True)
    assert sol == [{A: 1, B: 1}]
    f2 = f.subs({A: 1, B: 1})
    assert simplify(diff(f2, x) + (x + 3) * (x - 1) / (x**2 + 3)**2) == 0 and f2.subs(x, -3) == Rational(-1, 6)
    # x + a sin x
    xs = _grid(-10, 10, 4000)
    for A_ in [-1, -0.6, 0, 0.7, 1]:
        assert min(1 + A_ * math.cos(v) for v in xs) >= -1e-12
    for A_ in [1.02, 2, 5, -1.02, -3]:
        vals = [1 + A_ * math.cos(v) for v in xs]
        assert min(vals) < 0 < max(vals)
    for A_ in [-0.99, -0.5, 0.0, 0.3, 0.99]:
        assert _count(lambda v: A_ + 2 * v / (v * v + 1), _grid(-1e4, 1e4, 200000)) >= 1
    for A_ in [-1, -1.5, 1, 3]:
        vals = [A_ + 2 * v / (v * v + 1) for v in _grid(-50, 50, 20000)]
        assert min(vals) >= -1e-12 or max(vals) <= 1e-12
    # e^x - a x^2 の極値の個数（f' の符号変化の回数）
    xs = _grid(-80, 30, 220000)
    for A_, n in [(-3, 1), (-0.01, 1), (0, 0), (0.5, 0), (1.3, 0), (1.4, 2), (3, 2), (20, 2)]:
        assert _count(lambda v: math.exp(v) - 2 * A_ * v, xs) == n, (A_, n)
    assert min(math.exp(v) - math.e * v for v in xs) >= -1e-9       # a=e/2 は接するだけ
    assert simplify(diff(exp(x) / x, x) - (x - 1) * exp(x) / x**2) == 0
    # 練習：x^2 - a e^{-x}
    for A_, n in [(-5, 1), (-0.1, 1), (0, 1), (0.1, 2), (0.7, 2), (0.75, 0), (2, 0)]:
        assert _count(lambda v: 2 * v + A_ * math.exp(-v), _grid(-40, 40, 160000)) == n, (A_, n)
    assert min(2 * v + 2 / math.e * math.exp(-v) for v in _grid(-40, 40, 160000)) >= -1e-9


# ---------------------------------------------------------------- 節4 の図
def _fig41():
    g = _G(220, 110, (-2.3, 2.3), (-0.22, 1.25))
    g.axes()
    g.curve(lambda v: math.exp(-v * v), -2.3, 2.3)
    r = 1 / math.sqrt(2)
    for s_ in (-1, 1):
        g.seg((s_ * r, 0), (s_ * r, math.exp(-0.5)))
        g.pt(s_ * r, math.exp(-0.5), col=C2)
    g.txt(r, 0, "1/√2", dy=11, size=9.5)
    g.txt(-r, 0, "−1/√2", dy=11, size=9.5)
    g.ytick(1, "1")
    g.seg((0, math.exp(-0.5)), (r, math.exp(-0.5)))
    g.txt(1.45, 0.78, "変曲点", size=9.5, col=C2)
    return g.svg()


def _fig42():
    g = _G(190, 190, (-4.3, 2.7), (-5.2, 8.0))
    g.axes()
    g.seg((-5.2 / 3, -5.2), (2.65, 7.95), col=CG, w=0.9)
    g.seg((-4.3, -4.3), (2.65, 2.65), col=CG, w=0.9)
    f = lambda v: 2 * v + math.sqrt(max(v * v - 1, 0))
    g.curve(f, 1, 2.7)
    g.curve(f, -4.3, -1)
    g.pt(1, 2)
    g.pt(-1, -2)
    g.txt(2.6, 7.2, "y=3x", anc="end", dx=-6, it=True, size=10, col="#555")
    g.txt(-3.3, -3.3, "y=x", anc="start", dy=-6, it=True, size=10, col="#555")
    g.txt(1, 2, "(1, 2)", dx=-4, dy=-3, anc="end", size=9.5)
    g.txt(-1, -2, "(−1, −2)", dx=-2, dy=13, anc="middle", size=9.5)
    return g.svg()


def _fig43():
    g = _G(200, 200, (-4.2, 4.2), (-5.6, 5.6))
    g.axes()
    for xv in (-1, 1):
        g.seg((xv, -5.6), (xv, 5.6), col=CG, w=0.9)
    g.seg((-4.2, -4.2), (4.2, 4.2), col=CG, w=0.9)
    f = lambda v: v ** 3 / (v * v - 1)
    g.curve(f, -4.2, -1.0005, n=500)
    g.curve(f, -0.9995, 0.9995, n=500)
    g.curve(f, 1.0005, 4.2, n=500)
    r3 = math.sqrt(3)
    g.pt(r3, 1.5 * r3)
    g.pt(-r3, -1.5 * r3)
    g.pt(0, 0, col=C2)
    g.seg((r3, 0), (r3, 1.5 * r3))
    g.seg((-r3, 0), (-r3, -1.5 * r3))
    g.txt(r3, 0, "√3", dy=11, dx=3, size=9.5)
    g.txt(-r3, 0, "−√3", dy=-4, dx=-3, size=9.5)
    g.txt(1, 0, "1", dx=4, dy=-4, size=9.5)
    g.txt(-1, 0, "−1", dx=-6, dy=11, size=9.5)
    g.txt(4.1, 4.1, "y=x", anc="end", dy=-6, dx=-4, it=True, col="#555")
    return g.svg()


def _fig44():
    g = _G(160, 150, (-1.35, 1.35), (-1.3, 1.3))
    g.axes()
    g.pcurve(math.sin, lambda v: math.sin(2 * v), 0, 2 * math.pi, n=400)
    r = math.sqrt(2) / 2
    for p in [(1, 0), (-1, 0)]:
        g.pt(*p, col=C2)
    for p in [(r, 1), (r, -1), (-r, 1), (-r, -1)]:
        g.pt(*p)
        g.seg((p[0] - 0.22, p[1]), (p[0] + 0.22, p[1]), col=C2, w=0.9, dash="")
    for p in [(1, 0), (-1, 0)]:
        g.seg((p[0], -0.22), (p[0], 0.22), col=C2, w=0.9, dash="")
    g.txt(1, 0, "1", dx=4, dy=12, anc="start", size=9.5)
    g.txt(-1, 0, "−1", dx=-4, dy=12, anc="end", size=9.5)
    g.txt(0, 1, "1", dx=-4, dy=3, anc="end", size=9.5)
    return g.svg()


def _fig45():
    g = _G(210, 120, (-0.15, 4.4), (-0.1, 0.46))
    g.axes()
    g.curve(lambda v: math.exp(-v), 0.78, 4.4, col=CG, w=0.9, dash=DASH)
    g.curve(lambda v: -math.exp(-v), 2.31, 4.4, col=CG, w=0.9, dash=DASH)
    g.curve(lambda v: math.exp(-v) * math.sin(v), 0, 4.4)
    p4 = math.pi / 4
    g.pt(p4, math.exp(-p4) * math.sin(p4))
    g.pt(math.pi / 2, math.exp(-math.pi / 2), col=C2)
    g.seg((p4, 0), (p4, math.exp(-p4) * math.sin(p4)))
    g.txt(p4, 0, "π/4", dy=11, size=9.5)
    g.xtick(math.pi / 2, "π/2", it=False)
    g.xtick(math.pi, "π", dy=-4, it=False)
    g.txt(1.9, 0.24, "y=e⁻ˣ", anc="start", it=True, size=9.5, col="#555")
    return g.svg()


# ---------------------------------------------------------------- 節4
SEC.append({"title": r"グラフの凹凸・漸近線と概形",
"base": r"""・$f''(x)>0$ の区間で曲線 $y=f(x)$ は下に凸、$f''(x)<0$ の区間で上に凸。$f''(x)$ の符号が $x=a$ の前後で変わるとき、点 $(a,\ f(a))$ を変曲点という。<br>
・漸近線：$\displaystyle\lim_{x\to a\pm0}f(x)=\pm\infty$ なら直線 $x=a$。$\displaystyle m=\lim_{x\to\infty}\frac{f(x)}{x}$，$\displaystyle n=\lim_{x\to\infty}\{f(x)-mx\}$ が存在すれば直線 $y=mx+n$（$x\to-\infty$ も別に調べる）。<br>
・概形をかく手順：定義域・対称性 → 増減と極値 → 凹凸と変曲点 → 漸近線・端での極限 → 座標軸との交点<br>
・よく使う極限：$\displaystyle\lim_{x\to\infty}\frac{x^n}{e^x}=0$，$\displaystyle\lim_{x\to\infty}\frac{\log x}{x}=0$，$\displaystyle\lim_{x\to+0}x\log x=0$""",
"items": [
 {"lv": 1, "title": r"曲線の凹凸と変曲点",
  "q": r"曲線 $y=e^{-x^2}$ の凹凸を調べ、変曲点の座標を求めよ。",
  "hint": r"第2次導関数 $y''$ を求め、その符号を調べる。$e^{-x^2}>0$ だから多項式の部分の符号だけを見ればよい。",
  "sol": _fig41() +
         r"$y'=-2xe^{-x^2}$，$y''=-2e^{-x^2}+4x^2e^{-x^2}=2(2x^2-1)e^{-x^2}$<br>"
         r"$y''=0$ とすると $x=\pm\dfrac{1}{\sqrt2}$。$y''$ の符号は $2x^2-1$ の符号と一致するから<br>"
         r"$x<-\dfrac1{\sqrt2}$，$\dfrac1{\sqrt2}<x$ で<b>下に凸</b>，$-\dfrac1{\sqrt2}<x<\dfrac1{\sqrt2}$ で<b>上に凸</b><br>"
         r"$x=\pm\dfrac1{\sqrt2}$ のとき $y=e^{-\frac12}$ だから、変曲点は　$\boldsymbol{\left(\pm\dfrac{1}{\sqrt2},\ \dfrac{1}{\sqrt e}\right)}$",
  "note": r"この曲線は $y$ 軸に関して対称で、$x=0$ で最大値 $1$ をとり、$x$ 軸が漸近線である。統計で使う正規分布の曲線と同じ形をしている。",
  "ex": r"曲線 $y=\log(x^2+1)$ の凹凸を調べ、変曲点の座標を求めよ。",
  "exa": r"$-1<x<1$ で下に凸，$x<-1,\ 1<x$ で上に凸。変曲点 $(\pm1,\ \log2)$"},
 {"lv": 2, "title": r"漸近線（$x\to\infty$ と $x\to-\infty$ で異なる場合）",
  "q": r"曲線 $y=2x+\sqrt{x^2-1}$ の漸近線を求めよ。",
  "hint": r"定義域は $|x|\geqq1$。$\sqrt{x^2}=|x|$ なので、$x\to\infty$ と $x\to-\infty$ を別々に扱い、それぞれ $\displaystyle m=\lim\frac yx$，$n=\lim(y-mx)$ を計算する。",
  "sol": _fig42() +
         r"定義域は $x\leqq-1,\ 1\leqq x$ で、定義域の各点で $y$ は有限だから、$y$ 軸に平行な漸近線はない。<br>"
         r"<b>$x\to\infty$ のとき</b>　$\dfrac yx=2+\sqrt{1-\dfrac1{x^2}}\to3$，<br>"
         r"$y-3x=\sqrt{x^2-1}-x=\dfrac{-1}{\sqrt{x^2-1}+x}\to0$<br>"
         r"よって直線 $y=3x$ は漸近線。<br>"
         r"<b>$x\to-\infty$ のとき</b>　$x<0$ では $\sqrt{x^2-1}=|x|\sqrt{1-\dfrac{1}{x^2}}=-x\sqrt{1-\dfrac1{x^2}}$ だから<br>"
         r"$\dfrac yx=2-\sqrt{1-\dfrac1{x^2}}\to1$，$y-x=x+\sqrt{x^2-1}=\dfrac{-1}{\sqrt{x^2-1}-x}\to0$<br>"
         r"よって直線 $y=x$ も漸近線。答　$\boldsymbol{y=3x,\ y=x}$",
  "note": r"$\sqrt{x^2-1}=x\sqrt{1-\dfrac1{x^2}}$ としてよいのは $x>0$ のときだけ。$x\to-\infty$ では $x=-s$ とおいて $s\to\infty$ を考えると間違えにくい。",
  "ex": r"曲線 $y=\sqrt{x^2+4x+5}$ の漸近線を求めよ。",
  "exa": r"$y=x+2$（$x\to\infty$），$y=-x-2$（$x\to-\infty$）"},
 {"lv": 3, "title": r"分数関数のグラフの概形",
  "q": r"関数 $y=\dfrac{x^3}{x^2-1}$ の増減、極値、グラフの凹凸、漸近線を調べて、グラフの概形をかけ。",
  "hint": r"奇関数なのでグラフは原点に関して対称で、$x\geqq0$ で調べれば十分。$y=x+\dfrac{x}{x^2-1}$ と変形すれば斜めの漸近線 $y=x$ がわかる。$y'$，$y''$ は因数分解した形で求める。",
  "sol": _fig43() +
         r"定義域は $x\neq\pm1$。$y=x+\dfrac{x}{x^2-1}$ で、奇関数だからグラフは原点に関して対称。<br>"
         r"$y'=\dfrac{3x^2(x^2-1)-x^3\cdot2x}{(x^2-1)^2}=\dfrac{x^2(x^2-3)}{(x^2-1)^2}$，$y''=\dfrac{2x(x^2+3)}{(x^2-1)^3}$<br>"
         r"$x\geqq0$ での増減・凹凸は次の通り（$\frown$ は上に凸、$\smile$ は下に凸）。<br>"
         + _tb([r"$x$", r"$0$", DOT, r"$1$", DOT, r"$\sqrt3$", DOT],
               [r"$y'$", r"$0$", r"$-$", r"", r"$-$", r"$0$", r"$+$"],
               [r"$y''$", r"$0$", r"$-$", r"", r"$+$", r"$+$", r"$+$"],
               [r"$y$", r"$0$", r"$\searrow\ \frown$", r"", r"$\searrow\ \smile$", r"$\dfrac{3\sqrt3}{2}$", r"$\nearrow\ \smile$"]) +
         r"$-1<x<0$ では $y''>0$ だから、$y''$ は $x=0$ の前後で符号を変え、原点は変曲点（接線は $y=0$）。<br>"
         r"$\displaystyle\lim_{x\to1-0}y=-\infty$，$\displaystyle\lim_{x\to1+0}y=\infty$，$\displaystyle\lim_{x\to\infty}(y-x)=\lim_{x\to\infty}\frac{x}{x^2-1}=0$<br>"
         r"以上と対称性から<br>"
         r"極大値 $\boldsymbol{-\dfrac{3\sqrt3}2}$（$x=-\sqrt3$），極小値 $\boldsymbol{\dfrac{3\sqrt3}2}$（$x=\sqrt3$），変曲点 $\boldsymbol{(0,\ 0)}$，漸近線 $\boldsymbol{x=1,\ x=-1,\ y=x}$。グラフは図。",
  "note": r"原点では $y'=0$ だが $y'$ の符号は変わらない（極値ではない）。一方で $y''$ の符号は変わるので変曲点になる。グラフが漸近線 $y=x$ の上下どちらにあるかは、$y-x=\dfrac{x}{x^2-1}$ の符号でわかる（$x>1$ で上側）。",
  "ex": r"関数 $y=\dfrac{x^2-2x+2}{x-1}$ の極値と漸近線を求め、グラフの概形をかけ。",
  "exa": r"$x=0$ で極大値 $-2$，$x=2$ で極小値 $2$。漸近線 $x=1,\ y=x-1$（グラフは点 $(1,\ 0)$ に関して対称）"},
 {"lv": 3, "title": r"媒介変数表示された曲線の概形",
  "q": r"媒介変数 $t$（$0\leqq t\leqq2\pi$）を用いて $x=\sin t$，$y=\sin2t$ と表される曲線について、$x$ 軸に平行な接線をもつ点、$y$ 軸に平行な接線をもつ点を求め、曲線の概形をかけ。",
  "hint": r"$\dfrac{dx}{dt}$，$\dfrac{dy}{dt}$ の符号を $t$ について表にまとめると、点 $(x,\ y)$ の動く向きがわかる。$\dfrac{dy}{dt}=0$，$\dfrac{dx}{dt}\neq0$ の点で $x$ 軸に平行、$\dfrac{dx}{dt}=0$，$\dfrac{dy}{dt}\neq0$ の点で $y$ 軸に平行な接線をもつ。",
  "sol": _fig44() +
         r"$\dfrac{dx}{dt}=\cos t$，$\dfrac{dy}{dt}=2\cos2t$<br>"
         r"$\cos t=0$ となるのは $t=\dfrac\pi2,\ \dfrac32\pi$ で、このとき $2\cos2t=-2\neq0$。<br>"
         r"$\cos2t=0$ となるのは $t=\dfrac\pi4,\ \dfrac34\pi,\ \dfrac54\pi,\ \dfrac74\pi$ で、このとき $\cos t\neq0$。<br>"
         r"$t$ を $t+\pi$ にかえると点 $(x,\ y)$ は $(-x,\ y)$ に移るから、$0\leqq t\leqq\pi$ を調べればよい。<br>"
         + _tb([r"$t$", r"$0$", DOT, r"$\dfrac\pi4$", DOT, r"$\dfrac\pi2$", DOT, r"$\dfrac34\pi$", DOT, r"$\pi$"],
               [r"$\dfrac{dx}{dt}$", r"$+$", r"$+$", r"$+$", r"$+$", r"$0$", r"$-$", r"$-$", r"$-$", r"$-$"],
               [r"$\dfrac{dy}{dt}$", r"$+$", r"$+$", r"$0$", r"$-$", r"$-$", r"$-$", r"$0$", r"$+$", r"$+$"],
               [r"$(x,\,y)$", r"$(0,0)$", r"$\nearrow$", r"$\left(\frac{\sqrt2}2,1\right)$", r"$\searrow$", r"$(1,0)$", r"$\swarrow$", r"$\left(\frac{\sqrt2}2,-1\right)$", r"$\nwarrow$", r"$(0,0)$"]) +
         r"答　$x$ 軸に平行な接線をもつ点：$\boldsymbol{\left(\pm\dfrac{\sqrt2}{2},\ \pm1\right)}$（複号任意の4点）<br>"
         r"　　$y$ 軸に平行な接線をもつ点：$\boldsymbol{(1,\ 0),\ (-1,\ 0)}$<br>"
         r"概形は図（原点を2回通る「8の字」を横にした形）。",
  "note": r"$t$ を消去すると $y^2=4\sin^2t\cos^2t=4x^2(1-x^2)$ となり、曲線は $x$ 軸，$y$ 軸に関して対称である。原点では $t=0$ と $t=\pi$ のときに通り、接線の傾き $\dfrac{dy}{dx}=\dfrac{2\cos2t}{\cos t}$ はそれぞれ $2$，$-2$。",
  "ex": r"媒介変数 $t$ を用いて $x=t^2$，$y=t^3-3t$ と表される曲線について、$x$ 軸に平行な接線をもつ点、$y$ 軸に平行な接線をもつ点、曲線が自分自身と交わる点を求め、概形をかけ。",
  "exa": r"$x$ 軸に平行：$(1,\ -2)$，$(1,\ 2)$　$y$ 軸に平行：$(0,\ 0)$　自分自身と交わる点：$(3,\ 0)$（曲線は $x$ 軸に関して対称）"},
 {"lv": 4, "title": r"減衰振動のグラフと極値の和",
  "q": r"$x\geqq0$ で定義された関数 $f(x)=e^{-x}\sin x$ について、次の問いに答えよ。<br>"
       r"(1) $f(x)$ が極大値をとる $x$ の値と、その極大値を求めよ。<br>"
       r"(2) 極大値を $x$ の小さい方から順に $M_0,\ M_1,\ M_2,\ \cdots$ とするとき、$\displaystyle\sum_{n=0}^{\infty}M_n$ を求めよ。",
  "hint": r"$f'(x)=e^{-x}(\cos x-\sin x)$ を合成して $\sqrt2e^{-x}\cos\left(x+\dfrac\pi4\right)$ とすると符号の変化がわかる。極大値は公比 $e^{-2\pi}$ の等比数列になる。",
  "sol": _fig45() +
         r"(1) $f'(x)=e^{-x}(\cos x-\sin x)=\sqrt2e^{-x}\cos\left(x+\dfrac\pi4\right)$<br>"
         r"$x>0$ で $f'(x)=0$ となるのは $x+\dfrac\pi4=\dfrac\pi2+k\pi$，すなわち $x=\dfrac\pi4+k\pi$（$k=0,\ 1,\ 2,\ \cdots$）。<br>"
         r"$\cos\left(x+\dfrac\pi4\right)$ は $x=\dfrac\pi4+2n\pi$ の前後で正から負に、$x=\dfrac54\pi+2n\pi$ の前後で負から正に変わる。よって極大となるのは<br>"
         r"$\boldsymbol{x=\dfrac\pi4+2n\pi}$（$n=0,\ 1,\ 2,\ \cdots$）で、極大値は　$f\left(\dfrac\pi4+2n\pi\right)=e^{-\frac\pi4-2n\pi}\sin\dfrac\pi4=\boldsymbol{\dfrac{\sqrt2}{2}e^{-\frac\pi4-2n\pi}}$<br>"
         r"(2) $M_n=\dfrac{\sqrt2}2e^{-\frac\pi4}\left(e^{-2\pi}\right)^n$ だから、$\displaystyle\sum_{n=0}^\infty M_n$ は初項 $\dfrac{\sqrt2}2e^{-\frac\pi4}$，公比 $e^{-2\pi}$（$0<e^{-2\pi}<1$）の無限等比級数で、収束して<br>"
         r"$\displaystyle\sum_{n=0}^\infty M_n=\frac{\frac{\sqrt2}{2}e^{-\frac\pi4}}{1-e^{-2\pi}}=\boldsymbol{\frac{\sqrt2\,e^{\frac74\pi}}{2(e^{2\pi}-1)}}$",
  "note": r"$-e^{-x}\leqq f(x)\leqq e^{-x}$ なので、グラフは2曲線 $y=\pm e^{-x}$ の間で振動しながら $x$ 軸に近づく。$y=e^{-x}$ と接するのは $\sin x=1$ の点 $x=\dfrac\pi2+2n\pi$ で、極大点 $x=\dfrac\pi4+2n\pi$ とは一致しない（図）。",
  "ex": r"$x\geqq0$ で定義された関数 $f(x)=e^{-x}\cos x$ の極小値を、$x$ の小さい方から順に $m_0,\ m_1,\ m_2,\ \cdots$ とするとき、$\displaystyle\sum_{n=0}^\infty m_n$ を求めよ。",
  "exa": r"$-\dfrac{\sqrt2\,e^{\frac54\pi}}{2(e^{2\pi}-1)}$（極小となるのは $x=\dfrac34\pi+2n\pi$）"},
]})


def _v4():
    f = exp(-x**2)
    assert simplify(diff(f, x, 2) - 2 * (2 * x**2 - 1) * exp(-x**2)) == 0
    assert simplify(f.subs(x, 1 / sqrt(2)) - 1 / sqrt(E)) == 0
    g = log(x**2 + 1)
    assert simplify(diff(g, x, 2) - 2 * (1 - x**2) / (x**2 + 1)**2) == 0
    # 漸近線
    y1 = 2 * x + sqrt(x**2 - 1)
    assert limit(y1 / x, x, oo) == 3 and limit(y1 - 3 * x, x, oo) == 0
    assert limit(y1 / x, x, -oo) == 1 and limit(y1 - x, x, -oo) == 0
    for v in [1.5, 3, 10, 100]:
        assert abs((math.sqrt(v * v - 1) - v) - (-1 / (math.sqrt(v * v - 1) + v))) < 1e-12
        w = -v
        assert abs((w + math.sqrt(w * w - 1)) - (-1 / (math.sqrt(w * w - 1) - w))) < 1e-12
    y2 = sqrt(x**2 + 4 * x + 5)
    assert limit(y2 - (x + 2), x, oo) == 0 and limit(y2 + x + 2, x, -oo) == 0
    # x^3/(x^2-1)
    h = x**3 / (x**2 - 1)
    assert simplify(h - (x + x / (x**2 - 1))) == 0
    assert simplify(diff(h, x) - x**2 * (x**2 - 3) / (x**2 - 1)**2) == 0
    assert simplify(diff(h, x, 2) - 2 * x * (x**2 + 3) / (x**2 - 1)**3) == 0
    assert simplify(h.subs(x, sqrt(3)) - 3 * sqrt(3) / 2) == 0
    assert limit(h, x, 1, "-") == -oo and limit(h, x, 1, "+") == oo and limit(h - x, x, oo) == 0
    hp = lambdify(x, diff(h, x)); hpp = lambdify(x, diff(h, x, 2))
    assert hp(-0.5) < 0 and hp(0.5) < 0 and hpp(-0.5) > 0 and hpp(0.5) < 0
    assert hp(1.5) < 0 and hp(2) > 0 and hpp(1.2) > 0
    k = (x**2 - 2 * x + 2) / (x - 1)
    assert sorted(solve(diff(k, x), x)) == [0, 2] and k.subs(x, 0) == -2 and k.subs(x, 2) == 2
    assert simplify(k - (x - 1) - 1 / (x - 1)) == 0
    # 8の字
    X, Y = sin(t), sin(2 * t)
    for tv in [pi / 2, 3 * pi / 2]:
        assert diff(X, t).subs(t, tv) == 0 and diff(Y, t).subs(t, tv) == -2
    pts = set()
    for tv in [pi / 4, 3 * pi / 4, 5 * pi / 4, 7 * pi / 4]:
        assert simplify(diff(Y, t).subs(t, tv)) == 0 and diff(X, t).subs(t, tv) != 0
        pts.add((simplify(X.subs(t, tv)), simplify(Y.subs(t, tv))))
    r = sqrt(2) / 2
    assert pts == {(r, 1), (r, -1), (-r, 1), (-r, -1)}
    assert simplify(Y**2 - 4 * X**2 * (1 - X**2)) == 0
    assert simplify((diff(Y, t) / diff(X, t)).subs(t, 0)) == 2 and simplify((diff(Y, t) / diff(X, t)).subs(t, pi)) == -2
    assert simplify(X.subs(t, t + pi) + X) == 0 and simplify(Y.subs(t, t + pi) - Y) == 0
    # 練習 x=t^2, y=t^3-3t
    X, Y = t**2, t**3 - 3 * t
    assert solve(diff(X, t), t) == [0] and diff(Y, t).subs(t, 0) != 0
    assert {(X.subs(t, s_), Y.subs(t, s_)) for s_ in solve(diff(Y, t), t)} == {(1, -2), (1, 2)}
    s3 = sqrt(3)
    assert X.subs(t, s3) == X.subs(t, -s3) == 3 and Y.subs(t, s3) == Y.subs(t, -s3) == 0
    # e^{-x} sin x
    f = exp(-x) * sin(x)
    assert simplify(diff(f, x) - sqrt(2) * exp(-x) * cos(x + pi / 4)) == 0
    fp = lambdify(x, diff(f, x))
    for n in range(4):
        x0 = math.pi / 4 + 2 * n * math.pi
        assert fp(x0 - 1e-4) > 0 > fp(x0 + 1e-4)
        x1 = 5 * math.pi / 4 + 2 * n * math.pi
        assert fp(x1 - 1e-4) < 0 < fp(x1 + 1e-4)
        assert simplify(f.subs(x, pi / 4 + 2 * n * pi) - sqrt(2) / 2 * exp(-pi / 4 - 2 * n * pi)) == 0
    tot = sum(math.sqrt(2) / 2 * math.exp(-math.pi / 4 - 2 * n * math.pi) for n in range(60))
    assert abs(tot - math.sqrt(2) * math.exp(7 * math.pi / 4) / (2 * (math.exp(2 * math.pi) - 1))) < 1e-14
    g = exp(-x) * cos(x)
    gp = lambdify(x, diff(g, x))
    for n in range(4):
        x0 = 3 * math.pi / 4 + 2 * n * math.pi
        assert gp(x0 - 1e-4) < 0 < gp(x0 + 1e-4)
    tot = sum(math.exp(-x0) * math.cos(x0) for x0 in [3 * math.pi / 4 + 2 * n * math.pi for n in range(60)])
    assert abs(tot + math.sqrt(2) * math.exp(5 * math.pi / 4) / (2 * (math.exp(2 * math.pi) - 1))) < 1e-14


# ---------------------------------------------------------------- 節5 の図
def _fig54():
    k = (230 - 24) / 9.8
    g = _G(230, round(24 + 5.6 * k), (-4.2, 5.6), (-0.4, 5.2))
    W = 3 * math.sqrt(3)
    g.fill([(-4.2, 0), (W, 0), (W, 5.2), (0, 5.2), (0, 1), (-4.2, 1)], col="#eef2fa", op=1)
    wall = dict(col="#333", w=1.6, dash="")
    g.seg((-4.2, 0), (W, 0), **wall)
    g.seg((W, 0), (W, 5.2), **wall)
    g.seg((-4.2, 1), (0, 1), **wall)
    g.seg((0, 1), (0, 5.2), **wall)
    A, B = (-math.sqrt(3), 0), (W, 4)
    g.seg(A, B, col=C2, w=2.0, dash="")
    g.pt(0, 1)
    g.txt(0, 1, "P", dx=-3, dy=-4, anc="end", it=True)
    g.txt(-3.6, 0.5, "1", dy=3.5)
    dim = dict(col="#777", w=0.7, dash="")
    g.seg((-3.3, 0), (-3.3, 1), **dim)
    for yv in (0, 1):
        g.seg((-3.45, yv), (-3.15, yv), **dim)
    g.seg((0, 4.75), (W, 4.75), **dim)
    for xv in (0, W):
        g.seg((xv, 4.6), (xv, 4.9), **dim)
    g.txt(W / 2, 4.75, "3√3", dy=-3)
    th = math.pi / 6
    arc = [(A[0] + 0.9 * math.cos(th * i / 20), A[1] + 0.9 * math.sin(th * i / 20)) for i in range(21)]
    g._poly(arc, "#333", 0.8, "")
    g.txt(A[0] + 1.25, 0.18, "θ", it=True, dy=3)
    return g.svg()


def _fig55():
    g = _G(170, 170, (-2.6, 3.3), (-2.6, 3.3))
    g.axes()
    g.seg((-2.5, -2.5), (3.2, 3.2), col=CG, w=0.9)
    g.curve(math.exp, -2.6, 1.3)
    g.curve(math.log, 0.07, 3.3, col=C1)
    g.seg((0, 1), (1, 0), col=C2, w=1.4, dash="")
    g.pt(0, 1, col=C2)
    g.pt(1, 0, col=C2)
    g.txt(0, 1, "P", dx=-4, dy=-1, anc="end", it=True)
    g.txt(1, 0, "Q", dx=2, dy=12, anc="start", it=True)
    g.txt(1.15, 3.1, "y=eˣ", anc="start", it=True, size=9.5)
    g.txt(3.2, 1.45, "y=log x", anc="end", it=True, size=9.5)
    g.txt(-2.4, -2.1, "y=x", anc="start", it=True, size=9.5, col="#555")
    return g.svg()


# ---------------------------------------------------------------- 節5
SEC.append({"title": r"最大値・最小値",
"base": r"""・閉区間での最大・最小：極値と区間の端の値を比べる。開区間や無限区間では端での極限も調べる（最大値・最小値が存在しないこともある）。<br>
・文字定数を含むときは、極値をとる点が区間に入るかどうかで場合を分ける。<br>
・図形・文章題：長さや角などの変数を1つ決め、その<b>変域</b>を明記してから関数で表す。<br>
・2つの量が動くときは、一方を固定して考える、幾何的な性質（対称性・最短）を使う、などで1変数に帰着させる。""",
"items": [
 {"lv": 1, "title": r"閉区間における最大・最小（無理関数）",
  "q": r"関数 $f(x)=x\sqrt{4-x^2}$ の最大値と最小値を求めよ。",
  "hint": r"定義域は $-2\leqq x\leqq2$。$f'(x)$ を通分して符号を調べ、極値と定義域の端の値を比べる。",
  "sol": r"定義域は $-2\leqq x\leqq2$。$-2<x<2$ において<br>"
         r"$f'(x)=\sqrt{4-x^2}+x\cdot\dfrac{-x}{\sqrt{4-x^2}}=\dfrac{4-2x^2}{\sqrt{4-x^2}}=\dfrac{-2(x+\sqrt2)(x-\sqrt2)}{\sqrt{4-x^2}}$<br>"
         + _tb([r"$x$", r"$-2$", DOT, r"$-\sqrt2$", DOT, r"$\sqrt2$", DOT, r"$2$"],
               [r"$f'(x)$", r"", r"$-$", r"$0$", r"$+$", r"$0$", r"$-$", r""],
               [r"$f(x)$", r"$0$", DN, r"極小<br>$-2$", UP, r"極大<br>$2$", DN, r"$0$"]) +
         r"$f(\pm\sqrt2)=\pm\sqrt2\cdot\sqrt2=\pm2$，$f(\pm2)=0$ であるから<br>"
         r"最大値 $\boldsymbol{2}$（$x=\sqrt2$），最小値 $\boldsymbol{-2}$（$x=-\sqrt2$）",
  "note": r"$f(x)$ は奇関数なので、$x\geqq0$ で最大値を求めれば最小値はその符号を変えたものになる。$x\geqq0$ では $\{f(x)\}^2=x^2(4-x^2)\leqq\left(\dfrac{x^2+(4-x^2)}2\right)^2=4$（相加平均と相乗平均の関係）からも求まる。",
  "ex": r"関数 $f(x)=x\sqrt{1-x}$（$-3\leqq x\leqq1$）の最大値と最小値を求めよ。",
  "exa": r"最大値 $\dfrac{2\sqrt3}9$（$x=\dfrac23$），最小値 $-6$（$x=-3$）"},
 {"lv": 1, "title": r"三角関数の最大・最小",
  "q": r"$0\leqq x\leqq2\pi$ のとき、関数 $f(x)=2\sin x+\sin2x$ の最大値と最小値を求めよ。",
  "hint": r"$f'(x)=2\cos x+2\cos2x$ を2倍角の公式で $\cos x$ の2次式に直し、因数分解する。",
  "sol": r"$f'(x)=2\cos x+2\cos2x=2(2\cos^2x+\cos x-1)=2(2\cos x-1)(\cos x+1)$<br>"
         r"$\cos x+1\geqq0$ だから、$f'(x)$ の符号は（$x=\pi$ を除いて）$2\cos x-1$ の符号と一致する。$0\leqq x\leqq2\pi$ で $f'(x)=0$ となるのは $x=\dfrac\pi3,\ \pi,\ \dfrac53\pi$。<br>"
         + _tb([r"$x$", r"$0$", DOT, r"$\dfrac\pi3$", DOT, r"$\pi$", DOT, r"$\dfrac53\pi$", DOT, r"$2\pi$"],
               [r"$f'(x)$", r"", r"$+$", r"$0$", r"$-$", r"$0$", r"$-$", r"$0$", r"$+$", r""],
               [r"$f(x)$", r"$0$", UP, r"$\dfrac{3\sqrt3}2$", DN, r"$0$", DN, r"$-\dfrac{3\sqrt3}2$", UP, r"$0$"]) +
         r"よって　最大値 $\boldsymbol{\dfrac{3\sqrt3}2}$（$x=\dfrac\pi3$），最小値 $\boldsymbol{-\dfrac{3\sqrt3}2}$（$x=\dfrac53\pi$）",
  "note": r"$x=\pi$ では $f'(\pi)=0$ だが符号は変わらず、極値ではない。三角関数の最大・最小は、$\sin x$，$\cos x$ の1つの式に直せるとは限らないので、微分して増減を調べるのが確実。",
  "ex": r"$0\leqq x\leqq2\pi$ のとき、関数 $f(x)=(1+\sin x)\cos x$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $\dfrac{3\sqrt3}4$（$x=\dfrac\pi6$），最小値 $-\dfrac{3\sqrt3}4$（$x=\dfrac56\pi$）"},
 {"lv": 3, "title": r"区間が動くときの最大値",
  "q": r"$a$ を実数とする。関数 $f(x)=xe^{-x}$ の $a\leqq x\leqq a+1$ における最大値 $M(a)$ を求めよ。",
  "hint": r"まず $f(x)$ の増減を調べる（$x=1$ で極大）。区間 $a\leqq x\leqq a+1$ と極大点 $x=1$ の位置関係で場合を分ける。",
  "sol": r"$f'(x)=(1-x)e^{-x}$ より、$f(x)$ は $x\leqq1$ で増加、$x\geqq1$ で減少する。<br>"
         r"(i) $a+1\leqq1$，すなわち $a\leqq0$ のとき、区間で増加するから　$M(a)=f(a+1)=(a+1)e^{-a-1}$<br>"
         r"(ii) $a<1<a+1$，すなわち $0<a<1$ のとき、区間内の $x=1$ で最大となり　$M(a)=f(1)=\dfrac1e$<br>"
         r"(iii) $a\geqq1$ のとき、区間で減少するから　$M(a)=f(a)=ae^{-a}$<br>"
         r"答　$\boldsymbol{a\leqq0}$ のとき $\boldsymbol{M(a)=(a+1)e^{-a-1}}$，$\boldsymbol{0<a<1}$ のとき $\boldsymbol{M(a)=\dfrac1e}$，$\boldsymbol{a\geqq1}$ のとき $\boldsymbol{M(a)=ae^{-a}}$",
  "note": r"最小値を求める場合は、区間の両端の値 $f(a)$ と $f(a+1)$ の大小を比べる必要があり、$f(a)=f(a+1)$ となる $a$ が場合分けの境目になる。最大と最小で場合分けの仕方が違うことに注意。",
  "ex": r"$a>0$ とする。関数 $f(x)=\dfrac{\log x}{x}$ の $a\leqq x\leqq2a$ における最大値を求めよ。",
  "exa": r"$0<a\leqq\dfrac e2$ のとき $\dfrac{\log2a}{2a}$，$\dfrac e2<a<e$ のとき $\dfrac1e$，$a\geqq e$ のとき $\dfrac{\log a}{a}$"},
 {"lv": 3, "title": r"図形への応用（角を変数にとる）",
  "q": _fig54() +
       r"幅 $1$ の通路と幅 $3\sqrt3$ の通路が、図のように直角に交わっている。床に水平に保ったまま、この角を曲がって運ぶことのできる棒の長さの最大値を求めよ。ただし、棒の太さは考えない。",
  "hint": r"内側の角 $\mathrm P$ を通り、両側の外壁に両端をもつ線分の長さ $L(\theta)$ を、線分の傾き $\theta$ で表す。棒が通れる長さの最大値は $L(\theta)$ の<b>最小値</b>である。",
  "sol": r"図のように、内側の角 $\mathrm P$ を通り、両側の外壁に両端をもつ線分を考え、線分が幅 $1$ の通路の外壁となす角を $\theta$（$0<\theta<\dfrac\pi2$）とする。この線分の長さは<br>"
         r"$L(\theta)=\dfrac{1}{\sin\theta}+\dfrac{3\sqrt3}{\cos\theta}$<br>"
         r"棒の向きが $\theta$ のとき、角の部分を通れる棒の長さは $L(\theta)$ 以下である。角を曲がる間に $\theta$ は $0$ から $\dfrac\pi2$ までのすべての値をとるから、運べる棒の長さの最大値は $L(\theta)$ の最小値に等しい。<br>"
         r"$L'(\theta)=-\dfrac{\cos\theta}{\sin^2\theta}+\dfrac{3\sqrt3\sin\theta}{\cos^2\theta}=\dfrac{3\sqrt3\sin^3\theta-\cos^3\theta}{\sin^2\theta\cos^2\theta}=\dfrac{\cos\theta\,(3\sqrt3\tan^3\theta-1)}{\sin^2\theta}$<br>"
         r"$L'(\theta)=0$ $\iff$ $\tan^3\theta=\dfrac{1}{3\sqrt3}$ $\iff$ $\tan\theta=\dfrac{1}{\sqrt3}$ $\iff$ $\theta=\dfrac\pi6$。<br>"
         r"$0<\theta<\dfrac\pi6$ で $L'(\theta)<0$，$\dfrac\pi6<\theta<\dfrac\pi2$ で $L'(\theta)>0$ だから、$L(\theta)$ は $\theta=\dfrac\pi6$ で最小となり<br>"
         r"$L\left(\dfrac\pi6\right)=\dfrac{1}{\frac12}+\dfrac{3\sqrt3}{\frac{\sqrt3}2}=2+6=8$　　答　$\boldsymbol{8}$",
  "note": r"一般に幅 $p,\ q$ の通路なら $L(\theta)=\dfrac p{\sin\theta}+\dfrac q{\cos\theta}$ の最小値は $\tan^3\theta=\dfrac pq$ のときで、その値は $\left(p^{\frac23}+q^{\frac23}\right)^{\frac32}$。ここでは $(1+3)^{\frac32}=8$。",
  "ex": r"幅 $1$ の通路と幅 $8$ の通路が直角に交わっているとき、床に水平に保ったまま角を曲がって運ぶことのできる棒の長さの最大値を求めよ。",
  "exa": r"$5\sqrt5$"},
 {"lv": 4, "title": r"2曲線上の点の距離の最小値",
  "q": r"曲線 $C_1:y=e^x$ 上の点 $\mathrm P$ と、曲線 $C_2:y=\log x$ 上の点 $\mathrm Q$ の距離 $\mathrm{PQ}$ の最小値を求めよ。",
  "hint": r"$C_1$ と $C_2$ は直線 $y=x$ に関して対称で、$y=x$ をはさんで反対側にある。$\mathrm{PQ}$ は「$\mathrm P$ と直線 $y=x$ の距離」と「$\mathrm Q$ と直線 $y=x$ の距離」の和以上であることを使う。",
  "sol": _fig55() +
         r"$g(x)=e^x-x$ とすると $g'(x)=e^x-1$ より、$g(x)$ は $x=0$ で最小値 $1$ をとる。よって $e^x>x$ で、$C_1$ は直線 $\ell:y=x$ の上側にある。<br>"
         r"$h(x)=x-\log x$（$x>0$）とすると $h'(x)=1-\dfrac1x$ より、$h(x)$ は $x=1$ で最小値 $1$ をとる。よって $C_2$ は $\ell$ の下側にある。<br>"
         r"$\mathrm P(s,\ e^s)$，$\mathrm Q(t,\ \log t)$ とすると、$\ell$ との距離はそれぞれ<br>"
         r"$\dfrac{e^s-s}{\sqrt2}\geqq\dfrac1{\sqrt2}$，$\dfrac{t-\log t}{\sqrt2}\geqq\dfrac1{\sqrt2}$<br>"
         r"$\mathrm P$，$\mathrm Q$ は $\ell$ の反対側にあるから、線分 $\mathrm{PQ}$ は $\ell$ と点 $\mathrm R$ で交わり<br>"
         r"$\mathrm{PQ}=\mathrm{PR}+\mathrm{RQ}\geqq\dfrac{e^s-s}{\sqrt2}+\dfrac{t-\log t}{\sqrt2}\geqq\dfrac{2}{\sqrt2}=\sqrt2$<br>"
         r"等号は $s=0$，$t=1$，すなわち $\mathrm P(0,\ 1)$，$\mathrm Q(1,\ 0)$ のとき成り立つ（このとき $\mathrm{PQ}\perp\ell$，$\mathrm{PQ}=\sqrt2$）。<br>"
         r"よって、最小値は　$\boldsymbol{\sqrt2}$",
  "note": r"2変数の関数 $\mathrm{PQ}^2=(s-t)^2+(e^s-\log t)^2$ を直接扱うのは困難。逆関数のグラフが $y=x$ に関して対称であることを利用するのが鍵である。等号が成り立つとき、$\mathrm{PQ}$ は2曲線の共通の法線になっている。",
  "ex": r"曲線 $y=e^{2x}$ 上の点と、曲線 $y=\dfrac12\log x$ 上の点の距離の最小値を求めよ。",
  "exa": r"$\dfrac{1+\log2}{\sqrt2}$"},
 {"lv": 5, "title": r"最大値の最小値（1次式による近似）",
  "q": r"実数 $a,\ b$ に対し、$0\leqq x\leqq1$ における $|e^x-ax-b|$ の最大値を $M(a,\ b)$ とする。$a,\ b$ が実数全体を動くとき、$M(a,\ b)$ の最小値を求めよ。",
  "hint": r"曲線 $y=e^x$（$0\leqq x\leqq1$）の両端を結ぶ弦と、それに平行な接線との「真ん中」の直線が最良と予想できる。それより小さくできないことは、3点 $x=0,\ c,\ 1$ での値の<b>うまい1次結合</b>をつくって $a,\ b$ を消去して示す。",
  "sol": r"$c=\log(e-1)$ とおく。$1<e-1<e$ より $0<c<1$ で、$e^c=e-1$（平均値の定理の $c$）。<br>"
         r"$g(x)=e^x-(e-1)x$ とおくと $g'(x)=e^x-(e-1)$ より、$g(x)$ は $0\leqq x\leqq c$ で減少、$c\leqq x\leqq1$ で増加する。$g(0)=g(1)=1$，$g(c)=(e-1)(1-c)$ で、$g(c)<g(0)=1$。<br>"
         r"$m=\dfrac{1-g(c)}{2}=\dfrac{2-e+(e-1)\log(e-1)}{2}\ (>0)$ とおく。<br>"
         r"<b>[1]</b> $a=e-1$，$b=\dfrac{1+g(c)}{2}$ のとき、$0\leqq x\leqq1$ で $g(c)\leqq g(x)\leqq1$ だから<br>"
         r"$-m\leqq e^x-ax-b=g(x)-b\leqq m$<br>"
         r"で、$x=0$ のとき $m$ に等しい。よって $M(a,\ b)=m$。<br>"
         r"<b>[2]</b> 任意の $a,\ b$ について、$\varphi(x)=e^x-ax-b$，$M=M(a,\ b)$ とおくと $|\varphi(0)|,\ |\varphi(c)|,\ |\varphi(1)|\leqq M$。ここで<br>"
         r"$(1-c)\varphi(0)+c\varphi(1)-\varphi(c)=(1-c)(1-b)+c(e-a-b)-(e-1-ac-b)=2-e+(e-1)c=2m$<br>"
         r"（$a,\ b$ が消える）。$0<c<1$ だから<br>"
         r"$2m\leqq(1-c)|\varphi(0)|+c|\varphi(1)|+|\varphi(c)|\leqq(1-c)M+cM+M=2M$<br>"
         r"よって $M(a,\ b)\geqq m$。<br>"
         r"[1]，[2] より、$M(a,\ b)$ の最小値は　$\boldsymbol{\dfrac{2-e+(e-1)\log(e-1)}{2}}$（$a=e-1$，$b=\dfrac{e-(e-1)\log(e-1)}{2}$ のとき）",
  "note": r"最良の直線では、誤差 $e^x-ax-b$ が $x=0,\ c,\ 1$ で $m,\ -m,\ m$ と符号を交互に変えながら最大の絶対値をとる。この「交互に等しい誤差をとる」性質が最良近似の目印になる。数値は $m=0.1059\cdots$。係数 $1-c,\ c,\ 1$ は、$1$ と $x$ の項がともに消えるように選んだものである。",
  "ex": r"実数 $a,\ b$ に対し、$1\leqq x\leqq e$ における $|\log x-ax-b|$ の最大値を $M(a,\ b)$ とする。$a,\ b$ が実数全体を動くとき、$M(a,\ b)$ の最小値を求めよ。",
  "exa": r"$\dfrac12\left\{\log(e-1)-\dfrac{e-2}{e-1}\right\}$（$a=\dfrac1{e-1}$ のとき）"},
]})


def _v5():
    f = x * sqrt(4 - x**2)
    assert simplify(diff(f, x) - (4 - 2 * x**2) / sqrt(4 - x**2)) == 0
    vals = [v * math.sqrt(4 - v * v) for v in _grid(-2, 2, 40000)]
    assert abs(max(vals) - 2) < 1e-8 and abs(min(vals) + 2) < 1e-8 and simplify(f.subs(x, sqrt(2)) - 2) == 0
    f = x * sqrt(1 - x)
    assert simplify(diff(f, x) - (2 - 3 * x) / (2 * sqrt(1 - x))) == 0
    vals = [v * math.sqrt(1 - v) for v in _grid(-3, 1, 40000)]
    assert abs(max(vals) - 2 * math.sqrt(3) / 9) < 1e-8 and abs(min(vals) + 6) < 1e-12
    assert simplify(f.subs(x, Rational(2, 3)) - 2 * sqrt(3) / 9) == 0
    # 三角関数
    f = 2 * sin(x) + sin(2 * x)
    assert simplify(expand(diff(f, x) - 2 * (2 * cos(x) - 1) * (cos(x) + 1), trig=True)) == 0
    vals = [2 * math.sin(v) + math.sin(2 * v) for v in _grid(0, 2 * math.pi, 40000)]
    assert abs(max(vals) - 1.5 * math.sqrt(3)) < 1e-8 and abs(min(vals) + 1.5 * math.sqrt(3)) < 1e-8
    assert simplify(f.subs(x, pi / 3) - 3 * sqrt(3) / 2) == 0
    f = (1 + sin(x)) * cos(x)
    assert simplify(expand(diff(f, x) + (2 * sin(x) - 1) * (sin(x) + 1), trig=True)) == 0
    vals = [(1 + math.sin(v)) * math.cos(v) for v in _grid(0, 2 * math.pi, 40000)]
    assert abs(max(vals) - 0.75 * math.sqrt(3)) < 1e-8 and abs(min(vals) + 0.75 * math.sqrt(3)) < 1e-8
    assert simplify(f.subs(x, pi / 6) - 3 * sqrt(3) / 4) == 0 and simplify(f.subs(x, 5 * pi / 6) + 3 * sqrt(3) / 4) == 0
    # 区間が動く
    F = lambda v: v * math.exp(-v)
    for A in [-3, -1, -0.2, 0, 0.3, 0.7, 0.99, 1, 1.5, 4]:
        mx = max(F(v) for v in _grid(A, A + 1, 4000))
        M = (A + 1) * math.exp(-A - 1) if A <= 0 else (1 / math.e if A < 1 else A * math.exp(-A))
        assert abs(mx - M) < 1e-7, A
    F = lambda v: math.log(v) / v
    for A in [0.2, 1, math.e / 2, 1.5, 2, 2.7, math.e, 3, 6]:
        mx = max(F(v) for v in _grid(A, 2 * A, 4000))
        M = math.log(2 * A) / (2 * A) if A <= math.e / 2 else (1 / math.e if A < math.e else math.log(A) / A)
        assert abs(mx - M) < 1e-7, A
    # 通路
    L = lambda th: 1 / math.sin(th) + 3 * math.sqrt(3) / math.cos(th)
    ths = _grid(1e-4, math.pi / 2 - 1e-4, 200000)
    assert abs(min(L(v) for v in ths) - 8) < 1e-8 and abs(L(math.pi / 6) - 8) < 1e-12
    th = symbols("th", positive=True)
    Ls = 1 / sin(th) + 3 * sqrt(3) / cos(th)
    assert simplify(diff(Ls, th) - (3 * sqrt(3) * sin(th)**3 - cos(th)**3) / (sin(th)**2 * cos(th)**2)) == 0
    assert simplify(Ls.subs(th, pi / 6)) == 8
    assert abs(math.hypot(3 * math.sqrt(3) + math.sqrt(3), 4) - 8) < 1e-12        # 図の線分
    L2 = lambda v: 1 / math.sin(v) + 8 / math.cos(v)
    assert abs(min(L2(v) for v in ths) - 5 * math.sqrt(5)) < 1e-8
    # 2曲線の距離
    def dmin(f1, f2, s0, s1, t0, t1, n=500):
        S_ = _grid(s0, s1, n); T_ = _grid(t0, t1, n)
        F2 = [(tv, f2(tv)) for tv in T_]
        best = min(math.hypot(sv - tv, f1(sv) - w) for sv in S_ for tv, w in F2)
        return best
    d = dmin(math.exp, math.log, -3, 2, 0.05, 4)
    assert abs(d - math.sqrt(2)) < 1e-3 and d >= math.sqrt(2) - 1e-12
    assert abs(math.hypot(0 - 1, math.exp(0) - math.log(1)) - math.sqrt(2)) < 1e-15
    for _ in range(3000):
        sv, tv = random.uniform(-4, 3), random.uniform(0.01, 6)
        assert math.hypot(sv - tv, math.exp(sv) - math.log(tv)) >= math.sqrt(2) - 1e-12
    val = (1 + math.log(2)) / math.sqrt(2)
    d = dmin(lambda v: math.exp(2 * v), lambda v: 0.5 * math.log(v), -2, 1, 0.05, 3)
    assert abs(d - val) < 2e-3 and d >= val - 1e-12
    for _ in range(3000):
        sv, tv = random.uniform(-4, 2), random.uniform(0.01, 6)
        assert math.hypot(sv - tv, math.exp(2 * sv) - 0.5 * math.log(tv)) >= val - 1e-12
    # 最大値の最小値
    c = math.log(math.e - 1)
    m = (2 - math.e + (math.e - 1) * c) / 2
    assert 0 < c < 1 and abs(m - 0.10593) < 1e-4
    xs = _grid(0, 1, 20000)
    Mab = lambda A, B: max(abs(math.exp(v) - A * v - B) for v in xs)
    a0, b0 = math.e - 1, (math.e - (math.e - 1) * c) / 2
    assert abs(Mab(a0, b0) - m) < 1e-9
    for _ in range(300):
        A, B = a0 + random.uniform(-0.3, 0.3), b0 + random.uniform(-0.3, 0.3)
        assert Mab(A, B) >= m - 1e-12
    cs = symbols("c")
    phi = lambda v: (exp(v) if v != cs else (E - 1)) - a * v - b
    comb = expand((1 - cs) * phi(0) + cs * phi(1) - phi(cs))
    assert simplify(comb - (2 - E + (E - 1) * cs)) == 0
    # 練習：log x on [1, e]
    c2 = math.e - 1
    m2 = (math.log(math.e - 1) - (math.e - 2) / (math.e - 1)) / 2
    xs = _grid(1, math.e, 20000)
    Mab = lambda A, B: max(abs(math.log(v) - A * v - B) for v in xs)
    a1 = 1 / (math.e - 1)
    g1 = math.log(1) - a1 * 1
    gc = math.log(c2) - a1 * c2
    b1 = (g1 + gc) / 2
    assert abs(Mab(a1, b1) - m2) < 1e-9 and m2 > 0
    for _ in range(300):
        A, B = a1 + random.uniform(-0.2, 0.2), b1 + random.uniform(-0.2, 0.2)
        assert Mab(A, B) >= m2 - 1e-12
    w1, we = 1 / (math.e - 1), (math.e - 2) / (math.e - 1)
    assert abs(w1 + we - 1) < 1e-15 and abs(w1 * 1 + we * math.e - c2) < 1e-14
    assert abs((w1 * 0 + we * 1 - math.log(c2)) + 2 * m2) < 1e-14


# ---------------------------------------------------------------- 節6 の図
def _fig61():
    g = _G(180, 130, (-0.3, 2.2), (-0.6, 1.55))
    g.axes()
    g.curve(lambda v: v * math.log(v), 1e-6, 2.2)
    r = 1 / math.e
    g.pt(r, -r)
    g.seg((r, 0), (r, -r))
    g.seg((0, -r), (r, -r))
    g.pt(0, 0, hollow=True, r=2.2)
    g.xtick(1, "1")
    g.txt(r, 0, "1/e", dy=-4, size=9.5)
    g.txt(0, -r, "−1/e", dx=-3, dy=3.5, anc="end", size=9.5)
    g.seg((-0.25, -0.2), (2.15, -0.2), col=C2, w=1.0, dash="")
    g.txt(2.15, -0.2, "y=a", anc="end", dy=12, it=True, col=C2)
    g.txt(0.25, 1.25, "y=x log x", anc="start", it=True, size=9.5)
    return g.svg()


def _fig62():
    g = _G(210, 130, (-1.2, 7.2), (-0.14, 0.86))
    g.axes()
    g.curve(lambda v: v * v * math.exp(-v), -1.2, 7.2)
    M = 4 / math.e ** 2
    g.pt(2, M)
    g.seg((2, 0), (2, M))
    g.seg((0, M), (2, M))
    g.xtick(2, "2")
    g.txt(0, M, "4/e²", dx=4, dy=-3, anc="start", size=9.5)
    g.seg((-1.15, 0.3), (7.1, 0.3), col=C2, w=1.0, dash="")
    g.txt(7.1, 0.3, "y=a", anc="end", dy=-4, it=True, col=C2)
    g.txt(4.6, 0.62, "y=x²e⁻ˣ", anc="start", it=True, size=9.5)
    return g.svg()


def _fig63():
    g = _G(210, 150, (-0.4, 9.2), (-0.75, 0.55))
    g.axes()
    g.curve(lambda v: math.log(v) / v, 0.3, 9.2)
    g.pt(math.e, 1 / math.e)
    g.seg((math.e, 0), (math.e, 1 / math.e))
    g.seg((0, 1 / math.e), (math.e, 1 / math.e))
    g.xtick(1, "1")
    g.txt(math.e, 0, "e", dy=11, it=True)
    g.txt(0, 1 / math.e, "1/e", dx=-3, dy=3.5, anc="end", size=9.5)
    g.seg((-0.35, 0.2), (9.1, 0.2), col=C2, w=1.0, dash="")
    g.txt(7.3, 0.2, "y=log a", anc="middle", dy=12, it=True, col=C2)
    g.txt(4.0, -0.4, "y=(log x)/x", anc="start", it=True, size=9.5)
    return g.svg()


def _fig65():
    g = _G(250, 175, (-1.1, 7.6), (-0.42, 0.78))
    f = lambda v: v * math.exp(-v)
    L = lambda v: (4 - v) / math.e ** 2
    xs = _grid(-1.1, 2, 120)
    g.fill([(v, L(v)) for v in xs] + [(v, max(f(v), 0)) for v in reversed(xs)])
    xs = _grid(2, 7.6, 160)
    g.fill([(v, f(v)) for v in xs] + [(v, max(L(v), 0)) for v in reversed(xs)])
    g.axes()
    g.curve(f, -1.1, 7.6)
    g.curve(L, -1.1, 7.6, col=C2, w=1.1)
    g.pt(2, 2 / math.e ** 2, col="#333", hollow=True, r=2.2)
    g.txt(2, 2 / math.e ** 2, "A", dx=3, dy=-6, anc="start", it=True)
    g.xtick(2, "2")
    g.xtick(4, "4")
    g.xtick(1, "1")
    g.txt(-0.6, 0.62, "ℓ", it=True, col=C2, size=11)
    g.txt(-0.45, -0.3, "C", it=True, col=C1, size=11)
    g.txt(5.3, 0.17, "C", it=True, col=C1, size=11)
    return g.svg()


# ---------------------------------------------------------------- 節6
SEC.append({"title": r"方程式の実数解の個数",
"base": r"""・方程式 $f(x)=a$ の実数解の個数は、曲線 $y=f(x)$ と直線 $y=a$ の共有点の個数に等しい。文字定数は分離できれば分離する。<br>
・グラフをかくときは、増減・極値に加え、$x\to\pm\infty$ や定義域の端での極限を必ず調べる（「近づくが到達しない値」に注意）。<br>
・解の存在は中間値の定理で、解がただ1つであることは単調性で示す。<br>
・曲線外の点から引ける接線の本数は「接点の個数」を数える。異なる2点で接する直線がないことを確かめておく。""",
"items": [
 {"lv": 2, "title": r"定数を分離して解の個数を調べる",
  "q": r"$a$ を定数とする。方程式 $\log x=\dfrac ax$ の異なる実数解の個数を調べよ。",
  "hint": r"真数条件 $x>0$ のもとで両辺に $x$ を掛けると $x\log x=a$。$y=x\log x$ のグラフと直線 $y=a$ の共有点を数える。$x\to+0$ での極限に注意。",
  "sol": _fig61() +
         r"真数条件より $x>0$。$x>0$ のとき、方程式は $x\log x=a$ と同値である。<br>"
         r"$h(x)=x\log x$ とおくと $h'(x)=\log x+1$ で、$h(x)$ は $0<x\leqq\dfrac1e$ で減少、$x\geqq\dfrac1e$ で増加し、最小値 $h\left(\dfrac1e\right)=-\dfrac1e$ をとる。<br>"
         r"また $\displaystyle\lim_{x\to+0}x\log x=0$，$\displaystyle\lim_{x\to\infty}x\log x=\infty$ で、$0<x<1$ では $h(x)<0$。<br>"
         r"$y=h(x)$ のグラフ（図）と直線 $y=a$ の共有点の個数を調べて<br>"
         r"$\boldsymbol{a<-\dfrac1e}$ のとき $\boldsymbol0$ 個，$\boldsymbol{a=-\dfrac1e}$ のとき $\boldsymbol1$ 個，$\boldsymbol{-\dfrac1e<a<0}$ のとき $\boldsymbol2$ 個，$\boldsymbol{a\geqq0}$ のとき $\boldsymbol1$ 個",
  "note": r"$x\to+0$ のとき $h(x)\to0$ だが、$h(x)=0$ にはならない（図の白丸）。そのため $a=0$ のときは $x=1$ の1個だけ、$-\dfrac1e<a<0$ では $0<x<\dfrac1e$ と $\dfrac1e<x<1$ に1個ずつとなる。",
  "ex": r"$a$ を定数とする。方程式 $e^{x}=\dfrac{a}{x}$ の異なる実数解の個数を調べよ。",
  "exa": r"$a<-\dfrac1e$ のとき0個，$a=-\dfrac1e$ のとき1個，$-\dfrac1e<a<0$ のとき2個，$a=0$ のとき0個，$a>0$ のとき1個"},
 {"lv": 3, "title": r"解の個数（極限の扱いに注意）",
  "q": r"$a$ を定数とする。方程式 $x^2=ae^{x}$ の異なる実数解の個数を調べよ。",
  "hint": r"$e^x>0$ で割ると $x^2e^{-x}=a$。$y=x^2e^{-x}$ のグラフをかく。$x\to\infty$ で $y\to0$ となることが、解の個数を決めるポイントになる。",
  "sol": _fig62() +
         r"$e^x>0$ より、方程式は $x^2e^{-x}=a$ と同値。$g(x)=x^2e^{-x}$ とおくと<br>"
         r"$g'(x)=(2x-x^2)e^{-x}=-x(x-2)e^{-x}$<br>"
         + _tb([r"$x$", DOT, r"$0$", DOT, r"$2$", DOT],
               [r"$g'(x)$", r"$-$", r"$0$", r"$+$", r"$0$", r"$-$"],
               [r"$g(x)$", DN, r"$0$", UP, r"$\dfrac4{e^2}$", DN]) +
         r"$\displaystyle\lim_{x\to-\infty}g(x)=\infty$，$\displaystyle\lim_{x\to\infty}g(x)=\lim_{x\to\infty}\frac{x^2}{e^x}=0$ で、$x\neq0$ のとき $g(x)>0$。<br>"
         r"$y=g(x)$ のグラフ（図）と直線 $y=a$ の共有点の個数を調べて<br>"
         r"$\boldsymbol{a<0}$ のとき $\boldsymbol0$ 個，$\boldsymbol{a=0}$ のとき $\boldsymbol1$ 個，$\boldsymbol{0<a<\dfrac4{e^2}}$ のとき $\boldsymbol3$ 個，$\boldsymbol{a=\dfrac4{e^2}}$ のとき $\boldsymbol2$ 個，$\boldsymbol{a>\dfrac4{e^2}}$ のとき $\boldsymbol1$ 個",
  "note": r"$\displaystyle\lim_{x\to\infty}\frac{x^2}{e^x}=0$ を確認しないと、$x>2$ の部分で直線 $y=a$ と交わるかどうかが判断できない。この極限は、$x>0$ で $e^x>\dfrac{x^3}{6}$（微分を3回くり返して示せる）から $0<\dfrac{x^2}{e^x}<\dfrac6x$ として得られる。",
  "ex": r"$a$ を定数とする。方程式 $x=ae^{x^2}$ の異なる実数解の個数を調べよ。",
  "exa": r"$|a|>\dfrac1{\sqrt{2e}}$ のとき0個，$|a|=\dfrac1{\sqrt{2e}}$ のとき1個，$0<|a|<\dfrac1{\sqrt{2e}}$ のとき2個，$a=0$ のとき1個"},
 {"lv": 3, "title": r"指数方程式 $a^x=x$ の解の個数",
  "q": r"$a$ を正の定数とする。方程式 $a^x=x$ の異なる実数解の個数を調べよ。",
  "hint": r"$a^x>0$ だから解は正。両辺の自然対数をとると $x\log a=\log x$，すなわち $\dfrac{\log x}{x}=\log a$。$y=\dfrac{\log x}{x}$ のグラフと直線 $y=\log a$ の共有点を数える。",
  "sol": _fig63() +
         r"$a^x>0$ だから、解は $x>0$ の範囲にある。$x>0$ のとき<br>"
         r"$a^x=x\iff x\log a=\log x\iff\dfrac{\log x}{x}=\log a$<br>"
         r"$g(x)=\dfrac{\log x}{x}$ とおくと $g'(x)=\dfrac{1-\log x}{x^2}$ より、$g(x)$ は $0<x\leqq e$ で増加、$x\geqq e$ で減少し、最大値 $g(e)=\dfrac1e$。<br>"
         r"$\displaystyle\lim_{x\to+0}g(x)=-\infty$，$\displaystyle\lim_{x\to\infty}g(x)=0$ で、$x>1$ のとき $g(x)>0$。<br>"
         r"$y=g(x)$ のグラフ（図）と直線 $y=\log a$ の共有点の個数を調べて<br>"
         r"$\log a\leqq0$，すなわち $\boldsymbol{0<a\leqq1}$ のとき $\boldsymbol1$ 個<br>"
         r"$0<\log a<\dfrac1e$，すなわち $\boldsymbol{1<a<e^{\frac1e}}$ のとき $\boldsymbol2$ 個<br>"
         r"$\log a=\dfrac1e$，すなわち $\boldsymbol{a=e^{\frac1e}}$ のとき $\boldsymbol1$ 個<br>"
         r"$\log a>\dfrac1e$，すなわち $\boldsymbol{a>e^{\frac1e}}$ のとき $\boldsymbol0$ 個",
  "note": r"$a=e^{\frac1e}=1.444\cdots$ のとき、曲線 $y=a^x$ と直線 $y=x$ は点 $(e,\ e)$ で接する。例えば $a=\sqrt2$ $\left(<e^{\frac1e}\right)$ のときは $x=2,\ 4$ の2つの解をもつ（$\sqrt2^{\,2}=2$，$\sqrt2^{\,4}=4$）。",
  "ex": r"$a$ を正の定数とする。$x>0$ の範囲で、方程式 $x^a=a^x$ の異なる実数解の個数を調べよ。",
  "exa": r"$0<a\leqq1$ または $a=e$ のとき1個（$x=a$ のみ），$1<a<e$ または $a>e$ のとき2個"},
 {"lv": 4, "title": r"2つの解の和の評価（極値点からのずれ）",
  "q": r"$a>1$ とする。<br>"
       r"(1) 方程式 $e^x=x+a$ はちょうど2つの実数解をもつことを示せ。また、2つの解を $\alpha,\ \beta$（$\alpha<\beta$）とすると、$\alpha<0<\beta$ であることを示せ。<br>"
       r"(2) $\alpha+\beta<0$ であることを示せ。",
  "hint": r"(1) $f(x)=e^x-x$ の増減を調べる。(2) 示すべきは $\alpha<-\beta$。$\alpha$ と $-\beta$ はともに $f$ が減少する範囲 $x<0$ にあるので、$f(\alpha)$ と $f(-\beta)$ の大小に言いかえ、$f(\alpha)=f(\beta)$ を使う。",
  "sol": r"(1) $f(x)=e^x-x$ とおくと、方程式は $f(x)=a$ と同値。$f'(x)=e^x-1$ より、$f(x)$ は $x\leqq0$ で減少、$x\geqq0$ で増加し、最小値 $f(0)=1$。<br>"
         r"また $\displaystyle\lim_{x\to-\infty}f(x)=\infty$，$\displaystyle\lim_{x\to\infty}f(x)=\lim_{x\to\infty}x\left(\frac{e^x}{x}-1\right)=\infty$。$f(x)$ は連続で $a>1$ だから、$f(x)=a$ は $x<0$ と $x>0$ にそれぞれただ1つの解をもつ。よって解はちょうど2つで、$\alpha<0<\beta$。<br>"
         r"(2) $\psi(t)=f(t)-f(-t)=e^t-e^{-t}-2t$ とおくと<br>"
         r"$\psi'(t)=e^t+e^{-t}-2=\left(e^{\frac t2}-e^{-\frac t2}\right)^2$<br>"
         r"で、$t>0$ のとき $\psi'(t)>0$。$\psi(0)=0$ だから、$t>0$ のとき $\psi(t)>0$。<br>"
         r"$\beta>0$ だから $f(\beta)>f(-\beta)$，すなわち　$f(\alpha)=a=f(\beta)>f(-\beta)$<br>"
         r"$\alpha<0$，$-\beta<0$ で、$f(x)$ は $x\leqq0$ で減少するから、$f(\alpha)>f(-\beta)$ より $\alpha<-\beta$。<br>"
         r"よって　$\alpha+\beta<0$　$\blacksquare$",
  "note": r"$\psi(t)>0$ は「極小点 $x=0$ から同じ距離だけ離れると、右側の方が値が大きい」こと、つまりグラフが左右対称でないことを表す。2つの解は極小点から等距離にはなく、右側の解の方が極小点に近い。この型は入試でくり返し出題される。",
  "ex": r"$0<a<\dfrac1e$ とする。方程式 $xe^{-x}=a$ の2つの実数解を $\alpha,\ \beta$（$\alpha<\beta$）とするとき、$\alpha+\beta>2$ であることを示せ。",
  "exa": r"$f(x)=xe^{-x}$ とすると $0<\alpha<1<\beta$。$\psi(t)=f(1+t)-f(1-t)$ は $\psi'(t)=\dfrac{t(e^t-e^{-t})}{e}>0$（$t>0$）より $t>0$ で正。$f(\beta)=f(\alpha)<f(2-\alpha)$ で、$f$ は $x\geqq1$ で減少するから $\beta>2-\alpha$。"},
 {"lv": 5, "title": r"点から引ける接線の本数（存在範囲の図示）",
  "q": r"曲線 $C:y=xe^{-x}$ について、次の問いに答えよ。<br>"
       r"(1) $C$ の変曲点 $\mathrm A$ の座標と、$\mathrm A$ における $C$ の接線 $\ell$ の方程式を求めよ。<br>"
       r"(2) $C$ 上の異なる2点で $C$ に接する直線は存在しないことを示せ。<br>"
       r"(3) 点 $(p,\ q)$ から $C$ にちょうど3本の接線が引けるような点 $(p,\ q)$ の存在範囲を求め、図示せよ。",
  "hint": r"(2) 2点で接するとすると、差の関数にロルの定理をくり返し使えて、$y''=0$ の解が2つ以上必要になる。(3) 接点を $(t,\ te^{-t})$ とすると、接線が $(p,\ q)$ を通る条件は $q=g(t)$ の形の $t$ の方程式。(2) より接線の本数＝実数解 $t$ の個数。$g'(t)$ を因数分解すると $t=2,\ p$ が極値点になるので、$p$ と $2$ の大小で場合を分ける。",
  "sol": r"(1) $y'=(1-x)e^{-x}$，$y''=(x-2)e^{-x}$。$y''$ は $x=2$ の前後で符号を変えるから、変曲点は $\boldsymbol{\mathrm A\left(2,\ \dfrac{2}{e^2}\right)}$。$y'(2)=-\dfrac{1}{e^2}$ より、$\ell:y=-\dfrac1{e^2}(x-2)+\dfrac2{e^2}$，すなわち $\boldsymbol{y=\dfrac{4-x}{e^2}}$<br>"
         r"(2) $f(x)=xe^{-x}$ とし、直線 $y=kx+n$ が $C$ に $x=s,\ t$（$s<t$）の2点で接すると仮定する。$d(x)=f(x)-(kx+n)$ とおくと $d(s)=d(t)=0$，$d'(s)=d'(t)=0$。ロルの定理より $d'(u)=0$ となる $u$（$s<u<t$）があり、さらに $d'(x)$ に区間 $s\leqq x\leqq u$，$u\leqq x\leqq t$ でロルの定理を用いると、$d''(x)=f''(x)=(x-2)e^{-x}$ が $0$ となる $x$ が $s<x<u$ と $u<x<t$ に1つずつ存在する。これは $f''(x)=0$ の解が $x=2$ だけであることに矛盾する。$\blacksquare$<br>"
         r"(3) 接点 $(t,\ te^{-t})$ における接線 $y=(1-t)e^{-t}(x-t)+te^{-t}$ が点 $(p,\ q)$ を通る条件は<br>"
         r"$q=\{(1-t)(p-t)+t\}e^{-t}=(t^2-pt+p)e^{-t}$ …①<br>"
         r"(2) より接点が異なれば接線も異なるから、接線の本数は①を満たす実数 $t$ の個数に等しい。$g(t)=(t^2-pt+p)e^{-t}$ とおくと<br>"
         r"$g'(t)=\{(2t-p)-(t^2-pt+p)\}e^{-t}=-(t-2)(t-p)e^{-t}$<br>"
         r"$g(2)=\dfrac{4-p}{e^2}$，$g(p)=pe^{-p}$，$\displaystyle\lim_{t\to-\infty}g(t)=\infty$，$\displaystyle\lim_{t\to\infty}g(t)=0$。<br>"
         r"・$p<2$ のとき　$g(t)$ は $t\leqq p$ で減少、$p\leqq t\leqq2$ で増加、$t\geqq2$ で減少する。$t>2$ では $g(t)$ は $g(2)$ から減少しながら $0$ に近づくので $0<g(t)<g(2)$。したがって①の解は、$t<p$ に $q>g(p)$ のとき1個、$p<t<2$ に $g(p)<q<g(2)$ のとき1個、$t>2$ に $0<q<g(2)$ のとき1個あり、それ以外の $q$ では解は高々2個。よって3個となる条件は　$g(p)<q<g(2)$ かつ $q>0$<br>"
         r"・$p=2$ のとき　$g'(t)=-(t-2)^2e^{-t}\leqq0$ で $g(t)$ は単調に減少し、解は高々1個。<br>"
         r"・$p>2$ のとき　$g(t)$ は $t\leqq2$ で減少、$2\leqq t\leqq p$ で増加、$t\geqq p$ で減少するから、同様にして3個となる条件は　$g(2)<q<g(p)$ かつ $q>0$<br>"
         r"ここで $k(x)=xe^{-x}-\dfrac{4-x}{e^2}$ とおくと $k'(x)=(1-x)e^{-x}+e^{-2}$，$k''(x)=(x-2)e^{-x}$ より $k'(x)\geqq k'(2)=0$ で $k(x)$ は増加し、$k(2)=0$。よって $C$ は $x<2$ で $\ell$ の下側、$x>2$ で $\ell$ の上側にある。<br>"
         r"以上より、求める範囲は<br>"
         r"$p<2$ のとき $\max\{pe^{-p},\ 0\}<q<\dfrac{4-p}{e^2}$，$p>2$ のとき $\max\left\{\dfrac{4-p}{e^2},\ 0\right\}<q<pe^{-p}$<br>"
         r"すなわち、<b>曲線 $C$ と接線 $\ell$ にはさまれ、かつ $x$ 軸より上側にある部分</b>で、下の図の色をつけた部分（境界線上の点は含まない）。<br>"
         + _fig65().replace('class="fig"', 'class="fig" style="float:none;margin:1.5mm auto"'),
  "note": r"境界はすべて意味をもつ：曲線 $C$ 自身（$p$ が極値点になる場合）、変曲点での接線 $\ell$（$t=2$ が極値点になる場合）、そして漸近線である $x$ 軸（$t\to\infty$ の極限値）。3次関数のグラフで「接線が3本引ける範囲は曲線と変曲点での接線にはさまれた部分」となるのと同じ構造に、漸近線が加わっている。",
  "ex": r"曲線 $y=xe^{x}$ に、点 $(p,\ q)$ からちょうど3本の接線が引けるような点 $(p,\ q)$ の存在範囲を求めよ。",
  "exa": r"曲線 $y=xe^{x}$ と直線 $y=-\dfrac{x+4}{e^2}$（変曲点 $\left(-2,\ -\dfrac2{e^2}\right)$ における接線）にはさまれ、かつ $x$ 軸より下側にある部分（境界を含まない）"},
]})


def _v6():
    import numpy as np
    # x log x = a
    xs = _geo(1e-12, 1e6, 60000)
    h = lambda v: v * math.log(v)
    for A, n in [(-1, 0), (-0.37, 0), (-0.36, 2), (-0.1, 2), (-1e-4, 2), (0, 1), (0.5, 1), (100, 1)]:
        assert _count(lambda v: h(v) - A, xs) == n, (A, n)
    assert min(h(v) for v in xs) >= -1 / math.e - 1e-12 and abs(h(1 / math.e) + 1 / math.e) < 1e-15
    # 練習 x e^x = a（x≠0）
    xs = [v for v in _grid(-60, 30, 180001) if v != 0]
    k = lambda v: v * math.exp(v)
    for A, n in [(-1, 0), (-0.37, 0), (-0.36, 2), (-0.01, 2), (0.01, 1), (5, 1)]:
        assert _count(lambda v: k(v) - A, xs) == n, (A, n)
    assert min(k(v) for v in xs) >= -1 / math.e - 1e-12
    assert all(k(v) != 0 for v in xs)                   # a=0 のときは解なし（x=0 は除く）
    # x^2 e^{-x} = a
    xs = _grid(-30, 60, 180000)
    g = lambda v: v * v * math.exp(-v)
    M = 4 / math.e ** 2
    for A, n in [(-0.1, 0), (0.01, 3), (0.3, 3), (M - 1e-3, 3), (M + 1e-3, 1), (2, 1)]:
        assert _count(lambda v: g(v) - A, xs) == n, (A, n)
    assert max(g(v) for v in _grid(0, 60, 60000)) <= M + 1e-15
    assert _count(lambda v: g(v) - M, [v for v in xs if v < 1]) == 1
    assert limit(x**2 * exp(-x), x, oo) == 0
    # 練習 x e^{-x^2} = a
    xs = _grid(-20, 20, 80000)
    g = lambda v: v * math.exp(-v * v)
    Mx = 1 / math.sqrt(2 * math.e)
    assert abs(max(g(v) for v in xs) - Mx) < 1e-8
    for A, n in [(0, 1), (0.1, 2), (-0.1, 2), (Mx - 1e-3, 2), (Mx + 1e-3, 0), (-Mx - 1e-3, 0)]:
        assert _count(lambda v: g(v) - A, xs) == n, (A, n)
    # a^x = x
    xs = _geo(1e-6, 1e5, 60000)
    for A, n in [(0.2, 1), (0.9, 1), (1, 1), (1.2, 2), (math.sqrt(2), 2), (1.44, 2), (1.45, 0), (3, 0)]:
        assert _count(lambda v: v * math.log(A) - math.log(v), xs) == n, (A, n)
    ae = math.e ** (1 / math.e)
    assert min(v * math.log(ae) - math.log(v) for v in xs) >= -1e-12
    # 練習 x^a = a^x
    for A, n in [(0.3, 1), (1, 1), (1.5, 2), (2, 2), (2.7, 2), (2.75, 2), (5, 2)]:
        assert _count(lambda v: math.log(v) / v - math.log(A) / A, xs) == n, (A, n)
    assert min(1 / math.e - math.log(v) / v for v in xs) >= -1e-15
    # 2解の和
    for _ in range(300):
        A = random.uniform(1.001, 30)
        F = lambda v: math.exp(v) - v - A
        al = _bis(F, -A - 1, 0)
        be = _bis(F, 0, math.log(A) + 2)
        assert al < 0 < be and abs(F(al)) < 1e-9 and abs(F(be)) < 1e-9 and al + be < 0
    for _ in range(300):
        A = random.uniform(1e-4, 1 / math.e - 1e-4)
        F = lambda v: v * math.exp(-v) - A
        al = _bis(F, 0, 1)
        be = _bis(F, 1, 60)
        assert 0 < al < 1 < be and al + be > 2
    s_ = symbols("s", positive=True)
    assert simplify(diff(exp(s_) - exp(-s_) - 2 * s_, s_) - (exp(s_ / 2) - exp(-s_ / 2))**2) == 0
    fpsi = (1 + s_) * exp(-1 - s_) - (1 - s_) * exp(-1 + s_)
    assert simplify(diff(fpsi, s_) - s_ * (exp(s_) - exp(-s_)) / E) == 0
    # 接線の本数（存在範囲）
    p, q = symbols("p q", real=True)
    f = x * exp(-x)
    assert simplify(diff(f, x, 2) - (x - 2) * exp(-x)) == 0
    tl = diff(f, x).subs(x, t) * (x - t) + f.subs(x, t)
    G = simplify(tl.subs(x, p) * exp(t))
    assert expand(G - (t**2 - p * t + p)) == 0
    gt = (t**2 - p * t + p) * exp(-t)
    assert simplify(diff(gt, t) + (t - 2) * (t - p) * exp(-t)) == 0
    assert simplify(diff(f, x).subs(x, 2) * (x - 2) + f.subs(x, 2) - (4 - x) / E**2) == 0
    T = np.linspace(-35, 70, 210001)
    eT = np.exp(-T)

    def nroots(P, Q, sgn=1):
        if sgn == 1:
            v = (T * T - P * T + P) * eT - Q
        else:                                      # 練習：y = x e^x
            v = (-T * T + P * T + P) * np.exp(T) - Q
        v = v[v != 0]
        return int(np.count_nonzero(np.signbit(v[1:]) != np.signbit(v[:-1])))

    random.seed(24)
    cnt3 = 0
    for _ in range(700):
        P, Q = random.uniform(-3, 9), random.uniform(-0.6, 0.9)
        Cv, Lv = P * math.exp(-P), (4 - P) / math.e ** 2
        if min(abs(Q - Cv), abs(Q - Lv), abs(Q)) < 0.01 or abs(P - 2) < 0.05:
            continue
        inside = Q > 0 and min(Cv, Lv) < Q < max(Cv, Lv)
        n = nroots(P, Q)
        assert (n == 3) == inside, (P, Q, n)
        assert n <= 3
        cnt3 += inside
        # 練習：点対称な曲線 y = x e^x
        Cv2, Lv2 = P * math.exp(P), -(P + 4) / math.e ** 2
        if min(abs(Q - Cv2), abs(Q - Lv2), abs(Q)) < 0.01 or abs(P + 2) < 0.05:
            continue
        inside2 = Q < 0 and min(Cv2, Lv2) < Q < max(Cv2, Lv2)
        assert (nroots(P, Q, -1) == 3) == inside2, (P, Q)
    assert cnt3 > 30
    for v in _grid(-5, 9, 2000):                     # C は x<2 で ℓ の下側、x>2 で上側
        dv = v * math.exp(-v) - (4 - v) / math.e ** 2
        assert (dv < 0) if v < 2 - 1e-6 else ((dv > 0) if v > 2 + 1e-6 else True)


# ---------------------------------------------------------------- 節7
SEC.append({"title": r"不等式の証明",
"base": r"""・$f(x)>g(x)$ を示すには、$F(x)=f(x)-g(x)$ の最小値が正であることを示す。$F'(x)$ の符号がわかりにくければ $F''(x)$ までさかのぼる。<br>
・$F(a)=0$ で、$x>a$ のとき $F'(x)>0$ ならば、$x>a$ のとき $F(x)>0$。<br>
・微分する前に形を整えると楽になる：両辺の対数をとる、$\dfrac ba=t$ のように比でおきかえる、割り算で文字定数を分離する、累乗根をとる など。<br>
・「すべての $x$ で $f(x)\geqq a$」$\iff$「$f(x)$ の最小値 $\geqq a$」（最小値がないときは下限との比較で、等号の扱いに注意）""",
"items": [
 {"lv": 2, "title": r"微分をくり返して示す不等式",
  "q": r"$x>0$ のとき、$e^x>1+x+\dfrac{x^2}{2}$ が成り立つことを証明せよ。",
  "hint": r"$f(x)=e^x-\left(1+x+\dfrac{x^2}2\right)$ とおく。$f'(x)$ の符号がすぐにはわからないので、$f''(x)$ の符号から順にさかのぼる。",
  "sol": r"$f(x)=e^x-1-x-\dfrac{x^2}2$ とおくと　$f'(x)=e^x-1-x$，$f''(x)=e^x-1$<br>"
         r"$x>0$ のとき $f''(x)>0$ だから、$f'(x)$ は $x\geqq0$ で増加し、$f'(0)=0$ より $x>0$ のとき $f'(x)>0$。<br>"
         r"よって $f(x)$ は $x\geqq0$ で増加し、$f(0)=0$ より $x>0$ のとき $f(x)>0$。<br>"
         r"すなわち　$e^x>1+x+\dfrac{x^2}2$　$\blacksquare$",
  "note": r"同じ方法と数学的帰納法で、$x>0$ のとき $e^x>1+x+\dfrac{x^2}{2!}+\cdots+\dfrac{x^n}{n!}$ が示せる。特に $e^x>\dfrac{x^{n+1}}{(n+1)!}$ から $0<\dfrac{x^n}{e^x}<\dfrac{(n+1)!}{x}$ となり、$\displaystyle\lim_{x\to\infty}\frac{x^n}{e^x}=0$ が導ける。",
  "ex": r"$x>0$ のとき、$\log(1+x)>x-\dfrac{x^2}2$ が成り立つことを証明せよ。",
  "exa": r"$f(x)=\log(1+x)-x+\dfrac{x^2}2$ とおくと $f'(x)=\dfrac{x^2}{1+x}>0$（$x>0$），$f(0)=0$ より $x>0$ で $f(x)>0$。"},
 {"lv": 2, "title": r"つねに成り立つ不等式（定数の分離）",
  "q": r"すべての正の数 $x$ に対して $\log x\leqq a\sqrt x$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$\sqrt x>0$ で両辺を割ると $\dfrac{\log x}{\sqrt x}\leqq a$。左辺の最大値以上であればよい。",
  "sol": r"$x>0$ のとき、不等式は $\dfrac{\log x}{\sqrt x}\leqq a$ と同値。$h(x)=\dfrac{\log x}{\sqrt x}$ とおくと<br>"
         r"$h'(x)=\dfrac{\frac1x\cdot\sqrt x-\log x\cdot\frac{1}{2\sqrt x}}{x}=\dfrac{2-\log x}{2x\sqrt x}$<br>"
         r"$0<x<e^2$ で $h'(x)>0$，$x>e^2$ で $h'(x)<0$ だから、$h(x)$ は $x=e^2$ で最大値 $h(e^2)=\dfrac{2}{e}$ をとる。<br>"
         r"すべての $x>0$ で $h(x)\leqq a$ となる条件は　$\boldsymbol{a\geqq\dfrac2e}$",
  "note": r"$a=\dfrac2e$ のとき、曲線 $y=\log x$ と $y=\dfrac2e\sqrt x$ は点 $(e^2,\ 2)$ で接する。割る数の符号（ここでは $\sqrt x>0$）を確認してから分離すること。",
  "ex": r"すべての正の数 $x$ に対して $e^x\geqq ax^3$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$a\leqq\dfrac{e^3}{27}$"},
 {"lv": 3, "title": r"関数の単調性を利用した大小比較",
  "q": r"$e^\pi$ と $\pi^e$ の大小を比較せよ。",
  "hint": r"両辺の自然対数は $\pi$ と $e\log\pi$。これらを $e\pi$ で割ると $\dfrac{\log e}{e}$ と $\dfrac{\log\pi}{\pi}$ の比較になり、関数 $\dfrac{\log x}{x}$ の増減に帰着する。",
  "sol": r"$f(x)=\dfrac{\log x}{x}$（$x>0$）とおくと $f'(x)=\dfrac{1-\log x}{x^2}$ で、$x>e$ のとき $f'(x)<0$。よって $f(x)$ は $x\geqq e$ で減少する。<br>"
         r"$e<\pi$ だから $f(e)>f(\pi)$，すなわち $\dfrac1e>\dfrac{\log\pi}{\pi}$。両辺に $e\pi\ (>0)$ を掛けて<br>"
         r"$\pi>e\log\pi$，すなわち $\log e^\pi>\log\pi^e$<br>"
         r"$\log x$ は増加関数だから　$\boldsymbol{e^\pi>\pi^e}$",
  "note": r"実際 $e^\pi=23.14\cdots$，$\pi^e=22.45\cdots$ で非常に近く、数値計算では判定しにくい。一般に $e\leqq a<b$ ならば $a^b>b^a$ である。$a^b$ と $b^a$ の比較は「対数をとって $\dfrac{\log x}{x}$ の比較」が定石。",
  "ex": r"(1) $3^\pi$ と $\pi^3$ の大小を比較せよ。<br>(2) 自然数 $n$ に対して、$\sqrt[n]{n}$ が最大となる $n$ を求めよ。",
  "exa": r"(1) $3^\pi>\pi^3$　(2) $n=3$（$\sqrt2<\sqrt[3]3$ で、$n\geqq3$ では減少）"},
 {"lv": 4, "title": r"端での微分係数に注目する不等式",
  "q": r"$x\geqq0$ を満たすすべての $x$ に対して $e^x\geqq1+x+ax^2$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$f(x)=e^x-1-x-ax^2$ は $f(0)=0$，$f'(0)=0$ を満たすので、$x=0$ のすぐ右での符号は $f''(0)=1-2a$ の符号で決まる。$a>\dfrac12$ では $0$ の近くで $f(x)<0$ となることを示す。",
  "sol": r"$f(x)=e^x-1-x-ax^2$ とおくと　$f(0)=0$，$f'(x)=e^x-1-2ax$，$f'(0)=0$，$f''(x)=e^x-2a$<br>"
         r"(i) $a\leqq\dfrac12$ のとき　$x>0$ で $f''(x)=e^x-2a>1-2a\geqq0$ だから、$f'(x)$ は $x\geqq0$ で増加し $f'(x)\geqq f'(0)=0$。よって $f(x)$ も増加し $f(x)\geqq f(0)=0$ で、不等式は成り立つ。<br>"
         r"(ii) $a>\dfrac12$ のとき　$2a>1$ より $\log2a>0$。$0<x<\log2a$ で $f''(x)<0$ だから、$f'(x)$ はこの区間で減少し $f'(x)<f'(0)=0$。よって $f(x)$ も減少し、$0<x<\log2a$ で $f(x)<f(0)=0$ となって、不等式は成り立たない。<br>"
         r"以上より　$\boldsymbol{a\leqq\dfrac12}$",
  "note": r"定数を分離すると $a\leqq\dfrac{e^x-1-x}{x^2}$（$x>0$）となる。右辺は $x>0$ でつねに $\dfrac12$ より大きく（この節の最初の例題）、$x\to+0$ で $\dfrac12$ に近づく。最小値はないが下限が $\dfrac12$ なので、答は等号を含めて $a\leqq\dfrac12$。分離した関数の極限計算が難しいときは、本解のように端での状況に注目する。",
  "ex": r"$x\geqq0$ を満たすすべての $x$ に対して $\log(1+x)\geqq x-ax^2$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$a\geqq\dfrac12$（$f(x)=\log(1+x)-x+ax^2$ とすると $f'(x)=\dfrac{x(2ax+2a-1)}{1+x}$）"},
 {"lv": 4, "title": r"2変数の不等式（比を1つの文字でおく）",
  "q": r"$0<a<b$ のとき、次の不等式を証明せよ。<br>$\sqrt{ab}<\dfrac{b-a}{\log b-\log a}<\dfrac{a+b}{2}$",
  "hint": r"各辺を $a$ で割り $t=\dfrac ba\ (>1)$ とおくと、$t$ だけの不等式になる。$\log t$ を単独にした形に直してから微分すると、導関数が平方の形にまとまる。",
  "sol": r"$t=\dfrac ba$ とおくと $t>1$，$\log b-\log a=\log t$。各辺を $a\ (>0)$ で割ると、示すべき不等式は<br>"
         r"$\sqrt t<\dfrac{t-1}{\log t}<\dfrac{t+1}{2}$<br>"
         r"$t>1$ で $\log t>0$ だから、これは　$\dfrac{2(t-1)}{t+1}<\log t<\dfrac{t-1}{\sqrt t}$ …(*)　と同値。<br>"
         r"<b>右側</b>　$f(t)=\dfrac{t-1}{\sqrt t}-\log t=\sqrt t-\dfrac1{\sqrt t}-\log t$ とおくと<br>"
         r"$f'(t)=\dfrac1{2\sqrt t}+\dfrac1{2t\sqrt t}-\dfrac1t=\dfrac{t-2\sqrt t+1}{2t\sqrt t}=\dfrac{(\sqrt t-1)^2}{2t\sqrt t}>0$（$t>1$）<br>"
         r"$f(1)=0$ より、$t>1$ で $f(t)>0$。<br>"
         r"<b>左側</b>　$g(t)=\log t-\dfrac{2(t-1)}{t+1}$ とおくと<br>"
         r"$g'(t)=\dfrac1t-\dfrac{4}{(t+1)^2}=\dfrac{(t-1)^2}{t(t+1)^2}>0$（$t>1$）<br>"
         r"$g(1)=0$ より、$t>1$ で $g(t)>0$。<br>"
         r"よって (*) が成り立ち、与えられた不等式が示された。$\blacksquare$",
  "note": r"中辺を $a,\ b$ の<b>対数平均</b>といい、「相乗平均＜対数平均＜相加平均」が成り立つ。平均値の定理で $\dfrac{\log b-\log a}{b-a}=\dfrac1c$（$a<c<b$）と書くと、この $c$ は対数平均そのものであり、不等式は $c$ の位置をさらにくわしく限定している。",
  "ex": r"$x<y$ のとき、$\dfrac{e^y-e^x}{y-x}>e^{\frac{x+y}2}$ を証明せよ。",
  "exa": r"両辺を $e^{\frac{x+y}2}$ で割り $s=\dfrac{y-x}2\ (>0)$ とおくと、$e^s-e^{-s}-2s>0$ を示せばよい（導関数 $e^s+e^{-s}-2>0$）。"},
 {"lv": 5, "title": r"形を整えてから微分する不等式（三角関数）",
  "q": r"$0<x<\dfrac\pi2$ のとき、$\left(\dfrac{\sin x}{x}\right)^3>\cos x$ が成り立つことを証明せよ。",
  "hint": r"$\dfrac{\sin^3x}{x^3}-\cos x$ をそのまま微分しても符号は判定しにくい。両辺の3乗根をとって $x$ を単独にした形 $\dfrac{\sin x}{\sqrt[3]{\cos x}}>x$ に直すと、導関数が $\cos^{\frac23}x$ の式にまとまる。",
  "sol": r"$0<x<\dfrac\pi2$ では $\sin x>0$，$\cos x>0$，$x>0$ だから、不等式は<br>"
         r"$\dfrac{\sin x}{x}>\sqrt[3]{\cos x}$，すなわち　$\dfrac{\sin x}{(\cos x)^{\frac13}}>x$<br>"
         r"と同値である。$f(x)=\sin x\,(\cos x)^{-\frac13}-x$ $\left(0\leqq x<\dfrac\pi2\right)$ とおくと<br>"
         r"$f'(x)=\cos x\,(\cos x)^{-\frac13}+\sin x\cdot\left(-\dfrac13\right)(\cos x)^{-\frac43}\cdot(-\sin x)-1=(\cos x)^{\frac23}+\dfrac{\sin^2x}{3(\cos x)^{\frac43}}-1$<br>"
         r"$u=(\cos x)^{\frac23}$ とおくと、$\cos^2x=u^3$，$\sin^2x=1-u^3$，$(\cos x)^{\frac43}=u^2$ だから<br>"
         r"$f'(x)=u+\dfrac{1-u^3}{3u^2}-1=\dfrac{2u^3-3u^2+1}{3u^2}=\dfrac{(u-1)^2(2u+1)}{3u^2}$<br>"
         r"$0<x<\dfrac\pi2$ では $0<u<1$ だから $f'(x)>0$。$f(0)=0$ なので、$0<x<\dfrac\pi2$ のとき $f(x)>0$。<br>"
         r"よって　$\left(\dfrac{\sin x}{x}\right)^3>\cos x$　$\blacksquare$",
  "note": r"$x\to0$ のとき両辺はともに $1-\dfrac{x^2}{2}+\cdots$ で、差は $\dfrac{x^4}{15}$ 程度しかない。差をそのまま微分すると何回も微分が必要になり、符号の判定も難しい。「比べるものの形を整え、$x$ と比べる形にしてから微分する」のが要点で、$\sin x<x<\tan x$ の証明と同じ発想である。",
  "ex": r"$0<x<\dfrac\pi2$ のとき、$3\sin x<x(2+\cos x)$ が成り立つことを証明せよ。",
  "exa": r"$f(x)=x(2+\cos x)-3\sin x$ とおくと $f'(x)=2-2\cos x-x\sin x=2\sin\dfrac x2\cos\dfrac x2\left(2\tan\dfrac x2-x\right)>0$（$\tan\theta>\theta$ を用いる），$f(0)=0$。"},
 {"lv": 5, "title": r"不等式による評価と極限",
  "q": r"(1) $x>0$ のとき、$x-\dfrac{x^2}2<\log(1+x)<x-\dfrac{x^2}2+\dfrac{x^3}3$ が成り立つことを証明せよ。<br>"
       r"(2) $a_n=\left(1+\dfrac1n\right)^n$（$n=1,\ 2,\ 3,\ \cdots$）とするとき、$\displaystyle\lim_{n\to\infty}n(e-a_n)$ を求めよ。",
  "hint": r"(2) $\log a_n=n\log\left(1+\dfrac1n\right)$ を (1) ではさむと、$a_n$ が $e^{1-\frac1{2n}}$ と $e^{1-\frac1{2n}+\frac1{3n^2}}$ ではさまれる。$e-a_n$ を $e(1-e^{-h})$ の形で評価し、$\displaystyle\lim_{h\to0}\frac{e^h-1}{h}=1$ を使う。",
  "sol": r"(1) $f(x)=\log(1+x)-x+\dfrac{x^2}2$ とおくと $f'(x)=\dfrac1{1+x}-1+x=\dfrac{x^2}{1+x}>0$（$x>0$），$f(0)=0$ より $x>0$ で $f(x)>0$。<br>"
         r"$g(x)=x-\dfrac{x^2}2+\dfrac{x^3}3-\log(1+x)$ とおくと $g'(x)=1-x+x^2-\dfrac1{1+x}=\dfrac{x^3}{1+x}>0$（$x>0$），$g(0)=0$ より $x>0$ で $g(x)>0$。$\blacksquare$<br>"
         r"(2) (1) で $x=\dfrac1n$ とし、各辺に $n$ を掛けると<br>"
         r"$1-\dfrac1{2n}<n\log\left(1+\dfrac1n\right)<1-\dfrac1{2n}+\dfrac1{3n^2}$<br>"
         r"$h_n=\dfrac1{2n}$，$k_n=\dfrac1{2n}-\dfrac1{3n^2}=\dfrac{3n-2}{6n^2}\ (>0)$ とおくと $e^{1-h_n}<a_n<e^{1-k_n}$ だから<br>"
         r"$e\left(1-e^{-k_n}\right)<e-a_n<e\left(1-e^{-h_n}\right)$ …①<br>"
         r"ここで $n\to\infty$ のとき $h_n\to0$，$k_n\to0$ で、$\displaystyle\lim_{h\to0}\frac{e^{h}-1}{h}=1$ より<br>"
         r"$n\left(1-e^{-h_n}\right)=nh_n\cdot\dfrac{e^{-h_n}-1}{-h_n}\to\dfrac12\cdot1=\dfrac12$，$n\left(1-e^{-k_n}\right)=nk_n\cdot\dfrac{e^{-k_n}-1}{-k_n}\to\dfrac12$<br>"
         r"（$nh_n=\dfrac12$，$nk_n=\dfrac12-\dfrac1{3n}\to\dfrac12$）。①の各辺に $n$ を掛け、はさみうちの原理により<br>"
         r"$\displaystyle\lim_{n\to\infty}n(e-a_n)=\boldsymbol{\frac e2}$",
  "note": r"$e-a_n\fallingdotseq\dfrac{e}{2n}$ なので、$a_n$ が $e$ に近づく速さは遅い（$n=1000$ でも $e-a_n=0.00135\cdots$）。(1) の不等式で $x^3$ の項まで用意したのは、$a_n$ を $e^{1-\frac{1}{2n}}$ の精度で両側から押さえるためで、$\log(1+x)<x$ のような粗い評価では極限の値が決まらない。",
  "ex": r"$\displaystyle\lim_{n\to\infty}n\left\{\left(1+\dfrac1n\right)^{n+1}-e\right\}$ を求めよ。",
  "exa": r"$\dfrac e2$"},
]})


def _v7():
    f = exp(x) - 1 - x - x**2 / 2
    assert diff(f, x, 2) == exp(x) - 1 and f.subs(x, 0) == 0 and diff(f, x).subs(x, 0) == 0
    g = log(1 + x) - x + x**2 / 2
    assert simplify(diff(g, x) - x**2 / (1 + x)) == 0
    for _ in range(2000):
        v = random.uniform(1e-3, 30)
        assert math.exp(v) > 1 + v + v * v / 2 and math.log1p(v) > v - v * v / 2
    # 定数の分離
    h = log(x) / sqrt(x)
    assert simplify(diff(h, x) - (2 - log(x)) / (2 * x * sqrt(x))) == 0 and simplify(h.subs(x, E**2) - 2 / E) == 0
    xs = _geo(1e-8, 1e8, 40000)
    assert all(math.log(v) <= 2 / math.e * math.sqrt(v) + 1e-12 for v in xs)
    assert any(math.log(v) > 0.73 * math.sqrt(v) for v in xs)
    assert abs(min(math.exp(v) / v**3 for v in _geo(1e-3, 100, 40000)) - math.e**3 / 27) < 1e-8
    # 大小比較
    assert math.exp(math.pi) > math.pi ** math.e and 3 ** math.pi > math.pi ** 3
    assert abs(math.exp(math.pi) - 23.1407) < 1e-4 and abs(math.pi ** math.e - 22.4592) < 1e-4
    vals = [n ** (1 / n) for n in range(1, 2000)]
    assert vals.index(max(vals)) + 1 == 3
    # 端での微分係数
    xs = _grid(0, 20, 40000)
    assert all(math.exp(v) - 1 - v - 0.5 * v * v >= -1e-12 for v in xs)
    for A in [0.51, 0.6, 1, 3]:
        assert math.exp(1e-3) - 1 - 1e-3 - A * 1e-6 < 0 or min(math.exp(v) - 1 - v - A * v * v for v in xs) < 0
        v = math.log(2 * A) / 2
        assert math.exp(v) - 1 - v - A * v * v < 0
    assert all(math.log1p(v) - v + 0.5 * v * v >= -1e-12 for v in xs)
    for A in [0.49, 0.4, 0, -1]:
        assert min(math.log1p(v) - v + A * v * v for v in _grid(0, 2, 4000)) < 0
    A_ = symbols("A")
    assert simplify(diff(log(1 + x) - x + A_ * x**2, x) - x * (2 * A_ * x + 2 * A_ - 1) / (1 + x)) == 0
    # 対数平均
    tp = symbols("tp", positive=True)
    assert simplify(diff(sqrt(tp) - 1 / sqrt(tp) - log(tp), tp) - (sqrt(tp) - 1)**2 / (2 * tp * sqrt(tp))) == 0
    assert simplify(diff(log(tp) - 2 * (tp - 1) / (tp + 1), tp) - (tp - 1)**2 / (tp * (tp + 1)**2)) == 0
    for _ in range(3000):
        A = random.uniform(0.01, 10)
        B = A * random.uniform(1.0001, 50)
        Lm = (B - A) / (math.log(B) - math.log(A))
        assert math.sqrt(A * B) < Lm < (A + B) / 2
        X = random.uniform(-5, 5)
        Y = X + random.uniform(1e-3, 6)
        assert (math.exp(Y) - math.exp(X)) / (Y - X) > math.exp((X + Y) / 2)
    # (sin x / x)^3 > cos x
    for v in _grid(1e-3, math.pi / 2 - 1e-6, 20000):
        assert (math.sin(v) / v) ** 3 > math.cos(v)
        assert 3 * math.sin(v) < v * (2 + math.cos(v))
    assert expand((u - 1)**2 * (2 * u + 1) - (2 * u**3 - 3 * u**2 + 1)) == 0
    xp = symbols("xp", positive=True)
    F = sin(xp) * cos(xp)**Rational(-1, 3) - xp
    U = cos(xp)**Rational(2, 3)
    assert _z(diff(F, xp) - (U + (1 - U**3) / (3 * U**2) - 1), 0.05, 1.5)
    sr = series((sin(x) / x)**3 - cos(x), x, 0, 6).removeO()
    assert simplify(sr - x**4 / 15) == 0
    G = x * (2 + cos(x)) - 3 * sin(x)
    assert _z(diff(G, x) - 2 * sin(x / 2) * cos(x / 2) * (2 * tan(x / 2) - x))
    # 評価と極限
    g2 = x - x**2 / 2 + x**3 / 3 - log(1 + x)
    assert simplify(diff(g2, x) - x**3 / (1 + x)) == 0
    for _ in range(2000):
        v = random.uniform(1e-3, 20)
        assert v - v * v / 2 < math.log1p(v) < v - v * v / 2 + v**3 / 3
    import mpmath as mp
    mp.mp.dps = 50
    for n in [10**4, 10**6, 10**8]:
        an = (1 + mp.mpf(1) / n) ** n
        hn, kn = mp.mpf(1) / (2 * n), mp.mpf(1) / (2 * n) - mp.mpf(1) / (3 * n * n)
        assert kn > 0 and mp.e * (1 - mp.e**(-kn)) < mp.e - an < mp.e * (1 - mp.e**(-hn))
        assert abs(n * (mp.e - an) - mp.e / 2) < 3 / mp.mpf(n)
        bn = (1 + mp.mpf(1) / n) ** (n + 1)
        assert abs(n * (bn - mp.e) - mp.e / 2) < 3 / mp.mpf(n)
    n = 1000
    assert abs((math.e - (1 + 1 / n) ** n) - 0.001359) < 2e-6


# ---------------------------------------------------------------- 節8 の図
def _fig83():
    k = (220 - 24) / 7.1
    g = _G(220, round(24 + 2.9 * k), (-0.3, 6.8), (-0.3, 2.6))
    g.axes(o="O")
    g.pcurve(lambda v: v - math.sin(v), lambda v: 1 - math.cos(v), 0, 2 * math.pi)
    t1 = math.pi / 2
    g.pcurve(lambda v: t1 + math.cos(v), lambda v: 1 + math.sin(v), 0, 2 * math.pi, col=CG, w=0.8, dash=DASH)
    P1 = (t1 - 1, 1)
    g.pt(*P1, col=C2)
    g.arrow(P1, (P1[0] + 0.7, P1[1] + 0.7))
    P2 = (math.pi, 2)
    g.pt(*P2, col=C2)
    g.arrow(P2, (P2[0] + 1.4, 2))
    g.txt(math.pi, 2, "t=π", dy=-5, size=9.5)
    g.txt(P1[0], 1, "t=π/2", dx=5, dy=4, anc="start", size=9.5)
    g.xtick(2 * math.pi, "2π", it=False)
    return g.svg()


# ---------------------------------------------------------------- 節8
SEC.append({"title": r"速度・加速度と近似式",
"base": r"""・数直線上の運動 $x=f(t)$：速度 $v=\dfrac{dx}{dt}$，加速度 $\alpha=\dfrac{dv}{dt}=\dfrac{d^2x}{dt^2}$，速さ $|v|$<br>
・平面上の運動 $(x,\ y)=(x(t),\ y(t))$：速度 $\vec v=\left(\dfrac{dx}{dt},\ \dfrac{dy}{dt}\right)$，速さ $|\vec v|=\sqrt{\left(\dfrac{dx}{dt}\right)^2+\left(\dfrac{dy}{dt}\right)^2}$，加速度 $\vec\alpha=\left(\dfrac{d^2x}{dt^2},\ \dfrac{d^2y}{dt^2}\right)$<br>
・1次の近似式：$|h|$ が十分小さいとき $f(a+h)\fallingdotseq f(a)+f'(a)h$。特に $x\fallingdotseq0$ のとき $f(x)\fallingdotseq f(0)+f'(0)x$<br>
　例：$(1+x)^p\fallingdotseq1+px$，$\sin x\fallingdotseq x$，$e^x\fallingdotseq1+x$，$\log(1+x)\fallingdotseq x$<br>
・時刻とともに変化する量どうしの関係式を $t$ で微分すると、変化の速さの関係が得られる（合成関数の微分）。""",
"items": [
 {"lv": 1, "title": r"直線上の運動（単振動）",
  "q": r"数直線上を運動する点 $\mathrm P$ の時刻 $t$ における座標が $x=3\sin\left(2t+\dfrac\pi6\right)$ であるとき、時刻 $t$ における $\mathrm P$ の速度 $v$ と加速度 $\alpha$ を求めよ。また、$\alpha=-4x$ が成り立つことを示し、$t=\dfrac\pi6$ における速度と加速度を求めよ。",
  "hint": r"$x$ を $t$ で微分して $v$，さらに微分して $\alpha$。合成関数の微分で、内側の $2t+\dfrac\pi6$ の微分 $2$ が掛かることに注意。",
  "sol": r"$v=\dfrac{dx}{dt}=\boldsymbol{6\cos\left(2t+\dfrac\pi6\right)}$，$\alpha=\dfrac{dv}{dt}=\boldsymbol{-12\sin\left(2t+\dfrac\pi6\right)}$<br>"
         r"$\alpha=-4\cdot3\sin\left(2t+\dfrac\pi6\right)=-4x$　$\blacksquare$<br>"
         r"$t=\dfrac\pi6$ のとき $2t+\dfrac\pi6=\dfrac\pi2$ だから　速度 $v=\boldsymbol{0}$，加速度 $\alpha=\boldsymbol{-12}$",
  "note": r"$\alpha=-\omega^2x$ を満たす運動を単振動という（ここでは $\omega=2$）。$v=0$ となる瞬間に $\mathrm P$ は振動の端 $x=3$ にあり、加速度の大きさが最大になる。",
  "ex": r"数直線上を運動する点 $\mathrm P$ の時刻 $t$ における座標が $x=2\cos\left(3t-\dfrac\pi4\right)$ であるとき、$t=\dfrac\pi{12}$ における $\mathrm P$ の速度と加速度を求めよ。",
  "exa": r"速度 $0$，加速度 $-18$"},
 {"lv": 1, "title": r"1次の近似式と近似値",
  "q": r"(1) $x$ が $0$ に十分近いとき、$\sqrt[3]{1+x}$ の1次の近似式を求めよ。<br>(2) (1) を用いて、$\sqrt[3]{1003}$ の近似値を小数第2位まで求めよ。",
  "hint": r"$f(x)\fallingdotseq f(0)+f'(0)x$ を使う。(2) は $1003=1000\times1.003$ と変形し、$0$ に近い数 $0.003$ が現れるようにする。",
  "sol": r"(1) $f(x)=(1+x)^{\frac13}$ とおくと $f'(x)=\dfrac13(1+x)^{-\frac23}$ で、$f(0)=1$，$f'(0)=\dfrac13$。よって<br>"
         r"$\boldsymbol{\sqrt[3]{1+x}\fallingdotseq1+\dfrac x3}$<br>"
         r"(2) $\sqrt[3]{1003}=\sqrt[3]{1000\times1.003}=10\sqrt[3]{1+0.003}\fallingdotseq10\left(1+\dfrac{0.003}{3}\right)=\boldsymbol{10.01}$",
  "note": r"実際の値は $\sqrt[3]{1003}=10.00999\cdots$ で、よく一致する。誤差はおよそ $\dfrac{f''(0)}{2}x^2$ の大きさで、$x$ が小さいほど近似がよい。$\sqrt[3]{1003}$ を $\sqrt[3]{1+1002}$ として近似するのは無意味（$1002$ は $0$ に近くない）。",
  "ex": r"1次の近似式を用いて、$\sin31^\circ$ の近似値を小数第3位まで求めよ。ただし、$\pi=3.14$，$\sqrt3=1.73$ とする。",
  "exa": r"$0.515$（$\sin\left(\dfrac\pi6+h\right)\fallingdotseq\dfrac12+\dfrac{\sqrt3}2h$，$h=\dfrac{\pi}{180}$）"},
 {"lv": 2, "title": r"平面上の運動（速さと加速度）",
  "q": _fig83() +
       r"座標平面上を運動する点 $\mathrm P$ の時刻 $t$ における座標が $x=t-\sin t$，$y=1-\cos t$ で与えられている。<br>"
       r"(1) 時刻 $t$ における $\mathrm P$ の速さを求めよ。<br>"
       r"(2) $0\leqq t\leqq2\pi$ において、速さが最大となる時刻と、そのときの $\mathrm P$ の座標を求めよ。<br>"
       r"(3) 加速度の大きさは一定であることを示せ。",
  "hint": r"速度ベクトル $\left(\dfrac{dx}{dt},\ \dfrac{dy}{dt}\right)$ の大きさが速さ。半角の公式 $1-\cos t=2\sin^2\dfrac t2$ を使うと根号がはずれる。",
  "sol": r"(1) $\dfrac{dx}{dt}=1-\cos t$，$\dfrac{dy}{dt}=\sin t$ より、速さは<br>"
         r"$\sqrt{(1-\cos t)^2+\sin^2t}=\sqrt{2-2\cos t}=\sqrt{4\sin^2\dfrac t2}=\boldsymbol{2\left|\sin\dfrac t2\right|}$<br>"
         r"(2) $0\leqq t\leqq2\pi$ では $0\leqq\dfrac t2\leqq\pi$ だから、速さは $2\sin\dfrac t2$ で、最大値 $2$ をとるのは $\dfrac t2=\dfrac\pi2$，すなわち $\boldsymbol{t=\pi}$ のとき。このとき $\mathrm P\boldsymbol{(\pi,\ 2)}$。<br>"
         r"(3) $\dfrac{d^2x}{dt^2}=\sin t$，$\dfrac{d^2y}{dt^2}=\cos t$ より、加速度の大きさは $\sqrt{\sin^2t+\cos^2t}=1$（一定）　$\blacksquare$",
  "note": r"$\mathrm P$ の描く曲線はサイクロイドで、半径 $1$ の円が $x$ 軸上をすべらずに転がるときの円周上の点の軌跡（図の破線は $t=\dfrac\pi2$ のときの円）。最高点で速さは $2$（円の中心の速さ $1$ の2倍）、$x$ 軸に触れる瞬間（$t=0,\ 2\pi$）に速さは $0$ になる。",
  "ex": r"座標平面上を運動する点 $\mathrm P$ の時刻 $t$ における座標が $x=e^t\cos t$，$y=e^t\sin t$ であるとき、時刻 $t$ における $\mathrm P$ の速さと加速度の大きさを求めよ。",
  "exa": r"速さ $\sqrt2e^t$，加速度の大きさ $2e^t$"},
 {"lv": 2, "title": r"変化の速さ（水面の上昇）",
  "q": r"底面の半径が $4\,\mathrm{cm}$，深さが $8\,\mathrm{cm}$ の直円錐形の容器を、頂点を下にして軸が鉛直になるように置き、毎秒 $2\pi\,\mathrm{cm^3}$ の割合で水を注ぐ。水の深さが $4\,\mathrm{cm}$ になった瞬間における、水面の上昇する速さと、水面の面積が増加する速さを求めよ。",
  "hint": r"水の深さ $h$ を時刻 $t$ の関数とみて、体積 $V$ と $h$ の関係式を $t$ で微分する（合成関数の微分）。$\dfrac{dV}{dt}=2\pi$ がわかっているので $\dfrac{dh}{dt}$ が求まる。",
  "sol": r"注ぎ始めてから $t$ 秒後の水の深さを $h$，水面の半径を $r$，水の体積を $V$，水面の面積を $S$ とする。相似より $r=\dfrac h2$ だから<br>"
         r"$V=\dfrac13\pi\left(\dfrac h2\right)^2h=\dfrac{\pi}{12}h^3$，$S=\pi r^2=\dfrac\pi4h^2$<br>"
         r"$V$ を $t$ で微分すると $\dfrac{dV}{dt}=\dfrac\pi4h^2\cdot\dfrac{dh}{dt}$。$\dfrac{dV}{dt}=2\pi$ だから $\dfrac{dh}{dt}=\dfrac{8}{h^2}$。<br>"
         r"また $\dfrac{dS}{dt}=\dfrac\pi2h\cdot\dfrac{dh}{dt}=\dfrac{4\pi}{h}$。<br>"
         r"$h=4$ のとき　$\dfrac{dh}{dt}=\dfrac12$，$\dfrac{dS}{dt}=\pi$<br>"
         r"答　水面の上昇する速さ $\boldsymbol{\dfrac12\,\mathrm{cm/s}}$，水面の面積の増加する速さ $\boldsymbol{\pi\,\mathrm{cm^2/s}}$",
  "note": r"$\dfrac{dV}{dt}=S\cdot\dfrac{dh}{dt}$（体積の増える速さ＝水面の面積×水面の上がる速さ）という関係になっている。水面が高くなるほど $S$ が大きくなるので、上昇は遅くなる。",
  "ex": r"長さ $5\,\mathrm m$ のはしごが鉛直な壁に立てかけてある。はしごの下端を毎秒 $0.5\,\mathrm m$ の速さで壁から水平に遠ざけるとき、下端が壁から $3\,\mathrm m$ の位置にある瞬間に、上端が下がる速さを求めよ。",
  "exa": r"毎秒 $\dfrac38\,\mathrm m$"},
]})


def _v8():
    X = 3 * sin(2 * t + pi / 6)
    v, al = diff(X, t), diff(X, t, 2)
    assert simplify(v - 6 * cos(2 * t + pi / 6)) == 0 and simplify(al + 12 * sin(2 * t + pi / 6)) == 0
    assert simplify(al + 4 * X) == 0 and v.subs(t, pi / 6) == 0 and al.subs(t, pi / 6) == -12
    X = 2 * cos(3 * t - pi / 4)
    assert simplify(diff(X, t).subs(t, pi / 12)) == 0 and simplify(diff(X, t, 2).subs(t, pi / 12)) == -18
    # 近似式
    f = (1 + x)**Rational(1, 3)
    assert f.subs(x, 0) == 1 and diff(f, x).subs(x, 0) == Rational(1, 3)
    approx = 10 * (1 + 0.003 / 3)
    assert abs(approx - 10.01) < 1e-12 and round(1003 ** (1 / 3), 2) == 10.01
    s31 = 0.5 + 1.73 / 2 * (3.14 / 180)
    assert abs(s31 - 0.51509) < 1e-5 and round(s31, 3) == 0.515 and round(math.sin(math.radians(31)), 3) == 0.515
    # サイクロイド
    X, Y = t - sin(t), 1 - cos(t)
    sp2 = diff(X, t)**2 + diff(Y, t)**2
    assert simplify(sp2 - 4 * sin(t / 2)**2) == 0
    sp = [2 * abs(math.sin(w / 2)) for w in _grid(0, 2 * math.pi, 4000)]
    assert abs(max(sp) - 2) < 1e-12 and abs(sp.index(max(sp)) * 2 * math.pi / 4000 - math.pi) < 1e-9
    assert X.subs(t, pi) == pi and Y.subs(t, pi) == 2
    assert simplify(diff(X, t, 2)**2 + diff(Y, t, 2)**2) == 1
    X, Y = exp(t) * cos(t), exp(t) * sin(t)
    assert simplify(diff(X, t)**2 + diff(Y, t)**2 - 2 * exp(2 * t)) == 0
    assert simplify(diff(X, t, 2)**2 + diff(Y, t, 2)**2 - 4 * exp(2 * t)) == 0
    # 水面の上昇
    h = symbols("h", positive=True)
    V = pi / 12 * h**3
    dh = 2 * pi / diff(V, h)
    assert simplify(dh - 8 / h**2) == 0 and dh.subs(h, 4) == Rational(1, 2)
    S_ = pi / 4 * h**2
    assert simplify(diff(S_, h) * dh - 4 * pi / h) == 0 and simplify((diff(S_, h) * dh).subs(h, 4) - pi) == 0
    assert simplify(diff(V, h) - S_) == 0
    # はしご：x^2 + y^2 = 25, x = 3, dx/dt = 1/2
    xv, yv = 3, 4
    dy = -Rational(xv, yv) * Rational(1, 2)
    assert dy == Rational(-3, 8)


# ==== END SECTIONS ====
CH = {"no": 24, "sections": SEC}


def verify():
    for f in [_v1, _v2, _v3, _v4, _v5, _v6, _v7, _v8]:
        f()
    items = [it for s_ in SEC for it in s_["items"]]
    lv = [it["lv"] for it in items]
    cnt = {k: lv.count(k) for k in range(1, 6)}
    assert 4 <= len(SEC) <= 9 and 37 <= len(items) <= 43, len(items)
    assert cnt[5] >= 5 and 7 <= cnt[1] <= 10 and 8 <= cnt[2] <= 12 and 8 <= cnt[3] <= 12 and 5 <= cnt[4] <= 9, cnt
    for s_ in SEC:
        ls = [it["lv"] for it in s_["items"]]
        assert ls == sorted(ls), s_["title"]
        for it in s_["items"]:
            for key in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(key), (it.get("title"), key)
            for key in ("title", "q", "hint", "sol", "note", "ex", "exa"):
                assert "$$" not in it.get(key, "") and it.get(key, "").count("$") % 2 == 0, (it["title"], key)
            if it["lv"] >= 3:
                assert it.get("note"), it["title"]
