"""第26章 積分法の応用（数学III）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。
図の座標はすべて Python で計算する。体積は sympy の積分に加えて、数値積分・モンテカルロ法でも確かめる。"""
import math
import random
import numpy as np
from sympy import (symbols, Rational, sqrt, exp, log, sin, cos, tan, pi, E, integrate, simplify, diff,
                   solve, expand, factor, Abs, N, nsimplify, oo, limit, Symbol, cbrt)

SEC = []

# ---------------------------------------------------------------- 図の道具
C1, C2, C3, CG, CF, CF2 = "#16367a", "#d9701e", "#2e8b57", "#888888", "#c9daf3", "#f6d3a8"
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

    def axes(s, xl="x", yl="y", o="O", ox=True, oy=True):
        X0, Y0 = s.X(0), s.Y(0)
        xa, xb, ya, yb = s.X(s.x0), s.X(s.x1), s.Y(s.y0), s.Y(s.y1)
        if ox:
            s.o.append(f'<line x1="{xa}" y1="{Y0}" x2="{xb}" y2="{Y0}" stroke="#333" stroke-width="0.8"/>')
            s.o.append(f'<polygon points="{xb + 3},{Y0} {xb - 3},{Y0 - 2.6} {xb - 3},{Y0 + 2.6}" fill="#333"/>')
            s.o.append(f'<text x="{xb - 1}" y="{Y0 - 4}" text-anchor="end" font-style="italic" font-family="serif" font-size="11">{xl}</text>')
        if oy:
            s.o.append(f'<line x1="{X0}" y1="{ya}" x2="{X0}" y2="{yb}" stroke="#333" stroke-width="0.8"/>')
            s.o.append(f'<polygon points="{X0},{yb - 3} {X0 - 2.6},{yb + 3} {X0 + 2.6},{yb + 3}" fill="#333"/>')
            s.o.append(f'<text x="{X0 + 5}" y="{yb + 6}" font-style="italic" font-family="serif" font-size="11">{yl}</text>')
        if o:
            s.o.append(f'<text x="{X0 - 3}" y="{Y0 + 10}" text-anchor="end" font-style="italic" font-family="serif" font-size="10">{o}</text>')

    def _pl(s, pts, col, w, dash):
        s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{dash} points="'
                   + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts) + '"/>')

    def curve(s, f, a, b, col=C1, w=1.4, dash="", n=240):
        """y=f(x)（a≦x≦b）。枠の上下からはみ出す部分は描かない。"""
        cur = []
        for i in range(n + 1):
            x = a + (b - a) * i / n
            y = f(x)
            if s.y0 <= y <= s.y1:
                cur.append((x, y))
            else:
                if len(cur) > 1:
                    s._pl(cur, col, w, dash)
                cur = []
        if len(cur) > 1:
            s._pl(cur, col, w, dash)

    def pcurve(s, fx, fy, t0, t1, col=C1, w=1.4, dash="", n=300):
        """媒介変数で表した曲線。"""
        cur = []
        for i in range(n + 1):
            u = t0 + (t1 - t0) * i / n
            p, q = fx(u), fy(u)
            if s.x0 <= p <= s.x1 and s.y0 <= q <= s.y1:
                cur.append((p, q))
            else:
                if len(cur) > 1:
                    s._pl(cur, col, w, dash)
                cur = []
        if len(cur) > 1:
            s._pl(cur, col, w, dash)

    def poly(s, pts, fill=CF, op=0.9, stroke="none", w=0.8):
        s.o.append('<polygon points="' + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts)
                   + f'" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{w}"/>')

    def band(s, lo, hi, a, b, n=160, fill=CF, op=0.9):
        """a≦x≦b で lo(x)≦y≦hi(x) の部分を塗る。"""
        xs = [a + (b - a) * i / n for i in range(n + 1)]
        s.poly([(x, hi(x)) for x in xs] + [(x, lo(x)) for x in reversed(xs)], fill, op)

    def seg(s, p, q, col=CG, w=0.8, dash=DASH):
        s.o.append(f'<line x1="{s.X(p[0])}" y1="{s.Y(p[1])}" x2="{s.X(q[0])}" y2="{s.Y(q[1])}" stroke="{col}" stroke-width="{w}"{dash}/>')

    def pt(s, x, y, col=C1, r=1.8):
        s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="{col}"/>')

    def txt(s, x, y, t, dx=0, dy=0, anc="middle", it=False, size=10, col="#222"):
        st = ' font-style="italic" font-family="serif"' if it else ""
        s.o.append(f'<text x="{round(s.X(x) + dx, 1)}" y="{round(s.Y(y) + dy, 1)}" text-anchor="{anc}" font-size="{size}" fill="{col}"{st}>{t}</text>')

    def xtick(s, x, t, dy=11, dx=0):
        s.o.append(f'<line x1="{s.X(x)}" y1="{s.Y(0) - 2}" x2="{s.X(x)}" y2="{s.Y(0) + 2}" stroke="#333" stroke-width="0.8"/>')
        s.txt(x, 0, t, dx=dx, dy=dy, size=10)

    def ytick(s, y, t, dx=-4):
        s.o.append(f'<line x1="{s.X(0) - 2}" y1="{s.Y(y)}" x2="{s.X(0) + 2}" y2="{s.Y(y)}" stroke="#333" stroke-width="0.8"/>')
        s.txt(0, y, t, dx=dx, dy=3.5, anc="end", size=10)

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" font-size="10">'
                + "".join(s.o) + "</svg>")


# ---------------------------------------------------------------- 数値計算の道具
def _simpson(f, a, b, n=4000):
    """合成シンプソン公式（n は偶数）。"""
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(t) for t in xs], dtype=float)
    h = (b - a) / n
    return h / 3 * (ys[0] + ys[-1] + 4 * ys[1:-1:2].sum() + 2 * ys[2:-1:2].sum())


def _close(u, v, tol=1e-9):
    return abs(float(u) - float(v)) < tol


def _eq(u, v):
    return simplify(u - v) == 0


x, y, t, a, k, n, th = symbols("x y t a k n theta", real=True)


# ---------------------------------------------------------------- 第1節の図
def _f14():
    g = _G(200, 128, (-0.35, 3.35), (-0.55, 1.55))
    e_ = math.e
    pts = [(0, 0), (e_, 1)] + [(math.exp(1 - i / 80), 1 - i / 80) for i in range(81)]
    g.poly(pts)
    g.axes()
    g.curve(lambda u: math.log(u), 0.42, 3.3)
    g.curve(lambda u: u / e_, -0.3, 3.3, col=C2)
    g.pt(e_, 1)
    g.seg((e_, 0), (e_, 1))
    g.xtick(1, "1", dy=11, dx=3)
    g.xtick(e_, "e", dy=11)
    g.txt(2.3, 1.3, "ℓ : y=x/e", anc="end", it=True, col=C2, size=9)
    g.txt(1.2, -0.42, "y=log x", anc="start", it=True, size=9)
    return g.svg()


def _f15():
    g = _G(190, 140, (-0.25, 1.85), (-0.2, 1.3))
    al = math.atan(4 / 3)
    lo = lambda u: min(math.cos(u), 0.75 * math.sin(u))
    g.band(lambda u: 0, math.cos, 0, math.pi / 2)
    g.band(lambda u: 0, lo, 0, math.pi / 2, fill=CF2)
    g.axes()
    g.curve(math.cos, -0.1, math.pi / 2)
    g.curve(lambda u: 0.75 * math.sin(u), -0.1, 1.85, col=C2)
    g.seg((al, 0), (al, math.cos(al)))
    g.xtick(al, "α")
    g.xtick(math.pi / 2, "π/2", dx=2)
    g.txt(0.25, 1.03, "y=cos x", anc="start", it=True, size=9)
    g.txt(1.82, 0.84, "y=a sin x", anc="end", it=True, col=C2, size=9)
    g.txt(0.75, 0.2, "T", it=True)
    return g.svg()


# ---------------------------------------------------------------- 節1
SEC.append({"title": r"面積（1）　y＝f(x) で表される曲線",
"base": r"""・$a\leqq x\leqq b$ で $f(x)\geqq g(x)$ のとき，2曲線 $y=f(x)$，$y=g(x)$ と2直線 $x=a$，$x=b$ で囲まれた部分の面積は　$\displaystyle S=\int_a^b\{f(x)-g(x)\}\,dx$。上下が入れかわるときは区間を分ける（$\displaystyle\int_a^b|f(x)-g(x)|\,dx$）。<br>
・$y$ について積分する：$c\leqq y\leqq d$ で $x=h(y)\geqq0$ のとき，曲線 $x=h(y)$ と $y$ 軸，2直線 $y=c$，$y=d$ で囲まれた部分の面積は　$\displaystyle S=\int_c^d h(y)\,dy$。逆関数が簡単な形になるときに有効。<br>
・交点の $x$ 座標が具体的に求まらないときは $\alpha$ などとおき，交点の条件（$\tan\alpha=\cdots$ など）を使って $\sin\alpha$，$\cos\alpha$ などを処理する。""",
"items": [
 {"lv": 1, "title": r"曲線と $x$ 軸の間の面積",
  "q": r"次の面積 $S$ を求めよ。<br>(1) 曲線 $y=\dfrac1x$ と $x$ 軸および2直線 $x=1$，$x=e^2$ で囲まれた部分の面積<br>(2) 曲線 $y=\sin x\ (0\leqq x\leqq2\pi)$ と $x$ 軸で囲まれた2つの部分の面積の和",
  "hint": r"まず区間内での関数の符号を調べる。$x$ 軸より下にある部分は $\displaystyle\int(-f(x))\,dx$ として正の値にしてから加える。",
  "sol": r"(1) $1\leqq x\leqq e^2$ で $\dfrac1x>0$ だから　$\displaystyle S=\int_1^{e^2}\frac{dx}{x}=\Big[\log x\Big]_1^{e^2}=\boldsymbol{2}$<br>"
         r"(2) $0\leqq x\leqq\pi$ で $\sin x\geqq0$，$\pi\leqq x\leqq2\pi$ で $\sin x\leqq0$ だから<br>"
         r"$\displaystyle S=\int_0^\pi\sin x\,dx-\int_\pi^{2\pi}\sin x\,dx=\Big[-\cos x\Big]_0^\pi-\Big[-\cos x\Big]_\pi^{2\pi}=2-(-2)=\boldsymbol{4}$",
  "note": r"(2) を $\displaystyle\int_0^{2\pi}\sin x\,dx$ と計算すると $0$ になってしまう。定積分は「符号つきの面積」であることに注意。",
  "ex": r"次の面積を求めよ。<br>(1) 曲線 $y=e^x$ と $x$ 軸，$y$ 軸および直線 $x=2$ で囲まれた部分<br>(2) 曲線 $y=\cos x\ \left(0\leqq x\leqq\dfrac32\pi\right)$ と $x$ 軸および $y$ 軸で囲まれた2つの部分の面積の和",
  "exa": r"(1) $e^2-1$　(2) $3$"},
 {"lv": 1, "title": r"2曲線の間の面積",
  "q": r"$\dfrac\pi4\leqq x\leqq\dfrac54\pi$ において，2曲線 $y=\sin x$，$y=\cos x$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"2曲線は $x=\dfrac\pi4$，$\dfrac54\pi$ で交わる。その間でどちらが上にあるかを，差 $\sin x-\cos x$ を合成して調べる。",
  "sol": r"$\sin x-\cos x=\sqrt2\sin\left(x-\dfrac\pi4\right)$ で，$\dfrac\pi4\leqq x\leqq\dfrac54\pi$ のとき $0\leqq x-\dfrac\pi4\leqq\pi$ だから $\sin x\geqq\cos x$。<br>"
         r"$\displaystyle S=\int_{\frac\pi4}^{\frac54\pi}(\sin x-\cos x)\,dx=\Big[-\cos x-\sin x\Big]_{\frac\pi4}^{\frac54\pi}=\left(\frac{\sqrt2}2+\frac{\sqrt2}2\right)-\left(-\frac{\sqrt2}2-\frac{\sqrt2}2\right)=\boldsymbol{2\sqrt2}$",
  "note": r"$\displaystyle\int_{\frac\pi4}^{\frac54\pi}\sqrt2\sin\left(x-\frac\pi4\right)dx=\sqrt2\int_0^\pi\sin u\,du=2\sqrt2$ と，合成した形のまま積分してもよい。",
  "ex": r"2曲線 $y=e^x$，$y=e^{-x}$ と直線 $x=1$ で囲まれた部分の面積を求めよ。",
  "exa": r"$e+\dfrac1e-2$"},
 {"lv": 2, "title": r"$y$ について積分する",
  "q": r"曲線 $y=\log x$ と $x$ 軸，$y$ 軸および直線 $y=2$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$x$ で積分すると $0\leqq x\leqq1$ と $1\leqq x\leqq e^2$ に分けたうえで $\int\log x\,dx$ が必要になる。$x=e^y$ と逆に解けば，$y$ についての1つの積分で済む。",
  "sol": r"$y=\log x\iff x=e^y$。求める部分は $0\leqq y\leqq2$，$0\leqq x\leqq e^y$ と表されるから<br>"
         r"$\displaystyle S=\int_0^2e^y\,dy=\Big[e^y\Big]_0^2=\boldsymbol{e^2-1}$",
  "note": r"$x$ で積分すると　$\displaystyle S=\int_0^1 2\,dx+\int_1^{e^2}(2-\log x)\,dx=2+2(e^2-1)-\Big[x\log x-x\Big]_1^{e^2}=e^2-1$ となり，同じ結果だが手間が多い。",
  "ex": r"曲線 $y=\log(x+1)$ と $y$ 軸および直線 $y=1$ で囲まれた部分の面積を求めよ。",
  "exa": r"$e-2$"},
 {"lv": 2, "title": r"原点から引いた接線と囲む部分の面積",
  "q": r"原点から曲線 $y=\log x$ に引いた接線を $\ell$ とする。曲線 $y=\log x$，接線 $\ell$ および $x$ 軸で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"接点を $(t,\ \log t)$ とおいて接線の方程式をつくり，原点を通る条件で $t$ を決める。囲まれた部分は $y$ で積分すると1つの式で表せる。",
  "sol": _f14() + r"$y'=\dfrac1x$ より，点 $(t,\ \log t)$ における接線は　$y=\dfrac1t(x-t)+\log t$。<br>"
         r"これが原点を通るとき $0=-1+\log t$，$t=e$。よって $\ell:\ y=\dfrac xe$，接点は $(e,\ 1)$。<br>"
         r"$0\leqq y\leqq1$ において，$\ell$ 上の点の $x$ 座標は $ey$，曲線上の点の $x$ 座標は $e^y$ で，曲線 $y=\log x$ は上に凸だから接線 $\ell$ の下側にあり，$e^y\geqq ey$。よって<br>"
         r"$\displaystyle S=\int_0^1(e^y-ey)\,dy=\Big[e^y-\frac e2y^2\Big]_0^1=e-\frac e2-1=\boldsymbol{\frac e2-1}$",
  "note": r"$x$ で積分すると，3点 $(0,\ 0)$，$(e,\ 0)$，$(e,\ 1)$ を頂点とする三角形（面積 $\dfrac e2$）から $\displaystyle\int_1^e\log x\,dx=1$ を引いて $\dfrac e2-1$。図形を「引き算」で見るのも有効である。",
  "ex": r"曲線 $y=\log x$ 上の点 $(e^2,\ 2)$ における接線と，曲線 $y=\log x$ および $x$ 軸で囲まれた部分の面積を求めよ。",
  "exa": r"$e^2-1$"},
 {"lv": 3, "title": r"面積を2等分する曲線（交点の座標を文字のまま扱う）",
  "q": r"曲線 $y=\cos x\ \left(0\leqq x\leqq\dfrac\pi2\right)$ と $x$ 軸，$y$ 軸で囲まれた部分を $D$ とする。曲線 $y=a\sin x$（$a$ は正の定数）が $D$ の面積を2等分するとき，$a$ の値を求めよ。",
  "hint": r"2曲線の交点の $x$ 座標 $\alpha$ は具体的には求まらない。$\tan\alpha=\dfrac1a$ という関係だけを使い，$\sin\alpha$，$\cos\alpha$ を $a$ で表して面積を $a$ の式にする。",
  "sol": _f15() + r"$D$ の面積は $\displaystyle\int_0^{\frac\pi2}\cos x\,dx=1$。<br>"
         r"$h(x)=a\sin x-\cos x$ は $h'(x)=a\cos x+\sin x>0\ \left(0<x<\dfrac\pi2\right)$ より増加し，$h(0)=-1<0$，$h\left(\dfrac\pi2\right)=a>0$ だから，2曲線は $0<x<\dfrac\pi2$ のただ1点で交わる。その $x$ 座標を $\alpha$ とすると $a\sin\alpha=\cos\alpha$，すなわち $\tan\alpha=\dfrac1a$。<br>"
         r"$D$ のうち曲線 $y=a\sin x$ の下側の部分の面積を $T$ とする。$0\leqq x\leqq\alpha$ では $a\sin x\leqq\cos x$，$\alpha\leqq x\leqq\dfrac\pi2$ では $\cos x\leqq a\sin x$ だから<br>"
         r"$\displaystyle T=\int_0^\alpha a\sin x\,dx+\int_\alpha^{\frac\pi2}\cos x\,dx=a(1-\cos\alpha)+(1-\sin\alpha)=a+1-(a\cos\alpha+\sin\alpha)$<br>"
         r"$0<\alpha<\dfrac\pi2$，$\tan\alpha=\dfrac1a$ より $\cos\alpha=\dfrac{a}{\sqrt{a^2+1}}$，$\sin\alpha=\dfrac1{\sqrt{a^2+1}}$ なので　$a\cos\alpha+\sin\alpha=\dfrac{a^2+1}{\sqrt{a^2+1}}=\sqrt{a^2+1}$<br>"
         r"よって $T=a+1-\sqrt{a^2+1}$。$T=\dfrac12$ より $\sqrt{a^2+1}=a+\dfrac12$。両辺は正だから2乗して $a^2+1=a^2+a+\dfrac14$，すなわち　$\boldsymbol{a=\dfrac34}$",
  "note": r"$\alpha$ を求めずに「$\tan\alpha$ の値から $\sin\alpha$，$\cos\alpha$ を出す」のが要点。$T$ は $a$ について単調増加（$T'=1-\dfrac{a}{\sqrt{a^2+1}}>0$）で $0<T<1$ だから，2等分する $a$ はただ1つである。",
  "ex": r"曲線 $y=\sin x\ \left(0\leqq x\leqq\dfrac\pi2\right)$ と $x$ 軸および直線 $x=\dfrac\pi2$ で囲まれた部分を $D$ とする。$D$ は曲線 $y=a\cos x$（$a>0$）によって2つの部分に分けられる。そのうち $x$ 軸側の部分の面積が $D$ の面積の $\dfrac13$ となるような $a$ の値を求めよ。",
  "exa": r"$a=\dfrac5{12}$"},
 {"lv": 3, "title": r"面積の最小（接点が動く）",
  "q": r"$0\leqq t\leqq2$ とする。曲線 $y=e^x$ 上の点 $(t,\ e^t)$ における接線を $\ell$ とし，曲線 $y=e^x$，接線 $\ell$ および2直線 $x=0$，$x=2$ で囲まれた部分の面積を $S(t)$ とする。$S(t)$ の最小値と，そのときの $t$ の値を求めよ。",
  "hint": r"$y=e^x$ は下に凸だから，接線はつねに曲線の下にある。$S(t)$ を $t$ の関数として具体的に表し，微分して増減を調べる。",
  "sol": r"$\ell:\ y=e^t(x-t)+e^t=e^t(x-t+1)$。$y=e^x$ は下に凸なので，すべての $x$ で $e^x\geqq e^t(x-t+1)$。よって<br>"
         r"$\displaystyle S(t)=\int_0^2\{e^x-e^t(x-t+1)\}\,dx=(e^2-1)-e^t\Big[\frac{(x-t+1)^2}{2}\Big]_0^2$<br>"
         r"$\displaystyle\qquad=e^2-1-e^t\cdot\frac{(3-t)^2-(1-t)^2}{2}=e^2-1-e^t(4-2t)$<br>"
         r"$S'(t)=-\{e^t(4-2t)-2e^t\}=2e^t(t-1)$<br>"
         r"<table><tr><th>$t$</th><td>$0$</td><td>$\cdots$</td><td>$1$</td><td>$\cdots$</td><td>$2$</td></tr><tr><th>$S'(t)$</th><td></td><td>$-$</td><td>$0$</td><td>$+$</td><td></td></tr><tr><th>$S(t)$</th><td></td><td>$\searrow$</td><td>極小</td><td>$\nearrow$</td><td></td></tr></table>"
         r"よって $\boldsymbol{t=1}$ のとき最小で，最小値は　$S(1)=\boldsymbol{e^2-2e-1}$",
  "note": r"一般に，下に凸な $f(x)$ のグラフと区間 $a\leqq x\leqq b$ での接線とで囲まれる面積は，区間の中点 $t=\dfrac{a+b}2$ で接するとき最小になる。$S(t)=\displaystyle\int_a^bf(x)\,dx-(b-a)\left\{f(t)+f'(t)\left(\frac{a+b}2-t\right)\right\}$ を微分すると $S'(t)=(b-a)f''(t)\left(t-\dfrac{a+b}2\right)$ となるからである。",
  "ex": r"$1\leqq t\leqq3$ とする。曲線 $y=\log x$ 上の点 $(t,\ \log t)$ における接線と，曲線 $y=\log x$ および2直線 $x=1$，$x=3$ で囲まれた部分の面積の最小値と，そのときの $t$ の値を求めよ。",
  "exa": r"$t=2$ のとき最小値 $2+2\log2-3\log3$"},
 {"lv": 3, "title": r"面積の無限級数",
  "q": r"曲線 $y=e^{-x}\sin x\ (x\geqq0)$ と $x$ 軸で囲まれた部分のうち，$n\pi\leqq x\leqq(n+1)\pi$ の部分の面積を $S_n$（$n=0,\ 1,\ 2,\ \cdots$）とする。$S_n$ を求めよ。また，$\displaystyle\sum_{n=0}^\infty S_n$ を求めよ。",
  "hint": r"$\displaystyle\int e^{-x}\sin x\,dx$ は部分積分を2回行う（または微分して確かめる）。$n\pi\leqq x\leqq(n+1)\pi$ での $\sin x$ の符号は $(-1)^n$ である。",
  "sol": r"$\left\{-\dfrac12e^{-x}(\sin x+\cos x)\right\}'=\dfrac12e^{-x}(\sin x+\cos x)-\dfrac12e^{-x}(\cos x-\sin x)=e^{-x}\sin x$ だから<br>"
         r"$\displaystyle\int e^{-x}\sin x\,dx=-\frac12e^{-x}(\sin x+\cos x)+C$<br>"
         r"$n\pi\leqq x\leqq(n+1)\pi$ で $\sin x$ の符号は $(-1)^n$ だから，$\cos n\pi=(-1)^n$，$\sin n\pi=0$ を用いて<br>"
         r"$\displaystyle S_n=(-1)^n\int_{n\pi}^{(n+1)\pi}e^{-x}\sin x\,dx=(-1)^n\cdot\left\{-\frac12e^{-(n+1)\pi}(-1)^{n+1}+\frac12e^{-n\pi}(-1)^n\right\}$<br>"
         r"$\displaystyle\qquad=\boldsymbol{\frac{1+e^{-\pi}}2\,e^{-n\pi}}$<br>"
         r"これは初項 $\dfrac{1+e^{-\pi}}2$，公比 $e^{-\pi}\ (0<e^{-\pi}<1)$ の等比数列だから，無限級数は収束して<br>"
         r"$\displaystyle\sum_{n=0}^\infty S_n=\frac{1+e^{-\pi}}{2(1-e^{-\pi})}=\boldsymbol{\frac{e^\pi+1}{2(e^\pi-1)}}$",
  "note": r"$x=u+n\pi$ と置換すると $\sin x=(-1)^n\sin u$ より $\displaystyle S_n=e^{-n\pi}\int_0^\pi e^{-u}\sin u\,du=e^{-n\pi}S_0$ となり，$S_n$ が等比数列になることが計算の前に分かる。",
  "ex": r"曲線 $y=e^{-2x}\sin x\ (x\geqq0)$ と $x$ 軸で囲まれた部分のうち，$n\pi\leqq x\leqq(n+1)\pi$ の部分の面積を $S_n$ とする。$S_n$ と $\displaystyle\sum_{n=0}^\infty S_n$ を求めよ。",
  "exa": r"$S_n=\dfrac{1+e^{-2\pi}}5e^{-2n\pi}$，$\displaystyle\sum_{n=0}^\infty S_n=\frac{e^{2\pi}+1}{5(e^{2\pi}-1)}$"},
]})


