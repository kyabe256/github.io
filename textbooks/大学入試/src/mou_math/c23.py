r"""第23章 微分法（数学III）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。
範囲：導関数の定義と微分可能性、積・商・合成関数、三角・指数・対数関数、対数微分法、
陰関数・媒介変数表示・逆関数、高次導関数、微分係数の定義の活用と関数方程式。
（接線・増減・グラフ・最大最小・不等式などの応用は第24章）"""
import math
import random
from fractions import Fraction as Fr
from sympy import (symbols, Symbol, Rational, sqrt, sin, cos, tan, exp, log, Abs, pi, E, S,
                   diff, limit, simplify, expand, factor, solve, rem, oo, idiff, cbrt, root,
                   factorial, together, Function, nsimplify, binomial)

SEC = []

# ---------------------------------------------------------------- 図の道具
C1, CG = "#16367a", "#888888"


class _F:
    """数学座標で描いて SVG 文字列にする小さな道具（座標は Python で計算）。"""

    def __init__(s, W, H, xr, yr, m=10):
        s.W, s.H, s.m = W, H, m
        s.x0, s.x1 = xr
        s.y0, s.y1 = yr
        s.o = []

    def X(s, x):
        return round(s.m + (x - s.x0) / (s.x1 - s.x0) * (s.W - 2 * s.m), 1)

    def Y(s, y):
        return round(s.m + (s.y1 - y) / (s.y1 - s.y0) * (s.H - 2 * s.m), 1)

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

    def curve(s, f, a, b, col=C1, w=1.4, dash="", n=400):
        pts = []
        for i in range(n + 1):
            x = a + (b - a) * i / n
            y = f(x)
            if s.y0 - 1e-9 <= y <= s.y1 + 1e-9:
                pts.append(f"{s.X(x)},{s.Y(y)}")
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{d} points="' + " ".join(pts) + '"/>')

    def pt(s, x, y, col=C1, r=1.9):
        s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="{col}"/>')

    def txt(s, x, y, t, dx=0, dy=0, anc="middle", it=False, size=10, col="#222"):
        st = ' font-style="italic" font-family="serif"' if it else ""
        s.o.append(f'<text x="{round(s.X(x) + dx, 1)}" y="{round(s.Y(y) + dy, 1)}" text-anchor="{anc}" font-size="{size}" fill="{col}"{st}>{t}</text>')

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" font-size="10">'
                + "".join(s.o) + "</svg>")


def _fig_abs():
    """y=|x^2-2x| のグラフ（x=2 でとがる）"""
    g = _F(170, 120, (-0.9, 3.2), (-0.4, 2.6))
    g.axes()
    g.curve(lambda x: abs(x * x - 2 * x), -0.75, 3.1)
    g.pt(2, 0)
    g.txt(2, 0, "2", dy=11, it=True)
    g.txt(1.05, 1.45, "y=|x²−2x|", size=10, col=C1)
    return g.svg()


def _fig_x2sin():
    """y=x^2 sin(1/x) と y=±x^2"""
    g = _F(200, 140, (-0.42, 0.42), (-0.17, 0.17))
    g.axes()
    g.curve(lambda x: x * x, -0.41, 0.41, col=CG, w=0.9, dash="3,2")
    g.curve(lambda x: -x * x, -0.41, 0.41, col=CG, w=0.9, dash="3,2")
    f = lambda x: x * x * math.sin(1 / x) if x != 0 else 0.0
    g.curve(f, -0.41, -0.0005, n=3000)
    g.curve(f, 0.0005, 0.41, n=3000)
    g.txt(0.41, 0.168, "y=x²", anc="end", dy=10, size=9, col="#666")
    g.txt(0.41, -0.168, "y=−x²", anc="end", dy=-3, size=9, col="#666")
    return g.svg()


def _same(e, a, var=None, pts=(0.31, 0.77, 1.23, -0.58, 2.07, -1.41)):
    """e と a が等しいことを、simplify か複数点での数値比較で確認する。"""
    if simplify(e - a) == 0:
        return True
    var = var or sorted((e - a).free_symbols, key=str)[0]
    for v in pts:
        A, B = complex(e.subs(var, v).evalf()), complex(a.subs(var, v).evalf())
        if abs(A - B) > 1e-9 * (1 + abs(A)):
            return False
    return True


# ---------------------------------------------------------------- 節1
SEC.append({"title": r"導関数の定義と微分可能性",
"base": r"""・微分係数 $f'(a)=\displaystyle\lim_{h\to0}\dfrac{f(a+h)-f(a)}{h}=\lim_{x\to a}\dfrac{f(x)-f(a)}{x-a}$。この極限が存在するとき、$f(x)$ は $x=a$ で<b>微分可能</b>という。<br>
・$x=a$ で微分可能 $\iff$ 右側微分係数 $\displaystyle\lim_{h\to+0}\dfrac{f(a+h)-f(a)}{h}$ と左側微分係数 $\displaystyle\lim_{h\to-0}\dfrac{f(a+h)-f(a)}{h}$ が存在して一致する。<br>
・導関数 $f'(x)=\displaystyle\lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$<br>
・<b>微分可能ならば連続</b>。逆は成り立たない（$|x|$ は $x=0$ で連続だが微分可能でない）。""",
"items": [
 {"lv": 1, "title": r"定義に従って導関数を求める",
  "q": r"導関数の定義に従って、次の関数の導関数を求めよ。<br>(1) $f(x)=\sqrt{2x+1}$　　(2) $f(x)=\dfrac{1}{x^2}$",
  "hint": r"$f'(x)=\displaystyle\lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$ に代入する。そのままでは $\dfrac00$ の形なので、(1) は分子を有理化し、(2) は通分して、分母の $h$ を約分できる形にする。",
  "sol": r"(1) $\dfrac{f(x+h)-f(x)}{h}=\dfrac{\sqrt{2x+2h+1}-\sqrt{2x+1}}{h}=\dfrac{(2x+2h+1)-(2x+1)}{h\left(\sqrt{2x+2h+1}+\sqrt{2x+1}\right)}=\dfrac{2}{\sqrt{2x+2h+1}+\sqrt{2x+1}}$<br>"
         r"よって　$f'(x)=\displaystyle\lim_{h\to0}\dfrac{2}{\sqrt{2x+2h+1}+\sqrt{2x+1}}=\dfrac{2}{2\sqrt{2x+1}}=\boldsymbol{\dfrac{1}{\sqrt{2x+1}}}$　$\left(x>-\dfrac12\right)$<br>"
         r"(2) $\dfrac{f(x+h)-f(x)}{h}=\dfrac1h\left\{\dfrac{1}{(x+h)^2}-\dfrac{1}{x^2}\right\}=\dfrac{x^2-(x+h)^2}{hx^2(x+h)^2}=\dfrac{-2xh-h^2}{hx^2(x+h)^2}=\dfrac{-2x-h}{x^2(x+h)^2}$<br>"
         r"よって　$f'(x)=\displaystyle\lim_{h\to0}\dfrac{-2x-h}{x^2(x+h)^2}=\dfrac{-2x}{x^4}=\boldsymbol{-\dfrac{2}{x^3}}$　$(x\neq0)$",
  "note": r"<b>微分可能ならば連続</b>であることも定義から示せる：$f(a+h)-f(a)=\dfrac{f(a+h)-f(a)}{h}\cdot h\to f'(a)\cdot0=0$（$h\to0$）。(1) の $f(x)$ は $x=-\dfrac12$ で連続だが、差分商 $\dfrac{\sqrt{2h}}{h}$ が $h\to+0$ で発散するので微分可能でない。",
  "ex": r"導関数の定義に従って、次の関数の導関数を求めよ。<br>(1) $f(x)=\sqrt{3-x}$　　(2) $f(x)=\dfrac{1}{2x+1}$",
  "exa": r"(1) $-\dfrac{1}{2\sqrt{3-x}}$　(2) $-\dfrac{2}{(2x+1)^2}$"},
 {"lv": 2, "title": r"連続性と微分可能性の判定（絶対値を含む関数）",
  "q": r"次の関数の［　］内の $x$ の値における連続性と微分可能性を調べよ。<br>(1) $f(x)=|x^2-2x|$　$[x=2]$　　(2) $g(x)=x|x|$　$[x=0]$" + _fig_abs(),
  "hint": r"絶対値の中の符号が変わる点では、右側と左側で関数の式が異なる。差分商の極限を $h\to+0$ と $h\to-0$ に分けて計算し、<b>両者が一致するか</b>を調べる。",
  "sol": r"(1) $\displaystyle\lim_{x\to2}f(x)=|4-4|=0=f(2)$ であるから、$f(x)$ は $x=2$ で連続である。<br>"
         r"$0<|h|<2$ のとき $2+h>0$ であるから $f(2+h)=|(2+h)^2-2(2+h)|=|(2+h)h|=(2+h)|h|$。よって $\dfrac{f(2+h)-f(2)}{h}=\dfrac{(2+h)|h|}{h}$ で<br>"
         r"$\displaystyle\lim_{h\to+0}\dfrac{f(2+h)-f(2)}{h}=\lim_{h\to+0}(2+h)=2$，　$\displaystyle\lim_{h\to-0}\dfrac{f(2+h)-f(2)}{h}=\lim_{h\to-0}\{-(2+h)\}=-2$<br>"
         r"右側微分係数と左側微分係数が一致しないから、$f(x)$ は $x=2$ で<b>連続であるが微分可能でない</b>。<br>"
         r"(2) $\displaystyle\lim_{x\to0}g(x)=0=g(0)$ であるから連続。また $\dfrac{g(0+h)-g(0)}{h}=\dfrac{h|h|}{h}=|h|\to0$（$h\to0$）。<br>"
         r"よって $g(x)$ は $x=0$ で<b>連続かつ微分可能</b>で　$\boldsymbol{g'(0)=0}$",
  "note": r"(1) の $x=2$ のように微分可能でない点では、グラフが「とがる」。(2) は $x\geqq0$ で $x^2$，$x<0$ で $-x^2$ であり、原点でなめらかにつながっている。式が切り替わる点では、導関数の式に代入するのではなく<b>定義に戻って</b>調べるのが原則である。",
  "ex": r"次の関数の［　］内の $x$ の値における連続性と微分可能性を調べよ。<br>(1) $f(x)=|x^2-1|$　$[x=-1]$　　(2) $g(x)=|x|\sin x$　$[x=0]$",
  "exa": r"(1) 連続であるが微分可能でない（右側微分係数 $2$，左側微分係数 $-2$）　(2) 連続かつ微分可能で $g'(0)=0$"},
 {"lv": 3, "title": r"つなぎ目で微分可能となる条件",
  "q": r"関数 $f(x)=\begin{cases}\sqrt{x}&(x\geqq1)\\ax^2+bx&(x<1)\end{cases}$ が $x=1$ で微分可能となるように、定数 $a,\ b$ の値を定めよ。",
  "hint": r"微分可能ならば連続であるから、まず<b>連続の条件</b>で $a,\ b$ の関係式を1つ得る。次に右側微分係数と左側微分係数を<b>定義から</b>計算して一致させる。",
  "sol": r"$f(x)$ が $x=1$ で微分可能ならば $x=1$ で連続であるから $\displaystyle\lim_{x\to1-0}f(x)=f(1)$，すなわち　$a+b=1$　…①<br>"
         r"右側微分係数は　$\displaystyle\lim_{h\to+0}\dfrac{\sqrt{1+h}-1}{h}=\lim_{h\to+0}\dfrac{1}{\sqrt{1+h}+1}=\dfrac12$<br>"
         r"左側微分係数は、①を用いて<br>$\displaystyle\lim_{h\to-0}\dfrac{a(1+h)^2+b(1+h)-1}{h}=\lim_{h\to-0}\dfrac{(a+b-1)+(2a+b)h+ah^2}{h}=\lim_{h\to-0}(2a+b+ah)=2a+b$<br>"
         r"これらが一致するから　$2a+b=\dfrac12$　…②<br>"
         r"①，②を解いて　$\boldsymbol{a=-\dfrac12,\ b=\dfrac32}$<br>"
         r"逆にこのとき、①が成り立ち、右側・左側の微分係数はともに $\dfrac12$ となるから、$f(x)$ は $x=1$ で微分可能である。",
  "note": r"よくある誤りは、連続の条件①を忘れて、$x>1$ での導関数 $\dfrac{1}{2\sqrt x}$ と $x<1$ での導関数 $2ax+b$ の値を $x=1$ で一致させるだけにすること。$a+b\neq1$ なら左側の差分商の分子が $0$ に近づかず、極限は発散する。",
  "ex": r"関数 $f(x)=\begin{cases}\log x&(x\geqq1)\\ax^2+bx&(x<1)\end{cases}$ が $x=1$ で微分可能となるように、定数 $a,\ b$ の値を定めよ。",
  "exa": r"$a=1,\ b=-1$"},
 {"lv": 4, "title": r"微分可能であるが導関数が連続でない関数",
  "q": r"関数 $f(x)=\begin{cases}x^2\sin\dfrac1x&(x\neq0)\\0&(x=0)\end{cases}$ について、次のことを示せ。<br>"
       r"(1) $f(x)$ は $x=0$ で微分可能で、$f'(0)=0$ である。<br>(2) 導関数 $f'(x)$ は $x=0$ で連続でない。" + _fig_x2sin(),
  "hint": r"(1) は定義に戻り、$\left|\sin\dfrac1h\right|\leqq1$ を用いてはさみうちの原理を使う。(2) は $x\neq0$ での $f'(x)$ を計算し、$0$ に収束する数列 $x_n$ で $f'(x_n)$ が $f'(0)$ に近づかないものを見つける。",
  "sol": r"(1) $h\neq0$ のとき　$\left|\dfrac{f(h)-f(0)}{h}\right|=\left|h\sin\dfrac1h\right|\leqq|h|$<br>"
         r"$\displaystyle\lim_{h\to0}|h|=0$ であるから、はさみうちの原理より $\displaystyle\lim_{h\to0}\dfrac{f(h)-f(0)}{h}=0$。よって $f(x)$ は $x=0$ で微分可能で $f'(0)=0$ である。<br>"
         r"(2) $x\neq0$ のとき　$f'(x)=2x\sin\dfrac1x+x^2\cos\dfrac1x\cdot\left(-\dfrac{1}{x^2}\right)=2x\sin\dfrac1x-\cos\dfrac1x$<br>"
         r"$x_n=\dfrac{1}{2n\pi}$（$n$ は自然数）とおくと、$n\to\infty$ のとき $x_n\to0$ であり<br>"
         r"$f'(x_n)=\dfrac{1}{n\pi}\sin2n\pi-\cos2n\pi=-1$<br>"
         r"もし $f'(x)$ が $x=0$ で連続ならば $\displaystyle\lim_{n\to\infty}f'(x_n)=f'(0)=0$ となるはずであるが、つねに $f'(x_n)=-1$ であるから矛盾する。<br>よって、$f'(x)$ は $x=0$ で連続でない。（終）",
  "note": r"$f'(0)$ を「$x\neq0$ での $f'(x)$ の式で $x\to0$ とする」方法で求めようとすると、$\displaystyle\lim_{x\to0}\cos\dfrac1x$ が存在しないので求まらない。<b>微分係数は定義で求める</b>のが原則。グラフは $y=x^2$ と $y=-x^2$ の間を振動しながら、原点で $x$ 軸に接している。",
  "ex": r"関数 $g(x)=\begin{cases}x^3\sin\dfrac1x&(x\neq0)\\0&(x=0)\end{cases}$ について、$g'(0)$ を求めよ。また、$g'(x)$ は $x=0$ で連続かどうか調べよ。",
  "exa": r"$g'(0)=0$。$x\neq0$ で $g'(x)=3x^2\sin\dfrac1x-x\cos\dfrac1x$，$|g'(x)|\leqq3x^2+|x|\to0$ より $x=0$ で連続。"},
 {"lv": 5, "title": r"$|f(x)-f(y)|\leqq(x-y)^2$ を満たす関数（定義と分割による評価）",
  "q": r"実数全体で定義された関数 $f(x)$ が、すべての実数 $x,\ y$ に対して $|f(x)-f(y)|\leqq(x-y)^2$ を満たしている。<br>"
       r"(1) $f(x)$ はすべての実数 $x$ で微分可能であることを示し、$f'(x)$ を求めよ。<br>"
       r"(2) $f(x)$ は定数関数であることを証明せよ。ただし、「導関数がつねに $0$ である関数は定数関数である」という事実は用いないこと。",
  "hint": r"(1) は $y=x+h$ として差分商を評価する。(2) は $0$ から $x$ までを $n$ 等分し、隣り合う分点での $f$ の差を足し合わせる。各差は $\left(\dfrac xn\right)^2$ 以下なので合計は $\dfrac{x^2}{n}$ 以下となり、<b>細かく分けるほど小さくなる</b>。",
  "sol": r"(1) 任意の実数 $x$ と $h\neq0$ に対し、条件で $y=x+h$ とすると $|f(x+h)-f(x)|\leqq h^2$。よって<br>"
         r"$\left|\dfrac{f(x+h)-f(x)}{h}\right|\leqq|h|$<br>"
         r"$h\to0$ のとき右辺 $\to0$ であるから、はさみうちの原理より $\displaystyle\lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}=0$。<br>"
         r"よって $f(x)$ はすべての $x$ で微分可能で　$\boldsymbol{f'(x)=0}$<br>"
         r"(2) 実数 $x$ を1つ固定し、$n$ を自然数とする。$x_k=\dfrac{kx}{n}$（$k=0,\ 1,\ \cdots,\ n$）とおくと、$x_0=0$，$x_n=x$，$x_k-x_{k-1}=\dfrac xn$ であるから<br>"
         r"$\displaystyle|f(x)-f(0)|=\left|\sum_{k=1}^{n}\{f(x_k)-f(x_{k-1})\}\right|\leqq\sum_{k=1}^{n}|f(x_k)-f(x_{k-1})|\leqq\sum_{k=1}^{n}\left(\dfrac xn\right)^2=\dfrac{x^2}{n}$<br>"
         r"左辺は $n$ によらない値であり、この不等式はすべての自然数 $n$ について成り立つ。$n\to\infty$ とすると右辺 $\to0$ であるから $|f(x)-f(0)|\leqq0$，すなわち $f(x)=f(0)$。<br>"
         r"$x$ は任意であったから、$f(x)$ は定数関数である。（終）",
  "note": r"指数 $2$ を $\alpha>1$ に変えた $|f(x)-f(y)|\leqq|x-y|^{\alpha}$ でも、$n\left(\dfrac{|x|}{n}\right)^{\alpha}=\dfrac{|x|^{\alpha}}{n^{\alpha-1}}\to0$ から同じ結論が得られる。一方 $\alpha=1$ では $f(x)=x$ などがあり、定数とは限らない。平均値の定理（第24章）を使えば (1) から直ちに (2) が従うが、本問の分割による評価はそれを使わない、より初等的な証明である。",
  "ex": r"実数全体で定義された関数 $g(x)$ が、すべての実数 $x,\ y$ に対して $|g(x)-g(y)-2(x-y)|\leqq|x-y|\sqrt{|x-y|}$ を満たすとき、$g(x)$ を $x$ と $g(0)$ で表せ。",
  "exa": r"$g(x)=2x+g(0)$（$f(x)=g(x)-2x$ は $|f(x)-f(y)|\leqq|x-y|^{\frac32}$ を満たし、$|f(x)-f(0)|\leqq n\left(\dfrac{|x|}{n}\right)^{\frac32}=\dfrac{|x|^{\frac32}}{\sqrt n}\to0$）"},
]})


