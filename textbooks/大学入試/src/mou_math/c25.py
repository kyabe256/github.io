r"""第25章 積分法（数学III）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。
面積・体積・曲線の長さなどの応用は第26章で扱う。図の座標はすべて Python で計算する。"""
import math
import random
from fractions import Fraction as Fr
from sympy import (symbols, Rational, sqrt, exp, log, sin, cos, tan, pi, E, integrate, diff,
                   simplify, expand, factorial, binomial, lambdify, N, Abs, Poly, div, S)
import mpmath as mp

mp.mp.dps = 30
x, t, u = symbols("x t u", real=True)
SEC = []

# ---------------------------------------------------------------- 検算の道具


def _mpf(v):
    return mp.mpf(str(N(v, 40)))


def _D(F, f, pts):
    """F'(x)=f(x) を多数の点で数値的に確認する（原始関数の検算）。"""
    d = lambdify(x, diff(F, x) - f, "mpmath")
    for p in pts:
        val = d(mp.mpf(p))
        assert abs(val) < mp.mpf("1e-18"), (F, f, p, val)


def _Q(f, a, b, val, brk=(), sym=True):
    """∫_a^b f dx = val を数値積分（と、可能なら sympy の integrate）で確認する。"""
    g = lambdify(x, f, "mpmath")
    q = mp.quad(g, [_mpf(a)] + [_mpf(c) for c in brk] + [_mpf(b)])
    assert abs(q - _mpf(val)) < mp.mpf("1e-15"), (f, a, b, q, N(val))
    if sym:
        I = integrate(f, (x, a, b))
        assert abs(N(I - val, 30)) < 1e-20, (f, I, val)


# ---------------------------------------------------------------- 図の道具
C1, C2, CG, CF = "#16367a", "#d9701e", "#888888", "#c9daf3"


class _G:
    """数学座標で描いて SVG 文字列にする小さな道具。"""

    def __init__(s, W, H, xr, yr, m=12):
        s.W, s.H, s.m = W, H, m
        s.x0, s.x1 = xr
        s.y0, s.y1 = yr
        s.sx = (W - 2 * m) / (s.x1 - s.x0)
        s.sy = (H - 2 * m) / (s.y1 - s.y0)
        s.o = []

    def X(s, v):
        return round(s.m + (v - s.x0) * s.sx, 1)

    def Y(s, v):
        return round(s.m + (s.y1 - v) * s.sy, 1)

    def axes(s, xl="x", yl="y", o="O"):
        X0, Y0 = s.X(0), s.Y(0)
        xa, xb, ya, yb = s.X(s.x0), s.X(s.x1), s.Y(s.y0), s.Y(s.y1)
        s.o.append(f'<line x1="{xa}" y1="{Y0}" x2="{xb}" y2="{Y0}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{xb + 3},{Y0} {xb - 3},{Y0 - 2.6} {xb - 3},{Y0 + 2.6}" fill="#333"/>')
        s.o.append(f'<line x1="{X0}" y1="{ya}" x2="{X0}" y2="{yb}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{X0},{yb - 3} {X0 - 2.6},{yb + 3} {X0 + 2.6},{yb + 3}" fill="#333"/>')
        s.text(xb - 1, Y0 - 4, xl, anchor="end", it=True, raw=True)
        s.text(X0 + 5, yb + 7, yl, it=True, raw=True)
        if o:
            s.text(X0 - 3, Y0 + 10, o, anchor="end", it=True, raw=True, size=10)

    def text(s, px, py, txt, anchor="start", it=False, raw=False, size=11, col="#222"):
        if not raw:
            px, py = s.X(px), s.Y(py)
        st = ' font-style="italic" font-family="serif"' if it else ' font-family="serif"'
        s.o.append(f'<text x="{px}" y="{py}" text-anchor="{anchor}"{st} font-size="{size}" fill="{col}">{txt}</text>')

    def curve(s, f, a, b, col=C1, w=1.4, n=200):
        pts = [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
        s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}" points="'
                   + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts) + '"/>')

    def poly(s, pts, fill="none", col=C1, w=1.0, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<polygon points="' + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts)
                   + f'" fill="{fill}" stroke="{col}" stroke-width="{w}"{d}/>')

    def circle(s, cx, cy, r, col="#333", w=1.0):
        s.o.append(f'<ellipse cx="{s.X(cx)}" cy="{s.Y(cy)}" rx="{round(r * s.sx, 1)}" ry="{round(r * s.sy, 1)}" '
                   f'fill="none" stroke="{col}" stroke-width="{w}"/>')

    def seg(s, p, q, col=CG, w=0.8, dash="3,2"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<line x1="{s.X(p[0])}" y1="{s.Y(p[1])}" x2="{s.X(q[0])}" y2="{s.Y(q[1])}" stroke="{col}" stroke-width="{w}"{d}/>')

    def pt(s, px, py, col="#222", r=1.8):
        s.o.append(f'<circle cx="{s.X(px)}" cy="{s.Y(py)}" r="{r}" fill="{col}"/>')

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(s.o) + '</svg>')


# ---------------------------------------------------------------- 節1
SEC.append({"title": r"不定積分の基本",
"base": r"""・以下、$C$ は積分定数を表す。$\displaystyle\int x^{\alpha}dx=\dfrac{x^{\alpha+1}}{\alpha+1}+C$（$\alpha\neq-1$），$\displaystyle\int\dfrac{dx}{x}=\log|x|+C$<br>
・$\displaystyle\int e^xdx=e^x+C$，$\displaystyle\int a^xdx=\dfrac{a^x}{\log a}+C$（$a>0,\ a\neq1$）<br>
・$\displaystyle\int\sin x\,dx=-\cos x+C$，$\displaystyle\int\cos x\,dx=\sin x+C$，$\displaystyle\int\dfrac{dx}{\cos^2x}=\tan x+C$，$\displaystyle\int\dfrac{dx}{\sin^2x}=-\dfrac1{\tan x}+C$<br>
・$F'(x)=f(x)$ のとき　$\displaystyle\int f(ax+b)\,dx=\dfrac1aF(ax+b)+C$（$a\neq0$），$\displaystyle\int f(g(x))g'(x)\,dx=F(g(x))+C$，$\displaystyle\int\dfrac{g'(x)}{g(x)}dx=\log|g(x)|+C$""",
"items": [
 {"lv": 1, "title": r"基本的な関数の不定積分",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{(\sqrt x-1)^2}{x}\,dx$　　(2) $\displaystyle\int\left(3e^x-2^{x+1}\right)dx$",
  "hint": r"(1) 分子を展開して $x^{\alpha}$ の和に分ける。根号は $\sqrt x=x^{\frac12}$ と指数で表してから公式を使う。(2) $2^{x+1}=2\cdot2^x$ として $a^x$ の公式を使う。",
  "sol": r"(1) $x>0$ であり、$\dfrac{(\sqrt x-1)^2}{x}=\dfrac{x-2\sqrt x+1}{x}=1-2x^{-\frac12}+\dfrac1x$ であるから<br>"
         r"$\displaystyle\int\dfrac{(\sqrt x-1)^2}{x}dx=x-2\cdot\dfrac{x^{\frac12}}{\frac12}+\log x+C=\boldsymbol{x-4\sqrt x+\log x+C}$<br>"
         r"(2) $\displaystyle\int\left(3e^x-2\cdot2^x\right)dx=3e^x-\dfrac{2\cdot2^x}{\log2}+C=\boldsymbol{3e^x-\dfrac{2^{x+1}}{\log2}+C}$",
  "note": r"(1) は定義域が $x>0$ なので $\log|x|$ を $\log x$ と書いてよい。答えは微分してもとに戻ることで確かめられる：$\left(x-4\sqrt x+\log x\right)'=1-\dfrac2{\sqrt x}+\dfrac1x$。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{(x+1)^2}{x\sqrt x}\,dx$　　(2) $\displaystyle\int\left(2e^x+3^{x-1}\right)dx$",
  "exa": r"(1) $\dfrac23x\sqrt x+4\sqrt x-\dfrac2{\sqrt x}+C$　(2) $2e^x+\dfrac{3^{x-1}}{\log3}+C$"},
 {"lv": 1, "title": r"三角関数の不定積分（式の変形）",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\tan^2x\,dx$　　(2) $\displaystyle\int\dfrac{\cos2x}{\cos x-\sin x}\,dx$",
  "hint": r"そのままでは公式が使えないので、三角関数の公式で式を変形する。(1) は $1+\tan^2x=\dfrac1{\cos^2x}$、(2) は $\cos2x=\cos^2x-\sin^2x$ を因数分解する。",
  "sol": r"(1) $\tan^2x=\dfrac1{\cos^2x}-1$ より　$\displaystyle\int\tan^2x\,dx=\boldsymbol{\tan x-x+C}$<br>"
         r"(2) $\cos2x=\cos^2x-\sin^2x=(\cos x-\sin x)(\cos x+\sin x)$ より<br>"
         r"$\displaystyle\int\dfrac{\cos2x}{\cos x-\sin x}dx=\int(\cos x+\sin x)\,dx=\boldsymbol{\sin x-\cos x+C}$",
  "note": r"$\sin^2x$，$\cos^2x$ そのものは2倍角の公式で次数を下げて積分する（3節）。$\tan^2x$ は「$\dfrac1{\cos^2x}$ をつくる」と覚えておく。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{dx}{\tan^2x}$　　(2) $\displaystyle\int\dfrac{\sin^2x}{1+\cos x}\,dx$",
  "exa": r"(1) $-\dfrac1{\tan x}-x+C$　(2) $x-\sin x+C$"},
 {"lv": 1, "title": r"$f(ax+b)$ の不定積分",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int(2x+1)^5dx$　　(2) $\displaystyle\int\sqrt{4-3x}\,dx$　　(3) $\displaystyle\int\dfrac{dx}{3x+2}$　　(4) $\displaystyle\int\sin\left(2x-\dfrac\pi3\right)dx$",
  "hint": r"$F'(x)=f(x)$ なら $\{F(ax+b)\}'=aF'(ax+b)$ なので、$\displaystyle\int f(ax+b)\,dx=\dfrac1aF(ax+b)+C$。$x$ の係数 $a$ で割ることを忘れない。",
  "sol": r"(1) $\dfrac12\cdot\dfrac{(2x+1)^6}{6}+C=\boldsymbol{\dfrac{(2x+1)^6}{12}+C}$<br>"
         r"(2) $\sqrt{4-3x}=(4-3x)^{\frac12}$ より　$-\dfrac13\cdot\dfrac{(4-3x)^{\frac32}}{\frac32}+C=\boldsymbol{-\dfrac29(4-3x)\sqrt{4-3x}+C}$<br>"
         r"(3) $\boldsymbol{\dfrac13\log|3x+2|+C}$<br>"
         r"(4) $\boldsymbol{-\dfrac12\cos\left(2x-\dfrac\pi3\right)+C}$",
  "note": r"(2) は $x$ の係数が負であることに注意。微分して確かめると $\left\{-\dfrac29(4-3x)^{\frac32}\right\}'=-\dfrac29\cdot\dfrac32(4-3x)^{\frac12}\cdot(-3)=\sqrt{4-3x}$。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int(1-3x)^4dx$　　(2) $\displaystyle\int\dfrac{dx}{(2x+3)^2}$　　(3) $\displaystyle\int e^{3x+2}dx$　　(4) $\displaystyle\int\cos\left(\dfrac\pi6-x\right)dx$",
  "exa": r"(1) $-\dfrac{(1-3x)^5}{15}+C$　(2) $-\dfrac1{2(2x+3)}+C$　(3) $\dfrac13e^{3x+2}+C$　(4) $-\sin\left(\dfrac\pi6-x\right)+C$"},
 {"lv": 2, "title": r"$\dfrac{g'(x)}{g(x)}$ 型と $f(g(x))g'(x)$ 型の不定積分",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{2x+1}{x^2+x+3}\,dx$　　(2) $\displaystyle\int\tan x\,dx$　　(3) $\displaystyle\int xe^{-x^2}dx$　　(4) $\displaystyle\int\dfrac{(\log x)^2}{x}\,dx$",
  "hint": r"被積分関数の中に、ある関数 $g(x)$ とその導関数 $g'(x)$ の組を探す。(1)(2) は分子が分母の導関数（の定数倍）、(3)(4) は $-x^2$，$\log x$ の導関数が掛かっている。",
  "sol": r"(1) $(x^2+x+3)'=2x+1$，$x^2+x+3=\left(x+\dfrac12\right)^2+\dfrac{11}4>0$ より　$\boldsymbol{\log(x^2+x+3)+C}$<br>"
         r"(2) $\tan x=\dfrac{\sin x}{\cos x}=-\dfrac{(\cos x)'}{\cos x}$ より　$\boldsymbol{-\log|\cos x|+C}$<br>"
         r"(3) $(-x^2)'=-2x$ より $xe^{-x^2}=-\dfrac12e^{-x^2}\cdot(-x^2)'$ だから　$\boldsymbol{-\dfrac12e^{-x^2}+C}$<br>"
         r"(4) $(\log x)'=\dfrac1x$ より $\dfrac{(\log x)^2}{x}=(\log x)^2(\log x)'$ だから　$\boldsymbol{\dfrac13(\log x)^3+C}$",
  "note": r"(3)(4) は $-x^2=u$，$\log x=u$ とおく置換積分（次節）と同じことである。慣れたら置き換えずに「$g(x)$ のかたまりのまま」積分してよい。(2) と同様に $\displaystyle\int\dfrac{dx}{\tan x}=\log|\sin x|+C$。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{e^x-e^{-x}}{e^x+e^{-x}}\,dx$　　(2) $\displaystyle\int\dfrac{dx}{x\log x}$　　(3) $\displaystyle\int\sin x\cos^4x\,dx$　　(4) $\displaystyle\int\dfrac{x}{\sqrt{x^2+1}}\,dx$",
  "exa": r"(1) $\log(e^x+e^{-x})+C$　(2) $\log|\log x|+C$　(3) $-\dfrac15\cos^5x+C$　(4) $\sqrt{x^2+1}+C$"},
]})


def _v1():
    P = [0.3, 0.7, 1.3, 2.1, 3.7]
    _D(x - 4*sqrt(x) + log(x), (sqrt(x)-1)**2/x, P)
    assert simplify(expand((sqrt(x)-1)**2/x) - (1 - 2/sqrt(x) + 1/x)) == 0
    _D(3*exp(x) - 2**(x+1)/log(2), 3*exp(x) - 2**(x+1), P)
    _D(Rational(2, 3)*x*sqrt(x) + 4*sqrt(x) - 2/sqrt(x), (x+1)**2/(x*sqrt(x)), P)
    _D(2*exp(x) + 3**(x-1)/log(3), 2*exp(x) + 3**(x-1), P)
    # 三角関数
    _D(tan(x) - x, tan(x)**2, [0.3, 0.7, 1.2, -0.5, 2.5])
    _D(sin(x) - cos(x), cos(2*x)/(cos(x)-sin(x)), [0.3, 1.2, 2.0, -0.5])
    assert simplify(cos(2*x) - (cos(x)-sin(x))*(cos(x)+sin(x))) == 0
    _D(-1/tan(x) - x, 1/tan(x)**2, [0.3, 0.7, 1.2, 2.0])
    _D(x - sin(x), sin(x)**2/(1+cos(x)), [0.3, 0.7, 1.2, 2.0])
    # f(ax+b)
    _D((2*x+1)**6/12, (2*x+1)**5, P)
    _D(-Rational(2, 9)*(4-3*x)*sqrt(4-3*x), sqrt(4-3*x), [0.3, 0.7, 1.0, -1.5])
    _D(log(3*x+2)/3, 1/(3*x+2), P)
    _D(-cos(2*x - pi/3)/2, sin(2*x - pi/3), P)
    _D(-(1-3*x)**5/15, (1-3*x)**4, P)
    _D(-1/(2*(2*x+3)), 1/(2*x+3)**2, P)
    _D(exp(3*x+2)/3, exp(3*x+2), P)
    _D(-sin(pi/6 - x), cos(pi/6 - x), P)
    # g'/g, f(g)g'
    _D(log(x**2+x+3), (2*x+1)/(x**2+x+3), P + [-2.5])
    _D(-log(cos(x)), tan(x), [0.3, 0.7, 1.2, -0.9])
    _D(-log(-cos(x)), tan(x), [1.8, 2.5, 3.0])
    _D(-exp(-x**2)/2, x*exp(-x**2), P)
    _D(log(x)**3/3, log(x)**2/x, P)
    _D(log(sin(x)), 1/tan(x), [0.3, 1.2, 2.5])
    _D(log(exp(x)+exp(-x)), (exp(x)-exp(-x))/(exp(x)+exp(-x)), P + [-1.2])
    _D(log(log(x)), 1/(x*log(x)), [1.3, 2.1, 3.7])
    _D(log(-log(x)), 1/(x*log(x)), [0.3, 0.7])
    _D(-cos(x)**5/5, sin(x)*cos(x)**4, P)
    _D(sqrt(x**2+1), x/sqrt(x**2+1), P + [-1.1])