def _v1():
    # 曲線と x 軸
    assert _eq(integrate(1 / x, (x, 1, E**2)), 2)
    assert _close(_simpson(lambda u: abs(math.sin(u)), 0, 2 * math.pi), 4, 1e-8)
    assert _eq(integrate(exp(x), (x, 0, 2)), E**2 - 1)
    assert _close(_simpson(lambda u: abs(math.cos(u)), 0, 1.5 * math.pi), 3, 1e-8)
    # 2曲線
    assert _eq(integrate(sin(x) - cos(x), (x, pi / 4, 5 * pi / 4)), 2 * sqrt(2))
    assert all(math.sin(u) >= math.cos(u) - 1e-12 for u in np.linspace(math.pi / 4, 5 * math.pi / 4, 999))
    assert _eq(integrate(exp(x) - exp(-x), (x, 0, 1)), E + 1 / E - 2)
    # y について積分
    assert _eq(integrate(exp(y), (y, 0, 2)), E**2 - 1)
    assert _eq(2 + integrate(2 - log(x), (x, 1, E**2)), E**2 - 1)
    assert _eq(integrate(exp(y) - 1, (y, 0, 1)), E - 2)
    assert _close(_simpson(lambda u: 1 - math.log(u + 1), 0, math.e - 1), math.e - 2)
    # 原点からの接線
    tt = solve(-1 + log(t), t)
    assert tt == [E]
    assert _eq(integrate(exp(y) - E * y, (y, 0, 1)), E / 2 - 1)
    assert _eq(Rational(1, 2) * E * 1 - integrate(log(x), (x, 1, E)), E / 2 - 1)
    assert all(math.exp(v) >= math.e * v for v in np.linspace(0, 1, 101))
    # 練習：(e^2,2) での接線 y = x/e^2 + 1、x 切片 -e^2
    tl = lambda u: u / math.e**2 + 1
    assert _close(tl(-math.e**2), 0) and _close(tl(math.e**2), 2)
    assert _eq(Rational(1, 2) * 2 * E**2 * 2 - integrate(log(x), (x, 1, E**2)), E**2 - 1)
    assert _eq(integrate(exp(y) - E**2 * (y - 1), (y, 0, 2)), E**2 - 1)
    # 2等分：T(a) = a+1-sqrt(a^2+1)
    aa = Rational(3, 4)
    Tn = _simpson(lambda u: min(math.cos(u), 0.75 * math.sin(u)), 0, math.pi / 2, 20000)
    assert abs(Tn - 0.5) < 1e-6
    assert _eq(aa + 1 - sqrt(aa**2 + 1), Rational(1, 2))
    al = math.atan(1 / 0.75)
    assert _close(0.75 * (1 - math.cos(al)) + 1 - math.sin(al), 0.5)
    Tn = _simpson(lambda u: min(math.sin(u), 5 / 12 * math.cos(u)), 0, math.pi / 2, 20000)
    assert abs(Tn - 1 / 3) < 1e-6
    # 面積の最小
    S = integrate(exp(x) - exp(t) * (x - t + 1), (x, 0, 2))
    assert _eq(S, E**2 - 1 - exp(t) * (4 - 2 * t))
    assert _eq(diff(S, t), 2 * exp(t) * (t - 1))
    Sf = lambda s: math.e**2 - 1 - math.exp(s) * (4 - 2 * s)
    vals = [Sf(s) for s in np.linspace(0, 2, 2001)]
    assert abs(min(vals) - (math.e**2 - 2 * math.e - 1)) < 1e-9 and abs(Sf(1) - min(vals)) < 1e-12
    S2 = integrate(log(t) + (x - t) / t - log(x), (x, 1, 3))
    S2f = lambda s: float(S2.subs(t, s))
    vals = [S2f(s) for s in np.linspace(1, 3, 801)]
    m2 = 2 + 2 * math.log(2) - 3 * math.log(3)
    assert abs(min(vals) - m2) < 1e-9 and abs(S2f(2) - m2) < 1e-12 and m2 > 0
    # 無限級数
    assert _eq(diff(-exp(-x) * (sin(x) + cos(x)) / 2, x), exp(-x) * sin(x))
    for nn in range(4):
        num = _simpson(lambda u: abs(math.exp(-u) * math.sin(u)), nn * math.pi, (nn + 1) * math.pi, 4000)
        assert abs(num - (1 + math.exp(-math.pi)) / 2 * math.exp(-nn * math.pi)) < 1e-10
        num = _simpson(lambda u: abs(math.exp(-2 * u) * math.sin(u)), nn * math.pi, (nn + 1) * math.pi, 4000)
        assert abs(num - (1 + math.exp(-2 * math.pi)) / 5 * math.exp(-2 * nn * math.pi)) < 1e-10
    tot = sum((1 + math.exp(-math.pi)) / 2 * math.exp(-m * math.pi) for m in range(60))
    assert _close(tot, (math.exp(math.pi) + 1) / (2 * (math.exp(math.pi) - 1)))
    tot = sum((1 + math.exp(-2 * math.pi)) / 5 * math.exp(-2 * m * math.pi) for m in range(60))
    assert _close(tot, (math.exp(2 * math.pi) + 1) / (5 * (math.exp(2 * math.pi) - 1)))


# ---------------------------------------------------------------- 第2節の図
def _shoe(pts):
    """多角形（閉曲線の近似）の面積（靴ひも公式）。"""
    P = np.array(pts, dtype=float)
    xs, ys = P[:, 0], P[:, 1]
    return 0.5 * abs(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1)))


def _f22():
    g = _G(220, 100, (-0.4, 6.9), (-0.45, 2.55), eq=True)
    fx, fy = (lambda u: u - math.sin(u)), (lambda u: 1 - math.cos(u))
    g.poly([(fx(2 * math.pi * i / 200), fy(2 * math.pi * i / 200)) for i in range(201)])
    g.axes()
    g.pcurve(fx, fy, 0, 2 * math.pi)
    g.xtick(2 * math.pi, "2π")
    g.xtick(math.pi, "π")
    g.seg((math.pi, 0), (math.pi, 2))
    g.txt(math.pi, 2, "2", dx=0, dy=-3)
    return g.svg()


def _f23():
    g = _G(170, 130, (-0.75, 1.3), (-0.8, 0.8), eq=True)
    up = lambda u: u * math.sqrt(1 - u)
    g.band(lambda u: -up(u), up, 0, 1)
    g.axes()
    g.curve(up, -0.7, 1, n=300)
    g.curve(lambda u: -up(u), -0.7, 1, n=300)
    g.xtick(1, "1", dy=11, dx=4)
    g.txt(0.25, -0.66, "y²=x²(1−x)", anc="start", it=True, size=9)
    return g.svg()


def _f24():
    g = _G(150, 150, (-0.3, 1.35), (-1.15, 1.15), eq=True)
    fx, fy = math.sin, (lambda u: math.sin(2 * u))
    g.poly([(fx(math.pi * i / 200), fy(math.pi * i / 200)) for i in range(201)])
    g.axes()
    g.pcurve(fx, fy, 0, math.pi)
    g.xtick(1, "1", dy=11, dx=4)
    return g.svg()


def _f25():
    g = _G(170, 150, (-0.45, 2.3), (-1.4, 1.4), eq=True)
    r = lambda u: 1 + math.cos(u)
    g.poly([(r(2 * math.pi * i / 240) * math.cos(2 * math.pi * i / 240), r(2 * math.pi * i / 240) * math.sin(2 * math.pi * i / 240)) for i in range(241)])
    g.axes()
    g.pcurve(lambda u: r(u) * math.cos(u), lambda u: r(u) * math.sin(u), 0, 2 * math.pi)
    th0 = 0.9
    g.seg((0, 0), (r(th0) * math.cos(th0), r(th0) * math.sin(th0)), col=C2, dash="")
    g.txt(0.42, 0.15, "θ", it=True, size=9, col=C2)
    g.txt(0.62, 0.95, "r", it=True, size=10, col=C2)
    g.xtick(2, "2", dy=11, dx=4)
    return g.svg()


def _f26():
    g = _G(160, 160, (-1.6, 2.0), (-1.6, 2.0), eq=True)
    fx = lambda u: 3 * u / (1 + u**3)
    fy = lambda u: 3 * u * u / (1 + u**3)
    loop = [(fx(math.tan(math.pi / 2 * i / 200)), fy(math.tan(math.pi / 2 * i / 200))) if i < 200 else (0, 0) for i in range(201)]
    g.poly(loop)
    g.axes()
    g._pl(loop, C1, 1.4, "")
    g.pcurve(fx, fy, -0.7, 0, n=600)
    g.pcurve(fx, fy, -8.0, -1.2, n=900)
    g.curve(lambda u: -1 - u, -1.0, 2.0, col=CG, w=0.8, dash=DASH)
    g.seg((0, 0), (1.6, 1.6), col=CG)
    g.txt(1.95, 1.75, "y=x", anc="end", it=True, size=9, col="#666")
    g.txt(1.95, -1.25, "x+y+1=0", anc="end", it=True, size=8, col="#666")
    return g.svg()


# ---------------------------------------------------------------- 節2
SEC.append({"title": r"面積（2）　陰関数・媒介変数・極座標で表された曲線",
"base": r"""・楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ で囲まれた部分の面積は $\pi ab$。$\displaystyle\int_0^a\sqrt{a^2-x^2}\,dx=\frac{\pi a^2}4$（四分円の面積）を使う。<br>
・陰関数 $F(x,\ y)=0$ で表された曲線：$y$ について解き，対称性（$x$ 軸・$y$ 軸・原点・直線 $y=x$ に関する対称）を利用する。<br>
・媒介変数表示 $x=f(t)$，$y=g(t)$：$\displaystyle S=\int_a^by\,dx=\int_\alpha^\beta g(t)f'(t)\,dt$（$x=a,\ b$ に $t=\alpha,\ \beta$ が対応，$y\geqq0$）。$x$ が $t$ の単調関数でないときは区間を分ける。<br>
・極方程式 $r=f(\theta)$ の曲線と2つの半直線 $\theta=\alpha$，$\theta=\beta$ で囲まれた部分の面積は　$\displaystyle S=\frac12\int_\alpha^\beta r^2\,d\theta$（中心角 $\Delta\theta$ の細い扇形 $\dfrac12r^2\Delta\theta$ を加えると考える）。""",
"items": [
 {"lv": 1, "title": r"楕円の面積",
  "q": r"楕円 $\dfrac{x^2}9+\dfrac{y^2}4=1$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"対称性から第1象限の部分の4倍。$\displaystyle\int_0^3\sqrt{9-x^2}\,dx$ は計算せずに「半径 $3$ の円の $\dfrac14$」と見る。",
  "sol": r"楕円は $x$ 軸，$y$ 軸に関して対称で，$y\geqq0$ の部分は $y=\dfrac23\sqrt{9-x^2}$ だから<br>"
         r"$\displaystyle S=4\int_0^3\frac23\sqrt{9-x^2}\,dx=\frac83\int_0^3\sqrt{9-x^2}\,dx$<br>"
         r"$\displaystyle\int_0^3\sqrt{9-x^2}\,dx$ は半径 $3$ の円の面積の $\dfrac14$ で $\dfrac94\pi$ だから　$S=\dfrac83\cdot\dfrac94\pi=\boldsymbol{6\pi}$",
  "note": r"一般に楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ の面積は $\pi ab$（円を $y$ 軸方向に $\dfrac ba$ 倍に縮めた図形）。媒介変数 $x=3\cos\theta$，$y=2\sin\theta$ を使って $\displaystyle S=4\int_{\frac\pi2}^0 2\sin\theta\cdot(-3\sin\theta)\,d\theta=24\int_0^{\frac\pi2}\sin^2\theta\,d\theta=6\pi$ としてもよい。",
  "ex": r"楕円 $\dfrac{x^2}4+y^2=1$ の内部のうち，$x\geqq1$ の部分の面積を求めよ。",
  "exa": r"$\dfrac23\pi-\dfrac{\sqrt3}2$"},
 {"lv": 1, "title": r"媒介変数表示の曲線と面積（サイクロイド）",
  "q": r"サイクロイド $x=\theta-\sin\theta$，$y=1-\cos\theta\ (0\leqq\theta\leqq2\pi)$ と $x$ 軸で囲まれた部分の面積 $S$ を求めよ。" + _f22(),
  "hint": r"$\displaystyle S=\int_0^{2\pi}y\,dx$ を $\theta$ の積分に置換する。$dx=(1-\cos\theta)\,d\theta$，$x=0,\ 2\pi$ に $\theta=0,\ 2\pi$ が対応。",
  "sol": r"$\dfrac{dx}{d\theta}=1-\cos\theta\geqq0$ より $x$ は $\theta$ とともに $0$ から $2\pi$ まで増加し，$y=1-\cos\theta\geqq0$ である。よって<br>"
         r"$\displaystyle S=\int_0^{2\pi}y\,dx=\int_0^{2\pi}(1-\cos\theta)^2\,d\theta=\int_0^{2\pi}\left(\frac32-2\cos\theta+\frac{\cos2\theta}2\right)d\theta=\boldsymbol{3\pi}$",
  "note": r"サイクロイドは半径 $1$ の円が $x$ 軸上を転がるとき，円周上の定点が描く曲線。1つの弧の下の面積は，転がる円の面積 $\pi$ のちょうど $3$ 倍である。",
  "ex": r"アステロイド $x=\cos^3\theta$，$y=\sin^3\theta\ (0\leqq\theta\leqq2\pi)$ で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac38\pi$"},
 {"lv": 2, "title": r"陰関数で表された曲線（ループ）の面積",
  "q": r"曲線 $y^2=x^2(1-x)$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$y^2\geqq0$ から $x$ の範囲が分かる。$y=\pm x\sqrt{1-x}$ と解けるので，曲線は $x$ 軸に関して対称。上半分の面積を2倍する。",
  "sol": _f23() + r"$y^2=x^2(1-x)\geqq0$ より $x\leqq1$。$x$ を固定すると $y=\pm x\sqrt{1-x}$ だから，曲線は $x$ 軸に関して対称である。<br>"
         r"$0\leqq x\leqq1$ の部分は2曲線 $y=x\sqrt{1-x}$，$y=-x\sqrt{1-x}$ からなり，原点と点 $(1,\ 0)$ で結ばれて閉曲線をつくる（$x<0$ の部分は原点から左へのびる2本の枝で，囲まれた部分をつくらない）。よって<br>"
         r"$\displaystyle S=2\int_0^1x\sqrt{1-x}\,dx$<br>"
         r"$1-x=u$ とおくと　$\displaystyle\int_0^1x\sqrt{1-x}\,dx=\int_0^1(1-u)\sqrt u\,du=\Big[\frac23u^{\frac32}-\frac25u^{\frac52}\Big]_0^1=\frac4{15}$<br>"
         r"したがって　$S=\boldsymbol{\dfrac8{15}}$",
  "note": r"陰関数の曲線は，まず「とり得る $x$ の範囲」「対称性」「座標軸との交点」を調べて概形をつかむ。このループは $x=\dfrac23$ のとき $y$ が最大 $\dfrac{2\sqrt3}9$ となる。",
  "ex": r"曲線 $\sqrt x+\sqrt y=1$ と $x$ 軸，$y$ 軸で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac16$"},
 {"lv": 3, "title": r"媒介変数表示の閉曲線の面積（$x$ が往復する）",
  "q": r"曲線 $C:\ x=\sin t,\ y=\sin2t\ (0\leqq t\leqq\pi)$ で囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$x=\sin t$ は $t=\dfrac\pi2$ で増加から減少に変わるので，曲線を2つの弧に分ける。$t$ を $\pi-t$ にかえると $(x,\ y)$ は $(x,\ -y)$ に移る（$x$ 軸対称）ことを使うと，上側の弧だけで済む。",
  "sol": _f24() + r"$\sin(\pi-t)=\sin t$，$\sin2(\pi-t)=-\sin2t$ だから，$\dfrac\pi2\leqq t\leqq\pi$ の部分は，$0\leqq t\leqq\dfrac\pi2$ の部分を $x$ 軸に関して折り返したものである。<br>"
         r"$0\leqq t\leqq\dfrac\pi2$ では $x=\sin t$ は $0$ から $1$ まで増加し，$y=2\sin t\cos t\geqq0$。よって $C$ は $x$ 軸に関して対称な閉曲線で<br>"
         r"$\displaystyle S=2\int_0^1y\,dx=2\int_0^{\frac\pi2}\sin2t\cdot\cos t\,dt=4\int_0^{\frac\pi2}\sin t\cos^2t\,dt=4\Big[-\frac{\cos^3t}3\Big]_0^{\frac\pi2}=\boldsymbol{\frac43}$",
  "note": r"対称性が使えないときは，上側の弧（$x$ が増加）と下側の弧（$x$ が減少）を別々に $\int y\,dx$ で表して差をとる。結果として，閉曲線を時計回りに1周するときの $\displaystyle\int y\frac{dx}{dt}\,dt$ が面積になる。実際 $\displaystyle\int_0^\pi\sin2t\cos t\,dt=\frac43$ である。",
  "ex": r"曲線 $x=t^2,\ y=t^3-3t\ (-\sqrt3\leqq t\leqq\sqrt3)$ で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac{24\sqrt3}5$"},
 {"lv": 3, "title": r"極方程式で表された曲線の面積",
  "q": r"極方程式 $r=1+\cos\theta\ (0\leqq\theta\leqq2\pi)$ で表される曲線（カージオイド）で囲まれた部分の面積 $S$ を求めよ。" + _f25(),
  "hint": r"原点からのびる細い扇形に分けて考えると $\displaystyle S=\frac12\int_0^{2\pi}r^2\,d\theta$。$\cos^2\theta$ は半角の公式で次数を下げる。",
  "sol": r"$r=1+\cos\theta\geqq0$ で，曲線は原点を囲み，各半直線 $\theta$ と1点で交わるから<br>"
         r"$\displaystyle S=\frac12\int_0^{2\pi}(1+\cos\theta)^2\,d\theta=\frac12\int_0^{2\pi}\left(1+2\cos\theta+\frac{1+\cos2\theta}2\right)d\theta=\frac12(2\pi+\pi)=\boldsymbol{\frac32\pi}$",
  "note": r"<b>公式の理由</b>：$\theta=\alpha$ から $\theta$ までの部分の面積を $S(\theta)$ とすると，$\theta$ から $\theta+\Delta\theta$ までの部分の面積 $\Delta S$ は，半径が $r$ の最小値・最大値の2つの扇形の面積ではさまれるので，$\Delta\theta\to0$ として $S'(\theta)=\dfrac12r^2$。<br>媒介変数表示 $x=(1+\cos\theta)\cos\theta$，$y=(1+\cos\theta)\sin\theta$ と見て $\int y\,dx$ で計算することもできる。",
  "ex": r"極方程式 $r^2=\cos2\theta$ で表される曲線（レムニスケート）で囲まれた部分の面積を求めよ。",
  "exa": r"$1$"},
 {"lv": 4, "title": r"極座標に直して求める面積（デカルトの葉線）",
  "q": r"曲線 $x^3+y^3=3xy$ のうち $x\geqq0$，$y\geqq0$ の部分は閉曲線（ループ）をなす。このループで囲まれた部分の面積 $S$ を求めよ。",
  "hint": r"$y$ について解けない。原点を通る半直線との交点を考える，すなわち $x=r\cos\theta$，$y=r\sin\theta$ を代入すると $r$ が $\theta$ で表せる。$\tan\theta=u$ の置換で積分できる。",
  "sol": _f26() + r"$x=r\cos\theta$，$y=r\sin\theta\ (r\geqq0)$ を代入すると　$r^3(\cos^3\theta+\sin^3\theta)=3r^2\cos\theta\sin\theta$<br>"
         r"$0\leqq\theta\leqq\dfrac\pi2$ では $\cos^3\theta+\sin^3\theta>0$ だから，原点以外の点は　$r=\dfrac{3\cos\theta\sin\theta}{\cos^3\theta+\sin^3\theta}$（これを $f(\theta)$ とおく）<br>"
         r"$f(0)=f\left(\dfrac\pi2\right)=0$，$0<\theta<\dfrac\pi2$ で $f(\theta)>0$ だから，ループの内部は $0\leqq r\leqq f(\theta)$ と表される。また，方程式は $x$ と $y$ を入れかえても変わらないので，曲線は直線 $y=x$ に関して対称である。よって<br>"
         r"$\displaystyle S=2\cdot\frac12\int_0^{\frac\pi4}f(\theta)^2\,d\theta=\int_0^{\frac\pi4}\frac{9\cos^2\theta\sin^2\theta}{(\cos^3\theta+\sin^3\theta)^2}\,d\theta=\int_0^{\frac\pi4}\frac{9\tan^2\theta}{(1+\tan^3\theta)^2}\cdot\frac{d\theta}{\cos^2\theta}$<br>"
         r"（分母・分子を $\cos^6\theta$ で割った。）$\tan\theta=u$ とおくと $\dfrac{d\theta}{\cos^2\theta}=du$，$\theta:0\to\dfrac\pi4$ のとき $u:0\to1$ だから<br>"
         r"$\displaystyle S=\int_0^1\frac{9u^2}{(1+u^3)^2}\,du=\Big[-\frac3{1+u^3}\Big]_0^1=-\frac32+3=\boldsymbol{\frac32}$",
  "note": r"$u=\tan\theta=\dfrac yx$ は原点を通る直線 $y=ux$ の傾きで，これを媒介変数にすると $x=\dfrac{3u}{1+u^3}$，$y=\dfrac{3u^2}{1+u^3}$ と表せる。この曲線は直線 $x+y+1=0$ を漸近線にもつ。$\displaystyle\int_0^{\frac\pi2}$ のまま置換すると $u$ の範囲が $0\to\infty$ となるので，対称性で区間を半分にしておくのがよい。",
  "ex": r"曲線 $(x^2+y^2)^3=4x^2y^2$ で囲まれた部分の面積を求めよ。",
  "exa": r"$\dfrac\pi2$"},
]})


def _v2():
    # 楕円
    assert _eq(4 * integrate(Rational(2, 3) * sqrt(9 - x**2), (x, 0, 3)), 6 * pi)
    assert _eq(integrate(sqrt(4 - x**2), (x, 1, 2)), 2 * pi / 3 - sqrt(3) / 2)
    rnd = random.Random(26)
    hit = sum(1 for _ in range(200000) if (lambda p, q: p * p / 4 + q * q <= 1)(1 + rnd.random(), rnd.uniform(-1, 1)))
    assert abs(hit / 200000 * 2 - (2 * math.pi / 3 - math.sqrt(3) / 2)) < 0.01
    # サイクロイド・アステロイド
    assert _eq(integrate((1 - cos(th))**2, (th, 0, 2 * pi)), 3 * pi)
    assert _eq(integrate(12 * sin(th)**4 * cos(th)**2, (th, 0, pi / 2)), 3 * pi / 8)
    pts = [(math.cos(u)**3, math.sin(u)**3) for u in np.linspace(0, 2 * math.pi, 20001)[:-1]]
    assert abs(_shoe(pts) - 3 * math.pi / 8) < 1e-6
    pts = [(u - math.sin(u), 1 - math.cos(u)) for u in np.linspace(0, 2 * math.pi, 20001)]
    assert abs(_shoe(pts) - 3 * math.pi) < 1e-6
    # ループ
    assert _eq(2 * integrate(x * sqrt(1 - x), (x, 0, 1)), Rational(8, 15))
    hit = sum(1 for _ in range(200000) if (lambda p, q: q * q <= p * p * (1 - p))(rnd.random(), rnd.uniform(-0.5, 0.5)))
    assert abs(hit / 200000 - 8 / 15) < 0.006
    assert _eq(integrate((1 - sqrt(x))**2, (x, 0, 1)), Rational(1, 6))
    xm = Rational(2, 3)
    assert _eq(xm * sqrt(1 - xm), 2 * sqrt(3) / 9)
    # 媒介変数の閉曲線
    assert _eq(2 * integrate(sin(2 * t) * cos(t), (t, 0, pi / 2)), Rational(4, 3))
    assert _eq(integrate(sin(2 * t) * cos(t), (t, 0, pi)), Rational(4, 3))
    pts = [(math.sin(u), math.sin(2 * u)) for u in np.linspace(0, math.pi, 20001)[:-1]]
    assert abs(_shoe(pts) - 4 / 3) < 1e-6
    r3 = math.sqrt(3)
    pts = [(u * u, u**3 - 3 * u) for u in np.linspace(-r3, r3, 20001)[:-1]]
    assert abs(_shoe(pts) - 24 * r3 / 5) < 1e-6
    assert _eq(2 * integrate((t**3 - 3 * t) * 2 * t, (t, 0, -sqrt(3))), 24 * sqrt(3) / 5)
    # カージオイド・レムニスケート
    assert _eq(integrate((1 + cos(th))**2, (th, 0, 2 * pi)) / 2, 3 * pi / 2)
    pts = [((1 + math.cos(u)) * math.cos(u), (1 + math.cos(u)) * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 20001)[:-1]]
    assert abs(_shoe(pts) - 1.5 * math.pi) < 1e-6
    lem = [(math.sqrt(max(math.cos(2 * u), 0)) * math.cos(u), math.sqrt(max(math.cos(2 * u), 0)) * math.sin(u)) for u in np.linspace(-math.pi / 4, math.pi / 4, 20001)]
    assert abs(2 * _shoe(lem) - 1) < 1e-5
    assert _eq(2 * integrate(cos(2 * th), (th, -pi / 4, pi / 4)) / 2, 1)
    # 葉線
    assert _eq(integrate(9 * t**2 / (1 + t**3)**2, (t, 0, 1)), Rational(3, 2))
    f = lambda u: 3 * math.cos(u) * math.sin(u) / (math.cos(u)**3 + math.sin(u)**3)
    pts = [(f(u) * math.cos(u), f(u) * math.sin(u)) for u in np.linspace(0, math.pi / 2, 40001)]
    assert abs(_shoe(pts) - 1.5) < 1e-6
    for u in np.linspace(0.05, 1.5, 30):
        X, Y = f(u) * math.cos(u), f(u) * math.sin(u)
        assert abs(X**3 + Y**3 - 3 * X * Y) < 1e-9
    # (x^2+y^2)^3=4x^2y^2 → r=|sin2θ|
    pts = []
    for u in np.linspace(0, 2 * math.pi, 40001)[:-1]:
        r = abs(math.sin(2 * u))
        X, Y = r * math.cos(u), r * math.sin(u)
        assert abs((X * X + Y * Y)**3 - 4 * X * X * Y * Y) < 1e-12
        pts.append((X, Y))
    assert abs(_shoe(pts) - math.pi / 2) < 1e-6
    assert _eq(integrate(sin(2 * th)**2, (th, 0, 2 * pi)) / 2, pi / 2)


# ---------------------------------------------------------------- 第3節の図
def _mc_rev(inside, box, N=300000, seed=1):
    """直方体 box=((x0,x1),(y0,y1),(z0,z1)) に一様に点をとり、inside(x,y,z) の割合から体積を推定する。"""
    rg = np.random.default_rng(seed)
    (a0, a1), (b0, b1), (c0, c1) = box
    X = rg.uniform(a0, a1, N)
    Y = rg.uniform(b0, b1, N)
    Z = rg.uniform(c0, c1, N)
    vol = (a1 - a0) * (b1 - b0) * (c1 - c0)
    return vol * np.count_nonzero(inside(X, Y, Z)) / N