def _v1():
    x, h = symbols("x h")
    xp = Symbol("x", positive=True)
    # 例題1・練習（定義に従う）
    assert simplify(limit((sqrt(2*xp+2*h+1)-sqrt(2*xp+1))/h, h, 0) - 1/sqrt(2*xp+1)) == 0
    assert simplify(limit((1/(xp+h)**2-1/xp**2)/h, h, 0) + 2/xp**3) == 0
    assert simplify(((2*x+2*h+1)-(2*x+1))/h - 2) == 0
    assert simplify((1/(x+h)**2-1/x**2)/h - (-2*x-h)/(x**2*(x+h)**2)) == 0
    for xv in [Rational(1, 3), 1, 2]:
        assert simplify(limit((sqrt(3-xv-h)-sqrt(3-xv))/h, h, 0) + 1/(2*sqrt(3-xv))) == 0
        assert simplify(limit((1/(2*(xv+h)+1)-1/(2*xv+1))/h, h, 0) + 2/(2*xv+1)**2) == 0
    # 例題2
    f = lambda t: Abs(t**2-2*t)
    assert limit((f(2+h)-f(2))/h, h, 0, "+") == 2 and limit((f(2+h)-f(2))/h, h, 0, "-") == -2
    assert limit((h*Abs(h))/h, h, 0) == 0
    f = lambda t: Abs(t**2-1)
    assert limit((f(-1+h)-f(-1))/h, h, 0, "+") == 2 and limit((f(-1+h)-f(-1))/h, h, 0, "-") == -2
    assert limit(Abs(h)*sin(h)/h, h, 0, "+") == 0 and limit(Abs(h)*sin(h)/h, h, 0, "-") == 0
    hh = 0.37
    assert abs(abs((2+hh)**2-2*(2+hh)) - (2+hh)*abs(hh)) < 1e-12 and abs(abs((2-hh)**2-2*(2-hh)) - (2-hh)*hh) < 1e-12
    # 例題3・練習
    a, b = symbols("a b")
    sol = solve([a+b-1, 2*a+b-Rational(1, 2)], [a, b])
    assert sol == {a: Rational(-1, 2), b: Rational(3, 2)}
    assert limit((sqrt(1+h)-1)/h, h, 0, "+") == Rational(1, 2)
    A, B = sol[a], sol[b]
    assert limit((A*(1+h)**2+B*(1+h)-1)/h, h, 0, "-") == Rational(1, 2)
    assert expand(a*(1+h)**2+b*(1+h)-1) == expand((a+b-1)+(2*a+b)*h+a*h**2)
    sol = solve([a+b, 2*a+b-1], [a, b])
    assert sol == {a: 1, b: -1}
    assert limit(log(1+h)/h, h, 0, "+") == 1 and limit(((1+h)**2-(1+h))/h, h, 0, "-") == 1
    # 例題4・練習
    assert limit(h*sin(1/h), h, 0) == 0
    fp = diff(x**2*sin(1/x), x)
    assert simplify(fp - (2*x*sin(1/x)-cos(1/x))) == 0
    for n in range(1, 6):
        assert simplify(fp.subs(x, 1/(2*n*pi)) + 1) == 0
    gp = diff(x**3*sin(1/x), x)
    assert simplify(gp - (3*x**2*sin(1/x)-x*cos(1/x))) == 0
    assert limit(h**2*sin(1/h), h, 0) == 0
    for xv in [0.1, -0.01, 0.003, -0.0007]:
        assert abs(float(gp.subs(x, xv))) <= 3*xv*xv + abs(xv) + 1e-15
    # 例題5・練習（分割の評価の計算、等号のない評価を数値で）
    n = Symbol("n", positive=True)
    assert simplify(n*(x/n)**2 - x**2/n) == 0
    assert simplify(n*(xp/n)**Rational(3, 2) - xp**Rational(3, 2)/sqrt(n)) == 0
    random.seed(23)
    for _ in range(200):     # 練習：g(x)=2x+c は条件を満たす（左辺 0）
        X, Y, c = random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-3, 3)
        g = lambda t: 2*t + c
        assert abs(g(X)-g(Y)-2*(X-Y)) <= abs(X-Y)**1.5 + 1e-12


# ---------------------------------------------------------------- 節2
SEC.append({"title": r"積・商・合成関数の微分",
"base": r"""・積：$\{f(x)g(x)\}'=f'(x)g(x)+f(x)g'(x)$<br>
・商：$\left\{\dfrac{f(x)}{g(x)}\right\}'=\dfrac{f'(x)g(x)-f(x)g'(x)}{\{g(x)\}^2}$，特に $\left\{\dfrac{1}{g(x)}\right\}'=-\dfrac{g'(x)}{\{g(x)\}^2}$<br>
・合成関数：$y=f(u)$，$u=g(x)$ のとき $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$，すなわち $\{f(g(x))\}'=f'(g(x))\,g'(x)$。特に $\{(ax+b)^n\}'=na(ax+b)^{n-1}$<br>
・$r$ が有理数のとき $(x^r)'=rx^{r-1}$（$x>0$）。例：$(\sqrt x)'=\dfrac{1}{2\sqrt x}$""",
"items": [
 {"lv": 1, "title": r"積・商の導関数",
  "q": r"次の関数を微分せよ。<br>(1) $y=(2x+1)(x^2-3)$　　(2) $y=\dfrac{2x-1}{x^2+1}$　　(3) $y=\dfrac{1}{x^2+x+1}$",
  "hint": r"積・商の微分公式をそのまま用いる。(3) は分子が定数なので $\left\{\dfrac1{g(x)}\right\}'=-\dfrac{g'(x)}{\{g(x)\}^2}$ を使うと速い。",
  "sol": r"(1) $y'=2\cdot(x^2-3)+(2x+1)\cdot2x=2x^2-6+4x^2+2x=\boldsymbol{6x^2+2x-6}$<br>"
         r"(2) $y'=\dfrac{2(x^2+1)-(2x-1)\cdot2x}{(x^2+1)^2}=\dfrac{2x^2+2-4x^2+2x}{(x^2+1)^2}=\boldsymbol{\dfrac{-2x^2+2x+2}{(x^2+1)^2}}$<br>"
         r"(3) $y'=-\dfrac{(x^2+x+1)'}{(x^2+x+1)^2}=\boldsymbol{-\dfrac{2x+1}{(x^2+x+1)^2}}$",
  "note": r"商の公式は分子の引き算の順序（$f'g-fg'$）を間違えやすい。$\dfrac{f}{g}=f\cdot\dfrac1g$ と見て積の公式から導けることも確認しておこう。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=(x^3+2)(1-x^2)$　　(2) $y=\dfrac{x}{x^2-x+1}$　　(3) $y=\dfrac{1}{2x^2-3}$",
  "exa": r"(1) $-5x^4+3x^2-4x$　(2) $\dfrac{1-x^2}{(x^2-x+1)^2}$　(3) $-\dfrac{4x}{(2x^2-3)^2}$"},
 {"lv": 1, "title": r"合成関数の微分",
  "q": r"次の関数を微分せよ。<br>(1) $y=(3x^2-1)^4$　　(2) $y=\sqrt{x^2+4}$　　(3) $y=\dfrac{1}{(2x+1)^3}$",
  "hint": r"「外側の関数」と「内側の関数」に分けて $\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$。(1) は $u=3x^2-1$，(2) は $u=x^2+4$ として $y=u^{\frac12}$，(3) は $y=u^{-3}$（$u=2x+1$）と見る。",
  "sol": r"(1) $u=3x^2-1$ とおくと $y=u^4$ で　$y'=4u^3\cdot u'=4(3x^2-1)^3\cdot6x=\boldsymbol{24x(3x^2-1)^3}$<br>"
         r"(2) $y=(x^2+4)^{\frac12}$ より　$y'=\dfrac12(x^2+4)^{-\frac12}\cdot2x=\boldsymbol{\dfrac{x}{\sqrt{x^2+4}}}$<br>"
         r"(3) $y=(2x+1)^{-3}$ より　$y'=-3(2x+1)^{-4}\cdot2=\boldsymbol{-\dfrac{6}{(2x+1)^4}}$",
  "note": r"内側の関数の微分（(1) の $6x$，(3) の $2$）を掛け忘れるのが最も多い誤り。(1) を展開してから微分しても答えは同じだが、合成関数の微分の方がはるかに速い。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=(1-2x^3)^5$　　(2) $y=\sqrt{4-x^2}$　　(3) $y=\dfrac{1}{(x^2+1)^2}$",
  "exa": r"(1) $-30x^2(1-2x^3)^4$　(2) $-\dfrac{x}{\sqrt{4-x^2}}$　(3) $-\dfrac{4x}{(x^2+1)^3}$"},
 {"lv": 2, "title": r"有理数乗・無理関数の微分",
  "q": r"次の関数を微分せよ。<br>(1) $y=\sqrt[3]{x^2}$　$(x>0)$　　(2) $y=x\sqrt{1-x^2}$　$(-1<x<1)$　　(3) $y=\sqrt{\dfrac{1-x}{1+x}}$　$(-1<x<1)$",
  "hint": r"累乗根は $x^{\frac pq}$ の形に直して $(x^r)'=rx^{r-1}$ を使う。(2) は積、(3) は合成関数（外側が $\sqrt{u}$、内側が商）として微分し、最後に通分・約分して整理する。",
  "sol": r"(1) $y=x^{\frac23}$ より　$y'=\dfrac23x^{-\frac13}=\boldsymbol{\dfrac{2}{3\sqrt[3]{x}}}$<br>"
         r"(2) $y'=\sqrt{1-x^2}+x\cdot\dfrac{-2x}{2\sqrt{1-x^2}}=\dfrac{(1-x^2)-x^2}{\sqrt{1-x^2}}=\boldsymbol{\dfrac{1-2x^2}{\sqrt{1-x^2}}}$<br>"
         r"(3) $u=\dfrac{1-x}{1+x}$ とおくと $u'=\dfrac{-(1+x)-(1-x)}{(1+x)^2}=-\dfrac{2}{(1+x)^2}$ であるから<br>"
         r"$y'=\dfrac{u'}{2\sqrt u}=\dfrac12\sqrt{\dfrac{1+x}{1-x}}\cdot\left\{-\dfrac{2}{(1+x)^2}\right\}=-\dfrac{\sqrt{1+x}}{\sqrt{1-x}\,(1+x)^2}=\boldsymbol{-\dfrac{1}{(1+x)\sqrt{1-x^2}}}$",
  "note": r"$r=\dfrac pq$（$q$ は自然数，$p$ は整数）のとき、$y=x^{\frac pq}$ は $y^q=x^p$ を満たす。両辺を $x$ で微分すると $qy^{q-1}y'=px^{p-1}$ となり、$y'=\dfrac{p}{q}\cdot\dfrac{x^{p-1}}{y^{q-1}}=\dfrac pqx^{\frac pq-1}$ が得られる。これが有理数乗の公式の証明である。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=\dfrac{1}{\sqrt[4]{x}}$　$(x>0)$　　(2) $y=x^2\sqrt{x+1}$　$(x>-1)$　　(3) $y=\sqrt{\dfrac{x-1}{x+1}}$　$(x>1)$",
  "exa": r"(1) $-\dfrac{1}{4x\sqrt[4]{x}}$　(2) $\dfrac{5x^2+4x}{2\sqrt{x+1}}$　(3) $\dfrac{1}{(x+1)\sqrt{x^2-1}}$"},
 {"lv": 3, "title": r"微分を利用した整式の割り算",
  "q": r"$n$ を2以上の自然数とする。<br>(1) $x^n$ を $(x-1)^2$ で割ったときの余りを求めよ。<br>(2) 整式 $ax^{n+1}+bx^n+1$ が $(x-1)^2$ で割り切れるように、定数 $a,\ b$ の値を定めよ。",
  "hint": r"$x^n=(x-1)^2Q(x)+px+q$ の両辺を $x$ で微分すると、$\{(x-1)^2Q(x)\}'=2(x-1)Q(x)+(x-1)^2Q'(x)$ は $x=1$ で $0$ になる。もとの式と微分した式に $x=1$ を代入すれば、商 $Q(x)$ を知らなくても $p,\ q$ が決まる。",
  "sol": r"(1) 商を $Q(x)$，余りを $px+q$ とおくと　$x^n=(x-1)^2Q(x)+px+q$　…①<br>"
         r"①に $x=1$ を代入して　$1=p+q$<br>"
         r"①の両辺を $x$ で微分して　$nx^{n-1}=2(x-1)Q(x)+(x-1)^2Q'(x)+p$。$x=1$ を代入して　$n=p$<br>"
         r"よって $p=n$，$q=1-n$ で、余りは　$\boldsymbol{nx-n+1}$<br>"
         r"(2) $P(x)=ax^{n+1}+bx^n+1$ とおく。$P(x)$ が $(x-1)^2$ で割り切れるための必要十分条件は $P(1)=P'(1)=0$ である（下の検討）。<br>"
         r"$P'(x)=(n+1)ax^n+nbx^{n-1}$ より　$P(1)=a+b+1=0$，$P'(1)=(n+1)a+nb=0$<br>"
         r"第1式より $b=-a-1$。第2式に代入して $(n+1)a-n(a+1)=0$，すなわち $a=n$。<br>よって　$\boldsymbol{a=n,\ b=-n-1}$",
  "note": r"【$P(x)$ が $(x-\alpha)^2$ で割り切れる $\iff$ $P(\alpha)=P'(\alpha)=0$】　$P(x)=(x-\alpha)^2Q(x)+px+q$ とおくと、(1) と同様にして $P(\alpha)=p\alpha+q$，$P'(\alpha)=p$。よって $P(\alpha)=P'(\alpha)=0\iff p=q=0$。<br>"
          r"(1) は二項定理 $x^n=\{1+(x-1)\}^n=1+n(x-1)+{}_n\mathrm{C}_2(x-1)^2+\cdots$ からも得られる。",
  "ex": r"$n$ を2以上の自然数とする。<br>(1) $x^n$ を $(x+1)^2$ で割ったときの余りを求めよ。<br>(2) 整式 $ax^{n+2}+bx^n+1$ が $(x-1)^2$ で割り切れるように、定数 $a,\ b$ の値を定めよ。",
  "exa": r"(1) $(-1)^{n-1}(nx+n-1)$　(2) $a=\dfrac n2,\ b=-\dfrac{n+2}{2}$"},
]})