# ---------------------------------------------------------------- 節2
SEC.append({"title": r"置換積分法と部分積分法",
"base": r"""・置換積分法：$x=g(t)$ とおくと $\displaystyle\int f(x)\,dx=\int f(g(t))g'(t)\,dt$。$g(x)=t$ とおくと $\displaystyle\int f(g(x))g'(x)\,dx=\int f(t)\,dt$<br>
・部分積分法：$\displaystyle\int f(x)g'(x)\,dx=f(x)g(x)-\int f'(x)g(x)\,dx$<br>
・部分積分では、微分すると簡単になるもの（$x^n$，$\log x$）を $f(x)$ に、積分しやすいもの（$e^x$，$\sin x$，$\cos x$）を $g'(x)$ に選ぶ""",
"items": [
 {"lv": 1, "title": r"置換積分法（1次式やその根号を1文字でおく）",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x\sqrt{x+1}\,dx$　　(2) $\displaystyle\int\dfrac{x}{(x+2)^3}\,dx$",
  "hint": r"扱いにくいかたまり（$\sqrt{x+1}$，$x+2$）を $t$ とおき、$x$ と $dx$ をすべて $t$ で表す。最後に $t$ を $x$ に戻す。",
  "sol": r"(1) $\sqrt{x+1}=t$ とおくと $x=t^2-1$，$dx=2t\,dt$。<br>"
         r"$\displaystyle\int x\sqrt{x+1}\,dx=\int(t^2-1)\cdot t\cdot2t\,dt=\int(2t^4-2t^2)\,dt=\dfrac25t^5-\dfrac23t^3+C=\dfrac2{15}t^3(3t^2-5)+C$<br>"
         r"$t^2=x+1$ を代入して　$\boldsymbol{\dfrac2{15}(3x-2)(x+1)\sqrt{x+1}+C}$<br>"
         r"(2) $x+2=t$ とおくと $x=t-2$，$dx=dt$。<br>"
         r"$\displaystyle\int\dfrac{t-2}{t^3}dt=\int\left(t^{-2}-2t^{-3}\right)dt=-\dfrac1t+\dfrac1{t^2}+C=\dfrac{1-t}{t^2}+C=\boldsymbol{-\dfrac{x+1}{(x+2)^2}+C}$",
  "note": r"(1) は $x+1=u$ とおいて $\displaystyle\int(u-1)\sqrt u\,du=\int\left(u^{\frac32}-u^{\frac12}\right)du$ としてもよい。根号ごと $t$ とおくと分数の指数が出てこないので、計算が楽になることが多い。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x\sqrt{2x-1}\,dx$　　(2) $\displaystyle\int\dfrac{x^2}{(x+1)^3}\,dx$",
  "exa": r"(1) $\dfrac1{15}(3x+1)(2x-1)\sqrt{2x-1}+C$　(2) $\log|x+1|+\dfrac2{x+1}-\dfrac1{2(x+1)^2}+C$"},
 {"lv": 1, "title": r"部分積分法の基本",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x\cos x\,dx$　　(2) $\displaystyle\int\log x\,dx$　　(3) $\displaystyle\int xe^{2x}dx$",
  "hint": r"$\displaystyle\int f(x)g'(x)\,dx=f(x)g(x)-\int f'(x)g(x)\,dx$。微分すると簡単になる $x$ や $\log x$ を $f(x)$ に、積分しやすい $\cos x$，$e^{2x}$ を $g'(x)$ に選ぶ。(2) は $\log x=(x)'\log x$ と見る。",
  "sol": r"(1) $\displaystyle\int x(\sin x)'dx=x\sin x-\int\sin x\,dx=\boldsymbol{x\sin x+\cos x+C}$<br>"
         r"(2) $\displaystyle\int(x)'\log x\,dx=x\log x-\int x\cdot\dfrac1x\,dx=\boldsymbol{x\log x-x+C}$<br>"
         r"(3) $\displaystyle\int x\left(\dfrac12e^{2x}\right)'dx=\dfrac12xe^{2x}-\int\dfrac12e^{2x}dx=\boldsymbol{\dfrac14(2x-1)e^{2x}+C}$",
  "note": r"$f$ と $g'$ の選び方を逆にすると（例えば (1) で $\cos x$ を微分する側にすると）、$\displaystyle\int\dfrac{x^2}2\sin x\,dx$ が現れてかえって複雑になる。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x\sin2x\,dx$　　(2) $\displaystyle\int x\log x\,dx$　　(3) $\displaystyle\int(x+1)e^{-x}dx$",
  "exa": r"(1) $-\dfrac12x\cos2x+\dfrac14\sin2x+C$　(2) $\dfrac{x^2}2\log x-\dfrac{x^2}4+C$　(3) $-(x+2)e^{-x}+C$"},
 {"lv": 2, "title": r"部分積分法をくり返す",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x^2e^{-x}dx$　　(2) $\displaystyle\int(\log x)^2dx$",
  "hint": r"1回の部分積分で $x^2\to2x$（$(\log x)^2\to2\log x$）と次数が1つ下がる。もう1回部分積分すれば、前の例題の基本形に帰着する。",
  "sol": r"(1) $\displaystyle\int x^2(-e^{-x})'dx=-x^2e^{-x}+\int2xe^{-x}dx$。さらに $\displaystyle\int2xe^{-x}dx=-2xe^{-x}+\int2e^{-x}dx=-2xe^{-x}-2e^{-x}+C$ であるから<br>"
         r"$\displaystyle\int x^2e^{-x}dx=\boldsymbol{-(x^2+2x+2)e^{-x}+C}$<br>"
         r"(2) $\displaystyle\int(x)'(\log x)^2dx=x(\log x)^2-\int x\cdot\dfrac{2\log x}{x}dx=x(\log x)^2-2\int\log x\,dx$<br>"
         r"$=x(\log x)^2-2(x\log x-x)+C=\boldsymbol{x(\log x)^2-2x\log x+2x+C}$",
  "note": r"（多項式）$\times e^{ax}$ の不定積分は（同じ次数の多項式）$\times e^{ax}$ の形になる。(1) で答えを $(px^2+qx+r)e^{-x}$ とおき、微分して $x^2e^{-x}$ と係数を比べてもよい（$p=-1$，$q=-2$，$r=-2$）。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int x^2\cos x\,dx$　　(2) $\displaystyle\int x(\log x)^2dx$",
  "exa": r"(1) $x^2\sin x+2x\cos x-2\sin x+C$　(2) $\dfrac{x^2}2(\log x)^2-\dfrac{x^2}2\log x+\dfrac{x^2}4+C$"},
 {"lv": 3, "title": r"同じ形が現れる部分積分（$e^x\sin x$ の積分）",
  "q": r"不定積分 $\displaystyle I=\int e^x\sin x\,dx$，$\displaystyle J=\int e^x\cos x\,dx$ を求めよ。",
  "hint": r"$e^x$ も $\sin x$ も、何回微分・積分しても形が消えない。部分積分を2回行うと元の積分 $I$ が再び現れるので、$I$ についての方程式とみて解く。",
  "sol": r"$e^x=(e^x)'$ として部分積分すると（積分定数は最後にまとめてつける）<br>"
         r"$I=e^x\sin x-\displaystyle\int e^x\cos x\,dx=e^x\sin x-J$　…①，　$J=e^x\cos x+\displaystyle\int e^x\sin x\,dx=e^x\cos x+I$　…②<br>"
         r"②を①に代入すると $I=e^x\sin x-e^x\cos x-I$ となるから<br>"
         r"$I=\boldsymbol{\dfrac12e^x(\sin x-\cos x)+C}$<br>"
         r"①より $J=e^x\sin x-I$ だから　$J=\boldsymbol{\dfrac12e^x(\sin x+\cos x)+C}$",
  "note": r"【別解】$(e^x\sin x)'=e^x(\sin x+\cos x)$，$(e^x\cos x)'=e^x(\cos x-\sin x)$ を辺々引くと $\{e^x(\sin x-\cos x)\}'=2e^x\sin x$、辺々加えると $\{e^x(\sin x+\cos x)\}'=2e^x\cos x$。これからただちに $I,\ J$ が得られる。一般に $\displaystyle\int e^{ax}\sin bx\,dx=\dfrac{e^{ax}(a\sin bx-b\cos bx)}{a^2+b^2}+C$。",
  "ex": r"不定積分 $\displaystyle\int e^{-x}\cos2x\,dx$ を求めよ。",
  "exa": r"$\dfrac15e^{-x}(2\sin2x-\cos2x)+C$"},
]})


def _v2():
    P = [0.3, 0.7, 1.3, 2.1, 3.7]
    _D(Rational(2, 15)*(3*x-2)*(x+1)*sqrt(x+1), x*sqrt(x+1), P + [-0.5])
    tt = symbols("tt", positive=True)
    assert expand(Rational(2, 5)*tt**5 - Rational(2, 3)*tt**3 - Rational(2, 15)*tt**3*(3*tt**2-5)) == 0
    _D(-(x+1)/(x+2)**2, x/(x+2)**3, P + [-1.5, -3.0])
    _D(Rational(1, 15)*(3*x+1)*(2*x-1)*sqrt(2*x-1), x*sqrt(2*x-1), [0.6, 1.3, 2.1, 3.7])
    _D(log(x+1) + 2/(x+1) - 1/(2*(x+1)**2), x**2/(x+1)**3, P)
    _D(x*sin(x) + cos(x), x*cos(x), P)
    _D(x*log(x) - x, log(x), P)
    _D((2*x-1)*exp(2*x)/4, x*exp(2*x), P)
    _D(-x*cos(2*x)/2 + sin(2*x)/4, x*sin(2*x), P)
    _D(x**2*log(x)/2 - x**2/4, x*log(x), P)
    _D(-(x+2)*exp(-x), (x+1)*exp(-x), P)
    _D(-(x**2+2*x+2)*exp(-x), x**2*exp(-x), P)
    _D(x*log(x)**2 - 2*x*log(x) + 2*x, log(x)**2, P)
    _D(x**2*sin(x) + 2*x*cos(x) - 2*sin(x), x**2*cos(x), P)
    _D(x**2*log(x)**2/2 - x**2*log(x)/2 + x**2/4, x*log(x)**2, P)
    _D(exp(x)*(sin(x)-cos(x))/2, exp(x)*sin(x), P)
    _D(exp(x)*(sin(x)+cos(x))/2, exp(x)*cos(x), P)
    a_, b_ = symbols("a_ b_", positive=True)
    assert simplify(diff(exp(a_*x)*(a_*sin(b_*x)-b_*cos(b_*x))/(a_**2+b_**2), x) - exp(a_*x)*sin(b_*x)) == 0
    _D(exp(-x)*(2*sin(2*x)-cos(2*x))/5, exp(-x)*cos(2*x), P)


# ---------------------------------------------------------------- 節3
SEC.append({"title": r"いろいろな関数の不定積分",
"base": r"""・積→和：$\sin\alpha\cos\beta=\dfrac12\{\sin(\alpha+\beta)+\sin(\alpha-\beta)\}$ など。次数下げ：$\sin^2x=\dfrac{1-\cos2x}2$，$\cos^2x=\dfrac{1+\cos2x}2$<br>
・$\sin x$ の奇数乗は $\sin x$ を1つ残して $\cos x=t$、$\cos x$ の奇数乗は $\cos x$ を1つ残して $\sin x=t$ とおく<br>
・分数関数：（分子の次数）≧（分母の次数）なら割り算をして次数を下げ、分母を因数分解して部分分数に分ける<br>
・無理関数：$\sqrt{ax+b}=t$，$x+\sqrt{x^2+A}=t$ などとおく。$\sqrt{a^2-x^2}$ は $x=a\sin\theta$ とおく（次節）""",
"items": [
 {"lv": 1, "title": r"三角関数の積と次数下げ",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\sin3x\cos x\,dx$　　(2) $\displaystyle\int\cos^22x\,dx$",
  "hint": r"三角関数の積や2乗は、そのままでは積分できない。積→和の公式、半角（2倍角）の公式で1次の三角関数の和に直す。",
  "sol": r"(1) $\sin3x\cos x=\dfrac12(\sin4x+\sin2x)$ より<br>"
         r"$\displaystyle\int\sin3x\cos x\,dx=\dfrac12\left(-\dfrac14\cos4x-\dfrac12\cos2x\right)+C=\boldsymbol{-\dfrac18\cos4x-\dfrac14\cos2x+C}$<br>"
         r"(2) $\cos^22x=\dfrac{1+\cos4x}2$ より　$\displaystyle\int\cos^22x\,dx=\boldsymbol{\dfrac x2+\dfrac18\sin4x+C}$",
  "note": r"積→和の公式は、加法定理 $\sin(\alpha\pm\beta)=\sin\alpha\cos\beta\pm\cos\alpha\sin\beta$ を辺々加えれば導ける。忘れたらその場でつくればよい。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\cos3x\cos2x\,dx$　　(2) $\displaystyle\int\sin^23x\,dx$",
  "exa": r"(1) $\dfrac1{10}\sin5x+\dfrac12\sin x+C$　(2) $\dfrac x2-\dfrac1{12}\sin6x+C$"},
 {"lv": 2, "title": r"分数関数の不定積分（割り算と部分分数分解）",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{x+5}{x^2+x-2}\,dx$　　(2) $\displaystyle\int\dfrac{x^2}{x^2-1}\,dx$",
  "hint": r"分母を因数分解し、$\dfrac{a}{x-\alpha}+\dfrac{b}{x-\beta}$ の形（部分分数）に分ける。(2) のように分子の次数が分母の次数以上なら、まず割り算をして分子の次数を下げる。",
  "sol": r"(1) $\dfrac{x+5}{(x-1)(x+2)}=\dfrac a{x-1}+\dfrac b{x+2}$ とおくと $x+5=a(x+2)+b(x-1)$。$x=1$ として $a=2$，$x=-2$ として $b=-1$。<br>"
         r"$\displaystyle\int\left(\dfrac2{x-1}-\dfrac1{x+2}\right)dx=2\log|x-1|-\log|x+2|+C=\boldsymbol{\log\dfrac{(x-1)^2}{|x+2|}+C}$<br>"
         r"(2) $\dfrac{x^2}{x^2-1}=1+\dfrac1{x^2-1}=1+\dfrac12\left(\dfrac1{x-1}-\dfrac1{x+1}\right)$ より<br>"
         r"$\displaystyle\int\dfrac{x^2}{x^2-1}dx=\boldsymbol{x+\dfrac12\log\left|\dfrac{x-1}{x+1}\right|+C}$",
  "note": r"分母に重複する因数があるときは、$\dfrac1{x(x+1)^2}=\dfrac ax+\dfrac b{x+1}+\dfrac c{(x+1)^2}$ のようにおく。分母が $x^2+a^2$ の形で因数分解できないときは、$x=a\tan\theta$ の置換（次節）を使う。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\dfrac{x+7}{x^2-x-6}\,dx$　　(2) $\displaystyle\int\dfrac{dx}{x(x+1)^2}$",
  "exa": r"(1) $2\log|x-3|-\log|x+2|+C$　(2) $\log\left|\dfrac x{x+1}\right|+\dfrac1{x+1}+C$"},
 {"lv": 2, "title": r"三角関数の奇数乗と $\dfrac1{\cos x}$ の積分",
  "q": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\sin^3x\,dx$　　(2) $\displaystyle\int\dfrac{dx}{\cos x}$",
  "hint": r"奇数乗は1つを $dx$ の側に残す。$\sin^3x=(1-\cos^2x)\sin x$ とすれば、$\cos x=t$ で多項式の積分になる。(2) も分母分子に $\cos x$ を掛けて $\dfrac{\cos x}{1-\sin^2x}$ とし、$\sin x=t$ とおく。",
  "sol": r"(1) $\cos x=t$ とおくと $-\sin x\,dx=dt$。<br>"
         r"$\displaystyle\int(1-\cos^2x)\sin x\,dx=-\int(1-t^2)\,dt=-t+\dfrac{t^3}3+C=\boldsymbol{-\cos x+\dfrac13\cos^3x+C}$<br>"
         r"(2) $\sin x=t$ とおくと $\cos x\,dx=dt$。<br>"
         r"$\displaystyle\int\dfrac{\cos x}{1-\sin^2x}dx=\int\dfrac{dt}{1-t^2}=\dfrac12\int\left(\dfrac1{1+t}+\dfrac1{1-t}\right)dt=\dfrac12\log\left|\dfrac{1+t}{1-t}\right|+C$<br>"
         r"$\cos x\neq0$ より $-1<\sin x<1$ だから　$\displaystyle\int\dfrac{dx}{\cos x}=\boldsymbol{\dfrac12\log\dfrac{1+\sin x}{1-\sin x}+C}$",
  "note": r"偶数乗（$\sin^4x$ など）は (1) の方法が使えないので、半角の公式で次数を下げる：$\sin^4x=\left(\dfrac{1-\cos2x}2\right)^2=\dfrac38-\dfrac12\cos2x+\dfrac18\cos4x$。",
  "ex": r"次の不定積分を求めよ。<br>(1) $\displaystyle\int\cos^3x\,dx$　　(2) $\displaystyle\int\dfrac{dx}{\sin x}$",
  "exa": r"(1) $\sin x-\dfrac13\sin^3x+C$　(2) $\dfrac12\log\dfrac{1-\cos x}{1+\cos x}+C$"},
 {"lv": 3, "title": r"無理関数の積分（$x+\sqrt{x^2+1}=t$ の置換）",
  "q": r"$x+\sqrt{x^2+1}=t$ とおくことにより、不定積分 $\displaystyle\int\dfrac{dx}{\sqrt{x^2+1}}$ を求めよ。",
  "hint": r"$\sqrt{x^2+1}=t-x$ の両辺を2乗すると $x^2$ が消え、$x$ が $t$ の分数式で表せる。$dx$ と $\sqrt{x^2+1}$ をともに $t$ で表す。",
  "sol": r"$\sqrt{x^2+1}=t-x$ の両辺を2乗して $x^2+1=t^2-2tx+x^2$，よって $x=\dfrac{t^2-1}{2t}$。<br>"
         r"このとき $dx=\dfrac{t^2+1}{2t^2}dt$，$\sqrt{x^2+1}=t-x=\dfrac{t^2+1}{2t}$ だから<br>"
         r"$\displaystyle\int\dfrac{dx}{\sqrt{x^2+1}}=\int\dfrac{2t}{t^2+1}\cdot\dfrac{t^2+1}{2t^2}dt=\int\dfrac{dt}t=\log|t|+C$<br>"
         r"$\sqrt{x^2+1}>|x|$ より $t>0$ だから　$\displaystyle\int\dfrac{dx}{\sqrt{x^2+1}}=\boldsymbol{\log\left(x+\sqrt{x^2+1}\right)+C}$",
  "note": r"答えを知っていれば、$\left(x+\sqrt{x^2+1}\right)'=1+\dfrac x{\sqrt{x^2+1}}=\dfrac{x+\sqrt{x^2+1}}{\sqrt{x^2+1}}$ から $\dfrac1{\sqrt{x^2+1}}=\dfrac{\left(x+\sqrt{x^2+1}\right)'}{x+\sqrt{x^2+1}}$ と見ることもできる。同様に $A\neq0$ のとき $\displaystyle\int\dfrac{dx}{\sqrt{x^2+A}}=\log\left|x+\sqrt{x^2+A}\right|+C$。さらに部分積分と組み合わせると $\displaystyle\int\sqrt{x^2+1}\,dx=\dfrac12\left\{x\sqrt{x^2+1}+\log\left(x+\sqrt{x^2+1}\right)\right\}+C$ が得られる。",
  "ex": r"不定積分 $\displaystyle\int\dfrac{dx}{\sqrt{x^2+2x+5}}$ を求めよ。",
  "exa": r"$\log\left(x+1+\sqrt{x^2+2x+5}\right)+C$"},
]})


