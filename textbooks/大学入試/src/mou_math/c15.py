"""第15章 積分法（数学II）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。
扱う関数は整式（と、その絶対値）だけ。図の座標はすべて Python で計算する。"""
import math
import random
from fractions import Fraction as Fr
from sympy import (symbols, Rational, sqrt, expand, factor, diff, integrate, simplify, solve, Poly,
                   Abs, nsimplify, cbrt, pi, sin, Piecewise, S, lambdify, N)

SEC = []

# ---------------------------------------------------------------- 図の道具
C1, C2, CG, CF = "#16367a", "#d9701e", "#888888", "#c9daf3"
DASH = ' stroke-dasharray="3,2"'


class _G:
    """数学座標で描いて SVG 文字列にする小さな道具。eq=True なら縦横の縮尺をそろえる。"""

    def __init__(s, W, H, xr, yr, m=10, eq=False):
        s.x0, s.x1 = xr
        s.y0, s.y1 = yr
        s.m = m
        s.sx = (W - 2 * m) / (s.x1 - s.x0)
        s.sy = (H - 2 * m) / (s.y1 - s.y0)
        if eq:
            k = min(s.sx, s.sy)
            s.sx = s.sy = k
            W = round(2 * m + (s.x1 - s.x0) * k)
            H = round(2 * m + (s.y1 - s.y0) * k)
        s.W, s.H = W, H
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

    def curve(s, f, a, b, col=C1, w=1.4, dash="", n=240):
        """y=f(x)（a≦x≦b）。枠の上下からはみ出す部分は切る。"""
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
            if len(sg) > 1:
                s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{dash} points="'
                           + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in sg) + '"/>')

    def pcurve(s, fx, fy, t0, t1, col=C1, w=1.4, dash="", n=240):
        """媒介変数で表した曲線（円など）。"""
        pts = [(fx(t0 + (t1 - t0) * i / n), fy(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]
        s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{dash} points="'
                   + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts) + '"/>')

    def seg(s, p, q, col=CG, w=0.8, dash=DASH):
        s.o.append(f'<line x1="{s.X(p[0])}" y1="{s.Y(p[1])}" x2="{s.X(q[0])}" y2="{s.Y(q[1])}" stroke="{col}" stroke-width="{w}"{dash}/>')

    def pt(s, x, y, col=C1, r=1.8):
        s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="{col}"/>')

    def txt(s, x, y, t, dx=0, dy=0, anc="middle", it=False, size=10, col="#222"):
        st = ' font-style="italic" font-family="serif"' if it else ""
        s.o.append(f'<text x="{round(s.X(x) + dx, 1)}" y="{round(s.Y(y) + dy, 1)}" text-anchor="{anc}" font-size="{size}" fill="{col}"{st}>{t}</text>')

    def band(s, lo, hi, a, b, n=120, fill=CF):
        """a≦x≦b で lo(x)≦y≦hi(x) の部分を塗る。"""
        xs = [a + (b - a) * i / n for i in range(n + 1)]
        P = [(x, hi(x)) for x in xs] + [(x, lo(x)) for x in reversed(xs)]
        s.o.append('<polygon points="' + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in P)
                   + f'" fill="{fill}" fill-opacity="0.9" stroke="none"/>')

    def xtick(s, x, t, dy=11):
        s.o.append(f'<line x1="{s.X(x)}" y1="{s.Y(0) - 2}" x2="{s.X(x)}" y2="{s.Y(0) + 2}" stroke="#333" stroke-width="0.8"/>')
        s.txt(x, 0, t, dy=dy, size=10)

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" font-size="10">'
                + "".join(s.o) + "</svg>")


x, t, a, b, c, k, m = symbols("x t a b c k m", real=True)


def _eq(u, v):
    return simplify(u - v) == 0


# ---------------------------------------------------------------- 節1
SEC.append({"title": "不定積分と定積分の計算",
"base": r"""・$\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+C$（$n=0,\ 1,\ 2,\ \cdots$，$C$ は積分定数），$\displaystyle\int(x+p)^n\,dx=\frac{(x+p)^{n+1}}{n+1}+C$<br>
・$F'(x)=f(x)$ のとき　$\displaystyle\int_a^b f(x)\,dx=\Big[F(x)\Big]_a^b=F(b)-F(a)$<br>
・$\displaystyle\int_a^b f(x)\,dx+\int_b^c f(x)\,dx=\int_a^c f(x)\,dx$，$\displaystyle\int_b^a f(x)\,dx=-\int_a^b f(x)\,dx$<br>
・$\displaystyle\int_{-a}^{a}x^{2n}\,dx=2\int_0^a x^{2n}\,dx$，$\displaystyle\int_{-a}^{a}x^{2n+1}\,dx=0$（$n=0,\ 1,\ 2,\ \cdots$）<br>
・$\displaystyle\int_\alpha^\beta(x-\alpha)(x-\beta)\,dx=-\frac{(\beta-\alpha)^3}{6}$""",
"items": [
 {"lv": 1, "title": "不定積分の計算",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int(3x^2-4x+5)\,dx$　　(2) $\displaystyle\int(2x+1)(x-3)\,dx$　　(3) $\displaystyle\int(x+1)^2\,dx-\int(x-1)^2\,dx$",
  "hint": r"積の形は展開して $x^n$ の和にしてから、項ごとに公式を使う。(3) は2つの不定積分を1つにまとめてから計算すると楽。",
  "sol": r"以下、$C$ は積分定数とする。<br>"
         r"(1) $\displaystyle\int(3x^2-4x+5)\,dx=3\cdot\frac{x^3}{3}-4\cdot\frac{x^2}{2}+5x+C=\boldsymbol{x^3-2x^2+5x+C}$<br>"
         r"(2) $(2x+1)(x-3)=2x^2-5x-3$ より　$\displaystyle\int(2x^2-5x-3)\,dx=\boldsymbol{\frac23x^3-\frac52x^2-3x+C}$<br>"
         r"(3) $(x+1)^2-(x-1)^2=4x$ より　与式 $\displaystyle=\int4x\,dx=\boldsymbol{2x^2+C}$",
  "note": r"不定積分は「微分すると被積分関数に戻る」ことで検算できる。(3) では2つの積分定数の差をまとめて1つの $C$ で表している。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int(6x^2+2x-3)\,dx$　　(2) $\displaystyle\int(x-2)(3x+1)\,dx$　　(3) $\displaystyle\int(2x+1)^2\,dx+\int(2x-1)^2\,dx$",
  "exa": r"（$C$ は積分定数）(1) $2x^3+x^2-3x+C$　(2) $x^3-\dfrac52x^2-2x+C$　(3) $\dfrac83x^3+2x+C$"},
 {"lv": 1, "title": "導関数（接線の傾き）から関数を決定する",
  "q": r"(1) $f'(x)=6x^2-2x+1$，$f(1)=3$ を満たす関数 $f(x)$ を求めよ。<br>"
       r"(2) 曲線 $y=g(x)$ 上の各点 $(x,\ g(x))$ における接線の傾きが $3x^2-4x$ で、この曲線が点 $(2,\ 1)$ を通るとき、$g(x)$ を求めよ。",
  "hint": r"$f(x)=\int f'(x)\,dx$ で、積分定数 $C$ を含む形まで決まる。残りの $C$ を、与えられた1点の条件で決める。",
  "sol": r"(1) $f(x)=\displaystyle\int(6x^2-2x+1)\,dx=2x^3-x^2+x+C$（$C$ は定数）。<br>"
         r"$f(1)=2-1+1+C=2+C$ で、これが $3$ に等しいから $C=1$。よって　$\boldsymbol{f(x)=2x^3-x^2+x+1}$<br>"
         r"(2) 接線の傾きは $g'(x)$ だから $g'(x)=3x^2-4x$。よって $g(x)=x^3-2x^2+C$（$C$ は定数）。<br>"
         r"曲線が点 $(2,\ 1)$ を通るから $g(2)=8-8+C=1$，$C=1$。よって　$\boldsymbol{g(x)=x^3-2x^2+1}$",
  "note": r"導関数だけでは関数は「定数の差」を除いてしか決まらない。条件が1つ与えられて初めて1つに決まる。",
  "ex": r"(1) $f'(x)=-3x^2+4x+2$，$f(-1)=0$ を満たす関数 $f(x)$ を求めよ。<br>(2) 曲線 $y=g(x)$ 上の各点 $(x,\ g(x))$ における接線の傾きが $6x-5$ で、この曲線が点 $(1,\ 2)$ を通るとき、$g(x)$ を求めよ。",
  "exa": r"(1) $f(x)=-x^3+2x^2+2x-1$　(2) $g(x)=3x^2-5x+4$"},
 {"lv": 1, "title": "定積分の計算と区間の性質",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-1}^{2}(3x^2-2x+1)\,dx$　　(2) $\displaystyle\int_{-1}^{1}(x^2+x)\,dx+\int_{1}^{2}(x^2+x)\,dx$<br>(3) $\displaystyle\int_0^2(x^2-3x)\,dx-\int_3^2(x^2-3x)\,dx$",
  "hint": r"(2)(3) は被積分関数が同じなので、区間をつなげて1つの定積分にまとめる。(3) は $-\int_3^2=\int_2^3$ と直してからつなぐ。",
  "sol": r"(1) $\Big[x^3-x^2+x\Big]_{-1}^{2}=(8-4+2)-(-1-1-1)=6+3=\boldsymbol{9}$<br>"
         r"(2) 与式 $\displaystyle=\int_{-1}^{2}(x^2+x)\,dx=\Big[\frac{x^3}3+\frac{x^2}2\Big]_{-1}^{2}=\Big(\frac83+2\Big)-\Big(-\frac13+\frac12\Big)=\frac{14}3-\frac16=\boldsymbol{\frac92}$<br>"
         r"(3) $\displaystyle-\int_3^2(x^2-3x)\,dx=\int_2^3(x^2-3x)\,dx$ だから　与式 $\displaystyle=\int_0^3(x^2-3x)\,dx=\Big[\frac{x^3}3-\frac32x^2\Big]_0^3=9-\frac{27}2=\boldsymbol{-\frac92}$",
  "note": r"定積分 $\int_a^b f(x)\,dx$ は $a>b$ のときも同じ式 $F(b)-F(a)$ で定める。そのため区間の加法性は $a,\ b,\ c$ の大小に関係なく成り立つ。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-2}^{1}(x^2+4x-1)\,dx$　　(2) $\displaystyle\int_0^2(2x^2-x)\,dx+\int_2^3(2x^2-x)\,dx$",
  "exa": r"(1) $-6$　(2) $\dfrac{27}{2}$"},
 {"lv": 1, "title": "偶関数・奇関数の定積分",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-2}^{2}(x^3+3x^2-5x+1)\,dx$　　(2) $\displaystyle\int_{-1}^{1}(x+1)^3\,dx$",
  "hint": r"積分区間が $-a$ から $a$ までのときは、奇数次の項の積分は $0$、偶数次の項（定数項を含む）は $2\int_0^a$ にできる。",
  "sol": r"(1) $x^3,\ -5x$ は奇数次なので積分は $0$。よって<br>"
         r"　与式 $\displaystyle=2\int_0^2(3x^2+1)\,dx=2\Big[x^3+x\Big]_0^2=2\cdot10=\boldsymbol{20}$<br>"
         r"(2) $(x+1)^3=x^3+3x^2+3x+1$ のうち $x^3,\ 3x$ の積分は $0$ だから<br>"
         r"　与式 $\displaystyle=2\int_0^1(3x^2+1)\,dx=2\Big[x^3+x\Big]_0^1=\boldsymbol{4}$",
  "note": r"(2) は $\displaystyle\int(x+1)^3dx=\frac{(x+1)^4}{4}+C$ を使って $\Big[\dfrac{(x+1)^4}{4}\Big]_{-1}^{1}=\dfrac{16}{4}=4$ としてもよい。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-3}^{3}(2x^3-x^2+4x-3)\,dx$　　(2) $\displaystyle\int_{-2}^{2}(x-1)^2\,dx$",
  "exa": r"(1) $-36$　(2) $\dfrac{28}{3}$"},
 {"lv": 2, "title": r"$\frac16$ 公式の証明と利用",
  "q": r"(1) 等式 $\displaystyle\int_\alpha^\beta(x-\alpha)(x-\beta)\,dx=-\frac{(\beta-\alpha)^3}{6}$ を証明せよ。<br>"
       r"(2) $\displaystyle\int_{1-\sqrt2}^{1+\sqrt2}(x^2-2x-1)\,dx$ を求めよ。",
  "hint": r"(1) $x-\beta=(x-\alpha)-(\beta-\alpha)$ と変形すると、$(x-\alpha)^n$ の積分の公式がそのまま使える。(2) 積分区間の両端が $x^2-2x-1=0$ の2つの解であることに注目する。",
  "sol": r"(1) $(x-\alpha)(x-\beta)=(x-\alpha)\{(x-\alpha)-(\beta-\alpha)\}=(x-\alpha)^2-(\beta-\alpha)(x-\alpha)$ より<br>"
         r"$\displaystyle\int_\alpha^\beta(x-\alpha)(x-\beta)\,dx=\Big[\frac{(x-\alpha)^3}{3}-(\beta-\alpha)\cdot\frac{(x-\alpha)^2}{2}\Big]_\alpha^\beta=\frac{(\beta-\alpha)^3}3-\frac{(\beta-\alpha)^3}2=-\frac{(\beta-\alpha)^3}6$　■<br>"
         r"(2) $x^2-2x-1=0$ の解は $x=1\pm\sqrt2$ なので、$\alpha=1-\sqrt2,\ \beta=1+\sqrt2$ とおくと $x^2-2x-1=(x-\alpha)(x-\beta)$，$\beta-\alpha=2\sqrt2$。(1) より<br>"
         r"　$\displaystyle\int_\alpha^\beta(x-\alpha)(x-\beta)\,dx=-\frac{(2\sqrt2)^3}{6}=-\frac{16\sqrt2}{6}=\boldsymbol{-\frac{8\sqrt2}3}$",
  "note": r"(2) を直接計算すると $(1\pm\sqrt2)^3$ が現れて大変。$x^2$ の係数が $p$ のときは $\displaystyle\int_\alpha^\beta p(x-\alpha)(x-\beta)\,dx=-\frac p6(\beta-\alpha)^3$。同じ変形で $\displaystyle\int_\alpha^\beta(x-\alpha)^2(x-\beta)\,dx=-\frac{(\beta-\alpha)^4}{12}$ も示せる（3次関数と接線の面積で使う）。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-1}^{3}(x+1)(x-3)\,dx$　　(2) $\displaystyle\int_{\frac{1-\sqrt5}2}^{\frac{1+\sqrt5}2}(2x^2-2x-2)\,dx$",
  "exa": r"(1) $-\dfrac{32}{3}$　(2) $-\dfrac{5\sqrt5}{3}$"},
 {"lv": 2, "title": "定積分の条件から2次関数を決定する",
  "q": r"2次関数 $f(x)$ が　$f(1)=5$，$\displaystyle\int_{-1}^{1}f(x)\,dx=0$，$\displaystyle\int_{-1}^{1}xf(x)\,dx=2$　を満たすとき、$f(x)$ を求めよ。",
  "hint": r"$f(x)=ax^2+bx+c$（$a\neq0$）とおき、3つの条件を $a,\ b,\ c$ の連立方程式にする。$\int_{-1}^1$ なので奇数次の項は消える。",
  "sol": r"$f(x)=ax^2+bx+c$（$a\neq0$）とおく。<br>"
         r"$\displaystyle\int_{-1}^{1}f(x)\,dx=2\int_0^1(ax^2+c)\,dx=\frac{2}{3}a+2c$，"
         r"$\displaystyle\int_{-1}^{1}xf(x)\,dx=\int_{-1}^{1}(ax^3+bx^2+cx)\,dx=2\int_0^1bx^2\,dx=\frac23b$<br>"
         r"よって　$a+b+c=5$，$\dfrac23a+2c=0$，$\dfrac23b=2$<br>"
         r"第3式から $b=3$。第1式から $a+c=2$，第2式から $a=-3c$。よって $-2c=2$ より $c=-1,\ a=3$（$a\neq0$ を満たす）。<br>"
         r"したがって　$\boldsymbol{f(x)=3x^2+3x-1}$",
  "ex": r"2次関数 $f(x)$ が　$f(0)=1$，$\displaystyle\int_0^1f(x)\,dx=\frac32$，$\displaystyle\int_0^2f(x)\,dx=8$　を満たすとき、$f(x)$ を求めよ。",
  "exa": r"$f(x)=3x^2-x+1$"},
 {"lv": 3, "title": "シンプソンの公式（3次以下の整式）",
  "q": r"$f(x)$ を3次以下の整式とし、$m=\dfrac{a+b}{2}$ とする。<br>"
       r"(1) $\displaystyle\int_a^b f(x)\,dx=\frac{b-a}{6}\{f(a)+4f(m)+f(b)\}$ が成り立つことを示せ。<br>"
       r"(2) (1) を用いて $\displaystyle\int_1^3(2x^3-x^2+4)\,dx$ を求めよ。",
  "hint": r"区間の中点 $m$ を基準にして、$f(x)$ を $x-m$ の整式 $p+q(x-m)+r(x-m)^2+s(x-m)^3$ で表す。$h=\dfrac{b-a}2$ とおくと $a=m-h,\ b=m+h$ で、$(x-m)$ の奇数乗の積分は $0$ になる。",
  "sol": r"(1) $h=\dfrac{b-a}2$ とおくと $a=m-h$，$b=m+h$。3次以下の整式 $f(x)$ は<br>"
         r"　$f(x)=p+q(x-m)+r(x-m)^2+s(x-m)^3$（$p,\ q,\ r,\ s$ は定数）<br>"
         r"と表せる。$\displaystyle\int_a^b(x-m)^n\,dx=\Big[\frac{(x-m)^{n+1}}{n+1}\Big]_{m-h}^{m+h}=\frac{h^{n+1}-(-h)^{n+1}}{n+1}$ は、$n=0,\ 1,\ 2,\ 3$ のときそれぞれ $2h,\ 0,\ \dfrac23h^3,\ 0$。よって<br>"
         r"　左辺 $=2hp+\dfrac23rh^3$<br>"
         r"一方、$f(m)=p$，$f(a)=p-qh+rh^2-sh^3$，$f(b)=p+qh+rh^2+sh^3$ より $f(a)+4f(m)+f(b)=6p+2rh^2$ で、$\dfrac{b-a}6=\dfrac h3$ だから<br>"
         r"　右辺 $=\dfrac h3(6p+2rh^2)=2hp+\dfrac23rh^3$<br>"
         r"よって左辺と右辺は等しい。■<br>"
         r"(2) $f(x)=2x^3-x^2+4$，$a=1,\ b=3,\ m=2$ とすると $f(1)=5$，$f(2)=16$，$f(3)=49$。(1) より<br>"
         r"　$\displaystyle\int_1^3f(x)\,dx=\frac{3-1}{6}(5+4\cdot16+49)=\frac13\cdot118=\boldsymbol{\frac{118}3}$",
  "note": r"4次以上では一般に成り立たない（例：$f(x)=x^4,\ a=-1,\ b=1$ で左辺 $\frac25$，右辺 $\frac23$）。$f(x)=(x-\alpha)(x-\beta)$ に使うと $f(\alpha)=f(\beta)=0$，$f(m)=-\left(\frac{\beta-\alpha}2\right)^2$ から $\frac16$ 公式が出る。定積分の検算にも便利。",
  "ex": r"上の (1) の公式を用いて $\displaystyle\int_{-1}^{3}(x^3-3x^2+2x+5)\,dx$ を求めよ。",
  "exa": r"$20$"},
]})