def _f31():
    # 斜投影：u = x + 0.42y, v = z + 0.3y
    P = lambda X, Y, Z: (X + 0.42 * Y, Z + 0.3 * Y)
    g = _G(200, 150, (-1.6, 1.7), (-0.55, 1.95), eq=True)
    circ = [P(math.cos(u), math.sin(u), 0) for u in np.linspace(0, 2 * math.pi, 200)]
    g.poly(circ, fill="#eef2fa", op=1, stroke=C1, w=1.0)
    t0 = 0.25
    w = math.sqrt(1 - t0 * t0)
    tri = [P(t0, -w, 0), P(t0, w, 0), P(t0, 0, math.sqrt(3) * w)]
    g.poly(tri, fill=CF2, op=0.85, stroke=C2, w=1.2)
    g.seg(P(-1.45, 0, 0), P(1.6, 0, 0), col="#333", dash="")
    g.pt(*P(-1, 0, 0), col="#333")
    g.pt(*P(1, 0, 0), col="#333")
    g.txt(*P(-1, 0, 0), "A", dx=-5, dy=12, size=10)
    g.txt(*P(1, 0, 0), "B", dx=6, dy=12, size=10)
    g.txt(*P(1.6, 0, 0), "x", dx=2, dy=-4, it=True, size=11)
    g.txt(*P(t0, 0, 0), "t", dx=5, dy=11, it=True, size=10)
    return g.svg()


def _f35():
    g = _G(200, 105, (-0.25, 3.45), (-0.25, 1.4), eq=True)
    g.band(lambda u: 0, math.sin, 0, math.pi)
    g.axes()
    g.curve(math.sin, -0.1, 3.35)
    g.seg((-0.2, 1), (3.4, 1), col=C2, dash="", w=1.1)
    g.txt(3.4, 1.07, "y=1", anc="end", it=True, size=9, col=C2)
    u0 = 0.75
    g.seg((u0, math.sin(u0)), (u0, 1), col=C3, dash="", w=1.3)
    g.seg((u0, 0), (u0, math.sin(u0)), col=CG)
    g.xtick(math.pi, "π")
    return g.svg()


def _f36():
    g = _G(200, 150, (-0.2, 4.2), (-1.25, 1.25), eq=True)
    a0, a1 = math.pi / 4, 5 * math.pi / 4
    g.band(math.cos, math.sin, a0, a1)
    g.axes()
    g.curve(math.sin, -0.1, 4.1)
    g.curve(math.cos, -0.1, 4.1, col=C2)
    # x 軸より下の部分を折り返したもの（破線）
    neg = lambda u: max(-min(math.sin(u), 0), 0)
    g.curve(lambda u: -math.cos(u), math.pi / 2, a1, col=C2, w=0.9, dash=DASH)
    g.curve(lambda u: -math.sin(u), math.pi, a1, col=C1, w=0.9, dash=DASH)
    for u in (3 * math.pi / 4,):
        g.seg((u, -0.8), (u, 0.8))
        g.txt(u, -0.8, "3π/4", dy=10, size=9)
    g.xtick(math.pi / 2, "π/2", dy=11, dx=-6)
    g.txt(0.3, -0.5, "y=cos x", anc="start", it=True, size=9, col=C2)
    g.txt(1.65, 1.07, "y=sin x", anc="start", it=True, size=9)
    return g.svg()


# ---------------------------------------------------------------- 節3
SEC.append({"title": r"体積（1）　断面積・x 軸のまわりの回転体",
"base": r"""・$x$ 軸に垂直な平面 $x=t$ による切り口の面積が $S(t)$ である立体の，$a\leqq x\leqq b$ の部分の体積は　$\displaystyle V=\int_a^bS(x)\,dx$<br>
・曲線 $y=f(x)$ と $x$ 軸，2直線 $x=a$，$x=b$ で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積は　$\displaystyle V=\pi\int_a^b\{f(x)\}^2\,dx$<br>
・$0\leqq g(x)\leqq f(x)$ のとき，2曲線の間の部分を回転すると　$\displaystyle V=\pi\int_a^b\left[\{f(x)\}^2-\{g(x)\}^2\right]dx$（$\pi\int(f-g)^2\,dx$ ではない）<br>
・回転軸が直線 $y=c$ のときは，各 $x$ で軸からの距離の最大値・最小値を外径・内径にとる。図形が軸の両側にあるときは，一方を軸に関して折り返し，重なりを考えて外側の境界だけを使う。""",
"items": [
 {"lv": 1, "title": r"断面積から体積を求める",
  "q": r"底面が半径 $1$ の円で，底面の1つの直径 $\mathrm{AB}$ に垂直な平面で切った切り口がつねに正三角形（1辺は底面上にある）である立体の体積 $V$ を求めよ。",
  "hint": r"$\mathrm{AB}$ を $x$ 軸にとり，平面 $x=t$ による切り口の面積 $S(t)$ を $t$ で表して積分する。回転体でなくても，切り口の面積が分かれば体積が求まる。",
  "sol": _f31() + r"直径 $\mathrm{AB}$ を $x$ 軸，底面の中心を原点にとり，底面を $x^2+y^2\leqq1$（$xy$ 平面上）とする。<br>"
         r"$-1\leqq t\leqq1$ のとき，平面 $x=t$ と底面の共通部分は長さ $2\sqrt{1-t^2}$ の線分で，切り口はこれを1辺とする正三角形だから，その面積は<br>"
         r"$S(t)=\dfrac{\sqrt3}4\left(2\sqrt{1-t^2}\right)^2=\sqrt3(1-t^2)$<br>"
         r"$\displaystyle V=\int_{-1}^1\sqrt3(1-t^2)\,dt=2\sqrt3\int_0^1(1-t^2)\,dt=2\sqrt3\cdot\frac23=\boldsymbol{\frac{4\sqrt3}3}$",
  "note": r"体積の基本は「切り口の面積を積分する」こと。回転体の公式 $\pi\int y^2\,dx$ も，切り口が半径 $y$ の円（面積 $\pi y^2$）である場合にすぎない。",
  "ex": r"底面が半径 $1$ の円で，底面の1つの直径に垂直な平面で切った切り口がつねに正方形（1辺は底面上にある）である立体の体積を求めよ。",
  "exa": r"$\dfrac{16}3$"},
 {"lv": 1, "title": r"$x$ 軸のまわりの回転体の体積",
  "q": r"次の図形を $x$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。<br>(1) 曲線 $y=\sqrt x$ と $x$ 軸および直線 $x=4$ で囲まれた部分<br>(2) 曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた部分",
  "hint": r"$x$ 軸に垂直な平面で切った切り口は半径 $|y|$ の円で，面積は $\pi y^2$。$\sin^2x$ は半角の公式で次数を下げる。",
  "sol": r"(1) $\displaystyle V=\pi\int_0^4(\sqrt x)^2\,dx=\pi\Big[\frac{x^2}2\Big]_0^4=\boldsymbol{8\pi}$<br>"
         r"(2) $\displaystyle V=\pi\int_0^\pi\sin^2x\,dx=\pi\int_0^\pi\frac{1-\cos2x}2\,dx=\pi\Big[\frac x2-\frac{\sin2x}4\Big]_0^\pi=\boldsymbol{\frac{\pi^2}2}$",
  "ex": r"次の図形を $x$ 軸のまわりに1回転してできる立体の体積を求めよ。<br>(1) 曲線 $y=e^x$ と $x$ 軸，$y$ 軸および直線 $x=1$ で囲まれた部分<br>(2) 曲線 $y=\cos x\ \left(0\leqq x\leqq\dfrac\pi2\right)$ と $x$ 軸，$y$ 軸で囲まれた部分",
  "exa": r"(1) $\dfrac\pi2(e^2-1)$　(2) $\dfrac{\pi^2}4$"},
 {"lv": 1, "title": r"2曲線の間の部分の回転",
  "q": r"曲線 $y=\sqrt x$ と直線 $y=\dfrac x2$ で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"切り口は穴のあいた円（円環）。外側の円の面積から内側の円の面積を引く。",
  "sol": r"$\sqrt x=\dfrac x2$ より $x=0,\ 4$。$0\leqq x\leqq4$ で $\sqrt x\geqq\dfrac x2\geqq0$ だから，平面 $x=t$ による切り口は外径 $\sqrt t$，内径 $\dfrac t2$ の円環である。<br>"
         r"$\displaystyle V=\pi\int_0^4\left\{(\sqrt x)^2-\left(\frac x2\right)^2\right\}dx=\pi\Big[\frac{x^2}2-\frac{x^3}{12}\Big]_0^4=\pi\left(8-\frac{16}3\right)=\boldsymbol{\frac{8}{3}\pi}$",
  "note": r"$\displaystyle\pi\int_0^4\left(\sqrt x-\frac x2\right)^2dx=\frac8{15}\pi$ とするのは典型的な誤り。$(f-g)^2$ は円環の面積ではない。",
  "ex": r"2曲線 $y=\sin x$，$y=\cos x$ と $y$ 軸で囲まれた部分 $\left(0\leqq x\leqq\dfrac\pi4\right)$ を $x$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac\pi2$"},
 {"lv": 2, "title": r"球の一部の体積",
  "q": r"半径 $r$ の球を，中心からの距離が $a\ (0\leqq a<r)$ の平面で切ったとき，小さい方の部分の体積 $V$ を $r,\ a$ で表せ。",
  "hint": r"球は円 $x^2+y^2=r^2$ を $x$ 軸のまわりに回転したもの。切る平面を $x=a$ とすれば，$a\leqq x\leqq r$ の部分の回転体になる。",
  "sol": r"球を，円 $x^2+y^2=r^2$ を $x$ 軸のまわりに1回転してできる球面で囲まれた立体と考え，切る平面を $x=a$ とする。小さい方の部分は $a\leqq x\leqq r$ の部分だから<br>"
         r"$\displaystyle V=\pi\int_a^r(r^2-x^2)\,dx=\pi\Big[r^2x-\frac{x^3}3\Big]_a^r=\frac\pi3(2r^3-3r^2a+a^3)=\boldsymbol{\frac\pi3(r-a)^2(2r+a)}$",
  "note": r"$a=0$ とすると半球の体積 $\dfrac23\pi r^3$ になる。切り取られる部分の高さを $h=r-a$ とすると $V=\dfrac{\pi h^2(3r-h)}3$ とも書ける。同様に，楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ を $x$ 軸のまわりに回転した回転楕円体の体積は $\dfrac43\pi ab^2$。",
  "ex": r"半径 $3$ の球を，中心からの距離がそれぞれ $1$ と $2$ である平行な2平面（中心に関して同じ側にある）で切ったとき，2平面ではさまれた部分の体積を求めよ。",
  "exa": r"$\dfrac{20}3\pi$"},
 {"lv": 2, "title": r"$x$ 軸に平行な直線のまわりの回転",
  "q": r"曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた部分を，直線 $y=1$ のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"各 $x$ で，図形の点の回転軸 $y=1$ からの距離は $1-\sin x$ 以上 $1$ 以下。切り口は外径 $1$，内径 $1-\sin x$ の円環になる。",
  "sol": _f35() + r"$0\leqq x\leqq\pi$ のとき $0\leqq\sin x\leqq1$ だから，図形は直線 $y=1$ の下側にあり，$x$ を固定したときの線分 $0\leqq y\leqq\sin x$ 上の点と直線 $y=1$ との距離は $1-\sin x$ 以上 $1$ 以下である。よって切り口は外径 $1$，内径 $1-\sin x$ の円環で<br>"
         r"$\displaystyle V=\pi\int_0^\pi\left\{1^2-(1-\sin x)^2\right\}dx=\pi\int_0^\pi(2\sin x-\sin^2x)\,dx=\pi\left(4-\frac\pi2\right)=\boldsymbol{4\pi-\frac{\pi^2}2}$",
  "note": r"$\displaystyle\int_0^\pi2\sin x\,dx=4$，$\displaystyle\int_0^\pi\sin^2x\,dx=\frac\pi2$ を使った。回転軸が $y=c$ のときは「$y-c$」を半径と考えて，$x$ 軸の場合と同じように扱えばよい。",
  "ex": r"曲線 $y=\log x$，$x$ 軸および直線 $x=e$ で囲まれた部分を，直線 $y=1$ のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\pi(4-e)$"},
 {"lv": 3, "title": r"$x$ 軸の両側にまたがる図形の回転",
  "q": r"$\dfrac\pi4\leqq x\leqq\dfrac54\pi$ において，2曲線 $y=\sin x$，$y=\cos x$ で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$x$ 軸より下にある部分を $x$ 軸に関して折り返すと，回転体は「折り返した図形ともとの図形を合わせたもの」の回転体と同じ。各 $x$ で，$|y|$ の最大値と，線分が $x$ 軸をまたぐかどうかを調べる。",
  "sol": _f36() + r"$\dfrac\pi4\leqq x\leqq\dfrac54\pi$ で $\cos x\leqq\sin x$。$x$ を固定したとき，線分 $\cos x\leqq y\leqq\sin x$ を $x$ 軸のまわりに回転した切り口を調べる。<br>"
         r"(i) $\dfrac\pi4\leqq x\leqq\dfrac\pi2$：$0\leqq\cos x\leqq\sin x$ で，外径 $\sin x$，内径 $\cos x$ の円環。<br>"
         r"(ii) $\dfrac\pi2\leqq x\leqq\pi$：$\cos x\leqq0\leqq\sin x$ で，半径 $\max\{\sin x,\ -\cos x\}$ の円。$\sin x\geqq-\cos x\iff\sin x+\cos x\geqq0\iff x\leqq\dfrac34\pi$。<br>"
         r"(iii) $\pi\leqq x\leqq\dfrac54\pi$：$\cos x\leqq\sin x\leqq0$ で，外径 $-\cos x$，内径 $-\sin x$ の円環。<br>"
         r"よって<br>"
         r"$\displaystyle\frac V\pi=\int_{\frac\pi4}^{\frac\pi2}(\sin^2x-\cos^2x)\,dx+\int_{\frac\pi2}^{\frac34\pi}\sin^2x\,dx+\int_{\frac34\pi}^{\pi}\cos^2x\,dx+\int_\pi^{\frac54\pi}(\cos^2x-\sin^2x)\,dx$<br>"
         r"ここで　$\displaystyle\int_{\frac\pi4}^{\frac\pi2}(-\cos2x)\,dx=\Big[-\frac{\sin2x}2\Big]_{\frac\pi4}^{\frac\pi2}=\frac12$，$\displaystyle\int_\pi^{\frac54\pi}\cos2x\,dx=\Big[\frac{\sin2x}2\Big]_\pi^{\frac54\pi}=\frac12$，<br>"
         r"$\displaystyle\int_{\frac\pi2}^{\frac34\pi}\sin^2x\,dx=\Big[\frac x2-\frac{\sin2x}4\Big]_{\frac\pi2}^{\frac34\pi}=\frac\pi8+\frac14$，$\displaystyle\int_{\frac34\pi}^\pi\cos^2x\,dx=\Big[\frac x2+\frac{\sin2x}4\Big]_{\frac34\pi}^\pi=\frac\pi8+\frac14$<br>"
         r"したがって　$V=\pi\left(\dfrac32+\dfrac\pi4\right)=\boldsymbol{\dfrac{\pi^2}4+\dfrac32\pi}$",
  "note": r"「上の部分の回転体＋下の部分の回転体」とすると，重なった部分を2回数えてしまう。また，線分が $x$ 軸をまたぐ区間 (ii) では切り口に穴があかないことにも注意。",
  "ex": r"放物線 $y=x^2-2x$ と直線 $y=x$ で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{20}3\pi$"},
]})


def _rev_strip(lo, hi):
    """x を固定し、線分 lo≦y≦hi を x 軸のまわりに回転したときの切り口の面積/π。"""
    if lo <= 0 <= hi:
        return max(hi, -lo)**2
    R, r = max(abs(lo), abs(hi)), min(abs(lo), abs(hi))
    return R * R - r * r


def _v3():
    # 断面積
    assert _eq(integrate(sqrt(3) * (1 - t**2), (t, -1, 1)), 4 * sqrt(3) / 3)
    assert _eq(integrate(4 * (1 - t**2), (t, -1, 1)), Rational(16, 3))
    def tri(X, Y, Z):
        w = np.sqrt(np.clip(1 - X * X, 0, None))
        return (np.abs(Y) <= w) & (Z >= 0) & (Z <= math.sqrt(3) * (w - np.abs(Y)))
    assert abs(_mc_rev(tri, ((-1, 1), (-1, 1), (0, 1.75))) - 4 * math.sqrt(3) / 3) < 0.03
    def sq(X, Y, Z):
        w = np.sqrt(np.clip(1 - X * X, 0, None))
        return (np.abs(Y) <= w) & (Z >= 0) & (Z <= 2 * w)
    assert abs(_mc_rev(sq, ((-1, 1), (-1, 1), (0, 2))) - 16 / 3) < 0.05
    # x 軸回転
    assert _eq(pi * integrate(x, (x, 0, 4)), 8 * pi)
    assert _eq(pi * integrate(sin(x)**2, (x, 0, pi)), pi**2 / 2)
    assert _eq(pi * integrate(exp(2 * x), (x, 0, 1)), pi * (E**2 - 1) / 2)
    assert _eq(pi * integrate(cos(x)**2, (x, 0, pi / 2)), pi**2 / 4)
    # 2曲線の間
    assert solve(sqrt(x) - x / 2, x) == [0, 4]
    assert _eq(pi * integrate(x - x**2 / 4, (x, 0, 4)), 8 * pi / 3)
    assert _eq(pi * integrate((sqrt(x) - x / 2)**2, (x, 0, 4)), 8 * pi / 15)
    assert _eq(pi * integrate(cos(x)**2 - sin(x)**2, (x, 0, pi / 4)), pi / 2)
    # 球の一部
    r_, a_ = symbols("r a", positive=True)
    Vc = pi * integrate(r_**2 - x**2, (x, a_, r_))
    assert _eq(Vc, pi / 3 * (r_ - a_)**2 * (2 * r_ + a_))
    assert _eq(Vc, pi / 3 * (2 * r_**3 - 3 * r_**2 * a_ + a_**3))
    assert _eq(Vc.subs(a_, 0), 2 * pi * r_**3 / 3)
    hh = r_ - a_
    assert _eq(Vc, pi * hh**2 * (3 * r_ - hh) / 3)
    assert _eq(pi * integrate(9 - x**2, (x, 1, 2)), 20 * pi / 3)
    ball = lambda X, Y, Z: (X * X + Y * Y + Z * Z <= 9) & (X >= 1) & (X <= 2)
    assert abs(_mc_rev(ball, ((1, 2), (-3, 3), (-3, 3))) - 20 * math.pi / 3) < 0.15
    # y=1 のまわり
    assert _eq(pi * integrate(1 - (1 - sin(x))**2, (x, 0, pi)), 4 * pi - pi**2 / 2)
    def s35(X, Y, Z):
        rho = np.sqrt((Y - 1)**2 + Z * Z)
        return (rho <= 1) & (rho >= 1 - np.sin(X))
    assert abs(_mc_rev(s35, ((0, math.pi), (0, 2), (-1, 1))) - (4 * math.pi - math.pi**2 / 2)) < 0.06
    assert _eq(pi * integrate(1 - (1 - log(x))**2, (x, 1, E)), pi * (4 - E))
    assert all(0 <= math.log(u) <= 1 for u in np.linspace(1, math.e, 50))
    # x 軸をまたぐ図形
    parts = (integrate(sin(x)**2 - cos(x)**2, (x, pi / 4, pi / 2)), integrate(sin(x)**2, (x, pi / 2, 3 * pi / 4)),
             integrate(cos(x)**2, (x, 3 * pi / 4, pi)), integrate(cos(x)**2 - sin(x)**2, (x, pi, 5 * pi / 4)))
    assert _eq(parts[0], Rational(1, 2)) and _eq(parts[3], Rational(1, 2))
    assert _eq(parts[1], pi / 8 + Rational(1, 4)) and _eq(parts[2], pi / 8 + Rational(1, 4))
    V36 = pi * sum(parts)
    assert _eq(V36, pi**2 / 4 + 3 * pi / 2)
    num = math.pi * _simpson(lambda u: _rev_strip(math.cos(u), math.sin(u)), math.pi / 4, 5 * math.pi / 4, 20000)
    assert abs(num - float(V36)) < 1e-6
    def s36(X, Y, Z):
        rho = np.sqrt(Y * Y + Z * Z)
        lo, hi = np.cos(X), np.sin(X)
        return ((rho >= lo) & (rho <= hi)) | ((-rho >= lo) & (-rho <= hi))
    assert abs(_mc_rev(s36, ((math.pi / 4, 5 * math.pi / 4), (-1, 1), (-1, 1)), N=400000) - float(V36)) < 0.06
    # 練習：y=x^2-2x と y=x
    Vex = pi * (integrate((2 * x - x**2)**2, (x, 0, 1)) + integrate(x**2, (x, 1, 2)) + integrate(x**2 - (x**2 - 2 * x)**2, (x, 2, 3)))
    assert _eq(Vex, 20 * pi / 3)
    num = math.pi * _simpson(lambda u: _rev_strip(u * u - 2 * u, u), 0, 3, 30000)
    assert abs(num - 20 * math.pi / 3) < 1e-5


# ---------------------------------------------------------------- 第4節の図
def _f43():
    g = _G(200, 110, (-0.3, 3.5), (-0.3, 1.45), eq=True)
    g.band(lambda u: 0, math.sin, 0, math.pi)
    g.axes()
    g.curve(math.sin, -0.1, 3.4)
    y0 = 0.62
    x1, x2 = math.asin(y0), math.pi - math.asin(y0)
    g.seg((0, y0), (x2, y0), col=C2, dash="", w=1.1)
    g.pt(x1, y0, col=C2)
    g.pt(x2, y0, col=C2)
    g.txt(x1, y0, "x₁", dx=-1, dy=-5, it=True, size=10, col=C2)
    g.txt(x2, y0, "x₂", dx=6, dy=-5, it=True, size=10, col=C2)
    g.txt(0, y0, "y", dx=-4, dy=4, anc="end", it=True, size=10)
    g.xtick(math.pi, "π")
    return g.svg()


def _f45():
    g = _G(220, 95, (-0.5, 6.9), (-0.35, 2.45), eq=True)
    fx, fy = (lambda u: u - math.sin(u)), (lambda u: 1 - math.cos(u))
    g.poly([(fx(2 * math.pi * i / 200), fy(2 * math.pi * i / 200)) for i in range(201)])
    g.axes()
    g.pcurve(fx, fy, 0, 2 * math.pi)
    y0 = 1.3
    t1 = math.acos(1 - y0)
    t2 = 2 * math.pi - t1
    g.seg((0, y0), (fx(t2), y0), col=C2, dash="", w=1.1)
    g.pt(fx(t1), y0, col=C2)
    g.pt(fx(t2), y0, col=C2)
    g.txt(fx(t1), y0, "x₁", dx=-3, dy=-5, it=True, size=10, col=C2)
    g.txt(fx(t2), y0, "x₂", dx=8, dy=-4, it=True, size=10, col=C2)
    g.xtick(2 * math.pi, "2π")
    g.ytick(2, "2")
    return g.svg()