def _v2():
    x = symbols("x")
    xp = Symbol("x", positive=True)
    eq = _same
    # 例題6・練習
    assert expand(diff((2*x+1)*(x**2-3), x)) == 6*x**2+2*x-6
    assert eq(diff((2*x-1)/(x**2+1), x), (-2*x**2+2*x+2)/(x**2+1)**2)
    assert eq(diff(1/(x**2+x+1), x), -(2*x+1)/(x**2+x+1)**2)
    assert expand(diff((x**3+2)*(1-x**2), x)) == -5*x**4+3*x**2-4*x
    assert eq(diff(x/(x**2-x+1), x), (1-x**2)/(x**2-x+1)**2)
    assert eq(diff(1/(2*x**2-3), x), -4*x/(2*x**2-3)**2)
    # 例題7・練習
    assert eq(diff((3*x**2-1)**4, x), 24*x*(3*x**2-1)**3)
    assert eq(diff(sqrt(x**2+4), x), x/sqrt(x**2+4))
    assert eq(diff(1/(2*x+1)**3, x), -6/(2*x+1)**4)
    assert eq(diff((1-2*x**3)**5, x), -30*x**2*(1-2*x**3)**4)
    assert eq(diff(sqrt(4-x**2), x), -x/sqrt(4-x**2))
    assert eq(diff(1/(x**2+1)**2, x), -4*x/(x**2+1)**3)
    # 例題8・練習（区間内の数値でも確認）
    assert eq(diff(xp**Rational(2, 3), xp), 2/(3*cbrt(xp)))
    assert eq(diff(x*sqrt(1-x**2), x), (1-2*x**2)/sqrt(1-x**2))
    y3 = sqrt((1-x)/(1+x))
    a3 = -1/((1+x)*sqrt(1-x**2))
    for v in [Rational(-9, 10), Rational(-1, 3), 0, Rational(1, 2), Rational(4, 5)]:
        assert abs(float(diff(y3, x).subs(x, v) - a3.subs(x, v))) < 1e-12
        assert abs(float((-sqrt(1+x)/(sqrt(1-x)*(1+x)**2) - a3).subs(x, v))) < 1e-12
    assert eq(diff(xp**Rational(-1, 4), xp), -1/(4*xp*root(xp, 4)))
    for v in [Rational(-1, 2), 0, 1, 3]:
        assert abs(float(diff(x**2*sqrt(x+1), x).subs(x, v) - ((5*x**2+4*x)/(2*sqrt(x+1))).subs(x, v))) < 1e-12
    for v in [Rational(3, 2), 2, 5]:
        assert abs(float(diff(sqrt((x-1)/(x+1)), x).subs(x, v) - (1/((x+1)*sqrt(x**2-1))).subs(x, v))) < 1e-12
    # 例題9・練習
    a, b = symbols("a b")
    for n in range(2, 12):
        assert expand(rem(x**n, (x-1)**2, x) - (n*x-n+1)) == 0
        assert expand(rem(x**n, (x+1)**2, x) - (-1)**(n-1)*(n*x+n-1)) == 0
        assert rem(n*x**(n+1)-(n+1)*x**n+1, (x-1)**2, x) == 0
        assert rem(Rational(n, 2)*x**(n+2)-Rational(n+2, 2)*x**n+1, (x-1)**2, x) == 0
        P = a*x**(n+1)+b*x**n+1
        assert solve([P.subs(x, 1), diff(P, x).subs(x, 1)], [a, b]) == {a: n, b: -n-1}


# ---------------------------------------------------------------- 節3
SEC.append({"title": r"三角関数・指数関数・対数関数の導関数",
"base": r"""・$(\sin x)'=\cos x$，$(\cos x)'=-\sin x$，$(\tan x)'=\dfrac{1}{\cos^2x}$<br>
・$(e^x)'=e^x$，$(a^x)'=a^x\log a$，$(\log|x|)'=\dfrac1x$，$(\log_a|x|)'=\dfrac{1}{x\log a}$（$a>0$，$a\neq1$）<br>
・合成関数の形：$\{\sin(ax+b)\}'=a\cos(ax+b)$，$\{e^{g(x)}\}'=g'(x)e^{g(x)}$，$\{\log|g(x)|\}'=\dfrac{g'(x)}{g(x)}$<br>
・公式のもとになる極限：$\displaystyle\lim_{h\to0}\dfrac{\sin h}{h}=1$，$\displaystyle\lim_{t\to0}(1+t)^{\frac1t}=e$，$\displaystyle\lim_{h\to0}\dfrac{e^h-1}{h}=1$""",
"items": [
 {"lv": 1, "title": r"三角関数の導関数",
  "q": r"次の関数を微分せよ。<br>(1) $y=\sin3x$　　(2) $y=\cos^2x$　　(3) $y=\tan(2x+1)$　　(4) $y=\dfrac{1}{\tan x}$",
  "hint": r"(1)～(3) は合成関数の微分。(2) は $u=\cos x$ として $y=u^2$。(4) は $\dfrac{\cos x}{\sin x}$ と直して商の微分。",
  "sol": r"(1) $y'=\cos3x\cdot3=\boldsymbol{3\cos3x}$<br>"
         r"(2) $y'=2\cos x\cdot(-\sin x)=-2\sin x\cos x=\boldsymbol{-\sin2x}$<br>"
         r"(3) $y'=\dfrac{1}{\cos^2(2x+1)}\cdot2=\boldsymbol{\dfrac{2}{\cos^2(2x+1)}}$<br>"
         r"(4) $y=\dfrac{\cos x}{\sin x}$ より　$y'=\dfrac{-\sin x\cdot\sin x-\cos x\cdot\cos x}{\sin^2x}=\boldsymbol{-\dfrac{1}{\sin^2x}}$",
  "note": r"(2) は $\cos^2x=\dfrac{1+\cos2x}{2}$ と次数を下げてから微分しても $-\sin2x$ となる。$\sin^2x$，$\cos^2x$ の微分は2倍角の公式で簡単になることが多い。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=\cos(1-2x)$　　(2) $y=\sin^3x$　　(3) $y=\tan^2x$　　(4) $y=\dfrac{1}{\sin x}$",
  "exa": r"(1) $2\sin(1-2x)$　(2) $3\sin^2x\cos x$　(3) $\dfrac{2\tan x}{\cos^2x}$　(4) $-\dfrac{\cos x}{\sin^2x}$"},
 {"lv": 1, "title": r"指数関数・対数関数の導関数",
  "q": r"次の関数を微分せよ。<br>(1) $y=e^{-x^2}$　　(2) $y=\log(x^2+1)$　　(3) $y=2^{3x}$　　(4) $y=\log_3|2x-1|$",
  "hint": r"いずれも合成関数。$\{e^{g(x)}\}'=g'(x)e^{g(x)}$，$\{\log|g(x)|\}'=\dfrac{g'(x)}{g(x)}$。底が $e$ でないものは $(a^x)'=a^x\log a$，$(\log_a|x|)'=\dfrac{1}{x\log a}$ を使う。",
  "sol": r"(1) $y'=e^{-x^2}\cdot(-2x)=\boldsymbol{-2xe^{-x^2}}$<br>"
         r"(2) $y'=\boldsymbol{\dfrac{2x}{x^2+1}}$<br>"
         r"(3) $y'=2^{3x}\log2\cdot3=\boldsymbol{3\cdot2^{3x}\log2}$<br>"
         r"(4) $y'=\dfrac{1}{(2x-1)\log3}\cdot2=\boldsymbol{\dfrac{2}{(2x-1)\log3}}$",
  "note": r"(3) は $2^{3x}=e^{3x\log2}$ と底を $e$ にそろえて $(e^{3x\log2})'=3\log2\cdot e^{3x\log2}$ としてもよい。(4) は底の変換 $\log_3|2x-1|=\dfrac{\log|2x-1|}{\log3}$ と同じことである。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=e^{3x+1}$　　(2) $y=\log(x^2+x+1)$　　(3) $y=5^{-x}$　　(4) $y=\log_2|x^2-4|$",
  "exa": r"(1) $3e^{3x+1}$　(2) $\dfrac{2x+1}{x^2+x+1}$　(3) $-5^{-x}\log5$　(4) $\dfrac{2x}{(x^2-4)\log2}$"},
 {"lv": 2, "title": r"定義に従う導関数の公式の証明",
  "q": r"次の等式を、導関数の定義に従って証明せよ。ただし、$\displaystyle\lim_{h\to0}\dfrac{\sin h}{h}=1$，$\displaystyle\lim_{t\to0}(1+t)^{\frac1t}=e$ は用いてよい。<br>(1) $(\sin x)'=\cos x$　　(2) $(\log x)'=\dfrac1x$　$(x>0)$",
  "hint": r"(1) は和を積に直す公式 $\sin A-\sin B=2\cos\dfrac{A+B}2\sin\dfrac{A-B}{2}$ で $\dfrac{\sin\theta}{\theta}$ の形を作る。(2) は対数の性質で差を1つの対数にまとめ、$(1+t)^{\frac1t}$ の形を作る。",
  "sol": r"(1) $\sin(x+h)-\sin x=2\cos\left(x+\dfrac h2\right)\sin\dfrac h2$ であるから<br>"
         r"$\dfrac{\sin(x+h)-\sin x}{h}=\cos\left(x+\dfrac h2\right)\cdot\dfrac{\sin\frac h2}{\frac h2}$<br>"
         r"$h\to0$ のとき $\dfrac h2\to0$ であるから、これは $\cos x\cdot1=\cos x$ に収束する。よって $(\sin x)'=\cos x$。（終）<br>"
         r"(2) $x>0$ とする。$\dfrac{\log(x+h)-\log x}{h}=\dfrac1h\log\left(1+\dfrac hx\right)=\dfrac1x\cdot\dfrac xh\log\left(1+\dfrac hx\right)$<br>"
         r"$t=\dfrac hx$ とおくと、$h\to0$ のとき $t\to0$ で、上の式は $\dfrac1x\log(1+t)^{\frac1t}$ となり、$\dfrac1x\log e=\dfrac1x$ に収束する。<br>よって $(\log x)'=\dfrac1x$。（終）",
  "note": r"(2) で $\log$ が連続であることを用いた。$x<0$ のときは $\log|x|=\log(-x)$ を合成関数として微分して $\dfrac{-1}{-x}=\dfrac1x$ となり、まとめて $(\log|x|)'=\dfrac1x$ が成り立つ。",
  "ex": r"次の等式を、導関数の定義に従って証明せよ。ただし、$\displaystyle\lim_{h\to0}\dfrac{\sin h}{h}=1$，$\displaystyle\lim_{t\to0}(1+t)^{\frac1t}=e$ は用いてよい。<br>(1) $(\cos x)'=-\sin x$　　(2) $(e^x)'=e^x$",
  "exa": r"(1) $\cos(x+h)-\cos x=-2\sin\left(x+\dfrac h2\right)\sin\dfrac h2$ を用いる。　(2) $\dfrac{e^{x+h}-e^x}{h}=e^x\cdot\dfrac{e^h-1}{h}$，$t=e^h-1$ とおくと $\dfrac{e^h-1}{h}=\dfrac{1}{\log(1+t)^{\frac1t}}\to1$"},
 {"lv": 2, "title": r"いろいろな関数の導関数（結果の整理まで）",
  "q": r"次の関数を微分せよ。結果はできるだけ簡単な形で答えよ。<br>(1) $y=e^{-x}\cos2x$　　(2) $y=\log\left(x+\sqrt{x^2+1}\right)$<br>(3) $y=\dfrac{\sin x}{1+\cos x}$　　(4) $y=\log\left|\tan\dfrac x2\right|$",
  "hint": r"積・商・合成の公式を組み合わせる。微分した後、(2) は通分して約分、(3) は $\sin^2x+\cos^2x=1$，(4) は2倍角の公式 $2\sin\dfrac x2\cos\dfrac x2=\sin x$ で整理できる。",
  "sol": r"(1) $y'=-e^{-x}\cos2x+e^{-x}\cdot(-2\sin2x)=\boldsymbol{-e^{-x}(\cos2x+2\sin2x)}$<br>"
         r"(2) $y'=\dfrac{\left(x+\sqrt{x^2+1}\right)'}{x+\sqrt{x^2+1}}=\dfrac{1+\frac{x}{\sqrt{x^2+1}}}{x+\sqrt{x^2+1}}=\dfrac{\sqrt{x^2+1}+x}{\sqrt{x^2+1}\left(x+\sqrt{x^2+1}\right)}=\boldsymbol{\dfrac{1}{\sqrt{x^2+1}}}$<br>"
         r"(3) $y'=\dfrac{\cos x(1+\cos x)-\sin x\cdot(-\sin x)}{(1+\cos x)^2}=\dfrac{\cos x+\cos^2x+\sin^2x}{(1+\cos x)^2}=\dfrac{1+\cos x}{(1+\cos x)^2}=\boldsymbol{\dfrac{1}{1+\cos x}}$<br>"
         r"(4) $y'=\dfrac{\left(\tan\frac x2\right)'}{\tan\frac x2}=\dfrac{1}{2\cos^2\frac x2}\cdot\dfrac{\cos\frac x2}{\sin\frac x2}=\dfrac{1}{2\sin\frac x2\cos\frac x2}=\boldsymbol{\dfrac{1}{\sin x}}$",
  "note": r"(2)，(4) の結果は、積分法で $\displaystyle\int\dfrac{dx}{\sqrt{x^2+1}}=\log\left(x+\sqrt{x^2+1}\right)+C$，$\displaystyle\int\dfrac{dx}{\sin x}=\log\left|\tan\dfrac x2\right|+C$ として使われる。微分した結果を整理して簡単な形にする習慣が、積分の計算力にもつながる。",
  "ex": r"次の関数を微分せよ。結果はできるだけ簡単な形で答えよ。<br>(1) $y=e^{2x}\sin3x$　　(2) $y=\log\left(x+\sqrt{x^2-1}\right)$　$(x>1)$<br>(3) $y=\dfrac{\cos x}{1-\sin x}$　　(4) $y=\log\left|\dfrac{1+\sin x}{\cos x}\right|$",
  "exa": r"(1) $e^{2x}(2\sin3x+3\cos3x)$　(2) $\dfrac{1}{\sqrt{x^2-1}}$　(3) $\dfrac{1}{1-\sin x}$　(4) $\dfrac{1}{\cos x}$"},
]})


def _v3():
    h, t = symbols("h t")
    x = Symbol("x", real=True)
    xp = Symbol("x", positive=True)
    eq = _same

    def num(e, a, pts):
        for v in pts:
            assert abs(complex(e.subs(x, v)).real - complex(a.subs(x, v)).real) < 1e-10, (e, a, v)
    # 例題10・練習
    assert eq(diff(sin(3*x), x), 3*cos(3*x))
    assert eq(diff(cos(x)**2, x), -sin(2*x))
    assert eq(diff(tan(2*x+1), x), 2/cos(2*x+1)**2)
    assert eq(diff(1/tan(x), x), -1/sin(x)**2)
    assert eq(diff(cos(1-2*x), x), 2*sin(1-2*x))
    assert eq(diff(sin(x)**3, x), 3*sin(x)**2*cos(x))
    assert eq(diff(tan(x)**2, x), 2*tan(x)/cos(x)**2)
    assert eq(diff(1/sin(x), x), -cos(x)/sin(x)**2)
    # 例題11・練習
    assert eq(diff(exp(-x**2), x), -2*x*exp(-x**2))
    assert eq(diff(log(x**2+1), x), 2*x/(x**2+1))
    assert eq(diff(2**(3*x), x), 3*2**(3*x)*log(2))
    num(diff(log(Abs(2*x-1), 3), x), 2/((2*x-1)*log(3)), [-2, Rational(1, 4), 3])
    assert eq(diff(exp(3*x+1), x), 3*exp(3*x+1))
    assert eq(diff(log(x**2+x+1), x), (2*x+1)/(x**2+x+1))
    assert eq(diff(5**(-x), x), -5**(-x)*log(5))
    num(diff(log(Abs(x**2-4), 2), x), 2*x/((x**2-4)*log(2)), [-3, -1, Rational(1, 2), 5])
    # 例題12・練習（用いる恒等式と極限）
    assert eq(sin(x+h)-sin(x), 2*cos(x+h/2)*sin(h/2))
    assert eq(cos(x+h)-cos(x), -2*sin(x+h/2)*sin(h/2))
    assert limit((sin(x+h)-sin(x))/h, h, 0) == cos(x)
    assert limit((cos(x+h)-cos(x))/h, h, 0) == -sin(x)
    assert limit((log(xp+h)-log(xp))/h, h, 0) == 1/xp
    assert limit(log(1+t)/t, t, 0) == 1 and limit((exp(h)-1)/h, h, 0) == 1
    # 例題13・練習
    assert eq(diff(exp(-x)*cos(2*x), x), -exp(-x)*(cos(2*x)+2*sin(2*x)))
    assert eq(diff(log(x+sqrt(x**2+1)), x), 1/sqrt(x**2+1))
    assert eq(diff(sin(x)/(1+cos(x)), x), 1/(1+cos(x)))
    num(diff(log(Abs(tan(x/2))), x), 1/sin(x), [0.3, 1.2, 2.5, -0.7, 4.0])
    assert eq(diff(exp(2*x)*sin(3*x), x), exp(2*x)*(2*sin(3*x)+3*cos(3*x)))
    num(diff(log(x+sqrt(x**2-1)), x), 1/sqrt(x**2-1), [1.5, 2, 7])
    assert eq(diff(cos(x)/(1-sin(x)), x), 1/(1-sin(x)))
    num(diff(log(Abs((1+sin(x))/cos(x))), x), 1/cos(x), [0.3, 1.2, 2.5, -0.7, 4.0])