def _v3():
    P = [0.3, 0.7, 1.3, 2.1, 3.7, -0.4]
    assert simplify(sin(3*x)*cos(x) - (sin(4*x)+sin(2*x))/2) == 0
    _D(-cos(4*x)/8 - cos(2*x)/4, sin(3*x)*cos(x), P)
    _D(x/2 + sin(4*x)/8, cos(2*x)**2, P)
    _D(sin(5*x)/10 + sin(x)/2, cos(3*x)*cos(2*x), P)
    _D(x/2 - sin(6*x)/12, sin(3*x)**2, P)
    # 分数関数
    assert simplify(2/(x-1) - 1/(x+2) - (x+5)/(x**2+x-2)) == 0
    _D(log((x-1)**2/(x+2)), (x+5)/(x**2+x-2), [1.3, 2.1, 3.7])
    _D(log((x-1)**2/(-(x+2))), (x+5)/(x**2+x-2), [-2.5, -4.0])
    _D(x + log((x-1)/(x+1))/2, x**2/(x**2-1), [1.3, 2.1, 3.7])
    _D(x + log((1-x)/(x+1))/2, x**2/(x**2-1), [0.3, -0.4])
    assert simplify(2/(x-3) - 1/(x+2) - (x+7)/(x**2-x-6)) == 0
    _D(2*log(x-3) - log(x+2), (x+7)/(x**2-x-6), [3.5, 5.0])
    _D(log(x/(x+1)) + 1/(x+1), 1/(x*(x+1)**2), [0.3, 1.3, 3.7])
    assert simplify(1/x - 1/(x+1) - 1/(x+1)**2 - 1/(x*(x+1)**2)) == 0
    # 奇数乗・1/cos
    _D(-cos(x) + cos(x)**3/3, sin(x)**3, P)
    _D(log((1+sin(x))/(1-sin(x)))/2, 1/cos(x), [0.3, 0.7, 1.3, -0.4, 2.1, 3.7])
    for p in [0.37, 1.1, 2.9, -0.8]:
        assert abs(N((sin(x)**4 - (Rational(3, 8) - cos(2*x)/2 + cos(4*x)/8)).subs(x, p))) < 1e-14
    _D(sin(x) - sin(x)**3/3, cos(x)**3, P)
    _D(log((1-cos(x))/(1+cos(x)))/2, 1/sin(x), [0.3, 1.3, 2.1, -0.4, -2.0])
    # 無理関数
    _D(log(x + sqrt(x**2+1)), 1/sqrt(x**2+1), P)
    tt = symbols("tt", positive=True)
    X = (tt**2-1)/(2*tt)
    assert simplify(diff(X, tt) - (tt**2+1)/(2*tt**2)) == 0 and simplify(tt - X - (tt**2+1)/(2*tt)) == 0
    assert simplify((tt - X)**2 - (X**2 + 1)) == 0
    _D((x*sqrt(x**2+1) + log(x+sqrt(x**2+1)))/2, sqrt(x**2+1), P)
    _D(log(x + sqrt(x**2+3)), 1/sqrt(x**2+3), P)
    _D(log(x + sqrt(x**2-2)), 1/sqrt(x**2-2), [1.6, 2.1, 3.7])
    _D(log(x + 1 + sqrt(x**2+2*x+5)), 1/sqrt(x**2+2*x+5), P + [-3.0])


# ---------------------------------------------------------------- 節4
SEC.append({"title": r"定積分の計算と性質",
"base": r"""・置換積分：$x=g(t)$，$a=g(\alpha)$，$b=g(\beta)$ のとき $\displaystyle\int_a^bf(x)\,dx=\int_\alpha^\beta f(g(t))g'(t)\,dt$（積分区間も変える）<br>
・部分積分：$\displaystyle\int_a^bf(x)g'(x)\,dx=\Big[f(x)g(x)\Big]_a^b-\int_a^bf'(x)g(x)\,dx$<br>
・$\sqrt{a^2-x^2}$ は $x=a\sin\theta$，$\dfrac1{x^2+a^2}$ は $x=a\tan\theta$ とおく（$a>0$）<br>
・$f(x)$ が偶関数なら $\displaystyle\int_{-a}^af(x)\,dx=2\int_0^af(x)\,dx$，奇関数なら $\displaystyle\int_{-a}^af(x)\,dx=0$<br>
・$x=a+b-t$ の置換により $\displaystyle\int_a^bf(x)\,dx=\int_a^bf(a+b-x)\,dx$""",
"items": [
 {"lv": 1, "title": r"定積分の置換積分法・部分積分法",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^1x(1-x)^5dx$　　(2) $\displaystyle\int_1^ex^2\log x\,dx$",
  "hint": r"(1) $1-x=t$ とおく。置換したら積分区間も $t$ の値に変える。(2) 微分すると簡単になる $\log x$ を残し、$x^2$ を積分する側にして部分積分する。",
  "sol": r"(1) $1-x=t$ とおくと $dx=-dt$。$x:0\to1$ のとき $t:1\to0$ だから<br>"
         r"$\displaystyle\int_0^1x(1-x)^5dx=\int_1^0(1-t)t^5(-dt)=\int_0^1(t^5-t^6)\,dt=\dfrac16-\dfrac17=\boldsymbol{\dfrac1{42}}$<br>"
         r"(2) $\displaystyle\int_1^e\left(\dfrac{x^3}3\right)'\log x\,dx=\left[\dfrac{x^3}3\log x\right]_1^e-\int_1^e\dfrac{x^3}3\cdot\dfrac1x\,dx=\dfrac{e^3}3-\left[\dfrac{x^3}9\right]_1^e=\dfrac{e^3}3-\dfrac{e^3-1}9=\boldsymbol{\dfrac{2e^3+1}9}$",
  "note": r"定積分の置換では、もとの変数 $x$ に戻す必要はない（積分区間を $t$ の値に変えたので、$t$ のまま計算を終えられる）。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^1x\sqrt{1-x}\,dx$　　(2) $\displaystyle\int_0^{\frac\pi2}x\cos x\,dx$",
  "exa": r"(1) $\dfrac4{15}$　(2) $\dfrac\pi2-1$"},
 {"lv": 2, "title": r"$x=a\sin\theta$，$x=a\tan\theta$ の置換",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^1\sqrt{4-x^2}\,dx$　　(2) $\displaystyle\int_0^{\sqrt3}\dfrac{dx}{x^2+3}$",
  "hint": r"$\sqrt{a^2-x^2}$ は $x=a\sin\theta$ とおくと $\sqrt{a^2(1-\sin^2\theta)}=a\cos\theta$、$\dfrac1{x^2+a^2}$ は $x=a\tan\theta$ とおくと $1+\tan^2\theta=\dfrac1{\cos^2\theta}$ により、根号や分母が簡単になる。",
  "sol": r"(1) $x=2\sin\theta$ とおくと $dx=2\cos\theta\,d\theta$，$x:0\to1$ のとき $\theta:0\to\dfrac\pi6$。この範囲で $\cos\theta>0$ だから $\sqrt{4-x^2}=2\cos\theta$。<br>"
         r"$\displaystyle\int_0^{\frac\pi6}4\cos^2\theta\,d\theta=\int_0^{\frac\pi6}2(1+\cos2\theta)\,d\theta=\Big[2\theta+\sin2\theta\Big]_0^{\frac\pi6}=\boldsymbol{\dfrac\pi3+\dfrac{\sqrt3}2}$<br>"
         r"(2) $x=\sqrt3\tan\theta$ とおくと $dx=\dfrac{\sqrt3}{\cos^2\theta}d\theta$，$x:0\to\sqrt3$ のとき $\theta:0\to\dfrac\pi4$。$x^2+3=\dfrac3{\cos^2\theta}$ だから<br>"
         r"$\displaystyle\int_0^{\frac\pi4}\dfrac{\cos^2\theta}3\cdot\dfrac{\sqrt3}{\cos^2\theta}d\theta=\dfrac1{\sqrt3}\cdot\dfrac\pi4=\boldsymbol{\dfrac{\sqrt3}{12}\pi}$",
  "note": r"(1) は円 $x^2+y^2=4$ の一部の面積で、中心角 $\dfrac\pi6$ の扇形（面積 $\dfrac\pi3$）と直角三角形（面積 $\dfrac{\sqrt3}2$）に分けても求められる。置換の結果を図形で確かめる習慣をつけるとよい。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-1}^1\sqrt{2-x^2}\,dx$　　(2) $\displaystyle\int_0^1\dfrac{dx}{x^2+x+1}$",
  "exa": r"(1) $\dfrac\pi2+1$　(2) $\dfrac{\sqrt3}9\pi$"},
 {"lv": 2, "title": r"偶関数・奇関数の定積分",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-\frac\pi2}^{\frac\pi2}(x+\cos x)^2dx$　　(2) $\displaystyle\int_{-1}^1\dfrac{x^3+x^2+\sin x}{1+x^2}\,dx$",
  "hint": r"積分区間が原点について対称なので、被積分関数を偶関数と奇関数に分ける。奇関数の部分は $0$、偶関数の部分は $\displaystyle2\int_0^a$ になる。（奇関数）×（偶関数）は奇関数である。",
  "sol": r"(1) $(x+\cos x)^2=x^2+\cos^2x+2x\cos x$ で、$x^2+\cos^2x$ は偶関数、$2x\cos x$ は奇関数だから<br>"
         r"$\displaystyle\int_{-\frac\pi2}^{\frac\pi2}(x+\cos x)^2dx=2\int_0^{\frac\pi2}\left(x^2+\dfrac{1+\cos2x}2\right)dx=2\left[\dfrac{x^3}3+\dfrac x2+\dfrac{\sin2x}4\right]_0^{\frac\pi2}=\boldsymbol{\dfrac{\pi^3}{12}+\dfrac\pi2}$<br>"
         r"(2) $\dfrac{x^3+\sin x}{1+x^2}$ は奇関数、$\dfrac{x^2}{1+x^2}$ は偶関数である。$x=\tan\theta$ とおくと $\displaystyle\int_0^1\dfrac{dx}{1+x^2}=\int_0^{\frac\pi4}d\theta=\dfrac\pi4$ だから<br>"
         r"$\displaystyle\int_{-1}^1\dfrac{x^3+x^2+\sin x}{1+x^2}dx=2\int_0^1\left(1-\dfrac1{1+x^2}\right)dx=2\left(1-\dfrac\pi4\right)=\boldsymbol{2-\dfrac\pi2}$",
  "note": r"$\dfrac{\sin x}{1+x^2}$ のように原始関数が求められない奇関数でも、原点対称な区間での積分は $0$ になる。原始関数を探す前に、まず偶奇を確認する。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{-\pi}^{\pi}(x+\sin x)^2dx$　　(2) $\displaystyle\int_{-2}^2\dfrac{x^5-x^2+2x}{x^2+4}\,dx$",
  "exa": r"(1) $\dfrac23\pi^3+5\pi$　(2) $\pi-4$"},
 {"lv": 2, "title": r"絶対値を含む関数の定積分",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_{\frac1e}^e|\log x|\,dx$　　(2) $\displaystyle\int_0^\pi x|\cos x|\,dx$",
  "hint": r"絶対値の中身の符号が変わる点（$x=1$，$x=\dfrac\pi2$）で積分区間を分け、絶対値をはずす。原始関数は部分積分で求める。",
  "sol": r"(1) $\displaystyle\int\log x\,dx=x\log x-x+C$ を用いる。$\dfrac1e\leqq x\leqq1$ で $\log x\leqq0$，$1\leqq x\leqq e$ で $\log x\geqq0$ より<br>"
         r"$\displaystyle\int_{\frac1e}^e|\log x|\,dx=-\Big[x\log x-x\Big]_{\frac1e}^1+\Big[x\log x-x\Big]_1^e=-\left\{-1-\left(-\dfrac2e\right)\right\}+\{0-(-1)\}=\boldsymbol{2-\dfrac2e}$<br>"
         r"(2) $\displaystyle\int x\cos x\,dx=x\sin x+\cos x+C$ を用いる。$0\leqq x\leqq\dfrac\pi2$ で $\cos x\geqq0$，$\dfrac\pi2\leqq x\leqq\pi$ で $\cos x\leqq0$ より<br>"
         r"$\displaystyle\int_0^\pi x|\cos x|\,dx=\Big[x\sin x+\cos x\Big]_0^{\frac\pi2}-\Big[x\sin x+\cos x\Big]_{\frac\pi2}^\pi=\left(\dfrac\pi2-1\right)-\left(-1-\dfrac\pi2\right)=\boldsymbol{\pi}$",
  "note": r"$a\leqq x\leqq c$ で $f(x)\geqq0$，$c\leqq x\leqq b$ で $f(x)\leqq0$ のとき、$f(x)$ の原始関数 $G(x)$ を用いて $\displaystyle\int_a^b|f(x)|\,dx=\{G(c)-G(a)\}-\{G(b)-G(c)\}=2G(c)-G(a)-G(b)$ とまとめて計算できる。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^2|e^x-e|\,dx$　　(2) $\displaystyle\int_0^2|x-1|e^x\,dx$",
  "exa": r"(1) $(e-1)^2$　(2) $2e-2$"},
 {"lv": 3, "title": r"対称性を利用する置換（$x=\dfrac\pi2-t$，$x=-t$）",
  "q": r"次の定積分を求めよ。<br>(1) $\displaystyle I=\int_0^{\frac\pi2}\dfrac{\sin x}{\sin x+\cos x}\,dx$　　(2) $\displaystyle K=\int_{-1}^1\dfrac{x^2}{1+e^x}\,dx$",
  "hint": r"原始関数を直接求めるのは大変。(1) は $x=\dfrac\pi2-t$ とおくと $\sin$ と $\cos$ が入れかわった積分になり、もとの積分と足すと簡単になる。(2) は $x=-t$ とおいて、もとの積分と足し合わせる。",
  "sol": r"(1) $x=\dfrac\pi2-t$ とおくと $dx=-dt$，$x:0\to\dfrac\pi2$ のとき $t:\dfrac\pi2\to0$ で<br>"
         r"$I=\displaystyle\int_{\frac\pi2}^0\dfrac{\cos t}{\cos t+\sin t}(-dt)=\int_0^{\frac\pi2}\dfrac{\cos x}{\sin x+\cos x}dx$<br>"
         r"よって $2I=\displaystyle\int_0^{\frac\pi2}\dfrac{\sin x+\cos x}{\sin x+\cos x}dx=\dfrac\pi2$ だから　$I=\boldsymbol{\dfrac\pi4}$<br>"
         r"(2) $x=-t$ とおくと $K=\displaystyle\int_1^{-1}\dfrac{t^2}{1+e^{-t}}(-dt)=\int_{-1}^1\dfrac{t^2e^t}{e^t+1}dt=\int_{-1}^1\dfrac{x^2e^x}{1+e^x}dx$。<br>"
         r"よって $2K=\displaystyle\int_{-1}^1\dfrac{x^2(1+e^x)}{1+e^x}dx=\int_{-1}^1x^2dx=\dfrac23$ だから　$K=\boldsymbol{\dfrac13}$",
  "note": r"一般に $\displaystyle\int_0^{\frac\pi2}f(\sin x)\,dx=\int_0^{\frac\pi2}f(\cos x)\,dx$，$\displaystyle\int_{-a}^af(x)\,dx=\int_0^a\{f(x)+f(-x)\}\,dx$ が成り立つ。(2) では $\dfrac1{1+e^x}+\dfrac1{1+e^{-x}}=1$ がかぎになる。",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^{\frac\pi2}\dfrac{\cos^3x}{\sin^3x+\cos^3x}\,dx$　　(2) $\displaystyle\int_{-\frac\pi2}^{\frac\pi2}\dfrac{\cos x}{1+e^x}\,dx$",
  "exa": r"(1) $\dfrac\pi4$　(2) $1$"},
 {"lv": 4, "title": r"$x=\pi-t$ の置換と $\displaystyle\int_0^\pi xf(\sin x)\,dx$",
  "q": r"(1) 連続関数 $f(u)$ に対して、$\displaystyle\int_0^\pi xf(\sin x)\,dx=\dfrac\pi2\int_0^\pi f(\sin x)\,dx$ が成り立つことを示せ。<br>(2) 定積分 $\displaystyle\int_0^\pi\dfrac{x\sin x}{1+\cos^2x}\,dx$ を求めよ。",
  "hint": r"$x=\pi-t$ とおくと $\sin x=\sin t$ は変わらず、$x$ だけが $\pi-t$ に変わる。これで厄介な因子 $x$ を消すことができる。(2) は $1+\cos^2x=2-\sin^2x$ と見れば (1) が使える。",
  "sol": r"(1) $I=\displaystyle\int_0^\pi xf(\sin x)\,dx$ で $x=\pi-t$ とおくと、$dx=-dt$，$\sin(\pi-t)=\sin t$ より<br>"
         r"$I=\displaystyle\int_\pi^0(\pi-t)f(\sin t)(-dt)=\pi\int_0^\pi f(\sin t)\,dt-\int_0^\pi tf(\sin t)\,dt=\pi\int_0^\pi f(\sin x)\,dx-I$<br>"
         r"よって $\displaystyle I=\dfrac\pi2\int_0^\pi f(\sin x)\,dx$ が成り立つ。<br>"
         r"(2) $\dfrac{\sin x}{1+\cos^2x}=\dfrac{\sin x}{2-\sin^2x}$ は、$f(u)=\dfrac u{2-u^2}$（$0\leqq u\leqq1$ で連続）として $f(\sin x)$ の形である。(1) より<br>"
         r"$\displaystyle\int_0^\pi\dfrac{x\sin x}{1+\cos^2x}dx=\dfrac\pi2\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx$<br>"
         r"右辺の積分で $\cos x=u$ とおくと $-\sin x\,dx=du$，$x:0\to\pi$ のとき $u:1\to-1$ だから、$u=\tan\theta$ の置換も用いて<br>"
         r"$\displaystyle\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx=\int_{-1}^1\dfrac{du}{1+u^2}=2\int_0^{\frac\pi4}d\theta=\dfrac\pi2$<br>"
         r"したがって、求める値は $\dfrac\pi2\cdot\dfrac\pi2=\boldsymbol{\dfrac{\pi^2}4}$",
  "note": r"$\dfrac{x\sin x}{1+\cos^2x}$ の原始関数を部分積分などで直接求めるのは難しい。置換で $x$ を消すのが定石である。同じ方法で $\displaystyle\int_0^\pi x\sin^3x\,dx=\dfrac\pi2\int_0^\pi\sin^3x\,dx=\dfrac23\pi$ なども計算できる。",
  "ex": r"定積分 $\displaystyle\int_0^\pi\dfrac{x\sin x}{3+\sin^2x}\,dx$ を求めよ。",
  "exa": r"$\dfrac\pi4\log3$"},
]})