# ---------------------------------------------------------------- 節4
SEC.append({"title": r"体積（2）　y 軸のまわりの回転体・バウムクーヘン型・媒介変数表示",
"base": r"""・$y$ 軸のまわり：曲線 $x=g(y)$ と $y$ 軸，2直線 $y=c$，$y=d$ で囲まれた部分を回転すると　$\displaystyle V=\pi\int_c^d\{g(y)\}^2\,dy$<br>
・$x$ について解けないときは，$y=f(x)$ で置換して $\displaystyle\pi\int x^2\,dy=\pi\int x^2f'(x)\,dx$ とする（$f(x)$ が単調な区間に分ける）。<br>
・バウムクーヘン型：$0\leqq a<b$，$f(x)\geqq0$ のとき，曲線 $y=f(x)$ と $x$ 軸，2直線 $x=a$，$x=b$ で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積は　$\displaystyle V=2\pi\int_a^bxf(x)\,dx$（半径 $x$，高さ $f(x)$，厚さ $dx$ の薄い円筒 $2\pi xf(x)\,dx$ を集めたもの）<br>
・媒介変数表示 $x=f(t)$，$y=g(t)$ の曲線の回転体：$\displaystyle V=\pi\int y^2\,dx=\pi\int\{g(t)\}^2f'(t)\,dt$""",
"items": [
 {"lv": 2, "title": r"$y$ 軸のまわりの回転体の体積",
  "q": r"曲線 $y=\log x$ と $x$ 軸，$y$ 軸および直線 $y=1$ で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$y$ 軸に垂直な平面で切った切り口は円。$x=e^y$ と $y$ の関数で表して，$\pi\int x^2\,dy$ を計算する。",
  "sol": r"$y=\log x\iff x=e^y$ だから，図形は $0\leqq y\leqq1$，$0\leqq x\leqq e^y$ と表される。<br>"
         r"$y$ 軸に垂直な平面で切った切り口は半径 $e^y$ の円だから<br>"
         r"$\displaystyle V=\pi\int_0^1(e^y)^2\,dy=\pi\Big[\frac{e^{2y}}2\Big]_0^1=\boldsymbol{\frac\pi2(e^2-1)}$",
  "ex": r"曲線 $y=\dfrac1x\ (x>0)$ と $y$ 軸および2直線 $y=1$，$y=3$ で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac23\pi$"},
 {"lv": 2, "title": r"媒介変数表示の曲線の回転体（サイクロイド）",
  "q": r"サイクロイド $x=\theta-\sin\theta$，$y=1-\cos\theta\ (0\leqq\theta\leqq2\pi)$ と $x$ 軸で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$\displaystyle V=\pi\int_0^{2\pi}y^2\,dx$ を $\theta$ の積分に置換する。$(1-\cos\theta)^3$ を展開し，$\cos^2\theta$，$\cos^3\theta$ の積分は次数を下げて求める。",
  "sol": r"$\dfrac{dx}{d\theta}=1-\cos\theta\geqq0$ で，$x:0\to2\pi$ に $\theta:0\to2\pi$ が対応するから<br>"
         r"$\displaystyle V=\pi\int_0^{2\pi}y^2\,dx=\pi\int_0^{2\pi}(1-\cos\theta)^2(1-\cos\theta)\,d\theta=\pi\int_0^{2\pi}(1-3\cos\theta+3\cos^2\theta-\cos^3\theta)\,d\theta$<br>"
         r"$\displaystyle\int_0^{2\pi}\cos\theta\,d\theta=0$，$\displaystyle\int_0^{2\pi}\cos^2\theta\,d\theta=\pi$，$\cos^3\theta=\dfrac{3\cos\theta+\cos3\theta}4$ より $\displaystyle\int_0^{2\pi}\cos^3\theta\,d\theta=0$ だから<br>"
         r"$V=\pi(2\pi+3\pi)=\boldsymbol{5\pi^2}$",
  "note": r"媒介変数表示のままでも，「$x$ の積分 → $\theta$ の積分」の置換と考えれば $y=f(x)$ の場合と同じである。$x$ が $\theta$ について単調であることを最初に確認しておく。",
  "ex": r"アステロイド $x=\cos^3\theta$，$y=\sin^3\theta\ (0\leqq\theta\leqq2\pi)$ で囲まれた部分を $x$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{32}{105}\pi$"},
 {"lv": 3, "title": r"$x$ について解けない曲線の $y$ 軸のまわりの回転（置換積分）",
  "q": r"曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$y$ を固定すると $\sin x=y$ を満たす $x$ は2つ（$x_1\leqq x_2$）あり，切り口は外径 $x_2$，内径 $x_1$ の円環。$x_1,\ x_2$ は具体的に表せないので，$y=\sin x$ と置換して $x$ の積分に直す。",
  "sol": _f43() + r"$0\leqq y\leqq1$ のとき，$\sin x=y$ を満たす $x$ は $0\leqq x\leqq\dfrac\pi2$ と $\dfrac\pi2\leqq x\leqq\pi$ に1つずつある。それぞれ $x_1$，$x_2$ とすると，$y$ 軸に垂直な平面による切り口は外径 $x_2$，内径 $x_1$ の円環だから<br>"
         r"$\displaystyle V=\pi\int_0^1x_2^2\,dy-\pi\int_0^1x_1^2\,dy$<br>"
         r"$y=\sin x$ とおくと $dy=\cos x\,dx$。$x_2$ では $y:0\to1$ に $x:\pi\to\dfrac\pi2$，$x_1$ では $x:0\to\dfrac\pi2$ が対応するから<br>"
         r"$\displaystyle V=\pi\int_\pi^{\frac\pi2}x^2\cos x\,dx-\pi\int_0^{\frac\pi2}x^2\cos x\,dx=-\pi\int_0^\pi x^2\cos x\,dx$<br>"
         r"部分積分により　$\displaystyle\int x^2\cos x\,dx=x^2\sin x-\int2x\sin x\,dx=x^2\sin x+2x\cos x-2\sin x+C$<br>"
         r"$\displaystyle\int_0^\pi x^2\cos x\,dx=\Big[x^2\sin x+2x\cos x-2\sin x\Big]_0^\pi=-2\pi$　よって　$V=\boldsymbol{2\pi^2}$",
  "note": r"2つの積分を「同じ被積分関数 $x^2\cos x$ で，区間がつながる」形にまとめるのがポイント。次の例題のバウムクーヘン型の公式を使うと　$\displaystyle V=2\pi\int_0^\pi x\sin x\,dx=2\pi\Big[-x\cos x+\sin x\Big]_0^\pi=2\pi^2$ とすぐに求まる。",
  "ex": r"曲線 $y=\sin2x\ \left(0\leqq x\leqq\dfrac\pi2\right)$ と $x$ 軸で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{\pi^2}2$"},
 {"lv": 3, "title": r"バウムクーヘン型の求積",
  "q": r"曲線 $y=xe^{-x}\ (0\leqq x\leqq1)$，$x$ 軸および直線 $x=1$ で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$y=xe^{-x}$ は $x$ について解けない。半径 $x$，高さ $y$ の薄い円筒を集める $\displaystyle V=2\pi\int_0^1xf(x)\,dx$ を使う（公式の確かめ方は検討）。",
  "sol": r"$0\leqq x\leqq1$ で $f(x)=xe^{-x}\geqq0$ だから，バウムクーヘン型の公式により<br>"
         r"$\displaystyle V=2\pi\int_0^1x\cdot xe^{-x}\,dx=2\pi\int_0^1x^2e^{-x}\,dx$<br>"
         r"$\displaystyle\int x^2e^{-x}\,dx=-x^2e^{-x}+\int2xe^{-x}\,dx=-x^2e^{-x}-2xe^{-x}-2e^{-x}+C=-(x^2+2x+2)e^{-x}+C$ より<br>"
         r"$\displaystyle V=2\pi\Big[-(x^2+2x+2)e^{-x}\Big]_0^1=2\pi\left(2-\frac5e\right)=\boldsymbol{4\pi-\frac{10\pi}e}$",
  "note": r"<b>公式の確かめ</b>：$f'(x)=(1-x)e^{-x}\geqq0$ より $f$ は $0\leqq x\leqq1$ で増加し，$f(1)=\dfrac1e$。$0\leqq y\leqq\dfrac1e$ に対して $f(x)=y$ となる $x$ を $x(y)$ とすると，切り口は外径 $1$，内径 $x(y)$ の円環だから，$y=f(x)$ と置換して<br>"
          r"$\displaystyle V=\pi\int_0^{\frac1e}\{1-x(y)^2\}\,dy=\frac\pi e-\pi\int_0^1x^2f'(x)\,dx=\frac\pi e-\pi\left(\Big[x^2f(x)\Big]_0^1-\int_0^12xf(x)\,dx\right)=2\pi\int_0^1xf(x)\,dx$<br>"
          r"一般の場合も，$f(x)$ が単調な区間に分けて同様に示せる。答案で公式を使うときは，このような説明を添えるとよい。",
  "ex": r"曲線 $y=\sin x\ \left(0\leqq x\leqq\dfrac\pi2\right)$，$x$ 軸および直線 $x=\dfrac\pi2$ で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$2\pi$"},
 {"lv": 4, "title": r"媒介変数表示の曲線を $y$ 軸のまわりに回転する",
  "q": r"サイクロイド $x=\theta-\sin\theta$，$y=1-\cos\theta\ (0\leqq\theta\leqq2\pi)$ と $x$ 軸で囲まれた部分を $y$ 軸のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$y$ を固定すると，曲線上の点は $0\leqq\theta\leqq\pi$ と $\pi\leqq\theta\leqq2\pi$ に1つずつある。$y=\sin x$ の例題と同様に，$\pi\int(x_2^2-x_1^2)\,dy$ を $\theta$ の積分にまとめる。",
  "sol": _f45() + r"$y=1-\cos\theta$ は $0\leqq\theta\leqq\pi$ で $0$ から $2$ まで増加し，$\pi\leqq\theta\leqq2\pi$ で $2$ から $0$ まで減少する。$x=\theta-\sin\theta$ は増加関数である。<br>"
         r"$0\leqq y\leqq2$ に対応する $\theta$ を $\theta_1\ (0\leqq\theta_1\leqq\pi)$，$\theta_2\ (\pi\leqq\theta_2\leqq2\pi)$，対応する $x$ を $x_1\leqq x_2$ とすると，$y$ 軸に垂直な平面による切り口は外径 $x_2$，内径 $x_1$ の円環だから<br>"
         r"$\displaystyle V=\pi\int_0^2x_2^2\,dy-\pi\int_0^2x_1^2\,dy$<br>"
         r"$dy=\sin\theta\,d\theta$ で，$x_2$ では $y:0\to2$ に $\theta:2\pi\to\pi$，$x_1$ では $\theta:0\to\pi$ が対応するから<br>"
         r"$\displaystyle V=\pi\int_{2\pi}^{\pi}x^2\sin\theta\,d\theta-\pi\int_0^\pi x^2\sin\theta\,d\theta=-\pi\int_0^{2\pi}(\theta-\sin\theta)^2\sin\theta\,d\theta$<br>"
         r"$(\theta-\sin\theta)^2\sin\theta=\theta^2\sin\theta-2\theta\sin^2\theta+\sin^3\theta$ で<br>"
         r"$\displaystyle\int_0^{2\pi}\theta^2\sin\theta\,d\theta=\Big[-\theta^2\cos\theta+2\theta\sin\theta+2\cos\theta\Big]_0^{2\pi}=-4\pi^2$<br>"
         r"$\displaystyle\int_0^{2\pi}2\theta\sin^2\theta\,d\theta=\int_0^{2\pi}\theta(1-\cos2\theta)\,d\theta=2\pi^2-\Big[\frac{\theta\sin2\theta}2+\frac{\cos2\theta}4\Big]_0^{2\pi}=2\pi^2$<br>"
         r"$\displaystyle\int_0^{2\pi}\sin^3\theta\,d\theta=\int_0^{2\pi}\frac{3\sin\theta-\sin3\theta}4\,d\theta=0$<br>"
         r"よって　$V=-\pi(-4\pi^2-2\pi^2+0)=\boldsymbol{6\pi^3}$",
  "note": r"バウムクーヘン型を使えば $\displaystyle V=2\pi\int_0^{2\pi}xy\,dx=2\pi\int_0^{2\pi}(\theta-\sin\theta)(1-\cos\theta)^2\,d\theta=6\pi^3$。また，図形の面積 $3\pi$ と，図形の重心から回転軸までの距離 $\pi$（対称性）を用いると $2\pi\cdot\pi\cdot3\pi=6\pi^3$ となり，検算に使える（パップス・ギュルダンの定理）。",
  "ex": r"上の例題の図形を，直線 $x=\pi$ のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac32\pi^3-\dfrac83\pi$"},
]})


def _cyc_inv(X):
    """θ−sinθ = X（0≦X≦2π）を満たす θ を二分法で求める（numpy 配列可）。"""
    lo = np.zeros_like(X)
    hi = np.full_like(X, 2 * math.pi)
    for _ in range(60):
        mid = (lo + hi) / 2
        f = mid - np.sin(mid) - X
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    return (lo + hi) / 2


def _v4():
    assert _eq(pi * integrate(exp(2 * y), (y, 0, 1)), pi * (E**2 - 1) / 2)
    assert _eq(pi * integrate(1 / y**2, (y, 1, 3)), 2 * pi / 3)
    # サイクロイド x 軸
    assert _eq(pi * integrate((1 - cos(th))**3, (th, 0, 2 * pi)), 5 * pi**2)
    assert _eq(integrate(cos(th)**3, (th, 0, 2 * pi)), 0) and _eq(expand((3 * cos(th) + cos(3 * th)) / 4 - cos(th)**3).rewrite(exp).simplify(), 0)
    def cx(X, Y, Z):
        h = 1 - np.cos(_cyc_inv(np.clip(X, 0, 2 * math.pi)))
        return Y * Y + Z * Z <= h * h
    assert abs(_mc_rev(cx, ((0, 2 * math.pi), (-2, 2), (-2, 2))) - 5 * math.pi**2) / (5 * math.pi**2) < 0.01
    # アステロイド x 軸：V = 6π∫ sin^7 cos^2
    Va = 6 * pi * integrate(sin(th)**7 * cos(th)**2, (th, 0, pi / 2))
    assert _eq(Va, 32 * pi / 105)
    assert abs(2 * math.pi * _simpson(lambda u: (1 - u**(2 / 3))**3, 0, 1, 20000) - 32 * math.pi / 105) < 1e-6
    # sin x を y 軸のまわり
    assert _eq(-pi * integrate(x**2 * cos(x), (x, 0, pi)), 2 * pi**2)
    assert _eq(diff(x**2 * sin(x) + 2 * x * cos(x) - 2 * sin(x), x), x**2 * cos(x))
    assert _eq(2 * pi * integrate(x * sin(x), (x, 0, pi)), 2 * pi**2)
    def sy(X, Y, Z):
        rho = np.sqrt(X * X + Z * Z)
        return (rho <= math.pi) & (Y >= 0) & (Y <= np.sin(rho))
    assert abs(_mc_rev(sy, ((-math.pi, math.pi), (0, 1), (-math.pi, math.pi))) - 2 * math.pi**2) < 0.25
    # 練習：sin 2x（置換による計算とバウムクーヘン型の一致）
    assert _eq(-pi * integrate(x**2 * 2 * cos(2 * x), (x, 0, pi / 2)), pi**2 / 2)
    assert _eq(2 * pi * integrate(x * sin(2 * x), (x, 0, pi / 2)), pi**2 / 2)
    # バウムクーヘン型 xe^{-x}
    Vb = 2 * pi * integrate(x**2 * exp(-x), (x, 0, 1))
    assert _eq(Vb, 4 * pi - 10 * pi / E)
    f = x * exp(-x)
    assert _eq(pi / E - pi * integrate(x**2 * diff(f, x), (x, 0, 1)), Vb)
    def bk(X, Y, Z):
        rho = np.sqrt(X * X + Z * Z)
        return (rho <= 1) & (Y >= 0) & (Y <= rho * np.exp(-rho))
    assert abs(_mc_rev(bk, ((-1, 1), (0, 0.37), (-1, 1))) - float(Vb)) < 0.02
    assert _eq(2 * pi * integrate(x * sin(x), (x, 0, pi / 2)), 2 * pi)
    # サイクロイド y 軸
    Vc = -pi * integrate((th - sin(th))**2 * sin(th), (th, 0, 2 * pi))
    assert _eq(Vc, 6 * pi**3)
    assert _eq(integrate(th**2 * sin(th), (th, 0, 2 * pi)), -4 * pi**2)
    assert _eq(integrate(2 * th * sin(th)**2, (th, 0, 2 * pi)), 2 * pi**2)
    assert _eq(integrate(sin(th)**3, (th, 0, 2 * pi)), 0)
    assert _eq(2 * pi * integrate((th - sin(th)) * (1 - cos(th))**2, (th, 0, 2 * pi)), 6 * pi**3)
    def cyy(X, Y, Z):
        rho = np.sqrt(X * X + Z * Z)
        h = 1 - np.cos(_cyc_inv(np.clip(rho, 0, 2 * math.pi)))
        return (rho <= 2 * math.pi) & (Y >= 0) & (Y <= h)
    R = 2 * math.pi
    assert abs(_mc_rev(cyy, ((-R, R), (0, 2), (-R, R)), N=500000) - 6 * math.pi**3) / (6 * math.pi**3) < 0.01
    # 練習：x=π のまわり（左半分の回転）
    Vp = pi * integrate((pi - th + sin(th))**2 * sin(th), (th, 0, pi))
    assert _eq(Vp, 3 * pi**3 / 2 - 8 * pi / 3)
    def cyp(X, Y, Z):
        rho = np.sqrt((X - math.pi)**2 + Z * Z)
        h = 1 - np.cos(_cyc_inv(np.clip(math.pi - rho, 0, 2 * math.pi)))
        return (rho <= math.pi) & (Y >= 0) & (Y <= h)
    assert abs(_mc_rev(cyp, ((0, 2 * math.pi), (0, 2), (-math.pi, math.pi)), N=500000) - float(Vp)) / float(Vp) < 0.01


# ---------------------------------------------------------------- 第5節の図
def _plen(fx, fy, t0, t1, N=200000):
    """媒介変数表示の曲線を細かい折れ線で近似した長さ。"""
    T = np.linspace(t0, t1, N + 1)
    X, Y = fx(T), fy(T)
    return float(np.sum(np.hypot(np.diff(X), np.diff(Y))))


def _f54():
    g = _G(160, 150, (-1.9, 3.4), (-2.9, 2.9), eq=True)
    fx = lambda u: 2 * math.cos(u) + math.cos(2 * u)
    fy = lambda u: 2 * math.sin(u) - math.sin(2 * u)
    g.axes()
    g.pcurve(fx, fy, 0, 2 * math.pi, n=360)
    for u, lab, dx, dy in ((0, "t=0", 2, 12), (2 * math.pi / 3, "t=2π/3", -4, -5), (4 * math.pi / 3, "t=4π/3", -4, 12)):
        g.pt(fx(u), fy(u), col=C2)
        g.txt(fx(u), fy(u), lab, dx=dx, dy=dy, size=8, col=C2, anc="middle" if u else "end")
    return g.svg()


# ---------------------------------------------------------------- 節5
SEC.append({"title": r"曲線の長さ・道のり",
"base": r"""・曲線 $x=f(t)$，$y=g(t)\ (\alpha\leqq t\leqq\beta)$ の長さ　$\displaystyle L=\int_\alpha^\beta\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt$<br>
・曲線 $y=f(x)\ (a\leqq x\leqq b)$ の長さ　$\displaystyle L=\int_a^b\sqrt{1+\{f'(x)\}^2}\,dx$　　・極方程式 $r=f(\theta)$ の曲線の長さ　$\displaystyle L=\int_\alpha^\beta\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta$<br>
・数直線上を速度 $v(t)$ で動く点：位置の変化量は $\displaystyle\int_a^bv(t)\,dt$，道のりは $\displaystyle\int_a^b|v(t)|\,dt$。平面上の運動では，速さ $\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}$ を積分したものが道のり。<br>
・根号をはずすときは $\sqrt{A^2}=|A|$ に注意する（半角の公式などで平方の形をつくる）。""",
"items": [
 {"lv": 1, "title": r"曲線の長さの基本",
  "q": r"次の曲線の長さ $L$ を求めよ。<br>(1) $x=t^2,\ y=\dfrac23t^3\ (0\leqq t\leqq\sqrt3)$　　(2) $y=\dfrac{e^x+e^{-x}}2\ (0\leqq x\leqq1)$",
  "hint": r"根号の中を平方の形（または平方 × 簡単な式）に整理する。(2) は $1+\{f'(x)\}^2$ がちょうど $\{f(x)\}^2$ になる。",
  "sol": r"(1) $\dfrac{dx}{dt}=2t$，$\dfrac{dy}{dt}=2t^2$ より $\left(\dfrac{dx}{dt}\right)^2+\left(\dfrac{dy}{dt}\right)^2=4t^2(1+t^2)$。$t\geqq0$ だから<br>"
         r"$\displaystyle L=\int_0^{\sqrt3}2t\sqrt{1+t^2}\,dt=\Big[\frac23(1+t^2)^{\frac32}\Big]_0^{\sqrt3}=\frac23(8-1)=\boldsymbol{\frac{14}3}$<br>"
         r"(2) $y'=\dfrac{e^x-e^{-x}}2$ より $1+y'^2=\dfrac{e^{2x}+2+e^{-2x}}4=\left(\dfrac{e^x+e^{-x}}2\right)^2$。よって<br>"
         r"$\displaystyle L=\int_0^1\frac{e^x+e^{-x}}2\,dx=\Big[\frac{e^x-e^{-x}}2\Big]_0^1=\boldsymbol{\frac{e-e^{-1}}2}$",
  "note": r"(2) の曲線は懸垂線（カテナリー）とよばれ，ひもの両端を持ってたらしたときの形である。",
  "ex": r"次の曲線の長さを求めよ。<br>(1) $x=e^t\cos t,\ y=e^t\sin t\ (0\leqq t\leqq1)$　　(2) $y=\log(1-x^2)\ \left(0\leqq x\leqq\dfrac12\right)$",
  "exa": r"(1) $\sqrt2(e-1)$　(2) $\log3-\dfrac12$"},
 {"lv": 2, "title": r"サイクロイドの長さ（根号のはずし方）",
  "q": r"サイクロイド $x=\theta-\sin\theta$，$y=1-\cos\theta\ (0\leqq\theta\leqq2\pi)$ の長さ $L$ を求めよ。",
  "hint": r"$\left(\dfrac{dx}{d\theta}\right)^2+\left(\dfrac{dy}{d\theta}\right)^2=2(1-\cos\theta)$ を半角の公式で $4\sin^2\dfrac\theta2$ と平方の形にし，区間での $\sin\dfrac\theta2$ の符号を確認して根号をはずす。",
  "sol": r"$\dfrac{dx}{d\theta}=1-\cos\theta$，$\dfrac{dy}{d\theta}=\sin\theta$ より<br>"
         r"$\left(\dfrac{dx}{d\theta}\right)^2+\left(\dfrac{dy}{d\theta}\right)^2=1-2\cos\theta+\cos^2\theta+\sin^2\theta=2(1-\cos\theta)=4\sin^2\dfrac\theta2$<br>"
         r"$0\leqq\theta\leqq2\pi$ では $0\leqq\dfrac\theta2\leqq\pi$ で $\sin\dfrac\theta2\geqq0$ だから<br>"
         r"$\displaystyle L=\int_0^{2\pi}2\sin\frac\theta2\,d\theta=\Big[-4\cos\frac\theta2\Big]_0^{2\pi}=4+4=\boldsymbol{8}$",
  "note": r"1つの弧の長さ $8$ は，転がる円の直径 $2$ のちょうど $4$ 倍。区間が $2\pi$ をこえるときは $\left|\sin\dfrac\theta2\right|$ のまま区間を分ける。",
  "ex": r"アステロイド $x=\cos^3\theta$，$y=\sin^3\theta\ (0\leqq\theta\leqq2\pi)$ の長さ（全長）を求めよ。",
  "exa": r"$6$"},
 {"lv": 2, "title": r"直線上の運動の位置と道のり",
  "q": r"数直線上を動く点 $\mathrm{P}$ の時刻 $t$ における速度が $v(t)=\sin t+\cos t$ である。$t=0$ から $t=\pi$ までの間について，次のものを求めよ。<br>(1) $\mathrm{P}$ の位置の変化量　　(2) $\mathrm{P}$ が動いた道のり",
  "hint": r"位置の変化量は $\int v\,dt$，道のりは $\int|v|\,dt$。$v(t)$ を合成して符号が変わる時刻を求める。",
  "sol": r"$F(t)=-\cos t+\sin t$ とおくと $F'(t)=v(t)$。<br>"
         r"(1) $\displaystyle\int_0^\pi v(t)\,dt=F(\pi)-F(0)=1-(-1)=\boldsymbol{2}$<br>"
         r"(2) $v(t)=\sqrt2\sin\left(t+\dfrac\pi4\right)$ で，$0\leqq t\leqq\pi$ では $0\leqq t\leqq\dfrac34\pi$ のとき $v(t)\geqq0$，$\dfrac34\pi\leqq t\leqq\pi$ のとき $v(t)\leqq0$。$F\left(\dfrac34\pi\right)=\sqrt2$ だから<br>"
         r"$\displaystyle\int_0^\pi|v(t)|\,dt=\int_0^{\frac34\pi}v(t)\,dt-\int_{\frac34\pi}^\pi v(t)\,dt=\{\sqrt2-(-1)\}-(1-\sqrt2)=\boldsymbol{2\sqrt2}$",
  "note": r"$\mathrm{P}$ は $t=\dfrac34\pi$ まで正の向きに $\sqrt2+1$ だけ進み，その後 $\sqrt2-1$ だけもどる。差が位置の変化量 $2$，和が道のり $2\sqrt2$ である。",
  "ex": r"数直線上を動く点 $\mathrm{P}$ の時刻 $t$ における速度が $v(t)=\cos t-\dfrac12$ で，$t=0$ のとき $\mathrm{P}$ は原点にある。$t=\pi$ における $\mathrm{P}$ の座標と，$0\leqq t\leqq\pi$ の間に $\mathrm{P}$ が動いた道のりを求めよ。",
  "exa": r"座標 $-\dfrac\pi2$，道のり $\sqrt3+\dfrac\pi6$"},
 {"lv": 3, "title": r"平面上の運動の道のり",
  "q": r"座標平面上を動く点 $\mathrm{P}$ の時刻 $t$ における座標が $x=2\cos t+\cos2t$，$y=2\sin t-\sin2t$ で与えられている。$t=0$ から $t=2\pi$ までに $\mathrm{P}$ が動く道のり $L$ を求めよ。",
  "hint": r"速さの2乗を計算すると，加法定理で $\cos3t$ がまとまって $8(1-\cos3t)=16\sin^2\dfrac{3t}2$ となる。$\sin\dfrac{3t}2$ は区間内で符号が変わるので絶対値のまま扱う。",
  "sol": _f54() + r"$\dfrac{dx}{dt}=-2(\sin t+\sin2t)$，$\dfrac{dy}{dt}=2(\cos t-\cos2t)$ より<br>"
         r"$\left(\dfrac{dx}{dt}\right)^2+\left(\dfrac{dy}{dt}\right)^2=4\{(\sin t+\sin2t)^2+(\cos t-\cos2t)^2\}=4\{2+2(\sin t\sin2t-\cos t\cos2t)\}$<br>"
         r"$\qquad=8(1-\cos3t)=16\sin^2\dfrac{3t}2$<br>"
         r"よって速さは $4\left|\sin\dfrac{3t}2\right|$。$u=\dfrac{3t}2$ とおくと<br>"
         r"$\displaystyle L=\int_0^{2\pi}4\left|\sin\frac{3t}2\right|dt=\frac83\int_0^{3\pi}|\sin u|\,du=\frac83\cdot3\int_0^\pi\sin u\,du=\frac83\cdot3\cdot2=\boldsymbol{16}$",
  "note": r"この曲線はデルトイドとよばれる。速さが $0$ になる $t=0,\ \dfrac23\pi,\ \dfrac43\pi$ の点がとがった点で，そこで $\sin\dfrac{3t}2$ の符号が変わる。「速さ $=0$ の時刻」で区間を分けるのが道のりの計算の基本。",
  "ex": r"座標平面上を動く点の時刻 $t$ における座標が $x=3\cos t+\cos3t$，$y=3\sin t-\sin3t$ であるとき，$t=0$ から $t=2\pi$ までに動く道のりを求めよ。",
  "exa": r"$24$"},
 {"lv": 3, "title": r"極方程式で表された曲線の長さ",
  "q": r"極方程式 $r=1+\cos\theta\ (0\leqq\theta\leqq2\pi)$ で表される曲線（カージオイド）の長さ $L$ を求めよ。",
  "hint": r"$x=r\cos\theta$，$y=r\sin\theta$ を $\theta$ の媒介変数表示とみる。$\left(\dfrac{dx}{d\theta}\right)^2+\left(\dfrac{dy}{d\theta}\right)^2=r^2+\left(\dfrac{dr}{d\theta}\right)^2$ となる。",
  "sol": r"$x=r\cos\theta$，$y=r\sin\theta$ より $\dfrac{dx}{d\theta}=r'\cos\theta-r\sin\theta$，$\dfrac{dy}{d\theta}=r'\sin\theta+r\cos\theta$（$r'=\dfrac{dr}{d\theta}$）だから<br>"
         r"$\left(\dfrac{dx}{d\theta}\right)^2+\left(\dfrac{dy}{d\theta}\right)^2=r^2+r'^2=(1+\cos\theta)^2+\sin^2\theta=2(1+\cos\theta)=4\cos^2\dfrac\theta2$<br>"
         r"曲線は $x$ 軸に関して対称で，$0\leqq\theta\leqq\pi$ では $\cos\dfrac\theta2\geqq0$ だから<br>"
         r"$\displaystyle L=2\int_0^\pi2\cos\frac\theta2\,d\theta=2\Big[4\sin\frac\theta2\Big]_0^\pi=\boldsymbol{8}$",
  "note": r"$\displaystyle\int_0^{2\pi}2\cos\frac\theta2\,d\theta=0$ としてしまうのが典型的な誤り。$\pi\leqq\theta\leqq2\pi$ では $\cos\dfrac\theta2\leqq0$ である。",
  "ex": r"極方程式 $r=\theta^2\ (0\leqq\theta\leqq\sqrt5)$ で表される曲線の長さを求めよ。",
  "exa": r"$\dfrac{19}3$"},
 {"lv": 4, "title": r"放物線の長さ（$\sqrt{x^2+1}$ の積分）",
  "q": r"放物線 $y=\dfrac{x^2}2\ (0\leqq x\leqq1)$ の長さ $L$ を求めよ。",
  "hint": r"$\displaystyle L=\int_0^1\sqrt{1+x^2}\,dx$。$t=x+\sqrt{x^2+1}$ とおくと，$x$ も $\sqrt{x^2+1}$ も $t$ の有理式で表せて，有理関数の積分になる。",
  "sol": r"$y'=x$ より $\displaystyle L=\int_0^1\sqrt{1+x^2}\,dx$。<br>"
         r"$t=x+\sqrt{x^2+1}$ とおくと $t-x=\sqrt{x^2+1}$。両辺を2乗して $t^2-2tx=1$ より　$x=\dfrac12\left(t-\dfrac1t\right)$，$\sqrt{x^2+1}=t-x=\dfrac12\left(t+\dfrac1t\right)$<br>"
         r"$dx=\dfrac12\left(1+\dfrac1{t^2}\right)dt$，$x:0\to1$ のとき $t:1\to1+\sqrt2$ だから<br>"
         r"$\displaystyle L=\int_1^{1+\sqrt2}\frac12\left(t+\frac1t\right)\cdot\frac12\left(1+\frac1{t^2}\right)dt=\frac14\int_1^{1+\sqrt2}\left(t+\frac2t+\frac1{t^3}\right)dt=\frac14\Big[\frac{t^2}2+2\log t-\frac1{2t^2}\Big]_1^{1+\sqrt2}$<br>"
         r"$t=1+\sqrt2$ のとき $t^2=3+2\sqrt2$，$\dfrac1{t^2}=(\sqrt2-1)^2=3-2\sqrt2$ で $\dfrac{t^2}2-\dfrac1{2t^2}=2\sqrt2$。$t=1$ のとき $\dfrac{t^2}2-\dfrac1{2t^2}=0$。よって<br>"
         r"$L=\dfrac14\{2\sqrt2+2\log(1+\sqrt2)\}=\boldsymbol{\dfrac{\sqrt2+\log(1+\sqrt2)}2}$",
  "note": r"<b>別解</b>：$\{\log(x+\sqrt{x^2+1})\}'=\dfrac1{\sqrt{x^2+1}}$ を使う。部分積分で $\displaystyle L=\Big[x\sqrt{1+x^2}\Big]_0^1-\int_0^1\frac{x^2}{\sqrt{1+x^2}}dx=\sqrt2-L+\int_0^1\frac{dx}{\sqrt{1+x^2}}$ より $2L=\sqrt2+\log(1+\sqrt2)$。",
  "ex": r"放物線 $y=x^2\ (0\leqq x\leqq1)$ の長さを求めよ。",
  "exa": r"$\dfrac{2\sqrt5+\log(2+\sqrt5)}4$"},
]})