def _v1():
    C = symbols("C")
    F = integrate(3*x**2-4*x+5, x); assert _eq(F, x**3-2*x**2+5*x)
    assert _eq(integrate((2*x+1)*(x-3), x), Rational(2, 3)*x**3-Rational(5, 2)*x**2-3*x)
    assert _eq(integrate((x+1)**2-(x-1)**2, x), 2*x**2)
    assert _eq(integrate(6*x**2+2*x-3, x), 2*x**3+x**2-3*x)
    assert _eq(integrate((x-2)*(3*x+1), x), x**3-Rational(5, 2)*x**2-2*x)
    assert _eq(integrate((2*x+1)**2+(2*x-1)**2, x), Rational(8, 3)*x**3+2*x)
    f = 2*x**3-x**2+x+1; assert _eq(diff(f, x), 6*x**2-2*x+1) and f.subs(x, 1) == 3
    g = x**3-2*x**2+1; assert _eq(diff(g, x), 3*x**2-4*x) and g.subs(x, 2) == 1
    f = -x**3+2*x**2+2*x-1; assert _eq(diff(f, x), -3*x**2+4*x+2) and f.subs(x, -1) == 0
    g = 3*x**2-5*x+4; assert _eq(diff(g, x), 6*x-5) and g.subs(x, 1) == 2
    assert integrate(3*x**2-2*x+1, (x, -1, 2)) == 9
    assert integrate(x**2+x, (x, -1, 1))+integrate(x**2+x, (x, 1, 2)) == Rational(9, 2)
    assert integrate(x**2-3*x, (x, 0, 2))-integrate(x**2-3*x, (x, 3, 2)) == Rational(-9, 2)
    assert integrate(x**2+4*x-1, (x, -2, 1)) == -6
    assert integrate(2*x**2-x, (x, 0, 2))+integrate(2*x**2-x, (x, 2, 3)) == Rational(27, 2)
    assert integrate(x**3+3*x**2-5*x+1, (x, -2, 2)) == 20
    assert integrate((x+1)**3, (x, -1, 1)) == 4
    assert integrate(2*x**3-x**2+4*x-3, (x, -3, 3)) == -36
    assert integrate((x-1)**2, (x, -2, 2)) == Rational(28, 3)
    al, be = symbols("alpha beta")
    assert _eq(integrate((x-al)*(x-be), (x, al, be)), -(be-al)**3/6)
    assert _eq(integrate((x-al)**2*(x-be), (x, al, be)), -(be-al)**4/12)
    assert _eq(integrate(x**2-2*x-1, (x, 1-sqrt(2), 1+sqrt(2))), -8*sqrt(2)/3)
    assert integrate((x+1)*(x-3), (x, -1, 3)) == Rational(-32, 3)
    assert _eq(integrate(2*x**2-2*x-2, (x, (1-sqrt(5))/2, (1+sqrt(5))/2)), -5*sqrt(5)/3)
    # 条件から2次関数
    f = 3*x**2+3*x-1
    assert f.subs(x, 1) == 5 and integrate(f, (x, -1, 1)) == 0 and integrate(x*f, (x, -1, 1)) == 2
    A, B, Cc = symbols("A B Cc")
    sol = solve([A+B+Cc-5, integrate(A*x**2+B*x+Cc, (x, -1, 1)), integrate(x*(A*x**2+B*x+Cc), (x, -1, 1))-2], [A, B, Cc])
    assert sol == {A: 3, B: 3, Cc: -1}
    f = 3*x**2-x+1
    assert f.subs(x, 0) == 1 and integrate(f, (x, 0, 1)) == Rational(3, 2) and integrate(f, (x, 0, 2)) == 8
    sol = solve([Cc-1, integrate(A*x**2+B*x+Cc, (x, 0, 1))-Rational(3, 2), integrate(A*x**2+B*x+Cc, (x, 0, 2))-8], [A, B, Cc])
    assert sol == {A: 3, B: -1, Cc: 1}
    # シンプソン：3次以下の一般の整式で恒等式
    p, q, r, s_, aa, bb = symbols("p q r s aa bb")
    f = p+q*x+r*x**2+s_*x**3
    mm = (aa+bb)/2
    assert _eq(integrate(f, (x, aa, bb)), (bb-aa)/6*(f.subs(x, aa)+4*f.subs(x, mm)+f.subs(x, bb)))
    h = symbols("h")
    ff = p+q*(x-mm)+r*(x-mm)**2+s_*(x-mm)**3
    assert _eq(integrate(ff, (x, mm-h, mm+h)), 2*h*p+Rational(2, 3)*r*h**3)
    f = 2*x**3-x**2+4
    assert [f.subs(x, v) for v in (1, 2, 3)] == [5, 16, 49]
    assert integrate(f, (x, 1, 3)) == Rational(118, 3) == Rational(2, 6)*(5+64+49)
    f = x**3-3*x**2+2*x+5
    assert integrate(f, (x, -1, 3)) == 20 == Rational(4, 6)*(f.subs(x, -1)+4*f.subs(x, 1)+f.subs(x, 3))
    assert integrate(x**4, (x, -1, 1)) == Rational(2, 5) and Rational(2, 6)*(1+0+1) == Rational(2, 3)


def _tb(*rows):
    """増減表など。rows の各行は [見出し, セル, ...]（raw 文字列）。"""
    h = "<table>"
    for r in rows:
        h += "<tr><th>" + r[0] + "</th>" + "".join("<td>" + c_ + "</td>" for c_ in r[1:]) + "</tr>"
    return h + "</table>"


UP, DN = r"$\nearrow$", r"$\searrow$"