def _v4():
    _Q(x*(1-x)**5, 0, 1, Rational(1, 42))
    _Q(x**2*log(x), 1, E, (2*E**3+1)/9)
    _Q(x*sqrt(1-x), 0, 1, Rational(4, 15))
    _Q(x*cos(x), 0, pi/2, pi/2 - 1)
    _Q(sqrt(4-x**2), 0, 1, pi/3 + sqrt(3)/2)
    _Q(1/(x**2+3), 0, sqrt(3), sqrt(3)*pi/12)
    _Q(sqrt(2-x**2), -1, 1, pi/2 + 1)
    _Q(1/(x**2+x+1), 0, 1, sqrt(3)*pi/9)
    # 偶奇
    _Q((x+cos(x))**2, -pi/2, pi/2, pi**3/12 + pi/2)
    _Q((x**3+x**2+sin(x))/(1+x**2), -1, 1, 2 - pi/2, sym=False)
    _Q(x**2/(1+x**2), -1, 1, 2 - pi/2)
    _Q((x+sin(x))**2, -pi, pi, 2*pi**3/3 + 5*pi)
    _Q((x**5-x**2+2*x)/(x**2+4), -2, 2, pi - 4)
    # 絶対値
    _Q(Abs(log(x)), 1/E, E, 2 - 2/E, brk=(1,), sym=False)
    _Q(-log(x), 1/E, 1, 1 - 2/E)
    _Q(x*Abs(cos(x)), 0, pi, pi, brk=(pi/2,), sym=False)
    _Q(Abs(exp(x)-E), 0, 2, (E-1)**2, brk=(1,), sym=False)
    _Q(Abs(x-1)*exp(x), 0, 2, 2*E - 2, brk=(1,), sym=False)
    _Q((x-1)*exp(x), 1, 2, E)
    _Q(E-exp(x), 0, 1, 1)
    _Q(exp(x)-E, 1, 2, E**2 - 2*E)
    # 対称性
    _Q(sin(x)/(sin(x)+cos(x)), 0, pi/2, pi/4, sym=False)
    _Q(x**2/(1+exp(x)), -1, 1, Rational(1, 3), sym=False)
    _Q(cos(x)**3/(sin(x)**3+cos(x)**3), 0, pi/2, pi/4, sym=False)
    _Q(cos(x)/(1+exp(x)), -pi/2, pi/2, 1, sym=False)
    # x=π-t
    _Q(x*sin(x)/(1+cos(x)**2), 0, pi, pi**2/4, sym=False)
    _Q(sin(x)/(1+cos(x)**2), 0, pi, pi/2)
    _Q(x*sin(x)**3, 0, pi, 2*pi/3)
    _Q(x*sin(x)/(3+sin(x)**2), 0, pi, pi*log(3)/4, sym=False)
    _Q(sin(x)/(3+sin(x)**2), 0, pi, log(3)/2, sym=False)
    for _ in range(5):   # (1) の恒等式を f をいろいろ変えて数値確認
        c = [random.uniform(-2, 2) for _ in range(4)]
        f = c[0] + c[1]*x + c[2]*x**2 + c[3]*exp(x)
        L = mp.quad(lambdify(x, x*f.subs(x, sin(x)), "mpmath"), [0, mp.pi])
        R = mp.pi/2*mp.quad(lambdify(x, f.subs(x, sin(x)), "mpmath"), [0, mp.pi])
        assert abs(L - R) < 1e-20


# ---------------------------------------------------------------- 節5
SEC.append({"title": r"定積分で表された関数",
"base": r"""・$a$ が定数のとき $\dfrac{d}{dx}\displaystyle\int_a^xf(t)\,dt=f(x)$。一般に $\dfrac{d}{dx}\displaystyle\int_{h(x)}^{g(x)}f(t)\,dt=f(g(x))g'(x)-f(h(x))h'(x)$<br>
・$\displaystyle\int_a^bf(t)\,dt$（$a,\ b$ は定数）は定数なので、文字でおいて方程式をつくる<br>
・$\displaystyle\int_a^x(x-t)f(t)\,dt=x\int_a^xf(t)\,dt-\int_a^xtf(t)\,dt$ と、$x$ を積分の外に出してから微分する""",
"items": [
 {"lv": 2, "title": r"定積分で表された関数の微分",
  "q": r"次の関数を $x$ で微分せよ。<br>(1) $\displaystyle\int_0^{x^2}\sin\sqrt t\,dt$（$x>0$）　　(2) $\displaystyle\int_x^{2x}\dfrac{dt}{1+t^2}$　　(3) $\displaystyle\int_0^x(x-t)e^t\,dt$",
  "hint": r"$f(t)$ の原始関数を $F(t)$ とすると $\displaystyle\int_{h(x)}^{g(x)}f(t)\,dt=F(g(x))-F(h(x))$。合成関数の微分法で $f(g(x))g'(x)-f(h(x))h'(x)$ となる。(3) は被積分関数に $x$ が含まれるので、$x$ を積分の外に出してから微分する。",
  "sol": r"(1) $\sin\sqrt t$ の原始関数の1つを $F(t)$ とすると、与えられた関数は $F(x^2)-F(0)$。$x>0$ より $\sqrt{x^2}=x$ だから<br>"
         r"$\dfrac{d}{dx}\{F(x^2)-F(0)\}=F'(x^2)\cdot2x=\boldsymbol{2x\sin x}$<br>"
         r"(2) $\dfrac{1}{1+(2x)^2}\cdot2-\dfrac1{1+x^2}=\dfrac{2(1+x^2)-(1+4x^2)}{(1+x^2)(1+4x^2)}=\boldsymbol{\dfrac{1-2x^2}{(1+x^2)(1+4x^2)}}$<br>"
         r"(3) $\displaystyle\int_0^x(x-t)e^tdt=x\int_0^xe^tdt-\int_0^xte^tdt$ だから、積の微分法により、導関数は<br>"
         r"$\displaystyle\int_0^xe^tdt+xe^x-xe^x=\int_0^xe^tdt=\boldsymbol{e^x-1}$",
  "note": r"(3) で「$\dfrac{d}{dx}\displaystyle\int_0^x(x-t)e^tdt=(x-x)e^x=0$」とするのは誤り。被積分関数が $x$ を含むときは、必ず $x$ を積分の外に出す。",
  "ex": r"次の関数を $x$ で微分せよ。<br>(1) $\displaystyle\int_0^{\sin x}\sqrt{1-t^2}\,dt$（$0<x<\dfrac\pi2$）　　(2) $\displaystyle\int_x^{x^2}\log t\,dt$（$x>0$）　　(3) $\displaystyle\int_0^x(x-t)\cos t\,dt$",
  "exa": r"(1) $\cos^2x$　(2) $(4x-1)\log x$　(3) $\sin x$"},
 {"lv": 2, "title": r"定積分を含む関数方程式（定積分を定数とおく）",
  "q": r"等式 $f(x)=e^x+\displaystyle\int_0^1tf(t)\,dt$ を満たす関数 $f(x)$ を求めよ。",
  "hint": r"積分区間が定数なので $\displaystyle\int_0^1tf(t)\,dt$ は定数である。これを $a$ とおくと $f(x)=e^x+a$ と表せるので、$a$ の定義式に代入して $a$ の方程式をつくる。",
  "sol": r"$a=\displaystyle\int_0^1tf(t)\,dt$ とおくと $f(x)=e^x+a$。よって<br>"
         r"$a=\displaystyle\int_0^1t(e^t+a)\,dt=\Big[(t-1)e^t\Big]_0^1+\dfrac a2=1+\dfrac a2$<br>"
         r"これを解いて $a=2$。したがって　$\boldsymbol{f(x)=e^x+2}$",
  "note": r"積分区間に $x$ を含む場合（$\displaystyle\int_0^xf(t)\,dt$ など）は定数ではないので、定数とおくことはできない。その場合は両辺を微分する（後の例題）。",
  "ex": r"等式 $f(x)=e^{-x}+\displaystyle\int_0^1e^tf(t)\,dt$ を満たす関数 $f(x)$ を求めよ。",
  "exa": r"$f(x)=e^{-x}-\dfrac1{e-2}$"},
 {"lv": 3, "title": r"$\displaystyle\int_0^x(x-t)f(t)\,dt$ を含む等式",
  "q": r"すべての実数 $x$ について $\displaystyle\int_0^x(x-t)f(t)\,dt=e^{2x}+ax+b$ が成り立つような連続関数 $f(x)$ と定数 $a,\ b$ を求めよ。",
  "hint": r"左辺を $\displaystyle x\int_0^xf(t)\,dt-\int_0^xtf(t)\,dt$ と分けて2回微分すると $f(x)$ が得られる。微分すると定数の情報が失われるので、各段階で $x=0$ を代入した式も使う。",
  "sol": r"左辺 $=x\displaystyle\int_0^xf(t)\,dt-\int_0^xtf(t)\,dt$。両辺を $x$ で微分すると<br>"
         r"$\displaystyle\int_0^xf(t)\,dt+xf(x)-xf(x)=2e^{2x}+a$，すなわち　$\displaystyle\int_0^xf(t)\,dt=2e^{2x}+a$　…①<br>"
         r"①で $x=0$ とおくと $0=2+a$ より $a=-2$。①をさらに微分して　$f(x)=4e^{2x}$<br>"
         r"また、もとの等式で $x=0$ とおくと $0=1+b$ より $b=-1$。<br>"
         r"逆に $f(x)=4e^{2x}$ のとき、部分積分により<br>"
         r"$\displaystyle\int_0^x(x-t)\cdot4e^{2t}dt=\Big[(x-t)\cdot2e^{2t}\Big]_0^x+\int_0^x2e^{2t}dt=-2x+e^{2x}-1$<br>"
         r"となり、$a=-2$，$b=-1$ で等式は成り立つ。よって　$\boldsymbol{f(x)=4e^{2x},\ a=-2,\ b=-1}$",
  "note": r"「微分した等式」と「もとの等式」は同値ではない。$F'(x)=G'(x)$ から言えるのは $F(x)=G(x)+c$（$c$ は定数）までなので、$x=0$ での値の一致を加えてはじめて同値になる。",
  "ex": r"すべての実数 $x$ について $\displaystyle\int_0^x(x-t)f(t)\,dt=e^{-x}+ax+b$ が成り立つような連続関数 $f(x)$ と定数 $a,\ b$ を求めよ。",
  "exa": r"$f(x)=e^{-x}$，$a=1$，$b=-1$"},
 {"lv": 3, "title": r"定積分で表された関数の最大値",
  "q": r"$x\geqq0$ において、関数 $F(x)=\displaystyle\int_0^xe^{-t}\sin t\,dt$ の最大値を求めよ。",
  "hint": r"$F'(x)=e^{-x}\sin x$ の符号から増減を調べる。極大となる点は無数にあるので、極大値を具体的に計算して大小を比べる。",
  "sol": r"$F'(x)=e^{-x}\sin x$。$e^{-x}>0$ より $F'(x)$ の符号は $\sin x$ の符号と一致し、$k=0,\ 1,\ 2,\ \cdots$ に対して、$F(x)$ は $2k\pi\leqq x\leqq(2k+1)\pi$ で増加、$(2k+1)\pi\leqq x\leqq(2k+2)\pi$ で減少する。<br>"
         r"よって、区間 $2k\pi\leqq x\leqq(2k+2)\pi$ における最大値は $F((2k+1)\pi)$ であり、$F(x)$ の最大値はこれらのうち最大のものである。<br>"
         r"部分積分を2回行うと $\displaystyle\int e^{-t}\sin t\,dt=-\dfrac12e^{-t}(\sin t+\cos t)+C$ が得られるから<br>"
         r"$F(x)=\dfrac12-\dfrac12e^{-x}(\sin x+\cos x)$，　$F((2k+1)\pi)=\dfrac12\left\{1+e^{-(2k+1)\pi}\right\}$<br>"
         r"これは $k$ が大きいほど小さいから、最大値は $k=0$ のときの　$\boldsymbol{F(\pi)=\dfrac{1+e^{-\pi}}2}$",
  "note": r"$x\to\infty$ のとき $F(x)\to\dfrac12$。極大値 $\dfrac12(1+e^{-\pi}),\ \dfrac12(1+e^{-3\pi}),\ \cdots$ は $\dfrac12$ に近づきながら減少し、極小値 $F(2k\pi)=\dfrac12(1-e^{-2k\pi})$ は増加する。$F(x)$ は振動しながら $\dfrac12$ に収束する。",
  "ex": r"$x\geqq0$ において、関数 $F(x)=\displaystyle\int_0^xe^{-t}\cos t\,dt$ の最大値を求めよ。",
  "exa": r"$x=\dfrac\pi2$ のとき最大値 $\dfrac{1+e^{-\frac\pi2}}2$"},
 {"lv": 4, "title": r"絶対値を含む定積分で表された関数の最小値",
  "q": r"実数 $x$ に対して $F(x)=\displaystyle\int_0^{\frac\pi2}|\sin t-x\cos t|\,dt$ とする。$F(x)$ の最小値と、そのときの $x$ の値を求めよ。",
  "hint": r"$x\leqq0$ なら絶対値の中は常に $0$ 以上。$x>0$ なら $\sin t-x\cos t=\cos t(\tan t-x)$ の符号は、$\tan\alpha=x$ となる $\alpha$ の前後で変わる。$\alpha$ を用いて積分を計算し、最後に $\sin\alpha,\ \cos\alpha$ を $x$ で表す。",
  "sol": r"【$x\leqq0$ のとき】$0\leqq t\leqq\dfrac\pi2$ で $\sin t-x\cos t\geqq0$ だから $F(x)=\Big[-\cos t-x\sin t\Big]_0^{\frac\pi2}=1-x\geqq1$。<br>"
         r"【$x>0$ のとき】$\tan\alpha=x$，$0<\alpha<\dfrac\pi2$ となる $\alpha$ をとる。$\sin t-x\cos t=\cos t(\tan t-x)$ は $0\leqq t\leqq\alpha$ で $0$ 以下、$\alpha\leqq t\leqq\dfrac\pi2$ で $0$ 以上である（$t=\dfrac\pi2$ では値 $1$）。<br>"
         r"$G(t)=-\cos t-x\sin t$ とおくと $G'(t)=\sin t-x\cos t$ だから<br>"
         r"$F(x)=-\{G(\alpha)-G(0)\}+\left\{G\left(\dfrac\pi2\right)-G(\alpha)\right\}=G(0)+G\left(\dfrac\pi2\right)-2G(\alpha)=-1-x+2(\cos\alpha+x\sin\alpha)$<br>"
         r"$\cos\alpha=\dfrac1{\sqrt{1+x^2}}$，$\sin\alpha=\dfrac x{\sqrt{1+x^2}}$ より $\cos\alpha+x\sin\alpha=\sqrt{1+x^2}$ なので<br>"
         r"$F(x)=2\sqrt{1+x^2}-x-1$，　$F'(x)=\dfrac{2x}{\sqrt{1+x^2}}-1=\dfrac{2x-\sqrt{1+x^2}}{\sqrt{1+x^2}}$<br>"
         r"$x>0$ では、$2x-\sqrt{1+x^2}$ の符号は $4x^2-(1+x^2)=3x^2-1$ の符号と一致するから、$F(x)$ は $0<x\leqq\dfrac1{\sqrt3}$ で減少、$x\geqq\dfrac1{\sqrt3}$ で増加し、$F\left(\dfrac1{\sqrt3}\right)=\dfrac4{\sqrt3}-\dfrac1{\sqrt3}-1=\sqrt3-1$。<br>"
         r"$\sqrt3-1<1$ だから、$x\leqq0$ の場合も含めて　$\boldsymbol{x=\dfrac{\sqrt3}3}$ のとき最小値 $\boldsymbol{\sqrt3-1}$",
  "note": r"$\sin t-x\cos t=\sqrt{1+x^2}\sin(t-\alpha)$ と合成すると、$F(x)=\sqrt{1+x^2}\displaystyle\int_0^{\frac\pi2}|\sin(t-\alpha)|\,dt$ と見ることもできる。定積分で表された関数は「まず積分を計算して $x$ の式にする」のが基本で、絶対値は符号の変わる点を文字（ここでは $\alpha$）でおいて処理する。",
  "ex": r"実数 $x$ に対して $F(x)=\displaystyle\int_0^1|e^t-x|\,dt$ とする。$F(x)$ の最小値と、そのときの $x$ の値を求めよ。",
  "exa": r"$x=\sqrt e$ のとき最小値 $(\sqrt e-1)^2$"},
 {"lv": 5, "title": r"$\displaystyle\int_x^{2x}\dfrac{\sin t}t\,dt$ の最大（評価による極大値の比較）",
  "q": r"$x>0$ に対して $F(x)=\displaystyle\int_x^{2x}\dfrac{\sin t}t\,dt$ とする。$F(x)$ を最大にする $x$ の値を求めよ。",
  "hint": r"$F'(x)$ の符号から極大となる $x$ は無数にあるが、$\dfrac{\sin t}t$ の原始関数は求められないので、極大値どうしを直接比べることはできない。部分積分で「$x$ が大きいと $|F(x)|$ は小さい」ことを示し、最初の極大値を下から評価して比べる。",
  "sol": r"$F'(x)=2\cdot\dfrac{\sin2x}{2x}-\dfrac{\sin x}x=\dfrac{\sin2x-\sin x}x=\dfrac{\sin x(2\cos x-1)}x$<br>"
         r"$x>0$ だから $F'(x)$ の符号は $\sin x(2\cos x-1)$ の符号と一致し、周期 $2\pi$ でくり返す。$0<x<2\pi$ では $0<x<\dfrac\pi3$ で正、$\dfrac\pi3<x<\pi$ で負、$\pi<x<\dfrac53\pi$ で正、$\dfrac53\pi<x<2\pi$ で負。<br>"
         r"よって $F(x)$ は $0<x\leqq\dfrac\pi3$ で増加、$\dfrac\pi3\leqq x\leqq\pi$ で減少、$\pi\leqq x\leqq\dfrac53\pi$ で増加する。<br>"
         r"【$x$ が大きいときの評価】部分積分により<br>"
         r"$F(x)=\left[-\dfrac{\cos t}t\right]_x^{2x}-\displaystyle\int_x^{2x}\dfrac{\cos t}{t^2}dt=\dfrac{\cos x}x-\dfrac{\cos2x}{2x}-\int_x^{2x}\dfrac{\cos t}{t^2}dt$<br>"
         r"$\displaystyle\left|\int_x^{2x}\dfrac{\cos t}{t^2}dt\right|\leqq\int_x^{2x}\dfrac{dt}{t^2}=\dfrac1{2x}$ だから　$|F(x)|\leqq\dfrac1x+\dfrac1{2x}+\dfrac1{2x}=\dfrac2x$<br>"
         r"【最初の極大値の評価】$\dfrac\pi3\leqq t\leqq\dfrac23\pi$ で $\sin t\geqq\dfrac{\sqrt3}2$，$\dfrac1t\geqq\dfrac3{2\pi}$ だから　$F\left(\dfrac\pi3\right)\geqq\dfrac{\sqrt3}2\cdot\dfrac3{2\pi}\cdot\dfrac\pi3=\dfrac{\sqrt3}4$<br>"
         r"【比較】$5\sqrt3\pi>5\cdot1.7\cdot3=25.5>24$ より $\dfrac6{5\pi}<\dfrac{\sqrt3}4$。<br>"
         r"$x\geqq\dfrac53\pi$ のとき $F(x)\leqq\dfrac2x\leqq\dfrac6{5\pi}<\dfrac{\sqrt3}4\leqq F\left(\dfrac\pi3\right)$。<br>"
         r"$\pi\leqq x<\dfrac53\pi$ のときは、増加することから $F(x)<F\left(\dfrac53\pi\right)<F\left(\dfrac\pi3\right)$。<br>"
         r"$0<x<\pi$ のときは、増減から $F(x)\leqq F\left(\dfrac\pi3\right)$ で、等号は $x=\dfrac\pi3$ のときに限る。<br>"
         r"以上より、$F(x)$ を最大にする $x$ は　$\boldsymbol{x=\dfrac\pi3}$",
  "note": r"$F\left(\dfrac\pi3\right)\fallingdotseq0.661$ である。$|F(x)|\leqq\dfrac2x$ から $\displaystyle\lim_{x\to\infty}F(x)=0$ もわかる。極大値を直接比べられないときは、(i) 遠くの値をまとめて上から評価する、(ii) 候補の値を下から評価する、の2つで挟むのが最難関レベルの定石である。評価は粗くてよいが、(i) をどこから使うか（ここでは2番目の極大点 $\dfrac53\pi$ から）を決めるのが要点。",
  "ex": r"$x>0$ に対して $F(x)=\displaystyle\int_x^{2x}\dfrac{\sin t}t\,dt$ とする。$F(x)$ を最小にする $x$ の値を求めよ。",
  "exa": r"$x=\pi$（極小点は $\pi,\ 2\pi,\ 3\pi,\ \cdots$。$F(\pi)<-\dfrac1{2\pi}\displaystyle\int_\pi^{2\pi}|\sin t|\,dt=-\dfrac1\pi$，$x\geqq2\pi$ では $F(x)\geqq-\dfrac2x\geqq-\dfrac1\pi$）"},
]})