def _v5():
    # 基本
    assert _eq(integrate(2 * t * sqrt(1 + t**2), (t, 0, sqrt(3))), Rational(14, 3))
    assert abs(_plen(lambda u: u * u, lambda u: 2 / 3 * u**3, 0, math.sqrt(3)) - 14 / 3) < 1e-8
    ch = (exp(x) + exp(-x)) / 2
    assert _eq(simplify(1 + diff(ch, x)**2 - ch**2), 0)
    assert _eq(integrate(ch, (x, 0, 1)), (E - 1 / E) / 2)
    assert abs(_plen(lambda u: u, lambda u: np.cosh(u), 0, 1) - (math.e - 1 / math.e) / 2) < 1e-8
    assert abs(_plen(lambda u: np.exp(u) * np.cos(u), lambda u: np.exp(u) * np.sin(u), 0, 1) - math.sqrt(2) * (math.e - 1)) < 1e-8
    assert abs(_plen(lambda u: u, lambda u: np.log(1 - u * u), 0, 0.5) - (math.log(3) - 0.5)) < 1e-8
    assert _eq(integrate((1 + x**2) / (1 - x**2), (x, 0, Rational(1, 2))), log(3) - Rational(1, 2))
    # サイクロイド・アステロイド
    assert _eq(integrate(2 * sin(th / 2), (th, 0, 2 * pi)), 8)
    assert abs(_plen(lambda u: u - np.sin(u), lambda u: 1 - np.cos(u), 0, 2 * math.pi) - 8) < 1e-7
    assert abs(_plen(lambda u: np.cos(u)**3, lambda u: np.sin(u)**3, 0, 2 * math.pi) - 6) < 1e-7
    # 直線上の運動
    F = -cos(t) + sin(t)
    assert _eq(diff(F, t), sin(t) + cos(t))
    assert _eq(F.subs(t, pi) - F.subs(t, 0), 2)
    assert _eq(F.subs(t, 3 * pi / 4), sqrt(2))
    assert abs(_simpson(lambda u: abs(math.sin(u) + math.cos(u)), 0, math.pi, 30000) - 2 * math.sqrt(2)) < 1e-6
    assert _eq(integrate(cos(t) - Rational(1, 2), (t, 0, pi)), -pi / 2)
    assert abs(_simpson(lambda u: abs(math.cos(u) - 0.5), 0, math.pi, 30000) - (math.sqrt(3) + math.pi / 6)) < 1e-6
    # デルトイド
    dx_, dy_ = diff(2 * cos(t) + cos(2 * t), t), diff(2 * sin(t) - sin(2 * t), t)
    assert _eq((dx_**2 + dy_**2).rewrite(exp).simplify() - (16 * sin(3 * t / 2)**2).rewrite(exp).simplify(), 0)
    assert abs(_plen(lambda u: 2 * np.cos(u) + np.cos(2 * u), lambda u: 2 * np.sin(u) - np.sin(2 * u), 0, 2 * math.pi) - 16) < 1e-6
    assert abs(_plen(lambda u: 3 * np.cos(u) + np.cos(3 * u), lambda u: 3 * np.sin(u) - np.sin(3 * u), 0, 2 * math.pi) - 24) < 1e-6
    # カージオイド・r=θ^2
    cr = lambda u: (1 + np.cos(u))
    assert abs(_plen(lambda u: cr(u) * np.cos(u), lambda u: cr(u) * np.sin(u), 0, 2 * math.pi) - 8) < 1e-6
    assert _eq(integrate(th * sqrt(th**2 + 4), (th, 0, sqrt(5))), Rational(19, 3))
    assert abs(_plen(lambda u: u * u * np.cos(u), lambda u: u * u * np.sin(u), 0, math.sqrt(5)) - 19 / 3) < 1e-6
    # 放物線
    Lp = (sqrt(2) + log(1 + sqrt(2))) / 2
    assert abs(_simpson(lambda u: math.sqrt(1 + u * u), 0, 1) - float(Lp)) < 1e-12
    assert _eq(integrate((t + 2 / t + 1 / t**3) / 4, (t, 1, 1 + sqrt(2))) - Lp, 0)
    tt = 1 + sqrt(2)
    assert _eq(tt**2 / 2 - 1 / (2 * tt**2), 2 * sqrt(2))
    xs = (t - 1 / t) / 2
    assert _eq(sqrt(xs**2 + 1).subs(t, 3) - (3 + Rational(1, 3)) / 2, 0)
    assert _eq(diff(log(x + sqrt(x**2 + 1)), x) - 1 / sqrt(x**2 + 1), 0)
    assert abs(_plen(lambda u: u, lambda u: u * u, 0, 1) - (2 * math.sqrt(5) + math.log(2 + math.sqrt(5))) / 4) < 1e-8


# ---------------------------------------------------------------- 第6節の図
def _f63():
    g = _G(190, 110, (-2.6, 3.4), (-0.35, 2.2), eq=True)
    g.axes()
    g.curve(lambda u: math.sqrt(max(u, 0)), 0, 3.3, n=400)
    t0 = 1.6
    p = (t0, math.sqrt(t0))
    g.curve(lambda u: (u + t0) / (2 * math.sqrt(t0)), -2.5, 3.3, col=C2, w=1.1)
    g.pt(*p)
    g.pt(-t0, 0, col=C2)
    g.pt(t0, 0)
    g.seg(p, (t0, 0))
    g.txt(*p, "P", dx=-4, dy=-6, size=10)
    g.txt(-t0, 0, "Q", dy=12, size=10)
    g.txt(t0, 0, "H", dy=12, size=10)
    g.txt(3.35, 1.25, "y=√x", anc="end", it=True, size=9)
    return g.svg()


# ---------------------------------------------------------------- 節6
SEC.append({"title": r"微分方程式",
"base": r"""・未知の関数とその導関数を含む等式を<b>微分方程式</b>といい，それを満たす関数を求めることを微分方程式を解くという。<br>
・変数分離形 $\dfrac{dy}{dx}=f(x)g(y)$：$g(y)\neq0$ のとき $\dfrac1{g(y)}\dfrac{dy}{dx}=f(x)$ の両辺を $x$ で積分して　$\displaystyle\int\frac{dy}{g(y)}=\int f(x)\,dx$（$g(y)=0$ となる定数関数も解になり得るので別に調べる）<br>
・$\dfrac{dy}{dx}=ky$ の解は　$y=Ce^{kx}$（$C$ は任意の定数）。「増加・減少の速さが量に比例する」現象を表す。<br>
・$f'(x)-pf(x)=q(x)$ の形は，両辺に $e^{-px}$ を掛けると $\{e^{-px}f(x)\}'=e^{-px}q(x)$ となり，積分できる。<br>
・積分定数は，与えられた条件（初期条件）から決める。""",
"items": [
 {"lv": 1, "title": r"変数分離形の微分方程式",
  "q": r"次の微分方程式を，( ) 内の条件のもとで解け。<br>(1) $\dfrac{dy}{dx}=2xy$　（$x=0$ のとき $y=3$）　　(2) $y\dfrac{dy}{dx}=x$　（$x=0$ のとき $y=1$，$y>0$）",
  "hint": r"$y$ を含む部分を左辺に，$x$ を含む部分を右辺に分けて，両辺を $x$ で積分する。最後に条件で積分定数を決める。",
  "sol": r"(1) 定数関数 $y=0$ は条件を満たさない。$y\neq0$ のとき $\dfrac1y\dfrac{dy}{dx}=2x$ の両辺を $x$ で積分すると<br>"
         r"$\displaystyle\int\frac{dy}y=\int2x\,dx$ より $\log|y|=x^2+C_1$（$C_1$ は定数）。よって $y=\pm e^{C_1}e^{x^2}=Ce^{x^2}$（$C=\pm e^{C_1}$）<br>"
         r"$x=0$ のとき $y=3$ より $C=3$。よって　$\boldsymbol{y=3e^{x^2}}$<br>"
         r"(2) 両辺を $x$ で積分すると $\displaystyle\int y\,dy=\int x\,dx$ より $\dfrac{y^2}2=\dfrac{x^2}2+C$（$C$ は定数）。<br>"
         r"$x=0$ のとき $y=1$ より $C=\dfrac12$ で $y^2=x^2+1$。$y>0$ だから　$\boldsymbol{y=\sqrt{x^2+1}}$",
  "note": r"答えを微分して，もとの方程式に代入して確かめるとよい。(1) では $y'=6xe^{x^2}=2x\cdot3e^{x^2}$ となり成り立つ。",
  "ex": r"次の微分方程式を，( ) 内の条件のもとで解け。<br>(1) $\dfrac{dy}{dx}=y\cos x$　（$x=0$ のとき $y=2$）　　(2) $\dfrac{dy}{dx}=e^{x-y}$　（$x=0$ のとき $y=1$）",
  "exa": r"(1) $y=2e^{\sin x}$　(2) $y=\log(e^x+e-1)$"},
 {"lv": 2, "title": r"減衰の法則（ニュートンの冷却法則）",
  "q": r"室温 $20\,{}^\circ\mathrm{C}$ の部屋に置いた物体の温度 $T\ ({}^\circ\mathrm{C})$ は，時刻 $t$（分）に対して $\dfrac{dT}{dt}=-k(T-20)$（$k$ は正の定数）を満たして変化する。$t=0$ のとき $T=80$，$t=10$ のとき $T=50$ であった。<br>(1) $T$ を $t$ で表せ。　(2) $t=20$ のときの $T$ を求めよ。　(3) $T=25$ となる $t$ を求めよ。",
  "hint": r"$T-20=u$ とおくと $\dfrac{du}{dt}=-ku$ で，$u=Ce^{-kt}$。$k$ の値そのものより $e^{-10k}$ の値が分かれば十分。",
  "sol": r"(1) $T=20$（定数）は条件に合わない。$T\neq20$ のとき $\dfrac1{T-20}\dfrac{dT}{dt}=-k$ の両辺を $t$ で積分して $\log|T-20|=-kt+C_1$，すなわち $T-20=Ae^{-kt}$（$A$ は定数）。<br>"
         r"$t=0$ のとき $T=80$ より $A=60$。$t=10$ のとき $T=50$ より $60e^{-10k}=30$，$e^{-10k}=\dfrac12$。よって $e^{-kt}=\left(e^{-10k}\right)^{\frac t{10}}=2^{-\frac t{10}}$ で<br>"
         r"$\boldsymbol{T=20+60\cdot2^{-\frac t{10}}}$<br>"
         r"(2) $T=20+60\cdot2^{-2}=\boldsymbol{35}$<br>"
         r"(3) $60\cdot2^{-\frac t{10}}=5$ より $2^{\frac t{10}}=12$，$\dfrac t{10}=\log_212=2+\log_23$。よって　$\boldsymbol{t=20+10\log_23}$（約 $35.8$ 分）",
  "note": r"温度差 $T-20$ は $10$ 分ごとに半分になる（半減期が一定）。放射性物質の崩壊，薬の血中濃度なども同じ形の微分方程式で表される。",
  "ex": r"ある細菌の個数 $N$ は，増加の速さが $N$ に比例する（$\dfrac{dN}{dt}=kN$，$k>0$）として変化し，$2$ 時間で $3$ 倍になった。はじめから $5$ 時間後には，はじめの何倍になるか。",
  "exa": r"$9\sqrt3$ 倍"},
 {"lv": 3, "title": r"接線の条件から曲線を決める",
  "q": r"$x>0$ で定義された微分可能な関数 $f(x)$ は $f(x)>0$，$f'(x)>0$ を満たし，曲線 $C:\ y=f(x)$ は点 $(1,\ 1)$ を通る。$C$ 上の任意の点 $\mathrm{P}$ における接線と $x$ 軸との交点を $\mathrm{Q}$，$\mathrm{P}$ から $x$ 軸に下ろした垂線の足を $\mathrm{H}$ とすると，線分 $\mathrm{QH}$ の中点がつねに原点 $\mathrm{O}$ である。$f(x)$ を求めよ。",
  "hint": r"$\mathrm{P}(t,\ f(t))$ として $\mathrm{Q}$ の $x$ 座標を $t,\ f(t),\ f'(t)$ で表す。条件は $f$ と $f'$ の関係式（微分方程式）になる。",
  "sol": _f63() + r"$\mathrm{P}(t,\ f(t))\ (t>0)$ における接線 $y-f(t)=f'(t)(x-t)$ で $y=0$ とおくと，$f'(t)>0$ より $x=t-\dfrac{f(t)}{f'(t)}$。<br>"
         r"よって $\mathrm{Q}\left(t-\dfrac{f(t)}{f'(t)},\ 0\right)$，$\mathrm{H}(t,\ 0)$ で，$\mathrm{QH}$ の中点が原点である条件は<br>"
         r"$\dfrac12\left\{\left(t-\dfrac{f(t)}{f'(t)}\right)+t\right\}=0$　すなわち　$\dfrac{f(t)}{f'(t)}=2t$，$\dfrac{f'(t)}{f(t)}=\dfrac1{2t}$<br>"
         r"これがすべての $t>0$ で成り立つから，両辺を積分して（$f(x)>0$，$x>0$）　$\log f(x)=\dfrac12\log x+C$（$C$ は定数）<br>"
         r"$f(1)=1$ より $C=0$。よって $\log f(x)=\log\sqrt x$，すなわち　$\boldsymbol{f(x)=\sqrt x}$（これは $f(x)>0$，$f'(x)>0$ を満たす）",
  "note": r"放物線 $y^2=x$ の「接線の $x$ 切片は接点の $x$ 座標の $-1$ 倍」という性質を逆にたどったことになる。図形の条件を，接点の座標 $t$ を使って $f(t)$，$f'(t)$ の関係に翻訳するのが要点。",
  "ex": r"すべての実数 $x$ で定義された微分可能な関数 $f(x)$ は $f(x)>0$，$f'(x)>0$ を満たし，曲線 $C:\ y=f(x)$ は点 $(0,\ 1)$ を通る。$C$ 上の任意の点 $\mathrm{P}$ における接線と $x$ 軸との交点を $\mathrm{Q}$，$\mathrm{P}$ から $x$ 軸に下ろした垂線の足を $\mathrm{H}$ とすると，つねに $\mathrm{QH}=2$ である。$f(x)$ を求めよ。",
  "exa": r"$f(x)=e^{\frac x2}$"},
 {"lv": 3, "title": r"積分方程式と微分方程式（$e^{-x}$ を掛ける）",
  "q": r"連続関数 $f(x)$ が　$\displaystyle f(x)=\sin x+\int_0^xf(t)\,dt$　を満たすとき，$f(x)$ を求めよ。",
  "hint": r"右辺は微分可能だから $f(x)$ も微分可能。両辺を微分すると $f'(x)=\cos x+f(x)$，また $x=0$ とおいて $f(0)=0$。$f'-f$ の形は $e^{-x}$ を掛けると $\{e^{-x}f(x)\}'$ になる。",
  "sol": r"右辺は微分可能だから $f(x)$ も微分可能で，両辺を $x$ で微分すると $f'(x)=\cos x+f(x)$。また $x=0$ とおくと $f(0)=0$。<br>"
         r"$\{e^{-x}f(x)\}'=e^{-x}\{f'(x)-f(x)\}=e^{-x}\cos x$ だから，$0$ から $x$ まで積分して<br>"
         r"$\displaystyle e^{-x}f(x)-f(0)=\int_0^xe^{-t}\cos t\,dt$<br>"
         r"$\left\{\dfrac{e^{-t}(\sin t-\cos t)}2\right\}'=\dfrac{-e^{-t}(\sin t-\cos t)+e^{-t}(\cos t+\sin t)}2=e^{-t}\cos t$ より<br>"
         r"$\displaystyle\int_0^xe^{-t}\cos t\,dt=\frac{e^{-x}(\sin x-\cos x)}2+\frac12$<br>"
         r"よって $e^{-x}f(x)=\dfrac{e^{-x}(\sin x-\cos x)+1}2$ で　$\boldsymbol{f(x)=\dfrac{e^x+\sin x-\cos x}2}$<br>"
         r"逆にこのとき，$g(x)=f(x)-\sin x-\displaystyle\int_0^xf(t)\,dt$ は $g'(x)=f'(x)-\cos x-f(x)=0$，$g(0)=0$ を満たすから $g(x)=0$ となり，与えられた等式が成り立つ。",
  "note": r"「微分した式」と「$x=0$ を代入した式」の2つで，もとの積分方程式と同値になる。$f'(x)-f(x)=\cos x$ のような形を1階線形微分方程式といい，$e^{-x}$ を掛けて積の微分の形にするのが定石。",
  "ex": r"連続関数 $f(x)$ が　$\displaystyle f(x)=x^2+\int_0^xf(t)\,dt$　を満たすとき，$f(x)$ を求めよ。",
  "exa": r"$f(x)=2e^x-2x-2$"},
 {"lv": 4, "title": r"容器から流れ出る水（体積の変化と微分方程式）",
  "q": r"曲線 $y=x^2\ (x\geqq0)$ を $y$ 軸のまわりに1回転してできる曲面を内面とする容器がある（$y$ 軸は鉛直上向き，単位は cm）。この容器に水を入れ，底（原点）にあけた小さな穴から流出させる。水深が $h$ cm のとき，毎分 $k\sqrt h$ cm${}^3$（$k$ は正の定数）の割合で水が流出するものとする。水深が $4$ cm から $1$ cm になるまでに $7$ 分かかった。水深が $1$ cm になってから容器が空になるまでに何分かかるか。",
  "hint": r"水深 $h$ のときの水の体積 $V(h)$ を求め，$\dfrac{dV}{dt}=\dfrac{dV}{dh}\cdot\dfrac{dh}{dt}=-k\sqrt h$ とする。これを変形すると，$h$ のある累乗が $t$ の1次関数であることが分かる。",
  "sol": r"水深 $h$ のときの水の体積は　$\displaystyle V(h)=\pi\int_0^hx^2\,dy=\pi\int_0^hy\,dy=\frac\pi2h^2$<br>"
         r"時刻 $t$（分）における水深を $h$ とすると　$\dfrac{dV}{dt}=\dfrac{dV}{dh}\cdot\dfrac{dh}{dt}=\pi h\dfrac{dh}{dt}=-k\sqrt h$<br>"
         r"よって $\sqrt h\,\dfrac{dh}{dt}=-\dfrac k\pi$ で，$\dfrac{d}{dt}\left(h^{\frac32}\right)=\dfrac32\sqrt h\,\dfrac{dh}{dt}=-\dfrac{3k}{2\pi}$（一定）。<br>"
         r"したがって $h^{\frac32}$ は $t$ の1次関数で，一定の割合 $\dfrac{3k}{2\pi}$ で減少する。<br>"
         r"$h=4$ から $h=1$ まで，$h^{\frac32}$ は $8$ から $1$ まで $7$ だけ減少するのに $7$ 分かかったから，毎分 $1$ の割合で減少する。<br>"
         r"$h=1$ から $h=0$ まで，$h^{\frac32}$ は $1$ だけ減少するから，かかる時間は　$\boldsymbol{1}$ <b>分</b>",
  "note": r"流出の速さが $\sqrt h$ に比例するのはトリチェリの定理（穴から出る水の速さは $\sqrt{2gh}$）による。容器の形によって $V(h)$ が変わり，1次関数になる量も変わる。円柱の容器なら $\sqrt h$ が1次関数になる。",
  "ex": r"直線 $y=2x\ (x\geqq0)$ を $y$ 軸のまわりに1回転してできる円錐面を内面とする容器（頂点が下）に水を入れ，頂点の小さな穴から，水深 $h$ のとき毎分 $k\sqrt h$ の割合で流出させる。水深が $4$ cm から $1$ cm になるまでに $62$ 分かかった。水深が $1$ cm になってから空になるまでに何分かかるか。",
  "exa": r"$2$ 分"},
]})


def _v6():
    # 変数分離形
    for sol_, rhs, x0, y0 in ((3 * exp(x**2), lambda Y: 2 * x * Y, 0, 3), (2 * exp(sin(x)), lambda Y: Y * cos(x), 0, 2),
                               (log(exp(x) + E - 1), lambda Y: exp(x - Y), 0, 1)):
        assert _eq(diff(sol_, x) - rhs(sol_), 0) and _eq(sol_.subs(x, x0), y0)
    Y = sqrt(x**2 + 1)
    assert _eq(Y * diff(Y, x) - x, 0) and Y.subs(x, 0) == 1
    # 冷却
    kk = log(2) / 10
    T = 20 + 60 * 2**(-t / 10)
    assert _eq(diff(T, t) + kk * (T - 20), 0)
    assert T.subs(t, 0) == 80 and _eq(T.subs(t, 10), 50) and _eq(T.subs(t, 20), 35)
    t25 = 20 + 10 * log(3) / log(2)
    assert _eq(T.subs(t, t25), 25) and abs(float(t25) - 35.85) < 0.01
    # 細菌：N = N0 3^{t/2} → 5 時間で 3^{5/2}
    assert _eq(Rational(3)**Rational(5, 2), 9 * sqrt(3))
    # 接線の条件
    for t0 in (0.3, 1.0, 2.5, 7.0):
        f0, d0 = math.sqrt(t0), 0.5 / math.sqrt(t0)
        xq = t0 - f0 / d0
        assert abs((xq + t0) / 2) < 1e-12
        f0 = d0 = None
        f0, d0 = math.exp(t0 / 2), 0.5 * math.exp(t0 / 2)
        assert abs(t0 - (t0 - f0 / d0) - 2) < 1e-12
    # 積分方程式
    f = (exp(x) + sin(x) - cos(x)) / 2
    assert _eq(f - sin(x) - integrate(f.subs(x, t), (t, 0, x)), 0)
    assert _eq(diff(exp(-t) * (sin(t) - cos(t)) / 2, t), exp(-t) * cos(t))
    f = 2 * exp(x) - 2 * x - 2
    assert _eq(f - x**2 - integrate(f.subs(x, t), (t, 0, x)), 0)
    # 容器：h^{3/2} が毎分 1 ずつ減る → h(t) = (8-t)^{2/3}，k = 2π/3
    hh = (8 - t)**Rational(2, 3)
    V = pi * hh**2 / 2
    kv = 2 * pi / 3
    assert _eq(diff(V, t) + kv * sqrt(hh), 0)
    assert hh.subs(t, 0) == 4 and hh.subs(t, 7) == 1 and hh.subs(t, 8) == 0
    # 数値シミュレーション（RK4）：k を 7 分の条件から決め、残り時間を測る
    def run(Vp, k_, h0, h1, dt=1e-4):
        h_, tt_ = h0, 0.0
        g_ = lambda hv: -k_ * math.sqrt(max(hv, 0)) / Vp(hv)
        while h_ > h1:
            a1 = g_(h_); a2 = g_(h_ + dt / 2 * a1); a3 = g_(h_ + dt / 2 * a2); a4 = g_(h_ + dt * a3)
            h_ += dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            tt_ += dt
        return tt_
    Vp = lambda hv: math.pi * hv          # dV/dh
    assert abs(run(Vp, 2 * math.pi / 3, 4, 1) - 7) < 1e-3
    assert abs(run(Vp, 2 * math.pi / 3, 1, 1e-6) - 1) < 2e-3
    # 練習：円錐 V = πh^3/12，(h^{5/2})' = -10k/π，32→1 で 62 分 → k = π/20
    Vp2 = lambda hv: math.pi * hv * hv / 4
    assert abs(run(Vp2, math.pi / 20, 4, 1) - 62) < 1e-2
    assert abs(run(Vp2, math.pi / 20, 1, 1e-6) - 2) < 2e-3
    assert _eq(pi * integrate((y / 2)**2, (y, 0, a)), pi * a**3 / 12)