# ---------------------------------------------------------------- 節4
SEC.append({"title": r"対数微分法",
"base": r"""・$\{\log|f(x)|\}'=\dfrac{f'(x)}{f(x)}$<br>
・<b>対数微分法</b>：両辺の絶対値の自然対数をとってから微分する。積・商・累乗根の形の関数、$f(x)^{g(x)}$ の形の関数に有効。<br>
・$y=f(x)^{g(x)}$（$f(x)>0$）は $\log y=g(x)\log f(x)$ として微分する（$y=e^{g(x)\log f(x)}$ と変形してもよい）。<br>
・$\alpha$ が実数のとき $(x^{\alpha})'=\alpha x^{\alpha-1}$（$x>0$）：$\log y=\alpha\log x$ より $\dfrac{y'}{y}=\dfrac{\alpha}{x}$""",
"items": [
 {"lv": 2, "title": r"$x^x$ 型（底と指数に $x$ を含む関数）の微分",
  "q": r"次の関数を微分せよ。<br>(1) $y=x^x$　$(x>0)$　　(2) $y=x^{\frac1x}$　$(x>0)$",
  "hint": r"底にも指数にも $x$ があるので、$(x^n)'=nx^{n-1}$ も $(a^x)'=a^x\log a$ も使えない。$y>0$ だから両辺の自然対数をとり、「$\log y=$（指数）$\times\log$（底）」の形にしてから微分する。",
  "sol": r"(1) $x>0$ より $y>0$。両辺の自然対数をとって　$\log y=x\log x$<br>"
         r"両辺を $x$ で微分して　$\dfrac{y'}{y}=\log x+x\cdot\dfrac1x=\log x+1$<br>"
         r"よって　$y'=\boldsymbol{x^x(\log x+1)}$<br>"
         r"(2) $y>0$ であり　$\log y=\dfrac{\log x}{x}$<br>"
         r"両辺を $x$ で微分して　$\dfrac{y'}{y}=\dfrac{\frac1x\cdot x-\log x}{x^2}=\dfrac{1-\log x}{x^2}$<br>"
         r"よって　$y'=\boldsymbol{\dfrac{x^{\frac1x}(1-\log x)}{x^2}}$",
  "note": r"$(x^x)'$ を「$x\cdot x^{x-1}=x^x$」や「$x^x\log x$」とするのはどちらも誤り。前者は指数を定数、後者は底を定数とみなした結果で、正しい答えはその<b>和</b> $x^x+x^x\log x$ になっている。$y=e^{x\log x}$ と変形して合成関数として微分しても同じ結果を得る。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=x^{\sin x}$　$(x>0)$　　(2) $y=(\log x)^x$　$(x>1)$",
  "exa": r"(1) $x^{\sin x}\left(\cos x\log x+\dfrac{\sin x}{x}\right)$　(2) $(\log x)^x\left\{\log(\log x)+\dfrac{1}{\log x}\right\}$"},
 {"lv": 2, "title": r"積・商・累乗根の形の関数の微分",
  "q": r"次の関数を微分せよ。<br>(1) $y=\dfrac{(x+1)^2}{(x+2)^3(x+3)^4}$　　(2) $y=\sqrt[3]{\dfrac{(x-1)^2}{x+2}}$　$(x\neq1,\ -2)$",
  "hint": r"商の公式を何度も使うと計算が膨れる。両辺の<b>絶対値の</b>自然対数をとると、積・商・累乗が対数の和・差・定数倍に分解され、$\dfrac{y'}{y}$ が部分分数の和として簡単に求まる。",
  "sol": r"(1) $x\neq-1,\ -2,\ -3$ で考える。両辺の絶対値の自然対数をとって<br>"
         r"$\log|y|=2\log|x+1|-3\log|x+2|-4\log|x+3|$<br>"
         r"両辺を $x$ で微分して<br>"
         r"$\dfrac{y'}{y}=\dfrac{2}{x+1}-\dfrac{3}{x+2}-\dfrac{4}{x+3}=\dfrac{2(x+2)(x+3)-3(x+1)(x+3)-4(x+1)(x+2)}{(x+1)(x+2)(x+3)}=-\dfrac{5x^2+14x+5}{(x+1)(x+2)(x+3)}$<br>"
         r"よって　$y'=\dfrac{(x+1)^2}{(x+2)^3(x+3)^4}\cdot\left\{-\dfrac{5x^2+14x+5}{(x+1)(x+2)(x+3)}\right\}=\boldsymbol{-\dfrac{(x+1)(5x^2+14x+5)}{(x+2)^4(x+3)^5}}$<br>"
         r"（$x=-1$ でも、もとの関数を商の公式で微分すれば同じ式が成り立つ。）<br>"
         r"(2) 両辺の絶対値の自然対数をとって　$\log|y|=\dfrac23\log|x-1|-\dfrac13\log|x+2|$<br>"
         r"両辺を $x$ で微分して　$\dfrac{y'}{y}=\dfrac{2}{3(x-1)}-\dfrac{1}{3(x+2)}=\dfrac{2(x+2)-(x-1)}{3(x-1)(x+2)}=\dfrac{x+5}{3(x-1)(x+2)}$<br>"
         r"よって　$y'=\sqrt[3]{\dfrac{(x-1)^2}{x+2}}\cdot\dfrac{x+5}{3(x-1)(x+2)}=\boldsymbol{\dfrac{x+5}{3\sqrt[3]{(x-1)(x+2)^4}}}$",
  "note": r"$y$ が負の値をとる範囲もあるので、絶対値をつけて対数をとる。$\{\log|f(x)|\}'=\dfrac{f'(x)}{f(x)}$ は $f(x)$ の符号によらず成り立つから、絶対値をつけても計算は同じである。最後の整理では $\sqrt[3]{A}\div B=\sqrt[3]{\dfrac{A}{B^3}}$ を使った。",
  "ex": r"次の関数を微分せよ。<br>(1) $y=\dfrac{(x-1)^3}{(x+1)^2(x+2)}$　　(2) $y=\sqrt{\dfrac{x+1}{x^2+1}}$　$(x>-1)$",
  "exa": r"(1) $\dfrac{(x-1)^2(7x+11)}{(x+1)^3(x+2)^2}$　(2) $\dfrac{1-2x-x^2}{2\sqrt{x+1}\,(x^2+1)\sqrt{x^2+1}}$"},
 {"lv": 4, "title": r"対数微分法による高次の微分係数",
  "q": r"$n$ を自然数とし、$f(x)=(1+x)(1+2x)(1+3x)\cdots(1+nx)$ とする。$f'(0)$，$f''(0)$ を求めよ。",
  "hint": r"展開するのは大変。$x=0$ の近くでは各因数が正なので、対数をとると $\log f(x)=\displaystyle\sum_{k=1}^n\log(1+kx)$ と<b>和</b>になり、$\dfrac{f'(x)}{f(x)}=\displaystyle\sum_{k=1}^n\dfrac{k}{1+kx}$ が得られる。$f''$ は $f'(x)=f(x)\displaystyle\sum_{k=1}^n\dfrac{k}{1+kx}$ をさらに積の形で微分する。",
  "sol": r"$|x|<\dfrac1n$ のとき $1+kx>0$（$k=1,\ 2,\ \cdots,\ n$）であるから $f(x)>0$ で<br>"
         r"$\log f(x)=\displaystyle\sum_{k=1}^{n}\log(1+kx)$<br>"
         r"両辺を $x$ で微分して　$\dfrac{f'(x)}{f(x)}=\displaystyle\sum_{k=1}^{n}\dfrac{k}{1+kx}$，すなわち　$f'(x)=f(x)\displaystyle\sum_{k=1}^{n}\dfrac{k}{1+kx}$　…①<br>"
         r"$f(0)=1$ であるから　$f'(0)=\displaystyle\sum_{k=1}^{n}k=\boldsymbol{\dfrac{n(n+1)}{2}}$<br>"
         r"①の両辺を $x$ で微分して　$f''(x)=f'(x)\displaystyle\sum_{k=1}^{n}\dfrac{k}{1+kx}-f(x)\sum_{k=1}^{n}\dfrac{k^2}{(1+kx)^2}$<br>"
         r"$x=0$ とおいて<br>"
         r"$f''(0)=\{f'(0)\}^2-\displaystyle\sum_{k=1}^{n}k^2=\dfrac{n^2(n+1)^2}{4}-\dfrac{n(n+1)(2n+1)}{6}=\dfrac{n(n+1)\{3n(n+1)-2(2n+1)\}}{12}$<br>"
         r"$=\dfrac{n(n+1)(3n^2-n-2)}{12}=\boldsymbol{\dfrac{(n-1)n(n+1)(3n+2)}{12}}$",
  "note": r"$f(x)$ を展開したときの $x$ の係数を $a_1$，$x^2$ の係数を $a_2$ とすると $f'(0)=a_1$，$f''(0)=2a_2$ である。$a_2=\displaystyle\sum_{i<j}ij$ であり、$\left(\displaystyle\sum k\right)^2=\sum k^2+2\sum_{i<j}ij$ から上の結果と一致する。$\dfrac{f'}{f}$ が「各因数の対数微分の和」になることが、積の形の関数に対数微分法が有効な理由である。",
  "ex": r"$n$ を自然数とし、$f(x)=(1+x)(1+2x)^2(1+3x)^3\cdots(1+nx)^n$ とする。$f'(0)$，$f''(0)$ を求めよ。",
  "exa": r"$f'(0)=\dfrac{n(n+1)(2n+1)}{6}$，$f''(0)=\dfrac{(n-1)n^2(n+1)^2(n+2)}{9}$"},
]})


def _v4():
    x = Symbol("x", positive=True)
    xr = Symbol("x", real=True)
    eq = _same
    # 例題14・練習
    assert eq(diff(x**x, x), x**x*(log(x)+1))
    assert eq(diff(x**(1/x), x), x**(1/x)*(1-log(x))/x**2)
    assert eq(diff(x**sin(x), x), x**sin(x)*(cos(x)*log(x)+sin(x)/x))
    for v in [1.5, 2.7, 6.0]:
        e = diff(log(xr)**xr, xr).subs(xr, v)
        a = (log(xr)**xr*(log(log(xr))+1/log(xr))).subs(xr, v)
        assert abs(float(e - a)) < 1e-10
    # 例題15・練習
    y1 = (xr+1)**2/((xr+2)**3*(xr+3)**4)
    assert eq(diff(y1, xr), -(xr+1)*(5*xr**2+14*xr+5)/((xr+2)**4*(xr+3)**5))
    assert expand(2*(xr+2)*(xr+3)-3*(xr+1)*(xr+3)-4*(xr+1)*(xr+2)) == -(5*xr**2+14*xr+5)
    rc = lambda u: math.copysign(abs(u)**(1/3), u)      # 実数の3乗根
    for v in [-5.0, -3.0, -1.5, 0.0, 0.5, 2.0, 4.0]:
        F = lambda t: rc((t-1)**2/(t+2))
        d = 1e-6
        num_d = (F(v+d)-F(v-d))/(2*d)
        assert abs(num_d - (v+5)/(3*rc((v-1)*(v+2)**4))) < 1e-5
    assert eq(Rational(2, 3)/(xr-1)-Rational(1, 3)/(xr+2), (xr+5)/(3*(xr-1)*(xr+2)))
    y3 = (xr-1)**3/((xr+1)**2*(xr+2))
    assert eq(diff(y3, xr), (xr-1)**2*(7*xr+11)/((xr+1)**3*(xr+2)**2))
    for v in [-0.5, 0, 1, 3.5]:
        e = diff(sqrt((xr+1)/(xr**2+1)), xr).subs(xr, v)
        a = ((1-2*xr-xr**2)/(2*sqrt(xr+1)*(xr**2+1)*sqrt(xr**2+1))).subs(xr, v)
        assert abs(float(e - a)) < 1e-12
    # 例題16・練習
    for n in range(1, 9):
        f = 1
        g = 1
        for k in range(1, n+1):
            f *= (1+k*xr)
            g *= (1+k*xr)**k
        assert diff(f, xr).subs(xr, 0) == Rational(n*(n+1), 2)
        assert diff(f, xr, 2).subs(xr, 0) == Rational((n-1)*n*(n+1)*(3*n+2), 12)
        assert Rational(n*(n+1)*(3*n**2-n-2), 12) == Rational((n-1)*n*(n+1)*(3*n+2), 12)
        assert diff(g, xr).subs(xr, 0) == Rational(n*(n+1)*(2*n+1), 6)
        assert diff(g, xr, 2).subs(xr, 0) == Rational((n-1)*n**2*(n+1)**2*(n+2), 9)