def _v5():
    # 微分
    for p in [0.4, 1.1, 2.3]:
        X = mp.mpf(p)
        g = lambda X: mp.quad(lambda s: mp.sin(mp.sqrt(s)), [0, X**2])
        assert abs(mp.diff(g, X) - 2*X*mp.sin(X)) < 1e-15
        g = lambda X: mp.quad(lambda s: 1/(1+s**2), [X, 2*X])
        assert abs(mp.diff(g, X) - (1-2*X**2)/((1+X**2)*(1+4*X**2))) < 1e-15
        g = lambda X: mp.quad(lambda s: (X-s)*mp.e**s, [0, X])
        assert abs(mp.diff(g, X) - (mp.e**X - 1)) < 1e-15
        g = lambda X: mp.quad(lambda s: mp.sqrt(1-s**2), [0, mp.sin(X)])
        if p < 1.5:
            assert abs(mp.diff(g, X) - mp.cos(X)**2) < 1e-12
        g = lambda X: mp.quad(lambda s: mp.log(s), [X, X**2])
        assert abs(mp.diff(g, X) - (4*X-1)*mp.log(X)) < 1e-15
        g = lambda X: mp.quad(lambda s: (X-s)*mp.cos(s), [0, X])
        assert abs(mp.diff(g, X) - mp.sin(X)) < 1e-15
    # 関数方程式
    a = symbols("a")
    assert integrate(t*(exp(t)+a), (t, 0, 1)).expand() == 1 + a/2
    _Q(x*(exp(x)+2), 0, 1, 2)
    av = 1/(2-E)
    _Q(exp(x)*(exp(-x)+av), 0, 1, av)
    assert abs(N(av + 1/(E-2))) < 1e-15
    # (x-t)f(t)
    X = symbols("X", real=True)
    assert simplify(integrate((X-t)*4*exp(2*t), (t, 0, X)) - (exp(2*X) - 2*X - 1)) == 0
    assert simplify(integrate((X-t)*exp(-t), (t, 0, X)) - (exp(-X) + X - 1)) == 0
    # 最大値 F(x)=∫e^{-t}sin t
    Fx = Rational(1, 2) - exp(-x)*(sin(x)+cos(x))/2
    _D(Fx, exp(-x)*sin(x), [0.3, 1.7, 4.2])
    assert Fx.subs(x, 0) == 0
    Ff = lambdify(x, Fx, "math")
    xs = [0.001*k for k in range(0, 40000)]
    i = max(range(len(xs)), key=lambda k: Ff(xs[k]))
    assert abs(xs[i] - math.pi) < 2e-3 and abs(Ff(math.pi) - (1+math.exp(-math.pi))/2) < 1e-12
    Gx = Rational(1, 2) + exp(-x)*(sin(x)-cos(x))/2
    _D(Gx, exp(-x)*cos(x), [0.3, 1.7, 4.2])
    assert Gx.subs(x, 0) == 0
    Gf = lambdify(x, Gx, "math")
    i = max(range(len(xs)), key=lambda k: Gf(xs[k]))
    assert abs(xs[i] - math.pi/2) < 2e-3 and abs(Gf(math.pi/2) - (1+math.exp(-math.pi/2))/2) < 1e-12
    # 最小値 ∫|sin t - x cos t|
    def Fa(X):
        return mp.quad(lambda s: abs(mp.sin(s) - X*mp.cos(s)), [0, mp.atan(X) if X > 0 else 0, mp.pi/2])
    for X in [-1.3, -0.2, 0.3, 0.577, 1.0, 2.5]:
        exact = 1 - X if X <= 0 else 2*mp.sqrt(1+X**2) - X - 1
        assert abs(Fa(mp.mpf(X)) - exact) < 1e-15
    vals = [(2*math.sqrt(1+(k/1e4)**2) - k/1e4 - 1, k/1e4) for k in range(1, 50000)]
    m = min(vals)
    assert abs(m[0] - (math.sqrt(3)-1)) < 1e-8 and abs(m[1] - 1/math.sqrt(3)) < 2e-4
    def Fe(X):
        if X <= 1:
            return mp.e - 1 - X
        if X >= mp.e:
            return X - mp.e + 1
        return 2*X*mp.log(X) - 3*X + 1 + mp.e
    for X in [0.5, 1.2, 1.9, 2.5, 3.0]:
        brk = [0, mp.log(X), 1] if 1 < X < mp.e else [0, 1]
        assert abs(mp.quad(lambda s: abs(mp.e**s - X), brk) - Fe(mp.mpf(X))) < 1e-15
    m = min((float(Fe(mp.mpf(0.5 + k/2000))), 0.5 + k/2000) for k in range(0, 6000))
    assert abs(m[0] - (math.sqrt(math.e)-1)**2) < 1e-7 and abs(m[1] - math.sqrt(math.e)) < 1e-3
    # ★5：∫_x^{2x} sin t / t
    Fs = lambda X: mp.si(2*X) - mp.si(X)
    assert abs(Fs(mp.mpf(1.3)) - mp.quad(lambda s: mp.sin(s)/s, [1.3, 2.6])) < 1e-20
    for p in [0.5, 1.7, 3.3, 6.0, 11.0]:
        assert abs(mp.diff(Fs, p) - mp.sin(p)*(2*mp.cos(p)-1)/p) < 1e-15
    for _ in range(300):
        X = mp.mpf(random.uniform(0.05, 200))
        assert abs(Fs(X)) <= 2/X
    assert Fs(mp.pi/3) > mp.sqrt(3)/4 > 6/(5*mp.pi) and 5*math.sqrt(3)*math.pi > 25.5 > 24
    assert abs(Fs(mp.pi/3) - mp.mpf("0.661")) < 5e-4
    xs = [0.002*k for k in range(1, 40000)]
    v = [float(Fs(X)) for X in xs[::5]]
    i = max(range(len(v)), key=lambda k: v[k]); j = min(range(len(v)), key=lambda k: v[k])
    assert abs(xs[::5][i] - math.pi/3) < 0.011 and abs(xs[::5][j] - math.pi) < 0.011
    assert max(v[k] for k in range(len(v)) if xs[::5][k] >= 5*math.pi/3) < float(Fs(mp.pi/3))
    assert Fs(mp.pi) < -1/mp.pi and Fs(2*mp.pi) > -1/mp.pi


# ---------------------------------------------------------------- 節6
SEC.append({"title": r"定積分の漸化式",
"base": r"""・$I_n$ を部分積分して $I_{n-1}$ や $I_{n-2}$ で表す（$\sin^nx=\sin^{n-1}x\cdot\sin x$ のように1つを積分する側に回す）<br>
・$I_n=\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx=\int_0^{\frac\pi2}\cos^nx\,dx$ について　$I_n=\dfrac{n-1}nI_{n-2}$（$n\geqq2$），$I_0=\dfrac\pi2$，$I_1=1$<br>
・極限は「漸化式」と「$I_n\geqq0$ や $I_{n+1}\leqq I_n$ などの大小関係（評価）」を組み合わせて求める""",
"items": [
 {"lv": 3, "title": r"$\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx$ の漸化式",
  "q": r"$I_n=\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $n\geqq2$ のとき $I_n=\dfrac{n-1}nI_{n-2}$ が成り立つことを示せ。<br>(2) $I_5$，$I_6$ を求めよ。",
  "hint": r"$\sin^nx=\sin^{n-1}x\cdot\sin x$ と分け、$\sin x=(-\cos x)'$ として部分積分する。現れる $\cos^2x$ を $1-\sin^2x$ に直すと、$I_{n-2}$ と $I_n$ が出てくる。",
  "sol": r"(1) $n\geqq2$ のとき<br>"
         r"$I_n=\displaystyle\int_0^{\frac\pi2}\sin^{n-1}x(-\cos x)'dx=\Big[-\sin^{n-1}x\cos x\Big]_0^{\frac\pi2}+(n-1)\int_0^{\frac\pi2}\sin^{n-2}x\cos^2x\,dx$<br>"
         r"$=(n-1)\displaystyle\int_0^{\frac\pi2}\sin^{n-2}x(1-\sin^2x)\,dx=(n-1)(I_{n-2}-I_n)$<br>"
         r"よって $nI_n=(n-1)I_{n-2}$，すなわち $I_n=\dfrac{n-1}nI_{n-2}$。<br>"
         r"(2) $I_0=\dfrac\pi2$，$I_1=\displaystyle\int_0^{\frac\pi2}\sin x\,dx=1$ だから<br>"
         r"$I_5=\dfrac45\cdot\dfrac23\cdot I_1=\boldsymbol{\dfrac8{15}}$，　$I_6=\dfrac56\cdot\dfrac34\cdot\dfrac12\cdot I_0=\boldsymbol{\dfrac5{32}\pi}$",
  "note": r"$x=\dfrac\pi2-t$ とおくと $\displaystyle\int_0^{\frac\pi2}\cos^nx\,dx=I_n$ もわかる。<br>一般に　$I_{2m}=\dfrac{(2m-1)(2m-3)\cdots1}{2m(2m-2)\cdots2}\cdot\dfrac\pi2$，　$I_{2m+1}=\dfrac{2m(2m-2)\cdots2}{(2m+1)(2m-1)\cdots3}$",
  "ex": r"次の定積分を求めよ。<br>(1) $\displaystyle\int_0^{\frac\pi2}\cos^7x\,dx$　　(2) $\displaystyle\int_0^{\frac\pi2}\sin^4x\cos^2x\,dx$",
  "exa": r"(1) $\dfrac{16}{35}$　(2) $\dfrac\pi{32}$"},
 {"lv": 3, "title": r"$\displaystyle\int_1^e(\log x)^ndx$ の漸化式と極限",
  "q": r"$I_n=\displaystyle\int_1^e(\log x)^n\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $n\geqq1$ のとき $I_n=e-nI_{n-1}$ が成り立つことを示せ。<br>(2) $I_3$ を求めよ。<br>(3) $\displaystyle\lim_{n\to\infty}nI_n$ を求めよ。",
  "hint": r"(1) $(\log x)^n=(x)'(\log x)^n$ として部分積分する。(3) $1\leqq x\leqq e$ で $0\leqq\log x\leqq1$ だから $I_n\geqq0$。漸化式を「$I_n$ を $I_{n+1}$ で表す式」として使うと、$I_n$ を上から評価できる。",
  "sol": r"(1) $I_n=\Big[x(\log x)^n\Big]_1^e-\displaystyle\int_1^ex\cdot\dfrac{n(\log x)^{n-1}}x\,dx=e-nI_{n-1}$<br>"
         r"(2) $I_0=e-1$，$I_1=e-I_0=1$，$I_2=e-2I_1=e-2$，$I_3=e-3I_2=\boldsymbol{6-2e}$<br>"
         r"(3) $1\leqq x\leqq e$ で $(\log x)^{n+1}\geqq0$ だから $I_{n+1}\geqq0$。(1) より $(n+1)I_n=e-I_{n+1}\leqq e$，よって $0\leqq I_n\leqq\dfrac e{n+1}$ で、$\displaystyle\lim_{n\to\infty}I_n=0$。<br>"
         r"したがって　$nI_n=\dfrac n{n+1}(e-I_{n+1})\to\boldsymbol{e}$　$(n\to\infty)$",
  "note": r"$x=e^u$ とおくと $I_n=\displaystyle\int_0^1u^ne^u\,du$ となる。このように「積分区間の端 $u=1$ の近くだけが効く」積分では、$n$ 倍するとその端での値（ここでは $e^1$）に近づく。本章の最後の節で、この近づき方をさらに詳しく調べる。",
  "ex": r"$J_n=\displaystyle\int_0^1x^ne^{-x}\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $n\geqq1$ のとき、$J_n$ を $J_{n-1}$ で表せ。　(2) $J_3$ を求めよ。　(3) $\displaystyle\lim_{n\to\infty}nJ_n$ を求めよ。",
  "exa": r"(1) $J_n=nJ_{n-1}-\dfrac1e$　(2) $6-\dfrac{16}e$　(3) $\dfrac1e$"},
 {"lv": 4, "title": r"$\displaystyle\int_0^{\frac\pi4}\tan^nx\,dx$ の漸化式と無限級数",
  "q": r"$I_n=\displaystyle\int_0^{\frac\pi4}\tan^nx\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $I_n+I_{n+2}=\dfrac1{n+1}$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}I_n=0$ を示せ。<br>(3) $\displaystyle\sum_{k=1}^\infty\dfrac{(-1)^{k-1}}{2k-1}=1-\dfrac13+\dfrac15-\dfrac17+\cdots=\dfrac\pi4$ を示せ。",
  "hint": r"(1) $\tan^nx(1+\tan^2x)=\tan^nx\cdot(\tan x)'$ に着目する。(3) (1) の式に $(-1)^{k-1}$ を掛けて加えると、隣どうしが打ち消し合う形になる。誤差が $I_{2n}$ で表されるので (2) が使える。",
  "sol": r"(1) $I_n+I_{n+2}=\displaystyle\int_0^{\frac\pi4}\tan^nx(1+\tan^2x)\,dx=\int_0^{\frac\pi4}\tan^nx(\tan x)'\,dx=\left[\dfrac{\tan^{n+1}x}{n+1}\right]_0^{\frac\pi4}=\dfrac1{n+1}$<br>"
         r"(2) $0\leqq x\leqq\dfrac\pi4$ で $\tan x\geqq0$ だから $I_n\geqq0$，$I_{n+2}\geqq0$。(1) より $0\leqq I_n\leqq\dfrac1{n+1}$ で、はさみうちの原理により $\displaystyle\lim_{n\to\infty}I_n=0$。<br>"
         r"(3) (1) で $n=2k-2$ とし、両辺に $(-1)^{k-1}$ を掛けると<br>"
         r"$\dfrac{(-1)^{k-1}}{2k-1}=(-1)^{k-1}I_{2k-2}+(-1)^{k-1}I_{2k}=(-1)^{k-1}I_{2(k-1)}-(-1)^kI_{2k}$<br>"
         r"$k=1,\ 2,\ \cdots,\ n$ として加えると　$\displaystyle\sum_{k=1}^n\dfrac{(-1)^{k-1}}{2k-1}=I_0-(-1)^nI_{2n}=\dfrac\pi4-(-1)^nI_{2n}$<br>"
         r"(2) より $I_{2n}\to0$ だから　$\displaystyle\sum_{k=1}^\infty\dfrac{(-1)^{k-1}}{2k-1}=\boldsymbol{\dfrac\pi4}$",
  "note": r"奇数番目を使うと、$I_1=\displaystyle\int_0^{\frac\pi4}\tan x\,dx=\dfrac12\log2$ と $I_{2k-1}+I_{2k+1}=\dfrac1{2k}$ から $\displaystyle\sum_{k=1}^\infty\dfrac{(-1)^{k-1}}{2k}=\dfrac12\log2$，すなわち $1-\dfrac12+\dfrac13-\cdots=\log2$ も得られる。無限級数の部分和を「（極限値）＋（積分で表された誤差）」の形にし、その積分が $0$ に近づくことを示すのが定石。",
  "ex": r"$J_n=\displaystyle\int_0^1\dfrac{x^n}{1+x}\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $J_n+J_{n+1}$ を求めよ。　(2) $\displaystyle\sum_{k=1}^\infty\dfrac{(-1)^{k-1}}k=\log2$ を示せ。",
  "exa": r"(1) $\dfrac1{n+1}$　(2) $0\leqq J_n\leqq\dfrac1{n+1}$ より $J_n\to0$。$\displaystyle\sum_{k=1}^n\dfrac{(-1)^{k-1}}k=J_0-(-1)^nJ_n=\log2-(-1)^nJ_n\to\log2$"},
 {"lv": 5, "title": r"ウォリスの公式と二項係数の評価",
  "q": r"$I_n=\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx$（$n=0,\ 1,\ 2,\ \cdots$）とする。<br>(1) $n\geqq1$ のとき $nI_nI_{n-1}=\dfrac\pi2$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\sqrt n\,I_n=\sqrt{\dfrac\pi2}$ を示せ。<br>(3) $\displaystyle\lim_{n\to\infty}\dfrac{\sqrt n\ {}_{2n}\mathrm{C}_n}{4^n}$ を求めよ。",
  "hint": r"(1) 漸化式 $I_n=\dfrac{n-1}nI_{n-2}$（本節の最初の例題）から、$nI_nI_{n-1}$ が $n$ によらないことを示す。(2) $0<\sin x<1$ から $I_n$ は減少する。これと (1) を組み合わせて $I_n^{\,2}$ を両側から挟む。(3) $I_{2n}$ を階乗で表し、(2) を $2n$ 番目に適用する。",
  "sol": r"(1) 部分積分により $I_n=\dfrac{n-1}nI_{n-2}$（$n\geqq2$）が成り立つ（本節の最初の例題）。$a_n=nI_nI_{n-1}$ とおくと、$n\geqq2$ のとき $a_n=(n-1)I_{n-2}I_{n-1}=a_{n-1}$。よって $a_n=a_1=1\cdot I_1I_0=\dfrac\pi2$。<br>"
         r"(2) $0<x<\dfrac\pi2$ で $0<\sin x<1$ より $\sin^{n+1}x<\sin^nx$ だから $0<I_{n+1}<I_n$。(1) より<br>"
         r"$\dfrac\pi2=(n+1)I_{n+1}I_n<(n+1)I_n^{\,2}$，　$\dfrac\pi2=nI_nI_{n-1}>nI_n^{\,2}$<br>"
         r"よって $\dfrac\pi{2(n+1)}<I_n^{\,2}<\dfrac\pi{2n}$，すなわち $\sqrt{\dfrac n{n+1}}\sqrt{\dfrac\pi2}<\sqrt n\,I_n<\sqrt{\dfrac\pi2}$。<br>"
         r"$n\to\infty$ のとき左辺 $\to\sqrt{\dfrac\pi2}$ だから、はさみうちの原理により $\displaystyle\lim_{n\to\infty}\sqrt n\,I_n=\sqrt{\dfrac\pi2}$。<br>"
         r"(3) 漸化式をくり返し用いると、$2n(2n-2)\cdots2=2^nn!$ より<br>"
         r"$I_{2n}=\dfrac{(2n-1)(2n-3)\cdots1}{2n(2n-2)\cdots2}\cdot\dfrac\pi2=\dfrac{(2n)!}{\{2n(2n-2)\cdots2\}^2}\cdot\dfrac\pi2=\dfrac{(2n)!}{4^n(n!)^2}\cdot\dfrac\pi2=\dfrac{{}_{2n}\mathrm{C}_n}{4^n}\cdot\dfrac\pi2$<br>"
         r"（2つ目の等号は、分母分子に $2n(2n-2)\cdots2$ を掛けた。）(2) で $n$ を $2n$ におきかえた $\sqrt{2n}\,I_{2n}\to\sqrt{\dfrac\pi2}$ を用いて<br>"
         r"$\dfrac{\sqrt n\ {}_{2n}\mathrm{C}_n}{4^n}=\dfrac{\sqrt{2n}\,I_{2n}}{\sqrt2}\cdot\dfrac2\pi\to\dfrac1{\sqrt2}\sqrt{\dfrac\pi2}\cdot\dfrac2\pi=\boldsymbol{\dfrac1{\sqrt\pi}}$",
  "note": r"(3) は ${}_{2n}\mathrm{C}_n\fallingdotseq\dfrac{4^n}{\sqrt{\pi n}}$ という二項係数の大きさの評価を与える（$n=10$ で ${}_{20}\mathrm{C}_{10}=184756$，$\dfrac{4^{10}}{\sqrt{10\pi}}\fallingdotseq187079$）。また $I_{2n+1}<I_{2n}<I_{2n-1}$ を同様に用いると $\dfrac\pi2=\displaystyle\lim_{n\to\infty}\dfrac{2\cdot2}{1\cdot3}\cdot\dfrac{4\cdot4}{3\cdot5}\cdots\dfrac{2n\cdot2n}{(2n-1)(2n+1)}$（ウォリスの公式）が得られる。",
  "ex": r"$I_n=\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx$，$P_n=\dfrac{2\cdot4\cdot6\cdots(2n)}{1\cdot3\cdot5\cdots(2n-1)}$ とする。$I_{2n+1}$ を $P_n$ で表し、$\displaystyle\lim_{n\to\infty}\dfrac{P_n^{\,2}}n$ を求めよ。ただし $\displaystyle\lim_{n\to\infty}\sqrt n\,I_n=\sqrt{\dfrac\pi2}$ を用いてよい。",
  "exa": r"$I_{2n+1}=\dfrac{P_n}{2n+1}$，$\displaystyle\lim_{n\to\infty}\dfrac{P_n^{\,2}}n=\pi$"},
]})