# ---------------------------------------------------------------- 第7節の図
def _f72():
    g = _G(190, 120, (-0.3, 5.6), (-0.15, 1.25))
    f = lambda u: 1 / (u * u)
    for kk in range(2, 6):
        g.poly([(kk - 1, 0), (kk - 1, f(kk)), (kk, f(kk)), (kk, 0)], fill=CF2, op=0.9, stroke=C2, w=0.7)
    g.axes()
    g.curve(f, 0.9, 5.5)
    for kk in range(1, 6):
        g.xtick(kk, str(kk))
    g.txt(1.15, 1.08, "y=1/x²", anc="start", it=True, size=9)
    return g.svg()


def _f73():
    g = _G(190, 120, (-0.3, 5.6), (-0.15, 1.25))
    f = lambda u: 1 / u
    for kk in range(1, 5):
        g.poly([(kk, 0), (kk, f(kk)), (kk + 1, f(kk)), (kk + 1, 0)], fill=CF2, op=0.9, stroke=C2, w=0.7)
    g.axes()
    g.curve(f, 0.85, 5.5)
    for kk in range(1, 6):
        g.xtick(kk, str(kk))
    g.txt(1.6, 0.95, "y=1/x", anc="start", it=True, size=9)
    return g.svg()


def _f75():
    g = _G(200, 130, (-0.15, 3.7), (-0.08, 1.15))
    f = lambda u: 1 / u
    k0 = 1.6
    g.band(lambda u: 0, f, k0 - 0.5, k0 + 0.5, fill=CF)
    g.axes(o="")
    g.curve(f, 0.85, 3.6)
    g.curve(lambda u: (2 * k0 - u) / k0**2, k0 - 0.8, k0 + 0.8, col=C3, w=1.0)
    a_, b_ = 2.6, 3.4
    g.seg((a_, f(a_)), (b_, f(b_)), col=C2, dash="", w=1.1)
    g.seg((a_, 0), (a_, f(a_)))
    g.seg((b_, 0), (b_, f(b_)))
    g.seg((k0, 0), (k0, f(k0)))
    g.xtick(k0, "k", dy=11)
    g.txt(k0 - 0.5, 0, "k−½", dy=11, size=8)
    g.txt(k0 + 0.5, 0, "k+½", dy=11, size=8)
    g.xtick(a_, "j", dy=11)
    g.xtick(b_, "j+1", dy=11)
    g.txt(1.0, 1.05, "y=1/x", anc="start", it=True, size=9)
    g.txt(0.8, 0.7, "接線", size=8, col=C3, anc="start")
    g.txt(3.0, 0.47, "弦", size=8, col=C2)
    return g.svg()


# ---------------------------------------------------------------- 節7
SEC.append({"title": r"積分と級数の評価",
"base": r"""・$a\leqq x\leqq b$ で連続な $f(x)$，$g(x)$ が $f(x)\leqq g(x)$ を満たし，等号がつねには成り立たないとき　$\displaystyle\int_a^bf(x)\,dx<\int_a^bg(x)\,dx$<br>
・$f(x)$ が減少関数のとき，$k\leqq x\leqq k+1$ で $f(k+1)\leqq f(x)\leqq f(k)$ より　$\displaystyle f(k+1)<\int_k^{k+1}f(x)\,dx<f(k)$<br>
　これを $k$ について加えると，和 $\sum f(k)$ を定積分ではさむことができる（幅 $1$ の長方形の面積と，曲線の下の面積との比較）。<br>
・下に凸な関数では，接線は曲線の下に，弦（2点を結ぶ線分）は曲線の上にある。これを使うと台形・中点による，より精密な評価ができる。""",
"items": [
 {"lv": 2, "title": r"定積分の値の評価",
  "q": r"不等式　$\displaystyle\frac43<\int_0^1e^{x^2}dx<e-1$　を証明せよ。",
  "hint": r"$e^{x^2}$ の不定積分は初等関数で表せない。$0<x<1$ で $e^{x^2}$ を，積分できる関数で上下からはさむ。下からは $e^u\geqq1+u$，上からは $x^2<x$ を使う。",
  "sol": r"$u>0$ で $g(u)=e^u-1-u$ とおくと $g'(u)=e^u-1>0$，$g(0)=0$ だから $g(u)>0$，すなわち $e^u>1+u$。<br>"
         r"$0<x<1$ のとき，$u=x^2$ として $e^{x^2}>1+x^2$。また $x^2<x$ より $e^{x^2}<e^x$。よって $0<x<1$ で<br>"
         r"$1+x^2<e^{x^2}<e^x$<br>"
         r"各辺は連続だから，$0$ から $1$ まで積分して<br>"
         r"$\displaystyle\int_0^1(1+x^2)\,dx<\int_0^1e^{x^2}dx<\int_0^1e^x\,dx$　すなわち　$\displaystyle\boldsymbol{\frac43<\int_0^1e^{x^2}dx<e-1}$",
  "note": r"実際の値は約 $1.4627$。$e^u>1+u+\dfrac{u^2}2\ (u>0)$ を使うと下からの評価は $\dfrac43+\dfrac1{10}=\dfrac{43}{30}\fallingdotseq1.433$ に改良される。",
  "ex": r"不等式　$\displaystyle\frac12<\int_0^{\frac12}\frac{dx}{\sqrt{1-x^4}}<\frac\pi6$　を証明せよ。",
  "exa": r"$0<x<\dfrac12$ で $1<\dfrac1{\sqrt{1-x^4}}<\dfrac1{\sqrt{1-x^2}}$ を積分する。右辺の積分は $x=\sin\theta$ とおいて $\dfrac\pi6$。"},
 {"lv": 2, "title": r"和を積分で上から評価する",
  "q": r"$2$ 以上の自然数 $n$ に対して，不等式　$\displaystyle\sum_{k=1}^n\frac1{k^2}<2-\frac1n$　を証明せよ。",
  "hint": r"$\dfrac1{k^2}$ を，底辺 $1$・高さ $\dfrac1{k^2}$ の長方形の面積とみる。区間 $k-1\leqq x\leqq k$ にとると，長方形は曲線 $y=\dfrac1{x^2}$ の下に入る。",
  "sol": _f72() + r"$k\geqq2$ のとき，$k-1\leqq x\leqq k$ で $\dfrac1{x^2}\geqq\dfrac1{k^2}$（等号は $x=k$ のときのみ）だから<br>"
         r"$\displaystyle\frac1{k^2}<\int_{k-1}^k\frac{dx}{x^2}$<br>"
         r"$k=2,\ 3,\ \cdots,\ n$ について加えると　$\displaystyle\sum_{k=2}^n\frac1{k^2}<\int_1^n\frac{dx}{x^2}=\Big[-\frac1x\Big]_1^n=1-\frac1n$<br>"
         r"両辺に $1$ を加えて　$\displaystyle\sum_{k=1}^n\frac1{k^2}<2-\frac1n$",
  "note": r"$k=1$ の項まで積分にふくめると $\displaystyle\int_0^1\frac{dx}{x^2}$ が現れて評価できない。最初の項は別にしておくのがコツ。この結果から $\displaystyle\sum_{k=1}^\infty\frac1{k^2}$ は収束し，その和は $2$ 以下である（実際の値は $\dfrac{\pi^2}6\fallingdotseq1.645$）。",
  "ex": r"自然数 $n$ に対して，不等式　$\displaystyle\sum_{k=1}^n\frac1{k^3}<\frac32$　を証明せよ。",
  "exa": r"$k\geqq2$ で $\dfrac1{k^3}<\displaystyle\int_{k-1}^k\frac{dx}{x^3}$ を $k=2$ から $n$ まで加えると，和 $<1+\dfrac12\left(1-\dfrac1{n^2}\right)<\dfrac32$（$n=1$ は明らか）。"},
 {"lv": 3, "title": r"調和級数と $\log n$ の比較",
  "q": r"(1) $2$ 以上の自然数 $n$ に対して，不等式　$\displaystyle\log(n+1)<\sum_{k=1}^n\frac1k<1+\log n$　を証明せよ。<br>(2) 極限 $\displaystyle\lim_{n\to\infty}\frac1{\log n}\sum_{k=1}^n\frac1k$ を求めよ。",
  "hint": r"$k\leqq x\leqq k+1$ で $\dfrac1{k+1}\leqq\dfrac1x\leqq\dfrac1k$。左側の不等式は長方形が曲線の上にある図，右側は下にある図に対応する。(2) は (1) を $\log n$ で割って，はさみうちの原理を使う。",
  "sol": _f73() + r"(1) $k\leqq x\leqq k+1$ で $\dfrac1{k+1}\leqq\dfrac1x\leqq\dfrac1k$ で，等号はつねには成り立たないから<br>"
         r"$\displaystyle\frac1{k+1}<\int_k^{k+1}\frac{dx}x<\frac1k$　……①<br>"
         r"① の右側を $k=1,\ 2,\ \cdots,\ n$ について加えると　$\displaystyle\sum_{k=1}^n\frac1k>\int_1^{n+1}\frac{dx}x=\log(n+1)$<br>"
         r"① の左側を $k=1,\ 2,\ \cdots,\ n-1$ について加えると　$\displaystyle\sum_{k=2}^n\frac1k<\int_1^n\frac{dx}x=\log n$　より　$\displaystyle\sum_{k=1}^n\frac1k<1+\log n$<br>"
         r"(2) $n\geqq2$ のとき $\log n>0$ だから，(1) の各辺を $\log n$ で割って<br>"
         r"$\displaystyle\frac{\log(n+1)}{\log n}<\frac1{\log n}\sum_{k=1}^n\frac1k<\frac1{\log n}+1$<br>"
         r"$\log(n+1)>\log n$ より左辺 $>1$，右辺 $\to1\ (n\to\infty)$ だから，はさみうちの原理により　$\displaystyle\lim_{n\to\infty}\frac1{\log n}\sum_{k=1}^n\frac1k=\boldsymbol{1}$",
  "note": r"(1) より $\displaystyle\sum_{k=1}^n\frac1k\to\infty$（調和級数は発散）であることも分かる。さらに $\displaystyle a_n=\sum_{k=1}^n\frac1k-\log n$ は減少数列で $0<a_n\leqq1$ を満たし，ある値（オイラーの定数 $\gamma\fallingdotseq0.577$）に収束する。",
  "ex": r"(1) $2$ 以上の自然数 $n$ に対して，不等式　$\displaystyle2\sqrt{n+1}-2<\sum_{k=1}^n\frac1{\sqrt k}<2\sqrt n-1$　を証明せよ。<br>(2) 極限 $\displaystyle\lim_{n\to\infty}\frac1{\sqrt n}\sum_{k=1}^n\frac1{\sqrt k}$ を求めよ。",
  "exa": r"(1) $\dfrac1{\sqrt{k+1}}<\displaystyle\int_k^{k+1}\frac{dx}{\sqrt x}<\frac1{\sqrt k}$ を加える。(2) $2$"},
 {"lv": 4, "title": r"$\log n!$ の評価と極限",
  "q": r"(1) $2$ 以上の自然数 $n$ に対して，不等式　$n\log n-n+1<\log n!<(n+1)\log(n+1)-n$　を証明せよ。<br>(2) 極限 $\displaystyle\lim_{n\to\infty}\frac{\sqrt[n]{n!}}{n}$ を求めよ。",
  "hint": r"$\log n!=\log1+\log2+\cdots+\log n$ は「高さ $\log k$ の長方形の和」。$\log x$ は増加関数だから，$\displaystyle\int_{k-1}^k\log x\,dx<\log k<\int_k^{k+1}\log x\,dx$。(2) は対数をとって (1) を $n$ で割る。",
  "sol": r"(1) $\log x$ は増加関数だから，$k-1\leqq x\leqq k$ で $\log x\leqq\log k$，$k\leqq x\leqq k+1$ で $\log x\geqq\log k$（等号はそれぞれ $x=k$ のときのみ）。よって<br>"
         r"$\displaystyle\int_{k-1}^k\log x\,dx<\log k<\int_k^{k+1}\log x\,dx$<br>"
         r"左側を $k=2,\ \cdots,\ n$ について加えると　$\displaystyle\log n!=\sum_{k=2}^n\log k>\int_1^n\log x\,dx=\Big[x\log x-x\Big]_1^n=n\log n-n+1$<br>"
         r"右側を $k=1,\ \cdots,\ n$ について加えると　$\displaystyle\log n!<\int_1^{n+1}\log x\,dx=(n+1)\log(n+1)-(n+1)+1=(n+1)\log(n+1)-n$<br>"
         r"(2) $a_n=\log\dfrac{\sqrt[n]{n!}}n=\dfrac1n\log n!-\log n$ とおく。(1) の各辺を $n$ で割って $\log n$ を引くと<br>"
         r"$\displaystyle-1+\frac1n<a_n<\frac{n+1}n\log(n+1)-1-\log n=\log\left(1+\frac1n\right)+\frac{\log(n+1)}n-1$<br>"
         r"$n\to\infty$ のとき $\log\left(1+\dfrac1n\right)\to0$，$\dfrac{\log(n+1)}n=\dfrac{\log(n+1)}{n+1}\cdot\dfrac{n+1}n\to0$（$\displaystyle\lim_{x\to\infty}\frac{\log x}x=0$）だから，はさみうちの原理により $a_n\to-1$。<br>"
         r"よって　$\displaystyle\lim_{n\to\infty}\frac{\sqrt[n]{n!}}n=\boldsymbol{\frac1e}$",
  "note": r"$\log n!$ は $n\log n-n$ とほぼ等しい（誤差は $\log n$ 程度）。さらに精密には $n!\fallingdotseq\sqrt{2\pi n}\left(\dfrac ne\right)^n$（スターリングの公式）が知られている。区分求積法を使って $\displaystyle\lim a_n=\int_0^1\log x\,dx=-1$ と見ることもできる。",
  "ex": r"極限 $\displaystyle\lim_{n\to\infty}\sqrt[n]{\frac{(2n)!}{n!\,n^n}}$ を求めよ。",
  "exa": r"$\dfrac4e$"},
 {"lv": 5, "title": r"$\log2$ との差の精密な評価（凸性による台形・中点評価）",
  "q": r"$\displaystyle S_n=\sum_{k=n+1}^{2n}\frac1k$ とする。極限 $\displaystyle\lim_{n\to\infty}n(\log2-S_n)$ を求めよ。",
  "hint": r"長方形による評価 $\displaystyle\int_{n+1}^{2n+1}\frac{dx}x<S_n<\int_n^{2n}\frac{dx}x$ では誤差が $\dfrac1n$ の程度でしか分からず，$n$ 倍すると極限が決まらない。$y=\dfrac1x$ が下に凸であることから，弦（台形）で上から，接線（中点）で下から積分をはさむ。",
  "sol": _f75() + r"<b>[1] 弦による評価</b>　$j\leqq x\leqq j+1$（$j$ は自然数）で，2点 $\left(j,\ \dfrac1j\right)$，$\left(j+1,\ \dfrac1{j+1}\right)$ を結ぶ弦 $\ell_j(x)=\dfrac1j+\dfrac1{j+1}-\dfrac{x}{j(j+1)}$ について<br>"
         r"$xj(j+1)\left\{\ell_j(x)-\dfrac1x\right\}=(2j+1)x-x^2-j(j+1)=-(x-j)(x-j-1)\geqq0$<br>"
         r"等号は端点のみだから　$\displaystyle\int_j^{j+1}\frac{dx}x<\int_j^{j+1}\ell_j(x)\,dx=\frac12\left(\frac1j+\frac1{j+1}\right)$（台形の面積）<br>"
         r"$j=n,\ n+1,\ \cdots,\ 2n-1$ について加えると<br>"
         r"$\displaystyle\log2=\int_n^{2n}\frac{dx}x<\frac12\sum_{j=n}^{2n-1}\left(\frac1j+\frac1{j+1}\right)=\frac12\left\{\left(\frac1n+S_n-\frac1{2n}\right)+S_n\right\}=S_n+\frac1{4n}$<br>"
         r"よって　$n(\log2-S_n)<\dfrac14$　……①<br>"
         r"<b>[2] 接線による評価</b>　自然数 $k$ と $x>0$ に対し，$x=k$ における接線 $y=\dfrac{2k-x}{k^2}$ について　$\dfrac1x-\dfrac{2k-x}{k^2}=\dfrac{(x-k)^2}{k^2x}\geqq0$（等号は $x=k$ のみ）<br>"
         r"よって　$\displaystyle\int_{k-\frac12}^{k+\frac12}\frac{dx}x>\int_{k-\frac12}^{k+\frac12}\frac{2k-x}{k^2}\,dx=\frac{2k-k}{k^2}=\frac1k$（台形の面積は中点の高さ × 幅）<br>"
         r"$k=n+1,\ \cdots,\ 2n$ について加えると　$\displaystyle S_n<\int_{n+\frac12}^{2n+\frac12}\frac{dx}x=\log\frac{4n+1}{2n+1}$<br>"
         r"よって　$\log2-S_n>\log\dfrac{2(2n+1)}{4n+1}=\log\left(1+\dfrac1{4n+1}\right)$　……②<br>"
         r"<b>[3] 極限</b>　$h_n=\dfrac1{4n+1}$ とおくと，② より　$n(\log2-S_n)>n\log(1+h_n)=\dfrac{n}{4n+1}\cdot\dfrac{\log(1+h_n)}{h_n}$<br>"
         r"$n\to\infty$ のとき $h_n\to0$ で，$\displaystyle\lim_{h\to0}\frac{\log(1+h)}h=1$ だから右辺 $\to\dfrac14$。① と合わせ，はさみうちの原理により<br>"
         r"$\displaystyle\lim_{n\to\infty}n(\log2-S_n)=\boldsymbol{\frac14}$",
  "note": r"$S_n\to\log2$ だけなら長方形の評価で足りるが，「差が $\dfrac1n$ の何倍か」を問われると，誤差の主要部まで正確にとらえる評価が必要になる。弦（台形公式）は下に凸な関数の積分を大きく，接線（中点公式）は小さく見積もる。実は $\log2-S_n=\dfrac1{4n}-\dfrac1{16n^2}+\cdots$ である。一般に $\displaystyle\lim_{n\to\infty}n\left(\log m-\sum_{k=n+1}^{mn}\frac1k\right)=\frac{m-1}{2m}$ となる。",
  "ex": r"$\displaystyle T_n=\sum_{k=n+1}^{3n}\frac1k$ とする。極限 $\displaystyle\lim_{n\to\infty}n(\log3-T_n)$ を求めよ。",
  "exa": r"$\dfrac13$"},
]})


def _v7():
    from fractions import Fraction as Fr
    # 定積分の評価
    I = _simpson(lambda u: math.exp(u * u), 0, 1)
    assert 4 / 3 < I < math.e - 1 and abs(I - 1.4627) < 1e-4
    assert all(1 + u * u < math.exp(u * u) < math.exp(u) for u in np.linspace(0.001, 0.999, 999))
    assert _eq(integrate(1 + x**2 + x**4 / 2, (x, 0, 1)), Rational(43, 30))
    J = _simpson(lambda u: 1 / math.sqrt(1 - u**4), 0, 0.5)
    assert 0.5 < J < math.pi / 6
    assert _eq(integrate(1, (th, 0, pi / 6)), pi / 6) and abs(math.asin(0.5) - math.pi / 6) < 1e-15
    assert all(1 < 1 / math.sqrt(1 - u**4) < 1 / math.sqrt(1 - u * u) for u in np.linspace(0.001, 0.499, 499))
    # Σ1/k^2, Σ1/k^3（厳密な有理数で）
    s2, s3 = Fr(0), Fr(0)
    for m in range(1, 301):
        s2 += Fr(1, m * m)
        s3 += Fr(1, m**3)
        if m >= 2:
            assert s2 < 2 - Fr(1, m)
        assert s3 < Fr(3, 2) and s3 < 1 + Fr(1, 2) * (1 - Fr(1, m * m)) + (0 if m > 1 else 1)
    # 調和級数
    H = 0.0
    R = 0.0
    for m in range(1, 20001):
        H += 1 / m
        R += 1 / math.sqrt(m)
        if m >= 2:
            assert math.log(m + 1) < H < 1 + math.log(m)
            assert 2 * math.sqrt(m + 1) - 2 < R < 2 * math.sqrt(m) - 1
    assert 1 < H / math.log(20000) < 1 + 1 / math.log(20000)
    assert abs(R / math.sqrt(20000) - 2) < 0.02 and (2 * math.sqrt(20001) - 2) / math.sqrt(20000) < R / math.sqrt(20000) < 2
    # log n!
    for m in range(2, 2001):
        L = math.lgamma(m + 1)
        assert m * math.log(m) - m + 1 < L < (m + 1) * math.log(m + 1) - m
    assert _eq(integrate(log(x), (x, 1, n)), n * log(n) - n + 1)
    m = 10**7
    assert abs(math.exp(math.lgamma(m + 1) / m) / m - 1 / math.e) < 1e-5
    assert abs(math.exp((math.lgamma(2 * m + 1) - math.lgamma(m + 1)) / m - math.log(m)) - 4 / math.e) < 1e-5
    # log2 との差
    jj, xx = symbols("j xx", positive=True)
    lj = 1 / jj + 1 / (jj + 1) - xx / (jj * (jj + 1))
    assert _eq(expand(xx * jj * (jj + 1) * (lj - 1 / xx)), expand(-(xx - jj) * (xx - jj - 1)))
    assert _eq(integrate(lj, (xx, jj, jj + 1)), (1 / jj + 1 / (jj + 1)) / 2)
    assert _eq(1 / xx - (2 * jj - xx) / jj**2 - (xx - jj)**2 / (jj**2 * xx), 0)
    assert _eq(integrate((2 * jj - xx) / jj**2, (xx, jj - Rational(1, 2), jj + Rational(1, 2))), 1 / jj)
    for m in range(1, 3001):
        Sn = sum(1 / q for q in range(m + 1, 2 * m + 1))
        d = math.log(2) - Sn
        assert math.log(1 + 1 / (4 * m + 1)) < d < 1 / (4 * m)
        assert Sn < math.log((4 * m + 1) / (2 * m + 1))
        if m % 500 == 0:
            Tn = sum(1 / q for q in range(m + 1, 3 * m + 1))
            e3 = math.log(3) - Tn
            assert math.log(1 + 2 / (6 * m + 1)) < e3 < 1 / (3 * m)
    m = 10**6
    Sn = math.fsum(1 / q for q in range(m + 1, 2 * m + 1))
    assert abs(m * (math.log(2) - Sn) - 0.25) < 1e-5
    Tn = math.fsum(1 / q for q in range(m + 1, 3 * m + 1))
    assert abs(m * (math.log(3) - Tn) - 1 / 3) < 1e-5
    # 検討の主張：log2 - S_n = 1/(4n) - 1/(16n^2) + …、一般に n(log m - Σ_{n+1}^{mn} 1/k) → (m-1)/(2m)
    m = 2000
    d = math.log(2) - math.fsum(1 / q for q in range(m + 1, 2 * m + 1))
    assert abs(m * m * (1 / (4 * m) - d) - 1 / 16) < 1e-3
    for mm in (2, 3, 4, 5):
        m = 200000
        d = math.log(mm) - math.fsum(1 / q for q in range(m + 1, mm * m + 1))
        assert abs(m * d - (mm - 1) / (2 * mm)) < 1e-4
    # オイラーの定数の近似：a_n = H_n - log n は減少し 0 < a_n ≦ 1
    Hs, prev = 0.0, 2.0
    for m in range(1, 5001):
        Hs += 1 / m
        an = Hs - math.log(m)
        assert 0 < an <= 1 and an < prev
        prev = an
    assert abs(an - 0.5772) < 1e-3
    # 台形の和の計算 S_n + 1/(4n)
    for m in (3, 7, 20):
        lhs = sum(Fr(1, 2) * (Fr(1, q) + Fr(1, q + 1)) for q in range(m, 2 * m))
        assert lhs == sum(Fr(1, q) for q in range(m + 1, 2 * m + 1)) + Fr(1, 4 * m)
        lhs = sum(Fr(1, 2) * (Fr(1, q) + Fr(1, q + 1)) for q in range(m, 3 * m))
        assert lhs == sum(Fr(1, q) for q in range(m + 1, 3 * m + 1)) + Fr(1, 3 * m)