# ---------------------------------------------------------------- 節5
SEC.append({"title": r"陰関数・媒介変数表示・逆関数の微分",
"base": r"""・<b>陰関数</b>：$F(x,\ y)=0$ の両辺を $x$ で微分する。$y$ を含む項は合成関数の微分：$\dfrac{d}{dx}f(y)=f'(y)\dfrac{dy}{dx}$（例：$\dfrac{d}{dx}y^2=2y\dfrac{dy}{dx}$）<br>
・<b>媒介変数表示</b> $x=f(t)$，$y=g(t)$：$\dfrac{dy}{dx}=\dfrac{\frac{dy}{dt}}{\frac{dx}{dt}}=\dfrac{g'(t)}{f'(t)}$（$f'(t)\neq0$），$\dfrac{d^2y}{dx^2}=\dfrac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{\frac{dx}{dt}}$<br>
・<b>逆関数</b>：$y=f^{-1}(x)\iff x=f(y)$ で $\dfrac{dy}{dx}=\dfrac{1}{\frac{dx}{dy}}$。$g=f^{-1}$，$b=f(a)$，$f'(a)\neq0$ のとき $g'(b)=\dfrac{1}{f'(a)}$""",
"items": [
 {"lv": 1, "title": r"陰関数の導関数",
  "q": r"次の方程式で定められる $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $x,\ y$ を用いて表せ。<br>(1) $\dfrac{x^2}{4}+y^2=1$　　(2) $y^2=4x$　　(3) $\sqrt x+\sqrt y=1$",
  "hint": r"$y$ を $x$ の関数とみて、方程式の両辺を $x$ で微分する。$y^2$ や $\sqrt y$ は合成関数として微分し、$\dfrac{dy}{dx}$ を掛けるのを忘れない。",
  "sol": r"(1) 両辺を $x$ で微分すると　$\dfrac{x}{2}+2y\dfrac{dy}{dx}=0$　よって、$y\neq0$ のとき　$\dfrac{dy}{dx}=\boldsymbol{-\dfrac{x}{4y}}$<br>"
         r"(2) 両辺を $x$ で微分すると　$2y\dfrac{dy}{dx}=4$　よって、$y\neq0$ のとき　$\dfrac{dy}{dx}=\boldsymbol{\dfrac{2}{y}}$<br>"
         r"(3) $x>0$，$y>0$ で考える。両辺を $x$ で微分すると　$\dfrac{1}{2\sqrt x}+\dfrac{1}{2\sqrt y}\cdot\dfrac{dy}{dx}=0$<br>よって　$\dfrac{dy}{dx}=\boldsymbol{-\dfrac{\sqrt y}{\sqrt x}}$",
  "note": r"(2) を $y=\pm2\sqrt x$ と解いて微分すると $y'=\pm\dfrac{1}{\sqrt x}=\dfrac{2}{\pm2\sqrt x}=\dfrac2y$ となり、上の結果と一致する。陰関数の微分を使えば、$y$ について解かずに（2つの場合に分けずに）まとめて計算できる。",
  "ex": r"次の方程式で定められる $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $x,\ y$ を用いて表せ。<br>(1) $x^2+3y^2=12$　　(2) $y^2=-6x$　　(3) $x^3+y^3=1$",
  "exa": r"(1) $-\dfrac{x}{3y}$　(2) $-\dfrac{3}{y}$　(3) $-\dfrac{x^2}{y^2}$"},
 {"lv": 2, "title": r"媒介変数表示された関数の導関数",
  "q": r"次の媒介変数表示で表された $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $t$ の式で表せ。<br>"
       r"(1) $x=\cos^3t,\ y=\sin^3t$　$\left(0<t<\dfrac\pi2\right)$　　(2) $x=\dfrac{1-t^2}{1+t^2},\ y=\dfrac{2t}{1+t^2}$　$(t>0)$",
  "hint": r"$\dfrac{dx}{dt}$，$\dfrac{dy}{dt}$ をそれぞれ求め、$\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$。$\dfrac{dx}{dt}\neq0$ であることを確認しておく。",
  "sol": r"(1) $\dfrac{dx}{dt}=3\cos^2t\cdot(-\sin t)=-3\sin t\cos^2t$，$\dfrac{dy}{dt}=3\sin^2t\cos t$<br>"
         r"$0<t<\dfrac\pi2$ では $\dfrac{dx}{dt}\neq0$ であるから　$\dfrac{dy}{dx}=\dfrac{3\sin^2t\cos t}{-3\sin t\cos^2t}=\boldsymbol{-\tan t}$<br>"
         r"(2) $\dfrac{dx}{dt}=\dfrac{-2t(1+t^2)-(1-t^2)\cdot2t}{(1+t^2)^2}=-\dfrac{4t}{(1+t^2)^2}$，$\dfrac{dy}{dt}=\dfrac{2(1+t^2)-2t\cdot2t}{(1+t^2)^2}=\dfrac{2(1-t^2)}{(1+t^2)^2}$<br>"
         r"$t>0$ では $\dfrac{dx}{dt}\neq0$ であるから　$\dfrac{dy}{dx}=\dfrac{2(1-t^2)}{-4t}=\boldsymbol{\dfrac{t^2-1}{2t}}$",
  "note": r"(2) は $x^2+y^2=1$（単位円）の媒介変数表示である。陰関数の微分で $\dfrac{dy}{dx}=-\dfrac xy=-\dfrac{1-t^2}{2t}$ となり、結果が一致することを確かめられる。",
  "ex": r"次の媒介変数表示で表された $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $t$ の式で表せ。<br>"
        r"(1) $x=2\cos t,\ y=3\sin t$　$(0<t<\pi)$　　(2) $x=t+\dfrac1t,\ y=t-\dfrac1t$　$(t>1)$",
  "exa": r"(1) $-\dfrac{3\cos t}{2\sin t}$　(2) $\dfrac{t^2+1}{t^2-1}$"},
 {"lv": 3, "title": r"逆関数の微分法と逆関数の微分係数",
  "q": r"(1) $x=\tan y$ $\left(-\dfrac\pi2<y<\dfrac\pi2\right)$ で定められる $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $x$ の式で表せ。<br>"
       r"(2) $f(x)=x^3+3x+1$ の逆関数を $g(x)$ とする。$g'(5)$，$g''(5)$ の値を求めよ。",
  "hint": r"逆関数は具体的な式で表せないことが多いので、$x=f(y)$ の形のまま $\dfrac{dy}{dx}=\dfrac{1}{dx/dy}$ を使う。(2) では、まず $f(y)=5$ となる $y$（すなわち $g(5)$）を求める。$g''$ は $\dfrac{dy}{dx}=\dfrac{1}{f'(y)}$ をさらに $x$ で微分する（$y$ の式を $x$ で微分するので合成関数の微分）。",
  "sol": r"(1) $\dfrac{dx}{dy}=\dfrac{1}{\cos^2y}=1+\tan^2y=1+x^2$（$>0$）であるから　$\dfrac{dy}{dx}=\boldsymbol{\dfrac{1}{1+x^2}}$<br>"
         r"(2) $x^3$，$3x$ はともに増加関数であるから $f(x)$ は増加関数であり、逆関数 $g(x)$ が存在する。<br>$y=g(x)$ とおくと　$x=f(y)=y^3+3y+1$<br>"
         r"$\dfrac{dx}{dy}=3y^2+3>0$ であるから　$\dfrac{dy}{dx}=\dfrac{1}{3y^2+3}$　…①<br>"
         r"$x=5$ のとき $y^3+3y+1=5$，$(y-1)(y^2+y+4)=0$。$y^2+y+4=\left(y+\dfrac12\right)^2+\dfrac{15}4>0$ より $y=1$，すなわち $g(5)=1$。<br>"
         r"①より　$g'(5)=\dfrac{1}{3+3}=\boldsymbol{\dfrac16}$<br>"
         r"①の両辺を $x$ で微分すると　$\dfrac{d^2y}{dx^2}=\dfrac{d}{dy}\left(\dfrac{1}{3y^2+3}\right)\cdot\dfrac{dy}{dx}=-\dfrac{6y}{(3y^2+3)^2}\cdot\dfrac{1}{3y^2+3}=-\dfrac{6y}{(3y^2+3)^3}$<br>"
         r"$y=1$ を代入して　$g''(5)=-\dfrac{6}{6^3}=\boldsymbol{-\dfrac{1}{36}}$",
  "note": r"一般に、$y=g(x)$ のとき $g'(x)=\dfrac{1}{f'(y)}$，$g''(x)=-\dfrac{f''(y)}{\{f'(y)\}^3}$。$g'(5)=\dfrac{1}{f'(5)}$ としてしまう誤りが多い。$f'$ に代入するのは $5$ ではなく、$f(y)=5$ を満たす $y=g(5)=1$ である。",
  "ex": r"(1) $x=\sin y$ $\left(-\dfrac\pi2<y<\dfrac\pi2\right)$ で定められる $x$ の関数 $y$ について、$\dfrac{dy}{dx}$ を $x$ の式で表せ。<br>"
        r"(2) $f(x)=x+e^x$ の逆関数を $g(x)$ とする。$g'(1)$，$g''(1)$ の値を求めよ。",
  "exa": r"(1) $\dfrac{1}{\sqrt{1-x^2}}$（$-1<x<1$）　(2) $g'(1)=\dfrac12$，$g''(1)=-\dfrac18$"},
 {"lv": 3, "title": r"陰関数の第2次導関数",
  "q": r"方程式 $x^2-xy+y^2=3$ で定められる $x$ の関数 $y$ について、$\dfrac{d^2y}{dx^2}$ を $x,\ y$ の式で表せ。ただし、$x\neq2y$ とする。",
  "hint": r"まず $y'$ を $x,\ y$ で表す。それを商の微分公式で $x$ について微分し、現れた $y'$ に先の式を代入する。最後に<b>もとの方程式 $x^2-xy+y^2=3$ を用いて</b>分子を定数にできる。",
  "sol": r"両辺を $x$ で微分すると　$2x-y-xy'+2yy'=0$，$(2y-x)y'=y-2x$<br>"
         r"$x\neq2y$ より　$y'=\dfrac{y-2x}{2y-x}$　…①<br>"
         r"①の右辺を商の微分公式で $x$ について微分すると<br>"
         r"$y''=\dfrac{(y'-2)(2y-x)-(y-2x)(2y'-1)}{(2y-x)^2}$<br>"
         r"分子 $=2yy'-xy'-4y+2x-2yy'+y+4xy'-2x=3xy'-3y=3(xy'-y)$<br>"
         r"①より　$xy'-y=\dfrac{x(y-2x)-y(2y-x)}{2y-x}=\dfrac{-2(x^2-xy+y^2)}{2y-x}=\dfrac{-6}{2y-x}$<br>"
         r"よって　$\dfrac{d^2y}{dx^2}=\dfrac{3}{(2y-x)^2}\cdot\dfrac{-6}{2y-x}=\boldsymbol{-\dfrac{18}{(2y-x)^3}}$",
  "note": r"もとの方程式を使わずに $-\dfrac{6(x^2-xy+y^2)}{(2y-x)^3}$ と答えても誤りではないが、曲線上では $x^2-xy+y^2=3$ なので簡単にできる。$y''$ の計算は「$y'$ の式を代入 → 通分 → もとの方程式で整理」が定石。",
  "ex": r"方程式 $x^2+xy+y^2=3$ で定められる $x$ の関数 $y$ について、$\dfrac{d^2y}{dx^2}$ を $x,\ y$ の式で表せ。ただし、$x\neq-2y$ とする。",
  "exa": r"$-\dfrac{18}{(x+2y)^3}$"},
 {"lv": 3, "title": r"媒介変数表示された関数の第2次導関数",
  "q": r"サイクロイド $x=t-\sin t,\ y=1-\cos t$　$(0<t<2\pi)$ について、$\dfrac{dy}{dx}$，$\dfrac{d^2y}{dx^2}$ を $t$ の式で表せ。",
  "hint": r"$\dfrac{dy}{dx}$ は $t$ の関数なので、これを $x$ で微分するには合成関数の微分で $\dfrac{d}{dx}=\dfrac{d}{dt}\cdot\dfrac{dt}{dx}$，すなわち「$t$ で微分して $\dfrac{dx}{dt}$ で割る」。",
  "sol": r"$\dfrac{dx}{dt}=1-\cos t$，$\dfrac{dy}{dt}=\sin t$。$0<t<2\pi$ では $1-\cos t>0$ であるから<br>"
         r"$\dfrac{dy}{dx}=\boldsymbol{\dfrac{\sin t}{1-\cos t}}$<br>"
         r"次に　$\dfrac{d}{dt}\left(\dfrac{\sin t}{1-\cos t}\right)=\dfrac{\cos t(1-\cos t)-\sin t\cdot\sin t}{(1-\cos t)^2}=\dfrac{\cos t-1}{(1-\cos t)^2}=-\dfrac{1}{1-\cos t}$<br>"
         r"よって　$\dfrac{d^2y}{dx^2}=\dfrac{d}{dt}\left(\dfrac{dy}{dx}\right)\cdot\dfrac{dt}{dx}=-\dfrac{1}{1-\cos t}\cdot\dfrac{1}{1-\cos t}=\boldsymbol{-\dfrac{1}{(1-\cos t)^2}}$",
  "note": r"よくある誤りは $\dfrac{d^2y}{dx^2}=\dfrac{d^2y/dt^2}{d^2x/dt^2}$ とすること（これだと $\dfrac{\cos t}{\sin t}$ となり誤り）。また、半角の公式から $\dfrac{dy}{dx}=\dfrac{2\sin\frac t2\cos\frac t2}{2\sin^2\frac t2}=\dfrac{1}{\tan\frac t2}$ とも表せる。",
  "ex": r"$x=\cos^3t,\ y=\sin^3t$　$\left(0<t<\dfrac\pi2\right)$ について、$\dfrac{d^2y}{dx^2}$ を $t$ の式で表せ。",
  "exa": r"$\dfrac{1}{3\sin t\cos^4t}$"},
]})


def _v5():
    x, y, t = symbols("x y t")
    xp, yp = symbols("x y", positive=True)
    eq = _same
    # 例題17・練習
    assert eq(idiff(x**2/4+y**2-1, y, x), -x/(4*y))
    assert eq(idiff(y**2-4*x, y, x), 2/y)
    assert eq(idiff(sqrt(xp)+sqrt(yp)-1, yp, xp), -sqrt(yp)/sqrt(xp))
    assert eq(idiff(x**2+3*y**2-12, y, x), -x/(3*y))
    assert eq(idiff(y**2+6*x, y, x), -3/y)
    assert eq(idiff(x**3+y**3-1, y, x), -x**2/y**2)
    # 例題18・練習
    P = lambda X, Y: diff(Y, t)/diff(X, t)
    assert eq(P(cos(t)**3, sin(t)**3), -tan(t))
    assert eq(P((1-t**2)/(1+t**2), 2*t/(1+t**2)), (t**2-1)/(2*t))
    assert eq(diff((1-t**2)/(1+t**2), t), -4*t/(1+t**2)**2) and eq(diff(2*t/(1+t**2), t), 2*(1-t**2)/(1+t**2)**2)
    assert eq(-((1-t**2)/(1+t**2))/(2*t/(1+t**2)), (t**2-1)/(2*t))
    assert eq(P(2*cos(t), 3*sin(t)), -3*cos(t)/(2*sin(t)))
    assert eq(P(t+1/t, t-1/t), (t**2+1)/(t**2-1))
    # 例題19・練習
    assert eq(1/diff(tan(y), y), 1/(1+tan(y)**2))
    assert eq(1/diff(sin(y), y), 1/sqrt(1-sin(y)**2), y, (0.3, -0.9, 1.2))
    assert expand((y-1)*(y**2+y+4)) == y**3+3*y-4
    for f, b, a, g1, g2 in [(y**3+3*y+1, 5, 1, Rational(1, 6), Rational(-1, 36)),
                            (y+exp(y), 1, 0, Rational(1, 2), Rational(-1, 8))]:
        assert f.subs(y, a) == b
        fp, fpp = diff(f, y), diff(f, y, 2)
        assert 1/fp.subs(y, a) == g1 and simplify(-fpp.subs(y, a)/fp.subs(y, a)**3 - g2) == 0
        # 数値で逆関数を作って差分で確認
        F = lambda u: float(f.subs(y, u))

        def G(v):
            lo, hi = -10.0, 10.0
            for _ in range(200):
                mid = (lo+hi)/2
                lo, hi = (mid, hi) if F(mid) < v else (lo, mid)
            return (lo+hi)/2
        d = 1e-3
        assert abs((G(b+d)-G(b-d))/(2*d) - float(g1)) < 1e-6
        assert abs((G(b+d)-2*G(b)+G(b-d))/d**2 - float(g2)) < 1e-4
    assert eq(diff(1/(3*y**2+3), y)*1/(3*y**2+3), -6*y/(3*y**2+3)**3)
    # 例題20・練習（曲線上の点で数値比較）
    for F_, ans in [(x**2-x*y+y**2-3, lambda X, Y: -18/(2*Y-X)**3), (x**2+x*y+y**2-3, lambda X, Y: -18/(X+2*Y)**3)]:
        y2 = idiff(F_, y, x, 2)
        for X in [-1.5, -0.4, 0.3, 1.1, 1.7]:
            for Y in solve(F_.subs(x, X), y):
                Y = complex(Y.evalf())
                if abs(Y.imag) < 1e-12:
                    Y = Y.real
                    assert abs(float(y2.subs({x: X, y: Y})) - ans(X, Y)) < 1e-9
    yp_ = Symbol("yp")       # 例題20の途中式（分子の展開）
    assert expand((yp_-2)*(2*y-x)-(y-2*x)*(2*yp_-1) - 3*(x*yp_-y)) == 0
    assert simplify(x*(y-2*x)-y*(2*y-x) + 2*(x**2-x*y+y**2)) == 0
    # 例題21・練習
    X, Y = t-sin(t), 1-cos(t)
    d1 = diff(Y, t)/diff(X, t)
    assert eq(d1, sin(t)/(1-cos(t)))
    assert eq(diff(d1, t), -1/(1-cos(t)))
    assert eq(diff(d1, t)/diff(X, t), -1/(1-cos(t))**2)
    X, Y = cos(t)**3, sin(t)**3
    d1 = diff(Y, t)/diff(X, t)
    assert eq(diff(d1, t)/diff(X, t), 1/(3*sin(t)*cos(t)**4), t, (0.2, 0.7, 1.3))