def _v6():
    # sin^n
    def Isin(n):
        return integrate(sin(x)**n, (x, 0, pi/2))
    I = [pi/2, S(1)]
    for n in range(2, 12):
        I.append(Rational(n-1, n)*I[n-2])
    for n in range(0, 9):
        assert simplify(Isin(n) - I[n]) == 0
    assert I[5] == Rational(8, 15) and simplify(I[6] - 5*pi/32) == 0
    _Q(cos(x)**7, 0, pi/2, Rational(16, 35))
    _Q(sin(x)**4*cos(x)**2, 0, pi/2, pi/32)
    assert simplify(I[4] - I[6] - pi/32) == 0
    # (log x)^n と x^n e^{-x}
    L = [E - 1]
    for n in range(1, 8):
        L.append(E - n*L[n-1])
    for n in range(0, 6):
        _Q(log(x)**n, 1, E, L[n])
    assert simplify(L[3] - (6 - 2*E)) == 0
    J = [1 - 1/E]
    for n in range(1, 8):
        J.append(n*J[n-1] - 1/E)
    for n in range(0, 6):
        _Q(x**n*exp(-x), 0, 1, J[n])
    assert simplify(J[3] - (6 - 16/E)) == 0
    for n in [50, 200, 1000]:   # n I_n → e，n J_n → 1/e（数値積分で確認）
        In = mp.quad(lambda s: mp.log(s)**n, [1, mp.e - mp.mpf(1)/n, mp.e])
        Jn = mp.quad(lambda s: s**n*mp.e**(-s), [0, 1 - mp.mpf(1)/n, 1])
        assert abs(n*In - mp.e) < 3*mp.e/n and abs(n*Jn - 1/mp.e) < 3/n
    # tan^n
    T = [pi/4, log(2)/2]
    for n in range(0, 10):
        T.append(1/S(n+1) - T[n])
    for n in range(0, 8):
        _Q(tan(x)**n, 0, pi/4, T[n], sym=(n <= 3))
    for n in range(1, 30):
        part = sum(Fr((-1)**(k-1), 2*k-1) for k in range(1, n+1))
        I2n = mp.quad(lambda s: mp.tan(s)**(2*n), [0, mp.pi/4])
        assert abs(mp.mpf(part.numerator)/part.denominator - (mp.pi/4 - (-1)**n*I2n)) < 1e-20
        assert 0 <= I2n <= mp.mpf(1)/(2*n+1)
        part2 = sum(Fr((-1)**(k-1), k) for k in range(1, n+1))
        Jn = mp.quad(lambda s: s**n/(1+s), [0, 1])
        assert abs(mp.mpf(part2.numerator)/part2.denominator - (mp.log(2) - (-1)**n*Jn)) < 1e-20
        Jn1 = mp.quad(lambda s: s**(n+1)/(1+s), [0, 1])
        assert abs(Jn + Jn1 - mp.mpf(1)/(n+1)) < 1e-20
    # Wallis
    for n in range(1, 11):
        assert simplify(n*I[n]*I[n-1] - pi/2) == 0
    for n in range(1, 6):
        assert simplify(I[2*n] - binomial(2*n, n)/4**n*pi/2) == 0
        Pn = Fr(1)
        for k in range(1, n+1):
            Pn *= Fr(2*k, 2*k-1)
        assert simplify(I[2*n+1] - Rational(Pn.numerator, Pn.denominator)/(2*n+1)) == 0
    for n in [10, 100, 1000, 10000]:
        In = mp.pi/2*mp.binomial(2*n, n)/mp.mpf(4)**n          # I_{2n}
        assert abs(mp.sqrt(2*n)*In - mp.sqrt(mp.pi/2)) < 1/mp.mpf(n)
        assert abs(mp.sqrt(n)*mp.binomial(2*n, n)/mp.mpf(4)**n - 1/mp.sqrt(mp.pi)) < 1/mp.mpf(n)
        Pn2 = (mp.mpf(4)**n/mp.binomial(2*n, n))**2            # P_n = 4^n / C(2n,n)
        assert abs(Pn2/n - mp.pi) < 3/mp.mpf(n)
    assert binomial(20, 10) == 184756 and round(4**10/math.sqrt(10*math.pi)) == 187079


# ---------------------------------------------------------------- 節7


def _fig_tri():
    """円周の12等分点と三角形 ABC（弧の長さ 5, 3, 4）。"""
    g = _G(150, 150, (-1.3, 1.3), (-1.3, 1.3), m=5)
    n = 12
    P = [(math.cos(2*math.pi*k/n), math.sin(2*math.pi*k/n)) for k in range(n)]
    A, B, Cc = P[0], P[5], P[8]
    g.poly([A, B, Cc], fill=CF, col=C1, w=1.2)
    g.circle(0, 0, 1, col="#444", w=0.9)
    for v in (A, B, Cc):
        g.seg((0, 0), v, col=C2, w=0.9)
    for p in P:
        g.pt(*p, r=1.5)
    g.pt(0, 0, r=1.6)
    g.text(0.06, -0.2, "O", it=True, size=11)
    for (px, py), lab in ((A, "A"), (B, "B"), (Cc, "C")):
        g.text(1.17*px - 0.05, 1.17*py - 0.06, lab, it=True, size=11)
    return g.svg()


SEC.append({"title": r"区分求積法",
"base": r"""・$f(x)$ が連続のとき $\displaystyle\lim_{n\to\infty}\dfrac1n\sum_{k=1}^nf\!\left(\dfrac kn\right)=\lim_{n\to\infty}\dfrac1n\sum_{k=0}^{n-1}f\!\left(\dfrac kn\right)=\int_0^1f(x)\,dx$<br>
・$\dfrac1n$ をくくり出し、残りを $\dfrac kn$ の式にする。和が $k=1$ から $2n$ までなら積分区間は $[0,\ 2]$ になる<br>
・積の極限は対数をとって和に直す。ガウス記号などを含むときは、不等式ではさんでから区分求積法を使う""",
"items": [
 {"lv": 2, "title": r"区分求積法の基本",
  "q": r"次の極限値を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^n\dfrac n{n^2+k^2}$　　(2) $\displaystyle\lim_{n\to\infty}\left(\dfrac1{n+1}+\dfrac1{n+2}+\cdots+\dfrac1{3n}\right)$　　(3) $\displaystyle\lim_{n\to\infty}\dfrac1{n^2}\sum_{k=1}^nk\sin\dfrac{k\pi}n$",
  "hint": r"$\dfrac1n$ をくくり出し、残りを $\dfrac kn$ だけの式 $f\left(\dfrac kn\right)$ にする。(2) は $\displaystyle\sum_{k=1}^{2n}\dfrac1{n+k}$ で、$\dfrac kn$ が $0$ から $2$ まで動くので積分区間は $[0,\ 2]$ になる。",
  "sol": r"(1) $\displaystyle\sum_{k=1}^n\dfrac n{n^2+k^2}=\dfrac1n\sum_{k=1}^n\dfrac1{1+\left(\frac kn\right)^2}\to\int_0^1\dfrac{dx}{1+x^2}=\boldsymbol{\dfrac\pi4}$（$x=\tan\theta$ とおいて計算）<br>"
         r"(2) $\displaystyle\sum_{k=1}^{2n}\dfrac1{n+k}=\dfrac1n\sum_{k=1}^{2n}\dfrac1{1+\frac kn}\to\int_0^2\dfrac{dx}{1+x}=\Big[\log(1+x)\Big]_0^2=\boldsymbol{\log3}$<br>"
         r"(3) $\displaystyle\dfrac1{n^2}\sum_{k=1}^nk\sin\dfrac{k\pi}n=\dfrac1n\sum_{k=1}^n\dfrac kn\sin\dfrac{k\pi}n\to\int_0^1x\sin\pi x\,dx$<br>"
         r"$=\left[-\dfrac{x\cos\pi x}\pi\right]_0^1+\dfrac1\pi\displaystyle\int_0^1\cos\pi x\,dx=\dfrac1\pi+0=\boldsymbol{\dfrac1\pi}$",
  "note": r"(2) の $\dfrac1n\displaystyle\sum_{k=1}^{2n}f\left(\dfrac kn\right)$ は、区間 $[0,\ 2]$ を幅 $\dfrac1n$ の $2n$ 個の小区間に分けてつくった長方形の面積の和であり、その極限が $\displaystyle\int_0^2f(x)\,dx$ である。",
  "ex": r"(1) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^n\dfrac k{n^2+k^2}$ を求めよ。<br>(2) 半径 $1$ の円に内接する正 $n$ 角形の頂点を順に $\mathrm{P}_0,\ \mathrm{P}_1,\ \cdots,\ \mathrm{P}_{n-1}$ とする。$\displaystyle\lim_{n\to\infty}\dfrac1n\sum_{k=1}^{n-1}\mathrm{P}_0\mathrm{P}_k$ を求めよ。",
  "exa": r"(1) $\dfrac12\log2$　(2) $\dfrac4\pi$（$\mathrm{P}_0\mathrm{P}_k=2\sin\dfrac{k\pi}n$）"},
 {"lv": 3, "title": r"積の極限（対数をとって区分求積法）",
  "q": r"極限値 $\displaystyle\lim_{n\to\infty}\dfrac1n\sqrt[n]{(n+1)(n+2)\cdots(2n)}$ を求めよ。",
  "hint": r"積の形のままでは区分求積法が使えない。対数をとると積が和になり、$\dfrac1n\displaystyle\sum_{k=1}^n\log\left(1+\dfrac kn\right)$ の形になる。",
  "sol": r"$a_n=\dfrac1n\sqrt[n]{(n+1)(n+2)\cdots(2n)}=\left\{\left(1+\dfrac1n\right)\left(1+\dfrac2n\right)\cdots\left(1+\dfrac nn\right)\right\}^{\frac1n}$ とおくと<br>"
         r"$\log a_n=\dfrac1n\displaystyle\sum_{k=1}^n\log\left(1+\dfrac kn\right)\to\int_0^1\log(1+x)\,dx=\Big[(1+x)\log(1+x)-x\Big]_0^1=2\log2-1$<br>"
         r"よって　$\displaystyle\lim_{n\to\infty}a_n=e^{2\log2-1}=\boldsymbol{\dfrac4e}$",
  "note": r"$\dfrac1n$ を $\sqrt[n]{\ }$ の中に入れると $\dfrac1{n^n}$ になり、$n$ 個の因数それぞれを $n$ で割る形になる。積や累乗根の極限は $\log$ をとって和にし、最後に $e^x$ の連続性で戻す。",
  "ex": r"極限値 $\displaystyle\lim_{n\to\infty}\dfrac1{n^2}\sqrt[n]{(n^2+1^2)(n^2+2^2)\cdots(n^2+n^2)}$ を求めよ。",
  "exa": r"$2e^{\frac\pi2-2}$"},
 {"lv": 4, "title": r"区分求積法と確率（ガウス記号とはさみうち）",
  "q": r"$n$ を自然数とする。$1$ から $n$ までの整数の中から、重複を許して無作為に $a,\ b$ を選ぶ（$n^2$ 通りが同様に確からしい）。$a^2+b^2\leqq n^2$ となる確率を $p_n$ とするとき、$\displaystyle\lim_{n\to\infty}p_n$ を求めよ。",
  "hint": r"$a$ を固定して $b$ の個数を数えると $\left[\sqrt{n^2-a^2}\right]$ 個（$[\ ]$ はガウス記号）。ガウス記号のままでは区分求積法が使えないので、$u-1<[u]\leqq u$ ではさむ。",
  "sol": r"$a$（$1\leqq a\leqq n$）を固定すると、条件を満たす $b$ は $1\leqq b\leqq\sqrt{n^2-a^2}$ を満たす整数で、$\sqrt{n^2-a^2}\leqq n$ だからその個数は $\left[\sqrt{n^2-a^2}\right]$。よって<br>"
         r"$p_n=\dfrac1{n^2}\displaystyle\sum_{a=1}^n\left[\sqrt{n^2-a^2}\right]$<br>"
         r"$u-1<[u]\leqq u$ より<br>"
         r"$\dfrac1{n^2}\displaystyle\sum_{a=1}^n\left(\sqrt{n^2-a^2}-1\right)<p_n\leqq\dfrac1{n^2}\sum_{a=1}^n\sqrt{n^2-a^2}$<br>"
         r"ここで、右辺は $\dfrac1n\displaystyle\sum_{a=1}^n\sqrt{1-\left(\dfrac an\right)^2}\to\int_0^1\sqrt{1-x^2}\,dx=\dfrac\pi4$（半径 $1$ の四分円の面積）<br>"
         r"であり、左辺は（右辺）$-\dfrac1n\to\dfrac\pi4$。はさみうちの原理により　$\displaystyle\lim_{n\to\infty}p_n=\boldsymbol{\dfrac\pi4}$",
  "note": r"点 $(a,\ b)$ は正方形内の格子点で、$p_n$ は「四分円の中に入る格子点の割合」である。その極限が面積比 $\dfrac\pi4$ になることを、ガウス記号の評価と区分求積法で厳密に示した。練習のように $b$ の上限（$\dfrac{n^2}{2a}$ など）が $n$ を超えることがある場合は、$a$ の範囲を分けて数える。",
  "ex": r"$n$ を自然数とする。$1$ から $n$ までの整数の中から、重複を許して無作為に $a,\ b$ を選ぶ。$2ab\leqq n^2$ となる確率を $q_n$ とするとき、$\displaystyle\lim_{n\to\infty}q_n$ を求めよ。",
  "exa": r"$\dfrac{1+\log2}2$（$a\leqq\dfrac n2$ ではすべての $b$ が適し、$a>\dfrac n2$ では $\left[\dfrac{n^2}{2a}\right]$ 個）"},
 {"lv": 5, "title": r"円周の等分点でつくる三角形の面積の期待値",
  "q": _fig_tri() + r"$n\geqq3$ とする。半径 $1$ の円周を $n$ 等分する $n$ 個の点から異なる3点を無作為に選び、それらを頂点とする三角形の面積の期待値を $E_n$ とする。$\displaystyle\lim_{n\to\infty}E_n$ を求めよ。",
  "hint": r"円の中心を $\mathrm{O}$、3頂点を反時計回りに $\mathrm{A},\ \mathrm{B},\ \mathrm{C}$ とすると、面積は3つの弧の中心角 $\theta_1,\ \theta_2,\ \theta_3$ を用いて $\dfrac12(\sin\theta_1+\sin\theta_2+\sin\theta_3)$ と表せる。面積の総和を、三角形ごとに数える代わりに「弧ごと」に数え直すと1重の和になり、区分求積法が使える。",
  "sol": r"等分点を反時計回りに $\mathrm{P}_0,\ \mathrm{P}_1,\ \cdots,\ \mathrm{P}_{n-1}$ とし、円の中心を $\mathrm{O}$ とする。選んだ3点を反時計回りに $\mathrm{A},\ \mathrm{B},\ \mathrm{C}$ とし、反時計回りの弧 $\mathrm{AB}$，$\mathrm{BC}$，$\mathrm{CA}$ が等分された弧をそれぞれ $i,\ j,\ l$ 個含むとする（$i+j+l=n$，$i,\ j,\ l\geqq1$）。<br>"
         r"$\triangle\mathrm{OAB}$，$\triangle\mathrm{OBC}$，$\triangle\mathrm{OCA}$ の面積を、中心角が $\pi$ を超えるときは負として加えると $\triangle\mathrm{ABC}$ になる（$\mathrm{O}$ が三角形の外にあっても成り立つ）から<br>"
         r"$\triangle\mathrm{ABC}=\dfrac12\left(\sin\dfrac{2\pi i}n+\sin\dfrac{2\pi j}n+\sin\dfrac{2\pi l}n\right)$<br>"
         r"【総和を弧ごとに数える】三角形は ${}_n\mathrm{C}_3$ 個ある。「三角形とその弧の1つ」の組は、弧の始点 $\mathrm{P}_s$（$n$ 通り）、弧に含まれる等分弧の個数 $i$（$1\leqq i\leqq n-2$）、残りの頂点（弧の外にある $n-1-i$ 個の点から1つ）を決めると1通りに定まる。よって、面積の総和を $S_n$ とすると<br>"
         r"$S_n=\dfrac12\displaystyle\sum_{i=1}^{n-2}n(n-1-i)\sin\dfrac{2\pi i}n$，　$E_n=\dfrac{S_n}{{}_n\mathrm{C}_3}=\dfrac3{(n-1)(n-2)}\displaystyle\sum_{i=1}^{n-2}(n-1-i)\sin\dfrac{2\pi i}n$<br>"
         r"【区分求積】$n-1-i=n\left(1-\dfrac in\right)-1$ と分けると<br>"
         r"$E_n=\dfrac{3n^2}{(n-1)(n-2)}\left\{\dfrac1n\displaystyle\sum_{i=1}^{n-2}\left(1-\dfrac in\right)\sin\dfrac{2\pi i}n-\dfrac1{n^2}\sum_{i=1}^{n-2}\sin\dfrac{2\pi i}n\right\}$<br>"
         r"中かっこの中の第2項の絶対値は $\dfrac{n-2}{n^2}$ 以下で $0$ に収束する。第1項は、$i=n-1,\ n$ の項（絶対値はいずれも $\dfrac1{n^2}$ 以下）を補った $\dfrac1n\displaystyle\sum_{i=1}^n\left(1-\dfrac in\right)\sin\dfrac{2\pi i}n$ と同じ極限をもち<br>"
         r"$\to\displaystyle\int_0^1(1-x)\sin2\pi x\,dx=\left[-\dfrac{(1-x)\cos2\pi x}{2\pi}\right]_0^1-\int_0^1\dfrac{\cos2\pi x}{2\pi}dx=\dfrac1{2\pi}$<br>"
         r"$\dfrac{3n^2}{(n-1)(n-2)}\to3$ だから　$\displaystyle\lim_{n\to\infty}E_n=\boldsymbol{\dfrac3{2\pi}}$",
  "note": r"実際に和を計算すると $E_n=\dfrac{3n}{2(n-1)(n-2)\tan\frac\pi n}$ となり（$n=3$ で正三角形の面積 $\dfrac{3\sqrt3}4$）、確かに $\dfrac3{2\pi}\fallingdotseq0.477$ に近づく。$\dfrac3{2\pi}$ は「円周上に独立に3点を一様にとったときの三角形の面積の期待値」でもある。三角形の面積の和を弧ごとに数え直すところが最大の山場。",
  "ex": r"$n\geqq3$ とする。半径 $1$ の円周を $n$ 等分する $n$ 個の点から異なる3点を無作為に選び、それらを頂点とする三角形の周の長さの期待値を $L_n$ とする。$\displaystyle\lim_{n\to\infty}L_n$ を求めよ。",
  "exa": r"$\dfrac{12}\pi$（$L_n=\dfrac6{(n-1)(n-2)}\displaystyle\sum_{i=1}^{n-2}(n-1-i)\cdot2\sin\dfrac{i\pi}n\to12\int_0^1(1-x)\sin\pi x\,dx$）"},
]})