# ---------------------------------------------------------------- 第8節の図
def _f82():
    g = _G(165, 165, (-0.12, 1.18), (-0.12, 1.18), eq=True)
    ast = [(math.cos(u)**3, math.sin(u)**3) for u in np.linspace(0, math.pi / 2, 120)]
    g.poly([(0, 0)] + ast, fill=CF, op=0.9)
    g.axes()
    for i in range(1, 12):
        th_ = math.pi / 2 * i / 12
        g.seg((math.cos(th_), 0), (0, math.sin(th_)), col=C1, dash="", w=0.6)
    g.pcurve(lambda u: math.cos(u)**3, lambda u: math.sin(u)**3, 0, math.pi / 2, col=C2, w=1.5)
    th_ = math.pi / 2 * 4 / 12
    g.pt(math.cos(th_), 0)
    g.pt(0, math.sin(th_))
    g.txt(math.cos(th_), 0, "P", dy=11, size=10)
    g.txt(0, math.sin(th_), "Q", dx=-6, dy=4, anc="end", size=10)
    g.xtick(1, "1", dy=11, dx=3)
    g.ytick(1, "1")
    return g.svg()


def _f83():
    g = _G(150, 150, (-0.2, 1.3), (-0.2, 1.3), eq=True)
    g.band(lambda u: u * u, lambda u: u, 0, 1)
    g.axes()
    g.curve(lambda u: u * u, -0.15, 1.14)
    g.seg((-0.15, -0.15), (1.28, 1.28), col=C2, dash="", w=1.2)
    x0 = 0.62
    P = (x0, x0 * x0)
    h = (x0 + x0 * x0) / 2
    H = (h, h)
    g.seg(P, H, col=C3, dash="", w=1.3)
    g.pt(*P)
    g.pt(*H, col=C2)
    g.txt(*P, "P", dx=6, dy=8, size=10)
    g.txt(*H, "H", dx=-5, dy=-4, size=10, anc="end")
    g.txt(h / 2, h / 2, "s", dx=-6, dy=-2, it=True, size=10, col=C2)
    g.txt(0.95, 1.2, "y=x", anc="end", it=True, size=9, col=C2)
    g.txt(1.15, 0.85, "y=x²", anc="start", it=True, size=9, dx=-14)
    return g.svg()


def _f84():
    g = _G(175, 185, (-1.6, 2.6), (-0.5, 4.6), eq=True)
    g.band(lambda u: u * u, lambda u: u + 2, -1, 2)
    g.axes()
    g.curve(lambda u: u * u, -1.5, 2.1)
    g.curve(lambda u: u + 2, -1.6, 2.55, col=C2, w=1.2)
    c0 = -0.17
    al, be = (-1 - math.sqrt(1 + 4 * c0)) / 2, (-1 + math.sqrt(1 + 4 * c0)) / 2
    g.curve(lambda u: c0 - u, -1.55, 0.25, col=C3, w=1.0)
    g.pt(al, al * al, col=C3)
    g.pt(be, be * be, col=C3)
    g.txt(al, al * al, "A", dx=-6, dy=-2, size=9, anc="end")
    g.txt(be, be * be, "B", dx=5, dy=-3, size=9, anc="start")
    c1 = 3.2
    b1 = (-1 + math.sqrt(1 + 4 * c1)) / 2
    g.curve(lambda u: c1 - u, (c1 - 2) / 2 - 0.4, b1 + 0.4, col=C3, w=1.0, dash=DASH)
    g.pt(b1, b1 * b1, col=C3)
    g.txt(2.55, 4.38, "ℓ", anc="end", it=True, size=11, col=C2)
    g.txt(-1.45, 3.0, "y=x²", anc="start", it=True, size=9)
    g.xtick(-1, "−1", dy=11, dx=-3)
    g.xtick(2, "2", dy=11)
    return g.svg()


def _f85():
    P = lambda X, Y, Z: (Y - 0.45 * X, Z - 0.33 * X)
    g = _G(165, 165, (-0.55, 1.1), (-0.45, 1.15), eq=True)
    V = [(i, j, k_) for i in (0, 1) for j in (0, 1) for k_ in (0, 1)]
    for A in V:
        for B in V:
            if A < B and sum(abs(A[q] - B[q]) for q in range(3)) == 1:
                hidden = (A == (0, 0, 0) or B == (0, 0, 0))
                g.seg(P(*A), P(*B), col="#555", w=0.8, dash=DASH if hidden else "")
    u0 = 1.5
    hexa = [(1, u0 - 1, 0), (1, 0, u0 - 1), (u0 - 1, 0, 1), (0, u0 - 1, 1), (0, 1, u0 - 1), (u0 - 1, 1, 0)]
    g.poly([P(*q) for q in hexa], fill=CF2, op=0.75, stroke=C2, w=1.0)
    g.seg(P(0, 0, 0), P(1, 1, 1), col=C1, dash="", w=1.4)
    g.pt(*P(0.5, 0.5, 0.5), col=C1)
    g.txt(*P(0, 0, 0), "O", dx=-5, dy=4, size=10, anc="end")
    g.txt(*P(1, 1, 1), "G", dx=5, dy=-2, size=10, anc="start")
    g.txt(*P(0.5, 0.5, 0.5), "M", dx=6, dy=10, size=9)
    return g.svg()


def _f86():
    g = _G(160, 160, (-1.3, 1.3), (-1.3, 1.3), eq=True)
    al = 0.42
    a_, t_ = math.cos(al), math.sin(al)
    pts = []
    for q in range(4):
        base = q * math.pi / 2
        for u in np.linspace(-math.pi / 4, math.pi / 4, 60):
            ang = base + u
            r = min(1.0, a_ / max(abs(math.cos(u)), 1e-12))
            pts.append((r * math.cos(ang), r * math.sin(ang)))
    g.poly(pts, fill=CF, op=0.95)
    g.pcurve(math.cos, math.sin, 0, 2 * math.pi, col=CG, w=0.8)
    g.poly([(a_, a_), (-a_, a_), (-a_, -a_), (a_, -a_)], fill="none", op=1, stroke=C2, w=1.0)
    g.axes()
    g.seg((0, 0), (a_, t_), col=C1, dash="", w=0.9)
    g.seg((0, 0), (1.05 * math.cos(math.pi / 4), 1.05 * math.sin(math.pi / 4)), col=CG)
    g.pt(a_, t_)
    g.txt(a_, t_, "(a, t)", dx=4, dy=-3, anc="start", size=9)
    g.txt(0.35, 0.07, "α", it=True, size=9)
    g.txt(a_, 0, "a", dx=4, dy=11, it=True, size=10, col=C2)
    return g.svg()


def _f87():
    g = _G(190, 155, (-1.3, 1.65), (-1.2, 1.2), eq=True)
    g.axes(yl="z")
    for t_ in (0, 0.2, 0.4, 0.6, 0.8, 0.92):
        r = math.sqrt(1 - t_ * t_)
        g.pcurve(lambda u, t_=t_, r=r: t_ + r * math.cos(u), lambda u, r=r: r * math.sin(u), 0, 2 * math.pi, col=C1, w=0.6, n=120)
    g.pcurve(math.cos, math.sin, math.pi / 2, 3 * math.pi / 2, col=C2, w=1.8)
    g.pcurve(lambda u: math.sqrt(2) * math.cos(u), math.sin, -math.pi / 2, math.pi / 2, col=C2, w=1.8)
    g.xtick(math.sqrt(2), "√2", dy=11, dx=4)
    g.xtick(-1, "−1", dy=11, dx=-9)
    g.xtick(1, "1", dy=11, dx=-4)
    return g.svg()


# ---------------------------------------------------------------- 節8
SEC.append({"title": r"最難関の体積・面積（立体の切り口・斜めの回転軸・通過領域）",
"base": r"""・回転体でない立体も，切り口の面積が分かれば体積が求まる。切り口が簡単になる方向を選ぶ（対称性を利用する）。<br>
・回転体の切り口：回転させる図形を，回転軸に垂直な平面で切った切り口 $K$ を考える。$K$ がつながっているとき，回転体の切り口は，$K$ の点と軸との距離の最大値 $R$，最小値 $r$ による円環（$K$ が軸と交われば $r=0$ で円）で，面積は $\pi(R^2-r^2)$。<br>
・回転軸が斜めのとき：軸上に座標 $s$ をとり，各 $s$ での半径を図形上の点の座標で表して $\displaystyle V=\pi\int(R^2-r^2)\,ds$ を置換積分する。$s$ が単調に動くかどうかに注意。<br>
・通過領域：動かすもの（パラメータ）を固定するのではなく，<b>切り口（座標）を固定してパラメータを動かし</b>，その切り口に現れる点の範囲を調べる。""",
"items": [
 {"lv": 4, "title": r"立体の切り口（2つの円柱の共通部分）",
  "q": r"座標空間において，2つの円柱 $x^2+y^2\leqq1$，$x^2+z^2\leqq1$ の共通部分の体積 $V$ を求めよ。",
  "hint": r"どちらの円柱も，$x$ 軸に垂直な平面で切ると切り口は帯状になる。その共通部分は正方形。$z$ 軸に垂直に切ると「円と帯の共通部分」となり計算が複雑。",
  "sol": r"平面 $x=t\ (-1\leqq t\leqq1)$ による切り口は　$y^2\leqq1-t^2$ かつ $z^2\leqq1-t^2$，すなわち $|y|\leqq\sqrt{1-t^2}$，$|z|\leqq\sqrt{1-t^2}$<br>"
         r"で表される1辺 $2\sqrt{1-t^2}$ の正方形で，面積は $4(1-t^2)$。よって<br>"
         r"$\displaystyle V=\int_{-1}^14(1-t^2)\,dt=8\int_0^1(1-t^2)\,dt=\boldsymbol{\frac{16}3}$",
  "note": r"同じ平面で単位球を切ると，切り口はこの正方形の内接円（面積 $\pi(1-t^2)$）になる。切り口の面積の比がつねに $\pi:4$ だから，体積の比も $\pi:4$ で，$\dfrac43\pi:\dfrac{16}3=\pi:4$ と確かめられる。",
  "ex": r"座標空間において，円柱 $x^2+y^2\leqq1$ と，不等式 $|y|+|z|\leqq1$ の表す立体の共通部分の体積を求めよ。",
  "exa": r"$2\pi-\dfrac83$"},
 {"lv": 4, "title": r"線分の通過領域の面積",
  "q": r"座標平面上で，長さ $1$ の線分 $\mathrm{PQ}$ が，端点 $\mathrm{P}$ は $x$ 軸の $x\geqq0$ の部分を，端点 $\mathrm{Q}$ は $y$ 軸の $y\geqq0$ の部分を動く。線分 $\mathrm{PQ}$ が通過する領域の面積 $S$ を求めよ。",
  "hint": r"線分を1本ずつ描いても領域の境界は分からない。$x=a$ を固定し，線分を動かしたときに直線 $x=a$ 上で通過する点の $y$ 座標の範囲を，$\theta$ の関数の最大値として求める。",
  "sol": _f82() + r"$\mathrm{P}(\cos\theta,\ 0)$，$\mathrm{Q}(0,\ \sin\theta)\ \left(0\leqq\theta\leqq\dfrac\pi2\right)$ と表せる。$0<\theta<\dfrac\pi2$ のとき，線分 $\mathrm{PQ}$ は　$\dfrac x{\cos\theta}+\dfrac y{\sin\theta}=1\ (0\leqq x\leqq\cos\theta)$<br>"
         r"$0<a<1$ を固定する。線分 $\mathrm{PQ}$ が直線 $x=a$ と交わるのは $a\leqq\cos\theta$ のときで，$\cos\theta_0=a\ \left(0<\theta_0<\dfrac\pi2\right)$ とすると $0\leqq\theta\leqq\theta_0$。交点の $y$ 座標は<br>"
         r"$g(\theta)=\sin\theta\left(1-\dfrac a{\cos\theta}\right)=\sin\theta-a\tan\theta$，　$g'(\theta)=\cos\theta-\dfrac a{\cos^2\theta}=\dfrac{\cos^3\theta-a}{\cos^2\theta}$<br>"
         r"$\cos^3\theta_1=a$ となる $\theta_1\ (0<\theta_1<\theta_0)$ で $g$ は増加から減少に変わり，$a=\cos^3\theta_1$ より $1-\dfrac a{\cos\theta_1}=\sin^2\theta_1$ だから<br>"
         r"最大値 $g(\theta_1)=\sin^3\theta_1=(1-\cos^2\theta_1)^{\frac32}=\left(1-a^{\frac23}\right)^{\frac32}$<br>"
         r"$g(0)=g(\theta_0)=0$ で $g$ は連続だから，直線 $x=a$ 上で通過する点の $y$ 座標の範囲は $0\leqq y\leqq\left(1-a^{\frac23}\right)^{\frac32}$。よって<br>"
         r"$\displaystyle S=\int_0^1\left(1-x^{\frac23}\right)^{\frac32}dx$<br>"
         r"$x=\cos^3u\ \left(0\leqq u\leqq\dfrac\pi2\right)$ とおくと $dx=-3\cos^2u\sin u\,du$，$\left(1-x^{\frac23}\right)^{\frac32}=\sin^3u$，$x:0\to1$ に $u:\dfrac\pi2\to0$ が対応して<br>"
         r"$\displaystyle S=\int_{\frac\pi2}^0\sin^3u\cdot(-3\cos^2u\sin u)\,du=3\int_0^{\frac\pi2}\sin^4u\cos^2u\,du$<br>"
         r"$\sin^4u\cos^2u=\dfrac{\sin^22u}4\cdot\dfrac{1-\cos2u}2=\dfrac18(\sin^22u-\sin^22u\cos2u)$ で<br>"
         r"$\displaystyle\int_0^{\frac\pi2}\sin^22u\,du=\frac\pi4$，$\displaystyle\int_0^{\frac\pi2}\sin^22u\cos2u\,du=\Big[\frac{\sin^32u}6\Big]_0^{\frac\pi2}=0$　だから　$S=3\cdot\dfrac18\cdot\dfrac\pi4=\boldsymbol{\dfrac{3}{32}\pi}$",
  "note": r"領域の境界 $x^{\frac23}+y^{\frac23}=1$ はアステロイドで，すべての線分 $\mathrm{PQ}$ に接する曲線（包絡線）である。「$x$ を固定してパラメータを動かす」方法は，数学IIの通過領域と同じ考え方。",
  "ex": r"座標平面上で，点 $\mathrm{P}$ は $x$ 軸の $x\geqq0$ の部分を，点 $\mathrm{Q}$ は $y$ 軸の $y\geqq0$ の部分を，$\mathrm{OP}+\mathrm{OQ}=1$（$\mathrm{O}$ は原点）を満たしながら動く。線分 $\mathrm{PQ}$ が通過する領域の面積を求めよ。",
  "exa": r"$\dfrac16$"},
 {"lv": 4, "title": r"回転軸が斜めの回転体",
  "q": r"放物線 $y=x^2$ と直線 $y=x$ で囲まれた部分を，直線 $y=x$ のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"回転軸 $y=x$ 上に原点からの距離 $s$ をとる。放物線上の点 $\mathrm{P}(x,\ x^2)$ から軸に下ろした垂線の足を $\mathrm{H}$ とし，半径 $\mathrm{PH}$ と $s=\mathrm{OH}$ を $x$ で表して，$\displaystyle\pi\int\mathrm{PH}^2\,ds$ を $x$ の積分に置換する。",
  "sol": _f83() + r"$0\leqq x\leqq1$ で $x^2\leqq x$。$\mathrm{P}(x,\ x^2)\ (0\leqq x\leqq1)$ から直線 $y=x$ に下ろした垂線の足を $\mathrm{H}$ とすると<br>"
         r"$\mathrm{PH}=\dfrac{|x-x^2|}{\sqrt2}=\dfrac{x-x^2}{\sqrt2}$（点と直線の距離），　$s=\mathrm{OH}=\dfrac{x+x^2}{\sqrt2}$（$\overrightarrow{\mathrm{OP}}$ と単位ベクトル $\dfrac1{\sqrt2}(1,\ 1)$ の内積）<br>"
         r"$\dfrac{ds}{dx}=\dfrac{1+2x}{\sqrt2}>0$ より，$s$ は $x$ とともに $0$ から $\sqrt2$ まで増加する。よって軸上の各点 $\mathrm{H}$ で軸に垂直な直線と図形の共通部分は線分 $\mathrm{HP}$ で，回転体の切り口は半径 $\mathrm{PH}$ の円。したがって<br>"
         r"$\displaystyle V=\pi\int_0^{\sqrt2}\mathrm{PH}^2\,ds=\pi\int_0^1\frac{(x-x^2)^2}2\cdot\frac{1+2x}{\sqrt2}\,dx=\frac\pi{2\sqrt2}\int_0^1(x^2-3x^4+2x^5)\,dx$<br>"
         r"$\displaystyle\qquad=\frac\pi{2\sqrt2}\left(\frac13-\frac35+\frac13\right)=\frac\pi{2\sqrt2}\cdot\frac1{15}=\boldsymbol{\frac{\sqrt2}{60}\pi}$",
  "note": r"$(x-x^2)^2(1+2x)=x^2-3x^4+2x^5$ と展開した。座標軸を $45^\circ$ 回転して $y=x$ を新しい横軸にとる方法もあるが，曲線の式が複雑になる。$s$ を $x$ で表して置換する方法が一般的で，このとき $s$ が $x$ の単調関数であることの確認が欠かせない（次の例題）。",
  "ex": r"放物線 $y=x^2$ と直線 $y=2x$ で囲まれた部分を，直線 $y=2x$ のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{16\sqrt5}{75}\pi$"},
 {"lv": 5, "title": r"放物線と弦で囲まれた図形を弦のまわりに回転する（切り口が円環になる部分）",
  "q": r"放物線 $y=x^2$ と直線 $\ell:\ y=x+2$ で囲まれた部分 $D$ を，直線 $\ell$ のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"$\ell$ に垂直な直線 $x+y=c$ で $D$ を切る。前の例題と違い，この直線と $D$ の共通部分が $\ell$ に届かず，放物線上の2点 $\mathrm{A}$，$\mathrm{B}$ を結ぶ線分になる $c$ がある（図の実線）。そこでは回転体の切り口が円環になる。",
  "sol": _f84() + r"$\ell$ の方向の単位ベクトルは $\dfrac1{\sqrt2}(1,\ 1)$ で，$\ell$ に垂直な直線は $m_c:\ x+y=c$ と表せる。$m_c$ 上の点の軸方向の座標は $s=\dfrac c{\sqrt2}$（一定）である。<br>"
         r"$D=\{(x,\ y)\mid x^2\leqq y\leqq x+2\}$ の点 $(x,\ y)$ と $\ell$ の距離は $\dfrac{x+2-y}{\sqrt2}$。$m_c$ 上の点 $(x,\ c-x)$ では $d=\dfrac{2x+2-c}{\sqrt2}$ で，これは $x$ の増加関数。<br>"
         r"$m_c$ と $D$ の共通部分は　$x^2+x-c\leqq0$ かつ $x\geqq\dfrac{c-2}2$　……①<br>"
         r"$h(x)=x^2+x-c$ とし，$h(x)=0$ の2解を $\alpha\leqq\beta$（$c\geqq-\frac14$）とすると $\alpha+\beta=-1$ より $\alpha\leqq-\dfrac12\leqq\beta$。<br>"
         r"(i) $0\leqq c\leqq6$ のとき：$h(-1)=-c\leqq0$，$h\left(\dfrac{c-2}2\right)=\dfrac{c(c-6)}4\leqq0$ より $\alpha\leqq-1\leqq\dfrac{c-2}2\leqq\beta$。① は $\dfrac{c-2}2\leqq x\leqq\beta$ で，端点 $x=\dfrac{c-2}2$ は $\ell$ 上（$d=0$）。切り口は半径 $d(\beta)$ の円。<br>"
         r"(ii) $-\dfrac14\leqq c<0$ のとき：$h(-1)=-c>0$ で $-1<-\dfrac12$ だから $-1<\alpha$，よって $\dfrac{c-2}2<-1<\alpha$。① は $\alpha\leqq x\leqq\beta$ で両端とも放物線上にあり，切り口は外径 $d(\beta)$，内径 $d(\alpha)$ の円環。<br>"
         r"(iii) $c<-\dfrac14$ または $c>6$ のとき，共通部分はない。<br>"
         r"放物線上の点 $(x,\ x^2)$ では $c=x+x^2$，$dc=(1+2x)\,dx$，$d^2=\dfrac{(x+2-x^2)^2}2$。$c$ が $-\dfrac14$ から $6$ まで動くとき $\beta$ は $-\dfrac12$ から $2$ まで，$c$ が $-\dfrac14$ から $0$ まで動くとき $\alpha$ は $-\dfrac12$ から $-1$ まで動く。$ds=\dfrac{dc}{\sqrt2}$ だから<br>"
         r"$\displaystyle V=\frac\pi{\sqrt2}\left\{\int_{-\frac12}^2\frac{(x+2-x^2)^2}2(1+2x)\,dx-\int_{-\frac12}^{-1}\frac{(x+2-x^2)^2}2(1+2x)\,dx\right\}=\frac\pi{2\sqrt2}\int_{-1}^2(2+x-x^2)^2(1+2x)\,dx$<br>"
         r"$x=w+\dfrac12$ とおくと $2+x-x^2=\dfrac94-w^2$，$1+2x=2+2w$ で，$w\left(\dfrac94-w^2\right)^2$ は奇関数だから<br>"
         r"$\displaystyle\int_{-1}^2(2+x-x^2)^2(1+2x)\,dx=\int_{-\frac32}^{\frac32}\left(\frac94-w^2\right)^2(2+2w)\,dw=4\int_0^{\frac32}\left(\frac{81}{16}-\frac92w^2+w^4\right)dw$<br>"
         r"$\displaystyle\qquad=4\left(\frac{243}{32}-\frac{81}{16}+\frac{243}{160}\right)=4\cdot\frac{81}{20}=\frac{81}5$<br>"
         r"よって　$V=\dfrac\pi{2\sqrt2}\cdot\dfrac{81}5=\boldsymbol{\dfrac{81\sqrt2}{20}\pi}$",
  "note": r"結果として，$s$ が $x$ の単調関数でなくても，$\displaystyle\pi\int d^2\frac{ds}{dx}\,dx$ を放物線の弧全体で積分すればよいことになった（$\dfrac{ds}{dx}<0$ の部分が，円環の穴の分を自動的に引いている）。ただし答案では，このように切り口が円環になることを説明する必要がある。穴を無視して (i) の式を $-\dfrac14\leqq c\leqq6$ 全体で使うと誤りになる。<br>"
          r"検算：$D$ の面積は $\dfrac{3^3}6=\dfrac92$，$D$ の重心と $\ell$ の距離は $\dfrac{9\sqrt2}{20}$ で，$2\pi\cdot\dfrac{9\sqrt2}{20}\cdot\dfrac92=\dfrac{81\sqrt2}{20}\pi$（パップス・ギュルダンの定理）。",
  "ex": r"放物線 $y=x^2$ と直線 $y=2x+3$ で囲まれた部分を，直線 $y=2x+3$ のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{512\sqrt5}{75}\pi$"},
 {"lv": 5, "title": r"立方体をその対角線のまわりに回転する",
  "q": r"1辺の長さが $1$ の立方体を，1本の対角線のまわりに1回転してできる立体の体積 $V$ を求めよ。",
  "hint": r"対角線に垂直な平面で立方体を切った切り口 $K$（三角形または六角形）を考える。$K$ は対角線との交点 $\mathrm{M}$ を含むので，回転体の切り口は「$\mathrm{M}$ から最も遠い $K$ の点までの距離」を半径とする円になる。",
  "sol": _f85() + r"立方体を $0\leqq x,\ y,\ z\leqq1$，対角線を $\mathrm{O}(0,\ 0,\ 0)$ と $\mathrm{G}(1,\ 1,\ 1)$ を結ぶ線分とする。平面 $\pi_u:\ x+y+z=u\ (0\leqq u\leqq3)$ は $\mathrm{OG}$ に垂直で，$\mathrm{OG}$ と $\mathrm{M}\left(\dfrac u3,\ \dfrac u3,\ \dfrac u3\right)$ で交わり，$\mathrm{OM}=\dfrac u{\sqrt3}$。<br>"
         r"$\pi_u$ による立方体の切り口 $K_u$ は $\mathrm{M}$ を含む凸多角形である。$K_u$ はつながっていて $\mathrm{M}$ を含むから，$K_u$ を $\mathrm{OG}$ のまわりに回転したものは，$\mathrm{M}$ から $K_u$ の点までの距離の最大値 $R(u)$ を半径とする円板。$K_u$ の辺上の点と $\mathrm{M}$ の距離の2乗は辺上の位置の2次関数（2次の係数は正）だから，最大値は頂点でとる。<br>"
         r"(i) $0\leqq u\leqq1$：$K_u$ は3点 $(u,\ 0,\ 0)$，$(0,\ u,\ 0)$，$(0,\ 0,\ u)$ を頂点とする三角形で　$R(u)^2=\left(\dfrac{2u}3\right)^2+\left(\dfrac u3\right)^2+\left(\dfrac u3\right)^2=\dfrac23u^2$<br>"
         r"(ii) $1\leqq u\leqq2$：$\pi_u$ は立方体の辺と，$(u-1,\ 1,\ 0)$ およびその座標を入れかえた6点で交わり，$K_u$ はこれらを頂点とする六角形。$\mathrm{M}$ の座標はすべて等しいので6頂点は $\mathrm{M}$ から等距離で<br>"
         r"$R(u)^2=\left(\dfrac{2u}3-1\right)^2+\left(1-\dfrac u3\right)^2+\left(\dfrac u3\right)^2=\dfrac23u^2-2u+2$<br>"
         r"(iii) $2\leqq u\leqq3$：立方体の中心に関する対称性から $R(u)=R(3-u)$。<br>"
         r"$s=\mathrm{OM}=\dfrac u{\sqrt3}$ とすると $ds=\dfrac{du}{\sqrt3}$ だから<br>"
         r"$\displaystyle V=\pi\int_0^{\sqrt3}R^2\,ds=\frac\pi{\sqrt3}\left\{2\int_0^1\frac23u^2\,du+\int_1^2\left(\frac23u^2-2u+2\right)du\right\}=\frac\pi{\sqrt3}\left(\frac49+\frac59\right)=\boldsymbol{\frac{\sqrt3}3\pi}$",
  "note": r"$\displaystyle\int_1^2\left(\frac23u^2-2u+2\right)du=\frac{14}9-3+2=\frac59$。この立体は両端が円錐（$R$ が $u$ の1次式），中央部は $R^2$ が $u$ の2次式となる回転一葉双曲面で囲まれている。中央のくびれの半径は $R\left(\dfrac32\right)=\dfrac1{\sqrt2}$ で，対角線と，それとねじれの位置にある辺との距離に等しい。",
  "ex": r"座標空間において，$xy$ 平面上の正方形 $\mathrm{OABC}$（$\mathrm{O}(0,\ 0,\ 0)$，$\mathrm{A}(1,\ 0,\ 0)$，$\mathrm{B}(1,\ 1,\ 0)$，$\mathrm{C}(0,\ 1,\ 0)$）を，直線 $x=y=z$ のまわりに1回転してできる立体の体積を求めよ。",
  "exa": r"$\dfrac{\sqrt3}9\pi$"},
 {"lv": 5, "title": r"3つの円柱の共通部分",
  "q": r"座標空間において，3つの円柱 $x^2+y^2\leqq1$，$y^2+z^2\leqq1$，$z^2+x^2\leqq1$ の共通部分の体積 $V$ を求めよ。",
  "hint": r"平面 $z=t$ で切ると，後の2つの条件は $|x|\leqq\sqrt{1-t^2}$，$|y|\leqq\sqrt{1-t^2}$（正方形），最初の条件は単位円板。正方形の頂点が円の外に出るかどうかで場合を分ける。円と正方形の辺の交点が $(a,\ t)$ になることに注目すると，角を $\alpha\ (t=\sin\alpha)$ で表せる。",
  "sol": _f86() + r"対称性から $z\geqq0$ の部分の2倍を考える。$0\leqq t\leqq1$ とし，$a=\sqrt{1-t^2}$ とおくと，平面 $z=t$ による切り口 $K_t$ は　$x^2+y^2\leqq1$，$|x|\leqq a$，$|y|\leqq a$<br>"
         r"(i) $\dfrac1{\sqrt2}\leqq t\leqq1$ のとき：$a\leqq\dfrac1{\sqrt2}$ で正方形の頂点 $(\pm a,\ \pm a)$ は円の内部にあるから，$K_t$ は正方形で面積 $A(t)=4a^2=4(1-t^2)$。<br>"
         r"(ii) $0\leqq t\leqq\dfrac1{\sqrt2}$ のとき：$a\geqq\dfrac1{\sqrt2}\geqq t$。円 $x^2+y^2=1$ と直線 $x=a$ は $a^2+t^2=1$ より点 $(a,\ \pm t)$ で交わる。$t=\sin\alpha$，$a=\cos\alpha\ \left(0\leqq\alpha\leqq\dfrac\pi4\right)$ とおく。<br>"
         r"$K_t$ は $x$ 軸，$y$ 軸，直線 $y=\pm x$ に関して対称だから，$0\leqq y\leqq x$ の部分の8倍。その部分は，三角形（頂点 $(0,\ 0)$，$(a,\ 0)$，$(a,\ t)$，面積 $\dfrac{at}2$）と，中心角 $\dfrac\pi4-\alpha$ の扇形（面積 $\dfrac12\left(\dfrac\pi4-\alpha\right)$）を合わせたものなので<br>"
         r"$A(t)=8\left\{\dfrac{at}2+\dfrac12\left(\dfrac\pi4-\alpha\right)\right\}=4at+\pi-4\alpha$<br>"
         r"$t=\sin\alpha$ と置換すると（$dt=\cos\alpha\,d\alpha$）<br>"
         r"$\displaystyle\int_0^{\frac1{\sqrt2}}A(t)\,dt=\int_0^{\frac\pi4}(4\sin\alpha\cos\alpha+\pi-4\alpha)\cos\alpha\,d\alpha=\Big[-\frac43\cos^3\alpha\Big]_0^{\frac\pi4}+\pi\Big[\sin\alpha\Big]_0^{\frac\pi4}-4\Big[\alpha\sin\alpha+\cos\alpha\Big]_0^{\frac\pi4}$<br>"
         r"$\displaystyle\qquad=\frac43\left(1-\frac1{2\sqrt2}\right)+\frac\pi{\sqrt2}-4\left(\frac\pi{4\sqrt2}+\frac1{\sqrt2}-1\right)=\frac{16}3-\frac{7\sqrt2}3$<br>"
         r"$\displaystyle\int_{\frac1{\sqrt2}}^14(1-t^2)\,dt=4\Big[t-\frac{t^3}3\Big]_{\frac1{\sqrt2}}^1=4\left(\frac23-\frac5{6\sqrt2}\right)=\frac83-\frac{5\sqrt2}3$<br>"
         r"よって　$V=2\left(\dfrac{16}3-\dfrac{7\sqrt2}3+\dfrac83-\dfrac{5\sqrt2}3\right)=2(8-4\sqrt2)=\boldsymbol{16-8\sqrt2}$",
  "note": r"$\int\alpha\cos\alpha\,d\alpha=\alpha\sin\alpha+\cos\alpha+C$（部分積分）を使った。2つの円柱の共通部分 $\dfrac{16}3\fallingdotseq5.33$，3つの円柱の共通部分 $16-8\sqrt2\fallingdotseq4.69$，球 $\dfrac43\pi\fallingdotseq4.19$ と，条件が増えるほど小さくなっていることも確かめよう。<br>"
          r"別解：座標の入れかえと符号の対称性で48個の合同な部分に分けると，$0\leqq x\leqq y\leqq z$ の部分では条件 $y^2+z^2\leqq1$ だけが効く，という見方もできる。",
  "ex": r"座標空間において，2つの円柱 $y^2+z^2\leqq1$，$z^2+x^2\leqq1$ と，不等式 $|x|+|y|\leqq1$ の表す立体の共通部分の体積を求めよ。",
  "exa": r"$\dfrac{8\pi+16}3-6\sqrt3$"},
 {"lv": 5, "title": r"動く球の通過領域の体積",
  "q": r"$0\leqq t\leqq1$ を満たす実数 $t$ に対し，座標空間の点 $(t,\ 0,\ 0)$ を中心とする半径 $\sqrt{1-t^2}$ の球（内部を含む）を $B_t$ とする。$t$ が $0\leqq t\leqq1$ の範囲を動くとき，$B_t$ が通過する部分 $K$ の体積 $V$ を求めよ。",
  "hint": r"中心はすべて $x$ 軸上にあるので，$K$ は $x$ 軸のまわりの回転体。平面 $x=c$ で切ると，$B_t$ の切り口はすべて中心 $(c,\ 0,\ 0)$ の円板（同心円）だから，$K$ の切り口はその中で最大のもの。$c$ を固定して $t$ を動かし，半径の2乗の最大値を求める。",
  "sol": _f87() + r"平面 $x=c$ と $B_t$ の共通部分は $(c-t)^2+y^2+z^2\leqq1-t^2$，すなわち，中心 $(c,\ 0,\ 0)$，半径の2乗が<br>"
         r"$f(t)=1-t^2-(c-t)^2=-2\left(t-\dfrac c2\right)^2+1-\dfrac{c^2}2$<br>"
         r"の円板である（$f(t)>0$ のとき）。これらは同心の円板だから，$0\leqq t\leqq1$ における $f(t)$ の最大値を $M(c)$ とすると，$K$ の平面 $x=c$ による切り口は，$M(c)>0$ のとき半径 $\sqrt{M(c)}$ の円板，$M(c)\leqq0$ のとき高々1点である。<br>"
         r"(i) $c<0$ のとき：$f(t)$ は $0\leqq t\leqq1$ で減少し $M(c)=f(0)=1-c^2$。$M(c)>0\iff-1<c<0$。<br>"
         r"(ii) $0\leqq c\leqq2$ のとき：$0\leqq\dfrac c2\leqq1$ だから $M(c)=1-\dfrac{c^2}2$。$M(c)>0\iff0\leqq c<\sqrt2$。<br>"
         r"(iii) $c>2$ のとき：$f(t)$ は $0\leqq t\leqq1$ で増加し $M(c)=f(1)=-(c-1)^2<0$。<br>"
         r"よって<br>"
         r"$\displaystyle V=\pi\int_{-1}^0(1-c^2)\,dc+\pi\int_0^{\sqrt2}\left(1-\frac{c^2}2\right)dc=\frac23\pi+\pi\left(\sqrt2-\frac{\sqrt2}3\right)=\boldsymbol{\frac{2(1+\sqrt2)}3\pi}$",
  "note": r"$K$ は，$x\leqq0$ の部分が半球（$B_0$ の半分），$x\geqq0$ の部分が回転楕円体 $\dfrac{x^2}2+y^2+z^2\leqq1$ の一部である。$x=c\ (0\leqq c<\sqrt2)$ で境界をつくるのは $t=\dfrac c2$ の球で，境界の曲面は球面たちの包絡面になっている。「パラメータ $t$ を固定して球を1つずつ考える」のではなく「切り口 $x=c$ を固定して $t$ を動かす」のが通過領域の定石。",
  "ex": r"$-\dfrac12\leqq t\leqq\dfrac12$ を満たす実数 $t$ に対し，点 $(t,\ 0,\ 0)$ を中心とする半径 $\sqrt{1-t^2}$ の球（内部を含む）を考える。$t$ がこの範囲を動くとき，球が通過する部分の体積を求めよ。",
  "exa": r"$\dfrac{2+\sqrt3}2\pi$"},
]})