# ---------------------------------------------------------------- 節2
SEC.append({"title": "定積分で表された関数",
"base": r"""・$a$ が定数のとき　$\dfrac{d}{dx}\displaystyle\int_a^x f(t)\,dt=f(x)$，また $\displaystyle\int_a^a f(t)\,dt=0$<br>
・$\displaystyle\int_a^b f(t)\,dt$（$a,\ b$ は定数）は定数 → $k$ などとおき、$k$ についての方程式を立てる<br>
・被積分関数が $x$ を含むときは $x$ を積分の外に出す：$\displaystyle\int_a^x(x-t)f(t)\,dt=x\int_a^x f(t)\,dt-\int_a^x tf(t)\,dt$<br>
・整式 $g(x)$ について $\{xg(x)\}'=g(x)+xg'(x)$（展開すれば確かめられる）""",
"items": [
 {"lv": 1, "title": "上端が $x$ の定積分の微分",
  "q": r"次の関数を $x$ で微分せよ。<br>(1) $\displaystyle\int_1^x(t^2-3t+1)\,dt$　　(2) $\displaystyle\int_x^2(t^3-t)\,dt$　　(3) $\displaystyle\int_{-1}^{x}(x+t)\,dt$",
  "hint": r"(1) は公式 $\dfrac{d}{dx}\int_a^x f(t)\,dt=f(x)$ そのもの。(2) は上端と下端を入れかえる。(3) は被積分関数に $x$ が含まれるので公式は使えない。$t$ で積分すると $x$ は定数扱い。",
  "sol": r"(1) $\boldsymbol{x^2-3x+1}$<br>"
         r"(2) $\displaystyle\int_x^2(t^3-t)\,dt=-\int_2^x(t^3-t)\,dt$ だから、微分すると　$-(x^3-x)=\boldsymbol{-x^3+x}$<br>"
         r"(3) $t$ についての積分で、$x$ は定数とみて<br>"
         r"　$\displaystyle\int_{-1}^{x}(x+t)\,dt=\Big[xt+\frac{t^2}2\Big]_{t=-1}^{t=x}=\Big(x^2+\frac{x^2}2\Big)-\Big(-x+\frac12\Big)=\frac32x^2+x-\frac12$<br>"
         r"　よって、微分すると　$\boldsymbol{3x+1}$",
  "note": r"(3) で公式をそのまま使って「$x+x=2x$」とするのはよくある誤り。$x$ を含むときは、先に積分してしまうか、$\displaystyle x\int_{-1}^x dt+\int_{-1}^x t\,dt$ と $x$ を外に出してから微分する。",
  "ex": r"次の関数を $x$ で微分せよ。<br>(1) $\displaystyle\int_{-1}^{x}(2t^2+t-4)\,dt$　　(2) $\displaystyle\int_x^0(t^2+5)\,dt$　　(3) $\displaystyle\int_0^x(2x-t)\,dt$",
  "exa": r"(1) $2x^2+x-4$　(2) $-x^2-5$　(3) $3x$"},
 {"lv": 2, "title": r"$\int_a^x f(t)\,dt=g(x)$ 型（関数と定数の決定）",
  "q": r"等式 $\displaystyle\int_a^x f(t)\,dt=x^3-2x^2+x-2$ を満たす関数 $f(x)$ と定数 $a$ の値を求めよ。",
  "hint": r"両辺を $x$ で微分すれば $f(x)$ が出る。$a$ は「$x=a$ を代入すると左辺が $0$」から求める。",
  "sol": r"両辺を $x$ で微分すると　$\boldsymbol{f(x)=3x^2-4x+1}$<br>"
         r"また、等式に $x=a$ を代入すると、左辺は $\displaystyle\int_a^a f(t)\,dt=0$ だから<br>"
         r"　$0=a^3-2a^2+a-2=a^2(a-2)+(a-2)=(a-2)(a^2+1)$<br>"
         r"$a$ は実数なので　$\boldsymbol{a=2}$",
  "note": r"微分すると右辺の定数項 $-2$ の情報が消える。それを補うのが $x=a$ の代入である。逆に $f(x)=3x^2-4x+1,\ a=2$ のとき $\int_2^x f(t)\,dt=\Big[t^3-2t^2+t\Big]_2^x=x^3-2x^2+x-2$ で確かに成り立つ。",
  "ex": r"等式 $\displaystyle\int_a^x f(t)\,dt=x^2+x-6$ を満たす関数 $f(x)$ と定数 $a$ の値を求めよ。",
  "exa": r"$f(x)=2x+1$，$a=2,\ -3$"},
 {"lv": 2, "title": r"$\int_a^b f(t)\,dt$ を含む関数（定数とおく）",
  "q": r"等式 $f(x)=3x^2-x\displaystyle\int_0^2 f(t)\,dt+2$ を満たす関数 $f(x)$ を求めよ。",
  "hint": r"$\displaystyle\int_0^2 f(t)\,dt$ は積分区間が定数なので定数である。これを $k$ とおくと $f(x)=3x^2-kx+2$ と表せ、$k$ の定義に戻って $k$ の方程式を作る。",
  "sol": r"$\displaystyle\int_0^2 f(t)\,dt=k$（定数）とおくと　$f(x)=3x^2-kx+2$<br>"
         r"よって　$\displaystyle k=\int_0^2(3t^2-kt+2)\,dt=\Big[t^3-\frac k2t^2+2t\Big]_0^2=8-2k+4=12-2k$<br>"
         r"これより $3k=12$，$k=4$。したがって　$\boldsymbol{f(x)=3x^2-4x+2}$",
  "note": r"$\int_0^2 f(t)\,dt$ の $t$ を $x$ と書いても同じ値（積分変数は何でもよい）。$\int_0^x f(t)\,dt$ のように区間に $x$ を含むものは定数ではないので、区別すること。",
  "ex": r"等式 $f(x)=x^2-2x\displaystyle\int_0^1 f(t)\,dt+1$ を満たす関数 $f(x)$ を求めよ。",
  "exa": r"$f(x)=x^2-\dfrac43x+1$"},
 {"lv": 2, "title": "定積分で表された関数の最大・最小",
  "q": r"$F(x)=\displaystyle\int_0^x(t-1)(t-3)\,dt$ の $0\leqq x\leqq4$ における最大値と最小値を求めよ。",
  "hint": r"$F'(x)=(x-1)(x-3)$ なので、積分を計算しなくても増減はわかる。極値と端点の値は $F(x)$ を計算して比べる。",
  "sol": r"$F'(x)=(x-1)(x-3)$。また<br>"
         r"　$\displaystyle F(x)=\int_0^x(t^2-4t+3)\,dt=\frac{x^3}3-2x^2+3x=\frac13x(x-3)^2$<br>"
         + _tb([r"$x$", r"$0$", r"$\cdots$", r"$1$", r"$\cdots$", r"$3$", r"$\cdots$", r"$4$"],
               [r"$F'(x)$", "", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$", ""],
               [r"$F(x)$", r"$0$", UP, r"$\frac43$", DN, r"$0$", UP, r"$\frac43$"]) +
         r"$F(1)=\dfrac13\cdot1\cdot4=\dfrac43$，$F(4)=\dfrac13\cdot4\cdot1=\dfrac43$ だから<br>"
         r"　<b>最大値</b> $\boldsymbol{\dfrac43}$（$x=1,\ 4$），<b>最小値</b> $\boldsymbol{0}$（$x=0,\ 3$）",
  "note": r"$F(x)$ は「$y=(t-1)(t-3)$ のグラフと $t$ 軸の間の、$0$ から $x$ までの符号つき面積」を表す。$1\leqq t\leqq3$ では負なので $F$ は減少し、$F(3)=0$ は正の部分と負の部分の面積が等しいことを意味する。",
  "ex": r"$G(x)=\displaystyle\int_1^x(t^2-4)\,dt$ の $-3\leqq x\leqq3$ における最大値と最小値を求めよ。",
  "exa": r"最大値 $9$（$x=-2$），最小値 $-\dfrac53$（$x=2$）"},
 {"lv": 3, "title": "2つの定積分を定数とおく",
  "q": r"等式 $f(x)=3x^2-2x+\displaystyle\int_0^2(t-x)f(t)\,dt$ を満たす関数 $f(x)$ を求めよ。",
  "hint": r"$x$ は $t$ の積分では定数なので、$\displaystyle\int_0^2(t-x)f(t)\,dt=\int_0^2 tf(t)\,dt-x\int_0^2 f(t)\,dt$ と分ける。2つの定数 $A=\int_0^2 f(t)\,dt$，$B=\int_0^2 tf(t)\,dt$ についての連立方程式を立てる。",
  "sol": r"$A=\displaystyle\int_0^2 f(t)\,dt$，$B=\displaystyle\int_0^2 tf(t)\,dt$（ともに定数）とおくと<br>"
         r"　$f(x)=3x^2-2x+B-Ax=3x^2-(A+2)x+B$<br>"
         r"$\displaystyle A=\int_0^2\{3t^2-(A+2)t+B\}\,dt=8-2(A+2)+2B$ より　$3A-2B=4$　…①<br>"
         r"$\displaystyle B=\int_0^2\{3t^3-(A+2)t^2+Bt\}\,dt=12-\frac83(A+2)+2B$ より　$8A-3B=20$　…②<br>"
         r"①$\times3-$②$\times2$ より $-7A=-28$，$A=4$。①より $B=4$。<br>"
         r"よって　$\boldsymbol{f(x)=3x^2-6x+4}$",
  "note": r"検算：$\int_0^2(3t^2-6t+4)\,dt=8-12+8=4$，$\int_0^2(3t^3-6t^2+4t)\,dt=12-16+8=4$ で $A=B=4$ と一致する。$x$ を積分の外に出すことを忘れて $(t-x)$ のまま定数とおくのは誤り。",
  "ex": r"等式 $f(x)=6x^2-x+\displaystyle\int_0^1(x-t)f(t)\,dt$ を満たす関数 $f(x)$ を求めよ。",
  "exa": r"$f(x)=6x^2-1$"},
 {"lv": 3, "title": r"$\int_a^x(x-t)f(t)\,dt$ 型",
  "q": r"等式 $\displaystyle\int_a^x(x-t)f(t)\,dt=x^3-3x^2+4$ を満たす整式 $f(x)$ と定数 $a$ の値を求めよ。",
  "hint": r"$x$ を積分の外に出し $x\int_a^x f(t)\,dt-\int_a^x tf(t)\,dt$ としてから微分する。2回微分すると $f(x)$ が出る。$a$ は、もとの等式と1回微分した等式の両方に $x=a$ を代入して求める。",
  "sol": r"左辺 $\displaystyle=x\int_a^x f(t)\,dt-\int_a^x tf(t)\,dt$。両辺を $x$ で微分すると<br>"
         r"　$\displaystyle\int_a^x f(t)\,dt+xf(x)-xf(x)=3x^2-6x$，すなわち　$\displaystyle\int_a^x f(t)\,dt=3x^2-6x$　…①<br>"
         r"①の両辺をさらに微分して　$\boldsymbol{f(x)=6x-6}$<br>"
         r"もとの等式に $x=a$ を代入すると　$0=a^3-3a^2+4=(a+1)(a-2)^2$　より $a=-1,\ 2$<br>"
         r"①に $x=a$ を代入すると　$0=3a^2-6a=3a(a-2)$　より $a=0,\ 2$<br>"
         r"両方を満たすのは　$\boldsymbol{a=2}$<br>"
         r"逆にこのとき、①の左辺は $\Big[3t^2-6t\Big]_2^x=3x^2-6x$ で①が成り立つ。よってもとの等式の両辺は微分すると等しく、$x=2$ でともに $0$ だから、もとの等式も成り立つ。",
  "note": r"微分するたびに定数の情報が1つずつ失われるので、条件「$x=a$ で $0$」を各段階で使う必要がある。$a=-1$ はもとの等式の条件は満たすが、①を満たさない（実際 $\int_{-1}^x(x-t)(6t-6)\,dt=x^3-3x^2-9x-5$ となり、等式は成り立たない）。",
  "ex": r"等式 $\displaystyle\int_a^x(x-t)f(t)\,dt=x^4-2x^2+1$ を満たす整式 $f(x)$ と定数 $a$ の値を求めよ。",
  "exa": r"$f(x)=12x^2-4$，$a=\pm1$"},
 {"lv": 4, "title": "次数に注目して整式を決定する",
  "q": r"定数でない整式 $f(x)$ で、すべての実数 $x$ について　$\displaystyle\int_0^x f(t)\,dt=\frac13f(x)f'(x)$　を満たすものを求めよ。",
  "hint": r"$f(x)$ の次数を $n$ として、両辺の次数と最高次の係数を比べる。まず次数 $n$ を決めてから、係数を比較する。",
  "sol": r"$f(x)$ の次数を $n\ (n\geqq1)$、最高次の係数を $p\ (p\neq0)$ とする。<br>"
         r"左辺は $n+1$ 次式で、最高次の係数は $\dfrac{p}{n+1}$。右辺は $f'(x)$ が $n-1$ 次（最高次の係数 $np$）なので $2n-1$ 次式で、最高次の係数は $\dfrac13\cdot p\cdot np=\dfrac{np^2}3$。<br>"
         r"次数を比べて $n+1=2n-1$，よって $n=2$。最高次の係数を比べて $\dfrac p3=\dfrac{2p^2}3$，$p\neq0$ より $p=\dfrac12$。<br>"
         r"そこで $f(x)=\dfrac12x^2+qx+r$ とおくと、$f'(x)=x+q$ で<br>"
         r"　左辺 $=\dfrac16x^3+\dfrac q2x^2+rx$<br>"
         r"　右辺 $=\dfrac13\Big(\dfrac12x^2+qx+r\Big)(x+q)=\dfrac16x^3+\dfrac q2x^2+\dfrac{q^2+r}3x+\dfrac{qr}3$<br>"
         r"係数を比べて　$r=\dfrac{q^2+r}{3}$，$\dfrac{qr}3=0$。第1式から $q^2=2r$。第2式から $q=0$ または $r=0$ で、どちらの場合も $q^2=2r$ から $q=r=0$。<br>"
         r"よって　$\boldsymbol{f(x)=\dfrac12x^2}$（実際、両辺とも $\dfrac16x^3$ となり成り立つ）",
  "note": r"「整式である」ことが次数比較の根拠である。$x=0$ を代入すると $f(0)f'(0)=0$ という条件も得られ、結果と矛盾しない。定数でないという条件がなければ、$f(x)=0$ も解になる。",
  "ex": r"定数でない整式 $f(x)$ で、すべての実数 $x$ について $\displaystyle\int_0^x f(t)\,dt=\frac14\{f(x)\}^2$ を満たすものを求めよ。",
  "exa": r"$f(x)=2x$"},
 {"lv": 4, "title": r"$\int_x^{x+1}f(t)\,dt$ で表された関数方程式",
  "q": r"すべての実数 $x$ について　$\displaystyle\int_x^{x+1}f(t)\,dt=x^2$　を満たす整式 $f(x)$ を求めよ。",
  "hint": r"$\displaystyle\int_x^{x+1}t^n\,dt=\frac{(x+1)^{n+1}-x^{n+1}}{n+1}$ は、最高次の係数が $1$ の $x$ の $n$ 次式。したがって左辺は $f(x)$ と同じ次数になり、$f(x)$ は2次式とわかる。",
  "sol": r"$\displaystyle\int_x^{x+1}t^n\,dt=\frac{(x+1)^{n+1}-x^{n+1}}{n+1}$ を展開すると、$x^n$ の係数が $1$ で、残りは $n-1$ 次以下の項である。よって、$f(x)$ が $n$ 次式（最高次の係数 $p\neq0$）なら左辺は $n$ 次式（最高次の係数 $p$）になる。右辺と比べて $f(x)$ は2次式で、$x^2$ の係数は $1$。<br>"
         r"$f(x)=x^2+qx+r$ とおくと<br>"
         r"　$\displaystyle\int_x^{x+1}f(t)\,dt=\frac{(x+1)^3-x^3}3+q\cdot\frac{(x+1)^2-x^2}2+r=x^2+x+\frac13+qx+\frac q2+r$<br>"
         r"　$=x^2+(1+q)x+\dfrac13+\dfrac q2+r$<br>"
         r"これが $x^2$ に恒等的に等しいから　$1+q=0$，$\dfrac13+\dfrac q2+r=0$<br>"
         r"よって $q=-1$，$r=\dfrac16$ で　$\boldsymbol{f(x)=x^2-x+\dfrac16}$",
  "note": r"両辺を $x$ で微分して $f(x+1)-f(x)=2x$ を導き、次数を比べる方法もある（その場合、定数 $r$ は $x=0$ を代入した $\int_0^1f(t)\,dt=0$ から決める）。",
  "ex": r"すべての実数 $x$ について $\displaystyle\int_x^{x+1}f(t)\,dt=3x^2+x$ を満たす整式 $f(x)$ を求めよ。",
  "exa": r"$f(x)=3x^2-2x$"},
]})


def _v2():
    X = symbols("X", real=True)
    assert _eq(diff(integrate(t**2-3*t+1, (t, 1, x)), x), x**2-3*x+1)
    assert _eq(diff(integrate(t**3-t, (t, x, 2)), x), -x**3+x)
    I3 = integrate(x+t, (t, -1, x)); assert _eq(I3, Rational(3, 2)*x**2+x-Rational(1, 2)) and _eq(diff(I3, x), 3*x+1)
    assert _eq(diff(integrate(2*t**2+t-4, (t, -1, x)), x), 2*x**2+x-4)
    assert _eq(diff(integrate(t**2+5, (t, x, 0)), x), -x**2-5)
    assert _eq(diff(integrate(2*x-t, (t, 0, x)), x), 3*x)
    # ∫_a^x f = g
    assert _eq(integrate(3*t**2-4*t+1, (t, 2, x)), x**3-2*x**2+x-2)
    assert solve(a**3-2*a**2+a-2, a) == [2]
    assert _eq(integrate(2*t+1, (t, 2, x)), x**2+x-6) and _eq(integrate(2*t+1, (t, -3, x)), x**2+x-6)
    assert sorted(solve(a**2+a-6, a)) == [-3, 2]
    # 定数とおく
    f = 3*x**2-4*x+2; assert _eq(f, 3*x**2-x*integrate(f.subs(x, t), (t, 0, 2))+2)
    kk = symbols("kk"); assert solve(kk-integrate(3*t**2-kk*t+2, (t, 0, 2)), kk) == [4]
    f = x**2-Rational(4, 3)*x+1; assert _eq(f, x**2-2*x*integrate(f.subs(x, t), (t, 0, 1))+1)
    assert solve(kk-integrate(t**2-2*kk*t+1, (t, 0, 1)), kk) == [Rational(2, 3)]
    # 最大最小
    F = integrate((t-1)*(t-3), (t, 0, x)); assert _eq(F, x*(x-3)**2/3)
    vals = [F.subs(x, Rational(i, 100)) for i in range(0, 401)]
    assert max(vals) == Rational(4, 3) and min(vals) == 0
    assert F.subs(x, 1) == Rational(4, 3) and F.subs(x, 4) == Rational(4, 3) and F.subs(x, 3) == 0
    G = integrate(t**2-4, (t, 1, x))
    vals = [G.subs(x, Rational(i, 100)) for i in range(-300, 301)]
    assert max(vals) == 9 == G.subs(x, -2) and min(vals) == Rational(-5, 3) == G.subs(x, 2)
    assert G.subs(x, -3) < 9 and G.subs(x, 3) > Rational(-5, 3)
    # 2つの定数
    f = 3*x**2-6*x+4
    assert _eq(f, 3*x**2-2*x+integrate((t-x)*f.subs(x, t), (t, 0, 2)))
    A, B = symbols("A B")
    ff = 3*x**2-(A+2)*x+B
    e1 = expand(A-integrate(ff.subs(x, t), (t, 0, 2))); e2 = expand(B-integrate(t*ff.subs(x, t), (t, 0, 2)))
    assert _eq(e1, 3*A-2*B-4) and _eq(e2, (8*A-3*B-20)/3)
    assert solve([e1, e2], [A, B]) == {A: 4, B: 4}
    f = 6*x**2-1
    assert _eq(f, 6*x**2-x+integrate((x-t)*f.subs(x, t), (t, 0, 1)))
    # (x-t)型
    assert _eq(integrate((x-t)*(6*t-6), (t, 2, x)), x**3-3*x**2+4)
    assert _eq(integrate((x-t)*(6*t-6), (t, -1, x)), x**3-3*x**2-9*x-5)
    assert _eq(factor(a**3-3*a**2+4), (a+1)*(a-2)**2)
    assert _eq(integrate((x-t)*(12*t**2-4), (t, 1, x)), (x**2-1)**2)
    assert _eq(integrate((x-t)*(12*t**2-4), (t, -1, x)), (x**2-1)**2)
    # 次数：3次以下の一般形で解をすべて求める（次数の議論は本文）
    cs = symbols("c0:5")
    for deg in range(1, 5):
        f = sum(cs[i]*x**i for i in range(deg+1))
        eqs = Poly(expand(integrate(f.subs(x, t), (t, 0, x))-f*diff(f, x)/3), x).all_coeffs()
        sols = solve(eqs, cs[:deg+1], dict=True)
        nonconst = [expand(f.subs(s_)) for s_ in sols if any(expand(f.subs(s_)).coeff(x, i) != 0 for i in range(1, deg+1))]
        assert all(_eq(g_, x**2/2) for g_ in nonconst) and (deg < 2 or nonconst)
        eqs = Poly(expand(integrate(f.subs(x, t), (t, 0, x))-f**2/4), x).all_coeffs()
        sols = solve(eqs, cs[:deg+1], dict=True)
        nonconst = [expand(f.subs(s_)) for s_ in sols if any(expand(f.subs(s_)).coeff(x, i) != 0 for i in range(1, deg+1))]
        assert all(_eq(g_, 2*x) for g_ in nonconst) and nonconst
    # ∫_x^{x+1}
    for rhs, ans in ((x**2, x**2-x+Rational(1, 6)), (3*x**2+x, 3*x**2-2*x)):
        assert _eq(integrate(ans.subs(x, t), (t, x, x+1)), rhs)
        f = sum(cs[i]*x**i for i in range(5))
        sols = solve(Poly(expand(integrate(f.subs(x, t), (t, x, x+1))-rhs), x).all_coeffs(), cs, dict=True)
        assert len(sols) == 1 and _eq(f.subs(sols[0]), ans)


# ---------------------------------------------------------------- 節3 の図
def _f31():
    g = _G(190, 150, (-0.7, 3.6), (-1.5, 3.6))
    f = lambda u: u*u-2*u
    g.band(f, lambda u: 0, 0, 2)
    g.band(lambda u: 0, f, 2, 3)
    g.axes()
    g.seg((3, -1.4), (3, 3.5), col="#555", dash="")
    g.curve(f, -0.65, 3.4)
    g.txt(2, 0, "2", dx=-6, dy=-4)
    g.txt(3, 0, "3", dx=6, dy=11)
    g.txt(2.25, 2.6, "y=x²−2x", anc="end", it=True)
    return g.svg()


def _f32():
    g = _G(190, 160, (-1.8, 3.2), (-0.6, 5.0))
    f, l = (lambda u: u*u), (lambda u: u+2)
    g.band(f, l, -1, 2)
    g.axes()
    g.curve(f, -1.8, 2.3)
    g.curve(l, -1.8, 3.2, col=C2)
    g.seg((-1, 0), (-1, 1)); g.seg((2, 0), (2, 4))
    g.xtick(-1, "−1"); g.xtick(2, "2")
    g.txt(2.12, 3.5, "y=x+2", anc="start", it=True, col=C2)
    g.txt(-1.75, 3.6, "y=x²", anc="start", it=True)
    return g.svg()


def _f34():
    g = _G(190, 160, (-0.8, 4.2), (-1.5, 4.9))
    f1, f2 = (lambda u: u*u-4*u+3), (lambda u: -u*u+2*u+3)
    g.band(f1, f2, 0, 3)
    g.axes()
    g.curve(f1, -0.4, 4.15)
    g.curve(f2, -0.8, 3.6, col=C2)
    g.xtick(3, "")
    g.txt(3, 0, "3", dx=-11, dy=-3, size=9)
    g.txt(3.5, 3.6, "y=x²−4x+3", anc="end", it=True)
    g.txt(1.0, 4.35, "y=−x²+2x+3", anc="start", it=True, col=C2, dx=6)
    return g.svg()


def _f35():
    g = _G(170, 150, (-0.6, 3.0), (-2.6, 4.6))
    f, l = (lambda u: u*u-2*u+2), (lambda u: 2*u-2)
    g.band(l, f, 0, 2)
    g.axes()
    g.curve(f, -0.6, 2.95)
    g.curve(l, -0.3, 3.0, col=C2)
    g.pt(2, 2)
    g.seg((2, 0), (2, 2))
    g.xtick(2, "2", dy=11)
    g.txt(2, 2, "(2, 2)", dx=-4, dy=-6, anc="end", size=9)
    g.txt(0, 2, "2", dx=-5, dy=4, anc="end", size=9)
    g.txt(2.95, 1.5, "ℓ", anc="end", it=True, col=C2)
    return g.svg()


def _f36():
    g = _G(190, 160, (-1.8, 2.7), (-2.7, 5.0))
    f, l1, l2 = (lambda u: u*u), (lambda u: -2*u-1), (lambda u: 4*u-4)
    g.band(lambda u: max(l1(u), l2(u)), f, -1, 2)
    g.axes()
    g.curve(f, -1.8, 2.25)
    g.curve(l1, -1.8, 1.2, col=C2)
    g.curve(l2, 0.0, 2.2, col=C2)
    g.pt(-1, 1); g.pt(2, 4); g.pt(0.5, -2)
    g.seg((0.5, 0), (0.5, -2))
    g.txt(0.5, 0, "½", dx=6, dy=11, size=10)
    g.txt(-1, 1, "(−1, 1)", dx=-4, dy=12, anc="end", size=9)
    g.txt(2, 4, "(2, 4)", dx=-5, dy=1, anc="end", size=9)
    g.txt(-1.7, -2.2, "ℓ₁", anc="start", it=True, col=C2)
    g.txt(2.3, 4.6, "ℓ₂", anc="start", it=True, col=C2)
    return g.svg()


def _f37():
    m0 = 2-4**(1/3)
    g = _G(190, 130, (-0.4, 2.6), (-0.35, 1.45))
    f, l = (lambda u: 2*u-u*u), (lambda u: m0*u)
    g.band(lambda u: 0, lambda u: min(f(u), l(u)), 0, 2, fill="#e6eefa")
    g.band(l, f, 0, 2-m0)
    g.axes()
    g.curve(f, -0.15, 2.15)
    g.curve(l, -0.3, 2.55, col=C2)
    g.xtick(2, "")
    g.txt(2, 0, "2", dx=7, dy=-3)
    g.txt(2.55, 1.18, "y=mx", anc="end", it=True, col=C2)
    g.txt(1.0, 1.0, "y=2x−x²", dy=-5, it=True)
    return g.svg()


def _f38():
    g = _G(190, 165, (-0.6, 4.1), (-1.6, 9.0))
    f1, f2, l = (lambda u: u*u), (lambda u: u*u-4*u+8), (lambda u: 2*u-1)
    g.band(l, f1, 1, 2)
    g.band(l, f2, 2, 3)
    g.axes()
    g.curve(f1, -0.6, 3.0)
    g.curve(f2, 0.2, 4.1)
    g.curve(l, 0.0, 4.1, col=C2)
    g.pt(1, 1); g.pt(3, 5); g.pt(2, 4)
    g.seg((2, 0), (2, 4)); g.seg((1, 0), (1, 1)); g.seg((3, 0), (3, 5))
    g.xtick(1, "1"); g.xtick(2, "2"); g.xtick(3, "3")
    g.txt(2.55, 8.2, "C₁", anc="end", it=True)
    g.txt(0.45, 7.2, "C₂", anc="start", it=True)
    g.txt(4.0, 6.0, "ℓ", anc="end", it=True, col=C2)
    return g.svg()


def _f39():
    g = _G(200, 170, (-1.55, 1.55), (-0.3, 2.45), eq=True)
    r3 = math.sqrt(3)/2
    arc = lambda u: 1.25-math.sqrt(max(0.0, 1-u*u))
    g.band(lambda u: u*u, arc, -r3, r3)
    g.axes()
    g.curve(lambda u: u*u, -1.5, 1.5)
    g.pcurve(lambda s_: math.cos(s_), lambda s_: 1.25+math.sin(s_), 0, 2*math.pi, col=C2)
    g.pt(r3, 0.75); g.pt(-r3, 0.75); g.pt(0, 1.25, col=C2, r=1.5)
    g.txt(1.5, 2.15, "P", anc="end", it=True)
    g.txt(-1.0, 2.15, "C", anc="end", it=True, col=C2)
    return g.svg()


# ---------------------------------------------------------------- 節3
SEC.append({"title": "放物線と面積",
"base": r"""・$a\leqq x\leqq b$ で $f(x)\geqq g(x)$ のとき、2曲線と2直線 $x=a,\ x=b$ で囲まれた部分の面積は　$S=\displaystyle\int_a^b\{f(x)-g(x)\}\,dx$（上の式 − 下の式）<br>
・放物線と直線（または2つの放物線）が $x=\alpha,\ \beta\ (\alpha<\beta)$ で交わり、差の式の $x^2$ の係数が $p$ のとき、囲まれた部分の面積は　$S=\dfrac{|p|}{6}(\beta-\alpha)^3$<br>
・放物線 $y=px^2+qx+r$ と、$x=\alpha,\ \beta$ における2本の接線で囲まれた部分の面積は　$\dfrac{|p|}{12}(\beta-\alpha)^3$（2接線の交点の $x$ 座標は $\dfrac{\alpha+\beta}2$）""",
"items": [
 {"lv": 1, "title": "曲線と $x$ 軸の間の面積",
  "q": r"次の部分の面積 $S$ を求めよ。<br>(1) 放物線 $y=-x^2+2x+3$ と $x$ 軸で囲まれた部分<br>(2) 放物線 $y=x^2-2x$ と $x$ 軸、直線 $x=3$ で囲まれた2つの部分（面積の和）",
  "hint": r"まずグラフをかいて $x$ 軸との上下を確認する。$x$ 軸より下にある部分では、$-\int f(x)\,dx$ が面積になる。",
  "sol": _f31() +
         r"(1) $-x^2+2x+3=-(x+1)(x-3)$ より、$x$ 軸との交点の $x$ 座標は $-1,\ 3$ で、$-1\leqq x\leqq3$ で $y\geqq0$。<br>"
         r"$\displaystyle S=\int_{-1}^{3}(-x^2+2x+3)\,dx=\Big[-\frac{x^3}3+x^2+3x\Big]_{-1}^{3}=9-\Big(-\frac53\Big)=\boldsymbol{\frac{32}3}$<br>"
         r"(2) $x^2-2x=x(x-2)$ より、$0\leqq x\leqq2$ で $y\leqq0$，$2\leqq x\leqq3$ で $y\geqq0$（右図）。<br>"
         r"$\displaystyle S=-\int_0^2(x^2-2x)\,dx+\int_2^3(x^2-2x)\,dx$<br>"
         r"$F(x)=\dfrac{x^3}3-x^2$ とすると $F(0)=0$，$F(2)=-\dfrac43$，$F(3)=0$ だから<br>"
         r"$S=-\{F(2)-F(0)\}+\{F(3)-F(2)\}=\dfrac43+\dfrac43=\boldsymbol{\dfrac83}$",
  "note": r"(1) は $\frac16$ 公式で $\frac16\{3-(-1)\}^3=\frac{32}3$ と検算できる。(2) で $\int_0^3(x^2-2x)\,dx=F(3)-F(0)=0$ を答えるのは誤り。符号つきの面積が打ち消し合ってしまう。",
  "ex": r"次の部分の面積を求めよ。<br>(1) 放物線 $y=-x^2+4x$ と $x$ 軸で囲まれた部分<br>(2) 放物線 $y=x^2-x-2$ と $x$ 軸、$y$ 軸、直線 $x=3$ で囲まれた2つの部分（面積の和）",
  "exa": r"(1) $\dfrac{32}{3}$　(2) $\dfrac{31}{6}$"},
 {"lv": 1, "title": "放物線と直線の間の面積",
  "q": r"放物線 $y=x^2$ と直線 $y=x+2$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"交点の $x$ 座標を求め、その区間で「上の式 − 下の式」を積分する。",
  "sol": _f32() +
         r"$x^2=x+2$ より $(x+1)(x-2)=0$，$x=-1,\ 2$。<br>"
         r"$-1\leqq x\leqq2$ で $x+2\geqq x^2$ だから<br>"
         r"$\displaystyle S=\int_{-1}^{2}(x+2-x^2)\,dx=\Big[\frac{x^2}2+2x-\frac{x^3}3\Big]_{-1}^{2}$<br>"
         r"$\displaystyle=\Big(2+4-\frac83\Big)-\Big(\frac12-2+\frac13\Big)=\frac{10}3+\frac76=\boldsymbol{\frac92}$",
  "note": r"$x+2-x^2=-(x+1)(x-2)$ なので $\frac16$ 公式から $\frac16\cdot3^3=\frac92$ とすぐわかる。上下の判定は、区間内の1点（例えば $x=0$）で値を比べればよい。",
  "ex": r"放物線 $y=x^2-3$ と直線 $y=2x$ で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac{32}{3}$"},
 {"lv": 2, "title": r"$\frac16$ 公式（交点が無理数のとき）",
  "q": r"放物線 $y=x^2-2x-1$ と直線 $y=x+1$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"交点の $x$ 座標が無理数になるので、代入計算はしない。$x=\alpha,\ \beta$ を交点として $\frac16$ 公式を使い、$\beta-\alpha$ だけを求める。",
  "sol": r"$x^2-2x-1=x+1$ より $x^2-3x-2=0$。この2解を $\alpha,\ \beta\ (\alpha<\beta)$ とすると $\alpha,\ \beta=\dfrac{3\mp\sqrt{17}}2$ で、$\beta-\alpha=\sqrt{17}$。<br>"
         r"$\alpha\leqq x\leqq\beta$ では直線が放物線より上にあり、$(x+1)-(x^2-2x-1)=-(x^2-3x-2)=-(x-\alpha)(x-\beta)$ だから<br>"
         r"$\displaystyle S=-\int_\alpha^\beta(x-\alpha)(x-\beta)\,dx=\frac{(\beta-\alpha)^3}{6}=\frac{(\sqrt{17})^3}6=\boldsymbol{\frac{17\sqrt{17}}6}$",
  "note": r"$\beta-\alpha$ は解と係数の関係から $(\beta-\alpha)^2=(\alpha+\beta)^2-4\alpha\beta=9+8=17$ としても求まる。",
  "ex": r"放物線 $y=2x^2-3x$ と直線 $y=x+1$ で囲まれた部分の面積を求めよ。",
  "exa": r"$2\sqrt6$"},
 {"lv": 2, "title": "2つの放物線で囲まれた部分",
  "q": r"2つの放物線 $y=x^2-4x+3$，$y=-x^2+2x+3$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"2式の差は2次式になる。差の $x^2$ の係数が $2$ であることに注意して $\frac16$ 公式を使う。",
  "sol": _f34() +
         r"$x^2-4x+3=-x^2+2x+3$ より $2x^2-6x=0$，$x=0,\ 3$。<br>"
         r"$0\leqq x\leqq3$ では $-x^2+2x+3\geqq x^2-4x+3$ だから<br>"
         r"$\displaystyle S=\int_0^3\{(-x^2+2x+3)-(x^2-4x+3)\}\,dx=\int_0^3(-2x^2+6x)\,dx$<br>"
         r"$\displaystyle=-2\int_0^3x(x-3)\,dx=-2\cdot\Big(-\frac{3^3}6\Big)=\boldsymbol{9}$",
  "note": r"差の $x^2$ の係数 $2$ を掛け忘れて $\frac{27}6$ とする誤りが多い。直接 $\Big[-\frac23x^3+3x^2\Big]_0^3=-18+27=9$ と計算しても確かめられる。",
  "ex": r"2つの放物線 $y=2x^2-2x-1$，$y=-x^2+x+5$ で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac{27}{2}$"},
 {"lv": 2, "title": "放物線と接線で囲まれた部分",
  "q": r"放物線 $y=x^2-2x+2$ 上の点 $(2,\ 2)$ における接線を $\ell$ とする。この放物線と $\ell$ および $y$ 軸で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"放物線と接線の差は、接点の $x$ 座標を重解にもつので $(x-2)^2$ の形になる。$\displaystyle\int(x-p)^2dx=\frac{(x-p)^3}3+C$ を使う。",
  "sol": _f35() +
         r"$y'=2x-2$ より、点 $(2,\ 2)$ における接線の傾きは $2$。$\ell: y=2(x-2)+2=2x-2$<br>"
         r"$(x^2-2x+2)-(2x-2)=x^2-4x+4=(x-2)^2\geqq0$ だから、放物線は $\ell$ の上側にある（右図）。<br>"
         r"$\displaystyle S=\int_0^2(x-2)^2\,dx=\Big[\frac{(x-2)^3}{3}\Big]_0^2=0-\frac{-8}{3}=\boldsymbol{\frac83}$",
  "note": r"展開して $\int_0^2(x^2-4x+4)\,dx=\frac83-8+8$ としてもよいが、$(x-p)^2$ の形のまま積分すると計算が短く、誤りも少ない。",
  "ex": r"放物線 $y=-x^2+4x$ 上の点 $(3,\ 3)$ における接線と、この放物線および $y$ 軸で囲まれた部分の面積を求めよ。",
  "exa": r"$9$"},
 {"lv": 3, "title": "放物線と2本の接線で囲まれた部分",
  "q": r"放物線 $C: y=x^2$ 上の2点 $(-1,\ 1)$，$(2,\ 4)$ における接線をそれぞれ $\ell_1,\ \ell_2$ とする。$C,\ \ell_1,\ \ell_2$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"2接線の交点で区間を分ける。各区間で「放物線 − 接線」は $(x-p)^2$（$p$ は接点の $x$ 座標）の形になる。交点の $x$ 座標は、2つの接点の $x$ 座標の中点になる。",
  "sol": _f36() +
         r"$y'=2x$ より　$\ell_1: y=-2(x+1)+1=-2x-1$<br>"
         r"　　　　　　$\ell_2: y=4(x-2)+4=4x-4$<br>"
         r"$\ell_1,\ \ell_2$ の交点は $-2x-1=4x-4$ より $x=\dfrac12$。<br>"
         r"$x^2-(-2x-1)=(x+1)^2$，$x^2-(4x-4)=(x-2)^2$ だから<br>"
         r"$\displaystyle S=\int_{-1}^{\frac12}(x+1)^2\,dx+\int_{\frac12}^{2}(x-2)^2\,dx=\Big[\frac{(x+1)^3}3\Big]_{-1}^{\frac12}+\Big[\frac{(x-2)^3}3\Big]_{\frac12}^{2}$<br>"
         r"$=\dfrac13\cdot\dfrac{27}8+\dfrac13\cdot\dfrac{27}8=\boldsymbol{\dfrac94}$",
  "note": r"一般に、放物線 $y=px^2+qx+r$ の $x=\alpha,\ \beta$ における2接線の交点の $x$ 座標は $\frac{\alpha+\beta}2$ で、囲まれた部分の面積は $\frac{|p|}{12}(\beta-\alpha)^3$（本問は $\frac1{12}\cdot3^3=\frac94$）。弦と放物線で囲まれた部分 $\frac16(\beta-\alpha)^3$ のちょうど半分になる。",
  "ex": r"点 $(1,\ -1)$ から放物線 $y=x^2-2x+2$ に引いた2本の接線と、この放物線で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac{4\sqrt2}{3}$"},
 {"lv": 3, "title": "面積を2等分する直線",
  "q": r"放物線 $y=2x-x^2$ と $x$ 軸で囲まれた部分の面積を、原点を通る直線 $y=mx$ が2等分するとき、定数 $m$ の値を求めよ。",
  "hint": r"直線が囲まれた部分を通るのは $0<m<2$（$2$ は原点での放物線の接線の傾き）。直線と放物線で囲まれた部分の面積が、全体の半分になればよい。",
  "sol": _f37() +
         r"全体の面積は $\displaystyle\int_0^2(2x-x^2)\,dx=\frac{2^3}6=\frac43$。<br>"
         r"直線 $y=mx$ が囲まれた部分を2つに分けるのは $0<m<2$ のときで、このとき直線と放物線の交点の $x$ 座標は、$2x-x^2=mx$ より $x=0,\ 2-m$。<br>"
         r"直線と放物線で囲まれた部分（右図の濃い部分）の面積は<br>"
         r"$\displaystyle\int_0^{2-m}\{(2x-x^2)-mx\}\,dx=-\int_0^{2-m}x\{x-(2-m)\}\,dx=\frac{(2-m)^3}{6}$<br>"
         r"これが $\dfrac12\cdot\dfrac43=\dfrac23$ に等しいから $(2-m)^3=4$，$2-m=\sqrt[3]4$<br>"
         r"よって $\boldsymbol{m=2-\sqrt[3]4}$（$1<\sqrt[3]4<2$ より $0<m<2$ を満たす）",
  "note": r"直線より下側の部分（$x$ 軸との間）を直接計算するより、直線と放物線で囲まれた部分を $\frac16$ 公式で計算するほうが簡単。",
  "ex": r"放物線 $y=4x-x^2$ と $x$ 軸で囲まれた部分の面積を、直線 $y=mx$ が2等分するとき、定数 $m$ の値を求めよ。",
  "exa": r"$m=4-2\sqrt[3]{4}$"},
 {"lv": 3, "title": "2つの放物線と共通接線",
  "q": r"2つの放物線 $C_1: y=x^2$，$C_2: y=x^2-4x+8$ の両方に接する直線 $\ell$ の方程式を求めよ。また、$C_1,\ C_2,\ \ell$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$C_1$ 上の点 $(s,\ s^2)$ における接線を $C_2$ と連立し、重解をもつ（判別式 $=0$）条件で $s$ を決める。面積は $C_1$ と $C_2$ の交点で区間を分ける。",
  "sol": _f38() +
         r"$C_1$ 上の点 $(s,\ s^2)$ における接線は $y=2sx-s^2$。これが $C_2$ に接する条件は、<br>"
         r"$x^2-4x+8=2sx-s^2$，すなわち $x^2-2(s+2)x+s^2+8=0$ が重解をもつことで<br>"
         r"$\dfrac D4=(s+2)^2-(s^2+8)=4s-4=0$　より $s=1$<br>"
         r"よって　$\boldsymbol{\ell: y=2x-1}$。$C_1$ との接点は $x=1$，$C_2$ との接点は重解 $x=s+2=3$。<br>"
         r"$C_1$ と $C_2$ の交点は $x^2=x^2-4x+8$ より $x=2$。<br>"
         r"$x^2-(2x-1)=(x-1)^2$，$(x^2-4x+8)-(2x-1)=(x-3)^2$ だから<br>"
         r"$\displaystyle S=\int_1^2(x-1)^2\,dx+\int_2^3(x-3)^2\,dx=\frac13+\frac13=\boldsymbol{\frac23}$",
  "note": r"$x^2$ の係数が等しい2つの放物線では、交点の $x$ 座標 $2$ は2つの接点の $x$ 座標 $1,\ 3$ の中点になる。これは前の例題の「2接線の交点は接点の中点」と表裏の関係にある。",
  "ex": r"2つの放物線 $y=x^2+1$，$y=x^2-6x+4$ の両方に接する直線の方程式を求めよ。また、2つの放物線とこの直線で囲まれた部分の面積を求めよ。",
  "exa": r"$y=-2x$，面積 $\dfrac94$"},
 {"lv": 4, "title": "放物線と円で囲まれた部分",
  "q": _f39() +
       r"円 $C: x^2+\left(y-\dfrac54\right)^2=1$ と放物線 $P: y=x^2$ について<br>"
       r"(1) $C$ と $P$ は2点で接することを示せ。<br>"
       r"(2) $C$ と $P$ で囲まれた部分（右図の色のついた部分）の面積 $S$ を求めよ。",
  "hint": r"(1) $x^2=y$ を代入して $y$ だけの方程式にする。(2) 「直線 $y=\frac34$ と放物線で囲まれた部分」から「円の弓形（弦の下の部分）」を除く。弓形は扇形から三角形を引いて求める。",
  "sol": r"(1) $x^2=y$ を円の式に代入すると　$y+\left(y-\dfrac54\right)^2=1$，すなわち $y^2-\dfrac32y+\dfrac9{16}=\left(y-\dfrac34\right)^2=0$<br>"
         r"よって共有点は $y=\frac34$，$x=\pm\frac{\sqrt3}2$ の2点だけである。点 $\big(\frac{\sqrt3}2,\ \frac34\big)$ で、$P$ の接線の傾きは $2\cdot\frac{\sqrt3}2=\sqrt3$。円の中心 $\big(0,\ \frac54\big)$ とこの点を結ぶ半径の傾きは $\big(-\frac12\big)\div\frac{\sqrt3}2=-\frac1{\sqrt3}$ で、円の接線はこれに垂直だから傾き $\sqrt3$。接線が一致するので、この点で接する。対称性から点 $\big(-\frac{\sqrt3}2,\ \frac34\big)$ でも接する。■<br>"
         r"(2) 求める部分は、弦 $y=\frac34$（$|x|\leqq\frac{\sqrt3}2$）と $P$ で囲まれた部分から、弦と円の下側の弧で囲まれた弓形を除いたものである。<br>"
         r"前者の面積は　$\displaystyle\int_{-\frac{\sqrt3}2}^{\frac{\sqrt3}2}\left(\frac34-x^2\right)dx=\frac16(\sqrt3)^3=\frac{\sqrt3}2$<br>"
         r"円の中心から弦までの距離は $\dfrac54-\dfrac34=\dfrac12$，半径は $1$ なので、弦の両端を見込む中心角は $\dfrac{2}{3}\pi$。弓形の面積は<br>"
         r"　$\dfrac12\cdot1^2\cdot\dfrac23\pi-\dfrac12\cdot1^2\cdot\sin\dfrac23\pi=\dfrac\pi3-\dfrac{\sqrt3}4$<br>"
         r"よって　$S=\dfrac{\sqrt3}2-\left(\dfrac\pi3-\dfrac{\sqrt3}4\right)=\boldsymbol{\dfrac{3\sqrt3}4-\dfrac\pi3}$",
  "note": r"円の弧は整式のグラフではないので、直接は積分できない。直線（弦）で区切って「放物線の部分」と「扇形・三角形」に分けるのが定石。一般に $y=x^2$ と中心 $(0,\ b)$ の円が2点で接する条件は、$y$ の2次方程式が重解をもつことから $r^2=b-\frac14$（$b>\frac12$）。",
  "ex": r"円 $x^2+\left(y-\dfrac34\right)^2=\dfrac12$ と放物線 $y=x^2$ は2点で接する。この円と放物線で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac5{12}-\dfrac\pi8$"},
]})


def _num_area(top, bot, a_, b_, n=20000):
    h = (b_-a_)/n
    return sum((top(a_+(i+0.5)*h)-bot(a_+(i+0.5)*h))*h for i in range(n))


def _v3():
    assert integrate(-x**2+2*x+3, (x, -1, 3)) == Rational(32, 3)
    assert -integrate(x**2-2*x, (x, 0, 2))+integrate(x**2-2*x, (x, 2, 3)) == Rational(8, 3)
    assert integrate(-x**2+4*x, (x, 0, 4)) == Rational(32, 3)
    assert -integrate(x**2-x-2, (x, 0, 2))+integrate(x**2-x-2, (x, 2, 3)) == Rational(31, 6)
    assert abs(_num_area(lambda u: abs(u*u-u-2), lambda u: 0, 0, 3)-31/6) < 1e-6
    assert integrate(x+2-x**2, (x, -1, 2)) == Rational(9, 2)
    assert solve(x**2-3-2*x, x) == [-1, 3] and integrate(2*x-(x**2-3), (x, -1, 3)) == Rational(32, 3)
    r_ = solve(x**2-3*x-2, x); al, be = min(r_), max(r_)
    assert _eq(be-al, sqrt(17)) and _eq(integrate(x+1-(x**2-2*x-1), (x, al, be)), 17*sqrt(17)/6)
    r_ = solve(2*x**2-4*x-1, x); al, be = min(r_), max(r_)
    assert _eq(integrate(x+1-(2*x**2-3*x), (x, al, be)), 2*sqrt(6))
    assert integrate((-x**2+2*x+3)-(x**2-4*x+3), (x, 0, 3)) == 9
    assert solve((2*x**2-2*x-1)-(-x**2+x+5), x) == [-1, 2]
    assert integrate((-x**2+x+5)-(2*x**2-2*x-1), (x, -1, 2)) == Rational(27, 2)
    # 接線と y 軸
    assert _eq((x**2-2*x+2)-(2*x-2), (x-2)**2) and integrate((x-2)**2, (x, 0, 2)) == Rational(8, 3)
    f = -x**2+4*x; l = diff(f, x).subs(x, 3)*(x-3)+f.subs(x, 3)
    assert _eq(l-f, (x-3)**2) and integrate(l-f, (x, 0, 3)) == 9
    # 2接線
    S = integrate((x+1)**2, (x, -1, Rational(1, 2)))+integrate((x-2)**2, (x, Rational(1, 2), 2))
    assert S == Rational(9, 4)
    assert abs(_num_area(lambda u: u*u, lambda u: max(-2*u-1, 4*u-4), -1, 2)-2.25) < 1e-6
    f = x**2-2*x+2; s_ = symbols("s_")
    tl = diff(f, x).subs(x, s_)*(1-s_)+f.subs(x, s_)
    ss = sorted(solve(tl+1, s_), key=lambda v: float(v)); assert _eq(ss[0], 1-sqrt(2)) and _eq(ss[1], 1+sqrt(2))
    mid = (ss[0]+ss[1])/2
    T = lambda s0: diff(f, x).subs(x, s0)*(x-s0)+f.subs(x, s0)
    S = integrate(f-T(ss[0]), (x, ss[0], mid))+integrate(f-T(ss[1]), (x, mid, ss[1]))
    assert _eq(S, 4*sqrt(2)/3)
    # 2等分
    m0 = 2-cbrt(4)
    assert _eq(integrate(2*x-x**2-m0*x, (x, 0, 2-m0)), Rational(2, 3)) and 0 < float(m0) < 2
    m1 = 4-2*cbrt(4)
    assert _eq(integrate(4*x-x**2-m1*x, (x, 0, 4-m1)), Rational(16, 3)) and 0 < float(m1) < 4
    mm = float(m0)
    lower = _num_area(lambda u: min(2*u-u*u, mm*u), lambda u: 0, 0, 2)
    assert abs(lower-2/3) < 1e-6
    # 共通接線
    assert solve(expand((s_+2)**2-(s_**2+8)), s_) == [1]
    assert _eq(x**2-4*x+8-(2*x-1), (x-3)**2) and _eq(x**2-(2*x-1), (x-1)**2)
    assert integrate((x-1)**2, (x, 1, 2))+integrate((x-3)**2, (x, 2, 3)) == Rational(2, 3)
    # 練習：y=x^2+1, y=x^2-6x+4
    l = -2*x
    assert _eq(x**2+1-l, (x+1)**2) and _eq(x**2-6*x+4-l, (x-2)**2) and solve(x**2+1-(x**2-6*x+4), x) == [Rational(1, 2)]
    assert integrate((x+1)**2, (x, -1, Rational(1, 2)))+integrate((x-2)**2, (x, Rational(1, 2), 2)) == Rational(9, 4)
    # 円と放物線
    y = symbols("y")
    assert _eq(expand(y+(y-Rational(5, 4))**2-1), (y-Rational(3, 4))**2)
    r3 = sqrt(3)/2
    S = integrate(Rational(3, 4)-x**2, (x, -r3, r3))-(pi/3-sqrt(3)/4)
    assert _eq(S, 3*sqrt(3)/4-pi/3)
    num = _num_area(lambda u: 1.25-math.sqrt(1-u*u), lambda u: u*u, -float(r3), float(r3))
    assert abs(num-float(S)) < 1e-6
    assert _eq(expand(y+(y-Rational(3, 4))**2-Rational(1, 2)), (y-Rational(1, 4))**2)
    num = _num_area(lambda u: 0.75-math.sqrt(0.5-u*u), lambda u: u*u, -0.5, 0.5)
    assert abs(num-(5/12-math.pi/8)) < 1e-6
    # 接している（両側で円の下側の弧が放物線より上）
    assert all(1.25-math.sqrt(1-u*u) >= u*u-1e-12 for u in [i/1000*0.866 for i in range(-1000, 1001)])


# ---------------------------------------------------------------- 節4 の図
def _f41():
    g = _G(180, 130, (-0.5, 2.6), (-0.6, 0.65))
    f = lambda u: u*(u-1)*(u-2)
    g.band(lambda u: 0, f, 0, 1)
    g.band(f, lambda u: 0, 1, 2)
    g.axes()
    g.curve(f, -0.3, 2.45)
    g.txt(1, 0, "1", dx=-5, dy=11); g.txt(2, 0, "2", dx=-9, dy=11)
    g.txt(2.5, -0.56, "y=x³−3x²+2x", anc="end", it=True)
    return g.svg()


def _f42():
    g = _G(180, 160, (-2.6, 2.6), (-4.6, 4.2))
    f, l = (lambda u: u**3-4*u), (lambda u: -u-2)
    g.band(l, f, -2, 1)
    g.axes()
    g.curve(f, -2.6, 2.6)
    g.curve(l, -2.6, 2.4, col=C2)
    g.pt(1, -3); g.pt(-2, 0)
    g.seg((1, 0), (1, -3))
    g.txt(-2, 0, "−2", dx=-4, dy=11, anc="end")
    g.txt(1, 0, "1", dx=0, dy=-4)
    g.txt(1, -3, "(1, −3)", dx=-5, dy=12, anc="end", size=9)
    g.txt(-2.5, 1.2, "ℓ", anc="start", it=True, col=C2)
    g.txt(2.5, 3.6, "C", anc="end", it=True)
    return g.svg()


def _f43():
    g = _G(190, 150, (-0.4, 4.6), (-0.8, 5.4))
    f, l = (lambda u: u**3-6*u*u+9*u), (lambda u: u)
    g.band(l, f, 0, 2)
    g.band(f, l, 2, 4)
    g.axes()
    g.curve(f, -0.12, 4.45)
    g.curve(l, -0.4, 4.6, col=C2)
    g.pt(2, 2); g.pt(4, 4)
    g.seg((2, 0), (2, 2)); g.seg((4, 0), (4, 4))
    g.xtick(2, "2"); g.xtick(4, "4")
    g.txt(4.12, 3.55, "y=x", anc="start", it=True, col=C2)
    g.txt(1.0, 4.0, "y=x³−6x²+9x", dy=-5, it=True)
    return g.svg()


def _f45():
    g = _G(180, 150, (-1.75, 1.6), (-2.6, 2.4))
    f, l = (lambda u: u**4-2*u*u+u), (lambda u: u-1)
    g.band(l, f, -1, 1)
    g.axes()
    g.curve(f, -1.72, 1.52)
    g.curve(l, -1.75, 1.6, col=C2)
    g.pt(-1, -2); g.pt(1, 0)
    g.seg((-1, 0), (-1, -2))
    g.txt(-1, 0, "−1", dx=-2, dy=-4)
    g.txt(1, 0, "1", dx=4, dy=11)
    g.txt(1.58, 0.95, "ℓ", anc="end", it=True, col=C2)
    g.txt(-1.7, 1.4, "C", anc="start", it=True)
    return g.svg()


# ---------------------------------------------------------------- 節4
SEC.append({"title": "3次関数・4次関数のグラフと面積",
"base": r"""・曲線と $x$ 軸・直線の上下は、差の式を因数分解して符号を調べる<br>
・$\displaystyle\int_\alpha^\beta(x-\alpha)^2(x-\beta)\,dx=-\frac{(\beta-\alpha)^4}{12}$：3次関数 $y=px^3+\cdots$ のグラフと、$x=\alpha$ で接し $x=\beta$ で交わる直線で囲まれた部分の面積は $\dfrac{|p|}{12}|\beta-\alpha|^4$<br>
・$\displaystyle\int_\alpha^\beta(x-\alpha)^2(x-\beta)^2\,dx=\frac{(\beta-\alpha)^5}{30}$：4次関数 $y=px^4+\cdots$ のグラフと、$x=\alpha,\ \beta$ の2点で接する直線で囲まれた部分の面積は $\dfrac{|p|}{30}(\beta-\alpha)^5$<br>
・3次関数 $y=px^3+qx^2+rx+s$ のグラフは、$x=-\dfrac{q}{3p}$ の点に関して点対称""",
"items": [
 {"lv": 1, "title": "3次関数のグラフと $x$ 軸で囲まれた部分",
  "q": r"曲線 $y=x^3-3x^2+2x$ と $x$ 軸で囲まれた2つの部分の面積の和 $S$ を求めよ。",
  "hint": r"因数分解して $x$ 軸との交点と、各区間での符号を調べる。$x$ 軸より下の部分は $-\int$ にする。",
  "sol": _f41() +
         r"$x^3-3x^2+2x=x(x-1)(x-2)$ より、$x$ 軸との交点の $x$ 座標は $0,\ 1,\ 2$。<br>"
         r"$0\leqq x\leqq1$ で $y\geqq0$，$1\leqq x\leqq2$ で $y\leqq0$。<br>"
         r"$F(x)=\dfrac{x^4}4-x^3+x^2$ とすると $F(0)=0$，$F(1)=\dfrac14$，$F(2)=0$ だから<br>"
         r"$\displaystyle S=\int_0^1 y\,dx-\int_1^2 y\,dx=\{F(1)-F(0)\}-\{F(2)-F(1)\}=\frac14+\frac14=\boldsymbol{\frac12}$",
  "note": r"このグラフは点 $(1,\ 0)$ に関して対称なので、2つの部分の面積は等しい。$\int_0^2y\,dx=0$ になるのはそのためで、「面積 $=0$」ではない。",
  "ex": r"曲線 $y=x^3-x^2-2x$ と $x$ 軸で囲まれた2つの部分の面積の和を求めよ。",
  "exa": r"$\dfrac{37}{12}$"},
 {"lv": 2, "title": "3次関数のグラフと接線で囲まれた部分",
  "q": r"曲線 $C: y=x^3-4x$ 上の点 $(1,\ -3)$ における接線を $\ell$ とする。$C$ と $\ell$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"「曲線 − 接線」は接点 $x=1$ を重解にもつので $(x-1)^2$ を因数にもつ。残りの因数から、もう1つの交点がわかる。",
  "sol": _f42() +
         r"$y'=3x^2-4$ より、$x=1$ における接線の傾きは $-1$。$\ell: y=-(x-1)-3=-x-2$<br>"
         r"$(x^3-4x)-(-x-2)=x^3-3x+2=(x-1)^2(x+2)$<br>"
         r"よって $C$ と $\ell$ は $x=-2$ でも交わり、$-2\leqq x\leqq1$ で $(x-1)^2(x+2)\geqq0$（$C$ が上）。<br>"
         r"$\displaystyle S=\int_{-2}^{1}(x-1)^2(x+2)\,dx$ で、$x+2=(x-1)+3$ と変形すると<br>"
         r"$\displaystyle S=\int_{-2}^{1}\{(x-1)^3+3(x-1)^2\}\,dx=\Big[\frac{(x-1)^4}4+(x-1)^3\Big]_{-2}^{1}=0-\Big(\frac{81}4-27\Big)=\boldsymbol{\frac{27}4}$",
  "note": r"公式 $\displaystyle\int_\alpha^\beta(x-\alpha)^2(x-\beta)\,dx=-\frac{(\beta-\alpha)^4}{12}$ を使えば $S=\dfrac{\{1-(-2)\}^4}{12}=\dfrac{81}{12}=\dfrac{27}4$。展開して $\Big[\frac{x^4}4-\frac32x^2+2x\Big]_{-2}^{1}=\frac34+6$ としてもよい。",
  "ex": r"曲線 $y=x^3+x^2$ 上の点 $(-1,\ 0)$ における接線と、この曲線で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac43$"},
 {"lv": 3, "title": "2つの部分の面積が等しくなる条件",
  "q": r"曲線 $y=x^3-6x^2+9x$ と直線 $y=mx$ が異なる3点で交わり、曲線と直線で囲まれた2つの部分の面積が等しくなるような定数 $m$ の値を求めよ。",
  "hint": r"3つの交点の $x$ 座標を $p<q<r$ とし、$g(x)$ を「曲線の式 − 直線の式」とすると、2つの部分の面積が等しい $\iff$ $\int_p^r g(x)\,dx=0$（符号つき面積の和が $0$）。この積分を計算すると、条件は「$q$ が $p,\ r$ の中点」になる。",
  "sol": _f43() +
         r"$g(x)=(x^3-6x^2+9x)-mx=x(x^2-6x+9-m)$ とする。異なる3点で交わる条件は、$x^2-6x+9-m=0$ が $0$ 以外の異なる2つの実数解をもつことで、$\dfrac D4=9-(9-m)=m>0$ かつ $9-m\neq0$。このとき2解は $x=3\pm\sqrt m$。<br>"
         r"3つの交点の $x$ 座標を $p<q<r$ とすると $g(x)=(x-p)(x-q)(x-r)$ で、$p\leqq x\leqq q$ で $g(x)\geqq0$，$q\leqq x\leqq r$ で $g(x)\leqq0$。よって<br>"
         r"　面積が等しい $\iff\displaystyle\int_p^q g(x)\,dx=-\int_q^r g(x)\,dx\iff\int_p^r g(x)\,dx=0$<br>"
         r"$d=r-p,\ e=q-p$ とおくと $g(x)=(x-p)\{(x-p)-e\}\{(x-p)-d\}=(x-p)^3-(d+e)(x-p)^2+de(x-p)$ だから<br>"
         r"　$\displaystyle\int_p^r g(x)\,dx=\frac{d^4}4-\frac{(d+e)d^3}3+\frac{de\cdot d^2}2=\frac{d^3(2e-d)}{12}$<br>"
         r"$d>0$ より、条件は $2e=d$，すなわち $q=\dfrac{p+r}2$（真ん中の交点が両端の中点）。<br>"
         r"・$0<m<9$ のとき　$p=0,\ q=3-\sqrt m,\ r=3+\sqrt m$ で、$3-\sqrt m=\dfrac{3+\sqrt m}2$ より $\sqrt m=1$，$m=1$（適する）。<br>"
         r"・$m>9$ のとき　$p=3-\sqrt m<0=q$ で、$q=\dfrac{p+r}2=3$ となり $q=0$ に反する。<br>"
         r"よって　$\boldsymbol{m=1}$",
  "note": r"$m=1$ のとき真ん中の交点は $(2,\ 2)$ で、これはグラフの対称の中心（$x=-\frac{-6}{3}=2$）である。直線が対称の中心を通れば2つの部分は合同になる。上の計算は、その逆も成り立つことを示している。",
  "ex": r"曲線 $y=x^3-3x^2$ と直線 $y=mx$ が異なる3点で交わり、曲線と直線で囲まれた2つの部分の面積が等しくなるような定数 $m$ の値を求めよ。",
  "exa": r"$m=-2$"},
 {"lv": 4, "title": "接線をくり返して引いたときの面積比",
  "q": r"曲線 $C: y=x^3$ 上の点 $\mathrm{P}(t,\ t^3)\ (t\neq0)$ における接線が $C$ と再び交わる点を $\mathrm{Q}$ とする。P における接線と $C$ で囲まれた部分の面積を $S_1$，Q における $C$ の接線と $C$ で囲まれた部分の面積を $S_2$ とするとき、$S_1:S_2$ を求めよ。",
  "hint": r"「曲線 − 接線」は $(x-t)^2(x-u)$ の形になり、$x^2$ の係数（$0$）を比べると $u=-2t$ がすぐわかる。面積は $\frac1{12}|u-t|^4$。",
  "sol": r"$y'=3x^2$ より、P における接線は $y=3t^2(x-t)+t^3=3t^2x-2t^3$。<br>"
         r"$x^3-(3t^2x-2t^3)=(x-t)^2(x+2t)$ より、Q の $x$ 座標は $-2t$（$t\neq0$ より $-2t\neq t$）。<br>"
         r"$-2t$ と $t$ の間で $(x-t)^2(x+2t)$ の符号は一定だから<br>"
         r"　$\displaystyle S_1=\left|\int_{-2t}^{t}(x-t)^2(x+2t)\,dx\right|=\frac{|t-(-2t)|^4}{12}=\frac{81t^4}{12}$<br>"
         r"同様に、$x$ 座標が $s$ の点における接線は $C$ と $x=-2s$ で再び交わる。Q（$s=-2t$）における接線は $x=4t$ で交わるから<br>"
         r"　$S_2=\dfrac{|4t-(-2t)|^4}{12}=\dfrac{1296t^4}{12}$<br>"
         r"よって　$S_1:S_2=81:1296=\boldsymbol{1:16}$",
  "note": r"一般の3次関数 $y=px^3+qx^2+\cdots$ でも、対称の中心の $x$ 座標 $x_0=-\frac q{3p}$ から測ると、接点 $x_0+h$ の接線は $x_0-2h$ で再び交わる。したがって面積比は常に $1:2^4=1:16$ で、$t$ によらない。",
  "ex": r"曲線 $C: y=x^3-3x^2$ 上の点 $\mathrm{P}(3,\ 0)$ における接線が $C$ と再び交わる点を Q とする。P における接線と $C$ で囲まれた部分の面積 $S_1$ と、Q における接線と $C$ で囲まれた部分の面積 $S_2$ を求めよ。",
  "exa": r"$S_1=108$，$S_2=1728$（$S_1:S_2=1:16$）"},
 {"lv": 4, "title": "4次関数のグラフと2点で接する直線",
  "q": r"曲線 $C: y=x^4-2x^2+x$ と異なる2点で接する直線 $\ell$ の方程式を求めよ。また、$C$ と $\ell$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$\ell: y=ax+b$ が $x=\alpha,\ \beta$ で接する $\iff$ $x^4-2x^2+x-(ax+b)=(x-\alpha)^2(x-\beta)^2$ が恒等式。右辺を $(x^2-sx+t)^2$（$s=\alpha+\beta,\ t=\alpha\beta$）として係数を比べる。",
  "sol": _f45() +
         r"$\ell: y=ax+b$ が $C$ と $x=\alpha,\ \beta\ (\alpha\neq\beta)$ で接する条件は<br>"
         r"　$x^4-2x^2+(1-a)x-b=(x-\alpha)^2(x-\beta)^2$（恒等式）<br>"
         r"$s=\alpha+\beta,\ t=\alpha\beta$ とおくと 右辺 $=(x^2-sx+t)^2=x^4-2sx^3+(s^2+2t)x^2-2stx+t^2$。<br>"
         r"係数を比べて　$-2s=0$，$s^2+2t=-2$，$-2st=1-a$，$t^2=-b$<br>"
         r"よって $s=0,\ t=-1,\ a=1,\ b=-1$。$\alpha,\ \beta$ は $x^2-1=0$ の解 $\pm1$ で、確かに異なる。<br>"
         r"したがって　$\boldsymbol{\ell: y=x-1}$<br>"
         r"$C$ と $\ell$ の差は $(x^2-1)^2\geqq0$ なので、$-1\leqq x\leqq1$ で $C$ が上にあり<br>"
         r"$\displaystyle S=\int_{-1}^{1}(x^2-1)^2\,dx=2\int_0^1(x^4-2x^2+1)\,dx=2\Big(\frac15-\frac23+1\Big)=\boldsymbol{\frac{16}{15}}$",
  "note": r"公式 $\int_\alpha^\beta(x-\alpha)^2(x-\beta)^2dx=\frac{(\beta-\alpha)^5}{30}$ で $\frac{2^5}{30}=\frac{16}{15}$ と検算できる（$x-\beta=(x-\alpha)-(\beta-\alpha)$ と変形して示せる）。3次関数のグラフには2点で接する直線は存在しない。",
  "ex": r"曲線 $y=x^4-6x^3+9x^2-x$ と異なる2点で接する直線の方程式を求めよ。また、曲線とこの直線で囲まれた部分の面積を求めよ。",
  "exa": r"$y=-x$，面積 $\dfrac{81}{10}$"},
]})


def _v4():
    F = integrate(x**3-3*x**2+2*x, x)
    assert F.subs(x, 1) == Rational(1, 4) and F.subs(x, 2) == 0
    assert abs(_num_area(lambda u: abs(u*(u-1)*(u-2)), lambda u: 0, 0, 2)-0.5) < 1e-6
    g = x**3-x**2-2*x; assert _eq(g, x*(x+1)*(x-2))
    assert integrate(g, (x, -1, 0))-integrate(g, (x, 0, 2)) == Rational(37, 12)
    # 接線
    assert _eq(x**3-4*x-(-x-2), (x-1)**2*(x+2)) and integrate((x-1)**2*(x+2), (x, -2, 1)) == Rational(27, 4)
    assert _eq(integrate((x-1)**3+3*(x-1)**2, (x, -2, 1)), Rational(27, 4))
    f = x**3+x**2; l = diff(f, x).subs(x, -1)*(x+1)+f.subs(x, -1)
    assert _eq(f-l, (x+1)**2*(x-1)) and integrate(f-l, (x, -1, 1)) == Rational(-4, 3)
    # 等面積
    p_, d_, e_ = symbols("p_ d_ e_")
    gg = (x-p_)*(x-p_-e_)*(x-p_-d_)
    assert _eq(integrate(gg, (x, p_, p_+d_)), d_**3*(2*e_-d_)/12)
    assert _eq(expand((x-p_)**3-(d_+e_)*(x-p_)**2+d_*e_*(x-p_)), expand(gg))
    g = x**3-6*x**2+9*x-x
    assert _eq(g, x*(x-2)*(x-4)) and integrate(g, (x, 0, 2)) == -integrate(g, (x, 2, 4))
    # m の総当たり的確認：m>0, m≠9 の範囲で ∫_p^r g = 0 となる m は 1 だけ
    def bal(mv):
        rts = sorted([0.0, 3-math.sqrt(mv), 3+math.sqrt(mv)])
        P = lambda u: u**4/4-2*u**3+(9-mv)*u**2/2
        return P(rts[2])-P(rts[0])
    sgn = [bal(mv) > 0 for mv in [0.01*i for i in range(1, 3000) if abs(0.01*i-9) > 1e-9]]
    changes = sum(1 for i in range(len(sgn)-1) if sgn[i] != sgn[i+1])
    assert abs(bal(1.0)) < 1e-9 and changes == 1
    g = x**3-3*x**2+2*x
    assert _eq(g, x*(x-1)*(x-2)) and integrate(g, (x, 0, 1)) == -integrate(g, (x, 1, 2))
    def bal2(mv):   # 練習：y=x^3-3x^2 と y=mx（-9/4<m, m≠0）
        dd = math.sqrt(9+4*mv); rts = sorted([0.0, (3-dd)/2, (3+dd)/2])
        P = lambda u: u**4/4-u**3-mv*u**2/2
        return P(rts[2])-P(rts[0])
    ms = [-2.2499+0.005*i for i in range(2500) if abs(-2.2499+0.005*i) > 1e-9]
    sg = [bal2(mv) > 0 for mv in ms]
    assert abs(bal2(-2.0)) < 1e-9 and sum(1 for i in range(len(sg)-1) if sg[i] != sg[i+1]) == 1
    # 1:16
    tt = symbols("tt", positive=True)
    assert _eq(x**3-(3*tt**2*x-2*tt**3), (x-tt)**2*(x+2*tt))
    S1 = integrate((x-tt)**2*(x+2*tt), (x, -2*tt, tt))
    s0 = -2*tt; l2 = 3*s0**2*(x-s0)+s0**3
    assert _eq(x**3-l2, (x-s0)**2*(x-4*tt))
    S2 = integrate((x-s0)**2*(x-4*tt), (x, s0, 4*tt))
    assert _eq(S1, 81*tt**4/12) and _eq(-S2, 1296*tt**4/12) and _eq(S1/(-S2), Rational(1, 16))
    f = x**3-3*x**2
    l1 = diff(f, x).subs(x, 3)*(x-3); assert _eq(f-l1, (x-3)**2*(x+3))
    l2 = diff(f, x).subs(x, -3)*(x+3)+f.subs(x, -3); assert _eq(f-l2, (x+3)**2*(x-9))
    assert abs(integrate(f-l1, (x, -3, 3))) == 108 and abs(integrate(f-l2, (x, -3, 9))) == 1728
    # 4次・2重接線
    aa, bb, ss, tq = symbols("aa bb ss tq")
    eqs = Poly(expand(x**4-2*x**2+(1-aa)*x-bb-(x**2-ss*x+tq)**2), x).all_coeffs()
    assert solve(eqs, [aa, bb, ss, tq], dict=True) == [{aa: 1, bb: -1, ss: 0, tq: -1}]
    assert _eq(x**4-2*x**2+x-(x-1), (x**2-1)**2) and integrate((x**2-1)**2, (x, -1, 1)) == Rational(16, 15)
    al, be = symbols("al be")
    assert _eq(integrate((x-al)**2*(x-be)**2, (x, al, be)), (be-al)**5/30)
    eqs = Poly(expand(x**4-6*x**3+9*x**2-x-aa*x-bb-(x**2-ss*x+tq)**2), x).all_coeffs()
    assert solve(eqs, [aa, bb, ss, tq], dict=True) == [{aa: -1, bb: 0, ss: 3, tq: 0}]
    assert integrate((x*(x-3))**2, (x, 0, 3)) == Rational(81, 10)


# ---------------------------------------------------------------- 節5 の図
def _f51():
    g = _G(170, 120, (-0.4, 3.4), (-0.35, 2.3))
    f = lambda u: abs(u*u-3*u+2)
    g.band(lambda u: 0, f, 0, 3)
    g.axes()
    g.curve(lambda u: u*u-3*u+2, 0.95, 2.05, col=CG, dash=DASH, w=0.9)
    g.curve(f, -0.1, 3.25)
    g.xtick(1, "1"); g.xtick(2, "2"); g.xtick(3, "3")
    g.txt(2.75, 2.05, "y=|x²−3x+2|", anc="end", it=True)
    return g.svg()


def _f52():
    g = _G(180, 130, (-0.4, 3.5), (-0.4, 3.4))
    f = lambda u: abs(u*u-2*u)
    g.band(lambda u: 0, f, 0, 2.6)
    g.axes()
    g.curve(lambda u: u*u-2*u, 0, 2, col=CG, dash=DASH, w=0.9)
    g.curve(f, -0.3, 3.35)
    g.seg((2.6, 0), (2.6, f(2.6)))
    g.xtick(2, "2"); g.txt(2.6, 0, "a", dy=11, it=True)
    g.txt(1, 1, "1", dx=0, dy=-5, size=9, col="#555")
    g.txt(2.7, 2.9, "y=|x²−2x|", anc="end", it=True)
    return g.svg()


# ---------------------------------------------------------------- 節5
SEC.append({"title": "絶対値を含む関数の定積分",
"base": r"""・$|f(x)|$ の定積分は、$f(x)=0$ となる $x$ で区間を分け、$f(x)\geqq0$ の区間では $f(x)$，$f(x)\leqq0$ の区間では $-f(x)$ を積分する<br>
・$\displaystyle\int_a^b|f(x)|\,dx$ は、曲線 $y=f(x)$ と $x$ 軸、2直線 $x=a,\ x=b$ で囲まれた部分の面積に等しい<br>
・$f(x)\leqq0$ となるのが区間 $c\leqq x\leqq d$ だけのときは　$\displaystyle\int_a^b|f(x)|\,dx=\int_a^b f(x)\,dx-2\int_c^d f(x)\,dx$　とすると計算が楽<br>
・文字を含むときは、$f(x)=0$ となる $x$ と積分区間の位置関係で場合分けする""",
"items": [
 {"lv": 2, "title": "絶対値を含む関数の定積分",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^3|x^2-3x+2|\,dx$　　(2) $\displaystyle\int_{-2}^{2}|x^2+x-2|\,dx$",
  "hint": r"絶対値の中身を因数分解して符号の変わる点を求め、区間を分ける。負になる区間の積分は $\frac16$ 公式で求めると速い。",
  "sol": _f51() +
         r"(1) $f(x)=x^2-3x+2=(x-1)(x-2)$ は、$1\leqq x\leqq2$ で $f(x)\leqq0$，それ以外の区間では $f(x)\geqq0$。よって<br>"
         r"$\displaystyle\int_0^3|f(x)|\,dx=\int_0^3 f(x)\,dx-2\int_1^2 f(x)\,dx$<br>"
         r"$\displaystyle\int_0^3f(x)\,dx=9-\frac{27}2+6=\frac32$，$\displaystyle\int_1^2f(x)\,dx=-\frac{(2-1)^3}6=-\frac16$ だから<br>"
         r"　与式 $=\dfrac32+\dfrac13=\boldsymbol{\dfrac{11}6}$<br>"
         r"(2) $x^2+x-2=(x+2)(x-1)$ は、$-2\leqq x\leqq1$ で $\leqq0$，$1\leqq x\leqq2$ で $\geqq0$。<br>"
         r"$\displaystyle\int_{-2}^{1}\{-(x^2+x-2)\}\,dx=\frac{\{1-(-2)\}^3}6=\frac92$<br>"
         r"$\displaystyle\int_1^2(x^2+x-2)\,dx=\Big[\frac{x^3}3+\frac{x^2}2-2x\Big]_1^2=\frac23-\Big(-\frac76\Big)=\frac{11}6$<br>"
         r"よって　与式 $=\dfrac92+\dfrac{11}6=\boldsymbol{\dfrac{19}3}$",
  "note": r"(1) の変形は、$|f|=f-2f$（$f\leqq0$ の区間）であることによる。$\int_0^3|f(x)|\,dx$ はグラフ $y=|f(x)|$（$x$ 軸より下の部分を折り返したもの）と $x$ 軸の間の面積で、右図の色の部分にあたる。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-1}^{2}|x^2-1|\,dx$　　(2) $\displaystyle\int_0^3|x^2-4|\,dx$",
  "exa": r"(1) $\dfrac83$　(2) $\dfrac{23}{3}$"},
 {"lv": 3, "title": "上端に文字を含む絶対値の定積分",
  "q": r"$a>0$ とし、$S(a)=\displaystyle\int_0^a|x^2-2x|\,dx$ とする。<br>(1) $S(a)$ を $a$ の式で表せ。　(2) $S(a)=\dfrac83$ となる $a$ の値を求めよ。",
  "hint": r"$x^2-2x$ の符号は $x=2$ で変わる。上端 $a$ が $2$ より小さいか大きいかで場合分けする。",
  "sol": _f52() +
         r"(1) $0\leqq x\leqq2$ で $|x^2-2x|=2x-x^2$，$x\geqq2$ で $|x^2-2x|=x^2-2x$。<br>"
         r"(i) $0<a\leqq2$ のとき　$\displaystyle S(a)=\int_0^a(2x-x^2)\,dx=\boldsymbol{a^2-\frac{a^3}3}$<br>"
         r"(ii) $a>2$ のとき<br>"
         r"　$\displaystyle S(a)=\int_0^2(2x-x^2)\,dx+\int_2^a(x^2-2x)\,dx=\frac43+\Big[\frac{x^3}3-x^2\Big]_2^a=\boldsymbol{\frac{a^3}3-a^2+\frac83}$<br>"
         r"(2) 被積分関数は $0$ 以上なので、$S(a)$ は $a$ について増加する。(i) では $S(a)\leqq S(2)=\dfrac43<\dfrac83$ だから $a>2$ で<br>"
         r"　$\dfrac{a^3}3-a^2+\dfrac83=\dfrac83$　より　$a^2(a-3)=0$<br>"
         r"$a>2$ より　$\boldsymbol{a=3}$",
  "note": r"(i)(ii) の式は $a=2$ でともに $\frac43$ となりつながっている（検算に使える）。$S'(a)=|a^2-2a|$ となることも確かめてみよう。",
  "ex": r"$a>0$ とし、$S(a)=\displaystyle\int_0^a|x^2-1|\,dx$ とする。$S(a)$ を $a$ の式で表し、$S(a)=2$ となる $a$ の値を求めよ。",
  "exa": r"$0<a\leqq1$ のとき $a-\dfrac{a^3}3$，$a>1$ のとき $\dfrac{a^3}3-a+\dfrac43$；$a=2$"},
 {"lv": 4, "title": "絶対値を含む定積分で表された関数の最小値",
  "q": r"実数 $a$ に対して $F(a)=\displaystyle\int_0^1|x^2-ax|\,dx$ とする。$F(a)$ を $a$ の式で表し、$F(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "hint": r"$x^2-ax=x(x-a)$ の符号が変わる点 $x=a$ が、積分区間 $0\leqq x\leqq1$ の左にあるか、中にあるか、右にあるかで場合分けする。",
  "sol": r"(i) $a\leqq0$ のとき　$0\leqq x\leqq1$ で $x(x-a)\geqq0$ だから　$F(a)=\displaystyle\int_0^1(x^2-ax)\,dx=\frac13-\frac a2$<br>"
         r"(ii) $0<a<1$ のとき　$0\leqq x\leqq a$ で $x(x-a)\leqq0$，$a\leqq x\leqq1$ で $\geqq0$ だから<br>"
         r"　$\displaystyle F(a)=\int_0^1(x^2-ax)\,dx-2\int_0^a(x^2-ax)\,dx=\frac13-\frac a2-2\Big(-\frac{a^3}6\Big)=\frac{a^3}3-\frac a2+\frac13$<br>"
         r"(iii) $a\geqq1$ のとき　$0\leqq x\leqq1$ で $x(x-a)\leqq0$ だから　$F(a)=\dfrac a2-\dfrac13$<br>"
         r"(i) で $F(a)$ は減少、(iii) で増加。(ii) では $F'(a)=a^2-\dfrac12$ だから、$a=\dfrac1{\sqrt2}$ で減少から増加に変わる。<br>"
         + _tb([r"$a$", r"$\cdots$", r"$0$", r"$\cdots$", r"$\frac1{\sqrt2}$", r"$\cdots$", r"$1$", r"$\cdots$"],
               [r"$F(a)$", DN, r"$\frac13$", DN, r"$\frac{2-\sqrt2}6$", UP, r"$\frac16$", UP]) +
         r"$F\Big(\dfrac1{\sqrt2}\Big)=\dfrac13\cdot\dfrac1{2\sqrt2}-\dfrac1{2\sqrt2}+\dfrac13=\dfrac13-\dfrac1{3\sqrt2}=\dfrac{2-\sqrt2}6$<br>"
         r"よって　$a=\dfrac{\sqrt2}2$ のとき　<b>最小値</b> $\boldsymbol{\dfrac{2-\sqrt2}6}$",
  "note": r"$F(a)$ は $a=0,\ 1$ でもつながっている（$\frac13,\ \frac16$）。(ii) の $F'(a)=a^2-\frac12=\int_0^ax\,dx-\int_a^1x\,dx$ と書けるので、最小となる $a$ は「$x$ の重みで測った左右の釣り合いの位置」になる。",
  "ex": r"$a\geqq0$ に対して $G(a)=\displaystyle\int_0^2|x^2-a^2|\,dx$ とする。$G(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "exa": r"最小値 $2$（$a=1$）"},
 {"lv": 5, "title": "絶対値の定積分の最小値（符号関数による評価）",
  "q": r"$a,\ b$ が実数全体を動くとき、$I(a,\ b)=\displaystyle\int_{-1}^{1}|x^2+ax+b|\,dx$ の最小値を求めよ。",
  "hint": r"最小を与える関数は対称性から $x^2-c$ の形と予想され、さらに「正の区間と負の区間の長さがつり合う」と考えると $x^2-\frac14$（符号は $x=\pm\frac12$ で変わる）が候補。証明は、$|g(x)|\geqq s(x)g(x)$（$s(x)=\pm1$）を使って下から評価する。$s(x)$ をうまく選ぶと $a,\ b$ が消える。",
  "sol": r"$g(x)=x^2+ax+b$ とし、$-1\leqq x\leqq1$ で<br>"
         r"　$s(x)=1\ \Big(\dfrac12\leqq|x|\leqq1\Big)$，$s(x)=-1\ \Big(|x|<\dfrac12\Big)$<br>"
         r"と定める。各 $x$ で $|g(x)|\geqq s(x)g(x)$ だから<br>"
         r"　$\displaystyle I(a,\ b)\geqq\int_{-1}^{-\frac12}g(x)\,dx-\int_{-\frac12}^{\frac12}g(x)\,dx+\int_{\frac12}^{1}g(x)\,dx$　…①<br>"
         r"①の右辺を項ごとに計算する。区間 $\Big[-1,\ -\dfrac12\Big]$ と $\Big[\dfrac12,\ 1\Big]$ は原点に関して対称なので、$x$ の項は打ち消し合い、<br>"
         r"　$x^2$ の項：$\displaystyle2\int_{\frac12}^1x^2dx-\int_{-\frac12}^{\frac12}x^2dx=2\cdot\frac{7}{24}-\frac1{12}=\frac12$<br>"
         r"　$x$ の項：$\displaystyle a\Big(\int_{-1}^{-\frac12}x\,dx+\int_{\frac12}^{1}x\,dx-\int_{-\frac12}^{\frac12}x\,dx\Big)=a(0-0)=0$<br>"
         r"　定数項：$b\Big(\dfrac12+\dfrac12-1\Big)=0$<br>"
         r"よって、すべての $a,\ b$ について　$I(a,\ b)\geqq\dfrac12$。<br>"
         r"一方、$a=0,\ b=-\dfrac14$ のとき $g(x)=x^2-\dfrac14$ は $\dfrac12\leqq|x|\leqq1$ で $g\geqq0$，$|x|<\dfrac12$ で $g<0$ なので $|g(x)|=s(x)g(x)$ が常に成り立ち、①は等号になる。すなわち $I\Big(0,\ -\dfrac14\Big)=\dfrac12$。<br>"
         r"以上より　<b>最小値</b> $\boldsymbol{\dfrac12}$",
  "note": r"$a,\ b$ の2変数で場合分けして $I(a,\ b)$ を直接計算するのは非常に大変。「$|A|\geqq\pm A$ を区間ごとに使い分けると、$1$ と $x$ の積分が $0$ になるように符号を選べる」のが鍵。等号は $g(\pm\frac12)=0$ のときに限るので、最小を与える $g$ は $x^2-\frac14$ だけである。",
  "ex": r"$a,\ b$ が実数全体を動くとき、$\displaystyle\int_0^1|x^2+ax+b|\,dx$ の最小値を求めよ。",
  "exa": r"$\dfrac1{16}$（$x^2-x+\dfrac3{16}$ のとき。符号が $x=\frac14,\ \frac34$ で変わる関数 $s(x)$ を掛けて評価する）"},
]})


def _absint(coeffs, lo, hi):
    """∫_lo^hi |poly| を、根で区間を分けて厳密に（sympy）計算する。coeffs は x の式。"""
    f = coeffs
    rts = sorted([r_ for r_ in solve(f, x) if r_.is_real and lo < r_ < hi], key=lambda v: float(v))
    pts = [lo]+rts+[hi]
    return sum(Abs(integrate(f, (x, pts[i], pts[i+1]))) for i in range(len(pts)-1))


def _v5():
    assert _absint(x**2-3*x+2, 0, 3) == Rational(11, 6)
    assert integrate(x**2-3*x+2, (x, 0, 3)) == Rational(3, 2) and integrate(x**2-3*x+2, (x, 1, 2)) == Rational(-1, 6)
    assert _absint(x**2+x-2, -2, 2) == Rational(19, 3)
    assert integrate(x**2+x-2, (x, 1, 2)) == Rational(11, 6)
    assert _absint(x**2-1, -1, 2) == Rational(8, 3) and _absint(x**2-4, 0, 3) == Rational(23, 3)
    # S(a)
    for av in map(Rational, ["1/2", "3/2", "2", "5/2", "3", "4"]):
        val = _absint(x**2-2*x, 0, av)
        ex_ = av**2-av**3/3 if av <= 2 else av**3/3-av**2+Rational(8, 3)
        assert val == ex_
        val = _absint(x**2-1, 0, av)
        ex_ = av-av**3/3 if av <= 1 else av**3/3-av+Rational(4, 3)
        assert val == ex_
    assert _absint(x**2-2*x, 0, 3) == Rational(8, 3) and _absint(x**2-1, 0, 2) == 2
    assert solve(a**3/3-a**2, a) == [0, 3] and _eq(factor(a**3-3*a-2), (a-2)*(a+1)**2)
    # F(a)=∫_0^1|x^2-ax|
    for av in map(Rational, ["-2", "-1", "0", "1/3", "1/2", "3/4", "1", "2"]):
        val = _absint(x**2-av*x, 0, 1)
        ex_ = Rational(1, 3)-av/2 if av <= 0 else (av**3/3-av/2+Rational(1, 3) if av < 1 else av/2-Rational(1, 3))
        assert val == ex_
    Fm = (a**3/3-a/2+Rational(1, 3)).subs(a, 1/sqrt(2)); assert _eq(Fm, (2-sqrt(2))/6)
    fl = lambda av: sum(abs((((i+0.5)/4000)**2-av*(i+0.5)/4000))/4000 for i in range(4000))
    vals = [(fl(av), av) for av in [i/200 for i in range(-200, 401)]]
    mn = min(vals); assert abs(mn[0]-float(Fm)) < 1e-4 and abs(mn[1]-1/math.sqrt(2)) < 0.01
    # G(a)=∫_0^2|x^2-a^2|
    for av in map(Rational, ["0", "1/2", "1", "3/2", "2", "3"]):
        val = _absint(x**2-av**2, 0, 2)
        ex_ = Rational(4, 3)*av**3-2*av**2+Rational(8, 3) if av <= 2 else 2*av**2-Rational(8, 3)
        assert val == ex_
    gl = lambda av: sum(abs(((i+0.5)/2000)**2-av*av)*2/4000 for i in range(4000))
    vals = [(gl(av), av) for av in [i/100 for i in range(0, 301)]]
    mn = min(vals); assert abs(mn[0]-2) < 1e-4 and abs(mn[1]-1) < 0.011
    # L1 最小（例題）
    sfun = lambda u: 1 if abs(u) >= Rational(1, 2) else -1
    I2 = 2*integrate(x**2, (x, Rational(1, 2), 1))-integrate(x**2, (x, -Rational(1, 2), Rational(1, 2)))
    assert integrate(x**2, (x, Rational(1, 2), 1)) == Rational(7, 24) and I2 == Rational(1, 2)
    I1 = integrate(x, (x, -1, -Rational(1, 2)))+integrate(x, (x, Rational(1, 2), 1))-integrate(x, (x, -Rational(1, 2), Rational(1, 2)))
    I0 = Rational(1, 2)+Rational(1, 2)-1
    assert I1 == 0 and I0 == 0
    assert _absint(x**2-Rational(1, 4), -1, 1) == Rational(1, 2)
    rnd = random.Random(15)
    def L1(av, bv, lo, hi, n=3000):
        h = (hi-lo)/n
        return sum(abs((lo+(i+0.5)*h)**2+av*(lo+(i+0.5)*h)+bv)*h for i in range(n))
    for _ in range(300):
        av, bv = rnd.uniform(-3, 3), rnd.uniform(-3, 3)
        assert L1(av, bv, -1, 1) >= 0.5-1e-5
    for da in (-0.01, 0, 0.01):
        for db in (-0.01, 0, 0.01):
            assert L1(da, -0.25+db, -1, 1) >= L1(0, -0.25, -1, 1)-1e-9
    # 練習：∫_0^1、s=+1 on [0,1/4]∪[3/4,1]
    q1, q3 = Rational(1, 4), Rational(3, 4)
    J = lambda f: integrate(f, (x, 0, q1))-integrate(f, (x, q1, q3))+integrate(f, (x, q3, 1))
    assert J(1) == 0 and J(x) == 0 and J(x**2) == Rational(1, 16)
    assert _eq(expand((x-q1)*(x-q3)), x**2-x+Rational(3, 16)) and _absint(x**2-x+Rational(3, 16), 0, 1) == Rational(1, 16)
    for _ in range(300):
        av, bv = rnd.uniform(-3, 2), rnd.uniform(-1.5, 1.5)
        assert L1(av, bv, 0, 1) >= 1/16-1e-5


# ---------------------------------------------------------------- 節6 の図
def _f62():
    a0 = 0.58
    g = _G(150, 130, (-0.25, 1.3), (-0.12, 1.15))
    f = lambda u: u*u
    g.band(f, lambda u: a0*a0, 0, a0)
    g.band(lambda u: a0*a0, f, a0, 1)
    g.axes()
    g.curve(f, 0, 1.05)
    g.seg((0, a0*a0), (1.2, a0*a0), col=C2, dash="", w=1.2)
    g.seg((1, 0), (1, 1), col="#555", dash="")
    g.seg((a0, 0), (a0, a0*a0))
    g.xtick(a0, "a", dy=11); g.xtick(1, "1")
    g.txt(0, a0*a0, "a²", dx=-3, dy=4, anc="end", size=9)
    g.txt(0.62, 1.0, "y=x²", anc="end", it=True)
    return g.svg()


def _f64():
    k0 = 38-27*math.sqrt(2)
    al0 = 3*math.sqrt(2)-3
    g = _G(200, 140, (-0.3, 2.45), (-0.62, 0.62))
    f, l = (lambda u: u**3-3*u*u+2*u), (lambda u: k0*u)
    g.band(l, f, 0, al0)
    g.band(f, l, al0, 3-al0)
    g.axes()
    g.curve(f, -0.12, 2.4)
    g.curve(l, -0.3, 2.45, col=C2)
    g.seg((al0, 0), (al0, l(al0))); g.seg((3-al0, 0), (3-al0, l(3-al0)))
    g.txt(al0, 0, "α", dx=-2, dy=-4, it=True)
    g.txt(3-al0, 0, "β", dx=2, dy=-4, it=True)
    g.txt(2.42, -0.53, "ℓ", anc="end", it=True, col=C2)
    g.txt(2.3, 0.45, "C", anc="end", it=True)
    return g.svg()


def _f65():
    g = _G(210, 150, (-1.35, 1.35), (-0.22, 1.32), eq=True)
    def hi(u):
        if u <= -0.5:
            return -u
        if u <= 0.5:
            return u*u+0.25
        return u
    g.band(lambda u: u*u, hi, -1, 1)
    g.axes()
    for p in (-0.8, -0.6, -0.35, -0.15):
        g.seg((p, p*p), (p+1, (p+1)**2), col="#7f8fb3", dash="", w=0.6)
    g.curve(lambda u: u*u+0.25, -0.75, 0.75, col=CG, dash=DASH, w=0.9)
    g.curve(lambda u: u*u, -1.15, 1.15)
    g.seg((-1, 1), (0, 0), col=C2, dash="", w=1.2)
    g.seg((0, 0), (1, 1), col=C2, dash="", w=1.2)
    g.pt(-1, 1); g.pt(1, 1)
    g.xtick(-1, "−1"); g.xtick(1, "1")
    g.txt(0.78, 0.86, "y=x²+¼", anc="end", it=True, size=9, col="#555")
    g.txt(1.12, 1.18, "C", anc="start", it=True)
    return g.svg()


# ---------------------------------------------------------------- 節6
SEC.append({"title": "面積の最大・最小",
"base": r"""・面積を1つの文字（直線の傾き・接点や交点の $x$ 座標など）の関数で表し、平方完成や微分で最大・最小を調べる<br>
・交点の $x$ 座標 $\alpha,\ \beta$ が求めにくいときは、$(\beta-\alpha)^2=(\alpha+\beta)^2-4\alpha\beta$（判別式 $D$ を使えば $\beta-\alpha=\frac{\sqrt D}{|p|}$）<br>
・どの文字を変数にとるかで計算量が大きく変わる。根号が出る文字より、交点の座標などを変数にすると整式で表せることが多い<br>
・文字の動く範囲（交わる条件・接する条件）を必ず押さえる""",
"items": [
 {"lv": 3, "title": "定点を通る直線と放物線で囲まれた面積の最小",
  "q": r"点 $(1,\ 3)$ を通る傾き $m$ の直線と、放物線 $y=x^2$ で囲まれた部分の面積を $S(m)$ とする。$S(m)$ の最小値と、そのときの $m$ の値を求めよ。",
  "hint": r"交点の $x$ 座標を $\alpha,\ \beta$ とすると $S=\frac16(\beta-\alpha)^3$。$\beta-\alpha$ は判別式 $D$ を使って $\sqrt D$ と表せるので、$D$ の最小を考えればよい。",
  "sol": r"直線の方程式は $y=m(x-1)+3$。放物線と連立して　$x^2-mx+m-3=0$　…①<br>"
         r"①の判別式は　$D=m^2-4(m-3)=m^2-4m+12=(m-2)^2+8>0$<br>"
         r"なので、どんな $m$ に対しても直線と放物線は2点で交わる。その $x$ 座標を $\alpha,\ \beta\ (\alpha<\beta)$ とすると $\beta-\alpha=\sqrt D$ で<br>"
         r"　$S(m)=\dfrac{(\beta-\alpha)^3}6=\dfrac{D\sqrt D}6$<br>"
         r"$D\geqq8$（等号は $m=2$）で、$S$ は $D$ について増加するから、$m=2$ のとき最小で<br>"
         r"　<b>最小値</b> $\dfrac{8\sqrt8}6=\boldsymbol{\dfrac{8\sqrt2}3}$（$\boldsymbol{m=2}$）",
  "note": r"点 $(1,\ 3)$ は放物線の内側（$3>1^2$）にあるので、どの直線も2点で交わる。最小を与える傾き $m=2$ は放物線の $x=1$ における接線の傾きと等しく、このとき点 $(1,\ 3)$ は弦の中点になっている。",
  "ex": r"点 $(2,\ 1)$ を通る直線と放物線 $y=x^2-2x$ で囲まれた部分の面積の最小値と、そのときの直線の傾きを求めよ。",
  "exa": r"最小値 $\dfrac43$（傾き $2$）"},
 {"lv": 3, "title": "2つの部分の面積の和の最小",
  "q": r"$0<a<1$ とする。曲線 $y=x^2\ (0\leqq x\leqq1)$ と、直線 $y=a^2$，$y$ 軸，直線 $x=1$ で囲まれた2つの部分の面積の和 $S(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "hint": r"曲線と直線 $y=a^2$ の交点は $x=a$。$0\leqq x\leqq a$ では直線が上、$a\leqq x\leqq1$ では曲線が上。$S(a)$ は $a$ の3次式になる。",
  "sol": _f62() +
         r"曲線と直線 $y=a^2$ は $x=a$ で交わる（右図）。<br>"
         r"$\displaystyle S(a)=\int_0^a(a^2-x^2)\,dx+\int_a^1(x^2-a^2)\,dx$<br>"
         r"$=\Big(a^3-\dfrac{a^3}3\Big)+\Big\{\dfrac13-a^2-\Big(\dfrac{a^3}3-a^3\Big)\Big\}=\dfrac43a^3-a^2+\dfrac13$<br>"
         r"$S'(a)=4a^2-2a=2a(2a-1)$ より、$0<a<\dfrac12$ で減少、$\dfrac12<a<1$ で増加。<br>"
         r"よって $a=\dfrac12$ のとき最小で　<b>最小値</b> $S\Big(\dfrac12\Big)=\dfrac16-\dfrac14+\dfrac13=\boldsymbol{\dfrac14}$",
  "note": r"これは $\int_0^1|x^2-a^2|\,dx$ の最小を求めることと同じ。$S'(a)=2a\{a-(1-a)\}$ と書けるので、最小のとき「曲線が直線より下にある区間の長さ $a$」と「上にある区間の長さ $1-a$」が等しい。",
  "ex": r"$0<t<1$ とする。曲線 $y=x^3\ (0\leqq x\leqq1)$ と、直線 $y=t$，$y$ 軸，直線 $x=1$ で囲まれた2つの部分の面積の和の最小値と、そのときの $t$ の値を求めよ。",
  "exa": r"最小値 $\dfrac7{32}$（$t=\dfrac18$）"},
 {"lv": 4, "title": "弦の長さが一定のときの面積の最大",
  "q": r"放物線 $y=x^2$ 上の2点 A，B が $\mathrm{AB}=2$ を満たしながら動くとき、線分 AB と放物線で囲まれた部分の面積 $S$ の最大値を求めよ。",
  "hint": r"A, B の $x$ 座標を $\alpha<\beta$ とすると $S=\frac16(\beta-\alpha)^3$。条件 $\mathrm{AB}=2$ を $\beta-\alpha$ と $\alpha+\beta$ で表すと、$\beta-\alpha$ の最大値がわかる。",
  "sol": r"$\mathrm{A}(\alpha,\ \alpha^2)$，$\mathrm{B}(\beta,\ \beta^2)$ $(\alpha<\beta)$ とする。直線 AB は $y=(\alpha+\beta)x-\alpha\beta$ で、$(\alpha+\beta)x-\alpha\beta-x^2=-(x-\alpha)(x-\beta)$ だから<br>"
         r"　$S=\dfrac{(\beta-\alpha)^3}6$<br>"
         r"また　$\mathrm{AB}^2=(\beta-\alpha)^2+(\beta^2-\alpha^2)^2=(\beta-\alpha)^2\{1+(\alpha+\beta)^2\}=4$<br>"
         r"よって　$(\beta-\alpha)^2=\dfrac4{1+(\alpha+\beta)^2}\leqq4$，すなわち $\beta-\alpha\leqq2$<br>"
         r"等号は $\alpha+\beta=0$，つまり $\alpha=-1,\ \beta=1$ のとき成り立つ（このとき確かに $\mathrm{AB}=2$）。<br>"
         r"したがって　<b>最大値</b> $\dfrac{2^3}6=\boldsymbol{\dfrac43}$",
  "note": r"弦の長さが同じでも、弦の傾きが急になるほど $\beta-\alpha$ は小さくなり面積も小さい。$\alpha+\beta$ を大きくすると $S$ はいくらでも $0$ に近づくので、最小値は存在しない。",
  "ex": r"放物線 $y=x^2$ 上の2点 A，B が $\mathrm{AB}=2\sqrt2$ を満たしながら動くとき、線分 AB と放物線で囲まれた部分の面積の最大値を求めよ。",
  "exa": r"$\dfrac{8\sqrt2}{3}$"},
 {"lv": 5, "title": "3次関数と直線で囲まれた2つの部分の面積の和の最小",
  "q": r"曲線 $C: y=x^3-3x^2+2x$ と直線 $\ell: y=kx$ が、原点以外の異なる2点で交わり、その2点の $x$ 座標がともに正であるとする。$C$ と $\ell$ で囲まれた2つの部分の面積の和を $S$ とするとき、$S$ を最小にする $k$ の値と、$S$ の最小値を求めよ。",
  "hint": r"$k$ を変数にすると交点の座標に根号が入る。交点の $x$ 座標の小さい方 $\alpha$ を変数にとると、$k$ も $S$ も $\alpha$ の整式になる。面積の和は $2\int_0^\alpha g\,dx-\int_0^\beta g\,dx$ と符号つきの積分で書ける。",
  "sol": _f64() +
         r"$g(x)=x^3-3x^2+(2-k)x=x\{x^2-3x+(2-k)\}$。$x^2-3x+2-k=0$ の2解を $\alpha,\ \beta\ (0<\alpha<\beta)$ とすると、$\alpha+\beta=3$，$\alpha\beta=2-k$。<br>"
         r"よって $0<\alpha<\dfrac32$，$\beta=3-\alpha$，$k=2-\alpha(3-\alpha)=\alpha^2-3\alpha+2$ で、逆に $0<\alpha<\dfrac32$ の各 $\alpha$ に対して条件を満たす $k$ がただ1つ定まる。<br>"
         r"$g(x)=x(x-\alpha)(x-\beta)$ は $0\leqq x\leqq\alpha$ で $g\geqq0$，$\alpha\leqq x\leqq\beta$ で $g\leqq0$。<br>"
         r"$g(x)=x^3-3x^2+\alpha\beta x$ なので、$\displaystyle G(u)=\int_0^ug(x)\,dx=\frac{u^4}4-u^3+\frac{\alpha\beta}2u^2$ とおくと<br>"
         r"　$\displaystyle S=\int_0^\alpha g\,dx-\int_\alpha^\beta g\,dx=2G(\alpha)-G(\beta)$<br>"
         r"$\alpha\beta=(3-\alpha)\alpha$ を用いて　$G(\alpha)=\dfrac{\alpha^4}4-\alpha^3+\dfrac{(3-\alpha)\alpha^3}2=\dfrac{\alpha^3(2-\alpha)}4$<br>"
         r"同様に（$\alpha\beta=(3-\beta)\beta$ を用いて）$G(\beta)=\dfrac{\beta^3(2-\beta)}4=\dfrac{(3-\alpha)^3(\alpha-1)}4$。よって<br>"
         r"　$S=\dfrac{2\alpha^3(2-\alpha)-(3-\alpha)^3(\alpha-1)}4=-\dfrac14(\alpha^4+6\alpha^3-36\alpha^2+54\alpha-27)$<br>"
         r"　$\dfrac{dS}{d\alpha}=-\dfrac14(4\alpha^3+18\alpha^2-72\alpha+54)=-\dfrac12(2\alpha-3)(\alpha^2+6\alpha-9)$<br>"
         r"$0<\alpha<\dfrac32$ では $2\alpha-3<0$ なので、$\dfrac{dS}{d\alpha}$ の符号は $\alpha^2+6\alpha-9$ と同じ。$\alpha^2+6\alpha-9=0$ の正の解 $\alpha_0=3\sqrt2-3\ (\fallingdotseq1.24)$ は $0<\alpha_0<\dfrac32$ を満たし、<br>"
         + _tb([r"$\alpha$", r"$(0)$", r"$\cdots$", r"$\alpha_0$", r"$\cdots$", r"$\left(\frac32\right)$"],
               [r"$\frac{dS}{d\alpha}$", "", r"$-$", r"$0$", r"$+$", ""],
               [r"$S$", "", DN, "最小", UP, ""]) +
         r"$\alpha_0^2=9-6\alpha_0$ より $\alpha_0^4+6\alpha_0^3=\alpha_0^2(\alpha_0^2+6\alpha_0)=9\alpha_0^2$ だから<br>"
         r"　$S=-\dfrac14(-27\alpha_0^2+54\alpha_0-27)=\dfrac{27}4(\alpha_0-1)^2=\dfrac{27}4(3\sqrt2-4)^2=\dfrac{27}4(34-24\sqrt2)$<br>"
         r"また　$k=\alpha_0^2-3\alpha_0+2=(9-6\alpha_0)-3\alpha_0+2=11-9\alpha_0=38-27\sqrt2$<br>"
         r"よって　$\boldsymbol{k=38-27\sqrt2}$ のとき　<b>最小値</b> $\boldsymbol{\dfrac{27(17-12\sqrt2)}2}$",
  "note": r"$k$ の範囲は $-\frac14<k<2$ で、$k=38-27\sqrt2\fallingdotseq-0.18$ はその内部にある。$k\to-\frac14$（$\alpha\to\frac32$，右の部分が消える）のとき $S\to\frac{27}{64}$ で、最小値 $\fallingdotseq0.397$ より大きい。「一方の部分が消えるときが最小」という直感は誤り。極値の値を求めるときは $\alpha_0$ の満たす2次方程式で次数を下げる。",
  "ex": r"$0<a<1$ とする。曲線 $y=x(x-a)(x-1)$ と $x$ 軸で囲まれた2つの部分の面積の和 $S(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "exa": r"最小値 $\dfrac1{32}$（$a=\dfrac12$）"},
 {"lv": 5, "title": "弦が通過する範囲の面積",
  "q": r"放物線 $C: y=x^2$ 上の2点 P，Q（P の $x$ 座標は Q の $x$ 座標より小さい）を、線分 PQ と $C$ で囲まれた部分の面積が $\dfrac16$ となるように動かす。P の $x$ 座標が $-1$ 以上 $0$ 以下の範囲を動くとき、線分 PQ が通過する範囲の面積 $T$ を求めよ。",
  "hint": r"面積の条件から Q の $x$ 座標は $p+1$。線分上の点 $(X,\ Y)$ の $X$ を固定すると、$Y$ は $p$ の2次関数で、$p$ の動く範囲は $X$ によって変わる。各 $X$ ごとに $Y$ のとり得る値の範囲（$p$ の2次関数の値域）を求める。",
  "sol": _f65() +
         r"$\mathrm{P}(p,\ p^2)$，$\mathrm{Q}(q,\ q^2)$ $(p<q)$ とする。直線 PQ は $y=(p+q)x-pq$ で、線分 PQ と $C$ で囲まれた部分の面積は $\dfrac{(q-p)^3}6$。これが $\dfrac16$ だから $q=p+1$。よって線分 PQ は<br>"
         r"　$y=(2p+1)x-p(p+1)$　$(p\leqq x\leqq p+1)$，　$-1\leqq p\leqq0$<br>"
         r"点 $(X,\ Y)$ が通過範囲に属する $\iff$ $\max(-1,\ X-1)\leqq p\leqq\min(0,\ X)$ を満たす $p$ で $Y=h(p)$ となるものが存在する。ここで<br>"
         r"　$h(p)=(2p+1)X-p^2-p=-\Big\{p-\Big(X-\dfrac12\Big)\Big\}^2+X^2+\dfrac14$<br>"
         r"$p$ の範囲が空でないのは $-1\leqq X\leqq1$ のときで、$Y$ の範囲はその範囲での $h(p)$ の最小値から最大値までである。$h(X)=h(X-1)=X^2$，$h(-1)=-X$，$h(0)=X$ に注意する。<br>"
         r"(i) $-1\leqq X\leqq0$ のとき　$p$ の範囲は $-1\leqq p\leqq X$ で、端での値は $-X$ と $X^2$（$X^2\leqq-X$）。<br>"
         r"　・$-\frac12\leqq X\leqq0$：軸 $p=X-\frac12$ が範囲内にあり　$X^2\leqq Y\leqq X^2+\frac14$<br>"
         r"　・$-1\leqq X\leqq-\frac12$：軸が範囲の左にあり $h$ は減少するから　$X^2\leqq Y\leqq-X$<br>"
         r"(ii) $0\leqq X\leqq1$ のとき　$p$ の範囲は $X-1\leqq p\leqq0$ で、端での値は $X^2$ と $X$（$X^2\leqq X$）。<br>"
         r"　・$0\leqq X\leqq\frac12$：$X^2\leqq Y\leqq X^2+\frac14$　　・$\frac12\leqq X\leqq1$：$h$ は増加し　$X^2\leqq Y\leqq X$<br>"
         r"通過範囲は右図の色の部分で、$y$ 軸に関して対称だから<br>"
         r"　$\displaystyle T=2\Big\{\int_0^{\frac12}\frac14\,dx+\int_{\frac12}^1(x-x^2)\,dx\Big\}=2\Big(\frac18+\frac1{12}\Big)=\boldsymbol{\frac5{12}}$",
  "note": r"境界の一部 $y=x^2+\frac14$ は、すべての直線 PQ が接する放物線である（$x^2+\frac14-\{(2p+1)x-p^2-p\}=\big(x-p-\frac12\big)^2$）。$p$ を固定して線分を描くのではなく、$x$ を固定して $p$ を動かすのが通過範囲の定石。端の線分（$p=-1,\ 0$）と接する放物線の切り替わりを見落とさないこと。",
  "ex": r"$t$ が $0\leqq t\leqq1$ の範囲を動くとき、放物線 $y=x^2$ と直線 $y=2tx-t^2+1$ で囲まれた部分が通過する範囲の面積を求めよ。",
  "exa": r"$\dfrac73$"},
]})


def _v6():
    # 定点を通る直線
    D = expand(m**2-4*(m-3)); assert _eq(D, (m-2)**2+8)
    Sm = lambda mv: (mv*mv-4*mv+12)**1.5/6
    vals = [(Sm(i/100), i/100) for i in range(-500, 901)]
    mn = min(vals); assert abs(mn[0]-8*math.sqrt(2)/3) < 1e-9 and mn[1] == 2
    r_ = solve(x**2-2*x-(2*(x-2)+1), x); assert _eq(integrate(2*(x-2)+1-(x**2-2*x), (x, min(r_), max(r_))), Rational(4, 3))
    D2 = expand((2+m)**2-4*(2*m-1)); assert _eq(D2, (m-2)**2+4)
    # 2部分の和
    S = integrate(a**2-x**2, (x, 0, a))+integrate(x**2-a**2, (x, a, 1))
    assert _eq(S, Rational(4, 3)*a**3-a**2+Rational(1, 3)) and S.subs(a, Rational(1, 2)) == Rational(1, 4)
    vals = [float(S.subs(a, i/1000)) for i in range(1, 1000)]; assert abs(min(vals)-0.25) < 1e-9
    cc = symbols("cc", positive=True)
    S3 = integrate(cc**3-x**3, (x, 0, cc))+integrate(x**3-cc**3, (x, cc, 1))
    assert _eq(S3, Rational(3, 2)*cc**4-cc**3+Rational(1, 4)) and S3.subs(cc, Rational(1, 2)) == Rational(7, 32)
    vals = [float(S3.subs(cc, i/1000)) for i in range(1, 1000)]; assert abs(min(vals)-7/32) < 1e-9
    # 弦の長さ一定：ランダムに α+β を選んで β-α を求め、S ≦ 4/3
    rnd = random.Random(6)
    for _ in range(500):
        sm = rnd.uniform(-5, 5); d = 2/math.sqrt(1+sm*sm)
        al_, be_ = (sm-d)/2, (sm+d)/2
        assert abs(math.hypot(be_-al_, be_**2-al_**2)-2) < 1e-9 and d**3/6 <= 4/3+1e-12
    for L, ans in ((2, Rational(4, 3)), (2*sqrt(2), 8*sqrt(2)/3)):
        assert _eq(L**3/6, ans)
    # 3次と直線：α を変数に
    al = symbols("al", positive=True)
    be = 3-al
    g = x*(x-al)*(x-be)
    assert _eq(expand(g), expand(x**3-3*x**2+(2-(al**2-3*al+2))*x))
    S = integrate(g, (x, 0, al))-integrate(g, (x, al, be))
    assert _eq(S, -(al**4+6*al**3-36*al**2+54*al-27)/4)
    assert _eq(integrate(g, (x, 0, al)), al**3*(2-al)/4) and _eq(integrate(g, (x, 0, be)), (3-al)**3*(al-1)/4)
    assert _eq(diff(S, al), -(2*al-3)*(al**2+6*al-9)/2)
    a0 = 3*sqrt(2)-3
    assert _eq(S.subs(al, a0), 27*(17-12*sqrt(2))/2) and _eq(a0**2-3*a0+2, 38-27*sqrt(2))
    assert _eq(S.subs(al, a0), Rational(27, 4)*(a0-1)**2)
    def Snum(kv):   # k を直接動かして数値で面積の和を求める
        dd = math.sqrt(1+4*kv); r1, r2 = (3-dd)/2, (3+dd)/2
        gg = lambda u: abs(u**3-3*u*u+(2-kv)*u)
        return _num_area(gg, lambda u: 0, 0, r2, n=4000)
    ks = [-0.2499+i*(2.2499)/600 for i in range(1, 600)]
    vv = [(Snum(kv), kv) for kv in ks]
    mn = min(vv); assert abs(mn[0]-float(S.subs(al, a0))) < 2e-4 and abs(mn[1]-(38-27*math.sqrt(2))) < 0.01
    assert _eq(S.subs(al, Rational(3, 2)), Rational(27, 64)) and float(S.subs(al, a0)) < 27/64
    # 練習 y=x(x-a)(x-1)
    g = x*(x-a)*(x-1)
    S = integrate(g, (x, 0, a))-integrate(g, (x, a, 1))
    assert _eq(diff(S, a), -(2*a-1)*(2*a**2-2*a-1)/6) and S.subs(a, Rational(1, 2)) == Rational(1, 32)
    vals = [float(S.subs(a, i/1000)) for i in range(1, 1000)]; assert abs(min(vals)-1/32) < 1e-9
    # 弦の通過範囲：X を固定し、p を細かく動かして Y の範囲を数値で求める
    def strip(X, n=600):
        lo_, hi_ = max(-1.0, X-1), min(0.0, X)
        ys = [(2*p+1)*X-p*p-p for p in [lo_+(hi_-lo_)*j/n for j in range(n+1)]]
        return max(ys)-min(ys), min(ys)
    N_ = 2000
    tot = 0.0
    for i in range(N_):
        X = -1+(i+0.5)*2/N_
        w, lo_ = strip(X)
        assert abs(lo_-X*X) < 1e-9
        tot += w*2/N_
    assert abs(tot-5/12) < 1e-4
    assert _eq(expand(x**2+Rational(1, 4)-((2*a+1)*x-a**2-a)), (x-a-Rational(1, 2))**2)
    assert 2*(Rational(1, 8)+integrate(x-x**2, (x, Rational(1, 2), 1))) == Rational(5, 12)
    # 練習：D_t の通過範囲（各 X で上端 = max_t (2tX-t^2+1)、下端 X^2）
    tot = 0.0
    for i in range(N_):
        X = -1.5+(i+0.5)*4/N_
        top = max(2*tt*X-tt*tt+1 for tt in [j/400 for j in range(401)])
        tot += max(0.0, top-X*X)*4/N_
    assert abs(tot-7/3) < 2e-3
    assert integrate(1-x**2, (x, -1, 0))+1+integrate(2*x-x**2, (x, 1, 2)) == Rational(7, 3)


# ---------------------------------------------------------------- 節7 の図
def _f72():
    t0 = (math.sqrt(3)-1)/2
    g = _G(190, 120, (-2.1, 2.2), (-0.25, 1.75))
    f = lambda u: abs(u*u-1)
    g.band(lambda u: 0, f, t0, t0+1)
    g.axes()
    g.curve(f, -1.8, 1.8)
    g.seg((t0, 0), (t0, f(t0))); g.seg((t0+1, 0), (t0+1, f(t0+1)))
    g.seg((t0, f(t0)), (t0+1, f(t0+1)), col=C2)
    g.txt(t0, 0, "t", dy=11, it=True)
    g.txt(t0+1, 0, "t+1", dy=11, it=True, dx=4)
    g.txt(-1, 0, "−1", dy=11); g.txt(1, 0, "1", dy=11)
    g.txt(-0.08, 1.5, "y=|x²−1|", anc="end", it=True)
    return g.svg()


# ---------------------------------------------------------------- 節7
SEC.append({"title": "定積分と最大・最小，論証",
"base": r"""・$\displaystyle\int_a^b(x^2+px+q)^2dx$ などは係数 $p,\ q$ の2次式 → 平方完成して最小値を求める<br>
・$\displaystyle\int_{-1}^{1}x^{2n+1}dx=0$ を使うと交差項が消える。$\int_{-1}^1 g(x)h(x)\,dx=0$ となる $g,\ h$ を組み合わせると、$\int\{\ \}^2dx$ が平方の和になる<br>
・コーシー・シュワルツの不等式：$(u_1v_1+u_2v_2+u_3v_3)^2\leqq(u_1^2+u_2^2+u_3^2)(v_1^2+v_2^2+v_3^2)$<br>
・整式 $h(x)$ が $a\leqq x\leqq b$ で $h(x)\geqq0$ で、恒等的に $0$ でなければ　$\displaystyle\int_a^b h(x)\,dx>0$""",
"items": [
 {"lv": 3, "title": "2乗の定積分の最小（最小2乗近似）",
  "q": r"$a,\ b$ が実数全体を動くとき、$I=\displaystyle\int_{-1}^{1}(x^2-ax-b)^2\,dx$ の最小値と、そのときの $a,\ b$ の値を求めよ。",
  "hint": r"展開して積分すると $a,\ b$ の2次式になる。区間が $-1$ から $1$ なので、奇数次の項（$x^3$ や $abx$）は消える。あとは $a,\ b$ それぞれについて平方完成。",
  "sol": r"$(x^2-ax-b)^2=x^4-2ax^3+(a^2-2b)x^2+2abx+b^2$。$-1\leqq x\leqq1$ で積分すると、奇数次の項の積分は $0$ だから<br>"
         r"　$I=\dfrac25+\dfrac23(a^2-2b)+2b^2=\dfrac23a^2+2b^2-\dfrac43b+\dfrac25$<br>"
         r"　$=\dfrac23a^2+2\Big(b-\dfrac13\Big)^2+\dfrac25-\dfrac29=\dfrac23a^2+2\Big(b-\dfrac13\Big)^2+\dfrac8{45}$<br>"
         r"よって　$\boldsymbol{a=0,\ b=\dfrac13}$ のとき　<b>最小値</b> $\boldsymbol{\dfrac8{45}}$",
  "note": r"最小を与える $x^2-\frac13$ は、$\int_{-1}^1\big(x^2-\frac13\big)dx=0$，$\int_{-1}^1x\big(x^2-\frac13\big)dx=0$ を満たす（$1$ とも $x$ とも「直交」する）。これは「$x^2$ を1次式 $ax+b$ で最もよく近似する」問題で、誤差 $x^2-(ax+b)$ が $1,\ x$ と直交するときに最良になる。",
  "ex": r"$p,\ q$ が実数全体を動くとき、$\displaystyle\int_0^1(x^2+px+q)^2\,dx$ の最小値と、そのときの $p,\ q$ の値を求めよ。",
  "exa": r"最小値 $\dfrac1{180}$（$p=-1,\ q=\dfrac16$）"},
 {"lv": 4, "title": "幅一定の区間で積分した関数の最小",
  "q": r"実数 $t$ に対して $F(t)=\displaystyle\int_t^{t+1}|x^2-1|\,dx$ とする。$F(t)$ の最小値と、そのときの $t$ の値を求めよ。",
  "hint": r"$y=|x^2-1|$ のグラフは $y$ 軸に関して対称なので $F(-1-t)=F(t)$（区間を折り返す）。$t\geqq-\frac12$ で考え、区間 $[t,\ t+1]$ が $x=1$ をまたぐかどうかで場合分けする。",
  "sol": _f72() +
         r"$y=|x^2-1|$ のグラフは $y$ 軸に関して対称で、区間 $[t,\ t+1]$ を $y$ 軸で折り返すと $[-1-t,\ -t]$ になるから $F(-1-t)=F(t)$。よって $t\geqq-\dfrac12$ で調べれば十分である。<br>"
         r"(i) $-\dfrac12\leqq t\leqq0$ のとき　区間は $[-1,\ 1]$ に含まれ<br>"
         r"　$\displaystyle F(t)=\int_t^{t+1}(1-x^2)\,dx=1-\frac{(t+1)^3-t^3}3=-t^2-t+\frac23$（減少）<br>"
         r"(ii) $0\leqq t\leqq1$ のとき<br>"
         r"　$\displaystyle F(t)=\int_t^1(1-x^2)\,dx+\int_1^{t+1}(x^2-1)\,dx=\frac23t^3+t^2-t+\frac23$<br>"
         r"　$F'(t)=2t^2+2t-1$ は $t_0=\dfrac{-1+\sqrt3}2$ で $0$ になり、$0\leqq t<t_0$ で負、$t_0<t\leqq1$ で正。<br>"
         r"(iii) $t\geqq1$ のとき　$\displaystyle F(t)=\int_t^{t+1}(x^2-1)\,dx=t^2+t-\frac23$（増加）<br>"
         r"(i)〜(iii) の式は $t=0,\ 1$ でつながっているので、$t\geqq-\dfrac12$ では $t=t_0$ で最小。<br>"
         r"$2t_0^2=1-2t_0$ より $t_0^2=\dfrac12-t_0$，$t_0^3=t_0\cdot t_0^2=\dfrac{3t_0-1}2$ だから<br>"
         r"　$F(t_0)=\dfrac23\cdot\dfrac{3t_0-1}2+\Big(\dfrac12-t_0\Big)-t_0+\dfrac23=\dfrac56-t_0=\dfrac43-\dfrac{\sqrt3}2$<br>"
         r"対称性から $t=-1-t_0=\dfrac{-1-\sqrt3}2$ でも同じ値をとる。よって<br>"
         r"　$\boldsymbol{t=\dfrac{-1\pm\sqrt3}2}$ のとき　<b>最小値</b> $\boldsymbol{\dfrac43-\dfrac{\sqrt3}2}$",
  "note": r"どの場合も $F'(t)=|(t+1)^2-1|-|t^2-1|$ となっている（区間の右端の高さ − 左端の高さ）。最小のとき両端の高さが等しい（右図の線分が水平）。$t=-\frac12$ は $F$ の極大で、$F\big(-\frac12\big)=\frac{11}{12}$。",
  "ex": r"実数 $t$ に対して $G(t)=\displaystyle\int_t^{t+1}|x^2-4|\,dx$ とする。$G(t)$ の最小値と、そのときの $t$ の値を求めよ。",
  "exa": r"最小値 $\dfrac{32}3-\dfrac{5\sqrt{15}}2$（$t=\dfrac{-1\pm\sqrt{15}}2$）"},
 {"lv": 5, "title": "2乗の積分が一定のときの値の最大",
  "q": r"2次以下の整式 $f(x)$ が $\displaystyle\int_{-1}^{1}\{f(x)\}^2\,dx=1$ を満たしながら動くとき、$f(1)$ の最大値を求めよ。また、最大値を与える $f(x)$ を求めよ。",
  "hint": r"$1,\ x,\ x^2-\frac13$ は、どの2つの積も $-1$ から $1$ までの積分が $0$ になる。$f(x)$ をこの3つの組合せで表すと $\int f^2dx$ が平方の和になり、コーシー・シュワルツの不等式が使える。",
  "sol": r"$f(x)$ は2次以下だから、定数 $\alpha,\ \beta,\ \gamma$ を用いて　$f(x)=\alpha+\beta x+\gamma\Big(x^2-\dfrac13\Big)$　とただ1通りに表せる。<br>"
         r"$\displaystyle\int_{-1}^1x\,dx=0$，$\displaystyle\int_{-1}^1x\Big(x^2-\frac13\Big)dx=0$，$\displaystyle\int_{-1}^1\Big(x^2-\frac13\Big)dx=\frac23-\frac23=0$ だから、$\{f(x)\}^2$ を展開したときの異なる2つの積の項の積分はすべて $0$ で<br>"
         r"　$\displaystyle\int_{-1}^1\{f(x)\}^2dx=2\alpha^2+\frac23\beta^2+\gamma^2\int_{-1}^1\Big(x^2-\frac13\Big)^2dx=2\alpha^2+\frac23\beta^2+\frac8{45}\gamma^2$<br>"
         r"（$\int_{-1}^1(x^4-\frac23x^2+\frac19)dx=\frac25-\frac49+\frac29=\frac8{45}$）。また $f(1)=\alpha+\beta+\dfrac23\gamma$。<br>"
         r"$u_1=\sqrt2\,\alpha$，$u_2=\sqrt{\frac23}\,\beta$，$u_3=\sqrt{\frac8{45}}\,\gamma$ とおくと、条件は $u_1^2+u_2^2+u_3^2=1$ で<br>"
         r"　$f(1)=\dfrac1{\sqrt2}u_1+\sqrt{\dfrac32}\,u_2+\dfrac23\sqrt{\dfrac{45}8}\,u_3$<br>"
         r"コーシー・シュワルツの不等式より<br>"
         r"　$\{f(1)\}^2\leqq\Big(\dfrac12+\dfrac32+\dfrac49\cdot\dfrac{45}8\Big)(u_1^2+u_2^2+u_3^2)=\dfrac12+\dfrac32+\dfrac52=\dfrac92$<br>"
         r"よって $f(1)\leqq\dfrac3{\sqrt2}=\dfrac{3\sqrt2}2$。等号は $(u_1,\ u_2,\ u_3)$ が $\Big(\frac1{\sqrt2},\ \sqrt{\frac32},\ \frac23\sqrt{\frac{45}8}\Big)$ の正の定数倍のとき、すなわち<br>"
         r"　$\alpha:\beta:\gamma=\dfrac12:\dfrac32:\dfrac{15}4$，$\alpha=\dfrac\lambda2,\ \beta=\dfrac{3\lambda}2,\ \gamma=\dfrac{15\lambda}4\ (\lambda>0)$<br>"
         r"のときで、条件から $\dfrac{\lambda^2}2+\dfrac{3\lambda^2}2+\dfrac{5\lambda^2}2=1$，$\lambda=\dfrac{\sqrt2}3$。このとき<br>"
         r"　$f(x)=\lambda\Big\{\dfrac12+\dfrac32x+\dfrac{15}4\Big(x^2-\dfrac13\Big)\Big\}=\dfrac{\lambda}4(15x^2+6x-3)=\dfrac{\sqrt2}4(5x^2+2x-1)$<br>"
         r"よって　<b>最大値</b> $\boldsymbol{\dfrac{3\sqrt2}2}$，そのとき $\boldsymbol{f(x)=\dfrac{\sqrt2}4(5x^2+2x-1)}$",
  "note": r"別解：$K(x)=\frac14(15x^2+6x-3)$ は $\int_{-1}^1K\,dx=\int_{-1}^1xK\,dx=\int_{-1}^1x^2K\,dx=1$ を満たすので、2次以下のすべての $f$ について $f(1)=\int_{-1}^1f(x)K(x)\,dx$。これに $\int\{f-tK\}^2dx\geqq0$ の判別式（シュワルツの不等式）を使うと $\{f(1)\}^2\leqq\int f^2dx\int K^2dx=\frac92$。$n$ 次以下の整式にすると最大値は $\frac{n+1}{\sqrt2}$ になる。",
  "ex": r"2次以下の整式 $f(x)$ が $f(0)=1$ を満たしながら動くとき、$\displaystyle\int_0^1\{f(x)\}^2\,dx$ の最小値と、そのときの $f(x)$ を求めよ。",
  "exa": r"最小値 $\dfrac19$（$f(x)=\dfrac{10}3x^2-4x+1$）"},
 {"lv": 5, "title": "定積分の条件と方程式の解の個数（論証）",
  "q": r"3次関数 $f(x)=x^3+ax^2+bx+c$ が　$\displaystyle\int_{-1}^{1}f(x)\,dx=0$，$\displaystyle\int_{-1}^{1}xf(x)\,dx=0$　を満たすとき、方程式 $f(x)=0$ は $-1<x<1$ の範囲に異なる2つ以上の実数解をもつことを示せ。",
  "hint": r"背理法。$-1<x<1$ で $f(x)$ の符号が変わる点が1個以下だとすると、ある1次式 $x-r$（または定数）を掛けて $(x-r)f(x)$ の符号を一定にできる。一方、条件から $\int_{-1}^1(x-r)f(x)\,dx=0$。",
  "sol": r"$-1<x<1$ において $f(x)$ の符号が変わる点の個数を $N$ とする。$f(x)$ は恒等的に $0$ でない整式であることに注意する。<br>"
         r"(i) $N=0$ と仮定すると、$-1\leqq x\leqq1$ で常に $f(x)\geqq0$ または常に $f(x)\leqq0$。どちらの場合も $\displaystyle\int_{-1}^1f(x)\,dx\neq0$ となり、条件に反する。<br>"
         r"(ii) $N=1$ と仮定し、符号が変わる点を $x=r\ (-1<r<1)$ とする。$x=r$ の両側で $f(x)$ と $x-r$ はともに符号が変わり、それ以外では符号が変わらないから、$(x-r)f(x)$ は $-1\leqq x\leqq1$ で常に $0$ 以上または常に $0$ 以下である。$(x-r)f(x)$ は恒等的に $0$ でない整式なので　$\displaystyle\int_{-1}^1(x-r)f(x)\,dx\neq0$<br>"
         r"一方、条件から　$\displaystyle\int_{-1}^1(x-r)f(x)\,dx=\int_{-1}^1xf(x)\,dx-r\int_{-1}^1f(x)\,dx=0$　となり矛盾。<br>"
         r"よって $N\geqq2$。符号が変わる点では $f(x)=0$ だから、$f(x)=0$ は $-1<x<1$ に異なる2つ以上の実数解をもつ。■",
  "note": r"条件は $b=-\frac35$，$c=-\frac a3$ と同値である。例えば $a=0$ なら $f(x)=x^3-\frac35x=x\big(x^2-\frac35\big)$ は $-1<x<1$ に3つの解をもつ。さらに $\int_{-1}^1x^2f(x)\,dx=0$ も課すと $f(x)=x^3-\frac35x$ に決まり、同じ論法で「3つの解」が示せる（ルジャンドル多項式の性質）。「重解」は符号が変わらないこともあるので、解の個数ではなく符号の変わる点の個数で論じるのが要点。",
  "ex": r"3次関数 $f(x)$ が $\displaystyle\int_0^1f(x)\,dx=\int_0^1xf(x)\,dx=\int_0^1x^2f(x)\,dx=0$ を満たすとき、方程式 $f(x)=0$ は $0<x<1$ に異なる3つの実数解をもつことを示せ。",
  "exa": r"背理法：$0<x<1$ で符号の変わる点が2個以下なら、それらを解にもつ2次以下の整式 $h(x)$ について $h(x)f(x)$ は符号一定で恒等的に $0$ でなく、$\int_0^1h(x)f(x)\,dx\neq0$。一方、条件から $\int_0^1h(x)f(x)\,dx=0$ となり矛盾。"},
]})


def _v7():
    I = expand(integrate((x**2-a*x-b)**2, (x, -1, 1)))
    assert _eq(I, Rational(2, 3)*a**2+2*(b-Rational(1, 3))**2+Rational(8, 45))
    p, q = symbols("p q")
    J = expand(integrate((x**2+p*x+q)**2, (x, 0, 1)))
    sol = solve([diff(J, p), diff(J, q)], [p, q]); assert sol == {p: -1, q: Rational(1, 6)}
    assert J.subs(sol) == Rational(1, 180)
    # J は正定値の2次式（ヘッセ行列が正定値）なので停留点が最小
    H = [[diff(J, p, 2), diff(J, p, q)], [diff(J, q, p), diff(J, q, 2)]]
    assert H[0][0] > 0 and H[0][0]*H[1][1]-H[0][1]*H[1][0] > 0
    # F(t)=∫_t^{t+1}|x^2-1|
    tt = symbols("tt")
    F1 = integrate(1-x**2, (x, tt, tt+1)); assert _eq(F1, -tt**2-tt+Rational(2, 3))
    F2 = integrate(1-x**2, (x, tt, 1))+integrate(x**2-1, (x, 1, tt+1)); assert _eq(F2, Rational(2, 3)*tt**3+tt**2-tt+Rational(2, 3))
    F3 = integrate(x**2-1, (x, tt, tt+1)); assert _eq(F3, tt**2+tt-Rational(2, 3))
    assert _eq(diff(F2, tt), 2*tt**2+2*tt-1)
    t0 = (-1+sqrt(3))/2
    assert _eq(F2.subs(tt, t0), Rational(4, 3)-sqrt(3)/2)
    Fn = lambda tv: _num_area(lambda u: abs(u*u-1), lambda u: 0, tv, tv+1, n=600)
    vals = [(Fn(-3+i*0.004), -3+i*0.004) for i in range(0, 1501)]
    mn = min(vals); assert abs(mn[0]-float(Rational(4, 3)-sqrt(3)/2)) < 1e-4
    assert min(abs(mn[1]-float(t0)), abs(mn[1]-float(-1-t0))) < 0.005
    assert abs(Fn(-1-float(t0))-Fn(float(t0))) < 1e-9 and abs(Fn(-0.5)-11/12) < 1e-5
    G2 = integrate(4-x**2, (x, tt, 2))+integrate(x**2-4, (x, 2, tt+1))
    t1 = (-1+sqrt(15))/2
    assert _eq(diff(G2, tt), 2*tt**2+2*tt-7) and _eq(G2.subs(tt, t1), Rational(32, 3)-5*sqrt(15)/2)
    Gn = lambda tv: _num_area(lambda u: abs(u*u-4), lambda u: 0, tv, tv+1, n=600)
    vals = [(Gn(-4+i*0.005), -4+i*0.005) for i in range(0, 1601)]
    mn = min(vals); assert abs(mn[0]-float(Rational(32, 3)-5*sqrt(15)/2)) < 1e-4
    assert min(abs(mn[1]-float(t1)), abs(mn[1]-float(-1-t1))) < 0.006
    # max f(1)
    P2 = x**2-Rational(1, 3)
    assert integrate(x*P2, (x, -1, 1)) == 0 and integrate(P2, (x, -1, 1)) == 0 and integrate(P2**2, (x, -1, 1)) == Rational(8, 45)
    assert Rational(1, 2)+Rational(3, 2)+Rational(4, 9)*Rational(45, 8) == Rational(9, 2)
    fbest = sqrt(2)/4*(5*x**2+2*x-1)
    assert _eq(integrate(fbest**2, (x, -1, 1)), 1) and _eq(fbest.subs(x, 1), 3*sqrt(2)/2)
    lam = sqrt(2)/3
    assert _eq(expand(lam*(Rational(1, 2)+Rational(3, 2)*x+Rational(15, 4)*P2)), expand(fbest))
    K = (15*x**2+6*x-3)/4
    assert [integrate(x**i*K, (x, -1, 1)) for i in range(3)] == [1, 1, 1] and integrate(K**2, (x, -1, 1)) == Rational(9, 2)
    rnd = random.Random(7)
    for _ in range(2000):
        cf = [rnd.gauss(0, 1) for _ in range(3)]
        nrm = float(integrate((cf[0]+cf[1]*x+cf[2]*x**2)**2, (x, -1, 1))) if _ < 20 else \
            2*cf[0]**2+2*cf[1]**2/3+2*cf[2]**2/5+4*cf[0]*cf[2]/3
        val = (cf[0]+cf[1]+cf[2])/math.sqrt(nrm)
        assert val <= 3/math.sqrt(2)+1e-9
    # 練習：f(0)=1 で ∫_0^1 f^2 の最小
    q1, q2 = symbols("q1 q2")
    J = expand(integrate((1+q1*x+q2*x**2)**2, (x, 0, 1)))
    sol = solve([diff(J, q1), diff(J, q2)], [q1, q2]); assert sol == {q1: -4, q2: Rational(10, 3)}
    assert J.subs(sol) == Rational(1, 9)
    H = [[diff(J, q1, 2), diff(J, q1, q2)], [diff(J, q2, q1), diff(J, q2, 2)]]
    assert H[0][0] > 0 and H[0][0]*H[1][1]-H[0][1]*H[1][0] > 0
    # 解の個数：条件 ⇔ b=-3/5, c=-a/3。ランダムな a で符号の変わる点を数える
    A_, B_, C_ = symbols("A_ B_ C_")
    f = x**3+A_*x**2+B_*x+C_
    assert solve([integrate(f, (x, -1, 1)), integrate(x*f, (x, -1, 1))], [B_, C_]) == {B_: Rational(-3, 5), C_: -A_/3}
    for _ in range(400):
        av = rnd.uniform(-20, 20)
        fv = lambda u: u**3+av*u*u-0.6*u-av/3
        xs = [-1+2*i/20000 for i in range(1, 20000)]
        ch = sum(1 for i in range(len(xs)-1) if fv(xs[i])*fv(xs[i+1]) < 0)
        assert ch >= 2
    assert _eq(integrate((x-c)*f, (x, -1, 1)), integrate(x*f, (x, -1, 1))-c*integrate(f, (x, -1, 1)))
    f0 = f.subs({B_: Rational(-3, 5), C_: -A_/3})
    assert solve(integrate(x**2*f0, (x, -1, 1)), A_) == [0] and _eq(factor(f0.subs(A_, 0)), x*(5*x**2-3)/5)
    f = x**3+A_*x**2+B_*x+C_
    sol = solve([integrate(x**i*f, (x, 0, 1)) for i in range(3)], [A_, B_, C_])
    rts = Poly(f.subs(sol), x).nroots()
    assert len(rts) == 3 and all(abs(complex(r_).imag) < 1e-12 and 0 < complex(r_).real < 1 for r_ in rts)


CH = {"no": 15, "sections": SEC}


def verify():
    vs = [g for n_, g in sorted(globals().items()) if n_.startswith("_v") and n_[2:].isdigit()]
    for g in vs:
        g()
    items = [it for s_ in SEC for it in s_["items"]]
    cnt = {L: sum(1 for it in items if it["lv"] == L) for L in range(1, 6)}
    print("c15:", len(SEC), "sections,", len(items), "items", cnt)
    assert len(SEC) == 7 and 37 <= len(items) <= 43 and cnt[5] >= 5
    assert cnt == {1: 8, 2: 10, 3: 11, 4: 8, 5: 5}
    for it in items:
        for k_ in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
            assert it.get(k_) not in (None, ""), it["title"]
        if it["lv"] >= 3:
            assert it.get("note"), it["title"]