# ---------------------------------------------------------------- 節6
SEC.append({"title": r"高次導関数",
"base": r"""・第2次導関数 $y''=f''(x)=\dfrac{d^2y}{dx^2}$，第3次導関数 $y'''$，第 $n$ 次導関数 $y^{(n)}=f^{(n)}(x)=\dfrac{d^ny}{dx^n}$<br>
・$(e^{ax})^{(n)}=a^ne^{ax}$，$(\sin x)^{(n)}=\sin\left(x+\dfrac{n\pi}{2}\right)$，$(\cos x)^{(n)}=\cos\left(x+\dfrac{n\pi}{2}\right)$，$(\log x)^{(n)}=\dfrac{(-1)^{n-1}(n-1)!}{x^n}$<br>
・第 $n$ 次導関数は、何回か微分して規則を予想し、<b>数学的帰納法</b>で証明する。部分分数分解・次数下げ・三角関数の合成などで、微分しやすい形に直してから考える。<br>
・（参考）ライプニッツの公式：$(uv)^{(n)}=\displaystyle\sum_{k=0}^{n}{}_n\mathrm{C}_k\,u^{(n-k)}v^{(k)}$""",
"items": [
 {"lv": 1, "title": r"第2次・第3次導関数",
  "q": r"次の関数の第2次導関数と第3次導関数を求めよ。<br>(1) $y=x\log x$　　(2) $y=e^{-x}\sin x$",
  "hint": r"1回ずつ順に微分する。(2) は毎回積の微分になるので、$e^{-x}$ でくくって整理しながら進める。",
  "sol": r"(1) $y'=\log x+x\cdot\dfrac1x=\log x+1$ であるから　$y''=\boldsymbol{\dfrac1x}$，　$y'''=\boldsymbol{-\dfrac{1}{x^2}}$<br>"
         r"(2) $y'=-e^{-x}\sin x+e^{-x}\cos x=e^{-x}(\cos x-\sin x)$<br>"
         r"$y''=-e^{-x}(\cos x-\sin x)+e^{-x}(-\sin x-\cos x)=\boldsymbol{-2e^{-x}\cos x}$<br>"
         r"$y'''=2e^{-x}\cos x+2e^{-x}\sin x=\boldsymbol{2e^{-x}(\sin x+\cos x)}$",
  "note": r"(2) をもう1回微分すると $y^{(4)}=-2e^{-x}(\sin x+\cos x)+2e^{-x}(\cos x-\sin x)=-4e^{-x}\sin x=-4y$ となる。したがって $y^{(n+4)}=-4y^{(n)}$ で、高次導関数は4回ごとに $-4$ 倍される。",
  "ex": r"次の関数の第2次導関数と第3次導関数を求めよ。<br>(1) $y=x^2e^x$　　(2) $y=\log(x^2+1)$",
  "exa": r"(1) $y''=(x^2+4x+2)e^x$，$y'''=(x^2+6x+6)e^x$　(2) $y''=\dfrac{2(1-x^2)}{(x^2+1)^2}$，$y'''=\dfrac{4x(x^2-3)}{(x^2+1)^3}$"},
 {"lv": 2, "title": r"導関数を含む等式の証明",
  "q": r"次の関数が、［　］内の等式を満たすことを示せ。<br>"
       r"(1) $y=e^{-x}\sin2x$　$[\,y''+2y'+5y=0\,]$　　(2) $y=\log(\cos x)$ $\left(-\dfrac\pi2<x<\dfrac\pi2\right)$　$[\,y''+(y')^2+1=0\,]$",
  "hint": r"$y'$，$y''$ を計算して左辺に代入する。(1) は $e^{-x}$ でくくり、$\sin2x$，$\cos2x$ の係数がそれぞれ $0$ になることを見る。(2) は $1+\tan^2x=\dfrac{1}{\cos^2x}$ を使う。",
  "sol": r"(1) $y'=-e^{-x}\sin2x+2e^{-x}\cos2x=e^{-x}(-\sin2x+2\cos2x)$<br>"
         r"$y''=-e^{-x}(-\sin2x+2\cos2x)+e^{-x}(-2\cos2x-4\sin2x)=e^{-x}(-3\sin2x-4\cos2x)$<br>"
         r"よって　$y''+2y'+5y=e^{-x}\{(-3\sin2x-4\cos2x)+(-2\sin2x+4\cos2x)+5\sin2x\}=0$　（終）<br>"
         r"(2) $-\dfrac\pi2<x<\dfrac\pi2$ で $\cos x>0$ である。$y'=\dfrac{-\sin x}{\cos x}=-\tan x$，$y''=-\dfrac{1}{\cos^2x}=-(1+\tan^2x)$<br>"
         r"よって　$y''+(y')^2+1=-(1+\tan^2x)+\tan^2x+1=0$　（終）",
  "note": r"導関数を含む等式を<b>微分方程式</b>という。(1) のように、$e^{px}\sin qx$，$e^{px}\cos qx$ は $y''-2py'+(p^2+q^2)y=0$ を満たす（(1) は $p=-1,\ q=2$）。",
  "ex": r"次の関数が、［　］内の等式を満たすことを示せ。<br>(1) $y=e^x\cos3x$　$[\,y''-2y'+10y=0\,]$　　(2) $y=\sqrt{1+x^2}$　$[\,y^3y''=1\,]$",
  "exa": r"(1) $y'=e^x(\cos3x-3\sin3x)$，$y''=e^x(-8\cos3x-6\sin3x)$ を代入。　(2) $y'=\dfrac xy$，$y''=\dfrac{y-xy'}{y^2}=\dfrac{y^2-x^2}{y^3}=\dfrac{1}{y^3}$"},
 {"lv": 3, "title": r"第 $n$ 次導関数（部分分数分解・次数下げ）",
  "q": r"$n$ を自然数とする。次の関数の第 $n$ 次導関数を求めよ。<br>(1) $y=\dfrac{1}{x^2-1}$　　(2) $y=\cos^2x$",
  "hint": r"そのまま $n$ 回微分して規則を探すのは難しい。(1) は部分分数に分解して $\left(\dfrac{1}{x-a}\right)^{(n)}$ の公式を、(2) は半角の公式で次数を下げて $\{\cos(ax+b)\}^{(n)}$ の公式を使う。公式そのものは帰納法で示しておく。",
  "sol": r"まず　$\left(\dfrac{1}{x-a}\right)^{(n)}=\dfrac{(-1)^nn!}{(x-a)^{n+1}}$　…①　を示す。<br>"
         r"$n=1$ のとき $\left(\dfrac1{x-a}\right)'=-\dfrac{1}{(x-a)^2}$ で成り立つ。$n=k$ のとき成り立つとすると<br>"
         r"$\left(\dfrac{1}{x-a}\right)^{(k+1)}=\left\{(-1)^kk!(x-a)^{-k-1}\right\}'=(-1)^kk!\cdot(-k-1)(x-a)^{-k-2}=\dfrac{(-1)^{k+1}(k+1)!}{(x-a)^{k+2}}$<br>"
         r"となり、$n=k+1$ のときも成り立つ。よって①はすべての自然数 $n$ で成り立つ。<br>"
         r"(1) $\dfrac{1}{x^2-1}=\dfrac12\left(\dfrac{1}{x-1}-\dfrac{1}{x+1}\right)$ であるから、①より<br>"
         r"$y^{(n)}=\boldsymbol{\dfrac{(-1)^nn!}{2}\left\{\dfrac{1}{(x-1)^{n+1}}-\dfrac{1}{(x+1)^{n+1}}\right\}}$<br>"
         r"(2) $\{\cos(ax+b)\}'=-a\sin(ax+b)=a\cos\left(ax+b+\dfrac\pi2\right)$ であるから、1回微分するごとに $a$ 倍され、角が $\dfrac\pi2$ 増える。よって（帰納法により）<br>"
         r"$\{\cos(ax+b)\}^{(n)}=a^n\cos\left(ax+b+\dfrac{n\pi}{2}\right)$<br>"
         r"$y=\cos^2x=\dfrac{1+\cos2x}{2}$ であるから　$y^{(n)}=\dfrac12\cdot2^n\cos\left(2x+\dfrac{n\pi}{2}\right)=\boldsymbol{2^{n-1}\cos\left(2x+\dfrac{n\pi}{2}\right)}$",
  "note": r"(2) を $y'=-2\sin x\cos x$，$y''=\cdots$ とそのまま計算すると規則が見えにくい。<b>微分しやすい形に直してから</b> $n$ 次導関数を考えるのが鉄則。(1) で $x^2-1$ のように因数分解できる分母は、部分分数分解が第一手。",
  "ex": r"$n$ を自然数とする。次の関数の第 $n$ 次導関数を求めよ。<br>(1) $y=\dfrac{1}{x^2-3x+2}$　　(2) $y=\sin^2x$",
  "exa": r"(1) $(-1)^nn!\left\{\dfrac{1}{(x-2)^{n+1}}-\dfrac{1}{(x-1)^{n+1}}\right\}$　(2) $-2^{n-1}\cos\left(2x+\dfrac{n\pi}{2}\right)$"},
 {"lv": 4, "title": r"$e^x\sin x$ の第 $n$ 次導関数（合成と帰納法）",
  "q": r"$f(x)=e^x\sin x$ とする。<br>(1) 第 $n$ 次導関数 $f^{(n)}(x)$ を求めよ。<br>(2) $f^{(n)}(0)=0$ となる自然数 $n$ をすべて求めよ。",
  "hint": r"$f'(x)=e^x(\sin x+\cos x)$ を三角関数の合成で $\sqrt2e^x\sin\left(x+\dfrac\pi4\right)$ と表すと、「1回微分するごとに $\sqrt2$ 倍され、角が $\dfrac\pi4$ 進む」という規則が見える。これを $e^x\sin(x+\theta)$ の形の関数一般について示し、帰納法につなげる。",
  "sol": r"(1) 任意の定数 $\theta$ に対して<br>"
         r"$\{e^x\sin(x+\theta)\}'=e^x\sin(x+\theta)+e^x\cos(x+\theta)=\sqrt2e^x\sin\left(x+\theta+\dfrac\pi4\right)$　…①<br>"
         r"これから　$f^{(n)}(x)=(\sqrt2)^ne^x\sin\left(x+\dfrac{n\pi}{4}\right)$　…②　と推測し、数学的帰納法で示す。<br>"
         r"[1] $n=1$ のとき、①で $\theta=0$ として成り立つ。<br>"
         r"[2] $n=k$ のとき②が成り立つとすると、①で $\theta=\dfrac{k\pi}{4}$ として<br>"
         r"$f^{(k+1)}(x)=(\sqrt2)^k\cdot\sqrt2e^x\sin\left(x+\dfrac{k\pi}{4}+\dfrac\pi4\right)=(\sqrt2)^{k+1}e^x\sin\left(x+\dfrac{(k+1)\pi}{4}\right)$<br>"
         r"となり、$n=k+1$ のときも成り立つ。<br>"
         r"[1]，[2] より　$\boldsymbol{f^{(n)}(x)=(\sqrt2)^ne^x\sin\left(x+\dfrac{n\pi}{4}\right)}$<br>"
         r"(2) $f^{(n)}(0)=(\sqrt2)^n\sin\dfrac{n\pi}{4}$ であるから、$f^{(n)}(0)=0\iff\sin\dfrac{n\pi}{4}=0\iff\dfrac{n\pi}{4}$ が $\pi$ の整数倍 $\iff n$ が $4$ の倍数<br>"
         r"よって　$\boldsymbol{n=4m}$（$m$ は自然数）",
  "note": r"②で $n=4$ とすると $f^{(4)}(x)=4e^x\sin(x+\pi)=-4f(x)$。この節の最初の例題 (2) の $e^{-x}\sin x$ と同じく、4回微分すると $-4$ 倍になる。数学Cの複素数平面の言葉でいえば、1回の微分が $1+i=\sqrt2\left(\cos\dfrac\pi4+i\sin\dfrac\pi4\right)$ を掛けることにあたる（$\sqrt2$ 倍して $\dfrac\pi4$ 回転）。",
  "ex": r"$f(x)=e^x\cos x$ とする。第 $n$ 次導関数 $f^{(n)}(x)$ を求めよ。また、$f^{(n)}(0)=0$ となる自然数 $n$ をすべて求めよ。",
  "exa": r"$f^{(n)}(x)=(\sqrt2)^ne^x\cos\left(x+\dfrac{n\pi}{4}\right)$，$n=4m-2$（$m$ は自然数）"},
 {"lv": 4, "title": r"高次導関数の漸化式と微分係数 $f^{(n)}(0)$",
  "q": r"$f(x)=e^{-x^2}$ とし、$f^{(0)}(x)=f(x)$ と定める。<br>"
       r"(1) すべての自然数 $n$ に対して、$f^{(n+1)}(x)=-2xf^{(n)}(x)-2nf^{(n-1)}(x)$ が成り立つことを証明せよ。<br>"
       r"(2) $f^{(n)}(0)$ を求めよ。",
  "hint": r"$f^{(n)}(x)$ の具体的な式は複雑になるので、$f'(x)=-2xf(x)$ という簡単な関係式を出発点にする。積 $x\cdot f^{(k)}(x)$ を微分するたびに $f^{(k)}$ の項が1つ増えることに注目して帰納法。(2) は (1) で $x=0$ とした漸化式を、偶数番目と奇数番目に分けて解く。",
  "sol": r"(1) $f'(x)=-2xe^{-x^2}=-2xf(x)$　…①<br>"
         r"[1] $n=1$ のとき、①を微分して $f''(x)=-2f(x)-2xf'(x)=-2xf'(x)-2\cdot1\cdot f(x)$ で成り立つ。<br>"
         r"[2] $n=k$ のとき成り立つとすると $f^{(k+1)}(x)=-2xf^{(k)}(x)-2kf^{(k-1)}(x)$。両辺を微分して<br>"
         r"$f^{(k+2)}(x)=-2f^{(k)}(x)-2xf^{(k+1)}(x)-2kf^{(k)}(x)=-2xf^{(k+1)}(x)-2(k+1)f^{(k)}(x)$<br>"
         r"となり、$n=k+1$ のときも成り立つ。よって、すべての自然数 $n$ で成り立つ。（終）<br>"
         r"(2) (1) で $x=0$ とおくと　$f^{(n+1)}(0)=-2nf^{(n-1)}(0)$　…②。また $f(0)=1$，$f'(0)=0$。<br>"
         r"②より $f^{(2m+1)}(0)=-4mf^{(2m-1)}(0)$ であるから、$f'(0)=0$ から順に　$f^{(2m-1)}(0)=0$<br>"
         r"②より $f^{(2m)}(0)=-2(2m-1)f^{(2m-2)}(0)$ であるから<br>"
         r"$f^{(2m)}(0)=(-2)^m(2m-1)(2m-3)\cdots3\cdot1\cdot f(0)=(-2)^m\cdot\dfrac{(2m)!}{2^m\cdot m!}=\dfrac{(-1)^m(2m)!}{m!}$<br>"
         r"（$(2m)!$ から偶数の積 $2\cdot4\cdots(2m)=2^m\cdot m!$ を除くと奇数の積が残る。）<br>"
         r"よって　$\boldsymbol{f^{(2m-1)}(0)=0,\ \ f^{(2m)}(0)=\dfrac{(-1)^m(2m)!}{m!}}$（$m$ は自然数）",
  "note": r"(1) はライプニッツの公式を①に用いて、$\{xf(x)\}^{(n)}=xf^{(n)}(x)+nf^{(n-1)}(x)$（$x$ の2回以上の微分は $0$）としても得られる。結果は、$e^t=1+t+\dfrac{t^2}{2!}+\cdots$ に $t=-x^2$ を代入したときの $x^{2m}$ の係数 $\dfrac{(-1)^m}{m!}$ が $\dfrac{f^{(2m)}(0)}{(2m)!}$ に等しいことと合っている（参考）。",
  "ex": r"$f(x)=\dfrac{1}{1+x^2}$ とし、$f^{(0)}(x)=f(x)$ と定める。<br>(1) すべての自然数 $n$ に対して、$(1+x^2)f^{(n+1)}(x)+2(n+1)xf^{(n)}(x)+n(n+1)f^{(n-1)}(x)=0$ が成り立つことを証明せよ。<br>(2) $f^{(n)}(0)$ を求めよ。",
  "exa": r"(1) $(1+x^2)f'(x)+2xf(x)=0$ を微分して $n=1$，同様に両辺を微分して帰納法。　(2) $f^{(2m-1)}(0)=0$，$f^{(2m)}(0)=(-1)^m(2m)!$"},
 {"lv": 5, "title": r"すべての次数の微分係数が $0$ になる関数",
  "q": r"関数 $f(x)=\begin{cases}e^{-\frac{1}{x^2}}&(x\neq0)\\0&(x=0)\end{cases}$ について、次の問いに答えよ。ただし、任意の自然数 $m$ に対して $\displaystyle\lim_{t\to\infty}\dfrac{t^m}{e^t}=0$ であることは用いてよい。<br>"
       r"(1) 任意の自然数 $m$ に対して $\displaystyle\lim_{x\to0}\dfrac{1}{x^m}e^{-\frac{1}{x^2}}=0$ であることを示せ。<br>"
       r"(2) 各自然数 $n$ に対して、$x\neq0$ のとき $f^{(n)}(x)=P_n\left(\dfrac1x\right)e^{-\frac{1}{x^2}}$ となる整式 $P_n(t)$ が存在することを示せ。<br>"
       r"(3) $f(x)$ は $x=0$ で何回でも微分可能であり、すべての自然数 $n$ に対して $f^{(n)}(0)=0$ であることを示せ。",
  "hint": r"(1) は $t=\dfrac{1}{x^2}$ とおき、与えられた極限に帰着させる。(2) は $P_{n+1}$ を $P_n$ で表す漸化式を作り帰納法。(3) は「$f^{(k)}(0)=0$ が分かれば、$f^{(k+1)}(0)$ を<b>定義で</b>計算できる」という帰納法で、差分商が $\dfrac1hP_k\left(\dfrac1h\right)e^{-\frac{1}{h^2}}$ となるので (1) が使える。",
  "sol": r"(1) $x\neq0$ で $t=\dfrac{1}{x^2}$ とおくと、$x\to0$ のとき $t\to\infty$ であり　$\left|\dfrac{1}{x^m}e^{-\frac{1}{x^2}}\right|=\dfrac{t^{\frac m2}}{e^t}$<br>"
         r"$t\geqq1$ のとき $0<\dfrac{t^{\frac m2}}{e^t}\leqq\dfrac{t^m}{e^t}$ で、$\dfrac{t^m}{e^t}\to0$ であるから、はさみうちの原理より成り立つ。（終）<br>"
         r"$\displaystyle\lim_{x\to0}e^{-\frac{1}{x^2}}=0$ とあわせて、任意の整式 $Q(t)$ に対して　$\displaystyle\lim_{x\to0}Q\left(\dfrac1x\right)e^{-\frac{1}{x^2}}=0$　…①<br>"
         r"(2) $x\neq0$ のとき $f'(x)=\dfrac{2}{x^3}e^{-\frac{1}{x^2}}$ であるから、$P_1(t)=2t^3$ とすればよい。<br>"
         r"$f^{(k)}(x)=P_k\left(\dfrac1x\right)e^{-\frac{1}{x^2}}$ となる整式 $P_k(t)$ が存在するとすると<br>"
         r"$f^{(k+1)}(x)=P_k'\left(\dfrac1x\right)\cdot\left(-\dfrac{1}{x^2}\right)e^{-\frac{1}{x^2}}+P_k\left(\dfrac1x\right)\cdot\dfrac{2}{x^3}e^{-\frac{1}{x^2}}$<br>"
         r"であるから、$P_{k+1}(t)=2t^3P_k(t)-t^2P_k'(t)$ とおけば、これは整式で $f^{(k+1)}(x)=P_{k+1}\left(\dfrac1x\right)e^{-\frac{1}{x^2}}$ となる。帰納法により示された。（終）<br>"
         r"(3) $P_0(t)=1$ とおくと、(2) の式は $n=0$ でも成り立つ（$f^{(0)}=f$）。<br>"
         r"「$f(x)$ は $x=0$ で $n$ 回微分可能で $f^{(n)}(0)=0$」…(＊) を $n=0,\ 1,\ 2,\ \cdots$ について帰納法で示す。$n=0$ のときは $f(0)=0$ で成り立つ。<br>"
         r"(＊) が $n=k$ で成り立つとすると、$f^{(k)}(x)$ はすべての $x$ で定義され、$h\neq0$ に対して<br>"
         r"$\dfrac{f^{(k)}(h)-f^{(k)}(0)}{h}=\dfrac1hP_k\left(\dfrac1h\right)e^{-\frac{1}{h^2}}$<br>"
         r"$Q(t)=tP_k(t)$ は整式であるから、①より $h\to0$ のときこれは $0$ に収束する。よって $f^{(k)}(x)$ は $x=0$ で微分可能で $f^{(k+1)}(0)=0$ となり、(＊) は $n=k+1$ でも成り立つ。（終）",
  "note": r"この $f(x)$ は、$x=0$ ですべての次数の微分係数が $0$ であるのに、恒等的に $0$ ではない。整式ならば「すべての $f^{(n)}(0)=0$ なら $f=0$」であるが、一般の関数ではそうならない。関数を整式で近似する理論（テイラー展開）の限界を示す有名な例で、グラフは原点の近くで極めて平らになる。",
  "ex": r"関数 $g(x)=\begin{cases}e^{-\frac1x}&(x>0)\\0&(x\leqq0)\end{cases}$ は $x=0$ で何回でも微分可能であり、すべての自然数 $n$ に対して $g^{(n)}(0)=0$ であることを示せ。ただし、任意の自然数 $m$ に対して $\displaystyle\lim_{t\to\infty}\dfrac{t^m}{e^t}=0$ であることは用いてよい。",
  "exa": r"$x>0$ で $g^{(n)}(x)=Q_n\left(\dfrac1x\right)e^{-\frac1x}$，$Q_{n+1}(t)=t^2\{Q_n(t)-Q_n'(t)\}$（整式）。右側の差分商 $\dfrac1hQ_n\left(\dfrac1h\right)e^{-\frac1h}\to0$（$h\to+0$），左側の差分商は $0$ なので、帰納法で $g^{(n)}(0)=0$。"},
]})