def _rev2d(inD, p0, e, nrm):
    """平面図形 D（直線の nrm 側にある）を、点 p0 を通り方向 e の直線のまわりに回転した立体の内部判定。"""
    def f(X, Y, Z):
        dx, dy = X - p0[0], Y - p0[1]
        s_ = dx * e[0] + dy * e[1]
        h_ = dx * nrm[0] + dy * nrm[1]
        rho = np.sqrt(h_ * h_ + Z * Z)
        qx, qy = p0[0] + s_ * e[0] + rho * nrm[0], p0[1] + s_ * e[1] + rho * nrm[1]
        return inD(qx, qy)
    return f


def _v8():
    r2 = math.sqrt(2)
    # 2つの円柱
    assert _eq(integrate(4 * (1 - t**2), (t, -1, 1)), Rational(16, 3))
    v = _mc_rev(lambda X, Y, Z: (X * X + Y * Y <= 1) & (X * X + Z * Z <= 1), ((-1, 1), (-1, 1), (-1, 1)), N=600000)
    assert abs(v - 16 / 3) < 0.04
    assert _eq(2 * integrate(4 * sqrt(1 - t**2) * (1 - t), (t, 0, 1)), 2 * pi - Rational(8, 3))
    v = _mc_rev(lambda X, Y, Z: (X * X + Y * Y <= 1) & (np.abs(Y) + np.abs(Z) <= 1), ((-1, 1), (-1, 1), (-1, 1)), N=600000)
    assert abs(v - (2 * math.pi - 8 / 3)) < 0.03
    # 線分の通過領域
    S = _simpson(lambda u: (1 - u**(2 / 3))**1.5, 0, 1, 40000)
    assert abs(S - 3 * math.pi / 32) < 1e-6
    assert _eq(3 * integrate(sin(t)**4 * cos(t)**2, (t, 0, pi / 2)), 3 * pi / 32)
    assert _eq(integrate(sin(2 * t)**2, (t, 0, pi / 2)), pi / 4)
    ths = np.linspace(1e-4, math.pi / 2 - 1e-4, 4001)
    for a0 in (0.05, 0.2, 0.5, 0.8, 0.95):
        gv = np.where(np.cos(ths) >= a0, np.sin(ths) - a0 * np.tan(ths), -1)
        assert abs(gv.max() - (1 - a0**(2 / 3))**1.5) < 1e-5
    rg = np.random.default_rng(8)
    P = rg.uniform(0, 1, (20000, 2))
    hit = 0
    for px, py in P:
        hmin = np.min(px / np.cos(ths) + py / np.sin(ths))
        hit += hmin <= 1
    assert abs(hit / 20000 - 3 * math.pi / 32) < 0.008
    ps = np.linspace(1e-4, 1 - 1e-4, 4001)
    hit = 0
    for px, py in P:
        hit += np.min(px / ps + py / (1 - ps)) <= 1
    assert abs(hit / 20000 - 1 / 6) < 0.008
    assert _eq(integrate((1 - sqrt(x))**2, (x, 0, 1)), Rational(1, 6))
    # 斜めの回転軸 y=x
    assert _eq(expand((x - x**2)**2 * (1 + 2 * x)), x**2 - 3 * x**4 + 2 * x**5)
    V3 = pi / (2 * sqrt(2)) * integrate(x**2 - 3 * x**4 + 2 * x**5, (x, 0, 1))
    assert _eq(V3, sqrt(2) * pi / 60)
    f = _rev2d(lambda qx, qy: (qx * qx <= qy) & (qy <= qx), (0, 0), (1 / r2, 1 / r2), (1 / r2, -1 / r2))
    v = _mc_rev(f, ((-0.1, 1.1), (-0.1, 1.1), (-0.2, 0.2)), N=600000)
    assert abs(v - math.sqrt(2) * math.pi / 60) < 0.003
    V3e = pi * integrate((2 * x - x**2)**2 / 5 * (1 + 4 * x) / sqrt(5), (x, 0, 2))
    assert _eq(V3e, 16 * sqrt(5) * pi / 75)
    r5 = math.sqrt(5)
    f = _rev2d(lambda qx, qy: (qx * qx <= qy) & (qy <= 2 * qx), (0, 0), (1 / r5, 2 / r5), (2 / r5, -1 / r5))
    v = _mc_rev(f, ((-0.3, 2.3), (-0.3, 4.3), (-0.95, 0.95)), N=800000)
    assert abs(v - 16 * r5 * math.pi / 75) / (16 * r5 * math.pi / 75) < 0.03
    # 弦のまわり（円環の部分あり）
    cc = symbols("c", real=True)
    hh = lambda xv: xv**2 + xv - cc
    assert _eq(hh((cc - 2) / 2), cc * (cc - 6) / 4)
    w = symbols("w", real=True)
    assert _eq(expand(2 + x - x**2).subs(x, w + Rational(1, 2)), Rational(9, 4) - w**2)
    I4 = integrate((2 + x - x**2)**2 * (1 + 2 * x), (x, -1, 2))
    assert I4 == Rational(81, 5)
    assert integrate(Rational(81, 16) - Rational(9, 2) * w**2 + w**4, (w, 0, Rational(3, 2))) == Rational(81, 20)
    V4 = pi / (2 * sqrt(2)) * I4
    assert _eq(V4, 81 * sqrt(2) * pi / 20)
    # 断面ごとに円環/円を数値積分（c で）して一致を確認
    def sec_area(c_):
        al_, be_ = (-1 - math.sqrt(1 + 4 * c_)) / 2, (-1 + math.sqrt(1 + 4 * c_)) / 2
        dist = lambda xv: (2 * xv + 2 - c_) / r2
        lo = max(al_, (c_ - 2) / 2)
        if lo > be_:
            return 0.0
        R_, r_ = dist(be_), dist(lo)
        return R_ * R_ - max(r_, 0)**2
    num = math.pi / r2 * _simpson(sec_area, -0.25, 6, 60000)
    assert abs(num - float(V4)) < 1e-4
    f = _rev2d(lambda qx, qy: (qx * qx <= qy) & (qy <= qx + 2), (0, 2), (1 / r2, 1 / r2), (1 / r2, -1 / r2))
    v = _mc_rev(f, ((-2.3, 2.7), (-0.6, 4.6), (-1.65, 1.65)), N=800000)
    assert abs(v - float(V4)) / float(V4) < 0.02
    # 誤答（穴を無視）は大きくなる
    wrong = math.pi / r2 * _simpson(lambda c_: ((2 * ((-1 + math.sqrt(1 + 4 * c_)) / 2) + 2 - c_) / r2)**2, -0.25, 6, 60000)
    assert wrong > float(V4) + 0.01
    # パップスの検算：重心と ℓ の距離
    A_ = integrate(x + 2 - x**2, (x, -1, 2))
    dbar = integrate(integrate((x + 2 - y) / sqrt(2), (y, x**2, x + 2)), (x, -1, 2)) / A_
    assert A_ == Rational(9, 2) and _eq(dbar, 9 * sqrt(2) / 20) and _eq(2 * pi * dbar * A_, V4)
    # 練習：y=x^2 と y=2x+3
    V4e = pi / (5 * sqrt(5)) * integrate((3 + 2 * x - x**2)**2 * (1 + 4 * x), (x, -1, 3))
    assert _eq(V4e, 512 * sqrt(5) * pi / 75)
    f = _rev2d(lambda qx, qy: (qx * qx <= qy) & (qy <= 2 * qx + 3), (0, 3), (1 / r5, 2 / r5), (2 / r5, -1 / r5))
    v = _mc_rev(f, ((-2.7, 3.7), (-0.5, 9.6), (-1.85, 1.85)), N=800000)
    assert abs(v - float(V4e)) / float(V4e) < 0.03
    # 立方体を対角線のまわりに
    def Rcube(u):
        pts = []
        for ax in range(3):
            o1, o2 = [q for q in range(3) if q != ax]
            for b1 in (0, 1):
                for b2 in (0, 1):
                    val = u - b1 - b2
                    if 0 <= val <= 1:
                        pnt = [0, 0, 0]; pnt[ax] = val; pnt[o1] = b1; pnt[o2] = b2
                        pts.append(pnt)
        m_ = u / 3
        return max(sum((c_ - m_)**2 for c_ in q) for q in pts)
    for u in np.linspace(0, 3, 61):
        R2 = (2 / 3) * u * u if u <= 1 else ((2 / 3) * u * u - 2 * u + 2 if u <= 2 else (2 / 3) * (3 - u)**2)
        assert abs(Rcube(u) - R2) < 1e-12
    V5 = pi / sqrt(3) * (2 * integrate(Rational(2, 3) * x**2, (x, 0, 1)) + integrate(Rational(2, 3) * x**2 - 2 * x + 2, (x, 1, 2)))
    assert _eq(V5, sqrt(3) * pi / 3)
    num = math.pi / math.sqrt(3) * _simpson(Rcube, 0, 3, 6000)
    assert abs(num - math.sqrt(3) * math.pi / 3) < 1e-6
    # モンテカルロ：立方体の点を一様にとり回転した像…ではなく、空間の点が回転体に入るかを R(u) で判定
    rg = np.random.default_rng(5)
    N = 400000
    Q = rg.uniform(-0.6, 1.6, (N, 3))
    u_ = Q.sum(axis=1)
    rho2 = ((Q - (u_ / 3)[:, None])**2).sum(axis=1)
    R2v = np.where(u_ <= 1, 2 / 3 * u_**2, np.where(u_ <= 2, 2 / 3 * u_**2 - 2 * u_ + 2, 2 / 3 * (3 - u_)**2))
    inside = (u_ >= 0) & (u_ <= 3) & (rho2 <= R2v)
    assert abs(2.2**3 * inside.mean() - math.sqrt(3) * math.pi / 3) < 0.03
    # 練習：正方形（切り口は線分 → 円環）
    def sq_ring(u):
        lo, hi = max(0, u - 1), min(1, u)
        xs = np.linspace(lo, hi, 2001)
        d2 = (xs - u / 3)**2 + (u - xs - u / 3)**2 + (u / 3)**2
        return d2.max() - d2.min()
    for u in np.linspace(0.01, 1.99, 50):
        ex_ = u * u / 2 if u <= 1 else (u - 2)**2 / 2
        assert abs(sq_ring(u) - ex_) < 1e-6
    assert _eq(pi / sqrt(3) * (integrate(x**2 / 2, (x, 0, 1)) + integrate((x - 2)**2 / 2, (x, 1, 2))), sqrt(3) * pi / 9)
    # 3つの円柱
    al_ = symbols("alpha", real=True)
    I1 = integrate((4 * sin(al_) * cos(al_) + pi - 4 * al_) * cos(al_), (al_, 0, pi / 4))
    assert _eq(I1, Rational(16, 3) - 7 * sqrt(2) / 3)
    I2 = integrate(4 * (1 - t**2), (t, 1 / sqrt(2), 1))
    assert _eq(I2, Rational(8, 3) - 5 * sqrt(2) / 3)
    assert _eq(2 * (I1 + I2), 16 - 8 * sqrt(2))
    def A6(tv):
        av = math.sqrt(1 - tv * tv)
        if tv >= 1 / r2:
            return 4 * av * av
        alv = math.asin(tv)
        return 4 * av * tv + math.pi - 4 * alv
    # 切り口の面積を格子で直接数えて確認
    G = np.linspace(-1, 1, 1601)
    XX, YY = np.meshgrid(G, G)
    for tv in (0.1, 0.4, 0.6, 0.8, 0.95):
        av = math.sqrt(1 - tv * tv)
        cnt = np.count_nonzero((XX**2 + YY**2 <= 1) & (np.abs(XX) <= av) & (np.abs(YY) <= av)) * (2 / 1600)**2
        assert abs(cnt - A6(tv)) < 0.01
    assert abs(2 * _simpson(A6, 0, 1, 20000) - (16 - 8 * r2)) < 1e-4
    v = _mc_rev(lambda X, Y, Z: (X * X + Y * Y <= 1) & (Y * Y + Z * Z <= 1) & (Z * Z + X * X <= 1), ((-1, 1), (-1, 1), (-1, 1)), N=800000)
    assert abs(v - (16 - 8 * r2)) < 0.03
    ans_ex = (8 * math.pi + 16) / 3 - 6 * math.sqrt(3)
    v = _mc_rev(lambda X, Y, Z: (Y * Y + Z * Z <= 1) & (Z * Z + X * X <= 1) & (np.abs(X) + np.abs(Y) <= 1), ((-1, 1), (-1, 1), (-1, 1)), N=800000)
    assert abs(v - ans_ex) < 0.03
    aa_ = sqrt(1 - t**2)
    Vex = 2 * (integrate(-4 * aa_**2 + 8 * aa_ - 2, (t, 0, sqrt(3) / 2)) + integrate(4 * aa_**2, (t, sqrt(3) / 2, 1)))
    assert abs(float(Vex) - ans_ex) < 1e-10
    # 球の通過領域
    V7 = pi * integrate(1 - x**2, (x, -1, 0)) + pi * integrate(1 - x**2 / 2, (x, 0, sqrt(2)))
    assert _eq(V7, 2 * (1 + sqrt(2)) * pi / 3)
    tg = np.linspace(0, 1, 401)
    def ball(X, Y, Z):
        r2_ = Y * Y + Z * Z
        best = np.full(X.shape, np.inf)
        for tv in tg:
            best = np.minimum(best, (X - tv)**2 + r2_ - (1 - tv * tv))
        return best <= 0
    v = _mc_rev(ball, ((-1, 1.5), (-1, 1), (-1, 1)), N=200000)
    assert abs(v - float(V7)) < 0.06
    V7e = 2 * pi * (integrate(1 - x**2 / 2, (x, 0, 1)) + integrate(Rational(1, 2) + x - x**2, (x, 1, (1 + sqrt(3)) / 2)))
    assert _eq(V7e, (2 + sqrt(3)) * pi / 2)
    tg = np.linspace(-0.5, 0.5, 401)
    v = _mc_rev(ball, ((-1.4, 1.4), (-1, 1), (-1, 1)), N=200000)
    assert abs(v - float(V7e)) < 0.06


CH = {"no": 26, "sections": SEC}


def verify():
    _v1()
    _v2()
    _v3()
    _v4()
    _v5()
    _v6()
    _v7()
    _v8()
    # 検討の主張：葉線の漸近線 x+y+1=0、立方体の中央のくびれの半径 = 対角線とねじれの位置にある辺の距離
    uu = symbols("u", real=True)
    X_, Y_ = 3 * uu / (1 + uu**3), 3 * uu**2 / (1 + uu**3)
    assert _eq(limit(X_ + Y_ + 1, uu, -1), 0)
    assert _eq(Rational(2, 3) * Rational(9, 4) - 3 + 2, Rational(1, 2))
    dvec = np.array([1, 1, 1]) / math.sqrt(3)
    cr = np.cross(np.array([1, 1, 1]), np.array([0, 1, 0]))
    assert abs(abs(np.dot(np.array([1, 0, 0]), cr)) / np.linalg.norm(cr) - 1 / math.sqrt(2)) < 1e-12
    # 題数・難易度の配分
    import re
    items = [it for sec in SEC for it in sec["items"]]
    cnt = {lv: sum(1 for it in items if it["lv"] == lv) for lv in range(1, 6)}
    assert 4 <= len(SEC) <= 9
    assert 42 <= len(items) <= 48, len(items)
    assert cnt[5] >= 5 and cnt[1] >= 7 and cnt[2] >= 9 and cnt[3] >= 9 and cnt[4] >= 6, cnt
    for sec in SEC:
        lvs = [it["lv"] for it in sec["items"]]
        assert lvs == sorted(lvs), sec["title"]
    # 表記の点検：$ の対応、$$ なし、数式中に日本語なし、数式の外に半角の不等号なし
    cjk = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff\uff01-\uff5e]")
    for sec in SEC:
        for it in [sec] + sec["items"]:
            for key in ("title", "base", "q", "hint", "sol", "note", "ex", "exa"):
                txt_ = it.get(key)
                if not txt_:
                    continue
                txt_ = re.sub(r"<svg.*?</svg>", "", txt_, flags=re.S)
                assert "$$" not in txt_ and txt_.count("$") % 2 == 0, (it.get("title"), key)
                for m_ in re.findall(r"\$([^$]*)\$", txt_):
                    assert not cjk.search(m_), (it.get("title"), key, m_)
                rest = re.sub(r"\$[^$]*\$", "", txt_)
                rest = re.sub(r"</?[a-z]+[^<>]*>", "", rest)
                assert "<" not in rest and ">" not in rest, (it.get("title"), key)