def _v7():
    # 基本
    _Q(1/(1+x**2), 0, 1, pi/4)
    _Q(1/(1+x), 0, 2, log(3))
    _Q(x*sin(pi*x), 0, 1, 1/pi)
    _Q(x/(1+x**2), 0, 1, log(2)/2)
    _Q(2*sin(pi*x), 0, 1, 4/pi)
    n = 20000
    assert abs(sum(n/(n*n+k*k) for k in range(1, n+1)) - math.pi/4) < 1/n
    assert abs(sum(1/(n+k) for k in range(1, 2*n+1)) - math.log(3)) < 1/n
    assert abs(sum(k*math.sin(k*math.pi/n) for k in range(1, n+1))/n**2 - 1/math.pi) < 1/n
    assert abs(sum(k/(n*n+k*k) for k in range(1, n+1)) - math.log(2)/2) < 1/n
    assert abs(sum(2*math.sin(k*math.pi/n) for k in range(1, n))/n - 4/math.pi) < 1/n
    for m in [5, 7, 12]:   # 弦の長さ P0Pk = 2 sin(kπ/m)
        for k in range(1, m):
            d = math.dist((1, 0), (math.cos(2*math.pi*k/m), math.sin(2*math.pi*k/m)))
            assert abs(d - 2*math.sin(k*math.pi/m)) < 1e-12
    # 積の極限
    _Q(log(1+x), 0, 1, 2*log(2) - 1)
    for n in [1000, 100000]:
        la = (math.lgamma(2*n+1) - math.lgamma(n+1))/n - math.log(n)
        assert abs(math.exp(la) - 4/math.e) < 5/n
    _Q(log(1+x**2), 0, 1, log(2) - 2 + pi/2)
    assert abs(N(exp(log(2) - 2 + pi/2) - 2*exp(pi/2 - 2))) < 1e-15
    n = 100000
    la = sum(math.log(1 + (k/n)**2) for k in range(1, n+1))/n
    assert abs(math.exp(la) - 2*math.exp(math.pi/2 - 2)) < 1e-4
    # 格子点の確率
    _Q(sqrt(1-x**2), 0, 1, pi/4)
    for n in [10, 57, 300, 3000]:
        cnt = sum(math.isqrt(n*n - a*a) for a in range(1, n+1))
        brute = sum(1 for a in range(1, n+1) for b in range(1, n+1) if a*a+b*b <= n*n) if n <= 300 else cnt
        assert cnt == brute
        R = sum(math.sqrt(n*n - a*a) for a in range(1, n+1))/n**2
        assert R - 1/n < cnt/n**2 <= R + 1e-12
    n = 3000
    assert abs(sum(math.isqrt(n*n - a*a) for a in range(1, n+1))/n**2 - math.pi/4) < 2/n
    for n in [10, 41, 200]:
        brute = sum(1 for a in range(1, n+1) for b in range(1, n+1) if 2*a*b <= n*n)
        assert brute == sum(min(n, (n*n)//(2*a)) for a in range(1, n+1))
    n = 200000
    q = sum(min(n, (n*n)//(2*a)) for a in range(1, n+1))/n**2
    assert abs(q - (1 + math.log(2))/2) < 2e-5
    # ★5 三角形の面積の期待値（総当たり）
    from itertools import combinations
    for n in range(3, 15):
        P = [(math.cos(2*math.pi*k/n), math.sin(2*math.pi*k/n)) for k in range(n)]
        tot = per = 0.0
        for a, b, c in combinations(range(n), 3):
            (x1, y1), (x2, y2), (x3, y3) = P[a], P[b], P[c]
            ar = abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))/2
            i, j, l = b-a, c-b, n-(c-a)
            assert abs(ar - (math.sin(2*math.pi*i/n)+math.sin(2*math.pi*j/n)+math.sin(2*math.pi*l/n))/2) < 1e-12
            tot += ar
            per += math.dist(P[a], P[b]) + math.dist(P[b], P[c]) + math.dist(P[c], P[a])
        En = tot/math.comb(n, 3)
        f1 = 3/((n-1)*(n-2))*sum((n-1-i)*math.sin(2*math.pi*i/n) for i in range(1, n-1))
        f2 = 3*n/(2*(n-1)*(n-2)*math.tan(math.pi/n))
        assert abs(En - f1) < 1e-12 and abs(En - f2) < 1e-12
        assert abs(tot - 0.5*sum(n*(n-1-i)*math.sin(2*math.pi*i/n) for i in range(1, n-1))) < 1e-9
        Ln = per/math.comb(n, 3)
        assert abs(Ln - 6/((n-1)*(n-2))*sum((n-1-i)*2*math.sin(i*math.pi/n) for i in range(1, n-1))) < 1e-12
    assert abs(3*3/(2*2*1*math.tan(math.pi/3)) - 3*math.sqrt(3)/4) < 1e-12
    _Q((1-x)*sin(2*pi*x), 0, 1, 1/(2*pi))
    _Q((1-x)*sin(pi*x), 0, 1, 1/pi)
    n = 10**6
    assert abs(3*n/(2*(n-1)*(n-2)*math.tan(math.pi/n)) - 3/(2*math.pi)) < 1e-5
    n = 20000
    Ln = 6/((n-1)*(n-2))*sum((n-1-i)*2*math.sin(i*math.pi/n) for i in range(1, n-1))
    assert abs(Ln - 12/math.pi) < 1e-3 and abs(3/(2*math.pi) - 0.477) < 5e-4


# ---------------------------------------------------------------- 節8


def _fig_harm():
    """y=1/x と、幅1の長方形（上：高さ 1/k，下：高さ 1/(k+1)）。"""
    g = _G(200, 128, (-0.35, 5.9), (-0.16, 1.22), m=8)
    for k in range(1, 5):
        g.poly([(k, 0), (k+1, 0), (k+1, 1/k), (k, 1/k)], fill="none", col=C2, w=0.9, dash="3,2")
        g.poly([(k, 0), (k+1, 0), (k+1, 1/(k+1)), (k, 1/(k+1))], fill=CF, col=C1, w=0.7)
    g.axes()
    g.curve(lambda v: 1/v, 0.84, 5.7, col=C1, w=1.4)
    for k in range(1, 6):
        g.text(k, -0.13, str(k), anchor="middle", size=10)
    g.text(1.25, 1.12, "y=1/x", it=True, size=10, col=C1)
    return g.svg()


SEC.append({"title": r"定積分と不等式・極限",
"base": r"""・$a\leqq x\leqq b$ で $f(x)\leqq g(x)$ なら $\displaystyle\int_a^bf(x)\,dx\leqq\int_a^bg(x)\,dx$（$f,\ g$ が連続で $f\neq g$ となる点があれば等号は成り立たない）<br>
・和の評価：$f(x)$ が減少関数なら $f(k+1)<\displaystyle\int_k^{k+1}f(x)\,dx<f(k)$。これを $k$ について加える<br>
・$\displaystyle\left|\int_a^bf(x)\,dx\right|\leqq\int_a^b|f(x)|\,dx$，　$\displaystyle\int_a^b\{f(x)-g(x)\}^2dx\geqq0$（等号は $f=g$ のとき）""",
"items": [
 {"lv": 3, "title": r"定積分と和の不等式（面積の比較）",
  "q": r"(1) $n\geqq2$ のとき、$\log(n+1)<1+\dfrac12+\dfrac13+\cdots+\dfrac1n<1+\log n$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\dfrac1{\log n}\left(1+\dfrac12+\cdots+\dfrac1n\right)$ を求めよ。",
  "hint": r"$\displaystyle\sum\dfrac1k$ は計算できないが、$\displaystyle\int\dfrac{dx}x$ は計算できる。$y=\dfrac1x$ のグラフの下の面積と、幅 $1$ の長方形の面積を比べる（図）。",
  "sol": _fig_harm() + r"$S_n=1+\dfrac12+\cdots+\dfrac1n$ とおく。$k\leqq x\leqq k+1$ で $\dfrac1{k+1}\leqq\dfrac1x\leqq\dfrac1k$（等号は端点のみ）だから<br>"
         r"$\dfrac1{k+1}<\displaystyle\int_k^{k+1}\dfrac{dx}x<\dfrac1k$　…①<br>"
         r"(1) ①の右側の不等式を $k=1,\ 2,\ \cdots,\ n$ について加えると $\displaystyle\int_1^{n+1}\dfrac{dx}x<S_n$，すなわち $\log(n+1)<S_n$。<br>"
         r"①の左側の不等式を $k=1,\ 2,\ \cdots,\ n-1$ について加えると $S_n-1<\displaystyle\int_1^n\dfrac{dx}x=\log n$，すなわち $S_n<1+\log n$。<br>"
         r"(2) (1) より $\dfrac{\log(n+1)}{\log n}<\dfrac{S_n}{\log n}<\dfrac1{\log n}+1$。<br>"
         r"$\dfrac{\log(n+1)}{\log n}=1+\dfrac{\log\left(1+\frac1n\right)}{\log n}\to1$，$\dfrac1{\log n}\to0$ だから、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}\dfrac{S_n}{\log n}=\boldsymbol{1}$",
  "note": r"(1) から $S_n$ は $\log n$ と同じ速さで限りなく大きくなる（調和級数は発散する）。さらに $S_n-\log n$ は減少し（①の左側による）、$0$ と $1$ の間の値に収束する（その値はオイラーの定数 $0.577\cdots$）。",
  "ex": r"(1) $n\geqq2$ のとき、$2\sqrt{n+1}-2<\displaystyle\sum_{k=1}^n\dfrac1{\sqrt k}<2\sqrt n-1$ を示せ。<br>(2) $\displaystyle\sum_{k=1}^{10000}\dfrac1{\sqrt k}$ の整数部分を求めよ。",
  "exa": r"(1) $\dfrac1{\sqrt{k+1}}<\displaystyle\int_k^{k+1}\dfrac{dx}{\sqrt x}<\dfrac1{\sqrt k}$ を加える　(2) $198$"},
 {"lv": 4, "title": r"定積分の最小値（$\displaystyle\int(f-g)^2dx\geqq0$ の利用）",
  "q": r"$0\leqq x\leqq1$ で連続な関数 $f(x)$ が $\displaystyle\int_0^1f(x)\,dx=1$，$\displaystyle\int_0^1xf(x)\,dx=1$ を満たしている。$\displaystyle\int_0^1\{f(x)\}^2dx$ の最小値と、最小値を与える $f(x)$ を求めよ。",
  "hint": r"$\displaystyle\int_0^1\{f(x)-g(x)\}^2dx\geqq0$ を展開すると $\displaystyle\int f^2dx\geqq2\int fg\,dx-\int g^2dx$。$g(x)=px+q$ とすれば $\displaystyle\int fg\,dx=p\int xf\,dx+q\int f\,dx$ は条件だけで決まる。さらに $g$ 自身が条件を満たすように $p,\ q$ を選べば、等号が成り立つ $f$（$f=g$）が存在する。",
  "sol": r"$g(x)=px+q$ が条件を満たすように定める。$\displaystyle\int_0^1g\,dx=\dfrac p2+q=1$，$\displaystyle\int_0^1xg\,dx=\dfrac p3+\dfrac q2=1$ を解いて $p=6$，$q=-2$，すなわち $g(x)=6x-2$。<br>"
         r"条件を満たす任意の $f(x)$ に対して<br>"
         r"$\displaystyle\int_0^1f(x)g(x)\,dx=6\int_0^1xf(x)\,dx-2\int_0^1f(x)\,dx=4$，　$\displaystyle\int_0^1\{g(x)\}^2dx=\int_0^1(36x^2-24x+4)\,dx=4$<br>"
         r"であるから<br>"
         r"$0\leqq\displaystyle\int_0^1\{f(x)-g(x)\}^2dx=\int_0^1\{f(x)\}^2dx-2\cdot4+4$<br>"
         r"よって $\displaystyle\int_0^1\{f(x)\}^2dx\geqq4$。等号は、連続関数 $\{f(x)-g(x)\}^2\ (\geqq0)$ の積分が $0$ のとき、すなわち常に $f(x)=g(x)$ のときに限る。<br>"
         r"したがって　最小値 $\boldsymbol{4}$（$\boldsymbol{f(x)=6x-2}$ のとき）",
  "note": r"シュワルツの不等式 $\displaystyle\left(\int_0^1fg\,dx\right)^2\leqq\int_0^1f^2dx\int_0^1g^2dx$ を使っても、$16\leqq4\displaystyle\int_0^1f^2dx$ から同じ結果が得られる。シュワルツの不等式自体は、$s$ の2次式 $\displaystyle\int_0^1(sf-g)^2dx\geqq0$ の判別式から証明できる。",
  "ex": r"$0\leqq x\leqq1$ で連続な関数 $f(x)$ が $\displaystyle\int_0^1f(x)\,dx=0$，$\displaystyle\int_0^1xf(x)\,dx=1$ を満たすとき、$\displaystyle\int_0^1\{f(x)\}^2dx$ の最小値と、最小値を与える $f(x)$ を求めよ。",
  "exa": r"最小値 $12$（$f(x)=12x-6$ のとき）"},
 {"lv": 4, "title": r"$|\sin nx|$ を含む定積分の極限",
  "q": r"自然数 $n$ に対して $a_n=\displaystyle\int_0^\pi e^{-x}|\sin nx|\,dx$ とする。$\displaystyle\lim_{n\to\infty}a_n$ を求めよ。",
  "hint": r"$|\sin nx|$ は周期 $\dfrac\pi n$ の関数。区間 $[0,\ \pi]$ を $n$ 等分し、各小区間で $x=\dfrac{(k-1)\pi}n+t$ とおくと、どの区間の積分も同じ積分 $\displaystyle\int_0^{\frac\pi n}e^{-t}\sin nt\,dt$ の定数倍になり、和は等比数列の和になる。",
  "sol": r"$k=1,\ 2,\ \cdots,\ n$ に対し、$\dfrac{(k-1)\pi}n\leqq x\leqq\dfrac{k\pi}n$ の部分で $x=\dfrac{(k-1)\pi}n+t$ とおくと、$0\leqq t\leqq\dfrac\pi n$ で $|\sin nx|=|\sin(nt+(k-1)\pi)|=\sin nt$ だから<br>"
         r"$\displaystyle\int_{\frac{(k-1)\pi}n}^{\frac{k\pi}n}e^{-x}|\sin nx|\,dx=e^{-\frac{(k-1)\pi}n}b_n$，　ただし $b_n=\displaystyle\int_0^{\frac\pi n}e^{-t}\sin nt\,dt$<br>"
         r"よって $a_n=b_n\displaystyle\sum_{k=1}^ne^{-\frac{(k-1)\pi}n}=b_n\cdot\dfrac{1-e^{-\pi}}{1-e^{-\frac\pi n}}$。<br>"
         r"$\{-e^{-t}(\sin nt+n\cos nt)\}'=(n^2+1)e^{-t}\sin nt$ より<br>"
         r"$b_n=\left[-\dfrac{e^{-t}(\sin nt+n\cos nt)}{n^2+1}\right]_0^{\frac\pi n}=\dfrac{n\left(1+e^{-\frac\pi n}\right)}{n^2+1}$<br>"
         r"したがって $a_n=(1-e^{-\pi})\cdot\dfrac{n^2}{n^2+1}\cdot\left(1+e^{-\frac\pi n}\right)\cdot\dfrac1{n\left(1-e^{-\frac\pi n}\right)}$。<br>"
         r"$h=\dfrac\pi n$ とおくと $n\left(1-e^{-\frac\pi n}\right)=\pi\cdot\dfrac{1-e^{-h}}h\to\pi$（$h\to0$。$e^x$ の $x=0$ における微分係数が $1$ であることによる）だから<br>"
         r"$\displaystyle\lim_{n\to\infty}a_n=(1-e^{-\pi})\cdot1\cdot2\cdot\dfrac1\pi=\boldsymbol{\dfrac{2(1-e^{-\pi})}\pi}$",
  "note": r"結果は $\dfrac2\pi\displaystyle\int_0^\pi e^{-x}dx$ に等しい。$|\sin nx|$ の1周期での平均値は $\dfrac2\pi$ であり、$n$ が大きいと $|\sin nx|$ は激しく振動して、その平均値でおきかえたものに近づく。一般に、連続関数 $f(x)$ に対して $\displaystyle\lim_{n\to\infty}\int_a^bf(x)|\sin nx|\,dx=\dfrac2\pi\int_a^bf(x)\,dx$ が成り立つ。",
  "ex": r"自然数 $n$ に対して $a_n=\displaystyle\int_0^1e^x|\sin n\pi x|\,dx$ とする。$\displaystyle\lim_{n\to\infty}a_n$ を求めよ。",
  "exa": r"$\dfrac{2(e-1)}\pi$"},
 {"lv": 5, "title": r"定積分による $\pi$ の評価",
  "q": r"(1) 定積分 $\displaystyle I=\int_0^1\dfrac{x^4(1-x)^4}{1+x^2}\,dx$ を求めよ。<br>(2) $3.141<\pi<3.142$ を示せ。",
  "hint": r"(1) 分子を $1+x^2$ で割ると、$\pi$ が $\dfrac{22}7$ との差として現れる。(2) 被積分関数の $\dfrac1{1+x^2}$ を上下から多項式ではさみ、多項式の積分で $I$ を評価する。上からは $\dfrac1{1+x^2}<1$ で足りるが、下からは精度のよい評価が必要になる。",
  "sol": r"(1) $x^4(1-x)^4=x^8-4x^7+6x^6-4x^5+x^4$ を $x^2+1$ で割ると<br>"
         r"$x^4(1-x)^4=(x^2+1)(x^6-4x^5+5x^4-4x^2+4)-4$<br>"
         r"よって $I=\displaystyle\int_0^1(x^6-4x^5+5x^4-4x^2+4)\,dx-4\int_0^1\dfrac{dx}{1+x^2}=\left(\dfrac17-\dfrac23+1-\dfrac43+4\right)-4\cdot\dfrac\pi4=\boldsymbol{\dfrac{22}7-\pi}$<br>"
         r"(2) $A=\displaystyle\int_0^1x^4(1-x)^4dx$，$B=\displaystyle\int_0^1x^6(1-x)^4dx$ とおく。展開して計算すると<br>"
         r"$A=\dfrac19-\dfrac12+\dfrac67-\dfrac23+\dfrac15=\dfrac1{630}$，　$B=\dfrac1{11}-\dfrac25+\dfrac23-\dfrac12+\dfrac17=\dfrac1{2310}$<br>"
         r"【$\pi$ の下からの評価】$0<x<1$ で $\dfrac1{1+x^2}<1$，$x^4(1-x)^4>0$ だから $I<A=\dfrac1{630}$。<br>"
         r"よって $\pi=\dfrac{22}7-I>\dfrac{22}7-\dfrac1{630}=\dfrac{1979}{630}$。$630\times3.141=1978.83$ だから $\dfrac{1979}{630}>3.141$。<br>"
         r"【$\pi$ の上からの評価】$0<x<1$ で $(1-x^2)(1+x^2)=1-x^4<1$ より $\dfrac1{1+x^2}>1-x^2$。よって<br>"
         r"$I>\displaystyle\int_0^1x^4(1-x)^4(1-x^2)\,dx=A-B=\dfrac1{630}-\dfrac1{2310}=\dfrac4{3465}$<br>"
         r"したがって $\pi<\dfrac{22}7-\dfrac4{3465}=\dfrac{10886}{3465}$。$3465\times3.142=10887.03$ だから $\dfrac{10886}{3465}<3.142$。<br>"
         r"以上より　$\boldsymbol{3.141<\pi<3.142}$",
  "note": r"上からの評価に $\dfrac1{1+x^2}\geqq\dfrac12$ を使うと $I\geqq\dfrac1{1260}$ で、$\pi\leqq\dfrac{22}7-\dfrac1{1260}=3.14206\cdots$ となり、$\pi<3.142$ は示せない。どこまで精密に評価すべきかを見極めるのが、評価問題の核心である。なお $I>0$ だけからも $\pi<\dfrac{22}7$ がわかる。",
  "ex": r"(1) 定積分 $\displaystyle\int_0^1\dfrac{(1-x)^4}{1+x^2}\,dx$ を求めよ。<br>(2) $\dfrac{47}{15}<\pi<\dfrac{22}7$ を示せ。",
  "exa": r"(1) $\dfrac{10}3-\pi$　(2) $\dfrac1{1+x^2}<1$ から $\dfrac{10}3-\pi<\dfrac15$，$\dfrac1{1+x^2}>1-x^2$ から $\dfrac{10}3-\pi>\dfrac15-\dfrac1{105}=\dfrac4{21}$"},
 {"lv": 5, "title": r"$n\displaystyle\int_0^1\dfrac{x^n}{1+x}dx$ の極限と、その近づき方",
  "q": r"$J_n=\displaystyle\int_0^1\dfrac{x^n}{1+x}\,dx$（$n=1,\ 2,\ 3,\ \cdots$）とする。<br>(1) $\displaystyle\lim_{n\to\infty}nJ_n$ を求めよ。<br>(2) $\displaystyle\lim_{n\to\infty}n\left(nJ_n-\dfrac12\right)$ を求めよ。",
  "hint": r"$x^n$ は $n$ が大きいと $x=1$ の近く以外ではほぼ $0$ なので、$nJ_n$ は $\dfrac1{1+x}$ の $x=1$ での値 $\dfrac12$ に近づくと予想できる。$x^n=\left(\dfrac{x^{n+1}}{n+1}\right)'$ として部分積分すると端の値 $\dfrac12$ が取り出され、残りは $\dfrac1n$ 程度小さい積分になる。(2) は同じ操作をもう一度行う。",
  "sol": r"自然数 $m$ に対し $K_m=\displaystyle\int_0^1\dfrac{x^m}{(1+x)^2}dx$，$L_m=\displaystyle\int_0^1\dfrac{x^m}{(1+x)^3}dx$ とおく。$0\leqq x\leqq1$ で $\dfrac1{(1+x)^2}\leqq1$，$\dfrac1{(1+x)^3}\leqq1$ だから<br>"
         r"$0<K_m\leqq\displaystyle\int_0^1x^mdx=\dfrac1{m+1}$，　$0<L_m\leqq\dfrac1{m+1}$　…①<br>"
         r"(1) 部分積分により<br>"
         r"$J_n=\left[\dfrac{x^{n+1}}{(n+1)(1+x)}\right]_0^1+\dfrac1{n+1}\displaystyle\int_0^1\dfrac{x^{n+1}}{(1+x)^2}dx=\dfrac1{2(n+1)}+\dfrac{K_{n+1}}{n+1}$　…②<br>"
         r"よって $nJ_n=\dfrac n{2(n+1)}+\dfrac n{n+1}K_{n+1}$。①より $K_{n+1}\to0$ だから　$\displaystyle\lim_{n\to\infty}nJ_n=\boldsymbol{\dfrac12}$<br>"
         r"(2) 同様に部分積分して<br>"
         r"$K_m=\left[\dfrac{x^{m+1}}{(m+1)(1+x)^2}\right]_0^1+\dfrac2{m+1}\displaystyle\int_0^1\dfrac{x^{m+1}}{(1+x)^3}dx=\dfrac1{4(m+1)}+\dfrac{2L_{m+1}}{m+1}$<br>"
         r"よって $(m+1)K_m=\dfrac14+2L_{m+1}\to\dfrac14$（①より $L_{m+1}\to0$）。<br>"
         r"②より $nJ_n-\dfrac12=\dfrac n{2(n+1)}-\dfrac12+\dfrac n{n+1}K_{n+1}=-\dfrac1{2(n+1)}+\dfrac n{n+1}K_{n+1}$ だから<br>"
         r"$n\left(nJ_n-\dfrac12\right)=-\dfrac n{2(n+1)}+\left(\dfrac n{n+1}\right)^2\cdot\dfrac{n+1}{n+2}\cdot(n+2)K_{n+1}$<br>"
         r"$(n+2)K_{n+1}\to\dfrac14$（$m=n+1$ とした）だから　$\displaystyle\lim_{n\to\infty}n\left(nJ_n-\dfrac12\right)=-\dfrac12+\dfrac14=\boldsymbol{-\dfrac14}$",
  "note": r"一般に、$f(x)$ が十分なめらかな関数なら $\displaystyle\lim_{n\to\infty}n\int_0^1x^nf(x)\,dx=f(1)$，$\displaystyle\lim_{n\to\infty}n\left(n\int_0^1x^nf(x)\,dx-f(1)\right)=-f(1)-f'(1)$ となる。$f(x)=\dfrac1{1+x}$ では $-\dfrac12+\dfrac14=-\dfrac14$。極限値だけでなく「近づく速さ」まで求めるには、部分積分で主要部を取り出す操作をくり返す。",
  "ex": r"$b_n=\displaystyle\int_0^1x^n\log(1+x)\,dx$（$n=1,\ 2,\ 3,\ \cdots$）とする。$\displaystyle\lim_{n\to\infty}nb_n$ と $\displaystyle\lim_{n\to\infty}n(nb_n-\log2)$ を求めよ。ただし、$\displaystyle\lim_{n\to\infty}n\int_0^1\dfrac{x^n}{1+x}dx=\dfrac12$ を用いてよい。",
  "exa": r"$\log2$，$-\log2-\dfrac12$"},
]})


def _v8():
    # 和の不等式
    S_ = 0.0
    for n in range(1, 3001):
        S_ += 1/n
        if n >= 2:
            assert math.log(n+1) < S_ < 1 + math.log(n)
    T_ = 0.0
    for n in range(1, 3001):
        T_ += 1/math.sqrt(n)
        if n >= 2:
            assert 2*math.sqrt(n+1) - 2 < T_ < 2*math.sqrt(n) - 1
    T_ = math.fsum(1/math.sqrt(k) for k in range(1, 10001))
    assert int(T_) == 198 and 2*math.sqrt(10001) - 2 > 198
    for k in range(1, 50):
        assert 1/(k+1) < math.log((k+1)/k) < 1/k and 1/math.sqrt(k+1) < 2*(math.sqrt(k+1)-math.sqrt(k)) < 1/math.sqrt(k)
    # (f-g)^2 による最小
    g = 6*x - 2
    assert integrate(g, (x, 0, 1)) == 1 and integrate(x*g, (x, 0, 1)) == 1 and integrate(g**2, (x, 0, 1)) == 4
    P2, P3 = 6*x**2 - 6*x + 1, 20*x**3 - 30*x**2 + 12*x - 1   # 1, x と直交
    for h in (P2, P3, sin(5*x) - integrate(sin(5*x)*(4-6*x), (x, 0, 1)) - integrate(sin(5*x)*(12*x-6), (x, 0, 1))*x):
        assert abs(N(integrate(h, (x, 0, 1)))) < 1e-12 and abs(N(integrate(x*h, (x, 0, 1)))) < 1e-12
    for _ in range(5):
        c2, c3 = random.uniform(-3, 3), random.uniform(-3, 3)
        f = g + c2*P2 + c3*P3
        assert abs(N(integrate(f, (x, 0, 1))) - 1) < 1e-12 and abs(N(integrate(x*f, (x, 0, 1))) - 1) < 1e-12
        assert N(integrate(f**2, (x, 0, 1))) > 4
    g = 12*x - 6
    assert integrate(g, (x, 0, 1)) == 0 and integrate(x*g, (x, 0, 1)) == 1 and integrate(g**2, (x, 0, 1)) == 12
    p, q = symbols("p q")
    from sympy import solve
    assert solve([p/2 + q - 1, p/3 + q/2 - 1], [p, q]) == {p: 6, q: -2}
    # |sin nx|
    nn = symbols("nn", positive=True, integer=True)
    assert simplify(diff(-exp(-t)*(sin(nn*t) + nn*cos(nn*t)), t) - (nn**2+1)*exp(-t)*sin(nn*t)) == 0
    for n in range(1, 9):
        q_ = mp.quad(lambda s: mp.e**(-s)*abs(mp.sin(n*s)), [mp.pi*k/n for k in range(n+1)])
        b = n*(1 + mp.e**(-mp.pi/n))/(n**2 + 1)
        assert abs(q_ - b*(1 - mp.e**(-mp.pi))/(1 - mp.e**(-mp.pi/n))) < 1e-20
        q2 = mp.quad(lambda s: mp.e**s*abs(mp.sin(n*mp.pi*s)), [mp.mpf(k)/n for k in range(n+1)])
        c = n*mp.pi
        f2 = (mp.e - 1)*c*(mp.e**(mp.mpf(1)/n) + 1)/((1 + c**2)*(mp.e**(mp.mpf(1)/n) - 1))
        assert abs(q2 - f2) < 1e-20
    n = mp.mpf(10)**6
    an = (1 - mp.e**(-mp.pi))*n**2/(n**2+1)*(1 + mp.e**(-mp.pi/n))/(n*(1 - mp.e**(-mp.pi/n)))
    assert abs(an - 2*(1 - mp.e**(-mp.pi))/mp.pi) < 1e-5
    c = n*mp.pi
    a2 = (mp.e - 1)*c*(mp.e**(1/n) + 1)/((1 + c**2)*(mp.e**(1/n) - 1))
    assert abs(a2 - 2*(mp.e - 1)/mp.pi) < 1e-5
    # π の評価
    num = x**4*(1-x)**4
    qq, rr = div(Poly(num, x), Poly(x**2+1, x))
    assert qq.as_expr() == x**6 - 4*x**5 + 5*x**4 - 4*x**2 + 4 and rr.as_expr() == -4
    _Q(num/(1+x**2), 0, 1, Rational(22, 7) - pi)
    assert integrate(qq.as_expr(), (x, 0, 1)) == Rational(22, 7)
    A_ = integrate(num, (x, 0, 1)); B_ = integrate(x**6*(1-x)**4, (x, 0, 1))
    assert A_ == Rational(1, 630) and B_ == Rational(1, 2310) and A_ - B_ == Rational(4, 3465)
    assert Rational(1, 9) - Rational(1, 2) + Rational(6, 7) - Rational(2, 3) + Rational(1, 5) == A_
    assert Rational(1, 11) - Rational(2, 5) + Rational(2, 3) - Rational(1, 2) + Rational(1, 7) == B_
    assert Rational(22, 7) - Rational(1, 630) == Rational(1979, 630) > Rational(3141, 1000)
    assert Rational(22, 7) - Rational(4, 3465) == Rational(10886, 3465) < Rational(3142, 1000)
    assert Rational(1979, 630) < pi < Rational(10886, 3465)
    assert Rational(22, 7) - Rational(1, 1260) > Rational(3142, 1000)
    assert integrate(num/2, (x, 0, 1)) == Rational(1, 1260)
    for v in [0.1, 0.5, 0.9, 0.999]:
        assert 1 - v**2 < 1/(1+v**2) < 1
    _Q((1-x)**4/(1+x**2), 0, 1, Rational(10, 3) - pi)
    assert integrate((1-x)**4, (x, 0, 1)) == Rational(1, 5) and integrate(x**2*(1-x)**4, (x, 0, 1)) == Rational(1, 105)
    assert Rational(10, 3) - Rational(1, 5) == Rational(47, 15) and Rational(10, 3) - Rational(4, 21) == Rational(22, 7)
    assert Rational(1, 5) - Rational(1, 105) == Rational(4, 21) and Rational(47, 15) < pi < Rational(22, 7)
    # n J_n の極限と誤差
    def Jq(n, f):
        return mp.quad(f, [0] + [1 - mp.mpf(c)/n for c in (60, 8, 1) if c < n] + [1])
    for n in [3, 10, 40]:
        Jn = Jq(n, lambda s: s**n/(1+s))
        K = Jq(n, lambda s: s**(n+1)/(1+s)**2)
        assert abs(Jn - (1/(2*mp.mpf(n+1)) + K/(n+1))) < 1e-20
        m = n + 1
        Km = Jq(n, lambda s: s**m/(1+s)**2)
        Lm1 = Jq(n, lambda s: s**(m+1)/(1+s)**3)
        assert abs(Km - (1/(4*mp.mpf(m+1)) + 2*Lm1/(m+1))) < 1e-20
        assert 0 < Km <= 1/mp.mpf(m+1) and 0 < Lm1 <= 1/mp.mpf(m+2)
    prev = None
    for n in [1000, 10000, 100000]:
        Jn = Jq(n, lambda s: s**n/(1+s))
        e1 = n*(n*Jn - mp.mpf(1)/2)
        assert abs(n*Jn - mp.mpf(1)/2) < 1/mp.mpf(n) and abs(e1 + mp.mpf(1)/4) < 3/mp.mpf(n)
        bn = Jq(n, lambda s: s**n*mp.log(1+s))
        e2 = n*(n*bn - mp.log(2))
        assert abs(n*bn - mp.log(2)) < 2/mp.mpf(n) and abs(e2 - (-mp.log(2) - mp.mpf(1)/2)) < 5/mp.mpf(n)
    # 一般の主張 -f(1)-f'(1)：f = e^x で確認
    n = 100000
    cn = Jq(n, lambda s: s**n*mp.e**s)
    assert abs(n*(n*cn - mp.e) - (-2*mp.e)) < 20/mp.mpf(n)


# ==== END SECTIONS ====

CH = {"no": 25, "sections": SEC}


def verify():
    vs = [g for n_, g in sorted(globals().items()) if n_.startswith("_v") and n_[2:].isdigit()]
    for g in vs:
        g()
    items = [it for s_ in SEC for it in s_["items"]]
    cnt = {L: sum(1 for it in items if it["lv"] == L) for L in range(1, 6)}
    print("c25:", len(SEC), "sections,", len(items), "items", cnt)
    for s_ in SEC:
        lvs = [it["lv"] for it in s_["items"]]
        assert lvs == sorted(lvs), s_["title"]          # 節の中は易しい順
    if len(SEC) == 8:   # 執筆途中（節が揃う前）は配分の検査をしない
        assert 32 <= len(items) <= 38 and cnt[5] >= 3
        assert all(cnt[L] >= 3 for L in range(1, 6))