def _v6():
    x = Symbol("x", real=True)
    xp = Symbol("x", positive=True)
    t = Symbol("t")
    eq = _same
    # 例題22・練習
    assert eq(diff(xp*log(xp), xp, 2), 1/xp) and eq(diff(xp*log(xp), xp, 3), -1/xp**2)
    y = exp(-x)*sin(x)
    assert eq(diff(y, x), exp(-x)*(cos(x)-sin(x)))
    assert eq(diff(y, x, 2), -2*exp(-x)*cos(x)) and eq(diff(y, x, 3), 2*exp(-x)*(sin(x)+cos(x)))
    assert eq(diff(y, x, 4), -4*y)
    assert eq(diff(x**2*exp(x), x, 2), (x**2+4*x+2)*exp(x)) and eq(diff(x**2*exp(x), x, 3), (x**2+6*x+6)*exp(x))
    assert eq(diff(log(x**2+1), x, 2), 2*(1-x**2)/(x**2+1)**2) and eq(diff(log(x**2+1), x, 3), 4*x*(x**2-3)/(x**2+1)**3)
    # 例題23・練習
    y = exp(-x)*sin(2*x)
    assert eq(diff(y, x), exp(-x)*(-sin(2*x)+2*cos(2*x))) and eq(diff(y, x, 2), exp(-x)*(-3*sin(2*x)-4*cos(2*x)))
    assert eq(diff(y, x, 2)+2*diff(y, x)+5*y, S(0))
    y = log(cos(x))
    assert eq(diff(y, x, 2)+diff(y, x)**2+1, S(0), x, (0.2, -0.9, 1.3))
    y = exp(x)*cos(3*x)
    assert eq(diff(y, x), exp(x)*(cos(3*x)-3*sin(3*x))) and eq(diff(y, x, 2), exp(x)*(-8*cos(3*x)-6*sin(3*x)))
    assert eq(diff(y, x, 2)-2*diff(y, x)+10*y, S(0))
    y = sqrt(1+x**2)
    assert eq(y**3*diff(y, x, 2), S(1))
    # 例題24・練習
    for n in range(1, 7):
        assert eq(diff(1/(x**2-1), x, n), Rational((-1)**n, 2)*factorial(n)*(1/(x-1)**(n+1)-1/(x+1)**(n+1)), x, (0.3, 2.5, -3.1))
        assert eq(diff(cos(x)**2, x, n), 2**(n-1)*cos(2*x+n*pi/2))
        assert eq(diff(1/(x**2-3*x+2), x, n), (-1)**n*factorial(n)*(1/(x-2)**(n+1)-1/(x-1)**(n+1)), x, (0.3, 1.5, -3.1, 4.2))
        assert eq(diff(sin(x)**2, x, n), -2**(n-1)*cos(2*x+n*pi/2))
        assert eq(diff(1/(x-3), x, n), (-1)**n*factorial(n)/(x-3)**(n+1), x, (0.3, 5.5))
    # 例題25・練習
    for n in range(1, 11):
        assert eq(diff(exp(x)*sin(x), x, n), sqrt(2)**n*exp(x)*sin(x+n*pi/4))
        assert eq(diff(exp(x)*cos(x), x, n), sqrt(2)**n*exp(x)*cos(x+n*pi/4))
    for n in range(1, 41):
        assert (sin(n*pi/4) == 0) == (n % 4 == 0)
        assert (cos(n*pi/4) == 0) == (n % 4 == 2)
    # 例題26・練習
    f = exp(-x**2)
    g = 1/(1+x**2)
    D = [f] + [diff(f, x, k) for k in range(1, 13)]
    E_ = [g] + [diff(g, x, k) for k in range(1, 13)]
    for n in range(1, 12):
        assert simplify(D[n+1] + 2*x*D[n] + 2*n*D[n-1]) == 0
        assert simplify((1+x**2)*E_[n+1] + 2*(n+1)*x*E_[n] + n*(n+1)*E_[n-1]) == 0
    for m in range(1, 6):
        assert D[2*m-1].subs(x, 0) == 0 and D[2*m].subs(x, 0) == (-1)**m*factorial(2*m)/factorial(m)
        assert E_[2*m-1].subs(x, 0) == 0 and E_[2*m].subs(x, 0) == (-1)**m*factorial(2*m)
        prod_odd = 1
        for j in range(1, 2*m, 2):
            prod_odd *= j
        assert prod_odd == factorial(2*m)/(2**m*factorial(m))
    # 例題27・練習
    P = [S(1)]
    Q = [S(1)]
    for n in range(1, 6):
        P.append(expand(2*t**3*P[-1] - t**2*diff(P[-1], t)))
        Q.append(expand(t**2*(Q[-1] - diff(Q[-1], t))))
    assert P[1] == 2*t**3 and Q[1] == t**2
    for n in range(1, 5):
        assert eq(diff(exp(-1/x**2), x, n), P[n].subs(t, 1/x)*exp(-1/x**2), x, (0.4, -0.7, 1.3, 2.2))
        assert eq(diff(exp(-1/xp), xp, n), Q[n].subs(t, 1/xp)*exp(-1/xp), xp, (0.4, 0.9, 2.2))
    for m in range(1, 7):
        assert limit(exp(-1/x**2)/x**m, x, 0, "+") == 0 and limit(exp(-1/x**2)/x**m, x, 0, "-") == 0
        assert limit(exp(-1/xp)/xp**m, xp, 0, "+") == 0
    for n in range(0, 4):     # 差分商 (1/h)P_n(1/h)e^{-1/h^2} → 0
        assert limit((t*P[n]).subs(t, 1/x)*exp(-1/x**2), x, 0, "+") == 0
        assert limit((t*P[n]).subs(t, 1/x)*exp(-1/x**2), x, 0, "-") == 0
        assert limit((t*Q[n]).subs(t, 1/xp)*exp(-1/xp), xp, 0, "+") == 0


# ---------------------------------------------------------------- 節7
SEC.append({"title": r"微分係数の定義の活用と関数方程式",
"base": r"""・$\displaystyle\lim_{x\to a}\dfrac{f(x)-f(a)}{x-a}=f'(a)$，$\displaystyle\lim_{h\to0}\dfrac{f(a+ph)-f(a)}{h}=pf'(a)$（$p$ は $0$ でない定数）。極限の計算に「微分係数の形」を見つけて使う。<br>
・<b>関数方程式</b>の定石：① $x=y=0$ などを代入して $f(0)$ を求める　② 導関数の定義の式の $f(x+h)$ に関数方程式を用い、$f'(x)$ を $f'(0)$ などで表す　③ 得られた関係式から $f(x)$ を決める<br>
・すべての $x$ で $g'(x)=0$ ならば $g(x)$ は定数関数（平均値の定理から導かれる。第24章）""",
"items": [
 {"lv": 2, "title": r"微分係数の定義を利用する極限",
  "q": r"次の極限値を求めよ。<br>(1) $\displaystyle\lim_{x\to\frac\pi6}\dfrac{2\sin x-1}{6x-\pi}$　　(2) $\displaystyle\lim_{x\to1}\dfrac{\log x}{x^2-1}$　　(3) $\displaystyle\lim_{x\to0}\dfrac{3^x-1}{x}$",
  "hint": r"$\displaystyle\lim_{x\to a}\dfrac{f(x)-f(a)}{x-a}=f'(a)$ の形を見つける。(1) は $f(x)=\sin x$，$a=\dfrac\pi6$，(2) は $f(x)=\log x$，$a=1$，(3) は $f(x)=3^x$，$a=0$ とみる。",
  "sol": r"(1) $f(x)=\sin x$ とおくと $f\left(\dfrac\pi6\right)=\dfrac12$ であるから<br>"
         r"$\dfrac{2\sin x-1}{6x-\pi}=\dfrac{2\left(\sin x-\frac12\right)}{6\left(x-\frac\pi6\right)}=\dfrac13\cdot\dfrac{f(x)-f\left(\frac\pi6\right)}{x-\frac\pi6}\to\dfrac13f'\left(\dfrac\pi6\right)=\dfrac13\cos\dfrac\pi6=\boldsymbol{\dfrac{\sqrt3}{6}}$<br>"
         r"(2) $f(x)=\log x$ とおくと $f(1)=0$ であるから<br>"
         r"$\dfrac{\log x}{x^2-1}=\dfrac{1}{x+1}\cdot\dfrac{f(x)-f(1)}{x-1}\to\dfrac12f'(1)=\boldsymbol{\dfrac12}$<br>"
         r"(3) $f(x)=3^x$ とおくと $f(0)=1$ であるから<br>"
         r"$\dfrac{3^x-1}{x}=\dfrac{f(x)-f(0)}{x-0}\to f'(0)=3^0\log3=\boldsymbol{\log3}$",
  "note": r"(3) は $3^x=e^{x\log3}$ として $\displaystyle\lim_{t\to0}\dfrac{e^t-1}{t}=1$ を使っても求まる。微分係数の定義は、導関数の公式を「極限の公式集」として使えることを意味している。",
  "ex": r"次の極限値を求めよ。<br>(1) $\displaystyle\lim_{x\to\frac\pi4}\dfrac{\tan x-1}{4x-\pi}$　　(2) $\displaystyle\lim_{x\to e}\dfrac{\log x-1}{x-e}$　　(3) $\displaystyle\lim_{x\to0}\dfrac{e^{2x}-1}{\sin x}$",
  "exa": r"(1) $\dfrac12$　(2) $\dfrac1e$　(3) $2$"},
 {"lv": 3, "title": r"抽象的な関数の微分係数と極限",
  "q": r"関数 $f(x)$ は $x=a$ で微分可能であるとする。次の極限を $a$，$f(a)$，$f'(a)$ を用いて表せ。<br>"
       r"(1) $\displaystyle\lim_{h\to0}\dfrac{f(a+3h)-f(a-h)}{h}$　　(2) $\displaystyle\lim_{x\to a}\dfrac{x^2f(a)-a^2f(x)}{x-a}$",
  "hint": r"(1) は分子に $f(a)$ を引いて足し、$\dfrac{f(a+3h)-f(a)}{3h}$ と $\dfrac{f(a-h)-f(a)}{-h}$ を作る。(2) は $a^2f(a)$ を引いて足し、$x^2-a^2$ の部分と $f(x)-f(a)$ の部分に分ける。",
  "sol": r"(1) $\dfrac{f(a+3h)-f(a-h)}{h}=\dfrac{\{f(a+3h)-f(a)\}-\{f(a-h)-f(a)\}}{h}=3\cdot\dfrac{f(a+3h)-f(a)}{3h}+\dfrac{f(a-h)-f(a)}{-h}$<br>"
         r"$h\to0$ のとき $3h\to0$，$-h\to0$ であるから　(与式)$=3f'(a)+f'(a)=\boldsymbol{4f'(a)}$<br>"
         r"(2) $x^2f(a)-a^2f(x)=(x^2-a^2)f(a)-a^2\{f(x)-f(a)\}$ であるから<br>"
         r"$\dfrac{x^2f(a)-a^2f(x)}{x-a}=(x+a)f(a)-a^2\cdot\dfrac{f(x)-f(a)}{x-a}\to\boldsymbol{2af(a)-a^2f'(a)}$",
  "note": r"逆に $\displaystyle\lim_{h\to0}\dfrac{f(a+h)-f(a-h)}{2h}$ が存在しても、$f(x)$ が $x=a$ で微分可能とは限らない。例えば $f(x)=|x|$，$a=0$ ではこの極限は $0$ であるが、$f'(0)$ は存在しない。(1) で2つの極限に分けられるのは、$f'(a)$ の存在を仮定しているからである。",
  "ex": r"関数 $f(x)$ は $x=a$ で微分可能であるとする。次の極限を $a$，$f(a)$，$f'(a)$ を用いて表せ。<br>"
        r"(1) $\displaystyle\lim_{h\to0}\dfrac{f(a+2h)-f(a-3h)}{h}$　　(2) $\displaystyle\lim_{x\to a}\dfrac{e^xf(a)-e^af(x)}{x-a}$",
  "exa": r"(1) $5f'(a)$　(2) $e^a\{f(a)-f'(a)\}$"},
 {"lv": 4, "title": r"関数方程式から導関数と関数を求める",
  "q": r"実数全体で定義された関数 $f(x)$ が、すべての実数 $x,\ y$ に対して $f(x+y)=f(x)e^y+f(y)e^x$ を満たし、さらに $x=0$ で微分可能で $f'(0)=1$ であるとする。<br>"
       r"(1) $f(0)$ を求めよ。<br>"
       r"(2) $f(x)$ はすべての $x$ で微分可能であることを示し、$f'(x)$ を $f(x)$ を用いて表せ。<br>"
       r"(3) $f(x)$ を求めよ。ただし、すべての $x$ で $g'(x)=0$ となる関数 $g(x)$ は定数関数であることを用いてよい。",
  "hint": r"(1) は $x=y=0$ を代入。(2) は差分商 $\dfrac{f(x+h)-f(x)}{h}$ の $f(x+h)$ に関数方程式を用い、$\displaystyle\lim_{h\to0}\dfrac{f(h)-f(0)}{h}=f'(0)$ と $\displaystyle\lim_{h\to0}\dfrac{e^h-1}{h}=1$ に帰着させる。(3) は $f'(x)-f(x)=e^x$ の左辺が $e^x\{e^{-x}f(x)\}'$ であることに注目する。",
  "sol": r"(1) $x=y=0$ を代入すると $f(0)=2f(0)$。よって　$\boldsymbol{f(0)=0}$<br>"
         r"(2) 任意の $x$ と $h\neq0$ に対して、(1) を用いると<br>"
         r"$\dfrac{f(x+h)-f(x)}{h}=\dfrac{f(x)e^h+f(h)e^x-f(x)}{h}=f(x)\cdot\dfrac{e^h-1}{h}+e^x\cdot\dfrac{f(h)-f(0)}{h}$<br>"
         r"$h\to0$ のとき右辺は $f(x)\cdot1+e^x\cdot f'(0)=f(x)+e^x$ に収束する。<br>"
         r"よって $f(x)$ はすべての $x$ で微分可能で　$\boldsymbol{f'(x)=f(x)+e^x}$<br>"
         r"(3) $g(x)=e^{-x}f(x)-x$ とおくと<br>"
         r"$g'(x)=-e^{-x}f(x)+e^{-x}f'(x)-1=e^{-x}\{f'(x)-f(x)\}-1=e^{-x}\cdot e^x-1=0$<br>"
         r"よって $g(x)$ は定数関数で、$g(x)=g(0)=f(0)-0=0$。したがって　$\boldsymbol{f(x)=xe^x}$<br>"
         r"逆に $f(x)=xe^x$ は $f(x)e^y+f(y)e^x=(x+y)e^{x+y}=f(x+y)$，$f'(0)=1$ を満たす。",
  "note": r"$f(x)$ の微分可能性は $x=0$ でしか仮定されていないが、関数方程式によって $x=0$ の情報がすべての $x$ に「運ばれる」。なお $g(x)=e^{-x}f(x)$ とおくと関数方程式は $g(x+y)=g(x)+g(y)$ となり、$g'(x)=g'(0)=1$ が同様に示せる。",
  "ex": r"実数全体で定義された関数 $f(x)$ が、すべての実数 $x,\ y$ に対して $f(x+y)=f(x)+f(y)+xy(x+y)$ を満たし、$x=0$ で微分可能で $f'(0)=2$ であるとする。$f'(x)$ と $f(x)$ を求めよ。（例題と同じ事実を用いてよい）",
  "exa": r"$f'(x)=x^2+2$，$f(x)=\dfrac{x^3}{3}+2x$"},
 {"lv": 5, "title": r"加法定理型の関数方程式",
  "q": r"実数全体で定義された関数 $f(x)$，$g(x)$ が、すべての実数 $x,\ y$ に対して<br>"
       r"$f(x+y)=f(x)f(y)-g(x)g(y)$，　$g(x+y)=g(x)f(y)+f(x)g(y)$<br>"
       r"を満たし、さらに $f(x)$，$g(x)$ は $x=0$ で微分可能で $f'(0)=0$，$g'(0)=1$ であるとする。<br>"
       r"(1) $f(0)=1$，$g(0)=0$ であることを示せ。<br>"
       r"(2) $f(x)$，$g(x)$ はすべての $x$ で微分可能で、$f'(x)=-g(x)$，$g'(x)=f(x)$ であることを示せ。<br>"
       r"(3) $f(x)=\cos x$，$g(x)=\sin x$ であることを示せ。ただし、すべての $x$ で $u'(x)=0$ となる関数 $u(x)$ は定数関数であることを用いてよい。",
  "hint": r"(1) は $x=y=0$ を代入して $f(0)$，$g(0)$ の連立方程式を作り、条件に合わない解を除く（$f(0)=0$ の場合は $y=0$ の代入で $f,\ g$ が恒等的に $0$ になる）。(2) は前の例題と同じく定義の式に加法の式を代入する。(3) は $\cos x$，$\sin x$ も同じ微分の関係を満たすので、<b>差の2乗和</b> $u(x)=\{f(x)-\cos x\}^2+\{g(x)-\sin x\}^2$ を考える。",
  "sol": r"(1) $x=y=0$ を代入すると　$f(0)=\{f(0)\}^2-\{g(0)\}^2$　…①，　$g(0)=2f(0)g(0)$　…②<br>"
         r"$g(0)\neq0$ とすると、②より $f(0)=\dfrac12$ で、①より $\{g(0)\}^2=\dfrac14-\dfrac12<0$ となり不合理。よって $g(0)=0$ で、①より $f(0)=0$ または $1$。<br>"
         r"$f(0)=0$ とすると、与えられた式で $y=0$ として、すべての $x$ で $f(x)=f(x)f(0)-g(x)g(0)=0$，$g(x)=g(x)f(0)+f(x)g(0)=0$。これは $g'(0)=1$ に反する。<br>"
         r"よって　$f(0)=1$，$g(0)=0$　（終）<br>"
         r"(2) 任意の $x$ と $h\neq0$ に対して<br>"
         r"$\dfrac{f(x+h)-f(x)}{h}=\dfrac{f(x)f(h)-g(x)g(h)-f(x)}{h}=f(x)\cdot\dfrac{f(h)-f(0)}{h}-g(x)\cdot\dfrac{g(h)-g(0)}{h}$<br>"
         r"$\to f(x)f'(0)-g(x)g'(0)=-g(x)$　（$h\to0$）<br>"
         r"$\dfrac{g(x+h)-g(x)}{h}=\dfrac{g(x)f(h)+f(x)g(h)-g(x)}{h}=g(x)\cdot\dfrac{f(h)-f(0)}{h}+f(x)\cdot\dfrac{g(h)-g(0)}{h}$<br>"
         r"$\to g(x)f'(0)+f(x)g'(0)=f(x)$　（$h\to0$）<br>"
         r"よって $f(x)$，$g(x)$ はすべての $x$ で微分可能で、$f'(x)=-g(x)$，$g'(x)=f(x)$ である。（終）<br>"
         r"(3) $u(x)=\{f(x)-\cos x\}^2+\{g(x)-\sin x\}^2$ とおくと、(2) より<br>"
         r"$u'(x)=2\{f(x)-\cos x\}\{f'(x)+\sin x\}+2\{g(x)-\sin x\}\{g'(x)-\cos x\}$<br>"
         r"$=2\{f(x)-\cos x\}\{-g(x)+\sin x\}+2\{g(x)-\sin x\}\{f(x)-\cos x\}=0$<br>"
         r"よって $u(x)$ は定数関数で、(1) より $u(x)=u(0)=(1-1)^2+(0-0)^2=0$。<br>"
         r"$f(x)-\cos x$，$g(x)-\sin x$ は実数であるから、ともに $0$。すなわち $f(x)=\cos x$，$g(x)=\sin x$。（終）",
  "note": r"加法定理と原点での微分係数だけで $\cos x$，$\sin x$ が特徴づけられる。(3) で2つの関数の差を2乗和で1つの関数 $u$ にまとめるのがポイントで、「導関数が $0$ なら定数」を1回使うだけで済む。同様に $\{f(x)^2+g(x)^2\}'=2ff'+2gg'=0$ から $f(x)^2+g(x)^2=1$ も分かる。",
  "ex": r"実数全体で定義された関数 $f(x)$，$g(x)$ が、すべての実数 $x,\ y$ に対して $f(x+y)=f(x)f(y)+g(x)g(y)$，$g(x+y)=g(x)f(y)+f(x)g(y)$ を満たし、$x=0$ で微分可能で $f'(0)=0$，$g'(0)=1$ であるとする。$f(x)$，$g(x)$ を求めよ。（例題と同じ事実を用いてよい）",
  "exa": r"$f(x)=\dfrac{e^x+e^{-x}}{2}$，$g(x)=\dfrac{e^x-e^{-x}}{2}$（$f(0)=1$，$g(0)=0$ を示し（$g(0)\neq0$ なら $f=\pm g$ となり $f'(0)=\pm g'(0)$ に反する）、$f'=g$，$g'=f$ から $\{e^{-x}(f+g)\}'=0$，$\{e^{x}(f-g)\}'=0$）"},
 {"lv": 5, "title": r"微分係数の定義と和の極限",
  "q": r"関数 $f(x)$ は $-1<x\leqq1$ で定義され、$x=0$ で微分可能で $f(0)=0$ であるとする。<br>"
       r"(1) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}f\left(\dfrac{k}{n^2}\right)=\dfrac{f'(0)}{2}$ であることを証明せよ。<br>"
       r"(2) $\displaystyle\lim_{n\to\infty}\left(1+\dfrac{1}{n^2}\right)\left(1+\dfrac{2}{n^2}\right)\left(1+\dfrac{3}{n^2}\right)\cdots\left(1+\dfrac{n}{n^2}\right)$ を求めよ。",
  "hint": r"$h$ が小さいとき $f(h)\fallingdotseq f'(0)h$ なので、和はおよそ $f'(0)\displaystyle\sum_{k=1}^n\dfrac{k}{n^2}=f'(0)\cdot\dfrac{n+1}{2n}$。<b>誤差を厳密に扱う</b>ため $f(h)=h\{f'(0)+\varepsilon(h)\}$（$\varepsilon(h)\to0$）と書き、$n$ 個の誤差の和を $|\varepsilon|$ の最大値で一括して評価する。(2) は対数をとって (1) を $f(x)=\log(1+x)$ に用いる。",
  "sol": r"(1) $h\neq0$ に対して $\varepsilon(h)=\dfrac{f(h)}{h}-f'(0)$ とおくと、$f(0)=0$ より $\varepsilon(h)=\dfrac{f(h)-f(0)}{h}-f'(0)$ であり、$\displaystyle\lim_{h\to0}\varepsilon(h)=0$。また $f(h)=h\{f'(0)+\varepsilon(h)\}$ である。よって<br>"
         r"$S_n=\displaystyle\sum_{k=1}^{n}f\left(\dfrac{k}{n^2}\right)=f'(0)\sum_{k=1}^{n}\dfrac{k}{n^2}+\sum_{k=1}^{n}\dfrac{k}{n^2}\varepsilon\left(\dfrac{k}{n^2}\right)=f'(0)\cdot\dfrac{n+1}{2n}+R_n$<br>"
         r"（$R_n$ は第2項の和）。$\left|\varepsilon\left(\dfrac{1}{n^2}\right)\right|,\ \left|\varepsilon\left(\dfrac{2}{n^2}\right)\right|,\ \cdots,\ \left|\varepsilon\left(\dfrac{n}{n^2}\right)\right|$ のうち最大のものを $M_n=\left|\varepsilon\left(\dfrac{k_n}{n^2}\right)\right|$（$1\leqq k_n\leqq n$）とすると<br>"
         r"$|R_n|\leqq\displaystyle\sum_{k=1}^{n}\dfrac{k}{n^2}M_n=\dfrac{n+1}{2n}M_n$<br>"
         r"$0<\dfrac{k_n}{n^2}\leqq\dfrac1n$ より $n\to\infty$ のとき $\dfrac{k_n}{n^2}\to0$ であるから、$M_n\to0$。よって $R_n\to0$ で<br>"
         r"$\displaystyle\lim_{n\to\infty}S_n=f'(0)\cdot\dfrac12=\dfrac{f'(0)}{2}$　（終）<br>"
         r"(2) 与えられた積を $P_n$ とすると $P_n>0$ で　$\log P_n=\displaystyle\sum_{k=1}^{n}\log\left(1+\dfrac{k}{n^2}\right)$<br>"
         r"$f(x)=\log(1+x)$ は $f(0)=0$，$f'(0)=\dfrac{1}{1+0}=1$ を満たすから、(1) より $\log P_n\to\dfrac12$。<br>"
         r"よって　$\displaystyle\lim_{n\to\infty}P_n=e^{\frac12}=\boldsymbol{\sqrt e}$",
  "note": r"「$f(h)\fallingdotseq f'(0)h$ を代入して $\dfrac{f'(0)}{2}$」は答えの見当としては正しいが、それだけでは証明にならない。項の個数 $n$ が増えていくので、個々の誤差が小さくても和が小さいとは限らないからである。本問では各誤差が「$\dfrac{k}{n^2}$ と小さい数の積」の形で、その重み $\dfrac{k}{n^2}$ の和 $\dfrac{n+1}{2n}$ が有界なので和も $0$ に近づく。$f$ に必要なのは $x=0$ での微分可能性だけである。",
  "ex": r"関数 $f(x)$ は $-1<x\leqq1$ で定義され、$x=0$ で微分可能で $f(0)=0$ であるとする。<br>(1) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}f\left(\dfrac{k^2}{n^3}\right)$ を $f'(0)$ で表せ。<br>"
        r"(2) $\displaystyle\lim_{n\to\infty}\left(1+\dfrac{1^2}{n^3}\right)\left(1+\dfrac{2^2}{n^3}\right)\cdots\left(1+\dfrac{n^2}{n^3}\right)$ を求めよ。",
  "exa": r"(1) $\dfrac{f'(0)}{3}$　(2) $\sqrt[3]{e}$"},
]})


def _v7():
    x, y, h = symbols("x y h")
    a = Symbol("a", real=True)
    eq = _same
    # 例題28・練習
    assert simplify(limit((2*sin(x)-1)/(6*x-pi), x, pi/6) - sqrt(3)/6) == 0
    assert limit(log(x)/(x**2-1), x, 1) == Rational(1, 2)
    assert simplify(limit((3**x-1)/x, x, 0) - log(3)) == 0
    assert limit((tan(x)-1)/(4*x-pi), x, pi/4) == Rational(1, 2)
    assert limit((log(x)-1)/(x-E), x, E) == 1/E
    assert limit((exp(2*x)-1)/sin(x), x, 0) == 2
    # 例題29・練習（具体的な関数でいくつか確認）
    for f in [lambda u: u**3 + sin(u), lambda u: exp(2*u) - u, lambda u: log(u + 3)]:
        for av in [Rational(1, 2), 1, 2]:
            fp = diff(f(x), x).subs(x, av)
            assert simplify(limit((f(av+3*h)-f(av-h))/h, h, 0) - 4*fp) == 0
            assert simplify(limit((x**2*f(av)-av**2*f(x))/(x-av), x, av) - (2*av*f(av)-av**2*fp)) == 0
            assert simplify(limit((f(av+2*h)-f(av-3*h))/h, h, 0) - 5*fp) == 0
            assert simplify(limit((exp(x)*f(av)-exp(av)*f(x))/(x-av), x, av) - exp(av)*(f(av)-fp)) == 0
    assert limit((Abs(h)-Abs(-h))/(2*h), h, 0) == 0
    # 例題30・練習
    F = lambda u: u*exp(u)
    assert simplify(F(x+y) - (F(x)*exp(y)+F(y)*exp(x))) == 0
    assert diff(F(x), x).subs(x, 0) == 1 and simplify(diff(F(x), x) - (F(x)+exp(x))) == 0
    assert limit((exp(h)-1)/h, h, 0) == 1
    G = lambda u: u**3/3 + 2*u
    assert expand(G(x+y) - (G(x)+G(y)+x*y*(x+y))) == 0
    assert diff(G(x), x).subs(x, 0) == 2 and expand(diff(G(x), x) - (x**2+2)) == 0
    assert expand((G(h) + x*h*(x+h))/h - (G(h)/h + x**2 + x*h)) == 0
    # 例題31・練習
    assert simplify(cos(x+y) - (cos(x)*cos(y)-sin(x)*sin(y))) == 0
    assert simplify(sin(x+y) - (sin(x)*cos(y)+cos(x)*sin(y))) == 0
    f0, g0 = symbols("f0 g0", real=True)
    assert set(map(tuple, solve([f0-f0**2+g0**2, g0-2*f0*g0], [f0, g0]))) == {(0, 0), (1, 0)}
    sols = solve([f0-f0**2-g0**2, g0-2*f0*g0], [f0, g0])
    assert set(map(tuple, sols)) == {(0, 0), (1, 0), (Rational(1, 2), Rational(1, 2)), (Rational(1, 2), Rational(-1, 2))}
    fF, gF = Function("f")(x), Function("g")(x)
    u = (fF-cos(x))**2 + (gF-sin(x))**2
    du = diff(u, x).subs({diff(fF, x): -gF, diff(gF, x): fF})
    assert expand(du) == 0
    ch, sh = (exp(x)+exp(-x))/2, (exp(x)-exp(-x))/2
    assert simplify(ch.subs(x, x+y) - (ch*ch.subs(x, y)+sh*sh.subs(x, y))) == 0
    assert simplify(sh.subs(x, x+y) - (sh*ch.subs(x, y)+ch*sh.subs(x, y))) == 0
    assert diff(ch, x).subs(x, 0) == 0 and diff(sh, x).subs(x, 0) == 1
    assert simplify(diff(exp(-x)*(fF+gF), x).subs({diff(fF, x): gF, diff(gF, x): fF})) == 0
    assert simplify(diff(exp(x)*(fF-gF), x).subs({diff(fF, x): gF, diff(gF, x): fF})) == 0
    # 例題32・練習
    n = Symbol("n", positive=True, integer=True)
    k = Symbol("k", positive=True, integer=True)
    from sympy import summation
    assert simplify(summation(k/n**2, (k, 1, n)) - (n+1)/(2*n)) == 0
    assert limit(summation(k**2/n**3, (k, 1, n)), n, oo) == Rational(1, 3)
    N = 40000
    s1 = sum(math.log1p(j/N**2) for j in range(1, N+1))
    s2 = sum(math.log1p(j*j/N**3) for j in range(1, N+1))
    s3 = sum(math.sin(j/N**2) + (j/N**2)**2 for j in range(1, N+1))   # f'(0)=1 の別の関数
    assert abs(s1 - 0.5) < 1e-4 and abs(math.exp(s1) - math.sqrt(math.e)) < 1e-3
    assert abs(s2 - 1/3) < 1e-4 and abs(math.exp(s2) - math.e**(1/3)) < 1e-3
    assert abs(s3 - 0.5) < 1e-4


CH = {"no": 23, "sections": SEC}


def verify():
    for v in [g for k, g in sorted(globals().items()) if k.startswith("_v") and callable(g)]:
        v()
    items = [it for s in SEC for it in s["items"]]
    lv = [it["lv"] for it in items]
    cnt = {k: lv.count(k) for k in range(1, 6)}
    assert 27 <= len(items) <= 33 and 4 <= len(SEC) <= 9
    assert cnt[5] >= 3 and all(cnt[k] >= 3 for k in range(1, 6))
    for s in SEC:                      # 節の中は易しい順
        ls = [it["lv"] for it in s["items"]]
        assert ls == sorted(ls), s["title"]
    print("c23:", len(items), "題", cnt)
